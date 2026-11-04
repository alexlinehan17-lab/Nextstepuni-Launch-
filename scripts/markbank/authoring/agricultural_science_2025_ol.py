"""2025 Ordinary review: the 72 original cards reconciled against the SEC sources.

All 40 paper pages and 25 scheme pages were inspected and the independent
census transcribed before any card was touched. 68 original card objects match
a published boundary and tariff and stay byte-identical (Q8(b) keeps its earlier
reviewed correction and Atlas identity). Three are corrected IN PLACE, keeping
their IDs: Q1(a)(i) becomes one any-three-of-four card listing all four
breeds, and the two cards that fused Q9(b)(i)+(ii) and (iii)+(iv) are
narrowed to (i) and (iii) because (ii) and (iv) already ship as their own cards.
Each correction records the original wording, marks and object hash plus the
SEC page and quote that justify it.
"""
import hashlib
import json
from agricultural_science_2010_hl import ROOT, point, menu, region
from agricultural_science_2010_parity import scan
from agricultural_science_2011_hl import variants

FILE = 'LC024GLP000EV.pdf'
YEAR = 2025
HASHES = {'exampapers':'481fbf4a01b2ed81472ad70745f47b2c413131939a6cc1b42cc1a16e40f458a7',
          'markingschemes':'c2170cf98ba10073a7fa35497bc54ba039f807b1985bf616f5556cd57918e624'}
SELECTIONS = {
    '4c18810fccd08db1':('exam-selection','Section A: ten of twelve independent questions. Every question and both sides of each internal choice are retained.'),
    'f9890666bf4b5f74':('exam-selection','Section B: four of six independent questions. Every question is retained.'),
    '02be49493afa8e7c':('exam-selection','Repeated Section A instruction: ten independent 10-mark questions, all retained.'),
    '90d5750e2aa45b66':('independent-task-selection','Q1 either (a) or (b): both alternatives are retained.'),
    '02e7b70e9366b1ef':('closed','Q1(a)(i) prints cattle A–D and asks for any three, 3x2. One card: a single anyN row lists every printed item with the scheme\'s wording, claim limit as printed (item-choice siblings are not separate practice identities).'),
    '54e0749a8c2f9250':('answer-identification','Q1(b)(i) "which bull ... you would advise Jack to choose": the scheme accepts Aberdeen Angus only; not a route.'),
    'b06358c53d0c52b9':('not-a-selection','Q4(c) "suited to either method of grazing": one explanation of the farm layout, not a route choice.'),
    '8a6e390f36e0a801':('closed','Q7(a) prints plants A–D and asks for any three, 3x2. One card: a single anyN row lists every printed item with the scheme\'s wording, claim limit as printed (item-choice siblings are not separate practice identities).'),
    '38c2a2684ba96ccf':('answer-identification','Q8(b): tick the two correct warning signs (already reviewed as a two-option group).'),
    '0d127836401c20be':('independent-task-selection','Q9 either (a) or (b): both alternatives are retained.'),
    'c22de058fcbf5bdd':('independent-task-selection','Q11 either (a) or (b): both alternatives are retained.'),
    '3d6d2aadcb4e0fb3':('independent-task-selection','Q12 either (a) or (b): both alternatives are retained.'),
    '01d5f968562bfc85':('exam-selection','Section B heading: four of six independent 50-mark questions, all retained.'),
    '66dc076510443757':('answer-identification','Q14(c)(i): tick the one correct minimum germination rate (85%).'),
    '9f2f2597438fe0f3':('closed','Q14(c)(iii) prints crops J, K and L and asks for any two, 2(4). One card: a single anyN row lists every printed item with the scheme\'s wording, claim limit as printed (item-choice siblings are not separate practice identities).'),
    '286650213bca37f4':('independent-task-selection','Q15: (a) and (b) with either (c) or (d). Every part, including both (c) and (d), is retained.'),
    '0c87d89efc00ea50':('independent-task-selection','Q17: (a) and (b) with either (c) or (d). Every part, including both (c) and (d), is retained.'),
    '787dc7a1aba3278c':('not-a-selection','Prose inside a Q17(b)(ii) step ("Add calcium carbonate to one of the test tubes"); no response choice.'),
}
SUPPLEMENTARY = [
    (21,'named tillage crop','open','Q14(a)(ii): the crop and its two weather conditions are student choices; the scheme table (potatoes, barley, kale) is a marking menu.'),
    (33,'For a livestock enterprise you have studied','open','Q17(d): the enterprise and its two systems are student choices; the scheme tables (beef, dairy, sheep) are marking menus.'),
    (19,'Named method:','open','Q13(b): the texture method is the student’s choice (feel, sedimentation or sieve in the scheme).'),
]
TOPIC = 'agricultural-science-ordinary-'
SNAPSHOT = ROOT / 'scripts/markbank/authored/agricultural-science-corrected-originals.json'


def original_hash(card):
    return hashlib.sha256(json.dumps(card, ensure_ascii=False, sort_keys=True).encode()).hexdigest()


def paper_review():
    observed, supplementary = scan(YEAR, FILE, HASHES, SELECTIONS, SUPPLEMENTARY)
    return dict(year=YEAR, level='ordinary', lang='ev', paperFileid=FILE, hashes=HASHES,
                wholePaperVisualReview='reviewed', schemeBoundaryReview='reviewed',
                paperPagesInspected=list(range(1, 41)), schemePagesInspected=list(range(1, 26)),
                selectionDirectives=observed, supplementarySelections=supplementary, sourceNotes=[],
                independentBoundaryReview='91 base tasks, one card each. 68 original cards match a published boundary and tariff unchanged (Q8(b) keeps its earlier reviewed correction). Three are corrected in place (Q1(a)(i) becomes one any-three-of-four card; Q9(b)(i) and (iii) separated from the parts already carded on their own); 19 cards are added, including one card each for the item-choice pools Q7(a) and Q14(c)(iii).',
                cropVisualReview='Every distinct paper/scheme crop pair rendered and inspected.',
                runtimeReview='Integrated production-component cases at 1200px and 390px. Signed-in full-app navigation remains open.',
                remaining=['Irish edition comparison (deferred)', 'Full application navigation review', 'Corpus-wide reconciliation'])


P = lambda *r: [region(*x) for x in r]
REGIONS = {
    'Q1(a)(i)': (P((3, .16, .735)), P((12, .166, .274))),
    'Q1(a)(ii)': (P((3, .16, .80)), P((12, .274, .325))),
    'Q1(b)(i)': (P((4, .093, .495)), P((12, .342, .432))),
    'Q1(b)(ii)': (P((4, .093, .12), (4, .497, .668)), P((12, .432, .481))),
    'Q1(b)(iii)': (P((4, .093, .12), (4, .674, .765)), P((12, .481, .546))),
    'Q2': (P((5, .065, .395)), P((12, .546, .694))),
    'Q3': (P((5, .40, .84)), P((12, .694, .84))),
    'Q4(a)': (P((6, .065, .60)), P((13, .085, .185))),
    'Q4(b)': (P((6, .065, .44), (6, .603, .685)), P((13, .185, .249))),
    'Q4(c)': (P((6, .065, .44), (6, .688, .86)), P((13, .249, .366))),
    'Q5(a)': (P((7, .065, .645)), P((13, .366, .491))),
    'Q5(b)': (P((7, .065, .495), (7, .644, .77)), P((13, .491, .574))),
    'Q5(c)': (P((7, .769, .885)), P((13, .574, .640))),
    'Q6(a)': (P((8, .065, .318)), P((13, .640, .706))),
    'Q6(b)': (P((8, .065, .165), (8, .318, .48)), P((13, .706, .805))),
    'Q7(a)': (P((8, .48, .777)), P((14, .084, .206))),
    'Q7(b)': (P((8, .48, .87)), P((14, .206, .254))),
    'Q8(a)': (P((9, .065, .53)), P((14, .254, .370))),
    'Q9(a)(i)': (P((10, .065, .55)), P((14, .418, .519))),
    'Q9(a)(ii)': (P((10, .065, .40), (10, .552, .78)), P((14, .524, .616))),
    'Q9(b)(i)': (P((11, .065, .40)), P((14, .634, .682))),
    'Q9(b)(ii)': (P((11, .09, .34), (11, .40, .57)), P((14, .682, .731))),
    'Q9(b)(iii)': (P((11, .09, .34), (11, .57, .63)), P((14, .731, .779))),
    'Q9(b)(iv)': (P((11, .09, .34), (11, .63, .76)), P((14, .779, .827))),
    'Q10(a)': (P((12, .065, .74)), P((15, .084, .132))),
    'Q10(b)': (P((12, .065, .74)), P((15, .132, .196))),
    'Q10(c)': (P((12, .065, .74)), P((15, .196, .296))),
    'Q11(a)(i)': (P((13, .065, .492)), P((15, .296, .345))),
    'Q11(a)(ii)': (P((13, .09, .405), (13, .466, .625)), P((15, .345, .410))),
    'Q11(a)(iii)': (P((13, .09, .405), (13, .625, .85)), P((15, .410, .508))),
    'Q11(b)(i)': (P((14, .065, .59)), P((15, .526, .643))),
    'Q11(b)(ii)': (P((14, .09, .415), (14, .59, .81)), P((15, .643, .727))),
    'Q12(a)(i)': (P((15, .065, .60)), P((16, .084, .132))),
    'Q12(a)(ii)': (P((15, .065, .635)), P((16, .132, .180))),
    'Q12(a)(iii)': (P((15, .09, .13), (15, .633, .785)), P((16, .180, .263))),
    'Q12(b)(i)': (P((16, .065, .53)), P((16, .281, .329))),
    'Q12(b)(ii)': (P((16, .09, .44), (16, .53, .625)), P((16, .329, .378))),
    'Q12(b)(iii)': (P((16, .09, .44), (16, .625, .72)), P((16, .378, .426))),
    'Q12(b)(iv)': (P((16, .09, .44), (16, .72, .82)), P((16, .426, .474))),
    'Q13(a)(i)': (P((18, .155, .56)), P((17, .151, .259))),
    'Q13(a)(ii)': (P((18, .18, .385), (18, .557, .655)), P((17, .259, .308))),
    'Q13(a)(iii)': (P((18, .18, .205), (18, .655, .745)), P((17, .308, .357))),
    'Q13(b)': (P((19, .065, .86)), P((17, .357, .760))),
    'Q13(c)(i)': (P((20, .065, .29)), P((17, .760, .809))),
    'Q13(c)(ii)': (P((20, .065, .175), (20, .29, .447)), P((17, .809, .875))),
    'Q13(c)(iii)': (P((20, .065, .175), (20, .447, .575)), P((18, .084, .151))),
    'Q13(c)(iv)': (P((20, .575, .875)), P((18, .151, .241))),
    'Q14(a)(i)': (P((21, .065, .53)), P((18, .241, .290))),
    'Q14(a)(ii)': (P((21, .53, .84)), P((18, .290, .820))),
    'Q14(a)(iii)': (P((22, .065, .21)), P((19, .084, .288))),
    'Q14(b)(i)': (P((22, .21, .41)), P((19, .288, .372))),
    'Q14(b)(ii)': (P((22, .21, .31), (22, .41, .57)), P((19, .372, .445))),
    'Q14(b)(iii)': (P((22, .21, .31), (22, .572, .815)), P((19, .445, .511))),
    'Q14(b)(iv)': (P((22, .21, .31), (23, .065, .27)), P((19, .511, .617))),
    'Q14(c)(i)': (P((23, .27, .40)), P((19, .617, .666))),
    'Q14(c)(ii)': (P((23, .27, .325), (23, .397, .555)), P((19, .666, .732))),
    'Q14(c)(iii)': (P((23, .557, .875)), P((19, .732, .825))),
    'Q15(a)(i)': (P((24, .065, .585)), P((20, .084, .192))),
    'Q15(a)(ii)': (P((24, .09, .375), (24, .585, .71)), P((20, .192, .241))),
    'Q15(a)(iii)': (P((24, .09, .375), (24, .71, .86)), P((20, .241, .307))),
    'Q15(b)(i)': (P((25, .065, .22)), P((20, .307, .391))),
    'Q15(b)(ii)': (P((25, .065, .09), (25, .217, .43)), P((20, .391, .515))),
    'Q15(b)(iii)': (P((25, .43, .88)), P((20, .515, .580))),
    'Q15(c)': (P((26, .065, .88)), P((20, .580, .715))),
    'Q15(d)(i)': (P((27, .065, .635)), P((20, .733, .782))),
    'Q15(d)(ii)': (P((27, .065, .09), (27, .635, .875)), P((20, .782, .91))),
    'Q16(a)(i)': (P((28, .065, .445)), P((21, .084, .201))),
    'Q16(a)(ii)': (P((28, .065, .12), (28, .445, .665)), P((21, .201, .355))),
    'Q16(a)(iii)': (P((28, .065, .12), (28, .665, .875)), P((21, .355, .473))),
    'Q16(b)': (P((29, .065, .85)), P((21, .473, .690))),
    'Q16(c)(i)': (P((30, .065, .235)), P((21, .690, .739))),
    'Q16(c)(ii)': (P((30, .065, .09), (30, .236, .33)), P((21, .739, .822))),
    'Q16(c)(iii)': (P((30, .065, .09), (30, .333, .505)), P((21, .822, .89))),
    'Q17(a)(i)': (P((31, .065, .345)), P((22, .04, .143))),
    'Q17(a)(ii)': (P((31, .065, .13), (31, .345, .56)), P((22, .143, .243))),
    'Q17(b)(i)': (P((31, .56, .79)), P((22, .243, .309))),
    'Q17(b)(ii)': (P((31, .56, .585), (32, .06, .64)), P((22, .309, .358))),
    'Q17(b)(iii)': (P((31, .56, .585), (32, .06, .74)), P((22, .358, .424))),
    'Q17(b)(iv)': (P((32, .06, .64), (32, .74, .80)), P((22, .424, .473))),
    'Q17(c)': (P((33, .065, .44)), P((22, .473, .625))),
    'Q17(d)': (P((33, .47, .73)), P((23, .029, .54))),
    'Q18(a)(i)': (P((34, .065, .50)), P((23, .543, .626))),
    'Q18(a)(ii)': (P((34, .09, .405), (34, .50, .585)), P((23, .626, .690))),
    'Q18(a)(iii)': (P((34, .09, .145), (34, .585, .74)), P((23, .690, .807))),
    'Q18(b)(i)': (P((35, .065, .25)), P((23, .807, .883))),
    'Q18(b)(ii)': (P((35, .065, .09), (35, .25, .56)), P((24, .03, .112))),
    'Q18(b)(iii)': (P((35, .56, .88)), P((24, .112, .212))),
    'Q18(c)(i)': (P((36, .065, .475)), P((24, .212, .280))),
    'Q18(c)(ii)': (P((36, .065, .41), (36, .475, .545)), P((24, .280, .330))),
    'Q18(c)(iii)': (P((36, .065, .09), (36, .545, .715)), P((24, .330, .434))),
}
ATLAS = {
    'Q1(a)': 'animal-production|classification-of-organisms', 'Q1(b)': 'animal-production|genetics',
    'Q2': 'animal-production|animal-diseases', 'Q3': 'crop-production|grassland', 'Q4': 'animal-production|grassland',
    'Q5(a)': 'soil-science', 'Q5(b)': 'soil-science', 'Q5(c)': 'plant-physiology|crop-production',
    'Q6': 'crop-production|fertilisers-pollution-the-environment', 'Q7': 'grassland|classification-of-organisms',
    'Q8': 'health-safety|fertilisers-pollution-the-environment', 'Q9(a)': 'animal-production|animal-physiology',
    'Q9(b)': 'animal-production|crop-production', 'Q10': 'genetics|animal-production', 'Q11(a)': 'animal-production|animal-diseases',
    'Q11(b)': 'innovation-and-biotechnology-in-agriculture|animal-production', 'Q12': 'animal-production',
    'Q13(a)': 'soil-science|scientific-practices-experiments-investigations', 'Q13(b)': 'soil-science|scientific-practices-experiments-investigations',
    'Q13(c)': 'soil-science|crop-production', 'Q14(a)': 'grassland|crop-production', 'Q14(b)': 'scientific-practices-experiments-investigations|crop-production',
    'Q14(c)': 'crop-production', 'Q15(a)': 'innovation-and-biotechnology-in-agriculture|animal-production', 'Q15(b)': 'animal-production',
    'Q15(c)': 'scientific-practices-experiments-investigations|animal-production', 'Q15(d)': 'animal-production|animal-physiology',
    'Q16(a)': 'animal-production|health-safety', 'Q16(b)': 'grassland|scientific-practices-experiments-investigations',
    'Q16(c)': 'grassland|animal-production', 'Q17(a)': 'soil-science', 'Q17(b)': 'soil-science|scientific-practices-experiments-investigations',
    'Q17(c)': 'plant-physiology|fertilisers-pollution-the-environment', 'Q17(d)': 'animal-production',
    'Q18(a)': 'animal-production', 'Q18(b)': 'animal-production|animal-physiology', 'Q18(c)': 'innovation-and-biotechnology-in-agriculture|animal-production',
}


def atlas_for(ref):
    base = ref.split(' — ')[0]
    for key in (base, base.split(')(')[0] + ')' if ')(' in base else None, base.split('(')[0]):
        if key and key in ATLAS:
            return ATLAS[key]
    raise KeyError(ref)


def reviewed_tasks(existing):
    paper_review()
    cards, tasks, corrections = [], [], {}
    originals = {cid: card for cid, card in existing.items()
                 if cid.startswith('agsci-2025-ol-') and (card.get('qa') or {}).get('humanReviewedBy') != 'agent-source-reviewed'}
    snapshot = json.loads(SNAPSHOT.read_text()) if SNAPSHOT.exists() else {}
    for cid, record in snapshot.items():
        if cid.startswith('agsci-2025-ol-'):
            originals[cid] = record['original']

    def task(cid, ref, base, selection=None, note=None):
        pp, sp = REGIONS[base]
        t = dict(questionRef='2025 OL ' + ref, paperPage=pp[0]['p'], schemePage=sp[0]['p'], paperRegions=pp, schemeRegions=sp,
                 atlasNumbers={cid: str(1002 + len(tasks))}, cardIds=[cid],
                 examTopicIds=[TOPIC + x for x in atlas_for(ref).split('|')],
                 selection=selection or {'kind': 'none', 'reason': 'Required response at a published boundary. Scheme alternatives remain marking menus.'},
                 evidence='All 40 paper and 25 scheme pages visually inspected. Boundary and tariff checked against the independently transcribed census.')
        if note:
            t['schemeNote'] = note
        tasks.append(t)
        return t

    def keep(key, ref):
        cid = 'agsci-2025-ol-' + key
        card = originals[cid]
        assert card['questionRef'] == '2025 OL ' + ref, (cid, card['questionRef'])
        t = task(cid, ref, ref)
        t['marksPerRoute'] = card['totalMarks']
        t['originalCard'] = 'unchanged'

    def add(key, ref, base, topic, concept, question, rows, stem=None, marks=None, selection=None, figure=None, labels=None, extra=(), correction=None):
        cid = 'agsci-2025-ol-' + key
        rows = [dict(row, id=f'r-{i+1}') for i, row in enumerate(rows)]
        pp, _ = REGIONS[base]
        card = dict(id=cid, subjectId='agricultural-science', year=YEAR, level='ordinary',
                    section='A' if int(base.split('(')[0][1:]) <= 12 else 'B', questionRef='2025 OL ' + ref,
                    topicId='agsci-' + topic, curriculumNodeIds=['agsci-' + t for t in (topic, *extra)],
                    conceptId=concept, questionText=question, rows=rows,
                    totalMarks=marks if marks is not None else sum(r['marks'] for r in rows),
                    tariffModel={'kind': 'questionTotal' if marks is not None else 'fixed'},
                    sourceMaterial=dict(kind='source-text', label='OFFICIAL QUESTION PAGE', title='Agricultural Science 2025 Ordinary — ' + ref,
                        pages=sorted({r['p'] for r in pp}), attribution='SEC Agricultural Science 2025 Ordinary Level examination paper — © State Examinations Commission.',
                        presentationNote='Open the original page for the published wording, photographs, tables and examination context.'))
        if extra:
            card['additionalTopicIds'] = ['agsci-' + t for t in extra]
        if stem: card['stem'] = stem
        if figure: card['figureKey'] = figure
        if labels: card['labelKey'] = labels
        t = task(cid, ref, base, selection)
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

    def closed(choose, options):
        # Item choice is ONE practice card (coordinator rule, 2026-10-12).
        return {'kind': 'closed', 'choose': choose, 'options': options, 'pooled': True}

    # Section A ---------------------------------------------------------------
    breeds = {'A': 'A: Charolais', 'B': 'B: Jersey', 'C': 'C: Limousin', 'D': 'D: Holstein Friesian'}
    meanings = {'A': 'Charolais', 'B': 'Jersey', 'C': 'Limousin', 'D': 'Holstein Friesian'}
    add('q1ai', 'Q1(a)(i)', 'Q1(a)(i)', '4-2', 'identifying-cattle-breeds-from-a-list',
        'Identify any three breeds A, B, C or D using the list below.',
        [menu(list(breeds.values()), [2, 2, 2], 'Any three of the four photographs, 2 marks each (3x2).')],
        'Word list: Jersey, Holstein Friesian, Charolais, Limousin.',
        selection=closed(3, list(breeds)), figure='agricultural-science-2025-OL-paper-p03-art',
        labels=[dict(letter=l, meaning=meanings[l], askedInThisQuestion=True) for l in breeds], extra=('4-3-2',),
        correction=('Visually verified paper PDF page 3 ("Identify any three breeds A, B, C or D using the list below", four photographs) and scheme PDF page 12 ("3x2": A Charolais, B Jersey, C Limousin, D Holstein Friesian). '
                    'The original stem was the word list run together with a stray "Or", and only A–C were decoded, with D carried as an accepted alternative. Same ID: one any-three-of-four card whose anyN row lists all four breeds, '
                    'claim limit three, with every photograph decoded and the word list as printed. Its topic moves to identification (4.2).'))
    for k, ref in [('q1aii', 'Q1(a)(ii)'), ('q1bi', 'Q1(b)(i)'), ('q1bii', 'Q1(b)(ii)'), ('q1biii', 'Q1(b)(iii)'), ('q2', 'Q2'), ('q3', 'Q3'),
                   ('q4a', 'Q4(a)'), ('q4b', 'Q4(b)'), ('q4c', 'Q4(c)')]:
        keep(k, ref)
    soil = 'The diagram shows the effect of soil composition on the productivity of a crop. Key: mineral and organic matter, soil water, soil air. Analyse the diagram and answer the questions that follow.'
    add('q5a', 'Q5(a)', 'Q5(a)', '2-2-2', 'ideal-soil-composition', 'Identify with reason which picture A, B, or C has the ideal soil composition.',
        [point('Picture: B', 3), menu(['soil has (50%) mineral and organic matter or 25% air or 25% water', 'seed can access adequate air or water or has space to grow',
                                        'adequate amounts of mineral or organic matter', 'seedling is largest in picture B'], [2], 'Reason.')], soil)
    add('q5b', 'Q5(b)', 'Q5(b)', '2-2-2', 'high-mineral-organic-soil', 'Outline one reason why soil C has a high percentage of mineral and organic matter.',
        [menu(['It is a clay soil', 'under continuous grassland', 'organic matter or manure or slurry or fertiliser has been added'], [2])], soil, extra=('2-3',))
    keep('q5c', 'Q5(c)')
    keep('q6a', 'Q6(a)')
    keep('q6b', 'Q6(b)')
    plants = {'A': 'A: (Perennial) ryegrass', 'B': 'B: (White)clover', 'C': 'C: Nettle', 'D': 'D: Chicory'}
    add('q7a', 'Q7(a)', 'Q7(a)', '3-2', 'identifying-grassland-plants',
        'Identify any three plants shown in the table below using the list opposite.',
        [menu(list(plants.values()), [2, 2, 2], 'Any three of the four photographs, 2 marks each (3x2).')],
        'List: Chicory, White clover, Perennial ryegrass, Nettle.', selection=closed(3, list(plants)))
    add('q7b', 'Q7(b)', 'Q7(b)', '3-3-2', 'undesirable-sward-plant', 'State which plant from part (a) above is not desired in a grassland sward.',
        [point('Nettle or C', 4)], 'Part (a) shows A (perennial) ryegrass, B (white) clover, C nettle and D chicory.', extra=('3-2',))
    keep('q8a', 'Q8(a)')
    add('q9ai', 'Q9(a)(i)', 'Q9(a)(i)', '4-1', 'calf-birth-position', 'Identify with reason which picture A or B is the correct position for a calf at birth.',
        [point('Picture: B', 3), point('Fore or front legs first (with head lying flat on top of legs) or normal presentation or easier calving', 2, 'Reason.')],
        'The pictures below show calves presented in various positions leading up to birth.', extra=('4-3-3',))
    keep('q9aii', 'Q9(a)(ii)')
    index = ('The picture shows the Agricultural Price Index for 12 months up to March 2024.\nChanges in Agricultural Input Price: Electricity down 22% · Fertilisers down 40% · Feedstuffs down 21%\n'
             'Changes in Agricultural Output Price: Sheep up 30% · Cereals down 31% · Milk down 5%')
    add('q9bi-ii', 'Q9(b)(i)', 'Q9(b)(i)', '1-3', 'agricultural-input-price-index', 'State if the input prices have increased or decreased.',
        [point('Decreased', 3, 'All three input prices in the index fell.')], index, figure='agricultural-science-2025-OL-paper-p11-i0',
        correction=('Visually verified paper PDF page 11 ("(i) State if the input prices have increased or decreased." and "(ii) Identify what your answer in part (i) above means for farmers") and scheme PDF page 14 ((i) "Decreased" 3; (ii) "Costs less to produce" 2). '
                    'The original fused (i) and (ii) into one 5-mark card while (ii) also ships as agsci-2025-ol-q9bii, so (ii) was carded twice. This ID keeps part (i) at its published 3 marks.'))
    keep('q9bii', 'Q9(b)(ii)')
    add('q9biii-iv', 'Q9(b)(iii)', 'Q9(b)(iii)', '1-3', 'agricultural-output-price-index', 'Which agricultural enterprise’s output price has increased?',
        [point('Sheep', 3, 'Sheep is the only output price up (30%); cereals and milk both fell.')], index, figure='agricultural-science-2025-OL-paper-p11-i0',
        correction=('Visually verified paper PDF page 11 ("(iii) Which agricultural enterprise’s output price has increased?") and scheme PDF page 14 ((iii) "Sheep" 3; (iv) "Increased profit" 2). '
                    'The original fused (iii) and (iv) into one 5-mark card while (iv) also ships as agsci-2025-ol-q9biv. This ID keeps part (iii) at its published 3 marks; its source-page binding is replaced by the card’s own source.'))
    keep('q9biv', 'Q9(b)(iv)')
    sexing = 'The diagram shows the process of sex sorting bull semen. Analyse the picture and answer the questions that follow.'
    add('q10a', 'Q10(a)', 'Q10(a)', '4-1', 'sex-sorted-semen-cell', 'Identify the sex cell labelled A.', [point('Sperm or male', 3)], sexing,
        figure='agricultural-science-2025-OL-paper-p12-i0', labels=[dict(letter='A', meaning='Sperm or male', askedInThisQuestion=True)], extra=('4-3-2',))
    keep('q10b', 'Q10(b)')
    keep('q10c', 'Q10(c)')
    for k, ref in [('q11ai', 'Q11(a)(i)'), ('q11aii', 'Q11(a)(ii)'), ('q11aiii', 'Q11(a)(iii)'), ('q11bi', 'Q11(b)(i)'), ('q11bii', 'Q11(b)(ii)')]:
        keep(k, ref)
    mortality = 'The graph shows the main causes of lamb mortality (death) on Irish sheep farms: chill and starvation 30%, abortion and stillbirth 40%, disease (bar not drawn), accidents and predators 5%, birth defects 5%.'
    add('q12ai', 'Q12(a)(i)', 'Q12(a)(i)', '4-3-3', 'lamb-mortality-cause', 'Identify the main cause of lamb mortality.', [point('Abortion and stillbirth', 3)], mortality, extra=('1-3',))
    add('q12aii', 'Q12(a)(ii)', 'Q12(a)(ii)', '1-4', 'completing-a-bar-chart', 'Complete the graph above to show that 20% of lambs die due to disease.',
        [point('Bar inserted in graph to height of 20', 2, kind='criterion')], mortality, extra=('4-3-3',))
    keep('q12aiii', 'Q12(a)(iii)')
    growth = ('The graph shows the lamb growth rate and weight of two lambs on Lucy’s farm. Single lamb: birth 5 kg, then 16.5, 27.5, 35, 42.5 and 50 kg at weeks 5–25. '
              'Twin lamb: birth 4.5 kg, then 14, 23.5, 29.5, 37 and 44.5 kg.')
    add('q12bi', 'Q12(b)(i)', 'Q12(b)(i)', '4-3-2', 'lamb-growth-rate', 'Identify which lamb (single or twin) had a higher growth rate over the 25 weeks.', [point('Single', 3)], growth, extra=('1-3',))
    keep('q12bii', 'Q12(b)(ii)')
    add('q12biii', 'Q12(b)(iii)', 'Q12(b)(iii)', '4-3-2', 'lamb-slaughter-weight-prediction', 'Predict which lamb will have a higher weight at slaughter.', [point('Single', 3)], growth, extra=('1-3',))
    keep('q12biv', 'Q12(b)(iv)')
    # Section B ---------------------------------------------------------------
    for k, ref in [('q13ai', 'Q13(a)(i)'), ('q13a-ii', 'Q13(a)(ii)'), ('q13a-iii', 'Q13(a)(iii)'), ('q13b', 'Q13(b)'), ('q13c-i', 'Q13(c)(i)'),
                   ('q13c-ii', 'Q13(c)(ii)'), ('q13c-iii', 'Q13(c)(iii)'), ('q13c-iv', 'Q13(c)(iv)'), ('q14a-i', 'Q14(a)(i)')]:
        keep(k, ref)
    crops = {
        'potatoes': ('Potatoes', ['Frost free warm soil temperatures needed for development of tubers', 'Warm temperatures improve germination and establishment'],
                     ['Heavy rainfall may delay the planting of the potato crop', 'heavy rainfall may reduce tuber size or increase disease susceptibility or cause crop failure', 'precipitation is crucial for tuber development and yield']),
        'barley': ('Barley', ['Cold temperatures can delay germination', 'Warm temperatures improve germination and establishment'],
                   ['Heavy rainfall can reduce % germination', 'heavy rainfall can lead to decreased yield or crop failure', 'drought can reduce yield or lead to crop failure']),
        'kale': ('Kale', ['Frost may damage new seedlings', 'kale tolerates cooler temperatures (winter crop)', 'Warm temperatures improve germination and establishment'],
                 ['Heavy rainfall can lead to decreased yield or mineral content', 'drought can reduce yield or lead to crop failure']),
    }
    def weather_rows(name, temp, rain):
        return [menu(['Temperature', 'Precipitation'], [2, 2], f'Named tillage crop: {name}. Two named weather conditions, 2(2).'),
                menu(temp + rain, [3, 2], 'One matching impact for each named condition, 3+2: the first options are temperature impacts, the rest precipitation impacts. (accept valid weather condition with matching valid impact)')]
    c = add('q14a-ii', 'Q14(a)(ii)', 'Q14(a)(ii)', '3-3-1', 'weather-and-tillage-planting', 'Explain the impacts of two named weather conditions on the planting of a named tillage crop.',
            weather_rows(*crops['potatoes']), 'The graph shows the average monthly soil temperatures in Ballyhaise Agricultural College, Co. Cavan for 2023.', extra=('2-3',))
    variants(c, [(k, name, weather_rows(name, temp, rain)) for k, (name, temp, rain) in crops.items()])
    keep('q14a-iii', 'Q14(a)(iii)')
    for k, ref in [('q14b-i', 'Q14(b)(i)'), ('q14b-ii', 'Q14(b)(ii)'), ('q14b-iii', 'Q14(b)(iii)'), ('q14b-iv', 'Q14(b)(iv)'), ('q14c-i', 'Q14(c)(i)'), ('q14c-ii', 'Q14(c)(ii)')]:
        keep(k, ref)
    tillage = {'J': 'J: Maize', 'K': 'K: Wheat', 'L': 'L: Oilseed rape'}
    add('q14ciii', 'Q14(c)(iii)', 'Q14(c)(iii)', '3-2', 'identifying-tillage-crops',
        'The photographs below J, K and L show three common crops grown in Ireland. Identify any two of these crops, using the following list.',
        [menu(list(tillage.values()), [4, 4], 'Any two of the three photographs, 4 marks each (2(4)).')], 'List: Maize, Oilseed rape, Wheat.',
        selection=closed(2, list(tillage)), extra=('3-3-1',))
    for k, ref in [('q15a-i', 'Q15(a)(i)'), ('q15a-ii', 'Q15(a)(ii)'), ('q15a-iii', 'Q15(a)(iii)'), ('q15b-i', 'Q15(b)(i)'), ('q15b-ii', 'Q15(b)(ii)'), ('q15b-iii', 'Q15(b)(iii)'), ('q15c', 'Q15(c)')]:
        keep(k, ref)
    add('q15di', 'Q15(d)(i)', 'Q15(d)(i)', '4-3-2', 'calf-nutrition-order',
        'The photographs below show four stages of calf nutrition from birth to six weeks old. Place each step in the correct order by matching the correct letter to the number in the box.',
        [menu(['D', 'A', 'B', 'C'], [2, 2, 2, 2], 'Correct order: D – A – B - C (calf fed colostrum, calves on milk replacer, calf on hay, calf on grass). The scheme prints 4x2.')],
        'A: Calves on milk replacer. B: Calf on hay. C: Calf on grass. D: Calf fed colostrum.')
    keep('q15d-ii', 'Q15(d)(ii)')
    add('q16ai', 'Q16(a)(i)', 'Q16(a)(i)', '4-3-3', 'beef-housing-features', 'Identify three things that make the housing in the photograph suitable for beef animals.',
        [menu('Slatted floor|rubber mats|natural lighting|straw bedding|adequate space in pens|(adequate) feeding space|good ventilation|high roof for good air circulation|headlock gates|pen gates', [4, 4, 2])],
        'Winter months can be hard on beef farms due to harsh weather conditions.')
    keep('q16aii', 'Q16(a)(ii)')
    keep('q16aiii', 'Q16(a)(iii)')
    keep('q16b', 'Q16(b)')
    add('q16ci', 'Q16(c)(i)', 'Q16(c)(i)', '3-3-3', 'silage-dry-matter-percentage',
        'The DM% of typical forage crops is shown below in the table. Identify which DM% represents Tom’s silage, by placing a tick (✓) in the correct box.',
        [point('25%', 6, 'The scheme accepts 25%.')], 'Options: 25%, 45%, 65%.', extra=('4-3-2',))
    keep('q16cii', 'Q16(c)(ii)')
    keep('q16ciii', 'Q16(c)(iii)')
    for k, ref in [('q17ai', 'Q17(a)(i)'), ('q17aii', 'Q17(a)(ii)'), ('q17bi', 'Q17(b)(i)')]:
        keep(k, ref)
    add('q17bii', 'Q17(b)(ii)', 'Q17(b)(ii)', '1-2', 'flocculation-investigation-order',
        'Describe how a student would show that flocculation has occurred in a soil by arranging the steps of the investigation shown below in the correct order.',
        [menu(['D', 'A', 'B', 'C'], [4, 4, 4, 4], 'Correct order: D - A - B - C (add clay soil to two test tubes; add calcium carbonate to one; add water, stopper and shake; leave to settle). The scheme prints 4x4.')],
        'A: Add calcium carbonate to one of the test tubes. B: Add water to each test tube, then stopper and shake the test tubes. C: Leave to settle, one test tube stays muddy, while one test tube goes clear. D: Add clay soil to two test tubes.',
        extra=('2-2-2',))
    keep('q17biii', 'Q17(b)(iii)')
    keep('q17biv', 'Q17(b)(iv)')
    keep('q17c', 'Q17(c)')
    enterprises = {
        'beef': ('Beef', [('1: Calf to beef', 'Friesian or Friesian X Hereford / Aberdeen Angus or Hereford', 'Easy calving'),
                          ('2: Suckler beef', 'Limousin or Charolais or Simmental', 'Good conformation / good LWG')]),
        'dairy': ('Dairy', [('1: Liquid milk', 'Holstein Friesian', 'High milk volume'), ('2: Creamery milk', 'Jersey', 'High milk solids')]),
        'sheep': ('Sheep', [('1: Mountain sheep', 'Blackface mountain or Wicklow cheviot', 'Good mothering ability / hardy'),
                            ('2: Lowland sheep', 'Suffolk or Texel', 'Fast growth rates / good conformation')]),
    }
    def system_rows(systems):
        rows = []
        for name, breed, reason in systems:
            rows += [point(breed, 3, f'{name}: breed of dam. Named breed must be linked to the choice; or other valid example.'), point(reason, 3, f'{name}: reason for choice.')]
        return rows
    c = add('q17d', 'Q17(d)', 'Q17(d)', '4-3-1', 'production-systems-dam-breeds',
            'For a livestock enterprise you have studied state two different named systems of production. For each system identify a suitable breed of dam (female) and explain a reason for your choice.',
            system_rows(enterprises['beef'][1]), extra=('4-2',))
    variants(c, [(k, label, system_rows(systems)) for k, (label, systems) in enterprises.items()])
    for k, ref in [('q18ai', 'Q18(a)(i)'), ('q18aii', 'Q18(a)(ii)'), ('q18aiii', 'Q18(a)(iii)'), ('q18bi', 'Q18(b)(i)'), ('q18bii', 'Q18(b)(ii)'), ('q18biii', 'Q18(b)(iii)')]:
        keep(k, ref)
    exports = 'The graph below shows Irish Dairy Exports for 2015 and 2021 (Bord Bia, 2024): cheese, butter, infant food, milk and cream, skim milk powder, in tonnes.'
    add('q18ci', 'Q18(c)(i)', 'Q18(c)(i)', '1-3', 'dairy-export-decrease', 'Identify the dairy product which decreased in exports between 2015 and 2021.',
        [point('Infant food', 6)], exports, extra=('4-3-1',))
    add('q18cii', 'Q18(c)(ii)', 'Q18(c)(ii)', '1-3', 'butter-export-estimate', 'Using the graph, estimate the value of Irish butter exports to Ireland in 2021.',
        [point('265,000 to 275,000', 6)], exports, extra=('4-3-1',))
    keep('q18ciii', 'Q18(c)(iii)')
    assert len(tasks) == 90 and len(cards) == 22 and len(corrections) == 3 and len(originals) == 71, (len(tasks), len(cards), len(corrections), len(originals))
    assert {t['cardIds'][0] for t in tasks} | {'agsci-2025-ol-q8b'} >= set(originals) | {'agsci-2025-ol-q8b'}, 'Every original 2025 Ordinary card must be reviewed'
    return cards, tasks, corrections
