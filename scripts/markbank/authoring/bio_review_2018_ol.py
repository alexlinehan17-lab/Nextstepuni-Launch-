"""Biology 2018 Ordinary Level — reviewed task ledger, carded from the paper for the first time.

Independent visual sweep (2026-10-24), every page rendered and read:
  * The 2018 paper is one booklet, 16 pages: p1 cover and instructions,
    p2-p4 Section A Questions 1-6, p5-p7 Section B Questions 7-9, p8-p15
    Section C Questions 10-15, p16 "Blank Page". Sections A and B are
    answered on the paper; Section C in an answer book.
  * The marking scheme, 12 pages: p1 cover, p2 note, p3 introduction and
    cancelled and surplus answers, p4 surplus answers continued and the
    conventions, p5-p10 Questions 1-15 (one table, no page numbers), p11
    "Blank Page", p12 back cover.

The paper keeps the long-standing shape: any five of Section A's six
questions, any two of Section B's three, any four of Section C's six, and
Questions 14 and 15 are each any two of (a), (b), (c). Every printed ask is
carded. No Biology card existed for 2018 Ordinary before this review.

The scheme counts POINTS ("(1 pt)", "(2 pts)") and heads each question or
part with what the points are worth. Ordered splits are carded at their first
rate: Q1 and Q3 "9 + 8 + 3(1)" over five points, Q2, Q4 and Q5 "8 + 7 + 5(1)"
over seven, Q6 "4(4) + 4(1)" over eight, every Section B (a) "5 + 1" and (b)
"2(9) + 6(1)", every Section C (a) of Q10-Q13 "7 + 2(1)", and Q12(b)(ii)
"6 + 3" over its two numbered items. Section C (b) is "9(3)", (c) "8(3)",
Q12(b) prices each roman ("4(3)", "6 + 3", "3", "3"), and every part of Q14
and Q15 is "10(3)": a fixed 3 per point. A Section C (a) ladder sits beside
its question's fixed (b) and (c), so each such ladder names their units as
fixed and their cards are exempt from its notation.

Most of the scheme sets its compressed reprint of the ask on the answer's own
printed line ("Monosaccharide example: e.g. Glucose"); those tasks are anchored
on the part's own marker under its question (SQ path), as 2019 Higher does.
Where the reprint stands on a line of its own above the answer it is the
pairing anchor and is wording-checked.

The scheme numbers Q11(a)(iii) "(ii)" a second time; it is anchored on its
reprint "Homozygous:" instead. The census reader lost Questions 6-15 to a head
welded after Q5(g)'s circle options "T F" (paper.py WELDED_HEADS, gated to
this sitting). No printed choice is marked differently per option: Q7(b)'s
breathing or pulse rate and Q14(a)(vi)'s ear or eye share one set of rows.
"""
from bio_review_lib import Q, SQ, S, M, pt, anyn, T, L

YEAR, LEVEL = 2018, 'ol'
REVIEWED_AT = '2026-10-24'

SOURCES = {
    'paper': {'path': 'examiner-reports/biology/papers/2018-ol-paper.pdf',
              'fileid': 'LC025GLP000EV.pdf',
              'sha256': '414dc21d069b170d4010359a90b3e066fd1d73cd8a0444870008a0f64ff32ad4',
              'pages': 16},
    'scheme': {'path': 'examiner-reports/biology/schemes/2018-ol.pdf',
               'fileid': 'LC025GLP000EV.pdf',
               'sha256': '7b130a4f431b363258859c1b56d4d41df1aa44f771c20298de51feddb803c972',
               'pages': 12},
}

PAGE_ROLES = {
    'paper': {1: 'cover', **{p: 'questions' for p in range(2, 16)}, 16: 'blank'},
    'scheme': {1: 'cover', 2: 'note', 3: 'introduction', 4: 'conventions',
               **{p: 'marking' for p in range(5, 11)}, 11: 'blank', 12: 'back-cover'},
}


def _ladder(notation, **extra):
    """An ordered split as the scheme prints it ("9 + 8 + 3(1)", "2(9) + 6(1)")."""
    steps = []
    for term in notation.split('+'):
        n, _, m = term.strip().partition('(')
        steps += [int(m.rstrip(')'))] * int(n) if m else [int(n)]
    return {'steps': steps, 'notation': notation, **extra}


QUESTION_TOTALS = {
    **{n: 20 for n in range(1, 7)}, **{n: 30 for n in range(7, 10)},
    **{n: 60 for n in range(10, 14)}, 14: 90, 15: 90,   # Q14, Q15: any two of three 30s
}
PART_TOTALS = {
    **{(n, x): t for n in (10, 11, 13) for x, t in (('b', 27), ('c', 24))},
    (12, 'c'): 24,   # Q12(b) holds the "6 + 3" ladder, so its cards do not add to 27
    **{(n, x): 30 for n in (14, 15) for x in 'abc'},
}
LADDERS = {
    1: _ladder('9 + 8 + 3(1)'), 3: _ladder('9 + 8 + 3(1)'),
    **{q: _ladder('8 + 7 + 5(1)') for q in (2, 4, 5)},
    6: _ladder('4(4) + 4(1)'),
    **{(n, 'a'): _ladder('5 + 1') for n in (7, 8, 9)},
    **{(n, 'b'): _ladder('2(9) + 6(1)') for n in (7, 8, 9)},
    # Section C (a) "7 + 2(1)"; (b) "9(3)" and (c) "8(3)" are fixed points
    # beside it, named here so the question's total is the ladder's.
    **{(n, 'abc'): _ladder('7 + 2(1)', fixed={3: 17}) for n in (10, 11, 13)},
    # Q12: (b)(i) "4(3)", (iii) "3", (iv) "3" and (c) "8(3)" fixed; (b)(ii)
    # "6 + 3" is a ladder of its own over its two numbered items.
    (12, 'abc'): _ladder('7 + 2(1)', fixed={3: 14}),
    (12, 'B'): _ladder('6 + 3'),
}
LADDER_OF = {'12bii1': (12, 'B'), '12bii2': (12, 'B')}

CHECKSUMS = {
    1: {9: 5}, 3: {9: 5}, **{q: {8: 7} for q in (2, 4, 5)}, 6: {4: 8},
    **{(n, 'a'): {5: 2} for n in (7, 8, 9)}, **{(n, 'b'): {9: 8} for n in (7, 8, 9)},
    **{(n, 'a'): {7: 3} for n in range(10, 14)},
    **{(n, 'b'): {3: 9} for n in (10, 11, 13)}, (12, 'b'): {3: 6, 6: 2},
    **{(n, 'c'): {3: 8} for n in range(10, 14)},
    **{(n, x): {3: 10} for n in (14, 15) for x in 'abc'},
}

SCAN_PAGES = {'paper': range(1, 16)}
SELECTION_SCAN = [
    ('paper', 1, 'any five', 'Cover rubric, Section A: whole-question choice; every question is carded.'),
    ('paper', 1, 'any two', 'Cover rubric, Section B: whole-question choice; every question is carded.'),
    ('paper', 1, 'any four', 'Cover rubric, Section C: whole-question choice; every question is carded.'),
    ('paper', 2, 'any five', 'Section A rubric repeated.'),
    ('paper', 3, 'choose', 'Q3 "Choose a term": every description matched, one card per lettered part.'),
    ('paper', 3, 'the following', 'Q3 list of terms: the options.'),
    ('paper', 4, 'the following', 'Q5 lead-in: every statement asked, one card per letter.'),
    ('paper', 4, 'or', 'Q5 "true (T) or false (F)": the answer options.'),
    ('paper', 4, 'or', 'Q5 "T or F": the answer options.'),
    ('paper', 4, 'any two', 'Q6(b) "Name any two structures": one menu, claim two.'),
    ('paper', 4, 'both', 'Q6(c) "Name both": both substances asked, a row each.'),
    ('paper', 5, 'any two', 'Section B rubric repeated.'),
    ('paper', 5, 'or', 'Q7(b) "breathing rate or on pulse rate": either investigation; marked on the same rows.'),
    ('paper', 8, 'any four', 'Section C rubric repeated.'),
    ('paper', 8, 'the following', 'Q10(a) lead-in: every term asked, one card per roman.'),
    ('paper', 8, 'or', 'Q10(c) passage "brown or beige": passage text.'),
    ('paper', 9, 'the following', 'Q11(a) lead-in: every term asked, one card per roman.'),
    ('paper', 10, 'the following', 'Q12(b)(i) "each of the following parts": one card per numbered part.'),
    ('paper', 10, 'or', 'Q12(b)(iii) "Name or give the letter": either form of the one answer; one row.'),
    ('paper', 11, 'the following', 'Q13(a) lead-in: every process asked, one card per roman.'),
    ('paper', 12, 'any two', 'Q14 "any two of (a), (b), (c)": whole-part choice; every part is carded.'),
    ('paper', 12, 'or', 'Q14(a)(vi) "of the ear or of the eye": marked on one disorder row and one correction row; '
                        'one card.'),
    ('paper', 14, 'any two', 'Q15 "any two of (a), (b), (c)": whole-part choice; every part is carded.'),
    ('paper', 14, 'or', 'Q15(b)(v) "monocotyledonous (monocot) or dicotyledonous (dicot)": description.'),
    ('paper', 14, 'any one', 'Q15(b)(v) "Give any one difference": one response.'),
]

ROUTES = {}

SEC = 'State Examinations Commission'
SAME_LINE = 'The scheme sets its reprint of the ask on the answer\'s own line: anchored on the part\'s marker.'
COMPRESSED = 'The scheme heads the answer with a compressed reprint of the ask.'
EACH_ITEM = 'A list the scheme prices entry by entry: one card per entry, each its own slice of the printed line.'
NO_ANSWER = 'The scheme prints no answer here, only what earns the marks.'
TWO_POINTS = 'The scheme prices this part at two points: each printed point its own row.'


def at(page, q, *path_and_marker, why=SAME_LINE):
    """The part's own marker under its question (and letter) on the scheme page."""
    *path, marker = path_and_marker
    return SQ(page, marker, path=[str(q), *path], paired=why, bare=True)


def rq(page, label, paired=None):
    """The scheme's reprint of the ask on a line of its own above the answer."""
    return SQ(page, label, label, paired=paired)


def ask(page, sentence, **kw):
    """A one-line ask closed by its own punctuation, before its answer line."""
    return Q(page, sentence, sentence, **kw)


def cell(line, i, cuts, page=None, meaning=False):
    """Cell i of a scheme line printed as cells ("A = Ligament B = Cartilage C = ..."), cut at the
    cells' own printed boundaries: cuts[k] = (text opening cell k+1, text closing cell k). With
    `meaning`, the cell's answer alone (after its " = "), for a figure's label key."""
    pieces, seps = [], []
    if i > 0:
        pieces.append(2)
        seps.append(cuts[i - 1][1])
    if i < len(cuts):
        pieces.append(1)
        seps.append(cuts[i][0])
    if meaning:
        pieces.append(2)
        seps.append(' = ')
    return S(line, page=page, piece=pieces, psep=seps)


def labels(line, letters, cuts, page, asked=None):
    return [L(x, cell(line, i, cuts, page=page, meaning=True), x == asked) for i, x in enumerate(letters)]


# ------------------------------------------------------------ question text --
Q2 = Q(2, 'The diagram shows a human synovial joint.')
Q3 = Q(3, 'Choose a term from the following list and place it in Column B to match a description in',
       'The first one has been completed as an example.')
Q4 = Q(3, 'The diagram shows the human male reproductive system.')
Q5 = Q(4, 'Indicate whether each of the following statements is true (T) or false (F) by drawing a circle around',
       'T or F in each case.')
Q6 = Q(4, 'The diagram shows a plant cell.')
Q7B = Q(5, 'You investigated the effect of exercise on breathing rate or on pulse rate.')
Q7BIII = [Q(5, 'A fit student and an unfit student measured their breathing rates, then carried out',
            'These are their results.'),
          Q(5, 'Use the table to identify the:', br=True), Q(5, 'Unfit student', br=True)]
Q8B = Q(5 + 1, 'You investigated the effect of temperature on the rate of activity of an enzyme.')
Q9B = Q(7, 'You investigated digestive activity in germinating seeds.')
Q9BII = [Q(7, 'The seeds were divided into two batches.'), Q(7, 'Batch A seeds were not treated before use.'),
         Q(7, 'How did you treat the other batch of seeds (batch B) before using them in the', 'investigation?')]
Q9BV = Q(7, 'After a few days the seeds were removed from the agar. A solution was then poured',
         'over the agar. Name this solution.')
Q10A = Q(8, 'Explain the following terms used in ecology:')
Q10B = Q(8, 'The food web below shows the feeding relationships between some plants and animals in a',
         'Study the web and answer the questions below.')
Q10C = Q(8, 'Peacock spiders are tiny jumping spiders found in southern Australia. They do not build',
         'are brown or beige in colour and are well camouflaged in their environment.')
Q11A = Q(9, 'Explain the following terms used in genetics:')
Q11B = [Q(9, 'DNA has four bases: Adenine (A), Guanine (G), Cytosine (C), and Thymine (T).'),
        Q(9, 'The diagram below outlines part of the structure of DNA.')]
Q11BV = [Q(9, 'Another molecule in the cell also has four bases, one of which is uracil.'),
         Q(9, 'Name this molecule.')]
Q11C = Q(9, 'In plants the allele for tall (T) is dominant to the allele for short (t).')
Q11CHUMAN = Q(9, 'In humans, sex is determined by two chromosomes, X and Y.')
Q12A = Q(10, 'Most animals and plants have vascular systems.')
Q12B = Q(10, 'The diagram represents the human blood circulatory system.')
Q12BI = Q(10, 'In your answer book, state which letter represents each of the following parts:')
Q12BII = Q(10, 'State what changes occur in the blood as it passes through:')
Q12C = Q(10, 'The diagram shows a section through human skin.')
Q13A = Q(11, 'Name the cell part associated with each of the following:')
Q13B = Q(11, 'The equation below represents photosynthesis.')
Q13CIII = [Q(11, 'Fermentation is another name for anaerobic respiration.'),
           Q(11, 'Name one organism used in the fermentation process that produces beer and wine.')]
Q14A = Q(12, 'The diagram shows the human ear.')
Q14B = Q(12, 'In 1796 an English doctor‐scientist called Edward Jenner inserted pus from a cowpox blister',
         'half of the 20th century, smallpox was declared eradicated in 1980.')
Q14C = Q(13, 'The diagram shows a human mouth.')
Q14CI = [Q(13, 'In your answer book, match each type of tooth from the list below to one of the',
           'letters in the diagram above.'),
         Q(13, 'List: Canine,', 'Pre‐molar.', br=True)]
Q14CIII = Q(13, 'Suggest, from the above list, a type of tooth that is much larger in dogs.')
Q14CV = Q(13, 'The mouth has glands that make a liquid. The liquid contains an enzyme.')
Q15A = Q(14, 'The diagram shows a flower.')
Q15AIV = Q(14, 'Some seeds undergo a period of dormancy.')
Q15AV = Q(14, 'It is possible to produce seedless fruits.')
Q15B = Q(14, 'The diagram shows a transverse section of a dicotyledonous (dicot) root.')

# ------------------------------------------------------- scheme cell lines --
JOINT = ('A = Ligament B = Cartilage C = (Synovial) fluid', [(' B =', 'Ligament '), (' C =', 'Cartilage ')])
MALE = ('A = Penis B = Testis C = Urethra [allow sperm duct or vas deferens]',
        [(' B =', 'Penis '), (' C =', 'Testis ')])
CELL = ('D = Vacuole E = Nucleus', [(' E =', 'Vacuole ')])
STUDENTS = ('Unfit student = B Fit student = A', [(' Fit student =', '= B ')])
BASES = ('X = Adenine or A Y = Guanine or G', [(' Y =', 'or A ')])
SEXES = ('Male = XY Female = XX', [(' Female =', '= XY ')])
SKIN = ('A = Hair B = Blood vessel(s) C = Sweat gland', [(' B =', 'Hair '), (' C =', 'vessel(s) ')])
TEETH = ('Canine = C Molar = A Incisor = D Pre-molar = B',
         [(' Molar =', '= C '), (' Incisor =', '= A '), (' Pre-molar =', '= D ')])
FLOWER = ('A = Stigma B = Anther C = Ovary (or ovule)', [(' B =', 'Stigma '), (' C =', 'Anther ')])
ROOT = ('A = Phloem B = Xylem C = Root hair', [(' B =', 'Phloem '), (' C =', 'Xylem ')])
EAR = ['A = Semi-circular canal(s)/ function = balance', 'B = Cochlea/ function = hearing',
       'C = Ear drum/ function = hearing']
VESSELS = [('E', 'Aorta = E', [' 2. ', ' = ']), ('F', 'Hepatic portal vein = F', [' = ']),
           ('D', 'Pulmonary vein = D', [' 4. ', ' = ']), ('J', 'Vena cava = J', [' = '])]


def tooth_labels(asked):
    # The scheme names each tooth by its letter ("Canine = C"): the letter's meaning is the tooth.
    return [L(letter, S(TEETH[0], page=9, piece=([2] if i else []) + ([1] if i < 3 else []) + [1],
                        psep=([TEETH[1][i - 1][1]] if i else []) + ([TEETH[1][i][0]] if i < 3 else []) + [' = ']),
              letter == asked) for i, letter in enumerate('CADB')]


def vessel_labels(asked):
    return [L(letter, S(start, page=8, piece=[1] * len(seps), psep=seps), letter == asked)
            for letter, start, seps in VESSELS]


def ear_labels(asked):
    return [L(x, S(line, page=9, piece=[1, 2], psep=['/', ' = ']), x == asked) for x, line in zip('ABC', EAR)]


TASKS = [
    # ------------------------------------------------------------ Section A --
] + [
    T(f'1{x}', f'Q1({x})', 'A', q, [pt(S(ans), 9)], 'bio-1-2', concept, at(5, 1, f'({x})'), 9)
    for x, q, ans, concept in [
        ('a', Q(2, 'All proteins are made of carbon, hydrogen, oxygen, and'), 'Nitrogen', 'elements-in-protein'),
        ('b', ask(2, 'Give one example of a monosaccharide.'), 'e.g. Glucose', 'monosaccharide'),
        ('c', Q(2, 'A solution used to test for the presence of a reducing sugar is'), "Benedict's or Fehling's",
         'test-for-reducing-sugar'),
        ('d', ask(2, 'Name one mineral needed for healthy bones.'), 'Calcium or phosphorus', 'minerals-for-bones'),
        ('e', ask(2, 'Glycerol is part of a biomolecule. Name the biomolecule.'), 'Lipid', 'glycerol-in-lipids')]
] + [
    T(f'2a-{x.lower()}', 'Q2(a)', 'A', Q(2, 'Name the parts labelled A, B, C.'), [pt(cell(JOINT[0], i, JOINT[1]), 8)],
      'bio-2-4', concept, at(5, 2, '(a)'), 8, stem=[Q2], fig='q2-joint', item=(x.lower(), x),
      labels=labels(JOINT[0], 'ABC', JOINT[1], 5, asked=x), decision=EACH_ITEM)
    for i, (x, concept) in enumerate([('A', 'ligament'), ('B', 'cartilage'), ('C', 'synovial-fluid')])
] + [
    T(f'2{x}', f'Q2({x})', 'A', ask(2, q), [pt(S(ans), 8, **kw)], 'bio-2-4', concept, at(5, 2, f'({x})'), 8,
      stem=stem, fig='q2-joint')
    for x, q, ans, kw, concept, stem in [
        ('b', 'What type of synovial joint is the elbow?', 'Hinge', {}, 'hinge-joint', [Q2]),
        ('c', 'Name the structures that attach muscle to bone.', 'Tendons', {}, 'tendons', [Q2]),
        ('d', 'Name one disorder of the musculoskeletal system.', 'Arthritis or osteoporosis', {},
         'musculoskeletal-disorder', [Q2]),
        ('e', 'Suggest one treatment for the disorder mentioned above.', 'Matching treatment',
         {'kind': 'criterion', 'note': NO_ANSWER}, 'treating-a-musculoskeletal-disorder',
         [Q2, M('(d)', 2), ask(2, 'Name one disorder of the musculoskeletal system.')])]
] + [
    T(f'3{x}', f'Q3({x})', 'A', Q(3, *q), [pt(S(ans), 9)], 'bio-2-1', concept, at(5, 3, f'({x})'), 9,
      stem=[Q3], qfig='q3-table',
      decision='The list of terms (its first struck through as the worked example) and the table are shown as '
               'the question\'s own print.')
    for x, q, ans, concept in [
        ('a', ('An advantage of using immobilised enzymes',), 'Reusable', 'immobilised-enzymes-reusable'),
        ('b', ('A gel in which enzymes are trapped',), 'Alginate', 'alginate'),
        ('c', ('An example of an immobilised enzyme',), 'Pectinase', 'example-of-an-immobilised-enzyme'),
        ('d', ('The substance that hardens the gel beads', 'containing the trapped enzyme'), 'Calcium chloride',
         'calcium-chloride'),
        ('e', ('Immobilised enzymes can also be used in',), 'Washing powder', 'uses-of-immobilised-enzymes')]
] + [
    T(f'4a-{x.lower()}', 'Q4(a)', 'A', Q(3, 'Name the parts labelled A, B, C.'), [pt(cell(MALE[0], i, MALE[1]), 8)],
      'bio-2-5', concept, at(5, 4, '(a)'), 8, stem=[Q4], fig='q4-male', item=(x.lower(), x),
      labels=labels(MALE[0], 'ABC', MALE[1], 5, asked=x), decision=EACH_ITEM)
    for i, (x, concept) in enumerate([('A', 'penis'), ('B', 'testis'), ('C', 'urethra')])
] + [
    T(f'4{x}', f'Q4({x})', 'A', ask(3, q), [pt(S(ans), 8)], 'bio-2-5', concept, at(5, 4, f'({x})'), 8,
      stem=[Q4], fig='q4-male')
    for x, q, ans, concept in [
        ('b', 'Where are sperm cells produced?', 'Testis or B', 'where-sperm-are-made'),
        ('c', 'Name one male sex hormone.', 'Testosterone', 'testosterone'),
        ('d', 'Explain the term infertility.', 'Inability to produce offspring', 'infertility'),
        ('e', 'Give one cause of infertility in men.', 'e.g. Low sperm count', 'male-infertility')]
] + [
    T(f'5{x}', f'Q5({x})', 'A', Q(4, q), [pt(S(ans), 8)], 'bio-u2', concept, at(5, 5, f'({x})'), 8, stem=[Q5])
    for x, q, ans, concept in [
        ('a', 'A control is used for comparison in experiments', 'TRUE', 'controls'),
        ('b', 'The information collected in an experiment is called data', 'TRUE', 'data'),
        ('c', 'A hypothesis is a proven idea', 'FALSE', 'hypothesis'),
        ('d', 'Replicating an experiment means repeating it a number of times', 'TRUE', 'replication'),
        ('e', 'A theory is a hypothesis that has been disproved', 'FALSE', 'theory'),
        ('f', 'A variable never changes during an experiment', 'FALSE', 'variables'),
        ('g', 'Scientific discoveries are first published in newspapers', 'FALSE', 'publishing-results')]
] + [
    T(f'6a-{x.lower()}', 'Q6(a)', 'A', Q(4, 'Name the parts labelled D and E.'), [pt(cell(CELL[0], i, CELL[1]), 4)],
      'bio-1-3', concept, at(5, 6, '(a)'), 4, stem=[Q6], fig='q6-cell', item=(x.lower(), x),
      labels=labels(CELL[0], 'DE', CELL[1], 5, asked=x), decision=EACH_ITEM)
    for i, (x, concept) in enumerate([('D', 'vacuole'), ('E', 'nucleus')])
] + [
    T('6b', 'Q6(b)', 'A', Q(4, 'Name any two structures from the diagram that indicate this is a plant cell.'),
      [anyn(S('(Cell) wall/ (large) vacuole/ chloroplast(s) Any two'), 2, 4)], 'bio-1-3', 'plant-cell-structures',
      rq(5, 'Two structures that indicate it is a plant cell:'), 8, stem=[Q6], fig='q6-cell'),
    T('6c', 'Q6(c)', 'A', Q(4, 'The cell membrane is composed of two substances. Name both.'),
      [pt(S('Lipid and protein', piece=n, psep=' and '), 4) for n in (1, 2)], 'bio-1-3', 'cell-membrane',
      at(5, 6, '(c)'), 8, stem=[Q6], fig='q6-cell', decision=TWO_POINTS),
    T('6d', 'Q6(d)', 'A', ask(4, 'Which labelled part is made of cellulose?'), [pt(S('(Cell) wall or B'), 4)],
      'bio-1-3', 'cell-wall', at(5, 6, '(d)'), 4, stem=[Q6], fig='q6-cell'),
    T('6e', 'Q6(e)', 'A', Q(4, 'What type of microscope is needed to show the ultrastructure of organelles such as C,',
                            'above?'),
      [pt(S('Electron (microscope)'), 4)], 'bio-1-3', 'electron-microscope', at(5, 6, '(e)'), 4, stem=[Q6],
      fig='q6-cell'),
    # ------------------------------------------------------------ Section B --
    T('7ai', 'Q7(a)(i)', 'B', ask(5, 'Name one muscle involved in breathing.'),
      [pt(S('Intercostal(s) or diaphragm'), 5)], 'bio-2-6', 'breathing-muscles', at(6, 7, '(a)', '(i)'), 5),
    T('7aii', 'Q7(a)(ii)', 'B', ask(5, 'In which structures does gas exchange occur in the lungs?'),
      [pt(S('Alveoli (or air sacs) [allow capillaries]'), 5)], 'bio-2-6', 'alveoli',
      rq(6, 'Lung structures in which gas exchange takes place:'), 5),
    T('7bi', 'Q7(b)(i)', 'B', ask(5, 'How did you measure the resting rate?'),
      [pt(S('Count pulse or count breaths/ time or rate/ repeat or average', piece=n), 9) for n in (1, 2, 3)],
      'bio-2-6', 'measuring-resting-rate', rq(6, 'How resting rate measured:'), 27, stem=[Q7B],
      decision='The scheme prices the method at three points (3 pts), each its own row on the ladder.'),
    T('7bii', 'Q7(b)(ii)', 'B', Q(5, 'After measuring the resting rate, what other steps did you carry out to complete',
                                  'the investigation?'),
      [pt(S('Exercise/ measure rate afterwards', piece=n), 9) for n in (1, 2)], 'bio-2-6', 'exercise-and-rate',
      at(6, 7, '(b)', '(ii)'), 18, stem=[Q7B], decision=TWO_POINTS),
    T('7biii', 'Q7(b)(iii)', 'B', Q7BIII, [pt(cell(STUDENTS[0], i, STUDENTS[1]), 9) for i in (0, 1)], 'bio-2-6',
      'fit-and-unfit-students', at(6, 7, '(b)', '(iii)'), 18, stem=[Q7B], fig='q7-table', decision=TWO_POINTS),
    T('7biv', 'Q7(b)(iv)', 'B', ask(5, 'Give a reason for your choice.'),
      [pt(S("Unfit student's rate increases by much more than fit student's rate or", 'vice versa'), 9)], 'bio-2-6',
      'fitness-and-breathing-rate', rq(6, 'Reason for choice:'), 9, stem=[Q7B, M('(iii)', 5)] + Q7BIII,
      fig='q7-table'),
    T('8ai', 'Q8(a)(i)', 'B', ask(6, 'What is an enzyme?'), [pt(S('Biological catalyst'), 5)], 'bio-2-1', 'enzyme',
      at(6, 8, '(a)', '(i)'), 5),
    T('8aii', 'Q8(a)(ii)', 'B', ask(6, 'From which biomolecule are enzymes made?'), [pt(S('Protein'), 5)], 'bio-2-1',
      'enzymes-are-proteins', at(6, 8, '(a)', '(ii)'), 5),
] + [
    T(f'8b{r}', f'Q8(b)({r})', 'B', q, rows, 'bio-2-1', concept, at(6, 8, '(b)', f'({r})'), total, stem=[Q8B],
      decision=decision)
    for r, q, rows, concept, total, decision in [
        ('i', ask(6, 'What enzyme did you use?'), [pt(S('Named enzyme'), 9, kind='criterion', note=NO_ANSWER)],
         'enzyme-used', 9, ''),
        ('ii', ask(6, 'What substrate did you use?'), [pt(S('Matching substrate'), 9, kind='criterion', note=NO_ANSWER)],
         'substrate-used', 9, ''),
        ('iii', Q(6, 'How did you vary the temperature during the investigation?'),
         [pt(S('Water bath(s)/ at different temperatures', piece=n), 9) for n in (1, 2)], 'varying-temperature', 18,
         TWO_POINTS),
        ('iv', Q(6, 'How did you measure the rate of enzyme activity?'),
         [pt(S('Relevant change/ per unit time', piece=1), 9, kind='criterion', note=NO_ANSWER),
          pt(S('Relevant change/ per unit time', piece=2), 9)], 'measuring-enzyme-activity', 18,
         TWO_POINTS + ' "Relevant change" names what earns the point, not an answer.'),
        ('v', [Q(6, 'During this investigation pH was kept constant.'), Q(6, 'How did you keep the pH constant?')],
         [pt(S('Buffer (solution)'), 9)], 'constant-ph', 9, ''),
        ('vi', Q(6, 'What was the result of your investigation?'),
         [pt(S('e.g. Increased activity as temperature increases or', 'enzyme stops working after a certain temperature'),
             9)], 'temperature-and-enzyme-activity', 9, '')]
] + [
    T('9ai', 'Q9(a)(i)', 'B', ask(7, 'What is meant by the term digestion?'), [pt(S('Breakdown of food'), 5)], 'bio-2-5',
      'digestion', at(6, 9, '(a)', '(i)'), 5),
    T('9aii', 'Q9(a)(ii)', 'B', Q(7, 'Name a carbohydrate that is stored in a seed.'), [pt(S('Starch'), 5)], 'bio-2-5',
      'seed-food-store', at(6, 9, '(a)', '(ii)'), 5),
    T('9bi', 'Q9(b)(i)', 'B', ask(7, 'Which type of agar did you use in this investigation?'),
      [pt(S('Starch (agar) or (skimmed) milk (agar)'), 9)], 'bio-2-5', 'agar-for-digestive-activity',
      at(6, 9, '(b)', '(i)'), 9, stem=[Q9B], fig='q9-plates'),
    T('9bii', 'Q9(b)(ii)', 'B', Q9BII, [pt(S('Boiled'), 9)], 'bio-2-5', 'boiled-seeds', at(6, 9, '(b)', '(ii)'), 9,
      stem=[Q9B], fig='q9-plates'),
    T('9biii', 'Q9(b)(iii)', 'B', Q(7, 'Why was such treatment necessary?'),
      [pt(S('To kill seeds or to denature enzymes [do not allow to kill', 'enzymes]'), 9)], 'bio-2-5',
      'why-boil-the-seeds', at(6, 9, '(b)', '(iii)'), 9, stem=[Q9B, M('(ii)', 7)] + Q9BII, fig='q9-plates'),
    T('9biv', 'Q9(b)(iv)', 'B', [Q(7, 'The seeds were cut in half and placed cut‐face‐down on the agar.'),
                                 Q(7, 'Why were they placed cut‐face‐down on the agar?')],
      [pt(S('To allow enzymes to diffuse into agar'), 9)], 'bio-2-5', 'cut-face-down',
      rq(6, 'Why seeds cut-face-down on agar:'), 9, stem=[Q9B], fig='q9-plates'),
    T('9bv', 'Q9(b)(v)', 'B', Q9BV,
      [pt(S('Iodine or biuret [must match (b) (i)]', after='To allow enzymes to diffuse into agar'), 9)], 'bio-2-5',
      'testing-the-agar', rq(6, 'Solution poured over agar:'), 9, stem=[Q9B], fig='q9-plates',
      decision='The scheme sets its reprint on the answer\'s own line under a marker printed "(v )"; the answer is '
               'lifted from that line.'),
    T('9bvi', 'Q9(b)(vi)', 'B', Q(7, 'Which substance is shown to be present by the solution named in (v)?'),
      [pt(S('Starch or protein [must match (b) (i)and (b) (v)]'), 9)], 'bio-2-5', 'substance-revealed',
      rq(6, 'Presence of which substance revealed:',
         paired='The scheme rewords "shown to be present" as "Presence ... revealed".'), 9,
      stem=[Q9B, M('(v)', 7), Q9BV], fig='q9-plates'),
    T('9bvii', 'Q9(b)(vii)', 'B', [Q(7, 'Give the results of your investigation.'),
                                   ask(7, 'Untreated seeds – Plate A.', br=True), ask(7, 'Treated seeds – Plate B.', br=True)],
      [pt(S('Clear under seeds', after='Starch or protein'), 9,
          label=S('Result for untreated seeds (batch A):', 'Result for untreated seeds (batch A):',
                  after='Starch or protein')),
       pt(S('Blue-black or violet-purple under seeds [allow no clear patches] [must', 'match (b) (i) and (b) (v)]'), 9,
          label=S('Result for treated seeds (batch B):'))], 'bio-2-5', 'results-of-digestive-activity',
      rq(6, 'Result for untreated seeds (batch A):'), 18, stem=[Q9B], fig='q9-plates',
      decision='One result per plate, a point each: a row each.'),
    # ------------------------------------------------------------ Section C --
] + [
    T(f'10a{r}', f'Q10(a)({r})', 'C', [Q10A, Q(8, *term, br=True)], [pt(S(ans), 7)], 'bio-3-1', concept,
      at(7, 10, '(a)', f'({r})'), 7)
    for r, term, ans, concept in [('i', ('Niche',), 'Role of organism (in its habitat)', 'niche'),
                                  ('ii', ('Aquatic',), '(Factors) relating to water', 'aquatic'),
                                  ('iii', ('Flora.', 'Flora.'), 'Plants', 'flora')]
] + [
    T(f'10b{r}', f'Q10(b)({r})', 'C', q, [row], 'bio-3-1', concept, at(7, 10, '(b)', f'({r})'), total,
      stem=[Q10B], fig='q10-web')
    for r, q, row, concept, total in [
        ('i', Q(8, 'Name one producer from the web.'), pt(S('Grass or blackberry'), 3), 'producer', 3),
        ('ii', Q(8, 'Name one omnivore from the web.'), pt(S('Thrush'), 3), 'omnivore', 3),
        ('iii', Q(8, 'Name one herbivore from the web.'), pt(S('Rabbit or mouse or greenfly'), 3), 'herbivore', 3),
        ('iv', Q(8, 'Explain the term carnivore.'), pt(S('Eats (only) animals'), 3), 'carnivore', 3),
        ('v', Q(8, 'If there was a decline in the number of rabbits, what effect would this have on the',
              'number of foxes?'), pt(S('Decrease'), 3), 'predator-and-prey', 3),
        ('vi', Q(8, 'Suggest two reasons why the number of rabbits might decline.'),
         anyn(S('e.g. Lack of food/ disease'), 2, 3, open_list=True), 'population-decline', 6),
        ('vii', Q(8, 'What is an abiotic factor?'), pt(S('Non-living (factor)'), 3), 'abiotic-factor', 3),
        ('viii', Q(8, 'Give one example of an abiotic factor.'), pt(S('e.g. Temperature'), 3),
         'example-of-an-abiotic-factor', 3)]
] + [
    T(f'10c{r}', f'Q10(c)({r})', 'C', Q(8, q), rows, topic, concept, sq, total, stem=[Q10C], decision=decision)
    for r, q, rows, topic, concept, sq, total, decision in [
        ('i', 'To which kingdom do peacock spiders belong?', [pt(S('Animal (kingdom)'), 3)], 'bio-1-1',
         'animal-kingdom', at(7, 10, '(c)', '(i)'), 3, ''),
        ('ii', 'In what country are the peacock spiders found?', [pt(S('Australia'), 3)], 'bio-3-1',
         'where-peacock-spiders-live', at(7, 10, '(c)', '(ii)'), 3, ''),
        ('iii', 'What is the prey of the peacock spiders?', [pt(S('(Small) insects'), 3)], 'bio-3-1', 'prey',
         at(7, 10, '(c)', '(iii)'), 3, ''),
        ('iv', 'Suggest two ways in which these spiders are adapted to be predators.',
         [anyn(S('Good eyesight'), 2, 3)], 'bio-3-1', 'predator-adaptations',
         rq(7, 'How peacock spiders adapted to be predators:'), 6, ''),
        ('v', 'In what two ways do male peacock spiders attract females?',
         [pt(S('Brightly-coloured abdominal flaps', piece=n), 3) for n in (1, 2)], 'bio-3-1', 'courtship',
         rq(7, 'How peacock spider males attract females:'), 6, TWO_POINTS),
        ('vi', 'What advantage is camouflage to organisms?', [anyn(S('Hide from predators'), 1, 3)], 'bio-3-1',
         'camouflage', at(7, 10, '(c)', '(vi)'), 3,
         'One point, either printed advantage: a menu of the two, claim one.')]
] + [
    T(f'11a{r}', f'Q11(a)({r})', 'C', [Q11A, Q(9, term, br=True)], [pt(S(ans, **kw), 7)], 'bio-1-4', concept, sq, 7,
      decision=decision)
    for r, term, ans, kw, concept, sq, decision in [
        ('i', 'Heredity', 'Passing on characteristics from generation to generation', {}, 'heredity',
         at(7, 11, '(a)', '(i)'), ''),
        ('ii', 'Gene', 'Piece of DNA that codes for a protein', {}, 'gene', at(7, 11, '(a)', '(ii)'), ''),
        ('iii', 'Homozygous.', 'Alleles are the same', {'after': 'Gene: Piece of DNA'}, 'homozygous',
         rq(7, 'Homozygous:'),
         'The scheme prints this part\'s marker as "(ii)" a second time: anchored on its reprint "Homozygous:", '
         'whose answer is on the same line.')]
] + [
    T(f'11bi{n}', f'Q11(b)(i){n}', 'C', Q(9, f'{n}. Which of the above four bases is represented by the letter {x} in the diagram?'),
      [pt(cell(BASES[0], n - 1, BASES[1]), 3)], 'bio-1-2', f'base-{x.lower()}', at(7, 11, '(b)', '(i)'), 3,
      stem=Q11B, fig='q11-dna', labels=labels(BASES[0], 'XY', BASES[1], 7, asked=x), decision=EACH_ITEM)
    for n, x in [(1, 'X'), (2, 'Y')]
] + [
    T(f'11b{r}', f'Q11(b)({r})', 'C', q, [pt(S(ans), 3)], 'bio-1-2', concept, at(7, 11, '(b)', f'({r})'), 3,
      stem=stem, fig='q11-dna')
    for r, q, ans, concept, stem in [
        ('ii', Q(9, 'Chromosomes are made of DNA and which other substance?'), 'Protein', 'chromosome-protein', Q11B),
        ('iii', Q(9, 'How many chromosomes are in a normal human cheek cell?'), '46', 'human-chromosome-number', Q11B),
        ('iv', Q(9, 'Where are chromosomes located in the cell?'), 'Nucleus', 'where-chromosomes-are', Q11B),
        ('v', Q11BV, 'RNA', 'rna', Q11B),
        ('vi', [Q(9, 'In this molecule, uracil replaces one of the four DNA bases mentioned above.'),
                Q(9, 'Which base does uracil replace?')], 'Thymine or T', 'uracil-replaces-thymine',
         Q11B + [M('(v)', 9)] + Q11BV),
        ('vii', [Q(9, 'DNA contains the code for making proteins.'), Q(9, 'Where are proteins made in the cell?')],
         'Ribosome', 'ribosomes', Q11B),
        ('viii', Q(9, 'What molecule carries the DNA code to where proteins are made?'), 'mRNA', 'mrna', Q11B)]
] + [
    T('11ci', 'Q11(c)(i)', 'C', Q(9, 'Give the genotype for a heterozygous plant.'), [pt(S('Tt'), 3)], 'bio-1-4',
      'heterozygous-genotype', at(7, 11, '(c)', '(i)'), 3, stem=[Q11C]),
    T('11cii', 'Q11(c)(ii)', 'C', Q(9, 'Give the genotypes of the gametes of the plant mentioned in (i).'),
      [pt(S('T and t', piece=n, psep=' and '), 3) for n in (1, 2)], 'bio-1-4', 'gametes-of-a-heterozygote',
      at(7, 11, '(c)', '(ii)'), 6, stem=[Q11C, M('(i)', 9), Q(9, 'Give the genotype for a heterozygous plant.')],
      decision=TWO_POINTS),
    T('11ciii', 'Q11(c)(iii)', 'C', Q(9, 'Give the genotype for a small plant.'), [pt(S('tt'), 3)], 'bio-1-4',
      'recessive-genotype', at(7, 11, '(c)', '(iii)'), 3, stem=[Q11C]),
    T('11civ', 'Q11(c)(iv)', 'C', Q(9, 'Give the genotype of a male and the genotype of a female.'),
      [pt(cell(SEXES[0], i, SEXES[1]), 3) for i in (0, 1)], 'bio-1-4', 'sex-chromosomes', at(7, 11, '(c)', '(iv)'), 6,
      stem=[Q11CHUMAN], decision=TWO_POINTS),
    T('11cv', 'Q11(c)(v)', 'C', [Q(9, 'It is often said that the male determines the sex of the child.'),
                                 Q(9, 'Explain fully why this is the case.')],
      [pt(S('Eggs can only be X [If no gametes mentioned, max. 1 pt]', piece=1, psep=' ['), 3,
          note_sel=S('Eggs can only be X [If no gametes mentioned, max. 1 pt]', piece=[2, 1], psep=[' [', ']'])),
       pt(S('Sperms can be X or Y'), 3)], 'bio-1-4', 'sex-determination',
      rq(7, "Why/ how males determine child's sex:", paired=COMPRESSED), 6, stem=[Q11CHUMAN],
      decision='Two points, a row each; the scheme\'s bracketed direction (at most one point without gametes) is '
               'the first row\'s note.'),
    T('12ai', 'Q12(a)(i)', 'C', Q(10, 'Name the two main types of vascular tissue in flowering plants.'),
      [pt(S('Xylem and phloem', piece=n, psep=' and '), 7) for n in (1, 2)], 'bio-2-6', 'vascular-tissue',
      at(8, 12, '(a)', '(i)'), 14, stem=[Q12A],
      decision='Two points on the ladder ("7 + 2(1)"), printed "Xylem and phloem": a row each.'),
    T('12aii', 'Q12(a)(ii)', 'C', Q(10, 'Which tissue carries water?', 'Which tissue carries water?'),
      [pt(S('Xylem'), 7)], 'bio-2-6', 'xylem', at(8, 12, '(a)', '(ii)'), 7, stem=[Q12A]),
] + [
    T(f'12bi{n}', f'Q12(b)(i){n}', 'C',
      [Q12BI, Q(10, '1. Aorta; 2. Hepatic portal vein; 3. Pulmonary vein; 4. Vena cava.', piece=n, psep='; ', br=True)],
      [pt(S(start, piece=1, psep=seps[0]) if len(seps) > 1 else S(start), 3)], 'bio-2-6', concept,
      at(8, 12, '(b)', '(i)'), 3, stem=[Q12B], fig='q12-circulation', labels=vessel_labels(letter),
      decision=EACH_ITEM + ' "4(3)": 3 for each.')
    for n, (letter, start, seps), concept in zip((1, 2, 3, 4), VESSELS,
                                                 ('aorta', 'hepatic-portal-vein', 'pulmonary-vein', 'vena-cava'))
] + [
    T(f'12bii{n}', f'Q12(b)(ii){n}', 'C', [Q12BII, Q(10, item, br=True)], [pt(S(*ans), 6)], 'bio-2-6', concept,
      rq(8, sq), 6, stem=[Q12B], fig='q12-circulation',
      decision='"6 + 3" over the two numbered items: the first correct answer earns 6, the next 3; each item is '
               'carded at the first rate.')
    for n, item, ans, concept, sq in [
        (1, '1. The lungs', ('Oxygen gained or carbon dioxide lost or water lost',), 'blood-through-the-lungs',
         '1. Changes to blood passing through lungs:'),
        (2, '2. The kidneys.', ('Carbon dioxide gained or oxygen lost or urea lost or water lost (or',
                                'gained) or salt lost (or gained)'), 'blood-through-the-kidneys',
         '2. Changes to blood passing through kidneys:')]
] + [
    T('12biii', 'Q12(b)(iii)', 'C', Q(10, 'Name or give the letter from the diagram of one blood vessel that is rich in oxygen.'),
      [pt(S('Pulmonary vein or D or aorta or E or renal artery or G'), 3)], 'bio-2-6', 'oxygenated-blood-vessels',
      rq(8, 'Vessel containing oxygen-rich blood:'), 3, stem=[Q12B], fig='q12-circulation'),
    T('12biv', 'Q12(b)(iv)', 'C', [Q(10, 'The human circulatory system is said to be a closed system.'),
                                   ask(10, 'What is meant by a closed circulatory system?')],
      [pt(S('Blood circulates (or always) in vessels'), 3)], 'bio-2-6', 'closed-circulation',
      rq(8, 'Closed circulatory system:'), 3, stem=[Q12B], fig='q12-circulation'),
] + [
    T(f'12ci-{x.lower()}', 'Q12(c)(i)', 'C', Q(10, 'Name the parts labelled A, B, C.'), [pt(cell(SKIN[0], i, SKIN[1]), 3)],
      'bio-2-4', concept, at(8, 12, '(c)', '(i)'), 3, stem=[Q12C], fig='q12-skin', item=(x.lower(), x),
      labels=labels(SKIN[0], 'ABC', SKIN[1], 8, asked=x), decision=EACH_ITEM)
    for i, (x, concept) in enumerate([('A', 'hair'), ('B', 'skin-blood-vessels'), ('C', 'sweat-gland')])
] + [
    T(f'12cii-{x.lower()}', 'Q12(c)(ii)', 'C', [Q(10, 'A function of the skin is to maintain a constant body temperature.'),
                                               Q(10, 'Give one role of each of the three parts A, B, C, in cooling the body on a warm day.')],
      [pt(sel, 3)], 'bio-2-4', concept, at(8, 12, '(c)', '(ii)'), 3, stem=[Q12C], fig='q12-skin', item=(x.lower(), x),
      labels=labels(SKIN[0], 'ABC', SKIN[1], 8),
      decision=EACH_ITEM + ' The scheme runs its third heading on from the second line ("... dilate Role of").')
    for x, sel, concept in [
        ('A', S('Role of hair in cooling body:Hairs lie flat', piece=2, psep=':'), 'hair-in-cooling'),
        ('B', S('Blood vessels dilate', piece=1, psep=' Role of'), 'vasodilation'),
        ('C', S('Sweat glands make sweat'), 'sweating')]
] + [
    T('12ciii', 'Q12(c)(iii)', 'C', ask(10, 'Give two other functions of the skin.'),
      [anyn(S('Prevents water loss/ prevents pathogen entry/ sense organ/', 'Any two'), 2, 3)], 'bio-2-4',
      'functions-of-the-skin', rq(8, 'Two other skin functions:'), 6, stem=[Q12C], fig='q12-skin'),
] + [
    T(f'13a{r}', f'Q13(a)({r})', 'C', [Q13A, Q(11, *term, br=True)], [pt(S(ans), 7)], 'bio-1-3', concept,
      at(8, 13, '(a)', f'({r})'), 7)
    for r, term, ans, concept in [('i', ('Photosynthesis',), 'Chloroplast', 'chloroplast'),
                                  ('ii', ('Aerobic respiration',), 'Mitochondrion', 'mitochondrion'),
                                  ('iii', ('Anaerobic respiration.', 'Anaerobic respiration.'), 'Cytoplasm',
                                   'cytoplasm')]
] + [
    T(f'13b{r}', f'13b{r}' and f'Q13(b)({r})', 'C', q, rows, topic, concept, sq, total, stem=[Q13B],
      fig='q13-equation')
    for r, q, rows, topic, concept, sq, total in [
        ('i', Q(11, 'Name the gas X.'), [pt(S('Gas X = Carbon dioxide'), 3)], 'bio-2-2', 'carbon-dioxide',
         at(8, 13, '(b)', '(i)'), 3),
        ('ii', Q(11, 'Name substance Y.'), [pt(S('Substance Y = Glucose'), 3)], 'bio-2-2', 'glucose',
         at(8, 13, '(b)', '(ii)'), 3),
        ('iii', Q(11, 'What is the main source of energy for photosynthesis?'), [pt(S('Light'), 3)], 'bio-2-2',
         'light-energy', at(8, 13, '(b)', '(iii)'), 3),
        ('iv', [Q(11, 'Chlorophyll is used to trap energy in the plant.'), Q(11, 'What colour is chlorophyll?')],
         [pt(S('Green'), 3)], 'bio-2-2', 'chlorophyll', at(8, 13, '(b)', '(iv)'), 3),
        ('v', Q(11, 'What happens to the oxygen that is formed in photosynthesis?'),
         [pt(S('Respired or enters atmosphere'), 3)], 'bio-2-2', 'fate-of-oxygen', at(8, 13, '(b)', '(v)'), 3),
        ('vi', Q(11, 'Name two environmental factors that may affect the rate of photosynthesis.'),
         [anyn(None, 2, 3, open_list=True,
               options=[S('e.g. Temperature', piece=1), S('e.g. Temperature', piece=2), S('e.g. Temperature', piece=3),
                        S('e.g. Temperature', piece=[4, 1], psep=['/', ' Any two'])])], 'bio-2-2',
         'rate-of-photosynthesis', rq(8, 'Environmental factors affecting the rate of photosynthesis:'), 6),
        ('vii', Q(11, 'Through which part of the plant does gas X enter?'), [pt(S('Stoma(ta)'), 3)], 'bio-2-2',
         'stomata', at(8, 13, '(b)', '(vii)'), 3),
        ('viii', Q(11, 'Name the process by which water enters the plant.', 'Name the process by which water enters the plant.'),
         [pt(S('Osmosis'), 3)], 'bio-2-6', 'osmosis', at(8, 13, '(b)', '(viii)'), 3)]
] + [
    T(f'13c{r}', f'Q13(c)({r})', 'C', q, rows, 'bio-2-2', concept, at(8, 13, '(c )', f'({r})'), total, stem=stem,
      decision=decision)
    for r, q, rows, concept, total, stem, decision in [
        ('i', Q(11, 'Explain the term respiration.'),
         [pt(S('Release of energy', piece=1), 3), pt(S('Release of energy', piece=[2, 1], psep=['/', ' (2 pts)']), 3)],
         'respiration', 6, [], TWO_POINTS),
        ('ii', Q(11, 'Why is aerobic respiration considered to be more efficient than anaerobic', 'respiration?'),
         [pt(S('Releases more energy'), 3)], 'aerobic-efficiency', 3, [], ''),
        ('iii', Q13CIII, [pt(S('Yeast'), 3)], 'yeast', 3, [], ''),
        ('iv', Q(11, 'Name the two molecules produced by this fermentation.'),
         [pt(S('Ethanol', piece=1), 3), pt(S('Ethanol', piece=[2, 1], psep=['/', ' (2 pts)']), 3)],
         'products-of-fermentation', 6, [M('(iii)', 11)] + Q13CIII, TWO_POINTS),
        ('v', [Q(11, 'Cramps may be caused by the absence of gas G in muscle cells.'), Q(11, 'Name gas G.')],
         [pt(S('Oxygen'), 3)], 'oxygen-and-cramps', 3, [], ''),
        ('vi', [Q(11, 'Cramps may be caused by the presence of substance S in muscle cells.'), Q(11, 'Name substance S.')],
         [pt(S('Lactic acid'), 3)], 'lactic-acid', 3, [], '')]
] + [
    T(f'14a{r}', f'Q14(a)({r})', 'C', Q(12, f'Name the part labelled {x} and give its function.'),
      [pt(S(line, piece=n), 3) for n in (1, 2)], 'bio-2-4', concept, at(9, 14, '(a)', f'({r})'), 6, stem=[Q14A],
      fig='q14-ear', labels=ear_labels(x), decision='The part and its function, a point each: a row each.')
    for r, x, line, concept in zip(('i', 'ii', 'iii'), 'ABC', EAR,
                                   ('semicircular-canals', 'cochlea', 'eardrum'))
] + [
    T('14aiv', 'Q14(a)(iv)', 'C', Q(12, 'What is connected to the middle ear by the Eustachian tube?'),
      [pt(S('Throat'), 3)], 'bio-2-4', 'eustachian-tube', at(9, 14, '(a)', '(iv)'), 3, stem=[Q14A], fig='q14-ear'),
    T('14av', 'Q14(a)(v)', 'C', Q(12, 'To which organ does the auditory nerve connect the ear?'),
      [pt(S('Brain'), 3)], 'bio-2-4', 'auditory-nerve', at(9, 14, '(a)', '(v)'), 3, stem=[Q14A], fig='q14-ear'),
    T('14avi', 'Q14(a)(vi)', 'C', Q(12, 'State how any named disorder of the ear or of the eye may be corrected.'),
      [pt(S('e.g. Long-sightedness or short-sightedness or hearing loss or glue ear'), 3,
          label=S('Disorder of eye or of ear:')),
       pt(S('e.g. Convex lens for long-sightedness or concave lens for', 'grommets for glue ear'), 3,
          label=S('Disorder correction:'))], 'bio-2-4', 'ear-and-eye-disorders', at(9, 14, '(a)', '(vi)'), 6,
      stem=[Q14A], fig='q14-ear',
      decision='Ear or eye: one disorder row and one correction row for either, so one card.'),
    T('14bi', 'Q14(b)(i)', 'C', Q(12, 'Edward Jenner discovered a vaccination against which disease?'),
      [pt(S('Smallpox'), 3)], 'bio-2-4', 'smallpox', at(9, 14, '(b)', '(i)'), 3, stem=[Q14B]),
    T('14bii', 'Q14(b)(ii)', 'C', Q(12, 'Explain what we now understand about how vaccination works.'),
      [anyn(S('Non-disease-causing/ (dose of a) pathogen/ stimulates immune', 'Any three'), 3, 3)], 'bio-2-4',
      'vaccination', rq(9, 'How vaccination works:'), 9, stem=[Q14B]),
    T('14biii', 'Q14(b)(iii)', 'C', Q(12, 'What is meant by the term immunity?'),
      [pt(S('Ability of the body to resist infection'), 3)], 'bio-2-4', 'immunity', at(9, 14, '(b)', '(iii)'), 3,
      stem=[Q14B]),
    T('14biv', 'Q14(b)(iv)', 'C', Q(12, 'Outline the difference between active immunity and passive immunity.'),
      [pt(S('Active immunity:'), 3), pt(S('Passive immunity:'), 3)], 'bio-2-4', 'active-and-passive-immunity',
      at(9, 14, '(b)', '(iv)'), 6, stem=[Q14B], decision='One point for each kind of immunity: a row each.'),
    T('14bv', 'Q14(b)(v)', 'C', Q(12, 'What is a pathogen?'), [pt(S('Disease-causing organism'), 3)], 'bio-2-4',
      'pathogen', at(9, 14, '(b)', '(v)'), 3, stem=[Q14B]),
    T('14bvi', 'Q14(b)(vi)', 'C', [Q(12, 'Colostrum is the first milk a baby gets from its mother.'),
                                   Q(12, 'How does colostrum help to protect the baby from disease?')],
      [anyn(S('Contains antibodies/ contains lymphocytes/ nutritional boost', 'Any two'), 2, 3)], 'bio-2-4',
      'colostrum', rq(9, 'How colostrum protects babies from disease:'), 6, stem=[Q14B]),
] + [
    T(f'14ci-{slug}', 'Q14(c)(i)', 'C', Q14CI, [pt(cell(TEETH[0], i, TEETH[1]), 3)], 'bio-2-6', slug,
      at(9, 14, '(c )', '(i)'), 3, stem=[Q14C], fig='q14-mouth', item=(slug, name), labels=tooth_labels(letter),
      decision=EACH_ITEM + ' "(4 pts)": 3 for each.')
    for i, (slug, name, letter) in enumerate([('canine', 'Canine', 'C'), ('molar', 'Molar', 'A'),
                                              ('incisor', 'Incisor', 'D'), ('premolar', 'Pre-molar', 'B')])
] + [
    T('14cii', 'Q14(c)(ii)', 'C', Q(13, 'Give the full dental formula for an adult human.'),
      [pt(S('i2. c1. pm2. m3 [Format correct: 1 pt]'), 3), pt(S('i2. c1. pm2. m3 [Numbers correct: 1 pt]'), 3)],
      'bio-2-6', 'dental-formula', rq(9, 'Full dental formula for adult human:'), 6, stem=[Q14C], fig='q14-mouth',
      decision='The scheme prints the formula on two lines, the first underlined (one jaw over the other), and '
               'prices its format and its numbers at a point each: a row each, as printed.'),
    T('14ciii', 'Q14(c)(iii)', 'C', Q14CIII, [pt(S('Canine [allow molar]'), 3)], 'bio-2-6', 'canines-in-dogs',
      at(9, 14, '(c )', '(iii)'), 3, stem=[Q14C] + Q14CI[1:], fig='q14-mouth'),
    T('14civ', 'Q14(c)(iv)', 'C', Q(13, 'Give a reason for your answer to part (iii).'),
      [pt(S('To tear (flesh or meat) [if molar in (iii), allow to crush bones]'), 3)], 'bio-2-6', 'why-dogs-have-canines',
      rq(9, 'Why type of tooth is larger in dogs:'), 3, stem=[Q14C, M('(iii)', 13), Q14CIII], fig='q14-mouth'),
    T('14cv1', 'Q14(c)(v)1', 'C', Q(13, '1. Name the liquid.'), [pt(S('Saliva', piece=1, psep=' 2.'), 3)], 'bio-2-6',
      'saliva', at(9, 14, '(c )', '(v)'), 3, stem=[Q14C, Q14CV], fig='q14-mouth', decision=EACH_ITEM),
    T('14cv2', 'Q14(c)(v)2', 'C', Q(13, '2. Name the enzyme the liquid contains.'), [pt(S('Amylase'), 3)], 'bio-2-6',
      'amylase', at(9, 14, '(c )', '(v)'), 3, stem=[Q14C, Q14CV], fig='q14-mouth',
      decision=EACH_ITEM + ' The scheme sets item 2\'s number at the end of item 1\'s line.'),
] + [
    T(f'15ai-{x.lower()}', 'Q15(a)(i)', 'C', Q(14, 'Name the parts labelled A, B, C.'),
      [pt(cell(FLOWER[0], i, FLOWER[1]), 3)], 'bio-2-5', concept, at(10, 15, '(a)', '(i)'), 3, stem=[Q15A],
      fig='q15-flower', item=(x.lower(), x), labels=labels(FLOWER[0], 'ABC', FLOWER[1], 10, asked=x),
      decision=EACH_ITEM)
    for i, (x, concept) in enumerate([('A', 'stigma'), ('B', 'anther'), ('C', 'ovary')])
] + [
    T('15aii', 'Q15(a)(ii)', 'C', Q(14, 'What substance produced by flowers causes hay fever in some people?'),
      [pt(S('Pollen'), 3)], 'bio-2-5', 'pollen-and-hay-fever', at(10, 15, '(a)', '(ii)'), 3, stem=[Q15A],
      fig='q15-flower'),
    T('15aiii', 'Q15(a)(iii)', 'C', Q(14, 'Which labelled part will contain the seeds?'),
      [pt(S('C or ovary (or ovule)'), 3)], 'bio-2-5', 'where-seeds-form', at(10, 15, '(a)', '(iii)'), 3, stem=[Q15A],
      fig='q15-flower'),
    T('15aiv1', 'Q15(a)(iv)1', 'C', Q(14, '1. Explain the term dormancy.'),
      [pt(S('Period of no germination or no growth (after dispersal, despite',
            'conditions necessary for germination being present)'), 3)], 'bio-2-5', 'dormancy',
      rq(10, '1. Dormancy:'), 3, stem=[Q15A, Q15AIV], fig='q15-flower', decision=EACH_ITEM),
    T('15aiv2', 'Q15(a)(iv)2', 'C', Q(14, '2. Give two advantages of dormancy.'),
      [anyn(S('adverse conditions/ winter or cold/ drought/', 'waterlogging'), 2, 3,
            note_sel=S('Ability to survive:', 'Ability to survive:'))], 'bio-2-5', 'advantages-of-dormancy',
      rq(10, '2. Advantages of dormancy:'), 6, stem=[Q15A, Q15AIV], fig='q15-flower',
      decision=EACH_ITEM + ' The scheme heads the menu "Ability to survive:"; it is the row\'s note.'),
    T('15av1', 'Q15(a)(v)1', 'C', Q(14, '1. Give one example of a seedless fruit.'), [pt(S('e.g. Grapes'), 3)],
      'bio-2-5', 'seedless-fruit', at(10, 15, '(a)', '(v)'), 3, stem=[Q15A, Q15AV], fig='q15-flower',
      decision=EACH_ITEM),
    T('15av2', 'Q15(a)(v)2', 'C', Q(14, '2. Suggest one advantage of seedless fruits.'),
      [anyn(S('Allows artificial control of development/ more energy for fruit/ easier', 'Any one'), 1, 3)], 'bio-2-5',
      'advantages-of-seedless-fruit', rq(10, '2. Advantage of seedless fruits:'), 3, stem=[Q15A, Q15AV],
      fig='q15-flower', decision=EACH_ITEM),
] + [
    T(f'15bi-{x.lower()}', 'Q15(b)(i)', 'C', Q(14, 'Name the parts labelled A, B, C.', after='The diagram shows a transverse'),
      [pt(cell(ROOT[0], i, ROOT[1]), 3)], 'bio-2-6', concept, at(10, 15, '(b)', '(i)'), 3, stem=[Q15B],
      fig='q15-root', item=(x.lower(), x), labels=labels(ROOT[0], 'ABC', ROOT[1], 10, asked=x), decision=EACH_ITEM)
    for i, (x, concept) in enumerate([('A', 'root-phloem'), ('B', 'root-xylem'), ('C', 'root-hair')])
] + [
    T('15bii', 'Q15(b)(ii)', 'C', Q(14, 'Give one example of a root modified for food storage.'),
      [pt(S('e.g. Carrot'), 3)], 'bio-2-6', 'storage-roots', at(10, 15, '(b)', '(ii)'), 3, stem=[Q15B],
      fig='q15-root'),
    T('15biii', 'Q15(b)(iii)', 'C', Q(14, 'Other than food storage, state two functions of roots.'),
      [anyn(S('To absorb water (or minerals)/ to anchor plant/ asexual reproduction'), 2, 3)], 'bio-2-6',
      'functions-of-roots', rq(10, 'Other root functions:'), 6, stem=[Q15B], fig='q15-root'),
    T('15biv', 'Q15(b)(iv)', 'C', Q(14, 'What is the first root called that grows from a seed?'),
      [pt(S('Radicle'), 3)], 'bio-2-6', 'radicle', at(10, 15, '(b)', '(iv)'), 3, stem=[Q15B], fig='q15-root'),
    T('15bv', 'Q15(b)(v)', 'C', [Q(14, 'Flowering plants can be monocotyledonous (monocot) or dicotyledonous (dicot).'),
                                 Q(14, 'Give any one difference between a monocot plant and a dicot plant.')],
      [pt(S('e.g. Monocot has parallel veins, dicot has network of veins'), 3)], 'bio-2-6', 'monocots-and-dicots',
      rq(10, 'Difference between monocot and dicot:'), 3, stem=[Q15B], fig='q15-root'),
    T('15bvi', 'Q15(b)(vi)', 'C', Q(14, 'Give one example of a monocot plant and one example of a dicot plant.'),
      [anyn(S('e.g. Grass/ tulip/ daffodil'), 1, 3, open_list=True, note_sel=S('Monocot plant:', 'Monocot plant:')),
       anyn(S('e.g. Oak/ laurel/ rose'), 1, 3, open_list=True, note_sel=S('Dicot plant:', 'Dicot plant:'))],
      'bio-2-6', 'monocot-and-dicot-examples', at(10, 15, '(b)', '(vi)'), 6, stem=[Q15B], fig='q15-root',
      decision='One point for each plant, any one of its printed examples: a menu each, its heading the note.'),
    T('15ci', 'Q15(c)(i)', 'C', Q(15, 'What are tropisms?'),
      [pt(S('Growth responses of plants', piece=n), 3) for n in (1, 2)], 'bio-2-4', 'tropisms',
      at(10, 15, '(c)', '(i)'), 6, fig='q15-tropism', decision=TWO_POINTS),
    T('15cii', 'Q15(c)(ii)', 'C', Q(15, 'Which tropism is shown in the above diagram?'), [pt(S('Phototropism'), 3)],
      'bio-2-4', 'phototropism', at(10, 15, '(c)', '(ii)'), 3, fig='q15-tropism'),
    T('15ciii', 'Q15(c)(iii)', 'C', Q(15, 'Name one factor to which plants respond, other than light.'),
      [pt(S('Water or gravity or touch or chemicals'), 3)], 'bio-2-4', 'plant-stimuli', at(10, 15, '(c)', '(iii)'), 3,
      fig='q15-tropism'),
    T('15civ', 'Q15(c)(iv)', 'C', Q(15, 'Name one growth regulator in plants.'), [pt(S('e.g. Auxin'), 3)], 'bio-2-4',
      'growth-regulators', at(10, 15, '(c)', '(iv)'), 3, fig='q15-tropism'),
    T('15cv', 'Q15(c)(v)', 'C', Q(15, 'State two uses in horticulture of artificial growth regulators.'),
      [anyn(S('e.g. rooting powder'), 2, 3, open_list=True)], 'bio-2-4', 'uses-of-growth-regulators',
      rq(10, 'Uses of artificial growth regulators:'), 6, fig='q15-tropism'),
    T('15cvi', 'Q15(c)(vi)', 'C', Q(15, 'How do thorns protect some plants?'),
      [pt(S('Discourage animals from eating them'), 3)], 'bio-2-4', 'thorns', at(10, 15, '(c)', '(vi)'), 3,
      fig='q15-tropism'),
    T('15cvii', 'Q15(c)(vii)', 'C', Q(15, 'Give two other features that plants use to protect themselves.'),
      [anyn(None, 2, 3, open_list=True,
            options=[S('e.g. Stings', piece=1), S('e.g. Stings', piece=2),
                     S('e.g. Stings', piece=[3, 1], psep=['/', ' Any two'])])], 'bio-2-4', 'plant-defences',
      at(10, 15, '(c)', '(vii)'), 6, fig='q15-tropism'),
]

# Section C (b) and (c) of Q10-Q13 are fixed points beside their question's
# "7 + 2(1)" ladder: their units count to it as fixed, their cards keep their
# own marks.
LADDER_EXEMPT = {t['key'] for t in TASKS if t['sec'] == 'C' and t['key'][:2] in ('10', '11', '12', '13')
                 and t['key'][2] in 'bc' and t['key'] not in LADDER_OF}

FIGURES = {
    # key suffix: (doc, page, rect in PDF points, credit, letters, alt, solution)
    'q2-joint': ('paper', 2, (165, 338, 345, 486), SEC, ['A', 'B', 'C'], 'Drawing of a synovial joint: the rounded ends of two bones meet inside a covering. A points to the covering on the left, B to the dark layer on the end of the upper bone, C into the space between the two bone ends.', False),
    'q3-table': ('paper', 3, (30, 54, 552, 334), SEC, [], 'Question 3 as printed: the instruction, then the list Immobilised (struck through), Washing powder, Alginate, Calcium chloride, Reusable, Pectinase above a two-column table: Column A lists "Enzyme trapped in a gel" (answered Immobilised) and parts (a) to (e); Column B is blank.', False),
    'q4-male': ('paper', 3, (155, 400, 478, 552), SEC, ['A', 'B', 'C'], 'Side view of the human male reproductive system. A points to the outer organ at the front, B to the oval body at the bottom, C to a tube running below the bladder.', False),
    'q6-cell': ('paper', 4, (190, 333, 350, 478), SEC, ['A', 'B', 'C', 'D', 'E'], 'Diagram of a plant cell: a rounded rectangle with a grey outer layer, oval bodies around its edge, a large black circle and a large clear space. A and B point to the edge of the cell, at the top left corner and on the right; C points to an oval body beside the clear space, D into the clear space and E to the black circle.', False),
    'q7-table': ('paper', 5, (148, 538, 500, 640), SEC, ['A', 'B'], 'Table of breaths per minute: Student A, 14 before exercise and 17 after; Student B, 15 before exercise and 35 after.', False),
    'q9-plates': ('paper', 7, (105, 156, 530, 254), SEC, ['A', 'B'], 'Two Petri dishes, A and B, each holding agar with four seed halves on it; Seed and Agar are labelled on each dish.', False),
    'q10-web': ('paper', 8, (95, 205, 470, 375), SEC, [], 'Food web: Grass to Rabbit; Rabbit to Fox and to Owl; Blackberry to Mouse, to Greenfly and to Thrush; Mouse to Owl and to Hawk; Greenfly to Thrush; Thrush to Hawk.', False),
    'q11-dna': ('paper', 9, (180, 150, 415, 324), SEC, ['X', 'Y'], 'Part of a DNA molecule: two strands of pentagons marked S and circles marked P, joined across by three pairs of boxes: X with T, Y with C, and T with X.', False),
    'q12-circulation': ('paper', 10, (185, 146, 410, 390), SEC, ['D', 'E', 'F', 'G', 'H', 'I', 'J', 'K'], 'Diagram of the human circulatory system: the heart in the middle, with vessels to and from the head, lungs, liver, intestine, kidneys and legs. K and D label vessels at the lungs, J and E vessels at the heart, I and F vessels at the liver and intestine, H and G vessels at the kidneys.',
                        False),
    'q12-skin': ('paper', 10, (186, 549, 409, 731), SEC, ['A', 'B', 'C'], 'Section through human skin. A points to a long dark shaft rising from a bulb deep in the skin, B to a small looped structure just below the surface layer, C to a coiled tube deep in the skin with a duct running up to the surface.', False),
    'q13-equation': ('paper', 11, (172, 158, 322, 180), SEC, ['X', 'Y'], 'The equation as printed: Water + X, an arrow, Y + Oxygen.', False),
    'q14-ear': ('paper', 12, (130, 98, 462, 287), SEC, ['A', 'B', 'C'], 'Diagram of the human ear with Middle ear, Auditory nerve and Eustachian tube labelled. A points to the looped structures at the top of the inner ear, B to the coiled structure below them, C to the inner end of the ear canal.', False),
    'q14-mouth': ('paper', 13, (190, 66, 405, 298), SEC, ['A', 'B', 'C', 'D'], 'An open human mouth showing the upper and lower teeth, the tongue and the throat. Gum is labelled; A, B, C and D point to four teeth of the lower jaw, from the back (A) towards the front (D).', False),
    'q15-flower': ('paper', 14, (163, 88, 362, 244), SEC, ['A', 'B', 'C', 'D'], 'Section through a flower. A points to the tip of the long central stalk, B to the head of one of the shorter stalks around it, C to the swollen base of the central structure, which holds small round bodies, D to a small leaf-like part below the petals.', False),
    'q15-root': ('paper', 14, (210, 462, 425, 566), SEC, ['A', 'B', 'C'], 'Transverse section of a dicot root: a circle with a cross-shaped core and four small round patches between its arms, and thin outgrowths from its outside. A points to one of the round patches, B to the cross-shaped core, C to one of the outgrowths.', False),
    'q15-tropism': ('paper', 15, (168, 60, 426, 222), SEC, [], 'A plant shoot, labelled, rising from the soil and curving over to the right; arrows labelled Light direction point at it from the right.', False),
}
