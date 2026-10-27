"""2024 Ordinary review: the 77 original cards reconciled against the SEC sources.

All 40 paper pages and 26 scheme pages were inspected and the independent
census transcribed before any card was touched. 74 original card objects match
a published task boundary and tariff and are left byte-identical; they only
gain an Atlas binding and an inspected official source page. The printed item
choices (Q5(a), Q6(a)(i), Q6(a)(ii), Q7(a), Q13(a)(ii)) are already one card
each that lets any printed choice score. Three originals are corrected IN
PLACE, keeping their IDs: Q2(b)(iii) loses a stem of diagram-label soup, and
Q14(c)(ii) and Q14(d) regain the published per-name, per-description and
per-cell awards that their combined rows had made all-or-nothing. Five cards
are added for parts the deck lacked. Each correction records the original
wording, marks and object hash plus the SEC page that justifies it.
"""
import copy
import hashlib
import json
from agricultural_science_2010_hl import ROOT, point, menu, region
from agricultural_science_2010_parity import scan

FILE = 'LC024GLP000EV.pdf'
YEAR = 2024
HASHES = {'exampapers':'dfdcb939847873c973368e2d59e01a1b9420a160d187398e4fed01131c273275',
          'markingschemes':'b728e72363e7d7b7123f38884f637fcfad73adf2e32c6aaf57dce95eae52690e'}
KEPT_ONE_CARD = ' The original one-card form already lets any printed choice score, so it is kept unchanged (item-choice siblings are not separate practice identities).'
SELECTIONS = {
    'f20ee9787884d6ee':('exam-selection','Instructions: Section A, ten of twelve independent questions. Every question and both sides of each internal choice are retained.'),
    '377a00c3ba8ea2cd':('exam-selection','Instructions: Section B, four of six independent questions. Every question is retained.'),
    'ae7e26ead376acf7':('exam-selection','Repeated Section A instruction: ten independent 10-mark questions, all retained.'),
    'f53c880b06b4d0ba':('independent-task-selection','Q2 either (a) or (b): both independently marked alternatives are retained.'),
    '72605f73bb19c4b3':('closed','Q5(a): label any three of the four lettered stomach parts, 3(2).' + KEPT_ONE_CARD),
    'dcf430b417ad8fe4':('independent-task-selection','Q6 either (a) or (b): both alternatives are retained.'),
    'db8c5487f0a8935f':('closed','Q6(a)(i): identify any three of the four sheep breeds A–D, 3(2).' + KEPT_ONE_CARD),
    '7a495caeee110e18':('closed','Q7(a): any three of the four printed soil-compaction headings, 3(2).' + KEPT_ONE_CARD),
    '9851e46935218bd6':('open','Q8(a): any three advantages of jackets framed by four printed headings; the scheme marks one pool of advantages, not a pool per heading, so the headings are not answer routes.'),
    '40981c6586dd4843':('independent-task-selection','Q9 either (a) or (b): both alternatives are retained.'),
    'b3c8d3bbf76a7542':('not-a-selection','Text inside the Q11(a) flowchart ("Choose the best offspring and breed"); no response choice.'),
    'f048f0379636bf19':('independent-task-selection','Q11 either (a) or (b): both alternatives are retained.'),
    '21fc1411c480cdfc':('answer-identification','Q11(b)(ii): state which cow, A or B, to choose; one correct answer (B), not a route.'),
    '01b2b759eebc6ee1':('exam-selection','Section B heading: four of six independent 50-mark questions, all retained.'),
    '151e5877fd6cd086':('not-a-selection','Prose in the Q13(a) stem ("One of the areas Lisa decided to investigate"); no response choice.'),
    '2c775fcd995a6bd2':('closed','Q13(a)(ii): identify any three of the four plants A–D, 3(4).' + KEPT_ONE_CARD),
    '86eb3a30d4e75f80':('independent-task-selection','Q15: (a) and (b) with either (c) or (d). Every part, including both (c) and (d), is retained.'),
    '95305b1ad7da523c':('independent-task-selection','Q18: (a) and (b) with either (c) or (d). Every part, including both (c) and (d), is retained.'),
}
SUPPLEMENTARY = [
    (8,'Outline one reason why any named breed in part (i) above is suitable for sheep meat','closed','Q6(a)(ii): one of the four printed breeds, 4 marks.' + KEPT_ONE_CARD),
    (32,'Based on a named food crop (other than grass) you have studied','open','Q17(b)(i): a student-named crop; barley, potatoes and kale are the scheme\'s worked examples ("or another valid crop").'),
    (11,'Briefly explain how one piece of technology you have studied','open','Q8(b): a student-chosen technology; the scheme adds "any other valid answer".'),
    (12,'State two agricultural practices which contribute to water pollution','open','Q9(b): student-chosen practices; the scheme\'s four practices are a marking menu.'),
    (3,'in the correct box below to show the direction of grazing','answer-identification','Q1(a): one correct direction box.'),
    (21,'Identify the most suitable chart or graph to display the above results','answer-identification','Q13(b)(iii): one correct chart (B).'),
]
TOPIC = 'agricultural-science-ordinary-'
SNAPSHOT = ROOT / 'scripts/markbank/authored/agricultural-science-corrected-originals.json'
PREFIX = 'agsci-2024-ol-'


def original_hash(card):
    return hashlib.sha256(json.dumps(card, ensure_ascii=False, sort_keys=True).encode()).hexdigest()


def paper_review():
    observed, supplementary = scan(YEAR, FILE, HASHES, SELECTIONS, SUPPLEMENTARY)
    return dict(year=YEAR, level='ordinary', lang='ev', paperFileid=FILE, hashes=HASHES,
                wholePaperVisualReview='reviewed', schemeBoundaryReview='reviewed',
                paperPagesInspected=list(range(1, 41)), schemePagesInspected=list(range(1, 27)),
                selectionDirectives=observed, supplementarySelections=supplementary, sourceNotes=[],
                independentBoundaryReview='82 base tasks, one card each. 74 original cards match a published boundary and tariff unchanged; the item choices Q5(a), Q6(a)(i), Q6(a)(ii), Q7(a) and Q13(a)(ii) are already one card each. Three are corrected in place (Q2(b)(iii) stem; Q14(c)(ii) and Q14(d) awards); five cards are added for the missing Q1(a), Q11(a)(ii), Q13(b)(iii), Q14(a)(ii) and Q14(b)(i).',
                cropVisualReview='Every distinct paper/scheme crop pair rendered and inspected.',
                runtimeReview='Integrated production-component cases at 1200px and 390px. Signed-in full-app navigation remains open.',
                remaining=['Irish edition comparison (deferred)', 'Full application navigation review', 'Corpus-wide reconciliation'])


# Paper / scheme crop regions for every base task (original cards included).
P = lambda *r: [region(*x) for x in r]
Q1 = (3, .16, .462)
Q2B = (5, .09, .355)
REGIONS = {
    'Q1(a)': (P((3, .16, .578)), P((12, .137, .195))),
    'Q1(b)': (P(Q1, (3, .578, .60)), P((12, .195, .243))),
    'Q1(c)': (P(Q1, (3, .647, .67)), P((12, .243, .291))),
    'Q1(d)': (P(Q1, (3, .711, .733)), P((12, .291, .374))),
    'Q2(a)': (P((4, .065, .79)), P((12, .374, .500))),
    'Q2(b)(i)': (P((5, .065, .38)), P((12, .516, .581))),
    'Q2(b)(ii)': (P(Q2B, (5, .423, .446)), P((12, .581, .682))),
    'Q2(b)(iii)': (P(Q2B, (5, .550, .59)), P((12, .682, .763))),
    'Q2(b)(iv)': (P((5, .695, .735)), P((12, .763, .846))),
    'Q3': (P((6, .065, .39)), P((13, .085, .253))),
    'Q4': (P((6, .41, .80)), P((13, .253, .372))),
    'Q5(a)': (P((7, .065, .535)), P((13, .372, .472))),
    'Q5(b)': (P((7, .065, .133), (7, .681, .82)), P((13, .472, .566))),
    'Q6(a)(i)': (P((8, .065, .64)), P((13, .566, .666))),
    'Q6(a)(ii)': (P((8, .065, .16), (8, .639, .705)), P((13, .666, .840))),
    'Q6(b)(i)': (P((9, .07, .445)), P((14, .085, .168))),
    'Q6(b)(ii)': (P((9, .09, .42), (9, .551, .573)), P((14, .168, .233))),
    'Q6(b)(iii)': (P((9, .09, .42), (9, .678, .70)), P((14, .233, .351))),
    'Q7(a)': (P((10, .065, .29)), P((14, .351, .537))),
    'Q7(b)': (P((10, .065, .13), (10, .587, .83)), P((14, .537, .598))),
    'Q8(a)': (P((11, .065, .42)), P((14, .598, .714))),
    'Q8(b)': (P((11, .065, .115), (11, .705, .745)), P((14, .714, .797))),
    'Q9(a)(i)': (P((12, .065, .21)), P((15, .085, .133))),
    'Q9(a)(ii)': (P((12, .065, .148, 0, .61), (12, .267, .29, 0, .61)), P((15, .133, .183))),
    'Q9(a)(iii)': (P((12, .065, .148, 0, .61), (12, .364, .49)), P((15, .183, .258))),
    'Q9(b)': (P((12, .496, .62)), P((15, .258, .530))),
    'Q10(a)': (P((13, .065, .225)), P((15, .530, .614))),
    'Q10(b)': (P((13, .065, .18), (13, .324, .46)), P((15, .614, .752))),
    'Q10(c)(i)': (P((13, .464, .725)), P((15, .752, .805))),
    'Q10(c)(ii)': (P((13, .464, .66), (13, .724, .765)), P((15, .805, .854))),
    'Q11(a)(i)': (P((14, .065, .56)), P((16, .085, .133))),
    'Q11(a)(ii)': (P((14, .065, .52), (14, .615, .64)), P((16, .133, .181))),
    'Q11(a)(iii)': (P((14, .12, .18), (14, .682, .85)), P((16, .181, .270))),
    'Q11(b)(i)': (P((15, .07, .40)), P((16, .288, .370))),
    'Q11(b)(ii)': (P((15, .09, .37), (15, .534, .75)), P((16, .370, .452))),
    'Q12(a)': (P((16, .065, .636)), P((16, .452, .567))),
    'Q12(b)': (P((16, .065, .133), (16, .636, .67)), P((16, .567, .650))),
    'Q13(a)(i)': (P((19, .16, .30)), P((17, .145, .281))),
    'Q13(a)(ii)': (P((20, .065, .44)), P((17, .281, .382))),
    'Q13(b)(i)': (P((20, .562, .81)), P((17, .382, .469))),
    'Q13(b)(ii)': (P((20, .562, .785), (21, .065, .09)), P((17, .469, .534))),
    'Q13(b)(iii)': (P((21, .222, .434)), P((17, .534, .738))),
    'Q13(b)(iv)': (P((21, .435, .46)), P((17, .738, .846))),
    'Q14(a)(i)': (P((22, .065, .18)), P((18, .085, .168))),
    'Q14(a)(ii)': (P((22, .065, .13), (22, .313, .523)), P((18, .168, .328))),
    'Q14(a)(iii)': (P((22, .065, .13), (22, .525, .55)), P((18, .328, .371))),
    'Q14(b)(i)': (P((22, .648, .87)), P((18, .371, .522))),
    'Q14(b)(ii)': (P((22, .648, .87), (23, .065, .09)), P((18, .522, .588))),
    'Q14(b)(iii)': (P((22, .648, .87), (23, .19, .32)), P((18, .588, .664))),
    'Q14(c)(i)': (P((23, .323, .37)), P((18, .664, .851))),
    'Q14(c)(ii)': (P((23, .323, .345), (24, .065, .09)), P((19, .085, .453))),
    'Q14(d)': (P((24, .347, .655)), P((19, .453, .580))),
    'Q15(a)(i)': (P((25, .065, .44)), P((20, .085, .175))),
    'Q15(a)(ii)': (P((25, .442, .80)), P((20, .175, .245))),
    'Q15(b)(i)': (P((26, .065, .11)), P((20, .245, .309))),
    'Q15(b)(ii)': (P((26, .24, .41)), P((20, .309, .355))),
    'Q15(b)(iii)': (P((26, .24, .29), (26, .413, .53)), P((20, .355, .423))),
    'Q15(b)(iv)': (P((26, .536, .845)), P((20, .423, .494))),
    'Q15(c)(i)': (P((27, .065, .21)), P((20, .494, .565))),
    'Q15(c)(ii)': (P((27, .215, .24)), P((20, .565, .631))),
    'Q15(d)': (P((27, .413, .45)), P((20, .631, .715))),
    'Q16(a)(i)': (P((28, .065, .15)), P((21, .085, .150))),
    'Q16(a)(ii)': (P((28, .09, .115), (28, .245, .27)), P((21, .150, .216))),
    'Q16(a)(iii)': (P((28, .09, .115), (28, .402, .71)), P((21, .216, .324))),
    'Q16(a)(iv)': (P((28, .09, .115), (28, .711, .735)), P((21, .324, .407))),
    'Q16(b)': (P((29, .065, .11)), P((21, .407, .545))),
    'Q16(c)(i)': (P((30, .065, .155)), P((21, .545, .680))),
    'Q16(c)(ii)': (P((30, .065, .125), (30, .309, .35)), P((21, .680, .744))),
    'Q16(c)(iii)': (P((30, .065, .125), (30, .394, .48)), P((21, .744, .848))),
    'Q17(a)(i)': (P((31, .065, .40)), P((22, .085, .184))),
    'Q17(a)(ii)': (P((31, .09, .352), (31, .509, .53)), P((22, .184, .249))),
    'Q17(a)(iii)': (P((31, .633, .68)), P((22, .249, .477))),
    'Q17(b)(i)': (P((32, .065, .16)), P((22, .477, .853))),
    'Q17(b)(ii)': (P((32, .065, .10), (32, .478, .50)), P((23, .085, .429))),
    'Q17(b)(iii)': (P((32, .065, .10), (32, .754, .775)), P((23, .429, .495))),
    'Q17(c)': (P((33, .065, .75)), P((23, .495, .650))),
    'Q18(a)(i)': (P((34, .065, .20)), P((24, .085, .201))),
    'Q18(a)(ii)': (P((34, .09, .135), (34, .472, .495)), P((24, .201, .284))),
    'Q18(a)(iii)': (P((34, .629, .84)), P((24, .284, .334))),
    'Q18(b)': (P((35, .065, .36)), P((24, .334, .474))),
    'Q18(c)': (P((35, .372, .45)), P((24, .474, .555))),
    'Q18(d)': (P((35, .671, .84)), P((24, .555, .718))),
}
# Atlas topics, read from each task's content (SEC-derived, not copied).
ATLAS = {
    'Q1': 'grassland', 'Q2(a)': 'health-safety|crop-production', 'Q2(b)': 'animal-production|health-safety',
    'Q3': 'soil-science', 'Q4': 'animal-diseases', 'Q5(a)': 'animal-physiology', 'Q5(b)': 'animal-production|animal-physiology',
    'Q6(a)': 'classification-of-organisms|animal-production', 'Q6(a)(ii)': 'animal-production',
    'Q6(b)': 'grassland|animal-production', 'Q6(b)(iii)': 'innovation-and-biotechnology-in-agriculture|grassland',
    'Q7': 'soil-science', 'Q8(a)': 'animal-production|health-safety', 'Q8(b)': 'innovation-and-biotechnology-in-agriculture|animal-production',
    'Q9(a)': 'plant-physiology', 'Q9(a)(iii)': 'plant-physiology|soil-science', 'Q9(b)': 'fertilisers-pollution-the-environment',
    'Q10': 'animal-production', 'Q11(a)': 'genetics|animal-production', 'Q11(b)': 'genetics|animal-production',
    'Q12': 'scientific-practices-experiments-investigations|crop-production',
    'Q13(a)(i)': 'scientific-practices-experiments-investigations|grassland', 'Q13(a)(ii)': 'classification-of-organisms|grassland',
    'Q13(b)': 'scientific-practices-experiments-investigations|grassland',
    'Q14': 'grassland', 'Q14(c)(i)': 'scientific-practices-experiments-investigations|grassland',
    'Q15': 'animal-production', 'Q15(a)(ii)': 'animal-physiology|animal-production',
    'Q16': 'soil-science', 'Q16(b)': 'soil-science|scientific-practices-experiments-investigations', 'Q16(c)': 'soil-science|scientific-practices-experiments-investigations',
    'Q17(a)': 'genetics|animal-production', 'Q17(b)': 'crop-production', 'Q17(b)(iii)': 'health-safety|crop-production', 'Q17(c)': 'crop-production',
    'Q18': 'animal-production', 'Q18(a)(iii)': 'classification-of-organisms|animal-production',
}
SILAGE_WAYS = {
    'pH': 'squeeze liquid from silage / place pH probe into liquid and note the reading or dip pH paper in the liquid and compare to the colour chart / low pH indicates good quality',
    'colour': 'Yellow - green indicates good quality / dark green indicates poor quality',
    'smell': 'sharp acidic or vinegary indicates good quality / putrid or rancid indicates poor quality',
    'DM content': 'squeeze with one hand / liquid removed indicates poor quality / wring with two hands / little or no liquid removed indicates good quality',
    'texture': 'rub the silage sample between your fingers / soft but firm or fibres do not wear easily indicates good quality / wet and slimy indicates poor quality',
    'leaf to stem': 'weigh sample of silage / separate leaves from the stems / weigh each separately / calculate the ratio of stem to leaves',
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
    originals = {cid: card for cid, card in existing.items()
                 if cid.startswith(PREFIX) and (card.get('qa') or {}).get('humanReviewedBy') != 'agent-source-reviewed'}
    snapshot = json.loads(SNAPSHOT.read_text()) if SNAPSHOT.exists() else {}
    for cid, record in snapshot.items():
        if cid.startswith(PREFIX):
            originals[cid] = record['original']

    def task(cid, ref, base, selection=None):
        pp, sp = REGIONS[base]
        t = dict(questionRef='2024 OL ' + ref, paperPage=pp[0]['p'], schemePage=sp[0]['p'], paperRegions=pp, schemeRegions=sp,
                 atlasNumbers={cid: str(1001 + len(tasks))}, cardIds=[cid],
                 examTopicIds=[TOPIC + t for t in atlas_for(ref).split('|')],
                 selection=selection or {'kind': 'none', 'reason': 'Required response at a published boundary. Scheme alternatives remain marking menus.'},
                 evidence='All 40 paper and 26 scheme pages visually inspected. Boundary and tariff checked against the independently transcribed census.')
        tasks.append(t)
        return t

    def keep(key, ref, selection=None):
        cid = PREFIX + key
        card = originals[cid]
        assert card['questionRef'] == '2024 OL ' + ref, (cid, card['questionRef'])
        t = task(cid, ref, ref, selection)
        t['marksPerRoute'] = card['totalMarks']
        t['originalCard'] = 'unchanged'

    def source(ref, pp):
        return dict(kind='source-text', label='OFFICIAL QUESTION PAGE', title='Agricultural Science 2024 Ordinary — ' + ref,
                    pages=sorted({r['p'] for r in pp}), attribution='SEC Agricultural Science 2024 Ordinary Level examination paper — © State Examinations Commission.',
                    presentationNote='Open the original page for the published wording, photographs, tables and examination context.')

    def record(cid, t, reason):
        old = originals[cid]
        corrections[cid] = dict(originalSha256=original_hash(old), originalQuestionRef=old['questionRef'],
                                originalQuestionText=old['questionText'], originalTotalMarks=old['totalMarks'],
                                originalTariffModel=old['tariffModel'], reason=reason)
        t['originalCard'] = 'corrected-in-place'

    def add(key, ref, topic, concept, question, rows, stem=None, figure=None, labels=None, extra=(), extra_fields=None):
        cid = PREFIX + key
        assert cid not in originals, f'{cid} would replace an original card without a correction record'
        rows = [dict(row, id=f'r-{i+1}') for i, row in enumerate(rows)]
        pp, _ = REGIONS[ref]
        card = dict(id=cid, subjectId='agricultural-science', year=YEAR, level='ordinary',
                    section='A' if int(ref.split('(')[0][1:]) <= 12 else 'B', questionRef='2024 OL ' + ref,
                    topicId='agsci-' + topic, curriculumNodeIds=['agsci-' + t for t in (topic, *extra)],
                    conceptId=concept, questionText=question, rows=rows,
                    totalMarks=sum(r['marks'] for r in rows), tariffModel={'kind': 'fixed'},
                    sourceMaterial=source(ref, pp))
        if extra:
            card['additionalTopicIds'] = ['agsci-' + t for t in extra]
        if stem: card['stem'] = stem
        if figure: card['figureKey'] = figure
        if labels: card['labelKey'] = labels
        if extra_fields: card.update(extra_fields)
        t = task(cid, ref, ref)
        t['marksPerRoute'] = card['totalMarks']
        t['originalCard'] = 'added'
        cards.append(card)
        return card

    def fix(key, ref, changes, drop=(), correction=None):
        """Correct an original in place: same ID, ref and boundary; only the named fields change."""
        cid = PREFIX + key
        card = copy.deepcopy(originals[cid])
        assert card['questionRef'] == '2024 OL ' + ref, (cid, card['questionRef'])
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
        return {'kind': 'closed', 'choose': choose, 'options': options, 'pooled': True}

    # Section A ---------------------------------------------------------------
    add('q1a', 'Q1(a)', '3-3-2', 'strip-grazing-direction',
        'Place a tick (✓) in the correct box below to show the direction of grazing in the above diagram. [→ / ←]',
        [point('←', 3, 'The scheme ticks the box beside the left-pointing arrow; its printed answer shows after you reveal.')],
        'The diagram below shows a type of grazing system. Analyse the diagram and answer the questions that follow.',
        figure='agsci-2024-ol-scheme-grazing-direction', extra_fields={'questionFigureKey': 'agsci-2024-ol-paper-grazing-direction'})
    for k, ref in [('q1b', 'Q1(b)'), ('q1c', 'Q1(c)'), ('q1d', 'Q1(d)'), ('q2a', 'Q2(a)'), ('q2bi', 'Q2(b)(i)'), ('q2bii', 'Q2(b)(ii)')]:
        keep(k, ref)
    fix('q2biii', 'Q2(b)(iii)', dict(
        stem='Answer either (a) or (b). The picture shows different cattle handling facilities. Analyse the pictures and answer the questions that follow.',
        figureKey='agricultural-science-2024-OL-paper-p05-i0'),
        correction=('Visually verified paper PDF page 5 ("The picture shows different cattle handling facilities. Analyse the pictures and answer the questions that follow.", pictures A and B) and scheme PDF page 12 (2 marks). '
                    'The original stem was the diagram labels run together ("Single file race Round crowd pen Wrong way Right way Headgate Cattle see place to go"). '
                    'Same ID, rows and 2 marks; the stem is the paper\'s own lead-in and the card shows the inspected picture crop with the labelled head gate.'))
    keep('q2biv', 'Q2(b)(iv)')
    keep('q3', 'Q3')
    keep('q4', 'Q4')
    keep('q5a', 'Q5(a)', selection=closed(3, ['A', 'B', 'C', 'D']))
    keep('q5b', 'Q5(b)')
    keep('q6ai', 'Q6(a)(i)', selection=closed(3, ['A', 'B', 'C', 'D']))
    keep('q6aii', 'Q6(a)(ii)', selection=closed(1, ['Texel', 'Suffolk', 'Charolais', 'Border Leicester']))
    for k, ref in [('q6bi', 'Q6(b)(i)'), ('q6bii', 'Q6(b)(ii)'), ('q6biii', 'Q6(b)(iii)')]:
        keep(k, ref)
    keep('q7a', 'Q7(a)', selection=closed(3, ['Machine size', 'Soil water content', 'Tillage system', 'Crop rotation']))
    for k, ref in [('q7b', 'Q7(b)'), ('q8a', 'Q8(a)'), ('q8b', 'Q8(b)'), ('q9ai', 'Q9(a)(i)'), ('q9aii', 'Q9(a)(ii)'), ('q9aiii', 'Q9(a)(iii)'), ('q9b', 'Q9(b)'),
                   ('q10a', 'Q10(a)'), ('q10b', 'Q10(b)'), ('q10ci', 'Q10(c)(i)'), ('q10cii', 'Q10(c)(ii)'), ('q11ai', 'Q11(a)(i)')]:
        keep(k, ref)
    add('q11aii', 'Q11(a)(ii)', '4-3-2', 'choosing-the-best-offspring',
        'In step 2, state which hen A, B or C is the best offspring to breed future generations.',
        [point('A', 3, 'Hen A.')],
        'Answer either (a) or (b). Selective breeding has been done for thousands of years to improve characteristics of plants and animals. '
        'Analyse the diagram in relation to egg production and answer the questions that follow.',
        figure='agricultural-science-2024-ol-paper-p014-i0')
    for k, ref in [('q11aiii', 'Q11(a)(iii)'), ('q11bi', 'Q11(b)(i)'), ('q11bii', 'Q11(b)(ii)'), ('q12a', 'Q12(a)'), ('q12b', 'Q12(b)')]:
        keep(k, ref)
    # Section B ---------------------------------------------------------------
    keep('q13ai', 'Q13(a)(i)')
    keep('q13aii', 'Q13(a)(ii)', selection=closed(3, ['A', 'B', 'C', 'D']))
    keep('q13bi', 'Q13(b)(i)')
    keep('q13bii', 'Q13(b)(ii)')
    add('q13biii', 'Q13(b)(iii)', '1-3', 'choosing-a-chart',
        'Identify the most suitable chart or graph to display the above results by placing a tick (✓) in the correct box.',
        [point('B', 6, 'The scheme ticks B, the bar chart.')],
        'The results from the investigation give the average % frequency of each plant across ten quadrat throws: dock leaf A, perennial ryegrass 100, nettle 30 and white clover 70.',
        figure='agsci-2024-ol-paper-chart-choice')
    keep('q13biv', 'Q13(b)(iv)')
    keep('q14ai', 'Q14(a)(i)')
    silage = 'Silage making is a very important aspect of farm life as it is an essential feedstuff for ruminant animals on farms.'
    add('q14aii', 'Q14(a)(ii)', '3-3-3', 'best-time-to-cut-silage',
        'Identify the best time of the year to cut grass for silage by placing an X on the diagram.',
        [point('X', 3, 'The scheme places the X at the top of the first, higher peak of grass growth, under its Spring heading; its printed answer shows after you reveal.')],
        silage, figure='agsci-2024-ol-scheme-grass-growth-x', extra_fields={'questionFigureKey': 'agsci-2024-ol-paper-grass-growth'})
    keep('q14aiii', 'Q14(a)(iii)')
    q14b_labels = copy.deepcopy(originals[PREFIX + 'q14bii']['labelKey'])
    add('q14bi', 'Q14(b)(i)', '3-3-3', 'silage-cutting-stage',
        'Identify the correct stage of cutting the grass for silage by placing a tick (✓) in the correct box.',
        [point('B', 2, 'The scheme ticks B.')], silage, figure='agricultural-science-2024-OL-paper-p22-i1', labels=q14b_labels)
    for k, ref in [('q14bii', 'Q14(b)(ii)'), ('q14biii', 'Q14(b)(iii)'), ('q14ci', 'Q14(c)(i)')]:
        keep(k, ref)
    fix('q14cii', 'Q14(c)(ii)', dict(
        rows=[menu(list(SILAGE_WAYS), [2, 2], 'Name of each of your two ways, 2 marks each. The scheme notes "Allow 2 + 2 for name or description".'),
              menu(list(SILAGE_WAYS.values()), [2, 2], 'Description of each of the same two ways, 2 marks each (2(2) + 2(2)). In order the options describe pH, colour, smell, DM content, texture and leaf to stem.')],
        tariffModel={'kind': 'fixed', 'notation': '2(2) + 2(2)'}), drop=('notes',),
        correction=('Visually verified paper PDF page 24 ("Briefly describe two other ways to measure the quality of silage") and scheme PDF page 19 (six named ways with descriptions, "2(2) + 2(2)", "Allow 2 + 2 for name or description"). '
                    'The original priced each way as one 4-mark row, so naming a way without its description scored nothing. Same ID, boundary and 8 marks: two names at 2 each and two descriptions at 2 each.'))
    fix('q14d', 'Q14(d)', dict(
        rows=[point('Length of drying, hay — 5 – 7 days', 2), point('Length of drying, silage — 24 hours', 2),
              point('Method of preservation, hay — Dehydration', 2), point('Method of preservation, silage — Fermentation', 2),
              point('Storage, hay — Shed', 2), point('Storage, silage — Under plastic', 2)],
        tariffModel={'kind': 'fixed', 'notation': '6(2)'}), drop=('notes',),
        correction=('Visually verified paper PDF page 24 (a three-heading hay/silage table filled from a six-word list) and scheme PDF page 19 (six cells, "6(2)"). '
                    'The original paired the hay and silage cells of each heading into one 4-mark row, so one correct cell scored nothing. Same ID, boundary and 12 marks: six cells at 2 marks each.'))
    for k, ref in [('q15ai', 'Q15(a)(i)'), ('q15aii', 'Q15(a)(ii)'), ('q15bi', 'Q15(b)(i)'), ('q15bii', 'Q15(b)(ii)'), ('q15biii', 'Q15(b)(iii)'),
                   ('q15biv', 'Q15(b)(iv)'), ('q15ci', 'Q15(c)(i)'), ('q15cii', 'Q15(c)(ii)'), ('q15d', 'Q15(d)'),
                   ('q16ai', 'Q16(a)(i)'), ('q16aii', 'Q16(a)(ii)'), ('q16aiii', 'Q16(a)(iii)'), ('q16aiv', 'Q16(a)(iv)'), ('q16b', 'Q16(b)'),
                   ('q16ci', 'Q16(c)(i)'), ('q16cii', 'Q16(c)(ii)'), ('q16ciii', 'Q16(c)(iii)'),
                   ('q17ai', 'Q17(a)(i)'), ('q17aii', 'Q17(a)(ii)'), ('q17aiii', 'Q17(a)(iii)'), ('q17bi', 'Q17(b)(i)'), ('q17bii', 'Q17(b)(ii)'),
                   ('q17biii', 'Q17(b)(iii)'), ('q17c', 'Q17(c)'),
                   ('q18ai', 'Q18(a)(i)'), ('q18aii', 'Q18(a)(ii)'), ('q18aiii', 'Q18(a)(iii)'), ('q18b', 'Q18(b)'), ('q18c', 'Q18(c)'), ('q18d', 'Q18(d)')]:
        keep(k, ref)
    assert len(tasks) == 82 and len(cards) == 8 and len(corrections) == 3 and len(originals) == 77, (len(tasks), len(cards), len(corrections), len(originals))
    assert {t['cardIds'][0] for t in tasks} >= set(originals), 'Every original 2024 Ordinary card must be reviewed'
    return cards, tasks, corrections
