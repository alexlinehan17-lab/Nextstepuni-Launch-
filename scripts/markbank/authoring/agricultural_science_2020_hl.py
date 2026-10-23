"""2020 Higher: every task authored from the SEC paper and marking scheme (no cards existed).

All 8 paper pages and 14 scheme pages were inspected and the independent census transcribed
before authoring: 60 base tasks, one card each. Question 1 parts are whole where one instruction
carries a first-correct scale (4 + 3 + 3) or one drawing band; parts asked separately and priced
separately are separate tasks. The Q4(b) enzyme methods are answer routes; the Q8(c) choice of
three pairs from four is one card listing all eight members. Answers are the scheme's words.
"""
from agricultural_science_legacy import Paper, P, point, menu, closed, routes

FILE = 'LC024ALP000EV.pdf'
HASHES = {'exampapers': '18ff9aba31b70f50fd65384ab901a9986a39dd43cc2651474263ed752c3016bb',
          'markingschemes': 'a82cef8f5c02ace6ac4049496bb08a65edad60ca08732e0ca01f2b727b2f76da'}
SELECTIONS = {
    '4911308c64d8f1e9': ('exam-selection', 'Six of nine independent examination questions; every question is retained.'),
    '962283b963326a84': ('independent-task-selection', 'Q1: six of ten separately priced lettered parts; all ten are retained.'),
    'e55782cd87e50f6e': ('open', 'Q2(a)(ii): any two cementation factors from the scheme pool; a marking menu, not a printed item choice.'),
    '0bf9143554c6df30': ('open', 'Q2(a)(iii): any two separation factors from the scheme pool; a marking menu.'),
    '76f733ff62fbc13b': ('open', 'Q3 Option One (b): any four flock-preparation aspects; the scheme prices selection, health, flushing and one extra point.'),
    '98d009d050c51805': ('open', 'Q3 Option One (c): any four parasite-control methods with matching parasites; a marking menu.'),
    '572179c5e3a7d686': ('not-a-selection', '"sown as either winter crops or spring crops" in Q3 Option Two (a)(ii) is the lead-in to a comparison, not a response choice.'),
    '0f331c2e6199d5a8': ('open', 'Q3 Option Two (c): any two direct-control methods; a marking menu.'),
    'c5d0dce02d2551c8': ('open', 'Q3 Option Two (c): any two indirect-control methods; a marking menu.'),
    'fa700a51b93d4682': ('independent-task-selection', 'Q4: two of four independently priced 24-mark methods; all four are retained.'),
    'a544d511088b35cb': ('open', 'Q5(b)(i): any two heat-detection methods; a marking menu.'),
    '93539704ddfab8e0': ('open', 'Q5(c): any two milk tests, each stated as hygiene or composition; a marking menu.'),
    '1b2a4243a870a40c': ('independent-task-selection', 'Q8: two of three independently priced 24-mark parts; all three are retained.'),
    'fc34ea1ab76aaf8a': ('closed', 'Q8(c): any three of four printed pairs of terms. One card lists the eight members as parts and counts the best six (three pairs).'),
    '2e2454056135a7d3': ('independent-task-selection', 'Q9: four of five independently priced 12-mark explanations; all five are retained.'),
}
SUPPLEMENTARY = [
    (4, 'Option Two.', 'closed', 'Both Q3 options are retained at their own task addresses.'),
    (4, 'Describe the cultivation of potatoes or of a named root crop', 'open', 'Q3 Option Two (b): the scheme answers for potatoes and adds "Apply a similar system for a named root crop".'),
    (5, 'To show the action of a named animal enzyme', 'closed', 'Q4(b): the scheme answers for catalase or amylase, kept as answer routes on one card.'),
    (3, 'Describe an experiment to test for the presence of a named soil mineral', 'open', 'Q2(c): any named mineral with its matching reagent and result; the scheme names no list.'),
]
ATLAS = {
    'Q1(a)': 'crop-production', 'Q1(b)': 'classification-of-animals-plants', 'Q1(c)': 'crop-production',
    'Q1(d)': 'plant-physiology', 'Q1(e)': 'animal-physiology-reproductive-systems', 'Q1(f)': 'sheep',
    'Q1(g)': 'plant-physiology|grassland', 'Q1(h)': 'animal-physiology-reproductive-systems', 'Q1(i)': 'soil-science',
    'Q1(j)': 'beef-cattle|crop-production', 'Q2': 'soil-science', 'Q2(c)': 'soil-science|scientific-practices-experiments-investigations',
    'Q3 Option One': 'sheep', 'Q3 Option Two': 'crop-production', 'Q4': 'scientific-practices-experiments-investigations',
    'Q4(a)': 'scientific-practices-experiments-investigations|plant-physiology', 'Q4(b)': 'scientific-practices-experiments-investigations|animal-physiology-digestive-system',
    'Q4(c)': 'scientific-practices-experiments-investigations|soil-science', 'Q4(d)': 'scientific-practices-experiments-investigations|crop-production',
    'Q5': 'dairy-cattle', 'Q5(b)': 'dairy-cattle|animal-physiology-reproductive-systems', 'Q6': 'grassland',
    'Q7': 'genetics', 'Q8(a)': 'fertilisers-pollution-environment-cycles', 'Q8(b)': 'animal-diseases',
    'Q8(c)': 'animal-physiology-digestive-system|plant-physiology|soil-science', 'Q9(a)': 'crop-production',
    'Q9(b)': 'animal-physiology-digestive-system', 'Q9(c)': 'crop-production', 'Q9(d)': 'soil-science', 'Q9(e)': 'beef-cattle|fertilisers-pollution-environment-cycles',
}
REGIONS = {
    'Q1(a)(i)': (P((2, 0.064, 0.120)), P((3, 0.106, 0.187))),
    'Q1(a)(ii)': (P((2, 0.064, 0.099), (2, 0.120, 0.151)), P((3, 0.106, 0.132), (3, 0.187, 0.238))),
    'Q1(b)(i)': (P((2, 0.064, 0.099), (2, 0.151, 0.173)), P((3, 0.106, 0.132), (3, 0.238, 0.292))),
    'Q1(b)(ii)': (P((2, 0.064, 0.099), (2, 0.173, 0.206)), P((3, 0.106, 0.132), (3, 0.292, 0.325))),
    'Q1(c)': (P((2, 0.064, 0.099), (2, 0.206, 0.238)), P((3, 0.106, 0.132), (3, 0.325, 0.394))),
    'Q1(d)': (P((2, 0.064, 0.099), (2, 0.238, 0.293)), P((3, 0.106, 0.132), (3, 0.394, 0.482))),
    'Q1(e)': (P((2, 0.064, 0.099), (2, 0.293, 0.414)), P((3, 0.106, 0.132), (3, 0.482, 0.555))),
    'Q1(f)': (P((2, 0.064, 0.099), (2, 0.414, 0.502)), P((3, 0.106, 0.132), (3, 0.555, 0.597))),
    'Q1(g)': (P((2, 0.064, 0.099), (2, 0.502, 0.536)), P((3, 0.106, 0.132), (3, 0.597, 0.652))),
    'Q1(h)': (P((2, 0.064, 0.099), (2, 0.536, 0.641)), P((3, 0.106, 0.132), (3, 0.652, 0.720))),
    'Q1(i)': (P((2, 0.064, 0.099), (2, 0.641, 0.745)), P((3, 0.106, 0.132), (3, 0.720, 0.788))),
    'Q1(j)': (P((2, 0.064, 0.099), (2, 0.745, 0.819)), P((3, 0.106, 0.132), (3, 0.788, 0.843))),
    'Q2(a)(i)': (P((3, 0.067, 0.138)), P((4, 0.100, 0.162))),
    'Q2(a)(ii)': (P((3, 0.067, 0.116), (3, 0.138, 0.155)), P((4, 0.100, 0.121), (4, 0.162, 0.213))),
    'Q2(a)(iii)': (P((3, 0.067, 0.116), (3, 0.155, 0.206)), P((4, 0.100, 0.121), (4, 0.213, 0.283))),
    'Q2(b)(i)': (P((3, 0.206, 0.260)), P((4, 0.100, 0.121), (4, 0.283, 0.339))),
    'Q2(b)(ii)': (P((3, 0.206, 0.238), (3, 0.260, 0.293)), P((4, 0.100, 0.121), (4, 0.339, 0.391))),
    'Q2(b)(iii)': (P((3, 0.206, 0.238), (3, 0.293, 0.343)), P((4, 0.100, 0.121), (4, 0.391, 0.460))),
    'Q2(c)': (P((3, 0.343, 0.419)), P((4, 0.100, 0.121), (4, 0.460, 0.572))),
    'Q3 Option One (a)': (P((4, 0.067, 0.154)), P((5, 0.072, 0.313))),
    'Q3 Option One (b)': (P((4, 0.067, 0.102), (4, 0.154, 0.206)), P((5, 0.072, 0.095), (5, 0.313, 0.457))),
    'Q3 Option One (c)': (P((4, 0.067, 0.102), (4, 0.206, 0.328)), P((5, 0.072, 0.095), (5, 0.457, 0.709))),
    'Q3 Option Two (a)(i)': (P((4, 0.397, 0.468)), P((6, 0.097, 0.264))),
    'Q3 Option Two (a)(ii)': (P((4, 0.397, 0.432), (4, 0.468, 0.517)), P((6, 0.097, 0.120), (6, 0.264, 0.406))),
    'Q3 Option Two (b)(i)': (P((4, 0.397, 0.432), (4, 0.517, 0.573)), P((6, 0.097, 0.120), (6, 0.406, 0.480))),
    'Q3 Option Two (b)(ii)': (P((4, 0.397, 0.432), (4, 0.517, 0.552), (4, 0.573, 0.590)), P((6, 0.097, 0.120), (6, 0.406, 0.427), (6, 0.480, 0.514))),
    'Q3 Option Two (b)(iii)': (P((4, 0.397, 0.432), (4, 0.517, 0.552), (4, 0.590, 0.607)), P((6, 0.097, 0.120), (6, 0.406, 0.427), (6, 0.514, 0.583))),
    'Q3 Option Two (b)(iv)': (P((4, 0.397, 0.432), (4, 0.517, 0.552), (4, 0.607, 0.641)), P((6, 0.097, 0.120), (6, 0.406, 0.427), (6, 0.583, 0.641))),
    'Q3 Option Two (c)': (P((4, 0.397, 0.432), (4, 0.641, 0.732)), P((6, 0.097, 0.120), (6, 0.641, 0.807))),
    'Q4(a)': (P((5, 0.067, 0.134)), P((7, 0.065, 0.193))),
    'Q4(b)': (P((5, 0.067, 0.099), (5, 0.134, 0.169)), P((7, 0.065, 0.103), (7, 0.193, 0.421))),
    'Q4(c)': (P((5, 0.067, 0.099), (5, 0.169, 0.204)), P((7, 0.065, 0.103), (7, 0.421, 0.529))),
    'Q4(d)': (P((5, 0.067, 0.099), (5, 0.204, 0.328)), P((7, 0.065, 0.103), (7, 0.529, 0.625))),
    'Q5(a)(i)': (P((5, 0.328, 0.382)), P((8, 0.083, 0.193))),
    'Q5(a)(ii)': (P((5, 0.328, 0.360), (5, 0.382, 0.412)), P((8, 0.083, 0.102), (8, 0.193, 0.262))),
    'Q5(b)(i)': (P((5, 0.412, 0.468)), P((8, 0.083, 0.102), (8, 0.262, 0.318))),
    'Q5(b)(ii)': (P((5, 0.412, 0.447), (5, 0.468, 0.502)), P((8, 0.083, 0.102), (8, 0.318, 0.387))),
    'Q5(c)': (P((5, 0.502, 0.628)), P((8, 0.083, 0.102), (8, 0.387, 0.517))),
    'Q6(a)(i)': (P((6, 0.067, 0.155)), P((9, 0.065, 0.139))),
    'Q6(a)(ii)': (P((6, 0.067, 0.136), (6, 0.155, 0.173)), P((9, 0.065, 0.104), (9, 0.139, 0.191))),
    'Q6(a)(iii)': (P((6, 0.067, 0.136), (6, 0.173, 0.206)), P((9, 0.065, 0.104), (9, 0.191, 0.261))),
    'Q6(b)(i)': (P((6, 0.206, 0.277)), P((9, 0.065, 0.085), (9, 0.261, 0.317))),
    'Q6(b)(ii)': (P((6, 0.206, 0.258), (6, 0.277, 0.308)), P((9, 0.065, 0.085), (9, 0.317, 0.403))),
    'Q6(c)': (P((6, 0.308, 0.432)), P((9, 0.065, 0.085), (9, 0.403, 0.516))),
    'Q7(a)': (P((6, 0.432, 0.502)), P((10, 0.061, 0.172))),
    'Q7(b)(i)': (P((6, 0.502, 0.556)), P((10, 0.061, 0.081), (10, 0.172, 0.227))),
    'Q7(b)(ii)': (P((6, 0.502, 0.536), (6, 0.556, 0.606)), P((10, 0.061, 0.081), (10, 0.227, 0.348))),
    'Q7(c)(i)': (P((6, 0.606, 0.694)), P((10, 0.061, 0.081), (10, 0.348, 0.517))),
    'Q7(c)(ii)': (P((6, 0.606, 0.676), (6, 0.694, 0.819)), P((10, 0.061, 0.081), (10, 0.517, 0.633))),
    'Q8(a)(i)': (P((7, 0.067, 0.173)), P((11, 0.082, 0.158))),
    'Q8(a)(ii)': (P((7, 0.067, 0.151), (7, 0.173, 0.221)), P((11, 0.082, 0.103), (11, 0.158, 0.243))),
    'Q8(b)(i)': (P((7, 0.067, 0.099), (7, 0.221, 0.311)), P((11, 0.082, 0.103), (11, 0.243, 0.324))),
    'Q8(b)(ii)': (P((7, 0.067, 0.099), (7, 0.221, 0.273), (7, 0.311, 0.329)), P((11, 0.082, 0.103), (11, 0.243, 0.261), (11, 0.324, 0.401))),
    'Q8(b)(iii)': (P((7, 0.067, 0.099), (7, 0.221, 0.273), (7, 0.329, 0.360)), P((11, 0.082, 0.103), (11, 0.243, 0.261), (11, 0.401, 0.470))),
    'Q8(c)': (P((7, 0.067, 0.099), (7, 0.360, 0.554)), P((11, 0.082, 0.103), (11, 0.470, 0.697))),
    'Q9(a)': (P((7, 0.554, 0.621)), P((12, 0.065, 0.176))),
    'Q9(b)': (P((7, 0.554, 0.586), (7, 0.621, 0.656)), P((12, 0.065, 0.103), (12, 0.176, 0.251))),
    'Q9(c)': (P((7, 0.554, 0.586), (7, 0.656, 0.691)), P((12, 0.065, 0.103), (12, 0.251, 0.326))),
    'Q9(d)': (P((7, 0.554, 0.586), (7, 0.691, 0.726)), P((12, 0.065, 0.103), (12, 0.326, 0.402))),
    'Q9(e)': (P((7, 0.554, 0.586), (7, 0.726, 0.805)), P((12, 0.065, 0.103), (12, 0.402, 0.504))),
}


def build():
    p = Paper(2020, 'higher', FILE, HASHES, REGIONS, ATLAS, 8, 14, SELECTIONS, SUPPLEMENTARY,
              section=lambda ref: 'A' if ref.startswith('Q1(') else 'B')
    add = p.add
    # Question 1 -------------------------------------------------------------
    add('q1ai', 'Q1(a)(i)', '3-2', 'noxious-weed', 'What is meant by the term noxious weed?',
        [menu('Physical or economic damage|legally required to control|may be poisonous|difficult to control|highly competitive or may be persistent', [3, 3], 'Any two points, 3 marks each (2(3)).')])
    add('q1aii', 'Q1(a)(ii)', '3-2', 'noxious-weed-examples', 'Give two examples of noxious weeds.',
        [menu('Ragwort|(creeping) thistle|wild oat|dock|(common) barberry|(male) wild hops', [2, 2], 'Any two, 2 marks each (2(2)).')])
    add('q1bi', 'Q1(b)(i)', '3-3-2', 'incomplete-metamorphosis', 'What is meant by the term incomplete metamorphosis?',
        [menu('Egg-nymph-adult|grow by moulting|instars|nymph resembles adult|no larval stage', [3, 3], 'Any two points, 3 marks each (2(3)).')], node='2-4')
    add('q1bii', 'Q1(b)(ii)', '3-3-2', 'incomplete-metamorphosis-example', 'Give one example of incomplete metamorphosis.',
        [menu('Aphid|dragonfly|cockroach|or other example', [4], 'One example, 4 marks.')], node='2-4')
    add('q1c', 'Q1(c)', '3-3-2', 'thinning-forestry-trees', 'Outline three reasons for the practice of thinning forestry trees.',
        [menu('Poorest trees removed|diseased or damaged trees removed|reduces competition|remaining trees grows faster|improves size of trees|allows access', [4, 3, 3],
              'Any three: the first correct earns 4 and the next two 3 each (4 + 3 + 3).')])
    add('q1d', 'Q1(d)', '3-1', 'dicot-root-vascular-tissue', 'Draw a labelled diagram to show the arrangement of the vascular tissues in a dicotyledonous (dicot) root.',
        [point('Vascular cylinder (stele) and xylem and phloem', None, 'Diagram: 4, 2, 0.', kind='criterion'),
         point('Vascular bundle or vascular cylinder or central cylinder or stele/ xylem/ phloem', None, 'Labels: any two, 3 marks each (2(3)).')],
        marks=10, tariff={'kind': 'questionTotal', 'notation': '4, 2, 0 + 2(3)'})
    add('q1e', 'Q1(e)', '4-1', 'mammalian-part-locations', 'State the location in the mammalian body of each of the following parts: (i) Humerus (ii) Pituitary gland (iii) Bowman’s capsule (iv) Cervix.',
        [menu(['(i) Location of humerus: Front leg (or arm)', '(ii) Location of pituitary gland: Brain',
               '(iii) Location of Bowman’s capsule: Kidney', '(iv) Location of cervix: Uterus (or neck)'], [3, 3, 2, 2],
              'All four locations; the first two correct answers earn 3 each and the other two 2 each (2(3) + 2(2)).')],
        tariff={'kind': 'fixed', 'notation': '2(3) + 2(2)'})
    add('q1f', 'Q1(f)', '4-3-3', 'dagging-and-tagging', 'Explain each of the following terms: (i) Dagging (ii) Tagging.',
        [point('(i) Dagging: Cutting away (dirty or wet) wool from around the tail end of sheep', 5),
         point('(ii) Tagging: Attaching an ID (object or tag) to a livestock animal (or named animal)', 5)])
    add('q1g', 'Q1(g)', '3-1', 'wind-pollinated-grass-flower', 'Describe how the structure of the grass flower is suited to wind pollination.',
        [menu('Long stamens|stamens outside flower|reduced petals or absent petals|large amount of pollen|light pollen or smooth pollen|feathery stigma', [4, 3, 3],
              'Three features: the first correct earns 4 and the next two 3 each (4 + 3 + 3).')], node='2-0|2-6')
    add('q1h', 'Q1(h)', '4-1', 'gestation-lengths', 'State the length of gestation, in days, for each of the following farm animals: (i) Cow (ii) Sheep (iii) Pig.',
        [menu(['(i) 280 ‒ 288 days (allow 9½ ‒ 10 months)', '(ii) 145 ‒ 150 days (allow 5 months)', '(iii) 113 ‒ 117 days (allow 3 months, 3 weeks, 3 days)'], [4, 3, 3],
              'Cow, sheep and pig in order; the first correct answer earns 4 and the next two 3 each (4 + 3 + 3).')])
    add('q1i', 'Q1(i)', '2-1', 'principal-rock-types', 'Classify each of the following into a principal rock type: (i) Slate (ii) Granite (iii) Limestone.',
        [menu(['(i) Slate: Metamorphic', '(ii) Granite: Igneous', '(iii) Limestone: Sedimentary'], [4, 3, 3], 'The first correct answer earns 4 and the next two 3 each (4 + 3 + 3).')])
    add('q1j', 'Q1(j)', '4-3-2', 'rolling-barley', 'Explain the reason for rolling barley grains before feeding to cattle.',
        [point('Hard testa (coat) or rolling breaks coat', 5), point('Otherwise indigestible or allows digestion', 5)])
    # Question 2 -------------------------------------------------------------
    soil = 'Cementation and separation are two processes that affect the development of a soil structure.'
    add('q2ai', 'Q2(a)(i)', '2-2-2', 'cementation-and-separation', 'What is meant by each of the terms cementation and separation?',
        [point('Cementation: (Soil) particles pushed together', 2), point('Separation: Break-up of aggregated or large (soil) particles', 2)], soil)
    add('q2aii', 'Q2(a)(ii)', '2-2-2', 'cementation-factors', 'Outline any two factors that contribute to cementation.',
        [menu('(Small) root activity|bacteria or fungi|drying|ingestion or egestion by earthworms|machinery load or poaching or trampling', [4, 4], 'Any two, 4 marks each (2(4)).')], soil)
    add('q2aiii', 'Q2(a)(iii)', '2-2-2', 'separation-factors', 'Outline any two factors that contribute to separation.',
        [menu('Freeze-thaw action|wetting|(large) root activity|earthworm casts or channels|cultivation practice', [4, 4], 'Any two, 4 marks each (2(4)).')], soil)
    cec = 'Cation exchange capacity (CEC) is an important chemical property of soil.'
    add('q2bi', 'Q2(b)(i)', '2-2-1', 'cation-exchange-capacity', 'What is meant by the term cation exchange capacity?',
        [point('Measure (allow quantity) of the ability of a soil to hold or to release', 2), point('positive ions or named example showing positive charges', 2)], cec)
    add('q2bii', 'Q2(b)(ii)', '2-2-1', 'cec-sand-and-clay', 'Cation exchange capacity is lower in sandy soils than in clay soils. Give two reasons for this.',
        [point('Sand particles chemically inert', 2), point('have fewer negative charges or clay has more', 2)], cec)
    add('q2biii', 'Q2(b)(iii)', '2-2-1', 'raising-cec', 'Describe a method by which cation exchange capacity may be increased in a soil.',
        [point('Add organic matter (or example) or add FYM or add slurry or add lime or add humus or add green manure or add clay', 4)], cec)
    add('q2c', 'Q2(c)', '2-2-1', 'soil-mineral-test', 'Describe an experiment to test for the presence of a named soil mineral.',
        [point('Named mineral', 4), point('Matching reagent', 4), point('Correct result', 4),
         point('Soil sample in test tube or distilled water or shake or filter', 4, 'The scheme names no list of minerals: the reagent and result must match the mineral you named.')],
        node='1-2|0-1')
    # Question 3 -------------------------------------------------------------
    o1 = 'Question 3, Option One.'
    add('q3o1a', 'Q3 Option One (a)', '4-3-1', 'mountain-and-lowland-sheep', 'Compare two named sheep production enterprises that are commonly practised in Ireland.',
        [point('Mountain sheep production', 2), point('Lowland sheep production', 2),
         menu('Low stocking rate or extensive|low production targets|high mortality|single lambs|less labour|outdoor|no flushing or sponging|later lambing|named breed|rough grazing', [4, 4, 4],
              'Comparisons between the enterprises, any three at 4 marks each (3(4)). Each comparison sets a mountain point against its lowland counterpart; the scheme prints the mountain list above "vs" and the lowland list: '
              '"High stocking rate or intensive/ high production targets/ low mortality/ more twins/ more labour/ indoor/ flushing or sponging/ earlier lambing/ named breed/ quality grazing".')],
        o1)
    add('q3o1b', 'Q3 Option One (b)', '4-3-2', 'flock-preparation-before-mating', 'Preparation at breeding time is an important aspect of good flock management. Discuss any four aspects of flock preparation prior to mating.',
        [point('One selection point based on: breed or terminal sire or ewe prolificacy or ram fertility or other valid criterion', 4),
         point('One health point based on: age or mouth or feet or udder or body condition or other valid criterion', 4),
         point('One flushing or sponging point', 4), point('Any one extra point from any of the three above', 4)], o1)
    add('q3o1c', 'Q3 Option One (c)', '4-3-3', 'sheep-parasite-control', 'Control of internal and external parasites is a routine feature of sheep husbandry. Describe any four methods to control named parasites in sheep.',
        [menu('Bolus: stomach worms|Dipping: maggots or sheep scab|Dosing: stomach worms or intestinal worms or other correct|Land drainage: liver fluke|Liming: liver fluke|Pour-on: lice or worms or other correct|Rotational grazing: worms or other correct|Shearing or dagging: maggots|Vaccination: lungworm',
              [4, 4, 4, 4], 'Any four, 4 marks each (4(4)), with the matching parasite in each case.')], o1)
    o2 = 'Question 3, Option Two.'
    add('q3o2ai', 'Q3 Option Two (a)(i)', '3-3-2', 'cereal-location-in-ireland', 'Discuss two features that influence the geographical location of cereal crop production in Ireland.',
        [point('Climate or rainfall or sunshine or temperature', 1), point('Statement comparing effect of rainfall or sunshine or temperature', 2),
         point('Statement linking stated geographical feature to cereal growth', 1), point('Soil', 1),
         point('Heavier soils in northwest and lighter in southeast (or other similar comparison)', 2), point('Lighter soils better suited to cereal crops', 1)], o2, node='2-2')
    add('q3o2aii', 'Q3 Option Two (a)(ii)', '3-3-1', 'winter-and-spring-cereals', 'Cereals in Ireland are sown as either winter crops or spring crops. Outline four differences between the growing of winter and spring cereals.',
        [menu('Sown in September or October|frost resistant|harvested mid-July|higher yield|less N applied', [1, 1, 1, 1], 'Winter cereals: any four, 1 mark each (4(1)).'),
         menu('Sown in March or April|not frost resistant|harvested August or Sept.|lower yield|more N applied', [1, 1, 1, 1], 'Spring cereals: any four, 1 mark each (4(1)).')], o2)
    roots = 'Describe the cultivation of potatoes or of a named root crop under the following headings. The scheme answers for potatoes and adds "Apply a similar system for a named root crop".'
    add('q3o2bi', 'Q3 Option Two (b)(i)', '3-3-1', 'potato-soil-suitability', 'Describe the cultivation of potatoes or of a named root crop under the heading: Soil suitability.',
        [menu('Stone free|pH 5.5 ‒ 6|sandy loam or similar soil type|deep|well-drained', [2, 2], 'Any two, 2 marks each (2(2)).')], roots)
    add('q3o2bii', 'Q3 Option Two (b)(ii)', '3-3-1', 'potato-variety-choice', 'Describe the cultivation of potatoes or of a named root crop under the heading: Choice of variety.',
        [menu('Maincrop|first earlies|second earlies or other named varieties', [2, 2], 'Any two, 2 marks each (2(2)).')], roots)
    add('q3o2biii', 'Q3 Option Two (b)(iii)', '3-3-3', 'potato-yield', 'Describe the cultivation of potatoes or of a named root crop under the heading: Yield.',
        [point('30 ‒ 40 tonne', 2), point('per hectare', 2, 'The scheme adds "(for maincrop or appropriate tonnage for other varieties)".')], roots)
    add('q3o2biv', 'Q3 Option Two (b)(iv)', '3-3-3', 'potato-uses', 'Describe the cultivation of potatoes or of a named root crop under the heading: Uses.',
        [menu('Animal feed|human consumption|seed potatoes', [2, 2], 'Any two, 2 marks each (2(2)).')], roots)
    add('q3o2c', 'Q3 Option Two (c)', '3-3-2', 'direct-and-indirect-crop-protection', 'Weeds, pests and diseases in crops can be controlled by direct or indirect methods. Describe any two methods of direct control and any two methods of indirect control.',
        [menu('Herbicide + description|pesticide + description|fungicide + description', [4, 4], 'Direct control: any two, 2 for the method and 2 for its description each (2(2 + 2)).'),
         menu('Crop rotation + description|growth encouragement+ description|resistant varieties + description|early harvest + description|stubble cleaning + description|biological control + description', [4, 4],
              'Indirect control: any two, 2 for the method and 2 for its description each (2(2 + 2)).')], o2)
    # Question 4 -------------------------------------------------------------
    lab = 'In the case of any two of the following, describe a laboratory or field method.'
    add('q4a', 'Q4(a)', '3-1', 'grass-pigment-chromatography', 'Describe a laboratory or field method to extract different pigments from a sample of grass.',
        [menu('Grind grass|in alcohol|using mortar and pestle|filter (extract)|drop of extract onto|chromatography paper|allow to stand|in solvent (or named)|correct result or pigments named', [4] * 6, 'Any six, 4 marks each (6(4)).')], lab, node='2-0|0-1')
    enzymes = [('catalase', 'Catalase', 'Liver contains catalase|grind liver with sand|add hydrogen peroxide|control or described|water bath at 37 °C|washing up liquid|buffer solution or optimum pH or pH 7|add liver|correct result|correct conclusion|repeat'),
               ('amylase', 'Amylase', 'Saliva contains amylase|saliva into a test tube|add starch solution|control or described|water bath at 37 °C|leave for 5 minutes|buffer solution or optimum pH or pH 7|test with Benedict’s solution or Fehling’s solution|positive result or brick red colour|correct conclusion|repeat')]
    rows, variants = routes([(slug, label, [point('Catalase or amylase or other named animal enzyme', 4, 'Naming the enzyme, 4 marks.'),
                                            menu(steps, [4] * 5, f'{label}: any five points, 4 marks each (5(4)).')]) for slug, label, steps in enzymes])
    add('q4b', 'Q4(b)', '4-1', 'animal-enzyme-action', 'Describe a laboratory or field method to show the action of a named animal enzyme.', rows, lab,
        selection=closed(1, ['Catalase', 'Amylase']), node='3-0|0-1', extra={'answerVariants': variants})
    add('q4c', 'Q4(c)', '2-2-2', 'soil-capillarity-comparison', 'Describe a laboratory or field method to compare capillarity in soil samples.',
        [menu('Two dry soil samples|different types of soil|two open ended glass tubes|cotton wool plugging one end of each|one soil sample into each tube|cotton wool end of both tubes into water|leave for minimum of one hour|correct result|correct conclusion|repeat', [4] * 6, 'Any six, 4 marks each (6(4)).')], lab, node='1-3|0-1')
    add('q4d', 'Q4(d)', '3-3-3', 'root-crop-yield-estimate', 'Describe a laboratory or field method to estimate the yield per hectare of a named root crop.',
        [point('Named root crop', 4), menu('A measured area|dig at harvest time|wash or clean crop|weigh crop|repeat|calculate|details of calculation', [4] * 5, 'Any five, 4 marks each (5(4)).')], lab, node='2-5|0-1')
    # Question 5 -------------------------------------------------------------
    dry = 'The dry period is of great importance to the overall performance of the dairy cow.'
    add('q5ai', 'Q5(a)(i)', '4-3-2', 'dry-period-importance', 'Outline two reasons for the importance of the dry period.',
        [menu('Allows repair of udder tissue|allows development of unborn calf|allows production of colostrum|avoids calving difficulty or cow regains body condition|allows milk reserves to be built up or increased milk yield after calving|allows minerals (or named mineral) to be replenished', [4, 4], 'Any two, 4 marks each (2(4)).')], dry)
    add('q5aii', 'Q5(a)(ii)', '4-3-2', 'dry-cow-management', 'Describe two features of the management of the dairy cow during the dry period.',
        [menu('Body condition score assessed|appropriate feeding regime|(dry cow) mastitis treatment|dosing or other health point', [4, 4], 'Any two, 4 marks each (2(4)).')], dry)
    heat = 'Accurate heat detection is crucial in the use of artificial insemination (AI) in the dairy herd.'
    add('q5bi', 'Q5(b)(i)', '4-3-2', 'heat-detection-methods', 'Describe any two methods of heat detection.',
        [menu('Tail painting or pressure-sensitive paint tag|teaser bulls|electronic activity indicator|mounting activity|chin ball', [4, 4], 'Any two, 2 for the method and 2 for its description each (2(2 + 2)).')], heat, node='3-4|3-6')
    add('q5bii', 'Q5(b)(ii)', '4-3-2', 'ai-advantages-dairy', 'Give two advantages of the use of AI in the dairy herd.',
        [menu('Greater choice of breeds|access to genetically superior bulls|safety|less expensive for smaller herd|accurate calving dates|sexed semen', [4, 4], 'Any two, 4 marks each (2(4)).')], heat, node='3-6')
    add('q5c', 'Q5(c)', '4-3-1', 'milk-quality-tests', 'The hygiene quality and the composition of milk may affect the price per litre paid to the farmer. Describe any two tests carried out on milk to determine hygiene quality or composition. For each test described, state clearly if hygiene quality or composition is being determined.',
        [menu('Total bacterial count (TBC)|somatic cell count|sediment|% water or % solids|% butterfat or % protein|% lactose|presence of antibiotics|presence of thermoduric bacteria', [2, 2], 'Test names: any two, 2 marks each (2(2)).'),
         point('Whether hygiene or composition determined for each test named', 4, '2 marks for each test (2(2)).'),
         point('Two points of description for each test named', 8, '2 + 2 for each test (2(2 + 2)).')],
        tariff={'kind': 'fixed', 'notation': '2(2) + 2(2) + 2(2 + 2)'})
    # Question 6 -------------------------------------------------------------
    sow = 'Direct sowing is the traditional method of sowing grass seed in Ireland. In relation to direct sowing of grass:'
    add('q6ai', 'Q6(a)(i)', '3-3-1', 'grass-seedbed-preparation', 'Describe the stages involved in seed bed preparation.',
        [menu('Ploughing|harrowing or rotavating|rolling', [2, 2], 'Any two, 2 marks each (2(2)).')], sow, node='2-6')
    add('q6aii', 'Q6(a)(ii)', '3-3-1', 'sowing-grass-seed', 'Describe how the seed is sown.',
        [menu('Seed drill|seeds and fertiliser|10 cm apart|2 cm deep|one-pass system', [2, 2, 2], 'Any three, 2 marks each (3(2)).')], sow, node='2-6')
    add('q6aiii', 'Q6(a)(iii)', '2-3', 'direct-sowing-in-loam', 'Explain the benefit of this cultivation method in a loam soil.',
        [menu('Improves structure|improves aeration|improves drainage|exposes pests to predators|better soil-seed contact|better capillarity', [3, 3], 'Any two, 3 marks each (2(3)).')], sow, node='1-5|2-6')
    paddock = 'Paddock grazing may be described as being of great benefit to agriculture but of less benefit to the environment.'
    add('q6bi', 'Q6(b)(i)', '3-3-2', 'paddock-grazing-benefits', 'Give two benefits of paddock grazing in livestock production.',
        [menu('Maximum grass utilisation (no waste)|parasite control|leader-follower system|high quality grazing|less labour-intensive', [4, 4], 'Any two, 4 marks each (2(4)).')], paddock, node='2-6')
    add('q6bii', 'Q6(b)(ii)', '3-3-2', 'paddock-grazing-environment', 'Explain two ways in which paddock grazing may be harmful to the environment.',
        [menu('Monoculture or loss of biodiversity|hedgerow removal or less shelter|habitat removal or habitat loss|poaching|soil erosion|excess fertiliser use', [4, 4], 'Any two, 4 marks each (2(4)).')], paddock, node='2-6|1-6')
    add('q6c', 'Q6(c)', '3-3-3', 'hay-and-silage', 'Compare the contrasting methods of grass conservation in hay making and in silage making.',
        [menu('Dehydration or drying|less than 20% moisture|stemmy or less leafy|aerobic or uncovered', [4, 4], 'Hay: any two, 4 marks each (2(4)).'),
         menu('(Controlled) fermentation|pH reduction|leafy grass|anaerobic or sealed', [4, 4], 'Silage: any two, 4 marks each (2(4)).')], node='2-6')
    # Question 7 -------------------------------------------------------------
    add('q7a', 'Q7(a)', '4-1', 'stages-of-mitosis', 'Mitosis and meiosis are forms of cell division that occur in all agriculturally important organisms. Describe, with the aid of labelled diagrams, the stages of mitosis.',
        [point('Stages named in order: Prophase—metaphase—anaphase—telophase', None, '1 mark for each stage named in order (4(1)).', kind='criterion'),
         point('Diagram of each stage', None, '2 marks for each diagram (4(2)).', kind='criterion'),
         point('Any two correct labels other than the stage names', None, '1 mark each (2(1)).', kind='criterion')],
        marks=14, tariff={'kind': 'questionTotal', 'notation': '4(1) + 4(2) + 2(1)'}, node='3-6')
    mei = 'Meiosis occurs during the production of male and female gametes.'
    add('q7bi', 'Q7(b)(i)', '4-1', 'meiosis-in-gametes', 'Explain the significance of meiosis in gamete formation.',
        [point('Halves (or reduces) diploid number', 4), point('Allows for fertilisation', 4)], mei, node='3-6')
    add('q7bii', 'Q7(b)(ii)', '4-1', 'crossing-over', 'Outline the process of crossing-over which occurs during meiosis and explain its significance.',
        [point('Homologous chromosomes', 3, 'Process.'), point('Exchange DNA', 3, 'Process.'), point('Allows variation', 2, 'Significance.')], mei, node='3-6')
    bean = ('In the bean plant, hairless leaf (H) is dominant over hairy leaf (h), and straight petiole (S) is dominant over spiral petiole (s). '
            'A bean plant, heterozygous for both conditions, was self-fertilised and the seeds were collected and germinated and grown to maturity.')
    add('q7ci', 'Q7(c)(i)', '4-1', 'dihybrid-bean-cross', 'Outline the details of this cross.',
        [point('HS Hs hS hs Parental gametes', None, '2(2) for the parental gametes.', kind='criterion'),
         point('All offspring genotypes', None, '6 or 0: the scheme\'s grid lists HHSS, HHSs, HhSS, HhSs, HHss, Hhss, hhSS, hhSs and hhss across the sixteen boxes.', kind='criterion')],
        bean, marks=10, tariff={'kind': 'questionTotal', 'notation': '2(2) + 6, 0'}, node='3-6')
    add('q7cii', 'Q7(c)(ii)', '4-1', 'dihybrid-bean-proportions', 'State what proportions of the offspring plants you would expect to see with: 1. Hairless leaf 2. Straight petiole 3. Spiral petiole 4. Hairless leaf together with spiral petiole.',
        [point('1. Hairless leaf: 12/16 (75%)', 2), point('2. Straight petiole: 12/16 (75%)', 2), point('3. Spiral petiole: 4/16 (25%)', 2),
         point('4. Hairless leaf with spiral petiole: 3/16 (18.75%)', 2)], bean, node='3-6')
    # Question 8 -------------------------------------------------------------
    carbon = 'It is said that agriculture is the single largest contributor to Irish greenhouse gas emissions.'
    add('q8ai', 'Q8(a)(i)', '2-3', 'carbon-cycle-diagram', 'Use a labelled diagram to illustrate the carbon cycle.',
        [point('Diagram', None, 'Diagram: 6, 3, 0.', kind='criterion'),
         point('CO2 in air/ plants/ animals/ fossil fuels', None, 'Labels: five, 2 marks each (5(2)).')],
        carbon, marks=16, tariff={'kind': 'questionTotal', 'notation': 'D 6, 3, 0 + L 5(2)'}, node='1-6')
    add('q8aii', 'Q8(a)(ii)', '2-3', 'cutting-farm-emissions', 'With reference to the carbon cycle, suggest two ways in which the emissions from agriculture could be reduced to help meet Ireland’s climate change targets.',
        [menu('Reduction in national cattle herd|afforestation|energy crops|carbon sequestration|reduction in fossil fuel use or example of increased efficiency|renewable energy sources', [4, 4], 'Any two, 4 marks each (2(4)).')], carbon, node='1-6')
    abx = 'The overuse of antibiotics to control bacterial diseases in farm animals can lead to these and other bacteria becoming resistant to antibiotics.'
    add('q8bi', 'Q8(b)(i)', '4-3-3', 'bacterial-diseases-of-farm-animals', 'Name two common bacterial diseases of farm animals, which are treated with antibiotics.',
        [menu('Mastitis|blackleg|footrot|bacterial scour|farrowing fever|bacterial pneumonia|joint-ill|other correct', [4, 4], 'Any two, 4 marks each (2(4)).')], abx)
    add('q8bii', 'Q8(b)(ii)', '4-3-3', 'antibiotic-resistance', 'Outline how antibiotic resistance develops in bacteria.',
        [menu('Overuse of antibiotics|mutation|evolution|natural selection|uptake of genes from plasmids or from viruses or from other resistant bacteria', [4, 4, 4], 'Any three, 4 marks each (3(4)).')], abx, node='3-5|3-6')
    add('q8biii', 'Q8(b)(iii)', '4-3-3', 'disease-control-without-antibiotics', 'Suggest a method of disease control other than using antibiotics.',
        [point('Milking out or hygiene or vaccination or footbath or biosecurity or culling or isolation', 4)], abx)
    pairs = [('i', 'Ruminant stomach', 'Four-chambered stomach|allows cellulose digestion'), ('i', 'Monogastric stomach', 'Single stomach|does not digest cellulose'),
             ('ii', 'Transpiration', 'Loss of water vapour|from the stomata'), ('ii', 'Translocation', 'Movement of materials|through the phloem'),
             ('iii', 'Saturated flow', 'Movement of water|below water table'), ('iii', 'Unsaturated flow', 'Movement of water|above water table'),
             ('iv', 'Hypogeal germination', 'Germination below the soil|cotyledons for energy'), ('iv', 'Epigeal germination', 'Germination above the soil|cotyledons above soil')]
    add('q8c', 'Q8(c)', '4-1', 'distinguishing-paired-terms', 'Distinguish clearly between the members of any three of the following pairs of terms: (i) Ruminant and monogastric digestive systems (ii) Transpiration and translocation (iii) Saturated flow and unsaturated flow in soils (iv) Hypogeal germination and epigeal germination.',
        [menu(pool, [2, 2], f'({k}) {label}: two points.' + (' Any three pairs: both members of each, 2 + 2 per member (3 × (2 + 2) vs (2 + 2)).' if i == 0 else ''))
         for i, (k, label, pool) in enumerate(pairs)],
        marks=24, tariff={'kind': 'bestNofParts', 'answer': 6, 'ofParts': 8, 'perPart': 4},
        selection=closed(3, ['i', 'ii', 'iii', 'iv']), node='3-0|2-0|1-3')
    # Question 9 -------------------------------------------------------------
    why = 'Give scientific explanations for any four of the following.'
    for key, ref, topic, concept, question, options, node in [
            ('q9a', 'Q9(a)', '3-3-1', 'chitting-early-potatoes', 'Sprouting or ‘chitting’ of early potatoes.', 'Exposing potato tubers to light|develops shoots|early crop|early harvest|increased yield|reduces incidence of blight', None),
            ('q9b', 'Q9(b)', '4-1', 'grit-in-fowl', 'The presence of grit in the digestive tract of fowl.', 'Fowl have no teeth|gizzard|muscular|(mechanically) grinds food|breaks hard coat|allows digestion', None),
            ('q9c', 'Q9(c)', '3-3-2', 'leatherjackets-after-grass', 'A high incidence of leatherjackets in cereal crops, following grass.', 'Cranefly|active in autumn|lay eggs in tufts of grass|larval stage is leatherjacket|grass and cereal crops are same plant family', None),
            ('q9d', 'Q9(d)', '2-3', 'deep-ploughing-podzol', 'Deep ploughing of a podzol soil.', 'Iron pan|hard or impermeable layer|between A and B horizon|improves drainage|improves aeration|deep ploughing breaks iron pan', '1-5|1-0'),
            ('q9e', 'Q9(e)', '4-3-2', 'nitrogen-in-winter-finishing-slurry', 'The increased nitrogen content of slurry produced by winter‐finishing cattle.', 'Increased concentrates diet|high level of protein|protein digested|amino acids broken down in liver|urea produced|removed from blood by kidneys|excreted in urine', '3-4|1-6')]:
        add(key, ref, topic, concept, 'Give a scientific explanation for: ' + question, [menu(options, [4, 4, 4], 'Any three points, 4 marks each (3(4)).')], why, node=node)
    assert len(p.tasks) == 60, len(p.tasks)
    return p


def reviewed_tasks():
    p = build()
    return p.cards, p.tasks


def paper_review():
    return build().review('60 base tasks, one card each. Question 1 parts are whole where one instruction carries a first-correct scale or a drawing band; '
                          'parts asked and priced separately are separate tasks. Q4(b) carries catalase and amylase as answer routes; Q8(c) is one card for the choice of three pairs from four.')
