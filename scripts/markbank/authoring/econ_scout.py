"""Print an Economics paper's cardable parts, so a paper is authored against
what the scheme contains rather than against what it is assumed to.

    python3 scripts/markbank/authoring/econ_scout.py 2025 higher
    python3 scripts/markbank/authoring/econ_scout.py 2025 higher 13    # one question

Each line is one mark cell with the question text that precedes it — which is
the unit a card is made from. `⟨2 @ 7⟩` over a list of named responses is a
menu; `⟨8⟩` on its own is usually a calculation or a single definite answer;
two cells in a row (`⟨1 @ 6⟩ ⟨1 @ 4⟩`, or "1st @ 8 / 2nd @ 4" at Ordinary
Level) is a descending tariff.

The paper is Section A (Questions 1-10, short) and Section B (Questions 11-16,
long), plus a Student Research Project that is coursework and not carded.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from econ_lib import load, tidy  # noqa: E402

year, level = int(sys.argv[1]), sys.argv[2]
only = sys.argv[3] if len(sys.argv) > 3 else None
T = tidy(load(year, level))

# The scheme prints its answers once and the appended blocks repeat them, so the
# body is bounded to the first pass; anchoring past that finds a table cell.
# The INDEX lists "Question 11" too, and on some papers it is the first match —
# which anchored the whole scout inside the front matter, where there are no
# mark cells at all. The body heading is the one followed by the scheme's own
# "Possible responses" caption.
starts = [(m.group(1), m.start()) for m in re.finditer(r'Question (1[1-6])\b', T)
          if re.search(r'Possible [Rr]esponses', T[m.start():m.start() + 60])]
if not starts:                       # a paper that does not print the caption
    starts = [(m.group(1), m.start()) for m in re.finditer(r'Question (1[1-6])\b', T)]
first = {}
for q, at in starts:
    first.setdefault(q, at)
order = sorted(first.items(), key=lambda kv: kv[1])
bounds = {q: (at, order[i + 1][1] if i + 1 < len(order) else at + 20000)
          for i, (q, at) in enumerate(order)}

CELL = re.compile(r'⟨[^⟩]{1,16}⟩|\d+(?:st|nd|rd|th)\s*@\s*\d+')

for q, (a, b) in bounds.items():
    if only and q != only:
        continue
    seg = T[a:b]
    print(f'\n══ Question {q}   T[{a}:{b}]  ({b - a} chars)')
    prev = 0
    for m in CELL.finditer(seg):
        before = tidy(seg[max(prev, m.start() - 190):m.start()])
        print(f'  {a + m.start():>7}  {m.group(0):<10} …{before[-165:]}')
        prev = m.end()
