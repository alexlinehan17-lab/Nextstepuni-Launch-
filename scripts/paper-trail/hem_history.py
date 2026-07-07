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
Paper Trail — History (Early Modern) LC096: BANDED DBQ maps.

Why bespoke: LC096 shares its marking-scheme FILE with mainstream History
(LC004) — the SEC publishes ONE combined History scheme per level/year whose
first half is the Later Modern field of study and whose second half is Early
Modern (verified byte-identical uploads under both fileids for 2021/2022).
The old COVERAGE.md note "wrong scheme-file pairing in corpus" is stale: the
pairing is correct, but the generic engine cannot use it —

  * its first-hit scheme markers land in the LATER MODERN half (wrong field
    of study — the worst possible failure), and
  * the paper's only globally-numbered questions (DBQ Q1–4) sit on a single
    page, which today's chip-on-cover spread guard rejects (mainstream
    History shipped in wave 3, before that guard, with exactly this shape).

This generator therefore pins the scheme band to the EARLY MODERN half
(divider cover page "Early Modern"/"EARLY MODERN"), maps the four
Section 1 DBQ questions — the same four-question coverage the shipped
LC004 (HL) sidecars have — and bounds Q4 at the "Section 2 and Section 3"
criteria page. Level scope is HIGHER EV only, mirroring shipped mainstream
History (no LC004G sidecar exists: the OL scheme repeats a compact 1.–4.
"four parts" instruction list right before the real DBQ answers, so
first-marker banding is ambiguous — OL drops rather than risk cropping the
instruction list).

Safety posture identical to anchor-map.py / wave10_sections.py: COUNT
RECONCILE — all four DBQ questions must land a monotonic in-band region or
the paper drops. Coordinates only, sidecar schema v1.

Usage: python3 hem_history.py            # maps corpus years, writes answers/<year>/
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
LEAD_X = 95          # a DBQ answer marker "N." starts left of this (points)
YEARS = range(2010, 2026)
FILEIDS = ["LC096ALP000EV.pdf"]   # HIGHER EV only — see module docstring

DBQ_RE = re.compile(r"SECTION\s+1\s*:\s*DOCUMENTS-BASED\s+QUESTION", re.I)
SEC23_RE = re.compile(r"Section\s+2\s+and\s+Section\s+3\s*:", re.I)
LEAD_RE = re.compile(r"^([1-4])\.(\s|$)")


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


def paper_dbq_headers(doc):
    """{n: (page0, yFrac)} for DBQ Q1–4 on the Section 1 page, else None."""
    for pi in range(len(doc)):
        txt = doc[pi].get_text()
        if not DBQ_RE.search(txt):
            continue
        found = {}
        for t, x, y in lines_with_pos(doc[pi]):
            m = LEAD_RE.match(t)
            if m and x < LEAD_X:
                n = int(m.group(1))
                if n not in found:
                    found[n] = (pi, y)
        if sorted(found) == [1, 2, 3, 4]:
            ys = [found[n][1] for n in (1, 2, 3, 4)]
            if all(ys[i] < ys[i + 1] for i in range(3)):
                return found
        return None  # DBQ page found but markers unclean — drop, don't hunt on
    return None


def em_band_start(scheme):
    """0-based page of the 'Early Modern' divider cover, else None."""
    for pi in range(len(scheme)):
        ls = lines_with_pos(scheme[pi])
        for t, x, y in ls:
            if re.fullmatch(r"early\s+modern", t.strip(), re.I) and len(ls) <= 6:
                return pi
    return None


def scheme_dbq_markers(scheme, band_start):
    """{n: (page0, yFrac)} first in-band 'N.' lead markers at/after the band's
    DBQ header; plus the 0-based page of the Section 2/3 boundary. None on any
    ambiguity."""
    dbq_pi = None
    for pi in range(band_start, len(scheme)):
        if DBQ_RE.search(scheme[pi].get_text()):
            dbq_pi = pi
            break
    if dbq_pi is None:
        return None, None
    sec23_pi = None
    found = {}
    for pi in range(dbq_pi, len(scheme)):
        txt = scheme[pi].get_text()
        if SEC23_RE.search(txt):
            sec23_pi = pi
            break
        for t, x, y in lines_with_pos(scheme[pi]):
            m = LEAD_RE.match(t)
            if m and x < LEAD_X:
                n = int(m.group(1))
                if n not in found:
                    found[n] = (pi, y)
    if sorted(found) != [1, 2, 3, 4] or sec23_pi is None:
        return None, None
    pts = [found[n] for n in (1, 2, 3, 4)]
    if not all(pts[i] < pts[i + 1] for i in range(3)):
        return None, None
    return found, sec23_pi


def is_blank(page):
    return not page.get_text().strip()


def build_sidecar(paper_path, scheme_path):
    paper = fitz.open(paper_path)
    scheme = fitz.open(scheme_path)

    headers = paper_dbq_headers(paper)
    if headers is None:
        return None, "no clean DBQ Q1-4 on the paper's Section 1 page"
    band_start = em_band_start(scheme)
    if band_start is None:
        return None, "no 'Early Modern' divider page in scheme"
    markers, sec23_pi = scheme_dbq_markers(scheme, band_start)
    if markers is None:
        return None, "Early Modern band DBQ markers do not reconcile 1-4"

    # paper y-bands (all four headers share the Section 1 page)
    p_pi = headers[1][0]
    ys = [headers[n][1] for n in (1, 2, 3, 4)] + [1.0]

    qout = []
    for i, n in enumerate((1, 2, 3, 4)):
        s_pi, s_y = markers[n]
        if n < 4:
            e_pi, e_y = markers[n + 1]
        else:
            e_pi, e_y = sec23_pi, 0.0   # Q4 runs to the Section 2/3 criteria page
        region = []
        if e_pi == s_pi:
            region.append({"p": s_pi + 1, "r": [0.0, round(s_y, 4), 1.0, round(e_y, 4)]})
        else:
            region.append({"p": s_pi + 1, "r": [0.0, round(s_y, 4), 1.0, 1.0]})
            for mid in range(s_pi + 1, e_pi):
                if not is_blank(scheme[mid]):
                    region.append({"p": mid + 1, "r": [0.0, 0.0, 1.0, 1.0]})
            if e_y > 0.0 and not is_blank(scheme[e_pi]):
                region.append({"p": e_pi + 1, "r": [0.0, 0.0, 1.0, round(e_y, 4)]})
        qout.append({"n": str(n), "pP": p_pi + 1,
                     "pY": [round(ys[i], 4), round(ys[i + 1], 4)],
                     "region": region, "mode": "crop", "conf": 1.0})

    return {
        "v": SIDECAR_V,
        "paperFileid": os.path.basename(paper_path),
        "schemeFileid": os.path.basename(scheme_path),
        "component": "",
        "band": [band_start + 1, len(scheme) + 1],
        "copyright": COPYRIGHT,
        "q": qout,
    }, None


def main():
    wrote = 0
    for year in YEARS:
        for fid in FILEIDS:
            ppath = os.path.join(CORPUS, "exampapers", str(year), fid)
            spath = os.path.join(CORPUS, "markingschemes", str(year), fid)
            if not (os.path.exists(ppath) and os.path.exists(spath)):
                continue
            sidecar, reason = build_sidecar(ppath, spath)
            if sidecar is None:
                print(f"DROP {year} {fid}: {reason}")
                continue
            # QA echo: first line of every crop for eyeball + verify_all
            scheme = fitz.open(spath)
            for q in sidecar["q"]:
                seg = q["region"][0]
                pg = scheme[seg["p"] - 1]
                W, H = pg.rect.width, pg.rect.height
                x0, y0, x1, y1 = seg["r"]
                t = pg.get_text("text", clip=fitz.Rect(x0 * W, y0 * H, x1 * W, y1 * H))
                first = next((l.strip() for l in t.splitlines() if l.strip()), "")
                print(f"  {year} Q{q['n']} p{seg['p']} starts: {first[:70]!r}")
            ydir = os.path.join(ANSWERS_DIR, str(year))
            os.makedirs(ydir, exist_ok=True)
            out = os.path.join(ydir, f"{fid}.json")
            with open(out, "w", encoding="utf-8") as fh:
                json.dump(sidecar, fh, ensure_ascii=False, sort_keys=True,
                          separators=(",", ":"))
            print(f"WROTE {out}")
            wrote += 1
    print(f"done: {wrote} sidecars")
    return 0


if __name__ == "__main__":
    sys.exit(main())
