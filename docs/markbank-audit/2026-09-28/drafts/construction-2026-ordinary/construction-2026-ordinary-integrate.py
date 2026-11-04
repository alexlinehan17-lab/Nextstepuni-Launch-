"""Integrate the validated 2026 Ordinary Q1-Q9 draft into the Construction Studies runtime inputs.

NOT replay-safe: it refuses to run once the reviewed 2026 Ordinary file exists. Appends 166 cards
(all 852 prior cards byte-identical), installs 33 inspected figures with manifest entries, and
writes the reviewed file, the exact Atlas bridge, the 2026 Ordinary theory scheme text and the
test fixture/count updates.
"""
import hashlib
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
R = HERE.parents[4]
sys.path.insert(0, str(R / 'scripts/markbank/authoring'))
import construction_2026_ordinary as validator  # noqa: E402

import fitz  # noqa: E402


def read(p):
    return json.loads(Path(p).read_text())


def save(p, d):
    Path(p).write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n')


draft = read(HERE / 'ordinary-2026-draft.json')
report = validator.validate(draft, figure_dir=HERE, integrated=False)
review_path = R / 'scripts/markbank/authored/construction-studies-2026-ordinary-reviewed.json'
bridge_path = R / 'scripts/markbank/atlas-reviews/construction-studies-2026-ordinary.json'
scheme_md = R / 'examiner-reports/construction-studies/schemes/2026-ol.md'
authored_path = R / 'scripts/markbank/authored/construction-studies.json'
manifest_path = R / 'components/MarkBank/figures-construction-studies.json'
fixture = R / 'test/fixtures/construction2026Reviewed.ts'
public = R / 'public/exam-figures/construction-studies/markbank'
assert not review_path.exists() and not bridge_path.exists() and not scheme_md.exists() and fixture.exists()

prior = read(authored_path)
assert len(prior) == 852 and len({c['id'] for c in prior}) == 852
new_cards = [t['card'] for t in draft['tasks']]
assert not {c['id'] for c in new_cards} & {c['id'] for c in prior}
assert not {c['questionRef'] for c in new_cards} & {c['questionRef'] for c in prior}
manifest = read(manifest_path)
assert len(manifest) == 106
known_md5 = {e['md5'] for e in manifest.values()}

ALT = {
    'q1-original': 'Original SEC 2026 Ordinary Construction Studies Question 1: the printed question with a cut-away sketch of the strip foundation, cavity wall and floating timber floor.',
    'q2-original': 'Original SEC 2026 Ordinary Construction Studies Question 2: the printed question with a sketch of a 1970s bungalow.',
    'q3-original': 'Original SEC 2026 Ordinary Construction Studies Question 3: the printed question with a cross-section of a two-storey house showing the bath, basin, toilet and kitchen sink.',
    'q4-original': 'Original SEC 2026 Ordinary Construction Studies Question 4: the printed question with the site location map showing site A, the road and the north point.',
    'q5-original': 'Original SEC 2026 Ordinary Construction Studies Question 5: the printed question with a sketch of the cavity wall beside an external wooden door.',
    'q6-original': 'Original SEC 2026 Ordinary Construction Studies Question 6: the printed question with a sketch of a student using a pillar drill.',
    'q7-original': 'Original SEC 2026 Ordinary Construction Studies Question 7: the printed question with the plan of the rear garden and patio.',
    'q8-original': 'Original SEC 2026 Ordinary Construction Studies Question 8: the printed list of nine terms, any five of which are explained.',
    'q9-original': 'Original SEC 2026 Ordinary Construction Studies Question 9: the printed question with a sketch of a farmhouse and its proposed timber-clad extension.',
    'q1-section': 'SEC model section through the strip foundation, cavity wall and insulated floor, with an arrow (b) to the radon barrier under the floor.',
    'q1-scheme': 'SEC 2026 Ordinary marking scheme page for Question 1: the model foundation, wall and floor section with its typical specification list.',
    'q2-scheme': 'SEC 2026 Ordinary marking scheme page for Question 2: advantages, the cavity-fill method with sketches, insulation types and thickness, and other upgrade areas.',
    'q2-upgrade': 'SEC model sketch of a window section and a roll of insulation, illustrating other upgrade areas.',
    'q3-system': 'SEC model cold water diagram: attic storage tank with overflow and valves, rising main, and cold feeds to the kitchen sink, bath, basin and toilet cistern, with the typical details listed.',
    'q3-water-butt': 'SEC model sketch of a green rainwater butt on a stand.',
    'q4-site-plan': 'SEC model sketch of site A with the house, a curved driveway from the road, the garage in a corner and hedgerow boundaries.',
    'q4-site-notice': 'SEC model sketch of a planning site notice headed Notice of Proposed Development.',
    'q5-section': 'SEC model section through the cavity wall, lintels, thermally broken door frame and insulated door, with the typical specification list.',
    'q5-wall-tie': 'SEC model detail with an arrow to a wall tie spanning the insulated cavity.',
    'q6-precautions': 'SEC table of safety precautions for using a scroll saw and for applying a spray finish, with a sketch of a respirator mask.',
    'q6-pillar-drill': 'SEC model sketch of a pillar drill with its guard, chuck and the work piece clamped in a vice.',
    'q7-garden-plan': 'SEC model garden plan with a patio dining area and cooking area by the house, a lawn with a play frame, and flowerbeds and trees along the boundary.',
    'q8-triple-glazing': 'SEC model sketch of a triple-glazed window section with three panes.',
    'q8-wind-turbine': 'SEC model sketch of a vertical-axis wind turbine.',
    'q8-carbon-monoxide-alarm': 'SEC model sketch of a carbon monoxide alarm.',
    'q8-mortise-and-tenon-joint': 'SEC model sketch of a mortise and tenon joint with the two parts separated.',
    'q8-butt-hinge': 'SEC model sketch of a butt hinge with its two leaves, knuckles and screw holes.',
    'q8-ball-valve': 'SEC model sketch of a lever-operated ball valve.',
    'q8-cordless-circular-saw': 'SEC model sketch of a cordless circular saw.',
    'q8-fascia-board': 'SEC model sketch of a profiled fascia board.',
    'q8-smart-meter': 'SEC model sketch of a smart electricity meter with its display.',
    'q9-extension': 'SEC model sketch of the timber-clad extension with additional windows, a large glazed door and decking to the garden.',
    'q9-cladding': 'Photograph from the SEC scheme of dark charred timber cladding around a glazed door.',
}
assert set(ALT) == {f['key'].removeprefix(validator.FP) for f in draft['questionFigures']}
for f in draft['questionFigures']:
    src = HERE / f"{f['key']}.png"
    md5 = hashlib.md5(src.read_bytes()).hexdigest()
    assert f['key'] not in manifest and md5 not in known_md5 and not (public / src.name).exists()
    known_md5.add(md5)

now = datetime.now(timezone.utc).isoformat()
save(HERE / 'prior-authored-card-hashes.json', dict(count=852, algorithm='sha256 of json.dumps(card, ensure_ascii=False, sort_keys=True)',
     cards={c['id']: hashlib.sha256(json.dumps(c, ensure_ascii=False, sort_keys=True).encode()).hexdigest() for c in prior}))
for f in draft['questionFigures']:
    dst = public / f"{f['key']}.png"
    shutil.copyfile(HERE / dst.name, dst)
    manifest[f['key']] = dict(src='/' + str(dst.relative_to(R / 'public')), md5=hashlib.md5(dst.read_bytes()).hexdigest(),
                              alt=ALT[f['key'].removeprefix(validator.FP)],
                              attribution='SEC Leaving Certificate Construction Studies 2026 Ordinary Level — © State Examinations Commission.',
                              solution=f['solution'])
save(manifest_path, manifest)
review = dict(draft, status='2026 Ordinary main English theory Q1–Q9: 166 source-reviewed tasks integrated; whole theory paper reconciled against the original paper and scheme. Practical component and Irish edition remain separate work.',
              reviewedAt=now, paperComplete=True,
              fullPaperReconciliation=dict(questions=9, wholeQuestionRoutes=report['wholeQuestionRoutes'], q8Routes=126,
                                           examRubric='Any four of nine questions, 50 marks each, 200 total; no full-exam Cartesian cards.',
                                           method='Same-operator source review of paper pages 1–4 and scheme pages 2–26; validator construction_2026_ordinary.py.'),
              priorAuthoredCardHashes='docs/markbank-audit/2026-09-28/drafts/construction-2026-ordinary/prior-authored-card-hashes.json')
save(review_path, review)
save(authored_path, prior + new_cards)
assert read(authored_path)[:852] == prior
save(bridge_path, dict(schemaVersion=1, subjectId='construction-studies', year=2026, level='ordinary', lang='ev', sitting='main',
                       paperKey='single', reviewedAt=now, authoringReview=str(review_path.relative_to(R)), sourceHashes=draft['sourceHashes'],
                       expectedRuntimeCards=166,
                       reason='2026 Ordinary main English theory: all nine printed questions and 166 source-reviewed tasks, including all 126 Q8 choose-five routes. Joinery/tools nodes without an Ordinary reference heading are declared in taxonomyGaps. Practical/Irish/other papers remain open.',
                       questions=[dict(n=q, fileid='LC029GLP000EV.pdf',
                                       topicIds=sorted({t for b in draft['bindings'] if b['questionNumber'] == q for t in b['atlasTopicIds']}))
                                  for q in draft['questionsReviewed']],
                       cards=draft['bindings'], taxonomyGaps=draft['taxonomyGaps']))
with fitz.open(R / validator.S) as pdf:
    raw = '\n\n'.join(f'<!-- Original PDF page {i + 1} -->\n' + p.get_text() for i, p in enumerate(pdf) if i < 26)
scheme_md.write_text('# SEC Construction Studies 2026 Ordinary theory marking scheme\n\n' + raw)

ids = [c['id'] for c in new_cards]
s = fixture.read_text()
assert 'CONSTRUCTION_2026_ORDINARY_REVIEWED_IDS' not in s
fixture.write_text(s + '\n// Original 2026 Ordinary Q1–Q9: every separately marked task, every complete question and all\n'
                   '// 126 choose-five Q8 routes (C(9,5)).\n'
                   'export const CONSTRUCTION_2026_ORDINARY_REVIEWED_IDS = ' + json.dumps(ids, indent=2).replace('"', "'") + ';\n')
for path, pairs in [
    ('test/constructionStudiesExamTopics.test.ts', [
        ("import { CONSTRUCTION_2026_HIGHER_REVIEWED_IDS } from './fixtures/construction2026Reviewed';",
         "import { CONSTRUCTION_2026_HIGHER_REVIEWED_IDS, CONSTRUCTION_2026_ORDINARY_REVIEWED_IDS } from './fixtures/construction2026Reviewed';"),
        ('    expect(CONSTRUCTION_ORDINARY).toHaveLength(250 + CONSTRUCTION_2015_ORDINARY_REVIEWED_IDS.length);',
         '    expect(CONSTRUCTION_ORDINARY).toHaveLength(250 + CONSTRUCTION_2015_ORDINARY_REVIEWED_IDS.length + CONSTRUCTION_2026_ORDINARY_REVIEWED_IDS.length);'),
        ('CONSTRUCTION_2015_ORDINARY_REVIEWED_IDS.length + CONSTRUCTION_2026_HIGHER_REVIEWED_IDS.length);',
         'CONSTRUCTION_2015_ORDINARY_REVIEWED_IDS.length + CONSTRUCTION_2026_HIGHER_REVIEWED_IDS.length + CONSTRUCTION_2026_ORDINARY_REVIEWED_IDS.length);'),
    ]),
    ('test/markBankCardPreservation.test.ts', [
        ("import { CONSTRUCTION_2026_HIGHER_REVIEWED_IDS } from './fixtures/construction2026Reviewed';",
         "import { CONSTRUCTION_2026_HIGHER_REVIEWED_IDS, CONSTRUCTION_2026_ORDINARY_REVIEWED_IDS } from './fixtures/construction2026Reviewed';"),
        ('...CONSTRUCTION_2026_HIGHER_REVIEWED_IDS]);', '...CONSTRUCTION_2026_HIGHER_REVIEWED_IDS, ...CONSTRUCTION_2026_ORDINARY_REVIEWED_IDS]);'),
    ]),
]:
    p = R / path
    s = p.read_text()
    for old, new in pairs:
        assert s.count(old) == 1, (path, old)
        s = s.replace(old, new)
    p.write_text(s)
save(HERE / 'integration.json', dict(reviewedAt=now, addedTasks=166, priorAuthoredCardsPreserved=852, newAuthoredCount=1018, newFigures=33,
                                     wholeQuestionRoutes=report['wholeQuestionRoutes'], validator=report,
                                     status='Authored/bridge/test inputs applied; generation and runtime checks next.'))
print('Integrated 166 tasks; authored deck input 1018 cards; 33 figures.')
