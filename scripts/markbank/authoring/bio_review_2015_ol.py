"""Biology 2015 Ordinary Level — reviewed task ledger, carded from the paper for the first time.

Independent visual sweep (2026-10-25), every page rendered and read:
  * The 2015 paper is one booklet (M43), 16 pages: p1 cover and instructions,
    p2-p4 Section A Questions 1-6, p5-p7 Section B Questions 7-9, p8-p13
    Section C Questions 10-15, p14-p16 "Blank Page". Sections A and B are
    answered on the paper; Section C in an answer book. No acknowledgements
    page: the Q15(a) fruit photographs and every drawing carry no credit (the
    Q11(c) passage prints its own source line, "[Adapted from an article Irish
    Owls from ENFO Ireland]").
  * The marking scheme, 12 pages: p1 cover, p2 note, p3 introduction,
    cancelled and surplus answers, p4 surplus answers continued and the
    conventions, p5-p10 Questions 1-15 (one table, no page numbers), p11
    "Blank Page", p12 back cover.

The paper keeps the long-standing shape: any five of Section A's six
questions, any two of Section B's three, any four of Section C's six, and
Questions 14 and 15 are each any two of (a), (b), (c). Every printed ask is
carded. No Biology card existed for 2015 Ordinary before this review.

This scheme prints no reprint of any question: each answer stands under its
own question number, letter and roman. A task is anchored on its own part
marker, found by walking the scheme's numbering down to it (SQ path). Where
the text layer sets a roman's marker on its answer's own line ("(vii) Valves
(closing)") the marker is a welded bare anchor and the row is read from that
line. The text layer reads three answers away from their markers: Q10(b)(i)'s
order and its marker at the foot of p7, and the markers of Q15(a)(i) and
Q15(b)(i) at the foot of p10 after their own "(3 pts)" and "(4 pts)" cells.
Those are anchored by walking through the cell printed in their own row, and
their answers are read with `after=` from the line printed before them.
Q3(e)'s marker is printed "(e )", with a space, which the anchor check does
not read as a marker: it is anchored on (d)'s marker and its answer read from
there.

The scheme counts POINTS ("(1 pt)", "(2 pts)") and heads each question or
part with what they are worth. Ordered splits are carded at their first
rate: Q1 and Q4 "2(7)+3(2)" over five points, Q2, Q3, Q5 and Q6 "2(5) +
5(2)" over seven, every Section B (a) "5 + 1" over two, and every Section C
(a) of Q10-Q13 "7 + 2(1)" over three. Section B (b) is "8(3)", Section C (b)
"9(3)" (Q10(b) "3(5)+4(3)", printed against its rows: "3(5)" beside (i)'s
"[Any three correctly placed]", "4(3)" over (ii)-(iv)), (c) "8(3)", and every
part of Q14 and Q15 "10(3)": a fixed mark per point. Q14(c)(i) and Q15(c)(i)
price their drawings on their own row, "3,0 + 3(1) (Non-sliding)" and
"6,3,0 + 3(2) (non-sliding)", beside the rest of the part's points at 3. A
Section C (a) ladder sits beside its question's fixed (b) and (c), so each
such ladder names their units as fixed and their cards are exempt from its
notation. Every printed answer fits a per-response tariff, so no part is
carded whole.

The census reader lost Question 15's three letters (paper.py WELDED_HEADS,
gated to this sitting): page 13 sets "(a)" on a line of its own under the
head "15. Answer any two of (a), (b), (c). (30, 30)", the text layer reads it
into the head's block, and with no (a) read, (b) and (c) were not taken as
letters; all eighteen romans filed as six romans of a letterless Q15. The fix
takes the census from 129 leaves to the paper's 141.
"""
from bio_review_lib import Q, SQ, S, M, pt, anyn, T, L, parse_ref

YEAR, LEVEL = 2015, 'ol'
REVIEWED_AT = '2026-10-25'

SOURCES = {
    'paper': {'path': 'examiner-reports/biology/papers/2015-ol-paper.pdf',
              'fileid': 'LC025GLP000EV.pdf',
              'sha256': '6ac18153d414adddbee7e7add1e5fe2c2c2b51eb288ca86870ed858f18cb3686',
              'pages': 16},
    'scheme': {'path': 'examiner-reports/biology/schemes/2015-ol.pdf',
               'fileid': 'LC025GLP000EV.pdf',
               'sha256': '100ba10d216acd682eb151e7be83b7622ded2b1097e9788a7a3a12d133d21080',
               'pages': 12},
}

PAGE_ROLES = {
    'paper': {1: 'cover', **{p: 'questions' for p in range(2, 14)}, 14: 'blank', 15: 'blank', 16: 'blank'},
    'scheme': {1: 'cover', 2: 'note', 3: 'introduction', 4: 'conventions',
               **{p: 'marking' for p in range(5, 11)}, 11: 'blank', 12: 'back-cover'},
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
    **{(n, 'b'): 24 for n in (7, 8, 9)},   # p5: "part (b) carries 24 marks"; "8(3)"
    **{(n, x): t for n in range(10, 14) for x, t in (('b', 27), ('c', 24))},
    **{(n, x): 30 for n in (14, 15) for x in 'abc'},
}
LADDERS = {
    1: _ladder('2(7)+3(2)'), 4: _ladder('2(7) + 3(2)'),
    **{q: _ladder('2(5) + 5(2)') for q in (2, 3, 5, 6)},
    **{(n, 'a'): _ladder('5 + 1') for n in (7, 8, 9)},
    # Section C (a) "7 + 2(1)"; (b) and (c) are fixed points beside it, named
    # here so the question's total is the ladder's. Q10(b) is "3(5)+4(3)".
    (10, 'abc'): _ladder('7 + 2(1)', fixed={5: 3, 3: 12}),
    **{(n, 'abc'): _ladder('7 + 2(1)', fixed={3: 17}) for n in (11, 12, 13)},
}

CHECKSUMS = {
    1: {7: 5}, 4: {7: 5}, **{q: {5: 7} for q in (2, 3, 5, 6)},
    **{(n, 'a'): {5: 2} for n in (7, 8, 9)}, **{(n, 'b'): {3: 8} for n in (7, 8, 9)},
    **{(n, 'a'): {7: 3} for n in range(10, 14)},
    (10, 'b'): {5: 3, 3: 4}, **{(n, 'b'): {3: 9} for n in (11, 12, 13)},
    **{(n, 'c'): {3: 8} for n in range(10, 14)},
    (14, 'a'): {3: 10}, (14, 'b'): {3: 10}, (14, 'c'): {3: 9, 1: 3},
    (15, 'a'): {3: 10}, (15, 'b'): {3: 10}, (15, 'c'): {6: 1, 2: 3, 3: 6},
}

SCAN_PAGES = {'paper': range(1, 14)}
SELECTION_SCAN = [
    ('paper', 1, 'any five', 'Cover rubric, Section A: whole-question choice; every question is carded.'),
    ('paper', 1, 'any two', 'Cover rubric, Section B: whole-question choice; every question is carded.'),
    ('paper', 1, 'any four', 'Cover rubric, Section C: whole-question choice; every question is carded.'),
    ('paper', 2, 'any five', 'Section A rubric repeated.'),
    ('paper', 2, 'the following', 'Q1 lead-in: every part asked, one card per letter.'),
    ('paper', 2, 'the following', 'Q2 lead-in: every statement asked, one card per letter.'),
    ('paper', 2, 'or', 'Q2 "true (T) or false (F)": the answer options.'),
    ('paper', 2, 'or', 'Q2 "T or F": the answer options.'),
    ('paper', 2, 'or', 'Q2(b) statement "in test tubes or Petri dishes": the statement\'s own words.'),
    ('paper', 3, 'or', 'Q3(b) "asexual or sexual reproduction": the answer options.'),
    ('paper', 3, 'choose', 'Q4 "Choose each term": every description matched, one card per lettered part.'),
    ('paper', 3, 'the following', 'Q4 list of terms: the options.'),
    ('paper', 4, 'the following', 'Q5 lead-in: every part asked, one card per letter.'),
    ('paper', 4, 'the following', 'Q6 lead-in: every part asked, one card per letter.'),
    ('paper', 4, 'or', 'Q6(a) "released or absorbed": the answer options.'),
    ('paper', 5, 'any two', 'Section B rubric repeated.'),
    ('paper', 5, 'the following', 'Q7(b) lead-in: every part asked.'),
    ('paper', 6, 'the following', 'Q8(b) lead-in: every part asked.'),
    ('paper', 7, 'any one', 'Q9(a)(i) "Give any one base pair": one answer; the scheme prints the two pairs as '
                            'alternatives.'),
    ('paper', 7, 'or', 'Q9(a)(ii) "changes in DNA or chromosomes": description.'),
    ('paper', 7, 'the following', 'Q9(b) lead-in: every part asked.'),
    ('paper', 8, 'any four', 'Section C rubric repeated.'),
    ('paper', 8, 'the following', 'Q10(a) lead-in: every term asked, one card per roman.'),
    ('paper', 8, 'the following', 'Q10(b)(i) "the following steps": the four steps to be ordered; one card.'),
    ('paper', 8, 'the following', 'Q10(c) "Copy the following": every line of the cross asked, one card per line.'),
    ('paper', 9, 'the following', 'Q11(a) lead-in: every term asked, one card per roman.'),
    ('paper', 9, 'or', 'Q11(b)(vi) "damaged or harmed": description.'),
    ('paper', 9, 'or', 'Q11(c) passage "mice or rats": passage text.'),
    ('paper', 9, 'or', 'Q11(c) passage "barns or old buildings": passage text.'),
    ('paper', 10, 'the following', 'Q12(a)(ii) "each of the following": both items asked, one card each.'),
    ('paper', 10, 'or', 'Q12(a)(ii) "mechanical or chemical digestion": the answer options.'),
    ('paper', 10, 'or', 'Q12(c) passage "Irritable bowel syndrome or IBS": passage text.'),
    ('paper', 11, 'or', 'Q13(b)(iii) "oxygenated or deoxygenated": the answer options.'),
    ('paper', 12, 'any two', 'Q14 "any two of (a), (b), (c)": whole-part choice; every part is carded.'),
    ('paper', 12, 'or', 'Q14(a)(ii)1 "a plant cell or an animal cell": the answer options.'),
    ('paper', 12, 'or', 'Q14(a)(v) "selectively permeable or semi-permeable": description.'),
    ('paper', 13, 'any two', 'Q15 "any two of (a), (b), (c)": whole-part choice; every part is carded.'),
    ('paper', 13, 'or', 'Q15(a)(v) "seeds or fruits": description.'),
]

ROUTES = {}

SEC = 'State Examinations Commission'
NO_REPRINT = 'The scheme prints no reprint of any question: anchored on the part\'s own marker.'
WELDED = ('The scheme prints no reprint and sets this part\'s marker on its answer\'s own line: anchored on that '
          'marker.')
EACH_ITEM = 'A list the scheme prices entry by entry: one card per entry, each its own slice of the printed line.'
NO_ANSWER = 'The scheme prints no answer here, only what earns the marks.'
TWO_POINTS = 'The scheme prices this part at two points: each printed point its own row.'
CROSS_ROMANS = ('The scheme prints no reprint and numbers the cross\'s printed lines (i) to (iii), a numbering the '
                'paper does not print: anchored on the scheme\'s own marker over the line\'s answer.')
FOOT = ('The text layer reads this part\'s marker at the foot of the scheme page, after the "{cell}" cell printed in '
        'its own row: anchored on the marker reached through that cell, its answer read from the line printed '
        'before it.')


def at(page, q, *path_and_marker, why=NO_REPRINT, nth=1):
    """The part's own marker under its question (and letter) on the scheme page."""
    *path, marker = path_and_marker
    return SQ(page, marker, path=[str(q), *path], paired=why, bare=True, nth=nth)


def welded(page, q, *path_and_marker):
    """The part's marker opening its own answer line ("(vii) Valves (closing)")."""
    *path, marker = path_and_marker
    return SQ(page, marker, path=[str(q), *path], paired=WELDED, bare=True, welded=True)


def ask(page, sentence, **kw):
    """A one-line ask closed by its own punctuation, before its answer line."""
    return Q(page, sentence, sentence, **kw)


def dots(page, sentence, **kw):
    """An ask whose closing mark runs straight into its printed answer dots ("...reproduction?......"):
    the line cut at the dots."""
    return Q(page, sentence, piece=1, psep='..', **kw)


def cell(line, i, cuts, page=None, meaning=False, after=None, end=None):
    """Cell i of a scheme line printed as cells ("A = Ovary B = Anther C = Petal"), cut at the
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
    return S(line, end, page=page, piece=pieces, psep=seps, after=after)


def labels(cells, page, asked=None):
    """A figure's label key from its scheme cells: [(letter, line, i, cuts, end, after)]."""
    return [L(x, cell(line, i, cuts, page=page, meaning=True, after=after, end=end), x == asked)
            for x, line, i, cuts, end, after in cells]


def bracket(line, end=None, after=None):
    """A scheme answer and its square-bracketed direction, cut at the bracket: (answer, note)."""
    sel = (line, end) if end else (line,)
    return (S(*sel, piece=1, psep=' [', after=after), S(*sel, piece=[2, 1], psep=[' [', ']'], after=after))


def plain(line, marks, end=None, after=None, **kw):
    """One answer whose square-bracketed direction ("[accept stamen]") is the row's note."""
    ans, note = bracket(line, end, after)
    return pt(ans, marks, note_sel=note, **kw)


def own_note(line, marks, **kw):
    """An answer followed on its own line by the scheme's bracketed direction."""
    return pt(S(line), marks, note_sel=S(kw.pop('note_line'), piece=[2, 1], psep=['[', ']']), **kw)


def labelled(line, marks, **kw):
    """A scheme row printed "Label : answer" (with spaces round its colon): label and answer cut there."""
    return pt(S(line, piece=2, psep=' : '), marks, label=S(line, piece=1, psep=' : '), **kw)


# ------------------------------------------------------------ question text --
Q1 = Q(2, 'Use your knowledge of nutrition to answer the following questions.')
Q2 = Q(2, 'Indicate whether the following statements are true (T) or false (F) by drawing a circle around',
       'T or F in each case.')
Q3 = Q(3, 'The diagram shows a vertical section through a flower.')
Q4 = Q(3, 'Choose each term from the following list and place it in Column B to match a description in',
       'Column A. The first one has been completed as an example.')
Q5 = Q(4, 'Use your knowledge of ecology to answer the following:')
Q6 = Q(4, 'Use your knowledge of photosynthesis to answer the following:')
Q6B = ask(4, 'Name the green pigment found in plants that is necessary for photosynthesis.')
Q7B = Q(5, 'Answer the following questions in relation to your investigation into the growth of leaf yeast.')
Q8B = Q(6, 'Answer the following questions in relation to practical work you carried out to investigate',
        'the conditions necessary for seed germination.')
Q9B = Q(7, 'Answer the following in relation to practical work you carried out to isolate DNA from plant', 'tissue.')
Q9BII = [Q(7, 'Below is a list of some of the steps carried out during the practical work but they are not',
           'in the correct order.'),
         Q(7, 'A. Pour freezer-cold ethanol down the inside of the test tube containing the filtered', 'plant extract.',
           br=True),
         ask(7, 'B. Add the mixture of the plant tissue, salt and washing up liquid to a blender.', br=True),
         ask(7, 'C. Chop the plant tissue into small pieces.', br=True),
         ask(7, 'D. Add 2 – 3 drops of protease to the filtered plant extract.', br=True),
         ask(7, 'Indicate below, using the letters A, B, C and D, the correct order of the above steps.', br=True)]
Q10A = Q(8, 'Explain the following terms used in genetics:')
Q10C = [Q(8, 'In snapdragon plants, the allele for red flower (R) is incompletely dominant to the',
          'A pink-flowered snapdragon is crossed with a white-flowered snapdragon.'),
        Q(8, 'Copy the following into your answer book and fill in the blank spaces appropriately:'),
        Q(8, 'Pink White', br=True)]
CROSS = [Q(8, 'Genotypes of parents', br=True), Q(8, 'Possible gametes', br=True),
         Q(8, 'Genotypes of offspring', br=True), Q(8, 'Matching phenotypes of offspring', br=True)]
Q11A = Q(9, 'Explain the following terms used in ecology:')
Q11B = Q(9, 'During your study of ecology you carried out a quantitative survey to estimate the population of',
         'a particular animal in an ecosystem.')
Q11BIII = Q(9, 'On another day you collected animals in the same location.',
            'How many animals might you have collected on that second day?')
Q11C = [Q(9, 'Read the passage below and answer the questions that follow:'),
        Q(9, 'The barn owl is a species whose numbers have greatly decreased in Ireland over the last number',
          'food and poisoning from pesticides.')]
Q12AII = Q(10, 'Mechanical digestion and chemical digestion are two types of digestion.',
           'State whether each of the following is involved in mechanical or chemical digestion.')
Q12B = Q(10, 'The diagram shows the human digestive system.')
Q12C = Q(10, 'Irritable bowel syndrome or IBS is a common problem associated with the digestive system.',
         'including medication and changing the diet.')
Q13B = Q(11, 'The diagram shows a human heart.')
Q13C = Q(11, 'The diagram shows part of the human breathing system.')
Q14A = Q(12, 'The diagram shows a cell.')
Q14AII1 = [M('1.', 12), ask(12, 'Does the diagram shown above represent a plant cell or an animal cell?')]
Q15B = Q(13, 'The diagram shows the human skin.')
Q15CII = ask(13, 'What term is used to describe the nutrition of Rhizopus?')

# ------------------------------------------------------- scheme cell lines --
FLOWER = ('A = Ovary B = Anther C = Petal', [(' B =', 'Ovary '), (' C =', 'Anther ')])
DIGEST1 = ('A = Duodenum (or small Intestine); B = Liver', [('; ', '; ')])
DIGEST2 = ('C = Stomach; D = Pancreas; E = Colon (or large intestine)', [('; ', 'Stomach; '), ('; ', 'Pancreas; ')])
HEART = ('A = Aorta B = Septum C = Right atrium', [(' B =', 'Aorta '), (' C =', 'Septum ')])
LUNGS1 = ('A = Larynx (or voice box) B = Trachea (or windpipe)', [(' B =', 'box) ')])
LUNGS2 = ('C = Bronchus D = Alveolus (or air sac(s))', [(' D =', 'Bronchus ')])
CELL1 = ('A = Cell membrane B = Cell Wall', [(' B =', 'membrane ')])
CELL2 = ('C = Chloroplast or mitochondrion D = Vacuole', [(' D =', 'mitochondrion ')])
SKIN1 = ('A = Hair B = Blood vessel (or artery or vein or arteriole or', [(' B =', 'Hair ')],
         'venule) [do not accept capillary]')
SKIN2 = ('C = Sweat gland D = (Erector) muscle', [(' D =', 'gland ')])
FRUITS = ('Blackberry = animal Sycamore = wind', [(' Sycamore =', 'animal ')])
# Read after the line printed before them: the text layer sets Q10(b)(i)'s order
# at the foot of p7, and Q15(a)(i)'s and Q15(b)(i)'s markers at the foot of p10.
BEFORE_10BI = 'Eating poisoned prey'
BEFORE_15AI = '10(3)'
BEFORE_15BI = 'Disadvantage : No variety or all susceptible to same diseases'
GE_ORDER = '1. Isolation; 2. Cutting; 3. Transformation; 4. Expression'
CROSS_NOTE = S('[accept gametes and offspring genotypes if shown in Punnett square]', piece=[2, 1], psep=['[', ']'])
OWL_FORMULA = 'A = number given in (iii)'
RHIZOPUS = ('Diagram + 3 labels [Diagram to include hypha(e) or stolon(s);',
            'minimum of 2 rhizoids; sporangium; sporangiophore ]')


def flower_labels(asked=None):
    return labels([(x, FLOWER[0], i, FLOWER[1], None, None) for i, x in enumerate('ABC')], 5, asked)


def digest_labels(asked=None):
    return labels([(x, DIGEST1[0], i, DIGEST1[1], None, None) for i, x in enumerate('AB')]
                  + [(x, DIGEST2[0], i, DIGEST2[1], None, None) for i, x in enumerate('CDE')], 8, asked)


def heart_labels(asked=None):
    return labels([(x, HEART[0], i, HEART[1], None, None) for i, x in enumerate('ABC')], 8, asked)


def lung_labels(asked=None):
    return labels([(x, LUNGS1[0], i, LUNGS1[1], None, None) for i, x in enumerate('AB')]
                  + [(x, LUNGS2[0], i, LUNGS2[1], None, None) for i, x in enumerate('CD')], 8, asked)


def cell_labels(asked=None):
    return labels([(x, CELL1[0], i, CELL1[1], None, None) for i, x in enumerate('AB')]
                  + [(x, CELL2[0], i, CELL2[1], None, None) for i, x in enumerate('CD')], 9, asked)


def skin_labels(asked=None):
    # B's cell runs onto a second printed line and closes on the scheme's
    # bracketed "do not accept capillary", which is no part of its name.
    a = L('A', S(SKIN1[0], SKIN1[2], page=10, piece=[1, 2], psep=[' B =', ' = '], after=BEFORE_15BI), asked == 'A')
    b = L('B', S(SKIN1[0], SKIN1[2], page=10, piece=[2, 1, 2], psep=['Hair ', ' [', ' = '], after=BEFORE_15BI),
          asked == 'B')
    return [a, b] + labels([(x, SKIN2[0], i, SKIN2[1], None, BEFORE_15BI) for i, x in enumerate('CD')], 10, asked)


TASKS = [
    # ------------------------------------------------------------ Section A --
] + [
    T(f'1{x}', f'Q1({x})', 'A', q, [row], 'bio-1-2', concept, at(5, 1, f'({x})'), 7, stem=[Q1])
    for x, q, row, concept in [
        ('a', Q(2, 'Carbohydrates are composed of carbon, hydrogen and', piece=1, psep='..'), pt(S('Oxygen'), 7),
         'elements-in-carbohydrates'),
        ('b', Q(2, 'Vitamins B and C are', 'soluble vitamins.'), pt(S('Water'), 7), 'water-soluble-vitamins'),
        ('c', ask(2, 'Give one difference between fats and oils at room temperature.'),
         pt(S('Fats are solid or oils are liquid'), 7), 'fats-and-oils'),
        ('d', Q(2, 'In food tests, Benedict’s/Fehling’s solution is used to test for the presence of'),
         pt(S('Reducing sugar (or named reducing sugar)'), 7), 'test-for-reducing-sugar'),
        ('e', ask(2, 'Name one mineral needed by plants.'), pt(S('Magnesium or calcium or any other correct mineral'), 7),
         'minerals-for-plants')]
] + [
    T(f'2{x}', f'Q2({x})', 'A', ask(2, q), [pt(S(ans), 5)], topic, concept, at(5, 2, f'({x})'), 5, stem=[Q2])
    for x, q, ans, topic, concept in [
        ('a', 'Tissues are made of organs.', 'FALSE', 'bio-1-3', 'tissues-and-organs'),
        ('b', 'Tissue culture is the growth of tissue in test tubes or Petri dishes.', 'TRUE', 'bio-1-3',
         'tissue-culture'),
        ('c', 'Human skin tissue will grow best at 10 °C.', 'FALSE', 'bio-1-3', 'temperature-for-tissue-culture'),
        ('d', 'Cells will grow only in a sterile medium.', 'FALSE', 'bio-1-3', 'sterile-medium'),
        ('e', 'Tissue culture is used in micropropagation.', 'TRUE', 'bio-1-3', 'micropropagation'),
        ('f', 'Cancer is the controlled growth of cells.', 'FALSE', 'bio-2-3', 'cancer'),
        ('g', 'Chemotherapy is used as a cancer treatment.', 'TRUE', 'bio-2-3', 'chemotherapy')]
] + [
    T(f'3a-{x.lower()}', 'Q3(a)', 'A', ask(3, 'Name the parts labelled A, B and C.'), [pt(cell(FLOWER[0], i, FLOWER[1]), 5)],
      'bio-2-5', concept, at(5, 3, '(a)'), 5, stem=[Q3], fig='q3-flower', item=(x.lower(), x),
      labels=flower_labels(x), decision=EACH_ITEM + ' Three points of the "2(5) + 5(2)" ladder, one per label.')
    for i, (x, concept) in enumerate([('A', 'ovary'), ('B', 'anther'), ('C', 'petal')])
] + [
    T('3b', 'Q3(b)', 'A', dots(3, 'Is the flower an organ for asexual or sexual reproduction?'), [pt(S('Sexual'), 5)],
      'bio-2-5', 'flowers-are-for-sexual-reproduction', at(5, 3, '(b)'), 5, stem=[Q3], fig='q3-flower'),
    T('3c', 'Q3(c)', 'A', dots(3, 'What part of the flower produces pollen?'),
      [pt(S("Anther [accept stamen] or 'B' [accept what candidate has called", "'B' in part (a) ]"), 5)], 'bio-2-5',
      'pollen-production', at(5, 3, '(c)'), 5, stem=[Q3], fig='q3-flower', labels=flower_labels(),
      decision='The scheme sets a bracketed direction inside each of its two alternatives ("Anther [accept stamen] or '
               '\'B\' [accept ...]"): the printed answer is one row, read whole.'),
    T('3d', 'Q3(d)', 'A', ask(3, 'How do the parts labelled C help the flower in reproduction?'),
      [pt(S('Attract insects or attract pollinators (or named pollinator)'), 5)], 'bio-2-5', 'role-of-petals',
      at(5, 3, '(d)'), 5, stem=[Q3], fig='q3-flower', labels=flower_labels()),
    T('3e', 'Q3(e)', 'A', dots(3, 'In which labelled part does fertilisation take place?'),
      [plain("A or ovary [accept what candidate has called 'A' in part (a) ]", 5)], 'bio-2-5', 'site-of-fertilisation',
      at(5, 3, '(d)', why='The scheme prints this part\'s marker "(e )", with a space, which the anchor check does not '
                          'read as a marker: anchored on (d)\'s marker, the marker printed before it, and its answer '
                          'read from there.'),
      5, stem=[Q3], fig='q3-flower', labels=flower_labels()),
] + [
    T(f'4{x}', f'Q4({x})', 'A', Q(3, *q), [pt(S(ans), 7)], 'bio-2-4', concept, at(5, 4, f'({x})'), 7,
      stem=[Q4], qfig='q4-table',
      decision='The list of terms (its "Fluid balance" struck through as the worked example) and the table are shown '
               'as the question\'s own print.')
    for x, q, ans, concept in [
        ('a', ('An example of an animal whose body temperature', 'changes with its environment'), 'Lizard', 'ectotherms'),
        ('b', ('A term for maintaining a constant internal environment', 'in the body'), 'Homeostasis', 'homeostasis'),
        ('c', ('An organ that has a role in maintaining a constant', 'internal environment in the body'), 'Skin',
         'skin-in-homeostasis'),
        ('d', ('A term for an animal that generates its own body heat', 'A term for an animal that generates its own body heat'),
         'Endotherm', 'endotherm'),
        ('e', ('An example of an animal that generates its own body', 'heat'), 'Rabbit', 'endotherm-example')]
] + [
    T(f'5{x}', f'Q5({x})', 'A', ask(4, q), [row], 'bio-3-1', concept, at(5, 5, f'({x})'), total, stem=[Q5],
      fig=None if x == 'c' else 'q5-foodweb', decision=decision)
    for x, q, row, concept, total, decision in [
        ('a', 'What name is given to the above diagram?', pt(S('Food web'), 5), 'food-web', 5, ''),
        ('b', 'What do the arrows on the diagram mean?', pt(S('"Eaten by" or energy flow or food chains'), 5),
         'arrows-in-a-food-web', 5, ''),
        ('c', 'Green plants are producers. What does this mean?', pt(S('Make their own food or carry out photosynthesis'), 5),
         'producers', 5, ''),
        ('d', 'Name two primary consumers from the above diagram.', anyn(S('Greenfly/ caterpillar/ snail/ mouse/ rabbit'), 2, 5),
         'primary-consumers', 10,
         'Two points ("(2 pts)") from the printed list: one menu, claim two, each response at the ladder\'s first rate.'),
        ('e', 'Name a carnivore from the above diagram.',
         pt(S('Ladybird or blackbird or hedgehog or stoat or fox or', 'sparrowhawk'), 5), 'carnivores', 5, ''),
        ('f', 'To which trophic level does the hedgehog belong?', pt(S('3rd or secondary consumer'), 5),
         'trophic-level', 5, '')]
] + [
    T(f'6{x}', f'Q6({x})', 'A', q, [row], 'bio-2-2', concept, at(5, 6, f'({x})'), total, stem=stem, decision=decision)
    for x, q, row, concept, total, stem, decision in [
        ('a', ask(4, 'Is energy released or absorbed during photosynthesis?'), pt(S('Absorbed'), 5),
         'photosynthesis-absorbs-energy', 5, [Q6], ''),
        ('b', Q6B, pt(S('Chlorophyll'), 5), 'chlorophyll', 5, [Q6], ''),
        ('c', ask(4, 'Where is this pigment found in plant cells?'), pt(S('Chloroplasts'), 5), 'chloroplasts', 5,
         [Q6, M('(b)', 4), Q6B], ''),
        ('d', ask(4, 'Name two other factors a plant needs for photosynthesis.'),
         anyn(S('Water/ carbon dioxide/ light/ enzymes/ suitable temperature (or', 'warmth [do not accept heat])'), 2, 5),
         'factors-for-photosynthesis', 10, [Q6],
         'Two points ("(2 pts)") from the printed list: one menu, claim two, each response at the ladder\'s first rate.'),
        ('e', ask(4, 'What gas is released during photosynthesis?'), pt(S('Oxygen'), 5), 'oxygen-from-photosynthesis',
         5, [Q6], ''),
        ('f', dots(4, 'What substance is split into electrons, oxygen and protons during photosynthesis?'),
         pt(S('Water'), 5), 'splitting-water', 5, [Q6], '')]
] + [
    # ------------------------------------------------------------ Section B --
    T('7ai', 'Q7(a)(i)', 'B', ask(5, 'What term is used to describe asexual reproduction in yeast?'),
      [pt(S('Budding'), 5)], 'bio-3-2', 'budding', at(6, 7, '(a)', '(i)'), 5,
      decision='"5 + 1" over (a)\'s two parts, each carded at its first rate.'),
    T('7aii', 'Q7(a)(ii)', 'B', Q(5, 'Explain the term sterile as it applies in microbiology', piece=1, psep=' …'),
      [pt(S('Free from micro-organisms'), 5)], 'bio-3-2', 'sterile', at(6, 7, '(a)', '(ii)'), 5,
      decision='The paper runs this ask straight into its answer line, with no full stop: the ask is cut at the line.'),
] + [
    T(f'7b{r}', f'Q7(b)({r})', 'B', q, rows, 'bio-3-2', concept, at(6, 7, '(b)', f'({r})'), 3 * len(rows),
      stem=[Q7B], decision=decision)
    for r, q, rows, concept, decision in [
        ('i', ask(5, 'From the leaves of which plant did you obtain the yeast?'),
         [pt(S('Any named tree or shrub'), 3, kind='criterion', note=NO_ANSWER)], 'source-of-leaf-yeast', ''),
        ('ii', ask(5, 'When collecting the leaves, what did you do to try to keep them free from contamination?'),
         [pt(S('Wear gloves or handled leaves with e.g. tweezers or put into', 'plastic bag'), 3)],
         'collecting-leaves-aseptically', ''),
        ('iii', ask(5, 'Name the nutrient medium on which you grew the yeast.'), [pt(S('(Malt) agar'), 3)],
         'nutrient-medium', ''),
        ('iv', ask(5, 'Outline the steps you followed in the laboratory to show the presence of the yeast.'),
         [pt(S('One aseptic technique'), 3, kind='criterion', note=NO_ANSWER),
          pt(S('attach leaves or leaf sections to (inside of) lid,', piece=1, psep=','), 3),
          pt(S('incubate'), 3)], 'growing-leaf-yeast',
         'Three points, each printed on its own line with its own "(1 pt)": a row each. The first is the scheme\'s '
         '"One aseptic technique", which names what earns the point; the second is cut at the comma that closes '
         'its printed line.'),
        ('v', ask(5, 'How did you conclude that yeast was present?'),
         [pt(S("Pink colonies or pink with 'colonies' described"), 3)], 'identifying-leaf-yeast', ''),
        ('vi', Q(5, 'At the end of the investigation, how exactly should any remaining material be treated',
                 'before disposal?'),
         [pt(S('e.g. Autoclave or incinerate or soak in disinfectant'), 3)], 'disposal-of-cultures', '')]
] + [
    T('8ai', 'Q8(a)(i)', 'B', ask(6, 'Explain the term germination.'), [pt(S('Growth of seed (into new plant)'), 5)],
      'bio-2-5', 'germination', at(6, 8, '(a)', '(i)'), 5,
      decision='"5 + 1" over (a)\'s two parts, each carded at its first rate.'),
    T('8aii', 'Q8(a)(ii)', 'B', ask(6, 'What part of the germinated seed becomes the root?'), [pt(S('Radicle'), 5)],
      'bio-2-5', 'radicle', at(6, 8, '(a)', '(ii)'), 5),
] + [
    T(f'8b{r}', f'Q8(b)({r})', 'B', q, rows, 'bio-2-5', concept, at(6, 8, '(b)', f'({r})'), 3 * len(rows),
      stem=[Q8B], fig='q8-tubes', decision=decision)
    for r, q, rows, concept, decision in [
        ('i', Q(6, 'Tube A has all the factors needed for germination. Tubes B, C and D lack one',
                'essential factor each. Name the three factors that are present in tube A.'),
         [pt(S('Water/ oxygen/ suitable temperature (or warmth [do not accept', 'heat]'), 3, kind='point')],
         'conditions-for-germination',
         'The scheme prices this part at one point ("(1 pt)") against one printed line naming the three factors: '
         'the line is one row worth that point, read whole.'),
        ('ii', ask(6, 'What is the purpose of the oil in tube D?'), [plain('To exclude oxygen [accept to exclude air]', 3)],
         'purpose-of-the-oil', ''),
        ('iii', ask(6, 'Why were many seeds added to each tube rather than using just one seed in each tube?'),
         [pt(S('Some seeds may fail to germinate'), 3)], 'why-many-seeds', ''),
        ('iv', ask(6, 'Which tube acted as a control?'), [pt(S('A'), 3)], 'germination-control', ''),
        ('v', ask(6, 'State the results of your investigation:'),
         [pt(S(f'Tube {x} - {"" if x == "A" else "no "}germination'), 3) for x in 'ABCD'], 'germination-results',
         'Four points, one per tube, each printed on its own line with its own "(1 pt)": a row each.')]
] + [
    T('9ai', 'Q9(a)(i)', 'B', ask(7, 'Give any one base pair found in DNA.'), [pt(S('A - T or G - C'), 5)], 'bio-1-2',
      'base-pairs', at(6, 9, '(a)', '(i)'), 5, decision='"5 + 1" over (a)\'s two parts, each carded at its first rate.'),
    T('9aii', 'Q9(a)(ii)', 'B', [Q(7, 'Mutations are changes in DNA or chromosomes.'), ask(7, 'State one cause of mutation.')],
      [pt(S('e.g. Radiation or chemicals or named chemicals e.g. cigarette', 'smoke or viruses'), 5)], 'bio-2-3',
      'causes-of-mutation', at(6, 9, '(a)', '(ii)'), 5),
    T('9bi', 'Q9(b)(i)', 'B', ask(7, 'Name a suitable plant for this activity.'), [pt(S('e.g. Onion'), 3)], 'bio-1-2',
      'plant-for-dna-isolation', at(6, 9, '(b)', '(i)'), 3, stem=[Q9B]),
    T('9bii', 'Q9(b)(ii)', 'B', Q9BII,
      [pt(S(ans), 3, label=Q(7, f'Step {n}')) for n, ans in
       enumerate(['C or chop', 'B or add to blender', 'D or add protease', 'A or pour ethanol'], 1)],
      'bio-1-2', 'order-of-dna-isolation', at(6, 9, '(b)', '(ii)'), 12, stem=[Q9B],
      decision='Four points, one per step, each printed in order on its own line with its own "(1 pt)": a row each, '
               'labelled with the paper\'s own "Step 1" to "Step 4" in the order the scheme prints them.'),
    T('9biii', 'Q9(b)(iii)', 'B', ask(7, 'Why was the protease added to the filtered plant extract?'),
      [pt(S('To breakdown protein (in the chromosomes)'), 3)], 'bio-1-2', 'protease-in-dna-isolation',
      at(6, 9, '(b)', '(iii)'), 3, stem=[Q9B]),
    T('9biv', 'Q9(b)(iv)', 'B', ask(7, 'What was the purpose of adding washing up liquid to the mixture?'),
      [pt(S('To breakdown (cell) membranes'), 3)], 'bio-1-2', 'washing-up-liquid-in-dna-isolation',
      at(6, 9, '(b)', '(iv)'), 3, stem=[Q9B]),
    T('9bv', 'Q9(b)(v)', 'B', ask(7, 'What was the purpose of the freezer-cold ethanol?'),
      [pt(S('To bring DNA out of solution (or allows DNA to be seen)'), 3)], 'bio-1-2', 'freezer-cold-ethanol',
      at(6, 9, '(b)', '(v)'), 3, stem=[Q9B]),
    # ------------------------------------------------------------ Section C --
] + [
    # The three terms ("Chromosome.", "Homozygous.", "Phenotype.") alone are too
    # short a question to stand: each card carries the printed lead-in in its
    # question text, as 2016 Ordinary Q10(a) does.
    T(f'10a{r}', f'Q10(a)({r})', 'C', [Q10A, ask(8, term, br=True)], [pt(S(ans), 7)], 'bio-1-4', concept,
      at(7, 10, '(a)', f'({r})'), 7)
    for r, term, ans, concept in [
        ('i', 'Chromosome.', '(Molecule) made of DNA and protein or chain of genes', 'chromosome'),
        ('ii', 'Homozygous.', 'Both alleles the same', 'homozygous'),
        ('iii', 'Phenotype.', 'Physical appearance (of organism) or expression of genotype', 'phenotype')]
] + [
    T('10bi', 'Q10(b)(i)', 'C', [Q(8, 'Genetic engineering involves the following steps:'),
                                  ask(8, 'Transformation, Cutting, Isolation, Expression.', br=True),
                                  ask(8, 'Rewrite these steps, placing them in the correct order.', br=True)],
      [anyn(S(GE_ORDER, after=BEFORE_10BI), 3, 5, sep='; ',
            note_sel=S('[Any three correctly placed ]', piece=[2, 1], psep=['[', ']'], after=BEFORE_10BI))],
      'bio-3-3', 'steps-of-genetic-engineering', at(7, 10, '(b)', '3(5)', '(i)', why=FOOT.format(cell='3(5)')), 15,
      decision='The scheme prints "3(5)" against (i) and "[Any three correctly placed]" under its four placed steps: '
               'one menu of the four placements, cut at the scheme\'s own semicolons, claim three at 5. The (b) '
               'heading "3(5)+4(3)" is printed against its rows, "3(5)" beside (i) and "4(3)" over (ii)-(iv)\'s four '
               'points, so (b) is priced part by part.'),
    T('10bii', 'Q10(b)(ii)', 'C', Q(8, 'In the process of genetic engineering the DNA has to be cut.',
                                    'What is used to cut the DNA?'),
      [pt(S('Enzymes'), 3)], 'bio-3-3', 'restriction-enzymes', at(7, 10, '(b)', '(ii)'), 3),
    T('10biii', 'Q10(b)(iii)', 'C', ask(8, 'During the isolation step, what is taken out of the cell?'),
      [pt(S('Gene(s) or (piece of) plasmid or (piece of) DNA or (piece of)', 'chromosome'), 3)], 'bio-3-3', 'isolation',
      at(7, 10, '(b)', '(iii)'), 3),
    T('10biv', 'Q10(b)(iv)', 'C', ask(8, 'Give two examples of the use of genetic engineering.'),
      [anyn(S('e.g. Bacteria (engineered to express genes to) produce human', 'produce Vitamin A'), 2, 3, open_list=True)],
      'bio-3-3', 'applications-of-genetic-engineering', at(7, 10, '(b)', '(iv)'), 6,
      decision='Two points ("(2 pts)") from the scheme\'s examples: one menu, claim two.'),
] + [
    T(f'10c-{slug}', 'Q10(c)', 'C', CROSS[k], rows, 'bio-1-4', concept, at(7, 10, '(c )', roman, why=CROSS_ROMANS), 3 * len(rows),
      stem=Q10C + CROSS[:k], fig='q10-cross', item=(slug, name),
      decision='The scheme prices each line of the cross on its own ("(1 pt)", "(3 pts)", "(2 pts)", "(2 pts)"): '
               'one card per line, every printed genotype, gamete or phenotype its own row. ' + extra)
    for k, slug, name, roman, rows, concept, extra in [
        (0, 'parents', 'Genotypes of parents', '(i)',
         [labelled('Genotype of pink parent : (RW)', 3)], 'parent-genotypes',
         'The white parent\'s "( WW )" is printed on the paper; the scheme prices the pink parent\'s.'),
        (1, 'gametes', 'Possible gametes', '(ii)',
         [pt(S('Gametes : (R) (W) x ( W)', piece=[2, 1, 1], psep=[' : ', ' x ', ' ']), 3, note_sel=CROSS_NOTE),
          pt(S('Gametes : (R) (W) x ( W)', piece=[2, 1, 2], psep=[' : ', ' x ', ' ']), 3, note_sel=CROSS_NOTE),
          pt(S('Gametes : (R) (W) x ( W)', piece=[2, 2], psep=[' : ', ' x ']), 3, note_sel=CROSS_NOTE)],
         'gametes-of-a-cross',
         'The scheme prints the gametes "(R) (W) x ( W)": cut at its own "x" and spaces, the two before the "x" '
         'the pink parent\'s and the one after it the white parent\'s.'),
        (2, 'offspring-genotypes', 'Genotypes of offspring', '(ii)',
         [pt(S('Offspring genotypes : (RW) (WW)', piece=[2, n], psep=[' : ', ' ']), 3, note_sel=CROSS_NOTE)
          for n in (1, 2)], 'offspring-genotypes', ''),
        (3, 'phenotypes', 'Matching phenotypes of offspring', '(iii)',
         [pt(S('Matching phenotypes : Pink White', piece=[2, n], psep=[' : ', ' ']), 3) for n in (1, 2)],
         'offspring-phenotypes', 'Each phenotype matches the genotype printed above it.')]
] + [
    T(f'11a{r}', f'Q11(a)({r})', 'C', [Q11A, ask(9, term, br=True)], [pt(S(ans), 7)], 'bio-3-1', concept,
      at(7, 11, '(a)', f'({r})'), 7)
    for r, term, ans, concept in [
        ('i', 'Biosphere.', 'Part of the earth (and atmosphere) that support life', 'biosphere'),
        ('ii', 'Omnivore.', '(An animal that) eats both plants and animals', 'omnivore'),
        ('iii', 'Niche.', 'The role of the organism (in the ecosystem)', 'niche')]
] + [
    T('11bi', 'Q11(b)(i)', 'C', Q(9, 'Name one animal from the ecosystem you have studied and state a suitable method of',
                                   'collecting that animal.'),
      [pt(S('Named animal and suitable apparatus (or method)', piece=1, psep=' and '), 3, kind='criterion', note=NO_ANSWER),
       pt(S('Named animal and suitable apparatus (or method)', piece=2, psep=' and '), 3, kind='criterion', note=NO_ANSWER,
          note_sel=S('[No animal named - no marks for a collection method ]', piece=[2, 1], psep=['[', ']']))],
      'bio-3-1', 'collecting-an-animal', at(7, 11, '(b)', '(i)'), 6, stem=[Q11B],
      decision=TWO_POINTS + ' The scheme prints "Named animal and suitable apparatus (or method)" ("(2 pts)"): cut '
                            'at its own "and", a criterion row each; its bracketed direction is the second row\'s note.'),
    T('11bii', 'Q11(b)(ii)', 'C', Q(9, 'Say 50 animals were collected on the first day. These animals were then marked.',
                                     'How did you mark the animals before you released them?'),
      [pt(S('e.g. paint or tag or snip hair or to avoid making animals', 'conspicuous'), 3)], 'bio-3-1',
      'marking-animals', at(7, 11, '(b)', '(ii)'), 3, stem=[Q11B]),
    T('11biii', 'Q11(b)(iii)', 'C', Q11BIII, [pt(S('≥ 20'), 3)], 'bio-3-1', 'second-capture', at(7, 11, '(b)', '(iii)'), 3,
      stem=[Q11B]),
    T('11biv', 'Q11(b)(iv)', 'C', Q(9, 'You noted that 20 of the animals you collected on the second day were already marked.',
                                     'animal population.'),
      [pt(S(OWL_FORMULA), 3, kind='criterion', note=NO_ANSWER), pt(S('B = 20'), 3),
       pt(S("Correct answer from candidate's figures"), 3, kind='criterion', note=NO_ANSWER)], 'bio-3-1',
      'capture-recapture-calculation', at(7, 11, '(b)', '(iv)'), 9, stem=[Q11B, M('(iii)', 9), Q11BIII],
      fig='q11-formula',
      decision='Three points ("(1 pt)" each), each printed on its own line: a row each. The first and last are the '
               'scheme\'s own words for what earns the point (A is the number given in (iii); the answer follows '
               'from the candidate\'s figures).'),
    T('11bv', 'Q11(b)(v)', 'C', Q(9, 'It is important to try to protect animal and plant populations in their natural environments.',
                                   'What term is used in ecology for the wise management of our natural environments?'),
      [pt(S('Conservation'), 3)], 'bio-3-1', 'conservation', at(7, 11, '(b)', '(v)'), 3),
    T('11bvi', 'Q11(b)(vi)', 'C', ask(9, 'Suggest one way in which our environment could be damaged or harmed.'),
      [pt(S('One suggestion'), 3, kind='criterion', note=NO_ANSWER)], 'bio-3-1', 'environmental-damage',
      at(7, 11, '(b)', '(vi)'), 3),
] + [
    T(f'11c{r}', f'Q11(c)({r})', 'C', ask(9, q), rows, 'bio-3-1', concept, at(7, 11, '(c )', f'({r})'), total,
      stem=Q11C, decision=decision)
    for r, q, rows, concept, total, decision in [
        ('i', 'What colours are the barn owl feathers?', [pt(S('Honey (coloured)/ white', piece=n), 3) for n in (1, 2)],
         'barn-owl-feathers', 6, TWO_POINTS + ' Cut at the scheme\'s own solidus.'),
        ('ii', 'What does the barn owl eat?', [pt(S('Mice or rats'), 3)], 'barn-owl-diet', 3, ''),
        ('iii', 'Name one site where the owl will nest.', [pt(S('Barns or old buildings'), 3)], 'barn-owl-nest-sites', 3,
         ''),
        ('iv', 'Give two reasons why barn owl numbers have decreased in recent years.',
         [anyn(S('Lack of nesting sites or poisoning from pesticides or a lack of', 'food'), 2, 3, sep=' or ')],
         'decline-of-the-barn-owl', 6,
         'Two points ("(2 pts)") from the three reasons the scheme prints joined by "or": one menu cut at its own '
         '"or", claim two.'),
        ('v', 'What is a pesticide?', [pt(S('Chemical (or substance) to kill insects (or to kill other plant pests)'), 3)],
         'pesticide', 3, ''),
        ('vi', 'Suggest how owls might be poisoned by pesticides?', [pt(S('Eating poisoned prey'), 3)],
         'pesticides-in-food-chains', 3, '')]
] + [
    T('12ai', 'Q12(a)(i)', 'C', ask(10, 'Explain the term digestion.'), [pt(S('Breakdown of food'), 7)], 'bio-2-6',
      'digestion', at(8, 12, '(a)', '(i)'), 7),
] + [
    T(f'12aii{n}', f'Q12(a)(ii){n}', 'C', [Q12AII, ask(10, f'{n}. {item}.', br=True)],
      [pt(S(line, piece=2, psep=' = '), 7, label=S(line, piece=1, psep=' = '))], 'bio-2-6', concept,
      at(8, 12, '(a)', '(ii)'), 7,
      decision=EACH_ITEM + ' Two of the three points of the "7 + 2(1)" ladder, one per numbered item. Each item alone '
                           '("1. Enzymes.") is too short a question to stand, so the card carries the printed lead-in '
                           'in its question text.')
    for n, item, line, concept in [(1, 'Enzymes', '1. Enzymes = chemical', 'enzymes-in-chemical-digestion'),
                                   (2, 'Teeth', '2. Teeth = mechanical', 'teeth-in-mechanical-digestion')]
] + [
    T(f'12bi-{x.lower()}', 'Q12(b)(i)', 'C', ask(10, 'Name the parts labelled A, B, C, D and E.'),
      [pt(cell(line[0], i, line[1]), 3)], 'bio-2-6', concept, at(8, 12, '(b)', '(i)'), 3, stem=[Q12B],
      fig='q12-digestive', item=(x.lower(), x), labels=digest_labels(x),
      decision=EACH_ITEM + ' "(5 pts)" over the five labels, cut at the scheme\'s own semicolons.')
    for x, line, i, concept in [('A', DIGEST1, 0, 'duodenum'), ('B', DIGEST1, 1, 'liver'), ('C', DIGEST2, 0, 'stomach'),
                                ('D', DIGEST2, 1, 'pancreas'), ('E', DIGEST2, 2, 'colon')]
] + [
    T('12bii', 'Q12(b)(ii)', 'C', ask(10, 'Part C releases an acid. Name that acid.'),
      [pt(S('Hydrochloric (acid) or HCl'), 3)], 'bio-2-6', 'stomach-acid', at(8, 12, '(b)', '(ii)'), 3, stem=[Q12B],
      fig='q12-digestive', labels=digest_labels()),
    T('12biii', 'Q12(b)(iii)', 'C', ask(10, 'Name and give one function of the liquid stored in the gall bladder.'),
      [pt(S('Bile'), 3), pt(S('Emulsifies fat'), 3)], 'bio-2-6', 'bile', at(8, 12, '(b)', '(iii)'), 6, stem=[Q12B],
      fig='q12-digestive', decision='The liquid and its function, a point each ("(2 pts)"), each on its own line: '
                                    'a row each.'),
    T('12biv', 'Q12(b)(iv)', 'C', Q(10, 'Amylase is an enzyme. Name one part of the digestive system where amylase is',
                                     'produced.'),
      [pt(S('Mouth or pancreas or salivary glands.'), 3)], 'bio-2-6', 'sources-of-amylase', at(8, 12, '(b)', '(iv)'), 3,
      stem=[Q12B], fig='q12-digestive'),
] + [
    T(f'12c{r}', f'Q12(c)({r})', 'C', ask(10, q), rows, 'bio-2-6', concept, at(8, 12, '(c )', f'({r})'), total,
      stem=[Q12C], decision=decision)
    for r, q, rows, concept, total, decision in [
        ('i', 'Give two symptoms of irritable bowel syndrome.',
         [anyn(S('Abdominal pain (or cramps)/ constipation/ diarrhoea'), 2, 3)], 'symptoms-of-ibs', 6,
         'Two points ("(2 pts)") from the printed list: one menu, claim two.'),
        ('ii', 'Constipation may result from reabsorbing too much of which liquid into the bloodstream?',
         [pt(S('Water'), 3)], 'constipation', 3, ''),
        ('iii', 'Give two treatments for irritable bowel syndrome.',
         [pt(S('Change diet (or example)/ medication (or example)', piece=n), 3) for n in (1, 2)], 'treating-ibs', 6,
         TWO_POINTS + ' Cut at the scheme\'s own solidus.'),
        ('iv', 'Peristalsis occurs in the digestive system. Explain the term peristalsis.',
         [pt(S('Muscular contraction/ to move food along', piece=n), 3) for n in (1, 2)], 'peristalsis', 6,
         TWO_POINTS + ' Cut at the scheme\'s own solidus.'),
        ('v', 'Give one beneficial effect of the bacteria found in the large intestine.',
         [pt(S('e.g. Produce vitamins or out-compete pathogens'), 3)], 'gut-bacteria', 3, '')]
] + [
    T('13ai', 'Q13(a)(i)', 'C', Q(11, 'Heart disease is a major problem in Ireland. State two ways to keep your heart healthy.'),
      [anyn(S('e.g. Exercise/ dietary (or example)/ specific medication or stop', 'smoking'), 2, 7, open_list=True)],
      'bio-2-6', 'healthy-heart', at(8, 13, '(a)', '(i)'), 14,
      decision='Two points ("(2 pts)") of the "7 + 2(1)" ladder from the scheme\'s examples: one menu, claim two, each '
               'response at the ladder\'s first rate.'),
    T('13aii', 'Q13(a)(ii)', 'C',
      ask(11, 'Why is the muscle of the left side of the heart thicker than the muscle of the right side?'),
      [pt(S('Left side pumps blood further'), 7)], 'bio-2-6', 'left-ventricle-wall', at(8, 13, '(a)', '(ii)'), 7),
] + [
    T(f'13bi-{x.lower()}', 'Q13(b)(i)', 'C', ask(11, 'Name the parts labelled A, B and C.'),
      [pt(cell(HEART[0], i, HEART[1]), 3)], 'bio-2-6', concept, at(8, 13, '(b)', '(i)'), 3, stem=[Q13B],
      fig='q13-heart', item=(x.lower(), x), labels=heart_labels(x), decision=EACH_ITEM + ' "(3 pts)" over the three labels.')
    for i, (x, concept) in enumerate([('A', 'aorta'), ('B', 'septum'), ('C', 'right-atrium')])
] + [
    T(f'13b{r}', f'Q13(b)({r})', 'C', ask(11, q), [row], 'bio-2-6', concept, sq, 3, stem=[Q13B], fig='q13-heart',
      labels=heart_labels() if letters else None)
    for r, q, row, concept, letters, sq in [
        ('ii', 'To which organs does blood vessel E carry blood?', pt(S('Lungs'), 3), 'pulmonary-artery', True,
         at(8, 13, '(b)', '(ii)')),
        ('iii', 'Is the blood in blood vessel A oxygenated or deoxygenated?', pt(S('Oxygenated'), 3), 'blood-in-the-aorta',
         True, at(8, 13, '(b)', '(iii)')),
        ('iv', 'Name the arteries that supply the muscle in the heart wall with blood.', pt(S('Coronary or cardiac'), 3),
         'coronary-arteries', False, at(8, 13, '(b)', '(iv)')),
        ('v', 'The pacemaker controls heartbeat. In which labelled part is the pacemaker located?',
         own_note('C or Right atrium', 3, note_line="[accept what candidate has called 'C' in part (i) ]"), 'pacemaker',
         True, at(8, 13, '(b)', '(v)')),
        ('vi', 'What is the average number of heartbeats per minute in a resting adult?',
         plain('72 (beats per minute) [accept 70 to 75]', 3), 'resting-heart-rate', False, at(8, 13, '(b)', '(vi)')),
        ('vii', 'What causes the sound of the heartbeat?', pt(S('Valves (closing)'), 3), 'heart-sounds', False,
         welded(8, 13, '(b)', '(vii)'))]
] + [
    T(f'13ci-{x.lower()}', 'Q13(c)(i)', 'C', ask(11, 'Name the parts labelled A, B, C and D.'),
      [pt(cell(line[0], i, line[1]), 3)], 'bio-2-6', concept, at(8, 13, '(c )', '(i)'), 3, stem=[Q13C],
      fig='q13-lungs', item=(x.lower(), x), labels=lung_labels(x), decision=EACH_ITEM + ' "(4 pts)" over the four labels.')
    for x, line, i, concept in [('A', LUNGS1, 0, 'larynx'), ('B', LUNGS1, 1, 'trachea'), ('C', LUNGS2, 0, 'bronchus'),
                                ('D', LUNGS2, 1, 'alveolus')]
] + [
    T(f'13c{r}', f'Q13(c)({r})', 'C', ask(11, q), [row], 'bio-2-6', concept, at(8, 13, '(c )', f'({r})'), 3, stem=[Q13C],
      fig='q13-lungs', labels=lung_labels() if letters else None)
    for r, q, row, concept, letters in [
        ('ii', 'In which labelled part does gas exchange take place?',
         plain("D or alveolus [accept what candidate has called 'D' in part (i) ]", 3), 'site-of-gas-exchange', True),
        ('iii', 'What is the function of part A?', pt(S('Make sound'), 3), 'larynx-function', True),
        ('iv', 'B and C have rings of cartilage. Suggest a function of these rings.', pt(S('Keep tube open'), 3),
         'cartilage-rings', True),
        ('v', 'Suggest a reason why smoking cigarettes is bad for your lungs.',
         anyn(S('(It can cause) e.g. cancer/ emphysema/ chronic cough/ COPD'), 1, 3, open_list=True),
         'smoking-and-the-lungs', False)]
] + [
    T(f'14ai-{x.lower()}', 'Q14(a)(i)', 'C', ask(12, 'Name the parts labelled A, B, C and D in the diagram.'),
      [pt(cell(line[0], i, line[1]), 3)], 'bio-1-3', concept, at(9, 14, '(a)', '(i)'), 3, stem=[Q14A], fig='q14-cell',
      item=(x.lower(), x), labels=cell_labels(x), decision=EACH_ITEM + ' "(4 pts)" over the four labels.')
    for x, line, i, concept in [('A', CELL1, 0, 'cell-membrane'), ('B', CELL1, 1, 'cell-wall'),
                                ('C', CELL2, 0, 'chloroplast'), ('D', CELL2, 1, 'vacuole')]
] + [
    T('14aii1', 'Q14(a)(ii)1', 'C', Q14AII1, [pt(S('1. Plant Cell', piece=2, psep='1. '), 3)], 'bio-1-3',
      'plant-or-animal-cell', at(9, 14, '(a)', '(ii)'), 3, stem=[Q14A], fig='q14-cell',
      decision=EACH_ITEM + ' Each numbered item a point ("(1 pt)"); the answer is cut after the scheme\'s own number.'),
    T('14aii2', 'Q14(a)(ii)2', 'C', [M('2.', 12), ask(12, 'Give a reason for your answer.')],
      [pt(S('2. Cell wall or vacuole or chloroplast(s)', piece=2, psep='2. '), 3)], 'bio-1-3', 'features-of-plant-cells',
      at(9, 14, '(a)', '(ii)'), 3, stem=[Q14A] + Q14AII1, fig='q14-cell', labels=cell_labels(),
      decision=EACH_ITEM + ' Each numbered item a point ("(1 pt)"); the answer is cut after the scheme\'s own number.'),
] + [
    T(f'14a{r}', f'Q14(a)({r})', 'C', Q(12, *q), [row], 'bio-1-3', concept, at(9, 14, '(a)', f'({r})'), 3, stem=[Q14A],
      fig='q14-cell', labels=cell_labels() if letters else None)
    for r, q, row, concept, letters in [
        ('iii', ('Name one substance usually found in part D.', 'Name one substance usually found in part D.'),
         pt(S('e.g. Water or sugar or salt or pigments'), 3), 'vacuole-contents', True),
        ('iv', ('Name the carbohydrate found in part B.', 'Name the carbohydrate found in part B.'), pt(S('Cellulose'), 3),
         'cellulose', True),
        ('v', ('Part A is said to be selectively permeable or semi-permeable. What does this mean?',
               'Part A is said to be selectively permeable or semi-permeable. What does this mean?'),
         pt(S('Allows some substances to pass through it'), 3), 'selective-permeability', True),
        ('vi', ('Ribosomes are also found in cells. What is their function?',
                'Ribosomes are also found in cells. What is their function?'), pt(S('To make protein'), 3), 'ribosomes',
         False)]
] + [
    T(f'14b{r}', f'Q14(b)({r})', 'C', q, rows, 'bio-2-1', concept, sq, 3 * len(rows), decision=decision)
    for r, q, rows, concept, sq, decision in [
        ('i', ask(12, 'What is an enzyme?'), [pt(S('Biological/ catalyst', piece=n), 3) for n in (1, 2)], 'enzyme',
         at(9, 14, '(b)', '(i)'), TWO_POINTS + ' Cut at the scheme\'s own solidus.'),
        ('ii', ask(12, 'Name one enzyme, other than amylase, and name its substrate.'),
         [pt(S('Named enzyme --------- Matching substrate', piece=1, psep=' -'), 3, kind='criterion', note=NO_ANSWER),
          pt(S('Named enzyme --------- Matching substrate', piece=2, psep='- '), 3, kind='criterion', note=NO_ANSWER,
             note_sel=S('[No enzyme named - no marks for a substrate ]', piece=[2, 1], psep=['[', ']']))],
         'enzyme-and-substrate', at(9, 14, '(b)', '(ii)'),
         TWO_POINTS + ' The scheme prints "Named enzyme --------- Matching substrate" ("(2 pts)"): cut at its own '
                      'dashes, a criterion row each; its bracketed direction is the second row\'s note.'),
        ('iii', ask(12, 'From which biomolecule are enzymes made?'), [pt(S('Protein'), 3)], 'enzymes-are-proteins',
         at(9, 14, '(b)', '(iii)'), ''),
        ('iv', Q(12, 'Enzymes are sometimes immobilised for use in industry. What is meant by the term',
                 'immobilised in relation to enzymes?'),
         [pt(S('(Enzyme) trapped/ in a gel (or in sodium alginate)', piece=n), 3) for n in (1, 2)],
         'immobilised-enzymes', at(9, 14, '(b)', '(iv)'), TWO_POINTS + ' Cut at the scheme\'s own solidus.'),
        ('v', ask(12, 'Name one substance used to immobilise enzymes.'), [pt(S('Sodium alginate'), 3)],
         'sodium-alginate', at(9, 14, '(b)', '(v)'), ''),
        ('vi', ask(12, 'Give one advantage of using immobilised enzymes.'),
         [pt(S('e.g. Reusable or pure product or cheaper or continuous', 'production'), 3)],
         'advantages-of-immobilised-enzymes', at(9, 14, '(b)', '(vi)'), ''),
        ('vii', ask(12, 'Suggest one reason why enzymes are sometimes used in washing powders.'),
         [pt(S('To breakdown biological stains (or example)'), 3)], 'enzymes-in-washing-powder',
         welded(9, 14, '(b)', '(vii)'), '')]
] + [
    T('14ci', 'Q14(c)(i)', 'C', ask(12, 'Draw a diagram of a plant. Label the root, stem and leaf on the diagram.'),
      [pt(S('Diagram + 3 labels', piece=1, psep=' + '), 3, kind='criterion',
          note_sel=S('[Diagram must show root, stem & leaf to get the 3 marks]', piece=[2, 1], psep=['[', ']'])),
       pt(S('Diagram + 3 labels', piece=2, psep=' + '), 3, kind='criterion', units=[1, 1, 1], note=NO_ANSWER)],
      'bio-2-6', 'drawing-a-plant', at(9, 14, '(c )', '(i)'), 6,
      decision='The scheme prices the drawing on its own row, "Diagram + 3 labels" at "3,0 + 3(1) (Non-sliding)": the '
               'diagram (3 or 0, its bracketed direction the row\'s note) and the three labels at 1 each, a criterion '
               'row each, cut at the scheme\'s own "+". The (c) heading "10(3)" counts this row as two of its ten '
               'points.'),
    T('14cii', 'Q14(c)(ii)', 'C', ask(12, 'Where in a plant does photosynthesis usually occur?'), [pt(S('Leaf'), 3)],
      'bio-2-6', 'leaf-is-the-site-of-photosynthesis', at(9, 14, '(c )', '(ii)'), 3),
    T('14ciii', 'Q14(c)(iii)', 'C', ask(12, 'Give two functions of the root.'),
      [anyn(S('Anchorage/ absorb water/ transport water (or food)/ store food/', 'asexual reproduction'), 2, 3)],
      'bio-2-6', 'functions-of-the-root', at(9, 14, '(c )', '(iii)'), 6,
      decision='Two points (the scheme prints "(2 pst)") from the printed list: one menu, claim two.'),
    T('14civ', 'Q14(c)(iv)', 'C', ask(12, 'Plants contain vascular tissue. Explain the term vascular.'),
      [pt(S('Transport (tissue)'), 3)], 'bio-2-6', 'vascular-tissue', at(9, 14, '(c )', '(iv)'), 3),
    T('14cv', 'Q14(c)(v)', 'C', ask(12, 'Name the two types of vascular tissue found in plants.'),
      [pt(S('Xylem/ phloem', piece=n), 3) for n in (1, 2)], 'bio-2-6', 'xylem-and-phloem', at(9, 14, '(c )', '(v)'), 6,
      decision=TWO_POINTS + ' Cut at the scheme\'s own solidus.'),
    T('14cvi', 'Q14(c)(vi)', 'C', Q(12, 'Explain the term meristem and give one location in a plant where meristematic tissue',
                                     'can be found.'),
      [pt(S('Area of active cell division or area of active mitosis'), 3),
       pt(S('Location : tip of shoot or tip of root [accep t cambium]', piece=[1, 2], psep=[' [', ' : ']), 3,
          label=S('Location : tip of shoot or tip of root [accep t cambium]', piece=1, psep=' : '),
          note_sel=S('Location : tip of shoot or tip of root [accep t cambium]', piece=[2, 1], psep=[' [', ']']))],
      'bio-2-6', 'meristems', at(9, 14, '(c )', '(vi)'), 6,
      decision='The meaning and the location, a point each, each on its own line: a row each. The scheme prints its '
               'direction "[accep t cambium]" with a gap in "accept" (rendered and looked at); it is lifted as printed.'),
    # ------------------------------------------------------------ Q15 --------
    T('15ai', 'Q15(a)(i)', 'C', Q(13, 'Plants need to disperse their seeds. The diagram above shows three different fruits.',
                                   'Indicate how each of the above fruits disperses its seeds.'),
      [pt(cell(FRUITS[0], 0, FRUITS[1], after=BEFORE_15AI), 3), pt(cell(FRUITS[0], 1, FRUITS[1], after=BEFORE_15AI), 3),
       pt(S('Peas = self or explosive', after=BEFORE_15AI), 3)], 'bio-2-5', 'seed-dispersal',
      at(10, 15, '(a)', '(3 pts)', '(i)', why=FOOT.format(cell='(3 pts)')), 9, fig='q15-fruits',
      decision='Three points ("(3 pts)"), one per fruit, the scheme printing each as "Fruit = method": a row each, cut '
               'at the cells\' own boundaries. The fruits are named only in the photographs\' own captions, so the '
               'three are one card on the one printed ask.'),
    T('15aii', 'Q15(a)(ii)', 'C', Q(13, 'After dispersal, some seeds undergo a period of dormancy.',
                                     'What is meant by the term dormancy?'),
      [pt(S('Period of no germination (or no growth) despite usual conditions', 'for germination being present'), 3)],
      'bio-2-5', 'dormancy', at(10, 15, '(a)', '(ii)'), 3),
    T('15aiii', 'Q15(a)(iii)', 'C', ask(13, 'Give one advantage of dormancy to plants.'),
      [pt(S('Better chance of survival or gives time for seeds to be dispersed', 'or allows time for seeds to mature'), 3)],
      'bio-2-5', 'advantages-of-dormancy', at(10, 15, '(a)', '(iii)'), 3),
    T('15aiv', 'Q15(a)(iv)', 'C', Q(13, 'Seedless fruits, e.g. grapes, are available in shops.',
                                     'Give one way to produce seedless fruits.'),
      [pt(S('Genetically or growth regulators or valid example'), 3)], 'bio-2-5', 'seedless-fruits',
      at(10, 15, '(a)', '(iv)'), 3),
    T('15av', 'Q15(a)(v)', 'C', Q(13, 'Artificial propagation of plants does not require seeds or fruits.',
                                   'Give two methods of artificial propagation used by gardeners.'),
      [anyn(S('e.g. Cutting/ grafting/ layering/ micropropagation'), 2, 3, open_list=True)], 'bio-2-5',
      'artificial-propagation', at(10, 15, '(a)', '(v)'), 6,
      decision='Two points ("(2 pts)") from the scheme\'s examples: one menu, claim two.'),
    T('15avi', 'Q15(a)(vi)', 'C', ask(13, 'Give one advantage and one disadvantage of artificial propagation.'),
      [labelled('Advantage : Fast or all plants identical', 3),
       labelled('Disadvantage : No variety or all susceptible to same diseases', 3)], 'bio-2-5',
      'artificial-propagation-pros-and-cons', at(10, 15, '(a)', '(vi)'), 6,
      decision='An advantage and a disadvantage, a point each, each printed under its own label: a row each.'),
] + [
    T(f'15bi-{x.lower()}', 'Q15(b)(i)', 'C', ask(13, 'Name the parts labelled A, B, C and D.'), [row], 'bio-2-4', concept,
      at(10, 15, '(b)', '(4 pts)', '(i)', why=FOOT.format(cell='(4 pts)')), 3, stem=[Q15B], fig='q15-skin',
      item=(x.lower(), x), labels=skin_labels(x), decision=EACH_ITEM + ' "(4 pts)" over the four labels.' + extra)
    for x, row, concept, extra in [
        ('A', pt(S(SKIN1[0], SKIN1[2], piece=1, psep=' B =', after=BEFORE_15BI), 3), 'hair', ''),
        ('B', pt(S(SKIN1[0], SKIN1[2], piece=[2, 1], psep=['Hair ', ' ['], after=BEFORE_15BI), 3,
                 note_sel=S(SKIN1[0], SKIN1[2], piece=[2, 2, 1], psep=['Hair ', ' [', ']'], after=BEFORE_15BI)),
         'blood-vessel-in-the-skin', ' B\'s cell runs onto a second printed line; its bracketed direction is the '
                                     'row\'s note.'),
        ('C', pt(cell(SKIN2[0], 0, SKIN2[1], after=BEFORE_15BI), 3), 'sweat-gland', ''),
        ('D', pt(cell(SKIN2[0], 1, SKIN2[1], after=BEFORE_15BI), 3), 'erector-muscle', '')]
] + [
    T(f'15b{r}', f'Q15(b)({r})', 'C', ask(13, q), [row], topic, concept, at(10, 15, '(b)', f'({r})'), total,
      stem=[Q15B], fig='q15-skin', labels=skin_labels() if letters else None, decision=decision)
    for r, q, row, topic, concept, total, letters, decision in [
        ('ii', 'Which labelled part plays a role in excretion?',
         own_note('C or sweat gland', 3, note_line="[accept what candidate has called 'C' in part (i) ]"), 'bio-2-6',
         'skin-in-excretion', 3, True, ''),
        ('iii', 'Name one other excretory organ in the body.', plain('Kidney or lung [accept liver]', 3), 'bio-2-6',
         'excretory-organs', 3, False, ''),
        ('iv', 'Give two other functions of the skin.',
         anyn(S('Protection against infection/ protection against dehydration/ sense', 'organ/ temperature control'), 2, 3),
         'bio-2-4', 'functions-of-the-skin', 6, False, 'Two points ("(2 pts)") from the printed list: one menu, claim two.'),
        ('v', 'What happens to the structure labelled A when the body is very cold?', pt(S('Stands up'), 3), 'bio-2-4',
         'hair-in-the-cold', 3, True, ''),
        ('vi', 'E is the sebaceous gland. Name a liquid produced by this gland.', pt(S('Sebum or oil'), 3), 'bio-2-4',
         'sebum', 3, False, '')]
] + [
    T('15ci', 'Q15(c)(i)', 'C', ask(13, 'Draw a diagram of Rhizopus. Label a rhizoid, a sporangium and a stolon on the diagram.'),
      [pt(S(*RHIZOPUS, piece=1, psep=' + '), 6, kind='criterion',
          note_sel=S(*RHIZOPUS, piece=[2, 1], psep=[' [', ']'])),
       pt(S(*RHIZOPUS, piece=[2, 1], psep=[' + ', ' [']), 6, kind='criterion', units=[2, 2, 2], note=NO_ANSWER)],
      'bio-3-2', 'drawing-rhizopus', at(10, 15, '(c)', '(i)'), 12,
      decision='The scheme prices the drawing on its own row, "Diagram + 3 labels" at "6,3,0 + 3(2) (non-sliding)": '
               'the diagram (6, 3 or 0, its bracketed list of what it must include the row\'s note) and the three '
               'labels at 2 each, a criterion row each, cut at the scheme\'s own "+". The (c) heading "10(3)" counts '
               'this row as four of its ten points.'),
    T('15cii', 'Q15(c)(ii)', 'C', Q15CII, [pt(S('Saprophytic'), 3)], 'bio-3-2', 'saprophytic-nutrition',
      at(10, 15, '(c)', '(ii)'), 3),
    T('15ciii', 'Q15(c)(iii)', 'C', ask(13, 'Explain the importance of this type of nutrition in nature.'),
      [pt(S('Breaks down dead matter or recycles nutrients'), 3)], 'bio-3-2', 'importance-of-saprophytes',
      at(10, 15, '(c)', '(iii)'), 3, stem=[M('(ii)', 13), Q15CII]),
    T('15civ', 'Q15(c)(iv)', 'C', ask(13, 'To which kingdom does Rhizopus belong?'), [pt(S('Fungi'), 3)], 'bio-3-2',
      'rhizopus-kingdom', at(10, 15, '(c)', '(iv)'), 3),
    T('15cv', 'Q15(c)(v)', 'C', Q(13, 'Name one economically harmful member and one economically beneficial member',
                                   'of the kingdom to which Rhizopus belongs.'),
      [labelled('Harmful : e.g. rusts or mildews or ringworm (fungus)', 3),
       labelled('Beneficial : e.g. yeast or penicillium or blue mould in cheese', 3)], 'bio-3-2',
      'economic-importance-of-fungi', at(10, 15, '(c)', '(v)'), 6,
      decision='A harmful and a beneficial member, a point each ("(2 pts)"), each printed under its own label: a row '
               'each.'),
    T('15cvi', 'Q15(c)(vi)', 'C', ask(13, 'In Rhizopus, which type of reproduction results in the formation of a zygospore?'),
      [pt(S('Sexual'), 3)], 'bio-3-2', 'zygospores', at(10, 15, '(c)', '(vi)'), 3),
]

# Section C (b) and (c) of Q10-Q13 are fixed points beside their question's
# "7 + 2(1)" ladder: their units count to it as fixed, their cards keep their
# own marks.
LADDER_EXEMPT = {t['key'] for t in TASKS if t['sec'] == 'C' and parse_ref(t['ref'])[0] in (10, 11, 12, 13)
                 and parse_ref(t['ref'])[1] in ('b', 'c')}

FIGURES = {
    # key suffix: (doc, page, rect in PDF points, credit, letters, alt, solution)
    'q3-flower': ('paper', 3, (200, 57, 400, 198), SEC, ['A', 'B', 'C'], 'Drawing of a vertical section through a flower: spreading outer parts with dotted edges form a cup opening upwards; inside it three stalks rise, the two outer ones each topped by a small oval head and the middle one longer, with a small knob at its tip and its base swollen into a large rounded body; the whole sits on a smaller rounded base with small leaf-like parts spreading at the bottom. A points to the large rounded body at the base of the middle stalk, B to the oval head on top of the right-hand stalk, C to the spreading outer part at the upper right.', False),
    'q4-table': ('paper', 3, (36, 452, 560, 768), SEC, [], 'Question 4 as printed: the instruction, then the list Homeostasis, Rabbit, Fluid balance (struck through), Lizard, Endotherm, Skin above a two-column table: Column A lists "A function of the kidney" (answered Fluid balance in Column B as the example) and parts (a) to (e); Column B is blank beside them.', False),
    'q5-foodweb': ('paper', 4, (105, 50, 432, 296), SEC, [], 'Diagram of names joined by arrows. At the bottom is Green Plants, with arrows from it up to Greenfly, Caterpillar, Snail, Mouse and Rabbit. Arrows also run from Greenfly to Ladybird; from Ladybird, Caterpillar and Snail to Blackbird; from Caterpillar and Snail to Hedgehog; from Blackbird and Mouse to Sparrow hawk; from Rabbit to Stoat; and from Hedgehog, Stoat and Rabbit to Fox.', False),
    'q8-tubes': ('paper', 6, (100, 214, 500, 378), SEC, ['A', 'B', 'C', 'D'], 'Four test tubes in a row, lettered A, B, C and D. Each has a shaded plug of cotton wool at the bottom (labelled Cotton wool) with a few seeds on it (labelled Seeds). Tubes A, B and C are otherwise empty. In tube D the seeds are covered by a liquid labelled Cool Boiled Water, under a layer labelled Oil at the top of the tube.', False),
    'q10-cross': ('paper', 8, (36, 479, 548, 596), SEC, [], 'The cross as printed for copying, under the headings Pink and White. Genotypes of parents: an empty bracket under Pink, a multiplication sign, then ( WW ) under White. Possible gametes: two empty brackets, a multiplication sign, one empty bracket. Genotypes of offspring: two empty brackets. Matching phenotypes of offspring: two blank lines.', False),
    'q11-formula': ('paper', 9, (120, 312, 440, 352), SEC, ['A', 'B'], 'The formula as printed: 50 × A over B, equals Number of animals in the population.', False),
    'q12-digestive': ('paper', 10, (120, 178, 425, 398), SEC, ['A', 'B', 'C', 'D', 'E'], 'Drawing of the human digestive system inside an outline of the trunk: a large dotted organ at the upper left with a small sac beneath it labelled Gall bladder; a bag-shaped organ at the upper right; a tube running down from under the bag; a ridged organ lying beneath the bag; coiled tubes filling the middle, framed by a wide wrinkled tube running up the left side, across the top and down the right side to a twisted end at the bottom. A points to the tube running down from under the bag, B to the large dotted organ, C to the bag-shaped organ, D to the ridged organ beneath it, E to the wide wrinkled tube on the right side.', False),
    'q13-heart': ('paper', 11, (180, 133, 420, 308), SEC, ['A', 'B', 'C', 'D', 'E'], 'Section through the human heart: four chambers with dotted walls, a thick dividing wall down the middle, and vessels rising from the top. The thick wall at the right of the drawing is labelled Left Side. A points to a vessel arching up at the top right, E to a vessel rising just left of the centre, C to the upper chamber at the left, D to the lower chamber at the left, B to the dividing wall in the middle.', False),
    'q13-lungs': ('paper', 11, (200, 465, 400, 680), SEC, ['A', 'B', 'C', 'D'], 'Drawing of part of the human breathing system: a tube ringed with bands runs down from a box-like structure at the top and branches at its base into a lung, drawn as an outline packed with clusters of small round sacs on branching tubes. A points to the box-like structure at the top, B to the ringed tube, C to the short tube branching off at its base, D to a cluster of small sacs inside the lung.', False),
    'q14-cell': ('paper', 12, (210, 90, 375, 246), SEC, ['A', 'B', 'C', 'D', 'E'], "Drawing of a rectangular cell with rounded corners: a grey outer layer with a thin line just inside it, several small oval bodies around the edge, a dark round body at the left and a large irregular clear space in the lower middle. A points to the cell's edge at its top left corner, B to its right-hand edge, C to a small oval body at the right, D to the large clear space, E to the dark round body.", False),
    'q15-fruits': ('paper', 13, (105, 64, 495, 176), SEC, [], 'Three photographs in a row, captioned Blackberries, Sycamore fruit and Peas: a cluster of dark, knobbly berries with leaves behind them; two fruits on long stalks, each a pair of thin papery wings joined at the seed; an open pod with a row of round peas inside.', False),
    'q15-skin': ('paper', 13, (188, 365.5, 440, 548), SEC, ['A', 'B', 'C', 'D', 'E'], 'Section through human skin: a dotted surface layer along the top; a hair rising out of the skin from a bulb deep in a lower layer of small round cells; a rounded gland beside the hair near the top; a thin band running at a slant beside the hair; a network of looped vessels under the surface; a long tube running down from the surface to a tightly coiled knot in the lower layer; and small round bodies in between. A points to the hair above the surface, B to the looped vessels under the surface, C to the coiled knot, D to the slanting band beside the hair, E to the rounded gland beside the hair.', False),
}
