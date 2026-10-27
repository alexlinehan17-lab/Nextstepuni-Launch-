"""Biology 2011 Ordinary Level — reviewed task ledger, carded from the paper for the first time.

Independent visual sweep (2026-10-25), every page rendered and read:
  * The 2011 paper is one booklet (M43), 16 pages: p1 cover and instructions,
    p2-p4 Section A Questions 1-6, p5-p7 Section B Questions 7-9, p8-p13
    Section C Questions 10-15, p14-p16 "Blank Page". Sections A and B are
    answered on the paper; Section C in an answer book. No acknowledgements
    page: every drawing and the Q11(b) food web carry no credit; the Q11(c)
    passage carries its own "[Adapted from 'Science Spin' Issue 26, January
    2008. By Anthony King.]". Questions 10-13 print their part totals "(9)",
    "(24)", "(27)"; Q14 and Q15 print "(30, 30)".
  * The marking scheme, 16 pages: p1 cover, p2 blank (no text layer), p3
    introduction, cancelled answers, surplus answers and conventions 1-3, p4
    conventions 4-6, p5-p12 Questions 1-15 (one table, printed page numbers
    4-11), p13 blank but for its page number "12", p14 and p15 blank (no text
    layer), p16 back cover (no text layer).

The paper keeps the long-standing shape: any five of Section A's six
questions, any two of Section B's three, any four of Section C's six, and
Questions 14 and 15 are each any two of (a), (b), (c). No Biology card existed
for 2011 Ordinary before this review.

The paper's pages 11, 12 and 13 (Questions 13, 14 and 15) could not be lifted
as read.
Each renders cleanly, but its text layer is set in overlapping vertical
strips: every printed line reaches the text layer as several pieces, one per
strip, and the character at each strip's edge is set in both ("Namme the
liquidd part of thee blood."). bio_review_lib.Src reads those pieces as
separate lines ("Nam", "me the liquid", "d part of the", "e blood."), so no
selector can open or close on a printed line, and PyMuPDF's own search finds
none of the page's sentences either. The census reader reads the same pieces:
it keyed Q13 correctly only by accident, found three of Q14's seventeen asks and
mis-keyed all of Q15, and the page-13 footer "16" (from "Page 13 of 16") filed
as a phantom Question 16. The author brought this to the coordinator, who added
paper.STRIP_SET_PAGES: for these three pages both the census and Src pool every
glyph, keep a glyph set twice at the same place once (strip edges repeat at
0.00-0.06pt; a printed double letter sits 3.3pt or more apart), group by
baseline and read left to right, which rebuilds every printed line. Questions
13-15 are carded from those lines (the section at the end of this file, the
author's draft merged by the coordinator). The heads of Q14 and Q15 print "Answer
any two of (a), (b), (c) (30, 30)" with no full stop after "(c)", so the census
read "(c) (30, 30)" as a part: a gated MISPRINTS entry drops that "(c)". The
scheme's text layer for them (p10-p12) is sound.

This scheme prints no reprint of a question except in Q4 and Q5, where each
answer's letter or term is set at the end of its statement's own line. Every
task is anchored on its part marker, found by walking the scheme's numbering
down to it (SQ path); Q4's walk passes "3" first, because the page number "4"
heads scheme p5.

Tariffs. Section A's ordered splits lead with their largest rate and are
carded at it: Q1, Q3 and Q5 "2(7) + 3(2)" over five answers, Q2 "3(4) +4 (2)",
Q4 and Q6 "3(4) + 4(2)" over seven. Section B: Q7(a) is fixed, "5,2,0
(diagram) + 1 (label)"; Q8(a) and Q9(a) "5+1" and every (b) "2(6)+6(2)" are
ladders carded at their first rate. Section C: Q10(a) and Q12(a) "7+2(1)",
Q10(b) and Q12(b) "2(6) + 6(2)", Q10(c) and Q12(c) "3(5)+6(2)", each a ladder
of its own part carded at its first rate.

Question 11's three notations lead with their SMALLEST rate: (a) "2(1) + 7",
(b) "6(2)+2(6)", (c) "6(2)+3(5)" (scheme p8, rendered and looked at). Read as
the conventions page (p4, rule 4: "the first two correct answers are awarded 4
marks each and each subsequent correct answer is awarded 3 marks") defines an
ordered split, the first correct answers would earn 1 or 2 and the last 7, 6
or 5, where every other ladder of this scheme leads with its largest rate.
No reading prices each printed answer on its own, so each part of Q11 is ONE
card at the paper's printed part total ("(9)", "(24)", "(27)"), every row
unpriced (the coordinator's whole-part rule, as 2012 Ordinary Section A and
2013 Ordinary Section B (a)); no response is carded at a first rate and no
reordering is derived. Brought to the coordinator.

The scheme's text layer reads its quotation marks as U+2018/U+2019, as
printed; nothing in it reads as U+201E/U+201F.

The census reader finds all 142 printed asks, keyed as the paper prints them:
94 in Questions 1-12, and 48 in Questions 13-15 once the strip-set pages are
read as rebuilt lines (above); all are claimed.
"""
from bio_review_lib import Q, SQ, S, M, pt, anyn, T, L

YEAR, LEVEL = 2011, 'ol'
REVIEWED_AT = '2026-10-25'

SOURCES = {
    'paper': {'path': 'examiner-reports/biology/papers/2011-ol-paper.pdf',
              'fileid': 'LC025GLP000EV.pdf',
              'sha256': 'f63cdb6415745ec2a23e86a2148aa407728afa5298828fcb69941618ca9ed9c1',
              'pages': 16},
    'scheme': {'path': 'examiner-reports/biology/schemes/2011-ol.pdf',
               'fileid': 'LC025GLP000EV.pdf',
               'sha256': '6fcb0417a0b2da9ddb97a69c6dcbdd993f249d17c8d3e430cbc5a3bdbff9e61c',
               'pages': 16},
}

PAGE_ROLES = {
    'paper': {1: 'cover', **{p: 'questions' for p in range(2, 14)}, 14: 'blank', 15: 'blank', 16: 'blank'},
    'scheme': {1: 'cover', 2: 'blank', 3: 'introduction', 4: 'conventions',
               **{p: 'marking' for p in range(5, 13)}, 13: 'blank', 14: 'blank', 15: 'blank', 16: 'back-cover'},
}


def _ladder(notation, **extra):
    """An ordered split as the scheme prints it ("2(7) + 3(2)", "5+1")."""
    steps = []
    for term in notation.split('+'):
        n, _, m = term.strip().partition('(')
        steps += [int(m.rstrip(')'))] * int(n) if m else [int(n)]
    return {'steps': steps, 'notation': notation, **extra}


QUESTION_TOTALS = {
    **{n: 20 for n in range(1, 7)}, **{n: 30 for n in range(7, 10)},
    10: 60, 11: 60, 12: 60,
}
PART_TOTALS = {
    (7, 'a'): 6,   # paper p5: "Part (a) carries 6 marks"; the scheme's "5,2,0 (diagram) + 1 (label)"
    (11, 'a'): 9, (11, 'b'): 24, (11, 'c'): 27,   # the paper's "(9)", "(24)", "(27)": whole-part cards
}
LADDERS = {
    1: _ladder('2(7) + 3(2)'), 2: _ladder('3(4) +4 (2)'), 3: _ladder('2(7) + 3(2)'),
    4: _ladder('3(4) + 4(2)'), 5: _ladder('2(7) + 3(2)'), 6: _ladder('3(4) + 4(2)'),
    # Q7(a) "5,2,0 (diagram) + 1 (label)" is fixed, beside (b)'s ladder.
    (7, 'b'): _ladder('2(6)+6(2)'),
    (8, 'a'): _ladder('5+1'), (8, 'b'): _ladder('2(6) + 6(2)'),
    (9, 'a'): _ladder('5+1'), (9, 'b'): _ladder('2(6)+6(2)'),
    (10, 'a'): _ladder('7+2(1)'), (10, 'b'): _ladder('2(6) + 6(2)'), (10, 'c'): _ladder('3(5)+6(2)'),
    (12, 'a'): _ladder('7 + 2(1)'), (12, 'b'): _ladder('2(6) + 6(2)'), (12, 'c'): _ladder('3(5)+6(2)'),
}

# The scheme's answer and point counts ("(3 Pts)", "2(Pts)"), as mark units:
# each response at its ladder's first rate, Q7(a)'s drawing as printed.
CHECKSUMS = {
    1: {7: 5}, 2: {4: 7}, 3: {7: 5}, 4: {4: 7}, 5: {7: 5}, 6: {4: 7},
    (7, 'a'): {5: 1, 1: 1}, (7, 'b'): {6: 8},
    (8, 'a'): {5: 2}, (8, 'b'): {6: 8},
    (9, 'a'): {5: 2}, (9, 'b'): {6: 8},
    (10, 'a'): {7: 3}, (10, 'b'): {6: 8}, (10, 'c'): {5: 9},
    (12, 'a'): {7: 3}, (12, 'b'): {6: 8}, (12, 'c'): {5: 9},
}

# Pages 11-13 (Questions 13-15) are left out: their text layer is set in
# strips (see the docstring), so a scan of them reads fragments, and none of
# their asks is carded yet.
SCAN_PAGES = {'paper': range(1, 14)}
SELECTION_SCAN = [
    ('paper', 1, 'any five', 'Cover rubric, Section A: whole-question choice; every question is carded.'),
    ('paper', 1, 'any two', 'Cover rubric, Section B: whole-question choice; every question is carded.'),
    ('paper', 1, 'any four', 'Cover rubric, Section C: whole-question choice; every question is carded.'),
    ('paper', 2, 'any five', 'Section A rubric repeated.'),
    ('paper', 2, 'the following', 'Q1 lead-in: every part asked, one card per roman.'),
    ('paper', 3, 'both', 'Q3(d) "in both plants and animals": description.'),
    ('paper', 3, 'the following', 'Q4 lead-in: every statement asked, one card per letter.'),
    ('paper', 3, 'or', 'Q4 "true (T) or false (F)": the answer options.'),
    ('paper', 3, 'or', 'Q4 "T or F": the answer options.'),
    ('paper', 4, 'choose', 'Q5 "Choose each term": every description matched, one card per roman.'),
    ('paper', 4, 'the following', 'Q5 list of terms: the options.'),
    ('paper', 5, 'any two', 'Section B rubric repeated.'),
    ('paper', 5, 'the following', 'Q7(b) lead-in: every part asked.'),
    ('paper', 6, 'the following', 'Q8(b) lead-in: every item asked, one card per roman.'),
    ('paper', 6, 'or', 'Q8(b)(i) "Fehling\'s solution or Benedict\'s solution": a reagent the candidate chooses; the '
                       'scheme prices one purpose for both, so no route.'),
    ('paper', 7, 'the following', 'Q9(b) lead-in: every part asked.'),
    ('paper', 8, 'any four', 'Section C rubric repeated.'),
    ('paper', 8, 'the following', 'Q10(a) lead-in: every term asked, one card per roman.'),
    ('paper', 8, 'or', 'Q10(b)(iii) "Using a Punnett square or another method": a method the candidate chooses; the '
                       'scheme prices the offspring alike, so no route.'),
    ('paper', 8, 'choose', 'Q10(c)(iii) "Some people choose to be screened": description.'),
    ('paper', 8, 'the following', 'Q10(c)(v) "The following are the results": the printed profile, the card\'s figure.'),
    ('paper', 8, 'or', 'Q10(c)(v) "A, B or C": the answer options.'),
    ('paper', 9, 'the following', 'Q11(a)(ii) "Explain the following terms": both terms asked, rows of the (a) card.'),
    ('paper', 9, 'or', 'Q11(c) passage "or they may fall prey to the domestic cat": passage text.'),
    ('paper', 10, 'any two', 'Q12(b)(iii)1 "Name any two environmental factors": one menu, claim two.'),
    ('paper', 10, 'both', 'Q12(c) lead-in "in both plants and animals": description.'),
    ('paper', 10, 'any one', 'Q12(c)(ii) "Name any one enzyme, and its substrate, and its product": the scheme prices '
                             'any enzyme with its matching substrate and product (criterion rows).'),
    ('paper', 10, 'any two', 'Q12(c)(iii) "Name any two factors": the scheme prints exactly two, a row each.'),
    ('paper', 11, 'any two', 'Q13(a)(ii) "Name any two of these factors": a menu, claim two.'),
    ('paper', 11, 'or', 'Q13(b)(ii) "towards or away from the heart": the answer options.'),
    ('paper', 11, 'any two', 'Q13(b)(vii) "Give any two functions of the lymphatic system": a menu, claim two.'),
    ('paper', 12, 'any two', 'Q14 head "Answer any two of (a), (b), (c)": part choice; every part is carded.'),
    ('paper', 12, 'the following', 'Q14(a)(ii) lead-in: both events asked.'),
    ('paper', 12, 'any one', 'Q14(b)(ii) "Name any one hormone": the scheme prices any human hormone (a criterion '
                             'row).'),
    ('paper', 13, 'any two', 'Q15 head "Answer any two of (a), (b), (c)": part choice; every part is carded.'),
    ('paper', 13, 'any two', 'Q15(a)(v) "Name any two methods of artificially propagating plants": a menu, claim '
                             'two.'),
    ('paper', 13, 'or', 'Q15(b)(v) "monocotyledonous or dicotyledonous": description.'),
    ('paper', 13, 'any one', 'Q15(b)(v) "Give any one difference": a menu of the scheme\'s differences, claim one.'),
]

ROUTES = {}

SEC = 'State Examinations Commission'
NO_REPRINT = 'The scheme prints no reprint of this question: anchored on the part\'s own marker.'
ON_ITS_LINE = ('The scheme sets this answer at the end of its reprinted statement\'s own line: anchored on the '
               'part\'s marker and the answer cut from the end of that line at its statement\'s full stop.')
EACH_ITEM = 'A list the scheme prices entry by entry: one card per entry, each its own slice of the printed line.'
NO_ANSWER = 'The scheme prints no answer here, only what earns the marks.'
POINTS = 'The scheme prices this part at {n} points ("{pts}"): each printed point its own row.'
MENU = '{n} ("{pts}") from the printed list: one menu, claim {claim}.'
ONE = 'One response of the "{notation}" ladder, any one of the printed alternatives: a menu, claim one.'
LEAD_IN = ('The printed term alone is too short a question to stand, so the card carries the printed lead-in in its '
           'question text.')
WHOLE_11 = ('The scheme prints Q11({x}) as "{notation}" over its {n} points (p8). Read as the conventions page (p4, '
            'rule 4) defines an ordered split, the first correct answers would earn {low} and the last {high}: the '
            'notation leads with its smallest rate, where every other ladder of this scheme leads with its largest, '
            'and no reading prices each printed answer on its own. So the part is one card at the paper\'s printed '
            '"({total})", every row unpriced (the coordinator\'s whole-part rule, as 2012 Ordinary Section A); no '
            'response is carded at a first rate and no reordering is derived. Each row carries the scheme\'s own '
            'printed part marker or label. Brought to the coordinator.')


def at(page, *path_and_marker, why=NO_REPRINT, nth=1):
    """The part's own marker under its printed question (and letter) lines on the scheme page."""
    *path, marker = path_and_marker
    return SQ(page, marker, path=path, paired=why, bare=True, nth=nth)


def ask(page, sentence, **kw):
    """A one-line ask closed by its own punctuation."""
    return Q(page, sentence, sentence, **kw)


def eg(start, end=None, **kw):
    """A scheme answer printed after its "e.g.": the list itself, cut after the scheme's own "e.g."."""
    return S(start, end, piece=2, psep='e.g. ', **kw)


def tail(line, page=None):
    """The answer the scheme sets at the end of its reprinted statement ("... balance. T"), cut at the
    statement's own full stop."""
    return S(line, page=page, piece=2, psep='. ')


# ------------------------------------------------------------ question text --
Q1 = Q(2, 'Use your knowledge of nutrition to answer the following questions:')
Q3 = Q(3, 'The diagram shows a cell undergoing cell division.')
Q4 = Q(3, 'Indicate whether each of the following statements is true (T) or false (F) by drawing a circle',
       'around T or F in each case.')
Q5 = [Q(4, 'Choose each term from the following list and place it in Column B to match a description in',
        'Column A. The first one has been completed as an example.'),
      Q(4, 'Alcohol, Oxygen, Water, Mitochondria, Lactic acid, Large')]
Q6 = Q(4, 'The diagram shows a vertical section through the human eye.')
Q6A = ask(4, 'Name the parts labelled A, B, C.')
Q7B = Q(5, 'Answer the following questions in relation to your investigation into the growth of leaf', 'yeast.')
Q8A = Q(6, 'The scientific method involves making a hypothesis, carrying out experiments,',
        'recording results, and forming conclusions.')
Q8B = Q(6, 'For what purpose did you use each of the following in the course of your practical', 'activities?')
Q9A = ask(7, 'Name the parts of the light microscope labelled A and B.')
Q9B = Q(7, 'Answer the following questions in relation to obtaining and staining a sample of plant',
        'cells and viewing them under the microscope.')
Q10A = Q(8, 'Explain the following terms that are used in genetics:')
Q10B = Q(8, 'In humans, brown eye (B) is dominant to blue eye (b). Two parents, one heterozygous for',
         'eye colour and the other with blue eyes, start a family.')
Q10CIV = Q(8, 'Blood samples taken from a crime scene were put through a process called DNA',
           'which was then cut into fragments. The fragments were then separated.')
Q11B = Q(9, 'The food web below was drawn by a group of students following their field work.',
         'Study the web and answer the questions.')
Q11C = [Q(9, 'Read the paragraph below and answer the questions that follow.'),
        Q(9, 'Shedding Daylight on Irish Bats.', 'to loss of hedgerows, pesticide use and the renovation of old buildings.'),
        Q(9, '[Adapted from ‘Science Spin’ Issue 26, January 2008. By Anthony King.]')]
Q12BIII = Q(10, 'The apparatus shown below may be used to investigate the effect of an',
            'environmental factor on the rate of photosynthesis.')
Q12C = Q(10, 'Enzymes are used in many processes in both plants and animals.')

# ------------------------------------------------------- scheme cell lines --
PROTEIN = ('(Lean) Meat / Fish / Cheese / Eggs / Pulses (Do not accept', 'Dairy Products)')
POLLUTION = 'Any harmful addition to the ecosystem (e.g. not acceptable)'
PROBLEM1 = 'e.g. Finding land for landfill sites'
PROBLEM2 = 'e.g. Litter / pollution or named form of pollution .'
REUSE = 'Reuse / Recycle … (or explained) (e.g. acceptable)'
CHROMOSOME = 'Chromosome (allow chromatid) (Do not allow DNA)'
ORGANS = 'Leaf / Root / Stem / Bud / Tuber / Flower/ bulbs/ Rhizome …'
STATEMENTS = {
    'a': 'The semicircular canals in the ear are involved in balance. T',
    'b': 'Growth response of a plant to light is phototropism. T',
    'c': 'Tendons attach bone to bone. F',
    'd': 'A motor neuron carries impulses to the brain. F',
    'e': 'Rhizopus is a member of the animal kingdom. F',
    'f': 'Xylem transports water in plants. T',
    'g': 'A potato is a modified stem. T',
}
TERMS = {
    'i': 'A substance required for aerobic respiration. Oxygen',
    'ii': 'A product of anaerobic respiration in muscles. Lactic Acid',
    'iii': 'A product of aerobic respiration. Water',
    'iv': 'A product of anaerobic respiration in yeast. Alcohol',
    'v': 'The cell structures in which Stage 2 occurs. Mitochondria',
}
EYE = {'A': 'A = Optic Nerve', 'B': 'B = Retina', 'C': 'C = Lens'}
YEAST_DIAGRAM = 'Suitable diagram of cell showing nucleus and bud = 5 marks'
VALID_PLANT = 'Any valid plant e.g. Ash / Privet …'
LEAF_STEPS = ('Leaf (or leaf section) stuck to lid / tweezers / stuck with what /of',
              'Petri dish / Yeast-side down / dish left agar-side down / 24 hours.')
STAIN = 'To stain (animal/plant) cells / nucleic acids'
MICROSCOPE = {'A': 'Eyepiece or Eye lens', 'B': 'Platform or Stage'}
SECTION_STEPS = ('Cut or peel /with what / onto slide / into water /safety point / stain /',
                 'cover slip / detail on cover slip')
ALLELE = 'Allele – alternative form of a gene'
HETEROZYGOUS = 'Heterozygous–two alleles / Tt (2 genes not acceptable)'
PHENOTYPE = 'Phenotype – genotype expressed / genotype +environment'
ONE_PARENT = 'One Parent – (B) / (b)'
OTHER_PARENT = 'Other Parent - (b)'
PUNNETT_NOTE = S('Allow non-matching when vague i.e. genotypes are', 'two types of gametes etc, allow no marks')
CAUSES = 'Any two causes e.g. Radiation / Smoking …'
HERBIVORE = 'Herbivore: Caterpillar / Mouse / Greenfly'
CARNIVORE = 'Carnivore: Hawk / Spider / Ladybird'
APPARATUS = 'Pooter / Beating tray / Pitfall trap / Net…'
BAT_HELP = ('Maintain hedgerows/cut use of pestcides/don’t refurbish/education/', 'bat boxes/don’t kill bats')
EQUATION = '6CO2 + 6H2O C6H12O6 + 6O2'
EQUATION_MARKING = S('Balancing correct = 1 point… any mistake = 0',
                     'Chemicals correct = 2pts.. 1 mistake = 1pt.. 2 mistakes = 0')
CATALYST = 'A biological (or organic or protein) / catalyst'


def cell_labels(asked=None):
    # The scheme names A ("Chromosome ...") and never names B, whose function (b) asks.
    return [L('A', S(CHROMOSOME, page=5, piece=1, psep=' ('), asked == 'A')]


def eye_labels(asked=None):
    return [L(x, S(EYE[x], page=5, piece=2, psep=' = '), x == asked) for x in 'ABC']


def microscope_labels(asked=None):
    return [L(x, S(MICROSCOPE[x], page=6), x == asked) for x in 'AB']


TASKS = [
    # ------------------------------------------------------------ Section A --
] + [
    T(f'1{r}', f'Q1({r})', 'A', q, [row], 'bio-1-2', concept, at(5, '1', f'({r})'), 7, stem=[Q1],
      decision=decision)
    for r, q, row, concept, decision in [
        ('i', Q(2, 'Carbohydrates always contain the elements carbon, hydrogen and'), pt(S('Oxygen'), 7),
         'elements-in-carbohydrates', ''),
        ('ii', Q(2, 'Lipids are made up of fatty acids and'), pt(S('Glycerol'), 7), 'lipids-and-glycerol', ''),
        ('iii', ask(2, 'Name a fat-soluble vitamin.'), anyn(S('A / D / E / K'), 1, 7), 'fat-soluble-vitamins',
         ONE.format(notation='2(7) + 3(2)')),
        ('iv', ask(2, 'Name a structural carbohydrate found in plants.'), pt(S('Cellulose'), 7),
         'structural-carbohydrate', ''),
        ('v', ask(2, 'Name one good source of protein in the human diet.'),
         anyn(S(*PROTEIN, piece=1, psep=' ('), 1, 7, note_sel=S(*PROTEIN, piece=[2, 1], psep=[' (', ')'])),
         'sources-of-protein', ONE.format(notation='2(7) + 3(2)') + ' The list is cut before its bracketed '
                                                                    'direction, which is the row\'s note.')]
] + [
    T(f'2{r}', f'Q2({r})', 'A', q, [row], 'bio-3-1', concept, at(5, '2', f'({r})'), total, decision=decision)
    for r, q, row, concept, total, decision in [
        ('i', ask(2, 'What is meant by pollution?'),
         pt(S(POLLUTION, piece=1, psep=' (e.g.'), 4, note_sel=S(POLLUTION, piece=[2, 1], psep=[' (', ')'])),
         'pollution', 4, 'The scheme\'s bracketed "(e.g. not acceptable)" is the row\'s note.'),
        ('ii', ask(2, 'Name one human activity that causes pollution.'),
         pt(S('Any relevant activity but not naturally occurring catastrophe'), 4, kind='criterion', note=NO_ANSWER),
         'human-causes-of-pollution', 4, 'The scheme prices an activity without naming one: a criterion row.'),
        ('iii', ask(2, 'State two problems associated with waste disposal in Ireland.'),
         anyn(None, 2, 4, open_list=True,
              options=[eg(PROBLEM1), S(PROBLEM2, piece=[2, 1], psep=['e.g. ', ' / ']),
                       S(PROBLEM2, piece=[2, 2, 1], psep=['e.g. ', ' / ', ' .'])]),
         'problems-of-waste-disposal', 8,
         MENU.format(n='Two responses', pts='3(4) +4 (2)', claim='two') + ' The scheme numbers two examples, '
         '"1. e.g. Finding land for landfill sites" and "2. e.g. Litter / pollution or named form of pollution .": '
         'each option a slice after its own "e.g.", the second line cut at its solidus.'),
        ('iv', ask(2, 'List two ways of minimising waste.'),
         anyn(None, 2, 4, open_list=True,
              options=[S('Reduce'), S(REUSE, piece=1, psep=' / '), S(REUSE, piece=[2, 1], psep=[' / ', ' …'])],
              note_sel=S(REUSE, piece=[2, 2], psep=[' / ', '… '])),
         'minimising-waste', 8,
         MENU.format(n='Two responses', pts='3(4) +4 (2)', claim='two') + ' The scheme numbers "1. Reduce" and '
         '"2. Reuse / Recycle … (or explained) (e.g. acceptable)": its ellipsis leaves the list open and its '
         'brackets are the row\'s note.'),
        ('v', ask(2, 'Give one example of the use of microorganisms in waste management.'),
         anyn(eg('e.g. Breaks down waste / in sewage treatment plants'), 1, 4, open_list=True),
         'microorganisms-in-waste-management', 4,
         ONE.format(notation='3(4) +4 (2)') + ' Printed after "e.g.": an open menu.')]
] + [
    T(f'3{x}', f'Q3({x})', 'A', ask(3, q), [row], topic, concept, at(5, '3', f'({x})'), 7,
      stem=[Q3] if fig else [], fig='q3-cell' if fig else None, labels=cell_labels('A' if x == 'a' else None)
      if fig else None, decision=decision)
    for x, q, row, topic, concept, fig, decision in [
        ('a', 'Genes are found on structure A. Name structure A.',
         pt(S(CHROMOSOME, piece=1, psep=' ('), 7, note_sel=S(CHROMOSOME, piece=2, psep='Chromosome ')),
         'bio-2-3', 'chromosome', True, 'The scheme\'s two bracketed directions are the row\'s note.'),
        ('b', 'What is the function of structure B?',
         anyn(S('To contract / to separate chromosomes / chromatid / to attach'), 1, 7), 'bio-2-3', 'spindle-fibres',
         True, ONE.format(notation='2(7) + 3(2)') + ' Cut at the scheme\'s own solidus (its "chromatid" is a piece of '
                                                    'its own). The scheme never names B, so the label key carries A '
                                                    'only.'),
        ('c', 'Tissues grow by cell division. Name the type of cell division by which tissues grow.',
         pt(S('Mitosis'), 7), 'bio-2-3', 'mitosis-and-growth', False, ''),
        ('d', 'Organs are found in both plants and animals. What is meant by the term organ?',
         anyn(S('A group of tissues / Structure composed of two or more tissues'), 1, 7), 'bio-1-3', 'organ', False,
         ONE.format(notation='2(7) + 3(2)')),
        ('e', 'Name one organ found in plants.', anyn(S(ORGANS, piece=1, psep=' …'), 1, 7, open_list=True),
         'bio-1-3', 'plant-organs', False,
         ONE.format(notation='2(7) + 3(2)') + ' The scheme closes the list with "…": open, the ellipsis cut off.')]
] + [
    T(f'4{x}', f'Q4({x})', 'A', ask(3, q), [pt(tail(STATEMENTS[x]), 4)], topic, concept,
      at(5, '3', '4', f'({x})', why=ON_ITS_LINE), 4, stem=[Q4])
    for x, q, topic, concept in [
        ('a', 'The semicircular canals in the ear are involved in balance.', 'bio-2-4', 'semicircular-canals'),
        ('b', 'The growth response of a plant to light is called phototropism.', 'bio-2-4', 'phototropism'),
        ('c', 'Tendons attach bone to bone.', 'bio-2-4', 'tendons'),
        ('d', 'A motor neuron carries impulses to the brain.', 'bio-2-4', 'motor-neuron'),
        ('e', 'Rhizopus is a member of the animal kingdom.', 'bio-3-2', 'rhizopus-kingdom'),
        ('f', 'Xylem transports water in plants.', 'bio-2-6', 'xylem-transports-water'),
        ('g', 'A potato is a modified stem.', 'bio-2-6', 'potato')]
] + [
    T(f'5{r}', f'Q5({r})', 'A', q, [pt(tail(TERMS[r]), 7)], 'bio-2-2', concept, at(5, '5', f'({r})', why=ON_ITS_LINE),
      7, stem=Q5, qfig='q5-table',
      decision='The list of terms (its "Large" struck through as the worked example) and the table are shown as the '
               'question\'s own print.')
    for r, q, concept in [
        ('i', ask(4, 'A substance required for aerobic respiration.'), 'oxygen-for-aerobic-respiration'),
        ('ii', ask(4, 'A product of anaerobic respiration in muscles.'), 'lactic-acid'),
        ('iii', ask(4, 'A product of aerobic respiration.'), 'water-from-aerobic-respiration'),
        ('iv', ask(4, 'A product of anaerobic respiration in yeast.'), 'alcohol-from-yeast'),
        ('v', Q(4, 'The cell structures in which Stage 2 of aerobic', 'respiration takes place.'), 'mitochondria')]
] + [
    T(f'6a-{x.lower()}', 'Q6(a)', 'A', Q6A, [pt(S(EYE[x]), 4)], 'bio-2-4', concept, at(5, '6', '(a)'), 4, stem=[Q6],
      fig='q6-eye', item=(x.lower(), x), labels=eye_labels(x),
      decision=EACH_ITEM + ' Three responses of the "3(4) + 4(2)" ladder, one per label, each printed on its own '
                           'line.')
    for x, concept in [('A', 'optic-nerve'), ('B', 'retina'), ('C', 'lens')]
] + [
    T(f'6{x}', f'Q6({x})', 'A', ask(4, q), [row], 'bio-2-4', concept, at(5, '6', f'({x})'), 4, stem=[Q6],
      fig='q6-eye', labels=eye_labels() if letters else None, decision=decision)
    for x, q, row, concept, letters, decision in [
        ('b', 'Name the coloured part of the eye.', pt(S('Iris'), 4), 'iris', False, ''),
        ('c', 'What is the function of the pupil in the eye?', pt(S('To allow light in'), 4), 'pupil', False, ''),
        ('d', 'In which labelled part would you find the rods and cones?', pt(S('B or retina'), 4),
         'rods-and-cones', True, ''),
        ('e', 'What is the function of the cones?', anyn(S('To detect colour / colour vision / bright light'), 1, 4),
         'cones', False, ONE.format(notation='3(4) + 4(2)'))]
] + [
    # ------------------------------------------------------------ Section B --
    T('7a', 'Q7(a)', 'B', ask(5, 'Draw a labelled diagram of a single, reproducing, yeast cell.'),
      [pt(S(YEAST_DIAGRAM, piece=1, psep=' = '), 5, kind='criterion', note=NO_ANSWER,
          note_sel=S('(If either nucleus or bud is absent then only allow 2 marks - if both',
                     'are missing then allow no marks)')),
       pt(S('+ 1 (label)', piece=[2, 1], psep=['(', ')']), 1, kind='criterion', note=NO_ANSWER)],
      'bio-3-2', 'drawing-a-budding-yeast-cell', at(6, '7', '(a)'), 6,
      decision='The scheme prices the drawing on its own, "5,2,0 (diagram) + 1 (label)", making the rubric\'s 6: the '
               'diagram (5, 2 or 0) one criterion row cut before its printed "= 5 marks", its bracketed banding the '
               'row\'s note, and the label a criterion row of its own, the scheme\'s "(label)" cut out of its '
               'brackets. The scheme names no label.'),
] + [
    T(f'7b{r}', f'Q7(b)({r})', 'B', ask(5, q), rows, 'bio-3-2', concept, at(6, '7', '(b)', f'({r})'), 6 * n,
      stem=[Q7B], decision=decision)
    for r, q, rows, n, concept, decision in [
        ('i', 'From what plant did you obtain the yeast?',
         [anyn(S(VALID_PLANT, piece=[2, 1], psep=['e.g. ', ' …']), 1, 6, open_list=True,
               note_sel=S(VALID_PLANT, piece=1, psep=' e.g.'))], 1, 'source-of-leaf-yeast',
         'One response of the "2(6)+6(2)" ladder: the scheme\'s examples after its "e.g.", an open menu, claim one; '
         'its "Any valid plant" is the row\'s note.'),
        ('ii', 'Name the nutrient medium on which you grew the yeast.', [pt(S('(nutrient) Agar'), 6)], 1,
         'nutrient-agar', ''),
        ('iii', 'Outline the steps you followed to get the yeast cells onto the nutrient medium.',
         [anyn(S(*LEAF_STEPS), 3, 6)], 3, 'getting-leaf-yeast-onto-agar',
         MENU.format(n='Three points', pts='(3 Pts)', claim='three') + ' Cut at the scheme\'s own solidus, as the '
         'conventions page (p4, rule 1) defines it; the scheme sets a solidus between "stuck with what" and "of Petri '
         'dish", so "of Petri dish" is a piece of its own.'),
        ('iv', 'How long did it take for the yeast to become visible on the nutrient medium?',
         [pt(S('≥ 72 hours or 3 days'), 6)], 1, 'time-for-leaf-yeast-to-grow', ''),
        ('v', 'How did you recognise the yeast?', [pt(S('Pink colonies or pink spots'), 6)], 1,
         'recognising-leaf-yeast', ''),
        ('vi', 'Describe one aseptic technique you carried out during this investigation.',
         [anyn(S('Swab bench with disinfectant / sterilise instrument / Petri dish face', 'downwards on bench'), 1, 6)],
         1, 'aseptic-technique', ONE.format(notation='2(6)+6(2)'))]
] + [
    T('8ai', 'Q8(a)(i)', 'B', ask(6, 'Why is it a good idea to repeat an experiment many times?'),
      [anyn(S('To verify results /(statistical) reliability/ minimise error'), 1, 5)], 'bio-u2',
      'repeating-experiments', at(6, '8', '(a)', '(i)'), 5, stem=[Q8A],
      decision='One response of the "5+1" ladder, carded at its first rate: any one of the printed answers, a menu, '
               'claim one.'),
    T('8aii', 'Q8(a)(ii)', 'B', ask(6, 'Why is a control used when carrying out experiments?'),
      [pt(S('To compare (with experiment)'), 5)], 'bio-u2', 'purpose-of-a-control', at(6, '8', '(a)', '(ii)'), 5,
      decision='One response of the "5+1" ladder, carded at its first rate.'),
] + [
    # "IAA." alone is too short a question to stand: its card carries the printed
    # lead-in in its question text.
    T(f'8b{r}', f'Q8(b)({r})', 'B', [Q8B, ask(6, item, br=True)] if len(item) < 8 else ask(6, item), [row], topic,
      concept, at(6, '8', '(b)', f'({r})'), 6, stem=[] if len(item) < 8 else [Q8B],
      decision=(decision + (' ' + LEAD_IN if len(item) < 8 else '')).strip())
    for r, item, row, topic, concept, decision in [
        ('i', 'Fehling’s solution or Benedict’s solution.', anyn(S('To check for Glucose / reducing sugar'), 1, 6),
         'bio-1-2', 'use-of-benedicts', ONE.format(notation='2(6) + 6(2)')),
        ('ii', 'Anaerobic jar.', anyn(S('To see if O2 is necessary for germination / to limit or reduce O2'), 1, 6),
         'bio-2-5', 'anaerobic-jar', ONE.format(notation='2(6) + 6(2)')),
        ('iii', 'Cover slip.', anyn(S('To examine a specimen / to reduce evaporation / to hold specimen',
                                      'in place / to protect lens or microscope'), 1, 6),
         'bio-1-3', 'cover-slip', ONE.format(notation='2(6) + 6(2)')),
        ('iv', 'Buffer solution.', pt(S('To keep pH constant'), 6), 'bio-2-1', 'buffers', ''),
        ('v', 'Methylene blue.',
         anyn(None, 1, 6, options=[S(STAIN, piece=1, psep=' / '), S(STAIN, piece=2, psep=' / ')]), 'bio-1-3',
         'methylene-blue', ONE.format(notation='2(6) + 6(2)') + ' Cut at the scheme\'s spaced solidus, so its '
                                                               '"(animal/plant)" stays whole.'),
        ('vi', 'Sodium alginate.', anyn(S('To immobilise enzymes (or yeast cells) /to make beads'), 1, 6), 'bio-2-1',
         'sodium-alginate', ONE.format(notation='2(6) + 6(2)')),
        ('vii', 'IAA.', anyn(S('(To examine the effect of) growth regulators (on plants) / to',
                               'stimulate plant growth / to inhibit plant growth.'), 1, 6), 'bio-2-4', 'iaa',
         ONE.format(notation='2(6) + 6(2)')),
        ('viii', 'Freezer-cold alcohol.', anyn(S('To bring DNA out of solution / to isolate DNA'), 1, 6), 'bio-1-2',
         'freezer-cold-ethanol', ONE.format(notation='2(6) + 6(2)'))]
] + [
    T(f'9a-{x.lower()}', 'Q9(a)', 'B', Q9A, [pt(S(MICROSCOPE[x]), 5, label=S(x))], 'bio-1-3', concept,
      at(6, '9', '(a)'), 5, fig='q9-microscope', item=(x.lower(), x), labels=microscope_labels(x),
      decision=EACH_ITEM + ' Two responses of the "5+1" ladder, carded at its first rate, each under the scheme\'s own '
                           'letter.')
    for x, concept in [('A', 'eyepiece'), ('B', 'microscope-stage')]
] + [
    T(f'9b{r}', f'Q9(b)({r})', 'B', q, rows, 'bio-1-3', concept, at(6, '9', '(b)', f'({r})'), 6 * n, stem=[Q9B],
      decision=decision)
    for r, q, rows, n, concept, decision in [
        ('i', ask(7, 'From what plant did you obtain the cells?'),
         [pt(S('Any named plant'), 6, kind='criterion', note=NO_ANSWER)], 1, 'plant-for-cell-study',
         'The scheme prices a named plant without naming one: a criterion row.'),
        ('ii', Q(7, 'How did you obtain a thin piece of a sample of the cells and prepare it for', 'examination?'),
         [anyn(S(*SECTION_STEPS), 3, 6, note_sel=S('(At least 1 point ‘HOW’ and 1 point ‘PREPARE)'))], 3,
         'preparing-a-plant-cell-slide',
         MENU.format(n='Three points', pts='(3 Pts)', claim='three') + ' Cut at the scheme\'s own solidus; its bold '
                                                                     'direction is the row\'s note.'),
        ('iii', ask(7, 'What stain did you use on the cells?'), [pt(S('Iodine solution.'), 6)], 1, 'iodine-stain', ''),
        ('iv', ask(7, 'Describe how you applied the stain.'),
         [anyn(S('With a dropper / under coverslip / method'), 1, 6)], 1, 'applying-the-stain',
         ONE.format(notation='2(6)+6(2)')),
        ('v', Q(7, 'The objective lenses on a microscope are usually labelled 40X, 10X, and 4X.',
                'Which objective lens should you begin with when using the microscope?'),
         [pt(S('4X or Low Power'), 6)], 1, 'starting-objective-lens', ''),
        ('vi', ask(7, 'Give one cell structure that you observed that indicated that the cells were plant cells.'),
         [anyn(S('Cell wall / chloroplast / (large)vacuole'), 1, 6)], 1, 'features-of-plant-cells',
         ONE.format(notation='2(6)+6(2)'))]
] + [
    # ------------------------------------------------------------ Section C --
    # "Allele" alone is too short a question to stand: its card carries the
    # printed lead-in in its question text.
    T(f'10a{r}', f'Q10(a)({r})', 'C', [Q10A, ask(8, term, br=True)] if len(term) < 8 else ask(8, term), [row],
      'bio-1-4', concept, at(7, '10', '(a)', f'({r})'), 7, stem=[] if len(term) < 8 else [Q10A],
      decision=(decision + (' ' + LEAD_IN if len(term) < 8 else '')).strip())
    for r, term, row, concept, decision in [
        ('i', 'Allele', pt(S(ALLELE, piece=2, psep=' – '), 7, label=S(ALLELE, piece=1, psep=' – ')), 'allele',
         'One response of the "7+2(1)" ladder, carded at its first rate; the scheme\'s term is the row\'s label.'),
        ('ii', 'Heterozygous',
         anyn(None, 1, 7, options=[S(HETEROZYGOUS, piece=[2, 1], psep=['–', ' / ']),
                                   S(HETEROZYGOUS, piece=[2, 2, 1], psep=['–', ' / ', ' ('])],
              note_sel=S(HETEROZYGOUS, piece=[2, 2, 2, 1], psep=['–', ' / ', ' (', ')'])), 'heterozygous',
         ONE.format(notation='7+2(1)') + ' Cut after the scheme\'s term at its own solidus; its bracketed direction '
                                         'is the row\'s note.'),
        ('iii', 'Phenotype.', anyn(S(PHENOTYPE, piece=2, psep=' – '), 1, 7), 'phenotype',
         ONE.format(notation='7+2(1)') + ' Cut after the scheme\'s term at its own solidus.')]
] + [
    T('10bi', 'Q10(b)(i)', 'C', ask(8, 'What is the genotype of the blue-eyed parent?'), [pt(S('(bb)'), 6)], 'bio-1-4',
      'genotype-of-blue-eyed-parent', at(7, '10', '(b)', '(i)'), 6, stem=[Q10B]),
    T('10bii', 'Q10(b)(ii)', 'C', ask(8, 'What are the possible gametes that each parent can produce?'),
      [pt(S(ONE_PARENT, piece=[2, k], psep=['– ', ' / ']), 6, label=S(ONE_PARENT, piece=1, psep=' –')) for k in (1, 2)]
      + [pt(S(OTHER_PARENT, piece=2, psep=' - '), 6, label=S(OTHER_PARENT, piece=1, psep=' - '))],
      'bio-1-4', 'gametes-of-each-parent', at(7, '10', '(b)', '(ii)'), 18, stem=[Q10B],
      decision=POINTS.format(n='three', pts='3(Pts)') + ' The scheme prints "One Parent – (B) / (b)" and "Other '
                                                         'Parent - (b)": each gamete a row under its parent\'s label.'),
    T('10biii', 'Q10(b)(iii)', 'C', Q(8, 'Using a Punnett square or another method work out the possible genotypes and',
                                      'phenotypes of their children.'),
      [pt(S('Bb'), 6, note_sel=PUNNETT_NOTE), pt(S('Brown'), 6), pt(S('bb'), 6), pt(S('Blue'), 6)],
      'bio-1-4', 'eye-colour-cross', at(7, '10', '(b)', '(iii)'), 24, stem=[Q10B],
      decision=POINTS.format(n='four', pts='4(Pts)') + ' The scheme answers in a Punnett square: the column gamete "b" '
               'over the row gametes "B" and "b", giving "Bb" "Brown" and "bb" "Blue". Each printed offspring '
               'genotype and phenotype is a row, read cell by cell; the boxed direction printed beside the square is '
               'the first row\'s note.'),
] + [
    T(f'10c{r}', f'Q10(c)({roman}){n}', 'C', q, rows, topic, concept, at(7, '10', '(c)', f'({roman})'), total,
      stem=stem, fig='q10-profile' if r == 'v' else None, decision=decision)
    for r, roman, n, q, rows, topic, concept, total, stem, decision in [
        ('i', 'i', '', ask(8, 'Explain, in terms of what happens to body cells, what is meant by the term cancer.'),
         [pt(S('Control over cell division is lost'), 5)], 'bio-2-3', 'cancer', 5, [], ''),
        ('ii', 'ii', '', ask(8, 'Give two possible causes of cancer.'),
         [anyn(S(CAUSES, piece=[2, 1], psep=['e.g. ', ' …']), 2, 5, open_list=True,
               note_sel=S(CAUSES, piece=1, psep=' e.g.'))], 'bio-2-3', 'causes-of-cancer', 10, [],
         MENU.format(n='Two points', pts='(2 Pts)', claim='two') + ' The scheme\'s examples after its "e.g.", open; '
                                                                   'its "Any two causes" is the row\'s note.'),
        ('iii', 'iii', '', Q(8, 'Some people choose to be screened to determine their risk of getting a particular',
                             'What is meant by genetic screening?'),
         [pt(S('Checking / for presence of specific gene', piece=k), 5) for k in (1, 2)], 'bio-1-4',
         'genetic-screening', 10, [], POINTS.format(n='two', pts='(2 Pts)') + ' Cut at the scheme\'s own solidus.'),
        ('iv1', 'iv', '1', ask(8, '1. What was used to cut the DNA?'), [pt(S('Enzyme'), 5)], 'bio-3-3',
         'enzymes-in-dna-profiling', 5, [Q10CIV],
         EACH_ITEM + ' Each numbered item a point ("3(Pts)" over the three), read after the scheme\'s own number.'),
        ('iv2', 'iv', '2', ask(8, '2. On what basis were the DNA fragments separated?'), [pt(S('Size'), 5)], 'bio-3-3',
         'separating-dna-fragments', 5, [Q10CIV],
         EACH_ITEM + ' Each numbered item a point ("3(Pts)" over the three), read after the scheme\'s own number.'),
        ('iv3', 'iv', '3', ask(8, '3. Give an application of DNA profiling other than solving crime.'),
         [anyn(S('Paternity or maternity / taxonomy / evolution'), 1, 5)], 'bio-3-3',
         'applications-of-dna-profiling', 5, [Q10CIV],
         EACH_ITEM + ' Each numbered item a point ("3(Pts)" over the three); this one any one of the printed '
                     'applications, a menu, claim one.'),
        ('v', 'v', '', Q(8, 'The following are the results of the DNA profiling process. Using these results,',
                         'identify which suspect, A, B or C committed the crime.'),
         [pt(S('B'), 5)], 'bio-3-3', 'reading-a-dna-profile', 5, [], '')]
] + [
    # Question 11: each part one whole card (WHOLE_11 and the docstring).
    T('11a', 'Q11(a)', 'C',
      [M('(i)', 9), ask(9, 'What is the main source of energy in an ecosystem?'),
       M('(ii)', 9, br=True), ask(9, 'Explain the following terms used in ecology:'),
       Q(9, '1. Biosphere', br=True), Q(9, '2. Habitat.', br=True)],
      [pt(S('The Sun'), 0, label=S('(i)'))]
      + [pt(S(line, piece=2, psep=' – '), 0, label=S(line, piece=1, psep=' – '))
         for line in ('1. Biosphere – Everywhere life is possible', '2. Habitat – A place where organism(s) live')],
      'bio-3-1', 'ecosystem-energy-and-terms', at(8, '11', '(a)'), 9, tariff='questionTotal',
      decision=WHOLE_11.format(x='a', notation='2(1) + 7', n='three', low=1, high=7, total=9)
      + ' (ii)\'s two terms each keep the scheme\'s numbered term as their label.'),
    T('11b', 'Q11(b)', 'C',
      [M('(i)', 9), ask(9, 'Name one primary producer from the web.'),
       M('(ii)', 9, br=True), ask(9, 'Name one herbivore and one carnivore from the web.'),
       M('(iii)', 9, br=True), ask(9, 'Name one omnivore from the web.'),
       M('(iv)', 9, br=True), ask(9, 'What would happen to the number of caterpillars if all the thrushes died?'),
       M('(v)', 9, br=True), ask(9, 'What is meant by a quantitative survey of organisms in a habitat?'),
       M('(vi)', 9, br=True), ask(9, 'Name two pieces of apparatus used to collect animals from an ecosystem.')],
      [pt(S('Oak or Blackberry'), 0, label=S('(i)'))]
      + [pt(S(line, piece=[2, k], psep=[': ', ' / ']), 0, label=S(line, piece=1, psep=':'))
         for line in (HERBIVORE, CARNIVORE) for k in (1, 2, 3)]
      + [pt(S('Thrush'), 0, label=S('(iii)')), pt(S('Increase (in number)'), 0, label=S('(iv)')),
         pt(S('A survey in which the number of a particular species/organism is', 'counted'), 0, label=S('(v)'))]
      + [pt(S(APPARATUS, piece=k), 0, label=S('(vi)')) for k in (1, 2, 3)]
      + [pt(S(APPARATUS, piece=[4, 1], psep=['/', '…']), 0, label=S('(vi)'),
            note='The scheme closes this list with "…": it is open.')],
      'bio-3-1', 'food-web-and-surveys', at(8, '11', '(b)'), 24, stem=[Q11B], fig='q11-web', tariff='questionTotal',
      decision=WHOLE_11.format(x='b', notation='6(2)+2(6)', n='eight', low=2, high=6, total=24)
      + ' (ii)\'s herbivores and carnivores are each a row under the scheme\'s own "Herbivore:" and "Carnivore:", cut '
        'at its solidus; (vi)\'s list is cut at its solidus, its closing "…" the last row\'s note.'),
    T('11c', 'Q11(c)', 'C',
      [M('(i)', 9), ask(9, 'How many species of bat are found in Ireland?'),
       M('(ii)', 9, br=True), ask(9, 'What is the name of the most common species found here?'),
       M('(iii)', 9, br=True), ask(9, 'What do bats feed on?'),
       M('(iv)', 9, br=True), ask(9, 'What is meant by the term predator?'),
       M('(v)', 9, br=True), ask(9, 'Name a predator of Irish bats.'),
       M('(vi)', 9, br=True), ask(9, 'Suggest one reason why many bats hibernate in winter.'),
       M('(vii)', 9, br=True), ask(9, 'What is meant by the term conservation?'),
       M('(viii)', 9, br=True), ask(9, 'Suggest one way to help bat conservation in Ireland.')],
      [pt(S('10'), 0, label=S('(i)')), pt(S('Pipistrelle'), 0, label=S('(ii)'))]
      + [pt(S('Moths / Insects', piece=k), 0, label=S('(iii)')) for k in (1, 2)]
      + [pt(S('Organism that kills & eats others (allow kills its prey)'), 0, label=S('(iv)'))]
      + [pt(S('Barn Owl / Cat', piece=k), 0, label=S('(v)')) for k in (1, 2)]
      + [pt(S('To conserve energy or explained / lack of food', piece=k), 0, label=S('(vi)')) for k in (1, 2)]
      + [pt(S('Management of an ecosystem (not natural resource & not protection)'), 0, label=S('(vii)'))]
      + [pt(S(*BAT_HELP, piece=k), 0, label=S('(viii)')) for k in range(1, 7)],
      'bio-3-1', 'bats-in-ireland', at(8, '11', '(c)'), 27, stem=Q11C, tariff='questionTotal',
      decision=WHOLE_11.format(x='c', notation='6(2)+3(5)', n='nine', low=2, high=5, total=27)
      + ' Every printed list is cut at the scheme\'s own solidus, each piece a row under its part\'s marker. The '
        'scheme\'s "pestcides" is lifted as printed.'),
] + [
    T(f'12a{r}', f'Q12(a)({r})', 'C', q, [row], 'bio-2-2', concept, at(9, '12', '(a)', f'({r})'), 7,
      decision=decision)
    for r, q, row, concept, decision in [
        ('i', ask(10, 'What is meant by the term photosynthesis?'),
         pt(S('The method by which plants make their own food'), 7), 'photosynthesis', ''),
        ('ii', Q(10, 'A gas from the air is needed for photosynthesis.', 'Name this gas.'),
         anyn(S('CO2 / water vapour'), 1, 7), 'gas-for-photosynthesis', ONE.format(notation='7 + 2(1)')),
        ('iii', ask(10, 'Name the part of a plant cell in which photosynthesis takes place.'),
         pt(S('Chloroplasts'), 7), 'chloroplast', '')]
] + [
    T('12bi', 'Q12(b)(i)', 'C', ask(10, 'Write a balanced equation for photosynthesis.'),
      [pt(S(EQUATION), 18, units=[6, 6, 6], note_sel=EQUATION_MARKING,
          note='The scheme prints an arrow between 6H2O and C6H12O6, drawn as a line that its text layer does not '
               'carry.')],
      'bio-2-2', 'photosynthesis-equation', at(9, '12', '(b)', '(i)'), 18,
      decision='Three points ("(3 Pts)") of the "2(6) + 6(2)" ladder, carded at its first rate: the scheme prints the '
               'one equation and prices it by its own two criteria printed under it ("Balancing correct = 1 point" '
               'and "Chemicals correct = 2pts"), which are the row\'s note. The text layer flattens the subscripts.'),
    T('12bii', 'Q12(b)(ii)', 'C', Q(10, 'Plants contain the green pigment chlorophyll.',
                                    'What is the role of chlorophyll in photosynthesis?'),
      [anyn(S('To absorb light / to convert light to chemical energy'), 1, 6)], 'bio-2-2', 'role-of-chlorophyll',
      at(9, '12', '(b)', '(ii)'), 6, decision=ONE.format(notation='2(6) + 6(2)')),
    T('12biii1', 'Q12(b)(iii)1', 'C', Q(10, '1. Name any two environmental factors affecting photosynthesis that could be',
                                        'investigated using the apparatus shown.'),
      [anyn(S('CO2 (concentration) / light (intensity) / temperature'), 2, 6)], 'bio-2-2',
      'factors-affecting-photosynthesis', at(9, '12', '(b)', '(iii)'), 12, stem=[Q12BIII], fig='q12-apparatus',
      decision=EACH_ITEM + ' Item 1 is two points ("(2 pts)") from the printed list: a menu, claim two.'),
    T('12biii2', 'Q12(b)(iii)2', 'C', ask(10, '2. How would you measure the rate of photosynthesis using the apparatus below?'),
      [pt(S('(Count) number of bubbles (of O2 ) / per unit time', piece=k), 6) for k in (1, 2)], 'bio-2-2',
      'measuring-the-rate-of-photosynthesis', at(9, '12', '(b)', '(iii)'), 12, stem=[Q12BIII], fig='q12-apparatus',
      decision=EACH_ITEM + ' Item 2 is two points ("(2 Pts)"): cut at the scheme\'s own solidus, a row each.'),
] + [
    T(f'12c{r}', f'Q12(c)({r})', 'C', q, rows, 'bio-2-1', concept, at(9, '12', '(c)', f'({r})'), 5 * n, stem=[Q12C],
      decision=decision)
    for r, q, rows, n, concept, decision in [
        ('i', ask(10, 'What is an enzyme?'), [pt(S(CATALYST, piece=k), 5) for k in (1, 2)], 2, 'enzyme',
         POINTS.format(n='two', pts='(2 Pts)') + ' Cut at the scheme\'s own solidus.'),
        ('ii', ask(10, 'Name any one enzyme, and its substrate, and its product.'),
         [pt(S(line), 5, kind='criterion', note=NO_ANSWER)
          for line in ('Enzyme: any enzyme', 'Substrate: must match enzyme', 'Product: must match substrate or enzyme')],
         3, 'enzyme-substrate-and-product',
         POINTS.format(n='three', pts='(3 Pts)') + ' The scheme names no enzyme: each line is a criterion row under its '
                                                   'own label.'),
        ('iii', Q(10, 'The rate of activity of enzymes can be affected by various factors.',
                  'Name any two factors that can affect enzyme activity.'),
         [pt(S('Temperature / pH', piece=k), 5) for k in (1, 2)], 2, 'factors-affecting-enzymes',
         POINTS.format(n='two', pts='(2 Pts)') + ' The scheme prints exactly two factors: a row each.'),
        ('iv', Q(10, 'Enzymes are sometimes immobilised in industrial processes.',
                 'What is meant by the term immobilised in relation to enzymes?'),
         [anyn(S('Attached to a (inert)substance/ trapped / in beads'), 1, 5)], 1, 'immobilised-enzymes',
         ONE.format(notation='3(5)+6(2)')),
        ('v', ask(10, 'Give one advantage of using immobilised enzymes.'),
         [anyn(S('Can be reused / pure product / cheaper'), 1, 5)], 1, 'advantage-of-immobilised-enzymes',
         ONE.format(notation='3(5)+6(2)'))]
]

FIGURES = {
    # key suffix: (doc, page, rect in PDF points, credit, letters, alt, solution)
    'q3-cell': ('paper', 3, (200, 44, 378, 156), SEC, ['A', 'B'],
        'Drawing of a dividing cell: an oval outline with a small star-shaped body at its top pole and another at '
        'its bottom pole, fine lines fanning from each pole towards the middle, and two rows of dark curved bodies '
        'across the middle, the upper row arched upwards and the lower row arched downwards. A points to a dark '
        'curved body at the right end of the upper row; B points to one of the fine lines in the lower half.', False),
    'q5-table': ('paper', 4, (52, 25, 552, 292), SEC, [],
        'Question 5 as printed: the instruction, then the list Alcohol, Oxygen, Water, Mitochondria, Lactic acid, '
        'Large (struck through) above a two-column table. Column A lists "The amount of energy released in aerobic '
        'respiration." (answered Large in Column B as the example) and parts (i) to (v); Column B is blank beside '
        'them.', False),
    'q6-eye': ('paper', 4, (190, 330, 390, 458), SEC, ['A', 'B', 'C'],
        'Drawing of an eye in vertical section: a round eyeball with a layered wall, the front at the left, where a '
        'clear oval body is held between two small dark blocks; a speckled band lines the inside of the back wall; '
        'a bundle of fibres leaves the back of the eye at the lower right. A points to the bundle of fibres, B to '
        'the speckled band at the upper right of the back wall, C to the clear oval body at the front.', False),
    'q9-microscope': ('paper', 7, (418, 18, 592, 168), SEC, ['A', 'B'],
        'Line drawing of a light microscope seen from the side: a curved arm on a heavy base, a vertical tube with a '
        'short cylinder at its top, a rotating head carrying lenses below the tube, a flat horizontal plate with a '
        'clip below that, and further parts under the plate. A points to the short cylinder at the top of the tube; '
        'a pointer printed Objective lens points to the lens just above the plate; B points to the flat horizontal '
        'plate.', False),
    'q10-profile': ('paper', 8, (62, 482, 560, 766), SEC, ['A', 'B', 'C'],
        'Five columns of bands under the underlined headings Crime Scene, Victim, Suspect A, Suspect B and Suspect '
        'C, each band a thick black bar or a thin line, single or double. Reading down eight levels: 1, a thick bar '
        'in Crime Scene only; 2, a thin single line in Crime Scene and Suspect B; 3, a thin double line in Suspect A '
        'and Suspect C; 4, a thick bar in Crime Scene and Suspect B; 5, a thick bar in Suspect A; 6, a thick bar in '
        'Crime Scene, Victim and Suspect C; 7, a thin double line in Crime Scene, Suspect A and Suspect B; 8, a '
        'thick bar in Crime Scene and Suspect B.', False),
    'q11-web': ('paper', 9, (150, 148, 480, 322), SEC, [],
        'A food web of nine boxed names joined by arrows: Oaktree to Caterpillar and to Mouse; Blackberry to '
        'Thrush, to Mouse and to Greenfly; Caterpillar to Thrush; Thrush to Hawk; Mouse to Hawk; Greenfly to Spider '
        'and to Ladybird; Ladybird to Spider.', False),
    'q12-apparatus': ('paper', 10, (140, 252, 480, 472), SEC, [],
        'Apparatus as drawn: a bulb in a reflector at the left, labelled Strong light source, at one end of a ruler '
        'labelled Metre stick; an arrow labelled Set distance runs from the bulb to a test tube standing in a '
        'beaker. The beaker is labelled Water bath at 25°C and holds a thermometer, labelled Thermometer; the test '
        'tube holds a coiled plant labelled Pondweed, its stem labelled Cut stem, in liquid labelled Varied NaHCO3 '
        'soln.', False),
}


# ===================================================== Questions 13-15 ======
# Paper pages 11-13 store every printed line in overlapping vertical strips;
# they are read through paper.STRIP_SET_PAGES (strip_set_lines), which both the
# census and bio_review_lib.Src use for this paper. Authored by the author
# against the rebuilt lines; merged here by the coordinator.
Q13_15_QUESTION_TOTALS = {13: 60, 14: 90, 15: 90}   # Q14, Q15: any two of three 30s
Q13_15_PART_TOTALS = {(14, 'a'): 30, (15, 'a'): 30}   # "(30, 30)"; (a) is fixed marks
Q13_15_LADDERS = {
    (13, 'a'): _ladder('7 + 2(1)'), (13, 'b'): _ladder('2(6)+6(2)'), (13, 'c'): _ladder('3(5)+6(2)'),
    (14, 'b'): _ladder('2(7) + 8(2)'), (14, 'c'): _ladder('2(7) + 8(2)'),
    (15, 'b'): _ladder('2(7) + 8(2)'), (15, 'c'): _ladder('2(7) + 8(2)'),
}
Q13_15_CHECKSUMS = {
    (13, 'a'): {7: 3}, (13, 'b'): {6: 8}, (13, 'c'): {5: 9},
    (14, 'a'): {6: 1, 2: 3, 3: 6}, (14, 'b'): {7: 10}, (14, 'c'): {7: 10},
    (15, 'a'): {6: 1, 2: 3, 3: 6}, (15, 'b'): {7: 10}, (15, 'c'): {7: 10},
}

# ------------------------------------------------------------ question text --
Q13B = Q(11, 'The diagram shows a section through the human heart.')
Q13C = Q(11, 'The diagram shows part of the human breathing system.')
Q14AI = ask(12, 'Draw a large labelled diagram of the human female reproductive system.')
Q14B = Q(12, 'The diagram shows some parts of the human endocrine system.')
Q14CIII = Q(12, 'The diagram shows the human urinary system.')
Q14CIV = [Q(12, 'Name the parts of the kidney in which each of the'), Q(12, 'following takes place:')]
Q15B = Q(13, 'The diagram shows a transverse section of a dicotyledonous (dicot) root.')
Q15C = Q(13, 'The diagram shows the structure of a type of virus.')

# ------------------------------------------------------- scheme cell lines --
AIRWAYS = 'A=bronchus; B= trachea (allow cartilage for A or B)'
INHALE = ('Impulse from brain / (intercostal) muscles contract /', 'four points)')
FEMALE = ('Diagram must show at least three of the following: Ovaries,',
          'then only 3 marks and any three missing then zero marks)')
FLOWER = ('Diagram must show at least three of the following: Sepals,',
          'only 3 marks and any three missing then zero marks)')
IN_VITRO = 'In a glass vessel / test tube (Allow ‘outside body’)'
INFERTILITY = ('Inability to ovulate / blocked oviducts / menopause or age /', 'weight / excessive exercise …')
GLANDS = {'A': 'A = Thyroid (allow parathyroid)', 'B': 'B = Adrenals'}
URINARY = 'A = kidney; B = ureter; C = bladder'
URINARY_CUTS = [('; B =', 'kidney; '), ('; C =', 'ureter; ')]
ROOT = 'A = phloem; B = xylem; C = root hair'
ROOT_CUTS = [('; B =', 'phloem; '), ('; C =', 'xylem; ')]
VIRUS = {'A': 'A = nucleic acid (or DNA or RNA);', 'B': 'B = protein/coat'}
SAFE_DOSE = ('‘Safe dose’ of a pathogen / causing antibody production or', 'causing an immune response')
DRAWING = ('The scheme prices the drawing on its own, "6,3,0 (diagram) + 3(2) ( labels)", and (ii)-(v) "6(3)": a fixed '
           'tariff. The diagram (6, 3 or 0) is one criterion row naming what it must show, cut before its printed '
           '"= 6 marks", its bracketed banding the row\'s note; the labels one criterion row worth their three 2s, the '
           'scheme\'s "( labels)" cut out of its brackets. The scheme names no label.')


def _strip_cell(line, i, cuts, page=None):
    pieces, seps = [], []
    if i > 0:
        pieces.append(2)
        seps.append(cuts[i - 1][1])
    if i < len(cuts):
        pieces.append(1)
        seps.append(cuts[i][0])
    return S(line, page=page, piece=pieces, psep=seps)


def meaning(line, i, cuts, page):
    sel = _strip_cell(line, i, cuts, page=page)
    return {**sel, 'piece': sel['piece'] + [2], 'psep': sel['psep'] + [' = ']}


def heart_labels(asked=None):
    # The scheme names A ((i) "Aorta") and C ((iii) "Right ventricle"); B is never named.
    return [L('A', S('Aorta', page=10), asked == 'A'), L('C', S('Right ventricle', page=10), asked == 'C')]


def airway_labels(asked=None):
    return [L('A', S(AIRWAYS, page=10, piece=[1, 2], psep=['; ', '=']), asked == 'A'),
            L('B', S(AIRWAYS, page=10, piece=[2, 1, 2], psep=['; ', ' (', '= ']), asked == 'B')]


def gland_labels(asked=None):
    return [L('A', S(GLANDS['A'], page=11, piece=[2, 1], psep=[' = ', ' (']), asked == 'A'),
            L('B', S(GLANDS['B'], page=11, piece=2, psep=' = '), asked == 'B')]


def urinary_labels(asked=None):
    return [L(x, meaning(URINARY, i, URINARY_CUTS, 11), x == asked) for i, x in enumerate('ABC')]


def root_labels(asked=None):
    return [L(x, meaning(ROOT, i, ROOT_CUTS, 12), x == asked) for i, x in enumerate('ABC')]


def virus_labels(asked=None):
    return [L('A', S(VIRUS['A'], page=12, piece=[2, 1], psep=[' = ', ';']), asked == 'A'),
            L('B', S(VIRUS['B'], page=12, piece=2, psep=' = '), asked == 'B')]


Q13_15_TASKS = [
    # ------------------------------------------------------------ Q13 --------
    T('13ai', 'Q13(a)(i)', 'C', ask(11, 'Name the liquid part of the blood.'), [pt(S('Plasma'), 7)], 'bio-2-6',
      'plasma', at(10, '13', '(a)', '(i)'), 7),
    T('13aii', 'Q13(a)(ii)', 'C', Q(11, 'Different lifestyle factors have an effect on the health of our circulatory system.',
                                    'Name any two of these factors.'),
      [pt(S('Any two factors'), 14, kind='criterion', units=[7, 7], note=NO_ANSWER)], 'bio-2-6',
      'lifestyle-and-the-circulatory-system', at(10, '13', '(a)', '(ii)'), 14,
      decision='Two points ("(2 Pts)") of the "7 + 2(1)" ladder at its first rate. The scheme prints "Any two factors" '
               'and names none: one criterion row worth its two responses.'),
] + [
    T(f'13b{r}', f'Q13(b)({r})', 'C', q, [row], 'bio-2-6', concept, at(10, '13', '(b)', f'({r})'), total,
      stem=[Q13B] if fig else [], fig='q13-heart' if fig else None, labels=labels, decision=decision)
    for r, q, row, concept, total, fig, labels, decision in [
        ('i', ask(11, 'Name the blood vessel labelled A.'), pt(S('Aorta'), 6), 'aorta', 6, True, heart_labels('A'), ''),
        ('ii', ask(11, 'Does A carry blood towards or away from the heart?'), pt(S('Away from'), 6),
         'direction-of-aortic-blood', 6, True, heart_labels(), ''),
        ('iii', ask(11, 'Name the chamber of the heart labelled C.'), pt(S('Right ventricle'), 6), 'right-ventricle', 6,
         True, heart_labels('C'), ''),
        ('iv', ask(11, 'Why is the wall of chamber B thicker than the wall of chamber C?'),
         anyn(S('Blood from B must be pumped further / greater pressure'), 1, 6), 'ventricle-walls', 6, True,
         heart_labels(), ONE.format(notation='2(6)+6(2)') + ' The scheme never names B: the label key carries A and C.'),
        ('v', ask(11, 'Name the arteries that supply the heart wall with blood.'), anyn(S('Coronary / Cardiac'), 1, 6),
         'coronary-arteries', 6, False, None, ONE.format(notation='2(6)+6(2)')),
        ('vi', ask(11, 'What is the role of valves in the heart?'), pt(S('To prevent backflow (of blood)'), 6),
         'heart-valves', 6, False, None, ''),
        ('vii', Q(11, 'The lymphatic system is another series of vessels carrying fluid in the body.',
                  'Give any two functions of the lymphatic system.'),
         anyn(S('Returns fluid to blood / transport / lymphocytes(Immunity)'), 2, 6), 'lymphatic-system', 12, False,
         None, MENU.format(n='Two points', pts='(2 Pts)', claim='two'))]
] + [
    T(f'13ci-{x.lower()}', 'Q13(c)(i)', 'C', ask(11, 'Name the parts labelled A and B.'), [row], 'bio-2-6', concept,
      at(10, '13', '(c)', '(i)'), 5, stem=[Q13C], fig='q13-breathing', item=(x.lower(), x), labels=airway_labels(x),
      decision=EACH_ITEM + ' "(2 Pts)" over the two labels, cut at the scheme\'s own semicolon; its bracketed '
                           'direction is each row\'s note.')
    for x, row, concept in [
        ('A', pt(S(AIRWAYS, piece=1, psep='; '), 5, note_sel=S(AIRWAYS, piece=[2, 2, 1], psep=['; ', ' (', ')'])),
         'bronchus'),
        ('B', pt(S(AIRWAYS, piece=[2, 1], psep=['; ', ' (']), 5, note_sel=S(AIRWAYS, piece=[2, 2, 1],
                                                                             psep=['; ', ' (', ')'])), 'trachea')]
] + [
    T(f'13c{r}', f'Q13(c)({r})', 'C', q, [row], 'bio-2-6', concept, at(10, '13', '(c)', f'({r})'), total,
      decision=decision)
    for r, q, row, concept, total, decision in [
        ('ii', ask(11, 'In what structures in the lungs does gaseous exchange take place?'), pt(S('Alveoli or Air sacs'), 5),
         'alveoli', 5, ''),
        ('iii', Q(11, 'Give one feature of the structures referred to in (ii) that allows efficient exchange of', 'gases.'),
         anyn(S('Thin walls / moist surfaces / surrounded by capillaries/ large', 'surface area / expandable'), 1, 5),
         'features-of-alveoli', 5, ONE.format(notation='3(5)+6(2)')),
        ('iv', ask(11, 'What is the function of the larynx?'), pt(S('To make sound'), 5), 'larynx', 5, ''),
        ('v', ask(11, 'Outline the steps involved in inhalation.'),
         anyn(S(*INHALE, piece=1, psep=' (Any'), 4, 5, note_sel=S(*INHALE, piece=[2, 1], psep=['air in (', ')'])),
         'inhalation', 20, MENU.format(n='Four points', pts='(4 Pts)', claim='four') + ' Cut at the scheme\'s own '
                                                                                      'solidus; its "(Any four points)" '
                                                                                      'is the row\'s note.')]
] + [
    # ------------------------------------------------------------ Q14 --------
    T('14ai', 'Q14(a)(i)', 'C', Q14AI,
      [pt(S(*FEMALE, piece=1, psep=' = 6 marks '), 6, kind='criterion', whole=True, note=NO_ANSWER,
          note_sel=S(*FEMALE, piece=2, psep=' = 6 marks ')),
       pt(S('+ 3(2) ( labels)', piece=[2, 1], psep=['( ', ')']), 6, kind='criterion', units=[2, 2, 2], note=NO_ANSWER)],
      'bio-2-5', 'drawing-the-female-reproductive-system', at(11, '14', '(a)', '(i)'), 12, decision=DRAWING),
    T('14aii', 'Q14(a)(ii)', 'C',
      [ask(12, 'Indicate clearly on your diagram where each of the following events takes place:'),
       Q(12, '1. Ovulation', br=True), Q(12, '2. Fertilisation.', br=True)],
      [pt(S('1. On ovary'), 3),
       pt(S('2. In oviduct (not in uterus)', piece=1, psep=' ('), 3,
          note_sel=S('2. In oviduct (not in uterus)', piece=[2, 1], psep=[' (', ')']))],
      'bio-2-5', 'sites-of-ovulation-and-fertilisation', at(11, '14', '(a)', '(ii)-(vi)', '(ii)'), 6,
      stem=[Q14AI],
      decision=POINTS.format(n='two', pts='(2 Pts)') + ' Fixed at 3 each ("6(3)" over (ii)-(vi)); each numbered answer '
                                                       'read whole, the second\'s bracket its note.'),
] + [
    T(f'14a{r}', f'Q14(a)({r})', 'C', q, [row], 'bio-2-5', concept, at(11, '14', '(a)', '(ii)-(vi)', f'({r})'), 3,
      decision=decision)
    for r, q, row, concept, decision in [
        ('iii', ask(12, 'What does the term infertility mean?'),
         pt(S('The inability to produce offspring or the inability to produce', 'gametes'), 3), 'infertility', ''),
        ('iv', Q(12, 'In vitro fertilisation is a method used to treat infertility.',
                 'What is meant by the term in vitro in relation to fertilisation?'),
         anyn(S(IN_VITRO, piece=1, psep=' ('), 1, 3, note_sel=S(IN_VITRO, piece=[2, 1], psep=[' (', ')'])),
         'in-vitro', 'One point at 3 ("6(3)"): either printed answer, a menu, claim one; its bracket is the note.'),
        ('v', ask(12, 'Give one cause of infertility in women.'),
         anyn(S(*INFERTILITY, piece=1, psep=' …'), 1, 3, open_list=True), 'causes-of-infertility',
         'One point at 3 ("6(3)"): any one of the printed causes, a menu, claim one; its "…" leaves it open.'),
        ('vi', Q(12, 'As a result of fertility treatment, an embryo develops successfully from an in vitro',
                 'fertilisation. What is the next step for the embryo?'),
         anyn(S('Implantation / frozen'), 1, 3), 'after-ivf', 'One point at 3 ("6(3)"): either printed answer.')]
] + [
    T(f'14bi-{x.lower()}', 'Q14(b)(i)', 'C', ask(12, 'Name the glands labelled A and B.'),
      [pt(S(GLANDS[x], piece=1, psep=' (') if x == 'A' else S(GLANDS[x]), 7,
          **({'note_sel': S(GLANDS['A'], piece=[2, 1], psep=[' (', ')'])} if x == 'A' else {}))],
      'bio-2-4', concept, at(11, '14', '(b)', '(i)'), 7, stem=[Q14B], fig='q14-endocrine', item=(x.lower(), x),
      labels=gland_labels(x), decision=EACH_ITEM + ' "2(Pts)" over the two glands, each on its own line.')
    for x, concept in [('A', 'thyroid'), ('B', 'adrenal-glands')]
] + [
    T(f'14b{r}', f'Q14(b)({r})', 'C', q, rows, 'bio-2-4', concept, at(11, '14', '(b)', f'({r})'), 7 * n,
      decision=decision)
    for r, q, rows, n, concept, decision in [
        ('ii', ask(12, 'Name any one hormone produced by the body.'),
         [pt(S('Any human hormone'), 7, kind='criterion', note=NO_ANSWER)], 1, 'naming-a-hormone',
         'The scheme names no hormone: a criterion row.'),
        ('iii', Q(12, 'Give a deficiency symptom of the hormone named', 'in (ii) above.'),
         [pt(S('Deficiency symptom must match Hormone'), 7, kind='criterion', note=NO_ANSWER)], 1,
         'hormone-deficiency-symptom', 'The scheme names no symptom: a criterion row.'),
        ('iv', ask(12, 'Give one example of the use of hormone supplements.'),
         [pt(S('Any one use'), 7, kind='criterion', note=NO_ANSWER)], 1, 'hormone-supplements',
         'The scheme names no use: a criterion row.'),
        ('v', Q(12, 'The central nervous system is made up of two main parts.', 'Name each part.'),
         [pt(S('Brain/spinal cord', piece=k), 7) for k in (1, 2)], 2, 'parts-of-the-cns',
         POINTS.format(n='two', pts='(2 Pts)') + ' Cut at the scheme\'s own solidus.'),
        ('vi', Q(12, 'Name a disorder of the nervous system.', 'treating the disorder.'),
         [pt(S('Named disorder/cause/treatment', piece=k), 7, kind='criterion', note=NO_ANSWER) for k in (1, 2, 3)], 3,
         'nervous-system-disorder', POINTS.format(n='three', pts='(3 Pts)') + ' The scheme names no disorder: cut at '
                                                                              'its own solidus, a criterion row each.')]
] + [
    T('14ci', 'Q14(c)(i)', 'C', ask(12, 'Explain the term excretion.'),
      [pt(S('Getting rid of waste / made in the body', piece=k), 7) for k in (1, 2)], 'bio-2-6', 'excretion',
      at(11, '14', '(c)', '(i)'), 14, decision=POINTS.format(n='two', pts='(2 Pts)') + ' Cut at the scheme\'s own solidus.'),
    T('14cii', 'Q14(c)(ii)', 'C', ask(12, 'Name two substances excreted by the kidneys.'),
      [anyn(S('Urea/water/salt / urine'), 2, 7)], 'bio-2-6', 'substances-excreted-by-the-kidneys',
      at(11, '14', '(c)', '(ii)'), 14, decision=MENU.format(n='Two points', pts='(2 Pts)', claim='two')),
] + [
    T(f'14ciii-{x.lower()}', 'Q14(c)(iii)', 'C', ask(12, 'Name the parts labelled A, B, and C.'),
      [pt(_strip_cell(URINARY, i, URINARY_CUTS), 7)], 'bio-2-6', concept, at(11, '14', '(c)', '(iii)'), 7, stem=[Q14CIII],
      fig='q14-urinary', item=(x.lower(), x), labels=urinary_labels(x),
      decision=EACH_ITEM + ' "(3 Pts)" over the three labels, cut at the scheme\'s own semicolons.')
    for i, (x, concept) in enumerate([('A', 'kidney'), ('B', 'ureter'), ('C', 'bladder')])
] + [
    T(f'14civ{n}', f'Q14(c)(iv){n}', 'C', Q14CIV + [Q(12, item, br=True)], [pt(S(ans), 7)], 'bio-2-6', concept,
      at(11, '14', '(c)', '(iv)'), 7, decision=EACH_ITEM + ' "(2 Pts)" over the two numbered processes.')
    for n, item, ans, concept in [(1, '1. Filtration', '1. Cortex', 'site-of-filtration'),
                                  (2, '2. Reabsorption.', '2. Medulla or Cortex', 'site-of-reabsorption')]
] + [
    T('14cv', 'Q14(c)(v)', 'C', ask(12, 'Name one other excretory organ in the body.'),
      [anyn(S('Lungs/skin/liver'), 1, 7)], 'bio-2-6', 'other-excretory-organs', at(11, '14', '(c)', '(v)'), 7,
      decision=ONE.format(notation='2(7) + 8(2)')),
    # ------------------------------------------------------------ Q15 --------
    T('15ai', 'Q15(a)(i)', 'C', ask(13, 'Draw a large labelled diagram to show the internal structure of a flower.'),
      [pt(S(*FLOWER, piece=1, psep=' = 6 marks '), 6, kind='criterion', whole=True, note=NO_ANSWER,
          note_sel=S(*FLOWER, piece=2, psep=' = 6 marks ')),
       pt(S('+ 3(2) ( labels)', piece=[2, 1], psep=['( ', ')']), 6, kind='criterion', units=[2, 2, 2], note=NO_ANSWER)],
      'bio-2-5', 'drawing-a-flower', at(12, '15', '(a)', '(i)'), 12, decision=DRAWING),
] + [
    T(f'15a{r}', f'Q15(a)({r})', 'C', q, [row], 'bio-2-5', concept, at(12, '15', '(a)', '(ii)–(v)', f'({r})'), total,
      decision=decision)
    for r, q, row, concept, total, decision in [
        ('ii', ask(13, 'Give two ways by which pollen is transferred from one flower to another.'),
         anyn(S('Wind / insects / birds'), 2, 3), 'methods-of-pollination', 6,
         MENU.format(n='Two points', pts='2(Pts)', claim='two') + ' Fixed at 3 each ("6(3)" over (ii)-(v)).'),
        ('iii', ask(13, 'After fertilisation, what part of the flower becomes the fruit?'),
         pt(S('Ovary (allow ‘carpel’)', piece=1, psep=' ('), 3,
            note_sel=S('Ovary (allow ‘carpel’)', piece=[2, 1], psep=[' (', ')'])), 'ovary-becomes-fruit', 3, ''),
        ('iv', Q(13, 'Many seedless fruits, e.g. grapes, are available in shops today.',
                 'State one way of forming seedless fruits.'),
         anyn(S('Genetic engineering / growth regulators / hormones /', 'selective breeding'), 1, 3), 'seedless-fruits', 3,
         'One point at 3 ("6(3)"): any one of the printed ways, a menu, claim one.'),
        ('v', Q(13, 'Sometimes artificial methods are used to propagate (reproduce) plants.',
                'Name any two methods of artificially propagating plants.'),
         anyn(S('Grafting/cutting/layering...'), 2, 3), 'artificial-propagation', 6,
         MENU.format(n='Two points', pts='2(Pts)', claim='two') + ' Its "..." leaves the list open.')]
] + [
    T(f'15bi-{x.lower()}', 'Q15(b)(i)', 'C', ask(13, 'Name the parts labelled A, B and C.'),
      [pt(_strip_cell(ROOT, i, ROOT_CUTS), 7)], 'bio-2-6', concept, at(12, '15', '(b)', '(i)'), 7, stem=[Q15B],
      fig='q15-root', item=(x.lower(), x), labels=root_labels(x),
      decision=EACH_ITEM + ' "3(Pts)" over the three labels, cut at the scheme\'s own semicolons.')
    for i, (x, concept) in enumerate([('A', 'phloem-in-the-root'), ('B', 'xylem-in-the-root'), ('C', 'root-hair')])
] + [
    T(f'15b{r}', f'Q15(b)({r})', 'C', q, rows, topic, concept, at(12, '15', '(b)', f'({r})'), total, decision=decision)
    for r, q, rows, topic, concept, total, decision in [
        ('ii', ask(13, 'State two functions of a root.'),
         [anyn(S('Absorb water/ absorb minerals / anchorage / food store /', 'reproduction (qualfied)'), 2, 7)],
         'bio-2-6', 'functions-of-a-root', 14,
         MENU.format(n='Two points', pts='2(Pts)', claim='two') + ' The scheme\'s "qualfied" is lifted as printed.'),
        ('iii', ask(13, 'From what part of a seed does the root develop?'),
         [pt(S('Radicles (allow embryo)', piece=1, psep=' ('), 7,
             note_sel=S('Radicles (allow embryo)', piece=[2, 1], psep=[' (', ')']))], 'bio-2-5', 'radicle', 7, ''),
        ('iv', ask(13, 'Give one example of a root modified for food storage.'),
         [anyn(S('Carrot / turnip / parsnip / root tuber ...'), 1, 7)], 'bio-2-6', 'food-storage-roots', 7,
         ONE.format(notation='2(7) + 8(2)') + ' Its "..." leaves the list open.'),
        ('v', Q(13, 'Plants can be monocotyledonous or dicotyledonous.', 'plant.'),
         [anyn(None, 1, 7, options=[S('One cotyledon vs two cotyledons'),
                                    S('Parallel venation vs reticulate venation/', piece=1, psep='/'),
                                    S('Flower parts in multiples of 3 vs flower parts in multiples of', '4 / 5.'),
                                    S('Scattered vs ring of vascular bundles in stems'),
                                    S('Fibrous roots vs tap roots')],
               note_sel=S('(One side of', 'sufficient)'))], 'bio-2-6', 'monocots-and-dicots', 7,
         'One point ("1 (Pt)"): the scheme prints five differences, one per line, each a menu option, claim one; its '
         'direction "(One side of argument is sufficient)" is the row\'s note.'),
        ('vi', Q(13, 'Give one example of a monocotyledonous plant and one example of a', 'dicotyledonous plant.'),
         [pt(S('Example monocot / Example dicot', piece=k), 7, kind='criterion', note=NO_ANSWER) for k in (1, 2)],
         'bio-2-6', 'monocot-and-dicot-examples', 14,
         POINTS.format(n='two', pts='2(Pts)') + ' The scheme names no plant: cut at its own solidus, a criterion row '
                                                'each.')]
] + [
    T(f'15ci-{x.lower()}', 'Q15(c)(i)', 'C', ask(13, 'Name the parts labelled A and B.'), [row], 'bio-1-1', concept,
      at(12, '15', '(c)', '(i)'), 7, stem=[Q15C], fig='q15-virus', item=(x.lower(), x), labels=virus_labels(x),
      decision=EACH_ITEM + ' "2(Pts)" over the two labels, each on its own line.')
    for x, row, concept in [
        ('A', pt(S(VIRUS['A'], piece=1, psep=';'), 7), 'viral-nucleic-acid'),
        ('B', pt(S(VIRUS['B']), 7), 'viral-protein-coat')]
] + [
    T(f'15c{r}', f'Q15(c)({r})', 'C', q, rows, topic, concept, at(12, '15', '(c)', f'({r})'), total, decision=decision)
    for r, q, rows, topic, concept, total, decision in [
        ('ii', ask(13, 'State two harmful effects of viruses.'),
         [pt(S('Two harmful effects (Any two viral diseases)', piece=1, psep=' ('), 14, kind='criterion', units=[7, 7],
             note=NO_ANSWER, note_sel=S('Two harmful effects (Any two viral diseases)', piece=[2, 1], psep=[' (', ')']))],
         'bio-1-1', 'harmful-effects-of-viruses', 14,
         'Two points ("2(Pts)"): the scheme names no effect, so its "Two harmful effects" is one criterion row worth '
         'both responses, its bracket the note.'),
        ('iii', ask(13, 'What is meant by the term immunity?'), [pt(S('Defence against disease'), 7)], 'bio-2-4',
         'immunity', 7, ''),
        ('iv', Q(13, 'The skin is an important part of our immune system.',
                 'Outline two ways in which the skin provides immunity.'),
         [anyn(S('Barrier / sweat / scabs'), 2, 7)], 'bio-2-4', 'skin-and-immunity', 14,
         MENU.format(n='Two points', pts='2(Pts)', claim='two')),
        ('v', Q(13, 'To help the immune system, many people receive vaccinations during their lifetime.',
                'What is meant by the term vaccination?'),
         [pt(S(*SAFE_DOSE, piece=k), 7) for k in (1, 2)], 'bio-2-4', 'vaccination', 14,
         POINTS.format(n='two', pts='2(Pts)') + ' Cut at the scheme\'s own solidus.'),
        ('vi', Q(13, 'Antibiotics are usually not given to a person suffering from a viral infection.',
                 'Suggest a reason for this.'),
         [pt(S('Antibiotics have no effect on viruses'), 7)], 'bio-1-1', 'antibiotics-and-viruses', 7, '')]
]

Q13_15_FIGURES = {
    'q13-heart': ('paper', 11, (195, 104, 440, 330), SEC, ['A', 'B', 'C'],
        'Drawing of the heart in section: chambers within a thick speckled wall, upper and lower, with vessels '
        'rising from the top. A points to a vessel arching over the top '
        'at the right; a pointer printed Bicuspid valve points between the upper and lower chambers on the right; C '
        'points into the lower chamber on the left; B points into the lower chamber on the right.', False),
    'q13-breathing': ('paper', 11, (215, 478, 450, 690), SEC, ['A', 'B'],
        'Drawing of the chest: a ringed tube running down from a structure at the top labelled Larynx, dividing into '
        'branches that enter the lungs, with ribs at the left and a lung opened to show its branching airways at '
        'the right. B points to the ringed tube in the neck; A points to the point just below where the tube '
        'divides, at the entrance to the right-hand lung.', False),
    'q14-endocrine': ('paper', 12, (438, 234, 590, 437), SEC, ['A', 'B'],
        'Outline of a human body from the head to the hips showing some organs: a small butterfly-shaped gland in '
        'the neck, the stomach and a long gland beneath it, and two kidneys, each with a small gland on its top. A '
        'points to the gland in the neck; B has two pointers, one to the small gland on top of each kidney.', False),
    'q14-urinary': ('paper', 12, (422, 464, 590, 632), SEC, ['A', 'B', 'C'],
        'Drawing of the lower trunk: two bean-shaped organs, each with a small cap on top, joined by vessels to two '
        'large central vessels; a narrow tube runs down from each bean-shaped organ to a round sac at the bottom. A '
        'points to the right-hand bean-shaped organ, B to the narrow tube leaving it, C to the round sac.', False),
    'q15-root': ('paper', 13, (230, 200, 420, 304), SEC, ['A', 'B', 'C'],
        'Diagram of a root in transverse section: a large circle with an inner circle at its centre holding a dark '
        'four-armed cross with a small grey round body between each pair of arms; long thin threads grow out from '
        'the outer edge. A points to one of the small grey round bodies, B to the dark cross, C to one of the thin '
        'threads.', False),
    'q15-virus': ('paper', 13, (215, 490, 360, 658), SEC, ['A', 'B'],
        'Drawing of a virus: a many-sided head containing a coiled strand, on a ringed hollow tail ending in a flat '
        'base plate with six long jointed legs. A points to the coiled strand inside the head; B points to the '
        'outer surface of the head.', False),
}


QUESTION_TOTALS.update(Q13_15_QUESTION_TOTALS)
PART_TOTALS.update(Q13_15_PART_TOTALS)
LADDERS.update(Q13_15_LADDERS)
CHECKSUMS.update(Q13_15_CHECKSUMS)
TASKS += Q13_15_TASKS
FIGURES.update(Q13_15_FIGURES)
