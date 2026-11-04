"""Remove one appended manifest entry by key, preserving every other byte."""
from pathlib import Path
import json, sys
m = str(Path(__file__).resolve().parents[5] / 'components/MarkBank/figures.json')
t = open(m).read()
key = sys.argv[1]
assert key in json.loads(t)
a = t.index(f'  "{key}": {{')
b = t.index('\n  }', a) + 4
if t[b:b + 2] == ',\n':
    t = t[:a] + t[b + 2:]
else:
    t = t[:a].rstrip().rstrip(',') + '\n' + t[b:].lstrip('\n')
json.loads(t)
open(m, 'w').write(t)
print('removed', key)
