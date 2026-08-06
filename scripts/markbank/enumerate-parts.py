#!/usr/bin/env python3
"""
Mark Bank — enumerate every examinable part, from the marking scheme.

The COVERAGE DENOMINATOR: what a deck is measured against, so that what gets
built is compared to what exists rather than to whatever the authoring agents
happened to return.

    python3 scripts/markbank/enumerate-parts.py examiner-reports/<subject>/schemes/2024-hl.md

Read from the SCHEME, not the paper. That is a deliberate second attempt. The
papers are typeset as answerbooks — question numbers alone on a line, every space
set as U+00A0, section headings listed on a booklet cover before the section they
name, and "Question 1" in words in one section against "1." in another. Three
successive regexes over them each produced a different wrong answer: 6 of 10
papers reading as empty, then "6 marks" counted as question 6. A denominator that
is quietly wrong is worse than none, because it converts a coverage gap into a
false all-clear.

The scheme has none of those problems, and it is the stronger source anyway: a
part that is marked MUST appear in it, or the examiner could not have marked it.
"""

import argparse
import json
import re
import sys
from pathlib import Path

# In the answer region the scheme heads each block plainly.
# "Section A", or "Section A 60 marks" — some years print the tariff on the
# heading line and some do not, and requiring a bare heading left whole papers
# with no section at all.
SECTION = re.compile(r"^\s*Section\s+([A-C1-3])\s*(\d+\s*(or\s*\d+\s*)?marks?)?\s*$", re.I)
SHORT_Q = re.compile(r"^\s*(\d{1,2})\.\s+(\S.*)$")
# Section C writes its questions "4.(a)" — number, dot, part, no space between —
# which matches none of the other shapes, so the whole section went uncounted.
ELECTIVE_Q = re.compile(r"^\s*(\d{1,2})\.\s*\(([a-h])\)\s*(.*)$")
LONG_Q = re.compile(r"^\s*Question\s+(\d{1,2})\s*$", re.I)
PART = re.compile(r"^\s*\(([a-h])\)\s+(\S.*)$")
SUBPART = re.compile(r"^\s*\(([ivx]{1,4})\)\s+(\S.*)$", re.I)
ELECTIVE = re.compile(r"^\s*(Elective\s+\d[^\n]{0,70})", re.I)
MARKS = re.compile(r"\((\d{1,3})\s*marks?\)", re.I)
MARKS_CELL = re.compile(r"⟨[^⟩]*⟩")


def enumerate_parts(text: str):
    """Sections are inferred from question SHAPE, not from headings.

    Headings cannot be trusted here: every scheme prints a rubric block naming
    all three sections a few lines apart, so reading them in order flips into
    Section C before a single Section A answer — which is how 2022 came back with
    no Section A at all. The shapes are stable across every paper in the corpus:
    Section A is short questions written "1.", Sections B and C are "Question 1"
    with lettered parts, and Section C is whatever follows an Elective heading.
    """
    out, section, elective, question, last_part = [], None, None, None, None
    for raw in text.split("\n"):
        line = MARKS_CELL.sub(" ", raw).rstrip()
        if SECTION.match(line):
            continue
        if (m := ELECTIVE.match(line)):
            elective, section, question = m.group(1).strip(), "C", None
            continue
        if (m := LONG_Q.match(line)):
            question = m.group(1)
            # Section B runs 1-5; Section C's core question restarts the count
            # under an Elective heading, which sets the section above.
            if section != "C":
                section = "B"
            continue
        if (m := ELECTIVE_Q.match(line)):
            question = m.group(1)
            out.append(_row(section or "C", elective, question, m.group(2), None, line, m.group(3)))
            continue
        if (m := SHORT_Q.match(line)):
            question, section = m.group(1), "A"
            out.append(_row(section, elective, question, None, None, line, m.group(2)))
            continue
        if question and (m := PART.match(line)):
            last_part = m.group(1)
            out.append(_row(section, elective, question, last_part, None, line, m.group(2)))
            continue
        # A roman sub-entry counts ONLY where it is separately marked.
        #
        # Both readings were wrong in turn. Counting them all inflated 2021
        # Higher's twelve Section A questions to twenty-eight, because there
        # "(i) Oxidative rancidity — This occurs as a result of…" is the ANSWER
        # to a short question. Counting none of them then made Section C parts
        # the unit, and a Section C (a) is three separately-marked sub-parts —
        # 16, 24 and 10 — which became one fifty-mark card holding five rows,
        # with the marking detail gone. A printed "(N marks)" is what separates a
        # question part from a line of answer text.
        if question and (m := SUBPART.match(line)) and MARKS.search(line):
            out.append(_row(section, elective, question, last_part, m.group(1), line, m.group(2)))
    return out


def _row(section, elective, question, part, sub, line, text):
    ref = f"Section {section} Q{question}"
    if part:
        ref += f"({part})"
    if sub:
        ref += f"({sub})"
    hit = MARKS.search(line)
    return {"ref": ref, "section": section, "elective": elective, "question": question,
            "part": part, "sub": sub, "marks": int(hit.group(1)) if hit else None,
            "text": text.strip()[:170]}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("scheme", type=Path)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    rows = enumerate_parts(args.scheme.read_text())
    if args.json:
        print(json.dumps(rows, indent=1))
    else:
        for r in rows:
            print(f"{r['ref']:26} {str(r['marks'] or ''):>4}  {r['text'][:78]}")
    print(f"{len(rows)} examinable parts in {args.scheme.name}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
