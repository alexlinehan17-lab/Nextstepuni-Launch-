"""prevalidate.py YEAR LEVEL: validate a draft against its module before integration."""
import json, sys, importlib
from pathlib import Path
W = Path(__file__).resolve().parents[4]  # repository root
sys.path.insert(0, str(W / 'scripts/markbank/authoring'))
year, level = sys.argv[1], sys.argv[2]
m = importlib.import_module(f'construction_{year}_{level}')
D = W / f'docs/markbank-audit/2026-09-28/drafts/construction-{year}-{level}'
print(m.validate(json.loads((D / f'{level}-{year}-draft.json').read_text()), figure_dir=D, integrated=False))
