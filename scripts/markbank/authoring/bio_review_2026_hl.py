"""Biology 2026 Higher Level — reviewed task ledger.

Independent visual sweep (2026-10-11), every page rendered and read:
  * LC025ALP038EV (Sections A and B and Answerbook), 40 pages: p1 cover,
    p2 instructions, p3-p12 Questions 1-10, p13 Section C answerbook
    instructions, p14-p15 graph paper, p16-p38 ruled answer pages, p39
    acknowledgements, p40 back cover.
  * LC025ALP040EV (Section C), 12 pages: p1 cover, p2-p10 Questions 11-17,
    p11 acknowledgements, p12 back cover.
  * LC025ALP000EV (marking scheme), 36 pages: p1 cover, p2 note, p3-p5
    introduction and marking examples, p6 annotations and grading table, p7
    Irish-medium bonus, p8-p34 Questions 1-17, p35 blank, p36 back cover.

Task boundary rule: one task per printed address (letter, roman or numbered
item) that the scheme prices on its own line or lines. Lines priced inside one
address (two terms to explain, labels under a diagram) stay rows of that task.
Every scheme block closes with an examiner tick summary ("6 x 3 + 1 x 2");
CHECKSUMS pins it and the build of this ledger re-derives it from the rows.

Finite printed routes: Q12(c)(ii) and Q12(c)(iii) each print a closed
choose-one pool ("from one of the following areas: agriculture or fisheries
or forestry. Indicate clearly to which area your answer refers."), so each is
expanded into three route cards at the route tariff. Every other selection
directive on the paper is classified in SELECTION_SCAN with its reason.

Scheme notes carried onto cards:
  * Q16(a): the scheme records an error in the labelling of Diagram B (every
    daughter cell is printed "2n") and awards full marks for (i) and (ii) to
    every candidate who attempted any part of 16(a). The (i) and (ii) cards
    keep the scheme's own answers and carry that note.
  * Q5(e): the paper prints "(such as G A G or C U G)"; the scheme's reprint
    reads "G A G or G U C". The card uses the paper's wording.
  * Q4(d) is answered in the scheme only by a drawing (graph 2 with the curve
    continued upwards). Its one row quotes the scheme's own priced line and the
    scheme's drawing is the card's solution figure.
"""
from bio_review_lib import Q, SQ, S, M, pt, anyn, T, L

YEAR, LEVEL = 2026, 'hl'

SOURCES = {
    '038': {'path': 'examiner-reports/biology/papers/2026-hl-038-paper.pdf',
            'fileid': 'LC025ALP038EV.pdf',
            'sha256': '1c3aa8ed6f7543e9ee2ced1f749ccdf8f85c708317bd243d51c2d4d8503dfa51',
            'pages': 40},
    '040': {'path': 'examiner-reports/biology/papers/2026-hl-040-paper.pdf',
            'fileid': 'LC025ALP040EV.pdf',
            'sha256': 'c86209f155cfce3e0a9ddbd23567c5029b2ae59e8f631b56e951adf911966c24',
            'pages': 12},
    'scheme': {'path': 'examiner-reports/biology/schemes/2026-hl.pdf',
               'fileid': 'LC025ALP000EV.pdf',
               'sha256': '82da86ffaa8e6989e44d4d4175488b5debe07193c31d05316089446888c0571e',
               'pages': 36},
}

PAGE_ROLES = {
    '038': {1: 'cover', 2: 'instructions', **{p: 'questions' for p in range(3, 13)},
            13: 'answerbook-instructions', 14: 'graph-paper', 15: 'graph-paper',
            **{p: 'answer-pages' for p in range(16, 39)}, 39: 'acknowledgements',
            40: 'back-cover'},
    '040': {1: 'cover', **{p: 'questions' for p in range(2, 11)}, 11: 'acknowledgements',
            12: 'back-cover'},
    'scheme': {1: 'cover', 2: 'note', 3: 'introduction', 4: 'marking-examples',
               5: 'marking-examples', 6: 'annotations-grading', 7: 'irish-bonus',
               **{p: 'marking' for p in range(8, 35)}, 35: 'blank', 36: 'back-cover'},
}

# Printed totals: Section A any five of seven at 20, Section B any two of three
# at 30 (6 + 24), Section C any four of seven at 60; Q16 and Q17 any two of
# (a)-(d) at 30 each.
QUESTION_TOTALS = {
    **{n: 20 for n in range(1, 8)}, **{n: 30 for n in range(8, 11)},
    **{n: 60 for n in range(11, 16)},
}
PART_TOTALS = {  # (question, letter) -> printed/scheme part total
    (8, 'a'): 6, (8, 'b'): 24, (9, 'a'): 6, (9, 'b'): 24, (10, 'a'): 6, (10, 'b'): 24,
    (11, 'a'): 9, (11, 'b'): 27, (11, 'c'): 24, (12, 'a'): 9, (12, 'b'): 27, (12, 'c'): 24,
    (13, 'a'): 9, (13, 'b'): 27, (13, 'c'): 24, (14, 'a'): 9, (14, 'b'): 27, (14, 'c'): 24,
    (15, 'a'): 9, (15, 'b'): 27, (15, 'c'): 24,
    **{(n, x): 30 for n in (16, 17) for x in 'abcd'},
}
# Q1 is "best five answers from (a)-(f)": six parts at 4, best five count.
BEST_OF = {1: (5, 4)}

# The examiner tick summary printed under each scheme block, read off the
# rendered scheme pages: {mark value: count}. Keyed by question or
# (question, letter) where the scheme closes a part on its own.
CHECKSUMS = {
    1: {2: 2, 4: 5},          # "2 x2 + 4 x4 or 5 x4": (a) is 2(2), (b)-(f) 4 each
    2: {2: 1, 3: 6}, 3: {3: 6, 2: 1}, 4: {3: 6, 2: 1}, 5: {3: 6, 2: 1},
    6: {3: 2, 2: 7}, 7: {2: 10},
    (8, 'a'): {3: 2}, (8, 'b'): {3: 8}, (9, 'a'): {3: 2}, (9, 'b'): {3: 8},
    (10, 'a'): {3: 2}, (10, 'b'): {3: 8},
    (11, 'a'): {3: 3}, (11, 'b'): {3: 9}, (11, 'c'): {3: 8},
    (12, 'a'): {3: 3}, (12, 'b'): {3: 8, 2: 1, 1: 1}, (12, 'c'): {3: 8},
    (13, 'a'): {3: 2, 1: 3}, (13, 'b'): {3: 5, 2: 4, 1: 4}, (13, 'c'): {3: 7, 2: 1, 1: 1},
    (14, 'a'): {3: 3}, (14, 'b'): {3: 7, 2: 3}, (14, 'c'): {3: 7, 2: 1, 1: 1},
    (15, 'a'): {3: 1, 2: 3}, (15, 'b'): {3: 7, 1: 6}, (15, 'c'): {3: 4, 2: 3, 1: 6},
    (16, 'a'): {3: 9, 1: 3}, (16, 'b'): {3: 9, 2: 1, 1: 1}, (16, 'c'): {3: 9, 2: 1, 1: 1},
    (16, 'd'): {3: 9, 1: 3},
    (17, 'a'): {3: 6, 2: 5, 1: 2}, (17, 'b'): {3: 4, 2: 9}, (17, 'c'): {3: 6, 2: 4, 1: 4},
    (17, 'd'): {3: 5, 2: 6, 1: 3},
}

# Every selection directive on the question pages, in reading order, with its
# disposition. The build re-scans the PDFs and fails if this list drifts.
SELECTION_SCAN = [
    ('038', 2, 'or', 'Instructions: "blue or black pen", not a question.'),
    ('038', 2, 'any five', 'Section A rubric: whole-question choice; every question is carded.'),
    ('038', 2, 'any two', 'Section B rubric: whole-question choice; every question is carded.'),
    ('038', 2, 'any four', 'Section C rubric: whole-question choice; every question is carded.'),
    ('038', 3, 'any five', 'Section A rubric repeated.'),
    ('038', 3, 'any five', 'Q1 best five of (a)-(f): each part is its own card at 4 marks.'),
    ('038', 3, 'the following', 'Q1 parts list.'),
    ('038', 3, 'or', 'Q1(f) "or of any other named vitamin": open choice, one card.'),
    ('038', 4, 'or', 'Q2(e) "(or uses)": synonym, not a choice.'),
    ('038', 7, 'the following', 'Q5 lead-in.'),
    ('038', 7, 'or', 'Q5(e) examples "G A G or C U G", not a choice.'),
    ('038', 8, 'the following', 'Q6 lead-in.'),
    ('038', 9, 'the following', 'Q7 compulsory list of five structures, each its own letter.'),
    ('038', 10, 'any two', 'Section B rubric: whole-question choice.'),
    ('038', 10, 'the following', 'Q8(b)(iii) compulsory numbered items 1 and 2.'),
    ('038', 10, 'or', 'Q8(b)(iii)1 "Washing up liquid or detergent": synonym.'),
    ('038', 10, 'or', 'Answer-box label repeating the same synonym.'),
    ('040', 2, 'any four', 'Section C rubric: whole-question choice.'),
    ('040', 2, 'the following', 'Q11(b) lead-in.'),
    ('040', 3, 'or', 'Q12(b)(ii) "From the passage or otherwise": flexible source, one card.'),
    ('040', 3, 'or', 'Q12(b)(vi) "A or B": the answer, not a route.'),
    ('040', 3, 'one of the following', 'Q12(c)(ii) closed pool of three areas: three route cards.'),
    ('040', 3, 'or', 'Q12(c)(ii) pool: agriculture or fisheries.'),
    ('040', 3, 'or', 'Q12(c)(ii) pool: fisheries or forestry.'),
    ('040', 3, 'one of the following', 'Q12(c)(iii) closed pool of three areas: three route cards.'),
    ('040', 3, 'or', 'Q12(c)(iii) pool: agriculture or fisheries.'),
    ('040', 3, 'or', 'Q12(c)(iii) pool: fisheries or forestry.'),
    ('040', 3, 'any one', 'Q12(c)(v) "any one pollutant": open choice, one card.'),
    ('040', 4, 'both', 'Q13(c)(iii) both naturalists required, not a choice.'),
    ('040', 5, 'or', 'Q14(a) "monocotyledonous (monocot) or dicotyledonous": classification.'),
    ('040', 5, 'any one', 'Q14(b)(ii) any one method of dispersal: open choice.'),
    ('040', 6, 'any three', 'Q15(a)(ii) any three methods: open, priced 3(2).'),
    ('040', 6, 'the following', 'Q15(b) lead-in.'),
    ('040', 6, 'the following', 'Q15(b)(i) compulsory label list.'),
    ('040', 6, 'any one', 'Q15(b)(ii) any one role of oestrogen: open choice.'),
    ('040', 7, 'any two', 'Q16 any two of (a)-(d): every part carded.'),
    ('040', 7, 'the following', 'Q16(a) lead-in.'),
    ('040', 7, 'the following', 'Q16(a)(i) compulsory numbered terms 1 and 2.'),
    ('040', 7, 'any three', 'Q16(a)(iv) label any three parts: scheme menu, Any three 3(1).'),
    ('040', 8, 'or', 'Q16(c)(vii) "(A or B)": the answer, not a route.'),
    ('040', 8, 'any three', 'Q16(d)(iv) label any three parts: open, priced 3(1).'),
    ('040', 8, 'both', 'Q16(d)(v) both underlined terms required.'),
    ('040', 9, 'any two', 'Q17 any two of (a)-(d): every part carded.'),
    ('040', 9, 'the following', 'Q17(a)(ii) compulsory numbered terms.'),
    ('040', 9, 'the following', 'Q17(a)(vi) compulsory numbered factors.'),
    ('040', 10, 'the following', 'Q17(c)(ii)1 compulsory label list.'),
    ('040', 10, 'the following', 'Q17(d)(iv)2 compulsory label list.'),
]
SCAN_PAGES = {'038': range(2, 13), '040': range(2, 11)}

ROUTES = {
    'Q12(c)(ii)': ['agriculture', 'fisheries', 'forestry'],
    'Q12(c)(iii)': ['agriculture', 'fisheries', 'forestry'],
}

SEC = 'State Examinations Commission'
FIGURES = {
    # key suffix: (doc, page, rect in PDF points, credit, letters, alt, solution[, masks])
    # masks: rects (PDF points) of neighbouring page furniture -- an answer box,
    # the end of a printed sentence -- whitened inside the crop.
    'q2-cheek-cells': ('038', 4, (300, 76, 506, 244), 'alamy.com', [],
        'Black-and-white light micrograph of two flattened human cheek cells lying side by '
        'side. Each is an irregular, many-sided cell with one dark oval nucleus near its '
        'centre; small dark specks are scattered over the cytoplasm.', False),
    'q3-breathing-system': ('038', 5, (196, 72, 404, 322), 'biorender.com', [],
        'Grey diagram of a human head in side section above a windpipe and two lungs. A '
        'leader line labelled Epiglottis points to the flap at the top of the windpipe; '
        'Trachea labels the ringed tube that runs down and branches into the lungs, the '
        'left-hand lung drawn solid and the right-hand lung showing branching airways. No '
        'diaphragm and no ribs are drawn.', False),
    'q4-leaf-surface': ('038', 6, (316, 52, 541, 226), 'alamy.com', ['P', 'Q'],
        'Light micrograph of the undersurface of a leaf: long, wavy-walled cells packed in '
        'rows, with five small lens-shaped pores scattered among them. Each pore is '
        'bordered by two curved cells, which a leader line labels Guard cells. Two arrows '
        'labelled P point to pores; two arrows labelled Q point to the ordinary surface '
        'cells between them.', False, [(316, 118, 338, 226)]),
    'q4-graphs': ('038', 6, (128, 270, 412, 424), SEC, [],
        'Two line graphs side by side, each with Time on the horizontal axis. Graph 1, '
        '"Concentration of gas X", is a straight line rising steadily from a point part-way '
        'up the vertical axis. Graph 2, "Size of openings P", is a curve that starts high and '
        'falls, levelling off towards the right.', False),
    'q5-translation': ('038', 7, (288, 238, 545, 482), 'biorender.com', ['A', 'B'],
        'Diagram of translation: a large grey blob labelled Structure A sits on a horizontal '
        'strand labelled mRNA, whose bases read A U G, G A G, C U G, C U A, G U A, A C A. '
        'Clover-shaped molecules carrying small balls dock on the strand by matching '
        'three-base sequences (U A C, C U C, G A C, G A U); an arrow labelled B points to one '
        'of them. The balls joined in a chain above are labelled Growing amino acid sequence.',
        False),
    'q6-nitrogen-cycle': ('038', 8, (110, 140, 362, 330), SEC, ['A', 'B', 'C', 'X', 'Y'],
        'Flow diagram of the nitrogen cycle with boxes for Nitrogen gas, Nitrate, Plant '
        'biomolecules, Animal biomolecules, Urea, Molecule X and Molecule Y. A curved arrow A '
        'runs from Nitrogen gas to Nitrate. Nitrate leads to Plant biomolecules, and arrow B '
        'runs from Plant biomolecules to Animal biomolecules. Animal biomolecules, Urea and '
        'Plant biomolecules all lead to Molecule X; a curved arrow C runs from Molecule X up '
        'to Molecule Y and on, as C again, to Nitrate. No arrow leaves Nitrate or the '
        'molecules for Nitrogen gas.', False),
    'q12-population-graph': ('040', 3, (402, 384, 542, 498), SEC, ['A', 'B'],
        'Graph of Population against Time with two wavy lines. Solid line A rises and falls '
        'in two tall peaks; dashed line B, lower on the graph, rises and falls in smaller '
        'peaks that come a little after the peaks of A.', False),
    'q14-germinating-seed': ('040', 5, (426, 284, 550, 458), 'dreamstime.com', ['A', 'B', 'C'],
        'Photograph of a bean seed shortly after germination began. Arrow A points to the '
        'rounded seed itself; a curved shoot with a small pair of leaves grows up and to the '
        'right of it, labelled C; a long pale root with thin side branches grows downwards, '
        'labelled B.', False, [(426, 430, 466, 458)]),
    'q14-xylem-vessel': ('040', 5, (420, 520, 546, 690), SEC, [],
        'Drawing of a single upright xylem vessel: a long tube with pitted, wavy side walls, '
        'open at the top, with water drawn as dots inside it and two upward arrows showing '
        'water moving up the vessel. A leader line labels Water.', False),
    'q15-embryo-stages': ('040', 6, (134, 374, 512, 470), 'biorender.com', ['A', 'B', 'C'],
        'Three circles joined by arrows, left to right, showing early human embryo stages. A '
        'is a single cell with a membrane around it and two small round bodies inside; B is a '
        'solid ball of about a dozen cells; C is a hollow ball of many small cells with a '
        'cluster of cells at the top inside it.', False),
    'q16-cell-division': ('040', 7, (110, 102, 512, 246), 'biorender.com', [],
        'Two boxed diagrams. Box A: a parent cell marked 2n divides into two daughter cells, '
        'each marked 2n. Box B: a parent cell marked 2n divides into four daughter cells, '
        'each also marked 2n. The scheme records that the labelling of Diagram B is an error.',
        False),
    'q16-virus': ('040', 7, (424, 444, 542, 570), 'biorender.com', ['X', 'Y'],
        'Diagram 1: a round virus with spikes around its outer coat. Arrow X points to the '
        'tip of a spike on the outer coat; arrow Y points to a coiled strand inside the '
        'virus.', False),
    'q16-virus-host': ('040', 7, (424, 572, 542, 692), 'biorender.com', [],
        'Diagram 2: a small round virus at the edge of a large host cell, with a short arrow '
        'pointing from the virus into the cell, which has a round nucleus drawn inside it.',
        False),
    'q16-plant-cells': ('040', 8, (344, 52, 543, 202), SEC, [],
        'Two plant cells side by side in rectangular containers. In solution A the cell '
        'contents have shrunk away from the cell wall into an irregular shape held by thin '
        'strands. In solution B the cell is full, with a large vacuole pressing the contents '
        'against the wall.', False),
    'q16-yeast': ('040', 8, (420, 400, 546, 610), 'biorender.com', [],
        'Diagram of a yeast cell with a small bud growing from its top: a dark nucleus '
        'stretches up into the bud, a large pale vacuole fills the lower half of the cell, '
        'and a few small striped organelles lie in the cytoplasm.', False),
    'q17-capillary-network': ('040', 9, (350, 82, 546, 252), 'biorender.com', ['X', 'Y'],
        'A capillary network between two vessels. Blood in enters a vessel on the left; X '
        'labels the small vessel branching into a mesh of fine capillaries among round '
        'cells; the capillaries rejoin into the small vessel labelled Y on the right, which '
        'leads to Blood out. An arrow along the bottom is labelled Blood flow, pointing left '
        'to right.', False),
    'q17-skin': ('040', 9, (336, 456, 546, 572), SEC, [],
        'Outline of a block of skin, labelled Skin: three roughly horizontal lines divide it '
        'into layers, with no glands, hairs or vessels drawn in.', False),
    'q17-nephron': ('040', 10, (371, 172.5, 527, 338), 'biorender.com', ['A', 'B'],
        'Diagram of a nephron: a cup-shaped capsule holding a knot of capillaries at the top '
        'left, labelled A, leads into a coiled tubule, a long hairpin loop labelled B at the '
        'bottom, a second coiled tubule, and a collecting duct on the right.', False),
    'q17-spinal-cord': ('040', 10, (338, 452, 550, 606), 'biorender.com', ['P', 'Q', 'Y'],
        'Cross-section of the spinal cord: a pale outer region labelled P around a darker '
        'butterfly-shaped inner region labelled Q, with a tiny central canal labelled Central '
        'canal. Y labels the thin layered covering around the outside of the cord.', False),
    'q4d-scheme-graph': ('scheme', 10, (96, 230, 330, 351.4), SEC, [],
        'The scheme\'s answer to Question 4(d): graph 2, Size of openings P against Time, with '
        'the printed falling curve continued by the examiner: it flattens at a low point and '
        'then rises again towards the top right.', True),
    'q13a-scheme-nucleotide': ('scheme', 21, (258, 100, 508, 204), SEC, [],
        'The scheme\'s model drawing of a DNA nucleotide: a circle labelled Phosphate joined to '
        'a pentagon labelled Deoxyribose, which is joined at another corner, at an angle, to '
        'a double ring of a hexagon and a pentagon labelled (Nitrogenous) base.', True),
    'q13b-ii-scheme': ('scheme', 21, (108, 324, 296, 344), SEC, [],
        'The scheme\'s accepted forms of the heterozygous female genotype: XXNn, XNXn, X with N '
        'and X with n written as subscripts, and X with N and X with n written as '
        'superscripts.', True),
    'q13b-iii-scheme': ('scheme', 21, (108, 364, 296, 384), SEC, [],
        'The scheme\'s accepted forms of the colour-blind male genotype: XYn followed by a '
        'dash, XnY followed by a dash, and the same with n written as a subscript and as a '
        'superscript on the X.', True),
    'q13b-iv-scheme': ('scheme', 21, (104, 415, 490, 497), SEC, [],
        'The scheme\'s table of the four possible offspring: each row gives a genotype in four '
        'equivalent notations (letters in line, then as subscripts, then as superscripts on '
        'the X) worth 2 marks, and its matching phenotype worth 1 mark — female normal (colour '
        'vision), female colour-blind, male normal (colour vision), male colour-blind.', True),
}


def _A(page, start, end=None, **kw):
    return Q(page, start, end, doc='038', **kw)


def _C(page, start, end=None, **kw):
    return Q(page, start, end, doc='040', **kw)


ERRATUM = S('Due to the error in the labelling', 'of this question.')
Q6_STEM = _A(8, 'The diagram below shows the nitrogen cycle.')
Q12_PASSAGE = [_C(3, 'Read the passage below'),
               _C(3, 'Vine weevils are a common beetle', 'can easily increase again.'),
               _C(3, 'Adapted from rhs.org.uk')]
Q12_GRAPH = _C(3, 'The graph shows the relationship', 'shrew populations.')
Q12_POLLUTION = _C(3, 'Pollution is a problem associated')
Q13_B = _C(4, 'Red-green colour blindness is an inherited', 'allele (N).')
Q13_C = _C(4, 'The theory of evolution by natural selection', 'population.')
Q14_A = _C(5, 'Flowering plants can be described', '(dicot).')
Q14_B = _C(5, 'Sexual reproduction in flowering plants', 'before germination.')
Q14_SEED = _C(5, 'The image shows a seed shortly')
Q14_C = _C(5, 'The diagram shows a xylem vessel', 'stem of a plant.')
Q14_CT = _C(5, 'The cohesion-tension model explains', 'transported in xylem.')
Q15_FEM = _C(6, 'Answer the following questions in relation to the female')
Q15_EMB = _C(6, 'The diagram (not drawn to scale) shows the early', 'after fertilisation.')
Q16_A = _C(7, 'Study the diagrams below')
Q16_A_TERMS = _C(7, 'Using diagrams A and B as an aid', 'following terms:')
Q16_B = _C(7, 'Viruses can have a variety of shapes', 'classifying viruses as living.')
Q16_C = _C(8, 'The diagram (not drawn to scale) shows a', 'placed in solution B.')
Q16_OSM = _C(8, 'Osmosis is a special type of diffusion', 'named above.')
Q16_D = _C(8, 'The diagram shows a yeast cell undergoing', 'reproduction.')
Q17_A = _C(9, 'The diagram shows a capillary network', 'connects to an artery.')
Q17_TERMS = _C(9, 'Explain the following terms:')
Q17_FACTORS = _C(9, 'Describe the effects of the following factors', 'circulatory system:')
Q17_B = _C(9, 'The diagram shows the basic structure of the skin.')
Q17_COPY = _C(9, 'Copy the diagram into your', 'correct locations.')
Q17_C = _C(10, 'The urinary system functions in excretion.')
Q17_URINARY = _C(10, 'Draw a large diagram of the human urinary system', 'Urethra.')
Q17_NEPHRON = _C(10, 'The diagram on the right shows the functional', 'of the kidney.')
Q17_D = _C(10, 'The human nervous system can be divided', 'section through the spinal cord.')
Q17_NEURON = _C(10, 'Draw a large diagram of a neuron.')

FIRST_NAME = S('(first correct name = 2 marks)')
GATE_NOTE = ('Asterisked in the scheme: only this exact term scores, and a wrong extra '
             'answer given alongside it cancels it.')

TASKS = [
    # ------------------------------------------------------------ Section A --
    T('1a', 'Q1(a)', 'A', _A(3, 'State two reasons', 'require food.'),
      [anyn(S('For energy', 'for repair'), 2, 2)], 'bio-1-2', 'why-organisms-need-food',
      SQ(8, 'State two reasons'), 4),
    T('1b', 'Q1(b)', 'A', _A(3, 'Name the chemical elements', 'all lipids.'),
      [pt(S('Carbon (C) and Hydrogen'), 4, kind='allOf')], 'bio-1-2', 'elements-in-lipids',
      SQ(8, 'Name the chemical elements'), 4,
      decision='One 4-mark line naming all three elements: carded as one all-of row.'),
    T('1c', 'Q1(c)', 'A', _A(3, 'Name the basic unit of a lipid.'),
      [pt(S('Triglyceride'), 4)], 'bio-1-2', 'basic-unit-of-a-lipid',
      SQ(8, 'Name the basic unit'), 4),
    T('1d', 'Q1(d)', 'A', _A(3, 'State one metabolic role'),
      [pt(S('Provide energy'), 4)], 'bio-1-2', 'metabolic-role-of-lipids',
      SQ(8, 'State one metabolic role'), 4),
    T('1e', 'Q1(e)', 'A', _A(3, 'Identify one vitamin'),
      [pt(S('A or D or E or K'), 4)], 'bio-1-2', 'fat-soluble-vitamins',
      SQ(8, 'Identify one vitamin'), 4),
    T('1f', 'Q1(f)', 'A', _A(3, 'State one deficiency disorder', 'named vitamin.'),
      [pt(S('Any correct vitamin deficiency'), 4, kind='criterion')], 'bio-1-2',
      'vitamin-deficiency-disorders', SQ(8, 'State one deficiency disorder'), 4,
      stem=[M('(e)', 3), _A(3, 'Identify one vitamin')],
      decision='Depends on (e): the stem carries the printed (e) ask. The scheme prices a '
               'judgement, so the row is a criterion.'),
    T('2a', 'Q2(a)', 'A', _A(4, 'In the box above, name a structure', 'named structure.'),
      [pt(S('Nucleus and arrow to nucleus'), 2)], 'bio-1-3', 'eukaryotic-cell-evidence',
      SQ(8, 'Name a structure visible'), 2, stem=[_A(4, 'Human cheek cells are shown')],
      fig='q2-cheek-cells'),
    T('2b', 'Q2(b)', 'A', _A(4, 'What term describes cells that are not'),
      [pt(S('Prokaryotic'), 3)], 'bio-1-3', 'prokaryotic-cells', SQ(8, 'What term describes'), 3),
    T('2c', 'Q2(c)', 'A', _A(4, 'Explain the term tissue culture.'),
      [pt(S('Growth of cells outside'), 3)], 'bio-1-3', 'tissue-culture',
      SQ(8, 'Explain the term tissue culture'), 3,
      stem=[_A(4, 'Human cells are used in tissue culture.')]),
    T('2d', 'Q2(d)', 'A', _A(4, 'State two conditions necessary'),
      [anyn(S('Sterility', 'other correct'), 2, 3)], 'bio-1-3', 'tissue-culture-conditions',
      SQ(8, 'State two conditions'), 6),
    T('2e', 'Q2(e)', 'A', _A(4, 'State two applications'),
      [anyn(S('Cancer research', 'other correct'), 2, 3)], 'bio-1-3', 'tissue-culture-uses',
      SQ(8, 'State two applications'), 6),
    T('3a', 'Q3(a)', 'A', _A(5, 'Name the body cavity'),
      [pt(S('Thoracic or chest'), 3)], 'bio-2-6', 'thoracic-cavity',
      SQ(9, 'Name the body cavity'), 3),
    T('3b', 'Q3(b)', 'A', _A(5, 'State the function of the epiglottis.'),
      [pt(S('Prevent food entering'), 3)], 'bio-2-6', 'epiglottis-function',
      SQ(9, 'State the function of the epiglottis'), 3),
    T('3c', 'Q3(c)', 'A', _A(5, 'What is the function of these rings'),
      [pt(S('To keep (the trachea) open'), 3)], 'bio-2-6', 'tracheal-cartilage-rings',
      SQ(9, 'What is the function of these rings'), 3,
      stem=[_A(5, 'The trachea has rings')]),
    T('3di', 'Q3(d)(i)', 'A', _A(5, 'Sketch and label the diaphragm'),
      [pt(S('Diaphragm muscle drawn'), 3, kind='criterion')], 'bio-2-6', 'diaphragm-position',
      SQ(9, 'Sketch and label the diaphragm'), 3,
      stem=[_A(5, 'The diagram shows parts of the human'), _A(5, 'On the diagram above,')],
      fig='q3-breathing-system'),
    T('3dii', 'Q3(d)(ii)', 'A', _A(5, 'Draw an arrow to show the direction', 'inhalation.'),
      [pt(S('Down arrow'), 2)], 'bio-2-6', 'diaphragm-in-inhalation',
      SQ(9, 'Draw an arrow to show'), 2,
      stem=[_A(5, 'The diagram shows parts of the human'), _A(5, 'On the diagram above,')],
      fig='q3-breathing-system'),
    T('3e', 'Q3(e)', 'A', _A(5, 'Name one other muscle'),
      [pt(S('Intercostal (muscle)'), 3)], 'bio-2-6', 'muscles-of-inhalation',
      SQ(9, 'Name one other muscle'), 3),
    T('3f', 'Q3(f)', 'A', _A(5, 'Briefly describe what happens'),
      [pt(S('Moves up and out'), 3)], 'bio-2-6', 'rib-cage-in-inhalation',
      SQ(9, 'Briefly describe'), 3, stem=[_A(5, 'The ribs are not shown')],
      fig='q3-breathing-system'),
    T('4a', 'Q4(a)', 'A', _A(6, 'Name the openings P', 'exchange to occur.'),
      [pt(S('Stomata'), 3)], 'bio-2-6', 'stomata',
      SQ(10, 'Name the openings P'), 3,
      stem=[_A(6, 'The image shows the undersurface', 'light microscope.')],
      fig='q4-leaf-surface'),
    T('4b', 'Q4(b)', 'A', _A(6, 'The size of these openings', 'Identify gas X.'),
      [pt(S('Carbon dioxide'), 3)], 'bio-2-6', 'carbon-dioxide-and-stomata',
      SQ(10, 'Identify gas X.'), 3),
    T('4c', 'Q4(c)', 'A', _A(6, 'State the relationship between'),
      [pt(S('As X increases'), 3)], 'bio-2-6', 'carbon-dioxide-and-stomatal-size',
      SQ(10, 'State the relationship'), 3,
      stem=[_A(6, 'The graphs (1. and 2.)', 'period of time.')], fig='q4-graphs'),
    T('4d', 'Q4(d)', 'A', _A(6, 'On graph 2., continue the curve', 'leaf reduced.'),
      [pt(S('On graph 2., continue the curve', 'leaf reduced.', after='(d)'), 2, kind='criterion',
          note='The scheme answers this part with a drawing, shown after reveal: graph 2 with '
               'the curve continued so that it levels off and then rises again.')],
      'bio-2-6', 'stomata-reopen-as-carbon-dioxide-falls', SQ(10, 'On graph 2., continue'), 2,
      stem=[_A(6, 'The graphs (1. and 2.)', 'period of time.')], fig='q4d-scheme-graph',
      source_pages=[6],
      decision='The scheme prints no words for (d), only the continued curve. The row quotes '
               'the scheme\'s own priced line; the scheme drawing is the solution figure and '
               'the question page (graph 2) opens from the card before reveal.'),
    T('4ei', 'Q4(e)(i)', 'A', _A(6, 'The label Q in the image above', 'these cells belong?'),
      [pt(S('Dermal'), 3)], 'bio-2-6', 'leaf-dermal-tissue',
      SQ(10, 'To which tissue type'), 3,
      stem=[_A(6, 'The image shows the undersurface', 'light microscope.')],
      fig='q4-leaf-surface'),
    T('4eii', 'Q4(e)(ii)', 'A', _A(6, 'Other than gas exchange, state one function', '(e) (i) above.'),
      [pt(S('Protection'), 3)], 'bio-2-6', 'dermal-tissue-function',
      SQ(10, 'Other than gas exchange'), 3,
      stem=[M('(e)', 6), M('(i)', 6), _A(6, 'The label Q in the image above', 'these cells belong?')],
      fig='q4-leaf-surface'),
    T('4f', 'Q4(f)', 'A', _A(6, 'Name the openings in the stems'),
      [pt(S('Lenticels'), 3)], 'bio-2-6', 'lenticels',
      SQ(10, 'Name the openings in the stems'), 3),
    T('5a', 'Q5(a)', 'A', _A(7, 'The first stage in protein synthesis', 'describe this stage?'),
      [pt(S('Transcription'), 3)], 'bio-2-3', 'transcription',
      SQ(11, 'The first stage in protein synthesis'), 3,
      stem=[_A(7, 'Answer the following questions in relation to protein')]),
    T('5b', 'Q5(b)', 'A', _A(7, 'Where in the cell does the stage'),
      [pt(S('Nucleus'), 3)], 'bio-2-3', 'where-transcription-occurs',
      SQ(11, 'Where in the cell'), 3,
      stem=[M('(a)', 7), _A(7, 'The first stage in protein synthesis', 'describe this stage?')]),
    T('5c', 'Q5(c)', 'A', _A(7, 'Name structure A', 'occurs in the cell.'),
      [pt(S('Ribosome'), 3)], 'bio-2-3', 'ribosome-and-translation',
      SQ(11, 'Name structure A'), 3,
      stem=[_A(7, 'The diagram below shows the second stage')], fig='q5-translation',
      labels=[L('A', S('Ribosome', page=11), True), L('B', S('Transfer or t', page=11), False)]),
    T('5d', 'Q5(d)', 'A', _A(7, 'The part labelled B', 'type of RNA.'),
      [pt(S('Transfer or t'), 3)], 'bio-2-3', 'transfer-rna',
      SQ(11, 'The part labelled B'), 3,
      stem=[_A(7, 'The diagram below shows the second stage')], fig='q5-translation',
      labels=[L('A', S('Ribosome', page=11), False), L('B', S('Transfer or t', page=11), True)]),
    T('5e', 'Q5(e)', 'A', _A(7, 'Part B attaches', 'sequences of mRNA?'),
      [pt(S('Codon or triplet'), 3)], 'bio-2-3', 'codons',
      SQ(11, 'Part B attaches'), 3,
      stem=[_A(7, 'The diagram below shows the second stage')], fig='q5-translation',
      notes='The paper prints "(such as G A G or C U G)"; the scheme reprint reads '
            '"G A G or G U C". The card uses the paper.'),
    T('5f', 'Q5(f)', 'A', _A(7, 'Part of the mRNA sequence above', 'this mRNA sequence.'),
      [pt(S('G A T'), 3)], 'bio-2-3', 'dna-sequence-from-mrna',
      SQ(11, 'Part of the mRNA sequence'), 3, fig='q5-translation'),
    T('5g', 'Q5(g)', 'A', _A(7, 'What happens to the fully translated', 'functional protein?'),
      [pt(S('It folds'), 2)], 'bio-2-3', 'protein-folding',
      SQ(11, 'What happens to the fully translated'), 2),
    T('6a', 'Q6(a)', 'A', _A(8, 'Complete the cycle by drawing', 'box provided.'),
      [pt(S('Denitrification'), 2),
       pt(S('Arrow from nitrate', 'arrow from molecule Y to nitrogen gas'), 2)],
      'bio-3-2', 'denitrification', SQ(12, 'Complete the cycle'), 4,
      stem=[_A(8, 'Answer the following questions in relation to the nitrogen'),
            _A(8, 'The diagram below shows the nitrogen cycle.', 'has been omitted.')],
      fig='q6-nitrogen-cycle'),
    T('6b', 'Q6(b)', 'A', _A(8, 'Write down the names of processes'),
      [pt(S('Nitrogen fixation'), 2, label=S('A:')),
       pt(S('Assimilation or nutrition'), 2, label=S('B:')),
       pt(S('Nitrification'), 2, label=S('C:'))],
      'bio-3-2', 'nitrogen-cycle-processes', SQ(12, 'Write down the names'), 6,
      stem=[Q6_STEM], fig='q6-nitrogen-cycle'),
    T('6ci', 'Q6(c)(i)', 'A', _A(8, 'Outline one way in which process A'),
      [pt(S('Action of (nitrogen fixing)'), 3)], 'bio-3-2', 'how-nitrogen-is-fixed',
      SQ(12, 'Outline one way in which process A'), 3, stem=[Q6_STEM], fig='q6-nitrogen-cycle'),
    T('6cii', 'Q6(c)(ii)', 'A', _A(8, 'Suggest an advantage to plants'),
      [pt(S('Make nitrogen easier'), 3)], 'bio-3-2', 'advantage-of-nitrogen-fixation',
      SQ(12, 'Suggest an advantage to plants'), 3, stem=[Q6_STEM], fig='q6-nitrogen-cycle'),
    T('6d', 'Q6(d)', 'A', _A(8, 'Name molecules X and Y.'),
      [pt(S('Ammonium or ammonia'), 2, label=S('X:')), pt(S('Nitrite'), 2, label=S('Y:'))],
      'bio-3-2', 'nitrogen-cycle-molecules', SQ(12, 'Name molecule X and Y.'), 4,
      stem=[Q6_STEM], fig='q6-nitrogen-cycle'),
] + [
    T(f'7{x}', f'Q7({x})', 'A',
      [_A(9, 'For each of the following structures', 'main function.'), _A(9, f'({x})'),
       _A(9, name)],
      [pt(S(loc, loc_end), 2, label=S('Precise location:')),
       pt(S(fn, fn_end), 2, label=S('Main function:'))],
      topic, concept, SQ(13, name), 4)
    for x, name, loc, loc_end, fn, fn_end, topic, concept in [
        ('a', 'Retina', 'At the back of the eye', None, 'Converts light', None,
         'bio-2-4', 'retina'),
        ('b', 'Sino-atrial node', 'Wall of the right atrium', None, 'Sends impulse to the atria',
         'or pacemaker', 'bio-2-6', 'sino-atrial-node'),
        ('c', 'Gall bladder', 'Underneath liver', None, 'Storage of bile', None,
         'bio-2-6', 'gall-bladder'),
        ('d', 'Adrenal gland', 'On top of the kidneys', None, 'Produce adrenaline', None,
         'bio-2-4', 'adrenal-gland'),
        ('e', 'Cerebellum', 'Back of the brain', None, 'Coordination (control)', 'speech',
         'bio-2-4', 'cerebellum'),
    ]
] + [
    # ------------------------------------------------------------ Section B --
    T('8a', 'Q8(a)', 'B', _A(10, 'In relation to scientific investigations', 'on each.'),
      [pt(S('Qualitative:', 'not numerical'), 3), pt(S('Quantitative:', 'data that is numerical'), 3)],
      'bio-u2', 'qualitative-and-quantitative', SQ(14, 'In relation to scientific'), 6),
    T('8bi', 'Q8(b)(i)', 'B', _A(10, 'Outline a qualitative test'),
      [pt(S('Add Benedict'), 3), pt(S('A (brick) red'), 3)], 'bio-1-2', 'test-for-reducing-sugar',
      SQ(14, 'Outline a qualitative test'), 6,
      stem=[_A(10, 'You carried out various investigations')]),
    T('8bii', 'Q8(b)(ii)', 'B', _A(10, 'Describe how you prepared a sample', 'microscope.'),
      [pt(S('Cut (or peel)'), 3), pt(S('Place sample on a'), 3), pt(S('Add a named stain'), 3),
       pt(S('Add a coverslip', 'stage'), 3)],
      'bio-1-3', 'preparing-stained-plant-cells', SQ(14, 'Describe how you prepared a sample'), 12,
      stem=[_A(10, 'You carried out various investigations')]),
    T('8biii1', 'Q8(b)(iii)1', 'B', _A(10, '1. Washing up liquid'),
      [pt(S('To break the membranes'), 3)], 'bio-1-2', 'dna-isolation-detergent',
      SQ(14, '1. Washing up liquid'), 3,
      stem=[_A(10, 'You carried out various investigations'),
            _A(10, 'When isolating DNA', 'the following:')]),
    T('8biii2', 'Q8(b)(iii)2', 'B', _A(10, '2. Ice cold ethanol'),
      [pt(S('To precipitate the DNA'), 3)], 'bio-1-2', 'dna-isolation-ethanol',
      SQ(14, '2. Ice cold ethanol'), 3,
      stem=[_A(10, 'You carried out various investigations'),
            _A(10, 'When isolating DNA', 'the following:')]),
    T('9ai', 'Q9(a)(i)', 'B', _A(11, 'What is an enzyme?'),
      [pt(S('A biological catalyst'), 3)], 'bio-2-1', 'what-is-an-enzyme',
      SQ(15, 'What is an enzyme?'), 3),
    T('9aii', 'Q9(a)(ii)', 'B', _A(11, 'What happens to an enzyme when'),
      [pt(S('Loses its shape'), 3)], 'bio-2-1', 'enzyme-denaturation',
      SQ(15, 'What happens to an enzyme'), 3),
    T('9b', 'Q9(b)', 'B', _A(11, 'During your practical studies', 'if you wish.'),
      [anyn(None, 8, 3, options=[
          S('Preparation of enzyme'), S('Name of enzyme and named'), S('Addition of different pH'),
          S('Fair test described'), S('How rate of reaction was measured', 'or source)'),
          S('Named piece of apparatus'), S('Results described', 'or source)'),
          S('Safety precaution described')], note_sel=S('Points may be obtained'))],
      'bio-2-1', 'effect-of-ph-on-enzyme-activity', SQ(15, 'During your practical studies'), 24,
      decision='Eight compulsory 3-mark points, grouped as one all-of-eight menu so the card '
               'carries the full 24 within the five-row cap (AGENTS.md: compact, never re-tariff).'),
    T('10ai', 'Q10(a)(i)', 'B', _A(12, 'In Biology, what is meant by the term geotropism?'),
      [pt(S('Growth response of a plant'), 3)], 'bio-2-4', 'geotropism',
      SQ(16, 'In Biology, what is meant'), 3),
    T('10aii', 'Q10(a)(ii)', 'B', _A(12, 'State one location in plants'),
      [pt(S('Meristem or named'), 3)], 'bio-2-4', 'where-growth-regulators-are-made',
      SQ(16, 'State one location in plants'), 3),
    T('10bi', 'Q10(b)(i)', 'B', _A(12, 'Describe how you set up this investigation.', 'if you wish.'),
      [anyn(None, 7, 3, options=[
          S('Seeds or named tissue'), S('Addition of different concentrations'),
          S('Control named and described'), S('Stored at a suitable temperature'),
          S('(Another) fair test described'), S('Left for a suitable length'),
          S('Safety precaution described')], note_sel=S('Points may be obtained'))],
      'bio-2-4', 'effect-of-iaa-on-plant-tissue',
      SQ(16, 'Describe how you set up this investigation.'), 21,
      stem=[_A(12, 'During your practical studies, you investigated the effect of IAA',
               'plant tissue.')],
      decision='Seven compulsory 3-mark points grouped as one all-of-seven menu.'),
    T('10bii', 'Q10(b)(ii)', 'B', _A(12, 'State one result of your investigation.'),
      [pt(S('Root growth best', 'very high concentrations'), 3)], 'bio-2-4', 'iaa-investigation-result',
      SQ(16, 'State one result'), 3,
      stem=[_A(12, 'During your practical studies, you investigated the effect of IAA',
               'plant tissue.')]),
    # ------------------------------------------------------------ Section C --
    T('11ai', 'Q11(a)(i)', 'C', _C(2, 'What is meant by the term metabolism?'),
      [pt(S('(All) the chemical reactions'), 3)], 'bio-2-2', 'metabolism',
      SQ(17, 'What is meant by the term metabolism?'), 3, stem=[_C(2, 'The molecule ATP plays')]),
    T('11aii', 'Q11(a)(ii)', 'C', _C(2, 'What do the letters ATP stand for?'),
      [pt(S('Adenosine triphosphate'), 3)], 'bio-2-2', 'atp-name',
      SQ(17, 'What do the letters ATP'), 3, stem=[_C(2, 'The molecule ATP plays')]),
    T('11aiii', 'Q11(a)(iii)', 'C', _C(2, 'What is the role of ATP in metabolism?'),
      [pt(S('To carry energy'), 3)], 'bio-2-2', 'role-of-atp',
      SQ(17, 'What is the role of ATP'), 3, stem=[_C(2, 'The molecule ATP plays')]),
    T('11bi', 'Q11(b)(i)', 'C', _C(2, 'What name is given to the first stage'),
      [pt(S('Glycolysis'), 3)], 'bio-2-2', 'glycolysis',
      SQ(17, 'What name is given to the first stage'), 3,
      stem=[_C(2, 'Answer the following questions in relation to aerobic')]),
    T('11bii', 'Q11(b)(ii)', 'C', _C(2, 'Describe the events of the first stage'),
      [pt(S('Glucose converted to pyruvate'), 3), pt(S('ATP produced (or released)', 'protons (H+)'), 3)],
      'bio-2-2', 'events-of-glycolysis', SQ(17, 'Describe the events of the first stage'), 6,
      stem=[_C(2, 'Answer the following questions in relation to aerobic')]),
    T('11biii1', 'Q11(b)(iii)1', 'C', _C(2, 'What small gaseous molecule', 'respiration to occur?'),
      [pt(S('Oxygen'), 3)], 'bio-2-2', 'oxygen-and-stage-two',
      SQ(17, 'What small gaseous molecule'), 3,
      stem=[_C(2, 'Answer the following questions in relation to aerobic')]),
    T('11biii2', 'Q11(b)(iii)2', 'C', _C(2, 'Where in the cell does the second stage'),
      [pt(S('Mitochondrion'), 3)], 'bio-2-2', 'site-of-stage-two',
      SQ(17, '2. Where in the cell'), 3,
      stem=[_C(2, 'Answer the following questions in relation to aerobic')]),
    T('11biii3', 'Q11(b)(iii)3', 'C', _C(2, 'Describe the events of the second stage'),
      [anyn(S('Pyruvate (pyruvic acid) to acetyl', 'combine with oxygen to form water'), 4, 3)],
      'bio-2-2', 'krebs-cycle-and-electron-transport', SQ(17, '3. Describe the events'), 12,
      stem=[_C(2, 'Answer the following questions in relation to aerobic')]),
    T('11ci', 'Q11(c)(i)', 'C', _C(2, 'Why is this stage called'),
      [pt(S('Uses (or requires) light'), 3)], 'bio-2-2', 'light-dependent-stage',
      SQ(18, 'Why is this stage called'), 3,
      stem=[_C(2, 'The light-dependent stage of photosynthesis', 'pathways (1 and 2).')]),
    T('11cii1', 'Q11(c)(ii)1', 'C', _C(2, 'Name the molecule that releases'),
      [pt(S('Chlorophyll'), 3)], 'bio-2-2', 'chlorophyll-releases-electrons',
      SQ(18, 'Name the molecule that releases'), 3,
      stem=[_C(2, 'The light-dependent stage of photosynthesis', 'pathways (1 and 2).'),
            _C(2, 'In pathway 1, energised electrons', 'electron acceptors.')]),
    T('11cii2', 'Q11(c)(ii)2', 'C', _C(2, 'At the end of this pathway'),
      [pt(S('Return to chlorophyll'), 3)], 'bio-2-2', 'cyclic-electron-flow',
      SQ(18, 'At the end of this pathway'), 3,
      stem=[_C(2, 'The light-dependent stage of photosynthesis', 'pathways (1 and 2).'),
            _C(2, 'In pathway 1, energised electrons', 'electron acceptors.')]),
    T('11ciii1', 'Q11(c)(iii)1', 'C', _C(2, 'What name is given to this splitting'),
      [pt(S('Photolysis'), 3)], 'bio-2-2', 'photolysis',
      SQ(18, 'What name is given to this splitting'), 3,
      stem=[_C(2, 'The light-dependent stage of photosynthesis', 'pathways (1 and 2).'),
            _C(2, 'Water is split during pathway 2.')]),
    T('11ciii2', 'Q11(c)(iii)2', 'C', _C(2, 'Name the cell organelle where water'),
      [pt(S('Chloroplast'), 3)], 'bio-2-2', 'where-water-is-split',
      SQ(18, 'Name the cell organelle where water'), 3,
      stem=[_C(2, 'The light-dependent stage of photosynthesis', 'pathways (1 and 2).'),
            _C(2, 'Water is split during pathway 2.')]),
    T('11civ', 'Q11(c)(iv)', 'C', _C(2, 'Protons (H+ ions) are released', 'carbohydrate production.'),
      [anyn(S('Form a (proton) pool', 'reduce CO2 (to glucose)'), 2, 3)], 'bio-2-2',
      'fate-of-protons', SQ(18, 'Describe what happens to these protons'), 6,
      stem=[_C(2, 'The light-dependent stage of photosynthesis', 'pathways (1 and 2).')]),
    T('11cv', 'Q11(c)(v)', 'C', _C(2, 'State one method that horticulturists', 'greenhouses.'),
      [pt(S('Increase carbon dioxide'), 3)], 'bio-2-2', 'greenhouse-crop-growth',
      SQ(18, 'State one method that horticulturists'), 3),
    T('12ai', 'Q12(a)(i)', 'C', _C(3, 'In ecology, what is meant by the term competition?'),
      [pt(S('Struggle between organisms'), 3)], 'bio-3-1', 'competition',
      SQ(19, 'In ecology, what is meant'), 3),
    T('12aii', 'Q12(a)(ii)', 'C', _C(3, 'Name and describe one type of competition'),
      [pt(S('Contest or scramble'), 3, label=S('Name:')),
       pt(S('Description: Matching description'), 3, kind='criterion')],
      'bio-3-1', 'types-of-competition', SQ(19, 'Name and describe one type'), 6),
    T('12bi', 'Q12(b)(i)', 'C', _C(3, 'Identify one behavioural adaptation'),
      [pt(S('Correct behavioural adaptation'), 3, kind='criterion')], 'bio-3-1',
      'behavioural-adaptation', SQ(19, 'Identify one behavioural adaptation'), 3, stem=Q12_PASSAGE),
    T('12bii', 'Q12(b)(ii)', 'C', _C(3, 'From the passage or otherwise', 'weevil.'),
      [pt(S('Valid explanation of benefit'), 3, kind='criterion')], 'bio-3-1',
      'benefit-of-an-adaptation', SQ(19, 'Explain how this adaptation'), 3,
      stem=Q12_PASSAGE + [M('(i)', 3), _C(3, 'Identify one behavioural adaptation')]),
    T('12biii', 'Q12(b)(iii)', 'C', _C(3, 'Suggest a reason why the vine weevil'),
      [pt(S('Not all are killed', 'suggestion'), 3)], 'bio-3-1', 'population-recovery',
      SQ(19, 'Suggest a reason why the vine weevil'), 3, stem=Q12_PASSAGE),
    T('12biv', 'Q12(b)(iv)', 'C', _C(3, 'Using organisms named in the passage', 'trophic levels.'),
      [pt(S('Correct food chain'), 3, kind='criterion')], 'bio-3-1', 'food-chain',
      SQ(19, 'Using organisms named'), 3, stem=Q12_PASSAGE),
    T('12bv', 'Q12(b)(v)', 'C', _C(3, 'Construct a pyramid of numbers'),
      [pt(S('Matching pyramid'), 3, kind='criterion')], 'bio-3-1', 'pyramid-of-numbers',
      SQ(19, 'Construct a pyramid'), 3,
      stem=Q12_PASSAGE + [M('(iv)', 3), _C(3, 'Using organisms named in the passage', 'trophic levels.')]),
    T('12bvi', 'Q12(b)(vi)', 'C', _C(3, 'Which line, A or B', 'Explain your answer.'),
      [pt(S('A'), 2), pt(S('higher peaks', '(population)'), 1, label=S('Explain:'))],
      'bio-3-1', 'predator-prey-graph', SQ(19, 'Which line, A or B'), 3,
      stem=[Q12_GRAPH], fig='q12-population-graph'),
    T('12bvii', 'Q12(b)(vii)', 'C', _C(3, 'Suggest a reason for the population', 'different times.'),
      [pt(S('Takes time for reproduction'), 3)], 'bio-3-1', 'predator-prey-time-lag',
      SQ(19, 'Suggest a reason for the population'), 3, stem=[Q12_GRAPH],
      fig='q12-population-graph'),
    T('12bviii', 'Q12(b)(viii)', 'C', _C(3, 'Other than predation and competition', 'numbers.'),
      [pt(S('Parasitism'), 3), pt(S('Symbiosis'), 3)], 'bio-3-1', 'factors-controlling-populations',
      SQ(19, 'Other than predation'), 6),
    T('12ci', 'Q12(c)(i)', 'C', _C(3, 'In terms of ecology, explain the term conservation.'),
      [pt(S('Management of organisms'), 3)], 'bio-3-1', 'conservation',
      SQ(20, 'In ecology, explain the term conservation'), 3),
] + [
    T('12cii', 'Q12(c)(ii)', 'C', _C(3, 'Outline one conservation practice', 'your answer refers.'),
      [pt(S('Outline of named conservation'), 3, kind='criterion'),
       pt(S('Matching benefit outlined'), 3, kind='criterion')],
      'bio-3-1', f'conservation-practice-{area}', SQ(20, 'Outline one conservation practice'), 6,
      route=area,
      decision='Closed choose-one pool of three printed areas: one card per area at the '
               'route tariff of 6.')
    for area in ROUTES['Q12(c)(ii)']
] + [
    T('12ciii', 'Q12(c)(iii)', 'C', _C(3, 'State one example of waste management', 'your answer refers.'),
      [pt(S('Correct example given'), 3, kind='criterion')], 'bio-3-1',
      f'waste-management-{area}', SQ(20, 'State one example of waste'), 3, route=area,
      decision='Closed choose-one pool of three printed areas: one card per area at the '
               'route tariff of 3.')
    for area in ROUTES['Q12(c)(iii)']
] + [
    T('12civ', 'Q12(c)(iv)', 'C', _C(3, 'Explain the term pollution.'),
      [pt(S('A harmful addition'), 3)], 'bio-3-1', 'pollution',
      SQ(20, 'Explain the term pollution.'), 3, stem=[Q12_POLLUTION]),
    T('12cv', 'Q12(c)(v)', 'C', _C(3, 'Name any one pollutant'),
      [pt(S('Named pollutant'), 3, kind='criterion'),
       pt(S('Effect of named pollutant'), 3, kind='criterion')],
      'bio-3-1', 'pollutant-and-effect', SQ(20, 'Name any one pollutant'), 6, stem=[Q12_POLLUTION]),
    T('12cvi', 'Q12(c)(vi)', 'C', _C(3, 'State one problem associated with waste'),
      [pt(S('Unsightly or smell', 'problem stated'), 3)], 'bio-3-1', 'waste-disposal-problems',
      SQ(20, 'State one problem associated'), 3, stem=[Q12_POLLUTION]),
    T('13a', 'Q13(a)', 'C', _C(4, 'Draw a labelled diagram of one nucleotide'),
      [pt(S('Diagram: Three shapes connected'), 3, kind='criterion'),
       pt(S('Angle'), 3, kind='criterion',
          note='The scheme\'s model drawing is shown after reveal; this mark is for the angle '
               'at which the parts are joined, as drawn there.'),
       anyn(None, 3, 1, options=[S('Phosphate'), S('Deoxyribose'), S('(Nitrogenous)', 'base')])],
      'bio-1-2', 'dna-nucleotide', SQ(21, 'Draw a labelled diagram of one nucleotide'), 9,
      stem=[_C(4, 'Deoxyribonucleic acid (DNA) is a polynucleotide.')],
      fig='q13a-scheme-nucleotide'),
    T('13bi', 'Q13(b)(i)', 'C', _C(4, 'Explain the underlined terms.'),
      [pt(S('Sex linked:', 'or on Y chromosome).'), 3), pt(S('Recessive:', 'dominant allele.'), 3)],
      'bio-1-4', 'sex-linkage-and-recessive-alleles', SQ(21, 'Explain the underlined terms'), 6,
      stem=[Q13_B], source_pages=[4],
      decision='The paper underlines the two terms. The lifted text cannot carry an '
               'underline, so the official question page opens from the card; a crop of '
               'the full-width paragraph was tried and is illegible at phone width.'),
    T('13bii', 'Q13(b)(ii)', 'C', _C(4, 'State the full genotype of a heterozygous'),
      [pt(S('XXNn'), 3, first_alt=True,
          note='The scheme accepts the same genotype in three other notations, shown after '
               'reveal: the alleles written as subscripts or as superscripts on each X.')],
      'bio-1-4', 'heterozygous-female-genotype', SQ(21, 'State the full genotype of a heterozygous'),
      3, stem=[Q13_B], fig='q13b-ii-scheme'),
    T('13biii', 'Q13(b)(iii)', 'C', _C(4, 'State the full genotype of a colour-blind male.'),
      [pt(S('XYn–'), 3, first_alt=True,
          note='The scheme accepts the same genotype in three other notations, shown after '
               'reveal: the allele written as a subscript or a superscript on the X.')],
      'bio-1-4', 'colour-blind-male-genotype', SQ(21, 'State the full genotype of a colour-blind'),
      3, stem=[Q13_B], fig='q13b-iii-scheme'),
    T('13biv', 'Q13(b)(iv)', 'C', _C(4, 'State all the genotypes and matching', '(iii) above.'),
      [anyn(None, 4, 2, options=[{'sel': S('XXNn'), 'first_alt': True},
                                 {'sel': S('XXnn'), 'first_alt': True},
                                 {'sel': S('XYN–'), 'first_alt': True},
                                 {'sel': S('XYn–'), 'first_alt': True}],
            note='Each genotype is also accepted in the subscript and superscript notations '
                 'shown in the scheme extract after reveal.'),
       anyn(None, 4, 1, options=[S('female normal (colour vision)'), S('female colour-blind'),
                                 S('male normal (colour vision)'), S('male colour-blind')],
            note_sel=S('Phenotype must match'))],
      'bio-1-4', 'sex-linked-cross', SQ(21, 'State all the genotypes'), 12,
      stem=[Q13_B, M('(ii)', 4), _C(4, 'State the full genotype of a heterozygous'),
            M('(iii)', 4), _C(4, 'State the full genotype of a colour-blind male.')],
      fig='q13b-iv-scheme',
      decision='Four genotypes at 2 and four phenotypes at 1, all asterisked: two all-of '
               'menus keep the 2/1 split within the row cap.'),
    T('13bv', 'Q13(b)(v)', 'C', _C(4, 'Explain why males are more likely'),
      [pt(S('Males only inherit'), 3)], 'bio-1-4', 'why-males-are-colour-blind',
      SQ(21, 'Explain why males'), 3, stem=[Q13_B]),
    T('13ci', 'Q13(c)(i)', 'C', _C(4, 'Explain the underlined terms.', nth=2),
      [pt(S('Evolution:', 'due to the environment.'), 3), pt(S('Variation:', 'same species.'), 3)],
      'bio-1-5', 'evolution-and-variation', SQ(22, 'Explain the underlined terms.'), 6,
      stem=[Q13_C], source_pages=[4],
      decision='The underlined terms are visible on the official question page, which opens '
               'from the card.'),
    T('13cii', 'Q13(c)(ii)', 'C', _C(4, 'Variation can be caused by mutations.', 'types of mutation.'),
      [pt(S('Chromosome'), 3), pt(S('Gene'), 3)], 'bio-2-3', 'types-of-mutation',
      SQ(22, 'Name two types of mutation.'), 6),
    T('13ciii', 'Q13(c)(iii)', 'C', _C(4, 'Name both of the naturalists'),
      [anyn(None, 2, 2, steps=[2, 1], options=[S('(Charles) Darwin'), S('(Alfred Russell-)Wallace')],
            note_sel=FIRST_NAME, note=GATE_NOTE)],
      'bio-1-5', 'darwin-and-wallace', SQ(22, 'Name both of the naturalists'), 3, stem=[Q13_C]),
    T('13civ', 'Q13(c)(iv)', 'C', _C(4, 'Suggest a benefit to species'),
      [pt(S('(There is a high death rate)'), 3)], 'bio-1-5', 'why-produce-many-offspring',
      SQ(22, 'Suggest a benefit'), 3, stem=[Q13_C]),
    T('13cv', 'Q13(c)(v)', 'C', _C(4, 'Explain how the accumulation of favourable', 'natural selection.'),
      [pt(S('Those organisms', 'or explained'), 3)], 'bio-1-5', 'favourable-traits',
      SQ(22, 'Explain how the accumulation'), 3, stem=[Q13_C]),
    T('13cvi', 'Q13(c)(vi)', 'C', _C(4, 'State one piece of evidence'),
      [pt(S('Fossils or comparative'), 3)], 'bio-1-5', 'evidence-for-natural-selection',
      SQ(22, 'State one piece of evidence'), 3),
    T('14ai', 'Q14(a)(i)', 'C', _C(5, 'What is a cotyledon?'),
      [pt(S('A seed leaf'), 3)], 'bio-2-5', 'cotyledon', SQ(23, 'What is a cotyledon?'), 3,
      stem=[Q14_A]),
    T('14aii', 'Q14(a)(ii)', 'C', _C(5, 'Other than the number of cotyledons', 'dicotyledonous plant.'),
      [anyn(None, 2, 3, options=[
          S('Vascular bundles are', 'ring (in stem)'), S('(Mostly) herbaceous', '(Mostly) woody'),
          S('Flower parts usually in', 'four or five'), S('(Mostly have) narrow leaves', 'broad leaves'),
          {'sel': S('(Mostly) have parallel leaf', 'venation'), 'end_nth': 2},
          S('Fibrous roots', 'Tap roots'), S('(Mostly) endospermic', 'non-endospermic')],
          note='Each option reads monocot first, then dicot, as the scheme\'s two columns do.')],
      'bio-2-6', 'monocots-and-dicots', SQ(23, 'Other than the number'), 6, stem=[Q14_A]),
    T('14bi', 'Q14(b)(i)', 'C', _C(5, 'Name the part of the flower that develops'),
      [pt(S('Ovule'), 3)], 'bio-2-5', 'ovule-becomes-seed', SQ(23, 'Name the part of the flower'), 3,
      stem=[Q14_B]),
    T('14bii', 'Q14(b)(ii)', 'C', _C(5, 'State any one method of seed dispersal.'),
      [pt(S('Wind or animal'), 3)], 'bio-2-5', 'seed-dispersal-methods',
      SQ(23, 'State any one method'), 3, stem=[Q14_B]),
    T('14biii', 'Q14(b)(iii)', 'C', _C(5, 'State one advantage to the plant of seed dispersal.'),
      [pt(S('Reduce competition'), 3)], 'bio-2-5', 'advantage-of-seed-dispersal',
      SQ(23, 'State one advantage to the plant of seed'), 3, stem=[Q14_B]),
    T('14biv', 'Q14(b)(iv)', 'C', _C(5, 'State one advantage to the plant of dormancy.'),
      [pt(S('Allows time for dispersal'), 3)], 'bio-2-5', 'advantage-of-dormancy',
      SQ(23, 'State one advantage to the plant of dormancy'), 3, stem=[Q14_B]),
    T('14bv1', 'Q14(b)(v)1', 'C', _C(5, 'What is meant by the term germination?'),
      [pt(S('The growth of a seed'), 3)], 'bio-2-5', 'germination',
      SQ(23, 'What is meant by the term germination?'), 3, stem=[Q14_SEED],
      fig='q14-germinating-seed'),
    T('14bv2', 'Q14(b)(v)2', 'C', _C(5, 'What name is given to the outer covering', 'labelled A?'),
      [pt(S('Testa'), 2)], 'bio-2-5', 'testa',
      SQ(23, 'What name is given to the outer covering'), 2, stem=[Q14_SEED],
      fig='q14-germinating-seed',
      labels=[L('A', S('Testa', page=23), True), L('B', S('Root or', page=23), False),
              L('C', S('Shoot or', page=23), False)]),
    T('14bv3', 'Q14(b)(v)3', 'C', _C(5, 'Name the parts labelled B and C.'),
      [pt(S('Root or'), 2, label=S('B:')), pt(S('Shoot or'), 2, label=S('C:'))],
      'bio-2-5', 'radicle-and-plumule', SQ(23, 'Name the parts labelled B and C.'), 4,
      stem=[Q14_SEED], fig='q14-germinating-seed',
      labels=[L('A', S('Testa', page=23), False), L('B', S('Root or', page=23), True),
              L('C', S('Shoot or', page=23), True)]),
    T('14bvi', 'Q14(b)(vi)', 'C', _C(5, 'Describe the role of water'),
      [pt(S('Soften or bursting', 'transports materials'), 3)], 'bio-2-5', 'water-in-germination',
      SQ(23, 'Describe the role of water'), 3,
      stem=[_C(5, 'Seeds require water, oxygen', 'germination to occur.')]),
    T('14bvii', 'Q14(b)(vii)', 'C', _C(5, 'Outline the role of a suitable temperature', 'germination.'),
      [pt(S('Allows for optimum'), 3)], 'bio-2-5', 'temperature-in-germination',
      SQ(23, 'Outline the role of a suitable temperature'), 3,
      stem=[_C(5, 'Seeds require water, oxygen', 'germination to occur.')]),
    T('14ci', 'Q14(c)(i)', 'C', _C(5, 'Name one other substance transported'),
      [pt(S('Minerals or named mineral'), 3)], 'bio-2-6', 'xylem-carries-minerals',
      SQ(24, 'Name one other substance'), 3, stem=[Q14_C], fig='q14-xylem-vessel'),
    T('14cii', 'Q14(c)(ii)', 'C', _C(5, 'Describe two structural features of xylem', 'efficiently.'),
      [anyn(S('Vessels are tubular', 'tapered ends'), 2, 3)], 'bio-2-6', 'xylem-structure',
      SQ(24, 'Describe two structural features'), 6, stem=[Q14_C], fig='q14-xylem-vessel'),
    T('14ciii1', 'Q14(c)(iii)1', 'C', _C(5, 'Name the two Irish scientists', 'model.'),
      [anyn(None, 2, 2, steps=[2, 1], options=[S('(Henry) Dixon'), S('(John) Joly')],
            note_sel=FIRST_NAME, note=GATE_NOTE)],
      'bio-2-6', 'dixon-and-joly', SQ(24, 'Name the two Irish scientists'), 3,
      stem=[Q14_C, Q14_CT], fig='q14-xylem-vessel'),
    T('14ciii2', 'Q14(c)(iii)2', 'C', _C(5, 'Describe the process of the cohesion-tension', 'in xylem.'),
      [pt(S('Water molecules are attracted together'), 3),
       pt(S('Water molecules are attracted to sides', 'walls of xylem'), 3),
       pt(S('Water evaporates at the leaves'), 3), pt(S('Water is pulled upwards'), 3)],
      'bio-2-6', 'cohesion-tension-model', SQ(24, 'Describe the process of the cohesion'), 12,
      stem=[Q14_C, Q14_CT], fig='q14-xylem-vessel'),
    T('15ai', 'Q15(a)(i)', 'C', _C(6, 'What is meant by the term contraception?'),
      [pt(S('Prevention of fertilisation'), 3)], 'bio-2-5', 'contraception',
      SQ(25, 'What is meant by the term contraception'), 3),
    T('15aii', 'Q15(a)(ii)', 'C', _C(6, 'State any three methods of contraception.'),
      [pt(S('Any three correct examples'), 6, kind='criterion', units=[2, 2, 2],
          note='Priced 3(2): two marks for each of three correct methods.')],
      'bio-2-5', 'methods-of-contraception', SQ(25, 'State any three methods'), 6),
    T('15bi', 'Q15(b)(i)', 'C', _C(6, 'Draw a large diagram of the human female', 'Vagina.'),
      [pt(S('Diagram: Ovary and Fallopian tube', 'correct locations'), 6, kind='criterion',
          units=[3, 3], note_sel=S('Any one missing = 3')),
       anyn(S('Ovary / Fallopian tube', 'Vagina'), 6, 1)],
      'bio-2-5', 'female-reproductive-system', SQ(25, 'Draw a large diagram of the human female'),
      12, stem=[Q15_FEM]),
    T('15bii', 'Q15(b)(ii)', 'C', _C(6, 'State any one role of oestrogen'),
      [pt(S('To build up (or repair)', 'LH production'), 3)], 'bio-2-5', 'role-of-oestrogen',
      SQ(25, 'State any one role of oestrogen'), 3,
      stem=[Q15_FEM, _C(6, 'The ovary produces oestrogen.')]),
    T('15biii', 'Q15(b)(iii)', 'C', _C(6, 'Name one other female sex hormone', 'precise function.'),
      [pt(S('Progesterone'), 3), pt(S('Maintains endometrium'), 3,
                                    note_sel=S('Name = 3; Precise function = 3'))],
      'bio-2-5', 'female-sex-hormones', SQ(25, 'Name one other female sex hormone'), 6,
      stem=[Q15_FEM],
      decision='Open choice of hormone; the scheme prints three name-and-function routes '
               '(progesterone, FSH, LH). Carded once with the three as answer variants, not '
               'as separate cards, because the paper prints no pool.'),
    T('15biv', 'Q15(b)(iv)', 'C', _C(6, 'State one cause of a named menstrual disorder.'),
      [pt(S('Correctly named menstrual disorder'), 3, kind='criterion'),
       pt(S('Matching cause'), 3, kind='criterion')],
      'bio-2-5', 'menstrual-disorder-cause', SQ(25, 'State one cause of a named'), 6, stem=[Q15_FEM]),
    T('15ci', 'Q15(c)(i)', 'C', _C(6, 'Identify structures A, B and C.'),
      [pt(S('Zygote'), 1, label=S('A:')), pt(S('Morula'), 1, label=S('B:')),
       pt(S('Blastocyst'), 1, label=S('C:'))],
      'bio-2-5', 'zygote-morula-blastocyst', SQ(26, 'Identify structures A, B and C.'), 3,
      stem=[Q15_EMB], fig='q15-embryo-stages',
      labels=[L('A', S('Zygote', page=26), True), L('B', S('Morula', page=26), True),
              L('C', S('Blastocyst', page=26), True)]),
    T('15cii', 'Q15(c)(ii)', 'C', _C(6, 'Where in the female reproductive system does structure B'),
      [pt(S('Fallopian tube (or'), 3)], 'bio-2-5', 'where-the-morula-forms',
      SQ(26, 'Where in the female reproductive tract'), 3, stem=[Q15_EMB], fig='q15-embryo-stages',
      notes='The paper says "reproductive system"; the scheme reprint says "reproductive tract".'),
    T('15ciii', 'Q15(c)(iii)', 'C', _C(6, 'What must happen to structure C'),
      [pt(S('Implantation or described'), 3)], 'bio-2-5', 'implantation',
      SQ(26, 'What must happen to structure C'), 3, stem=[Q15_EMB], fig='q15-embryo-stages'),
    T('15civ', 'Q15(c)(iv)', 'C', _C(6, 'Three germ layers form within', 'layer you named.'),
      [anyn(None, 3, 2, options=[S('Ectoderm'), S('Mesoderm'), S('Endoderm')]),
       anyn(None, 3, 1, options=[S('Matching structure: skin'), S('Matching structure: liver'),
                                 S('Matching structure: internal lining')],
            note='Listed in the same order as the layers: ectoderm, mesoderm, endoderm.')],
      'bio-2-5', 'germ-layers', SQ(26, 'Name the three germ layers'), 9, stem=[Q15_EMB],
      fig='q15-embryo-stages',
      decision='Three layers at 2 and a matching structure for each at 1: two all-of menus '
               'keep the 2/1 tariff within the row cap.'),
    T('15cv', 'Q15(c)(v)', 'C', _C(6, 'Infertility is the inability', 'for infertility.'),
      [anyn(S('In vitro fertilisation', 'other correct'), 2, 3)], 'bio-2-5', 'treating-infertility',
      SQ(26, 'State two possible corrective'), 6),
    T('16ai1', 'Q16(a)(i)1', 'C', [Q16_A_TERMS, _C(7, '1.'), _C(7, 'Mitosis')],
      [pt(S('One nucleus divides'), 3, note_sel=ERRATUM)], 'bio-2-3', 'mitosis',
      SQ(27, '1. Mitosis'), 3, stem=[Q16_A], fig='q16-cell-division',
      notes='Scheme erratum: full marks for (i) and (ii) to every candidate who attempted 16(a).'),
    T('16ai2', 'Q16(a)(i)2', 'C', [Q16_A_TERMS, _C(7, '2.'), _C(7, 'Meiosis')],
      [pt(S('One diploid (or 2n)', 'different) nuclei'), 3, note_sel=ERRATUM)], 'bio-2-3', 'meiosis',
      SQ(27, '2. Meiosis'), 3, stem=[Q16_A], fig='q16-cell-division'),
    T('16aii1', 'Q16(a)(ii)1', 'C', _C(7, 'State a role of mitosis'),
      [pt(S('Growth or repair'), 3, note_sel=ERRATUM)], 'bio-2-3', 'role-of-mitosis',
      SQ(27, '1. State a role of mitosis'), 3, stem=[Q16_A], fig='q16-cell-division'),
    T('16aii2', 'Q16(a)(ii)2', 'C', _C(7, 'State a role of meiosis'),
      [pt(S('(Allows for) sexual reproduction'), 3, note_sel=ERRATUM)], 'bio-2-3', 'role-of-meiosis',
      SQ(27, '2. State a role of meiosis'), 3, stem=[Q16_A], fig='q16-cell-division'),
    T('16aiii', 'Q16(a)(iii)', 'C', _C(7, 'Explain the terms haploid and diploid.'),
      [pt(S('Haploid: Having one copy'), 3), pt(S('Diploid:', '(in the nucleus).'), 3)],
      'bio-2-3', 'haploid-and-diploid', SQ(27, 'Explain the terms haploid'), 6),
    T('16aiv', 'Q16(a)(iv)', 'C', _C(7, 'Draw a diagram of a cell with a diploid number', 'only visible during mitosis.'),
      [pt(S('Diagram: Four pairs of chromosomes'), 3, kind='criterion'),
       pt(S('being pulled apart by spindle fibres'), 3, kind='criterion'),
       anyn(S('Spindle (fibres)', 'pole'), 3, 1)],
      'bio-2-3', 'anaphase-of-mitosis', SQ(27, 'Draw a diagram of a cell with a diploid'), 9),
    T('16av', 'Q16(a)(v)', 'C', _C(7, 'What term describes uncontrolled mitosis'),
      [pt(S('Cancer'), 3)], 'bio-2-3', 'cancer', SQ(27, 'What terms describes uncontrolled'), 3),
    T('16bi', 'Q16(b)(i)', 'C', _C(7, 'Name the types of biomolecules X and Y', 'of this virus.'),
      [anyn(None, 2, 2, steps=[2, 1], options=[S('X:'), S('Y:')], note_sel=FIRST_NAME,
            note=GATE_NOTE)],
      'bio-3-2', 'virus-biomolecules', SQ(28, 'Name the types of biomolecules'), 3,
      stem=[Q16_B], fig='q16-virus'),
    T('16bii', 'Q16(b)(ii)', 'C', _C(7, 'The virus in diagram 1 is a round-shaped', 'shape of a virus.'),
      [pt(S('Rod or complex'), 3)], 'bio-3-2', 'virus-shapes',
      SQ(28, 'State any other possible shape'), 3, stem=[Q16_B], fig='q16-virus'),
    T('16biii', 'Q16(b)(iii)', 'C', _C(7, 'Diagram 2 shows a virus attaching', 'large number of viruses.'),
      [anyn(S('DNA or RNA or nucleic acid enters', '(host) cell bursts'), 4, 3)], 'bio-3-2',
      'viral-replication', SQ(28, 'Describe how the virus uses'), 12, stem=[Q16_B],
      fig='q16-virus-host'),
    T('16biv', 'Q16(b)(iv)', 'C', _C(7, 'Suggest a reason why a red blood cell', 'host cell for viruses.'),
      [pt(S('(RBCs) do not contain'), 3)], 'bio-3-2', 'red-blood-cells-and-viruses',
      SQ(28, 'Suggest a reason why a red blood cell'), 3),
    T('16bv', 'Q16(b)(v)', 'C', _C(7, 'State two examples of harmful viruses.'),
      [pt(S('Any two harmful viruses'), 6, kind='criterion', units=[3, 3],
          note='Priced 2(3): three marks for each of two harmful viruses.')],
      'bio-3-2', 'harmful-viruses', SQ(28, 'State two examples of harmful'), 6),
    T('16bvi', 'Q16(b)(vi)', 'C', _C(7, 'State one example of the beneficial use'),
      [pt(S('Any one beneficial use'), 3, kind='criterion')], 'bio-3-2', 'beneficial-viruses',
      SQ(28, 'State one example of the beneficial'), 3),
    T('16ci', 'Q16(c)(i)', 'C', _C(8, 'What has happened to the cell in', 'solution A?'),
      [pt(S('Lost water (by osmosis)'), 3)], 'bio-2-6', 'plasmolysis',
      SQ(29, 'What has happened to the cell'), 3, stem=[Q16_C], fig='q16-plant-cells'),
    T('16cii', 'Q16(c)(ii)', 'C', _C(8, 'Name the condition that describes', 'solution B.'),
      [pt(S('Turgid'), 3)], 'bio-2-6', 'turgidity', SQ(29, 'Name the condition that describes'), 3,
      stem=[Q16_C], fig='q16-plant-cells'),
    T('16ciii1', 'Q16(c)(iii)1', 'C', _C(8, 'What is meant by the term diffusion?'),
      [pt(S('Movement of molecules from a region', 'concentration gradient.'), 3)], 'bio-2-6',
      'diffusion', SQ(29, '1. What is meant by the term diffusion?'), 3, stem=[Q16_OSM]),
    T('16ciii2', 'Q16(c)(iii)2', 'C', _C(8, 'Explain in detail why osmosis'),
      [pt(S('It is the movement of water'), 3)], 'bio-2-6', 'osmosis-as-special-diffusion',
      SQ(29, '2. Explain in detail why osmosis'), 3, stem=[Q16_OSM]),
    T('16ciii3', 'Q16(c)(iii)3', 'C', _C(8, 'Why is diffusion described as passive'),
      [pt(S('No energy is required'), 3)], 'bio-2-6', 'passive-transport',
      SQ(29, '3. Why is diffusion'), 3, stem=[Q16_OSM]),
    T('16civ', 'Q16(c)(iv)', 'C', _C(8, 'Outline how a named structure in the cell in solution B', 'shape of the cell.'),
      [pt(S('Vacuole or cell wall'), 3, label=S('Named structure:')),
       pt(S('Vacuole fills with water'), 3)],
      'bio-2-6', 'how-plant-cells-keep-their-shape', SQ(29, 'Outline how a named structure'), 6,
      stem=[Q16_C], fig='q16-plant-cells'),
    T('16cv', 'Q16(c)(v)', 'C', _C(8, 'Explain how solution B differs from solution A.'),
      [anyn(None, 1, 3, options=[S('Low solute (or named solute)', 'solute) concentration'),
                                 S('Higher water concentration', 'Lower water concentration')],
            note='Each option reads solution B first, then solution A, as the scheme\'s two '
                 'columns do.')],
      'bio-2-6', 'comparing-solutions', SQ(29, 'Explain how solution B differs'), 3,
      stem=[Q16_C], fig='q16-plant-cells'),
    T('16cvi', 'Q16(c)(vi)', 'C', _C(8, 'Suggest what might happen to an animal cell'),
      [pt(S('Swell or burst'), 3)], 'bio-2-6', 'animal-cell-in-dilute-solution',
      SQ(29, 'Suggest what might happen'), 3, stem=[Q16_C], fig='q16-plant-cells'),
    T('16cvii', 'Q16(c)(vii)', 'C', _C(8, 'Foods can be preserved using different solutions.', 'Explain your answer.'),
      [pt(S('A'), 2), pt(S('Micro-organisms (or named example)'), 1)], 'bio-2-6',
      'osmosis-in-food-preservation', SQ(29, 'Foods can be preserved'), 3,
      stem=[Q16_C], fig='q16-plant-cells'),
    T('16di', 'Q16(d)(i)', 'C', _C(8, 'Name the kingdom to which yeast belong.'),
      [pt(S('Fungi'), 3)], 'bio-3-2', 'yeast-kingdom', SQ(30, 'Name the kingdom'), 3,
      stem=[Q16_D], fig='q16-yeast'),
    T('16dii', 'Q16(d)(ii)', 'C', _C(8, 'Name the type of asexual reproduction shown', 'diagram.'),
      [pt(S('Budding'), 3)], 'bio-3-2', 'budding', SQ(30, 'Name the type of asexual'), 3,
      stem=[Q16_D], fig='q16-yeast'),
    T('16diii', 'Q16(d)(iii)', 'C', _C(8, 'Identify one advantage of asexual reproduction.'),
      [pt(S('Fast or only one parent'), 3)], 'bio-3-2', 'advantage-of-asexual-reproduction',
      SQ(30, 'Identify one advantage'), 3),
    T('16div', 'Q16(d)(iv)', 'C', _C(8, 'Copy the diagram into your answerbook and label any', 'three parts.'),
      [pt(S('Any three parts correctly labelled'), 3, kind='criterion', units=[1, 1, 1],
          note='Priced 3(1): one mark for each correctly labelled part.')],
      'bio-3-2', 'yeast-cell-structure', SQ(30, 'Copy the diagram'), 3, stem=[Q16_D], fig='q16-yeast'),
    T('16dv', 'Q16(d)(v)', 'C', _C(8, 'Micro-organisms, such as yeasts', 'underlined terms clearly.'),
      [pt(S('Asepsis:', 'Free from pathogens.'), 3), pt(S('Sterility:', 'organisms.'), 3)],
      'bio-3-2', 'asepsis-and-sterility', SQ(30, 'Micro-organisms, such as yeasts'), 6),
    T('16dvi', 'Q16(d)(vi)', 'C', _C(8, 'Name one other species you have studied', 'kingdom as yeast.'),
      [pt(S('Rhizopus'), 3)], 'bio-3-2', 'rhizopus', SQ(30, 'Name one other species'), 3),
    T('16dvii', 'Q16(d)(vii)', 'C', _C(8, 'State how the process of asexual reproduction', 'species you named at part (vi) above.'),
      [pt(S('Uses spores'), 3)], 'bio-3-2', 'asexual-reproduction-in-rhizopus',
      SQ(30, 'State how the process'), 3,
      stem=[M('(ii)', 8), _C(8, 'Name the type of asexual reproduction shown', 'diagram.'),
            M('(vi)', 8), _C(8, 'Name one other species you have studied', 'kingdom as yeast.')],
      fig='q16-yeast'),
    T('16dviii', 'Q16(d)(viii)', 'C', _C(8, 'Name one other unicellular organism', 'which it belongs.'),
      [pt(S('Amoeba or bacteria'), 3, label=S('Name:')), pt(S('Protista or Monera'), 3, label=S('Kingdom:'))],
      'bio-3-2', 'unicellular-organisms', SQ(30, 'Name one other unicellular'), 6),
    T('17ai', 'Q17(a)(i)', 'C', _C(9, 'Identify each type of blood vessel,', 'X and Y.'),
      [pt(S('Arteriole'), 2, label=S('X:')), pt(S('Venule'), 2, label=S('Y:'))], 'bio-2-6',
      'arterioles-and-venules', SQ(31, 'Identify each type of blood vessel'), 4,
      stem=[Q17_A], fig='q17-capillary-network'),
    T('17aii1', 'Q17(a)(ii)1', 'C', [Q17_TERMS, _C(9, '1.'), _C(9, 'Blood pressure')],
      [pt(S('The force the blood exerts'), 3)], 'bio-2-6', 'blood-pressure',
      SQ(31, '1. Blood pressure'), 3),
    T('17aii2', 'Q17(a)(ii)2', 'C', [Q17_TERMS, _C(9, '2.'), _C(9, 'Pulse')],
      [pt(S('(Rhythmic) expansion'), 3)], 'bio-2-6', 'pulse', SQ(31, '2. Pulse'), 3),
    T('17aiii', 'Q17(a)(iii)', 'C', _C(9, 'How does the blood pressure change as', 'the diagram?'),
      [pt(S('Decreases'), 3)], 'bio-2-6', 'blood-pressure-in-capillaries',
      SQ(31, 'How does the blood pressure change'), 3, stem=[Q17_A], fig='q17-capillary-network'),
    T('17aiv', 'Q17(a)(iv)', 'C', _C(9, 'Draw labelled diagrams of a vein', 'between them.'),
      [pt(S('Diagram of vein:', 'large lumen'), 2, kind='criterion'),
       pt(S('Diagram of artery:', 'small lumen'), 2, kind='criterion'),
       pt(S('Diagram of capillary: wall one cell thick'), 2, kind='criterion'),
       anyn(S('muscle wall / lumen', 'endothelium'), 2, 1)],
      'bio-2-6', 'artery-vein-capillary', SQ(31, 'Draw labelled diagrams of a vein'), 8),
    T('17av', 'Q17(a)(v)', 'C', _C(9, 'Name the type of vessel that is also present', 'around the cells.'),
      [pt(S('Lymph (vessel)'), 3)], 'bio-2-6', 'lymph-vessels', SQ(31, 'Name the type of vessel'), 3),
    T('17avi1', 'Q17(a)(vi)1', 'C', [Q17_FACTORS, _C(9, '1.', nth=2), _C(9, 'Exercise')],
      [pt(S('Correct matching effect described'), 3, kind='criterion')], 'bio-2-6',
      'exercise-and-the-circulatory-system', SQ(31, '1. Exercise'), 3),
    T('17avi2', 'Q17(a)(vi)2', 'C', [Q17_FACTORS, _C(9, '2.', nth=2), _C(9, 'Diet')],
      [pt(S('Correct matching effect described'), 3, kind='criterion')], 'bio-2-6',
      'diet-and-the-circulatory-system', SQ(31, '2. Diet'), 3),
    T('17bi1', 'Q17(b)(i)1', 'C', [Q17_COPY, _C(9, '1.', nth=3), _C(9, 'A sweat gland')],
      [pt(S('A sweat gland: Sketch'), 3, kind='criterion')], 'bio-2-4', 'sweat-gland-in-skin',
      SQ(32, 'Copy the diagram into your answerbook'), 3, stem=[Q17_B], fig='q17-skin'),
    T('17bi2', 'Q17(b)(i)2', 'C', [Q17_COPY, _C(9, '2.', nth=3), _C(9, 'A hair')],
      [pt(S('A hair:', 'and labelled'), 3, kind='criterion')], 'bio-2-4', 'hair-in-skin',
      SQ(32, 'Copy the diagram into your answerbook'), 3, stem=[Q17_B], fig='q17-skin'),
    T('17bii', 'Q17(b)(ii)', 'C', _C(9, 'Name the two main components of', 'sweat.'),
      [pt(S('Water'), 2), pt(S('Salt'), 2)], 'bio-2-4', 'components-of-sweat',
      SQ(32, 'Name the two main components'), 4),
    T('17biii', 'Q17(b)(iii)', 'C', _C(9, 'Describe how this helps to regulate'),
      [pt(S('Water evaporates from surface'), 2), pt(S('Using body heat'), 2),
       pt(S('Cools body down'), 2)],
      'bio-2-4', 'sweating-and-temperature', SQ(32, 'Describe how this helps'), 6,
      stem=[_C(9, 'In warm conditions, sweat is produced.')]),
    T('17biv', 'Q17(b)(iv)', 'C', _C(9, 'State and explain how hair on the skin', 'cold conditions.'),
      [pt(S('Hair stands up or piloerection'), 2, label=S('State:')),
       pt(S('Traps air'), 2, label=S('Explain:')), pt(S('Insulates'), 2)],
      'bio-2-4', 'hair-and-temperature', SQ(32, 'State and explain how hair'), 6),
    T('17bv', 'Q17(b)(v)', 'C', _C(9, 'Explain the term endotherm.'),
      [pt(S('An animal that can generate', 'its own temperature'), 3)], 'bio-2-4', 'endotherms',
      SQ(32, 'Explain the term endotherm'), 3),
    T('17bvi', 'Q17(b)(vi)', 'C', _C(9, 'What name is given to the ability of organisms', 'environment?'),
      [pt(S('Homeostasis'), 3)], 'bio-2-4', 'homeostasis', SQ(32, 'What name is given to the ability'), 3),
    T('17bvii', 'Q17(b)(vii)', 'C', _C(9, 'State one reason why it is important', 'internal environment.'),
      [pt(S('So enzymes (or metabolism)'), 2)], 'bio-2-4', 'why-homeostasis-matters',
      SQ(32, 'State one reason why it is important'), 2),
    T('17ci', 'Q17(c)(i)', 'C', _C(10, 'Explain the term excretion.'),
      [pt(S('Removal of the waste products'), 3)], 'bio-2-6', 'excretion',
      SQ(33, 'Explain the term excretion'), 3, stem=[Q17_C]),
    T('17cii1', 'Q17(c)(ii)1', 'C', Q17_URINARY,
      [pt(S('Diagram: Kidney and ureter', 'correct locations'), 6, kind='criterion', units=[3, 3],
          note_sel=S('(One missing or incorrect location', '= 0 marks)')),
       anyn(S('Kidney / Ureter', 'Urethra'), 4, 1)],
      'bio-2-6', 'urinary-system', SQ(33, 'Draw a large diagram of the human urinary'), 10),
    T('17cii2', 'Q17(c)(ii)2', 'C', _C(10, 'On the diagram you have drawn', 'through the ureter.'),
      [pt(S('Correct arrow showing pathway'), 2, kind='criterion')], 'bio-2-6', 'path-of-urine',
      SQ(33, 'On the diagram you have drawn'), 2, stem=[M('1.', 10), Q17_URINARY]),
    T('17ciii1', 'Q17(c)(iii)1', 'C', _C(10, 'What name is given to this structure?'),
      [pt(S('Nephron'), 2)], 'bio-2-6', 'nephron', SQ(33, 'What name is given to this structure?'), 2,
      stem=[Q17_NEPHRON], fig='q17-nephron'),
    T('17ciii2', 'Q17(c)(iii)2', 'C', _C(10, 'Name the parts labelled A and B.'),
      [pt(S('Bowman'), 2, label=S('A:')), pt(S('Loop of Henle'), 2, label=S('B:'))], 'bio-2-6',
      'bowmans-capsule-and-loop-of-henle', SQ(33, 'Name the parts labelled A and B.'), 4,
      stem=[Q17_NEPHRON], fig='q17-nephron',
      labels=[L('A', S('Bowman', page=33), True), L('B', S('Loop of Henle', page=33), True)]),
    T('17ciii3', 'Q17(c)(iii)3', 'C', _C(10, 'Outline what happens in each part', 'production.'),
      [pt(S('Filtration (of small molecules)'), 3, label=S('A:')),
       pt(S('Reabsorption of water'), 3, label=S('B:'))],
      'bio-2-6', 'filtration-and-reabsorption', SQ(33, 'Outline what happens in each part'), 6,
      stem=[Q17_NEPHRON], fig='q17-nephron',
      labels=[L('A', S('Bowman', page=33), False), L('B', S('Loop of Henle', page=33), False)]),
    T('17civ', 'Q17(c)(iv)', 'C', _C(10, 'Under normal conditions, there is no protein', 'absence from urine.'),
      [pt(S('(Protein) is too big'), 3)], 'bio-2-6', 'no-protein-in-urine',
      SQ(33, 'Under normal conditions'), 3),
    T('17di', 'Q17(d)(i)', 'C', _C(10, 'Name the fluid found in the central', 'canal.'),
      [pt(S('Cerebrospinal (fluid)'), 2)], 'bio-2-4', 'cerebrospinal-fluid',
      SQ(34, 'Name the fluid found'), 2, stem=[Q17_D], fig='q17-spinal-cord'),
    T('17dii1', 'Q17(d)(ii)1', 'C', _C(10, 'Name the protective tissue Y', 'has three layers.'),
      [pt(S('Meninges'), 2)], 'bio-2-4', 'meninges', SQ(34, '1. Name the protective tissue Y'), 2,
      stem=[Q17_D], fig='q17-spinal-cord'),
    T('17dii2', 'Q17(d)(ii)2', 'C', _C(10, 'Name one other structure that', 'protects the spinal cord.'),
      [pt(S('Vertebrae'), 2)], 'bio-2-4', 'vertebrae-protect-the-cord',
      SQ(34, '2. Name one other structure'), 2, stem=[Q17_D], fig='q17-spinal-cord'),
    T('17diii', 'Q17(d)(iii)', 'C', _C(10, 'Name the regions of the spinal cord', 'labelled P and Q.'),
      [pt(S('White matter'), 2, label=S('P:')), pt(S('Grey matter'), 2, label=S('Q:'))], 'bio-2-4',
      'white-and-grey-matter', SQ(34, 'Name the regions of the spinal cord'), 4,
      stem=[Q17_D], fig='q17-spinal-cord',
      labels=[L('P', S('White matter', page=34), True), L('Q', S('Grey matter', page=34), True),
              L('Y', S('Meninges', page=34), False)]),
    T('17div1', 'Q17(d)(iv)1', 'C', Q17_NEURON,
      [pt(S('Diagram: Dendrites and cell body'), 6, kind='criterion', units=[3, 3],
          note_sel=S('(One missing = 3 marks'))],
      'bio-2-4', 'neuron-diagram', SQ(34, '1. Draw a large diagram of a neuron.'), 6),
    T('17div2', 'Q17(d)(iv)2', 'C', _C(10, 'On your diagram label the following parts:', 'Myelin sheath'),
      [anyn(S('Axon / Dendrite / Myelin sheath'), 3, 1)], 'bio-2-4', 'parts-of-a-neuron',
      SQ(34, '2. On your diagram label'), 3, stem=[M('1.', 10), Q17_NEURON]),
    T('17div3', 'Q17(d)(iv)3', 'C', _C(10, 'On your diagram indicate with an arrow', 'impulse.'),
      [pt(S('Arrow from dendrite towards axon'), 2)], 'bio-2-4', 'direction-of-an-impulse',
      SQ(34, '3. On your diagram indicate'), 2, stem=[M('1.', 10), Q17_NEURON]),
    T('17dv', 'Q17(d)(v)', 'C', _C(10, 'Describe the mechanism of a reflex action.'),
      [anyn(S('Receptor detects stimulus', 'muscle contracts'), 3, 3,
            note_sel=S('If ‘impulse’ or ‘message’'))],
      'bio-2-4', 'reflex-action', SQ(34, 'Describe the mechanism of a reflex'), 9),
]

# Q15(b)(iii): the scheme's three name-and-function routes, one per hormone.
ANSWER_VARIANTS = {
    '15biii': [
        ('progesterone', 'Progesterone',
         [pt(S('Progesterone'), 3), pt(S('Maintains endometrium'), 3,
                                       note_sel=S('Name = 3; Precise function = 3'))]),
        ('fsh', 'FSH', [pt(S('FSH'), 3), pt(S('Stimulate follicles'), 3,
                                           note_sel=S('Name = 3; Precise function = 3'))]),
        ('lh', 'LH', [pt(S('LH'), 3), pt(S('Stimulates ovulation'), 3,
                                         note_sel=S('Name = 3; Precise function = 3'))]),
    ],
}
