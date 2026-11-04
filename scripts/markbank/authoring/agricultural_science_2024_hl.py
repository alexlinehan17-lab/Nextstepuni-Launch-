"""2024 Higher review: the 72 original cards reconciled against the SEC sources.

All 44 paper pages and 28 scheme pages were inspected and the independent
census transcribed before any card was touched. 63 original card objects match
a published task boundary and tariff and are left byte-identical; they only
gain an Atlas binding and an inspected official source page. Nine original
cards are corrected IN PLACE, keeping their IDs (and saved progress): Q2(a)(i)
and Q6(a) become one card each for their printed item choice (a printed
any-N-of-M choice is one practice card, never combination siblings); Q17(a)
and Q18(a)(iii) regain their published first-correct splits; Q2(a)(iii) loses
an accepted "answer" that was the question's own wording; Q16(b)(i) regains the
truncated end of its answer; and Q16(b)(ii), Q17(c)(ii) and Q17(c)(iii)
replace a results table flattened into label soup with the paper's own wording
and the table crop. Each correction records the original wording, marks and
object hash plus the SEC page that justifies it.
"""
import copy
import hashlib
import json
from agricultural_science_2010_hl import ROOT, point, menu, region
from agricultural_science_2010_parity import scan

FILE = 'LC024ALP000EV.pdf'
YEAR = 2024
HASHES = {'exampapers':'6dce8f33e8e14be906d7d48b0585be29982238a2579ab0d1ac1cadb2a2f0cd84',
          'markingschemes':'a3ae68c8d965d958bc13054ef527ddf64d8f8991053859aae5b4823d69b3f225'}
SELECTIONS = {
    '843cec95ff3043cb':('exam-selection','Instructions: Section A, ten of twelve independent questions. Every question and both sides of each internal choice are retained.'),
    'ea3b3226438791d2':('exam-selection','Instructions: Section B, four of six independent questions. Every question is retained.'),
    '71038ca6471079fa':('exam-selection','Repeated Section A instruction: ten independent 10-mark questions, all retained.'),
    '9e20b1d011162ade':('independent-task-selection','Q2 either (a) or (b): both independently marked alternatives are retained.'),
    '223b9af9c9f623b0':('closed','Q2(a)(i): identify any two of the three printed breed photographs A, B and C, 2(2). One card: a single anyN row lists all three breeds, claim limit two (item-choice siblings are not separate practice identities).'),
    '6caaad42c1aa08a4':('not-a-selection','Prose in the Q2(b) article ("one of the rarest Irish cattle breeds"); no response choice.'),
    '33e6c4291021cdb1':('independent-task-selection','Q3 either (a) or (b): both alternatives are retained.'),
    '1219196bfd47c12c':('independent-task-selection','Q6 either (a) or (b): both alternatives are retained.'),
    '4d4469089bd00069':('closed','Q6(a): any two of four printed target features / activities, each with its action (3) and benefit (2). One card: an anyN action row and an anyN benefit row, each listing all four features, claim limit two.'),
    'f1e2ff4300775d5c':('closed','Q6(b)(ii): any two of three printed target features, 3+1. The original one-card form already lets any two of the three score, so it is kept unchanged.'),
    'db3e9151df2a298b':('not-a-selection','Prose in the Q7 article ("trees with either crops or livestock"); no response choice.'),
    'e9ba4a6006d2032d':('independent-task-selection','Q9 either (a) or (b): both alternatives are retained.'),
    '33be39e92663abfa':('exam-selection','Section B heading: four of six independent 50-mark questions, all retained.'),
    'f3d547c8be945360':('independent-task-selection','Q13: (a) and (b) with either (c) or (d). Every part, including both (c) and (d), is retained.'),
    '65f7e71bb67d2c28':('not-a-selection','Prose in the Q13(a) stem ("one of the best ways"); no response choice.'),
    '18b0f122a37a410d':('independent-task-selection','Q14: (a) and (b) with either (c) or (d). Every part, including both (c) and (d), is retained.'),
}
SUPPLEMENTARY = [
    (28,'State two animal-related factors or two environmental conditions.','closed','Q15(a)(iii): two from one of two printed columns, 2(2). The original one-card form lists both columns in one anyN row, claim limit two, so it is kept unchanged.'),
    (7,'climate and /or environmental benefits','open','Q3(b): flexible and/or wording; one response.'),
    (13,'provide another example of a biological control and state its target','open','Q8(c): a student-chosen biological control; the scheme table is a marking menu.'),
    (23,'State two locations in Ireland where you would find a peat soil.','open','Q13(b)(ii): any named correct locations; no printed pool.'),
    (29,'Briefly describe the symptoms and prevention of a named mineral deficiency in cows.','open','Q15(a)(v): a student-named deficiency; the scheme rows are worked examples kept as exclusive marking routes on one card.'),
    (34,'Briefly describe how any named abiotic factor will affect Irish agriculture.','open','Q17(a): a student-named abiotic factor; the scheme table is a marking menu ("any named correct effect").'),
    (38,'Briefly describe one named method of genetic engineering you have studied','open','Q18(b)(iii): a student-named method; the scheme adds "or other valid example".'),
    (9,'Assist farmers by identifying A, B and C as barley, wheat or oats.','answer-identification','Q5(a): one correct crop per photograph; the three names are answers, not routes.'),
    (14,'identify the soil quality of each of the','answer-identification','Q9(b)(i): one quality per soil sample from the printed list; identification, not a route choice.'),
    (22,'Identify the plants A, B, C and D using the list below.','answer-identification','Q13(a)(ii): one name per photograph from the printed list.'),
    (6,'Using the list provided, state which grazing system is most likely to be associated with','answer-identification','Q3(a)(iii): one system for each of the two printed periods.'),
]
SOURCE_NOTES = {
    'Q18':'The published allocations for Question 18 total 54, not the printed 50: (a) 4 + (6+2) + (6+2) = 20, (b) 4 + (6+2) + 3(2) = 18 and (c) 6+6+4 = 16. Each part keeps its published tariff; no marks are invented or removed.',
}
TOPIC = 'agricultural-science-higher-'
SNAPSHOT = ROOT / 'scripts/markbank/authored/agricultural-science-corrected-originals.json'
PREFIX = 'agsci-2024-hl-'
# Original objects written back unchanged after an earlier review rewrote them.
RESTORED = []


def original_hash(card):
    return hashlib.sha256(json.dumps(card, ensure_ascii=False, sort_keys=True).encode()).hexdigest()


def paper_review():
    observed, supplementary = scan(YEAR, FILE, HASHES, SELECTIONS, SUPPLEMENTARY)
    notes = [dict(questionN='18', questionRef='Q18', note=SOURCE_NOTES['Q18'])]
    return dict(year=YEAR, level='higher', lang='ev', paperFileid=FILE, hashes=HASHES,
                wholePaperVisualReview='reviewed', schemeBoundaryReview='reviewed',
                paperPagesInspected=list(range(1, 45)), schemePagesInspected=list(range(1, 29)),
                selectionDirectives=observed, supplementarySelections=supplementary, sourceNotes=notes,
                independentBoundaryReview='81 base tasks, one card each. 63 original cards match a published boundary and tariff unchanged (Q6(b)(ii) and Q15(a)(iii) already let any printed choice score). Nine are corrected in place (Q2(a)(i) and Q6(a) become one item-choice card each; Q2(a)(iii), Q16(b)(i), Q16(b)(ii), Q17(a), Q17(c)(ii), Q17(c)(iii), Q18(a)(iii)); 9 cards are added for the missing Q5(a), Q9(b)(i), Q9(b)(ii), Q13(a)(ii), Q14(c), Q15(c)(i), Q18(a)(ii), Q18(b)(iii) and Q18(c).',
                cropVisualReview='Every distinct paper/scheme crop pair rendered and inspected.',
                runtimeReview='Integrated production-component cases at 1200px and 390px. Signed-in full-app navigation remains open.',
                remaining=['Irish edition comparison (deferred)', 'Full application navigation review', 'Corpus-wide reconciliation'])


# Paper / scheme crop regions for every base task (original cards included).
P = lambda *r: [region(*x) for x in r]
REGIONS = {
    'Q1(a)': (P((3, .16, .68)), P((12, .137, .222))),
    'Q1(b)': (P((3, .16, .68), (3, .684, .712)), P((12, .222, .302))),
    'Q2(a)(i)': (P((4, .065, .265)), P((12, .302, .385))),
    'Q2(a)(ii)': (P((4, .065, .265), (4, .326, .362)), P((12, .385, .449))),
    'Q2(a)(iii)': (P((4, .065, .265), (4, .468, .505)), P((12, .449, .531))),
    'Q2(b)(i)': (P((5, .065, .503)), P((12, .531, .614))),
    'Q2(b)(ii)': (P((5, .065, .475), (5, .578, .60)), P((12, .614, .678))),
    'Q2(b)(iii)': (P((5, .065, .475), (5, .675, .785)), P((12, .678, .848))),
    'Q3(a)(i)': (P((6, .065, .563)), P((13, .085, .133))),
    'Q3(a)(ii)': (P((6, .065, .536), (6, .605, .627)), P((13, .133, .232))),
    'Q3(a)(iii)': (P((6, .065, .536), (6, .729, .88)), P((13, .232, .313))),
    'Q3(b)': (P((7, .065, .21)), P((13, .313, .588))),
    'Q4': (P((8, .065, .705)), P((14, .085, .472))),
    'Q5(a)': (P((9, .065, .612)), P((14, .472, .548))),
    'Q5(b)': (P((9, .065, .13), (9, .612, .668)), P((14, .548, .631))),
    'Q6(a)': (P((10, .065, .36)), P((15, .085, .623))),
    'Q6(b)(i)': (P((11, .07, .356)), P((15, .623, .710))),
    'Q6(b)(ii)': (P((11, .07, .118), (11, .497, .676)), P((15, .710, .878))),
    'Q7(a)': (P((12, .065, .273)), P((16, .085, .148))),
    'Q7(b)': (P((12, .065, .246), (12, .349, .37)), P((16, .148, .280))),
    'Q8(a)': (P((13, .065, .456)), P((16, .280, .342))),
    'Q8(b)': (P((13, .065, .432), (13, .531, .565)), P((16, .342, .402))),
    'Q8(c)': (P((13, .065, .432), (13, .704, .78)), P((16, .402, .518))),
    'Q9(a)': (P((14, .065, .342)), P((16, .518, .720))),
    'Q9(b)(i)': (P((14, .379, .703)), P((16, .720, .804))),
    'Q9(b)(ii)': (P((14, .379, .703), (14, .707, .729)), P((16, .804, .902))),
    'Q10(a)': (P((15, .065, .486)), P((17, .085, .133))),
    'Q10(b)': (P((15, .065, .452), (15, .531, .553)), P((17, .133, .183))),
    'Q10(c)': (P((15, .065, .452), (15, .627, .666)), P((17, .183, .316))),
    'Q11(a)': (P((16, .065, .385)), P((17, .316, .403))),
    'Q11(b)': (P((16, .065, .362), (16, .570, .591)), P((17, .403, .486))),
    'Q11(c)': (P((16, .065, .362), (16, .666, .689)), P((17, .486, .571))),
    'Q12(a)': (P((17, .065, .459)), P((17, .571, .706))),
    'Q12(b)': (P((17, .065, .15), (17, .654, .693)), P((17, .706, .823))),
    'Q13(a)(i)': (P((21, .155, .246)), P((18, .138, .274))),
    'Q13(a)(ii)': (P((22, .065, .33)), P((18, .274, .359))),
    'Q13(a)(iii)': (P((22, .334, .666)), P((18, .359, .454))),
    'Q13(b)(i)': (P((23, .065, .093)), P((18, .454, .569))),
    'Q13(b)(ii)': (P((23, .786, .808)), P((18, .569, .614))),
    'Q13(c)': (P((24, .065, .106)), P((18, .614, .761))),
    'Q13(d)': (P((24, .494, .517)), P((18, .778, .914))),
    'Q14(a)(i)': (P((25, .065, .30)), P((19, .085, .152))),
    'Q14(a)(ii)': (P((25, .065, .128), (25, .304, .344)), P((19, .152, .314))),
    'Q14(a)(iii)': (P((25, .065, .128), (25, .750, .88)), P((19, .314, .379))),
    'Q14(b)(i)': (P((26, .065, .17)), P((19, .379, .613))),
    'Q14(b)(ii)': (P((25, .065, .128), (27, .065, .09)), P((19, .613, .692))),
    'Q14(c)': (P((27, .345, .40)), P((19, .692, .876))),
    'Q14(d)': (P((27, .678, .70)), P((20, .085, .163))),
    'Q15(a)(i)': (P((28, .065, .325)), P((20, .163, .205))),
    'Q15(a)(ii)': (P((28, .065, .303), (28, .40, .69)), P((20, .205, .438))),
    'Q15(a)(iii)': (P((28, .695, .88)), P((20, .438, .565))),
    'Q15(a)(iv)': (P((29, .065, .266)), P((20, .565, .783))),
    'Q15(a)(v)': (P((29, .265, .486)), P((21, .085, .506))),
    'Q15(b)(i)': (P((29, .487, .554)), P((21, .506, .602))),
    'Q15(b)(ii)': (P((29, .487, .531), (29, .716, .739)), P((21, .602, .703))),
    'Q15(c)(i)': (P((30, .065, .417)), P((21, .703, .872))),
    'Q15(c)(ii)': (P((30, .065, .125), (30, .611, .666)), P((22, .085, .171))),
    'Q16(a)(i)': (P((31, .065, .443)), P((22, .171, .278))),
    'Q16(a)(ii)': (P((31, .065, .416), (31, .517, .54)), P((22, .278, .386))),
    'Q16(a)(iii)': (P((31, .065, .416), (31, .675, .87)), P((22, .386, .516))),
    'Q16(a)(iv)': (P((31, .065, .416), (32, .065, .09)), P((22, .516, .599))),
    'Q16(b)(i)': (P((32, .216, .496)), P((22, .599, .681))),
    'Q16(b)(ii)': (P((32, .216, .452), (32, .565, .601)), P((22, .681, .780))),
    'Q16(c)': (P((31, .065, .20), (32, .727, .768)), P((22, .780, .880))),
    'Q16(d)': (P((33, .065, .115), (33, .340, .362), (33, .588, .611)), P((23, .085, .287))),
    'Q17(a)': (P((34, .065, .196)), P((23, .287, .640))),
    'Q17(b)(i)': (P((34, .065, .135), (34, .334, .40)), P((23, .640, .747))),
    'Q17(b)(ii)': (P((34, .334, .362), (34, .591, .616)), P((23, .747, .849))),
    'Q17(b)(iii)': (P((34, .334, .362), (34, .748, .87)), P((24, .085, .151))),
    'Q17(b)(iv)': (P((34, .334, .362), (35, .065, .09)), P((24, .151, .337))),
    'Q17(b)(v)': (P((34, .334, .362), (35, .345, .386)), P((24, .337, .450))),
    'Q17(c)(i)': (P((36, .065, .136)), P((24, .450, .556))),
    'Q17(c)(ii)': (P((36, .065, .104), (36, .266, .442)), P((24, .556, .675))),
    'Q17(c)(iii)': (P((36, .065, .104), (36, .266, .414), (36, .622, .646)), P((24, .675, .795))),
    'Q18(a)(i)': (P((37, .065, .135)), P((25, .085, .150))),
    'Q18(a)(ii)': (P((37, .238, .489)), P((25, .150, .225))),
    'Q18(a)(iii)': (P((37, .238, .81)), P((25, .225, .306))),
    'Q18(b)(i)': (P((38, .065, .162)), P((25, .306, .356))),
    'Q18(b)(ii)': (P((38, .065, .135), (38, .266, .29)), P((25, .356, .475))),
    'Q18(b)(iii)': (P((38, .065, .135), (38, .484, .52)), P((25, .475, .888))),
    'Q18(c)': (P((39, .065, .302)), P((26, .085, .418))),
}
# Atlas topics, read from each task's content (SEC-derived, not copied).
ATLAS = {
    'Q1(a)': 'sheep|grassland', 'Q1(b)': 'sheep',
    'Q2(a)(i)': 'pigs|sheep|beef-cattle', 'Q2(a)(ii)': 'sheep|genetics', 'Q2(a)(iii)': 'beef-cattle|genetics',
    'Q2(b)': 'beef-cattle|dairy-cattle', 'Q3': 'grassland', 'Q3(b)': 'grassland|fertilisers-pollution-environment-cycles',
    'Q4': 'soil-science', 'Q5': 'crop-production', 'Q5(a)': 'crop-production|classification-of-animals-plants',
    'Q6': 'sheep', 'Q7': 'fertilisers-pollution-environment-cycles|innovation-and-biotechnology-in-agriculture',
    'Q8': 'grassland|crop-production', 'Q9': 'soil-science', 'Q10': 'grassland|soil-science',
    'Q11': 'dairy-cattle|animal-physiology-reproductive-systems', 'Q12': 'fertilisers-pollution-environment-cycles',
    'Q13(a)(i)': 'grassland|scientific-practices-experiments-investigations', 'Q13(a)(ii)': 'classification-of-animals-plants|grassland',
    'Q13(a)(iii)': 'grassland|fertilisers-pollution-environment-cycles', 'Q13(b)': 'soil-science',
    'Q13(c)': 'soil-science|fertilisers-pollution-environment-cycles', 'Q13(d)': 'fertilisers-pollution-environment-cycles',
    'Q14': 'grassland', 'Q14(b)(i)': 'grassland|scientific-practices-experiments-investigations', 'Q14(c)': 'grassland|plant-physiology',
    'Q15': 'beef-cattle', 'Q15(a)(i)': 'beef-cattle|genetics', 'Q15(a)(v)': 'beef-cattle|animal-diseases',
    'Q16': 'dairy-cattle|scientific-practices-experiments-investigations', 'Q16(c)': 'dairy-cattle|animal-physiology-digestive-system',
    'Q16(d)': 'dairy-cattle', 'Q17': 'soil-science', 'Q17(a)': 'soil-science|crop-production',
    'Q17(c)': 'soil-science|scientific-practices-experiments-investigations',
    'Q18(a)': 'genetics|dairy-cattle', 'Q18(a)(ii)': 'classification-of-animals-plants|genetics',
    'Q18(b)': 'genetics|innovation-and-biotechnology-in-agriculture', 'Q18(c)': 'crop-production',
}
BREEDS = {'A': 'Landrace', 'B': 'Blue Leicester', 'C': 'Simmental'}
# Q6(a): the four printed target features with the scheme's actions (i) and benefits (ii).
FEATURES = {
    'lameness': ('Lameness control', ['regular checking', 'footbath', 'antibiotic spray', 'paring hooves', 'vaccination', 'closed flock', 'breed selection'],
                 ['increased LWG', 'increased conception rates', 'increased milk production']),
    'minerals': ("Mineral supplementation of ewe's post mating", ['(bucket) lick', 'bolus', 'injection', 'feed additive', 'drench'],
                 ['improve (P) conception rate or maintain pregnancy', 'improved development of embryo (health) or foetus or lamb', '(Mg) prevent grass tetany or reduced (nutritional) disease']),
    'meal': ("Meal feeding of lamb's post weaning", ['creep feeder', 'trough'],
             ['increase liveweight gain', 'reach slaughter weight quicker', 'reduces stress of weaning']),
    'scanning': ('Scanning of in-lamb ewes', ['ultrasound scanner or scanner placed on abdomen'],
                 ['determine the number of lambs the ewe is carrying', 'can feed ewes accordingly or housing management', 'cull barren ewes']),
}
# Q6(b)(ii): the three printed target features with the scheme's explanations.
# The scheme heads the first one "Mineral supplementation lambs pre-weaning".
SCHEME_LABEL = {'Mineral supplementation of lambs pre-weaning': 'Mineral supplementation lambs pre-weaning'}
WELFARE = {
    'minerals': ('Mineral supplementation of lambs pre-weaning', ['improved LWG', 'reduced nutritional disease']),
    'flystrike': ('Flystrike control', ['prevent maggots feeding off them (which increases liveweight of animal)', 'less pain']),
    'genotyping': ('Genotyping of ram', ['provides easier lambing', 'better disease resistance', 'less mutations', 'improved dag score', 'increased survival (rate)']),
}
FACTORS = {
    'animal-related-factors': ('Animal-related factors', ['Weight', 'age', 'sex', 'stage and extent of production', 'body composition', 'genetics', 'amount of physical activity', 'health']),
    'environmental-conditions': ('Environmental conditions', ['Temperature', 'humidity', 'wind chill or draught free', 'ultraviolet radiation or UV light', 'precipitation', 'soil nutrient deficiencies']),
}


def atlas_for(ref):
    base = ref.split(' — ')[0]
    for key in (base, base.split(')(')[0] + ')' if ')(' in base else None, base.split('(')[0]):
        if key and key in ATLAS:
            return ATLAS[key]
    raise KeyError(ref)


def reviewed_tasks(existing):
    """existing: {id: card} from the authored file (originals are read, never rewritten unless corrected)."""
    paper_review()
    cards, tasks, corrections = [], [], {}
    RESTORED.clear()
    # Original cards carry no review stamp; cards this review wrote do. The
    # corrected originals come from their frozen snapshot, never the file.
    originals = {cid: card for cid, card in existing.items()
                 if cid.startswith(PREFIX) and (card.get('qa') or {}).get('humanReviewedBy') != 'agent-source-reviewed'}
    snapshot = json.loads(SNAPSHOT.read_text()) if SNAPSHOT.exists() else {}
    for cid, record in snapshot.items():
        if cid.startswith(PREFIX):
            originals[cid] = record['original']

    def task(cid, ref, base, selection=None, examTopics=None, note=None):
        pp, sp = REGIONS[base]
        t = dict(questionRef='2024 HL ' + ref, paperPage=pp[0]['p'], schemePage=sp[0]['p'], paperRegions=pp, schemeRegions=sp,
                 atlasNumbers={cid: str(1001 + len(tasks))}, cardIds=[cid],
                 examTopicIds=[TOPIC + t for t in (examTopics or atlas_for(ref)).split('|')],
                 selection=selection or {'kind': 'none', 'reason': 'Required response at a published boundary. Scheme alternatives remain marking menus.'},
                 evidence='All 44 paper and 28 scheme pages visually inspected. Boundary and tariff checked against the independently transcribed census.')
        if note:
            t['schemeNote'] = note
        tasks.append(t)
        return t

    def keep(key, ref, examTopics=None, selection=None):
        cid = PREFIX + key
        card = originals[cid]
        assert card['questionRef'] == '2024 HL ' + ref, (cid, card['questionRef'])
        t = task(cid, ref, ref, selection=selection, examTopics=examTopics)
        t['marksPerRoute'] = card['totalMarks']
        t['originalCard'] = 'unchanged'
        if cid in snapshot:
            assert original_hash(card) == snapshot[cid]['originalSha256']
            RESTORED.append(card)

    def source(ref, pp):
        return dict(kind='source-text', label='OFFICIAL QUESTION PAGE', title='Agricultural Science 2024 Higher — ' + ref,
                    pages=sorted({r['p'] for r in pp}), attribution='SEC Agricultural Science 2024 Higher Level examination paper — © State Examinations Commission.',
                    presentationNote='Open the original page for the published wording, photographs, tables and examination context.')

    def record(cid, t, reason):
        old = originals[cid]
        corrections[cid] = dict(originalSha256=original_hash(old), originalQuestionRef=old['questionRef'],
                                originalQuestionText=old['questionText'], originalTotalMarks=old['totalMarks'],
                                originalTariffModel=old['tariffModel'], reason=reason)
        t['originalCard'] = 'corrected-in-place'

    def add(key, ref, base, topic, concept, question, rows, stem=None, marks=None, tariff=None, selection=None, figure=None, labels=None,
            extra=(), examTopics=None, correction=None, extra_fields=None):
        cid = PREFIX + key
        rows = [dict(row, id=f'r-{i+1}') for i, row in enumerate(rows)]
        pp, _ = REGIONS[base]
        card = dict(id=cid, subjectId='agricultural-science', year=YEAR, level='higher',
                    section='A' if int(base.split('(')[0][1:]) <= 12 else 'B', questionRef='2024 HL ' + ref,
                    topicId='agsci-' + topic, curriculumNodeIds=['agsci-' + t for t in (topic, *extra)],
                    conceptId=concept, questionText=question, rows=rows,
                    totalMarks=marks if marks is not None else sum(r['marks'] for r in rows),
                    tariffModel=tariff or {'kind': 'questionTotal' if marks is not None else 'fixed'},
                    sourceMaterial=source(ref, pp))
        if extra:
            card['additionalTopicIds'] = ['agsci-' + t for t in extra]
        if stem: card['stem'] = stem
        if figure: card['figureKey'] = figure
        if labels: card['labelKey'] = labels
        if extra_fields: card.update(extra_fields)
        t = task(cid, ref, base, selection, examTopics)
        t['marksPerRoute'] = card['totalMarks']
        if correction:
            record(cid, t, correction)
        else:
            assert cid not in originals, f'{cid} would replace an original card without a correction record'
            t['originalCard'] = 'added'
        cards.append(card)
        return card

    def fix(key, ref, changes, drop=(), correction=None):
        """Correct an original in place: same ID, ref and boundary; only the named fields change."""
        cid = PREFIX + key
        card = copy.deepcopy(originals[cid])
        assert card['questionRef'] == '2024 HL ' + ref, (cid, card['questionRef'])
        for field in drop:
            card.pop(field, None)
        if 'rows' in changes:
            changes = dict(changes, rows=[dict(row, id=f'r-{i+1}') for i, row in enumerate(changes['rows'])])
        card.update(changes)
        card['curriculumNodeIds'] = [card['topicId']]
        card['sourceMaterial'] = source(ref, REGIONS[ref][0])
        t = task(cid, ref, ref)
        t['marksPerRoute'] = card['totalMarks']
        record(cid, t, correction)
        cards.append(card)
        return card

    def closed(choose, options):
        # Item choice is ONE practice card (coordinator rule, 2026-10-12).
        return {'kind': 'closed', 'choose': choose, 'options': options, 'pooled': True}

    # Section A ---------------------------------------------------------------
    keep('q1a', 'Q1(a)')
    keep('q1b', 'Q1(b)')
    letters = list(BREEDS)
    add('q2ai', 'Q2(a)(i)', 'Q2(a)(i)', '4-1', 'identifying-pig-sheep-and-cattle-breeds',
        'Identify any two of the following breeds.', [menu([f'{l}: {BREEDS[l]}' for l in letters], [2, 2], 'Any two of the three photographs, 2 marks each (2(2)).')],
        'Answer either (a) or (b).', selection=closed(2, letters), figure='agricultural-science-2024-HL-paper-p04-art',
        labels=[dict(letter=l, meaning=BREEDS[l], askedInThisQuestion=True) for l in letters],
        examTopics='pigs|sheep|beef-cattle',
        correction=('Visually verified paper PDF page 4 ("Identify any two of the following breeds", photographs A, B and C) and scheme PDF page 12 ("2(2)": A Landrace, B Blue Leicester, C Simmental). '
                    'The original stem was the stray word "Or" and only A and B were decoded, with C carried as an accepted alternative. Same ID: one any-two-of-three card whose anyN row lists all three breeds, '
                    'claim limit two, with every photograph decoded.'))
    keep('q2aii', 'Q2(a)(ii)')
    fix('q2aiii', 'Q2(a)(iii)', dict(
        stem='Answer either (a) or (b). Part (i) shows three photographs lettered A, B and C; C is a bull.',
        rows=[menu(['Good conformation', 'high muscle', 'good KO%', 'good carcase weight'], [2, 2],
                   'Two characteristics at 2 marks each (2(2)).')], tariffModel={'kind': 'fixed', 'notation': '2(2)'}),
        correction=('Visually verified paper PDF page 4 ("Briefly explain characteristics of bull C in part (i) above that make it suitable as a terminal sire") and scheme PDF page 12 ("Good conformation / high muscle / good KO% / good carcase weight", 2(2)). '
                    'Both original rows listed the question\'s own wording as an accepted answer. Same ID, boundary and 4 marks; the rows are now the four printed characteristics, any two at 2 marks each.'))
    keep('q2bi', 'Q2(b)(i)')
    keep('q2bii', 'Q2(b)(ii)')
    keep('q2biii', 'Q2(b)(iii)')
    for k, ref in [('q3ai', 'Q3(a)(i)'), ('q3aii', 'Q3(a)(ii)'), ('q3aiii', 'Q3(a)(iii)'), ('q3b', 'Q3(b)'), ('q4', 'Q4')]:
        keep(k, ref)
    cereal_stem = ('Cereal crops form the basis of many animal and human diets with an estimated 2.1 million tonnes being produced in 2023. '
                   'You have been asked to show a group of farmers barley, wheat and oats crops. At the time of visiting the farm, each crop was at the stage shown in row 1. '
                   'Each crop at its ripening stage is shown for reference in row 2.')
    add('q5a', 'Q5(a)', 'Q5(a)', '3-3-1', 'identifying-barley-wheat-and-oats',
        'Assist farmers by identifying A, B and C as barley, wheat or oats.',
        [point('A — Oats', None, 'The scheme prints 5+2(1): the first correct identification earns 5 marks and the next two 1 each.'),
         point('B — Wheat', None), point('C — Barley', None)],
        cereal_stem, marks=7, tariff={'kind': 'orderedSplit', 'notation': '5+2(1)'},
        figure='agricultural-science-2024-hl-paper-p009-i0',
        labels=[dict(letter=l, meaning=m, askedInThisQuestion=True) for l, m in (('A', 'Oats'), ('B', 'Wheat'), ('C', 'Barley'))], extra=('3-2',))
    keep('q5b', 'Q5(b)')
    sheep_stem = ('Answer either (a) or (b). Many Irish sheep farmers now take part in the Sheep Improvement Scheme. Some of the target features / activities of this scheme are: '
                  "lameness control; mineral supplementation of ewe's post mating; meal feeding of lamb's post weaning; scanning of in-lamb ewes.")
    slugs = list(FEATURES)
    action_text = {'lameness': 'Lameness control: regular checking or footbath or antibiotic spray or paring hooves or vaccination or closed flock or breed selection',
                   'minerals': 'Mineral supplementation of ewe’s post mating: (bucket) lick / bolus / injection / feed additive / drench',
                   'meal': 'Meal feeding lambs post weaning: creep feeder / trough',
                   'scanning': 'Scanning in-lamb ewes: ultrasound scanner or scanner placed on abdomen'}
    benefit_text = {'lameness': 'Lameness control: increased LWG or increased conception rates or increased milk production',
                    'minerals': 'Mineral supplementation of ewes’ post mating: improve (P) conception rate or maintain pregnancy / improved development of embryo (health) or foetus or lamb / (Mg) prevent grass tetany or reduced (nutritional) disease',
                    'meal': 'Meal feeding lambs post weaning: increase liveweight gain / reach slaughter weight quicker / reduces stress of weaning',
                    'scanning': 'Scanning in-lamb ewes: determine the number of lambs the ewe is carrying / can feed ewes accordingly or housing management / cull barren ewes'}
    add('q6a', 'Q6(a)', 'Q6(a)', '4-3-2', 'sheep-improvement-scheme-measures',
        'For any two of the above listed target features / activities: (i) Describe how to action (carry out) these target features / activities. (ii) Describe the benefit of each target features / activities to overall production of the flock.',
        [menu([action_text[k] for k in slugs], [3, 3], '(i) Action for each of your two features, 3 marks each.'),
         menu([benefit_text[k] for k in slugs], [2, 2], '(ii) Benefit of each of the same two features, 2 marks each. The scheme prints 2(3) + 2(2); each benefit must belong to a feature whose action you gave.')],
        sheep_stem, selection=closed(2, [FEATURES[k][0] for k in slugs]),
        correction=('Visually verified paper PDF page 10 ("For any two of the above listed target features / activities", four printed features, (i) action and (ii) benefit) and scheme PDF page 15 (one action and one benefit per feature, "2(3) + 2(2)"). '
                    'The original fused card was referenced "Q6(a)(i)–(ii)" and spread the four features across mismatched answer slots. Same ID and 10 marks: one any-two-of-four card with an action row and a benefit row, '
                    'each listing all four features in the scheme\'s wording, claim limit two.'))
    keep('q6bi', 'Q6(b)(i)')
    keep('q6bii', 'Q6(b)(ii)', selection=closed(2, [w[0] for w in WELFARE.values()]))
    for k, ref in [('q7a', 'Q7(a)'), ('q7b', 'Q7(b)'), ('q8a', 'Q8(a)'), ('q8b', 'Q8(b)'), ('q8c', 'Q8(c)'), ('q9a', 'Q9(a)')]:
        keep(k, ref)
    soil_stem = ('Answer either (a) or (b). Soil structure describes the arrangement of soil particles within a soil. '
                 'These particles form clusters known as aggregates or peds in the soil.')
    quality = (('A', 'Good'), ('B', 'Moderate'), ('C', 'Poor'))
    add('q9bi', 'Q9(b)(i)', 'Q9(b)(i)', '2-2-2', 'judging-soil-structure-quality',
        'Based on your knowledge of soil structure, identify the soil quality of each of the different soils in A, B and C using the list below: Moderate quality, Poor quality, Good quality.',
        [point(f'{l}: {q}', 2, f'Soil {l}.') for l, q in quality], soil_stem,
        figure='agsci-2024-hl-paper-soil-structure',
        labels=[dict(letter=l, meaning=q + ' quality', askedInThisQuestion=True) for l, q in quality])
    add('q9bii', 'Q9(b)(ii)', 'Q9(b)(ii)', '2-2-2', 'reason-for-good-soil-structure',
        'Briefly describe one reason for your choice of good quality soil structure in part (i) above.',
        [menu(['Soil particles are predominantly small', 'soil particles are predominantly round', 'good crumb structure', 'presence of organic matter'], [4],
              'One reason, 4 marks.')],
        soil_stem + ' In part (i), soil A is the good quality soil structure.', figure='agsci-2024-hl-paper-soil-structure')
    for k, ref in [('q10a', 'Q10(a)'), ('q10b', 'Q10(b)'), ('q10c', 'Q10(c)'), ('q11a', 'Q11(a)'), ('q11b', 'Q11(b)'), ('q11c', 'Q11(c)'),
                   ('q12a', 'Q12(a)'), ('q12b', 'Q12(b)')]:
        keep(k, ref)
    # Section B ---------------------------------------------------------------
    keep('q13ai', 'Q13(a)(i)')
    plants = (('A', 'Primrose'), ('B', 'Nettle'), ('C', 'Ragwort'), ('D', 'Meadow Thistle'))
    add('q13aii', 'Q13(a)(ii)', 'Q13(a)(ii)', '3-2', 'identifying-grassland-indicator-plants',
        'Gill identified the following plants on the land when carrying out the investigation. Identify the plants A, B, C and D using the list below: Ragwort, Meadow Thistle, Nettle, Primrose.',
        [point(f'{l} — {p}', 2, f'Photograph {l}.') for l, p in plants],
        'Answer both (a) and (b) with either (c) or (d). Gill, an agricultural advisor, carried out an investigation to determine the botanical composition of a farmer\'s land.',
        figure='agsci-2024-hl-paper-indicator-plants',
        labels=[dict(letter=l, meaning=p, askedInThisQuestion=True) for l, p in plants], extra=('1-2',))
    for k, ref in [('q13aiii', 'Q13(a)(iii)'), ('q13bi', 'Q13(b)(i)'), ('q13bii', 'Q13(b)(ii)'), ('q13c', 'Q13(c)'), ('q13d', 'Q13(d)'),
                   ('q14ai', 'Q14(a)(i)'), ('q14aii', 'Q14(a)(ii)'), ('q14aiii', 'Q14(a)(iii)'), ('q14bi', 'Q14(b)(i)'), ('q14bii', 'Q14(b)(ii)')]:
        keep(k, ref)
    add('q14c', 'Q14(c)', 'Q14(c)', '3-2', 'drawing-grass-at-harvest-stage',
        'Draw a labelled diagram of a grass plant at the ideal named growth stage for harvesting.',
        [point('Name: Vegetative', None, 'Named stage: 2 marks.'),
         point('Elements of diagram: To show at least 3 leaves or tillers, and no seed head for 2m;', None,
               'Diagram, D = 2, 1, 0: seed head present or less than 3 leaves for 1m; no elements listed present 0m.', kind='criterion'),
         point('Leaf / tiller / node / stem/ sheath / collar / root', None, 'Labelled diagram, L = 2.')],
        'Answer both (a) and (b) with either (c) or (d). Silage harvest 2023 has been difficult for farmers due to prolonged periods of adverse weather conditions. '
        'Parts (c) and (d) are alternatives — answer one of them. The paper gives a Stage line and a box for your labelled diagram.',
        marks=6, extra=('3-3-3',))
    keep('q14d', 'Q14(d)')
    beef_stem = ('Read the article and answer the questions that follow. NUTRIENT REQUIREMENTS OF BEEF CATTLE — Beef cattle productivity is highly dependent on nutrition and the ability of the animal\'s diet to meet nutrient requirements. '
                 'To survive and be productive, beef cattle require water, energy, protein, minerals, and vitamins. (Adapted from mcdvetmanual.com) '
                 'The amounts of nutrients that cattle require is influenced by various animal-related factors and environmental conditions.')
    keep('q15ai', 'Q15(a)(i)')
    keep('q15aii', 'Q15(a)(ii)')
    keep('q15aiii', 'Q15(a)(iii)', selection=closed(1, [f[0] for f in FACTORS.values()]))
    for k, ref in [('q15aiv', 'Q15(a)(iv)'), ('q15av', 'Q15(a)(v)'), ('q15bi', 'Q15(b)(i)'), ('q15bii', 'Q15(b)(ii)')]:
        keep(k, ref)
    add('q15ci', 'Q15(c)(i)', 'Q15(c)(i)', '4-3-1', 'calculating-daily-liveweight-gain',
        'Calculate the average (mean) daily liveweight gain of the calves from birth to 15 weeks.',
        [point('85/105 = 0.81(kg/day)', 6, '125 – 40 = 85; 15 X 7 = 105; 85/105 = 0.81 (kg/day). The scheme adds: if a candidate gives 0.81 without showing calculation, award 6m; '
               'if the candidate completes two correct calculations, award 5m; if the candidate gives the correct calculation, award 4m.')],
        'Paul started weighing his beef calves to increase efficiency and comply with the Dairy Beef Weighing Scheme. Paul recorded the weight of his 52 beef calves. '
        'The average weight from birth to 15 weeks is shown in the graph below. Analyse the graph and answer the questions that follow.',
        figure='agsci-2024-hl-paper-liveweight-graph', extra=('1-3',))
    keep('q15cii', 'Q15(c)(ii)')
    for k, ref in [('q16ai', 'Q16(a)(i)'), ('q16aii', 'Q16(a)(ii)'), ('q16aiii', 'Q16(a)(iii)'), ('q16aiv', 'Q16(a)(iv)')]:
        keep(k, ref)
    colostrum = ('Ella and Sadie are agricultural science students carrying out an investigation to determine the effect of feeding pooled (combining colostrum from a number of cows) '
                 'high quality colostrum on the health and performance of dairy calves. Results of the investigation are shown in the table below. Analyse the table and answer the questions that follow.')
    table = 'agricultural-science-2024-hl-paper-p032-i0'
    flat = ('Visually verified paper PDF page 32: the results table has four columns, "Sample number Treatment group", "Colostrum IgG (mg/ml)", "Average birthweight (kg)" and "Average weaning weight (kg)". '
            'The original stem flattened it so that "(mg/ml)" fell inside "Average weaning weight". The stem now carries the paper\'s own lead-in and the card shows the inspected table crop.')
    fix('q16bi', 'Q16(b)(i)', dict(stem=colostrum, figureKey=table,
        rows=[dict(point('Pooled colostrum is best', 4, 'One 4-mark statement.'), accepts=['valid comparison with Sample 2 or Sample 3'])]),
        correction=flat + ' Scheme PDF page 22 prints the answer as "Pooled colostrum is best or valid comparison with Sample 2 or Sample 3"; the original answer stopped at "Sample 2 or". Same ID, boundary and 4 marks.')
    fix('q16bii', 'Q16(b)(ii)', dict(stem=colostrum, figureKey=table),
        correction=flat + ' Rows, boundary and 4 marks are unchanged (scheme PDF page 22).')
    keep('q16c', 'Q16(c)')
    keep('q16d', 'Q16(d)')
    fix('q17a', 'Q17(a)', dict(
        rows=[dict(menu(['Temperature', 'Humidity', 'Soil chemistry', 'Salinity', 'Oxygen levels', 'Moisture levels or drought or flooding'], [5],
                        'Named abiotic factor: 5 marks. The scheme closes its table with "Any named correct effect on plant or animal production + matching description".'), openList=True),
              menu(['Too hot or cold will cause crop failure or animal disease', 'Cause crop failure or animal disease',
                    'If not correct for plant type will cause reduced crop yields', 'May cause reduced yield'], [1],
                   'Description matching the factor named: 1 mark. Scheme pairs: temperature, too hot or cold; humidity, crop failure or animal disease; soil chemistry, salinity and oxygen levels, reduced crop yields if not correct for the plant type; moisture levels, reduced yield.')],
        tariffModel={'kind': 'fixed', 'notation': '5 (factor) + 1 (description)'}, totalMarks=6), drop=('notes',),
        correction=('Visually verified paper PDF page 34 ("Briefly describe how any named abiotic factor will affect Irish agriculture", a Named abiotic factor line and answer box) and scheme PDF page 23 ("5 (factor) + 1 (description)"). '
                    'The original priced each factor-and-description pair at 6 or nothing (best one of four), so a correctly named factor with a weak description could not earn its 5. '
                    'Same ID, boundary and 6 marks; the factor menu earns 5 and the matching description 1.'))
    for k, ref in [('q17bi', 'Q17(b)(i)'), ('q17bii', 'Q17(b)(ii)'), ('q17biii', 'Q17(b)(iii)'), ('q17biv', 'Q17(b)(iv)'), ('q17bv', 'Q17(b)(v)'), ('q17ci', 'Q17(c)(i)')]:
        keep(k, ref)
    peat = ('A student carried out an investigation to determine the percentage organic matter of two different 90g soil samples, one a loam soil and the other a peat soil. '
            'Results from the investigation are shown in the table below.')
    peat_reason = ('Visually verified paper PDF page 36: the results table has four columns, "Soil sample", "Loss in mass (g)", "% Soil organic matter" and "% Soil organic carbon". '
                   'The original stem flattened it into "Soil sample Loss in mass (g) % Soil organic % Soil organic matter carbon Peat 55.2 A B Loam 3.8 4.2 2.4". '
                   'The stem now carries the paper\'s own lead-in; the card keeps its inspected table crop, rows, boundary and 6 marks (scheme PDF page 24).')
    fix('q17cii', 'Q17(c)(ii)', dict(stem=peat), correction=peat_reason)
    fix('q17ciii', 'Q17(c)(iii)', dict(stem=peat), correction=peat_reason)
    keep('q18ai', 'Q18(a)(i)')
    isobel = 'Isobel was crossbreeding some of the cattle on her dairy farm.'
    add('q18aii', 'Q18(a)(ii)', 'Q18(a)(ii)', '4-1', 'identifying-hereford-and-friesian',
        'Identify the breeds shown in A and B.',
        [point('A: Hereford', None, 'The scheme prints 6+2: the first correct breed earns 6 marks and the second 2.'), point('B: (Holstein) Friesian', None)],
        isobel, marks=8, tariff={'kind': 'orderedSplit', 'notation': '6+2'}, figure='agsci-2024-hl-paper-breeds-ab',
        labels=[dict(letter='A', meaning='Hereford', askedInThisQuestion=True), dict(letter='B', meaning='(Holstein) Friesian', askedInThisQuestion=True)],
        extra=('4-3-3',))
    fix('q18aiii', 'Q18(a)(iii)', dict(
        stem=isobel + ' Part (ii) shows breeds A and B; Isobel crossed them and the resulting offspring is shown in C.',
        rows=[menu(['Black coat colour', 'coat pattern', 'white face', 'white legs and belly', 'pink nose', 'tail switch'], [6, 2],
                   'Any two dominant features: the first correct earns 6 marks and the second 2 (6+2).')],
        questionText='Isobel crossed breeds A and B in part (ii) above. The resulting offspring is shown in C below. List two dominant features from parents in A and B in part (ii) above that are passed to the offspring C.',
        tariffModel={'kind': 'fixed', 'notation': '6+2'}), drop=('notes',),
        correction=('Visually verified paper PDF page 37 ("List two dominant features from parents in A and B in part (ii) above that are passed to the offspring C") and scheme PDF page 25 ("Black coat colour / coat pattern / white face / white legs and belly / pink nose / tail switch", 6+2). '
                    'The original fixed the 6 marks to black coat colour and the 2 to coat pattern, so any other printed pair scored nothing, and its question carried a stray "C" picture label. Same ID, boundary and 8 marks; any two of the six printed features, the first correct at 6 and the second at 2.'))
    keep('q18bi', 'Q18(b)(i)')
    keep('q18bii', 'Q18(b)(ii)')
    add('q18biii', 'Q18(b)(iii)', 'Q18(b)(iii)', '4-3-3', 'genetic-engineering-in-animal-breeding',
        'Briefly describe one named method of genetic engineering you have studied and explain its importance in animal breeding.',
        [dict(menu(['Cloning', 'Genetic modification (GM)', 'Gene editing'], [2], 'Named method: 2 marks. The scheme adds "Or other valid example and explained importance".'), openList=True),
         menu(['Exact genotypic copies of living things', 'Organism whose genetic make up has been modified in a lab', 'Scientist can change or alter the DNA of an organism'], [2],
              'Description of the method named: 2 marks.'),
         menu(['To produce more meat or milk', 'research animal diseases', 'maintain superior animal characteristics', 'Increased disease resistance', 'polled animals',
               'sterile male animals', 'reduced genetic disorders passed on', 'increased productivity', 'adjust rumen function'], [2],
              'Importance in animal breeding, matching the method: 2 marks (3(2) in all). Cloning: more meat or milk, research animal diseases, maintain superior characteristics. Genetic modification and gene editing: disease resistance, polled or sterile male animals, fewer genetic disorders, productivity, research, rumen function.')],
        'In June 2023, The National Genotyping Programme was introduced to genotype the national herd.')
    add('q18c', 'Q18(c)', 'Q18(c)', '3-3-2', 'integrated-pest-management-advice',
        'Using the information shown in the diagram on IPM, advise farmers on ways they can reduce chemical inputs on their farm.',
        [point('Biological – ladybirds control aphids / ducks or geese control mud snail / dock beetle and dock leaf / cat or dog and rodent', None,
               'IPM – Preventative methods are the most important part of IPM and the use of chemicals should be a last resort. The scheme prints 6+6+4: three points, the first two at 6 marks and the third at 4.'),
         point('Physical / mechanical – fans / pulling by hand or rogueing / scorching / grazing / fleece / netting / eggshells / sticky pads / named relevant physical barrier / topping', None),
         point('Cultural / sanitation – machine hygiene / biosecurity or closed herd / correct crop storage methods', None),
         point('Prevention – crop rotation / sterile seed bed /correct sowing date / certified seed / timely harvest / resistant varieties / any minimum cultivation method / companion crop (cover crop)', None)],
        "With the EU's 'Farm to Fork Strategy' proposed to reduce by 50% the use of chemical pesticides, Integrated Pest Management (IPM) systems are becoming increasingly important. "
        'The IPM diagram is a pyramid: Prevention at the base, then Cultural / Sanitation, Physical / Mechanical, Biological, and Chemical (Pesticide) at the top.',
        marks=16, tariff={'kind': 'orderedSplit', 'notation': '6+6+4'}, figure='agsci-2024-hl-paper-ipm-pyramid', extra=('2-3',))
    assert len(tasks) == 81 and len(cards) == 18 and len(corrections) == 9 and len(originals) == 72 and len(RESTORED) == 2, (len(tasks), len(cards), len(corrections), len(originals), len(RESTORED))
    assert {t['cardIds'][0] for t in tasks} >= set(originals), 'Every original 2024 Higher card must be reviewed'
    return cards, tasks, corrections
