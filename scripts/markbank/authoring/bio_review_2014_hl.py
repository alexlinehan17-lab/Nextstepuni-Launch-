"""Biology 2014 Higher Level — reviewed task ledger, carded from the paper for the first time.

Independent visual sweep (2026-10-25), every page rendered and read:
  * The 2014 paper is one booklet (M44), 16 pages: p1 cover and instructions,
    p2-p5 Section A Questions 1-6, p6-p8 Section B Questions 7-9, p9-p15
    Section C Questions 10-15, p16 "Blank Page". Sections A and B are
    answered on the paper; Section C in an answer book. No acknowledgements
    page: the Q11(a) photograph and every drawing carry no credit; the
    Q11(c) extract prints its own source line (TIME), lifted with it.
  * The marking scheme, 20 pages: p1 cover, p2 note, p3 introduction,
    cancelled answers and surplus answers, p4 surplus answers (continued) and
    conventions, p5-p16 Questions 1-15, p17-p19 "Blank Page", p20 back cover
    (no text layer).

The paper's shape is the long-standing one: any five of Section A's six
questions, any two of Section B's three, any four of Section C's six, and
Q14 and Q15 are each any two of (a), (b), (c). Every printed ask is carded.

This scheme prints no reprint of any question, only a few label words
("Graph A:", "Advantage:", "Labels:"): each answer stands under its own
question number, letter and roman. A task is anchored on its own part marker,
found by walking the scheme's numbering down to it (SQ path); where the
marker opens its answer's own line ("(a) C = Lymph vessel", "(iii) *mRNA") it
is a welded bare anchor. A numbered item ("1.", "2.") is anchored on the roman
it is printed under. Q1's terms are the one reprint: the scheme prints each
term ("Biosphere") over its definition, and Q1's tasks are anchored on it.

Tariffs. Section A is ordered splits, carded at their first rate: Q1 "2(7) +
3(2) i.e. best five answers from (a) - (f)" (six parts, the best five
priced), Q2 "7 + 6 + 7(1)" (nine responses), Q3, Q4, Q5 and Q6 "8 + 7 +
5(1)" (seven responses each). Sections B and C print a mark against every
row ("3", "2(3)", "3(1)", a drawing's "6, 3, 0" or "3, 0", Q8(a)(ii)'s "3, 2,
1, 0"), so every Section B and C task is priced row by row against the
paper's Section B rubric "Part (a) carries 6 marks and part (b) carries 24
marks", Section C's (9), (27), (24), and Q14/Q15's (30, 30).

Every printed answer fits a per-response tariff, so no part is carded whole.

Q5's key is a separate box beside Q4's ("5. 8 + 7 + 5(1)") holding seven
cells, F F F T F F T, one per statement in the order (a)-(g), with no part
markers and no reprint. Each statement's answer is read from its own cell by
glyph position, and the task is anchored on that cell (see Q5_KEY below).

The text layer interleaves Q4's answer lines with Q5's cells printed beside
them; Q4(a)(i), (iii) and (iv) are read from their own column by glyph
position. Q12(c)(iv)'s two answers are printed side by side, joined by "OR";
each reason is read from its own column.

Alternatives the scheme prints as matched sets joined by "OR" are answer
variants of one task: Q10(b)(v) "No, because ..." or "Yes, because ...",
Q12(c)(iv) pulmonary vein or pulmonary artery with its reason, Q13(c)(iii)
the iodoform or the dichromate test.

Q15(c)(ii)'s menu prints its last line as "or improved medicine or improved
hygiene" after a solidus; the runner reads a menu line opening "or" as a
closing alternative, shows it with the menu and marks the menu open.

The census reader welded Q9(b)(ii) onto the tail of Q9(b)(i) (page 8 sets
"(ii)" on its own line under Q9(b)(i)3's answer line); a gated WELDED_HEADS
entry in paper.py splits it, which takes the census from 128 leaves to the
paper's 129. All 129 are claimed by the 139 tasks here.
"""
from bio_review_lib import Q, SQ, S, M, pt, anyn, T, L, G

YEAR, LEVEL = 2014, 'hl'
REVIEWED_AT = '2026-10-25'

SOURCES = {
    'paper': {'path': 'examiner-reports/biology/papers/2014-hl-paper.pdf',
              'fileid': 'LC025ALP000EV.pdf',
              'sha256': '94a39630e704fc6acec5ff8e78d44757f9121ceea16ab3ab4d3df87a34e4dbba',
              'pages': 16},
    'scheme': {'path': 'examiner-reports/biology/schemes/2014-hl.pdf',
               'fileid': 'LC025ALP000EV.pdf',
               'sha256': '3b597c53e9e2a4570891c681ce06d873d5616124a58f0101505ab2eae9adb576',
               'pages': 20},
}

PAGE_ROLES = {
    'paper': {1: 'cover', **{p: 'questions' for p in range(2, 16)}, 16: 'blank'},
    'scheme': {1: 'cover', 2: 'note', 3: 'introduction', 4: 'conventions',
               **{p: 'marking' for p in range(5, 17)}, **{p: 'blank' for p in range(17, 20)},
               20: 'back-cover'},
}


def _ladder(notation, **extra):
    steps = []
    for term_ in notation.split('+'):
        n, _, m = term_.strip().partition('(')
        steps += [int(m.rstrip(')'))] * int(n) if m else [int(n)]
    return {'steps': steps, 'notation': notation, **extra}


QUESTION_TOTALS = {
    **{n: 20 for n in range(1, 7)}, **{n: 30 for n in range(7, 10)},
    **{n: 60 for n in range(10, 14)}, 14: 90, 15: 90,   # Q14, Q15: any two of three 30s
}
# Only parts priced row by row: a ladder question's cards are carded at the
# ladder's first rate, so their sum is not the printed total.
PART_TOTALS = {
    **{(n, 'a'): 6 for n in (7, 8, 9)},   # p6: "Part (a) carries 6 marks
    **{(n, 'b'): 24 for n in (7, 8, 9)},   # and part (b) carries 24 marks"
    **{(n, 'a'): 9 for n in (10, 11, 12, 13)},   # the paper's "(9)"
    **{(n, 'b'): 27 for n in (10, 11, 12, 13)},   # "(27)"
    **{(n, 'c'): 24 for n in (10, 11, 12, 13)},   # "(24)"
    **{(n, x): 30 for n in (14, 15) for x in 'abc'},   # "(30, 30)"
}
LADDERS = {
    # Q1: six parts, the best five priced "2(7) + 3(2)".
    1: _ladder('2(7) + 3(2)', responses=6),
    2: _ladder('7 + 6 + 7(1)'),
    3: _ladder('8 + 7 + 5(1)'), 4: _ladder('8 + 7 + 5(1)'), 5: _ladder('8 + 7 + 5(1)'), 6: _ladder('8 + 7 + 5(1)'),
}

CHECKSUMS = {
    1: {7: 6}, 2: {7: 9}, 3: {8: 7}, 4: {8: 7}, 5: {8: 7}, 6: {8: 7},
    (7, 'a'): {3: 1, 1: 3}, (7, 'b'): {3: 8},
    (8, 'a'): {3: 2}, (8, 'b'): {3: 8},
    (9, 'a'): {3: 2}, (9, 'b'): {3: 8},
    (10, 'a'): {3: 3}, (10, 'b'): {3: 7, 6: 1}, (10, 'c'): {3: 8},
    (11, 'a'): {3: 3}, (11, 'b'): {3: 9}, (11, 'c'): {3: 8},
    (12, 'a'): {3: 3}, (12, 'b'): {6: 1, 1: 3, 3: 6}, (12, 'c'): {3: 8},
    (13, 'a'): {3: 3}, (13, 'b'): {3: 9}, (13, 'c'): {3: 7, 1: 3},
    (14, 'a'): {3: 10}, (14, 'b'): {3: 8, 1: 6}, (14, 'c'): {3: 10},
    (15, 'a'): {2: 13, 4: 1}, (15, 'b'): {2: 6, 3: 6}, (15, 'c'): {2: 13, 1: 4},
}

SCAN_PAGES = {'paper': range(1, 16)}
SELECTION_SCAN = [
    ('paper', 1, 'any five', 'Cover rubric, Section A: whole-question choice; every question is carded.'),
    ('paper', 1, 'any two', 'Cover rubric, Section B: whole-question choice; every question is carded.'),
    ('paper', 1, 'any four', 'Cover rubric, Section C: whole-question choice; every question is carded.'),
    ('paper', 2, 'any five', 'Section A rubric repeated.'),
    ('paper', 2, 'any five', 'Q1 "explain any five of the following terms": best five of (a)-(f); each part is its own '
                             'card on the "2(7) + 3(2)" ladder.'),
    ('paper', 2, 'the following', 'Q1, same lead-in.'),
    ('paper', 2, 'the following', 'Q2(a) "The following biochemical reactions": both reactions asked, one card each.'),
    ('paper', 2, 'or', 'Q2(a)(i) "anabolism or catabolism": the answer options.'),
    ('paper', 2, 'any two', 'Q2(b)(iv) "Give any two functions of minerals": a bounded menu, claim two.'),
    ('paper', 4, 'the following', 'Q4(a) "each of the following pairs of kingdoms": every pair asked, one card each.'),
    ('paper', 4, 'the following', 'Q4(b) "each of the following cases": every case asked, one card each.'),
    ('paper', 4, 'the following', 'Q5 "Indicate whether the following statements": every statement asked, one card '
                                  'per letter.'),
    ('paper', 4, 'or', 'Q5 "true (T) or false (F)": the answer options of each statement.'),
    ('paper', 6, 'any two', 'Section B rubric: whole-question choice; every question is carded.'),
    ('paper', 6, 'the following', 'Q7(b) lead-in: every part asked.'),
    ('paper', 7, 'the following', 'Q8(a) lead-in: every part asked.'),
    ('paper', 7, 'the following', 'Q8(b) lead-in: every part asked.'),
    ('paper', 8, 'the following', 'Q9(b) lead-in: every part asked.'),
    ('paper', 8, 'or', 'Q9(b)(ii)1 "pulse rate or breathing rate": either investigation; marked on the same row.'),
    ('paper', 8, 'or', 'Q9(b)(ii)2 "pulse rate or breathing rate": either; marked on the same menu.'),
    ('paper', 9, 'any four', 'Section C rubric: whole-question choice; every question is carded.'),
    ('paper', 10, 'the following', 'Q11(b) lead-in: every part asked.'),
    ('paper', 10, 'the following', 'Q11(c) "Read the following extract": every part asked.'),
    ('paper', 10, 'or', 'Q11(c)(ii) "a single gene or by many genes": the answer options.'),
    ('paper', 11, 'the following', 'Q12(c) lead-in: every part asked.'),
    ('paper', 12, 'or', 'Q13(b)(ii) "plant or animal cells": description.'),
    ('paper', 13, 'any two', 'Q14 "any two of (a), (b), (c)": whole-part choice; every part is carded.'),
    ('paper', 13, 'the following', 'Q14(b)(i) "each of the following: dermal tissue, ground tissue, vascular tissue": '
                                   'every tissue located; the scheme prices the labels "3(1)".'),
    ('paper', 13, 'any two', 'Q14(c)(iv) "any two processes": a bounded menu, claim two.'),
    ('paper', 14, 'any two', 'Q15 "any two of (a), (b), (c)": whole-part choice; every part is carded.'),
    ('paper', 14, 'or', 'Q15(b) passage "washed or blown away": description.'),
]

ROUTES = {}

SEC = 'State Examinations Commission'
NO_REPRINT = 'The scheme prints no reprint of any question: anchored on the part\'s own marker.'
ITEM_ROMAN = ('The scheme prints no reprint: a numbered item is anchored on the roman it is printed under.')
WELDED = ('The scheme prints no reprint and sets this part\'s marker on its answer\'s own line: anchored on that '
          'marker.')
ITEM_WELDED = ('The scheme prints no reprint: a numbered item is anchored on the roman it is printed under, which '
               'opens its answer\'s own line.')
TERM = 'The scheme prints the term over its definition: anchored on the term.'
Q5_KEY = ('The scheme prints Q5\'s key as a box of seven cells under "5. 8 + 7 + 5(1)", one per statement in the '
          'order (a)-(g), with no part markers and no reprint: anchored on the statement\'s own cell, the n-th '
          'of its letter in that box.')
EACH_ITEM = 'A numbered list the scheme prices entry by entry: one card per entry.'
NO_ANSWER = 'The scheme prints no answer here, only what earns the marks.'
ROW_PRICED = 'Sections B and C print a mark against every row.'
COLUMN = ('The text layer interleaves this answer\'s lines with Q5\'s key printed beside them; the answer is read '
          'from its own column by glyph position.')


def ask(page, sentence, **kw):
    """A one-line ask closed by its own punctuation."""
    return Q(page, sentence, sentence, **kw)


def term(page, word, br=False):
    """A printed term the paper sets before its answer line ("Niche. ____")."""
    return Q(page, word, word, br=br)


def item(page, n, end, anchor):
    """One entry of a printed numbered list."""
    return Q(page, f'{n}.', end, after=anchor, br=True)


def at(page, *path_and_marker, nth=1, why=NO_REPRINT):
    """The part's own marker, walked down to through the scheme's numbering."""
    *path, marker = path_and_marker
    return SQ(page, marker, path=path, paired=why, bare=True, nth=nth)


def welded(page, *path_and_marker, nth=1, why=WELDED):
    """The part's marker opening its own answer line ("(a) C = Lymph vessel"):
    a welded bare anchor."""
    *path, marker = path_and_marker
    return SQ(page, marker, path=path, paired=why, bare=True, nth=nth, welded=True)


def pieces(sel_start, sel_end=None, n=2, **kw):
    """Each answer of a printed solidus list, in order: one selector per entry."""
    return [dict(S(sel_start, sel_end, piece=i, **kw)) for i in range(1, n + 1)]


def lead(spec, words):
    """A row whose lifted note is the scheme's own tariff notation, led by a direction."""
    return dict(spec, note_lead=words)


def ladder(q, notation):
    return f'The scheme prints Q{q} as "{notation}": an ordered split, each response carded at its first rate.'


def col(page, clip, expect, marks, kind='alt'):
    """An answer read from its own column by glyph position."""
    return G('tokens', page=page, clip=clip, expect=expect, marks=marks, row_kind=kind)


# ------------------------------------------------------------ question text --
Q1 = Q(2, 'From your knowledge of ecology explain any five of the following terms:')
Q2A = Q(2, 'The following biochemical reactions took place in some living cells:')
Q2BII = ask(2, 'Name a fat-soluble vitamin.')
Q3 = ask(3, 'The diagram shows a region of tissue that includes body cells and parts of the circulatory and '
            'lymphatic systems.')
Q4A = [Q(4, 'The living world may be divided into five kingdoms: Monera; Protista; Fungi; Plantae; Animalia.'),
       Q(4, 'In the case of each of the following pairs of kingdoms give any structural feature of members of the',
         'first-named kingdom not found in members of the second kingdom.')]
Q4B = Q(4, 'In each of the following cases, name an organism that fits the description.')
Q5 = Q(4, 'Indicate whether the following statements are true (T) or false (F) by placing a tick (✓) in the appropriate',
       'box in each case.')
Q6D = Q(5, 'What is the name of the two-carbon compound into which pyruvate is broken down under', 'aerobic conditions?')
Q7B = ask(6, 'Answer the following questions on seed germination.')
Q7BI = Q(6, 'At the start of the investigation to show digestive activity during germination the seeds were',
         'sterilised.')
Q7BII = ask(6, 'Name the substance that is used as a medium on which to germinate the seeds.')
Q8A = ask(7, 'Answer the following questions with reference to the microscope.')
Q8B = Q(7, 'Answer the following questions in relation to the procedures that you followed when preparing',
        'animal cells for examination with a light microscope.')
Q9B = ask(8, 'Answer the following in relation to investigations that you carried out in the laboratory.')
Q9BI1 = item(8, 1, 'valve?', 'carried out in the laboratory.')
Q9BII1 = item(8, 1, 'rate what did you first establish?', 'Where did you find the semilunar valves')
Q10B = Q(9, 'Last year it was discovered, by DNA analysis, that meat products labelled as beef contained',
         'meat from other animals, particularly horses and pigs.')
Q10BI = ask(9, 'Name the biomolecule that is the major component of meat.')
Q10BIV = Q(9, 'Name and outline the procedure used for analysing the DNA samples that revealed the',
           'presence of horse meat in products labelled as beef.')
Q10C = Q(9, 'The diagram shows part of the genotype of an individual of the Aberdeen Angus cattle breed.',
         'the horned condition.')
Q11B = ask(10, 'Answer the following questions in relation to the human nervous system.')
Q11BI = Q(10, 'Name the type of particle whose movement in and out of neurons is an essential feature of',
          'nerve impulse transmission.')
Q11C = [ask(10, 'Read the following extract and then answer the questions below.'),
        Q(10, 'Alzheimer’s disease (a degenerative brain condition), like many other degenerative illnesses, is',
          'very molecules that give rise to the disease.'),
        Q(10, '(Adapted from Alzheimer’s Unlocked, TIME, Volume 176, No. 17. 2010.)')]
Q12AI = Q(11, 'Name the structures found in stems, equivalent to stomata in leaves, which are involved in gaseous',
          'exchange in plants.')
Q12C = ask(11, 'Answer the following questions in relation to carbon dioxide.')
Q12CIII = Q(11, 'Carbon dioxide levels are usually higher in venous blood than in arterial blood.', 'Why is this the case?')
Q13A = ask(12, 'Study the graphs of enzyme activity below and answer the questions that follow.')
Q13BIII = Q(12, 'Some biological washing powders contain enzymes similar to the ones found in our digestive',
            'Many of these enzymes are extracted from bacteria.')
Q13C = Q(12, 'In the course of your practical studies you immobilised an enzyme and then investigated its activity.',
         'You also prepared alcohol using yeast.')
Q14AI = [Q(13, 'Name:'), Q(13, '1.', 'the site of production of a pollen grain and', after='Name:', br=True),
         Q(13, '2.', 'the structure on which it must land to complete pollination.', after='Name:', br=True)]
Q14BI = Q(13, 'Draw a diagram of a transverse section through a young dicotyledonous stem as seen under',
          'following: dermal tissue, ground tissue, vascular tissue.')
Q14BII1 = item(13, 1, 'in a young root?', 'vascular tissue.')
Q14BIII = ask(13, 'Draw labelled diagrams to show the detailed structure of the two vascular tissues of plants.')
Q14CI = ask(13, 'Explain how water enters root hairs and then passes to the vascular tissue.')
Q14CII = ask(13, 'In which of the vascular tissues will water now rise through the plant?')
Q15A = Q(14, 'Phytoplankton is the collective term covering the small photosynthetic organisms which are part of',
         'in temperature, light and nutrient levels.')
Q15B = [ask(14, 'Read the passage below and answer the questions that follow.'),
        Q(14, 'European rabbits were introduced by settlers into Australia in 1859.',
          'this solution was not long-lasting and rabbit numbers recovered.')]
Q15C = ask(15, 'The graph shows the growth in human population from 1 AD to present times.')

# Q4(a)'s answers read from their own column (x 130-460 points, page 6), clear
# of Q5's key printed beside them.
Q4_COL = {
    'i': ((130, 95, 460, 140), 'Cell wall or hypha (or named hypha) or mycelium or named reproductive structure'),
    'iii': ((130, 165, 460, 232), 'Nucleus or mitochondrion or multicellular or eukaryotic or nervous system or '
                                  'digestive system or reproductive system or muscular system'),
    'iv': ((130, 234, 460, 278), '(Can be) unicellular or (can have) chloroplast or pseudopodia or contractile '
                                 'vacuole or food vacuole'),
}
# Q5's key: (statement, the n-th of its letter in the box, the cell's rows in
# points on page 6 (x 515-540), the letter printed there, concept).
TF = [('a', 'Single-celled organisms use meiosis for asexual reproduction.', 1, (95, 117), 'F',
       'asexual-reproduction-by-mitosis'),
      ('b', 'In telophase of mitosis, a cleavage furrow forms in plant cells.', 2, (119, 140), 'F', 'cell-plate'),
      ('c', 'When a cell is not dividing it is said to be in prophase.', 3, (142, 164), 'F', 'interphase'),
      ('d', 'The nuclear membrane disappears in the early part of mitosis.', 1, (165, 187), 'T',
       'nuclear-membrane-in-mitosis'),
      ('e', 'Centromeres give rise to the nuclear spindle.', 4, (188, 210), 'F', 'spindle-formation'),
      ('f', 'Mitosis is a source of variation.', 5, (211, 233), 'F', 'mitosis-and-variation'),
      ('g', 'In multicellular organisms mitosis is primarily used for growth.', 2, (234, 257), 'T',
       'mitosis-for-growth')]

MICROSCOPE_A = [L('A', S('Coarse focus or focus with low power', page=7), True)]
ELBOW_A = [L('A', S('*Tendon', page=10), True)]

# Q15(c)(ii): the scheme's three reasons, separated by its own solidus; the
# third line opens with a connector, "/ or improved medicine or improved hygiene".
Q15CII_LIST = ('Better nutrition or better food distribution or better farming', 'or improved medicine or improved hygiene')

TASKS = [
    # ------------------------------------------------------------ Section A --
    # "Niche." alone is below the build's eight-character floor, so that card
    # carries Q1's printed lead-in in its question text instead of its stem.
    T(f'1{x}', f'Q1({x})', 'A', [Q1, term(2, word, br=True)] if len(word) < 8 else term(2, word), [pt(S(ans), 7)],
      'bio-3-1', concept, SQ(5, label, paired=TERM), 7, stem=[] if len(word) < 8 else [Q1],
      decision=ladder(1, '2(7) + 3(2) i.e. best five answers from (a) – (f)') + ' Six parts, the best five priced.')
    for x, word, label, ans, concept in [
        ('a', 'Biosphere.', 'Biosphere', 'Parts of the earth where life (or organisms) exists', 'biosphere'),
        ('b', 'Niche.', 'Niche', 'The (functional) role of an organism or a role explained', 'niche'),
        ('c', 'Biotic factor.', 'Biotic factor', 'A living factor (in an ecosystem)', 'biotic-factor'),
        ('d', 'Trophic level.', 'Trophic level', 'Feeding level or energy level or position in food chain',
         'trophic-level'),
        ('e', 'Competition.', 'Competition', 'The struggle for a resource (or named resource)', 'competition'),
        ('f', 'Symbiosis.', 'Symbiosis', 'Relationship between two species involving benefit.', 'symbiosis')]
] + [
    T('2ai', 'Q2(a)(i)', 'A', ask(2, 'Is this an example of anabolism or catabolism?'), [pt(S('Catabolism'), 7)],
      'bio-1-2', 'catabolism', at(5, '2.', '(a)', '(i)'), 7, stem=[Q2A], fig='q2ai-reaction',
      decision=ladder(2, '7 + 6 + 7(1)') + ' Nine responses. The paper prints the reaction with a drawn arrow, '
               'which the text layer drops; the printed reaction is the figure.'),
    T('2aii', 'Q2(a)(ii)', 'A', ask(2, 'Identify X and Y.'),
      [pt(s, 7) for s in pieces('X = lipase, Y = glycerol', psep=', ')], 'bio-1-2', 'digesting-fat',
      at(5, '2.', '(a)', '(ii)'), 14, stem=[Q2A], fig='q2aii-reaction',
      decision='X and Y are two responses on the "7 + 6 + 7(1)" ladder, cut at the scheme\'s own comma. The paper '
               'prints X over the reaction\'s drawn arrow; the printed reaction is the figure.'),
    T('2bi', 'Q2(b)(i)', 'A', ask(2, 'How does a phospholipid differ from a fat?'),
      [pt(S('(A phospholipid) has a phosphate or (a phospholipid) has two fatty acids'), 7),
       pt(S('(A fat) has three fatty acids'), 7)], 'bio-1-2', 'phospholipids', at(5, '2.', '(b)', '(i)'), 14,
      decision='The phospholipid and the fat are two responses on the "7 + 6 + 7(1)" ladder, as the paper\'s two '
               'answer lines ("Phospholipid:", "Fat:") ask.'),
    T('2bii', 'Q2(b)(ii)', 'A', Q2BII, [pt(S('A, D, E, or K'), 7)], 'bio-1-2', 'fat-soluble-vitamins',
      at(5, '2.', '(b)', '(ii)'), 7, decision=ladder(2, '7 + 6 + 7(1)') + ' Nine responses.'),
    T('2biii', 'Q2(b)(iii)', 'A', ask(2, 'State a disorder due to a dietary deficiency of the vitamin referred to in (b) (ii).'),
      [pt(S('Matching disorder'), 7, kind='criterion', note=NO_ANSWER)], 'bio-1-2', 'vitamin-deficiency',
      at(5, '2.', '(b)', '(iii)'), 7, stem=[M('(ii)', 2), Q2BII],
      decision=ladder(2, '7 + 6 + 7(1)') + ' Nine responses.'),
    T('2biv', 'Q2(b)(iv)', 'A', ask(2, 'Give any two functions of minerals in organisms.'),
      [anyn(S('Formation of rigid structure (or named) /', 'mineral(s)'), 2, 7, open_list=True)], 'bio-1-2',
      'functions-of-minerals', at(5, '2.', '(b)', '(iv)'), 14,
      decision='Two responses on the "7 + 6 + 7(1)" ladder. The menu closes on "any other specific function(s) of '
               'named mineral(s)", so it is open.'),
] + [
    T(f'3{x}', f'Q3({x})', 'A', q, rows, 'bio-2-6', concept, welded(5, '3.', f'({x})'), total, stem=[Q3],
      fig='q3-tissue', labels=labels, decision=ladder(3, '8 + 7 + 5(1)') + ' Seven responses.' + extra)
    for x, q, rows, concept, total, labels, extra in [
        ('a', ask(3, 'Name part C.'), [pt(S('C = Lymph vessel'), 8)], 'lymph-vessel', 8,
         [L('C', S('C = Lymph vessel', page=5, piece=2, psep=' = '), True)], ''),
        ('b', Q(3, 'What type of blood vessel is A?', piece=1, psep='_'), [pt(S('Arteriole [accept artery]'), 8)],
         'arteriole', 8, [L('A', S('Arteriole [accept artery]', page=5), True)],
         ' The paper prints the answer line straight after the ask\'s question mark; the ask is cut there.'),
        ('c', Q(3, 'If a transverse section of A were viewed under the microscope state one way in which it would',
              'differ from a transverse section through B.'),
         [pt(S('Narrow(er) lumen or thick(er) wall or no valves'), 8)], 'arteries-and-veins', 8, None, ''),
        ('d', ask(3, 'Give two functions of the lymphatic system.'),
         [anyn(S('Maintains a constant level of ECF', 'transport of named material'), 2, 8)], 'lymphatic-system', 16,
         None, ' The two functions are two responses.'),
        ('e', ask(3, 'Give one way in which lymph differs from blood.'),
         [anyn(S('No red blood cells or no haemoglobin', 'higher fat level [accept correct colour difference]'), 1, 8)],
         'lymph-and-blood', 8, None, ''),
        ('f', ask(3, 'Name a major blood vessel that returns the blood in B to the heart.'), [pt(S('Vena cava'), 8)],
         'vena-cava', 8, None, '')]
] + [
    T(f'4a{r}', f'Q4(a)({r})', 'A', term(4, pair), rows, 'bio-3-2', concept, sq, 8, stem=Q4A,
      decision=ladder(4, '8 + 7 + 5(1)') + ' Seven responses.' + extra)
    for r, pair, rows, concept, sq, extra in [
        ('i', 'Fungi and Animalia.', [col(6, *Q4_COL['i'], 8)], 'fungi-and-animals', at(6, '4.', '(a)', '(i)'),
         ' ' + COLUMN),
        ('ii', 'Plantae and Fungi.', [pt(S('Chloroplast or cellulose cell wall or named anatomical feature'), 8)],
         'plants-and-fungi', welded(6, '4.', '(a)', '(ii)'), ''),
        ('iii', 'Animalia and Monera.', [col(6, *Q4_COL['iii'], 8)], 'animals-and-bacteria',
         welded(6, '4.', '(a)', '(iii)'), ' ' + COLUMN),
        ('iv', 'Protista and Animalia.', [col(6, *Q4_COL['iv'], 8)], 'protists-and-animals',
         welded(6, '4.', '(a)', '(iv)'), ' ' + COLUMN)]
] + [
    T('4bi', 'Q4(b)(i)', 'A', term(4, 'A multicellular fungus.'),
      [pt(S('Rhizopus (or bread mould) or other named fungus'), 8)], 'bio-3-2', 'multicellular-fungus',
      at(6, '4.', '(b)', '(i)'), 8, stem=[Q4B], decision=ladder(4, '8 + 7 + 5(1)') + ' Seven responses.'),
    T('4bii', 'Q4(b)(ii)', 'A', ask(4, 'A member of the Protista that catches and consumes smaller organisms.'),
      [pt(S('Amoeba'), 8)], 'bio-3-2', 'amoeba', at(6, '4.', '(b)', '(ii)'), 8, stem=[Q4B],
      decision=ladder(4, '8 + 7 + 5(1)') + ' Seven responses.'),
    T('4biii', 'Q4(b)(iii)', 'A', term(4, 'A harmful member of the Monera.'),
      [pt(S('Any named (harmful) bacterium', 'or named (harmful) effect of a bacterium'), 8, kind='criterion',
          note_sel=S('[NB The word ‘bacterium’ is essential if effect given]'), note=NO_ANSWER)],
      'bio-3-2', 'harmful-bacteria', welded(6, '4.', '(b)', '(iii)'), 8, stem=[Q4B],
      decision=ladder(4, '8 + 7 + 5(1)') + ' Seven responses.'),
] + [
    T(f'5{x}', f'Q5({x})', 'A', ask(4, statement),
      [G('tokens', page=6, clip=(515, y[0], 540, y[1]), expect=answer, marks=8)], 'bio-2-3', concept,
      SQ(6, answer, answer, nth=nth, path=['5. 8 + 7 + 5(1)'], paired=Q5_KEY), 8, stem=[Q5],
      decision=ladder(5, '8 + 7 + 5(1)') + ' Seven responses. The scheme prints the answer as the letter ' + answer
      + f' in row ({x}) of its key box, read from that cell.')
    for x, statement, nth, y, answer, concept in TF
] + [
    T('6a', 'Q6(a)', 'A', ask(5, 'Suggest an advantage of using ATP as an energy store in cells.'),
      [pt(S('High-energy molecule (or bond) or easily broken down or easily re-formed or reusable',
            'or energy easily released'), 8)], 'bio-2-2', 'atp-as-energy-store', at(6, '6.', '(a)'), 8,
      decision=ladder(6, '8 + 7 + 5(1)') + ' Seven responses.'),
    T('6b', 'Q6(b)', 'A', ask(5, 'Name two processes requiring ATP that occur in cells.'),
      [anyn(None, 2, 8, open_list=True,
            options=[S('Any two named cell processes', piece=[1, 2], psep=[', ', 'e.g. ']),
                     S('Any two named cell processes', piece=2, psep=', '),
                     S('Any two named cell processes', piece=3, psep=', '),
                     S('mitosis (or named phase of mitosis)')],
            note_sel=S('Any two named cell processes', piece=[1, 1], psep=[', ', ' e.g. ']))],
      'bio-2-2', 'processes-needing-atp', at(6, '6.', '(b)'), 16,
      decision='Two responses on the "8 + 7 + 5(1)" ladder. The scheme prints "Any two named cell processes e.g." '
               'and four examples, the first three cut at its commas and the fourth on its own printed line: an '
               'open menu.'),
    T('6c', 'Q6(c)', 'A', Q(5, 'Name two substances, other than carbon dioxide, into which pyruvate may be broken down',
                            'under anaerobic conditions in cells.'),
      [pt(S('Lactic Acid'), 8), pt(S('Ethanol [accept alcohol]'), 8)], 'bio-2-2', 'anaerobic-products',
      at(6, '6.', '(c)'), 16, decision='The two substances, numbered 1. and 2. by the scheme, are two responses on '
                                       'the "8 + 7 + 5(1)" ladder.'),
    T('6d', 'Q6(d)', 'A', Q6D, [pt(S('Acetyl (Co-enzyme A)'), 8)], 'bio-2-2', 'acetyl-coenzyme-a', at(6, '6.', '(d)'),
      8, decision=ladder(6, '8 + 7 + 5(1)') + ' Seven responses.'),
    T('6e', 'Q6(e)', 'A', Q(5, 'Briefly describe the fate, under aerobic conditions, of the two-carbon compound referred to in',
                            'part (d).'),
      [pt(S('Enters Krebs Cycle (or explained) or (broken down) to CO2 and H2O'), 8)], 'bio-2-2',
      'fate-of-acetyl-coenzyme-a', at(6, '6.', '(e)'), 8, stem=[M('(d)', 5), Q6D],
      decision=ladder(6, '8 + 7 + 5(1)') + ' Seven responses. The text layer flattens the subscripts of CO2 and H2O.'),
    # ------------------------------------------------------------ Section B --
    T('7ai', 'Q7(a)(i)', 'B', ask(6, 'Name a part of a seed in which food for germination is stored.'),
      [pt(S('*Cotyledon or *endosperm'), 3)], 'bio-2-5', 'food-store-in-seeds', at(7, '7.', '(a)', '(i)'), 3,
      decision=ROW_PRICED),
    T('7aii', 'Q7(a)(ii)', 'B', ask(6, 'Name the three factors necessary for seeds to germinate.'),
      [anyn(S('Water / oxygen / suitable temperature (or warmth)'), 3, 1)], 'bio-2-5',
      'conditions-for-germination', at(7, '7.', '(a)', '(ii)'), 3,
      decision='"3(1)": the three factors, cut at the scheme\'s own solidus into a menu the student claims all '
               'three of. As three separate rows the deck build refused the third, "suitable temperature (or '
               'warmth)", whose wording matches its content-free pattern for method prose ("suitable '
               'temperature"); here it is the printed answer. Coordinator\'s reviewer pass.'),
] + [
    T(f'7bi{n}', f'Q7(b)(i){n}', 'B', item(6, n, end, 'sterilised.'), [pt(S(ans), 3)], 'bio-2-5', concept,
      at(7, '7.', '(b)', '(i)', why=ITEM_ROMAN), 3, stem=[Q7B, Q7BI], decision=EACH_ITEM)
    for n, end, ans, concept in [
        (1, 'Why is this necessary?', 'To kill (or inhibit) any microorganisms (or bacteria and fungi)',
         'why-sterilise-seeds'),
        (2, 'How did you sterilise the seeds?', 'Disinfectant or named disinfectant.', 'sterilising-seeds')]
] + [
    T('7bii', 'Q7(b)(ii)', 'B', Q7BII, [pt(S('Agar'), 3)], 'bio-2-5', 'agar', at(7, '7.', '(b)', '(ii)'), 3,
      stem=[Q7B, Q7BI]),
    T('7biii', 'Q7(b)(iii)', 'B', ask(6, 'What substance, to be digested by the seeds, was added to the above medium?'),
      [pt(S('Starch or milk or protein'), 3)], 'bio-2-5', 'substrate-in-the-agar', welded(7, '7.', '(b)', '(iii)'), 3,
      stem=[Q7B, Q7BI, M('(ii)', 6), Q7BII]),
    T('7biv', 'Q7(b)(iv)', 'B', ask(6, 'What control did you use in this demonstration?'),
      [pt(S('(Same set-up and procedure with) boiled seeds'), 3)], 'bio-2-5', 'boiled-seed-control',
      welded(7, '7.', '(b)', '(iv)'), 3, stem=[Q7B, Q7BI]),
    T('7bv', 'Q7(b)(v)', 'B', ask(6, 'How did you demonstrate that digestive activity had taken place?'),
      [pt(s, 3) for s in pieces('Iodine (or biuret) (solution)', 'starch (or protein)', n=3)], 'bio-2-5',
      'evidence-of-digestion', at(7, '7.', '(b)', '(v)'), 9, stem=[Q7B, Q7BI],
      decision='"3(3)": the three points, each cut at the scheme\'s own solidus.'),
    T('8ai', 'Q8(a)(i)', 'B', ask(7, 'State the function of the part labelled A in the diagram.'),
      [pt(S('Coarse focus or focus with low power'), 3)], 'bio-1-3', 'coarse-focus', at(7, '8.', '(a)', '(i)'), 3,
      stem=[Q8A], fig='q8a-microscope', labels=MICROSCOPE_A,
      decision=ROW_PRICED + ' The scheme names A only by its function; that answer is its key, shown after the '
                            'reveal.'),
    T('8aii', 'Q8(a)(ii)', 'B', Q(7, 'Lens E is marked 10× and lens O is marked 40×.', 'What is the actual diameter of the cell?'),
      [pt(S('0.002 mm'), 3, note_sel=S('3, 2, 1, 0'), note_lead='The scheme marks this answer')], 'bio-1-3',
      'magnification', at(7, '8.', '(a)', '(ii)'), 3, stem=[Q8A], fig='q8a-microscope',
      decision='The answer is one priced item, marked "3, 2, 1, 0".'),
    T('8bi', 'Q8(b)(i)', 'B', ask(7, 'Describe how you obtained a sample of cells.'),
      [pt(S('Rubbed inside cheek with swab (or example)'), 3)], 'bio-1-3', 'sampling-cheek-cells',
      at(7, '8.', '(b)', '(i)'), 3, stem=[Q8B]),
    T('8bii', 'Q8(b)(ii)', 'B', ask(7, 'What stain did you use on the sample?'), [pt(S('Methylene blue'), 3)], 'bio-1-3',
      'methylene-blue', at(7, '8.', '(b)', '(ii)'), 3, stem=[Q8B]),
    T('8biii', 'Q8(b)(iii)', 'B', ask(7, 'Outline how you used the coverslip.'),
      [pt(s, 3) for s in pieces('(Coverslip) at angle / how lowered')], 'bio-1-3', 'lowering-the-coverslip',
      at(7, '8.', '(b)', '(iii)'), 6, stem=[Q8B], decision='"2(3)": the two points, cut at the scheme\'s own solidus.'),
    T('8biv', 'Q8(b)(iv)', 'B', ask(7, 'Explain why a coverslip is used.'),
      [pt(S('To protect the sample from drying out', 'or to protect the lens (from the stain)'), 3)], 'bio-1-3',
      'why-a-coverslip', at(7, '8.', '(b)', '(iv)'), 3, stem=[Q8B]),
    T('8bv', 'Q8(b)(v)', 'B', ask(7, 'Describe how you examined the cells using the microscope.'),
      [pt(S('Focus using coarse (focus) or focus using A', 'or focus using lower power'), 3),
       pt(S('(focus) using medium (or high) power (or using fine focus)'), 3)], 'bio-1-3', 'using-the-microscope',
      welded(7, '8.', '(b)', '(v)'), 6, stem=[Q8B], fig='q8a-microscope', labels=[L('A', S('Coarse focus or focus with low power', page=7), False)],
      decision=ROW_PRICED + ' The first answer names the part labelled A in (a)\'s diagram, so the card shows that '
                            'diagram.'),
    T('8bvi', 'Q8(b)(vi)', 'B', ask(7, 'Draw a labelled diagram of the cells as seen at high magnification.'),
      [pt(S('Appropriate labelled diagram [at least 1 label required]'), 3, kind='criterion', note=NO_ANSWER)],
      'bio-1-3', 'drawing-cheek-cells', at(7, '8.', '(b)', '(vi)'), 3, stem=[Q8B],
      decision='The drawing is one priced item: one criterion row naming what it must show.'),
    T('9ai', 'Q9(a)(i)', 'B', ask(8, 'Give one example of a limitation of the scientific method.'),
      [pt(S('(The extent of) our basic knowledge or the basis of investigation or', 'or accidental discoveries'), 3)],
      'bio-u2', 'limitations-of-scientific-method', at(8, '9.', '(a)', '(i)'), 3, decision=ROW_PRICED),
    T('9aii', 'Q9(a)(ii)', 'B', ask(8, 'Where do scientists usually publish the results and conclusions of their investigations?'),
      [pt(S('Scientific journal(s)'), 3)], 'bio-u2', 'publishing-results', at(8, '9.', '(a)', '(ii)'), 3),
    T('9bi1', 'Q9(b)(i)1', 'B', Q9BI1, [pt(S('Between the right atrium and right ventricle'), 3)], 'bio-2-6',
      'tricuspid-valve', at(8, '9.', '(b)', '(i)', why=ITEM_ROMAN), 3, stem=[Q9B], decision=EACH_ITEM),
    T('9bi2', 'Q9(b)(i)2', 'B', item(8, 2, 'Briefly describe how you carried out the dissection to expose this valve.',
                                    'carried out in the laboratory.'),
      [pt(s, 3) for s in pieces('Cut through the right side of the heart / using a scalpel')], 'bio-2-6',
      'dissecting-the-heart', at(8, '9.', '(b)', '(i)', why=ITEM_ROMAN), 6, stem=[Q9B, Q9BI1],
      decision=EACH_ITEM + ' "2(3)": the two points, cut at the scheme\'s own solidus.'),
    T('9bi3', 'Q9(b)(i)3', 'B', item(8, 3, 'Where did you find the semilunar valves during the dissection?',
                                    'carried out in the laboratory.'),
      [pt(s, 3) for s in pieces('At the base / of the aorta or the pulmonary artery')], 'bio-2-6',
      'semilunar-valves', at(8, '9.', '(b)', '(i)', why=ITEM_ROMAN), 6, stem=[Q9B],
      decision=EACH_ITEM + ' "2(3)": the two points, cut at the scheme\'s own solidus.'),
    T('9bii1', 'Q9(b)(ii)1', 'B', Q9BII1, [pt(S('The resting (pulse) rate or resting (breathing) rate'), 3)], 'bio-2-6',
      'resting-rate', at(8, '9.', '(b)', '(ii)', why=ITEM_ROMAN), 3, stem=[Q9B], decision=EACH_ITEM),
    T('9bii2', 'Q9(b)(ii)2', 'B', item(8, 2, 'How did you measure pulse rate or breathing rate?',
                                      'Where did you find the semilunar valves'),
      [anyn(S('Feel (or locate) pulse (or observe breathing) /', 'Repeat and find average.'), 2, 3)], 'bio-2-6',
      'measuring-pulse-rate', at(8, '9.', '(b)', '(ii)', why=ITEM_ROMAN), 6, stem=[Q9B, Q9BII1],
      decision=EACH_ITEM + ' "2(3)" over three printed points: a menu, claim two.'),
    # ------------------------------------------------------------ Section C --
    T('10ai', 'Q10(a)(i)', 'C', ask(9, 'Explain the term species.'),
      [pt(s, 3) for s in pieces('Interbreeding (population) / producing fertile offspring')], 'bio-1-4', 'species',
      at(9, '10.', '(a)', '(i)'), 6, decision='"2(3)": the two points, cut at the scheme\'s own solidus.'),
    T('10aii', 'Q10(a)(ii)', 'C', ask(9, 'What is meant by the term gene expression?'),
      [pt(S('The production of a (particular) protein (using the gene’s code)'), 3)], 'bio-1-4', 'gene-expression',
      at(9, '10.', '(a)', '(ii)'), 3),
    T('10bi', 'Q10(b)(i)', 'C', Q10BI, [pt(S('*Protein'), 3)], 'bio-1-2', 'protein-in-meat', at(9, '10.', '(b)', '(i)'),
      3, stem=[Q10B]),
    T('10bii', 'Q10(b)(ii)', 'C', ask(9, 'Where in a cell are these biomolecules manufactured?'),
      [pt(S('Ribosomes'), 3)], 'bio-2-3', 'ribosomes', at(9, '10.', '(b)', '(ii)'), 3, stem=[Q10B, M('(i)', 9), Q10BI]),
    T('10biii', 'Q10(b)(iii)', 'C', Q(9, 'Name the molecule, formed from DNA, which carries the instruction to manufacture these',
                                      'biomolecules.'),
      [pt(S('*mRNA'), 3)], 'bio-2-3', 'mrna', welded(9, '10.', '(b)', '(iii)'), 3, stem=[Q10B, M('(i)', 9), Q10BI]),
    T('10biv', 'Q10(b)(iv)', 'C', Q10BIV,
      [pt(S('(DNA) profiling'), 3),
       anyn(S('Cut (DNA into fragments) / with (restriction) enzymes /', 'analyse results (or explained)'), 3, 3)],
      'bio-1-4', 'dna-profiling', at(9, '10.', '(b)', '(iv)'), 12, stem=[Q10B],
      decision='The name "3" and the outline "3(3)", three points from the printed five.'),
    T('10bv', 'Q10(b)(v)', 'C', Q(9, 'Would the result obtained from the procedure referred to in (iv) be the same if the beef were',
                                  'contaminated with pig meat? Explain your answer.'),
      [pt(S('No, because pig DNA is not the same as horse DNA'), 6, note_sel=S('6, 3, 0'),
          note_lead='The scheme marks this answer')], 'bio-1-4', 'dna-profiles-differ', at(9, '10.', '(b)', '(v)'), 6,
      stem=[Q10B, M('(iv)', 9), Q10BIV],
      decision='One priced item, "6, 3, 0", printed as two answers joined by "OR": answer variants of one task.'),
] + [
    T(f'10c{r}', f'Q10(c)({r})', 'C', q, rows, 'bio-1-4', concept, sq, total, stem=[Q10C], fig='q10c-genotype',
      decision=decision)
    for r, q, rows, concept, sq, total, decision in [
        ('i', ask(9, 'What term is used to describe the allele pair Pp?'), [pt(S('*Heterozygous'), 3)],
         'heterozygous', at(9, '10.', '(c)', '(i)'), 3, ROW_PRICED),
        ('ii', ask(9, 'Is this a sex-linked condition? Explain your answer.'),
         [pt(S('No'), 3), pt(S('Because they (‘P’ genes) are not on the X (or Y or sex) chromosome'), 3)],
         'sex-linkage', at(9, '10.', '(c)', '(ii)'), 6, 'The answer and its explanation are priced "3" each.'),
        ('iii', ask(9, 'What is the phenotype and sex of the animal whose partial genotype is shown above?'),
         [pt(S('Hornless (or polled)'), 3), pt(S('Male'), 3)], 'phenotype-and-sex', at(9, '10.', '(c)', '(iii)'), 6,
         'The phenotype and the sex are priced "3" each.'),
        ('iv', Q(9, 'Draw a diagram, similar to the one shown, to describe an Aberdeen Angus which, when',
                 'crossed with the one above, would ensure the production of a polled calf.'),
         [pt(S('PP properly located on chromosome pair'), 3, kind='criterion',
             note_sel=S('[genotype alone gets 3 marks]')),
          pt(S('XX properly labelled as chromosome pair'), 3, kind='criterion')],
         'homozygous-dominant-cow', at(9, '10.', '(c)', '(iv)'), 6,
         'The drawing is priced "3" for the genotype and "3" for the sex chromosomes: two criterion rows.'),
        ('v', Q(9, 'Name a group of organisms in which the XY chromosome pair gives rise to a different sex',
                'than in cattle.'),
         [pt(S('Birds or butterflies or moths'), 3)], 'sex-determination-in-birds', welded(9, '10.', '(c)', '(v)'), 3,
         '')]
] + [
    T('11ai', 'Q11(a)(i)', 'C', ask(10, 'Name the type of joint shown in the diagram.'), [pt(S('*Hinge'), 3)], 'bio-2-4',
      'hinge-joint', at(10, '11.', '(a)', '(i)'), 3, fig='q11a-elbow', decision=ROW_PRICED),
    T('11aii', 'Q11(a)(ii)', 'C', ask(10, 'Name the structure labelled A, which attaches muscle to bone.'),
      [pt(S('*Tendon'), 3)], 'bio-2-4', 'tendon', at(10, '11.', '(a)', '(ii)'), 3, fig='q11a-elbow', labels=ELBOW_A),
    T('11aiii', 'Q11(a)(iii)', 'C', ask(10, 'Explain what is meant by an antagonistic muscle pair.'),
      [pt(S('(A pair of muscles that) work with opposing actions', 'or explained.'), 3)], 'bio-2-4',
      'antagonistic-muscles', welded(10, '11.', '(a)', '(iii)'), 3),
    T('11bi', 'Q11(b)(i)', 'C', Q11BI, [pt(S('*Ion'), 3)], 'bio-2-4', 'ions-in-impulses', at(10, '11.', '(b)', '(i)'), 3,
      stem=[Q11B]),
    T('11bii', 'Q11(b)(ii)', 'C', ask(10, 'Give an account of how neurotransmitters work.'),
      [anyn(S('(Neurotransmitters are) secreted by the neuron /', '(presynaptic neuron)'), 4, 3)], 'bio-2-4',
      'neurotransmitters', at(10, '11.', '(b)', '(ii)'), 12,
      stem=[Q11B, M('(i)', 10), Q11BI,
            ask(10, 'One of the roles of the particles referred to in (i) is the activation of neurotransmitters.')]),
    T('11biii1', 'Q11(b)(iii)1', 'C', item(10, 1, 'in the human brain.', 'how neurotransmitters work.'),
      [pt(S('The cerebellum – hind brain and cerebrum – forebrain'), 3)], 'bio-2-4', 'cerebellum-and-cerebrum',
      at(10, '11.', '(b)', '(iii)', why=ITEM_ROMAN), 3, stem=[Q11B], decision=EACH_ITEM),
    T('11biii2', 'Q11(b)(iii)2', 'C', item(10, 2, 'State three functions of the cerebrum.', 'how neurotransmitters work.'),
      [anyn(S('memory / learning / emotion', 'personality / taste'), 3, 3, note_sel=S('Any three functions:'))],
      'bio-2-4', 'functions-of-the-cerebrum', at(10, '11.', '(b)', '(iii)', why=ITEM_ROMAN), 9, stem=[Q11B],
      decision=EACH_ITEM),
] + [
    T(f'11c{r}', f'Q11(c)({r})', 'C', q, rows, 'bio-2-4', concept, sq, total, stem=Q11C, decision=decision)
    for r, q, rows, concept, sq, total, decision in [
        ('i', ask(10, 'What do you think is meant by the term “degenerative illnesses”?'), [pt(S('Getting worse'), 3)],
         'degenerative-illness', at(10, '11.', '(c)', '(i)'), 3, ''),
        ('ii', ask(10, 'Is Alzheimer’s disease driven by a single gene or by many genes?'), [pt(S('Many (or group)'), 3)],
         'alzheimers-genes', at(10, '11.', '(c)', '(ii)'), 3, ''),
        ('iii', ask(10, 'What is thought to cause the disease?'), [pt(S('A build up of protein plaques'), 3)],
         'alzheimers-cause', at(10, '11.', '(c)', '(iii)'), 3, ''),
        ('iv', ask(10, 'Suggest a possible symptom of Alzheimer’ disease.'), [pt(S('e.g. memory loss'), 3)],
         'alzheimers-symptom', at(10, '11.', '(c)', '(iv)'), 3,
         'The scheme prints one example ("e.g. memory loss"); the ask is the paper\'s, its missing "s" included.'),
        ('v', ask(10, 'How is the advance of technology helping in the fight against the disease?'),
         [pt(S('Scans can examine the brain (for early detection)'), 3)], 'brain-scans', at(10, '11.', '(c)', '(v)'), 3,
         ''),
        ('vi', Q(10, 'There are probably more people suffering from the disease now than ever before.',
                 'Suggest a reason for this.'),
         [pt(S('Larger population or more people living into old age'), 3)], 'ageing-population',
         at(10, '11.', '(c)', '(vi)'), 3, ''),
        ('vii', ask(10, 'Name another disorder of the nervous system and give a possible treatment for it.'),
         [pt(s, 3, kind='criterion', note=NO_ANSWER) for s in pieces('Name / treatment')], 'nervous-system-disorder',
         welded(10, '11.', '(c)', '(vii)'), 6,
         'The scheme prices "Name / treatment" "2(3)" and prints neither: two criterion rows, cut at its solidus.')]
] + [
    T('12ai', 'Q12(a)(i)', 'C', Q12AI, [pt(S('*Lenticels'), 3)], 'bio-2-6', 'lenticels', at(11, '12.', '(a)', '(i)'), 3,
      decision=ROW_PRICED),
    T('12aii', 'Q12(a)(ii)', 'C', ask(11, 'Name two compounds that leave the plant through the structures referred to in part (i).'),
      [pt(s, 3) for s in pieces('Water / carbon dioxide')], 'bio-2-6', 'gases-through-lenticels',
      at(11, '12.', '(a)', '(ii)'), 6, stem=[M('(i)', 11), Q12AI],
      decision='"2(3)": the two compounds, cut at the scheme\'s own solidus.'),
    T('12bi', 'Q12(b)(i)', 'C', ask(11, 'Draw a large labelled diagram of the human breathing tract.'),
      [pt(S('Diagram showing: trachea, bronchus and bronchioles'), 6, kind='criterion', note_sel=S('6, 3, 0'),
          note_lead='The scheme marks this diagram'),
       anyn(S('Labels: trachea / cartilage / bronchi / bronchioles / alveoli', piece=2, psep=': '), 3, 1)],
      'bio-2-6', 'drawing-the-breathing-tract', at(11, '12.', '(b)', '(i)'), 9,
      decision='The drawing is one priced item ("6, 3, 0") and its labels "3(1)", three from the printed five.'),
    T('12bii', 'Q12(b)(ii)', 'C', ask(11, 'Outline the details of the process of inhalation.'),
      [anyn(S('Brain sends message to muscles /', 'pressure drops / air in'), 6, 3)], 'bio-2-6', 'inhalation',
      at(11, '12.', '(b)', '(ii)'), 18),
    T('12ci', 'Q12(c)(i)', 'C', ask(11, 'Name a structure found in cells in which carbon dioxide is produced.'),
      [pt(S('*Mitochondrion'), 3)], 'bio-2-2', 'mitochondrion', at(11, '12.', '(c)', '(i)'), 3, stem=[Q12C]),
    T('12cii', 'Q12(c)(ii)', 'C', ask(11, 'Give a feature of a capillary which allows the rapid uptake of carbon dioxide.'),
      [pt(S('Wall one cell thick or thin wall'), 3)], 'bio-2-6', 'capillary-wall', at(11, '12.', '(c)', '(ii)'), 3,
      stem=[Q12C]),
    T('12ciii', 'Q12(c)(iii)', 'C', Q12CIII,
      [anyn(S('Venous blood has collected CO2 /', 'blood has been cleared of CO2 (in lungs)'), 2, 3)], 'bio-2-6',
      'carbon-dioxide-in-venous-blood', at(11, '12.', '(c)', '(iii)'), 6, stem=[Q12C]),
    T('12civ', 'Q12(c)(iv)', 'C', Q(11, 'Name a blood vessel which is an exception to the situation outlined in (iii) above.',
                                    'Give a reason for the exception.'),
      [pt(S('Pulmonary Vein'), 3), col(11, (140, 498, 300, 550), 'Blood has been cleared of CO2 in the lungs', 3,
                                       kind='point')],
      'bio-2-6', 'pulmonary-vessels', at(11, '12.', '(c)', '(iv)'), 6, stem=[Q12C, M('(iii)', 11), Q12CIII],
      decision='The vessel and its reason are priced "3" each. The scheme prints two sets side by side joined by '
               '"OR" (pulmonary vein, or pulmonary artery, each with its reason): answer variants of one task, each '
               'reason read from its own column by glyph position.'),
    T('12cv', 'Q12(c)(v)', 'C', ask(11, 'Briefly outline the role of carbon dioxide in the control of the human breathing rate.'),
      [pt(S('Medulla oblongata registers blood CO2 levels'), 3),
       pt(S('More CO2 results in faster (breathing)', 'or less CO2 results in slower (breathing)'), 3)], 'bio-2-6',
      'carbon-dioxide-and-breathing-rate', at(11, '12.', '(c)', '(v)'), 6, stem=[Q12C]),
    T('13ai', 'Q13(a)(i)', 'C', Q(12, 'In the case of each graph state the relationship between the rate of reaction (y-axis) and another',
                                  'factor (x-axis).'),
      [pt(S('(Rate of reaction) decreases as x-axis (or other) factor increases'), 3, label=S('Graph A:')),
       pt(S('(Rate of reaction) increases and (then) decreases as x-axis (or other)', 'factor increases'), 3,
          label=S('Graph B:'))], 'bio-2-1', 'reading-enzyme-graphs', at(12, '13.', '(a)', '(i)'), 6, stem=[Q13A],
      fig='q13a-graphs', decision=ROW_PRICED),
    T('13aii', 'Q13(a)(ii)', 'C', Q(12, 'In the case of graph B, what factor could be responsible for the changes in activity of the',
                                    'enzyme?'),
      [pt(S('pH or temperature'), 3)], 'bio-2-1', 'factors-affecting-enzymes', at(12, '13.', '(a)', '(ii)'), 3,
      stem=[Q13A], fig='q13a-graphs'),
    T('13bi', 'Q13(b)(i)', 'C', ask(12, 'Give a detailed account of how enzymes work, referring in your answer to their specificity.'),
      [anyn(S('(Enzymes have) active site(s) / induced fit (or explained) /', 'enzyme unchanged (or can be reused)'),
            4, 3)], 'bio-2-1', 'how-enzymes-work', at(12, '13.', '(b)', '(i)'), 12),
    T('13bii', 'Q13(b)(ii)', 'C', ask(12, 'Name two processes that occur in plant or animal cells that require the use of enzymes.'),
      [pt(S('Any two named cellular processes'), 6, kind='criterion', units=[3, 3], note=NO_ANSWER)], 'bio-2-1',
      'processes-needing-enzymes', at(12, '13.', '(b)', '(ii)'), 6,
      decision='The scheme prices "Any two named cellular processes" "2(3)" and names none: one criterion row worth '
               'its two 3s.'),
] + [
    T(f'13biii{n}', f'Q13(b)(iii){n}', 'C', item(12, n, end, 'extracted from bacteria.'), [pt(S(ans), 3)], 'bio-2-1',
      concept, at(12, '13.', '(b)', '(iii)', why=ITEM_ROMAN), 3, stem=[Q13BIII], decision=EACH_ITEM)
    for n, end, ans, concept in [
        (1, 'Suggest why such enzymes are included in washing powder.',
         'To break down food-based (or other biological) stains', 'enzymes-in-washing-powder'),
        (2, 'Why is 40 °C the recommended temperature for these washing powders?', 'Optimum (temperature) or explained',
         'optimum-temperature'),
        (3, 'Suggest what would happen to these enzymes in an 80 °C wash.', 'Denaturation or explained',
         'denaturation')]
] + [
    T('13ci', 'Q13(c)(i)', 'C', ask(12, 'Draw a labelled diagram of the apparatus you used to prepare alcohol.'),
      [pt(S('Diagram: flask + contents + indication of air exclusion'), 3, kind='criterion'),
       anyn(S('glucose (solution) / yeast / fermentation (or air) lock', 'or oil layer or anaerobic conditions'), 3, 1,
            note_sel=S('Labels:'))],
      'bio-2-2', 'alcohol-apparatus', at(12, '13.', '(c)', '(i)'), 6, stem=[Q13C],
      decision='The drawing is one priced item ("3") and its labels "3(1)".'),
    T('13cii', 'Q13(c)(ii)', 'C', ask(12, 'Give two advantages of using immobilised yeast cells in the production of alcohol.'),
      [anyn(S('Can be reused / are easy to extract from the solution / pure product'), 2, 3)], 'bio-2-1',
      'immobilised-cells', at(12, '13.', '(c)', '(ii)'), 6, stem=[Q13C]),
    T('13ciii', 'Q13(c)(iii)', 'C', ask(12, 'How did you test for the presence of alcohol?'),
      [anyn(S('Iodoform test / sodium hypochlorite / potassium iodide /', 'heat or warm / yellow (crystals)'), 4, 3)],
      'bio-2-2', 'testing-for-alcohol', at(12, '13.', '(c)', '(iii)'), 12, stem=[Q13C],
      decision='"4(3)" over either test the scheme prints, joined by "OR" (iodoform or dichromate): answer variants '
               'of one task, four points from the test\'s five.'),
    T('14ai', 'Q14(a)(i)', 'C', Q14AI, [pt(S('Anther [accept stamen]'), 3), pt(S('*Stigma'), 3)], 'bio-2-5',
      'anther-and-stigma', at(13, '14.', '(a)', '(i)'), 6,
      decision='The paper asks both names in one sentence ("Name: 1. ... and 2. ..."); the scheme prices each "3": '
               'two rows on one card.'),
    T('14aii', 'Q14(a)(ii)', 'C', ask(13, 'Name two methods of cross pollination.'),
      [anyn(S('Wind / animal (or example) / water'), 2, 3)], 'bio-2-5', 'cross-pollination',
      at(13, '14.', '(a)', '(ii)'), 6),
    T('14aiii', 'Q14(a)(iii)', 'C', Q(13, 'Many species of plant have mechanisms that prevent self-pollination.',
                                      'Suggest how such plants could benefit from this.'),
      [pt(S('Greater variation or explained or prevents inbreeding or explained'), 3)], 'bio-2-5',
      'avoiding-self-pollination', at(13, '14.', '(a)', '(iii)'), 3),
    T('14aiv', 'Q14(a)(iv)', 'C', Q(13, 'Describe in detail the events that follow the arrival of a pollen grain at the destination referred',
                                    'to in (i), up to and including fertilisation.'),
      [anyn(S('Pollen (grain) germinates or pollen tube produced / grows through', 'one fertilises the polar nuclei.'),
            4, 3)], 'bio-2-5', 'fertilisation-in-flowers', at(13, '14.', '(a)', '(iv)'), 12,
      stem=[M('(i)', 13)] + Q14AI),
    T('14av', 'Q14(a)(v)', 'C', ask(13, 'Which part of a flower usually develops into a fruit?'), [pt(S('*Ovary'), 3)],
      'bio-2-5', 'ovary-to-fruit', at(13, '14.', '(a)', '(v)'), 3),
    T('14bi', 'Q14(b)(i)', 'C', Q14BI,
      [pt(S('Diagram:'), 3, kind='criterion', note=NO_ANSWER),
       pt(S('Labels correctly located:'), 3, kind='criterion', units=[1, 1, 1], note=NO_ANSWER)],
      'bio-2-6', 'drawing-a-stem-section', at(13, '14.', '(b)', '(i)'), 6,
      decision='The scheme prices the drawing "3, 0" and the three tissues\' locations "3(1)", and prints neither '
               'what the drawing shows nor the labels: two criterion rows, the second worth its three 1s.'),
] + [
    T(f'14bii{n}', f'Q14(b)(ii){n}', 'C', q, [pt(S(ans), 3)], 'bio-2-6', concept,
      at(13, '14.', '(b)', '(ii)', why=ITEM_ROMAN), 3, stem=stem, decision=EACH_ITEM)
    for n, q, ans, concept, stem in [
        (1, Q14BII1, '*Vascular', 'vascular-tissue-in-roots', [Q14BI]),
        (2, item(13, 2, 'found in the root?', 'vascular tissue.'), 'In the centre', 'root-vascular-tissue',
         [Q14BI, Q14BII1]),
        (3, item(13, 3, 'Give one function of ground tissue.', 'vascular tissue.'),
         'Support or storage or photosynthesis', 'ground-tissue', [])]
] + [
    T('14biii', 'Q14(b)(iii)', 'C', Q14BIII,
      [pt(S('Diagram 1 (phloem): tube + companion cell (or sieve plate)'), 3, kind='criterion',
          note_sel=S('[accept transverse section]')),
       pt(S('Diagram 2 (xylem): tube + 1 wall feature (or tapering ends)'), 3, kind='criterion'),
       anyn(None, 3, 1, note_sel=S('[maximum of two labels from either diagram]'),
            options=[S('Labels (diagram 1): phloem, sieve tube, sieve plate, companion cell', 'cytoplasm',
                       piece=[2, i], psep=[': ', ', ']) for i in range(1, 6)]
            + [S('Labels (diagram 2): xylem, pits, thick wall, tracheid, vessel', piece=[2, i], psep=[': ', ', '])
               for i in range(1, 6)])],
      'bio-2-6', 'drawing-xylem-and-phloem', welded(13, '14.', '(b)', '(iii)'), 9,
      decision='Each drawing is priced "3, 0" and the labels "3(1)", three from either diagram\'s printed list, '
               'no more than two from one.'),
    T('14biv', 'Q14(b)(iv)', 'C', ask(13, 'Which of the tissues referred to in (iii) is composed of living cells?'),
      [pt(S('Phloem'), 3)], 'bio-2-6', 'phloem-is-living', welded(13, '14.', '(b)', '(iv)'), 3,
      stem=[M('(iii)', 13), Q14BIII]),
    T('14bv', 'Q14(b)(v)', 'C', ask(13, 'What is the function of meristematic tissue?'),
      [pt(S('Mitosis or cell division or growth or to produce new cells'), 3)], 'bio-2-6', 'meristems',
      at(13, '14.', '(b)', '(v)'), 3),
    T('14ci', 'Q14(c)(i)', 'C', Q14CI,
      [pt(s, 3) for s in pieces('Osmosis / soil water more dilute', 'concentrated / cell to cell (by osmosis)', n=3)],
      'bio-2-6', 'water-into-roots', at(14, '14.', '(c)', '(i)'), 9,
      decision='"3(3)": the three points, each cut at the scheme\'s own solidus.'),
    T('14cii', 'Q14(c)(ii)', 'C', Q14CII, [pt(S('*Xylem'), 3)], 'bio-2-6', 'xylem', at(14, '14.', '(c)', '(ii)'), 3,
      stem=[M('(i)', 13), Q14CI]),
    T('14ciii', 'Q14(c)(iii)', 'C', ask(13, 'Give two features of the tissue referred to in (ii) that facilitate this upward movement of water.'),
      [anyn(S('Narrow / continuous tube', 'no cell contents / attraction of H2O to walls / thick wall'), 2, 3)],
      'bio-2-6', 'xylem-adaptations', welded(14, '14.', '(c)', '(iii)'), 6, stem=[M('(ii)', 13), Q14CII]),
    T('14civ', 'Q14(c)(iv)', 'C', Q(13, 'Name and briefly explain any two processes involved in the upward movement of water in',
                                    'plants.'),
      [anyn(S('Root pressure / transpiration / adhesion / cohesion'), 2, 3),
       anyn(None, 2, 3, note_sel=S('Two explanations:'),
            options=[S('Root pressure:', 'H2O in pushes H2O up'), S('Transpiration:', 'H2O out pulls H2O up (or creates tension)'),
                     S('Adhesion:', 'H2O attracted to walls'), S('Cohesion:', 'continuous stream')])],
      'bio-2-6', 'water-transport-processes', welded(14, '14.', '(c)', '(iv)'), 12,
      decision='The names "2(3)" and the explanations "2(3)": two menus, claim two of each.'),
    # Q15(a)
    T('15ai', 'Q15(a)(i)', 'C', ask(14, 'What does the graph tell you about the phytoplankton population?'),
      [anyn(S('Decreases (or low) in winter / increases (or high) in spring or', 'decreases (or low) in autumn'), 3, 2)],
      'bio-3-1', 'phytoplankton-numbers', at(15, '15.', '(a)', '(i)'), 6, stem=[Q15A], fig='q15a-graph',
      decision=ROW_PRICED),
    T('15aii', 'Q15(a)(ii)', 'C', ask(14, 'Why do you think that nutrient levels are high in winter and then drop sharply in spring?'),
      [anyn(S('Plankton absorb (or use) (nutrients) /', '(extra) nutrients from dead organisms'), 3, 2,
            note_sel=S('Any three'))], 'bio-3-1', 'nutrient-levels', at(15, '15.', '(a)', '(ii)'), 6, stem=[Q15A],
      fig='q15a-graph'),
    T('15aiii', 'Q15(a)(iii)', 'C', Q(14, 'Give an example of an inorganic nutrient, necessary for phytoplankton growth, that you would',
                                      'expect to find in lake water.'),
      [pt(S('e.g. Nitrate [accept nitrogen]'), 2)], 'bio-3-1', 'inorganic-nutrient', at(15, '15.', '(a)', '(iii)'), 2,
      stem=[Q15A], fig='q15a-graph'),
    T('15aiv', 'Q15(a)(iv)', 'C', Q(14, 'Zooplankton is the collective term for the small animals present in the lake. Copy the graph',
                                    'Briefly explain the graph that you have drawn.'),
      [pt(s, 2, kind='criterion', note_sel=S('Features to look for in Graph:') if i == 0 else None)
       for i, s in enumerate(pieces('Zooplankton numbers lower than phytoplankton /', 'autumn peak shifted to the right',
                                    n=4))]
      + [anyn(S('Zooplankton eat phytoplankton /', 'for numbers to change'), 2, 2, note_sel=S('Explanation:'))],
      'bio-3-1', 'predator-prey-graph', at(15, '15.', '(a)', '(iv)'), 12, stem=[Q15A], fig='q15a-graph',
      decision='The graph\'s four printed features "4(2)", each cut at the scheme\'s own solidus, and the explanation '
               '"2(2)", two points from three. The scheme prints "speak shifted to the right" (for the spring '
               'peak); lifted as printed.'),
    T('15av', 'Q15(a)(v)', 'C', Q(14, 'Other than the effect of the zooplankton, suggest why the phytoplankton population drops in',
                                  'late autumn.'),
      [pt(S('Low temperature or low light (intensity)'), 4)], 'bio-3-1', 'autumn-decline', at(15, '15.', '(a)', '(v)'),
      4, stem=[Q15A], fig='q15a-graph'),
    # Q15(b)
    T('15bi', 'Q15(b)(i)', 'C', ask(14, 'Describe a procedure for estimating rabbit numbers in an ecosystem.'),
      [anyn(S('e.g. Capture-recapture: how captured', 'formula or calculation described', piece=2, psep=': '), 6, 2,
            open_list=True,
            note_sel=S('e.g. Capture-recapture: how captured', 'formula or calculation described', piece=1, psep=': '))],
      'bio-3-1', 'capture-recapture', at(16, '15.', '(b)', '(i)'), 12, stem=Q15B,
      decision='The scheme prints its points under one example method ("e.g. Capture-recapture"): an open menu, '
               'six points from seven.'),
    T('15bii', 'Q15(b)(ii)', 'C', ask(14, 'Suggest one reason for the initial rapid increase of the rabbit population.'),
      [pt(S('No predator or plenty of food or warm climate'), 3)], 'bio-3-1', 'population-growth',
      at(16, '15.', '(b)', '(ii)'), 3, stem=Q15B),
    T('15biii', 'Q15(b)(iii)', 'C', ask(14, 'Give two possible effects on an ecosystem of the extinction of a plant species.'),
      [anyn(S('Soil erosion / less nutrients', '/ change of animal species'), 2, 3)], 'bio-3-1', 'effects-of-extinction',
      at(16, '15.', '(b)', '(iii)'), 6, stem=Q15B),
    T('15biv', 'Q15(b)(iv)', 'C', ask(14, 'Suggest one advantage and one disadvantage of biological control of a pest organism.'),
      [pt(S('No (harmful) chemicals or specific (target pest)'), 3, label=S('Advantage:')),
       pt(S('Possible extinction (of a species) or may not be', 'balance of nature disturbed (or explained)'), 3,
          label=S('Disadvantage:'))], 'bio-3-1', 'biological-control', at(16, '15.', '(b)', '(iv)'), 6, stem=Q15B),
    T('15bv', 'Q15(b)(v)', 'C', ask(14, 'Suggest one reason why the rabbit numbers recovered.'),
      [pt(S('Immunity (to the virus evolved)'), 3)], 'bio-3-1', 'resistance-to-myxoma', at(16, '15.', '(b)', '(v)'), 3,
      stem=Q15B),
    # Q15(c)
    T('15ci', 'Q15(c)(i)', 'C', ask(15, 'Name three factors can that affect human population.'),
      [anyn(S('War / famine / contraception', 'disease or health care'), 3, 2)], 'bio-3-1', 'human-population-factors',
      at(16, '15.', '(c)', '(i)'), 6, stem=[Q15C], fig='q15c-graph'),
    T('15cii', 'Q15(c)(ii)', 'C', ask(15, 'Suggest two reasons why the human population increased so rapidly from the mid-1800s.'),
      [anyn(None, 2, 2, options=[S(*Q15CII_LIST, piece=1), S(*Q15CII_LIST, piece=2),
                                 S(*Q15CII_LIST, piece=2, psep='/ or ')])],
      'bio-3-1', 'population-explosion', at(16, '15.', '(c)', '(ii)'), 4, stem=[Q15C], fig='q15c-graph',
      decision='The scheme prints three reasons separated by its own solidus, the third on a line that opens '
               '"or improved medicine or improved hygiene"; read whole, the runner takes a line opening "or" as a '
               'closing alternative and would leave that priced reason unclaimable. Each reason is its own '
               'option, cut at the solidus, the third without the line\'s leading "or". Coordinator\'s reviewer pass.'),
    T('15ciii', 'Q15(c)(iii)', 'C', ask(15, 'Suggest what could happen to biological diversity as the human population continues to increase.'),
      [pt(S('Decrease or increase or stays the same'), 1)], 'bio-3-1', 'biodiversity-and-population',
      at(16, '15.', '(c)', '(iii)'), 1, stem=[Q15C], fig='q15c-graph'),
    T('15civ', 'Q15(c)(iv)', 'C', Q(15, 'The vast amount of waste generated is one of the consequences of this huge increase.',
                                    'Mention the three main ways in which waste can be minimised.'),
      [pt(s, 1) for s in pieces('Reduce / reuse / recycle', n=3)], 'bio-3-1', 'minimising-waste',
      at(16, '15.', '(c)', '(iv)'), 3, stem=[Q15C], fig='q15c-graph',
      decision='"3 (1)": the three ways, each cut at the scheme\'s own solidus.'),
    T('15cv', 'Q15(c)(v)', 'C', ask(15, 'What is pollution?'), [pt(S('Any harmful addition to the environment'), 2)],
      'bio-3-1', 'pollution', at(16, '15.', '(c)', '(v)'), 2),
    T('15cvi', 'Q15(c)(vi)', 'C', ask(15, 'What is the role of microorganisms in pollution control?'),
      [pt(S('Decomposition (or explained)'), 2)], 'bio-3-2', 'microorganisms-in-pollution-control',
      at(16, '15.', '(c)', '(vi)'), 2),
] + [
    T(f'15cvii{n}', f'Q15(c)(vii){n}', 'C',
      [Q(15, 'Describe the role of'), Q(15, f'{n}. {who}', br=True),
       Q(15, 'in the Nitrogen Cycle and in the Carbon Cycle.', br=True)],
      [anyn(S(f'{who}: {first}', last, piece=2, psep=': '), 3, 2)], 'bio-3-2', concept,
      welded(16, '15.', '(c)', '(vii)', why=ITEM_WELDED), 6, decision=EACH_ITEM + extra)
    for n, who, first, last, concept, extra in [
        (1, 'Plants', 'absorb nitrates / synthesise protein / absorb CO2 /', 'respire / die', 'plants-in-cycles',
         ' The scheme prints "photsynthesise"; lifted as printed.'),
        (2, 'Animals', 'consume plants / assimilate protein / assimilate.', 'respire / die', 'animals-in-cycles',
         ' The scheme sets a full stop inside "assimilate. carbohydrate"; lifted as printed.')]
]

ANSWER_VARIANTS = {
    '10bv': [
        ('no', 'No', [pt(S('No, because pig DNA is not the same as horse DNA'), 6, note_sel=S('6, 3, 0'),
                         note_lead='The scheme marks this answer')]),
        ('yes', 'Yes', [pt(S('Yes, because not all the DNA is beef DNA'), 6, note_sel=S('6, 3, 0'),
                           note_lead='The scheme marks this answer')]),
    ],
    '12civ': [
        ('pulmonary-vein', 'Pulmonary vein',
         [pt(S('Pulmonary Vein'), 3),
          col(11, (140, 498, 300, 550), 'Blood has been cleared of CO2 in the lungs', 3, kind='point')]),
        ('pulmonary-artery', 'Pulmonary artery',
         [pt(S('Pulmonary Artery'), 3),
          col(11, (335, 498, 460, 550), 'Brings CO2 rich blood to the lungs', 3, kind='point')]),
    ],
    '13ciii': [
        ('iodoform', 'Iodoform test',
         [anyn(S('Iodoform test / sodium hypochlorite / potassium iodide /', 'heat or warm / yellow (crystals)'), 4, 3)]),
        ('dichromate', 'Dichromate test',
         [anyn(S('Dichromate test / potassium dichromate or sodium dichromate /', 'acidified / warm / from orange to green'),
               4, 3)]),
    ],
}

FIGURES = {
    # key suffix: (doc, page, rect in PDF points, credit, letters, alt, solution[, masks])
    'q2ai-reaction': ('paper', 2, (185, 346, 350, 372), SEC, [],
                      'The reaction as the paper prints it on one line: the letter A, an arrow pointing right, then '
                      'B + C + D.', False),
    'q2aii-reaction': ('paper', 2, (140, 428, 390, 460), SEC, [],
                       'The reaction as the paper prints it on one line: the word Fat, an arrow pointing right with '
                       'the letter X written above it, then Fatty Acids + Y.', False),
    'q3-tissue': ('paper', 3, (110, 78, 470, 262), SEC, ['A', 'B', 'C'],
                  'Line drawing of a cluster of round body cells, each with a dark nucleus, set in stippled tissue '
                  'and threaded through by a network of fine branching tubes. Two lines labelled Body Cells point to '
                  'cells at the top. At the top right a wider tube labelled A joins the network, a thick arrow '
                  'labelled Direction of blood flow pointing down into it. At the bottom left a wider tube labelled B '
                  'leaves the network, a thick arrow pointing out of its open end. At the right a tube labelled C '
                  'branches off the network and runs out to the right, drawn with zigzag lines inside it.', False),
    'q8a-microscope': ('paper', 7, (440, 22, 555, 165), SEC, ['A', 'E', 'O'],
                       'Line drawing of a light microscope: an eyepiece tube on top of a curved arm, two round knobs '
                       'on the side of the arm, a revolving nosepiece with objective lenses over a stage holding a '
                       'slide, and a footed base. Label E points to the top of the eyepiece tube, label A to the '
                       'upper, larger knob, and label O to one of the objective lenses.', False),
    'q10c-genotype': ('paper', 9, (418, 453.5, 522, 542), SEC, [],
                      'A circle holding two pairs of chromosomes. On the left, two long rods side by side, the left '
                      'one marked P and the right one marked p at the same height near their tops. On the right, a '
                      'short pair: a longer hooked chromosome marked X and a much shorter one marked Y.', False),
    'q11a-elbow': ('paper', 10, (460, 25, 565, 140), SEC, ['A'],
                   'Shaded image of a human elbow seen from the side: the upper-arm bone meeting the forearm bones, '
                   'with muscle running down the upper arm on each side. Label A points to a pale band running from '
                   'the lower end of the left-hand muscle to a forearm bone.', False),
    'q13a-graphs': ('paper', 12, (130, 62, 445, 180), SEC, [],
                    'Two small sketch graphs side by side, each with an arrow up the vertical axis and an arrow along '
                    'the horizontal axis, and no labels or scales. Graph A: a straight line falling from upper left '
                    'to lower right. Graph B: a curve rising steeply from low on the left to a single peak, then '
                    'falling steeply to the right.', False),
    'q15a-graph': ('paper', 14, (100, 118, 475, 276), SEC, [],
                   'Line graph over one year, the horizontal axis divided into WINTER, SPRING, SUMMER and AUTUMN, '
                   'with no vertical scale. Four lines are labelled at the left. The thick solid line, '
                   'Phytoplankton, falls to a low in winter, rises to a sharp peak in spring, drops and stays low '
                   'with small rises through summer, rises to a second sharp peak, a little lower, in autumn, then '
                   'falls. The dashed line, Nutrients, is high through winter, falls steeply in spring, stays low '
                   'through summer and rises again through autumn. The dotted line, Light, rises from a low in '
                   'winter to a high in summer and falls in autumn. The dash-dot line, Temperature, is low in '
                   'winter, rises to a high in summer and falls through autumn.', False),
    'q15c-graph': ('paper', 15, (108, 55, 430, 268), SEC, [],
                   'Line graph titled World Population Growth in Billions: Billions of People, 0 to 10, against '
                   'Year, 0 to 2500, on a grid. The line runs almost flat, below 1 billion, from year 0 to about '
                   '1750, then curves upward ever more steeply, passing about 4 billion near 2000 and ending near 9 '
                   'billion a little after 2000.', False),
}
