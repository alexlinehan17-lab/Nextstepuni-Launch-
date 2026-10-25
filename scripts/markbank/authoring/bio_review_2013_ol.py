"""Biology 2013 Ordinary Level — reviewed task ledger, carded from the paper for the first time.

Independent visual sweep (2026-10-25), every page rendered and read:
  * The 2013 paper is one booklet (M43), 16 pages: p1 cover and instructions,
    p2-p4 Section A Questions 1-6, p5-p7 Section B Questions 7-9, p8-p13
    Section C Questions 10-15, p14-p16 "Blank Page". Sections A and B are
    answered on the paper; Section C in an answer book. No acknowledgements
    page: the Q9(b) quadrat photograph and every drawing carry no credit.
  * The marking scheme, 16 pages: p1 cover, p2 note, p3 introduction,
    cancelled and surplus answers, p4 conventions, p5-p14 Questions 1-15 (one
    table, no page numbers), p15 "Blank Page", p16 back cover (no text).

The paper keeps the long-standing shape: any five of Section A's six
questions, any two of Section B's three, any four of Section C's six, and
Questions 14 and 15 are each any two of (a), (b), (c). Every printed ask is
carded. No Biology card existed for 2013 Ordinary before this review.

This scheme prints no reprint of any question: each answer stands under its
own question number, letter and roman, every marker on a line of its own. A
task is anchored on its own part marker, found by walking the scheme's
numbering down to it (SQ path). The scheme prints Section A's heads "1." to
"6." and Q7-Q10, Q13 and Q15 as "7." over "(a)"; Q11, Q12 and Q14 set head
and letter on one line ("11. (a)", "14. (b)"), and the path walks those lines.

The scheme counts POINTS ("(1 pt)", "(3 pts)") and heads each question or
part with what they are worth. Q1 and Q5 are "5(4)", a fixed 4 per part.
Ordered splits are carded at their first rate: Q2, Q3, Q4 and Q6 "6(3) + 2"
over seven points; every Section B (a) "1 + 5" over two (read below); and in
Section C every (a) of Q10-Q12 "7 + 2(1)" over three points, every (b) of
Q10-Q13 "3(5) + 6(2)" over nine and every (c) of Q10-Q12 "2(6) + 6(2)" over
eight, each a ladder of its own part. Section B (b) is "8(3)" (Q8(b): the
drawing "D. 6,3,0 L.3(2)" and then "4(3)"), Q13(a) "3(3)" (its drawing "3,0 +
3(1)"), Q13(c) "8(3)" (its drawing "3,0 + 3") and every part of Q14 and Q15
"10(3)": a fixed mark per point. Every printed answer fits a per-response
tariff, so no part is carded whole.

Section B (a): the scheme prints "1 + 5" over each (a)'s two "(1 pt)" answers
for Q7, Q8 and Q9 (scheme p7 and p8, rendered and looked at), where the 2014
to 2020 Ordinary schemes print "5 + 1". Read by the scheme's own conventions
(p4, rule 4: "the first two correct answers are awarded 4 marks each and each
subsequent correct answer is awarded 3 marks") it is an ordered split whose
first rate is 1: each (a) card is carded at 1, as printed; no reordering is
derived.

Q13(b)(ii): the scheme prints its answer "A = Lipid / B = Protein" struck
through (rendered and looked at), beside "*7 marks to be allocated here as
long as any part of 13 (b) attempted" and "7 marks [i.e. one 5+one 2]".
Carded as printed, as 2019 Higher Q7(b)(iii)-(iv) are under Alex's rule that
a printed ask is never left out: each label a card at its place on the
"3(5) + 6(2)" ladder, its struck answer as the row and the scheme's footnote
as the row's note.

The paper prints Question 13's third part as "(b)" again (p11: "(b) Answer
the following questions in relation to an investigation you carried out into
fermentation by yeast cells."); the scheme (p12) numbers it (c), and it is
carded as Q13(c). The census reader read that second "(b)" into the first
and lost Question 4 (paper.py MISPRINTS and WELDED_HEADS, gated to this
sitting): p3's Q3(g) row ends in its circle options "T F", so the "4." head
filed as the tail of Q3(g) and Q4's (a)-(d) were lost. The two fixes take
the census from 128 leaves to the paper's 137.
"""
from bio_review_lib import Q, SQ, S, M, pt, anyn, T, L

YEAR, LEVEL = 2013, 'ol'
REVIEWED_AT = '2026-10-25'

SOURCES = {
    'paper': {'path': 'examiner-reports/biology/papers/2013-ol-paper.pdf',
              'fileid': 'LC025GLP000EV.pdf',
              'sha256': 'ddb1f40e0e70051c92304d159ad607325d592d9ea91d916049b2ca2a7d66e79a',
              'pages': 16},
    'scheme': {'path': 'examiner-reports/biology/schemes/2013-ol.pdf',
               'fileid': 'LC025GLP000EV.pdf',
               'sha256': '433c42f4000af3a9d43d04d56e8b93e6973fa0ad8e6c8ca50266db00d5b58900',
               'pages': 16},
}

PAGE_ROLES = {
    'paper': {1: 'cover', **{p: 'questions' for p in range(2, 14)}, 14: 'blank', 15: 'blank', 16: 'blank'},
    'scheme': {1: 'cover', 2: 'note', 3: 'introduction', 4: 'conventions',
               **{p: 'marking' for p in range(5, 15)}, 15: 'blank', 16: 'back-cover'},
}


def _ladder(notation, **extra):
    """An ordered split as the scheme prints it ("6(3) + 2", "1 + 5")."""
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
    **{(n, 'a'): 6 for n in (7, 8, 9)},    # paper p5: "Part (a) carries 6 marks
    **{(n, 'b'): 24 for n in (7, 8, 9)},   # and part (b) carries 24 marks"
    (13, 'a'): 9, (13, 'c'): 24,           # the paper's "(9)" and "(24)"
    **{(n, x): 30 for n in (14, 15) for x in 'abc'},   # "(30, 30)"
}
LADDERS = {
    **{q: _ladder('6(3) + 2') for q in (2, 3, 4, 6)},
    **{(n, 'a'): _ladder('7 + 2(1)') for n in (10, 11, 12)},
    **{(n, 'b'): _ladder('3(5) + 6(2)') for n in (10, 11, 12, 13)},
    **{(n, 'c'): _ladder('2(6) + 6(2)') for n in (10, 11, 12)},
}

CHECKSUMS = {
    1: {4: 5}, 2: {3: 7}, 3: {3: 7}, 4: {3: 7}, 5: {4: 5}, 6: {3: 7},
    (7, 'b'): {3: 8}, (8, 'b'): {6: 1, 2: 3, 3: 4}, (9, 'b'): {3: 8},
    **{(n, 'a'): {7: 3} for n in (10, 11, 12)},
    **{(n, 'b'): {5: 9} for n in (10, 11, 12, 13)},
    **{(n, 'c'): {6: 8} for n in (10, 11, 12)},
    (13, 'a'): {3: 2, 1: 3}, (13, 'c'): {3: 8},
    **{(n, x): {3: 10} for n in (14, 15) for x in 'abc'},
}

SCAN_PAGES = {'paper': range(1, 14)}
SELECTION_SCAN = [
    ('paper', 1, 'any five', 'Cover rubric, Section A: whole-question choice; every question is carded.'),
    ('paper', 1, 'any two', 'Cover rubric, Section B: whole-question choice; every question is carded.'),
    ('paper', 1, 'any four', 'Cover rubric, Section C: whole-question choice; every question is carded.'),
    ('paper', 2, 'any five', 'Section A rubric repeated.'),
    ('paper', 2, 'the following', 'Q1 lead-in: every part asked, one card per letter.'),
    ('paper', 3, 'the following', 'Q3 lead-in: every statement asked, one card per letter.'),
    ('paper', 3, 'or', 'Q3 "true (T) or false (F)": the answer options.'),
    ('paper', 3, 'or', 'Q3 "T or F": the answer options.'),
    ('paper', 4, 'choose', 'Q5 "Choose each term": every description matched, one card per lettered part.'),
    ('paper', 4, 'the following', 'Q5 list of terms: the options.'),
    ('paper', 5, 'any two', 'Section B rubric repeated.'),
    ('paper', 5, 'the following', 'Q7(b) lead-in: every part asked.'),
    ('paper', 5, 'or', 'Q7(b) lead-in "light intensity or carbon dioxide concentration": the candidate ticks the '
                       'factor; the scheme prints one menu per part with each factor\'s answers in it, so no route.'),
    ('paper', 5, 'or', 'Q7(b)(ii) "the light intensity or the carbon dioxide concentration": the same ticked factor; '
                       'the scheme prints both answers, joined by its own "OR", as one claim-one menu.'),
    ('paper', 6, 'the following', 'Q8(b) lead-in: every part asked.'),
    ('paper', 8, 'any four', 'Section C rubric repeated.'),
    ('paper', 8, 'the following', 'Q10(a) lead-in: every term asked, one card per roman.'),
    ('paper', 8, 'or', 'Q10(c) "Using a Punnett square or otherwise": a method the candidate chooses; the scheme '
                       'prices "Punnett square or other scheme shown" alike.'),
    ('paper', 8, 'or', 'Q10(c) "male or female": description.'),
    ('paper', 9, 'the following', 'Q11(a) lead-in: every term asked, one card per roman.'),
    ('paper', 9, 'any two', 'Q11(c)(i) "State any two types of pollution": two answers from the scheme\'s menu.'),
    ('paper', 9, 'or', 'Q11(c)(ii)1 "agriculture or forestry or fisheries": a choose-one area the scheme prices '
                       'alike ("Example of waste"), so no route.'),
    ('paper', 9, 'or', 'Q11(c)(ii)1, the second "or" of the same list.'),
    ('paper', 11, 'the following', 'Q13(c) (printed "(b)") lead-in: every part asked.'),
    ('paper', 12, 'any two', 'Q14 "any two of (a), (b), (c)": whole-part choice; every part is carded.'),
    ('paper', 12, 'or', 'Q14(c)(vii) "a disorder of the ear or of the eye": a choose-one the scheme prices alike '
                        '("Disorder/ Corrective measure"), so no route.'),
    ('paper', 13, 'any two', 'Q15 "any two of (a), (b), (c)": whole-part choice; every part is carded.'),
    ('paper', 13, 'or', 'Q15(b)(ii) "a stem, a root, a leaf or a bud": the answer options.'),
    ('paper', 13, 'or', 'Q15(b)(iv) "gardeners or horticulturists": description.'),
    ('paper', 13, 'or', 'Q15(c)(iv) "living or dead": the answer options.'),
]

ROUTES = {}

SEC = 'State Examinations Commission'
NO_REPRINT = 'The scheme prints no reprint of any question: anchored on the part\'s own marker.'
EACH_ITEM = 'A list the scheme prices entry by entry: one card per entry, each its own slice of the printed line.'
NO_ANSWER = 'The scheme prints no answer here, only what earns the marks.'
TWO_POINTS = 'The scheme prices this part at two points: each printed point its own row.'
MENU = '{n} ("{pts}") from the printed list: one menu, claim {claim}.'
STRUCK = 'The scheme prints this answer struck through, beside its note:'
ONE_FIVE = ('The scheme prints "1 + 5" over (a)\'s two "(1 pt)" answers, where the 2014-2020 Ordinary schemes print '
            '"5 + 1". Read as the conventions page (p4, rule 4) defines an ordered split, the first correct answer '
            'would earn 1 and the second 5, which prices neither printed answer on its own, so the part is one card at '
            'the rubric\'s printed 6 ("Part (a) carries 6 marks"), every row unpriced (the coordinator\'s whole-part '
            'rule, as 2013 Higher Q5 and Q6; the author had carded each answer at 1). Brought to Alex.')


def at(page, *path_and_marker, why=NO_REPRINT, nth=1):
    """The part's own marker under its printed question (and letter) lines on the scheme page."""
    *path, marker = path_and_marker
    return SQ(page, marker, path=path, paired=why, bare=True, nth=nth)


def ask(page, sentence, **kw):
    """A one-line ask closed by its own punctuation."""
    return Q(page, sentence, sentence, **kw)


def dots(page, sentence, sep='…', **kw):
    """An ask that runs straight into its printed answer dots: the line cut at the dots."""
    return Q(page, sentence, piece=1, psep=sep, **kw)


def eg(start, end=None, **kw):
    """A scheme menu printed after its "e.g.": the list itself, cut after the scheme's own "e.g."."""
    return S(start, end, piece=2, psep='e.g. ', **kw)


def labels(cells, asked=None):
    """A figure's label key: [(letter, meaning selector)]."""
    return [L(x, sel, x == asked) for x, sel in cells]


# ------------------------------------------------------------ question text --
Q1 = Q(2, 'Use your knowledge of nutrients to answer the following questions:')
Q2 = Q(2, 'The diagram shows the structure of a flowering plant.')
Q2B = ask(2, 'Give one main function of each of the parts labelled A, B and C.')
Q3 = Q(3, 'Indicate whether the following statements are true (T) or false (F) by drawing a circle around T or F in',
       'each case.')
Q4 = Q(3, 'The diagram shows the cell cycle.')
Q4A = Q(3, 'There are two parts in the cell cycle – cell division and interphase.',
        'Match these two parts to the letters in the diagram.')
Q5 = [Q(4, 'Choose each term from the following list and place it in Column B to match a description in',
        'Column A. The first one has been completed as an example.'),
      Q(4, 'List: Amylase; Temperature; Substrate; Immobilised; Reusable; Protein.')]
Q6 = Q(4, 'The diagram shows a vertical section through a human kidney.')
Q7B = [Q(5, 'Answer the following questions in relation to an investigation that you carried out to study the effect',
         'of light intensity or carbon dioxide concentration on the rate of photosynthesis.'),
       ask(5, 'Tick the factor you will refer to.')]
Q8B = ask(6, 'Answer the following in relation to an activity you carried out to demonstrate osmosis.')
Q9BII = ask(7, 'Name the piece of apparatus shown.')
Q10A = Q(8, 'Explain the following terms used in genetics:')
Q10B = Q(8, 'There are four bases in DNA structure.', 'These are adenine (A), cytosine (C), thymine (T) and guanine (G).')
Q10C = [Q(8, 'In humans, sex is determined by genes located on pairs of chromosomes called sex chromosomes.'),
        Q(8, 'Using a Punnett square or otherwise, show that there is an equal chance of a child being male or',
          'female.')]
Q10C_GIVE = Q(8, 'In your answer give:')
Q11A = Q(9, 'Explain the following terms as used in ecology:')
Q11B = [Q(9, 'Climate Change'),
        Q(9, 'There is now widespread evidence that the emission of greenhouse gases', 'escaping back into space.')]
Q11BV = [Q(9, 'The diagram below shows the carbon cycle.'),
         Q(9, 'In your answer book match the terms from the list below to the letters A, B, C, D and E in the',
           'diagram.'),
         Q(9, 'List: Photosynthesis; Respiration; Eaten by; Combustion; Decay.', br=True)]
Q11C = Q(9, 'Improper waste disposal may cause pollution.')
Q11CII1 = Q(9, '1. Give one example of a waste associated with agriculture or forestry or fisheries.')
Q12B = Q(10, 'The diagram shows the foetus in the womb.')
Q12C = Q(10, 'The diagram shows a regular female menstrual cycle.')
Q13B = Q(11, 'The diagram below shows the ultrastructure of a section of cell membrane.')
Q13C = Q(11, 'Answer the following questions in relation to an investigation you carried out into fermentation by',
         'yeast cells.')
Q14A = Q(12, 'The diagram shows a synovial joint.')
Q14BV = Q(12, 'The heart pumps blood around the body.')
Q14BV1 = ask(12, '1. Name the structure in the heart that controls the heartbeat.')
Q14C = Q(12, 'The diagram shows the human ear.')
Q15A = Q(13, 'The diagram shows the structure of a flower.')
Q15C = Q(13, 'The diagrams show two types of vascular tissue in plants.')

# ------------------------------------------------------- scheme cell lines --
PLANT = 'A = Stem or internode B = Leaf or midrib C = Root'
PLANT_CUTS = [(' B =', 'internode '), (' C =', 'midrib ')]
FUNCTIONS = {'A': ('Function of A: e.g. photosynthesis/support/ transport/ (food)', 'storage'),
             'B': ('Function of B: e.g. photosynthesis/ transpiration/ gaseous', 'exchange/ (food) storage'),
             'C': ('Function of C: e.g. anchorage/ absorption (of water or', 'minerals)/ (food) storage')}
CYCLE = 'Cell division = A/ Interphase = B'
KIDNEY = 'A = Cortex B = Medulla/ Pyramid C = Ureter'
KIDNEY_CUTS = [(' B =', 'Cortex '), (' C =', 'Pyramid ')]
CONSISTENT = S('If parts (ii), (iii), (iv) and (vi) are not consistent from answer to',
               'answer then go with version that yields the greater marks.', after='(b)')
RESULT = ('Greater light intensity or higher CO2 conc./ → higher rate of', 'photosynthesis')
BASES = 'X = Thymine or T Y = Cytosine or C'
BASES_CUTS = [(' Y =', 'or T ')]
GAMETES = 'Female gametes → X / Male gametes → X and Y'
CARBON1 = 'A= Decay; B= Photosynthesis; C= Combustion;'
CARBON2 = 'D= Eaten by; E= Respiration'
CARBON = [('A', CARBON1, 1), ('B', CARBON1, 2), ('C', CARBON1, 3), ('D', CARBON2, 1), ('E', CARBON2, 2)]
SEQUENCES = S('[If no explicit matching is given then accept as fully correct either', 'respective sequences.]',
              piece=[2, 1], psep=['[', ']'])
MINIMISE = 'e.g. Reduce/ Reuse / Recycle [Not multiple examples from same category]'
BABY = ('Benefit for baby: mother-baby bonding/ antibodies in milk/', 'body temperature')
MOTHER = ('Benefit for mother: bonding/ uterus recovers faster/ natural', 'contraceptive/ reduces risk of breast cancer')
MEMBRANE = ('A = Lipid / B = Protein *7 marks to be allocated here as', 'long as any part of 13 (b) attempted')
FERMENTER = ('Diagram and one label [only acceptable labels: oil; airlock;',
             'tube, where the tube is delivering gas into liquid]')
JOINT = 'A = Ligament/ B = Cartilage/ C = Synovial fluid'
VERTEBRAE = ('Thoracic - back of chest/ Lumbar - small of back/', 'Sacral - back of pelvis/ Caudal or coccyx - tail end')
HEART = '1. Pacemaker/ 2. Right atrium'
EAR = 'A =Semicircular canals/ B = Cochlea'
FLOWER = 'A = Stigma/ B = Anther/ C = Ovary/ D= Sepal'


def plant_labels(asked=None):
    return labels([(x, meaning(PLANT, i, PLANT_CUTS, 5)) for i, x in enumerate('ABC')], asked)


def cell(line, i, cuts, page=None):
    """Cell i of a scheme line printed as cells ("A = Cortex B = Medulla/ Pyramid C = Ureter"), cut at the
    cells' own printed boundaries: cuts[k] = (text opening cell k+1, text closing cell k)."""
    pieces, seps = [], []
    if i > 0:
        pieces.append(2)
        seps.append(cuts[i - 1][1])
    if i < len(cuts):
        pieces.append(1)
        seps.append(cuts[i][0])
    return S(line, page=page, piece=pieces, psep=seps)


def meaning(line, i, cuts, page):
    """The answer alone of cell i (after its " = "), for a figure's label key."""
    sel = cell(line, i, cuts, page=page)
    return {**sel, 'piece': sel['piece'] + [2], 'psep': sel['psep'] + [' = ']}


def kidney_labels(asked=None):
    return labels([(x, meaning(KIDNEY, i, KIDNEY_CUTS, 6)) for i, x in enumerate('ABC')], asked)


def cycle_labels():
    # The scheme prints "Cell division = A/ Interphase = B": the meaning is the cell's left side.
    return [L(x, S(CYCLE, page=6, piece=[k, 1], psep=['/', ' = ']), True) for k, x in ((1, 'A'), (2, 'B'))]


def bases_labels(asked=None):
    return labels([(x, meaning(BASES, i, BASES_CUTS, 9)) for i, x in enumerate('XY')], asked)


def carbon_labels(asked=None):
    return labels([(x, S(line, page=10, piece=[k, 2], psep=[';', '='])) for x, line, k in CARBON], asked)


def membrane_labels(asked=None):
    return labels([(x, S(*MEMBRANE, page=12, piece=[1, k, 2], psep=[' *', ' / ', ' = ']))
                   for k, x in ((1, 'A'), (2, 'B'))], asked)


def joint_labels(asked=None):
    return labels([(x, S(JOINT, page=13, piece=[k, 2], psep=['/', ' = '])) for k, x in ((1, 'A'), (2, 'B'), (3, 'C'))],
                  asked)


def ear_labels(asked=None):
    return labels([(x, S(EAR, page=13, piece=[k, 2], psep=['/', '='])) for k, x in ((1, 'A'), (2, 'B'))], asked)


def flower_labels(asked=None):
    return labels([(x, S(FLOWER, page=14, piece=[k, 2], psep=['/', '=']))
                   for k, x in ((1, 'A'), (2, 'B'), (3, 'C'), (4, 'D'))], asked)


def tissue_labels(asked=None):
    return labels([(x, S(f'{x} = {name}', page=14, piece=2, psep=' = '))
                   for x, name in (('A', 'Xylem'), ('B', 'Phloem'))], asked)


TASKS = [
    # ------------------------------------------------------------ Section A --
] + [
    T(f'1{x}', f'Q1({x})', 'A', q, [row], 'bio-1-2', concept, at(5, '1.', f'({x})'), 4, stem=[Q1],
      decision=decision)
    for x, q, row, concept, decision in [
        ('a', Q(2, 'Proteins always contain the elements carbon, hydrogen, oxygen and'), pt(S('Nitrogen'), 4),
         'elements-in-protein', ''),
        ('b', ask(2, 'Glucose is an example of which type of biomolecule?'),
         anyn(S('Carbohydrate/ monosaccharide/ sugar'), 1, 4), 'glucose-is-a-carbohydrate',
         'One point ("(1 pt)"), any one of the printed alternatives: a menu, claim one.'),
        ('c', Q(2, 'An example of a fat-soluble vitamin is'), anyn(S('A/ D/ E/ K'), 1, 4), 'fat-soluble-vitamins',
         'One point ("(1 pt)"), any one of the four printed vitamins: a menu, claim one.'),
        ('d', Q(2, 'A solution used to test for the presence of glucose is'), anyn(S('Benedict'), 1, 4),
         'test-for-glucose', 'One point ("(1 pt)"), either printed solution: a menu, claim one.'),
        ('e', Q(2, 'Calcium and iron are examples of essential'), anyn(S('Minerals / elements'), 1, 4),
         'minerals', 'One point ("(1 pt)"), either printed word: a menu, claim one.')]
] + [
    T(f'2a-{x.lower()}', 'Q2(a)', 'A', ask(2, 'Name the parts labelled A, B, and C.'), [pt(cell(PLANT, i, PLANT_CUTS), 3)],
      'bio-2-6', concept, at(5, '2.', '(a)'), 3, stem=[Q2], fig='q2-plant', item=(x.lower(), x),
      labels=plant_labels(x), decision=EACH_ITEM + ' Three points ("(3 pts)") of the "6(3) + 2" ladder, one per label.')
    for i, (x, concept) in enumerate([('A', 'stem'), ('B', 'leaf'), ('C', 'root')])
] + [
    T(f'2b-{x.lower()}', 'Q2(b)', 'A', [Q2B, Q(2, f'Function of part {x}', piece=1, psep=' …', br=True)],
      [anyn(eg(*FUNCTIONS[x]), 1, 3, open_list=True)], 'bio-2-6', concept, at(5, '2.', '(b)'), 3, stem=[Q2],
      fig='q2-plant', item=(x.lower(), x), labels=plant_labels(),
      decision=EACH_ITEM + ' Three points ("(3 pts)"), one per part; each part\'s printed "e.g." list is a menu, '
                           'claim one, cut after the scheme\'s own "e.g.".')
    for x, concept in [('A', 'function-of-the-stem'), ('B', 'function-of-the-leaf'), ('C', 'function-of-the-root')]
] + [
    T('2c', 'Q2(c)', 'A', ask(2, 'Flowers are the organs of which type of reproduction in the plant?'),
      [pt(S('Sexual'), 3)], 'bio-2-5', 'flowers-are-for-sexual-reproduction', at(5, '2.', '(c)'), 3, stem=[Q2],
      fig='q2-plant'),
] + [
    T(f'3{x}', f'Q3({x})', 'A', ask(3, q), [row], topic, concept, at(5, '3.', f'({x})'), 3, stem=[Q3],
      decision=decision)
    for x, q, row, topic, concept, decision in [
        ('a', 'Metabolism is the sum of all the chemical reactions in the body.', pt(S('T'), 3), 'bio-1-1',
         'metabolism', ''),
        ('b', 'Anabolism is the breaking down of large molecules.', pt(S('F'), 3), 'bio-1-1', 'anabolism', ''),
        ('c', 'Nutrition is the way living organisms get rid of waste.', pt(S('F'), 3), 'bio-1-1', 'nutrition', ''),
        ('d', 'The term abiotic refers to the living factors in an ecosystem.', pt(S('F'), 3), 'bio-3-1',
         'abiotic-factors', ''),
        ('e', 'In science, a hypothesis is an educated guess based on observations.', pt(S('T'), 3), 'bio-u2',
         'hypothesis', ''),
        ('f', 'In experiments the factor that is changed is called the variable.', anyn(S('T/F'), 1, 3), 'bio-u2',
         'variable', 'The scheme prints "T/F": either answer earns the point, a menu, claim one.'),
        ('g', 'Grazing food chains begin with animals.', pt(S('F'), 3), 'bio-3-1', 'grazing-food-chains', '')]
] + [
    T(f'4a-{slug}', 'Q4(a)', 'A', [Q4A, Q(3, name, piece=1, psep=' …', br=True)],
      [pt(S(CYCLE, piece=k), 3)], 'bio-2-3', slug, at(6, '4.', '(a)'), 3, stem=[Q4], fig='q4-cycle',
      item=(slug, name), labels=cycle_labels(),
      decision=EACH_ITEM + ' The scheme prints "Cell division = A/ Interphase = B" ("(2 pts)"): one card per part '
                           'of the cycle, as the paper sets its two blanks, cut at the scheme\'s own solidus.')
    for k, slug, name in [(1, 'cell-division', 'Cell division'), (2, 'interphase', 'Interphase')]
] + [
    T('4b', 'Q4(b)', 'A', ask(3, 'Name the two types of cell division.'),
      [pt(S('1. Mitosis 2. Meiosis (any order)', piece=[1, 2], psep=[' 2. ', '1. ']), 3,
          note_sel=S('1. Mitosis 2. Meiosis (any order)', piece=[2, 2, 1], psep=[' 2. ', ' (', ')'])),
       pt(S('1. Mitosis 2. Meiosis (any order)', piece=[2, 1], psep=[' 2. ', ' (']), 3)],
      'bio-2-3', 'types-of-cell-division', at(6, '4.', '(b)'), 6,
      decision=TWO_POINTS + ' The scheme prints "1. Mitosis 2. Meiosis (any order)": cut after its own numbers, '
                            'its "(any order)" the first row\'s note.'),
    T('4c', 'Q4(c)', 'A', Q(3, 'Cancer is the uncontrolled multiplication of abnormal cells. Give two causes of cancer.'),
      [anyn(eg('Two causes: e.g. viruses/ radiation/ (cigarette) smoking/', 'named pollutant'), 2, 3, open_list=True)],
      'bio-2-3', 'causes-of-cancer', at(6, '4.', '(c)'), 6,
      decision=MENU.format(n='Two points', pts='2 pts', claim='two') + ' Cut after the scheme\'s own "e.g.".'),
    T('4d', 'Q4(d)', 'A', dots(3, 'Suggest a possible treatment for cancer'),
      [anyn(eg('A treatment: e.g. chemotherapy/ radiotherapy/ surgery'), 1, 3, open_list=True)],
      'bio-2-3', 'treating-cancer', at(6, '4.', '(d)'), 3,
      decision='One point ("(1 pt)"), any one of the scheme\'s examples: a menu, claim one.'),
] + [
    T(f'5{x}', f'Q5({x})', 'A', ask(4, q), [pt(S(ans), 4)], 'bio-2-1', concept, at(6, '5.', f'({x})'), 4,
      stem=Q5, qfig='q5-table',
      decision='The list of terms (its "Amylase" struck through as the worked example) and the table are shown as the '
               'question\'s own print.')
    for x, q, ans, concept in [
        ('a', 'The group of biomolecules to which enzymes belong.', 'Proteins', 'enzymes-are-proteins'),
        ('b', 'Enzyme activity is affected by this.', 'Temperature', 'temperature-and-enzymes'),
        ('c', 'Enzymes trapped in an inactive material.', 'Immobilised', 'immobilised-enzymes'),
        ('d', 'The substance with which an enzyme reacts.', 'Substrate', 'substrate'),
        ('e', 'Advantage of using immobilised enzymes.', 'Reusable', 'advantage-of-immobilised-enzymes')]
] + [
    T(f'6a-{x.lower()}', 'Q6(a)', 'A', ask(4, 'Name the parts labelled A, B and C.'),
      [pt(cell(KIDNEY, i, KIDNEY_CUTS), 3)], 'bio-2-6', concept, at(6, '6.', '(a)'), 3, stem=[Q6], fig='q6-kidney',
      item=(x.lower(), x), labels=kidney_labels(x), decision=EACH_ITEM + ' "(3 pts)" over the three labels.')
    for i, (x, concept) in enumerate([('A', 'renal-cortex'), ('B', 'renal-medulla'), ('C', 'ureter')])
] + [
    T(f'6{x}', f'Q6({x})', 'A', dots(4, q), [row], 'bio-2-6', concept, at(6, '6.', f'({x})'), 3, stem=[Q6],
      fig='q6-kidney', labels=kidney_labels() if letters else None, decision=decision)
    for x, q, row, concept, letters, decision in [
        ('b', 'Name the organ that is attached to the kidney by part C.', pt(S('Bladder'), 3), 'bladder', True, ''),
        ('c', 'Name one substance excreted by the kidneys.', anyn(S('Urine/ Urea/ Water/ Salt'), 1, 3),
         'substances-excreted-by-the-kidneys', False, 'One point ("(1 pt)"), any one of the printed substances: a menu, '
                                                      'claim one.'),
        ('d', 'Name the site in the kidney where filtration takes place', anyn(S('Cortex/ Bowman', 'named in (a)'), 1, 3),
         'site-of-filtration', True, 'One point ("(1 pt)"), any one of the printed answers: a menu, claim one.'),
        ('e', 'Suggest one possible treatment for kidney failure', anyn(eg('e.g. Dialysis/ transplant'), 1, 3,
                                                                         open_list=True),
         'treating-kidney-failure', False, 'One point ("(1 pt)"), any one of the scheme\'s examples: a menu, claim '
                                           'one.')]
] + [
    # ------------------------------------------------------------ Section B --
    T('7a', 'Q7(a)', 'B',
      [M('(i)', 5), dots(5, 'Where in a plant cell does photosynthesis take place?', sep='..'),
       M('(ii)', 5, br=True), dots(5, 'Name the gas released during photosynthesis')],
      [pt(S('Chloroplast'), 0), pt(S('Oxygen'), 0)], 'bio-2-2', 'photosynthesis-site-and-gas',
      at(7, '7.', '(a)', '(i)'), 6, tariff='questionTotal', decision=ONE_FIVE),
] + [
    T(f'7b{r}', f'Q7(b)({r})', 'B', q, rows, 'bio-2-2', concept, at(7, '7.', '(b)', f'({r})'), 3 * len(rows),
      stem=Q7B, fig='q7-apparatus', decision=decision)
    for r, q, rows, concept, decision in [
        ('i', dots(5, 'Name the plant that you used', sep='..'),
         [pt(S('Name of plant [must be aquatic]', piece=1, psep=' ['), 3, kind='criterion', note=NO_ANSWER,
             note_sel=S('Name of plant [must be aquatic]', piece=[2, 1], psep=[' [', ']']))],
         'plant-for-photosynthesis-rate', 'The scheme prices a named plant without printing one; its bracketed '
                                          'direction is the row\'s note.'),
        ('ii', ask(5, 'How did you vary the light intensity or the carbon dioxide concentration?'),
         [anyn(None, 1, 3, options=[S('Increased or decreased lamp-beaker distance'), S('Different concs of NaHCO3')],
               note_sel=CONSISTENT)], 'varying-the-factor',
         'One point ("(1 pt)"): the scheme prints an answer for each factor, joined by its own "OR": a menu, claim '
         'one. Its direction over (b) on parts (ii), (iii), (iv) and (vi) is the row\'s note.'),
        ('iii', ask(5, 'Name one factor that you kept constant during the investigation.'),
         [anyn(eg('e.g. Temperature/ light intensity if CO2 ticked/ CO2 conc. if light', 'intensity ticked'), 1, 3,
               open_list=True, note_sel=CONSISTENT)], 'factor-kept-constant',
         'One point ("(1 pt)"), any one of the scheme\'s examples, each with its own printed condition: a menu, claim '
         'one.'),
        ('iv', ask(5, 'How did you keep that factor constant?'),
         [anyn(S('Water bath if temperature/ (same) lamp at same distance if light',
                 'intensity/ same conc NaHCO3 if CO2 conc.'), 1, 3, note_sel=CONSISTENT)], 'keeping-a-factor-constant',
         'One point ("(1 pt)"), the printed answer for the factor kept constant: a menu, claim one.'),
        ('v', ask(5, 'How did you measure the rate of photosynthesis?'),
         [pt(S('(Count) bubbles/ per unit time', piece=n), 3) for n in (1, 2)], 'measuring-the-rate',
         TWO_POINTS + ' Cut at the scheme\'s own solidus.'),
        ('vi', ask(5, 'What was the result of your investigation?'),
         [pt(S(*RESULT, piece=1), 3, note_sel=S('OR', 'Opposite statement')),
          pt(S(*RESULT, piece=2), 3, note_sel=CONSISTENT)], 'result-of-photosynthesis-investigation',
         TWO_POINTS + ' Cut at the scheme\'s own solidus; its "OR Opposite statement" is the first row\'s note.')]
] + [
    T('8a', 'Q8(a)', 'B',
      [M('(i)', 6), ask(6, 'Which substance moves through cell membranes by osmosis?'),
       M('(ii)', 6, br=True),
       Q(6, 'Name one other term used in biology to describe the movement of substances through cell', 'membranes.')],
      [pt(S('Water'), 0), anyn(S('Diffusion/ active transport'), 1, 0)], 'bio-2-6', 'movement-through-membranes',
      at(7, '8.', '(a)', '(i)'), 6, tariff='questionTotal', decision=ONE_FIVE + ' (ii) prints either term.'),
    T('8bi', 'Q8(b)(i)', 'B', ask(6, 'In the space below, draw a labelled diagram of the apparatus you used in your demonstration.'),
      [pt(S('Diagram + 3 labels', piece=1, psep=' + '), 6, kind='criterion', note=NO_ANSWER, note_sel=S('D. 6,3,0')),
       pt(S('Diagram + 3 labels', piece=2, psep=' + '), 6, kind='criterion', units=[2, 2, 2], note=NO_ANSWER,
          note_sel=S('L.3(2)', 'L.3(2)'))], 'bio-2-6', 'drawing-an-osmosis-apparatus', at(7, '8.', '(b)', '(i)'), 12,
      stem=[Q8B],
      decision='The scheme prices the drawing on its own row, "Diagram + 3 labels" at "D. 6,3,0 L.3(2)": the diagram '
               '(6, 3 or 0) and the three labels at 2 each, a criterion row each, cut at the scheme\'s own "+", each '
               'carrying its printed tariff as its note. "4(3)" follows for (ii)-(v).'),
] + [
    T(f'8b{r}', f'Q8(b)({r})', 'B', ask(6, q), [pt(S(ans), 3)], topic, concept, at(7, '8.', '(b)', f'({r})'), 3,
      stem=[Q8B])
    for r, q, ans, topic, concept in [
        ('ii', 'Suggest a control that you might use in this activity.', 'Same concentrations e.g. only water (in bag)',
         'bio-2-6', 'osmosis-control'),
        ('iii', 'State the result(s) of your investigation.',
         'e.g. increase (or decrease) in mass or volume of Visking tubing', 'bio-2-6', 'osmosis-result'),
        ('iv', 'Briefly explain the result(s) referred to in part (iii).', 'Water moved into (or out of) tubing',
         'bio-2-6', 'explaining-the-osmosis-result'),
        ('v', 'What is the purpose of a control in scientific experiments?', 'To compare (with the experiment)',
         'bio-u2', 'purpose-of-a-control')]
] + [
    T('9a', 'Q9(a)', 'B',
      [ask(7, '(i) In ecology, what is meant by the term conservation?'),
       M('(ii)', 7, br=True), ask(7, 'Suggest why conservation is important in an ecosystem.')],
      [pt(S('Wise management of natural resources'), 0),
       anyn(S('To prevent extinction/ (to maintain) biodiversity/ (to maintain) the', 'balance of nature'), 1, 0)],
      'bio-3-1', 'conservation', at(8, '9.', '(a)', '(i)'), 6, tariff='questionTotal',
      decision=ONE_FIVE + ' (ii) prints three reasons, any one.'),
    T('9bi', 'Q9(b)(i)', 'B', Q(7, 'As part of your ecosystem study, you used various pieces of apparatus to collect animals for',
                                 'in each case name the apparatus and an animal collected.'),
      [pt(S(line, nth=nth), 3, kind='criterion', note=NO_ANSWER) for line, nth in
       [('Apparatus 1name', 1), ('Named animal', 1), ('Diagram', 1), ('Apparatus 2 name', 1), ('Named animal', 2),
        ('Diagram', 2)]],
      'bio-3-1', 'apparatus-for-collecting-animals', at(8, '9.', '(b)', '(i)'), 18,
      decision='Six points ("(6 pts)"), each printed on its own line: a criterion row each, in the scheme\'s order '
               '(its "Apparatus 1name" lifted as printed). The scheme prints no apparatus, animal or drawing.'),
    T('9bii', 'Q9(b)(ii)', 'B', Q9BII, [pt(S('Quadrat'), 3)], 'bio-3-1', 'quadrat', at(8, '9.', '(b)', '(ii)'), 3,
      fig='q9-quadrat'),
    T('9biii', 'Q9(b)(iii)', 'B', ask(7, 'What is this piece of apparatus used for in your ecology studies?'),
      [pt(S('Quantitative surveys e.g. distribution, frequency, cover'), 3)], 'bio-3-1', 'uses-of-a-quadrat',
      at(8, '9.', '(b)', '(iii)'), 3, stem=[M('(ii)', 7), Q9BII], fig='q9-quadrat'),
    # ------------------------------------------------------------ Section C --
] + [
    # The terms alone ("Gene.", "Allele.") are too short a question to stand:
    # each card carries the printed lead-in in its question text.
    T(f'10a{r}', f'Q10(a)({r})', 'C', [Q10A, ask(8, term, br=True)], [row], 'bio-1-4', concept,
      at(9, '10.', '(a)', f'({r})'), 7, decision=decision)
    for r, term, row, concept, decision in [
        ('i', 'Gene.', anyn(S('Unit of heredity/ functional section of DNA'), 1, 7), 'gene',
         'One point of the "7 + 2(1)" ladder, either printed meaning: a menu, claim one.'),
        ('ii', 'Allele.', pt(S('Alternative form of a gene'), 7), 'allele', ''),
        ('iii', 'Genotype.', pt(S('Genetic makeup (of organism)'), 7), 'genotype', '')]
] + [
    T(f'10bi-{x.lower()}', 'Q10(b)(i)', 'C', ask(8, 'Name the bases at positions X and Y in the diagram.'),
      [pt(cell(BASES, i, BASES_CUTS), 5)], 'bio-1-2', concept, at(9, '10.', '(b)', '(i)'), 5, stem=[Q10B],
      fig='q10-dna', item=(x.lower(), x), labels=bases_labels(x),
      decision=EACH_ITEM + ' "(2 pts)" over the two positions.')
    for i, (x, concept) in enumerate([('X', 'base-pairing-thymine'), ('Y', 'base-pairing-cytosine')])
] + [
    T(f'10b{r}', f'Q10(b)({r})', 'C', q, [row], topic, concept, at(9, '10.', '(b)', f'({r})'), total,
      decision=decision)
    for r, q, row, topic, concept, total, decision in [
        ('ii', ask(8, 'Where in a human cell would you expect to find most DNA?'),
         pt(S('Nucleus only – [accept chromosomes]', piece=1, psep=' – ['), 5,
            note_sel=S('Nucleus only – [accept chromosomes]', piece=[2, 1], psep=[' – [', ']'])), 'bio-1-2',
         'location-of-dna', 5, ''),
        ('iii', Q(8, 'Proteins are made in the ribosomes using a code from DNA. Name the molecule that',
                  'carries the DNA code to the ribosomes.'), pt(S('mRNA'), 5), 'bio-2-3', 'mrna', 5, ''),
        ('iv', ask(8, 'What is meant by DNA profiling?'),
         anyn(S('Treating a DNA sample/ revealing a pattern/ unique to', 'species or individual or compare with other pattern'),
              2, 5), 'bio-3-3', 'dna-profiling', 10,
         MENU.format(n='Two points', pts='2 pts', claim='two') + ' Cut at the scheme\'s own solidus.'),
        ('v', ask(8, 'In DNA profiling, what is used to cut the DNA strands into fragments?'), pt(S('Enzymes'), 5),
         'bio-3-3', 'enzymes-in-dna-profiling', 5, ''),
        ('vi', ask(8, 'Give two applications of DNA profiling.'),
         anyn(eg('e.g. forensics/ paternity or maternity testing'), 2, 5, open_list=True), 'bio-3-3',
         'applications-of-dna-profiling', 10, MENU.format(n='Two points', pts='2 pts', claim='two')
         + ' Cut after the scheme\'s own "e.g.".')]
] + [
    T('10c', 'Q10(c)', 'C', Q10C[1],
      [pt(S('Punnett square or other scheme shown'), 6, kind='criterion', note=NO_ANSWER),
       pt(S('Cross completed correctly'), 6, kind='criterion', note=NO_ANSWER)],
      'bio-1-4', 'sex-determination-cross', at(9, '10.', '(c)'), 12, stem=[Q10C[0]],
      decision='The scheme prices the cross itself at two points priced under (c) before its romans ("Punnett '
               'square or other scheme shown" and "Cross completed correctly", "(1 pt)" each): one card for the '
               'printed ask they answer, a criterion row each, at the "2(6) + 6(2)" ladder\'s first rate.'),
] + [
    T(f'10c{r}', f'Q10(c)({r})', 'C', ask(8, q), rows, 'bio-1-4', concept, at(9, '10.', '(c)', f'({r})'),
      6 * len(rows), stem=Q10C + [Q10C_GIVE], decision=decision)
    for r, q, rows, concept, decision in [
        ('i', 'The genotypes and matching phenotypes of the parents.',
         [pt(S('XX = Female/ XY = Male', piece=n), 6) for n in (1, 2)], 'parents-sex-chromosomes',
         TWO_POINTS + ' Cut at the scheme\'s own solidus, one parent each.'),
        ('ii', 'The possible genotypes of the gametes that can be produced by each parent.',
         [pt(S(GAMETES, piece=1, psep=' / '), 6),
          pt(S(GAMETES, piece=[2, 1], psep=[' / ', ' and ']), 6),
          pt(S(GAMETES, piece=[2, 2], psep=[' / ', ' and ']), 6, label=S(GAMETES, piece=[2, 1], psep=[' / ', ' → ']))],
         'gametes-and-sex', 'Three points ("(3 pts)"), one per gamete: the scheme prints "Female gametes → X / Male '
                            'gametes → X and Y", cut at its own solidus and "and", the last row labelled with the '
                            'scheme\'s own "Male gametes".'),
        ('iii', 'The genotypes of the offspring.', [pt(S('XX and XY'), 6)], 'offspring-sex-chromosomes',
         'One point ("(1 pt)") for the printed offspring genotypes, read whole.')]
] + [
    T(f'11a{r}', f'Q11(a)({r})', 'C', [Q11A, ask(9, term, br=True)], [pt(S(ans), 7)], 'bio-3-1', concept,
      at(10, '11. (a)', f'({r})'), 7)
    for r, term, ans, concept in [
        ('i', 'Producer.', 'Organism that makes its own food', 'producer'),
        ('ii', 'Niche.', 'Role or', 'niche'),
        ('iii', 'Habitat.', 'Where an organism lives', 'habitat')]
] + [
    T(f'11b{r}', f'Q11(b)({r})', 'C', ask(9, q), [row], 'bio-3-1', concept, at(10, '11. (a)', '(b)', f'({r})'), 5,
      stem=Q11B, decision=decision)
    for r, q, row, concept, decision in [
        ('i', 'Name one greenhouse gas.', anyn(S('Carbon dioxide/ methane/ water vapour'), 1, 5), 'greenhouse-gases',
         'One point ("(1 pt)"), any one of the printed gases: a menu, claim one.'),
        ('ii', 'Why are greenhouse gases so called?', pt(S('They traps some of sun'), 5), 'greenhouse-effect',
         'The scheme\'s "They traps" is lifted as printed.'),
        ('iii', 'What is meant by the term pollution?', pt(S('Any harmful addition to the environment'), 5),
         'pollution', ''),
        ('iv', 'Suggest one way to reduce the levels of greenhouse gases in the air.',
         anyn(eg('e.g. More trees/ fewer cattle/ burn less fossil fuel'), 1, 5, open_list=True),
         'reducing-greenhouse-gases', 'One point ("(1 pt)"), any one of the scheme\'s examples: a menu, claim one.')]
] + [
    T(f'11bv-{x.lower()}', 'Q11(b)(v)', 'C', Q11BV, [pt(S(line, piece=k, psep=';'), 5, note_sel=SEQUENCES)],
      'bio-3-2', concept, at(10, '11. (a)', '(b)', '(v)'), 5, fig='q11-carbon', item=(x.lower(), x),
      labels=carbon_labels(x),
      decision=EACH_ITEM + ' Five points ("(5 pts)"), one per letter, cut at the scheme\'s own semicolons; its '
                           'bracketed direction on unmatched sequences is the row\'s note.')
    for x, line, k, concept in [(x, line, k, c) for (x, line, k), c in zip(CARBON, [
        'decay-in-the-carbon-cycle', 'photosynthesis-in-the-carbon-cycle', 'combustion-in-the-carbon-cycle',
        'feeding-in-the-carbon-cycle', 'respiration-in-the-carbon-cycle'])]
] + [
    T('11ci', 'Q11(c)(i)', 'C', ask(9, 'State any two types of pollution associated with waste disposal.'),
      [anyn(eg('e.g. air pollution/ water pollution/ ground pollution'), 2, 6, open_list=True)], 'bio-3-1',
      'pollution-from-waste', at(10, '11. (a)', '(c)', '(i)'), 12, stem=[Q11C],
      decision=MENU.format(n='Two points', pts='2 pts', claim='two') + ' Cut after the scheme\'s own "e.g.".'),
    T('11cii1', 'Q11(c)(ii)1', 'C', Q11CII1,
      [pt(S('1. Example of waste', piece=2, psep='1. '), 6, kind='criterion', note=NO_ANSWER)], 'bio-3-1',
      'waste-example', at(10, '11. (a)', '(c)', '(ii)'), 6, stem=[Q11C],
      decision=EACH_ITEM + ' Each numbered item a point ("(2 pts)" over the two); the scheme prints what earns '
                           'each, cut after its own number.'),
    T('11cii2', 'Q11(c)(ii)2', 'C', ask(9, '2. State how the named waste is managed.'),
      [pt(S('2. How waste is managed', piece=2, psep='2. '), 6, kind='criterion', note=NO_ANSWER)], 'bio-3-1',
      'waste-management', at(10, '11. (a)', '(c)', '(ii)'), 6, stem=[Q11C, M('(ii)', 9), Q11CII1],
      decision=EACH_ITEM + ' Each numbered item a point ("(2 pts)" over the two); the scheme prints what earns '
                           'each, cut after its own number.'),
    T('11ciii', 'Q11(c)(iii)', 'C', ask(9, 'Give three ways to minimise waste.'),
      [anyn(S(MINIMISE, piece=[2, 1], psep=['e.g. ', ' [']), 3, 6, open_list=True,
            note_sel=S(MINIMISE, piece=[2, 1], psep=[' [', ']']))], 'bio-3-1', 'minimising-waste',
      at(10, '11. (a)', '(c)', '(iii)'), 18, stem=[Q11C],
      decision='Three points ("(3 pts)") from the scheme\'s examples: one menu, claim three, cut after its own '
               '"e.g."; its bracketed direction is the row\'s note.'),
    T('11civ', 'Q11(c)(iv)', 'C', ask(9, 'Give one example of the use of micro-organisms in waste management.'),
      [pt(S('e.g. to consume waste e.g. sewage breakdown'), 6)], 'bio-3-1', 'microorganisms-in-waste-management',
      at(10, '11. (a)', '(c)', '(iv)'), 6, stem=[Q11C]),
] + [
    T('12ai', 'Q12(a)(i)', 'C', ask(10, 'Explain the term secondary sexual characteristics.'),
      [pt(S('Features that develop at or after puberty (but are not', 'directly involved in reproduction)'), 7)],
      'bio-2-5', 'secondary-sexual-characteristics', at(11, '12. (a)', '(i)'), 7),
    T('12aii', 'Q12(a)(ii)', 'C', ask(10, 'Give two examples of secondary sexual characteristics in males.'),
      [anyn(S('Facial hair/ broader shoulders/ larger larynx or deeper', 'hair/ enlargement of genitals'), 2, 7)],
      'bio-2-5', 'male-secondary-sexual-characteristics', at(11, '12. (a)', '(ii)'), 14,
      decision='Two points ("(2 pts)") of the "7 + 2(1)" ladder from the printed list: one menu, claim two, each '
               'response at the ladder\'s first rate.'),
    T('12bi', 'Q12(b)(i)', 'C', ask(10, 'Give two functions of the placenta.'),
      [anyn(S('Makes progesterone/ conducts food to embryo (foetus)/', 'blood apart.'), 2, 5)], 'bio-2-5',
      'functions-of-the-placenta', at(11, '12. (a)', '(b)', '(i)'), 10, stem=[Q12B], fig='q12-foetus',
      decision=MENU.format(n='Two points', pts='2 pts', claim='two')),
    T('12bii', 'Q12(b)(ii)', 'C', ask(10, 'Give the three stages of childbirth.'),
      [pt(S('1. Contraction of uterus or waters break or dilation of', 'cervix [accept labour]', piece=1, psep=' ['), 5,
          note_sel=S('1. Contraction of uterus or waters break or dilation of', 'cervix [accept labour]',
                     piece=[2, 1], psep=[' [', ']'])),
       pt(S('2. Baby delivered'), 5), pt(S('3. Afterbirth delivered'), 5)], 'bio-2-5', 'stages-of-childbirth',
      at(11, '12. (a)', '(b)', '(ii)'), 15,
      decision='Three points ("(3 pts)"), one per stage, each printed on its own numbered line: a row each; the first '
               'stage\'s bracketed direction is its note.'),
    T('12biii', 'Q12(b)(iii)', 'C', ask(10, 'Many babies are breast fed after birth. Give two biological benefits of breastfeeding.'),
      [anyn(None, 2, 5, options=[S(*BABY, piece=k) for k in range(1, 7)] + [S(*MOTHER, piece=k) for k in range(1, 5)])],
      'bio-2-5', 'benefits-of-breastfeeding', at(11, '12. (a)', '(b)', '(iii)'), 10,
      decision='Two points ("(2 pts)") from the scheme\'s two printed lists, "Benefit for baby:" and "Benefit for '
               'mother:": one menu, claim two, each option a slice of its list at the scheme\'s own solidus (the '
               'first option of each list keeps its printed heading).'),
    T('12biv', 'Q12(b)(iv)', 'C', ask(10, 'What is meant by the term infertility?'),
      [pt(S('Inability to produce offspring'), 5)], 'bio-2-5', 'infertility', at(11, '12. (a)', '(b)', '(iv)'), 5),
    T('12bv', 'Q12(b)(v)', 'C', Q(10, 'In vitro fertilisation is a method used to treat infertility.',
                                   'What is meant by in vitro fertilisation?'),
      [pt(S('Fusion of gametes [accept fertilisation] outside the body', '(e.g. in a Petri dish)'), 5)], 'bio-2-5',
      'in-vitro-fertilisation', at(11, '12. (a)', '(b)', '(v)'), 5,
      decision='The scheme sets its bracketed direction inside the answer ("Fusion of gametes [accept fertilisation] '
               'outside the body"): the printed answer is one row, read whole.'),
] + [
    T(f'12c{r}', f'Q12(c)({r})', 'C', ask(10, q), [row], 'bio-2-5', concept, at(11, '12. (a)', '(c)', f'({r})'),
      total, stem=[Q12C], fig='q12-cycle', decision=decision)
    for r, q, row, concept, total, decision in [
        ('i', 'What happens in the womb during menstruation (days 1 – 5)?',
         anyn(S('Loss of blood/ loss of endometrium'), 1, 6), 'menstruation', 6,
         'One point ("(1 pt)"), either printed answer: a menu, claim one.'),
        ('ii', 'Explain the term ovulation.', pt(S('Release of egg (from ovary)'), 6), 'ovulation', 6, ''),
        ('iii', 'What is meant by the fertile period?',
         anyn(S('(Time) when fertilisation is possible [accept “when you can', 'get pregnant”] / when egg is in oviduct'),
              1, 6), 'fertile-period', 6,
         'One point ("(1 pt)"), either printed answer at the scheme\'s own solidus (the first with its bracketed '
         'direction): a menu, claim one.'),
        ('iv', 'Where does fertilisation occur in the female body?', pt(S('Oviducts'), 6), 'site-of-fertilisation', 6,
         ''),
        ('v', 'Explain the term implantation.', pt(S('Embedding of embryo in endometrium'), 6), 'implantation', 6, ''),
        ('vi', 'Name two female hormones that have a role in the menstrual cycle.',
         anyn(S('Oestrogen/ progesterone/ FSH/ LH'), 2, 6), 'menstrual-hormones', 12,
         MENU.format(n='Two points', pts='2 pts', claim='two')),
        ('vii', 'What happens to the menstrual cycle when a woman reaches the menopause?', pt(S('It stops'), 6),
         'menopause', 6, '')]
] + [
    T('13ai', 'Q13(a)(i)', 'C', ask(11, 'Draw a labelled diagram of an animal cell as seen using a light microscope.'),
      [pt(S('Diagram - three labels', piece=1, psep=' - '), 3, kind='criterion', note=NO_ANSWER),
       pt(S('Diagram - three labels', piece=2, psep=' - '), 3, kind='criterion', units=[1, 1, 1], note=NO_ANSWER)],
      'bio-1-3', 'drawing-an-animal-cell', at(12, '13.', '(a)', '(i)'), 6,
      decision='The scheme prices the drawing "Diagram - three labels" at "3,0 + 3(1)": the diagram (3 or 0) and the '
               'three labels at 1 each, a criterion row each, cut at the scheme\'s own dash. The (a) heading "3(3)" '
               'counts the labels\' 3(1) as one of its three 3s.'),
    T('13aii', 'Q13(a)(ii)', 'C', ask(11, 'Name another type of microscope that gives greater detail than a light microscope.'),
      [pt(S('Electron microscope'), 3)], 'bio-1-3', 'electron-microscope', at(12, '13.', '(a)', '(ii)'), 3),
    T('13bi', 'Q13(b)(i)', 'C', ask(11, 'Give two functions of the cell membrane.'),
      [anyn(S('Holds cell together/ selectively permeable/ displays antigens'), 2, 5)], 'bio-1-3',
      'functions-of-the-cell-membrane', at(12, '13.', '(b)', '(i)'), 10, stem=[Q13B], fig='q13-membrane',
      decision=MENU.format(n='Two points', pts='2(pts)', claim='two')),
] + [
    T(f'13bii-{x.lower()}', 'Q13(b)(ii)', 'C', ask(11, 'Name the parts labelled A and B.'),
      [pt(S(*MEMBRANE, piece=[1, k], psep=[' *', ' / ']), 5, note_sel=S(*MEMBRANE, piece=2, psep=' *'),
          note_lead=STRUCK)],
      'bio-1-3', concept, at(12, '13.', '(b)', '(ii)'), 5, stem=[Q13B], fig='q13-membrane', item=(x.lower(), x),
      labels=membrane_labels(x),
      decision='The scheme prints "A = Lipid / B = Protein" struck through, beside "*7 marks to be allocated here as '
               'long as any part of 13 (b) attempted" and "7 marks [i.e. one 5+one 2]" (scheme p12, rendered and '
               'looked at). Carded as printed under Alex\'s rule that a printed ask is never left out (as 2019 Higher '
               'Q7(b)(iii)-(iv)): one card per label, at its place on the "3(5) + 6(2)" ladder, cut at the scheme\'s '
               'own solidus; the struck answer is the row and the footnote its note.')
    for k, x, concept in [(1, 'A', 'membrane-lipid'), (2, 'B', 'membrane-protein')]
] + [
    T(f'13b{r}', f'Q13(b)({r})', 'C', ask(11, q), [row], topic, concept, at(12, '13.', '(b)', f'({r})'), total,
      decision=decision)
    for r, q, row, topic, concept, total, decision in [
        ('iii', 'Which organelle is known as “the powerhouse of the cell”?', pt(S('Mitochondrion'), 5), 'bio-1-3',
         'mitochondrion', 5, ''),
        ('iv', 'Why does the nucleus of a cell have many pores?',
         pt(S('To allow passage of materials – [accept (to make it)', 'permeable]', piece=1, psep=' – ['), 5,
            note_sel=S('To allow passage of materials – [accept (to make it)', 'permeable]', piece=[2, 1],
                       psep=[' – [', ']'])), 'bio-1-3', 'nuclear-pores', 5, ''),
        ('v', 'List two differences between a plant cell and an animal cell.',
         anyn(S('Plant cells have a wall/ large vacuole/ chloroplast'), 2, 5), 'bio-1-3', 'plant-and-animal-cells', 10,
         MENU.format(n='Two points', pts='2 pts', claim='two')),
        ('vi', 'What is the primary source of energy for plant cells?', anyn(S('Sun/ light'), 1, 5), 'bio-2-2',
         'energy-source-for-plants', 5, 'One point ("(1 pt)"), either printed word: a menu, claim one.')]
] + [
    T(f'13c{r}', f'Q13(c)({r})', 'C', q, rows, 'bio-2-2', concept, at(12, '13.', '(c)', f'({r})'), total, stem=[Q13C],
      decision=decision)
    for r, q, rows, concept, total, decision in [
        ('i', ask(11, 'Explain what is meant by anaerobic respiration.'),
         [pt(S('Energy release (from food)/ without oxygen', piece=n), 3) for n in (1, 2)], 'anaerobic-respiration', 6,
         TWO_POINTS + ' Cut at the scheme\'s own solidus.'),
        ('ii', ask(11, 'Where in the cell does anaerobic respiration occur?'), [pt(S('Cytoplasm'), 3)],
         'site-of-anaerobic-respiration', 3, ''),
        ('iii', Q(11, 'Describe, with the aid of a diagram, how you kept the yeast under anaerobic conditions during the',
                  'investigation.'),
         [pt(S(*FERMENTER, piece=[1, 1], psep=[' [', ' and ']), 3, kind='criterion', note=NO_ANSWER),
          anyn(S(*FERMENTER, piece=[2, 1, 2], psep=[' [', ']', ': ']), 1, 3, sep=';',
               note_sel=S(*FERMENTER, piece=[2, 1, 1], psep=[' [', ']', ': ']))],
         'keeping-yeast-anaerobic', 6,
         'The scheme prices "Diagram and one label" at "3,0 + 3": the diagram (3 or 0) a criterion row, and the label '
         'a menu, claim one, of the labels its bracketed direction names as the only acceptable ones, cut at its own '
         'semicolons.'),
        ('iv', ask(11, 'Name the two substances produced by the yeast in the process of fermentation.'),
         [pt(S('Ethanol or alcohol/ carbon dioxide (CO2)', piece=n), 3) for n in (1, 2)], 'products-of-fermentation', 6,
         TWO_POINTS + ' Cut at the scheme\'s own solidus.'),
        ('v', ask(11, 'How did you know that fermentation had ceased?'), [pt(S('Bubbling stopped'), 3)],
         'end-of-fermentation', 3, '')]
] + [
    # ------------------------------------------------------------ Q14 --------
    T(f'14ai-{x.lower()}', 'Q14(a)(i)', 'C', ask(12, 'Name the parts labelled A, B and C.'),
      [pt(S(JOINT, piece=k), 3)], 'bio-2-4', concept, at(13, '14. (a)', '(i)'), 3, stem=[Q14A], fig='q14-joint',
      item=(x.lower(), x), labels=joint_labels(x), decision=EACH_ITEM + ' "(3 pts)" over the three labels.')
    for k, x, concept in [(1, 'A', 'ligament'), (2, 'B', 'cartilage'), (3, 'C', 'synovial-fluid')]
] + [
    T('14aii', 'Q14(a)(ii)', 'C', ask(12, 'Give two functions of the human skeleton.'),
      [anyn(S('Strength/ support/ shape / mobility/ protection/ muscle', 'attachment [accept blood cell production]',
              piece=1, psep=' ['), 2, 3,
            note_sel=S('Strength/ support/ shape / mobility/ protection/ muscle',
                       'attachment [accept blood cell production]', piece=[2, 1], psep=[' [', ']']))],
      'bio-2-4', 'functions-of-the-skeleton', at(13, '14. (a)', '(ii)'), 6,
      decision=MENU.format(n='Two points', pts='2 pts', claim='two') + ' Its bracketed direction is the row\'s note.'),
    T('14aiii', 'Q14(a)(iii)', 'C', Q(12, 'Vertebrae in the neck are called the cervical vertebrae.',
                                       'Name and give the exact location of two other types of vertebrae.'),
      [anyn(None, 2, 3, options=[S(*VERTEBRAE, piece=[k, 1], psep=['/', ' - ']) for k in range(1, 5)],
            note_sel=S('Any two pairs')),
       anyn(None, 2, 3, options=[S(*VERTEBRAE, piece=[k, 2], psep=['/', ' - ']) for k in range(1, 5)],
            note='Listed in the same order as the types: each location belongs to the type printed in the same place.')],
      'bio-2-4', 'types-of-vertebrae', at(13, '14. (a)', '(iii)'), 12,
      decision='Four points ("(4 pts)", "Any two pairs"): two types and the location of each. The scheme prints four '
               'type - location pairs at its own solidus; each pair is cut at its own " - " into a menu of types and a '
               'menu of locations, claim two of each at 3, as 2026 Higher Q15(c)(iv) carries its layers and matching '
               'structures.'),
    T('14aiv', 'Q14(a)(iv)', 'C', ask(12, 'Name one disorder of the musculoskeletal system.'),
      [anyn(eg('e.g. arthritis/ osteoporosis'), 1, 3, open_list=True)], 'bio-2-4', 'musculoskeletal-disorders',
      at(13, '14. (a)', '(iv)'), 3, decision='One point ("(1 pt)"), any one of the scheme\'s examples: a menu, claim one.'),
] + [
    T(f'14b{r}', f'Q14(b)({roman}){n}', 'C', q, [row], 'bio-2-6', concept, at(13, '14. (b)', f'({roman})'), 3,
      stem=stem,
      decision=decision)
    for r, roman, n, q, row, concept, stem, decision in [
        ('i', 'i', '', Q(12, 'Blood is made up of plasma and blood cells. What is plasma?'),
         pt(S('Liquid (part of blood)'), 3), 'plasma', [], ''),
        ('ii', 'ii', '', Q(12, 'What is the function of white blood cells?'), pt(S('Fight disease'), 3),
         'white-blood-cells', [], ''),
        ('iii', 'iii', '', ask(12, 'Where in the body are white blood cells produced?'), pt(S('e.g. bone (marrow)'), 3),
         'where-white-blood-cells-are-made', [], ''),
        ('iv', 'iv', '', Q(12, 'Some people may have the blood group B Positive (B+).',
                         'What factor is present in their blood that makes it positive?'), pt(S('Rhesus'), 3),
         'rhesus-factor', [], ''),
        ('v1', 'v', '1', Q14BV1, pt(S(HEART, piece=[1, 2], psep=['/', '1. ']), 3), 'pacemaker', [Q14BV],
         EACH_ITEM + ' Each numbered item a point ("(2 pts)" over the two), cut after the scheme\'s own number.'),
        ('v2', 'v', '2', ask(12, '2. Where is this structure located in the heart?'),
         pt(S(HEART, piece=[2, 2], psep=['/', '2. ']), 3), 'location-of-the-pacemaker', [Q14BV, Q14BV1],
         EACH_ITEM + ' Each numbered item a point ("(2 pts)" over the two), cut after the scheme\'s own number.'),
        ('vi', 'vi', '', Q(12, 'What causes the sound of a heartbeat?'), pt(S('Valves closing'), 3), 'heart-sounds', [],
         ''),
        ('vii', 'vii', '', ask(12, 'Name the blood vessels that supply the heart cells with blood.'),
         pt(S('Coronary [accept cardiac] arteries'), 3), 'coronary-arteries', [],
         'The scheme sets its bracketed direction inside the answer: the printed answer is one row, read whole.')]
] + [
    T('14bviii', 'Q14(b)(viii)', 'C', ask(12, 'Mention two ways to maintain a healthy heart.'),
      [anyn(eg('e.g. eat less fat/ exercise regularly/ avoid excess stress/ eat', 'smoke'), 2, 3, open_list=True)],
      'bio-2-6', 'healthy-heart', at(13, '14. (b)', '(viii)'), 6,
      decision=MENU.format(n='Two points', pts='2 pts', claim='two') + ' Cut after the scheme\'s own "e.g.".'),
] + [
    T(f'14ci-{x.lower()}', 'Q14(c)(i)', 'C', ask(12, 'Name the parts labelled A and B.'), [pt(S(EAR, piece=k), 3)],
      'bio-2-4', concept, at(13, '14. (c)', '(i)'), 3, stem=[Q14C], fig='q14-ear', item=(x.lower(), x),
      labels=ear_labels(x), decision=EACH_ITEM + ' "(2 pts)" over the two labels, cut at the scheme\'s own solidus.')
    for k, x, concept in [(1, 'A', 'semicircular-canals'), (2, 'B', 'cochlea')]
] + [
    T(f'14c{r}', f'Q14(c)({r})', 'C', ask(12, q) if one_line else Q(12, *q), rows, 'bio-2-4', concept,
      at(13, '14. (c)', f'({r})'), 6 if r in ('vi', 'vii') else 3, stem=[Q14C] if fig else [],
      fig='q14-ear' if fig else None, labels=ear_labels() if r in ('ii', 'iii') else None, decision=decision)
    for r, q, one_line, rows, concept, fig, decision in [
        ('ii', 'What is the function of part A?', True, [pt(S('Balance'), 3)], 'function-of-semicircular-canals', True,
         ''),
        ('iii', 'What is the function of part B?', True, [pt(S('Hearing'), 3)], 'function-of-the-cochlea', True, ''),
        ('iv', 'What is connected to the middle ear by the Eustachian tube?', True, [pt(S('Throat'), 3)],
         'eustachian-tube', True, ''),
        ('v', 'What surrounds the bones in the middle ear?', True, [pt(S('Air'), 3)], 'middle-ear', True, ''),
        ('vi', ('The ear is an example of a sense organ.',
                'Name two sense organs, other than the ear and the eye, in the human body.'), False,
         [anyn(S('Skin/ tongue/ nose'), 2, 3)], 'sense-organs', False,
         MENU.format(n='Two points', pts='2 pts', claim='two')),
        ('vii', ('Name one disorder of the ear or of the eye and give a corrective measure for the',
                 'disorder referred to.'), False,
         [pt(S('Disorder/ Corrective measure', piece=n), 3, kind='criterion', note=NO_ANSWER) for n in (1, 2)],
         'eye-or-ear-disorder', False,
         TWO_POINTS + ' The scheme prints "Disorder/ Corrective measure": cut at its own solidus, a criterion row '
                      'each.')]
] + [
    # ------------------------------------------------------------ Q15 --------
    T(f'15ai-{x.lower()}', 'Q15(a)(i)', 'C', ask(13, 'Name the parts labelled A, B, C and D.'),
      [pt(S(FLOWER, piece=k), 3)], 'bio-2-5', concept, at(14, '15.', '(a)', '(i)'), 3, stem=[Q15A], fig='q15-flower',
      item=(x.lower(), x), labels=flower_labels(x), decision=EACH_ITEM + ' "(4 pts)" over the four labels.')
    for k, x, concept in [(1, 'A', 'stigma'), (2, 'B', 'anther'), (3, 'C', 'ovary'), (4, 'D', 'sepal')]
] + [
    T(f'15a{r}', f'Q15(a)({r})', 'C', ask(13, q), rows, 'bio-2-5', concept, at(14, '15.', '(a)', f'({r})'), total,
      decision=decision)
    for r, q, rows, concept, total, decision in [
        ('ii', 'What is meant by the term pollination?',
         [pt(S('Transfer of pollen/ (from anther) to stigma', piece=n), 3) for n in (1, 2)], 'pollination', 6,
         TWO_POINTS + ' Cut at the scheme\'s own solidus.'),
        ('iii', 'Give two methods of pollination in plants.', [anyn(S('Wind/ insect/ other animal/ self'), 2, 3)],
         'methods-of-pollination', 6, MENU.format(n='Two points', pts='2 pts', claim='two')),
        ('iv', 'What is the next step after pollination in the lifecycle of the plant?', [pt(S('Fertilisation'), 3)],
         'fertilisation-follows-pollination', 3, ''),
        ('v', 'Suggest a substance that flowers produce that may cause hay fever in some people.',
         [pt(S('Pollen'), 3)], 'pollen-and-hay-fever', 3, '')]
] + [
    T('15bi', 'Q15(b)(i)', 'C', ask(13, 'What is meant by the term vegetative propagation?'),
      [pt(S('Asexual / reproduction', piece=n), 3) for n in (1, 2)], 'bio-2-5', 'vegetative-propagation',
      at(14, '15.', '(b)', '(i)'), 6, decision=TWO_POINTS + ' Cut at the scheme\'s own solidus.'),
    T('15bii', 'Q15(b)(ii)', 'C', Q(13, 'Give one example of vegetative propagation in plants and state whether it involve a stem, a',
                                     'root, a leaf or a bud.'),
      [pt(S('One example/ whether stem-root-leaf-bud', piece=n), 3, kind='criterion', note=NO_ANSWER) for n in (1, 2)],
      'bio-2-5', 'example-of-vegetative-propagation', at(14, '15.', '(b)', '(ii)'), 6,
      decision=TWO_POINTS + ' The scheme prints "One example/ whether stem-root-leaf-bud": cut at its own solidus, a '
                            'criterion row each. The paper\'s "whether it involve" is lifted as printed.'),
    T('15biii', 'Q15(b)(iii)', 'C', ask(13, 'State two ways that vegetative propagation differs from reproduction by seed.'),
      [anyn(S('Spread/ limited spread/ offspring all susceptible to same', 'diseases'), 2, 3)], 'bio-2-5',
      'vegetative-propagation-and-seeds', at(14, '15.', '(b)', '(iii)'), 6,
      decision=MENU.format(n='Two points', pts='2 pts', claim='two') + ' Cut at the scheme\'s own solidus.'),
    T('15biv', 'Q15(b)(iv)', 'C', Q(13, 'Artificial propagation is widely used in horticulture. Give two example of artificial propagation',
                                     'carried out by gardeners or horticulturists.'),
      [anyn(eg('e.g. Cuttings/ layering/ budding/ grafting'), 2, 3, open_list=True)], 'bio-2-5',
      'artificial-propagation', at(14, '15.', '(b)', '(iv)'), 6,
      decision=MENU.format(n='Two points', pts='2 pts', claim='two') + ' Cut after the scheme\'s own "e.g.". The '
                                                                     'paper\'s "two example" is lifted as printed.'),
    T('15bv', 'Q15(b)(v)', 'C', ask(13, 'Give one advantage and one disadvantage of artificial propagation.'),
      [pt(S('Advantage: e.g. can control production of desirable', 'features'), 3),
       pt(S('Disadvantage: e.g. offspring all susceptilble to same', 'diseases'), 3)], 'bio-2-5',
      'artificial-propagation-pros-and-cons', at(14, '15.', '(b)', '(v)'), 6,
      decision='An advantage and a disadvantage, a point each ("(2 pts)"), each printed under its own label: a row '
               'each. The scheme\'s "susceptilble" is lifted as printed.'),
] + [
    T(f'15ci-{x.lower()}', 'Q15(c)(i)', 'C', ask(13, 'Name the tissues A and B.'), [pt(S(f'{x} = {name}'), 3)],
      'bio-2-6', concept, at(14, '15.', '(c)', '(i)'), 3, stem=[Q15C], fig='q15-vascular', item=(x.lower(), x),
      labels=tissue_labels(x), decision=EACH_ITEM + ' "(2 pts)" over the two tissues, each on its own line.')
    for x, name, concept in [('A', 'Xylem', 'xylem'), ('B', 'Phloem', 'phloem')]
] + [
    T(f'15c{r}', f'Q15(c)({r})', 'C', ask(13, q), [row], 'bio-2-6', concept, at(14, '15.', '(c)', f'({r})'), total,
      stem=[Q15C] if fig else [], fig='q15-vascular' if fig else None, labels=tissue_labels() if fig else None,
      decision=decision)
    for r, q, row, concept, total, fig, decision in [
        ('ii', 'Which of the above tissues transports water from the roots?', pt(S('A or Xylem'), 3),
         'xylem-carries-water', 3, True, ''),
        ('iii', 'Which of the above tissues transports food from the leaves?', pt(S('B or Phloem'), 3),
         'phloem-carries-food', 3, True, ''),
        ('iv', 'Is tissue A living or dead?', pt(S('Dead'), 3), 'xylem-is-dead', 3, True, ''),
        ('v', 'Suggest a role of the lignin in tissue A.', pt(S('Support'), 3), 'lignin', 3, True, ''),
        ('vi', 'Name one process that causes water to move upwards through a plant.',
         anyn(eg('e.g. root pressure/ cohesion/ adhesion/ transpiration', 'stream'), 1, 3, open_list=True),
         'water-movement-in-plants', 3, False,
         'One point ("(1 pt)"), any one of the scheme\'s examples: a menu, claim one.'),
        ('vii', 'Name the structures in the leaves through which water exits the plant.', pt(S('Stomata'), 3),
         'stomata', 3, False, ''),
        ('viii', 'Vascular tissue is one type of plant tissue. Name two other plant tissues.',
         anyn(S('Ground/ epidermal/ meristematic'), 2, 3), 'plant-tissue-types', 6, False,
         MENU.format(n='Two points', pts='2 pts', claim='two'))]
]

FIGURES = {
    # key suffix: (doc, page, rect in PDF points, credit, letters, alt, solution)
    'q2-plant': ('paper', 2, (105, 430, 300, 582), SEC, ['A', 'B', 'C'], 'Drawing of a flowering plant: an upright main shoot with leaves and clusters of flowers at its top and on side branches, a dashed horizontal line across the plant near the middle, and a branching system below the line. A points to the upright main shoot above the dashed line, B to a leaf on a side branch at the right, C to the main axis just below the dashed line.', False),
    'q4-cycle': ('paper', 3, (150, 340, 350, 520), SEC, ['A', 'B'], 'A circle divided by two lines from its centre into a small wedge at the right, lettered A, and the rest of the circle, lettered B; a curved arrow drawn around the centre points clockwise.', False),
    'q5-table': ('paper', 4, (52, 25, 525, 262), SEC, [], 'Question 5 as printed: the instruction, then the list Amylase (struck through), Temperature, Substrate, Immobilised, Reusable, Protein above a two-column table. Column A lists "An example of an enzyme." (answered Amylase in Column B as the example) and parts (a) to (e); Column B is blank beside them.', False),
    'q6-kidney': ('paper', 4, (110, 330, 350, 452), SEC, ['A', 'B', 'C'], 'Vertical section through a kidney, shaded in greys: a pale outer band round the edge, a ring of darker cone-shaped segments inside it, a paler central space, blood vessels entering at the indented side on the left and a tube leaving downwards from there. A points to the pale outer band at the top, B to one of the dark cone-shaped segments, C to the tube leaving at the lower left.', False),
    'q7-apparatus': ('paper', 5, (75, 188, 485, 430), SEC, [], 'Apparatus as drawn: a bulb in a lamp holder, labelled strong light source, at the left end of a ruler labelled metre stick; near the far end of the ruler a beaker of water (labelled water) holding a thermometer and a test tube; in the test tube, in water, a plant with a cut stem (labels: cut stem, water, plant, thermometer). Beneath it the paper prints "Tick the factor you will refer to." beside a two-row table, Light intensity and CO2 concentration, each with an empty box.', False),
    'q9-quadrat': ('paper', 7, (410, 518, 531, 610), SEC, [], 'Photograph of a square frame of white strips laid flat on grass, divided by white strings into a grid of smaller squares.', False),
    'q10-dna': ('paper', 8, (130, 185, 340, 325), SEC, ['A', 'G', 'P', 'S', 'X', 'Y'], 'Diagram of a short section of DNA: two backbones of grey pentagons lettered S alternating with black circles lettered P, joined across by three pairs of boxed letters with dashed lines between each pair: A paired with X at the top, G with Y in the middle, and X with A at the bottom.', False),
    'q11-carbon': ('paper', 9, (55, 360, 462, 540), SEC, ['A', 'B', 'C', 'D', 'E'], 'Diagram of the carbon cycle drawn as broad grey arrows between labelled boxes: CO2 in atmosphere at the top, PLANTS at the right, ANIMALS in the middle, DECOMPOSERS at the left and FOSSIL FUELS at the bottom. Five empty boxes lettered A to E sit on the arrows: B on the arrow curving down from CO2 in atmosphere to PLANTS; D on the arrow from PLANTS to ANIMALS; E beside the arrows rising from ANIMALS and from PLANTS to CO2 in atmosphere; A on the arrow running from PLANTS round under ANIMALS to DECOMPOSERS; C on the broad arc that runs from FOSSIL FUELS round the left-hand side and over the top into CO2 in atmosphere, which an arrow rising from DECOMPOSERS joins. Two boxes are filled in: Death on the arrow from ANIMALS to DECOMPOSERS, and Changed to on the arrow from PLANTS down to FOSSIL FUELS.', False),
    'q12-foetus': ('paper', 10, (55, 95, 272, 252), SEC, [], 'Drawing of a foetus curled up head-down inside the womb, its umbilical cord coiled about it; a thick speckled layer on the inner wall of the womb at the left is labelled Placenta; the narrow neck of the womb is at the bottom.', False),
    'q12-cycle': ('paper', 10, (165, 374, 380, 588), SEC, [], 'Diagram of the menstrual cycle as a ring of 28 numbered day boxes round a circle labelled MENSTRUAL CYCLE. Days 1 to 5 are dotted and the shaded sector inside them is labelled Menstruation; arrows run clockwise round the inside. Inside the ring the diagram prints "Lining repairs and builds up again" after menstruation, a two-headed arrow labelled Fertile period across the lower days and "Implantation may happen" on the left; a line from day 14 is labelled Ovulation.', False),
    'q13-membrane': ('paper', 11, (145, 122, 368, 246), SEC, ['A', 'B'], 'Diagram of a section of cell membrane: two rows of small units, each a round head with a two-line tail, the heads facing out along the top and the bottom, with three large dotted oval bodies set among them, two of them running right through from top to bottom. B points to the top of the dotted oval body at the left; A points to the tail of one of those units at the upper right.', False),
    'q14-joint': ('paper', 12, (100, 80, 265, 203), SEC, ['A', 'B', 'C'], 'Section through a joint between the ends of two bones, each filled with a speckled spongy pattern, the joint enclosed on each side by a dotted layer. A points to the dotted layer at the left side of the joint, B to the dark band capping the end of the upper bone, C to the space between the two bone ends.', False),
    'q14-ear': ('paper', 12, (97, 460, 536, 652), SEC, ['A', 'B'], 'Drawing of the human ear in section, with printed labels Ear lobe (the outer ear flap at the left), Middle ear (pointing to the small bones in the middle), Eustachian tube (a tube running down from the middle ear) and Auditory nerve (nerve fibres at the right). A points to a set of looped tubes at the upper right; B points to the coiled, snail-shaped structure at the lower right.', False),
    'q15-flower': ('paper', 13, (145, 86, 320, 245), SEC, ['A', 'B', 'C', 'D'], 'Section through a flower: wide petals spreading out from a cup; inside it a long central stalk with a knob at its tip rises from a swollen base holding small round bodies, among several shorter stalks each topped by a small head; small leaf-like parts sit below the petals at the base. A points to the knob at the tip of the long central stalk, B to the head of one of the shorter stalks, C to the swollen base with the round bodies, D to a small leaf-like part at the base.', False),
    'q15-vascular': ('paper', 13, (95, 490, 450, 652), SEC, ['A', 'B'], 'Two drawings side by side, lettered A and B. A: two long tubes side by side, their walls strengthened with rings and spirals, labelled Lignin. B: a long tube with dotted cross-walls at its ends, labelled Sieve plate and Sieve tube, with a narrow cell beside it labelled Companion cell with dense cytoplasm.', False),
}
