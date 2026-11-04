"""Integrate the validated 2024 Higher Q1-Q10 (and alternative Q10) draft into the Construction Studies runtime inputs.

NOT replay-safe: it refuses to run once the reviewed 2024 Higher file exists. Corrects the 22
pre-audit 2024 Higher cards in place (same IDs, hash-linked corrections), appends 23 new tasks (all
688 other prior cards byte-identical), installs 32 inspected figures with manifest entries, writes the
hosted paper anchor (copied from the tracked classic sidecar, each anchor checked against its printed
question marker), retires the stale build-time source binding for cons-2024-hl-q8-a, and writes the
reviewed file, the exact Atlas bridge and the test fixture/count updates. The 2024 Higher theory scheme
text already ships in examiner-reports/construction-studies/schemes/2024-hl.md and is left unchanged.
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
import construction_2024_higher as validator  # noqa: E402
import construction_corrections  # noqa: E402

import fitz  # noqa: E402


def read(p):
    return json.loads(Path(p).read_text())


def save(p, d):
    Path(p).write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n')


draft = read(HERE / 'higher-2024-draft.json')
report = validator.validate(draft, figure_dir=HERE, integrated=False)
review_path = R / 'scripts/markbank/authored/construction-studies-2024-higher-reviewed.json'
bridge_path = R / 'scripts/markbank/atlas-reviews/construction-studies-2024-higher.json'
authored_path = R / 'scripts/markbank/authored/construction-studies.json'
manifest_path = R / 'components/MarkBank/figures-construction-studies.json'
bindings_path = R / 'scripts/markbank/card-source-bindings.json'
fixture = R / 'test/fixtures/construction2024Reviewed.ts'
anchor_path = R / 'public/paper-anchors/2024/LC029ALP000EV.pdf.json'
public = R / 'public/exam-figures/construction-studies/markbank'
assert not review_path.exists() and not bridge_path.exists() and not anchor_path.exists()
assert (R / 'examiner-reports/construction-studies/schemes/2024-hl.md').exists()

prior = read(authored_path)
assert len(prior) == 710 and len({c['id'] for c in prior}) == 710
tasks = draft['tasks']
corrected = {t['card']['id']: t['card'] for t in tasks if t['correction']}
added = [t['card'] for t in tasks if not t['correction']]
assert len(corrected) == 22 and len(added) == 23
assert set(corrected) <= {c['id'] for c in prior} and not {c['id'] for c in added} & {c['id'] for c in prior}
assert not {c['questionRef'] for c in added} & {c['questionRef'] for c in prior if c['id'] not in corrected}
manifest = read(manifest_path)
known_md5 = {e['md5'] for e in manifest.values()}

ALT = {
    'q1-original': 'Original SEC 2024 Higher Construction Studies Question 1: the printed question with a sketch of an entrance porch with a slated lean-to roof and larch cladding.',
    'q1-section': 'SEC model vertical section through the lean-to porch roof: the clad cavity wall and eaves, insulated rafters and slates, and the abutment with the front wall of the house.',
    'q1-ventilation': 'SEC model eaves detail with arrows showing the ventilation path through the soffit and above the roof insulation, labelled “Ventilation”.',
    'q2-original': 'Original SEC 2024 Higher Construction Studies Question 2: the printed question with the draft plan of a bedroom and the en suite at A.',
    'q2-guidelines': 'SEC 2024 Higher marking scheme pages on lifetime-use kitchens and bedrooms, with sketches of accessible worktops, sockets, a wheelchair at a sink and a bedroom turning circle.',
    'q2-layouts': 'SEC model en suite layouts 1 and 2 for a person with limited mobility: door, level shower, W.C., wash basin and grab rails with turning circles.',
    'q2-justify': 'SEC 2024 Higher marking scheme page justifying the location of the en suite door, shower, W.C., wash basin and grab rails, with sketches.',
    'q3-original': 'Original SEC 2024 Higher Construction Studies Question 3: the printed question with the front elevation and plan of a house and the adjoining stone forge, walls A-A and B-B marked.',
    'q3-layout': 'SEC model revised layouts of the forge as an open-plan kitchen/dining and living space linked to the house, with the layout notes (two pages).',
    'q3-external': 'SEC model sketches of the renovated forge exterior in stone and corrugated metal with glazed gables and ridge glazing, with the external design notes (two pages).',
    'q4-original': 'Original SEC 2024 Higher Construction Studies Question 4: the printed question with the site location map showing sites A and B.',
    'q4-sites': 'SEC 2024 Higher marking scheme page on the considerations for site A and site B, with sketches of each site.',
    'q4-site-plans': 'SEC model site sketches for sites A and B showing the house orientation, outdoor living space, road entrance and driveway, with the notes.',
    'q5-original': 'Original SEC 2024 Higher Construction Studies Question 5: the printed question with a sketch of the ICF wall and all the construction and thermal data.',
    'q5-calculation': 'SEC worked solution: the U-value table giving a total resistance of 7.044 and U = 0.142 W/m²°C, and the annual heat-loss cost of €31.71 by two methods.',
    'q6-original': 'Original SEC 2024 Higher Construction Studies Question 6: the printed question with the elevation and ground-floor plan of an urban house.',
    'q6-low-impact': 'SEC 2024 Higher marking scheme page on low-environmental-impact features, with sketches of the timber frame, south glazing, solar gain and insulation.',
    'q6-features': 'SEC 2024 Higher marking scheme page on features that would increase energy efficiency: solar panels, a storm lobby, a sliding door, sun shading and larger south glazing, with sketches.',
    'q7-original': 'Original SEC 2024 Higher Construction Studies Question 7: the printed question with a sketch of the window, timber-frame wall and first-floor junction.',
    'q7-section': 'SEC model vertical section through the timber-frame wall with block outer leaf, the window head and the first floor, with the list of details.',
    'q7-airtightness': 'SEC model detail of the first-floor joist at the timber-frame inner leaf, with arrows to the airtightness barrier and taped junctions.',
    'q8-original': 'Original SEC 2024 Higher Construction Studies Question 8: the printed question with a sketch of a wood-burning stove.',
    'q8-system': 'SEC model single-line diagram of the stove supplying the hot-water cylinder and two zoned radiator circuits, with the typical pipe sizes.',
    'q8-renewables': 'SEC 2024 Higher marking scheme page on renewable hot water: a solar collector and photovoltaic panels with an immersion diverter, each with a sketch.',
    'q9-original': 'Original SEC 2024 Higher Construction Studies Question 9: the printed question with a sketch of an attic converted to a home office.',
    'q9-requirements': 'SEC 2024 Higher marking scheme page on the functional requirements of an attic home office, with sketches of roof windows, insulation, storage and furniture.',
    'q9-sound': 'SEC 2024 Higher marking scheme page on sound insulation of the attic floor and stud wall, with section sketches, and the start of the sound-insulation principles.',
    'q10-original': 'Original SEC 2024 Higher Construction Studies Question 10: the printed question with a sketch of a retrofitted bungalow.',
    'q10-items': 'SEC 2024 Higher marking scheme notes and sketches for all three Question 10(a) items: airtightness, windows and building fabric (two pages).',
    'q10-upgrade': 'SEC 2024 Higher marking scheme page on improving indoor air quality and space heating to the EnerPHit standard, with sketches of MVHR and a heat pump.',
    'q10-scheme': 'SEC marking-scheme notes and sketches for Question 10(a) and (b): airtightness, windows, building fabric, indoor air quality and space heating (three pages).',
    'q10-alt-original': 'Original SEC 2024 Higher Construction Studies alternative Question 10: the printed Irish Green Building Council quotation on buildings across their lifecycle and its two parts.',
}
assert set(ALT) == {f['key'].removeprefix(validator.FP) for f in draft['questionFigures']}
for f in draft['questionFigures']:
    src = HERE / f"{f['key']}.png"
    md5 = hashlib.md5(src.read_bytes()).hexdigest()
    assert f['key'] not in manifest and md5 not in known_md5 and not (public / src.name).exists()
    known_md5.add(md5)

# Hosted paper anchor: the tracked classic sidecar's question anchors, each checked against its printed marker.
sidecar = read(R / 'scripts/paper-trail/answers/2024/LC029ALP000EV.pdf.json')
with fitz.open(R / validator.P) as pdf:
    for q in sidecar['q']:
        page = pdf[q['pP'] - 1]
        h = page.rect.height
        lines = [(ln['bbox'][1] / h, ''.join(s['text'] for s in ln['spans']).strip())
                 for b in page.get_text('dict')['blocks'] for ln in b.get('lines', [])]
        hits = [y for y, text in lines if text.split()[0:1] == [f"{q['n']}."]]
        assert hits and abs(min(hits, key=lambda y: abs(y - q['pY'][0])) - q['pY'][0]) < 0.02, (q['n'], q['pY'], hits)
anchor = dict(band=[1, 1], component='000', copyright=sidecar['copyright'], paperFileid=sidecar['paperFileid'], paperOnly=1, schemeFileid='', v=1,
              q=[dict(conf=0.5, mode='pagejump', n=q['n'], pP=q['pP'], pY=q['pY'], region=[{'p': 1}]) for q in sidecar['q']])
assert [q['n'] for q in anchor['q']] == [str(i) for i in range(1, 11)] and sidecar['paperFileid'] == 'LC029ALP000EV.pdf'
anchor_path.write_text(json.dumps(anchor, ensure_ascii=False, sort_keys=True, separators=(',', ':')))

now = datetime.now(timezone.utc).isoformat()
save(HERE / 'prior-authored-card-hashes.json', dict(count=710, algorithm='sha256 of json.dumps(card, ensure_ascii=False, sort_keys=True)',
     cards={c['id']: construction_corrections.card_hash(c) for c in prior}))
for f in draft['questionFigures']:
    dst = public / f"{f['key']}.png"
    shutil.copyfile(HERE / dst.name, dst)
    manifest[f['key']] = dict(src='/' + str(dst.relative_to(R / 'public')), md5=hashlib.md5(dst.read_bytes()).hexdigest(),
                              alt=ALT[f['key'].removeprefix(validator.FP)], attribution='SEC Leaving Certificate Construction Studies 2024 Higher Level — © State Examinations Commission.',
                              solution=f['solution'])
save(manifest_path, manifest)

# Retire the stale build-time source binding: the reviewed card carries its own lifted text and source material.
source_bindings = read(bindings_path)
assert source_bindings['construction-studies'].pop('cons-2024-hl-q8-a') == {'pages': [6], 'stripStem': True}
save(bindings_path, source_bindings)

review = dict(draft, status='2024 Higher main English theory Q1–Q10 and the alternative Q10: 45 source-reviewed tasks (23 added, 22 pre-audit cards corrected in place under their original IDs); whole theory paper reconciled against the original paper and scheme; the printed choice Q10(a) is one card. Practical component and Irish edition remain separate work.',
              reviewedAt=now, paperComplete=True,
              fullPaperReconciliation=dict(questions=10, alternativeQuestions=1,
                                           examRubric='Any five of ten questions, 60 marks each, 300 total; no full-exam Cartesian cards.',
                                           method='Same-operator source review of paper pages 1–7 and scheme pages 2–46; validator construction_2024_higher.py.',
                                           validator=report),
              priorAuthoredCardHashes='docs/markbank-audit/2026-09-28/drafts/construction-2024-higher/prior-authored-card-hashes.json',
              priorCorrectedCards='docs/markbank-audit/2026-09-28/drafts/construction-2024-higher/prior-2024-higher-cards.json',
              retiredBuildOverrides=[dict(file='scripts/markbank/card-source-bindings.json', cardId='cons-2024-hl-q8-a',
                                          reason='The pre-audit binding attached page 6 as an official-page source and stripped the stem. The reviewed card carries its own lifted stem and Question 8 source material (pages 1 and 6), so the build-time override is retired rather than allowed to replace reviewed content.')])
save(review_path, review)
merged = [corrected.get(c['id'], c) for c in prior] + added
save(authored_path, merged)
check = read(authored_path)
assert [c['id'] for c in check[:710]] == [c['id'] for c in prior]
assert all(a == b for a, b in zip(check, prior) if a['id'] not in corrected) and check[710:] == added
save(bridge_path, dict(schemaVersion=1, subjectId='construction-studies', year=2024, level='higher', lang='ev', sitting='main',
                       paperKey='single', reviewedAt=now, authoringReview=str(review_path.relative_to(R)), sourceHashes=draft['sourceHashes'],
                       expectedRuntimeCards=45,
                       reason='2024 Higher main English theory: all ten printed questions and the alternative Question 10 (sharing the original Q10 anchor); 45 source-reviewed tasks, including the 22 pre-audit cards corrected in place; the printed choice Q10(a) is one card. Practical/Irish/other papers remain open.',
                       questions=[dict(n=q, fileid='LC029ALP000EV.pdf',
                                       topicIds=sorted({t for b in draft['bindings'] if b['questionNumber'] == q for t in b['atlasTopicIds']}))
                                  for q in draft['questionsReviewed']],
                       cards=draft['bindings']))
added_ids = [c['id'] for c in added]
corrected_ids = [t['card']['id'] for t in tasks if t['correction']]
fixture.write_text('// Original 2024 Higher Q1–Q10 and the alternative Q10. ADDED: every separately marked task and every complete\n'
                   '// question not previously carded; the printed choice Q10(a) is one card (choice is not a route).\n'
                   '// CORRECTED: the pre-audit 2024 Higher cards, kept under their original IDs and corrected in place.\n'
                   'export const CONSTRUCTION_2024_HIGHER_ADDED_IDS = ' + json.dumps(added_ids, indent=2).replace('"', "'") + ';\n\n'
                   'export const CONSTRUCTION_2024_HIGHER_CORRECTED_IDS = ' + json.dumps(corrected_ids, indent=2).replace('"', "'") + ';\n')
save(HERE / 'integration.json', dict(reviewedAt=now, addedTasks=23, correctedTasks=22, priorAuthoredCardsPreserved=688, newAuthoredCount=733,
                                     newFigures=32, validator=report, status='Authored/bridge/anchor/fixture inputs applied; test counts, generation and runtime checks next.'))
print('Integrated 45 tasks (23 added, 22 corrected); authored deck input 733 cards; 32 figures.')
