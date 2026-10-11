"""Integrate the validated 2026 Higher Q1-Q10 (and alternative Q10) draft into the Construction Studies runtime inputs.

NOT replay-safe: it refuses to run once the reviewed 2026 Higher file exists. Appends 69 cards
(all 783 prior cards byte-identical), installs 36 inspected figures with manifest entries, and
writes the reviewed file, the exact Atlas bridge, the 2026 Higher theory scheme text and the
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
import construction_2026_higher as validator  # noqa: E402

import fitz  # noqa: E402


def read(p):
    return json.loads(Path(p).read_text())


def save(p, d):
    Path(p).write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n')


draft = read(HERE / 'higher-2026-draft.json')
report = validator.validate(draft, figure_dir=HERE, integrated=False)
review_path = R / 'scripts/markbank/authored/construction-studies-2026-higher-reviewed.json'
bridge_path = R / 'scripts/markbank/atlas-reviews/construction-studies-2026-higher.json'
scheme_md = R / 'examiner-reports/construction-studies/schemes/2026-hl.md'
authored_path = R / 'scripts/markbank/authored/construction-studies.json'
manifest_path = R / 'components/MarkBank/figures-construction-studies.json'
fixture = R / 'test/fixtures/construction2026Reviewed.ts'
public = R / 'public/exam-figures/construction-studies/markbank'
assert not review_path.exists() and not bridge_path.exists() and not scheme_md.exists() and not fixture.exists()

prior = read(authored_path)
assert len(prior) == 783 and len({c['id'] for c in prior}) == 783
new_cards = [t['card'] for t in draft['tasks']]
assert not {c['id'] for c in new_cards} & {c['id'] for c in prior}
assert not {c['questionRef'] for c in new_cards} & {c['questionRef'] for c in prior}
manifest = read(manifest_path)
assert len(manifest) == 70
known_md5 = {e['md5'] for e in manifest.values()}

ALT = {
    'q1-original': 'Original SEC 2026 Higher Construction Studies Question 1: the printed question with a sketch of a house with a slated cut roof.',
    'q1-roof-section': 'SEC model section through one half of a traditional cut roof and cavity external wall: rafters, purlin, strut, collar tie, ceiling joists with layered insulation, eaves ventilation, slates and gutter.',
    'q1-airtightness': 'SEC model eaves detail with an arrow to the airtightness tape sealing the junction of the ceiling and the external wall.',
    'q2-original': 'Original SEC 2026 Higher Construction Studies Question 2: the printed question with the ground-floor plan of a draft garage conversion.',
    'q2-entrance-access': 'SEC 2026 Higher marking scheme page on lifetime-use entrance access, with sketches of a level threshold under a canopy, a recessed drainage channel and a 1000 mm wide entrance door.',
    'q2-bathroom': 'SEC 2026 Higher marking scheme page on a lifetime-use bathroom, with sketches of a Ø1800 mm turning circle in plan and grab rails, WC and basin heights in elevation.',
    'q2-kitchen-plan': 'SEC model plan of the garage conversion with wheelchair turning circles marked in the kitchen, dining and living areas.',
    'q3-original': 'Original SEC 2026 Higher Construction Studies Question 3: the printed question with the farmhouse front elevation and ground-floor plan marked A-A and B-B.',
    'q3-option-1': 'SEC model option 1: revised farmhouse ground-floor plan with a rear extension, open-plan kitchen, dining and living area on the south side, and the layout notes.',
    'q3-option-2': 'SEC model option 2: revised farmhouse ground-floor plan with a glazed south extension for the living area, and the layout notes.',
    'q4-original': 'Original SEC 2026 Higher Construction Studies Question 4: the printed question with a sketch of a brick railway keeper’s cottage.',
    'q4-stone-wall': 'SEC 2026 Higher marking scheme page on upgrading a solid stone wall, with sections showing breathable insulation and lime plaster on the inside face.',
    'q4-cut-roof': 'SEC 2026 Higher marking scheme page on upgrading a traditional cut roof, with sketches of spliced rafter repairs and an insulated slated roof at the eaves.',
    'q4-sash-windows': 'SEC 2026 Higher marking scheme page on repairing sliding sash windows, with sketches of a sash window and of secondary glazing.',
    'q5-original': 'Original SEC 2026 Higher Construction Studies Question 5: the printed question with a cut-away sketch of the timber-frame wall and all the construction and thermal data.',
    'q5-calculation': 'SEC worked solution: the U-value table giving a total resistance of 7.367 and U = 0.136 W/m²°C, and the annual heat-loss cost of €40.27 by two methods.',
    'q5-moisture': 'SEC model timber-frame wall section with arrows to the outer breather membrane and the inner vapour control layer, with notes.',
    'q6-original': 'Original SEC 2026 Higher Construction Studies Question 6: the printed question with the house elevation and ground-floor plan around a central courtyard.',
    'q6-low-impact': 'SEC 2026 Higher marking scheme page on low-environmental-impact features, with sketches of timber-frame and stone walls and of south-facing glazing.',
    'q6-nature': 'SEC 2026 Higher marking scheme page on connection with nature, with sketches of large folding glazed doors and of a person working beside a window.',
    'q7-original': 'Original SEC 2026 Higher Construction Studies Question 7: the printed question with a sketch of an open riser wooden stairs.',
    'q7-stairs': 'SEC model section through an open riser stairs showing newel post, balusters, string and handrail, 100 mm sphere gaps, the 840–900 mm handrail height and the design rules.',
    'q8-original': 'Original SEC 2026 Higher Construction Studies Question 8: the printed question with a sketch of an en-suite shower room.',
    'q8-stack': 'SEC model sketch of a single-stack soil and vent pipe serving a shower, basin and WC on the first floor.',
    'q8-traps': 'SEC model sketches of a deep-seal trap and a basin trap connected to the stack.',
    'q9-original': 'Original SEC 2026 Higher Construction Studies Question 9: the printed question with a wall section showing four circled locations at the eaves, window head, window cill and ground floor.',
    'q9-wall-roof': 'SEC model detail at the wall and roof junction showing continuous wall and roof insulation at the eaves.',
    'q9-window-head': 'SEC model detail at the window head showing the insulated head and cavity closer.',
    'q9-window-cill': 'SEC model detail at the window cill showing insulation continued under the cill.',
    'q9-wall-floor': 'SEC model detail at the wall and floor junction showing perimeter insulation meeting the cavity insulation.',
    'q9-details': 'SEC model details for all four circled locations: eaves, window head, window cill and the wall-floor junction.',
    'q10-original': 'Original SEC 2026 Higher Construction Studies Question 10: the printed question with a sketch of a retrofitted bungalow.',
    'q10-areas': 'SEC 2026 Higher marking scheme page listing building-fabric areas for an EnerPHit retrofit, with a sketch of the insulated envelope.',
    'q10-retrofit': 'SEC 2026 Higher marking scheme page on retrofitting external walls and the ground floor, with insulated wall and floor sketches.',
    'q10-blower-door': 'SEC model sketch of a blower door test: a fan in a frame fitted to the doorway, with arrows showing air leakage through the house.',
    'q10-alt-original': 'Original SEC 2026 Higher Construction Studies alternative Question 10: the printed quotation on indoor air quality and its two parts.',
}
assert set(ALT) == {f['key'].removeprefix(validator.FP) for f in draft['questionFigures']}
for f in draft['questionFigures']:
    src = HERE / f"{f['key']}.png"
    md5 = hashlib.md5(src.read_bytes()).hexdigest()
    assert f['key'] not in manifest and md5 not in known_md5 and not (public / src.name).exists()
    known_md5.add(md5)

now = datetime.now(timezone.utc).isoformat()
save(HERE / 'prior-authored-card-hashes.json', dict(count=783, algorithm='sha256 of json.dumps(card, ensure_ascii=False, sort_keys=True)',
     cards={c['id']: hashlib.sha256(json.dumps(c, ensure_ascii=False, sort_keys=True).encode()).hexdigest() for c in prior}))
for f in draft['questionFigures']:
    dst = public / f"{f['key']}.png"
    shutil.copyfile(HERE / dst.name, dst)
    manifest[f['key']] = dict(src='/' + str(dst.relative_to(R / 'public')), md5=hashlib.md5(dst.read_bytes()).hexdigest(),
                              alt=ALT[f['key'].removeprefix(validator.FP)],
                              attribution='SEC Leaving Certificate Construction Studies 2026 Higher Level — © State Examinations Commission.',
                              solution=f['solution'])
save(manifest_path, manifest)
review = dict(draft, status='2026 Higher main English theory Q1–Q10 and the alternative Q10: 69 source-reviewed tasks integrated; whole theory paper reconciled against the original paper and scheme. Practical component and Irish edition remain separate work.',
              reviewedAt=now, paperComplete=True,
              fullPaperReconciliation=dict(questions=10, alternativeQuestions=1, wholeQuestionRoutes=report['wholeQuestionRoutes'],
                                           examRubric='Any five of ten questions, 60 marks each, 300 total; no full-exam Cartesian cards.',
                                           method='Same-operator source review of paper pages 1–7 and scheme pages 2–53; validator construction_2026_higher.py.'),
              priorAuthoredCardHashes='docs/markbank-audit/2026-09-28/drafts/construction-2026-higher/prior-authored-card-hashes.json')
save(review_path, review)
save(authored_path, prior + new_cards)
assert read(authored_path)[:783] == prior
save(bridge_path, dict(schemaVersion=1, subjectId='construction-studies', year=2026, level='higher', lang='ev', sitting='main',
                       paperKey='single', reviewedAt=now, authoringReview=str(review_path.relative_to(R)), sourceHashes=draft['sourceHashes'],
                       expectedRuntimeCards=69,
                       reason='2026 Higher main English theory: all ten printed questions and the alternative Question 10 (sharing the original Q10 anchor); 69 source-reviewed tasks with every finite route. Practical/Irish/other papers remain open.',
                       questions=[dict(n=q, fileid='LC029ALP000EV.pdf',
                                       topicIds=sorted({t for b in draft['bindings'] if b['questionNumber'] == q for t in b['atlasTopicIds']}))
                                  for q in draft['questionsReviewed']],
                       cards=draft['bindings']))
with fitz.open(R / validator.S) as pdf:
    raw = '\n\n'.join(f'<!-- Original PDF page {i + 1} -->\n' + p.get_text() for i, p in enumerate(pdf) if i < 53)
scheme_md.write_text('# SEC Construction Studies 2026 Higher theory marking scheme\n\n' + raw)

ids = [c['id'] for c in new_cards]
fixture.write_text('// Original 2026 Higher Q1–Q10 and the alternative Q10: every separately marked task, every\n'
                   '// complete question and all finite routes (Q4 3 × 3, Q9 C(4,3)).\n'
                   'export const CONSTRUCTION_2026_HIGHER_REVIEWED_IDS = ' + json.dumps(ids, indent=2).replace('"', "'") + ';\n')
p = R / 'test/constructionStudiesExamTopics.test.ts'
s = p.read_text()
for old, new in [
    ("import { CONSTRUCTION_2015_HIGHER_REVIEWED_IDS, CONSTRUCTION_2015_ORDINARY_REVIEWED_IDS } from './fixtures/construction2015Reviewed';",
     "import { CONSTRUCTION_2015_HIGHER_REVIEWED_IDS, CONSTRUCTION_2015_ORDINARY_REVIEWED_IDS } from './fixtures/construction2015Reviewed';\nimport { CONSTRUCTION_2026_HIGHER_REVIEWED_IDS } from './fixtures/construction2026Reviewed';"),
    ('    expect(CONSTRUCTION_HIGHER).toHaveLength(255 + CONSTRUCTION_2015_HIGHER_REVIEWED_IDS.length);',
     '    expect(CONSTRUCTION_HIGHER).toHaveLength(255 + CONSTRUCTION_2015_HIGHER_REVIEWED_IDS.length + CONSTRUCTION_2026_HIGHER_REVIEWED_IDS.length);'),
    (').size).toBe(505 + CONSTRUCTION_2015_HIGHER_REVIEWED_IDS.length + CONSTRUCTION_2015_ORDINARY_REVIEWED_IDS.length);',
     ').size).toBe(505 + CONSTRUCTION_2015_HIGHER_REVIEWED_IDS.length + CONSTRUCTION_2015_ORDINARY_REVIEWED_IDS.length + CONSTRUCTION_2026_HIGHER_REVIEWED_IDS.length);'),
]:
    assert s.count(old) == 1, old
    s = s.replace(old, new)
p.write_text(s)
p = R / 'test/markBankCardPreservation.test.ts'
s = p.read_text()
for old, new in [
    ("import { CONSTRUCTION_2015_HIGHER_REVIEWED_IDS, CONSTRUCTION_2015_ORDINARY_REVIEWED_IDS } from './fixtures/construction2015Reviewed';",
     "import { CONSTRUCTION_2015_HIGHER_REVIEWED_IDS, CONSTRUCTION_2015_ORDINARY_REVIEWED_IDS } from './fixtures/construction2015Reviewed';\nimport { CONSTRUCTION_2026_HIGHER_REVIEWED_IDS } from './fixtures/construction2026Reviewed';"),
    ('const recoveredConstructionIds = new Set([...CONSTRUCTION_2015_HIGHER_REVIEWED_IDS, ...CONSTRUCTION_2015_ORDINARY_REVIEWED_IDS]);',
     'const recoveredConstructionIds = new Set([...CONSTRUCTION_2015_HIGHER_REVIEWED_IDS, ...CONSTRUCTION_2015_ORDINARY_REVIEWED_IDS, ...CONSTRUCTION_2026_HIGHER_REVIEWED_IDS]);'),
]:
    assert s.count(old) == 1, old
    s = s.replace(old, new)
p.write_text(s)
save(HERE / 'integration.json', dict(reviewedAt=now, addedTasks=69, priorAuthoredCardsPreserved=783, newAuthoredCount=852, newFigures=36,
                                     wholeQuestionRoutes=report['wholeQuestionRoutes'], validator=report,
                                     status='Authored/bridge/test inputs applied; generation and runtime checks next.'))
print('Integrated 69 tasks; authored deck input 852 cards; 36 figures.')
