"""2021 Ordinary review: the 111 original cards reconciled against the SEC sources.

All 44 paper pages and 26 scheme pages were inspected and the independent
census transcribed before any card was touched. 113 base tasks, one card each
(Q1(a)(i)-(iii) and Q6(a)-(e) each sit under one instruction and stay one card;
Q15(b) and Q18(a)(i) are carded by printed heading because the scheme prices
each heading on its own). 77 original card objects match a published boundary
and tariff and are left byte-identical; they only gain an Atlas binding and an
inspected official source page. 34 originals are corrected IN PLACE, keeping
their IDs: pools that dropped published points list every point; pinned
first-correct awards follow the order of correct answers; named-breed,
error, result and implication answers become answer routes; stems and
questions built from diagram, word-list or table debris are replaced by the
paper's wording; and Q18(a)(i) Seedbed preparation regains the 2 marks the
scheme gives for naming the crop. Cards are added for the missing Q11(b)(iv)
and Q18(b)(iii). Each correction records the original wording, marks and object
hash plus the SEC page that justifies it.
"""
import copy
import hashlib
import json
import re
from agricultural_science_2010_hl import ROOT, point, menu, region
from agricultural_science_2010_parity import scan

FILE = 'LC024GLP000EV.pdf'
YEAR = 2021
HASHES = {'exampapers':'e4cad5e9b9c5a3bd923da963916baebeaa7d49044bfb856434a318bd1755df59',
          'markingschemes':'efec540781423841de14dfde99b9c751e7f04c6240e4f8db7fd8db9e0855ee8c'}
SELECTIONS = {
    'bb826982be26b3fd':('exam-selection','Instructions: Section A, seven of twelve independent questions. Every question and both sides of each internal choice are retained.'),
    'cae58822c07e7e8f':('exam-selection','Instructions: Section B, three of six independent questions. Every question is retained.'),
    '9499c498ff4b44c5':('exam-selection','Repeated Section A instruction: seven independent 10-mark questions, all retained.'),
    '6a51f955bb7c716d':('independent-task-selection','Q1 either (a) or (b): both independently marked alternatives are retained.'),
    '11fe9c7f90da3413':('independent-task-selection','Q3 either (a) or (b): both alternatives are retained.'),
    '6d1fc746a03ac8cc':('independent-task-selection','Q8 either (a) or (b): both alternatives are retained.'),
    '2f2efcba6a37013a':('independent-task-selection','Q11 either (a) or (b): both alternatives are retained.'),
    'e6b887262892b9a6':('closed','Q12(b): a characteristic of a named pig, horse or poultry breed; the scheme answers for Landrace, Large White, Rhode Island Red and Irish Sport Horse, kept as answer routes on one card.'),
    '91da7ffbc8313021':('exam-selection','Section B heading: three of six independent 50-mark questions, all retained.'),
    '7298acb588a1ac0f':('not-a-selection','"a farmer would choose" in Q14(a)(i) is the farmer\'s breeding decision, not a response choice; the scheme\'s breeds are a marking menu.'),
    '48656172bf06e787':('open','Q14(a)(ii): any three hygiene ways from the scheme\'s list; a marking menu, not a printed item choice.'),
    '2336d1655183ff65':('open','Q14(a)(iii): any two milk tests from the scheme\'s list; a marking menu, not a printed item choice.'),
    'fbdb6acf218bdd9b':('open','Q15(a)(ii): a reason for any grass the student named at part (i); a marking menu.'),
    '641f3d80ee58032d':('independent-task-selection','Q16: (a) and (b) with either (c) or (d). Every part, including both (c) and (d), is retained.'),
    'b74a4f78e4b2ce70':('independent-task-selection','Q18: (a) and (b) with either (c) or (d). Every part, including both (c) and (d), is retained.'),
    '9be212ee2fd9a1a1':('closed','Q18(b)(iii): one physical trait of either animal with its reason; the scheme\'s good conformation, polled and smaller calves traits are kept as answer routes on one card.'),
}
SUPPLEMENTARY = [
    (3,'by placing a tick','answer-identification','Q1(a)(i)-(iii): one correct box per photograph (oilseed rape, barley, clover).'),
    (9,'using words from the list','answer-identification','Q6: each word from the list completes one sentence.'),
    (9,'Indicate whether each of the following is true or false','answer-identification','Q7(a)-(e): one correct box per statement.'),
    (13,'Indicate by placing an X on the diagram','answer-identification','Q10(d): one correct position (the cervix).'),
    (15,'Place an X on the plan view above','open','Q11(b)(iv): any of the scheme\'s three slatted-tank positions, with its reason; one card.'),
    (16,'Identify each breed using the list of names','answer-identification','Q12(a): each photograph has one breed in the list.'),
    (24,'State one error that could occur during this investigation','closed','Q14(b)(iii): each published error with its own remedy, kept as answer routes on one card.'),
    (24,'State whether the results obtained from the investigation','closed','Q14(b)(iv): qualitative (resazurin) or quantitative (total bacterial count), kept as answer routes on one card.'),
    (28,'State one implication the result has on the management of the field','closed','Q16(c)(v): each published implication with its own reason, kept as answer routes on one card.'),
    (33,'Discuss the production of a named crop that you have studied','open','Q18(a)(i): any named crop, 2 marks; the scheme\'s potatoes-only and tillage-only points stay qualifiers within one menu.'),
]
TOPIC = 'agricultural-science-ordinary-'
SNAPSHOT = ROOT / 'scripts/markbank/authored/agricultural-science-corrected-originals.json'
PREFIX = 'agsci-2021-ol-'
RESTORED = []
PAGE4 = 'The scheme\'s own rule (PDF page 4): "the first correct answer encountered is awarded" the first mark, and each later correct answer the next.'

P = lambda *r: [region(*x) for x in r]
REGIONS = {
    'Q1(a)': (P((3, .148, .62)), P((11, .137, .217))),
    'Q1(a)(iv)': (P((3, .148, .20), (3, .636, .678)), P((11, .213, .292))),
    'Q1(b)(i)': (P((4, .065, .58)), P((11, .29, .40))),
    'Q1(b)(ii)': (P((4, .065, .44), (4, .588, .612)), P((11, .398, .445))),
    'Q2(a)': (P((5, .065, .60)), P((11, .447, .523))),
    'Q2(b)': (P((5, .065, .11), (5, .61, .65)), P((11, .523, .628))),
    'Q3(a)(i)': (P((6, .065, .137)), P((11, .628, .706))),
    'Q3(a)(ii)': (P((6, .065, .113), (6, .208, .232)), P((11, .706, .784))),
    'Q3(a)(iii)': (P((6, .065, .113), (6, .363, .387)), P((11, .784, .9))),
    'Q3(b)(i)': (P((6, .518, .566)), P((12, .085, .167))),
    'Q3(b)(ii)': (P((6, .065, .09), (6, .643, .667)), P((12, .167, .249))),
    'Q3(b)(iii)': (P((6, .065, .09), (6, .714, .739)), P((12, .249, .345))),
    'Q4(a)': (P((7, .065, .432)), P((12, .357, .421))),
    'Q4(b)': (P((7, .065, .33), (7, .441, .465)), P((12, .421, .468))),
    'Q4(c)': (P((7, .065, .33), (7, .535, .559)), P((12, .468, .615))),
    'Q5(a)': (P((8, .065, .224)), P((12, .628, .675))),
    'Q5(b)': (P((8, .065, .155), (8, .294, .318)), P((12, .675, .791))),
    'Q5(c)': (P((8, .065, .155), (8, .508, .533)), P((12, .791, .838))),
    'Q5(d)': (P((8, .065, .155), (8, .572, .597)), P((12, .838, .905))),
    'Q6(a)–(e)': (P((9, .065, .45)), P((13, .085, .2))),
    'Q7(a)': (P((9, .487, .652)), P((13, .205, .249))),
    'Q7(b)': (P((9, .487, .62), (9, .662, .687)), P((13, .205, .228), (13, .249, .267))),
    'Q7(c)': (P((9, .487, .62), (9, .697, .722)), P((13, .205, .228), (13, .267, .285))),
    'Q7(d)': (P((9, .487, .62), (9, .731, .772)), P((13, .205, .228), (13, .285, .303))),
    'Q7(e)': (P((9, .487, .62), (9, .781, .822)), P((13, .205, .228), (13, .303, .324))),
    'Q8(a)(i)': (P((10, .065, .183)), P((13, .327, .374))),
    'Q8(a)(ii)': (P((10, .065, .148), (10, .245, .362)), P((13, .374, .438))),
    'Q8(a)(iii)': (P((10, .065, .09), (10, .368, .432)), P((13, .438, .502))),
    'Q8(a)(iv)': (P((10, .065, .09), (10, .504, .568)), P((13, .502, .568))),
    'Q8(b)(i)': (P((11, .065, .20)), P((13, .57, .632))),
    'Q8(b)(ii)': (P((11, .065, .09), (11, .205, .386)), P((13, .632, .728))),
    'Q8(b)(iii)': (P((11, .065, .09), (11, .492, .536)), P((13, .728, .88))),
    'Q9(a)': (P((12, .065, .44)), P((14, .085, .131))),
    'Q9(b)': (P((12, .065, .375), (12, .445, .469)), P((14, .131, .212))),
    'Q9(c)': (P((12, .599, .658)), P((14, .212, .45))),
    'Q10(a)': (P((13, .065, .346)), P((14, .46, .506))),
    'Q10(b)': (P((13, .065, .32), (13, .386, .41)), P((14, .506, .571))),
    'Q10(c)': (P((13, .48, .61)), P((14, .571, .638))),
    'Q10(d)': (P((13, .065, .32), (13, .623, .687)), P((14, .638, .70))),
    'Q11(a)(i)': (P((14, .065, .447)), P((15, .085, .131))),
    'Q11(a)(ii)': (P((14, .065, .42), (14, .485, .51)), P((15, .131, .23))),
    'Q11(a)(iii)': (P((14, .065, .42), (14, .64, .665)), P((15, .23, .294))),
    'Q11(a)(iv)': (P((14, .065, .42), (14, .733, .776)), P((15, .294, .392))),
    'Q11(b)(i)': (P((15, .065, .421)), P((15, .393, .491))),
    'Q11(b)(ii)': (P((15, .065, .39), (15, .49, .515)), P((15, .491, .555))),
    'Q11(b)(iii)': (P((15, .065, .13), (15, .585, .627)), P((15, .555, .619))),
    'Q11(b)(iv)': (P((15, .065, .39), (15, .727, .771)), P((15, .619, .725))),
    'Q12(a)': (P((16, .065, .60)), P((16, .085, .199))),
    'Q12(b)': (P((16, .611, .686)), P((16, .199, .5))),
    'Q13(a)(i)': (P((19, .155, .397)), P((17, .137, .185))),
    'Q13(a)(ii)': (P((19, .155, .372), (19, .436, .46)), P((17, .185, .231))),
    'Q13(a)(iii)': (P((19, .155, .372), (19, .528, .554)), P((17, .231, .348))),
    'Q13(b)(i)': (P((20, .065, .415)), P((17, .348, .387))),
    'Q13(b)(ii)': (P((20, .065, .44)), P((17, .387, .444))),
    'Q13(c)(i)': (P((20, .509, .533)), P((17, .444, .501))),
    'Q13(c)(ii)': (P((20, .603, .688)), P((17, .501, .558))),
    'Q13(c)(iii)': (P((20, .697, .739)), P((17, .558, .623))),
    'Q13(c)(iv)': (P((21, .065, .09)), P((17, .623, .749))),
    'Q13(c)(v)': (P((21, .28, .322)), P((17, .749, .915))),
    'Q14(a)(i)': (P((22, .065, .131)), P((18, .085, .141))),
    'Q14(a)(ii)': (P((22, .201, .26)), P((18, .141, .25))),
    'Q14(a)(iii)': (P((22, .451, .51)), P((18, .25, .307))),
    'Q14(a)(iv)': (P((22, .64, .682)), P((18, .307, .416))),
    'Q14(b)(i)': (P((23, .065, .131)), P((18, .416, .489))),
    'Q14(b)(ii)': (P((23, .065, .107), (23, .201, .243)), P((18, .489, .726))),
    'Q14(b)(iii)': (P((23, .065, .107), (24, .065, .107)), P((18, .726, .818))),
    'Q14(b)(iv)': (P((23, .065, .107), (24, .291, .332)), P((18, .818, .905))),
    'Q15(a)(i)': (P((25, .065, .114)), P((19, .085, .131))),
    'Q15(a)(ii)': (P((25, .065, .09), (25, .184, .208)), P((19, .131, .195))),
    'Q15(a)(iii)': (P((25, .278, .319)), P((19, .195, .297))),
    'Q15(b) Time of year of cutting': (P((25, .45, .522)), P((19, .297, .343))),
    'Q15(b) Fertiliser requirements': (P((25, .45, .491), (25, .567, .592)), P((19, .297, .318), (19, .343, .4))),
    'Q15(b) Harvesting and storage': (P((25, .45, .491), (25, .637, .661)), P((19, .297, .318), (19, .4, .487))),
    'Q15(c)(i)': (P((26, .065, .33)), P((19, .487, .573))),
    'Q15(c)(ii)': (P((26, .065, .199), (26, .373, .415)), P((19, .573, .651))),
    'Q15(c)(iii)': (P((26, .065, .199), (26, .597, .64)), P((19, .651, .795))),
    'Q15(c)(iv)': (P((26, .768, .795)), P((19, .795, .84))),
    'Q16(a)': (P((27, .065, .45)), P((20, .085, .39))),
    'Q16(b)(i)': (P((27, .065, .09), (27, .513, .538)), P((20, .39, .576))),
    'Q16(b)(ii)': (P((27, .065, .09), (27, .728, .753)), P((20, .576, .69))),
    'Q16(c)(i)': (P((28, .065, .114)), P((21, .085, .185))),
    'Q16(c)(ii)': (P((28, .065, .09), (28, .237, .296)), P((21, .185, .281))),
    'Q16(c)(iii)': (P((28, .065, .09), (28, .443, .57)), P((21, .281, .367))),
    'Q16(c)(iv)': (P((28, .065, .09), (28, .443, .57), (28, .616, .657)), P((21, .367, .431))),
    'Q16(c)(v)': (P((28, .065, .09), (28, .443, .57), (28, .75, .792)), P((21, .431, .515))),
    'Q16(d)(i)': (P((29, .065, .114)), P((21, .515, .648))),
    'Q16(d)(ii)': (P((29, .065, .09), (29, .237, .261)), P((21, .648, .764))),
    'Q16(d)(iii)': (P((29, .065, .09), (29, .445, .504)), P((21, .764, .878))),
    'Q17(a)(i)': (P((30, .065, .268)), P((22, .085, .166))),
    'Q17(a)(ii)': (P((30, .065, .241), (30, .448, .473)), P((22, .166, .247))),
    'Q17(a)(iii)': (P((30, .065, .241), (30, .54, .567)), P((22, .247, .311))),
    'Q17(a)(iv)': (P((30, .065, .241), (30, .636, .661)), P((22, .311, .393))),
    'Q17(a)(v)': (P((30, .065, .241), (31, .065, .179)), P((22, .393, .478))),
    'Q17(a)(vi)': (P((30, .065, .241), (31, .355, .397)), P((22, .478, .525))),
    'Q17(a)(vii)': (P((30, .065, .241), (31, .467, .508)), P((22, .525, .607))),
    'Q17(b)(i)': (P((32, .065, .486)), P((22, .607, .708))),
    'Q17(b)(ii)': (P((32, .065, .105), (32, .44, .537)), P((22, .708, .772))),
    'Q17(b)(iii)': (P((32, .637, .679)), P((22, .772, .868))),
    'Q18(a)(i) Seedbed preparation': (P((33, .065, .20)), P((23, .085, .222))),
    'Q18(a)(i) Weed control': (P((33, .065, .16), (33, .307, .331)), P((23, .085, .102), (23, .222, .286))),
    'Q18(a)(ii)': (P((33, .065, .09), (33, .431, .472)), P((23, .286, .368))),
    'Q18(a)(iii)': (P((33, .57, .715)), P((23, .368, .449))),
    'Q18(b)(i)': (P((34, .062, .089)), P((23, .449, .531))),
    'Q18(b)(ii)': (P((34, .187, .214)), P((23, .531, .612))),
    'Q18(b)(iii)': (P((34, .402, .717)), P((23, .612, .725))),
    'Q18(c)(i)': (P((35, .065, .273)), P((24, .085, .189))),
    'Q18(c)(ii)': (P((35, .065, .149), (35, .407, .79)), P((24, .189, .236))),
    'Q18(c)(iii)': (P((35, .065, .149), (35, .49, .74), (36, .062, .124)), P((24, .236, .30))),
    'Q18(c)(iv)': (P((35, .065, .149), (36, .222, .283)), P((24, .30, .366))),
    'Q18(d)(i)': (P((37, .065, .504)), P((24, .37, .43))),
    'Q18(d)(ii)': (P((37, .065, .46), (37, .572, .598)), P((24, .43, .477))),
    'Q18(d)(iii)': (P((37, .065, .158), (37, .666, .71)), P((24, .477, .558))),
    'Q18(d)(iv)': (P((38, .065, .79)), P((24, .558, .715))),
}
ATLAS = {
    'Q1': 'classification-of-organisms|crop-production', 'Q1(a)(iv)': 'classification-of-organisms|plant-physiology',
    'Q1(b)': 'classification-of-organisms|grassland', 'Q2': 'animal-physiology', 'Q3': 'crop-production',
    'Q3(a)(iii)': 'crop-production|fertilisers-pollution-the-environment', 'Q4': 'soil-science',
    'Q5': 'soil-science|scientific-practices-experiments-investigations', 'Q5(d)': 'soil-science', 'Q6': 'animal-production',
    'Q7': 'scientific-practices-experiments-investigations|innovation-and-biotechnology-in-agriculture', 'Q7(b)': 'animal-production',
    'Q7(d)': 'animal-production', 'Q8': 'health-safety', 'Q9': 'fertilisers-pollution-the-environment',
    'Q10': 'animal-physiology', 'Q10(d)': 'animal-physiology|animal-production', 'Q11': 'animal-production|health-safety',
    'Q11(a)(iv)': 'innovation-and-biotechnology-in-agriculture|animal-production', 'Q11(b)(iii)': 'innovation-and-biotechnology-in-agriculture|animal-production',
    'Q12': 'classification-of-organisms|animal-production', 'Q13': 'animal-diseases', 'Q13(c)(v)': 'animal-production|animal-diseases',
    'Q14': 'animal-production', 'Q14(b)': 'scientific-practices-experiments-investigations|animal-production',
    'Q15': 'grassland', 'Q15(c)(iv)': 'grassland|classification-of-organisms', 'Q16(a)': 'soil-science', 'Q16(b)': 'soil-science',
    'Q16(c)': 'soil-science|scientific-practices-experiments-investigations', 'Q16(d)': 'crop-production|soil-science',
    'Q17': 'scientific-practices-experiments-investigations|plant-physiology', 'Q17(a)(vii)': 'scientific-practices-experiments-investigations|health-safety',
    'Q18(a)': 'crop-production', 'Q18(a)(ii)': 'crop-production|health-safety', 'Q18(a)(iii)': 'crop-production|innovation-and-biotechnology-in-agriculture',
    'Q18(b)': 'genetics|animal-production', 'Q18(c)': 'animal-production', 'Q18(d)': 'scientific-practices-experiments-investigations|crop-production',
    'Q18(d)(iv)': 'fertilisers-pollution-the-environment|soil-science',
}
BREEDS = [
    ('landrace', 'Landrace', ['floppy ears', 'long body', 'good conformation', 'light forequarters', 'excellent ham development', 'high carcase weight',
                              'good milk production', 'prolificacy']),
    ('large-white', 'Large White', ['upright ears', 'pale skin', 'high growth rate', 'high lean meat %', 'good terminal sires', 'good uniformity of pigs',
                                    'prolific & good at converting feed']),
    ('rhode-island-red', 'Rhode Island Red', ['red‐orange eyes', 'reddish‐brown beaks', 'yellow feet and legs', 'hardy breed', 'produce well on marginal feed',
                                              'lay 200 ‐ 300 eggs per year (prolific)', 'produce large eggs', 'eggs pale brown colour (market demands)',
                                              'produce medium weight eggs']),
    ('irish-sport-horse', 'Irish Sport Horse', ['athleticism', 'jumping ability', 'courage', 'intelligence', 'soundness']),
]
RESAZURIN = ['Place (equal amounts of) milk into the test tubes or suitable container', 'add (few drops 1 cm3) of Resazurin', 'place (in water bath) at 37oC',
             '15 to 30 minutes', 'repeat (test on the same milk sample of various ages over time (immediately / at 5 hours / 24 hours / 48 hours / 72 hours)',
             '(record) colour change or stated colour change (fresh ‐ blue = good quality (low TBC) / blue ‐ deep mauve = good /deep pink = fair / light pink = poor /white = poor )']
OTHER_TESTS = ('The scheme adds "OR Diagram showing an investigation relating to milk quality: Total Bacterial Count (TBC) using a serial dilution + growing on agar plate / '
               'SCC ‐ California Mastitis Test (CMT) / antibiotics (Delvo) / % Solids ‐ excess water / thermoduric ‐ serial dilution & agar plate / % protein + % butterfat / Methylene Blue".')
ERRORS = [('temperature', 'Water bath temperature', 'Wrong temperature on water bath', 'use thermometer to check temperature'),
          ('amount', 'Amount of Resazurin or milk', 'incorrect amount of Resazurin or milk', 'use pipette or dropper'),
          ('sterile', 'Dirty test tubes or containers', 'non sterile or dirty test tubes or containers', 'use sterile test tubes or containers'),
          ('timing', 'Observation of time', 'correct observation of time', 'use a watch or timer')]
IMPLICATIONS = [('compaction', 'Compaction or poaching', 'Compaction or poaching', 'soft ground'),
                ('germination', 'Late or failed germination or lower yields', 'late or failed germination of crops or lower yields of crops or later harvesting dates', 'cold soil temperatures'),
                ('disease', 'Higher incidence of disease', 'higher incident of disease', 'liverfluke')]
TRAITS = [('conformation', 'Good conformation', 'BB or AA ‐ good conformation (double muscle gene)', 'high % lean meat or high price'),
          ('polled', 'Polled (no horns)', 'AA ‐ polled (no horns)', 'less dangerous'),
          ('smaller-calves', 'Smaller calves', 'smaller calves', 'lower mortality rates')]
PLAN = 'agricultural-science-2021-OL-paper-p15-i0'
PLAN_STEM = ('Answer either (a) or (b). (b) The following is a plan view of a combined robot milking unit and cow housing for Claire and John who plan to '
             'convert their suckler farm to a dairy farm.')


def original_hash(card):
    return hashlib.sha256(json.dumps(card, ensure_ascii=False, sort_keys=True).encode()).hexdigest()


def paper_review():
    observed, supplementary = scan(YEAR, FILE, HASHES, SELECTIONS, SUPPLEMENTARY)
    return dict(year=YEAR, level='ordinary', lang='ev', paperFileid=FILE, hashes=HASHES,
                wholePaperVisualReview='reviewed', schemeBoundaryReview='reviewed',
                paperPagesInspected=list(range(1, 45)), schemePagesInspected=list(range(1, 27)),
                selectionDirectives=observed, supplementarySelections=supplementary,
                sourceNotes=[dict(questionN='18', questionRef='Q18(a)(i)', note='Scheme PDF page 23 prints "Named crop 2" above the Seedbed preparation (4+3) and Weed control (4) headings; the 2 marks sit on the Seedbed preparation card.')],
                independentBoundaryReview='113 base tasks, one card each (Q1(a)(i)-(iii) and Q6(a)-(e) stay one card under one instruction; Q15(b) and Q18(a)(i) are carded by printed heading). 77 original cards match a published boundary and tariff unchanged. 34 are corrected in place; cards are added for the missing Q11(b)(iv) and Q18(b)(iii).',
                cropVisualReview='Every distinct paper/scheme crop pair rendered and inspected.',
                runtimeReview='Integrated production-component cases at 1200px and 390px. Signed-in full-app navigation remains open.',
                remaining=['Irish edition comparison (deferred)', 'Full application navigation review', 'Corpus-wide reconciliation'])


def atlas_for(ref):
    match = re.match(r'(Q\d+)((?:\([a-z]+\))*)', ref)
    parts = re.findall(r'\([a-z]+\)', match.group(2))
    for n in range(len(parts), -1, -1):
        key = match.group(1) + ''.join(parts[:n])
        if key in ATLAS:
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
        t = dict(questionRef='2021 OL ' + ref, paperPage=pp[0]['p'], schemePage=sp[0]['p'], paperRegions=pp, schemeRegions=sp,
                 atlasNumbers={cid: str(1001 + len(tasks))}, cardIds=[cid],
                 examTopicIds=[TOPIC + t for t in atlas_for(ref).split('|')],
                 selection=selection or {'kind': 'none', 'reason': 'Required response at a published boundary. Scheme alternatives remain marking menus.'},
                 evidence='All 44 paper and 26 scheme pages visually inspected. Boundary and tariff checked against the independently transcribed census.')
        tasks.append(t)
        return t

    def keep(key, ref, selection=None):
        cid = PREFIX + key
        card = originals[cid]
        assert card['questionRef'] == '2021 OL ' + ref, (cid, card['questionRef'])
        t = task(cid, ref, selection)
        t['marksPerRoute'] = card['totalMarks']
        t['originalCard'] = 'unchanged'
        if cid in snapshot:
            assert original_hash(card) == snapshot[cid]['originalSha256']
            RESTORED.append(card)

    def source(ref, pp):
        return dict(kind='source-text', label='OFFICIAL QUESTION PAGE', title='Agricultural Science 2021 Ordinary — ' + ref,
                    pages=sorted({r['p'] for r in pp}), attribution='SEC Agricultural Science 2021 Ordinary Level examination paper — © State Examinations Commission.',
                    presentationNote='Open the original page for the published wording, photographs, tables and examination context.')

    def record(cid, t, reason):
        old = originals[cid]
        corrections[cid] = dict(originalSha256=original_hash(old), originalQuestionRef=old['questionRef'],
                                originalQuestionText=old['questionText'], originalTotalMarks=old['totalMarks'],
                                originalTariffModel=old['tariffModel'], reason=reason)
        t['originalCard'] = 'corrected-in-place'

    def add(key, ref, topic, concept, question, rows, stem=None, marks=None, tariff=None, selection=None, figure=None, extra_fields=None):
        cid = PREFIX + key
        assert cid not in originals, f'{cid} would replace an original card without a correction record'
        rows = [dict(row, id=f'r-{i+1}') for i, row in enumerate(rows)]
        pp, _ = REGIONS[ref]
        card = dict(id=cid, subjectId='agricultural-science', year=YEAR, level='ordinary',
                    section='A' if int(re.match(r'Q(\d+)', ref).group(1)) <= 12 else 'B', questionRef='2021 OL ' + ref,
                    topicId='agsci-' + topic, curriculumNodeIds=['agsci-' + topic],
                    conceptId=concept, questionText=question, rows=rows,
                    totalMarks=marks if marks is not None else sum(r['marks'] for r in rows),
                    tariffModel=tariff or {'kind': 'fixed'}, sourceMaterial=source(ref, pp))
        if stem: card['stem'] = stem
        if figure: card['figureKey'] = figure
        if extra_fields: card.update(extra_fields)
        t = task(cid, ref, selection)
        t['marksPerRoute'] = card['totalMarks']
        t['originalCard'] = 'added'
        cards.append(card)
        return card

    def fix(key, ref, changes, drop=(), correction=None, selection=None):
        cid = PREFIX + key
        card = copy.deepcopy(originals[cid])
        assert card['questionRef'] == '2021 OL ' + ref, (cid, card['questionRef'])
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

    def pool(key, ref, options, steps, notation, note, page, scheme_page, wording, problem, open_list=False, changes=None):
        old = originals[PREFIX + key]
        row = menu(options, steps, note)
        if open_list:
            row['openList'] = True
        return fix(key, ref, dict(rows=[row], tariffModel={'kind': 'fixed', 'notation': notation}, **(changes or {})), drop=('notes',),
                   correction=(f'Visually verified paper PDF page {page} and scheme PDF page {scheme_page} ({wording}, "{notation}"). {problem} '
                               f'Same ID, boundary and {old["totalMarks"]} marks; one row lists every published point.'))

    def routes(built):
        variants = [dict(id=slug, label=label, rows=[dict(row, id=f'r-{i+1}') for i, row in enumerate(rows)]) for slug, label, rows in built]
        return variants[0]['rows'], variants

    def first(steps):
        return f'Any {len(steps)}: the first correct earns {steps[0]} and the next {", ".join(map(str, steps[1:]))} ({"+".join(map(str, steps))}). {PAGE4}'

    # Section A ---------------------------------------------------------------
    fix('q1a', 'Q1(a)', dict(stem='Answer either (a) or (b).'),
        correction=('Visually verified paper PDF page 3 ("Identify each of the following plants by placing a tick (✓) in the correct box.", three photographs (i)-(iii) each with four named boxes) and scheme PDF page 11 (oilseed rape, barley, clover, 2 each). '
                    'The original stem was two tick-box names and the next page\'s "Or" run together ("Soyabean Cocksfoot Or"). Same ID, rows, figure, boundary and 6 marks; the stem is the paper\'s instruction line.'))
    for k, ref in [('q1a-iv', 'Q1(a)(iv)'), ('q1b-i', 'Q1(b)(i)'), ('q1b-ii', 'Q1(b)(ii)'), ('q2a', 'Q2(a)'), ('q2b', 'Q2(b)')]:
        keep(k, ref)
    pool('q3a-i', 'Q3(a)(i)', ['Growth of crops in a defined sequence', 'growing different crops in a field every year (in a particular order)', 'correct named example of sequence'],
         [2], '2', 'One explanation, 2 marks.', 6, 11, '"Explain the underlined term", three explanations',
         'The original left out "growing different crops in a field every year (in a particular order)".')
    keep('q3a-ii', 'Q3(a)(ii)')
    pool('q3a-iii', 'Q3(a)(iii)', ['Toxic (harmful to human health)', 'build‐up of toxins in food chain', 'cause pollution',
                                   'kill other plant or animal species (e.g. pollinators ‐ bees) or harmful to the environment', 'pollution of air or soil',
                                   'volatilisation of fertiliser (e.g. urea) can kill germinating seedlings', 'resistance to chemical', 'cost'],
         [3, 1], '3+1', first([3, 1]), 6, 11, '"Suggest two disadvantages of using chemical sprays in crop production", eight disadvantages',
         'The original left out "kill other plant or animal species (e.g. pollinators ‐ bees) or harmful to the environment".')
    keep('q3b-i', 'Q3(b)(i)')
    keep('q3b-ii', 'Q3(b)(ii)')
    pool('q3b-iii', 'Q3(b)(iii)', ['No chemicals used', 'no entry of chemicals into food chain (soil) or water source', 'lower cost to farmer', 'no resistance build up',
                                   'less labour required', 'self‐sustaining or long term solution', 'improves biodiversity'],
         [3, 1], '3+1', first([3, 1]), 6, 12, '"Outline two advantages of using biological controls in crop production", seven advantages',
         'The original left out "less labour required".')
    keep('q4a', 'Q4(a)')
    soils = 'Diagrams A and B show the profiles of two common soil types in Ireland.'
    fix('q4b', 'Q4(b)', dict(stem=soils),
        correction=('Visually verified paper PDF page 7 ("Diagrams A and B show the profiles of two common soil types in Ireland.", "(b) Outline one use for soil A.") and scheme PDF page 12 (2). '
                    'The original stem was the diagram\'s horizon labels run together ("Humus, rich dark brown colour Pale grey, heavily leached ... Parent rock Parent rock"). Same ID, rows, figure, boundary and 2 marks; the stem is the paper\'s lead-in.'))
    pool('q4c', 'Q4(c)', ['Poor drainage (due to the impermeable iron pan)', 'poor aeration (as air spaces fill with water)',
                          'acidic or low pH (due to poor decomposition of organic matter)', 'poor fertility (low CEC) (due to acid leaching)',
                          'poor root penetration (due to iron pan)', 'reduced crop yield (due to acidic nature of soil or poor drainage or poor aeration or waterlogging of soil)',
                          'poor establishment or yield or growth'],
         [3, 1], '3+1', first([3, 1]), 7, 12, '"Describe two disadvantages associated with the use of soil B", seven disadvantages',
         'The original pinned the 3 marks to poor drainage and the 1 to poor aeration, so either given first after another disadvantage was mispriced, and its stem was the diagram\'s labels run together.',
         changes=dict(stem=soils))
    keep('q5a', 'Q5(a)')
    pool('q5b', 'Q5(b)', ['Use (same amount of) soil for each', '(each) sample in a funnel', '(lined) with filter paper',
                          'add (same volume of) water (using graduated cylinder or beaker)',
                          'record time for (all) water to pass through (both samples) (into graduated cylinder or container) or compare volume of water collected from each sample'],
         [3, 1], '3+1', first([3, 1]), 8, 12, '"Describe how they measured the infiltration rate in this investigation", five steps',
         'The original left out "record time for (all) water to pass through (both samples) (into graduated cylinder or container)", keeping only its alternative.')
    for k, ref in [('q5c', 'Q5(c)'), ('q5d', 'Q5(d)'), ('q6', 'Q6(a)–(e)'), ('q7a', 'Q7(a)'), ('q7b', 'Q7(b)'), ('q7c', 'Q7(c)'), ('q7d', 'Q7(d)'), ('q7e', 'Q7(e)'),
                   ('q8a-i', 'Q8(a)(i)'), ('q8a-ii', 'Q8(a)(ii)')]:
        keep(k, ref)
    pool('q8a-iii', 'Q8(a)(iii)', ['Gloves', 'respirator or mask', 'overalls (apron)', 'goggles', 'wellington (rubber) boots'],
         [2, 2], '2(2)', 'Any two pieces of PPE, 2 marks each (2(2)). The scheme adds "or any two valid examples".', 10, 13,
         '"Suggest two pieces of PPE that you would recommend he wears", five pieces', 'The original left out "wellington (rubber) boots".', open_list=True)
    pool('q8a-iv', 'Q8(a)(iv)', ['Wear gloves or wash hands afterwards', 'avoid touching the infected area on the cattle'], [2], '2', 'One precaution, 2 marks.',
         10, 13, '"Briefly explain one precaution she should take to prevent transmission of ringworm", two precautions',
         'The original second precaution read "infected area on the cattle", dropping "avoid touching the".')
    keep('q8bi', 'Q8(b)(i)')
    pool('q8b-ii', 'Q8(b)(ii)', ['Have a clear exit plan', 'have stick or fork with you',
                                 'keep all children and dogs away or do not make loud noises or sudden movements', 'never turn your back on the cow'],
         [2], '2', 'One precaution, 2 marks. The scheme adds "other valid answer".', 11, 13,
         '"Describe one safety precaution a farmer would take when handling the cow and calf immediately post‐calving", four precautions',
         'The original left out "keep all children and dogs away or do not make loud noises or sudden movements".', open_list=True)
    pool('q8b-iii', 'Q8(b)(iii)', ['Remove all animals from the shed', 'ventilate the shed', 'open tractor windows', 'use a gas monitor', 'do not enter shed while agitating',
                                   'ensure another person is present', 'stay clear of all agitation points or open hatches', 'spread on a windy day',
                                   'don’t spread near electric wires (when using the splash plate)', 'keep all persons and animals away during spreading', 'cover on PTO',
                                   'ear safety equipment'],
         [3, 2, 1], '3+2+1', first([3, 2, 1]) + ' The scheme adds "other valid answer".', 11, 13,
         '"Outline three safety precautions he should take when agitating and spreading the slurry", twelve precautions',
         'The original left out "don’t spread near electric wires (when using the splash plate)".', open_list=True)
    keep('q9a', 'Q9(a)')
    pool('q9b', 'Q9(b)', ['Animal (respiration)', 'slurry', 'FYM', 'synthetic fertiliser', 'lime', 'soils or soil cultivation (ploughing)', 'machinery (fuel)',
                          'ruminant digestion (enteric fermentation)'],
         [3, 1], '3+1', first([3, 1]), 12, 14, '"List two sources of greenhouse gases from agriculture", eight sources',
         'The original cut "soils or soil cultivation (ploughing)" to "soils" and left out "ruminant digestion (enteric fermentation)".')
    for k, ref in [('q9c', 'Q9(c)'), ('q10a', 'Q10(a)')]:
        keep(k, ref)
    fix('q10b', 'Q10(b)', dict(rows=[point('(Produces) eggs or ovulation or produces oestrogen or progesterone', 2)]), drop=('notes',),
        correction=('Visually verified paper PDF page 13 ("Outline the function of the part labelled A.") and scheme PDF page 14 ("(Produces) eggs or ovulation or produces oestrogen or progesterone", 2). '
                    'The original answer stopped at "oestrogen" and re-worded the rest as "(Produces) progesterone". Same ID, figure, boundary and 2 marks; one row in the scheme\'s words.'))
    keep('q10c', 'Q10(c)')
    fix('q10d', 'Q10(d)', dict(stem='The following is the reproductive system of a cow. Look at the diagram and answer the questions which follow.'),
        correction=('Visually verified paper PDF page 13 (the lead-in and "(d) ... Indicate by placing an X on the diagram exactly where the top of the insemination gun needs to be positioned.") and scheme PDF page 14 (2). '
                    'The original stem ended with the diagram\'s labels run together ("Vulva Bladder"). Same ID, rows, figure, boundary and 2 marks.'))
    for k, ref in [('q11a-i', 'Q11(a)(i)'), ('q11a-ii', 'Q11(a)(ii)'), ('q11a-iii', 'Q11(a)(iii)'), ('q11a-iv', 'Q11(a)(iv)')]:
        keep(k, ref)
    pool('q11b-i', 'Q11(b)(i)', ['If animal (cow) is sick or injured (must have isolation area to put them in during treatment)',
                                 'don’t pass disease (infection) to other animals or humans'], [2], '2', 'One reason, 2 marks.',
         15, 15, '"Explain why they have included an isolation area on the plan", two reasons',
         'The original second reason read "animals or humans", dropping "don’t pass disease (infection) to other", and the card carried no plan.',
         changes=dict(stem=PLAN_STEM, figureKey=PLAN))
    keep('q11b-ii', 'Q11(b)(ii)')
    pool('q11b-iii', 'Q11(b)(iii)', ['Better work‐life balance', 'less labour needed', 'increased milk yield from cows'], [2], '2', 'One reason, 2 marks.',
         15, 15, '"Outline one reason why Claire and John would have opted to install a robotic milking machine", three reasons',
         'The original left out "increased milk yield from cows".')
    add('q11b-iv', 'Q11(b)(iv)', '4-3-3', 'siting-slatted-tanks',
        'Place an X on the plan view above to show one place where you would advise Claire and John to install slatted tanks. Give a reason for your answer.',
        [menu(['Where cows stand in the feeding passage', 'passage behind cubicles', 'entry or exit point to graze way'], [2],
              'X on the diagram, 2 marks: any one of the scheme\'s places.'),
         point('Reason ‐ areas with high levels of slurry or cows are feeding or cows are there longer', 2, 'Reason, 2 marks.')],
        PLAN_STEM, figure=PLAN)
    fix('q12a', 'Q12(a)', dict(questionText='The photographs show some common breeds of cattle and sheep. Identify each breed using the list of names and write your answer in the space provided: Limousin, Jacob, Border Leicester, Charolais.'),
        correction=('Visually verified paper PDF page 16 (four photographs A–D, the list Limousin, Jacob, Border Leicester, Charolais, and A:–D: lines) and scheme PDF page 16 (A Charolais, B Limousin, C Jacob, D Border Leicester, 2 each). '
                    'The original question ran the photograph letters and the word list into the sentence ("... in the space provided. A B C D Limousin Jacob Border Leicester Charolais"). Same ID, rows, figure, boundary and 8 marks.'))
    built = []
    for slug, label, traits in BREEDS:
        row = menu(traits, [2], f'{label}: one characteristic, 2 marks. No marks for naming the breed. The scheme adds "Or other valid answer".')
        row['openList'] = True
        built.append((slug, label, [row]))
    rows, variants = routes(built)
    fix('q12b', 'Q12(b)', dict(rows=rows, answerVariants=variants), drop=('notes',), selection=closed(1, [label for _, label, _ in BREEDS]),
        correction=('Visually verified paper PDF page 16 ("Describe one characteristic of a named breed of either pig or horse or poultry that you have studied.", a Named breed line) and scheme PDF page 16 '
                    '("(0m for naming breed)", Landrace, Large White, Rhode Island Red and Irish Sport Horse characteristics, 2). The original printed the whole Landrace list as one answer with the other breeds\' lists as accepted wordings. '
                    'Same ID, boundary and 2 marks; each breed is an answer route the student chooses before reveal, listing its characteristics one each.'))
    # Section B ---------------------------------------------------------------
    for k, ref in [('q13a-i', 'Q13(a)(i)'), ('q13a-ii', 'Q13(a)(ii)'), ('q13a-iii', 'Q13(a)(iii)'), ('q13b-i', 'Q13(b)(i)'), ('q13b-ii', 'Q13(b)(ii)'),
                   ('q13c-i', 'Q13(c)(i)'), ('q13c-ii', 'Q13(c)(ii)'), ('q13c-iii', 'Q13(c)(iii)')]:
        keep(k, ref)
    pool('q13c-iv', 'Q13(c)(iv)', ['Operate closed herd (breed own replacements)', 'footbath or disposable footwear and clothing', 'limit visitors', 'fence boundaries',
                                   'quarantine new animals or isolate sick animals', 'do not share equipment or machinery or colostrum', 'disinfect trailers (machinery)',
                                   'use of AI (Artificial Insemination)', 'information signage'],
         [2, 2, 1], '2+2+1', first([2, 2, 1]) + ' The scheme adds "other valid answer".', 21, 17,
         '"State three practices farmers could employ to ensure good biosecurity on their farm", nine practices',
         'The original left out "do not share equipment or machinery or colostrum".', open_list=True)
    for k, ref in [('q13c-v', 'Q13(c)(v)'), ('q14a-i', 'Q14(a)(i)'), ('q14a-ii', 'Q14(a)(ii)'), ('q14a-iii', 'Q14(a)(iii)'), ('q14a-iv', 'Q14(a)(iv)'), ('q14b-i', 'Q14(b)(i)')]:
        keep(k, ref)
    pool('q14b-ii', 'Q14(b)(ii)', RESAZURIN, [3, 3, 3], '3(3)', 'Any three steps, 3 marks each (3(3)); "Diagram or text showing the following". ' + OTHER_TESTS,
         23, 18, '"Describe, using a labelled diagram, a method the farmer could use to carry out this investigation", six resazurin steps "OR" another milk-quality test',
         'The original left out "15 to 30 minutes" and the alternative tests, and cut the repeat and colour steps short.', open_list=True)
    rows, variants = routes([(slug, label, [point(error, 2, 'Error, 2 marks.'), point(remedy, 1, 'Reducing that error, 1 mark (2+1).')])
                             for slug, label, error, remedy in ERRORS])
    fix('q14b-iii', 'Q14(b)(iii)', dict(rows=rows, answerVariants=variants), drop=('notes',), selection=closed(1, [label for _, label, _, _ in ERRORS]),
        correction=('Visually verified paper PDF page 24 ("State one error that could occur during this investigation and outline one way that this error could be reduced", Error: and Reduce error: lines) and scheme PDF page 18 '
                    '(four errors, each with its remedy, "2+1"). The original row pinned the water-bath error and the thermometer remedy, with the other errors and remedies as unpaired accepted wordings, so an error could be credited with another error\'s remedy. '
                    'Same ID, boundary and 3 marks; each error is an answer route with its own remedy.'))
    rows, variants = routes([('resazurin', 'Qualitative (resazurin test)', [point('Result ‐ Qualitative (Resazurin test)', 2, 'Result, 2 marks.'),
                                                                            point('Justify Result ‐ colour change not measured numerically', 1, 'Justification, 1 mark (2+1). The scheme adds "(accept matching answer to valid test)".')]),
                             ('tbc', 'Quantitative (total bacterial count)', [point('Quantitative ‐ TBC', 2, 'Result, 2 marks.'),
                                                                               point('no. of CFU’s', 1, 'Justification, 1 mark (2+1).')])])
    fix('q14b-iv', 'Q14(b)(iv)', dict(rows=rows, answerVariants=variants), drop=('notes',), selection=closed(1, ['Qualitative (resazurin test)', 'Quantitative (total bacterial count)']),
        correction=('Visually verified paper PDF page 24 ("State whether the results obtained from the investigation at part (ii) above are quantitative or qualitative. Justify your answer.") and scheme PDF page 18 '
                    '(qualitative for a resazurin test justified by colour change, quantitative for a TBC justified by the number of CFUs, "2+1", "(accept matching answer to valid test)"). The original mixed the two results and justifications on one route. '
                    'Same ID, boundary and 3 marks; each test is an answer route with its own result and justification.'))
    for k, ref in [('q15a-i', 'Q15(a)(i)'), ('q15a-ii', 'Q15(a)(ii)'), ('q15a-iii', 'Q15(a)(iii)'), ('q15b-time', 'Q15(b) Time of year of cutting'),
                   ('q15b-fertiliser', 'Q15(b) Fertiliser requirements'), ('q15b-harvest', 'Q15(b) Harvesting and storage'), ('q15c-i', 'Q15(c)(i)'), ('q15c-ii', 'Q15(c)(ii)')]:
        keep(k, ref)
    pool('q15c-iii', 'Q15(c)(iii)', ['Cut at leafy stage to increase sugar for fermentation', 'do not cut during or after rainfall as water dilutes the sugar content',
                                     'cut in the afternoon as photosynthesis produces more sugar',
                                     'ensure pit (bales) packed tightly to remove air to promote growth of anaerobic bacteria (lactobacillus)',
                                     'allow grass to wilt to increase sugar content', 'use additive (molasses or acid or inoculants) to achieve correct pH'],
         [4, 2], '4+2', first([4, 2]), 26, 19, '"Outline two ways the farmer could have achieved the target pH", six ways',
         'The original cut the packing point at "to remove air", dropping "to promote growth of anaerobic bacteria (lactobacillus)".')
    for k, ref in [('q15c-iv', 'Q15(c)(iv)'), ('q16a', 'Q16(a)'), ('q16b-i', 'Q16(b)(i)')]:
        keep(k, ref)
    pool('q16b-ii', 'Q16(b)(ii)', ['Divide the area (to be sampled into regions) (2 ‐ 4 ha in size)', 'Sample at correct depth (where crop roots are growing) (5 ‐ 10 cm)',
                                   'take account of different soil types or slopes or previous cropping history', 'W shape', 'random', 'min 20 samples',
                                   'stay away from water troughs or ditches or wet marshy ground', 'soil auger'],
         [4, 2], '4+2', first([4, 2]), 27, 20, '"Outline two steps involved in collecting samples of soil for analysis", eight steps',
         'The original left out "take account of different soil types or slopes or previous cropping history".')
    keep('q16c-i', 'Q16(c)(i)')
    old = originals[PREFIX + 'q16c-ii']
    fix('q16c-ii', 'Q16(c)(ii)', dict(rows=[old['rows'][0], menu(['Lime regularly or reduce slurry', 'raise pH >6', 'poor grass growth as pH too low'], [2], 'Advice, 2 marks: any one.')]),
        drop=('notes',),
        correction=('Visually verified paper PDF page 28 ("Outline the effect this pH level has on the number of earthworms in the field and the advice you would give the farmer to ensure good grass growth.") and scheme PDF page 21 '
                    '("Number: Low earthworm numbers" 3, "Advice: Lime regularly or reduce slurry / raise pH >6 / poor grass growth as pH too low" 2). The original advice row left out "poor grass growth as pH too low". Same ID, boundary and 5 marks.'))
    for k, ref in [('q16c-iii', 'Q16(c)(iii)'), ('q16c-iv', 'Q16(c)(iv)')]:
        keep(k, ref)
    rows, variants = routes([(slug, label, [point('Implication — ' + implication, 2, 'Implication, 2 marks.'), point('Reason — ' + reason, 2, 'Its reason, 2 marks (2+2).')])
                             for slug, label, implication, reason in IMPLICATIONS])
    fix('q16c-v', 'Q16(c)(v)', dict(rows=rows, answerVariants=variants), drop=('notes',), selection=closed(1, [label for _, label, _, _ in IMPLICATIONS]),
        correction=('Visually verified paper PDF page 28 ("State one implication the result has on the management of the field and give one reason for your answer.") and scheme PDF page 21 '
                    '(three implications each paired with its reason, "2+2"). The original paired compaction with soft ground and left the other implications unpaired, without the cold-soil reason. '
                    'Same ID, boundary and 4 marks; each implication is an answer route with its own reason.'))
    pool('q16d-i', 'Q16(d)(i)', ['No GMO’s', 'no chemicals used (herbicides or pesticides or antibiotics or fertilisers)',
                                 'tillage practices which increase OM or increase soil stability or soil health', 'tillage practices to prevent compaction and erosion',
                                 'use organic fertilisers (e.g. slurry, seaweed)', 'use organic certified seed'],
         [4, 4], '4+4', 'Any two principles, 4 marks each (4+4).', 29, 21, '"State two principles of organic food production", six principles',
         'The original left out "tillage practices to prevent compaction and erosion".')
    for k, ref in [('q16d-ii', 'Q16(d)(ii)'), ('q16d-iii', 'Q16(d)(iii)'), ('q17a-i', 'Q17(a)(i)'), ('q17a-ii', 'Q17(a)(ii)')]:
        keep(k, ref)
    pool('q17a-iii', 'Q17(a)(iii)', ['Amount or type of seeds', 'same soil type', 'volume of soil', 'volume of water', 'time'],
         [4, 3], '4+3', first([4, 3]), 30, 22, '"List two factors that the student kept constant (fixed) during the investigation", five factors',
         'The original left out "volume of water".')
    pool('q17a-iv', 'Q17(a)(iv)', ['if sown too deep the seeds won’t (have enough energy) to get above ground',
                                   'if not sown deep enough they are more prone to attack from birds or drying out (desiccation)'],
         [3], '3', 'One effect, 3 marks.', 30, 22, '"How would the depth of sowing of the seeds affect the germination rate?", two effects',
         'The original second effect dropped "if not sown deep enough they are".')
    for k, ref in [('q17a-v', 'Q17(a)(v)'), ('q17a-vi', 'Q17(a)(vi)'), ('q17a-vii', 'Q17(a)(vii)'), ('q17b-i', 'Q17(b)(i)')]:
        keep(k, ref)
    pool('q17b-ii', 'Q17(b)(ii)', ['Sowing seeds at 25oC will give best germination rates', 'increase soil temp (25oC) get majority of seeds to germinate'],
         [3], '3', 'One piece of advice, 3 marks.', 32, 22, '"State one piece of advice you would give to farmers on the sowing of grass seed", two pieces of advice',
         'The original left out "increase soil temp (25oC) get majority of seeds to germinate".')
    keep('q17b-iii', 'Q17(b)(iii)')
    fix('q18a-i-seedbed', 'Q18(a)(i) Seedbed preparation', dict(
        stem='Answer both (a) and (b) with either (c) or (d). The paper prints a Named Crop line above the Seedbed preparation and Weed control headings.',
        rows=[point('Named crop', 2, 'Naming the crop, 2 marks; the seedbed and weed-control points must suit the crop named.'),
              menu(['Plough', 'harrow to produce fine tilth', 'pick stones to prevent damage to crop (potatoes only)', 'produce fine firm seedbed or ridge (potatoes only)',
                    'min‐till to minimise travelling or minimise compaction or minimise soil disturbance (tillage only)'], [4, 3], 'Seedbed preparation: ' + first([4, 3]))],
        tariffModel={'kind': 'fixed', 'notation': '2 + 4+3'}, totalMarks=9), drop=('notes',),
        correction=('Visually verified paper PDF page 33 ("Discuss the production of a named crop that you have studied under the following headings.", Named Crop:, Seedbed preparation: and Weed control: lines) and scheme PDF page 23 '
                    '("Named crop 2", Seedbed preparation "4+3", Weed control "4"), which is the 13 marks part (a)(i) needs for Question 18 to total 50. '
                    'The original priced the seedbed heading alone at 7 and left out both the 2 marks for naming the crop and "pick stones to prevent damage to crop (potatoes only)". '
                    'Same ID and heading; the card now carries the named crop at 2 and every published seedbed point at 4+3, 9 marks.'))
    for k, ref in [('q18a-i-weeds', 'Q18(a)(i) Weed control'), ('q18a-ii', 'Q18(a)(ii)'), ('q18a-iii', 'Q18(a)(iii)')]:
        keep(k, ref)
    pool('q18b-i', 'Q18(b)(i)', ['Process through which populations of living organisms adapt and change',
                                 'organisms better adapted to their environment tend to survive and produce more offspring'],
         [2], '2', 'One explanation, 2 marks.', 34, 23, '"Explain natural selection.", two explanations',
         'The original left out "or organisms better adapted to their environment tend to survive and produce more offspring".')
    keep('q18b-ii', 'Q18(b)(ii)')
    rows, variants = routes([(slug, label, [point(trait, 2, 'Physical trait, 2 marks.'), point(reason, 2, 'Its advantage to beef farmers, 2 marks.')])
                             for slug, label, trait, reason in TRAITS])
    add('q18b-iii', 'Q18(b)(iii)', '4-3-2', 'selectively-bred-beef-traits',
        'The following are pictures of two beef cattle breeds, Aberdeen Angus and Belgian Blue. Both breeds have been selectively bred based on physical traits. '
        'State one physical trait, in either of the animals above, and give one reason why this trait is an advantage to beef farmers.',
        rows, 'Answer both (a) and (b) with either (c) or (d).', selection=closed(1, [label for _, label, _, _ in TRAITS]),
        figure='agricultural-science-2021-OL-paper-p34-i0', extra_fields={'answerVariants': variants})
    for k, ref in [('q18c-i', 'Q18(c)(i)'), ('q18c-ii', 'Q18(c)(ii)')]:
        keep(k, ref)
    pool('q18c-iii', 'Q18(c)(iii)', ['Lambs are putting weight on in a consistent manner', 'putting on similar weight every week', 'growth rate and age are proportional'],
         [4], '4', 'One description, 4 marks.', 36, 24, '"Briefly describe what this information tells the farmer about the growth rate of the lambs", three descriptions',
         'The original left out "putting on similar weight every week", re-worded the question ("The graph of these liveweights against age ...") and carried no graph.',
         changes=dict(questionText='The graph at part (ii) is almost a straight line. Briefly describe what this information tells the farmer about the growth rate of the lambs.',
                      figureKey='agricultural-science-2021-OL-paper-p35-i0'))
    for k, ref in [('q18c-iv', 'Q18(c)(iv)'), ('q18d-i', 'Q18(d)(i)'), ('q18d-ii', 'Q18(d)(ii)')]:
        keep(k, ref)
    pool('q18d-iii', 'Q18(d)(iii)', ['Cut shoot at base of plant and measure length with a ruler', 'hold the shoot straight and measure the length with a ruler',
                                     'use a thread (string) to measure plant and then measure with a ruler'],
         [2], '2', 'One way, 2 marks.', 37, 24, '"Outline one way in which the student could have measured the shoot length", three ways',
         'The original left out "use a thread (string) to measure plant and then measure with a ruler".')
    keep('q18d-iv', 'Q18(d)(iv)')
    assert len(tasks) == 113 and len(corrections) == 34 and len(originals) == 111 and len(cards) == 36, (len(tasks), len(cards), len(corrections), len(originals))
    assert {t['cardIds'][0] for t in tasks} >= set(originals), 'Every original 2021 Ordinary card must be reviewed'
    return cards, tasks, corrections
