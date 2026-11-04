"""2015 Ordinary: every task authored from the SEC paper and marking scheme (no cards existed).

All 16 paper pages and 16 scheme pages were inspected and the independent census transcribed
before authoring: 63 base tasks, one card each. Section One questions are one task each, every
row carrying its own marks (5 × 4m, 4 × (3m + 2m), 10 × 2m); Q4's four cereals are answer routes.
Section Two parts are priced on their own. The Q12(c) cross is one task because the scheme ties
its genotype and phenotype marks to the lines above. The silage dry-matter methods (Q8(c)) and
the soil-texture methods (Q10(b)(ii)) are answer routes. Answers are the scheme's words.
"""
from agricultural_science_legacy import Paper, P, point, menu, closed, routes

FILE = 'LC024GLP000EV.pdf'
HASHES = {'exampapers': '9b807c836452b0b7fccef5d621b7c808374f284bd4b69236f34ca1a7b5d43ba7',
          'markingschemes': 'b39d01b60b7f6bfb66d583e5f0f297b49ec018e1860ce7e8d52f5715b638eefa'}
SELECTIONS = {
    '3639198ec73bd0a5': ('exam-selection', 'Section One: six of seven independent 20-mark questions; every question is retained.'),
    '9886f1326401f117': ('closed', 'Q4: one of the four pictured cereals, kept as four answer routes on one card.'),
    '1693adb03d028dd0': ('exam-selection', 'Section Two: three of six independent 60-mark questions; every question is retained.'),
    '6a67777492f6d3da': ('open', 'Q10(a)(ii): any three soil particle types from the scheme\'s four; a marking menu.'),
    '1c2a4c271a6052fb': ('open', 'Q12(a)(i): any three labels from the scheme\'s six; a marking menu.'),
    'd8109798a1f4bb86': ('independent-task-selection', 'Q13: two of four independently priced 30-mark parts; all four are retained.'),
    'ba0aed54a045327f': ('open', 'Q13(a)(ii): any three reasons from the scheme pool; a marking menu.'),
    'f439ef126fcd4f57': ('open', 'Q13(c)(ii): any three factors from the scheme pool; a marking menu.'),
    'dc3da7497d08f33d': ('open', 'Q13(c)(iii): any three milk tests from the scheme pool; a marking menu.'),
    '5bdd75c2f9772e3b': ('open', 'Q13(c)(iv): any two hygiene practices from the scheme pool; a marking menu.'),
}
SUPPLEMENTARY = [
    (8, 'Describe a laboratory or field experiment to estimate percentage', 'closed', 'Q8(c): the scheme gives an oven-drying method OR a wringing method, kept as answer routes on one card.'),
    (9, 'Describe an experiment to determine the texture of a soil sample', 'closed', 'Q10(b)(ii): the scheme gives the feel, sieve and sedimentation methods, kept as answer routes on one card.'),
]
ATLAS = {
    'Q1': 'plant-physiology', 'Q2': 'classification-of-organisms|animal-diseases', 'Q3': 'plant-physiology|animal-diseases|crop-production|animal-physiology|animal-production',
    'Q4': 'crop-production', 'Q5': 'scientific-practices-experiments-investigations', 'Q6': 'animal-diseases', 'Q7': 'animal-production|crop-production|soil-science|health-safety',
    'Q8': 'grassland', 'Q8(c)': 'grassland|scientific-practices-experiments-investigations',
    'Q9': 'animal-production', 'Q9(c)': 'animal-production|animal-diseases',
    'Q10': 'soil-science', 'Q10(b)(ii)': 'soil-science|scientific-practices-experiments-investigations', 'Q10(c)': 'soil-science|classification-of-organisms',
    'Q10(c)(iii)': 'soil-science|scientific-practices-experiments-investigations',
    'Q11': 'animal-physiology', 'Q11(c)': 'animal-production|animal-diseases', 'Q11(c)(i)': 'animal-production',
    'Q12': 'genetics', 'Q12(a)': 'plant-physiology|genetics',
    'Q13(a)': 'animal-production', 'Q13(b)': 'crop-production', 'Q13(c)': 'animal-production', 'Q13(d)': 'animal-production',
}
REGIONS = {
    # Drafted by regions.py.
    'Q1': (P((2, 0.345, 0.712)), P((5, 0.107, 0.304))),
    'Q2': (P((3, 0.083, 0.410)), P((5, 0.304, 0.619))),
    'Q3': (P((3, 0.410, 0.882)), P((5, 0.619, 0.834))),  # stops above the page footer
    'Q4': (P((4, 0.083, 0.795)), P((6, 0.080, 0.413))),
    'Q5': (P((5, 0.083, 0.897)), P((6, 0.413, 0.639))),  # stops above the page footer
    'Q6': (P((6, 0.083, 0.537)), P((7, 0.080, 0.461))),
    'Q7': (P((7, 0.083, 0.882)), P((7, 0.461, 0.848))),  # stops above the page footer
    'Q8(a)(i)': (P((8, 0.262, 0.365)), P((8, 0.119, 0.185))),
    'Q8(a)(ii)': (P((8, 0.262, 0.344), (8, 0.365, 0.381)), P((8, 0.119, 0.141), (8, 0.185, 0.268))),
    'Q8(a)(iii)': (P((8, 0.262, 0.344), (8, 0.381, 0.413)), P((8, 0.119, 0.141), (8, 0.268, 0.334))),
    'Q8(a)(iv)': (P((8, 0.262, 0.344), (8, 0.413, 0.442)), P((8, 0.119, 0.141), (8, 0.334, 0.383))),
    'Q8(b)(i)': (P((8, 0.262, 0.344), (8, 0.442, 0.463)), P((8, 0.119, 0.141), (8, 0.383, 0.482))),
    'Q8(b)(ii)': (P((8, 0.262, 0.344), (8, 0.463, 0.480)), P((8, 0.119, 0.141), (8, 0.482, 0.564))),
    'Q8(b)(iii)': (P((8, 0.262, 0.344), (8, 0.480, 0.508)), P((8, 0.119, 0.141), (8, 0.564, 0.662))),
    'Q8(c)': (P((8, 0.262, 0.344), (8, 0.508, 0.606)), P((8, 0.119, 0.141), (8, 0.662, 0.890))),
    'Q9(a)(i)': (P((8, 0.606, 0.692)), P((9, 0.080, 0.229))),
    'Q9(a)(ii)': (P((8, 0.606, 0.672), (8, 0.692, 0.721)), P((9, 0.080, 0.113), (9, 0.229, 0.360))),
    'Q9(b)(i)': (P((8, 0.606, 0.672), (8, 0.721, 0.758)), P((9, 0.080, 0.113), (9, 0.360, 0.426))),
    'Q9(b)(ii)': (P((8, 0.606, 0.672), (8, 0.758, 0.774)), P((9, 0.080, 0.113), (9, 0.426, 0.458))),
    'Q9(b)(iii)': (P((8, 0.606, 0.672), (8, 0.774, 0.803)), P((9, 0.080, 0.113), (9, 0.458, 0.524))),
    'Q9(c)(i)': (P((8, 0.606, 0.672), (8, 0.803, 0.824)), P((9, 0.080, 0.113), (9, 0.524, 0.606))),
    'Q9(c)(ii)': (P((8, 0.606, 0.672), (8, 0.824, 0.892)), P((9, 0.080, 0.113), (9, 0.606, 0.665))),
    'Q10(a)(i)': (P((9, 0.083, 0.152)), P((10, 0.080, 0.162))),
    'Q10(a)(ii)': (P((9, 0.083, 0.136), (9, 0.152, 0.181)), P((10, 0.080, 0.113), (10, 0.162, 0.211))),
    'Q10(b)(i)': (P((9, 0.083, 0.115), (9, 0.181, 0.201)), P((10, 0.080, 0.113), (10, 0.211, 0.244))),
    'Q10(b)(ii)': (P((9, 0.083, 0.115), (9, 0.201, 0.230)), P((10, 0.080, 0.113), (10, 0.244, 0.625))),
    'Q10(c)(i)': (P((9, 0.083, 0.115), (9, 0.230, 0.422)), P((10, 0.080, 0.113), (10, 0.625, 0.657))),
    'Q10(c)(ii)': (P((9, 0.083, 0.115), (9, 0.230, 0.401), (9, 0.422, 0.439)), P((10, 0.080, 0.113), (10, 0.657, 0.723))),
    'Q10(c)(iii)': (P((9, 0.083, 0.115), (9, 0.230, 0.401), (9, 0.439, 0.497)), P((10, 0.080, 0.113), (10, 0.723, 0.799))),  # stops after (60 marks), above the page footer
    'Q11(a)(i)': (P((10, 0.083, 0.372)), P((11, 0.080, 0.179))),
    'Q11(a)(ii)': (P((10, 0.083, 0.319), (10, 0.372, 0.389)), P((11, 0.080, 0.113), (11, 0.179, 0.244))),
    'Q11(a)(iii)': (P((10, 0.083, 0.319), (10, 0.389, 0.433)), P((11, 0.080, 0.113), (11, 0.244, 0.277))),
    'Q11(b)(i)': (P((10, 0.083, 0.319), (10, 0.433, 0.454)), P((11, 0.080, 0.113), (11, 0.277, 0.310))),
    'Q11(b)(ii)': (P((10, 0.083, 0.319), (10, 0.454, 0.486)), P((11, 0.080, 0.113), (11, 0.310, 0.359))),
    'Q11(b)(iii)': (P((10, 0.083, 0.319), (10, 0.486, 0.503)), P((11, 0.080, 0.113), (11, 0.359, 0.409))),
    'Q11(b)(iv)': (P((10, 0.083, 0.319), (10, 0.503, 0.532)), P((11, 0.080, 0.113), (11, 0.409, 0.474))),
    'Q11(c)(i)': (P((10, 0.083, 0.319), (10, 0.532, 0.553)), P((11, 0.080, 0.113), (11, 0.474, 0.523))),
    'Q11(c)(ii)': (P((10, 0.083, 0.319), (10, 0.553, 0.604)), P((11, 0.080, 0.113), (11, 0.523, 0.566))),
    'Q12(a)(i)': (P((11, 0.083, 0.152)), P((12, 0.080, 0.246))),
    'Q12(a)(ii)': (P((11, 0.083, 0.115), (11, 0.152, 0.168)), P((12, 0.080, 0.113), (12, 0.246, 0.279))),
    'Q12(a)(iii)': (P((11, 0.083, 0.115), (11, 0.168, 0.213)), P((12, 0.080, 0.113), (12, 0.279, 0.319))),
    'Q12(b)(i)': (P((11, 0.083, 0.115), (11, 0.213, 0.384)), P((12, 0.080, 0.113), (12, 0.320, 0.360))),  # hand-set: the scheme prints the cross lines without (i)-(iii)
    'Q12(b)(ii)': (P((11, 0.083, 0.115), (11, 0.213, 0.352), (11, 0.392, 0.417)), P((12, 0.080, 0.113), (12, 0.361, 0.389))),  # hand-set: the scheme prints the cross lines without (i)-(iii)
    'Q12(b)(iii)': (P((11, 0.083, 0.115), (11, 0.213, 0.352), (11, 0.425, 0.452)), P((12, 0.080, 0.113), (12, 0.393, 0.421))),  # hand-set: the scheme prints the cross lines without (i)-(iii)
    'Q12(c)': (P((11, 0.083, 0.115), (11, 0.492, 0.780)), P((12, 0.080, 0.113), (12, 0.443, 0.619))),  # stops above the page's [OVER] footer
    'Q13(a)(i)': (P((12, 0.083, 0.152)), P((13, 0.080, 0.146))),
    'Q13(a)(ii)': (P((12, 0.083, 0.131), (12, 0.152, 0.169)), P((13, 0.080, 0.113), (13, 0.146, 0.211))),
    'Q13(a)(iii)': (P((12, 0.083, 0.131), (12, 0.169, 0.185)), P((13, 0.080, 0.113), (13, 0.211, 0.293))),
    'Q13(a)(iv)': (P((12, 0.083, 0.131), (12, 0.185, 0.262)), P((13, 0.080, 0.113), (13, 0.293, 0.425))),
    'Q13(b)(i)': (P((12, 0.083, 0.131), (12, 0.262, 0.332)), P((13, 0.080, 0.113), (13, 0.425, 0.523))),
    'Q13(b)(ii)': (P((12, 0.083, 0.131), (12, 0.332, 0.349)), P((13, 0.080, 0.113), (13, 0.523, 0.572))),
    'Q13(b)(iii)': (P((12, 0.083, 0.131), (12, 0.349, 0.365)), P((13, 0.080, 0.113), (13, 0.572, 0.638))),
    'Q13(b)(iv)': (P((12, 0.083, 0.131), (12, 0.365, 0.410)), P((13, 0.080, 0.113), (13, 0.638, 0.720))),
    'Q13(c)(i)': (P((12, 0.083, 0.131), (12, 0.410, 0.611)), P((13, 0.080, 0.113), (13, 0.720, 0.769))),
    'Q13(c)(ii)': (P((12, 0.083, 0.131), (12, 0.410, 0.590), (12, 0.611, 0.627)), P((13, 0.080, 0.113), (13, 0.769, 0.834))),
    'Q13(c)(iii)': (P((12, 0.083, 0.131), (12, 0.410, 0.590), (12, 0.627, 0.660)), P((13, 0.080, 0.113), (13, 0.834, 0.894))),
    'Q13(c)(iv)': (P((12, 0.083, 0.131), (12, 0.410, 0.590), (12, 0.660, 0.705)), P((13, 0.080, 0.113), (14, 0.080, 0.181))),
    'Q13(d)(i)': (P((12, 0.083, 0.131), (12, 0.705, 0.759)), P((13, 0.080, 0.113), (14, 0.181, 0.214))),
    'Q13(d)(ii)': (P((12, 0.083, 0.131), (12, 0.705, 0.738), (12, 0.759, 0.775)), P((13, 0.080, 0.113), (14, 0.214, 0.246))),
    'Q13(d)(iii)': (P((12, 0.083, 0.131), (12, 0.705, 0.738), (12, 0.775, 0.791)), P((13, 0.080, 0.113), (14, 0.246, 0.312))),
    'Q13(d)(iv)': (P((12, 0.083, 0.131), (12, 0.705, 0.738), (12, 0.791, 0.808)), P((13, 0.080, 0.113), (14, 0.312, 0.377))),
    'Q13(d)(v)': (P((12, 0.083, 0.131), (12, 0.705, 0.738), (12, 0.808, 0.824)), P((13, 0.080, 0.113), (14, 0.377, 0.410))),
    'Q13(d)(vi)': (P((12, 0.083, 0.131), (12, 0.705, 0.738), (12, 0.824, 0.863)), P((13, 0.080, 0.113), (14, 0.410, 0.440))),
}
FIGURES = {
    'q4': ('agsci-2015-ol-paper-spring-cereals', [('A', 'Barley', True), ('B', 'Maize (the scheme accepts corn)', True), ('C', 'Oats', True), ('D', 'Wheat', True)]),
    'q5': ('agsci-2015-ol-paper-habitat-apparatus', [('A', 'Quadrat', True), ('B', 'Pooter', True), ('C', '(Sweep) net', True), ('D', '(Soil) thermometer', True)]),
    'q10ci': ('agsci-2015-ol-paper-earthworm', None), 'q10cii': ('agsci-2015-ol-paper-earthworm', None), 'q10ciii': ('agsci-2015-ol-paper-earthworm', None),
    'q11aii': ('agsci-2015-ol-paper-ruminant-stomach', [('B', 'Reticulum', True), ('C', 'Omasum', True), ('D', 'Abomasum', True)]),
    'q11aiii': ('agsci-2015-ol-paper-ruminant-stomach', None), 'q11bii': ('agsci-2015-ol-paper-ruminant-stomach', None),
    'q11biii': ('agsci-2015-ol-paper-ruminant-stomach', None), 'q11biv': ('agsci-2015-ol-paper-ruminant-stomach', None),
    'q13ci': ('agsci-2015-ol-paper-milk-composition', [('A', 'Water', True), ('B', 'Protein', True)]),
    'q13cii': ('agsci-2015-ol-paper-milk-composition', None), 'q13ciii': ('agsci-2015-ol-paper-milk-composition', None),
    'q13civ': ('agsci-2015-ol-paper-milk-composition', None),
}


def figured(card, key):
    figure, labels = FIGURES[key]
    card['figureKey'] = figure
    if labels:
        card['labelKey'] = [dict(letter=l, meaning=m, askedInThisQuestion=a) for l, m, a in labels]
    return card


def build():
    p = Paper(2015, 'ordinary', FILE, HASHES, REGIONS, ATLAS, 16, 16, SELECTIONS, SUPPLEMENTARY,
              section=lambda ref: 'A' if int(ref.split('(')[0].split(' ')[0][1:]) <= 7 else 'B')
    add = p.add
    # Section One ------------------------------------------------------------
    add('q1', 'Q1', '3-1', 'plant-parts-and-functions',
        'A list of plant parts is given below. Place these in Column A to match the description of each part in Column B. The first one is completed as an example. '
        'List: Stamens; Phloem; Petals; Xylem; Carpels; Stomata. Example: Petals — Attract bees and insects. Column B: Male parts of flower; Transports water through plant; '
        'Openings on underside of leaf; Female parts of flower; Transports food through plant.',
        [point('Male parts of flower — Stamens', 4, 'One part for each description, 4 marks each (5 × 4m).'), point('Transports water through plant — Xylem', 4),
         point('Openings on underside of leaf — Stomata', 4), point('Female parts of flower — Carpels', 4), point('Transports food through plant — Phloem', 4)],
        tariff={'kind': 'fixed', 'notation': '5 × 4m'}, node='2-0')
    organisms = [('Roundworm', 'Nematoda', '(Animal) parasite or pest/ weight loss or failure to thrive/ diarrhoea/ dehydration/ death/ causes disease or harm'),
                 ('Liver Fluke', 'Platyhelminthes', '(Animal) parasite or pest/ weight loss or failure to thrive/ anaemia/ reduced milk yield/ death/ diarrhoea/ loss of wool or hair/ causes disease or harm'),
                 ('Butterfly', 'Arthropoda', 'Pollination/ aids plant reproduction/ caterpillar or larval stage is a plant pest/ caterpillar stage damages plants'),
                 ('Mud Snail', 'Mollusca', '(Secondary) host of liverfluke')]
    rows = [menu([f'{organism}: {phylum}' for organism, phylum, _ in organisms], [3] * 4, '4 × (3m + 2m): the phylum 3 for each organism.'),
            menu([f'{organism} ({phylum}): {importance}' for organism, phylum, importance in organisms], [2] * 4, 'One importance (any one) 2 for each organism.')]
    add('q2', 'Q2', '3-2', 'organism-phyla-and-importance',
        'Some organisms of importance in agriculture are listed in the table below. In the table, name the phylum to which each organism belongs and state one reason why the organism is important in agriculture: '
        'Roundworm; Liver Fluke; Butterfly; Mud Snail.', rows, tariff={'kind': 'fixed', 'notation': '4 × (3m + 2m)'}, node='3-1|2-1|3-5')
    statements = [('a', 'Germination is the production of food in the leaf.', 'F'), ('b', 'Pneumonia is a common disease of calves.', 'T'),
                  ('c', 'Biuret reagent is used to test for protein.', 'T'), ('d', 'Urea is a high nitrogen fertiliser.', 'T'), ('e', 'Oak is a coniferous tree.', 'F'),
                  ('f', 'Powdery mildew is a disease of barley.', 'T'), ('g', 'Incisors are teeth used for cutting food.', 'T'), ('h', 'A hogget is a type of pig.', 'F'),
                  ('i', 'Kale is an example of a catch crop.', 'T'), ('j', 'Cows reach their peak milk yield one week after calving.', 'F')]
    add('q3', 'Q3', '4-1', 'true-or-false-farm-science',
        'Indicate whether the following statements are true (T) or false (F) by placing a circle around the correct answer in each case as shown in the example. '
        'Example: Suffolk is a breed of cow — F. ' + ' '.join(f'({k}) {s}' for k, s, _ in statements),
        [menu([f'({k}) {a}' for k, _, a in statements], [2] * 10,
              'All ten statements, 2 marks each (10 × 2m). T = true, F = false; the scheme gives each letter with T or F.')],
        tariff={'kind': 'fixed', 'notation': '10 × 2m'}, node='2-0|3-5|0-1|1-6|2-4|3-0|3-1|3-4')
    crops = [('barley', 'Barley', 'A = Barley', 'Feb – April', 'Animal feed/ malting/ food or named example/ straw bedding', '150 – 200', '5 – 8'),
             ('maize', 'Maize', 'B = Maize', 'March – May', 'Animal feed/ silage/ food or named example/ straw bedding', '20 - 28', '13 - 20'),
             ('oats', 'Oats', 'C = Oats', 'Feb - April', 'Animal feed/ food or named example/ straw bedding', '140 – 165', '4 – 7'),
             ('wheat', 'Wheat', 'D = Wheat', 'Feb - April', 'Animal feed/ flour production/ food or named example/ straw bedding', '140 – 190', '7 – 9')]
    rows, variants = routes([(slug, label, [point(f'Crop and name — {name}', 4, '5 × 4m: one row of the table each.' + (' [accept corn]' if slug == 'maize' else '')),
                                            point(f'Time of sowing — {sowing}', 4), point(f'Use of crop — {use}', 4, 'Any one.'),
                                            point(f'Seeding rate (kg/ha) — {rate}', 4), point(f'Yield of crop (t/ha) — {yld}', 4)])
                             for slug, label, name, sowing, use, rate, yld in crops])
    figured(add('q4', 'Q4', '3-3-1', 'spring-cereal-table',
                'Four spring cereal crops commonly grown in Ireland are shown below. In the table, identify one of the crops shown above and complete the table in relation to the crop you have chosen: '
                'Crop A, B, C or D; Name of crop; Time of sowing; Use of crop; Seeding rate (kg/ha); Yield of crop (t/ha).', rows,
                tariff={'kind': 'fixed', 'notation': '5 × 4m'}, selection=closed(1, [label for _, label, *_ in crops]), node='2-3|2-5', extra={'answerVariants': variants}), 'q4')
    apparatus = [('A', 'Quadrat', 'Sampling plants/ quantitative analysis/ studying (frequency of) plants'), ('B', 'Pooter', 'Collecting insects or (small) animals'),
                 ('C', '(Sweep) net', 'Collecting insects or (small) animals'), ('D', '(Soil) thermometer', 'Measuring (soil) temperature')]
    rows = [menu([f'{letter}: {name}' for letter, name, _ in apparatus], [3] * 4, '4 × (3m + 2m): the name 3 for each piece.'),
            menu([f'{letter} {name}: {use}' for letter, name, use in apparatus], [2] * 4, 'The use 2 for each piece (A: any one).')]
    figured(add('q5', 'Q5', '1-2', 'habitat-study-apparatus',
                'Four pieces of apparatus commonly used in habitat study are shown below. In the table, give the name and use for each piece: A; B; C; D.', rows,
                tariff={'kind': 'fixed', 'notation': '4 × (3m + 2m)'}, node='0-1|2-6'), 'q5')
    diseases = [('Mastitis', 'Bacteria', 'Parlour hygiene/ milker hygiene/ wash udder/ avoid over-milking/ teat dip/ strip cup/ antibiotic/ dry cow therapy/ clean bedding or cubicle mats or lime/ ensure milking machine in working order/ treat wounds on teats/ fly control/ apply Stockholm tar to teats/ cull chronically infected cows'),
                ('Pneumonia', 'Virus', 'Good ventilation/ draught free/ isolation/ colostrum/ vaccination/ dry housing/ avoid stress'),
                ('Ringworm', 'Fungus', 'Avoid contact with infected animals/ apply fungicide'),
                ('Blackleg', 'Bacteria', 'Vaccination/ colostrum (for lambs)/ antibiotics/ booster injection')]
    rows = [menu([f'{disease}: {microbe}' for disease, microbe, _ in diseases], [3] * 4, '4 × (3m + 2m): the microorganism type 3 for each disease.'),
            menu([f'{disease} ({microbe}): {prevention}' for disease, microbe, prevention in diseases], [2] * 4, 'One prevention or treatment (any one) 2 for each disease.')]
    add('q6', 'Q6', '4-3-3', 'cattle-disease-microbes',
        'Four common diseases of cattle that are caused by microorganisms are listed in the table below. In the table, state which type of microorganism is responsible for causing each disease and one method of prevention or treatment of each disease. '
        'One example is given in the table: TB — Bacteria — Breeding own replacements. Mastitis; Pneumonia; Ringworm; Blackleg.', rows,
        tariff={'kind': 'fixed', 'notation': '4 × (3m + 2m)'}, node='3-5')
    add('q7', 'Q7', '2-3', 'reasons-for-farm-practices',
        'Give one scientific reason why each of the following practices is carried out on Irish farms. (a) Sheep are culled from the flock. (b) Cows are ‘dried off’ two months before calving. '
        '(c) Trees in a forest plantation are thinned after about twenty years. (d) Lime is spread on some soils. (e) Great care is taken when agitating slurry.',
        [point('(a) Culling sheep — Lameness/ old age/ infertility/ disease/ mastitis/ broken mouth/ low BCS/ poor conformation/ poor quality wool/ mouth defects / prolapse/ poor previous performance or low number of lambs', 4,
               'One reason for each practice, 4 marks each (5 × 4m).'),
         point('(b) Drying off cows — Repair or regeneration of udder tissue/ improves BCS for calving/ cow does not lose condition/ allows for rapid development of calf/ gives cow a rest or allows cow to recover/ allows cow to reach milk yield potential (in following lactation) or cow will have more milk after calving', 4),
         point('(c) Thinning trees — Removes poorer trees/ more space/ less competition or named example/ remaining trees grow straighter or better/ improved access/ thinnings provide source of income/ use of thinnings to make products or named example', 4),
         point('(d) Spreading lime — Raises pH/ reduces acidity/ improves soil structure/ provides calcium/ improves aeration or opens up the soil/ flocculation/ improves drainage/ increases availability of nutrients/ improved crop growth/ higher yields/ improved microbial activity/ more earthworm activity/ improves soil fertility', 4),
         point('(e) Care when agitating slurry — Avoids toxic gases or named toxic gas/ avoids harm/ prevents deaths/ animal safety', 4)],
        tariff={'kind': 'fixed', 'notation': '5 × 4m'}, node='3-4|2-4|1-2|1-6')
    # Question 8 -------------------------------------------------------------
    hay = 'The two most common methods of grass conservation used in Ireland are silage production and hay production.'
    add('q8ai', 'Q8(a)(i)', '3-3-1', 'conservation-grass-species', 'Name two grass species commonly used in silage or hay production.',
        [menu('Perennial ryegrass or PRG|Italian ryegrass or IRG|Timothy', [3, 3], 'Any two, 3 marks each (2 × 3m). [Accept ryegrass]')], hay, node='2-6')
    add('q8aii', 'Q8(a)(ii)', '3-3-3', 'silage-cutting-stage', 'At what stage should the grass be cut for good quality silage?',
        [menu('Heading out stage|“in between” stage|6-8 week after closing off|May- (early) June|10 -12 weeks after fertiliser applied|when 50% grass showing seed heads', [3],
              'Any one, 3m. [Accept when grass is leafy]')], hay, node='2-6')
    add('q8aiii', 'Q8(a)(iii)', '3-3-3', 'dry-weather-for-hay', 'A long spell of dry weather is essential for making hay. What is the scientific reason for this?',
        [menu('Dehydration|enough time for grass, or hay, to dry|avoid mould infestation|avoid rotting or spoilage or heating', [3], 'Any one, 3m.')], hay, node='2-6')
    add('q8aiv', 'Q8(a)(iv)', '3-3-3', 'silage-bacteria', 'Give the name of a bacterial species needed to make good quality silage.', [point('Lactobacillus spp./ lactic acid bacteria', 3)], hay, node='2-6')
    add('q8bi', 'Q8(b)(i)', '3-3-3', 'haymaking-steps', 'Describe the steps you would carry out to make good quality hay.',
        [menu('Cut or mow|on dry day|allow to dry or wilt|ted or turn or shake|2-3 times|reduce degree of roughness of shaking|row or rake or gather|bale|stack in field|store in (leak proof) shed', [3] * 4,
              'Any four, 3 marks each (4 × 3m).')], hay, node='2-6')
    add('q8bii', 'Q8(b)(ii)', '3-3-3', 'silage-over-hay', 'Give three advantages of silage production over hay production.',
        [menu('Less weather dependent|faster|silage more digestible or higher DMD|silage higher in protein|higher feeding value or more nutritious|higher weight gains or milk yields|easier to feed|more palatable|easier to store', [3] * 3,
              'Any three, 3 marks each (3 × 3m).')], hay, node='2-6')
    add('q8biii', 'Q8(b)(iii)', '3-3-3', 'round-bale-over-pit', 'Give three advantages of round bale silage over pit silage.',
        [menu('Easier to make in small fields|lower capital costs or no need for a pit|easy to transport|easy to buy or sell|ease of storage|suitable for small amounts|can be fed outside|lower pollution risk|lower (dry matter) losses during production or storage', [3] * 3,
              'Any three, 3 marks each (3 × 3m).')], hay, node='2-6')
    methods = [('oven', 'Drying in an oven', 'Weigh beaker or named suitable container|weigh beaker and silage sample|calculate mass of silage|dry in oven|suitable time|re-weigh beaker and silage|repeat until no further loss in mass|calculate loss in mass|(loss in mass ÷ mass of fresh silage) x 100|repeat|average',
                ' [Award marks if points are shown on a labelled diagram] [Award maximum of 12 marks if no attempt at calculation]'),
               ('wring', 'Wringing between hands', 'Wring silage between hands|note rate at which juice runs out or note the amount of juice that runs out|if juice runs freely ⇒15% dry matter (DM)|if juice drips out ⇒20% DM|if very little juice runs out ⇒25% DM|repeat|average', '')]
    rows, variants = routes([(slug, label, [menu(steps, [3] * 5, f'{label}: any five, 3 marks each (5×3m).{caps}')]) for slug, label, steps, caps in methods])
    add('q8c', 'Q8(c)', '3-3-3', 'silage-dry-matter', 'Describe a laboratory or field experiment to estimate percentage (%) dry matter in a silage sample.', rows, hay,
        selection=closed(1, [label for _, label, *_ in methods]), node='2-6|0-1', extra={'answerVariants': variants})
    # Question 9 -------------------------------------------------------------
    breeds = 'Beef breeds and dairy breeds are commonly found on Irish cattle farms.'
    add('q9ai', 'Q9(a)(i)', '4-2', 'beef-and-dairy-breeds', 'Name two beef breeds and two dairy breeds.',
        [menu('Charolais|Limousin|Hereford|Aberdeen Angus|Belgian Blue', [3, 3], 'Beef breeds: any two, 3 marks each (2 × 3m).'),
         menu('Jersey|Holstein|(British) Friesian|Kerry|Montbeliarde', [3, 3], 'Dairy breeds: any two, 3 marks each (2 × 3m). [Accept Shorthorn]')], breeds, node='3-1')
    add('q9aii', 'Q9(a)(ii)', '4-2', 'beef-versus-dairy-conformation', 'Describe three differences between the conformation of beef and dairy breeds.',
        [point('Beef — Block shaped/ thick neck/ wide shoulders/ well fleshed or more muscle or heavier/ broad back/ wider hindquarters', None,
               'Any three differences, 4 marks each (3 × 4m): a beef feature set against the dairy feature.'),
         point('Dairy — Wedge shaped/ long neck/ narrow shoulders/ not well fleshed/ narrow back/ narrower hindquarters', None)],
        breeds, marks=12, tariff={'kind': 'questionTotal', 'notation': '3 × 4m'}, node='3-1')
    bcs = 'Condition scoring is an important skill in cattle farming.'
    add('q9bi', 'Q9(b)(i)', '4-3-2', 'condition-scoring', 'Explain what is meant by condition scoring in cattle.',
        [menu('Hand pressure applied to (specific areas of) backbone|to assess body fatness or thinness|scale of 1-5 in cattle|1 indicates overly thin|4 indicates overly fat', [4, 4], 'Any two, 4 marks each (2×4m).')], bcs, node='3-4')
    add('q9bii', 'Q9(b)(ii)', '4-3-2', 'condition-score-at-mating', 'What condition score is recommended for cows at mating?', [point('2.5 to 3', 4)], bcs, node='3-4')
    add('q9biii', 'Q9(b)(iii)', '4-3-2', 'high-condition-at-calving', 'Explain why a high condition score in cows can cause problems at calving.',
        [menu('Calf too big or calving difficulties or described|requirement for Caesarean or calving jack or vet|too much fat deposition in birth canal|milk fever', [4, 4], 'Any two, 4 marks each (2 × 4m).')],
        bcs, node='3-4')
    add('q9ci', 'Q9(c)(i)', '4-3-3', 'buying-replacement-heifers', 'State two precautions that should be taken when buying in replacement heifers.',
        [menu('Known supplier|quarantine or isolate|vaccinate|good BCS or good quality (or one named physical characteristic indicating good quality|check for diseases or for signs of good health|good temperament|good udder or good teat placement',
              [4, 4], 'Any two, 4 marks each (2 × 4m).')], node='3-5|3-4')
    add('q9cii', 'Q9(c)(ii)', '4-3-3', 'keeping-disease-out', 'Describe two common practices aimed at keeping livestock diseases from entering a farm.',
        [menu('Breed own replacements or closed herd|fencing|hygiene|disinfection points|quarantine|restrict access or visitors', [4, 4], 'Any two, 4 marks each (2 × 4m).')], node='3-5')
    # Question 10 ------------------------------------------------------------
    rock = 'The main mineral component of soil is made up of different particles of weathered rock.'
    add('q10ai', 'Q10(a)(i)', '2-1', 'physical-weathering', 'State three methods of physical weathering.',
        [menu('Freeze-thaw or frost action|heating and cooling or onion weathering|wind action|ice|water|gravity|roots|animal activity|grinding|erosion', [3] * 3, 'Any three, 3 marks each (3 × 3m).')], rock, node='1-0')
    add('q10aii', 'Q10(a)(ii)', '2-2-2', 'soil-particle-types', 'Name any three soil particle types.',
        [menu('Gravel|sand|silt|clay', [3] * 3, 'Any three, 3 marks each (3 × 3m).')], rock, node='1-3')
    add('q10bi', 'Q10(b)(i)', '2-2-2', 'soil-texture', 'Explain the term soil texture.', [point('The % sand, silt and clay in a soil', 6)], node='1-3')
    textures = [('feel', 'Feel method', 'Rub or feel (dry) soil (between thumb and fingers)|note grittiness or smoothness|repeat with wet soil|roll into a ball if possible|make threads of it if possible|bend into rings if possible|compare to flow chart for results|if soil feels gritty ⇒sandy soil|if soil rolls into threads ⇒clay soil'),
                ('sieve', 'Sieve method', 'Dry soil|how dried|crush the soil|weigh an empty weighing boat or named suitable container|place soil in a weighing boat|reweigh|find mass of soil (only)|sieve soil|re-weigh each part|calculate % sand, silt and clay|use soil textural triangle|use % figures to draw three lines|where lines cross over indicates soil textural class'),
                ('sedimentation', 'Sedimentation method', 'Place soil sample into a graduated cylinder or named suitable vessel|add water to vessel|break up large lumps|stopper|shake vigorously|allow to settle|measure total depth of soil|measure each layer of sand silt and clay|calculate % sand, silt and clay|use soil textural triangle|use % figures to draw three lines|where lines cross over indicates soil textural class')]
    rows, variants = routes([(slug, label, [menu(steps, [3] * 5, f'{label}: any five, 3 marks each (5 ×3m). [Award marks if points are shown on a labelled diagram]')]) for slug, label, steps in textures])
    add('q10bii', 'Q10(b)(ii)', '2-2-2', 'soil-texture-experiment', 'Describe an experiment to determine the texture of a soil sample.', rows,
        selection=closed(1, [label for _, label, _ in textures]), node='1-3|0-1', extra={'answerVariants': variants})
    worm = 'Organisms such as the one shown below are of great benefit to the soil.'
    figured(add('q10ci', 'Q10(c)(i)', '2-2-3', 'earthworm-identified', 'Name the organism shown above.', [point('Earthworm', 3)], worm, node='1-4'), 'q10ci')
    figured(add('q10cii', 'Q10(c)(ii)', '2-2-3', 'earthworm-benefits', 'Mention two ways in which the above organism benefits the soil.',
                [menu('Improve drainage|improve aeration|mix soil layers|improve fertility or add nutrients|improve structure|improve texture|decompose organic matter|create humus', [3, 3],
                      'Any two, 3 marks each (2 x 3m).')], worm, node='1-4'), 'q10cii')
    figured(add('q10ciii', 'Q10(c)(iii)', '2-2-3', 'earthworm-count', 'Describe an experiment to estimate the number of these organisms in the soil.',
                [menu('Mark out area to be sampled|quadrat|random|how random|remove vegetation|apply potassium permanganate or washing up liquid or soapy solution|suitable time|count worms|repeat|average|multiply (average) no. of earthworms × area sampled',
                      [3] * 4, 'Any four, 3 marks each (4 x 3m). [Award marks if points are shown on a labelled diagram]')], worm, node='1-4|0-1'), 'q10ciii')
    # Question 11 ------------------------------------------------------------
    stomach = 'The ruminant stomach is shown in the diagram below.'
    add('q11ai', 'Q11(a)(i)', '4-1', 'ruminant-and-monogastric-species',
        'The cow has a ruminant stomach. Name: 1. one other livestock species that has this type of stomach and 2. one livestock species that does not have this type of stomach.',
        [point('1. Sheep/ goat/ deer', 4), point('2. Pig/ horse/ poultry', 4)], node='3-0')
    figured(add('q11aii', 'Q11(a)(ii)', '4-1', 'ruminant-stomach-chambers', 'Name the chambers of the stomach labelled B, C and D.',
                [point('B = Reticulum', 4, '3 × 4m.'), point('C = Omasum', 4), point('D = Abomasum', 4)], stomach, node='3-0'), 'q11aii')
    figured(add('q11aiii', 'Q11(a)(iii)', '4-1', 'true-stomach-chamber', 'Which chamber of the ruminant stomach most closely resembles the monogastric stomach?',
                [point('Abomasum/ D', 4)], stomach, node='3-0'), 'q11aiii')
    add('q11bi', 'Q11(b)(i)', '4-1', 'grass-constituent-digested', 'Name the main constituent of grass that is digested in the ruminant stomach.', [point('Cellulose or fibre', 4)], node='3-0')
    figured(add('q11bii', 'Q11(b)(ii)', '4-1', 'regurgitation-benefit', 'Food is regurgitated from chamber B. How does this benefit the animal?',
                [menu('Further mechanical digestion|softens food|increases surface area', [4], 'Any one, 4m.')], stomach, node='3-0'), 'q11bii')
    figured(add('q11biii', 'Q11(b)(iii)', '4-1', 'chamber-c-role', 'What happens to the food in chamber C?',
                [menu('Food is squeezed or dried|water removed|water re-absorbed (into rumen)', [4], 'Any one, 4m.')], stomach, node='3-0'), 'q11biii')
    figured(add('q11biv', 'Q11(b)(iv)', '4-1', 'after-part-d', 'Precisely which part of the digestive system does food enter when it leaves part D?',
                [menu('Duodenum|small intestine', [4], 'Any one, 4m.')], stomach, node='3-0'), 'q11biv')
    add('q11ci', 'Q11(c)(i)', '4-3-2', 'calf-diet-twelve-weeks', 'Describe how the diet of the calf is changed over the first twelve weeks of life.',
        [menu('Colostrum|(whole) milk|milk replacer|concentrates or meals|hay|silage|grass', [4] * 4, 'Any four, 4 marks each (4 × 4m).')], node='3-4')
    add('q11cii', 'Q11(c)(ii)', '4-3-3', 'bloat-cause', 'Bloat is a common disorder in cattle. What causes bloat?',
        [menu('Build-up of gas|inability to belch|high clover content in sward', [4], 'Any one, 4m.')], node='3-5')
    # Question 12 ------------------------------------------------------------
    add('q12ai', 'Q12(a)(i)', '3-1', 'plant-cell-diagram', 'Draw a simple diagram of a plant cell as seen under a light microscope. Label any three parts, other than chromosomes.',
        [point('Diagram', None, 'Diagram: 4m, 2m, 0m. [Award 4 marks if diagram has the correct shape, a nucleus and two boundaries] [Award 2 marks if diagram has incorrect shape or has one boundary only or has no nucleus]', kind='criterion'),
         point('Cell wall/ cell membrane/ nucleus/ cytoplasm/ (large) vacuole/ chloroplasts', None, 'Labels: any three, 4 marks each (3 × 4m).')],
        marks=16, tariff={'kind': 'questionTotal', 'notation': '(4m, 2m, 0m) + 3 × 4m'}, node='2-0')
    add('q12aii', 'Q12(a)(ii)', '4-1', 'chromosome-location', 'Where in the cell are the chromosomes found?', [point('Nucleus', 4)], node='3-6')
    add('q12aiii', 'Q12(a)(iii)', '4-1', 'mitosis', 'Name the process by which an animal or plant cell divides into two identical cells.', [point('Mitosis', 4)], node='3-6')
    wheat = ('In wheat, the allele for red kernel (R) is dominant over the allele for white kernel (r). A wheat plant, homozygous for red kernel (RR), is crossed with a plant homozygous for white kernel (rr). '
             'Copy the following into your answer book and complete the spaces. Genotypes of original parents (RR) × (rr).')
    add('q12bi', 'Q12(b)(i)', '4-1', 'red-kernel-gametes', 'Complete: (i) Possible gametes ○ × ○', [point('Gametes — R', 4, '2 × 4m.'), point('Gametes — r', 4)], wheat, node='3-6')
    add('q12bii', 'Q12(b)(ii)', '4-1', 'red-kernel-f1-genotype', 'Complete: (ii) F1 genotype ( )', [point('F1 genotypes — Rr', 4)], wheat, node='3-6')
    add('q12biii', 'Q12(b)(iii)', '4-1', 'red-kernel-f1-phenotype', 'Complete: (iii) F1 phenotype ___', [point('F1 phenotype — Red', 4)], wheat, node='3-6')
    add('q12c', 'Q12(c)', '4-1', 'red-kernel-test-cross',
        'In your answer book, show a cross between a homozygous recessive plant and an F1 plant from the above cross. Show the following in your cross (Homozygous recessive; F1 from above): '
        '(i) Genotypes of parents ( ) × ( ) (ii) Possible gametes ○ × ○ ○ (iii) Genotypes of offspring ( ) ( ) (iv) Phenotypes of offspring ___ ___',
        [point('(i) Genotypes of parents (homozygous recessive × F1) — rr × Rr', 4, '2 × 2m.'),
         point('(ii) Possible gametes — r × R r', 6, '3 × 2m.'),
         point('(iii) Genotypes of offspring — Rr rr', 4, '2 × 2m. [Award marks for genotypes only if gametes correct in second line]'),
         point('(iv) Phenotypes of offspring — Red White', 6, '2 × 3m. [Award marks for phenotypes only if they match genotypes in third line]')],
        'In wheat, the allele for red kernel (R) is dominant over the allele for white kernel (r). A wheat plant, homozygous for red kernel (RR), is crossed with a plant homozygous for white kernel (rr).',
        node='3-6')
    # Question 13 ------------------------------------------------------------
    two = 'Answer any two of the parts (a), (b), (c), (d).'
    add('q13ai', 'Q13(a)(i)', '4-1', 'ewe-gestation', 'State the length in days of the gestation period in ewes.', [point('145 -155 days', 2)], two, node='3-0')
    add('q13aii', 'Q13(a)(ii)', '4-3-2', 'housing-at-lambing', 'Give any three reasons for housing sheep at lambing time.',
        [menu('Facilitates supervision|easier feeding|warmer|prevents hypothermia or chill|avoids predation or safer|prevents poaching|reduces mortality|more spring grass', [3] * 3, 'Any three, 3 marks each (3 × 3m).')],
        two, node='3-4')
    add('q13aiii', 'Q13(a)(iii)', '4-3-2', 'sheep-winter-housing', 'List three features of winter housing for sheep.',
        [menu('Good ventilation|no draughts|suitable floor type or named example|hygiene|dry (floor)|fresh water supply|adequate feeding space|suitable feeding system (e.g. barrier)|adequate floor space|adequate space at feeding trough or at barrier|warm',
              [3] * 3, 'Any three, 3 marks each (3 × 3m).')], two, node='3-4')
    add('q13aiv', 'Q13(a)(iv)', '4-3-3', 'lamp-and-fostering-crate', 'Describe the use of the following at lambing time: 1. The infra-red lamp 2. The fostering crate.',
        [menu('Warms young lambs|warms weak lambs|prevents hypothermia or chill', [3, 2], 'Infra- red lamp: any two, 3m + 2m.'),
         menu('To foster a lamb (from a multiple birth)|onto ewe with one, or no, lamb|restrains ewe|prevents ewe rejecting adopted lamb', [3, 2], 'Fostering crate: any two, 3m + 2m.')], two, node='3-5')
    add('q13bi', 'Q13(b)(i)', '3-2', 'potato-varieties', 'Name one variety of each of the following categories of potato: 1. First early potatoes 2. Second early potatoes 3. Maincrop potatoes.',
        [menu('Home Guard|Epicure', [3], 'First early: any one, 3m.'), menu('British Queen|Maris Piper', [3], 'Second early: any one, 3m.'),
         menu('Kerr Pinks|Rooster|Golden Wonder|Records', [3], 'Main crop: any one, 3m.')], two, node='2-1|2-3')
    add('q13bii', 'Q13(b)(ii)', '3-3-1', 'donegal-seed-potatoes', 'Explain why seed potatoes are mainly grown in Co. Donegal.',
        [menu('Windy weather|aphid free|prevents viral infection|isolation|reduces spread of diseases', [3] * 3, 'Any three, 3 marks each (3 × 3m).')], two, node='2-3|2-4')
    add('q13biii', 'Q13(b)(iii)', '3-3-2', 'earthing-up-reasons', 'Give two reasons for earthing-up of potatoes.',
        [menu('Prevents exposure to light|prevents greening|controls weeds|prevents blight spores reaching tubers|increases yield|supports plant|reduces frost damage', [3, 3], 'Any two, 3 marks each (2 × 3m).')],
        two, node='2-4')
    add('q13biv', 'Q13(b)(iv)', '3-3-3', 'potato-storage-conditions', 'State two conditions needed for the storage of harvested potatoes.',
        [menu('Good ventilation|dry|frost-proof|easy access|high humidity|hygiene|free from vermin or diseases|cold|dark|forced ventilation if stacks more than 1.8m', [3, 3], 'Any two, 3 marks each (2 × 3m).')],
        two, node='2-5')
    milk = two + ' The table below shows an average composition of cow’s milk.'
    figured(add('q13ci', 'Q13(c)(i)', '4-3-2', 'milk-constituents-a-b', 'Identify A and B from the table.', [point('A = Water', 3), point('B = Protein', 3)], milk, node='3-4'), 'q13ci')
    figured(add('q13cii', 'Q13(c)(ii)', '4-3-2', 'milk-fat-factors', 'A number of factors affect fat content in milk. List any three of these factors.',
                [menu('Breed|age|feed quantity|feed type|milking interval|stage of milking|stage of lactation|disease|individuality within breed', [3] * 3, 'Any three, 3 marks each (3 × 3m).')],
                milk, node='3-4'), 'q13cii')
    figured(add('q13ciii', 'Q13(c)(iii)', '4-3-2', 'milk-quality-tests',
                'To ensure milk is of good quality, it is tested in a number of ways. List any three of these tests, other than tests for fat or protein content.',
                [menu('Total bacterial count or TBC|somatic cell count or SCC|temperature|water content|antibiotic content|sediment|thermoduric', [3] * 3, 'Any three, 3 marks each (3 × 3m).')],
                milk, node='3-4|0-1'), 'q13ciii')
    figured(add('q13civ', 'Q13(c)(iv)', '4-3-2', 'milking-hygiene', 'Explain any two management practices to ensure good hygiene at milking.',
                [menu('Clean holding area|milker hygiene|parlour hygiene|wash or wipe udder|strip cup|teat dip|filter|plate cooler|wash equipment regularly|clean bulk tank|cool milk to 4 °C or less in bulk tank|fly screens',
                      [3, 3], 'Any two, 3 marks each (2 × 3m).')], milk, node='3-4'), 'q13civ')
    pigs = two + ' In pig production, the sow is moved to the farrowing house to have her bonhams (piglets).'
    for key, ref, topic, concept, question, rows, node in [
            ('q13di', 'Q13(d)(i)', '4-3-2', 'farrowing-house-temperature', 'What is the temperature in the farrowing house?', [point('20 °C', 3)], '3-4'),
            ('q13dii', 'Q13(d)(ii)', '4-3-1', 'pig-unit-parts', 'Name two other parts of a pig production unit.',
             [menu('Dry sow house|weaner house|fattener house', [3, 3], 'Any two, 3 marks each (2 × 3m).')], '3-3'),
            ('q13diii', 'Q13(d)(iii)', '4-3-2', 'farrowing-crate-use', 'Explain the use of the farrowing crate.',
             [menu('Allows sow to suckle bonhams|prevents crushing or death|prevents sow eating bonhams|allows bonhams access to creep', [3, 3], 'Any two, 3 marks each (2 × 3m).')], '3-4'),
            ('q13div', 'Q13(d)(iv)', '4-3-3', 'newborn-bonham-practices', 'Describe two practices carried out on newly born bonhams.',
             [menu('Teeth clipping|tail docking|iron injection|ears notched|ensure bonhams suck sow|navel dip', [3, 3], 'Any two, 3 marks each (2 × 3m).')], '3-5'),
            ('q13dv', 'Q13(d)(v)', '4-3-2', 'bonham-weaning-age', 'At what age are bonhams normally weaned?', [point('28 - 35 days/ 4 -5 weeks', 3)], '3-4'),
            ('q13dvi', 'Q13(d)(vi)', '4-3-2', 'food-conversion-ratio', 'Food conversion ratio (FCR) is a very important consideration in pig production. Explain the term FCR.',
             [menu(['Ratio of food consumed', 'to liveweight gained'], [3, 3], '2 × 3m.')], '3-4')]:
        add(key, ref, topic, concept, question, rows, pigs, node=node)
    assert len(p.tasks) == 63, len(p.tasks)
    return p


def reviewed_tasks():
    p = build()
    return p.cards, p.tasks


def paper_review():
    return build().review('63 base tasks, one card each. Section One is one task per question, each row carrying its own marks; Q4\'s four cereals are answer routes. '
                          'Section Two parts are priced on their own; the Q12(c) cross is one task because its marks are tied line to line. '
                          'Q8(c) dry-matter methods and Q10(b)(ii) soil-texture methods are answer routes.')
