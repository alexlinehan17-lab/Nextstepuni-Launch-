"""Biology 2016 Ordinary Level — reviewed task ledger, carded from the paper for the first time.

Independent visual sweep (2026-10-25), every page rendered and read:
  * The 2016 paper is one booklet (M43), 16 pages: p1 cover and instructions,
    p2-p4 Section A Questions 1-6, p5-p7 Section B Questions 7-9, p8-p13
    Section C Questions 10-15, p14-p16 "Blank Page". Sections A and B are
    answered on the paper; Section C in an answer book. No acknowledgements
    page: no figure carries a credit.
  * The marking scheme, 12 pages: p1 cover, p2 note, p3 introduction,
    cancelled and surplus answers, p4 conventions, p5-p10 Questions 1-15 (one
    table, no page numbers), p11 "Blank Page", p12 back cover.

The paper keeps the long-standing shape: any five of Section A's six
questions, any two of Section B's three, any four of Section C's six, and
Questions 14 and 15 are each any two of (a), (b), (c). Every printed ask is
carded. No Biology card existed for 2016 Ordinary before this review.

The scheme counts POINTS ("(1 pt)", "(3 pts)") and heads each question or
part with what they are worth. Ordered splits are carded at their first
rate: Q1 and Q5 "2(7)+3(2)" over five points, Q2, Q3, Q4 and Q6 "2(5)+5(2)"
over seven, every Section B (a) "5 + 1" over two and (b) "2(6)+6(2)" over
eight, and every Section C (a) of Q10-Q13 "7 + 2(1)" over three. Section C
(b) is "9(3)", (c) "8(3)", and every part of Q14 and Q15 "10(3)": a fixed 3
per point. A Section C (a) ladder sits beside its question's fixed (b) and
(c), so each such ladder names their units as fixed and their cards are
exempt from its notation. Every printed answer fits a per-response tariff,
so no part is carded whole.

The scheme mostly sets its compressed reprint of the ask on the answer's own
printed line ("Herbivore feeds on: Plants"); those tasks are anchored on the
part's own marker under its question (SQ path), as 2017 and 2018 Ordinary do.
Where the reprint stands on a line of its own above the answer (Q10(b)(v)),
or the part's marker is not printed alone on its line (Q4(e), Q6, Q9(a),
Q9(b)(viii), Q15(c)(vi)), the reprint is the pairing anchor and is
wording-checked; an answer sharing its reprint's line is read with `after=`
from the line printed before it. The text layer reads Q4(e)(ii)'s
treatments at the foot of scheme p5, after the "Section A" footer; they are
read after their own reprint "Treatment :".

Two printed choices are marked differently per option, each option with its
own printed list, so each is a route: Q4(e) arthritis or osteoporosis and
Q15(c)(vi) Parkinson's disease or paralysis, each for its cause and for its
treatment. The scheme prints both lists side by side, and the text layer
welds each printed row of the two columns into one line; each answer is cut
out of its line at the printed boundary and LAYOUT_CHECKS confirms, from
where it is printed, which column it stands in.

The census reader lost Question 4 (paper.py WELDED_HEADS, gated to this
sitting): Q3(g)'s row ends in its circle options "T F", so the "4." head was
never split off and Q4(e)(i)-(ii) filed as romans of Q3(g); the fix takes the
census from 138 leaves to the paper's 143.
"""
from bio_review_lib import Q, SQ, S, M, pt, anyn, T, L, parse_ref

YEAR, LEVEL = 2016, 'ol'
REVIEWED_AT = '2026-10-25'

SOURCES = {
    'paper': {'path': 'examiner-reports/biology/papers/2016-ol-paper.pdf',
              'fileid': 'LC025GLP000EV.pdf',
              'sha256': 'c084bd487b35d861bc45e84cd3a5e03130a3bd8a9ec48842d7d6ef0d4381478c',
              'pages': 16},
    'scheme': {'path': 'examiner-reports/biology/schemes/2016-ol.pdf',
               'fileid': 'LC025GLP000EV.pdf',
               'sha256': '236277809b8d5edfcb4c2a65485ce70a6d539b034dc63728173dcd84393e43a8',
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
    **{(n, x): t for n in range(10, 14) for x, t in (('b', 27), ('c', 24))},
    **{(n, x): 30 for n in (14, 15) for x in 'abc'},
}
LADDERS = {
    1: _ladder('2(7)+3(2)'), 5: _ladder('2(7)+3(2)'),
    **{q: _ladder('2(5)+5(2)') for q in (2, 3, 4, 6)},
    **{(n, 'a'): _ladder('5 + 1') for n in (7, 8, 9)},
    **{(n, 'b'): _ladder('2(6)+6(2)') for n in (7, 8, 9)},
    # Section C (a) "7 + 2(1)" (Q11 prints "7+2(1)"); (b) "9(3)" and (c)
    # "8(3)" are fixed points beside it, named here so the question's total is
    # the ladder's.
    **{(n, 'abc'): _ladder('7 + 2(1)', fixed={3: 17}) for n in (10, 12, 13)},
    (11, 'abc'): _ladder('7+2(1)', fixed={3: 17}),
}

CHECKSUMS = {
    1: {7: 5}, 5: {7: 5}, **{q: {5: 7} for q in (2, 3, 4, 6)},
    **{(n, 'a'): {5: 2} for n in (7, 8, 9)}, **{(n, 'b'): {6: 8} for n in (7, 8, 9)},
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
    ('paper', 2, 'the following', 'Q1 lead-in: every part asked, one card per letter.'),
    ('paper', 2, 'the following', 'Q2(a) "in the following list": every tissue type asked, one card per tissue.'),
    ('paper', 2, 'or', 'Q2(b) "1 or 2": the answer options.'),
    ('paper', 3, 'the following', 'Q3 lead-in: every statement asked, one card per letter.'),
    ('paper', 3, 'or', 'Q3 "true or false": the answer options.'),
    ('paper', 3, 'or', 'Q3 "T or F": the answer options.'),
    ('paper', 3, 'the following', 'Q4(e) lead-in "Answer the following": both romans asked.'),
    ('paper', 3, 'either', 'Q4(e) "either of the above disorders": the scheme prints a separate cause list and '
                           'treatment list for each, so each is a route card.'),
    ('paper', 4, 'the following', 'Q5 list of terms: the options; every description matched, one card per letter.'),
    ('paper', 4, 'the following', 'Q6 "Complete the following cross": every line of the cross asked, one card per '
                                  'line.'),
    ('paper', 5, 'any two', 'Section B rubric repeated.'),
    ('paper', 5, 'the following', 'Q7(b) lead-in: every part asked.'),
    ('paper', 6, 'the following', 'Q8(b) lead-in: every part asked.'),
    ('paper', 7, 'the following', 'Q9(b) "each of the following": every item asked, one card per roman.'),
    ('paper', 7, 'or', 'Q9(b)(vii) "Starch agar or milk agar": one item named either way; one answer.'),
    ('paper', 8, 'any four', 'Section C rubric repeated.'),
    ('paper', 8, 'the following', 'Q10(a) lead-in: every term asked, one card per roman.'),
    ('paper', 8, 'or', 'Q10(c) passage "giant deer or \'Irish Elk\'": passage text.'),
    ('paper', 8, 'or', 'Q10(c) passage "severe cold or over-hunting": passage text.'),
    ('paper', 8, 'either', 'Q10(c)(vi) "Name either one of the two": one response, either naturalist; one row.'),
    ('paper', 9, 'the following', 'Q11(a) lead-in: every term asked, one card per roman.'),
    ('paper', 9, 'or', 'Q11(c)(ii) "agriculture, industry or the home": description; marked on the same rows.'),
    ('paper', 9, 'or', 'Q11(c)(iv) "agriculture, fisheries or forestry": description; marked on the same row.'),
    ('paper', 10, 'the following', 'Q12(a) lead-in: every part asked, one card per roman.'),
    ('paper', 10, 'any two', 'Q12(b)(ii) "Name any two bacterial shapes": one menu, claim two.'),
    ('paper', 10, 'the following', 'Q12(c) lead-in: every part asked.'),
    ('paper', 11, 'the following', 'Q13(a)(ii) "each of the following processes": both processes asked, one card '
                                   'each.'),
    ('paper', 11, 'or', 'Q13(a)(ii) "anabolism or catabolism": the answer options.'),
    ('paper', 11, 'or', 'Q13(b)(v) "aerobic respiration or anaerobic respiration": the answer options.'),
    ('paper', 12, 'any two', 'Q14 "any two of (a), (b), (c)": whole-part choice; every part is carded.'),
    ('paper', 12, 'the following', 'Q14(a) lead-in: every part asked.'),
    ('paper', 12, 'any two', 'Q14(a)(iii) "Name any two of these groups": one menu, claim two.'),
    ('paper', 12, 'or', 'Q14(a)(iv) "positive (+) or negative (−)": description.'),
    ('paper', 12, 'or', 'Q14(a)(iv) "contains or does not contain": description.'),
    ('paper', 12, 'the following', 'Q14(b)(v) "each of the following": both processes asked, one card each.'),
    ('paper', 13, 'any two', 'Q15 "any two of (a), (b), (c)": whole-part choice; every part is carded.'),
    ('paper', 13, 'or', 'Q15(a)(ii) "a stem, a root, a bud or a leaf": the answer options for each example.'),
    ('paper', 13, 'the following', 'Q15(a)(iii) "from the following list": every function asked, one card each.'),
    ('paper', 13, 'any two', 'Q15(c)(v) "Name any two types of neuron": one menu, claim two.'),
    ('paper', 13, 'choose', 'Q15(c)(vi) "Clearly choose either of these disorders": the scheme prints a separate '
                            'cause and treatment for each, so each is a route card.'),
    ('paper', 13, 'either', 'Q15(c)(vi) "either of these disorders": the same choice; route cards.'),
]

ROUTES = {
    'Q4(e)(i)': ['arthritis', 'osteoporosis'],
    'Q4(e)(ii)': ['arthritis', 'osteoporosis'],
    'Q15(c)(vi)1': ['parkinsons', 'paralysis'],
    'Q15(c)(vi)2': ['parkinsons', 'paralysis'],
}

# Which column each answer of a side-by-side route list is printed in, read
# from the page: its left edge sits nearest the left edge of its own heading.
# Scheme p5 prints "genetics" once in each column, so each is read inside a
# clip that holds both headings and that one word. Where a word's box takes in
# the solidus printed after it, the item is read with that solidus.
LAYOUT_CHECKS = [
    ('scheme', 5, 'Loss of cartilage', ['Arthritis', 'Osteoporosis'], 'Arthritis'),
    ('scheme', 5, 'genetics', ['Arthritis', 'Osteoporosis'], 'Arthritis', (140, 430, 400, 483)),
    ('scheme', 5, 'wear & tear', ['Arthritis', 'Osteoporosis'], 'Arthritis'),
    ('scheme', 5, 'Loss of collagen', ['Arthritis', 'Osteoporosis'], 'Osteoporosis'),
    ('scheme', 5, 'genetics', ['Arthritis', 'Osteoporosis'], 'Osteoporosis', (175, 430, 440, 471)),
    ('scheme', 5, 'hormone imbalance', ['Arthritis', 'Osteoporosis'], 'Osteoporosis'),
    ('scheme', 5, 'eating disorder', ['Arthritis', 'Osteoporosis'], 'Osteoporosis'),
    ('scheme', 5, 'menopause', ['Arthritis', 'Osteoporosis'], 'Osteoporosis'),
    ('scheme', 5, 'No cure', ['Arthritis', 'Osteoporosis'], 'Arthritis'),
    ('scheme', 5, 'weight loss', ['Arthritis', 'Osteoporosis'], 'Arthritis'),
    ('scheme', 5, 'physiotherapy/', ['Arthritis', 'Osteoporosis'], 'Arthritis'),
    ('scheme', 5, 'joint replacement', ['Arthritis', 'Osteoporosis'], 'Arthritis'),
    ('scheme', 5, 'anti-inflamatory medication', ['Arthritis', 'Osteoporosis'], 'Arthritis'),
    ('scheme', 5, 'Special protein diet', ['Arthritis', 'Osteoporosis'], 'Osteoporosis'),
    ('scheme', 10, 'Failure to produce dopamine', ["Parkinson's", 'Paralysis'], "Parkinson's"),
    ('scheme', 10, 'Failure of nervous system/', ["Parkinson's", 'Paralysis'], 'Paralysis'),
    ('scheme', 10, 'stroke', ["Parkinson's", 'Paralysis'], 'Paralysis'),
    ('scheme', 10, 'Physiotherapy/', ["Parkinson's", 'Paralysis'], "Parkinson's"),
    ('scheme', 10, 'exercise', ["Parkinson's", 'Paralysis'], "Parkinson's"),
    ('scheme', 10, 'electrical stimulation (DBS)', ["Parkinson's", 'Paralysis'], "Parkinson's"),
    ('scheme', 10, 'drugs', ["Parkinson's", 'Paralysis'], "Parkinson's"),
    ('scheme', 10, 'Constant care', ["Parkinson's", 'Paralysis'], 'Paralysis'),
    ('scheme', 10, 'special aids', ["Parkinson's", 'Paralysis'], 'Paralysis'),
    ('scheme', 10, 'stem cell therapy/', ["Parkinson's", 'Paralysis'], 'Paralysis'),
    ('scheme', 10, 'physiotherapy', ["Parkinson's", 'Paralysis'], 'Paralysis'),
]

SEC = 'State Examinations Commission'
SAME_LINE = 'The scheme sets its reprint of the ask on the answer\'s own line: anchored on the part\'s marker.'
EACH_ITEM = 'A list the scheme prices entry by entry: one card per entry, each its own slice of the printed line.'
NO_ANSWER = 'The scheme prints no answer here, only what earns the marks.'
TWO_POINTS = 'The scheme prices this part at two points: each printed point its own row.'
ROUTE = ('A closed choose-one pool of two printed disorders, each with its own list in the scheme\'s side-by-side '
         'columns: one card per disorder, its answers cut out of the welded column rows at their printed '
         'boundaries (LAYOUT_CHECKS reads which column each stands in).')


def at(page, q, *path_and_marker, why=SAME_LINE):
    """The part's own marker under its question (and letter) on the scheme page."""
    *path, marker = path_and_marker
    return SQ(page, marker, path=[str(q), *path], paired=why, bare=True)


def rq(page, label, paired=None, path=None):
    """The scheme's reprint of the ask on a line of its own (or heading its answer's line)."""
    return SQ(page, label, label, paired=paired, path=path)


def ask(page, sentence, **kw):
    """A one-line ask closed by its own punctuation, before its answer line."""
    return Q(page, sentence, sentence, **kw)


def cell(line, i, cuts, page=None):
    """Cell i of a scheme line printed as cells ("A = Kidney B = Ureter"), cut at the cells' own
    printed boundaries: cuts[k] = (text opening cell k+1, text closing cell k)."""
    pieces, seps = [], []
    if i > 0:
        pieces.append(2)
        seps.append(cuts[i - 1][1])
    if i < len(cuts):
        pieces.append(1)
        seps.append(cuts[i][0])
    return S(line, page=page, piece=pieces, psep=seps)


def side(line, i, cuts, which, page=None):
    """One side of cell i's " = " (1: before it, 2: after it), for a figure's label key."""
    sel = cell(line, i, cuts, page=page)
    return {**sel, 'piece': sel['piece'] + [which], 'psep': sel['psep'] + [' = ']}


def labels(line, letters, cuts, page, asked=None, meaning_side=2):
    return [L(x, side(line, i, cuts, meaning_side, page=page), x == asked) for i, x in enumerate(letters)]


# ------------------------------------------------------------ question text --
Q1 = Q(2, 'Use your knowledge of ecology to answer the following questions.')
Q2 = Q(2, 'The diagram shows the internal structure of two plant parts.')
Q2A = [Q(2, 'The letters A, B, C in the diagram represent three different tissue types.'),
       Q(2, 'Match each letter with its correct tissue type in the following list:')]
Q3 = Q(3, 'Indicate whether the following statements are true or false by drawing a circle around T or F in',
       'each case.')
Q4 = Q(3, 'The diagram shows a section of the human skeleton.')
Q4E = [Q(3, 'Arthritis and osteoporosis are two disorders of the musculoskeletal system.'),
       Q(3, 'Answer the following in relation to either of the above disorders.'),
       ask(3, 'Name of disorder:', br=True)]
Q5 = Q(4, 'Place each term from the following list into Column B to match a description in Column A.',
       'The first one has been completed for you.')
Q6 = [Q(4, 'In humans, the allele for brown hair (B) is dominant to the allele for red hair (b).'),
      Q(4, 'Complete the following cross between a brown haired man and a red haired woman.'),
      Q(4, 'Genotypes of parents (Bb) × (bb)', br=True)]
Q7B = Q(5, 'Answer the following questions in relation to obtaining and staining a sample of plant',
        'cells and viewing them under the microscope.')
Q8B = Q(6, 'Answer the following in relation to your investigation into the effect of pH on the rate of',
        'enzyme activity.')
Q9B = Q(7, 'For what purpose did you use each of the following in the course of your practical', 'activities?')
Q10A = Q(8, 'Explain the following terms used in genetics.')
Q10BIII = Q(8, 'During DNA profiling cells are broken down to release the DNA, which is then cut into',
            'fragments. The fragments are then separated.')
Q10C = Q(8, 'The giant deer or ‘Irish Elk’ was a mammal that became extinct in Ireland about 9,000 years',
         'over-hunting have been put forward as to why the animal became extinct.')
Q11A = Q(9, 'Explain the following terms used in ecology.')
Q11B = Q(9, 'There are many bee species in Ireland.',
         'Conservation programmes will have to be introduced if we are to halt this decline.')
Q11C = Q(9, 'Humans can have many effects on an ecosystem, e.g. pollution.')
Q11CII = ask(9, 'Give one effect of a named pollutant in agriculture, industry or the home.')
Q12A = Q(10, 'Give one role for each of the following in defence against disease.')
Q12BIV1 = Q(10, '1. What structure do some bacterial cells form to survive harsh environmental', 'conditions?')
Q12C = Q(10, 'Answer the following questions in relation to the human endocrine system.')
Q12CII = ask(10, 'Give the location of a named endocrine gland in the body.')
Q12CIV = ask(10, 'Name a hormone produced by the gland referred to in part (ii).')
Q12CVI = ask(10, 'Give a deficiency symptom of this hormone.')
Q13AII = [Q(11, 'There are two types of metabolism – anabolism and catabolism.'),
          ask(11, 'State whether each of the following processes is an example of anabolism or catabolism.')]
Q13BII = Q(11, 'Aerobic respiration occurs in two stages. Where in the cell does')
Q13CII = Q(11, 'The apparatus shown below may be used to investigate the effect of environmental',
           'factors on the rate of photosynthesis.')
Q13CII1 = Q(11, '1. Name one environmental factor that has an effect on the rate of photosynthesis that',
            'could be investigated using the apparatus shown.')
Q14A = Q(12, 'Answer the following in relation to blood.')
Q14BII = Q(12, 'The diagram shows the human urinary system. Name the parts labelled A and B.')
Q14B = Q(12, 'The diagram shows the human urinary system. Name the parts labelled A and B.', piece=1,
         psep=' Name the')
Q14BV = Q(12, 'Name the region of part A in which each of the following takes place:')
Q15AIII = Q(13, 'Seeds are produced in flowering plant sexual reproduction.', 'following list:')
Q15B = Q(13, 'The diagram shows a virus.')
Q15C = Q(13, 'Alzheimer’s disease is a brain disorder that slowly destroys memory and thinking skills.',
         'pursuits may help to delay the onset of this disease.')
Q15CVI = Q(13, 'Parkinson’s disease and paralysis are other disorders associated with the nervous system.', 'give:')

# ------------------------------------------------------- scheme cell lines --
TISSUES = ('Vascular = B Dermal = C Ground = A', [(' Dermal =', '= B '), (' Ground =', '= C ')])
GAMETES = '(B) (b) x (b)'
SKELETON = "Backbone or vertebral column [Accept 'spine']"
FUNCTIONS = ('Protection/ movement/ support/ blood cell production/', 'shape or structure')
CAUSE = ('Loss of cartilage/ Loss of collagen/ genetics/', 'genetics/ hormone imbalance/',
         'wear & tear eating disorder/ menopause')
TREAT = ('No cure/ rest/ exercise/ Special protein diet/', 'weight loss/ physiotherapy/ exercise',
         'joint replacement/', 'anti-inflamatory medication')
MICROSCOPE = ('A = Eyepiece B = Stage or platform', [(' B =', 'Eyepiece ')])
ENZYME = "Named enzyme [not 'celery' or 'liver']"
CARNIVORE = ("(Organism that) eats animals [Accept 'eats only/mainly", "animals']")
BACTERIAL_CELL = 'Bacterial cell: Diagram: Marks (3,0)'
SHAPES = "Coccus [Accept 'round']/ rod/ spiral"
EQUATION = 'Glucose + Oxygen → Water + Carbon dioxide + Energy (or ATP) (1 pt)'
URINARY = ('A = Kidney B = Ureter', [(' B =', 'Kidney ')])
EXCRETED = 'Water/ salt/ urea [urine = 1pt ]'
EXAMPLES = 'e.g. Strawberry runner is a stem/ daffodil bulb is a bud'
VIRUS = ('A = Protein coat; B = Nucleic acid or DNA or RNA', [('; B =', 'coat; ')])
PCAUSE = 'Failure to produce dopamine Failure of nervous system/ stroke'
PTREAT = ('Physiotherapy/ exercise/ Constant care/ special aids', 'electrical stimulation (DBS) / stem cell therapy/',
          'drugs physiotherapy')


def bracket(line, end=None):
    """A scheme answer and its square-bracketed direction, cut at the bracket: (answer, note)."""
    sel = (line, end) if end else (line,)
    return (S(*sel, piece=1, psep=' ['), S(*sel, piece=[2, 1], psep=[' [', ']']))


def plain(line, marks, end=None, **kw):
    """One answer whose square-bracketed direction ("[not 'grass']") is the row's note."""
    ans, note = bracket(line, end)
    return pt(ans, marks, note_sel=note, **kw)


TASKS = [
    # ------------------------------------------------------------ Section A --
] + [
    T(f'1{x}', f'Q1({x})', 'A', Q(2, q, piece=1, psep='..'), [row], 'bio-3-1', concept, at(5, 1, f'({x})'), 7,
      stem=[Q1])
    for x, q, row, concept in [
        ('a', 'A herbivore is an animal that feeds on', plain("Plants [not 'grass']", 7), 'herbivore'),
        ('b', 'The functional role of an organism in an ecosystem is called its', pt(S('Niche'), 7), 'niche'),
        ('c', 'A decomposer is an organism that feeds on', pt(S('Dead or decaying material'), 7), 'decomposer'),
        ('d', 'In an ecosystem, the term edaphic factor refers to the', plain("Soil [not 'humus']", 7),
         'edaphic-factor'),
        ('e', 'The term fauna refers to', pt(S('Animals'), 7), 'fauna')]
] + [
    T(f'2a-{slug}', 'Q2(a)', 'A', Q2A + [Q(2, f'{name} tissue', piece=1, psep=' …', br=True)],
      [pt(cell(TISSUES[0], i, TISSUES[1]), 5)], 'bio-2-6', f'{slug}-tissue', at(5, 2, '(a)'), 5,
      stem=[Q2], fig='q2-tissues', item=(slug, f'{name} tissue'),
      labels=[L(letter, side(TISSUES[0], j, TISSUES[1], 1, page=5), letter == mine)
              for j, letter in ((2, 'A'), (0, 'B'), (1, 'C'))],
      decision=EACH_ITEM + ' The scheme prints "Vascular = B Dermal = C Ground = A" ("(3 pts)"): one card per '
                           'tissue type, as the paper lists them.')
    for i, (slug, name, mine) in enumerate([('vascular', 'Vascular', 'B'), ('dermal', 'Dermal', 'C'),
                                            ('ground', 'Ground', 'A')])
] + [
    T('2b', 'Q2(b)', 'A', ask(2, 'Which of the two parts, 1 or 2, represents a young root?'),
      [pt(S('Young root = Diagram 2', piece=2, psep=' = '), 5)], 'bio-2-6', 'identifying-a-root', at(5, 2, '(b)'), 5,
      stem=[Q2], fig='q2-tissues'),
    T('2c', 'Q2(c)', 'A', ask(2, 'Give one feature of the part you have chosen that indicates it is a root.'),
      [pt(S('Root hairs or central xylem'), 5)], 'bio-2-6', 'features-of-a-root', at(5, 2, '(c)'), 5,
      stem=[Q2], fig='q2-tissues'),
    T('2d', 'Q2(d)', 'A', ask(2, 'Give one function of dermal tissue in plants.'),
      [pt(S('Protection or absorption'), 5)], 'bio-2-6', 'functions-of-dermal-tissue', at(5, 2, '(d)'), 5),
    T('2e', 'Q2(e)', 'A', ask(2, 'Give one function of ground tissue in plants.'),
      [pt(S('Photosynthesis or storage or support'), 5)], 'bio-2-6', 'functions-of-ground-tissue', at(5, 2, '(e)'), 5),
] + [
    T(f'3{x}', f'Q3({x})', 'A', Q(3, *q), [pt(S(ans), 5)], 'bio-2-6', concept, at(5, 3, f'({x})'), 5, stem=[Q3])
    for x, q, ans, concept in [
        ('a', ('Diffusion is the movement of molecules from where they are more',
               'concentrated to where they are less concentrated.'), 'TRUE', 'diffusion'),
        ('b', ('Semi-permeable means all substances can pass through.',
               'Semi-permeable means all substances can pass through.'), 'FALSE', 'semi-permeable'),
        ('c', ('Turgor pressure helps to give shape to plant cells.',
               'Turgor pressure helps to give shape to plant cells.'), 'TRUE', 'turgor'),
        ('d', ('Osmosis is the basis for some methods of food preservation.',
               'Osmosis is the basis for some methods of food preservation.'), 'TRUE', 'osmosis-and-food-preservation'),
        ('e', ('Energy is required for diffusion to happen.', 'Energy is required for diffusion to happen.'), 'FALSE',
         'diffusion-is-passive'),
        ('f', ('Osmosis concerns the movement of water.', 'Osmosis concerns the movement of water.'), 'TRUE',
         'osmosis-moves-water'),
        ('g', ('Oxygen passes from our lungs to our blood by osmosis.',
               'Oxygen passes from our lungs to our blood by osmosis.'), 'FALSE', 'oxygen-moves-by-diffusion')]
] + [
    T('4a', 'Q4(a)', 'A', Q(3, 'What common name is given to this section of the human', 'skeleton?'),
      [plain(SKELETON, 5)], 'bio-2-4', 'vertebral-column', at(5, 4, '(a)'), 5, stem=[Q4], fig='q4-skeleton'),
    T('4b', 'Q4(b)', 'A', Q(3, 'This section is made up of many small bones. What name is', 'given to these bones?'),
      [pt(S('Vertebrae'), 5)], 'bio-2-4', 'vertebrae', at(5, 4, '(b)'), 5, stem=[Q4], fig='q4-skeleton'),
    T('4c', 'Q4(c)', 'A', Q(3, 'Discs are found between these small bones. What are these', 'discs made from?'),
      [pt(S('Cartilage'), 5)], 'bio-2-4', 'intervertebral-discs', at(5, 4, '(c)'), 5, stem=[Q4], fig='q4-skeleton'),
    T('4d', 'Q4(d)', 'A', ask(3, 'Give two functions of the human skeleton.'), [anyn(S(*FUNCTIONS), 2, 5)],
      'bio-2-4', 'functions-of-the-skeleton', at(5, 4, '(d)'), 10,
      decision='Two points ("(2 pts)") from the printed list: one menu, claim two, each response at the ladder\'s '
               'first rate.'),
] + [
    T(f'4e{r}-{route}', f'Q4(e)({r})', 'A', ask(3, q), [anyn(None, 1, 5, options=opts)], 'bio-2-4',
      f'{what}-{route}', rq(5, sq, path=['4', '(e)']), 5, route=route, stem=Q4E,
      decision=ROUTE + ' One point ("(1 pt)"), any one of the disorder\'s printed answers: a menu, claim one.')
    for r, q, what, sq, route, opts in [
        ('i', 'One possible cause.', 'cause-of', 'Cause:', 'arthritis',
         [S(CAUSE[0], piece=1), S(CAUSE[1], piece=1), S(CAUSE[2], piece=1, psep=' eating')]),
        ('i', 'One possible cause.', 'cause-of', 'Cause:', 'osteoporosis',
         [S(CAUSE[0], piece=2), S(CAUSE[0], piece=3), S(CAUSE[1], piece=2),
          S(CAUSE[2], piece=[2, 1], psep=['tear ', '/']), S(CAUSE[2], piece=[2, 2], psep=['tear ', '/'])]),
        ('ii', 'One treatment for the disorder.', 'treating', 'Treatment :', 'arthritis',
         [S(TREAT[0], piece=1), S(TREAT[0], piece=2), S(TREAT[0], piece=3), S(TREAT[1], piece=1),
          S(TREAT[1], piece=2), S(TREAT[2], piece=1), S(TREAT[3])]),
        ('ii', 'One treatment for the disorder.', 'treating', 'Treatment :', 'osteoporosis',
         [S(TREAT[0], piece=4), S(TREAT[1], piece=3)])]
] + [
    T(f'5{x}', f'Q5({x})', 'A', Q(4, *q), [pt(S(ans), 7)], 'bio-u2', concept, at(5, 5, f'({x})'), 7,
      stem=[Q5], qfig='q5-terms',
      decision='The list of terms (its first struck through as the worked example) and the table are shown as '
               'the question\'s own print.')
    for x, q, ans, concept in [
        ('a', ('Repeating an experiment',), 'Replicate', 'replicate'),
        ('b', ('Information gathered during experiments',), 'Data', 'data'),
        ('c', ('Used for comparison in experiments',), 'Control', 'control'),
        ('d', ('Where only the investigator knows what', 'treatment the participant is receiving'), 'Blind test',
         'blind-test'),
        ('e', ('An idea supported by different experiments',), 'Theory', 'theory')]
] + [
    T(f'6-{slug}', 'Q6', 'A', Q(4, *q, **({'piece': 1, 'psep': ' …'} if slug == 'phenotypes' else {})), rows, 'bio-1-4', concept, rq(5, sq), len(rows) * 5, stem=Q6,
      item=(slug, name), decision=decision)
    for slug, name, q, rows, concept, sq, decision in [
        ('gametes', 'Possible gametes', ('Possible gametes ( ) ( ) × ( )',),
         [pt(S(GAMETES, piece=[1, 1], psep=[' x ', ' '], after='Idea supported by experiments: Theory'), 5,
             note='Before the scheme\'s "x": a gamete of the (Bb) parent.'),
          pt(S(GAMETES, piece=[1, 2], psep=[' x ', ' '], after='Idea supported by experiments: Theory'), 5,
             note='Before the scheme\'s "x": a gamete of the (Bb) parent.'),
          pt(S(GAMETES, piece=2, psep=' x ', after='Idea supported by experiments: Theory'), 5,
             note='After the scheme\'s "x": the gamete of the (bb) parent.')],
         'gametes-of-a-cross', 'Gametes:',
         'The scheme prices each line of the cross on its own ("(3 pts)", "(2 pts)", "(2 pts)"): one card per line. '
         'It prints the gametes "(B) (b) x (b)": three points, a row each, cut at its own "x" and spaces.'),
        ('offspring-genotypes', 'Genotypes of offspring', ('Genotypes of offspring ( ) ( )',),
         [pt(S('(Bb) (bb)', piece=n, psep=' ', after='Gametes: (B) (b) x (b)'), 5) for n in (1, 2)],
         'offspring-genotypes', 'Genotypes of offspring:',
         'The scheme prices each line of the cross on its own: "(Bb) (bb)" is two points, a row each.'),
        ('phenotypes', 'Matching phenotypes of offspring',
         ('Matching phenotypes of offspring',),
         [pt(S('Brown Red', piece=n, psep=' ', after='Genotypes of offspring: (Bb) (bb)'), 5) for n in (1, 2)],
         'offspring-phenotypes', 'Matching phenotypes:',
         'The scheme prices each line of the cross on its own: "Brown Red" is two points, a row each, matching '
         'the genotypes printed above them.')]
] + [
    # ------------------------------------------------------------ Section B --
    T(f'7a-{x.lower()}', 'Q7(a)', 'B', ask(5, 'Name the parts of the light microscope labelled A and B.'),
      [pt(cell(MICROSCOPE[0], i, MICROSCOPE[1]), 5)], 'bio-1-3', concept, at(6, 7, '(a)'), 5, fig='q7-microscope',
      item=(x.lower(), x), labels=labels(MICROSCOPE[0], 'AB', MICROSCOPE[1], 6, asked=x),
      decision=EACH_ITEM + ' "5 + 1" over the two labels, carded at its first rate.')
    for i, (x, concept) in enumerate([('A', 'eyepiece'), ('B', 'stage')])
] + [
    T(f'7b{r}', f'Q7(b)({r})', 'B', Q(5, *q), [row], 'bio-1-3', concept, at(6, 7, '(b)', f'({r})'), total,
      stem=[Q7B], decision=decision)
    for r, q, row, concept, total, decision in [
        ('i', ('From what plant did you obtain the cells?', 'From what plant did you obtain the cells?'),
         pt(S('e. g. Onion'), 6), 'plant-for-a-cell-sample', 6, ''),
        ('ii', ('How did you prepare the slide of the plant cell sample for examination?',
                'How did you prepare the slide of the plant cell sample for examination?'),
         anyn(S('Thin piece of tissue/ in water/ on slide/ add stain/', 'add coverslip'), 3, 6), 'preparing-a-slide',
         18, 'Three points ("(3 pts)") from the printed steps: one menu, claim three, each response at the ladder\'s '
             'first rate.'),
        ('iii', ('What stain did you use on the cells?', 'What stain did you use on the cells?'),
         pt(S('e.g. Iodine'), 6), 'stain-for-plant-cells', 6, ''),
        ('iv', ('How did you apply the stain?', 'How did you apply the stain?'), pt(S('e.g. Dropper'), 6),
         'applying-a-stain', 6, ''),
        ('v', ('There are usually 3 objective lenses on a microscope – low, medium and high power.',
               'Which objective lens should you begin with when using the microscope?'), pt(S('Low (power)'), 6),
         'low-power-first', 6, ''),
        ('vi', ('Give one cell structure that you observed that indicated that the cells were plant cells.',
                'Give one cell structure that you observed that indicated that the cells were plant cells.'),
         pt(S('Cell wall or vacuole'), 6), 'plant-cell-structures', 6, '')]
] + [
    T('8ai', 'Q8(a)(i)', 'B', ask(6, 'To which group of biomolecules do enzymes belong?'), [pt(S('Protein'), 5)],
      'bio-2-1', 'enzymes-are-proteins', at(6, 8, '(a)', '(i)'), 5),
    T('8aii', 'Q8(a)(ii)', 'B', ask(6, 'Give one biological explanation why washing powder may contain enzymes.'),
      [pt(S('Breakdown or digest any organic matter'), 5)], 'bio-2-1', 'enzymes-in-washing-powder',
      at(6, 8, '(a)', '(ii)'), 5),
] + [
    T(f'8b{r}', f'Q8(b)({r})', 'B', ask(6, q), rows, 'bio-2-1', concept, at(6, 8, '(b)', f'({r})'), 6 * len(rows),
      stem=[Q8B] + extra, decision=decision)
    for r, q, rows, concept, extra, decision in [
        ('i', 'Name the enzyme you used in this investigation.',
         [pt(bracket(ENZYME)[0], 6, kind='criterion', note_sel=bracket(ENZYME)[1], note=NO_ANSWER)],
         'enzyme-used', [], 'The scheme prices a named enzyme without naming one; its bracketed direction is the '
                            'row\'s note.'),
        ('ii', 'Name the substrate of this enzyme.',
         [pt(S('Matching substrate: Matching substrate', piece=2, psep=': '), 6, kind='criterion', note=NO_ANSWER)],
         'substrate-of-the-enzyme', [M('(i)', 6), ask(6, 'Name the enzyme you used in this investigation.')], ''),
        ('iii', 'How did you vary the pH?', [pt(S('(Different) buffers'), 6)], 'varying-ph', [], ''),
        ('iv', 'Name one factor you kept constant.', [pt(S('e.g. Temperature'), 6)], 'factor-kept-constant', [], ''),
        ('v', 'How did you keep this factor constant?', [pt(S('e.g. Waterbath'), 6)], 'keeping-a-factor-constant',
         [M('(iv)', 6), ask(6, 'Name one factor you kept constant.')], ''),
        ('vi', 'How did you measure the rate of enzyme activity?',
         [pt(S('How measured/ (per unit) time', piece=1), 6, kind='criterion', note=NO_ANSWER),
          pt(S('How measured/ (per unit) time', piece=2), 6)], 'measuring-enzyme-activity', [],
         TWO_POINTS + ' Its first point is the scheme\'s "How measured", which names what earns the point.'),
        ('vii', 'What was the result of your investigation?', [pt(S('pH 4 -10'), 6)], 'result-of-the-ph-investigation',
         [], '')]
] + [
    T('9a', 'Q9(a)', 'B', ask(7, 'Give two reasons why water is important for all living organisms.'),
      [anyn(S('Transport/ solvent/ medium for', 'metabolic reactions/ temperature control', after='(a) (i) &'), 2, 5)],
      'bio-1-2', 'why-water-is-important', rq(6, 'Two reasons why water important:', path=['9']), 10,
      decision='"5 + 1" over the two reasons, carded at its first rate: one menu, claim two. The scheme sets the '
               'part\'s markers "(a) (i) &" / "(ii)" over its reprint, which heads the answer\'s own line; the answer '
               'is read from after those markers.'),
] + [
    # "Pooter." and "IAA." alone are too short a question to stand (the build's
    # floor is eight characters), so those cards carry the printed lead-in in
    # their question text instead of their stem, as 2018 Higher Q2(e) does.
    T(f'9b{r}', f'Q9(b)({r})', 'B', [Q9B, ask(7, q, br=True)] if len(q) < 8 else ask(7, q), [pt(sel, 6)], topic,
      concept, sq, 6, stem=[] if len(q) < 8 else [Q9B])
    for r, q, sel, topic, concept, sq in [
        ('i', 'Anaerobic jar.', S('To provide environment without oxygen'), 'bio-2-5', 'anaerobic-jar',
         at(6, 9, '(b)', '(i)')),
        ('ii', 'Backed blade.', S('To avoid injury or to cut thin slice'), 'bio-2-6', 'backed-blade',
         at(6, 9, '(b)', '(ii)')),
        ('iii', 'Sodium alginate.', S('To immobilise enzyme (or yeast)'), 'bio-2-1', 'sodium-alginate',
         at(6, 9, '(b)', '(iii)')),
        ('iv', 'Pooter.', S('To collect small organisms e.g. insects, spiders'), 'bio-3-1', 'pooter',
         at(6, 9, '(b)', '(iv)')),
        ('v', 'Freezer-cold ethanol.', S('To precipitate DNA (to make it insoluble or to', 'make it come out of solution)'),
         'bio-1-2', 'freezer-cold-ethanol', at(6, 9, '(b)', '(v)')),
        ('vi', 'IAA.', S('To cause (or inhibit) root growth or to cause (or inhibit) stem', 'growth or plant growth'),
         'bio-2-4', 'iaa', at(6, 9, '(b)', '(vi)')),
        ('vii', 'Starch agar or milk agar.', S('To show digestive activity during germination', '(or in seeds)'),
         'bio-2-5', 'starch-or-milk-agar', at(6, 9, '(b)', '(vii)')),
        ('viii', 'Limewater.', S('To test for carbon dioxide', after='(or in seeds)'), 'bio-2-2', 'limewater',
         rq(6, 'Limewater:', path=['9', '(b)'],
            paired='The scheme sets "(viii)" on the reprint\'s own line, so the reprint is the anchor; the answer '
                   'shares that line and is read from after (vii)\'s answer, the line printed before it.'))]
] + [
    # ------------------------------------------------------------ Section C --
] + [
    # "Allele." alone is too short a question to stand: its card carries the
    # printed lead-in in its question text instead of its stem.
    T(f'10a{r}', f'Q10(a)({r})', 'C', [Q10A, ask(8, q, br=True)] if len(q) < 8 else ask(8, q), [pt(S(ans), 7)],
      'bio-1-4', concept, at(7, 10, '(a)', f'({r})'), 7, stem=[] if len(q) < 8 else [Q10A])
    for r, q, ans, concept in [('i', 'Genotype.', 'Genetic make-up (of an organism)', 'genotype'),
                               ('ii', 'Allele.', 'Different form of a gene', 'allele'),
                               ('iii', 'Haploid.', 'One set of chromosomes', 'haploid')]
] + [
    T('10bi', 'Q10(b)(i)', 'C', Q(8, 'The structure of DNA is organised into strands.',
                                   'How many strands are there in DNA structure?'),
      [pt(S('Two'), 3)], 'bio-1-2', 'dna-strands', at(7, 10, '(b)', '(i)'), 3),
    T('10bii', 'Q10(b)(ii)', 'C', Q(8, 'Blood samples can be put through a process called DNA profiling.',
                                     'Explain the term DNA profiling.'),
      [pt(S("(Producing) patterns or bands/ of (an organism's) DNA", piece=n), 3) for n in (1, 2)], 'bio-3-3',
      'dna-profiling', at(7, 10, '(b)', '(ii)'), 6, decision=TWO_POINTS),
] + [
    T(f'10biii{n}', f'Q10(b)(iii){n}', 'C', ask(8, q), [pt(S(ans), 3)], 'bio-3-3', concept, at(7, 10, '(b)', '(iii)'),
      3, stem=[Q10BIII], decision=EACH_ITEM)
    for n, q, ans, concept in [(1, '1. What is used to cut the DNA?', 'Enzymes', 'cutting-dna'),
                               (2, '2. On what basis are the DNA fragments separated?', 'Size or length',
                                'separating-dna-fragments')]
] + [
    T('10biv', 'Q10(b)(iv)', 'C', ask(8, 'Give two applications of DNA profiling.'),
      [anyn(S('e.g. Forensic/ paternity tests'), 2, 3, open_list=True)], 'bio-3-3', 'applications-of-dna-profiling',
      at(7, 10, '(b)', '(iv)'), 6, decision='Two points ("(2 pts)") from the printed examples: one menu, claim two.'),
    T('10bv', 'Q10(b)(v)', 'C', ask(8, 'What is meant by genetic screening?'),
      [pt(S('Testing for/ (presence or absence) of a particular gene.', piece=1), 3),
       pt(S('Testing for/ (presence or absence) of a particular gene.', piece=2), 3, kind='point')], 'bio-3-3',
      'genetic-screening', rq(7, 'Genetic screening:'), 6, decision=TWO_POINTS),
] + [
    T(f'10c{r}', f'Q10(c)({r})', 'C', Q(8, *q), rows, 'bio-1-5', concept, at(7, 10, '(c)', f'({r})'), 3 * len(rows),
      stem=[Q10C], decision=decision)
    for r, q, rows, concept, decision in [
        ('i', ('What is a fossil?', 'What is a fossil?'),
         [pt(S('Remains, impression or trace of something that lived a long', 'time ago'), 3)], 'fossil', ''),
        ('ii', ('Name two places where fossils of the ‘Irish Elk’ were found.',
                'Name two places where fossils of the ‘Irish Elk’ were found.'),
         [pt(S('Bogs/ mud dried lakes', piece=n), 3) for n in (1, 2)], 'where-fossils-are-found',
         TWO_POINTS + ' The scheme prints exactly the two places asked.'),
        ('iii', ('When did the ‘Irish Elk’ become extinct in Ireland?',
                 'When did the ‘Irish Elk’ become extinct in Ireland?'), [pt(S('9,000 years ago'), 3)],
         'irish-elk-extinction', ''),
        ('iv', ('Suggest one reason why this animal became extinct.',
                'Suggest one reason why this animal became extinct.'),
         [pt(S('Disease or severe cold or over-hunting'), 3)], 'causes-of-extinction', ''),
        ('v', ('What is meant by evolution?', 'What is meant by evolution?'),
         [pt(S('(Development of) new species/ over time', piece=n), 3) for n in (1, 2)], 'evolution', TWO_POINTS),
        ('vi', ('Name either one of the two 19th century British naturalists who introduced the theory of',
                'evolution by natural selection.'), [pt(S('Darwin or Wallace'), 3)], 'darwin-or-wallace', '')]
] + [
    T('11ai', 'Q11(a)(i)', 'C', ask(9, 'Carnivore.'), [plain(CARNIVORE[0], 7, end=CARNIVORE[1])], 'bio-3-1',
      'carnivore', at(7, 11, '(a)', '(i)'), 7, stem=[Q11A],
      decision='The scheme\'s bracketed "Accept" direction, printed over two lines, is the row\'s note.'),
    T('11aii', 'Q11(a)(ii)', 'C', ask(9, 'Abiotic factor.'), [pt(S('Non-living'), 7)], 'bio-3-1', 'abiotic-factor',
      at(7, 11, '(a)', '(ii)'), 7, stem=[Q11A]),
    T('11aiii', 'Q11(a)(iii)', 'C', ask(9, 'Consumer.'), [pt(S('Eats other organisms'), 7)], 'bio-3-1', 'consumer',
      at(7, 11, '(a)', '(iii)'), 7, stem=[Q11A]),
] + [
    T(f'11b{r}', f'Q11(b)({r})', 'C', ask(9, q), rows, 'bio-3-1', concept, at(7, 11, '(b)', f'({r})'), 3 * len(rows),
      stem=[Q11B], decision=decision)
    for r, q, rows, concept, decision in [
        ('i', 'When does the queen bee come out of hibernation?',
         [pt(S('Spring (Feb., March, April, May) (1 pt)', piece=1, psep=' (1 pt)'), 3)], 'bee-hibernation',
         'The scheme glues the tariff "(1 pt)" to the answer\'s line; the answer is cut before it.'),
        ('ii', 'Where does she make her nest?', [pt(S('Old mouse hole'), 3)], 'bee-nest', ''),
        ('iii', 'What do unfertilised eggs become?', [pt(S('Males'), 3)], 'unfertilised-bee-eggs', ''),
        ('iv', 'Name two substances that the female bee collects from the flower.',
         [pt(S('Nectar/ pollen', piece=n), 3) for n in (1, 2)], 'what-bees-collect',
         TWO_POINTS + ' The scheme prints exactly the two substances asked.'),
        ('v', 'Explain the term habitat.', [pt(S('Place where an organism lives'), 3)], 'habitat', ''),
        ('vi', 'Give one reason why bee habitats have been lost.', [pt(S('Farming or forestry or housing'), 3)],
         'habitat-loss', ''),
        ('vii', 'What is meant by conservation?',
         [pt(S('(Wise) management/ of environment (2 pts)', piece=[1, n], psep=[' (2 pts)', '/']), 3)
          for n in (1, 2)], 'conservation',
         TWO_POINTS + ' The scheme glues the tariff "(2 pts)" to the answer\'s line; the answer is cut before it.')]
] + [
    T('11ci', 'Q11(c)(i)', 'C', ask(9, 'Explain the term pollution.'),
      [pt(S('Any harmful addition/ to the environment (2 pts)', piece=[1, n], psep=[' (2 pts)', '/']), 3)
       for n in (1, 2)], 'bio-3-1', 'pollution', at(7, 11, '(c )', '(i)'), 6, stem=[Q11C],
      decision=TWO_POINTS + ' The scheme glues the tariff "(2 pts)" to the answer\'s line; the answer is cut before '
                            'it. The scheme prints this part\'s marker "(c )".'),
    T('11cii', 'Q11(c)(ii)', 'C', Q11CII,
      [pt(S('Name of pollutant: Named pollutant'), 3, kind='criterion', note=NO_ANSWER),
       pt(S('Effect of pollution: Effect of this pollutant'), 3, kind='criterion', note=NO_ANSWER)], 'bio-3-1',
      'effect-of-a-pollutant', at(7, 11, '(c )', '(ii)'), 6, stem=[Q11C],
      decision='The pollutant named and its effect, a point each: a criterion row each, labelled with the scheme\'s '
               'own reprints.'),
    T('11ciii', 'Q11(c)(iii)', 'C', ask(9, 'Give one specific way of controlling the pollution referred to in (ii) above.'),
      [pt(S('Method of control'), 3, kind='criterion', note=NO_ANSWER)], 'bio-3-1', 'controlling-pollution',
      at(7, 11, '(c )', '(iii)'), 3, stem=[Q11C, M('(ii)', 9), Q11CII]),
    T('11civ', 'Q11(c)(iv)', 'C', ask(9, 'Give one example of good waste management from agriculture, fisheries or forestry.'),
      [pt(S('One example'), 3, kind='criterion', note=NO_ANSWER)], 'bio-3-1', 'waste-management',
      at(7, 11, '(c )', '(iv)'), 3, stem=[Q11C]),
    T('11cv', 'Q11(c)(v)', 'C', ask(9, 'Give two ways to minimise domestic waste.'),
      [anyn(S('Reduce/ reuse/ recycle'), 2, 3)], 'bio-3-1', 'minimising-domestic-waste', at(7, 11, '(c )', '(v)'), 6,
      stem=[Q11C], decision='Two points ("(2 pts)") from the printed three: one menu, claim two.'),
] + [
    T(f'12a{r}', f'Q12(a)({r})', 'C', ask(10, q), [pt(S(ans), 7)], 'bio-2-4', concept, at(8, 12, '(a)', f'({r})'), 7,
      stem=[Q12A])
    for r, q, ans, concept in [('i', 'The skin.', 'Barrier or antimicrobial secretions', 'skin-in-defence'),
                               ('ii', 'Cilia in the airway.', 'Move mucus out (of airways)', 'cilia-in-defence'),
                               ('iii', 'Acid in the stomach.', 'Kills pathogens', 'stomach-acid-in-defence')]
] + [
    T('12bi', 'Q12(b)(i)', 'C', ask(10, 'Draw a large labelled diagram of a typical bacterial cell.'),
      [pt(S(BACTERIAL_CELL, piece=1, psep=': Marks'), 3, kind='criterion', note_sel=S(BACTERIAL_CELL, piece=2,
                                                                                       psep='Marks '),
          note_lead='The scheme marks the diagram'),
       pt(S('Two labels'), 6, kind='criterion', units=[3, 3], note=NO_ANSWER)], 'bio-3-2', 'drawing-a-bacterial-cell',
      at(8, 12, '(b)', '(i)'), 9,
      decision='The diagram ("Marks (3,0)", one point) and its two labels ("(2 pts)", which the scheme does not '
               'name) are priced on their own: one criterion row for the diagram, one worth both points for the '
               'labels.'),
    T('12bii', 'Q12(b)(ii)', 'C', Q(10, 'Bacteria may be classified by their shape.', 'Name any two bacterial shapes.'),
      [anyn(None, 2, 3, options=[S(SHAPES, piece=[1, 1], psep=['/', ' [']), S(SHAPES, piece=2), S(SHAPES, piece=3)],
            note_sel=S(SHAPES, piece=[1, 2, 1], psep=['/', ' [', ']']))], 'bio-3-2', 'bacterial-shapes',
      at(8, 12, '(b)', '(ii)'), 6,
      decision='Two points ("(2 pts)") from the printed three: one menu, claim two; the bracketed "Accept" direction '
               'printed with the first is the row\'s note.'),
    T('12biii', 'Q12(b)(iii)', 'C', ask(10, 'Name the method by which bacteria reproduce.'), [pt(S('Binary fission'), 3)],
      'bio-3-2', 'binary-fission', at(8, 12, '(b)', '(iii)'), 3),
] + [
    T(f'12biv{n}', f'Q12(b)(iv){n}', 'C', q, [pt(S(*ans), 3)], 'bio-3-2', concept, at(8, 12, '(b)', '(iv)'), 3,
      stem=stem, decision=EACH_ITEM)
    for n, q, ans, concept, stem in [
        (1, Q12BIV1, ('Endospore',), 'endospores', []),
        (2, ask(10, '2. Give one example of such harsh environmental conditions.'),
         ('Extreme temperature or extreme pH or', 'lack of oxygen or lack of food'), 'harsh-conditions', [Q12BIV1]),
        (3, ask(10, '3. What happens to the structure when environmental conditions return to normal?'),
         ('Wall breaks down or spore germinates', 'or new (bacterial) cell forms'), 'endospore-germination',
         [Q12BIV1])]
] + [
    T(f'12c{r}', f'Q12(c)({r})', 'C', q, rows, 'bio-2-4', concept, at(8, 12, '(c)', f'({r})'), 3 * len(rows),
      stem=[Q12C] + extra, decision=decision)
    for r, q, rows, concept, extra, decision in [
        ('i', ask(10, 'Explain the term endocrine.'), [pt(S('Ductless or secretes directly into blood'), 3)],
         'endocrine', [], ''),
        ('ii', Q12CII, [pt(S('Gland name: Name of endocrine gland'), 3, kind='criterion', note=NO_ANSWER),
                        pt(S('Gland location: Location of above gland'), 3, kind='criterion', note=NO_ANSWER)],
         'endocrine-glands', [],
         'The gland named and its location, a point each: a criterion row each, labelled with the scheme\'s own '
         'reprints.'),
        ('iii', ask(10, 'What is a hormone?'), [pt(S('Chemical messenger'), 3)], 'hormone', [], ''),
        ('iv', Q12CIV, [pt(S('Hormone name'), 3, kind='criterion', note=NO_ANSWER)], 'hormone-of-the-gland',
         [M('(ii)', 10), Q12CII], ''),
        ('v', ask(10, 'Give a function of this hormone.'),
         [pt(S('Function of given hormone'), 3, kind='criterion', note=NO_ANSWER)], 'function-of-the-hormone',
         [M('(iv)', 10), Q12CIV], ''),
        ('vi', Q12CVI, [pt(S('Appropriate symptom'), 3, kind='criterion', note=NO_ANSWER)], 'hormone-deficiency',
         [M('(iv)', 10), Q12CIV], ''),
        ('vii', ask(10, 'Give one corrective measure for this deficiency.'),
         [pt(S('Appropriate corrective measure'), 3, kind='criterion', note=NO_ANSWER)], 'correcting-a-deficiency',
         [M('(vi)', 10), Q12CVI], '')]
] + [
    T('13ai', 'Q13(a)(i)', 'C', ask(11, 'Explain the term metabolism.'),
      [pt(S('(All) the chemical reactions in an organism or in a cell', 'or in the body'), 7)], 'bio-2-1', 'metabolism',
      at(8, 13, '(a)', '(i)'), 7),
] + [
    T(f'13aii{n}', f'Q13(a)(ii){n}', 'C', ask(11, q), [pt(S(line, piece=2, psep=' = '), 7)], 'bio-2-1', concept,
      at(8, 13, '(a)', '(ii)'), 7, stem=Q13AII, decision=EACH_ITEM + ' Two points on the ladder ("7 + 2(1)").')
    for n, q, line, concept in [(1, '1. Respiration.', '1. Respiration = Catabolism', 'respiration-is-catabolic'),
                                (2, '2. Photosynthesis.', '2. Photosynthesis = Anabolism', 'photosynthesis-is-anabolic')]
] + [
    T('13bi', 'Q13(b)(i)', 'C', ask(11, 'Explain the term respiration.'),
      [pt(S('Release of energy/ from food', piece=n), 3) for n in (1, 2)], 'bio-2-2', 'respiration',
      at(8, 13, '(b)', '(i)'), 6, decision=TWO_POINTS),
] + [
    T(f'13bii{n}', f'Q13(b)(ii){n}', 'C', q, [pt(S(ans), 3)], 'bio-2-2', concept, at(8, 13, '(b)', '(ii)'), 3,
      stem=[Q13BII], decision=EACH_ITEM)
    for n, q, ans, concept in [(1, ask(11, '1. Stage 1 occur?'), 'Cytoplasm', 'site-of-stage-1'),
                               (2, [M('2.', 11), ask(11, 'Stage 2 occur?')], 'Mitochondria', 'site-of-stage-2')]
] + [
    T('13biii', 'Q13(b)(iii)', 'C', ask(11, 'Write a word equation for aerobic respiration.'),
      [pt(S(EQUATION, piece=1, psep=' (1 pt)'), 3, kind='point',
          note_sel=S('[NB: all or nothing; accept formulae ]', piece=[2, 1], psep=['[', ']']))], 'bio-2-2',
      'aerobic-respiration-equation', at(8, 13, '(b)', '(iii)'), 3,
      decision='One point for the whole equation; the scheme\'s bracketed note (all or nothing; formulae accepted) '
               'is the row\'s note.'),
] + [
    T(f'13b{r}', f'Q13(b)({r})', 'C', Q(11, *q), [pt(S(ans), 3)], 'bio-2-2', concept, at(8, 13, '(b)', f'({r})'), 3)
    for r, q, ans, concept in [
        ('iv', ('What is meant by anaerobic respiration?', 'What is meant by anaerobic respiration?'),
         '(Respiration) without oxygen', 'anaerobic-respiration'),
        ('v', ('Does aerobic respiration or anaerobic respiration produce more ATP?',
               'Does aerobic respiration or anaerobic respiration produce more ATP?'), 'Aerobic (respiration)',
         'atp-yield'),
        ('vi', ('Fermentation is a form of anaerobic respiration carried out by yeasts.',
                'Name one product of this fermentation.'), 'Alcohol or ethanol or carbon dioxide',
         'products-of-fermentation'),
        ('vii', ('What acid is produced when anaerobic respiration occurs in human muscle?',
                 'What acid is produced when anaerobic respiration occurs in human muscle?'), 'Lactic (acid)',
         'lactic-acid')]
] + [
    T('13ci', 'Q13(c)(i)', 'C', ask(11, 'Explain the term photosynthesis.'),
      [pt(S('(Process by which) plants/ make their own food', piece=n), 3) for n in (1, 2)], 'bio-2-2',
      'photosynthesis', at(8, 13, '(c )', '(i)'), 6,
      decision=TWO_POINTS + ' The scheme prints this part\'s marker "(c )".'),
] + [
    T(f'13cii{n}', f'Q13(c)(ii){n}', 'C', q, rows, 'bio-2-2', concept, at(8, 13, '(c )', '(ii)'), 3 * len(rows),
      stem=stem, fig='q13-apparatus', decision=decision)
    for n, q, rows, concept, stem, decision in [
        (1, Q13CII1, [pt(S('Light (intensity) or temperature or', 'carbon dioxide (concentration)'), 3)],
         'factors-affecting-photosynthesis', [Q13CII], EACH_ITEM),
        (2, ask(11, '2. How would you vary this factor?'),
         [pt(S('Method to vary factor given in (ii) 1.'), 3, kind='criterion', note=NO_ANSWER)],
         'varying-a-factor', [Q13CII, Q13CII1], EACH_ITEM),
        (3, ask(11, '3. How would you measure the rate of photosynthesis?'),
         [pt(S('Number of bubbles or volume of oxygen/ (per unit) time', piece=n), 3) for n in (1, 2)],
         'measuring-photosynthesis', [Q13CII], EACH_ITEM + ' ' + TWO_POINTS)]
] + [
    T('13ciii', 'Q13(c)(iii)', 'C', Q(11, 'From your knowledge of photosynthesis, suggest two ways by which a gardener could',
                                      'artificially increase the yield of vegetables in a greenhouse.'),
      [anyn(S('Brighter light/ light for longer/ burning a fuel/', 'increase temperature'), 2, 3)], 'bio-2-2',
      'increasing-greenhouse-yield', at(8, 13, '(c )', '(iii)'), 6,
      decision='Two points ("(2 pts)") from the printed four: one menu, claim two.'),
    # ------------------------------------------------------- Q14 and Q15 --
    T('14ai', 'Q14(a)(i)', 'C', ask(12, 'What is blood plasma?'), [pt(S('Liquid part (of blood)'), 3)], 'bio-2-6',
      'blood-plasma', at(9, 14, '(a)', '(i)'), 3, stem=[Q14A]),
    T('14aii', 'Q14(a)(ii)', 'C', ask(12, 'Name two types of cell found in the blood and give a function for each.'),
      [pt(S(line, piece=n), 3, **({'note_sel': S(line, piece=1), 'note_lead': 'Function of'} if n == 2 else {}))
       for line in ('Red blood cells/ carry oxygen', 'White blood cells/ fight disease') for n in (1, 2)], 'bio-2-6',
      'blood-cells-and-their-functions', at(9, 14, '(a)', '(ii)'), 12, stem=[Q14A],
      decision='Two cell types, each with its function, at two points a line ("(2 pts)", "(2 pts)"): the cell and '
               'its function a row each, cut at the scheme\'s own solidus.'),
    T('14aiii', 'Q14(a)(iii)', 'C', Q(12, 'The ABO blood group system has four blood groups. Name any two of these groups.'),
      [anyn(S('A or B or AB or O'), 2, 3, sep=' or ')], 'bio-2-6', 'abo-blood-groups', at(9, 14, '(a)', '(iii)'), 6,
      stem=[Q14A], decision='Two points ("(2 pts)") from the printed four, joined by "or": one menu, claim two.'),
    T('14aiv', 'Q14(a)(iv)', 'C', Q(12, 'Blood groups can be positive (+) or negative (−) according to whether the blood contains',
                                     'or does not contain a particular factor. Name this factor.'),
      [pt(S('Rhesus (factor) or Rh (factor)'), 3)], 'bio-2-6', 'rhesus-factor', at(9, 14, '(a)', '(iv)'), 3,
      stem=[Q14A]),
    T('14av', 'Q14(a)(v)', 'C', ask(12, 'Suggest a reason why it is important to know a person’s blood group.'),
      [pt(S('(Blood) transfusions'), 3)], 'bio-2-6', 'why-blood-groups-matter', at(9, 14, '(a)', '(v)'), 3,
      stem=[Q14A]),
    T('14avi', 'Q14(a)(vi)', 'C', ask(12, 'What is the function of platelets in the blood?'),
      [pt(S('To clot the blood'), 3)], 'bio-2-6', 'platelets', at(9, 14, '(a)', '(vi)'), 3, stem=[Q14A]),
    T('14bi', 'Q14(b)(i)', 'C', ask(12, 'Explain the term excretion.'),
      [pt(S('Removal of waste products/ of metabolism or from cell', piece=n), 3) for n in (1, 2)], 'bio-2-6',
      'excretion', at(9, 14, '(b)', '(i)'), 6, decision=TWO_POINTS),
] + [
    T(f'14bii-{x.lower()}', 'Q14(b)(ii)', 'C', Q14BII, [pt(cell(URINARY[0], i, URINARY[1]), 3)], 'bio-2-6', concept,
      at(9, 14, '(b)', '(ii)'), 3, fig='q14-urinary', item=(x.lower(), x),
      labels=labels(URINARY[0], 'AB', URINARY[1], 9, asked=x),
      decision=EACH_ITEM + ' "(2 pts)" over the two labels.')
    for i, (x, concept) in enumerate([('A', 'kidney'), ('B', 'ureter')])
] + [
    T('14biii', 'Q14(b)(iii)', 'C', ask(12, 'Give the function of the part labelled C.'), [pt(S('Stores urine'), 3)],
      'bio-2-6', 'bladder', at(9, 14, '(b)', '(iii)'), 3, stem=[Q14B], fig='q14-urinary',
      labels=labels(URINARY[0], 'AB', URINARY[1], 9),
      decision='The scheme names parts A and B only; C is not named, so the label key carries A and B.'),
    T('14biv', 'Q14(b)(iv)', 'C', ask(12, 'Name two substances excreted by part A.'),
      [anyn(None, 2, 3, options=[S(EXCRETED, piece=1), S(EXCRETED, piece=2), S(EXCRETED, piece=[3, 1], psep=['/', ' ['])],
            note_sel=S(EXCRETED, piece=[3, 2, 1], psep=['/', ' [', ']']))], 'bio-2-6', 'substances-excreted-by-the-kidney',
      at(9, 14, '(b)', '(iv)'), 6, stem=[Q14B], fig='q14-urinary', labels=labels(URINARY[0], 'AB', URINARY[1], 9),
      decision='Two points ("(2 pts)") from the printed three: one menu, claim two; the bracketed direction '
               '"urine = 1pt" is the row\'s note.'),
] + [
    T(f'14bv{n}', f'Q14(b)(v){n}', 'C', ask(12, q), [pt(S(ans), 3)], 'bio-2-6', concept, at(9, 14, '(b)', '(v)'), 3,
      stem=[Q14B, Q14BV], fig='q14-urinary', labels=labels(URINARY[0], 'AB', URINARY[1], 9), decision=EACH_ITEM)
    for n, q, ans, concept in [(1, '1. Filtration.', 'Cortex', 'site-of-filtration'),
                               (2, '2. Reabsorption.', 'Medulla', 'site-of-reabsorption')]
] + [
    T('14bvi', 'Q14(b)(vi)', 'C', ask(12, 'Give a function of part A other than excretion.'),
      [pt(S('Homeostasis or osmoregulation or pH balance'), 3)], 'bio-2-6', 'other-functions-of-the-kidney',
      at(9, 14, '(b)', '(vi)'), 3, stem=[Q14B], fig='q14-urinary', labels=labels(URINARY[0], 'AB', URINARY[1], 9)),
] + [
    T(f'14c{r}', f'Q14(c)({r})', 'C', Q(12, *q), [row], 'bio-2-5', concept, at(9, 14, '(c )', f'({r})'), total,
      decision=decision)
    for r, q, row, concept, total, decision in [
        ('i', ('In the female menstrual cycle what is meant by the fertile period?',
               'In the female menstrual cycle what is meant by the fertile period?'),
         pt(S('Most likely time for fertilisation to occur'), 3), 'fertile-period', 3,
         'The scheme prints this part\'s marker "(c )".'),
        ('ii', ('Name two hormones that have a role in the menstrual cycle.',
                'Name two hormones that have a role in the menstrual cycle.'),
         anyn(S('Oestrogen/ progesterone/ FSH/ LH'), 2, 3), 'menstrual-hormones', 6,
         'Two points ("(2 pts)") from the printed four: one menu, claim two.'),
        ('iii', ('What is meant by the term infertility?', 'What is meant by the term infertility?'),
         pt(S('The inability to produce offspring'), 3), 'infertility', 3, ''),
        ('iv', ('Give one cause of infertility in women.', 'Give one cause of infertility in women.'),
         pt(S('Blockage of Fallopian tubes or failure to',
              'excessive smoking or alcohol abuse or old age or menopause'), 3), 'causes-of-female-infertility', 3, ''),
        ('v', ('In vitro fertilisation is one method used to deal with infertility.',
               'What is meant by in vitro fertilisation?'), pt(S('Fertilisation in a test tube or outside the body'), 3),
         'in-vitro-fertilisation', 3, ''),
        ('vi', ('The placenta is a structure that forms in the womb between the mother',
                'and baby during pregnancy. Give two functions of the placenta.'),
         anyn(S('Allows nutrients to pass from mother to baby/', 'blood pressures separate'), 2, 3),
         'functions-of-the-placenta', 6, 'Two points ("(2 pts)") from the printed list: one menu, claim two.'),
        ('vii', ('Many babies are breast fed after birth. Give two benefits of breastfeeding.',
                 'Many babies are breast fed after birth. Give two benefits of breastfeeding.'),
         anyn(S('Antibodies/ sterile/ balanced nutrients/', 'bonding/ uterus returns to normal size more quickly'), 2, 3),
         'benefits-of-breastfeeding', 6, 'Two points ("(2 pts)") from the printed list: one menu, claim two.')]
] + [
    T('15ai', 'Q15(a)(i)', 'C', ask(13, 'What is meant by vegetative propagation?'),
      [pt(S('Asexual/ reproduction', piece=n), 3) for n in (1, 2)], 'bio-2-5', 'vegetative-propagation',
      at(10, 15, '(a)', '(i)'), 6, decision=TWO_POINTS),
    T('15aii', 'Q15(a)(ii)', 'C', Q(13, 'Give two examples of vegetative propagation and state whether each involves a stem,',
                                     'a root, a bud or a leaf.'),
      [pt(S(EXAMPLES, piece=n), 6, units=[3, 3],
          note='The scheme prints its two examples after "e.g.", each worth two points.') for n in (1, 2)],
      'bio-2-5', 'examples-of-vegetative-propagation',
      at(10, 15, '(a)', '(ii)'), 12,
      decision='The scheme prints two examples after "e.g.", each with its matching plant part, and prices each '
               'example "(2 pts)": a row each worth its two points, cut at the scheme\'s own solidus.'),
] + [
    T(f'15aiii{n}', f'Q15(a)(iii){n}', 'C', ask(13, q), [pt(S(ans), 3)], 'bio-2-5', concept, at(10, 15, '(a)', '(iii)'),
      3, stem=[Q15AIII], fig='q15-seed',
      decision=EACH_ITEM + ' "(4 pts)" over the four numbered functions (the scheme prints the tariff at the foot '
                           'of the page).')
    for n, q, ans, concept in [(1, '1. Part that becomes the shoot.', 'Plumule', 'plumule'),
                               (2, '2. Food store for seed.', 'Cotyledon', 'cotyledon'),
                               (3, '3. Part that becomes the root.', 'Radicle', 'radicle'),
                               (4, '4. Protection.', 'Testa', 'testa')]
] + [
    T(f'15bi-{x.lower()}', 'Q15(b)(i)', 'C', ask(13, 'Name the parts labelled A and B.'),
      [pt(cell(VIRUS[0], i, VIRUS[1]), 3)], 'bio-1-1', concept, at(10, 15, '(b)', '(i)'), 3, stem=[Q15B],
      fig='q15-virus', item=(x.lower(), x), labels=labels(VIRUS[0], 'AB', VIRUS[1], 10, asked=x),
      decision=EACH_ITEM + ' "(2 pts)" over the two labels.')
    for i, (x, concept) in enumerate([('A', 'protein-coat'), ('B', 'viral-nucleic-acid')])
] + [
    T(f'15b{r}', f'Q15(b)({r})', 'C', Q(13, *q), rows, topic, concept, at(10, 15, '(b)', f'({r})'), total,
      decision=decision)
    for r, q, rows, topic, concept, total, decision in [
        ('ii', ('Name two diseases in humans caused by viruses.', 'Name two diseases in humans caused by viruses.'),
         [anyn(S('e.g. Influenza/ rabies/ AIDS/ measles/ mumps'), 2, 3, open_list=True)], 'bio-1-1', 'viral-diseases',
         6, 'Two points ("(2 pts)") from the printed examples: one menu, claim two.'),
        ('iii', ('Suggest two methods of transmission of viruses.', 'Suggest two methods of transmission of viruses.'),
         [anyn(S('e.g. Contact or water or air or transfusion'), 2, 3, sep=' or ', open_list=True)], 'bio-1-1',
         'virus-transmission', 6,
         'Two points ("(2 pts)") from the printed examples, joined by "or": one menu, claim two.'),
        ('iv', ('Why are viruses called obligate parasites?', 'Why are viruses called obligate parasites?'),
         [pt(S('Can only replicate in a living cell or host'), 3)], 'bio-1-1', 'obligate-parasites', 3, ''),
        ('v', ('Viruses can be used in the production of vaccines.', 'What is a vaccine?'),
         [pt(S('Non-disease causing dose of a pathogen/ to trigger', 'immune response', piece=n), 3) for n in (1, 2)],
         'bio-2-4', 'vaccine', 6, TWO_POINTS),
        ('vi', ('Antibiotics are not usually given to a person suffering from a viral infection.',
                'Suggest a reason for this.'), [pt(S('No effect on viruses'), 3)], 'bio-1-1',
         'antibiotics-and-viruses', 3, '')]
] + [
    T(f'15c{r}', f'Q15(c)({r})', 'C', Q(13, *q), rows, 'bio-2-4', concept, at(10, 15, '(c )', f'({r})'), total,
      stem=stem, decision=decision)
    for r, q, rows, concept, total, stem, decision in [
        ('i', ('What two skills are destroyed by Alzheimer’s disease?',
               'What two skills are destroyed by Alzheimer’s disease?'),
         [pt(S('Memory / thinking', piece=n), 3) for n in (1, 2)], 'skills-lost-in-alzheimers', 6, [Q15C],
         TWO_POINTS + ' The scheme prints exactly the two skills asked, and this part\'s marker "(c )".'),
        ('ii', ('Name the protein that may cause the brain damage associated with the disease.',
                'Name the protein that may cause the brain damage associated with the disease.'),
         [pt(S('Amyloid'), 3)], 'amyloid', 3, [Q15C], ''),
        ('iii', ('Give two symptoms of Alzheimer’s disease.', 'Give two symptoms of Alzheimer’s disease.'),
         [anyn(S('Wandering/ getting lost/ repeating questions/ problems', 'recognising family and friends'), 2, 3)],
         'symptoms-of-alzheimers', 6, [Q15C], 'Two points ("(2 pts)") from the printed four: one menu, claim two.'),
        ('iv', ('Give one possible activity that may delay the onset of the disease as people age.',
                'Give one possible activity that may delay the onset of the disease as people age.'),
         [pt(S('Social engagement or mentally stimulating pursuits'), 3)], 'delaying-alzheimers', 3, [Q15C], ''),
        ('v', ('Nerve messages are carried around the body by neurons.', 'Name any two types of neuron.'),
         [anyn(S('Motor/ sensory/ inter or relay'), 2, 3)], 'types-of-neuron', 6, [],
         'Two points ("(2 pts)") from the printed three: one menu, claim two.')]
] + [
    T(f'15cvi{n}-{route}', f'Q15(c)(vi){n}', 'C', [M(f'{n}.', 13), ask(13, q)], [row], 'bio-2-4', f'{what}-{route}',
      rq(10, sq, path=['15', '(c )']), 3, route=route, stem=[Q15CVI],
      decision=ROUTE + ' One point ("(1 pt)").')
    for n, q, what, sq, route, row in [
        (1, 'One possible cause.', 'cause-of', 'Cause:', 'parkinsons', pt(S(PCAUSE, piece=1, psep=' Failure of'), 3)),
        (1, 'One possible cause.', 'cause-of', 'Cause:', 'paralysis',
         anyn(None, 1, 3, options=[S(PCAUSE, piece=[2, 1], psep=['dopamine ', '/']),
                                   S(PCAUSE, piece=[2, 2], psep=['dopamine ', '/'])])),
        (2, 'One treatment.', 'treating', 'Treatment:', 'parkinsons',
         anyn(None, 1, 3, options=[S(PTREAT[0], piece=1), S(PTREAT[0], piece=2), S(PTREAT[1], piece=1),
                                   S(PTREAT[2], piece=1, psep=' physiotherapy')])),
        (2, 'One treatment.', 'treating', 'Treatment:', 'paralysis',
         anyn(None, 1, 3, options=[S(PTREAT[0], piece=3), S(PTREAT[0], piece=4), S(PTREAT[1], piece=2),
                                   S(PTREAT[2], piece=2, psep='drugs ')]))]
]

# Section C (b) and (c) of Q10-Q13 are fixed points beside their question's
# "7 + 2(1)" ladder: their units count to it as fixed, their cards keep their
# own marks.
LADDER_EXEMPT = {t['key'] for t in TASKS if t['sec'] == 'C' and parse_ref(t['ref'])[0] in (10, 11, 12, 13)
                 and parse_ref(t['ref'])[1] in ('b', 'c')}

FIGURES = {
    # key suffix: (doc, page, rect in PDF points, credit, letters, alt, solution)
    'q2-tissues': ('paper', 2, (156, 344, 444, 468), SEC, ['A', 'B', 'C'], 'Two circular cross-sections of plant parts side by side, numbered 1 and 2 beneath them. Section 1: a circle with a thin dark outer layer and about a dozen small oval patches, each half dark and half dotted, scattered through its inside; one patch is boxed. Section 2: a circle with a thick dark outer layer from which several long hair-like projections stick out, and at its centre a small round core with a four-armed shape inside it. A has leader lines to the inner filling of both circles, B to the boxed patch in 1 and to the central core in 2, and C to the outer layer of both circles.', False),
    'q4-skeleton': ('paper', 3, (408, 324, 566, 614), SEC, [], 'Side view of a section of the human skeleton: a column of small stacked bones with thin discs between them, curving gently from top to bottom and ending in a fused, tapering tip. Brackets on the right divide it into five printed regions, top to bottom: Cervical, Thoracic, Lumbar, Sacrum and Coccyx.', False),
    'q5-terms': ('paper', 4, (36, 38, 535, 312), SEC, [], 'Question 5 as printed: the instruction, then the list Hypothesis (struck through), Control, Data, Blind test, Theory, Replicate above a two-column table. Column A lists "An educated guess based on observations" (answered Hypothesis in Column B as the example) and parts (a) to (e): (a) Repeating an experiment, (b) Information gathered during experiments, (c) Used for comparison in experiments, (d) Where only the investigator knows what treatment the participant is receiving, (e) An idea supported by different experiments. Column B is blank beside them.', False),
    'q7-microscope': ('paper', 5, (386, 106, 560, 262), SEC, ['A', 'B'], 'Line drawing of a light microscope seen from the side: a curved arm, an upright tube with a short, wider cylinder at its top, lenses on a revolving piece beneath the tube, a flat platform with clips under the lenses, more parts below the platform, and a heavy base. A points to the short cylinder at the top of the tube; B points to the flat platform with its clips.', False),
    'q13-apparatus': ('paper', 11, (118, 425, 463, 628), SEC, [], 'Apparatus with printed labels: a Strong light source (a bulb in a reflector) at the left, beside a Metre stick running along the bottom; a Set distance arrow runs from the bulb to a beaker on the right, labelled Water bath at 25°C. In the beaker stands a test tube of NaHCO3 soln. holding a sprig of Pondweed with a Cut stem at its top, and a Thermometer stands in the water bath.', False),
    'q14-urinary': ('paper', 12, (199, 301, 398, 467), SEC, ['A', 'B', 'C'], 'Front view of the human urinary system inside the outline of the lower trunk: two bean-shaped organs, each with a small knobbly body on top, joined by short vessels to the large blood vessels running down the middle; a narrow tube runs down from each bean-shaped organ to a round bag at the bottom, which opens into a short tube below it. A points to the right-hand bean-shaped organ, B to the narrow tube running down from it, C to the round bag.', False),
    'q15-seed': ('paper', 13, (424, 99, 595, 263), SEC, [], 'Drawing of a seed cut open lengthways, with four printed labels: Testa points to the thin outer layer, Cotyledon to the large shaded bulk inside it, Plumule to a small leafy tip near the middle, and Radicle to the darker finger-shaped part running down from that tip.', False),
    'q15-virus': ('paper', 13, (390, 281, 551, 386), SEC, ['A', 'B'], 'Drawing of a virus particle: a round body with a spiky outer rim and a tangle of thread-like strands inside it. A points to the spiky outer rim; B points to the tangled strands inside.', False),
}
