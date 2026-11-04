"""Integrate the validated 2015 Ordinary Q1-Q9 draft into the Construction Studies runtime inputs.

NOT replay-safe: it refuses to run once the reviewed Ordinary file exists. It appends
176 cards to the authored deck input (all 607 prior cards byte-identical), installs 35
inspected figures and manifest entries, writes the reviewed file, the exact Atlas bridge,
the 2015 Ordinary theory scheme text and the test fixture/count updates.
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
import construction_2015_ordinary as validator  # noqa: E402

import fitz  # noqa: E402


def read(p):
    return json.loads(Path(p).read_text())


def save(p, d):
    Path(p).write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n')


draft = read(HERE / 'ordinary-draft.json')
report = validator.validate(draft, figure_dir=HERE, integrated=False)
review_path = R / 'scripts/markbank/authored/construction-studies-2015-ordinary-reviewed.json'
bridge_path = R / 'scripts/markbank/atlas-reviews/construction-studies-2015-ordinary.json'
scheme_md = R / 'examiner-reports/construction-studies/schemes/2015-ol.md'
authored_path = R / 'scripts/markbank/authored/construction-studies.json'
manifest_path = R / 'components/MarkBank/figures-construction-studies.json'
public = R / 'public/exam-figures/construction-studies/markbank'
assert not review_path.exists() and not bridge_path.exists() and not scheme_md.exists()

prior = read(authored_path)
assert len(prior) == 607 and len({c['id'] for c in prior}) == 607
new_cards = [t['card'] for t in draft['tasks']]
assert not {c['id'] for c in new_cards} & {c['id'] for c in prior}
assert not {c['questionRef'] for c in new_cards} & {c['questionRef'] for c in prior}
manifest = read(manifest_path)
assert len(manifest) == 35
known_md5 = {e['md5'] for e in manifest.values()}

ALT = {
    'q1-original': 'Original SEC 2015 Ordinary Construction Studies Question 1: the printed question with a sketch of a house with a tiled front porch.',
    'q1-roof-section': 'SEC model section through one half of the insulated porch roof, from below the wallplate through the cavity wall and eaves to the ridge, with the typical specification list and the stainless-steel strap securing the wallplate.',
    'q2-original': 'Original SEC 2015 Ordinary Construction Studies Question 2: the printed question with a sketch of a single-storey house built over 40 years ago.',
    'q2-cavity-fill': 'SEC model sketches of cavity-fill insulation: a drill entering the outer leaf of a cavity wall, and the wall face with injection holes spaced 800 mm horizontally and 1350 mm vertically.',
    'q2-external-insulation': 'SEC model sketch of an external insulation system on a cavity wall, showing the wall, adhesive, insulation board and a mechanical fixing labelled A to D.',
    'q2-insulated-wall': 'SEC model sketch of insulation being pumped into a wall cavity through a hose, with arrows showing heat kept in by the insulated wall.',
    'q2-scheme': 'SEC 2015 Ordinary marking scheme page for Question 2: typical steps and sketches for filling the cavity and adding external insulation, and advantages of insulating the house.',
    'q3-original': 'Original SEC 2015 Ordinary Construction Studies Question 3: the printed question with a sketch of a bathroom with a shower and toilet.',
    'q3-system': 'SEC model single-line diagram: attic storage tank with overflow, rising main, valves, cold feed to the hot water cylinder, expansion pipe, hot and cold supplies to the mixer-shower and cold supply to the toilet cistern, with insulation shown.',
    'q3-scheme': 'SEC 2015 Ordinary marking scheme page for Question 3: typical pipework specifications and diagram, and sketched water-saving methods for the shower, wash hand basin, toilet and bath.',
    'q4-original': 'Original SEC 2015 Ordinary Construction Studies Question 4: the printed question with the site map showing site A, house B, roadway C-C and the north point.',
    'q4-site-plans': 'Two SEC model site plans showing a curved driveway from a splayed entrance at roadway C-C to house B, the septic tank and percolation area, and trees planted along the boundaries.',
    'q5-original': 'Original SEC 2015 Ordinary Construction Studies Question 5: the printed question with a cut-away sketch of a strip foundation, timber-frame external wall and insulated ground floor.',
    'q5-section': 'SEC 2015 Ordinary marking scheme page for Question 5: model section through the strip foundation, timber-frame wall and insulated concrete floor, with typical construction details and the insulation positions.',
    'q6-original': 'Original SEC 2015 Ordinary Construction Studies Question 6: the printed question with a sketch of site hoarding displaying safety signs.',
    'q6-hand-sign': 'SEC model blue circular mandatory sign with white gloves, labelled Hand protection.',
    'q6-ear-sign': 'SEC model blue circular mandatory sign with a head wearing ear defenders, labelled Ear protection.',
    'q6-eye-sign': 'SEC model blue circular mandatory sign with a face wearing safety goggles, labelled Eye protection.',
    'q6-signs': 'The three SEC model mandatory safety signs for hand protection, ear protection and eye protection.',
    'q7-original': 'Original SEC 2015 Ordinary Construction Studies Question 7: the printed question with a sketch of a water butt beside a house under a pitched roof.',
    'q7-water-butt': 'SEC model sketch of a water butt on a stand beside a house, fed from the downpipe through a diverter and hose, with the eaves gutter above.',
    'q8-original': 'Original SEC 2015 Ordinary Construction Studies Question 8: the printed list of nine terms, any five of which are explained.',
    'q8-box-dovetail-joint': 'SEC model sketch of a box dovetail joint at the corner of a box.',
    'q8-triple-glazing': 'SEC model sketch of a triple-glazed unit: three panes separated by two cavities and spacers.',
    'q8-solar-panel': 'SEC model sketches of a flat-plate solar collector on a roof and an evacuated-tube collector.',
    'q8-cordless-drill': 'SEC model sketch of a cordless drill with its battery.',
    'q8-skirting-board': 'SEC model sketch of a profiled skirting board fixed at the base of a wall.',
    'q8-compression-fitting': 'SEC model sketch of a compression fitting joining two pipes, with its nuts.',
    'q8-natural-seasoning': 'SEC 2015 Ordinary marking scheme notes on natural seasoning, with sketches of timber stacked on piers in an open-sided shed and a covered stack separated by stickers.',
    'q8-concrete-lintel': 'SEC model sketch of a concrete lintel bearing on blockwork.',
    'q8-radon-barrier': 'SEC model cut-away of a floor and external wall showing the radon barrier A laid under the floor and continued through the wall.',
    'q9-original': 'Original SEC 2015 Ordinary Construction Studies Question 9: the printed question with a sketch of the corner of a slatted wooden table.',
    'q9-joint': 'SEC model haunched mortise and tenon joint: the leg with its mortise (A), the rail with its haunched tenon (B), the assembled joint, the notes and the reasons for choosing it.',
    'q9-table-features': 'SEC model sketch of spaced tabletop boards, with arrows showing water dripping through the gaps at A and B.',
    'q9-finish': 'SEC model sketches of an orbital sander, a paintbrush and a tin of finish.',
}
assert set(ALT) == {f['key'].removeprefix(validator.FP) for f in draft['questionFigures']}
for f in draft['questionFigures']:
    src = HERE / f"{f['key']}.png"
    md5 = hashlib.md5(src.read_bytes()).hexdigest()
    assert f['key'] not in manifest and md5 not in known_md5 and not (public / src.name).exists()
    known_md5.add(md5)

# ---- mutate (all preconditions checked above)
now = datetime.now(timezone.utc).isoformat()
prior_hashes = {c['id']: hashlib.sha256(json.dumps(c, ensure_ascii=False, sort_keys=True).encode()).hexdigest() for c in prior}
save(HERE / 'prior-authored-card-hashes.json', dict(count=607, algorithm='sha256 of json.dumps(card, ensure_ascii=False, sort_keys=True)', cards=prior_hashes))
for f in draft['questionFigures']:
    key = f['key']
    dst = public / f'{key}.png'
    shutil.copyfile(HERE / f'{key}.png', dst)
    manifest[key] = dict(src='/' + str(dst.relative_to(R / 'public')), md5=hashlib.md5(dst.read_bytes()).hexdigest(),
                         alt=ALT[key.removeprefix(validator.FP)],
                         attribution='SEC Leaving Certificate Construction Studies 2015 Ordinary Level — © State Examinations Commission.',
                         solution=f['solution'])
save(manifest_path, manifest)
review = dict(draft, status='2015 Ordinary main English theory Q1–Q9: 176 source-reviewed tasks integrated; whole theory paper reconciled against the original paper and scheme. Practical component and Irish edition remain separate work.',
              reviewedAt=now, paperComplete=True,
              fullPaperReconciliation=dict(questions=9, wholeQuestionRoutes=report['wholeQuestionRoutes'], q8Routes=126,
                                           examRubric='Q1 plus three other questions, 50 marks each, 200 total; no full-exam Cartesian cards.',
                                           method='Same-operator source review of paper pages 1–3 and scheme pages 2–25; validator construction_2015_ordinary.py.'),
              priorAuthoredCardHashes='docs/markbank-audit/2026-09-28/drafts/construction-2015-ordinary-q1-q9/prior-authored-card-hashes.json')
save(review_path, review)
save(authored_path, prior + new_cards)
assert read(authored_path)[:607] == prior
bridge = dict(schemaVersion=1, subjectId='construction-studies', year=2015, level='ordinary', lang='ev', sitting='main',
              paperKey='single', reviewedAt=now, authoringReview=str(review_path.relative_to(R)), sourceHashes=draft['sourceHashes'],
              expectedRuntimeCards=176,
              reason='2015 Ordinary main English theory: all nine printed questions and 176 source-reviewed tasks, including all 126 Q8 choose-five routes. Exact original-question anchors and constituent topics; joinery/tools nodes without an Ordinary reference heading are declared in taxonomyGaps. Practical/Irish/other papers remain open.',
              questions=[dict(n=q, fileid='LC029GLP000EV.pdf',
                              topicIds=sorted({t for b in draft['bindings'] if b['questionNumber'] == q for t in b['atlasTopicIds']}))
                         for q in draft['questionsReviewed']],
              cards=draft['bindings'], taxonomyGaps=draft['taxonomyGaps'])
save(bridge_path, bridge)
with fitz.open(R / validator.S) as pdf:
    raw = '\n\n'.join(f'<!-- Original PDF page {i + 1} -->\n' + p.get_text() for i, p in enumerate(pdf) if i < 25)
scheme_md.write_text('# SEC Construction Studies 2015 Ordinary theory marking scheme\n\n' + raw)

ids = [c['id'] for c in new_cards]
p = R / 'test/fixtures/construction2015Reviewed.ts'
s = p.read_text()
assert 'CONSTRUCTION_2015_ORDINARY_REVIEWED_IDS' not in s
s += ('\n// Original 2015 Ordinary Q1–Q9: every separately marked task, every complete question and all\n'
      '// 126 choose-five Q8 routes (C(9,5)).\n'
      'export const CONSTRUCTION_2015_ORDINARY_REVIEWED_IDS = '
      + json.dumps(ids, indent=2).replace('"', "'") + ';\n')
p.write_text(s)
p = R / 'test/constructionStudiesExamTopics.test.ts'
s = p.read_text()
for old, new in [
    ("import { CONSTRUCTION_2015_HIGHER_REVIEWED_IDS } from './fixtures/construction2015Reviewed';",
     "import { CONSTRUCTION_2015_HIGHER_REVIEWED_IDS, CONSTRUCTION_2015_ORDINARY_REVIEWED_IDS } from './fixtures/construction2015Reviewed';"),
    ('    expect(CONSTRUCTION_ORDINARY).toHaveLength(250);',
     '    expect(CONSTRUCTION_ORDINARY).toHaveLength(250 + CONSTRUCTION_2015_ORDINARY_REVIEWED_IDS.length);'),
    (').size).toBe(505 + CONSTRUCTION_2015_HIGHER_REVIEWED_IDS.length);',
     ').size).toBe(505 + CONSTRUCTION_2015_HIGHER_REVIEWED_IDS.length + CONSTRUCTION_2015_ORDINARY_REVIEWED_IDS.length);'),
]:
    assert s.count(old) == 1, old
    s = s.replace(old, new)
p.write_text(s)
p = R / 'test/markBankCardPreservation.test.ts'
s = p.read_text()
for old, new in [
    ("import { CONSTRUCTION_2015_HIGHER_REVIEWED_IDS } from './fixtures/construction2015Reviewed';",
     "import { CONSTRUCTION_2015_HIGHER_REVIEWED_IDS, CONSTRUCTION_2015_ORDINARY_REVIEWED_IDS } from './fixtures/construction2015Reviewed';"),
    ('const recoveredConstructionIds = new Set(CONSTRUCTION_2015_HIGHER_REVIEWED_IDS);',
     'const recoveredConstructionIds = new Set([...CONSTRUCTION_2015_HIGHER_REVIEWED_IDS, ...CONSTRUCTION_2015_ORDINARY_REVIEWED_IDS]);'),
]:
    assert s.count(old) == 1, old
    s = s.replace(old, new)
p.write_text(s)

save(HERE / 'integration.json', dict(reviewedAt=now, addedTasks=176, priorAuthoredCardsPreserved=607, newAuthoredCount=783,
                                     newFigures=35, wholeQuestionRoutes=report['wholeQuestionRoutes'], q8Routes=126,
                                     validator=report, status='Authored/bridge/test inputs applied; generation and runtime checks next.'))
print('Integrated 176 Ordinary tasks; authored deck input 783 cards; 35 figures.')
