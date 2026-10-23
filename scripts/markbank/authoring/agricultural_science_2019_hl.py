"""2019 Higher: every task authored from the SEC paper and marking scheme (no cards existed).

All 8 paper pages and 16 scheme pages were inspected and the independent census transcribed
before authoring: 61 base tasks, one card each. The scheme's own convention (PDF page 4) reads a
scale such as 4 + 1 + 5 as "the first correct answer encountered is awarded 4 marks and each
subsequent correct answer" the next value, so a Q1 part whose scale spans (i) and (ii) is one
task stating the scale (orderedSplit); a part with one pool keeps the steps on its menu. Method,
cause and grazing-system answers are answer routes; the Q8(c) choice of three pairs from four is
one card whose eight members are parts. Answers are the scheme's words.
"""
from agricultural_science_legacy import Paper, P, point, menu, closed, routes

FILE = 'LC024ALP000EV.pdf'
HASHES = {'exampapers': '2afa8bbcd1d0c6a2f00808e35eb08dec57f7a078c88a1665c827320b9d273f75',
          'markingschemes': '7514b3e21ea16acc7f17e9089eb189576853ce75badcace2e8bd54a92adf08b4'}
SELECTIONS = {
    '15eead8d9cf785a3': ('exam-selection', 'Six of nine independent examination questions; every question is retained.'),
    '8825d399020b1b34': ('independent-task-selection', 'Q1: six of ten separately priced lettered parts; all ten are retained.'),
    'a8d82cbee557eab7': ('open', 'Q2(b)(i): any four causes of soil acidity from the scheme pool; a marking menu.'),
    '22914d5f718927a0': ('closed', 'Q2(b)(ii): any one cause from (i), explained. The scheme gives two points for each cause ("two points from any one category"), kept as answer routes on one card.'),
    'a7c8b62fcdd55c4e': ('independent-task-selection', 'Q4: two of four independently priced 24-mark methods; all four are retained.'),
    '3df80576aaf9c89b': ('independent-task-selection', 'Q8: two of three independently priced 24-mark parts; all three are retained.'),
    'd7ff31562bea3b03': ('closed', 'Q8(c): any three of four printed pairs of terms. One card lists the eight members as parts and counts the best six (three pairs).'),
    'c7aca7d6f7fa2f7c': ('independent-task-selection', 'Q9: four of five independently priced 12-mark explanations; all five are retained.'),
}
SUPPLEMENTARY = [
    (4, 'Option Two', 'closed', 'Both Q3 options are retained at their own task addresses.'),
    (4, 'Describe the grazing management of the suckler herd', 'closed', 'Q3 Option One (b)(ii): the scheme prices a named grazing system and three points from it, for eight systems; kept as answer routes on one card.'),
    (5, 'To show the effect of a mineral deficiency on crop growth', 'closed', 'Q4(a): the scheme gives a flask method OR a soil method, kept as answer routes on one card.'),
]
ATLAS = {
    'Q1(a)': 'crop-production', 'Q1(b)': 'crop-production', 'Q1(c)': 'plant-physiology', 'Q1(d)': 'soil-science',
    'Q1(e)': 'animal-diseases', 'Q1(f)': 'soil-science|scientific-practices-experiments-investigations',
    'Q1(g)': 'animal-physiology-digestive-system', 'Q1(h)': 'crop-production', 'Q1(i)': 'animal-physiology-circulatory-system',
    'Q1(j)': 'sheep|animal-diseases', 'Q2': 'soil-science', 'Q2(c)': 'soil-science|scientific-practices-experiments-investigations',
    'Q3 Option One': 'beef-cattle', 'Q3 Option One (b)(ii)': 'beef-cattle|grassland',
    'Q3 Option Two (a)': 'plant-physiology', 'Q3 Option Two (b)': 'grassland|plant-physiology', 'Q3 Option Two (c)': 'soil-science|animal-diseases|crop-production',
    'Q4': 'scientific-practices-experiments-investigations', 'Q4(a)': 'scientific-practices-experiments-investigations|plant-physiology',
    'Q4(b)': 'scientific-practices-experiments-investigations|dairy-cattle', 'Q4(c)': 'scientific-practices-experiments-investigations|soil-science',
    'Q4(d)': 'scientific-practices-experiments-investigations|grassland',
    'Q5(a)': 'crop-production', 'Q5(b)': 'energy-crop-catch-crop|crop-production', 'Q5(c)': 'crop-production',
    'Q6(a)': 'soil-science', 'Q6(b)': 'grassland', 'Q6(c)': 'fertilisers-pollution-environment-cycles',
    'Q7': 'genetics', 'Q7(c)(ii)': 'genetics|sheep',
    'Q8(a)': 'animal-diseases|sheep', 'Q8(b)': 'plant-physiology', 'Q8(c)': 'animal-physiology-digestive-system|fertilisers-pollution-environment-cycles|dairy-cattle',
    'Q9(a)': 'grassland', 'Q9(b)': 'dairy-cattle', 'Q9(c)': 'crop-production', 'Q9(d)': 'fertilisers-pollution-environment-cycles', 'Q9(e)': 'sheep',
}
REGIONS = {
    # Drafted by regions.py. Hand-set where the scheme centres a letter in its cell below the
    # part's first line (Q7(c)), prints no (ii) marker (Q8(b)(ii)), or the last part would run
    # onto the blank back pages (Q9(e)).
'Q1(a)': (P((2, 0.084, 0.217)), P((5, 0.076, 0.170))),
    'Q1(b)': (P((2, 0.084, 0.116), (2, 0.217, 0.252)), P((5, 0.076, 0.102), (5, 0.170, 0.241))),
    'Q1(c)': (P((2, 0.084, 0.116), (2, 0.252, 0.302)), P((5, 0.076, 0.102), (5, 0.241, 0.332))),
    'Q1(d)': (P((2, 0.084, 0.116), (2, 0.302, 0.339)), P((5, 0.076, 0.102), (5, 0.332, 0.391))),
    'Q1(e)': (P((2, 0.084, 0.116), (2, 0.339, 0.391)), P((5, 0.076, 0.102), (5, 0.391, 0.482))),
    'Q1(f)': (P((2, 0.084, 0.116), (2, 0.391, 0.507)), P((5, 0.076, 0.102), (5, 0.482, 0.571))),
    'Q1(g)': (P((2, 0.084, 0.116), (2, 0.507, 0.558)), P((5, 0.076, 0.102), (5, 0.571, 0.660))),
    'Q1(h)(i)': (P((2, 0.084, 0.116), (2, 0.558, 0.579)), P((5, 0.076, 0.102), (5, 0.660, 0.683))),
    'Q1(h)(ii)': (P((2, 0.084, 0.116), (2, 0.579, 0.609)), P((5, 0.076, 0.102), (5, 0.683, 0.751))),
    'Q1(i)': (P((2, 0.084, 0.116), (2, 0.609, 0.708)), P((5, 0.076, 0.102), (5, 0.751, 0.807))),
    'Q1(j)': (P((2, 0.084, 0.116), (2, 0.708, 0.819)), P((5, 0.076, 0.102), (5, 0.807, 0.886))),
    'Q2(a)(i)': (P((3, 0.102, 0.221)), P((6, 0.081, 0.209))),
    'Q2(a)(ii)': (P((3, 0.102, 0.154), (3, 0.221, 0.310)), P((6, 0.081, 0.103), (6, 0.209, 0.330))),
    'Q2(b)(i)': (P((3, 0.310, 0.358)), P((6, 0.081, 0.103), (6, 0.330, 0.404))),
    'Q2(b)(ii)': (P((3, 0.310, 0.339), (3, 0.358, 0.389)), P((6, 0.081, 0.103), (6, 0.404, 0.632))),
    'Q2(c)': (P((3, 0.389, 0.448)), P((6, 0.081, 0.103), (6, 0.632, 0.728))),
    'Q3 Option One (a)(i)': (P((4, 0.067, 0.150)), P((7, 0.100, 0.162))),
    'Q3 Option One (a)(ii)': (P((4, 0.067, 0.131), (4, 0.150, 0.167)), P((7, 0.100, 0.123), (7, 0.162, 0.215))),
    'Q3 Option One (a)(iii)': (P((4, 0.067, 0.131), (4, 0.167, 0.200)), P((7, 0.100, 0.123), (7, 0.215, 0.267))),
    'Q3 Option One (b)(i)': (P((4, 0.067, 0.099), (4, 0.200, 0.236)), P((7, 0.100, 0.123), (7, 0.267, 0.321))),
    'Q3 Option One (b)(ii)': (P((4, 0.067, 0.099), (4, 0.236, 0.270)), P((7, 0.100, 0.123), (7, 0.321, 0.908))),
    'Q3 Option One (c)': (P((4, 0.067, 0.099), (4, 0.270, 0.339)), P((7, 0.100, 0.123), (8, 0.081, 0.270))),
    'Q3 Option Two (a)(i)': (P((4, 0.409, 0.492)), P((8, 0.321, 0.365))),
    'Q3 Option Two (a)(ii)': (P((4, 0.409, 0.473), (4, 0.492, 0.542)), P((8, 0.321, 0.344), (8, 0.365, 0.482))),
    'Q3 Option Two (b)': (P((4, 0.409, 0.444), (4, 0.542, 0.612)), P((8, 0.321, 0.344), (8, 0.482, 0.677))),
    'Q3 Option Two (c)': (P((4, 0.409, 0.444), (4, 0.612, 0.703)), P((8, 0.321, 0.344), (8, 0.677, 0.843))),
    'Q4(a)': (P((5, 0.067, 0.136)), P((9, 0.098, 0.259))),
    'Q4(b)': (P((5, 0.067, 0.102), (5, 0.136, 0.171)), P((9, 0.098, 0.119), (9, 0.259, 0.351))),
    'Q4(c)': (P((5, 0.067, 0.102), (5, 0.171, 0.206)), P((9, 0.098, 0.119), (9, 0.351, 0.444))),
    'Q4(d)': (P((5, 0.067, 0.102), (5, 0.206, 0.310)), P((9, 0.098, 0.119), (9, 0.444, 0.540))),
    'Q5(a)(i)': (P((5, 0.310, 0.364)), P((10, 0.097, 0.188))),
    'Q5(a)(ii)': (P((5, 0.310, 0.345), (5, 0.364, 0.382)), P((10, 0.097, 0.137), (10, 0.188, 0.257))),
    'Q5(a)(iii)': (P((5, 0.310, 0.345), (5, 0.382, 0.399)), P((10, 0.097, 0.137), (10, 0.257, 0.309))),
    'Q5(a)(iv)': (P((5, 0.310, 0.345), (5, 0.399, 0.432)), P((10, 0.097, 0.137), (10, 0.309, 0.384))),
    'Q5(b)(i)': (P((5, 0.432, 0.503)), P((10, 0.097, 0.117), (10, 0.384, 0.459))),
    'Q5(b)(ii)': (P((5, 0.432, 0.484), (5, 0.503, 0.521)), P((10, 0.097, 0.117), (10, 0.459, 0.494))),
    'Q5(b)(iii)': (P((5, 0.432, 0.484), (5, 0.521, 0.588)), P((10, 0.097, 0.117), (10, 0.494, 0.597))),
    'Q5(c)(i)': (P((5, 0.588, 0.677)), P((10, 0.097, 0.117), (10, 0.597, 0.651))),
    'Q5(c)(ii)': (P((5, 0.588, 0.641), (5, 0.677, 0.732)), P((10, 0.097, 0.117), (10, 0.651, 0.846))),
    'Q6(a)(i)': (P((6, 0.067, 0.121)), P((11, 0.081, 0.139))),
    'Q6(a)(ii)': (P((6, 0.067, 0.102), (6, 0.121, 0.137)), P((11, 0.081, 0.101), (11, 0.139, 0.192))),
    'Q6(a)(iii)': (P((6, 0.067, 0.102), (6, 0.137, 0.188)), P((11, 0.081, 0.101), (11, 0.192, 0.224))),
    'Q6(b)(i)': (P((6, 0.188, 0.242)), P((11, 0.081, 0.101), (11, 0.224, 0.296))),
    'Q6(b)(ii)': (P((6, 0.188, 0.223), (6, 0.242, 0.293)), P((11, 0.081, 0.101), (11, 0.296, 0.416))),
    'Q6(c)': (P((6, 0.293, 0.502)), P((11, 0.081, 0.101), (11, 0.416, 0.612))),
    'Q7(a)(i)': (P((6, 0.502, 0.550)), P((12, 0.081, 0.122))),
    'Q7(a)(ii)': (P((6, 0.502, 0.530), (6, 0.550, 0.567)), P((12, 0.081, 0.101), (12, 0.122, 0.174))),
    'Q7(a)(iii)': (P((6, 0.502, 0.530), (6, 0.567, 0.584)), P((12, 0.081, 0.101), (12, 0.174, 0.208))),
    'Q7(a)(iv)': (P((6, 0.502, 0.530), (6, 0.584, 0.618)), P((12, 0.081, 0.101), (12, 0.208, 0.242))),
    'Q7(b)': (P((6, 0.618, 0.704)), P((12, 0.081, 0.101), (12, 0.242, 0.630))),
    'Q7(c)(i)': (P((6, 0.704, 0.739)), P((12, 0.081, 0.101), (12, 0.630, 0.736))),
    'Q7(c)(ii)': (P((6, 0.739, 0.866)), P((12, 0.081, 0.101), (12, 0.736, 0.835))),
    'Q8(a)': (P((7, 0.067, 0.154)), P((13, 0.081, 0.288))),
    'Q8(b)(i)': (P((7, 0.067, 0.102), (7, 0.154, 0.189)), P((13, 0.081, 0.102), (13, 0.282, 0.400))),
    'Q8(b)(ii)': (P((7, 0.067, 0.102), (7, 0.189, 0.240)), P((13, 0.081, 0.102), (13, 0.400, 0.530))),
    'Q8(c)': (P((7, 0.067, 0.102), (7, 0.240, 0.450)), P((13, 0.081, 0.102), (13, 0.538, 0.833))),
    'Q9(a)': (P((7, 0.450, 0.519)), P((14, 0.081, 0.199))),
    'Q9(b)': (P((7, 0.450, 0.484), (7, 0.519, 0.554)), P((14, 0.081, 0.102), (14, 0.199, 0.277))),
    'Q9(c)': (P((7, 0.450, 0.484), (7, 0.554, 0.588)), P((14, 0.081, 0.102), (14, 0.277, 0.363))),
    'Q9(d)': (P((7, 0.450, 0.484), (7, 0.588, 0.624)), P((14, 0.081, 0.102), (14, 0.363, 0.450))),
    'Q9(e)': (P((7, 0.450, 0.484), (7, 0.624, 0.697)), P((14, 0.081, 0.102), (14, 0.450, 0.526))),
}
FIRST = 'The scheme\'s convention: the first correct answer encountered earns the first value and each later correct answer the next ({}).'


def split(text, note=None):
    """A row of an orderedSplit card: the scheme prices the scale, not the row."""
    return point(text, None, note)


def build():
    p = Paper(2019, 'higher', FILE, HASHES, REGIONS, ATLAS, 8, 16, SELECTIONS, SUPPLEMENTARY,
              section=lambda ref: 'A' if ref.startswith('Q1(') else 'B')
    add = p.add
    # Question 1 -------------------------------------------------------------
    six = 'Answer any six of the parts (a) – (j).'
    add('q1a', 'Q1(a)', '3-3-3', 'spring-cereal-yields', 'Give the target yield in tonnes per hectare of each of the following spring cereal crops: (i) Barley (ii) Wheat (iii) Oats.',
        [menu(['(i) Barley: 6 ‒ 8', '(ii) Wheat: 7 ‒ 9', '(iii) Oats: 5 ‒ 7'], [4, 1, 5], FIRST.format('4 + 1 + 5'))], six)
    add('q1b', 'Q1(b)', '3-3-2', 'dense-forest-planting', 'Give three reasons for the dense planting of Irish coniferous forests.',
        [menu('Trees grow tall or straight or increases competition|fewer side branches|free from knots|allows for thinning|controls weeds|allows for diseased or failed trees', [4, 1, 5],
              'Any three. ' + FIRST.format('4 + 1 + 5'))], six)
    add('q1c', 'Q1(c)', '3-1', 'vegetative-reproduction', '(i) What is meant by the term vegetative reproduction? (ii) Give two examples of vegetative reproduction.',
        [split('(i) Vegetative reproduction — Producing plants from existing plants without using seeds or asexual', FIRST.format('4 + 1 + 5') + ' Three answers: (i) and two examples.'),
         split('(ii) Examples of vegetative propagation — Stolons/ runners/ bulbs/ corms/ rhizomes/ grafting/ cuttings/ layering/ tubers/ budding/ micropropagation/ offshoots or plantlets', 'Any two.')],
        six, marks=10, tariff={'kind': 'orderedSplit', 'notation': '4 + 1 + 5'}, node='2-0')
    add('q1d', 'Q1(d)', '2-2-2', 'loam-characteristics', 'List four characteristics of a loam soil.',
        [menu('Easily tilled or light|good drainage|retains nutrients|good aeration|warmer|retains water', [4, 1, 1, 4], 'Any four. ' + FIRST.format('4 + 1 + 1 + 4'))], six)
    add('q1e', 'Q1(e)', '4-3-3', 'zoonoses', '(i) What is meant by the term zoonosis? (ii) Give two examples of zoonoses with relevance to agriculture.',
        [split('(i) Zoonosis — Disease that can be transmitted from animals to humans', FIRST.format('4 + 1 + 5') + ' Three answers: (i) and two examples.'),
         split('(ii) Agriculturally relevant zoonoses — Orf/ TB/ brucellosis/ ringworm/ foot and mouth/ anthrax/ bird ‘flu/ swine ‘flu/ BSE (CJD)/ rabies/ Lyme disease/ Weil’s disease or leptospirosis',
               'Any two. The examiner reads only the first two items given.')],
        six, marks=10, tariff={'kind': 'orderedSplit', 'notation': '4 + 1 + 5'})
    add('q1f', 'Q1(f)', '2-2-1', 'nitrate-and-phosphate-tests',
        'Nitrates and phosphates are important soil minerals. In the case of each: (i) Describe the test used to show the presence of the mineral. (ii) Describe the colour change that indicates a positive result for the presence of the mineral.',
        [split('(i) Test for nitrates — Diphenylamine or iron sulfate + H2SO4', FIRST.format('4 + 1 + 1 + 4') + ' Four answers: each test and each colour.'),
         split('(i) Test for phosphates — Ammonium molybdate + HNO3'),
         split('(ii) Positive colour for nitrates — Blue with diphenylamine or brown (ring) with FeSO4'),
         split('(ii) Positive colour for phosphates — Yellow')],
        six, marks=10, tariff={'kind': 'orderedSplit', 'notation': '4 + 1 + 1 + 4'}, node='1-2|0-1')
    add('q1g', 'Q1(g)', '4-1', 'liver-functions', 'The liver is the largest internal organ in the mammalian body. State three functions of the liver.',
        [menu('Produces bile|stores glycogen or regulates glucose level|stores minerals|converts amino acids to urea (deamination)|breaks down (old) red blood cells|regulates temperature|stores fat-soluble vitamins or named|assimilates food|produces plasma proteins|detoxification',
              [4, 1, 5], 'Any three. ' + FIRST.format('4 + 1 + 5'))], six)
    add('q1hi', 'Q1(h)(i)', '3-3-2', 'biological-control', 'What is meant by the term biological control?',
        [point('Control of pests by predators or parasites or infectious agent', 6)], six, node='2-4')
    add('q1hii', 'Q1(h)(ii)', '3-3-2', 'biological-control-example', 'Give an example of biological control in agriculture.',
        [point('Rodent or named by cat or dog or mudsnail by geese or ducks or whitefly by parasitic wasp or red spider mite or aphid by ladybird or vine weevil by nematodes or other correct example', 4)], six, node='2-4')
    add('q1i', 'Q1(i)', '4-1', 'organ-locations', 'State the location of each of the following in the mammalian body: (i) Nephron (ii) Adrenal gland (iii) Cerebrum.',
        [menu(['(i) Location of nephron: Kidney', '(ii) Location of adrenal gland: Above or on top of kidney', '(iii) Location of cerebrum: Brain'], [4, 1, 5], FIRST.format('4 + 1 + 5'))], six)
    add('q1j', 'Q1(j)', '4-3-3', 'dipping-and-pour-on', 'Why are practices such as sheep dipping and the use of pour-on essential in flock management?',
        [menu('Control of parasites|prevention of fly strike or control of maggots|prevention of sheep scab or control of mange mites|boost production|control of intestinal worms or ticks', [4, 1, 5],
              'Any three. ' + FIRST.format('4 + 1 + 5'))], six)
    # Question 2 -------------------------------------------------------------
    drought = 'Summer 2018 saw drought conditions across many parts of Ireland, which greatly affected both crop and grass growth.'
    add('q2ai', 'Q2(a)(i)', '2-2-2', 'moisture-stress-and-wilting-point', 'Explain the following terms: 1. Moisture stress 2. Permanent wilting point.',
        [point('1. Moisture stress — Water level in plants lower than normal or water is held tightly in soil by capillary forces or the transpiration rate is too high', 3),
         point('2. Permanent wilting point — The point at which plants cannot extract water from soil', 3)], drought, node='1-3')
    add('q2aii', 'Q2(a)(ii)', '2-2-2', 'available-water-capacity',
        'Available water capacity is an important term in the context of soils. 1. What is meant by the term available water capacity? 2. Which soil type has the highest available water capacity? Give two reasons for your answer.',
        [point('1. Available water capacity — The water that can be extracted from soil or the water available between field capacity and permanent wilting point', 3),
         point('2. Soil with highest available water capacity — Loams or sandy loams', 2),
         menu('High field capacity|medium-to-low permanent wilting point|water not held tightly by soil pores or large pores', [2, 2], 'Reasons: any two, 2 marks each (2(2)).')], drought, node='1-3')
    acid = 'Agricultural land usually becomes more acidic over time.'
    add('q2bi', 'Q2(b)(i)', '2-2-1', 'causes-of-soil-acidity', 'List any four causes of increasing soil acidity over time.',
        [menu('Rainfall or acid rain|crop production|animal urine|leaching|use of some fertilisers|manures or slurry or OM|pine needles|cation exchange|waterlogging', [3] * 4, 'Any four, 3 marks each (4(3)).')], acid, node='1-2')
    causes = [('rainfall', 'Rainfall', 'Slightly acidic nature of rain|because of dissolved CO2'),
              ('acid-rain', 'Acid rain', 'Pollution or detail of|makes rain more acidic than ordinary rain'),
              ('crop-production', 'Crop production', 'Uptake by crops of base-forming cations|e.g. Ca2+'),
              ('animal-urine', 'Animal urine', 'Urine is acidic|due to presence of uric acid'),
              ('leaching', 'Leaching', 'Deposition of alkaline cations or named|away from A horizon'),
              ('fertilisers', 'Some fertilisers', 'Lead to cation exchange|removing base-forming cations|acidic components in some fertilisers'),
              ('cation-exchange', 'Cation exchange', 'Where some base-forming cations are replaced|by more acid-forming ones'),
              ('manures', 'Manures', 'Decomposition of organic matter|acidic component in slurry'),
              ('pine-needles', 'Pine needles', 'Pine needles are acidic|decomposition releases acid'),
              ('waterlogging', 'Waterlogging', 'Anaerobic conditions|produce acids')]
    rows, variants = routes([(slug, label, [menu(points, [3, 3], f'{label}: two points from this cause, 3 marks each (2(3)).')]) for slug, label, points in causes])
    add('q2bii', 'Q2(b)(ii)', '2-2-1', 'explaining-a-cause-of-acidity', 'Explain in detail how any one of the above causes increases soil acidity.', rows, acid,
        selection=closed(1, [label for _, label, _ in causes]), node='1-2', extra={'answerVariants': variants})
    add('q2c', 'Q2(c)', '2-2-1', 'showing-flocculation', 'Describe an experiment to show flocculation in a soil sample.',
        [menu('Equal volumes of water in suitable containers|deionised water|equal volumes of soil or clay|add lime or named flocculant to one|shake both for equal amount of time|allow to stand|result or conclusion', [3] * 5,
              'Any five, 3 marks each (5(3)).')], node='1-2|0-1')
    # Question 3 -------------------------------------------------------------
    sucklers = 'Suckler cows in Ireland are frequently cross-breeds.'
    add('q3o1ai', 'Q3 Option One (a)(i)', '4-2', 'suckler-cross-breeds', 'Suggest two suitable breeds from which to produce cross-breed sucklers.',
        [point('Any two named breeds (maximum one dairy breed)', 4, '2(2): 2 marks for each named breed.')], sucklers, node='3-1|3-6')
    add('q3o1aii', 'Q3 Option One (a)(ii)', '4-3-1', 'cross-breed-cow-benefits', 'Describe the benefits of using cross-breed cows.',
        [menu('Beef traits or named|increased milk yield|hybrid vigour or named', [3, 3], 'Any two, 3 marks each (2(3)).')], sucklers, node='3-3|3-6')
    add('q3o1aiii', 'Q3 Option One (a)(iii)', '4-3-2', 'reproductive-efficiency', 'Explain the term reproductive efficiency in the context of the suckler herd.',
        [point('Number of calves weaned', 3, '2(3).'), point('per hundred cows mated (per year) or per pregnancy rate (per year)', 3)], sucklers, node='3-4')
    add('q3o1bi', 'Q3 Option One (b)(i)', '4-3-1', 'suckled-calf-growth', 'Compare the growth rate of the suckled calf with that of the artificially-reared calf, from birth to weaning.',
        [menu(['LWG 1.2 kg per day', 'LWG 0.8 kg per day'], [2, 2],
              'Suckled (artificially reared), 2(2): the suckled calf\'s figure, then the artificially reared calf\'s in brackets; "higher (lower)" is accepted.')], node='3-3')
    systems = [('paddock', 'Paddock grazing', '21 equal-size paddocks|a paddock grazed for one day|stock moved to next paddock|fertilizer spread on grazed paddock|grass has three weeks to recover|permanent water supply|central roadway|permanent fencing|all grass eaten'),
               ('strip', 'Strip grazing', 'Movable electric fence|fresh grass supplied each day|back fence used to allow grass to recover|all grass eaten|movable water supply|labour-intensive'),
               ('block', 'Block grazing', 'Livestock in same field for up to a week|moved to next field|permanent fencing|not as productive as paddock or strip grazing|weeds and unpalatable grasses a problem|permanent water supply|field fertilized when animals are moved to next field'),
               ('set-stocking', 'Set stocking', 'Animals have free access to most of the farm|difficult to manage livestock|weed problems|unpalatable grasses not eaten|little fertilizer used|permanent water supply'),
               ('zero', 'Zero grazing', 'Animals indoors or confined in yard|grass is cut and brought to animals|land not poached'),
               ('leader-follower', 'Leader-follower', 'Younger animals graze ahead of older animals|young animals eat the tender grass|older animals eat the tougher grasses|efficient use of grass|fewer stomach worms in young animals'),
               ('creep', 'Creep grazing', 'Creep gate or raised fence|young or smaller animals can access fresh grass|young animals can access concentrates|calves can return to suck mother|older animals remain in field to eat tougher grasses'),
               ('mixed', 'Mixed grazing', 'Two different livestock species graze the same field (sheep and cattle)|increases productivity|sheep encourage tillering of grass|sheep eat ragwort|sheep eat grass near dung paths which cattle do not eat|fewer tufts of grass')]
    rows, variants = routes([(slug, label, [point(f'A named grazing system — {label}', 3, 'A named grazing system 3 + any three management points from it, 3 marks each (3(3)).'),
                                            menu(points, [3, 3, 3], f'{label}: any three points.')]) for slug, label, points in systems])
    add('q3o1bii', 'Q3 Option One (b)(ii)', '4-3-2', 'suckler-grazing-management', 'Describe the grazing management of the suckler herd.', rows,
        selection=closed(1, [label for _, label, _ in systems]), node='3-4|2-6', extra={'answerVariants': variants})
    add('q3o1c', 'Q3 Option One (c)', '4-3-1', 'bull-versus-heifer-beef', 'Compare bull-beef production with heifer-beef production.',
        [menu('High LWG|1.4 − 1.6 kg per day|leaner or higher killing-out %|housed or fenced|aggressive|age 15 − 24 months|more concentrates', [3, 1, 1, 3], 'Bull production: any four. ' + FIRST.format('3 + 1 + 1 + 3')),
         menu('Lower LWG|0.8 − 1.0 kg per day|fatter or lower killing out %|outdoors|docile|19 ‒ 24 months|less concentrates', [3, 1, 1, 3], 'Heifer production: any four, 3 + 1 + 1 + 3.')], node='3-3')
    photo = 'Photosynthesis takes place mainly in the leaves of green plants.'
    add('q3o2ai', 'Q3 Option Two (a)(i)', '3-1', 'photosynthesis-equation', 'Give a balanced chemical equation for photosynthesis.',
        [point('Photosynthesis equation — 6CO2 + 6H2O → C6H12O6 + 6O2', 4, '4 or 0.')], photo, node='2-0')
    add('q3o2aii', 'Q3 Option Two (a)(ii)', '3-1', 'leaf-structure-photosynthesis', 'Outline four ways in which the structure of the leaf is suited to photosynthesis.',
        [menu('Thin so faster diffusion|broad or large surface area traps light|chlorophyll or chloroplasts near top surface increases photosynthesis|(efficient) transport in vascular bundles|cuticle conserves water|air spaces or cells not tightly packed allow diffusion|gaseous exchange through stomata',
              [5, 1, 1, 5], 'Any four. ' + FIRST.format('5 + 1 + 1 + 5'))], photo, node='2-0')
    add('q3o2b', 'Q3 Option Two (b)', '3-3-3', 'photosynthesis-microbes-silage',
        'Both photosynthesis and the activity of micro-organisms directly affect the feeding value of silage. Discuss this statement using appropriate references to silage making.',
        [menu(['Photosynthesis: High carbohydrate or sugar', 'cut in middle of day or cut in afternoon', 'for high quality silage',
               'Microorganisms: Lactobacillus (species) or fermentation or anaerobic respiration', 'converts sugar to lactic acid', '(weak) acids preserve grass', 'correct pH stated',
               'fermentation by clostridium produces poor quality silage or aerobic respiration leads to decay'], [4] * 4,
              'Any four, 4 marks each (4(4)), with at least one point on photosynthesis and one on micro-organisms.')], node='2-6|2-0')
    add('q3o2c', 'Q3 Option Two (c)', '2-2-3', 'microorganisms-good-and-bad',
        'Micro-organisms can have both positive and negative effects in agriculture. Describe two positive effects and two negative effects of micro-organisms in agriculture, other than in relation to post-harvest silage production.',
        [menu('Mineralisation or decomposition of organic matter|nitrogen fixation|nitrification|rumen or hindgut digestion|vitamin synthesis|microbial protein|mycorrhizal effect|vaccines or biotechnology', [4, 4], 'Positive effects: any two, 4 marks each (2(4)).'),
         menu('Animal diseases or named|plant diseases or named|denitrification|food spoilage or example|production of toxic gases in slurry tanks', [4, 4], 'Negative effects: any two, 4 marks each (2(4)).')], node='1-4|3-5')
    # Question 4 -------------------------------------------------------------
    lab = 'In the case of any two of the following, describe a laboratory or a field method.'
    rows, variants = routes([(slug, label, [menu(points, [4] * 6, f'{label}: any six, 4 marks each (6(4)).')]) for slug, label, points in [
        ('flasks', 'Flask method', 'Two sterile flasks|deionised water|seedlings to both|nutrient tablet in one|described control|aerate both|cover both|leave for at least two weeks|comparison detail|correct result'),
        ('soil', 'Soil method', 'Fertile soil|soil deficient in mineral|sow equal number of plants in each|similar conditions or named|grown for same length of time|harvest or observe|comparison detail|correct result')]])
    add('q4a', 'Q4(a)', '3-1', 'mineral-deficiency-method', 'Describe a laboratory or a field method to show the effect of a mineral deficiency on crop growth.', rows, lab,
        selection=closed(1, ['Flask method', 'Soil method']), node='2-0|0-1', extra={'answerVariants': variants},
        note='The scheme\'s Question 4 heading reads "Two of (a), (b), (c) to be answered" although it answers all four printed parts (a)-(d); the paper asks for any two of (a)-(d).')
    add('q4b', 'Q4(b)', '4-3-2', 'milk-water-and-solids', 'Describe a laboratory or a field method to estimate the percentages of water and solids in a sample of milk.',
        [menu('Mass of clean container|add milk sample|find mass of milk|dry in oven or on hotplate|to 100 °C|reweigh|to constant mass|loss of mass = mass of water or remaining mass = mass of solids|% calculation for both water and solids', [4] * 6,
              'Any six, 4 marks each (6(4)).')], lab, node='3-4|0-1')
    add('q4c', 'Q4(c)', '2-2-3', 'clover-root-microorganisms', 'Describe a laboratory or a field method to show the presence of micro-organisms in the roots of a clover plant.',
        [menu('Swab bench with disinfectant or work near lit Bunsen|two sterile agar plates|one unopened|wash soil off roots|dip in mild disinfectant solution|crush nodules|streak on agar plate|with inoculating loop|incubate for at least 5 days|20 – 30 °C or room temperature|colonies', [4] * 6,
              'Any six, 4 marks each (6(4)).')], lab, node='1-4|0-1')
    add('q4d', 'Q4(d)', '3-3-3', 'silage-digestibility-method', 'Describe a laboratory or a field method to estimate the digestibility of a silage sample.',
        [menu('Mass of sample|separate into leaf and stem components|mass of each component|calculate ratio between stem and leaf masses|express as fraction or percentage of total mass|the greater the leaf component, the better the digestibility|repeat', [4] * 6,
              'Any six, 4 marks each (6(4)).')], lab, node='2-6|0-1')
    # Question 5 -------------------------------------------------------------
    potato = 'Describe the cultivation of potatoes under the following headings.'
    for key, ref, topic, concept, heading, points, node in [
            ('q5ai', 'Q5(a)(i)', '3-3-1', 'potato-soil-preparation', 'Soil preparation', 'Remove stones|deep plough or > 20 cm depth|rotavate or harrow|drills or ridges', None),
            ('q5aii', 'Q5(a)(ii)', '3-3-1', 'potato-planting', 'Planting', 'Sprouting|potato planter|10 cm deep|drills 70 – 80 cm apart|seeds 25 – 35 cm apart|size of seed 35 – 55 mm|40,000 − 60,00 per ha|correct month of planting for category of potato', None),
            ('q5aiii', 'Q5(a)(iii)', '3-3-2', 'potato-weed-control', 'Weed control', '(Contact and residual) herbicide|earthing-up|shading|hand method or hoeing or scuffling', None),
            ('q5aiv', 'Q5(a)(iv)', '3-3-3', 'potato-harvesting', 'Harvesting', 'Correct time of year related to category|spray haulms in advance|leave for 2 – 3 weeks (to allow skins to harden)|elevator digger|short drop to avoid tuber damage|by hand', None)]:
        add(key, ref, topic, concept, 'Describe the cultivation of potatoes under the heading: ' + heading + '.',
            [menu(points, [1, 1, 2], 'Any three. ' + FIRST.format('1 + 1 + 2'))], potato, node=node)
    catch = 'Due to the possibility of fodder shortages, catch crops were widely sown in autumn 2018.'
    add('q5bi', 'Q5(b)(i)', '3-3-2', 'catch-crop-examples', 'Give two examples of catch crops.',
        [menu('Kale|radish|buckwheat|red clover|berseem clover|fodder rape|black oats|Phacelia|mustard|rye|redstart|IRG|vetch|peas|beans|stubble turnip', [2, 2], 'Any two, 2 marks each (2(2)).')], catch, node='2-4')
    add('q5bii', 'Q5(b)(ii)', '3-3-2', 'catch-crop-rotation', 'Outline one possible rotation that includes a catch crop.',
        [point('Named crop/ named catch crop/ named following winter or spring crop', 6, '6 or 0: the whole rotation.')], catch, node='2-4')
    add('q5biii', 'Q5(b)(iii)', '3-3-2', 'catch-crop-benefits', 'Other than being a source of animal fodder, outline four benefits of sowing a catch crop on a tillage farm.',
        [menu('Ground cover|captures soil nutrients|improves soil organic matter levels|weed suppression|reduces nitrate leaching|less need for winter housing|high yielding|prevents soil erosion or maintain soil structure|some have high crude protein|increases biodiversity|provides a break between grass and cereals or crop rotation',
              [2, 2, 1, 1], 'Any four: 2(2) + 2(1), the first two correct earn 2 each and the next two 1 each.')], catch, node='2-4|1-5')
    spray = 'The use of glyphosate weedkillers, such as Roundup™, has recently been authorised by the EU for a further five years.'
    add('q5ci', 'Q5(c)(i)', '3-3-2', 'broad-spectrum-weedkiller-uses', 'Describe two situations in agriculture in which such broad-spectrum weedkillers might be used.',
        [menu('Before reseeding|pre-harvesting cereals|paths or farm roads|controlling invasive species|seed bed preparation', [1, 3], 'Any two. ' + FIRST.format('1 + 3'))], spray, node='2-4')
    add('q5cii', 'Q5(c)(ii)', '1-5', 'spray-precautions', 'List four precautions that should be taken when using chemical sprays in agriculture, and give a reason for each precaution.',
        [menu('Certified operative|face mask or goggles|respirator|gloves|overalls|do not apply on windy days|wash hands after use|do not apply near waterways or hedgerows|safe disposal of containers or washing out|not on crops near harvest time|apply at the correct rate|correct time of application|avoid livestock',
              [2] * 4, 'Precautions: any four, 2 marks each (4(2)).'),
         menu('To avoid inhaling the chemical|to avoid skin contact|to avoid pollution or to avoid killing non-target species|to avoid entry to food chain', [1] * 4,
              'A matching reason for each precaution, 1 mark each (4(1)); a reason may serve more than one precaution.')], spray, node='0-4|2-4')
    # Question 6 -------------------------------------------------------------
    compaction = 'Soil compaction is common in Irish soils.'
    add('q6ai', 'Q6(a)(i)', '2-3', 'compaction-causes', 'Suggest two possible causes of soil compaction.',
        [menu('Machinery|livestock|overcultivation|plough pan', [2, 2], 'Any two, 2 marks each (2(2)).')], compaction, node='1-5')
    add('q6aii', 'Q6(a)(ii)', '2-3', 'compaction-effects', 'Describe two effects of soil compaction.',
        [menu('Poor aeration|poor root penetration|restricted growth|poor drainage|soil erosion or run-off|damages soil structure', [4, 4], 'Any two, 4 marks each (2(4)).')], compaction, node='1-5')
    add('q6aiii', 'Q6(a)(iii)', '2-3', 'compaction-remedy', 'Explain how soil compaction may be remedied.',
        [point('Cultivation or example of cultivation or subsoiling or aerating', 3)], compaction, node='1-5')
    clover = 'Clover is often included in seed mixtures for grazing.'
    add('q6bi', 'Q6(b)(i)', '3-3-1', 'clover-benefits', 'Give three benefits of the inclusion of clover in a seed mixture.',
        [menu('Nitrogen fixation|ground cover|weed control|palatable|protein rich|high in minerals|high yielding|suited to organic farming or less N application', [3, 3, 3], 'Any three, 3 marks each (3(3)).')], clover, node='2-6')
    add('q6bii', 'Q6(b)(ii)', '3-3-1', 'white-and-red-clover', 'Explain why white clover is used in grazing seed mixtures and red clover is used in silage seed mixtures.',
        [menu('Prostrate|N-fixation|persistent|grazing encourages stolon growth|aggressive or weed control', [3, 3], 'White clover: any two, 3 marks each (2(3)).'),
         menu('Upright or tall|N-fixation|drought tolerant|because deeper tap root|high yield|competes better with taller plants', [3, 3], 'Red clover: any two, 3 marks each (2(3)).')], clover, node='2-6')
    add('q6c', 'Q6(c)', '2-3', 'slurry-versus-fym',
        'Slurry and farmyard manure (FYM) are widely used in Irish agriculture. Compare slurry and FYM under the following headings: (i) Composition (ii) Organic matter content (iii) Storage (iv) Method of application.',
        [split('(i) Composition, slurry — Liquid or Urine + faeces or No straw or High N', FIRST.format('4(2) + 4(1)') + ' Eight answers: slurry and FYM under each heading.'),
         split('(i) Composition, FYM — Solid or Urine + faeces + straw (bedding) or Low N'),
         split('(ii) Organic matter, slurry — Lower OM'), split('(ii) Organic matter, FYM — Higher OM'),
         split('(iii) Storage, slurry — Stored in tanks'), split('(iii) Storage, FYM — Stored open or dungsted'),
         split('(iv) Spreading method, slurry — Slurry tanker or trailing shoe'), split('(iv) Spreading method, FYM — Muck spreader or fork')],
        marks=12, tariff={'kind': 'orderedSplit', 'notation': '4(2) + 4(1)'}, node='1-6')
    # Question 7 -------------------------------------------------------------
    terms = 'Explain the following terms.'
    for key, ref, topic, concept, term, answer in [
            ('q7ai', 'Q7(a)(i)', '4-3-2', 'pedigree-herd', 'Pedigree herd', 'All animals descended from a purebreeding line'),
            ('q7aii', 'Q7(a)(ii)', '4-1', 'recessive-allele', 'Recessive allele', 'Not expressed when paired with dominant allele or only expressed when paired with another recessive allele'),
            ('q7aiii', 'Q7(a)(iii)', '4-3-2', 'natural-service', 'Natural service', 'Use of a male animal in the herd to mate or fertilise the females'),
            ('q7aiv', 'Q7(a)(iv)', '4-1', 'independent-assortment', 'Independent assortment', 'When either of a pair of alleles can combine with either of another pair')]:
        add(key, ref, topic, concept, f'Explain the term: {term}.', [point(answer, 4)], terms, node='3-6')
    add('q7b', 'Q7(b)', '4-1', 'dihybrid-squash-cross',
        'Show the genotypes and phenotypes of the cross between two plants, heterozygous for both characteristics.',
        [point('Parental genotype: WwFf', 2),
         point('Gamete genotypes, across — WF Wf wF wf', 2, '2 or 0.'), point('Gamete genotypes, down — WF Wf wF wf', 2, '2 or 0.'),
         point('Offspring genotypes', 6, '6 or 0: the scheme\'s grid of the gametes WF, Wf, wF and wf each way gives WWFF, WWFf, WwFF, WwFf, WWff, Wwff, wwFF, wwFf and wwff across its sixteen boxes.'),
         point('Phenotypes — White, flat: 9 White, round: 3 Yellow, flat: 3 Yellow, round: 1', 2, 'The four phenotypes, 2 or 0.'),
         point('Matching ratios — White, flat: 9 White, round: 3 Yellow, flat: 3 Yellow, round: 1', 2, 'Their matching ratios, 2 or 0.')],
        'In the squash plant, the allele for white fruit (W) is dominant over the allele for yellow fruit (w), and the allele for flat fruit (F) is dominant over the allele for round fruit (f).',
        node='3-6')
    add('q7ci', 'Q7(c)(i)', '4-1', 'why-drosophila', 'Outline four reasons why fruit flies (Drosophila) are used for genetics experiments.',
        [menu('Large number of offspring|short reproductive time|easily identified traits|easy to keep or cheap|small number of chromosomes|large chromosomes|distinct male and female bodily characteristics|visible sex-linked characteristics|well documented mutations', [2] * 4,
              'Any four, 2 marks each (4(2)).')], node='3-6')
    add('q7cii', 'Q7(c)(ii)', '4-3-1', 'lambing-percentage-and-sex-ratio',
        'On a lowland sheep farm with 100 ewes, the farmer noted at the end of the lambing season that she had 180 lambs born, of which 92 were rams. Comment on the lambing percentage and on the almost equal number of male and female lambs.',
        [point('180% or lambing rate of 1.8 lambs per ewe or a valid comment on lowland sheep production', 4),
         point('Numbers male and female — Males produce X or Y gametes', 2, '2(2).'), point('Numbers male and female — females produce only X gametes', 2)], node='3-3|3-6')
    # Question 8 -------------------------------------------------------------
    twoof = 'Answer any two of (a), (b), (c).'
    add('q8a', 'Q8(a)', '4-3-3', 'liver-fluke-life-cycle', 'Describe, with the aid of a labelled diagram, the life cycle of the liver fluke (Fasciola hepatica).',
        [point('Any six stages in the correct cyclical sequence, indicated or drawn', None, 'Drawing: 6, 3, 0.', kind='criterion'),
         point('Adult fluke in sheep or in cow or in primary host/ eggs out with faeces/ eggs hatch into miracidia/ water or acidic conditions or 10 °C/ miracidia into water snail or into secondary host/ time point (24 hours)/ sporocysts develop in snail/ rediae develop from sporocysts/ cercariae develop from rediae/ cercariae exit snail onto grass/ cercariae encyst/ are grazed by primary host',
               None, 'Labels or description: any six, 3 marks each (6(3)).')],
        twoof, marks=24, tariff={'kind': 'questionTotal', 'notation': 'D 6, 3, 0 + 6(3)'}, node='3-5')
    add('q8bi', 'Q8(b)(i)', '3-1', 'dicot-stem-ts', 'Draw a labelled diagram of a transverse section (T.S.) of a dicotyledonous (dicot) stem.',
        [point('Circular outer surface/ a ring of oval shapes (bundles)/ at least one bundle shown divided into an inner and an outer region by a central strip', None, 'Drawing: 6, 3, 0.', kind='criterion'),
         point('Epidermis or dermal tissue/ vascular bundles(s)/ xylem/ phloem/ cambium/ cortex or pith or ground tissue', None, 'Labels: six, 1 mark each (6(1)).')],
        twoof, marks=12, tariff={'kind': 'questionTotal', 'notation': 'D 6, 3, 0 + L 6(1)'}, node='2-0')
    add('q8bii', 'Q8(b)(ii)', '3-1', 'monocot-versus-dicot-stems', 'Outline two differences to be seen in the transverse sections of monocot and dicot stems.',
        [point('Monocot stem TS — Vascular bundles scattered', 3, 'Monocot 2(3) + dicot 2(3).'), point('Monocot stem TS — no cambium or no secondary thickening or no annual rings', 3),
         point('Dicot stem TS — Vascular bundles in ring', 3), point('Dicot stem TS — cambium present or secondary thickening occurs or annual rings', 3)], twoof, node='2-0')
    members = [('i', 'Omasum', 'Third ruminant stomach compartment or book stomach or manyplies or absorbs water'),
               ('i', 'Abomasum', 'Fourth ruminant stomach compartment or true stomach or completes digestion'),
               ('ii', 'Ureter', 'Connects kidney to bladder or carries urine to the bladder'), ('ii', 'Urethra', 'Carries urine out of body or from bladder'),
               ('iii', 'Split dressing', 'Fertiliser applied in more than one application'), ('iii', 'Top dressing', 'Fertiliser spread over growing crop or bare ground'),
               ('iv', 'Maintenance ration', 'Amount of food needed to maintain bodyweight or to maintain health'),
               ('iv', 'Production ration', 'Amount of extra nutrients needed to produce milk or meat or wool or eggs')]
    add('q8c', 'Q8(c)', '4-1', 'distinguishing-paired-terms',
        'Distinguish clearly between the members of any three of the following pairs of terms: (i) Omasum and abomasum (ii) Ureter and urethra (iii) Split dressing and top dressing (iv) Maintenance ration and production ration.',
        [point(f'({k}) {label} — {answer}', 4, ('Any three pairs: both members of each, 4 + 4 per pair (3(4 + 4)).' if i == 0 else None)) for i, (k, label, answer) in enumerate(members)],
        twoof, marks=24, tariff={'kind': 'bestNofParts', 'answer': 6, 'ofParts': 8, 'perPart': 4},
        selection=closed(3, ['i', 'ii', 'iii', 'iv']), node='3-0|1-6|3-4')
    # Question 9 -------------------------------------------------------------
    why = 'Give scientific explanations for any four of the following.'
    for key, ref, topic, concept, item, points, node in [
            ('q9a', 'Q9(a)', '3-3-3', 'grass-digestibility-season', 'The change in the digestibility of grass over the growing season.', 'Before seed head mainly soluble carbohydrate or sugar (and protein)|almost fully digestible|after seed head more fibre or more cellulose|less digestible|drop from 80% to 50% or drop of 0.5% per day|less glucose at the end of the season', '2-6'),
            ('q9b', 'Q9(b)', '4-3-2', 'culling-older-cows', 'The culling of older cows from the dairy herd.', 'Milk yield decreasing|fertility decreasing|lameness or injury|calving difficulties|increasing cell count or decline in milk quality|more prone to disease|genetic improvement of herd', '3-4'),
            ('q9c', 'Q9(c)', '3-3-1', 'wet-spring-establishment', 'A low rate of establishment of seedlings during a very wet spring.', 'Soil temperature too low|waterlogging|lack of oxygen|low air temperature|slower seedling growth|deferred germination|fungal diseases|pest attack', None),
            ('q9d', 'Q9(d)', '2-3', 'hedgerow-conservation', 'The practice of hedgerow conservation on Irish farms.', 'Shelter livestock or crops or buildings or warm soil|nature corridor or habitat|biodiversity|aesthetic|division of land|environmental schemes|biosecurity', '1-6'),
            ('q9e', 'Q9(e)', '4-3-2', 'flushing-ewes', 'Flushing of ewes prior to mating.', 'Ewes in improving condition|more eggs|better conception rate|regular heat|higher implantation rates|more compact lambing|higher chance of multiple births', None)]:
        add(key, ref, topic, concept, 'Give a scientific explanation for: ' + item, [menu(points, [4, 4, 4], 'Any three points, 4 marks each (3(4)).')], why, node=node)
    assert len(p.tasks) == 61, len(p.tasks)
    return p


def reviewed_tasks():
    p = build()
    return p.cards, p.tasks


def paper_review():
    return build().review('61 base tasks, one card each. A scale the scheme prints across a part\'s (i) and (ii) (Q1(c), (e), (f); Q6(c)) is one task with the scale stated; '
                          'parts priced separately are separate tasks. Q2(b)(ii) causes, Q3 Option One (b)(ii) grazing systems and Q4(a) methods are answer routes; '
                          'Q8(c) is one card for the choice of three pairs from four.')
