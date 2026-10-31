"""Physics 2020 Higher Level — reviewed task ledger, carded from the paper for the first time.

Independent visual sweep (2026-10-28), every page rendered and read:
  * The paper (LC021ALP000EV), 12 pages: p1 cover ("Answer three questions from Section A and
    five questions from Section B"), p2-p3 Section A (120 marks) Questions 1-4 (experiments, 40
    marks each, group marks printed after runs of romans), p4-p11 Section B (280 marks) Questions
    5-12 (56 marks each), p11 also the acknowledgements (images on pages 4-11), p12 back cover.
  * The marking scheme, 24 pages: p1 cover, p2 note on published schemes, p3 points to note
    (solidus, double solidus, units, graphs, slips), p4 annotation symbols, p5-p19 Questions 1-12
    (each question reprinted in regular type, its answers in bold, a mark column at x 518 and a
    second column of PART totals at x 554 on the last line of each part), p20-p22 blank (footers
    [18]-[20]), p23 blank, p24 back cover.

Every printed ask is carded at the scheme's own mark boundary: a roman, a letter (Q5, Q11, and the
romans of Q10(a)/(b) and Q12(a)-(d), letter-major), or a sub-letter where the scheme prices the
paper's (a), (b), (c) inside one roman apart (Q4(i), Q10(b)(ii)). Where one cell prices a part's
sub-asks together (Q5(i) a./b. "4 + 3", Q11(a) (i)/(ii) "4 + 3") the part is one card. Q5 is
"Answer any eight of (a)-(j)" (best eight of ten at 7 each = 56) and prints (j) as "a. ... or b.
...": both alternatives are carded as routes of the one leaf. Q10 is "Answer either part (a) or
part (b)" (two 56s, both carded, 112), Q12 "Answer any two of (a), (b), (c), (d)" (four 28s, 112).

The census read (paper_census) needed one gated entry (paper.INLINE_SENTENCE_MARKERS, 2020 HL):
Q6(v), Q8(i)-(ii) and Q9(iv)-(v) are printed inside a sentence ("Calculate (v) how long ...",
"Define (i) radioactivity, (ii) the becquerel.") and had been lost (flags roman-gap); 101 -> 106
leaves, no flag left.

The scheme's mathematics is set in Cambria with an identity text layer: every maths glyph reaches
the text layer as its glyph id ("u = 0.57" reads as code points U+089B, U+0D4C, U+0AD9 ...).
GLYPHS sets each id the scheme uses by the character it draws, every id read on the rendered page
(a contact sheet of each glyph, cropped at its first use, 2026-10-28); the SymbolMT letters (λ, μ,
π, Ω) likewise, on the paper as well. Stacked fractions are read with G('fraction'), the nuclear
equations and the slashed "C = Q/V" with G('equation'), Q8(vii)'s nested "λ = ln2/(T½)" and
Q9(iv)'s rooted "f = 1/(2l) √(T/μ)" included.

The scheme prints a second marks column of PART totals at x 554 ("With emission of radiation 3 6"):
TOTAL_COLUMN_X keeps those numbers off the mark cells.
"""
from phys_review_lib import Q, SQ, S, M, G, pt, anyn, T

YEAR, LEVEL = 2020, 'hl'
REVIEWED_AT = '2026-10-28'
LETTERED = {5, 10, 11, 12}

SOURCES = {
    'paper': {'path': 'examiner-reports/physics/papers/2020-hl-paper.pdf', 'fileid': 'LC021ALP000EV.pdf',
              'sha256': '03fcec1103a5196021790d3f05bd9f4952fdc86509b370d2129ea260e1649add', 'pages': 12},
    'scheme': {'path': 'examiner-reports/physics/schemes/2020-hl.pdf', 'fileid': 'LC021ALP000EV.pdf',
               'sha256': '325af94020ee2310c8afb79615542822b49fcf70c0e0476509657595ae7aa588', 'pages': 24},
}

PAGE_ROLES = {
    'paper': {1: 'cover', **{p: 'questions' for p in range(2, 11)}, 11: 'questions-acknowledgements',
              12: 'back-cover'},
    'scheme': {1: 'cover', 2: 'note', 3: 'conventions', 4: 'annotations', **{p: 'marking' for p in range(5, 20)},
               **{p: 'blank' for p in range(20, 24)}, 24: 'back-cover'},
}

# The scheme's second marks column: each part's printed total at x 554 (the row cells sit at x 518).
TOTAL_COLUMN_X = 545

# Glyph ids of the scheme's Cambria (identity text layer: the code point read is the glyph id), each
# read on the rendered page from a crop of its first use (contact sheet, 2026-10-28).
_BOLD_UPRIGHT = {1788: 'N', 1803: 'c', 1807: 'g', 1809: 'i', 1811: 'k', 1812: 'l', 1813: 'm', 1814: 'n',
                 1815: 'o', 1818: 'r', 1819: 's'}     # units and words: "m s", "kg", "cm", "or", "sin", "ln", "N"
_ITALIC = {1861: 'i', 1870: 'r'}                      # p6 table "sin i", "sin r"
_BOLD_ITALIC = {2157: 'A', 2159: 'C', 2161: 'E', 2162: 'F', 2163: 'G', 2164: 'H', 2165: 'I', 2169: 'M',
                2170: 'N', 2172: 'P', 2173: 'Q', 2174: 'R', 2176: 'T', 2177: 'U', 2178: 'V',
                2183: 'a', 2184: 'b', 2185: 'c', 2186: 'd', 2187: 'e', 2188: 'f', 2190: 'h', 2191: 'i',
                2193: 'k', 2194: 'l', 2195: 'm', 2196: 'n', 2197: 'o', 2198: 'p', 2200: 'r', 2201: 's',
                2202: 't', 2203: 'u', 2204: 'v', 2206: 'x', 2207: 'y'}
_GREEK = {2237: 'γ', 2242: 'θ', 2246: 'μ', 2250: 'π', 2251: 'ρ', 2261: 'ϵ', 2743: 'Ω'}
_DIGITS = {2777 + k: str(k) for k in range(10)}       # bold digits 0-9 ("0.57", "85", "19.8")
_OPS = {3406: '≈', 3415: '/', 3495: '√'}              # p6 "m = n ≈ 1.50"; p11 the slash of "C = Q/V"; p13 root
_SYMBOL = {58: 'Ω', 79: 'λ', 80: 'μ', 83: 'π'}        # SymbolMT: p8 "R (Ω)", p7 "v = fλ", p11 "4000 μF", p17 "2πR"
GLYPHS = {'scheme': {'Cambria': {**_BOLD_UPRIGHT, **_ITALIC, **_BOLD_ITALIC, **_GREEK, **_DIGITS, **_OPS},
                     'SymbolMT': _SYMBOL},
          'paper': {'SymbolMT': {58: 'Ω', 80: 'μ'}}}  # paper p3 "R (Ω)", p6 "4000 μF"
VERIFIED_LINES = []

QUESTION_TOTALS = {**{n: 40 for n in range(1, 5)}, **{n: 56 for n in range(5, 10)},
                   10: 112,   # either (a) or (b), 56 each: both carded
                   11: 56,
                   12: 112}   # any two of (a)-(d), 28 each: all four carded
PART_TOTALS = {(10, 'a'): 56, (10, 'b'): 56,
               (11, 'a'): 7, (11, 'b'): 7, (11, 'c'): 7, (11, 'd'): 7, (11, 'e'): 14, (11, 'f'): 14,
               **{(12, x): 28 for x in 'abcd'}}
BEST_OF = {5: (8, 7)}
GROUP_TOTALS = {
    (1, ('i', 'ii', 'iii')): 21, (1, ('iv', 'v')): 19,
    (2, ('i', 'ii')): 15, (2, ('iii', 'iv', 'v')): 25,
    (3, ('i', 'ii', 'iii')): 18, (3, ('iv', 'v', 'vi')): 22,
    (4, ('i', 'ii')): 12, (4, ('iii', 'iv', 'v')): 21, (4, ('vi',)): 7,
    (6, ('i', 'ii')): 20, (6, ('iii',)): 9, (6, ('iv', 'v', 'vi', 'vii', 'viii')): 27,
    (7, ('i', 'ii')): 12, (7, ('iii', 'iv', 'v')): 18, (7, ('vi', 'vii', 'viii', 'ix')): 26,
    (8, ('i', 'ii')): 9, (8, ('iii', 'iv', 'v')): 20, (8, ('vi', 'vii', 'viii', 'ix', 'x')): 27,
    (9, ('i', 'ii')): 15, (9, ('iii', 'iv', 'v')): 24, (9, ('vi', 'vii', 'viii')): 17,
}
# Q10(a)'s and (b)'s own group marks ((24), (12), (20); (30), (26)) and Q12's ((18) + (10), (14) + (14),
# (12) + (16)) sit under letters, which GROUP_TOTALS cannot key: checked by hand against the tasks
# (10a: 6+3+6+3+6, 12, 6+4+4+6; 10b: 9+12+9, 3+9+6+8; 12a: 12+6, 6+4; 12b: 6+6+6, 10; 12c: 6+8, 10+4;
# 12d: 6+6, 7+9), and the letters' totals by PART_TOTALS.
CHECKSUMS = {}

# Q5(j): "a. Write a nuclear equation to show the pair annihilation of a positron and an electron.
# or b. Draw the truth table for an OR gate." Two printed alternatives of the one 7-mark part.
ROUTES = {'Q5(j)': ['pair-annihilation', 'or-gate']}

SCAN_PAGES = {'paper': range(2, 12)}
SELECTION_SCAN = [
    ('paper', 2, 'the following', 'Q1 "The following data were recorded": a reference to the data.'),
    ('paper', 2, 'the following', 'Q2 "The following data were recorded": a reference to the table.'),
    ('paper', 3, 'the following', 'Q3 "The following data were recorded": a reference to the table.'),
    ('paper', 3, 'or', 'Q3(vi) "Hence or otherwise": a method, one answer.'),
    ('paper', 3, 'the following', 'Q4 "The following data were recorded": a reference to the table.'),
    ('paper', 4, 'the following', 'Q5 "Answer any eight of the following parts": a best-eight of (a)-(j) at 7 each '
                                  '(8 x 7); every part is carded (BEST_OF).'),
    ('paper', 4, 'or', 'Q5(j) "a. ... or b. ...": two printed alternatives, each carded (ROUTES).'),
    ('paper', 4, 'or', 'Q5(j)b "an OR gate": the gate\'s name, not a choice.'),
    ('paper', 8, 'either', 'Q10 "Answer either part (a) or part (b)": whole-part choice; both parts are carded.'),
    ('paper', 8, 'or', 'Q10, the same choice.'),
    ('paper', 8, 'or', 'Q10(a)(x) "a spontaneous or a non-spontaneous process": the ask\'s own alternatives, one answer.'),
    ('paper', 9, 'the following', 'Q11 "Read the following passage": a reference to the passage.'),
    ('paper', 10, 'any two', 'Q12 "Answer any two of the following parts": every part is carded.'),
    ('paper', 10, 'the following', 'Q12, the same rubric.'),
    ('paper', 10, 'or', 'Q12(a) lead-in "further from the Earth than anyone before or since": description.'),
]
ASK_SCAN_PAGES = {'paper': range(2, 12)}
ASK_EXEMPT = [
    (5, 'the ball was caught by another player.', 'Q6 lead-in to (v)-(viii) ("... When it was caught the ball was again '
                                                  'at a height of 1.6 m."): a description, not an ask; lifted into '
                                                  'those cards\' stem.'),
    (7, 'pickup consists of a stationary magnet', 'Q9 lead-in to (vi)-(viii) ("... When the string vibrates an emf is '
                                                  'induced."): a description, not an ask; lifted into those cards\' stem.'),
    (11, 'State Examinations Commission', 'Acknowledgements: an image credit, not an ask.'),
]

SEC = 'State Examinations Commission'
CRIT = 'The scheme prints no answer here, only what earns the marks.'
VALUES = 'The scheme prints the values it expects in the table shown in the figure.'
DSL = ('The scheme\'s "//" (page 3): the answers either side are mutually exclusive; a partial answer from one '
       'side may not be taken with one from the other.')
ORDERED = ('The scheme prints these items under one sum, {cell}, and names no order: a response earns the marks '
           'step by step.')
LINKED = ('{w} reads to the figure-pointer check as a printed figure; the ask is the student\'s own drawing, so the '
          'card links its exam page.')

def P(page, start, end=None, **kw):
    return Q(page, start, end, **kw)


def R(text, marks, end=None, **kw):
    """A row lifted whole from the task's scheme page."""
    return pt(S(text, end), marks, **kw)


def C(text, marks, end=None, note=CRIT, **kw):
    """A criterion the scheme prices without printing an answer."""
    return pt(S(text, end), marks, kind='criterion', note=note, **kw)


def FR(page, clip, expect, marks, **kw):
    """A stacked fraction read from where its numerator and denominator are printed."""
    return G('fraction', page=page, clip=clip, expect=expect, marks=marks, **kw)


def EQ(page, clip, expect, marks, **kw):
    """A nuclear equation (or slashed formula) read from where each glyph is printed."""
    return G('equation', page=page, clip=clip, expect=expect, marks=marks, **kw)


def pieces(sel, marks, sep):
    """One row per entry of a printed list, each its own slice, at the marks in order."""
    return [pt(dict(sel, piece=i + 1, psep=sep), m) for i, m in enumerate(marks)]


# ------------------------------------------------------------------ stems --
STEM1 = P(2, 'In an experiment to verify the principle of conservation of momentum', 'at constant velocity.')
USE1 = P(2, 'Use the data to')
STEM2 = P(2, 'In an experiment to determine the refractive index of glass', 'different values of i.')
TABLE2 = P(2, 'i (°)', '41')
STEM3 = P(3, 'In an experiment to determine the speed of sound in air a student determined the lengths l of',
          'different fundamental frequencies f.')
TABLE3 = P(3, 'f (Hz)', '17.0')
STEM4 = P(3, 'In an experiment to determine the resistivity of nichrome', 'The diameter of the wire was also measured.')
TABLE4 = [P(3, 'l (cm)', '0.28', nth=2), P(3, 'Diameter of wire = 2.05 mm')]
Q4I = P(3, 'Name the pieces of apparatus that were used to measure (a) the diameter, (b) the length',
        'and (c) the resistance of the wire.')
MASS5 = P(4, '(mass of Earth = 6.0 × 10²⁴ kg)', br=True)
STEM6 = P(5, 'Motion and the effects of forces can be explained using Newton’s three laws of motion.')
CRICKET6 = P(5, 'A cricket player moves her hands away from the motion of the ball as she', 'catches it.')
THROW6 = P(5, 'She then throws a ball upwards with an initial velocity of 28 m s⁻¹ at 45° to', 'again at a height of 1.6 m.')
G6 = P(5, '(acceleration due to gravity = 9.8 m s⁻²)')
CALC6 = dict(P(5, 'Calculate (v)'), piece=1, psep=' (v)')
STEM7 = P(6, 'All insulated metal bodies can store charge.')
CAP7 = P(6, 'A charged capacitor stores energy.')
HEAT7 = P(6, 'A 4000 μF capacitor is connected across 500 V.', 'container.')
SHC7 = P(6, '(specific heat capacity of water = 4180 J kg⁻¹ K⁻¹)')
LEYDEN7 = [P(6, 'A Leyden jar acts as a parallel‐plate capacitor.'),
           P(6, 'A student makes a Leyden jar in the laboratory.', 'the jar.')]
BECQ8 = P(7, 'Radioactivity was discovered in 1896 by Henri Becquerel.')
Q8DEF = P(7, 'Define (i) radioactivity, (ii) the becquerel.')
SERIES8 = P(7, 'In the uranium decay series, U–238 decays to Pb–206 in a series of alpha and beta decays.',
            'the final decay is a beta decay.')
HALF8 = P(7, 'The half‐life of U–238 is 4.5 × 10⁹ years.')
RADON8 = P(7, 'Radon gas forms part of the uranium decay series.')
STEM9 = [P(7, 'There are two types of guitars, acoustic guitars and electric guitars.'),
         P(7, 'In acoustic guitars resonance occurs between the vibrating strings and', 'other parts of the guitar.')]
STRING9 = P(7, 'A guitar string has length 2 m and mass 0.88 g. It is stretched across two fixed',
            'fundamental frequency of 330 Hz.')
Q9C = P(7, 'Calculate (iv) the tension in the string, (v) the speed of sound in the string.')
PICKUP9 = P(7, 'In an electric guitar a magnetic pickup detects the vibration in the string. The',
            'string vibrates an emf is induced.')
FERMI10 = P(8, 'Fermilab is an American particle physics laboratory', 'South Dakota.')
COLLIDE10 = P(8, 'In another experiment in Fermilab two protons, each with a kinetic energy of 29 GeV, collide and',
              'new particles is 16 GeV.')
REACTOR10 = P(8, 'Enrico Fermi proposed the existence of the neutrino. He also built the first self‐sustaining nuclear',
              'fission reactor.')
GALV10 = P(8, 'A moving‐coil galvanometer detects and measures small currents.')
Q10BII = P(8, 'Draw labelled diagrams to show how a moving‐coil galvanometer can be converted',
           'into (a) an ammeter, (b) an ohmmeter.')
LED10 = P(8, 'LEDs can also indicate the flow of current.')
APOLLO12 = P(10, 'Fifty years ago the Apollo 13 mission to the Moon captured', 'before or since.')
DATA12A = P(10, '(mass of Earth = 6.0 × 10²⁴ kg;', 'radius of the Moon’s orbit around Earth = 3.85 × 10⁸ m)')
ANT12 = P(10, 'On a particular day, solar radiation falls on the surface of Antarctica at a rate of 850 W m⁻².',
          'radiation is 15 THz.')
Q12BII = P(10, 'Calculate the infra‐red energy that falls on 0.25 m² of Antarctica in 3 minutes.')
GLACIER12 = P(10, 'As part of the greenhouse effect infra‐red radiation is reflected back to Earth.',
              'volume of ice in glaciers on Earth is 170,000 km³.')
DATA12B = P(10, '(density of glacier ice = 920 kg m⁻³;', 'specific heat capacity of glacier ice = 2900 J kg⁻¹ K⁻¹)')
DOPPLER12 = P(11, 'Speed cameras make use of the Doppler effect.')
SOURCE12 = P(11, 'A source of sound approaches a stationary observer.', 'its frequency at rest.')
SOUND12 = P(11, '(speed of sound in air = 340 m s⁻¹)')
AMP12 = P(11, 'In May of 2019 the definition of the ampere, the SI unit of current,', 'elementary charge.')
PREV12 = P(11, 'The previous definition of the ampere was based on the', 'force on each other.')

TASKS = [
    # ============================================================ Section A ==
    # ---------------------------------------------------------------- Q1 --
    T('1i', 'Q1(i)', 'A', P(2, 'Draw a labelled diagram of how the apparatus was arranged in this experiment.'),
      [R('Two trolleys/riders on track', 3), C('Means of attachment', 3), C('Timing device', 3)],
      'phys-1-2', 'momentum-apparatus',
      SQ(5, 'Draw a labelled diagram of how the apparatus was arranged in this experiment.'), 9, stem=[STEM1]),
    T('1ii', 'Q1(ii)', 'A', P(2, 'Describe how the time interval was measured.'),
      [pt(S('Number of gaps // light gate', piece=1, psep='//'), 3, route='side-a', note=DSL),
       pt(S('× 0.02 (s)'), 3, route='side-a'),
       pt(S('Number of gaps // light gate', piece=2, psep='//'), 3, route='side-b'),
       pt(S('// rider passing through', piece=2, psep='//'), 3, route='side-b')],
      'phys-1-2', 'measuring-the-time-interval', SQ(5, 'Describe how the time interval was measured.'), 6,
      stem=[STEM1],
      decision='The scheme prints two columns separated by "//": counting gaps × 0.02 s, or a light gate the rider '
               'passes through; each side is a route at 3 + 3.'),
    T('1iii', 'Q1(iii)', 'A', P(2, 'How were the effects of (a) friction and (b) gravity minimised?'),
      [pt(S('Air cushion'), 3, route='side-a', note=DSL,
          note_sel=S('[“dust/polish runway” – maximum of 3 marks]')),
       pt(S('Horizontal track // frictional force', piece=1, psep='//'), 3, route='side-a'),
       pt(S('// track sloped', piece=2, psep='//'), 3, route='side-b',
          note_sel=S('[“dust/polish runway” – maximum of 3 marks]')),
       pt(S('Horizontal track // frictional force', piece=2, psep='//'), 3, route='side-b')],
      'phys-1-2', 'minimising-friction-and-gravity',
      SQ(5, 'How were the effects of (a) friction and (b) gravity minimised?'), 6, stem=[STEM1],
      decision='The paper prints (a) and (b) inside one sentence, priced [3] and [3]; the scheme answers both on '
               'each side of a "//" (an air cushion and a horizontal track, or a sloped track and its frictional '
               'force balanced by gravity), so (a) and (b) cannot be carded apart: one card, each side a route.'),
    T('1iv', 'Q1(iv)', 'A', [USE1, P(2, 'calculate the initial and final velocities of body A,')],
      [FR(5, (95, 490, 140, 518), 'v= s/t', 3),
       FR(5, (95, 518, 215, 546), 'u= .114/0.2 or v= .061/0.2', 3),
       pt(S('u =0.57 m s⁻¹ ; v =0.305 m s⁻¹', piece=1, psep=';'), 2),
       pt(S('u =0.57 m s⁻¹ ; v =0.305 m s⁻¹', piece=2, psep=';'), 1)],
      'phys-1-2', 'velocities-before-and-after-collision',
      SQ(5, 'calculate the initial and final velocities of body A,'), 9, stem=[STEM1], fig='q1-data',
      cells='The [3] printed against "u = .114/0.2 or v = .061/0.2" shares its baseline with the fractions\' '
            'denominators (0.2), so the reader takes it for a table cell: the scheme prints 3, 3 and 2 + 1 against '
            'these rows (= 9).',
      decision='The paper prints "Use the data to" once above (iv) and (v): each ask is lifted with it. "2 + 1" '
               'against the line holding both velocities: u 2, v 1, in the order printed.'),
    T('1v', 'Q1(v)', 'A', [USE1, P(2, 'demonstrate how the experiment verifies the principle of conservation of momentum.')],
      [R('p=mv', 3), R('pb=(0.1256)(0.57) or pₐ=(0.1256+0.1111)(0.305)', 3),
       pt(S('pb= 0.072 (kg m s⁻¹) ; pₐ=0.072 (kg m s⁻¹)', piece=1, psep=';'), 1,
          note_sel=S('[units not necessary]')),
       pt(S('pb= 0.072 (kg m s⁻¹) ; pₐ=0.072 (kg m s⁻¹)', piece=2, psep=';'), 1),
       R('pb= pₐ', 2)],
      'phys-1-2', 'verifying-conservation-of-momentum',
      SQ(5, 'demonstrate how the experiment verifies the principle of conservation of momentum.'), 10,
      stem=[STEM1], fig='q1-data',
      decision='"1 + 1" against the line holding both momenta: one each, in the order printed. The scheme sets p '
               'with a lowered b (before) and a (after); the b has no subscript form and reads "pb".'),
    # ---------------------------------------------------------------- Q2 --
    T('2i', 'Q2(i)', 'A', [P(2, 'Explain how the refracted ray and the angle of refraction were determined.'),
                           P(2, '(A labelled diagram may help your answer.)', br=True)],
      [R('Using ray box / pins / laser the ray in the block is determined', 3),
       R('Normal is drawn at point of incidence', 3),
       R('Angle between the normal and the ray in the block is measured with a protractor', 3)],
      'phys-2-3', 'finding-the-angle-of-refraction',
      SQ(6, 'Explain how the refracted ray and the angle of refraction were determined.'), 9, stem=[STEM2]),
    T('2ii', 'Q2(ii)', 'A', P(2, 'Why would using a smaller angle of incidence have led to a less accurate measurement of the',
                             'angle of refraction?'),
      [R('Smaller angle', 3), R('Greater percentage error', 3, note_sel=S('[−1 if “percentage” not mentioned]'))],
      'phys-2-3', 'small-angle-less-accurate',
      SQ(6, 'Why would using a smaller angle of incidence have led to a less accurate measurement of the',
         'angle of refraction?'), 6, stem=[STEM2]),
    T('2iii', 'Q2(iii)', 'A', P(2, 'Use the data to draw a suitable graph to verify Snell’s law.'),
      [C('6 values of sini and sinr calculated', 3, note=VALUES), C('Labelled axes', 3), C('6 points plotted', 3),
       C('Straight line with good fit', 3)],
      'phys-2-3', 'snells-law-graph', SQ(6, 'Use the data to draw a suitable graph to verify Snell’s law.'), 12,
      stem=[STEM2, TABLE2], fig='q2iii-scheme-table',
      decision='The scheme prints "6 values of sin i and sin r calculated" (its maths font sets no space after sin) '
               'over a table of the values: one criterion row in its words, the table the solution figure. The '
               'data table is lifted into the stem.'),
    T('2iv', 'Q2(iv)', 'A', P(2, 'Explain how your graph verifies Snell’s law.'),
      [R('Straight line graph', 3), R('Through origin', 3)], 'phys-2-3', 'graph-verifies-snells-law',
      SQ(6, 'Explain how your graph verifies Snell’s law.'), 6, stem=[STEM2]),
    T('2v', 'Q2(v)', 'A', P(2, 'Use your graph to calculate the refractive index of the glass.'),
      [FR(6, (95, 600, 165, 630), 'm= (y₂−y₁)/(x₂−x₁)', 3),
       C('Correct substitution using two points from line on graph', 2), R('Appropriate answer with m=n≈1.50', 2)],
      'phys-2-3', 'refractive-index-from-graph',
      SQ(6, 'Use your graph to calculate the refractive index of the glass.'), 7, stem=[STEM2, TABLE2]),
    # ---------------------------------------------------------------- Q3 --
    T('3i', 'Q3(i)', 'A', P(3, 'Draw a labelled diagram of how the apparatus was arranged in this experiment.'),
      [R('Air column and tuning fork', 3), C('Means of adjusting the length of the air column', 3),
       C('Correct arrangement', 3)],
      'phys-2-5', 'speed-of-sound-apparatus',
      SQ(7, 'Draw a labelled diagram of how the apparatus was arranged in this experiment.'), 9, stem=[STEM3]),
    T('3ii', 'Q3(ii)', 'A', P(3, 'How did the student determine the length of the air column for a particular frequency?'),
      [R('Hold a vibrating tuning fork over the air column', 3),
       R('Change length of air column until loud sound is heard', 3)],
      'phys-2-5', 'finding-the-resonant-length',
      SQ(7, 'How did the student determine the length of the air column for a particular frequency?'), 6,
      stem=[STEM3]),
    T('3iii', 'Q3(iii)', 'A', P(3, 'How did the student ensure that the fundamental frequency, not an overtone,',
                               'was observed?'),
      [R('Start with a small length (and increase length until first loud sound is heard)', 3)],
      'phys-2-5', 'ensuring-the-fundamental',
      SQ(7, 'How did the student ensure that the fundamental frequency, not an overtone, was observed?'), 3,
      stem=[STEM3]),
    T('3iv', 'Q3(iv)', 'A', P(3, 'Use the data to draw a graph of f against ¹/l .'),
      [C('6 values of ¹/ₗ calculated', 3, note=VALUES), C('Labelled axes', 3), C('6 points plotted', 3),
       C('Straight line with good fit', 3)],
      'phys-2-5', 'frequency-against-inverse-length-graph',
      SQ(7, 'Use the data to draw a graph of f against ¹/l.'), 12, stem=[STEM3, TABLE3], fig='q3iv-scheme-table',
      decision='The scheme prints "6 values of 1/l calculated" over a table of the values: one criterion row in its '
               'words, the table the solution figure. The data table is lifted into the stem.'),
    T('3v', 'Q3(v)', 'A', P(3, 'Calculate the slope of your graph.'),
      [FR(7, (95, 560, 165, 590), 'm= (y₂−y₁)/(x₂−x₁)', 2),
       C('Correct substitution using two points from line on graph', 2), R('Appropriate answer with m≈85', 2)],
      'phys-2-5', 'slope-of-frequency-graph', SQ(7, 'Calculate the slope of your graph.'), 6,
      stem=[STEM3, TABLE3]),
    T('3vi', 'Q3(vi)', 'A', P(3, 'Hence or otherwise calculate the speed of sound in air.'),
      [R('v= fλ', 2), R('v≈340 m s⁻¹', 2)], 'phys-2-5', 'speed-of-sound-from-slope',
      SQ(7, 'Hence or otherwise, calculate the speed of sound in air.'), 4, stem=[STEM3]),
    # ---------------------------------------------------------------- Q4 --
    T('4ia', 'Q4(i)(a)', 'A', dict(Q4I, piece=1, psep=', (b)'),
      [R('Micrometer / vernier calipers / digital calipers', 3)], 'phys-3-3', 'measuring-the-diameter',
      SQ(8, 'Name the pieces of apparatus that were used to measure (a) the diameter, (b) the length and (c)',
         'the resistance of the wire.'), 3, stem=[STEM4],
      decision='The paper prints (a), (b) and (c) inside one sentence; the scheme prices each on its own line [3]: '
               'one card each, the question the printed sentence cut at its own markers.'),
    T('4ib', 'Q4(i)(b)', 'A', [dict(Q4I, piece=1, psep=' (a) the diameter, '),
                               dict(Q4I, piece=[2, 1], psep=[' (a) the diameter, ', ' and (c)'])],
      [R('Metre stick', 3)], 'phys-3-3', 'measuring-the-length',
      SQ(8, 'Name the pieces of apparatus that were used to measure (a) the diameter, (b) the length and (c)',
         'the resistance of the wire.'), 3, stem=[STEM4],
      decision='The question is the printed sentence without (a)\'s and (c)\'s words.'),
    T('4ic', 'Q4(i)(c)', 'A', [dict(Q4I, piece=1, psep=' (a) the diameter, (b) the length and '),
                               dict(Q4I, piece=2, psep=' (a) the diameter, (b) the length and ')],
      [R('Ohmmeter / multimeter', 3)], 'phys-3-3', 'measuring-the-resistance',
      SQ(8, 'Name the pieces of apparatus that were used to measure (a) the diameter, (b) the length and (c)',
         'the resistance of the wire.'), 3, stem=[STEM4],
      decision='The question is the printed sentence without (a)\'s and (b)\'s words.'),
    T('4ii', 'Q4(ii)', 'A', P(3, 'How did the student ensure that the diameter of the wire was uniform?'),
      [R('Measured diameter at different places on the wire / no kinks', 3)], 'phys-3-3', 'uniform-diameter',
      SQ(8, 'How did the student ensure that the diameter of the wire was uniform?'), 3, stem=[STEM4]),
    T('4iii', 'Q4(iii)', 'A', P(3, 'Use the data to draw a graph of R against l.'),
      [C('Labelled axes', 3), C('6 points plotted', 3), C('Straight line with good fit', 3)],
      'phys-3-3', 'resistance-against-length-graph', SQ(8, 'Use the data to draw a graph of R against l.'), 9,
      stem=[STEM4] + TABLE4, decision='The data table is lifted into the stem.'),
    T('4iv', 'Q4(iv)', 'A', P(3, 'Calculate the slope of your graph.', nth=2),
      [FR(8, (95, 470, 165, 499), 'm= (y₂−y₁)/(x₂−x₁)', 2),
       C('Correct substitution using two points from line on graph', 2), R('Appropriate answer with m≈0.34', 2)],
      'phys-3-3', 'slope-of-resistance-graph', SQ(8, 'Calculate the slope of your graph.'), 6,
      stem=[STEM4] + TABLE4),
    T('4v', 'Q4(v)', 'A', P(3, 'Hence calculate the resistivity of the metal.'),
      [FR(8, (95, 565, 140, 592), 'ρ= RA/l', 3), R('ρ≈1.12 ×10⁻⁶ Ω m', 3)], 'phys-3-3', 'resistivity-of-nichrome',
      SQ(8, 'Hence calculate the resistivity of the metal.'), 6, stem=[STEM4, TABLE4[1]]),
    T('4vi', 'Q4(vi)', 'A', P(3, 'How would the resistance of a fixed length of wire change if its diameter was doubled?'),
      [FR(8, (95, 637, 152, 664), 'R∝ 1/d²', 2, route='side-a', note=DSL),
       FR(8, (166, 637, 275, 664), 'ρ= RA/l and A=πr²', 2, route='side-b'),
       R('4 times', 2), R('Smaller', 3)],
      'phys-3-3', 'doubling-the-diameter',
      SQ(8, 'How would the resistance of a fixed length of wire change if its diameter was doubled?'), 7,
      decision='The first line prints two reasons separated by "//": each side is a route at 2; "4 times" and '
               '"Smaller" are common to both.'),
    # ============================================================ Section B ==
    # ---------------------------------------------------------------- Q5 --
    T('5a', 'Q5(a)', 'B', P(4, 'State Boyle’s law.'),
      [anyn(None, 3, 3, steps=[3, 2, 2], note=ORDERED.format(cell='"3 + 2 + 2"'),
            options=[S('For a fixed mass of gas'), S('At constant temperature'),
                     S('Pressure is inversely proportional to volume')])],
      'phys-2-1', 'boyles-law', SQ(9, 'State Boyle’s law.'), 7,
      decision='"3 + 2 + 2" against the three conditions of the law, which the scheme prints in no order: a menu '
               'priced step by step.'),
    T('5b', 'Q5(b)', 'B', [P(4, 'A neutron star has a density of 3.7 × 10¹⁷ kg m⁻³. What would the radius of the',
                             'Earth be if it had the same density as the neutron star?'), MASS5],
      [FR(9, (80, 147, 220, 172), 'ρ= m/V / V=1.62×10⁷', 3), FR(9, (80, 170, 145, 195), 'V= 4/3 πr³', 2),
       R('r=157 m', 2)],
      'phys-1-2', 'radius-of-earth-as-neutron-star',
      SQ(9, 'A neutron star has a density of 3.7 × 10¹⁷ kg m⁻³. What would the radius of the Earth be if it had',
         'the same density as the neutron star?'), 7,
      decision='"3 + 2 + 2" against the three lines of the calculation: in the order printed.'),
    T('5c', 'Q5(c)', 'B', P(4, 'A spring has a length of 22 cm when a 2 N weight hangs from it. The spring',
                            'Calculate the natural length of the spring.'),
      [R('F=−ks', 3), R('s=4 cm', 2), R('Natural length =18 cm', 2)], 'phys-1-3', 'natural-length-of-spring',
      SQ(9, 'A spring has a length of 22 cm when a 2 N weight hangs from it. The spring constant is 50 N m⁻¹.',
         'Calculate the natural length of the spring.'), 7,
      decision='"3 + 2 + 2" against the three lines of the calculation: in the order printed.'),
    T('5d', 'Q5(d)', 'B', P(4, 'Draw a ray diagram to show the formation of an image in a convex mirror.'),
      [anyn(None, 3, 3, steps=[3, 2, 2], note=ORDERED.format(cell='"3 + 2 + 2"') + ' ' + CRIT,
            options=[S('Object and correct mirror'), S('Two correct rays'),
                     S('Appropriate lines behind mirror and correct image')])],
      'phys-2-3', 'convex-mirror-ray-diagram',
      SQ(9, 'Draw a ray diagram to show the formation of an image in a convex mirror.'), 7,
      decision='"3 + 2 + 2" against the three features of the drawing, which the scheme prints in no order: a menu '
               'priced step by step.'),
    T('5e', 'Q5(e)', 'B', P(4, 'What is meant by the amplitude of a wave?'),
      [R('Maximum', 4), R('Displacement (from rest position)', 3)], 'phys-2-2', 'amplitude-of-a-wave',
      SQ(9, 'What is meant by the amplitude of a wave?'), 7,
      decision='"4 + 3" against the two lines of one definition: in the order printed.'),
    T('5f', 'Q5(f)', 'B', P(4, 'Name one of the three primary colours of light. What is its complementary colour?'),
      [pt(S('Red'), 4, route='side-a', note=DSL), pt(S('Cyan'), 3, route='side-a'),
       pt(S('// green', piece=2, psep='//'), 4, route='side-b'), pt(S('// magenta', piece=2, psep='//'), 3, route='side-b'),
       pt(S('// blue', piece=2, psep='//'), 4, route='side-c'), pt(S('// yellow', piece=2, psep='//'), 3, route='side-c')],
      'phys-2-4', 'primary-and-complementary-colour',
      SQ(9, 'Name one of the three primary colours of light. What is its complementary colour?'), 7,
      decision='The scheme prints the three primary colours on one line [4] and their complements under them on the '
               'next [3], each line\'s entries separated by "//": a colour and the complement printed under it are '
               'one answer, so each column is a route, 4 + 3.'),
    T('5g', 'Q5(g)', 'B', P(4, 'Draw a labelled diagram to show how an electric field pattern can be demonstrated in the',
                            'laboratory.'),
      [R('Source of high voltage', 4, note_sel=S('[−1 if “high” not mentioned]')),
       R('Connected across plates, with oil, semolina', 3)],
      'phys-3-2', 'demonstrating-an-electric-field-pattern',
      SQ(9, 'Draw a labelled diagram to show how an electric field pattern can be demonstrated in the',
         'laboratory.'), 7, decision='"4 + 3" against the two lines: in the order printed.'),
    T('5h', 'Q5(h)', 'B', P(4, 'Distinguish between intrinsic and extrinsic conduction in a', 'semiconductor.'),
      [R('Intrinsic is through a pure semiconductor / intrinsic: equal number of holes and electrons', 4),
       pt(S('Extrinsic is through a doped semiconductor', piece=1, psep=' 4 + 3'), 3)],
      'phys-3-3', 'intrinsic-and-extrinsic-conduction',
      SQ(9, 'Distinguish between intrinsic and extrinsic conduction in a semiconductor'), 7,
      decision='"4 + 3" against the two lines, in the order printed. The cell is set inside the second line\'s own '
               'text object, so the reader keeps it in the line: the row is that line cut at the cell.'),
    T('5i', 'Q5(i)', 'B', P(4, 'The diagram shows a sketch of a photocell.', 'In what direction do the particles move?'),
      [pt(S('Electrons'), 4, label=S('a.', 'a.')), pt(S('From cathode to anode'), 3, label=S('b.', 'b.'))],
      'phys-4-2', 'photocell-particles-and-direction', SQ(9, 'The diagram shows a sketch of a photocell.'), 7,
      fig='q5i-photocell',
      decision='One cell "4 + 3" prices a. and b. together: one card, a. 4 and b. 3 in the order printed.'),
    T('5j', 'Q5(j)', 'B', P(4, 'Write a nuclear equation to show the pair annihilation of a', 'positron and an electron.'),
      [EQ(9, (95, 645, 330, 670), '⁰₋₁e + ⁰₁e / e⁻ + e⁺', 4), R('→2hf / →2γ', 3)],
      'phys-4-5', 'pair-annihilation-equation',
      SQ(9, 'Write a nuclear equation to show the pair annihilation of a positron and an electron.'), 7,
      route='pair-annihilation',
      decision='Q5(j) prints a. and b. joined by "or": each is carded at the part\'s 7, as routes of the one leaf. '
               'The particles are priced "2 + 2" on one line (one row at 4, read from where each number is '
               'printed), the products "2 + 1" on the next (one row at 3).'),
    T('5j2', 'Q5(j)', 'B', P(4, 'Draw the truth table for an OR gate.'),
      [anyn(None, 4, 2, steps=[2, 2, 2, 1], note=ORDERED.format(cell='"2 + 2 + 2 + 1"'),
            options=[S('1 + 1 → 1; 1 + 0 → 1; 0 + 1 → 1; 0 + 0 → 0', piece=k, psep=';') for k in (1, 2, 3, 4)])],
      'phys-3-3', 'or-gate-truth-table', SQ(9, 'Draw the truth table for an OR gate.'), 7, route='or-gate',
      decision='The second alternative of Q5(j). The scheme prints the table as four input-output rows on one line, '
               'priced "2 + 2 + 2 + 1" (set on a line of its own, read as no cell): the rows are interchangeable '
               'items, a menu priced step by step.'),
    # ---------------------------------------------------------------- Q6 --
    T('6i', 'Q6(i)', 'B', P(5, 'State Newton’s laws of motion.'),
      [R('A body remains at a constant velocity / a body remains at rest', 2), R('Unless acted on by a force', 2),
       R('Force is proportional to', 2), R('The rate of change of momentum', 2),
       R('When body A applies a force to body B', 2), R('Body B applies an equal and opposite force to body A', 2)],
      'phys-1-2', 'newtons-laws', SQ(10, 'State Newton’s laws of motion.'), 12, stem=[STEM6]),
    T('6ii', 'Q6(ii)', 'B', P(5, 'Show that F = ma is a special case of Newton’s second law.'),
      [FR(10, (80, 196, 285, 222), 'F=k ∆(mv)/(∆t) / F is proportional to ∆(mv)/(∆t)', 2),
       FR(10, (80, 219, 145, 244), 'F=k m∆v/(∆t)', 2), R('F=kma', 2),
       R('(From definition of the newton) k = 1 so F = ma', 2)],
      'phys-1-2', 'f-equals-ma', SQ(10, 'Show that F = ma is a special case of Newton’s second law.'), 8,
      stem=[STEM6]),
    T('6iii', 'Q6(iii)', 'B', P(5, 'Describe an experiment to find the resultant of two co‐planar vectors.'),
      [C('Apparatus', 3), C('Method', 3), C('Observation', 3)], 'phys-1-2', 'resultant-of-two-vectors-experiment',
      SQ(10, 'Describe an experiment to find the resultant of two co‐planar vectors.'), 9,
      decision='A "describe an experiment" part the scheme prices "Apparatus 3, Method 3, Observation 3" without '
               'an answer: three criterion rows.'),
    T('6iv', 'Q6(iv)', 'B', P(5, 'Use Newton’s laws of motion to explain why she moves her hands',
                              'away from the motion of the ball.'),
      [FR(10, (80, 382, 450, 404), 'F∝ 1/(∆t) / longer time therefore smaller force', 3)],
      'phys-1-2', 'catching-a-ball',
      SQ(10, 'Explain, using Newton’s laws of motion, why she moves her hands away from the motion of the',
         'ball.'), 3, stem=[CRICKET6]),
    T('6v', 'Q6(v)', 'B', P(5, 'Calculate (v)', 'how long the ball was in the air,'),
      [FR(10, (95, 483, 250, 510), 'v=u+at / s=ut+ ½ at²', 3), R('4.04 s', 3)],
      'phys-1-1', 'time-of-flight', SQ(10, 'how long the ball was in the air,'), 6, stem=[THROW6, G6],
      decision='The paper prints "Calculate" once before (v), (vi) and (vii): each ask is lifted with it.'),
    T('6vi', 'Q6(vi)', 'B', [CALC6, P(5, '(vi)', 'the horizontal distance travelled by the ball,')],
      [pt(S('s=vt // v=28cos45 (=19.8)', piece=1, psep='//'), 3, route='side-a', note=DSL),
       pt(S('s=vt // v=28cos45 (=19.8)', piece=2, psep='//'), 3, route='side-b'), R('s=80 m', 3)],
      'phys-1-1', 'horizontal-range', SQ(10, 'the horizontal distance travelled by the ball,'), 6,
      stem=[THROW6, G6],
      decision='The first line prints the formula and the horizontal velocity separated by "//": each side is a route '
               'at 3; the answer is common.'),
    T('6vii', 'Q6(vii)', 'B', [CALC6, P(5, '(vii) the maximum height above the ground reached by the', 'ball.')],
      [FR(10, (95, 584, 270, 610), 's=ut+ ½ at² / v²=u²+2as', 3),
       R('s=20+1.6=21.6 m', 3, note_sel=S('[–1 if addition of 1.6 m is omitted]'))],
      'phys-1-1', 'maximum-height', SQ(10, 'the maximum height above the ground reached by the ball.'), 6,
      stem=[THROW6, G6]),
    T('6viii', 'Q6(viii)', 'B', P(5, 'Draw a diagram to show the velocity v and acceleration a of the ball when it is at its',
                                 'your vectors.'),
      pieces(S('v horizontal; a vertically down; F vertically down'), [2, 2, 2], ';'),
      'phys-1-2', 'vectors-at-maximum-height',
      SQ(10, 'Draw a diagram to show the velocity v, acceleration a and force(s) F on the ball when it is at its',
         'maximum height. Use the letters v, a and F to label your vectors.'), 6, stem=[THROW6],
      decision='"3 × 2" against the three vectors printed on one line: one row each at 2.'),
    # ---------------------------------------------------------------- Q7 --
    T('7i', 'Q7(i)', 'B', P(6, 'Describe how a pear‐shaped metal body can be charged by induction.'),
      [R('Bring charged body close to pear shaped conductor', 3), R('Connect the conductor to Earth', 3),
       R('Remove the connection to Earth, then the charged body', 3)],
      'phys-3-1', 'charging-by-induction',
      SQ(11, 'Describe how a pear shaped metal body can be charged by induction.'), 9, stem=[STEM7], fig='q7-pear'),
    T('7ii', 'Q7(ii)', 'B', P(6, 'Draw a diagram to show the distribution of charge on the body after', 'charging.'),
      [R('Charge throughout with concentration at the pointed end', 3)], 'phys-3-1', 'charge-distribution',
      SQ(11, 'Draw a diagram to show the distribution of charge on the body after charging.'), 3,
      stem=[STEM7, M('(i)', 6), P(6, 'Describe how a pear‐shaped metal body can be charged by induction.')],
      fig='q7-pear'),
    T('7iii', 'Q7(iii)', 'B', P(6, 'Define capacitance.'),
      [EQ(11, (80, 196, 135, 224), 'C=Q/V', 3), C('Notation explained', 3)], 'phys-3-2', 'capacitance-definition',
      SQ(11, 'Define capacitance.'), 6, stem=[CAP7],
      decision='The scheme sets C = Q/V with a raised Q, a slash and a lowered V (no fraction bar): read from where '
               'each glyph is printed, left to right (G(\'equation\')).'),
    T('7iv', 'Q7(iv)', 'B', P(6, 'Draw the circuit symbol for a capacitor.'),
      [C('Symbol', 3)], 'phys-3-2', 'capacitor-symbol', SQ(11, 'Draw the circuit symbol for a capacitor.'), 3,
      stem=[CAP7], source_pages=[6], decision=LINKED.format(w='"the circuit symbol"')),
    T('7v', 'Q7(v)', 'B', P(6, 'Calculate the maximum rise in temperature of the water.'),
      [FR(11, (80, 313, 212, 335), 'E= ½ CV² or E=mc∆θ', 3), FR(11, (80, 331, 165, 352), 'mc∆θ= ½ CV²', 3),
       R('3 °C', 3)],
      'phys-3-2', 'temperature-rise-from-capacitor',
      SQ(11, 'Calculate the maximum rise in temperature of the water.'), 9, stem=[HEAT7, SHC7]),
    T('7vi', 'Q7(vi)', 'B', P(6, 'Describe an experiment to demonstrate how the capacitance of a parallel‐plate capacitor',
                              'changes with the distance between the plates.'),
      [C('Apparatus', 3), C('Method', 3), C('Observation', 3)], 'phys-3-2', 'capacitance-and-plate-separation',
      SQ(11, 'Describe an experiment to demonstrate how the capacitance of a parallel‐plate capacitor',
         'changes with the distance between its plates.'), 9,
      decision='A "describe an experiment" part the scheme prices "Apparatus 3, Method 3, Observation 3" without '
               'an answer: three criterion rows.'),
    T('7vii', 'Q7(vii)', 'B', P(6, 'Calculate the surface area of the inner cylinder of aluminium foil.'),
      [R('A=2πrh', 3), R('A=0.064 m²', 3)], 'phys-3-2', 'area-of-foil',
      SQ(11, 'Calculate the surface area of the inner cylinder of aluminium foil.'), 6, stem=LEYDEN7),
    T('7viii', 'Q7(viii)', 'B', P(6, 'Calculate the capacitance of the Leyden jar.'),
      [FR(11, (80, 569, 125, 596), 'C= ϵA/d', 3), R('C=0.238 nF', 3)], 'phys-3-2', 'capacitance-of-leyden-jar',
      SQ(11, 'Calculate the capacitance of the Leyden jar.'), 6, stem=LEYDEN7),
    T('7ix', 'Q7(ix)', 'B', P(6, 'What property of glass allows it to be used as a dielectric?'),
      [R('Insulator', 5)], 'phys-3-2', 'glass-as-dielectric',
      SQ(11, 'What property of glass allows it to be used as a dielectric?'), 5, stem=LEYDEN7),
    # ---------------------------------------------------------------- Q8 --
    T('8i', 'Q8(i)', 'B', dict(Q8DEF, piece=1, psep=', (ii)'),
      [R('(Spontaneous) disintegration of a nucleus', 3, note_sel=S('[−1 for “atom” instead of nucleus]')),
       R('With emission of radiation', 3)],
      'phys-4-4', 'radioactivity-definition', SQ(12, 'Define (i) radioactivity, (ii) the becquerel.'), 6,
      stem=[BECQ8],
      decision='The paper prints (i) and (ii) inside one sentence, priced apart (3 + 3, and 3): the question is the '
               'printed sentence cut at its own markers.'),
    T('8ii', 'Q8(ii)', 'B', [dict(Q8DEF, piece=1, psep=' (i) radioactivity, '),
                             dict(Q8DEF, piece=2, psep=' (i) radioactivity, ')],
      [R('One disintegration per second', 3)], 'phys-4-4', 'the-becquerel',
      SQ(12, 'Define (i) radioactivity, (ii) the becquerel.'), 3, stem=[BECQ8],
      decision='The question is the printed sentence without (i)\'s words.'),
    T('8iii', 'Q8(iii)', 'B', P(7, 'Write a nuclear equation for the first decay in this series.'),
      [EQ(12, (80, 196, 200, 218), '²³⁸₉₂U → ⁴₂He + ²³⁴₉₀Th', 7, note='The scheme prices the equation "7 × 1".')],
      'phys-4-4', 'first-decay-equation', SQ(12, 'Write a nuclear equation for the first decay in this series.'), 7,
      stem=[SERIES8],
      decision='The scheme sets the equation in its identity-mapped maths font (GLYPHS sets each glyph by its id): '
               'read from where each nuclide\'s numbers are printed, one row at the printed "7 × 1".'),
    T('8iv', 'Q8(iv)', 'B', P(7, 'Write a nuclear equation for the final decay in this series.'),
      [EQ(12, (80, 228, 200, 250), '²⁰⁶₈₁Tl → ⁰₋₁e + ²⁰⁶₈₂Pb', 7, note='The scheme prices the equation "7 × 1".')],
      'phys-4-4', 'final-decay-equation', SQ(12, 'Write a nuclear equation for the final decay in this series.'), 7,
      stem=[SERIES8],
      decision='Read from where each nuclide\'s numbers are printed (GLYPHS): one row at the printed "7 × 1".'),
    T('8v', 'Q8(v)', 'B', P(7, 'Calculate the total number of alpha particles and the total number of beta particles emitted',
                            'in the series.'),
      [R('8 alpha', 3), R('6 beta', 3)], 'phys-4-4', 'alpha-and-beta-count',
      SQ(12, 'Calculate the total number of alpha particles and the total number of beta particles emitted in',
         'the series.'), 6, stem=[SERIES8]),
    T('8vi', 'Q8(vi)', 'B', P(7, 'How long will it take for the number of U–238 nuclei in a sample to decrease by',
                              'a factor of 8?'),
      [R('3 half lives', 3), R('1.35 × 10¹⁰ years', 3)], 'phys-4-4', 'three-half-lives',
      SQ(12, 'How long will it take for the number of U–238 nuclei in a sample to decrease by a factor of 8?'), 6,
      stem=[HALF8]),
    T('8vii', 'Q8(vii)', 'B', P(7, 'A sample of U–238 contains 3.2 × 10¹⁰ nuclei. Calculate its activity.'),
      [FR(12, (80, 389, 135, 423), 'λ= ln2/(T½)', 3), R('A=λN', 3), R('A=1.56× 10⁻⁷ Bq', 3)],
      'phys-4-4', 'activity-of-uranium-sample',
      SQ(12, 'A sample of U–238 nuclei contains 3.2 × 10¹⁰ nuclei. Calculate its activity.'), 9, stem=[HALF8],
      decision='"3, 3, 3" against the three lines. The first is the decay constant\'s formula, a stacked fraction '
               'whose denominator holds a second one (T with a lowered one half): G(\'fraction\') reads the inner '
               'bar first and sets it in the outer denominator.'),
    T('8viii', 'Q8(viii)', 'B', P(7, 'U–238 is an isotope of uranium. What are isotopes?'),
      [R('Same number of protons / same atomic number / same element', 3),
       R('Different number of neutrons / different mass number', 3)], 'phys-4-4', 'isotopes',
      SQ(12, 'U–238 is an isotope of uranium. What are isotopes?'), 6),
    T('8ix', 'Q8(ix)', 'B', P(7, 'Why is radon considered to be dangerous?'),
      [R('e.g.radioactive', 3)], 'phys-4-4', 'radon-danger',
      SQ(12, 'Why is radon gas considered to be dangerous?'), 3, stem=[RADON8]),
    T('8x', 'Q8(x)', 'B', P(7, 'How can the build‐up of radon in a building be reduced?'),
      [R('Sump / membrane / ventilation', 3)], 'phys-4-4', 'reducing-radon',
      SQ(12, 'How can the build‐up of radon gas in a building be reduced?'), 3, stem=[RADON8]),
    # ---------------------------------------------------------------- Q9 --
    T('9i', 'Q9(i)', 'B', P(7, 'Define resonance.'),
      [R('Transfer of energy', 3), R('Between two bodies of the same natural frequency', 3)], 'phys-2-6',
      'resonance-definition', SQ(13, 'Define resonance.'), 6, stem=STEM9),
    T('9ii', 'Q9(ii)', 'B', P(7, 'Describe a laboratory experiment to demonstrate resonance.', 'resonance.'),
      [C('Apparatus', 3), C('Method', 3), C('Observation', 3)], 'phys-2-6', 'demonstrating-resonance',
      SQ(13, 'Describe a laboratory experiment to demonstrate resonance.'), 9, stem=STEM9,
      decision='A "describe an experiment" part the scheme prices "Apparatus 3, Method 3, Observation 3" without '
               'an answer: three criterion rows.'),
    T('9iii', 'Q9(iii)', 'B', P(7, 'Draw a labelled diagram to show a guitar string vibrating at its fundamental',
                               'frequency.'),
      [R('Nodes at each end', 3), R('One antinode in the middle', 3)], 'phys-2-6', 'string-at-fundamental',
      SQ(13, 'Draw a labelled diagram to show a guitar string vibrating at its fundamental frequency.'), 6,
      stem=[STRING9]),
    T('9iv', 'Q9(iv)', 'B', dict(Q9C, piece=1, psep=', (v)'),
      [FR(13, (95, 307, 215, 336), 'μ= m/l / μ= (0.88×10⁻³)/2', 3),
       FR(13, (95, 335, 155, 362), 'f= 1/(2l) √(T/μ)', 3),
       C('Substitution', 3), R('T=81 N', 3)],
      'phys-2-6', 'tension-in-guitar-string', SQ(13, 'the tension in the string,'), 12, stem=[STRING9],
      decision='The paper prints (iv) and (v) inside one sentence, priced apart (12 and 6): the question is the '
               'printed sentence cut at its own markers. The second line is the string\'s frequency formula, read '
               'with G(\'fraction\'): the root\'s overbar is the highest bar where the root sign ends, and what it '
               'covers (the stacked T over μ) is the radicand.'),
    T('9v', 'Q9(v)', 'B', [dict(Q9C, piece=1, psep=' (iv) the tension in the string, '),
                           dict(Q9C, piece=2, psep=' (iv) the tension in the string, ')],
      [R('v=fλ', 3), R('v=429 m s⁻¹', 3)], 'phys-2-6', 'wave-speed-in-string',
      SQ(13, 'the speed of sound in the string.'), 6, stem=[STRING9],
      decision='The question is the printed sentence without (iv)\'s words.'),
    T('9vi', 'Q9(vi)', 'B', P(7, 'Draw the magnetic field around a bar magnet.'),
      [C('Correct shape', 3), C('Correct direction', 3)], 'phys-3-4', 'field-of-bar-magnet',
      SQ(13, 'Draw the magnetic field around a bar magnet.'), 6, stem=[PICKUP9]),
    T('9vii', 'Q9(vii)', 'B', P(7, 'Explain how an emf is induced in the coil.'),
      [R('Moving coil', 3), R('Changing magnetic field cutting the coil', 3)], 'phys-3-6', 'emf-in-pickup',
      SQ(13, 'Explain how the emf is induced in the coil.'), 6, stem=[PICKUP9]),
    T('9viii', 'Q9(viii)', 'B', P(7, 'Sketch a graph to show how the output current varies with time.'),
      [C('Labelled axes', 3), R('a.c.', 2)], 'phys-3-6', 'pickup-output-current',
      SQ(13, 'Sketch a graph to show how the output current varies with time.'), 5, stem=[PICKUP9],
      decision='"3 + 2" against the two lines: labelled axes 3, a.c. 2, in the order printed.'),
    # ---------------------------------------------------------------- Q10 --
    T('10ai', 'Q10(a)(i)', 'B', P(8, 'What are the two fundamental forces that the neutrino experiences?'),
      pieces(S('Weak, gravitational'), [3, 3], ','), 'phys-4-5', 'forces-on-a-neutrino',
      SQ(14, 'What are the two fundamental forces that the neutrino experiences?'), 6, stem=[FERMI10],
      decision='"3 + 3" against the two forces printed on one line: one row each.'),
    T('10aii', 'Q10(a)(ii)', 'B', P(8, 'Pions and kaons are members of the meson family. What are mesons?'),
      [R('Quark and anti‐quark pair', 3)], 'phys-4-5', 'mesons',
      SQ(14, 'Pions and kaons are members of the meson family. What are mesons?'), 3, stem=[FERMI10]),
    T('10aiii', 'Q10(a)(iii)', 'B', P(8, 'List the three types of neutrino in order of increasing mass.'),
      [pt(S('Electron neutrino, muon neutrino, tau neutrino', piece=1, psep=','), 2,
          note_sel=S('[any order acceptable]')),
       pt(S('Electron neutrino, muon neutrino, tau neutrino', piece=2, psep=','), 2),
       pt(S('Electron neutrino, muon neutrino, tau neutrino', piece=3, psep=','), 2)],
      'phys-4-5', 'three-neutrinos', SQ(14, 'List the three types of neutrino in order of increasing mass.'), 6,
      stem=[FERMI10],
      decision='"3 × 2" against the three neutrinos: one row each at 2. The ask says "in order of increasing mass"; '
               'the scheme says "[any order acceptable]", kept as the first row\'s note.'),
    T('10aiv', 'Q10(a)(iv)', 'B', P(8, 'Why is no tunnel required to transport the neutrinos underground to South Dakota?'),
      [R('Small mass / no charge / little interaction with matter', 3)], 'phys-4-5', 'neutrinos-need-no-tunnel',
      SQ(14, 'Why is no tunnel required to transport the neutrinos underground to South Dakota?'), 3,
      stem=[FERMI10]),
    T('10av', 'Q10(a)(v)', 'B', P(8, 'Calculate the time taken for the neutrino to travel from Fermilab to South Dakota.'),
      [FR(14, (80, 216, 120, 243), 'v= s/t', 3), R('t=4.4 ms', 3)], 'phys-1-1', 'neutrino-travel-time',
      SQ(14, 'Calculate the time taken for the neutrino to travel from Fermilab to South Dakota.'), 6,
      stem=[FERMI10], fig='q10a-map',
      decision='The distance (1300 km) is printed only on the paper\'s drawing: the drawing is the figure.'),
    T('10avi', 'Q10(a)(vi)', 'B', P(8, 'Calculate the total mass of the new particles created.'),
      [R('Change in energy = 42 (GeV)', 3), R('6.72 × 10⁻⁹ (J)', 3), R('E=mc²', 3), R('m=7.48 ×10⁻²⁶ kg', 3)],
      'phys-4-5', 'mass-of-new-particles', SQ(14, 'Calculate the total mass of the new particles created.'), 12,
      stem=[COLLIDE10]),
    T('10avii', 'Q10(a)(vii)', 'B', P(8, 'What is nuclear fission?'),
      [R('Splitting of a large nucleus into smaller nuclei', 3,
         note_sel=S('[−1 for “atom” instead of nucleus]', '[−1 for omission of nuclear size]')),
       R('With the emission of energy and neutrons', 3, note_sel=S('[−1 for omission of neutrons]'))],
      'phys-4-6', 'nuclear-fission', SQ(14, 'What is nuclear fission?'), 6, stem=[REACTOR10]),
    T('10aviii', 'Q10(a)(viii)', 'B', P(8, 'Why was Fermi’s nuclear reactor self‐sustaining?'),
      [R('Chain reaction / on average every fission caused another fission', 4)], 'phys-4-6', 'self-sustaining-reactor',
      SQ(14, 'Why was Fermi’s nuclear reactor considered to be self‐sustaining?'), 4, stem=[REACTOR10]),
    T('10aix', 'Q10(a)(ix)', 'B', P(8, 'Graphite was used in his nuclear reactor. What was the purpose of the graphite?'),
      [R('To slow down fast neutrons / to increase the rate of fission / to act as a moderator', 4)],
      'phys-4-6', 'purpose-of-graphite',
      SQ(14, 'Graphite was used in his fission reactor. What was the purpose of the graphite?'), 4, stem=[REACTOR10]),
    T('10ax', 'Q10(a)(x)', 'B', P(8, 'Is nuclear fission a spontaneous or a non‐spontaneous process? Explain your answer.'),
      [R('Non‐spontaneous', 3), R('A neutron is required to initiate', 3)], 'phys-4-6', 'fission-not-spontaneous',
      SQ(14, 'Is nuclear fission a spontaneous or a non‐spontaneous process? Explain your answer.'), 6),
    T('10bi', 'Q10(b)(i)', 'B', P(8, 'Describe, with the aid of a labelled diagram, the principle of operation of the galvanometer.'),
      [R('Coil, core, magnets, spring, pointer and scale', 3), R('Current in coil', 3),
       R('Coil experiences a force and rotates', 3)],
      'phys-3-5', 'galvanometer-principle',
      SQ(15, 'Describe, with the aid of a labelled diagram, the principle of operation of a galvanometer.'), 9,
      stem=[GALV10]),
    T('10biia', 'Q10(b)(ii)(a)', 'B', dict(Q10BII, piece=1, psep=', (b)'),
      [R('Low resistance', 3), R('In parallel', 3)], 'phys-3-3', 'galvanometer-to-ammeter',
      SQ(15, 'Draw labelled diagrams to show how a moving‐coil galvanometer can be converted into (a) an',
         'ammeter, (b) an ohmmeter.'), 6, stem=[GALV10],
      decision='The paper prints (a) and (b) inside one sentence; the scheme prices each under its own marker '
               '(3 + 3 each): the question is the printed sentence cut at its own markers.'),
    T('10biib', 'Q10(b)(ii)(b)', 'B', [dict(Q10BII, piece=1, psep=' (a) an ammeter, '),
                                       dict(Q10BII, piece=2, psep=' (a) an ammeter, ')],
      [R('Variable resistor and power supply', 3), R('In series', 3)], 'phys-3-3', 'galvanometer-to-ohmmeter',
      SQ(15, 'Draw labelled diagrams to show how a moving‐coil galvanometer can be converted into (a) an',
         'ammeter, (b) an ohmmeter.'), 6, stem=[GALV10],
      decision='The question is the printed sentence without (a)\'s words.'),
    T('10biii', 'Q10(b)(iii)', 'B', P(8, 'A moving‐coil galvanometer has a full scale deflection of 50 mA and an internal resistance',
                                     'deflection of 10 V.'),
      [R('Rₜₒₜₐₗ=x+7.2', 3), FR(15, (95, 291, 135, 318), 'R= V/I', 3), R('Rmultiplier=193 Ω', 3)],
      'phys-3-3', 'multiplier-resistance',
      SQ(15, 'A moving‐coil galvanometer has a full scale deflection of 50 mA and an internal resistance of 7.2',
         '10 V.'), 9),
    T('10biv', 'Q10(b)(iv)', 'B', P(8, 'What is an LED?'),
      [R('Light emitting diode', 3)], 'phys-3-3', 'what-is-an-led', SQ(15, 'What is an LED?'), 3, stem=[LED10]),
    T('10bv', 'Q10(b)(v)', 'B', P(8, 'Describe, with the aid of a labelled diagram, the principle of operation of an LED.'),
      [R('Diagram with p‐n junction and depletion layer', 3),
       R('Forward bias connection, electrons and holes interact', 3), R('Emitting photons', 3)],
      'phys-3-3', 'led-principle',
      SQ(15, 'Describe, with the aid of a labelled diagram, the principle of operation of an LED.'), 9, stem=[LED10]),
    T('10bvi', 'Q10(b)(vi)', 'B', P(8, 'LEDs are fragile. How can they be protected in a circuit?'),
      [R('Resistor', 3), R('In series', 3)], 'phys-3-3', 'protecting-an-led',
      SQ(15, 'LEDs are fragile. How can they be protected in a circuit?'), 6, stem=[LED10]),
    T('10bvii', 'Q10(b)(vii)', 'B', P(8, 'State two differences between LEDs and photodiodes.'),
      [R('LEDs emit light, photodiodes need to absorb light', 4),
       R('LEDs in forward bias, photodiodes in reverse bias', 4)], 'phys-3-3', 'leds-and-photodiodes',
      SQ(15, 'State two difference between LEDs and photodiodes.'), 8, stem=[LED10]),
    # ---------------------------------------------------------------- Q11 --
    T('11a', 'Q11(a)', 'B', [P(9, 'J.J. Thomson used cathode ray tubes in his research.'),
                             P(9, 'How are electrons (i) produced, (ii) deviated in a cathode ray tube?')],
      [R('(i) Heated cathode / thermionic emission', 4), R('(ii) Electric/magnetic fields', 3)],
      'phys-4-1', 'cathode-ray-electrons',
      SQ(16, 'J.J. Thomson used cathode ray tubes in his research. How are electrons (a) produced, (b)',
         'deviated in a cathode ray tube?'), 7,
      decision='One cell "4 + 3" prices (i) and (ii) together: one card, (i) 4 and (ii) 3 in the order printed. The '
               'scheme reprints the ask as "(a) produced, (b) deviated" where the paper prints (i) and (ii); its '
               'answers are marked (i) and (ii).'),
    T('11b', 'Q11(b)', 'B', P(9, 'Cathode rays are accelerated through a potential difference of 4 kV in a cathode ray',
                              'tube. Calculate the maximum speed of an electron in the tube.'),
      [FR(16, (95, 149, 215, 170), 'E= ½ mv² or E=QV', 3), FR(16, (95, 167, 170, 187), '½ mv²=QV', 2),
       R('v=3.75 ×10⁷ m s⁻¹', 2)],
      'phys-4-1', 'speed-of-cathode-ray-electron',
      SQ(16, 'Cathode rays are accelerated through a potential difference of 4 kV in a cathode ray tube.',
         'Calculate the maximum speed of an electron in the tube.'), 7),
    T('11c', 'Q11(c)', 'B', P(9, 'What pieces of apparatus can be used to demonstrate the diffraction of light in the',
                              'laboratory?'),
      [anyn(None, 3, 3, steps=[3, 2, 2], note=ORDERED.format(cell='"3 + 2 + 2"'),
            options=[S('Diffraction grating, light source, screen/spectrometer', piece=k, psep=',') for k in (1, 2, 3)])],
      'phys-2-6', 'diffraction-apparatus',
      SQ(16, 'What pieces of apparatus can be used to demonstrate the diffraction of light in the laboratory?'), 7,
      decision='"3 + 2 + 2" against three pieces of apparatus printed on one line: a menu priced step by step.'),
    T('11d', 'Q11(d)', 'B', P(9, 'Geiger also played an important role in the development of the Geiger counter,',
                              'nuclear radiation.', end_nth=2),
      [R('Ionisation', 4),
       R('Correct valid detail e.g. producing current', 3,
         note='The scheme names what earns the marks and gives one example ("e.g.").')],
      'phys-4-4', 'radiation-detector-principle',
      SQ(16, 'Geiger also played an important role in the development of the Geiger counter, a detector of',
         'any detector of radiation.'), 7),
    T('11e', 'Q11(e)', 'B', P(9, 'Describe the Geiger‐Marsden experiment that used thin sheets of gold. Include their',
                              'setup, observations and conclusions.'),
      [anyn(S('Zinc sulphide / fluorescent screen; alpha source; gold foil; vacuum'), 3, 1, sep=';',
            note='The scheme prints "any 3 × 1" against this line.'),
       R('Flashes on screen / scintillations', 3), R('Most alphas straight through / deviated slightly', 2),
       R('A few alphas reflected', 2), R('Atom mostly empty space', 2), R('Small/dense positive core', 2)],
      'phys-4-3', 'geiger-marsden-experiment',
      SQ(16, 'Describe the Geiger‐Marsden experiment that used thin sheets of gold. Include their setup,',
         'observations and conclusions.'), 14,
      decision='The setup is "any 3 × 1" of four items separated by ";": a menu of three claims at 1; the '
               'observations and conclusions each on their own line.'),
    T('11f', 'Q11(f)', 'B', P(9, 'Describe with the aid of a labelled diagram the Bohr model of the atom. Use the',
                              'model to explain emission line spectra.'),
      [R('Nucleus', 3), R('Electrons in different energy levels', 3), R('Electrons given energy', 2),
       R('Rise to higher energy level', 2), R('Fall to lower energy level', 2), R('Photon/light emitted', 2)],
      'phys-4-3', 'bohr-model-and-line-spectra',
      SQ(16, 'Describe with the aid of a labelled diagram the Bohr model of the atom. Use the model to',
         'explain emission line spectra.'), 14),
    # ---------------------------------------------------------------- Q12 --
    T('12ai', 'Q12(a)(i)', 'B', P(10, 'Derive an expression for the period of orbit T of the', '(of mass M).'),
      [FR(17, (108, 155, 175, 184), 'mv²/R = GmM/R²', 3), FR(17, (108, 179, 162, 205), 'v²= GM/R', 3),
       FR(17, (108, 200, 160, 227), 'T= 2πR/v', 3), FR(17, (108, 222, 172, 251), 'T²= 4π²R³/(GM)', 3)],
      'phys-1-5', 'period-of-orbit-derivation',
      SQ(17, 'Derive an expression for the period of orbit T of the Moon around the Earth (of mass M)',
         'with radius of orbit R.'), 12, stem=[APOLLO12]),
    T('12aii', 'Q12(a)(ii)', 'B', P(10, 'Calculate the period of the Moon as it orbits the Earth.'),
      [FR(17, (108, 262, 265, 290), 'T²= (4π²(3.85×10⁸)³)/((6.7×10⁻¹¹)(6.0×10²⁴))', 3), R('T=2.37×10⁶ s', 3)],
      'phys-1-5', 'period-of-the-moon', SQ(17, 'Calculate the period of the Moon as it orbits the Earth.'), 6,
      stem=[DATA12A]),
    T('12aiii', 'Q12(a)(iii)', 'B', P(10, 'Calculate the gravitational force exerted by the Moon on an astronaut of mass 80 kg',
                                     'when he is 250 km above the surface of the Moon.'),
      [FR(17, (108, 335, 165, 362), 'F= GMm/d²', 3), R('F=98.73 N', 3)], 'phys-1-5', 'force-on-astronaut',
      SQ(17, 'Calculate the gravitational force exerted by the Moon on an astronaut of mass 80 kg when',
         'he is 250 km above the surface of the Moon.'), 6, stem=[DATA12A]),
    T('12aiv', 'Q12(a)(iv)', 'B', P(10, 'Astronauts appear to be weightless when they orbit the Moon. Explain why.'),
      [R('Astronaut and spaceship have common acceleration / spaceship in freefall', 4)], 'phys-1-5',
      'apparent-weightlessness', SQ(17, 'Astronauts appear to be weightless when they orbit the moon. Explain why.'), 4),
    T('12bi', 'Q12(b)(i)', 'B', P(10, 'Radiation is one of three methods of heat transfer. What are the other two methods?'),
      pieces(S('Conduction, convection'), [3, 3], ','), 'phys-2-1', 'methods-of-heat-transfer',
      SQ(18, 'Radiation is one of three methods of heat transfer. What are the other two methods?'), 6,
      decision='"3 + 3" against the two methods printed on one line: one row each.'),
    T('12bii', 'Q12(b)(ii)', 'B', Q12BII,
      [R('850 × 0.52', 3), R('× 0.25 × 180 = 19890 J', 3)], 'phys-2-4', 'infra-red-energy',
      SQ(18, 'Calculate the infra‐red energy that falls on 0.25 m² of Antarctica in 3 minutes.'), 6, stem=[ANT12]),
    T('12biii', 'Q12(b)(iii)', 'B', P(10, 'Calculate the number of infra‐red photons that fall on this area in this time.'),
      [R('E=hf / E=9.9 ×10⁻²¹', 3), FR(18, (108, 244, 280, 270), 'Number = 19890/(9.9 ×10⁻²¹) =2 ×10²⁴', 3)],
      'phys-2-4', 'number-of-infra-red-photons',
      SQ(18, 'Calculate the number of infra‐red photons that fall on this area in this time.'), 6,
      stem=[ANT12, M('(ii)', 10), Q12BII]),
    T('12biv', 'Q12(b)(iv)', 'B', P(10, 'Calculate the energy required to melt 0.5% of the Earth’s glaciers if their average',
                                   'temperature is –6 °C and the melting point of glacier ice is –2 °C.'),
      [FR(18, (108, 327, 150, 354), 'ρ= m/V', 2), R('m=7.82 ×10¹⁴ (kg)', 2), pt(S('E=mc∆θ+ml'), 4, units=[2, 2]),
       R('E=2.67 ×10²⁰ J', 2)],
      'phys-2-1', 'energy-to-melt-glaciers',
      SQ(18, 'Calculate the energy required to melt 0.5% of the Earth’s glaciers if their average',
         'temperature is –6 °C and the melting point of glacier ice is –2 °C.'), 10, stem=[GLACIER12, DATA12B],
      decision='"2 + 2" against the one formula holding both energies (mcΔθ + ml): one row at 4.'),
    T('12ci', 'Q12(c)(i)', 'B', P(11, 'What is the Doppler effect?'),
      [R('Change of observed frequency', 3), R('Due to relative motion between the source and the observer', 3)],
      'phys-2-7', 'doppler-effect', SQ(19, 'What is the Doppler effect?'), 6, stem=[DOPPLER12]),
    T('12cii', 'Q12(c)(ii)', 'B', P(11, 'Explain, with the aid of labelled diagrams, how the Doppler', 'effect occurs.'),
      [R('Labelled non‐concentric circles', 2), R('Source moves towards observer', 2), R('Wavelength is shorter', 2),
       R('Frequency is higher', 2)],
      'phys-2-7', 'how-the-doppler-effect-occurs',
      SQ(19, 'Explain, with the aid of labelled diagrams, how the Doppler effect occurs.'), 8, stem=[DOPPLER12]),
    T('12ciii', 'Q12(c)(iii)', 'B', P(11, 'Calculate the speed of the source.'),
      [FR(19, (108, 244, 162, 270), 'f′= fc/(c−u)', 4), R('f′=1.2 f', 3), R('u=56.7 m s⁻¹', 3)],
      'phys-2-7', 'speed-of-the-source', SQ(19, 'Calculate the speed of the source.'), 10,
      stem=[SOURCE12, SOUND12]),
    T('12civ', 'Q12(c)(iv)', 'B', P(11, 'The Doppler effect is also used to detect the red‐shift of galaxies.',
                                   'What does the red‐shift tell us about the universe?'),
      [R('Universe is expanding', 4)], 'phys-2-7', 'red-shift',
      SQ(19, 'The Doppler effect is also used to detect the red shift of galaxies. What does the red shift',
         'tell us about the universe?'), 4),
    T('12di', 'Q12(d)(i)', 'B', P(11, 'What is current?'),
      [R('The flow', 3), R('Of charge', 3)], 'phys-3-3', 'what-is-current', SQ(19, 'What is current?'), 6,
      stem=[AMP12]),
    T('12dii', 'Q12(d)(ii)', 'B', P(11, 'Calculate the current flowing when a mole (6.0 × 10²³) of',
                                   'electrons passes a point in 30 minutes.'),
      [R('Q=(6.0 ×10²³)(1.6×10⁻¹⁹)=96000 C', 3), FR(19, (108, 502, 200, 528), 'I= Q/t =53.3 A', 3)],
      'phys-3-3', 'current-from-a-mole-of-electrons',
      SQ(19, 'Calculate the current flowing when one mole (6.0 × 10²³) of electrons passes a point in',
         '30 minutes.'), 6, stem=[AMP12]),
    T('12diii', 'Q12(d)(iii)', 'B', P(11, 'Explain why this phenomenon occurs.'),
      [R('Each current carrying wire has a magnetic field', 4),
       R('Each wire experiences a force in the other’s magnetic field', 3)],
      'phys-3-5', 'force-between-parallel-conductors', SQ(19, 'Explain why this phenomenon occurs.'), 7,
      stem=[PREV12]),
    T('12div', 'Q12(d)(iv)', 'B', P(11, 'Describe a laboratory experiment to demonstrate this phenomenon.'),
      [R('Power supply and U‐shaped foil', 3), R('Allow current to flow', 3), R('Foil moves', 3)],
      'phys-3-5', 'demonstrating-force-between-conductors',
      SQ(19, 'Describe a laboratory experiment to demonstrate this phenomenon.'), 9, stem=[PREV12]),
]

FIGURES = {
    # key suffix: (doc, page, rect in PDF points, credit, letters, alt, solution[, masks])
    'q1-data': ('paper', 2, (80, 226, 445, 306), SEC, [],
                'The recorded data: mass of body A = 125.6 g; mass of body B = 111.1 g; distance travelled by body '
                'A for 0.2 s before collision = 11.4 cm; distance travelled by bodies A and B for 0.2 s after '
                'collision = 6.1 cm.', False),
    'q2iii-scheme-table': ('scheme', 6, (130, 392, 465, 442), SEC, [],
                           "The marking scheme's table of values: sin i 0.50, 0.64, 0.77, 0.87, 0.94, 0.98; sin r "
                           "0.33, 0.42, 0.52, 0.57, 0.63, 0.66.", True),
    'q3iv-scheme-table': ('scheme', 7, (130, 420, 465, 470), SEC, [],
                          "The marking scheme's table of values: f 250, 300, 350, 400, 450, 500; 1/l 2.94, 3.53, 4.17, "
                          "4.88, 5.24, 5.88.", True),
    'q5i-photocell': ('paper', 4, (380, 425, 545, 595), SEC, [],
                      'A sketch of a photocell: a glass tube on a base with four pins, holding two electrodes, one '
                      'labelled Cathode and the other labelled Anode.', False,
                      [(380, 496, 424, 512), (380, 540, 404, 556)]),
    'q7-pear': ('paper', 6, (440, 55, 542, 212), 'uaf.edu; pinterest.ch', [],
                'Photograph of a pear-shaped metal body on an insulating stand: a rounded end on the left tapering to '
                'a point on the right.', False),
    'q10a-map': ('paper', 8, (270, 130, 550, 215), SEC, [],
                 'Drawing of a curved section of the Earth, shaded grey, with Sanford Lab (Lead, South Dakota) marked '
                 'on the left and Fermilab (Batavia, Illinois) on the right, joined by a dashed straight line through '
                 'the Earth labelled 1300 km.', False),
}
