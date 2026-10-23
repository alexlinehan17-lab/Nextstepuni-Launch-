"""2019 Ordinary: every task authored from the SEC paper and marking scheme (no cards existed).

All 16 paper pages and 16 scheme pages were inspected and the independent census transcribed
before authoring: 54 base tasks, one card each. Where the scheme prices several parts with one
shared scale (Q1, Q5, Q7, Q9(c), Q10(a), Q13(a), (b), (d)) the scale's span is the task and the
card states the scale (orderedSplit). Hill or lowland sheep (Q8(c)), sandy or clay soil (Q11(b)),
the two milk-hygiene methods (Q12(c)) and the three transpiration demonstrations (Q13(d)(iv))
are answer routes on one card. Answers are the scheme's words.
"""
from agricultural_science_legacy import Paper, P, point, menu, closed, routes

FILE = 'LC024GLP000EV.pdf'
HASHES = {'exampapers': 'd5978d8b8f4ce76f7cafcd14c6be9f7072aef3e0335f12ea1ec1e9d76429b3d8',
          'markingschemes': '80e7534cdefcbe5d0d7921ed0ffb5041c5628cce01e910b4c75ab55ba8ef9ca0'}
SELECTIONS = {
    'c8504d75225fbfc5': ('exam-selection', 'Section One: six of seven independent 20-mark questions; every question is retained.'),
    'f2ea94f03d317398': ('exam-selection', 'Section Two: three of six independent 60-mark questions; every question is retained.'),
    '82e8a73b4285d153': ('open', 'Q8(a)(ii): the importance of any one of the candidate’s own housing features; the scheme tabulates an importance for each feature (a marking menu).'),
    '72b70b60ca49f954': ('closed', 'Q8(c): hill (mountain) or lowland sheep production, kept as answer routes on one card.'),
    'c349dfaa48b0ec42': ('open', 'Q9(a)(iii): the reason for any one of the candidate’s own named grass species; the scheme gives reasons per species (a marking menu).'),
    '526c9f54802d9199': ('open', 'Q9(b)(ii): the importance of any two of the candidate’s own silage steps; the scheme tabulates an importance for each step.'),
    'ae0afb674c064a2a': ('open', 'Q12(b)(iii): any three hygiene measures from the scheme pool; a marking menu.'),
    '1617d9049f8f6d3c': ('independent-task-selection', 'Q13: two of four independently priced 30-mark parts; all four are retained.'),
}
SUPPLEMENTARY = [
    (11, 'Describe a sandy soil', 'closed', 'Q11(b): sandy or clay soil, kept as answer routes on one card.'),
    (12, 'Describe an experiment to compare the hygiene quality of two milk samples', 'closed', 'Q12(c): the scheme answers by the resazurin test OR by agar plates, kept as answer routes on one card.'),
    (13, 'Describe an experiment to demonstrate transpiration in a plant', 'closed', 'Q13(d)(iv): the scheme gives a plastic-bag, a potometer and a coloured-dye method, kept as answer routes on the Q13(d) card.'),
]
ATLAS = {
    'Q1': 'soil-science|scientific-practices-experiments-investigations', 'Q2': 'crop-production|animal-production|grassland',
    'Q3': 'animal-production|scientific-practices-experiments-investigations|soil-science|plant-physiology|animal-physiology',
    'Q4': 'animal-production', 'Q5': 'crop-production',
    'Q6(a)': 'crop-production|animal-diseases', 'Q6(b)': 'animal-production', 'Q6(c)': 'animal-diseases', 'Q6(d)': 'fertilisers-pollution-the-environment|health-safety',
    'Q6(e)': 'fertilisers-pollution-the-environment', 'Q7': 'grassland|plant-physiology',
    'Q8': 'animal-production', 'Q9': 'grassland', 'Q9(c)': 'crop-production|grassland',
    'Q10': 'genetics', 'Q10(d)': 'genetics|animal-production', 'Q11': 'soil-science',
    'Q12(a)': 'animal-production', 'Q12(b)': 'animal-diseases|animal-production', 'Q12(c)': 'scientific-practices-experiments-investigations|animal-production',
    'Q13(a)': 'crop-production', 'Q13(b)': 'animal-physiology', 'Q13(c)': 'crop-production|fertilisers-pollution-the-environment',
    'Q13(d)': 'plant-physiology|scientific-practices-experiments-investigations',
}
REGIONS = {
    # Drafted by regions.py. Hand-trimmed where a last part would run onto the next page's
    # repeated question header or the blank back pages (Q9(b)(iv), Q13(c)(iv), Q13(d)).
'Q1': (P((2, 0.276, 0.841)), P((5, 0.126, 0.426))),
    'Q2': (P((3, 0.043, 0.913)), P((5, 0.426, 0.672))),
    'Q3': (P((4, 0.043, 0.496)), P((5, 0.672, 0.882))),
    'Q4': (P((4, 0.496, 0.918)), P((6, 0.094, 0.257))),
    'Q5': (P((5, 0.043, 0.777)), P((6, 0.257, 0.529))),
    'Q6(a)': (P((6, 0.043, 0.219)), P((6, 0.529, 0.609))),
    'Q6(b)': (P((6, 0.043, 0.109), (6, 0.219, 0.327)), P((6, 0.529, 0.562), (6, 0.609, 0.689))),
    'Q6(c)': (P((6, 0.043, 0.109), (6, 0.327, 0.436)), P((6, 0.529, 0.562), (6, 0.689, 0.754))),
    'Q6(d)': (P((6, 0.043, 0.109), (6, 0.436, 0.546)), P((6, 0.529, 0.562), (6, 0.754, 0.817))),
    'Q6(e)': (P((6, 0.043, 0.109), (6, 0.546, 0.645)), P((6, 0.529, 0.562), (6, 0.817, 0.896))),
    'Q7': (P((7, 0.043, 0.758)), P((7, 0.094, 0.434))),
    'Q8(a)(i)': (P((8, 0.238, 0.304)), P((8, 0.127, 0.229))),
    'Q8(a)(ii)': (P((8, 0.238, 0.272), (8, 0.304, 0.336)), P((8, 0.127, 0.159), (8, 0.229, 0.442))),
    'Q8(a)(iii)': (P((8, 0.238, 0.272), (8, 0.336, 0.515)), P((8, 0.127, 0.159), (8, 0.442, 0.519))),
    'Q8(b)(i)': (P((8, 0.238, 0.272), (8, 0.515, 0.546)), P((8, 0.127, 0.159), (8, 0.519, 0.542))),
    'Q8(b)(ii)': (P((8, 0.238, 0.272), (8, 0.546, 0.578)), P((8, 0.127, 0.159), (8, 0.542, 0.560))),
    'Q8(b)(iii)': (P((8, 0.238, 0.272), (8, 0.578, 0.706)), P((8, 0.127, 0.159), (8, 0.560, 0.676))),
    'Q8(c)': (P((8, 0.238, 0.272), (8, 0.706, 0.907)), P((8, 0.127, 0.159), (8, 0.676, 0.884))),
    'Q9(a)(i)': (P((9, 0.043, 0.141)), P((9, 0.093, 0.223))),
    'Q9(a)(ii)': (P((9, 0.043, 0.109), (9, 0.141, 0.173)), P((9, 0.093, 0.119), (9, 0.223, 0.281))),
    'Q9(a)(iii)': (P((9, 0.043, 0.109), (9, 0.173, 0.205)), P((9, 0.093, 0.119), (9, 0.281, 0.437))),
    'Q9(a)(iv)': (P((9, 0.043, 0.109), (9, 0.205, 0.267)), P((9, 0.093, 0.119), (9, 0.437, 0.509))),
    'Q9(b)(i)': (P((9, 0.043, 0.077), (9, 0.267, 0.331)), P((9, 0.093, 0.119), (9, 0.509, 0.610))),
    'Q9(b)(ii)': (P((9, 0.043, 0.077), (9, 0.267, 0.299), (9, 0.331, 0.362)), P((9, 0.093, 0.119), (9, 0.610, 0.857))),
    'Q9(b)(iii)': (P((9, 0.043, 0.077), (9, 0.267, 0.299), (9, 0.362, 0.394)), P((9, 0.093, 0.119), (9, 0.857, 0.879))),
    'Q9(b)(iv)': (P((9, 0.043, 0.077), (9, 0.267, 0.299), (9, 0.394, 0.458)), P((9, 0.093, 0.119), (9, 0.879, 0.901))),
    'Q9(c)': (P((9, 0.043, 0.077), (9, 0.458, 0.767)), P((10, 0.081, 0.341))),  # page 10's own Q9 header carries the 4(3)
    'Q10(a)': (P((10, 0.043, 0.220)), P((10, 0.382, 0.537))),
    'Q10(b)': (P((10, 0.043, 0.077), (10, 0.220, 0.528)), P((10, 0.382, 0.412), (10, 0.537, 0.606))),
    'Q10(c)': (P((10, 0.043, 0.077), (10, 0.528, 0.754)), P((10, 0.382, 0.412), (10, 0.606, 0.694))),
    'Q10(d)(i)': (P((10, 0.043, 0.077), (10, 0.754, 0.812)), P((10, 0.382, 0.412), (10, 0.694, 0.814))),
    'Q10(d)(ii)': (P((10, 0.043, 0.077), (10, 0.754, 0.780), (10, 0.812, 0.834)), P((10, 0.382, 0.412), (10, 0.814, 0.892))),
    'Q11(a)(i)': (P((11, 0.043, 0.236)), P((11, 0.099, 0.197))),
    'Q11(a)(ii)': (P((11, 0.043, 0.077), (11, 0.236, 0.268)), P((11, 0.099, 0.127), (11, 0.197, 0.232))),
    'Q11(a)(iii)': (P((11, 0.043, 0.077), (11, 0.268, 0.317)), P((11, 0.099, 0.127), (11, 0.232, 0.375))),
    'Q11(b)': (P((11, 0.043, 0.077), (11, 0.317, 0.493)), P((11, 0.099, 0.127), (11, 0.375, 0.493))),
    'Q11(c)(i)': (P((11, 0.043, 0.077), (11, 0.493, 0.525)), P((11, 0.099, 0.127), (11, 0.493, 0.581))),
    'Q11(c)(ii)': (P((11, 0.043, 0.077), (11, 0.525, 0.557)), P((11, 0.099, 0.127), (11, 0.581, 0.668))),
    'Q11(c)(iii)': (P((11, 0.043, 0.077), (11, 0.557, 0.599)), P((11, 0.099, 0.127), (11, 0.668, 0.764))),
    'Q12(a)(i)': (P((12, 0.043, 0.162)), P((12, 0.099, 0.218))),
    'Q12(a)(ii)': (P((12, 0.043, 0.129), (12, 0.162, 0.193)), P((12, 0.099, 0.149), (12, 0.218, 0.253))),
    'Q12(a)(iii)': (P((12, 0.043, 0.129), (12, 0.193, 0.225)), P((12, 0.099, 0.149), (12, 0.253, 0.305))),
    'Q12(a)(iv)': (P((12, 0.043, 0.129), (12, 0.225, 0.257)), P((12, 0.099, 0.149), (12, 0.305, 0.367))),
    'Q12(b)(i)': (P((12, 0.043, 0.077), (12, 0.257, 0.628)), P((12, 0.099, 0.127), (12, 0.367, 0.460))),
    'Q12(b)(ii)': (P((12, 0.043, 0.077), (12, 0.257, 0.564), (12, 0.628, 0.680)), P((12, 0.099, 0.127), (12, 0.460, 0.564))),
    'Q12(b)(iii)': (P((12, 0.043, 0.077), (12, 0.257, 0.564), (12, 0.680, 0.729)), P((12, 0.099, 0.127), (12, 0.564, 0.637))),
    'Q12(c)': (P((12, 0.043, 0.077), (12, 0.729, 0.751)), P((12, 0.099, 0.127), (12, 0.637, 0.895))),
    'Q13(a)': (P((13, 0.043, 0.294)), P((13, 0.099, 0.395))),
    'Q13(b)': (P((13, 0.043, 0.109), (13, 0.294, 0.650)), P((13, 0.099, 0.127), (13, 0.395, 0.618))),
    'Q13(c)(i)': (P((13, 0.043, 0.109), (13, 0.650, 0.682)), P((13, 0.099, 0.127), (13, 0.618, 0.726))),
    'Q13(c)(ii)': (P((13, 0.043, 0.109), (13, 0.682, 0.714)), P((13, 0.099, 0.127), (13, 0.726, 0.760))),
    'Q13(c)(iii)': (P((13, 0.043, 0.109), (13, 0.714, 0.743)), P((13, 0.099, 0.127), (13, 0.760, 0.828), (13, 0.828, 0.848, 0.85, 1))),  # its 5 sits on the (iv) heading line
    'Q13(c)(iv)': (P((13, 0.043, 0.109), (13, 0.743, 0.781)), P((13, 0.099, 0.127), (13, 0.828, 0.848, 0, 0.85), (13, 0.848, 0.886))),
    'Q13(d)': (P((13, 0.043, 0.109), (13, 0.781, 0.901)), P((13, 0.099, 0.127), (14, 0.102, 0.623))),
}
SHARED = 'Shared scale {}: the first correct answers earn the higher award, whichever part they answer, so no part carries a mark of its own.'
FIGURES = {
    'q1': ('agsci-2019-ol-paper-wormery', None),
    'q2': ('agsci-2019-ol-paper-farm-machinery', [('A', 'Silage wagon (the completed example)', False), ('B', '(Rotary) tedder or hay bob', True),
                                                  ('C', 'Creep feeder', True), ('D', 'Shear grab or silage grab', True), ('E', '(Grain) silo', True), ('F', 'Combine (harvester)', True)]),
    'q5': ('agsci-2019-ol-paper-cereals', [('A', 'Barley', True), ('B', 'Oats', True), ('C', 'Wheat', True)]),
    'q7': ('agsci-2019-ol-paper-clover-nodules', None),
    'q8aiii': ('agsci-2019-ol-paper-farrowing-crate', None),
    'q9c': ('agsci-2019-ol-paper-stubble-turnips', None),
    'q12bi': ('agsci-2019-ol-paper-milking-parlour', None),
    'q13b': ('agsci-2019-ol-paper-sheep-heart', [('A', 'Pulmonary artery', True), ('B', 'Vena cava', True), ('C', 'Left atrium', True), ('D', 'Left ventricle', True)]),
}


def split(text, note=None, route=None):
    """A row of an orderedSplit card: the scheme prices the scale, not the row."""
    row = point(text, None, note)
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
    p = Paper(2019, 'ordinary', FILE, HASHES, REGIONS, ATLAS, 16, 16, SELECTIONS, SUPPLEMENTARY,
              section=lambda ref: 'A' if int(ref.split('(')[0][1:]) <= 7 else 'B')
    add = p.add
    # Question 1: one shared scale over (a) and (b) ---------------------------
    figured(add('q1', 'Q1', '2-2-3', 'earthworms-and-the-wormery',
                '(a) (i) Name the phylum to which earthworms belong. (ii) State two beneficial effects of earthworms in the soil. '
                '(b) The photograph shows a wormery, which is used to show the activity of earthworms. (i) Describe four steps taken when setting up the wormery to investigate earthworm activity. '
                '(ii) Name one sign of earthworm activity that would be observed in the wormery at the end of the investigation.',
                [split('(a)(i) Phylum — Annelida', SHARED.format('2(4) + 6(2)') + ' Eight answers: the phylum, two effects, four steps and one sign.'),
                 split('(a)(ii) Beneficial effects of earthworms — Improve drainage/ improve aeration/ break down organic matter or create humus/ break down soil/ mix soil layers/ improve soil structure/ (waste products) increase soil fertility', 'Any two.'),
                 split('(b)(i) Setting up a wormery — Layer of soil/ layer of sand/ layer of chalk/ leaves or organic matter on top/ add worms/ keep moist/ keep in darkness/ cool place/ leave for at least a week', 'Any four.'),
                 split('(b)(ii) Sign of earthworm activity — Mixed layers or tunnels (or holes) through layers or worm casts or leaves not present on top')],
                marks=20, tariff={'kind': 'orderedSplit', 'notation': '2(4) + 6(2)'}, node='1-4|0-1'), 'q1')
    # Question 2 -------------------------------------------------------------
    machines = [('B', '(Rotary) tedder or hay bob', 'Shaking out grass (to allow it to dry) or making rows of hay or gathers hay'),
                ('C', 'Creep feeder', 'Allows lambs access to feed (but excludes ewes) or to feed meals to lambs'),
                ('D', 'Shear grab or silage grab', 'Transports silage (from pit to feeders)'),
                ('E', '(Grain) silo', 'Storing grain (or animal feed)'), ('F', 'Combine (harvester)', 'Harvesting cereals (or named cereal)')]
    figured(add('q2', 'Q2', '2-3', 'farm-machinery-names-functions',
                'Name and state the function of each of the items of farm equipment and machinery shown below (B to F). Item A has been completed for you: Silage Wagon — Transports grass from field to cattle or to pit.',
                [menu([name, use], [2, 2], f'{letter}: its name and its function, 2(2).') for letter, name, use in machines],
                tariff={'kind': 'fixed', 'notation': '5 × 2(2)'}, node='1-5|2-5|3-4'), 'q2')
    # Question 3 -------------------------------------------------------------
    statements = [('a', 'A gilt is a young female pig', 'T'), ('b', 'Benedict’s or Fehling’s solution is used to test a food for starch', 'F'),
                  ('c', 'Ground limestone is used to raise soil pH', 'T'), ('d', 'Plants make carbon dioxide during photosynthesis', 'F'),
                  ('e', 'Urea is a fertiliser which has a high content of nitrogen', 'T'), ('f', 'Pigs have a ruminant stomach', 'F'),
                  ('g', 'Crop rotation helps to reduce the incidence of crop pests', 'T'), ('h', 'Chlorophyll is a pigment in grass', 'T'),
                  ('i', 'Dairy cows are usually dried off for five months each year', 'F'), ('j', 'Pollen is produced by the carpels in a flower', 'F')]
    add('q3', 'Q3', '4-1', 'true-or-false-farm-science',
        'Indicate whether each of the following statements is true (T) or false (F) by placing a circle around the correct answer in each case. Example: Liver fluke is a parasite of sheep and cattle — T. '
        '(a) A gilt is a young female pig. (b) Benedict’s or Fehling’s solution is used to test a food for starch. (c) Ground limestone is used to raise soil pH. '
        '(d) Plants make carbon dioxide (CO2) during photosynthesis. (e) Urea is a fertiliser which has a high content of nitrogen. (f) Pigs have a rumen in their digestive system. '
        '(g) Crop rotation helps control crop pests. (h) Chlorophyll is a pigment found in grass. (i) Dairy cows are usually dried off for five months each year. (j) Pollen is produced by the carpels in a flower.',
        [menu([f'({k}) {s}: {a}' for k, s, a in statements], [2] * 10,
              'All ten statements, 2 marks each (10(2)). T = true, F = false; the scheme words each statement as shown.')],
        tariff={'kind': 'fixed', 'notation': '10(2)'}, node='3-0|0-1|1-2|2-0|1-6|2-4')
    # Question 4 -------------------------------------------------------------
    add('q4', 'Q4', '4-2', 'breed-descriptions',
        'The following is a list of breeds of farm animals: Jersey, Suffolk, Holstein-Friesian, Landrace, Wicklow Cheviot, Belgian Blue. Match each description with a breed name. The first one has been completed for you: Wicklow Cheviot — Mountain/ hill sheep breed. '
        'Cow with a high butterfat content in milk; Beef breed of cattle; Pig breed with lean carcass; Sheep breed with good conformation; Dairy breed with high milk yield.',
        [point('Cow with a high butterfat content in milk — Jersey', 4, '5(4): 4 marks for each description.'), point('Beef breed of cattle — Belgian Blue', 4),
         point('Pig breed with a lean carcass — Landrace', 4), point('Sheep breed with good conformation — Suffolk', 4),
         point('Dairy breed with a high milk yield — Holstein-Friesian', 4)], node='3-1')
    # Question 5: one shared scale over (a)-(c) -------------------------------
    figured(add('q5', 'Q5', '3-3-1', 'cereals-harvest-and-certified-seed',
                '(a) Identify each of the cereals shown in the photographs (A, B, C). (b) State two ways you would know when cereal A is ready for harvesting. '
                '(c) Certified seeds are used when sowing a cereal crop. State three features of certified seeds.',
                [split('(a) Cereal A — Barley', SHARED.format('2(4) + 6(2)') + ' Eight answers: three cereals, two signs and three features.'),
                 split('(a) Cereal B — Oats'), split('(a) Cereal C — Wheat'),
                 split('(b) When cereal A ready for harvest — Seed-head (or ear) lies parallel to stem/ grain hard/ grain dry/ flag leaf withers/ grain falling off seed-head/ crop is bleached in appearance', 'Any two.'),
                 split('(c) Features of certified seeds — Minimum 85% germination rate/ minimum 98% purity/ free from wild oats/ seed is treated (with fungicide and pesticide) or is disease free/ true to type', 'Any three.')],
                marks=20, tariff={'kind': 'orderedSplit', 'notation': '2(4) + 6(2)'}, node='2-1|2-3|2-5'), 'q5')
    # Question 6 -------------------------------------------------------------
    practice = 'State one reason for each of the following farming practices.'
    for key, ref, topic, concept, item, answer, node in [
            ('q6a', 'Q6(a)', '3-3-2', 'why-spray-potatoes-fungicide', 'Spraying a potato crop with fungicide.', 'To prevent (or to control) fungal disease(s) or named fungal disease', None),
            ('q6b', 'Q6(b)', '4-3-2', 'why-house-beef-in-winter', 'Housing of beef animals in the winter.', 'To provide shelter (from harsh weather) or higher live-weight gain or easier to feed or easier supervision or prevents poaching or more grass in spring or lack of grass outdoors in winter or allows higher stocking rates', None),
            ('q6c', 'Q6(c)', '4-3-3', 'why-pare-hooves', 'Paring the hooves of sheep.', 'To treat foot-rot or to prevent lameness or to remove infected growth or allows oxygen to circulate between hooves', None),
            ('q6d', 'Q6(d)', '2-3', 'why-agitate-slurry', 'Agitating slurry before it is spread.', 'To break hard crust or to mix the solids and liquid or to allow gases to escape or easier to spread', '1-6'),
            ('q6e', 'Q6(e)', '2-3', 'why-plant-shelter-belts', 'Planting shelter belts on a farm.', 'To prevent damage to buildings or to keep animals warm or to protect crops or to increase soil temperature or habitat for wildlife or natural boundaries or improved crop growth (on sheltered side) or reduces soil erosion', '1-6')]:
        add(key, ref, topic, concept, 'State one reason for the following farming practice: ' + item, [point(answer, 4, 'One reason, 4 marks (5(4) across the five practices).')], practice, node=node)
    # Question 7: one shared scale over (a) and (b) ---------------------------
    figured(add('q7', 'Q7', '3-3-1', 'clover-nodules',
                'The photograph shows nodules on the roots of a clover plant. (a) (i) Name the plant family to which clover belongs. (ii) What is contained in the root nodules in clover? '
                '(iii) What is the role of the contents of these nodules? (iv) Name another plant belonging to the same plant family as clover. '
                '(b) State three beneficial effects of including clover in a seed mixture when reseeding grassland.',
                [split('(a)(i) Clover family — Leguminosae or Fabaceae or Papilionaceae or legumes', SHARED.format('3(4) + 4(2)') + ' Seven answers: (i)-(iv) and three effects.'),
                 split('(a)(ii) In root nodules — Bacteria'), split('(a)(iii) Role of nodule bacteria — To fix nitrogen (or described)'),
                 split('(a)(iv) Plant in same family as clover — Peas or beans or vetch or gorse (furze, whin)'),
                 split('(b) Beneficial effects of clover in grassland seed mixture — Reduces amount of artificial N-fertiliser needed/ palatable/ productive/ digestible/ rich in protein/ used in organic farming/ increases grass growth/ fixes nitrogen or increases soil fertility/ good ground cover or controls weeds/ rich in minerals or named mineral/ meets REPS requirements', 'Any three.')],
                marks=20, tariff={'kind': 'orderedSplit', 'notation': '3(4) + 4(2)'}, node='2-6|1-4'), 'q7')
    # Question 8 -------------------------------------------------------------
    add('q8ai', 'Q8(a)(i)', '4-3-1', 'pig-housing-features', 'State two features of the housing used in pig production.',
        [menu('Well insulated|draught free|low roof|warm|well ventilated|adequate space|(clean) water supply|good hygiene', [4, 4], 'Any two, 4 marks each (2(4)).')], node='3-3')
    add('q8aii', 'Q8(a)(ii)', '4-3-1', 'pig-housing-importance', 'State the importance of any one of those housing features.',
        [menu(['Well insulated: Reduces heat loss or prevents over-heating (in summer)', 'Draught free: Reduces chill or prevents disease(s)', 'Low roof: Easier to heat',
               'Warm: Increases live-weight gain or lowers FCR', 'Well ventilated: Prevents disease(s) or removes stale air or removes gases',
               'Adequate space: Reduces spread of disease(s) or animal welfare', '(Clean) water: Prevents dehydration', 'Good hygiene: Prevents disease(s)'], [4],
              'The importance of any one of your features, 4 marks.')], 'State two features of the housing used in pig production.', node='3-3')
    figured(add('q8aiii', 'Q8(a)(iii)', '4-3-3', 'why-farrowing-crates', 'The photograph shows a sow and bonhams (piglets) in a farrowing crate. State two reasons for using farrowing crates.',
                [menu('Allows bonhams to suck|allows bonhams access to a creep area|restricts movement of sow (or prevents bonhams being crushed or reduced mortality rates in bonhams)', [4, 4],
                      'Any two, 4 marks each (2(4)).')], node='3-3|3-5'), 'q8aiii')
    add('q8bi', 'Q8(b)(i)', '4-1', 'sow-gestation', 'What is the length of gestation for a sow?',
        [point('3 months + 3 weeks + 3 days (or 110 – 118 days)', 4, '5(4) across (b): 4 marks for each answer.')], node='3-0')
    add('q8bii', 'Q8(b)(ii)', '4-3-1', 'sow-litter-size', 'What is the average litter size for a sow?', [point('9 – 12 (bonhams)', 4)], node='3-3')
    add('q8biii', 'Q8(b)(iii)', '4-3-3', 'piglet-rearing-reasons',
        'Explain why each of the following is carried out in the rearing of pigs: 1. Bonhams (piglets) are given an iron injection 2. Lysine is included in the diet of pigs 3. A creep area is used.',
        [point('1. Why iron injection — To prevent anaemia or sow’s milk is low in iron', 4),
         point('2. Why lysine in diet — Pigs are not able to make their own or it is an essential amino acid', 4),
         point('3. Why creep area — Allows bonhams access to high temp (or 30 °C) or keeps bonhams warm or prevents bonhams being crushed or allows creep feeding', 4)], node='3-5|3-4')
    sheep = [('hill', 'Hill (mountain) sheep production', ['Rough grazing or named example(s)', 'Extensive or described', 'One lamb per ewe', 'Low stocking rate or example', 'Low labour input']),
             ('lowland', 'Lowland sheep production', ['Good quality grazing or named example(s)', 'Intensive or described', 'Ewes may have twins or triplets', 'High stocking rate or example', 'High labour input'])]
    headings = ['(i) Grass quality', '(ii) Method of grazing', '(iii) Number of lambs', '(iv) Stocking rate', '(v) Labour']
    rows, variants = routes([(slug, label, [point(f'{h} — {a}', 4, f'{label}: 5(4), 4 marks for each heading.' if i == 0 else None)
                                            for i, (h, a) in enumerate(zip(headings, answers))]) for slug, label, answers in sheep])
    add('q8c', 'Q8(c)', '4-3-1', 'hill-or-lowland-sheep',
        'Describe either hill (mountain) sheep production or lowland sheep production under the following headings: (i) Grass quality (ii) Method of grazing (iii) Number of lambs produced (iv) Stocking rate (v) Amount of labour involved.',
        rows, selection=closed(1, [label for _, label, _ in sheep]), node='3-3', extra={'answerVariants': variants})
    # Question 9 -------------------------------------------------------------
    reseed = 'Many farmers reseed grassland on a regular basis.'
    add('q9ai', 'Q9(a)(i)', '3-3-1', 'why-reseed-grassland', 'State two reasons why grassland may have to be reseeded.',
        [menu('Poaching damage|poor quality grass(es)(in old sward)|weed infestation (in old sward)|to increase productivity or yield|to improve digestibility|to improve palatability|to improve stocking rates|to introduce clover into sward|to increase silage yields (IRG)',
              [3, 3], 'Any two, 3 marks each (2(3)).')], reseed, node='2-6')
    add('q9aii', 'Q9(a)(ii)', '3-2', 'reseeding-grass-species', 'Name two grass species commonly used when reseeding.',
        [menu('Perennial rye grass (or PRG)|Italian rye grass (or IRG)|Timothy|hybrid ryegrass', [3, 3], 'Any two, 3 marks each (2(3)).')], reseed, node='2-6|2-1')
    add('q9aiii', 'Q9(a)(iii)', '3-2', 'grass-species-reason', 'Explain the reason for using any one of the grass species named.',
        [menu(['PRG: Palatable or productive or digestible or persistent or long growing season', 'IRG: Palatable or productive or digestible or long growing season or short term ley',
               'Timothy: Palatable or productive or digestible or suitable for hay',
               'Hybrid ryegrass: Combines desirable characteristics of PRG and IRG or palatable or productive or digestible or persistent or long growing season'], [3],
              'A reason for any one of your species, 3 marks.')], reseed, node='2-6')
    add('q9aiv', 'Q9(a)(iv)', '3-3-2', 'why-top-grassland', 'State two reasons why grassland is topped.',
        [menu('Increases tillering|weed control|encourages leafy growth|increases yield of grass|removes stemmy growth (or undigestible parts of grass) or increases digestibility', [3, 3],
              'Any two, 3 marks each (2(3)).')], reseed, node='2-6')
    silage = 'Feeding good quality silage is essential for cattle to reach production targets.'
    add('q9bi', 'Q9(b)(i)', '3-3-3', 'making-pit-silage', 'List four stages in making good quality pit silage.',
        [menu('Close off field for at least six weeks|fertilise (or spread slurry)|cut in afternoon|cut at correct growth stage|allow grass to wilt|use a precision or double-chop harvester|roll the pit|use additive|seal pit',
              [3] * 4, 'Any four, 3 marks each (4(3)).')], silage, node='2-6')
    add('q9bii', 'Q9(b)(ii)', '3-3-3', 'silage-step-importance', 'Explain the importance of any two of the steps mentioned.',
        [menu(['Close off field for at least six weeks: Gives time for grass to grow', 'Fertilise (or spread slurry): Provides the nutrients for growth',
               'Cut at the correct growing stage: Higher DMD or grass more leafy (or less stemmy)', 'Cut grass at mid-day: Higher concentration of sugar (or carbohydrates)',
               'Allow grass to wilt: Increases dry matter content or less effluent', 'Use a precision or double chop harvester: Better fermentation or sugar released',
               'Roll the grass thoroughly: Creates anaerobic conditions (or eliminates air)', 'Use additive (or named additive): Better fermentation or lowers pH',
               'Seal pit tightly: Anaerobic conditions or prevents rotting of grass'], [3, 3], 'The importance of any two of your steps, 3 marks each (2(3)).')], silage, node='2-6')
    add('q9biii', 'Q9(b)(iii)', '3-3-3', 'silage-dmd-meaning', 'Explain what is meant by the DMD of silage.',
        [point('Dry matter digestibility or the % of dry matter that can be digested', 3)], silage, node='2-6')
    add('q9biv', 'Q9(b)(iv)', '3-3-3', 'silage-dmd-target', 'State the DMD of good quality silage.', [point('70% or greater', 3)], silage, node='2-6')
    figured(add('q9c', 'Q9(c)', '3-3-2', 'catch-crops',
                'The photograph shows stubble turnips which are grown as a catch crop. (i) What is meant by the term catch crop? (ii) Name another example of a catch crop. '
                '(iii) State two methods of feeding catch crops to farm animals. (iv) Suggest two reasons why farmers are encouraged to grow catch crops.',
                [split('(i) Catch crop — Crop grown after one main crop and before another [allow between main crops]', SHARED.format('4(3) + 2 + 1') + ' Six answers: (i), (ii), two methods and two reasons.'),
                 split('(ii) Example of catch crop — Kale or rape or fodder beet or stubble turnips or any other correct'),
                 split('(iii) How to feed catch crop to animals — In situ (or described)/ strip graze (or described)/ zero graze (or described)/ ensile', 'Any two.'),
                 split('(iv) Why grow catch crops — Fast growing/ high yield/ winter feed/ feed in early spring/ high protein content/ less silage (or concentrates) needed/ prevents nitrogen leaching/ extra feed during fodder shortage', 'Any two.')],
                marks=15, tariff={'kind': 'orderedSplit', 'notation': '4(3) + 2 + 1'}, node='2-4|2-6'), 'q9c')
    # Question 10 ------------------------------------------------------------
    add('q10a', 'Q10(a)', '4-1', 'genetics-terms', 'Explain the following terms used in genetics: (i) Gamete (ii) In-breeding (iii) Clone.',
        [split('(i) Gamete — A sex cell [allow a sperm (cell) or an egg (cell)]', SHARED.format('4 + 2(3)') + ' Three answers.'),
         split('(ii) In-breeding — Mating or crossing two closely related (species of) plants or animals'),
         split('(iii) Clone — A group of genetically identical organisms or a group of asexually produced offspring from the same parent [allow an asexually reproduced individual]')],
        marks=10, tariff={'kind': 'orderedSplit', 'notation': '4 + 2(3)'}, node='3-6')
    polled = 'Livestock without horns are referred to as polled animals. In sheep the gene for having no horns (P) is dominant, and the gene for having horns (p) is recessive.'
    add('q10b', 'Q10(b)', '4-1', 'polled-cross-1',
        'Copy and complete the following to give the genotype and phenotype of the lambs from the cross. Parents’ phenotypes: Pure-breeding polled ram × Horned ewe. Parents’ genotypes: PP × pp. Gametes: ( ) × ( ). Genotype of offspring: ( ). Phenotype of offspring: ____.',
        [point('Gametes: (P)', 4, 'Gametes 2(4), offspring genotype 4, offspring phenotype 4.'), point('Gametes: (p)', 4),
         point('Offspring genotype: (Pp)', 4), point('Offspring phenotype: Polled (or no horns)', 4)], polled, node='3-6')
    add('q10c', 'Q10(c)', '4-1', 'polled-cross-2',
        'A ram and a ewe with the same genotype as the offspring above are bred with each other. Copy and complete the following to give the possible genotypes and phenotypes of the lambs from this cross. '
        'Parents’ genotypes: ( ) × ( ). Possible gametes: ( ) ( ) × ( ) ( ). Genotypes of offspring: ( ) ( ) ( ). Phenotypes of offspring: ____ ____.',
        [point('Parents’ genotypes — (Pp) × (Pp)', 4, '2(2): 2 for each parent\'s genotype.'),
         point('Possible gametes — (P) (p) × (P) (p)', 8, '4(2): 2 for each gamete.'),
         menu(['(PP)', '(Pp)', '(pp)'], [2, 2, 2], 'Offspring genotypes, 3(2).'),
         menu(['Polled', 'Horned'], [2, 2], 'Offspring phenotypes, 2(2).')], polled, node='3-6')
    ai = 'Artificial insemination (AI) is carried out on some farm animals.'
    add('q10di', 'Q10(d)(i)', '4-3-2', 'ai-advantages', 'State two advantages of artificial insemination.',
        [menu('Can select superior bulls or better choice|bulls have been performance tested|bulls have been progeny tested|can use sexed semen|easier to transport|less chance of sexually transmitted diseases|cheaper than keeping a bull|choose bulls with lower calving difficulty history|don’t have to keep a dangerous animal',
              [3, 3], 'Any two, 3 marks each (2(3)).')], ai, node='3-6|3-4')
    add('q10dii', 'Q10(d)(ii)', '4-3-2', 'ai-disadvantages', 'State two disadvantages of artificial insemination.',
        [menu('Need for accurate heat detection|semen must be stored properly|lower conception rate|more labour intensive|must be carried out by trained personnel|may also have to keep a bull',
              [3, 3], 'Any two, 3 marks each (2(3)).')], ai, node='3-6|3-4')
    # Question 11 ------------------------------------------------------------
    add('q11ai', 'Q11(a)(i)', '2-1', 'rock-types-from-list',
        'From the list of rock types below, name 1. a sedimentary rock 2. a metamorphic rock 3. an igneous rock. The list: basalt, sandstone, marble, granite, limestone, slate.',
        [point('1. Sedimentary — Sandstone or limestone or shale', 4), point('2. Metamorphic — Marble or slate or quartzite', 4), point('3. Igneous — Basalt or granite', 4)], node='1-0')
    add('q11aii', 'Q11(a)(ii)', '2-1', 'weathering-meaning', 'What is meant by the weathering of rock?', [point('The breaking down of rock (into small particles)', 4)], node='1-0')
    add('q11aiii', 'Q11(a)(iii)', '2-1', 'how-rock-weathers', 'Describe two ways in which rock is weathered.',
        [menu('Water in cracks in rock freezes and expands|acid in rain dissolves rock|heating and cooling causes rock to expand and contract|roots grow into cracks and split the rock|sea waves break up rock|animals break rocks by digging or burrowing or trampling|glaciers crush rock|oxidation-reduction reactions decompose rock|quarrying breaks rock|farm cultivation can break rock|hydration can decompose rock minerals|water can dissolve minerals in rocks',
              [4, 4], 'Any two ways; the scheme awards each 2 + 2 (2(2 + 2)).')], node='1-0')
    soils = [('sandy', 'Sandy soil', ['Coarse or rough', 'Large', 'Poor', 'Suitable or easily tilled']),
             ('clay', 'Clay soil', ['Fine or smooth', 'Small', 'Good', 'Not suitable or difficult to till'])]
    heads = ['(i) How the soil feels', '(ii) Particle size', '(iii) Fertility', '(iv) Suitability for tillage']
    rows, variants = routes([(slug, label, [point(f'{h} — {a}', 4, f'{label}: 4 marks for each heading.' if i == 0 else None)
                                            for i, (h, a) in enumerate(zip(heads, answers))]) for slug, label, answers in soils])
    add('q11b', 'Q11(b)', '2-2-2', 'sandy-or-clay-soil',
        'Describe a sandy soil or a clay soil under the following headings: (i) How the soil feels (ii) Particle size (iii) Fertility (iv) Suitability for tillage.',
        rows, selection=closed(1, [label for _, label, _ in soils]), node='1-3', extra={'answerVariants': variants})
    add('q11ci', 'Q11(c)(i)', '2-2-3', 'organic-matter-importance', 'State two reasons why organic matter is important in a soil.',
        [menu('Increases soil fertility or provides nutrients|retains water|improves soil structure|increases number of earthworms|binds the soil|improves soil aeration|creates humus (when decomposed)', [4, 4],
              'Any two, 4 marks each (2(4)).')], node='1-4')
    add('q11cii', 'Q11(c)(ii)', '2-3', 'adding-organic-matter', 'State two ways in which organic matter may be added to soil.',
        [menu('Spreading farmyard manure|spreading slurry|green manure (or described)|adding seaweed|crop rotation|animal dung when grazing|topping grassland|ploughing in stubble', [4, 4],
              'Any two, 4 marks each (2(4)).')], node='1-5|1-4')
    add('q11ciii', 'Q11(c)(iii)', '2-2-2', 'clay-soils-in-drought', 'Explain why plants grown in clay soil survive better in a drought than those grown in sandy soil.',
        [point('Clay soils retain more water or more water lost by drainage in sandy soils or small soil particles in clay hold more water than larger sand particles or clay soils have better capillarity or clay soils are able to bring up water from deeper in the soil', 4)],
        node='1-3')
    # Question 12 ------------------------------------------------------------
    calf = 'Describe the care and management of a new-born dairy calf from birth to weaning, under the following headings.'
    for key, ref, concept, heading, points, node in [
            ('q12ai', 'Q12(a)(i)', 'dairy-calf-care-at-birth', 'Care at birth', 'Feed colostrum|clear mucus from nose and mouth|spray navel with iodine|adequate supervision or have experienced person at hand|call vet if necessary|clean bedding|dry calf or ensure cow licks calf', '3-5'),
            ('q12aii', 'Q12(a)(ii)', 'dairy-calf-diet', 'Changes in diet', 'Colostrum|cow’s milk|milk replacer|concentrates|hay (or roughage)', '3-4'),
            ('q12aiii', 'Q12(a)(iii)', 'dairy-calf-housing', 'Housing', 'Straw bed or dry bed|good hygiene or disinfect house|good ventilation|draught free|water supply|adequate space|lighting', '3-4'),
            ('q12aiv', 'Q12(a)(iv)', 'dairy-calf-disease-control', 'Disease control', 'Good hygiene|vaccination|monitor health or good supervision|colostrum|calving box|isolate sick animal(s)|good feeding practices|call vet', '3-5')]:
        add(key, ref, '4-3-3' if node == '3-5' else '4-3-2', concept, 'Describe the care and management of a new-born dairy calf from birth to weaning under the heading: ' + heading + '.',
            [menu(points, [3, 3], 'Any two, 3 marks each (2(3)).')], calf, node=node)
    mastitis = 'Maintaining hygiene in a milking parlour is important; nevertheless, cows do sometimes contract mastitis.'
    figured(add('q12bi', 'Q12(b)(i)', '4-3-3', 'mastitis-cause-and-symptoms', '1. What causes mastitis? 2. Describe two symptoms of mastitis.',
                [point('1. Cause of mastitis — Bacteria', 3),
                 menu('Swollen udder or lumps on udder or on teats|tender udder|redness in udder|cow irritable|watery milk or yellowing of milk|bloody or curdled milk|high cell count', [3, 3],
                      '2. Symptoms of mastitis: any two, 3 marks each (2(3)).')],
                'The photograph shows cows in a milking parlour. ' + mastitis, node='3-5'), 'q12bi')
    add('q12bii', 'Q12(b)(ii)', '4-3-2', 'parlour-hygiene-reason', 'Give another reason why maintaining a high level of hygiene in a milking parlour is important.',
        [point('To prevent spread of disease or to keep a low bacterial count in the milk or to ensure milk is not contaminated from dirty equipment or to ensure operator does not transfer infection from one cow to another or to ensure milk is not contaminated by dirt on cow’s udder or to avoid penalties for dirty milk', 3)],
        mastitis, node='3-4|3-5')
    add('q12biii', 'Q12(b)(iii)', '4-3-2', 'maintaining-parlour-hygiene', 'State any three ways that hygiene is maintained before, during, or after milking.',
        [menu('Clean housing (e.g. lime and/or sawdust on floor of cubicles)|sterilised equipment|milker hygiene|clean milking parlour|teat dips used|udder hygiene|fly control|milk is filtered|milk is refrigerated|clean bulk tank',
              [3, 3, 3], 'Any three, 3 marks each (3(3)).')], mastitis, node='3-4|3-5')
    caps = 'Maximum of 12 marks if no result given; all points may be obtained from a labelled diagram; maximum of 3 marks for an unlabelled diagram.'
    rows, variants = routes([(slug, label, [menu(points, [3] * 5, f'{label}: any five, 3 marks each (5(3)). {caps}')]) for slug, label, points in [
        ('resazurin', 'Resazurin test', 'Two sterile test tubes|equal amount of different milk sample into each test-tube|add resazurin (or methylene blue) solution to each|record colour of each at start|kept at 37 °C|in water-bath|for 15 minutes|change to blue is good quality|change to white is poorest quality|pink or mauve is intermediate quality (for resazurin)'),
        ('agar', 'Agar plates', 'Two sterile nutrient agar plates|two different milk samples|inoculating loop|flame loop|transfer milk from each sample onto each dish or method of transfer|invert dishes|incubate at 25 °C|suitable time|count the colonies in each dish|staler milk will have more bacteria colonies than fresher milk')]])
    add('q12c', 'Q12(c)', '4-3-2', 'milk-hygiene-experiment', 'Describe an experiment to compare the hygiene quality of two milk samples.', rows,
        selection=closed(1, ['Resazurin test', 'Agar plates']), node='3-4|0-1', extra={'answerVariants': variants})
    # Question 13: any two of (a)-(d) -----------------------------------------
    two = 'Answer any two of (a), (b), (c), (d).'
    add('q13a', 'Q13(a)', '3-3-1', 'maincrop-potatoes',
        '(i) Name two varieties of maincrop potatoes. (ii) Describe the growing of maincrop potatoes under the following headings: 1. Soil preparation 2. Time of planting 3. Weed control 4. Method of harvesting 5. Expected yield 6. Method of storage.',
        [split('(i) Maincrop potato varieties — Rooster/ Kerr Pinks/ Golden Wonder/ Cara/ Record', SHARED.format('7(4) + 2') + ' Eight answers: two varieties and the six headings.'),
         split('(ii) 1. Soil preparation — Plough (or dig) or remove stones or rotavate or harrow or rake soil'),
         split('(ii) 2. When to plant — March ‒ April'),
         split('(ii) 3. Weed control — Spray or apply herbicide (or weed-killer) or mechanical (or explained) or pull by hand or crop rotation or burning or shading action or earthing up'),
         split('(ii) 4. Harvesting method — Elevator digger or potato harvester or complete harvester or by hand'),
         split('(ii) 5. Expected yield — 30 ‒ 40 tonnes per hectare'),
         split('(ii) 6. Storage — Cool (or refrigerated store) or dry or pest free or well ventilated shed or in darkness or frost free or high humidity')],
        two, marks=30, tariff={'kind': 'orderedSplit', 'notation': '7(4) + 2'}, node='2-3|2-4|2-5')
    figured(add('q13b', 'Q13(b)', '4-1', 'sheep-heart-and-blood',
                'The diagram shows a dissected sheep’s heart. (i) Name the parts labelled A, B, C, D. (ii) The blood in C and D has come from the lungs. State one way blood changes as it passes through the lungs. '
                '(iii) Name two types of blood cell and state the function of each. (iv) Name the liquid part of blood.',
                [split('(i) A — Pulmonary artery', SHARED.format('5(4) + 5(2)') + ' Ten answers: four parts, (ii), two cell types with their functions, and (iv).'),
                 split('(i) B — Vena cava'), split('(i) C — Left atrium'), split('(i) D — Left ventricle'),
                 split('(ii) How blood changes through lungs — Loses carbon dioxide or picks up oxygen (or is oxygenated)'),
                 split('(iii) Types of blood cells — Red blood cells/ white blood cells/ platelets', 'Any two.'),
                 split('(iii) Function of red blood cells — Carry oxygen'),
                 split('(iii) Function of white blood cells — Produce antibodies or fight disease or fight infection'),
                 split('(iii) Function of platelets — (Blood) clotting', 'The functions of your two cell types.'),
                 split('(iv) Liquid part of blood — Plasma')],
                two, marks=30, tariff={'kind': 'orderedSplit', 'notation': '5(4) + 5(2)'}, node='3-0'), 'q13b')
    add('q13ci', 'Q13(c)(i)', '3-3-2', 'why-conifers', 'Give two reasons why conifers are the main type of tree grown in Irish forests.',
        [menu('Can withstand harsh climatic conditions (or named harsh condition)|flexible (or do not break easily in the wind)|have shallow root system (for shallow soils in the mountains)|grow well in poorer-quality soils|snow falls off them easily|fast growing|easy to grow',
              [5, 5], 'Any two, 5 marks each (2(5)).')], two, node='2-4')
    add('q13cii', 'Q13(c)(ii)', '3-2', 'irish-conifer-species', 'Name a species of conifer commonly grown in Ireland.',
        [point('Spruce or fir or pine or larch or juniper', 5)], two, node='2-1')
    add('q13ciii', 'Q13(c)(iii)', '3-3-2', 'why-thin-forestry', 'Why are forestry trees thinned at various times?',
        [point('Removes diseased (or damaged) trees or improves quality of remaining trees or increases size of remaining trees or reduces competition (or named example) or improves access or thinnings provide income or useful products made from thinnings', 5)],
        two, node='2-4', note='The scheme prints the 5 marks for (iii) level with the (iv) heading; (iv) carries its own 2(5), so Question 13(c) totals 10 + 5 + 5 + 10 = 30.')
    add('q13civ', 'Q13(c)(iv)', '2-3', 'forestry-environment-benefits', 'State two beneficial effects of forestry on the environment.',
        [menu('Produces oxygen|consumes carbon dioxide|reduces noise|provides habitat for wildlife|provides shelter|aesthetic|prevents soil erosion|natural amenity', [5, 5],
              'Any two, 5 marks each (2(5)).')], two, node='1-6')
    methods = [('bag', 'Plastic bag', 'Potted plant/ water well/ soil covered with plastic/ plant enclosed in a plastic bag (or bell jar)/ leave in a bright place/ for suitable time/ drops of liquid form on the inside of plastic bag (or bell jar)/ test liquid with anhydrous copper sulfate/ colour change from white to blue indicates liquid is water'),
               ('potometer', 'Potometer', 'Cut leafy shoot (at an angle)/ under water/ fill potometer with water/ by submerging/ place shoot in the potometer/ seal shoot in potometer/ introduce bubble into potometer/ place potometer in front of a lamp or in bright place/ record position of bubble/ leave for suitable time/ movement of bubble indicates transpiration'),
               ('celery', 'Coloured dye', 'Celery/ cut under water/ place in coloured dye/ leave for suitable time/ presence of dye in leaves (or in upper part(s) of stem or in xylem vessels) indicates transpiration or upward movement of water (by transpiration)')]
    add('q13d', 'Q13(d)', '3-1', 'transpiration',
        '(i) What is meant by the term transpiration? (ii) State two environmental factors that affect the rate of transpiration. (iii) Why is transpiration important in plants? (iv) Describe an experiment to demonstrate transpiration in a plant.',
        [split('(i) Transpiration — Loss of water vapour through (stomata of) leaves', SHARED.format('6 + 8(3)') + ' Nine answers: (i), two factors, (iii) and five points of one experiment.'),
         split('(ii) Factors affecting transpiration rate — Air temperature/ air movements/ relative humidity/ light intensity/ availability of soil water/ presence or absence of a cuticle', 'Any two.'),
         split('(iii) Importance of transpiration — Cools the plant or brings water through the plant or brings minerals through the plant')]
        + [split(f'(iv) {label} method — {points}', (f'Any five points of one method. {caps}' if slug == 'bag' else None), route=slug) for slug, label, points in methods],
        two, marks=30, tariff={'kind': 'orderedSplit', 'notation': '6 + 8(3)'}, selection=closed(1, [label for _, label, _ in methods]), node='2-0|0-1')
    assert len(p.tasks) == 54, len(p.tasks)
    return p


def reviewed_tasks():
    p = build()
    return p.cards, p.tasks


def paper_review():
    return build().review('54 base tasks, one card each. A shared scale the scheme prints across several parts (Q1, Q5, Q7, Q9(c), Q10(a), Q13(a), (b), (d)) is one task with the scale stated; '
                          'parts priced on their own are separate tasks. Q8(c) hill or lowland sheep, Q11(b) sandy or clay soil, Q12(c) the two milk-hygiene methods and Q13(d)(iv) the three demonstrations are answer routes.')
