#!/usr/bin/env python3
"""
Mark Bank — cut a marking scheme down to one question.

An authoring agent needs one question's marking notes. It was being handed the
whole scheme and left to find them, and it did that by grepping: across three
waves, 415 agents made 5,294 shell calls — a thousand greps, seven hundred seds
— hunting through 40-75k characters of someone else's paper.

That hunt is what the run costs. Every turn re-sends the whole conversation, so
an agent that takes 28 turns to reach its answer pays for its context 28 times:
95% of all tokens spent on this deck were cache reads, against 3% for the cards
themselves. And the hunt is identical for every agent working the same paper,
and needs no judgement at all.

So do it once, here, deterministically.

    python3 scripts/markbank/slice-scheme.py <scheme.md> --section 3 --question 4

The slice keeps BOTH regions a question has: the structure grid near the front,
which states the tariff notation, and the support notes later, which carry the
marking points. Missing either is worse than sending the whole file, so when the
boundaries cannot be found with confidence this prints nothing and exits 3 —
the caller then falls back to the full scheme rather than authoring from half a
question.
"""

import argparse
import re
import sys
from pathlib import Path

# "Question 4", "Question 4 Max", "4 (A) Explain the term…" — the shapes a
# question boundary takes in the two regions of an SEC Business scheme.
GRID_HEAD = re.compile(r"^\s*Question\s+(\d+)\b", re.I)
NOTES_HEAD = re.compile(r"^\s*(\d+)\s*\((A|a)\)")
SECTION_HEAD = re.compile(r"^\s*Section\s*([123ABC])\b", re.I)


def regions(lines):
    """Every (question number, start, end) block found, in file order."""
    marks = []
    for i, line in enumerate(lines):
        m = GRID_HEAD.match(line) or NOTES_HEAD.match(line)
        if m:
            marks.append((int(m.group(1)), i))
    out = []
    for idx, (q, start) in enumerate(marks):
        end = marks[idx + 1][1] if idx + 1 < len(marks) else len(lines)
        out.append((q, start, end))
    return out


def section_bounds(lines, section):
    """Where the named section starts and the next one begins."""
    starts = [(i, m.group(1).upper()) for i, line in enumerate(lines)
              if (m := SECTION_HEAD.match(line))]
    hits = [i for i, s in starts if s == section.upper()]
    if not hits:
        return 0, len(lines)
    # A scheme names its sections repeatedly — 2024 Higher prints "Section 3"
    # three times, in the rubric, over the support notes, and again in a trailing
    # summary. The support notes are the LONGEST stretch between one heading for
    # this section and whatever heading follows it, so measure rather than
    # guessing an ordinal: taking the last hit landed on the trailing summary.
    best, span = (0, len(lines)), -1
    for start in hits:
        later = [i for i, _ in starts if i > start]
        end = later[0] if later else len(lines)
        if end - start > span:
            best, span = (start, end), end - start
    return best


def slice_for(text, section, question):
    lines = text.split("\n")
    blocks = [b for b in regions(lines) if b[0] == question]
    if not blocks:
        return None
    lo, hi = section_bounds(lines, section) if section else (0, len(lines))
    # Keep every block for this question: the grid entry AND the support notes.
    kept = []
    for q, start, end in blocks:
        kept.append((start, end))
    if not kept:
        return None
    parts = []
    for start, end in kept:
        where = "support notes" if lo <= start < hi else "structure grid"
        parts.append(f"[{where}, scheme lines {start + 1}-{end}]\n"
                     + "\n".join(lines[start:end]).strip())
    return "\n\n".join(parts)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("scheme", type=Path)
    ap.add_argument("--section", default=None, help="1, 2, 3, A, B or C")
    ap.add_argument("--question", type=int, required=True)
    args = ap.parse_args()

    text = args.scheme.read_text()
    out = slice_for(text, args.section, args.question)
    if not out:
        print(f"could not locate question {args.question} in {args.scheme.name}",
              file=sys.stderr)
        return 3
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
