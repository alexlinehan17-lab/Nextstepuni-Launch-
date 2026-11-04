"""Biology 2014 Ordinary Level — reviewed task ledger, carded from the paper for the first time.

Independent visual sweep (2026-10-25), every page rendered and read:
  * The 2014 paper is one booklet (M43), 16 pages: p1 cover and instructions,
    p2-p4 Section A Questions 1-6, p5-p7 Section B Questions 7-9, p8-p13
    Section C Questions 10-15, p14-p16 "Blank Page". Sections A and B are
    answered on the paper; Section C in an answer book. No acknowledgements
    page: the Q11(b) photograph and every drawing carry no credit (the Q11(b)
    passage prints its own source line, "[Meerkats at Dublin Zoo (series 4,
    2013) adapted from RTE programme website notes and other sources]").
  * The marking scheme, 12 pages: p1 cover, p2 note, p3 introduction,
    cancelled and surplus answers, p4 conventions, p5-p11 Questions 1-15 (one
    table, printed page numbers 3-9), p12 back cover (no text).

The paper keeps the long-standing shape: any five of Section A's six
questions, any two of Section B's three, any four of Section C's six, and
Questions 14 and 15 are each any two of (a), (b), (c). Every printed ask is
carded. No Biology card existed for 2014 Ordinary before this review.

This scheme prints no reprint of any question: each answer stands under its
own question number, letter and roman. A task is anchored on its own part
marker, found by walking the scheme's numbering down to it (SQ path). Where
the text layer sets a roman's marker on its answer's own line ("(vii) Looks
alert, ...") the marker is a welded bare anchor and the row is read from that
line. A numbered item ("1.", "2.") is anchored on the roman it is printed
under. Four Section A markers are printed "(c )", with a space, which the
anchor check does not read as a marker (Q1, Q2, Q3, Q5): each is anchored on
(b)'s marker, the marker printed before it, and its answer read from there.
Scheme p5 prints its page number "3" as its first line, so Question 3 is
found by walking through Question 2's head first.

The scheme counts POINTS ("2 pts", "3 pts"; a row with no count is one
point) and heads each question or part with what they are worth. Ordered
splits are carded at their first rate: Q1 "2(7)+3(2)" over the best five of
its six parts, Q2, Q3 and Q5 "6(3) +2" over seven points, Q6 "4(3) +
[3+3(1)] + 2" over five points beside its pyramid drawing's own "[3 +
3(1)]", every Section B (a) "5 + 1" over two, and every Section C (a) of
Q10-Q13 "7 + 2(1)" over three. Q4 is "5(4)"; Section B (b) "8(3)" (Q8) or
"6(3)+[3+3(1)]" (Q7, Q9: six points and a drawing priced 3 + 3(1)); Section
C (b) "9(3)" and (c) "8(3)"; every part of Q14 and Q15 "10(3)": a fixed mark
per point. A Section C (a) ladder sits beside its question's fixed (b) and
(c), so each such ladder names their units as fixed and their cards are
exempt from its notation; Q6's pyramid is fixed beside its ladder the same
way. Every printed answer fits a per-response tariff, so no part is carded
whole.

Read off the rendered scheme, and lifted as printed: Q7(b)'s heading
"6(3)+[3+(3(1)]" (a stray bracket); Q14(a)'s rows numbered (i), (ii), (ii),
(iv), the second "(ii)" standing in (iii)'s place, which anchors Q14(a)(iii);
Q12(c)(iv)'s "In the blood on in the lymph.".

Points the scheme counts without printing a count against them, settled by
its own totals: Q8(b) "8(3)" prints "Sterilised (seeds) / facedown on agar"
"2 pts" for (iv), then "Add iodine or biuret solution to plate" on a row of
its own before (v)'s marker, then (v)'s "1." and "2." results, each printed
twice in two wordings; eight points only if (iv) is three points (the
iodine row answers the ask's second half, how digestion was shown) and (v)
two, one per numbered result with its two wordings a claim-one menu. Q11(b)
"9(3)" makes (ii) one point, so its "Dry, open plains or scrubland /
network of burrows" is a claim-one menu; Q11(c)(iii)'s "Counting / numbers /
how many" likewise. Q11(b)(iii) "Kills / prey or kill / to eat or kills/
for food" (2 pts) is read by the conventions page's rule 1 (the solidus
separates the words that earn marks) with its "or"s joining three
alternative pairs: answer variants Kills / prey, kill / to eat, kills / for
food, two rows each (coordinator's reviewer pass).

The census reads all 136 of the paper's printed asks (no paper.py entry is
needed for this sitting); all 136 are claimed here.
"""
from bio_review_lib import Q, SQ, S, M, pt, anyn, T, L, parse_ref

YEAR, LEVEL = 2014, 'ol'
REVIEWED_AT = '2026-10-25'

SOURCES = {
    'paper': {'path': 'examiner-reports/biology/papers/2014-ol-paper.pdf',
              'fileid': 'LC025GLP000EV.pdf',
              'sha256': '276a219dd85252dfcdfc968e12c1e3e009b3a17cf59e6211f925537bfee15142',
              'pages': 16},
    'scheme': {'path': 'examiner-reports/biology/schemes/2014-ol.pdf',
               'fileid': 'LC025GLP000EV.pdf',
               'sha256': '05c884d7539d58b5d88ac0897aa4ddbd57a7113598d0afa63d72cf0f14fb8240',
               'pages': 12},
}

PAGE_ROLES = {
    'paper': {1: 'cover', **{p: 'questions' for p in range(2, 14)}, 14: 'blank', 15: 'blank', 16: 'blank'},
    'scheme': {1: 'cover', 2: 'note', 3: 'introduction', 4: 'conventions',
               **{p: 'marking' for p in range(5, 12)}, 12: 'back-cover'},
}


def _ladder(notation, **extra):
    """An ordered split as the scheme prints it ("2(7)+3(2)", "5 + 1")."""
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
    **{(n, 'b'): 24 for n in (7, 8, 9)},   # p5: "part (b) carries 24 marks"
    **{(n, x): t for n in range(10, 14) for x, t in (('b', 27), ('c', 24))},   # the paper's "(27)", "(24)"
    **{(n, x): 30 for n in (14, 15) for x in 'abc'},   # "(30, 30)"
}
LADDERS = {
    # Q1: six parts, the best five priced ("Answer any five of parts (a) to (f)").
    1: _ladder('2(7)+3(2)', responses=6),
    **{q: _ladder('6(3) +2') for q in (2, 3)}, 5: _ladder('6(3)+2'),
    # Q6 "4(3) + [3+3(1)] + 2": five single answers on the ladder "4(3) ... + 2",
    # the pyramid's "[3+3(1)]" fixed beside it.
    6: {'steps': [3, 3, 3, 3, 2], 'notation': '4(3) + [3+3(1)] + 2', 'fixed': {3: 1, 1: 3}},
    **{(n, 'a'): _ladder('5 + 1') for n in (7, 8, 9)},
    # Section C (a) "7 + 2(1)"; (b) "9(3)" and (c) "8(3)" are fixed points
    # beside it, named here so the question's total is the ladder's.
    **{(n, 'abc'): _ladder('7 + 2(1)', fixed={3: 17}) for n in (10, 11, 12, 13)},
}

CHECKSUMS = {
    1: {7: 6}, 2: {3: 7}, 3: {3: 7}, 4: {4: 5}, 5: {3: 7}, 6: {3: 6, 1: 3},
    **{(n, 'a'): {5: 2} for n in (7, 8, 9)},
    (7, 'b'): {3: 7, 1: 3}, (8, 'b'): {3: 8}, (9, 'b'): {3: 7, 1: 3},
    **{(n, 'a'): {7: 3} for n in range(10, 14)},
    **{(n, 'b'): {3: 9} for n in range(10, 14)},
    **{(n, 'c'): {3: 8} for n in range(10, 14)},
    **{(n, x): {3: 10} for n in (14, 15) for x in 'abc'},
}

SCAN_PAGES = {'paper': range(1, 14)}
SELECTION_SCAN = [
    ('paper', 1, 'any five', 'Cover rubric, Section A: whole-question choice; every question is carded.'),
    ('paper', 1, 'any two', 'Cover rubric, Section B: whole-question choice; every question is carded.'),
    ('paper', 1, 'any four', 'Cover rubric, Section C: whole-question choice; every question is carded.'),
    ('paper', 2, 'any five', 'Section A rubric repeated.'),
    ('paper', 2, 'any five', 'Q1 "Answer any five of parts (a) to (f)": the best five of six parts priced; every part '
                             'is carded.'),
    ('paper', 2, 'any one', 'Q1(e) "State any one of these functions": one answer.'),
    ('paper', 2, 'the following', 'Q2 lead-in: every statement asked, one card per letter.'),
    ('paper', 2, 'or', 'Q2 "true (T) or false (F)": the answer options.'),
    ('paper', 2, 'or', 'Q2 "T or F": the answer options.'),
    ('paper', 3, 'choose', 'Q4 "Choose each term": every description matched, one card per lettered part.'),
    ('paper', 3, 'the following', 'Q4 list of terms: the options.'),
    ('paper', 4, 'the following', 'Q6 lead-in: every part asked.'),
    ('paper', 4, 'the following', 'Q6(b) "The following food chain": the printed chain, shown as a figure.'),
    ('paper', 5, 'any two', 'Section B rubric repeated.'),
    ('paper', 5, 'the following', 'Q7(b) lead-in: every part asked.'),
    ('paper', 5, 'the following', 'Q7(b)(v) "Label the following": all three labels asked.'),
    ('paper', 6, 'the following', 'Q8(b) lead-in: every part asked.'),
    ('paper', 6, 'or', 'Q8(b)(iv) "whether or not digestion had occurred": description.'),
    ('paper', 7, 'the following', 'Q9(b) lead-in: every part asked.'),
    ('paper', 7, 'both', 'Q9(b)(iv) "both the aorta and the pulmonary artery": description.'),
    ('paper', 7, 'the following', 'Q9(b)(v) "label the following parts": all three labels asked.'),
    ('paper', 8, 'any four', 'Section C rubric repeated.'),
    ('paper', 8, 'the following', 'Q10(a) lead-in: every term asked, one card per roman.'),
    ('paper', 9, 'or', 'Q11(b) passage "sunbathe or sleep": passage text.'),
    ('paper', 10, 'any two', 'Q12(b)(ii) "Name any two types of neuron": two answers from the printed menu.'),
    ('paper', 11, 'the following', 'Q13(a)(i) "each of the following": both processes asked, one card each.'),
    ('paper', 11, 'or', 'Q13(a)(i) "catabolism or anabolism": the answer options.'),
    ('paper', 11, 'or', 'Q13(c)(iv) "a little or a lot": the answer options.'),
    ('paper', 12, 'any two', 'Q14 "any two of the parts (a), (b), (c)": whole-part choice; every part is carded.'),
    ('paper', 12, 'or', 'Q14(a)(v) "two or more bones": description.'),
    ('paper', 12, 'any two', 'Q14(b)(iv) "Name any two diseases": two answers.'),
    ('paper', 13, 'any two', 'Q15 "any two of the parts (a), (b), (c)": whole-part choice; every part is carded.'),
    ('paper', 13, 'the following', 'Q15(b) lead-in: every part asked.'),
    ('paper', 13, 'both', 'Q15(b)(ii) "Name both.": both muscles asked, a row each.'),
]


# Q11(b)(iii) "Explain the term predator." (2 pts): three alternative pairs on one
# printed line, each pair two rows cut at the scheme's own solidus and "or".
PREDATOR_LINE = 'Kills / prey or kill / to eat or kills/ for food'
PREDATOR = [
    ('kills-prey', 'Kills prey',
     [pt(S(PREDATOR_LINE, piece=1), 3), pt(S(PREDATOR_LINE, piece=[2, 1], psep=['/', ' or ']), 3)]),
    ('kill-to-eat', 'Kill to eat',
     [pt(S(PREDATOR_LINE, piece=[2, 2], psep=['/', ' or ']), 3),
      pt(S(PREDATOR_LINE, piece=[3, 1], psep=['/', ' or ']), 3)]),
    ('kills-for-food', 'Kills for food',
     [pt(S(PREDATOR_LINE, piece=[3, 2], psep=['/', ' or ']), 3), pt(S(PREDATOR_LINE, piece=4), 3)]),
]
ANSWER_VARIANTS = {'11biii': PREDATOR}

ROUTES = {}

SEC = 'State Examinations Commission'
NO_REPRINT = 'The scheme prints no reprint of any question: anchored on the part\'s own marker.'
WELDED = ('The scheme prints no reprint and sets this part\'s marker on its answer\'s own line: anchored on that '
          'marker.')
SPACED = ('The scheme prints this part\'s marker "(c )", with a space, which the anchor check does not read as a '
          'marker: anchored on (b)\'s marker, the marker printed before it, and its answer read from there.')
MISNUMBERED = ('The scheme prints this part\'s marker as a second "(ii)" (rendered and looked at: the rows run (i), '
               '(ii), (ii), (iv)); anchored on that second "(ii)", the marker printed in (iii)\'s place.')
EACH_ITEM = 'A list the scheme prices entry by entry: one card per entry, each its own slice of the printed line.'
NO_ANSWER = 'The scheme prints no answer here, only what earns the marks.'
TWO_POINTS = 'The scheme prices this part at two points ("2 pts"): each printed point its own row.'
LEAD_IN = ('The printed item alone is too short a question to stand, so the card carries the printed lead-in in its '
           'question text.')
# Scheme p5 prints its page number "3" as its first line: Question 3 is found
# under its own head after Question 2's.
AFTER_Q2 = ['2', '3']


def at(page, q, *path_and_marker, why=NO_REPRINT, nth=1, head=None):
    """The part's own marker under its question (and letter) on the scheme page."""
    *path, marker = path_and_marker
    return SQ(page, marker, path=[*(head or [str(q)]), *path], paired=why, bare=True, nth=nth)


def welded(page, q, *path_and_marker):
    """The part's marker opening its own answer line ("(vii) Looks alert, ...")."""
    *path, marker = path_and_marker
    return SQ(page, marker, path=[str(q), *path], paired=WELDED, bare=True, welded=True)


def ask(page, sentence, **kw):
    """A one-line ask closed by its own punctuation, before its answer line."""
    return Q(page, sentence, sentence, **kw)


def dots(page, sentence, **kw):
    """An ask whose last word runs straight into its printed answer dots ("...foodchain ......"):
    the line cut at the dots."""
    return Q(page, sentence, piece=1, psep='..', **kw)


def item(page, n, sentence, **kw):
    """A numbered item printed with its number on a line of its own ("1." / "What are these gaps
    called?"): the number, then the ask."""
    return [M(f'{n}.', page), ask(page, sentence, **kw)]


def cell(line, i, cuts, page=None, meaning=False, after=None, end=None):
    """Cell i of a scheme line printed as cells ("A = Biceps B = Triceps"), cut at the cells' own
    printed boundaries: cuts[k] = (text opening cell k+1, text closing cell k). With `meaning`, the
    cell's answer alone (after its " = "), for a figure's label key."""
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
    return S(line, end, page=page, piece=pieces, psep=seps, after=after)


def labels(cells, page, asked=None):
    """A figure's label key from its scheme cells: [(letter, line, i, cuts)]."""
    return [L(x, cell(line, i, cuts, page=page, meaning=True), x == asked) for x, line, i, cuts in cells]


def bracket(line, end=None, after=None):
    """A scheme answer and its square-bracketed direction, cut at the bracket: (answer, note)."""
    sel = (line, end) if end else (line,)
    return (S(*sel, piece=1, psep=' [', after=after), S(*sel, piece=[2, 1], psep=[' [', ']'], after=after))


def plain(line, marks, end=None, after=None, **kw):
    """One answer whose square-bracketed direction ("[Accept scissors]") is the row's note."""
    ans, note = bracket(line, end, after)
    return pt(ans, marks, note_sel=note, **kw)


def pieces(line, n, end=None):
    """The scheme's own solidus-separated points of one line, a row selector each."""
    return [S(*((line, end) if end else (line,)), piece=k) for k in range(1, n + 1)]


# ------------------------------------------------------------ question text --
Q1 = Q(2, 'A meal in a fast-food restaurant consists of fish and chips with a glass of water to drink.')
Q1C = ask(2, 'Chips contain starch. What chemical is used to test for the presence of starch?')
Q2 = Q(2, 'Indicate whether the following statements are true (T) or false (F) by drawing a circle around T or F in',
       'each case.')
Q3 = Q(3, 'The diagram shows the human female reproductive system.')
Q4 = Q(3, 'Choose each term from the following list and place it in Column B to match a description in Column A.',
       'The first one has been completed as an example.')
Q5A = Q(4, 'The diagram shows three bacterial shapes. Match the correct letter with the name of each shape', 'below.')
Q6 = Q(4, 'Use your knowledge of ecology to answer the following:')
Q6B = Q(4, 'The following food chain is from a grassland ecosystem:')
Q7B = Q(5, 'Answer the following questions in relation to how you prepared and examined with a microscope a',
        'transverse section (T.S.) of a dicotyledonous stem.')
Q8B = Q(6, 'Answer the following questions in relation to practical work you carried out to investigate',
        'digestive activity in germinating seeds.')
Q8BII = Q(6, 'The seeds were divided into two batches. One batch was used untreated.',
          'How did you treat the other batch of seeds before using them in the investigation?')
Q8BV = ask(6, 'Give the results of your investigation.')
Q9B = ask(7, 'Answer the following questions in relation to the dissection of a heart.')
Q10A = Q(8, 'Explain the following terms as used in genetics:')
Q10B = Q(8, 'In cats, black coat colour (B) is dominant to white coat colour (b).',
         'If a white cat is crossed with a cat heterozygous for coat colour, state:')
Q10C = Q(8, 'The diagram shows a cell undergoing division.')
Q10CII = ask(8, 'This type of cell division is called mitosis.')
Q11A = Q(9, 'In relation to ecology, explain the terms')
Q11B = [ask(9, 'Read the passage below and answer the questions that follow.'),
        Q(9, 'In the wild, meerkats live in South Africa and Namibia, in dry, open plains and scrubland.',
          'and then eat its body.')]
Q12AI = Q(10, 'Plants and animals respond to some outside stimuli.', 'Name two stimuli to which plants respond.')
Q12B = Q(10, 'The diagram shows the human nervous system.')
Q12BIII = Q(10, 'Tiny gaps are found where one neuron ends and the next', 'one begins.')
Q12BIV1 = item(10, 1, 'Name one disorder of the human nervous system.')
Q12C = Q(10, 'Obesity is an excessive level of body fat. It is generally caused by over-eating and lack of',
         'thirst and fatigue.')
Q13AI = Q(11, 'Catabolism and anabolism are two types of metabolism.',
          'State whether each of the following is an example of catabolism or anabolism:')
Q13B = Q(11, 'The diagram shows a section through a leaf.')
Q13CIII = ask(11, 'Which type of respiration results in the production of acid in our muscles?')
Q13CV = ask(11, 'What is the name of the acid produced in the muscles?')
Q14A = Q(12, 'The diagram shows muscles and bones in a human arm.')
# Page 12 prints these two items' "1." after their roman ("(vi) 1.", "(iii) 1."), never alone on its
# line: the number is lifted from that line, the first and second such on the page.
Q14AVI1 = [Q(12, '1.'), ask(12, 'Name one disorder of the human musculoskeletal system.')]
Q14BIII1 = [Q(12, '1.', nth=2), ask(12, 'Distinguish between active immunity and passive immunity by defining each.')]
Q14C = Q(12, 'The diagram shows the human male reproductive system.')
Q15A = Q(13, 'The diagram shows a section through the human eye.')
Q15B = Q(13, 'Answer the following questions in relation to the human breathing system.')
Q15BIV1 = ask(13, '1. Name one disorder of the human breathing system.')
Q15C = Q(13, 'Water is vital for the survival of plants.')

# ------------------------------------------------------- scheme cell lines --
FEMALE1 = ('A = Vagina B = Womb or Uterus', [(' B =', 'Vagina ')])
FEMALE2 = ('C = Ovary D = Fallopian Tube or Oviduct', [(' D =', 'Ovary ')])
BACTERIA = ('Rod = B Cocci = C Spiral = A', [(' Cocci =', 'B '), (' Spiral =', 'C ')])
PYRAMID = 'Correct diagram shape + named organisms [each level = 1pt]'
NERVE = 'A = Brain B = Spinal cord [Accept spine]'
ARM = ('A = Biceps B = Triceps', [(' B =', 'Biceps ')])
MALE = ('A = Penis B = Urethra C = Sperm duct or Vas deferens', [(' B =', 'Penis '), (' C =', 'Urethra ')])
EYE = ('A = Retina B = Lens', [(' B =', 'Retina ')])
GAMETES = 'Gametes: (b) ( B) (b)'


def female_labels(asked=None):
    return labels([(x, FEMALE1[0], i, FEMALE1[1]) for i, x in enumerate('AB')]
                  + [(x, FEMALE2[0], i, FEMALE2[1]) for i, x in enumerate('CD')], 5, asked)


def nerve_labels(asked=None):
    # B's cell closes on the scheme's bracketed "Accept spine", no part of its name.
    return [L('A', S(NERVE, page=8, piece=[1, 2], psep=[' B =', ' = ']), asked == 'A'),
            L('B', S(NERVE, page=8, piece=[2, 1, 2], psep=['Brain ', ' [', ' = ']), asked == 'B')]


def arm_labels(asked=None):
    return labels([(x, ARM[0], i, ARM[1]) for i, x in enumerate('AB')], 10, asked)


def male_labels(asked=None):
    return labels([(x, MALE[0], i, MALE[1]) for i, x in enumerate('ABC')], 10, asked)


def eye_labels(asked=None):
    return labels([(x, EYE[0], i, EYE[1]) for i, x in enumerate('AB')], 11, asked)


def leaf_labels(asked=None):
    # The scheme names no structure for B (its (ii) answer is what B's cells
    # hold); A is named by (iii)'s answer.
    return [L('A', S('Stoma(ta)', page=9), asked == 'A')]


TASKS = [
    # ------------------------------------------------------------ Section A --
] + [
    T(f'1{x}', f'Q1({x})', 'A', q, [row], 'bio-1-2', concept, sq, 7, stem=stem,
      decision='Q1 prints "Answer any five of parts (a) to (f)" and the scheme "2(7)+3(2)": an ordered split over '
               'the best five of the six parts, each part carded at its first rate.')
    for x, q, row, concept, sq, stem in [
        ('a', ask(2, 'Give a good source of protein from this meal.'), pt(S('Fish'), 7), 'source-of-protein',
         at(5, 1, '(a)'), [Q1]),
        ('b', ask(2, 'Give one function of protein in the human body.'),
         pt(S('Growth or repair or (to make) enzymes or hormones or antibodies', 'or any named example of these.'), 7),
         'functions-of-protein', at(5, 1, '(b)'), [Q1]),
        ('c', Q1C, pt(S('Iodine'), 7), 'test-for-starch', at(5, 1, '(b)', why=SPACED), [Q1]),
        ('d', ask(2, 'State the colour of the chemical referred to in (c) if starch is present.'),
         pt(S('Blue-black'), 7), 'positive-starch-test', at(5, 1, '(d)'), [Q1, M('(c)', 2), Q1C]),
        ('e', ask(2, 'Water has many functions in the human body. State any one of these functions.'),
         pt(S('Solvent or transport or medium for reactions or reactant.'), 7), 'functions-of-water',
         at(5, 1, '(e)'), [Q1]),
        ('f', ask(2, 'Suggest a reason why eating too much fast food could be bad for your health.'),
         pt(S('Obesity or high blood pressure or constipation (low fibre) or', 'clogged arteries.'), 7),
         'unhealthy-diet', at(5, 1, '(f)'), [Q1])]
] + [
    T(f'2{x}', f'Q2({x})', 'A', ask(2, q), [pt(S(ans), 3)], topic, concept,
      at(5, 2, '(b)', why=SPACED) if x == 'c' else at(5, 2, f'({x})'), 3, stem=[Q2],
      decision='Seven statements on the "6(3) +2" ladder, each carded at its first rate. The scheme prints each answer '
               'as the word TRUE or FALSE.')
    for x, q, ans, topic, concept in [
        ('a', 'Chromosomes are made up of DNA and protein.', 'TRUE', 'bio-1-4', 'chromosome-composition'),
        ('b', 'A human sperm cell contains 23 chromosomes.', 'TRUE', 'bio-1-4', 'chromosome-number-in-gametes'),
        ('c', 'Phenotype is the genetic make-up of an organism.', 'FALSE', 'bio-1-4', 'phenotype'),
        ('d', 'Replication is the copying of DNA.', 'TRUE', 'bio-2-3', 'dna-replication'),
        ('e', 'RNA contains the base thymine.', 'FALSE', 'bio-1-2', 'bases-of-rna'),
        ('f', 'Genetic engineering is the manipulation and alteration of genes.', 'TRUE', 'bio-3-3',
         'genetic-engineering'),
        ('g', 'The copying of the DNA code into mRNA is called transcription.', 'TRUE', 'bio-2-3', 'transcription')]
] + [
    T(f'3a-{x.lower()}', 'Q3(a)', 'A', ask(3, 'Name the parts labelled A, B, C and D.'),
      [pt(cell(line[0], i, line[1]), 3)], 'bio-2-5', concept, at(5, 3, '(a)', head=AFTER_Q2), 3, stem=[Q3],
      fig='q3-female', item=(x.lower(), x), labels=female_labels(x),
      decision=EACH_ITEM + ' Four points of the "6(3) +2" ladder, one per label.')
    for x, line, i, concept in [('A', FEMALE1, 0, 'vagina'), ('B', FEMALE1, 1, 'uterus'), ('C', FEMALE2, 0, 'ovary'),
                                ('D', FEMALE2, 1, 'fallopian-tube')]
] + [
    T('3b', 'Q3(b)', 'A', ask(3, 'State one function of the part labelled C in the diagram.'),
      [pt(S('Produce eggs or hormones (oestrogen, progesterone)'), 3)], 'bio-2-5', 'functions-of-the-ovary',
      at(5, 3, '(b)', head=AFTER_Q2), 3, stem=[Q3], fig='q3-female', labels=female_labels('C')),
    T('3c', 'Q3(c)', 'A', ask(3, 'Give one cause of infertility in women.'),
      [pt(S('Blockage of Fallopian tubes or hormonal or failure to ovulate or', 'excessive exercise.'), 3)], 'bio-2-5',
      'female-infertility', at(5, 3, '(b)', head=AFTER_Q2, why=SPACED), 3, stem=[Q3], fig='q3-female'),
    T('3d', 'Q3(d)', 'A', Q(3, 'In cases of infertility, eggs may be fertilised outside the body. Following this procedure,',
                            'into which part of the reproductive system is the developing embryo then placed?'),
      [pt(S('Womb or uterus or endometrium / lining of womb or uterus or ‘E’'), 3)], 'bio-2-5', 'in-vitro-fertilisation',
      at(5, 3, '(d)', head=AFTER_Q2), 3, stem=[Q3], fig='q3-female', labels=female_labels(),
      decision='One point of the ladder: the scheme\'s one printed line is read whole (its solidus joins two wordings '
               'of the one answer, "endometrium / lining of womb or uterus", and it accepts the figure\'s letter E).'),
] + [
    T(f'4{x}', f'Q4({x})', 'A', Q(3, q), [pt(S(ans), 4)], 'bio-1-3', concept, at(5, 4, f'({x})'), 4,
      stem=[Q4], qfig='q4-table',
      decision='The list of terms (its "Tissue" struck through as the worked example) and the table are shown as the '
               'question\'s own print.')
    for x, q, ans, concept in [
        ('a', 'A plant organ', 'Leaf', 'plant-organ'),
        ('b', 'Cells growing in a test tube', 'In vitro growth', 'in-vitro-growth'),
        ('c', 'The heart', 'Organ', 'organ'),
        ('d', 'A use of tissue culture', 'Skin graft', 'uses-of-tissue-culture'),
        ('e', 'A plant tissue', 'Dermal', 'plant-tissue')]
] + [
    # "Rod.", "Cocci." and "Spiral." alone are too short a question to stand:
    # each card carries the printed lead-in in its question text.
    T(f'5a-{name.lower()}', 'Q5(a)', 'A', [Q5A, ask(4, f'{name}.', br=True)], [pt(cell(BACTERIA[0], i, BACTERIA[1]), 3)],
      'bio-3-2', concept, at(5, 5, '(a)'), 3, fig='q5-bacteria', item=(name.lower(), name),
      decision=EACH_ITEM + ' Three points of the "6(3)+2" ladder, one per shape. ' + LEAD_IN)
    for i, (name, concept) in enumerate([('Rod', 'rod-shaped-bacteria'), ('Cocci', 'cocci'),
                                         ('Spiral', 'spiral-bacteria')])
] + [
    T(f'5{x}', f'Q5({x})', 'A', q, [pt(S(ans), 3)], 'bio-3-2', concept, sq, 3)
    for x, q, ans, concept, sq in [
        ('b', dots(4, 'Bacteria reproduce by a method known as'), 'Binary fission', 'binary-fission', at(5, 5, '(b)')),
        ('c', ask(4, 'Some bacteria have flagella. What are flagella used for?'), 'Movement', 'flagella',
         at(5, 5, '(b)', why=SPACED)),
        ('d', dots(4, 'Give one harmful effect of bacteria'), 'e.g. Diseases or food decay or named disease',
         'harmful-bacteria', at(5, 5, '(d)')),
        ('e', ask(4, 'Give one beneficial effect of bacteria.'), 'e.g. Yoghurt or cheese or antibiotic production',
         'beneficial-bacteria', at(5, 5, '(e)'))]
] + [
    T('6a', 'Q6(a)', 'A', ask(4, 'What do we mean by the word ecology?'),
      [pt(S('(Study of relationship between) organisms & their environment'), 3)], 'bio-3-1', 'ecology',
      at(6, 6, '(a)'), 3, stem=[Q6],
      decision='One of the five single answers on the ladder "4(3) ... + 2", carded at its first rate.'),
] + [
    T(f'6b{r}', f'Q6(b)({r})', 'A', q, [pt(S(ans), 3)], 'bio-3-1', concept, at(6, 6, '(b)', f'({r})'), 3,
      stem=[Q6, Q6B], fig='q6-chain',
      decision='One of the five single answers on the ladder "4(3) ... + 2", carded at its first rate.')
    for r, q, ans, concept in [
        ('i', ask(4, 'Name a secondary consumer from the above food chain.'), 'Fox', 'secondary-consumer'),
        ('ii', dots(4, 'Name a producer from the above foodchain'), 'Grass', 'producer'),
        ('iii', dots(4, 'Name a herbivore from the above foodchain'), 'Rabbit', 'herbivore'),
        ('v', ask(4, 'If all the foxes were killed, what would happen to the number of rabbits?'),
         'e.g. Number would increase', 'removing-a-predator')]
] + [
    T('6biv', 'Q6(b)(iv)', 'A', ask(4, 'In the space below, show the above foodchain as a pyramid of numbers.'),
      [pt(S(PYRAMID, piece=1, psep=' + '), 3, kind='criterion', note=NO_ANSWER),
       pt(S(PYRAMID, piece=[2, 1], psep=[' + ', ' [']), 3, kind='criterion', units=[1, 1, 1], note=NO_ANSWER,
          note_sel=S(PYRAMID, piece=[2, 2, 1], psep=[' + ', ' [', ']']))],
      'bio-3-1', 'pyramid-of-numbers', at(6, 6, '(b)', '(iv)'), 6, stem=[Q6, Q6B], fig='q6-chain',
      decision='The scheme prices the pyramid on its own row at "[3 + 3(1)]", beside the ladder: the shape (3) and the '
               'named organisms (1 a level, the scheme\'s bracketed "each level = 1pt" the row\'s note), a criterion '
               'row each, cut at the scheme\'s own "+".'),
    # ------------------------------------------------------------ Section B --
    T('7ai', 'Q7(a)(i)', 'B', ask(5, 'Why is a dicotyledonous (dicot) plant so called?'),
      [pt(S('Two cotyledons or two seed leaves (in each seed)'), 5)], 'bio-2-6', 'dicotyledons',
      at(6, 7, '(a)', '(i)'), 5, decision='"5 + 1" over (a)\'s two parts, each carded at its first rate.'),
    T('7aii', 'Q7(a)(ii)', 'B', ask(5, 'Give one function of vascular tissue in plants.'),
      [pt(S('Transport or transport example or support'), 5)], 'bio-2-6', 'functions-of-vascular-tissue',
      at(6, 7, '(a)', '(ii)'), 5),
] + [
    T(f'7b{r}', f'Q7(b)({r})', 'B', q, rows, 'bio-2-6', concept, at(6, 7, '(b)', f'({r})'), total, stem=[Q7B],
      decision=decision)
    for r, q, rows, concept, total, decision in [
        ('i', ask(5, 'Name the plant that you used.'),
         [plain('Name of plant [do not accept a mature tree]', 3, kind='criterion', note=NO_ANSWER)], 'plant-for-a-stem-section',
         3, 'The scheme\'s "Name of plant" names what earns the point; its bracketed direction is the row\'s note.'),
        ('ii', ask(5, 'Why did you use a herbaceous (non-woody) stem rather than a woody one?'),
         [pt(S('Easier to cut'), 3)], 'herbaceous-stem', 3, ''),
        ('iii', ask(5, 'Outline how you made the section of the stem and prepared it for examination.'),
         [pt(s, 3) for s in pieces('(Cut) a thin slice / place, in water or stain, on slide', 2)], 'cutting-a-stem-section',
         6, TWO_POINTS + ' Cut at the scheme\'s own solidus.'),
        ('iv', ask(5, 'Describe how you examined your section of stem with the microscope.'),
         [pt(s, 3) for s in pieces('Turn on light or mirror / low power lens or coarse focus', 2)],
         'examining-a-stem-section', 6, TWO_POINTS + ' Cut at the scheme\'s own solidus.'),
        ('v', [ask(5, 'Draw a labelled diagram to best represent what was seen on your slide.'),
               ask(5, 'Label the following on your diagram: ground tissue, xylem, phloem.', br=True)],
         [pt(S('Diagram (circle or sector with bundle) + 3 labels', piece=1, psep=' + '), 3, kind='criterion',
             note=NO_ANSWER),
          pt(S('Diagram (circle or sector with bundle) + 3 labels', piece=2, psep=' + '), 3, kind='criterion',
             units=[1, 1, 1], note=NO_ANSWER)], 'drawing-a-stem-section', 6,
         'The scheme prices the drawing at "[3+3(1)]": the diagram (3) and the three labels at 1 each, a criterion '
         'row each, cut at the scheme\'s own "+". The (b) heading "6(3)+[3+(3(1)]" (sic) prints this bracket beside '
         'the six points of (i)-(iv).')]
] + [
    T('8ai', 'Q8(a)(i)', 'B', ask(6, 'What is meant by the term digestion?'), [pt(S('Breakdown of food'), 5)], 'bio-2-5',
      'digestion', at(6, 8, '(a)', '(i)'), 5, decision='"5 + 1" over (a)\'s two parts, each carded at its first rate.'),
    T('8aii', 'Q8(a)(ii)', 'B', ask(6, 'Name a carbohydrate you would expect to find stored in a seed.'),
      [pt(S('Starch'), 5)], 'bio-2-5', 'seed-food-store', at(6, 8, '(a)', '(ii)'), 5),
    T('8bi', 'Q8(b)(i)', 'B', ask(6, 'What type of agar did you use in this investigation?'),
      [pt(S('Starch (agar) or milk (agar)'), 3)], 'bio-2-5', 'agar-for-digestive-activity', at(6, 8, '(b)', '(i)'), 3,
      stem=[Q8B]),
    T('8bii', 'Q8(b)(ii)', 'B', Q8BII, [pt(S('Boiled'), 3)], 'bio-2-5', 'boiled-seeds', at(6, 8, '(b)', '(ii)'), 3,
      stem=[Q8B]),
    T('8biii', 'Q8(b)(iii)', 'B', ask(6, 'Why was such treatment necessary?'),
      [pt(S('To kill the seeds or destroy enzymes or act as control'), 3)], 'bio-2-5', 'why-boil-the-seeds',
      at(6, 8, '(b)', '(iii)'), 3, stem=[Q8B, M('(ii)', 6), Q8BII]),
    T('8biv', 'Q8(b)(iv)', 'B', Q(6, 'Describe how you carried out the investigation and indicate clearly how you showed',
                                   'whether or not digestion had occurred.'),
      [*(pt(s, 3) for s in pieces('Sterilised (seeds) / facedown on agar', 2)),
       pt(S('Add iodine or biuret solution to plate'), 3)], 'bio-2-5', 'investigating-digestive-activity',
      at(6, 8, '(b)', '(iv)'), 9, stem=[Q8B],
      decision='Three points, a row each: the scheme prints "Sterilised (seeds) / facedown on agar" with "2 pts" and, '
               'on its own row before (v)\'s marker, "Add iodine or biuret solution to plate" (one point: how the '
               'result was shown, the ask\'s second half). With (i)-(iii) and (v)\'s two results these are the eight '
               'points of "8(3)".'),
] + [
    T(f'8bv{n}', f'Q8(b)(v){n}', 'B', [Q8BV, M(f'{n}.', 6, br=True), Q(6, ask_)],
      [anyn(None, 1, 3, options=options)], 'bio-2-5', concept, at(6, 8, '(b)', '(v)'), 3, stem=[Q8B],
      decision=EACH_ITEM + ' The scheme prints two lines under each number, two wordings of the one result: a menu of '
                           'the two, claim one.')
    for n, ask_, options, concept in [
        (1, 'Untreated seeds.', [S('The plate turns blue-black or purple except where the', 'clear under the seeds'),
                                 S('Clear patches in the agar under the seeds')], 'result-with-untreated-seeds'),
        (2, 'Treated seeds.', [S('the agar turned blue-black or purple'),
                               S('Treated (boiled) seeds left agar unchanged (blue-black /', 'purple)')],
         'result-with-treated-seeds')]
] + [
    T('9ai', 'Q9(a)(i)', 'B', ask(7, 'What is the purpose of the valves in the heart?'),
      [pt(S('Prevent backflow (of blood)'), 5)], 'bio-2-6', 'heart-valves', at(7, 9, '(a)', '(i)'), 5,
      decision='"5 + 1" over (a)\'s two parts, each carded at its first rate.'),
    T('9aii', 'Q9(a)(ii)', 'B', ask(7, 'What structure separates the right side of the heart from the left side?'),
      [pt(S('Septum'), 5)], 'bio-2-6', 'septum', at(7, 9, '(a)', '(ii)'), 5),
] + [
    T(f'9b{r}', f'Q9(b)({r})', 'B', q, rows, 'bio-2-6', concept, at(7, 9, '(b)', f'({r})'), total, stem=[Q9B],
      decision=decision)
    for r, q, rows, concept, total, decision in [
        ('i', ask(7, 'How did you distinguish between the left side and the right side of the heart?'),
         [pt(S('Left side firmer or thicker'), 3)], 'left-and-right-side-of-the-heart', 3, ''),
        ('ii', ask(7, 'What was the main instrument that you used for the actual dissection?'),
         [plain('Scalpel [Accept scissors]', 3)], 'dissecting-instrument', 3, ''),
        ('iii', ask(7, 'Describe how you carried out the dissection.'),
         [pt(s, 3) for s in pieces('Cut / left side / right side', 3)], 'dissecting-the-heart', 9,
         'Three points ("3 pts"), a row each, cut at the scheme\'s own solidus.'),
        ('iv', ask(7, 'Name the valves found at the base of both the aorta and the pulmonary artery.'),
         [pt(S('Semi-lunar valves'), 3)], 'semilunar-valves', 3, ''),
        ('v', [Q(7, 'Based on your dissection, draw a diagram to show and label the following parts:',
                 'bicuspid valve, left atrium, left ventricle.')],
         [pt(S('Diagram and 3 named labels', piece=1, psep=' and '), 3, kind='criterion', note=NO_ANSWER),
          pt(S('Diagram and 3 named labels', piece=2, psep=' and '), 3, kind='criterion', units=[1, 1, 1],
             note=NO_ANSWER)], 'drawing-the-dissected-heart', 6,
         'The scheme prices the drawing at "[3+3(1)]": the diagram (3) and the three named labels at 1 each, a '
         'criterion row each, cut at the scheme\'s own "and".')]
] + [
    # ------------------------------------------------------------ Section C --
    # The three terms ("Diploid." and the rest) alone are too short a question
    # to stand: each card carries the printed lead-in in its question text.
    T(f'10a{r}', f'Q10(a)({r})', 'C', [Q10A, ask(8, term, br=True)], [pt(S(ans), 7)], topic, concept,
      at(7, 10, '(a)', f'({r})'), 7, decision='"7 + 2(1)" over (a)\'s three terms, each carded at its first rate. ' + LEAD_IN)
    for r, term, ans, topic, concept in [
        ('i', 'Heterozygous.', 'Alleles are different', 'bio-1-4', 'heterozygous'),
        ('ii', 'Sex chromosome.', 'Controls sex of organism', 'bio-1-4', 'sex-chromosome'),
        ('iii', 'Diploid.', 'Two sets of chromosomes or chromosomes in pairs', 'bio-2-3', 'diploid')]
] + [
    T('10bi', 'Q10(b)(i)', 'C', ask(8, 'The genotype of each parent cat.'),
      [pt(S('Parents: bb and Bb', piece=[2, n], psep=[': ', ' and ']), 3, label=S('Parents: bb and Bb', piece=1, psep=': '))
       for n in (1, 2)], 'bio-1-4', 'parent-genotypes', at(7, 10, '(b)', '(i)'), 6, stem=[Q10B],
      decision='Two points ("2 pts"), one per parent, cut at the scheme\'s own "and".'),
    T('10bii', 'Q10(b)(ii)', 'C', ask(8, 'The genotype(s) of the gametes produced by each parent.'),
      [pt(S(GAMETES, piece=pc, psep=ps), 3, label=S(GAMETES, piece=1, psep=': '))
       for pc, ps in (([2, 1], [': ', ' ( ']), ([2, 2, 1], [': ', '(b) ', ' (b)']), ([2, 3], [': ', ') ']))],
      'bio-1-4', 'gametes-of-a-cross', at(7, 10, '(b)', '(ii)'), 9, stem=[Q10B],
      decision='Three points ("3 pts"), one per printed gamete, cut at the printed spaces between the bracketed '
               'gametes "(b) ( B) (b)" (the scheme sets the dominant gamete "( B)" with a space inside its bracket).'),
    T('10biii', 'Q10(b)(iii)', 'C', ask(8, 'The genotypes and the matching phenotypes of the kittens produced by the cross.'),
      [pt(S(line, piece=[2, n], psep=[': ', ' ']), 3, label=S(line, piece=1, psep=': '))
       for line in ('Offspring genotypes: Bb bb', 'Matching phenotypes: black white') for n in (1, 2)],
      'bio-1-4', 'offspring-genotypes-and-phenotypes', at(7, 10, '(b)', '(iii)'), 12, stem=[Q10B],
      decision='Four points: the two offspring genotypes ("2 pts") and their two matching phenotypes ("2 pts"), a '
               'row each, cut at the printed spaces; each phenotype matches the genotype printed above it.'),
    T('10ci', 'Q10(c)(i)', 'C', ask(8, 'On which structure in the diagram are the genes located?'),
      [pt(S('Chromosome'), 3)], 'bio-1-4', 'genes-on-chromosomes', at(7, 10, '(c )', '(i)'), 3, stem=[Q10C],
      fig='q10-cell'),
] + [
    T(f'10c{r}{n}', f'Q10(c)({r}){n}', 'C', item(8, n, q), [row], 'bio-2-3', concept, at(7, 10, '(c )', f'({r})'), 3,
      stem=stem, fig='q10-cell', decision=EACH_ITEM + ' Each numbered item a point.')
    for r, n, q, row, concept, stem in [
        ('ii', 1, 'How many cells are formed when a cell divides by mitosis?', pt(S('Two'), 3), 'products-of-mitosis',
         [Q10C, Q10CII]),
        ('ii', 2, 'Name the other type of cell division.', pt(S('Meiosis'), 3), 'meiosis', [Q10C, Q10CII]),
        ('iii', 1, 'What is the purpose of mitosis in single-celled organisms?', pt(S('Reproduction'), 3),
         'mitosis-in-unicellular-organisms', [Q10C]),
        ('iii', 2, 'Name a single-celled organism.',
         pt(S('Named single - celled organism'), 3, kind='criterion', note=NO_ANSWER), 'single-celled-organisms', [Q10C])]
] + [
    T('10civ', 'Q10(c)(iv)', 'C', ask(8, 'Which genetic structure changes when a mutation occurs?'),
      [pt(S('Gene or chromosome or DNA'), 3)], 'bio-2-3', 'mutation', at(7, 10, '(c )', '(iv)'), 3, stem=[Q10C],
      fig='q10-cell'),
    T('10cv', 'Q10(c)(v)', 'C', ask(8, 'What is meant by genetic screening?'),
      [pt(s, 3) for s in pieces('Checking or testing (DNA) / for a gene', 2)], 'bio-1-4', 'genetic-screening',
      at(7, 10, '(c )', '(v)'), 6, stem=[Q10C], fig='q10-cell', decision=TWO_POINTS + ' Cut at the scheme\'s own solidus.'),
] + [
    T(f'11a{r}', f'Q11(a)({r})', 'C', [Q11A, ask(9, term, br=True)], [pt(S(ans), 7)], 'bio-3-1', concept,
      at(8, 11, '(a)', f'({r})'), 7, decision='"7 + 2(1)" over (a)\'s three terms, each carded at its first rate. ' + LEAD_IN)
    for r, term, ans, concept in [
        ('i', 'Abiotic.', 'Abiotic: non-living (factors)', 'abiotic-factors'),
        ('ii', 'Edaphic.', 'Edaphic: (relating to) soil', 'edaphic-factors'),
        ('iii', 'Habitat.', 'Habitat: where an organism lives', 'habitat')]
] + [
    T(f'11b{r}', f'Q11(b)({r})', 'C', ask(9, q), rows, 'bio-3-1', concept, sq, total, stem=Q11B, fig='q11-meerkat',
      decision=decision)
    for r, q, rows, concept, total, sq, decision in [
        ('i', 'Name one country where meerkats live in the wild.', [pt(S('South Africa or Namibia'), 3)],
         'meerkat-range', 3, at(8, 11, '(b)', '(i)'), ''),
        ('ii', 'Where do colonies of meerkats make their home?',
         [anyn(S('Dry, open plains or scrubland / network of burrows'), 1, 3)], 'meerkat-habitat', 3,
         at(8, 11, '(b)', '(ii)'),
         'One point (no count printed), either printed answer: a menu cut at the scheme\'s own solidus, claim one.'),
        ('iii', 'Explain the term predator.', PREDATOR[0][2], 'predator', 6, at(8, 11, '(b)', '(iii)'),
         'Two points ("2 pts"). The scheme prints "Kills / prey or kill / to eat or kills/ for food": its '
         'conventions page says the solidus separates the words that earn marks, and the "or"s join three '
         'alternative pairs (Kills / prey, kill / to eat, kills / for food). Each pair is an answer variant of '
         'two rows, cut from the printed line at its own solidus and "or". Coordinator\'s reviewer pass; the '
         'author had read the line as a four-option menu, which offered "prey or kill" as one answer.'),
        ('iv', 'What evidence is in the passage to suggest that meerkats are omnivores?',
         [pt(S('They eat animals and plant or fungus'), 3)], 'omnivores', 3, at(8, 11, '(b)', '(iv)'), ''),
        ('v', 'Meerkats have a high immunity to the sting of which animal?', [pt(S('Scorpion'), 3)],
         'meerkat-immunity', 3, at(8, 11, '(b)', '(v)'), ''),
        ('vi', 'Name the three kingdoms of organisms represented in the passage above.',
         [pt(S('Plants and animals and fungi'), 3)], 'kingdoms-in-the-passage', 3, at(8, 11, '(b)', '(vi)'),
         'One point (no count printed) for the three kingdoms together: one row.'),
        ('vii', 'Give two reasons suggested by the photograph why meerkats make good sentries.',
         [anyn(S('Looks alert, upright (posture) or large ears or large nose or large', 'eyes'), 2, 3, sep=' or ')],
         'meerkats-as-sentries', 6, welded(8, 11, '(b)', '(vii)'),
         'Two points ("2 pts") from the reasons the scheme prints joined by "or": one menu cut at its own "or", '
         'claim two.')]
] + [
    T(f'11c{r}', f'Q11(c)({r})', 'C', q, rows, 'bio-3-1', concept, at(8, 11, '(c )', f'({r})'), total,
      decision=decision)
    for r, q, rows, concept, total, decision in [
        ('i', ask(9, 'Give two problems associated with waste disposal.'),
         [anyn(S('smell, unsightly, vermin, disease, pollution,', 'illegal dumping'), 2, 3, sep=',', open_list=True,
               note_sel=S('Any two problems e.g. smell, unsightly, vermin, disease, pollution,', 'illegal dumping',
                          piece=1, psep=' e.g.'))], 'problems-of-waste-disposal', 6,
         'Two points ("2 pts") from the scheme\'s examples, cut at its own commas: one menu, claim two; its "Any two '
         'problems" is the row\'s note.'),
        ('ii', ask(9, 'Mention two ways of minimising the amount of waste produced.'),
         [anyn(S('reduce or reuse or recycle - any two', piece=1, psep=' -'), 2, 3, sep=' or ',
               note_sel=S('reduce or reuse or recycle - any two', piece=2, psep='- '))], 'minimising-waste', 6,
         'Two points ("2 pts") from the three ways the scheme prints joined by "or": one menu, claim two; its "any '
         'two" is the row\'s note.'),
        ('iii', Q(9, 'A quantitative survey was carried out to show the effect of poor waste management on the',
                  'What is meant by the term quantitative?'),
         [anyn(S('Counting / numbers / how many'), 1, 3)], 'quantitative-survey', 3,
         'One point (no count printed), any one of the printed wordings: a menu cut at the scheme\'s own solidus, '
         'claim one.'),
        ('iv', ask(9, 'Describe how you carried out a quantitative survey on a species of plant in its habitat.'),
         [anyn(S('Quadrat / random or how achieved /count / number of times'), 3, 3)], 'quadrat-survey', 9,
         'Three points ("3 pts") from the four printed points, cut at the scheme\'s own solidus: one menu, claim '
         'three.')]
] + [
    T('12ai', 'Q12(a)(i)', 'C', Q12AI,
      [anyn(S('Light or water or gravity or touch or chemicals or temperature'), 2, 7, sep=' or ')], 'bio-2-4',
      'plant-stimuli', at(8, 12, '(a)', '(i)'), 14,
      decision='Two points ("2 pts") of the "7 + 2(1)" ladder from the stimuli the scheme prints joined by "or": one '
               'menu, claim two, each response at the ladder\'s first rate.'),
    T('12aii', 'Q12(a)(ii)', 'C', ask(10, 'Give one example of a plant response to such a stimulus.'),
      [pt(S('Growth towards (or away from) stimulus e.g. phototropism'), 7)], 'bio-2-4', 'plant-responses',
      at(8, 12, '(a)', '(ii)'), 7, stem=[M('(i)', 10), Q12AI]),
] + [
    T(f'12bi-{x.lower()}', 'Q12(b)(i)', 'C', ask(10, 'Name the parts labelled A and B.'), [row], 'bio-2-4', concept,
      at(8, 12, '(b)', '(i)'), 3, stem=[Q12B], fig='q12-nervous', item=(x.lower(), x), labels=nerve_labels(x),
      decision=EACH_ITEM + ' "2 pts" over the two labels.' + extra)
    for x, row, concept, extra in [
        ('A', pt(S(NERVE, piece=1, psep=' B ='), 3), 'brain', ''),
        ('B', pt(S(NERVE, piece=[2, 1], psep=['Brain ', ' [']), 3,
                 note_sel=S(NERVE, piece=[2, 2, 1], psep=['Brain ', ' [', ']'])), 'spinal-cord',
         ' Its bracketed direction is the row\'s note.')]
] + [
    T('12bii', 'Q12(b)(ii)', 'C', Q(10, 'Nerve impulses are carried around the body by neurons.',
                                     'Name any two types of neuron.'),
      [anyn(S('Sensory / motor / inter (relay)'), 2, 3)], 'bio-2-4', 'types-of-neuron', at(8, 12, '(b)', '(ii)'), 6,
      stem=[Q12B], fig='q12-nervous', decision='Two points ("2 pts") from the printed list: one menu, claim two.'),
] + [
    T(f'12b{r}{n}', f'Q12(b)({r}){n}', 'C', item(10, n, q), [row], 'bio-2-4', concept, at(8, 12, '(b)', f'({r})'), 3,
      stem=stem, fig='q12-nervous', decision=EACH_ITEM + ' Each numbered item a point.' + extra)
    for r, n, q, row, concept, stem, extra in [
        ('iii', 1, 'What are these gaps called?', plain('Synaptic cleft [Accept synapse].', 3), 'synapse',
         [Q12B, Q12BIII], ''),
        ('iii', 2, 'What substances carry nerve impulses across the gaps?',
         pt(S('Neurotransmitter(s) or named neurotransmitter'), 3), 'neurotransmitters', [Q12B, Q12BIII], ''),
        ('iv', 1, 'Name one disorder of the human nervous system.', pt(S("Named disorder: e.g. Parkinson's"), 3),
         'nervous-system-disorder', [Q12B], ''),
        ('iv', 2, 'Give one cause of the disorder.', pt(S('Cause: lack of dopamine'), 3), 'cause-of-a-nervous-disorder',
         [Q12B, M('(iv)', 10)] + Q12BIV1, ' The scheme prints the cause for its example disorder, Parkinson\'s.'),
        ('iv', 3, 'Suggest a means of treating the disorder.', pt(S('Treatment: drugs'), 3),
         'treating-a-nervous-disorder', [Q12B, M('(iv)', 10)] + Q12BIV1,
         ' The scheme prints the treatment for its example disorder, Parkinson\'s.')]
] + [
    T(f'12c{r}', f'Q12(c)({r})', 'C', ask(10, q), [row], 'bio-2-4', concept, at(8, 12, '(c )', f'({r})'), 3,
      stem=[Q12C], decision=decision)
    for r, q, row, concept, decision in [
        ('i', 'What is meant by the term obesity?', plain('Excessive level of body fat [Accept high BMI]', 3), 'obesity', ''),
        ('ii', 'What is meant by the term endocrine?', pt(S('Ductless or not having tube(s)'), 3), 'endocrine-glands', ''),
        ('iii', 'Where in the human body is the pancreas located?', pt(S('Abdomen or under the stomach or near duodenum'), 3),
         'location-of-the-pancreas', ''),
        ('iv', 'How are hormones carried around the body?', pt(S('In the blood on in the lymph.'), 3),
         'transport-of-hormones',
         'The scheme prints "In the blood on in the lymph." (rendered and looked at); it is lifted as printed.')]
] + [
    T(f'12cv{n}', f'Q12(c)(v){n}', 'C', item(10, n, q), [row], 'bio-2-4', concept, at(8, 12, '(c )', '(v)'), total,
      stem=[Q12C], decision=EACH_ITEM + ' ' + decision)
    for n, q, row, concept, total, decision in [
        (1, 'Give one cause of diabetes.',
         plain('Lack of insulin or insulin not functioning or genetics [Accept', 3,
               end='causes listed in introduction to question].'), 'causes-of-diabetes', 3,
         'One point; its bracketed direction is the row\'s note.'),
        (2, 'Give two symptoms of diabetes.',
         anyn(S('Thirst, fatigue, high or low blood sugar levels'), 2, 3, sep=',', open_list=True), 'symptoms-of-diabetes',
         6, 'Two points ("2 pts") from the scheme\'s examples, cut at its own commas: one menu, claim two.'),
        (3, 'Suggest one treatment for a person who suffers from diabetes.',
         anyn(S('Insulin injections / dietary management / exercise'), 1, 3, open_list=True), 'treating-diabetes', 3,
         'One point from the scheme\'s examples, cut at its own solidus: one menu, claim one.')]
] + [
    T(f'13ai{n}', f'Q13(a)(i){n}', 'C', ask(11, f'{n}. {name}.'), [pt(S(f'{name}: {ans}'), 7)], 'bio-2-1', concept,
      at(9, 13, '(a)', '(i)'), 7, stem=[Q13AI], decision=EACH_ITEM + ' Two of the three points of the "7 + 2(1)" ladder.')
    for n, name, ans, concept in [(1, 'Photosynthesis', 'anabolism', 'photosynthesis-is-anabolic'),
                                  (2, 'Respiration', 'catabolism', 'respiration-is-catabolic')]
] + [
    T('13aii', 'Q13(a)(ii)', 'C', ask(11, 'What is the main source of energy for photosynthesis?'),
      [pt(S('Light or sunlight'), 7)], 'bio-2-2', 'energy-for-photosynthesis', at(9, 13, '(a)', '(ii)'), 7),
] + [
    T(f'13b{r}', f'Q13(b)({r})', 'C', q, rows, 'bio-2-2', concept, at(9, 13, '(b)', f'({r})'),
      6 if r == 'vi' else 3 * len(rows),
      stem=[Q13B], fig='q13-leaf', labels=leaf_labels('A' if r == 'iii' else None) if r in ('ii', 'iii') else None,
      decision=decision)
    for r, q, rows, concept, decision in [
        ('i', ask(11, 'Name the green pigment present in leaves that is essential for photosynthesis.'),
         [pt(S('Chlorophyll'), 3)], 'chlorophyll', ''),
        ('ii', Q(11, 'Name the cell structures, present in large numbers in part B, that are needed for',
                 'photosynthesis.'), [pt(S('Chloroplast'), 3)], 'chloroplasts',
         'The scheme names no structure for B; the card\'s key decodes the one letter it does name, A, not asked here.'),
        ('iii', ask(11, 'Name the opening labelled A that is used for gas exchange.'), [pt(S('Stoma(ta)'), 3)], 'stomata',
         ''),
        ('iv', ask(11, 'Name the gas in the air needed for photosynthesis.'),
         [plain('Carbon dioxide [Accept water vapour]', 3)], 'carbon-dioxide-for-photosynthesis', ''),
        ('v', Q(11, 'In photosynthesis, water is split into three products.', 'Name these three products.'),
         [pt(s, 3) for s in pieces('Protons (hydrogen ions) / electrons / oxygen', 3)], 'splitting-water',
         'Three points ("3 pts"), all three asked: a row each, cut at the scheme\'s own solidus.'),
        ('vi', Q(11, 'From your knowledge of photosynthesis, suggest two ways of improving the rate of',
                 'photosynthesis of plants in a greenhouse.'),
         [anyn(S('More light (intensity or hours) / more carbon dioxide / more heat'), 2, 3)],
         'improving-photosynthesis', 'Two points ("2 pts") from the printed list: one menu, claim two.')]
] + [
    T(f'13c{r}', f'Q13(c)({r})', 'C', q, rows, 'bio-2-2', concept, at(9, 13, '(c )', f'({r})'), 3 * len(rows),
      stem=stem, decision=decision)
    for r, q, rows, concept, stem, decision in [
        ('i', ask(11, 'What is meant by the term respiration?'),
         [pt(s, 3) for s in pieces('(Release of) energy / from food', 2)], 'respiration', [],
         TWO_POINTS + ' Cut at the scheme\'s own solidus.'),
        ('ii', ask(11, 'Name the two types of respiration.'), [pt(s, 3) for s in pieces('Aerobic / anaerobic', 2)],
         'types-of-respiration', [], TWO_POINTS + ' Cut at the scheme\'s own solidus.'),
        ('iii', Q13CIII, [plain('Anaerobic [Accept aerobic]', 3)], 'anaerobic-respiration-in-muscle', [], ''),
        ('iv', ask(11, 'In the type of respiration referred to in (iii), is a little or a lot of energy produced?'),
         [plain('Little (lot) [parts iv, v & vi must match part (iii)]', 3)], 'energy-from-anaerobic-respiration',
         [M('(iii)', 11), Q13CIII], 'The scheme\'s bracketed direction is the row\'s note.'),
        ('v', Q13CV, [pt(S('Lactic if anaerobic (pyruvic if aerobic)'), 3)], 'lactic-acid', [M('(iii)', 11), Q13CIII],
         ''),
        ('vi', ask(11, 'Suggest what might happen to this acid in the muscles afterwards.'),
         [pt(S('Broken down or diffuses away or turns to fat (respired', 'aerobically)'), 3)], 'fate-of-lactic-acid',
         [M('(v)', 11), Q13CV], '')]
] + [
    # ------------------------------------------------------------ Q14 --------
    T(f'14ai-{x.lower()}', 'Q14(a)(i)', 'C', ask(12, 'Name the muscles labelled A and B.'),
      [pt(cell(ARM[0], i, ARM[1]), 3)], 'bio-2-4', concept, at(10, 14, '(a)', '(i)'), 3, stem=[Q14A], fig='q14-arm',
      item=(x.lower(), x), labels=arm_labels(x), decision=EACH_ITEM + ' "2 pts" over the two labels.')
    for i, (x, concept) in enumerate([('A', 'biceps'), ('B', 'triceps')])
] + [
    T(f'14a{r}', f'Q14(a)({r})', 'C', ask(12, q), rows, 'bio-2-4', concept, sq, 3 * len(rows), stem=[Q14A],
      fig='q14-arm', labels=arm_labels() if r == 'iv' else None, decision=decision)
    for r, q, rows, concept, sq, decision in [
        ('ii', 'These two muscles are an antagonistic pair. What does this mean?',
         [pt(S('The two work in opposition to each other'), 3)], 'antagonistic-pair', at(10, 14, '(a)', '(ii)'), ''),
        ('iii', 'Name the structures that attach muscles to bones.', [pt(S('Tendons'), 3)], 'tendons',
         at(10, 14, '(a)', '(ii)', nth=2, why=MISNUMBERED), ''),
        ('iv', 'Describe the roles of the muscles A and B in raising the forearm.',
         [pt(s, 3) for s in pieces('Biceps contracts / triceps relaxes', 2)], 'raising-the-forearm',
         at(10, 14, '(a)', '(iv)'), TWO_POINTS + ' Cut at the scheme\'s own solidus.'),
        ('v', 'What general name is given to places in the body where two or more bones meet?', [pt(S('Joints'), 3)],
         'joints', at(10, 14, '(a)', '(v)'), '')]
] + [
    T('14avi1', 'Q14(a)(vi)1', 'C', Q14AVI1, [pt(S('Named disorder'), 3, kind='criterion', note=NO_ANSWER)], 'bio-2-4',
      'musculoskeletal-disorder', at(10, 14, '(a)', '(vi)'), 3, stem=[Q14A], fig='q14-arm',
      decision=EACH_ITEM + ' The scheme prints "1. Named disorder", what earns the point.'),
    T('14avi2', 'Q14(a)(vi)2', 'C', item(12, 2, 'Suggest one cause and one treatment for the disorder referred to in (vi) 1. above.'),
      [pt(S('Cause'), 3, kind='criterion', note=NO_ANSWER), pt(S('Treatment'), 3, kind='criterion', note=NO_ANSWER)],
      'bio-2-4', 'cause-and-treatment-of-a-musculoskeletal-disorder', at(10, 14, '(a)', '(vi)'), 6,
      stem=[Q14A, M('(vi)', 12)] + Q14AVI1, fig='q14-arm',
      decision='The paper\'s item 2 asks for a cause and a treatment; the scheme prices them as its "2. Cause" and '
               '"3. Treatment", a point each and what earns it: a criterion row each.'),
] + [
    T(f'14b{r}', f'Q14(b)({r})', 'C', q, rows, topic, concept, at(10, 14, '(b)', f'({r})'), total, stem=stem,
      decision=decision)
    for r, q, rows, topic, concept, total, stem, decision in [
        ('i', ask(12, 'What term is used to describe organisms that cause disease?'), [pt(S('Pathogen'), 3)], 'bio-2-4',
         'pathogen', 3, [], ''),
        ('ii', Q(12, 'The general defence system tries to prevent disease-causing organisms entering the body.',
                 'List two parts of the general defence system in the body.'),
         [anyn(S('Skin or cilia or stomach acid or tears or white blood cells or', 'blood clotting'), 2, 3, sep=' or ',
               open_list=True)], 'bio-2-4', 'general-defence-system', 6, [],
         'Two points ("2 pts") from the scheme\'s examples joined by "or": one menu cut at its own "or", claim two.'),
        ('iv', Q(12, 'Viruses cause disease in plants, humans, and other animals.', 'Name any two diseases caused by viruses.'),
         [pt(S('Two disease examples'), 6, kind='criterion', units=[3, 3], note=NO_ANSWER)], 'bio-1-1', 'viral-diseases',
         6, [], 'Two points ("2 pts") for the scheme\'s "Two disease examples", what earns them: one criterion row.'),
        ('v', Q(12, 'Some people receive vaccinations to protect them from disease.', 'What is meant by the term vaccination?'),
         [pt(s, 3) for s in pieces('Non-disease causing dose / of a pathogen', 2)], 'bio-2-4', 'vaccination', 6, [],
         TWO_POINTS + ' Cut at the scheme\'s own solidus.')]
] + [
    T('14biii1', 'Q14(b)(iii)1', 'C', Q14BIII1,
      [pt(S('Active immunity: (body) produces antibodies'), 3),
       pt(S('Passive immunity: antibodies given or administered', '(produced by another organism).'), 3)], 'bio-2-4',
      'active-and-passive-immunity', at(10, 14, '(b)', '(iii)'), 6,
      decision=EACH_ITEM + ' Item 1 is two of (iii)\'s "3 pts", one per definition, each printed under its own label.'),
    T('14biii2', 'Q14(b)(iii)2', 'C', item(12, 2, 'Which of these produces the longest-lasting immunity?'),
      [pt(S('Active', after='(produced by another organism).'), 3)], 'bio-2-4', 'lasting-immunity',
      at(10, 14, '(b)', '(iii)'), 3, stem=[M('(iii)', 12)] + Q14BIII1, decision=EACH_ITEM + ' The third of (iii)\'s "3 pts".'),
] + [
    T(f'14ci-{x.lower()}', 'Q14(c)(i)', 'C', ask(12, 'Name the parts A, B, C.'), [pt(cell(MALE[0], i, MALE[1]), 3)],
      'bio-2-5', concept, at(10, 14, '(c )', '(i)'), 3, stem=[Q14C], fig='q14-male', item=(x.lower(), x),
      labels=male_labels(x), decision=EACH_ITEM + ' "3 pts" over the three labels.')
    for i, (x, concept) in enumerate([('A', 'penis'), ('B', 'urethra'), ('C', 'sperm-duct')])
] + [
    T(f'14c{r}', f'Q14(c)({r})', 'C', q, [row], 'bio-2-5', concept, sq, total, stem=[Q14C], fig='q14-male',
      labels=male_labels() if r in ('iv', 'v') else None, decision=decision)
    for r, q, row, concept, total, sq, decision in [
        ('ii', ask(12, 'Name one male sex hormone.'), pt(S('Testosterone or FSH or LH'), 3), 'male-sex-hormones', 3,
         at(10, 14, '(c )', '(ii)'), ''),
        ('iii', ask(12, 'What is the function of the prostate gland?'),
         pt(S('Release liquid or nourish or support sperm'), 3), 'prostate-gland', 3, at(10, 14, '(c )', '(iii)'), ''),
        ('iv', Q(12, 'Suggest a reason why the structure containing', 'part D must be kept below body temperature.'),
         pt(S('Sperm production better if cooler'), 3), 'scrotum-temperature', 3, at(10, 14, '(c )', '(iv)'),
         'The scheme names no structure for D except as (v)\'s answer; the card\'s key decodes A, B and C, none asked.'),
        ('v', ask(12, 'In which labelled part does meiosis occur?'), pt(S('D or testes'), 3), 'meiosis-in-the-testes', 3,
         at(10, 14, '(c )', '(v)'), ''),
        ('vi', ask(12, 'What is meant by the term contraception?'), pt(S('Prevention of pregnancy'), 3), 'contraception',
         3, at(10, 14, '(c )', '(vi)'), ''),
        ('vii', ask(12, 'List two methods of contraception.'),
         anyn(S('barrier (or named e.g. condom) / (contraceptive) pill', '/ surgical (or named e.g. vasectomy) / abstain'),
              2, 3), 'methods-of-contraception', 6, welded(10, 14, '(c )', '(vii)'),
         'Two points ("2 pts") from the four methods the scheme prints after its "Two methods:": one menu cut at its '
         'own solidus, claim two.')]
] + [
    # ------------------------------------------------------------ Q15 --------
    T(f'15ai-{x.lower()}', 'Q15(a)(i)', 'C', ask(13, 'Name the parts labelled A and B.'), [pt(cell(EYE[0], i, EYE[1]), 3)],
      'bio-2-4', concept, at(11, 15, '(a)', '(i)'), 3, stem=[Q15A], fig='q15-eye', item=(x.lower(), x),
      labels=eye_labels(x), decision=EACH_ITEM + ' "2 pts" over the two labels.')
    for i, (x, concept) in enumerate([('A', 'retina'), ('B', 'lens')])
] + [
    T(f'15a{r}', f'Q15(a)({r})', 'C', ask(13, q), rows, 'bio-2-4', concept, at(11, 15, '(a)', f'({r})'), total,
      stem=[Q15A], fig='q15-eye', decision=decision)
    for r, q, rows, concept, total, decision in [
        ('ii', 'Name and give a function of the coloured part of the eye.',
         [pt(S('Name: iris'), 3), pt(S('Function: control amount of light entering eye'), 3)], 'iris', 6,
         'The name and the function, a point each ("2 pts"), each printed under its own label: a row each.'),
        ('iii', 'The eye is filled with fluid. What is the function of this fluid?',
         [pt(S('Give shape to eye or support lens or transmits light'), 3)], 'fluids-of-the-eye', 3, ''),
        ('iv', 'Explain in detail how the eye works.',
         [anyn(S('Light through cornea / pupil / lens / accommodation / focus / onto',
                 'retina / rods / cones / nerve impulse / optic nerve'), 5, 3)], 'how-the-eye-works', 15,
         'Five points ("5 pts") from the ten printed points, cut at the scheme\'s own solidus: one menu, claim five.')]
] + [
    T(f'15b{r}', f'Q15(b)({r})', 'C', q, rows, 'bio-2-6', concept, at(11, 15, '(b)', f'({r})'), total, stem=[Q15B],
      decision=decision)
    for r, q, rows, concept, total, decision in [
        ('i', ask(13, 'When we breathe we inhale air. What gas in the air is essential for respiration?'),
         [pt(S('Oxygen'), 3)], 'oxygen-for-respiration', 3, ''),
        ('ii', Q(13, 'One large muscle and one set of muscles are involved in inhalation.', 'Name both.'),
         [pt(s, 3) for s in pieces('Diaphragm / intercostal (rib) muscles', 2)], 'muscles-of-inhalation', 6,
         TWO_POINTS + ' Cut at the scheme\'s own solidus.'),
        ('iii', ask(13, 'Describe in detail how we inhale air.'),
         [anyn(S('Intercostal muscles contract / to move ribcage up and out /', 'increases / pressure decreases / air moves in'),
               4, 3)], 'inhalation', 12,
         'Four points ("4 pts") from the six printed points, cut at the scheme\'s own solidus: one menu, claim four.')]
] + [
    T(f'15biv{n}', f'Q15(b)(iv){n}', 'C', q, [pt(S(crit), 3, kind='criterion', note=NO_ANSWER)], 'bio-2-6', concept,
      at(11, 15, '(b)', '(iv)'), 3, stem=stem,
      decision=EACH_ITEM + f' The scheme prints "{n}. {crit}", what earns the point.')
    for n, q, crit, concept, stem in [
        (1, Q15BIV1, 'Named disorder', 'breathing-disorder', [Q15B]),
        (2, ask(13, '2. Suggest a possible cause of the disorder.'), 'Cause', 'cause-of-a-breathing-disorder',
         [Q15B, M('(iv)', 13), Q15BIV1]),
        (3, ask(13, '3. Suggest a treatment for the disorder.'), 'Treatment', 'treating-a-breathing-disorder',
         [Q15B, M('(iv)', 13), Q15BIV1])]
] + [
    T(f'15ci{n}', f'Q15(c)(i){n}', 'C', q, [pt(S(ans), 3)], 'bio-2-6', concept, at(11, 15, '(c )', '(i)'), 3,
      stem=[Q15C], fig='q15-plant', decision=EACH_ITEM + ' Each numbered item a point.')
    for n, q, ans, concept in [
        (1, Q(13, '1. What would you expect to notice after a few hours about the stem and leaves of a plant',
              'in an experiment such as the one shown above?'), 'Red colour', 'transport-in-xylem'),
        (2, ask(13, '2. Suggest a reason why a layer of oil was placed on top of the water.'), 'Prevent evaporation',
         'oil-layer')]
] + [
    T(f'15c{r}', f'Q15(c)({r})', 'C', ask(13, q), [pt(S(ans), 3)], 'bio-2-6', concept, at(11, 15, '(c )', f'({r})'), 3,
      stem=[Q15C])
    for r, q, ans, concept in [
        ('ii', 'Through which microscopic structures does water enter a plant from the soil?', 'Root hairs', 'root-hairs'),
        ('iii', 'By what process does water enter a plant?', 'Osmosis', 'osmosis-into-roots'),
        ('iv', 'Explain the term transpiration.', 'Loss of water (vapour) through leaves of plant', 'transpiration')]
] + [
    T('15cv1', 'Q15(c)(v)1', 'C', ask(13, '1. What are growth regulators in plants?'),
      [pt(S('Chemicals that control growth (in plants)'), 3)], 'bio-2-4', 'growth-regulators',
      at(11, 15, '(c )', '(v)'), 3, stem=[Q15C], decision=EACH_ITEM + ' Item 1 one point.'),
    T('15cv2', 'Q15(c)(v)2', 'C', ask(13, '2. Give two examples of the use of plant growth regulators.'),
      [pt(S('Two examples (within the plant or as commercial uses)'), 6, kind='criterion', units=[3, 3], note=NO_ANSWER)],
      'bio-2-4', 'uses-of-growth-regulators', at(11, 15, '(c )', '(v)'), 6, stem=[Q15C],
      decision=EACH_ITEM + ' Item 2 two points ("2 pts") for the scheme\'s "Two examples (within the plant or as '
                           'commercial uses)", what earns them: one criterion row.'),
    T('15cvi', 'Q15(c)(vi)', 'C', Q(13, 'Plants have evolved certain adaptations that protect them from adverse conditions.',
                                     'List two such adaptations.'),
      [anyn(S('waxy layer or opening and closing of', 'stomata or thorns or stings'), 2, 3, sep=' or ', open_list=True)],
      'bio-2-4', 'protective-adaptations-of-plants', at(11, 15, '(c )', '(vi)'), 6, stem=[Q15C],
      decision='Two points ("2pts") from the scheme\'s examples after its "Two adaptations: e.g.", joined by "or": one '
               'menu cut at its own "or", claim two.'),
]

# Section C (b) and (c) of Q10-Q13 are fixed points beside their question's
# "7 + 2(1)" ladder, and Q6's pyramid is fixed beside "4(3) ... + 2": their
# units count to the ladder as fixed, their cards keep their own marks.
LADDER_EXEMPT = {t['key'] for t in TASKS if t['sec'] == 'C' and parse_ref(t['ref'])[0] in (10, 11, 12, 13)
                 and parse_ref(t['ref'])[1] in ('b', 'c')} | {'6biv'}

FIGURES = {
    # key suffix: (doc, page, rect in PDF points, credit, letters, alt, solution[, masks])
    'q3-female': ('paper', 3, (184, 66, 444, 259), SEC, ['A', 'B', 'C', 'D', 'E'], 'Drawing of the human female reproductive system seen from the front: a broad central organ with thick shaded walls around a narrow cavity shaped like an upside-down triangle, narrowing below into a neck that opens into a tube running down to the bottom edge; from each upper corner a long curved tube with a white channel arches outwards and down to a fringed open end beside an oval body, one on each side. A points to the tube at the bottom, B to the thick wall of the central organ, C to the oval body on the left, D to the curved tube at the upper right, E to the inner lining of the central cavity.', False),
    'q4-table': ('paper', 3, (40, 517, 590, 776), SEC, [], 'Question 4 as printed: the instruction, then the list Skin graft, Dermal, Organ, Leaf, Tissue (struck through), In vitro growth above a two-column table: Column A lists "A group of cells with the same function" (answered Tissue in Column B as the example) and parts (a) to (e); Column B is blank beside them.', False),
    'q5-bacteria': ('paper', 4, (114, 57, 384, 176), SEC, ['A', 'B', 'C'], 'Three bacterial shapes: A, a long, thin, wavy strand; B, a single elongated shape with rounded ends; C, a curved chain of small round cells.', False),
    'q6-chain': ('paper', 4, (95, 503, 380, 527), SEC, [], 'The food chain as printed: Grass, an arrow, Rabbit, an arrow, Fox.', False),
    'q10-cell': ('paper', 8, (185, 312, 445, 442), SEC, [], 'Drawing of a cell undergoing division: a round cell with a small dot at its top and at its bottom, the top one labelled Centriole; curved fibres run between the two dots, one labelled Spindle fibre; four X-shaped bodies are lined up across the middle of the cell on the fibres, the right-hand one labelled Chromosome and the point where its arms cross labelled Centromere.', False),
    'q11-meerkat': ('paper', 9, (205, 134, 405, 293), SEC, [], 'Black-and-white photograph of a meerkat, its head and upper body in profile facing right, against a dark background.', False),
    'q12-nervous': ('paper', 10, (424, 96, 592, 362), SEC, ['A', 'B'], 'Outline drawing of a human figure from the front showing the nervous system: a dark mass in the head, a line running from it down the middle of the back, and many fine branching lines spreading from that line through the trunk, arms and legs. A points to the dark mass in the head, B to the line down the middle of the back.', False),
    'q13-leaf': ('paper', 11, (140, 167, 410, 352), SEC, ['A', 'B'], 'Drawing of a section through a leaf: a row of flat cells along the top surface and another along the bottom, a layer of tall, closely packed, column-shaped cells under the top row, loosely arranged rounded cells with spaces between them below that, and a round bundle of small thick-walled cells in the middle. B points to the layer of tall column-shaped cells; A points to a gap between two cells in the bottom row.', False),
    'q14-arm': ('paper', 12, (138, 76, 396, 249), SEC, ['A', 'B'], 'Drawing of the bones and muscles of a human arm bent at the elbow, the upper arm upright and the forearm level, with a flat bone at the top labelled Shoulder blade and a forearm bone labelled Radius. A points to the muscle on the front of the upper arm (the side the forearm points to), B to the muscle on the back of the upper arm.', False),
    'q14-male': ('paper', 12, (361, 555, 580, 733), SEC, ['A', 'B', 'C', 'D'], 'Side-view drawing of the human male reproductive system: a rounded sac at the top; small glands, one lumpy and one coiled, behind and below it; a tube that loops up from a pouch at the bottom, over the sac and down again into a long organ hanging at the front; and an oval body inside the pouch with a coiled structure on its side. A points to the outer edge of the long organ at the front, B to the tube running down inside that organ, C to the tube looping up from the pouch, D to the oval body inside the pouch.', False, [(361, 552, 385, 568)]),
    'q15-eye': ('paper', 13, (214, 69, 402, 217), SEC, ['A', 'B'], 'Section through the human eye: a round eyeball with layered walls, a clear oval body near the front held between two dark bands, a curved clear bulge at the very front, and a thick stalk leaving the back of the eye at the right. B points to the clear oval body near the front; A points to the inner layer lining the back wall of the eye.', False),
    'q15-plant': ('paper', 13, (278, 452, 446, 618), SEC, [], 'A leafy plant with its roots in a test tube of liquid: the shoot above the tube is labelled Stem and leaves, a layer on top of the liquid near the mouth of the tube is labelled Oil, and the liquid round the roots is labelled Red dye in water.', False),
}
