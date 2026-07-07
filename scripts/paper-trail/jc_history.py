#!/usr/bin/env python3
# Copyright 2026 Nextstepuni
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Paper Trail — Junior Cycle History (JC004, new spec 2022–2025): PAGE-RUN maps.

COVERAGE.md recorded JC History as "DBQ/essay" (no per-question key). That note
is stale for the new-spec Junior Cycle scheme: every answer page in the scheme
is stamped with a left-margin "Q N" table header, and the paper has clean
"Question N" headers (1..8, one to three pages each). The scheme's per-question
answer is therefore the contiguous RUN of pages stamped with that question's
marker — no essay-rubric sharing at all (wave10-style, but simpler).

Safety: COUNT RECONCILE — every paper question must own a non-empty page run,
the runs must be contiguous and in order, and together they must tile the
scheme's answer band (front matter before the first run; the Irish-bonus
appendix after the last). Anything else drops the whole paper. Coordinates
only, sidecar schema v1.

Usage: python3 jc_history.py            # maps corpus years, writes answers/<year>/
"""
import json
import os
import re
import sys

import fitz  # pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
CORPUS = os.path.join(REPO, "paper-trail-corpus")
ANSWERS_DIR = os.path.join(HERE, "answers")

SIDECAR_V = 1
COPYRIGHT = "© State Examinations Commission"
FILEID = "JC004CLP000EV.pdf"
YEARS = range(2022, 2026)
MARK_X = 170

PQ_RE = re.compile(r"^Question\s+(\d{1,2})\b")
SQ_RE = re.compile(r"^Q\s?(\d{1,2})$")


def lines_with_pos(page):
    H = page.rect.height
    out = []
    for blk in page.get_text("dict")["blocks"]:
        if blk.get("type") != 0:
            continue
        for ln in blk.get("lines", []):
            txt = "".join(sp["text"] for sp in ln.get("spans", [])).strip()
            if txt:
                out.append((txt, ln["bbox"][0], ln["bbox"][1] / H))
    out.sort(key=lambda t: t[2])
    return out


def paper_headers(doc):
    """{n: (page0, yFrac)} first 'Question N' header; must be clean 1..N."""
    seen = {}
    for pi in range(len(doc)):
        for t, x, y in lines_with_pos(doc[pi]):
            if x >= MARK_X:
                continue
            m = PQ_RE.match(t)
            if m:
                n = int(m.group(1))
                if n not in seen:
                    seen[n] = (pi, y)
    ns = sorted(seen)
    if not ns or ns != list(range(1, len(ns) + 1)) or len(ns) < 3:
        return None
    pts = [seen[n] for n in ns]
    if any(pts[i] >= pts[i + 1] for i in range(len(pts) - 1)):
        return None
    return seen


def scheme_runs(doc):
    """{n: (firstPage0, yFrac, lastPage0)} from per-page 'Q N' stamps.
    Every stamped page belongs to exactly one question; runs must be
    contiguous, ordered 1..N, and gap-free between first and last stamp."""
    stamps = []   # (page0, n, yFrac) — at most one accepted stamp per page
    for pi in range(len(doc)):
        page_stamp = None
        for t, x, y in lines_with_pos(doc[pi]):
            if x >= MARK_X:
                continue
            m = SQ_RE.match(t)
            if m and y < 0.3:
                page_stamp = (pi, int(m.group(1)), y)
                break
        if page_stamp:
            stamps.append(page_stamp)
    if not stamps:
        return None
    runs = {}
    order = []
    for pi, n, y in stamps:
        if n not in runs:
            runs[n] = [pi, y, pi]
            order.append(n)
        else:
            if pi != runs[n][2] + 1 or order[-1] != n:
                return None       # non-contiguous / interleaved stamps
            runs[n][2] = pi
    ns = sorted(runs)
    if ns != list(range(1, len(ns) + 1)) or order != ns:
        return None
    # runs must tile: question n+1 starts on the page after n's last
    for a, b in zip(ns, ns[1:]):
        if runs[b][0] != runs[a][2] + 1:
            return None
    return {n: tuple(v) for n, v in runs.items()}


def build_sidecar(paper_path, scheme_path):
    paper = fitz.open(paper_path)
    scheme = fitz.open(scheme_path)

    headers = paper_headers(paper)
    if headers is None:
        return None, "no clean 'Question 1..N' paper sequence"
    runs = scheme_runs(scheme)
    if runs is None:
        return None, "scheme 'Q N' page stamps do not form clean runs"
    if set(headers) != set(runs):
        return None, (f"count reconcile failed: paper {sorted(headers)} "
                      f"vs scheme {sorted(runs)}")

    by_page = {}
    for n, (pi, y) in headers.items():
        by_page.setdefault(pi, []).append(y)
    for pi in by_page:
        by_page[pi].sort()

    qout = []
    for n in sorted(headers):
        p_pi, p_y = headers[n]
        nxt = next((yy for yy in by_page[p_pi] if yy > p_y + 1e-6), 1.0)
        s_pi, s_y, e_pi = runs[n]
        region = [{"p": s_pi + 1, "r": [0.0, round(s_y, 4), 1.0, 1.0]}]
        for mid in range(s_pi + 1, e_pi + 1):
            region.append({"p": mid + 1, "r": [0.0, 0.0, 1.0, 1.0]})
        qout.append({"n": str(n), "pP": p_pi + 1,
                     "pY": [round(p_y, 4), round(nxt, 4)],
                     "region": region, "mode": "crop", "conf": 1.0})

    return {
        "v": SIDECAR_V,
        "paperFileid": os.path.basename(paper_path),
        "schemeFileid": os.path.basename(scheme_path),
        "component": "",
        "band": [1, len(scheme) + 1],
        "copyright": COPYRIGHT,
        "q": qout,
    }, None


def qa_echo(paper_path, scheme_path, sidecar):
    paper, scheme = fitz.open(paper_path), fitz.open(scheme_path)
    for q in sidecar["q"]:
        pg = paper[q["pP"] - 1]
        W, H = pg.rect.width, pg.rect.height
        pt = pg.get_text(clip=fitz.Rect(0, q["pY"][0] * H, W, min(q["pY"][0] + 0.25, 1) * H))
        pt = " ".join(pt.split())[:70]
        seg = q["region"][0]
        sg = scheme[seg["p"] - 1]
        W, H = sg.rect.width, sg.rect.height
        st = sg.get_text(clip=fitz.Rect(0, seg["r"][1] * H, W, min(seg["r"][1] + 0.25, 1) * H))
        st = " ".join(st.split())[:70]
        pages = [s["p"] for s in q["region"]]
        print(f"    Q{q['n']} paper p{q['pP']}: {pt!r}")
        print(f"       scheme p{pages}: {st!r}")


def main():
    wrote = 0
    for year in YEARS:
        ppath = os.path.join(CORPUS, "exampapers", str(year), FILEID)
        spath = os.path.join(CORPUS, "markingschemes", str(year), FILEID)
        if not (os.path.exists(ppath) and os.path.exists(spath)):
            continue
        sidecar, reason = build_sidecar(ppath, spath)
        if sidecar is None:
            print(f"DROP {year}: {reason}")
            continue
        print(f"MAP  {year}: {len(sidecar['q'])} questions")
        qa_echo(ppath, spath, sidecar)
        ydir = os.path.join(ANSWERS_DIR, str(year))
        os.makedirs(ydir, exist_ok=True)
        with open(os.path.join(ydir, f"{FILEID}.json"), "w", encoding="utf-8") as fh:
            json.dump(sidecar, fh, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"))
        wrote += 1
    print(f"done: {wrote} sidecars")
    return 0


if __name__ == "__main__":
    sys.exit(main())
