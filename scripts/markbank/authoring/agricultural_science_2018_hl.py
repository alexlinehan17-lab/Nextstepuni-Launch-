"""2018 Higher: every task authored from the SEC paper and marking scheme (no cards existed).

All 8 paper pages and 16 scheme pages were inspected and the independent census transcribed
before authoring: 57 base tasks, one card each. Under the scheme's convention (PDF page 4) a
scale such as 4 + 3 + 3 pays the first correct answer 4 and each later one 3, so a Question 1
part whose scale spans its (i) and (ii) is one task stating the scale (orderedSplit); a part
with one pool keeps the steps on its menu. Named-cereal, enzyme and Option One preventative
answers follow the scheme's own routes; the Q8(c) choice of three pairs from four is one card
whose eight members are parts. Answers are the scheme's words.
"""
from agricultural_science_legacy import Paper, P, point, menu, closed, routes

FILE = 'LC024ALP000EV.pdf'
HASHES = {'exampapers': 'c3f4587b9485b694119190e30e5cae7d3ca80f7879252ba1de545f4a6b99e785',
          'markingschemes': '8872670e2cb5e7a56f3894429919359a95db6f9eb34acd36f475418d6c8937de'}
SELECTIONS = {
    '61c124a2fda83e4f': ('exam-selection', 'Six of nine independent examination questions; every question is retained.'),
    '07845e871a47f79c': ('independent-task-selection', 'Q1: six of ten separately priced lettered parts; all ten are retained.'),
    '507447764647264a': ('open', 'Q1(d)(ii): any two factors affecting FCR from the scheme pool; a marking menu.'),
    '86376d9f30a5003a': ('open', 'Q1(i): any three qualities of wool from the scheme pool; a marking menu.'),
    'd9df8a54ee2641fe': ('open', 'Q2(a)(ii): factors for any two horizons of the candidate’s own profile; the scheme gives factors for the O, A, B and C horizons (a marking menu).'),
    'df2254f16cc50d0f': ('open', 'Q2(b)(ii): any two of the scheme’s three texture types (clay, sandy, loam), compared heading by heading; each heading lists all three.'),
    '6b4324667a4d0a6f': ('independent-task-selection', 'Q4: two of four independently priced 24-mark methods; all four are retained.'),
    'f39cd1ef8ac3e423': ('open', 'Q6(a)(i): any two of the scheme’s five reseeding methods with matching descriptions; a marking menu.'),
    '9c1f3d83307c8571': ('independent-task-selection', 'Q8: two of three independently priced 24-mark parts; all three are retained.'),
    '51ef1330be5f3708': ('closed', 'Q8(c): any three of four printed pairs of terms. One card lists the eight members as parts and counts the best six (three pairs).'),
    '37d52e2b68a48a10': ('independent-task-selection', 'Q9: four of five independently priced 12-mark explanations; all five are retained.'),
}
SUPPLEMENTARY = [
    (4, 'Option Two', 'closed', 'Both Q3 options are retained at their own task addresses.'),
    (4, 'Describe the cultivation of a named cereal', 'closed', 'Q3 Option Two (b): the scheme answers for barley, wheat, oats or maize, kept as answer routes on one card.'),
    (5, 'To show the action of a named enzyme', 'closed', 'Q4(c): the scheme answers for amylase or catalase (each name compulsory), kept as answer routes on one card.'),
]
ATLAS = {
    'Q1(a)': 'beef-cattle|dairy-cattle|sheep', 'Q1(b)': 'plant-physiology', 'Q1(c)': 'animal-physiology-reproductive-systems',
    'Q1(d)': 'pigs', 'Q1(e)': 'plant-physiology', 'Q1(f)': 'animal-physiology-digestive-system',
    'Q1(g)': 'animal-physiology-reproductive-systems', 'Q1(h)': 'animal-physiology-reproductive-systems', 'Q1(i)': 'sheep',
    'Q1(j)': 'fertilisers-pollution-environment-cycles', 'Q2': 'soil-science', 'Q2(c)': 'soil-science|scientific-practices-experiments-investigations',
    'Q3 Option One': 'dairy-cattle', 'Q3 Option One (b)': 'dairy-cattle|animal-diseases', 'Q3 Option One (c)': 'beef-cattle|animal-physiology-digestive-system',
    'Q3 Option Two (a)': 'crop-production|animal-diseases', 'Q3 Option Two (b)': 'crop-production', 'Q3 Option Two (c)': 'crop-production',
    'Q4': 'scientific-practices-experiments-investigations', 'Q4(a)': 'scientific-practices-experiments-investigations|grassland',
    'Q4(b)': 'scientific-practices-experiments-investigations|plant-physiology', 'Q4(c)': 'scientific-practices-experiments-investigations|animal-physiology-digestive-system',
    'Q4(d)': 'scientific-practices-experiments-investigations|grassland',
    'Q5': 'sheep', 'Q5(c)': 'sheep|animal-diseases', 'Q6': 'grassland', 'Q6(c)': 'grassland|animal-diseases',
    'Q7': 'genetics', 'Q7(c)': 'genetics|innovation-and-biotechnology-in-agriculture',
    'Q8(a)': 'grassland', 'Q8(b)': 'fertilisers-pollution-environment-cycles|plant-physiology', 'Q8(c)': 'grassland|crop-production|soil-science',
    'Q9(a)': 'fertilisers-pollution-environment-cycles', 'Q9(b)': 'crop-production', 'Q9(c)': 'fertilisers-pollution-environment-cycles',
    'Q9(d)': 'pigs', 'Q9(e)': 'soil-science|grassland',
}
REGIONS = {
    # Drafted by regions.py; hand-trimmed where a last part would run onto the page's [OVER] or the blank back page.
'Q1(a)': (P((2, 0.085, 0.221)), P((5, 0.078, 0.182))),
    'Q1(b)': (P((2, 0.085, 0.135), (2, 0.221, 0.274)), P((5, 0.078, 0.102), (5, 0.182, 0.270))),
    'Q1(c)': (P((2, 0.085, 0.135), (2, 0.274, 0.363)), P((5, 0.078, 0.102), (5, 0.270, 0.350))),
    'Q1(d)': (P((2, 0.085, 0.135), (2, 0.363, 0.415)), P((5, 0.078, 0.102), (5, 0.350, 0.455))),
    'Q1(e)': (P((2, 0.085, 0.135), (2, 0.415, 0.520)), P((5, 0.078, 0.102), (5, 0.455, 0.564))),
    'Q1(f)': (P((2, 0.085, 0.135), (2, 0.520, 0.587)), P((5, 0.078, 0.102), (5, 0.564, 0.640))),
    'Q1(g)': (P((2, 0.085, 0.135), (2, 0.587, 0.674)), P((5, 0.078, 0.102), (5, 0.640, 0.716))),
    'Q1(h)': (P((2, 0.085, 0.135), (2, 0.674, 0.711)), P((5, 0.078, 0.102), (5, 0.716, 0.775))),
    'Q1(i)': (P((2, 0.085, 0.135), (2, 0.711, 0.761)), P((5, 0.078, 0.102), (5, 0.775, 0.845))),
    'Q1(j)': (P((2, 0.085, 0.135), (2, 0.761, 0.853)), P((5, 0.078, 0.102), (5, 0.845, 0.917))),
    'Q2(a)(i)': (P((3, 0.085, 0.104)), P((6, 0.085, 0.193))),
    'Q2(a)(ii)': (P((3, 0.104, 0.154)), P((6, 0.085, 0.103), (6, 0.193, 0.353))),
    'Q2(b)(i)': (P((3, 0.154, 0.173)), P((6, 0.085, 0.103), (6, 0.353, 0.387))),
    'Q2(b)(ii)': (P((3, 0.173, 0.293)), P((6, 0.085, 0.103), (6, 0.387, 0.515))),
    'Q2(c)': (P((3, 0.293, 0.345)), P((6, 0.085, 0.103), (6, 0.515, 0.587))),  # stops before the page's [OVER]
    'Q3 Option One (a)(i)': (P((4, 0.085, 0.139)), P((7, 0.085, 0.143))),
    'Q3 Option One (a)(ii)': (P((4, 0.085, 0.119), (4, 0.139, 0.191)), P((7, 0.085, 0.104), (7, 0.143, 0.195))),
    'Q3 Option One (a)(iii)': (P((4, 0.085, 0.119), (4, 0.191, 0.240)), P((7, 0.085, 0.104), (7, 0.195, 0.336))),
    'Q3 Option One (b)(i)': (P((4, 0.085, 0.119), (4, 0.240, 0.294)), P((7, 0.085, 0.104), (7, 0.336, 0.388))),
    'Q3 Option One (b)(ii)': (P((4, 0.085, 0.119), (4, 0.240, 0.276), (4, 0.294, 0.311)), P((7, 0.085, 0.104), (7, 0.388, 0.405))),
    'Q3 Option One (b)(iii)': (P((4, 0.085, 0.119), (4, 0.240, 0.276), (4, 0.311, 0.344)), P((7, 0.085, 0.104), (7, 0.405, 0.639))),
    'Q3 Option One (c)(i)': (P((4, 0.085, 0.119), (4, 0.344, 0.363)), P((7, 0.085, 0.104), (7, 0.639, 0.691))),
    'Q3 Option One (c)(ii)': (P((4, 0.085, 0.119), (4, 0.363, 0.479)), P((7, 0.085, 0.104), (7, 0.691, 0.728))),
    'Q3 Option Two (a)': (P((4, 0.545, 0.630)), P((8, 0.103, 0.269))),
    'Q3 Option Two (b)': (P((4, 0.545, 0.578), (4, 0.630, 0.735)), P((8, 0.103, 0.121), (8, 0.269, 0.600))),
    'Q3 Option Two (c)(i)': (P((4, 0.545, 0.578), (4, 0.735, 0.754)), P((8, 0.103, 0.121), (8, 0.600, 0.652))),
    'Q3 Option Two (c)(ii)': (P((4, 0.545, 0.578), (4, 0.754, 0.790)), P((8, 0.103, 0.121), (8, 0.652, 0.724))),
    'Q4(a)': (P((5, 0.085, 0.154)), P((9, 0.085, 0.180))),
    'Q4(b)': (P((5, 0.085, 0.119), (5, 0.154, 0.189)), P((9, 0.085, 0.102), (9, 0.180, 0.289))),
    'Q4(c)': (P((5, 0.085, 0.119), (5, 0.189, 0.224)), P((9, 0.085, 0.102), (9, 0.289, 0.513))),
    'Q4(d)': (P((5, 0.085, 0.119), (5, 0.224, 0.356)), P((9, 0.085, 0.102), (9, 0.513, 0.568))),
    'Q5(a)': (P((5, 0.356, 0.391)), P((10, 0.085, 0.264))),
    'Q5(b)': (P((5, 0.391, 0.426)), P((10, 0.085, 0.101), (10, 0.264, 0.341))),
    'Q5(c)': (P((5, 0.426, 0.600)), P((10, 0.085, 0.101), (10, 0.341, 0.549))),  # stops before the page's [OVER]
    'Q6(a)(i)': (P((6, 0.085, 0.104)), P((11, 0.085, 0.296))),
    'Q6(a)(ii)': (P((6, 0.104, 0.121)), P((11, 0.085, 0.101), (11, 0.296, 0.331))),
    'Q6(a)(iii)': (P((6, 0.121, 0.154)), P((11, 0.085, 0.101), (11, 0.331, 0.407))),
    'Q6(b)(i)': (P((6, 0.154, 0.226)), P((11, 0.085, 0.101), (11, 0.407, 0.529))),
    'Q6(b)(ii)': (P((6, 0.154, 0.191), (6, 0.226, 0.259)), P((11, 0.085, 0.101), (11, 0.529, 0.601))),
    'Q6(c)(i)': (P((6, 0.259, 0.330)), P((11, 0.085, 0.101), (11, 0.601, 0.705))),
    'Q6(c)(ii)': (P((6, 0.259, 0.295), (6, 0.330, 0.428)), P((11, 0.085, 0.101), (11, 0.705, 0.742))),
    'Q7(a)(i)': (P((6, 0.428, 0.482)), P((12, 0.085, 0.177))),
    'Q7(a)(ii)': (P((6, 0.428, 0.465), (6, 0.482, 0.499)), P((12, 0.085, 0.103), (12, 0.177, 0.229))),
    'Q7(a)(iii)': (P((6, 0.428, 0.465), (6, 0.499, 0.533)), P((12, 0.085, 0.103), (12, 0.229, 0.310))),
    'Q7(b)': (P((6, 0.533, 0.654)), P((12, 0.085, 0.103), (12, 0.310, 0.689))),
    'Q7(c)(i)': (P((6, 0.654, 0.674)), P((12, 0.085, 0.103), (12, 0.689, 0.740))),
    'Q7(c)(ii)': (P((6, 0.674, 0.727)), P((12, 0.085, 0.103), (12, 0.740, 0.831))),
    'Q8(a)(i)': (P((7, 0.085, 0.156)), P((13, 0.085, 0.174))),
    'Q8(a)(ii)': (P((7, 0.085, 0.118), (7, 0.156, 0.207)), P((13, 0.085, 0.102), (13, 0.174, 0.357))),
    'Q8(b)(i)': (P((7, 0.085, 0.118), (7, 0.207, 0.295)), P((13, 0.085, 0.102), (13, 0.357, 0.545))),
    'Q8(b)(ii)': (P((7, 0.085, 0.118), (7, 0.207, 0.243), (7, 0.295, 0.346)), P((13, 0.085, 0.102), (13, 0.357, 0.372), (13, 0.545, 0.640))),
    'Q8(c)': (P((7, 0.085, 0.118), (7, 0.346, 0.520)), P((13, 0.085, 0.102), (13, 0.640, 0.903))),
    'Q9(a)': (P((7, 0.520, 0.589)), P((14, 0.085, 0.180))),
    'Q9(b)': (P((7, 0.520, 0.555), (7, 0.589, 0.624)), P((14, 0.085, 0.102), (14, 0.180, 0.255))),
    'Q9(c)': (P((7, 0.520, 0.555), (7, 0.624, 0.659)), P((14, 0.085, 0.102), (14, 0.255, 0.314))),
    'Q9(d)': (P((7, 0.520, 0.555), (7, 0.659, 0.694)), P((14, 0.085, 0.102), (14, 0.314, 0.390))),
    'Q9(e)': (P((7, 0.520, 0.555), (7, 0.694, 0.771)), P((14, 0.085, 0.102), (14, 0.390, 0.462))),  # not onto the blank back page
}
FIRST = 'The scheme\'s convention: the first correct answer encountered earns the first value and each later correct answer the next ({}).'


def split(text, note=None):
    """A row of an orderedSplit card: the scheme prices the scale, not the row."""
    return point(text, None, note)


def build():
    p = Paper(2018, 'higher', FILE, HASHES, REGIONS, ATLAS, 8, 16, SELECTIONS, SUPPLEMENTARY,
              section=lambda ref: 'A' if ref.startswith('Q1(') else 'B')
    add = p.add
    six = 'Answer any six of the parts (a) – (j).'
    # Question 1 -------------------------------------------------------------
    add('q1a', 'Q1(a)', '4-3-1', 'livestock-unit', '(i) Explain the term livestock unit. (ii) Give the livestock unit value for: 1. A mature dairy cow 2. A mature sheep.',
        [split('(i) Livestock unit — Amount of feed eaten by a (550 kg) mature cow (or correct number of other farm animals) or equivalent to 12 tonnes of dry matter per annum', FIRST.format('4 + 3 + 3') + ' Three answers.'),
         split('(ii) For mature dairy cow — 1 LU'), split('(ii) For mature sheep — 0.14-0.2 LU')],
        six, marks=10, tariff={'kind': 'orderedSplit', 'notation': '4 + 3 + 3'}, node='3-3')
    add('q1b', 'Q1(b)', '3-1', 'wind-pollinated-flower-diagram', 'Draw a labelled diagram to show the main features of a wind pollinated flower.',
        [point('Drawing to show: feathery stigma and stamens outside flower and no petals (or reduced petals)', None, 'Drawing: 6, 3, 0.', kind='criterion'),
         point('carpel/ stigma/ style/ ovary/ stamen/ anther/ filament/ bracts (or small petals)', None, 'Labels: any four, 1 mark each (4(1)).')],
        six, marks=10, tariff={'kind': 'questionTotal', 'notation': 'D 6, 3, 0 + L 4(1)'}, node='2-0')
    add('q1c', 'Q1(c)', '4-1', 'thyroid-and-adrenal', '(i) State the location in the mammalian body of 1. The thyroid gland 2. The adrenal gland. (ii) Name one hormone secreted by each gland.',
        [split('(i) 1. Thyroid location — Near larynx (or trachea) or in neck', FIRST.format('2(3) + 2(2)') + ' Four answers.'),
         split('(i) 2. Adrenal location — On top of kidney'), split('(ii) 1. Thyroid hormone — Thyroxine or calcitonin'),
         split('(ii) 2. Adrenal hormone — Adrenaline or cortisone or cortisol')],
        six, marks=10, tariff={'kind': 'orderedSplit', 'notation': '2(3) + 2(2)'})
    add('q1d', 'Q1(d)', '4-3-2', 'food-conversion-ratio', '(i) Explain the term food conversion ratio (FCR). (ii) List any two factors that affect FCR in pigs.',
        [split('(i) FCR — Number of kg of feed required to produce 1 kg LWG or ratio of food consumed to liveweight gained', FIRST.format('4 + 3 + 3') + ' Three answers: (i) and two factors.'),
         split('(ii) Factors affecting FCR in pigs — Diet/ breed/ health/ housing or temperature/ management/ age/ sex', 'Any two.')],
        six, marks=10, tariff={'kind': 'orderedSplit', 'notation': '4 + 3 + 3'}, node='3-4')
    add('q1e', 'Q1(e)', '3-1', 'plant-cell-functions', 'Plants are made of different cell types. Give the function of each of the following plant cell types: (i) Xylem (ii) Phloem (iii) Epidermis.',
        [menu(['(i) Xylem: Transport of water (or minerals) or strength or support', '(ii) Phloem: Transport of (named) food or translocation',
               '(iii) Epidermis: Protection against water loss or against infection or prevents damage or regulates gas exchange or boundary or secretes metabolic compounds or root hairs in the epidermis absorb water and minerals'],
              [4, 3, 3], FIRST.format('4 + 3 + 3'))], six, node='2-0')
    add('q1f', 'Q1(f)', '4-1', 'gizzard-and-crop', 'Describe the functions of the following parts of the avian digestive system: (i) The gizzard (ii) The crop.',
        [menu(['(i) Gizzard: Uses grit', 'for physical (or mechanical) digestion or muscular', '(ii) Crop: Storage of food', 'temporarily or for later release for digestion'],
              [4, 3, 3], 'Any three points across the gizzard and the crop. ' + FIRST.format('4 + 3 + 3'))], six)
    add('q1g', 'Q1(g)', '4-1', 'gestation-days', 'Give the length of the gestation period, in days, of (i) Pigs (ii) Sheep (iii) Cows.',
        [menu(['Pig: 113 – 117 days', 'Sheep: 145 – 150 days', 'Cow: 280 – 288 days'], [4, 3, 3], FIRST.format('4 + 3 + 3'))], six)
    add('q1h', 'Q1(h)', '4-1', 'cow-reproductive-system-diagram', 'Draw a labelled diagram of the reproductive system of the cow.',
        [point('Drawing to show: Vagina and uterus and oviduct and ovary', None, 'Drawing: 4, 2, 0.', kind='criterion'),
         point('Vagina/ uterus/ oviduct/ ovary/ cervix', None, 'Labels: any three, 2 marks each (3(2)).')],
        six, marks=10, tariff={'kind': 'questionTotal', 'notation': 'D 4, 2, 0 + L 3(2)'})
    add('q1i', 'Q1(i)', '4-3-1', 'wool-qualities', 'Wool has many qualities that make it useful as a material. List any three of these qualities.',
        [menu('Hard-wearing|lightweight|dirt resistant|ignition resistant|absorbs moisture|mordant (or holds dye well)|(temperature) insulation|flexible', [4, 3, 3],
              'Any three. ' + FIRST.format('4 + 3 + 3'))], six)
    add('q1j', 'Q1(j)', '2-3', 'hedgerow-conservation-reasons', 'Give three reasons why hedgerow conservation is encouraged in Irish agriculture.',
        [menu('Shelter or protect buildings|habitat or wildlife corridor|biodiversity|biosecurity|land division|increase soil (or air) temperature|aesthetic', [4, 3, 3],
              'Any three. ' + FIRST.format('4 + 3 + 3'))], six, node='1-6')
    # Question 2 -------------------------------------------------------------
    add('q2ai', 'Q2(a)(i)', '2-1', 'soil-profile-diagram', 'Draw a labelled diagram of the soil profile of a named soil type.',
        [point('Soil type — Name of soil type', None, '3 marks.'),
         point('At least three horizons which must match the named soil type', None, 'Drawing: 4, 2, 0.', kind='criterion'),
         point('Any three valid labels for named soil type', None, 'Labels: 3(1).')],
        marks=10, tariff={'kind': 'questionTotal', 'notation': '3 + D 4, 2, 0 + L 3(1)'}, node='1-0')
    add('q2aii', 'Q2(a)(ii)', '2-1', 'horizon-forming-factors', 'Outline the factors responsible for creating any two of the soil horizons shown.',
        [menu(['O horizon: waterlogging or anaerobic conditions or low pH or build-up of organic material',
               'A horizon: activity of soil animals (or plant roots) or presence of humus (or organic matter)',
               'B horizon: leaching of nutrients or build-up of nutrients from the A (horizon) or less organic matter (or humus)',
               'C horizon: weathering of parent rock'], [3, 3], 'Correct factors for two horizons (particular rather than general), 3 marks each (2(3)).')],
        'Draw a labelled diagram of the soil profile of a named soil type.', node='1-0')
    add('q2bi', 'Q2(b)(i)', '2-2-2', 'soil-texture-meaning', 'Explain the term soil texture.',
        [point('Relative proportions of different particles in a soil or sand, silt and clay by %', 4)], node='1-3')
    texture = [('1. Fertility', 'High / Low / High'), ('2. Temperature', 'Low / High / High'), ('3. Drainage', 'Poor / Good / Good'), ('4. Ease of tilling', 'Poor / Good / Good')]
    add('q2bii', 'Q2(b)(ii)', '2-2-2', 'comparing-texture-types',
        'Name any two soil texture types and compare them under the following headings: 1. Fertility 2. Temperature 3. Drainage 4. Ease of tilling.',
        [point(f'{heading} (clay / sandy / loam) — {values}', 4,
               'Each heading 2 + 2: one mark pair for each of your two types (4(2 + 2)). The scheme tabulates clay, sandy and loam in that order.' if i == 0 else None)
         for i, (heading, values) in enumerate(texture)], node='1-3')
    add('q2c', 'Q2(c)', '2-2-3', 'earthworm-activity-experiment', 'Describe an experiment to show the activity of earthworms in the soil.',
        [menu('Wormery|layers (or sand, chalk, clay)|organic matter on top|add worms|cover|leave in a cool place|keep moist|minimum of a week|control|correct result', [2] * 6,
              'Any six, 2 marks each (6(2)).')], node='1-4|0-1')
    # Question 3 -------------------------------------------------------------
    add('q3o1ai', 'Q3 Option One (a)(i)', '4-3-2', 'body-condition-score', 'Explain the term body condition score (BCS).',
        [point('Assessment of level of fat reserves in an animal’s body or lean-to-fat ratio', 4)], node='3-4')
    add('q3o1aii', 'Q3 Option One (a)(ii)', '4-3-2', 'optimum-bcs', 'State the optimum BCS of a dairy cow at 1. Calving 2. Mating.',
        [point('At calving — BCS 3.0 – 3.5', 3), point('At mating — BCS 2.5 – 3.0', 3)], node='3-4')
    add('q3o1aiii', 'Q3 Option One (a)(iii)', '4-3-2', 'off-target-bcs', 'Explain the possible consequences of an animal not being at the optimum BCS at these times.',
        [point('At calving — BCS low: small calf or reduced milk yield or metabolic diseases or BCS high: calving difficulty', 3),
         point('At mating — BCS low: irregular heat pattern or poor conception rate or metabolic diseases', 3)], 'State the optimum BCS of a dairy cow at 1. Calving 2. Mating.', node='3-4')
    cows = 'Dairy cows can be affected by both bacterial diseases and metabolic deficiency disorders.'
    add('q3o1bi', 'Q3 Option One (b)(i)', '4-3-3', 'bacterial-diseases-dairy', 'Give two examples of bacterial diseases that can affect dairy cows.',
        [menu('TB|brucellosis|mastitis|leptospirosis|blackleg|Johne’s disease|anthrax|bacterial pneumonia|foot rot|(bovine) conjunctivitis (or pink eye)', [2, 2], 'Any two, 2 marks each (2(2)).')], cows, node='3-5')
    add('q3o1bii', 'Q3 Option One (b)(ii)', '4-3-3', 'deficiency-disorders-dairy', 'Give two examples of deficiency disorders that can affect dairy cows.',
        [menu('Milk fever|grass tetany', [2, 2], 'Any two, 2 marks each (2(2)); the scheme gives these as examples.')], cows, node='3-5')
    add('q3o1biii', 'Q3 Option One (b)(iii)', '4-3-3', 'preventing-dairy-diseases', 'Describe a preventative measure for each example.',
        [menu(['TB or Brucellosis: Closed herd or biosecurity or fencing or culling or testing', 'Mastitis: Hygiene or fly control or dry cow treatment or culling',
               'Blackleg or bacterial pneumonia or leptospirosis: Vaccination or hygiene', 'Foot rot: Foot bath or paring', 'Johne’s disease: Culling or do not mix colostrum',
               'Anthrax: Culling', 'Pink eye: Vaccination or fly control',
               'Milk fever: (Dairy) ration or minerals or licks or bolus or adding minerals to water or pasture dressing or correct BCS at calving',
               'Grass tetany: Bolus or licks or (dairy) ration or adding Mg soln. to water or avoid fresh grass and clover'], [2] * 4,
              'Four measures to match the diseases and disorders given in (i) and (ii), 2 marks each (4(2)).')], cows, node='3-5')
    add('q3o1ci', 'Q3 Option One (c)(i)', '4-3-2', 'beef-calf-diet-changes', 'Describe the changes in the diet of a beef calf, from birth to weaning.',
        [point('Colostrum [compulsory]', 3, 'Colostrum plus any other three, all in correct order, 3 marks each (4(3)).'),
         menu('milk|milk replacer|concentrates|hay|grass', [3, 3, 3], 'Any other three, in the correct order after colostrum.')], node='3-4')
    add('q3o1cii', 'Q3 Option One (c)(ii)', '4-1', 'rumen-development', 'Explain how these changes affect the development of the ruminant stomach.',
        [point('Hay or concentrate', 2, '2(2).'), point('develops rumen flora or scratch factor', 2)], 'Describe the changes in the diet of a beef calf, from birth to weaning.', node='3-0')
    add('q3o2a', 'Q3 Option Two (a)', '3-3-2', 'potato-blight-life-cycle', 'Describe with the aid of a labelled diagram the life cycle of a named fungus that affects the potato plant.',
        [point('Name of fungus — Phytophthora infestans or potato blight (fungus)', 2),
         point('Drawing of life cycle to feature: A leaf TS with a sporangiophore emerging from a stoma, and at least one labelled hypha or haustorium or sporangium or zoospore', 4, '4 or 0.'),
         menu('Haustoria absorb food (from cells)|sporangiophores grow out of stomata|sporangia break off|(sporangia become) airborne|onto soil|(sporangia) germinate in humid conditions (or develop into conidium if dry)|produce zoospores|infect tubers or growing plants',
              [2] * 5, 'Description: any five, 2 marks each (5(2)).')], node='2-4')
    cereals = [('barley', 'Barley', 'pH 6 – 6.5|fertile|sandy loam or free draining|brown earth or grey-brown podzolic', None, 'July - September', '6 – 8 t/ ha for spring or 8 – 9 t/ ha for winter'),
               ('wheat', 'Wheat', 'pH 5 – 7|soil as for barley', 'As for barley', 'July - Sept.', '7 – 8 t/ ha for spring or 9 – 11 t/ ha for winter'),
               ('oats', 'Oats', 'pH 5.5|soil as for barley', 'As for barley', 'July - Sept.', '6 – 7 t/ ha for spring or 7 – 8 t/ ha for winter'),
               ('maize', 'Maize', 'pH 6.6 – 7|soil as for barley', 'As for barley', 'July - Sept.', '15 – 20 t/ ha of dry matter')]
    built = []
    for slug, label, soil, climate, harvest, yld in cereals:
        rows = [point(f'Named cereal — {label}', 2, 'Name 2.'),
                menu(soil, [2, 2], '(i) Soil requirements, 2(2).' + (' The scheme gives barley\'s soil as fertile/ sandy loam or free draining/ brown earth or grey-brown podzolic.' if slug != 'barley' else ''))]
        rows.append(menu('Warm|moist|dry or sunshine', [2, 2], '(ii) Climate, 2(2).') if climate is None else
                    point(f'(ii) Climate — {climate}', 4, '2(2). The scheme gives barley\'s climate: warm/ moist/ dry or sunshine.'))
        rows += [point(f'(iii) Harvest date — {harvest}', 3), point(f'(iv) Yield — {yld}', 3)]
        built.append((slug, label, rows))
    rows, variants = routes(built)
    add('q3o2b', 'Q3 Option Two (b)', '3-3-1', 'named-cereal-cultivation',
        'Describe the cultivation of a named cereal under the following headings: (i) Soil requirements (ii) Climate (iii) Harvest date (iv) Yield.', rows,
        selection=closed(1, [label for _, label, *_ in cereals]), node='2-3|2-5', extra={'answerVariants': variants})
    add('q3o2ci', 'Q3 Option Two (c)(i)', '3-3-2', 'indirect-weed-control', 'Explain what is meant by indirect control of weeds in crops.',
        [point('Any method of control that is effective despite not being targeted at the affected species (accept a method that does not use chemicals)', 4)], node='2-4')
    add('q3o2cii', 'Q3 Option Two (c)(ii)', '3-3-2', 'indirect-weed-control-examples', 'Give four examples of such indirect control.',
        [menu('Crop rotation|growth encouragement|stubble cleaning|aggressive crop varieties|early harvest|ploughing|use certified seeds|catch crop|earthing up', [3] * 4,
              'Any four, 3 marks each (4(3)).')], 'Explain what is meant by indirect control of weeds in crops.', node='2-4')
    # Question 4 -------------------------------------------------------------
    lab = 'In the case of any two of the following describe a laboratory or field method.'
    add('q4a', 'Q4(a)', '3-3-3', 'grass-sugar-percentage', 'Describe a laboratory or field method to determine the percentage (%) sugar in a sample of grass.',
        [menu('Dry grass sample|chop|freezer bag|roll or remove air|freeze|squeeze or collect sap|refractometer|read % from scale|repeat (to establish statistical significance)', [4] * 6,
              'Any six, 4 marks each (6(4)).')], lab, node='2-6|0-1')
    add('q4b', 'Q4(b)', '3-1', 'shading-and-crop-growth', 'Describe a laboratory or field method to show the effect of shading on crop growth.',
        [menu('1 m2 (plots or other measured areas) or transect(s)|one shaded and one unshaded|sow crop seeds or established crop|similar (or named) conditions|leave for a time appropriate for crop|harvest or measure|compare yields (or growth differences)|correct result|repeat (to establish statistical significance)',
              [4] * 6, 'Any six, 4 marks each (6(4)).')], lab, node='2-0|0-1')
    enzymes = [('amylase', 'Amylase', 'two test tubes|add equal amounts of starch solution (to each)|add amylase to one|other is control|waterbath at 37 °C|at least 5 min.|add iodine|negative for starch|Benedict’s or Fehling’s|positive (or brick red) for reducing sugar|repeat (to establish statistical significance)'),
               ('catalase', 'Catalase', 'fresh liver sample (or celery or potato or other suitable source)|one cubed, one chopped, one boiled|add a few drops of washing-up liquid to each|use buffer solution|add equal amounts of hydrogen peroxide|compare number of bubbles produced (or height of foam)|catalase breaks down hydrogen peroxide|high temperature denatures catalase|repeat (to establish statistical significance)')]
    rows, variants = routes([(slug, label, [point(f'{label} [compulsory]', 4, 'Enzyme name plus any other five, 4 marks each (6(4)).'), menu(steps, [4] * 5, f'{label}: any five other points.')])
                             for slug, label, steps in enzymes])
    add('q4c', 'Q4(c)', '4-1', 'named-enzyme-action', 'Describe a laboratory or field method to show the action of a named enzyme.', rows, lab,
        selection=closed(1, ['Amylase', 'Catalase']), node='3-0|0-1', extra={'answerVariants': variants})
    add('q4d', 'Q4(d)', '3-3-2', 'botanical-composition', 'Describe a laboratory or field method to compare the botanical composition of an old pasture and a newly sown pasture.',
        [menu('Quadrat|random|record plants|repeat (x 10)|repeat for other pasture|identification key|frequency|compare|sample results', [4] * 6, 'Any six, 4 marks each (6(4)).')],
        lab, node='2-6|0-1')
    # Question 5 -------------------------------------------------------------
    add('q5a', 'Q5(a)', '4-3-1', 'hill-versus-lowland-sheep', 'Compare mountain/ hill sheep production with lowland sheep production.',
        [menu(['Extensive (or low) stocking rate / Intensive (or high) stocking rate', 'Low production / Higher production', 'Rough grazing / Better grazing',
               'High mortality / Lower mortality', 'Single lambs / More than one lamb', 'Breed example / Breed example', 'Low labour / High labour'], [4] * 4,
              'Any four comparisons, each 2 + 2: the mountain/ hill point and its lowland counterpart (4(2 + 2)).')], node='3-3')
    add('q5b', 'Q5(b)', '4-3-3', 'lambing-management', 'Describe the management practices used by sheep farmers at lambing time.',
        [menu('Housing|feeding concentrates|supervision (or assistance)|lambing pens|colostrum|fostering|infra-red lamp|iodine on navel cord or other point of disease control (or hygiene)', [4] * 4,
              'Any four, 4 marks each (4(4)).')], node='3-5')
    add('q5c', 'Q5(c)', '4-3-3', 'sheep-welfare-scheme',
        'Many Irish sheep farmers now take part in the Sheep Welfare Scheme. Three of the features of this scheme are lameness control, flystrike control and scanning of in-lamb ewes. For each of the above explain (i) How it is carried out (ii) The benefit to overall production in the flock.',
        [point('(i) Methods, lameness control — Regular checking or footbath or antibiotic spray or paring hooves or vaccination', None,
               'The scheme\'s convention: the first correct answers earn the higher award (4(3) + 2(2)). Six answers: a method and a benefit for each feature.'),
         point('(i) Methods, flystrike control — Dipping or pour-on or shearing or dagging or tail docking', None),
         point('(i) Methods, scanning in-lamb ewes — Ultrasound scanner or scanner placed on abdomen', None),
         point('(ii) Benefits, lameness control — Increased production levels or more constant grazing', None),
         point('(ii) Benefits, flystrike control — Increased production or more constant grazing or lower mortality rates', None),
         point('(ii) Benefits, scanning in-lamb ewes — Identify multiple births or allow for correct feeding levels or helps to prevent twin-lamb disease or identify barren ewes', None)],
        marks=16, tariff={'kind': 'orderedSplit', 'notation': '4(3) + 2(2)'}, node='3-5|3-4')
    # Question 6 -------------------------------------------------------------
    add('q6ai', 'Q6(a)(i)', '3-3-1', 'reseeding-methods', 'Describe any two commonly used methods of reseeding grassland.',
        [menu('Direct sowing|Stitching in|Undersowing|Direct drilling|Slurry seeding', [2, 2], 'Any two method names, 2 marks each (2(2)).'),
         menu(['Direct sowing: total herbicide applied/ ploughed/ fine seed bed/ seeds sown by drill or broadcast/ chain harrow/ fertilise',
               'Stitching in: old grassland not killed (or not checked back)/ slit made in land/ grass seeds sown by drill/ fertilise',
               'Undersowing: land is ploughed (or tilled)/ grass seeds sown with tillage crop (or nurse crop)/ nurse crop harvested/ grassland establishes',
               'Direct drilling: grass killed off/ fertiliser and slug pellets drilled in with grass seed/ used in soil subject to poaching (or shallow or stony soils)',
               'Slurry seeding: seeds drilled into ground/ slurry is applied during or after sowing/ successful with adequate rainfall'], [4, 4],
              'Matching descriptions 2(2 + 2): two points, 2 marks each, describing each of your two methods.')], node='2-6')
    sward = 'Describe any two commonly used methods of reseeding grassland.'
    add('q6aii', 'Q6(a)(ii)', '3-3-1', 'grass-establishment', 'Explain the term establishment in the context of newly-sown grass.',
        [point('Progression from emerged seedlings to thick grass sward', 4)], sward, node='2-6')
    add('q6aiii', 'Q6(a)(iii)', '3-3-1', 'successful-establishment', 'Describe two practices that contribute to successful establishment.',
        [menu('Tillering|grazing with light stock or topping or rolling|manure (or fertiliser) application|weed control|use certified seed|use productive (or named) grass species', [2, 2],
              'Any two, 2 marks each (2(2)).')], sward, node='2-6')
    rye = 'Perennial ryegrass (PRG) and Italian ryegrass (IRG) are commonly sown in Irish grassland.'
    add('q6bi', 'Q6(b)(i)', '3-2', 'prg-versus-irg', 'Compare features of perennial ryegrass and Italian ryegrass that contribute to their productivity.',
        [menu(['Tillers vigorously / Tillers less vigorously', 'Aggressive / Less aggressive', 'Persistent / Less persistent', 'Fast-growing / Faster than PRG',
               'Long growing season / Longer growing season'], [4] * 3, 'Any three comparisons, each 2 + 2: the PRG feature and the IRG feature (3(2 + 2)).')], rye, node='2-6|2-1')
    add('q6bii', 'Q6(b)(ii)', '3-2', 'hybrid-grasses', 'Explain the term hybrid grasses and suggest why they might be used.',
        [point('What are they — Result of crossing of different species e.g. PRG and IRG', 2), point('Why use them — Hybrid vigour or best qualities of crossed species combined', 2)], rye, node='2-6')
    para = 'Poor grassland management can contribute to an increase in the number of parasites that affect cattle.'
    add('q6ci', 'Q6(c)(i)', '4-3-3', 'grassland-parasite-control', 'Explain how improved grassland management may prevent this happening.',
        [menu('Rotational grazing (or mixed grazing or leader-follower grazing) disturbs parasite life cycle|reseeding disturbs parasite lifecycle|scrub removal (or topping) removes parasite habitat|draining (or fencing off) wet land disturbs the life cycle of the liver fluke|liming disturbs life cycle of liver fluke',
              [3, 3], 'Any two, 3 marks each (2(3)).')], para, node='3-5|2-6')
    add('q6cii', 'Q6(c)(ii)', '4-3-3', 'cattle-parasites', 'Name two such parasites.',
        [menu('Stomach worms|lung worms|ticks|liver fluke', [3, 3], 'Any two, 3 marks each (2(3)).')], para, node='3-5')
    # Question 7 -------------------------------------------------------------
    concepts = 'Explain each of the following agriculturally relevant concepts in genetics and give an appropriate example in each case.'
    for key, ref, concept, term, explain, example in [
            ('q7ai', 'Q7(a)(i)', 'polyploidy', 'Polyploidy', '(Cells with) more than two sets of chromosomes (or 3n or higher)', 'Wheat or strawberry plants or grasses (or named grasses) or beet or endosperm (tissue) or 3n (or higher)'),
            ('q7aii', 'Q7(a)(ii)', 'freemartin', 'Freemartin condition', 'Infertility in some female animals with a male twin', 'Calves'),
            ('q7aiii', 'Q7(a)(iii)', 'micropropagation', 'Micropropagation', 'Plant tissue grown to produce clone(s) (or to produce plants identical to the parent)', 'Seed potato propagation')]:
        add(key, ref, '4-1', concept, f'Explain the concept and give an appropriate example: {term}.',
            [point(f'Explain — {explain}', 3, '3 + 2.'), point(f'Example — {example}', 2)], concepts, node='3-6')
    add('q7b', 'Q7(b)', '4-1', 'drosophila-dihybrid-cross', 'Outline the details of the cross between two flies, heterozygous for both conditions.',
        [point('Parental genotype — GgNn', 2),
         point('Gamete genotypes, across and down — GN Gn gN gn', 4, '2 or 0 across, 2 or 0 down.'),
         point('Offspring genotypes grid', 4, '4 or 0: the grid gives GGNN, GGNn, GgNN, GgNn, GGnn, Ggnn, ggNN, ggNn and ggnn across its sixteen boxes.'),
         menu(['Grey colour, normal antennae', 'Grey colour, twisted antennae', 'Ebony colour, normal antennae', 'Ebony colour, twisted antennae'], [1] * 4, 'Offspring phenotypes, 4(1).'),
         point('Matching ratio [2 = correct ratio not matched to phenotypes] — Grey colour, normal antennae 9; Grey colour, twisted antennae 3; Ebony colour, normal antennae 3; Ebony colour, twisted antennae 1', 4,
               'Matching ratio 4, 2, 0: 4 when the ratio is matched to the phenotypes, 2 for a correct ratio not matched to them. The scheme allows correct fractions or decimals or percentages in place of 9, 3, 3, 1.')],
        'Drosophila melanogaster is a species of fruit fly commonly used in genetic research. The normal body colour of such flies is grey (GG). A recessive ebony body (gg) is also possible. The flies’ antennae can be normal (NN), or twisted (nn), which is a recessive condition.',
        node='3-6')
    add('q7ci', 'Q7(c)(i)', '4-1', 'embryo-transfer', 'Explain what is meant by embryo transfer in farm animals.',
        [point('Embryos from one (or donor) animal', 3, '2(3).'), point('implanted into surrogate (or other animal)', 3)], node='3-6')
    add('q7cii', 'Q7(c)(ii)', '4-1', 'embryo-transfer-benefits', 'Give three benefits of embryo transfer.',
        [menu('More offspring from superior (stock)|genetic improvement|produces replacement stock|reduces pregnancy stress on superior animal|allows import and export of embryos|(allows) beef (production) in dairy enterprise|decreases time for genetic improvement',
              [3] * 3, 'Any three, 3 marks each (3(3)).')], 'Explain what is meant by embryo transfer in farm animals.', node='3-6')
    # Question 8 -------------------------------------------------------------
    twoof = 'Answer any two of the parts (a), (b), (c).'
    add('q8ai', 'Q8(a)(i)', '3-3-3', 'grass-to-silage-processes', 'Describe the main processes at work during the conversion of grass to silage.',
        [menu('Anaerobic conditions|Lactobacillus species|fermentation|carbohydrates in grass|converted to (weak) acids|lowers pH|kills bacteria|grass preserved', [3] * 4, 'Any four, 3 marks each (4(3)).')],
        twoof, node='2-6')
    add('q8aii', 'Q8(a)(ii)', '3-3-3', 'silage-steps-and-processes', 'Relate three practical steps in the making of good quality silage to the processes above.',
        [menu(['Cut grass when dry to have increased carbohydrate in grass', 'cut at correct heading-out stage to encourage lactic acid (or weak acid) production',
               'cut in the afternoon to take advantage of maximum photosynthesis (or to increase carbohydrate)',
               'double (or precision) chopping (of grass) to increase surface area (or for greater bacterial access (or activity) or to release more sugars)',
               'roll well to expel air (or to provide anaerobic conditions)', 'seal tightly to exclude air (or to provide anaerobic conditions)',
               'additives to increase carbohydrate', 'wilting to increase carbohydrate concentration'], [4] * 3, 'Any three, 4 marks each (3(4)).')], twoof, node='2-6')
    npk = 'Three of the major elements needed for good plant growth are nitrogen (N), phosphorus (P), and potassium (K).'
    add('q8bi', 'Q8(b)(i)', '2-3', 'npk-functions-and-deficiencies', 'In the case of each element describe 1. Its function in the plant 2. A deficiency symptom.',
        [point('N: Function — Chlorophyll or protein or leafy growth', 2), point('N: Deficiency symptom — Slow growth or low yield or pale green colour or yellowing of leaves', 2),
         point('P: Function — Root growth or reproduction or flower or seed formation', 2), point('P: Deficiency symptom — Stunted growth or low yield or blue colour on leaves or lack of flowers', 2),
         point('K: Function — Protein or translocation or disease resistance or seed (or fruit) formation', 2),
         point('K: Deficiency symptom — Reduced yield or poor growth or scorching of leaves or lodging or poor root development', 2)], npk, node='1-6|2-0')
    add('q8bii', 'Q8(b)(ii)', '2-3', 'deficiency-experiment', 'Describe a laboratory experiment to show the effect of the deficiency of a particular element in a plant.',
        [menu('Sterilise test tubes or containers|seedlings in two tubes|tablet minus nutrient|tablet complete|aeration|similar conditions|cover to prevent algae|leave for a minimum of two weeks|measure or compare|correct result',
              [2] * 6, 'Any six, 2 marks each (6(2)).')], npk, node='2-0|0-1')
    members = [('i', 'Zero grazing', 'animals are indoors or enclosed|grass is cut to be brought in for feed'),
               ('i', 'Strip grazing', 'Allowing animals access a fresh strip of grass or forage crop daily|moveable fence'),
               ('ii', 'Contact fungicides', 'Kill fungi they touch|fast acting|more coverage needed'),
               ('ii', 'Systemic fungicides', 'Absorbed into plant|translocated to all parts|slow acting|less coverage needed'),
               ('iii', 'First early potatoes', 'Harvested immature in June|sown in early spring|low yield|sprouted|grown in coastal regions (or under plastic)'),
               ('iii', 'Maincrop potatoes', 'Sown in late spring|harvested fully mature in autumn|high yield'),
               ('iv', 'Abiotic factors', 'Non- living factors|in a habitat'), ('iv', 'Edaphic factors', 'Soil factors|in a habitat')]
    add('q8c', 'Q8(c)', '3-3-2', 'distinguishing-paired-terms',
        'Distinguish clearly between the members of any three of the following pairs of terms: (i) Zero grazing and strip grazing (ii) Contact fungicides and systemic fungicides (iii) First early potatoes and maincrop potatoes (iv) Abiotic factors and edaphic factors.',
        [menu(pool, [2, 2], f'({k}) {label}: two points, 2(2).' + (' Any three pairs: both members of each, 2(2) per member.' if i == 0 else ''))
         for i, (k, label, pool) in enumerate(members)],
        twoof, marks=24, tariff={'kind': 'bestNofParts', 'answer': 6, 'ofParts': 8, 'perPart': 4},
        selection=closed(3, ['i', 'ii', 'iii', 'iv']), node='2-6|2-4|1-0')
    # Question 9 -------------------------------------------------------------
    why = 'Give scientific explanations for any four of the following.'
    for key, ref, topic, concept, item, points, node in [
            ('q9a', 'Q9(a)', '2-3', 'trailing-shoe', 'Use of a trailing shoe in slurry spreading.', 'Slurry in narrow bands on surface|reduces N loss to atmosphere|less smell|environmentally friendly (or complies with farm schemes)|reduces volatilisation|early return to grazing', '1-6'),
            ('q9b', 'Q9(b)', '3-3-2', 'thinning-forest-trees', 'Trees in a forest plantation are thinned at various time intervals.', 'Poorest (or diseased or damaged) trees removed|reduces competition|remaining trees grow faster|improves tree quality|improves size of trees|income from thinnings', None),
            ('q9c', 'Q9(c)', '2-3', 'summer-algal-bloom', 'Algal bloom in waterways following rainfall in summer.', 'Eutrophication (or nutrient enrichment)|run-off (or leaching)|slurry (or silage effluent or fertiliser)|rivers low|warm water', '1-6'),
            ('q9d', 'Q9(d)', '4-3-1', 'farrowing-crate', 'Use of a farrowing crate in pig production.', 'Restricts sow movement|prevents crushing of bonhams|ease of suckling|bonhams can access creep area or higher temperature|better survival rates', None),
            ('q9e', 'Q9(e)', '2-3', 'rushes-on-gley', 'Growth of rushes in grassland over gley soils.', 'Impeded drainage|high water table|rushes grow well in poorly-drained land|temporary inaccessibility of land for spraying (or for topping)|cold soil means less competition from other plants', '1-5|2-6')]:
        add(key, ref, topic, concept, 'Give a scientific explanation for: ' + item, [menu(points, [4, 4, 4], 'Any three points, 4 marks each (3(4)).')], why, node=node)
    assert len(p.tasks) == 57, len(p.tasks)
    return p


def reviewed_tasks():
    p = build()
    return p.cards, p.tasks


def paper_review():
    return build().review('57 base tasks, one card each. A scale the scheme prints across a part\'s (i) and (ii) (Q1(a), (c), (d); Q5(c)) is one task with the scale stated; '
                          'parts priced separately are separate tasks. Q3 Option Two (b) cereals and Q4(c) enzymes are answer routes; Q8(c) is one card for the choice of three pairs from four.')
