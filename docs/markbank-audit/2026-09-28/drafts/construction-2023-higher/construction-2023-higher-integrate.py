"""Integrate the validated 2023 Higher Q1-Q10 (and alternative Q10) draft into the Construction Studies runtime inputs.

NOT replay-safe: it refuses to run once the reviewed 2023 Higher file exists. Corrects the 29
pre-audit 2023 Higher cards in place (same IDs, hash-linked corrections), appends 21 new tasks (all
709 other prior cards byte-identical), installs 33 inspected figures with manifest entries, writes the
hosted paper anchor (copied from the tracked classic sidecar, each anchor checked against its printed
question marker), and writes the reviewed file, the exact Atlas bridge and the test fixture. The 2023
Higher theory scheme text already ships in examiner-reports/construction-studies/schemes/2023-hl.md and
is left unchanged. No build-time override names a 2023 Higher card.
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
import construction_2023_higher as validator  # noqa: E402
import construction_corrections  # noqa: E402

import fitz  # noqa: E402


def read(p):
    return json.loads(Path(p).read_text())


def save(p, d):
    Path(p).write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n')


draft = read(HERE / 'higher-2023-draft.json')
report = validator.validate(draft, figure_dir=HERE, integrated=False)
review_path = R / 'scripts/markbank/authored/construction-studies-2023-higher-reviewed.json'
bridge_path = R / 'scripts/markbank/atlas-reviews/construction-studies-2023-higher.json'
authored_path = R / 'scripts/markbank/authored/construction-studies.json'
manifest_path = R / 'components/MarkBank/figures-construction-studies.json'
fixture = R / 'test/fixtures/construction2023Reviewed.ts'
anchor_path = R / 'public/paper-anchors/2023/LC029ALP000EV.pdf.json'
public = R / 'public/exam-figures/construction-studies/markbank'
assert not review_path.exists() and not bridge_path.exists() and not anchor_path.exists() and not fixture.exists()
assert (R / 'examiner-reports/construction-studies/schemes/2023-hl.md').exists()
for name in ['card-source-bindings.json', 'card-corrections.json']:
    assert not [k for k in read(R / 'scripts/markbank' / name).get('construction-studies', {}) if k.startswith(validator.PREFIX)], name

prior = read(authored_path)
assert len(prior) == 738 and len({c['id'] for c in prior}) == 738
tasks = draft['tasks']
corrected = {t['card']['id']: t['card'] for t in tasks if t['correction']}
added = [t['card'] for t in tasks if not t['correction']]
assert len(corrected) == 29 and len(added) == 21
assert set(corrected) <= {c['id'] for c in prior} and not {c['id'] for c in added} & {c['id'] for c in prior}
assert not {c['questionRef'] for c in added} & {c['questionRef'] for c in prior if c['id'] not in corrected}
manifest = read(manifest_path)
known_md5 = {e['md5'] for e in manifest.values()}

ALT = {
    'q1-original': 'Original SEC 2023 Higher Construction Studies Question 1: the printed question with a sketch of a house with a tiled trussed-rafter roof.',
    'q1-section': 'SEC model vertical section through half of the trussed roof from the timber-frame wall and eaves to the ridge, with insulation at ceiling level.',
    'q1-ventilation': 'SEC model eaves detail with arrows showing air entering through the soffit and passing over the insulation into the roof space, labelled “(b) Ventilation”.',
    'q2-original': 'Original SEC 2023 Higher Construction Studies Question 2: the printed question with an illustration of workers in hard hats and high-visibility vests on a site.',
    'q2-site-access': 'SEC 2023 Higher marking scheme page on site access guidelines, with sketches of a keypad, signage, hoarding, a site entrance with access control and a worker at a turnstile.',
    'q2-ladder': 'SEC 2023 Higher marking scheme page on using a ladder safely, with sketches of a worker on a ladder, a ladder at a scaffold and a ladder secured at its base.',
    'q2-guidelines': 'SEC 2023 Higher marking scheme guidelines for site access and for using a ladder, with their sketches (two pages).',
    'q3-original': 'Original SEC 2023 Higher Construction Studies Question 3: the printed question with the elevation and first-floor plan of a coastal two-storey house, walls A-A and B-B marked.',
    'q3-considerations': 'SEC 2023 Higher marking scheme notes on design considerations for a first-floor kitchen/dining and living area, with a sketch of the kitchen work triangle (two pages).',
    'q3-layout': 'SEC model revised first-floor layouts with the kitchen/dining and living area, two bedrooms and the stairs, with the layout notes (two pages).',
    'q4-original': 'Original SEC 2023 Higher Construction Studies Question 4: the printed question with a sketch of a vernacular Irish homestead.',
    'q4-features': 'SEC 2023 Higher marking scheme notes on vernacular features, with sketches of the plan, a half-door, rubble stonework, a chimney and a sash window (two pages).',
    'q4-refurbishment': 'SEC 2023 Higher marking scheme notes on choice of materials, craft skills and respect for local character in refurbishing a vernacular cottage, with a sketch of slate verges (two pages).',
    'q4-scheme': 'SEC marking-scheme notes and sketches for Question 4(a) and (b): vernacular features, choice of materials, craft skills and respect for local character (three pages).',
    'q5-original': 'Original SEC 2023 Higher Construction Studies Question 5: the printed question with a sketch of the flat roof and all the construction and thermal data.',
    'q5-calculation': 'SEC worked solution: the U-value table giving a total resistance of 9.647 and U = 0.104 W/m²°C, and the annual heat-loss cost of €12.53 by two methods.',
    'q5-thermal-bridge': 'SEC model detail of the junction of the flat roof and the full-fill cavity wall, showing thermal blocks and continuous insulation.',
    'q6-original': 'Original SEC 2023 Higher Construction Studies Question 6: the printed question with the elevation and ground-floor plan of a low-impact house.',
    'q6-low-impact': 'SEC 2023 Higher marking scheme notes on low-environmental-impact features, with sketches of timber framing, south glazing, the plan, roof lights and solar gain (two pages).',
    'q6-technologies': 'SEC 2023 Higher marking scheme notes on photovoltaic panels, an air-to-water heat pump and evacuated tubes, each with a system sketch (two pages).',
    'q7-original': 'Original SEC 2023 Higher Construction Studies Question 7: the printed question with a sketch of a sheeted external door in a rendered wall.',
    'q7-section': 'SEC model vertical section through the external door, the cavity wall and lintels, and the insulated ground floor at the threshold.',
    'q7-threshold': 'SEC model threshold detail with arrows marked B to the drainage channel, sloped cill and upstand that keep moisture out.',
    'q8-original': 'Original SEC 2023 Higher Construction Studies Question 8: the printed question with a sketch of a wastewater treatment system being installed beside a house.',
    'q8-system': 'SEC model layout of a wastewater treatment system, distribution box and percolation trenches with typical dimensions, and a section of a percolation trench (two pages).',
    'q9-original': 'Original SEC 2023 Higher Construction Studies Question 9: the printed question with a sketch of a living room with a large window.',
    'q9-requirements': 'SEC 2023 Higher marking scheme notes on the functional requirements of modern glazing, with sketches of triple glazing, smart glass and an escape window (two pages).',
    'q9-calculation': 'SEC worked solution by the degree of efficiency method: floor area 18.9 m² and a window area of 9.45 m².',
    'q10-original': 'Original SEC 2023 Higher Construction Studies Question 10: the printed question with the draft ground-floor plan of a new house.',
    'q10-features': 'SEC 2023 Higher marking scheme notes and sketches for all three Question 10(a) items: foundation design, solar shading and a thermally efficient building envelope (three pages).',
    'q10-mvhr': 'SEC model MVHR layout on the given ground-floor plan, showing the unit, supply and extract ducts and airflow, with notes on how the system works.',
    'q10-scheme': 'SEC marking-scheme notes and sketches for Question 10(a) and (b): foundation design, solar shading, the building envelope and the MVHR layout (three pages).',
    'q10-alt-original': 'Original SEC 2023 Higher Construction Studies alternative Question 10: the printed National Disability Authority quotation on Universal Design for homes and its two parts.',
}
assert set(ALT) == {f['key'].removeprefix(validator.FP) for f in draft['questionFigures']}
for f in draft['questionFigures']:
    src = HERE / f"{f['key']}.png"
    md5 = hashlib.md5(src.read_bytes()).hexdigest()
    assert f['key'] not in manifest and md5 not in known_md5 and not (public / src.name).exists()
    known_md5.add(md5)

# Hosted paper anchor: the tracked classic sidecar's question anchors, each checked against its printed marker.
sidecar = read(R / 'scripts/paper-trail/answers/2023/LC029ALP000EV.pdf.json')
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
save(HERE / 'prior-authored-card-hashes.json', dict(count=738, algorithm='sha256 of json.dumps(card, ensure_ascii=False, sort_keys=True)',
     cards={c['id']: construction_corrections.card_hash(c) for c in prior}))
for f in draft['questionFigures']:
    dst = public / f"{f['key']}.png"
    shutil.copyfile(HERE / dst.name, dst)
    manifest[f['key']] = dict(src='/' + str(dst.relative_to(R / 'public')), md5=hashlib.md5(dst.read_bytes()).hexdigest(),
                              alt=ALT[f['key'].removeprefix(validator.FP)], attribution='SEC Leaving Certificate Construction Studies 2023 Higher Level — © State Examinations Commission.',
                              solution=f['solution'])
save(manifest_path, manifest)

review = dict(draft, status='2023 Higher main English theory Q1–Q10 and the alternative Q10: 50 source-reviewed tasks (21 added, 29 pre-audit cards corrected in place under their original IDs); whole theory paper reconciled against the original paper and scheme; the printed choices Q4(b) and Q10(a) are one card each. Practical component and Irish edition remain separate work.',
              reviewedAt=now, paperComplete=True,
              fullPaperReconciliation=dict(questions=10, alternativeQuestions=1,
                                           examRubric='Any five of ten questions, 60 marks each, 300 total; no full-exam Cartesian cards.',
                                           method='Same-operator source review of paper pages 1–7 and scheme pages 2–43; validator construction_2023_higher.py.',
                                           validator=report),
              priorAuthoredCardHashes='docs/markbank-audit/2026-09-28/drafts/construction-2023-higher/prior-authored-card-hashes.json',
              priorCorrectedCards='docs/markbank-audit/2026-09-28/drafts/construction-2023-higher/prior-2023-higher-cards.json')
save(review_path, review)
merged = [corrected.get(c['id'], c) for c in prior] + added
save(authored_path, merged)
check = read(authored_path)
assert [c['id'] for c in check[:738]] == [c['id'] for c in prior]
assert all(a == b for a, b in zip(check, prior) if a['id'] not in corrected) and check[738:] == added
save(bridge_path, dict(schemaVersion=1, subjectId='construction-studies', year=2023, level='higher', lang='ev', sitting='main',
                       paperKey='single', reviewedAt=now, authoringReview=str(review_path.relative_to(R)), sourceHashes=draft['sourceHashes'],
                       expectedRuntimeCards=50,
                       reason='2023 Higher main English theory: all ten printed questions and the alternative Question 10 (sharing the original Q10 anchor); 50 source-reviewed tasks, including the 29 pre-audit cards corrected in place; the printed choices Q4(b) and Q10(a) are one card each. Practical/Irish/other papers remain open.',
                       questions=[dict(n=q, fileid='LC029ALP000EV.pdf',
                                       topicIds=sorted({t for b in draft['bindings'] if b['questionNumber'] == q for t in b['atlasTopicIds']}))
                                  for q in draft['questionsReviewed']],
                       cards=draft['bindings']))
added_ids = [c['id'] for c in added]
corrected_ids = [t['card']['id'] for t in tasks if t['correction']]
fixture.write_text('// Original 2023 Higher Q1–Q10 and the alternative Q10. ADDED: every separately marked task and every complete\n'
                   '// question not previously carded; the printed choices Q4(b) and Q10(a) are one card each (choice is not a route).\n'
                   '// CORRECTED: the pre-audit 2023 Higher cards, kept under their original IDs and corrected in place.\n'
                   'export const CONSTRUCTION_2023_HIGHER_ADDED_IDS = ' + json.dumps(added_ids, indent=2).replace('"', "'") + ';\n\n'
                   'export const CONSTRUCTION_2023_HIGHER_CORRECTED_IDS = ' + json.dumps(corrected_ids, indent=2).replace('"', "'") + ';\n')
save(HERE / 'integration.json', dict(reviewedAt=now, addedTasks=21, correctedTasks=29, priorAuthoredCardsPreserved=709, newAuthoredCount=759,
                                     newFigures=33, validator=report, status='Authored/bridge/anchor/fixture inputs applied; test counts, generation and runtime checks next.'))
print('Integrated 50 tasks (21 added, 29 corrected); authored deck input 759 cards; 33 figures.')
