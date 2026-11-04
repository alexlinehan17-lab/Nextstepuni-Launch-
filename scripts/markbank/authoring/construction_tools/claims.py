"""claims.py YEAR LEVEL: check every draft row claim against the scheme .md with the deck's own rule."""
import json, re, subprocess, sys
from pathlib import Path
W = Path(__file__).resolve().parents[4]  # repository root
year, level = sys.argv[1], sys.argv[2]
tok = 'hl' if level == 'higher' else 'ol'
d = json.loads((W / f'docs/markbank-audit/2026-09-28/drafts/construction-{year}-{level}/{level}-{year}-draft.json').read_text())
claims = {}
for t in d['tasks']:
    for r in t['card']['rows']:
        for c in (r['group']['options'] if r['kind'] == 'anyN' and r.get('group') else [re.split(r'\s[—-]\s', r['verbatim'])[-1]]):
            claims.setdefault(c, set()).add(t['card']['id'])
inp = json.dumps(dict(scheme=f'examiner-reports/construction-studies/schemes/{year}-{tok}.md', claims=sorted(claims)))
out = json.loads(subprocess.run(['node', 'scripts/markbank/authoring/verify-claims.mjs'], input=inp, capture_output=True, text=True, cwd=W, check=True).stdout)
print(len(out['ok']), 'ok;', len(out['bad']), 'bad')
for c in out['bad']:
    print('  BAD', repr(c), sorted(claims[c])[:3])
