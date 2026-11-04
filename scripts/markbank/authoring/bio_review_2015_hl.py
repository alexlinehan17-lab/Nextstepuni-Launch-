"""Biology 2015 Higher Level — reviewed task ledger, carded from the paper for the first time.

Independent visual sweep (2026-10-25), every page rendered and read:
  * The 2015 paper is one booklet (M44), 16 pages: p1 cover and instructions,
    p2-p5 Section A Questions 1-6, p6-p8 Section B Questions 7-9, p9-p15
    Section C Questions 10-15, p16 "Blank Page". Sections A and B are
    answered on the paper; Section C in an answer book. No acknowledgements
    page: the Q11(c) photograph and every drawing carry no credit.
  * The marking scheme, 24 pages: p1 cover, p2 note, p3 introduction,
    cancelled answers and surplus answers, p4 surplus answers (continued) and
    conventions, p5-p19 Questions 1-15, p20-p23 "Blank Page", p24 back cover.

The paper's shape is the long-standing one: any five of Section A's six
questions, any two of Section B's three, any four of Section C's six, and
Q14 and Q15 are each any two of (a), (b), (c).

This scheme prints no reprint of any question: each answer stands under its
own question number, letter and roman, and a few rows carry a label word
("Heterotrophic:", "Piloerection:", "Ecosystem:"). A task is anchored on the
label where the scheme prints one that names the ask, and otherwise on its
own part marker, found by walking the scheme's numbering down to it (SQ
path). A numbered item ("1.", "2.") is anchored on the roman it is printed
under, as 2016 Higher anchors its items. Where the text layer sets a roman's
marker on its answer's own line ("(iii) mRNA is formed ..."), the roman is
anchored on the letter it is printed under.

Tariffs. Section A is ordered splits, carded at their first rate: Q1 "10 + 7
+ 3(1) i.e. best five answers from (a) - (f)" (six parts, the best five
priced), Q2, Q4 and Q6 "8 + 7 + 5(1)" (seven responses), Q3 "Best 6: 8 + 8 +
4(1)" (seven parts, the best six priced), Q5 "8 + 8 + 4(1)" (six responses).
Section B prints "5 + 1" over each (a)'s two parts, "8 + 8 + 8(1)" over Q7
(b) + (c), and "9 + 9 + 6(1)" over Q8 (b) + (c) and Q9 (b). Section C prints
a mark against every row, so every Section C task is priced row by row against
the paper's (9), (27), (24) and Q14/Q15's (30, 30); a descending split printed
over one row ("3 + 2" over Q14(c)(i)'s labels) is a menu with its steps.

One part prints answers with no per-response tariff they fit: Q12(b) prices
its (ii), four printed points, "3 + 6", which reads either as an ordered split
(first point 3, second 6) or as three points at 3; the whole of Q12(b) is
carded as one task at the paper's (27), every row unpriced (questionTotal).

The scheme prints Q4's key as the letters T and F beside each part's marker;
each is read from its own cell. Q11(c)(i)1's dental formula is printed as
fractions; it is read left to right from glyph positions and the scheme's own
print of it is the solution figure. Printed choices the scheme marks
differently per option are routes: Q7(c)(i)2 and 3, catalase or pepsin or
amylase (three boxed columns joined by "or").

The census reader finds all 125 printed asks (after the coordinator's
answer-line head fix); no paper.py entry was needed for this sitting.

Ten Section A parts print their answer on the same scheme line as the part's
own marker ("(a) Protein", "(b) Water or minerals or space"), with no reprint
of the ask: each is anchored on that marker with a welded bare anchor (the
runner reads the rows from the marker's own line).
"""
from bio_review_lib import Q, SQ, S, M, pt, anyn, allof, T, L, G

YEAR, LEVEL = 2015, 'hl'
REVIEWED_AT = '2026-10-25'

SOURCES = {
    'paper': {'path': 'examiner-reports/biology/papers/2015-hl-paper.pdf',
              'fileid': 'LC025ALP000EV.pdf',
              'sha256': '46dbe0b5bc176f4d29943597accb73676303c2bacb1617534887ee046639e887',
              'pages': 16},
    'scheme': {'path': 'examiner-reports/biology/schemes/2015-hl.pdf',
               'fileid': 'LC025ALP000EV.pdf',
               'sha256': 'e9129c41fe6c7fbea992d7d7c4e83c50d379f92e9f972e5452bf8f7daf4b7551',
               'pages': 24},
}

PAGE_ROLES = {
    'paper': {1: 'cover', **{p: 'questions' for p in range(2, 16)}, 16: 'blank'},
    'scheme': {1: 'cover', 2: 'note', 3: 'introduction', 4: 'conventions',
               **{p: 'marking' for p in range(5, 20)}, **{p: 'blank' for p in range(20, 24)},
               24: 'back-cover'},
}


def _ladder(notation, **extra):
    steps = []
    for term in notation.split('+'):
        n, _, m = term.strip().partition('(')
        steps += [int(m.rstrip(')'))] * int(n) if m else [int(n)]
    return {'steps': steps, 'notation': notation, **extra}


QUESTION_TOTALS = {
    **{n: 20 for n in range(1, 7)}, **{n: 30 for n in range(7, 10)},
    **{n: 60 for n in range(10, 14)}, 14: 90, 15: 90,   # Q14, Q15: any two of three 30s
}
# Only parts priced row by row (and Q12(b), carded whole): a ladder part's
# cards are carded at the ladder's first rate, so their sum is not its total.
PART_TOTALS = {
    **{(n, 'a'): 9 for n in (10, 11, 12, 13)},   # the paper's "(9)"
    **{(n, 'b'): 27 for n in (10, 11, 12, 13)},   # "(27)"; Q12(b) carded whole at it
    **{(n, 'c'): 24 for n in (10, 11, 12, 13)},   # "(24)"
    **{(n, x): 30 for n in (14, 15) for x in 'abc'},   # "(30, 30)"
}
LADDERS = {
    # Q1: six parts, the best five priced "10 + 7 + 3(1)".
    1: _ladder('10 + 7 + 3(1)', responses=6),
    2: _ladder('8 + 7 + 5(1)'),
    # Q3: seven parts, "Best 6: 8 + 8 + 4(1)".
    3: _ladder('8 + 8 + 4(1)', responses=7),
    4: _ladder('8 + 7 + 5(1)'), 5: _ladder('8 + 8 + 4(1)'), 6: _ladder('8 + 7 + 5(1)'),
    **{(n, 'a'): _ladder('5 + 1') for n in (7, 8, 9)},
    (7, 'bc'): _ladder('8 + 8 + 8(1)'), (8, 'bc'): _ladder('9 + 9 + 6(1)'), (9, 'b'): _ladder('9 + 9 + 6(1)'),
}

CHECKSUMS = {
    1: {10: 6}, 2: {8: 7}, 3: {8: 7}, 4: {8: 7}, 5: {8: 6}, 6: {8: 7},
    **{(n, 'a'): {5: 2} for n in (7, 8, 9)},
    (7, 'b'): {8: 4}, (7, 'c'): {8: 6}, (8, 'b'): {9: 4}, (8, 'c'): {9: 4}, (9, 'b'): {9: 8},
    (10, 'a'): {3: 3}, (10, 'b'): {3: 9}, (10, 'c'): {3: 8},
    (11, 'a'): {3: 3}, (11, 'b'): {6: 1, 2: 6, 3: 3}, (11, 'c'): {3: 8},
    (12, 'a'): {6: 1, 3: 1}, (12, 'c'): {3: 7, 1: 3},   # Q12(b) is carded whole: no units to count
    (13, 'a'): {3: 3}, (13, 'b'): {3: 9}, (13, 'c'): {6: 4},
    (14, 'a'): {3: 6, 6: 2}, (14, 'b'): {1: 3, 3: 5, 6: 2}, (14, 'c'): {6: 1, 3: 7, 2: 1, 1: 1},
    (15, 'a'): {3: 10}, (15, 'b'): {3: 9, 1: 3}, (15, 'c'): {1: 6, 3: 8},
}

SCAN_PAGES = {'paper': range(1, 16)}
SELECTION_SCAN = [
    ('paper', 1, 'any five', 'Cover rubric, Section A: whole-question choice; every question is carded.'),
    ('paper', 1, 'any two', 'Cover rubric, Section B: whole-question choice; every question is carded.'),
    ('paper', 1, 'any four', 'Cover rubric, Section C: whole-question choice; every question is carded.'),
    ('paper', 2, 'any five', 'Section A rubric repeated.'),
    ('paper', 2, 'any five', 'Q1 "Answer any five of the following parts": best five of (a)-(f); each part is its own '
                             'card on the "10 + 7 + 3(1)" ladder.'),
    ('paper', 2, 'the following', 'Q1, same lead-in.'),
    ('paper', 2, 'the following', 'Q2(e) lead-in: every part asked.'),
    ('paper', 3, 'the following', 'Q4 lead-in: every statement asked, one card per letter.'),
    ('paper', 3, 'or', 'Q4 "true or false": the answer options of each statement.'),
    ('paper', 5, 'the following', 'Q6(c) "Define each of the following words": both words asked, one card each.'),
    ('paper', 6, 'any two', 'Section B rubric: whole-question choice; every question is carded.'),
    ('paper', 6, 'the following', 'Q7(b)(i) "each of the following": one card per numbered item.'),
    ('paper', 6, 'or', 'Q7(b)(i)1 "Washing-up or similar liquid": the item named.'),
    ('paper', 6, 'the following', 'Q7(c)(i) "answer the following": one card per numbered item.'),
    ('paper', 9, 'any four', 'Section C rubric: whole-question choice; every question is carded.'),
    ('paper', 9, 'the following', 'Q10(b) "each of the following topics": every topic asked, one card per roman.'),
    ('paper', 10, 'the following', 'Q11(b)(i) "label all of the following": every label pair asked, one row each.'),
    ('paper', 10, 'the following', 'Q11(b)(ii) lead-in: one card per numbered item.'),
    ('paper', 11, 'or', 'Q12(c)(ii) "a letter or name": either form of the one answer; one row per table row.'),
    ('paper', 12, 'the following', 'Q13(a) lead-in: every word asked, one card per roman.'),
    ('paper', 12, 'the following', 'Q13(b) lead-in: every part asked.'),
    ('paper', 12, 'the following', 'Q13(c) "each of the following practices": every practice asked, one card per roman.'),
    ('paper', 13, 'any two', 'Q14 "any two of (a), (b), (c)": whole-part choice; every part is carded.'),
    ('paper', 13, 'any one', 'Q14(a)(i) "any one named feature": one feature; the scheme prices its name and mechanism.'),
    ('paper', 13, 'both', 'Q14(a)(iv)1 "both killer T cells and helper T cells": one row each.'),
    ('paper', 14, 'any two', 'Q15 "any two of (a), (b), (c)": whole-part choice; every part is carded.'),
    ('paper', 14, 'either', 'Q15(a) lead-in "either endospermic or non-endospermic": description.'),
    ('paper', 14, 'or', 'Q15(a) lead-in, same description.'),
    ('paper', 14, 'or', 'Q15(a) lead-in "endosperm or cotyledon tissue": description.'),
    ('paper', 14, 'either', 'Q15(a) lead-in "either monocotyledonous or dicotyledonous": description.'),
    ('paper', 14, 'or', 'Q15(a) lead-in, same description.'),
    ('paper', 14, 'or', 'Q15(a)(iii) "endosperm or cotyledon tissue": either tissue; one menu.'),
    ('paper', 14, 'both', 'Q15(a)(v) "both endosperm and embryo tissue": description of the graph.'),
    ('paper', 15, 'the following', 'Q15(c)(v) "Answer the following questions": one card per numbered item.'),
]

ROUTES = {
    'Q7(c)(i)2': ['catalase', 'pepsin', 'amylase'],
    'Q7(c)(i)3': ['catalase', 'pepsin', 'amylase'],
}

SEC = 'State Examinations Commission'
NO_REPRINT = 'The scheme prints no reprint of any question: anchored on the part\'s own marker.'
ITEM_ROMAN = ('The scheme prints no reprint: a numbered item is anchored on the roman it is printed under, its own '
              'number opening its answer\'s line.')
PARENT_LETTER = ('The scheme prints no reprint and the text layer sets this roman\'s marker on its answer\'s own line: '
                 'anchored on the letter it is printed under.')
ANSWER_LINE = ('The scheme prints no reprint and sets this part\'s marker on its answer\'s own line: anchored on that '
               'line, which shares the ask\'s wording.')
WELDED = ('The scheme prints no reprint and sets this part\'s marker on its answer\'s own line: anchored on that '
          'marker.')
EACH_ITEM = 'A numbered list the scheme prices entry by entry: one card per entry.'
NO_ANSWER = 'The scheme prints no answer here, only what earns the marks.'
SECTION_B_A = 'Section B (a) is "5 + 1" over its two parts: an ordered split, each part carded at its first rate.'


def ask(page, sentence, **kw):
    """A one-line ask closed by its own punctuation, before its answer line."""
    return Q(page, sentence, sentence, **kw)


def item(page, n, end, anchor):
    """One entry of a printed numbered list."""
    return Q(page, f'{n}.', end, after=anchor, br=True)


def at(page, *path_and_marker, nth=1, why=NO_REPRINT):
    """The part's own marker, walked down to through the scheme's numbering."""
    *path, marker = path_and_marker
    return SQ(page, marker, path=path, paired=why, bare=True, nth=nth)


def on_line(page, *path_and_marker, nth=1):
    """The part's marker line, its answer on it: a reprint-less anchor whose
    answer shares the ask's wording (2017 Ordinary Q6(c) anchors the same way)."""
    *path, marker = path_and_marker
    return SQ(page, marker, path=path, paired=ANSWER_LINE, nth=nth)


def welded(page, *path_and_marker, nth=1):
    """The part's marker opening its own answer line ("(a) Protein"): a welded
    bare anchor."""
    *path, marker = path_and_marker
    return dict(SQ(page, marker, path=path, paired=WELDED, bare=True, nth=nth), welded=True)


def lab(page, label, **kw):
    """The scheme's label word naming the ask ("Piloerection:"): the pairing anchor."""
    return SQ(page, label, label, **kw)


def lead(spec, words):
    """A row whose lifted note is the scheme's own tariff notation, led by a direction."""
    return dict(spec, note_lead=words)


def ladder(q, notation):
    return f'The scheme prints Q{q} as "{notation}": an ordered split, each response carded at its first rate.'


# ------------------------------------------------------------ question text --
Q1 = Q(2, 'Answer any five of the following parts (a) to (f):')
Q1A = ask(2, 'What name is given to the simplest units of carbohydrates?')
Q1D = ask(2, 'Name a structural polysaccharide found in plants.')
Q2E = Q(2, 'Answer the following questions in relation to a quantitative survey of a species of small herbaceous',
        'plant.')
Q3 = Q(3, 'The diagram shows the structure of a type of virus.')
Q4 = Q(3, 'Indicate whether the following statements are true or false by placing a tick (✓) in the appropriate box in',
       'each case.')
Q5 = Q(4, 'In an experiment, a student cut some potatoes into small, evenly-shaped pieces.', 'The graph is shown below.')
Q5B = Q(4, 'Explain in detail why the pieces in solutions D to F lost mass.')
Q6 = Q(5, 'The diagram shows a vertical section through human skin.')
Q6C = Q(5, 'Define each of the following words and explain how each process keeps the human body warm.')
Q7BI = Q(6, 'In relation to the isolation of DNA from a plant tissue, explain why you used each of the', 'following:')
Q7CI = Q(6, 'In relation to an investigation you carried out into heat denaturation of an enzyme, answer',
         'the following:')
Q7CI1 = item(6, 1, 'Name the enzyme you used.', 'heat denaturation of an enzyme')
Q8B = Q(7, 'Answer the questions below in relation to the growth of leaf yeast in the laboratory.')
Q8CI = ask(7, 'Describe how you carried out the investigation into the effect of IAA on plant tissue.')
Q9B = Q(8, 'A scientist wished to investigate the effect of the concentration of iodine on the rate of growth of',
        'stock solution of iodine.')
Q9BII = Q(8, 'At the start of the investigation the scientist divided the tadpoles into four groups of 25, one of',
          'which was to be the control.')
Q10B = Q(9, 'Write notes on each of the following topics in relation to nucleic acids.',
         'Do not give diagrams in your answers.')
Q10C = [Q(9, 'Unlike the situation in humans, maleness in birds results from the presence of the XX chromosome',
          'The gene for plumage colour is linked to the gene for tail length.'),
        Q(9, 'Study the genotypes of the above bird species shown in the diagrams below and in your answer',
          'A diagram may match more than one of the descriptions.')]
Q11BII = Q(10, 'Answer the following questions in relation to lipase.')
Q11CI1 = Q(10, '1.', 'Write the dental formula for an adult human with a full set of teeth.',
           after='What is the approximate pH at the site of lipase action?')
Q12B = Q(11, 'Researchers have taken an important step towards enhancing photosynthesis by creating',
         'Rubisco can account for up to half of all the soluble protein found in a leaf.')
Q12C = Q(11, 'The diagram below represents stages in respiration in yeast cells.')
Q13A = Q(12, 'Explain the following words as used in ecology:')
Q13B = Q(12, 'Answer the following questions in relation to the ecosystem you have studied.')
Q13BIII = Q(12, 'In relation to this diagram of a pyramid of numbers,')
Q13BIV = Q(12, 'What is the significance of energy loss at each stage in a food chain in relation to:')
Q13C = Q(12, 'Using your knowledge of ecology, suggest why caution is advised regarding each of the',
         'following practices.')
Q14AIV = Q(13, 'T cells are a type of lymphocyte, with different sub-types having different roles in our immune',
           'system.')
Q14BIV = Q(13, 'Reflex actions are very important in animals.')
Q14CI = Q(13, 'Draw a labelled diagram of the human male reproductive system and its associated glands.')
Q14CIV = Q(13, 'The diagram shows the structure of a human sperm cell. Part B contains many mitochondria.')
Q15A = Q(14, 'Seeds may be classified as either endospermic or non-endospermic, based on whether food is stored',
         'Seeds may also be either monocotyledonous or dicotyledonous.')
Q15AV = Q(14, 'The graph below shows the changes in dry mass of both endosperm and embryo tissue of a',
          'of a tissue with its water content removed.)')
Q15CV = [Q(15, 'When growing bacteria in the laboratory, samples are taken regularly from the growth',
           'similar to the one shown below.'),
         Q(15, 'Answer the following questions in relation to this graph.')]

SKIN = [('A', 'A = erector muscle'), ('B', 'B = sweat gland')]
SPINAL = [('A', 'A = *grey matter'), ('B', 'B = *white matter'),
          ('C', 'C = *central canal or *cerebrospinal fluid (CSF)')]
STAGES = [('B', 'B = *log (phase)'), ('C', 'C = *stationary (phase)'), ('D', 'D = *decline (or *death) (phase)')]

# Q4's key: the letter the scheme prints beside each part's marker, read from
# its own cell (x 505-530 points, one printed row each, page 6).
TF = [('a', 'Meiosis is an important source of variation.', 2, (118, 138), 'T', 'meiosis-and-variation'),
      ('b', 'Mitosis occurs in mature red blood cells in humans.', 2, (147, 166), 'F', 'mature-red-cells-do-not-divide'),
      ('c', 'During mitosis the nuclear membrane temporarily disappears.', 1, (175, 195), 'T',
       'nuclear-membrane-in-mitosis'),
      ('d', 'Meiosis gives rise to the haploid condition.', 1, (203, 223), 'T', 'meiosis-gives-haploid-cells'),
      ('e', 'In multicellular organisms mitosis functions primarily in growth.', 1, (232, 252), 'T',
       'mitosis-for-growth'),
      ('f', 'In plants, a cell plate forms during telophase of mitosis.', 1, (260, 280), 'T', 'cell-plate'),
      ('g', 'The human zygote divides by meiosis.', 1, (288, 308), 'F', 'zygote-divides-by-mitosis')]

TASKS = [
    # ------------------------------------------------------------ Section A --
    T(f'1{x}', f'Q1({x})', 'A', q, [pt(S(ans), 10)], 'bio-1-2', concept, at(5, '1.', f'({x})'), 10, stem=stem,
      decision=ladder(1, '10 + 7 + 3(1) i.e. best five answers from (a) – (f)') + ' Six parts, the best five priced.'
      + (' The text layer flattens the formula\'s subscripts: "Cx(H2O)y" is C with a subscript x, H2O in brackets '
         'with a subscript y.' if x == 'c' else ''))
    for x, q, stem, ans, concept in [
        ('a', Q1A, [Q1], 'Monosaccharides', 'monosaccharides'),
        ('b', ask(2, 'Name a catabolic process that produces these simplest units.'), [Q1, M('(a)', 2), Q1A],
         'Digestion', 'catabolism-of-carbohydrates'),
        ('c', Q(2, 'The general formula of carbohydrates is Cx(H2O)y.', 'used for energy by human cells?'), [Q1], '6',
         'carbohydrate-formula'),
        ('d', Q1D, [Q1], 'Cellulose', 'cellulose'),
        ('e', ask(2, 'Name a polysaccharide, other than the one referred to in part (d), commonly found in plants.'),
         [Q1, M('(d)', 2), Q1D], 'Starch', 'starch'),
        ('f', ask(2, 'Which carbohydrate is always found in DNA?'), [Q1], 'Deoxyribose', 'deoxyribose')]
] + [
    T('2a', 'Q2(a)', 'A', ask(2, 'What do ecologists mean by the term scramble competition?'),
      [pt(S('All (individuals) get some of a (scarce) resource'), 8)], 'bio-3-1', 'scramble-competition',
      at(5, '2.', '(a)'), 8, decision=ladder(2, '8 + 7 + 5(1)') + ' Seven responses.'),
    T('2c', 'Q2(c)', 'A', Q(2, 'Give one example of a factor, other than food, which may be a source of competition among',
                            'animals.'),
      [pt(S('Water or mate(s) or shelter or territory (or space)'), 8)], 'bio-3-1', 'competition-among-animals',
      at(5, '2.', '(c)'), 8, decision=ladder(2, '8 + 7 + 5(1)') + ' Seven responses.'),
    T('2d', 'Q2(d)', 'A', Q(2, 'Caterpillars have mouth parts that are suitable for chewing on leaves',
                            'competition between the adults and the young of such species.'),
      [pt(S('Different food or feed on different parts of the plant', after='Water or mate(s)'), 8)], 'bio-3-1',
      'reducing-competition', on_line(5, '2.', '(d)'), 8, decision=ladder(2, '8 + 7 + 5(1)') + ' Seven responses.'),
] + [
    T(f'2e{r}', f'Q2(e)({r})', 'A', ask(2, q), [pt(S(*ans), 8)], 'bio-3-1', concept, at(5, '2.', '(e)', f'({r})'), 8,
      stem=[Q2E], decision=ladder(2, '8 + 7 + 5(1)') + ' Seven responses.')
    for r, q, ans, concept in [
        ('i', 'Name the method that you would employ.', ('Frequency or cover or transect or quadrat',),
         'quantitative-survey-method'),
        ('ii', 'How would you ensure that your sampling was random?',
         ('Throw (object) over shoulder (and place quadrat) or random numbers matched to a', 'Grid'), 'random-sampling'),
        ('iii', 'Name one edaphic factor that could affect the distribution of this plant in the ecosystem.',
         ('pH or temperature or air content or water content or mineral content', 'microorganisms'), 'edaphic-factors')]
] + [
    T('3d', 'Q3(d)', 'A', ask(3, 'Name one virus that causes disease in plants.'),
      [pt(S('mosaic (virus)', after='RNA or DNA'), 8)], 'bio-1-1', 'plant-virus', on_line(6, '3.', '(d)', nth=2), 8,
      decision=ladder(3, 'Best 6: 8 + 8 + 4(1)') + ' Seven parts, the best six priced.'),
] + [
    T(f'4{x}', f'Q4({x})', 'A', Q(3, statement), [G('tokens', page=6, clip=(505, y[0], 530, y[1]), expect=answer, marks=8)],
      'bio-2-3', concept, at(6, '4.', f'({x})', nth=nth), 8, stem=[Q4],
      decision=ladder(4, '8 + 7 + 5(1)') + ' The scheme prints the answer as the letter ' + answer
      + ' beside the part\'s marker, read from that cell.')
    for x, statement, nth, y, answer, concept in TF
] + [
    T('5a', 'Q5(a)', 'A', Q(4, 'From the graph, determine the concentration of the contents of the potato cells.'),
      [pt(S('(Equivalent to ) 0.3 – 0.35 (% sucrose solution)', after='Best 6:'), 8)], 'bio-2-6',
      'potato-cell-concentration', on_line(6, '5.', '(a)'), 8, stem=[Q5], fig='q5-graph',
      decision=ladder(5, '8 + 8 + 4(1)') + ' Six responses: (a), (b)\'s two, (c) and (d)\'s two.'),
    T('6a', 'Q6(a)', 'A', ask(5, 'Place an X on the adipose tissue.'),
      [pt(S('X correctly placed on adipose tissue'), 8, kind='criterion', note=NO_ANSWER)], 'bio-2-4', 'adipose-tissue',
      at(7, '6.', '(a)'), 8, stem=[Q6], fig='q6-skin', decision=ladder(6, '8 + 7 + 5(1)') + ' Seven responses.'),
] + [
    T(f'6b-{x.lower()}', 'Q6(b)', 'A', ask(5, 'Name A and B.'), [pt(S(line, piece=2, psep=' = '), 8)], 'bio-2-4',
      concept, at(7, '6.', '(b)'), 8, stem=[Q6], fig='q6-skin', item=(x.lower(), x),
      labels=[L(y, S(ln, page=7, piece=2, psep=' = '), y == x) for y, ln in SKIN],
      decision='A lettered figure the scheme prices letter by letter: one card per letter, each a response on the '
               '"8 + 7 + 5(1)" ladder.')
    for (x, line), concept in zip(SKIN, ['erector-muscle', 'sweat-gland'])
] + [
    T('6ci', 'Q6(c)(i)', 'A', ask(5, 'Piloerection.'),
      [pt(S('Hair stands up'), 8), pt(S('Air is trapped or (air) insulates or reduces (or prevents)', 'heat loss'), 8)],
      'bio-2-4', 'piloerection', lab(7, 'Piloerection:'), 16, stem=[Q6C],
      decision='The definition and how it keeps the body warm are two responses on the "8 + 7 + 5(1)" ladder.'),
    T('6cii', 'Q6(c)(ii)', 'A', ask(5, 'Vasoconstriction.'),
      [pt(S('Blood vessels (or arteries or arterioles) narrow'), 8),
       pt(S('Reducing (or preventing) heat loss or less blood to skin'), 8)],
      'bio-2-4', 'vasoconstriction', lab(7, 'Vasoconstriction:'), 16, stem=[Q6C],
      decision='The definition and how it keeps the body warm are two responses on the "8 + 7 + 5(1)" ladder.'),
    # ------------------------------------------------------------ Section B --
    T('7ai', 'Q7(a)(i)', 'B', ask(6, 'What is the chemical composition of a chromosome?'), [pt(S('DNA and protein'), 5)],
      'bio-1-2', 'chromosome-composition', at(8, '7.', '(a)', '(i)'), 5, decision=SECTION_B_A),
    T('7aii', 'Q7(a)(ii)', 'B', ask(6, 'What is meant by the term junk DNA?'), [pt(S('Non-coding (DNA)'), 5)],
      'bio-1-2', 'junk-dna', at(8, '7.', '(a)', '(ii)'), 5, decision=SECTION_B_A),
] + [
    T(f'7bi{n}', f'Q7(b)(i){n}', 'B', item(6, n, end, 'isolation of DNA from a plant tissue'), [pt(S(*ans), 8)],
      'bio-1-2', concept, at(8, '7.', '(b) + (c)', '(b)', '(i)', why=ITEM_ROMAN), 8, stem=[Q7BI],
      decision=EACH_ITEM + ' ' + ladder('7 (b) + (c)', '8 + 8 + 8(1)') + ' Ten responses over (b) and (c).')
    for n, end, ans, concept in [
        (1, 'Washing-up or similar liquid.', ('To breakdown the (cell) membrane(s)',), 'washing-up-liquid'),
        (2, 'Sodium chloride.', ('To cause the DNA to clump',), 'salt-in-dna-isolation'),
        (3, 'Protease.', ('To breakdown (or remove or digest) the protein in the chromosomes',), 'protease-in-dna-isolation'),
        (4, 'Freezer-cold ethanol.', ('To bring the DNA out of solution or to make the DNA visible',
                                      'or to separate the DNA'), 'ethanol-in-dna-isolation')]
] + [
    T('7ci1', 'Q7(c)(i)1', 'B', Q7CI1,
      [anyn(None, 1, 8, options=[S('Catalase'), S('Pepsin', '(or protease)'), S('Amylase', '(or diastase)')])],
      'bio-2-1', 'enzyme-for-heat-denaturation', at(8, '7.', '(b) + (c)', '(c)', '(i)', why=ITEM_ROMAN), 8,
      stem=[Q7CI], decision=EACH_ITEM + ' The scheme prints three enzymes in boxed columns joined by "or": one menu, '
                                        'claim one.'),
] + [
    T('7ci2', 'Q7(c)(i)2', 'B', item(6, 2, 'Name the enzyme’s substrate.', 'heat denaturation of an enzyme'),
      [pt(S(*sub), 8)], 'bio-2-1', f'substrate-of-{route}', at(8, '7.', '(b) + (c)', '(c)', '(i)', why=ITEM_ROMAN),
      8, route=route, stem=[Q7CI, Q7CI1],
      decision='Catalase, pepsin or amylase: the scheme prints each enzyme\'s substrate and products in its own boxed '
               'column, the columns joined by "or", so each is a route card. ' + EACH_ITEM)
    for route, sub in [('catalase', ('Hydrogen', 'peroxide')), ('pepsin', ('Protein',)), ('amylase', ('Starch',))]
] + [
    T('7ci3', 'Q7(c)(i)3', 'B', item(6, 3, 'Name the product(s) formed.', 'heat denaturation of an enzyme'),
      [pt(S(*prod), 8)], 'bio-2-1', f'products-of-{route}', at(8, '7.', '(b) + (c)', '(c)', '(i)', why=ITEM_ROMAN),
      8, route=route, stem=[Q7CI, Q7CI1],
      decision='Catalase, pepsin or amylase: the scheme prints each enzyme\'s substrate and products in its own boxed '
               'column, the columns joined by "or", so each is a route card. ' + EACH_ITEM)
    for route, prod in [('catalase', ('Oxygen (and', 'water)')), ('pepsin', ('Peptides', '(or amino acids)')),
                        ('amylase', ('Maltose',))]
] + [
    T('7cii', 'Q7(c)(ii)', 'B', ask(6, 'How did you denature the enzyme?'),
      [pt(S('Boil or heat to high temperature (≥ 60 °C)'), 8)], 'bio-2-1', 'denaturing-the-enzyme',
      at(8, '7.', '(b) + (c)', '(c)', '(ii)'), 8, stem=[Q7CI]),
    T('7ciii', 'Q7(c)(iii)', 'B', ask(6, 'How did you know that the enzyme had been denatured?'),
      [pt(S('negative result for named test for product', 'or positive result for named test for substrate'), 8,
          kind='criterion', note_sel=S('[must match enzyme or product in c (i) above]'), note=NO_ANSWER)],
      'bio-2-1', 'evidence-of-denaturation', at(8, '7.', '(b) + (c)', '(c)', why=PARENT_LETTER), 8, stem=[Q7CI]),
    T('7civ', 'Q7(c)(iv)', 'B', ask(6, 'Why are buffers needed when carrying out experiments with enzymes in school?'),
      [pt(S('To maintain (a constant) pH or to vary pH'), 8)], 'bio-2-1', 'buffers',
      at(8, '7.', '(b) + (c)', '(c)', why=PARENT_LETTER), 8),
    T('8ai', 'Q8(a)(i)', 'B', Q(7, 'Fungi may be classified into two groups on the basis of their nutrition.',
                                'What is the other group?'),
      [pt(S('Saprophytic'), 5, note_sel=S('[accept *saprobic]'))], 'bio-3-2', 'saprophytic-fungi',
      at(9, '8.', '(a)', '(i)'), 5, decision=SECTION_B_A),
    T('8aii', 'Q8(a)(ii)', 'B', ask(7, 'Draw a labelled diagram of a reproducing yeast cell.'),
      [pt(S('Diagram: cell + nucleus + attached bud with bud (or a nucleus) labelled'), 5, kind='criterion')],
      'bio-3-2', 'drawing-budding-yeast', at(9, '8.', '(a)', '(ii)'), 5,
      decision=SECTION_B_A + ' The drawing is one priced item: one criterion row naming what it must show.'),
    T('8bi', 'Q8(b)(i)', 'B', ask(7, 'What principal nutrient was added to the agar for the yeast?'),
      [pt(S('Malt (extract)'), 9)], 'bio-3-2', 'malt-agar', at(9, '8.', '(b) + (c)', '8.', '(b)', '(i)'), 9,
      stem=[Q8B], decision=ladder('8 (b) + (c)', '9 + 9 + 6(1)') + ' Eight responses over (b) and (c).'),
    T('8bii', 'Q8(b)(ii)', 'B', ask(7, 'How did you introduce the yeast into the Petri dishes?'),
      [pt(S('Attach leaves (or leaf pieces) to (inside of) lid'), 9),
       pt(S('Replace lid (on dish) or (dish) upright for 24 hours', 'or one aseptic technique described'), 9)],
      'bio-3-2', 'introducing-leaf-yeast', at(9, '8.', '(b) + (c)', '8.', '(b)', '(ii)'), 18, stem=[Q8B],
      decision='Two responses on the "9 + 9 + 6(1)" ladder.'),
    T('8biii', 'Q8(b)(iii)', 'B', ask(7, 'What did the yeast look like when it had grown on the agar?'),
      [pt(S('Pink colonies or pink with ‘colonies’ described'), 9)], 'bio-3-2', 'leaf-yeast-colonies',
      at(9, '8.', '(b) + (c)', '8.', '(b)', '(iii)'), 9, stem=[Q8B]),
    T('8ci', 'Q8(c)(i)', 'B', Q8CI,
      [pt(S('Some exposed to IAA and some not exposed to IAA', 'or tissue exposed to different concentrations of IAA'),
          9),
       pt(S('Leave for at least 2 days'), 9), pt(S('Measure (or record) growth or compare growth'), 9)],
      'bio-2-4', 'iaa-investigation', at(9, '8.', '(b) + (c)', '8.', '(c)', '(i)'), 27,
      decision='Three responses on the "9 + 9 + 6(1)" ladder.'),
    T('8cii', 'Q8(c)(ii)', 'B', ask(7, 'What were the results of your investigation?'),
      [pt(S('Description of how concentration (or IAA) changed growth (of tissue)'), 9, kind='criterion',
          note=NO_ANSWER)],
      'bio-2-4', 'iaa-results', at(9, '8.', '(b) + (c)', '8.', '(c)', why=PARENT_LETTER), 9,
      stem=[M('(i)', 7), Q8CI]),
    T('9ai', 'Q9(a)(i)', 'B', ask(8, 'What is the purpose of a hypothesis in the scientific method?'),
      [pt(S('To form the basis of a prediction or to give a starting point for an',
            'experiment or (to attempt) to explain an observation'), 5)], 'bio-u2', 'purpose-of-a-hypothesis',
      at(10, '9.', '(a)', '9.', '(a)', '(i)'), 5, decision=SECTION_B_A),
    T('9aii', 'Q9(a)(ii)', 'B', ask(8, 'Explain what is meant by double-blind testing in scientific experimentation.'),
      [pt(S('Neither the experimenter nor the test group knows who gets what', '(or described)'), 5)], 'bio-u2',
      'double-blind-testing', at(10, '9.', '(a)', '9.', '(a)', '(ii)'), 5, decision=SECTION_B_A),
    T('9bi', 'Q9(b)(i)', 'B', ask(8, 'Why do you think that it was important that all the tadpoles came from the same mother?'),
      [pt(S('So they are genetically similar or they are likely to respond in the', 'same way (to iodine)'), 9)],
      'bio-u2', 'same-mother', at(10, '9.', '(b)', '9.', '(b)', '(i)'), 9, stem=[Q9B],
      decision=ladder('9(b)', '9 + 9 + 6(1)') + ' Eight responses.'),
] + [
    T(f'9bii{n}', f'Q9(b)(ii){n}', 'B', item(8, n, end, 'which was to be the control.'), rows, 'bio-u2', concept,
      at(10, '9.', '(b)', '9.', '(b)', '(ii)', why=ITEM_ROMAN), total, stem=[Q9B, Q9BII], decision=EACH_ITEM)
    for n, end, rows, concept, total in [
        (1, 'Why is a control essential in scientific experiments?',
         [pt(S('To (provide a standard or baseline to) compare with the experiment'), 9)], 'why-a-control', 9),
        (2, 'Suggest why he used 25 tadpoles in each group.',
         [pt(S('A larger sample makes allowance for illness (or death)',
               'or to make the results more statistically significant'), 9)], 'sample-size', 9),
        (3, 'Suggest how this investigation would have been carried out.',
         [anyn(S('Different concentrations of iodine (solution) / made up using pond water /', '(control) no iodine'),
               3, 9, note_sel=S('Any Three'))], 'designing-the-investigation', 27)]
] + [
    T('9biii', 'Q9(b)(iii)', 'B', ask(8, 'Suggest two factors that the scientist would have kept constant during the investigation.'),
      [anyn(S('Temperature / amount of food / oxygen concentration / light (exposure) /',
              'volume of water / duration of exposure'), 2, 9, note_sel=S('Any Two'))], 'bio-u2',
      'controlled-variables', at(10, '9.', '(b)', '9.', '(b)', why=PARENT_LETTER), 18, stem=[Q9B]),
    # ------------------------------------------------------------ Section C --
] + [
    T(f'10a{r}', f'Q10(a)({r})', 'C', ask(9, q), [pt(S(*ans), 3)], 'bio-1-4', concept, at(11, '10.', '(a)', f'({r})'), 3)
    for r, q, ans, concept in [
        ('i', 'Which famous 19th century biologist is regarded as ‘the father of genetics’?', ('Mendel',), 'mendel'),
        ('ii', 'In genetics, what is meant by segregation?',
         ('Separation of homologous chromosomes', 'or separation of alleles'), 'segregation'),
        ('iii', 'Give an example of a sex-linked characteristic in humans.',
         ('Haemophilia or (red-green) colour-blindness',), 'sex-linked-characteristic')]
] + [
    # "Codons." alone is too short a question to stand (the build's floor is
    # eight characters): its card carries the printed lead-in in its question
    # text instead of its stem, as 2018 Higher Q2(e) does.
    T(f'10b{r}', f'Q10(b)({r})', 'C', [Q10B, ask(9, q, br=True)] if len(q) < 8 else ask(9, q),
      [anyn(S(*menu), 3, 3)], topic, concept, sq, 9, stem=[] if len(q) < 8 else [Q10B])
    for r, q, menu, topic, concept, sq in [
        ('i', 'Complementary base pairs.', ('(Two bases joined by) hydrogen bonds / purine with pyrimidine /',
                                            'Adenine with Uracil in RNA or Thymine replaced by Uracil in RNA'),
         'bio-1-2', 'complementary-base-pairs', at(11, '10.', '(b)', '(i)')),
        ('ii', 'Codons.', ('Sequence(s) of three bases / on DNA / on mRNA or on tRNA / (each',
                           'codon) codes for one amino acid / that codes for a start (or stop)'),
         'bio-2-3', 'codons', at(11, '10.', '(b)', '(ii)')),
        ('iii', 'Transcription.', ('mRNA is formed / using a (single) strand of DNA / (DNA acts) as a',
                                   'template (or described) / in nucleus / (catalysed by) RNA polymerase'),
         'bio-2-3', 'transcription', at(11, '10.', '(b)', why=PARENT_LETTER))]
] + [
    T(f'10c{r}', f'Q10(c)({r})', 'C', ask(9, q), [pt(S(ans), 3)], 'bio-1-4', concept, at(11, '10.', '(c)', f'({r})'), 3,
      stem=Q10C, fig='q10c-birds', decision='The scheme prints the answer as the letter of the matching diagram.')
    for r, q, ans, concept in [
        ('i', 'A female that is heterozygous in respect of plumage colour and tail length.', 'E',
         'heterozygous-female'),
        ('ii', 'A male that can produce only one type of gamete.', 'C', 'male-with-one-gamete-type'),
        ('iii', 'The individual that can produce the greatest number of different gametes.', 'E',
         'most-gamete-types'),
        ('iv', 'A male, all of whose offspring will have long tails.', 'C', 'male-all-long-tailed-offspring'),
        ('v', 'A female, all of whose offspring will have green plumage.', 'B', 'female-all-green-offspring'),
        ('vi', 'A male that is homozygous in respect of plumage colour and tail length.', 'C', 'homozygous-male')]
] + [
    T('10cvii', 'Q10(c)(vii)', 'C',
      ask(9, 'In your answer book, write out the genotypes of the gametes that bird D can produce.'),
      [pt(S('glX / glY', piece=1), 3), pt(S('glX / glY', piece=2), 3)], 'bio-1-4', 'gametes-of-bird-d',
      at(11, '10.', '(c)', why=PARENT_LETTER), 6, stem=Q10C, fig='q10c-birds',
      decision='"2(3)": the two gametes, each cut at the scheme\'s own solidus.'),
    T('11ai', 'Q11(a)(i)', 'C', ask(10, 'Humans are heterotrophic and omnivorous. Explain each of these terms.'),
      [pt(S('must consume food or eats other organisms', 'or cannot make their food', skip_marks=True), 3,
          label=S('Heterotrophic:', after='(i)')),
       pt(S('eats both animal and plant (material)'), 3, label=S('Omnivorous:'))], 'bio-2-6',
      'heterotrophic-and-omnivorous', lab(12, 'Heterotrophic:'), 6,
      decision='The scheme prints the first answer\'s mark between its two lines; the answer is read without it.'),
    T('11aii', 'Q11(a)(ii)', 'C', ask(10, 'What is meant by a balanced diet?'),
      [pt(S('Correct amounts of each food type (for health)'), 3)], 'bio-2-6', 'balanced-diet',
      at(12, '11.', '(a)', '(ii)'), 3),
    T('11bi', 'Q11(b)(i)', 'C',
      [Q(10, 'Draw a large diagram of the human alimentary canal and its associated glands.',
         'On your diagram label all of the following:'),
       Q(10, '1.', 'each name to indicate it is a gland.', after='On your diagram label', br=True),
       Q(10, '2.', 'it is part of the small intestine.', after='On your diagram label', br=True),
       Q(10, '3.', 'it is part of the large intestine.', after='On your diagram label', br=True)],
      [pt(S('continuous tube + stomach + intestines + a gland'), 6, kind='criterion', label=S('Diagram:'),
          note_sel=S('6, 3, 0'), note_lead='The scheme marks this diagram'),
       lead(anyn(S('Liver / salivary glands / pancreas'), 2, 2, note_sel=S('2(2, 1, 0)')),
            'The scheme marks these two labels'),
       lead(anyn(S('Duodenum / ileum'), 2, 2, note_sel=S('2(2, 1, 0)', after='Duodenum / ileum')),
            'The scheme marks these two labels'),
       lead(anyn(S('Colon / caecum (or appendix) / rectum'), 2, 2, note_sel=S('2(2, 1, 0)', after='Colon / caecum')),
            'The scheme marks these two labels')],
      'bio-2-6', 'drawing-the-alimentary-canal', at(12, '11.', '(b)', '(i)'), 18,
      decision='The drawing is priced "6, 3, 0" and each numbered pair of labels "2(2, 1, 0)": two labels at up to 2 '
               'each. The scheme does not say what earns a label 1 rather than 2; each label is carded at its full 2.'),
] + [
    T(f'11bii{n}', f'Q11(b)(ii){n}', 'C', item(10, n, end, 'in relation to lipase.'), rows, 'bio-2-6', concept,
      at(12, '11.', '(b)', '(ii)', why=ITEM_ROMAN), 3, stem=[Q11BII], decision=EACH_ITEM)
    for n, end, rows, concept in [
        (1, 'What is lipase?', [pt(S('Enzyme that digests lipids (or fats or oils)'), 3)], 'lipase'),
        (2, 'Give one part of the alimentary canal that secretes lipase.',
         [pt(S('Stomach or duodenum'), 3, note_sel=S('[accept small intestine or ileum or salivary glands or pancreas]'))],
         'where-lipase-is-made'),
        (3, 'What is the approximate pH at the site of lipase action?',
         [anyn(None, 1, 3, options=[S('Stomach: (pH) < 7'), S('Duodenum or small intestine or ileum: (pH) 7 – 9')])],
         'ph-for-lipase')]
] + [
    T('11ci1', 'Q11(c)(i)1', 'C', Q11CI1,
      [G('tokens-x', page=12, clip=(160, 470, 256, 508), expect='I 2 2 C 1 1 PM 2 2 M 3 3', marks=3,
         note='The scheme\'s formula is shown after reveal.')],
      'bio-2-6', 'human-dental-formula', at(12, '11.', '(c)', '(i)', why=ITEM_ROMAN), 3, fig='q11c-i-scheme',
      decision=EACH_ITEM + ' The scheme prints the formula as fractions (each tooth type\'s upper count over its lower '
               'count); the row reads it left to right from glyph positions, and the scheme\'s print of it is the '
               'solution figure.'),
    T('11ci2', 'Q11(c)(i)2', 'C', Q(10, '2.', 'arrangement of the mammal in the photograph below.',
                                  after='Write the dental formula'),
      [pt(S('(Humans have) fewer incisors (or fewer canines)', 'or Animal shown has more incisors (or more canines)'),
          3)], 'bio-2-6', 'comparing-dentition', at(12, '11.', '(c)', '(i)', why=ITEM_ROMAN), 3, stem=[Q11CI1],
      fig='q11c-teeth', decision=EACH_ITEM),
    T('11ci3', 'Q11(c)(i)3', 'C', Q(10, '3.', 'Explain your answer.', after='arrangement of the mammal'),
      [pt(S('meat or flesh or other animals'), 3, label=S('Type of food:')),
       pt(S('long (or sharp or pointed or large or extra)', 'canines (or incisors)'), 3, label=S('Explanation:'))],
      'bio-2-6', 'diet-from-teeth', at(12, '11.', '(c)', '(i)', why=ITEM_ROMAN), 6, fig='q11c-teeth',
      decision=EACH_ITEM),
    T('11cii', 'Q11(c)(ii)', 'C', ask(10, 'Give two functions of the large intestine.'),
      [anyn(S('Absorption of water / peristalsis / egestion / absorb vitamins'), 2, 3)], 'bio-2-6',
      'large-intestine', at(12, '11.', '(c)', '(ii)'), 6),
    T('11ciii', 'Q11(c)(iii)', 'C', ask(10, 'Outline two beneficial functions of the bacteria that live in the digestive tract.'),
      [anyn(S('Production of vitamins / compete with other micro-organisms /', 'digestion / benefit immune system'),
            2, 3)], 'bio-2-6', 'gut-bacteria', at(12, '11.', '(c)', '(iii)'), 6),
    T('12ai', 'Q12(a)(i)', 'C', ask(11, 'Write a balanced chemical equation for photosynthesis.'),
      [pt(S('6CO2 + 6H2O → C6H12O6 + 6O2'), 6, note_sel=S('6, 3, 0'), note_lead='The scheme marks this equation')],
      'bio-2-2', 'photosynthesis-equation', at(13, '12.', '(a)', '(i)'), 6,
      decision='The equation is one priced item ("6, 3, 0"). The text layer flattens its subscripts.'),
    T('12aii', 'Q12(a)(ii)', 'C', ask(11, 'Where precisely in a plant cell does photosynthesis occur?'),
      [pt(S('Chloroplast(s)'), 3)], 'bio-2-2', 'chloroplast', at(13, '12.', '(a)', '(ii)'), 3),
    T('12b', 'Q12(b)', 'C',
      [M('(i)', 11), ask(11, 'What is the energy source for the dark stage?'),
       M('(ii)', 11, br=True), Q(11, 'Give the details of the dark stage of photosynthesis.', 'diagram alone.'),
       M('(iii)', 11, br=True), ask(11, 'Give two uses of the main product of the dark stage.'),
       M('(iv)', 11, br=True), ask(11, 'Name two environmental factors on which the rate of photosynthesis depends.'),
       M('(v)', 11, br=True), ask(11, 'Suggest one advantage of using genetically modified crops.')],
      [pt(S('ATP'), 0),
       anyn(S('NADPH supplies H+ and e- (or NADPH supplies hydrogen or NADPH', 'NADP (or ADP) regenerated'), 4, 0),
       pt(S('Respiration (or described)'), 0),
       pt(S('Conversion to starch (or to other named carbohydrate)', 'or provides food (for other organisms)'), 0),
       anyn(S('Temperature / light intensity / CO2 conc.'), 2, 0),
       pt(S('Greater crop yield or resistant to disease or resistence to drought', 'or example of commercial advantage'),
          0)],
      'bio-2-2', 'dark-stage-of-photosynthesis', at(13, '12.', '(b)'), 27, stem=[Q12B], tariff='questionTotal',
      decision='The scheme prices (ii), four printed points, "3 + 6": as an ordered split (first point 3, second 6) '
               'or as three points at 3, the printed answers fit no one reading, so the whole of (b) is carded at the '
               'paper\'s (27), every row unpriced. The scheme\'s own notation: (i) "3", (ii) "3 + 6", (iii) "3" and '
               '"3", (iv) "2(3)", (v) "3".'),
    T('12ci', 'Q12(c)(i)', 'C', ask(11, 'Name Stage 1 and state its location in yeast cells.'),
      [pt(S('Glycolysis'), 3, label=S('Name:')), pt(S('Cytosol (or *cytoplasm)'), 3, label=S('Location:'))],
      'bio-2-2', 'glycolysis', at(13, '12.', '(c)', '(i)'), 6, stem=[Q12C], fig='q12c-respiration'),
    T('12cii', 'Q12(c)(ii)', 'C', Q(11, 'Copy the table below into your answer book and complete it', 'shown.'),
      [pt(S('Glucose or (Compound C)'), 3, label=S('6')), pt(S('Pyruvic acid'), 3, label=S('3', nth=2)),
       pt(S('Acetyl CoA or (Compound A)'), 3, label=S('2'))],
      'bio-2-2', 'carbon-atoms-in-respiration', at(13, '12.', '(c)', '(ii)'), 9, fig='q12c-respiration',
      qfig='q12c-ii-table',
      decision='Each row of the scheme\'s table is labelled with its own number of carbon atoms; the printed table '
               'and its ask are the question figure, the diagram the figure.'),
    T('12ciii', 'Q12(c)(iii)', 'C', ask(11, 'Name Gas X and Gas Y.'),
      [pt(S('Carbon dioxide'), 1, label=S('Gas X:'), note_sel=S('[accept CO2]')),
       pt(S('Oxygen'), 1, label=S('Gas Y:'), note_sel=S('[accept O2]'))],
      'bio-2-2', 'gases-in-respiration', at(13, '12.', '(c)', '(iii)'), 2, stem=[Q12C], fig='q12c-respiration'),
    T('12civ', 'Q12(c)(iv)', 'C', ask(11, 'Name the compound D and give two functions of this compound in yeast cells.'),
      [pt(S('Water'), 1, label=S('Compound D:'), note_sel=S('[accept H2O]')),
       anyn(S('solvent / biochemical reactant / maintain', 'medium for chemical reactions'), 2, 3)],
      'bio-1-2', 'functions-of-water', at(13, '12.', '(c)', '(iv)'), 7, stem=[Q12C], fig='q12c-respiration'),
] + [
    # "Fauna." alone is too short a question to stand: its card carries the
    # printed lead-in in its question text instead of its stem.
    T(f'13a{r}', f'Q13(a)({r})', 'C', [Q13A, ask(12, word, br=True)] if len(word) < 8 else ask(12, word),
      [pt(S(ans), 3)], 'bio-3-1', concept, lab(14, label), 3, stem=[] if len(word) < 8 else [Q13A])
    for r, word, label, ans, concept in [
        ('i', 'Ecosystem.', 'Ecosystem:', 'Organisms (interacting) with their environment', 'ecosystem'),
        ('ii', 'Community.', 'Community:', 'All (or groups) of organisms found in an ecosystem', 'community'),
        ('iii', 'Fauna.', 'Fauna:', 'Animals', 'fauna')]
] + [
    T('13bi', 'Q13(b)(i)', 'C', Q(12, 'All organisms have adaptations that help them survive and thrive.',
                                  'technique of the predator.'),
      [pt(S('Named predator and matching ecosystem'), 3, kind='criterion', note=NO_ANSWER),
       pt(S('Matching (behavioural) adaptive technique'), 3, kind='criterion', note=NO_ANSWER)],
      'bio-3-1', 'predator-adaptation', at(14, '13.', '(b)', '(i)'), 6, stem=[Q13B]),
    T('13bii1', 'Q13(b)(ii)1', 'C', Q(12, '1.', 'What is meant by the term variation?', after='technique of the predator.'),
      [pt(S('Differences within a population (or within a species or between', 'individuals)'), 3)], 'bio-1-5',
      'variation', at(14, '13.', '(b)', '(ii)', why=ITEM_ROMAN), 3, stem=[Q13B], decision=EACH_ITEM),
    T('13bii2', 'Q13(b)(ii)2', 'C', Q(12, '2.', 'ecosystem.', after='What is meant by the term variation?'),
      [pt(S('Differences in a named factor'), 3, kind='criterion', note=NO_ANSWER)], 'bio-3-1',
      'variation-in-plant-height', at(14, '13.', '(b)', '(ii)', why=ITEM_ROMAN), 3, stem=[Q13B],
      decision=EACH_ITEM),
    T('13biii1', 'Q13(b)(iii)1', 'C', Q(12, '1.', 'name appropriate organisms at A, B, C and D.', after='pyramid of numbers,'),
      [lead(allof([(S(ln, piece=1, psep=' = '), S(ln, piece=2, psep=' = ')) for ln in
                   ('D = Parasite', 'C = Named larger carnivore', 'B = Named smaller herbivore',
                    'A = Named (large) producer')], 3, note_sel=S('3, 2, 0')),
            'The scheme marks this item')],
      'bio-3-1', 'pyramid-of-numbers', at(14, '13.', '(b)', '(iii)', why=ITEM_ROMAN), 3, stem=[Q13B, Q13BIII],
      fig='q13b-pyramid',
      decision=EACH_ITEM + ' The four levels are priced together as one item ("3, 2, 0"): one row. The scheme names D '
                           'and prints only what earns the marks for A, B and C.'),
    T('13biii2', 'Q13(b)(iii)2', 'C', Q(12, '2.', 'indicate which organism is most likely to be a herbivore.',
                                        after='pyramid of numbers,'),
      [pt(S('B or herbivore named in (iii) B, above'), 3)], 'bio-3-1', 'herbivore-in-the-pyramid',
      at(14, '13.', '(b)', '(iii)', why=ITEM_ROMAN), 3, stem=[Q13B, Q13BIII], fig='q13b-pyramid',
      decision=EACH_ITEM),
    T('13biv1', 'Q13(b)(iv)1', 'C', Q(12, '1.', 'the length of the food chain?', after='What is the significance'),
      [pt(S('Limits the length (or described)'), 3)], 'bio-3-1', 'energy-loss-and-chain-length',
      at(14, '13.', '(b)', '(iv)', why=ITEM_ROMAN), 3, stem=[Q13B, Q13BIV], decision=EACH_ITEM),
    T('13biv2', 'Q13(b)(iv)2', 'C', Q(12, '2.', 'the number of organisms at the final trophic level?',
                                      after='What is the significance'),
      [pt(S('Limits the number (or described)'), 3)], 'bio-3-1', 'energy-loss-and-top-numbers',
      at(14, '13.', '(b)', '(iv)', why=ITEM_ROMAN), 3, stem=[Q13B, Q13BIV], decision=EACH_ITEM),
    T('13bv', 'Q13(b)(v)', 'C', Q(12, 'If a niche becomes vacant in an ecosystem for a decomposer species',
                                  'decomposer species may not be able to occupy the vacant niche.'),
      [pt(S('May not be suitably adapted (or described)'), 3)], 'bio-3-1', 'vacant-niche',
      at(14, '13.', '(b)', '(v)'), 3, stem=[Q13B]),
] + [
    T(f'13c{r}', f'Q13(c)({r})', 'C', ask(12, practice), [pt(S(*ans), 6)], 'bio-3-1', concept,
      at(14, '13.', '(c)', f'({r})'), 6, stem=[Q13C])
    for r, practice, ans, concept in [
        ('i', 'The release of non-native animals into the Irish countryside.',
         ('Can become pests or can spread disease or native organisms have', 'or extinction of native species'),
         'non-native-animals'),
        ('ii', 'Using fishing nets of very small mesh size.',
         ('Young (or small) fish trapped or reduced reproduction rates (or', 'depletes fish stocks) or extinction of species'),
         'small-mesh-nets'),
        ('iii', 'Hedgerow cutting in spring and summer.',
         ('Disrupts (bird) nesting or endangering animals or disrupts food', 'chains (or described)'),
         'hedgerow-cutting'),
        ('iv', 'Spreading slurry on farmland.', ('Toxic or risk of infection or pollution of waterways (or described)',),
         'spreading-slurry')]
] + [
    T('14ai', 'Q14(a)(i)', 'C', ask(13, 'Outline how any one named feature of the human general defence system works.'),
      [pt(S('Feature named'), 3, kind='criterion', note=NO_ANSWER),
       pt(S('Mechanism described'), 3, kind='criterion', note=NO_ANSWER)], 'bio-2-4', 'general-defence-system',
      at(15, '14.', '(a)', '(i)'), 6),
    T('14aii', 'Q14(a)(ii)', 'C', ask(13, 'Name two organs in the human body that are specific to the immune system.'),
      [anyn(S('Thymus / spleen / lymph nodes / tonsils'), 2, 3)], 'bio-2-4', 'immune-organs',
      at(15, '14.', '(a)', '(ii)'), 6),
    T('14aiii', 'Q14(a)(iii)', 'C', ask(13, 'Distinguish clearly between an antigen and an antibody.'),
      [anyn(None, 1, 3, options=[S('Antigen:', '(foreign particle that) causes an antibody response'),
                                 S('Antibody:', 'infection)')])], 'bio-2-4', 'antigen-and-antibody',
      at(15, '14.', '(a)', '(iii)'), 3,
      decision='The scheme prints the antigen and the antibody joined by "OR" at "3": one menu, claim one.'),
    T('14aiv1', 'Q14(a)(iv)1', 'C', item(13, 1, 'in an immune response.', 'T cells are a type of lymphocyte'),
      [pt(S('recognise infected cell (or cancer or antigen)', 'or kill cancer cell', skip_marks=True), 6,
          label=S('Killer T cells:')),
       pt(S('produce interferon or recognise antigens or', 'activate Killer T cells'), 6, label=S('Helper T cells:'))],
      'bio-2-4', 'killer-and-helper-t-cells', at(15, '14.', '(a)', '(iv)', why=ITEM_ROMAN), 12, stem=[Q14AIV],
      decision=EACH_ITEM + ' The scheme prints the killer T cell row\'s mark between its lines; the answer is read '
                           'without it.'),
    T('14aiv2', 'Q14(a)(iv)2', 'C', item(13, 2, 'Name the T cells that stop the immune response.',
                                         'T cells are a type of lymphocyte'),
      [pt(S('Suppressor (T cells)'), 3)], 'bio-2-4', 'suppressor-t-cells',
      at(15, '14.', '(a)', '(iv)', why=ITEM_ROMAN), 3, stem=[Q14AIV], decision=EACH_ITEM),
] + [
    T(f'14bi-{x.lower()}', 'Q14(b)(i)', 'C',
      ask(13, 'Name the parts labelled A, B and C in the diagram of the cross section of the spinal cord.'),
      [pt(S(line, piece=2, psep=' = '), 1)], 'bio-2-4', concept, at(16, '14.', '(b)', '(i)'), 1, fig='q14b-spinal',
      item=(x.lower(), x), labels=[L(y, S(ln, page=16, piece=2, psep=' = '), y == x) for y, ln in SPINAL],
      decision='A lettered figure the scheme prices letter by letter ("1" each): one card per letter.')
    for (x, line), concept in zip(SPINAL, ['grey-matter', 'white-matter', 'central-canal'])
] + [
    T('14bii', 'Q14(b)(ii)', 'C', ask(13, 'What is the main structural difference between A and B?'),
      [pt(S('A: consists (mainly) of cell bodies or (mostly) no myelin'), 3),
       pt(S('B: consists (mainly) of axons or (mostly) myelin'), 3)], 'bio-2-4', 'grey-and-white-matter',
      at(16, '14.', '(b)', '(ii)'), 6, fig='q14b-spinal',
      labels=[L(y, S(ln, page=16, piece=2, psep=' = '), False) for y, ln in SPINAL]),
    T('14biii1', 'Q14(b)(iii)1', 'C', Q(13, '1.', 'What is the function of the meninges?',
                                        after='What is the main structural difference'),
      [pt(S('Protection (of CNS)'), 3)], 'bio-2-4', 'function-of-meninges',
      at(16, '14.', '(b)', '(iii)', why=ITEM_ROMAN), 3, decision=EACH_ITEM),
    T('14biii2', 'Q14(b)(iii)2', 'C', Q(13, '2.', 'How many layers are present in the meninges?',
                                        after='What is the main structural difference'),
      [pt(S('Three'), 3)], 'bio-2-4', 'layers-of-meninges', at(16, '14.', '(b)', '(iii)', why=ITEM_ROMAN), 3,
      decision=EACH_ITEM),
    T('14biv1', 'Q14(b)(iv)1', 'C', item(13, 1, 'What is a reflex action?', 'Reflex actions are very important'),
      [pt(S('Automatic (or involuntary) response to a stimulus'), 3)], 'bio-2-4', 'reflex-action',
      at(16, '14.', '(b)', '(iv)', why=ITEM_ROMAN), 3, stem=[Q14BIV], decision=EACH_ITEM),
    T('14biv2', 'Q14(b)(iv)2', 'C', item(13, 2, 'Outline the mechanism of a reflex action.', 'Reflex actions are very important'),
      [anyn(S('Stimulus at receptor / (causes) impulse along sensory', '(another impulse is sent) to the brain.'), 2, 6,
            note_sel=S('Any Two'))], 'bio-2-4', 'reflex-arc', at(16, '14.', '(b)', '(iv)', why=ITEM_ROMAN), 12,
      stem=[Q14BIV], decision=EACH_ITEM),
    T('14ci', 'Q14(c)(i)', 'C', Q14CI,
      [pt(S('testis + prostate (or seminal vesicles or Cowper’s gland)', '+ sperm duct & urethra + penis'), 6,
          kind='criterion', label=S('Diagram:'), note_sel=S('6, 3, 0'), note_lead='The scheme marks this diagram'),
       anyn(S('testis, epididymis, sperm duct, seminal vesicle,', 'Cowper’s gland, prostate gland, urethra, penis, scrotum'),
            2, 3, steps=[3, 2], sep=',')],
      'bio-2-5', 'drawing-the-male-system', at(16, '14.', '(c)', '(i)'), 11,
      decision='The drawing is priced "6, 3, 0" and its labels "3 + 2": a menu of the printed labels, the first '
               'correct label 3 and the second 2.'),
    T('14cii', 'Q14(c)(ii)', 'C', ask(13, 'Put X on the diagram where meiosis occurs.'),
      [pt(S('X on testes'), 1)], 'bio-2-5', 'where-meiosis-occurs', at(16, '14.', '(c)', '(ii)'), 1,
      stem=[M('(i)', 13), Q14CI],
      decision='"The diagram" is the candidate\'s own drawing from (i), not printed artwork: no figure.'),
    T('14ciii', 'Q14(c)(iii)', 'C', ask(13, 'Give a function of one named gland.'),
      [pt(S('Named gland + function'), 3, kind='criterion', note=NO_ANSWER)], 'bio-2-5', 'gland-function',
      at(16, '14.', '(c)', '(iii)'), 3),
    T('14civ1', 'Q14(c)(iv)1', 'C', item(13, 1, 'Suggest why a sperm cell needs so many mitochondria.',
                                         'Part B contains many mitochondria.'),
      [pt(S('(Sperm cells) need a lot of energy or (sperm cells) need to swim',
            'long distances (or described) (compared to their size)'), 3),
       pt(S('Mitochondria produce energy or mitochondria carry out', '(aerobic) respiration'), 3)],
      'bio-2-5', 'mitochondria-in-sperm', at(16, '14.', '(c)', '(iv)', why=ITEM_ROMAN), 6, stem=[Q14CIV],
      fig='q14c-sperm', decision=EACH_ITEM),
    T('14civ2', 'Q14(c)(iv)2', 'C', item(13, 2, 'Suggest why this is the case.', 'Part B contains many mitochondria.'),
      [pt(S('Only the head (of the sperm) enters the egg', 'or no sperm mitochondria enter the egg'), 3)],
      'bio-2-5', 'maternal-mitochondria', at(16, '14.', '(c)', '(iv)', why=ITEM_ROMAN), 3, stem=[Q14CIV],
      fig='q14c-sperm', decision=EACH_ITEM),
    T('14cv', 'Q14(c)(v)', 'C', ask(13, 'State the survival times of the egg and sperm in the female body.'),
      [pt(S('12 – 48 hours'), 3, label=S('Egg:')), pt(S('0 – 7 days'), 3, label=S('Sperm:'))], 'bio-2-5',
      'survival-of-gametes', at(16, '14.', '(c)', '(v)'), 6),
] + [
    T(f'15a{r}', f'Q15(a)({r})', 'C', ask(14, q), rows, 'bio-2-5', concept, at(17, '15.', '(a)', f'({r})'), total,
      stem=[Q15A])
    for r, q, rows, concept, total in [
        ('i', 'Following fertilisation, from precisely which part of the flower is the seed formed?',
         [pt(S('Ovule'), 3)], 'ovule', 3),
        ('ii', 'What is meant by the term monocotyledonous?', [pt(S('One seed leaf'), 3)], 'monocotyledonous', 3),
        ('iii', 'Name two biomolecules stored in endosperm or cotyledon tissue.',
         [anyn(S('Lipids (or fats or oils) / protein / carbohydate (or named) / vitamin(s)'), 2, 3)], 'seed-food-stores',
         6),
        ('iv', 'Give one way knowledge of seed dormancy has been useful to humans.',
         [pt(S('How to store (seeds) or when to sow (seeds) or maximise the growing',
               'season or seed treatment before sowing (or examples)'), 3)], 'uses-of-dormancy', 3)]
] + [
    T(f'15av{n}', f'Q15(a)(v){n}', 'C', item(14, n, end, 'of a tissue with its water content removed.)'), rows,
      'bio-2-5', concept, at(17, '15.', '(a)', '(v)', why=ITEM_ROMAN), total, stem=[Q15A, Q15AV], fig='q15a-graph',
      decision=EACH_ITEM)
    for n, end, rows, concept, total in [
        (1, 'Suggest why the measurement of dry mass is preferred in these investigations.',
         [pt(S('Water content could vary between seeds'), 3)], 'why-dry-mass', 3),
        (2, 'Explain why the dry mass of the endosperm tissue decreases over the three weeks.',
         [pt(S('Food is transferred to the embryo or respiration or loss of CO2'), 3)], 'endosperm-loses-mass', 3),
        (3, 'What process begins at A?', [pt(S('Photosynthesis'), 3)], 'photosynthesis-begins', 3),
        (4, 'Explain your answer.', [pt(S('(No as) it will lose mass'), 3), pt(S('(Due to) respiration or loss of CO2'), 3)],
         'seed-dry-mass-before-photosynthesis', 6)]
] + [
    T('15bi', 'Q15(b)(i)', 'C', ask(14, 'Draw a large labelled diagram to show the structure of Rhizopus.'),
      [pt(S('rhizoids + hypha + sporangiophore + sporangium'), 3, kind='criterion', label=S('Diagram:'),
          note_sel=S('3, 0'), note_lead='The scheme marks this diagram'),
       anyn(S('Rhizoids / hypha(e) or stolon / apophysis / sporangium /', 'sporangiophore / columella / spores / mycelium'),
            3, 1)],
      'bio-3-2', 'drawing-rhizopus', at(18, '15.', '(b)', '(i)'), 6,
      decision='The drawing is priced "3, 0" and its labels "3(1)": the drawing and the label menu are the rows.'),
    T('15bii1', 'Q15(b)(ii)1', 'C', item(14, 1, 'What is the role of fungi such as Rhizopus in nature?',
                                         'Draw a large labelled diagram to show the structure'),
      [pt(S('Decomposer (or description of decomposition)'), 3)], 'bio-3-2', 'fungi-as-decomposers',
      at(18, '15.', '(b)', '(ii)', why=ITEM_ROMAN), 3, decision=EACH_ITEM),
    T('15bii2', 'Q15(b)(ii)2', 'C', item(14, 2, 'Why is this role vital?', 'Draw a large labelled diagram to show the structure'),
      [pt(S('(To allow) recycling of nutrients (or minerals or elements)'), 3)], 'bio-3-2', 'why-decomposition-matters',
      at(18, '15.', '(b)', '(ii)', why=ITEM_ROMAN), 3,
      stem=[item(14, 1, 'What is the role of fungi such as Rhizopus in nature?',
                 'Draw a large labelled diagram to show the structure')], decision=EACH_ITEM),
    T('15biii', 'Q15(b)(iii)', 'C', ask(14, 'Give one structural difference between Fungi and Plantae.'),
      [pt(S('(Fungi) have (cell wall of) chitin', 'or (Plantae) have chloroplasts'), 3)], 'bio-3-2',
      'fungi-and-plants', at(18, '15.', '(b)', '(iii)'), 3),
    T('15biv', 'Q15(b)(iv)', 'C', ask(14, 'Name the method of asexual reproduction in Rhizopus.'),
      [pt(S('Sporulation'), 3)], 'bio-3-2', 'rhizopus-asexual-reproduction', at(18, '15.', '(b)', '(iv)'), 3),
    T('15bv', 'Q15(b)(v)', 'C', ask(14, 'Describe in detail the process of sexual reproduction in Rhizopus.'),
      [anyn(S('Different strains of or', 'meiosis or germination (of zygospore)'), 4, 3,
            note='The empty box after "+" is printed so in the scheme: a character its font did not print.')],
      'bio-3-2',
      'rhizopus-sexual-reproduction', at(18, '15.', '(b)', '(v)'), 12,
      decision='The scheme\'s first point prints its minus sign as a missing glyph (the page shows an empty box '
               'between the quotation marks after "+"); the point is lifted as printed.'),
    T('15ci', 'Q15(c)(i)', 'C', ask(15, 'Name the three general shapes of bacterial cells.'),
      [anyn(S('Rod (or bacilli) / spherical (or cocci) / spiral (or spirilla)'), 3, 1)], 'bio-3-2', 'bacterial-shapes',
      at(19, '15.', '(c)', '(i)'), 3),
    T('15cii', 'Q15(c)(ii)', 'C', ask(15, 'What is meant by the term pathogen?'),
      [pt(S('Disease-causing (agent or organism)'), 3)], 'bio-3-2', 'pathogen', at(19, '15.', '(c)', '(ii)'), 3),
    T('15ciii', 'Q15(c)(iii)', 'C', ask(15, 'What is the difference between ‘asepsis’ and ‘sterility’?'),
      [pt(S('Free of pathogens'), 3, label=S('Asepsis:')), pt(S('Free of (micro)organisms'), 3, label=S('Sterility:'))],
      'bio-3-2', 'asepsis-and-sterility', at(19, '15.', '(c)', '(iii)'), 6),
    T('15civ', 'Q15(c)(iv)', 'C', ask(15, 'Give one way in which bacteria cope with unfavourable environments.'),
      [pt(S('(Endo)spore formation'), 3)], 'bio-3-2', 'endospores', at(19, '15.', '(c)', '(iv)'), 3),
] + [
    T(f'15cv1-{x.lower()}', 'Q15(c)(v)1', 'C', item(15, 1, 'Name the stages B, C and D.', 'in relation to this graph.'),
      [pt(S(line, piece=2, psep=' = '), 1)], 'bio-3-2', concept, at(19, '15.', '(c)', '(v)', why=ITEM_ROMAN), 1,
      stem=Q15CV, fig='q15c-graph', item=(x.lower(), x),
      labels=[L(y, S(ln, page=19, piece=2, psep=' = '), y == x) for y, ln in STAGES],
      decision='A lettered graph the scheme prices stage by stage ("1" each): one card per letter.')
    for (x, line), concept in zip(STAGES, ['log-phase', 'stationary-phase', 'decline-phase'])
] + [
    T('15cv2', 'Q15(c)(v)2', 'C', item(15, 2, 'Explain what is happening during stage C.', 'in relation to this graph.'),
      [pt(S('Limited space (or food or O2) or waste (or toxin) accumulating', 'or death rate = birth rate'), 3)],
      'bio-3-2', 'stationary-phase-explained', at(19, '15.', '(c)', '(v)', why=ITEM_ROMAN), 3, stem=Q15CV,
      fig='q15c-graph', decision=EACH_ITEM),
    T('15cv3', 'Q15(c)(v)3', 'C', item(15, 3, 'stages labelled in the graph in your answer.', 'in relation to this graph.'),
      [pt(S('Fixed amount of nutrients added at beginning', 'or (bioreactor) emptied at end of production'), 3,
          label=S('Batch processing:')),
       pt(S('Nutrients continuously fed into (bioreactor)', 'or product removed continuously'), 3,
          label=S('Continuous flow:')),
       anyn(None, 1, 3, options=[S('Batch:', 'All stages occur'),
                                 S('Continuous flow:', 'maintained', after='Stage Reference:')],
            note_sel=S('Stage Reference:'))],
      'bio-3-2', 'batch-and-continuous-flow', at(19, '15.', '(c)', '(v)', why=ITEM_ROMAN), 9, stem=Q15CV,
      fig='q15c-graph',
      decision=EACH_ITEM + ' The stage reference prints the batch and the continuous-flow answers joined by "OR" at '
                           '"3": one menu, claim one.'),
]

# Section A parts anchored on a marker that opens its own answer line.
WELDED_TASKS = [
    T('2b', 'Q2(b)', 'A', ask(2, 'Give one example of a factor, other than light, which may be a source of competition among plants.'),
      [pt(S('Water or minerals or space', after='All (individuals) get some'), 8)], 'bio-3-1',
      'competition-among-plants', welded(5, '2.', '(b)'), 8, decision=ladder(2, '8 + 7 + 5(1)') + ' Seven responses.'),
    T('3a', 'Q3(a)', 'A', ask(3, 'What is the main chemical constituent of part A?'),
      [pt(S('Protein', after='Best 6:'), 8)], 'bio-1-1', 'virus-protein-coat', welded(6, '3.', '(a)'), 8, stem=[Q3],
      fig='q3-virus', decision=ladder(3, 'Best 6: 8 + 8 + 4(1)') + ' Seven parts, the best six priced.'),
    T('3b', 'Q3(b)', 'A', ask(3, 'Viruses are obligate parasites. What does this mean in relation to viruses?'),
      [G('tokens', page=6, clip=(100, 145, 455, 196),
         expect='Can only replicate (or reproduce) in a cell or can only replicate using a cell', marks=8,
         row_kind='alt')],
      'bio-1-1', 'obligate-parasites', welded(6, '3.', '(b)'), 8,
      decision=ladder(3, 'Best 6: 8 + 8 + 4(1)') + ' The text layer interleaves this answer\'s two lines with Q4\'s '
               'key printed beside them; the answer is read from its own column by glyph position.'),
    T('3c', 'Q3(c)', 'A', ask(3, 'B is one of two possible biomolecules. Name one of these.'),
      [pt(S('RNA or DNA', after='Best 6:'), 8)], 'bio-1-1', 'virus-nucleic-acid', welded(6, '3.', '(c)', nth=2), 8,
      stem=[Q3], fig='q3-virus', decision=ladder(3, 'Best 6: 8 + 8 + 4(1)') + ' Seven parts, the best six priced.'),
    T('3e', 'Q3(e)', 'A', ask(3, 'How do scientists distinguish between different viruses?'),
      [G('tokens', page=6, clip=(100, 258, 455, 309),
         expect='Shape (of protein coat) or type of nucleic acid or antibody (antigen) reaction or size or host '
                'species or structure', marks=8, row_kind='alt')],
      'bio-1-1', 'distinguishing-viruses', welded(6, '3.', '(e)', nth=2), 8,
      decision=ladder(3, 'Best 6: 8 + 8 + 4(1)') + ' The text layer interleaves this answer\'s two lines with Q4\'s '
               'key printed beside them; the answer is read from its own column by glyph position.'),
    T('3f', 'Q3(f)', 'A', ask(3, 'Viruses are difficult to classify into a kingdom. Why is this so?'),
      [pt(S('Non cellular or no (cell) organelles', after='Best 6:'), 8)], 'bio-1-1', 'classifying-viruses',
      welded(6, '3.', '(f)', nth=2), 8, decision=ladder(3, 'Best 6: 8 + 8 + 4(1)') + ' Seven parts, the best six priced.'),
    T('3g', 'Q3(g)', 'A', ask(3, 'Give one way in which viruses are economically important to humans.'),
      [pt(S('Manufacture of vaccines or enhancement of plant phenotype (or',
            'or biological control or harms plants (or harms animals)', after='Best 6:'), 8)], 'bio-1-1',
      'economic-importance-of-viruses', welded(6, '3.', '(g)', nth=2), 8,
      decision=ladder(3, 'Best 6: 8 + 8 + 4(1)') + ' Seven parts, the best six priced.'),
    T('5b', 'Q5(b)', 'A', Q5B,
      [anyn(S('They lost water / by osmosis / because sucrose was more concentrated', after='Best 6:'), 2, 8,
            note_sel=S('Any Two', after='Best 6:'))], 'bio-2-6', 'why-potato-lost-mass', welded(6, '5.', '(b)'), 16,
      stem=[Q5], fig='q5-graph', decision=ladder(5, '8 + 8 + 4(1)') + ' Any two: two responses on the ladder.'),
    T('5c', 'Q5(c)', 'A', Q(4, 'Give one example of the use of the mechanism(s) described in (b) in food preservation.'),
      [pt(S('Salting (or curing) meat (or fish) or making fruit products such as jam or use of sugar for',
            '(preserving) fruit', after='Best 6:'), 8)], 'bio-2-6', 'osmosis-in-food-preservation',
      welded(6, '5.', '(c)'), 8, stem=[Q5, M('(b)', 4), Q5B], fig='q5-graph', decision=ladder(5, '8 + 8 + 4(1)')),
    T('5d', 'Q5(d)', 'A', Q(4, 'Explain how plant cells remain turgid.'),
      [anyn(S('Water taken in / (water) into vacuole (or into cytoplasm) / protoplast (or membrane)',
              'presses against cell wall / wall prevents bursting', after='Best 6:'), 2, 8,
            note_sel=S('Any Two', after='Salting (or curing)'))], 'bio-2-6', 'turgor', welded(6, '5.', '(d)'), 16,
      decision=ladder(5, '8 + 8 + 4(1)') + ' Any two: two responses on the ladder.'),
]

FIGURES = {
    # key suffix: (doc, page, rect in PDF points, credit, letters, alt, solution[, masks])
    'q5-graph': ('paper', 4, (160, 118, 445, 342), SEC, ['A', 'B', 'C', 'D', 'E', 'F'],
                 'Line graph of change in mass (g), marked from -25 to 25 on the vertical axis, against % sucrose '
                 'solution, marked 0.2 to 1.0 on the horizontal axis, with a horizontal line drawn across at 0. Six '
                 'points labelled A to F are joined by a line that falls from left to right: A at about 23 on the '
                 'vertical axis, B at about 7 at 0.2, C where the line crosses the zero line between 0.2 and 0.4, '
                 'D at about -13 a little before 0.6, E at about -22 at 0.8 and F at about -24 at 1.0.', False),
    'q6-skin': ('paper', 5, (150, 58, 480, 282), SEC, ['A', 'B'],
                'Line drawing of a vertical section through skin: a dense speckled band along the top over a dotted '
                'layer; a hair rising out of the surface from a dark bulb deep in the section, with a rounded sac '
                'beside its shaft; a thin slanting band running from beside the hair\'s root up towards the surface '
                'layers; branching vessels, two round bodies with fine threads and a ringed body in the middle '
                'layer; a narrow tube running down from the surface to a tight coil; and a bottom layer of rounded '
                'cells. Label A points to the slanting band beside the hair and label B to the coiled tube.', False),
    'q10c-birds': ('paper', 9, (90, 420, 540, 518), SEC, ['A', 'B', 'C', 'D', 'E'],
                   'Five ovals labelled A to E, each holding a pair of long chromosomes, each marked at an upper and '
                   'a lower position, beside a pair of shorter chromosomes. A: G and g at the upper positions, L and '
                   'l at the lower, the short pair X and X. B: G and G, L and L, X and Y. C: G and G, L and L, X and '
                   'X. D: g and g, l and l, X and Y. E: G and g, L and l, X and Y.', False),
    'q11c-i-scheme': ('scheme', 12, (160, 468, 256, 509), SEC, [],
                      "The marking scheme's dental formula: I with 2 over 2, C with 1 over 1, PM with 2 over 2 and M "
                      'with 3 over 3, each pair of numbers set as a fraction after its letters.', True),
    'q11c-teeth': ('paper', 10, (195, 494, 462, 639), SEC, [],
                   "Black-and-white photograph, seen from the front, of a mammal's open mouth against a dark "
                   'background: a row of small, blunt front teeth along the upper and the lower jaw, with a long, '
                   'pointed, curved tooth rising well beyond them on each side.', False),
    'q12c-respiration': ('paper', 11, (120, 340, 455, 575), SEC, ['A', 'B', 'C', 'D', 'X', 'Y'],
                         'Flow diagram: Glucose, then an arrow labelled Stage 1 down to Pyruvic acid. From pyruvic '
                         'acid an arrow labelled Anaerobic pathway runs right to Compound A + Gas X, and a line runs '
                         'down to Acetyl CoA, branching on the way to give off Gas X to the left and Hydrogen to the '
                         'right. A curved arrow leads from Acetyl CoA into Compound C; an arc runs from Compound B '
                         'over to Compound C; beneath them, beside the words Other compounds, arrows give off Gas X '
                         'near Compound C and near Compound B, and a loop below sends an arrow right to a second '
                         'Hydrogen. Both Hydrogen arrows lead into a box labelled Electron transport system; beside '
                         'it, Gas Y enters a curved arrow that ends at Compound D.', False),
    'q12c-ii-table': ('paper', 11, (45, 615, 560, 736), SEC, [],
                      'The printed question: (ii) Copy the table below into your answer book and complete it by '
                      'inserting a letter or name, from the diagram above, to identify a compound which has the '
                      'number of carbon atoms shown. A two-column table headed Number of carbon atoms and Compound, '
                      'its rows reading 6, 3 and 2, the Compound column empty.', False),
    'q13b-pyramid': ('paper', 12, (432, 292, 502, 370), SEC, ['A', 'B', 'C', 'D'],
                     'A pyramid of numbers drawn as four stacked boxes: A, a small narrow box, at the bottom; B, a '
                     'wide box, above it; C, a small narrow box, above B; and D, a wide box, on top.', False),
    'q14b-spinal': ('paper', 13, (140, 225, 440, 368), SEC, ['A', 'B', 'C'],
                    'Drawing of a cross section of the spinal cord: a rounded outline with a deep notch at the bottom '
                    'and a shallow one at the top, two large looped outlines inside it on either side, a shaded grey '
                    'region shaped like a butterfly in the centre with a small oval opening at its middle, and nerve '
                    'fibres with small round cell bodies running out from the grey region to the right. Label A '
                    'points into the shaded region, label B to the unshaded tissue below it and label C to the small '
                    'central opening.', False),
    'q14c-sperm': ('paper', 13, (225, 628, 325, 692), SEC, ['B'],
                   'Drawing of a sperm cell: a rounded head on the right, a short, thicker section behind it and a '
                   'long, thin, curving tail. Label B points to the short section behind the head.', False),
    'q15a-graph': ('paper', 14, (222, 240, 420, 408), SEC, ['A'],
                   'Graph of dry mass (g) against time (days) from 0 to 21. A straight line labelled Endosperm falls '
                   'from high on the left to low on the right. A line labelled Embryo rises gently from low on the '
                   'left, crosses the endosperm line and, at a point labelled A shortly before day 21, turns sharply '
                   'upwards.', False),
    'q15c-graph': ('paper', 15, (165, 305, 405, 445), SEC, ['A', 'B', 'C', 'D'],
                   'Graph of bacterial population size against time: a low flat stretch labelled A, a steep rise '
                   'labelled B, a high flat stretch labelled C and a steep fall labelled D.', False),
}

WELDED_FIGURES = {
    'q3-virus': ('paper', 3, (200, 70, 400, 205), SEC, ['A', 'B'],
                 'Drawing of a round virus particle: a dark, finely speckled circular core holding a single wavy '
                 'thread, inside a lighter grey outer ring from which about twelve short stalks with rounded knobs '
                 'project all round. Label A points to the lighter outer ring and label B to the wavy thread in the '
                 'core.', False),
}

TASKS += WELDED_TASKS
FIGURES.update(WELDED_FIGURES)
