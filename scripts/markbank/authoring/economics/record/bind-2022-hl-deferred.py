"""Bind every 2022 HL deferred route to its complete official question pages (idempotent).

The pages are the deferred paper's, named by its Paper Trail id."""
from pathlib import Path
import json
W = str(Path(__file__).resolve().parents[5])
census = json.load(open(f'{W}/scripts/markbank/authoring/drafts/economics-2022-hl-deferred-ev.json'))
path = f'{W}/scripts/markbank/card-source-bindings.json'
b = json.load(open(path))
econ = b['economics']
n = 0
for q in census['questions']:
    for t in q['tasks']:
        econ[t['cardId']] = {'pages': q['paperPages'], 'sourceFileid': 'LC034ALP000EV-deferred'}
        n += 1
open(path, 'w').write(json.dumps(b, indent=2, ensure_ascii=False) + '\n')
print(n, 'bindings')
