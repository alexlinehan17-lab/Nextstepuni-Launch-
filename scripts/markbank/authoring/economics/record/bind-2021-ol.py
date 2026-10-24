"""Bind every 2021 OL route to its complete official question pages (idempotent).

Every 2021 OL stem is now lifted from the paper, so the stripStem an earlier pass
set on sa-q2, sa-q4 and q12-a-ii while they carried written text is dropped.
"""
from pathlib import Path
import json
W = str(Path(__file__).resolve().parents[5])
census = json.load(open(f'{W}/scripts/markbank/authoring/drafts/economics-2021-ol-ev.json'))
path = f'{W}/scripts/markbank/card-source-bindings.json'
b = json.load(open(path))
econ = b['economics']
n = 0
for q in census['questions']:
    for t in q['tasks']:
        econ[t['cardId']] = {'pages': q['paperPages']}
        n += 1
open(path, 'w').write(json.dumps(b, indent=2, ensure_ascii=False) + '\n')
print(n, 'bindings')
