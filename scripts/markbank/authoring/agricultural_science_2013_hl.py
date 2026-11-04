"""2013 Higher: every task authored from the SEC paper and marking scheme (no cards existed).

All 8 paper pages and 12 scheme pages were inspected and the independent census transcribed
before authoring: 59 base tasks, one card each. Question 1 parts print 4, 5, 1 as one pool (the
first correct answer encountered earns the first value), except Q1(h), whose (i) and (ii) carry
3 + 2 each and are separate tasks, Q1(e), whose 4, 5, 1 spans its (i) 1., 2. and (ii) (orderedSplit),
and the Q1(i) drawing. Section B parts are priced on their own; the three Q8(a) headings carry
4 + 4 each. The pH methods (Q2(c)) are answer routes; the Q8(c) choice of three pairs from four
is one card whose eight members are parts. Answers are the scheme's words.
"""
from agricultural_science_legacy import Paper, P, point, menu, closed, routes

FILE = 'LC024ALP000EV.pdf'
HASHES = {'exampapers': 'd238ab2a28d168a1fe5bbf3c6f47d423964d41bd0d88808e0f82d0bb0402c3d5',
          'markingschemes': '031445761b0665780e95b48adc979647bb79153e77c2b75a061e92de59b4a56b'}
SELECTIONS = {
    '875ddc8a7be99683': ('exam-selection', 'Six of nine independent examination questions; every question is retained.'),
    '46a76ead60c9e894': ('independent-task-selection', 'Q1: six of ten separately priced lettered parts; all ten are retained.'),
    'bf954103f9a4b1db': ('not-a-selection', '"Which one of the three macronutrients" asks for a single answer (Q2(a)(ii)), not a choice.'),
    'f1a6e608613461f7': ('open', 'Q2(b)(i): any two of the scheme\'s four standards for ground limestone; a marking menu.'),
    '6a899b1e5eae966e': ('independent-task-selection', 'Q4: two of four independently priced 24-mark experiments; all four are retained.'),
    '0691017188fd9260': ('independent-task-selection', 'Q8: two of three independently priced 24-mark parts; all three are retained.'),
    'ec5616bfbbaf171e': ('open', 'Q8(b)(iii): any two other stages of the carbon cycle from the scheme\'s four; a marking menu.'),
    '61844d336feba9ce': ('closed', 'Q8(c): any three of four printed pairs of terms. One card lists the eight members as parts and counts the best six (three pairs).'),
    'e99aef651ec25a14': ('independent-task-selection', 'Q9: four of five independently priced 12-mark explanations; all five are retained.'),
}
SUPPLEMENTARY = [
    (3, 'Option Two', 'closed', 'Both Q3 options are retained at their own task addresses.'),
    (2, 'Describe an investigation to determine the pH of a soil', 'closed', 'Q2(c): the scheme gives a universal-indicator method OR a pH-meter method, kept as answer routes on one card.'),
]
ATLAS = {
    'Q1(a)': 'pigs', 'Q1(b)': 'crop-production', 'Q1(c)': 'scientific-practices-experiments-investigations|animal-physiology-digestive-system',
    'Q1(d)': 'soil-science', 'Q1(e)': 'animal-diseases|crop-production', 'Q1(f)': 'animal-diseases', 'Q1(g)': 'fertilisers-pollution-environment-cycles',
    'Q1(h)': 'animal-physiology-circulatory-system', 'Q1(i)': 'plant-physiology|grassland', 'Q1(j)': 'dairy-cattle|sheep|pigs',
    'Q2': 'soil-science', 'Q2(a)': 'soil-science|fertilisers-pollution-environment-cycles', 'Q2(c)': 'soil-science|scientific-practices-experiments-investigations',
    'Q3 Option One': 'crop-production', 'Q3 Option One (c)': 'classification-of-animals-plants|crop-production',
    'Q3 Option Two': 'sheep', 'Q3 Option Two (b)': 'beef-cattle|animal-diseases|grassland',
    'Q4': 'scientific-practices-experiments-investigations', 'Q4(a)': 'scientific-practices-experiments-investigations|soil-science',
    'Q4(b)': 'scientific-practices-experiments-investigations|fertilisers-pollution-environment-cycles', 'Q4(c)': 'scientific-practices-experiments-investigations|grassland',
    'Q4(d)': 'scientific-practices-experiments-investigations|animal-physiology-digestive-system',
    'Q5(a)': 'beef-cattle', 'Q5(b)': 'dairy-cattle', 'Q5(c)': 'dairy-cattle|animal-diseases',
    'Q6(a)': 'grassland', 'Q6(b)': 'crop-production', 'Q6(c)': 'plant-physiology',
    'Q7': 'genetics', 'Q7(c)': 'genetics|dairy-cattle',
    'Q8(a)': 'crop-production', 'Q8(b)': 'fertilisers-pollution-environment-cycles|plant-physiology',
    'Q8(c)': 'animal-diseases|crop-production|grassland|sheep',
    'Q9(a)': 'dairy-cattle|genetics', 'Q9(b)': 'energy-crop-catch-crop|crop-production', 'Q9(c)': 'crop-production|innovation-and-biotechnology-in-agriculture',
    'Q9(d)': 'fertilisers-pollution-environment-cycles', 'Q9(e)': 'pigs',
}
REGIONS = {
    # Drafted by regions.py.
    'Q1(a)': (P((2, 0.052, 0.112)), P((5, 0.082, 0.154))),
    'Q1(b)': (P((2, 0.052, 0.083), (2, 0.112, 0.143)), P((5, 0.082, 0.102), (5, 0.154, 0.204))),
    'Q1(c)': (P((2, 0.052, 0.083), (2, 0.143, 0.173)), P((5, 0.082, 0.102), (5, 0.204, 0.237))),
    'Q1(d)': (P((2, 0.052, 0.083), (2, 0.173, 0.248)), P((5, 0.082, 0.102), (5, 0.237, 0.254))),
    'Q1(e)': (P((2, 0.052, 0.083), (2, 0.248, 0.323)), P((5, 0.082, 0.102), (5, 0.254, 0.320))),
    'Q1(f)': (P((2, 0.052, 0.083), (2, 0.323, 0.353)), P((5, 0.082, 0.102), (5, 0.320, 0.354))),
    'Q1(g)': (P((2, 0.052, 0.083), (2, 0.353, 0.383)), P((5, 0.082, 0.102), (5, 0.354, 0.453))),
    'Q1(h)(i)': (P((2, 0.052, 0.083), (2, 0.383, 0.417)), P((5, 0.082, 0.102), (5, 0.450, 0.4675), (5, 0.4675, 0.4845, 0, 0.8))),  # the second 3 + 2 belongs to (ii); left out
    'Q1(h)(ii)': (P((2, 0.052, 0.083), (2, 0.383, 0.402), (2, 0.417, 0.443)), P((5, 0.082, 0.102), (5, 0.4675, 0.4845, 0.8, 0.95), (5, 0.4845, 0.517))),  # with its 3 + 2, printed a line above
    'Q1(i)': (P((2, 0.052, 0.083), (2, 0.443, 0.473)), P((5, 0.082, 0.102), (5, 0.519, 0.564))),
    'Q1(j)': (P((2, 0.052, 0.083), (2, 0.473, 0.593)), P((5, 0.082, 0.102), (5, 0.564, 0.593))),
    'Q2(a)(i)': (P((2, 0.593, 0.778)), P((5, 0.593, 0.697))),
    'Q2(a)(ii)': (P((2, 0.593, 0.758), (2, 0.778, 0.803)), P((5, 0.593, 0.612), (5, 0.697, 0.711))),
    'Q2(b)(i)': (P((2, 0.803, 0.836)), P((5, 0.593, 0.612), (5, 0.711, 0.746))),
    'Q2(b)(ii)': (P((2, 0.836, 0.863)), P((5, 0.593, 0.612), (5, 0.746, 0.829))),
    'Q2(c)': (P((2, 0.863, 0.916)), P((5, 0.593, 0.612), (5, 0.829, 0.914))),
    'Q3 Option One (a)(i)': (P((3, 0.061, 0.125)), P((6, 0.082, 0.169))),
    'Q3 Option One (a)(ii)': (P((3, 0.061, 0.110), (3, 0.125, 0.150)), P((6, 0.082, 0.104), (6, 0.169, 0.186))),
    'Q3 Option One (b)(i)': (P((3, 0.061, 0.090), (3, 0.150, 0.185)), P((6, 0.082, 0.104), (6, 0.186, 0.235))),
    'Q3 Option One (b)(ii)': (P((3, 0.061, 0.090), (3, 0.150, 0.170), (3, 0.185, 0.211)), P((6, 0.082, 0.104), (6, 0.235, 0.269))),
    'Q3 Option One (c)(i)': (P((3, 0.061, 0.090), (3, 0.211, 0.230)), P((6, 0.082, 0.104), (6, 0.269, 0.362))),
    'Q3 Option One (c)(ii)': (P((3, 0.061, 0.090), (3, 0.230, 0.301)), P((6, 0.082, 0.104), (6, 0.362, 0.461))),
    'Q3 Option Two (a)(i)': (P((3, 0.361, 0.425)), P((6, 0.511, 0.580))),
    'Q3 Option Two (a)(ii)': (P((3, 0.361, 0.410), (3, 0.425, 0.451)), P((6, 0.511, 0.542), (6, 0.580, 0.664))),
    'Q3 Option Two (b)(i)': (P((3, 0.361, 0.391), (3, 0.451, 0.470)), P((6, 0.511, 0.542), (6, 0.664, 0.713))),
    'Q3 Option Two (b)(ii)': (P((3, 0.361, 0.391), (3, 0.470, 0.496)), P((6, 0.511, 0.542), (6, 0.713, 0.763))),
    'Q3 Option Two (c)(i)': (P((3, 0.361, 0.391), (3, 0.496, 0.545)), P((6, 0.511, 0.542), (6, 0.760, 0.7945), (6, 0.7945, 0.811, 0, 0.79))),  # the second 4+4 belongs to (ii); left out
    'Q3 Option Two (c)(ii)': (P((3, 0.361, 0.391), (3, 0.545, 0.662)), P((6, 0.511, 0.542), (6, 0.7945, 0.811, 0.79, 0.95), (6, 0.811, 0.847))),  # with its 4+4, printed a line above
    'Q4(a)': (P((3, 0.662, 0.721)), P((7, 0.099, 0.219))),
    'Q4(b)': (P((3, 0.662, 0.691), (3, 0.721, 0.751)), P((7, 0.099, 0.130), (7, 0.219, 0.301))),
    'Q4(c)': (P((3, 0.662, 0.691), (3, 0.751, 0.781)), P((7, 0.099, 0.130), (7, 0.301, 0.368))),
    'Q4(d)': (P((3, 0.662, 0.691), (3, 0.781, 0.823)), P((7, 0.099, 0.130), (7, 0.368, 0.544))),  # trimmed above the page footer
    'Q5(a)': (P((4, 0.061, 0.091)), P((7, 0.544, 0.664))),
    'Q5(b)': (P((4, 0.091, 0.121)), P((7, 0.544, 0.563), (7, 0.664, 0.731))),
    'Q5(c)': (P((4, 0.121, 0.226)), P((7, 0.544, 0.563), (7, 0.731, 0.782))),
    'Q6(a)(i)': (P((4, 0.226, 0.275)), P((8, 0.099, 0.169))),
    'Q6(a)(ii)': (P((4, 0.226, 0.260), (4, 0.275, 0.300)), P((8, 0.099, 0.118), (8, 0.169, 0.219))),
    'Q6(b)(i)': (P((4, 0.301, 0.320)), P((8, 0.099, 0.118), (8, 0.219, 0.252))),
    'Q6(b)(ii)': (P((4, 0.320, 0.361)), P((8, 0.099, 0.118), (8, 0.252, 0.433))),
    'Q6(c)(i)': (P((4, 0.361, 0.380)), P((8, 0.099, 0.118), (8, 0.433, 0.482))),
    'Q6(c)(ii)': (P((4, 0.380, 0.481)), P((8, 0.099, 0.118), (8, 0.482, 0.583))),
    'Q7(a)': (P((4, 0.481, 0.511)), P((9, 0.082, 0.170))),
    'Q7(b)(i)': (P((4, 0.511, 0.631)), P((9, 0.082, 0.101), (9, 0.170, 0.186))),
    'Q7(b)(ii)': (P((4, 0.511, 0.601), (4, 0.631, 0.662)), P((9, 0.082, 0.101), (9, 0.186, 0.202))),
    'Q7(b)(iii)': (P((4, 0.511, 0.601), (4, 0.662, 0.707)), P((9, 0.082, 0.101), (9, 0.202, 0.235))),
    'Q7(b)(iv)': (P((4, 0.511, 0.601), (4, 0.707, 0.781)), P((9, 0.082, 0.101), (9, 0.235, 0.433))),
    'Q7(c)': (P((4, 0.781, 0.834)), P((9, 0.082, 0.101), (9, 0.433, 0.484))),
    'Q8(a)(i)': (P((5, 0.061, 0.155)), P((10, 0.082, 0.169))),
    'Q8(a)(ii)': (P((5, 0.061, 0.140), (5, 0.155, 0.170)), P((10, 0.082, 0.104), (10, 0.169, 0.233))),
    'Q8(a)(iii)': (P((5, 0.061, 0.140), (5, 0.170, 0.211)), P((10, 0.082, 0.104), (10, 0.233, 0.284))),
    'Q8(b)(i)': (P((5, 0.061, 0.106), (5, 0.211, 0.245)), P((10, 0.082, 0.104), (10, 0.284, 0.329))),
    'Q8(b)(ii)': (P((5, 0.061, 0.106), (5, 0.211, 0.230), (5, 0.245, 0.260)), P((10, 0.082, 0.104), (10, 0.329, 0.362))),
    'Q8(b)(iii)': (P((5, 0.061, 0.106), (5, 0.211, 0.230), (5, 0.260, 0.299)), P((10, 0.082, 0.104), (10, 0.362, 0.596))),
    'Q8(c)': (P((5, 0.061, 0.106), (5, 0.299, 0.465)), P((10, 0.082, 0.104), (10, 0.596, 0.910))),
    'Q9(a)': (P((5, 0.465, 0.525)), P((11, 0.082, 0.170))),
    'Q9(b)': (P((5, 0.465, 0.495), (5, 0.525, 0.555)), P((11, 0.082, 0.114), (11, 0.170, 0.236))),
    'Q9(c)': (P((5, 0.465, 0.495), (5, 0.555, 0.585)), P((11, 0.082, 0.114), (11, 0.236, 0.302))),
    'Q9(d)': (P((5, 0.465, 0.495), (5, 0.585, 0.615)), P((11, 0.082, 0.114), (11, 0.302, 0.336))),
    'Q9(e)': (P((5, 0.465, 0.495), (5, 0.615, 0.671)), P((11, 0.082, 0.114), (11, 0.336, 0.407))),
}
FIRST = 'The scheme\'s convention: the first correct answer encountered earns the first value and each later correct answer the next ({}).'
TABLE = 'agsci-2013-hl-paper-soil-test-table'


def split(text, note=None):
    """A row of an orderedSplit card: the scheme prices the scale, not the row."""
    return point(text, None, note)


def build():
    p = Paper(2013, 'higher', FILE, HASHES, REGIONS, ATLAS, 8, 12, SELECTIONS, SUPPLEMENTARY,
              section=lambda ref: 'A' if ref.startswith('Q1(') else 'B')
    add = p.add
    six = 'Answer any six of the parts (a) – (j).'
    pool = 'Any three. ' + FIRST.format('4, 5, 1')
    # Question 1 -------------------------------------------------------------
    add('q1a', 'Q1(a)', '4-2', 'outdoor-pig-breeds', 'Name three breeds of pig including at least two breeds suitable for outdoor (non-intensive) rearing.',
        [menu('(British) Saddle Back|Duroc|Gloucester (Old Spot)|Tamworth|Berkshire|(Vietnamese) Pot-bellied|Pietrain|Large White (York) or Landrace', [4, 5, 1],
              'Three breeds: two from the outdoor breeds (Saddle Back to Pietrain) and one from Large White (York) or Landrace. ' + FIRST.format('4, 5, 1'))], six, node='3-1')
    for key, ref, topic, concept, question, options, node in [
            ('q1b', 'Q1(b)', '3-3-1', 'maize-under-plastic', 'List three advantages of sowing maize under plastic.',
             'Increases soil temp|can be sown earlier|requires a higher temperature for germination|longer growing season|higher yield|shorter germination time|maintains moisture|weed control|prevents bird attack', '2-3'),
            ('q1c', 'Q1(c)', '4-1', 'reducing-sugar-test', 'Describe briefly how you would test a food sample for the presence of a reducing sugar.',
             'Fehling‟s solution or Benedict‟s solution|heat|red = positive or blue = negative', '3-0|0-1'),
            ('q1f', 'Q1(f)', '4-3-3', 'babesia-life-cycle', 'Briefly describe the lifecycle of Babesia, the protozoan that causes red water fever.',
             'Tick sucks blood|from infected cow|sporozoites (in blood)|multiply in tick|in red blood cells|forming gametes|carried by tick|transfer to new cow', '3-5')]:
        add(key, ref, topic, concept, question, [menu(options, [4, 5, 1], pool)], six, node=node)
    add('q1d', 'Q1(d)', '2-1', 'rock-classification', 'Classify the following rock types: (i) quartzite (ii) shale (iii) basalt.',
        [menu(['(i) Metamorphic', '(ii) sedimentary', '(iii) igneous'], [4, 5, 1], 'All three. ' + FIRST.format('4, 5, 1'))], six, node='1-0')
    add('q1e', 'Q1(e)', '4-3-3', 'brown-rat-damage-control',
        '(i) In the case of the brown rat (Rattus norvegicus) on farms, give an example of damage caused: 1. in a livestock situation 2. in a crop situation. (ii) Describe one method of controlling this pest.',
        [split('(i) 1. Livestock situation — Leptospirosis/ Weil‟s disease/ abortion/ infected bites/ spread disease/ food spoilage', FIRST.format('4, 5, 1') + ' Three answers: 1., 2. and (ii).'),
         split('(i) 2. Crop situation — Grain spoilage/ potatoes eaten/ urinating on stored foodstuffs/ eating crop'),
         split('(ii) Control — Traps/ poison/ cats/ dogs/ ultrasonic repellent')],
        six, marks=10, tariff={'kind': 'orderedSplit', 'notation': '4, 5, 1'}, node='3-5|2-4')
    add('q1g', 'Q1(g)', '2-3', 'slurry-versus-fym', 'Compare slurry with farm yard manure (FYM).',
        [menu('liquid (solid)|no straw (straw)|little effect on soil structure (good for structure)|fast response (slow response)|slurry spreader (muck spreader)|fewer earthworms (earthworms)|toxic gases (non-toxic)|higher N or P or K (lower for all three)|more weeds (fewer weeds)|stored in tanks (not stored in tanks)|lower organic matter (higher)|method of reseeding (not a method of reseeding)',
              [4, 5, 1], 'Slurry (FYM): any three. ' + FIRST.format('4, 5, 1') + ' *Allow one point of similarity')], six, node='1-6')
    hepatic = 'Give the precise location and function of the following body parts of a mammal:'
    add('q1hi', 'Q1(h)(i)', '4-1', 'hepatic-artery', 'Give the precise location and function of the hepatic artery.',
        [point('Between aorta and liver', 3, '3 + 2: the location 3 and the function 2.'), point('carries oxygen and-or food or named food product (nutrients)', 2)], six + ' ' + hepatic, node='3-0')
    add('q1hii', 'Q1(h)(ii)', '4-1', 'hepatic-portal-vein', 'Give the precise location and function of the hepatic portal vein.',
        [point('Between small intestine (ileum) and liver', 3, '3 + 2: the location 3 and the function 2.'), point('carries food products or named food product (nutrient)', 2)], six + ' ' + hepatic, node='3-0')
    add('q1i', 'Q1(i)', '3-1', 'grass-flower-diagram', 'Draw a labelled diagram of a grass flower.',
        [point('Diagram', None, 'D 4,2,0. The scheme prints no model drawing.', kind='criterion'),
         point('Palea or glume or bract/ carpel/ stigma/ style/ ovary/ stamen/ anther/ filament', None, 'L 3×2: any three labels, 2 marks each.')],
        six, marks=10, tariff={'kind': 'questionTotal', 'notation': 'D 4,2,0 + L 3×2'}, node='2-0|2-6')
    add('q1j', 'Q1(j)', '4-3-1', 'birth-weights', 'State the approximate weight, in kg, at birth of: (i) a dairy bull calf (ii) a single lamb (iii) a piglet (bonham).',
        [menu(['(i) Calf = 35-45 kg', '(ii) Lamb = 3-5 kg', '(iii) Piglet =1-1.5 kg'], [4, 5, 1], 'All three. ' + FIRST.format('4, 5, 1'))], six, node='3-3')
    # Question 2 -------------------------------------------------------------
    soils = ('The table below shows the results of soil tests carried out on samples from three different fields. Field 1. A field sown with barley for the previous three years. '
             'Field 2. A ploughed-in ley. Field 3. A dairy paddock.')
    add('q2ai', 'Q2(a)(i)', '2-2-1', 'matching-soil-test-results', 'Match each field with its appropriate result and justify your choice in each case.',
        [menu(['Result A = Field 2', 'Result B = Field 1', 'Result C = Field 3'], [2] * 3, '3×2: each match 2.'),
         menu(['Result A - ploughed-in clover or grass adds nitrogen or phosphorus', 'Result B - nutrients or N or K removed from field by crop',
               'Result C - some nutrients replaced by animal waste/ recently fertilised'], [2] * 3, 'Reasons: 3×2, one for each match.')], soils, figure=TABLE, node='1-2|1-6')
    add('q2aii', 'Q2(a)(ii)', '2-3', 'non-polluting-macronutrient', 'Which one of the three macronutrients above is not considered a serious pollutant of water?',
        [point('(ii) Potassium', 4)], soils, figure=TABLE, node='1-6')
    add('q2bi', 'Q2(b)(i)', '2-2-1', 'ground-limestone-standards', 'State any two of the standards with which ground limestone must comply before it can be sold.',
        [menu('All must pass through sieve 3.35 mm mesh|1/3 must pass through 0.15 mm mesh|<3% water|total neutralising value (TNV) > 90%', [4, 4], 'Any two, 4+4.')], node='1-2')
    add('q2bii', 'Q2(b)(ii)', '2-2-1', 'over-liming', 'Mention two consequences of over-liming.',
        [menu('Trace element (copper) uptake diminished|mineralisation of micro nutrients|boron unavailable (immobilises nutrients)|grass burned|grass mat accumulates|scab in potatoes|pH too high for some crops|reduces yield|some minerals (nutrients) are toxic at high pH|damages soil structure|earthworm population decreased',
              [4, 4], 'Any two, 4+4.')], node='1-2')
    methods = [('indicator', 'Universal indicator', 'Small quantity of soil|add deionised (distilled) H2O|filter or add barium sulphate|add universal indicator to filtrate|note colour change|compare with colour chart'),
               ('meter', 'pH meter', 'Small quantity of soil|add deionised (distilled) H2O|filter|pH meter|calibrate|test filtrate with electrode')]
    rows, variants = routes([(slug, label, [menu(steps, [4] * 4, f'{label}: any four, 4 marks each (4×4).')]) for slug, label, steps in methods])
    add('q2c', 'Q2(c)', '2-2-1', 'soil-ph-investigation', 'Describe an investigation to determine the pH of a soil.', rows,
        selection=closed(1, [label for _, label, _ in methods]), node='1-2|0-1', extra={'answerVariants': variants})
    # Question 3 -------------------------------------------------------------
    oat = 'The common wild oat (Avena fatua) is described as a noxious weed.'
    add('q3o1ai', 'Q3 Option One (a)(i)', '3-3-2', 'wild-oat-noxious', 'Give three reasons why this weed is considered noxious.',
        [menu('Contaminates cereal sown for seed|has no food value|host for eelworm|reservoir for cereal diseases|Barley Yellow Dwarf Virus|hard to control (same family as cereals)|multiplies rapidly|competes with cereal (aggressive or invasive)',
              [4] * 3, 'Any three, 4 marks each (3×4).')], oat, node='2-4')
    add('q3o1aii', 'Q3 Option One (a)(ii)', '3-2', 'other-noxious-weeds', 'Name two other noxious weeds.',
        [menu('Ragwort|Thistle|Dock|Barberry|Hop', [2, 2], 'e.g. any two, 2+2.')], oat, node='2-1|2-4')
    sativa = 'The cultivated oat (Avena sativa) was once the most widely grown cereal in Ireland.'
    add('q3o1bi', 'Q3 Option One (b)(i)', '3-3-1', 'oat-decline', 'Give two reasons for the decline in the cultivation of Avena sativa.',
        [menu('Less use of horses|alternative feed available for horses|less human consumption|less thatching straw needed|lower feed value than barley|lower yield than barley|higher demand for barley', [4, 4],
              'Any two, 4+4.')], sativa, node='2-3')
    add('q3o1bii', 'Q3 Option One (b)(ii)', '3-3-1', 'reasons-to-sow-oats', 'Give two reasons for sowing oats.',
        [menu('Animal feed|human consumption|new winter varieties have higher yields|fuel source|grows in poor soils (climate)', [4, 4], 'Any two, 4+4.')], sativa, node='2-3')
    add('q3o1ci', 'Q3 Option One (c)(i)', '3-3-2', 'complete-versus-incomplete-metamorphosis', 'List three differences between complete and incomplete insect metamorphosis.',
        [menu('each stage is distinct (stages after egg [instars] resemble smaller adults)|larva (nymph)|pupa (nymph)|eggs laid (live birth in aphids)', [4] * 3,
              'Complete (Incomplete): any three, 4 marks each (3×4). (Nymph = one point) OR Labelled diagrams.')], node='2-4|3-1')
    add('q3o1cii', 'Q3 Option One (c)(ii)', '3-3-2', 'metamorphosis-examples', 'Name one insect that undergoes each type of metamorphosis.',
        [menu('butterfly|cranefly|click beetle|bluebottle', [2], 'Complete e.g., or correct example: 2.'), menu('aphid|dragonfly', [2], 'Incomplete e.g., or correct example: 2.')],
        'List three differences between complete and incomplete insect metamorphosis.', node='2-4|3-1')
    foster = 'Fostering lambs is a skill in sheep husbandry.'
    add('q3o2ai', 'Q3 Option Two (a)(i)', '4-3-3', 'fostering', 'Explain the term fostering in this context.',
        [point('Fostering: Getting a ewe to accept or allow to suck a lamb that is not her own', 4)], foster, node='3-5')
    add('q3o2aii', 'Q3 Option Two (a)(ii)', '4-3-3', 'fostering-methods', 'Outline three methods used in fostering lambs.',
        [menu('Rub birth-membranes (or fluids) from host ewe onto orphan|place lamb in front of ewe to be licked clean|recently lambed ewe|remove her own lamb|use fostering crate|don‟t let ewe turn round until she bonds|observation until acceptance|introduce dog - ewe becomes protective|use skin of dead lamb|fostering spray|tie legs of lamb',
              [3, 6, 3], 'Any three. ' + FIRST.format('3, 6, 3'))], foster, node='3-5')
    add('q3o2bi', 'Q3 Option Two (b)(i)', '4-3-2', 'overcrowded-cattle-sheds', 'Discuss why overcrowding in cattle sheds can cause serious animal health problems.',
        [menu('Not enough feeding space, airspace or floor space (one point only)|sick animals go unobserved|disease spreads|parasites spread|dung accumulates|stress|bullying|injuries caused', [3, 6, 3],
              'Any three. ' + FIRST.format('3, 6, 3'))], node='3-4|3-5')
    add('q3o2bii', 'Q3 Option Two (b)(ii)', '3-3-2', 'overstocked-paddock', 'Give one effect of overstocking in a paddock situation.',
        [menu('Poaching|disease|poor grass utilisation(waste)|overgrazing (slow recovery)|weeds|animals don‟t reach target-weights|lower milk yield|worms', [4], 'Any one, 4.')], node='2-6')
    lamb = 'In the case of early fat lamb production, state: 1. a suitable ram breed 2. a suitable ewe type.'
    add('q3o2ci', 'Q3 Option Two (c)(i)', '4-2', 'early-lamb-ram-and-ewe', 'In the case of early fat lamb production, state: 1. a suitable ram breed 2. a suitable ewe type.',
        [point('1 Ram: Suffolk (Charolais) not Texel', 4), menu('Hybrid|greyface|halfbred|crossbred|mule|Bellclare|Borris|Blueface Leicester', [4], '2 Ewe: any one, 4.')], node='3-1|3-3')
    add('q3o2cii', 'Q3 Option Two (c)(ii)', '4-3-1', 'early-lamb-justification', 'Justify your selection in each case.',
        [point('Ram: Early maturing breed needed for early finish (fast growth rate)', 4), point('Ewe: Prolificacy/ mothering ability', 4)], lamb, node='3-3')
    # Question 4 -------------------------------------------------------------
    lab = 'Describe laboratory or field experiments for any two of the following:'
    for key, ref, topic, concept, aim, steps, node in [
            ('q4a', 'Q4(a)', '2-2-2', 'structure-and-pore-space', 'To investigate the effect of structure on total pore space in a soil.',
             '2 samples dry soil or named soil types|crush one soil|add same amount or mass of each|to graduated cylinders|note the volume of each|add same amount of water to each|allow to settle for 1hour|record total volume of soil and water|calculate % pore space in each|better structure has greater pore space', '1-3|0-1'),
            ('q4b', 'Q4(b)', '2-2-3', 'rhizobium-culture', 'To grow a culture of bacteria from the root nodules of clover.',
             'Rinse roots|cut off roots|disinfect roots|crush nodules|sterilize inoculating loop|transfer crushed tissue sample|aseptically (or sterile)|to prepared Petri dish of nutrient agar (or agar plate)|control|incubate|at room temperature (18-30°C)|for a number of days (2-7 days)|invert|observe colonies|of Rhizobium', '1-4|0-1'),
            ('q4c', 'Q4(c)', '3-3-2', 'paddock-dry-matter', 'To estimate the amount of grass dry matter (DM) in a paddock.',
             'Quadrat or cage|cut grass within this|weigh|repeat|average mass (in quadrat)|calculate D.M.|by oven or other (squeeze) method|reweigh|constant mass|get area of paddock|D.M. per quadrat × no. of quadrats in paddock area = amount of dry matter in paddock (or correct calculations)', '2-6|0-1'),
            ('q4d', 'Q4(d)', '4-3-2', 'foodstuff-energy-value', 'To determine the energy value of a farm foodstuff.',
             'Stated amount of water|in calorimeter|note temp. at start|weigh sample of food|ignite food|deflagrating spoon|hold under beaker (vessel) until completely burned or dip into water in calorimeter|stir water|read final temp.|reweigh food sample|calculate the amount of heat released per gram of food that burned (ΔH = mCΔT)', '3-4|0-1')]:
        add(key, ref, topic, concept, 'Describe a laboratory or field experiment ' + aim[0].lower() + aim[1:], [menu(steps, [4] * 6, 'Any six, 4 marks each (6x4).')], lab, node=node)
    # Question 5 -------------------------------------------------------------
    add('q5a', 'Q5(a)', '4-3-1', 'bull-beef-principles', 'Briefly outline the main principles in bull beef production.',
        [menu('Bull has testosterone or not castrated|faster growth rate|better FCR|better ADG or LWG (1.5 v 1.3 kg per day)|animals mature more quickly (15-17 v 24 months)|high quality diet needed|more concentrates|barley-beef|small groups|aggressive animals|markets different to normal|high killing out %|better conformation|continental cross breeds|special fencing or housing',
              [4] * 4, 'Any four, 4 marks each (4x4).')], node='3-3')
    add('q5b', 'Q5(b)', '4-3-2', 'late-lactation-management', 'Outline the management principles for the dairy cow in mid-to-late lactation.',
        [menu('Cow is in-calf|BCS = 3|rotational grazing or named system|grass only (no meals should be required)|milk yield declining|once a day milking at end|dried-off 2 months before parturition|dry cow therapy (mastitis prevention)|dosing',
              [4] * 4, 'Any four, 4 marks each (4x4).')], node='3-4')
    add('q5c', 'Q5(c)', '4-3-2', 'high-tbc-reasons', 'Suggest reasons for a high total bacterial count (TBC) in milk.',
        [menu('Cows old|milk machine not serviced properly|liners old or faulty|failure to cool milk to 4°C|mastitis|unhygienic practices or examples of bad practice (allow two points)|injury to udder or teats', [4] * 4,
              'Any four, 4 marks each (4x4).')], node='3-4|3-5')
    # Question 6 -------------------------------------------------------------
    rain = 'Because of the prolonged rainfall in June and July 2012, farmers were advised to raise the cutting height of silage from 5 cm to10 cm.'
    add('q6ai', 'Q6(a)(i)', '3-3-3', 'raised-cutting-height', 'Suggest a scientific reason for this advice.',
        [menu('Prevents soil getting into pit (bales)|wrong type of fermentation|Clostridium spp. (not Lactobacillus)|mouldy|more leafy grass|less dead material|less risk of poaching', [4], 'Any one, 4.')], rain, node='2-6')
    add('q6aii', 'Q6(a)(ii)', '3-3-3', 'wet-silage-effects', 'What are the negative effects of making silage in such weather conditions?',
        [menu('Water-content too high|more effluent|acid too dilute or wrong pH|less sugar in the grass or additives necessary|lower DMD|difficult harvest|soil damage by machinery|less winter feed|difficult to bale', [3, 6, 3],
              'Any three. ' + FIRST.format('3, 6, 3'))], rain, node='2-6')
    add('q6bi', 'Q6(b)(i)', '3-3-2', 'crop-rotation', 'Explain the term crop rotation.',
        [point('Crop rotation: Growing different crops in an area in a definite sequence/ 4-year sequence/ certain crops follow on from each other', 4)], node='2-4')
    add('q6bii', 'Q6(b)(ii)', '3-3-2', 'rotation-crops-and-reasons', 'Name two crops that are commonly used in crop rotation and give a reason why each is used.',
        [menu(['Barley: breaks pest cycle/ breaks diseases of other crops/ breaks weeds of other crops/ less demand on soil nutrients',
               'Potato: breaks diseases of other crops/ breaks pests of other crops/ breaks weeds of other crops/ deep ploughing buries weeds or breaks up soil',
               'Legume: adds nitrogen/ breaks diseases of other crops/ breaks weeds of other crops/ breaks pests of other crops',
               'Grass: improves soil structure/ adds fertility/ breaks diseases of other crops/ breaks weeds of other crops/ breaks pests of other crops/ adds organic matter',
               'Maize: deep roots retrieve minerals'], [6, 6], 'Any two crops: Names 2+2, Reasons 4+4. OR any other crop with correct reason.')], node='2-4')
    add('q6ci', 'Q6(c)(i)', '3-1', 'leaf-structure-diagram', 'Draw a clearly labelled diagram of the internal structure of a leaf.',
        [point('Diagram', None, 'Diagram 4, 2, 0. The scheme prints no model drawing.', kind='criterion'),
         point('Labels: cuticle/ upper epidermis/ palisade/ spongy layer or air spaces/ guard cells/ stoma/ lower epidermis/ vascular bundle', None, 'Any four labels, 1 mark each (4x1).')],
        marks=8, tariff={'kind': 'questionTotal', 'notation': '4, 2, 0 + 4x1'}, node='2-0')
    add('q6cii', 'Q6(c)(ii)', '3-1', 'leaf-photosynthesis-features', 'List four features of a leaf that enable it to maximise photosynthesis.',
        [menu('Flat shape - exposure to more light|waxy cuticle - prevents water loss|many chloroplasts - make more food|chloroplasts concentrated near upper surface - for maximum light absorption|airspaces - for diffusion of O2 and CO2|stomata - for gaseous exchange|palisade cells vertical - to maximise light absorption|thinness - for fast diffusion of gases|vascular tissue - for transport|guard cells - to control stomatal opening',
              [2] * 4, 'Any four, 2 marks each (4x2marks).')], node='2-0')
    # Question 7 -------------------------------------------------------------
    add('q7a', 'Q7(a)', '4-1', 'allele-tetraploid-metaphase', 'Explain each of the following terms: Allele; Tetraploid; Metaphase.',
        [point('Allele: Alternative form of a gene', 4, '3x4.'), point('Tetraploid: 4 sets of chromosomes/ 4N', 4),
         point('Metaphase: 2nd stage in mitosis or meiosis or description of what occurs or explanatory diagram (at least one correct label)', 4)], node='3-6')
    hens = ('In broiler hens, white plumage (W) is dominant to red (w). Comb length on the head is controlled by two alleles: long comb (L) and short comb (S). '
            'An intermediate condition, medium comb, occurs when a pure breeding long-comb bird is crossed with a short-comb bird. Answer the following questions using the letters given above.')
    add('q7bi', 'Q7(b)(i)', '4-1', 'red-medium-comb-genotype', 'State the genotype of a red and medium-comb chick.', [point('(i) wwLS', 4)], hens, node='3-6')
    add('q7bii', 'Q7(b)(ii)', '4-1', 'red-short-comb-genotype', 'State the genotype of a red and short-comb chick.', [point('(ii) wwSS', 4)], hens, node='3-6')
    add('q7biii', 'Q7(b)(iii)', '4-1', 'broiler-f1', 'If a red and long-comb cock is crossed with a purebred white and short-comb hen, state the expected genotype and phenotype in the F1 generation.',
        [point('Genotype: WwLS', 4), point('Phenotype: White, medium-comb', 4)], hens, node='3-6')
    add('q7biv', 'Q7(b)(iv)', '4-1', 'broiler-f2-probabilities',
        'If two F1 siblings are then mated, what is the probability that an F2 chick will have: 1. white plumage and medium comb? 2. red plumage and medium comb? 3. red plumage and short comb?',
        [point('1. 6/16 or 37.5% (accept 6 if above Punnett square is shown)', 4, 'The scheme\'s Punnett square crosses WL, WS, wL and wS gametes.'),
         point('2. 1/8 or 12.5% (accept 2 if above Punnett square is shown)', 4), point('3. 1/16 or 6.25% (accept 1 if above Punnett square is shown)', 4)],
        hens + ' (iii) If a red and long-comb cock is crossed with a purebred white and short-comb hen, state the expected genotype and phenotype in the F1 generation.', node='3-6')
    add('q7c', 'Q7(c)', '4-3-2', 'sexed-semen-advantages', 'Explain the advantages of sexed semen as sold by AI companies.',
        [menu('More heifer calves|expand the herd|more replacements out of your top milkers|less calving difficulty|fewer unwanted (unsaleable) bull calves|90% success rate|can be used for production of top quality bulls', [4, 4],
              'Any two, 4 marks each (2x4).')], node='3-6|3-4')
    # Question 8 -------------------------------------------------------------
    twoof = 'Answer any two of the parts (a), (b), (c).'
    organic = twoof + ' Outline the strategies, other than crop rotation, employed by organic farmers and environmentally conscious growers in dealing with:'
    for key, ref, concept, heading, options in [
            ('q8ai', 'Q8(a)(i)', 'organic-weed-control', 'weeds',
             'tilling operation|hand weeding|certified seeds|growth encouragement|scuffling|hoeing|stubble-cleaning|flaming|mulching or plastic|higher seeding rate|early sowing dates|undersowing|topping|sowing clover'),
            ('q8aii', 'Q8(a)(ii)', 'organic-pest-control', 'invertebrate pests',
             'biological control (example given ducks or geese or ladybirds or bacteria)|growth encouragement|physical barriers (nets, fleece etc.)|early harvesting|hygiene|insect traps|companion crops|resistant varieties'),
            ('q8aiii', 'Q8(a)(iii)', 'organic-disease-control', 'fungal diseases',
             'resistant varieties|burn|remove infected plants or parts|earthing up|Bordeaux mixture|growth encouragement|proper plant density (spacing)|low nitrogen regime|timely harvest|no ground keepers')]:
        add(key, ref, '3-3-2', concept, f'Outline the strategies, other than crop rotation, employed by organic farmers and environmentally conscious growers in dealing with {heading}.',
            [menu(options, [4, 4], 'Any two, 4+4.')], organic, node='2-4')
    carbon = twoof + ' Photosynthesis plays an important role in the carbon cycle.'
    add('q8bi', 'Q8(b)(i)', '2-3', 'photosynthesis-in-carbon-cycle', 'Outline the role of photosynthesis in the carbon cycle.',
        [menu('absorbs CO2 from air|changes it to food|stores carbon|subsequently eaten', [4, 4], 'Photosynthesis: any two, 4+4.')], carbon, node='1-6|2-0')
    add('q8bii', 'Q8(b)(ii)', '3-1', 'photosynthesis-equation', 'Write a balanced equation for photosynthesis.',
        [point('6CO2 + 6H2O → C6H12O6 + 6O2', 4, '2 + 2.')], carbon, node='2-0')
    add('q8biii', 'Q8(b)(iii)', '2-3', 'carbon-cycle-stages', 'Name and describe any two other stages in the carbon cycle.',
        [menu(['Combustion Fossil fuels to CO2', 'Respiration Carbohydrate to CO2', 'Decay (decomposition) Organic matter or manure to CO2', 'Consumption Animals eat plants'], [6, 6],
              'Any two stages (Name of stage, Description): the names 2 + 2 and the descriptions 2(4). The scheme also prints a cycle diagram of combustion, respiration, photosynthesis, death and decay.')],
        carbon, node='1-6')
    members = [('i', 'Blackleg-Cattle', 'Clostridium spp.|lameness|swelling|fever|fatal'),
               ('i', 'Blackleg-Potatoes', 'bacterial infection (Erwinia)|causes soft rot|favoured by wet conditions|prevents emergence|yellow leaves|black stems'),
               ('ii', 'Fodderbeet', 'lower D.M.|*animal feed|can be grazed|higher wet yield'),
               ('ii', 'Sugarbeet', 'higher D.M.|cannot be grazed|high in sugar|sugar production|make ethanol|fed as pulp|produces molasses|*tops fed to cattle or sheep'),
               ('iii', 'Haylage', 'not allowed to dry fully|baled and wrapped|at 60% moisture|*low dry matter|fermentation|dust free'),
               ('iii', 'Hay', 'dried fully|20% moisture|*high dry matter|baled only|weather-dependent|stored under cover'),
               ('iv', 'Maggots', 'external parasites|larvae of flies|soiled wool|eat flesh|tail wagging|treated by dipping|secondary infections|phylum Arthropoda'),
               ('iv', 'Worms', 'internal parasites|endoparasites|treated by dosing|scour|some specific to sheep|mixed grazing|phyla Nematoda or Platyhelminthes')]
    notes = {'Fodderbeet': ' [*one point only for feeding to animals in (ii)]', 'Haylage': ' [*one point only for dry matter comparison in (iii)]'}
    add('q8c', 'Q8(c)', '4-3-3', 'distinguishing-paired-terms',
        'Distinguish between any three of the following pairs of terms: (i) Blackleg in cattle and Blackleg in potatoes. (ii) Fodder beet and Sugar beet. (iii) Haylage and Hay. (iv) Maggots and Worms in sheep.',
        [menu(pool_, [4], f'({k}) {label}: 4.' + notes.get(label, '') + (' 3x(4+4): each term 4, for any three pairs.' if i == 0 else ''))
         for i, (k, label, pool_) in enumerate(members)],
        twoof, marks=24, tariff={'kind': 'bestNofParts', 'answer': 6, 'ofParts': 8, 'perPart': 4},
        selection=closed(3, ['i', 'ii', 'iii', 'iv']), node='3-5|2-4|2-6')
    # Question 9 -------------------------------------------------------------
    why = 'Give scientific explanations for any four of the following:'
    for key, ref, topic, concept, item, points, node in [
            ('q9a', 'Q9(a)', '4-3-1', 'holstein-jersey-cross', 'The increasing popularity of Holstein-Jersey cross cows in dairying.',
             'Eat less|smaller|higher solids in milk|healthier animals|fewer fertility problems|fewer feet problems|easier calvers|hardier|can be outwintered|hybrid vigour', '3-3|3-6'),
            ('q9b', 'Q9(b)', '3-3-1', 'kale-popularity', 'The predominance of kale over other forms of winter forage crops in recent years.',
             'high in protein|good digestibility (68%)|higher yield|higher DM|good winter-hardiness|can feed sheep or cattle|can be zero-grazed|can be sown late (late July)|green “early- bite” for lactating sheep|catch crop|can be ensiled|less depletion of soil nutrients|fast growing', '2-3'),
            ('q9c', 'Q9(c)', '3-3-1', 'potato-micropropagation', 'The micropropagation of new potato varieties.',
             'Is a method of rapidly multiplying new plants|also called tissue culture|asexual reproduction|produces clones|gives large numbers of plants|from small numbers of tubers|disease-free|quick response (few weeks)|potatoes need large amount of seed (1 tonne per acre)', '2-3'),
            ('q9d', 'Q9(d)', '2-3', 'slurry-agitation', 'The agitation of slurry before spreading.',
             'Break crust|stop crust forming|liquefy slurry|makes spreading easy|uniform consistency|releases gases|aeration', '1-6'),
            ('q9e', 'Q9(e)', '4-3-2', 'overfat-pig-carcases', 'Why pigs in some poorly-managed units have overfat carcases.',
             'Not enough protein in diet|poor quality ingredients|pigs increase intake of carbohydrate (energy)|convert this excess energy to fat|poorer FCE|older pigs more likely to put on fat|feeding levels not reduced before slaughter|poor breed selection', '3-4')]:
        add(key, ref, topic, concept, 'Give a scientific explanation for: ' + item, [menu(points, [4] * 3, 'Any three points, 4 marks each (3x4).')], why, node=node)
    assert len(p.tasks) == 59, len(p.tasks)
    return p


def reviewed_tasks():
    p = build()
    return p.cards, p.tasks


def paper_review():
    return build().review('59 base tasks, one card each. Question 1 parts keep the printed 4, 5, 1 on their menus, except Q1(e) (one scale across 1., 2. and (ii): orderedSplit), '
                          'Q1(h), whose (i) and (ii) carry 3 + 2 each, and the Q1(i) drawing. Section B parts are priced on their own; Q2(c) pH methods are answer routes; '
                          'Q8(c) is one card for the choice of three pairs from four.')
