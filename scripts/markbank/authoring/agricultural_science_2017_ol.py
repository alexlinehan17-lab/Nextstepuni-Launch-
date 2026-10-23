"""2017 Ordinary: every task authored from the SEC paper and marking scheme (no cards existed).

All 16 paper pages and 16 scheme pages were inspected and the independent census transcribed
before authoring: 71 base tasks, one card each. Section One questions print one scale each:
where it runs across several parts (Q1, Q5, Q6) the question is one task stating the scale
(orderedSplit); where it is one pool of items (Q2-Q4, Q7) the steps sit on the menu. Section Two
parts are priced on their own, and the four Q13(c)(ii) situations carry their own 2(3) each.
The soil pH methods (Q11(c)) are answer routes. Answers are the scheme's words.
"""
from agricultural_science_legacy import Paper, P, point, menu, closed, routes

FILE = 'LC024GLP000EV.pdf'
HASHES = {'exampapers': 'ae9d18e016bfddf1e6b24436b60061e647eff4cf954d1e6c63d8a3c236315310',
          'markingschemes': '14128fb6c59bd93ed27f29e4ca4f92bddc94ac805206c25eeeaf45c4e58bc443'}
SELECTIONS = {
    '858a546507187ca7': ('exam-selection', 'Section One: six of seven independent 20-mark questions; every question is retained.'),
    '448299f42da93ad2': ('exam-selection', 'Section Two: three of six independent 60-mark questions; every question is retained.'),
    '469dd9015b51529e': ('open', 'Q8(c)(i): any two of the four stomach chambers; a marking menu, and (ii) takes a function for each chamber named.'),
    '6a8ecfdfce9bfd71': ('independent-task-selection', 'Q13: two of four independently priced 30-mark parts; all four are retained.'),
    'cd6ca16dbdbebef6': ('open', 'Q13(a)(iii): any two differences between colostrum and milk from the scheme pool; a marking menu.'),
}
SUPPLEMENTARY = [
    (11, 'Describe a method to measure the pH of a soil sample', 'closed', 'Q11(c): the scheme answers by universal indicator OR by pH meter, kept as answer routes on one card.'),
]
ATLAS = {
    'Q1': 'soil-science|scientific-practices-experiments-investigations', 'Q2': 'crop-production|animal-production',
    'Q3': 'animal-physiology|plant-physiology|animal-production|genetics|animal-diseases|grassland', 'Q4': 'animal-diseases',
    'Q5': 'plant-physiology|scientific-practices-experiments-investigations', 'Q6': 'classification-of-organisms|crop-production',
    'Q7': 'fertilisers-pollution-the-environment|animal-production|soil-science|animal-diseases',
    'Q8': 'animal-physiology', 'Q9': 'genetics', 'Q9(c)': 'genetics|animal-production',
    'Q10': 'grassland', 'Q10(d)': 'grassland|scientific-practices-experiments-investigations',
    'Q11': 'soil-science', 'Q11(c)': 'soil-science|scientific-practices-experiments-investigations',
    'Q12': 'plant-physiology', 'Q12(c)': 'plant-physiology|scientific-practices-experiments-investigations',
    'Q13(a)': 'animal-production', 'Q13(b)': 'crop-production', 'Q13(c)': 'fertilisers-pollution-the-environment', 'Q13(d)': 'animal-production',
}
REGIONS = {
    # Drafted by regions.py; each Q13(c)(ii) situation hand-set to its own scheme rows.
'Q1': (P((3, 0.249, 0.953)), P((5, 0.132, 0.529))),
    'Q2': (P((4, 0.033, 0.876)), P((5, 0.529, 0.783))),
    'Q3': (P((5, 0.033, 0.530)), P((6, 0.081, 0.356))),
    'Q4': (P((5, 0.530, 0.907)), P((6, 0.356, 0.560))),
    'Q5': (P((6, 0.033, 0.793)), P((6, 0.560, 0.811))),
    'Q6': (P((7, 0.033, 0.943)), P((7, 0.081, 0.486))),
    'Q7': (P((8, 0.033, 0.782)), P((7, 0.486, 0.874))),
    'Q8(a)(i)': (P((9, 0.206, 0.281)), P((8, 0.106, 0.203))),
    'Q8(a)(ii)': (P((9, 0.206, 0.246), (9, 0.281, 0.333)), P((8, 0.106, 0.133), (8, 0.203, 0.266))),
    'Q8(b)(i)': (P((9, 0.206, 0.246), (9, 0.333, 0.567)), P((8, 0.106, 0.133), (8, 0.266, 0.302))),
    'Q8(b)(ii)': (P((9, 0.206, 0.246), (9, 0.333, 0.532), (9, 0.567, 0.619)), P((8, 0.106, 0.133), (8, 0.302, 0.374))),
    'Q8(c)(i)': (P((9, 0.206, 0.246), (9, 0.619, 0.654)), P((8, 0.106, 0.133), (8, 0.374, 0.425))),
    'Q8(c)(ii)': (P((9, 0.206, 0.246), (9, 0.654, 0.707)), P((8, 0.106, 0.133), (8, 0.425, 0.696))),
    'Q8(d)(i)': (P((9, 0.206, 0.246), (9, 0.705, 0.915)), P((8, 0.106, 0.133), (8, 0.696, 0.797))),  # the whole (d) block: the heart diagram sits beside its lines
    'Q8(d)(ii)': (P((9, 0.206, 0.246), (9, 0.705, 0.915)), P((8, 0.106, 0.133), (8, 0.797, 0.866))),  # the whole (d) block: the heart diagram sits beside its lines
    'Q8(d)(iii)': (P((9, 0.206, 0.246), (9, 0.705, 0.915)), P((8, 0.106, 0.133), (8, 0.866, 0.911))),  # the whole (d) block: the heart diagram sits beside its lines
    'Q9(a)(i)': (P((10, 0.033, 0.142)), P((9, 0.081, 0.186))),
    'Q9(a)(ii)': (P((10, 0.033, 0.107), (10, 0.142, 0.177)), P((9, 0.081, 0.116), (9, 0.186, 0.221))),
    'Q9(a)(iii)': (P((10, 0.033, 0.107), (10, 0.177, 0.229)), P((9, 0.081, 0.116), (9, 0.221, 0.242))),
    'Q9(b)(i)': (P((10, 0.033, 0.072), (10, 0.229, 0.333)), P((9, 0.081, 0.116), (9, 0.242, 0.291))),
    'Q9(b)(ii)': (P((10, 0.033, 0.072), (10, 0.229, 0.299), (10, 0.333, 0.559)), P((9, 0.081, 0.116), (9, 0.291, 0.448))),
    'Q9(b)(iii)': (P((10, 0.033, 0.072), (10, 0.229, 0.299), (10, 0.559, 0.786)), P((9, 0.081, 0.116), (9, 0.448, 0.604))),
    'Q9(c)(i)': (P((10, 0.033, 0.072), (10, 0.786, 0.821)), P((9, 0.081, 0.116), (9, 0.604, 0.709))),
    'Q9(c)(ii)': (P((10, 0.033, 0.072), (10, 0.821, 0.842)), P((9, 0.081, 0.116), (9, 0.709, 0.788))),
    'Q10(a)(i)': (P((11, 0.033, 0.395)), P((10, 0.081, 0.166))),
    'Q10(a)(ii)': (P((11, 0.033, 0.360), (11, 0.395, 0.431)), P((10, 0.081, 0.113), (10, 0.166, 0.288))),
    'Q10(a)(iii)': (P((11, 0.033, 0.360), (11, 0.431, 0.465)), P((10, 0.081, 0.113), (10, 0.288, 0.323))),
    'Q10(a)(iv)': (P((11, 0.033, 0.360), (11, 0.465, 0.500)), P((10, 0.081, 0.113), (10, 0.323, 0.400))),
    'Q10(b)(i)': (P((11, 0.033, 0.069), (11, 0.500, 0.534)), P((10, 0.081, 0.113), (10, 0.400, 0.488))),
    'Q10(b)(ii)': (P((11, 0.033, 0.069), (11, 0.534, 0.569)), P((10, 0.081, 0.113), (10, 0.488, 0.561))),
    'Q10(c)': (P((11, 0.033, 0.069), (11, 0.569, 0.604)), P((10, 0.081, 0.113), (10, 0.561, 0.790))),
    'Q10(d)': (P((11, 0.033, 0.069), (11, 0.604, 0.652)), P((10, 0.081, 0.113), (10, 0.790, 0.917))),  # down to the table's foot: the last 3 sits below the text
    'Q11(a)(i)': (P((11, 0.652, 0.723)), P((11, 0.081, 0.218))),
    'Q11(a)(ii)': (P((11, 0.652, 0.688), (11, 0.723, 0.758)), P((11, 0.081, 0.113), (11, 0.218, 0.322))),
    'Q11(a)(iii)': (P((11, 0.652, 0.688), (11, 0.758, 0.792)), P((11, 0.081, 0.113), (11, 0.322, 0.357))),
    'Q11(a)(iv)': (P((11, 0.652, 0.688), (11, 0.792, 0.827)), P((11, 0.081, 0.113), (11, 0.357, 0.384))),
    'Q11(b)': (P((11, 0.652, 0.688), (11, 0.827, 0.862)), P((11, 0.081, 0.113), (11, 0.384, 0.511))),
    'Q11(c)': (P((11, 0.652, 0.688), (11, 0.862, 0.884)), P((11, 0.081, 0.113), (11, 0.511, 0.673))),
    'Q12(a)(i)': (P((12, 0.033, 0.365)), P((12, 0.081, 0.163))),
    'Q12(a)(ii)': (P((12, 0.033, 0.330), (12, 0.365, 0.400)), P((12, 0.081, 0.135), (12, 0.163, 0.232))),
    'Q12(a)(iii)': (P((12, 0.033, 0.330), (12, 0.400, 0.435)), P((12, 0.081, 0.135), (12, 0.232, 0.267))),
    'Q12(a)(iv)': (P((12, 0.033, 0.330), (12, 0.435, 0.487)), P((12, 0.081, 0.135), (12, 0.267, 0.355))),
    'Q12(b)(i)': (P((12, 0.033, 0.072), (12, 0.487, 0.733)), P((12, 0.081, 0.113), (12, 0.355, 0.407))),
    'Q12(b)(ii)': (P((12, 0.033, 0.072), (12, 0.487, 0.698), (12, 0.733, 0.770)), P((12, 0.081, 0.113), (12, 0.407, 0.442))),
    'Q12(b)(iii)': (P((12, 0.033, 0.072), (12, 0.487, 0.698), (12, 0.770, 0.805)), P((12, 0.081, 0.113), (12, 0.442, 0.511))),
    'Q12(b)(iv)': (P((12, 0.033, 0.072), (12, 0.487, 0.698), (12, 0.805, 0.857)), P((12, 0.081, 0.113), (12, 0.511, 0.564))),
    'Q12(c)': (P((12, 0.033, 0.072), (12, 0.857, 0.879)), P((12, 0.081, 0.113), (12, 0.564, 0.643))),
    'Q13(a)(i)': (P((13, 0.033, 0.394)), P((13, 0.081, 0.166))),
    'Q13(a)(ii)': (P((13, 0.033, 0.372), (13, 0.394, 0.411)), P((13, 0.081, 0.137), (13, 0.166, 0.218))),
    'Q13(a)(iii)': (P((13, 0.033, 0.372), (13, 0.411, 0.429)), P((13, 0.081, 0.137), (13, 0.218, 0.305))),
    'Q13(a)(iv)': (P((13, 0.033, 0.372), (13, 0.429, 0.446)), P((13, 0.081, 0.137), (13, 0.305, 0.444))),
    'Q13(a)(v)': (P((13, 0.033, 0.372), (13, 0.446, 0.463)), P((13, 0.081, 0.137), (13, 0.444, 0.496))),
    'Q13(a)(vi)': (P((13, 0.033, 0.372), (13, 0.463, 0.481)), P((13, 0.081, 0.137), (13, 0.496, 0.583))),
    'Q13(a)(vii)': (P((13, 0.033, 0.372), (13, 0.481, 0.498)), P((13, 0.081, 0.137), (13, 0.583, 0.618))),
    'Q13(a)(viii)': (P((13, 0.033, 0.372), (13, 0.498, 0.529)), P((13, 0.081, 0.137), (13, 0.618, 0.655))),
    'Q13(b)(i)': (P((13, 0.033, 0.095), (13, 0.529, 0.569)), P((13, 0.081, 0.113), (13, 0.655, 0.723))),
    'Q13(b)(ii)': (P((13, 0.033, 0.095), (13, 0.529, 0.550), (13, 0.569, 0.587)), P((13, 0.081, 0.113), (13, 0.655, 0.676), (13, 0.723, 0.775))),
    'Q13(b)(iii)': (P((13, 0.033, 0.095), (13, 0.529, 0.550), (13, 0.587, 0.604)), P((13, 0.081, 0.113), (13, 0.655, 0.676), (13, 0.775, 0.827))),
    'Q13(b)(iv)': (P((13, 0.033, 0.095), (13, 0.529, 0.550), (13, 0.604, 0.621)), P((13, 0.081, 0.113), (13, 0.655, 0.676), (13, 0.827, 0.889))),
    'Q13(b)(v)': (P((13, 0.033, 0.095), (13, 0.529, 0.550), (13, 0.621, 0.639)), P((13, 0.081, 0.113), (13, 0.655, 0.676), (14, 0.081, 0.151))),
    'Q13(b)(vi)': (P((13, 0.033, 0.095), (13, 0.529, 0.550), (13, 0.639, 0.669)), P((13, 0.081, 0.113), (13, 0.655, 0.676), (14, 0.151, 0.224))),
    'Q13(c)(i)': (P((13, 0.033, 0.095), (13, 0.669, 0.709)), P((13, 0.081, 0.113), (14, 0.224, 0.273))),
    'Q13(c)(ii) — silage': (P((13, 0.033, 0.095), (13, 0.669, 0.690), (13, 0.709, 0.823)), P((13, 0.081, 0.113), (14, 0.224, 0.244), (14, 0.273, 0.296), (14, 0.296, 0.352))),  # its own situation
    'Q13(c)(ii) — dairy farm': (P((13, 0.033, 0.095), (13, 0.669, 0.690), (13, 0.709, 0.823)), P((13, 0.081, 0.113), (14, 0.224, 0.244), (14, 0.273, 0.296), (14, 0.362, 0.439))),  # its own situation
    'Q13(c)(ii) — fertiliser': (P((13, 0.033, 0.095), (13, 0.669, 0.690), (13, 0.709, 0.823)), P((13, 0.081, 0.113), (14, 0.224, 0.244), (14, 0.273, 0.296), (14, 0.449, 0.544))),  # its own situation
    'Q13(c)(ii) — insecticides': (P((13, 0.033, 0.095), (13, 0.669, 0.690), (13, 0.709, 0.823)), P((13, 0.081, 0.113), (14, 0.224, 0.244), (14, 0.273, 0.296), (14, 0.553, 0.625))),  # its own situation
    'Q13(d)(i)': (P((13, 0.033, 0.095), (13, 0.823, 0.877)), P((13, 0.081, 0.113), (14, 0.625, 0.714))),
    'Q13(d)(ii)': (P((13, 0.033, 0.095), (13, 0.823, 0.860), (13, 0.877, 0.894)), P((13, 0.081, 0.113), (14, 0.625, 0.645), (14, 0.714, 0.767))),
    'Q13(d)(iii)': (P((13, 0.033, 0.095), (13, 0.823, 0.860), (13, 0.894, 0.912)), P((13, 0.081, 0.113), (14, 0.625, 0.645), (14, 0.767, 0.819))),
    'Q13(d)(iv)': (P((13, 0.033, 0.095), (13, 0.823, 0.860), (13, 0.912, 0.929)), P((13, 0.081, 0.113), (14, 0.625, 0.645), (14, 0.819, 0.836))),
    'Q13(d)(v)': (P((13, 0.033, 0.095), (13, 0.823, 0.860), (13, 0.929, 0.953)), P((13, 0.081, 0.113), (14, 0.625, 0.645), (14, 0.836, 0.898))),
}
SHARED = 'Shared scale {}: the first correct answers earn the higher award, whichever part they answer, so no part carries a mark of its own.'
FIGURES = {
    'q1': ('agsci-2017-ol-paper-burning-soil', None),
    'q2': ('agsci-2017-ol-paper-farm-machinery', [('A', 'Cattle crush (the completed example)', False), ('B', 'Bale wrapper', True), ('C', 'Crop sprayer', True),
                                                  ('D', 'Slurry tank', True), ('E', 'Power harrow', True), ('F', 'Combine harvester', True)]),
    'q5': ('agsci-2017-ol-paper-germination-flasks', [('A', 'Vacuum flask of germinating peas', False), ('B', 'Vacuum flask of boiled peas', False)]),
    'q6': ('agsci-2017-ol-paper-butterfly-life-cycle', [('W', 'Adult (or imago)', True), ('X', 'Egg', True), ('Y', 'Larva (or caterpillar)', True), ('Z', 'Pupa (or chrysalis)', True)]),
    'q8bi': ('agsci-2017-ol-paper-cow-skull', [('A', 'Incisor', True), ('B', 'Molar', True)]),
    'q8bii': ('agsci-2017-ol-paper-cow-skull', None),
    'q8diii': ('agsci-2017-ol-paper-cow-heart', None),
    'q8di': ('agsci-2017-ol-paper-cow-heart', [('A', '(Right) atrium', True), ('B', 'Aorta', True), ('C', 'Septum', True), ('D', '(Left) ventricle', True)]),
    'q8dii': ('agsci-2017-ol-paper-cow-heart', None),
    'q10ai': ('agsci-2017-ol-paper-reseeding-plants', None), 'q10aii': ('agsci-2017-ol-paper-reseeding-plants', None),
    'q10aiii': ('agsci-2017-ol-paper-reseeding-plants', None), 'q10aiv': ('agsci-2017-ol-paper-reseeding-plants', None),
    'q12ai': ('agsci-2017-ol-paper-leaf-section', [('A', 'Stoma', True), ('B', 'Cells whose main function is photosynthesis', False)]),
    'q12aii': ('agsci-2017-ol-paper-leaf-section', None),
    'q12aiii': ('agsci-2017-ol-paper-leaf-section', [('A', 'Stoma', False), ('B', 'Cells whose main function is photosynthesis', True)]),
    'q12aiv': ('agsci-2017-ol-paper-leaf-section', None),
    'q12bi': ('agsci-2017-ol-paper-stem-section', None),
    'q12bii': ('agsci-2017-ol-paper-stem-section', [('X', 'Vascular bundles (or vascular tissue) or phloem and xylem', True)]),
    'q12biii': ('agsci-2017-ol-paper-stem-section', None),
    'q13ai': ('agsci-2017-ol-paper-milk-pie-chart', [('A', 'Water (87.5%)', True)]),
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
    p = Paper(2017, 'ordinary', FILE, HASHES, REGIONS, ATLAS, 16, 16, SELECTIONS, SUPPLEMENTARY,
              section=lambda ref: 'A' if int(ref.split('(')[0].split(' ')[0][1:]) <= 7 else 'B')
    add = p.add
    # Section One ------------------------------------------------------------
    figured(add('q1', 'Q1', '2-2-3', 'soil-organic-matter',
                '(a) The diagram shows a soil sample being burned to find the percentage (%) organic matter in it. (i) Why was a dry soil sample used? (ii) How would a student know when all the organic matter has been removed from the soil? '
                '(b) (i) State two reasons why organic matter is important in a soil. (ii) State two ways that organic matter may be added to a soil. (iii) Name two components of soil other than organic matter.',
                [split('(a)(i) Why dry soil — So loss in mass is not due to water loss', SHARED.format('2(7) + 6(1)') + ' Eight answers: (a)(i), (a)(ii) and two for each of (b)(i)-(iii).'),
                 split('(a)(ii) How know all organic matter gone — No further smoke from soil or constant mass reached or soil turns black'),
                 split('(b)(i) Why organic matter important — Humus/ improves soil fertility/ improves soil structure/ increases earthworm activity/ improves pore space/ improves soil aeration/ improves soil drainage', 'Any two.'),
                 split('(b)(ii) How organic matter added to soil — Add FYM/ spread slurry/ add leaf mould/ add straw/ add (mushroom) compost/ add seaweed/ green manure/ crop rotation', 'Any two.'),
                 split('(b)(iii) Two other components of soil — Particles or one named particle type/ minerals or one named mineral/ living organisms or one named microorganism (or invertebrate)/ water/ air', 'Any two.')],
                marks=20, tariff={'kind': 'orderedSplit', 'notation': '2(7) + 6(1)'}, node='1-4|0-1'), 'q1')
    machines = [('Power harrow', 'E', 'To cultivate soil or to break up lumps of soil or to produce a fine seed bed'),
                ('Combine harvester', 'F', 'To harvest cereal (or named cereal)'),
                ('Bale wrapper', 'B', 'To wrap silage or to bale silage or to cover bales with plastic'),
                ('Crop sprayer', 'C', 'To apply herbicide (or weedkiller) or to apply fungicide or to apply pesticide or to apply growth regulator'),
                ('Slurry tank', 'D', 'To apply slurry')]
    figured(add('q2', 'Q2', '2-3', 'farm-machinery-letters-uses',
                'The following images show equipment/machinery used on farms. In the table identify and state the main use for each item: Power harrow; Combine harvester; Bale wrapper; Crop sprayer; Slurry tank. '
                'Item A is completed as an example: Cattle crush, A, To control animals for testing or dosing.',
                [menu([f'{name}: {letter}', use], [2, 2], f'{name}: its letter and its main use, 2 marks each (10(2)).') for name, letter, use in machines],
                tariff={'kind': 'fixed', 'notation': '10(2)'}, node='2-3|3-4'), 'q2')
    statements = [('a', 'Diaphragm separates chest from abdomen', 'T'), ('b', 'Hay develops rumen', 'T'), ('c', 'Cows’ gestation is seven months', 'F'),
                  ('d', 'Landrace is a sheep breed', 'F'), ('e', 'Animal gametes made by meiosis', 'T'), ('f', 'Vaccination provides immunity', 'T'),
                  ('g', 'Peas are legumes', 'T'), ('h', 'DMD of good silage is 50%', 'F'), ('i', 'Grass is dicot', 'F'), ('j', 'Plumule becomes stem', 'T')]
    add('q3', 'Q3', '4-1', 'true-or-false-farm-science',
        'Indicate whether the following statements are true (T) or false (F) by placing a circle around the correct answer in each case. Example: Basalt is an igneous rock — T. '
        '(a) The diaphragm separates the chest from the abdomen in mammals. (b) Hay helps to develop the rumen in calves. (c) The length of gestation in cows is seven months. (d) Landrace is a breed of sheep. '
        '(e) Animal gametes are produced as a result of meiosis. (f) Vaccination provides immunity. (g) Peas belong to the plant family Leguminosae (Fabaceae). (h) The dry matter digestibility (DMD) of good quality silage is 50%. '
        '(i) Grass is a dicot plant. (j) The plumule of a seed develops into the stem.',
        [menu([f'({k}) {s}: {a}' for k, s, a in statements], [2] * 10, 'All ten statements, 2 marks each (10(2)). T = true, F = false; the scheme words each statement as shown.')],
        tariff={'kind': 'fixed', 'notation': '10(2)'}, node='3-0|2-0|3-6|3-5|2-6')
    add('q4', 'Q4', '4-3-3', 'causes-of-animal-diseases',
        'Diseases of farm animals may be caused by viruses, bacteria, fungi or by a deficiency (of a vitamin or a mineral) in their diet. In the table indicate the cause of each of the diseases listed '
        '(the cause of foot rot, bacteria, is completed as an example): Swayback in lambs; Foot and mouth disease; Milk fever in cows; Ringworm; Tuberculosis (TB).',
        [menu(['Swayback: Deficiency', 'Foot and mouth disease: Virus', 'Milk fever in cows: Deficiency', 'Ringworm: Fungus', 'Tuberculosis: Bacteria'], [7, 7, 2, 2, 2],
              'All five, 2(7) + 3(2): the first two correct answers earn 7 each and the next three 2 each.')],
        tariff={'kind': 'fixed', 'notation': '2(7) + 3(2)'}, node='3-5')
    figured(add('q5', 'Q5', '3-1', 'germination-heat-flasks',
                'The diagram shows the apparatus used in an investigation on seed germination. (a) What aspect of seed germination is being investigated? '
                '(b) What change, if any, would you expect to find in the temperature inside each flask after 5 days? Flask A; Flask B. (c) Why was the inside of each flask sterilised at the beginning of the investigation? '
                '(d) State the three conditions necessary for seed germination.',
                [split('(a) What aspect of germination being tested — That heat is released from germinating seeds or that living organisms release heat during respiration', SHARED.format('2(5) + 5(2)') + ' Seven answers: (a), each flask, (c) and three conditions.'),
                 split('(b) Flask A — Temperature will rise'), split('(b) Flask B — Temperature remains the same'),
                 split('(c) Why flasks sterilised inside — To kill micro-organisms or to prevent contamination or to prevent peas rotting'),
                 split('(d) Three conditions for seed germination — (i) Water (or moisture) (ii) Suitable temperature (or warmth) (iii) Oxygen (or air)')],
                marks=20, tariff={'kind': 'orderedSplit', 'notation': '2(5) + 5(2)'}, node='2-0|0-1'), 'q5')
    figured(add('q6', 'Q6', '3-3-2', 'cabbage-white-life-cycle',
                'The diagram shows the stages of complete metamorphosis in the life cycle of the cabbage white butterfly. (a) Name the stages labelled W, X, Y, Z. (b) (i) State the different feeding methods of stage W and of stage Y. '
                '(ii) State the agricultural importance of stage W and of stage Y. (c) Name one other insect and state its agricultural importance.',
                [split('(a) W — Adult (or imago)', SHARED.format('5(3) + 5(1)') + ' Ten answers: four stages, two feeding methods, two importances, the insect and its importance.'),
                 split('(a) X — Egg'), split('(a) Y — Larva (or caterpillar)'), split('(a) Z — Pupa (or chrysalis)'),
                 split('(b)(i) Adult (W) — Sucks (nectar)'), split('(b)(i) Larva (Y) — Eats (leaves)'),
                 split('(b)(ii) Adult (W) — Pollinates crops [allow pollination]'), split('(b)(ii) Larva (Y) — Crop pest or eats crops or damages crops or reduces yield'),
                 split('(c) Other insect — Leatherjacket/ wireworm/ aphid/ louse (or lice)/ blowfly (or greenbottle) /bee /fly / ladybird'),
                 split('(c) Importance — Must match named insect', 'The importance of the insect you named.')],
                marks=20, tariff={'kind': 'orderedSplit', 'notation': '5(3) + 5(1)'}, node='2-4'), 'q6')
    add('q7', 'Q7', '2-3', 'reasons-for-farm-practices',
        'Give one scientific reason for each of the following practices carried out on Irish farms: (a) Growing shelter belts. (b) Keeping milk at approximately 4 °C in a bulk tank. (c) Tagging young animals. '
        '(d) Spreading ground limestone. (e) Injecting bonhams (piglets) with an iron solution.',
        [menu(['Shelter belts: Prevent damage to farm buildings or reduce wind damage or protect crops or protect livestock or wildlife habitat or land boundary or natural fencing or natural amenity or sound barrier or replenish oxygen or reduce carbon dioxide or increase soil temperature',
               'Milk at 4 °C: Slows down growth of bacteria or prevents milk from going sour or milk will stay fresh for longer or milk can be stored for longer',
               'Tagging young animals: To identify animals or traceability or record keeping or legal requirement',
               'Spreading lime: Raises pH or reduces soil acidity or improves soil structure or flocculation or provides calcium or improves soil drainage or improves soil aeration or improves crop growth or higher yields or improved microbial activity or more earthworm activity or improves soil fertility or increases nutrient availability or increases effectiveness of fertilisers',
               'Injecting bonhams with iron: Prevents anaemia'], [7, 7, 2, 2, 2],
              'One reason for each practice, 2(7) + 3(2): the first two correct reasons earn 7 each and the next three 2 each.')],
        tariff={'kind': 'fixed', 'notation': '2(7) + 3(2)'}, node='1-6|3-4|1-2|3-5')
    # Question 8 -------------------------------------------------------------
    add('q8ai', 'Q8(a)(i)', '4-1', 'cow-skeleton-functions', 'State three functions of the cow’s skeleton.',
        [menu('Protection|support|movement|produces blood cells|storage of minerals', [3] * 3, 'Any three, 3 marks each (3(3)).')], node='3-0')
    add('q8aii', 'Q8(a)(ii)', '4-1', 'bone-mineral-and-vitamin', 'Name one mineral and one vitamin necessary for proper bone development.',
        [point('Mineral: Calcium or phosphorus', 3), point('Vitamin: (Vitamin) D', 3)], node='3-0')
    skull = 'The photograph shows a cow’s skull.'
    figured(add('q8bi', 'Q8(b)(i)', '4-1', 'cow-teeth-types', 'Name the types of tooth labelled A and B.',
                [point('A = Incisor', 3, '2(3).'), point('B = Molar', 3)], skull, node='3-0'), 'q8bi')
    figured(add('q8bii', 'Q8(b)(ii)', '4-1', 'cow-teeth-functions', 'State the function of A and the function of B.',
                [point('A: To cut or bite (food)', 3), point('B: To crush (or chew or grind) (food)', 3)], skull, node='3-0'), 'q8bii')
    add('q8ci', 'Q8(c)(i)', '4-1', 'cow-stomach-chambers', 'Name any two chambers of the cow’s stomach.',
        [menu('Rumen|reticulum|omasum|abomasum', [3, 3], 'Any two, 3 marks each (2(3)).')], node='3-0')
    add('q8cii', 'Q8(c)(ii)', '4-1', 'stomach-chamber-functions', 'State the function of each of the chambers referred to in (i).',
        [menu(['Rumen: Digests cellulose or digests roughage (or named roughage) or contains bacteria', 'Reticulum: Traps sharp objects or regurgitates food',
               'Omasum: Removes water or squeezes food or dries food or water re-absorbed', 'Abomasum: Chemical digestion of food or acid produced or enzymes produced or digestion similar to true stomach'],
              [3, 3], 'Any one point from each of the two chambers you named in (i), 3 marks each (2(3)).')], 'Name any two chambers of the cow’s stomach.', node='3-0')
    heart = 'The diagram shows a section through a cow’s heart.'
    figured(add('q8di', 'Q8(d)(i)', '4-1', 'cow-heart-parts', 'Name each of the parts labelled A, B, C, D.',
                [point('A = (Right) atrium', 3), point('B = Aorta', 3), point('C = Septum', 3), point('D = (Left) ventricle', 3)], heart, node='3-0'), 'q8di')
    figured(add('q8dii', 'Q8(d)(ii)', '4-1', 'septum-function', 'State the function of part C.',
                [point('Prevents blood from both sides mixing or prevents oxygenated and de-oxygenated blood from mixing', 6)], heart, node='3-0'), 'q8dii')
    figured(add('q8diii', 'Q8(d)(iii)', '4-1', 'heart-location', 'State the location of the heart in the cow’s body.',
        [point('Chest (or thorax) or between lungs or above diaphragm', 3)], heart, node='3-0'), 'q8diii')
    # Question 9 -------------------------------------------------------------
    terms = 'Explain the following terms used in genetics.'
    for key, ref, concept, term, answer in [
            ('q9ai', 'Q9(a)(i)', 'haploid', 'Haploid', 'Half the diploid number of chromosomes or one copy of each chromosome [allow one set of chromosomes]'),
            ('q9aii', 'Q9(a)(ii)', 'homozygous', 'Homozygous', 'Both alleles are the same [allow pure breeding]'),
            ('q9aiii', 'Q9(a)(iii)', 'locus', 'Locus', 'Position of a gene on a chromosome')]:
        add(key, ref, '4-1', concept, f'Explain the term used in genetics: {term}.', [point(answer, 4)], terms, node='3-6')
    barley = 'The pure-breeding barley variety Alpha (AA) has a straw length of 800 mm. The pure-breeding barley variety Beta (BB) has a straw length of 600 mm. A cross between these two varieties results in a hybrid with a straw length of 700 mm.'
    add('q9bi', 'Q9(b)(i)', '4-1', 'incomplete-dominance-straw', 'What does this show about the genes that control straw length in this example?',
        [point('They are incompletely dominant or co-dominant or of equal dominance', 4)], barley, node='3-6')
    add('q9bii', 'Q9(b)(ii)', '4-1', 'barley-cross-1',
        'Copy and complete the following to show the cross between the Alpha and Beta varieties of barley. Parents: Pure-breeding Alpha X Pure-breeding Beta. Genotypes of parents: ( ) X ( ). Gametes: ( ) X ( ). Genotype of offspring: ( ). Phenotype of hybrid offspring: ____.',
        [point('Genotypes of parents — (AA ) X (BB)', 4, '2(2): 2 for each parent.'), point('Gametes — (A) X (B)', 4, '2(2): 2 for each gamete.'),
         point('Genotype of offspring — (AB)', 2), point('Phenotype of offspring — 700 mm', 2)], barley, node='3-6')
    add('q9biii', 'Q9(b)(iii)', '4-1', 'barley-cross-2',
        'The hybrid plants were allowed to self-pollinate and the resulting seeds were sown. Copy and complete the following, using the above hybrids as parents. Genotype of parents: ( ) X ( ). Gametes: ( )( ) X ( )( ). Genotypes of offspring: ( ) ( ) ( ). Phenotypes of offspring: ____ ____ ____.',
        [point('Genotype of parents — (AB) X (AB)', 4, '2(2): 2 for each parent.'), point('Gametes — (A) (B) X (A) (B)', 8, '4(2): 2 for each gamete.'),
         menu(['(AA)', '(AB)', '(BB)'], [2, 2, 2], 'Genotypes of offspring, 3(2).'), menu(['800 mm', '700 mm', '600 mm'], [2, 2, 2], 'Phenotypes of offspring, 3(2).')], barley, node='3-6')
    add('q9ci', 'Q9(c)(i)', '4-3-2', 'ai-advantage', 'State one advantage of using artificial insemination (AI) on a dairy farm.',
        [point('Improves quality of offspring or can select superior bull or no need to keep a bull (on a small farm) or bull performance tested or progeny tested or less risk of disease or less physical damage or less dangerous or less wastage of semen or semen can be sexed', 4)],
        node='3-6|3-4')
    add('q9cii', 'Q9(c)(ii)', '4-3-2', 'ai-disadvantage', 'State one disadvantage of using AI on a dairy farm.',
        [point('Heat has to be detected accurately or skilled technician required to inseminate cows or more labour or more time consuming or difficult to detect heifers in heat or stock bull may be required for mopping up at end of breeding season', 4)],
        node='3-6|3-4')
    # Question 10 ------------------------------------------------------------
    plants = 'The pictures show two plants that could be used when reseeding a pasture.'
    figured(add('q10ai', 'Q10(a)(i)', '3-2', 'grass-in-picture', 'Name the grass variety in picture A.',
                [point('Perennial ryegrass or PRG [allow ryegrass or Italian ryegrass or IRG]', 3)], plants, node='2-6|2-1'), 'q10ai')
    figured(add('q10aii', 'Q10(a)(ii)', '3-3-1', 'why-reseed-with-ryegrass', 'Give two reasons why a farmer would use this grass when reseeding.',
                [menu('High yield or high productivity|highly digestible or high % DMD|palatable or “sweet”|high tillering capacity|long growing season|recovers well after grazing|supports high stocking rates|promotes high milk yields or promotes high weight gains|good quality grass|nutritious|aggressive (not for IRG)|persistent (not for IRG)',
                      [3, 3], 'Any two, 3 marks each (2(3)).')], plants, node='2-6'), 'q10aii')
    figured(add('q10aiii', 'Q10(a)(iii)', '3-2', 'plant-in-picture', 'Name the plant in picture B.', [point('Clover', 3)], plants, node='2-6|2-1'), 'q10aiii')
    figured(add('q10aiv', 'Q10(a)(iv)', '3-3-1', 'why-clover-in-mixture', 'Give two reasons why plant B would be used in a seed mixture.',
                [menu('Nitrogen fixation|rich in protein|palatable or “sweet”|good ground cover|high digestibility|productive|weed control|rich in minerals or named mineral|less N required|increases grass growth or yield',
                      [3, 3], 'Any two, 3 marks each (2(3)).')], plants, node='2-6'), 'q10aiv')
    add('q10bi', 'Q10(b)(i)', '3-3-2', 'why-control-grassland-weeds', 'Give one reason why weeds should be controlled in grassland.',
        [point('Reduces competition (or named example of competition) or increases growth (or yield) of grass or legal requirement or removes noxious weeds or prevents poisoning of livestock', 3)], node='2-6')
    add('q10bii', 'Q10(b)(ii)', '3-3-2', 'non-chemical-weed-control', 'State two ways of controlling weeds in grassland, other than using herbicide (weedkiller).',
        [menu('Topping|(hand) pulling|using certified seed|crop rotation|mixed grazing|avoid overgrazing|apply lime or maintain correct pH|maintain good soil fertility|good drainage|reseeding', [3, 3],
              'Any two, 3 marks each (2(3)).')], node='2-6')
    add('q10c', 'Q10(c)', '3-3-2', 'strip-grazing', 'Describe strip grazing, with the aid of a labelled diagram.',
        [point('Diagram: Grazing area divided into strips by fence', 3),
         menu('Front fence or (movable) electric fence|back fence|water supply|area of recovery or regrowth|direction of fence movement', [2, 2, 2], 'Labels: any three, 2 marks each (3(2)).'),
         menu('Land divided into strips|(movable) electric fence|livestock graze strip for 24 hours|fresh strip each day (or fence moved each day)|N applied after grazing|back fence prevents trampling of regrowth|livestock return to 1st strip after 3-4 weeks|movable or fixed water supply',
              [3, 3, 3], 'Description: any three, 3 marks each (3(3)).')], node='2-6')
    add('q10d', 'Q10(d)', '3-3-3', 'grass-sugar-experiment', 'Describe an experiment to find the percentage (%) sugar in a sample of grass.',
        [point('Dry grass', 3), point('Grass into plastic bag or remove air or seal bag', 3),
         point('Bag into freezer or for at least 24 hours or cells burst or sap released or remove from freezer or allow to thaw or collect sap', 3),
         point('Refractometer', 3), point('Calibrate or sap on refractometer or read % sugar or repeat or get average', 3)], node='2-6|0-1')
    # Question 11 ------------------------------------------------------------
    add('q11ai', 'Q11(a)(i)', '2-1', 'iron-pan-formation', 'Explain how an iron pan is formed in a soil.',
        [point('Conditions: High rainfall or high altitude or low temperature or low evaporation or low pH (or acidic)', 4),
         menu('Iron leaches|from A horizon|iron deposited|in B horizon|iron solidifies', [4, 4], 'Effect: any two, 4 marks each (2(4)).')], node='1-0')
    add('q11aii', 'Q11(a)(ii)', '2-3', 'iron-pan-effects', 'What are the effects of an iron pan in a soil?',
        [menu('Waterlogging (or poor drainage)|poor aeration (or anaerobic conditions)|peat formation|reduced number of earthworms|reduced microbial activity|poor root growth|growth of water-loving plants|poor grassland (or poor grass growth)',
              [4, 4], 'Any two, 4 marks each (2(4)).')], node='1-5|1-0')
    add('q11aiii', 'Q11(a)(iii)', '2-1', 'iron-pan-soil-group', 'Name the soil group in which an iron pan is most likely to form.', [point('Podzol', 4)], node='1-0')
    add('q11aiv', 'Q11(a)(iv)', '2-3', 'removing-iron-pan', 'How can an iron pan in a soil be removed?', [point('Deep ploughing or subsoiler', 4)], node='1-5')
    add('q11b', 'Q11(b)', '2-2-1', 'soil-sampling', 'Describe the method of taking soil samples for testing.',
        [menu('Divide area to be sampled (into regions 2-4 ha in size)|take samples in W shaped pattern|at random|soil auger|at least 10 cm deep|take a number of samples|avoid gateways (or troughs or areas near ditches)|allow for variations in slope or previous cropping history or soil types|avoid sampling an area that was limed in previous 2 years|do not sample immediately after applying fertilisers',
              [4] * 4, 'Any four, 4 marks each (4(4)).')], node='1-2|0-1')
    common = 'Add soil to beaker|add distilled (or deionised) water|stir'
    rows, variants = routes([(slug, label, [menu(f'{common}|{rest}', [4] * 4, f'{label}: any four, 4 marks each (4(4)).')]) for slug, label, rest in [
        ('indicator', 'Universal indicator', 'filter|add universal indicator solution (or indicator paper) to filtrate|compare colour with pH chart'),
        ('meter', 'pH meter', 'pH meter|insert electrode (of meter) into distilled water to check if meter reading accurately|insert electrode into soil-water mixture|read the pH')]])
    add('q11c', 'Q11(c)', '2-2-1', 'measuring-soil-ph', 'Describe a method to measure the pH of a soil sample.', rows,
        selection=closed(1, ['Universal indicator', 'pH meter']), node='1-2|0-1', extra={'answerVariants': variants})
    # Question 12 ------------------------------------------------------------
    leaf = 'The diagram shows a section of a leaf.'
    figured(add('q12ai', 'Q12(a)(i)', '3-1', 'leaf-feature-a', 'Name the feature labelled A.', [point('A = Stoma', 4)], leaf, node='2-0'), 'q12ai')
    figured(add('q12aii', 'Q12(a)(ii)', '3-1', 'stoma-functions', 'State two functions of A.',
                [menu('Gaseous exchange|allows carbon dioxide in|allows oxygen out|allows water (vapour) out (or allows transpiration)', [4, 4], 'Any two, 4 marks each (2(4)).')], leaf, node='2-0'), 'q12aii')
    figured(add('q12aiii', 'Q12(a)(iii)', '3-1', 'cells-b-function', 'What is the main function of the cells labelled B?', [point('Photosynthesis', 4)], leaf, node='2-0'), 'q12aiii')
    figured(add('q12aiv', 'Q12(a)(iv)', '3-1', 'leaf-suited-to-photosynthesis', 'State two ways in which the structure of a leaf is suited to its main role.',
                [menu('Broad (or large surface area)|thin|stomata|large air spaces|most chloroplasts located at top of leaf (or in palisade layer)|good supply of veins (or vascular tissue or xylem or phloem)', [4, 4],
                      'Any two, 4 marks each (2(4)).')], leaf, node='2-0'), 'q12aiv')
    stem = 'The diagram shows a cross section of a plant stem.'
    figured(add('q12bi', 'Q12(b)(i)', '3-2', 'stem-plant-type', 'Name a type of plant that would have a stem cross section like this.', [point('Dicot (or named dicot)', 4)], stem, node='2-1|2-0'), 'q12bi')
    figured(add('q12bii', 'Q12(b)(ii)', '3-1', 'structures-x', 'Name the structures labelled X.', [point('X = Vascular bundles (or vascular tissue) or phloem and xylem', 4)], stem, node='2-0'), 'q12bii')
    figured(add('q12biii', 'Q12(b)(iii)', '3-1', 'vascular-bundle-functions', 'State two functions of X.',
                [menu('Transport water|transport minerals|transport food|strengthen (or support) plant', [4, 4], 'Any two, 4 marks each (2(4)).')], stem, node='2-0'), 'q12biii')
    add('q12biv', 'Q12(b)(iv)', '3-1', 'modified-stem', 'Name a plant that has a modified stem.', [point('e.g. Potato or strawberry or (creeping) buttercup', 4)], node='2-0')
    add('q12c', 'Q12(c)', '3-1', 'phototropism-experiment', 'Describe an experiment to show phototropism in seedlings.',
        [menu('Growing seedlings or growth conditions named|light from one direction|another (or control) plant with light from all sides (or with no light)|time allowed|result stated', [4] * 4,
              'Any four, 4 marks each (4(4)).')], node='2-0|0-1')
    # Question 13 ------------------------------------------------------------
    two = 'Answer any two parts of (a), (b), (c), (d).'
    milk = two + ' The pie-chart shows the approximate composition of cows’ milk: minerals 0.8%, protein 3.2%, butterfat 3.8%, lactose 4.6% and A 87.5%.'
    figured(add('q13ai', 'Q13(a)(i)', '4-3-2', 'milk-component-a', 'What component of milk is represented by the part labelled A?', [point('A = Water', 3)], milk, node='3-4'), 'q13ai')
    for key, ref, topic, concept, question, rows, node in [
            ('q13aii', 'Q13(a)(ii)', '4-3-2', 'colostrum', 'What is colostrum?', [point('First milk a young mammal (or named mammal) gets from its mother', 3)], '3-4'),
            ('q13aiii', 'Q13(a)(iii)', '4-3-2', 'colostrum-versus-milk', 'Give any two differences between colostrum and ordinary milk.',
             [menu('Thick(er)|yellow|low(er) water content|low(er) sugar(or lactose) content|high(er) solids content|rich in nutrients (or named nutrient)|rich in antibodies (or provides (passive) immunity) (or defends against diseases)|laxative', [3, 3],
                   'Any two, 3 marks each (2(3)).')], '3-4'),
            ('q13aiv', 'Q13(a)(iv)', '4-3-2', 'improving-milk-quality', 'Give two ways a farmer could improve the quality of the milk from his herd.',
             [menu('Feed good quality silage or increase fibre in diet or feed concentrates|treat for diseases|cull old cows|introduce breeds (e.g. Jersey) with high fat (or protein)|choose replacements from cows with high protein (or fat)|use A.I. from bulls with history of high protein (or fat)|wash teats|parlour hygiene|milker hygiene|teat dips|introduce younger cows into herd|shorter milking interval|milk cows completely|maintain equipment',
                   [3, 3], 'Any two, 3 marks each (2(3)).')], '3-4'),
            ('q13av', 'Q13(a)(v)', '4-3-3', 'mastitis-milk-withheld', 'Why is the milk from a cow treated for mastitis not allowed into the human food supply?',
             [point('(Milk) contains antibiotics or resistant (strains of) bacteria could develop', 3)], '3-5'),
            ('q13avi', 'Q13(a)(vi)', '4-3-2', 'culling-dairy-cows', 'Give one reasons for culling cows on a dairy farm.',
             [point('Disease or old age or high somatic cell count or calving difficulties or infertility or injury or to improve genetic merit or grading up or low milk yields or low milk quality or slow milker or difficult to get in calf or long calving interval', 3)], '3-4'),
            ('q13avii', 'Q13(a)(vii)', '4-2', 'dual-purpose-breed', 'What is meant by the term dual purpose breed?', [point('Produces both milk and beef (or meat)', 3)], '3-1'),
            ('q13aviii', 'Q13(a)(viii)', '4-2', 'dual-purpose-example', 'Give one example of a dual purpose breed.', [point('Friesian or Shorthorn or Montbeliarde or Simmental', 3)], '3-1')]:
        add(key, ref, topic, concept, question, rows, two, node=node)
    cultivation = two + ' Describe the cultivation of barley under the following headings.'
    for key, ref, topic, concept, heading, rows, node in [
            ('q13bi', 'Q13(b)(i)', '3-3-1', 'barley-soil-type', 'Soil type', [point('Any two appropriate soil types or any one with a key feature described', 6, '2(3).')], '2-3'),
            ('q13bii', 'Q13(b)(ii)', '3-3-1', 'barley-sowing-time', 'Sowing time', [point('Spring barley: February to May or Winter barley: September to November', 3)], '2-3'),
            ('q13biii', 'Q13(b)(iii)', '3-3-1', 'barley-sowing-method', 'Sowing method', [point('Combine drill or seed drill or corn drill or one-pass system', 3)], '2-3'),
            ('q13biv', 'Q13(b)(iv)', '3-3-2', 'barley-weed-control', 'Weed control',
             [menu('Spraying|herbicide (or weed killer)|crop rotation|pull by hand|certified seed|stubble cleaning', [3, 3], 'Any two, 3 marks each (2(3)).')], '2-4'),
            ('q13bv', 'Q13(b)(v)', '3-3-2', 'barley-disease-control', 'Disease control',
             [menu('Certified seed|crop rotation|fungicides|resistant varieties|growth encouragement', [3, 3], 'Any two, 3 marks each (2(3)). The scheme allows spraying if not given in part (iv).')], '2-4'),
            ('q13bvi', 'Q13(b)(vi)', '3-3-3', 'barley-harvesting', 'Harvesting',
             [menu('Combine harvester|any one sign of ripeness described (e.g. harvest when crop turns yellow)|harvest time', [3, 3], 'Any two, 3 marks each (2(3)). Harvest time must match sowing time in part (ii).')], '2-5')]:
        add(key, ref, topic, concept, f'Describe the cultivation of barley under the heading: {heading}.', rows, cultivation, node=node)
    pollution = two + ' Farmers have to be aware of the possibility of causing pollution while working on the farm.'
    add('q13ci', 'Q13(c)(i)', '2-3', 'pollution-meaning', 'What is meant by the term pollution?', [point('Any harmful addition to the environment.', 6)], pollution, node='1-6')
    for slug, label, points in [
            ('silage', 'When making silage', 'Allow silage to wilt|cut during dry weather|seal pit properly|collect silage effluent|covered tank|leak-proof|proper disposal of bale wrap'),
            ('dairy-farm', 'On a dairy farm', 'Collect washings from milking parlour|do not allow milk into waterways|correctly store and dispose of animal medicines|correctly dispose of dead animals'),
            ('fertiliser', 'When spreading artificial fertiliser', 'Apply correct amount|apply at correct growth stage|do not apply near waterways|do not apply to waterlogged soil|do not apply when wet weather is forecast|apply to growing crop|apply in Spring and Summer|use more organic fertilisers'),
            ('insecticides', 'When using insecticides or fungicides', 'Apply correct amount|do not apply just before harvesting|store and dispose of correctly|biological control|crop rotation|certified seed|apply during dry weather|do not apply near waterways')]:
        add(f'q13cii-{slug}', f'Q13(c)(ii) — {slug.replace("-", " ")}', '2-3', f'reducing-pollution-{slug}',
            f'State two ways that a farmer can reduce the risk of causing pollution: {label}.',
            [menu(points, [3, 3], 'Any two, 3 marks each (2(3)).')], pollution, node='1-6')
    weanlings = two + ' Comment on each of the following in relation to weanlings, from first winter housing until they are put out on grass the following spring.'
    for key, ref, topic, concept, heading, rows, node in [
            ('q13di', 'Q13(d)(i)', '4-3-2', 'weanling-housing', 'Housing',
             [menu('Slatted building or cubicles or loose house with straw bedding|dry bed|fresh water|well ventilated|no draughts|adequate floor (or lying) space|group according to size|adequate trough space|good hygiene', [3] * 3, 'Any three, 3 marks each (3(3)).')], '3-4'),
            ('q13dii', 'Q13(d)(ii)', '4-3-2', 'weanling-diet', 'Diet',
             [menu('Silage (or hay, or roughage)|70 – 75% DMD silage|concentrates (or meals)', [3, 3], 'Any two, 3 marks each (2(3)).')], '3-4'),
            ('q13diii', 'Q13(d)(iii)', '4-3-3', 'weanling-parasite-control', 'Control of disease and parasites',
             [menu('Dose (or inject) for worms|dose (or pour on or inject) for skin parasites|vaccinate|adequate ventilation', [3, 3], 'Any two, 3 marks each (2(3)).')], '3-5'),
            ('q13div', 'Q13(d)(iv)', '4-3-2', 'weanling-turnout-weight', 'Target weight at turnout', [point('270-320 kg', 3)], '3-4'),
            ('q13dv', 'Q13(d)(v)', '4-3-2', 'compensatory-growth', 'Compensatory growth',
             [menu('The extra growth an animal puts on|after let out to grass|on a high plane of nutrition|after a period of restricted feeding', [3, 3], 'Any two, 3 marks each (2(3)).')], '3-4')]:
        add(key, ref, topic, concept, f'Comment on the following in relation to weanlings: {heading}.', rows, weanlings, node=node)
    assert len(p.tasks) == 71, len(p.tasks)
    return p


def reviewed_tasks():
    p = build()
    return p.cards, p.tasks


def paper_review():
    return build().review('71 base tasks, one card each. Section One scales: across several parts (Q1, Q5, Q6) one task with the scale stated; one pool of items (Q2-Q4, Q7) with the steps on the menu. '
                          'Section Two parts are priced on their own; the four Q13(c)(ii) situations carry their own 2(3) each. Q11(c) carries the indicator and pH-meter methods as answer routes.')
