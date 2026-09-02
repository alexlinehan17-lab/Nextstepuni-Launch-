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
Paper Trail — Accounting (LC032), full-estate rebuild, 2010-2026.

The engine-era maps anchored workings decoys (2019 HL EV chips Q1 to a
one-line strip inside Q6's pages), so every sitting is rebuilt from the
question-head grammar rather than patched. Scheme headings come in four
families, often mixed inside one document:

  * "Question N" spelled out (incl. the ti-ligature "QuesƟon"),
  * "Q N" / "Q.N" / "QN", and Irish "Ceist N" / "C.N",
  * a broken-subset-font family where the extracted text is glyph-shifted:
    "Question" comes out as chr(0x59,0x1B5,0x11E,0x190,0x19A,0x15D,0x17D,
    0x176), "Ceist" loses its capital and comes out as "ĞŝƐƚ", and digit d
    comes out as chr(0x3BC+ord(d)) — the map is verified inside each
    document by its own printed page numbers,
  * lone "N." margin cells beside a title row (the older Ordinary schemes).

The first three are primary; the cell family is primary only when the
others find nothing, and otherwise fills gaps slot-bounded between two
confirmed neighbours (2023 HL heads Q5 as bare "5 Interpretation...").
Pages carrying 3+ candidates are treated as allocation grids and ignored.

Paper heads are "N." at the left margin; numbered instruction lists print
deeper into the page, so candidates are clustered on the minimum x and the
run must complete 1..K exactly, K taken from the scheme.

Q1 has no heading of its own in some schemes (2021 HL opens the solution
under the document title; the first "Question 1" line is the (B) workings
page) — when the apparent Q1 span is implausibly thin and deep, the region
is rebased to the first content page.

Usage: python3 accounting_era.py [--dry-run] [--only 2021AEV]
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

CQ = "".join(chr(c) for c in (0x59, 0x1B5, 0x11E, 0x190, 0x19A, 0x15D, 0x17D, 0x176))
CC = "".join(chr(c) for c in (0x11E, 0x15D, 0x190, 0x19A))
CORR_D = {chr(0x3BC + ord(d)): int(d) for d in "123456789"}

RX_WORD = re.compile(r"^(?:Ques.{0,2}on|Ceist)\s*\.?\s*\(?\s*(\d{1,2})", re.I)
RX_Q = re.compile(r"^[QC]\s?\.?\s?(\d{1,2})(?![0-9])")
RX_CELL = re.compile(r"^(\d{1,2})\s*[.\u0358]\s*$")
RX_CELL_P = re.compile(r"^(\d{1,2})\s*[.\u0358]?\s*\(\s*[A-Za-z]?\s*\)")
RX_CELL_T = re.compile(r"^(\d{1,2})[.\u0358\s]\s*[A-ZÁÉÍÓÚ]")
P_HEAD = re.compile(r"^(\d{1,2})\.(?:\s+\S|$)")


def lines_pos(page):
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


CORR_PUNCT = {";": "(", "\u037f": ")", "\u0380": "[", "\u0381": "]", "\u0358": "."}


def normalize(txt):
    """Repair a glyph-shifted row just enough for the head regexes."""
    if CQ not in txt and CC not in txt and not any(c in CORR_D for c in txt):
        return txt
    txt = txt.replace(CQ, "Question").replace(CC, "Ceist")
    txt = "".join(str(CORR_D.get(c, CORR_PUNCT.get(c, c))) for c in txt)
    if re.match(r"^Y\s?\d", txt):
        txt = "Q" + txt[1:]
    return txt


def scheme_heads(doc):
    primary, cells, bare = [], [], []
    for pi in range(1, len(doc)):
        rows = lines_pos(doc[pi])
        for txt, x, y in rows:
            if len(txt) > 90 or not txt:
                continue
            txt = normalize(txt)
            m = RX_WORD.match(txt) or (RX_Q.match(txt) if x < 0.35 else None)
            if m and 1 <= int(m.group(1)) <= 12 and (x < 0.35 or len(txt) < 40):
                primary.append((int(m.group(1)), pi + 1, y))
                continue
            m = RX_CELL.match(txt) or RX_CELL_P.match(txt) or RX_CELL_T.match(txt)
            if m and x < 0.3 and 1 <= int(m.group(1)) <= 12:
                cells.append((int(m.group(1)), pi + 1, y))
                continue
            # dotless lone digit counts only with a titlecase neighbour cell
            if re.match(r"^(\d{1,2})$", txt) and x < 0.3 and 1 <= int(txt) <= 12:
                if any(abs(oy - y) < 0.012 and x < ox < 0.5 and ot[:1].isupper()
                       for ot, ox, oy in rows if ot != txt):
                    bare.append((int(txt), pi + 1, y))

    def degrid(cands):
        from collections import Counter
        per_page = Counter(c[1] for c in cands)
        return [c for c in cands if per_page[c[1]] < 3]

    primary, cells = degrid(primary), degrid(cells)
    pool = primary if len({c[0] for c in primary}) >= 5 else cells
    have = {}
    for n, pg, y in sorted(pool, key=lambda c: (c[1], c[2])):
        if n not in have:
            have[n] = (pg, y)
    ns = sorted(have)
    order = [have[n] for n in ns]
    if order != sorted(order):
        keep, last = {}, (0, -1.0)
        for n in ns:
            if have[n] > last:
                keep[n], last = have[n], have[n]
        have = keep
    for n in range(1, 10):
        if n in have:
            continue
        lo = have.get(n - 1, (1, 0.0))
        hi = min((have[m] for m in have if m > n), default=(len(doc) + 1, 0.0))
        for pool2 in (cells, bare):
            for cn, pg, y in sorted(pool2, key=lambda c: (c[1], c[2])):
                if cn == n and lo < (pg, y) < hi:
                    have[n] = (pg, y)
                    break
            if n in have:
                break
        if n not in have and n - 1 in have and n + 1 in have:
            gap = range(have[n - 1][0] + 1, have[n + 1][0])
            if len(gap) == 1:
                have[n] = (gap[0], 0.0)
    K = 0
    while K + 1 in have:
        K += 1
    return {n: have[n] for n in have if n <= K}, K


def paper_run(doc, K):
    cands = []
    for pi in range(1, len(doc)):
        for txt, x, y in lines_pos(doc[pi]):
            m = P_HEAD.match(txt)
            if m and x < 0.16 and y > 0.02 and int(m.group(1)) <= 12:
                cands.append((int(m.group(1)), pi + 1, y, x))
    if not cands:
        return {}
    xf = min(c[3] for c in cands)
    tight = [c for c in cands if c[3] <= xf + 0.028]
    have, last = {}, (0, -1.0)
    for n, pg, y, x in sorted(tight, key=lambda c: (c[1], c[2])):
        if n == len(have) + 1 and (pg, y) > last:
            have[n], last = (pg, y), (pg, y)
    for n in range(1, K + 1):
        if n in have:
            continue
        lo = have.get(n - 1, (1, 0.0))
        hi = min((have[m] for m in have if m > n), default=(len(doc) + 1, 0.0))
        for txt, pg, y, x in (
            (t, pi + 1, yy, xx)
            for pi in range(1, len(doc))
            for t, xx, yy in lines_pos(doc[pi])
        ):
            m = re.match(r"^(\d{1,2})[.\s]?$", txt) or P_HEAD.match(txt)
            if m and x < 0.22 and y > 0.02 and int(m.group(1)) == n and lo < (pg, y) < hi:
                have[n] = (pg, y)
                break
    return have


def build(ppath, spath):
    paper, scheme = fitz.open(ppath), fitz.open(spath)
    sh, K = scheme_heads(scheme)
    if K not in (8, 9):
        return None, f"scheme head count K={K} (heads {sorted(sh)})"
    ph = paper_run(paper, K)
    M = 0
    while M + 1 in ph:
        M += 1
    if M != K:
        return None, f"paper run 1..{M} disagrees with scheme 1..{K}"
    ph = {n: ph[n] for n in ph if n <= M}
    if [ph[n] for n in sorted(ph)] != sorted(ph.values()):
        return None, "paper heads not monotonic"

    # Q1 rebase: apparent span < 2 pages while Q2 sits deep => headless (A) part.
    if 2 in sh and sh[2][0] > 4 and sh[2][0] - sh[1][0] < 2:
        sh[1] = (3, 0.0)

    q = []
    for n in range(1, K + 1):
        pg, y = ph[n]
        y_end = 1.0
        if n + 1 in ph and ph[n + 1][0] == pg and ph[n + 1][1] > y:
            y_end = ph[n + 1][1]
        spg, sy = sh[n]
        if n + 1 in sh:
            npg, ny = sh[n + 1]
        else:
            npg, ny = len(scheme), 1.0
        region = []
        if npg == spg:
            region.append({"p": spg, "r": [0.0, round(max(0.0, sy - 0.012), 4),
                                           1.0, round(ny if ny > sy else 1.0, 4)]})
        else:
            region.append({"p": spg, "r": [0.0, round(max(0.0, sy - 0.012), 4), 1.0, 1.0]})
            for mid in range(spg + 1, npg):
                region.append({"p": mid, "r": [0.0, 0.0, 1.0, 1.0]})
            if n + 1 in sh and ny > 0.04:
                region.append({"p": npg, "r": [0.0, 0.0, 1.0, round(ny, 4)]})
            elif n + 1 not in sh:
                region.append({"p": npg, "r": [0.0, 0.0, 1.0, 1.0]})
        q.append({"n": str(n), "conf": 1.0, "mode": "crop",
                  "pP": pg, "pY": [round(y, 4), round(y_end, 4)],
                  "region": region})
    return {
        "v": 1, "paperFileid": os.path.basename(ppath),
        "schemeFileid": os.path.basename(spath), "component": "",
        "band": [1, len(scheme) + 1], "copyright": COPYRIGHT, "q": q,
    }, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--only", default="")
    args = ap.parse_args()
    wrote = dropped = 0
    for year in range(2010, 2027):
        for lv in ("A", "G"):
            for lg in ("EV", "IV"):
                tag = f"{year}{lv}{lg}"
                if args.only and args.only != tag:
                    continue
                fid = f"LC032{lv}LP000{lg}.pdf"
                ppath = os.path.join(CORPUS, "exampapers", str(year), fid)
                spath = os.path.join(CORPUS, "markingschemes", str(year), fid)
                if not (os.path.exists(ppath) and os.path.exists(spath)):
                    continue
                sidecar, why = build(ppath, spath)
                if sidecar is None:
                    print(f"DROP {tag}: {why}")
                    dropped += 1
                    continue
                print(f"MAP  {tag}: {len(sidecar['q'])} chips")
                if not args.dry_run:
                    out = os.path.join(ANSWERS_DIR, str(year), f"{fid}.json")
                    os.makedirs(os.path.dirname(out), exist_ok=True)
                    with open(out, "w", encoding="utf-8") as fh:
                        json.dump(sidecar, fh, ensure_ascii=False, sort_keys=True,
                                  separators=(",", ":"))
                    wrote += 1
    print(f"done: {wrote} written, {dropped} dropped")
    return 0


if __name__ == "__main__":
    sys.exit(main())
