"""Integrate the validated 2024 Ordinary Q1-Q9 draft into the Construction Studies runtime inputs.

NOT replay-safe: it refuses to run once the reviewed 2024 Ordinary file exists. Corrects 17 pre-audit
2024 Ordinary cards in place (same IDs, hash-linked corrections), withdraws the other eight per-term Q8
cards into the surviving Q8 card through recorded progress aliases (choice is not a route), appends 13
new tasks (all other prior cards byte-identical), installs 26 inspected figures with manifest entries,
and writes the reviewed file, the exact Atlas bridge, the aliases and the test fixture/count updates.
The hosted paper anchor and the 2024 Ordinary theory scheme text already ship and are left unchanged.
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
import construction_2024_ordinary as validator  # noqa: E402
import construction_corrections  # noqa: E402


def read(p):
    return json.loads(Path(p).read_text())


def save(p, d):
    Path(p).write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n')


draft = read(HERE / 'ordinary-2024-draft.json')
report = validator.validate(draft, figure_dir=HERE, integrated=False)
review_path = R / 'scripts/markbank/authored/construction-studies-2024-ordinary-reviewed.json'
bridge_path = R / 'scripts/markbank/atlas-reviews/construction-studies-2024-ordinary.json'
authored_path = R / 'scripts/markbank/authored/construction-studies.json'
manifest_path = R / 'components/MarkBank/figures-construction-studies.json'
aliases_path = R / 'components/MarkBank/cardAliases.ts'
fixture = R / 'test/fixtures/construction2024Reviewed.ts'
public = R / 'public/exam-figures/construction-studies/markbank'
assert not review_path.exists() and not bridge_path.exists() and 'ORDINARY' not in fixture.read_text()
assert (R / 'examiner-reports/construction-studies/schemes/2024-ol.md').exists()
anchor = read(R / 'public/paper-anchors/2024/LC029GLP000EV.pdf.json')
assert anchor['paperOnly'] == 1 and [q['n'] for q in anchor['q']] == [str(i) for i in range(1, 10)]

prior = read(authored_path)
assert len(prior) == 733 and len({c['id'] for c in prior}) == 733
tasks = draft['tasks']
corrected = {t['card']['id']: t['card'] for t in tasks if t['correction']}
added = [t['card'] for t in tasks if not t['correction']]
withdrawn_ids = [m['cardId'] for m in draft['consolidatedLegacy']]
assert len(corrected) == 17 and len(added) == 13 and len(withdrawn_ids) == 8
assert set(corrected) | set(withdrawn_ids) == {c['id'] for c in prior if c['id'].startswith(validator.PREFIX)}
assert not {c['id'] for c in added} & {c['id'] for c in prior}
assert not {c['questionRef'] for c in [*added, *corrected.values()]} & {c['questionRef'] for c in prior if c['id'] not in corrected}
manifest = read(manifest_path)
known_md5 = {e['md5'] for e in manifest.values()}

ALT = {
    'q1-original': 'Original SEC 2024 Ordinary Construction Studies Question 1: the printed question with a sketch of the slated eaves of a trussed roof on a cavity wall.',
    'q2-original': 'Original SEC 2024 Ordinary Construction Studies Question 2: the printed question with a sketch of a worker fixing insulated plasterboard to a wall.',
    'q3-original': 'Original SEC 2024 Ordinary Construction Studies Question 3: the printed question with a sketch of an accessible bathroom with a level shower area.',
    'q4-original': 'Original SEC 2024 Ordinary Construction Studies Question 4: the printed question with a sketch of a stone-faced entrance wall and driveway under construction.',
    'q5-original': 'Original SEC 2024 Ordinary Construction Studies Question 5: the printed question with a sketch of a triple-glazed window and concrete cill in a rendered wall.',
    'q6-original': 'Original SEC 2024 Ordinary Construction Studies Question 6: the printed question with a sketch of a site dumper in operation.',
    'q7-original': 'Original SEC 2024 Ordinary Construction Studies Question 7: the printed question with the draft plan of an attic bedroom with stairs and an en suite.',
    'q8-original': 'Original SEC 2024 Ordinary Construction Studies Question 8: the printed list of nine construction terms.',
    'q9-original': 'Original SEC 2024 Ordinary Construction Studies Question 9: the printed question with a sketch of a zinc-clad family room at the rear of a semi-detached house.',
    'q1-scheme': 'SEC model section through the trussed-roof eaves and cavity wall, with the wallplate strap marked (b) and the specification list.',
    'q2-advantages': 'SEC 2024 Ordinary marking scheme notes on the advantages of improving a BER, with a BER scale graphic.',
    'q2-method': 'SEC 2024 Ordinary marking scheme notes on insulating the inside of an external wall, with sketches of insulated plasterboard and battens, and the insulation types and thickness.',
    'q2-reasons': 'SEC 2024 Ordinary marking scheme notes on upgrading walls and windows together, with a sketch of a window in an insulated wall.',
    'q3-system': 'SEC model single-line diagram of the bathroom hot and cold supply: rising main, insulated tank, cylinder, shower, basin and cistern, with typical sizes.',
    'q3-features': 'SEC 2024 Ordinary marking scheme notes on an accessible shower area, with sketches of a level shower and lever controls.',
    'q4-stone': 'SEC 2024 Ordinary marking scheme notes on a natural stone finish, with a sketch of a mason laying stone.',
    'q4-foundation': 'SEC model sketch of a reinforced strip foundation under a wall, with the design notes and dimensions.',
    'q5-section': 'SEC model section through the cavity wall and the bottom of the window with the concrete cill, with the specification list.',
    'q5-drip': 'SEC model detail of the window cill marked (b), showing the DPC and drip.',
    'q6-precautions': 'SEC 2024 Ordinary marking scheme notes on site dumper safety, with a sketch of a site dumper.',
    'q6-ppe': 'SEC model PPE signs for a hard hat, high-visibility vest, ear defenders, safety glasses and safety boots, each with a reason.',
    'q6-training': 'SEC 2024 Ordinary marking scheme notes on operator training, with a sketch of a certification card.',
    'q7-layout': 'SEC model plan of the attic bedroom showing the en suite access, double bed, clothes storage and study space.',
    'q8-terms': 'SEC marking-scheme notes and sketches for all nine Question 8 terms, in scheme order: gulley trap, smart lighting, site planning notice, halving joint, cordless drill, cavity closer, faceplate turning, plywood and heat pump.',
    'q9-zinc': 'SEC 2024 Ordinary marking scheme notes on zinc cladding, with a sketch of a zinc-clad wall.',
    'q9-modifications': 'SEC model sketches of the family room with roof lights and large glazed doors to the garden, and the list of modifications.',
}
assert set(ALT) == {f['key'].removeprefix(validator.FP) for f in draft['questionFigures']}
for f in draft['questionFigures']:
    src = HERE / f"{f['key']}.png"
    md5 = hashlib.md5(src.read_bytes()).hexdigest()
    assert f['key'] not in manifest and md5 not in known_md5 and not (public / src.name).exists()
    known_md5.add(md5)

now = datetime.now(timezone.utc).isoformat()
prior_hashes = {c['id']: construction_corrections.card_hash(c) for c in prior}
save(HERE / 'prior-authored-card-hashes.json', dict(count=733, algorithm='sha256 of json.dumps(card, ensure_ascii=False, sort_keys=True)', cards=prior_hashes))
for f in draft['questionFigures']:
    dst = public / f"{f['key']}.png"
    shutil.copyfile(HERE / dst.name, dst)
    manifest[f['key']] = dict(src='/' + str(dst.relative_to(R / 'public')), md5=hashlib.md5(dst.read_bytes()).hexdigest(),
                              alt=ALT[f['key'].removeprefix(validator.FP)],
                              attribution='SEC Leaving Certificate Construction Studies 2024 Ordinary Level — © State Examinations Commission.',
                              solution=f['solution'])
save(manifest_path, manifest)

RULE = ('Choice is not a route (coordinator rule, 2026-10-12): a printed choose-N-of-M is ONE card that prints all M items '
        'with one anyN group over them, never a card per item or per combination.')
withdrawn = [dict(cardId=m['cardId'], priorSha256=prior_hashes[m['cardId']], reason=RULE, aliasOf=m['aliasOf']) for m in draft['consolidatedLegacy']]
text = aliases_path.read_text()
assert text.rstrip().endswith('};') and not any(f'"{w["cardId"]}"' in text for w in withdrawn)
block = ('  /* 2026-10-12. Construction Studies 2024 Ordinary Q8 is one any-five card (choice is not a route); the other eight\n'
         '   * pre-audit per-term cards are consolidated into it and their progress goes to it. */\n'
         + ''.join(f'  "{w["cardId"]}": "{w["aliasOf"]}",\n' for w in withdrawn))
aliases_path.write_text(text.rstrip()[:-2] + block + '};\n')

review = dict(draft, status='2024 Ordinary main English theory Q1–Q9: 30 source-reviewed tasks (13 added, 17 pre-audit cards corrected in place under their original IDs; Q8 is one any-five card over all nine terms, and the other eight pre-audit per-term cards alias to it); whole theory paper reconciled against the original paper and scheme. Practical component and Irish edition remain separate work.',
              reviewedAt=now, paperComplete=True, withdrawn=withdrawn,
              fullPaperReconciliation=dict(questions=9, wholeQuestions=report['wholeQuestions'],
                                           examRubric='Any four of nine questions, 50 marks each, 200 total; no full-exam Cartesian cards.',
                                           method='Same-operator source review of paper pages 1–4 and scheme pages 2–24; validator construction_2024_ordinary.py.',
                                           validator=report),
              priorAuthoredCardHashes='docs/markbank-audit/2026-09-28/drafts/construction-2024-ordinary/prior-authored-card-hashes.json',
              priorCorrectedCards='docs/markbank-audit/2026-09-28/drafts/construction-2024-ordinary/prior-2024-ordinary-cards.json')
save(review_path, review)
gone = set(withdrawn_ids)
merged = [corrected.get(c['id'], c) for c in prior if c['id'] not in gone] + added
save(authored_path, merged)
check = read(authored_path)
kept = [c['id'] for c in prior if c['id'] not in gone]
assert [c['id'] for c in check[:len(kept)]] == kept and check[len(kept):] == added and len(check) == 738
save(bridge_path, dict(schemaVersion=1, subjectId='construction-studies', year=2024, level='ordinary', lang='ev', sitting='main',
                       paperKey='single', reviewedAt=now, authoringReview=str(review_path.relative_to(R)), sourceHashes=draft['sourceHashes'],
                       expectedRuntimeCards=30,
                       reason='2024 Ordinary main English theory: all nine printed questions; 30 source-reviewed tasks (the Q8 choice is one any-five card), including the 17 pre-audit cards corrected in place. Practical/Irish/other papers remain open.',
                       questions=[dict(n=q, fileid='LC029GLP000EV.pdf',
                                       topicIds=sorted({t for b in draft['bindings'] if b['questionNumber'] == q for t in b['atlasTopicIds']}))
                                  for q in draft['questionsReviewed']],
                       cards=draft['bindings']))
added_ids = [c['id'] for c in added]
corrected_ids = [t['card']['id'] for t in tasks if t['correction']]
fixture.write_text(fixture.read_text()
                   + '\n// Original 2024 Ordinary Q1–Q9: ADDED tasks (Q8 is one any-five card, never a route per combination) and the pre-audit\n'
                   '// 2024 Ordinary cards CORRECTED in place under their original IDs.\n'
                   'export const CONSTRUCTION_2024_ORDINARY_ADDED_IDS = ' + json.dumps(added_ids, indent=2).replace('"', "'") + ';\n\n'
                   'export const CONSTRUCTION_2024_ORDINARY_CORRECTED_IDS = ' + json.dumps(corrected_ids, indent=2).replace('"', "'") + ';\n')
save(HERE / 'integration.json', dict(reviewedAt=now, addedTasks=13, correctedTasks=17, withdrawnIntoAlias=8, newAuthoredCount=738,
                                     newFigures=26, validator=report, status='Authored/bridge/alias/fixture inputs applied; test counts, generation and runtime checks next.'))
print('Integrated 30 tasks (13 added, 17 corrected, 8 aliased); authored deck input 738 cards; 26 figures.')
