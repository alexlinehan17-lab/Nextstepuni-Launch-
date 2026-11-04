"""Undo an UNCOMMITTED engine integration of one paper so it can be re-run: unintegrate.py YEAR LEVEL [--anchor]"""
import json, subprocess, sys
from pathlib import Path
W = Path(__file__).resolve().parents[4]  # repository root
year, level = sys.argv[1], sys.argv[2]
code = 'HL' if level == 'higher' else 'OL'
fileid = 'LC029ALP000EV' if level == 'higher' else 'LC029GLP000EV'
review = W / f'scripts/markbank/authored/construction-studies-{year}-{level}-reviewed.json'
d = json.loads(review.read_text())
# shared build overrides: put back exactly what the integration popped, in HEAD order
for x in d.get('retiredBuildOverrides', []):
    path = W / x['file']
    cur = json.loads(path.read_text())
    head = json.loads(subprocess.check_output(['git', '-C', str(W), 'show', 'HEAD:' + x['file']]))
    assert head['construction-studies'][x['cardId']] == x['override']
    if x['cardId'] in cur['construction-studies']:
        continue
    cur['construction-studies'] = head['construction-studies'] if all(k in head['construction-studies'] for k in cur['construction-studies']) else cur['construction-studies']
    path.write_text(json.dumps(cur, ensure_ascii=False, indent=2) + '\n')
# aliases
if d.get('withdrawn'):
    subprocess.check_call(['git', '-C', str(W), 'checkout', 'HEAD', '--', 'components/MarkBank/cardAliases.ts'])
subprocess.check_call(['git', '-C', str(W), 'checkout', 'HEAD', '--', 'scripts/markbank/authored/construction-studies.json', 'components/MarkBank/figures-construction-studies.json'])
for f in [review, W / f'scripts/markbank/atlas-reviews/construction-studies-{year}-{level}.json',
          W / f'docs/markbank-audit/2026-09-28/drafts/construction-{year}-{level}/integration.json',
          W / f'docs/markbank-audit/2026-09-28/drafts/construction-{year}-{level}/prior-authored-card-hashes.json']:
    f.unlink(missing_ok=True)
if '--anchor' in sys.argv:
    (W / f'public/paper-anchors/{year}/{fileid}.pdf.json').unlink()
for p in (W / 'public/exam-figures/construction-studies/markbank').glob(f'construction-studies-{year}-{code}-*.png'):
    p.unlink()
fx = W / 'test/fixtures/constructionReviewedPapers.json'
if fx.exists():
    papers = [p for p in json.loads(fx.read_text()) if (str(p['year']), p['level']) != (year, level)]
    if papers:
        fx.write_text(json.dumps(papers, ensure_ascii=False, indent=2) + '\n')
    else:
        fx.unlink()
print('unintegrated', year, level)
