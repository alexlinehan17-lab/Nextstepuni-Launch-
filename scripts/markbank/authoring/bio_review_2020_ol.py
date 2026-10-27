"""Biology 2020 Ordinary Level — reviewed task ledger, carded from the papers for the first time.

Independent visual sweep (2026-10-14), every page rendered and read:
  * LC025GLP038EV (Sections A and B and Answerbook), 40 pages: p1 cover,
    p2 instructions, p3-p6 Section A Questions 1-6, p7-p9 Section B
    Questions 7-9, p10 Section C answerbook instructions, p11-p35 ruled
    answer pages, p36-p39 graph paper, p40 back cover with the copyright
    notice. No acknowledgements page.
  * LC025GLP040EV (Section C), 8 pages: p1 cover, p2-p7 Questions 10-15,
    p8 back cover with the copyright notice.
  * LC025GLP000EV (marking scheme), 16 pages: p1 cover, p2 note, p3
    introduction, p4 cancelled and surplus answers, p5-p14 Questions 1-15,
    p15 blank, p16 back cover.

The paper keeps the long-standing shape: any five of Section A's six
questions, any two of Section B's three, any four of Section C's six, and
Questions 14 and 15 are each any two of (a), (b), (c). Every printed question
is carded. No Biology card existed for 2020 before this review.

This scheme prints no reprint of any question: each answer stands under its
own question number, letter and roman. Every task is therefore anchored on
its own part marker, found by walking the scheme's numbering down to it
(SQ path), and is recorded as such.

Section A and B tariffs are the scheme's ordered splits, carded at their
first rate: "8+8+2+2(1)" (Q1, Q4: five responses), "7+7+2+4(1)" (Q2, Q3,
Q5, Q6: seven), "(5 + 1)" for every Section B (a) and "2(9)+6(1)" for every
(b). Section C prints a mark per row.

The paper prints Q14(c)'s second part as "(iii)" and its third as "(iii)"
again; the scheme numbers them (ii) and (iii), and so do the cards. Lists the
scheme prices entry by entry ("A = Larynx/ B = Trachea/ ...", "1=B/ 2=A/
...") are carded one entry per card, each its own slice of the printed line.
No printed choice is marked differently per option: Q15(a)(iv)'s eye or ear
shares one disorder row and one treatment row.
"""
from bio_review_lib import Q, SQ, S, M, pt, anyn, T, L

YEAR, LEVEL = 2020, 'ol'
REVIEWED_AT = '2026-10-14'

SOURCES = {
    '038': {'path': 'examiner-reports/biology/papers/2020-ol-038-paper.pdf',
            'fileid': 'LC025GLP038EV.pdf',
            'sha256': '7f533d8ea97af0160bc297528779a24d9ba7a22bc6745d7e6406d52d21d4d847',
            'pages': 40},
    '040': {'path': 'examiner-reports/biology/papers/2020-ol-040-paper.pdf',
            'fileid': 'LC025GLP040EV.pdf',
            'sha256': '88f563418ead0813185bf5e88f8e58b48ae57b531c51c57d022da9b434cee6dd',
            'pages': 8},
    'scheme': {'path': 'examiner-reports/biology/schemes/2020-ol.pdf',
               'fileid': 'LC025GLP000EV.pdf',
               'sha256': 'f9882d2413e659b8071ed262d09c18d2054f4b667194edf99a71dd4538b1c219',
               'pages': 16},
}

PAGE_ROLES = {
    '038': {1: 'cover', 2: 'instructions', **{p: 'questions' for p in range(3, 10)},
            10: 'answerbook-instructions', **{p: 'answer-pages' for p in range(11, 36)},
            **{p: 'graph-paper' for p in range(36, 40)}, 40: 'back-cover'},
    '040': {1: 'cover', **{p: 'questions' for p in range(2, 8)}, 8: 'back-cover'},
    'scheme': {1: 'cover', 2: 'note', 3: 'introduction', 4: 'marking-examples',
               **{p: 'marking' for p in range(5, 15)}, 15: 'blank', 16: 'back-cover'},
}

QUESTION_TOTALS = {
    **{n: 20 for n in range(1, 7)}, **{n: 30 for n in range(7, 10)},
    **{n: 60 for n in range(10, 14)},
}
PART_TOTALS = {
    **{(n, 'a'): 9 for n in range(10, 14)}, **{(n, 'b'): 27 for n in range(10, 14)},
    **{(n, 'c'): 24 for n in range(10, 14)},
    **{(n, x): 30 for n in (14, 15) for x in 'abc'},
}


def _ladder(notation):
    """An ordered split as the scheme prints it ("7+7+2+4(1)", "2(9)+6(1)")."""
    steps = []
    for term in notation.split('+'):
        n, _, m = term.strip().partition('(')
        steps += [int(m.rstrip(')'))] * int(n) if m else [int(n)]
    return {'steps': steps, 'notation': notation}


LADDERS = {
    1: _ladder('8+8+2+2(1)'), 4: _ladder('8+8+2+2(1)'),
    **{q: _ladder('7+7+2+4(1)') for q in (2, 3, 5, 6)},
    **{(n, 'a'): _ladder('5 + 1') for n in (7, 8, 9)},
    **{(n, 'b'): _ladder('2(9)+6(1)') for n in (7, 8, 9)},
}

CHECKSUMS = {
    1: {8: 5}, 4: {8: 5}, **{q: {7: 7} for q in (2, 3, 5, 6)},
    **{(n, 'a'): {5: 2} for n in (7, 8, 9)}, **{(n, 'b'): {9: 8} for n in (7, 8, 9)},
    **{(n, 'a'): {3: 3} for n in range(10, 14)}, **{(n, 'b'): {3: 9} for n in range(10, 14)},
    **{(n, 'c'): {3: 8} for n in range(10, 14)},
    (14, 'a'): {3: 10}, (14, 'b'): {3: 10}, (14, 'c'): {3: 9, 1: 3},
    **{(15, x): {3: 10} for x in 'abc'},
}

SCAN_PAGES = {'038': range(2, 10), '040': range(2, 8)}
SELECTION_SCAN = [
    ('038', 2, 'or', 'Instructions: "blue or black pen", not a question.'),
    ('038', 2, 'any five', 'Section A rubric: whole-question choice; every question is carded.'),
    ('038', 2, 'any two', 'Section B rubric: whole-question choice; every question is carded.'),
    ('038', 2, 'any four', 'Section C rubric: whole-question choice; every question is carded.'),
    ('038', 3, 'any five', 'Section A rubric repeated.'),
    ('038', 3, 'the following', 'Q1 lead-in: every part asked.'),
    ('038', 3, 'the following', 'Q2 lead-in: every statement asked.'),
    ('038', 3, 'or', 'Q2 "true (T) or false (F)": the answer options.'),
    ('038', 3, 'or', 'Q2 "T or F": the answer options.'),
    ('038', 5, 'choose', 'Q4 "Choose each term": every description matched, one card per lettered part.'),
    ('038', 5, 'the following', 'Q4 list of terms: the options.'),
    ('038', 5, 'the following', 'Q5 list of cell names: the options; every box asked, one card per letter.'),
    ('038', 7, 'any two', 'Section B rubric repeated.'),
    ('038', 7, 'the following', 'Q7(b) lead-in: every part asked.'),
    ('038', 8, 'or', 'Q8(b)(ii) "a plant or producer": the same ask.'),
    ('038', 9, 'the following', 'Q9(b) "recorded the following": a reference to the table.'),
    ('040', 2, 'any four', 'Section C rubric repeated.'),
    ('040', 2, 'the following', 'Q10(a) lead-in: every term asked, one card per roman.'),
    ('040', 2, 'the following', 'Q10(b) "the following article": a reference.'),
    ('040', 2, 'either', 'Q10(b) passage "either killed on the road": passage text.'),
    ('040', 2, 'or', 'Q10(b) passage "hunted or die from disease": passage text.'),
    ('040', 2, 'the following', 'Q10(c) list of equipment: every piece asked, one card each.'),
    ('040', 2, 'any one', 'Q10(c)(iii) "any one abiotic factor": one response.'),
    ('040', 4, 'both', 'Q12(c)(iii) "common to both structures": description.'),
    ('040', 5, 'either', 'Q13(c) "either monocotyledonous or dicotyledonous": description.'),
    ('040', 5, 'or', 'Q13(c) same description.'),
    ('040', 5, 'or', 'Q13(c)(i) "A or B": the answer options.'),
    ('040', 5, 'or', 'Q13(c)(iii) "A or B": the answer options.'),
    ('040', 5, 'the following', 'Q13(c)(vi) tissue types: the options.'),
    ('040', 5, 'the following', 'Q13(c)(vi) functions: every function asked, one card each.'),
    ('040', 6, 'any two', 'Q14 "any two of (a), (b), (c)": whole-part choice; every part is carded.'),
    ('040', 6, 'the following', 'Q14(c)(iii) "the following labels": all three labels asked.'),
    ('040', 7, 'any two', 'Q15 "any two of (a), (b), (c)": whole-part choice; every part is carded.'),
    ('040', 7, 'the following', 'Q15(a)(i) parts list: every part asked, one card each.'),
    ('040', 7, 'either', 'Q15(a)(iv) "either the eye or the ear": marked on one disorder row and one treatment row; '
                         'one card.'),
    ('040', 7, 'or', 'Q15(a)(iv), same choice.'),
    ('040', 7, 'the following', 'Q15(b)(i) functions list: every function asked, one card each.'),
]

ROUTES = {}

SEC = 'State Examinations Commission'
NO_REPRINT = 'The scheme prints no reprint of any question: anchored on its own part marker.'
EACH_ITEM = 'A list the scheme prices entry by entry: one card per entry, each its own slice of the printed line.'


def _A(page, start, end=None, **kw):
    return Q(page, start, end, doc='038', **kw)


def _C(page, start, end=None, **kw):
    return Q(page, start, end, doc='040', **kw)


def at(page, q, *path_and_marker):
    """The scheme's own part marker under its question (and letter)."""
    *path, marker = path_and_marker
    return SQ(page, marker, path=[str(q), *path], paired=NO_REPRINT, bare=True)


def item(page, n, end, anchor, doc='040'):
    """One entry of a printed numbered list."""
    return Q(page, f'{n}.', end, doc=doc, after=anchor, br=True)


Q1 = [_A(3, 'A student eats a meal containing fish and potatoes.'),
      _A(3, 'Use your knowledge of nutrition to answer the following questions about this meal.')]
Q2 = _A(3, 'Indicate whether the following statements are true (T) or false (F) by drawing a circle around',
        'T or F in each case.')
Q3 = [_A(4, 'The diagram shows part of the carbon cycle with several arrows missing from the diagram.'),
      _A(4, 'Answer the questions that follow by inserting arrows on the diagram as appropriate.')]
Q4 = _A(5, 'Choose each term from the following list and place it in Column B to match a description in',
        'The first one has been completed as an example.')
Q5 = _A(5, 'A selection of different cells is shown below.', 'shown below.')
Q5ASK = _A(5, 'Select the cell name from the following list and', 'as an example.')
Q6 = _A(6, 'The diagram shows the label found on blood stored for transfusion in a hospital.')
Q7B = _A(7, 'Answer the following questions in relation to an investigation you carried out to',
         'demonstrate osmosis.')
Q8B = _A(8, 'A student carried out a quantitative survey to estimate the % cover of a number of',
         'plants in an Irish ecosystem close to her school.')
Q8BV = _A(8, 'The diagram shows a plant found in one of the sample areas.', 'of intersection is directly above the plant.')
Q9B = _A(9, 'A student carried out an investigation into the effect of IAA growth regulator on plant',
         'tissue and recorded the following.')
Q10A = _C(2, 'Explain the following terms used in ecology:')
Q10B = [_C(2, 'Read the following article and answer the questions that follow it.'),
        _C(2, 'In the countryside foxes mostly feed on small', 'white‐tailed eagle.'),
        _C(2, '(Based on an article in RTE.ie', '2018)')]
Q10C = _C(2, 'A group of students collected information on the animals found in an ecosystem close',
          'the following pieces of equipment:')
Q11C = _C(3, 'The cross between two dogs with different coat colours is displayed below.', 'in your answer book.')
Q12B = _C(4, 'The diagram shows the human breathing system.')
Q12C = _C(4, 'The human body absorbs material into the bloodstream for transport to body cells.', 'human body.')
Q13C = _C(5, 'Flowering plants can be classified as either monocotyledonous (monocot) or', 'questions that follow.')
Q13CVI = [_C(5, 'Plants contain the following three tissue types:'), _C(5, 'A. Dermal'), _C(5, 'B. Ground'),
          _C(5, 'C. Vascular'), _C(5, 'Match the correct plant tissue type with each of the following functions:')]
Q14A = _C(6, 'A student is carrying out an experiment, using the equipment below, to investigate the',
          'products of anaerobic respiration (fermentation).')
Q14C = _C(6, 'Rhizopus is a harmful heterotrophic fungus.')
Q15 = _C(7, 'The diagram shows a section through the human eye.')
Q15AI = _C(7, 'In your answer book, state which letter represents each of the following parts:')
Q15BI = _C(7, 'In your answer book, state which letter represents the parts of the flower that',
           'carry out the following functions:')
Q15C = _C(7, 'The diagram shows the human male reproductive system.')

LUNGS = 'A = Larynx/ B = Trachea/ C = Bronchiole/ D = Bronchus'
CELL = ('A=Vacuole/ B=Cell Wall/ C=Cell membrane/', 'D=Mitochondria')
MALE = 'A = Penis/ B = Urethra/ C = Sperm duct/ D = Testes'

L_CARBON = [L('A', S('Decomposition', page=5), False)]
L_LUNGS = [L(x, S(LUNGS, page=11, piece=[i, 2], psep=['/', '=']), False) for i, x in enumerate('ABCD', 1)]
L_STRUCTURES = [L(x, S('A = Villus/ B = Alveolus', page=11, piece=[i, 2], psep=['/', '=']), False)
                for i, x in enumerate('AB', 1)]
L_CELL = [L(x, S(*CELL, page=13, piece=[i, 2], psep=['/', '=']), False) for i, x in enumerate('ABCD', 1)]
L_EYE = [L('C', _C(7, 'Optic Nerve', after='2. Lens'), True)]
L_MALE = [L(x, S(MALE, page=14, piece=[i, 2], psep=['/', '=']), False) for i, x in enumerate('ABCD', 1)]


def asked(keys, *letters):
    return [dict(k, asked=k['letter'] in letters) for k in keys]


TASKS = [
    # ------------------------------------------------------------ Section A --
] + [
    T(f'1{x}', f'Q1({x})', 'A', _A(3, ask), [pt(S(*ans), 8)], 'bio-1-2', concept, at(5, 1, f'({x})'), 8,
      stem=Q1)
    for x, ask, ans, concept in [
        ('a', 'State a reason why the body needs food.', ('Energy/materials for growth / repair',), 'why-food'),
        ('b', 'Name the main source of protein in this meal.', ('Fish',), 'protein-source'),
        ('c', 'Name the main source of carbohydrate in this meal.', ('Potatoes',), 'carbohydrate-source'),
        ('d', 'Name the three chemical elements found in all carbohydrates.', ('C/ H/ O/ (all or nothing)',),
         'elements-in-carbohydrates'),
        ('e', 'Suggest one function of fibre if it was added to this meal.',
         ('Prevent constipation/stimulate peristalsis / helps bowels', 'work /prevents bowel cancer'),
         'function-of-fibre')]
] + [
    T(f'2{x}', f'Q2({x})', 'A', _A(3, ask), [pt(S(ans), 7)], topic, concept, at(5, 2, f'({x})'), 7, stem=[Q2])
    for x, ask, ans, topic, concept in [
        ('a', 'Amoeba is in the kingdom Protista.', 'True', 'bio-1-1', 'amoeba-kingdom'),
        ('b', 'Fungi have cell walls.', 'True', 'bio-3-2', 'fungal-cell-walls'),
        ('c', 'Members of Monera have no nuclei.', 'True', 'bio-1-1', 'monera'),
        ('d', 'All members of the animal kingdom are saprophytes.', 'False', 'bio-1-1', 'animal-nutrition'),
        ('e', 'Members of the plant kingdom have cellulose cell walls.', 'True', 'bio-1-3', 'plant-cell-walls'),
        ('f', 'All fungi are parasites.', 'False', 'bio-3-2', 'fungal-nutrition'),
        ('g', 'Viruses are not members of any kingdom.', 'True', 'bio-1-1', 'viruses-and-kingdoms')]
] + [
    T(f'3{x}', f'Q3({x})', 'A', _A(4, ask), [pt(S(*ans), 7, **kw)], 'bio-3-2', concept, at(5, 3, f'({x})'), 7,
      stem=Q3, qfig='q3-carbon', labels=lab,
      decision='The carbon cycle the arrows are drawn on is shown as the question\'s own print.')
    for x, ask, ans, kw, concept, lab in [
        ('a', 'Draw one arrow labelled R on the diagram to represent respiration.',
         ('Arrow R humus/ animals/ plants to atmosphere',), {'kind': 'criterion'}, 'respiration-arrow', None),
        ('b', 'Draw one arrow labelled P on the diagram to represent photosynthesis.',
         ('Arrow P = atmosphere to plants',), {'kind': 'criterion'}, 'photosynthesis-arrow', None),
        ('c', 'Draw one arrow labelled B on the diagram to represent burning.', ('Arrow B = fuel to atmosphere',),
         {'kind': 'criterion'}, 'burning-arrow', None),
        ('d', 'Name a carbon compound plants use to store food.', ('Starch /oil',), {}, 'carbon-stores', None),
        ('e', 'Name the process shown by arrow A.', ('Decomposition',), {}, 'decomposition', None),
        ('f', 'Name a group of organisms which carry out the process labelled A.',
         ('Bacteria/ fungi/or named e.g. mushroom / moulds',), {}, 'decomposers', asked(L_CARBON)),
        ('g', 'Suggest one way of reducing high levels of carbon dioxide in the atmosphere.',
         ('Plant more trees / stop burning fossil fuels / use electric', 'cars / or other valid reason'), {},
         'reducing-carbon-dioxide', None)]
] + [
    T(f'4{x}', f'Q4({x})', 'A', _A(5, ask, end), [pt(S(ans), 8)], 'bio-2-1', concept, at(6, 4, f'({x})'), 8,
      stem=[Q4], qfig='q4-table')
    for x, ask, end, ans, concept in [
        ('a', 'An advantage of immobilised enzymes', None, 'Reusable', 'immobilised-enzyme-advantage'),
        ('b', 'How you would keep the temperature', 'constant', 'Water bath', 'constant-temperature'),
        ('c', 'The material an enzyme works on', None, 'Substrate', 'substrate'),
        ('d', 'This is formed at the end of an enzyme', 'reaction', 'Product', 'product'),
        ('e', 'Converts starch into maltose', None, 'Amylase', 'amylase')]
] + [
    T(f'5{x}', f'Q5({x})', 'A', Q5ASK, [pt(S(ans), 7)], topic, concept, at(6, 5, f'({x})'), 7, stem=[Q5],
      qfig='q5-cells', decision='Each lettered box under a drawing is its own part; the drawing it names is '
                                'shown in the question\'s own print.')
    for x, ans, topic, concept in [
        ('a', 'Cheek cell', 'bio-1-3', 'cheek-cell'), ('b', 'Amoeba', 'bio-1-1', 'amoeba'),
        ('c', 'Root hair', 'bio-2-6', 'root-hair'), ('d', 'Red blood cell', 'bio-2-6', 'red-blood-cell'),
        ('e', 'Xylem', 'bio-2-6', 'xylem-vessel'), ('f', 'Sperm', 'bio-2-5', 'sperm-cell'),
        ('g', 'Neuron', 'bio-2-4', 'neuron')]
] + [
    T('6a', 'Q6(a)', 'A', _A(6, 'Name the liquid part of blood.'), [pt(S('Plasma/ water'), 7)], 'bio-2-6',
      'plasma', at(6, 6, '(a)'), 7, stem=[Q6], fig='q6-label'),
    T('6b', 'Q6(b)', 'A', _A(6, 'State one function of this liquid.'),
      [pt(S('Transport food/ maintaining temperature'), 7)], 'bio-2-6', 'function-of-plasma', at(6, 6, '(b)'), 7,
      stem=[Q6, M('(a)', 6), _A(6, 'Name the liquid part of blood.')], fig='q6-label'),
    T('6c', 'Q6(c)', 'A', _A(6, 'What may be removed from blood to prevent it clotting during storage?'),
      [pt(S('Platelets/ clotting protein'), 7)], 'bio-2-6', 'preventing-clotting', at(6, 6, '(c)'), 7,
      stem=[Q6], fig='q6-label'),
    T('6d', 'Q6(d)', 'A', _A(6, 'The diagram shows blood group AB. Name two other blood groups.'),
      [anyn(S('A, B, O'), 2, 7, sep=',', note_sel=S('any two'))], 'bio-2-6', 'blood-groups', at(6, 6, '(d)'), 14,
      stem=[Q6], fig='q6-label'),
    T('6e', 'Q6(e)', 'A', _A(6, 'Name the blood cells that transport oxygen in the body.'),
      [pt(S('Red blood cells'), 7)], 'bio-2-6', 'red-blood-cells', at(6, 6, '(e)'), 7, stem=[Q6], fig='q6-label'),
    T('6f', 'Q6(f)', 'A', _A(6, 'Name the blood cells that produce antibodies to fight infection.'),
      [pt(S('White blood cells'), 7)], 'bio-2-4', 'white-blood-cells', at(6, 6, '(f)'), 7, stem=[Q6],
      fig='q6-label'),
    # ------------------------------------------------------------ Section B --
    T('7ai', 'Q7(a)(i)', 'B', _A(7, 'Give a reason why living cells need water.'),
      [pt(S('Temperature regulation/ transport/ use in chemical', 'reaction/ solvent / or other valid reason'), 5)],
      'bio-1-2', 'why-cells-need-water', at(7, 7, '(a)', '(i)'), 5),
    T('7aii', 'Q7(a)(ii)', 'B', _A(7, 'State a function of a selectively permeable membrane.'),
      [pt(S('Allows passage of some molecules'), 5)], 'bio-1-3', 'selectively-permeable-membranes',
      at(7, 7, '(a)', '(ii)'), 5),
    T('7bi', 'Q7(b)(i)', 'B', _A(7, 'Name one piece of apparatus and one solution you used during your investigation.'),
      [anyn(S('Test tube (or valid named vessel)/ sugar solution'), 2, 9)], 'bio-2-6', 'osmosis-apparatus',
      at(7, 7, '(b)', '(i)'), 18, stem=[Q7B],
      decision='One piece of apparatus and one solution: two responses on the printed line.'),
] + [
    T(f'7b{r}', f'Q7(b)({r})', 'B', _A(7, *ask), [pt(S(*ans), 9)], 'bio-2-6', concept, at(7, 7, '(b)', f'({r})'), 9,
      stem=[Q7B])
    for r, ask, ans, concept in [
        ('ii', ('What control was used?',), ('Boiled potato/ or distilled water (in ‘visking’ tube)',),
         'osmosis-control'),
        ('iii', ('What did you use as a selectively permeable membrane?',), ('‘Visking’ tubing/ or potato tissue',),
         'membrane-used'),
        ('iv', ('What information did you record at the start of the investigation?',),
         ('Mass/ turgid/ amount (volume) in tube',), 'starting-record'),
        ('v', ('What did you observe during the investigation that showed osmosis had occurred?',),
         ('Increase in mass/ more liquid in the tube/ idea of fatter', 'and more full'), 'evidence-of-osmosis'),
        ('vi', ('What did you conclude from your observations about the direction of water', 'movement during osmosis?'),
         ('From high water concentration to low water', 'concentration'), 'direction-of-osmosis'),
        ('vii', ('Name a simple food preservation technique linked to osmosis.',),
         ('Pickling/ high salt or sugar solution/ smoking/ or other', 'valid method'), 'osmosis-in-preservation')]
] + [
    T('8ai', 'Q8(a)(i)', 'B', _A(8, 'What is a qualitative survey?'),
      [pt(S('Whether an organism is present or not'), 5)], 'bio-3-1', 'qualitative-survey', at(7, 8, '(a)', '(i)'), 5),
    T('8aii', 'Q8(a)(ii)', 'B', [_A(8, 'Complete the statement below by placing the missing word in the answer box.'),
                                 _A(8, '“Flora is to plants as', 'is to animals”.', br=True)],
      [pt(S('Fauna'), 5)], 'bio-3-1', 'fauna', at(7, 8, '(a)', '(ii)'), 5),
] + [
    T(f'8b{r}', f'Q8(b)({r})', 'B', _A(8, *ask), rows, 'bio-3-1', concept, at(7, 8, '(b)', f'({r})'), total,
      stem=stem, fig=fig)
    for r, ask, rows, concept, total, stem, fig in [
        ('i', ('Name an ecosystem she may have studied.',), [pt(S('Grassland/ or other valid named ecosystem'), 9)],
         'naming-an-ecosystem', 9, [Q8B], None),
        ('ii', ('Name a plant or producer found in the ecosystem named in (i) above.',),
         [pt(S('Grass/ (or valid example linked to stated example in (i))'), 9)], 'a-producer', 9,
         [Q8B, M('(i)', 8), _A(8, 'Name an ecosystem she may have studied.')], None),
        ('iii', ('Name an instrument the student may have used to select an area for study.',), [pt(S('Quadrat'), 9)],
         'quadrat', 9, [Q8B], None),
        ('iv', ('How did the student avoid bias in the investigation?',),
         [pt(S('Throw behind back or randomly (over shoulder)'), 9)], 'avoiding-bias', 9, [Q8B], None),
        ('v', ('How many hits would the student record for this plant?',), [pt(S('4'), 9)], 'counting-hits', 9,
         [Q8B, Q8BV], 'q8-grid'),
        ('vi', ('Calculate the % cover for the plant in this sample area.',),
         [pt(S('16%'), 18, units=[9, 9], note_sel=S('(2 points)'))], 'percentage-cover', 18, [Q8B, Q8BV], 'q8-grid'),
        ('vii', ('What step could the student do next to improve the reliability of the survey?',),
         [pt(S('Repeat or calculate average'), 9)], 'reliable-surveys', 9, [Q8B], None)]
] + [
    T('9ai', 'Q9(a)(i)', 'B', _A(9, 'Name a growth response of a plant to a stimulus.'),
      [pt(S('Phototropism/ or geotropism/ or other valid named', 'tropism'), 5)], 'bio-2-4', 'tropisms',
      at(8, 9, '(a)', '(i)'), 5),
    T('9aii', 'Q9(a)(ii)', 'B', _A(9, 'Give one example where this growth response is important to a germinating seed.'),
      [pt(S('Must link with above answer (e.g. phototropism-stem', 'growing upwards/ root growing downwards)'), 5,
          kind='criterion')], 'bio-2-4', 'tropisms-in-germination', at(8, 9, '(a)', '(ii)'), 5,
      stem=[M('(i)', 9), _A(9, 'Name a growth response of a plant to a stimulus.')]),
] + [
    T(f'9b{r}', f'Q9(b)({r})', 'B', _A(9, ask), [pt(S(*ans), 9)], 'bio-2-4', concept, at(8, 9, '(b)', f'({r})'), 9,
      stem=[Q9B], fig='q9-table')
    for r, ask, ans, concept in [
        ('i', 'Identify which dish was the control.', ('Dish B',), 'iaa-control'),
        ('ii', 'Suggest a type of seed suitable for this investigation.', ('Radish/ or other named valid seed type',),
         'seed-for-iaa'),
        ('iii', 'Describe how the IAA solution was applied to the plant tissue.', ('Dropper/ to pour on/ bathe in',),
         'applying-iaa'),
        ('iv', 'Describe how the growth of the plant tissue was measured.', ('Ruler/ measuring tape',),
         'measuring-growth'),
        ('v', 'Why was the same number of seeds used in each dish?',
         ('Allow for failure or average/ to allow fair experiment',), 'same-number-of-seeds'),
        ('vi', 'Which part of the plant was stimulated by IAA?', ('Stem was stimulated',), 'iaa-stimulates'),
        ('vii', 'Which part of the plant was inhibited by IAA?', ('Root was inhibited',), 'iaa-inhibits'),
        ('viii', 'Name another plant growth regulator.', ('Abscisic acid/ or other valid growth regulator',),
         'other-growth-regulators')]
] + [
    # ------------------------------------------------------------ Section C --
    T(f'10a{r}', f'Q10(a)({r})', 'C', [Q10A, _C(2, term, br=True)], [pt(S(*ans), 3)], 'bio-3-1', concept,
      at(9, 10, '(a)', f'({r})'), 3)
    for r, term, ans, concept in [
        ('i', 'Competition', ('Struggle for (limited) resources (food)/ organism', 'struggling for resources'),
         'competition'),
        ('ii', 'Producer', ('Makes own food',), 'producer'),
        ('iii', 'Niche.', ('Role of organism',), 'niche')]
] + [
    T(f'10b{r}', f'Q10(b)({r})', 'C', _C(2, ask), rows, 'bio-3-1', concept, at(9, 10, '(b)', f'({r})'), total,
      stem=Q10B)
    for r, ask, rows, concept, total in [
        ('i', 'Why are foxes often found in towns and cities?', [pt(S('Easy availability of food'), 3)],
         'foxes-in-towns', 3),
        ('ii', 'Why are most foxes younger than 10 years old?', [pt(S('Killed on road'), 3)], 'fox-mortality', 3),
        ('iii', 'Name a producer from the article above.', [pt(S('Grass/ hedge or named hedgerow plant'), 3)],
         'a-producer-in-the-article', 3),
        ('iv', 'Name a primary consumer from the article above.', [pt(S('Rabbit'), 3)], 'a-primary-consumer', 3),
        ('v', 'Draw a food chain that includes four organisms from the article above.',
         [pt(S('Grass>Rabbit>Fox>Eagle (-3 for one organism missing)'), 6, units=[3, 3])], 'fox-food-chain', 6),
        ('vi', 'State an adaptation a fox has that increases its chance of survival.',
         [pt(S('Sharp teeth/ colour/ low centre of gravity for speed/ or', 'other valid adaptation'), 3)],
         'fox-adaptations', 3),
        ('vii', 'Mention two ways households could minimise the amount of waste produced.',
         [anyn(S('Reduce/ Reuse/ Recycle/ Repair'), 2, 3, note_sel=S('(any two)'))], 'minimising-waste', 6)]
] + [
    T(f'10ci-{slug}', 'Q10(c)(i)', 'C', _C(2, 'Draw a diagram of each piece of equipment and describe how each was used to',
                                           'Collect organisms for examination.'),
      [pt(S(row), 6, units=[3, 3])], 'bio-3-1', f'using-a-{slug}', at(9, 10, '(c)', '(i)'), 6,
      stem=[Q10C], item=(slug, name), decision=EACH_ITEM)
    for slug, name, row in [
        ('pooter', 'Pooter', 'Pooter diagram jar+two tubes/ Use by sucking up insects'),
        ('pitfall-trap', 'Pitfall Trap', 'Pitfall Trap diagram + (cover)/ Use-dig hole/ leave'),
        ('sweep-net', 'Sweep Net', 'Sweep net diagram net + handle/ Use drag over grass')]
] + [
    T('10cii', 'Q10(c)(ii)', 'C', _C(2, 'What did the students use to identify the animals they found?'),
      [pt(S('(Biological) key/ book/ hand lens/ magnifying glass'), 3)], 'bio-3-1', 'identifying-animals',
      at(9, 10, '(c)', '(ii)'), 3, stem=[Q10C]),
    T('10ciii', 'Q10(c)(iii)', 'C', _C(2, 'State any one abiotic factor that could influence the number of animals in the',
                                       'ecosystem.'),
      [pt(S('Soil pH/ temperature/ or any other named abiotic factor'), 3)], 'bio-3-1', 'abiotic-factors',
      at(9, 10, '(c)', '(iii)'), 3, stem=[Q10C]),
] + [
    T(f'11ai-{slug}', 'Q11(a)(i)', 'C', _C(3, 'Explain the terms haploid and diploid.'), [pt(S(ans), 3)], 'bio-2-3',
      slug, at(10, 11, '(a)', '(i)'), 3, item=(slug, name), decision=EACH_ITEM)
    for slug, name, ans in [('haploid', 'Haploid', 'Haploid-Single set chromosomes'),
                            ('diploid', 'Diploid', 'Diploid-2 sets chromosomes')]
] + [
    T('11aii', 'Q11(a)(ii)', 'C', _C(3, 'Name the type of cell division that halves the chromosome number.'),
      [pt(S('Meiosis'), 3)], 'bio-2-3', 'meiosis', at(10, 11, '(a)', '(ii)'), 3),
] + [
    T(f'11b{r}', f'Q11(b)({r})', 'C', q, [pt(S(ans), 3, **kw)], topic, concept, at(10, 11, '(b)', f'({r})'), 3,
      stem=stem)
    for r, q, ans, kw, topic, concept, stem in [
        ('i', _C(3, 'Chromosomes contain DNA. Name another substance found in chromosomes.'), 'Protein', {},
         'bio-1-2', 'chromosome-protein', []),
        ('ii', _C(3, 'Sections of DNA are called genes. What is the function of a gene?'), 'Code for protein production',
         {}, 'bio-1-4', 'function-of-a-gene', []),
        ('iii', _C(3, 'Describe the shape of a DNA molecule.'), '2 strands or helical or double helix', {}, 'bio-1-2',
         'double-helix', []),
        ('iv', _C(3, 'Name the base that combines with adenine in DNA.'), 'Thymine/ Capital "T"', {}, 'bio-1-2',
         'adenine-pairs-thymine', []),
        ('v', _C(3, 'Name the base that combines with guanine in DNA.'), 'Cytosine/ Capital "C"', {}, 'bio-1-2',
         'guanine-pairs-cytosine', []),
        ('vi', [_C(3, 'The stages involved in preparing a DNA profile are numbered below.'),
                _C(3, 'In your answer book, rewrite these stages', 'order in which they occur;'),
                _C(3, '1. The pattern of fragment distribution is analysed.', br=True),
                _C(3, '2. Fragments are separated on the basis of size.', br=True),
                _C(3, '3. Cells are broken down to release DNA.', br=True),
                _C(3, '4. DNA strands are cut into fragments.', br=True)],
         '3 - 4 - 2 - 1 (all or nothing)', {}, 'bio-3-3', 'order-of-profiling', []),
        ('vii', _C(3, 'Where in cells is most DNA located?'), 'Nucleus', {}, 'bio-1-3', 'where-dna-is', []),
        ('viii', _C(3, 'What is used to cut the DNA strand into fragments?'), '(Restriction)Enzymes', {}, 'bio-3-3',
         'restriction-enzymes', []),
        ('ix', _C(3, 'Suggest a reason for creating a genetic profile.', 'a genetic profile.'),
         'Paternity testing or forensics', {},
         'bio-3-3', 'uses-of-profiling', [])]
] + [
    T(f'11c{r}', f'Q11(c)({r})', 'C', _C(3, *ask), [pt(S(a), 3) for a in ans], 'bio-1-4', concept,
      at(10, 11, '(c)', f'({r})'), 3 * len(ans), stem=[Q11C], fig='q11c-cross')
    for r, ask, ans, concept in [
        ('i', ('Name the dominant allele in this cross.',), ['Dominant allele - B'], 'dominant-allele'),
        ('ii', ('Name the recessive allele in this cross.',), ['Recessive Allele - b'], 'recessive-allele'),
        ('iii', ('How many alleles for coat colour may be found in a single gamete?',), ['1'], 'alleles-in-a-gamete'),
        ('iv', ('What word is used to describe identical alleles in a genotype?',), ['Homozygous'], 'homozygous'),
        ('v', ('In your answer book, state the genotype and phenotype for the offspring',
               'missing from the shaded box above.'), ['Bb', 'Black'], 'missing-offspring'),
        ('vi', ('If the black dog is male, using X and Y, give the sex chromosomes of the black dog',
                'and the sex chromosomes of the white dog.'), ['XY', 'XX'], 'sex-chromosomes')]
] + [
    T('12ai', 'Q12(a)(i)', 'C', _C(4, 'Oxygen enters the blood in the lungs by diffusion. What is diffusion?'),
      [pt(S('Movement of molecules from a high concentration to low', 'concentration'), 3)], 'bio-2-6', 'diffusion',
      at(11, 12, '(a)', '(i)'), 3),
    T('12aii', 'Q12(a)(ii)', 'C',
      _C(4, 'Name the blood vessel that transports oxygenated blood from the lungs to the heart.'),
      [pt(S('Pulmonary vein'), 3)], 'bio-2-6', 'pulmonary-vein', at(11, 12, '(a)', '(ii)'), 3),
    T('12aiii', 'Q12(a)(iii)', 'C', _C(4, 'Name the chamber of the heart that receives oxygenated blood from the lungs.'),
      [pt(S('Left atrium'), 3)], 'bio-2-6', 'left-atrium', at(11, 12, '(a)', '(iii)'), 3),
] + [
    T(f'12bi-{x.lower()}', 'Q12(b)(i)', 'C', _C(4, 'Identify the structures labelled A, B C, D in the diagram.'),
      [pt(S(LUNGS, piece=i), 3)], 'bio-2-6', f'breathing-structure-{x.lower()}', at(11, 12, '(b)', '(i)'), 3,
      stem=[Q12B], fig='q12-lungs', labels=asked(L_LUNGS, x), item=(x.lower(), x), decision=EACH_ITEM)
    for i, x in enumerate('ABCD', 1)
] + [
    T('12bii', 'Q12(b)(ii)', 'C', _C(4, 'What prevents structure B from collapsing?'), [pt(S('Cartilage'), 3)],
      'bio-2-6', 'cartilage-in-the-trachea', at(11, 12, '(b)', '(ii)'), 3, stem=[Q12B], fig='q12-lungs',
      labels=asked(L_LUNGS, 'B')),
    T('12biii', 'Q12(b)(iii)', 'C', _C(4, 'Name a muscle that contracts during inhalation.'),
      [pt(S('Diaphragm or intercostal'), 3)], 'bio-2-6', 'breathing-muscles', at(11, 12, '(b)', '(iii)'), 3,
      stem=[Q12B], fig='q12-lungs'),
    T('12biv', 'Q12(b)(iv)', 'C', _C(4, 'Describe the change in air pressure inside the chest during inhalation.'),
      [pt(S('Decreases'), 3)], 'bio-2-6', 'pressure-in-inhalation', at(11, 12, '(b)', '(iv)'), 3, stem=[Q12B],
      fig='q12-lungs'),
] + [
    T(f'12bv-{slug}', 'Q12(b)(v)', 'C', [_C(4, 'Inhalation is an active process and exhalation is a passive process.'),
                                        _C(4, 'Explain the terms active and passive.')],
      [pt(S('Active requires energy/ passive (doesn’t require energy)', piece=i), 3)], 'bio-2-6', f'{slug}-process',
      at(11, 12, '(b)', '(v)'), 3, stem=[Q12B], fig='q12-lungs', item=(slug, name), decision=EACH_ITEM)
    for i, (slug, name) in enumerate([('active', 'Active'), ('passive', 'Passive')], 1)
] + [
    T(f'12ci-{x.lower()}', 'Q12(c)(i)', 'C', _C(4, 'Name each structure A and B.'),
      [pt(S('A = Villus/ B = Alveolus', piece=i), 3)], 'bio-2-6', f'exchange-structure-{x.lower()}',
      at(11, 12, '(c)', '(i)'), 3, stem=[Q12C], fig='q12-exchange', labels=asked(L_STRUCTURES, x),
      item=(x.lower(), x), decision=EACH_ITEM)
    for i, x in enumerate('AB', 1)
] + [
    T(f'12cii-{x.lower()}', 'Q12(c)(ii)', 'C', _C(4, 'State the exact location where each structure is found in the body.'),
      [pt(S('A in small intestine/ B in lungs', piece=i), 3)], 'bio-2-6', f'location-of-structure-{x.lower()}',
      at(11, 12, '(c)', '(ii)'), 3, stem=[Q12C], fig='q12-exchange', labels=asked(L_STRUCTURES, x),
      item=(x.lower(), x), decision=EACH_ITEM)
    for i, x in enumerate('AB', 1)
] + [
    T('12ciii', 'Q12(c)(iii)', 'C', _C(4, 'State two features, common to both structures, which are an adaptation to',
                                       'efficient exchange of materials.'),
      [anyn(S('Thin walls/ large capillary network/ numerous/ moist', 'surface'), 2, 3)], 'bio-2-6',
      'exchange-surfaces', at(11, 12, '(c)', '(iii)'), 6, stem=[Q12C], fig='q12-exchange'),
    T('12civ', 'Q12(c)(iv)', 'C', _C(4, 'Name a disorder of the breathing system and describe a treatment for that',
                                     'disorder.'),
      [pt(S('Asthma inhaler/ avoid allergens'), 6, units=[3, 3])], 'bio-2-6', 'breathing-disorder',
      at(11, 12, '(c)', '(iv)'), 6,
      decision='The scheme prints one disorder with its treatments on one 3,3 line: one row for both marks.'),
    T('13ai', 'Q13(a)(i)', 'C', _C(5, 'What role does chlorophyll play in photosynthesis?'),
      [pt(S('Traps sunlight energy/energised electrons/ take in or', 'absorb light'), 3)], 'bio-2-2',
      'role-of-chlorophyll', at(12, 13, '(a)', '(i)'), 3),
    T('13aii', 'Q13(a)(ii)', 'C', _C(5, 'Where is chlorophyll located in a plant cell?'), [pt(S('Chloroplast'), 3)],
      'bio-2-2', 'chloroplast', at(12, 13, '(a)', '(ii)'), 3),
    T('13aiii', 'Q13(a)(iii)', 'C', _C(5, 'Name the carbohydrate produced during photosynthesis.'),
      [pt(S('Glucose'), 3)], 'bio-2-2', 'glucose', at(12, 13, '(a)', '(iii)'), 3),
    T('13bi', 'Q13(b)(i)', 'C', _C(5, 'Name the basic source of energy for all organisms on earth.'),
      [pt(S('Sunlight'), 3)], 'bio-2-2', 'source-of-energy', at(12, 13, '(b)', '(i)'), 3, fig='q13-plant'),
    T('13bii', 'Q13(b)(ii)', 'C', _C(5, 'Name gas Y released by leaves during photosynthesis.'),
      [pt(S('Oxygen'), 3)], 'bio-2-2', 'oxygen-released', at(12, 13, '(b)', '(ii)'), 3, fig='q13-plant'),
    T('13biii', 'Q13(b)(iii)', 'C', _C(5, 'Name the openings in leaves that allow gas exchange.'),
      [pt(S('Stomata'), 3)], 'bio-2-6', 'stomata', at(12, 13, '(b)', '(iii)'), 3, fig='q13-plant'),
    T('13biv', 'Q13(b)(iv)', 'C', _C(5, 'Describe how water travels from the soil to the leaf.'),
      [anyn(S('Xylem/ tension/ osmosis/ root pressure', 'root pressure'), 2, 3)], 'bio-2-6', 'water-transport',
      at(12, 13, '(b)', '(iv)'), 6, fig='q13-plant'),
    T('13bv', 'Q13(b)(v)', 'C', [_C(5, 'When water reaches the site of photosynthesis in the leaf', 'Name these three products.')],
      [anyn(S('Electrons/ protons/ oxygen'), 3, 3)], 'bio-2-2', 'splitting-water', at(12, 13, '(b)', '(v)'), 9,
      fig='q13-plant'),
    T('13bvi', 'Q13(b)(vi)', 'C', _C(5, 'Name one method used by gardeners to increase the', 'growth of crops in greenhouses.'),
      [pt(S('Increase carbon dioxide / fertilise plants/ or other valid', 'method'), 3)], 'bio-2-2',
      'greenhouse-growth', at(12, 13, '(b)', '(vi)'), 3, fig='q13-plant'),
    T('13ci', 'Q13(c)(i)', 'C', _C(5, 'Identify which plant is a monocotyledon, A or B.'), [pt(S('A is a monocot'), 3)],
      'bio-2-6', 'identifying-a-monocot', at(12, 13, '(c)', '(i)'), 3, stem=[Q13C], fig='q13-plants'),
    T('13cii', 'Q13(c)(ii)', 'C', _C(5, 'State one feature that identifies a plant as a monocotyledon.'),
      [pt(S('Parallel veins/ scattered bundles/ floral parts in 3\'s'), 3, note_sel=S('(any one)'))], 'bio-2-6',
      'monocot-features', at(12, 13, '(c)', '(ii)'), 3, stem=[Q13C], fig='q13-plants'),
    T('13ciii', 'Q13(c)(iii)', 'C', _C(5, 'Identify which plant is a dicotyledon, A or B.'), [pt(S('B is a dicot'), 3)],
      'bio-2-6', 'identifying-a-dicot', at(12, 13, '(c)', '(iii)'), 3, stem=[Q13C], fig='q13-plants'),
    T('13civ', 'Q13(c)(iv)', 'C', _C(5, 'State one feature that identifies a plant as a dicotyledon.'),
      [pt(S('Netted veins/ bundles in a ring/ floral parts in 5 (any one)'), 3)], 'bio-2-6', 'dicot-features',
      at(12, 13, '(c)', '(iv)'), 3, stem=[Q13C], fig='q13-plants'),
    T('13cv', 'Q13(c)(v)', 'C', _C(5, 'The roots of plants absorb water. State one other function of plant roots.'),
      [pt(S('Anchorage/ or other valid function'), 3)], 'bio-2-6', 'functions-of-roots', at(12, 13, '(c)', '(v)'), 3),
] + [
    T(f'13cvi{n}', f'Q13(c)(vi){n}', 'C', item(5, n, end, 'Match the correct plant tissue type'),
      [pt(S('A=2/ B=3/ C=1', piece=piece), 3)], 'bio-2-6', concept, at(12, 13, '(c)', '(vi)'), 3,
      stem=Q13CVI, decision=EACH_ITEM)
    for n, end, piece, concept in [(1, 'Transport', 3, 'vascular-tissue'), (2, 'Protection', 1, 'dermal-tissue'),
                                   (3, 'Food storage', 2, 'ground-tissue')]
] + [
    T(f'14a{r}', f'Q14(a)({r})', 'C', _C(6, *ask), [pt(S(ans), 3)], topic, concept, at(13, 14, '(a)', f'({r})'), 3,
      stem=stem, fig='q14-fermentation')
    for r, ask, ans, topic, concept, stem in [
        ('i', ('Name an organism, represented by X', 'fermentation process.'), 'Yeast', 'bio-2-2', 'yeast', [Q14A]),
        ('ii', ('Name the product that is collected in', 'test tube B.'), 'Carbon dioxide', 'bio-2-2',
         'carbon-dioxide-collected', [Q14A]),
        ('iii', ('What effect does this product have', 'on the limewater in test tube B?'), 'Turns it a milky colour',
         'bio-2-2', 'limewater-test', [Q14A, M('(ii)', 6), _C(6, 'Name the product that is collected in', 'test tube B.')]),
        ('iv', ('Name the other product which', 'remains in test tube A.'), 'Alcohol', 'bio-2-2', 'alcohol-produced',
         [Q14A]),
        ('v', ('How do you know when fermentation has finished?',), 'No more bubbles', 'bio-2-2',
         'end-of-fermentation', [Q14A]),
        ('vi', ('What test can be used to show that the product, named in (iv), is present in test', 'tube A at the end.'),
         'Iodoform test', 'bio-2-2', 'testing-for-alcohol',
         [Q14A, M('(iv)', 6), _C(6, 'Name the other product which', 'remains in test tube A.')]),
        ('vii', ('What colour indicates a positive test for the product?',), 'Yellow', 'bio-2-2', 'positive-iodoform-test',
         [Q14A, M('(vi)', 6), _C(6, 'What test can be used to show that the product, named in (iv), is present in test',
                                 'tube A at the end.')]),
        ('viii', ('What substance is produced as a result of anaerobic respiration in human muscle?',), 'Lactic acid',
         'bio-2-2', 'lactic-acid', [Q14A]),
        ('ix', ('What effect does this substance have on human muscle?',), 'Cramps', 'bio-2-2', 'effect-of-lactic-acid',
         [Q14A, M('(viii)', 6), _C(6, 'What substance is produced as a result of anaerobic respiration in human muscle?')]),
        ('x', ('Give one other example of modern‐day bioprocessing.',),
         'Yoghurt/ or other valid example of bioprocessing', 'bio-3-2', 'bioprocessing', [Q14A])]
] + [
    T('14bi', 'Q14(b)(i)', 'C', _C(6, 'What is added to a cell sample to make structures more',
                                   'visible when viewed with a microscope?'),
      [pt(S('Stain/ (or a named stain)'), 3)], 'bio-1-3', 'staining', at(13, 14, '(b)', '(i)'), 3),
] + [
    T(f'14bii-{x.lower()}', 'Q14(b)(ii)', 'C', _C(6, 'Identify the parts A, B, C, D in the diagram of a plant cell.'),
      [pt(S(*CELL, piece=i), 3)], 'bio-1-3', f'plant-cell-part-{x.lower()}', at(13, 14, '(b)', '(ii)'), 3,
      fig='q14-cell', labels=asked(L_CELL, x), item=(x.lower(), x), decision=EACH_ITEM)
    for i, x in enumerate('ABCD', 1)
] + [
    T('14biii', 'Q14(b)(iii)', 'C', _C(6, 'What is the function of the part labelled B?'),
      [pt(S('Strength or rigidity/ shape/ protection/ structure'), 3)], 'bio-1-3', 'function-of-the-cell-wall',
      at(13, 14, '(b)', '(iii)'), 3, fig='q14-cell', labels=asked(L_CELL, 'B')),
    T('14biv', 'Q14(b)(iv)', 'C', _C(6, 'What is the function of the part labelled D?'),
      [pt(S('Respiration/ release energy'), 3)], 'bio-1-3', 'function-of-mitochondria', at(13, 14, '(b)', '(iv)'), 3,
      fig='q14-cell', labels=asked(L_CELL, 'D')),
    T('14bv', 'Q14(b)(v)', 'C', _C(6, 'What is a tissue?'),
      [pt(S('Similar cells working together /group of cells working', 'together'), 3)], 'bio-1-3', 'tissue',
      at(13, 14, '(b)', '(v)'), 3),
    T('14bvi', 'Q14(b)(vi)', 'C', _C(6, 'What is tissue culture?'),
      [pt(S('Growing cells outside body or in laboratory'), 3)], 'bio-1-3', 'tissue-culture', at(13, 14, '(b)', '(vi)'),
      3),
    T('14bvii', 'Q14(b)(vii)', 'C', _C(6, 'Describe one example of an application of tissue culture.'),
      [pt(S('Micro-propagation or skin tissue for grafts/ or other valid', 'application of tissue culture'), 3)],
      'bio-1-3', 'uses-of-tissue-culture', at(13, 14, '(b)', '(vii)'), 3),
    T('14ci', 'Q14(c)(i)', 'C', _C(6, 'Where would you find Rhizopus?'), [pt(S('Bread/ or other valid answer'), 3)],
      'bio-3-2', 'where-rhizopus-grows', at(13, 14, '(c)', '(i)'), 3, stem=[Q14C]),
    T('14cii', 'Q14(c)(ii)', 'C', _C(6, 'What is meant by the term heterotrophic?'),
      [pt(S('Not making its own food'), 3)], 'bio-3-2', 'heterotrophic', at(13, 14, '(c)', '(ii)'), 3, stem=[Q14C],
      decision='The paper prints this part as "(iii)" and the next as "(iii)" again; the scheme numbers it (ii).'),
    T('14ciii', 'Q14(c)(iii)', 'C', _C(6, 'Draw a diagram to show the structure of Rhizopus.',
                                       'rhizoids, sporangiophores and sporangium.'),
      [pt(S('Diagram'), 3, kind='criterion'), pt(S('Labels'), 3, kind='criterion', units=[1, 1, 1])], 'bio-3-2',
      'drawing-rhizopus', at(13, 14, '(c)', '(iii)'), 6, stem=[Q14C],
      decision='The scheme prices the drawing at 3 and its three named labels at 1 each.'),
    T('14civ', 'Q14(c)(iv)', 'C', _C(6, 'Label M on your diagram where mitosis occurs.'),
      [pt(S('Label M - Sporangium on the diagram'), 3, kind='criterion')], 'bio-3-2', 'mitosis-in-rhizopus',
      at(13, 14, '(c)', '(iv)'), 3, stem=[Q14C]),
    T('14cv', 'Q14(c)(v)', 'C', _C(6, 'Which form of reproduction results in the formation of a zygospore?'),
      [pt(S('Sexual'), 3)], 'bio-3-2', 'zygospores', at(13, 14, '(c)', '(v)'), 3, stem=[Q14C]),
    T('14cvi', 'Q14(c)(vi)', 'C', _C(6, 'Name another harmful fungus.'),
      [pt(S('Athletes foot/ or other valid example of a harmful fungus'), 3)], 'bio-3-2', 'harmful-fungi',
      at(13, 14, '(c)', '(vi)'), 3, stem=[Q14C]),
    T('14cvii', 'Q14(c)(vii)', 'C', _C(6, 'Name a beneficial fungus and give an example of its economic importance.'),
      [pt(S('Mushroom - food/ yeast – alcohol/ or other valid', 'matching name and matching example'), 6, units=[3, 3])],
      'bio-3-2', 'beneficial-fungi', at(13, 14, '(c)', '(vii)'), 6, stem=[Q14C]),
    T('14cviii', 'Q14(c)(viii)', 'C', _C(6, 'What can be used to treat fungal infections but is of no use against viral infections?'),
      [pt(S('Antibiotics'), 3)], 'bio-3-2', 'antibiotics', at(13, 14, '(c)', '(viii)'), 3, stem=[Q14C]),
] + [
    T(f'15ai{n}', f'Q15(a)(i){n}', 'C', [Q15AI, item(7, n, end, 'state which letter represents each of the following parts')],
      [pt(S('1=B/ 2=A/ 3=C/ 4=D', piece=n), 3)], 'bio-2-4', concept, at(14, 15, '(a)', '(i)'), 3,
      stem=[Q15], fig='q15-eye', decision=EACH_ITEM)
    for n, end, concept in [(1, 'Sclera', 'sclera'), (2, 'Lens', 'lens'), (3, 'Optic Nerve', 'optic-nerve'),
                            (4, 'Retina.', 'retina')]
] + [
    T('15aii', 'Q15(a)(ii)', 'C', _C(7, 'Explain the role of the pupil in the eye.'),
      [pt(S('Allows light into eye'), 3)], 'bio-2-4', 'pupil', at(14, 15, '(a)', '(ii)'), 3, stem=[Q15],
      fig='q15-eye'),
    T('15aiii', 'Q15(a)(iii)', 'C', _C(7, 'Name the two types of receptor cells', 'located in the retina that respond to light.'),
      [anyn(S('Rods/ cones'), 2, 3)], 'bio-2-4', 'rods-and-cones', at(14, 15, '(a)', '(iii)'), 6, stem=[Q15],
      fig='q15-eye'),
    T('15aiv', 'Q15(a)(iv)', 'C', _C(7, 'Name a disorder of either the eye or the', 'stated disorder.'),
      [pt(S('Disorder - short/ long sightedness or glue ear/ or other', 'valid disorder'), 3),
       pt(S('Treatment - correct corrective lens or grommets/ or other', 'valid treatment to named disorder'), 3)],
      'bio-2-4', 'eye-and-ear-disorders', at(14, 15, '(a)', '(iv)'), 6, stem=[Q15], fig='q15-eye',
      decision='Eye or ear: one disorder row and one treatment row for either, so one card.'),
    T('15av', 'Q15(a)(v)', 'C', _C(7, 'To which organ is the structure labelled C', 'connected?'),
      [pt(S('Brain/ CNS/ Cerebrum'), 3)], 'bio-2-4', 'optic-nerve-to-brain', at(14, 15, '(a)', '(v)'), 3,
      stem=[Q15], fig='q15-eye', labels=L_EYE),
] + [
    T(f'15bi{n}', f'Q15(b)(i){n}', 'C', [Q15BI, item(7, n, end, 'carry out the following functions:')],
      [pt(S('1=D/ 2=B/ 3=A/ 4=C', piece=n), 3)], 'bio-2-5', concept, at(14, 15, '(b)', '(i)'), 3,
      fig='q15-flower', decision=EACH_ITEM)
    for n, end, concept in [(1, 'Produces pollen', 'produces-pollen'),
                            (2, 'Attracts insects for pollination', 'attracts-insects'),
                            (3, 'Protects the flower as a bud', 'protects-the-bud'), (4, 'Produces eggs.', 'produces-eggs')]
] + [
    T('15bii', 'Q15(b)(ii)', 'C', _C(7, 'What is meant by pollination?'),
      [anyn(S('Transfer of pollen/ from anther to stigma'), 2, 3)], 'bio-2-5', 'pollination',
      at(14, 15, '(b)', '(ii)'), 6),
    T('15biii', 'Q15(b)(iii)', 'C', _C(7, 'Name the method of pollination that occurs in the', 'your answer.'),
      [anyn(S('Insect (animal)/ large petals / coloured petals/ or other', 'valid answer'), 2, 3)], 'bio-2-5',
      'insect-pollination', at(14, 15, '(b)', '(iii)'), 6, fig='q15-flower'),
    T('15biv', 'Q15(b)(iv)', 'C', _C(7, 'What is meant by dormancy and how does it', 'give an advantage to the seed?'),
      [anyn(None, 2, 3, options=[S('Period of no growth/ allows winter to pass', piece=1),
                                 S('Period of no growth/ allows winter to pass', piece=2),
                                 S('Low seed activity/ seed is inactive/ will grow when', 'conditions are better', piece=1),
                                 S('Low seed activity/ seed is inactive/ will grow when', 'conditions are better', piece=2),
                                 S('Low seed activity/ seed is inactive/ will grow when', 'conditions are better', piece=3)])],
      'bio-2-5', 'dormancy', at(14, 15, '(b)', '(iv)'), 6,
      decision='The scheme prints both lines of answers under one "2(3)": one menu of two responses.'),
] + [
    T(f'15ci-{x.lower()}', 'Q15(c)(i)', 'C', _C(7, 'Name the parts labelled A, B, C, D.'),
      [pt(S(MALE, piece=i), 3)], 'bio-2-5', f'male-part-{x.lower()}', at(14, 15, '(c)', '(i)'), 3, stem=[Q15C],
      fig='q15-male', labels=asked(L_MALE, x), item=(x.lower(), x), decision=EACH_ITEM)
    for i, x in enumerate('ABCD', 1)
] + [
    T('15cii', 'Q15(c)(ii)', 'C', _C(7, 'In which labelled structure are sperm cells', 'produced?'),
      [pt(S('D/ or testes'), 3)], 'bio-2-5', 'where-sperm-are-made', at(14, 15, '(c)', '(ii)'), 3, stem=[Q15C],
      fig='q15-male'),
    T('15ciii', 'Q15(c)(iii)', 'C', _C(7, 'What is the function of part labelled C?'),
      [pt(S('Carry sperm (to the penis)'), 3)], 'bio-2-5', 'sperm-duct', at(14, 15, '(c)', '(iii)'), 3, stem=[Q15C],
      fig='q15-male', labels=asked(L_MALE, 'C')),
    T('15civ', 'Q15(c)(iv)', 'C', _C(7, 'Give one function for the fluid produced by the', 'seminal vesicle.'),
      [pt(S('Help sperm swim or nourish sperm'), 3)], 'bio-2-5', 'seminal-fluid', at(14, 15, '(c)', '(iv)'), 3,
      stem=[Q15C], fig='q15-male'),
    T('15cv', 'Q15(c)(v)', 'C', _C(7, 'Name the sex hormone produced by the', 'structure labelled D.'),
      [pt(S('Testosterone'), 3)], 'bio-2-5', 'testosterone', at(14, 15, '(c)', '(v)'), 3, stem=[Q15C],
      fig='q15-male', labels=asked(L_MALE, 'D')),
    T('15cvi', 'Q15(c)(vi)', 'C', _C(7, 'Name one male secondary sexual characteristic.'),
      [pt(S('Broad shoulders/ or other valid characteristic'), 3)], 'bio-2-5', 'secondary-sexual-characteristics',
      at(14, 15, '(c)', '(vi)'), 3),
    T('15cvii', 'Q15(c)(vii)', 'C', _C(7, 'Give one disorder which results in male infertility.'),
      [pt(S('Low sperm count/ example needs to be qualified e.g. as a', 'result of cancer treatment'), 3)], 'bio-2-5',
      'male-infertility', at(14, 15, '(c)', '(vii)'), 3),
]

FIGURES = {
    # key suffix: (doc, page, rect in PDF points, credit, letters, alt, solution[, masks])
    'q3-carbon': ('038', 4, (55, 54, 545, 627), SEC, ['A'],
                  'Question 3 as printed: part of the carbon cycle with boxes for Carbon dioxide in atmosphere, Fossil '
                  'Fuels, Carbon compounds in plants, Carbon compounds in animals and Carbon compounds in Humus; one '
                  'arrow, labelled Feeding, runs from plants to animals, and an arrow marked A runs from animals to '
                  'humus. Below the diagram, parts (a) to (g) with their answer boxes.', False),
    'q4-table': ('038', 5, (55, 54, 541, 336), SEC, [],
                 'Question 4 as printed: the instruction, then the terms Substrate, Waterbath, Protein (struck '
                 'through), Reusable, Amylase and Product above a '
                 'two-column table: Column A lists "Enzymes are made of this" (answered Protein) and parts (a) to (e); '
                 'Column B is blank.', False),
    'q5-cells': ('038', 5, (55, 357, 556, 730), SEC, [],
                 'Question 5 as printed: the instruction, then the cell names Bacteria cell (struck through), Root hair, Amoeba, Cheek cell, Xylem vessel, Sperm '
                 'cell, Red blood cell and Neuron above eight drawings in boxes: a bacterium labelled Bacteria cell, '
                 'then (a) a round cell with a dark nucleus, (b) an irregular cell with extensions, (c) a cell with '
                 'a long outgrowth, (d) a disc-shaped cell with no nucleus, (e) a long tube with spiral thickening, '
                 '(f) a cell with a head and long tail, (g) a cell with many branches and a long fibre.', False),
    'q6-label': ('038', 6, (368, 76, 540, 248), SEC, [],
                 'A blood bag label with a barcode above large letters AB and the words Rh POSITIVE.', False),
    'q8-grid': ('038', 8, (378, 484, 545, 660), SEC, [],
                'A grid of squares over a round leafy plant, with an arrow marking "A point of intersection" where '
                'two grid lines cross.', False),
    'q9-table': ('038', 9, (128, 218, 465, 345), SEC, [],
                 'Table: Petri dish A, 5 seeds + IAA solution: average stem length after 1 week 15 mm, average root '
                 'length 2 mm. Petri dish B, 5 seeds + water: stem 10 mm, root 8 mm.', False),
    'q11c-cross': ('040', 3, (115, 428, 565, 597), SEC, [],
                   'The cross printed as: Parents Black Dog X White Dog; Genotypes Bb X bb; Gametes (B), (b) X (b). '
                   'Below, a grid with gamete b across the top and B and b down the side: the box for B is shaded '
                   'and the box for b reads bb (white), labelled Offspring. Beside it, a photograph of a black dog '
                   'and a white dog.', False),
    'q12-lungs': ('040', 4, (209, 143, 404, 309), SEC, ['A', 'B', 'C', 'D'],
                  'Diagram of the human breathing system. Lines point to A, a structure at the top of the central '
                  'tube; B, the central tube itself; C, a small branch inside the right lung; and D, the place where '
                  'the central tube divides.', False),
    'q12-exchange': ('040', 4, (165, 474, 515, 625), SEC, ['A', 'B'],
                     'Two drawings: A, a finger-like projection with blood vessels inside it, rising from a folded '
                     'lining; B, a rounded sac lined with cells and surrounded by small blood vessels.', False),
    'q13-plant': ('040', 5, (440, 124, 565, 295), SEC, [],
                  'Drawing of a flowering plant with an arrow labelled Gas Y leaving a leaf, and an arrow labelled '
                  'Water in soil at the roots.', False),
    'q13-plants': ('040', 5, (80, 392, 510, 560), SEC, ['A', 'B'],
                   'Two flowering plants, A and B, each drawn with a transverse section of its stem: the dots in '
                   'stem A\'s section are scattered throughout, those in stem B\'s section form a ring.', False),
    'q14-fermentation': ('040', 6, (328, 126, 572, 282), SEC, [],
                         'Two test tubes joined by a delivery tube: test tube A holds glucose and X under a layer of '
                         'oil; test tube B holds limewater.', False),
    'q14-cell': ('040', 6, (418, 420, 574, 568), SEC, ['A', 'B', 'C', 'D'],
                 'Diagram of a plant cell. A points to a large clear space in the middle, B to the outermost '
                 'boundary, C to the line just inside it and D to a small oval body with folded inner membranes; '
                 'the nucleus and cytoplasm are labelled.', False),
    'q15-eye': ('040', 7, (355, 124, 576, 298), SEC, ['A', 'B', 'C', 'D'],
                'Section through the human eye. A points at the oval structure behind the pupil, B at the outer coat '
                'at the bottom, C at the cord leaving the back of the eye and D at the inner layer lining the back.',
                False),
    'q15-flower': ('040', 7, (395, 372, 568, 508), SEC, ['A', 'B', 'C', 'D'],
                   'Section through a flower. A points at a small leaf-like part below the petals, B at a large '
                   'outer petal on the left, C at the swollen base of the central structure and D at the head of a '
                   'stalk on the right.', False),
    'q15-male': ('040', 7, (352, 566, 552, 760), SEC, ['A', 'B', 'C', 'D'],
                 'Diagram of the human male reproductive system with the seminal vesicle labelled. A points at the '
                 'outer organ, B at the tube running inside it, C at the tube looping up from the gland below and D '
                 'at the oval gland at the bottom.', False,
                 [(352, 566, 372, 577), (352, 714, 361, 746)]),   # ends of question lines printed beside it
}
