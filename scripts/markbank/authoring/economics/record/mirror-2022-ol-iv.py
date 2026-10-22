"""Mirror the three 2022 OL English route collapses into the Irish review's task lists only.

Q3, Q8 and Q14(b): the two task entries become one, keyed as the English census
keys them. No Irish reason, guidance or evidence text is re-reviewed or edited.
"""
import json
from pathlib import Path
p = (Path(__file__).resolve().parents[5] / 'scripts/markbank/authoring/reviews/economics-2022-ol-iv.json')
text = p.read_text()
d = json.loads(text)
P = 'econ-2022-ol-'
merge = {'3': ('i', 'ii', 'i+ii', 15), '8': ('i', 'ii', 'i+ii', 15), '14': ('b/i', 'b/ii', 'b/i+ii', 17)}
for q in d['questions']:
    if q['n'] not in merge: continue
    first, second, key, marks = merge[q['n']]
    keys = [t['key'] for t in q['tasks']]
    if key in keys: continue
    i, j = keys.index(first), keys.index(second)
    assert j == i + 1 and not q['tasks'][j].get('answerGuidance'), q['n']
    q['tasks'][i] = dict(q['tasks'][i], key=key, marks=marks)
    del q['tasks'][j]
indent = 2 if text.startswith('{\n  "') else 1
p.write_text(json.dumps(d, ensure_ascii=False, indent=indent) + ('\n' if text.endswith('\n') else ''))
print('mirrored')
