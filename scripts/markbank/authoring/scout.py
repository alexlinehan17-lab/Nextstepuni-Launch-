"""Print the Section C bounds and question map for a paper."""
import re, sys
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from he_lib import load, tidy

year, level = int(sys.argv[1]), sys.argv[2]
T = load(year, level)
starts = [m.start() for m in re.finditer(r'Section C', T)]
ends = [m.start() for m in re.finditer(r'Food Studies Coursework', T)]
a = [s for s in starts if s > 8000][-1] if len(starts) > 1 else starts[-1]
# the real Section C body starts at the LAST 'Section C' before the coursework block
b = min([e for e in ends if e > a], default=len(T))
a = max([s for s in starts if s < b], default=a)
print(f'# {year} {level}: SEC = T[{a}:{b}]   ({b-a} chars)')
sec = tidy(T[a:b])
for m in re.finditer(r'Elective \d[^C]{0,60}|Question 4 – Core[^C]{0,40}', sec):
    print(f'  {m.start():6d}  {m.group(0)[:80]}')
print()
for m in re.finditer(r'\d\.\((?:[a-c])\)|\((?:i{1,3}|iv)\)|\(\d+ marks\)|\d+ marks\)', sec):
    ctx = sec[m.start():m.start()+120]
    if re.match(r'\d\.\([a-c]\)|\((?:i{1,3}|iv)\)', m.group(0)):
        print(f'  {m.start():6d}  {ctx[:118]}')
