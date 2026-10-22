"""Integrate the validated 2023 Ordinary Q1-Q9 draft into the Construction Studies runtime inputs.

NOT replay-safe: it refuses to run once the reviewed 2023 Ordinary file exists. Corrects 19 pre-audit
2023 Ordinary cards in place (same IDs, hash-linked corrections), withdraws the other eight per-term Q8
cards into the surviving Q8 card through recorded progress aliases (choice is not a route), appends 11
new tasks (all other prior cards byte-identical), installs 30 inspected figures with manifest entries,
and writes the reviewed file, the exact Atlas bridge, the aliases and the test fixture.
The hosted paper anchor and the 2023 Ordinary theory scheme text already ship and are left unchanged.
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
import construction_2023_ordinary as validator  # noqa: E402
import construction_corrections  # noqa: E402


def read(p):
    return json.loads(Path(p).read_text())


def save(p, d):
    Path(p).write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n')


draft = read(HERE / 'ordinary-2023-draft.json')
report = validator.validate(draft, figure_dir=HERE, integrated=False)
review_path = R / 'scripts/markbank/authored/construction-studies-2023-ordinary-reviewed.json'
bridge_path = R / 'scripts/markbank/atlas-reviews/construction-studies-2023-ordinary.json'
authored_path = R / 'scripts/markbank/authored/construction-studies.json'
manifest_path = R / 'components/MarkBank/figures-construction-studies.json'
aliases_path = R / 'components/MarkBank/cardAliases.ts'
fixture = R / 'test/fixtures/construction2023Reviewed.ts'
public = R / 'public/exam-figures/construction-studies/markbank'
assert not review_path.exists() and not bridge_path.exists() and 'ORDINARY' not in fixture.read_text() and 'HIGHER' in fixture.read_text()
assert (R / 'examiner-reports/construction-studies/schemes/2023-ol.md').exists()
anchor = read(R / 'public/paper-anchors/2023/LC029GLP000EV.pdf.json')
assert anchor['paperOnly'] == 1 and [q['n'] for q in anchor['q']] == [str(i) for i in range(1, 10)]

prior = read(authored_path)
assert len(prior) == 759 and len({c['id'] for c in prior}) == 759
tasks = draft['tasks']
corrected = {t['card']['id']: t['card'] for t in tasks if t['correction']}
added = [t['card'] for t in tasks if not t['correction']]
withdrawn_ids = [m['cardId'] for m in draft['consolidatedLegacy']]
assert len(corrected) == 19 and len(added) == 11 and len(withdrawn_ids) == 8
assert set(corrected) | set(withdrawn_ids) == {c['id'] for c in prior if c['id'].startswith(validator.PREFIX)}
assert not {c['id'] for c in added} & {c['id'] for c in prior}
assert not {c['questionRef'] for c in [*added, *corrected.values()]} & {c['questionRef'] for c in prior if c['id'] not in corrected}
manifest = read(manifest_path)
known_md5 = {e['md5'] for e in manifest.values()}

ALT = {
    'q1-original': 'Original SEC 2023 Ordinary Construction Studies Question 1: the printed question with a sketch of a cavity wall supporting a timber first floor on joist hangers.',
    'q2-original': 'Original SEC 2023 Ordinary Construction Studies Question 2: the printed question with a sketch of an old two-storey stone house.',
    'q3-original': 'Original SEC 2023 Ordinary Construction Studies Question 3: the printed question with a sketch of a house with a solar collector on the roof.',
    'q4-original': 'Original SEC 2023 Ordinary Construction Studies Question 4: the printed question with a sketch of a roof of trussed rafters under construction.',
    'q5-original': 'Original SEC 2023 Ordinary Construction Studies Question 5: the printed question with a sketch of the eaves of a flat roof.',
    'q6-original': 'Original SEC 2023 Ordinary Construction Studies Question 6: the printed question with a sketch of a woodturning lathe.',
    'q7-original': 'Original SEC 2023 Ordinary Construction Studies Question 7: the printed question with the draft plan of a utility room with an external door, window and kitchen door.',
    'q8-original': 'Original SEC 2023 Ordinary Construction Studies Question 8: the printed list of nine construction terms.',
    'q9-original': 'Original SEC 2023 Ordinary Construction Studies Question 9: the printed question with a sketch of the front entrance of a semi-detached house.',
    'q1-scheme': 'SEC model section through the cavity wall and timber first floor on a joist hanger, with the wall tie marked (b) and the specification list.',
    'q2-reasons': 'SEC 2023 Ordinary marking scheme notes on why energy upgrade grants are available for old houses.',
    'q2-method': 'SEC 2023 Ordinary marking scheme notes on applying external insulation, with sketches of the insulation boards, mesh and render, and the insulation types and thickness.',
    'q2-upgrade': 'SEC 2023 Ordinary marking scheme notes on other energy upgrades, with sketches of a heat pump, solar panels on a roof and a wood-burning stove.',
    'q3-system': 'SEC model diagram of the solar collector connected to the cylinder, with the pump, expansion vessel, storage tank, shower and valves, and the typical details.',
    'q3-locations': 'SEC 2023 Ordinary marking scheme notes on considerations when locating solar panels on a house.',
    'q4-advantages': 'SEC 2023 Ordinary marking scheme notes on the advantages of trussed rafters.',
    'q4-fixing': 'SEC 2023 Ordinary marking scheme notes on securing a trussed rafter to the wall, with sketches of the wallplate, truss clip and nail plate.',
    'q4-finishes': 'SEC 2023 Ordinary marking scheme table of roof finishes (slate, tiles, photovoltaic slates and zinc sheeting) with reasons for each.',
    'q5-section': 'SEC model section through the cavity wall and the eaves of the insulated flat roof, with the specification list.',
    'q5-closer': 'SEC model detail of the cavity closer at wallplate level, marked (b).',
    'q6-classroom': 'SEC 2023 Ordinary marking scheme table of safety precautions when using a jigsaw and when using epoxy adhesive.',
    'q6-lathe': 'SEC 2023 Ordinary marking scheme notes on woodturning safety, with sketches of tied-back hair, a face visor, a dust mask and a lathe with its tool rest.',
    'q6-tidy': 'SEC 2023 Ordinary marking scheme notes on keeping the Construction Studies room organised and tidy.',
    'q7-advantages': 'SEC 2023 Ordinary marking scheme notes on the advantages of a large utility room.',
    'q7-layout': 'SEC model plan of the utility room with the sink under the window, the washing machine, storage units and seating/boot area, with the reasons for each location (two pages).',
    'q7-covering': 'SEC 2023 Ordinary marking scheme table of utility-room floor coverings (ceramic tiles, vinyl, polished concrete, wood laminate and linoleum) with reasons for each.',
    'q8-terms': 'SEC marking-scheme notes and sketches for all nine Question 8 terms, in scheme order: concrete mixer, smart radiator valve, ridge tile, triple glazing, balusters, cedar cladding, bridle joint, wood pellet stove and floor screed.',
    'q9-materials': 'SEC 2023 Ordinary marking scheme notes on front-door materials and reasons, with a sketch of a timber door under a canopy.',
    'q9-modifications': 'SEC 2023 Ordinary marking scheme notes on modifying the entrance for a person with limited mobility, with a sketch of an entrance opening in a brick wall.',
    'q9-reasons': 'SEC 2023 Ordinary marking scheme notes on why owners would create an entrance accessible to all, with a sketch of a ramped entrance.',
}
assert set(ALT) == {f['key'].removeprefix(validator.FP) for f in draft['questionFigures']}
for f in draft['questionFigures']:
    src = HERE / f"{f['key']}.png"
    md5 = hashlib.md5(src.read_bytes()).hexdigest()
    assert f['key'] not in manifest and md5 not in known_md5 and not (public / src.name).exists()
    known_md5.add(md5)

now = datetime.now(timezone.utc).isoformat()
prior_hashes = {c['id']: construction_corrections.card_hash(c) for c in prior}
save(HERE / 'prior-authored-card-hashes.json', dict(count=759, algorithm='sha256 of json.dumps(card, ensure_ascii=False, sort_keys=True)', cards=prior_hashes))
for f in draft['questionFigures']:
    dst = public / f"{f['key']}.png"
    shutil.copyfile(HERE / dst.name, dst)
    manifest[f['key']] = dict(src='/' + str(dst.relative_to(R / 'public')), md5=hashlib.md5(dst.read_bytes()).hexdigest(),
                              alt=ALT[f['key'].removeprefix(validator.FP)],
                              attribution='SEC Leaving Certificate Construction Studies 2023 Ordinary Level — © State Examinations Commission.',
                              solution=f['solution'])
save(manifest_path, manifest)

RULE = ('Choice is not a route (coordinator rule, 2026-10-12): a printed choose-N-of-M is ONE card that prints all M items '
        'with one anyN group over them, never a card per item or per combination.')
withdrawn = [dict(cardId=m['cardId'], priorSha256=prior_hashes[m['cardId']], reason=RULE, aliasOf=m['aliasOf']) for m in draft['consolidatedLegacy']]
text = aliases_path.read_text()
assert text.rstrip().endswith('};') and not any(f'"{w["cardId"]}"' in text for w in withdrawn)
block = ('  /* 2026-10-12. Construction Studies 2023 Ordinary Q8 is one any-five card (choice is not a route); the other eight\n'
         '   * pre-audit per-term cards are consolidated into it and their progress goes to it. */\n'
         + ''.join(f'  "{w["cardId"]}": "{w["aliasOf"]}",\n' for w in withdrawn))
aliases_path.write_text(text.rstrip()[:-2] + block + '};\n')

review = dict(draft, status='2023 Ordinary main English theory Q1–Q9: 30 source-reviewed tasks (11 added, 19 pre-audit cards corrected in place under their original IDs; Q8 is one any-five card over all nine terms, and the other eight pre-audit per-term cards alias to it); whole theory paper reconciled against the original paper and scheme. Practical component and Irish edition remain separate work.',
              reviewedAt=now, paperComplete=True, withdrawn=withdrawn,
              fullPaperReconciliation=dict(questions=9, wholeQuestions=report['wholeQuestions'],
                                           examRubric='Any four of nine questions, 50 marks each, 200 total; no full-exam Cartesian cards.',
                                           method='Same-operator source review of paper pages 1–4 and scheme pages 2–24; validator construction_2023_ordinary.py.',
                                           validator=report),
              priorAuthoredCardHashes='docs/markbank-audit/2026-09-28/drafts/construction-2023-ordinary/prior-authored-card-hashes.json',
              priorCorrectedCards='docs/markbank-audit/2026-09-28/drafts/construction-2023-ordinary/prior-2023-ordinary-cards.json')
save(review_path, review)
gone = set(withdrawn_ids)
merged = [corrected.get(c['id'], c) for c in prior if c['id'] not in gone] + added
save(authored_path, merged)
check = read(authored_path)
kept = [c['id'] for c in prior if c['id'] not in gone]
assert [c['id'] for c in check[:len(kept)]] == kept and check[len(kept):] == added and len(check) == 762
save(bridge_path, dict(schemaVersion=1, subjectId='construction-studies', year=2023, level='ordinary', lang='ev', sitting='main',
                       paperKey='single', reviewedAt=now, authoringReview=str(review_path.relative_to(R)), sourceHashes=draft['sourceHashes'],
                       expectedRuntimeCards=30,
                       reason='2023 Ordinary main English theory: all nine printed questions; 30 source-reviewed tasks (the Q8 choice is one any-five card), including the 19 pre-audit cards corrected in place. Practical/Irish/other papers remain open.',
                       questions=[dict(n=q, fileid='LC029GLP000EV.pdf',
                                       topicIds=sorted({t for b in draft['bindings'] if b['questionNumber'] == q for t in b['atlasTopicIds']}))
                                  for q in draft['questionsReviewed']],
                       cards=draft['bindings']))
added_ids = [c['id'] for c in added]
corrected_ids = [t['card']['id'] for t in tasks if t['correction']]
fixture.write_text(fixture.read_text()
                   + '\n// Original 2023 Ordinary Q1–Q9: ADDED tasks (Q8 is one any-five card, never a route per combination) and the pre-audit\n'
                   '// 2023 Ordinary cards CORRECTED in place under their original IDs.\n'
                   'export const CONSTRUCTION_2023_ORDINARY_ADDED_IDS = ' + json.dumps(added_ids, indent=2).replace('"', "'") + ';\n\n'
                   'export const CONSTRUCTION_2023_ORDINARY_CORRECTED_IDS = ' + json.dumps(corrected_ids, indent=2).replace('"', "'") + ';\n')
save(HERE / 'integration.json', dict(reviewedAt=now, addedTasks=11, correctedTasks=19, withdrawnIntoAlias=8, newAuthoredCount=762,
                                     newFigures=30, validator=report, status='Authored/bridge/alias/fixture inputs applied; test counts, generation and runtime checks next.'))
print('Integrated 30 tasks (11 added, 19 corrected, 8 aliased); authored deck input 762 cards; 30 figures.')
