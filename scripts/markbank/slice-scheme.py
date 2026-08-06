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

sys.path.insert(0, str(Path(__file__).resolve().parent))
from scheme_structure import blocks_for  # noqa: E402


def slice_for(text, section, question):
    """Every block belonging to one question — the grid entry AND the notes.

    Missing either is worse than sending the whole file: the grid states the
    tariff notation and the notes carry the marking points, so half a question is
    half an answer. Returns None rather than guess, and the caller falls back.
    """
    lines = text.split("\n")
    kept = blocks_for(lines, section, question)
    if not kept:
        return None
    parts = []
    for start, end in kept:
        parts.append(f"[scheme lines {start + 1}-{end}]\n"
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
