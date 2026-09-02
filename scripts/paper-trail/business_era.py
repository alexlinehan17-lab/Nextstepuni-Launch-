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
Paper Trail — Business booklet era (LC033 LP000, 2010-2019): ground-up REBUILD.

One booklet holds the whole exam: Section 1 short answers, the Section 2 ABQ,
and Section 3's long questions. The schemes print a MARK-ALLOCATION OUTLINE
first — a grid that numbers every question — and only then the detailed
answers, which restate each question. The engine-era maps anchored on the
outline (and on true/false grids inside answers), which is why a student
tapping 2011 OL Q8 got a grid tail: those shipped maps are being REPLACED, not
extended.

Two rules do the work:
  * every run is taken as the LAST full ascending run of its length — outline
    grids come first, detailed answers last;
  * every chip must ECHO: the scheme block must restate enough of the paper's
    own question words, or the paper drops. This is the gate that exposed the
    old maps.

Chips: Section 1 shorts (n=1..N, "Section 1 · Qn"), one ABQ chip, Section 3
longs ("Section 3 · Qn"). IV twins are built directly with the same grammar
(Ceist/ROINN tokens), not aligned — the English maps were the untrustworthy
part.

Usage: python3 business_era.py [--dry-run] [--years 2011,2012]
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

SEC = re.compile(r"^(?:SECTION|Section|ROINN|Roinn)\s*([123])\b")
QHEAD = re.compile(r"^(?:QUESTION|Question|CEIST|Ceist)\s*(\d{1,2})\b")
NHEAD = re.compile(r"^(\d{1,2})\.(?:\s|$)")


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


def harvest(doc):
    """(sections, qmarks, nmarks): positioned markers across the document."""
    sections, qmarks, nmarks = [], [], []
    for pi in range(len(doc)):
        for txt, x, y in lines_with_pos(doc[pi]):
            s = SEC.match(txt)
            if s and x < 0.75:
                sections.append((int(s.group(1)), pi + 1, y))
            q = QHEAD.match(txt)
            if q and x < 0.6:
                qmarks.append((int(q.group(1)), pi + 1, y, txt))
            n = NHEAD.match(txt)
            if n and x < 0.35:
                nmarks.append((int(n.group(1)), pi + 1, y, txt))
    return sections, qmarks, nmarks


def longest_run(marks, lo=1, min_len=4, max_len=20, after=(0, 0.0)):
    """The LONGEST ascending run lo..K (ties -> later), tolerant of decoys.

    An inner numbered list restarts at 1 and would chop a naive chain, so the
    builder keeps EVERY open run alive and lets each marker extend whichever
    run it continues.
    """
    open_runs, best = [], None
    for n, pg, y, txt in marks:
        if (pg, y) <= after:
            continue
        if n == lo:
            open_runs.append([(n, pg, y, txt)])
        else:
            for r in open_runs:
                if r[-1][0] + 1 == n and len(r) < max_len:
                    r.append((n, pg, y, txt))
                    break
        for r in open_runs:
            if len(r) >= min_len and (best is None or len(r) >= len(best)):
                best = list(r)
    return best


def echo_dp(paper, scheme, p_anchors, cands_by_i):
    """Ascending assignment of scheme candidates maximising total echo.

    p_anchors: [(pg, y)] per chip. cands_by_i: [[(pg, y), ...]] per chip.
    Returns [(pg, y)] or None. Decoy blocks (outline grids, inner lists)
    restate nothing, so any assignment through them scores lower than the
    real detailed answers.
    """
    if any(not c for c in cands_by_i):
        return None
    pwords = [words_of(paper, pg, y) for pg, y in p_anchors]
    scores = []
    for i, cands in enumerate(cands_by_i):
        row = []
        for (pg, y) in cands:
            row.append(len(pwords[i] & words_of(scheme, pg, y)))
        scores.append(row)
    NEG = -1e9
    n = len(cands_by_i)
    dp = [[NEG] * len(c) for c in cands_by_i]
    back = [[-1] * len(c) for c in cands_by_i]
    for j in range(len(cands_by_i[0])):
        dp[0][j] = scores[0][j]
    for i in range(1, n):
        for j, (pg, y) in enumerate(cands_by_i[i]):
            for k, (ppg, py) in enumerate(cands_by_i[i - 1]):
                if dp[i - 1][k] == NEG or (pg, y) <= (ppg, py):
                    continue
                v = dp[i - 1][k] + scores[i][j]
                if v > dp[i][j]:
                    dp[i][j] = v
                    back[i][j] = k
    j = max(range(len(cands_by_i[-1])), key=lambda jj: dp[-1][jj])
    if dp[-1][j] == NEG:
        return None
    out = [None] * n
    for i in range(n - 1, -1, -1):
        out[i] = cands_by_i[i][j]
        j = back[i][j]
    return out


def words_of(doc, pg, y0, span=0.14):
    page = doc[pg - 1]
    H = page.rect.height
    t = page.get_text(clip=fitz.Rect(0, y0 * H, page.rect.width,
                                     min(y0 + span, 1.0) * H))
    return set(w.lower() for w in re.findall(r"[A-Za-zÀ-ſ]{5,}", t))


def echo_ok(paper, scheme, p_anchor, s_anchor, need=3):
    return len(words_of(paper, *p_anchor) & words_of(scheme, *s_anchor)) >= need


def build(ppath, spath):
    paper, scheme = fitz.open(ppath), fitz.open(spath)
    psec, pq, pn = harvest(paper)
    ssec, sq, sn = harvest(scheme)

    p_s1 = next(((pg, y) for n, pg, y in psec if n == 1), None)
    p_s2 = next(((pg, y) for n, pg, y in psec if n == 2), None)
    if not (p_s1 and p_s2):
        return None, "paper does not print Sections 1 and 2"
    # OL papers put their long questions in Section 2 (no Section 3); HL in 3.
    has_s3 = any(n == 3 for n, pg, y in psec)
    longs_sec = 3 if has_s3 else 2

    # Section 1 shorts on the paper: N. heads between the section dividers.
    shorts = [(n, pg, y, t) for n, pg, y, t in pn
              if p_s1 <= (pg, y) < p_s2]
    s1run = longest_run(shorts, min_len=5)
    if not s1run:
        return None, "no Section 1 run on the paper"
    # Long questions on the paper: worded heads after the Section 2 divider.
    longs = [(n, pg, y, t) for n, pg, y, t in pq if (pg, y) > p_s2]
    p3run = longest_run(longs, min_len=4, max_len=8)

    # STRUCTURAL FENCES: every scheme prints its mark-allocation outline first
    # and then reprints the section headings to open the detailed answers —
    # so the LAST "SECTION 1" heading floors Section 1's answers and the LAST
    # heading of the long-question section floors the longs. This replaces
    # the per-chip echo hard-gate: 2011/2014/2015 HL answer without restating
    # the questions, and echo alone refused every one of them.
    s1_heads = [(pg, y) for n, pg, y in ssec if n == 1]
    s1_floor = s1_heads[-1] if len(s1_heads) > 1 else (0, 0.0)
    long_heads = [(pg, y) for n, pg, y in ssec if n == longs_sec]
    long_floor = long_heads[-1] if long_heads else (0, 0.0)
    if long_floor <= s1_floor:
        # a lone trailing heading (part 2 of the section) — take the first
        # heading of that section AFTER the Section-1 floor instead
        after = [h for h in long_heads if h > s1_floor]
        long_floor = after[0] if after else long_floor

    # Scheme side by ECHO-DP: candidates per number, the assignment that
    # restates the paper best wins; outline grids and inner lists lose.
    def rescue(n, floor, ceil):
        """Looser marker forms for a number the strict harvest missed: '5 ',
        '5:', 'Q5', a lone digit — inside the (floor, ceil) slot only."""
        out = []
        loose = re.compile(rf"^(?:Q\.?\s*)?{n}(?:[.:)\s]|$)")
        for pi in range(max(0, floor[0] - 1), min(len(scheme), ceil[0] + 1)):
            for txt, x, y in lines_with_pos(scheme[pi]):
                if x < 0.35 and loose.match(txt) and floor < (pi + 1, y) < ceil:
                    out.append((pi + 1, y))
        return out

    long_ceil = long_floor if long_floor > s1_floor else (len(scheme) + 1, 0.0)
    s1_cands = []
    for n, pg, y, t in s1run:
        cs = [(spg, sy) for m, spg, sy, st in sn
              if m == n and (spg, sy) > s1_floor]
        if not cs:
            cs = rescue(n, s1_floor, long_ceil)
        s1_cands.append(cs)
    s1_assign = echo_dp(paper, scheme,
                        [(pg, y) for n, pg, y, t in s1run], s1_cands)
    if s1_assign is None:
        return None, "scheme Section 1 would not reconcile"
    s1detail = [(s1run[i][0], pg, y, "") for i, (pg, y) in enumerate(s1_assign)]
    s3detail = None
    if p3run:
        floor = max(long_floor, (s1detail[-1][1], s1detail[-1][2]))
        s3_cands = []
        for n, pg, y, t in p3run:
            cs = [(spg, sy) for m, spg, sy, st in sq
                  if m == n and (spg, sy) > floor]
            if not cs:
                cs = rescue(n, floor, (len(scheme) + 1, 0.0))
            s3_cands.append(cs)
        s3_assign = echo_dp(paper, scheme,
                            [(pg, y) for n, pg, y, t in p3run], s3_cands)
        if s3_assign is None:
            return None, "scheme Section 3 would not reconcile"
        s3detail = [(p3run[i][0], pg, y, "") for i, (pg, y) in enumerate(s3_assign)]
    # ABQ block: the scheme's LAST Section-2 heading past the Section-1 floor.
    s2s = [(pg, y) for n, pg, y in ssec if n == 2 and (pg, y) > s1_floor]
    s2_block = s2s[-1] if s2s else None

    chips = []
    seq = 0

    def push(label, p_pg, p_y, s_pg, s_y, s_end):
        nonlocal seq
        seq += 1
        region = []
        epg, ey = s_end
        if epg == s_pg:
            region.append({"p": s_pg, "r": [0.0, round(max(0.0, s_y - 0.012), 4),
                                            1.0, round(ey if ey > s_y else 1.0, 4)]})
        else:
            region.append({"p": s_pg, "r": [0.0, round(max(0.0, s_y - 0.012), 4), 1.0, 1.0]})
            for mid in range(s_pg + 1, epg):
                region.append({"p": mid, "r": [0.0, 0.0, 1.0, 1.0]})
            if ey > 0.04:
                region.append({"p": epg, "r": [0.0, 0.0, 1.0, round(ey, 4)]})
        chips.append({"n": str(seq), "conf": 1.0, "mode": "crop",
                      "label": label, "pP": p_pg,
                      "pY": [round(p_y, 4), 1.0], "region": region})

    # Section 1 chips. Echo is advisory once the structural floor held: the
    # aggregate must show SOME restatement (the floor being wrong shows none),
    # but individual answers may legitimately not restate their question.
    hits = 0
    for i, (n, pg, y, txt) in enumerate(s1run):
        spg, sy = s1detail[i][1], s1detail[i][2]
        if i + 1 < len(s1detail):
            send = (s1detail[i + 1][1], s1detail[i + 1][2])
        elif s2_block and s2_block > (spg, sy):
            send = s2_block
        else:
            send = (spg, 1.0)
        if echo_ok(paper, scheme, (pg, y), (spg, sy), need=2):
            hits += 1
        push(f"Section 1 · Q{n}", pg, y, spg, sy, send)
    if hits < max(2, len(s1run) // 4):
        return None, f"only {hits}/{len(s1run)} Section 1 chips echo — floor suspect"

    # ABQ chip — HL only, and only when its block precedes the longs' answers.
    if has_s3 and s2_block and p3run and s2_block < (s3detail[0][1], s3detail[0][2]):
        end = (s3detail[0][1], s3detail[0][2])
        push("Section 2 · ABQ", p_s2[0], p_s2[1], s2_block[0], s2_block[1], end)

    # Long-question chips
    if p3run:
        hits = 0
        for i, (n, pg, y, txt) in enumerate(p3run):
            spg, sy = s3detail[i][1], s3detail[i][2]
            if i + 1 < len(s3detail):
                send = (s3detail[i + 1][1], s3detail[i + 1][2])
            else:
                send = (len(scheme), 1.0)
            if echo_ok(paper, scheme, (pg, y), (spg, sy), need=2):
                hits += 1
            push(f"Section {longs_sec} · Q{n}", pg, y, spg, sy, send)
        if hits < max(2, len(p3run) // 3):
            return None, f"only {hits}/{len(p3run)} long-question chips echo — floor suspect"

    # tighten paper y-ends within pages
    by_page = {}
    for c in chips:
        by_page.setdefault(c["pP"], []).append(c)
    for pg, cs in by_page.items():
        cs.sort(key=lambda c: c["pY"][0])
        for a, b in zip(cs, cs[1:]):
            if b["pY"][0] > a["pY"][0]:
                a["pY"][1] = b["pY"][0]

    return {
        "v": 1, "paperFileid": os.path.basename(ppath),
        "schemeFileid": os.path.basename(spath), "component": "",
        "band": [1, len(scheme) + 1], "copyright": COPYRIGHT,
        "q": sorted(chips, key=lambda c: int(c["n"])),
    }, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--years", default="")
    args = ap.parse_args()
    years = [int(y) for y in args.years.split(",") if y] or range(2010, 2020)
    wrote = dropped = 0
    for year in years:
        for lv in ("A", "G"):
            for lg in ("EV", "IV"):
                pf = f"LC033{lv}LP000{lg}.pdf"
                ppath = os.path.join(CORPUS, "exampapers", str(year), pf)
                spath = os.path.join(CORPUS, "markingschemes", str(year), pf)
                if not (os.path.exists(ppath) and os.path.exists(spath)):
                    continue
                sidecar, why = build(ppath, spath)
                tag = f"{year} {lv}{lg}"
                if sidecar is None:
                    print(f"DROP {tag}: {why}")
                    dropped += 1
                    continue
                print(f"MAP  {tag}: {len(sidecar['q'])} chips")
                if args.dry_run:
                    continue
                out = os.path.join(ANSWERS_DIR, str(year), f"{pf}.json")
                os.makedirs(os.path.dirname(out), exist_ok=True)
                with open(out, "w", encoding="utf-8") as fh:
                    json.dump(sidecar, fh, ensure_ascii=False, sort_keys=True,
                              separators=(",", ":"))
                wrote += 1
    print(f"done: {wrote} written, {dropped} dropped")
    return 0


if __name__ == "__main__":
    sys.exit(main())
