"""Biology 2019 Ordinary Level — reviewed task ledger, carded from the papers for the first time.

Independent visual sweep (2026-10-24), every page rendered and read:
  * LC025GLP038EV (Sections A and B), 8 pages: p1 cover, p2 instructions,
    p3-p5 Section A Questions 1-6, p6-p8 Section B Questions 7-9 (p8 is the
    booklet's back page and also carries the "Section C of this paper is
    supplied separately" notice). Section C was answered in a separate
    answerbook, so the booklet has no Section C answer pages.
  * LC025GLP040EV (Section C), 12 pages: p1 cover, p2 instructions, p3-p9
    Questions 10-15, p10-p11 "There is no examination material on this page",
    p12 back cover with the same notice.
  * LC025GLP000EV (marking scheme), 20 pages: p1 cover, p2 note, p3
    introduction, cancelled and surplus answers, p4 surplus answers continued
    and the marking scheme conventions, p5 annotations (one, a tick with a
    small "i", is "Correct response in Q9(b)(i) only"), p6-p18 Questions 1-15,
    p19 blank, p20 back cover.

The paper's shape: any five of Section A's six questions, any two of Section
B's three (the rubric: "Part (a) carries 6 marks and part (b) carries 24
marks"), any four of Section C's six; Q14 and Q15 are each any two of (a),
(b), (c) at "(30, 30)". Every printed question is carded. No Biology card
existed for 2019 Ordinary before this review.

Tariffs are the scheme's ordered splits, printed at question or part heads and
carded at their first rate: Q1 and Q3 "6 + 6 + 4 + 2 + 2" (five responses),
Q2, Q4, Q5, Q6 "6 + 6 + 4 + 4(1)" (seven), every Section B (a) "4 + 2", Q8(b)
"6 + 6 + 6 + 2 + 4(1)", Section C (a) "7 + 1 + 1" or "7 + 2(1)", (b) "9 + 9 + 3
+ 6(1)", Q14(b) "3 (6) + 4 (3)", Q15(a) and (b) "6 + 8(3)". Q10(c) and Q12(c)
print "8 X 3", eight responses at 3.

Seven parts print their answers but no per-response tariff the printed answers
fit, and each is carded as ONE whole-part task at its printed total, every row
unpriced (tariff='questionTotal', the coordinator's decision for this sitting):
Q7(b) 24 ("Drawing (3) + Labels - 3(3)" then "9 + 3(1)", which fits (ii)-(iv)
only if (iii)'s one answer counts twice), Q9(b) 24 ("Drawing (3) / Labels -
3(1)" prices (i) only), Q11(c) 24 ("8 X 3" prices eight responses, the scheme
prints seven), Q13(c) 24 (no tariff printed), Q14(a) 30 ("Drawing (3) / Labels
2(3)" prices (i) only), Q14(c) 30 (no tariff printed) and Q15(c) 30 ("6 +
8(3)" prices nine responses, the scheme prints eight).

Every question total is checked by the runner: a whole-part card adds its printed
total to its question's ladders. Q14 and Q15 are any two of three 30-mark parts:
their three parts make 90.

No printed choice is marked differently per option: Q7(b)'s light intensity or
carbon dioxide is answered by one set of answers ("Moved lamp or varied conc.
of NaHCO3 solution"), so there are no routes.
"""
from bio_review_lib import Q, SQ, S, M, pt, anyn, T, L

YEAR, LEVEL = 2019, 'ol'
REVIEWED_AT = '2026-10-24'

SOURCES = {
    '038': {'path': 'examiner-reports/biology/papers/2019-ol-038-paper.pdf',
            'fileid': 'LC025GLP038EV.pdf',
            'sha256': 'eccab6177a2648fc4f43fe6abfd80ff2e90b9c783bb51e20bb22d7e935367dea',
            'pages': 8},
    '040': {'path': 'examiner-reports/biology/papers/2019-ol-040-paper.pdf',
            'fileid': 'LC025GLP040EV.pdf',
            'sha256': 'cf8883d997fd914ef70eef2e25bb909556ddc776c3fc2b96cfab1cbde3754df8',
            'pages': 12},
    'scheme': {'path': 'examiner-reports/biology/schemes/2019-ol.pdf',
               'fileid': 'LC025GLP000EV.pdf',
               'sha256': '99ab1b9e15d04082c23467c2746761a722daf082313da0c4092a78aeb0e3f9b5',
               'pages': 20},
}

PAGE_ROLES = {
    '038': {1: 'cover', 2: 'instructions', **{p: 'questions' for p in range(3, 9)}},
    '040': {1: 'cover', 2: 'instructions', **{p: 'questions' for p in range(3, 10)},
            10: 'blank', 11: 'blank', 12: 'back-cover'},
    'scheme': {1: 'cover', 2: 'note', 3: 'introduction', 4: 'conventions', 5: 'annotations',
               **{p: 'marking' for p in range(6, 19)}, 19: 'blank', 20: 'back-cover'},
}


def _ladder(notation):
    """An ordered split as the scheme prints it ("6 + 6 + 4 + 4(1)", "3 (6) + 4 (3)")."""
    steps = []
    for term in notation.split('+'):
        n, _, m = term.strip().partition('(')
        steps += [int(m.rstrip(')'))] * int(n) if m else [int(n)]
    return {'steps': steps, 'notation': notation}


QUESTION_TOTALS = {**{n: 20 for n in range(1, 7)}, **{n: 30 for n in (7, 8, 9)},
                   **{n: 60 for n in range(10, 14)}, 14: 90, 15: 90}   # Q14, Q15: any two of three 30s
PART_TOTALS = {
    (7, 'b'): 24, (9, 'b'): 24,                       # Section B rubric: "part (b) carries 24 marks"
    (10, 'c'): 24, (11, 'c'): 24, (12, 'c'): 24, (13, 'c'): 24,
    (14, 'a'): 30, (14, 'c'): 30, (15, 'c'): 30,      # "(30, 30)"
}

LADDERS = {
    1: _ladder('6 + 6 + 4 + 2 + 2'), 3: _ladder('6 + 6 + 4 + 2 +2'),
    **{q: _ladder('6 + 6 + 4 + 4(1)') for q in (2, 4, 5, 6)},
    **{(n, 'a'): _ladder('4 + 2') for n in (7, 8, 9)},
    (8, 'b'): _ladder('6 + 6 + 6 + 2 + 4(1)'),
    (10, 'a'): _ladder('7 +1 + 1'), (11, 'a'): _ladder('7 + 1 + 1'),
    (12, 'a'): _ladder('7 + 2(1)'), (13, 'a'): _ladder('7 + 2(1)'),
    **{(n, 'b'): _ladder('9 + 9 + 3 + 6(1)') for n in (10, 11, 12, 13)},
    # "8 X 3": eight responses at 3, a flat rate (no notation, so the cards
    # keep their fixed marks); listed so Q10 and Q12 add up to their 60.
    (10, 'c'): [3] * 8, (12, 'c'): [3] * 8,
    (14, 'b'): _ladder('3 (6) + 4 (3)'),
    (15, 'a'): _ladder('6 + 8(3)'), (15, 'b'): _ladder('6 + 8(3)'),
}

CHECKSUMS = {
    1: {6: 5}, 3: {6: 5}, **{q: {6: 7} for q in (2, 4, 5, 6)},
    **{(n, 'a'): {4: 2} for n in (7, 8, 9)}, (8, 'b'): {6: 8},
    **{(n, 'a'): {7: 3} for n in (10, 11, 12, 13)},
    **{(n, 'b'): {9: 9} for n in (10, 11, 12, 13)},
    (10, 'c'): {3: 8}, (12, 'c'): {3: 8},
    (14, 'b'): {6: 7}, (15, 'a'): {6: 9}, (15, 'b'): {6: 9},
}

SCAN_PAGES = {'038': range(2, 9), '040': range(2, 10)}
SELECTION_SCAN = [
    ('038', 2, 'any five', 'Section A rubric: whole-question choice; every question is carded.'),
    ('038', 2, 'any two', 'Section B rubric: whole-question choice; every question is carded.'),
    ('038', 2, 'or', 'Instructions: "blue or black pen", not a question.'),
    ('038', 3, 'any five', 'Section A rubric repeated.'),
    ('038', 3, 'the following', 'Q1 lead-in: every part asked.'),
    ('038', 4, 'choose', 'Q3 "Choose each term": every description matched, one card per lettered part.'),
    ('038', 4, 'the following', 'Q3 list of terms: the options.'),
    ('038', 4, 'or', 'Q4(a) "at A or at B": the answer options.'),
    ('038', 5, 'the following', 'Q5 lead-in: every statement asked.'),
    ('038', 5, 'or', 'Q5 "true (T) or false (F)": the answer options.'),
    ('038', 5, 'or', 'Q5 "T or F": the answer options.'),
    ('038', 6, 'any two', 'Section B rubric repeated.'),
    ('038', 6, 'the following', 'Q7(b) lead-in: every part asked.'),
    ('038', 6, 'or', 'Q7(b) "light intensity or on carbon dioxide (CO2) concentration": the factor the student '
                     'chose, asked by "Which of the two factors did you investigate?"; the scheme answers both '
                     'with one set of rows, so no routes; inside the one whole-part card.'),
    ('038', 7, 'the following', 'Q8(b) lead-in: every part asked.'),
    ('038', 8, 'the following', 'Q9(b) lead-in: every part asked.'),
    ('038', 8, 'the following', 'Q9(b)(i) "label the following": all three labels asked; inside the whole-part card.'),
    ('040', 2, 'any four', 'Section C rubric: whole-question choice; every question is carded.'),
    ('040', 2, 'or', 'Instructions: "blue or black pen", not a question.'),
    ('040', 3, 'any four', 'Section C rubric repeated.'),
    ('040', 3, 'the following', 'Q10(a) lead-in: every term asked, one card per roman.'),
    ('040', 3, 'the following', 'Q10(c) passage "The following data were produced": a reference to the table.'),
    ('040', 4, 'the following', 'Q11(a) lead-in: every term asked, one card per roman.'),
    ('040', 5, 'the following', 'Q12(a) lead-in: every term asked, one card per roman.'),
    ('040', 5, 'the following', 'Q12(b) "the following steps": the steps to order and to describe.'),
    ('040', 5, 'the following', 'Q12(c)(i) "each of the following parts": every part asked, one card per '
                                'numbered part.'),
    ('040', 5, 'the following', 'Q12(c)(iii) "each of the following": one card per numbered item.'),
    ('040', 6, 'the following', 'Q13(a) lead-in: every term asked, one card per roman.'),
    ('040', 6, 'or', 'Q13(c)(iii) "A, B, C, or D": the answer options.'),
    ('040', 6, 'or', 'Q13(c)(v) "high salt or high sugar": description.'),
    ('040', 7, 'any two', 'Q14 "any two of (a), (b), (c)": whole-part choice; every part is carded.'),
    ('040', 7, 'or', 'Q14(c)(ii)2 "a stem, a root, a bud, or a leaf": the answer options.'),
    ('040', 8, 'any two', 'Q15 "any two of (a), (b), (c)": whole-part choice; every part is carded.'),
    ('040', 8, 'both', 'Q15(a)(v) "Name both parts": both asked, one card.'),
    ('040', 9, 'both', 'Q15(c)(iii) "present in both cells": description.'),
]

ROUTES = {}

SEC = 'State Examinations Commission'
COMPRESSED = 'The scheme heads each answer with a compressed reprint of the ask.'
MARKER = 'The scheme heads this answer with its part marker alone.'
EACH_ITEM = 'A list the scheme prices entry by entry: one card per entry.'
NO_ANSWER = 'The scheme prints no answer here, only what earns the marks.'
WHOLE = ('Carded whole at its printed total: the scheme prints the answers but no per-response tariff they fit, '
         'so no row carries marks of its own and none is derived.')


def _A(page, start, end=None, **kw):
    return Q(page, start, end, doc='038', **kw)


def _C(page, start, end=None, **kw):
    return Q(page, start, end, doc='040', **kw)


def at(page, *path_and_marker, why=MARKER):
    """The scheme's own part marker, found under its question (and letter)."""
    *path, marker = path_and_marker
    return SQ(page, marker, path=list(path), paired=why, bare=True)


def item(page, n, end, anchor, doc='040'):
    """One entry of a printed numbered list."""
    return Q(page, f'{n}.', end, doc=doc, after=anchor, br=True)


def asked(keys, *letters):
    return [dict(k, asked=k['letter'] in letters) for k in keys]


# ------------------------------------------------------------- paper stems --
Q1 = _A(3, 'Use your knowledge of nutrition to answer the following questions.')
Q2 = _A(3, 'The diagram shows human cheek cells at different stages during cell division.')
Q3 = _A(4, 'Choose each term from the following list and place it in Column B to match a description in',
        'The first one has been completed as an example.')
Q4 = _A(4, 'The diagram represents the human menstrual cycle.')
Q5 = _A(5, 'Indicate whether the following statements are true (T) or false (F) by drawing a circle around',
        'T or F in each case.')
Q6 = _A(5, 'The photograph shows a microscope used in a laboratory.')
Q7B = _A(6, 'Answer the following questions about an investigation that you carried out to see how',
         'concentration.')
Q8B = _A(7, 'Answer the following questions about food tests that you carried out as part of your',
         'practical work.')
Q8BI = _A(7, 'What reagent did you use to test for protein?')
Q8SUGAR = _A(7, 'You tested another food for the presence of reducing sugar.')
Q8BVI = _A(7, 'What test solution did you use?')
Q9B = _A(8, 'Answer the following questions in relation to the dissection of a heart.')
Q10A = _C(3, 'Explain the following terms used in ecology:')
Q10B = [_C(3, 'Read the paragraph below and answer the questions that follow.'),
        _C(3, 'From a pollinator’s point of view, a good hedge has flowers in early spring to feast on after',
           'They shelter livestock from harsh weather and the hot summer sun.'),
        _C(3, 'Adapted from ‘The Importance of a Good Hedgerow’, The Irish Times, 26th July, 2018')]
Q10BADGERS = _C(3, 'In 2009 a study of the badger population was carried out in the south‐east of the country.',
                'produced.')
Q11A = _C(4, 'Explain the following terms used in genetics:')
Q11B = [_C(4, 'In sheep, the gene for white wool (W) is dominant to the gene for black wool (w).'),
        _C(4, 'If a heterozygous white sheep is crossed with a black sheep state:')]
Q12A = _C(5, 'Explain the following terms used in human nutrition:')
Q12B = [_C(5, 'The passage of food through the human digestive tract involves the following steps:'),
        _C(5, 'Absorption Digestion Egestion Ingestion')]
Q12C = _C(5, 'The diagram shows part of the human skeleton.')
Q12CI = _C(5, 'In your answer book, state which letter represents each of the following parts.')
Q12CIII = _C(5, 'Describe the role of each of the following:')
Q13A = _C(6, 'Explain the following terms used in cell metabolism:')
Q13EQ = _C(6, 'The equation below represents aerobic respiration.')
Q13STAGES = _C(6, 'Aerobic respiration is a two‐stage process by which organisms break down food molecules',
               'to get chemical energy.')
Q14B = _C(7, 'Two human endocrine glands, labelled A and B, are shown below.')
Q14C = _C(7, 'Vegetative propagation is a form of asexual reproduction in plants.')
Q15A = _C(8, 'The diagram shows a motor neuron.')
Q15B = _C(8, 'The diagram shows a human kidney and some attached structures.')
Q15C = _C(9, 'Two single‐celled organisms are shown below.')

# ------------------------------------------------------------ scheme lines --
L2E = 'Smoking/ radiation/ virus..(2 points)'
L4C = 'Oestrogen and Progesterone…. (2 points)'
LAB7 = ('Labels: (any 3 points) Water Plant or named plant/ water/lamp/ glass vessel or', 'named vessel /bubbles')
ERR7 = 'Uncooperative pondweed/ inadequate light'
DRAW9 = 'Septum/ two upper chambers/ two lower chambers/ at least one valve'
LAB9 = 'Aorta/ bicuspid valve/ left ventricle'
BEN10 = ('Any 2 valid benefits, e.g. nesting sites/', 'pollutants/ shelter livestock')
PLANTS10 = 'Any 2 named hedgerow plants, e.g. Violet/ primrose / fern ….'
MAMMALS10 = 'Any 2 named hedgerow mammals, e.g. Fox/ hedgehog / rat ….'
OSMOSIS13 = 'Movement of water across a semi permeable membrane OR'
LAB14 = 'Protein (coat)/ DNA or RNA or nucleic acid'
VIRUS14 = 'Why virus non-living: Non-cellular/cannot reproduce without host'
DIS14 = 'Any 2 named viral diseases, e.g. Flu/ measles/ chicken pox/ AIDS….'
SHAPES14 = 'Rods / cocci/ spirals'
NAT14 = ('Any 2 valid methods, e.g. runner (strawberry) / tuber', '(potato) / bulb (onion) /....')
PART14 = ('Any valid example; Runner is a stem/ tuber is a stem/', 'bulb is a bud/…..')
ART14 = 'Cuttings/layering/grafting/ micro-propagation….'
ADV14 = 'Any 2 valid advantages; e.g. fast / good traits kept ….'
NEURONS15 = 'Sensory / interneuron (2 points)'
CNS15 = 'Brain and spinal cord (2 points)'
EXCR15 = 'Removal of waste / made in the body (2 points)'
ORGANS15 = 'Any 2 valid excretory organs, e.g. Lungs/ skin ….'

L_MICROSCOPE = [L(x, S(name, page=8), False) for x, name in [('A', 'Eyepiece'), ('B', 'Stage'), ('C', 'Objective lens')]]
L_SKELETON = [L(x, S(line, page=14, piece=2, psep=' or '), False) for x, line in
              [('A', '3 or pelvis'), ('B', '1 or femur'), ('C', '2 or joint'), ('D', '4 or marrow')]]
L_GLANDS = [L('A', S('Thyroid', page=16), False), L('B', S('Pancreas', page=16), False)]
L_NEURON = [L('A', S('Dendrite', page=17), False), L('B', S('Axon', page=17), False),
            L('C', S('Cell body [allow nucleus]', page=17, piece=1, psep=' ['), False)]
L_KIDNEY = [L(x, S(name, page=17), False) for x, name in [('A', '(Renal) vein'), ('B', '(Renal) artery'), ('C', 'Ureter')]]
L_CELLS = [L('A', S('Bud', page=18), True), L('B', S('Pseudopod or false foot', page=18), True)]


TASKS = [
    # ------------------------------------------------------------ Section A --
    T('1a', 'Q1(a)', 'A', _A(3, 'Name a fat‐soluble vitamin.'), [anyn(S('A, D, E, K'), 1, 6, sep=',')], 'bio-1-2',
      'fat-soluble-vitamins', SQ(6, 'Any fat-soluble vitamin:'), 6, stem=[Q1]),
    T('1b', 'Q1(b)', 'A', _A(3, 'Name a disorder caused by a lack of this vitamin in the diet.'),
      [pt(S('Named matching disorder'), 6, kind='criterion', note=NO_ANSWER)], 'bio-1-2', 'vitamin-deficiency-disorders',
      SQ(6, 'Matching disorder for named vitamin:'), 6, stem=[Q1, M('(a)', 3), _A(3, 'Name a fat‐soluble vitamin.')]),
    T('1c', 'Q1(c)', 'A', _A(3, 'Which molecules are proteins made of?'), [pt(S('Amino Acids'), 6)], 'bio-1-2',
      'amino-acids', SQ(6, 'Proteins are made of:'), 6, stem=[Q1]),
    T('1d', 'Q1(d)', 'A', _A(3, 'Name a mineral needed by plants.'), [pt(S('e.g. Magnesium etc.'), 6)], 'bio-1-2',
      'minerals-for-plants', SQ(6, 'Named mineral needed for plants:'), 6, stem=[Q1]),
    T('1e', 'Q1(e)', 'A', _A(3, 'Give an example of a polysaccharide.'), [pt(S('Starch'), 6)], 'bio-1-2',
      'polysaccharides', SQ(6, 'Example of polysaccharide:'), 6, stem=[Q1]),
    T('2a', 'Q2(a)', 'A', _A(3, 'Rewrite the letters A, B, C, D in the correct stage order.'), [pt(S('B, A, D, C'), 6)],
      'bio-2-3', 'order-of-mitosis', SQ(6, 'Order of stages:', paired=COMPRESSED), 6, stem=[Q2], fig='q2-division'),
    T('2b', 'Q2(b)', 'A', _A(3, 'What term is used to describe the stage of the cell cycle when the cell is not dividing?'),
      [pt(S('Interphase'), 6)], 'bio-2-3', 'interphase', SQ(6, 'When cell not dividing:'), 6, stem=[Q2],
      fig='q2-division'),
    T('2c', 'Q2(c)', 'A', _A(3, 'Name the two types of cell division.'),
      [pt(S('Mitosis and Meiosis', piece=1, psep=' and '), 6), pt(S('Mitosis and Meiosis', piece=2, psep=' and '), 6)],
      'bio-2-3', 'types-of-cell-division', SQ(6, 'Types of cell division:'), 12, stem=[Q2], fig='q2-division',
      decision='The scheme prints "Mitosis and Meiosis (2 points)": two responses, each its own row.'),
    T('2d', 'Q2(d)', 'A', _A(3, 'What disease is caused by uncontrolled cell division?'), [pt(S('Cancer'), 6)],
      'bio-2-3', 'cancer', SQ(6, 'Uncontrolled cell division disease:'), 6, stem=[Q2], fig='q2-division'),
    T('2e', 'Q2(e)', 'A', _A(3, 'Give two possible environmental causes of this disease.'),
      [anyn(None, 2, 6, options=[S(L2E, piece=1), S(L2E, piece=2), S(L2E, piece=[3, 1], psep=['/', '..'])],
            open_list=True)], 'bio-2-3', 'causes-of-cancer', SQ(6, 'Environmental causes of cancer:'), 12,
      stem=[Q2, M('(d)', 3), _A(3, 'What disease is caused by uncontrolled cell division?')], fig='q2-division',
      decision='"Smoking/ radiation/ virus..(2 points)": a menu of two responses; the trailing dots after "virus" '
               'are read as the scheme\'s open-list ellipsis, as its "…." is elsewhere.'),
] + [
    T(f'3{x}', f'Q3({x})', 'A', _A(4, ask), [pt(S(ans), 6)], topic, concept, SQ(6, sq), 6, stem=[Q3], qfig='q3-table',
      decision='The list of terms and the table are shown as the question\'s own print.')
    for x, ask, ans, topic, concept, sq in [
        ('a', 'Plant organ for photosynthesis', 'Leaf', 'bio-2-2', 'leaf', 'Photosynthesis organ:'),
        ('b', 'Tissues for transport in plants', 'Vascular', 'bio-2-6', 'vascular-tissue', 'Plant transport tissue:'),
        ('c', 'Tissues on outer plant surface', 'Dermal', 'bio-2-6', 'dermal-tissue', 'Outer surface tissue:'),
        ('d', 'A group of rapidly dividing plant cells', 'Meristem', 'bio-2-6', 'meristem', 'Dividing cell region:'),
        ('e', 'An opening on the stem for gas exchange', 'Lenticel', 'bio-2-6', 'lenticel', 'Stem gas exchange:')]
] + [
    T('4a', 'Q4(a)', 'A', _A(4, 'Does normal menstrual bleeding occur at A or at B?'), [pt(S('A'), 6)], 'bio-2-5',
      'menstruation', SQ(7, 'Normal bleeding at:'), 6, stem=[Q4], fig='q4-cycle'),
    T('4bi', 'Q4(b)(i)', 'A', _A(4, 'Place the letter X on the diagram to indicate when', 'fertilisation is most likely to occur.'),
      [pt(S('X - Any day(s) from 12 to 17 (inclusive)'), 6, kind='criterion')], 'bio-2-5', 'timing-of-fertilisation',
      SQ(7, 'Fertilisation:'), 6, stem=[Q4], fig='q4-cycle'),
    T('4bii', 'Q4(b)(ii)', 'A', _A(4, 'Place the letter Y on the diagram to indicate when', 'implantation is most likely to occur.'),
      [pt(S('Y - Any day(s) from 12 to 20 (inclusive)'), 6, kind='criterion')], 'bio-2-5', 'timing-of-implantation',
      SQ(7, 'Implantation:'), 6, stem=[Q4], fig='q4-cycle'),
    T('4c', 'Q4(c)', 'A', _A(4, 'Name two hormones that have a role in the menstrual cycle.'),
      [anyn(None, 2, 6, options=[S(L4C, piece=1, psep=' and '), S(L4C, piece=[2, 1], psep=[' and ', '…'])],
            open_list=True)], 'bio-2-5', 'menstrual-hormones', SQ(7, 'Menstrual cycle hormones:'), 12, stem=[Q4],
      fig='q4-cycle', decision='"Oestrogen and Progesterone…. (2 points)": two responses; the ellipsis leaves the list open.'),
    T('4d', 'Q4(d)', 'A', _A(4, 'Give a cause of infertility in women.'), [pt(S('e.g. Failure to ovulate ….'), 6)],
      'bio-2-5', 'female-infertility', SQ(7, 'Cause of female infertility:'), 6, stem=[Q4], fig='q4-cycle'),
    T('4e', 'Q4(e)', 'A', _A(4, 'Suggest a treatment to help a couple to have children in the case of infertility.'),
      [pt(S('e.g. IVF ….'), 6)], 'bio-2-5', 'infertility-treatment', SQ(7, 'Infertility treatment:'), 6, stem=[Q4],
      fig='q4-cycle'),
] + [
    T(f'5{x}', f'Q5({x})', 'A', _A(5, ask), [pt(S(ans), 6)], 'bio-3-1', concept, SQ(7, sq), 6, stem=[Q5])
    for x, ask, ans, concept, sq in [
        ('a', 'The sun is the primary source of energy for our planet.', 'TRUE', 'sun-as-energy-source',
         'The sun is our primary energy source:'),
        ('b', 'Pollution is the removal of harmful substances from the environment.', 'FALSE', 'pollution',
         'Pollution is removal of harmful substances:'),
        ('c', 'Qualitative surveys record the number of organisms.', 'FALSE', 'qualitative-survey',
         'Qualitative surveys record numbers:'),
        ('d', 'Food chains are always more than five organisms long.', 'FALSE', 'food-chain-length',
         'Food chains are always more than five organisms:'),
        ('e', 'Herbivores are animals that feed on plants only.', 'TRUE', 'herbivores', 'Herbivores feed on plants only:'),
        ('f', 'The functional role of an organism is called its niche.', 'TRUE', 'niche', 'The functional role is the niche:'),
        ('g', 'A producer is always at the start of a food chain.', 'TRUE', 'producers', 'Food chains start with producers:')]
] + [
    T('6a', 'Q6(a)', 'A', _A(5, 'What is the purpose of a microscope?'), [pt(S('To magnify'), 6)], 'bio-1-3',
      'purpose-of-a-microscope', SQ(8, 'Purpose of microscope:'), 6, stem=[Q6], fig='q6-microscope'),
] + [
    T(f'6b-{x.lower()}', 'Q6(b)', 'A', _A(5, 'Name the parts labelled A, B, C in the photograph.'), [pt(S(name), 6)],
      'bio-1-3', f'microscope-part-{x.lower()}', at(8, 'Q6', '(b)'), 6, stem=[Q6], fig='q6-microscope',
      labels=asked(L_MICROSCOPE, x), item=(x.lower(), x), decision=EACH_ITEM)
    for x, name in [('A', 'Eyepiece'), ('B', 'Stage'), ('C', 'Objective lens')]
] + [
    T('6c', 'Q6(c)', 'A', _A(5, 'Why is the low‐power lens used first when focusing on cells?'),
      [pt(S('Easier to locate cells'), 6)], 'bio-1-3', 'low-power-first', SQ(8, 'Why low-power first:'), 6, stem=[Q6],
      fig='q6-microscope'),
    T('6d', 'Q6(d)', 'A', _A(5, 'Use the letter F to label the coarse‐focus knob on the photograph.'),
      [pt(S('Indicating coarse focus knob in diagram'), 6, kind='criterion', note=NO_ANSWER)], 'bio-1-3',
      'coarse-focus-knob', at(8, 'Q6', '(d)'), 6, stem=[Q6], fig='q6-microscope'),
    T('6e', 'Q6(e)', 'A', _A(5, 'Why would you use a stain when preparing a microscope slide?'),
      [pt(S('Easier to see cells or particular parts of cells'), 6)], 'bio-1-3', 'why-stain', SQ(8, 'Why stain:'), 6,
      stem=[Q6], fig='q6-microscope'),
    # ------------------------------------------------------------ Section B --
    T('7ai', 'Q7(a)(i)', 'B', _A(6, 'In which plant cell structure does photosynthesis take place?'),
      [pt(S('Chloroplast'), 4)], 'bio-2-2', 'chloroplast', SQ(9, 'Where photosynthesis occurs:', paired=COMPRESSED), 4),
    T('7aii', 'Q7(a)(ii)', 'B', _A(6, 'Which biomolecule is made by photosynthesis?'), [pt(S('Glucose'), 4)], 'bio-2-2',
      'product-of-photosynthesis', SQ(9, 'Biomolecule made by photosynthesis:'), 4),
    T('7b', 'Q7(b)', 'B',
      [_A(6, 'Which of the two factors did you investigate?'),
       M('(i)', 6, br=True), _A(6, 'In the space below draw and label a diagram of the apparatus you used in your', 'investigation.'),
       M('(ii)', 6, br=True), _A(6, 'How did you vary your chosen factor?'),
       M('(iii)', 6, br=True), _A(6, 'How did you measure the rate of photosynthesis?'),
       M('(iv)', 6, br=True), _A(6, 'Describe a source of error in this investigation.')],
      [pt(S('Submerged plant and lamp'), 0, kind='criterion', label=S('Drawing to show:')),
       anyn(None, 3, 0, options=[S(*LAB7, piece=[1, 2], psep=['/', ') '])] + [S(*LAB7, piece=n) for n in (2, 3, 4, 5)],
            note_sel=S(*LAB7, piece=[1, 1], psep=['/', ' Water'])),
       pt(S('Moved lamp or varied conc. of NaHCO3 solution'), 0, label=S('How factor varied:')),
       pt(S('Number of bubbles/per minute (or per unit time)'), 0, label=S('How rate measured:')),
       pt(S(ERR7, piece=1), 0, label=S('Source of error:')), pt(S(ERR7, piece=2), 0, label=S('Source of error:'))],
      'bio-2-2', 'rate-of-photosynthesis-investigation', at(9, 'Q7', '(b)'), 24, stem=[Q7B], tariff='questionTotal',
      decision=WHOLE + ' The scheme prints "Drawing (3) + Labels - 3(3)" over (i) and "9 + 3(1)" over (ii)-(iv); '
               '(ii)-(iv) print three answers, which "9 + 3(1)" fits only if (iii)\'s "Number of bubbles/per minute" '
               'counts as two responses, which the scheme does not say. The unnumbered "Which of the two factors did '
               'you investigate?" has no printed answer. Part total from the Section B rubric: "part (b) carries 24 '
               'marks".'),
    T('8ai', 'Q8(a)(i)', 'B', _A(7, 'Name a food source that is rich in protein.'),
      [pt(S('e.g. Meat or any valid answer'), 4)], 'bio-1-2', 'protein-rich-food', SQ(10, 'Food rich in protein:'), 4),
    T('8aii', 'Q8(a)(ii)', 'B', _A(7, 'Give a reason why the body needs protein in the diet.'),
      [pt(S('Growth or repair'), 4)], 'bio-1-2', 'why-protein', SQ(10, 'Why body needs protein:'), 4),
] + [
    T(f'8b{r}', f'Q8(b)({r})', 'B', q, [pt(S(*ans), 6)], 'bio-1-2', concept, sq, 6, stem=stem)
    for r, q, ans, concept, sq, stem in [
        ('i', Q8BI, ('Biuret (Sodium Hydroxide and Copper Sulphate',), 'biuret', SQ(10, 'Protein test reagent:'), [Q8B]),
        ('ii', _A(7, 'What colour was this reagent before you added it to the food sample?'), ('Blue',),
         'biuret-colour-before', SQ(10, 'Colour before test:'), [Q8B, M('(i)', 7), Q8BI]),
        ('iii', _A(7, 'What was the final colour of this reagent if protein was present?'), ('Purple (violet, mauve)',),
         'biuret-positive', SQ(10, 'Positive colour:', paired=COMPRESSED), [Q8B, M('(i)', 7), Q8BI]),
        ('iv', _A(7, 'Name a piece of apparatus required to carry out this test in a laboratory.'),
         ('Any valid named piece of apparatus, e.g. Dropper, test-', 'tube, beaker etc.'), 'food-test-apparatus',
         SQ(10, 'Piece of apparatus for test:'), [Q8B, M('(i)', 7), Q8BI]),
        ('v', _A(7, 'Describe a safety precaution that should be taken during the investigation.'),
         ('Any valid safety precaution, e.g. Safety glasses, laboratory coat, gloves etc.',), 'food-test-safety',
         SQ(10, 'Safety precaution:'), [Q8B]),
        ('vi', Q8BVI, ("Benedict's (or Fehling's) (solution)",), 'benedicts', SQ(10, 'Reducing sugar test reagent:'),
         [Q8B, Q8SUGAR]),
        ('vii', _A(7, 'What colour was this solution before you added it to the food sample?'), ('Blue',),
         'benedicts-colour-before', SQ(10, 'Colour before test:', nth=2), [Q8B, Q8SUGAR, M('(vi)', 7), Q8BVI]),
        ('viii', _A(7, 'What was the final colour of this solution if reducing sugar was present?'), ('Red [allow brown]',),
         'benedicts-positive', SQ(10, 'Positive colour:', nth=2, paired=COMPRESSED), [Q8B, Q8SUGAR, M('(vi)', 7), Q8BVI])]
] + [
    T('9ai', 'Q9(a)(i)', 'B', _A(8, 'Name the type of muscle found in the heart.'), [pt(S('Cardiac', after='(i)'), 4)],
      'bio-2-6', 'cardiac-muscle', SQ(11, 'Heart muscle:', 'Heart muscle:'), 4,
      decision='The scheme sets the reprint and its answer on one line ("Heart muscle: Cardiac").'),
    T('9aii', 'Q9(a)(ii)', 'B', _A(8, 'Name the blood vessel that provides the heart muscle with oxygen.'),
      [pt(S('Coronary artery'), 4)], 'bio-2-6', 'coronary-artery', SQ(11, 'Vessel that provides heart muscle with O2:'), 4),
    T('9b', 'Q9(b)', 'B',
      [M('(i)', 8), _A(8, 'In the space below, draw a diagram of a dissected heart and on it label the', 'following:'),
       _A(8, 'Aorta', br=True), _A(8, 'Bicuspid valve'), _A(8, 'Left ventricle'),
       M('(ii)', 8, br=True), _A(8, 'Name a piece of equipment used during the dissection.'),
       M('(iii)', 8, br=True), _A(8, 'Outline a safety step, specific to this task, to be taken before beginning the',
                                  'dissection.'),
       M('(iv)', 8, br=True), _A(8, 'Describe how you carried out the dissection.')],
      # The drawing is one priced item ("Drawing (3)"); its four features are what
      # it must show, so they stay one criterion row rather than four.
      [pt(S(DRAW9), 0, kind='criterion', label=S('Drawing to show:'))]
      + [pt(S(LAB9, piece=n), 0, label=S('Labels:')) for n in (1, 2, 3)]
      + [pt(S('Piece of dissection equipment: Any valid piece of dissection equipment, e.g. Scalpel ….'), 0),
         pt(S('Any valid safety procedure, e.g. wash heart.'), 0, label=S('Safety procedure:')),
         anyn(S('Tray or dissection board/ another safety precaution /', 'correct disposal.'), 4, 0,
              note_sel=S('Dissection details – Any 4 points'))],
      'bio-2-6', 'heart-dissection', at(11, 'Q9', '(b)'), 24, stem=[Q9B], tariff='questionTotal',
      decision=WHOLE + ' The scheme prints "Drawing (3) / Labels - 3(1)" over (i) and no tariff for (ii)-(iv). Part '
               'total from the Section B rubric: "part (b) carries 24 marks".'),
    # ------------------------------------------------------------ Section C --
] + [
    T(f'10a{r}', f'Q10(a)({r})', 'C', [Q10A, _C(3, term, br=True)], [pt(S(ans), 7)], 'bio-3-1', concept, SQ(12, sq), 7)
    for r, term, ans, concept, sq in [
        ('i', 'Habitat', 'Where organism lives', 'habitat', 'Habitat:'),
        ('ii', 'Biosphere', 'Any place on earth where life can exist', 'biosphere', 'Biosphere:'),
        ('iii', 'Conservation.', 'Wise management of ecosystem', 'conservation', 'Conservation:')]
] + [
    T(f'10b{r}', f'Q10(b)({r})', 'C', _C(3, ask), rows, 'bio-3-1', concept, sq, total, stem=Q10B)
    for r, ask, rows, concept, sq, total in [
        ('i', 'Give an example of a pollinator.', [pt(S('Name of valid example, e.g. Bee ….'), 9)], 'pollinators',
         SQ(12, 'Pollinator:'), 9),
        ('ii', 'How do pollinators benefit from hedgerows?', [pt(S('Named benefit, e.g. Food ….'), 9)],
         'hedgerows-and-pollinators', SQ(12, 'How pollinators benefit:'), 9),
        ('iii', 'Give two other ways hedgerows provide benefit in nature.',
         [anyn(S(*BEN10, piece=2, psep='e.g. '), 2, 9, open_list=True, note_sel=S(*BEN10, piece=1, psep=', e.g.'))],
         'benefits-of-hedgerows', SQ(12, 'Other ways hedgerows provide benefit:'), 18),
        ('iv', 'Name two plants that are found in hedgerows.',
         [anyn(S(PLANTS10, piece=[2, 1], psep=['e.g. ', ' …']), 2, 9, open_list=True,
               note_sel=S(PLANTS10, piece=1, psep=', e.g.'))], 'hedgerow-plants', SQ(12, 'Hedgerow plants:'), 18),
        ('v', 'Name two mammals that are found in hedgerows.',
         [anyn(S(MAMMALS10, after='(v)', piece=[2, 1], psep=['e.g. ', ' …']), 2, 9, open_list=True,
               note_sel=S(MAMMALS10, after='(v)', piece=1, psep=', e.g.'))], 'hedgerow-mammals',
         SQ(12, 'Hedgerow mammals:', 'Hedgerow mammals:'), 18),
        ('vi', 'How does a plant benefit by producing flowers in early spring?',
         [pt(S('Completion of life cycle before canopy closure /', 'pollinators are present……'), 9)], 'early-flowering',
         SQ(12, 'Benefit to plant of early flowers:'), 9)]
] + [
    T('10ci', 'Q10(c)(i)', 'C', _C(3, 'What is meant by the term carnivore?'),
      [pt(S('Eats (other) animals only / eats meat'), 3)], 'bio-3-1', 'carnivore', SQ(12, 'Carnivore:'), 3),
    T('10cii', 'Q10(c)(ii)', 'C', _C(3, 'Name a carnivore from an ecosystem other than the hedgerow.'),
      [pt(S('Any non-hedgerow carnivore, e.g. Shark'), 3)], 'bio-3-1', 'a-carnivore',
      SQ(12, 'Carnivore not from hedgerow:'), 3),
    T('10ciii', 'Q10(c)(iii)', 'C', _C(3, 'Describe an adaptation that helps this animal to survive.'),
      [pt(S('Adaptation: (Related feature to named carnivore in (ii)) - e.g. Streamlined body for the Shark'), 3,
          kind='criterion'),
       pt(S('Benefit: (Related Benefit of adaptation stated in (ii)) - e.g. for speed, for the Shark'), 3,
          kind='criterion')],
      'bio-3-1', 'carnivore-adaptations', at(12, 'Q10', '(c)', '(iii)'), 6,
      stem=[M('(ii)', 3), _C(3, 'Name a carnivore from an ecosystem other than the hedgerow.')],
      decision='The scheme prices the adaptation and its benefit as two responses under "8 X 3".'),
    T('10civ', 'Q10(c)(iv)', 'C', _C(3, 'Suggest how the badgers should have been marked.'),
      [pt(S('Any stated named method or described;', 'e.g. unobtrusively marked or microchip or ear tag'), 3)],
      'bio-3-1', 'marking-animals', SQ(13, 'How badgers should have been marked:'), 3, stem=[Q10BADGERS]),
    T('10cv', 'Q10(c)(v)', 'C', _C(3, 'Using the data above, calculate the total population of badgers in the study area.',
                                   'Using the data above, calculate the total population of badgers in the study area.'),
      [pt(S('180 x 150'), 3), pt(S('÷ 40'), 3), pt(S('675'), 3)], 'bio-3-1', 'capture-recapture',
      SQ(13, '(v)', paired='The scheme heads the calculation "Calculation:", sharing no word with the ask; anchored '
                           'on its part marker.', bare=True), 9, stem=[Q10BADGERS], fig='q10-badgers',
      decision='The scheme prints the calculation as three lines, three responses under "8 X 3".'),
] + [
    T(f'11a{r}', f'Q11(a)({r})', 'C', [Q11A, _C(4, term, br=True)], [pt(S(*ans), 7)], 'bio-1-4', concept, SQ(13, sq), 7)
    for r, term, ans, concept, sq in [
        ('i', 'Dominant', ('Allele (or gene) that prevents expression of another allele/',
                           'Allele expressed in heterozygous condition'), 'dominant', 'Dominant:'),
        ('ii', 'Recessive', ('Allele expressed only in absence of dominant allele /', 'Allele expressed in homozygous condition'),
         'recessive', 'Recessive:'),
        ('iii', 'Gene expression.', ('Production of protein or development of trait',), 'gene-expression',
         'Gene expression:')]
] + [
    T(f'11b{r}', f'Q11(b)({r})', 'C', _C(4, *ask), rows, 'bio-1-4', concept, SQ(13, sq), 9 * len(rows), stem=Q11B,
      decision=dec)
    for r, ask, rows, concept, sq, dec in [
        ('i', ('The genotype of the black sheep.',), [pt(S('ww'), 9)], 'black-sheep-genotype', 'Black sheep\'s genotype:', ''),
        ('ii', ('The genotype of the white sheep.',), [pt(S('Ww'), 9)], 'white-sheep-genotype', 'White sheep\'s genotype:', ''),
        ('iii', ('The genotypes of the gametes that can be produced by the white sheep.',),
         [pt(S('W and w', piece=n, psep=' and '), 9) for n in (1, 2)], 'white-sheep-gametes', 'White sheep\'s gametes:',
         'The scheme prints "W and w": two gametes, two responses.'),
        ('iv', ('The genotype of the gametes that can be produced by the black sheep.',), [pt(S('w'), 9)],
         'black-sheep-gametes', 'Black sheep\'s gametes:', ''),
        ('v', ('The genotypes and matching phenotypes of the possible offspring.',
               'The genotypes and matching phenotypes of the possible offspring.'),
         [pt(S(line, piece=n, psep='='), 9) for line in ('Ww = White', 'ww = Black') for n in (1, 2)],
         'offspring-of-the-cross', 'Offspring genotypes and phenotypes:',
         'The scheme prints "Ww = White" and "ww = Black": two genotypes and their phenotypes, four responses; with '
         '(iii)\'s two, the part\'s nine responses fit "9 + 9 + 3 + 6(1)".')]
] + [
    T('11c', 'Q11(c)', 'C',
      [M('(i)', 4), _C(4, 'What is meant by the term species?'),
       M('(ii)', 4, br=True), _C(4, 'Give an example of an inherited characteristic from a named species.'),
       M('(iii)', 4, br=True), _C(4, 'What is meant by the term evolution?'),
       M('(iv)', 4, br=True), _C(4, 'Give a source of evidence that evolution has occurred.'),
       M('(v)', 4, br=True), _C(4, 'Explain what you understand by the theory of natural selection.',
                                'Explain what you understand by the theory of natural selection.')],
      [pt(S('(Group of) organisms that can interbreed to produce fertile offspring'), 0, label=S('Species:')),
       pt(S('Any valid named inherited characteristic', 'in a named species, e.g. Beak length in the finch…'), 0,
          label=S('Inherited characteristic in named species:')),
       pt(S('Change in species over time'), 0, label=S('Evolution:')),
       pt(S('Fossils or comparative anatomy or embryos….', page=14), 0, label=S('Evidence for evolution:', page=14)),
       anyn(S('Variation/ beneficial/ explanation of beneficial/', 'variation inherited/ leads to speciation', page=14),
            3, 0, note_sel=S('Natural selection: (Any 3 points):', page=14))],
      'bio-1-5', 'evolution-and-natural-selection', at(13, 'Q11', '(c)'), 24, tariff='questionTotal',
      decision=WHOLE + ' The scheme prints "8 X 3" (eight responses at 3) but seven answers: one each for (i)-(iv) '
               'and any three points for (v); (ii)\'s one printed answer ("Any valid named inherited characteristic '
               'in a named species") would have to count twice.'),
] + [
    T(f'12a{r}', f'Q12(a)({r})', 'C', [Q12A, _C(5, *term, br=True)], [pt(S(ans), 7)], 'bio-2-6', concept, SQ(14, sq), 7)
    for r, term, ans, concept, sq in [
        ('i', ('Heterotroph',), 'Obtains food from other organisms or cannot make its own food', 'heterotroph',
         'Heterotroph:'),
        ('ii', ('Omnivore',), 'Eats both plant an animal material', 'omnivore', 'Omnivore:'),
        ('iii', ('Peristalsis.', 'Peristalsis.'), '(Muscular) contractions of gut wall', 'peristalsis', 'Peristalsis:')]
] + [
    T('12bi', 'Q12(b)(i)', 'C', _C(5, 'In your answer book, rewrite these steps, placing them in the correct order.'),
      [pt(S('Ingestion, Digestion, Absorption, Egestion'), 9)], 'bio-2-6', 'order-of-digestion-steps',
      SQ(14, 'Correct order:'), 9, stem=Q12B),
] + [
    T(f'12bii-{slug}', 'Q12(b)(ii)', 'C', _C(5, 'Describe what happens during each of the steps, and say where each step occurs.'),
      [pt(S(line, piece=1), 9), pt(S(line, piece=2), 9)], 'bio-2-6', f'{slug}-described',
      SQ(14, 'Describe - 2 points for each', paired=COMPRESSED), 18, stem=Q12B, item=(slug, name),
      decision=EACH_ITEM + ' The scheme prices each step at "2 points for each": what happens, and where.')
    for slug, name, line in [
        ('ingestion', 'Ingestion', 'Ingestion: Taking in food / mouth'),
        ('digestion', 'Digestion', 'Digestion: breaking down food / mouth or stomach or small intestine'),
        ('absorption', 'Absorption', 'Absorption: (food molecules) entering blood / small intestine'),
        ('egestion', 'Egestion', 'Egestion: removing undigested material / rectum or anus')]
] + [
    T(f'12ci{n}', f'Q12(c)(i){n}', 'C', [Q12CI, part], [pt(S(ans), 3, label=S(f'{x}:'))], 'bio-2-4', concept,
      at(14, 'Q12', '(c)', '(i)'), 3, stem=[Q12C], fig='q12c-skeleton', labels=asked(L_SKELETON, x),
      decision=EACH_ITEM + ' The scheme prints the key by letter ("B: 1 or femur"); each card is one numbered part.')
    for n, part, x, ans, concept in [
        (1, _C(5, '1. Femur 2. Joint 3. Pelvis', piece=1, psep=' 2.', br=True), 'B', '1 or femur', 'femur'),
        (2, _C(5, '1. Femur 2. Joint 3. Pelvis', piece=[1, 2], psep=[' 3.', 'Femur '], br=True), 'C', '2 or joint',
         'joint'),
        (3, _C(5, '1. Femur 2. Joint 3. Pelvis', piece=2, psep='Joint ', br=True), 'A', '3 or pelvis', 'pelvis'),
        (4, _C(5, '4. Bone marrow', br=True), 'D', '4 or marrow', 'bone-marrow')]
] + [
    T('12cii', 'Q12(c)(ii)', 'C', _C(5, 'What is meant by the term antagonistic pair in reference to muscles?'),
      [pt(S('Muscles that move a bone in opposite directions'), 3)], 'bio-2-4', 'antagonistic-pairs',
      SQ(14, 'Antagonistic pair:'), 3),
    T('12ciii1', 'Q12(c)(iii)1', 'C', [Q12CIII, item(5, 1, 'Compact bone', 'Describe the role of each of the following:')],
      [pt(S('Support'), 3)], 'bio-2-4', 'compact-bone', SQ(14, 'Compact bone:'), 3, decision=EACH_ITEM),
    T('12ciii2', 'Q12(c)(iii)2', 'C', [Q12CIII, item(5, 2, 'Bone marrow.', 'Describe the role of each of the following:')],
      [pt(S('Makes blood cells or stores fat'), 3)], 'bio-2-4', 'role-of-bone-marrow', SQ(14, 'Marrow:'), 3,
      decision=EACH_ITEM),
    T('12civ', 'Q12(c)(iv)', 'C', _C(5, 'Give a treatment for a named disorder of the musculoskeletal system.',
                                     'Give a treatment for a named disorder of the musculoskeletal system.'),
      [anyn(None, 1, 3, options=[
          S('Arthritis: exercise or physiotherapy or joint replacement or anti-inflammatory medication OR', piece=1,
            psep=' OR'),
          S('Osteoporosis: diet or exercise OR', piece=1, psep=' OR')],
            open_list=True, note_sel=S('Another valid treatment for a valid musculoskeletal disorder'))],
      'bio-2-4', 'musculoskeletal-treatment', SQ(15, 'Treatment for named musculoskeletal disorder:'), 3,
      decision='One treatment for one named disorder: the scheme prints arthritis or osteoporosis "OR another valid '
               'treatment for a valid musculoskeletal disorder", so one open menu.'),
] + [
    T(f'13a{r}', f'Q13(a)({r})', 'C', [Q13A, _C(6, *term, br=True)], [pt(ans, 7)], topic, concept, sq, 7, decision=dec)
    for r, term, ans, topic, concept, sq, dec in [
        ('i', ('Enzyme',), S('Biological catalyst'), 'bio-2-1', 'enzyme', SQ(15, 'Enzyme:'), ''),
        ('ii', ('Aerobic',), S('Requires oxygen'), 'bio-2-2', 'aerobic', SQ(15, 'Aerobic:'), ''),
        ('iii', ('Fermentation.', 'Fermentation.'), S('Anaerobic respiration', after='(iii)'), 'bio-2-2', 'fermentation',
         SQ(15, 'Fermentation:', 'Fermentation:'), 'The scheme sets the reprint and its answer on one line.')]
] + [
    T(f'13b{r}', f'Q13(b)({r})', 'C', _C(6, *ask), rows, 'bio-2-2', concept, sq, 9 * len(rows), stem=stem, fig=fig)
    for r, ask, rows, concept, sq, stem, fig in [
        ('i', ('Name the gas X.',), [pt(S('Oxygen'), 9)], 'gas-x', SQ(15, 'Gas X:'), [Q13EQ], 'q13b-equation'),
        ('ii', ('Name a process that produces gas X.',), [pt(S('Photosynthesis'), 9)], 'source-of-oxygen',
         SQ(15, 'Gas X produced by:'), [Q13EQ], 'q13b-equation'),
        ('iii', ('Name the gas Y.',), [pt(S('Carbon dioxide'), 9)], 'gas-y', SQ(15, 'Gas Y:'), [Q13EQ], 'q13b-equation'),
        ('iv', ('Name a process, other than aerobic respiration, that produces gas Y.',),
         [pt(S('Burning or anaerobic respiration'), 9)], 'source-of-carbon-dioxide', SQ(15, 'Gas Y produced by:'),
         [Q13EQ], 'q13b-equation'),
        ('v', ('Name the locations in the cell for stage 1 and for stage 2.',),
         [pt(S('Cytoplasm'), 9, label=S('Stage 1:')), pt(S('Mitochondria'), 9, label=S('Stage 2:'))],
         'locations-of-respiration', at(15, 'Q13', '(b)', '(v)', why='The scheme heads each stage\'s answer separately.'),
         [Q13STAGES], None),
        ('vi', ('Which stage produces the larger amount of energy?',), [pt(S('Stage 2'), 9)], 'stage-two-energy',
         SQ(15, 'Larger amount of energy:'), [Q13STAGES], None),
        ('vii', ('Which stage requires gas X from the equation above?',), [pt(S('Stage 2'), 9)], 'stage-needing-oxygen',
         SQ(15, 'Requires gas X:'), [Q13EQ, Q13STAGES], 'q13b-equation'),
        ('viii', ('Give a role for the energy produced by the cell.', 'Give a role for the energy produced by the cell.'),
         [pt(S('Protein synthesis or cell division or other valid role….'), 9)], 'uses-of-energy',
         SQ(15, 'Role for energy produced:'), [Q13STAGES], None)]
] + [
    T('13c', 'Q13(c)', 'C',
      [M('(i)', 6), _C(6, 'Name two selectively permeable membranes in cells.'),
       M('(ii)', 6, br=True), _C(6, '1. What is meant by the term diffusion?'),
       _C(6, '2. What is meant by the term osmosis?', br=True),
       _C(6, 'The diagram shows how a plant cell changes when it is left in a highly concentrated salt', 'solution.',
          br=True),
       M('(iii)', 6, br=True), _C(6, 'Which letter A, B, C, or D, shows the cell when turgid?'),
       M('(iv)', 6, br=True), _C(6, 'What process has caused the appearance of the cell at D?'),
       M('(v)', 6, br=True), _C(6, 'Certain foods are treated with high salt or high sugar concentrations.'),
       _C(6, '1. Why are these foods treated in this way?', br=True),
       _C(6, '2. How does this treatment work?', '2. How does this treatment work?', br=True)],
      [anyn(S('Cell membrane/ chloroplast/ mitochondrion/ nuclear membrane ….', piece=1, psep=' …'), 2, 0,
            open_list=True, note_sel=S('Any 2 points')),
       pt(S('Movement of molecules from high conc. to low conc.'), 0, label=S('1. Diffusion:', piece=2, psep='. ')),
       pt(S(OSMOSIS13, page=16, piece=1, psep=' OR'), 0, label=S('2. Osmosis:', page=16, piece=2, psep='. ')),
       pt(S('Movement of water from dilute to a more concentrated solution', page=16), 0, label=S('2. Osmosis:', page=16, piece=2, psep='. ')),
       pt(S('A', page=16, after='Which cell turgid:'), 0, label=S('Which cell turgid:', page=16)),
       pt(S('Plasmolysis [allow cell lost water]', page=16), 0, label=S('What caused D:', page=16)),
       pt(S('Why food salted or sugared: Preserves food or stops food rotting or kills micro-organisms', page=16), 0),
       pt(S('Microorganisms lose water (by osmosis)', page=16), 0, label=S('2. How it works:', page=16, piece=2, psep='. '))],
      'bio-2-6', 'membranes-and-osmosis', at(15, 'Q13', '(c)'), 24, fig='q13c-cells', tariff='questionTotal',
      decision=WHOLE + ' The scheme prints no tariff at all for Q13(c), where Q10-Q12(c) print "8 X 3"; the part '
               'total is the paper\'s "(24)".'),
    T('14a', 'Q14(a)', 'C',
      [M('(i)', 7), _C(7, 'Draw a labelled diagram of a typical virus.'),
       M('(ii)', 7, br=True), _C(7, 'Give a reason why a virus is considered to be non‐living.'),
       M('(iii)', 7, br=True), _C(7, 'Name two diseases in humans caused by viruses.'),
       M('(iv)', 7, br=True), _C(7, 'Name the method of reproduction used by bacteria.'),
       M('(v)', 7, br=True), _C(7, 'Name the three main bacterial shapes.')],
      [pt(S('Outer coat and DNA / RNA fragments'), 0, kind='criterion', label=S('Drawing to show:')),
       pt(S(LAB14, piece=1), 0, label=S('Labels: (2 points)', piece=1, psep=':')),
       pt(S(LAB14, piece=2), 0, label=S('Labels: (2 points)', piece=1, psep=':')),
       pt(S(VIRUS14, piece=1), 0),
       pt(S(VIRUS14, piece=2), 0, label=S(VIRUS14, piece=[1, 1], psep=['/', ':'])),
       anyn(S(DIS14, piece=[2, 1], psep=['e.g. ', '…']), 2, 0, open_list=True, note_sel=S(DIS14, piece=1, psep=', e.g.')),
       pt(S('Binary fission'), 0, label=S('Bacterial reproduction:'))]
      + [pt(S(SHAPES14, piece=n), 0, label=S('Bacterial shapes:')) for n in (1, 2, 3)],
      'bio-3-2', 'viruses-and-bacteria', at(16, 'Q14', '(a)'), 30, tariff='questionTotal',
      decision=WHOLE + ' The scheme prints "Drawing (3) / Labels 2(3)", which prices (i) only, and no tariff for '
               '(ii)-(v); the part total is the paper\'s "(30, 30)".'),
    T('14bi', 'Q14(b)(i)', 'C', _C(7, 'What is meant by the term endocrine?'),
      [pt(S('Ductless (gland) or secretes directly into blood or lymph'), 6)], 'bio-2-4', 'endocrine',
      SQ(16, 'Endocrine:'), 6, stem=[Q14B], fig='q14b-glands'),
] + [
    T(f'14bii-{x.lower()}', 'Q14(b)(ii)', 'C', _C(7, 'Name the endocrine glands labelled A and B in the diagram.'),
      [pt(S(name), 6)], 'bio-2-4', f'gland-{x.lower()}', at(16, 'Q14', '(b)', '(ii)'), 6, stem=[Q14B], fig='q14b-glands',
      labels=asked(L_GLANDS, x), item=(x.lower(), x), decision=EACH_ITEM)
    for x, name in [('A', 'Thyroid'), ('B', 'Pancreas')]
] + [
    T('14biii', 'Q14(b)(iii)', 'C', _C(7, 'What is a hormone?'), [pt(S('Chemical messenger'), 6)], 'bio-2-4', 'hormone',
      SQ(16, 'Hormone:'), 6, stem=[Q14B], fig='q14b-glands'),
] + [
    T(f'14biv-{x.lower()}', 'Q14(b)(iv)', 'C', _C(7, 'Name a hormone produced by gland A, and a hormone produced by gland B.'),
      [pt(S(name), 6, label=S(f'{x} produces:'))], 'bio-2-4', f'hormone-of-gland-{x.lower()}',
      at(16, 'Q14', '(b)', '(iv)'), 6, stem=[Q14B], fig='q14b-glands', labels=asked(L_GLANDS, x), item=(x.lower(), x),
      decision=EACH_ITEM)
    for x, name in [('A', 'Thyroxine'), ('B', 'Insulin')]
] + [
    T('14bv', 'Q14(b)(v)', 'C', _C(7, 'Give an example of a hormone used in medical treatment.'),
      [pt(S('A named valid hormone for medical treatment,', 'e.g. Oestrogen or progesterone ….'), 6)], 'bio-2-4',
      'hormones-in-medicine', SQ(16, 'Hormone for medical treatment:'), 6, stem=[Q14B], fig='q14b-glands'),
    T('14c', 'Q14(c)', 'C',
      [M('(i)', 7), _C(7, 'What is meant by the term asexual reproduction?'),
       M('(ii)', 7, br=True), _C(7, '1. Give two examples of natural vegetative propagation.'),
       _C(7, '2. State whether each of your examples involves a stem, a root, a bud, or a leaf.', br=True),
       M('(iii)', 7, br=True), _C(7, 'Name two methods gardeners use to artificially propagate plants.'),
       M('(iv)', 7, br=True), _C(7, 'Give two advantages to the plant of vegetative propagation.'),
       M('(v)', 7, br=True), _C(7, 'Give a disadvantage to the plant of vegetative propagation.')],
      [pt(S('Asexual reproduction: No gametes involved or one parent', page=17), 0),
       anyn(None, 2, 0, options=[S(*NAT14, page=17, piece=[2, n], psep=['e.g. ', '/']) for n in (1, 2, 3)],
            open_list=True, note_sel=S(*NAT14, page=17, piece=1, psep=', e.g.')),
       anyn(None, 2, 0, options=[S(*PART14, page=17, piece=[2, n], psep=['; ', '/']) for n in (1, 2, 3)],
            open_list=True, note_sel=S(*PART14, page=17, piece=1, psep=';')),
       anyn(None, 2, 0, options=[S(ART14, page=17, piece=n) for n in (1, 2, 3)]
            + [S(ART14, page=17, piece=[4, 1], psep=['/', '…'])], open_list=True,
            note_sel=S('Any 2 valid methods of artificial propagation; e.g.', page=17, piece=1, psep=';')),
       anyn(None, 2, 0, options=[S(ADV14, page=17, piece=[2, 1], psep=['e.g. ', ' /']),
                                 S(ADV14, page=17, piece=[2, 2, 1], psep=['e.g. ', '/ ', ' …'])],
            open_list=True, note_sel=S(ADV14, page=17, piece=1, psep=';')),
       pt(S('No widespread dispersal or more competition or', 'susceptible to same diseases ….', page=17), 0,
          label=S('Disadvantage:', page=17))],
      'bio-2-5', 'vegetative-propagation', SQ(17, '(c)', paired=MARKER, bare=True), 30, stem=[Q14C],
      tariff='questionTotal',
      decision=WHOLE + ' The scheme prints no tariff at all for Q14(c); the part total is the paper\'s "(30, 30)".'),
] + [
    T(f'15ai-{x.lower()}', 'Q15(a)(i)', 'C', _C(8, 'Name the parts labelled A, B, C.'), [pt(S(name), 6)], 'bio-2-4',
      f'neuron-part-{x.lower()}', at(17, 'Q15', '(a)', '(i)'), 6, stem=[Q15A], fig='q15a-neuron',
      labels=asked(L_NEURON, x), item=(x.lower(), x), decision=EACH_ITEM)
    for x, name in [('A', 'Dendrite'), ('B', 'Axon'), ('C', 'Cell body [allow nucleus]')]
] + [
    T('15aii', 'Q15(a)(ii)', 'C', _C(8, 'Which part of the motor neuron receives impulses?'),
      [pt(S('A or dendrite or Cell Body or C'), 6)], 'bio-2-4', 'receiving-impulses', SQ(17, 'Part that receives impulses:'),
      6, stem=[Q15A], fig='q15a-neuron'),
    T('15aiii', 'Q15(a)(iii)', 'C', _C(8, 'Name the substance produced by the Schwann cells, which helps to speed up the nerve',
                                       'impulse.'),
      [pt(S('Myelin'), 6)], 'bio-2-4', 'myelin', SQ(17, 'Schwann cell substance:'), 6, stem=[Q15A], fig='q15a-neuron'),
    T('15aiv', 'Q15(a)(iv)', 'C', _C(8, 'Name two other types of nerve cells found in the body.'),
      [pt(S(NEURONS15, piece=1), 6), pt(S(NEURONS15, piece=[2, 1], psep=['/', ' (2']), 6)], 'bio-2-4', 'types-of-neuron',
      SQ(17, 'Other neuron types:'), 12, stem=[Q15A], fig='q15a-neuron',
      decision='The scheme prints "Sensory / interneuron (2 points)": two responses, each its own row.'),
    T('15av', 'Q15(a)(v)', 'C', _C(8, 'Name both parts of the central nervous system.'),
      [pt(S(CNS15, piece=1, psep=' and '), 6), pt(S(CNS15, piece=[2, 1], psep=[' and ', ' (2']), 6)], 'bio-2-4',
      'central-nervous-system', SQ(17, 'Parts of CNS:', paired=COMPRESSED), 12, stem=[Q15A], fig='q15a-neuron',
      decision='The scheme prints "Brain and spinal cord (2 points)": two responses, each its own row.'),
] + [
    T(f'15bi-{x.lower()}', 'Q15(b)(i)', 'C', _C(8, 'Name the structures labelled A, B, C.'), [pt(S(name), 6)], 'bio-2-6',
      f'kidney-structure-{x.lower()}', at(17, 'Q15', '(b)', '(i)'), 6, stem=[Q15B], fig='q15b-kidney',
      labels=asked(L_KIDNEY, x), item=(x.lower(), x), decision=EACH_ITEM)
    for x, name in [('A', '(Renal) vein'), ('B', '(Renal) artery'), ('C', 'Ureter')]
] + [
    T('15bii', 'Q15(b)(ii)', 'C', _C(8, 'Which letter shows the structure that would contain urine?'), [pt(S('C'), 6)],
      'bio-2-6', 'urine-in-the-ureter', SQ(17, 'Contains urine:'), 6, stem=[Q15B], fig='q15b-kidney'),
    T('15biii', 'Q15(b)(iii)', 'C', _C(8, 'Which other structure is attached to the kidney by part C?'),
      [pt(S('Bladder'), 6)], 'bio-2-6', 'bladder', SQ(17, 'Attached to kidney by C:'), 6, stem=[Q15B], fig='q15b-kidney',
      labels=asked(L_KIDNEY, 'C')),
    T('15biv', 'Q15(b)(iv)', 'C', _C(8, 'The kidney is an organ of excretion. What is meant by the term excretion?'),
      [pt(S(EXCR15, piece=1), 6), pt(S(EXCR15, piece=[2, 1], psep=['/', ' (2']), 6)], 'bio-2-6', 'excretion',
      SQ(17, 'Excretion:'), 12, stem=[Q15B], fig='q15b-kidney',
      decision='The scheme prints "Removal of waste / made in the body (2 points)": two responses, each its own row.'),
    T('15bv', 'Q15(b)(v)', 'C', _C(8, 'Name two other excretory organs in the human body.'),
      [anyn(S(ORGANS15, piece=[2, 1], psep=['e.g. ', ' …']), 2, 6, open_list=True,
            note_sel=S(ORGANS15, piece=1, psep=', e.g.'))], 'bio-2-6', 'excretory-organs', SQ(17, 'Excretory organs:'),
      12, stem=[Q15B], fig='q15b-kidney'),
    T('15c', 'Q15(c)', 'C',
      [M('(i)', 9), _C(9, 'Name the kingdom to which each belongs.'),
       M('(ii)', 9, br=True), _C(9, 'Name structure A and structure B.'),
       M('(iii)', 9, br=True), _C(9, 'Name a structure that is present in both cells.'),
       M('(iv)', 9, br=True), _C(9, 'Give an example of the economic importance of yeast.'),
       M('(v)', 9, br=True), _C(9, '1. What is meant by the term saprophyte?'),
       _C(9, '2. What is meant by the term parasite?', br=True)],
      [pt(S('Fungi'), 0, label=S('Yeast:')), pt(S('Protista'), 0, label=S('Amoeba:')),
       pt(S('Bud'), 0, label=S('A:')), pt(S('Pseudopod or false foot'), 0, label=S('B:')),
       pt(S('Nucleus or membrane or other valid part….'), 0, label=S('Present in both:')),
       pt(S('Economic importance of yeast: Brewing or baking'), 0),
       pt(S('Saprophyte: Organism that feeds on dead (organic) material'), 0),
       pt(S('Organism that feeds on live (organic) material and causes harm'), 0, label=S('2. Parasite:', piece=2, psep='. '))],
      'bio-3-2', 'yeast-and-amoeba', SQ(18, '(c)', paired=MARKER, bare=True), 30, stem=[Q15C], fig='q15c-cells',
      labels=L_CELLS, tariff='questionTotal',
      decision=WHOLE + ' The scheme prints "6 + 8(3)", nine responses, but eight answers: Fungi and Protista, Bud and '
               'Pseudopod, one each for (iii) and (iv), and the two definitions in (v); the part total is the paper\'s '
               '"(30, 30)".'),
]

FIGURES = {
    # key suffix: (doc, page, rect in PDF points, credit, letters, alt, solution[, masks])
    'q2-division': ('038', 3, (85, 350, 510, 485), SEC, ['A', 'B', 'C', 'D'],
                    'Four drawings of human cheek cells, labelled A to D below them: A, an oval cell with a dark line '
                    'across its middle and fine fibres fanning out to either end; B, a round cell with a tangled dark '
                    'mass at its centre; C, a cell pinched in two at its middle, with a small dark band in each half; '
                    'D, a round cell with a double dark band at its centre and fibres fanning out to either side.',
                    False),
    'q3-table': ('038', 4, (52, 50, 545, 360), SEC, [],
                 'Question 3 as printed: "Choose each term from the following list and place it in Column B to match '
                 'a description in Column A. The first one has been completed as an example." The list reads Flower '
                 '(struck through), Meristem, Dermal, Vascular, Leaf, Lenticel. Below it a two-column table headed '
                 'Column A and Column B: the example row "Attracts insects for pollination" with "Flower", then (a) '
                 'Plant organ for photosynthesis, (b) Tissues for transport in plants, (c) Tissues on outer plant '
                 'surface, (d) A group of rapidly dividing plant cells and (e) An opening on the stem for gas '
                 'exchange, each with an empty Column B cell.', False),
    'q4-cycle': ('038', 4, (385, 362, 565, 546), SEC, ['A', 'B'],
                 'The human menstrual cycle drawn as a circle with the days 1 to 28 numbered round its rim. A shaded '
                 'sector labelled A spans days 1 to 5; a darker sector labelled B, with the word OVULATION, spans '
                 'about days 12 to 16 at the bottom; the rest of the circle is white.', False),
    'q6-microscope': ('038', 5, (220, 333, 375, 490), SEC, ['A', 'B', 'C'],
                      'Photograph of a laboratory microscope with three label lines: A to the tilted tube at the top, '
                      'B to the flat black platform at the middle left, and C to a short barrel pointing down above '
                      'the platform.', False),
    'q10-badgers': ('040', 3, (86, 623, 512, 675), SEC, [],
                    'Table of three columns: Badgers caught and marked in session 1, 180; Badgers caught in session 2, '
                    '150; Badgers caught in session 2, marked from session 1, 40.', False),
    'q12c-skeleton': ('040', 5, (220, 318, 378, 503), SEC, ['A', 'B', 'C', 'D'],
                      'Drawing of part of the human skeleton: a long bone, cut open to show a speckled core, whose '
                      'rounded upper end fits into a socket in a broad bone above it. Label lines: A to the broad '
                      'upper bone, C to a circle drawn round the place where the rounded end meets the socket, D to '
                      'the speckled core inside the long bone, and B to the shaft of the long bone near the bottom.',
                      False),
    'q13b-equation': ('040', 6, (140, 150, 372, 172), SEC, [],
                      'The equation as printed: Glucose + X, an arrow pointing right, Water + Y + energy.', False),
    'q13c-cells': ('040', 6, (200, 536, 337, 655), SEC, ['A', 'B', 'C', 'D'],
                   'Four drawings of the same long plant cell, labelled A to D: in A the shaded contents fill the '
                   'space inside the wall; in B they have shrunk into a rounded block clear of the wall; in C they '
                   'fill the cell but are drawn in at both ends; in D they have pulled away from the wall in curved '
                   'bays down both sides.', False),
    'q14b-glands': ('040', 7, (96, 206, 502, 375), SEC, ['A', 'B'],
                    'Two drawings. Left: a gland wrapped round the front of the windpipe below the larynx, labelled '
                    'A, with the windpipe below it labelled Trachea. Right: a long lobed gland labelled B lying along '
                    'the curve of a looped tube labelled Duodenum, with ducts running into the loop.', False),
    'q15a-neuron': ('040', 8, (168, 76, 484, 266), SEC, ['A', 'B', 'C'],
                    'Diagram of a motor neuron. A points to the tip of one of the short branches round the cell\'s '
                    'swollen centre, B to the long fibre leaving it, and C to the swollen centre beside its dark oval '
                    'nucleus; the oval sheaths along the long fibre are labelled Schwann cell, and the fibre ends in '
                    'branches at the right.', False),
    'q15b-kidney': ('040', 8, (180, 457, 374, 643), SEC, ['A', 'B', 'C'],
                    'Diagram of a human kidney cut lengthways, with three tubes at its inner edge: A, the upper tube, '
                    'carries an arrow pointing away from the kidney; B, the speckled tube below it, carries an arrow '
                    'pointing into the kidney; C is the tube running straight down from the kidney.', False),
    'q15c-cells': ('040', 9, (157, 66, 441, 212), SEC, ['A', 'B'],
                   'Two single-celled organisms. Left, labelled Yeast: a large oval cell with a smaller oval cell '
                   'attached at its top, the smaller one bracketed and labelled A. Right, labelled Amoeba: an '
                   'irregular cell with a label line to a large clear vacuole, labelled Contractile vacuole, and a '
                   'label line B to one of the projections from its edge.', False),
}
