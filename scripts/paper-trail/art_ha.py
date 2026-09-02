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
Paper Trail — Art History & Appreciation, 2010-2013 era (LC014 LP013).

The engine dropped these years as "no clean paper question sequence", but the
sequence is clean — the numbers sit at x≈0.12 as their own cells, and the
generic detector's margin threshold missed them. The shared 000 scheme covers
every Art component; the H&A answers are the table blocks headed by SHORT
"Q N" cells (2-3 to a page), which the craftwork outline's long "Question N --
Title" lines cannot shadow because only the short-cell form is accepted.

Chips: one per printed question (continuous 1..N across the paper's three
sections), region = the question's Q-cell block to the next Q cell. Both
languages share the grammar (the Irish schemes keep the Q cells).

Usage: python3 art_ha.py [--dry-run]
"""
import argparse
import json
import os
import re
import sys

import fitz  # pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
CORPUS = os.path.join(REPO, "paper-trail-corpus")
ANSWERS_DIR = os.path.join(HERE, "answers")
COPYRIGHT = "© State Examinations Commission"

P_HEAD = re.compile(r"^(\d{1,2})\.(?:\s|$)")
S_CELL = re.compile(r"^[QC][.\s]?\s?(\d{1,2})\.?$")


def lines_with_pos(page):
    W, H = page.rect.width, page.rect.height
    rows = {}
    for w in page.get_text("words"):
        rows.setdefault((w[5], w[6]), []).append(w)
    out = []
    for key in rows:
        ws = sorted(rows[key], key=lambda w: w[0])
        out.append((" ".join(w[4] for w in ws).replace("\xa0", " ").strip(),
                    ws[0][0] / W,
                    min(1.0, max(0.0, min(w[1] for w in ws) / H))))
    out.sort(key=lambda t: (t[2], t[1]))
    return out


def paper_run(doc):
    found, want = {}, 1
    for pi in range(1, len(doc)):
        for txt, x, y in lines_with_pos(doc[pi]):
            m = P_HEAD.match(txt)
            if m and x < 0.2 and int(m.group(1)) == want:
                found[want] = (pi + 1, y)
                want += 1
    return found


def scheme_cells(doc):
    cells = []
    for pi in range(len(doc)):
        for txt, x, y in lines_with_pos(doc[pi]):
            m = S_CELL.match(txt)
            if m and x < 0.4:
                cells.append((int(m.group(1)), pi + 1, y))
    return cells


def build(ppath, spath):
    paper, scheme = fitz.open(ppath), fitz.open(spath)
    pq = paper_run(paper)
    if len(pq) < 8:
        return None, f"paper run is {len(pq)} — expected the full H&A set"
    cells = scheme_cells(scheme)
    have = {}
    for n, pg, y in cells:
        if n in pq and n not in have:
            have[n] = (pg, y)
    missing = [n for n in pq if n not in have]
    if missing:
        return None, f"scheme has no Q cells for {missing}"
    order = [have[n] for n in sorted(pq)]
    if order != sorted(order):
        return None, "scheme Q cells not monotonic"
    q = []
    ns = sorted(pq)
    for i, n in enumerate(ns):
        pg, y = pq[n]
        y_end = 1.0
        if i + 1 < len(ns) and pq[ns[i + 1]][0] == pg:
            y_end = pq[ns[i + 1]][1]
        spg, sy = have[n]
        if i + 1 < len(ns):
            npg, ny = have[ns[i + 1]]
        else:
            npg, ny = spg, 1.0
        region = []
        if npg == spg:
            region.append({"p": spg, "r": [0.0, round(max(0.0, sy - 0.012), 4),
                                           1.0, round(ny if ny > sy else 1.0, 4)]})
        else:
            region.append({"p": spg, "r": [0.0, round(max(0.0, sy - 0.012), 4), 1.0, 1.0]})
            for mid in range(spg + 1, npg):
                region.append({"p": mid, "r": [0.0, 0.0, 1.0, 1.0]})
            if i + 1 < len(ns) and ny > 0.04:
                region.append({"p": npg, "r": [0.0, 0.0, 1.0, round(ny, 4)]})
        q.append({"n": str(n), "conf": 1.0, "mode": "crop",
                  "pP": pg, "pY": [round(y, 4), round(y_end, 4)],
                  "region": region})
    return {
        "v": 1, "paperFileid": os.path.basename(ppath),
        "schemeFileid": os.path.basename(spath), "component": "013",
        "band": [1, len(scheme) + 1], "copyright": COPYRIGHT, "q": q,
    }, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    wrote = dropped = 0
    for year in (2010, 2011, 2012, 2013, 2020):
        for lv in ("A", "G"):
            for lg in ("EV", "IV"):
                pf = f"LC014{lv}LP013{lg}.pdf"
                sf = f"LC014{lv}LP000{lg}.pdf"
                ppath = os.path.join(CORPUS, "exampapers", str(year), pf)
                spath = os.path.join(CORPUS, "markingschemes", str(year), sf)
                if not (os.path.exists(ppath) and os.path.exists(spath)):
                    continue
                out = os.path.join(ANSWERS_DIR, str(year), f"{pf}.json")
                if os.path.exists(out):
                    continue
                sidecar, why = build(ppath, spath)
                tag = f"{year} {lv}{lg}"
                if sidecar is None:
                    print(f"DROP {tag}: {why}")
                    dropped += 1
                    continue
                print(f"MAP  {tag}: {len(sidecar['q'])} chips")
                if not args.dry_run:
                    os.makedirs(os.path.dirname(out), exist_ok=True)
                    with open(out, "w", encoding="utf-8") as fh:
                        json.dump(sidecar, fh, ensure_ascii=False, sort_keys=True,
                                  separators=(",", ":"))
                    wrote += 1
    print(f"done: {wrote} written, {dropped} dropped")
    return 0


if __name__ == "__main__":
    sys.exit(main())
