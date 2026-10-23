"""2018 Ordinary: every task authored from the SEC paper and marking scheme (no cards existed).

All 12 paper pages and 20 scheme pages were inspected and the independent census transcribed
before authoring: 60 base tasks, one card each. Every Section One question carries one scale
across all its parts ("10 + 6 + 4(1)": the first correct answer earns 10, the next 6, the rest
1), so each is one task stating its scale (orderedSplit); Question 5's ten statements are one
pool whose first five correct answers earn 3 and the rest 1. Section Two parts are priced on
their own; the potato headings of Q9(a)(ii) and the six sheep terms of Q13(a)(ii) carry their own
marks and are separate tasks. Answers are the scheme's words.
"""
from agricultural_science_legacy import Paper, P, point, menu, closed, routes

FILE = 'LC024GLP000EV.pdf'
HASHES = {'exampapers': 'e5eea810b3bab1e6eaed810445c4bba5c5f82bc82c2ea6749813e9edba0b5092',
          'markingschemes': '026ce005742b5f959b269c48e7339ac770d3c9227d6f01cc741b29d9020bd932'}
SELECTIONS = {
    '394fd85ab87bbd37': ('exam-selection', 'Section One: six of seven independent 20-mark questions; every question is retained.'),
    '59f8b0270bbb55ff': ('exam-selection', 'Section Two: three of six independent 60-mark questions; every question is retained.'),
    '4ee9b623570a63ab': ('not-a-selection', '"Farmers can sow either spring barley or winter barley" is the lead-in to Q11(a), whose table asks for both.'),
    '4a69fade05b74819': ('independent-task-selection', 'Q13: two of four independently priced 30-mark parts; all four are retained.'),
}
SUPPLEMENTARY = [
    (8, 'In the case of one named element', 'closed', 'Q8(b)(iii): the role of any one of nitrogen, phosphorus or potassium. One card lists all three, claim limit one.'),
    (11, 'Give the dental formula for a pig', 'closed', 'Q13(d)(iv): the pig or the sheep formula, kept as answer routes on one card (the scheme accepts two sheep formulas).'),
]
ATLAS = {
    'Q1': 'soil-science', 'Q2': 'animal-production', 'Q3': 'animal-diseases', 'Q4': 'animal-physiology', 'Q5': 'plant-physiology|soil-science|animal-diseases|animal-production',
    'Q6': 'plant-physiology|grassland', 'Q7': 'soil-science|grassland|animal-diseases',
    'Q8(a)': 'fertilisers-pollution-the-environment', 'Q8(b)': 'fertilisers-pollution-the-environment', 'Q8(c)': 'soil-science|scientific-practices-experiments-investigations',
    'Q9': 'crop-production', 'Q9(c)': 'crop-production|scientific-practices-experiments-investigations',
    'Q10': 'genetics', 'Q11': 'crop-production', 'Q11(e)': 'crop-production|scientific-practices-experiments-investigations',
    'Q12': 'grassland', 'Q13(a)': 'animal-production', 'Q13(b)': 'plant-physiology', 'Q13(b)(iv)': 'plant-physiology|scientific-practices-experiments-investigations',
    'Q13(c)': 'animal-production', 'Q13(d)': 'animal-physiology',
}
REGIONS = {
    # Drafted by regions.py (Q13's second printed "(a)" read as (b)); hand-set rows for the separately
    # priced potato headings and sheep terms, and trims where a crop would take a continued header.
'Q1': (P((2, 0.315, 0.788)), P((5, 0.072, 0.347))),
    'Q2': (P((3, 0.043, 0.321)), P((5, 0.347, 0.594))),
    'Q3': (P((3, 0.321, 0.922)), P((5, 0.594, 0.834))),
    'Q4': (P((4, 0.043, 0.789)), P((6, 0.033, 0.429))),
    'Q5': (P((5, 0.043, 0.820)), P((6, 0.429, 0.697))),
    'Q6': (P((6, 0.043, 0.680)), P((6, 0.697, 0.887))),
    'Q7': (P((7, 0.043, 0.794)), P((7, 0.033, 0.365))),
    'Q8(a)(i)': (P((8, 0.227, 0.326)), P((8, 0.053, 0.227))),
    'Q8(a)(ii)': (P((8, 0.227, 0.294), (8, 0.326, 0.378)), P((8, 0.053, 0.084), (8, 0.227, 0.303))),
    'Q8(b)(i)': (P((8, 0.227, 0.262), (8, 0.378, 0.442)), P((8, 0.053, 0.084), (8, 0.303, 0.373))),
    'Q8(b)(ii)': (P((8, 0.227, 0.262), (8, 0.378, 0.410), (8, 0.442, 0.474)), P((8, 0.053, 0.084), (8, 0.373, 0.494), (8, 0.494, 0.512, 0.85, 1))),  # its second 4 sits on the (iii) heading line
    'Q8(b)(iii)': (P((8, 0.227, 0.262), (8, 0.378, 0.410), (8, 0.474, 0.506)), P((8, 0.053, 0.084), (8, 0.494, 0.512, 0, 0.85), (8, 0.512, 0.659))),
    'Q8(c)': (P((8, 0.227, 0.262), (8, 0.506, 0.570)), P((8, 0.053, 0.084), (8, 0.659, 0.816))),
    'Q9(a)(i)': (P((8, 0.570, 0.637)), P((9, 0.033, 0.122))),
    'Q9(a)(ii) — soil preparation': (P((8, 0.570, 0.605), (8, 0.637, 0.796)), P((9, 0.033, 0.064), (9, 0.122, 0.192))),  # its own heading rows
    'Q9(a)(ii) — fertiliser use': (P((8, 0.570, 0.605), (8, 0.637, 0.796)), P((9, 0.033, 0.064), (9, 0.122, 0.139), (9, 0.192, 0.261))),
    'Q9(a)(ii) — weed control': (P((8, 0.570, 0.605), (8, 0.637, 0.796)), P((9, 0.033, 0.064), (9, 0.122, 0.139), (9, 0.261, 0.315))),
    'Q9(a)(ii) — blight control': (P((8, 0.570, 0.605), (8, 0.637, 0.796)), P((9, 0.033, 0.064), (9, 0.122, 0.139), (9, 0.315, 0.392))),
    'Q9(b)': (P((8, 0.570, 0.605), (8, 0.796, 0.828)), P((9, 0.033, 0.064), (9, 0.397, 0.457))),
    'Q9(c)': (P((8, 0.570, 0.605), (8, 0.828, 0.850)), P((9, 0.033, 0.064), (9, 0.457, 0.579))),
    'Q10(a)(i)': (P((9, 0.043, 0.258)), P((10, 0.033, 0.122))),
    'Q10(a)(ii)': (P((9, 0.043, 0.226), (9, 0.258, 0.290)), P((10, 0.033, 0.064), (10, 0.122, 0.139))),
    'Q10(a)(iii)': (P((9, 0.043, 0.226), (9, 0.290, 0.359)), P((10, 0.033, 0.064), (10, 0.139, 0.162))),
    'Q10(b)(i)': (P((9, 0.043, 0.077), (9, 0.359, 0.423)), P((10, 0.033, 0.064), (10, 0.162, 0.213))),
    'Q10(b)(ii)': (P((9, 0.043, 0.077), (9, 0.359, 0.391), (9, 0.423, 0.476)), P((10, 0.033, 0.064), (10, 0.213, 0.238))),
    'Q10(c)': (P((9, 0.043, 0.077), (9, 0.476, 0.727)), P((10, 0.033, 0.064), (10, 0.238, 0.381))),
    'Q10(d)': (P((9, 0.043, 0.077), (9, 0.727, 0.894)), P((10, 0.033, 0.064), (10, 0.381, 0.522))),
    'Q11(a)': (P((10, 0.060, 0.312)), P((11, 0.033, 0.245))),
    'Q11(b)': (P((10, 0.060, 0.094), (10, 0.312, 0.365)), P((11, 0.033, 0.064), (11, 0.245, 0.339))),
    'Q11(c)': (P((10, 0.060, 0.094), (10, 0.365, 0.397)), P((11, 0.033, 0.064), (11, 0.339, 0.431))),
    'Q11(d)(i)': (P((10, 0.060, 0.094), (10, 0.397, 0.460)), P((11, 0.033, 0.064), (11, 0.431, 0.448))),
    'Q11(d)(ii)': (P((10, 0.060, 0.094), (10, 0.397, 0.428), (10, 0.460, 0.492)), P((11, 0.033, 0.064), (11, 0.448, 0.466))),
    'Q11(d)(iii)': (P((10, 0.060, 0.094), (10, 0.397, 0.428), (10, 0.492, 0.524)), P((11, 0.033, 0.064), (11, 0.466, 0.574))),
    'Q11(e)': (P((10, 0.060, 0.094), (10, 0.524, 0.620)), P((11, 0.033, 0.064), (11, 0.574, 0.714))),
    'Q12(a)(i)': (P((10, 0.620, 0.674)), P((12, 0.033, 0.209))),
    'Q12(a)(ii)': (P((10, 0.620, 0.655), (10, 0.674, 0.691)), P((12, 0.033, 0.064), (12, 0.209, 0.348))),
    'Q12(a)(iii)': (P((10, 0.620, 0.655), (10, 0.691, 0.724)), P((12, 0.033, 0.064), (12, 0.348, 0.431))),
    'Q12(b)': (P((10, 0.620, 0.655), (10, 0.724, 0.757)), P((12, 0.033, 0.064), (12, 0.431, 0.770))),  # not the next page's continued header
    'Q12(c)': (P((10, 0.620, 0.655), (10, 0.757, 0.788)), P((12, 0.033, 0.064), (13, 0.064, 0.232))),
    'Q12(d)': (P((10, 0.620, 0.655), (10, 0.788, 0.827)), P((12, 0.033, 0.064), (13, 0.232, 0.606))),
    'Q13(a)(i)': (P((11, 0.043, 0.136)), P((14, 0.033, 0.138))),
    'Q13(a)(ii) — flushing': (P((11, 0.043, 0.109), (11, 0.136, 0.308)), P((14, 0.033, 0.064), (14, 0.138, 0.173), (14, 0.173, 0.313))),  # its own table row
    'Q13(a)(ii) — scanning': (P((11, 0.043, 0.109), (11, 0.136, 0.308)), P((14, 0.033, 0.064), (14, 0.138, 0.173), (14, 0.313, 0.422))),  # its own table row
    'Q13(a)(ii) — steaming up': (P((11, 0.043, 0.109), (11, 0.136, 0.308)), P((14, 0.033, 0.064), (14, 0.138, 0.173), (14, 0.422, 0.527))),  # its own table row
    'Q13(a)(ii) — vaccination': (P((11, 0.043, 0.109), (11, 0.136, 0.308)), P((14, 0.033, 0.064), (14, 0.138, 0.173), (14, 0.527, 0.649))),  # its own table row
    'Q13(a)(ii) — creep feeding': (P((11, 0.043, 0.109), (11, 0.136, 0.308)), P((14, 0.033, 0.064), (14, 0.138, 0.173), (14, 0.649, 0.775))),  # its own table row
    'Q13(a)(ii) — shearing': (P((11, 0.043, 0.109), (11, 0.136, 0.308)), P((14, 0.033, 0.064), (14, 0.138, 0.173), (14, 0.775, 0.856))),  # its own table row
    'Q13(b)(i)': (P((11, 0.043, 0.109), (11, 0.308, 0.604)), P((14, 0.033, 0.064), (15, 0.029, 0.071))),
    'Q13(b)(ii)': (P((11, 0.043, 0.109), (11, 0.308, 0.584), (11, 0.604, 0.621)), P((14, 0.033, 0.064), (15, 0.071, 0.106))),
    'Q13(b)(iii)': (P((11, 0.043, 0.109), (11, 0.308, 0.584), (11, 0.621, 0.638)), P((14, 0.033, 0.064), (15, 0.106, 0.140))),
    'Q13(b)(iv)': (P((11, 0.043, 0.109), (11, 0.308, 0.584), (11, 0.638, 0.689)), P((14, 0.033, 0.064), (15, 0.140, 0.237))),
    'Q13(c)(i)': (P((11, 0.043, 0.109), (11, 0.689, 0.735)), P((14, 0.033, 0.064), (15, 0.237, 0.322))),
    'Q13(c)(ii)': (P((11, 0.043, 0.109), (11, 0.689, 0.716), (11, 0.735, 0.752)), P((14, 0.033, 0.064), (15, 0.237, 0.252), (15, 0.322, 0.374))),
    'Q13(c)(iii)': (P((11, 0.043, 0.109), (11, 0.689, 0.716), (11, 0.752, 0.770)), P((14, 0.033, 0.064), (15, 0.237, 0.252), (15, 0.374, 0.479))),
    'Q13(c)(iv)': (P((11, 0.043, 0.109), (11, 0.689, 0.716), (11, 0.770, 0.787)), P((14, 0.033, 0.064), (15, 0.237, 0.252), (15, 0.479, 0.548))),
    'Q13(c)(v)': (P((11, 0.043, 0.109), (11, 0.689, 0.716), (11, 0.787, 0.821)), P((14, 0.033, 0.064), (15, 0.237, 0.252), (15, 0.548, 0.623))),
    'Q13(d)(i)': (P((11, 0.043, 0.109), (11, 0.821, 0.840)), P((14, 0.033, 0.064), (16, 0.029, 0.105))),
    'Q13(d)(ii)': (P((11, 0.043, 0.109), (11, 0.840, 0.857)), P((14, 0.033, 0.064), (16, 0.105, 0.172))),
    'Q13(d)(iii)': (P((11, 0.043, 0.109), (11, 0.857, 0.874)), P((14, 0.033, 0.064), (16, 0.172, 0.224))),
    'Q13(d)(iv)': (P((11, 0.043, 0.109), (11, 0.874, 0.898)), P((14, 0.033, 0.064), (16, 0.224, 0.530))),  # all three formula tables
}
SHARED = 'Shared scale {}: the first correct answer earns the higher award, whichever part it answers, so no part carries a mark of its own.'
FIGURES = {
    'q1': ('agsci-2018-ol-paper-sedimentation-cylinder', [('A', 'Humus or organic matter or living organisms (the layer floating on the water)', True), ('B', 'Clay (the cloudy water)', True)]),
    'q3': ('agsci-2018-ol-paper-liver-fluke-hosts', None),
    'q4': ('agsci-2018-ol-paper-ruminant-stomach', [('A', 'Rumen', True), ('B', 'Reticulum', True), ('C', 'Omasum', True), ('D', 'Abomasum', True)]),
    'q6': ('agsci-2018-ol-paper-grass-flower', [('A', 'Filament (the scheme allows stamen)', True), ('B', 'Stigma (the scheme allows carpel)', True), ('C', 'Anther: makes pollen', True)]),
    'q10ai': ('agsci-2018-ol-paper-mitosis', [('A', 'Chromatid (or chromosome)', True), ('B', 'Spindle (fibre)', True)]),
    'q10aii': ('agsci-2018-ol-paper-mitosis', None),
    'q10aiii': ('agsci-2018-ol-paper-mitosis', None),
    'q13bi': ('agsci-2018-ol-paper-photosynthesis', None),
    'q13bii': ('agsci-2018-ol-paper-photosynthesis', None),
    'q13biii': ('agsci-2018-ol-paper-photosynthesis', None),
    'q13biv': ('agsci-2018-ol-paper-photosynthesis', None),
}


def split(text, note=None):
    """A row of an orderedSplit card: the scheme prices the scale, not the row."""
    return point(text, None, note)


def figured(card, key):
    figure, labels = FIGURES[key]
    card['figureKey'] = figure
    if labels:
        card['labelKey'] = [dict(letter=l, meaning=m, askedInThisQuestion=a) for l, m, a in labels]
    return card


def build():
    p = Paper(2018, 'ordinary', FILE, HASHES, REGIONS, ATLAS, 12, 20, SELECTIONS, SUPPLEMENTARY,
              section=lambda ref: 'A' if int(ref.split('(')[0].split(' ')[0][1:]) <= 7 else 'B')
    add = p.add
    # Section One: one scale per question --------------------------------------
    figured(add('q1', 'Q1', '2-2-2', 'sedimentation-and-drainage',
                '(a) A soil sample is mixed with water in a graduated cylinder and allowed to settle as shown in the diagram. (i) What soil component is found at A? '
                '(ii) What is the principal type of soil particle found in B? (iii) 1. Would this soil have poor or good drainage? 2. Explain your answer. (b) State two reasons for poor soil drainage.',
                [split('(a)(i) Soil component at A — Humus or organic matter or living organisms (or named example e.g. earthworm)', SHARED.format('10 + 6 + 4(1)') + ' Six answers: (i), (ii), (iii) 1 and 2, and two reasons.'),
                 split('(a)(ii) Principal soil particle type in B — Clay'),
                 split('(a)(iii) 1. Type of drainage — Good'), split('(a)(iii) 2. Explanation — Large amount of sand'),
                 split('(b) Reasons for poor drainage — High clay content or low sand content/ impervious parent material/ iron pan (or hard pan or plough pan)/ soil compaction/ poor soil structure/ poaching damage', 'Any two.')],
                marks=20, tariff={'kind': 'orderedSplit', 'notation': '10 + 6 + 4(1)'}, node='1-3|0-1'), 'q1')
    add('q2', 'Q2', '4-3-1', 'pig-and-sheep-figures',
        'Complete the table in relation to the length of gestation, mass of offspring at birth, and slaughter mass, of the pig and sheep. Table rows: Length of gestation; Mass of offspring at birth (kg); Slaughter mass (kg). Columns: Pig, Sheep.',
        [split('Pig, length of gestation — 3 months, 3weeks, 3days (or 110 – 120 days)', SHARED.format('10 + 6 + 4(1)') + ' Six table cells.'),
         split('Sheep, length of gestation — 5 months (or 145 – 155 days)'), split('Pig, mass of offspring at birth — 1 – 1.5 kg'),
         split('Sheep, mass of offspring at birth — 3 – 5 kg'), split('Pig, slaughter mass — 75 – 90 kg'), split('Sheep, slaughter mass — 35 – 50 kg')],
        marks=20, tariff={'kind': 'orderedSplit', 'notation': '10 + 6 + 4(1)'}, node='3-3')
    figured(add('q3', 'Q3', '4-3-3', 'liver-fluke-hosts-and-control',
                'The three animals shown are involved in the life cycle of the liver fluke. (a) From the animals shown, name the primary host. (b) From the animals shown, name the secondary (intermediate) host. '
                '(c) State three practices carried out on farms to reduce the incidence of liver fluke. (d) Liver fluke is an endoparasite. Explain the term endoparasite. (e) Give an example of one other endoparasite.',
                [split('(a) Liver fluke’s primary host — Sheep', SHARED.format('8 + 7 + 5(1)') + ' Seven answers: (a), (b), three practices, (d) and (e).'),
                 split('(b) Secondary host — Mud snail (or freshwater snail or Limnaea truncatula) [allow snail]'),
                 split('(c) Practices to reduce liver fluke incidence — Drainage/ fencing off wet areas/ remove livestock from risky areas/ apply lime/ ducks and-or geese/ molluscicides/ dosing/ injection or vaccination or pour on', 'Any three.'),
                 split('(d) Endoparasite — A parasite that feeds on the inside of the host (or named host) or an organism that harms another living organism'),
                 split('(e) Another example of endoparasite — Roundworm or stomach worm or lungworm or Babesia or tapeworm or potato bight')],
                marks=20, tariff={'kind': 'orderedSplit', 'notation': '8 + 7 + 5(1)'}, node='3-5'), 'q3')
    figured(add('q4', 'Q4', '4-1', 'ruminant-stomach-parts-roles',
                'The diagram shows the stomach of a ruminant farm animal. (a) Name each labelled part of the stomach (A, B, C, D). (b) State the role of part A and of part D. '
                '(c) Name two farm animals with a ruminant stomach. (d) State one advantage to an animal of having a ruminant stomach.',
                [split('(a) Parts of stomach — A: Rumen, B: Reticulum, C: Omasum, D: Abomasum', SHARED.format('12 + 8(1)') + ' Nine answers: four parts, two roles, two animals and one advantage.'),
                 split('(b) Role of A — To digest cellulose or to digest roughage (or named roughage) or to store food or contains bacteria or makes vitamins or makes protein or mixes food'),
                 split('(b) Role of D — Produces gastric juice or produces enzymes (or named enzyme e.g. pepsin) or digests protein or produces (hydrochloric) acid or lowers pH of food or chemical digestion (of food) or digestion similar to true stomach'),
                 split('(c) Farm animals with ruminant stomach — Sheep/ cattle/ goats/ deer', 'Any two.'),
                 split('(d) Advantage of ruminant stomach — Animal can digest bulky foods (or named bulky food) or animal can digest roughage (or named roughage) or animal can digest cellulose or animal can make (essential) amino acids or animal can make protein')],
                marks=20, tariff={'kind': 'orderedSplit', 'notation': '12 + 8(1)'}, node='3-0'), 'q4')
    statements = [('a', 'Cotyledons store food in seeds', 'T'), ('b', 'Grasses in family Compositae', 'F'), ('c', 'Earthworms are parasites', 'F'),
                  ('d', 'Resazurin solution used to test hygienic quality of milk', 'T'), ('e', 'Vena cava takes blood away from heart', 'F'),
                  ('f', 'Granite is an igneous rock', 'T'), ('g', 'Aphids (greenfly) spread viral diseases', 'T'),
                  ('h', 'Respiration is loss of water vapour from stomata of leaves', 'F'), ('i', 'Footrot is a notifiable disease', 'F'), ('j', 'Hereford is a dairy breed of cattle', 'F')]
    add('q5', 'Q5', '3-1', 'true-or-false-farm-science',
        'Indicate whether each of the following statements is true (T) or false (F) by placing a circle around the correct answer in each case. Example: A cow is a carnivore — F. '
        '(a) Cotyledons store food in seeds. (b) Grasses belong to the plant family Compositae. (c) Earthworms are parasites. (d) Resazurin solution is used to test the hygienic quality of milk. '
        '(e) The vena cava takes blood away from the heart. (f) Granite is an igneous rock. (g) Aphids (greenfly) spread viral diseases. (h) Respiration is the loss of water vapour from stomata in leaves. '
        '(i) Footrot is a notifiable disease. (j) Hereford is a dairy breed of cattle.',
        [menu([f'({k}) {s}: {a}' for k, s, a in statements], [3] * 5 + [1] * 5,
              'All ten statements, 5(3) + 5(1): the first five correct answers earn 3 each and the next five 1 each. T = true, F = false; the scheme words each statement as shown.')],
        tariff={'kind': 'fixed', 'notation': '5(3) + 5(1)'}, node='2-0|1-4|3-5|3-0|1-0|2-4|3-1')
    figured(add('q6', 'Q6', '3-1', 'grass-flower-wind-pollination',
                'The diagram shows a grass flower. (a) Name the parts labelled A and B. What is the role of part C? (b) Grass is wind pollinated. State two features of a grass flower that make it suitable for wind pollination.',
                [split('(a) Parts of grass flower — A: Filament [allow stamen]', SHARED.format('8 + 6 + 3(2)') + ' Five answers: A, B, the role of C and two features.'),
                 split('(a) Parts of grass flower — B: Stigma [allow carpel]'),
                 split('(a) Role of C — To make pollen or to make male gamete (or sperm) or pollination'),
                 split('(b) Features of grass flowers suitable for wind pollination — Anther (or stamen) hangs outside flower/ stigma (or carpel) hangs outside flower/ stigma feathery/ large anther/ pollen light/ pollen smooth/ large amount of pollen/ large stigma', 'Any two.')],
                marks=20, tariff={'kind': 'orderedSplit', 'notation': '8 + 6 + 3(2)'}, node='2-0|2-6'), 'q6')
    add('q7', 'Q7', '2-3', 'reasons-for-farm-practices',
        'Give one scientific reason for each of the following practices carried out on Irish farms: (a) Finding the pH of the soil before sowing a crop. (b) Adding white clover to a seed mixture for a pasture sward. '
        '(c) Topping pastures in summer. (d) Using mineral licks on a dairy farm. (e) Isolating sick animals on a farm.',
        [split('(a) Finding soil pH before sowing — Determines if pH at optimum level for crop or determines if lime required or determines amount of lime required', SHARED.format('8 + 6 + 3(2)') + ' One reason for each of the five practices.'),
         split('(b) Adding white clover to seed mixture — Nitrogen fixation or rich in protein or rich in minerals (or named mineral) or ground cover or weed control or increases palatability or increases productivity (of sward) or high digestibility'),
         split('(c) Topping pastures — Increases tillering or promotes leafy growth or removes stemmy growth or weed control or increases grass growth or increases yield of grass'),
         split('(d) Using mineral licks — Provides mineral (or named mineral) or prevents mineral deficiency (or named mineral deficiency disease) or to supplement poor diet'),
         split('(e) Isolating sick animals — Prevents spread of disease or facilitates treatment of sick animal or ease of access to sick animal or can check sick animal easily')],
        marks=20, tariff={'kind': 'orderedSplit', 'notation': '8 + 6 + 3(2)'}, node='1-2|2-6|3-5')
    # Question 8 -------------------------------------------------------------
    manures = 'Slurry and farmyard manure are two sources of nutrients for crops.'
    add('q8ai', 'Q8(a)(i)', '2-3', 'slurry-versus-fym', 'State two differences between the composition of slurry and farmyard manure.',
        [menu('More water / Less water|No straw / Contains straw|More N / Less N|Less P / More P|Liquid / Solid|Low in organic matter / Rich in organic matter', [4, 4],
              'Any two, 4 marks each (2(4)). Each difference reads slurry, then FYM.')], manures, node='1-6')
    add('q8aii', 'Q8(a)(ii)', '2-3', 'slurry-pollution-steps', 'Slurry may cause water pollution. State two steps farmers may take to reduce the incidence of water pollution by slurry.',
        [menu('Correct application rate|do not spread during wet weather|do not spread on frozen ground|do not spread close to waterways|covered slurry tank|store slurry in leak-proof tanks|use injection system of application', [4, 4],
              'Any two, 4 marks each (2(4)).')], manures, node='1-6')
    npk = '18-6-12 is a compound fertiliser used on farms.'
    add('q8bi', 'Q8(b)(i)', '2-3', 'npk-elements', 'State the principal elements that 18-6-12 provides.',
        [point('Nitrogen', 4, '3(4). The scheme allows symbols, i.e. N P K.'), point('Phosphorus', 4), point('Potassium', 4)], npk, node='1-6')
    add('q8bii', 'Q8(b)(ii)', '2-3', 'artificial-fertiliser-pros-cons', 'State one advantage and one disadvantage of using artificial fertilisers.',
        [point('Advantage — Specially formulated for each crop or farmers knows the amount of nutrient(s) that has been applied to crop or fast-acting or may have a combination of fast and slow acting ingredients or easily absorbed by crop or less bulky or easy to transport or easy to apply or less odour', 4),
         point('Disadvantage — Expensive or may burn crop if too much applied or may cause pollution or easily washed out of soil', 4)], npk, node='1-6')
    add('q8biii', 'Q8(b)(iii)', '2-3', 'npk-element-role', 'In the case of one named element in 18-6-12, state its role in plants.',
        [menu(['Nitrogen: Formation of chlorophyll (or green colour) or prevents chlorosis or increases yield or protein formation or promotes leafy growth',
               'Phosphorus: Necessary for cell division or for energy transfer in cells or seed germination or promotes root growth or enhances seed formation',
               'Potassium: Necessary for protein formation or helps in disease prevention or promotes healthy growth or promotes early ripening or enhances fruit quality'], [4],
              'Any one named element with its role, 4 marks.')], npk, selection=closed(1, ['Nitrogen', 'Phosphorus', 'Potassium']), node='1-6|2-0',
        note='The scheme prints three 4s after (i)\'s 3(4): one beside the disadvantage, one level with the (iii) heading and one beside phosphorus. Part (b) totals 24, so (ii) takes 4 + 4 and (iii) one 4.')
    add('q8c', 'Q8(c)', '2-2-2', 'soil-water-percentage', 'Describe an experiment to find the percentage (%) of water in a soil sample.',
        [menu('Mass of empty (evaporating) basin (or dish) [allow place soil in basin]|find mass of dish + (fresh) soil|subtract to find mass of soil|place basin + soil in oven at 80 – 100 °C (or place basin in oven for 24 hours)|re-weigh to find mass dry soil|repeat until constant mass|subtract to find loss in mass|calculate % water content using: mass of water X 100|repeat to obtain average',
              [4] * 5, 'Any five, 4 marks each (5(4)). The % water is mass of water over mass of (fresh) soil, × 100. Some or all marks may be obtained from labelled diagram(s).')], node='1-3|0-1')
    # Question 9 -------------------------------------------------------------
    add('q9ai', 'Q9(a)(i)', '3-2', 'maincrop-potato-varieties', 'Name two varieties of maincrop potatoes.',
        [menu('Rooster|Kerr Pink|Golden Wonder|Record|Cara|Maris Piper|Pentland Dell', [4, 4], 'Any two, 4 marks each (2(4)).')], node='2-1')
    grow = 'Describe the growing of potatoes under the following headings.'
    add('q9aii-soil', 'Q9(a)(ii) — soil preparation', '3-3-1', 'potato-soil-preparation', 'Describe the growing of potatoes under the heading: 1. Soil preparation.',
        [menu('Plough|rotavate or soil cultivator named|harrow|remove stones|create beds|create drills or ridges', [4, 4], 'Any two, 4 marks each (2(4)).')], grow, node='2-3')
    add('q9aii-fertiliser', 'Q9(a)(ii) — fertiliser use', '3-3-1', 'potato-fertiliser-use', 'Describe the growing of potatoes under the heading: 2. Fertiliser use.',
        [point('Soil test or FYM or 10-10-20 (or 7-6-17) or 7-6-17 produces more floury potato or broadcast fertiliser or fertiliser applied beside seed using potato planter or amount fertiliser depends on soil test results or avoid over-application of N', 4)],
        grow, node='2-3')
    add('q9aii-weeds', 'Q9(a)(ii) — weed control', '3-3-2', 'potato-weed-control', 'Describe the growing of potatoes under the heading: 3. Weed control.',
        [point('Spraying or herbicide or mechanical (or explained e.g. hoeing) or remove by hand or burning or shading action or rotation or earthing-up or use of plastic', 4)], grow, node='2-4')
    add('q9aii-blight', 'Q9(a)(ii) — blight control', '3-3-2', 'potato-blight-control', 'Describe the growing of potatoes under the heading: 4. Potato blight control.',
        [point('Spraying or fungicide or certified seed or rotation or avoid groundkeepers or harvest all tubers or isolate potato dumps or resistant varieties or use dessicant before harvest or earthing up or remove infected tubers', 4)],
        grow, node='2-4')
    add('q9b', 'Q9(b)', '3-3-1', 'why-certified-seed-potatoes', 'State three reasons why farmers would use certified seed potatoes.',
        [menu('True-to-type|free from viruses|free from diseases or named disease|graded to uniform tuber size|higher yields', [4] * 3, 'Any three, 4 marks each (3(4)).')], node='2-3')
    add('q9c', 'Q9(c)', '3-3-3', 'potato-yield-estimate', 'Describe an experiment to estimate the yield of a potato crop prior to harvesting.',
        [menu('Measure out area of field (in m²) or calculate area of potato ridge (in m²)|harvest potatoes inside plot (or from ridge)|remove soil from potatoes (or wash and dry potatoes)|weigh|calculate mass of potatoes per m²|repeat for same size plot|find average|calculate yield of potatoes using: (average) mass of potatoes per m² X 10,000',
              [4] * 5, 'Any five, 4 marks each (5(4)). Some or all marks may be obtained from labelled diagram(s).')], node='2-5|0-1')
    # Question 10 ------------------------------------------------------------
    mitosis = 'The diagram shows a cell dividing by mitosis.'
    figured(add('q10ai', 'Q10(a)(i)', '4-1', 'mitosis-diagram-parts', 'Name the parts labelled A and B.',
                [point('A — Chromatid (or chromosome)', 3), point('B — Spindle (fibre)', 3)], mitosis, node='3-0'), 'q10ai')
    figured(add('q10aii', 'Q10(a)(ii)', '4-1', 'mitosis-stage-shown', 'Name the stage of mitosis shown.', [point('Metaphase', 3)], mitosis, node='3-0'), 'q10aii')
    figured(add('q10aiii', 'Q10(a)(iii)', '4-1', 'stage-before-metaphase', 'Name the stage of mitosis that comes immediately before the stage shown in the diagram.',
                [point('Prophase', 3)], mitosis, node='3-0'), 'q10aiii')
    clones = 'Mitosis is involved in the production of clones.'
    add('q10bi', 'Q10(b)(i)', '4-1', 'clone-meaning', 'What is a clone?',
        [point('A group of genetically identical organisms [allow a single organism genetically identical to original organism]', 3)], clones, node='3-6')
    add('q10bii', 'Q10(b)(ii)', '3-1', 'cloned-crop', 'Name one crop that may be produced by cloning.', [point('e.g. Potatoes or strawberries', 3)], clones, node='3-6|2-0')
    peas = 'The allele for round pea seeds (R) is dominant over the allele for wrinkled pea seeds (r).'
    add('q10c', 'Q10(c)', '4-1', 'pea-cross-1',
        'Copy and complete the following to show a cross between a plant with pure-breeding round seeds and a plant with wrinkled seeds. Genotypes of parents: ( ) × ( ). Gametes produced: ( ) × ( ). Genotype of offspring: ( ). Phenotype of offspring: ____.',
        [point('Genotypes of parents — (RR) × (rr)', 6, '2(3): 3 for each parent.'), point('Gametes — (R) × (r)', 6, '2(3): 3 for each gamete.'),
         point('Genotype of offspring — (Rr)', 3), point('Phenotype of offspring — Round', 3)], peas, node='3-6')
    add('q10d', 'Q10(d)', '4-1', 'pea-cross-2',
        'The plants produced from the above cross were allowed to self-pollinate. Copy and complete the following to show the self-pollination cross. Genotype of parents: ( ) × ( ). Possible gametes: ( ) ( ) × ( ) ( ). Genotypes of offspring: ( ) ( ) ( ). Phenotypes of offspring: ____ ____.',
        [point('Genotype of parents — (Rr) × (Rr)', 6, '2(3): 3 for each parent.'), point('Gametes — (R) (r) × (R) (r)', 8, '4(2): 2 for each gamete.'),
         menu(['(RR)', '(Rr)', '(rr)'], [2, 2, 2], 'Genotypes of offspring, 3(2).'), menu(['Round', 'Wrinkled'], [2, 2], 'Phenotypes of offspring, 2(2).')], peas, node='3-6')
    # Question 11 ------------------------------------------------------------
    add('q11a', 'Q11(a)', '3-3-1', 'spring-versus-winter-barley',
        'Farmers can sow either spring barley or winter barley. Copy and complete the following table: Month of sowing; Month of harvesting; Yield (tonnes/ hectare) — for spring barley and for winter barley.',
        [split('Spring barley, month of sowing — Feb. – May', SHARED.format('2(4) + 4(2)') + ' Six table cells.'), split('Winter barley, month of sowing — Sept. – Nov.'),
         split('Spring barley, month of harvest — Aug. – Oct.'), split('Winter barley, month of harvest — July – Aug.'),
         split('Spring barley, yield (tonnes/ ha.) — 5 – 7'), split('Winter barley, yield (tonnes/ ha.) — 6 – 9')],
        marks=16, tariff={'kind': 'orderedSplit', 'notation': '2(4) + 4(2)'}, node='2-3|2-5')
    add('q11b', 'Q11(b)', '3-3-2', 'feeding-versus-malting-barley', 'State two differences between the cultivation and harvesting of feeding barley and malting barley.',
        [menu('More care (or avoid damage to grain) at harvesting for malting barley|less nitrogen in fertiliser for malting barley|different varieties|winter barley not suitable for malting|malting barley requires well drained soil (or more suited to sandy loam soils) (or different soil types)',
              [2, 2], 'Any two, 2 marks each (2(2)).')], node='2-4')
    add('q11c', 'Q11(c)', '3-3-3', 'barley-harvest-ready', 'Describe two features of barley that show it is ready for harvesting.',
        [menu('Grain (or seed) becomes hard|moisture content drops to 16 – 18% (or grain becomes dry)|ear (or seed-head) and-or straw turns a golden (or yellow or bleached) colour|seed-head bends over (and lies parallel to stem)|flag leaf withers|grain starts to fall off stem',
              [2, 2], 'Any two, 2 marks each (2(2)).')], node='2-5')
    pests = 'The larvae of the click beetle and the crane fly cause damage to cereal crops.'
    add('q11di', 'Q11(d)(i)', '3-3-2', 'click-beetle-larva', 'Name the larva of the click beetle.', [point('Wireworm', 4)], pests, node='2-4')
    add('q11dii', 'Q11(d)(ii)', '3-3-2', 'crane-fly-larva', 'Name the larva of the crane fly.', [point('Leatherjacket', 4)], pests, node='2-4')
    add('q11diii', 'Q11(d)(iii)', '3-3-2', 'cereal-disease-and-control', 'Name one disease of cereal crops and state how it is prevented or controlled.',
        [point('Disease — Leaf smut or rust or (powdery) mildew or Rhyncosporium or barley yellow dwarf virus or leaf blotch (or Septoria) or leaf stripe or Fusarium or take-all or eyespot', 4),
         point('Prevention — Spraying or fungicide or crop rotation or certified seeds or resistant varieties or aphid control', 4)], pests, node='2-4')
    add('q11e', 'Q11(e)', '3-1', 'barley-germination-percentage', 'Describe how to find the percentage (%) germination of a sample of barley seeds.',
        [menu('100 seeds (or count seeds)|soak seeds (for 24 hours)|seed tray (or suitable container)|cotton wool (or suitable growing medium)|warm place or regular watering|leave for suitable time|count number of sprouted seeds|calculate % germination using: number of seeds germinated X 100|repeat|average',
              [4] * 5, 'Any five, 4 marks each (5(4)). The % germination is the number of seeds germinated over the original number of seeds, × 100. Some or all marks may be obtained from labelled diagram(s).')], node='2-0|0-1')
    # Question 12 ------------------------------------------------------------
    add('q12ai', 'Q12(a)(i)', '3-3-2', 'paddock-grazing-diagram', 'Draw a labelled diagram of a paddock grazing system.',
        [point('Means of access to paddocks (e.g. roadway or pathway) and at least 10 paddocks', None, 'Drawing: 6, 3, 0.', kind='criterion'),
         point('(Permanent) roadway/ water (supply)/ fencing/ gates/ paddocks showing re-growth or recovery/ indication of direction of movement of livestock/ number of paddocks labelled (e.g. 20 -25 paddocks)', None,
               'Labels: any three, 2 marks each (3(2)).')],
        marks=12, tariff={'kind': 'questionTotal', 'notation': 'D 6, 3, 0 + L 3(2)'}, node='2-6')
    add('q12aii', 'Q12(a)(ii)', '3-3-2', 'paddock-grazing-advantage', 'State one advantage of a paddock grazing system.',
        [point('Fresh grass each day or controlled grazing or 21-day rotation or time for grass to recover or reduced incidence of parasitic worms or paddocks can be fertilised when animals move or more efficient use of grass (or less wastage or less trampling of grass) or less time spent walking or (highly) palatable grass always available or grass more digestible or maximum production from animals or some paddocks can be closed off for silage (or hay) or low labour input', 3)],
        node='2-6')
    add('q12aiii', 'Q12(a)(iii)', '3-3-2', 'paddock-grazing-disadvantage', 'State one disadvantage of a paddock grazing system.',
        [point('Expensive to set up or each paddock must have a permanent water supply or fencing for each paddock or can be difficult to cut silage (or hay) if paddocks are small or poaching damage is possible (in certain weather conditions)', 3)],
        node='2-6')
    steps = [('Use good quality grass variety (or named grass variety e.g. PRG)', 'Hay of better quality or more digestible or higher yield'),
             ('Cut grass at correct growth stage', 'Hay of better quality or more digestible or easier to dry'),
             ('Control weeds', 'Hay of better quality or prevents poisoning (of livestock)'),
             ('Cut or mow grass in dry weather', 'Easier drying (or allows grass to dry) or lowers risk of weather damage'),
             ('Allow grass to wilt or dry', 'Lowers moisture content'), ('Ted (or turn or shake) grass', 'Faster drying or lets air through grass'),
             ('Rake (or gather) into rows', 'Easier to bale'), ('Bale hay', 'Easier to handle or to transport or to store'),
             ('Store hay in (leak-proof) shed or under cover', 'Keeps hay dry or prevents rotting')]
    add('q12b', 'Q12(b)', '3-3-3', 'making-good-hay', 'Describe three steps involved in making good quality hay, and give the reason for each step.',
        [menu([s for s, _ in steps], [3] * 3, 'Steps: any three, 3 marks each (3(3)).'),
         menu([f'{s}: {r}' for s, r in steps], [3] * 3, 'The reason for each of your three steps, 3 marks each (3(3)).')], node='2-6|2-5')
    add('q12c', 'Q12(c)', '3-3-3', 'good-silage', 'State how a farmer can ensure the production of good quality silage.',
        [menu('Use good quality grass variety or named grass (e.g. PRG)|close off field 6 – 8 weeks before cutting (or close off early)|apply fertiliser|control weeds|cut at leafy stage|cut grass in sunny weather (or cut at midday)|allow grass to wilt|avoid contamination|fill pit quickly|roll grass (or exclude air from grass in pit)|use additive if necessary|cover pit with black plastic (or bale silage)|seal tightly (or weigh down plastic)|tighten plastic again after 2 – 3 weeks',
              [3] * 3, 'Any three, 3 marks each (3(3)).')], node='2-6')
    tests = [('Leaf-to-stem ratio', 'Too much stem indicates poor quality (or more leaf indicates high quality)'),
             ('Squeeze silage (or dry matter or DM test)', 'A large amount of water produced indicates low quality (or little water produced indicates high quality)'),
             ('pH of silage', 'pH > 5 indicates poor quality (or pH < 5 indicates high quality)'),
             ('Colour of silage', 'Dark green (or brown) colour indicates poor quality (or yellow-green colour indicates high quality)'),
             ('Smell of silage', 'Putrid smell indicates poor quality (or sharp (acidic) smell indicates high quality)'),
             ('Taste of silage', 'No sharp (or acidic taste) indicates poor quality (or sharp acidic taste indicates high quality)'),
             ('Feel of silage', 'A slimy feel indicates poor quality (or a soft but firm texture indicates good quality)')]
    add('q12d', 'Q12(d)', '3-3-3', 'silage-quality-tests', 'List three simple tests a farmer can carry out to determine the quality of silage, and state the purpose of each test.',
        [menu([t for t, _ in tests], [3] * 3, 'Tests: any three, 3 marks each (3(3)).'),
         menu([f'{t}: {p}' for t, p in tests], [2] * 3, 'The purpose of each of your three tests, 2 marks each (3(2)).')], node='2-6|0-1')
    # Question 13 ------------------------------------------------------------
    two = 'Answer any two of the parts (a), (b), (c), (d).'
    add('q13ai', 'Q13(a)(i)', '4-2', 'lowland-sheep-breeds', 'Name two lowland sheep breeds.',
        [menu('Suffolk|Texel|Galway|Hampshire Down|Border Leicester|Charollais|Beltex|Blueface Leicester|Belclare Improver|Oxford Down', [3, 3], 'Any two, 3 marks each (2(3)).')], two, node='3-1')
    terms = 'Explain each of the following terms and state why each procedure is carried out on sheep farms.'
    for slug, label, topic, explain, reason in [
            ('flushing', 'Flushing', '4-3-2', 'Moving ewes from a low plane of nutrition to a high plane of nutrition (or to better grazing) before mating',
             'Increases fertility or increases number of eggs released (from ovary) or more twins or more regular heat periods or safer implantation or fewer returns to service or higher conception rates or increase in BCS'),
            ('scanning', 'Scanning', '4-3-2', 'Using ultrasound (or scanner) to find if ewe is in lamb',
             'To determine if ewe is pregnant or to determine how many lambs the ewe is carrying or to determine how much meal to feed pregnant ewe or to see if ewe is barren'),
            ('steaming-up', 'Steaming up', '4-3-2', 'Practice of feeding (increasing amounts of) concentrates in late pregnancy',
             'To prevent twin-lamb disease or to get stronger lamb(s) or reduces mortality or to increase milk production in ewe or to help ewe produce high-quality colostrum'),
            ('vaccination', 'Vaccination', '4-3-3', 'Injection used to prevent diseases (or named disease) or to stimulate antibody production or for immunity',
             'To reduce mortality or (if none of the following has already earned marks for explanation) to prevent diseases (or named disease) or to boost antibody production or for immunity'),
            ('creep-feeding', 'Creep feeding', '4-3-2', 'Using a creep feeder to allow lambs, but not ewes, access to concentrates or use of creep gates to allow lambs, but not ewes, access to grazing',
             'Improved growth rates in lambs or earlier weaning of lambs or lambs have choice of best grass or better parasite control'),
            ('shearing', 'Shearing', '4-3-3', 'Clipping off wool (or removal of wool)', 'To prevent animal over- heating or to prevent flystrike or to sell the wool or prevents sheep “going on their back”')]:
        add(f'q13aii-{slug}', f'Q13(a)(ii) — {slug.replace("-", " ")}', topic, f'sheep-term-{slug}',
            f'Explain the following term and state why the procedure is carried out on sheep farms: {label}.',
            [point(f'Explanation — {explain}', 2, '2(2): explanation 2 + reason 2.'), point(f'Reason for procedure — {reason}', 2)], terms, node='3-4|3-5')
    misprint = 'The paper prints this part\'s letter as a second "(a)"; the marking scheme marks it as Question 13(b).'
    photo = 'The diagram shows an investigation into photosynthesis.'
    figured(add('q13bi', 'Q13(b)(i)', '3-1', 'photosynthesis-gas', 'Name the gas collected in the test tube.',
                [point('Oxygen (or O2)[allow O]', 3)], photo, node='2-0', note=misprint), 'q13bi')
    figured(add('q13bii', 'Q13(b)(ii)', '3-1', 'photosynthesis-factors', 'Name two factors necessary for photosynthesis.',
        [menu('Carbon dioxide (or CO2)|water|chlorophyll|light', [3, 3], 'Any two, 3 marks each (2(3)).')], photo, node='2-0'), 'q13bii')
    figured(add('q13biii', 'Q13(b)(iii)', '3-1', 'photosynthesis-and-climate', 'How does photosynthesis help to reduce the problem of climate change?',
        [point('CO2 is absorbed during photosynthesis', 3)], photo, node='2-0|1-6'), 'q13biii')
    figured(add('q13biv', 'Q13(b)(iv)', '3-1', 'leaf-starch-test', 'Starch is stored in leaves as a result of photosynthesis. Describe how to test a leaf for the presence of starch.',
        [menu('Boil leaf (for 1 minute)|place in hot alcohol (for 10 minutes)|removes chlorophyll (or green colour)|rinse leaf in water|place on white tile|cover leaf with iodine|blue-black (or black) indicates presence of starch',
              [3] * 6, 'Any six, 3 marks each (6(3)). Some or all marks may be obtained from labelled diagram(s).')], photo, node='2-0|0-1'), 'q13biv')
    calves = 'Describe the management of dairy calves under the following headings.'
    for key, ref, concept, heading, points, topic in [
            ('q13ci', 'Q13(c)(i)', 'dairy-calf-care-at-birth', 'Care at birth', 'Have experienced person at hand|close supervision|remove mucus from nasal area (or ensure calf breathing)|dry calf (or ensure cow licks calf)|iodine on navel|clean bedding|colostrum (or ensure cow suckles calf)|keep calf warm|tag calf|vaccinate', '4-3-3'),
            ('q13cii', 'Q13(c)(ii)', 'dairy-calf-housing', 'Housing', 'Straw (or dry) bedding|good ventilation|draught free|walls and floor disinfected (or good hygiene)|feeding area available|fresh water|adequate space|adequate lighting', '4-3-2'),
            ('q13ciii', 'Q13(c)(iii)', 'dairy-calf-disease-prevention', 'Disease prevention', 'Isolate cow prior to calving (or cow in calving box)|house is disinfected (or maintain good hygiene)|navel is disinfected|calves are vaccinated|colostrum|equipment is disinfected|disposable gloves if assisting calving process|call vet if necessary|correct feeding techniques|disinfect boots', '4-3-3'),
            ('q13civ', 'Q13(c)(iv)', 'dairy-calf-hay', 'Introducing hay into their diet', 'Introduce hay in first 7 – 10 days|hay contains fibre|scratch factor|helps rumen to develop|introduces microbes into rumen|earlier weaning|more suitable roughage (than silage)for young calves', '4-3-2'),
            ('q13cv', 'Q13(c)(v)', 'dairy-calf-milk-replacer', 'Use of milk replacer', 'Calves weaned off cow’s milk|milk replacer cheaper than cow’s milk|powder is mixed with either cold or warm water|fed in buckets or ad lib|feed at correct temperature|mix powder thoroughly', '4-3-2')]:
        add(key, ref, topic, concept, 'Describe the management of dairy calves under the heading: ' + heading + '.',
            [menu(points, [3, 3], 'Any two, 3 marks each (2(3)).')], calves, node='3-5' if topic == '4-3-3' else '3-4')
    add('q13di', 'Q13(d)(i)', '4-1', 'molar-tooth-diagram', 'Draw a labelled diagram of a molar tooth.',
        [point('Diagram to show: Tooth with broad top surface and two roots', None, 'Drawing: 4, 2, 0.', kind='criterion'),
         point('Enamel/ dentine/ pulp (cavity)/ crown/ root/ jaw bone/ cement/ blood vessel/ nerve', None, 'Labels: any three, 2 marks each (3(2)).')],
        two, marks=10, tariff={'kind': 'questionTotal', 'notation': 'D 4, 2, 0 + L 3(2)'})
    add('q13dii', 'Q13(d)(ii)', '4-1', 'incisor-and-molar-functions', 'State the function of the incisors and of the molars in a farm animal.',
        [point('Function of incisor — To cut (or bite or slice) food', 3), point('Function of molar — To chew (or grind or crush) food', 3)], two)
    add('q13diii', 'Q13(d)(iii)', '4-1', 'other-tooth-types', 'Name two other types of tooth found in farm animals.',
        [point('1. Canines', 3), point('2. Pre-molars', 3)], two)
    formula = [('pig', 'Pig', [('Incisors', '3 3'), ('Canines', '1 1'), ('Pre-molars', '4 4'), ('Molars', '3 3')], '3 1 4 3 3 1 4 3'),
               ('sheep', 'Sheep', [('Incisors', '0 3'), ('Canines', '0 1'), ('Pre-molars', '3 3'), ('Molars', '3 3')], '0 0 3 3 3 1 3 3'),
               ('sheep-alternative', 'Sheep (the scheme\'s alternative)', [('Incisors', '0 4'), ('Canines', '0 0'), ('Pre-molars', '3 3'), ('Molars', '3 3')], '0 0 3 3 4 0 3 3')]
    rows, variants = routes([(slug, label, [point(f'{tooth} (upper, lower) — {value}', 2,
                                                  f'{label}: 4(2), one 2-mark unit per tooth type. The scheme\'s table reads {table} (incisor, canine, pre-molar, molar; upper jaw then lower jaw).' if i == 0 else None)
                                            for i, (tooth, value) in enumerate(teeth)]) for slug, label, teeth, table in formula])
    add('q13div', 'Q13(d)(iv)', '4-1', 'dental-formula', 'Give the dental formula for a pig or a sheep.', rows, two,
        selection=closed(1, ['Pig', 'Sheep']), extra={'answerVariants': variants})
    assert len(p.tasks) == 60, len(p.tasks)
    return p


def reviewed_tasks():
    p = build()
    return p.cards, p.tasks


def paper_review():
    return build().review('60 base tasks, one card each. Every Section One question is one task stating its scale (orderedSplit), because the scale runs across all its parts; Question 5 is one first-correct pool. '
                          'Section Two parts are priced on their own; the Q9(a)(ii) potato headings and the six Q13(a)(ii) sheep terms carry their own marks and are separate tasks. '
                          'Q13(d)(iv) carries the pig and sheep formulas as answer routes. The paper prints Q13(b) as a second "(a)".')
