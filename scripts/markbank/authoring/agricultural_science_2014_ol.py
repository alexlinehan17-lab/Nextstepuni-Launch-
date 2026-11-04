"""2014 Ordinary: every task authored from the SEC paper and marking scheme (no cards existed).

All 12 paper pages and 16 scheme pages were inspected and the independent census transcribed
before authoring: 61 base tasks, one card each. Section One questions are one task each, their
rows carrying the scheme's own marks (5 × 4m, 5 × (2m + 2m), 10 × 2m, and the per-part values of
Q4 and Q6). Section Two parts are priced on their own. The Q12(d) cross is one task because its
genotype and phenotype marks are tied line to line. Answers are the scheme's words.
"""
from agricultural_science_legacy import Paper, P, point, menu

FILE = 'LC024GLP000EV.pdf'
HASHES = {'exampapers': '9b45f4d47b5ce5deb0c1d70a46aea8093f17b3bd9460f05b9a2e04f6a6529958',
          'markingschemes': '19a6b5e1223a5cbd18178276d5c8a02ef7147cb85c419a61c081158d7823617a'}
SELECTIONS = {
    'ba59808665c9a3f1': ('exam-selection', 'Section One: six of seven independent 20-mark questions; every question is retained.'),
    '31d5766099026bef': ('open', 'Q6(b): any three types of tooth from the scheme\'s four; a marking menu.'),
    '1e8340f70da27719': ('exam-selection', 'Section Two: three of six independent 60-mark questions; every question is retained.'),
    '6eedd04e4a43a9d9': ('not-a-selection', '"The rumen is one of the calf’s stomach chambers" is the lead-in to Q8(d), not a choice.'),
    '907570a8c348a827': ('independent-task-selection', 'Q13: two of four independently priced 30-mark parts; all four are retained.'),
}
SUPPLEMENTARY = []
ATLAS = {
    'Q1': 'animal-production', 'Q2': 'crop-production', 'Q3': 'animal-diseases', 'Q4': 'crop-production|classification-of-organisms',
    'Q5': 'animal-production|plant-physiology|crop-production|grassland|animal-diseases|scientific-practices-experiments-investigations|fertilisers-pollution-the-environment',
    'Q6': 'animal-physiology', 'Q7': 'crop-production|animal-production|soil-science|fertilisers-pollution-the-environment',
    'Q8': 'animal-production', 'Q8(c)': 'animal-production|animal-diseases', 'Q8(d)': 'animal-physiology',
    'Q9': 'grassland', 'Q9(d)': 'grassland|fertilisers-pollution-the-environment', 'Q9(d)(ii)': 'grassland|scientific-practices-experiments-investigations',
    'Q10': 'animal-production', 'Q10(d)': 'animal-diseases',
    'Q11': 'soil-science', 'Q11(b)(iii)': 'soil-science|scientific-practices-experiments-investigations',
    'Q12': 'genetics', 'Q12(b)': 'genetics|animal-production',
    'Q13(a)': 'grassland', 'Q13(a)(iv)': 'grassland|scientific-practices-experiments-investigations', 'Q13(b)': 'plant-physiology|crop-production',
    'Q13(b)(iv)': 'plant-physiology|scientific-practices-experiments-investigations', 'Q13(c)': 'soil-science|classification-of-organisms',
    'Q13(c)(iv)': 'soil-science|scientific-practices-experiments-investigations', 'Q13(d)': 'animal-production|animal-physiology',
    'Q13(d)(iv)': 'animal-production|scientific-practices-experiments-investigations',
}
REGIONS = {
    # Drafted by regions.py.
    'Q1': (P((2, 0.259, 0.775)), P((5, 0.118, 0.303))),
    'Q2': (P((3, 0.031, 0.957)), P((5, 0.303, 0.476))),  # trimmed above the page footer
    'Q3': (P((4, 0.046, 0.879)), P((5, 0.476, 0.870))),  # trimmed above the page footer
    'Q4': (P((5, 0.046, 0.857)), P((6, 0.080, 0.327))),  # trimmed above the page footer
    'Q5': (P((6, 0.046, 0.471)), P((6, 0.327, 0.539))),
    'Q6': (P((6, 0.471, 0.914)), P((6, 0.539, 0.946))),
    'Q7': (P((7, 0.046, 0.778)), P((7, 0.080, 0.307))),  # trimmed above the page footer
    'Q8(a)': (P((8, 0.219, 0.294)), P((8, 0.124, 0.271))),
    'Q8(b)': (P((8, 0.219, 0.249), (8, 0.294, 0.339)), P((8, 0.124, 0.157), (8, 0.271, 0.354))),
    'Q8(c)(i)': (P((8, 0.219, 0.249), (8, 0.339, 0.373)), P((8, 0.124, 0.157), (8, 0.354, 0.451))),
    'Q8(c)(ii)': (P((8, 0.219, 0.249), (8, 0.373, 0.399)), P((8, 0.124, 0.157), (8, 0.451, 0.517))),
    'Q8(d)(i)': (P((8, 0.219, 0.249), (8, 0.399, 0.433)), P((8, 0.124, 0.157), (8, 0.517, 0.599))),
    'Q8(d)(ii)': (P((8, 0.219, 0.249), (8, 0.399, 0.418), (8, 0.433, 0.449)), P((8, 0.124, 0.157), (8, 0.599, 0.664))),
    'Q8(d)(iii)': (P((8, 0.219, 0.249), (8, 0.399, 0.418), (8, 0.449, 0.549)), P((8, 0.124, 0.157), (8, 0.664, 0.695))),  # trimmed above the page footer
    'Q9(a)(i)': (P((8, 0.549, 0.599)), P((9, 0.097, 0.195))),
    'Q9(a)(ii)': (P((8, 0.549, 0.580), (8, 0.599, 0.625)), P((9, 0.097, 0.129), (9, 0.195, 0.277))),
    'Q9(b)(i)': (P((8, 0.549, 0.580), (8, 0.625, 0.659)), P((9, 0.097, 0.129), (9, 0.277, 0.359))),
    'Q9(b)(ii)': (P((8, 0.549, 0.580), (8, 0.625, 0.644), (8, 0.659, 0.685)), P((9, 0.097, 0.129), (9, 0.359, 0.474))),
    'Q9(c)': (P((8, 0.549, 0.580), (8, 0.685, 0.715)), P((9, 0.097, 0.129), (9, 0.474, 0.555))),
    'Q9(d)(i)': (P((8, 0.549, 0.580), (8, 0.715, 0.749)), P((9, 0.097, 0.129), (9, 0.555, 0.605))),
    'Q9(d)(ii)': (P((8, 0.549, 0.580), (8, 0.715, 0.734), (8, 0.749, 0.782)), P((9, 0.097, 0.129), (9, 0.605, 0.685))),  # trimmed above the page footer
    'Q10(a)': (P((9, 0.031, 0.106)), P((10, 0.097, 0.227))),
    'Q10(b)(i)': (P((9, 0.031, 0.061), (9, 0.106, 0.1395)), P((10, 0.097, 0.129), (10, 0.228, 0.320))),  # hand-set: the scheme heads these Flushing: and Sponging: rather than (i) and (ii)
    'Q10(b)(ii)': (P((9, 0.031, 0.061), (9, 0.106, 0.124), (9, 0.1395, 0.155)), P((10, 0.097, 0.129), (10, 0.343, 0.434))),  # hand-set: the scheme heads these Flushing: and Sponging: rather than (i) and (ii)
    'Q10(c)': (P((9, 0.031, 0.061), (9, 0.166, 0.195)), P((10, 0.097, 0.129), (10, 0.457, 0.523))),
    'Q10(d)(i)': (P((9, 0.031, 0.061), (9, 0.195, 0.403)), P((10, 0.097, 0.129), (10, 0.523, 0.572))),
    'Q10(d)(ii)': (P((9, 0.031, 0.061), (9, 0.195, 0.384), (9, 0.403, 0.418)), P((10, 0.097, 0.129), (10, 0.572, 0.621))),
    'Q10(d)(iii)': (P((9, 0.031, 0.061), (9, 0.195, 0.384), (9, 0.418, 0.433)), P((10, 0.097, 0.129), (10, 0.621, 0.687))),
    'Q10(d)(iv)': (P((9, 0.031, 0.061), (9, 0.195, 0.384), (9, 0.433, 0.489)), P((10, 0.097, 0.129), (10, 0.687, 0.750))),  # trimmed above the page footer
    'Q11(a)': (P((9, 0.489, 0.745)), P((11, 0.097, 0.277))),
    'Q11(b)(i)': (P((9, 0.489, 0.519), (9, 0.745, 0.779)), P((11, 0.097, 0.129), (11, 0.277, 0.375))),
    'Q11(b)(ii)': (P((9, 0.489, 0.519), (9, 0.745, 0.764), (9, 0.779, 0.794)), P((11, 0.097, 0.129), (11, 0.375, 0.457))),
    'Q11(b)(iii)': (P((9, 0.489, 0.519), (9, 0.745, 0.764), (9, 0.794, 0.834)), P((11, 0.097, 0.129), (11, 0.457, 0.555))),
    'Q11(c)(i)': (P((9, 0.489, 0.519), (9, 0.834, 0.869)), P((11, 0.097, 0.129), (11, 0.555, 0.638))),
    'Q11(c)(ii)': (P((9, 0.489, 0.519), (9, 0.834, 0.854), (9, 0.869, 0.936)), P((11, 0.097, 0.129), (11, 0.638, 0.734))),  # trimmed above the page footer
    'Q12(a)(i)': (P((10, 0.031, 0.095)), P((12, 0.097, 0.196))),
    'Q12(a)(ii)': (P((10, 0.031, 0.080), (10, 0.095, 0.110), (10, 0.130, 0.296)), P((12, 0.097, 0.129), (12, 0.196, 0.245))),  # with the mitosis diagram printed under (iii)
    'Q12(a)(iii)': (P((10, 0.031, 0.080), (10, 0.110, 0.300)), P((12, 0.097, 0.129), (12, 0.245, 0.295))),
    'Q12(a)(iv)': (P((10, 0.031, 0.080), (10, 0.300, 0.360)), P((12, 0.097, 0.129), (12, 0.295, 0.343))),
    'Q12(b)(i)': (P((10, 0.031, 0.061), (10, 0.360, 0.395)), P((12, 0.097, 0.129), (12, 0.343, 0.393))),
    'Q12(b)(ii)': (P((10, 0.031, 0.061), (10, 0.360, 0.380), (10, 0.395, 0.414)), P((12, 0.097, 0.129), (12, 0.393, 0.525))),  # stops above the (c)/(d) answer-book instruction
    'Q12(c)(i)': (P((10, 0.031, 0.061), (10, 0.480, 0.646)), P((12, 0.097, 0.129), (12, 0.525, 0.574))),
    'Q12(c)(ii)': (P((10, 0.031, 0.061), (10, 0.480, 0.616), (10, 0.646, 0.676)), P((12, 0.097, 0.129), (12, 0.525, 0.547), (12, 0.574, 0.607))),
    'Q12(c)(iii)': (P((10, 0.031, 0.061), (10, 0.480, 0.616), (10, 0.676, 0.736)), P((12, 0.097, 0.129), (12, 0.525, 0.547), (12, 0.607, 0.640))),
    'Q12(d)': (P((10, 0.031, 0.061), (10, 0.736, 0.923)), P((12, 0.097, 0.129), (12, 0.640, 0.785))),  # trimmed above the page footer
    'Q13(a)(i)': (P((11, 0.046, 0.140)), P((13, 0.097, 0.195))),
    'Q13(a)(ii)': (P((11, 0.046, 0.125), (11, 0.140, 0.155)), P((13, 0.097, 0.162), (13, 0.195, 0.227))),
    'Q13(a)(iii)': (P((11, 0.046, 0.125), (11, 0.155, 0.170)), P((13, 0.097, 0.162), (13, 0.227, 0.261))),
    'Q13(a)(iv)': (P((11, 0.046, 0.125), (11, 0.170, 0.226)), P((13, 0.097, 0.162), (13, 0.261, 0.393))),
    'Q13(b)(i)': (P((11, 0.046, 0.106), (11, 0.226, 0.260)), P((13, 0.097, 0.162), (13, 0.393, 0.458))),
    'Q13(b)(ii)': (P((11, 0.046, 0.106), (11, 0.226, 0.245), (11, 0.260, 0.275)), P((13, 0.097, 0.162), (13, 0.458, 0.508))),
    'Q13(b)(iii)': (P((11, 0.046, 0.106), (11, 0.226, 0.245), (11, 0.275, 0.290)), P((13, 0.097, 0.162), (13, 0.508, 0.590))),
    'Q13(b)(iv)': (P((11, 0.046, 0.106), (11, 0.226, 0.245), (11, 0.290, 0.346)), P((13, 0.097, 0.162), (13, 0.590, 0.687))),  # trimmed above the page footer
    'Q13(c)(i)': (P((11, 0.046, 0.106), (11, 0.346, 0.380)), P((13, 0.097, 0.162), (14, 0.097, 0.146))),
    'Q13(c)(ii)': (P((11, 0.046, 0.106), (11, 0.346, 0.365), (11, 0.380, 0.395)), P((13, 0.097, 0.162), (14, 0.146, 0.261))),
    'Q13(c)(iii)': (P((11, 0.046, 0.106), (11, 0.346, 0.365), (11, 0.395, 0.410)), P((13, 0.097, 0.162), (14, 0.261, 0.310))),
    'Q13(c)(iv)': (P((11, 0.046, 0.106), (11, 0.346, 0.365), (11, 0.410, 0.466)), P((13, 0.097, 0.162), (14, 0.310, 0.457))),
    'Q13(d)(i)': (P((11, 0.046, 0.106), (11, 0.466, 0.500)), P((13, 0.097, 0.162), (14, 0.457, 0.508))),
    'Q13(d)(ii)': (P((11, 0.046, 0.106), (11, 0.466, 0.485), (11, 0.500, 0.515)), P((13, 0.097, 0.162), (14, 0.508, 0.622))),
    'Q13(d)(iii)': (P((11, 0.046, 0.106), (11, 0.466, 0.485), (11, 0.515, 0.531)), P((13, 0.097, 0.162), (14, 0.622, 0.688))),
    'Q13(d)(iv)': (P((11, 0.046, 0.106), (11, 0.466, 0.485), (11, 0.531, 0.552)), P((13, 0.097, 0.162), (14, 0.688, 0.785))),  # trimmed above the page footer
}
FIGURES = {
    'q2': ('agsci-2014-ol-paper-cereal-equipment', [('A', 'Roller', True), ('B', 'Combine (harvester)', True), ('C', 'Harrow / grubber', True), ('D', 'Seed drill / one pass', True), ('E', 'Sprayer', True)]),
    'q4': ('agsci-2014-ol-paper-cranefly', None),
    'q6': ('agsci-2014-ol-paper-sheep-skull', None),
    'q10di': ('agsci-2014-ol-paper-liver-fluke', None), 'q10dii': ('agsci-2014-ol-paper-liver-fluke', None),
    'q10diii': ('agsci-2014-ol-paper-liver-fluke', None), 'q10div': ('agsci-2014-ol-paper-liver-fluke', None),
    'q12aii': ('agsci-2014-ol-paper-mitosis', None), 'q12aiii': ('agsci-2014-ol-paper-mitosis', None),
}


def figured(card, key):
    figure, labels = FIGURES[key]
    card['figureKey'] = figure
    if labels:
        card['labelKey'] = [dict(letter=l, meaning=m, askedInThisQuestion=a) for l, m, a in labels]
    return card


def build():
    p = Paper(2014, 'ordinary', FILE, HASHES, REGIONS, ATLAS, 12, 16, SELECTIONS, SUPPLEMENTARY,
              section=lambda ref: 'A' if int(ref.split('(')[0].split(' ')[0][1:]) <= 7 else 'B')
    add = p.add
    # Section One ------------------------------------------------------------
    add('q1', 'Q1', '4-2', 'breed-descriptions',
        'A list of common animal breeds is given below. Place these in Column A to match a description of each breed in Column B. The first one is completed as an example. '
        'List: Charolais; Landrace; Scottish blackface; Friesian; Hereford; Texel. Example: Charolais — Continental beef breed. '
        'Column B: Lowland sheep breed; Pig breed; Dual-purpose breed; Mountain sheep breed; British beef breed.',
        [point('Lowland sheep breed — Texel', 4, 'One breed for each description, 4 marks each (5 × 4m).'), point('Pig breed — Landrace', 4), point('Dual-purpose breed — Friesian', 4),
         point('Mountain sheep breed — Scottish blackface', 4), point('British beef breed — Hereford', 4)],
        tariff={'kind': 'fixed', 'notation': '5 × 4m'}, node='3-1')
    figured(add('q2', 'Q2', '3-3-1', 'cereal-equipment-and-order',
                'All the equipment shown below is used in cereal production. In the table below: (a) Write the names of the pieces of equipment to match the letters under the photographs. '
                '(b) Number the pieces of equipment (1 – 5) in the order in which they are normally used in cereal production. (Used first = 1; Used last = 5). Letters A, B, C, D, E.',
                [menu(['A Roller 3 [Accept 2]', 'B Combine (harvester) 5', 'C Harrow / grubber 1', 'D Seed drill / one pass 2 [Accept 3]', 'E Sprayer 4'], [4] * 5,
                      '5 × (2m + 2m): for each letter, (a) the equipment name 2 and (b) its order of use 2 (the number after the name).')],
                tariff={'kind': 'fixed', 'notation': '5 × (2m + 2m)'}, node='2-3|2-5'), 'q2')
    diseases = [('Red water fever', 'Cattle', 'Red coloured urine / diarrhoea / increased pulse rate'), ('Orf', 'Sheep / human', 'Lesions or sores or spots on mouth (or udder or genitals)'),
                ('Anaemia', 'Pigs', 'Pale skin / weight loss / rapid breathing / weakness / scour'),
                ('Viral pneumonia', 'Cattle / sheep / pigs', '(Severe) coughing / rapid breathing / weight loss / discharge from eyes or nose / high temperature / fever'),
                ('Grass tetany', 'Cattle / sheep', 'Staggering / muscle twitching or tremors / falling down / coma / frothing at mouth / (sudden) death')]
    add('q3', 'Q3', '4-3-3', 'common-animal-diseases',
        'Give a brief account of each of the following common animal diseases, stating the type of animal affected and a symptom: (a) Red water fever (b) Orf (c) Anaemia (d) Viral pneumonia (e) Grass tetany.',
        [menu([f'{d}: Type of animal affected: {a} Symptom: {s}' for d, a, s in diseases], [4] * 5,
              '5 × (2m + 2m): for each disease, the type of animal affected 2 and one symptom (any one) 2.')],
        tariff={'kind': 'fixed', 'notation': '5 × (2m + 2m)'}, node='3-5')
    figured(add('q4', 'Q4', '3-3-2', 'cranefly-life-cycle',
                'The adult and the larva of a common crop pest are shown below. (a) Name the adult insect shown. (b) State the common name for the larva shown. '
                '(c) (i) Name the other two stages in the life cycle of this insect. (ii) What name is given to the type of insect life cycle, such as the one above, that has four different stages? '
                '(iii) Name another insect that has a similar type of life cycle. (d) Name a crop that is attacked by the pest shown in the diagram above.',
                [point('(a) Adult — Cranefly or daddy-long-legs', 3), point('(b) Larva — Leatherjacket', 3),
                 menu(['1. Egg', '2. Pupa / cocoon'], [2, 2], '(c)(i) The other two stages, 2m each.'),
                 point('(c)(ii) Life cycle — Complete metamorphosis', 4), point('(c)(iii) Another insect — Butterfly / click beetle / fly / bee', 3),
                 point('(d) Crop attacked — Grass / cereals or named cereal / potatoes', 3)],
                tariff={'kind': 'fixed', 'notation': '3 + 3 + 2 + 2 + 4 + 3 + 3'}, node='2-4|3-1'), 'q4')
    statements = [('a', 'Ewes are in lamb for 283 days.', 'F'), ('b', 'Buttercup is a member of the family Compositae (Asteraceae).', 'F'), ('c', 'A bullock is another name for a steer.', 'T'),
                  ('d', 'Lodging means the collapse of a crop.', 'T'), ('e', 'In set stocking land is divided into small areas for grazing.', 'F'), ('f', 'Tuberculosis (TB) is a notifiable disease.', 'T'),
                  ('g', 'A line transect is used in ecology.', 'T'), ('h', 'Silage effluent is a serious cause of water pollution.', 'T'),
                  ('i', 'Ground rock phosphate is used as a fertiliser in forestry production.', 'T'), ('j', 'The potato plant stores food in rhizomes.', 'F')]
    add('q5', 'Q5', '4-1', 'true-or-false-farm-science',
        'Indicate if the following statements are true (T) or false (F) by placing a circle around the correct answer in each case. An example is shown. '
        'Example: Rice is a cereal crop grown in Ireland — F. ' + ' '.join(f'({k}) {s}' for k, s, _ in statements),
        [menu([f'({k}) {a}' for k, _, a in statements], [2] * 10, 'All ten statements, 2 marks each (10 × 2m). T = true, F = false; the scheme gives each letter with T or F.')],
        tariff={'kind': 'fixed', 'notation': '10 × 2m'}, node='3-0|2-1|2-4|2-6|3-5|0-1|1-6')
    figured(add('q6', 'Q6', '4-1', 'sheep-skull-and-dentition',
                'The photograph shows the skull of a sheep, which is a herbivore. (a) Explain the term herbivore. (b) Name any three types of tooth that can be seen in the photograph. '
                '(c) Complete the following table to show the dental formula of the sheep (incisors, canines, pre-molars, molars). '
                '(d) Describe one way in which the dental arrangement of a sheep is different to that of a pig.',
                [point('(a) Herbivore: An animal that feeds on plants (only)', 2),
                 menu('Incisors|premolars|molars|canines', [2] * 3, '(b) Any three, 2 marks each (3 × 2m).'),
                 menu(['0 0 3 3 3 1 3 3', '0 0 3 3 4 0 3 3'], [8],
                      '(c) The dental formula, upper jaw over lower jaw for incisors, canines, pre-molars and molars: 4 × 2m, one per tooth type. The scheme accepts either table.'),
                 point('(d) Sheep dentition: absence of canines / lack of canines on upper jaw / lack of incisors on upper jaw / number of teeth (32 v 44) / dental pad (at front) on upper jaw', 4)],
                tariff={'kind': 'fixed', 'notation': '2 + 3 × 2m + 4 × 2m + 4m'}, node='3-0'), 'q6')
    add('q7', 'Q7', '2-3', 'reasons-for-farm-practices',
        'Give a scientific reason in each case why the following practices are carried out on Irish farms. (a) Selective herbicide is sprayed on cereal crops. (b) Beet tops are left to wilt before feeding to animals. '
        '(c) Tail paint is applied to cows. (d) Lime is regularly spread on soil. (e) Farm hedges are trimmed only after the first of September.',
        [point('(a) Selective herbicide — Eliminates or kills (broad leaved) weeds / kills weeds but does not damage crop plants / makes harvesting easier', 4, 'One reason for each practice, 4 marks each (5 × 4m).'),
         point('(b) Wilting beet tops — Prevents scour in animals / prevents digestive problems / reduces oxalic acid', 4),
         point('(c) Tail paint — To indicate when the cow is on heat / heat detection / records attempted mating', 4),
         point('(d) Spreading lime — Increases pH / reduces acidity / improves soil structure / supplies calcium / improves drainage / improves aeration / promotes flocculation / increases availability of nutrients / increases CEC', 4),
         point('(e) Trimming hedges after September — Prevents harm to wildlife or nesting birds / legal requirement / increases biodiversity', 4)],
        tariff={'kind': 'fixed', 'notation': '5 × 4m'}, node='2-4|3-4|1-2|1-6')
    # Question 8 -------------------------------------------------------------
    add('q8a', 'Q8(a)', '4-3-2', 'successful-calving-steps', 'Calving is a very important event on the dairy farm. List four steps the farmer can take to help successful calving.',
        [menu('Sire selection|record date of insemination|steaming up|cow at correct BCS (3 – 3.5)|reduce meal intake in final week|isolate cow before calving|clean calving box|adequate supervision|assist if necessary|call vet|proper equipment|farmer hygiene|clear airways or make sure calf breathing|make sure cow licks calf|iodine on navel|colostrum',
              [4] * 4, 'Any four, 4 marks each (4 × 4m).')], node='3-4|3-5')
    add('q8b', 'Q8(b)', '4-3-2', 'colostrum-versus-milk', 'Colostrum is produced by the cow immediately after calving. Give two differences between colostrum and milk.',
        [menu('Rich in antibodies|provides immunity|rich in nutrients or named nutrient|laxative effect|thicker|yellow in colour|higher in solids or lower water content', [4, 4],
              'Colostrum: any two, 4 marks each (2 × 4m).')], node='3-4')
    add('q8ci', 'Q8(c)(i)', '4-3-3', 'calf-rearing-hygiene', 'Good hygiene is essential for calf health. Describe three ways in which the farmer ensures good hygiene in calf-rearing.',
        [menu('Clean housing or named example (e.g. wash floors or lime on floors)|fresh straw|remove mucus|clean buckets|separation from cow after birth|iodine on navel|clean water supply|disease control|isolation of cow prior to calving',
              [4] * 3, 'Any three, 4 marks each (3 × 4m).')], node='3-5')
    add('q8cii', 'Q8(c)(ii)', '4-3-3', 'calf-diseases', 'Name two common diseases of calves.',
        [menu('Scour|joint-ill|navel ill|(viral) pneumonia|ringworm|lungworm|stomach worm|lice or any one named ectoparasite', [4, 4], 'Any two, 4 marks each (2 × 4m).')], node='3-5')
    rumen = 'The rumen is one of the calf’s stomach chambers.'
    add('q8di', 'Q8(d)(i)', '4-1', 'rumen-function', 'What is the main function of the rumen?',
        [menu('Digestion of cellulose|contains bacteria|digestion of roughage or named roughage|stores food|makes vitamins|makes protein', [3], 'Any one, 3m.')], rumen, node='3-0')
    add('q8dii', 'Q8(d)(ii)', '4-1', 'rumen-development', 'How can the rumen be helped to develop in the young calf?',
        [menu('Feeding of hay or straw|scratch factor|feeding of concentrates|creep feeding', [4], 'Any one, 4m.')], rumen, node='3-0|3-4')
    add('q8diii', 'Q8(d)(iii)', '4-1', 'other-stomach-chambers', 'Name the three other chambers in the stomach.',
        [menu('Reticulum|omasum|abomasum', [3] * 3, 'All three, 3 marks each (3 × 3m).')], rumen, node='3-0')
    # Question 9 -------------------------------------------------------------
    add('q9ai', 'Q9(a)(i)', '3-3-1', 'common-grass-species', 'Name two species of grass commonly sown on Irish farms.',
        [menu('Perennial ryegrass or PRG|Italian ryegrass or IRG|Timothy|Cocksfoot|Meadow fescue|Meadow foxtail', [3, 3], 'Any two, 3 marks each (2 × 3m).')], node='2-6')
    add('q9aii', 'Q9(a)(ii)', '3-3-1', 'clover-benefits', 'Clover is used in grass seed mixtures. Give two benefits of clover.',
        [menu('Nitrogen fixation|protein source|palatable|digestible|good ground cover|weed control|rich in minerals|less N required|saves money|improved productivity of grassland|improved silage if red clover stated',
              [4, 4], 'Any two, 4 marks each (2 × 4m).')], node='2-6')
    paddock = 'Paddock grazing is widely used on dairy farms.'
    add('q9bi', 'Q9(b)(i)', '3-3-2', 'paddock-system-diagram', 'Draw a labelled diagram to show a paddock grazing system.',
        [point('Diagram', None, 'Diagram: 4m, 2m, 0m. The scheme prints no model drawing.', kind='criterion'),
         point('Any two labels', None, 'Labels: any two, 3 marks each (2 × 3m). The scheme does not list the labels.', kind='criterion')],
        paddock, marks=10, tariff={'kind': 'questionTotal', 'notation': '4m, 2m, 0m + 2 × 3m'}, node='2-6')
    add('q9bii', 'Q9(b)(ii)', '3-3-2', 'paddock-advantages', 'Give two advantages of paddock grazing.',
        [menu('Better grass utilisation or less wastage or less trampling|more efficient|time for grass re-growth|easy herd movement|disease prevention|paddocks easily closed off for silage|less stemmy grass or more leafy grass|higher milk yield (in cows) or higher weight gain (in cattle)|less labour',
              [4, 4], 'Any two, 4 marks each (2 × 4m).')], paddock, node='2-6')
    add('q9c', 'Q9(c)', '3-3-2', 'mixed-grazing-benefits', 'Give two benefits of mixed grazing of cattle and sheep.',
        [menu('Increased growth rates in cattle and sheep|increased tillering|nutrient recycling|parasite control|prevents clumps of grass|less wastage of grass|easier management', [4, 4],
              'Any two, 4 marks each (2 x 4m).')], node='2-6')
    can = 'Calcium ammonium nitrate (CAN) is the most widely used fertiliser on Irish farms.'
    add('q9di', 'Q9(d)(i)', '2-3', 'nutrient-in-can', 'What is the main plant nutrient found in CAN?', [point('Nitrogen', 4)], can, node='1-6')
    add('q9dii', 'Q9(d)(ii)', '2-3', 'can-and-grass-growth', 'Describe an experiment to show the effect of CAN on grass growth.',
        [menu('One (or two) plots|suitable plot size e.g. 1m²|fence off|cut grass|apply CAN to one|suitable control|suitable time period|measure grass growth|cut grass|weigh grass|conclusion',
              [4] * 4, 'Any four, 4 marks each (4 × 4m).')], can, node='1-6|2-6|0-1')
    # Question 10 ------------------------------------------------------------
    add('q10a', 'Q10(a)', '4-3-2', 'breeding-ewe-selection', 'List the bodily characteristics to be considered in the selection of breeding ewes in a lowland sheep enterprise.',
        [menu('Sound feet or legs|healthy udder (no mastitis)|few, or no, missing teeth|no mouth defects|good body conformation or described|suitable body condition|healthy or free from diseases|no history of prolapse',
              [4] * 3, 'Any three, 4 marks each (3 × 4m).')], node='3-4')
    practices = 'Explain the following practices commonly used in sheep breeding:'
    add('q10bi', 'Q10(b)(i)', '4-3-2', 'flushing', 'Explain the following practice commonly used in sheep breeding: Flushing.',
        [menu('Ewes on bare pasture|high stocking rate|ewes moved to good pasture (one month) before mating|reduced stocking rate|kept on good pasture (until 3 weeks) after mating|increased number of eggs released|more twins|higher conception rates|more regular heat periods|fewer barren ewes|safer implantation of embryo(s)',
              [4, 4], 'Flushing: any two, 4 marks each (2 × 4m).')], practices, node='3-4')
    add('q10bii', 'Q10(b)(ii)', '4-3-2', 'sponging', 'Explain the following practice commonly used in sheep breeding: Sponging.',
        [menu('Sponge containing hormone or named hormone|ewe’s vagina|removed after 12 - 14 days|PMSG injection|ewes come into heat at same time|compact lambing season|early lamb production|easier management on mixed farm|reduced labour costs|reduced ram:ewe ratio or 1 ram:10 ewes',
              [4, 4], 'Sponging: any two, 4 marks each (2 × 4m).')], practices, node='3-4')
    add('q10c', 'Q10(c)', '4-3-2', 'lamb-diet-changes', 'Describe the changes in the diet of lambs from birth to slaughter.',
        [menu('Colostrum|ewe’s milk|hay|silage|grass|(creep) meal or concentrate feeding', [4] * 3, 'Any three, 4 marks each (3 × 4m).')], node='3-4')
    fluke = 'The photograph below shows an adult liver fluke (Fasciola hepatica), which is a common parasite of sheep.'
    figured(add('q10di', 'Q10(d)(i)', '4-3-3', 'fluke-larval-stage', 'Name one larval stage in the life-cycle of the liver fluke.',
                [menu('Miracidium|redia|sporocyst|cercarium', [4], 'Any one, 4m.')], fluke, node='3-5'), 'q10di')
    figured(add('q10dii', 'Q10(d)(ii)', '4-3-3', 'fluke-secondary-host', 'Name the secondary host of the liver fluke.', [point('Mud snail / freshwater snail', 4)], fluke, node='3-5'), 'q10dii')
    figured(add('q10diii', 'Q10(d)(iii)', '4-3-3', 'fluke-symptom', 'Describe one symptom of liver fluke infestation in sheep.',
                [menu('Loss in weight|failure to thrive|wool loss|anaemia|lump under jaw|diarrhoea|death', [4], 'Any one, 4m.')], fluke, node='3-5'), 'q10diii')
    figured(add('q10div', 'Q10(d)(iv)', '4-3-3', 'fluke-control', 'Give two methods of control of liver fluke.',
                [menu('Drainage|fence off wet land or remove from risky areas|liming (to kill eggs)|dosing or injection|biological control|molluscicides|pour on', [4, 4], 'Any two, 4 marks each (2 × 4m).')],
                fluke, node='3-5'), 'q10div')
    # Question 11 ------------------------------------------------------------
    add('q11a', 'Q11(a)', '2-1', 'podzol-paragraph',
        'Read the following paragraph about the formation and development of podzol soils and match the words from the list below with the numbered spaces. '
        'List: Iron pan; Leaching; Forestry; Iron; B horizon; Lime. Podzols are poor soils with high __1__ and fertiliser requirements. They are formed as a result of __2__. '
        'Aluminium and __3__ are moved from the A horizon to the __4__. Podzols show a distinct red layer called the __5__. Podzols are widely used for __6__.',
        [menu(['poor soils with high lime', 'result of leaching', 'Aluminium and iron', 'to the B horizon', 'called the iron pan', 'widely used for forestry'], [2] * 6,
              'All six spaces, 2 marks each (6 × 2m), in order 1 to 6: lime, leaching, iron, B horizon, iron pan, forestry.')], node='1-0')
    humus = 'Humus is a very important soil component.'
    add('q11bi', 'Q11(b)(i)', '2-2-3', 'humus-benefits', 'Describe three benefits of humus in the soil.',
        [menu('Rich in nutrients or plant food|improves soil structure|dark colour absorbs heat|improves CEC|source of food for soil organisms or increases soil organism population|improves water holding capacity of soil',
              [3] * 3, 'Any three, 3 marks each (3 × 3m).')], humus, node='1-4')
    add('q11bii', 'Q11(b)(ii)', '2-2-3', 'increasing-humus', 'Give two methods of increasing soil humus content.',
        [menu('Add FYM|add slurry|add seaweed|add sewage sludge|green manure|add earthworms|plough in organic matter or named example|crop rotation', [3, 3], 'Any two, 3 marks each (2 × 3m).')],
        humus, node='1-4')
    add('q11biii', 'Q11(b)(iii)', '2-2-3', 'organic-matter-experiment', 'Describe an experiment to estimate the percentage (%) organic matter in a soil sample.',
        [menu('(Empty) crucible or dish|weigh crucible|dry soil sample|place in crucible|mass of dry soil|Bunsen burner|pipe-clay triangle|heat strongly|stir|humus burns red|red colour is gone or smoke stops|re-weigh|loss in mass|calculation',
              [4] * 4, 'Any four, 4 marks each (4 × 4m).')], humus, node='1-4|0-1')
    texture = 'Soil texture influences the crops grown on a farm.'
    add('q11ci', 'Q11(c)(i)', '2-2-2', 'soil-texture', 'Explain what is meant by the term soil texture.',
        [point('% sand, silt and clay in a soil / relative proportions of sand, silt and clay in a soil / how the soil “feels” or described', 5)], texture, node='1-3')
    add('q11cii', 'Q11(c)(ii)', '2-2-2', 'sandy-versus-clay', 'Compare sandy soils and clay soils under the following headings: 1. Drainage. 2. Fertility. 3. Ease of tilling.',
        [menu(['Good drainage', 'Poor drainage'], [2, 2], '1. Drainage: sandy soils, then clay soils, 2 × 2m.'),
         menu(['Less natural fertility', 'Very fertile'], [2, 2], '2. Fertility: sandy soils, then clay soils, 2 × 2m.'),
         menu(['Easily tilled', 'Difficult to till'], [2, 2], '3. Ease of tilling: sandy soils, then clay soils, 2 × 2m.')], texture, node='1-3')
    # Question 12 ------------------------------------------------------------
    mitosis = 'Mitosis is one type of cell division.'
    add('q12ai', 'Q12(a)(i)', '4-1', 'mitosis-stages', 'List the four stages of mitosis in the correct sequence.',
        [point('1. Prophase 2. Metaphase 3. Anaphase 4. Telophase', 8, '4 × 2m. [Award maximum of 6 marks if not in correct sequence]')], mitosis, node='3-6')
    figured(add('q12aii', 'Q12(a)(ii)', '4-1', 'mitosis-stage-shown', 'Which stage of mitosis is shown in the diagram below?', [point('Metaphase', 3)], mitosis, node='3-6'), 'q12aii')
    figured(add('q12aiii', 'Q12(a)(iii)', '4-1', 'metaphase-events', 'Explain what is happening in the stage of mitosis shown below.',
                [menu('Chromosomes in centre of cell|attached to (spindle) fibres', [3], 'Any one, 3m.')], mitosis, node='3-6'), 'q12aiii')
    add('q12aiv', 'Q12(a)(iv)', '4-1', 'other-cell-division', 'Name the other type of cell division.', [point('Meiosis', 3)], mitosis, node='3-6')
    ai = 'The use of A.I. is very common on Irish farms.'
    add('q12bi', 'Q12(b)(i)', '4-3-2', 'ai-meaning', 'What do the letters A.I. stand for?', [point('Artificial insemination', 3)], ai, node='3-4')
    add('q12bii', 'Q12(b)(ii)', '4-3-2', 'ai-advantage-disadvantage', 'State one advantage and one disadvantage of A.I. in cattle.',
        [menu('Choice /superior bulls|lower cost|safer|prevents disease|higher conception rates|less physical damage|sexed semen', [3], 'Advantage: any one, 3m.'),
         menu('More labour|difficulty with heat detection', [3], 'Disadvantage: any one, 3m. [Accept “more expensive” if “lower cost” not given as an advantage]')], ai, node='3-4|3-6')
    pea = ('In pea plants the gene for yellow seed (Y) is dominant over the gene for green seed (y). A pea plant homozygous for yellow colour (YY) was crossed with a pea plant homozygous for green colour (yy). '
           'Copy the following into your answer book and complete the spaces (genotypes in brackets, phenotypes on lines). Genotypes of original parents (YY) × (yy).')
    add('q12ci', 'Q12(c)(i)', '4-1', 'pea-gametes', 'Complete: (i) Possible gametes ( ) × ( )', [point('Possible gametes: (Y) (y)', 8, '2 × 4m.')], pea, node='3-6')
    add('q12cii', 'Q12(c)(ii)', '4-1', 'pea-f1-genotype', 'Complete: (ii) F1 genotype ( )', [point('F1 genotype: (Yy)', 4)], pea, node='3-6')
    add('q12ciii', 'Q12(c)(iii)', '4-1', 'pea-f1-phenotype', 'Complete: (iii) F1 phenotype ___', [point('F1 phenotype: Yellow', 4)], pea, node='3-6')
    add('q12d', 'Q12(d)', '4-1', 'pea-test-cross',
        'In your answerbook show a cross between a homozygous recessive plant and an F1 plant from the above cross. Show the following in your cross: (i) Genotypes of parents ( ) × ( ) '
        '(ii) Possible gametes ( ) × ( ) ( ) (iii) Genotypes of offspring ( ) ( ) (iv) Phenotypes of offspring ___ ___',
        [point('(i) Genotypes of parents: (yy) × (Yy)', 4, '2 × 2m.'), point('(ii) Possible gametes: (y) × (Y) (y)', 6, '3 × 2m.'),
         point('(iii) Genotypes of offspring: (Yy) (yy)', 4, '2 × 2m.'), point('(iv) Phenotypes of offspring: Yellow Green', 4, '2 × 2m.')],
        'In pea plants the gene for yellow seed (Y) is dominant over the gene for green seed (y). A pea plant homozygous for yellow colour (YY) was crossed with a pea plant homozygous for green colour (yy).',
        node='3-6')
    # Question 13 ------------------------------------------------------------
    two = 'Answer any two of the parts (a), (b), (c), (d).'
    silage = two + ' Silage making involves the activity of anaerobic bacteria.'
    germ = two + ' A number of factors are needed for seeds to germinate.'
    worms = two + ' Earthworms are very important in the soil.'
    feed = two + ' Concentrates are commonly fed to farm animals.'
    for key, ref, topic, concept, question, rows, stem, node in [
            ('q13ai', 'Q13(a)(i)', '3-3-3', 'anaerobic', 'Explain the term anaerobic.', [point('Without oxygen (air)', 4)], silage, '2-6'),
            ('q13aii', 'Q13(a)(ii)', '3-3-3', 'silage-bacteria', 'Name two species of bacteria that may be involved in silage making.',
             [menu('Lactobacillus|Streptococcus|Clostridium', [4, 4], 'Any two, 4 marks each (2 × 4m).')], silage, '2-6'),
            ('q13aiii', 'Q13(a)(iii)', '3-3-3', 'anaerobic-silage-pit', 'Describe two ways of ensuring anaerobic conditions in the silage pit.',
             [menu('Rolling|quick filling|avoid air pockets|cover|tyres on top|re-seal', [3, 3], 'Any two, 3 marks each (2 × 3m).')], silage, '2-6'),
            ('q13aiv', 'Q13(a)(iv)', '3-3-3', 'bacteria-in-silage', 'Describe an experiment to show the presence of bacteria in a sample of silage.',
             [menu('Two sterile agar plates|inoculating loop|flame loop|transfer silage onto one plate|control|seal|place in oven|20 - 30°C|2 - 3 days|upside down|examine|bacteria appear as shiny spots|absence of spots in control',
                   [3] * 4, 'Any four, 3 marks each (4 × 3m).')], silage, '2-6|0-1'),
            ('q13bi', 'Q13(b)(i)', '3-1', 'germination', 'Explain the term germination.',
             [point('Growth of a new plant (from a seed) / re-growth of an embryo after dormancy / seed begins to grow / seed sprouts', 3)], germ, '2-0'),
            ('q13bii', 'Q13(b)(ii)', '3-1', 'germination-factors', 'List three factors needed for germination to take place.',
             [menu('Warmth or suitable temperature|moisture or water|oxygen or air', [3] * 3, 'All three, 3 marks each (3 × 3m).')], germ, '2-0'),
            ('q13biii', 'Q13(b)(iii)', '3-3-1', 'maize-under-plastic', 'Give two reasons why maize is commonly sown under plastic.',
             [menu('Keeps soil temperature higher|better germination|weed control|microclimate|earlier germination|longer growing season|higher yield|higher starch content|pest control or named example',
                   [3, 3], 'Any two, 3 marks each (2 × 3m).')], germ, '2-3'),
            ('q13biv', 'Q13(b)(iv)', '3-1', 'percentage-germination', 'Describe an experiment to investigate the percentage (%) germination in a sample of seeds.',
             [menu('Seeds|count|soak seeds (for 24 hours)|seed tray or suitable container|cotton wool or suitable growing medium|warm place|regular watering|leave for suitable time|count sprouted seed|repeat|average|control|calculate % germination',
                   [3] * 4, 'Any four, 3 marks each (4 × 3m). [Award maximum of 9 marks if candidate omits reference to calculation of % germination]')], germ, '2-0|0-1'),
            ('q13ci', 'Q13(c)(i)', '2-2-3', 'earthworm-phylum', 'Name the phylum to which earthworms belong.', [point('Annelida', 3)], worms, '1-4|3-1'),
            ('q13cii', 'Q13(c)(ii)', '2-2-3', 'earthworm-benefits', 'List three ways in which earthworms benefit the soil.',
             [menu('Improve aeration|improve drainage|mix soil (layers)|increase humus content|decompose organic matter|deepen topsoil|(excretory products) add nutrients to soil or improve soil fertility|dead earthworms improve organic matter content of soil|improve soil structure',
                   [3] * 3, 'Any three, 3 marks each (3 × 3m).')], worms, '1-4'),
            ('q13ciii', 'Q13(c)(iii)', '2-2-3', 'increasing-earthworms', 'Outline two ways by which the farmer can increase earthworm numbers in the soil.',
             [menu('Add lime or maintain correct pH|drain soil|add organic matter|aerate soil', [3, 3], 'Any two, 3 marks each (2 × 3m).')], worms, '1-4'),
            ('q13civ', 'Q13(c)(iv)', '2-2-3', 'earthworm-activity-experiment', 'Describe an experiment to show the activity of earthworms in the soil.',
             [menu('Wormery or suitable container described|layers of materials|leaves|add earthworms|cover|leave for suitable time|control|below 10 °C|observe changes in layers|leaves eaten|conclusion',
                   [3] * 4, 'Any four, 3 marks each (4 × 3m).')], worms, '1-4|0-1'),
            ('q13di', 'Q13(d)(i)', '4-3-2', 'concentrate-nutrients', 'Name two food nutrients found in concentrates.',
             [menu('Carbohydates|lipids or fats|protein|vitamins|minerals', [3, 3], 'Any two, 3 marks each (2 × 3m). [Accept named examples]')], feed, '3-4'),
            ('q13dii', 'Q13(d)(ii)', '4-3-2', 'nutrient-functions', 'Describe the function of each of the nutrients referred to in (i).',
             [menu(['Carbohydrate: Energy', 'Lipids: Energy / insulation / protection', 'Protein: Growth / repair',
                    'Vitamins: Prevents deficiency diseases or named deficiency disease / metabolism', 'Minerals: Prevent deficiency diseases or named deficiency disease'],
                   [4, 4], 'Any two, 4 marks each (2× 4m): the functions of your two nutrients.')], feed + ' (i) Name two food nutrients found in concentrates.', '3-0|3-4'),
            ('q13diii', 'Q13(d)(iii)', '4-3-2', 'dry-matter', 'Explain the term dry matter (DM) in relation to animal feed.',
             [point('The part of the food that contains nutrients / the part of the food that remains after water has been removed', 4)], feed, '3-4'),
            ('q13div', 'Q13(d)(iv)', '4-3-2', 'feed-dry-matter-experiment', 'Describe an experiment to measure the dry matter content of a named animal feed.',
             [menu('Named foodstuff|suitable container|mass of container|mass of food stuff|dry in oven|suitable time|new mass|loss in mass|calculation', [3] * 4,
                   'Any four, 3 marks each (4 × 3m). [Award maximum of 9 marks if candidate omits named foodstuff]')], feed, '3-4|0-1')]:
        add(key, ref, topic, concept, question, rows, stem, node=node)
    assert len(p.tasks) == 61, len(p.tasks)
    return p


def reviewed_tasks():
    p = build()
    return p.cards, p.tasks


def paper_review():
    return build().review('61 base tasks, one card each. Section One is one task per question with the scheme\'s own row marks. Section Two parts are priced on their own; '
                          'the Q12(d) cross is one task because its marks are tied line to line.')
