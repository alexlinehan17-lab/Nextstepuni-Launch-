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
Paper Trail — short-answer ANSWERBOOK components: Geography Part One (LC005
LP042) and Business Section 1 (LC033 LP032).

Why bespoke: both are the split-format answerbook the earlier waves skipped on
purpose. geo_pre2020.py records the reason — "its scheme collapses onto a 1-2
page key … NOT mapped" — because the generic engine wants one scheme BLOCK per
question and these schemes answer a dozen questions inside one page. That is a
region-shape problem, not a content problem: the sidecar's rect is fractional
in x as well as y, so a key laid out in columns or table rows crops exactly as
well as a full page. Every question on these components has a real, stated
answer printed against it, and students were seeing none of them.

Three scheme grammars, one paper grammar:

  * geography HL — a two-COLUMN key. Q1-Q6 run down the left of the page and
    Q7-Q12 down the right at the SAME y positions, so reading order interleaves
    them (Q1, Q7, Q2, Q8 …). Chips are cut per column: the x split is the
    midpoint between the two column origins, and a question ends at the next
    marker IN ITS OWN COLUMN, never at the next one in reading order.
  * geography OL — the same key set single-column, which needs no x bound.
    Handled by the same code: one detected column is the degenerate case.
  * business HL — a "Question | Possible Responses | Marks" table. The header
    row repeats above every question, so a question's block runs from its own
    header row to the next one. Anchoring on the number alone would start the
    crop below the ask it answers.
  * business OL — no table. An "EXPECTED RESPONSES" section lists "N." headings
    with the answers under them. The scheme's own text layer is glyph-mangled
    ("SecƟon 1"), so the section is found by the ASCII-safe half of the phrase.

The earlier mark-allocation grid both Business schemes print first ("QUESTION |
MARKING SCHEME | TOTAL MARKS", "Three factors: 4m + 3m + 3m") is deliberately
NOT the chip target: it prices the answer without stating it, and a student who
taps through to it learns nothing they did not already know from the paper.

Safety: COUNT RECONCILE — every question the paper prints must land exactly one
monotonic scheme region or the whole paper is DROPPED, never partially written.
Coordinates only, sidecar schema v1.

Usage:
  python3 short_answer_books.py                 # map every corpus year
  python3 short_answer_books.py --subject geography
  python3 short_answer_books.py --dry-run       # report, write nothing
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

YEARS = range(2010, 2027)
COPYRIGHT = "© State Examinations Commission"

# subject -> (paper stem, scheme stem, scheme reader, expected question count)
TARGETS = {
    "geography": {"code": "LC005", "paper": "LP042", "scheme": "LP000",
                  "reader": "geo", "qmin": 10, "qmax": 14},
    "business": {"code": "LC033", "paper": "LP032", "scheme": "LP000",
                 "reader": "bus", "qmin": 8, "qmax": 20},
}

# A question head on the paper: "7." at the left margin. The answerbook rules
# its answer space with nothing that looks like this, so no run guard beyond
# ascending-from-one is needed.
P_HEAD = re.compile(r"^(\d{1,2})\.(?:\s|$)")
# "Q.1", "Q 1", "Q1" on the scheme's key — and "C.1" for Ceist, which is what
# the Irish-language (IV) translation of the same scheme prints.
S_QMARK = re.compile(r"^[QC]\.?\s*(\d{1,2})\b")
# The short-answer section's own heading, in either language.
GEO_PART_ONE = re.compile(r"PART\s+ONE|CUID\s+A\s+HAON", re.I)
GEO_PART_TWO = re.compile(r"PART\s+TWO|CUID\s+A\s+D[ÓO]", re.I)
# The Business table's repeating header row, in either language.
BUS_HDR = re.compile(r"^(?:Question|Ceist)\b")
# Section 1's support-notes block and the Section 2 boundary that ends it. The
# Irish scheme prints ROINN / Nótaí Tacaíochta for the same things, and both
# schemes' text layers mangle "ti" ("SecƟon"), so the middle of each word is
# matched loosely rather than spelled out.
# The trailing (?!\d) rather than \b is deliberate: the Irish scheme welds the
# heading to the next word ("Roinn 1Ceisteanna GearrĬreagra"), and \b never
# fires between a digit and a letter.
BUS_SEC1 = re.compile(r"(?:SEC.{0,2}ON|ROINN)\s*1(?!\d)")
BUS_SEC2 = re.compile(r"(?:SEC.{0,2}ON|ROINN)\s*2(?!\d)")
BUS_NOTES = re.compile(r"SUPPORT\s+NOTES|N[ÓO]TA[ÍI]\s+TACA[ÍI]OCHTA|"
                       r"EXPECTED\s+RESPONSES|FREAGRA[ÍI]\s+A\s+MBEIF[ÍI]")
# Bare "4." / "11 (a)" / "14" heads in the Business OL expected-responses list.
# The trailing group must allow END OF LINE: 2025 OL sets its Q14 head as a
# lone "14" in its own cell, and requiring a following character lost it — and
# with it, silently, the whole paper.
BUS_OL_HEAD = re.compile(r"^(\d{1,2})(?:[.\s]|$)")


def lines_with_pos(page):
    """[(text, x0_frac, y0_frac)] in reading order, one entry per rendered line."""
    W, H = page.rect.width, page.rect.height
    rows = {}
    for w in page.get_text("words"):
        rows.setdefault((w[5], w[6]), []).append(w)
    out = []
    for key in rows:
        ws = sorted(rows[key], key=lambda w: w[0])
        out.append((" ".join(w[4] for w in ws).strip(),
                    ws[0][0] / W, min(w[1] for w in ws) / H))
    out.sort(key=lambda t: (t[2], t[1]))
    return out


# ------------------------------------------------------------------ paper ---

def _run_from(cands, xmax):
    """The ascending 1..N run among candidates left of xmax."""
    found, want = {}, 1
    for n, x, pg, y in cands:
        if x <= xmax and n == want:
            found[n] = (pg, y)
            want += 1
    return found


def paper_questions(doc):
    """{n: (page1, y_frac)} for the ascending 1..N run at the left margin.

    The margin is FOUND, not assumed. Business 2026 sets its heads at x=0.125
    and numbers each answer space "1." "2." underneath at x=0.141, so a fixed
    threshold either loses the question heads or swallows the answer-space
    numbering as questions. Trying every candidate margin and keeping the one
    that yields the longest run picks the heads' own column on both layouts.
    """
    cands = []
    for pi in range(len(doc)):
        for txt, x, y in lines_with_pos(doc[pi]):
            m = P_HEAD.match(txt)
            if m and x <= 0.22:
                cands.append((int(m.group(1)), x, pi + 1, y))
    if not cands:
        return {}
    # Thresholds are the candidates' own x values, UNROUNDED: rounding one down
    # (0.0952 -> 0.095) excludes the very head that produced it, which silently
    # emptied every Geography run.
    best = {}
    for xmax in sorted({x for _, x, _, _ in cands}):
        run = _run_from(cands, xmax)
        if len(run) > len(best):
            best = run
    return best


# ----------------------------------------------------------------- scheme ---

def _columns(marks):
    """Split [(n, x, y)] into columns by x, returning the x boundaries.

    Two origins 0.105 and 0.510 are two columns; a single origin is one. The
    boundary is the midpoint, so a crop never bleeds into its neighbour.
    """
    xs = sorted({round(x, 2) for _, x, _ in marks})
    cols = [[xs[0]]]
    for x in xs[1:]:
        (cols[-1] if x - cols[-1][-1] < 0.12 else cols.append([x]) or cols[-1]).append(x)
    centres = [sum(c) / len(c) for c in cols]
    bounds = []
    for i, c in enumerate(centres):
        # A column starts just left of its own marker and ends just left of the
        # NEXT column's — not at the midpoint between them. The midpoint sits
        # inside the previous column's marks column, so Q7's crop opened with a
        # stack of Q1's "2m" values hanging off its left edge.
        lo = max(0.0, c - 0.03)
        hi = 1.0 if i == len(centres) - 1 else max(lo, centres[i + 1] - 0.03)
        bounds.append((lo, min(1.0, hi)))
    return centres, bounds


def _page_markers(page):
    """[(n, x, y)] for the Q./C. markers on one key page, first hit per number."""
    marks, seen = [], set()
    for txt, x, y in lines_with_pos(page):
        m = S_QMARK.match(txt)
        if m and x < 0.75:
            n = int(m.group(1))
            # A repeated marker is a continuation line, not a new question.
            if n not in seen:
                seen.add(n)
                marks.append((n, x, y))
    return marks


def geo_key(doc):
    """Geography Part One: {n: {'r': [...], 'k': (page, col, y)}}.

    The key can run over two pages (2021 OL sets Q1-Q6 on one and Q7-Q12 on the
    next), and each page is columned independently, so columns are computed per
    page rather than once for the section.
    """
    start = None
    for pi in range(len(doc)):
        if GEO_PART_ONE.search(doc[pi].get_text()) and len(_page_markers(doc[pi])) >= 3:
            start = pi
            break
    if start is None:
        return {}

    out = {}
    for pi in range(start, min(start + 4, len(doc))):
        if pi > start and GEO_PART_TWO.search(doc[pi].get_text()):
            break
        marks = _page_markers(doc[pi])
        if not marks:
            if pi > start:
                break
            continue
        centres, bounds = _columns(marks)

        def col_of(x, centres=centres):
            return min(range(len(centres)), key=lambda i: abs(centres[i] - x))

        for n, x, y in marks:
            if n in out:
                continue
            ci = col_of(x)
            x0, x1 = bounds[ci]
            later = [yy for _, xx, yy in marks
                     if col_of(xx) == ci and yy > y + 0.005]
            y1 = min(later) if later else 0.96
            out[n] = {"r": [(pi + 1, x0, max(0.0, y - 0.012), x1, y1)],
                      "k": (pi + 1, ci, y)}
    return out


def _section_one_span(doc):
    """(first, last) page indices of the Section 1 support-notes block.

    Bounded on purpose: the same table is printed again for Section 2, whose
    questions restart at 1, so an unbounded scan would answer a Section 1
    question with a Section 2 block.
    """
    first = None
    for pi in range(len(doc)):
        upper = doc[pi].get_text().upper()
        if first is None:
            if BUS_SEC1.search(upper) and BUS_NOTES.search(upper):
                first = pi
            continue
        if BUS_SEC2.search(upper):
            return first, pi - 1
    return (first, len(doc) - 1) if first is not None else (None, None)


def bus_hl_table(doc):
    """Business HL: the Question / Possible Responses table, Section 1 only.

    Driven by the NUMBER cell rather than the header row. Most years repeat the
    "Question | Possible Responses | Marks" header above every question, but the
    2022 and 2023 Irish schemes print it once per PAGE with several questions
    under it — anchoring on the header lost every question after the first on
    those pages. The header is still used where it sits directly above a
    number, so the crop opens on the ask rather than under it.
    """
    first, last = _section_one_span(doc)
    if first is None:
        return {}
    regions = {}
    for pi in range(first, last + 1):
        lines = lines_with_pos(doc[pi])
        heads = sorted(y for txt, x, y in lines if BUS_HDR.match(txt) and x < 0.2)
        # A number cell can carry its first part with it ("11 (a)"), so it is
        # matched on its leading integer rather than as a bare number.
        nums = []
        for txt, x, y in lines:
            m = re.match(r"^(\d{1,2})\b", txt)
            if m and x < 0.17:
                nums.append((int(m.group(1)), y))
        nums.sort(key=lambda t: t[1])
        starts = []
        for n, y in nums:
            # A header belongs to the FIRST number under it only. Letting two
            # numbers share one header gave them the same start, and the zero
            # -height block that produced was silently dropped.
            above = [h for h in heads if y - 0.075 < h <= y
                     and not any(h < other < y for _, other in nums)]
            starts.append((n, min(above) if above else max(0.0, y - 0.012)))
        for i, (n, y0) in enumerate(starts):
            y1 = starts[i + 1][1] if i + 1 < len(starts) else 0.94
            if n in regions or y1 <= y0:
                continue
            regions[n] = {"r": [(pi + 1, 0.0, y0, 1.0, y1)],
                          "k": (pi + 1, 0, y0)}
    return regions


def bus_ol_expected(doc):
    """Business OL: {n: [...]} from the EXPECTED RESPONSES list."""
    start, _ = _section_one_span(doc)
    if start is None:
        return {}
    _, last = _section_one_span(doc)
    marks = []
    for pi in range(start, last + 1):
        for txt, x, y in lines_with_pos(doc[pi]):
            m = BUS_OL_HEAD.match(txt)
            if m and x < 0.20:
                n = int(m.group(1))
                if n not in [k for k, _, _ in marks]:
                    marks.append((n, pi + 1, y))
    regions = {}
    for i, (n, pg, y) in enumerate(marks):
        segs = []
        if i + 1 < len(marks) and marks[i + 1][1] == pg:
            segs.append((pg, 0.0, max(0.0, y - 0.012), 1.0, marks[i + 1][2]))
        else:
            segs.append((pg, 0.0, max(0.0, y - 0.012), 1.0, 0.94))
            if i + 1 < len(marks) and marks[i + 1][1] == pg + 1:
                segs.append((pg + 1, 0.0, 0.0, 1.0, marks[i + 1][2]))
        regions[n] = {"r": segs, "k": (pg, 0, y)}
    return regions


def scheme_regions(reader, level, doc):
    if reader == "geo":
        return geo_key(doc)
    return bus_hl_table(doc) if level == "A" else bus_ol_expected(doc)


# ------------------------------------------------------------------ build ---

def build_sidecar(paper_path, scheme_path, reader, level, spec):
    paper, scheme = fitz.open(paper_path), fitz.open(scheme_path)
    pq = paper_questions(paper)
    if not pq:
        return None, "no question run on the paper"
    if not (spec["qmin"] <= len(pq) <= spec["qmax"]):
        return None, f"paper run is {len(pq)} questions, outside {spec['qmin']}-{spec['qmax']}"
    sr = scheme_regions(reader, level, scheme)
    if not sr:
        return None, "no key found in the scheme"

    missing = [n for n in pq if n not in sr]
    if missing:
        return None, f"scheme has no block for question(s) {missing}"

    # The paper run is found, not counted, so it can END EARLY without saying
    # so — Business 2025 OL IV prints no text-layer head for its Q10 and the
    # run stopped at 9, which would have shipped a two-thirds map that looked
    # complete. A scheme block for a question past the run's end is proof the
    # paper reader stopped short.
    beyond = [n for n in sr if n > max(pq)]
    if beyond:
        return None, (f"paper run ends at {max(pq)} but the scheme answers "
                      f"{sorted(beyond)} — the paper reader stopped short")

    # Monotonic: the key must run in the paper's order WITHIN its own layout —
    # a two-column key restarts at the top of the page for its second column,
    # so the order key carries the column, not just the y.
    order = [sr[n]["k"] for n in sorted(pq)]
    if order != sorted(order):
        return None, "scheme blocks are not monotonic against the paper's order"

    q = []
    ordered = sorted(pq)
    for i, n in enumerate(ordered):
        pg, y = pq[n]
        y_end = 1.0
        if i + 1 < len(ordered) and pq[ordered[i + 1]][0] == pg:
            y_end = pq[ordered[i + 1]][1]
        q.append({
            "n": str(n), "conf": 1.0, "mode": "crop",
            "pP": pg, "pY": [round(y, 4), round(y_end, 4)],
            "region": [{"p": p, "r": [round(x0, 4), round(ry0, 4),
                                      round(x1, 4), round(ry1, 4)]}
                       for (p, x0, ry0, x1, ry1) in sr[n]["r"]],
        })
    return {
        "v": 1,
        "paperFileid": os.path.basename(paper_path),
        "schemeFileid": os.path.basename(scheme_path),
        "component": "",
        "band": [1, len(scheme) + 1],  # bounds SCHEME pages, upper exclusive
        "copyright": COPYRIGHT,
        "q": q,
    }, None


def qa_echo(paper_path, scheme_path, sidecar, limit=3):
    """Print paper ask vs scheme crop for the first few chips — the eyeball gate."""
    paper, scheme = fitz.open(paper_path), fitz.open(scheme_path)
    for chip in sidecar["q"][:limit]:
        pg = paper[chip["pP"] - 1]
        W, H = pg.rect.width, pg.rect.height
        ask = pg.get_text(clip=fitz.Rect(0, chip["pY"][0] * H, W,
                                         min(chip["pY"][0] + 0.09, 1.0) * H))
        seg = chip["region"][0]
        sg = scheme[seg["p"] - 1]
        SW, SH = sg.rect.width, sg.rect.height
        x0, y0, x1, y1 = seg["r"]
        crop = sg.get_text(clip=fitz.Rect(x0 * SW, y0 * SH, x1 * SW,
                                          min(y0 + 0.10, y1) * SH))
        print(f"      Q{chip['n']:<3} ask : {' '.join(ask.split())[:64]!r}")
        print(f"      {'':<4} crop: {' '.join(crop.split())[:64]!r}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--subject", choices=sorted(TARGETS))
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    wrote = dropped = 0
    for subject, spec in sorted(TARGETS.items()):
        if args.subject and subject != args.subject:
            continue
        for year in YEARS:
            for level in ("A", "G"):
                for lang in ("EV", "IV"):
                    pf = f"{spec['code']}{level}{spec['paper']}{lang}.pdf"
                    sf = f"{spec['code']}{level}{spec['scheme']}{lang}.pdf"
                    ppath = os.path.join(CORPUS, "exampapers", str(year), pf)
                    spath = os.path.join(CORPUS, "markingschemes", str(year), sf)
                    if not (os.path.exists(ppath) and os.path.exists(spath)):
                        continue
                    out = os.path.join(ANSWERS_DIR, str(year), f"{pf}.json")
                    if os.path.exists(out):
                        continue
                    sidecar, why = build_sidecar(ppath, spath, spec["reader"],
                                                 level, spec)
                    tag = f"{subject} {year} {'HL' if level == 'A' else 'OL'} {lang}"
                    if sidecar is None:
                        print(f"DROP {tag}: {why}")
                        dropped += 1
                        continue
                    print(f"MAP  {tag}: {len(sidecar['q'])} questions")
                    qa_echo(ppath, spath, sidecar)
                    if args.dry_run:
                        continue
                    os.makedirs(os.path.dirname(out), exist_ok=True)
                    with open(out, "w", encoding="utf-8") as fh:
                        json.dump(sidecar, fh, ensure_ascii=False, sort_keys=True,
                                  separators=(",", ":"))
                    wrote += 1
    print(f"done: {wrote} sidecars written, {dropped} dropped")
    return 0


if __name__ == "__main__":
    sys.exit(main())
