"""2025 Higher review: the 88 original cards reconciled against the SEC sources.

All 44 paper pages and 25 scheme pages were inspected and the independent
census transcribed before any card was touched. 78 original card objects
match a published task boundary and tariff and are left byte-identical; they
only gain an Atlas binding and an inspected official source page. Ten original
cards are corrected IN PLACE, keeping their IDs (and saved progress): where an
unexpanded printed pool becomes routes, the original card becomes the first
printed route; Q12 becomes its any-four-of-five 2(4)+2(1) scale and Q14(b)(i)
regains the published result mark. Each correction records the original
wording, marks and object hash plus the SEC page and quote that justify it.
"""
import hashlib
import json
from itertools import combinations
from agricultural_science_2010_hl import ROOT, point, menu, region
from agricultural_science_2010_parity import scan
from agricultural_science_2011_hl import variants

FILE = 'LC024ALP000EV.pdf'
YEAR = 2025
HASHES = {'exampapers':'5d6ace875795ceeed7f7738b6c137a17f62e7247be067b540907afa71f9880f0',
          'markingschemes':'47f040304b88a81e2c6de9783dc71914ac5863ea80416a280cf242c64014ba6d'}
SELECTIONS = {
    '1f08be7d0bf08721':('exam-selection','Section A: ten of twelve independent questions. Every question and both sides of each internal choice are retained.'),
    'ae168e9a0c211b77':('exam-selection','Section B: four of six independent questions. Every question is retained.'),
    '4d0e9772893bc740':('exam-selection','Repeated Section A instruction: ten independent 10-mark questions, all retained.'),
    '82944548c2c72701':('independent-task-selection','Q2 either (a) or (b): both independently marked alternatives are retained.'),
    '6cfb3ad3b6d6408b':('closed','Q2(a) prints annual, biennial and perennial and asks for any two: three routes at 10 marks each.'),
    '2e6cd11be874308c':('closed','Q2(b)(ii) "Choose" any two of five printed characteristics: ten routes at 2 marks each.'),
    '9ab2b0c47cfe5005':('closed','Second regex match in the same Q2(b)(ii) instruction ("any two"); the same ten routes.'),
    '4090a61f0e3cfda9':('independent-task-selection','Q3 either (a) or (b): both alternatives are retained.'),
    '9e6f5de3f3c38902':('independent-task-selection','Q4 either (a) or (b): both alternatives are retained.'),
    '980037ae98923503':('closed','Q6(b): any one of the three lambing tools identified in part (a); the scheme prints one description per tool, so three 4-mark routes.'),
    'a00923023b1eed61':('open','Q7(a): any two components of the soil microbiome; no printed pool, the scheme examples are a marking menu.'),
    '6cd6108e84f08878':('closed','Q7(b): any one of the four printed processes; four 5-mark routes, each with its own contribution and benefit.'),
    '57ae0134389e1d7a':('independent-task-selection','Q9 either (a) or (b): both alternatives are retained.'),
    '4303f26dc3d09f03':('not-a-selection','Prose in the Q11 stem ("one of the best"); no response choice.'),
    '00fdc88683e221c4':('closed','Q12: any four of five printed prompts under one 2(4)+2(1) scale; five 10-mark routes.'),
    '9fcb3888322d99ac':('exam-selection','Section B heading: four of six independent 50-mark questions, all retained.'),
    '145c11c431516d76':('independent-task-selection','Q13: (a) and (b) with either (c) or (d). Every part, including both (c) and (d), is retained.'),
    'b79207c595ecd897':('independent-task-selection','Q14: (a) and (b) with either (c) or (d). Every part, including both (c) and (d), is retained.'),
    'f937232b4d54fbc3':('open','Q15(a)(ii): characteristics for "any two parent plants" the student selects; no printed pool of plants.'),
    '708d97ce6238b64b':('closed','Q15(b): any three of four printed photographs A–D; four 3-mark routes.'),
}
SUPPLEMENTARY = [
    (11,'Identify the three pieces of equipment','answer-identification','Q6(a): the three correct pieces among six photographs (A, C and D); the distractors are not routes.'),
    (34,'Identify two inaccurate pieces of information','answer-identification','Q16(c)(i): find two of the three inaccuracies printed in the AI paragraph; identifying correct answers is not a route choice.'),
    (13,'and / or','open','Q8(a): flexible animal and/or crop production wording; one response.'),
    (38,'List with reason three types of plants','open','Q18(a)(i): student-chosen plants; the scheme table is a marking menu.'),
    (30,'under the following','required-condition','Q15(c): three required headings, one point under each and the fourth from any heading.'),
]
SOURCE_NOTES = {
    'q14bi':'The scheme prints 4x4 for four method points and a separate 1 mark for “*Result: valid result for investigation described”. This part totals 17, which Question 14 needs to total 50.',
}
TOPIC = 'agricultural-science-higher-'
SNAPSHOT = ROOT / 'scripts/markbank/authored/agricultural-science-corrected-originals.json'


def original_hash(card):
    return hashlib.sha256(json.dumps(card, ensure_ascii=False, sort_keys=True).encode()).hexdigest()


def paper_review():
    observed, supplementary = scan(YEAR, FILE, HASHES, SELECTIONS, SUPPLEMENTARY)
    notes = [dict(questionN='14', questionRef='Q14(b)(i)', note=SOURCE_NOTES['q14bi'])]
    return dict(year=YEAR, level='higher', lang='ev', paperFileid=FILE, hashes=HASHES,
                wholePaperVisualReview='reviewed', schemeBoundaryReview='reviewed',
                paperPagesInspected=list(range(1, 45)), schemePagesInspected=list(range(1, 26)),
                selectionDirectives=observed, supplementarySelections=supplementary, sourceNotes=notes,
                independentBoundaryReview='89 base tasks and 112 routes. 78 original cards match a published boundary and tariff unchanged. Ten are corrected in place (Q2(a), Q2(b)(ii), Q6(b), Q12(a)–(e), Q14(b)(i), Q15(b)); 24 cards are added: missing Q1(b), Q3(a)(ii), Q6(a), Q7(b) (four routes) and Q15(c), plus the remaining printed routes of Q2(a), Q2(b)(ii), Q6(b) and Q15(b).',
                cropVisualReview='Every distinct paper/scheme crop pair rendered and inspected.',
                runtimeReview='Integrated production-component cases at 1200px and 390px. Signed-in full-app navigation remains open.',
                remaining=['Irish edition comparison (deferred)', 'Full application navigation review', 'Corpus-wide reconciliation'])


# Paper / scheme crop regions for every base task (original cards included).
P = lambda *r: [region(*x) for x in r]
REGIONS = {
    'Q1(a)': (P((3, .155, .52)), P((12, .136, .209))),
    'Q1(b)': (P((3, .155, .45), (3, .52, .58)), P((12, .209, .273))),
    'Q1(c)': (P((3, .52, .556), (3, .592, .62)), P((12, .273, .322))),
    'Q2(a)': (P((4, .065, .20)), P((12, .322, .462))),
    'Q2(b)(i)': (P((5, .09, .35), (5, .355, .45)), P((12, .482, .545))),
    'Q2(b)(ii)': (P((5, .09, .35), (5, .45, .54)), P((12, .545, .795))),
    'Q2(b)(iii)': (P((5, .09, .35), (5, .75, .78)), P((12, .795, .856))),
    'Q3(a)(i)': (P((6, .09, .455)), P((13, .085, .181))),
    'Q3(a)(ii)': (P((6, .09, .112), (6, .632, .672)), P((13, .181, .268))),
    'Q3(b)(i)': (P((7, .09, .47)), P((13, .286, .406))),
    'Q3(b)(ii)': (P((7, .09, .43), (7, .665, .69)), P((13, .406, .489))),
    'Q4(a)(i)': (P((8, .065, .253)), P((13, .489, .580))),
    'Q4(a)(ii)': (P((8, .065, .20), (8, .498, .523)), P((13, .580, .681))),
    'Q4(a)(iii)': (P((8, .065, .20), (8, .652, .69)), P((13, .681, .78))),
    'Q4(b)(i)': (P((9, .09, .305)), P((14, .102, .151))),
    'Q4(b)(ii)': (P((9, .09, .305), (9, .31, .335)), P((14, .151, .199))),
    'Q4(b)(iii)': (P((9, .09, .305), (9, .404, .43)), P((14, .199, .265))),
    'Q4(b)(iv)': (P((9, .09, .305), (9, .528, .554)), P((14, .265, .313))),
    'Q5(a)': (P((10, .065, .188)), P((14, .313, .396))),
    'Q5(b)': (P((10, .065, .188), (10, .314, .372)), P((14, .396, .605))),
    'Q5(c)': (P((10, .065, .188), (10, .443, .63)), P((14, .605, .75))),
    'Q6(a)': (P((11, .065, .665)), P((15, .084, .151))),
    'Q6(b)': (P((11, .065, .113), (11, .666, .71)), P((15, .151, .299))),
    'Q7(a)': (P((12, .065, .138)), P((15, .299, .347))),
    'Q7(b)': (P((12, .065, .113), (12, .208, .595)), P((15, .347, .80))),
    'Q8(a)': (P((13, .065, .15)), P((16, .084, .235))),
    'Q9(a)': (P((14, .065, .172)), P((16, .235, .353))),
    'Q9(b)(i)': (P((14, .065, .132), (15, .09, .355)), P((16, .371, .435))),
    'Q9(b)(ii)': (P((14, .065, .132), (15, .09, .31), (15, .43, .466)), P((16, .435, .499))),
    'Q9(b)(iii)': (P((14, .065, .132), (15, .572, .596)), P((16, .499, .582))),
    'Q10(a)': (P((16, .065, .39)), P((16, .582, .665))),
    'Q10(b)': (P((16, .065, .37), (16, .52, .562)), P((16, .665, .826))),
    'Q11(a)': (P((17, .065, .32)), P((17, .084, .218))),
    'Q11(b)': (P((17, .065, .27), (17, .603, .627)), P((17, .218, .283))),
    'Q12': (P((18, .065, .114), (18, .117, .14), (18, .274, .298), (18, .432, .455), (18, .589, .612), (18, .716, .74)), P((17, .283, .62))),
    'Q13(a)(i)': (P((21, .155, .41)), P((18, .137, .254))),
    'Q13(a)(ii)': (P((21, .155, .37), (21, .548, .615)), P((18, .254, .328))),
    'Q13(a)(iii)': (P((21, .548, .636)), P((18, .328, .394))),
    'Q13(a)(iv)': (P((21, .155, .37), (21, .734, .76)), P((18, .394, .502))),
    'Q13(a)(v)': (P((21, .155, .37), (22, .065, .09)), P((18, .502, .617))),
    'Q13(a)(vi)': (P((21, .155, .25), (22, .282, .306)), P((18, .617, .666))),
    'Q13(a)(vii)': (P((21, .155, .25), (22, .346, .37)), P((18, .666, .749))),
    'Q13(b)(i)': (P((22, .56, .61)), P((18, .749, .815))),
    'Q13(b)(ii)': (P((22, .56, .585), (22, .71, .752)), P((18, .815, .90))),
    'Q13(b)(iii)': (P((22, .56, .585), (23, .065, .09)), P((19, .084, .167))),
    'Q13(c)(i)': (P((23, .28, .632)), P((19, .167, .215))),
    'Q13(c)(ii)': (P((23, .28, .595), (23, .67, .695)), P((19, .215, .265))),
    'Q13(d)(i)': (P((24, .09, .535)), P((19, .281, .330))),
    'Q13(d)(ii)': (P((24, .09, .50), (24, .603, .63)), P((19, .330, .396))),
    'Q14(a)(i)': (P((25, .065, .352)), P((19, .396, .503))),
    'Q14(a)(ii)': (P((25, .355, .812)), P((19, .503, .594))),
    'Q14(a)(iii)': (P((25, .355, .75), (26, .062, .09)), P((19, .594, .693))),
    'Q14(b)(i)': (P((26, .189, .236)), P((19, .693, .89))),
    'Q14(b)(ii)': (P((26, .189, .236), (27, .065, .165)), P((20, .085, .217))),
    'Q14(b)(iii)': (P((26, .189, .236), (27, .20, .226)), P((20, .217, .317))),
    'Q14(c)': (P((27, .415, .44)), P((20, .317, .470))),
    'Q14(d)': (P((27, .655, .68)), P((20, .488, .553))),
    'Q15(a)(i)': (P((28, .09, .418)), P((20, .553, .644))),
    'Q15(a)(ii)': (P((28, .09, .13), (28, .609, .65)), P((20, .644, .743))),
    'Q15(a)(iii)': (P((29, .065, .59)), P((20, .743, .87))),
    'Q15(a)(iv)': (P((29, .59, .755)), P((21, .084, .207))),
    'Q15(b)': (P((30, .065, .28)), P((21, .207, .345))),
    'Q15(c)': (P((30, .283, .91)), P((21, .345, .80))),
    'Q16(a)(i)': (P((32, .09, .358)), P((22, .084, .133))),
    'Q16(a)(ii)': (P((32, .09, .33), (32, .432, .456)), P((22, .133, .182))),
    'Q16(a)(iii)': (P((32, .09, .33), (32, .529, .555)), P((22, .182, .319))),
    'Q16(a)(iv)': (P((32, .09, .33), (32, .759, .785)), P((22, .319, .368))),
    'Q16(a)(v)': (P((32, .09, .13), (33, .065, .09)), P((22, .368, .417))),
    'Q16(a)(vi)': (P((32, .09, .13), (33, .192, .216)), P((22, .417, .465))),
    'Q16(b)': (P((32, .09, .33), (33, .41, .47)), P((22, .465, .563))),
    'Q16(c)(i)': (P((34, .065, .346)), P((22, .563, .650))),
    'Q16(c)(ii)': (P((34, .065, .32), (34, .471, .495)), P((22, .650, .748))),
    'Q16(c)(iii)': (P((34, .065, .32), (34, .617, .64)), P((22, .748, .831))),
    'Q16(c)(iv)': (P((34, .065, .32), (34, .744, .782)), P((22, .831, .915))),
    'Q17(a)(i)': (P((35, .09, .425)), P((23, .084, .133))),
    'Q17(a)(ii)': (P((35, .09, .40), (35, .527, .55)), P((23, .133, .182))),
    'Q17(a)(iii)': (P((35, .09, .13), (35, .59, .615)), P((23, .182, .298))),
    'Q17(a)(iv)': (P((35, .09, .13), (36, .065, .102)), P((23, .298, .397))),
    'Q17(a)(v)': (P((35, .09, .13), (36, .291, .333)), P((23, .397, .479))),
    'Q17(b)(i)': (P((36, .455, .496)), P((23, .479, .580))),
    'Q17(b)(ii)': (P((36, .455, .478), (36, .736, .76)), P((23, .580, .681))),
    'Q17(c)(i)': (P((37, .065, .248)), P((23, .681, .839))),
    'Q17(c)(ii)': (P((37, .065, .248), (37, .794, .817)), P((23, .839, .905))),
    'Q18(a)(i)': (P((38, .09, .14)), P((24, .084, .278))),
    'Q18(a)(ii)': (P((38, .09, .114), (38, .405, .43)), P((24, .278, .462))),
    'Q18(a)(iii)': (P((38, .09, .114), (38, .689, .715)), P((24, .462, .545))),
    'Q18(b)': (P((39, .065, .106)), P((24, .545, .661))),
    'Q18(c)(i)': (P((40, .065, .09)), P((24, .661, .727))),
    'Q18(c)(ii)': (P((40, .22, .262)), P((24, .727, .882))),
}
# Atlas topics, read from each task's content (SEC-derived, not copied).
ATLAS = {
    'Q1': 'beef-cattle|classification-of-animals-plants', 'Q1(b)': 'beef-cattle|genetics', 'Q1(c)': 'beef-cattle|genetics',
    'Q2(a)': 'crop-production|classification-of-animals-plants', 'Q2(b)': 'beef-cattle|dairy-cattle',
    'Q3': 'innovation-and-biotechnology-in-agriculture', 'Q4': 'animal-diseases', 'Q5': 'beef-cattle',
    'Q6': 'sheep', 'Q7(a)': 'soil-science', 'Q7(b)': 'soil-science|energy-crop-catch-crop',
    'Q8': 'fertilisers-pollution-environment-cycles|soil-science', 'Q9': 'soil-science|crop-production',
    'Q9(a)': 'soil-science|scientific-practices-experiments-investigations', 'Q10': 'sheep|genetics',
    'Q11': 'innovation-and-biotechnology-in-agriculture', 'Q13': 'dairy-cattle', 'Q13(a)(i)': 'dairy-cattle|beef-cattle',
    'Q13(c)': 'dairy-cattle|animal-physiology-reproductive-systems', 'Q13(d)': 'dairy-cattle|animal-physiology-reproductive-systems',
    'Q14': 'soil-science', 'Q14(b)': 'soil-science|scientific-practices-experiments-investigations',
    'Q15(a)': 'genetics|crop-production', 'Q15(b)': 'classification-of-animals-plants', 'Q15(c)': 'crop-production',
    'Q16(a)': 'beef-cattle|dairy-cattle', 'Q16(b)': 'beef-cattle', 'Q16(c)': 'grassland|innovation-and-biotechnology-in-agriculture',
    'Q17(a)': 'sheep', 'Q17(b)': 'sheep', 'Q17(c)': 'crop-production|energy-crop-catch-crop',
    'Q18(a)': 'grassland', 'Q18(b)': 'grassland|scientific-practices-experiments-investigations', 'Q18(c)': 'crop-production',
}
Q12_ITEMS = {
    'a': ('Progeny testing in dairy cows.', 'To assess the genetic merit (traits or characteristics) of a breeding animal through their offspring', '4-3-2', 'dairy-cattle|genetics'),
    'b': ('Having a buffer zone close to a waterway.', 'Reduce run off or prevent eutrophication / reduce sediment in rivers / increased bank stability / increased biodiversity', '2-3', 'fertilisers-pollution-environment-cycles'),
    'c': ('Presence of chloroplasts in the palisade layer of a leaf.', 'Close to surface to maximise photosynthesis', '3-1', 'plant-physiology'),
    'd': ('Culling of breeding ewes on a sheep farm.', 'Ewe could be lame or infertile or diseased or prevent undesirable traits (so is not suitable for breeding)', '4-3-1', 'sheep'),
    'e': ('Movement of water from the soil through the plant to the atmosphere.', 'To transport minerals / to provide water for photosynthesis / to cool the plant', '3-1', 'plant-physiology'),
}
# Each original part card becomes the four-part route that begins at that
# part in cyclic printed order, so every legacy ID keeps its own prompt.
Q12_LEGACY = {'a': 'abcd', 'b': 'bcde', 'c': 'acde', 'd': 'abde', 'e': 'abce'}
LIFECYCLES = {
    'Annual': ('Completes its life cycle in one year', 'wheat'),
    'Biennial': ('Completes its life cycle in two years', 'carrot'),
    'Perennial': ('Flower and reproduce for multiple years', 'perennial ryegrass'),
}
CHARACTERISTICS = {
    'Meat quality': ['Factors relating to marbling or texture or taste or tenderness (that appeal to consumers)', 'many cows go into calf to beef system so improved beef traits'],
    'Good growth rates': ['Will influence when an animal gets to slaughter and kill out weight (fast maturing)'],
    'Ease of calving': ['Reduced risk of complications', 'better suited for crossing with dairy cows rather than bigger continental breeds'],
    'Docility': ['Animals with good temperament are easier to handle', 'less risk of injury'],
    'Fertility': ['greater number of calves over lifetime of bull'],
}
TOOLS = {
    'Stomach tube': 'Tube is placed into stomach through oesophagus to deliver milk to stomach',
    'Heat lamp': 'The heat lamp is placed above the lamb',
    'Ropes': 'Ropes are tied above the hooves of lambs to pull lamb during birth',
}
PROCESSES = {
    'Water retention': (['(Mycorrhizal fungi) increase area for water absorption', '(bacteria and fungi) break down OM to humus which increase water retention', 'improves soil structure'],
                        ['Increased water availability to the crop', 'reduces effects of drought']),
    'Plant carbon sink': (['Micro-organisms feed on OM and allow for nutrient recycling (store carbon) in soil (biomass or humus)'], ['Greater nutrient availability for crop growth']),
    'Carbon sequestration': (['Decomposition of OM to humus for carbon storage in soil'], ['Improved soil structure for crop growth or greater nutrient availability for crop growth']),
    'Plant growth promotion': (['Symbiotic relationship (between plants and mycorrhizal fungi/bacteria) fixes nitrogen or makes phosphate available', 'mycorrhizal fungi produce growth hormones'],
                               ['Improved nutrient availability leading to improved yield', 'improved yield due to growth hormones']),
}
PLANTS = {'A': 'Cleavers', 'B': 'Chicory', 'C': 'Silverweed', 'D': 'Oilseed rape'}


def atlas_for(ref):
    for key in (ref.split(' — ')[0], ref.split(' — ')[0].split(')(')[0] + ')' if ')(' in ref else None, ref.split('(')[0]):
        if key and key in ATLAS:
            return ATLAS[key]
    raise KeyError(ref)


def opts(row):
    return menu(row, [1]) if len(row) > 1 else None


def reviewed_tasks(existing):
    """existing: {id: card} from the authored file (originals are read, never rewritten unless corrected)."""
    paper_review()
    cards, tasks, corrections = [], [], {}
    # Original cards carry no review stamp; cards this review wrote do. The
    # corrected originals come from their frozen snapshot, never the file.
    originals = {cid: card for cid, card in existing.items()
                 if cid.startswith('agsci-2025-hl-') and (card.get('qa') or {}).get('humanReviewedBy') != 'agent-source-reviewed'}
    snapshot = json.loads(SNAPSHOT.read_text()) if SNAPSHOT.exists() else {}
    for cid, record in snapshot.items():
        if cid.startswith('agsci-2025-hl-'):
            originals[cid] = record['original']

    def task(cid, ref, base, selection=None, examTopics=None, note=None):
        pp, sp = REGIONS[base]
        t = dict(questionRef='2025 HL ' + ref, paperPage=pp[0]['p'], schemePage=sp[0]['p'], paperRegions=pp, schemeRegions=sp,
                 atlasNumbers={cid: str(1001 + len(tasks))}, cardIds=[cid],
                 examTopicIds=[TOPIC + t for t in (examTopics or atlas_for(ref)).split('|')],
                 selection=selection or {'kind': 'none', 'reason': 'Required response at a published boundary. Scheme alternatives remain marking menus.'},
                 evidence='All 44 paper and 25 scheme pages visually inspected. Boundary and tariff checked against the independently transcribed census.')
        if note:
            t['schemeNote'] = note
        tasks.append(t)
        return t

    def keep(key, ref, examTopics=None):
        cid = 'agsci-2025-hl-' + key
        card = originals[cid]
        assert card['questionRef'] == '2025 HL ' + ref, (cid, card['questionRef'])
        t = task(cid, ref, ref, examTopics=examTopics)
        t['marksPerRoute'] = card['totalMarks']
        t['originalCard'] = 'unchanged'

    def add(key, ref, base, topic, concept, question, rows, stem=None, marks=None, selection=None, figure=None, labels=None,
            extra=(), examTopics=None, correction=None, extra_fields=None):
        cid = 'agsci-2025-hl-' + key
        rows = [dict(row, id=f'r-{i+1}') for i, row in enumerate(rows)]
        pp, _ = REGIONS[base]
        card = dict(id=cid, subjectId='agricultural-science', year=YEAR, level='higher',
                    section='A' if int(base.split('(')[0][1:]) <= 12 else 'B', questionRef='2025 HL ' + ref,
                    topicId='agsci-' + topic, curriculumNodeIds=['agsci-' + t for t in (topic, *extra)],
                    conceptId=concept, questionText=question, rows=rows,
                    totalMarks=marks if marks is not None else sum(r['marks'] for r in rows),
                    tariffModel={'kind': 'questionTotal' if marks is not None else 'fixed'},
                    sourceMaterial=dict(kind='source-text', label='OFFICIAL QUESTION PAGE', title='Agricultural Science 2025 Higher — ' + ref,
                        pages=sorted({r['p'] for r in pp}), attribution='SEC Agricultural Science 2025 Higher Level examination paper — © State Examinations Commission.',
                        presentationNote='Open the original page for the published wording, photographs, tables and examination context.'))
        if extra:
            card['additionalTopicIds'] = ['agsci-' + t for t in extra]
        if stem: card['stem'] = stem
        if figure: card['figureKey'] = figure
        if labels: card['labelKey'] = labels
        if extra_fields: card.update(extra_fields)
        note = SOURCE_NOTES.get(key)
        if note:
            rows[0]['contextNote'] = (rows[0].get('contextNote', '') + ' ' + note).strip()
        t = task(cid, ref, base, selection, examTopics, note)
        t['marksPerRoute'] = card['totalMarks']
        if correction:
            old = originals[cid]
            corrections[cid] = dict(originalSha256=original_hash(old), originalQuestionRef=old['questionRef'],
                                    originalQuestionText=old['questionText'], originalTotalMarks=old['totalMarks'],
                                    originalTariffModel=old['tariffModel'], reason=correction)
            t['originalCard'] = 'corrected-in-place'
        else:
            assert cid not in originals, f'{cid} would replace an original card without a correction record'
            t['originalCard'] = 'added'
        cards.append(card)
        return card

    def closed(choose, options, route):
        return {'kind': 'closed', 'choose': choose, 'options': options, 'route': route}

    # Section A ---------------------------------------------------------------
    keep('q1a', 'Q1(a)')
    add('q1b', 'Q1(b)', 'Q1(b)', '4-2', 'polled-breed', 'State which breed A or B has a dominant polled trait as a characteristic of the breed.',
        [point('A or Aberdeen Angus', 2)], 'Photographs A and B show two cattle breeds (part (a): identify both cattle breeds in A and B).', extra=('4-3-2',))
    keep('q1c', 'Q1(c)')
    life = list(LIFECYCLES)
    q2a_stem = 'Plant lifecycles can be distinguished as annual, biennial and perennial.'
    for chosen in combinations(life, 2):
        key = 'q2a' if chosen == ('Annual', 'Biennial') else 'q2a-route-' + '-'.join(c.lower() for c in chosen)
        rows = []
        for name in chosen:
            expl, example = LIFECYCLES[name]
            rows += [point(expl, 3, f'{name}: explanation.'),
                     dict(point(example, 2, f'Example of a {name.lower()} plant. (Any other valid example of a plant)'), openList=True)]
        add(key, 'Q2(a) — ' + ', '.join(chosen), 'Q2(a)', '3-2', 'plant-lifecycles',
            'Explain any two plant lifecycles and provide an example of each one.', rows,
            q2a_stem + ' Practice choice: ' + ', '.join(chosen) + '.', selection=closed(2, life, list(chosen)), extra=('3-1',),
            correction=('Visually verified paper PDF page 4 ("Explain any two plant lifecycles and provide an example of each one" beside the printed annual/biennial/perennial table) '
                        'and scheme PDF page 12 ("(3+2) + (3+2)"). The printed any-two-of-three pool expands into three routes; this ID becomes the first printed route, Annual and Biennial, with the published 10-mark tariff.')
                       if key == 'q2a' else None)
    keep('q2bi', 'Q2(b)(i)')
    wagyu = ('Japanese Wagyu beef is renowned for its superior marbling. A new Wagyu beef cross programme aims to process 150 head of cattle weekly in Ireland. '
             'Bull sires are selected on meat quality, good growth rates, ease of calving, docility and fertility. (Adapted from Independent.ie, 2024)')
    chars = list(CHARACTERISTICS)
    for chosen in combinations(chars, 2):
        key = 'q2bii' if chosen == ('Meat quality', 'Good growth rates') else 'q2bii-route-' + '-'.join(c.lower().replace(' ', '-') for c in chosen)
        rows = [menu(CHARACTERISTICS[c], [1], f'{c}: one description.') if len(CHARACTERISTICS[c]) > 1 else point(CHARACTERISTICS[c][0], 1, f'{c}: description.') for c in chosen]
        add(key, 'Q2(b)(ii) — ' + ', '.join(chosen), 'Q2(b)(ii)', '4-3-2', 'beef-cross-sire-selection',
            'Choose any two characteristics of the Wagyu breed from the list below and describe how each of your chosen characteristics makes the breed suitable for crossing with dairy cows.',
            rows, wagyu + ' Practice choice: ' + ', '.join(chosen) + '.', selection=closed(2, chars, list(chosen)), extra=('4-3-1',),
            correction=('Visually verified paper PDF page 5 ("Choose any two characteristics of the Wagyu breed from the list below", five printed characteristics) and scheme PDF page 12 ("1+1", one description per characteristic). '
                        'The printed two-of-five pool expands into ten routes; this ID becomes the first printed route, Meat quality and Good growth rates, at the published 2 marks.')
                       if key == 'q2bii' else None)
    keep('q2biii', 'Q2(b)(iii)')
    keep('q3ai', 'Q3(a)(i)')
    add('q3aii', 'Q3(a)(ii)', 'Q3(a)(ii)', '4-3-1', 'technology-environmental-sustainability',
        'In relation to environmental sustainability, briefly describe the advantages of one other named piece of farm technology you have studied.',
        [point('Two points on any named valid piece of technology relating to environmental sustainability', None,
               'The scheme prints 3+1: the first valid advantage earns 3 marks and the second 1. The technology is the student’s own choice.', kind='criterion')],
        'Cow brushes on dairy farms are becoming increasingly popular.', marks=4, extra=('2-3',))
    keep('q3bi', 'Q3(b)(i)')
    keep('q3bii', 'Q3(b)(ii)')
    for k, ref in [('q4ai', 'Q4(a)(i)'), ('q4aii', 'Q4(a)(ii)'), ('q4aiii', 'Q4(a)(iii)'), ('q4bi', 'Q4(b)(i)'), ('q4bii', 'Q4(b)(ii)'),
                   ('q4biii', 'Q4(b)(iii)'), ('q4biv', 'Q4(b)(iv)'), ('q5a', 'Q5(a)'), ('q5b', 'Q5(b)'), ('q5c', 'Q5(c)')]:
        keep(k, ref)
    lamb = 'Pádraig is a sheep and beef farmer. He is getting his equipment ready for lambing.'
    add('q6a', 'Q6(a)', 'Q6(a)', '4-3-3', 'lambing-equipment-identification', 'Identify the three pieces of equipment needed for lambing from the six images below.',
        [menu(['Stomach tube', 'heat lamp', 'ropes'], [1, 1, 1], 'Names: one mark for each correct piece of equipment named.'),
         menu(['A: Stomach tube', 'C: heat lamp', 'D: ropes'], [1, 1, 1], 'Identified: one mark for each correct photograph matched to its equipment. The scheme prints 3x1 (names) and 3x1 (identified).')],
        lamb, extra=('4-2',))
    tools = list(TOOLS)
    for name in tools:
        key = 'q6b' if name == 'Stomach tube' else 'q6b-route-' + name.lower().replace(' ', '-')
        add(key, f'Q6(b) — {name}', 'Q6(b)', '4-3-3', 'lambing-equipment-use',
            'Briefly describe how any one of your named pieces of equipment identified in part (a) above is used during the lambing period.',
            [point(TOOLS[name], 4, f'{name}.')], lamb + f' Part (a): the three pieces of lambing equipment are a stomach tube, a heat lamp and ropes. Practice choice: {name}.',
            selection=closed(1, tools, [name]),
            correction=('Visually verified paper PDF page 11 ("Briefly describe how any one of your named pieces of equipment identified in part (a)") and scheme PDF page 15 (one description each for stomach tube, heat lamp and ropes, 4 marks). '
                        'The one-of-three choice expands into three routes; this ID becomes the first printed route, Stomach tube.') if key == 'q6b' else None)
    keep('q7a', 'Q7(a)')
    procs = list(PROCESSES)
    for name in procs:
        contrib, benefit = PROCESSES[name]
        add('q7b-route-' + name.lower().replace(' ', '-'), f'Q7(b) — {name}', 'Q7(b)', '2-2-3', 'soil-microbiome-processes',
            'Outline how the soil microbiome contributes to any one of the above processes and state how this process in turn benefits productivity in a named catch or energy crop.',
            [menu(contrib, [4], f'{name}: contribution of the soil microbiome.') if len(contrib) > 1 else point(contrib[0], 4, f'{name}: contribution of the soil microbiome.'),
             menu(benefit, [1], 'Benefit to productivity in a named catch or energy crop. The scheme prints 4+1.') if len(benefit) > 1 else point(benefit[0], 1, 'Benefit to productivity in a named catch or energy crop. The scheme prints 4+1.')],
            'The soil microbiome plays a large role in soil health. The diagram shows four processes carried out by the soil microbiome: water retention, plant carbon sink, carbon sequestration and plant growth promotion. Practice choice: ' + name + '.',
            selection=closed(1, procs, [name]), extra=('3-3-2',))
    keep('q8a', 'Q8(a)')
    for k, ref in [('q9a', 'Q9(a)'), ('q9bi', 'Q9(b)(i)'), ('q9bii', 'Q9(b)(ii)'), ('q9biii', 'Q9(b)(iii)'), ('q10a', 'Q10(a)'), ('q10b', 'Q10(b)'), ('q11a', 'Q11(a)'), ('q11b', 'Q11(b)')]:
        keep(k, ref)
    letters = list(Q12_ITEMS)
    for legacy, route in Q12_LEGACY.items():
        items = [Q12_ITEMS[l] for l in route]
        ordered = list(route[route.index(legacy):] + route[:route.index(legacy)])
        assert sorted(route) == list(route)
        topics = list(dict.fromkeys(Q12_ITEMS[l][2] for l in ordered))
        add('q12' + legacy, 'Q12 — ' + ', '.join(route), 'Q12', topics[0], 'scientific-reasons-' + route,
            'Outline one scientific reason for any four of the following: (a) Progeny testing in dairy cows. (b) Having a buffer zone close to a waterway. (c) Presence of chloroplasts in the palisade layer of a leaf. (d) Culling of breeding ewes on a sheep farm. (e) Movement of water from the soil through the plant to the atmosphere.',
            [menu([Q12_ITEMS[l][1] for l in route], [4, 4, 1, 1],
                  'One reason for each of your four prompts, in order: ' + ' '.join(f'({l}) {Q12_ITEMS[l][0]}' for l in route)
                  + ' Alternatives within one prompt earn one award. The scheme prints 2(4)+2(1): the first two correct reasons earn 4 marks each and the next two 1 each.')],
            'Practice choice: ' + ', '.join(f'({l})' for l in route) + '.', selection=closed(4, letters, list(route)), extra=tuple(topics[1:]),
            examTopics='|'.join(dict.fromkeys(t for l in route for t in Q12_ITEMS[l][3].split('|'))),
            correction=(f'Visually verified paper PDF page 18 ("Outline one scientific reason for any four of the following", five prompts (a)–(e)) and scheme PDF page 17 (one "2(4)+2(1)" tariff for the whole question). '
                        f'The original carded each prompt as a separate 2-mark task, which matches neither the 10-mark question nor its first-correct scale. Q12 is one any-four-of-five task: five 10-mark routes. '
                        f'This ID, originally prompt ({legacy}), becomes the route that begins at ({legacy}) in cyclic printed order, ({") (".join(ordered)}), so its own prompt stays on the card.'
                        + (' Its topic moves from crop establishment (3.3.1) to soil management (2.3): a buffer zone protects water quality from run-off.' if legacy == 'b' else '')))
    # Section B ---------------------------------------------------------------
    for k, ref in [('q13ai', 'Q13(a)(i)'), ('q13aii', 'Q13(a)(ii)'), ('q13aiii', 'Q13(a)(iii)'), ('q13aiv', 'Q13(a)(iv)'), ('q13av', 'Q13(a)(v)'),
                   ('q13avi', 'Q13(a)(vi)'), ('q13avii', 'Q13(a)(vii)'), ('q13bi', 'Q13(b)(i)'), ('q13bii', 'Q13(b)(ii)'), ('q13biii', 'Q13(b)(iii)'),
                   ('q13ci', 'Q13(c)(i)'), ('q13cii', 'Q13(c)(ii)'), ('q13di', 'Q13(d)(i)'), ('q13dii', 'Q13(d)(ii)'),
                   ('q14ai', 'Q14(a)(i)'), ('q14aii', 'Q14(a)(ii)'), ('q14aiii', 'Q14(a)(iii)')]:
        keep(k, ref)
    methods = ['Put cotton wool or muslin cloth in open end of one tube (and place in retort stand)', 'obtain dry soil sample and compact one half of the sample',
               'place equal amounts of compacted soil in open end of the tubes and uncompacted soil in the other open-ended tube',
               'place both tubes in equal amounts of water', 'leave for a suitable valid time', 'measure or observe the level of water in each tube', 'other valid method']
    add('q14bi', 'Q14(b)(i)', 'Q14(b)(i)', '1-2', 'capillarity-compacted-vs-uncompacted',
        'Compare, with the aid of a labelled diagram, the capillarity of a compacted and uncompacted soil. State the results of this investigation.',
        [menu(methods, [4, 4, 4, 4], 'Four method points from one coherent investigation, 4x4.'),
         point('*Result: valid result for investigation described', 1, 'Result (compulsory, *): 1 mark.', kind='criterion')],
        'The picture shows crop growth in compacted and uncompacted soil. Part (b) is an investigation you carry out yourself; the labelled diagram is one you draw.', extra=('2-2-2',),
        correction=('Visually verified paper PDF page 26 ("Compare, with the aid of a labelled diagram, the capillarity of a compacted and uncompacted soil. State the results of this investigation") '
                    'and scheme PDF page 19 ("4x4" for the method and "1" for "*Result: valid result for investigation described"). The original totalled 16 and omitted the published result mark; '
                    'Question 14 totals 50 only with 17. Same ID; the method menu and the result criterion now total 17.'))
    keep('q14bii', 'Q14(b)(ii)')
    keep('q14biii', 'Q14(b)(iii)')
    keep('q14c', 'Q14(c)')
    keep('q14d', 'Q14(d)')
    for k, ref in [('q15ai', 'Q15(a)(i)'), ('q15aii', 'Q15(a)(ii)'), ('q15aiii', 'Q15(a)(iii)'), ('q15aiv', 'Q15(a)(iv)')]:
        keep(k, ref)
    plant_letters = list(PLANTS)
    for chosen in combinations(plant_letters, 3):
        key = 'q15b' if chosen == ('A', 'B', 'C') else 'q15b-route-' + ''.join(chosen).lower()
        add(key, 'Q15(b) — ' + ', '.join(chosen), 'Q15(b)', '3-2', 'identifying-common-farm-weeds',
            'Identify any three common plants found on Irish farms in the photographs below.',
            [point(f'{l}: {PLANTS[l]}', 1, f'Photograph {l}.') for l in chosen],
            'Practice choice: photographs ' + ', '.join(chosen) + '.', selection=closed(3, plant_letters, list(chosen)), extra=('3-1',),
            figure='agricultural-science-2025-HL-paper-p30-art',
            labels=[dict(letter=l, meaning=PLANTS[l], askedInThisQuestion=l in chosen) for l in plant_letters],
            correction=('Visually verified paper PDF page 30 ("Identify any three common plants found on Irish farms in the photographs below", photographs A–D) and scheme PDF page 21 ("3x1": A Cleavers, B Chicory, C Silverweed, D Oilseed rape). '
                        'The printed three-of-four pool expands into four routes; this ID becomes the first printed route, A, B and C. Its topic moves from plant physiology to identification (3.2), where weed identification sits.')
                       if key == 'q15b' else None)
    headings = {
        'types': ('Types of weed control', ['Crop rotation to reduce the build-up of weeds', 'correct seeding rate to increase competition',
                  'spray the field with pre-harvest or pre-emergence herbicides to reduce the weeds in the crop', 'ensure the machines are cleaned between fields to reduce weed seeds being carried',
                  'valid named biological control e.g. dock beetle to control dock leaves', 'stubble cleaning – depth of cultivation to target specific weeds', 'any valid qualified description of a point from diagram']),
        'negative': ('Negative effects of weed control on farms', ['Herbicides can kill non-target plants', 'reduced biodiversity', 'residues from herbicides in human or animal food chain',
                     'chemical run off into waterways', 'herbicide resistance in weeds']),
        'safety': ('Safety considerations farmers need to take into account when controlling weeds', ['Wear masks when spraying or wear gloves', 'take precaution when operating machinery', 'avoid drift', 'correct storage of chemicals']),
    }
    def heading_rows(extra_key):
        rows = [menu(pool, [4, 4] if k == extra_key else [4], label + ('. Two points from this heading in this allocation.' if k == extra_key else '.')) for k, (label, pool) in headings.items()]
        rows[0]['contextNote'] += ' (One point under each heading and the fourth point from any heading). 4x4.'
        return rows
    c = add('q15c', 'Q15(c)', 'Q15(c)', '3-3-2', 'weed-control-advice',
        'You have been asked to address a group of tillage and dairy farmers on controlling weeds on their farms in order to maximise crop productivity. Using the diagram below, outline the advice you would give them under the following headings: types of weed control; negative effects of weed control on farms; safety considerations farmers need to consider when controlling weeds.',
        heading_rows('types'), extra=('1-5',))
    variants(c, [(k, 'Fourth point under: ' + label, heading_rows(k)) for k, (label, _) in headings.items()])
    for k, ref in [('q16ai', 'Q16(a)(i)'), ('q16aii', 'Q16(a)(ii)'), ('q16aiii', 'Q16(a)(iii)'), ('q16aiv', 'Q16(a)(iv)'), ('q16av', 'Q16(a)(v)'),
                   ('q16avi', 'Q16(a)(vi)'), ('q16b', 'Q16(b)'), ('q16ci', 'Q16(c)(i)'), ('q16cii', 'Q16(c)(ii)'), ('q16ciii', 'Q16(c)(iii)'), ('q16civ', 'Q16(c)(iv)'),
                   ('q17ai', 'Q17(a)(i)'), ('q17aii', 'Q17(a)(ii)'), ('q17aiii', 'Q17(a)(iii)'), ('q17aiv', 'Q17(a)(iv)'), ('q17av', 'Q17(a)(v)'),
                   ('q17bi', 'Q17(b)(i)'), ('q17bii', 'Q17(b)(ii)'), ('q17ci', 'Q17(c)(i)'), ('q17cii', 'Q17(c)(ii)'),
                   ('q18ai', 'Q18(a)(i)'), ('q18aii', 'Q18(a)(ii)'), ('q18aiii', 'Q18(a)(iii)'), ('q18b', 'Q18(b)'), ('q18ci', 'Q18(c)(i)'), ('q18cii', 'Q18(c)(ii)')]:
        keep(k, ref)
    assert len(tasks) == 112 and len(cards) == 34 and len(corrections) == 10 and len(originals) == 88, (len(tasks), len(cards), len(corrections), len(originals))
    assert {t['cardIds'][0] for t in tasks} >= set(originals), 'Every original 2025 Higher card must be reviewed'
    return cards, tasks, corrections
