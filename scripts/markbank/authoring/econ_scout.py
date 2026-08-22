"""Print an Economics paper's question map, so a paper can be authored against
what the scheme actually contains rather than against what it is assumed to.

    python3 scripts/markbank/authoring/econ_scout.py 2024 higher
    python3 scripts/markbank/authoring/econ_scout.py 2024 higher --marks

The paper is Section A (Questions 1-10, short) and Section B (Questions 11-16,
long), plus a Student Research Project that is coursework and not carded.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from econ_lib import load, tidy  # noqa: E402

year, level = int(sys.argv[1]), sys.argv[2]
show_marks = '--marks' in sys.argv
T = load(year, level)

# The scheme repeats its section headers in the index and again over the answers;
# the body is what follows the LAST occurrence of each.
def last(pattern, before=None):
    hits = [m.start() for m in re.finditer(pattern, T)]
    if before is not None:
        hits = [h for h in hits if h < before]
    return hits[-1] if hits else None


a_start = last(r'SECTION A')
b_start = last(r'Section B: 300 marks')
print(f'# {year} {level}   {len(T):,} chars')
print(f'#   Section A body from {a_start}')
print(f'#   Section B body from {b_start}')
print()

body = T[a_start:] if a_start else T
flat = tidy(body)

# Question openers. Section B questions announce themselves as "Question 11";
# Section A's are a bare number in the leftmost table column, so they are found
# by their mark cell instead.
for m in re.finditer(r'Question\s+(1[1-6])\b', flat):
    print(f'  {m.start():7d}  {flat[m.start():m.start() + 150]}')

if show_marks:
    print('\n# mark cells')
    for m in re.finditer(r'⟨[^⟩]{1,18}⟩', flat):
        print(f'  {m.start():7d}  {m.group(0):<14} {flat[m.end():m.end() + 90]}')
