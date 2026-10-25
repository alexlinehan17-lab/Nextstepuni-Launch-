"""Biology 2012 Ordinary Level — reviewed task ledger, carded from the paper for the first time.

Independent visual sweep (2026-10-25), every page rendered and read:
  * The 2012 paper is one booklet (M43), 16 pages: p1 cover and instructions,
    p2-p4 Section A Questions 1-6, p5-p7 Section B Questions 7-9, p8-p13
    Section C Questions 10-15, p14-p16 "Blank Page". Sections A and B are
    answered on the paper; Section C in an answer book. No acknowledgements
    page: the Q11(b) rabbit photograph and every drawing carry no credit.
  * The marking scheme, 12 pages: p1 cover, p2 blank (no text), p3
    introduction, cancelled and surplus answers, p4 conventions, p5-p10
    Questions 1-15 (one table, printed page numbers 5-10), p11 blank (no
    text), p12 back cover (no text).

The paper keeps the long-standing shape: any five of Section A's six
questions, any two of Section B's three, any four of Section C's six, and
Questions 14 and 15 are each any two of (a), (b), (c). Every printed ask is
carded. No Biology card existed for 2012 Ordinary before this review.

This scheme prints no reprint of any question: each answer stands under its
own question number, letter and roman, in the table's own columns. A task is
anchored on its own part marker, found by walking the scheme's numbering down
to it (SQ path). The scheme prints Section A's heads "1." to "6." (Q5 as "5"),
Q7, Q10, Q12, Q13 and Q15 as a number over "(a)" (Q15's ladder between them),
Q8, Q9, Q11 and Q14(a) with the letter on the number's own line ("8. (a)",
"11 (a)", "14. (a)"), and Q14(b), (c) and Q15(b), (c) under a repeated "14."
or "15."; the path walks those lines. Two romans, Q9(b)(iv) and (viii), are set
on their answer's own line ("(iv) Water instead of starch"): each is a welded
bare anchor and its row is read from that line. A numbered item ("1.", "2.")
is anchored on the roman it is printed under.

The scheme counts POINTS ("(1 pt)", "(3 pts)"; Q6 "(3pts)") and heads each
question or part with what they are worth. Section A: Q1-Q4 and Q6 print "2(1)
+ 3(2) + 2(6)" over seven points and Q5 "3(2) + 2(7)" over five (scheme p5,
rendered and looked at). Read as the conventions page (p4, rule 4: "the first
two correct answers are awarded 4 marks each and each subsequent correct
answer is awarded 3 marks") defines an ordered split, the first correct
answers would earn 1 (Q5: 2) and the last 6 (Q5: 7): each notation leads with
its SMALLEST rate, where every Section B and C ladder of this scheme leads
with its largest, as every Section A split of the 2013-2018 Ordinary schemes
does ("6(3) + 2", "2(7)+3(2)", "2(5)+5(2)", "9 + 8 + 3(1)"). No reading prices
each printed answer on its own, so each Section A question is ONE card at the
rubric's printed 20 ("Each question carries 20 marks"), every row unpriced
(the coordinator's whole-part rule, as 2013 Higher Q5 and Q6 and 2013 Ordinary
Section B (a)); no response is carded at the notation's first rate and no
reordering is derived. Brought to the coordinator. The scheme prints no words
of its own over most Section A answers, so each row there carries the scheme's
own part marker as its label ("(a) (i)", "(c)"), lifted from the table, so the
rows can be told apart.

Every other ordered split leads with its largest rate and is carded at its
first rate: every Section B (a) "5 + 1" over two points and (b) "2(6)+6(2)"
over eight; Q10(b) "2(6) + 6(2) +3(1)" over eleven and (c) "2(6)+6(2)" over
eight; Q11(a) "6 + 3", (b) "2(5) + 3+7(2)" over ten and (c) "2(6)+6(2)";
Q12(a) "2(3)+3(1)", (b) "3(5) +6(2)" and (c) "3(4) + 6(2)"; Q13(a) "7 +
2(1)", (b)(ii)-(v) "2(6) + 4(2)" and (c) "2(7) +5(2)"; Q14(a) "2(5)+2(4)+4(1)",
(b) "2(5)+2(3)+7(2)" and (c) "2(5) + 2(4) + 5(1)"; Q15(a) and (c)
"2(5)+2(4)+6(2)" and (b) "2(5)+2(3)+7(2)". Each ladder is keyed to its own
part. Q10(a)'s pyramid is "3(3)", a fixed 3 per point, priced beside Q10's
ladders. Three drawings are priced on their own beside their part's ladder,
"D. 5,2,0" for the drawing and "L." for its labels: Q13(b)(i) "D. 5,2,0
L.2(1)", Q14(a)(iv) "D. 5,2,0 L. 3(1)" and Q14(c)(vii) "D. 5,2,0 L. 2(1)"; each
ladder names their units as fixed and their cards keep their own marks.

The scheme's text layer reads its single quotes as U+201E and U+201F
(Q1(a)(ii) "[not „spread‟]"); lifted as read.

The census reader lost Question 4 (paper.py WELDED_HEADS, gated to this
sitting): p3's Q3(g) row "An organ is a group of systems." ends in its circle
options "T F", so the "4." head filed as the tail of Q3(g) and Q4's (a)-(d)
were read as repeats of Q3's letters and lost. The fix takes the census from
125 leaves to the paper's 129; all 129 are claimed here.
"""
from bio_review_lib import Q, SQ, S, M, pt, anyn, allof, T, L

YEAR, LEVEL = 2012, 'ol'
REVIEWED_AT = '2026-10-25'

SOURCES = {
    'paper': {'path': 'examiner-reports/biology/papers/2012-ol-paper.pdf',
              'fileid': 'LC025GLP000EV.pdf',
              'sha256': '87549dd5cb4eb51d6f306c534bad3c0851cef5d83d40b8ea69e11de4f28882fc',
              'pages': 16},
    'scheme': {'path': 'examiner-reports/biology/schemes/2012-ol.pdf',
               'fileid': 'LC025GLP000EV.pdf',
               'sha256': 'a05fa5fd32ba75c1d8152df900adae39dbf76c43e6cf35ab5e1e6bb7d2cc2aad',
               'pages': 12},
}

PAGE_ROLES = {
    'paper': {1: 'cover', **{p: 'questions' for p in range(2, 14)}, 14: 'blank', 15: 'blank', 16: 'blank'},
    'scheme': {1: 'cover', 2: 'blank', 3: 'introduction', 4: 'conventions',
               **{p: 'marking' for p in range(5, 11)}, 11: 'blank', 12: 'back-cover'},
}


def _ladder(notation, **extra):
    """An ordered split as the scheme prints it ("2(6)+6(2)", "5 + 1")."""
    steps = []
    for term in notation.split('+'):
        n, _, m = term.strip().partition('(')
        steps += [int(m.rstrip(')'))] * int(n) if m else [int(n)]
    return {'steps': steps, 'notation': notation, **extra}


QUESTION_TOTALS = {
    **{n: 20 for n in range(1, 7)}, **{n: 30 for n in range(7, 10)},
    **{n: 60 for n in range(10, 14)}, 14: 90, 15: 90,   # Q14, Q15: any two of three 30s
}
# Only a part whose tasks sum to its printed total: Q10(a)'s "(9)", priced
# "3(3)". Every other part is an ordered split whose ladder makes its printed
# total (Section B's rubric "Part (a) carries 6 marks and part (b) carries 24
# marks"; Q10-Q13's "(9)", "(27)", "(24)"; Q14 and Q15's "(30, 30)"), each
# ladder below checked against it by hand: 5+1 = 6, 2(6)+6(2) = 24,
# 2(6)+6(2)+3(1) = 27, 6+3 = 9, 2(5)+3+7(2) = 27, 2(3)+3(1) = 9, 3(5)+6(2) =
# 27, 3(4)+6(2) = 24, 7+2(1) = 9, 2(6)+4(2) and its drawing's 5+2(1) = 27,
# 2(7)+5(2) = 24, 2(5)+2(4)+4(1) and its drawing's 5+3(1) = 30, 2(5)+2(3)+7(2)
# = 30, 2(5)+2(4)+5(1) and its drawing's 5+2(1) = 30, 2(5)+2(4)+6(2) = 30. The
# runner checks each question's ladders against its printed total.
PART_TOTALS = {(10, 'a'): 9}
LADDERS = {
    (7, 'a'): _ladder('5 + 1'), (8, 'a'): _ladder('5 + 1'), (9, 'a'): _ladder('5+1'),
    (7, 'b'): _ladder('2(6)+6(2)'), (8, 'b'): _ladder('2(6) + 6(2)'), (9, 'b'): _ladder('2(6)+6(2)'),
    # Q10(a) "3(3)" is fixed, beside these two.
    (10, 'b'): _ladder('2(6) + 6(2) +3(1)'), (10, 'c'): _ladder('2(6)+6(2)'),
    (11, 'a'): _ladder('6 + 3'), (11, 'b'): _ladder('2(5) + 3+7(2)'), (11, 'c'): _ladder('2(6)+6(2)'),
    (12, 'a'): _ladder('2(3)+3(1)'), (12, 'b'): _ladder('3(5) +6(2)'), (12, 'c'): _ladder('3(4) + 6(2)'),
    (13, 'a'): _ladder('7 + 2(1)'),
    # (b)(i)'s drawing "D. 5,2,0 L.2(1)" is fixed beside (ii)-(v)'s "2(6) + 4(2)".
    (13, 'b'): _ladder('2(6) + 4(2)', fixed={5: 1, 1: 2}),
    (13, 'c'): _ladder('2(7) +5(2)'),
    # (a)(iv)'s drawing "D. 5,2,0 L. 3(1)" and (c)(vii)'s "D. 5,2,0 L. 2(1)" are
    # fixed beside their parts' ladders.
    (14, 'a'): _ladder('2(5)+2(4)+4(1)', fixed={5: 1, 1: 3}),
    (14, 'b'): _ladder('2(5)+2(3)+7(2)'),
    (14, 'c'): _ladder('2(5) + 2(4) + 5(1)', fixed={5: 1, 1: 2}),
    (15, 'a'): _ladder('2(5)+2(4)+6(2)'), (15, 'b'): _ladder('2(5)+2(3)+7(2)'), (15, 'c'): _ladder('2(5)+2(4)+6(2)'),
}

# The scheme's point counts, as mark units: each point at its ladder's first
# rate, the drawings' units as printed.
CHECKSUMS = {
    **{(n, 'a'): {5: 2} for n in (7, 8, 9)}, **{(n, 'b'): {6: 8} for n in (7, 8, 9)},
    (10, 'a'): {3: 3}, (10, 'b'): {6: 11}, (10, 'c'): {6: 8},
    (11, 'a'): {6: 2}, (11, 'b'): {5: 10}, (11, 'c'): {6: 8},
    (12, 'a'): {3: 5}, (12, 'b'): {5: 9}, (12, 'c'): {4: 9},
    (13, 'a'): {7: 3}, (13, 'b'): {6: 6, 5: 1, 1: 2}, (13, 'c'): {7: 7},
    (14, 'a'): {5: 9, 1: 3}, (14, 'b'): {5: 11}, (14, 'c'): {5: 10, 1: 2},
    (15, 'a'): {5: 10}, (15, 'b'): {5: 11}, (15, 'c'): {5: 10},
}

SCAN_PAGES = {'paper': range(1, 14)}
SELECTION_SCAN = [
    ('paper', 1, 'any five', 'Cover rubric, Section A: whole-question choice; every question is carded.'),
    ('paper', 1, 'any two', 'Cover rubric, Section B: whole-question choice; every question is carded.'),
    ('paper', 1, 'any four', 'Cover rubric, Section C: whole-question choice; every question is carded.'),
    ('paper', 2, 'any five', 'Section A rubric repeated.'),
    ('paper', 3, 'the following', 'Q3 lead-in: every statement asked, a row each on the question\'s card.'),
    ('paper', 3, 'or', 'Q3 "true (T) or false (F)": the answer options.'),
    ('paper', 3, 'or', 'Q3 "T or F": the answer options.'),
    ('paper', 3, 'or', 'Q4(a) "a root or a stem": the answer options.'),
    ('paper', 3, 'the following', 'Q4(b) "in the following list": every tissue type asked.'),
    ('paper', 4, 'the following', 'Q5 list of terms: the options; every description matched.'),
    ('paper', 5, 'any two', 'Section B rubric repeated.'),
    ('paper', 5, 'the following', 'Q7(b) lead-in: every part asked.'),
    ('paper', 5, 'or', 'Q7(b) "your breathing rate or your pulse rate": the candidate ticks the rate; the scheme '
                       'prices both alike ("Count pulse or breaths", "Ticking Breathing Rate/Pulse Rate (0 pts)"), so '
                       'no route.'),
    ('paper', 5, 'both', 'Q7(b)(iv) "both fit and non-fit people": description.'),
    ('paper', 6, 'the following', 'Q8(b) lead-in: every part asked.'),
    ('paper', 7, 'the following', 'Q9(b) lead-in: every part asked.'),
    ('paper', 8, 'any four', 'Section C rubric repeated.'),
    ('paper', 8, 'any two', 'Q10(b)(ii) "Name any two abiotic factors": two factors, each with how it was measured.'),
    ('paper', 8, 'the following', 'Q10(b)(iii) "the following key": the printed key, shown with the animals as the '
                                  'question\'s own print.'),
    ('paper', 9, 'or', 'Q11(b) passage "skin, fur or eyes": passage text.'),
    ('paper', 9, 'or', 'Q11(b) passage "eyes, fur or hair": passage text.'),
    ('paper', 9, 'both', 'Q11(b) passage "if both genes are recessive": passage text.'),
    ('paper', 11, 'any two', 'Q13(b)(ii) "Name any two bacterial shapes": one menu, claim two.'),
    ('paper', 12, 'any two', 'Q14 "any two of the parts (a), (b), (c)": whole-part choice; every part is carded.'),
    ('paper', 12, 'or', 'Q14(a)(iii) "aerobic or anaerobic": the answer options.'),
    ('paper', 12, 'the following', 'Q14(a)(iv) "Answer the following questions in relation to the activity": every '
                                   'numbered item asked, one card each.'),
    ('paper', 12, 'or', 'Q14(c)(iv) "mitosis or meiosis": the answer options.'),
    ('paper', 13, 'any two', 'Q15 "any two of the parts (a), (b), (c)": whole-part choice; every part is carded.'),
    ('paper', 13, 'any two', 'Q15(b)(ii)2 "Name any two types of neuron": one menu, claim two.'),
]

ROUTES = {}

SEC = 'State Examinations Commission'
NO_REPRINT = 'The scheme prints no reprint of any question: anchored on the part\'s own marker.'
WELDED = ('The scheme prints no reprint and sets this part\'s marker on its answer\'s own line: anchored on that '
          'marker.')
WHOLE_ANCHOR = ('The scheme prints no reprint of any question: a whole question is anchored on its first part\'s '
                'marker under the question\'s number.')
EACH_ITEM = 'A list the scheme prices entry by entry: one card per entry, each its own slice of the printed line.'
NO_ANSWER = 'The scheme prints no answer here, only what earns the marks.'
TWO_POINTS = 'The scheme prices this part at {n} points ("({n} pts)"): each printed point its own row.'
LEAD_IN = ('The printed item alone is too short a question to stand, so the card carries the printed lead-in in its '
           'question text.')
WHOLE_A = ('The scheme prints Q{q} as "{notation}" over its {n} points (p5). Read as the conventions page (p4, rule 4) '
           'defines an ordered split, the first correct answers would earn {low} and the last {high}: the notation '
           'leads with its smallest rate, where every Section B and C ladder of this scheme leads with its largest, '
           'and no reading prices each printed answer on its own. So the whole question is one card at the Section A '
           'rubric\'s 20 ("Each question carries 20 marks"), every row unpriced (the coordinator\'s whole-part rule, '
           'as 2013 Higher Q5 and Q6); no response is carded at the first rate and no reordering is derived. Each row '
           'carries the scheme\'s own printed part marker or label. Brought to the coordinator.')
EG_OPEN = 'The scheme prints this answer after "e.g.": an example, an open menu.'
DRAWING = ('The scheme prices the drawing on its own, "{tariff}", beside the part\'s ladder: the diagram "5,2,0" as one '
           'row naming what it must show (its band the row\'s note) and the labels at 1 each.')


def at(page, *path_and_marker, why=NO_REPRINT, nth=1):
    """The part's own marker under its printed question (and letter) lines on the scheme page."""
    *path, marker = path_and_marker
    return SQ(page, marker, path=path, paired=why, bare=True, nth=nth)


def welded(page, *path_and_marker):
    """The part's marker opening its own answer line ("(iv) Water instead of starch")."""
    *path, marker = path_and_marker
    return SQ(page, marker, path=path, paired=WELDED, bare=True, welded=True)


def ask(page, sentence, **kw):
    """A one-line ask closed by its own punctuation, before its answer line."""
    return Q(page, sentence, sentence, **kw)


def blank(page, sentence, sep='_', **kw):
    """An ask whose last word runs straight into its printed answer line ("...protein?____"): the
    line cut at the line."""
    return Q(page, sentence, piece=1, psep=sep, **kw)


def eg(start, end=None, **kw):
    """A scheme answer printed after its "e.g.": the answer itself, cut after the scheme's own "e.g."."""
    return S(start, end, piece=2, psep='e.g. ', **kw)


def egs(line, k, sep=' / ', **kw):
    """Entry k of a scheme list printed after its "e.g." ("e.g. Wind dispersal / Animal dispersal")."""
    return S(line, piece=[2, k], psep=['e.g. ', sep], **kw)


def cell(line, i, cuts, page=None, end=None):
    """Cell i of a scheme line printed as cells ("A = Head B = Nucleus C = Tail"), cut at the cells' own
    printed boundaries: cuts[k] = (text opening cell k+1, text closing cell k)."""
    pieces, seps = [], []
    if i > 0:
        pieces.append(2)
        seps.append(cuts[i - 1][1])
    if i < len(cuts):
        pieces.append(1)
        seps.append(cuts[i][0])
    return S(line, end, page=page, piece=pieces, psep=seps)


def meaning(line, i, cuts, page, end=None):
    """The answer alone of cell i (after its " = "), for a figure's label key."""
    sel = cell(line, i, cuts, page=page, end=end)
    return {**sel, 'piece': sel['piece'] + [2], 'psep': sel['psep'] + [' = ']}


def labels(cells, asked=None):
    """A figure's label key: [(letter, meaning selector)]."""
    return [L(x, sel, x == asked) for x, sel in cells]


# ------------------------------------------------------------ question text --
Q1 = Q(2, 'A student brings a tuna and sweetcorn sandwich, an apple and a bag of crisps for her lunch.')
Q2 = Q(2, 'Amoeba is a tiny, one-celled organism.',
       'This diagram shows the structure of a freshwater Amoeba as seen through a microscope.')
Q3 = Q(3, 'Indicate whether each of the following statements is true (T) or false (F) by drawing a circle around T or F in',
       'each case.')
Q4 = Q(3, 'The diagram below represents a transverse section through part of a plant.')
Q5 = [Q(4, 'Place each term from the following list into Column B to match a description in Column A.',
        'The first one has been completed as an example.'),
      Q(4, 'List:', 'Smell.', br=True)]
Q6 = [Q(4, 'In pea plants the allele for tall (T) is dominant over the allele for dwarf (t).'),
      Q(4, 'A heterozygous tall plant is crossed with a dwarf plant.')]
Q7AI = ask(5, 'Name one disorder of the human breathing system.')
Q7B = [Q(5, 'Answer the following questions about an activity that you carried out to investigate the effect of',
         'exercise on your breathing rate or your pulse rate.'),
       ask(5, 'Tick the rate you will refer to.')]
Q7BIV = ask(5, 'Does this investigation give the same result for both fit and non-fit people?')
Q8AI = ask(6, 'What is an enzyme?')
Q8B = Q(6, 'Answer the following questions in relation to an investigation that you carried out into the effect of',
        'temperature on the rate of activity of an enzyme.')
Q9B = ask(7, 'Answer the following questions in relation to food tests that you carried out as part of your practical '
             'work.')
Q9BI = ask(7, 'What chemical did you use to test the food for starch?')
Q9BV = Q(7, 'Another food was tested for the presence of protein.', 'What solution was used to test for protein?')
Q10BI = [Q(8, 'All organisms in an ecosystem are influenced by biotic and abiotic factors.'),
         ask(8, 'Explain the underlined words.')]
Q10BIII = Q(8, 'Keys may be used to identify animals. Use the following key to identify animals A, B and C.',
            'The animals are not drawn to scale.')
Q10BIV = Q(8, 'All organisms are adapted to their own habitat.')
Q10BIV1 = [M('1.', 8), ask(8, 'Name one animal from the ecosystem you have studied.')]
Q10CII1 = [M('1.', 8), ask(8, 'Name one plant from the ecosystem you have studied.')]
Q11AI = ask(9, 'In genetics, what is meant by the term haploid?')
Q11B = [ask(9, 'Read the paragraph below and answer the questions that follow.'),
        Q(9, 'The rabbit in the photograph has no pigment in its skin, fur or eyes. This is due to',
          'rabbits, turtles, squirrels, deer and frogs.')]
Q11BIV = Q(9, 'Mutations can lead to variation in organisms. Variations that make an organism better adapted to its',
           'environment can lead to evolution.')
Q11CI = Q(9, 'Genetic engineering is regularly used in animals, plants and micro-organisms.',
          'What is meant by genetic engineering?')
Q12AI = ask(10, 'Name the two main types of reproduction.')
Q12B = Q(10, 'The flower is the organ of reproduction in many plants.')
Q12C = Q(10, 'The diagram shows a human sperm cell.')
Q13A = Q(11, 'All organisms may be classified (grouped) into five kingdoms.')
Q13C = Q(11, 'The diagram shows part of the fungus Rhizopus.')
Q14AII = Q(12, 'Aerobic respiration takes place in two stages.')
Q14AII1 = [M('1.', 12), ask(12, 'Where in a cell does stage 1 occur?')]
Q14AIV = Q(12, 'In yeast cells, alcohol is produced by fermentation.')
Q14AIVD = ask(12, 'Draw a labelled diagram showing how alcohol may be produced in the laboratory.')
Q14AIVQ = ask(12, 'Answer the following questions in relation to the activity:')
Q14AIV1 = [M('1.', 12), ask(12, 'Name another substance that is produced during the fermentation process.')]
Q14AIV2 = [M('2.', 12), ask(12, 'How would you detect this other substance?')]
Q14BIII = Q(12, 'During photosynthesis water is split into three products.')
Q14BIII1 = ask(12, '1. Name each of these three products.')
Q14C = Q(12, 'Tissue culture can be used to grow new tissues in the laboratory.')
Q14CV = ask(12, 'What medical term is used to describe the disease caused by uncontrolled mitosis in human cells?')
Q15A = Q(13, 'The diagram shows a section through human skin.')
Q15BI = Q(13, 'In relation to plant responses:')
Q15BII = Q(13, 'In relation to animal responses:')
Q15BII2 = Q(13, '2. Messages are carried around the body by neurons (nerve cells).', 'Name any two types of neuron.')
Q15C = Q(13, 'The diagram shows the human digestive system.')
Q15CI = ask(13, 'Name the parts labelled A, B and C.')

# ------------------------------------------------------- scheme cell lines --
# Section A heads, read with `after=` so a row and its part marker are found
# under their own question (scheme p5).
H1, H2, H3, H4, H5, H6 = '1.', '2.', '3.', '4.', '3(2) + 2(7)', '6.'
CRISPS = 'Crisps / “Butter” (on bread) [not „spread‟]'
BREAD = 'Bread or Sweetcorn / Apple'
PROTEIN = 'Keratin / Myosin / Collagen'
FAT = ('Energy (storage) / Insulation / Cell', 'vitamins/Protection')
AMOEBA = ('A = Contractile Vacuole B = Cytoplasm /', 'D = Nucleus')
AMOEBA_CUTS = [(' B =', 'Vacuole '), (' C =', 'Endoplasm '), (' D =', 'Foot ')]
FUNC_A = 'Function “A” = Water balance / Osmoregulation'
FUNC_C = ('Function “C” = Movement / Feeding / Egestion/', 'Homeostasis')
TF = [('a', 'F', 1), ('b', 'T or F', 1), ('c', 'F', 2), ('d', 'T', 2), ('e', 'T', 3), ('f', 'F', 3), ('g', 'F', 4)]
GAMETES = 'Possible gametes: (T) (t) X (t)'
OFFSPRING = 'Genotypes of offspring: (Tt) (tt)'
PHENOTYPES = 'Phenotypes of offspring: Tall & Dwarf (allow small)'
INHALER = 'e.g. Use of Inhaler (must match)'
RESTING = 'Count pulse or breaths / time or rate'
PEROXIDE = 'e.g. Hydrogen peroxide (Must match enzyme)'
FROTH = ('e.g. Volume of froth / time (Depends on enzyme', 'used)')
TEMP_RESULT = ('Increasing activity with increasing temp / works best at', 'certain temp.')
ABIOTIC = ('• Temperature – thermometer', '• Soil pH – pH meter')
KEY = 'A = Tribolium B = Planarian C = Nematode'
KEY_CUTS = [(' B =', 'Tribolium '), (' C =', 'Planarian ')]
ADAPTED = 'e.g. 1. Grasshopper 2. Green colour'
QUADRAT = 'Throw quadrat / note if daisies present /'
EFFECTS = ('Plants and/or animal numbers increase and /or', 'allowed)')
HAPLOID = ('Haploid = single set of chromosomes or half the diploid', 'number')
CHROMOSOME = ('Chromosome = group of genes joined together or large', 'DNA molecule')
MUTATION = ('Change (in the make-up) / in a gene or DNA or', 'chromosome')
SUNSCREEN = 'Absence of melanin / speeds up sunburn or opposite'
GE = ('Manipulation or artificial / alteration /of genes or', 'chromosomes')
PROCEDURES = ('Isolation / Cutting / Ligation / Transformation / Cloning /', 'Expression (Name or explain)')
GE_USES = 'EG. Long-life tomatoes / Weedkiller-resistant crops'
SEXUAL = 'Sexual & Asexual reproduction'
FERTILISATION = 'Fusion / of gametes / to produce a zygote'
OVARY = 'Ovary (accept carpel)'
DISPERSAL = 'e.g. Wind dispersal / Animal dispersal'
GERMINATION = 'Water / O2 (Allow air) / suitable temperature'
SPERM = 'A = Head B = Nucleus C = Tail'
SPERM_CUTS = [(' B =', 'Head '), (' C =', 'Nucleus ')]
CONTRACEPTION = 'e.g. Natural / Mechanical or examples'
SHAPES = ('Bacillus or rod shaped / Coccus or spherical', '(Round) / Spirillum or spiral shaped')
FISSION = 'Binary Fission or asexual [Not Mitosis]'
GROWTH = 'Temp / O2 (allow air)/ water/ food /pH / Waste'
RHIZOPUS = 'A = Stolon or Hypha; B = Rhizoid'
RHIZOPUS_CUTS = [('; B =', 'Hypha; ')]
RHIZOID = 'Anchor / absorb / secretes enzymes'
AEROBIC = ('Breakdown of food or production of energy / in', 'presence of O2')
OSMOSIS = ('(Movement of) H2O / through semi-permeable', 'conc)')
PRODUCTS = 'O2 / H+ / e-'
YIELD = 'e.g. extra CO2 / more light'
TISSUE = 'Group of cells / with a common function'
CAUSES = 'e.g. Radiation / smoking'
MEIOSIS = ('Reduction (halving) of Chromosome numbers or to', 'division)')
SKIN = 'A = Hair B = Sweat gland C = Blood vessels'
SKIN_CUTS = [(' B =', 'Hair '), (' C =', 'gland ')]
SKIN_FUNCTIONS = 'e.g. Protection / Melanin production'
EXCRETION = 'e.g. Kidney / Urine'
NEURONS = 'Motor Neuron / Sensory Neuron/ Interneuron'
GUT = {'A': 'A = Duodenum or Small Intestine', 'B': 'B = Colon or Large Intestine', 'C': 'C = Stomach'}
TOOTH = 'e.g. Incisor / to cut'
PANCREAS = 'Produces enzymes or named enzyme /'


def amoeba_labels():
    # (a) asks all four letters.
    return [L(x, meaning(AMOEBA[0], i, AMOEBA_CUTS, 5, end=AMOEBA[1]), True) for i, x in enumerate('ABCD')]


def section_labels():
    # The scheme prints each tissue type with its letter ("Ground Tissue = A;"): the meaning is the
    # cell's left side.
    return [L(x, S(line, page=5, piece=1, psep=' ='), True)
            for x, line in (('A', 'Ground Tissue = A;'), ('B', 'Vascular Tissue = B'), ('C', 'Dermal Tissue = C;'))]


def key_labels(asked=None):
    return labels([(x, meaning(KEY, i, KEY_CUTS, 7)) for i, x in enumerate('ABC')], asked)


def sperm_labels(asked=None):
    return labels([(x, meaning(SPERM, i, SPERM_CUTS, 8)) for i, x in enumerate('ABC')], asked)


def rhizopus_labels(asked=None):
    # The scheme names A and B; C (asked about in (iii)) is never named.
    return labels([(x, meaning(RHIZOPUS, i, RHIZOPUS_CUTS, 8)) for i, x in enumerate('AB')], asked)


def skin_labels(asked=None):
    return labels([(x, meaning(SKIN, i, SKIN_CUTS, 10)) for i, x in enumerate('ABC')], asked)


def gut_labels(asked=None):
    # The scheme names A, B and C; D (asked about in (v)) is never named.
    return labels([(x, S(GUT[x], page=10, piece=2, psep=' = ')) for x in 'ABC'], asked)


TASKS = [
    # ------------------------------------------------------------ Section A --
    # Each question one whole card at 20: see the docstring and WHOLE_A.
    T('1', 'Q1', 'A',
      [M('(a)', 2), Q(2, 'What food in the student’s lunch is:'),
       M('(i)', 2, br=True), blank(2, 'a good source of protein?'),
       M('(ii)', 2, br=True), blank(2, 'a good source of fat?'),
       M('(b)', 2, br=True), Q(2, 'Vitamins form part of a healthy diet and prevent many disorders.'),
       M('(i)', 2, br=True), ask(2, 'Name one water-soluble vitamin.'),
       M('(ii)', 2, br=True), ask(2, 'Suggest one food in the lunch that contains the water-soluble vitamin you have named.'),
       M('(c)', 2, br=True), ask(2, 'Name one structural protein in humans.'),
       M('(d)', 2, br=True), ask(2, 'Give one function of fat in the human body.'),
       M('(e)', 2, br=True), ask(2, 'What term is used to describe all the chemical reactions in the human body?')],
      [pt(S('Tuna', after=H1), 0, label=S('(a)', '(i)', after=H1)),
       pt(S(CRISPS, after=H1, piece=1), 0, label=S('(ii)', after=H1)),
       pt(S(CRISPS, after=H1, piece=[2, 1], psep=['/', ' [']), 0, label=S('(ii)', after=H1),
          note_sel=S(CRISPS, after=H1, piece=[2, 2, 1], psep=['/', ' [', ']'])),
       pt(S('B or C', after=H1), 0, label=S('(b)', '(i)', after=H1)),
       *[pt(S(BREAD, after=H1, piece=k), 0, label=S('(ii)', after=H1, nth=2)) for k in (1, 2)],
       *[pt(S(PROTEIN, after=H1, piece=k), 0, label=S('(c)', after=H1)) for k in (1, 2, 3)],
       *[pt(S(*FAT, after=H1, piece=k), 0, label=S('(d)', after=H1)) for k in (1, 2, 3, 4, 5)],
       pt(S('Metabolism', after=H1), 0, label=S('(e)', after=H1))],
      'bio-1-2', 'food-and-nutrients', at(5, '1.', '(a)', why=WHOLE_ANCHOR), 20, stem=[Q1], tariff='questionTotal',
      decision=WHOLE_A.format(q=1, notation='2(1) + 3(2) + 2(6)', n='seven', low=1, high=6)
      + ' (a)(ii)\'s bracketed "[not „spread‟]" is its butter row\'s note.'),
    T('2', 'Q2', 'A',
      [M('(a)', 2), ask(2, 'Name the parts labelled A, B, C and D.'),
       M('(b)', 2, br=True), ask(2, 'State:'), ask(2, 'one function of part A.', br=True),
       ask(2, 'one function of part C.', br=True),
       M('(c)', 2, br=True), ask(2, 'Give one difference between a plant cell and an amoeba.')],
      [*[pt(cell(AMOEBA[0], i, AMOEBA_CUTS, end=AMOEBA[1]), 0) for i in range(4)],
       *[pt(S(FUNC_A, piece=[2, k], psep=[' = ', '/']), 0, label=S(FUNC_A, piece=1, psep=' = ')) for k in (1, 2)],
       *[pt(S(*FUNC_C, piece=[2, k], psep=[' = ', '/']), 0, label=S(*FUNC_C, piece=1, psep=' = '))
         for k in (1, 2, 3, 4)],
       pt(S('e.g. Plant Cell has Cell Wall'), 0, label=S('(c)', after=H2))],
      'bio-1-3', 'amoeba-structure', at(5, '2.', '(a)', why=WHOLE_ANCHOR), 20, stem=[Q2], fig='q2-amoeba',
      labels=amoeba_labels(), tariff='questionTotal',
      decision=WHOLE_A.format(q=2, notation='2(1) + 3(2) + 2(6)', n='seven', low=1, high=6)
      + ' (a) is read cell by cell at its printed letters; each label\'s alternatives ("Cytoplasm / Endoplasm") are '
        'one cell, one row. (b)\'s alternatives are each a row under the scheme\'s own "Function “A”" and "Function '
        '“C”".'),
    T('3', 'Q3', 'A',
      [Q3] + [x for letter, stmt in [
          ('a', 'The base Uracil is found in DNA.'), ('b', 'Chloroplasts contain DNA.'),
          ('c', 'The microscope lenses closest to the stage are the eyepiece lenses.'),
          ('d', 'Sodium alginate is used to immobilise enzymes.'), ('e', 'Plant cell walls are fully permeable.'),
          ('f', 'Animal cells do not have membranes.'), ('g', 'An organ is a group of systems.')]
          for x in (M(f'({letter})', 3, br=True), ask(3, stmt))],
      [pt(S(ans, after=H3, nth=nth), 0, label=S(f'({x})', after=H3)) for x, ans, nth in TF],
      'bio-1-3', 'cells-and-biomolecules-true-or-false', at(5, '3.', '(a)', why=WHOLE_ANCHOR), 20,
      tariff='questionTotal',
      decision=WHOLE_A.format(q=3, notation='2(1) + 3(2) + 2(6)', n='seven', low=1, high=6)
      + ' The scheme prints each answer as the letter T or F; for (b) it prints "T or F", either earning the point.'),
    T('4', 'Q4', 'A',
      [M('(a)', 3), ask(3, 'Does the diagram represent a root or a stem?'),
       M('(b)', 3, br=True), Q(3, 'The letters A, B, C in the diagram, represent three different tissue types.'),
       Q(3, 'Match each letter with its correct tissue type in the following list:'),
       ask(3, 'Ground tissue.', br=True), ask(3, 'Dermal tissue.', br=True), ask(3, 'Vascular tissue.', br=True),
       M('(c)', 3, br=True), ask(3, 'State a function of vascular tissue.'),
       M('(d)', 3, br=True), ask(3, 'Name the two types of vascular tissue in plants.')],
      [pt(S('Stem'), 0, label=S('(a)', after=H4)),
       pt(S('Ground Tissue = A;', piece=1, psep=';'), 0), pt(S('Dermal Tissue = C;', piece=1, psep=';'), 0),
       pt(S('Vascular Tissue = B'), 0),
       *[pt(S('Transport / Support', piece=k), 0, label=S('(c)', after=H4)) for k in (1, 2)],
       pt(S('Xylem'), 0, label=S('(d)', '1.', after=H4)), pt(S('Phloem'), 0, label=S('2.', after=H4))],
      'bio-2-6', 'tissues-of-a-stem', at(5, '4.', '(a)', why=WHOLE_ANCHOR), 20, stem=[Q4], fig='q4-section',
      labels=section_labels(), tariff='questionTotal',
      decision=WHOLE_A.format(q=4, notation='2(1) + 3(2) + 2(6)', n='seven', low=1, high=6)
      + ' (b) prints each tissue type with its letter ("Ground Tissue = A;"), cut at its own semicolon.'),
    T('5', 'Q5', 'A',
      Q5 + [x for letter, desc in [
          ('a', 'Any harmful addition to the ecosystem.'), ('b', 'A problem associated with waste disposal.'),
          ('c', 'A way to minimise waste.'), ('d', 'Wise management of an ecosystem.'),
          ('e', 'A possible cause of pollution.')]
          for x in (M(f'({letter})', 4, br=True), ask(4, desc))],
      [pt(S(ans), 0, label=S(f'({x})', after=H5)) for x, ans in [
          ('a', 'Pollution'), ('b', 'Smell'), ('c', 'Recycle'), ('d', 'Conservation'), ('e', 'Burning Fuel')]],
      'bio-3-1', 'ecology-terms', at(5, '5', '(a)', why=WHOLE_ANCHOR), 20, qfig='q5-table', tariff='questionTotal',
      decision=WHOLE_A.format(q=5, notation='3(2) + 2(7)', n='five', low=2, high=7)
      + ' The list of terms (its "Niche" struck through as the worked example) and the table are shown as the '
        'question\'s own print.'),
    T('6', 'Q6', 'A',
      [ask(4, 'Complete the blank spaces below.'), Q(4, 'Genotypes of parents (Tt) × (tt)', br=True),
       M('(a)', 4, br=True), Q(4, 'Possible gametes'), Q(4, '( ) ( ) × ( )'),
       M('(b)', 4, br=True), Q(4, 'Genotypes of offspring ( ) ( )'),
       M('(c)', 4, br=True), Q(4, 'Phenotypes of offspring')],
      [*[pt(S(GAMETES, piece=p, psep=[': ', ' X ', ' '][:len(p)]), 0, label=S(GAMETES, piece=1, psep=': '))
         for p in ([2, 1, 1], [2, 1, 2], [2, 2])],
       *[pt(S(OFFSPRING, piece=[2, k], psep=[': ', ' ']), 0, label=S(OFFSPRING, piece=1, psep=': ')) for k in (1, 2)],
       pt(S(PHENOTYPES, piece=[2, 1], psep=[': ', ' & ']), 0, label=S(PHENOTYPES, piece=1, psep=': ')),
       pt(S(PHENOTYPES, piece=[2, 2, 1], psep=[': ', ' & ', ' (']), 0, label=S(PHENOTYPES, piece=1, psep=': '),
          note_sel=S(PHENOTYPES, piece=[2, 2, 2, 1], psep=[': ', ' & ', ' (', ')']))],
      'bio-1-4', 'monohybrid-cross-tall-and-dwarf', at(5, '6.', '(a)', why=WHOLE_ANCHOR), 20, stem=Q6,
      tariff='questionTotal',
      decision=WHOLE_A.format(q=6, notation='2(1) + 3(2) + 2(6)', n='seven', low=1, high=6)
      + ' The gametes ("(3pts)"), offspring genotypes ("(2pts)") and phenotypes ("(2pts)") are each cut at the '
        'printed spaces, "X" and "&"; "(allow small)" is the dwarf row\'s note.'),
    # ------------------------------------------------------------ Section B --
    T('7ai', 'Q7(a)(i)', 'B', Q7AI, [anyn(eg('e.g. Asthma'), 1, 5, open_list=True)], 'bio-2-6', 'breathing-disorder',
      at(6, '7.', '(a)', '(i)'), 5, decision='"5 + 1" over (a)\'s two points, each carded at its first rate. ' + EG_OPEN),
    T('7aii', 'Q7(a)(ii)', 'B', ask(5, 'Give one possible treatment for the disorder referred to above.'),
      [anyn(None, 1, 5, options=[S(INHALER, piece=[2, 1], psep=['e.g. ', ' ('])], open_list=True,
            note_sel=S(INHALER, piece=[2, 2, 1], psep=['e.g. ', ' (', ')']))],
      'bio-2-6', 'treating-a-breathing-disorder', at(6, '7.', '(a)', '(ii)'), 5, stem=[M('(i)', 5), Q7AI],
      decision=EG_OPEN + ' Its bracketed "must match" is the row\'s note.'),
] + [
    T(f'7b{r}', f'Q7(b)({r})', 'B', q, rows, 'bio-2-6', concept, at(6, '7.', '(b)', f'({r})'), 6 * len(rows),
      stem=stem, decision=decision)
    for r, q, rows, concept, stem, decision in [
        ('i', Q(5, 'The investigation starts by measuring the resting rate. How did you measure the resting rate?'),
         [pt(S(RESTING, piece=1), 6), pt(S(RESTING, piece=2), 6), pt(S('repeat or average'), 6)],
         'measuring-resting-rate', Q7B,
         'Three points: "Count pulse or breaths / time or rate" ("(2 pts)"), cut at the scheme\'s own solidus, and '
         '"repeat or average" ("(1 pt)"), a row each, each on the "2(6)+6(2)" ladder at its first rate. The scheme\'s '
         '"Ticking Breathing Rate/Pulse Rate (0 pts)" earns nothing.'),
        ('ii', ask(5, 'After measuring your resting rate, what other steps did you carry out to complete the investigation?'),
         [pt(S('Exercise / check rate', piece=k), 6) for k in (1, 2)], 'exercise-and-rate-steps', Q7B,
         TWO_POINTS.format(n=2) + ' Cut at the scheme\'s own solidus.'),
        ('iii', ask(5, 'What was the result of your investigation?'), [pt(S('Exercise causes increase in rate'), 6)],
         'effect-of-exercise-on-rate', Q7B, ''),
        ('iv', Q7BIV, [anyn(S('Yes / No'), 1, 6)], 'fit-and-unfit-people', Q7B,
         'One point ("(1 pt)"): the scheme prints "Yes / No", either answer earning the point (its (v) "Must match '
         '(iv)"): a menu, claim one.'),
        ('v', ask(5, 'Give a reason for your answer.'),
         [pt(S('Must match (iv)'), 6, kind='criterion', note=NO_ANSWER)], 'reason-fit-and-unfit', Q7B + [M('(iv)', 5),
                                                                                                        Q7BIV],
         'One point ("(1 pt)") for the scheme\'s "Must match (iv)", what earns it: one criterion row.')]
] + [
    T('8ai', 'Q8(a)(i)', 'B', Q8AI, [pt(S('A biological or organic or protein catalyst.'), 5)], 'bio-2-1', 'enzyme',
      at(6, '8. (a)', '(i)'), 5, decision='"5 + 1" over (a)\'s two points, each carded at its first rate.'),
    T('8aii', 'Q8(a)(ii)', 'B', ask(6, 'On what structures in the cytoplasm are enzymes made?'), [pt(S('Ribosome'), 5)],
      'bio-2-1', 'where-enzymes-are-made', at(6, '8. (a)', '(ii)'), 5, stem=[M('(i)', 6), Q8AI]),
] + [
    T(f'8b{r}', f'Q8(b)({r})', 'B', q, rows, 'bio-2-1', concept, at(6, '8. (a)', '(b)', f'({r})'), total, stem=[Q8B],
      decision=decision)
    for r, q, rows, concept, total, decision in [
        ('i', ask(6, 'What enzyme did you use?'), [anyn(eg('e.g. Catalase'), 1, 6, open_list=True)],
         'enzyme-used', 6, EG_OPEN),
        ('ii', ask(6, 'What substrate did you use?'),
         [anyn(None, 1, 6, options=[S(PEROXIDE, piece=[2, 1], psep=['e.g. ', ' ('])], open_list=True,
               note_sel=S(PEROXIDE, piece=[2, 2, 1], psep=['e.g. ', ' (', ')']))], 'substrate-used', 6,
         EG_OPEN + ' Its bracketed "Must match enzyme" is the row\'s note.'),
        ('iii', blank(6, 'How did you vary the temperature during the investigation?'), [pt(S('Waterbath'), 6)],
         'varying-temperature', 6, ''),
        ('iv', ask(6, 'How did you measure the rate of enzyme activity?'),
         [anyn(None, 2, 6, options=[S(*FROTH, piece=[2, 1], psep=['e.g. ', ' / ']),
                                    S(*FROTH, piece=[2, 2, 1], psep=['e.g. ', ' / ', ' ('])], open_list=True,
               note_sel=S(*FROTH, piece=[2, 2, 2, 1], psep=['e.g. ', ' / ', ' (', ')']))],
         'measuring-enzyme-activity', 12,
         'Two points ("(2 pts)"): the scheme\'s example "Volume of froth / time", cut at its own solidus, claim both; '
         'its bracketed "Depends on enzyme used" is the row\'s note and its "e.g." makes the menu open.'),
        ('v', Q(6, 'During this investigation pH was kept constant. How did you keep the pH constant?'),
         [pt(S('Buffer'), 6)], 'keeping-ph-constant', 6, ''),
        ('vi', ask(6, 'What was the result of your investigation?'),
         [anyn(S(*TEMP_RESULT), 2, 6, note_sel=S('(Can be shown by graph with one axis', 'labelled)'))],
         'effect-of-temperature-on-enzymes', 12,
         'Two points ("(2 pts)") from the three results the scheme prints, cut at its own solidus: a menu, claim two; '
         'its bracketed "(Can be shown by graph with one axis labelled)" is the row\'s note.')]
] + [
    T('9a', 'Q9(a)', 'B', ask(7, 'Give two reasons why water is important for all living organisms.'),
      [anyn(None, 2, 5, options=[eg('e.g. Water is a good solvent.'), eg('e.g. Water maintains its temperature well')],
            open_list=True)], 'bio-1-2', 'importance-of-water', at(6, '9. (a)', '(i)'), 10,
      decision='"5+1" over the two reasons, carded at its first rate. The scheme prints one example reason under each '
               'of (i) and (ii) (the paper\'s two answer lines), each after "e.g.": an open menu, claim two.'),
] + [
    T(f'9b{r}', f'Q9(b)({r})', 'B', q, [row], 'bio-1-2', concept, sq, 6, stem=stem, decision=decision)
    for r, q, row, concept, sq, stem, decision in [
        ('i', Q9BI, pt(S('Iodine (solution)'), 6), 'test-for-starch', at(6, '9. (a)', '(b)', '(i)'), [Q9B], ''),
        ('ii', ask(7, 'Was heat necessary for this test?'), pt(S('No'), 6), 'heat-and-the-starch-test',
         at(6, '9. (a)', '(b)', '(ii)'), [Q9B, M('(i)', 7), Q9BI], ''),
        ('iii', ask(7, 'How did you know that starch was present?'), pt(S('Blue/Black colour'), 6),
         'positive-starch-test', at(6, '9. (a)', '(b)', '(iii)'), [Q9B, M('(i)', 7), Q9BI],
         'One point ("(1 pt)"): "Blue/Black colour" is the one colour, read whole.'),
        ('iv', ask(7, 'What control did you use in this test?'), pt(S('Water instead of starch'), 6),
         'starch-test-control', welded(6, '9. (a)', '(b)', '(iv)'), [Q9B, M('(i)', 7), Q9BI], ''),
        ('v', Q9BV, pt(S('Biuret (solution) or named chemicals'), 6), 'test-for-protein',
         at(6, '9. (a)', '(b)', '(v)'), [Q9B], ''),
        ('vi', ask(7, 'What was the initial colour of the protein-testing solution before you put it on the food?'),
         pt(S('Blue'), 6), 'biuret-colour-before', at(6, '9. (a)', '(b)', '(vi)'), [Q9B, M('(v)', 7), Q9BV], ''),
        ('vii', ask(7, 'Was heat necessary for this test?', nth=2), pt(S('No'), 6), 'heat-and-the-protein-test',
         at(6, '9. (a)', '(b)', '(vii)'), [Q9B, M('(v)', 7), Q9BV], ''),
        ('viii', ask(7, 'What colour indicated that protein was present in the food?'),
         anyn(S('Purple / violet / Pink'), 1, 6), 'positive-protein-test', welded(6, '9. (a)', '(b)', '(viii)'),
         [Q9B, M('(v)', 7), Q9BV], 'One point ("(1 pt)"), any one of the printed colours: a menu, claim one.')]
] + [
    # ------------------------------------------------------------ Section C --
    T('10a', 'Q10(a)', 'C', Q(8, 'Using organisms from the ecosystem you have studied, draw a pyramid of numbers to show '
                                 'at least three', 'feeding levels.'),
      [pt(S('Correct shape -', piece=1, psep=' -'), 3, kind='criterion',
          note='(The scheme\'s example pyramid is shown after reveal.)'),
       pt(S('One Ecosystem'), 3, kind='criterion'), pt(S('Food chain', 'Food chain'), 3, kind='criterion')],
      'bio-3-1', 'pyramid-of-numbers', at(7, '10', '(a)'), 9, fig='q10a-scheme',
      decision='"3(3)": three points at 3, each the scheme\'s own criterion ("Correct shape - 3", "One Ecosystem 3", '
               '"Food chain 3"), a criterion row each. The scheme prints an example pyramid (Fox, Rabbit, Grass; '
               'Carnivore, Herbivore, Producer), shown as the answer figure.'),
    T('10bi', 'Q10(b)(i)', 'C', Q10BI,
      [pt(S('Biotic – concerned with the activities of living things'), 6),
       pt(S('Abiotic – concerned with the non-living part of the', 'environment'), 6)],
      'bio-3-1', 'biotic-and-abiotic-factors', at(7, '10', '(b)', '(i)'), 12, qfig='q10bi-ask',
      decision=TWO_POINTS.format(n=2) + ' One per underlined word, each on its own printed line, on the "2(6) + 6(2) '
               '+3(1)" ladder at its first rate. The ask is shown as printed: its underlining names the two words.'),
    T('10bii', 'Q10(b)(ii)', 'C', Q(8, 'Name any two abiotic factors from an ecosystem you have studied and describe how '
                                       'you measured', 'each one.'),
      [pt(S(ABIOTIC[0], piece=[2, 1], psep=['• ', ' – ']), 6,
          note='The scheme prints these after "e.g.": examples, not a closed list.'),
       pt(S(ABIOTIC[0], piece=[2, 2], psep=['• ', ' – ']), 6),
       pt(S(ABIOTIC[1], piece=[2, 1], psep=['• ', ' – ']), 6), pt(S(ABIOTIC[1], piece=[2, 2], psep=['• ', ' – ']), 6)],
      'bio-3-1', 'measuring-abiotic-factors', at(7, '10', '(b)', '(ii)'), 24,
      decision='Four points ("(4 pts)"): the scheme\'s two example factors, each with how it was measured ("Temperature '
               '– thermometer", "Soil pH – pH meter"), each factor and each method its own row, cut at the printed '
               'dash.'),
] + [
    T(f'10biii-{x.lower()}', 'Q10(b)(iii)', 'C', Q10BIII, [pt(cell(KEY, i, KEY_CUTS), 6)], 'bio-3-1', concept,
      at(7, '10', '(b)', '(iii)'), 6, qfig='q10b-key', item=(x.lower(), x), labels=key_labels(x),
      decision=EACH_ITEM + ' "(3 pts)" over the three animals. The key and the drawings are shown as the question\'s '
                           'own print.')
    for i, (x, concept) in enumerate([('A', 'keying-tribolium'), ('B', 'keying-planarian'), ('C', 'keying-nematode')])
] + [
    T('10biv1', 'Q10(b)(iv)1', 'C', Q10BIV1,
      [anyn(None, 1, 6, options=[S(ADAPTED, piece=[2, 1], psep=['e.g. 1. ', ' 2. '])], open_list=True)],
      'bio-3-1', 'animal-from-an-ecosystem', at(7, '10', '(b)', '(iv)'), 6, stem=[Q10BIV],
      decision=EACH_ITEM + ' "(2 pts)", one per numbered item. ' + EG_OPEN),
    T('10biv2', 'Q10(b)(iv)2', 'C', [M('2.', 8), ask(8, 'Describe one way in which it is adapted to its habitat.')],
      [anyn(None, 1, 6, options=[S(ADAPTED, piece=[2, 2], psep=['e.g. 1. ', ' 2. '])], open_list=True)],
      'bio-3-1', 'adaptation-to-habitat', at(7, '10', '(b)', '(iv)'), 6, stem=[Q10BIV] + Q10BIV1,
      decision=EACH_ITEM + ' ' + EG_OPEN + ' The adaptation printed is the example animal\'s (a grasshopper\'s).'),
    T('10ci', 'Q10(c)(i)', 'C',
      ask(8, 'Distinguish between a quantitative and a qualitative survey by writing a sentence about each.'),
      [pt(S('Quantitative survey - The number of individuals present'), 6),
       pt(S('Qualitative survey – Variety of organisms present'), 6)],
      'bio-3-1', 'quantitative-and-qualitative-surveys', at(7, '10', '(c)', '(i)'), 12,
      decision=TWO_POINTS.format(n=2) + ' One per survey, each on its own printed line, on the "2(6)+6(2)" ladder at '
                                        'its first rate.'),
    T('10cii1', 'Q10(c)(ii)1', 'C', Q10CII1, [anyn(S('e.g. 1. Daisy', piece=2, psep='e.g. 1. '), 1, 6, open_list=True)],
      'bio-3-1', 'plant-from-an-ecosystem', at(7, '10', '(c)', '(ii)'), 6,
      decision=EACH_ITEM + ' "(1 pt)". ' + EG_OPEN),
    T('10cii2', 'Q10(c)(ii)2', 'C',
      [M('2.', 8), ask(8, 'Describe how you carried out a quantitative survey to determine its frequency.')],
      [pt(S(QUADRAT, piece=1), 6), pt(S(QUADRAT, piece=2), 6), pt(S('random or repeat or calculate or scale up'), 6)],
      'bio-3-1', 'quantitative-survey-of-a-plant', at(7, '10', '(c)', '(ii)'), 18, stem=Q10CII1,
      decision=EACH_ITEM + ' Three points: "Throw quadrat / note if daisies present /" ("(2 pts)"), cut at the '
                           'scheme\'s own solidus, and "random or repeat or calculate or scale up" ("(1pt)"), one point '
                           'with its printed alternatives.'),
    T('10ciii', 'Q10(c)(iii)', 'C', Q(8, 'As a result of pollution, a species of plant disappears from an ecosystem.',
                                       'and animals living in the area.'),
      [pt(S(*EFFECTS, piece=1, psep=' ('), 12, units=[6, 6],
          note_sel=S(*EFFECTS, piece=[2, 1], psep=[' (', ')']))],
      'bio-3-1', 'effects-of-losing-a-plant-species', at(7, '10', '(c)', '(iii)'), 12,
      decision='Two points ("(2 pts)") for the scheme\'s one printed line, "Plants and/or animal numbers increase and '
               '/or decrease", the two effects it allows (its solidi sit inside "and/or", not between two answers): '
               'one row worth both points; its bracketed "valid examples allowed" is the row\'s note.'),
    T('11ai', 'Q11(a)(i)', 'C', Q11AI,
      [pt(S(*HAPLOID, piece=2, psep=' = '), 6, label=S(*HAPLOID, piece=1, psep=' = '))], 'bio-2-3', 'haploid',
      at(7, '11 (a)', '(i)'), 6, decision='"6 + 3" over (a)\'s two points, each carded at its first rate.'),
    T('11aii', 'Q11(a)(ii)', 'C', ask(9, 'What is a chromosome?'),
      [pt(S(*CHROMOSOME, piece=2, psep=' = '), 6, label=S(*CHROMOSOME, piece=1, psep=' = '))], 'bio-1-4', 'chromosome',
      at(7, '11 (a)', '(ii)'), 6),
] + [
    T(f'11b{r}', f'Q11(b)({r})', 'C', q, rows, topic, concept, at(7, '11 (a)', '(b)', f'({r})'), 5 * len(rows),
      stem=Q11B, fig='q11-rabbit', decision=decision)
    for r, q, rows, topic, concept, decision in [
        ('i', ask(9, 'What are the main characteristics of albinism?'),
         [pt(S('White or lack of pigment / skin or fur'), 5), pt(S('Pink or lack of pigment / eyes'), 5)],
         'bio-1-4', 'characteristics-of-albinism',
         'Two points ("(2 pts)"), one per printed line: each line one characteristic (its colour, its part of the '
         'body), each on the "2(5) + 3+7(2)" ladder at its first rate.'),
        ('ii', ask(9, 'What is meant by the term recessive gene?'),
         [pt(S('Only expressed in homozygous state or not dominant'), 5)], 'bio-1-4', 'recessive-gene', ''),
        ('iii', ask(9, 'What is a mutation?'), [pt(S(*MUTATION, piece=k), 5) for k in (1, 2)], 'bio-2-3', 'mutation',
         TWO_POINTS.format(n=2) + ' Cut at the scheme\'s own solidus.')]
] + [
    T(f'11biv{n}', f'Q11(b)(iv){n}', 'C', ask(9, q), [row], 'bio-1-5', concept, at(7, '11 (a)', '(b)', '(iv)'), 5,
      stem=Q11B + [Q11BIV] + stem, fig='q11-rabbit', decision=EACH_ITEM + ' "(3 pts)", one per numbered item.' + extra)
    for n, q, row, concept, stem, extra in [
        (1, '1. What is meant by evolution?',
         pt(S('Change in a species (over time) or (reference to)', 'natural selection'), 5), 'evolution', [], ''),
        (2, '2. Name one of the scientists who first explained how evolution occurs by natural selection.',
         pt(S('Darwin or Wallace'), 5), 'darwin-and-wallace', [], ''),
        (3, '3. Give one source of evidence for evolution.', anyn(eg('e.g. Fossils'), 1, 5, open_list=True),
         'evidence-for-evolution', [], ' ' + EG_OPEN)]
] + [
    T('11bv', 'Q11(b)(v)', 'C', Q(9, 'People with albinism should always apply a high-factor sunscreen when going '
                                     'outdoors and must avoid', 'strong sunshine. Suggest a reason for these precautions.'),
      [pt(S(SUNSCREEN, piece=k), 5) for k in (1, 2)], 'bio-1-4', 'albinism-and-sunlight',
      at(7, '11 (a)', '(b)', '(v)'), 10, stem=Q11B, fig='q11-rabbit',
      decision=TWO_POINTS.format(n=2) + ' Cut at the scheme\'s own solidus.'),
    T('11ci', 'Q11(c)(i)', 'C', Q11CI, [pt(S(*GE, piece=k), 6) for k in (1, 2, 3)], 'bio-3-3', 'genetic-engineering',
      at(7, '11 (a)', '(c)', '(i)'), 18,
      decision='Three points ("3(pts)", as printed) cut at the scheme\'s own solidus, each on the "2(6)+6(2)" ladder '
               'at its first rate.'),
    T('11cii', 'Q11(c)(ii)', 'C', ask(9, 'List three of the main procedures used in genetic engineering.'),
      [anyn(None, 3, 6, options=[S(*PROCEDURES, piece=k) for k in (1, 2, 3, 4, 5)]
            + [S(*PROCEDURES, piece=[6, 1], psep=['/', ' ('])],
            note_sel=S(*PROCEDURES, piece=[6, 2, 1], psep=['/', ' (', ')']))],
      'bio-3-3', 'procedures-in-genetic-engineering', at(7, '11 (a)', '(c)', '(ii)'), 18,
      decision='Three points ("(3 pts)") from the six printed procedures, cut at the scheme\'s own solidus: a menu, '
               'claim three; its bracketed "Name or explain" is the row\'s note.'),
    T('11ciii', 'Q11(c)(iii)', 'C', ask(9, 'Give two examples of how genetic engineering is used.'),
      [anyn(None, 2, 6, options=[S(GE_USES, piece=[2, k], psep=['EG. ', ' / ']) for k in (1, 2)], open_list=True)],
      'bio-3-3', 'uses-of-genetic-engineering', at(7, '11 (a)', '(c)', '(iii)'), 12,
      decision='Two points ("(2 Pts)"): the scheme\'s two examples after its "EG.", an open menu, claim two.'),
    T('12ai', 'Q12(a)(i)', 'C', Q12AI, [pt(S(SEXUAL, piece=k, psep=' & '), 3) for k in (1, 2)], 'bio-2-5',
      'types-of-reproduction', at(8, '12', '(a)', '(i)'), 6,
      decision=TWO_POINTS.format(n=2) + ' Cut at the scheme\'s own "&"; each on the "2(3)+3(1)" ladder at its first '
                                        'rate.'),
    T('12aii', 'Q12(a)(ii)', 'C', ask(10, 'Explain the term fertilisation.'),
      [pt(S(FERTILISATION, piece=k), 3) for k in (1, 2, 3)], 'bio-2-5', 'fertilisation', at(8, '12', '(a)', '(ii)'), 9,
      decision='Three points ("(3 pts)"), cut at the scheme\'s own solidus.'),
] + [
    T(f'12b{r}', f'Q12(b)({r})', 'C', ask(10, q), [row], 'bio-2-5', concept, at(8, '12', '(b)', f'({r})'), total,
      stem=[Q12B], decision=decision)
    for r, q, row, concept, total, decision in [
        ('i', 'What part of the flower produces pollen?', pt(S('The anther or stamen'), 5), 'anther', 5,
         'One point on the "3(5) +6(2)" ladder, at its first rate.'),
        ('ii', 'After fertilisation, what part of the flower becomes the fruit?',
         pt(S(OVARY, piece=1, psep=' ('), 5, note_sel=S(OVARY, piece=[2, 1], psep=[' (', ')'])), 'ovary-becomes-fruit',
         5, 'Its bracketed "accept carpel" is the row\'s note.'),
        ('iii', 'Give two methods of seed dispersal in plants.',
         anyn(None, 2, 5, options=[egs(DISPERSAL, k) for k in (1, 2)], open_list=True), 'seed-dispersal', 10,
         'Two points ("(2 pts)"): the scheme\'s two examples after its "e.g.", an open menu, claim two.'),
        ('iv', 'Why is it necessary for plants to disperse their seeds?',
         pt(S('To avoid competition or to avail of suitable conditions'), 5), 'why-disperse-seeds', 5, ''),
        ('v', 'What is the advantage of dormancy to seeds?', pt(S('To overcome adverse conditions'), 5),
         'advantage-of-dormancy', 5, ''),
        ('vi', 'Give three conditions necessary for seeds to germinate.', anyn(S(GERMINATION), 3, 5),
         'conditions-for-germination', 15,
         'Three points ("(3 Pts)"): the three conditions the scheme prints, cut at its own solidus, claim all three.')]
] + [
    T(f'12ci-{x.lower()}', 'Q12(c)(i)', 'C', ask(10, 'Name the parts labelled A, B and C.'),
      [pt(cell(SPERM, i, SPERM_CUTS), 4)], 'bio-2-5', concept, at(8, '12', '(c)', '(i)'), 4, stem=[Q12C],
      fig='q12-sperm', item=(x.lower(), x), labels=sperm_labels(x),
      decision=EACH_ITEM + ' "(3 Pts)" over the three labels, each on the "3(4) + 6(2)" ladder at its first rate.')
    for i, (x, concept) in enumerate([('A', 'sperm-head'), ('B', 'sperm-nucleus'), ('C', 'sperm-tail')])
] + [
    T(f'12c{r}', f'Q12(c)({r})', 'C', ask(10, q), [row], 'bio-2-5', concept, at(8, '12', '(c)', f'({r})'), total,
      stem=[Q12C] if fig else [], fig=fig, decision=decision)
    for r, q, row, concept, total, fig, decision in [
        ('ii', 'What is the function of the midpiece of the sperm?', pt(S('Respiration or to produce energy'), 4),
         'function-of-the-midpiece', 4, 'q12-sperm', ''),
        ('iii', 'Name the hormone responsible for sperm production.', pt(S('Testosterone'), 4), 'testosterone', 4,
         None, ''),
        ('iv', 'Give one cause of infertility in men.', anyn(eg('e.g. Low sperm counts'), 1, 4, open_list=True),
         'male-infertility', 4, None, EG_OPEN),
        ('v', 'Explain the term contraception.', pt(S('Prevention of fertilisation or prevention of pregnancy'), 4),
         'contraception', 4, None, ''),
        ('vi', 'Name two methods of contraception.',
         anyn(None, 2, 4, options=[egs(CONTRACEPTION, 1), S(CONTRACEPTION, piece=[2, 2, 1], psep=['e.g. ', ' / ', ' or '])],
              open_list=True, note_sel=S(CONTRACEPTION, piece=[2, 2], psep=['e.g. ', 'Mechanical '])),
         'methods-of-contraception', 8, None,
         'Two points ("(2 pts)"): the scheme\'s "e.g. Natural / Mechanical or examples", its two methods a menu, claim '
         'two, open; its closing "or examples" is the row\'s note.')]
] + [
    T('13ai', 'Q13(a)(i)', 'C', ask(11, 'Suggest one advantage of classifying organisms.'),
      [anyn(eg('e.g. Identification'), 1, 7, open_list=True)], 'bio-3-2', 'why-classify', at(8, '13', '(a)', '(i)'), 7,
      stem=[Q13A], decision='"7 + 2(1)" over (a)\'s three points, each carded at its first rate. ' + EG_OPEN),
    T('13aii', 'Q13(a)(ii)', 'C', ask(11, 'Name the kingdom to which bacteria belong.'), [pt(S('Monera'), 7)], 'bio-3-2',
      'monera', at(8, '13', '(a)', '(ii)'), 7, stem=[Q13A]),
    T('13aiii', 'Q13(a)(iii)', 'C', ask(11, 'Give one example of the economic importance of bacteria.'),
      [anyn(eg('e.g. Food Production'), 1, 7, open_list=True)], 'bio-3-2', 'economic-importance-of-bacteria',
      at(8, '13', '(a)', '(iii)'), 7, stem=[Q13A], decision=EG_OPEN),
    T('13bi', 'Q13(b)(i)', 'C', ask(11, 'Draw a large labelled diagram of a typical bacterial cell.'),
      [pt(S('Cell Memb/Cytoplasm + one other.'), 5, kind='criterion', label=S('Diagram to include:'),
          note_sel=S('Diagram:', 'Two absent = 0')),
       pt(S('Labels: Any two valid labels'), 2, kind='criterion', units=[1, 1], note=NO_ANSWER)],
      'bio-3-2', 'drawing-a-bacterial-cell', at(8, '13', '(b)', '(i)'), 7,
      decision=DRAWING.format(tariff='D. 5,2,0 L.2(1)') + ' The scheme names no label: "Any two valid labels" is one '
                                                          'criterion row worth its two 1s.'),
] + [
    T(f'13b{r}', f'Q13(b)({r})', 'C', q, [row], 'bio-3-2', concept, at(8, '13', '(b)', f'({r})'), total,
      decision=decision)
    for r, q, row, concept, total, decision in [
        ('ii', Q(11, 'Bacteria may be classified by their shape.', 'Name any two bacterial shapes.'),
         anyn(S(*SHAPES), 2, 6), 'bacterial-shapes', 12,
         'Two points ("(2 pts)") from the three shapes the scheme prints, cut at its own solidus: a menu, claim two, '
         'each on the "2(6) + 4(2)" ladder at its first rate.'),
        ('iii', ask(11, 'Name the method by which bacteria reproduce.'),
         pt(S(FISSION, piece=1, psep=' ['), 6, note_sel=S(FISSION, piece=[2, 1], psep=[' [', ']'])), 'binary-fission',
         6, 'Its bracketed "Not Mitosis" is the row\'s note.'),
        ('iv', ask(11, 'What are pathogenic bacteria?'), pt(S('Disease-causing'), 6), 'pathogenic-bacteria', 6, ''),
        ('v', ask(11, 'State two factors affecting the growth of bacteria.'), anyn(S(GROWTH), 2, 6),
         'factors-affecting-bacterial-growth', 12,
         'Two points ("(2 pts)") from the six factors the scheme prints, cut at its own solidus: a menu, claim two.')]
] + [
    T(f'13ci-{x.lower()}', 'Q13(c)(i)', 'C', ask(11, 'Name the parts labelled A and B.'),
      [pt(cell(RHIZOPUS, i, RHIZOPUS_CUTS), 7)], 'bio-3-2', concept, at(8, '13', '(c)', '(i)'), 7, stem=[Q13C],
      fig='q13-rhizopus', item=(x.lower(), x), labels=rhizopus_labels(x),
      decision=EACH_ITEM + ' "(2 pts)" over the two labels, cut at the scheme\'s own semicolon, each on the "2(7) '
                           '+5(2)" ladder at its first rate.')
    for i, (x, concept) in enumerate([('A', 'stolon'), ('B', 'rhizoid')])
] + [
    T(f'13c{r}', f'Q13(c)({r})', 'C', ask(11, q), [row], 'bio-3-2', concept, at(8, '13', '(c)', f'({r})'), total,
      stem=[Q13C] if fig else [], fig=fig, labels=lab, decision=decision)
    for r, q, row, concept, total, fig, lab, decision in [
        ('ii', 'Give two functions of structure B.', anyn(S(RHIZOID), 2, 7), 'functions-of-rhizoids', 14,
         'q13-rhizopus', rhizopus_labels('B'),
         'Two points ("(2 Pts)") from the three functions the scheme prints, cut at its own solidus: a menu, claim '
         'two.'),
        ('iii', 'Describe the role of part C in the reproduction of Rhizopus.',
         pt(S('(Release or production of) spores'), 7), 'role-of-the-sporangium', 7, 'q13-rhizopus', rhizopus_labels(),
         'The scheme never names C (it names A and B): the label key carries those two, neither asked here.'),
        ('iv', 'What is meant by saprophytic nutrition?', pt(S('Living on dead matter'), 7), 'saprophytic-nutrition', 7,
         None, None, ''),
        ('v', 'Give one beneficial use of fungi.', anyn(eg('e.g. Antibiotic Production'), 1, 7, open_list=True),
         'beneficial-fungi', 7, None, None, EG_OPEN)]
] + [
    T('14ai', 'Q14(a)(i)', 'C', ask(12, 'What is meant by aerobic respiration?'),
      [pt(S(*AEROBIC, piece=k), 5) for k in (1, 2)], 'bio-2-2', 'aerobic-respiration', at(9, '14. (a)', '(i)'), 10,
      decision=TWO_POINTS.format(n=2) + ' Cut at the scheme\'s own solidus, each on the "2(5)+2(4)+4(1)" ladder at its '
                                        'first rate.'),
    T('14aii1', 'Q14(a)(ii)1', 'C', Q14AII1, [pt(S('Cytoplasm'), 5)], 'bio-2-2', 'stage-1-of-respiration',
      at(9, '14. (a)', '(ii)'), 5, stem=[Q14AII], decision=EACH_ITEM + ' "(2 pts)", one per numbered item.'),
    T('14aii2', 'Q14(a)(ii)2', 'C', [M('2.', 12), ask(12, 'Where in a cell does stage 2 occur?')],
      [pt(S('Mitochondria'), 5)], 'bio-2-2', 'stage-2-of-respiration', at(9, '14. (a)', '(ii)'), 5,
      stem=[Q14AII], decision=EACH_ITEM),
    T('14aiii', 'Q14(a)(iii)', 'C', ask(12, 'Which type of respiration, aerobic or anaerobic, produces more energy?'),
      [pt(S('Aerobic (Respiration)'), 5)], 'bio-2-2', 'aerobic-yields-more-energy', at(9, '14. (a)', '(iii)'), 5),
    T('14aiv', 'Q14(a)(iv)', 'C', Q14AIVD,
      [allof([(S('Diagram must include:'), S('• Container', piece=2, psep='• ')),
              (None, S('• Liquid', piece=2, psep='• ')), (None, S('• Oil or Airlock', piece=2, psep='• '))], 5,
             note_sel=S('Diagram:', 'Two absent = 0')),
       *[pt(S(f'• {w}', piece=2, psep='• ', nth=nth), 1, label=S('Labels required:'))
         for w, nth in (('Glucose', 1), ('Yeast', 1), ('Oil or Airlock', 2))]],
      'bio-2-2', 'drawing-a-fermentation-apparatus', at(9, '14. (a)', '(iv)'), 8, stem=[Q14AIV],
      decision=DRAWING.format(tariff='D. 5,2,0 L. 3(1)') + ' The scheme prints both lists side by side: "Diagram must '
               'include" (Container, Liquid, Oil or Airlock) is the diagram\'s row, its three items cut at their '
               'printed bullets; "Labels required" (Glucose, Yeast, Oil or Airlock) a row per label.'),
] + [
    T(f'14aiv{n}', f'Q14(a)(iv){n}', 'C', q, [pt(S(ans), 5)], 'bio-2-2', concept, at(9, '14. (a)', '(iv)'), 5,
      stem=[Q14AIV, Q14AIVD, Q14AIVQ] + stem, decision=EACH_ITEM + ' "(3 pts)", one per numbered item.')
    for n, q, ans, concept, stem in [
        (1, Q14AIV1, 'CO2', 'carbon-dioxide-from-fermentation', []),
        (2, Q14AIV2, 'Bubbles', 'detecting-carbon-dioxide', Q14AIV1),
        (3, [M('3.', 12), ask(12, 'How would you know when fermentation had finished?')], 'Bubbling stops',
         'end-of-fermentation', [])]
] + [
    T('14bi', 'Q14(b)(i)', 'C', ask(12, 'In leaf cells, which chemical traps light energy for photosynthesis?'),
      [pt(S('Chlorophyll'), 5)], 'bio-2-2', 'chlorophyll', at(9, '14.', '(b)', '(i)'), 5,
      decision='One point on the "2(5)+2(3)+7(2)" ladder, at its first rate.'),
    T('14bii', 'Q14(b)(ii)', 'C', Q(12, 'Water for photosynthesis enters the roots of plants by osmosis.',
                                     'What is meant by osmosis?'),
      [pt(S(*OSMOSIS, piece=k), 5) for k in (1, 2, 3)], 'bio-2-6', 'osmosis', at(9, '14.', '(b)', '(ii)'), 15,
      decision='Three points ("(3 pts)"), cut at the scheme\'s own solidus.'),
    T('14biii1', 'Q14(b)(iii)1', 'C', Q14BIII1, [pt(S(PRODUCTS, piece=k), 5) for k in (1, 2, 3)], 'bio-2-2',
      'products-of-splitting-water', at(9, '14.', '(b)', '(iii)'), 15, stem=[Q14BIII],
      decision=EACH_ITEM + ' Item 1 three points ("(3 pts)"), one per product, cut at the scheme\'s own solidus.'),
    T('14biii2', 'Q14(b)(iii)2', 'C',
      ask(12, '2. Name the stage of photosynthesis during which water molecules are split.'),
      [pt(S('Light Stage'), 5)], 'bio-2-2', 'light-stage', at(9, '14.', '(b)', '(iii)'), 5, stem=[Q14BIII],
      decision=EACH_ITEM + ' Item 2 one point ("(1 pt)").'),
    T('14biv', 'Q14(b)(iv)', 'C', Q(12, 'Carbon dioxide (CO2) is also needed for photosynthesis.',
                                     'Where does CO2 enter the leaf?'),
      [pt(S('Stoma'), 5)], 'bio-2-2', 'carbon-dioxide-enters-by-stomata', at(9, '14.', '(b)', '(iv)'), 5),
    T('14bv', 'Q14(b)(v)', 'C', Q(12, 'A market gardener wants to increase the vegetable yield in his greenhouses.',
                                   'Suggest two ways he may achieve this.'),
      [anyn(None, 2, 5, options=[egs(YIELD, k) for k in (1, 2)], open_list=True)], 'bio-2-2',
      'increasing-crop-yield', at(9, '14.', '(b)', '(v)'), 10,
      decision='Two points ("(2 Pts)"): the scheme\'s two examples after its "e.g.", an open menu, claim two.'),
] + [
    T(f'14c{r}', f'Q14(c)({r})', 'C', q, [row] if not isinstance(row, list) else row, topic, concept,
      at(9, '14.', '(c)', f'({r})'), total, stem=stem, decision=decision)
    for r, q, row, topic, concept, total, stem, decision in [
        ('i', ask(12, 'What is a tissue?'), [pt(S(TISSUE, piece=k), 5) for k in (1, 2)], 'bio-1-3', 'tissue', 10,
         [Q14C], TWO_POINTS.format(n=2) + ' Cut at the scheme\'s own solidus, each on the "2(5) + 2(4) + 5(1)" ladder at '
                                          'its first rate.'),
        ('ii', ask(12, 'Name a gas that would be needed for the growth of tissue in the laboratory.'),
         pt(S('Oxygen'), 5), 'bio-1-3', 'gas-for-tissue-culture', 5, [Q14C], ''),
        ('iii', ask(12, 'Why are sterile conditions needed to grow the tissue?'), pt(S('To avoid contamination'), 5),
         'bio-1-3', 'sterile-conditions-for-tissue-culture', 5, [Q14C], ''),
        ('iv', ask(12, 'What type of cell division, mitosis or meiosis, is involved in tissue culture?'),
         pt(S('Mitosis'), 5), 'bio-2-3', 'mitosis-in-tissue-culture', 5, [Q14C], ''),
        ('v', Q14CV, pt(S('Cancer'), 5), 'bio-2-3', 'cancer', 5, [Q14C], ''),
        ('vi', ask(12, 'Give two causes of this uncontrolled cell division.'),
         anyn(None, 2, 5, options=[egs(CAUSES, k) for k in (1, 2)], open_list=True), 'bio-2-3', 'causes-of-cancer',
         10, [Q14C, M('(v)', 12), Q14CV],
         'Two points ("(2 pts)"): the scheme\'s two examples after its "e.g.", an open menu, claim two.'),
        ('viii', ask(12, 'What is the function of meiosis?'),
         pt(S(*MEIOSIS, piece=1, psep=' (Allow'), 5, note_sel=S(*MEIOSIS, piece=[2, 1], psep=['gametes (', ')'])),
         'bio-2-3', 'function-of-meiosis', 5, [Q14C], 'Its bracketed "Allow reduction division" is the row\'s note.')]
] + [
    T('14cvii', 'Q14(c)(vii)', 'C', ask(12, 'Draw a labelled diagram to show the normal cell cycle.'),
      [allof([(S('Diagram to include:'), S('• Cycle', piece=2, psep='• ')),
              (None, S('• Proportionality', piece=2, psep='• '))], 5,
             note_sel=S('Two correct = 5 marks', 'None = 0 marks')),
       pt(S('Any two correct', 'labels'), 2, kind='criterion', units=[1, 1], label=S('Labels:'), note=NO_ANSWER)],
      'bio-2-3', 'drawing-the-cell-cycle', at(9, '14.', '(c)', '(vii)'), 7, stem=[Q14C],
      decision=DRAWING.format(tariff='D. 5,2,0 L. 2(1)') + ' The diagram row is "Diagram to include" (Cycle, '
               'Proportionality), its band printed as "Two correct = 5 marks / One Correct = 2 marks / None = 0 '
               'marks"; the scheme names no label, so "Any two correct labels" is one criterion row worth its two 1s.'),
] + [
    T(f'15ai-{x.lower()}', 'Q15(a)(i)', 'C', ask(13, 'Name the parts labelled A, B, and C.'),
      [pt(cell(SKIN, i, SKIN_CUTS), 5)], 'bio-2-6', concept, at(10, '15.', '(a)', '(i)'), 5, stem=[Q15A],
      fig='q15-skin', item=(x.lower(), x), labels=skin_labels(x),
      decision=EACH_ITEM + ' "(3 pts)" over the three labels, each on the "2(5)+2(4)+6(2)" ladder at its first rate.')
    for i, (x, concept) in enumerate([('A', 'hair'), ('B', 'sweat-gland'), ('C', 'blood-vessels-of-the-skin')])
] + [
    T(f'15a{r}', f'Q15(a)({r})', 'C', q, rows, topic, concept, at(10, '15.', '(a)', f'({r})'), total,
      stem=[Q15A] if fig else [], fig=fig, decision=decision)
    for r, q, rows, topic, concept, total, fig, decision in [
        ('ii', Q(13, 'The skin is one of the excretory organs in humans.', 'Name one substance excreted by the skin.'),
         [anyn(eg('e.g. Sweat'), 1, 5, open_list=True)], 'bio-2-6', 'excreted-by-the-skin', 5, 'q15-skin', EG_OPEN),
        ('iii', ask(13, 'List two other functions of the skin.'),
         [anyn(None, 2, 5, options=[egs(SKIN_FUNCTIONS, k) for k in (1, 2)], open_list=True)], 'bio-2-6',
         'functions-of-the-skin', 10, 'q15-skin',
         'Two points ("(2 pts)"): the scheme\'s two examples after its "e.g.", an open menu, claim two.'),
        ('iv', ask(13, 'Name another organ of excretion and state one substance it excretes.'),
         [anyn(None, 1, 5, options=[egs(EXCRETION, 1)], open_list=True),
          anyn(None, 1, 5, options=[egs(EXCRETION, 2)], open_list=True)], 'bio-2-6', 'organs-of-excretion', 10,
         'q15-skin',
         'Two points ("(2 pts)"): the organ and the substance it excretes, a row each, cut at the scheme\'s own solidus; '
         'each is the scheme\'s example after its "e.g.", so each row is open.'),
        ('v', ask(13, 'What is meant by the term homeostasis?'), [pt(S('Maintaining constant internal conditions'), 5)],
         'bio-2-4', 'homeostasis', 5, None, ''),
        ('vi', Q(13, 'The human being is an endotherm. What does this mean?'),
         [pt(S('Produces heat (internally) or warm blooded'), 5)], 'bio-2-4', 'endotherm', 5, None, '')]
] + [
    T(f'15bi{n}', f'Q15(b)(i){n}', 'C', ask(13, q), [row], 'bio-2-4', concept, at(10, '15.', '(b)', '(i)'), 5,
      stem=[Q15BI], decision=EACH_ITEM + ' Each numbered item a point, on the "2(5)+2(3)+7(2)" ladder at its first '
                                         'rate.' + extra)
    for n, q, row, concept, extra in [
        (1, '1. What name is given to a plant’s response to light?', pt(S('Phototropism'), 5), 'phototropism', ''),
        (2, '2. Name one growth regulator produced in plants.', anyn(eg('e.g. Auxin'), 1, 5, open_list=True),
         'growth-regulator', ' ' + EG_OPEN),
        (3, '3. Where in a plant are growth regulators produced?', pt(S('Growing tip or apical meristem'), 5),
         'where-growth-regulators-are-made', ''),
        (4, '4. Give one way by which plants can protect themselves from attack.',
         anyn(eg('e.g. Sting'), 1, 5, open_list=True), 'plant-defences', ' ' + EG_OPEN)]
] + [
    T(f'15bii{n}', f'Q15(b)(ii){n}', 'C', q, rows, 'bio-2-4', concept, at(10, '15.', '(b)', '(ii)'), total,
      stem=[Q15BII], decision=EACH_ITEM + extra)
    for n, q, rows, concept, total, extra in [
        (1, ask(13, '1. Name the two main parts of the central nervous system in humans.'),
         [pt(S('Brain & Spinal Cord', piece=k, psep=' & '), 5) for k in (1, 2)], 'parts-of-the-cns', 10,
         ' Item 1 two points ("(2 pts)"), cut at the scheme\'s own "&".'),
        (2, Q15BII2, [anyn(S(NEURONS), 2, 5)], 'types-of-neuron', 10,
         ' Item 2 two points ("(2 Pts)") from the three neurons the scheme prints, cut at its own solidus: a menu, '
         'claim two.'),
        (3, ask(13, '3. What name is given to the area where one neuron ends and another begins?'),
         [pt(S('Synapse'), 5)], 'synapse', 5, ''),
        (4, ask(13, '4. Name the type of chemical that carries messages between two neurons.'),
         [pt(S('(Neuro) Transmitter'), 5)], 'neurotransmitter', 5, ''),
        (5, ask(13, '5. What happens to this chemical once the messages have been transmitted?'),
         [pt(S('Destroyed or reused'), 5)], 'fate-of-neurotransmitter', 5, '')]
] + [
    T(f'15ci-{x.lower()}', 'Q15(c)(i)', 'C', Q15CI, [pt(S(GUT[x]), 5)], 'bio-2-6', concept,
      at(10, '15.', '(c)', '(i)'), 5, stem=[Q15C], fig='q15-digestive', item=(x.lower(), x), labels=gut_labels(x),
      decision=EACH_ITEM + ' "(3 pts)" over the three labels, each printed on its own line, each on the '
                           '"2(5)+2(4)+6(2)" ladder at its first rate.')
    for x, concept in [('A', 'duodenum'), ('B', 'colon'), ('C', 'stomach')]
] + [
    T(f'15c{r}', f'Q15(c)({r})', 'C', q, rows, 'bio-2-6', concept, at(10, '15.', '(c)', f'({r})'), total,
      stem=[Q15C] if fig else [], fig=fig, labels=lab, decision=decision)
    for r, q, rows, concept, total, fig, lab, decision in [
        ('ii', ask(13, 'Explain the term digestion?'), [pt(S('Molecules or food broken down'), 5)], 'digestion', 5,
         None, None, ''),
        ('iii', ask(13, 'Name one human tooth type and give its function.'),
         [anyn(None, 1, 5, options=[egs(TOOTH, 1)], open_list=True),
          anyn(None, 1, 5, options=[egs(TOOTH, 2)], open_list=True)], 'teeth', 10, None, None,
         'Two points ("(2 pts)"): the tooth type and its function, a row each, cut at the scheme\'s own solidus; each '
         'is the scheme\'s example after its "e.g.", so each row is open.'),
        ('iv', Q(13, 'Part C secretes hydrochloric acid onto the ingested food.', 'Give one function of this acid.'),
         [anyn(eg('e.g. Kills bacteria'), 1, 5, open_list=True)], 'hydrochloric-acid-in-the-stomach', 5,
         'q15-digestive', gut_labels('C'), EG_OPEN),
        ('v', ask(13, 'Give one digestive function of part D.'), [anyn(eg('e.g. Bile'), 1, 5, open_list=True)],
         'digestive-function-of-the-liver', 5, 'q15-digestive', gut_labels(),
         EG_OPEN + ' The scheme never names D (it names A, B and C): the label key carries those three, none asked '
                   'here.'),
        ('vi', Q(13, 'Give one digestive function and one non-digestive', 'function of the pancreas.'),
         [pt(S(PANCREAS, piece=1), 5), pt(S('Produces Insulin'), 5)], 'functions-of-the-pancreas', 10,
         'q15-digestive', gut_labels(),
         'Two points ("(1 pt)" each): the digestive function and the non-digestive one, a row each.')]
]

# Drawings priced on their own beside their part's ladder: their units count to
# the ladder as fixed, their cards keep their own marks. Q10(a)'s "3(3)" sits
# under no ladder.
LADDER_EXEMPT = {'13bi', '14aiv', '14cvii'}

FIGURES = {
    # key suffix: (doc, page, rect in PDF points, credit, letters, alt, solution[, masks])
    'q2-amoeba': ('paper', 2, (140, 446, 345, 578), SEC, ['A', 'B', 'C', 'D'],
        'Drawing of an Amoeba as seen through a microscope: an irregular, lobed cell with a dotted interior and '
        'several blunt projections. A points to a clear round body with a frilled edge near the top, B to the dotted '
        'interior on the left, D to a dark solid oval right of centre, and C is a bracket under one of the lower '
        'projections.', False),
    'q4-section': ('paper', 3, (100, 352, 360, 489), SEC, ['A', 'B', 'C'],
        'Transverse section through part of a plant: a circle edged by a thick, rough outer band, with about twelve '
        'oval bundles, each part dark and part dotted, scattered through its pale interior. A points to the pale '
        'tissue between the bundles, B to two of the bundles, C to the outer band.', False),
    'q5-table': ('paper', 4, (40, 50, 560, 316), SEC, [],
        'Question 5 as printed: the instruction, then the list Pollution; Niche (struck through); Recycle; Burning '
        'fuel; Conservation; Smell, above a two-column table. Column A gives the worked example "The role of the '
        'organism in the habitat." (Niche in Column B) and the descriptions (a) to (e); Column B is blank beside '
        'them.', False),
    'q10a-scheme': ('scheme', 7, (150, 106, 440, 186), SEC, [],
        "The marking scheme's example pyramid: a triangle divided into three levels by two horizontal lines, with "
        'Fox, Rabbit and Grass written down its left side from top to bottom and Carnivore, Herbivore and Producer '
        'down its right side.', True),
    'q10bi-ask': ('paper', 8, (60, 127, 452, 158), SEC, [],
        'Question 10(b)(i) as printed, in two lines; in the first, the words biotic and abiotic are underlined.',
        False),
    'q10b-key': ('paper', 8, (80, 214, 545, 488), SEC, ['A', 'B', 'C'],
        'Question 10(b)(iii) as printed: the instruction, then five animal drawings in a row, not to scale: a '
        'caterpillar-like larva with many legs along its body (labelled legs); A, a small beetle with antennae and '
        'six legs (labelled antenna and legs); B, a flat, narrow animal with two dots at its head end; C, a long, '
        'rounded worm-like animal twisted into a loop; and a snail with a coiled shell. Below them the printed key, '
        'four numbered pairs of statements about a shell, legs, pairs of legs and body shape, each ending in a '
        'name or "Go to".', False),
    'q11-rabbit': ('paper', 9, (405, 100, 575, 248), SEC, [],
        'Black-and-white photograph of a white rabbit sitting in grass, seen from the side, its ears upright and its '
        'eye dark.', False),
    'q12-sperm': ('paper', 10, (95, 335, 420, 470), SEC, ['A', 'B', 'C'],
        'Simple drawing of a human sperm cell lying on its side: a long thin strand at the left, a thicker dark oval '
        'section bracketed and labelled Midpiece, and at the right a dark oval with a pale oval inside it. A is a '
        'bracket over the whole of the right-hand dark oval, B points to the pale oval inside it, C points to the '
        'long thin strand.', False),
    'q13-rhizopus': ('paper', 11, (165, 365, 395, 520), SEC, ['A', 'B', 'C'],
        'Drawing of part of the fungus Rhizopus: threads running across horizontally, a cluster of finely branched '
        'threads beneath them, and several upright stalks rising from where they meet, two topped by dark '
        'round heads. A points to a horizontal thread, B to the branched threads underneath, C to one of the dark '
        'round heads.', False),
    'q15-skin': ('paper', 13, (170, 66, 410, 262), SEC, ['A', 'B', 'C'],
        'Drawing of a section through human skin: a dotted surface layer over a deeper layer of rounded cells. A '
        'long dark strand rises from a bulb deep in the skin with a small sac beside it; a coiled tube deep in the '
        'lower layer has a duct running up to the surface; looped tubes lie under the surface layer. A points to the '
        'strand above the surface, B to the coiled tube deep in the skin, C to the looped tubes under the surface '
        'layer.', False),
    'q15-digestive': ('paper', 13, (385, 565, 580, 760), SEC, ['A', 'B', 'C', 'D'],
        'Outline drawing of the human digestive system inside the trunk: a large organ at the upper left, a sac at '
        'the upper right, a dark gland under the sac labelled Pancreas, a tube leaving the sac and curving down, and '
        'coiled tubes below, framed by a wide tube running up the right side, across the top and down the left. D '
        'points to the large organ at the upper left, C to the sac, A to the tube curving down from the sac, B to '
        'the wide tube on the right.', False),
}
