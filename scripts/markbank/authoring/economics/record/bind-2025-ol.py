"""Bind every 2025 HL route to its complete official question pages (idempotent).

An existing binding keeps its other settings (stripStem); only its pages are set.
"""
from pathlib import Path
import json
W = str(Path(__file__).resolve().parents[5])
census = json.load(open(f'{W}/scripts/markbank/authoring/drafts/economics-2025-ol-ev.json'))
path = f'{W}/scripts/markbank/card-source-bindings.json'
b = json.load(open(path))
econ = b['economics']
n = 0
for q in census['questions']:
    for t in q['tasks']:
        econ.setdefault(t['cardId'], {})['pages'] = q['paperPages']
        n += 1
open(path, 'w').write(json.dumps(b, indent=2, ensure_ascii=False) + '\n')
print(n, 'bindings')
