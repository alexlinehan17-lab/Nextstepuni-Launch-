"""Biology 2010 Ordinary Level — reviewed task ledger, carded from the paper for the first time.

Independent visual sweep (2026-10-27), every page rendered and read:
  * The 2010 paper is one booklet (M43), 16 pages: p1 cover and instructions,
    p2-p5 Section A Questions 1-6, p6-p8 Section B Questions 7-9, p9-p14
    Section C Questions 10-15, p15-p16 "Blank Page". Sections A and B are
    answered on the paper; Section C in an answer book. No acknowledgements
    page: every drawing and the Q14(c) fruit pictures carry no credit; the
    Q10(c) passage carries its own "(Adapted from Advanced Biology, 3rd
    Edition, J. Simpkins, J. I. Williams)". Questions 10-13 print their part
    totals "(9)", "(27)", "(24)"; Q14 and Q15 print "(30, 30)".
  * The marking scheme, 11 pages: p1 cover, p2 blank (no text layer), p3
    introduction, cancelled answers and surplus answers (printed page 2), p4
    surplus answers and conventions (printed page 3), p5-p10 Questions 1-15
    (one table, printed page numbers 4-9), p11 back cover (no text layer).

The paper keeps the long-standing shape: any five of Section A's six
questions, any two of Section B's three, any four of Section C's six, and
Questions 14 and 15 are each any two of (a), (b), (c). No Biology card existed
for 2010 Ordinary before this review.

This scheme prints no reprint of any question: each answer stands under its
own question number, letter and roman, in the table's own columns. Every task
is anchored on its part marker, found by walking the scheme's numbering down
to it (SQ path). One roman, Q7(b)(iv), is set on its answer's own line ("(iv)
To inactivate enzymes"): a welded bare anchor, its row read from that line. A
numbered item ("1.", "2.") is anchored on the roman it is printed under.

Tariffs. Every ordered split of this scheme leads with its largest rate and is
carded at it: Section A Q1, Q2, Q3 and Q5 "2(7) + 2 + 4(1)" over seven
answers, Q4 and Q6 "2(7) + 3(2)" over five (each question's own ladder);
Section B every (a) "5+1", Q7(b) and Q9(b) "2(6)+6(2)", and Q8(b) "2(6) +
4(2) +1" over its seven answers outside the drawing (its last step a single
1; with (iii)'s drawing, "Diagram: ... 2, 0" and "Label: [one label] 1",
printed beside it, the part makes the rubric's 24); Section C Q10(a), Q11(a),
Q12(a), Q13(a) "7+2(1)", Q10(b), Q11(b), Q12(b), Q13(b) "3(5)+6(2)", Q10(c),
Q11(c), Q13(c) "2(6)+6(2)", Q12(c)(ii)-(v) "3(5)+3(1)", Q14(a) and Q15(a)
"2(6)+6(2)", Q14(b) and Q15(b) "3(6)+6(2)", Q14(c) "2(6) +2(3) + 6(2)",
Q15(c)(ii)-(vii) "2(6) + 5(2)". Five drawings are priced on their own beside
their part's ladder: Q8(b)(iii) "2, 0" and "1", Q12(c)(i) "3,0", Q14(a)(v)
"3, 0" and Q15(a)(iv) "3, 0" each with "3(1)" for three labels, and Q15(c)(i)
"5, 3, 0" with "3(1)"; each ladder names their units as fixed and their cards
keep their own marks. No part needs a whole-part (questionTotal) card.

Q11(c)(vii) ("Give one function of proteins in living organisms.", paper p10)
has no answer in the scheme: its Q11(c) block (scheme p7) prints (i) to (vi)
and then blank table rows. Nothing can be lifted for it, so it is not in
TASKS. The review left the census leaf (11, 'c', 'vii') OPEN with its page
evidence (ca320bf8a); on 2026-10-27 it was decided to exclude it, with that
evidence: EXCLUDED_LEAVES records it, and the same entry stands in
exclusions/biology.json, which reconcile.py counts. The ladder "2(6)+6(2)"
has eight steps for (i)'s two bases and (ii)-(vii); seven of those responses
are carded, which LADDERS records as 'responses': 7.

The scheme's text layer reads its single quotes as U+2018/U+2019, as printed.
It misspells "Heterotrohic nutrition" (Q13(a)(ii)), "rythym" (Q14(b)(v)) and
"words to that affect" (Q1(c)); all are lifted as printed. Its Q1(a) cell sets
"[allow ‘decomposition’, allow ‘assimilation’]" after D's answer, on D's own
line, so it is D's note, as printed. The paper's Q1 carbon-cycle picture
carries a faint show-through of other printed text inside its scanned image,
behind the lower half of the drawing (partly legible at 6x zoom: "...
Photosynthesis ...", "... Combustion ...", "... Oxygen ..."); it is the SEC's
own print and is cropped as printed, not masked (brought to the coordinator).

The census reader finds all 145 printed asks, keyed as the paper prints them
(Q2 and Q4-Q6 by roman alone); no paper.py entry was needed. 144 are claimed
here; (11, 'c', 'vii') is the one excluded (above).
"""
from bio_review_lib import Q, SQ, S, M, pt, anyn, T, L

YEAR, LEVEL = 2010, 'ol'
REVIEWED_AT = '2026-10-27'

SOURCES = {
    'paper': {'path': 'examiner-reports/biology/papers/2010-ol-paper.pdf',
              'fileid': 'LC025GLP000EV.pdf',
              'sha256': '97369eec58626ea8011318460e4f7bda32b61b465aabab420f480e47823d010f',
              'pages': 16},
    'scheme': {'path': 'examiner-reports/biology/schemes/2010-ol.pdf',
               'fileid': 'LC025GLP000EV.pdf',
               'sha256': '09e0ceeb579948acbd7584859befa2efb9defc5ab857a27306560cb5130dfdc6',
               'pages': 11},
}

PAGE_ROLES = {
    'paper': {1: 'cover', **{p: 'questions' for p in range(2, 15)}, 15: 'blank', 16: 'blank'},
    'scheme': {1: 'cover', 2: 'blank', 3: 'introduction', 4: 'conventions',
               **{p: 'marking' for p in range(5, 11)}, 11: 'back-cover'},
}


def _ladder(notation, **extra):
    """An ordered split as the scheme prints it ("2(7) + 2 + 4(1)", "5+1")."""
    steps = []
    for term in notation.split('+'):
        n, _, m = term.strip().partition('(')
        steps += [int(m.rstrip(')'))] * int(n) if m else [int(n)]
    return {'steps': steps, 'notation': notation, **extra}


QUESTION_TOTALS = {
    **{n: 20 for n in range(1, 7)}, **{n: 30 for n in range(7, 10)},
    **{n: 60 for n in range(10, 14)}, 14: 90, 15: 90,   # Q14, Q15: any two of three 30s
}
# Every part is an ordered split whose ladder makes its printed total (Section
# B's rubric "Part (a) carries 6 marks and part (b) carries 24 marks"; Q10-Q13's
# "(9)", "(27)", "(24)"; Q14 and Q15's "(30, 30)"), each checked by hand:
# 2(7)+2+4(1) = 20, 2(7)+3(2) = 20, 5+1 = 6, 2(6)+6(2) = 24, 2(6)+4(2)+1 and
# its drawing's 2+1 = 24, 7+2(1) = 9, 3(5)+6(2) = 27, 3(5)+3(1) and its drawing's 3+3(1) = 24,
# 2(6)+6(2) and its drawing's 3+3(1) = 30, 3(6)+6(2) = 30, 2(6)+2(3)+6(2) =
# 30, 2(6)+5(2) and its drawing's 5+3(1) = 30. The runner checks each
# question's ladders against its printed total.
PART_TOTALS = {}
LADDERS = {
    1: _ladder('2(7) + 2 + 4(1)'), 2: _ladder('2(7) + 2 + 4(1)'), 3: _ladder('2(7) + 2 + 4(1)'),
    4: _ladder('2(7) + 3(2)'), 5: _ladder('2(7) + 2 + 4(1)'), 6: _ladder('2(7) + 3(2)'),
    (7, 'a'): _ladder('5+1'), (7, 'b'): _ladder('2(6)+6(2)'),
    # (b)(iii)'s drawing "2, 0" and label "1" are fixed beside (i), (ii) and (iv)-(vii)'s "2(6) + 4(2) +1".
    (8, 'a'): _ladder('5+1'), (8, 'b'): _ladder('2(6) + 4(2) +1', fixed={2: 1, 1: 1}),
    (9, 'a'): _ladder('5+1'), (9, 'b'): _ladder('2(6)+6(2)'),
    (10, 'a'): _ladder('7+2(1)'), (10, 'b'): _ladder('3(5)+6(2)'), (10, 'c'): _ladder('2(6)+6(2)'),
    (11, 'a'): _ladder('7+2(1)'), (11, 'b'): _ladder('3(5)+6(2)'),
    # Eight steps; (vii) has no printed answer and is not carded (docstring).
    (11, 'c'): _ladder('2(6)+6(2)', responses=7),
    (12, 'a'): _ladder('7+2(1)'), (12, 'b'): _ladder('3(5)+6(2)'),
    # (c)(i)'s drawing "3,0" and labels "3(1)" are fixed beside (ii)-(v)'s "3(5)+3(1)".
    (12, 'c'): _ladder('3(5)+3(1)', fixed={3: 1, 1: 3}),
    (13, 'a'): _ladder('7+2(1)'), (13, 'b'): _ladder('3(5)+6(2)'), (13, 'c'): _ladder('2(6)+6(2)'),
    # (a)(v)'s drawing "3, 0" and labels "3(1)" are fixed beside the ladder.
    (14, 'a'): _ladder('2(6)+6(2)', fixed={3: 1, 1: 3}),
    (14, 'b'): _ladder('3(6)+6(2)'), (14, 'c'): _ladder('2(6) +2(3) + 6(2)'),
    # (a)(iv)'s drawing "3, 0" and labels "3(1)", (c)(i)'s "5, 3, 0" and "3(1)".
    (15, 'a'): _ladder('2(6) +6(2)', fixed={3: 1, 1: 3}),
    (15, 'b'): _ladder('3(6) + 6(2)'),
    (15, 'c'): _ladder('2(6) + 5(2)', fixed={5: 1, 1: 3}),
}

# The scheme's answer and point counts ("(Two points)", "(Three points)"), as
# mark units: each response at its ladder's first rate, the drawings' units as
# printed.
CHECKSUMS = {
    1: {7: 7}, 2: {7: 7}, 3: {7: 7}, 4: {7: 5}, 5: {7: 7}, 6: {7: 5},
    (7, 'a'): {5: 2}, (7, 'b'): {6: 8},
    (8, 'a'): {5: 2}, (8, 'b'): {6: 7, 2: 1, 1: 1},
    (9, 'a'): {5: 2}, (9, 'b'): {6: 8},
    (10, 'a'): {7: 3}, (10, 'b'): {5: 9}, (10, 'c'): {6: 8},
    (11, 'a'): {7: 3}, (11, 'b'): {5: 9}, (11, 'c'): {6: 7},
    (12, 'a'): {7: 3}, (12, 'b'): {5: 9}, (12, 'c'): {5: 6, 3: 1, 1: 3},
    (13, 'a'): {7: 3}, (13, 'b'): {5: 9}, (13, 'c'): {6: 8},
    (14, 'a'): {6: 8, 3: 1, 1: 3}, (14, 'b'): {6: 9}, (14, 'c'): {6: 10},
    (15, 'a'): {6: 8, 3: 1, 1: 3}, (15, 'b'): {6: 9}, (15, 'c'): {6: 7, 5: 1, 1: 3},
}

SCAN_PAGES = {'paper': range(1, 15)}
SELECTION_SCAN = [
    ('paper', 1, 'any five', 'Cover rubric, Section A: whole-question choice; every question is carded.'),
    ('paper', 1, 'any two', 'Cover rubric, Section B: whole-question choice; every question is carded.'),
    ('paper', 1, 'any four', 'Cover rubric, Section C: whole-question choice; every question is carded.'),
    ('paper', 2, 'any five', 'Section A rubric repeated.'),
    ('paper', 2, 'the following', 'Q2 lead-in: every statement asked, one card per roman.'),
    ('paper', 2, 'or', 'Q2 "true (T) or false (F)": the answer options.'),
    ('paper', 2, 'or', 'Q2 "T or F": the answer options.'),
    ('paper', 3, 'or', 'Q3(a) "a plant cell or an animal cell": the answer options.'),
    ('paper', 3, 'choose', 'Q4 "Choose each term": every description matched, one card per roman.'),
    ('paper', 3, 'the following', 'Q4 list of terms: the options.'),
    ('paper', 4, 'or', 'Q5(v) "a disorder of the ear or of the eye": the candidate chooses; the scheme prices '
                       '"Disorder:" and "Corrective measure:" alike for either, so no route.'),
    ('paper', 5, 'both', 'Q6(i) "found at both V and Y": description.'),
    ('paper', 6, 'any two', 'Section B rubric repeated.'),
    ('paper', 7, 'the following', 'Q8(b) lead-in: every part asked.'),
    ('paper', 8, 'the following', 'Q9(b) lead-in: every part asked.'),
    ('paper', 8, 'the following', 'Q9(b)(iv) "the following diagrams": the printed diagrams, the card\'s figure.'),
    ('paper', 8, 'or', 'Q9(b)(iv) "A or B": the answer options.'),
    ('paper', 9, 'any four', 'Section C rubric repeated.'),
    ('paper', 9, 'any one', 'Q10(c)(ii) "any one named pollutant": the scheme prices a named pollutant and its '
                            'matching effect (criterion rows).'),
    ('paper', 9, 'one of the following', 'Q10(c)(iii) "one of the following industries": the candidate chooses; the '
                                         'scheme prices an outline alike for any, so no route.'),
    ('paper', 9, 'or', 'Q10(c)(iii) "agriculture or forestry": the industries of that choice.'),
    ('paper', 9, 'or', 'Q10(c)(iii) "forestry or fisheries": the industries of that choice.'),
    ('paper', 10, 'or', 'Q11(b)(i) "black or white": the answer options.'),
    ('paper', 10, 'or', 'Q11(b)(iii) "homozygous or heterozygous": the answer options.'),
    ('paper', 10, 'both', 'Q11(c)(ii) "both transcription and translation": description.'),
    ('paper', 11, 'the following', 'Q12(b)(i) "the following word equation": the printed equation, in the question '
                                   'text.'),
    ('paper', 11, 'or', 'Q12(b)(iii) "a large amount or a small amount": the answer options.'),
    ('paper', 11, 'or', 'Q12(c)(i) "light intensity or carbon dioxide concentration": the candidate\'s choice of '
                        'investigation; the scheme prices one diagram for either, so no route.'),
    ('paper', 11, 'or', 'Q12(c)(ii) "the light intensity or the carbon dioxide concentration": the scheme prints a '
                        'way for each ("OR"), priced alike: one menu, claim one, no route.'),
    ('paper', 11, 'either', 'Q12(c)(iv) "either the light intensity": the scheme prints one relationship for either.'),
    ('paper', 11, 'or', 'Q12(c)(iv) "or the carbon dioxide concentration": the same choice.'),
    ('paper', 12, 'the following', 'Q13(b)(ii) "each of the following types of teeth": every numbered item asked, '
                                   'one card each.'),
    ('paper', 12, 'the following', 'Q13(b)(iv) "the following changes": both numbered changes asked, one card each.'),
    ('paper', 13, 'any two', 'Q14 "any two of the parts (a), (b), (c)": whole-part choice; every part is carded.'),
    ('paper', 13, 'any one', 'Q14(b)(iv) "Give any one biological benefit": any one of the printed benefits.'),
    ('paper', 13, 'any two', 'Q14(c)(vi) "Name any two of these conditions": one menu, claim two.'),
    ('paper', 14, 'any two', 'Q15 "any two of the parts (a), (b), (c)": whole-part choice; every part is carded.'),
]

ROUTES = {}

# Left OPEN, neither carded nor excluded (the coordinator's rule: an ask the
# scheme prints no answer for stays open, with its page evidence, for Alex).
EXCLUDED_LEAVES = {
    (11, 'c', 'vii'): {
        'reason': 'The scheme prints no answer for this ask, so nothing can be lifted and no answer is written. '
                  'Left OPEN by the review (ca320bf8a); excluded with this page evidence on 2026-10-27 '
                  '(a decision Alex delegated to the coordinator).',
        'evidence': 'Paper p10 prints "(vii) Give one function of proteins in living organisms." '
                    'as the last ask of Q11(c), "(24)". Scheme p7 (printed page 6) prints Q11(c) '
                    '(i) "1. Thymine or T" / "2. Cytosine or C" to (vi) "It must fold (into its '
                    'functional shape)" beside "2(6)+6(2)", then an empty cell and a blank row; '
                    'scheme p8 opens on Question 12. There is no (vii) row. The ladder\'s eight '
                    'steps match (i)1, (i)2 and (ii)-(vii), so (vii) is priced (2) with no answer '
                    'printed (rendered and looked at).',
    },
}

SEC = 'State Examinations Commission'
NO_REPRINT = 'The scheme prints no reprint of any question: anchored on the part\'s own marker.'
WELDED = ('The scheme prints no reprint and sets this part\'s marker on its answer\'s own line: anchored on that '
          'marker.')
EACH_ITEM = 'A list the scheme prices entry by entry: one card per entry, each its own slice of the printed line.'
NO_ANSWER = 'The scheme prints no answer here, only what earns the marks.'
LADDER = 'One response of the "{notation}" ladder, carded at its first rate.'
POINTS = '{n} points ("{pts}"): each printed point its own row, each on the "{notation}" ladder at its first rate.'
MENU = ('{n} ("{pts}") from the printed list, cut at the scheme\'s own solidus: one menu, claim {claim}, each on '
        'the "{notation}" ladder at its first rate.')
EG_OPEN = 'The scheme prints this answer after "e.g.": an example, an open menu.'
LEAD_IN = 'The card carries the printed lead-in "Explain what is meant by" in its question text.'
DRAWING = ('The scheme prices the drawing on its own, "{band}" for the diagram and "3(1)" for three labels, beside '
           'the part\'s ladder: the diagram is one criterion row (its band the row\'s note), the labels {labels}.')
BAND = 'The scheme prints the diagram\'s band "{band}".'


def at(page, *path_and_marker, why=NO_REPRINT, nth=1):
    """The part's own marker under its printed question (and letter) lines on the scheme page."""
    *path, marker = path_and_marker
    return SQ(page, marker, path=path, paired=why, bare=True, nth=nth)


def welded(page, *path_and_marker):
    """The part's marker opening its own answer line ("(iv) To inactivate enzymes")."""
    *path, marker = path_and_marker
    return SQ(page, marker, path=path, paired=WELDED, bare=True, welded=True)


def ask(page, sentence, **kw):
    """A one-line ask closed by its own punctuation, before its answer line."""
    return Q(page, sentence, sentence, **kw)


def eg(start, end=None, **kw):
    """A scheme answer printed after its "e.g.": the answer itself, cut after the scheme's own "e.g."."""
    return S(start, end, piece=2, psep='e.g. ', **kw)


def bracket(start, end=None, cut=' [', **kw):
    """The answer before the scheme's bracketed direction ("Throat or Pharynx [allow ...]")."""
    return S(start, end, piece=1, psep=cut, **kw)


def direction(start, end=None, cut=' [', close=']', **kw):
    """The scheme's bracketed direction itself, without its brackets: the row's note."""
    return S(start, end, piece=[2, 1], psep=[cut, close], **kw)


def points(start, end=None, k=None, tail=' (Two', sep='/', **kw):
    """A line closed by the scheme's own point count ("(Two points)"): the line before it, or its
    k-th solidus piece."""
    if k is None:
        return S(start, end, piece=1, psep=tail, **kw)
    return S(start, end, piece=[1, k], psep=[tail, sep], **kw)


def cells(line, k, sep='; ', page=None):
    """Cell k of a scheme line printed as "A = ...; B = ...", cut at its own separator."""
    return S(line, page=page, piece=k, psep=sep)


def meaning(line, k, sep='; ', page=None):
    """The answer alone of cell k (after its " = "), for a figure's label key."""
    return S(line, page=page, piece=[k, 2], psep=[sep, ' = '])


# ------------------------------------------------------------ question text --
Q1 = Q(2, 'The diagram shows the carbon cycle.')
Q2 = Q(2, 'Indicate whether each of the following statements is true (T) or false (F) by drawing a circle around T or F',
       'in each case.')
Q3 = Q(3, 'The diagram shows a cell.')
Q4 = [Q(3, 'Choose each term from the following list and place it in Column A to match a description from Column B.',
        'The first one has been completed as an example.'),
      Q(3, 'Dominant Gamete Gene Mutation Genetics Genotype')]
Q5 = Q(4, 'The diagram shows the external and internal structure of the human ear.')
Q6 = Q(5, 'The diagram below shows the internal structure of a leaf.')
Q7 = Q(6, 'In one of your laboratory activities you isolated DNA from a plant tissue.')
Q7BII = Q(6, 'Detergent and salt were added to the chopped plant material, which was then heated.')
Q8B = Q(7, 'Answer the following questions in relation to your investigation into the effect of pH on the rate of',
        'enzyme activity.')
Q8BI = ask(7, 'Name the enzyme you used in this investigation.')
Q8BV = ask(7, 'Name one factor you kept constant..')
Q8B_LADDER = '2(6) + 4(2) +1'
Q9B = Q(8, 'Answer the following questions in relation to how you prepared and examined with a microscope a',
        'transverse section (T.S.) of a dicotyledonous stem.')
Q10A = Q(9, 'In ecology we study ecosystems, habitats and communities, in which every organism has its own', 'niche.')
Q10A_LEAD = Q(9, 'Explain what is meant by')
Q11A = Q(10, 'Many characteristics are passed on to children by their parents.')
Q11B = Q(10, 'When a pure-breeding black cat was mated with a pure-breeding white cat, all the kittens were black.')
Q11BII = Q(10, 'Using capital letters for dominant and lower case letters for recessive, give:')
Q11BIII = ask(10, 'Is the genotype of the kittens referred to as homozygous or heterozygous?')
Q11C = Q(10, 'The diagram shows a short section of a DNA molecule.')
Q12BI = Q(11, 'Which biological process is represented by the following word equation:',
          'glucose + oxygen → carbon dioxide + water + energy?')
Q12BIV = Q(11, 'Write a word equation to show what happens when yeast breaks down glucose', 'in the absence of oxygen.')
Q12CI = Q(11, 'Draw a labelled diagram of the apparatus you used to investigate the effect of light',
          'intensity or carbon dioxide concentration on the rate of photosynthesis.')
Q13BII = ask(12, 'Give one role for each of the following types of teeth:')
Q13BIV = ask(12, 'Describe the following changes that happen to food in the stomach:')
Q13C = Q(12, 'The liver, the gall bladder and the pancreas all play a part in digestion. Digested food is',
         'Undigested food enters the large intestine.')
Q14A = Q(13, 'The diagram shows the human male reproductive system.')
Q14B = Q(13, 'The diagram shows a foetus in the uterus.')
Q14CII = Q(13, 'Name the part of the flower in each case')
Q14CV = ask(13, 'What term is given to the growth of an embryo into a plant?')
Q15A = Q(14, 'Water is vital for the survival of living things. Plants absorb water from the soil.')
Q15AIII = ask(14, 'Name the tissue that water travels through in a plant.')
Q15B = Q(14, 'The diagram shows the bones of the human arm.')
Q15C = Q(14, 'Rhizopus is a type of mould often found growing on stale bread.')
Q15CIII = ask(14, 'What form of heterotrophic nutrition does Rhizopus have?')
Q15CV = ask(14, 'To what kingdom does Rhizopus belong?')

# ------------------------------------------------------- scheme cell lines --
CARBON = ('A = respiration / B = photosynthesis / C = consumption', '‘assimilation’]')
FOSSIL = 'Fossil fuel(s) or named example(s) of fossil fuel(s)'
CELL = 'A = (Large) vacuole; B = chloroplasts; C = (Cell) membrane'
EAR = 'A = Semi-circular canals; B = Cochlea'
GASES = ('Air or water (vapour) or O2 or CO2 or N2 or chemicals - in and/or', 'out')
PROFILING = ('Analysing or examining a person’s DNA (to compare patterns with', 'patterns or bands')
PROTEASE = ('To digest the protein (in the chromosomes) [allow ‘to unravel', 'DNA’]')
ETHANOL = ('Add freezer-cold ethanol or alcohol [allow ‘ice-cold ethanol or', 'alcohol’]')
PH = ('(A measure of) how acidic or alkaline a solution is [allow ‘neutral', 'or not’]')
ENZYME = 'Name of enzyme: amylase or pepsin or catalase'
SECTION = 'Make section: cut/scalpel or (backed) blade/thinly/safety point'
PREPARE = ('Prepare for examination: section into water/onto slide/', 'cover slip on/how/stain/how (Two points)')
EXAMINE = ('Light source/low power objective first/ look through eyepiece /move',
           'to higher objective/coarse focus knob/fine focus knob')
ECOSYSTEM = 'Organisms/interacting/in their environment'
NICHE = ('The (functional) role (of an organism) or ‘occupation’ (of an', 'organism)')
CHAIN = ('Food chain: Must have at least three members and must match', 'named ecosystem. (Three points)')
NB = ('[N.B.: if chain does not match ecosystem, disallow the point with the', 'lowest mark]')
TROPHIC = 'A = producers; B = (primary) consumers or herbivores;'
TROPHIC_C = 'C = secondary consumers or carnivores or predators'
GAMETES = 'B and b [both letters must be given for any marks to be awarded]'
METABOLISM = ('(The sum of all) the chemical reactions (in an organism)', 'or catabolism + anabolism')
ENERGY = ('e.g. For movement/for heat/for making products/for internal', 'transport (Two points)')
EQUATION = '(Glucose →) Ethanol [allow ‘alcohol’]/ + CO2 /+ energy (Two points)'
BUBBLES = '(Counted number of ) bubbles/per unit time (Two points)'
RELATIONSHIP = ('As either light intensity or CO2 conc. increases, the rate of', 'photosynthesis increases.')
YIELD = ('Extra CO2/increase temperature/growth promotors/increase light/', 'add fertilizer (Two points)')
DIET = ('(One which contains) all the food types/in correct or suitable or', 'optimum proportions (Two points)')
AUTOTROPHIC = ('Autotrophic nutrition: Food synthesised from simple molecules',
               'or produces own food (Either point answered)')
HETEROTROPHIC = ('Heterotrohic nutrition: Already synthesised food consumed from',
                 'other organisms or food from other sources')
PERISTALSIS = ('(Muscular) contractions/in the walls of the alimentary canal/to move', 'food (Two points)')
CHEMICAL = ('pH changes or broken down by acid or broken down by', 'enzymes or proteins → peptides')
PANCREAS = ('Pancreas: Makes enzymes or makes neutralising secretion or', 'makes NaHCO3')
LIVER = ('Heat generation/vitamin storage/iron storage/makes',
         'poisons/makes plasma protein/breaks down blood cells (Two points)')
BACTERIA = ('Synthesise vitamins/out-compete pathogens or complement immune', 'system /break down fibre (Two points)')
MALE = 'A = prostate; B = urethra; C = testis; D = vas deferens or sperm duct'
SECONDARY = ('Deep voice/enlarged testes/enlarged penis/facial hair/chest', 'musculature/increase sex drive (Two points)')
PLACENTA = ('To allow nutrients/O2/antibodies to pass to child/to allow CO2 out/to', 'mother’s blood pressure (Two points)')
BIRTH = ('Oxytocin increases/progesterone decreases/uterus contracts/waters', 'out (Three points)')
CONTRACEPTION = ('Condom/pill/IUD/cap/diaphragm/spermicide/', 'surgical/chemical/mechanical/natural/rythym/implants')
CONDITIONS = ('Suitable temperature/moisture/O2 [Allow ‘pH’ and allow ‘light’ if',
              'light is linked to ‘some seeds’ or specifically named seed]')
XYLEM_LABELS = ('Labels: vessel or tracheid/pits or rings or spirals/lignin/hollow or',
                'dead [allow valid labels for other given tissue] [three labels]')
DARKNESS = ('Reason: photosynthesis stops or stomata close in darkness or night-', 'time is cooler (One point)')
PROTECTION = 'Thorns/stings/bad taste/poison/mimicry/cuticle/heat shock proteins'
ARM = 'A = Shoulder blade; B = Humerus; C = Ulna'
SKELETON = ('Protection or body support or shape or blood cell production or', 'muscle attachment')
RHIZOPUS_LABELS = 'Labels: hypha/sporangium/sporangiophore'
FEEDING = 'Secretes enzymes/onto bread/digests/absorbs products (Two points)'
HARMFUL = ('Name or effect: Rhizopus or mildew or rusts or smuts or blight or', 'dry rot (fungus) or athlete’s foot (fungus)')


def carbon_labels(asked=None):
    # (a) names A-D, cut at the scheme's own " / "; (b) names X, before its "or named example(s)".
    keys = [L(x, S(*CARBON, page=5, piece=[k, 2], psep=[' / ', ' = ']), x == asked)
            for k, x in ((1, 'A'), (2, 'B'), (3, 'C'))]
    keys.append(L('D', S(*CARBON, page=5, piece=[4, 1, 2], psep=[' / ', ' [', ' = ']), asked == 'D'))
    keys.append(L('X', S(FOSSIL, page=5, piece=1, psep=' or '), asked == 'X'))
    return keys


def cell_labels(asked=None):
    return [L(x, meaning(CELL, k, page=5), x == asked) for k, x in ((1, 'A'), (2, 'B'), (3, 'C'))]


def ear_labels(asked=None):
    return [L(x, meaning(EAR, k, page=5), x == asked) for k, x in ((1, 'A'), (2, 'B'))]


def trophic_labels(asked=None):
    keys = [L(x, S(TROPHIC, page=7, piece=[k, 2], psep=[';', ' = ']), x == asked) for k, x in ((1, 'A'), (2, 'B'))]
    keys.append(L('C', S(TROPHIC_C, page=7, piece=2, psep=' = '), asked == 'C'))
    return keys


def bases_labels(asked=None):
    return [L(x, S(ans, page=7), x == asked) for x, ans in (('1', 'Thymine or T'), ('2', 'Cytosine or C'))]


def male_labels(asked=None):
    return [L(x, meaning(MALE, k, page=9), x == asked) for k, x in ((1, 'A'), (2, 'B'), (3, 'C'), (4, 'D'))]


def arm_labels(asked=None):
    return [L(x, meaning(ARM, k, page=10), x == asked) for k, x in ((1, 'A'), (2, 'B'), (3, 'C'))]


TASKS = [
    # ------------------------------------------------------------ Section A --
] + [
    T(f'1a-{x.lower()}', 'Q1(a)', 'A', ask(2, 'Name the processes A, B, C, and D.'), [row], 'bio-3-2', concept,
      at(5, '1.', '(a)'), 7, stem=[Q1], fig='q1-carbon', item=(x.lower(), x), labels=carbon_labels(x),
      decision=EACH_ITEM + ' Four responses of the "2(7) + 2 + 4(1)" ladder, one per letter, cut at the scheme\'s own '
                           '" / ", each at the ladder\'s first rate.' + extra)
    for x, row, concept, extra in [
        ('A', pt(S(*CARBON, piece=1, psep=' / '), 7), 'respiration-in-the-carbon-cycle', ''),
        ('B', pt(S(*CARBON, piece=2, psep=' / '), 7), 'photosynthesis-in-the-carbon-cycle', ''),
        ('C', pt(S(*CARBON, piece=3, psep=' / '), 7), 'consumption-in-the-carbon-cycle', ''),
        ('D', pt(S(*CARBON, piece=[4, 1], psep=[' / ', ' [']), 7,
                 note_sel=S(*CARBON, piece=[4, 2, 1], psep=[' / ', ' [', ']'])),
         'combustion-in-the-carbon-cycle',
         ' The bracketed "allow ‘decomposition’, allow ‘assimilation’" is printed after D\'s answer, on D\'s line: the '
         'row\'s note.')]
] + [
    T(f'1{x}', f'Q1({x})', 'A', q, [row], 'bio-3-2', concept, at(5, '1.', f'({x})'), 7,
      stem=[Q1] if fig else [], fig='q1-carbon' if fig else None, labels=carbon_labels(asked) if fig else None,
      decision=decision)
    for x, q, row, concept, fig, asked, decision in [
        ('b', ask(2, 'Name the substances labelled X.'), pt(S(FOSSIL), 7), 'fossil-fuels', True, 'X',
         LADDER.format(notation='2(7) + 2 + 4(1)')),
        ('c', ask(2, 'Why are elements recycled in nature?'), pt(S('Limited supply or words to that affect or reused'), 7),
         'why-elements-are-recycled', False, None, LADDER.format(notation='2(7) + 2 + 4(1)')),
        ('d', ask(2, 'Name one group of organisms responsible for process 1 in the diagram.'),
         anyn(eg('e.g. bacteria or fungi or microorganisms or earthworms or', 'insects'), 1, 7, open_list=True,
              sep=' or '), 'decomposers', True, None,
         LADDER.format(notation='2(7) + 2 + 4(1)') + ' ' + EG_OPEN + ' Cut at the scheme\'s own "or".')]
] + [
    T(f'2{r}', f'Q2({r})', 'A', ask(2, stmt), [pt(S(ans), 7)], 'bio-1-2', concept, at(5, '2.', f'({r})'), 7, stem=[Q2],
      decision=LADDER.format(notation='2(7) + 2 + 4(1)') + ' The scheme prints the answer as the word.')
    for r, stmt, ans, concept in [
        ('i', 'Cellulose is a protein.', 'False', 'cellulose-is-a-carbohydrate'),
        ('ii', 'Iodine turns starch to a blue-black colour.', 'True', 'iodine-test-for-starch'),
        ('iii', 'Lipids are made of amino acids.', 'False', 'what-lipids-are-made-of'),
        ('iv', 'All vitamins are fat soluble.', 'False', 'fat-and-water-soluble-vitamins'),
        ('v', 'Eggs are a good source of fat in the diet.', 'True', 'eggs-as-a-source-of-fat'),
        ('vi', 'Nitrogen is a trace element.', 'False', 'nitrogen-is-a-major-element'),
        ('vii', 'Glucose is a monosaccharide.', 'True', 'glucose-is-a-monosaccharide')]
] + [
    T('3a', 'Q3(a)', 'A', [ask(3, 'Is this a plant cell or an animal cell?'),
                           ask(3, 'Give two reasons for the answer given above.', br=True)],
      [pt(S('Plant cell'), 7),
       anyn(S('1./2. e.g. cell wall/definite shape/chloroplasts/(large) vacuole', piece=2, psep='e.g. '), 2, 7,
            open_list=True)],
      'bio-1-3', 'plant-or-animal-cell', at(5, '3.', '(a)'), 21, stem=[Q3], fig='q3-cell',
      decision='Three responses of the "2(7) + 2 + 4(1)" ladder, each at its first rate: "Plant cell", and the two '
               'reasons the scheme prints as "1./2. e.g. cell wall/definite shape/chloroplasts/(large) vacuole (Two '
               'points)", cut at its own solidus, an open menu (its "e.g."), claim two.'),
] + [
    T(f'3b-{x.lower()}', 'Q3(b)', 'A', ask(3, 'Name the structures labelled A, B and C in the diagram.'),
      [pt(cells(CELL, k), 7)], 'bio-1-3', concept, at(5, '3.', '(b)'), 7, stem=[Q3], fig='q3-cell',
      item=(x.lower(), x), labels=cell_labels(x),
      decision=EACH_ITEM + ' Three responses of the "2(7) + 2 + 4(1)" ladder, one per letter, cut at the scheme\'s own '
                           'semicolons, each at the ladder\'s first rate.')
    for k, x, concept in [(1, 'A', 'vacuole'), (2, 'B', 'chloroplasts'), (3, 'C', 'cell-membrane')]
] + [
    T('3c', 'Q3(c)', 'A', ask(3, 'Name a substance found in A.'),
      [pt(S('Water or sugar or sap or salt(s) or named gases or protein'), 7)], 'bio-1-3', 'contents-of-the-vacuole',
      at(5, '3.', '(c)'), 7, stem=[Q3], fig='q3-cell', labels=cell_labels('A'),
      decision=LADDER.format(notation='2(7) + 2 + 4(1)')),
] + [
    T(f'4{r}', f'Q4({r})', 'A', ask(3, desc), [pt(S(ans), 7)], topic, concept, at(5, '4.', f'({r})'), 7, stem=Q4,
      qfig='q4-table',
      decision=LADDER.format(notation='2(7) + 3(2)') + ' The list of terms (its "Genetics" struck through as the worked '
                                                         'example) and the table are shown as the question\'s own print.')
    for r, desc, ans, topic, concept in [
        ('i', 'The genetic make up of an individual', 'Genotype', 'bio-1-4', 'genotype'),
        ('ii', 'A sex cell', 'Gamete', 'bio-1-4', 'gamete'),
        ('iii', 'A change in the structure of DNA', 'Mutation', 'bio-2-3', 'mutation'),
        ('iv', 'A part of DNA with information to make one protein', 'Gene', 'bio-1-4', 'gene'),
        ('v', 'The allele expressed in the heterozygous condition', 'Dominant', 'bio-1-4', 'dominant')]
] + [
    T(f'5i-{x.lower()}', 'Q5(i)', 'A', ask(4, 'Name the parts labelled A and B.'), [pt(cells(EAR, k), 7)], 'bio-2-4',
      concept, at(5, '5.', '(i)'), 7, stem=[Q5], fig='q5-ear', item=(x.lower(), x), labels=ear_labels(x),
      decision=EACH_ITEM + ' Two responses of the "2(7) + 2 + 4(1)" ladder, one per letter, cut at the scheme\'s own '
                           'semicolon.')
    for k, x, concept in [(1, 'A', 'semicircular-canals'), (2, 'B', 'cochlea')]
] + [
    T(f'5{r}', f'Q5({r})', 'A', q, rows, 'bio-2-4', concept, at(5, '5.', f'({r})'), total,
      stem=[Q5] if fig else [], fig='q5-ear' if fig else None, labels=ear_labels(asked) if fig else None,
      decision=decision)
    for r, q, rows, concept, total, fig, asked, decision in [
        ('ii', ask(4, 'What is the function of B?'), [pt(S('Hearing'), 7)], 'function-of-the-cochlea', 7, True, 'B',
         LADDER.format(notation='2(7) + 2 + 4(1)')),
        ('iii', ask(4, 'What is connected to the middle ear by the Eustachian tube?'),
         [pt(bracket('Throat or Pharynx [allow'), 7, note_sel=direction('Throat or Pharynx [allow'))],
         'eustachian-tube', 7, True, None,
         LADDER.format(notation='2(7) + 2 + 4(1)') + ' Its bracketed "allow ‘back of mouth’" is the row\'s note.'),
        ('iv', ask(4, 'What is the function of the Eustachian tube?'),
         [pt(S('To equalise pressure (on the eardrum) or air in or air out or', 'protection'), 7)],
         'function-of-the-eustachian-tube', 7, True, None, LADDER.format(notation='2(7) + 2 + 4(1)')),
        ('v', Q(4, 'Name one disorder of the ear or of the eye and give a corrective measure for the disorder you have',
                'named.'),
         [pt(S('Disorder:', piece=1, psep=':'), 7, kind='criterion', note=NO_ANSWER),
          pt(S('Corrective measure:', piece=1, psep=':'), 7, kind='criterion', note=NO_ANSWER)],
         'ear-or-eye-disorder', 14, False, None,
         'Two responses of the "2(7) + 2 + 4(1)" ladder, each at its first rate. The scheme prints only "Disorder:" '
         'and "Corrective measure:", each on its own line with no answer after it: a criterion row each, cut at its '
         'own colon.')]
] + [
    T(f'6{r}', f'Q6({r})', 'A', q, [row], 'bio-2-6', concept, at(5, '6.', f'({r})'), 7, stem=[Q6], fig='q6-leaf',
      decision=LADDER.format(notation='2(7) + 3(2)') + extra)
    for r, q, row, concept, extra in [
        ('i', ask(5, 'Name the one tissue type that is found at both V and Y.'), pt(S('(Epi)dermal'), 7),
         'epidermis', ''),
        ('ii', Q(5, 'The cells at W contain many organelles that carry out photosynthesis.',
                 'Suggest why the cells at W contain more of these organelles than the cells at X.'),
         pt(S('W is usually closer to the light'), 7), 'palisade-and-light', ''),
        ('iii', Q(5, 'In layer X, gases can diffuse throughout the leaf.', 'Name one such gas.'),
         pt(S(*GASES, piece=1, psep=' - '), 7, note_sel=S(*GASES, piece=2, psep=' - ')), 'gases-in-the-leaf',
         ' Its closing "in and/or out", printed after a dash, is the row\'s note.'),
        ('iv', ask(5, 'State one function of the opening at Z.'),
         pt(S('To allow gas exchange or transpiration or temperature control'), 7), 'function-of-stomata', ''),
        ('v', ask(5, 'Name the cells which are responsible for controlling the size of the opening at Z.'),
         pt(S('Guard cells'), 7), 'guard-cells', '')]
] + [
    # ------------------------------------------------------------ Section B --
    T('7ai', 'Q7(a)(i)', 'B', ask(6, 'Where in plant cells is DNA found?'),
      [pt(S('Nucleus or chloroplasts or mitochondria'), 5)], 'bio-1-2', 'where-dna-is-found',
      at(6, '7.', '(a)', '(i)'), 5, stem=[Q7], decision=LADDER.format(notation='5+1')),
    T('7aii', 'Q7(a)(ii)', 'B', ask(6, 'What is meant by DNA profiling?'), [pt(S(*PROFILING), 5)], 'bio-3-3',
      'dna-profiling', at(6, '7.', '(a)', '(ii)'), 5, decision=LADDER.format(notation='5+1')),
] + [
    T(f'7b{r}', f'Q7(b)({r})', 'B', q, [row], 'bio-1-2', concept, sq, 6, stem=[Q7] + stem, decision=decision)
    for r, q, row, concept, sq, stem, decision in [
        ('i', ask(6, 'Give one reason why you first chopped the plant material into very small pieces.'),
         pt(S('To increase surface area or to burst cells or to break cell walls'), 6), 'chopping-plant-material',
         at(6, '7.', '(b)', '(i)'), [], LADDER.format(notation='2(6)+6(2)')),
        ('ii', Q(6, 'Detergent and salt were added to the chopped plant material, which was then heated.',
                 'Explain why the detergent was used.'),
         pt(S('To break down cell membranes or to burst cells'), 6), 'detergent-in-dna-isolation',
         at(6, '7.', '(b)', '(ii)'), [], LADDER.format(notation='2(6)+6(2)')),
        ('iii', ask(6, 'How was this mixture heated?'), pt(S('In a water bath'), 6), 'heating-the-mixture',
         at(6, '7.', '(b)', '(iii)'), [M('(ii)', 6), Q7BII], LADDER.format(notation='2(6)+6(2)')),
        ('iv', ask(6, 'Why was this mixture heated?'), pt(S('To inactivate enzymes'), 6), 'why-the-mixture-is-heated',
         welded(6, '7.', '(b)', '(iv)'), [M('(ii)', 6), Q7BII], LADDER.format(notation='2(6)+6(2)')),
        ('v', Q(6, 'Later in the activity the mixture was blended for a maximum of 3 seconds.',
                'What would happen to the DNA if the mixture was blended for longer than 3 seconds?'),
         pt(S('It would be shredded'), 6), 'blending-time', at(6, '7.', '(b)', '(v)'), [],
         LADDER.format(notation='2(6)+6(2)')),
        ('vi', Q(6, 'Protease was then added to the mixture.', 'Why was protease added?'),
         pt(bracket(*PROTEASE), 6, note_sel=direction(*PROTEASE)), 'protease-in-dna-isolation',
         at(6, '7.', '(b)', '(vi)'), [],
         LADDER.format(notation='2(6)+6(2)') + ' Its bracketed "allow ‘to unravel DNA’" is the row\'s note.'),
        ('vii', Q(6, 'The mixture was then filtered.', 'After filtration, where was the DNA of your plant tissue to be '
                                                       'found?'),
         pt(S('In the filtrate or liquid or solution or test tube'), 6), 'dna-in-the-filtrate',
         at(6, '7.', '(b)', '(vii)'), [], LADDER.format(notation='2(6)+6(2)')),
        ('viii', ask(6, 'What should you do next to make the DNA visible?'),
         pt(bracket(*ETHANOL), 6, note_sel=direction(*ETHANOL)), 'ice-cold-ethanol', at(6, '7.', '(b)', '(viii)'), [],
         LADDER.format(notation='2(6)+6(2)') + ' Its bracketed "allow ‘ice-cold ethanol or alcohol’" is the row\'s '
                                               'note.')]
] + [
    T('8ai', 'Q8(a)(i)', 'B', ask(7, 'What is an enzyme?'), [pt(S('A (biological) catalyst or explained'), 5)],
      'bio-2-1', 'enzyme', at(6, '8.', '(a)', '(i)'), 5, decision=LADDER.format(notation='5+1')),
    T('8aii', 'Q8(a)(ii)', 'B', ask(7, 'Explain what is meant by the term pH.'),
      [pt(bracket(*PH), 5, kind='point', note_sel=direction(*PH))], 'bio-2-1', 'ph', at(6, '8.', '(a)', '(ii)'), 5,
      decision=LADDER.format(notation='5+1') + ' One definition ("acidic or alkaline" is its own wording, not two '
                                               'alternatives); its bracketed "allow ‘neutral or not’" is the row\'s '
                                               'note.'),
] + [
    T(f'8b{r}', f'Q8(b){ref}', 'B', q, rows, 'bio-2-1', concept, at(6, '8.', '(b)', f'({roman})'), total,
      stem=[Q8B] + stem, fig='q8-axes' if r == 'vii' else None, decision=decision)
    for r, ref, roman, q, rows, concept, total, stem, decision in [
        ('i', '(i)', 'i', Q8BI, [pt(S(ENZYME), 6)], 'enzyme-used', 6, [], LADDER.format(notation=Q8B_LADDER)),
        ('ii1', '(ii)1', 'ii', [Q(7, 'Name', nth=2), Q(7, '1. The substrate of this enzyme.',
                                                      '1. The substrate of this enzyme.', br=True)],
         [pt(S('Matching substrate'), 6, kind='criterion', note=NO_ANSWER)], 'substrate-of-the-enzyme', 6,
         [M('(i)', 7), Q8BI],
         EACH_ITEM + ' Each numbered item a response of the "' + Q8B_LADDER + '" ladder, read after the scheme\'s own '
         'number. The scheme prices a substrate matching the named enzyme without naming one: a criterion row.'),
        ('ii2', '(ii)2', 'ii', [Q(7, 'Name', nth=2), Q(7, '2. The product of this enzyme.',
                                                      '2. The product of this enzyme.', br=True)],
         [pt(S('Matching product'), 6, kind='criterion', note=NO_ANSWER)], 'product-of-the-enzyme', 6,
         [M('(i)', 7), Q8BI],
         EACH_ITEM + ' The scheme prices a product matching the named enzyme without naming one: a criterion row.'),
        ('iii', '(iii)', 'iii', ask(7, 'Draw a labelled diagram of the apparatus you used in your investigation.'),
         [pt(S('Diagram: [minimum of test tube with substance in it]'), 2, kind='criterion',
             note=BAND.format(band='2, 0')),
          pt(S('Label: [one label]'), 1, kind='criterion', note=NO_ANSWER)],
         'drawing-the-enzyme-apparatus', 3, [],
         'The scheme prices the drawing on its own beside the part\'s "' + Q8B_LADDER + '" ladder: "Diagram: [minimum '
         'of test tube with substance in it]" banded "2, 0" and "Label: [one label]" priced "1", a criterion row '
         'each (the scheme names no label).'),
        ('iv', '(iv)', 'iv', ask(7, 'How did you vary the pH?'), [pt(S('Add acid or add base or add (different) buffers'), 6)],
         'varying-the-ph', 6, [], LADDER.format(notation=Q8B_LADDER)),
        ('v', '(v)', 'v', Q8BV, [pt(S('Temperature'), 6)], 'factor-kept-constant', 6, [],
         LADDER.format(notation=Q8B_LADDER) + ' The paper prints the ask with a doubled full stop ("constant.."); '
                                              'lifted as printed.'),
        ('vi', '(vi)', 'vi', ask(7, 'How did you keep the named factor constant?'), [pt(S('Water bath'), 6)],
         'keeping-the-factor-constant', 6, [M('(v)', 7), Q8BV], LADDER.format(notation=Q8B_LADDER)),
        ('vii', '(vii)', 'vii',
         ask(7, 'Draw a graph, on the axes given below, to show the results of this investigation.'),
         [pt(S('Graph – any line that is not parallel to x axis and that is not ‘V’', 'shaped'), 6, kind='criterion',
             note=NO_ANSWER)], 'graph-of-ph-and-enzyme-activity', 6, [],
         LADDER.format(notation=Q8B_LADDER) + ' The scheme prints what the graph must show, not a graph: a criterion '
                                              'row. The printed axes are the card\'s figure.')]
] + [
    T('9ai', 'Q9(a)(i)', 'B', ask(8, 'In biology, what is meant by the term organ?'),
      [pt(S('A group of tissues (working together)'), 5)], 'bio-1-3', 'organ', at(6, '9.', '(a)', '(i)'), 5,
      decision=LADDER.format(notation='5+1')),
    T('9aii', 'Q9(a)(ii)', 'B', Q(8, 'In school, a light microscope is normally used to examine cells and tissues.',
                                   'greater detail (cell ultrastructure).'),
      [pt(S('Electron microscope'), 5)], 'bio-1-3', 'electron-microscope', at(6, '9.', '(a)', '(ii)'), 5,
      decision=LADDER.format(notation='5+1')),
] + [
    T(f'9b{r}', f'Q9(b)({r})', 'B', q, rows, 'bio-2-6', concept, at(6, '9.', '(b)', f'({r})'), total, stem=[Q9B],
      fig=fig, decision=decision)
    for r, q, rows, concept, total, fig, decision in [
        ('i', ask(8, 'Name the plant that you used.'),
         [pt(S('Any named dicot plant'), 6, kind='criterion', note=NO_ANSWER)], 'dicot-plant-used', 6, None,
         LADDER.format(notation='2(6)+6(2)') + ' The scheme prices a named dicot without naming one: a criterion '
                                                'row.'),
        ('ii', ask(8, 'How did you make a section of the stem and prepare it for examination?'),
         [anyn(S(SECTION, piece=2, psep=': '), 2, 6, note_sel=S(SECTION, piece=1, psep=':')),
          anyn(S(*PREPARE, piece=[2, 1], psep=[': ', ' (Two']), 2, 6, note_sel=S(*PREPARE, piece=1, psep=':'),
               note='The scheme prints "how" after "cover slip on" and after "stain": each a point of its own.')],
         'sectioning-a-stem', 24, None,
         'Four responses of the "2(6)+6(2)" ladder, each at its first rate: "Make section: ... (Two points)" and '
         '"Prepare for examination: ... (Two points)", each list cut at the scheme\'s own solidus, a menu each, claim '
         'two; each menu\'s printed heading is its note.'),
        ('iii', Q(8, 'Describe how you examined your section of stem once you had placed the slide on the stage of',
                  'the microscope.'),
         [anyn(S(*EXAMINE), 2, 6)], 'examining-the-section', 12, None,
         MENU.format(n='Two responses', pts='(Two points)', claim='two', notation='2(6)+6(2)')),
        ('iv', ask(8, 'Which of the following diagrams, A or B, best represents what was seen on your slide?'),
         [pt(S('B'), 6)], 'ts-of-a-dicot-stem', 6, 'q9-sections',
         LADDER.format(notation='2(6)+6(2)') + ' The two printed diagrams are the card\'s figure.')]
] + [
    # ------------------------------------------------------------ Section C --
    T('10ai', 'Q10(a)(i)', 'C', [Q10A_LEAD, Q(9, 'an ecosystem', br=True)],
      [pt(S(ECOSYSTEM), 7, note_sel=S('(Any two points for full marks)', piece=[2, 1], psep=['(', ')']))],
      'bio-3-1', 'ecosystem', at(7, '10.', '(a)', '(i)'), 7, stem=[Q10A],
      decision=LADDER.format(notation='7+2(1)') + ' (i) is one of the ladder\'s three responses (with (ii) and (iii)); '
               'the scheme prints its three points, "Organisms/interacting/in their environment", with "(Any two '
               'points for full marks)": one row, read whole, the direction its note. ' + LEAD_IN),
    T('10aii', 'Q10(a)(ii)', 'C', [Q10A_LEAD, Q(9, 'a habitat', br=True)],
      [pt(S('The place where an organism lives'), 7)], 'bio-3-1', 'habitat', at(7, '10.', '(a)', '(ii)'), 7,
      stem=[Q10A], decision=LADDER.format(notation='7+2(1)') + ' ' + LEAD_IN),
    T('10aiii', 'Q10(a)(iii)', 'C', [Q10A_LEAD, Q(9, 'a niche.', br=True)], [pt(S(*NICHE), 7)], 'bio-3-1', 'niche',
      at(7, '10.', '(a)', '(iii)'), 7, stem=[Q10A], decision=LADDER.format(notation='7+2(1)') + ' ' + LEAD_IN),
    T('10bi', 'Q10(b)(i)', 'C',
      ask(9, 'Name an ecosystem you have studied and construct a simple food chain from that ecosystem.'),
      [pt(S('Name of ecosystem: (One point)', piece=1, psep=':'), 5, kind='criterion', note=NO_ANSWER),
       pt(points(*CHAIN, tail=' (Three'), 15, kind='criterion', units=[5, 5, 5], note_sel=S(*NB, piece=[2, 1],
                                                                                            psep=['[', ']']))],
      'bio-3-1', 'food-chain-from-an-ecosystem', at(7, '10.', '(b)', '(i)'), 20,
      decision='Four responses of the "3(5)+6(2)" ladder, each at its first rate: "Name of ecosystem: (One point)" '
               'and "Food chain: Must have at least three members and must match named ecosystem. (Three points)". '
               'The scheme names no ecosystem and no chain: a criterion row each, the chain\'s row worth its three '
               'points; its "N.B." on a chain that does not match is the row\'s note.'),
    T('10bii', 'Q10(b)(ii)', 'C', ask(9, 'What is meant by a trophic level?'), [pt(S('Feeding (level)'), 5)], 'bio-3-1',
      'trophic-level', at(7, '10.', '(b)', '(ii)'), 5, decision=LADDER.format(notation='3(5)+6(2)')),
] + [
    T(f'10biii-{x.lower()}', 'Q10(b)(iii)', 'C',
      ask(9, 'Name the trophic levels A, B and C in the pyramid of numbers shown below.'), [pt(sel, 5)], 'bio-3-1',
      concept, at(7, '10.', '(b)', '(iii)'), 5, fig='q10-pyramid', item=(x.lower(), x), labels=trophic_labels(x),
      decision=EACH_ITEM + ' Three responses of the "3(5)+6(2)" ladder, one per letter, cut at the scheme\'s own '
                           'semicolons.')
    for x, sel, concept in [
        ('A', S(TROPHIC, piece=1, psep=';'), 'producers'),
        ('B', S(TROPHIC, piece=2, psep=';'), 'primary-consumers'),
        ('C', S(TROPHIC_C), 'secondary-consumers')]
] + [
    T('10biv', 'Q10(b)(iv)', 'C', Q(9, 'If all the organisms at C were removed (e.g. by disease) suggest what would '
                                       'happen to', 'the organisms at B?'),
      [pt(S('(Their number would) increase'), 5)], 'bio-3-1', 'removing-a-trophic-level', at(7, '10.', '(b)', '(iv)'),
      5, fig='q10-pyramid', labels=trophic_labels(), decision=LADDER.format(notation='3(5)+6(2)')),
    T('10ci', 'Q10(c)(i)', 'C', ask(9, 'Explain the underlined words from the passage.'),
      [pt(S('Pollution: Harmful addition to an ecosystem'), 6),
       pt(points('Conservation: Management of ecosystems (Two points)'), 6)],
      'bio-3-1', 'pollution-and-conservation', at(7, '10.', '(c)', '(i)'), 12,
      stem=[Q(9, 'The great pressure put on wildlife by the growing human population has caused many species to',
              'outcomes from which humans will benefit in future years.'),
            Q(9, '(Adapted from Advanced Biology, 3rd Edition, J. Simpkins, J. I. Williams)')],
      qfig='q10c-passage',
      decision=POINTS.format(n='Two', pts='(Two points)', notation='2(6)+6(2)') + ' One per underlined word. The '
               'paper marks the words to explain by underlining them in the passage, which the text layer drops: the '
               'question is shown as printed.'),
    T('10cii', 'Q10(c)(ii)', 'C', ask(9, 'State the effect of any one named pollutant.'),
      [pt(S('Named pollutant'), 6, kind='criterion', note=NO_ANSWER),
       pt(points('Effect must match named pollutant (Two points)'), 6, kind='criterion', note=NO_ANSWER)],
      'bio-3-1', 'effect-of-a-pollutant', at(7, '10.', '(c)', '(ii)'), 12,
      decision='Two responses of the "2(6)+6(2)" ladder ("(Two points)"), each at its first rate: the scheme prices '
               '"Named pollutant" and "Effect must match named pollutant" without naming either, a criterion row '
               'each.'),
    T('10ciii', 'Q10(c)(iii)', 'C', Q(9, 'Outline one conservation measure carried out by one of the following '
                                         'industries:', 'agriculture or forestry or fisheries.'),
      [pt(points('Outline of one conservation measure (Two points)'), 12, kind='criterion', units=[6, 6],
          note=NO_ANSWER)],
      'bio-3-1', 'conservation-in-an-industry', at(7, '10.', '(c)', '(iii)'), 12,
      decision='Two responses of the "2(6)+6(2)" ladder ("(Two points)"), each at its first rate. The scheme prints '
               'no measure, only "Outline of one conservation measure": one criterion row worth its two points.'),
    T('10civ', 'Q10(c)(iv)', 'C', ask(9, 'Name one problem associated with waste disposal.'),
      [pt(S('One problem associated with waste disposal'), 6, kind='criterion', note=NO_ANSWER)], 'bio-3-1',
      'problem-of-waste-disposal', at(7, '10.', '(c)', '(iv)'), 6,
      decision=LADDER.format(notation='2(6)+6(2)') + ' The scheme names no problem: a criterion row.'),
    T('10cv', 'Q10(c)(v)', 'C', ask(9, 'State one role of microorganisms in waste management.'),
      [pt(S('To consume waste'), 6)], 'bio-3-1', 'microorganisms-in-waste-management', at(7, '10.', '(c)', '(v)'), 6,
      decision=LADDER.format(notation='2(6)+6(2)')),
] + [
    T(f'11a{r}', f'Q11(a)({r})', 'C', ask(10, q), [row], 'bio-1-4', concept, at(7, '11.', '(a)', f'({r})'), 7,
      stem=[Q11A], decision=LADDER.format(notation='7+2(1)') + extra)
    for r, q, row, concept, extra in [
        ('i', 'Give one example of an inherited human characteristic.',
         anyn(eg('e.g. eye colour'), 1, 7, open_list=True), 'inherited-characteristic', ' ' + EG_OPEN),
        ('ii', 'Give one example of a non-inherited human characteristic.',
         anyn(eg('e.g. ability to roller skate'), 1, 7, open_list=True), 'non-inherited-characteristic',
         ' ' + EG_OPEN),
        ('iii', 'Which structures in sperm and egg nuclei are responsible for biological inheritance?',
         pt(S('Chromosomes or genes or DNA'), 7), 'chromosomes-and-inheritance', '')]
] + [
    T('11bi', 'Q11(b)(i)', 'C', ask(10, 'Which fur colour, black or white, is recessive in these cats?'),
      [pt(S('White'), 5)], 'bio-1-4', 'recessive-fur-colour', at(7, '11.', '(b)', '(i)'), 5, stem=[Q11B],
      decision=LADDER.format(notation='3(5)+6(2)')),
    T('11bii1', 'Q11(b)(ii)1', 'C', [Q11BII, Q(10, '1. The genotypes of the parent cats.', br=True)],
      [pt(S('(Black parents): BB'), 5), pt(S('(White parents): bb'), 5)], 'bio-1-4', 'genotypes-of-parent-cats',
      at(7, '11.', '(b)', '(ii)'), 10, stem=[Q11B],
      decision=EACH_ITEM + ' "(Three points)" over the three genotypes: item 1 two, one per parent, each printed on its '
                           'own line, each on the "3(5)+6(2)" ladder at its first rate.'),
    T('11bii2', 'Q11(b)(ii)2', 'C', [Q11BII, Q(10, '2. The genotype of the kittens.', br=True)],
      [pt(S('(Kittens): Bb (Three points)', piece=1, psep=' (Three'), 5)], 'bio-1-4', 'genotype-of-the-kittens',
      at(7, '11.', '(b)', '(ii)'), 5, stem=[Q11B], decision=EACH_ITEM + ' Item 2 the third of the three points.'),
    T('11biii', 'Q11(b)(iii)', 'C', Q11BIII, [pt(S('Heterozygous'), 5)], 'bio-1-4', 'heterozygous',
      at(7, '11.', '(b)', '(iii)'), 5, stem=[Q11B],
      decision=LADDER.format(notation='3(5)+6(2)') + ' The scheme stars the term (exact term required).'),
    T('11biv', 'Q11(b)(iv)', 'C', ask(10, 'Give a reason for your answer to part (iii).'),
      [pt(S('One of each type of allele or ‘Bb’'), 5)], 'bio-1-4', 'reason-heterozygous', at(7, '11.', '(b)', '(iv)'),
      5, stem=[Q11B, M('(iii)', 10), Q11BIII], decision=LADDER.format(notation='3(5)+6(2)')),
    T('11bv', 'Q11(b)(v)', 'C', Q(10, 'In relation to fur colour, what will be the genotypes of the gametes that these '
                                     'kittens will', 'produce?'),
      [pt(S(GAMETES, piece=1, psep=' ['), 10, units=[5, 5], note_sel=S(GAMETES, piece=[2, 1], psep=[' [', ']']))],
      'bio-1-4', 'gametes-of-the-kittens', at(7, '11.', '(b)', '(v)'), 10, stem=[Q11B],
      decision='Two responses of the "3(5)+6(2)" ladder ("(Two points)"), each at its first rate. The scheme prints '
               'the one answer "B and b" with "[both letters must be given for any marks to be awarded]": one row '
               'worth both points, the direction its note.'),
    T('11bvi', 'Q11(b)(vi)', 'C', ask(10, 'What are alleles?'), [pt(S('Different forms of the same gene or B,b'), 5)],
      'bio-1-4', 'alleles', at(7, '11.', '(b)', '(vi)'), 5, decision=LADDER.format(notation='3(5)+6(2)')),
] + [
    T(f'11ci-{n}', 'Q11(c)(i)', 'C', ask(10, 'Name the bases numbered 1 and 2 in the diagram above.'), [pt(S(ans), 6)],
      'bio-2-3', concept, at(7, '11.', '(c)', '(i)'), 6, stem=[Q11C], fig='q11-dna', item=(n, n),
      labels=bases_labels(n),
      decision=EACH_ITEM + ' Two responses of the "2(6)+6(2)" ladder, one per numbered base, each read after the '
                           'scheme\'s own number.')
    for n, ans, concept in [('1', 'Thymine or T', 'thymine-pairs-with-adenine'),
                            ('2', 'Cytosine or C', 'cytosine-pairs-with-guanine')]
] + [
    T(f'11c{r}', f'Q11(c)({r})', 'C', q, [pt(S(ans), 6)], 'bio-2-3', concept, at(7, '11.', '(c)', f'({r})'), 6,
      decision=LADDER.format(notation='2(6)+6(2)'))
    for r, q, ans, concept in [
        ('ii', Q(10, 'Protein synthesis involves both transcription and translation.',
                 'Where in a cell does transcription occur?'), 'Nucleus', 'site-of-transcription'),
        ('iii', ask(10, 'What type of RNA is involved in transcription?'), 'Messenger or m (RNA)', 'messenger-rna'),
        ('iv', ask(10, 'In what organelle does translation occur?'), 'Ribosome', 'site-of-translation'),
        ('v', ask(10, 'Name the small biomolecules that are joined together to make a protein.'), 'Amino acids',
         'amino-acids'),
        ('vi', ask(10, 'What must happen to the newly formed protein before it can begin to work?'),
         'It must fold (into its functional shape)', 'protein-folding')]
] + [
    T('12ai', 'Q12(a)(i)', 'C', ask(11, 'What is meant by metabolism?'), [pt(S(*METABOLISM), 7)], 'bio-2-1',
      'metabolism', at(8, '12.', '(a)', '(i)'), 7, decision=LADDER.format(notation='7+2(1)')),
    T('12aii', 'Q12(a)(ii)', 'C', ask(11, 'Give two reasons why living things need energy.'),
      [anyn(S(*ENERGY, piece=[2, 1], psep=['e.g. ', ' (Two']), 2, 7, open_list=True)], 'bio-2-1',
      'why-living-things-need-energy', at(8, '12.', '(a)', '(ii)'), 14,
      decision=MENU.format(n='Two responses', pts='(Two points)', claim='two', notation='7+2(1)') + ' ' + EG_OPEN),
    T('12bi', 'Q12(b)(i)', 'C', Q12BI, [pt(S('Aerobic/respiration (Two points)', piece=[1, k], psep=[' (Two', '/']), 5)
                                      for k in (1, 2)],
      'bio-2-2', 'aerobic-respiration', at(8, '12.', '(b)', '(i)'), 10,
      decision=POINTS.format(n='Two', pts='(Two points)', notation='3(5)+6(2)') + ' "Aerobic/respiration", cut at '
                                                                                   'the scheme\'s own solidus.'),
    T('12bii', 'Q12(b)(ii)', 'C', Q(11, 'The above process occurs in two stages, Stage 1 and Stage 2, that take place '
                                       'in different', 'where in the cell Stage 2 occurs.'),
      [pt(S('Stage 1. Cytoplasm'), 5), pt(S('Stage 2. Mitochondria'), 5)], 'bio-2-2', 'sites-of-respiration',
      at(8, '12.', '(b)', '(ii)'), 10, stem=[M('(i)', 11), Q12BI],
      decision='Two responses of the "3(5)+6(2)" ladder, one per stage, each printed on its own line.'),
    T('12biii', 'Q12(b)(iii)', 'C', ask(11, 'Does the whole process release a large amount or a small amount of energy?'),
      [pt(S('Large'), 5)], 'bio-2-2', 'energy-from-aerobic-respiration', at(8, '12.', '(b)', '(iii)'), 5,
      stem=[M('(i)', 11), Q12BI], decision=LADDER.format(notation='3(5)+6(2)')),
    T('12biv', 'Q12(b)(iv)', 'C', Q12BIV,
      [anyn(None, 2, 5, options=[S(EQUATION, piece=[1, 1], psep=['/', ' [']),
                                 S(EQUATION, piece=[2, 2], psep=['/', '+ ']),
                                 S(EQUATION, piece=[3, 2, 1], psep=['/', '+ ', ' (Two'])],
            note_sel=S(EQUATION, piece=[1, 2, 1], psep=['/', ' [', ']']))],
      'bio-2-2', 'fermentation-word-equation', at(8, '12.', '(b)', '(iv)'), 10,
      decision='Two responses of the "3(5)+6(2)" ladder ("(Two points)"), each at its first rate, from the three '
               'products the scheme prints, "(Glucose →) Ethanol [allow ‘alcohol’]/ + CO2 /+ energy", cut at its own '
               'solidus and before each printed "+": a menu, claim two; the bracketed "allow ‘alcohol’" is the row\'s '
               'note.'),
    T('12bv', 'Q12(b)(v)', 'C', ask(11, 'Give one industrial application of this process.'),
      [anyn(eg('e.g. Brewing or bread making'), 1, 5, open_list=True, sep=' or ')], 'bio-2-2',
      'industrial-fermentation', at(8, '12.', '(b)', '(v)'), 5, stem=[M('(iv)', 11), Q12BIV],
      decision=LADDER.format(notation='3(5)+6(2)') + ' ' + EG_OPEN + ' Cut at the scheme\'s own "or".'),
    T('12bvi', 'Q12(b)(vi)', 'C', Q(11, 'When muscles break down glucose in the absence of oxygen, one main product is',
                                     'Name this product.'),
      [pt(S('Lactic acid'), 5)], 'bio-2-2', 'lactic-acid', at(8, '12.', '(b)', '(vi)'), 5,
      decision=LADDER.format(notation='3(5)+6(2)')),
    T('12ci', 'Q12(c)(i)', 'C', Q12CI,
      [pt(S('Diagram [test tube + water + plant]'), 3, kind='criterion', note=BAND.format(band='3,0')),
       pt(S('Labels [three labels]'), 3, kind='criterion', units=[1, 1, 1], note=NO_ANSWER)],
      'bio-2-2', 'drawing-a-photosynthesis-apparatus', at(8, '12.', '(c)', '(i)'), 6,
      decision=DRAWING.format(band='3,0', labels='"Labels [three labels]" one criterion row worth its three 1s, as '
                                                 'the scheme names none')),
    T('12cii', 'Q12(c)(ii)', 'C', ask(11, 'How did you vary the light intensity or the carbon dioxide concentration?'),
      [anyn(None, 1, 5, options=[S('Vary light: lamp at different distances from plant'),
                                 S('Vary CO2 conc.: different concs of NaHCO3 solution')])],
      'bio-2-2', 'varying-light-or-carbon-dioxide', at(8, '12.', '(c)', '(ii)'), 5, stem=[M('(i)', 11), Q12CI],
      decision='One response of the "3(5)+3(1)" ladder, carded at its first rate. The scheme prints a way for each '
               'factor, joined by "OR": a menu, claim one (the candidate answers for the factor they investigated).'),
    T('12ciii', 'Q12(c)(iii)', 'C', ask(11, 'How did you measure the rate of photosynthesis?'),
      [pt(S(BUBBLES, piece=[1, k], psep=[' (Two', '/']), 5) for k in (1, 2)], 'bio-2-2',
      'measuring-the-rate-of-photosynthesis', at(8, '12.', '(c)', '(iii)'), 10, stem=[M('(i)', 11), Q12CI],
      decision=POINTS.format(n='Two', pts='(Two points)', notation='3(5)+3(1)') + ' Cut at the scheme\'s own '
                                                                                   'solidus.'),
    T('12civ', 'Q12(c)(iv)', 'C', Q(11, 'What is the relationship between the rate of photosynthesis and either the '
                                        'light intensity', 'or the carbon dioxide concentration'),
      [pt(S(*RELATIONSHIP), 5, kind='point')], 'bio-2-2', 'rate-of-photosynthesis-and-its-factors',
      at(8, '12.', '(c)', '(iv)'), 5, stem=[M('(i)', 11), Q12CI],
      decision=LADDER.format(notation='3(5)+3(1)') + ' One statement for either factor, read whole (its "either ... '
                                                     'or" names the factors, not alternative answers). The paper '
                                                     'prints the ask without a closing question mark.'),
    T('12cv', 'Q12(c)(v)', 'C', Q(11, 'Most Irish tomatoes are grown in greenhouses. State two ways a commercial '
                                      'producer', 'could increase her/his crop yield of tomatoes.'),
      [anyn(points(*YIELD), 2, 5)], 'bio-2-2', 'increasing-crop-yield', at(8, '12.', '(c)', '(v)'), 10,
      decision=MENU.format(n='Two responses', pts='(Two points)', claim='two', notation='3(5)+3(1)')),
    T('13ai', 'Q13(a)(i)', 'C', ask(12, 'What is meant by a ‘balanced’ diet?'),
      [pt(points(*DIET, k=k), 7) for k in (1, 2)], 'bio-2-6', 'balanced-diet', at(8, '13.', '(a)', '(i)'), 14,
      decision=POINTS.format(n='Two', pts='(Two points)', notation='7+2(1)') + ' Cut at the scheme\'s own solidus.'),
    T('13aii', 'Q13(a)(ii)', 'C', ask(12, 'Distinguish between autotrophic nutrition and heterotrophic nutrition.'),
      [anyn(None, 1, 7, options=[points(*AUTOTROPHIC, tail=' (Either'), S(*HETEROTROPHIC)],
            note_sel=S(AUTOTROPHIC[1], piece=[2, 1], psep=[' (', ')']))],
      'bio-2-6', 'autotrophic-and-heterotrophic-nutrition', at(8, '13.', '(a)', '(ii)'), 7,
      decision='One response of the "7+2(1)" ladder: the "7+2(1)" makes three responses, (i)\'s two points and this '
               'one, so the scheme\'s "(Either point answered)" prices either printed explanation for the one '
               'response: a menu, claim one, the direction its note. The scheme misspells "Heterotrohic"; lifted as '
               'printed.'),
    T('13bi', 'Q13(b)(i)', 'C', ask(12, 'Explain the word digestion.'), [pt(S('The breaking down of food'), 5)],
      'bio-2-6', 'digestion', at(8, '13.', '(b)', '(i)'), 5, decision=LADDER.format(notation='3(5)+6(2)')),
    T('13bii1', 'Q13(b)(ii)1', 'C', [Q13BII, M('1.', 12, br=True), Q(12, 'Incisors')], [pt(S('Cutting (food)'), 5)],
      'bio-2-6', 'incisors', at(8, '13.', '(b)', '(ii)'), 5,
      decision=EACH_ITEM + ' Each numbered tooth a response of the "3(5)+6(2)" ladder, read after the scheme\'s own '
                           'number.'),
    T('13bii2', 'Q13(b)(ii)2', 'C', [Q13BII, M('2.', 12, br=True), Q(12, 'Molars.')],
      [anyn(S('Chewing/grinding (food)'), 1, 5)], 'bio-2-6', 'molars', at(8, '13.', '(b)', '(ii)'), 5,
      decision=EACH_ITEM + ' One response: the ladder\'s count (nine responses for "3(5)+6(2)") gives item 2 one '
                           'point, so "Chewing/grinding (food)" is read as two printed alternatives: a menu, claim '
                           'one.'),
    T('13biii', 'Q13(b)(iii)', 'C', Q(12, 'Peristalsis begins when food enters the oesophagus.',
                                       'What is meant by peristalsis?'),
      [anyn(points(*PERISTALSIS), 2, 5)], 'bio-2-6', 'peristalsis', at(8, '13.', '(b)', '(iii)'), 10,
      decision=MENU.format(n='Two responses', pts='(Two points)', claim='two', notation='3(5)+6(2)')),
    T('13biv1', 'Q13(b)(iv)1', 'C', [Q13BIV, M('1.', 12, br=True), Q(12, 'Mechanical changes')],
      [pt(S('Churned'), 5)], 'bio-2-6', 'mechanical-digestion-in-the-stomach', at(8, '13.', '(b)', '(iv)'), 5,
      decision=EACH_ITEM + ' Each numbered change a response of the "3(5)+6(2)" ladder.'),
    T('13biv2', 'Q13(b)(iv)2', 'C', [Q13BIV, M('2.', 12, br=True), Q(12, 'Chemical changes.')],
      [pt(S(*CHEMICAL), 5)], 'bio-2-6', 'chemical-digestion-in-the-stomach', at(8, '13.', '(b)', '(iv)'), 5,
      decision=EACH_ITEM + ' Item 2 one point with its printed alternatives.'),
    T('13bv', 'Q13(b)(v)', 'C', ask(12, 'What is the pH of the stomach contents?'), [pt(S('0 − 3'), 5)], 'bio-2-6',
      'stomach-ph', at(8, '13.', '(b)', '(v)'), 5, decision=LADDER.format(notation='3(5)+6(2)')),
    T('13bvi', 'Q13(b)(vi)', 'C', ask(12, 'Where does the partially digested food go when it leaves the stomach?'),
      [pt(S('Duodenum or small intestine'), 5)], 'bio-2-6', 'food-leaving-the-stomach', at(8, '13.', '(b)', '(vi)'), 5,
      decision=LADDER.format(notation='3(5)+6(2)')),
] + [
    T(f'13ci{n}', f'Q13(c)(i){n}', 'C', [Q(12, 'State'), M(f'{n}.', 12, br=True), ask(12, q)], [pt(sel, 6)],
      'bio-2-6', concept, at(8, '13.', '(c)', '(i)'), 6, stem=[Q13C],
      decision=EACH_ITEM + ' Each numbered organ a response of the "2(6)+6(2)" ladder, read after the scheme\'s own '
                           'number, its organ the row\'s label.')
    for n, q, sel, concept in [
        (1, 'One role of the pancreas in digestion.', S(*PANCREAS), 'pancreas-in-digestion'),
        (2, 'One role of the gall bladder in digestion.', S('Gall bladder: Stores bile or releases bile'),
         'gall-bladder-in-digestion')]
] + [
    T(f'13c{r}', f'Q13(c)({r})', 'C', q, [row], 'bio-2-6', concept, at(8, '13.', f'(c)', f'({r})'), total,
      stem=[Q13C], decision=decision)
    for r, q, row, concept, total, decision in [
        ('ii', ask(12, 'From what part of the digestive system does the digested food enter the blood?'),
         pt(S('Small intestine or duodenum or jejunum or ileum'), 6), 'absorption-of-digested-food', 6,
         LADDER.format(notation='2(6)+6(2)')),
        ('iii', ask(12, 'Name the blood vessel that carries the digested food to the liver.'),
         pt(S('(Hepatic) portal vein'), 6), 'hepatic-portal-vein', 6, LADDER.format(notation='2(6)+6(2)')),
        ('iv', ask(12, 'State two functions of the liver – other than the processing of digested food.'),
         anyn(points(*LIVER), 2, 6), 'functions-of-the-liver', 12,
         MENU.format(n='Two responses', pts='(Two points)', claim='two', notation='2(6)+6(2)')),
        ('v', Q(12, 'The colon contains many symbiotic bacteria – mostly ‘good’ bacteria.',
                'State two benefits we get from these bacteria.'),
         anyn(points(*BACTERIA), 2, 6), 'symbiotic-bacteria-in-the-colon', 12,
         MENU.format(n='Two responses', pts='(Two points)', claim='two', notation='2(6)+6(2)'))]
] + [
    T(f'14ai-{x.lower()}', 'Q14(a)(i)', 'C', ask(13, 'Name the parts A, B, C and D.'), [pt(cells(MALE, k), 6)],
      'bio-2-5', concept, at(9, '14.', '(a)', '(i)'), 6, stem=[Q14A], fig='q14-male', item=(x.lower(), x),
      labels=male_labels(x),
      decision=EACH_ITEM + ' Four responses of the "2(6)+6(2)" ladder, one per letter, cut at the scheme\'s own '
                           'semicolons.')
    for k, x, concept in [(1, 'A', 'prostate-gland'), (2, 'B', 'urethra'), (3, 'C', 'testis'), (4, 'D', 'sperm-duct')]
] + [
    T(f'14a{r}', f'Q14(a)({r})', 'C', ask(13, q), rows, 'bio-2-5', concept, at(9, '14.', '(a)', f'({r})'), total,
      stem=[Q14A] if fig else [], fig='q14-male' if fig else None, labels=male_labels('D') if fig else None,
      decision=decision)
    for r, q, rows, concept, total, fig, decision in [
        ('ii', 'What is the function of part D?',
         [pt(bracket('To carry sperm [allow'), 6, note_sel=direction('To carry sperm [allow'))], 'function-of-the-sperm-duct',
         6, True, LADDER.format(notation='2(6)+6(2)') + ' Its bracketed "allow ‘to carry semen’" is the row\'s note.'),
        ('iii', 'Name the principal male sex hormone.', [pt(S('Testosterone'), 6)], 'testosterone', 6, False,
         LADDER.format(notation='2(6)+6(2)')),
        ('iv', 'Name two male secondary sexual characteristics.', [anyn(points(*SECONDARY), 2, 6)],
         'male-secondary-sexual-characteristics', 12, False,
         MENU.format(n='Two responses', pts='(Two points)', claim='two', notation='2(6)+6(2)')),
        ('v', 'Draw a labelled diagram of a human sperm cell.',
         [pt(S('Diagram [must have head and tail for 3 marks]'), 3, kind='criterion', note=BAND.format(band='3, 0')),
          pt(S('Labels [three labels]'), 3, kind='criterion', units=[1, 1, 1], note=NO_ANSWER)],
         'drawing-a-sperm-cell', 6, False,
         DRAWING.format(band='3, 0', labels='"Labels [three labels]" one criterion row worth its three 1s, as the '
                                            'scheme names none'))]
] + [
    T(f'14b{r}', f'Q14(b)({r})', 'C', ask(13, q), [row], 'bio-2-5', concept, at(9, '14.', '(b)', f'({r})'), total,
      stem=[Q14B] if fig else [], fig='q14-foetus' if fig else None, decision=decision)
    for r, q, row, concept, total, fig, decision in [
        ('i', 'From what tissues is the placenta formed?',
         pt(S('Mother’s and child’s (Single point)', piece=1, psep=' (Single'), 6), 'tissues-of-the-placenta', 6, True,
         LADDER.format(notation='3(6)+6(2)') + ' "(Single point)": one row.'),
        ('ii', 'Give two functions of the placenta.', anyn(points(*PLACENTA), 2, 6), 'functions-of-the-placenta', 12,
         True, MENU.format(n='Two responses', pts='(Two points)', claim='two', notation='3(6)+6(2)')),
        ('iii', 'Describe the process of birth.', anyn(points(*BIRTH, tail=' (Three'), 3, 6), 'birth', 18, True,
         MENU.format(n='Three responses', pts='(Three points)', claim='three', notation='3(6)+6(2)')),
        ('iv', 'Give any one biological benefit of breastfeeding.',
         pt(S('Ideal nutrient or antibodies or mother-baby bond or reduced', 'infection'), 6), 'breastfeeding', 6,
         False, LADDER.format(notation='3(6)+6(2)')),
        ('v', 'List two methods of contraception.', anyn(S(*CONTRACEPTION), 2, 6), 'methods-of-contraception', 12,
         False, MENU.format(n='Two responses', pts='(Two points)', claim='two', notation='3(6)+6(2)')
         + ' The scheme misspells "rythym"; lifted as printed.')]
] + [
    T('14ci', 'Q14(c)(i)', 'C', ask(13, 'What is meant by fertilisation?'),
      [pt(S('Fusion of gametes or formation of zygote'), 6)], 'bio-2-5', 'fertilisation-in-plants',
      at(9, '14.', '(c)', '(i)'), 6, decision=LADDER.format(notation='2(6) +2(3) + 6(2)')),
] + [
    T(f'14cii{n}', f'Q14(c)(ii){n}', 'C', [Q14CII, Q(13, q, q, br=True)], [pt(S(ans), 6)], 'bio-2-5', concept,
      at(9, '14.', '(c)', '(ii)'), 6,
      decision=EACH_ITEM + ' Each numbered item a response of the "2(6) +2(3) + 6(2)" ladder, read after the scheme\'s '
                           'own number.')
    for n, q, ans, concept in [
        (1, '1. Where fertilisation occurs', 'Embryo sac or ovule or ovary or carpel', 'where-fertilisation-occurs'),
        (2, '2. That becomes the fruit.', 'Carpel or ovary or receptacle', 'part-that-becomes-the-fruit')]
] + [
    T('14ciii', 'Q14(c)(iii)', 'C',
      [Q(13, 'Each seed is made up of an embryo, a food store and a seed coat (testa). One function of fruit is',
         'to aid dispersal.'), ask(13, 'Explain each of the underlined terms.')],
      [pt(S('Embryo: (part of seed that) becomes the new plant'), 6), pt(S('Dispersal: spreading of seeds.'), 6)],
      'bio-2-5', 'embryo-and-dispersal', at(9, '14.', '(c)', '(iii)'), 12, qfig='q14c-underlined',
      decision=POINTS.format(n='Two', pts='one per term', notation='2(6) +2(3) + 6(2)') + ' The paper marks the terms '
               'by underlining them, which the text layer drops: the question is shown as printed.'),
    T('14civ', 'Q14(c)(iv)', 'C', ask(13, 'By which method is each of the fruits shown above dispersed?'),
      [pt(S('Blackberries: Animals'), 6), pt(S('Sycamore fruit: Wind'), 6)], 'bio-2-5', 'fruit-dispersal',
      at(9, '14.', '(c)', '(iv)'), 12, fig='q14-fruits',
      decision='Two responses of the "2(6) +2(3) + 6(2)" ladder, one per fruit, each printed on its own line with the '
               'fruit as its label. The two printed pictures are the card\'s figure.'),
    T('14cv', 'Q14(c)(v)', 'C', Q14CV, [pt(S('Germination'), 6)], 'bio-2-5', 'germination', at(9, '14.', '(c)', '(v)'),
      6, decision=LADDER.format(notation='2(6) +2(3) + 6(2)')),
    T('14cvi', 'Q14(c)(vi)', 'C', Q(13, 'In order for this growth to be successful, certain environmental conditions '
                                        'must be', 'Name any two of these conditions.'),
      [anyn(bracket(*CONDITIONS), 2, 6, note_sel=direction(*CONDITIONS))], 'bio-2-5', 'conditions-for-germination',
      at(9, '14.', '(c)', '(vi)'), 12, stem=[M('(v)', 13), Q14CV],
      decision=MENU.format(n='Two responses', pts='(Two points)', claim='two', notation='2(6) +2(3) + 6(2)')
      + ' Its bracketed direction allowing pH and light is the row\'s note.'),
] + [
    T(f'15a{r}', f'Q15(a)({r})', 'C', q, rows, topic, concept, at(10, '15.', '(a)', f'({r})'), total,
      stem=[Q15A] + stem, decision=decision)
    for r, q, rows, topic, concept, total, stem, decision in [
        ('i', ask(14, 'Through which microscopic structures does water enter a plant from the soil?'),
         [pt(S('Root hairs'), 6)], 'bio-2-6', 'root-hairs', 6, [], LADDER.format(notation='2(6) +6(2)')),
        ('ii', ask(14, 'By what process does water enter a plant?'), [pt(S('Osmosis'), 6)], 'bio-2-6',
         'osmosis-into-roots', 6, [], LADDER.format(notation='2(6) +6(2)')),
        ('iii', Q15AIII, [pt(bracket('Xylem [allow'), 6, note_sel=direction('Xylem [allow'))], 'bio-2-6', 'xylem', 6,
         [], LADDER.format(notation='2(6) +6(2)') + ' Its bracketed direction is the row\'s note.'),
        ('iv', ask(14, 'Draw a labelled diagram of one cell of the tissue referred to in (iii) above.'),
         [pt(S('Diagram: [any two valid structures for three marks]'), 3, kind='criterion',
             note=BAND.format(band='3, 0') + ' ' + NO_ANSWER),
          anyn(S(*XYLEM_LABELS, piece=[2, 1], psep=[': ', ' [']), 3, 1,
               note_sel=S(*XYLEM_LABELS, piece=[2, 2], psep=[': ', 'dead ']))],
         'bio-2-6', 'drawing-a-xylem-cell', 6, [M('(iii)', 14), Q15AIII],
         DRAWING.format(band='3, 0', labels='"3(1)" from the four labels the scheme prints, cut at its own solidus, a '
                                            'menu, claim three, its bracketed directions the row\'s note')),
        ('v', ask(14, 'Name one process that causes water to move upwards in a plant.'),
         [pt(S('Root pressure or cohesion or adhesion or capillarity or transpiration'), 6)], 'bio-2-6',
         'water-movement-in-xylem', 6, [], LADDER.format(notation='2(6) +6(2)')),
        ('vi', Q(14, 'Consider that night has fallen and the plant is in darkness.', 'for your answer.'),
         [pt(S('Amount of water moving through the plant: decreases (One point)', piece=1, psep=' (One'), 6),
          pt(points(*DARKNESS, tail=' (One'), 6)], 'bio-2-6', 'transpiration-at-night', 12, [],
         'Two responses of the "2(6) +6(2)" ladder, each "(One point)", a row each.'),
        ('vii', ask(14, 'State two ways by which plants have adapted to protect themselves.'),
         [anyn(S(PROTECTION), 2, 6)], 'bio-2-4', 'plant-defences', 12, [],
         MENU.format(n='Two responses', pts='(Two points)', claim='two', notation='2(6) +6(2)'))]
] + [
    T(f'15bi-{x.lower()}', 'Q15(b)(i)', 'C', ask(14, 'Name the parts labelled A, B and C.'), [pt(cells(ARM, k), 6)],
      'bio-2-4', concept, at(10, '15.', '(b)', '(i)'), 6, stem=[Q15B], fig='q15-arm', item=(x.lower(), x),
      labels=arm_labels(x),
      decision=EACH_ITEM + ' Three responses of the "3(6) + 6(2)" ladder, one per letter, cut at the scheme\'s own '
                           'semicolons.')
    for k, x, concept in [(1, 'A', 'scapula'), (2, 'B', 'humerus'), (3, 'C', 'ulna')]
] + [
    T(f'15b{r}', f'Q15(b)({r})', 'C', ask(14, q), [pt(sel, 6)], 'bio-2-4', concept, at(10, '15.', '(b)', f'({r})'), 6,
      stem=[Q15B] if fig else [], fig='q15-arm' if fig else None, decision=LADDER.format(notation='3(6) + 6(2)'))
    for r, q, sel, concept, fig in [
        ('ii', 'What structures attach a muscle to a bone?', S('Tendons'), 'tendons', False),
        ('iii', 'Which upper arm muscle contracts to raise the lower arm?', S('Biceps'), 'biceps', True),
        ('iv', 'What is meant by the term antagonistic pair in reference to muscles?',
         S('(Two) muscles that work in opposition to each other'), 'antagonistic-pair', False),
        ('v', 'Name the type of joint at the elbow.', S('Hinge or synovial or moveable'), 'elbow-joint', True),
        ('vi', 'Apart from movement, give one other function of the skeleton.', S(*SKELETON),
         'functions-of-the-skeleton', False),
        ('vii', 'Suggest one reason why the bones of birds are almost hollow.', S('To be light or to allow flight'),
         'hollow-bird-bones', False)]
] + [
    T('15ci', 'Q15(c)(i)', 'C', ask(14, 'Draw a diagram of Rhizopus and on it label a hypha, a sporangium and a '
                                        'sporangiophore.'),
      [pt(S('Diagram: [hypha and sporangiophore as minimum]'), 5, kind='criterion', note=BAND.format(band='5, 3, 0')),
       *[pt(S(RHIZOPUS_LABELS, piece=[2, k], psep=[': ', '/']), 1, label=S(RHIZOPUS_LABELS, piece=1, psep=':'))
         for k in (1, 2, 3)]],
      'bio-3-2', 'drawing-rhizopus', at(10, '15.', '(c)', '(i)'), 8, stem=[Q15C],
      decision='The scheme prices the drawing on its own, "5, 3, 0" for the diagram and "3(1)" for its three named '
               'labels, beside the part\'s "2(6) + 5(2)" ladder: the diagram one criterion row (its band the row\'s '
               'note), each printed label its own row at 1, cut at the scheme\'s own solidus.'),
] + [
    T(f'15c{r}', f'Q15(c)({r})', 'C', ask(14, q) if isinstance(q, str) else q, [row], 'bio-3-2', concept,
      at(10, '15.', '(c)', f'({r})'), total, stem=[Q15C] + stem, decision=decision)
    for r, q, row, concept, total, stem, decision in [
        ('ii', 'Explain how Rhizopus gets its food.', anyn(points(FEEDING), 2, 6), 'nutrition-of-rhizopus', 12, [],
         MENU.format(n='Two responses', pts='(Two points)', claim='two', notation='2(6) + 5(2)')),
        ('iii', Q15CIII, pt(S('Saprophytic'), 6), 'saprophytic-nutrition', 6, [], LADDER.format(notation='2(6) + 5(2)')),
        ('iv', 'Outline the importance of this type of nutrition in nature.',
         pt(S('It breaks down dead organisms or recycling of nutrients or reusing'), 6), 'importance-of-saprophytes', 6,
         [M('(iii)', 14), Q15CIII], LADDER.format(notation='2(6) + 5(2)')),
        ('v', Q15CV, pt(S('Fungi'), 6), 'kingdom-fungi', 6, [], LADDER.format(notation='2(6) + 5(2)')),
        ('vi', 'Name one economically harmful member of this kingdom.', pt(S(*HARMFUL), 6), 'harmful-fungi', 6,
         [M('(v)', 14), Q15CV],
         LADDER.format(notation='2(6) + 5(2)') + ' Its printed "Name or effect" is the row\'s label.'),
        ('vii', Q(14, 'Mushrooms also belong to this kingdom. A restaurant owner decides to collect and cook wild',
                  'Suggest one reason why this may not be a good idea.'),
         pt(bracket('Some could be poisonous [allow'), 6, note_sel=direction('Some could be poisonous [allow')),
         'wild-mushrooms', 6, [], LADDER.format(notation='2(6) + 5(2)') + ' Its bracketed "allow ‘would make you '
                                                                          'sick’" is the row\'s note.')]
]

# Drawings priced on their own beside their part's ladder: their units count to
# the ladder as fixed, their cards keep their own marks.
LADDER_EXEMPT = {'8biii', '12ci', '14av', '15aiv', '15ci'}

FIGURES = {
    # key suffix: (doc, page, rect in PDF points, credit, letters, alt, solution[, masks])
    'q1-carbon': ('paper', 2, (140, 109, 468, 302), SEC, ['A', 'B', 'C', 'D', 'X'],
        'Diagram of the carbon cycle. CO2 at the top; Humus, Plant carbohydrate and Dead organisms across the middle; '
        'Animal carbohydrate at the bottom; an empty box labelled X at the top right. Arrows: one curving down from CO2 '
        'to Plant carbohydrate, labelled B; one curving back up from Plant carbohydrate to CO2, labelled A; one up from '
        'Humus to CO2; one from Plant carbohydrate left to Humus; one curving down from Plant carbohydrate to Animal '
        'carbohydrate, labelled C; one up from Animal carbohydrate to Humus, labelled 1; a long arc up the left side '
        'from Animal carbohydrate to CO2, also labelled A; one each from Plant carbohydrate and Animal carbohydrate to '
        'Dead organisms; one up from Dead organisms to the box X; and one from X back to CO2, labelled D. Faint, '
        'mostly illegible show-through of printed text lies behind the drawing.', False),
    'q3-cell': ('paper', 3, (120, 84, 482, 210), SEC, ['A', 'B', 'C'],
        'Drawing of a rectangular cell with a thick outer border and a thin line just inside it, its interior dotted. '
        'A large, irregular clear space fills the middle; a dark round shaded body sits at the upper right; six oval '
        'bodies, each holding small dark granules, lie around the edge. A points to the large clear space, B to two '
        'of the granule-filled oval bodies, C to the thin line just inside the border at the upper right.', False),
    'q4-table': ('paper', 3, (52, 488, 566, 736), SEC, [],
        'Question 4 as printed: the instruction, then the list Dominant, Gamete, Gene, Mutation, Genetics (struck '
        'through), Genotype above a two-column table. The first row is the worked example, Genetics in Column A '
        'beside "The study of biological inheritance" in Column B; rows (i) to (v) leave Column A blank beside the '
        'descriptions "The genetic make up of an individual", "A sex cell", "A change in the structure of DNA", "A '
        'part of DNA with information to make one protein" and "The allele expressed in the heterozygous '
        'condition".', False),
    'q5-ear': ('paper', 4, (115, 64, 430, 214), SEC, ['A', 'B'],
        'Drawing of the human ear in section, with printed labels Ear lobe (the outer ear flap at the left), Middle '
        'ear (pointing into a chamber holding small bones in the middle), Eustachian tube (a tube running down from '
        'the middle ear) and Auditory nerve (nerve fibres at the right). A points to a set of looped tubes at the '
        'upper right; B points to the coiled, snail-shaped structure at the lower right.', False),
    'q6-leaf': ('paper', 5, (152, 60, 340, 232), SEC, [],
        'Drawing of a section through a leaf, in layers, each marked by a bracket and letter at the right: V, a '
        'single row of flat, clear cells along the top; W, a row of tall, column-shaped cells packed with dark '
        'granules; X, rounded cells with fewer granules and spaces between them; Y, a row of small, flat cells along '
        'the bottom. In the bottom row two small cells with dotted contents sit side by side with a narrow gap '
        'between them, and a short bar marked Z lies beneath them. Faint show-through of printed text lies above '
        'the drawing.', False),
    'q8-axes': ('paper', 7, (140, 626, 368, 782), SEC, [],
        'The blank axes printed for the graph: a vertical axis labelled Rate of enzyme activity and a horizontal axis '
        'labelled pH, with no scale and no line drawn.', False),
    'q9-sections': ('paper', 8, (128, 658, 472, 764), SEC, ['A', 'B'],
        'Two circular cross-section drawings side by side. A: a wide circle with a ridged outer band and, at its '
        'centre, a small circle holding a four-armed cross shape with a small round body in each gap between the '
        'arms. B: a circle with a thick outer rim and a ring of ten small dark patches spaced evenly just inside the '
        'rim, its centre empty.', False),
    'q10-pyramid': ('paper', 9, (238, 296, 360, 393), SEC, ['A', 'B', 'C'],
        'A triangle divided by two horizontal lines into three levels, lettered from the base up: A in the widest '
        'bottom level, B in the middle level and C in the narrow top level, with the empty apex above C.', False),
    'q10c-passage': ('paper', 9, (80, 478, 562, 614), SEC, [],
        'Question 10(c) as printed: the passage on the pressure the growing human population puts on wildlife, with '
        'the words pollution and conservation underlined, its credit line "(Adapted from Advanced Biology, 3rd '
        'Edition, J. Simpkins, J. I. Williams)", and below it part (i): "Explain the underlined words from the '
        'passage."', False),
    'q11-dna': ('paper', 10, (190, 443, 420, 576), SEC, ['1', '2', 'A', 'G'],
        'Diagram of a short section of DNA: two side strands, each a chain of pentagons and circles joined by lines, '
        'linked across by two rungs. The upper rung is a box numbered 1 joined to a box lettered A, their ends '
        'fitting together in a pointed join; the lower rung is a box lettered G joined to a box numbered 2, their '
        'ends fitting together in a curved join.', False),
    'q14-male': ('paper', 13, (165, 66, 372, 228), SEC, ['A', 'B', 'C', 'D'],
        'Outline drawing of the human male reproductive system seen from the side: a large rounded sac at the top, '
        'a tube from beneath it running down through the penis, an oval body inside a pouch at the bottom, a lumpy '
        'structure at the upper right, and a thin tube looping up from the pouch over the top. A points to a rounded '
        'body just below the large sac, B to the tube running down inside the penis, C to the oval body inside the '
        'pouch, D to the thin tube rising from the pouch.', False, [(165, 219, 283, 228)]),
    'q14-foetus': ('paper', 13, (380, 358, 522, 499), SEC, [],
        'Drawing of a foetus curled up head-down inside the womb, its knees drawn up near the top, its umbilical '
        'cord coiled beside it and running to a thick speckled layer on the inner wall of the womb at the left; the '
        'narrow neck of the womb is at the bottom. No labels are printed.', False),
    'q14c-underlined': ('paper', 13, (105, 580, 568, 632), SEC, [],
        'Part (iii) of Question 14(c) as printed: "Each seed is made up of an embryo, a food store and a seed coat '
        '(testa). One function of fruit is to aid dispersal.", with the words embryo and dispersal underlined, then '
        '"Explain each of the underlined terms."', False),
    'q14-fruits': ('paper', 13, (186, 628, 418, 716), SEC, [],
        'Two pictures side by side with printed captions: Blackberries, a photograph of three clusters of round, '
        'glossy, dark berries with a leaf behind them; and Sycamore fruit, a drawing of fruits hanging in joined '
        'pairs on long stalks beneath leaves, each fruit with a long, flat, veined extension.', False),
    'q15-arm': ('paper', 14, (455, 308, 566, 506), SEC, ['A', 'B', 'C'],
        'Drawing of the bones of the human arm, from the top of the arm down to the bones of the hand. A points to '
        'a broad, flat bone at the top right; B to the single long bone of the upper arm; C to one of the two long '
        'bones of the forearm.', False),
}
