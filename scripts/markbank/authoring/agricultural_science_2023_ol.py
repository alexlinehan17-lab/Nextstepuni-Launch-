"""2023 Ordinary review: the 76 original cards reconciled against the SEC sources.

All 40 paper pages and 28 scheme pages were inspected and the independent
census transcribed before any card was touched. 81 base tasks, one card each.
57 original card objects match a published task boundary and tariff and are
left byte-identical; they only gain an Atlas binding and an inspected official
source page. 19 originals are corrected IN PLACE, keeping their IDs: Q2(a)
becomes one any-three-of-five card at the published 3+2+1; Q4, Q8(a),
Q9(b)(iii), Q13(a)(ii) and Q15(b) regain the scheme's first-correct awards
(its PDF page 4 rule) instead of a value pinned to one printed position;
Q16(a)(i) carries the resazurin and bacterial-count methods as answer routes;
Q1(b), Q6(a)(iii), Q9(a)(i), Q10(b)(ii), Q13(b)(ii), Q14(b)(i)-(iii) and
Q15(a)(ii) replace label soup or asterisk debris with the paper's wording (and
gain the paper's graph or diagram where they lacked one); Q14(a)(i) and
Q18(c)(i) regain answers cut mid-sentence; and the fused Q10(b)(i)-(iii) card
keeps part (i) alone, since (ii) already ships separately. Cards are added for
the missing Q5, Q7(a), Q10(b)(iii), Q11 and Q14(b)(iv). Each correction records
the original wording, marks and object hash plus the SEC page that justifies it.
"""
import copy
import hashlib
import json
from agricultural_science_2010_hl import ROOT, point, menu, region
from agricultural_science_2010_parity import scan

FILE = 'LC024GLP000EV.pdf'
YEAR = 2023
HASHES = {'exampapers':'98bdf03549315bcde81f97140f8d530f1081839c7aa7014c1ac8d00fda548510',
          'markingschemes':'64da1086feec80a142d752edffcb6104de0a1cd162367ecca6ebdf5d7695b0b1'}
KEPT_ONE_CARD = ' The original one-card form already lets any printed choice score, so it is kept unchanged (item-choice siblings are not separate practice identities).'
SELECTIONS = {
    '3e445c61dc61b226':('exam-selection','Instructions: Section A, ten of twelve independent questions. Every question and both sides of each internal choice are retained.'),
    'aff3032d941e5f07':('exam-selection','Instructions: Section B, four of six independent questions. Every question is retained.'),
    '1539e8c786747e62':('exam-selection','Repeated Section A instruction: ten independent 10-mark questions, all retained.'),
    'ff5a2cb01ab011a8':('closed','Q1(a): identify any two of the three lettered pieces of equipment A, B and C, 2(3).' + KEPT_ONE_CARD),
    '9dd672b5f0bfda82':('closed','Q2(a): identify any three of the five photographed breeds A–E, 3+2+1. One card: a single anyN row lists all five, claim limit three.'),
    '56768492225d0c88':('independent-task-selection','Q6 either (a) or (b): both independently marked alternatives are retained.'),
    'a66b3a1ca8a4bfd9':('independent-task-selection','Q8 either (a) or (b): both alternatives are retained.'),
    '3345c10f2c4c226c':('independent-task-selection','Q9 either (a) or (b): both alternatives are retained.'),
    '4ea3b9670e82f2e7':('independent-task-selection','Q10 either (a) or (b): both alternatives are retained.'),
    '0cd4bab120debd3c':('exam-selection','Section B heading: four of six independent 50-mark questions, all retained.'),
    '42e2493eb4807845':('independent-task-selection','Q13: (a) and (b) with either (c) or (d). Every part, including both (c) and (d), is retained.'),
    'e45e6e40c9a3b7bf':('independent-task-selection','Q15: (a) with either (b) or (c). Every part, including both (b) and (c), is retained.'),
    '5ff8077d65242b92':('not-a-selection','Prose in the Q16(c) article ("One of the measures used on the farm"); no response choice.'),
    '665d4bf69df14674':('not-a-selection','Prose in the Q18(a) article ("one of his 300 cows"); no response choice.'),
    '312f13b6b1706f1d':('closed','Q18(b)(iii): explain any two of three printed GM-crop issues, 4+2.' + KEPT_ONE_CARD),
    '5ddb5479aae42dd4':('not-a-selection','"could select for" in Q18(c)(ii) is breeding vocabulary, not a response choice; two student-chosen characteristics from an open pool.'),
}
SUPPLEMENTARY = [
    (5,'Outline three management practices carried out','open','Q3(a): student-chosen practices; the scheme pool is a marking menu.'),
    (23,'Using a food crop (other than grass) you have studied','open','Q14(a): a student-named crop; the scheme answers are general or "correct example".'),
    (29,'Describe with the aid of a labelled diagram, how he would carry out this investigation.','closed','Q16(a)(i): the scheme prints a resazurin method "Or" a total bacterial count method (and allows other valid tests); one card, the methods as answer routes.'),
    (5,'Identify the weight of an average dairy beef calf at weaning by placing a tick','answer-identification','Q3(b): one correct box (90kg).'),
    (11,'Identify the bacteria that','answer-identification','Q8(b)(i): one correct box (Rhizobium).'),
    (12,'Identify the pH of the rumen by placing a tick','answer-identification','Q9(a)(iii): one correct box (7.0).'),
    (15,'Identify which bull has the most abnormal sperm cells.','answer-identification','Q10(b)(i): one correct bull read from the table.'),
    (24,'State which diagram','answer-identification','Q14(b)(i): one correct diagram (C) with a reason.'),
    (25,'State which diagram represents farming in the least environmentally friendly way','answer-identification','Q14(b)(iv): one correct diagram (B) with two reasons.'),
    (34,'Identify the description which best explains the underlined term','answer-identification','Q18(a)(i): one correct box (Genetic information).'),
]
TOPIC = 'agricultural-science-ordinary-'
SNAPSHOT = ROOT / 'scripts/markbank/authored/agricultural-science-corrected-originals.json'
PREFIX = 'agsci-2023-ol-'
RESTORED = []
PAGE4 = 'The scheme\'s own rule (PDF page 4): "the first correct answer encountered is awarded" the first mark, and each later correct answer the next.'


def original_hash(card):
    return hashlib.sha256(json.dumps(card, ensure_ascii=False, sort_keys=True).encode()).hexdigest()


def paper_review():
    observed, supplementary = scan(YEAR, FILE, HASHES, SELECTIONS, SUPPLEMENTARY)
    return dict(year=YEAR, level='ordinary', lang='ev', paperFileid=FILE, hashes=HASHES,
                wholePaperVisualReview='reviewed', schemeBoundaryReview='reviewed',
                paperPagesInspected=list(range(1, 41)), schemePagesInspected=list(range(1, 29)),
                selectionDirectives=observed, supplementarySelections=supplementary, sourceNotes=[],
                independentBoundaryReview='81 base tasks, one card each. 57 original cards match a published boundary and tariff unchanged; Q1(a) and Q18(b)(iii) already let any printed choice score. 19 are corrected in place (Q1(b), Q2(a), Q4, Q6(a)(iii), Q8(a), Q9(a)(i), Q9(b)(iii), Q10(b)(i), Q10(b)(ii), Q13(a)(ii), Q13(b)(ii), Q14(a)(i), Q14(b)(i), Q14(b)(ii), Q14(b)(iii), Q15(a)(ii), Q15(b), Q16(a)(i), Q18(c)(i)); five cards are added for the missing Q5, Q7(a), Q10(b)(iii), Q11 and Q14(b)(iv).',
                cropVisualReview='Every distinct paper/scheme crop pair rendered and inspected.',
                runtimeReview='Integrated production-component cases at 1200px and 390px. Signed-in full-app navigation remains open.',
                remaining=['Irish edition comparison (deferred)', 'Full application navigation review', 'Corpus-wide reconciliation'])


P = lambda *r: [region(*x) for x in r]
Q1 = (3, .16, .228)
Q1FIG = (3, .16, .48)
Q2 = (4, .065, .14)
Q6 = (8, .065, .475)
Q9A = (12, .065, .355)
Q10A = (14, .065, .185, 0, .79)
Q10B = (15, .065, .26)
Q12 = (17, .065, .338)
Q13 = (20, .155, .18)
Q13B = (21, .065, .465)
Q14 = (23, .065, .165)
Q14B = (24, .065, .53)
Q15 = (26, .065, .13)
Q16 = (29, .065, .13)
Q16C = (31, .065, .36)
Q17 = (32, .065, .165, 0, .6)
Q17B = (33, .065, .09)
Q18A = (34, .065, .44)
Q18B = (35, .065, .125)
REGIONS = {
    'Q1(a)': (P((3, .16, .61)), P((12, .112, .195))),
    'Q1(b)': (P(Q1FIG, (3, .617, .642)), P((12, .195, .243))),
    'Q1(c)': (P(Q1, (3, .680, .705)), P((12, .243, .291))),
    'Q2(a)': (P((4, .065, .632)), P((12, .291, .409))),
    'Q2(b)': (P((4, .065, .478), (4, .64, .682)), P((12, .409, .475))),
    'Q3(a)': (P((5, .065, .232)), P((12, .475, .661))),
    'Q3(b)': (P((5, .065, .165, 0, .55), (5, .563, .705)), P((12, .661, .75))),
    'Q4': (P((6, .065, .745)), P((13, .041, .377))),
    'Q5': (P((7, .065, .81)), P((13, .377, .588))),
    'Q6(a)(i)': (P((8, .065, .515)), P((13, .588, .654))),
    'Q6(a)(ii)': (P(Q6, (8, .617, .70)), P((13, .654, .742))),
    'Q6(a)(iii)': (P(Q6, (8, .741, .765)), P((13, .742, .81))),
    'Q6(b)': (P((9, .065, .21)), P((14, .040, .244))),
    'Q7(a)': (P((10, .065, .742)), P((14, .244, .445))),
    'Q7(b)': (P((10, .065, .475), (10, .742, .767)), P((14, .445, .531))),
    'Q8(a)': (P((11, .065, .372)), P((14, .531, .598))),
    'Q8(b)(i)': (P((11, .41, .555)), P((14, .598, .716))),
    'Q8(b)(ii)': (P((11, .557, .60)), P((14, .716, .87))),
    'Q9(a)(i)': (P((12, .065, .39)), P((15, .041, .086))),
    'Q9(a)(ii)': (P(Q9A, (12, .424, .448)), P((15, .086, .164))),
    'Q9(a)(iii)': (P((12, .065, .13), (12, .637, .78)), P((15, .164, .27))),
    'Q9(b)(i)': (P((13, .065, .53)), P((15, .27, .40))),
    'Q9(b)(ii)': (P((13, .533, .592)), P((15, .40, .445))),
    'Q9(b)(iii)': (P((13, .597, .83)), P((15, .445, .591))),
    'Q10(a)(i)': (P((14, .065, .445)), P((15, .591, .725))),
    'Q10(a)(ii)': (P(Q10A, (14, .448, .49)), P((15, .725, .86))),
    'Q10(b)(i)': (P(Q10B, (15, .266, .29)), P((16, .040, .107))),
    'Q10(b)(ii)': (P(Q10B, (15, .329, .353)), P((16, .107, .156))),
    'Q10(b)(iii)': (P(Q10B, (15, .393, .417)), P((16, .156, .22))),
    'Q10(b)(iv)': (P((15, .065, .144), (15, .457, .50)), P((16, .22, .284))),
    'Q11': (P((16, .065, .16)), P((16, .284, .512))),
    'Q12(a)': (P(Q12, (17, .338, .358)), P((16, .512, .56))),
    'Q12(b)': (P(Q12, (17, .459, .575)), P((16, .56, .676))),
    'Q12(c)': (P(Q12, (17, .613, .638)), P((16, .676, .76))),
    'Q13(a)(i)': (P((20, .155, .225)), P((17, .111, .264))),
    'Q13(a)(ii)': (P(Q13, (20, .473, .705)), P((17, .264, .37))),
    'Q13(a)(iii)': (P(Q13, (20, .473, .705), (20, .722, .745)), P((17, .37, .504))),
    'Q13(b)(i)': (P((21, .065, .503)), P((17, .504, .568))),
    'Q13(b)(ii)': (P(Q13B, (21, .548, .585)), P((17, .568, .702))),
    'Q13(b)(iii)': (P((21, .065, .14), (21, .69, .713)), P((17, .702, .80))),
    'Q13(c)(i)': (P(Q13, (22, .065, .09)), P((18, .041, .158))),
    'Q13(c)(ii)': (P(Q13, (22, .34, .39)), P((18, .158, .222))),
    'Q13(d)': (P(Q13, (22, .493, .517)), P((18, .222, .357))),
    'Q14(a)(i)': (P((23, .065, .226)), P((18, .357, .481))),
    'Q14(a)(ii)': (P(Q14, (23, .364, .39)), P((18, .481, .658))),
    'Q14(a)(iii)': (P(Q14, (23, .518, .545)), P((18, .658, .935))),
    'Q14(a)(iv)': (P(Q14, (23, .673, .715)), P((19, .041, .213))),
    'Q14(b)(i)': (P(Q14B, (24, .534, .575)), P((19, .213, .336))),
    'Q14(b)(ii)': (P(Q14B, (24, .678, .72)), P((19, .336, .435))),
    'Q14(b)(iii)': (P(Q14B, (25, .065, .11)), P((19, .435, .551))),
    'Q14(b)(iv)': (P(Q14B, (25, .209, .252)), P((19, .551, .71))),
    'Q15(a)(i)': (P((26, .065, .155)), P((20, .041, .19))),
    'Q15(a)(ii)': (P(Q15, (26, .30, .505)), P((20, .19, .253))),
    'Q15(a)(iii)': (P(Q15, (26, .604, .628)), P((20, .253, .437))),
    'Q15(a)(iv)': (P(Q15, (26, .745, .768)), P((20, .437, .551))),
    'Q15(a)(v)': (P(Q15, (27, .065, .11)), P((20, .551, .706))),
    'Q15(a)(vi)': (P(Q15, (27, .724, .748)), P((20, .706, .803))),
    'Q15(b)': (P(Q15, (28, .065, .36)), P((20, .803, .875))),
    'Q15(c)': (P(Q15, (28, .461, .88)), P((21, .040, .148))),
    'Q16(a)(i)': (P((29, .065, .152)), P((21, .148, .741))),
    'Q16(a)(ii)': (P(Q16, (30, .065, .18)), P((21, .741, .895))),
    'Q16(a)(iii)': (P(Q16, (30, .179, .205)), P((22, .041, .15))),
    'Q16(b)(i)': (P((30, .300, .36)), P((22, .15, .265))),
    'Q16(b)(ii)': (P((30, .512, .72)), P((22, .265, .395))),
    'Q16(c)(i)': (P((31, .065, .395)), P((22, .395, .496))),
    'Q16(c)(ii)': (P(Q16C, (31, .497, .64)), P((22, .496, .58))),
    'Q17(a)(i)': (P((32, .065, .235)), P((23, .041, .155))),
    'Q17(a)(ii)': (P(Q17, (32, .393, .418)), P((23, .155, .251))),
    'Q17(a)(iii)': (P(Q17, (32, .52, .70)), P((23, .251, .381))),
    'Q17(b)(i)': (P((33, .065, .115)), P((23, .381, .443))),
    'Q17(b)(ii)': (P(Q17B, (33, .179, .203)), P((23, .443, .522))),
    'Q17(b)(iii)': (P(Q17B, (33, .36, .385)), P((23, .522, .637))),
    'Q17(c)': (P((33, .542, .88)), P((23, .637, .87))),
    'Q18(a)(i)': (P((34, .065, .565)), P((24, .041, .083))),
    'Q18(a)(ii)': (P(Q18A, (34, .564, .59)), P((24, .083, .145))),
    'Q18(a)(iii)': (P((34, .065, .11), (34, .719, .743)), P((24, .145, .242))),
    'Q18(b)(i)': (P((35, .065, .50)), P((24, .242, .322))),
    'Q18(b)(ii)': (P(Q18B, (35, .658, .683)), P((24, .322, .453))),
    'Q18(b)(iii)': (P((36, .065, .31)), P((24, .453, .677))),
    'Q18(c)(i)': (P((36, .503, .545)), P((24, .677, .757))),
    'Q18(c)(ii)': (P((36, .503, .524), (36, .644, .69)), P((24, .757, .85))),
}
ATLAS = {
    'Q1': 'soil-science|scientific-practices-experiments-investigations', 'Q2(a)': 'animal-production|classification-of-organisms',
    'Q2(b)': 'animal-production|health-safety', 'Q3': 'animal-production', 'Q4': 'crop-production|fertilisers-pollution-the-environment',
    'Q5': 'animal-diseases|health-safety', 'Q6': 'grassland|animal-production', 'Q7': 'animal-production',
    'Q8': 'animal-diseases|animal-production', 'Q9': 'animal-physiology', 'Q10(a)': 'animal-production|genetics',
    'Q10(b)': 'animal-production', 'Q10(b)(iv)': 'animal-production|health-safety',
    'Q11': 'soil-science|scientific-practices-experiments-investigations', 'Q12': 'crop-production|innovation-and-biotechnology-in-agriculture',
    'Q13': 'grassland', 'Q13(a)(ii)': 'grassland|classification-of-organisms', 'Q13(b)': 'grassland|scientific-practices-experiments-investigations',
    'Q14(a)': 'crop-production', 'Q14(a)(iv)': 'crop-production|health-safety', 'Q14(b)': 'fertilisers-pollution-the-environment',
    'Q15': 'soil-science', 'Q15(a)(v)': 'soil-science|scientific-practices-experiments-investigations',
    'Q15(a)(vi)': 'soil-science|scientific-practices-experiments-investigations',
    'Q16(a)': 'scientific-practices-experiments-investigations|animal-production', 'Q16(b)': 'animal-production',
    'Q16(c)': 'animal-production|fertilisers-pollution-the-environment', 'Q17': 'animal-production',
    'Q18': 'genetics|innovation-and-biotechnology-in-agriculture', 'Q18(c)': 'genetics',
}
BREEDS = {'A': ('Charolais', 'cream-white bull standing in grass'), 'B': ('Aubrac', 'dark grey-brown bull with a paler saddle and a ring in its nose'),
          'C': ('Limousine', 'solid red-brown bull beside a fence'), 'D': ('Simmental', 'red-and-white bull with a white face and a ring in its nose'),
          'E': ('Belgian Blue', 'heavily muscled black-and-white bull with a ring in its nose')}
RESAZURIN = ['Place milk sample into test tubes', 'add few drops (1 cm³) of Resazurin to three tubes (average)', 'place in water bath', 'at 37°C',
             'for 15 minutes', 'record colour change',
             'Result: (allow one only) Fresh – blue – good quality (low TBC) Blue – deep mauve = good (Deep) pink = fair (Light) pink = poor White = poor']
TBC = ['Get a sample of milk and carry out a serial dilution of the milk sample by adding 1ml of milk into 9ml of distilled water & shake to mix',
       'take 1ml from this test tube and add to 9ml of distilled water & shake', 'repeat this for 4 more test tubes',
       'take 1ml of milk from the last test tube & place on a prepared nutrient agar plate under aseptic conditions. Repeat 3 times for accurate results',
       'spread the milk around the plate using a plate spreader', 'leave one agar plate unopened as a control', 'place in incubator for 72 hours at 25°C',
       'remove plate & record number of bacteria colonies on the plate & multiply by 10⁶ to get the number of CFU’s',
       'Result: There will be CFU’s in the plate over - time as the number of bacteria in the sample multiply causing a decrease in quality of the milk.']
OTHER_TESTS = ('The scheme adds: "There are other valid tests a student could do - % protein / % butterfat (gerber method) / Presence of Thermoduric bacteria (serial dilution) / '
               'presence of antibiotics (Devlo test) / SCC – California Mastitis Test (CMT) / % Solids in a milk sample (excess water) (Points can be found on the diagram)".')
POLLUTION = ['cattle drinking in river', 'splash plate slurry spreading or slurry being spread near the river', 'no trees or plants', 'monoculture',
             'no wildlife corridors', 'river banks are being eroded into the river', 'water quality (eutrophication)', 'spraying weed killer (near river)']
EARTHWORM = ('Layer of organic matter (leaf litter) or grass on top / earthworms on top / layer of chalk or layer of compost / layer of sand or layer of gravel / '
             'layer of clay or layer of soil / earthworms create channels or channels shown / earthworms mixing layers or mixed layers shown / decompose organic matter')
ANTIBIOTIC = {'A': 'Antibiotic tube inserted into teat', 'B': 'Teat wiped with antiseptic wipe', 'C': 'Teat dipped in iodine',
              'D': 'Cow milked out', 'E': 'Teat massaged to move antibiotic from teat into udder'}


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
    originals = {cid: card for cid, card in existing.items()
                 if cid.startswith(PREFIX) and (card.get('qa') or {}).get('humanReviewedBy') != 'agent-source-reviewed'}
    snapshot = json.loads(SNAPSHOT.read_text()) if SNAPSHOT.exists() else {}
    for cid, record in snapshot.items():
        if cid.startswith(PREFIX):
            originals[cid] = record['original']

    def task(cid, ref, selection=None):
        pp, sp = REGIONS[ref]
        t = dict(questionRef='2023 OL ' + ref, paperPage=pp[0]['p'], schemePage=sp[0]['p'], paperRegions=pp, schemeRegions=sp,
                 atlasNumbers={cid: str(1001 + len(tasks))}, cardIds=[cid],
                 examTopicIds=[TOPIC + t for t in atlas_for(ref).split('|')],
                 selection=selection or {'kind': 'none', 'reason': 'Required response at a published boundary. Scheme alternatives remain marking menus.'},
                 evidence='All 40 paper and 28 scheme pages visually inspected. Boundary and tariff checked against the independently transcribed census.')
        tasks.append(t)
        return t

    def keep(key, ref, selection=None):
        cid = PREFIX + key
        card = originals[cid]
        assert card['questionRef'] == '2023 OL ' + ref, (cid, card['questionRef'])
        t = task(cid, ref, selection)
        t['marksPerRoute'] = card['totalMarks']
        t['originalCard'] = 'unchanged'
        if cid in snapshot:
            assert original_hash(card) == snapshot[cid]['originalSha256']
            RESTORED.append(card)

    def source(ref, pp):
        return dict(kind='source-text', label='OFFICIAL QUESTION PAGE', title='Agricultural Science 2023 Ordinary — ' + ref,
                    pages=sorted({r['p'] for r in pp}), attribution='SEC Agricultural Science 2023 Ordinary Level examination paper — © State Examinations Commission.',
                    presentationNote='Open the original page for the published wording, photographs, tables and examination context.')

    def record(cid, t, reason):
        old = originals[cid]
        corrections[cid] = dict(originalSha256=original_hash(old), originalQuestionRef=old['questionRef'],
                                originalQuestionText=old['questionText'], originalTotalMarks=old['totalMarks'],
                                originalTariffModel=old['tariffModel'], reason=reason)
        t['originalCard'] = 'corrected-in-place'

    def add(key, ref, topic, concept, question, rows, stem=None, marks=None, tariff=None, selection=None, figure=None, labels=None, correction=None):
        cid = PREFIX + key
        rows = [dict(row, id=f'r-{i+1}') for i, row in enumerate(rows)]
        pp, _ = REGIONS[ref]
        card = dict(id=cid, subjectId='agricultural-science', year=YEAR, level='ordinary',
                    section='A' if int(ref.split('(')[0][1:]) <= 12 else 'B', questionRef='2023 OL ' + ref,
                    topicId='agsci-' + topic, curriculumNodeIds=['agsci-' + topic],
                    conceptId=concept, questionText=question, rows=rows,
                    totalMarks=marks if marks is not None else sum(r['marks'] for r in rows),
                    tariffModel=tariff or {'kind': 'fixed'}, sourceMaterial=source(ref, pp))
        if stem: card['stem'] = stem
        if figure: card['figureKey'] = figure
        if labels: card['labelKey'] = labels
        t = task(cid, ref, selection)
        t['marksPerRoute'] = card['totalMarks']
        if correction:
            record(cid, t, correction)
        else:
            assert cid not in originals, f'{cid} would replace an original card without a correction record'
            t['originalCard'] = 'added'
        cards.append(card)
        return card

    def fix(key, ref, changes, drop=(), correction=None, selection=None):
        cid = PREFIX + key
        card = copy.deepcopy(originals[cid])
        assert card['questionRef'] == '2023 OL ' + ref, (cid, card['questionRef'])
        for field in drop:
            card.pop(field, None)
        if 'rows' in changes:
            changes = dict(changes, rows=[dict(row, id=f'r-{i+1}') for i, row in enumerate(changes['rows'])])
        card.update(changes)
        card['curriculumNodeIds'] = [card['topicId']]
        card['sourceMaterial'] = source(ref, REGIONS[ref][0])
        t = task(cid, ref, selection)
        t['marksPerRoute'] = card['totalMarks']
        record(cid, t, correction)
        cards.append(card)
        return card

    def closed(choose, options):
        return {'kind': 'closed', 'choose': choose, 'options': options, 'pooled': True}

    def ranked(key, ref, notation, note, page, scheme_page, wording, extra=None):
        """The scheme's first-correct awards instead of a value pinned to one position."""
        old = originals[PREFIX + key]
        rows = [dict(row, marks=None) for row in copy.deepcopy(old['rows'])]
        rows[0]['contextNote'] = note
        changes = dict(rows=rows, tariffModel={'kind': 'orderedSplit', 'notation': notation})
        changes.update(extra or {})
        pinned = ', '.join(f'{r["marks"]} to {r["verbatim"].split(" — ")[0].split(":")[0]!r}' for r in old['rows'])
        return fix(key, ref, changes, drop=('notes',), correction=(
            f'Visually verified paper PDF page {page} and scheme PDF page {scheme_page} ({wording}, "{notation}") with the scheme\'s PDF page 4 rule that "the first correct answer encountered" earns the first mark. '
            f'The original pinned the marks to positions ({pinned}), so a student whose first correct answer came later lost marks the scheme awards. '
            f'Same ID, rows, boundary and {old["totalMarks"]} marks; the awards follow the order of correct answers.'))

    # Section A ---------------------------------------------------------------
    keep('q1a', 'Q1(a)', selection=closed(2, ['A', 'B', 'C']))
    q1 = 'An agricultural science student wanted to test the pH of a sample of soil before deciding what crops to sow.'
    fix('q1b', 'Q1(b)', dict(stem=q1, rows=[point('6.5', 3, 'Asterisked in the scheme ("6.5*"): only this value scores. It is the reading on the pH probe in the drawing.', kind='gate')]),
        drop=('notes',),
        correction=('Visually verified paper PDF page 3 (the bench drawing with the pH probe reading 6.5, then "State the pH of the soil filtrate.") and scheme PDF page 12 ("6.5*", 3). '
                    'The original stem ended in the drawing\'s labels run together ("pH probe Universal Indicator") and the answer carried the scheme\'s asterisk as text. '
                    'Same ID, figure, boundary and 3 marks; the stem is the paper\'s lead-in and the asterisk is the exact-term rule.'))
    keep('q1c', 'Q1(c)')
    letters = list(BREEDS)
    fix('q2a', 'Q2(a)', dict(
        stem='Jimmy went to his local mart to buy continental beef cattle.',
        questionText='Assist Jimmy in identifying any three of the following continental beef cattle using the list below: Belgian Blue, Aubrac, Limousin, Charolais, Simmental.',
        rows=[menu([f'{l}: {BREEDS[l][0]}' for l in letters], [3, 2, 1], 'Any three of the five photographs. The scheme prints 3+2+1: the first correct identification earns 3, the second 2 and the third 1. The scheme spells C "Limousine".')],
        labelKey=[dict(letter=l, meaning=f'{BREEDS[l][1]} ({BREEDS[l][0]})', askedInThisQuestion=True) for l in letters]),
        drop=('notes',), selection=closed(3, letters),
        correction=('Visually verified paper PDF page 4 ("Assist Jimmy in identifying any three of the following continental beef cattle using the list below", word list and photographs A–E) and scheme PDF page 12 (A Charolais, B Aubrac, C Limousine, D Simmental, E Belgian Blue, "3+2+1"). '
                    'The original stem was the word list run together, its label key decoded only A–C, and the 3 marks were pinned to A. '
                    'Same ID: one any-three-of-five card whose anyN row lists all five breeds at 3+2+1, claim limit three, with every photograph decoded.'))
    keep('q2b', 'Q2(b)')
    keep('q3a', 'Q3(a)')
    keep('q3b', 'Q3(b)')
    ranked('q4', 'Q4', '6+2+2', 'One reason for each of the three practices. ' + PAGE4 + ' So the first correct reason earns 6 and each later one 2, whichever practice it is for.',
           6, 13, '"Outline one reason why each of the following farming practices is carried out", three printed practices')
    add('q5', 'Q5', '4-3-3', 'biosecurity-threats-and-risk-reduction',
        'Using your knowledge of biosecurity, explain how each of the following can threaten the biosecurity on a farm and outline what the farmer can do to reduce the risk: Sick animals; Contaminated vehicles and equipment.',
        [dict(point('Sick animals — Can pass the disease (infect) onto other animals or humans', None, 'Four answers: how each threatens biosecurity and how to reduce the risk. The scheme prints 4+4+1+1. ' + PAGE4),
              kind='alt', accepts=['cause a disease outbreak on the farm']),
         dict(point('Sick animals, reduce risk — Isolate new animals when entering the farm', None), kind='alt', accepts=['isolate sick animals', 'vaccination', 'cull sick animals']),
         dict(point('Contaminated vehicles and equipment — Can carry disease between farms (on tyres)', None), kind='alt', accepts=['in slurry tankers']),
         point('Contaminated vehicles and equipment, reduce risk — Wash or disinfect vehicles and equipment between farms', None)],
        'Biosecurity is crucial in maintaining healthy animals. Analyse the picture and answer the questions which follow.',
        marks=10, tariff={'kind': 'orderedSplit', 'notation': '4+4+1+1'}, figure='agricultural-science-2023-OL-paper-p07-i0')
    keep('q6a-i', 'Q6(a)(i)')
    keep('q6a-ii', 'Q6(a)(ii)')
    fix('q6aiii', 'Q6(a)(iii)', dict(
        stem='Answer either (a) or (b). The diagram shows the grass growth cycle and how each growth stage affects silage quality. Analyse the picture and answer the questions which follow.',
        figureKey='agricultural-science-2023-OL-paper-p08-i0'), drop=('notes',),
        correction=('Visually verified paper PDF page 8 (the grass growth diagram with silage DMD bands A–D and their animal captions, then "State which silage DMD % is suitable for dry suckler cows that have a good BCS.") and scheme PDF page 13 ("<67(%) or D", 1). '
                    'The original stem was the diagram\'s labels run together and the card had no diagram. Same ID, row, boundary and 1 mark; the stem is the paper\'s lead-in and the card shows the inspected diagram.'))
    keep('q6b', 'Q6(b)')
    ewes = 'The diagram below is used to rate how good a ewe is at looking after her lambs. Analyse the diagram and answer the questions which follow.'
    add('q7a', 'Q7(a)', '4-3-2', 'ewe-mothering-ability-implications',
        'Dónal was scoring his ewes mothering ability after lambing and recorded the results in the table below. Complete the table below for Dónal describing the implications of his results. '
        'The first one has been done as an example: ewe 106, score 5, "Very good, attentive mother and will protect lambs from predators and the weather".',
        [dict(point('Ewe 107, score 3 — (Average mother), not protective and moderately attentive', 3, 'The scheme adds "or valid implication described" (2(3)).'), openList=True),
         dict(point('Ewe 108, score 1 — (Very poor mother) with no interest in lambs', 3, 'Or a valid implication described.'), openList=True)],
        ewes, figure='agsci-2023-ol-paper-ewe-mothering')
    keep('q7b', 'Q7(b)')
    order = [('2nd', 'B'), ('3rd', 'A'), ('4th', 'E'), ('5th', 'C')]
    fix('q8a', 'Q8(a)', dict(
        rows=[point(f'{n} — {l}', None, f'{ANTIBIOTIC[l]}.' + (' The scheme prints D B A E C at 6+2+1+1, D being given. ' + PAGE4 if i == 0 else ''))
              for i, (n, l) in enumerate(order)],
        tariffModel={'kind': 'orderedSplit', 'notation': '6+2+1+1'}), drop=('notes',),
        correction=('Visually verified paper PDF page 11 ("Place the steps in correct order. The first one is done for you.", steps A–E with D given) and scheme PDF page 14 ("D B A E C", "6+2+1+1") with its PDF page 4 rule that "the first correct answer encountered" earns the first mark. '
                    'The original was one all-or-nothing 10-mark row, so three correct placements out of four scored nothing. '
                    'Same ID, boundary and 10 marks; the four placements earn 6, 2, 1 and 1 in the order they are correct.'))
    keep('q8b-i', 'Q8(b)(i)')
    keep('q8b-ii', 'Q8(b)(ii)')
    stomach = 'Answer either (a) or (b). The diagrams show the development of a ruminant stomach from birth to maturity. Analyse the diagrams and answer the questions which follow.'
    fix('q9ai', 'Q9(a)(i)', dict(stem=stomach, rows=[point('Abomasum', 3, 'Asterisked in the scheme ("Abomasum*"): only this term scores.', kind='gate')]),
        drop=('notes',),
        correction=('Visually verified paper PDF page 12 (three stomach diagrams, first week, 3 to 4 months and maturity, with chamber A arrowed, then "Identify the stomach chamber A.") and scheme PDF page 15 ("Abomasum*", 3). '
                    'The original had no stem and carried the scheme\'s asterisk as text in its answer. Same ID, figure, boundary and 3 marks.'))
    keep('q9a-ii', 'Q9(a)(ii)')
    keep('q9a-iii', 'Q9(a)(iii)')
    keep('q9b-i', 'Q9(b)(i)')
    keep('q9b-ii', 'Q9(b)(ii)')
    ranked('q9b-iii', 'Q9(b)(iii)', '3+1', 'One difference, given for both stomachs. The scheme prints 3+1. ' + PAGE4,
           13, 15, '"State one difference between a ruminant stomach and a monogastric stomach", a two-column table')
    keep('q10a-i', 'Q10(a)(i)')
    keep('q10a-ii', 'Q10(a)(ii)')
    bulls = ('Answer either (a) or (b). The vet was called to a farm to carry out a fertility test on four stock bulls. The vet collected a sample of semen from the four bulls for analysis. '
             'The results are shown in the table below. Analyse the table and answer the questions which follow.')
    add('q10b-i-iii', 'Q10(b)(i)', '4-1', 'semen-analysis-interpretation', 'Identify which bull has the most abnormal sperm cells.',
        [point('Bull 4', 3, 'Bull 4 has the highest abnormal structure, 10%.')], bulls, figure='agricultural-science-2023-OL-paper-p15-i1',
        correction=('Visually verified paper PDF page 15 ("(i) Identify which bull has the most abnormal sperm cells.", "(ii) Identify which bull has the best sperm motility.", "(iii) State which bull is the most fertile...") and scheme PDF page 16 ((i) Bull 4, 3; (ii) Bull 1, 3; (iii) Bull 1, 2). '
                    'The original fused (i)–(iii) into one 8-mark card while (ii) also ships as agsci-2023-ol-q10bii, so (ii) was carded twice. This ID keeps part (i) at its published 3 marks; (iii) is its own card.'))
    fix('q10bii', 'Q10(b)(ii)', dict(stem=bulls, figureKey='agricultural-science-2023-OL-paper-p15-i1'), drop=('notes',),
        correction=('Visually verified paper PDF page 15 (the lead-in, the results table, then "Identify which bull has the best sperm motility.") and scheme PDF page 16 ("Bull 1", 3). '
                    'The original stem was the results table run together ("Bull 1 Bull 2 Bull 3 Bull 4 Sperm motility (%) 100 95 90 95 ..."). Same ID, row, boundary and 3 marks; the stem is the paper\'s lead-in and the card shows the table crop.'))
    add('q10biii', 'Q10(b)(iii)', '4-3-2', 'choosing-the-most-fertile-bull',
        'State which bull is the most fertile and best to use with the maiden heifers on the farm.',
        [point('Bull 1', 2, 'Bull 1 has the best motility (100%) and the fewest abnormal sperm (5%).')], bulls, figure='agricultural-science-2023-OL-paper-p15-i1')
    keep('q10b-iv', 'Q10(b)(iv)')
    add('q11', 'Q11', '2-2-3', 'earthworm-activity-investigation',
        'A student was carrying out an investigation to show the activity of earthworms. Draw a labelled diagram showing this activity.',
        [point('Diagram – showing - suitable container, 2 layers, earthworms, mixing or tunnels', None,
               'Drawing, D = 0, 2, 4: any 3 correct for 4 marks / any 2 correct for 2 marks.', kind='criterion'),
         point(EARTHWORM, None, 'Labels: any 3 correct labels, 2 marks each (Labels = 3(2)).')],
        marks=10, tariff={'kind': 'questionTotal', 'notation': 'D = 0,2,4 + Labels = 3(2)'})
    for k, ref in [('q12a', 'Q12(a)'), ('q12b', 'Q12(b)'), ('q12c', 'Q12(c)')]:
        keep(k, ref)
    # Section B ---------------------------------------------------------------
    keep('q13a-i', 'Q13(a)(i)')
    ranked('q13aii', 'Q13(a)(ii)', '6+3+3', 'Three plants. The scheme prints 6+3+3 and adds "(clover accepted once only)". ' + PAGE4,
           20, 17, '"Identify the plants below that may be sown in a newly reseeded pasture", photographs A, B and C')
    keep('q13a-iii', 'Q13(a)(iii)')
    keep('q13b-i', 'Q13(b)(i)')
    reseed = ('Traditional reseeding methods involve mainly ploughing the land. Research into more sustainable practices (disc, one pass and direct drill) are shown in the graph below. '
              'Sustainable practices are being compared to ploughing which has a grass growth potential of 1. Analyse the graph and answer the questions which follow.')
    old_b2 = originals[PREFIX + 'q13bii']['rows'][0]
    fix('q13bii', 'Q13(b)(ii)', dict(stem=reseed, figureKey='agricultural-science-2023-OL-paper-p21-i0',
        rows=[dict(point(old_b2['verbatim'], 2, 'One conclusion, 2 marks.'), kind='alt', accepts=['correct ranking in relation to sustainability (using data from graph)'])]),
        drop=('notes',),
        correction=('Visually verified paper PDF page 21 (the lead-in, the bar chart of grass production relative to the plough method, then "Outline what conclusion the researchers can make in relation to the sustainable reseeding methods.") and scheme PDF page 17 (two alternatives, 2). '
                    'The original stem was the chart\'s labels and values run together, with no chart, and the second published conclusion ("correct ranking in relation to sustainability (using data from graph)") was missing. '
                    'Same ID, boundary and 2 marks; the stem is the paper\'s lead-in, the card shows the inspected chart and the row accepts both conclusions.'))
    for k, ref in [('q13b-iii', 'Q13(b)(iii)'), ('q13c-i', 'Q13(c)(i)'), ('q13c-ii', 'Q13(c)(ii)'), ('q13d', 'Q13(d)')]:
        keep(k, ref)
    fix('q14a-i', 'Q14(a)(i)', dict(rows=[
        point('Disease resistance: Ability to prevent or reduce the presence of diseases in a crop', 2, 'The scheme adds "/ or correct example".'),
        point('Time of harvest: The time of the year during which the crop is harvested', 2, 'The scheme adds "/ or correct example".')]),
        drop=('notes',),
        correction=('Visually verified paper PDF page 23 ("When selecting the seed for sowing, Lisa checked the disease resistance and time of harvest. Explain the underlined terms.") and scheme PDF page 18 (one definition each, 2 + 2). '
                    'The original answers stopped at "the presence of" and "during which the crop is", with the rest in notes. Same ID, boundary and 4 marks; each row is the whole published definition.'))
    for k, ref in [('q14a-ii', 'Q14(a)(ii)'), ('q14a-iii', 'Q14(a)(iii)'), ('q14a-iv', 'Q14(a)(iv)')]:
        keep(k, ref)
    diagrams = 'Analyse the diagrams and answer the questions which follow.'
    soup = ('Visually verified paper PDF page {p} ("Analyse the diagrams and answer the questions which follow.", block diagrams A, B and C of the same river, then "{q}") and scheme PDF page 19. '
            'The original stem was the diagram\'s arrow letters run together ("W X"). Same ID, rows, figure, boundary and {m} marks; the stem is the paper\'s own lead-in.')
    fix('q14bi', 'Q14(b)(i)', dict(stem=diagrams), correction=soup.format(p=24, q='State which diagram A, B or C has a higher biodiversity level and give a reason for your answer.', m=8))
    fix('q14bii', 'Q14(b)(ii)', dict(stem=diagrams), drop=('notes',), correction=soup.format(p=24, q='Outline the reason for the crop X being sown between the cows and the river in diagram A.', m=4))
    fix('q14b-iii', 'Q14(b)(iii)', dict(stem=diagrams), drop=('notes',), correction=soup.format(p='24 and page 25', q='The farmer W is spot spraying the weeds in the field in diagram B. Outline the advantage of spot spraying compared to spraying the whole field.', m=4))
    add('q14biv', 'Q14(b)(iv)', '2-3', 'least-environmentally-friendly-farm',
        'State which diagram represents farming in the least environmentally friendly way and give two reasons for your answer.',
        [point('Diagram: B', 4), menu(POLLUTION, [4, 4], 'Two reasons, 4 marks each (2(4)).')],
        diagrams, figure='agricultural-science-2023-OL-paper-p24-art')
    keep('q15a-i', 'Q15(a)(i)')
    brian = 'Answer (a) with either (b) or (c). Brian bought 120 hectares of land for a mixed tillage and beef enterprise. He carried out a number of tests on the soil.'
    fix('q15aii', 'Q15(a)(ii)', dict(stem=brian, figureKey='agsci-2023-ol-paper-compacted-soil'),
        correction=('Visually verified paper PDF page 26 ("Two soil samples A and B were collected are represented in the diagrams. Identify which soil is compacted and give a reason for your answer.", diagrams A and B with a soil particle / water / air key) and scheme PDF page 20 (B 5, reason 5). '
                    'The original stem was the diagram key run together ("Soil particle Water Air") and the card had no diagram. Same ID, rows, boundary and 10 marks; the stem is the paper\'s lead-in and the card shows the inspected diagrams.'))
    for k, ref in [('q15a-iii', 'Q15(a)(iii)'), ('q15a-iv', 'Q15(a)(iv)'), ('q15a-v', 'Q15(a)(v)'), ('q15a-vi', 'Q15(a)(vi)')]:
        keep(k, ref)
    ranked('q15b', 'Q15(b)', '6+4', 'Two labels. The scheme prints 6+4. ' + PAGE4,
           28, 20, '"Brian discovered the soil type to be a brown earth soil as shown in the diagram below. Assist Brian in labelling the diagram.", arrows A and B',
           extra=dict(stem=brian))
    keep('q15c', 'Q15(c)')
    resazurin = dict(menu(RESAZURIN, [4, 4, 4], 'Resazurin test: any three points, 4 marks each (3(4)). ' + OTHER_TESTS), id='r-1')
    tbc = dict(menu(TBC, [4, 4, 4], 'Total bacterial count: any three points, 4 marks each (3(4)). ' + OTHER_TESTS), id='r-1')
    fix('q16ai', 'Q16(a)(i)', dict(
        stem='Pat is doing a screening on his dairy herd. He wanted to check the quality of a milk sample.',
        rows=[resazurin], answerVariants=[dict(id='resazurin', label='Resazurin test', rows=[resazurin]), dict(id='tbc', label='Total bacterial count', rows=[tbc])],
        tariffModel={'kind': 'fixed', 'notation': '3(4)'}), drop=('notes',), selection=closed(1, ['Resazurin test', 'Total bacterial count']),
        correction=('Visually verified paper PDF page 29 ("Describe with the aid of a labelled diagram, how he would carry out this investigation.") and scheme PDF page 21 (a resazurin method "Or" a total bacterial count method, "Or" other valid tests, "3(4)"). '
                    'The original mixed three resazurin steps and three bacterial-count steps in one six-option group, leaving out the rest of both methods. '
                    'Same ID, boundary and 12 marks; the two methods are official answer routes the student chooses before reveal, each listing every published point, any three at 4 marks.'))
    for k, ref in [('q16aii', 'Q16(a)(ii)'), ('q16aiii', 'Q16(a)(iii)'), ('q16bi', 'Q16(b)(i)'), ('q16bii', 'Q16(b)(ii)'), ('q16ci', 'Q16(c)(i)'), ('q16cii', 'Q16(c)(ii)'),
                   ('q17ai', 'Q17(a)(i)'), ('q17aii', 'Q17(a)(ii)'), ('q17aiii', 'Q17(a)(iii)'), ('q17bi', 'Q17(b)(i)'), ('q17bii', 'Q17(b)(ii)'), ('q17biii', 'Q17(b)(iii)'),
                   ('q17c', 'Q17(c)'), ('q18ai', 'Q18(a)(i)'), ('q18aii', 'Q18(a)(ii)'), ('q18aiii', 'Q18(a)(iii)'), ('q18bi', 'Q18(b)(i)'), ('q18bii', 'Q18(b)(ii)')]:
        keep(k, ref)
    keep('q18biii', 'Q18(b)(iii)', selection=closed(2, ['Impact on the environment', 'Effect on food chain', 'Increase in production']))
    fix('q18ci', 'Q18(c)(i)', dict(rows=[
        point('Selective breeding involves choosing parents with particular characteristics to breed together', 2, 'Choosing the parents, 2 marks (2+2).'),
        point('produce offspring with more desirable characteristics.', 2, 'What the choosing is for, 2 marks.')]),
        drop=('notes',),
        correction=('Visually verified paper PDF page 36 ("Farmers and scientists have been improving crops and animals through selective breeding. Explain the underlined term.") and scheme PDF page 24 (two points, 2+2). '
                    'The original first answer stopped at "choosing parents with particular", with the whole sentence only as an accepted alternative. Same ID, boundary and 4 marks; the row is the whole published point.'))
    keep('q18cii', 'Q18(c)(ii)')
    assert len(tasks) == 81 and len(corrections) == 19 and len(originals) == 76 and len(cards) == 24, (len(tasks), len(cards), len(corrections), len(originals))
    assert {t['cardIds'][0] for t in tasks} >= set(originals), 'Every original 2023 Ordinary card must be reviewed'
    return cards, tasks, corrections
