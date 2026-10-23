"""2020 Ordinary: every task authored from the SEC paper and marking scheme (no cards existed).

All 12 paper pages and 17 scheme pages were inspected and the independent census transcribed
before authoring: 52 base tasks, one card each. Where the scheme prices several parts with one
shared scale (Q2 "4 + 8(2)", Q5, Q6, Q11(c), Q12(a)-(c), Q13(a)-(c)) the scale's span is the
task: the first correct answers earn the higher award whichever part they answer, so no part
has a mark of its own and the card states the scale (orderedSplit) rather than inventing one.
Method routes (Q1(b), Q8(c), Q9(a)(iii)) and the winter/spring barley choice (Q13(b)) are
answer routes on one card. Answers are the scheme's words.
"""
from agricultural_science_legacy import Paper, P, point, menu, closed, routes

FILE = 'LC024GLP000EV.pdf'
HASHES = {'exampapers': 'ad07041e0062736f05423d160ee9bd758976c40ef0911391cb78d06da487f247',
          'markingschemes': 'e54816cb1236808d572ec878c58e031ab2e533f9d8c4916b3d0fdc45cea99d8e'}
SELECTIONS = {
    '35e2b9a6b59ead9f': ('exam-selection', 'Section One: six of seven independent 20-mark questions; every question is retained.'),
    '9b59fe0e78ff8fc9': ('open', 'Q1(c): a reason for any one step of the candidate’s own method; the scheme tabulates a reason for every step (a marking menu).'),
    'bdb5cd761b56dd4c': ('exam-selection', 'Section Two: three of six independent 60-mark questions; every question is retained.'),
    'e2a8512e79d64f52': ('open', 'Q8(b)(i): a reason for any one of the candidate’s four hay-making steps; the scheme tabulates a reason for each step.'),
    'e17a2b8e8a420b32': ('closed', 'Q9(b)(ii): the function of any one of nitrogen, phosphorus or potassium. One card lists all three nutrients, claim limit one.'),
    '9c150159ed613827': ('open', 'Q11(a)(ii): why any one of the candidate’s own two breeds suits dairying; the scheme gives a suitability for each breed (a marking menu).'),
    'f8917d2fa96ee777': ('independent-task-selection', 'Q13: two of four independently priced 30-mark parts; all four are retained.'),
}
SUPPLEMENTARY = [
    (2, 'Using any suitable method', 'closed', 'Q1(b): the scheme answers by the sieve, feel or sedimentation method, kept as answer routes on one card.'),
    (7, 'Describe a simple on‐site test', 'closed', 'Q8(c): the scheme answers for six tests (colour, smell, squeeze, pH, taste, feel), kept as answer routes on one card.'),
    (8, 'Describe how you would find the pH of a soil sample', 'closed', 'Q9(a)(iii): the scheme answers by universal indicator or by pH meter, kept as answer routes on one card.'),
    (12, 'Describe winter barley or spring barley', 'closed', 'Q13(b)(i): winter or spring barley, kept as answer routes on the one Q13(b) card.'),
]
ATLAS = {
    'Q1': 'soil-science|scientific-practices-experiments-investigations', 'Q2': 'animal-production|animal-physiology',
    'Q3': 'plant-physiology|animal-physiology|crop-production|animal-diseases|soil-science', 'Q4': 'crop-production|animal-production',
    'Q5': 'fertilisers-pollution-the-environment', 'Q6': 'animal-physiology',
    'Q7(a)': 'animal-diseases', 'Q7(b)': 'animal-diseases', 'Q7(c)': 'crop-production', 'Q7(d)': 'soil-science',
    'Q7(e)': 'fertilisers-pollution-the-environment', 'Q8': 'grassland',
    'Q9(a)': 'soil-science', 'Q9(b)': 'fertilisers-pollution-the-environment', 'Q9(c)': 'fertilisers-pollution-the-environment',
    'Q9(c)(iii)': 'fertilisers-pollution-the-environment|health-safety',
    'Q10': 'genetics', 'Q10(a)(ii)': 'genetics|animal-physiology', 'Q11': 'animal-production',
    'Q12(a)': 'plant-physiology|scientific-practices-experiments-investigations', 'Q12(b)': 'animal-physiology', 'Q12(c)': 'plant-physiology',
    'Q13(a)': 'soil-science', 'Q13(b)': 'crop-production', 'Q13(c)': 'animal-production',
    'Q13(d)': 'animal-production', 'Q13(d)(ii)': 'animal-production|scientific-practices-experiments-investigations',
}
REGIONS = {
    # Drafted by regions.py; Q9(b) paper crops stop short of the fertiliser-bag photograph (nothing
    # in either part depends on it) and Q13 paper crops start inside the page's blue border.
    'Q1(a)': (P((2, 0.302, 0.528)), P((3, 0.126, 0.204))),
    'Q1(b)': (P((2, 0.302, 0.336), (2, 0.528, 0.739)), P((3, 0.126, 0.153), (3, 0.204, 0.514))),
    'Q1(c)': (P((2, 0.302, 0.336), (2, 0.739, 0.860)), P((3, 0.126, 0.153), (3, 0.514, 0.877), (4, 0.063, 0.365))),
    'Q2': (P((3, 0.067, 0.447)), P((4, 0.365, 0.668))),
    'Q3': (P((3, 0.447, 0.869)), P((4, 0.668, 0.870))),
    'Q4': (P((4, 0.067, 0.880)), P((5, 0.046, 0.265))),
    'Q5': (P((5, 0.067, 0.533)), P((5, 0.265, 0.681))),
    'Q6': (P((5, 0.533, 0.911)), P((6, 0.064, 0.351))),
    'Q7(a)': (P((6, 0.067, 0.261)), P((6, 0.351, 0.473))),
    'Q7(b)': (P((6, 0.067, 0.134), (6, 0.261, 0.389)), P((6, 0.351, 0.412), (6, 0.473, 0.522))),
    'Q7(c)': (P((6, 0.067, 0.134), (6, 0.389, 0.516)), P((6, 0.351, 0.412), (6, 0.522, 0.587))),
    'Q7(d)': (P((6, 0.067, 0.134), (6, 0.516, 0.644)), P((6, 0.351, 0.412), (6, 0.587, 0.648))),
    'Q7(e)': (P((6, 0.067, 0.134), (6, 0.644, 0.761)), P((6, 0.351, 0.412), (6, 0.648, 0.744))),
    'Q8(a)(i)': (P((7, 0.262, 0.334)), P((7, 0.092, 0.263))),
    'Q8(a)(ii)': (P((7, 0.262, 0.299), (7, 0.334, 0.386)), P((7, 0.092, 0.124), (7, 0.263, 0.507))),
    'Q8(b)(i)': (P((7, 0.262, 0.299), (7, 0.386, 0.473)), P((7, 0.092, 0.124), (7, 0.507, 0.886))),
    'Q8(b)(ii)': (P((7, 0.262, 0.299), (7, 0.386, 0.421), (7, 0.473, 0.680)), P((7, 0.092, 0.124), (8, 0.046, 0.289))),
    'Q8(c)': (P((7, 0.262, 0.299), (7, 0.680, 0.738)), P((7, 0.092, 0.124), (8, 0.289, 0.574))),
    'Q9(a)(i)': (P((8, 0.067, 0.194)), P((9, 0.064, 0.137))),
    'Q9(a)(ii)': (P((8, 0.067, 0.107), (8, 0.194, 0.229)), P((9, 0.064, 0.085), (9, 0.137, 0.224))),
    'Q9(a)(iii)': (P((8, 0.067, 0.107), (8, 0.229, 0.281)), P((9, 0.064, 0.085), (9, 0.224, 0.397))),
    'Q9(b)(i)': (P((8, 0.067, 0.107), (8, 0.281, 0.307, 0, 0.70), (8, 0.316, 0.368, 0, 0.70)), P((9, 0.064, 0.085), (9, 0.398, 0.502))),
    'Q9(b)(ii)': (P((8, 0.067, 0.107), (8, 0.281, 0.307, 0, 0.70), (8, 0.368, 0.455, 0, 0.70)), P((9, 0.064, 0.085), (9, 0.502, 0.717))),
    'Q9(c)(i)': (P((8, 0.067, 0.107), (8, 0.455, 0.525)), P((9, 0.064, 0.085), (10, 0.046, 0.186))),
    'Q9(c)(ii)': (P((8, 0.067, 0.107), (8, 0.455, 0.490), (8, 0.525, 0.577)), P((9, 0.064, 0.085), (10, 0.186, 0.485))),
    'Q9(c)(iii)': (P((8, 0.067, 0.107), (8, 0.455, 0.490), (8, 0.577, 0.634)), P((9, 0.064, 0.085), (10, 0.485, 0.543))),
    'Q10(a)(i)': (P((9, 0.067, 0.174)), P((11, 0.064, 0.144))),
    'Q10(a)(ii)': (P((9, 0.067, 0.139), (9, 0.174, 0.208)), P((11, 0.064, 0.092), (11, 0.144, 0.197))),
    'Q10(a)(iii)': (P((9, 0.067, 0.139), (9, 0.208, 0.261)), P((11, 0.064, 0.092), (11, 0.197, 0.248))),
    'Q10(b)': (P((9, 0.067, 0.105), (9, 0.261, 0.556)), P((11, 0.064, 0.092), (11, 0.248, 0.331))),
    'Q10(c)': (P((9, 0.067, 0.105), (9, 0.556, 0.782)), P((11, 0.064, 0.092), (11, 0.331, 0.432))),
    'Q10(d)(i)': (P((9, 0.067, 0.105), (9, 0.782, 0.852)), P((11, 0.064, 0.092), (11, 0.432, 0.502))),
    'Q10(d)(ii)': (P((9, 0.067, 0.105), (9, 0.782, 0.817), (9, 0.852, 0.873)), P((11, 0.064, 0.092), (11, 0.502, 0.564))),
    'Q11(a)(i)': (P((10, 0.067, 0.142)), P((12, 0.064, 0.179))),
    'Q11(a)(ii)': (P((10, 0.067, 0.107), (10, 0.142, 0.177)), P((12, 0.064, 0.092), (12, 0.179, 0.427))),
    'Q11(a)(iii)': (P((10, 0.067, 0.107), (10, 0.177, 0.264)), P((12, 0.064, 0.092), (12, 0.427, 0.513))),
    'Q11(b)(i)': (P((10, 0.067, 0.107), (10, 0.264, 0.333)), P((12, 0.064, 0.092), (12, 0.513, 0.615))),
    'Q11(b)(ii)': (P((10, 0.067, 0.107), (10, 0.264, 0.299), (10, 0.333, 0.368)), P((12, 0.064, 0.092), (12, 0.615, 0.667))),
    'Q11(b)(iii)': (P((10, 0.067, 0.107), (10, 0.264, 0.299), (10, 0.368, 0.403)), P((12, 0.064, 0.092), (12, 0.667, 0.720))),
    'Q11(b)(iv)': (P((10, 0.067, 0.107), (10, 0.264, 0.299), (10, 0.403, 0.473)), P((12, 0.064, 0.092), (12, 0.720, 0.781))),
    'Q11(c)': (P((10, 0.067, 0.107), (10, 0.473, 0.599)), P((12, 0.064, 0.092), (13, 0.046, 0.282))),
    'Q12(a)': (P((11, 0.067, 0.385)), P((14, 0.064, 0.358))),
    'Q12(b)': (P((11, 0.067, 0.107), (11, 0.385, 0.629)), P((14, 0.064, 0.084), (14, 0.358, 0.637))),
    'Q12(c)': (P((11, 0.067, 0.107), (11, 0.629, 0.860)), P((14, 0.064, 0.084), (14, 0.637, 0.906))),
    'Q13(a)': (P((12, 0.067, 0.335, 0.06, 1)), P((15, 0.064, 0.441))),
    'Q13(b)': (P((12, 0.067, 0.144, 0.06, 1), (12, 0.335, 0.526, 0.06, 1)), P((15, 0.064, 0.092), (15, 0.441, 0.775))),
    'Q13(c)': (P((12, 0.067, 0.144, 0.06, 1), (12, 0.526, 0.752, 0.06, 1)), P((15, 0.064, 0.092), (16, 0.046, 0.328))),
    'Q13(d)(i)': (P((12, 0.067, 0.144, 0.06, 1), (12, 0.752, 0.787, 0.06, 1)), P((15, 0.064, 0.092), (16, 0.328, 0.416))),
    'Q13(d)(ii)': (P((12, 0.067, 0.144, 0.06, 1), (12, 0.787, 0.822, 0.06, 1)), P((15, 0.064, 0.092), (16, 0.416, 0.515))),
    'Q13(d)(iii)': (P((12, 0.067, 0.144, 0.06, 1), (12, 0.822, 0.857, 0.06, 1)), P((15, 0.064, 0.092), (16, 0.515, 0.774))),
    'Q13(d)(iv)': (P((12, 0.067, 0.144, 0.06, 1), (12, 0.857, 0.891, 0.06, 1)), P((15, 0.064, 0.092), (16, 0.774, 0.844))),
    'Q13(d)(v)': (P((12, 0.067, 0.144, 0.06, 1), (12, 0.891, 0.917, 0.06, 1)), P((15, 0.064, 0.092), (16, 0.844, 0.909))),
}
FIGURES = {
    'q1a': ('agsci-2020-ol-paper-soil-sieves', None),
    'q4': ('agsci-2020-ol-paper-farm-machinery', [('A', 'Roller (the completed example)', False), ('B', 'Slurry agitator', True), ('C', 'Bale grabber', True),
                                                   ('D', '(Reversible) plough', True), ('E', 'Round feeder', True), ('F', 'Muck (or dung) spreader', True)]),
    'q6': ('agsci-2020-ol-paper-ruminant-stomach', [('A', 'Oesophagus (given on the paper)', False), ('B', 'Rumen', True), ('C', 'Reticulum', True),
                                                    ('D', 'Omasum', True), ('E', 'Abomasum', True)]),
    'q12b': ('agsci-2020-ol-paper-excretory-system', [('A', 'Kidney', True), ('B', 'Ureter', True), ('C', 'Bladder', True)]),
    'q12c': ('agsci-2020-ol-paper-flower', [('A', 'Petal', True), ('B', 'Anther (the scheme allows stamen)', True), ('C', 'Ovule', True),
                                            ('D', 'Stigma (the scheme allows carpel)', True), ('E', 'The part that develops into the fruit', True)]),
}
SHARED = 'Shared scale {}: the first correct answers earn the higher award, whichever part they answer, so no part carries a mark of its own.'


def split(text, marks=None, note=None):
    """A row of an orderedSplit card: the scheme prices the scale, not the row."""
    return point(text, None, note)


def figured(card, key):
    figure, labels = FIGURES[key]
    card['figureKey'] = figure
    if labels:
        card['labelKey'] = [dict(letter=l, meaning=m, askedInThisQuestion=a) for l, m, a in labels]
    return card


def build():
    p = Paper(2020, 'ordinary', FILE, HASHES, REGIONS, ATLAS, 12, 17, SELECTIONS, SUPPLEMENTARY,
              section=lambda ref: 'A' if int(ref.split('(')[0][1:]) <= 7 else 'B')
    add = p.add
    # Question 1 -------------------------------------------------------------
    figured(add('q1a', 'Q1(a)', '2-2-2', 'soil-texture-meaning', 'What is meant by the term soil texture?',
                [point('The % sand, silt and clay (in a soil)', 4)],
                'Soil sieves, as shown, are used in the laboratory to find the texture of a soil sample.', node='1-3'), 'q1a')
    methods = [('sieve', 'Sieve method', 'Dry soil|crush soil|weigh soil sample|arrange sieves so that sieve with largest mesh size is on top|place soil in top sieve and cover|shake sieves|weigh amount of soil in each sieve|refer to soil textural triangle'),
               ('feel', 'Feel method', 'Rub or feel (dry) soil (between thumb and finger)|note grittiness or smoothness|repeat with wet soil|roll wet soil into a ball or a thread or bend into rings if possible|compare (observations) to flow chart'),
               ('sedimentation', 'Sedimentation method', 'Place soil sample in beaker of water and stir|add soil- water mixture to a graduated cylinder and add more water|shake the soil- water mixture vigorously|allow soil to settle|measure the depth of each soil component|refer to soil textural triangle')]
    rows, variants = routes([(slug, label, [menu(steps, [3] * 4, f'{label}: any four steps, 3 marks each (4(3)).')]) for slug, label, steps in methods])
    add('q1b', 'Q1(b)', '2-2-2', 'finding-soil-texture', 'Using any suitable method, outline the steps you would take to find the texture of a soil sample in the laboratory.',
        rows, selection=closed(1, [label for _, label, _ in methods]), node='1-3|0-1', extra={'answerVariants': variants})
    reasons = ['Dry soil: Allows soil to pass through sieves', 'Crush soil: Breaks up lumps of soil',
               'Weigh soil: To find the mass of soil or to allow calculation of % of each soil component',
               'Sieves in correct order: To facilitate separation of soil particles', 'Shake sieves: To move soil particles through sieves',
               'Weigh soil in each sieve: To calculate mass of each soil component', 'Refer to soil textural triangle: To determine texture of soil',
               'Rub soil between fingers: To determine feel of soil', 'Note grittiness of soil: To assess sand content in soil',
               'Wet soil: To allow soil to be rolled into a ball or thread', 'Roll soil into a ball or thread: To assess clay and/or silt content in soil',
               'Compare to flow chart: To determine texture of soil', 'Stir soil and water in beaker: To break up lumps of soil',
               'Soil and water in a graduated cylinder: To allow soil- water mixture to be shaken or to allow layers of each particle type to be measured',
               'Shake soil-water mixture vigorously: To separate soil into its different components',
               'Allow soil to settle: To allow sand, silt and clay particles to settle into different layers.',
               'Measure depth of each layer: To calculate % sand, silt and clay']
    add('q1c', 'Q1(c)', '2-2-2', 'soil-texture-step-reason', 'Give a reason behind any one of the steps in (b).',
        [menu(reasons, [4], 'A reason for any one step of your method, 4 marks. The scheme tabulates a reason for each step of the sieve, feel and sedimentation methods; each method ends "Refer to soil textural triangle: To determine texture of soil".')],
        'Using any suitable method, outline the steps you would take to find the texture of a soil sample in the laboratory.', node='1-3|0-1')
    # Question 2: one shared scale over (a) and (b) ---------------------------
    add('q2', 'Q2', '4-3-3', 'gestation-birth-weight-colostrum',
        '(a) Complete the table for each of the named farm animals. Table columns: Animal | Length of gestation (pregnancy) | Birth weight of offspring (kg); rows: Pig, Sheep, Cow. (b) (i) What is colostrum? (ii) Give two reasons why colostrum is important.',
        [split('Pig, length of gestation — 3 months, 3weeks, 3 days (or 110 – 120 days)', note=SHARED.format('4 + 8(2)') + ' Nine answers: six table cells, what colostrum is, and two reasons.'),
         split('Pig, birth weight — 1 – 1.5 kg'), split('Sheep, length of gestation — 5 months (or 145 – 155 days)'), split('Sheep, birth weight — 3 – 5 kg'),
         split('Cow, length of gestation — 9.5months (or 280 – 290 days)'), split('Cow, birth weight — 35 – 45 kg'),
         split('(b)(i) What colostrum is — First milk a young mammal (or named mammal) gets from its mother'),
         split('(b)(ii) Why colostrum is important — Rich in nutrients (or named nutrient)/ highly digestible/ rich in antibodies/ provides immunity/ warming effect/ laxative effect', note='Any two.')],
        marks=20, tariff={'kind': 'orderedSplit', 'notation': '4 + 8(2)'}, node='3-5|3-0')
    # Question 3 -------------------------------------------------------------
    statements = [('a', 'Stomata are pores found on the leaves of plants', 'T'), ('b', 'Pigs have a ruminant stomach', 'F'),
                  ('c', 'Malting barley is used in the production of alcohol', 'T'), ('d', 'Brucellosis in cattle is caused by bacteria', 'T'),
                  ('e', 'Clover plants can fix nitrogen', 'T'), ('f', 'Golden Wonder potatoes are a first early potato variety', 'F'),
                  ('g', 'Sandstone is an igneous rock type', 'F'), ('h', 'L.W.G. stands for lower weight gain', 'F'),
                  ('i', 'The right ventricle of the heart pumps blood around the body', 'F'), ('j', 'The crane fly larva is called a leatherjacket', 'T')]
    add('q3', 'Q3', '3-1', 'true-or-false-farm-science',
        'Indicate whether each of the following statements is true (T) or false (F) by drawing a circle around the correct answer in each case. Example: Incisor teeth are used to chew food — F. '
        '(a) Stomata are pores found on the leaves of plants. (b) Pigs are ruminant animals. (c) Malting barley is used in the production of alcohol. (d) Brucellosis in cattle is caused by bacteria. '
        '(e) Clover is a nitrogen-fixing plant. (f) Golden Wonders are a ‘first early’ variety of potatoes. (g) Sandstone is an igneous rock. (h) LWG stands for lower weight gain. '
        '(i) The right ventricle of the heart pumps blood around the body. (j) The larva of the crane fly is called a leatherjacket.',
        [menu([f'({k}) {s}: {a}' for k, s, a in statements], [2] * 10,
              'All ten statements, 2 marks each (10(2)). T = true, F = false; the scheme words each statement as shown.')],
        tariff={'kind': 'fixed', 'notation': '10(2)'}, node='2-0|3-0|1-0|3-5|2-1')
    # Question 4 -------------------------------------------------------------
    machines = [('B', 'Slurry agitator', 'To break hard crust or to mix the solids and liquids or to allow gases to escape or easier to spread'),
                ('C', 'Bale grabber', 'To transport bales (of hay) or to stack bales'),
                ('D', '(Reversible) plough', 'To turn the soil or to bury stubble or to bury weeds'),
                ('E', 'Round feeder', 'Feeding fodder to livestock'), ('F', 'Muck (or dung) spreader', 'To spread farmyard manure')]
    figured(add('q4', 'Q4', '2-3', 'farm-machinery-names-functions',
                'Name and state the function of each item of farm equipment and machinery shown below (B to F). Item A has been completed for you: Roller — To break soil clumps or to level soil or to increase seed contact with soil or to remove air pockets from soil.',
                [menu([name, use], [2, 2], f'{letter}: its name and its function, 2 + 2.' + (' 5(2 + 2) across items B to F.' if letter == 'B' else ''))
                 for letter, name, use in machines],
                tariff={'kind': 'fixed', 'notation': '5(2 + 2)'}, node='1-5|2-3|3-4'), 'q4')
    # Question 5: one shared scale over (a)-(c) -------------------------------
    effects = [('Slurry', 'Water pollution'), ('Silage effluent', 'Water pollution'), ('Plastic', 'Choking of livestock'),
               ('Pesticides', 'Can kill non-target species'), ('Herbicides', 'Can kill non-target species'), ('Waste oil', 'Water pollution'),
               ('Lead paint', 'Toxic to livestock'), ('Smoke', 'Air pollution'), ('Parlour washings', 'Water pollution'), ('Fertiliser run-off', 'Water pollution')]
    add('q5', 'Q5', '2-3', 'farm-pollution-and-carbon',
        '(a) State two sources of pollution on a farm. (b) Describe the harmful effects of each of the above sources of farm pollution. (c) Increasing levels of carbon dioxide gas (CO2) in the atmosphere contribute to global warming. State two farming practices that can lead to a reduction in carbon dioxide levels in the atmosphere.',
        [split('(a) Sources of pollution — Slurry/ silage effluent/ plastic/ pesticides/ herbicides/ waste oil/ lead paint/ smoke (e.g. gorse fires)/ parlour washings/ fertiliser run-off',
               note=SHARED.format('4(4) + 2(2)') + ' Six answers: two sources, the harmful effect of each, and two practices. Any two sources.')]
        + [split(f'(b) Harmful effect of {source.lower()} — {effect}', note='The harmful effect of each source you gave in (a), as the scheme tabulates it.' if source == 'Slurry' else None)
           for source, effect in effects]
        + [split('(c) Farming practices to reduce CO2 in atmosphere — Plant trees (or hedgerows)/ more efficient farm machinery or proper maintenance of farm machinery/ solar panels/ minimum till/ wind generated electricity/ reduction in number of livestock on farm/ organic farming', note='Any two.')],
        marks=20, tariff={'kind': 'orderedSplit', 'notation': '4(4) + 2(2)'}, node='1-6')
    # Question 6: one shared scale over (a) and (b) ---------------------------
    figured(add('q6', 'Q6', '4-1', 'ruminant-stomach-parts-functions',
                '(a) The diagram shows some parts of the ruminant digestive system. Part A is the oesophagus. Name the parts labelled B, C, D and E. '
                '(b) Match each of the labelled parts with its correct function (letter only in each case): Squeezes, and absorbs water; Pushes food back up into the mouth; Completes digestion of food; Contains bacteria and protozoans which digest cellulose.',
                [split('(a) B — Rumen', note=SHARED.format('2(4) + 6(2)') + ' Eight answers: four names and four letters.'),
                 split('(a) C — Reticulum'), split('(a) D — Omasum'), split('(a) E — Abomasum'),
                 split('(b) Squeezes, and absorbs water — D'), split('(b) Pushes food back up into the mouth — C'),
                 split('(b) Completes digestion of food — E'), split('(b) Contains bacteria and protozoans which digest cellulose — B')],
                marks=20, tariff={'kind': 'orderedSplit', 'notation': '2(4) + 6(2)'}), 'q6')
    # Question 7 -------------------------------------------------------------
    practice = 'State one reason for each of the following farm practices.'
    for key, ref, topic, concept, item, answer, node in [
            ('q7a', 'Q7(a)', '4-3-3', 'why-vaccinate', 'Vaccination of farm animals.', 'Prevents disease (or named disease) or stimulates antibody production or provides immunity', None),
            ('q7b', 'Q7(b)', '4-3-3', 'why-footbaths', 'Using footbaths on a sheep farm.', 'To prevent foot rot or to prevent foot infection or to prevent lameness', None),
            ('q7c', 'Q7(c)', '3-3-1', 'why-certified-seed-potatoes', 'Growing certified seed potatoes.', 'Free from diseases (or named disease) or free from viruses or true-to-type or higher yields or seed graded to uniform tuber size', None),
            ('q7d', 'Q7(d)', '2-3', 'why-subsoil', 'Subsoiling a soil.', 'To break up pans or improves drainage or loosens compacted soils or improves root penetration or improves aeration', None),
            ('q7e', 'Q7(e)', '2-3', 'why-maintain-hedgerows', 'Maintaining hedgerows.', 'Habitat for wildlife or natural boundaries or natural amenity or improved crop growth (on sheltered side) or reduce soil erosion or to keep animals warm or to protect crops or to increase soil temperature or sound barrier or replenish oxygen or reduce carbon dioxide or encourages biodiversity or for biosecurity', '1-6')]:
        add(key, ref, topic, concept, 'State one reason for the following farm practice: ' + item, [point(answer, 4, 'One reason, 4 marks (5(4) across the five practices).')], practice, node=node)
    # Question 8 -------------------------------------------------------------
    add('q8ai', 'Q8(a)(i)', '3-3-2', 'paddock-grazing-diagram', 'Draw a labelled diagram of a paddock grazing system.',
        [point('Means of access to paddock (e.g. roadway or pathway) and at least 10 paddocks', None, 'Drawing: 5, 3, 0.', kind='criterion'),
         point('(Permanent) roadway/ water(supply)/ fencing/paddocks showing re-growth or recovery/ indication of direction of movement of livestock/ number of paddocks labelled (e.g. 20-25 paddocks)', None, 'Labels: any two, 2 marks each (2(2)).')],
        marks=9, tariff={'kind': 'questionTotal', 'notation': 'D 5, 3, 0 + L 2(2)'}, node='2-6')
    add('q8aii', 'Q8(a)(ii)', '3-3-2', 'paddock-grazing-pros-cons', 'State two advantages and two disadvantages of paddock grazing.',
        [menu('Fresh grass each day|controlled grazing|21-day rotation|time for grass to recover|reduced incidence of parasitic worms|paddocks can be fertilised when animals move|more efficient use of grass (or less wastage or less trampling of grass)|livestock spend less time walking|palatable grass always available|grass more digestible|maximum production from animals (or higher milk yields or increased weight gain)|some paddocks can be closed off for silage (or hay)|low labour input (or easy to manage)',
              [3, 3], 'Advantages: any two, 3 marks each (2(3)).'),
         menu('Expensive to set up|paddock must have permanent water supply|fencing for each paddock|can be difficult to cut silage (or hay) if paddocks are small|poaching damage is possible (in certain weather conditions)',
              [3, 3], 'Disadvantages: any two, 3 marks each (2(3)).')], node='2-6')
    hay = 'Hay and silage are made on Irish farms.'
    steps = [('Close field in time (or for 10 weeks)', 'Adequate time for grass to grow or higher yield of hay'), ('Adequate fertiliser', 'Promotes good growth or higher yield of hay'),
             ('Use good quality grass varieties (or named grass variety e.g. PRG)', 'Hay of better quality or more digestible or easier to dry'),
             ('Control weeds', 'Hay of better quality or prevents poisoning (of livestock)'), ('Cut or mow grass in dry weather', 'Easier drying or lowers risk of weather damage'),
             ('Allow grass to wilt or dry', 'Lowers moisture content'), ('Ted (or turn or shake) grass', 'Faster drying or lets air through grass'),
             ('Rake (or gather) into rows', 'Easier to bale'), ('Allow hay to dry before baling', 'Prevents rotting of hay'),
             ('Bale hay', 'Easier to handle (or transport) or easier to store'), ('Store hay in (leak-proof) shed or undercover', 'Keeps hay dry or prevents rotting')]
    add('q8bi', 'Q8(b)(i)', '3-3-3', 'making-good-hay', 'Outline four steps involved in making good quality hay and explain why any one of those steps is important.',
        [menu([s for s, _ in steps], [3] * 4, 'Steps: any four, 3 marks each (4(3)).'),
         menu([f'{s}: {r}' for s, r in steps], [3], 'Why any one of your steps is important, 3 marks.')], hay, node='2-6|2-5')
    add('q8bii', 'Q8(b)(ii)', '3-3-3', 'silage-step-reasons',
        'The following steps are taken when making good quality silage. State one reason for each of the steps listed below: 1. Cutting the grass on a sunny day. 2. Allowing the cut grass to wilt. 3. Rolling or baling the cut grass. 4. Covering the grass in plastic.',
        [point('1. Cutting the grass on a sunny day — Higher concentration of sugars (or carbohydrates)', 3, 'One reason for each step, 3 marks each (4(3)).'),
         point('2. Allowing the cut grass to wilt — Increases dry matter content or less effluent', 3),
         point('3. Rolling or baling the cut grass — Creates anaerobic conditions (or eliminates oxygen)', 3),
         point('4. Covering the grass in plastic — Creates anaerobic conditions or prevents rotting', 3)], hay, node='2-6|2-5')
    tests = [('colour', 'Colour of silage', 'Yellow-green indicates high quality or dark green (or brown) indicates poor quality'),
             ('smell', 'Smell of silage', 'Sharp (or acidic) smell indicates high quality or putrid smell indicates poor quality'),
             ('squeeze', 'Squeeze silage (or dry matter or DM test)', 'Small amount of liquid produced from silage indicates high quality or large amount of liquid produced indicates poor quality'),
             ('ph', 'pH of silage', 'pH < 5 indicates high quality or pH > 5 indicates poor quality'),
             ('taste', 'Taste of silage', 'Sharp (or acidic) taste indicates high quality or sweet or sour taste indicates poor quality'),
             ('feel', 'Feel of silage', 'A firm texture indicates high quality or a slimy feel indicates poor quality')]
    rows, variants = routes([(slug, label, [point(f'Test — {label}', 4, 'Test 4 + result 4 + conclusion 4.'),
                                            point(f'Result — {outcome}', 4, 'A possible result of your test.'),
                                            point(f'Conclusion — {outcome}', 4, 'What the result means about the quality of the silage.')]) for slug, label, outcome in tests])
    add('q8c', 'Q8(c)', '3-3-3', 'silage-on-site-test',
        'Describe a simple on-site test that a farmer can carry out on silage. Give a possible result of this test and say what the result means about the quality of the silage.',
        rows, selection=closed(1, [label for _, label, _ in tests]), node='2-6|0-1', extra={'answerVariants': variants})
    # Question 9 -------------------------------------------------------------
    add('q9ai', 'Q9(a)(i)', '2-2-1', 'liming-element', 'Which chemical element in ground limestone is the most important in raising the soil pH?',
        [point('Calcium', 3, 'The scheme accepts the symbol.')], 'Farmers use ground limestone (CaCO3) to raise the pH of the soil.', node='1-2')
    add('q9aii', 'Q9(a)(ii)', '2-2-1', 'soil-acidification', 'State two ways in which a soil may become acidic.',
        [menu('Crop removal|leaching|(acid) rain|animal urine|addition of certain fertilisers|plant vegetation (e.g. pine needles)|addition of slurry or of farmyard manure', [3, 2],
              'Any two: the first correct earns 3 and the second 2 (3 + 2).')], node='1-2')
    common = 'Add soil to beaker (or suitable container)|add distilled water (or deionised water)|stir soil and water'
    rows, variants = routes([(slug, label, [menu(f'{common}|{rest}', [3] * 4, f'{label}: any four, 3 marks each (4(3)).')]) for slug, label, rest in [
        ('indicator', 'Universal indicator', 'filter mixture|add universal indicator solution (or indicator paper) to filtrate|compare colour with pH chart'),
        ('meter', 'pH meter', 'pH meter|insert electrode (of meter) into distilled water to check if meter reading accurately|insert electrode into soil-water mixture|read the pH')]])
    add('q9aiii', 'Q9(a)(iii)', '2-2-1', 'finding-soil-ph', 'Describe how you would find the pH of a soil sample.', rows,
        selection=closed(1, ['Universal indicator', 'pH meter']), node='1-2|0-1', extra={'answerVariants': variants})
    npk = '10-10-20 is a common compound fertiliser used on Irish farms.'
    add('q9bi', 'Q9(b)(i)', '2-3', 'npk-nutrients', 'Name the three principal plant nutrients in 10-10-20.',
        [point('Nitrogen', 4, '3(4). The scheme allows symbols.'), point('Phosphorus', 4), point('Potassium', 4)], npk, node='1-6')
    add('q9bii', 'Q9(b)(ii)', '2-3', 'npk-nutrient-function', 'State the function of any one of the plant nutrients in 10-10-20.',
        [menu(['Nitrogen: Formation of chlorophyll (or of green colour) or prevents chlorosis (or prevents yellowing) or protein formation or increases yield or promotes leafy growth',
               'Phosphorus: Cell division or energy transfer in cells or seed germination or promotes root growth or enhances seed formation',
               'Potassium: Protein formation or disease prevention or promotes healthy growth or promotes early ripening or enhances fruit quality'], [4],
              'Any one nutrient with a function, 4 marks.')], npk, selection=closed(1, ['Nitrogen', 'Phosphorus', 'Potassium']), node='1-6|2-0')
    waste = 'Farmyard manure (FYM) and slurry are two forms of farm animal waste.'
    add('q9ci', 'Q9(c)(i)', '2-3', 'storing-fym-and-slurry', 'State how each is stored on a farm.',
        [point('Farmyard manure: In a dungstead or on concrete or on in the open', 4), point('Slurry: In an underground slurry tank or in a (covered) over-ground slurry tank', 4)], waste, node='1-6')
    add('q9cii', 'Q9(c)(ii)', '2-3', 'fym-versus-slurry', 'State two differences between the composition of FYM and the composition of slurry.',
        [menu('Less water or More water|Contains straw or No straw|Less nitrogen or More nitrogen|More phosphorus or Less phosphorus|Solid or Liquid|Rich in organic matter or Low in organic matter', [4, 4],
              'Any two, 4 marks each (2(4)). Each difference reads FYM, then slurry.')], waste, node='1-6')
    add('q9ciii', 'Q9(c)(iii)', '1-5', 'slurry-agitation-safety', 'Slurry has to be agitated before it can be spread. State two precautions taken by farmers when agitating slurry.',
        [menu('Wear a mask|do not work alone|remove livestock from shed|open shed doors|agitate on windy day|agitate from outside', [4, 4], 'Any two, 4 marks each (2(4)).')], waste, node='0-4|1-6')
    # Question 10 ------------------------------------------------------------
    cells = 'There are 60 chromosomes in the somatic cells (body cells) of cattle.'
    add('q10ai', 'Q10(a)(i)', '4-1', 'chromosomes-in-gametes', 'How many chromosomes are in the gametes of cattle?', [point('30', 4)], cells, node='3-6')
    add('q10aii', 'Q10(a)(ii)', '4-1', 'female-gamete-organ', 'Name the organ in which the female gametes are produced in cattle.', [point('Ovary', 4)], cells)
    add('q10aiii', 'Q10(a)(iii)', '4-1', 'gamete-cell-division', 'Name the type of cell division that produces gametes.', [point('Meiosis', 4)], cells, node='3-6')
    maize = 'In maize the allele for green seedlings (G) is dominant over the allele for albino seedlings (g). A maize plant, homozygous for green (GG), was crossed with a maize plant homozygous for albino (gg).'
    add('q10b', 'Q10(b)', '4-1', 'monohybrid-maize-cross-1',
        'Copy and complete this cross. Parent phenotypes: Green × Albino. Parent genotypes: (GG) × (gg). Gametes: ( ) × ( ). Genotype of offspring: ( ). Phenotype of offspring: ____.',
        [point('Gametes: (G)', 4, 'Gametes 2(4), offspring genotype 4, offspring phenotype 4.'), point('Gametes: (g)', 4),
         point('Offspring genotype: (Gg)', 4), point('Offspring phenotype: Green', 4)], maize, node='3-6')
    add('q10c', 'Q10(c)', '4-1', 'monohybrid-maize-cross-2',
        'Two plants with the same genotype as the offspring above were crossed with each other. Copy and complete the following to give the possible genotypes and phenotypes from this cross. '
        'Plant genotypes: ( ) × ( ). Possible gametes: ( ) ( ) × ( ) ( ). Genotypes of offspring: ( ) ( ) ( ). Phenotypes of offspring: ____ ____.',
        [point('Parents’ genotypes — (Gg) × (Gg)', 6, '2(3): 3 for each parent\'s genotype.'),
         point('Possible gametes — (G) (g) × (G) (g)', 8, '4(2): 2 for each gamete.'),
         menu(['(GG)', '(Gg)', '(gg)'], [2, 2, 2], 'Offspring genotypes, 3(2).'),
         menu(['Green', 'Albino'], [2, 2], 'Offspring phenotypes, 2(2).')], maize, node='3-6')
    crossing = 'Cross breeding is commonly used in agriculture.'
    add('q10di', 'Q10(d)(i)', '4-3-2', 'cross-breeding-meaning', 'What is meant by the term cross breeding?',
        [point('The mating of two different breeds of the same species or crossing two different varieties of plants', 4)], crossing, node='3-6')
    add('q10dii', 'Q10(d)(ii)', '4-3-2', 'cross-breeding-advantage', 'State one advantage of a cross breeding system.',
        [point('Hybrid vigour or increased prolificacy or increased milk yield or better quality milk or increased disease resistance or increased yields', 4)], crossing, node='3-6')
    # Question 11 ------------------------------------------------------------
    add('q11ai', 'Q11(a)(i)', '4-2', 'dairy-breeds', 'Name two breeds of dairy cow.',
        [menu('Holstein (Friesian)|Jersey|Ayrshire|Montbeliarde|Norwegian Red|(British) Friesian|Kerry|Shorthorn', [4, 4], 'Any two, 4 marks each (2(4)). The scheme allows Shorthorn.')], node='3-1|3-3')
    add('q11aii', 'Q11(a)(ii)', '4-2', 'dairy-breed-suitability', 'State why any one of these breeds is suitable as a dairy breed.',
        [menu(['Holstein (Friesian): High milk yields', 'Jersey: High milk solids or low maintenance or easy calving', 'Ayrshire: High milk solids or easy calving or longevity',
               'Montbeliarde: Milk suitable for cheese making or good fertility or longevity or good resistance to mastitis',
               'Norwegian Red: Easy calving or high fertility or good (udder) health', '(British) Friesian: Dual-purpose or high milk yields',
               'Shorthorn: Dual-purpose or high milk yields', 'Kerry: Hardy or easy calving or docile'], [4], 'Any one of your two breeds with its suitability, 4 marks.')],
        'Name two breeds of dairy cow.', node='3-1|3-3')
    add('q11aiii', 'Q11(a)(iii)', '4-3-2', 'culling-dairy-cows', 'Cows are culled on dairy farms. State two reasons why dairy cows are culled.',
        [menu('Injury (or lameness or bad feet)|low milk yield|poor milk quality (or explained)|disease (or named disease)|fertility problems|calving difficulties|bad temperament|grading up|old age|poor conformation|poor BCS',
              [4, 4], 'Any two, 4 marks each (2(4)).')], node='3-4')
    heifers = 'A dairy enterprise needs replacement heifers.'
    add('q11bi', 'Q11(b)(i)', '4-3-2', 'replacement-heifer-traits', 'Name two desirable characteristics of replacement heifers.',
        [menu('Good conformation|healthy udder or good teat placement|good feet|clean shiny coat|disease-free or healthy (or one sign of good health explained)|good BCS (or in good condition)|bred from cow with high % milk solids|good temperament|bred from a sire with a high EBI',
              [4, 4], 'Any two, 4 marks each (2(4)).')], heifers, node='3-4')
    add('q11bii', 'Q11(b)(ii)', '4-3-2', 'heifer-first-calving-age', 'At what age should a heifer give birth to her first calf?', [point('22 - 26 months', 4)], heifers, node='3-4')
    add('q11biii', 'Q11(b)(iii)', '4-3-2', 'heifer-first-calving-weight', 'What is the target weight for a heifer when she gives birth to her first calf?', [point('500 – 550 kg', 4)], heifers, node='3-4')
    add('q11biv', 'Q11(b)(iv)', '4-3-3', 'signs-of-calving', 'State two signs that a farmer would notice in a heifer when she is about to give birth.',
        [menu('Restlessness|isolates herself|swollen vulva|mucus discharge from vulva|swollen udder|milk leaking from udder|pelvic ligaments not visible (or pins drop)', [4, 4],
              'Any two, 4 marks each (2(4)).')], heifers, node='3-5')
    add('q11c', 'Q11(c)', '4-3-2', 'body-condition-scoring',
        '(i) What is meant by the term body condition scoring? (ii) How is the body condition score of a cow assessed? (iii) What would cause a cow to have a low body condition score? (iv) What is a desirable body condition score for a cow at calving?',
        [split('(i) Body condition scoring — A measure of the fat reserves on an animal’s body or the fat reserves measured on a scale of 1-5 for cattle or the fat reserves measured on a scale of 1-9 for pigs',
               note=SHARED.format('4 + 4(3)') + ' Five answers: (i), two points for (ii), (iii) and (iv).'),
         split('(ii) How BCS assessed in cows — Hand pressure applied to (specific areas of)backbone/to assess body fatness or thinness/scale of 1-5 in cattle/1 indicates overly thin/4 indicates overly fat', note='Any two.'),
         split('(iii) Cause of low BCS in cows — Poor feeding or disease or old age or injury or not steaming up'),
         split('(iv) Target BCS at calving — 3 – 3.5')],
        marks=16, tariff={'kind': 'orderedSplit', 'notation': '4 + 4(3)'}, node='3-4')
    # Question 12: three shared scales ---------------------------------------
    add('q12a', 'Q12(a)', '3-1', 'leaf-photosynthesis-and-starch-test',
        '(i) State two ways in which the structure of a leaf is suited to photosynthesis. (ii) A leaf stores the starch it makes during photosynthesis. To test a leaf for the presence of starch, the following method is used: '
        '1. Place the leaf in boiling water for a few seconds. 2. Boil the leaf in alcohol or methylated spirits. 3. Rinse the leaf in warm water. 4. Pour iodine solution on the leaf. '
        'State why each of the above procedures is carried out. (iii) After the above steps, what colour is produced in the leaf if starch is present?',
        [split('(i) Leaf adaptations for photosynthesis — Large surface area (or broad)/ thin/ stomata/ large air spaces/ most chloroplasts towards top of leaf (or in palisade layer)/ good supply of veins (or of vascular tissue or of xylem or of phloem)',
               note=SHARED.format('3(4) + 4(2)') + ' Seven answers: two adaptations, a reason for each of the four procedures, and the colour. Any two adaptations.'),
         split('(ii) Place leaf in boiling water — To kill the leaf or to destroy the enzymes'),
         split('(ii) Boil the leaf in alcohol or methylated spirits — To remove the chlorophyll (or green colour)'),
         split('(ii) Rinse the leaf in warm water — To remove the alcohol or to soften the leaf'),
         split('(ii) Pour iodine solution on the leaf — To test the leaf for starch'),
         split('(iii) Positive colour — Blue-black')],
        marks=20, tariff={'kind': 'orderedSplit', 'notation': '3(4) + 4(2)'}, node='2-0|0-1')
    figured(add('q12b', 'Q12(b)', '4-1', 'excretory-system',
                '(i) The diagram shows part of an animal’s excretory system. What does the term excretion mean? (ii) Name the parts of the diagram labelled A, B, C. '
                '(iii) Name two substances removed from the blood as it passes through part A. (iv) Name two other organs of excretion in a farm animal’s body.',
                [split('(i) Excretion — Removing waste products of metabolism from body or removing waste products from the blood',
                       note=SHARED.format('2(4) + 6(2)') + ' Eight answers: (i), three parts, two substances and two organs.'),
                 split('(ii) A — Kidney'), split('(ii) B — Ureter'), split('(ii) C — Bladder'),
                 split('(iii) Substances removed from blood in kidney — Water/ urea/ salt/ hormones/ water-soluble vitamins/ potassium ions', note='Any two.'),
                 split('(iv) Other organs of excretion — Skin'), split('(iv) Other organs of excretion — Lungs')],
                marks=20, tariff={'kind': 'orderedSplit', 'notation': '2(4) + 6(2)'}), 'q12b')
    figured(add('q12c', 'Q12(c)', '3-1', 'insect-pollinated-flower',
                '(i) Name the parts of the flower labelled A, B, C, D. (ii) Is this flower wind pollinated or insect pollinated? State two reasons for your answer. '
                '(iii) What does the part labelled E develop into? (iv) What does the part labelled C develop into? (v) State three conditions necessary for seeds to germinate.',
                [split('(i) A — Petal', note=SHARED.format('2(4) + 2(2) + 8(1)') + ' Twelve answers: four parts, insect, two reasons, (iii), (iv) and three conditions.'),
                 split('(i) B — Anther', note='The scheme allows stamen.'), split('(i) C — Ovule'), split('(i) D — Stigma', note='The scheme allows carpel.'),
                 split('(ii) Wind or insect pollinated — Insect'),
                 split('(ii) Reasons for choice — Large petals/petals brightly coloured/ scented petals/small anthers/anthers inside petals (or flower)/ stigma inside petals (or flower)', note='Any two.'),
                 split('(iii) E develops into — Fruit'), split('(iv) C develops into — Seed'),
                 split('(v) Conditions essential for germination — Moisture (or water) and Oxygen (or air) and Suitable temperature (or warmth)')],
                marks=20, tariff={'kind': 'orderedSplit', 'notation': '2(4) + 2(2) + 8(1)'}, node='2-0'), 'q12c')
    # Question 13: any two of (a)-(d) -----------------------------------------
    two = 'Answer any two of (a), (b), (c), (d).'
    add('q13a', 'Q13(a)', '2-2-2', 'soil-temperature-loam-earthworms',
        '(i) Name two factors that can affect soil temperature. (ii) What is a loam soil? (iii) State two advantages of a loam soil. (iv) State two ways that earthworms may improve the soil. (v) What may cause a decrease in the earthworm population of a soil?',
        [split('(i) Factors affecting soil temperature — Soil type/ water content/ colour/ humus or organic matter content/ aspect/ altitude/ drainage',
               note=SHARED.format('2(6) + 6(3)') + ' Eight answers: two factors, (ii), two advantages, two ways and (v). Any two factors.'),
         split('(ii) Loam soil — A soil with roughly equal amounts of sand, silt and clay or a soil with 40% sand, 40% silt and 20% clay.'),
         split('(iii) Advantages of loam — Good drainage/ good aeration/ fertile/ warm/ early/ easy to till/ good water holding capacity', note='Any two.'),
         split('(iv) How earthworms improve soil — Improve drainage/ improve aeration/ decompose organic matter into humus or add humus/ improve soil fertility/ mix soil/ improve soil structure', note='Any two.'),
         split('(v) Factor causing decrease in earthworm population — Low pH or water-logging or drought or lack of oxygen or soil cultivation or predators or low organic matter content')],
        two, marks=30, tariff={'kind': 'orderedSplit', 'notation': '2(6) + 6(3)'}, node='1-3|1-4')
    barley = [dict(split(f'(i) {crop}, {heading} — {value}', note=(SHARED.format('2(5) + 5(4)') + ' Seven answers: the three headings, a disease, a pest and two storage factors.') if crop == 'Winter barley' and heading == 'time of sowing' else None), route=slug)
              for slug, crop, values in [('winter-barley', 'Winter barley', ['September - November', 'July - August', '7‒9 tonne/ha']),
                                         ('spring-barley', 'Spring barley', ['February - April', 'August - October', '5‒8 tonne/ha'])]
              for heading, value in zip(['time of sowing', 'time of harvesting', 'expected yield'], values)]
    add('q13b', 'Q13(b)', '3-3-1', 'winter-or-spring-barley',
        '(i) Describe winter barley or spring barley under the following headings: 1. Time of sowing. 2. Time of harvesting. 3. Expected yield. (ii) Name a disease of barley. (iii) Name a pest of barley. (iv) State two factors that allow grain to be stored safely over the winter.',
        barley + [split('(ii) Disease — Rhynchosporium (or leaf blotch) or powdery mildew or leaf rust or barley yellow dwarf virus or eyespot'),
                  split('(iii) Pest — Wireworms or leatherjackets or aphids or birds or slugs'),
                  split('(iv) Safe winter grain storage — Dry (or correct moisture content or 14-18% moisture content)/ treated with acid/ sealed/ correct temperature/ good hygiene/ free from vermin/ good ventilation', note='Any two.')],
        two, marks=30, tariff={'kind': 'orderedSplit', 'notation': '2(5) + 5(4)'}, selection=closed(1, ['Winter barley', 'Spring barley']), node='2-3|2-4|2-5')
    add('q13c', 'Q13(c)', '4-3-3', 'lowland-lamb-management',
        'Describe the management of lowland lambs under the following headings: (i) Care at birth. (ii) Changes in diet. (iii) Housing. (iv) Disease control. (v) Age at weaning.',
        [split('(i) Care at birth — Remove mucus/ dry lamb ( or rub with straw) or make sure ewe licks lamb/ dip navel in iodine/ make sure lamb(s) suck or feed colostrum/ dry bed/ straw bedding/ good hygiene/ adequate supervision/ good shelter or lamb indoors/ remove to lambing pen/ encourage good bond between ewe and lamb(s)',
               note=SHARED.format('2(6) + 6(3)') + ' Eight answers: two for each of (i)-(iii), then (iv) and (v). Any two for (i).'),
         split('(ii) Changes in diet — Colostrum/ ewe’s milk/ meals (or concentrates or ration)/ hay/ silage/ grass', note='Any two.'),
         split('(iii) Housing — Dry/ straw bedding/ good ventilation/ draught free/ good hygiene (or clean)/ clean water supply/ individual lambing pens for first 2-3 days/ group pens for 2-3 days before turn-out', note='Any two.'),
         split('(iv) Disease control — Colostrum or good hygiene or vaccinate or adequate ventilation or antibiotics or isolate sick lamb(s) or steaming up of ewe(s) in late pregnancy or dosing'),
         split('(v) Age at weaning — 12 – 16 weeks')],
        two, marks=30, tariff={'kind': 'orderedSplit', 'notation': '2(6) + 6(3)'}, node='3-5|3-3')
    add('q13di', 'Q13(d)(i)', '4-1', 'dietary-protein-functions', 'State two functions of dietary protein in a farm animal’s body.',
        [menu('Growth|repair of damaged tissue|enzyme production|hormone production|antibodies|development of muscle tissue or meat production|hair or skin formation|improved milk quality', [2, 2],
              'Any two, 2 marks each (2(2)).')], two, node='3-0')
    add('q13dii', 'Q13(d)(ii)', '4-1', 'protein-food-test', 'Describe how to test a food for the presence of protein.',
        [menu('Food sample (or named food sample) in test-tube (or any suitable container)|control|add biuret solution (or add CuSO4 and NaOH)|shake to mix|note colour change|purple (or lilac or violet) colour indicates presence of protein|no change (or blue colour) in control',
              [3] * 4, 'Any four, 3 marks each (4(3)). The scheme notes that all these points may be obtained from a labelled diagram.')], two, node='3-0|0-1')
    add('q13diii', 'Q13(d)(iii)', '4-3-2', 'bulky-feeds-and-concentrates', 'Distinguish between bulky feeds and concentrates and give an example of each.',
        [menu('High water content or Low water content|High fibre content or Low fibre content|Low in energy or High in energy|Low dry matter content or High dry matter content', [4],
              'Any one difference, 4 marks. Each reads bulky feeds, then concentrates.'),
         point('Bulky feeds: grass or silage or hay or haylage or root crops (or named root crop) or forage crop (or named forage crop)', 2),
         point('Concentrates: cereals (or named cereal) or molasses or beet pulp or soya bean meal', 2)], two, node='3-4')
    add('q13div', 'Q13(d)(iv)', '4-3-2', 'maintenance-ration', 'What is meant by the term maintenance ration?',
        [point('The amount of feed needed by an animal to maintain a constant body weight or the amount of feed needed to keep an animal healthy', 3)], two, node='3-4')
    add('q13dv', 'Q13(d)(v)', '4-3-2', 'production-ration', 'What is meant by the term production ration?',
        [point('The extra amount of feed needed by an animal to produce: 1 kg of LWG or 1 litre of milk or 1 kg wool or a calf or a lamb', 3)], two, node='3-4')
    assert len(p.tasks) == 52, len(p.tasks)
    return p


def reviewed_tasks():
    p = build()
    return p.cards, p.tasks


def paper_review():
    return build().review('52 base tasks, one card each. A shared scale that the scheme prints across several parts (Q2, Q5, Q6, Q11(c), Q12(a)-(c), Q13(a)-(c)) is one task with the scale stated; '
                          'parts priced on their own are separate tasks. Q1(b), Q8(c) and Q9(a)(iii) carry the scheme\'s methods as answer routes; Q13(b) carries winter and spring barley as routes.')
