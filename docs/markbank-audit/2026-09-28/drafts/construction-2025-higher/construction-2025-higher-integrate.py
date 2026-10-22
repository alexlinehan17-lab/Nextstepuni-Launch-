"""Integrate the validated 2025 Higher Q1-Q10 (and alternative Q10) draft into the Construction Studies runtime inputs.

NOT replay-safe: it refuses to run once the reviewed 2025 Higher file exists. Corrects the 21
pre-audit 2025 Higher cards in place (same IDs, hash-linked corrections), appends 52 new tasks
(all 997 other prior cards byte-identical), installs 37 inspected figures with manifest entries,
writes the hosted paper anchor (copied from the tracked classic sidecar, each anchor checked
against its printed question marker), the reviewed file, the exact Atlas bridge and the test
fixture/count updates. The 2025 Higher theory scheme text already ships in
examiner-reports/construction-studies/schemes/2025-hl.md and is left unchanged.
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
import construction_2025_higher as validator  # noqa: E402
import construction_corrections  # noqa: E402

import fitz  # noqa: E402


def read(p):
    return json.loads(Path(p).read_text())


def save(p, d):
    Path(p).write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n')


draft = read(HERE / 'higher-2025-draft.json')
report = validator.validate(draft, figure_dir=HERE, integrated=False)
review_path = R / 'scripts/markbank/authored/construction-studies-2025-higher-reviewed.json'
bridge_path = R / 'scripts/markbank/atlas-reviews/construction-studies-2025-higher.json'
authored_path = R / 'scripts/markbank/authored/construction-studies.json'
manifest_path = R / 'components/MarkBank/figures-construction-studies.json'
fixture = R / 'test/fixtures/construction2025Reviewed.ts'
anchor_path = R / 'public/paper-anchors/2025/LC029ALP000EV.pdf.json'
public = R / 'public/exam-figures/construction-studies/markbank'
assert not review_path.exists() and not bridge_path.exists() and not fixture.exists() and not anchor_path.exists()
assert (R / 'examiner-reports/construction-studies/schemes/2025-hl.md').exists()

prior = read(authored_path)
assert len(prior) == 1018 and len({c['id'] for c in prior}) == 1018
tasks = draft['tasks']
corrected = {t['card']['id']: t['card'] for t in tasks if t['correction']}
added = [t['card'] for t in tasks if not t['correction']]
assert len(corrected) == 21 and len(added) == 52
assert set(corrected) <= {c['id'] for c in prior} and not {c['id'] for c in added} & {c['id'] for c in prior}
assert not {c['questionRef'] for c in added} & {c['questionRef'] for c in prior if c['id'] not in corrected}
assert not {c['questionRef'] for c in corrected.values()} & {c['questionRef'] for c in prior if c['id'] not in corrected}
manifest = read(manifest_path)
assert len(manifest) == 139, len(manifest)
known_md5 = {e['md5'] for e in manifest.values()}

ALT = {
    'q1-original': 'Original SEC 2025 Higher Construction Studies Question 1: the printed question with a sketch of a triple-glazed window in a rendered external wall.',
    'q1-section': 'SEC model vertical section from the reinforced strip foundation through the insulated solid ground floor and timber-frame wall with block outer leaf to the triple-glazed window cill.',
    'q1-radon': 'SEC model detail at the floor and wall junction with an arrow to the radon barrier, labelled “Radon Barrier prevents the penetration of radon gas”.',
    'q2-original': 'Original SEC 2025 Higher Construction Studies Question 2: the printed question with a sketch of insulation rolls in an attic.',
    'q2-trench': 'SEC 2025 Higher marking scheme page on deep-trench safety, with sketches of a trench box, battered and unbattered trench sides, sheet piling and shoring.',
    'q2-attic': 'SEC 2025 Higher marking scheme guidelines for installing attic insulation, with dust-mask and goggle safety signs and a worker in protective clothing kneeling on boards.',
    'q2-chimney': 'SEC 2025 Higher marking scheme guidelines for repairing a chimney capping, with sketches of a worker in a safety harness and a cherry picker at a chimney.',
    'q3-original': 'Original SEC 2025 Higher Construction Studies Question 3: the printed question with the front elevation and ground-floor plan of a semi-detached house and garage, wall A-A marked.',
    'q3-layout-1': 'SEC model revised ground-floor plan 1: open-plan kitchen and dining in the former garage, a new downstairs bathroom and the layout notes.',
    'q3-layout-2': 'SEC model revised ground-floor plan 2: an open-plan kitchen/dining room across the garage and utility with a family bathroom, and the layout notes.',
    'q3-garage': 'SEC model sketches of the converted garage exterior with large glazing and roof lights in the flat roof, and the external design notes.',
    'q4-original': 'Original SEC 2025 Higher Construction Studies Question 4: the printed question with a sketch of a proposed new house.',
    'q4-requirements': 'SEC 2025 Higher marking scheme page on the functional requirements of an external wall, with sketches of load paths, an insulated wall, fire resistance and an insulated envelope.',
    'q4-walls': 'SEC 2025 Higher marking scheme page on high-performance wall types: block cavity, insulated concrete forms and solid block with external insulation, each with a section sketch.',
    'q5-original': 'Original SEC 2025 Higher Construction Studies Question 5: the printed question with a cut-away sketch of the externally insulated hollow-block wall and all the construction and thermal data.',
    'q5-calculation': 'SEC worked solution: the U-value table giving a total resistance of 4.531 and U = 0.221 W/m²°C, and the annual heat-loss cost of €76.34 by two methods.',
    'q5-thickness': 'SEC worked solution for the additional insulation: required resistance 9.091, difference 4.566, thickness 0.137 m (137 mm).',
    'q6-original': 'Original SEC 2025 Higher Construction Studies Question 6: the printed question with the elevation and L-shaped ground-floor plan of a single-storey house.',
    'q6-low-impact': 'SEC 2025 Higher marking scheme page on low-environmental-impact features, with sketches of solar gain on the plan, an insulated timber-frame wall with larch cladding and a compact form.',
    'q7-original': 'Original SEC 2025 Higher Construction Studies Question 7: the printed question with a sketch of a rendered chimney stack on a slated roof.',
    'q7-section': 'SEC model vertical section through a chimney stack and pitched roof: flue liners, blockwork, capping, DPC trays, lead flashings, back gutter, rafters and slates, with the list of details.',
    'q7-flashing': 'SEC model detail of the chimney stack and roof junction with arrows to the lead flashings and DPC trays, and notes for the back and front of the chimney.',
    'q8-original': 'Original SEC 2025 Higher Construction Studies Question 8: the printed question with an outline section of a two-storey house and four circled locations.',
    'q8-door-head': 'SEC model section at the head of an external door with an arrow to the airtight seal between the door frame and the wall.',
    'q8-first-floor': 'SEC model sketches of the first-floor junction with the external wall: airtightness membrane and tape around the joist ends.',
    'q8-wallplate': 'SEC model eaves section at wallplate level with an arrow to the airtightness membrane wrapped onto the wallplate and wall.',
    'q8-mvhr-duct': 'SEC model sketches of an MVHR duct through the ceiling sealed to the airtightness membrane with a grommet or with tape.',
    'q9-original': 'Original SEC 2025 Higher Construction Studies Question 9: the printed question with a sketch of a room with a light switch and two pendant lights.',
    'q9-wiring': 'SEC model wiring diagram of a lighting circuit from the distribution board to a single switch and two pendant light points, with the cable size and colours.',
    'q9-safety': 'SEC 2025 Higher marking scheme page on lighting-circuit safety features, with sketches of a labelled distribution board and an RCBO.',
    'q10-original': 'Original SEC 2025 Higher Construction Studies Question 10: the printed question with a sketch of a two-storey Passive House in a rural setting.',
    'q10-building-form': 'SEC 2025 Higher marking scheme notes on Passive House building form, with sketches contrasting a complex plan (crossed) and a simple rectangle (ticked).',
    'q10-foundation-design': 'SEC 2025 Higher marking scheme notes on Passive House foundation design, with sections of insulated foundations at the wall and floor junction.',
    'q10-space-heating-energy-demand': 'SEC 2025 Higher marking scheme notes on space heating energy demand, with a sketch of solar gain warming an insulated house section.',
    'q10-orientation': 'SEC model orientation and sun-path sketches with the long glazed elevation facing south, and the benefits to the homeowner.',
    'q10-overheating': 'SEC 2025 Higher marking scheme page on reducing solar overheating, with sketches of dynamic glass, deciduous trees, a brise soleil and shutters.',
    'q10-alt-original': 'Original SEC 2025 Higher Construction Studies alternative Question 10: the printed Heritage Ireland 2030 quotation on reusing historic buildings and its two parts.',
}
assert set(ALT) == {f['key'].removeprefix(validator.FP) for f in draft['questionFigures']}
for f in draft['questionFigures']:
    src = HERE / f"{f['key']}.png"
    md5 = hashlib.md5(src.read_bytes()).hexdigest()
    assert f['key'] not in manifest and md5 not in known_md5 and not (public / src.name).exists()
    known_md5.add(md5)

# Hosted paper anchor: the tracked classic sidecar's question anchors, each checked against its printed marker.
sidecar = read(R / 'scripts/paper-trail/answers/2025/LC029ALP000EV.pdf.json')
with fitz.open(R / validator.P) as pdf:
    for q in sidecar['q']:
        page = pdf[q['pP'] - 1]
        h = page.rect.height
        lines = [(ln['bbox'][1] / h, ''.join(s['text'] for s in ln['spans']).strip())
                 for b in page.get_text('dict')['blocks'] for ln in b.get('lines', [])]
        hits = [y for y, text in lines if text == f"{q['n']}."]
        assert hits and abs(min(hits, key=lambda y: abs(y - q['pY'][0])) - q['pY'][0]) < 0.02, (q['n'], q['pY'], hits)
anchor = dict(band=[1, 1], component='000', copyright=sidecar['copyright'], paperFileid=sidecar['paperFileid'], paperOnly=1, schemeFileid='', v=1,
              q=[dict(conf=0.5, mode='pagejump', n=q['n'], pP=q['pP'], pY=q['pY'], region=[{'p': 1}]) for q in sidecar['q']])
assert [q['n'] for q in anchor['q']] == [str(i) for i in range(1, 11)] and sidecar['paperFileid'] == 'LC029ALP000EV.pdf'
anchor_path.write_text(json.dumps(anchor, ensure_ascii=False, sort_keys=True, separators=(',', ':')))

now = datetime.now(timezone.utc).isoformat()
save(HERE / 'prior-authored-card-hashes.json', dict(count=1018, algorithm='sha256 of json.dumps(card, ensure_ascii=False, sort_keys=True)',
     cards={c['id']: construction_corrections.card_hash(c) for c in prior}))
for f in draft['questionFigures']:
    dst = public / f"{f['key']}.png"
    shutil.copyfile(HERE / dst.name, dst)
    manifest[f['key']] = dict(src='/' + str(dst.relative_to(R / 'public')), md5=hashlib.md5(dst.read_bytes()).hexdigest(),
                              alt=ALT[f['key'].removeprefix(validator.FP)], attribution='SEC Leaving Certificate Construction Studies 2025 Higher Level — © State Examinations Commission.',
                              solution=f['solution'])
save(manifest_path, manifest)
review = dict(draft, status='2025 Higher main English theory Q1–Q10 and the alternative Q10: 73 source-reviewed tasks (52 added, 21 pre-audit cards corrected in place under their original IDs); whole theory paper reconciled against the original paper and scheme. Practical component and Irish edition remain separate work.',
              reviewedAt=now, paperComplete=True,
              fullPaperReconciliation=dict(questions=10, alternativeQuestions=1, wholeQuestionRoutes=report['wholeQuestionRoutes'],
                                           examRubric='Any five of ten questions, 60 marks each, 300 total; no full-exam Cartesian cards.',
                                           method='Same-operator source review of paper pages 1–7 and scheme pages 2–47; validator construction_2025_higher.py.'),
              priorAuthoredCardHashes='docs/markbank-audit/2026-09-28/drafts/construction-2025-higher/prior-authored-card-hashes.json',
              priorCorrectedCards='docs/markbank-audit/2026-09-28/drafts/construction-2025-higher/prior-2025-higher-cards.json')
save(review_path, review)
merged = [corrected.get(c['id'], c) for c in prior] + added
save(authored_path, merged)
check = read(authored_path)
assert [c['id'] for c in check[:1018]] == [c['id'] for c in prior]
assert all(a == b for a, b in zip(check, prior) if a['id'] not in corrected) and check[1018:] == added
save(bridge_path, dict(schemaVersion=1, subjectId='construction-studies', year=2025, level='higher', lang='ev', sitting='main',
                       paperKey='single', reviewedAt=now, authoringReview=str(review_path.relative_to(R)), sourceHashes=draft['sourceHashes'],
                       expectedRuntimeCards=73,
                       reason='2025 Higher main English theory: all ten printed questions and the alternative Question 10 (sharing the original Q10 anchor); 73 source-reviewed tasks with every finite route, including the 21 pre-audit cards corrected in place. Practical/Irish/other papers remain open.',
                       questions=[dict(n=q, fileid='LC029ALP000EV.pdf',
                                       topicIds=sorted({t for b in draft['bindings'] if b['questionNumber'] == q for t in b['atlasTopicIds']}))
                                  for q in draft['questionsReviewed']],
                       cards=draft['bindings']))
added_ids = [c['id'] for c in added]
corrected_ids = [t['card']['id'] for t in tasks if t['correction']]
fixture.write_text('// Original 2025 Higher Q1–Q10 and the alternative Q10. ADDED: every separately marked task, every complete\n'
                   '// question and all finite routes (Q2 C(3,2), Q8 C(4,3), Q10 C(3,2)) not previously carded.\n'
                   '// CORRECTED: the pre-audit 2025 Higher cards, kept under their original IDs and corrected in place.\n'
                   'export const CONSTRUCTION_2025_HIGHER_ADDED_IDS = ' + json.dumps(added_ids, indent=2).replace('"', "'") + ';\n\n'
                   'export const CONSTRUCTION_2025_HIGHER_CORRECTED_IDS = ' + json.dumps(corrected_ids, indent=2).replace('"', "'") + ';\n')
p = R / 'test/constructionStudiesExamTopics.test.ts'
s = p.read_text()
for old, new in [
    ("import { CONSTRUCTION_2026_HIGHER_REVIEWED_IDS, CONSTRUCTION_2026_ORDINARY_REVIEWED_IDS } from './fixtures/construction2026Reviewed';",
     "import { CONSTRUCTION_2026_HIGHER_REVIEWED_IDS, CONSTRUCTION_2026_ORDINARY_REVIEWED_IDS } from './fixtures/construction2026Reviewed';\nimport { CONSTRUCTION_2025_HIGHER_ADDED_IDS } from './fixtures/construction2025Reviewed';"),
    ('    expect(CONSTRUCTION_HIGHER).toHaveLength(255 + CONSTRUCTION_2015_HIGHER_REVIEWED_IDS.length + CONSTRUCTION_2026_HIGHER_REVIEWED_IDS.length);',
     '    expect(CONSTRUCTION_HIGHER).toHaveLength(255 + CONSTRUCTION_2015_HIGHER_REVIEWED_IDS.length + CONSTRUCTION_2026_HIGHER_REVIEWED_IDS.length + CONSTRUCTION_2025_HIGHER_ADDED_IDS.length);'),
    (').size).toBe(505 + CONSTRUCTION_2015_HIGHER_REVIEWED_IDS.length + CONSTRUCTION_2015_ORDINARY_REVIEWED_IDS.length + CONSTRUCTION_2026_HIGHER_REVIEWED_IDS.length + CONSTRUCTION_2026_ORDINARY_REVIEWED_IDS.length);',
     ').size).toBe(505 + CONSTRUCTION_2015_HIGHER_REVIEWED_IDS.length + CONSTRUCTION_2015_ORDINARY_REVIEWED_IDS.length + CONSTRUCTION_2026_HIGHER_REVIEWED_IDS.length + CONSTRUCTION_2026_ORDINARY_REVIEWED_IDS.length + CONSTRUCTION_2025_HIGHER_ADDED_IDS.length);'),
]:
    assert s.count(old) == 1, old
    s = s.replace(old, new)
p.write_text(s)
p = R / 'test/markBankCardPreservation.test.ts'
s = p.read_text()
for old, new in [
    ("import { CONSTRUCTION_2026_HIGHER_REVIEWED_IDS, CONSTRUCTION_2026_ORDINARY_REVIEWED_IDS } from './fixtures/construction2026Reviewed';",
     "import { CONSTRUCTION_2026_HIGHER_REVIEWED_IDS, CONSTRUCTION_2026_ORDINARY_REVIEWED_IDS } from './fixtures/construction2026Reviewed';\nimport { CONSTRUCTION_2025_HIGHER_ADDED_IDS } from './fixtures/construction2025Reviewed';"),
    ('...CONSTRUCTION_2026_HIGHER_REVIEWED_IDS, ...CONSTRUCTION_2026_ORDINARY_REVIEWED_IDS]);',
     '...CONSTRUCTION_2026_HIGHER_REVIEWED_IDS, ...CONSTRUCTION_2026_ORDINARY_REVIEWED_IDS, ...CONSTRUCTION_2025_HIGHER_ADDED_IDS]);'),
]:
    assert s.count(old) == 1, old
    s = s.replace(old, new)
p.write_text(s)
save(HERE / 'integration.json', dict(reviewedAt=now, addedTasks=52, correctedTasks=21, priorAuthoredCardsPreserved=997, newAuthoredCount=1070, newFigures=37,
                                     wholeQuestionRoutes=report['wholeQuestionRoutes'], validator=report,
                                     status='Authored/bridge/anchor/test inputs applied; generation and runtime checks next.'))
print('Integrated 73 tasks (52 added, 21 corrected); authored deck input 1070 cards; 37 figures.')
