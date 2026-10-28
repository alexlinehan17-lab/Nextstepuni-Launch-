"""Biology 2017 Ordinary Level — reviewed task ledger, carded from the paper for the first time.

Independent visual sweep (2026-10-25), every page rendered and read:
  * The 2017 paper is one booklet (M43), 16 pages: p1 cover and instructions,
    p2-p4 Section A Questions 1-6, p5-p7 Section B Questions 7-9, p8-p15
    Section C Questions 10-15, p16 "Blank Page". Sections A and B are
    answered on the paper; Section C in an answer book. No acknowledgements
    page: no figure carries a credit.
  * The marking scheme, 12 pages: p1 cover, p2 note, p3 introduction,
    cancelled and surplus answers, p4 surplus answers continued and the
    conventions, p5-p10 Questions 1-15 (one table, no page numbers), p11
    "Blank Page", p12 back cover.

The paper keeps the long-standing shape: any five of Section A's six
questions, any two of Section B's three, any four of Section C's six, and
Questions 14 and 15 are each any two of (a), (b), (c). Every printed ask is
carded. No Biology card existed for 2017 Ordinary before this review.

The scheme counts POINTS ("(1 pt)", "(3 pts)") and heads each question or
part with what they are worth. Q1-Q3 are "5(4)", a fixed 4 per point. Ordered
splits are carded at their first rate: Q4-Q6 "6(3) + 2" over seven points,
every Section B (a) "5 + 1", Q7(b) "2(6) + 6(2)" over eight, Q8(b)
"3(4) + 6(2)" over nine, and every Section C (a) "7 + 2(1)". Q9(b) prints
"6 + 3(2) + 4(3)" as its parts' own marks (the diagram "6,3,0", its labels
"3(2)", then (ii)-(v) a point each), so it is fixed, as are Section C (b)
"9(3)" and (c) "8(3)", every part of Q14 and Q15(a), (b) "10(3)", and Q15(c)
"3 + 6 + 3(2) + 5(3)" ((i), the lungs diagram "6, 3, 0", its labels "3(2)",
then five points at 3). A Section C (a) ladder sits beside its question's
fixed (b) and (c), so each such ladder names their units as fixed and their
cards are exempt from its notation.

The scheme mostly sets its compressed reprint of the ask on the answer's own
printed line ("Rhizopus kingdom: Fungi"); those tasks are anchored on the
part's own marker under its question (SQ path), as 2018 Ordinary does. Where
the reprint stands on a line of its own above the answer it is the pairing
anchor and is wording-checked. The text layer reads parts of five scheme pages
out of printed order (Q8(b)(v) and Q9(b)(iii)-(v) at the foot of p6, Q10(c)(iii)
and Q11(b)(iii) at the foot of p7, Q12(b)(i) and (c)(v) at the foot of p8,
Q14(b)(vii) and (c)(v) at the foot of p9, Q15(b)(ii)-(iii) and (c)(ii), (vi)
at the foot of p10); those answers are anchored on their own reprints, or
reached with `after=` from a line printed before them.

The census reader lost three things (paper.py, gated to this sitting): Question
2's key steps "3." and "4." read as question heads (MISPRINTS), Question 6
welded after Q5(g)'s circle options "T F", and Q7(b)(iii)'s marker welded to
the end of (ii)'s answer line (WELDED_HEADS). One printed choice is marked
differently per option: Q11(c)(iv)'s survey of the plant or the animal, each
with its own printed list, so each is a route card.
"""
from bio_review_lib import Q, SQ, S, M, pt, anyn, T, L, parse_ref

YEAR, LEVEL = 2017, 'ol'
REVIEWED_AT = '2026-10-25'

SOURCES = {
    'paper': {'path': 'examiner-reports/biology/papers/2017-ol-paper.pdf',
              'fileid': 'LC025GLP000EV.pdf',
              'sha256': 'f1f318b509edc95acba5fb11bb687145b4f9658cd71cd47661013b0c74d1cef3',
              'pages': 16},
    'scheme': {'path': 'examiner-reports/biology/schemes/2017-ol.pdf',
               'fileid': 'LC025GLP000EV.pdf',
               'sha256': 'c4719089bfe04eebdd2100e383820f99c74d1ea994cd88b25aa5a3d278b4c991',
               'pages': 12},
}

PAGE_ROLES = {
    'paper': {1: 'cover', **{p: 'questions' for p in range(2, 16)}, 16: 'blank'},
    'scheme': {1: 'cover', 2: 'note', 3: 'introduction', 4: 'conventions',
               **{p: 'marking' for p in range(5, 11)}, 11: 'blank', 12: 'back-cover'},
}


def _ladder(notation, **extra):
    """An ordered split as the scheme prints it ("6(3) + 2", "2(6) + 6(2)")."""
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
    (9, 'b'): 24,   # p5: "part (b) carries 24 marks"; priced part by part
    **{(n, x): t for n in range(10, 14) for x, t in (('b', 27), ('c', 24))},
    **{(n, x): 30 for n in (14, 15) for x in 'abc'},
}
LADDERS = {
    **{q: _ladder('6(3) + 2') for q in (4, 5, 6)},
    **{(n, 'a'): _ladder('5 + 1') for n in (7, 8, 9)},
    (7, 'b'): _ladder('2(6) + 6(2)'),
    (8, 'b'): _ladder('3(4) + 6(2)'),
    # Section C (a) "7 + 2(1)"; (b) "9(3)" and (c) "8(3)" are fixed points
    # beside it, named here so the question's total is the ladder's.
    **{(n, 'abc'): _ladder('7 + 2(1)', fixed={3: 17}) for n in range(10, 14)},
}

CHECKSUMS = {
    **{q: {4: 5} for q in (1, 2, 3)}, **{q: {3: 7} for q in (4, 5, 6)},
    **{(n, 'a'): {5: 2} for n in (7, 8, 9)}, (7, 'b'): {6: 8}, (8, 'b'): {4: 9},
    (9, 'b'): {6: 1, 2: 3, 3: 4},
    **{(n, 'a'): {7: 3} for n in range(10, 14)},
    **{(n, 'b'): {3: 9} for n in range(10, 14)},
    **{(n, 'c'): {3: 8} for n in range(10, 14)},
    **{(n, x): {3: 10} for n in (14, 15) for x in 'ab'}, (14, 'c'): {3: 10},
    (15, 'c'): {3: 6, 6: 1, 2: 3},
}

SCAN_PAGES = {'paper': range(1, 16)}
SELECTION_SCAN = [
    ('paper', 1, 'any five', 'Cover rubric, Section A: whole-question choice; every question is carded.'),
    ('paper', 1, 'any two', 'Cover rubric, Section B: whole-question choice; every question is carded.'),
    ('paper', 1, 'any four', 'Cover rubric, Section C: whole-question choice; every question is carded.'),
    ('paper', 2, 'any five', 'Section A rubric repeated.'),
    ('paper', 2, 'the following', 'Q1 lead-in: every part asked, one card per letter.'),
    ('paper', 2, 'the following', 'Q2 "Identify the following organisms": every organism of the key asked, one card '
                                  'per organism.'),
    ('paper', 3, 'choose', 'Q3 "Choose each term": every description matched, one card per lettered part.'),
    ('paper', 3, 'the following', 'Q3 list of terms: the options.'),
    ('paper', 4, 'the following', 'Q5 lead-in: every statement asked, one card per letter.'),
    ('paper', 4, 'or', 'Q5 "true (T) or false (F)": the answer options.'),
    ('paper', 4, 'or', 'Q5 "T or F": the answer options.'),
    ('paper', 5, 'any two', 'Section B rubric repeated.'),
    ('paper', 5, 'the following', 'Q7(b) lead-in: every part asked.'),
    ('paper', 5, 'the following', 'Q7(b)(v) "Which of the following diagrams": the two printed diagrams; one answer.'),
    ('paper', 5, 'or', 'Q7(b)(v) "A or B": the answer options.'),
    ('paper', 5, 'the following', 'Q7(b)(vi) "label the following tissues": both tissues asked, a row each.'),
    ('paper', 6, 'or', 'Q8(a)(ii) "more or less energy": the answer options.'),
    ('paper', 6, 'the following', 'Q8(b) lead-in: every part asked.'),
    ('paper', 7, 'the following', 'Q9(a) "Complete the following sentence": both blanks asked, a row each.'),
    ('paper', 7, 'the following', 'Q9(b) lead-in: every part asked.'),
    ('paper', 7, 'or', 'Q9(b)(v) "bacteria or fungi": description.'),
    ('paper', 8, 'any four', 'Section C rubric repeated.'),
    ('paper', 8, 'or', 'Q10(a)(iii) "the same as each other or different": the answer options.'),
    ('paper', 8, 'both', 'Q10(b)(ii) "Name both": both types asked, a row each.'),
    ('paper', 8, 'or', 'Q10(b)(vi) passage "one or more tissues": description.'),
    ('paper', 8, 'or', 'Q10(c) passage "chromosomes or genes": description.'),
    ('paper', 9, 'the following', 'Q11(c) lead-in: every part asked.'),
    ('paper', 9, 'either', 'Q11(c)(iv) "either the plant or the animal": the scheme prints a separate list for each, '
                           'so each is a route card.'),
    ('paper', 9, 'or', 'Q11(c)(iv) "the plant or the animal": the same choice; route cards.'),
    ('paper', 11, 'both', 'Q13(a) lead-in "both play a role": description.'),
    ('paper', 11, 'both', 'Q13(a)(ii) "Name both": both parts asked, a row each.'),
    ('paper', 11, 'or', 'Q13(b)(ii) "A to B to C OR from C to B to A": the answer options.'),
    ('paper', 12, 'any two', 'Q14 "any two of (a), (b), (c)": whole-part choice; every part is carded.'),
    ('paper', 12, 'the following', 'Q14(a)(ii) "each of the following processes": both processes asked, one card '
                                   'each.'),
    ('paper', 12, 'or', 'Q14(a)(ii) "catabolism or anabolism": the answer options.'),
    ('paper', 14, 'any two', 'Q15 "any two of (a), (b), (c)": whole-part choice; every part is carded.'),
    ('paper', 14, 'the following', 'Q15(b)(ii) "each of the following statements": every statement asked, one card '
                                   'each.'),
    ('paper', 15, 'or', 'Q15(c)(iv) "relaxing or contracting": the answer options.'),
]

ROUTES = {'Q11(c)(iv)': ['plant', 'animal']}

SEC = 'State Examinations Commission'
SAME_LINE = 'The scheme sets its reprint of the ask on the answer\'s own line: anchored on the part\'s marker.'
COMPRESSED = 'The scheme heads the answer with a compressed reprint of the ask.'
EACH_ITEM = 'A list the scheme prices entry by entry: one card per entry, each its own slice of the printed line.'
NO_ANSWER = 'The scheme prints no answer here, only what earns the marks.'
TWO_POINTS = 'The scheme prices this part at two points: each printed point its own row.'
MARKER_C = ('The scheme prints this part\'s marker "(c )", with a space, which the anchor check does not read as a '
            'marker; its answer shares its line with what heads it, so it is read from the line printed before it.')
OUT_OF_ORDER = ('The text layer reads this answer out of printed order, at the foot of the scheme page: anchored on '
                'its own reprint.')


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


def cell(line, i, cuts, page=None, meaning=False, after=None):
    """Cell i of a scheme line printed as cells ("A = Liver B = Stomach C = ..."), cut at the
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
    return S(line, page=page, piece=pieces, psep=seps, after=after)


def labels(line, letters, cuts, page, asked=None):
    return [L(x, cell(line, i, cuts, page=page, meaning=True), x == asked) for i, x in enumerate(letters)]


# ------------------------------------------------------------ question text --
Q1 = Q(2, 'Use your knowledge of nutrition to answer the following questions.')
Q2 = [Q(2, 'Identify the following organisms using the key given below.'),
      Q(2, 'Write the appropriate letter from the diagram after the identified organism in each case.')]
Q3 = Q(3, 'Choose each term from the following list and place it in Column B to match a description in',
       'Column A. The first one has been completed as an example.')
Q4 = Q(3, 'The diagram shows part of the human digestive system.')
Q5 = Q(4, 'Indicate whether the following statements are true (T) or false (F) by drawing a circle around',
       'T or F in each case.')
Q6 = Q(4, 'The diagram shows part of the organism Rhizopus.')
Q7B = Q(5, 'Answer the following questions in relation to how you prepared and examined with a',
        'microscope a transverse section (T.S.) of a dicotyledonous stem.')
Q8B = Q(6, 'Answer the following questions in relation to the production of alcohol by yeast.')
Q9B = Q(7, 'Answer the following in relation to an activity you carried out to demonstrate osmosis.')
Q10BD = Q(8, 'The diagram shows a cell undergoing cell division.')
Q10C = Q(8, 'Mutations are changes in the genetic material of a cell.', 'body cell.')
Q11B = Q(9, 'Over the years many new plant and animal species have spread to Ireland.',
         'examples of species not native to Ireland that have proved quite beneficial to us.')
Q11C = Q(9, 'Answer the following questions in relation to the ecosystem you have studied.')
Q11CII = Q(9, 'Name one plant and one animal from that ecosystem.')
Q12B = Q(10, 'The diagram shows the human female reproductive system.')
Q12CIII = Q(10, 'The hormones oxytocin and progesterone play a role in birth.')
Q13A = Q(11, 'The nervous system and the endocrine system both play a role in human responses.')
Q13B = Q(11, 'The diagram shows the nerve cells (neurons) in a reflex arc.')
Q13C = Q(11, 'The diagram shows the structure of the human brain.')
Q14AII = [Q(12, 'Catabolism and anabolism are the two main types of metabolism.'),
          Q(12, 'State whether each of the following processes is an example of catabolism or', 'anabolism:')]
Q14AVI = Q(12, 'Which type of respiration results in the production of acid in our muscles?')
Q14AVII = Q(12, 'What is the name of the acid produced in the muscles?')
Q14B = Q(12, 'The diagram shows a section through a leaf.')
Q14CV = Q(13, 'Tissue culture can be used to grow new tissues in the laboratory.')
Q15A = Q(14, 'The human eye is an example of a sense organ.')
Q15B = Q(14, 'The diagram below shows three blood vessels that form part of the circulatory system in the',
         'human body.')
Q15BII = Q(14, 'In your answer book, use one of the above letters A, B, C, to match a blood vessel to',
           'each of the following statements.')
Q15C = Q(15, 'Breathing supplies us with oxygen and gets rid of carbon dioxide.')
Q15CV = Q(15, 'Name one disorder associated with the breathing system.')

# ------------------------------------------------------- scheme cell lines --
LIPIDS = 'e.g. Energy, insulation [allow cell membrane]'
DIGEST = ('A = Liver B = Stomach C = Pancreas', [(' B =', 'Liver '), (' C =', 'Stomach ')])
RHIZOPUS = ('A = Hypha or stolon B = Rhizoid C = Sporangium', [(' B =', 'stolon '), (' C =', 'Rhizoid ')])
STEM = '(i) / (ii) e.g. Transport/ support [allow photosynthesis, food storage]'
TISSUES = 'Vascular and dermal on either diagram.'
FEMALE1 = ('A = Vagina B = Uterus (womb) C = Ovary', [(' B =', 'Vagina '), (' C =', '(womb) ')])
FEMALE2 = ('D = Oviduct (Fallopian tube) E = Endometrium (womb lining)', [(' E =', 'tube) ')])
NEURONS = ('A = Sensory B = Inter (or relay) C = Motor', [(' B =', 'Sensory '), (' C =', 'relay) ')])
BRAIN = ('A = Cerebrum B = Medulla (oblongata) C = Cerebellum', [(' B =', 'Cerebrum '), (' C =', '(oblongata) ')])
SKULL = 'Skull and meninges [allow membranes]'
EYE = ('A = Optic nerve B = Retina C = Lens', [(' B =', 'nerve '), (' C =', 'Retina ')])
VESSELS = ('A = Artery B = Vein C = Capillary', [(' B =', 'Artery '), (' C =', 'Vein ')])
# Q15(b)(ii)'s five lines are read after the lungs labels at the foot of p10.
VESSEL_ROWS = 'Lung/ trachea/ bronchus/ bronchiole/ alveolus'
BLOOD_TO_HEART_MUSCLE = 'Brings blood to heart muscle: A or artery [allow C or capillary]'


def female_labels(asked=None):
    return labels(FEMALE1[0], 'ABC', FEMALE1[1], 8, asked) + labels(FEMALE2[0], 'DE', FEMALE2[1], 8, asked)


TASKS = [
    # ------------------------------------------------------------ Section A --
] + [
    T(f'1{x}', f'Q1({x})', 'A', q, rows, 'bio-1-2', concept, at(5, 1, f'({x})'), 4, stem=[Q1], decision=decision)
    for x, q, rows, concept, decision in [
        ('a', Q(2, 'Lipids are composed of carbon, hydrogen and'), [pt(S('Oxygen or O'), 4)], 'elements-in-lipids', ''),
        ('b', ask(2, 'Give one function of lipids in the human body.'),
         [anyn(None, 1, 4, open_list=True,
               options=[S(LIPIDS, piece=1, psep=', '), S(LIPIDS, piece=[2, 1], psep=[', ', ' ['])],
               note_sel=S(LIPIDS, piece=[2, 1], psep=[' [', ']']))], 'functions-of-lipids',
         'One point, either printed example: a menu of the two, claim one; the scheme\'s bracketed "allow cell '
         'membrane" is the row\'s note.'),
        ('c', ask(2, 'Name one water‐soluble vitamin.'), [pt(S('B or C'), 4)], 'water-soluble-vitamins', ''),
        ('d', ask(2, 'Name one mineral needed by plants.'), [pt(S('e.g. Magnesium'), 4)], 'minerals-for-plants', ''),
        ('e', ask(2, 'Amino acids are the smallest unit of which biomolecule?'), [pt(S('Protein'), 4)],
         'amino-acids-make-protein', '')]
] + [
    T(f'2-{slug}', 'Q2', 'A', Q2 + [Q(2, line, br=True)], [pt(S(f'{name}: {letter}', after='5(4)'), 4)], 'bio-3-1',
      f'identifying-{slug}', SQ(5, f'{name}:', f'{name}:'), 4, qfig='q2-key', item=(slug, name),
      decision='The scheme prices each organism of the key at a point ("5(4)"): one card per organism, anchored on '
               'its name, which the scheme prints over its letter. The drawings and the key are shown as the '
               'question\'s own print.')
    for slug, name, line, letter in [
        ('helix', 'Helix', 'Animal has a shell Helix', 'E'),
        ('musca', 'Musca', 'Animal has three pairs of legs Musca', 'B'),
        ('chilopod', 'Chilopod', 'Animal has more than three pairs of legs Chilopod', 'D'),
        ('nematode', 'Nematode', 'Animal has long cylindrical body Nematode', 'A'),
        ('planarian', 'Planarian', 'Animal has flat body with two eye spots Planarian', 'C')]
] + [
    T(f'3{x}', f'Q3({x})', 'A', Q(3, *q), [pt(S(ans), 4)], 'bio-3-3', concept, at(5, 3, f'({x})'), 4,
      stem=[Q3], qfig='q3-table',
      decision='The list of terms (its first struck through as the worked example) and the table are shown as '
               'the question\'s own print.')
    for x, q, ans, concept in [
        ('a', ('Used to cut the DNA',), 'Enzyme', 'restriction-enzymes'),
        ('b', ('Removing the required DNA from the', 'cell'), 'Isolation', 'isolation'),
        ('c', ('A ring of DNA found in bacterial cells',), 'Plasmid', 'plasmid'),
        ('d', ('A substance produced by bacteria using', 'genetic engineering'), 'Insulin',
         'products-of-genetic-engineering'),
        ('e', ('An application of genetic engineering in', 'plants'), 'Weed-killer resistance',
         'genetic-engineering-in-plants')]
] + [
    T(f'4a-{x.lower()}', 'Q4(a)', 'A', Q(3, 'Name the parts labelled A, B, C.'), [pt(cell(DIGEST[0], i, DIGEST[1]), 3)],
      'bio-2-6', concept, at(5, 4, '(a)'), 3, stem=[Q4], fig='q4-digestive', item=(x.lower(), x),
      labels=labels(DIGEST[0], 'ABC', DIGEST[1], 5, asked=x), decision=EACH_ITEM)
    for i, (x, concept) in enumerate([('A', 'liver'), ('B', 'stomach'), ('C', 'pancreas')])
] + [
    T(f'4{x}', f'Q4({x})', 'A', q, rows, 'bio-2-6', concept,
      at(5, 4, marker) if marker else SQ(5, 'Function of liver:', 'Function of liver:',
                                         paired='The scheme names part A, the liver, in its reprint.'),
      3, stem=[Q4], fig='q4-digestive', labels=labs, decision=decision)
    for x, marker, q, rows, concept, labs, decision in [
        ('b', '(b)', ask(3, 'Name the liquid stored in the gallbladder.'), [pt(S('Bile [allow gall]'), 3)], 'bile',
         None, ''),
        ('c', None, ask(3, 'Give one function of part A.'),
         [anyn(S('e.g. Stores glycogen, breaks down alcohol', after='Stored in gallbladder: Bile [allow gall]'), 1, 3,
               sep=',', open_list=True)], 'functions-of-the-liver', labels(DIGEST[0], 'ABC', DIGEST[1], 5),
         'One point, either printed example: a menu of the two, claim one. ' + MARKER_C),
        ('d', '(d)', Q(3, 'What term is given to the waves of muscular contraction which push the food through the',
                       'alimentary canal?'), [pt(S('Peristalsis'), 3)], 'peristalsis', None, ''),
        ('e', '(e)', Q(3, 'Suggest a substance, produced in part B, that is responsible for ‘heartburn’.'),
         [pt(S('Acid'), 3)], 'stomach-acid', labels(DIGEST[0], 'ABC', DIGEST[1], 5), '')]
] + [
    T(f'5{x}', f'Q5({x})', 'A', ask(4, q), [pt(S(ans), 3)], 'bio-2-1', concept, at(5, 5, f'({x})'), 3, stem=[Q5])
    for x, q, ans, concept in [
        ('a', 'Enzymes are made from carbohydrates.', 'FALSE', 'enzymes-are-proteins'),
        ('b', 'The substance with which an enzyme reacts is called its substrate.', 'TRUE', 'substrate'),
        ('c', 'Enzyme reactions are specific.', 'TRUE', 'enzyme-specificity'),
        ('d', 'Amylases are enzymes that digest lipids in the body.', 'FALSE', 'amylase'),
        ('e', 'Changing pH can affect the rate of activity of an enzyme.', 'TRUE', 'ph-and-enzyme-activity'),
        ('f', 'Enzyme molecules have a folded shape.', 'TRUE', 'enzyme-shape'),
        ('g', 'An immobilised enzyme is one that has lost its function.', 'FALSE', 'immobilised-enzymes')]
] + [
    T('6a', 'Q6(a)', 'A', ask(4, 'To which kingdom does Rhizopus belong?'), [pt(S('Fungi'), 3)], 'bio-3-2',
      'rhizopus-kingdom', at(5, 6, '(a)'), 3, stem=[Q6], fig='q6-rhizopus'),
    T('6b', 'Q6(b)', 'A', ask(4, 'Name one other member of this kingdom.'), [pt(S('e.g. Yeast'), 3)], 'bio-3-2',
      'other-fungi', at(5, 6, '(b)'), 3, stem=[Q6], fig='q6-rhizopus'),
] + [
    T(f'6c-{x.lower()}', 'Q6(c)', 'A', Q(4, 'Name the parts labelled A, B, C in the diagram.'),
      [pt(cell(RHIZOPUS[0], i, RHIZOPUS[1], after='Another fungus: e.g. Yeast'), 3)], 'bio-3-2', concept,
      SQ(5, RHIZOPUS[0], paired='The scheme prints no reprint for (c), only its marker and the three labelled answers: '
                                'anchored on that answer line.'), 3,
      stem=[Q6], fig='q6-rhizopus', item=(x.lower(), x), labels=labels(RHIZOPUS[0], 'ABC', RHIZOPUS[1], 5, asked=x),
      decision=EACH_ITEM + ' ' + MARKER_C)
    for i, (x, concept) in enumerate([('A', 'hypha'), ('B', 'rhizoid'), ('C', 'sporangium')])
] + [
    T('6d', 'Q6(d)', 'A', Q(4, 'Give two examples of the economic importance of such organisms.'),
      [anyn(S('e.g. Brewing/ baking/ disease'), 2, 3, open_list=True)], 'bio-3-2', 'economic-importance-of-fungi',
      at(5, 6, '(d)'), 6, stem=[Q6], fig='q6-rhizopus',
      decision='Two points (the scheme prints "(2 pt)") from its examples: one menu, claim two.'),
    # ------------------------------------------------------------ Section B --
    T('7a', 'Q7(a)', 'B', Q(5, 'Give two functions of the stem in plants.'),
      [anyn(None, 2, 5, open_list=True,
            options=[S(STEM, piece=[2, 2], psep=['/', '(ii) ']), S(STEM, piece=[3, 1], psep=['/', ' ['])],
            note_sel=S(STEM, piece=[2, 1], psep=[' [', ']']))], 'bio-2-6', 'functions-of-the-stem',
      rq(6, 'Two stem functions:'), 10,
      decision='"5 + 1" over the two functions, carded at its first rate. The scheme sets both answer lines\' markers '
               '"(i) / (ii)" before its examples and brackets two more it allows; the examples are the menu, the '
               'bracket the row\'s note.'),
    T('7bi', 'Q7(b)(i)', 'B', ask(5, 'Name the plant that you used.'), [pt(S('e.g. Begonia'), 6)], 'bio-2-6',
      'plant-for-a-stem-section', at(6, 7, '(b)', '(i)'), 6, stem=[Q7B]),
    T('7bii', 'Q7(b)(ii)', 'B', Q(5, 'State one reason why you used a herbaceous stem rather than a woody one.'),
      [pt(S('Easier to cut'), 6)], 'bio-2-6', 'why-a-herbaceous-stem', at(6, 7, '(b)', '(ii)'), 6, stem=[Q7B]),
    T('7biii1', 'Q7(b)(iii)1', 'B', ask(5, '1. What did you use to cut the section of stem?'),
      [pt(S('Backed blade or scalpel'), 6)], 'bio-2-6', 'cutting-a-stem-section', at(6, 7, '(b)', '(iii)'), 6,
      stem=[Q7B], decision=EACH_ITEM),
    T('7biii2', 'Q7(b)(iii)2', 'B', Q(5, '2. What kind of transverse section did you cut?', piece=1, psep='_'),
      [pt(S('Thin'), 6)], 'bio-2-6', 'a-thin-section', at(6, 7, '(b)', '(iii)'), 6, stem=[Q7B],
      decision=EACH_ITEM + ' The paper runs this ask straight into its answer line; the ask is cut at the line.'),
    T('7biv', 'Q7(b)(iv)', 'B', Q(5, 'How did you transfer the section to the microscope slide?'),
      [pt(S('e.g. Paintbrush'), 6)], 'bio-2-6', 'transferring-the-section', at(6, 7, '(b)', '(iv)'), 6, stem=[Q7B]),
    T('7bv', 'Q7(b)(v)', 'B', Q(5, 'Which of the following diagrams, A or B, best represents what was seen on your slide?'),
      [pt(S('B'), 6)], 'bio-2-6', 'dicot-stem-section', at(6, 7, '(b)', '(v)'), 6, stem=[Q7B], fig='q7-stems'),
    T('7bvi', 'Q7(b)(vi)', 'B', Q(5, 'On your chosen diagram label the following tissues: 1. vascular tissue, 2. dermal tissue.'),
      [pt(S(TISSUES, piece=p, psep=sep), 6, note_sel=S(TISSUES, piece=[2, 2], psep=[' and ', 'dermal ']))
       for p, sep in ((1, ' and '), ([2, 1], [' and ', ' on ']))], 'bio-2-6', 'stem-tissues',
      at(6, 7, '(b)', '(vi)'), 12, stem=[Q7B], fig='q7-stems',
      decision=TWO_POINTS + ' The scheme prints "Vascular and dermal on either diagram." (2 pts): cut at its own '
                            '"and", a row each, its "on either diagram." each row\'s note.'),
    T('8ai', 'Q8(a)(i)', 'B', ask(6, 'What gas must be absent for anaerobic respiration to occur?'),
      [pt(S('Oxygen'), 5)], 'bio-2-2', 'anaerobic-respiration', at(6, 8, '(a)', '(i)'), 5),
    T('8aii', 'Q8(a)(ii)', 'B', ask(6, 'Does anaerobic respiration release more or less energy than aerobic respiration?'),
      [pt(S('Less'), 5)], 'bio-2-2', 'energy-from-anaerobic-respiration', at(6, 8, '(a)', '(ii)'), 5),
    T('8bi1', 'Q8(b)(i)1', 'B', ask(6, '1. To which flask was the yeast added?'),
      [pt(S('A 2. (1 pt)', piece=1, psep=' 2.'), 4)], 'bio-2-2', 'flask-with-yeast', at(6, 8, '(b)', '(i)'), 4,
      stem=[Q8B], fig='q8-flasks',
      decision=EACH_ITEM + ' The scheme prints item 2\'s number at the end of item 1\'s line ("A 2. (1 pt)").'),
    T('8bi2', 'Q8(b)(i)2', 'B', ask(6, '2. Give a reason for your choice.'),
      [pt(S('Reason for choice Bubbles (or CO2)', piece=2, psep='choice '), 4)], 'bio-2-2', 'evidence-of-fermentation',
      at(6, 8, '(b)', '(i)'), 4, stem=[Q8B, ask(6, '1. To which flask was the yeast added?')], fig='q8-flasks',
      decision=EACH_ITEM + ' The scheme sets the reprint "Reason for choice" before the answer with no colon; the '
                           'answer is the line cut after it.'),
    T('8bii', 'Q8(b)(ii)', 'B', ask(6, 'What is the purpose of the other flask?'), [pt(S('Control'), 4)], 'bio-2-2',
      'control-flask', at(6, 8, '(b)', '(ii)'), 4, stem=[Q8B], fig='q8-flasks'),
    T('8biii', 'Q8(b)(iii)', 'B', Q(6, 'Name the two substances in the original solution in the flasks.'),
      [pt(S('Glucose or sugar'), 4), pt(S('Water'), 4)], 'bio-2-2', 'fermentation-solution',
      rq(6, 'In original solution:'), 8, stem=[Q8B], fig='q8-flasks', decision=TWO_POINTS),
    T('8biv', 'Q8(b)(iv)', 'B', ask(6, 'What is the purpose of the water bath?'),
      [pt(S('To keep temperature constant'), 4)], 'bio-2-2', 'water-bath', at(6, 8, '(b)', '(iv)'), 4, stem=[Q8B],
      fig='q8-flasks'),
    T('8bv', 'Q8(b)(v)', 'B', ask(6, 'What is the purpose of a fermentation lock?'),
      [pt(S('To keep oxygen out or to avoid contamination'), 4)], 'bio-2-2', 'fermentation-lock',
      rq(6, 'Why fermentation lock:'), 4, stem=[Q8B], fig='q8-flasks', decision=OUT_OF_ORDER),
    T('8bvi', 'Q8(b)(vi)', 'B', Q(6, 'Say what test you performed to show the presence of alcohol and say what colour indicated',
                                  'a positive result.'),
      [pt(S('Alcohol test: Iodoform [allow dichromate] (1 pt)', piece=1, psep=' (1 pt)'), 4),
       pt(S('Positive colour: Yellow [allow green if dichromate used]'), 4)], 'bio-2-2', 'test-for-alcohol',
      at(6, 8, '(b)', '(vi)'), 8, stem=[Q8B], fig='q8-flasks',
      decision='The test and its colour, a point each: a row each, labelled with the scheme\'s own reprints.'),
    T('9a', 'Q9(a)', 'B', [Q(7, 'Complete the following sentence.'),
                           Q(7, 'Osmosis is the movement of water molecules', 'concentration of water molecules.',
                             br=True)],
      [pt(S('From: High(er) (conc. of water molecules)'), 5), pt(S('To: Low(er) (conc. of water molecules)'), 5)],
      'bio-2-6', 'osmosis', at(6, 9, '(a)', '(i)'), 10,
      decision='"5 + 1" over the sentence\'s two blanks, carded at its first rate: a row each, labelled with the '
               'scheme\'s own "From:" and "To:".'),
    T('9bi', 'Q9(b)(i)', 'B', Q(7, 'In the space below, draw a labelled diagram of the apparatus you used in your',
                                'demonstration.'),
      [pt(S('Diagram of osmosis set-up: Two solutions and a membrane'), 6, kind='criterion',
          note_sel=S('6,3,0'), note_lead='The scheme marks the diagram'),
       anyn(S('e.g. Water/ salt or sugar soln./ Visking tubing or potato'), 3, 2, open_list=True)], 'bio-2-6',
      'osmosis-apparatus', at(6, 9, '(b)', '(i)'), 12, stem=[Q9B],
      decision='The diagram ("6,3,0") and its labels ("3(2)") are priced on their own, as the scheme\'s '
               '"6 + 3(2) + 4(3)" sets out for (b).'),
    T('9bii', 'Q9(b)(ii)', 'B', ask(7, 'Suggest a control that you might use in this activity.'),
      [pt(S('e.g. Only water in tubing or boiled potato'), 3)], 'bio-2-6', 'osmosis-control',
      at(6, 9, '(b)', '(ii)'), 3, stem=[Q9B]),
    T('9biii', 'Q9(b)(iii)', 'B', ask(7, 'State the result(s) of the demonstration.'),
      [pt(S('e.g. Tubing heavier or tubing lighter or tubing swollen or', 'more liquid in scooped out potato',
            after='Section B'), 3)], 'bio-2-6', 'osmosis-result', rq(6, 'Result:'), 3, stem=[Q9B],
      decision=OUT_OF_ORDER + ' Its answer shares the reprint\'s line, so it is read from the line after the '
                              'page\'s "Section B" footer, the line printed before it.'),
    T('9biv', 'Q9(b)(iv)', 'B', ask(7, 'Briefly explain the result(s).'),
      [pt(S('Water moved from higher conc. of water molecules or to lower', 'conc. of water molecules'), 3)], 'bio-2-6',
      'explaining-osmosis', rq(6, 'Explain result:'), 3, stem=[Q9B], decision=OUT_OF_ORDER),
    T('9bv', 'Q9(b)(v)', 'B', ask(7, 'Suggest how storing food in salty water prevents the growth of bacteria or fungi.'),
      [pt(S('Microorganisms (or named) dehydrated'), 3)], 'bio-2-6', 'salt-as-a-preservative',
      rq(6, 'How salty water stops microorganisms growing:',
         paired='The scheme rewords "prevents the growth of bacteria or fungi" as "stops microorganisms growing".'),
      3, stem=[Q9B], decision=OUT_OF_ORDER),
    # ------------------------------------------------------------ Section C --
] + [
    T(f'10a{r}', f'Q10(a)({r})', 'C', Q(8, *q), [pt(S(*ans), 7)], 'bio-1-4', concept, at(7, 10, '(a)', f'({r})'), 7)
    for r, q, ans, concept in [
        ('i', ('Explain the term phenotype.',), ('(Physical) expression of the genotype [allow (physical)', 'appearance]'),
         'phenotype'),
        ('ii', ('How many characteristics are involved in a monohybrid cross?',), ('One (characteristic)',),
         'monohybrid-cross'),
        ('iii', ('Are heterozygous alleles the same as each other or different?',
                 'Are heterozygous alleles the same as each other or different?'), ('(Alleles) different',),
         'heterozygous')]
] + [
    T(f'10b{r}', f'Q10(b)({r})', 'C', Q(8, *q), rows, 'bio-2-3', concept, at(7, 10, '(b)', f'({r})'), total, stem=stem,
      fig=fig, decision=decision)
    for r, q, rows, concept, total, stem, fig, decision in [
        ('i', ('Cell division is one stage of the cell cycle. Name the other stage.',), [pt(S('Interphase'), 3)],
         'interphase', 3, [], None, ''),
        ('ii', ('There are two types of cell division. Name both.',), [pt(S('Mitosis'), 3), pt(S('Meiosis'), 3)],
         'types-of-cell-division', 6, [], None, TWO_POINTS),
        ('iii', ('Structure A is a chromosome. From which two substances are chromosomes made?',),
         [pt(S('DNA'), 3), pt(S('Protein'), 3)], 'chromosome-composition', 6, [Q10BD], 'q10-division', TWO_POINTS),
        ('iv', ('What is the function of structure B in the above diagram?',),
         [pt(S('To contract or to separate chromosomes'), 3)], 'spindle-fibres', 3, [Q10BD], 'q10-division', ''),
        ('v', ('How many chromosomes will be in each new cell formed from the above division?',), [pt(S('Four'), 3)],
         'chromosome-number-after-mitosis', 3, [Q10BD], 'q10-division', ''),
        ('vi', ('Cancer occurs when there is uncontrolled cell division in one or more tissues.',
                'Give two possible causes of cancer.'),
         [anyn(S('e.g. Radiation/ smoking/ viruses/ genetics'), 2, 3, open_list=True)], 'causes-of-cancer', 6, [], None,
         '')]
] + [
    T(f'10c{r}', f'Q10(c)({r})', 'C', Q(8, *q), rows, 'bio-2-3', concept, sq, total, stem=[Q10C] + extra,
      decision=decision)
    for r, q, rows, concept, sq, total, extra, decision in [
        ('i', ('What is a mutation?',), [pt(S('Change in the genetic material (or named) (of a cell)'), 3)], 'mutation',
         at(7, 10, '(c )', '(i)'), 3, [], ''),
        ('ii', ('Give an example of a disease caused by mutation.',), [pt(S("e.g.Huntington's disease"), 3)],
         'disease-caused-by-mutation', at(7, 10, '(c )', '(ii)'), 3, [], ''),
        ('iii', ('Give two symptoms of the disease.',),
         [anyn(S('e.g. Restlessness/ difficulty walking/ difficulty thinking/ difficulty', 'remembering'), 2, 3,
               open_list=True)], 'symptoms-of-huntingtons', rq(7, 'Two symptoms:'), 6,
         [M('(ii)', 8), Q(8, 'Give an example of a disease caused by mutation.')], OUT_OF_ORDER),
        ('iv', ('What is a mutagen?',), [pt(S('Causes mutations'), 3)], 'mutagen', at(7, 10, '(c )', '(iv)'), 3, [], ''),
        ('v', ('Give two examples of mutagens.',), [anyn(S('e.g. Gamma rays/ asbestos'), 2, 3, open_list=True)],
         'examples-of-mutagens', at(7, 10, '(c )', '(v)'), 6, [], ''),
        ('vi', ('How many copies of a chromosome are usually present in a gamete?',
                'How many copies of a chromosome are usually present in a gamete?'), [pt(S('One'), 3)],
         'haploid-gametes', at(7, 10, '(c )', '(vi)'), 3, [], '')]
] + [
    T(f'11a{r}', f'Q11(a)({r})', 'C', Q(9, q), [pt(S(ans), 7)], 'bio-3-1', concept, at(7, 11, '(a)', f'({r})'), 7)
    for r, q, ans, concept in [
        ('i', 'Why are plants known as producers?', 'Make their own food', 'producers'),
        ('ii', 'What is the main source of energy for living things?', 'Sun', 'energy-source'),
        ('iii', 'What term is given to a diagram showing a number of interlinked food chains?', 'Food web', 'food-web')]
] + [
    T(f'11b{r}', f'Q11(b)({r})', 'C', Q(9, q), rows, topic, concept, sq, total, stem=[Q11B], decision=decision)
    for r, q, rows, topic, concept, sq, total, decision in [
        ('i', 'What plant is spreading along the river banks?', [pt(S('(Giant) hogweed'), 3)], 'bio-3-1',
         'giant-hogweed', at(7, 11, '(b)', '(i)'), 3, ''),
        ('ii', 'How does this plant damage our skin?', [pt(S('Blisters'), 3)], 'bio-3-1', 'hogweed-blisters',
         at(7, 11, '(b)', '(ii)'), 3, 'The scheme prints this part\'s tariff "(1 tp)", a point.'),
        ('iii', 'What is meant by the term species?',
         [pt(S('Organisms that can interbreed/ to produce fertile offspring', piece=n), 3) for n in (1, 2)], 'bio-1-5',
         'species', rq(7, 'Species:'), 6, TWO_POINTS + ' ' + OUT_OF_ORDER),
        ('iv', 'Where did zebra mussels come from?', [pt(S('The Black Sea'), 3)], 'bio-3-1', 'zebra-mussels',
         at(7, 11, '(b)', '(iv)'), 3, ''),
        ('v', 'What species is attacking the earthworms?', [pt(S('New Zealand flatworms'), 3)], 'bio-3-1',
         'new-zealand-flatworms', at(7, 11, '(b)', '(v)'), 3, ''),
        ('vi', 'Mention two ways in which earthworms are important in the soil.',
         [anyn(S('e.g. Drainage/ aeration'), 2, 3, open_list=True)], 'bio-3-1', 'earthworms-in-soil',
         at(7, 11, '(b)', '(vi)'), 6, ''),
        ('vii', 'Name one resident animal that is not native to Ireland.',
         [anyn(S('e.g. Sheep/ pigs'), 1, 3, open_list=True)], 'bio-3-1', 'non-native-species',
         at(7, 11, '(b)', '(vii)'), 3, 'One point, any printed example: a menu, claim one.')]
] + [
    T('11ci', 'Q11(c)(i)', 'C', Q(9, 'Name the ecosystem.'),
      [pt(S('Name of ecosystem studied: Name'), 3, kind='criterion', note=NO_ANSWER)], 'bio-3-1', 'ecosystem-studied',
      at(7, 11, '(c)', '(i)'), 3, stem=[Q11C]),
    T('11cii', 'Q11(c)(ii)', 'C', Q11CII,
      [pt(S('One plant and one animal: Must match (c)(i)'), 6, kind='criterion', units=[3, 3], note=NO_ANSWER)],
      'bio-3-1', 'organisms-in-the-ecosystem', at(7, 11, '(c)', '(ii)'), 6, stem=[Q11C],
      decision='The scheme prices the plant and the animal at two points (2 pts) on one printed line, "Must match '
               '(c)(i)": one criterion row worth both.'),
    T('11ciii', 'Q11(c)(iii)', 'C', Q(9, 'What is a quantitative survey?'),
      [pt(S('Count or estimate number of organisms'), 3)], 'bio-3-1', 'quantitative-survey', at(7, 11, '(c)', '(iii)'),
      3, stem=[Q11C]),
] + [
    T('11civ', 'Q11(c)(iv)', 'C', Q(9, 'Describe how you carried out a quantitative survey to estimate the population of either',
                                    'the plant or the animal referred to in part (ii) above.'),
      [anyn(S(*menu), 4, 3)], 'bio-3-1', f'quantitative-survey-of-an-{route}' if route == 'animal'
      else f'quantitative-survey-of-a-{route}', at(7, 11, '(c)', '(iv)'), 12, route=route,
      stem=[Q11C, M('(ii)', 9), Q11CII],
      decision='The plant or the animal: the scheme prints a separate list for each, joined by "OR", each worth '
               '"(4 pts)", so each is a route card, any four of its points.')
    for route, menu in [('plant', ('Quadrat/ random/ how random/', 'count plants (or estimate cover)/ record/ repeat or scale up')),
                        ('animal', ('Capture/ mark or how mark/', 'count/ release/ recapture/ count marked/ calculation'))]
] + [
    T('12ai', 'Q12(a)(i)', 'C', Q(10, 'Name the two main types of reproduction.'),
      [pt(S('Asexual and sexual', piece=n, psep=' and '), 7) for n in (1, 2)], 'bio-2-5', 'types-of-reproduction',
      at(8, 12, '(a)', '(i)'), 14,
      decision='Two points on the ladder ("7 + 2(1)"), printed "Asexual and sexual": a row each.'),
    T('12aii', 'Q12(a)(ii)', 'C', Q(10, 'Which type of reproduction occurs in humans?'), [pt(S('Sexual'), 7)],
      'bio-2-5', 'human-reproduction', at(8, 12, '(a)', '(ii)'), 7),
] + [
    T(f'12bi-{x.lower()}', 'Q12(b)(i)', 'C', Q(10, 'Name the parts labelled A, B, C, D, E.'),
      [pt(cell(line[0], i, line[1]), 3)], 'bio-2-5', concept,
      SQ(8, '(i)', path=['12', '(b)'], nth=5, bare=True,
         paired='The text layer reads this marker and its two answer lines at the foot of the page, after Question '
                '13: the fifth "(i)" after Q12(b).'), 3,
      stem=[Q12B], fig='q12-female', item=(x.lower(), x), labels=female_labels(x), decision=EACH_ITEM)
    for x, line, i, concept in [('A', FEMALE1, 0, 'vagina'), ('B', FEMALE1, 1, 'uterus'), ('C', FEMALE1, 2, 'ovary'),
                                ('D', FEMALE2, 0, 'oviduct'), ('E', FEMALE2, 1, 'endometrium')]
] + [
    T('12bii', 'Q12(b)(ii)', 'C', Q(10, 'State one function of the part labelled C in the diagram.'),
      [pt(S('To produce eggs or to produce hormones (or named hormone)'), 3)], 'bio-2-5', 'functions-of-the-ovary',
      rq(8, 'Function of C:'), 3, stem=[Q12B], fig='q12-female', labels=female_labels()),
    T('12biii', 'Q12(b)(iii)', 'C', Q(10, 'In which labelled part does fertilisation usually occur?'),
      [pt(S('D or oviduct'), 3)], 'bio-2-5', 'site-of-fertilisation', at(8, 12, '(b)', '(iii)'), 3, stem=[Q12B],
      fig='q12-female'),
    T('12biv', 'Q12(b)(iv)', 'C', Q(10, 'What is meant by the term contraception?'),
      [pt(S('Prevention of fertilisation or prevention of pregnancy'), 3)], 'bio-2-5', 'contraception',
      rq(8, 'Contraception:'), 3, stem=[Q12B], fig='q12-female'),
    T('12bv', 'Q12(b)(v)', 'C', Q(10, 'Give one method of contraception.', 'Give one method of contraception.'),
      [pt(S('e.g. (The) Pill or condom'), 3)], 'bio-2-5', 'methods-of-contraception', at(8, 12, '(b)', '(v)'), 3,
      stem=[Q12B], fig='q12-female'),
    T('12ci', 'Q12(c)(i)', 'C', Q(10, 'How long does an average human pregnancy last?'),
      [pt(S('Nine months or 38-40 weeks'), 3)], 'bio-2-5', 'length-of-pregnancy', at(8, 12, '(c)', '(i)'), 3),
    T('12cii', 'Q12(c)(ii)', 'C', Q(10, 'Birth takes place in three stages. Describe what happens at each stage.'),
      [pt(S('Stage1: Contractions begin or waters break or cervix dilates'), 3),
       pt(S('Stage 2: Baby born through vagina'), 3), pt(S('Stage 3: Placenta out through vagina'), 3)], 'bio-2-5',
      'stages-of-birth', at(8, 12, '(c)', '(ii)'), 9,
      decision='One point for each stage, each printed on its own line under its stage: a row each.'),
] + [
    T(f'12ciii{n}', f'Q12(c)(iii){n}', 'C', ask(10, q), [pt(S(ans), 3)], 'bio-2-5', concept, at(8, 12, '(c)', '(iii)'),
      3, stem=[Q12CIII], decision=EACH_ITEM)
    for n, q, ans, concept in [(1, '1. What happens to the level of progesterone at birth?', 'Falls',
                                'progesterone-at-birth'),
                               (2, '2. What effect has oxytocin on the muscles of the wall of the womb?',
                                '(Muscles) contract', 'oxytocin')]
] + [
    T('12civ', 'Q12(c)(iv)', 'C', Q(10, 'What hormone controls the production of milk in humans?'),
      [pt(S('Prolactin'), 3)], 'bio-2-5', 'prolactin', at(8, 12, '(c)', '(iv)'), 3),
    T('12cv', 'Q12(c)(v)', 'C', Q(10, 'Suggest one reason why colostrum is important for new‐born babies.'),
      [pt(S('Rich in proteins (or fat) or rich in antibodies or rich in minerals'), 3)], 'bio-2-5', 'colostrum',
      rq(8, 'Why colostrum important:'), 3, decision=OUT_OF_ORDER),
    T('13ai', 'Q13(a)(i)', 'C', Q(11, 'Name the chemicals that act as messengers in the endocrine system.'),
      [pt(S('Hormones'), 7)], 'bio-2-4', 'hormones', at(8, 13, '(a)', '(i)'), 7, stem=[Q13A]),
    T('13aii', 'Q13(a)(ii)', 'C', Q(11, 'The central nervous system is made up of two parts. Name both.'),
      [pt(S('Brain and spinal cord', piece=n, psep=' and '), 7) for n in (1, 2)], 'bio-2-4', 'central-nervous-system',
      at(8, 13, '(a)', '(ii)'), 14, stem=[Q13A],
      decision='Two points on the ladder ("7 + 2(1)"), printed "Brain and spinal cord": a row each.'),
] + [
    T(f'13bi-{x.lower()}', 'Q13(b)(i)', 'C', Q(11, 'Name the neurons labelled A, B, C.'),
      [pt(cell(NEURONS[0], i, NEURONS[1]), 3)], 'bio-2-4', concept, at(8, 13, '(b)', '(i)'), 3, stem=[Q13B],
      fig='q13-reflex', item=(x.lower(), x), labels=labels(NEURONS[0], 'ABC', NEURONS[1], 8, asked=x),
      decision=EACH_ITEM)
    for i, (x, concept) in enumerate([('A', 'sensory-neuron'), ('B', 'interneuron'), ('C', 'motor-neuron')])
] + [
    T(f'13b{r}', f'Q13(b)({r})', 'C', Q(11, q), [row], 'bio-2-4', concept, at(8, 13, '(b)', f'({r})'), 3, stem=[Q13B],
      fig='q13-reflex', decision=decision)
    for r, q, row, concept, decision in [
        ('ii', 'Is the impulse transmitted from A to B to C OR from C to B to A?', pt(S('A to B to C'), 3),
         'direction-of-an-impulse', ''),
        ('iii', 'Give one example of a reflex action in humans.',
         anyn(S('e.g. Blinking, knee jerk'), 1, 3, sep=',', open_list=True), 'reflex-actions',
         'One point, either printed example: a menu of the two, claim one.'),
        ('iv', 'Why are reflex actions important to humans?', pt(S('Protection'), 3), 'why-reflexes-matter', ''),
        ('v', 'What name is given to the gaps between neurons?', pt(S('Synapses'), 3), 'synapses', ''),
        ('vi', 'Neurotransmitters are released into the gaps between the neurons. Why does this occur?',
         pt(S('To carry impulse (to next neuron)'), 3), 'neurotransmitters', ''),
        ('vii', 'What happens to neurotransmitters once they have carried out their function?',
         pt(S('Broken down or recycled'), 3), 'fate-of-neurotransmitters', '')]
] + [
    T(f'13ci-{x.lower()}', 'Q13(c)(i)', 'C', Q(11, 'Name the parts labelled A, B, C.'),
      [pt(cell(BRAIN[0], i, BRAIN[1]), 3)], 'bio-2-4', concept, at(8, 13, '(c )', '(i)'), 3, stem=[Q13C],
      fig='q13-brain', item=(x.lower(), x), labels=labels(BRAIN[0], 'ABC', BRAIN[1], 8, asked=x),
      decision=EACH_ITEM + ' The scheme prints its marker "(c )".')
    for i, (x, concept) in enumerate([('A', 'cerebrum'), ('B', 'medulla'), ('C', 'cerebellum')])
] + [
    T('13cii', 'Q13(c)(ii)', 'C', Q(11, 'Give one function of the part labelled B.'),
      [anyn(S('e.g. Controls breathing/ controls swallowing/', 'controls heart beat/ controls involuntary muscles'), 1, 3,
            open_list=True)], 'bio-2-4', 'functions-of-the-medulla', at(8, 13, '(c )', '(ii)'), 3, stem=[Q13C],
      fig='q13-brain', labels=labels(BRAIN[0], 'ABC', BRAIN[1], 8),
      decision='One point, any printed example: a menu, claim one.'),
    T('13ciii', 'Q13(c)(iii)', 'C', Q(11, 'Give one function of the part labelled C.'),
      [pt(S('(Muscle) co-ordination or balance'), 3)], 'bio-2-4', 'functions-of-the-cerebellum',
      at(8, 13, '(c )', '(iii)'), 3, stem=[Q13C], fig='q13-brain', labels=labels(BRAIN[0], 'ABC', BRAIN[1], 8)),
    T('13civ', 'Q13(c)(iv)', 'C', Q(11, 'What are the two main structures that protect the', 'brain?'),
      [pt(S(SKULL, piece=1, psep=' and '), 3),
       pt(S(SKULL, piece=[2, 1], psep=[' and ', ' [']), 3, note_sel=S(SKULL, piece=[2, 1], psep=[' [', ']']))],
      'bio-2-4', 'protecting-the-brain', at(8, 13, '(c )', '(iv)'), 6, stem=[Q13C], fig='q13-brain',
      decision=TWO_POINTS + ' The scheme\'s bracketed "allow membranes" is the second row\'s note.'),
    T('13cv', 'Q13(c)(v)', 'C', [Q(11, 'The hypothalamus in the brain plays a role in', 'homeostasis.'),
                                 Q(11, 'What is meant by the term homeostasis?')],
      [pt(S('Maintaining a constant internal environment (in the body)'), 3)], 'bio-2-4', 'homeostasis',
      rq(8, 'Homeostasis:'), 3, stem=[Q13C], fig='q13-brain'),
    T('14ai', 'Q14(a)(i)', 'C', Q(12, 'What is meant by the term metabolism?'),
      [pt(S('All the chemical reactions in a body or in a cell'), 3)], 'bio-2-1', 'metabolism',
      at(9, 14, '(a)', '(i)'), 3),
] + [
    T(f'14aii{n}', f'Q14(a)(ii){n}', 'C', Q(12, q), [pt(S(ans), 3)], 'bio-2-1', concept, at(9, 14, '(a)', '(ii)'), 3,
      stem=Q14AII, decision=EACH_ITEM + ' "(2 pts)" over the two numbered processes.')
    for n, q, ans, concept in [(1, '1. Photosynthesis.', 'Photosynthesis: Anabolism', 'photosynthesis-is-anabolic'),
                               (2, '2. Respiration.', 'Respiration: Catabolism', 'respiration-is-catabolic')]
] + [
    T(f'14a{r}', f'Q14(a)({r})', 'C', Q(12, *q), [row], topic, concept, at(9, 14, '(a)', f'({r})'), total,
      stem=stem, fig=fig)
    for r, q, row, topic, concept, total, stem, fig in [
        ('iii', ('Give two reasons why living things need energy.',),
         anyn(S('e.g. Movement/ heat/ growth'), 2, 3, open_list=True), 'bio-2-1', 'why-living-things-need-energy', 6,
         [], None),
        ('iv', ('In stage 1 of respiration glucose is partly broken down. Where in the cell does', 'this occur?'),
         pt(S('Cytoplasm'), 3), 'bio-2-2', 'site-of-glycolysis', 3, [], None),
        ('v', ('Name the cell structure shown below in which stage 2 of respiration takes', 'place.'),
         pt(S('Mitochondrion'), 3), 'bio-2-2', 'mitochondrion', 3, [], 'q14-mitochondrion'),
        ('vi', ('Which type of respiration results in the production of acid in our muscles?',),
         pt(S('Anaerobic'), 3), 'bio-2-2', 'anaerobic-respiration-in-muscle', 3, [], None),
        ('vii', ('What is the name of the acid produced in the muscles?',), pt(S('Lactic'), 3), 'bio-2-2',
         'lactic-acid', 3, [M('(vi)', 12), Q14AVI], None),
        ('viii', ('Suggest what might happen to this acid in the muscles afterwards.',), pt(S('Broken down'), 3),
         'bio-2-2', 'fate-of-lactic-acid', 3, [M('(vii)', 12), Q14AVII], None)]
] + [
    # (ii)-(iv) name lettered parts: their key decodes B and C with the scheme's
    # own answers (shown after the reveal; the asked letter is marked). The
    # scheme names no structure for A (its (ii) answer is what A's cells hold).
    T(f'14b{r}', f'Q14(b)({r})', 'C', Q(12, *q), rows, topic, concept, sq, total, stem=[Q14B], fig='q14-leaf',
      decision=decision,
      labels=[L('B', S('Stoma', page=9), r == 'iii'), L('C', S('Guard cells', page=9), r == 'iv')]
      if r in ('ii', 'iii', 'iv') else None)
    for r, q, rows, topic, concept, sq, total, decision in [
        ('i', ('Name the green pigment present in leaves that is essential for photosynthesis.',),
         [pt(S('Chlorophyll'), 3)], 'bio-2-2', 'chlorophyll', at(9, 14, '(b)', '(i)'), 3, ''),
        ('ii', ('Name the cell structures, present in large numbers in the cells labelled A that are',
                'needed for photosynthesis.'), [pt(S('Chloroplasts'), 3)], 'bio-2-2', 'chloroplasts',
         at(9, 14, '(b)', '(ii)'), 3, ''),
        ('iii', ('Name the opening labelled B that is used for gas exchange.',), [pt(S('Stoma'), 3)], 'bio-2-2',
         'stomata', at(9, 14, '(b)', '(iii)'), 3, ''),
        ('iv', ('Name the cells labelled C that control the opening of B.',), [pt(S('Guard cells'), 3)], 'bio-2-6',
         'guard-cells', at(9, 14, '(b)', '(iv)'), 3, ''),
        ('v', ('Name the gas in the air that is needed for photosynthesis.',), [pt(S('Carbon dioxide'), 3)], 'bio-2-2',
         'carbon-dioxide-for-photosynthesis', at(9, 14, '(b)', '(v)'), 3, ''),
        ('vi', ('In photosynthesis, water is split into three parts.', 'Name these three parts.'),
         [pt(S('Protons (H+)/ electrons/ oxygen', piece=n), 3) for n in (1, 2, 3)], 'bio-2-2', 'splitting-water',
         at(9, 14, '(b)', '(vi)'), 9, 'Three points, all three asked: a row each, cut at the scheme\'s own solidus.'),
        ('vii', ('From your knowledge of photosynthesis, suggest two ways of improving the rate of',
                 'photosynthesis of plants in a greenhouse.'),
         [anyn(S('Brighter light/ more carbon dioxide/ increased temperature'), 2, 3)], 'bio-2-2',
         'improving-photosynthesis', rq(9, 'Improve photosynthesis rate by:'), 6, OUT_OF_ORDER)]
] + [
    T('14ci', 'Q14(c)(i)', 'C', Q(13, 'What is an organ?'), [pt(S('Group of tissues working together'), 3)], 'bio-1-3',
      'organ', at(9, 14, '(c)', '(i)'), 3),
    T('14cii', 'Q14(c)(ii)', 'C', Q(13, 'Name one plant organ and one animal organ.'),
      [pt(S('Plant organ: e.g. Leaf (1 pt)', piece=1, psep=' (1 pt)'), 3), pt(S('Animal organ: e.g. Heart'), 3)],
      'bio-1-3', 'examples-of-organs', at(9, 14, '(c)', '(ii)'), 6,
      decision='One point for each organ, each printed under its own heading: a row each.'),
    T('14ciii', 'Q14(c)(iii)', 'C', Q(13, 'What is a tissue?'), [pt(S('Group of similar cells working together'), 3)],
      'bio-1-3', 'tissue', at(9, 14, '(c)', '(iii)'), 3),
    T('14civ', 'Q14(c)(iv)', 'C', Q(13, 'Name one plant tissue and one animal tissue.'),
      [pt(S('Plant tissue: e.g. Xylem'), 3), pt(S('Animal tissue: e.g. Blood'), 3)], 'bio-1-3', 'examples-of-tissues',
      at(9, 14, '(c)', '(iv)'), 6, decision='One point for each tissue, each printed under its own heading: a row each.'),
] + [
    T(f'14cv{n}', f'Q14(c)(v){n}', 'C', [M(f'{n}.', 13), Q(13, q)], [pt(S(ans, after='Animal tissue: e.g. Blood'), 3)],
      topic, concept, SQ(9, sq, sq), 3, stem=[Q14CV],
      decision=EACH_ITEM + ' "(4 pts)" over the four numbered asks. ' + OUT_OF_ORDER + ' Each answer shares its '
               'reprint\'s line, so it is read from after (c)(iv), the line printed before them.')
    for n, q, ans, topic, concept, sq in [
        (1, 'What gas would be needed for the growth of animal tissue in the laboratory?', 'Oxygen', 'bio-1-3',
         'gas-for-tissue-culture', '1. Gas needed for animal tissue growth:'),
        (2, 'What gas would be produced by animal tissue in the laboratory?', 'Carbon dioxide', 'bio-1-3',
         'gas-from-tissue-culture', '2. Gas produced by animal tissue growth:'),
        (3, 'Why are sterile conditions needed to grow tissue in the laboratory?', 'To prevent growth of microorganisms',
         'bio-1-3', 'sterile-tissue-culture', '3. Why sterile conditions:'),
        (4, 'Which type of cell division is involved in tissue culture?', 'Mitosis', 'bio-2-3',
         'mitosis-in-tissue-culture', '4. Cell division in tissue culture:')]
] + [
    T(f'15ai-{x.lower()}', 'Q15(a)(i)', 'C', Q(14, 'Name the parts labelled A, B, C.'), [pt(cell(EYE[0], i, EYE[1]), 3)],
      'bio-2-4', concept, at(10, 15, '(a)', '(i)'), 3, stem=[Q15A], fig='q15-eye', item=(x.lower(), x),
      labels=labels(EYE[0], 'ABC', EYE[1], 10, asked=x), decision=EACH_ITEM)
    for i, (x, concept) in enumerate([('A', 'optic-nerve'), ('B', 'retina'), ('C', 'lens')])
] + [
    T(f'15a{r}', f'Q15(a)({r})', 'C', Q(14, q), [row], 'bio-2-4', concept, at(10, 15, '(a)', f'({r})'), total,
      stem=[Q15A], fig='q15-eye', labels=labs)
    for r, q, row, concept, total, labs in [
        ('ii', 'What is the function of the iris in the eye?', pt(S('To control the amount of light entering the eye'), 3),
         'iris', 3, None),
        ('iii', 'In what labelled part would you find the rods and cones?', pt(S('B or retina'), 3), 'rods-and-cones', 3,
         None),
        ('iv', 'Give the precise function of the rods in the eye.', pt(S('Monochrome vision or work in dim light'), 3),
         'rods', 3, None),
        ('v', 'To which organ does part A connect the eye?', pt(S('Brain'), 3), 'optic-nerve-to-brain', 3,
         labels(EYE[0], 'ABC', EYE[1], 10)),
        ('vi', 'Name a part of the ear that has a similar function to part B of the eye.',
         pt(S('Cochlea or semicircular canals'), 3), 'ear-receptors', 3, labels(EYE[0], 'ABC', EYE[1], 10)),
        ('vii', 'Name two other sense organs.', anyn(S('e.g. Tongue/ nose/ skin'), 2, 3, open_list=True), 'sense-organs',
         6, None)]
] + [
    T(f'15bi-{x.lower()}', 'Q15(b)(i)', 'C', Q(14, 'Name the blood vessels labelled A, B, C.'),
      [pt(cell(VESSELS[0], i, VESSELS[1]), 3)], 'bio-2-6', concept, at(10, 15, '(b)', '(i)'), 3, stem=[Q15B],
      fig='q15-vessels', item=(x.lower(), x), labels=labels(VESSELS[0], 'ABC', VESSELS[1], 10, asked=x),
      decision=EACH_ITEM)
    for i, (x, concept) in enumerate([('A', 'artery'), ('B', 'vein'), ('C', 'capillary')])
] + [
    T(f'15bii{n}', f'Q15(b)(ii){n}', 'C', [M(f'{n}.', 14), Q(14, q)], [row], 'bio-2-6', concept, SQ(10, sq, sq), 3,
      stem=[Q15B, Q15BII], fig='q15-vessels',
      decision=EACH_ITEM + ' "(5 pts)" over the five numbered statements. ' + OUT_OF_ORDER + ' Each answer shares '
               'its reprint\'s line, so it is read from after the lungs labels, the line printed before them.')
    for n, q, row, concept, sq in [
        (1, 'Carries blood towards the heart.', pt(S('Carries blood towards heart: B or vein', after=VESSEL_ROWS), 3),
         'veins-carry-blood-to-the-heart', '1. Carries blood towards heart:'),
        (2, 'Contains valves.', pt(S('Contains valves: B or vein', after=VESSEL_ROWS), 3), 'veins-have-valves',
         '2. Contains valves:'),
        (3, 'Brings blood to the heart muscle.',
         pt(S(BLOOD_TO_HEART_MUSCLE, piece=1, psep=' [', after=VESSEL_ROWS), 3,
            note_sel=S(BLOOD_TO_HEART_MUSCLE, piece=[2, 1], psep=[' [', ']'], after=VESSEL_ROWS)),
         'coronary-artery', '3. Brings blood to heart muscle:'),
        (4, 'Has a pulse.', pt(S('Has a pulse: A or artery', after=VESSEL_ROWS), 3), 'arteries-have-a-pulse',
         '4. Has a pulse:'),
        (5, 'Delivers substances to cells.', pt(S('Delivers substances to cells: C or capillary', after=VESSEL_ROWS), 3),
         'capillaries-exchange-substances', '5. Delivers substances to cells:')]
] + [
    T('15biii', 'Q15(b)(iii)', 'C', Q(14, 'Suggest two ways to keep our circulatory system healthy.'),
      [anyn(S('e.g. Exercise/ do not smoke/ low-fat diet'), 2, 3, open_list=True)], 'bio-2-6',
      'healthy-circulatory-system', rq(10, 'Keep circulatory system healthy by:'), 6, stem=[Q15B], fig='q15-vessels',
      decision=OUT_OF_ORDER),
    T('15ci', 'Q15(c)(i)', 'C', Q(15, 'What other gas is excreted from the lungs with carbon dioxide?'),
      [pt(S('Water'), 3)], 'bio-2-6', 'water-vapour-excreted', at(10, 15, '(c)', '(i)'), 3, stem=[Q15C]),
    T('15cii', 'Q15(c)(ii)', 'C', Q(15, 'Draw a labelled diagram to show the structure of the human lungs.'),
      [pt(S('Trachea, lung outline, bronchus, bronchiole or alveolus'), 6, kind='criterion',
          note_sel=S('6, 3, 0'), note_lead='The scheme marks the diagram'),
       anyn(S('Lung/ trachea/ bronchus/ bronchiole/ alveolus'), 3, 2)], 'bio-2-6', 'drawing-the-lungs',
      rq(10, 'Diagram lungs:'), 12, stem=[Q15C],
      decision='The diagram ("6, 3, 0": one criterion row naming what it must show) and its labels ("3(2)") are '
               'priced on their own, as the scheme\'s "3 + 6 + 3(2) + 5(3)" sets out for (c). ' + OUT_OF_ORDER),
    T('15ciii', 'Q15(c)(iii)', 'C', Q(15, 'What is the function of the diaphragm in the human breathing system?'),
      [pt(S('To help vary the thoracic volume'), 3)], 'bio-2-6', 'diaphragm', at(10, 15, '(c)', '(iii)'), 3,
      stem=[Q15C]),
    T('15civ', 'Q15(c)(iv)', 'C', Q(15, 'Are the intercostal muscles (in the ribcage) relaxing or contracting when a person is',
                                    'inhaling (breathing in)?'),
      [pt(S('Contracting'), 3)], 'bio-2-6', 'intercostals-in-inhalation', at(10, 15, '(c)', '(iv)'), 3, stem=[Q15C]),
    T('15cv', 'Q15(c)(v)', 'C', Q15CV, [pt(S('e.g. Asthma or bronchitis'), 3)], 'bio-2-6', 'breathing-disorder',
      at(10, 15, '(c)', '(v)'), 3, stem=[Q15C]),
    T('15cvi', 'Q15(c)(vi)', 'C', Q(15, 'Give one possible cause and one possible treatment of the disorder.'),
      [pt(S('Possible cause of disorder: Must match disorder', after='+ 5(3)'), 3, kind='criterion', note=NO_ANSWER),
       pt(S('Possible treatment: Must match disorder'), 3, kind='criterion', note=NO_ANSWER)], 'bio-2-6',
      'cause-and-treatment-of-a-breathing-disorder', rq(10, 'Possible cause of disorder:'), 6,
      stem=[Q15C, M('(v)', 15), Q15CV],
      decision='A cause and a treatment, a point each (2 pts): a criterion row each. ' + OUT_OF_ORDER + ' The cause '
               'shares its reprint\'s line, so it is read from after the scheme\'s "+ 5(3)", the line printed '
               'before it.'),
]

# Section C (b) and (c) of Q10-Q13 are fixed points beside their question's
# "7 + 2(1)" ladder: their units count to it as fixed, their cards keep their
# own marks.
LADDER_EXEMPT = {t['key'] for t in TASKS if t['sec'] == 'C' and parse_ref(t['ref'])[0] in (10, 11, 12, 13)
                 and parse_ref(t['ref'])[1] in ('b', 'c')}

FIGURES = {
    # key suffix: (doc, page, rect in PDF points, credit, letters, alt, solution)
    'q2-key': ('paper', 2, (36, 320, 560, 780), SEC, ['A', 'B', 'C', 'D', 'E'], 'Question 2 as printed: the instruction, then five line drawings lettered A to E (A a long thin body looped over itself; B a winged insect seen from above; C a flat, elongated body with two dots at its front end; D a long segmented body with many legs along it; E a coiled shell with a soft body and tentacles beneath it), and below them the key in three columns, Key, Organism and Letter: 1. Animal has a shell, Helix; Animal does not have a shell, Go to 2. 2. Animal has legs, Go to 3; Animal does not have legs, Go to 4. 3. Animal has three pairs of legs, Musca; Animal has more than three pairs of legs, Chilopod. 4. Animal has long cylindrical body, Nematode; Animal has flat body with two eye spots, Planarian. Each organism has a blank line for its letter.', False),
    'q3-table': ('paper', 3, (36, 40, 560, 322), SEC, [], 'Question 3 as printed: the instruction, then the list Genetic engineering (struck through), Plasmid, Isolation, Weed-killer resistance, Insulin, Enzyme above a two-column table: Column A lists "Manipulation of genes" (answered Genetic engineering in Column B as the example) and parts (a) to (e); Column B is blank beside them.', False),
    'q4-digestive': ('paper', 3, (108, 361, 458, 516), SEC, ['A', 'B', 'C'], 'Drawing of part of the human digestive system: a large lobed organ at the top left with the gall bladder, labelled, tucked beneath it; a J-shaped bag-like organ on the right, joined to a tube at its top and opening into a curved tube at the lower left; and a lumpy organ lying along the curve below the bag. A points to the large lobed organ, B to the bag-like organ, C to the lumpy organ below it.', False),
    'q6-rhizopus': ('paper', 4, (206, 378, 392, 512), SEC, ['A', 'B', 'C'], 'Line drawing of part of Rhizopus: thread-like strands spread out sideways from one point, branched root-like strands grow down from that point, and upright stalks rise from it, two of them topped by a dark round head. A points to one of the sideways strands, B to the branched strands below, C to one of the dark round heads.', False),
    'q7-stems': ('paper', 5, (130, 545, 468, 700), SEC, ['A', 'B'], 'Two transverse sections, lettered A and B. A: a wide ring of cells around a small central core shaped like a cross, with small round patches between its arms. B: a single circle with about a dozen small dark patches spaced evenly in a ring just inside its edge and an empty centre.', False),
    'q8-flasks': ('paper', 6, (100, 125, 420, 306), SEC, ['A', 'B'], 'Apparatus: two conical flasks, A and B, standing in a labelled water bath, each partly filled with liquid and closed by a stopper carrying a U-shaped tube with two bulbs, the right-hand one labelled Fermentation lock. A thermometer stands in the water bath at the left. A label reading CO2 Bubbles points to bubbles in the liquid of the left-hand lock, above flask A; the lock above flask B shows none.', False),
    'q10-division': ('paper', 8, (198, 256, 380, 380), SEC, ['A', 'B'], 'Drawing of a dividing cell: an oval cell with a small star-shaped body at its top and at its bottom and fine lines running from each to a row of four curved, thread-like bodies, one row in the upper half and one in the lower half. A points to one of the upper thread-like bodies, B to the fine lines in the lower half.', False),
    'q12-female': ('paper', 10, (75, 145, 312, 332), SEC, ['A', 'B', 'C', 'D', 'E'], 'Front view of the human female reproductive system: a central chamber with thick walls narrowing into a canal at the bottom, and from each side of its top a tube curving out and down towards a round body. A points into the canal at the bottom, B to the thick wall of the central chamber, C to the round body on the left, D to the tube on the right, E to the inner lining of the central chamber.', False),
    'q13-reflex': ('paper', 11, (190, 196, 408, 345), SEC, ['A', 'B', 'C'], 'Diagram of the nerve cells of a reflex arc beside a cross-section of the spinal cord, whose central region is shaded dark grey: a long fibre runs in from the left, through a swelling holding a small oval, into the grey region; a short nerve cell lies inside the grey region; a second long fibre runs from the grey region back out and down to a block of muscle at the lower left. A points to the fibre coming in from the left, B to the short nerve cell in the grey region, C to the fibre running down to the muscle.', False),
    'q13-brain': ('paper', 11, (42, 606, 260, 781), SEC, ['A', 'B', 'C'], 'Section through the human brain, cut down the middle: a large, deeply folded upper part, a stalk running down from its base, and a smaller rounded part with fine branching inside it, behind the stalk. A points to the large folded part, B to the stalk, C to the smaller rounded part. An unlabelled leader line also points into the middle of the brain.', False),
    'q14-mitochondrion': ('paper', 12, (178, 242, 318, 316), SEC, [], 'Drawing of a sausage-shaped cell structure cut open lengthways: a smooth outer layer and, inside it, an inner layer folded into many finger-like ridges.', False),
    'q14-leaf': ('paper', 12, (190, 416, 350, 595), SEC, ['A', 'B', 'C'], 'Section through a leaf: a row of flat cells along the top and another along the bottom; under the top row a layer of tall cells dotted with small round bodies, then loosely packed rounded cells, also dotted, with air spaces between them. A has two leader lines, to a tall cell and to a rounded cell; B points to a gap in the bottom row; C has two leader lines, to the two small cells on either side of that gap.', False),
    'q15-eye': ('paper', 14, (100, 89, 400, 250), SEC, ['A', 'B', 'C'], 'Section through the human eye, front to the left: a round eyeball with an oval body near the front held between two dark bodies, the iris (labelled) in front of it, a dotted layer lining the inside of the back of the eyeball, and a bundle of fibres leaving at the back right. C points to the oval body at the front, B to the layer lining the back of the eyeball, A to the bundle of fibres leaving the back.', False),
    'q15-vessels': ('paper', 14, (96, 428, 552, 608), SEC, ['A', 'B', 'C'], 'Three blood vessels, lettered A, B and C, each with its own printed labels. A: a round vessel with a thick, dotted wall and a narrow centre, labelled Thick muscle and elastic fibres, Thick outer wall and Small lumen. B: a round vessel with a thinner wall and a wide centre, labelled Thinner, less muscular, Thin outer wall and Large lumen. C: a narrow tube built of a single layer of flat cells, labelled Very thin wall (one cell thick) and Tiny lumen.', False),
}
