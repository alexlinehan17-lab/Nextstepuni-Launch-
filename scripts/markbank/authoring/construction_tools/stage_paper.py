"""Stage one engine-reviewed Construction paper with explicit paths and Construction-only shared blobs.
stage_paper.py YEAR LEVEL"""
import json, subprocess, sys, tempfile
from pathlib import Path
W = Path(__file__).resolve().parents[4]  # repository root
SP = Path(tempfile.gettempdir()) / 'construction-stage'  # scratch for staged blobs; never committed
(SP / 'blobs').mkdir(parents=True, exist_ok=True)
year, level = sys.argv[1], sys.argv[2]
code = 'HL' if level == 'higher' else 'OL'
fileid = 'LC029ALP000EV' if level == 'higher' else 'LC029GLP000EV'
git = lambda *a: subprocess.check_output(['git', '-C', str(W), *a]).decode()  # noqa: E731
def blob(path, text):
    p = SP / 'blobs' / Path(path).name
    p.write_text(text)
    sha = git('hash-object', '-w', str(p)).strip()
    git('update-index', '--cacheinfo', f'100644,{sha},{path}')
    return sha
# shared JSON files: HEAD with only the construction-studies section taken from the worktree
for path in ['scripts/markbank/card-source-bindings.json', 'scripts/markbank/card-corrections.json']:
    head = git('show', f'HEAD:{path}')
    h, w = json.loads(head), json.loads((W / path).read_text())
    if h.get('construction-studies') != w.get('construction-studies'):
        h['construction-studies'] = w['construction-studies']
        text = json.dumps(h, ensure_ascii=False, indent=1 if head.startswith('{\n "') else 2) + '\n'
        rest_h = {k: v for k, v in json.loads(head).items() if k != 'construction-studies'}
        assert {k: v for k, v in json.loads(text).items() if k != 'construction-studies'} == rest_h
        print('blob', path, blob(path, text))
h = json.loads(git('show', 'HEAD:scripts/markbank/coverage-baseline.json'))
h['construction-studies'] = json.loads((W / 'scripts/markbank/coverage-baseline.json').read_text())['construction-studies']
print('blob baseline', blob('scripts/markbank/coverage-baseline.json', json.dumps(h, indent=2, sort_keys=True) + '\n'))
z = git('show', 'HEAD:components/MarkBank/cards/sizes.json'); hz = json.loads(z)['construction-studies']
wz = json.loads((W / 'components/MarkBank/cards/sizes.json').read_text())['construction-studies']
old = '"construction-studies": {\n  "higher": %d,\n  "ordinary": %d\n }' % (hz['higher'], hz['ordinary'])
assert z.count(old) == 1
print('blob sizes', blob('components/MarkBank/cards/sizes.json', z.replace(old, '"construction-studies": {\n  "higher": %d,\n  "ordinary": %d\n }' % (wz['higher'], wz['ordinary']))))
D = f'docs/markbank-audit/2026-09-28/drafts/construction-{year}-{level}'
paths = ['scripts/markbank/authored/construction-studies.json', f'components/MarkBank/cards/construction-studies/{level}.ts',
         'components/MarkBank/figures-construction-studies.json', 'data/examTopics/construction-studies-runtime.json',
         'data/markBank/construction-studies-library-topics.json', 'docs/markbank-audit/2026-09-28/construction-open-asks.json',
         f'{D}/construction-{year}-{level}-draft.py', f'{D}/construction-{year}-{level}-integrate.py', f'{D}/prior-{year}-{level}-cards.json',
         f'{D}/prior-authored-card-hashes.json', f'scripts/markbank/atlas-reviews/construction-studies-{year}-{level}.json',
         f'scripts/markbank/authored/construction-studies-{year}-{level}-reviewed.json', f'scripts/markbank/authoring/construction_{year}_{level}.py',
         f'scripts/markbank/authoring/test_construction_{year}_{level}.py', 'test/fixtures/constructionReviewedPapers.json']
anchor = f'public/paper-anchors/{year}/{fileid}.pdf.json'
if subprocess.run(['git', '-C', str(W), 'cat-file', '-e', f'HEAD:{anchor}'], capture_output=True).returncode != 0 and (W / anchor).exists():
    paths.append(anchor)
if git('diff', 'HEAD', '--name-only', '--', 'components/MarkBank/cardAliases.ts').strip():
    paths.append('components/MarkBank/cardAliases.ts')
pngs = sorted(str(p.relative_to(W)) for p in (W / 'public/exam-figures/construction-studies/markbank').glob(f'construction-studies-{year}-{code}-*.png'))
git('add', '--', *paths, *pngs)
stat = git('diff', '--cached', '--stat')
print('\n'.join(l for l in stat.splitlines() if '.png' not in l))
names = git('diff', '--cached', '--name-only').split()
print('pngs staged', sum(n.endswith('.png') for n in names))
allowed = ('construction', 'Construction', 'cardAliases.ts', 'sizes.json', 'coverage-baseline.json', 'card-source-bindings.json', 'card-corrections.json',
           'markBankCardPreservation.test.ts', 'constructionReviewedPapers', 'paper-anchors')
bad = [n for n in names if not any(a in n for a in allowed)]
print('outside Construction:', bad)
