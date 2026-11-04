"""2017 Higher: every task authored from the SEC paper and marking scheme (no cards existed).

All 8 paper pages and 20 scheme pages were inspected and the independent census transcribed
before authoring: 58 base tasks, one card each. Under the scheme's convention (PDF page 4) a
scale such as 6 + 3 + 1 pays the first correct answer 6 and each later one the next value, so a
Question 1 part whose scale spans its (i) and (ii) is one task stating the scale (orderedSplit);
a part with one pool keeps the steps on its menu. Method answers (Q4(a), Q4(b), Q5(a)(ii)) and
the named cereal (Q3 Option Two (b)) are answer routes; the Q8(c) choice of three pairs from four
is one card whose eight members are parts. Answers are the scheme's words.
"""
from agricultural_science_legacy import Paper, P, point, menu, closed, routes

FILE = 'LC024ALP000EV.pdf'
HASHES = {'exampapers': 'f8f371d593303ab2cf6b5ebb216be59009e8b2e90f54e1ddafd85e033efe3fe6',
          'markingschemes': 'b58e95e957390478fb1eb0654b95b8b1cea59c5cbbefd8871ea5b43266c0ad40'}
SELECTIONS = {
    '07c959f16d7f8e85': ('exam-selection', 'Six of nine independent examination questions; every question is retained.'),
    '977236632ed1560c': ('independent-task-selection', 'Q1: six of ten separately priced lettered parts; all ten are retained.'),
    'eb8d9a835963f21b': ('independent-task-selection', 'Q4: two of four independently priced 24-mark methods; all four are retained.'),
    '9f30ad8295679c77': ('closed', 'Q5(a)(ii): any one quantitative milk test. The scheme describes each test, kept as answer routes on one card.'),
    '8f043bb6e203c388': ('independent-task-selection', 'Q8: two of three independently priced 24-mark parts; all three are retained.'),
    '2f64a64ba040b797': ('open', 'Q8(b)(ii): any two insect pests with their damage; the scheme gives two examples (a marking menu).'),
    'ab6b026e92d18fa2': ('closed', 'Q8(c): any three of four printed pairs of terms. One card lists the eight members as parts and counts the best six (three pairs).'),
    'cdba7f87d55816fd': ('independent-task-selection', 'Q9: four of five independently priced 12-mark explanations; all five are retained.'),
}
SUPPLEMENTARY = [
    (3, 'Option Two', 'closed', 'Both Q3 options are retained at their own task addresses.'),
    (3, 'Describe the cultivation of a named cereal crop', 'closed', 'Q3 Option Two (b): the scheme gives a yield for barley, wheat, oats or maize, kept as answer routes on one card.'),
    (4, 'To compare the digestibility of whole and rolled cereal grains', 'closed', 'Q4(a): the scheme gives a feeding method OR a test-tube method, kept as answer routes on one card.'),
    (4, 'To determine the quality of silage in a pit or bale', 'closed', 'Q4(b): the scheme gives four methods, kept as answer routes on one card.'),
]
ATLAS = {
    'Q1(a)': 'grassland', 'Q1(b)': 'crop-production', 'Q1(c)': 'plant-physiology|classification-of-animals-plants', 'Q1(d)': 'soil-science',
    'Q1(e)': 'animal-physiology-digestive-system', 'Q1(f)': 'plant-physiology', 'Q1(g)': 'animal-physiology-digestive-system|sheep|pigs',
    'Q1(h)': 'soil-science|grassland', 'Q1(i)': 'dairy-cattle', 'Q1(j)': 'animal-physiology-reproductive-systems',
    'Q2': 'soil-science', 'Q2(c)': 'soil-science|scientific-practices-experiments-investigations',
    'Q3 Option One': 'beef-cattle', 'Q3 Option One (c)': 'fertilisers-pollution-environment-cycles|beef-cattle',
    'Q3 Option Two': 'crop-production', 'Q4': 'scientific-practices-experiments-investigations',
    'Q4(a)': 'scientific-practices-experiments-investigations|animal-physiology-digestive-system', 'Q4(b)': 'scientific-practices-experiments-investigations|grassland',
    'Q4(c)': 'scientific-practices-experiments-investigations|soil-science', 'Q4(d)': 'scientific-practices-experiments-investigations|plant-physiology',
    'Q5(a)': 'dairy-cattle', 'Q5(a)(ii)': 'dairy-cattle|scientific-practices-experiments-investigations', 'Q5(b)': 'sheep', 'Q5(c)': 'beef-cattle',
    'Q6': 'grassland', 'Q6(c)': 'animal-physiology-digestive-system|grassland',
    'Q7(a)': 'genetics|beef-cattle', 'Q7(b)': 'genetics', 'Q7(c)': 'genetics',
    'Q8(a)': 'fertilisers-pollution-environment-cycles', 'Q8(b)': 'classification-of-animals-plants|crop-production|animal-diseases',
    'Q8(c)': 'sheep|soil-science|animal-diseases|crop-production',
    'Q9(a)': 'pigs', 'Q9(b)': 'crop-production', 'Q9(c)': 'soil-science', 'Q9(d)': 'animal-physiology-digestive-system', 'Q9(e)': 'soil-science',
}
REGIONS = {
    # Drafted by regions.py.
'Q1(a)': (P((2, 0.057, 0.159)), P((5, 0.081, 0.288))),
    'Q1(b)': (P((2, 0.057, 0.090), (2, 0.159, 0.214)), P((5, 0.081, 0.102), (5, 0.288, 0.410))),
    'Q1(c)': (P((2, 0.057, 0.090), (2, 0.214, 0.283)), P((5, 0.081, 0.102), (5, 0.410, 0.600))),
    'Q1(d)': (P((2, 0.057, 0.090), (2, 0.283, 0.368)), P((5, 0.081, 0.102), (5, 0.600, 0.672))),
    'Q1(e)': (P((2, 0.057, 0.090), (2, 0.368, 0.403)), P((5, 0.081, 0.102), (5, 0.672, 0.730))),
    'Q1(f)': (P((2, 0.057, 0.090), (2, 0.403, 0.438)), P((5, 0.081, 0.102), (5, 0.730, 0.844))),
    'Q1(g)': (P((2, 0.057, 0.090), (2, 0.438, 0.510)), P((5, 0.081, 0.102), (6, 0.079, 0.221))),
    'Q1(h)': (P((2, 0.057, 0.090), (2, 0.510, 0.579)), P((5, 0.081, 0.102), (6, 0.221, 0.292))),
    'Q1(i)': (P((2, 0.057, 0.090), (2, 0.579, 0.666)), P((5, 0.081, 0.102), (6, 0.292, 0.397))),
    'Q1(j)': (P((2, 0.057, 0.090), (2, 0.666, 0.770)), P((5, 0.081, 0.102), (6, 0.397, 0.577))),
    'Q2(a)(i)': (P((2, 0.770, 0.807)), P((7, 0.081, 0.204))),
    'Q2(a)(ii)': (P((2, 0.770, 0.789), (2, 0.807, 0.840)), P((7, 0.081, 0.102), (7, 0.204, 0.296))),
    'Q2(b)(i)': (P((2, 0.840, 0.859)), P((7, 0.081, 0.102), (7, 0.296, 0.363))),
    'Q2(b)(ii)': (P((2, 0.859, 0.876)), P((7, 0.081, 0.102), (7, 0.363, 0.473))),
    'Q2(b)(iii)': (P((2, 0.876, 0.910)), P((7, 0.081, 0.102), (7, 0.473, 0.524))),
    'Q2(c)': (P((2, 0.910, 0.931)), P((7, 0.081, 0.102), (7, 0.524, 0.615))),
    'Q3 Option One (a)': (P((3, 0.040, 0.126)), P((8, 0.078, 0.159))),
    'Q3 Option One (b)(i)': (P((3, 0.040, 0.074), (3, 0.126, 0.163)), P((8, 0.078, 0.102), (8, 0.159, 0.246))),
    'Q3 Option One (b)(ii)': (P((3, 0.040, 0.074), (3, 0.163, 0.266)), P((8, 0.078, 0.102), (8, 0.246, 0.333))),
    'Q3 Option One (c)(i)': (P((3, 0.040, 0.074), (3, 0.266, 0.337)), P((8, 0.078, 0.102), (8, 0.333, 0.417))),
    'Q3 Option One (c)(ii)': (P((3, 0.040, 0.074), (3, 0.266, 0.320), (3, 0.337, 0.355)), P((8, 0.078, 0.102), (8, 0.333, 0.355), (8, 0.417, 0.470))),
    'Q3 Option One (c)(iii)': (P((3, 0.040, 0.074), (3, 0.266, 0.320), (3, 0.355, 0.372)), P((8, 0.078, 0.102), (8, 0.333, 0.355), (8, 0.470, 0.522))),
    'Q3 Option One (c)(iv)': (P((3, 0.040, 0.074), (3, 0.266, 0.320), (3, 0.372, 0.458)), P((8, 0.078, 0.102), (8, 0.333, 0.355), (8, 0.522, 0.708))),
    'Q3 Option Two (a)(i)': (P((3, 0.519, 0.610)), P((9, 0.081, 0.185))),
    'Q3 Option Two (a)(ii)': (P((3, 0.519, 0.591), (3, 0.610, 0.627)), P((9, 0.081, 0.122), (9, 0.185, 0.255))),
    'Q3 Option Two (a)(iii)': (P((3, 0.519, 0.591), (3, 0.627, 0.644)), P((9, 0.081, 0.122), (9, 0.255, 0.307))),
    'Q3 Option Two (a)(iv)': (P((3, 0.519, 0.591), (3, 0.644, 0.678)), P((9, 0.081, 0.122), (9, 0.307, 0.371))),
    'Q3 Option Two (b)': (P((3, 0.519, 0.556), (3, 0.678, 0.799)), P((9, 0.081, 0.103), (9, 0.371, 0.615))),
    'Q3 Option Two (c)(i)': (P((3, 0.519, 0.556), (3, 0.799, 0.835)), P((9, 0.081, 0.103), (9, 0.615, 0.734))),
    'Q3 Option Two (c)(ii)': (P((3, 0.519, 0.556), (3, 0.835, 0.873)), P((9, 0.081, 0.103), (9, 0.734, 0.917), (10, 0.081, 0.334))),
    'Q4(a)': (P((4, 0.040, 0.107)), P((11, 0.116, 0.335))),
    'Q4(b)': (P((4, 0.040, 0.072), (4, 0.107, 0.142)), P((11, 0.116, 0.137), (11, 0.335, 0.689))),
    'Q4(c)': (P((4, 0.040, 0.072), (4, 0.142, 0.176)), P((11, 0.116, 0.137), (11, 0.689, 0.781))),
    'Q4(d)': (P((4, 0.040, 0.072), (4, 0.176, 0.283)), P((11, 0.116, 0.137), (11, 0.781, 0.858))),
    'Q5(a)(i)': (P((4, 0.283, 0.302)), P((12, 0.081, 0.207))),
    'Q5(a)(ii)': (P((4, 0.302, 0.353)), P((12, 0.081, 0.101), (12, 0.207, 0.656))),
    'Q5(b)(i)': (P((4, 0.353, 0.372)), P((12, 0.081, 0.101), (12, 0.656, 0.866))),
    'Q5(b)(ii)': (P((4, 0.372, 0.422)), P((12, 0.081, 0.101), (12, 0.866, 0.906))),
    'Q5(c)(i)': (P((4, 0.422, 0.459)), P((12, 0.081, 0.101), (13, 0.081, 0.121))),
    'Q5(c)(ii)': (P((4, 0.422, 0.442), (4, 0.459, 0.562)), P((12, 0.081, 0.101), (13, 0.121, 0.315))),
    'Q6(a)': (P((4, 0.562, 0.614)), P((13, 0.315, 0.427))),
    'Q6(b)': (P((4, 0.614, 0.664)), P((13, 0.315, 0.335), (13, 0.427, 0.536))),
    'Q6(c)': (P((4, 0.664, 0.740)), P((13, 0.315, 0.335), (13, 0.536, 0.632))),
    'Q7(a)(i)': (P((5, 0.040, 0.144)), P((14, 0.081, 0.243))),
    'Q7(a)(ii)': (P((5, 0.040, 0.109), (5, 0.144, 0.214)), P((14, 0.081, 0.102), (14, 0.243, 0.319))),
    'Q7(b)(i)': (P((5, 0.214, 0.285)), P((14, 0.081, 0.102), (14, 0.319, 0.394))),
    'Q7(b)(ii)': (P((5, 0.214, 0.266), (5, 0.285, 0.302)), P((14, 0.081, 0.102), (14, 0.394, 0.429))),
    'Q7(b)(iii)': (P((5, 0.214, 0.266), (5, 0.302, 0.353)), P((14, 0.081, 0.102), (14, 0.429, 0.488))),
    'Q7(c)': (P((5, 0.353, 0.566)), P((14, 0.081, 0.102), (14, 0.488, 0.706))),
    'Q8(a)': (P((6, 0.040, 0.107)), P((15, 0.081, 0.382))),
    'Q8(b)(i)': (P((6, 0.040, 0.072), (6, 0.107, 0.181)), P((15, 0.081, 0.103), (15, 0.382, 0.454))),
    'Q8(b)(ii)': (P((6, 0.040, 0.072), (6, 0.107, 0.163), (6, 0.181, 0.231)), P((15, 0.081, 0.103), (15, 0.454, 0.540))),
    'Q8(c)': (P((6, 0.040, 0.072), (6, 0.231, 0.405)), P((15, 0.081, 0.103), (15, 0.540, 0.914))),
    'Q9(a)': (P((6, 0.405, 0.472)), P((16, 0.081, 0.209))),
    'Q9(b)': (P((6, 0.405, 0.438), (6, 0.472, 0.507)), P((16, 0.081, 0.102), (16, 0.209, 0.284))),
    'Q9(c)': (P((6, 0.405, 0.438), (6, 0.507, 0.542)), P((16, 0.081, 0.102), (16, 0.284, 0.343))),
    'Q9(d)': (P((6, 0.405, 0.438), (6, 0.542, 0.577)), P((16, 0.081, 0.102), (16, 0.343, 0.419))),
    'Q9(e)': (P((6, 0.405, 0.438), (6, 0.577, 0.639)), P((16, 0.081, 0.102), (16, 0.419, 0.504))),
}
FIRST = 'The scheme\'s convention: the first correct answer encountered earns the first value and each later correct answer the next ({}).'


def split(text, note=None, route=None):
    """A row of an orderedSplit card: the scheme prices the scale, not the row."""
    row = point(text, None, note)
    if route:
        row['route'] = route
    return row


def build():
    p = Paper(2017, 'higher', FILE, HASHES, REGIONS, ATLAS, 8, 20, SELECTIONS, SUPPLEMENTARY,
              section=lambda ref: 'A' if ref.startswith('Q1(') else 'B')
    add = p.add
    six = 'Answer any six of the parts (a) to (j).'
    # Question 1 -------------------------------------------------------------
    add('q1a', 'Q1(a)', '3-3-1', 'short-term-ley-species',
        '(i) Name two species that might be included in a seed mixture in a short-term ley for silage. (ii) Give a reason for each choice.',
        [split('(i) Species — Italian (or perennial or hybrid) ryegrass/ (red or white) clover/ peas (or beans or named legume)/ barley (or oats)', FIRST.format('2(4) + 2(1)') + ' Four answers: two species and a matching reason for each. Any two species.'),
         split('(ii) Reasons — Ryegrasses: High productivity or digestibility or palatability or fast growing', 'One matching reason for each of your two choices.'),
         split('(ii) Reasons — Clovers, peas, beans: Nitrogen fixation or high in protein or digestibility or productivity or palatability'),
         split('(ii) Reasons — Oats, barley: Productivity')],
        six, marks=10, tariff={'kind': 'orderedSplit', 'notation': '2(4) + 2(1)'}, node='2-6')
    add('q1b', 'Q1(b)', '3-3-2', 'biological-control', '(i) Explain the term biological control. (ii) Give two examples of biological control in agriculture, horticulture, or forestry.',
        [split('(i) Biological control — Control of pests (or weeds or diseases)/ using predators (or parasites or infectious agents or another living thing)', FIRST.format('2(4) + 2(1)') + ' Four answers: two points for (i) and two examples.'),
         split('(ii) Examples — e.g. Aphid-ladybird/ red spider mite-whitefly/ mouse-cat (or dog)/ slug (or snail)-duck (or goose)/ aphid-parasitic wasp/ vine weevil-nematode', 'Any two.')],
        six, marks=10, tariff={'kind': 'orderedSplit', 'notation': '2(4) + 2(1)'}, node='2-4')
    add('q1c', 'Q1(c)', '3-2', 'monocots-and-dicots',
        '(i) Give two structural differences between monocotyledonous (monocot) plants and dicotyledonous (dicot) plants. (ii) Give one example of a monocot plant and one example of a dicot plant.',
        [split('(i) Structural differences, monocot (dicot) — Narrow leaves (broad leaves)/ parallel veins (net or reticulate veins)/ flower parts in 3s or multiples of (flower parts in 4s or 5s or multiples of)/ vascular bundles scattered (vascular bundles in a ring)/ fibrous roots (tap root)/ seeds have one cotyledon (seeds have two cotyledons)/ vascular tissue in root in a circle (root vascular tissue star shaped)',
               FIRST.format('2(4) + 2(1)') + ' Four answers: two differences and two examples. Any two differences.'),
         split('(ii) Examples — Monocot: grass (or named grass or named cereal or other valid)'),
         split('(ii) Examples — Dicot: potatoes (or peas or beans or sunflower or other valid)')],
        six, marks=10, tariff={'kind': 'orderedSplit', 'notation': '2(4) + 2(1)'}, node='2-1')
    add('q1d', 'Q1(d)', '2-1', 'rock-classification', 'Classify each of the following rock types based on how they are formed: (i) Marble (ii) Granite (iii) Basalt.',
        [menu(['(i) Marble: Metamorphic', '(ii) Granite: Igneous', '(iii) Basalt: Igneous'], [6, 3, 1], FIRST.format('6 + 3 + 1'))], six, node='1-0')
    add('q1e', 'Q1(e)', '4-3-2', 'ration-protein-factors', 'List three factors that determine the amount of protein required in an animal ration.',
        [menu('Age|sex|production target|body condition score|health|type or breed of animal', [6, 3, 1], 'Any three. ' + FIRST.format('6 + 3 + 1'))], six, node='3-4')
    add('q1f', 'Q1(f)', '3-1', 'leaf-structure-photosynthesis', 'Outline three ways in which the structure of the leaf is suited to photosynthesis.',
        [menu('Thinness for diffusion|large surface area to trap light|more chloroplasts in palisade (upper) layer for increased photosynthesis|stomata for entry of air (or CO2)|vascular tissue for transport|cuticle to conserve water|spongy mesophyll (or air spaces) to allow diffusion',
              [6, 3, 1], 'Any three. ' + FIRST.format('6 + 3 + 1'))], six, node='2-0')
    add('q1g', 'Q1(g)', '4-1', 'sheep-and-pig-dental-formulae', 'Give the dental formula of each of the following animals: (i) Sheep (ii) Pig.',
        [menu(['(i) Sheep: 0033 / 3133', '(ii) Pig: 3143 / 3143'], [6, 4],
              FIRST.format('6 + 4') + ' Upper jaw over lower jaw; both formulae must have the order of incisors, canines, premolars, molars clearly stated. The scheme also allows 0033 / 4033 for the sheep.')], six, node='3-0')
    add('q1h', 'Q1(h)', '2-2-3', 'nitrogen-fixing-legumes',
        '(i) Name the nitrogen-fixing bacteria found in the root nodules of legumes such as clover. (ii) Name two legumes other than clover.',
        [split('(i) N-fixing bacteria — Rhizobia', FIRST.format('6 + 3 + 1') + ' Three answers: (i) and two legumes.'),
         split('(ii) Legumes other than clover — Peas/ beans/ vetch/ furze (or whin or gorse) or other valid', 'Any two.')],
        six, marks=10, tariff={'kind': 'orderedSplit', 'notation': '6 + 3 + 1'}, node='1-4|2-1')
    add('q1i', 'Q1(i)', '4-3-2', 'dairy-cow-bcs', '(i) Explain the term body condition score (BCS). (ii) Give the correct BCS for a dairy cow before calving and at mating time.',
        [split('(i) BCS — Degree of fat on the body or lean to fat ratio/ scale of 1 - 5 or 1 – 9', FIRST.format('2(4) + 2(1)') + ' Four answers: two points for (i) and the two scores.'),
         split('(ii) BCS for dairy cow — Before calving: 3.0 - 3.5'), split('(ii) BCS for dairy cow — At mating: 2.5 - 3.0')],
        six, marks=10, tariff={'kind': 'orderedSplit', 'notation': '2(4) + 2(1)'}, node='3-4')
    add('q1j', 'Q1(j)', '4-1', 'reproductive-hormones', 'Describe one function of each of the following mammalian reproductive hormones: (i) FSH (ii) Progesterone (iii) Testosterone.',
        [menu(['(i) FSH: Promotes follicle development or egg development or sperm production',
               '(ii) Progesterone: Inhibits ovulation or inhibits lactation or inhibits labour or maintains pregnancy or synchronised breeding or lambing out of season',
               '(iii) Testosterone: Development of male characteristics (or described) or sperm production'], [6, 3, 1], FIRST.format('6 + 3 + 1'))], six, node='3-0')
    # Question 2 -------------------------------------------------------------
    water = 'Water is held in the soil in two main ways.'
    add('q2ai', 'Q2(a)(i)', '2-2-2', 'how-soil-holds-water', 'Name both ways and explain how each works.',
        [point('Adsorption (hygroscopic)', 3, '3 + 2 for each way: the name 3, its explanation 2.'),
         point('held by attraction between negative charges on clay and positive charges on (polarised) water molecule', 2),
         point('Capillary (action)', 3), point('water held in small pores by capillary forces', 2, 'NB ‘capillary’ must be mentioned at least once to get both points.')], water, node='1-3')
    add('q2aii', 'Q2(a)(ii)', '2-3', 'artificial-drainage-benefits', 'Give two benefits of artificial drainage in soils.',
        [menu('Lowers water table|less risk of poaching (or compaction)|increases aeration|warmer soil|improved crop growth (or yield)|easier to cultivate (or earlier cultivation)|benefits earthworms|controls liver fluke|increased nutrient uptake',
              [3, 3], 'Any two, 3 marks each (2(3)).')], water, node='1-5')
    acidity = 'Give three ways in which soil acidity increases over time.'
    add('q2bi', 'Q2(b)(i)', '2-2-1', 'soil-acidity-causes', 'Give three ways in which soil acidity increases over time.',
        [menu('Rainfall|crop growth|animal excretion|fertilisers|acid rain|manures (or slurry or OM)|pine needles', [2] * 3, 'Any three, 2 marks each (3(2)).')], node='1-2')
    add('q2bii', 'Q2(b)(ii)', '2-2-1', 'soil-acidity-mechanisms', 'Explain the mechanism at work in each case.',
        [menu('Leaching of Ca(2+) (or Mg(2+))|incorporation of base-forming elements into plant tissues|urine is acidic|acidic components in some fertilisers|continuous effect of rain with acidic component|decomposition of organic matter or acidic component in slurry|pine needles are acidic',
              [2] * 3, 'Matching mechanisms for your three ways, 2 marks each (3(2)).')], acidity, node='1-2')
    add('q2biii', 'Q2(b)(iii)', '2-2-1', 'soil-acidity-crop-effects', 'Describe two effects of increased soil acidity on crops.',
        [menu('Poor nutrient uptake (or immobilisation of minerals)|inhibition of N fixation|unsuitable pH for most crops (or lower yield)', [2, 2], 'Any two, 2 marks each (2(2)).')], node='1-2')
    add('q2c', 'Q2(c)', '2-2-1', 'cation-exchange-experiment', 'Describe an experiment to show cation exchange in a soil sample.',
        [menu('High pH soil|filter|wash with KCl (soln)|test filtrate (leachate) for Ca(2+)|using ammonium oxalate|white ppt. is positive|repeat until negative (for Ca(2+))|test for K(+)|using sodium cobalt nitrate|purple colour is positive',
              [4, 4, 2, 2, 2, 2], 'Any six: 2(4) + 4(2), the first two correct earn 4 each and the next four 2 each.')], node='1-2|0-1')
    # Question 3 -------------------------------------------------------------
    add('q3o1a', 'Q3 Option One (a)', '4-3-2', 'weanling-winter-housing', 'Describe the main requirements of winter housing suitable for weanlings in a beef enterprise.',
        [menu('Slats|straw (or mats)|1.4 m2 floor space|7 m3 air space|ventilation (or draught-free)|clean water|feeding space', [6, 6, 2, 2],
              'Any four: 2(6) + 2(2), the first two correct earn 6 each and the next two 2 each.')], node='3-4')
    add('q3o1bi', 'Q3 Option One (b)(i)', '4-3-1', 'calf-to-beef-winter-feeding',
        'Compare the winter feeding programmes for first and second winters in a two year calf-to-beef system and account for any differences.',
        [menu('Silage in both for winter 1 and winter 2 or hay and silage for winter 1 and silage for winter 2|less or no concentrates for winter 1 or more concentrates for winter 2|valid reason for either difference',
              [6, 2, 2], 'Three points: 6 + 2(2), the first correct earns 6 and the next two 2 each.')], node='3-3')
    add('q3o1bii', 'Q3 Option One (b)(ii)', '4-3-1', 'calf-to-beef-target-weights',
        'Give the target weight for Hereford x Friesian steers at each of the following stages of the two year calf-to-beef system: Winter housing year 1; Winter housing year 2; Slaughter.',
        [menu(['Year 1 winter housing: 200-220 kg', 'Year 2 winter housing: 450-480 kg', 'Slaughter: 550-600 kg'], [4, 1, 1], '4 + 2(1): the first correct earns 4 and the next two 1 each.')], node='3-3')
    manure = 'Slurry and farmyard manure (FYM) are the most significant waste products of winter housing in a beef enterprise. Compare slurry and FYM under the following headings.'
    for key, ref, heading, slurry, fym in [
            ('q3o1ci', 'Q3 Option One (c)(i)', 'Nutrient value', 'Higher N or less OM or faster acting', 'Lower N or more OM or slower acting'),
            ('q3o1cii', 'Q3 Option One (c)(ii)', 'Storage', 'Tank', 'Dungstead or slab'),
            ('q3o1ciii', 'Q3 Option One (c)(iii)', 'Method of spreading', 'Slurry spreader or injection method', 'Muckspreader or by fork'),
            ('q3o1civ', 'Q3 Option One (c)(iv)', 'Disadvantages of spreading', 'Soil compaction or pollution or disease spread or odour or weed dispersal', 'Soil compaction or odour or pollution or weed dispersal or disease spread or slower to return to grazing')]:
        add(key, ref, '2-3', 'slurry-vs-fym-' + heading.lower().replace(' ', '-'), f'Compare slurry and FYM under the heading: {heading}.',
            [point(f'Slurry — {slurry}', 2, '2(2): slurry 2 + FYM 2.'), point(f'FYM — {fym}', 2)], manure, node='1-6')
    potato = 'Describe the following aspects of potato cultivation.'
    for key, ref, topic, aspect, points in [
            ('q3o2ai', 'Q3 Option Two (a)(i)', '3-3-1', 'Soil suitability', 'Deep|well drained|sandy loam or other valid soil type|pH 5.5-6.0|stone free'),
            ('q3o2aii', 'Q3 Option Two (a)(ii)', '3-3-1', 'Sowing', '10 cm below ridge|20-35 cm spacing|40,000-60,000 per ha.|potato planter|February to April|sprouting for earlies'),
            ('q3o2aiii', 'Q3 Option Two (a)(iii)', '3-3-2', 'Weed control', 'Earthing up|shading|herbicide|manual weeding|scuffling'),
            ('q3o2aiv', 'Q3 Option Two (a)(iv)', '3-3-3', 'Storage', 'Ventilated or correctly stacked|frost free|dry|no vermin|darkness|growth inhibitors|low temperature')]:
        add(key, ref, topic, 'potato-' + aspect.lower().replace(' ', '-'), f'Describe the following aspect of potato cultivation: {aspect}.',
            [menu(points, [3, 1], 'Any two: 3 + 1, the first correct earns 3 and the second 1.')], potato, node='2-3' if topic == '3-3-1' else ('2-4' if topic == '3-3-2' else '2-5'))
    cereals = [('barley', 'Barley', 'Barley: 6-8 t per ha for spring (8-9 t per ha for winter)'), ('wheat', 'Wheat', 'Wheat: 7-8 t per ha for spring (9-11 t per ha for winter)'),
               ('oats', 'Oats', 'Oats: 6-7 t per ha for spring (7-8 t per ha for winter)'), ('maize', 'Maize', 'Maize: 15-20 t per ha of dry matter')]
    rows, variants = routes([(slug, label, [point(f'Name — {label}', 3, 'Name 3; climate 3 + 1; disease 3 + 1; harvest date 3; yield 2.'),
                                            menu('Warm|moist|dry or sunshine', [3, 1], '(i) Climate: any two for any named crop, 3 + 1.'),
                                            menu('Fungal disease (or viral disease or disease named)|certified seed|spray|biological control', [3, 1], '(ii) Disease: any two, 3 + 1.'),
                                            point('(iii) Harvest date — July to September', 3), point(f'(iv) Yield — {yld}', 2)]) for slug, label, yld in cereals])
    add('q3o2b', 'Q3 Option Two (b)', '3-3-1', 'named-cereal-cultivation',
        'Describe the cultivation of a named cereal crop under the following headings: (i) Climate (ii) Disease (iii) Harvest date (iv) Yield.', rows,
        selection=closed(1, [label for _, label, _ in cereals]), node='2-3|2-4|2-5', extra={'answerVariants': variants})
    add('q3o2ci', 'Q3 Option Two (c)(i)', '3-3-3', 'cereal-ripening-changes', 'Describe the physiological changes that occur during the ripening process in the cereal referred to above.',
        [menu('Bleached colour of straw|head parallel to stem (barley only)|straw dry|grain hard|moisture content decreases below 20%|grain falls off|top leaves dead|For maize: silks dry|silks dark brown|kernel has clear liquid|ears plump',
              [4, 2, 2], 'Any three: 4 + 2(2), the first correct earns 4 and the next two 2 each. The last four points are for maize.')], node='2-5')
    add('q3o2cii', 'Q3 Option Two (c)(ii)', '3-3-3', 'grain-merchant-tests', 'Describe two tests carried out by a grain merchant on harvested grain.',
        [menu(['Moisture test: Find mass of sample/ dry at 100 °C/ find mass loss/ OR Moisture meter/ calibrate/ number of readings/ average',
               'Screenings test (test for purity): Find mass of sample/ separate impurities/ calculate % pure seed',
               'Hectolitre mass: Fill container of known volume (or chondrometer) with grain/ find mass of grain/ calculate for 100 litres',
               'Protein test: Find % nitrogen/ use Kjeldahl test/ multiply by 6.5 (or Pynes’s method/ titrate with NaOH)',
               'Hagberg test: Test for flour quality/ measures viscosity (or flow rate or use viscometer)/ of wheat flour and water mixture',
               'Germination test: Count seeds/ provide all conditions necessary for germination/ count number that germinate',
               'Mycotoxin test: Toxic substances/ from moulds/ detected by chromatography',
               '1,000 grain mass: Count a number of grains (or seeds)/ find the mass/ calculate mass for 1,000 grains (or seeds)'], [4, 4],
              'Any two tests: 2(2 + 2(1)), each test 2 for its name and 1 each for two points of its description.')], node='2-5|0-1')
    # Question 4 -------------------------------------------------------------
    lab = 'In the case of any two of the following, describe a laboratory or field method.'
    rows, variants = routes([(slug, label, [menu(steps, [4] * 6, f'{label}: any six, 4 marks each (6(4)).')]) for slug, label, steps in [
        ('cattle', 'Feeding trial', 'Two cattle of similar size or breed (or of known mass)|separate|equal ration|one whole and one rolled|valid time interval|examine dung (or find mass of animals again)|compare presence of grains (or mass of animals)|result (or conclusion)|repeat'),
        ('test-tubes', 'Test-tube method', 'Two equal samples of cereal grain|one whole and one rolled|added to two test tubes|add water and amylase to each|place in waterbath at 37 °C|test for starch (or presence of reducing sugar (or glucose or maltose))|using iodine for starch (or Benedict’s (or Fehling’s)) for reducing sugar)|correct conclusion')]])
    add('q4a', 'Q4(a)', '4-3-2', 'whole-versus-rolled-grain', 'Describe a laboratory or field method to compare the digestibility of whole and rolled cereal grains.', rows, lab,
        selection=closed(1, ['Feeding trial', 'Test-tube method']), node='3-4|0-1', extra={'answerVariants': variants})
    silage = [('leaf-stem', 'Leaf to stem ratio', 'Find mass of sample of silage|separate the leaves from the stems|find mass of two dishes|put leaves in one and stems in the other|find mass|get ratio of leaves to stem|correct conclusion (more leaf or better DMD)'),
              ('ph', 'pH test', 'Squeeze (or crush) sample of silage|collect liquid|add distilled water|test for pH with indicator or pH meter|record result (pH 3.8 to 4.2)|correct conclusion'),
              ('dm', 'To get DM content', 'Find mass of sample of silage|record|dry at 100 °C|get mass again and repeat drying until mass is constant|record final mass|calculate % DM|correct conclusion (16-20% DM)'),
              ('sensory', 'For good quality silage (poor quality)', 'colour|yellow-green (black-brown)|smell|slight or sharp (sweet or sour)|taste|sharp acidic (not sharp acidic)|feel|firm (mushy)|squeeze|releases a small amount of liquid or none with two hands (liquid released with one hand)')]
    rows, variants = routes([(slug, label, [menu(steps, [4] * 6, f'{label}: any six, 4 marks each (6(4)).')]) for slug, label, steps in silage])
    add('q4b', 'Q4(b)', '3-3-3', 'silage-quality-method', 'Describe a laboratory or field method to determine the quality of silage in a pit or bale.', rows, lab,
        selection=closed(1, [label for _, label, _ in silage]), node='2-6|0-1', extra={'answerVariants': variants})
    add('q4c', 'Q4(c)', '2-2-2', 'capillarity-two-soils', 'Describe a laboratory or field method to compare capillarity in two named soil types.',
        [point('Sandy soil and clay soil', 4, '6(4): the named soils are the compulsory point, then any five more.'),
         menu('each into an open ended glass tube|cotton wool plug in base|stand tubes in water|minimum of 1 hour|water rises higher in clay or lower in sand|capillarity greater in clay', [4] * 5, 'Any five more, 4 marks each.')],
        lab, node='1-3|0-1')
    add('q4d', 'Q4(d)', '3-1', 'transpiration-rate', 'Describe a laboratory or field method to measure the rate of transpiration in plants.',
        [menu('Potometer|leafy plant|cut under water|angled cut|insert in potometer|seal|insert air bubble|correct conditions (for transpiration)|time bubble movement|repeat', [4] * 6,
              'Any six, 4 marks each (6(4)).')], lab, node='2-0|0-1')
    # Question 5 -------------------------------------------------------------
    add('q5ai', 'Q5(a)(i)', '4-3-2', 'milk-tests', 'List two qualitative tests and two quantitative tests normally carried out on milk.',
        [menu('Methylene blue test|resazurin test|TBC|SCC|thermoduric bacteria|temperature|antibiotic (e.g. Delvo test)|added water', [2, 2], 'Qualitative: any two, 2 marks each (2(2)).'),
         menu('Sediment|% water (or % solids)|% lactose|butterfat test|% protein|% minerals|TBC|SCC|thermoduric bacteria|temperature', [2, 2], 'Quantitative: any two, 2 marks each (2(2)).')], node='3-4')
    tests = [('gerber', 'Gerber butterfat test', 'Butyrometer|10 cm3 sulphuric acid|10.75 cm3 milk|1 ml amyl alcohol|stopper butyrometer|shake until red colour|centrifuge at 1200 rpm for 4 minutes|adjust fat column with key|read result (from scale)'),
             ('lactometer', 'Adulteration of milk with water (lactometer)', 'Pour milk into graduated cylinder ⅔ of volume along sides|lower lactometer gently|read lactometer at the top of meniscus|repeat the procedure with milk sample with added water|lactometer sinks deeper in watered-down sample'),
             ('cryoscope', 'Adulteration of milk with water (cryoscope)', 'Find the freezing point of the milk|cryoscope|if freezing point is greater than - 0.5 °C|water has been added to the milk'),
             ('water-solids', '% water or % solids', 'Record the mass of a milk sample|dry at 100 °C|to a constant mass|find % water|correct result or correct conclusion'),
             ('ash', 'To find the % ash (or % minerals) in milk', 'Dry a milk sample|record the dry mass|burn the milk until it reaches a constant mass|calculate the % ash|correct result or correct conclusion'),
             ('lactose', 'To find the % lactose in milk', 'Allow milk to sour (or coagulate the protein and fat)|take a sample of the milk whey|place a sample on a refractometer or polarimeter|record %|repeat|find the average'),
             ('protein', 'To find the % protein', 'Find the % nitrogen in the milk|using the Kjeldahl method|multiply the % nitrogen by 6.5 (or using Pyne’s method|titrate with NaOH)|to find % protein')]
    rows, variants = routes([(slug, label, [menu(steps, [2] * 4, f'{label}: any four, 2 marks each (4(2)).')]) for slug, label, steps in tests])
    add('q5aii', 'Q5(a)(ii)', '4-3-2', 'quantitative-milk-test', 'Describe how you would carry out in the laboratory any one of the quantitative tests referred to above.', rows,
        'List two qualitative tests and two quantitative tests normally carried out on milk.',
        selection=closed(1, [label for _, label, _ in tests]), node='3-4|0-1', extra={'answerVariants': variants})
    add('q5bi', 'Q5(b)(i)', '4-2', 'lowland-sheep-breeds', 'Name two lowland sheep breeds and describe their bodily characteristics.',
        [menu('Galway|Texel|Suffolk|Border Leicester|Blue-faced Leicester or any valid', [2, 2], 'Any two breeds, 2 marks each (2(2)).'),
         menu(['Galway: Large or white wool or polled or wool on forehead',
               'Texel: White face or polled or excellent conformation or excellent carcase quality or short wool or white wool or wide face or head free of wool',
               'Suffolk: Excellent conformation or short wool or dark wool or black head or black legs or polled',
               'Border Leicester: Upright ears or polled or white wool or long wool or large',
               'Blue-faced Leicester: Upright ears or roman nose or blue skin or polled or white wool or long wool or large'], [3, 3],
              'One characteristic each from your two breeds, 3 marks each (2(3)).')], node='3-1|3-3')
    add('q5bii', 'Q5(b)(ii)', '4-3-1', 'crossbred-ewes', 'Explain fully why crossbred ewes are frequently used in a lowland sheep enterprise.',
        [menu('Hybrid vigour|good mothering ability|good carcase quality|prolific|good milk production', [3, 3], 'Any two, 3 marks each (2(3)).')], node='3-3|3-6')
    repro = 'Reproductive efficiency is an important target in a beef-rearing enterprise.'
    add('q5ci', 'Q5(c)(i)', '4-3-2', 'reproductive-efficiency', 'Explain the term reproductive efficiency.', [point('Number of calves weaned per 100 cows mated', 4)], repro, node='3-4')
    add('q5cii', 'Q5(c)(ii)', '4-3-2', 'reproductive-efficiency-factors', 'Describe three factors affecting reproductive efficiency.',
        [menu('BCS|heat detection|calving interval|age of cow|health of cow|culling rate|age at first calving|diseases linked to fertility|calf mortality|bull|timing of service|AI|diet|duration of oestrus|dam access to calf (or post-birth care)|breed',
              [4] * 3, 'Any three, 4 marks each (3(4)).')], repro, node='3-4')
    # Question 6 -------------------------------------------------------------
    add('q6a', 'Q6(a)', '3-3-3', 'dmd-through-growth', 'Describe how the dry matter digestibility (DMD) of a grass plant alters during its various stages of growth.',
        [menu('Leafy stage high DMD (or high sugar)|sugar converted to cellulose (or soluble to insoluble carbohydrate) as plant grows|DMD drops|heading date DMD very low|drops 0.5% per day (after heading date)|increased fibre (or stem)',
              [4] * 4, 'Any four, 4 marks each (4(4)).')], node='2-6')
    add('q6b', 'Q6(b)', '3-3-2', 'keeping-dmd-high', 'Describe four measures that can be used to maintain a high grass DMD for longer during the grazing season.',
        [menu('Rotational grazing (recovery time)|topping (new growth (or tillering))|(N) fertiliser or slurry (new foliage)|late-flowering grasses (delays drop in DMD)|PRG (high DMD late in season)|mixed grazing (high DMD)|early and late strains (different heading out dates)',
              [4] * 4, 'Any four: 4[2(2)], each method 2 and its effect (in brackets) 2.')], node='2-6')
    add('q6c', 'Q6(c)', '4-1', 'ruminant-stomach-grass', 'Explain how the ruminant stomach is suited to the digestion of plants in a grassland sward.',
        [point('Rumen/ cellulose digested (by rumen flora)', 4, '2(2) for each compartment: its name and its role.'), point('Reticulum/ regurgitation for chewing the cud', 4),
         point('Omasum/ water removed', 4), point('Abomasum/ digestion completed (by gastric juices)', 4)], node='3-0|2-6')
    # Question 7 -------------------------------------------------------------
    beef = 'Many Irish suckler beef producers are currently taking part in the Beef Data and Genomics Programme which aims to improve profitability in the suckler sector. Elements of this programme include performance testing and progeny testing.'
    add('q7ai', 'Q7(a)(i)', '4-3-2', 'performance-and-progeny-testing', 'Explain the terms performance testing and progeny testing.',
        [point('Performance testing — Comparing records of an animal’s performance (or FCR, or growth rate, or conformation)/ with the records of similar animals kept under the same conditions (to identify superior animals)', 4, '2(2) for each term.'),
         point('Progeny testing — Comparing the records of the performance of an animal’s offspring/ with the offspring of other animals kept under the same conditions (to identify superior breeding stock)', 4)],
        beef, node='3-6')
    add('q7aii', 'Q7(a)(ii)', '4-3-2', 'replacement-heifer-selection', 'List three characteristics which are important in the selection of replacement heifers for a suckler enterprise.',
        [menu('Fertility|calving ease|docility|beef traits|feed intake|conformation|growth rate|FCE|good potential milk yield|healthy udder and teats (or good health)|longevity|good cull value', [3] * 3,
              'Any three, 3 marks each (3(3)).')], beef, node='3-4|3-6')
    concepts = 'Explain the following concepts in genetics and give an appropriate example in each case.'
    for key, ref, concept, term, explain, example in [
            ('q7bi', 'Q7(b)(i)', 'incomplete-dominance', 'Incomplete dominance', 'Neither allele dominant (or co-dominant or of equal dominance) or both expressed in the phenotype (or resulting in an intermediate trait)', 'roan shorthorn cattle or pink flower or other valid'),
            ('q7bii', 'Q7(b)(ii)', 'alleles', 'Alleles', 'Alternative forms of a gene', 'tall-dwarf or other valid'),
            ('q7biii', 'Q7(b)(iii)', 'continuous-variation', 'Continuous variation', 'Characteristic controlled by a number of genes (or genes produce a range within a phenotype)', 'stem length or milk yield or other valid')]:
        add(key, ref, '4-1', concept, f'Explain the concept and give an appropriate example: {term}.', [point(explain, 3, '3 + 2.'), point(example, 2)], concepts, node='3-6')
    add('q7c', 'Q7(c)', '4-1', 'mouse-dihybrid-cross',
        'Two mice, heterozygous for both these genes, were mated. Taking care to differentiate clearly between uppercase and lowercase letters, explain with the aid of a Punnett square, the probability in each case that the offspring would have the following phenotypes: (i) Albino coat (ii) Bent hair (iii) Albino coat and bent hair (iv) Wild type coat colour and bent hair.',
        [point('All gametes correct — WS Ws wS ws', 4),
         point('All offspring genotypes correct', 4, 'The scheme\'s grid gives WWSS, WWSs, WwSS, WwSs, WWss, Wwss, wwSS, wwSs and wwss across its sixteen boxes.'),
         point('(i) Albino coat: 4/16', 2), point('(ii) Bent hair: 4/16', 2), point('(iii) Albino coat and bent hair: 1/16', 2), point('(iv) Wild type coat colour and bent hair: 3/16', 2)],
        'In mice the allele for wild type coat colour (W) is dominant to the allele for albino coat (w). The allele for straight hair (S) is dominant to the allele for bent hair (s).', node='3-6')
    # Question 8 -------------------------------------------------------------
    twoof = 'Answer any two of the parts (a), (b), (c).'
    add('q8a', 'Q8(a)', '2-3', 'carbon-cycle', 'Describe, with the aid of a labelled diagram, the carbon cycle.',
        [point('Carbon dioxide in air and photosynthesis and animals consume plants and death (or decay) of organisms and respiration and fossil fuels (or limestone (carbonates)) and combustion (or by rain)', None,
               'Diagram 6, 3, 0: 6 with all of these in correct relationship to each other; 3 with any one absent or any arrow absent or in a wrong direction.', kind='criterion'),
         point('Carbon absorbed by plants in photosynthesis/ carbon assimilated into biomolecules (or named biomolecule)/ plants consumed by animals/ assimilation point for animals if not already quoted for plants/ death (or decay) of organisms/ microorganisms (or named)/ carbon released by organisms in respiration/ carbon trapped in fossil fuels (or in limestone (or carbonates))/ carbon released from fossil fuels (or from plants) by combustion (or from limestone by rain)',
               None, 'Diagram labels or written account: any six, 3 marks each (6(3)).')],
        twoof, marks=24, tariff={'kind': 'questionTotal', 'notation': 'D 6, 3, 0 + 6(3)'}, node='1-6')
    insects = 'Phylum Arthropoda contains millions of species. Class Insecta (insects) is the class from this phylum with the greatest agricultural importance.'
    add('q8bi', 'Q8(b)(i)', '4-2', 'insect-structure', 'Outline the principal structural features of insects.',
        [menu('Exoskeleton (or chitin)|6 legs (or jointed legs)|3 body regions|head and thorax and abdomen|compound eyes|antennae|spiracles|(most have) wings', [3] * 4, 'Any four, 3 marks each (4(3)).')],
        twoof + ' ' + insects, node='3-1')
    add('q8bii', 'Q8(b)(ii)', '3-3-2', 'insect-pests-damage', 'Name any two insect pests in agriculture and describe the damage they cause to named crops or animals.',
        [menu(['e.g. Cabbage white butterfly (or caterpillar if adult not named)/ larva (or caterpillar) if not already given eats leaves/ of cabbage',
               'e.g. Green bottle (or blowfly) (or maggot if adult not named)/ larva (or maggot if not already given) eats flesh/ of sheep'], [6, 6],
              'Two pests: 3(2) each, 2 for the pest, 2 for the damage and 2 for the named crop or animal. The scheme gives these two as examples.')],
        twoof + ' ' + insects, node='2-4|3-5')
    members = [('i', 'Flushing', 'Stocking heavily on bare pasture (or put on a low plane of nutrition)|release on to better pasture (or put on a higher plane of nutrition) prior to mating'),
               ('i', 'Sponging', 'Insertion of progesterone-impregnated sponges into ewe’s vagina|to synchronise breeding or for breeding (or lambing) out of season'),
               ('ii', 'Aspect', 'Direction (south or north)|a field is facing'), ('ii', 'Topography', 'Landscape shape (or lie of the land)|sloped or flat'),
               ('iii', 'Zoonoses', 'Animal diseases|transmissible to humans'), ('iii', 'Notifiable diseases', 'Must be reported (to relevant authority)|quarantine|national importance|animals slaughtered'),
               ('iv', 'Stem tuber', '(Modified stem) with buds|food store|more starch (than rhizome)'), ('iv', 'Rhizome', '(Modified stem) with nodes|spreads horizontally|less starch (than tuber)')]
    add('q8c', 'Q8(c)', '4-3-2', 'distinguishing-paired-terms',
        'Distinguish clearly between the members of any three of the following pairs of terms: (i) Flushing and sponging (ii) Aspect and topography (iii) Zoonoses and notifiable diseases (iv) Stem tuber and rhizome.',
        [menu(pool, [2, 2], f'({k}) {label}: two points, 2(2).' + (' Two points per term for any three pairs (3{2[2(2)]}).' if i == 0 else ''))
         for i, (k, label, pool) in enumerate(members)],
        twoof, marks=24, tariff={'kind': 'bestNofParts', 'answer': 6, 'ofParts': 8, 'perPart': 4},
        selection=closed(3, ['i', 'ii', 'iii', 'iv']), node='3-4|1-0|3-5|2-0')
    # Question 9 -------------------------------------------------------------
    why = 'Give scientific explanations for any four of the following.'
    for key, ref, topic, concept, item, points, node in [
            ('q9a', 'Q9(a)', '4-3-2', 'pig-temperature-weight-gain', 'The influence of environmental temperature on weight gain in pigs.', 'Correct (or critical) temperature gives better FCR|food consumed goes to body mass rather than to maintain body temperature|reach slaughter mass faster|correct temperature for one specified house|in low temperatures they consume too much feed (or eat less at higher temperature)', None),
            ('q9b', 'Q9(b)', '3-3-2', 'dense-conifer-planting', 'The dense planting of coniferous trees in a forestry plantation.', 'Taller (or straighter) trees or increased competition|free from knots (or better quality timber)|prevents weeds|provides thinnings|provides shelter belt|allows for failed trees', None),
            ('q9c', 'Q9(c)', '2-2-3', 'earthworms-cultivated-soils', 'The low earthworm population in intensively cultivated soils.', 'Machinery damage|exposed to predation during cultivation|low OM|increased use of chemical sprays|compaction (or poor aeration)', None),
            ('q9d', 'Q9(d)', '4-1', 'grit-in-poultry', 'The presence of grit in the digestive tract of free-range poultry.', '(Birds have) no teeth|gizzard|muscular|(grit) grinds down|hard coat of (cereal) grains (or allows digestion of (cereal) grains)|improves shell quality', None),
            ('q9e', 'Q9(e)', '2-3', 'deep-ploughing-podzols', 'The deep ploughing of podzolic soils.', 'Breaks iron pan|improves drainage|improves aeration|restores soil nutrients (or recovers leached minerals)|allows penetration of roots', '1-5|1-0')]:
        add(key, ref, topic, concept, 'Give a scientific explanation for: ' + item, [menu(points, [4, 4, 4], 'Any three points, 4 marks each (3(4)).')], why, node=node)
    assert len(p.tasks) == 58, len(p.tasks)
    return p


def reviewed_tasks():
    p = build()
    return p.cards, p.tasks


def paper_review():
    return build().review('58 base tasks, one card each. A scale the scheme prints across a part\'s (i) and (ii) (Q1(a), (b), (c), (h), (i)) is one task with the scale stated; '
                          'parts priced separately are separate tasks. Q3 Option Two (b) cereals, Q4(a) and Q4(b) methods and Q5(a)(ii) quantitative milk tests are answer routes; '
                          'Q8(c) is one card for the choice of three pairs from four.')
