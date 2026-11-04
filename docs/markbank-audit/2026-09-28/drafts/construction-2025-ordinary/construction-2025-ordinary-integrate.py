"""Integrate the validated 2025 Ordinary Q1-Q9 draft into the Construction Studies runtime inputs.

NOT replay-safe: it refuses to run once the reviewed 2025 Ordinary file exists. Corrects the 21
pre-audit 2025 Ordinary cards in place (same IDs, hash-linked corrections), appends 14 new tasks
(all 1,049 other prior cards byte-identical), installs 25 inspected figures with manifest entries,
retires the build-time override of cons-2025-ol-q7-c-advantage, and writes the reviewed file, the
exact Atlas bridge and the test fixture/count updates. The hosted paper anchor and the 2025
Ordinary theory scheme text already ship and are left unchanged.
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
import construction_2025_ordinary as validator  # noqa: E402
import construction_corrections  # noqa: E402


def read(p):
    return json.loads(Path(p).read_text())


def save(p, d):
    Path(p).write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n')


draft = read(HERE / 'ordinary-2025-draft.json')
report = validator.validate(draft, figure_dir=HERE, integrated=False)
review_path = R / 'scripts/markbank/authored/construction-studies-2025-ordinary-reviewed.json'
bridge_path = R / 'scripts/markbank/atlas-reviews/construction-studies-2025-ordinary.json'
authored_path = R / 'scripts/markbank/authored/construction-studies.json'
manifest_path = R / 'components/MarkBank/figures-construction-studies.json'
corrections_path = R / 'scripts/markbank/card-corrections.json'
fixture = R / 'test/fixtures/construction2025Reviewed.ts'
public = R / 'public/exam-figures/construction-studies/markbank'
assert not review_path.exists() and not bridge_path.exists() and 'ORDINARY' not in fixture.read_text()
assert (R / 'examiner-reports/construction-studies/schemes/2025-ol.md').exists()
anchor = read(R / 'public/paper-anchors/2025/LC029GLP000EV.pdf.json')
assert anchor['paperOnly'] == 1 and [q['n'] for q in anchor['q']] == [str(i) for i in range(1, 10)]

prior = read(authored_path)
assert len(prior) == 1070 and len({c['id'] for c in prior}) == 1070
tasks = draft['tasks']
corrected = {t['card']['id']: t['card'] for t in tasks if t['correction']}
added = [t['card'] for t in tasks if not t['correction']]
assert len(corrected) == 21 and len(added) == 14
assert set(corrected) <= {c['id'] for c in prior} and not {c['id'] for c in added} & {c['id'] for c in prior}
assert not {c['questionRef'] for c in [*added, *corrected.values()]} & {c['questionRef'] for c in prior if c['id'] not in corrected}
manifest = read(manifest_path)
assert len(manifest) == 176, len(manifest)
known_md5 = {e['md5'] for e in manifest.values()}

ALT = {
    'q1-original': 'Original SEC 2025 Ordinary Construction Studies Question 1: the printed question with a sketch of a window in a rendered cavity wall.',
    'q2-original': 'Original SEC 2025 Ordinary Construction Studies Question 2: the printed question with a sketch of a worker insulating a sloped ceiling from a scaffold.',
    'q3-original': 'Original SEC 2025 Ordinary Construction Studies Question 3: the printed question with a section of a two-storey house with a wood pellet stove, cylinder, radiators and tank.',
    'q4-original': 'Original SEC 2025 Ordinary Construction Studies Question 4: the printed question with a site location map showing sites A and B beside a road.',
    'q5-original': 'Original SEC 2025 Ordinary Construction Studies Question 5: the printed question with a sketch of a closed string wooden stairs meeting a landing.',
    'q6-original': 'Original SEC 2025 Ordinary Construction Studies Question 6: the printed question with a sketch of two workers installing solar panels on a roof.',
    'q7-original': 'Original SEC 2025 Ordinary Construction Studies Question 7: the printed question with the plan of a garden office with decking.',
    'q8-original': 'Original SEC 2025 Ordinary Construction Studies Question 8: the printed list of nine construction terms.',
    'q9-original': 'Original SEC 2025 Ordinary Construction Studies Question 9: the printed question with a sketch of the rear of a 1970s bungalow and its garden.',
    'q1-scheme': 'SEC 2025 Ordinary marking scheme page for Question 1: a section through the cavity wall and window head with lintels, stepped DPC and cavity closer, and the specification.',
    'q1-section': 'SEC model section through the window head marked (b), with the stepped DPC over the concrete lintels.',
    'q2-method': 'SEC 2025 Ordinary marking scheme notes on insulating a sloped ceiling, with a sketch of a worker fitting insulation between rafters, and the insulation types and thickness.',
    'q2-light': 'SEC model sketches of roof windows set in a sloped roof, with the list of daylight features.',
    'q3-system': 'SEC model diagram of the pellet stove heating and hot water system: tanks, cylinder, radiators, flow and return pipes, pump and valves, with typical details.',
    'q3-zoning': 'SEC 2025 Ordinary marking scheme notes on zoned heating, with a sketch of a zone controller.',
    'q4-sites': 'SEC 2025 Ordinary marking scheme considerations for sites A and B, each with a map extract.',
    'q4-site-a': 'SEC model sketch of site A with the house position, entrance and curved driveway, and the house-position notes.',
    'q5-section': 'SEC model section through the top three steps of a closed string stairs and the landing, with the 35° pitch and specification.',
    'q5-glue-blocks': 'SEC model detail of a step with an arrow to the glue block between tread and riser.',
    'q6-signs': 'SEC model blue safety signs for a high-visibility vest, safety boots and ear defenders, each with a reason.',
    'q6-risks': 'SEC 2025 Ordinary marking scheme notes on risks when working at height, with a sketch of a scaffold and ladder.',
    'q6-access': 'SEC 2025 Ordinary marking scheme notes on safe roof access, with a sketch of a worker in a safety harness.',
    'q7-office-plan': 'SEC model plan of the garden office showing a corner desk, two windows, a bookcase and a seating area beside the decking.',
    'q9-modifications': 'SEC model sketch of the bungalow rear with glazed doors opening onto a patio, and the list of modifications.',
    'q9-uses': 'SEC model sketch of raised garden planters, with the list of family uses of a garden.',
}
assert set(ALT) == {f['key'].removeprefix(validator.FP) for f in draft['questionFigures']}
for f in draft['questionFigures']:
    src = HERE / f"{f['key']}.png"
    md5 = hashlib.md5(src.read_bytes()).hexdigest()
    assert f['key'] not in manifest and md5 not in known_md5 and not (public / src.name).exists()
    known_md5.add(md5)

now = datetime.now(timezone.utc).isoformat()
save(HERE / 'prior-authored-card-hashes.json', dict(count=1070, algorithm='sha256 of json.dumps(card, ensure_ascii=False, sort_keys=True)',
     cards={c['id']: construction_corrections.card_hash(c) for c in prior}))
for f in draft['questionFigures']:
    dst = public / f"{f['key']}.png"
    shutil.copyfile(HERE / dst.name, dst)
    manifest[f['key']] = dict(src='/' + str(dst.relative_to(R / 'public')), md5=hashlib.md5(dst.read_bytes()).hexdigest(),
                              alt=ALT[f['key'].removeprefix(validator.FP)],
                              attribution='SEC Leaving Certificate Construction Studies 2025 Ordinary Level — © State Examinations Commission.',
                              solution=f['solution'])
save(manifest_path, manifest)

# Retire the build-time override that would replace the reviewed Q7(c) advantage rows.
text = corrections_path.read_text()
overrides = json.loads(text)
old = overrides['construction-studies'].pop('cons-2025-ol-q7-c-advantage')
assert not [k for k in overrides['construction-studies'] if k.startswith(validator.PREFIX)]
corrections_path.write_text(json.dumps(overrides, ensure_ascii=False, indent=2) + '\n')

review = dict(draft, status='2025 Ordinary main English theory Q1–Q9: 35 source-reviewed tasks (14 added, 21 pre-audit cards corrected in place under their original IDs; Q8 is one any-five card over all nine terms); whole theory paper reconciled against the original paper and scheme. Practical component and Irish edition remain separate work.',
              reviewedAt=now, paperComplete=True,
              fullPaperReconciliation=dict(questions=9, wholeQuestions=report['wholeQuestions'],
                                           examRubric='Any four of nine questions, 50 marks each, 200 total; no full-exam Cartesian cards.',
                                           method='Same-operator source review of paper pages 1–4 and scheme pages 2–25; validator construction_2025_ordinary.py.'),
              priorAuthoredCardHashes='docs/markbank-audit/2026-09-28/drafts/construction-2025-ordinary/prior-authored-card-hashes.json',
              priorCorrectedCards='docs/markbank-audit/2026-09-28/drafts/construction-2025-ordinary/prior-2025-ordinary-cards.json',
              retiredBuildOverrides=[dict(file='scripts/markbank/card-corrections.json', cardId='cons-2025-ol-q7-c-advantage',
                                          reason='The pre-audit override replaced the generic "Advantage" heading with an unprinted label and an any-one menu. The reviewed card carries the printed "Advantage" row (6) with the scheme’s examples, so the build-time override is retired rather than allowed to replace reviewed content.',
                                          retiredOverrideSha256=construction_corrections.card_hash(old))])
save(review_path, review)
merged = [corrected.get(c['id'], c) for c in prior] + added
save(authored_path, merged)
check = read(authored_path)
assert [c['id'] for c in check[:1070]] == [c['id'] for c in prior]
assert all(a == b for a, b in zip(check, prior) if a['id'] not in corrected) and check[1070:] == added
save(bridge_path, dict(schemaVersion=1, subjectId='construction-studies', year=2025, level='ordinary', lang='ev', sitting='main',
                       paperKey='single', reviewedAt=now, authoringReview=str(review_path.relative_to(R)), sourceHashes=draft['sourceHashes'],
                       expectedRuntimeCards=35,
                       reason='2025 Ordinary main English theory: all nine printed questions; 35 source-reviewed tasks (the Q8 choice is one any-five card), including the 21 pre-audit cards corrected in place. Practical/Irish/other papers remain open.',
                       questions=[dict(n=q, fileid='LC029GLP000EV.pdf',
                                       topicIds=sorted({t for b in draft['bindings'] if b['questionNumber'] == q for t in b['atlasTopicIds']}))
                                  for q in draft['questionsReviewed']],
                       cards=draft['bindings']))
added_ids = [c['id'] for c in added]
corrected_ids = [t['card']['id'] for t in tasks if t['correction']]
fixture.write_text(fixture.read_text()
                   + '\n// Original 2025 Ordinary Q1–Q9: ADDED tasks (Q8 is one any-five card, never a route per combination) and the pre-audit\n'
                   '// 2025 Ordinary cards CORRECTED in place under their original IDs.\n'
                   'export const CONSTRUCTION_2025_ORDINARY_ADDED_IDS = ' + json.dumps(added_ids, indent=2).replace('"', "'") + ';\n\n'
                   'export const CONSTRUCTION_2025_ORDINARY_CORRECTED_IDS = ' + json.dumps(corrected_ids, indent=2).replace('"', "'") + ';\n')
p = R / 'test/constructionStudiesExamTopics.test.ts'
s = p.read_text()
for old_s, new_s in [
    ("import { CONSTRUCTION_2025_HIGHER_ADDED_IDS } from './fixtures/construction2025Reviewed';",
     "import { CONSTRUCTION_2025_HIGHER_ADDED_IDS, CONSTRUCTION_2025_ORDINARY_ADDED_IDS } from './fixtures/construction2025Reviewed';"),
    ('    expect(CONSTRUCTION_ORDINARY).toHaveLength(250 + CONSTRUCTION_2015_ORDINARY_REVIEWED_IDS.length + CONSTRUCTION_2026_ORDINARY_REVIEWED_IDS.length);',
     '    expect(CONSTRUCTION_ORDINARY).toHaveLength(250 + CONSTRUCTION_2015_ORDINARY_REVIEWED_IDS.length + CONSTRUCTION_2026_ORDINARY_REVIEWED_IDS.length + CONSTRUCTION_2025_ORDINARY_ADDED_IDS.length);'),
    ('+ CONSTRUCTION_2026_ORDINARY_REVIEWED_IDS.length + CONSTRUCTION_2025_HIGHER_ADDED_IDS.length);',
     '+ CONSTRUCTION_2026_ORDINARY_REVIEWED_IDS.length + CONSTRUCTION_2025_HIGHER_ADDED_IDS.length + CONSTRUCTION_2025_ORDINARY_ADDED_IDS.length);'),
]:
    assert s.count(old_s) == 1, old_s
    s = s.replace(old_s, new_s)
p.write_text(s)
p = R / 'test/markBankCardPreservation.test.ts'
s = p.read_text()
for old_s, new_s in [
    ("import { CONSTRUCTION_2025_HIGHER_ADDED_IDS } from './fixtures/construction2025Reviewed';",
     "import { CONSTRUCTION_2025_HIGHER_ADDED_IDS, CONSTRUCTION_2025_ORDINARY_ADDED_IDS } from './fixtures/construction2025Reviewed';"),
    ('...CONSTRUCTION_2025_HIGHER_ADDED_IDS]);', '...CONSTRUCTION_2025_HIGHER_ADDED_IDS, ...CONSTRUCTION_2025_ORDINARY_ADDED_IDS]);'),
]:
    assert s.count(old_s) == 1, old_s
    s = s.replace(old_s, new_s)
p.write_text(s)
save(HERE / 'integration.json', dict(reviewedAt=now, addedTasks=14, correctedTasks=21, priorAuthoredCardsPreserved=1049, newAuthoredCount=1084,
                                     newFigures=25, wholeQuestions=report['wholeQuestions'], validator=report,
                                     status='Authored/bridge/test inputs applied; generation and runtime checks next.'))
print('Integrated 35 tasks (14 added, 21 corrected); authored deck input 1084 cards; 25 figures.')
