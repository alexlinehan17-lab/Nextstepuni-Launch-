"""2016 Ordinary: every task authored from the SEC paper and marking scheme (no cards existed).

All 16 paper pages and 20 scheme pages were inspected and the independent census transcribed
before authoring: 69 base tasks, one card each. Section One questions are one task each: where
the scheme prints one scale across several parts (Q5, Q6, Q7) the question states the scale
(orderedSplit); where every part carries its own marks (Q1-Q4) the rows carry them. Section Two
parts are priced on their own, and the four Q11(a) headings carry 4 marks each. The pasture
sowing methods (Q8(a)(iii)), the lowland breeds (Q13(a)(ii)) and the two carbon dioxide
experiments (Q13(d)(iii)) are answer routes. Answers are the scheme's words.
"""
from agricultural_science_legacy import Paper, P, point, menu, closed, routes

FILE = 'LC024GLP000EV.pdf'
HASHES = {'exampapers': '688b5ed62a73c3b3d1bd877428c18f4843cb071a8b99d1580bd493f101901b38',
          'markingschemes': '2490229e979602112b9af92d4f48677e28ab1c4b7f794ee5e730bc5cb6068473'}
SELECTIONS = {
    '0e97cd518756c458': ('exam-selection', 'Section One: six of seven independent 20-mark questions; every question is retained.'),
    'b4ea10786cd5231a': ('not-a-selection', '"One of the flasks was used as a control" is Q1(b)(iv)\'s lead-in, not a choice.'),
    '3febd40a7e3c11ee': ('exam-selection', 'Section Two: three of six independent 60-mark questions; every question is retained.'),
    '62bc3a27901d580d': ('open', 'Q8(c): any two of the scheme\'s four silage tests; a marking menu, four points from each test chosen.'),
    '0c0455d0ba96aac8': ('independent-task-selection', 'Q13: two of four independently priced 30-mark parts; all four are retained.'),
    '0a7417c4e3e78d6c': ('open', 'Q13(a)(i): any two of the scheme\'s five lowland breeds; a marking menu.'),
    '325750fecd3e4a87': ('closed', 'Q13(a)(ii): characteristics of one of the breeds named, kept as five answer routes on one card.'),
}
SUPPLEMENTARY = [
    (9, 'Describe one method of sowing a field for pasture', 'closed', 'Q8(a)(iii): the scheme gives direct sowing, undersowing, direct drilling and stitching-in, kept as answer routes on one card.'),
    (13, 'a laboratory experiment to show that carbon', 'closed', 'Q13(d)(iii): the scheme gives Method A (soda lime) or Method B (pondweed), kept as answer routes on one card.'),
]
ATLAS = {
    'Q1': 'soil-science|scientific-practices-experiments-investigations', 'Q2': 'animal-physiology|animal-diseases|grassland|soil-science|animal-production',
    'Q3': 'animal-production|soil-science|crop-production|fertilisers-pollution-the-environment', 'Q4': 'scientific-practices-experiments-investigations',
    'Q5': 'plant-physiology|classification-of-organisms', 'Q6': 'animal-diseases|crop-production|classification-of-organisms', 'Q7': 'crop-production',
    'Q8': 'grassland', 'Q8(c)': 'grassland|scientific-practices-experiments-investigations',
    'Q9(a)(i)': 'animal-physiology', 'Q9(a)(ii)': 'animal-physiology', 'Q9(a)': 'animal-diseases', 'Q9(b)': 'animal-physiology', 'Q9(c)': 'animal-diseases',
    'Q10': 'crop-production', 'Q10(c)': 'crop-production|scientific-practices-experiments-investigations',
    'Q11(a)': 'soil-science', 'Q11(b)': 'soil-science', 'Q11(b)(iii)': 'soil-science|classification-of-organisms', 'Q11(b)(iv)': 'soil-science|classification-of-organisms',
    'Q11(c)': 'fertilisers-pollution-the-environment|soil-science', 'Q11(c)(i)': 'plant-physiology|fertilisers-pollution-the-environment',
    'Q12': 'genetics', 'Q12(d)': 'genetics|animal-production',
    'Q13(a)': 'animal-production', 'Q13(b)': 'animal-production', 'Q13(b)(iii)': 'animal-production|animal-diseases', 'Q13(c)': 'animal-production',
    'Q13(c)(i)': 'animal-production|animal-diseases', 'Q13(d)': 'plant-physiology', 'Q13(d)(iii)': 'plant-physiology|scientific-practices-experiments-investigations',
}
REGIONS = {
    # Drafted by regions.py.
    'Q1': (P((2, 0.212, 0.941)), P((5, 0.081, 0.341))),
    'Q2': (P((3, 0.046, 0.491)), P((5, 0.341, 0.555))),
    'Q3': (P((4, 0.031, 0.767)), P((5, 0.555, 0.873))),
    'Q4': (P((5, 0.031, 0.927)), P((6, 0.048, 0.314))),
    'Q5': (P((6, 0.031, 0.922)), P((6, 0.314, 0.626))),
    'Q6': (P((7, 0.031, 0.758)), P((6, 0.626, 0.912))),
    'Q7': (P((8, 0.031, 0.907)), P((7, 0.048, 0.529))),
    'Q8(a)(i)': (P((9, 0.202, 0.289)), P((8, 0.083, 0.198))),
    'Q8(a)(ii)': (P((9, 0.202, 0.270), (9, 0.289, 0.304)), P((8, 0.083, 0.119), (8, 0.198, 0.510))),
    'Q8(a)(iii)': (P((9, 0.202, 0.270), (9, 0.304, 0.345)), P((8, 0.083, 0.119), (8, 0.510, 0.928))),
    'Q8(b)(i)': (P((9, 0.202, 0.270), (9, 0.345, 0.379)), P((8, 0.083, 0.103), (9, 0.047, 0.129))),
    'Q8(b)(ii)': (P((9, 0.202, 0.270), (9, 0.345, 0.364), (9, 0.379, 0.420)), P((8, 0.083, 0.103), (9, 0.129, 0.210))),
    'Q8(c)': (P((9, 0.202, 0.270), (9, 0.420, 0.474)), P((8, 0.083, 0.103), (9, 0.210, 0.563))),
    'Q9(a)(i)': (P((10, 0.031, 0.369)), P((10, 0.048, 0.196))),
    'Q9(a)(ii)': (P((10, 0.031, 0.349), (10, 0.369, 0.386)), P((10, 0.048, 0.100), (10, 0.196, 0.245))),
    'Q9(a)(iii)': (P((10, 0.031, 0.349), (10, 0.386, 0.421)), P((10, 0.048, 0.100), (10, 0.245, 0.327))),
    'Q9(a)(iv)': (P((10, 0.031, 0.349), (10, 0.421, 0.438)), P((10, 0.048, 0.100), (10, 0.327, 0.409))),
    'Q9(a)(v)': (P((10, 0.031, 0.349), (10, 0.438, 0.504)), P((10, 0.048, 0.100), (10, 0.409, 0.458))),
    'Q9(b)(i)': (P((10, 0.031, 0.074), (10, 0.504, 0.762)), P((10, 0.048, 0.080), (10, 0.458, 0.540))),
    'Q9(b)(ii)': (P((10, 0.031, 0.074), (10, 0.504, 0.741), (10, 0.762, 0.779)), P((10, 0.048, 0.080), (10, 0.458, 0.478), (10, 0.540, 0.622))),
    'Q9(b)(iii)': (P((10, 0.031, 0.074), (10, 0.504, 0.741), (10, 0.779, 0.828)), P((10, 0.048, 0.080), (10, 0.458, 0.478), (10, 0.622, 0.688))),
    'Q9(c)': (P((10, 0.031, 0.074), (10, 0.828, 0.867)), P((10, 0.048, 0.080), (10, 0.688, 0.777))),
    'Q10(a)(i)': (P((11, 0.050, 0.103)), P((11, 0.048, 0.145))),
    'Q10(a)(ii)': (P((11, 0.050, 0.084), (11, 0.103, 0.118)), P((11, 0.048, 0.100), (11, 0.145, 0.227))),
    'Q10(a)(iii)': (P((11, 0.050, 0.084), (11, 0.118, 0.159)), P((11, 0.048, 0.100), (11, 0.227, 0.326))),
    'Q10(b)(i)': (P((11, 0.050, 0.084), (11, 0.159, 0.193)), P((11, 0.048, 0.080), (11, 0.326, 0.424))),
    'Q10(b)(ii)': (P((11, 0.050, 0.084), (11, 0.159, 0.178), (11, 0.193, 0.208)), P((11, 0.048, 0.080), (11, 0.326, 0.346), (11, 0.424, 0.506))),
    'Q10(b)(iii)': (P((11, 0.050, 0.084), (11, 0.159, 0.178), (11, 0.208, 0.223)), P((11, 0.048, 0.080), (11, 0.326, 0.346), (11, 0.506, 0.572))),
    'Q10(b)(iv)': (P((11, 0.050, 0.084), (11, 0.159, 0.178), (11, 0.223, 0.264)), P((11, 0.048, 0.080), (11, 0.326, 0.346), (11, 0.572, 0.670))),
    'Q10(c)': (P((11, 0.050, 0.084), (11, 0.264, 0.358)), P((11, 0.048, 0.080), (11, 0.670, 0.778))),
    'Q11(a)(i)': (P((11, 0.358, 0.430)), P((12, 0.048, 0.247))),  # whole comparison table with its 4 × 4m
    'Q11(a)(ii)': (P((11, 0.358, 0.416), (11, 0.430, 0.445)), P((12, 0.048, 0.247))),  # whole comparison table with its 4 × 4m
    'Q11(a)(iii)': (P((11, 0.358, 0.416), (11, 0.445, 0.461)), P((12, 0.048, 0.247))),  # whole comparison table with its 4 × 4m
    'Q11(a)(iv)': (P((11, 0.358, 0.416), (11, 0.461, 0.486)), P((12, 0.048, 0.247))),  # whole comparison table with its 4 × 4m
    'Q11(b)(i)': (P((11, 0.358, 0.396), (11, 0.486, 0.505)), P((12, 0.048, 0.080), (12, 0.247, 0.346))),
    'Q11(b)(ii)': (P((11, 0.358, 0.396), (11, 0.505, 0.520)), P((12, 0.048, 0.080), (12, 0.247, 0.268), (12, 0.346, 0.428))),
    'Q11(b)(iii)': (P((11, 0.358, 0.396), (11, 0.520, 0.535)), P((12, 0.048, 0.080), (12, 0.247, 0.268), (12, 0.428, 0.477))),
    'Q11(b)(iv)': (P((11, 0.358, 0.396), (11, 0.535, 0.561)), P((12, 0.048, 0.080), (12, 0.247, 0.268), (12, 0.477, 0.625))),
    'Q11(c)(i)': (P((11, 0.358, 0.396), (11, 0.561, 0.580)), P((12, 0.048, 0.080), (12, 0.625, 0.724))),
    'Q11(c)(ii)': (P((11, 0.358, 0.396), (11, 0.580, 0.596)), P((12, 0.048, 0.080), (12, 0.625, 0.646), (12, 0.724, 0.773))),
    'Q11(c)(iii)': (P((11, 0.358, 0.396), (11, 0.596, 0.614)), P((12, 0.048, 0.080), (12, 0.625, 0.646), (12, 0.773, 0.838))),
    'Q11(c)(iv)': (P((11, 0.358, 0.396), (11, 0.614, 0.668)), P((12, 0.048, 0.080), (12, 0.625, 0.646), (12, 0.838, 0.862))),
    'Q12(a)(i)': (P((12, 0.031, 0.104)), P((13, 0.048, 0.145))),
    'Q12(a)(ii)': (P((12, 0.031, 0.085), (12, 0.104, 0.119)), P((13, 0.048, 0.113), (13, 0.145, 0.178))),
    'Q12(a)(iii)': (P((12, 0.031, 0.085), (12, 0.119, 0.177)), P((13, 0.048, 0.113), (13, 0.178, 0.227))),
    'Q12(b)(i)': (P((12, 0.031, 0.085), (12, 0.177, 0.327)), P((13, 0.048, 0.080), (13, 0.227, 0.293))),
    'Q12(b)(ii)': (P((12, 0.031, 0.085), (12, 0.177, 0.297), (12, 0.327, 0.357)), P((13, 0.048, 0.080), (13, 0.227, 0.260), (13, 0.293, 0.326))),
    'Q12(b)(iii)': (P((12, 0.031, 0.085), (12, 0.177, 0.297), (12, 0.357, 0.417)), P((13, 0.048, 0.080), (13, 0.227, 0.260), (13, 0.326, 0.375))),
    'Q12(c)(i)': (P((12, 0.031, 0.085), (12, 0.417, 0.523)), P((13, 0.048, 0.080), (13, 0.375, 0.441))),
    'Q12(c)(ii)': (P((12, 0.031, 0.085), (12, 0.417, 0.492), (12, 0.523, 0.552)), P((13, 0.048, 0.080), (13, 0.375, 0.408), (13, 0.441, 0.473))),
    'Q12(c)(iii)': (P((12, 0.031, 0.085), (12, 0.417, 0.492), (12, 0.552, 0.583)), P((13, 0.048, 0.080), (13, 0.375, 0.408), (13, 0.473, 0.506))),
    'Q12(c)(iv)': (P((12, 0.031, 0.085), (12, 0.417, 0.492), (12, 0.583, 0.643)), P((13, 0.048, 0.080), (13, 0.375, 0.408), (13, 0.506, 0.555))),
    'Q12(d)(i)': (P((12, 0.031, 0.085), (12, 0.643, 0.662)), P((13, 0.048, 0.080), (13, 0.555, 0.654))),
    'Q12(d)(ii)': (P((12, 0.031, 0.085), (12, 0.662, 0.725)), P((13, 0.048, 0.080), (13, 0.555, 0.588), (13, 0.654, 0.726))),
    'Q13(a)(i)': (P((13, 0.031, 0.114)), P((14, 0.048, 0.129))),
    'Q13(a)(ii)': (P((13, 0.031, 0.094), (13, 0.114, 0.129)), P((14, 0.048, 0.100), (14, 0.129, 0.391))),
    'Q13(a)(iii)': (P((13, 0.031, 0.094), (13, 0.129, 0.144)), P((14, 0.048, 0.100), (14, 0.391, 0.473))),
    'Q13(a)(iv)': (P((13, 0.031, 0.094), (13, 0.144, 0.185)), P((14, 0.048, 0.100), (14, 0.473, 0.606))),
    'Q13(b)(i)': (P((13, 0.031, 0.094), (13, 0.185, 0.204)), P((14, 0.048, 0.080), (14, 0.606, 0.656))),
    'Q13(b)(ii)': (P((13, 0.031, 0.094), (13, 0.204, 0.219)), P((14, 0.048, 0.080), (14, 0.656, 0.803))),
    'Q13(b)(iii)': (P((13, 0.031, 0.094), (13, 0.219, 0.234)), P((14, 0.048, 0.080), (14, 0.803, 0.869))),
    'Q13(b)(iv)': (P((13, 0.031, 0.094), (13, 0.234, 0.275)), P((14, 0.048, 0.080), (14, 0.869, 0.925))),
    'Q13(c)(i)': (P((13, 0.031, 0.094), (13, 0.275, 0.294)), P((14, 0.048, 0.080), (15, 0.047, 0.162))),
    'Q13(c)(ii)': (P((13, 0.031, 0.094), (13, 0.294, 0.309)), P((14, 0.048, 0.080), (15, 0.047, 0.067), (15, 0.162, 0.211))),
    'Q13(c)(iii)': (P((13, 0.031, 0.094), (13, 0.309, 0.339)), P((14, 0.048, 0.080), (15, 0.047, 0.067), (15, 0.211, 0.277))),
    'Q13(c)(iv)': (P((13, 0.031, 0.094), (13, 0.339, 0.379)), P((14, 0.048, 0.080), (15, 0.047, 0.067), (15, 0.277, 0.375))),
    'Q13(d)(i)': (P((13, 0.031, 0.094), (13, 0.379, 0.458)), P((14, 0.048, 0.080), (15, 0.375, 0.442))),
    'Q13(d)(ii)': (P((13, 0.031, 0.094), (13, 0.379, 0.438), (13, 0.458, 0.472)), P((14, 0.048, 0.080), (15, 0.375, 0.396), (15, 0.442, 0.490))),
    'Q13(d)(iii)': (P((13, 0.031, 0.094), (13, 0.379, 0.438), (13, 0.472, 0.509)), P((14, 0.048, 0.080), (15, 0.375, 0.396), (15, 0.490, 0.927), (16, 0.063, 0.454))),
}
SHARED = 'Shared scale {}: the first correct answers earn the higher award, whichever part they answer, so no part carries a mark of its own.'
FIGURES = {
    'q1': ('agsci-2016-ol-paper-soil-flasks', [('A', 'Flask A: fresh soil in muslin bag, above limewater', False), ('B', 'Flask B: sterile soil in muslin bag, above limewater', False)]),
    'q4': ('agsci-2016-ol-paper-lab-equipment', [('A', 'Inoculating loop', True), ('B', 'Pooter', True), ('C', 'Refractometer', True), ('D', 'Soil sieves', True), ('E', 'Potometer', True)]),
    'q5': ('agsci-2016-ol-paper-flower-strawberry', [('A', 'Petal', True), ('B', 'Anther (the scheme accepts stamen)', True), ('C', 'Carpel (the scheme accepts ovary)', True),
                                                    ('D', 'The part whose function is to protect the (flower) bud or young flower', True), ('X', 'Stolon or runner or (horizontal) stem', True)]),
    'q6': ('agsci-2016-ol-paper-invertebrates', [('A', '(Liver)fluke', True), ('B', 'Cranefly or daddy long-legs', True), ('C', '(Sheep) tick', True)]),
    'q7': ('agsci-2016-ol-paper-barley-tramlines', None),
    'q9ai': ('agsci-2016-ol-paper-respiratory-system', [('A', 'Trachea or windpipe', True), ('B', 'Bronchus', True), ('C', 'Diaphragm', True)]),
    'q9aii': ('agsci-2016-ol-paper-respiratory-system', None),
    'q9bi': ('agsci-2016-ol-paper-urinary-system', None),
    'q9bii': ('agsci-2016-ol-paper-urinary-system', [('X', 'Ureter', True), ('Y', 'Bladder', True), ('Z', 'Urethra', True)]),
    'q9biii': ('agsci-2016-ol-paper-urinary-system', None),
}


def split(text, note=None, route=None, kind='point'):
    """An unpriced row: the scheme prices the scale (orderedSplit) or the question total, not the row."""
    row = point(text, None, note, kind)
    if route:
        row['route'] = route
    return row


def figured(card, key):
    figure, labels = FIGURES[key]
    card['figureKey'] = figure
    if labels:
        card['labelKey'] = [dict(letter=l, meaning=m, askedInThisQuestion=a) for l, m, a in labels]
    return card


def build():
    p = Paper(2016, 'ordinary', FILE, HASHES, REGIONS, ATLAS, 16, 20, SELECTIONS, SUPPLEMENTARY,
              section=lambda ref: 'A' if int(ref.split('(')[0].split(' ')[0][1:]) <= 7 else 'B')
    add = p.add
    # Section One ------------------------------------------------------------
    figured(add('q1', 'Q1', '2-2-3', 'rocks-and-soil-microbes',
                '(a) Name two sedimentary rocks and two metamorphic rocks from the following list: Basalt, marble, sandstone, granite, quartzite, limestone. (i) Two sedimentary rocks. (ii) Two metamorphic rocks. '
                '(b) An investigation on soil was carried out. Two flasks were set up as shown in the diagram. The flasks were left at room temperature for two days. At the end of the two days the limewater in one flask had turned white in colour. '
                '(i) In which flask did the limewater change colour? (ii) Explain why the limewater changed colour. (iii) How was the soil in flask B sterilised? (iv) One of the flasks was used as a control. What is meant by this?',
                [menu(['1. Sandstone', '2. Limestone'], [2, 2], '(a)(i) Two sedimentary rocks: 2 × 2m.'),
                 menu(['1. Marble', '2. Quartzite'], [2, 2], '(a)(ii) Two metamorphic rocks: 2 × 2m.'),
                 point('(b)(i) Limewater changed colour in — Flask A', 2),
                 menu(['Microorganisms or living organisms in A', 'release CO2', 'during respiration'], [4, 2], '(b)(ii) Why the limewater changed colour: any two, 4m + 2m.'),
                 point('(b)(iii) How flask B soil was sterilised — Heating the soil strongly or burning the soil or disinfectant', 2),
                 point('(b)(iv) Control — To compare (with flask A) or comparison described', 2)],
                node='1-0|1-4|0-1'), 'q1')
    statements = [('a', 'Grass tetany in dairy cows is caused by a lack of calcium.', 'F'), ('b', 'Clover increases the protein content of a sward.', 'T'),
                  ('c', 'Scots Pine is a broadleaved tree.', 'F'), ('d', 'Tillering is the development of side shoots in a grass plant.', 'T'),
                  ('e', 'The length of gestation in pigs is approximately 115 days.', 'T'), ('f', 'Iodine solution is used to test for the presence of glucose in food.', 'F'),
                  ('g', 'The omasum is found in a pig’s digestive system.', 'F'), ('h', 'Sheep do not have incisor teeth.', 'F'),
                  ('i', 'Chickens have a gizzard in their digestive system.', 'T'), ('j', 'A sub-soiler is used to improve drainage in soil.', 'T')]
    add('q2', 'Q2', '4-1', 'true-or-false-farm-science',
        'Indicate whether the following statements are true (T) or false (F) by placing a circle around the correct answer in each case, as shown in the example. '
        'Example: Applying ground limestone to grassland lowers the soil pH — F. ' + ' '.join(f'({k}) {s}' for k, s, _ in statements),
        [menu([f'({k}) {a}' for k, _, a in statements], [2] * 10,
              'All ten statements, 2 marks each (10 × 2m). T = true, F = false; the scheme gives each letter with T or F.')],
        tariff={'kind': 'fixed', 'notation': '10 × 2m'}, node='3-0|3-5|2-6|1-5')
    add('q3', 'Q3', '2-3', 'reasons-for-farm-practices',
        'Give one scientific reason in each case why the following practices are carried out on Irish farms. (a) Choosing Holstein-Friesian cows for a dairy farm. '
        '(b) Carrying out a soil test before sowing a crop. (c) Growing a catch crop on a farm. (d) Spreading slurry at certain times of the year only. (e) Practising crop rotation.',
        [point('(a) Holstein-Friesian cows — High milk yields or good quality milk or high % protein or highly efficient at converting grass to milk or produce good replacement heifers', 4,
               'One reason for each practice, 4 marks each (5 × 4m).'),
         point('(b) Soil test before sowing — To determine soil pH or to determine nutrient status of soil or to test soil for nutrient deficiency or to determine amount of fertiliser(s) to apply to crop or to determine fertility of soil or response to fertiliser', 4),
         point('(c) Catch crop — Fast growing or high yielding or additional winter feed or less risk of fodder shortage or fewer meals required or reduces cost of winter feed or early bite for cows or prevents leaching', 4),
         point('(d) Slurry at certain times only — Avoids pollution or less risk of run-off or prevents soil compaction or prevents damage to soil structure or legislation or optimises use by crop or gives time for soil (or crop) to absorb it or avoids contamination (of silage) or weather too wet', 4),
         point('(e) Crop rotation — Pest control or disease control or weed control or more balanced uptake of nutrients or improves soil structure or improves soil fertility or prevents plough pan or adds organic matter or improves yield or prevents nutrient depletion', 4)],
        tariff={'kind': 'fixed', 'notation': '5 × 4m'}, node='3-1|1-2|2-4|1-6')
    equipment = [('Soil sieves', 'D', 'To determine soil texture or to separate soil (particles) or to determine % of soil particles (or named soil particle(s) )'),
                 ('Potometer', 'E', 'To measure (the rate of) transpiration or to measure (the rate of) water uptake'),
                 ('Inoculating loop', 'A', 'To transfer soil (or milk or microorganisms) to agar plate or to streak the agar plate'),
                 ('Refractometer', 'C', 'To determine % sucrose content in sugar beet or grass'),
                 ('Pooter', 'B', 'To collect insects (or small animals) or to suck up insects')]
    rows = [menu([f'{name}: {letter}' for name, letter, _ in equipment], [2] * 5, '5 × (2m + 2m): the letter 2 for each piece of equipment.'),
            menu([f'{name} {letter}: {use}' for name, letter, use in equipment], [2] * 5, 'The main use 2 for each piece of equipment.')]
    figured(add('q4', 'Q4', '1-2', 'laboratory-equipment-uses',
                'The following images show equipment used when conducting experiments in Agricultural Science. In the table, match the letter on the image with the name of the equipment and state the main use of each piece of equipment: '
                'Soil sieves; Potometer; Inoculating loop; Refractometer; Pooter.', rows,
                tariff={'kind': 'fixed', 'notation': '5 × (2m + 2m)'}, node='0-1'), 'q4')
    figured(add('q5', 'Q5', '3-1', 'flower-and-strawberry-reproduction',
                '(a) The diagram shows a flower. (i) Name the parts A, B and C. (ii) What is the function of part D? (b) The picture shows a strawberry plant. (i) Part X is called a ___. '
                '(ii) The strawberry plant is shown reproducing without seeds. What is this type of reproduction called? (iii) Plants produced by this method are genetically identical. '
                'What name is given to a group of genetically identical plants? (iv) Name the method of reproduction in flowering plants in which seeds are formed.',
                [split('(a)(i) A — Petal', SHARED.format('(4 × 3m) + (4 × 2m)') + ' Eight answers: A, B, C, the function of D, X and (b)(ii)-(iv).'),
                 split('(a)(i) B — Anther [accept ‘stamen’]'), split('(a)(i) C — Carpel [accept ‘ovary’]'),
                 split('(a)(ii) Function of part D — To protect the (flower) bud or young flower'),
                 split('(b)(i) Part X — stolon or runner or (horizontal) stem'),
                 split('(b)(ii) Reproduction without seeds — Asexual (reproduction) or vegetative (reproduction)'),
                 split('(b)(iii) A group of genetically identical plants — A clone'),
                 split('(b)(iv) Reproduction in which seeds are formed — Sexual (reproduction)')],
                marks=20, tariff={'kind': 'orderedSplit', 'notation': '(4 × 3m) + (4 × 2m)'}, node='2-0|2-1'), 'q5')
    figured(add('q6', 'Q6', '4-3-3', 'invertebrates-of-agricultural-importance',
                '(a) The invertebrates pictured are of agricultural importance. Name each of them. (i) Invertebrate A is ___ (ii) Invertebrate B is ___ (iii) Invertebrate C is ___ '
                '(b) State the agricultural importance of each invertebrate. (i) The agricultural importance of A is ___ (ii) The agricultural importance of B is ___ '
                '(iii) The agricultural importance of C is ___ (iv) Which of the above invertebrates has a larva called a miracidium?',
                [split('(a)(i) Invertebrate A — (Liver)fluke', SHARED.format('(6 x 3m) + 2m') + ' Seven answers: the three names, the three importances and (b)(iv).'),
                 split('(a)(ii) Invertebrate B — Cranefly or daddy long-legs'), split('(a)(iii) Invertebrate C — (Sheep) tick'),
                 split('(b)(i) Importance of A — (Endo) parasite of sheep and-or cattle or causes weight loss (or lack of thrive) or causes diarrhoea or causes anaemia or causes lump under lower jaw or damages liver or reduces milk yield or causes death (in acute cases) or causes harm to animal',
                       'The scheme strikes out the brackets around "of sheep and-or cattle".'),
                 split('(b)(ii) Importance of B — Larva (or leatherjacket) attacks crop(s) or larva is pest of crops or larva attacks (or damages) crops or adult lays eggs which hatch into leatherjacket or larva attacks roots and-or stems of plants'),
                 split('(b)(iii) Importance of C — Host of Babesia or transfers Babesia to cattle or sucks blood or Babesia multiply inside sheep tick or irritates skin or bites into skin or is a parasite of sheep or harms animal'),
                 split('(b)(iv) Larva called a miracidium — (Liver)fluke or A')],
                marks=20, tariff={'kind': 'orderedSplit', 'notation': '(6 x 3m) + 2m'}, node='3-5|2-4'), 'q6')
    figured(add('q7', 'Q7', '3-3-3', 'barley-uses-and-practices',
                'Barley is a cereal crop commonly grown in Ireland. (a) Give two uses for barley. (b) State two features of a barley crop when it is ready for harvesting. '
                '(c) State a reason for each of the following practices when growing barley. (i) Providing “tramlines”. (ii) Using a combine drill. (iii) Rolling. (iv) Harvesting when weather is dry.',
                [split('(a) Uses for barley — Animal feed or meal or concentrate/ malting or alcohol/ (straw for) bedding/ straw for feeding/ human food',
                       SHARED.format('(4 × 3m) + (4 × 2m)') + ' Eight answers: two uses, two features and a reason for each of the four practices. Any two uses.'),
                 split('(b) Features when ready for harvesting — Grain or seed becomes hard/ seed becomes dry/ ear or seed-head and-or straw turns golden or yellow colour/ seed-head bends over (and lies parallel to stem)/ flag leaf withers', 'Any two.'),
                 split('(c)(i) Providing “tramlines” — Prevents damage to crop when driving through it or allows farmer to apply fertilisers or herbicides or pesticides or weedkillers or allows farmer to spray crop or allows more efficient use of fertiliser'),
                 split('(c)(ii) Using a combine drill — To sow the seed and fertiliser together or allows placement of fertiliser or more efficient use of fertiliser or reduces labour costs or reduces fuel costs/ gets job done faster'),
                 split('(c)(iii) Rolling — Levels the soil or ensures even seed-bed or breaks up (lumps of) soil or buries seed or prevents seed being blown away or ensures better seed-soil contact or brings up moisture or buries stones or compacts the soil'),
                 split('(c)(iv) Harvesting when weather is dry — Grain is drier or reduces damage to crop or reduces soil compaction or reduces moisture content at harvest or easier to harvest or prevents “clogging” of machine or less spoilage in storage or less acid required prior to storage or reduces need for drying prior to storage or straw will be drier or easier to bale straw')],
                marks=20, tariff={'kind': 'orderedSplit', 'notation': '(4 × 3m) + (4 × 2m)'}, node='2-3|2-5'), 'q7')
    # Question 8 -------------------------------------------------------------
    species = '(i) Name one grass and one other plant species suitable for best quality grazing for livestock.'
    add('q8ai', 'Q8(a)(i)', '3-3-1', 'grazing-sward-species', 'Name one grass and one other plant species suitable for best quality grazing for livestock.',
        [point('Grass: Perennial ryegrass (or PRG) or Italian ryegrass (or IRG)', 3, '[Accept ‘ryegrass’]'), point('Other plant species: e.g. Clover', 3)], node='2-6')
    add('q8aii', 'Q8(a)(ii)', '3-3-1', 'grazing-sward-species-reasons', 'Give a reason for the use of each of the named species.',
        [menu(['Perennial ryegrass: High productivity or high yield or highly digestible or high % DMD or palatable or “sweet” or persistent or high tillering capacity or long growing season or recovers well after grazing or aggressive or good ground cover or dominates pasture or reduces weeds or supports high stocking rates or promotes higher weight gains or higher milk yields',
               'Italian ryegrass: High productivity or high yield or highly digestible or high % DMD or palatable or “sweet” or long growing season or recovers well after grazing or supports high stocking rates or early bite for cows or promotes higher weight gains or higher milk yields'],
              [3], '[Any one reason for the use of either of the two grasses] 3m.'),
         point('e.g. Clover: Nitrogen fixation or improves fertility of soil or rich in protein or rich in minerals or rich in iron or palatable or ground cover or weed control or provides grazing during mid-summer (“slump” in grass growth)', 3,
               '[Any one reason for the use of the other species] 3m.')], species, node='2-6')
    methods = [('direct-sowing', 'Direct sowing', 'Plough|harrow or cultivate soil|roll soil before sowing|apply fertiliser|by broadcasting|sow grass seed|apply fertiliser and seed together|using combine drill|roll soil after sowing (to bury seeds)|Autumn sown or September|Spring sown or April-May'),
               ('undersowing', 'Undersowing', 'Common in tillage farming|nurse or companion crop|companion crop named e.g. barley|short- strawed varieties|Spring time or March – April|plough|harrow or cultivate soil|roll soil before sowing|apply fertiliser|sow nurse crop|sow grass seed|roll soil after sowing (to bury seeds)|harvest nurse crop in August-September or arable silage'),
               ('direct-drilling', 'Direct drilling (or direct seeding)', 'Land not ploughed|old grassland grazed bare|herbicide applied|to kill weeds and remaining grass|slits created|grass seed and fertiliser applied into slits|slug pellets applied into slits|new grass seedlings emerge|suitable method of re-seeding in shallow soils'),
               ('stitching-in', 'Stitching-in', 'Land not ploughed|old grassland grazed bare|no herbicide applied|old grassland remains|slits created|grass seed and fertiliser applied into slits|slug pellets applied into slits|new grass seedlings emerge|suitable method of re-seeding in shallow or poached soils')]
    rows, variants = routes([(slug, label, [point(f'Named method — {label}', 2, 'Named method 2m, then any four points from one of the methods (4 × 3m).'),
                                            menu(steps, [3] * 4, f'{label}: any four points, 3 marks each.')]) for slug, label, steps in methods])
    add('q8aiii', 'Q8(a)(iii)', '3-3-1', 'pasture-sowing-method', 'Describe one method of sowing a field for pasture.', rows,
        selection=closed(1, [label for _, label, _ in methods]), node='2-6', extra={'answerVariants': variants})
    bales = 'Some farmers make bales of silage rather than pit silage.'
    add('q8bi', 'Q8(b)(i)', '3-3-3', 'baled-silage-advantages', 'State two advantages of baled silage.',
        [menu('Easier to make in small fields|no need for pit or lower capital costs|easier to transport|easier to buy or sell|less effluent|lower pollution risk|less spoilage or can be kept longer|better quality|lower dry matter losses in storage|easy to store|less weather dependent',
              [3, 3], 'Any two, 3 marks each (2 × 3m).')], bales, node='2-6')
    add('q8bii', 'Q8(b)(ii)', '3-3-3', 'baled-silage-disadvantages', 'State two disadvantages of baled silage.',
        [menu('More expensive to make|not suitable for very wet silage|more labour involved at feeding time|more time consuming at feeding time|bales can be damaged|disposal of plastic|heavy to handle|special equipment needed to lift bales',
              [3, 3], 'Any two, 3 marks each (2 × 3m).')], bales, node='2-6')
    add('q8c', 'Q8(c)', '3-3-3', 'pit-silage-quality-tests', 'Describe any two tests that a farmer can undertake to assess the quality of pit silage.',
        [menu(['Examine the colour of the silage/ if yellow colour/ good quality silage or lactic acid preservation/ if brown or dark colour/ poor quality silage or butyric acid production/ repeat (to get representative sample)',
               'Examine the smell of the silage/ if sharp or vinegar smell/ good quality silage/ if rancid or “rotten” smell/ poor quality silage/ repeat (to get representative sample)',
               'Squeeze the silage between hands/ if juice runs freely/ low % dry matter content (DM) or 15% D.M. or low quality silage/ if juice drips out/ average D.M. content or 20% D.M. or average quality silage/ if no (or barely any) juice runs out/ high D.M. content or 25% D.M. or good quality silage/ repeat',
               'Squeeze the silage between hands/ collect juice/ test with universal indicator/ determine pH using colour chart/ if pH < 5/ good quality silage/ if pH > 5/ poor quality silage/ repeat'],
              [11, 11], 'Any two tests: 2[(3 × 3m) + 2m]. [Any four points each from two of the following tests]: in each test the first three correct points earn 3 each and the fourth 2.')],
        node='2-6|0-1')
    # Question 9 -------------------------------------------------------------
    lungs = 'The diagram shows the respiratory system of a farm animal.'
    figured(add('q9ai', 'Q9(a)(i)', '4-1', 'respiratory-system-parts', 'Name the parts A, B and C.',
                [point('A = Trachea or windpipe', 3, '3 × 3m. [Accept ring(s) of cartilage once for either A or B]'), point('B = Bronchus', 3), point('C = Diaphragm', 3)], lungs, node='3-0'), 'q9ai')
    figured(add('q9aii', 'Q9(a)(ii)', '4-1', 'respiratory-part-d-function', 'State the function of part D.', [point('Gaseous exchange or described', 3)], lungs, node='3-0'), 'q9aii')
    add('q9aiii', 'Q9(a)(iii)', '4-3-3', 'preventing-viral-pneumonia',
        'Viral pneumonia is a common illness which can occur during calf housing. How can viral pneumonia be prevented?',
        [menu('Good ventilation|no draughts|dry housing|adequate space per animal or avoid over-crowding|colostrum|vaccination|adequate cubic capacity or air space or high roof|reduce stress|isolation or quarantine or biosecurity',
              [6, 3], 'Any two: 6m + 3m, the first correct earns 6 and the second 3.')], node='3-5')
    add('q9aiv', 'Q9(a)(iv)', '4-3-3', 'lungworm-life-cycle', 'Describe briefly the life cycle of lungworms.',
        [menu('Adult (female) worm|lays eggs|inside lungs|eggs coughed up into mouth|eggs swallowed|enter intestine|exit animal in faeces|eggs on pasture|hatch|larvae|larvae eaten by animal|enter stomach|enter bloodstream|carried to lungs|larvae mature',
              [4] * 3, 'Any three, 4 marks each (3 × 4m).')], node='3-5')
    add('q9av', 'Q9(a)(v)', '4-3-3', 'lungworm-control', 'Outline one method of control of lungworms in cattle.',
        [point('Vaccination or dosing or leader-follower system or isolate or quarantine (infected animal)', 3)], node='3-5')
    kidneys = 'The diagram shows the urinary system of a farm animal.'
    figured(add('q9bi', 'Q9(b)(i)', '4-1', 'kidney-function', 'State a function of the kidneys.',
                [point('Excretion/ getting rid of wastes/ osmoregulation/ control of water balance or salt balance in body or filters blood', 3)], kidneys, node='3-0'), 'q9bi')
    figured(add('q9bii', 'Q9(b)(ii)', '4-1', 'urinary-system-parts', 'Name the parts X, Y and Z.',
                [point('X = Ureter', 3, '3 × 3m.'), point('Y = Bladder', 3), point('Z = Urethra', 3)], kidneys, node='3-0'), 'q9bii')
    figured(add('q9biii', 'Q9(b)(iii)', '4-1', 'bladder-contents', 'What is stored in part Y?', [point('Urine or salt or urea or water', 3)], kidneys, node='3-0'), 'q9biii')
    add('q9c', 'Q9(c)', '4-3-3', 'redwater-fever-spread', 'Redwater fever is a disease of cattle. Briefly outline how redwater fever can spread in a cattle herd.',
        [menu('Rough grazing or long grass|(sheep) tick|sucks blood|from infected cow|blood contains Babesia|Babesia form gametes|form zygotes|spores formed|asexual reproduction|tick bites another (healthy) cow|spores enter healthy cow|enter red blood cells|lack of preventive measure|vet not called|infected animal not isolated',
              [3] * 3, 'Any three, 3 marks each (3 × 3m).')], node='3-5')
    # Question 10 ------------------------------------------------------------
    add('q10ai', 'Q10(a)(i)', '3-3-2', 'blight-yield-loss', 'Explain how potato blight reduces the yield of maincrop potatoes.',
        [point('Damages leaves or damage described or less photosynthesis or tubers rot', 3)], node='2-4')
    add('q10aii', 'Q10(a)(ii)', '3-3-2', 'blight-symptoms', 'Describe two symptoms of potato blight.',
        [menu('Black or brown spots on leaves and-or stems|white mouldy growth on underside of leaves|tubers go black|tubers rot', [3, 3], 'Any two, 3 marks each (2 × 3m).')], node='2-4')
    add('q10aiii', 'Q10(a)(iii)', '3-3-2', 'blight-prevention', 'Outline two methods of preventing potato blight.',
        [menu('Certified seed|resistant varieties|rotation|avoid groundkeepers|isolate potato dumps or bury last years potatoes|earthing up|heed blight warnings|remove infected plant(s) immediately|spray|fungicide|repeat spray|dessicant',
              [3, 3], 'Any two, 3 marks each (2 × 3m).')], node='2-4')
    potatoes = 'Describe the cultivation of potatoes under the following headings:'
    for key, ref, topic, concept, heading, options, steps, note, node in [
            ('q10bi', 'Q10(b)(i)', '3-3-1', 'potato-soil-suitability', 'Soil suitability',
             '(Medium) loam or good texture|deep soil|fertile|good drainage|good aeration|good structure|free from stones|pH = 5.0 – 6.5|brown earth or grey-brown podzolic', [6, 3],
             'Any two: 6m + 3m, the first correct earns 6 and the second 3.', '2-3'),
            ('q10bii', 'Q10(b)(ii)', '3-3-1', 'potato-sowing-method', 'Method of sowing',
             'Potato planter|seed planted in ridges or drills|planted 10 – 15cm below soil|planted 25-35 apart in the ridge|in bag or suitable container|dig with spade', [6], 'Any one, 6m.', '2-3'),
            ('q10biii', 'Q10(b)(iii)', '3-3-2', 'potato-weed-control', 'Weed control',
             'Spray|herbicide|earthing up|mechanical or explained e.g. hoeing|hand pulling|burning|shading action|rotation', [3, 3], 'Any two, 3 marks each (2 × 3m).', '2-4'),
            ('q10biv', 'Q10(b)(iv)', '3-3-3', 'potato-harvesting', 'Harvesting',
             'Elevator digger|collected by hand|complete harvester|haulms or tops cut at harvesting|June -July (earlies)|August – December (maincrop)|yield of 7-10 tonnes/ha (earlies)|yield of 30 – 40 tonnes/ha (maincrop)|avoid tuber damage|avoid wet or frosty harvesting',
             [3, 3], 'Any two, 3 marks each (2 × 3m).', '2-5')]:
        add(key, ref, topic, concept, f'Describe the cultivation of potatoes under the heading: {heading}.', [menu(options, steps, note)], potatoes, node=node)
    add('q10c', 'Q10(c)', '3-3-3', 'potato-water-percentage', 'Describe an experiment to find the percentage (%) water in a sample of potatoes.',
        [menu('Wash (soil from) potatoes|dry potatoes|weigh empty beaker or suitable container|cut potatoes|equally sized cubes|place in beaker|re-weigh|find mass of potatoes by subtraction|place in oven|100º C|15 minutes|re-weigh|constant mass|calculate loss in mass|this equals mass of water|calculate % water content using (mass of water ÷ mass of fresh potatoes) × 100/1',
              [3] * 6, 'Any six, 3 marks each (6 × 3m). [Award maximum of 15m if no attempt at calculation] [Some, or all, of marks in method may be obtained from labelled diagram]')],
        node='2-5|0-1')
    # Question 11 ------------------------------------------------------------
    compare = 'Compare sandy soils and clay soils under the following headings:'
    for key, ref, concept, num, heading, sandy, clay in [
            ('q11ai', 'Q11(a)(i)', 'sandy-clay-drainage', 'i', 'Drainage', 'Well drained', 'Poorly drained'),
            ('q11aii', 'Q11(a)(ii)', 'sandy-clay-fertility', 'ii', 'Fertility', 'Low fertility', 'High fertility'),
            ('q11aiii', 'Q11(a)(iii)', 'sandy-clay-organic-matter', 'iii', 'Organic matter content', 'Low', 'High'),
            ('q11aiv', 'Q11(a)(iv)', 'sandy-clay-temperature', 'iv', 'Soil temperature', 'High', 'Low')]:
        add(key, ref, '2-2-2', concept, f'Compare sandy soils and clay soils under the heading: {heading}.',
            [point(f'({num}) {heading} — {sandy} or {clay}', 4,
                   '4 × 4m, one per heading. The scheme\'s table gives the sandy soil, then "or", then the clay soil: either answer earns the 4 marks.')], compare, node='1-3')
    add('q11bi', 'Q11(b)(i)', '2-2-3', 'increasing-earthworms', 'Outline two ways by which the number of earthworms in grassland could be increased.',
        [menu('Add organic matter or named example or increase soil fertility|drain soil|add lime|aerate soil', [3, 3], 'Any two, 3 marks each (2 × 3m).')], node='1-4')
    add('q11bii', 'Q11(b)(ii)', '2-2-3', 'earthworm-benefits', 'Explain how earthworms are beneficial in grassland.',
        [menu('Create channels or holes|improve drainage|improve aeration|mix soil|create humus|decompose organic matter|improve soil texture|improve soil structure|improve soil fertility', [3, 3],
              'Any two, 3 marks each (2 × 3m).')], node='1-4')
    add('q11biii', 'Q11(b)(iii)', '2-2-3', 'earthworm-phylum', 'Name the phylum to which earthworms belong.', [point('Annelida', 3)], node='1-4|3-1')
    add('q11biv', 'Q11(b)(iv)', '2-2-3', 'earthworm-diagram', 'Draw a diagram of an earthworm and label three parts.',
        [point('Cylindrical shape and segmented body', None,
               'Diagram: 5m, 3m, 0m. [For 5 marks: cylindrical shape and segmented body; if 1 missing, award 3m; if 2 missing, award 0m]', kind='criterion'),
         point('Mouth/ segment(s)/ anus/ clitellum or saddle/ setae or bristles/ cylindrical (shape)', None, 'Labels: any three, 2 marks each (3 × 2m).')],
        marks=11, tariff={'kind': 'questionTotal', 'notation': '(5m, 3m, 0m) + 3 × 2m'}, node='1-4|3-1')
    add('q11ci', 'Q11(c)(i)', '2-2-1', 'why-plants-need-nitrogen', 'Why is nitrogen needed in plants?',
        [point('Green colour or chlorophyll formation or protein formation or nucleic acid formation or increases crop growth or increases yield or leafy growth', 3)], node='1-6|2-0')
    add('q11cii', 'Q11(c)(ii)', '2-2-1', 'nitrogen-fertilisers', 'Name two artificial fertilisers which contain nitrogen.',
        [menu('Urea|C.A.N.|ammonium sulphate|10:10:20|5:5:10|7:6:17|18:6:12', [3, 3], 'Any two, 3 marks each (2 × 3m).')], node='1-6')
    add('q11ciii', 'Q11(c)(iii)', '2-2-1', 'nitrogen-leaching-harm', 'Give two reasons why leaching of nitrogen from soil is undesirable.',
        [menu('Pollution|eutrophication|algal bloom|fish kills|loss of nitrogen from crop|reduced crop yield|reduced crop growth or stunted growth|chlorosis or deficiency symptom described', [3, 3],
              'Any two, 3 marks each (2 × 3m).')], node='1-6')
    add('q11civ', 'Q11(c)(iv)', '2-2-1', 'clover-in-nitrogen-cycle', 'What role does clover play in the nitrogen cycle?', [point('Nitrogen fixation or explained', 3)], node='1-6|2-6')
    # Question 12 ------------------------------------------------------------
    add('q12ai', 'Q12(a)(i)', '4-1', 'chromosome-location', 'Where in a cell are chromosomes found?', [point('Nucleus', 4)], node='3-6')
    add('q12aii', 'Q12(a)(ii)', '4-1', 'chromosome-function', 'State a function of chromosomes.', [point('Carry genes or ‘in heredity’', 4)], node='3-6')
    add('q12aiii', 'Q12(a)(iii)', '4-1', 'sheep-gamete-chromosomes', 'There are 54 chromosomes in a body cell of a sheep. How many chromosomes are there in a gamete of a sheep?', [point('27', 4)], node='3-6')
    polled = ('In Aberdeen Angus cattle, the allele for the polled (hornless) condition (P) is dominant to the allele for having horns (p). A pure breeding polled bull and a cow with horns are crossed. '
              'What will be the genotype and phenotype of their calf? Copy the following into your answer book and complete the spaces (genotype in brackets, phenotype on line). Genotypes of parents (PP) × (pp).')
    add('q12bi', 'Q12(b)(i)', '4-1', 'polled-cross-gametes', 'Complete: (i) Gametes ( ) × ( )', [point('Gametes — (P)', 4, '2 × 4m.'), point('Gametes — (p)', 4)], polled, node='3-6')
    add('q12bii', 'Q12(b)(ii)', '4-1', 'polled-cross-calf-genotype', 'Complete: (ii) Genotype of calf ( )', [point('Genotype of calf — (Pp)', 4)], polled, node='3-6')
    add('q12biii', 'Q12(b)(iii)', '4-1', 'polled-cross-calf-phenotype', 'Complete: (iii) Phenotype of calf ___', [point('Phenotype of calf — Polled (or hornless)', 4)], polled, node='3-6')
    heifer = ('In Aberdeen Angus cattle, the allele for the polled (hornless) condition (P) is dominant to the allele for having horns (p). In part (b) a pure breeding polled bull and a cow with horns are crossed. '
              'A heifer resulting from the cross in part (b) is crossed with a bull that is heterozygous for horns. What are the possible genotypes and phenotypes of their calves? '
              'Copy the following into your answer book and complete the spaces (genotypes in brackets, phenotypes on lines).')
    add('q12ci', 'Q12(c)(i)', '4-1', 'heifer-cross-parent-genotypes', 'Complete: (i) Genotypes of parents ( ) × ( )',
        [point('Genotypes of parents — (Pp)', 2, '2 × 2m: one for each parent.'), point('Genotypes of parents — × (Pp)', 2)], heifer, node='3-6')
    add('q12cii', 'Q12(c)(ii)', '4-1', 'heifer-cross-gametes', 'Complete: (ii) Possible gametes ( ) ( ) × ( ) ( )',
        [point('Possible gametes — (P)', 2, '4 × 2m: two gametes from each parent.'), point('Possible gametes — (p)', 2),
         point('Possible gametes — × (P)', 2), point('Possible gametes — × (p)', 2)], heifer, node='3-6')
    add('q12ciii', 'Q12(c)(iii)', '4-1', 'heifer-cross-calf-genotypes', 'Complete: (iii) Possible genotypes of calves ( ) ( ) ( )',
        [point('(PP)', 2, '3 × 2m. The scheme heads this line "Possible gametes of calves"; the paper asks for the possible genotypes.'), point('(Pp)', 2), point('(pp)', 2)], heifer, node='3-6')
    add('q12civ', 'Q12(c)(iv)', '4-1', 'heifer-cross-calf-phenotypes', 'Complete: (iv) Possible phenotypes of calves ___ ___',
        [point('Polled', 2, '2 × 2m.'), point('Horned', 2)], heifer, node='3-6')
    add('q12di', 'Q12(d)(i)', '4-3-1', 'cross-breeding', 'What is cross-breeding?', [point('Crossing two different breeds of the same species', 4)], node='3-6|3-3')
    add('q12dii', 'Q12(d)(ii)', '4-3-1', 'sheep-cross-breeding-advantages', 'State, using examples, the advantages of cross-breeding in sheep production.',
        [menu('Ewes are better mothers|ewes are more prolific|lambs have faster growth rates|ewes have more milk|increased hardiness|hybrid vigour', [4, 2],
              'Any two: 4m + 2m, the first correct earns 4 and the second 2.')], node='3-6|3-3')
    # Question 13 ------------------------------------------------------------
    two = 'Answer any two of (a), (b), (c), (d).'
    breeds = two + ' (i) Name two of the most common lowland breeds of sheep farmed in Ireland.'
    add('q13ai', 'Q13(a)(i)', '4-2', 'lowland-sheep-breeds', 'Name two of the most common lowland breeds of sheep farmed in Ireland.',
        [menu('Suffolk|Texel|Border Leicester|Bluefaced Leicester|Galway', [3, 3], 'Any two, 3 marks each (2 × 3m).')], two, node='3-1')
    traits = [('suffolk', 'Suffolk', 'Terminal sire|excellent conformation or one conformation point described|short|good carcase quality|fast growth rates|shortwool|dark wool|black head|polled|early lamb production or Easter market'),
              ('texel', 'Texel', 'Terminal sire|excellent conformation|good carcase quality|shortwool|white wool|white face|mid -season lamb production|wide face|no wool on head'),
              ('border-leicester', 'Border Leicester', 'Prolific breed|large breed|long-wool|white wool|polled|upright ears'),
              ('bluefaced-leicester', 'Bluefaced Leicester', 'Prolific breed|large breed|long-wool|white wool|polled|upright ears|roman nose|blue skin'),
              ('galway', 'Galway', 'Large breed|white wool|polled|long-wool|“bob” of wool on forehead|good growth rates|not prolific')]
    rows, variants = routes([(slug, label, [menu(points, [3, 3], f'{label}: any two characteristics, 3 marks each (2 × 3m).')]) for slug, label, points in traits])
    add('q13aii', 'Q13(a)(ii)', '4-2', 'lowland-breed-characteristics', 'In the case of one of these breeds state two characteristics of the breed.', rows, breeds,
        selection=closed(1, [label for _, label, _ in traits]), node='3-1', extra={'answerVariants': variants})
    add('q13aiii', 'Q13(a)(iii)', '4-3-3', 'lamb-management-to-weaning', 'Describe the management of lambs from birth to weaning.',
        [menu('Clear mucus|navel dip|colostrum|vaccinate|tail docking|lambing pen|make sure ewe suckles lamb|mark lamb|tag lamb|infra-red lamp|castration|dosing|hardening off|hygiene|one feeding point|one housing point',
              [4] * 3, 'Any three, 4 marks each (3 × 4m).')], two, node='3-5|3-4')
    add('q13aiv', 'Q13(a)(iv)', '4-3-2', 'flushing-versus-steaming-up', 'Distinguish between flushing and steaming-up in lowland sheep production.',
        [point('Flushing: Process of moving ewes from a low plane of nutrition to a high plane of nutrition prior to mating or moving ewes to better grazing before mating', 3,
               '[Accept reason(s) for flushing e.g. increases fertility]'),
         point('Steaming up: Practice of feeding (increasing amount of) meals to ewes in late pregnancy', 3, '[Accept reason(s) for steaming up e.g. prevents twin lamb disease]')], two, node='3-4')
    add('q13bi', 'Q13(b)(i)', '4-2', 'irish-pig-breeds', 'Name two breeds of pig used in pig production in Ireland.',
        [menu('Large white|Landrace|Duroc|Saddleback|Tamworth', [3, 3], 'Any two, 3 marks each (2 × 3m).')], two, node='3-1')
    add('q13bii', 'Q13(b)(ii)', '4-3-2', 'dry-sow-and-farrowing-management', 'Describe the management of a sow in the dry sow house and in the farrowing house.',
        [menu('Kept loose|vaccinate|provide clean water|fed 2-3 kg meals per day|hygiene|mated 7-8 days after weaning|maintain temp. at 20° C', [3, 3], 'Dry sow house: any two, 3 marks each (2 × 3m).'),
         menu('Washed|de-wormed or dosed|treated for lice|dis-infected|vaccinated|good hygiene|placed in farrowing crate|provide temperature of 20ºC|provide clean water|fed 5-6 kg meals per day', [3, 3],
              'Farrowing house: any two, 3 marks each (2 × 3m).')], two, node='3-4')
    add('q13biii', 'Q13(b)(iii)', '4-3-3', 'bonham-anaemia', 'State the cause of anaemia in bonhams (piglets) and describe how it can be prevented.',
        [point('Cause of anaemia: lack of iron (in the diet)', 3), point('Prevention: Iron injection (in 1st week of life)', 3)], two, node='3-5')
    add('q13biv', 'Q13(b)(iv)', '4-3-2', 'gilt-selection', 'What criteria are used when selecting a gilt for breeding?',
        [menu('Good conformation|Good feet and legs|12 well-formed teats|healthy|reached puberty|docile|correct weight or correct body condition score|have come from mothers that are good milkers|come from mothers that are prolific',
              [3, 3], 'Any two, 3 marks each (2 × 3m).')], two, node='3-4')
    add('q13ci', 'Q13(c)(i)', '4-3-3', 'calf-death-precautions', 'Outline the precautions taken to reduce calf deaths at calving time on a dairy farm.',
        [menu('Good hygiene|adequate supervision|isolate cow at calving or calving box|steaming up of cow|reduce level of meal feeding in final week of pregnancy|clear mucus|navel dip|colostrum|proper equipment|call vet (if necessary)|good housing|choice of bull (ease of calving)|correct feeding technique (for calves)',
              [3] * 3, 'Any three, 3 marks each (3 × 3m).')], two, node='3-5')
    add('q13cii', 'Q13(c)(ii)', '4-3-3', 'why-feed-colostrum', 'Give two reasons why colostrum is fed to newly born calves.',
        [menu('Rich in antibodies|prevents diseases|rich in nutrients|laxative effect|warms the calf|high in energy', [3, 3], 'Any two, 3 marks each (2 × 3m).')], two, node='3-5')
    add('q13ciii', 'Q13(c)(iii)', '4-3-2', 'clean-milk-production', 'Describe two management practices which would result in the production of clean milk in the milking parlour.',
        [menu('Clean holding area|milker hygiene|parlour hygiene|wash or wipe udder|strip cup|teat dip|filter|plate cooler|wash equipment regularly|clean bulk tank|cool milk to 4ºC or less in bulk tank|fly screens|rubber mats or lime|disease control',
              [3, 3], 'Any two, 3 marks each (2 × 3m).')], two, node='3-4')
    add('q13civ', 'Q13(c)(iv)', '4-3-2', 'culling-dairy-cows', 'Give three reasons for culling cows from the herd.',
        [menu('Old age|grading up|lameness|disease|low milk yields|low milk quality|infertility|difficult to get back in calf or extended calving interval|calving difficulties|high somatic cell count|slow milkers|diseased udder',
              [3] * 3, 'Any three, 3 marks each (3 × 3m).')], two, node='3-4')
    carbon = two + (' Carbon dioxide levels in the atmosphere have become the subject of international concern in recent years, as demonstrated by the United Nations Climate Change Conference '
                    'held in Paris in December 2015.')
    add('q13di', 'Q13(d)(i)', '3-1', 'carbon-dioxide-in-photosynthesis', 'What happens to carbon dioxide during photosynthesis in green plants?',
        [point('To produce glucose or sugar', 3, '[Accept ‘starch’]')], carbon, node='2-0')
    add('q13dii', 'Q13(d)(ii)', '3-1', 'photosynthesis-pigment', 'Name the major pigment needed by plants for photosynthesis.', [point('Chlorophyll', 3)], carbon, node='2-0')
    caps = ' [Some, or all, of marks in method may be obtained from labelled diagram]'
    six = 'Method, result and conclusion together: any six points, 3 marks each (6 × 3m).'
    experiments = [
        ('method-a', 'Method A', '(potted) plant and plastic bag and dish (of soda lime)', 'plant/ plastic bag/ rubber band/ dish/ soda lime',
         [('method', 'Plant/ label A and B/ place in darkness/ 48 hours/ removes starch/ dish of soda lime in A/ soda lime absorbs CO2/ control/ water plants/ cover both plants with clear plastic/ light source/ ≥ 2hours/ '
                     'remove leaf from each plant/ boil leaf/ kills leaf/ place each leaf in alcohol for 10 minutes/ removes chlorophyll/ dip leaf in hot water/ softens leaf/ white tile/ cover with iodine',
           six + ' [Maximum of 2 × 3m from testing leaf]' + caps),
          ('result', 'A – no change in colour; B – turns blue-black or black', '[Maximum of 15 marks if no result for plant B given]'),
          ('conclusion', 'CO2 is needed for photosynthesis', None)]),
        ('method-b', 'Method B', 'pond weed and suitable container and water', 'pond weed or Elodea/ beaker or funnel or test tube/ water',
         [('method', 'Pondweed or Elodea/ suitable container',
           six + ' The scheme also credits labelling A and B: it prints "label test tubes A and B" with "test tubes" struck out.' + caps),
          ('method', 'reason why pondweed used/ add water to container(s)/ add excess sodium hydrogen carbonate to A/ why added/ no sodium hydrogen carbonate in B/ as control/ cut pondweed/ under water/ '
                     'place pondweed in containers A and B/ place A and B in water baths/ maintain temp. at 25º C/ dark room/ light source/ allow pondweed to adjust/ count bubbles (of oxygen) coming from pondweed', None),
          ('result', 'A – many bubbles (of oxygen) coming from pondweed; B - no (or very few) bubbles (of oxygen) coming from pondweed', '[Maximum of 15 marks if no result for plant A given]'),
          ('conclusion', 'CO2 is needed for photosynthesis', None)])]
    rows = []
    for slug, label, diagram, labels, parts in experiments:
        rows += [split(f'{label} diagram — {diagram}', f'Diagram: 3m or 0m. [For 3 marks diagram must show {diagram}]', route=slug, kind='criterion'),
                 split(f'{label} labels — {labels}', 'Labels: any three, 1 mark each (3 × 1m).', route=slug)]
        rows += [split(f'{label} {part} — {text}', note, route=slug) for part, text, note in parts]
    add('q13diii', 'Q13(d)(iii)', '3-1', 'carbon-dioxide-photosynthesis-experiment',
        'Describe, with the aid of a labelled diagram, a laboratory experiment to show that carbon dioxide is needed for photosynthesis.', rows, carbon,
        marks=24, tariff={'kind': 'questionTotal', 'notation': 'D (3m, 0m) + 3 × 1m + 6 × 3m'},
        selection=closed(1, [label for _, label, *_ in experiments]), node='2-0|0-1')
    assert len(p.tasks) == 69, len(p.tasks)
    return p


def reviewed_tasks():
    p = build()
    return p.cards, p.tasks


def paper_review():
    return build().review('69 base tasks, one card each. Section One is one task per question: a shared scale across parts (Q5, Q6, Q7) is stated on the card, '
                          'and parts priced on their own (Q1-Q4) carry their marks. Section Two parts are priced on their own; the four Q11(a) headings carry 4 marks each. '
                          'Q8(a)(iii) sowing methods, Q13(a)(ii) breeds and Q13(d)(iii) carbon dioxide experiments are answer routes.')
