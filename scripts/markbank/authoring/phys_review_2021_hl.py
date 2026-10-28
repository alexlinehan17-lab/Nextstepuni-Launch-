"""Physics 2021 Higher Level — reviewed task ledger, correcting the sitting in place.

Independent visual sweep (2026-10-28), every page rendered and read:
  * The paper (LC021ALP000EV), 16 pages: p1 cover ("Answer two questions from
    Section A and four questions from Section B"; the 2021 papers were adjusted
    to compensate for disruptions to learning due to COVID-19), p2-p4 Section A
    (80 marks) Questions 1-5 (any two, 40 marks each), p5-p15 Section B (224
    marks) Questions 6-14 (any four, 56 marks each), p15 also the
    acknowledgements (images on pages 5-15), p16 back cover (copyright notice).
  * The marking scheme, 28 pages: p1 cover, p2 note on published schemes, p3
    points to note (solidus, double solidus, units, graphs, slips), p4
    annotation symbols, p5 Irish-language bonus table (Tábla 304), p6-p24
    Questions 1-14 (each question reprinted, its answers in bold, the mark cells
    "(3)" at the right margin), p25-p27 blank, p28 back cover.

Every printed ask is carded at the scheme's own mark boundary: a roman, or a
sub-letter inside a roman where the scheme prices (a) and (b) apart (Q1(ii),
Q8(vii)). Sections A and B print a group mark after a run of romans ("(22)"
closing Q1(i)-(iii)): GROUP_TOTALS. Q6 is any eight of (a)-(l) at 7 each
(8 x 7): one card per letter. Q13 is either (a) or (b) and Q14 any two of
(a)-(d): every part is carded. A cell "(4 + 3)" set against two answer lines
that are one statement, or against (a) and (b) of one ask, is carded in the
order printed; set against interchangeable items (Q6(c)'s two laws, Q6(i),
Q6(l), Q12(ix), Q13(a)(vii), Q13(b)(iv)) it is a menu priced step by step, the
2022 and 2024 Higher convention. "(any 2 x 3)" menus are anyn. A line of
several items priced "(4 x 3)", "(3 x 3)", "(3 x 2)", "(4 x 1)" is cut at the
scheme's own commas, one row per item. A definition printed "words // expression"
or "words // notation" is one row per printed line, as printed, with the
scheme's own "//" rule as the note (the 2023-2025 convention). The "//" columns
of Q2(vi), Q2(vii), Q6(h), Q10(vi) and Q11(iv) are routes inside their cards;
Q10(vi)'s first and last lines, printed identically on both sides, are common
rows, and Q6(h)'s and Q11(iv)'s sides are menus so each card keeps within six
rows.

The scheme sets its three nuclear equations (Q6(k), Q11(i), Q13(a)(iv)) in
CambriaMath with each nuclide's numbers stacked AFTER the symbol; they are read
with G('equation'). Q13(a)(iv)'s antiproton bar is CambriaMath glyph 3364,
whose ToUnicode reads U+0D24 (a Malayalam letter): looked at on the rendered
page it is the bar over the p, read as U+0305 COMBINING OVERLINE (GLYPHS), as
2024 Higher reads the same glyph. No line of this scheme is set in a doubled
maths font. The paper sets its superscript minus as a hyphen U+2010 ("kg‐1"),
read as a superscript minus, and the tables' headers lose their theta: every
table is a crop, and Q5(iv) shows the table with the data
line under it (the asks between them masked).

The sitting was already carded (118 authored entries: 110 ids, eight of them
present twice). Every task is re-derived from the PDFs and every id is kept,
mapped (`id=`) to the task it was carding. The asks the bank had excluded
(Q2(iv), Q8(ii), Q10(ii), Q10(iii), Q11(i), Q13(a)(iv), Q14(b)(ii)) and the one
it had left open (Q7(ix)) are carded, and the bundled parts (Q1(ii), Q8(vii),
Q9(vii)-(viii), Q14(c)(i)-(iii)) are split at the scheme's own boundaries.
"""
from phys_review_lib import Q, SQ, S, M, G, pt, anyn, T, unprinted

YEAR, LEVEL = 2021, 'hl'
REVIEWED_AT = '2026-10-28'
BASELINE_COMMIT = '99ec7f0a0d6b243f4d5a1dc9b14a6a958e98095e'

SOURCES = {
    'paper': {'path': 'examiner-reports/physics/papers/2021-hl-paper.pdf', 'fileid': 'LC021ALP000EV.pdf',
              'sha256': '877a47fe07317037cee6147a35ec8648b91052b4748b3580dbf156c60e2c2d39', 'pages': 16},
    'scheme': {'path': 'examiner-reports/physics/schemes/2021-hl.pdf', 'fileid': 'LC021ALP000EV.pdf',
               'sha256': '7184b7194b479b4ee5129ea50847ff6f3a827df37a39f962fc5ccbe85a4b380d', 'pages': 28},
}

PAGE_ROLES = {
    'paper': {1: 'cover', **{p: 'questions' for p in range(2, 15)}, 15: 'questions-acknowledgements',
              16: 'back-cover'},
    'scheme': {1: 'cover', 2: 'note', 3: 'conventions', 4: 'annotations', 5: 'irish-bonus',
               **{p: 'marking' for p in range(6, 25)}, 25: 'blank', 26: 'blank', 27: 'blank', 28: 'back-cover'},
}

LETTERED = {6, 13, 14}

# The antiproton's bar in Q13(a)(iv) (scheme p19): CambriaMath glyph 3364, the only glyph of this id in the
# scheme, whose ToUnicode reads U+0D24. Peeked at 300 dpi: it is the bar drawn over the second p.
GLYPHS = {'scheme': {'CambriaMath': {3364: '̅'}}}

QUESTION_TOTALS = {**{n: 40 for n in range(1, 6)}, **{n: 56 for n in range(6, 13)},
                   13: 112,   # either (a) or (b), 56 each: both carded
                   14: 112}   # any two of (a)-(d), 28 each: all four carded
PART_TOTALS = {(13, 'a'): 56, (13, 'b'): 56, **{(14, x): 28 for x in 'abcd'}}
BEST_OF = {6: (8, 7)}
GROUP_TOTALS = {
    (1, ('i', 'ii', 'iii')): 22, (1, ('iv', 'v')): 18,
    (2, ('i', 'ii', 'iii', 'iv', 'v')): 25, (2, ('vi', 'vii')): 15,
    (3, ('i', 'ii')): 18, (3, ('iii', 'iv')): 22,
    (4, ('i', 'ii')): 15, (4, ('iii', 'iv')): 12, (4, ('v', 'vi')): 13,
    (5, ('i', 'ii')): 15, (5, ('iii', 'iv')): 25,
    (7, ('i', 'ii', 'iii')): 12, (7, ('iv', 'v', 'vi', 'vii', 'viii')): 32, (7, ('ix', 'x')): 12,
    (8, ('i', 'ii', 'iii', 'iv')): 28, (8, ('v', 'vi', 'vii', 'viii', 'ix')): 28,
    (9, ('i', 'ii', 'iii')): 18, (9, ('iv', 'v', 'vi')): 30, (9, ('vii', 'viii')): 8,
    (10, ('i', 'ii', 'iii')): 18, (10, ('iv', 'v')): 15, (10, ('vi', 'vii', 'viii')): 23,
    (11, ('i', 'ii')): 23, (11, ('iii', 'iv')): 12, (11, ('v', 'vi', 'vii', 'viii')): 21,
    (12, ('i', 'ii')): 18, (12, ('iii', 'iv', 'v', 'vi')): 21, (12, ('vii', 'viii', 'ix')): 17,
}
CHECKSUMS = {}
ROUTES = {}

SCAN_PAGES = {'paper': range(2, 16)}
SELECTION_SCAN = [
    ('paper', 2, 'the following', 'Q1 "The following data were recorded": a reference to the table.'),
    ('paper', 3, 'the following', 'Q2 "The following data were recorded": a reference to the table.'),
    ('paper', 3, 'the following', 'Q3 "The following data were recorded": a reference to the table.'),
    ('paper', 4, 'the following', 'Q4 "The following data were recorded": a reference to the table.'),
    ('paper', 4, 'the following', 'Q5 "The following data were recorded": a reference to the table.'),
    ('paper', 5, 'the following', 'Q6 "Answer any eight of the following parts": a best-eight of (a)-(l) at 7 '
                                  'each (8 x 7); every part is carded (BEST_OF).'),
    ('paper', 5, 'both', 'Q6(f) "a pipe that is open at both ends": description.'),
    ('paper', 10, 'both', 'Q11 lead-in "They both worked under Rutherford": description.'),
    ('paper', 12, 'either', 'Q13 "Answer either part (a) or part (b)": whole-part choice; both parts are carded.'),
    ('paper', 12, 'or', 'Q13, the same choice.'),
    ('paper', 12, 'the following', 'Q13(a) "Read the following passage": a reference to the passage.'),
    ('paper', 13, 'the following', 'Q13(b) "Read the following passage": a reference to the passage.'),
    ('paper', 13, 'or', 'Q13(b) passage "amplify voltage or switch electronic signals": description.'),
    ('paper', 14, 'any two', 'Q14 "Answer any two of the following parts": whole-part choice; every part is carded.'),
    ('paper', 14, 'the following', 'Q14, the same rubric.'),
    ('paper', 15, 'or', 'Q14(d)(i) "Is the image real or virtual?": the answer options.'),
]
ASK_SCAN_PAGES = {'paper': range(2, 16)}
ASK_EXEMPT = [
    (9, 'When placed in an external magnetic field', 'Q10 lead-in to (iv) ("When placed in an external magnetic '
                                                     'field, a current-carrying conductor may experience a force."): a '
                                                     'description, not an ask; lifted into the stem of (iv).'),
    (13, 'electrode. When a small current flowed', 'Q13(b) passage ("When a small current flowed through one of the '
                                                   'electrodes, ..."): description, not an ask.'),
    (14, 'sphere. When the magnet is attached', 'Q14(a) lead-in to (iv) ("When the magnet is attached to the sphere, '
                                               'the length of the spring increases by 15 mm."): description; lifted '
                                               'into the stem of (iv).'),
    (14, 'Sound travels faster in water than in air.', 'Q14(b) lead-in to (iv) ("When a sound wave travels from water '
                                                       'into air, it undergoes refraction."): description; lifted into '
                                                       'the stem of (iv).'),
    (15, 'State Examinations Commission', 'Acknowledgements: image credits, not an ask.'),
    (15, 'flinnsci.com', 'Acknowledgements ("flinnsci.com: State Examinations Commission"): an image credit, not an '
                         'ask.'),
]

SEC = 'State Examinations Commission'
CRIT = 'The scheme prints no answer here, only what earns the marks.'
EXPT = 'A "describe an experiment" part: the scheme prices apparatus, method and observation and prints no answer.'
NODIAG = S('(–1 if no diagram present or no label present)')
SPECIES = S('(–3 for each additional incorrect species)')
LEGEND = S('Answers that are separated by a double solidus, //, are answers which are mutually',
           'answer from the other side.', page=3)
ORDERED = ('The scheme prints these items under one sum, {cell}, and names no order: a response earns the marks '
           'step by step.')
DOUBLE = ('Each line printed with its // side, which names the alternative ("expression", "equation for c", '
          '"notation") without printing a formula: one row per line, as printed.')


LINKED = ('{w} reads to the figure-pointer check as a printed figure; {why}, so the card links its exam '
          'page.')
OWN = 'the ask is the student\'s own drawing'
IMAGE = 'it is the image the mirror forms, and the paper prints no figure for it'


def P(page, start, end=None, **kw):
    return Q(page, start, end, **kw)


def R(text, marks, end=None, **kw):
    """A row lifted whole from the task's scheme page."""
    return pt(S(text, end), marks, **kw)


def C(text, marks, end=None, note=CRIT, **kw):
    """A criterion the scheme prices without printing an answer."""
    return pt(S(text, end), marks, kind='criterion', note=note, **kw)


def items(line, marks, kinds=None, note_last=None):
    """One row per item of a line the scheme prices "(4 x 3)": the items cut at its own commas."""
    n = line.count(',') + 1
    kinds = kinds or [None] * n
    out = []
    for k in range(1, n + 1):
        kind = kinds[k - 1]
        extra = {'kind': 'criterion', 'note': CRIT} if kind == 'criterion' else {}
        if k == n and note_last is not None:
            extra['note_sel'] = note_last
        out.append(pt(S(line, piece=k, psep=','), marks, **extra))
    return out


def bundled(parts, keep):
    return f'The old card bundled {parts}, which the scheme prices apart; it keeps its id for {keep}.'


# ------------------------------------------------------------------ stems --
STEM1 = P(2, 'In an experiment to determine the acceleration due to gravity, a student set up a simple',
          'lengths l of the pendulum.')
Q1I = P(2, 'Draw a labelled diagram of how the apparatus was arranged in this experiment.')
Q1II = P(2, 'Indicate on the diagram')
STEM2 = P(3, 'In an experiment to determine the focal length of a concave mirror, a student first made an',
          'object distances u.')
STEM2B = P(3, 'Another student carried out this experiment but she measured the image distance v for each of six',
           'used the graph to calculate the focal length.')
STEM3 = P(3, 'A student investigated how the fundamental frequency f of a stretched string varied with its',
          'length of 65 cm.')
STEM4 = P(4, 'A student measured the resistance R of a wire of length 30 cm at different values of temperature θ.')
DIAM4 = P(4, 'The student measured the diameter of the wire to be 2.4 mm.')
STEM5 = P(4, 'In an experiment to verify Joule’s law a constant current I was passed through a heating coil',
          'kept constant at 105 g.')
STEM7 = P(6, 'An object A of mass 45 g is travelling at a horizontal', 'recoils with a speed of 1.1 m s⁻¹.')
CALC7 = P(6, 'Calculate')
G7 = P(6, '(acceleration due to gravity = 9.8 m s⁻²)')
CUT7 = P(6, 'The string is cut at the instant B is at its maximum height.')
Q8V = P(7, 'Calculate the angular separation between the two 3rd order images', 'lines per mm.')
Q8VII = P(7, 'What changes would be observed if the blue light was replaced (a) with red light,')
ICE9 = P(8, 'Ice is used as a coolant due to the high specific heat capacities', 'latent heat of fusion of ice.')
SHOWN9 = P(8, 'It is the principal coolant used', 'such as the one shown.')
PICNIC9 = P(8, 'A picnic box contains food items', 'the temperature of the food decreases.')
DATA9 = [P(8, '(specific heat capacity of ice = 2100'), P(8, '(specific latent heat of fusion of ice')]
PUMP9 = P(8, 'Freezers and refrigerators operate by use of a heat pump.')
APP9 = P(8, 'A student used the apparatus shown below to investigate how heat travels through water.')
CURRENT10 = P(9, 'A current flowing through a conductor creates a magnetic field around it.')
FORCE10 = P(9, 'When placed in an external magnetic field')
LOOP10 = P(9, 'A square loop of side 5 cm', 'field.')
NEUTRON11 = P(10, 'Shortly before this photograph was taken', 'a neutron was emitted.')
GEIGER11 = P(10, 'Geiger is best remembered for co')
GOLD11 = P(10, 'While working with Rutherford, Geiger assisted on the gold foil experiment.')
CAP12 = P(11, 'The plates of a parallel plate capacitor of capacitance 3.2 pF have a', 'are 15 mm apart.')
XRAY12 = P(11, 'A voltage of 20 kV is applied between the cathode and the anode in an X')
SPHERE14 = P(14, 'An iron sphere of mass 40 g hangs from a spring', 'The period of oscillation is 0.74 s.')
MAGNET14 = P(14, 'The iron sphere and the spring are brought to rest', '15 mm.')
G14 = P(14, '(acceleration due to gravity = 9.8 m s⁻²)')
HYDRO14 = P(14, 'Hydroacoustics is the study of sound in water.', 'hydroacoustics.')
SOURCE14 = P(14, 'A moving underwater source emits', 'a frequency of 806 kHz.')
REFR14 = P(14, 'Sound travels faster in water than in air.', 'undergoes refraction.')
C14 = P(14, '(speed of sound in water = 1480 m s⁻¹)')
PHOTO14 = P(15, 'In the photoelectric effect electrons are emitted', 'the threshold frequency.')
DESC14 = P(15, 'Describe what happens when')
LIGHT14 = P(15, 'Light of wavelength 440 nm is incident on a metal that has a work function of 2.6 eV.')
BALL14 = [P(15, 'Ball lenses are glass spheres which can be used for special effects in photography.'),
          P(15, 'Light travels at a different speed in air and in glass.')]
CRITANGLE14 = P(15, 'The critical angle of the glass in a ball lens is 41.4°.')

TASKS = [
    # ============================================================ Section A ==
    # ---------------------------------------------------------------- Q1 --
    T('1i', 'Q1(i)', 'A', Q1I,
      [C('correct arrangement of bob', 3), R('string', 3),
       R('split cork or similar / timer / metre stick', 3, note_sel=NODIAG)], 'phys-1-5', 'pendulum-apparatus',
      SQ(6, 'Draw a labelled diagram of how the apparatus was arranged in this experiment.'), 9, stem=[STEM1],
      id='phys-2021-hl-q1-i'),
    T('1iia', 'Q1(ii)(a)', 'A', [Q1II, M('(a)', 2), P(2, 'the fixed point of suspension,')],
      [R('bottom of split cork or similar', 3)], 'phys-1-5', 'fixed-point-of-suspension',
      SQ(6, 'the fixed point of suspension,'), 3, stem=[STEM1, M('(i)', 2), Q1I], id='phys-2021-hl-q1-ii',
      source_pages=[2],
      decision='The paper prints (a) and (b) under one roman, priced apart ((3), and (2 + 2)). ' +
               bundled('(a) and (b)', '(a)') + ' ' + LINKED.format(w='"the diagram"', why=OWN)),
    T('1iib', 'Q1(ii)(b)', 'A', [Q1II, M('(b)', 2), P(2, 'the distance l.')],
      [R('from fixed point of suspension', 2), R('to midpoint of bob', 2)], 'phys-1-5', 'pendulum-length',
      SQ(6, 'the distance l.'), 4, stem=[STEM1, M('(i)', 2), Q1I], source_pages=[2],
      decision='"(2 + 2)" against the two lines of one statement: in the order printed. ' +
               LINKED.format(w='"the diagram"', why=OWN)),
    T('1iii', 'Q1(iii)', 'A', P(2, 'Why did the student measure the time for 20 oscillations rather than the time for one',
                               'oscillation?'),
      [R('to get an average / to get a larger value (for time) / greater accuracy / it is difficult to know', 6,
         end='when an oscillation starts or finishes')], 'phys-1-5', 'timing-twenty-oscillations',
      SQ(6, 'Why did the student measure the time for 20 oscillations rather than the time for one', 'oscillation?'),
      6, stem=[STEM1], id='phys-2021-hl-q1-iii'),
    T('1iv', 'Q1(iv)', 'A', P(2, 'Use the data to draw a suitable graph to calculate the acceleration due to gravity, g.'),
      [C('values for (t/20)²', 3), C('labelled axes', 3), C('correct points plotted', 3), C('line of best fit', 3)],
      'phys-1-5', 'pendulum-graph',
      SQ(6, 'Use the data to draw a suitable graph to calculate the acceleration due to gravity, g.'), 12,
      stem=[STEM1], fig='q1-table', id='phys-2021-hl-q1-iv'),
    T('1v', 'Q1(v)', 'A', P(2, 'Hence determine g.'),
      [C('slope formula', 3), R('g (≈ 9.8 m s', 3)], 'phys-1-5', 'g-from-pendulum-graph',
      SQ(6, 'Hence determine g.'), 6, stem=[STEM1, M('(iv)', 2),
                                          P(2, 'Use the data to draw a suitable graph to calculate the acceleration')],
      fig='q1-table', id='phys-2021-hl-q1-v'),
    # ---------------------------------------------------------------- Q2 --
    T('2i', 'Q2(i)', 'A', P(3, 'Why did the student first make an approximate measurement of the focal length?'),
      [R('to ensure that the object was placed outside the focal point / so that a real image would', 6,
         end='be formed / so that the image can be formed on a screen / to check final answer')], 'phys-2-3',
      'approximate-focal-length',
      SQ(7, 'Why did the student first make an approximate measurement of the focal length?'), 6, stem=[STEM2],
      id='phys-2021-hl-q2-i', source_pages=[3], decision=LINKED.format(w='"the image distance"', why=IMAGE)),
    T('2ii', 'Q2(ii)', 'A', P(3, 'How did the student determine the image positions?'),
      [R('moved a screen until a sharp image was seen', 3)], 'phys-2-3', 'locating-the-image',
      SQ(7, 'How did the student determine the image positions?'), 3, stem=[STEM2], id='phys-2021-hl-q2-ii',
      source_pages=[3], decision=LINKED.format(w='"the image distance"', why=IMAGE)),
    T('2iii', 'Q2(iii)', 'A', P(3, 'Draw a labelled diagram of how the apparatus was arranged.'),
      items('object, mirror, screen, correct arrangement', 1, kinds=[None, None, None, 'criterion'],
            note_last=NODIAG), 'phys-2-3', 'concave-mirror-apparatus',
      SQ(7, 'Draw a labelled diagram of how the apparatus was arranged.'), 4, stem=[STEM2], id='phys-2021-hl-q2-iii',
      source_pages=[3],
      decision='"(4 × 1)" against one line of four items: one row per item, cut at the scheme\'s commas; "correct '
               'arrangement" names what earns the mark without an answer. ' +
               LINKED.format(w='"the image distance"', why=IMAGE)),
    T('2iv', 'Q2(iv)', 'A', P(3, 'On your diagram, indicate u and v.'),
      [unprinted(6, 'The scheme prints only the tariff "(2 × 3)" (two items at 3 marks) beside its reprint of this ask, '
                    'and no answer line.')],
      'phys-2-3', 'showing-u-and-v', SQ(7, 'On your diagram, indicate u and v.'), 6,
      stem=[STEM2, M('(iii)', 3), P(3, 'Draw a labelled diagram of how the apparatus was arranged.')],
      evidence='Paper p3 prints "(iv) On your diagram, indicate u and v." inside the run Q2(i)-(v) "(25)". Scheme p7 '
               '(printed page 5) prints the reprint "(iv) On your diagram, indicate u and v." with the cell "(2 × 3)" '
               'on the same line and no answer line under it; the next line is "(v)" (rendered and looked at, '
               '2026-10-28).',
      source_pages=[3],
      decision='The bank had excluded this part. The scheme prices it "(2 × 3)" and prints no answer: one unprinted '
               'row at 6. ' + LINKED.format(w='"the image distance"', why=IMAGE)),
    T('2v', 'Q2(v)', 'A', P(3, 'Use all of the data to calculate the focal length of the mirror.'),
      [C('formula', 3), R('average value for f (≈ 12.1 cm)', 3, note_sel=S('(–1 if average not found)'))],
      'phys-2-3', 'focal-length-from-data', SQ(7, 'Use all of the data to calculate the focal length of the mirror.'),
      6, stem=[STEM2], fig='q2-table', id='phys-2021-hl-q2-v'),
    T('2vi', 'Q2(vi)', 'A', P(3, 'Sketch a suitable graph that might have been drawn.'),
      [R('correct x-axis (1/u)', 3, route='side-a', note_sel=LEGEND), R('correct y-axis (1/v)', 3, route='side-a'),
       R('correct shape of curve (straight line with m', 3, route='side-a'),
       pt(S('// correct x-axis (u)', piece=2, psep='//'), 3, route='side-b'),
       pt(S('// correct y -axis (v)', piece=2, psep='//'), 3, route='side-b'),
       pt(S('// correct shape of curve', piece=2, psep='//'), 3, kind='criterion', note=CRIT, route='side-b')],
      'phys-2-3', 'mirror-graph-sketch', SQ(7, 'Sketch a suitable graph that might have been drawn.'), 9,
      stem=[STEM2B], id='phys-2021-hl-q2-vi', source_pages=[3],
      decision='The scheme prints two sketches side by side, separated by "//" (1/v against 1/u, or v against u): '
               'routes inside the card, each (3) (3) (3). ' + LINKED.format(w='"the image distance"', why=IMAGE)),
    T('2vii', 'Q2(vii)', 'A', P(3, 'How could this graph be used to calculate the focal length?'),
      [R('intercept(s)', 3, route='side-a', note_sel=LEGEND), R('= 1/f', 3, route='side-a'),
       pt(S('// point on curve', piece=2, psep='//'), 3, route='side-b'),
       pt(S('// substitute into formula', piece=2, psep='//'), 3, route='side-b')],
      'phys-2-3', 'focal-length-from-graph', SQ(7, 'How could this graph be used to calculate the focal length?'), 6,
      stem=[STEM2B], id='phys-2021-hl-q2-vii', source_pages=[3],
      decision='Two methods side by side, separated by "//": routes inside the card, each (3) (3). ' +
               LINKED.format(w='"the image distance"', why=IMAGE)),
    # ---------------------------------------------------------------- Q3 --
    T('3i', 'Q3(i)', 'A', P(3, 'Draw a labelled diagram of how the apparatus was arranged in this experiment.'),
      [R('stretched string', 3), R('newtonmeter / weights and pan', 3), R('metre stick / bridge(s) / paper rider', 3),
       R('tuning fork', 3, note_sel=NODIAG)], 'phys-2-6', 'sonometer-apparatus',
      SQ(8, 'Draw a labelled diagram of how the apparatus was arranged in this experiment.'), 12, stem=[STEM3],
      id='phys-2021-hl-q3-i'),
    T('3ii', 'Q3(ii)', 'A', P(3, 'Describe how the student used the apparatus.'),
      [R('held (vibrating) tuning fork to string and changed T', 3), R('paper rider fell off / loud sound', 3)],
      'phys-2-6', 'finding-resonance-by-tension', SQ(8, 'Describe how the student used the apparatus.'), 6,
      stem=[STEM3], id='phys-2021-hl-q3-ii'),
    T('3iii', 'Q3(iii)', 'A', P(3, 'Draw a suitable graph to show the relationship between f and T.'),
      [C('values for f', 3), C('labelled axes', 3), C('correct points plotted', 3), C('line of best fit', 3)],
      'phys-2-6', 'frequency-tension-graph', SQ(8, 'Draw a suitable graph to show the relationship between f and T.'),
      12, stem=[STEM3], fig='q3-table', id='phys-2021-hl-q3-iii'),
    T('3iv', 'Q3(iv)', 'A', P(3, 'Use your graph to calculate the mass per unit length (linear density) of the string.'),
      [C('slope formula', 3), R('value of slope', 2), C('formula', 3), R('μ (≈', 2)], 'phys-2-6',
      'linear-density-from-graph', SQ(8, 'Use your graph to calculate the mass per unit length'), 10, stem=[STEM3],
      fig='q3-table', id='phys-2021-hl-q3-iv'),
    # ---------------------------------------------------------------- Q4 --
    T('4i', 'Q4(i)', 'A', P(4, 'Draw a labelled diagram of how the apparatus was arranged in this experiment.'),
      items('resistor (in liquid), ohmmeter, source of heat, thermometer', 3, note_last=NODIAG), 'phys-3-3',
      'resistance-temperature-apparatus',
      SQ(9, 'Draw a labelled diagram of how the apparatus was arranged in this experiment.'), 12, stem=[STEM4],
      id='phys-2021-hl-q4-i',
      decision='"(4 × 3)" against one line of four pieces of apparatus: one row per item, cut at the scheme\'s commas.'),
    T('4ii', 'Q4(ii)', 'A', P(4, 'How did the student make the temperature of the wire 0 °C?'),
      [R('ice bath', 3)], 'phys-3-3', 'wire-at-zero-celsius',
      SQ(9, 'How did the student make the temperature of the wire 0 °C?'), 3, stem=[STEM4], id='phys-2021-hl-q4-ii'),
    T('4iii', 'Q4(iii)', 'A', P(4, 'Draw a suitable graph to show the relationship between R and θ.'),
      [C('labelled axes', 3), C('correct points plotted', 3), C('line of best fit', 3)], 'phys-3-3',
      'resistance-temperature-graph', SQ(9, 'Draw a suitable graph to show the relationship between R and'), 9,
      stem=[STEM4], fig='q4-table', id='phys-2021-hl-q4-iii'),
    T('4iv', 'Q4(iv)', 'A', P(4, 'Use your graph to determine the temperature when the resistance is 6 Ω.'),
      [R('value consistent with graph (≈ 55.5 °C)', 3)], 'phys-3-3', 'temperature-from-graph',
      SQ(9, 'Use your graph to determine the temperature when the resistance is 6 Ω.'), 3, stem=[STEM4],
      fig='q4-table', id='phys-2021-hl-q4-iv'),
    T('4v', 'Q4(v)', 'A', P(4, 'How did the student measure the diameter of the wire?'),
      [R('micrometer / digital callipers / vernier callipers', 4)], 'phys-3-3', 'measuring-wire-diameter',
      SQ(9, 'How did the student measure the diameter of the wire?'), 4, stem=[DIAM4], id='phys-2021-hl-q4-v'),
    T('4vi', 'Q4(vi)', 'A', P(4, 'Calculate the resistivity of the metal at a temperature of 20 °C.'),
      [C('formula', 3), R('substitution / area', 3), R('ρ = 8.44', 3)], 'phys-3-3', 'resistivity-at-20-celsius',
      SQ(9, 'Calculate the resistivity of the metal at a temperature of 20 °C.'), 9, stem=[STEM4, DIAM4],
      fig='q4-table', id='phys-2021-hl-q4-vi'),
    # ---------------------------------------------------------------- Q5 --
    T('5i', 'Q5(i)', 'A', P(4, 'Draw a labelled diagram of how the apparatus was arranged in this experiment.', nth=2),
      [R('power source', 3), C('means of varying current', 3), R('ammeter in series', 3),
       R('thermometer / coil (in water)', 3, note_sel=NODIAG)], 'phys-3-3', 'joules-law-apparatus',
      SQ(10, 'Draw a labelled diagram of how the apparatus was arranged in this experiment.'), 12, stem=[STEM5],
      id='phys-2021-hl-q5-i'),
    T('5ii', 'Q5(ii)', 'A', P(4, 'Why was the current allowed to flow for a constant period of time?'),
      [R('to remove time as a variable', 3)], 'phys-3-3', 'constant-time',
      SQ(10, 'Why was the current allowed to flow for a constant period of time?'), 3, stem=[STEM5],
      id='phys-2021-hl-q5-ii'),
    T('5iii', 'Q5(iii)', 'A', P(4, 'Draw a suitable graph to verify Joule’s law.'),
      [C('values for I²', 3), C('labelled axes', 3), C('correct points plotted', 3), C('line of best fit', 3)],
      'phys-3-3', 'joules-law-graph', SQ(10, 'Draw a suitable graph to verify Joule’s law.'), 12, stem=[STEM5],
      fig='q5-table', id='phys-2021-hl-q5-iii'),
    T('5iv', 'Q5(iv)', 'A', P(4, 'Use your graph to calculate the average resistance of the heating coil.'),
      [C('slope formula', 3), R('value of slope (≈ 2.03)', 3), R('I²Rt /', 3), R('I²Rt =', 2), R('R (≈ 3.71 Ω)', 2)],
      'phys-3-3', 'resistance-of-heating-coil',
      SQ(10, 'Use your graph to calculate the average resistance of the heating coil.'), 13, stem=[STEM5],
      fig='q5-data', id='phys-2021-hl-q5-iv',
      decision='The paper\'s data line under the question reads "kg‐1 K‐1" in the text layer (its raised minus is a '
               'hyphen the reader leaves as printed), so the figure shows the table and that line as printed, the '
               'asks between them masked.'),
    # ============================================================ Section B ==
    # ---------------------------------------------------------------- Q6 --
    T('6a', 'Q6(a)', 'B', P(5, 'Define acceleration. Hence derive the expression v = u + at.'),
      [R('rate of change of velocity / equation plus notation', 3), R('a = (v', 2), C('rearrangement', 2)],
      'phys-1-1', 'acceleration-and-v-equals-u-plus-at',
      SQ(11, 'Define acceleration. Hence derive the expression v = u + at.'), 7, id='phys-2021-hl-q6-a',
      decision='The old card asked only "Define acceleration." for 3; the part asks for the derivation too, (2) (2).'),
    T('6b', 'Q6(b)', 'B', P(5, 'A ball is kicked with an initial velocity of 20 m s⁻¹',
                           'horizontal distance it travels in 1.2 seconds.'),
      [R('s = ut', 3), R('u = 20Cos50', 2), R('15.43 m', 2)], 'phys-1-1', 'horizontal-distance-of-projectile',
      SQ(11, 'A ball is kicked with an initial velocity of 20 m s⁻¹ at an angle of', 'in 1.2 seconds.'), 7,
      id='phys-2021-hl-q6-b'),
    T('6c', 'Q6(c)', 'B', P(5, 'State the laws of equilibrium', 'planar forces.'),
      [anyn(None, 2, 4, steps=[4, 3], note=ORDERED.format(cell='(4 + 3)'),
            options=[S('sum of the forces (in any direction) is zero'), S('sum of the moments (about any axis) is zero')])],
      'phys-1-2', 'laws-of-equilibrium', SQ(11, 'State the laws of equilibrium for a set of co-planar forces.'), 7,
      id='phys-2021-hl-q6-c',
      decision='"(4 + 3)" against the two laws, which the scheme prints in no order: a menu priced step by step.'),
    T('6d', 'Q6(d)', 'B', P(5, 'State an expression for the acceleration due to gravity at a distance of 2R above the surface',
                           'radius R.'),
      [R('g = GM/d²', 4), R('g = GM/9R²', 3)], 'phys-1-5', 'gravity-at-2r-above-surface',
      SQ(11, 'State an expression for the acceleration due to gravity at a distance of 2R above the surface',
         'radius R.'), 7, id='phys-2021-hl-q6-d'),
    T('6e', 'Q6(e)', 'B', P(5, 'Two different types of thermometer can give different', 'Explain why this happens.'),
      [R('different thermometric properties', 7)], 'phys-2-1', 'thermometers-disagree',
      SQ(11, 'Two different types of thermometer can give different readings when placed in the same',
         'Explain why this happens.'), 7, id='phys-2021-hl-q6-e'),
    T('6f', 'Q6(f)', 'B', P(5, 'Draw a labelled diagram to represent the second harmonic', 'open at both ends.'),
      [R('antinode shown at both ends', 4),
       R('one full wave shown (i.e. antinode-node-antinode-node-antinode)', 3, note_sel=S('(–1 if no label present)'))],
      'phys-2-6', 'second-harmonic-open-pipe',
      SQ(11, 'Draw a labelled diagram to represent the second harmonic of a stationary wave in a pipe',
         'open at both ends.'), 7, id='phys-2021-hl-q6-f'),
    T('6g', 'Q6(g)', 'B', P(5, 'Calculate the sound intensity 6 m from a loudspeaker of power 20 mW.'),
      [R('I = P/A', 3), R('substitution / A = 4πr²', 2), R('4.4 ×', 2)], 'phys-2-5', 'sound-intensity',
      SQ(12, 'Calculate the sound intensity 6 m from a loudspeaker of power 20 mW.'), 7, id='phys-2021-hl-q6-g'),
    T('6h', 'Q6(h)', 'B', P(5, 'List two primary colours of light. What colour of light is produced when equal intensities of',
                           'these two primary colours are mixed?'),
      [anyn(None, 2, 2, route='side-a', note_sel=LEGEND,
            options=[S('red and blue', piece=k, psep=' and ') for k in (1, 2)]),
       R('magenta', 3, route='side-a'),
       anyn(None, 2, 2, route='side-b',
            options=[S('// blue and green', piece=[2, k], psep=['//', ' and ']) for k in (1, 2)]),
       pt(S('// cyan/turquoise', piece=2, psep='//'), 3, route='side-b'),
       anyn(None, 2, 2, route='side-c',
            options=[S('// green and red', piece=[2, k], psep=['//', ' and ']) for k in (1, 2)]),
       pt(S('// yellow', piece=2, psep='//'), 3, route='side-c')],
      'phys-2-4', 'primary-and-secondary-colours',
      SQ(12, 'List two primary colours of light. What colour of light is produced when equal intensities of',
         'these two primary colours are mixed?'), 7, id='phys-2021-hl-q6-h',
      decision='The scheme prints three columns separated by "//": a pair of primary colours "(2 × 2)" over the '
               'colour they make "(3)". Routes inside the card, one per column: the pair cut at its own "and" into '
               'two claimable colours at 2 each (a menu row of both, so the card keeps within six rows), then the '
               'colour mixed at 3.'),
    T('6i', 'Q6(i)', 'B', P(5, 'Distinguish between earthing and bonding in domestic electricity.'),
      [anyn(None, 2, 4, steps=[4, 3], note=ORDERED.format(cell='(4 + 3)'),
            options=[S('earthing means providing a (conducting) path to Earth, i.e. joining to Earth'),
                     S('bonding means providing a (conducting) path between objects, i.e. joining objects')])],
      'phys-3-3', 'earthing-and-bonding',
      SQ(12, 'Distinguish between earthing and bonding in domestic electricity.'), 7, id='phys-2021-hl-q6-i',
      decision='"(4 + 3)" against the two definitions, which the scheme prints in no order: a menu priced step by '
               'step.'),
    T('6j', 'Q6(j)', 'B', P(5, 'Draw a circuit diagram to show how voltage and current are measured for a diode in reverse',
                           'bias.'),
      [R('diode shown in reverse bias', 3), R('(micro)ammeter in series with diode', 2),
       R('voltmeter across diode and microammeter', 2)], 'phys-3-3', 'reverse-bias-circuit',
      SQ(12, 'Draw a circuit diagram to show how voltage and current are measured for a diode in reverse', 'bias.'),
      7, id='phys-2021-hl-q6-j', source_pages=[5], decision=LINKED.format(w='"a circuit diagram"', why=OWN)),
    T('6k', 'Q6(k)', 'B', P(5, 'Carbon', 'equation for this decay.'),
      [G('equation', page=12, clip=(80, 422, 200, 452), expect='C¹⁴₆ → N¹⁴₇ + e⁰₋₁', marks=7,
         note_sel=SPECIES, note_lead='The scheme prices the equation (7 × 1).')],
      'phys-4-4', 'carbon-14-decay-equation', SQ(12, 'Carbon', 'equation for this decay.'), 7,
      id='phys-2021-hl-q6-k',
      decision='The scheme sets the equation in CambriaMath, each nuclide\'s numbers stacked after its symbol; the old '
               'card read them flattened ("C6 14 → N7 14 + e-1 0"). Read from where each number is printed: one row '
               'at the printed (7 × 1) = 7.'),
    T('6l', 'Q6(l)', 'B', P(5, 'In terms of how they interact with the neutrons in a fission reactor, distinguish between a',
                           'moderator and a control rod.'),
      [anyn(None, 2, 4, steps=[4, 3], note=ORDERED.format(cell='(4 + 3)'),
            options=[S('a moderator slows down neutrons'), S('a control rod absorbs/stops/blocks neutrons')])],
      'phys-4-6', 'moderator-and-control-rod',
      SQ(12, 'In terms of how they interact with the neutrons in a fission reactor, distinguish between a',
         'moderator and a control rod.'), 7, id='phys-2021-hl-q6-l',
      decision='"(4 + 3)" against the two roles, which the scheme prints in no order: a menu priced step by step.'),
    # ---------------------------------------------------------------- Q7 --
    T('7i', 'Q7(i)', 'B', P(6, 'State Newton’s second law of motion.'),
      [R('force is proportional to', 3, end='// expression', note_sel=LEGEND),
       R('rate of change of momentum', 3, end='// notation',
         note_sel=S('(allow maximum of 3 marks for F = ma with notation)'))],
      'phys-1-2', 'newtons-second-law', SQ(13, 'State Newton’s second law of motion.'), 6, id='phys-2021-hl-q7-i',
      decision=DOUBLE),
    T('7ii', 'Q7(ii)', 'B', P(6, 'State the principle of conservation of momentum.'),
      [R('momentum before interaction = momentum after interaction / formula and notation', 3)], 'phys-1-2',
      'conservation-of-momentum', SQ(13, 'State the principle of conservation of momentum.'), 3,
      id='phys-2021-hl-q7-ii'),
    T('7iii', 'Q7(iii)', 'B', P(6, 'State the principle of conservation of energy.'),
      [R('energy is not destroyed or created (just converted into a different form)', 3)], 'phys-1-4',
      'conservation-of-energy', SQ(13, 'State the principle of conservation of energy.'), 3, id='phys-2021-hl-q7-iii'),
    T('7iv', 'Q7(iv)', 'B', [CALC7, M('(iv)', 6), P(6, 'the force exerted by B on A,')],
      [R('F = (mu', 3), R('F = 0.045(6.2', 3)], 'phys-1-2', 'force-exerted-by-b-on-a',
      SQ(13, 'the force exerted by B on A,'), 6, stem=[STEM7], fig='q7-diagram', id='phys-2021-hl-q7-iv'),
    T('7v', 'Q7(v)', 'B', [CALC7, M('(v)', 6), P(6, 'the maximum velocity of B,')],
      [R('0.045(6.2) =', 3), R('v = 4.11', 3)], 'phys-1-2', 'maximum-velocity-of-b',
      SQ(13, 'the maximum velocity of B,'), 6, stem=[STEM7], fig='q7-diagram', id='phys-2021-hl-q7-v'),
    T('7vi', 'Q7(vi)', 'B', [CALC7, M('(vi)', 6), P(6, 'the magnitude and direction of the maximum', 'centripetal force on B,')],
      [R('F = mv²/r', 3), R('F = 0.08(4.11)', 3), R('upwards / towards P', 2)], 'phys-1-6',
      'maximum-centripetal-force', SQ(13, 'the magnitude and direction of the maximum centripetal force on B,'), 8,
      stem=[STEM7], fig='q7-diagram', id='phys-2021-hl-q7-vi'),
    T('7vii', 'Q7(vii)', 'B', [CALC7, M('(vii)', 6), P(6, 'the maximum height gained by B,')],
      [R('½mv² / mgh', 3), R('h = 0.86 m', 3)], 'phys-1-4', 'maximum-height-of-b',
      SQ(13, 'the maximum height gained by B,'), 6, stem=[STEM7, G7], fig='q7-diagram', id='phys-2021-hl-q7-vii'),
    T('7viii', 'Q7(viii)', 'B', [CALC7, M('(viii)', 6), P(6, 'the maximum angular displacement of the string.')],
      [R('cosα', 3), R('α = 73.6°', 3)], 'phys-1-6', 'maximum-angular-displacement',
      SQ(13, 'the maximum angular displacement of the string.'), 6, stem=[STEM7], fig='q7-diagram',
      id='phys-2021-hl-q7-viii'),
    T('7ix', 'Q7(ix)', 'B', P(6, 'Draw a labelled diagram to show the force(s) acting on B when it is at its maximum height.'),
      [R('downward arrow, labelled as weight', 3),
       R('labelled tension arrow in correct direction', 3, note_sel=S('(–3 for each additional incorrect force)'))],
      'phys-1-2', 'forces-on-b-at-maximum-height',
      SQ(13, 'Draw a labelled diagram to show the force(s) acting on B when it is at its maximum height.'), 6,
      stem=[STEM7], fig='q7-diagram',
      decision='The bank had left this part open. The scheme prices the weight and the tension arrows (3) (3).'),
    T('7x', 'Q7(x)', 'B', P(6, 'What is the magnitude and direction of the acceleration of B after the string is cut?'),
      [R('9.8 m s', 3), R('downwards', 3)], 'phys-1-5', 'acceleration-after-string-cut',
      SQ(13, 'What is the magnitude and direction of the acceleration of B after the string is cut?'), 6,
      stem=[STEM7, CUT7, G7], fig='q7-diagram', id='phys-2021-hl-q7-x'),
    # ---------------------------------------------------------------- Q8 --
    T('8i', 'Q8(i)', 'B', P(7, 'What is meant by diffraction?'),
      [R('spreading of a wave', 2), R('through a gap / around an obstacle', 2)], 'phys-2-3', 'diffraction',
      SQ(14, 'What is meant by diffraction?'), 4, id='phys-2021-hl-q8-i'),
    T('8ii', 'Q8(ii)', 'B', P(7, 'A diffraction experiment can be used to demonstrate', 'Describe such an experiment.'),
      items('apparatus, method, observation', 3, kinds=['criterion'] * 3), 'phys-2-6',
      'diffraction-experiment-wave-nature',
      SQ(14, 'A diffraction experiment can be used to demonstrate the wave nature of light. Describe', 'such an experiment.'),
      9, decision='The bank had excluded this part. ' + EXPT + ' "(3 × 3)" against the one line: one criterion row '
                  'per item, in the scheme\'s words.'),
    T('8iii', 'Q8(iii)', 'B', P(7, 'What is a diffraction grating?'),
      [R('a series of (transparent) gaps', 3)], 'phys-2-6', 'diffraction-grating',
      SQ(14, 'What is a diffraction grating?'), 3, id='phys-2021-hl-q8-iii'),
    T('8iv', 'Q8(iv)', 'B', P(7, 'Derive the diffraction grating formula, nλ = dsinθ.'),
      [R('d indicated', 3), R('θ indicated', 3), R('extra path length', 3), R('for constructive interference', 3)],
      'phys-2-6', 'deriving-grating-formula', SQ(14, 'Derive the diffraction grating formula, nλ = dsinθ.'), 12,
      id='phys-2021-hl-q8-iv'),
    T('8v', 'Q8(v)', 'B', Q8V,
      [R('d = 1.67', 3), R('sinθ = 3', 3), R('2θ =', 3)], 'phys-2-6', 'angular-separation-third-order',
      SQ(14, 'Calculate the angular separation between the two 3rd order images formed when blue light', 'lines per mm.'),
      9, id='phys-2021-hl-q8-v'),
    T('8vi', 'Q8(vi)', 'B', P(7, 'Calculate the distance between these images on a screen placed 50 cm from the grating.'),
      [R('tanθ', 3), R('2x = 1.31 m', 3)], 'phys-2-6', 'distance-between-images',
      SQ(14, 'Calculate the distance between these images on a screen placed 50 cm from the grating.'), 6,
      stem=[M('(v)', 7), Q8V], id='phys-2021-hl-q8-vi'),
    T('8viia', 'Q8(vii)(a)', 'B', Q8VII,
      [R('greater angular separation / fewer images', 3)], 'phys-2-6', 'red-light-instead-of-blue',
      SQ(14, 'What changes would be observed if the blue light was replaced'), 3, stem=[M('(v)', 7), Q8V],
      id='phys-2021-hl-q8-vii',
      decision='The paper prints (a) and (b) inside one ask, priced apart ((3) and (3)). ' +
               bundled('(a) and (b)', '(a)')),
    T('8viib', 'Q8(vii)(b)', 'B', [dict(Q8VII, piece=1, psep=' (a) with'), M('(b)', 7), P(7, 'with white light?')],
      [R('spectrum (on either side of white zero-order image)', 3)], 'phys-2-6', 'white-light-instead-of-blue',
      SQ(14, 'What changes would be observed if the blue light was replaced', '(b) with white light?'), 3,
      stem=[M('(v)', 7), Q8V],
      decision='The paper prints (a) and (b) inside one ask: the question is its lead-in with (b).'),
    T('8viii', 'Q8(viii)', 'B', P(7, 'Compare the wavelengths of radio waves with those of visible light.'),
      [R('radio waves have longer wavelengths (than visible light)', 3)], 'phys-2-4', 'radio-and-visible-wavelengths',
      SQ(14, 'Compare the wavelengths of radio waves with those of visible light.'), 3, id='phys-2021-hl-q8-viii'),
    T('8ix', 'Q8(ix)', 'B', P(7, 'Why are radio waves not observed to undergo diffraction when incident on a diffraction',
                             'grating of 600 lines per mm?'),
      [R('d is too small / λ is too big', 4)], 'phys-2-3', 'radio-waves-not-diffracted',
      SQ(14, 'Why are radio waves not observed to undergo diffraction when incident on a diffraction',
         'grating of 600 lines per mm?'), 4, id='phys-2021-hl-q8-ix'),
    # ---------------------------------------------------------------- Q9 --
    T('9i', 'Q9(i)', 'B', P(8, 'What is meant by specific heat capacity?'),
      [R('energy to change temperature of 1 kg of a substance', 3, end='// equation for c', note_sel=LEGEND),
       R('by one kelvin', 3, end='// notation')], 'phys-2-1', 'specific-heat-capacity',
      SQ(15, 'What is meant by specific heat capacity?'), 6, id='phys-2021-hl-q9-i', decision=DOUBLE),
    T('9ii', 'Q9(ii)', 'B', P(8, 'Why does the high specific latent heat of fusion of ice make', 'it a good coolant?'),
      [R('takes in a lot of energy', 3), R('when melting', 3)], 'phys-2-1', 'latent-heat-makes-good-coolant',
      SQ(15, 'Why does the high specific latent heat of fusion of ice make it a good coolant?'), 6, stem=[ICE9],
      id='phys-2021-hl-q9-ii'),
    T('9iii', 'Q9(iii)', 'B', P(8, 'Suggest two reasons why the walls of a picnic box are made', 'rather than solid plastic.'),
      [anyn(S('better insulator, lower heat capacity, lighter, lower environmental impact'), 2, 3, sep=',')], 'phys-2-1', 'hollow-plastic-walls',
      SQ(15, 'Suggest two reasons why the walls of a picnic box are made from hollow plastic rather than',
         'solid plastic.'), 6, stem=[ICE9, SHOWN9], fig='q9-picnic', id='phys-2021-hl-q9-iii'),
    T('9iv', 'Q9(iv)', 'B', P(8, 'Calculate the final temperature inside the picnic box when its contents have reached',
                             'thermal equilibrium.'),
      [R('mc', 3), R('ml', 3), R('(0.25 × 2100', 3), R('= 17800', 3), R('θ = 5.04', 3)], 'phys-2-1',
      'final-temperature-in-picnic-box',
      SQ(15, 'Calculate the final temperature inside the picnic box when its contents have reached',
         'thermal equilibrium.'), 15, stem=[PICNIC9] + DATA9, id='phys-2021-hl-q9-iv'),
    T('9v', 'Q9(v)', 'B', P(8, 'Draw a labelled diagram of a heat pump.'),
      [R('compressor indicated', 3), R('(expansion) valve indicated', 3),
       C('correct arrangement of liquid/vapour indicated', 3)], 'phys-2-1', 'heat-pump-diagram',
      SQ(15, 'Draw a labelled diagram of a heat pump.'), 9, stem=[PUMP9], id='phys-2021-hl-q9-v'),
    T('9vi', 'Q9(vi)', 'B', P(8, 'Explain how a heat pump works.'),
      [R('heat taken in by liquid evaporating', 3), R('heat given out by vapour condensing', 3)], 'phys-2-1',
      'how-a-heat-pump-works', SQ(15, 'Explain how a heat pump works.'), 6, stem=[PUMP9], id='phys-2021-hl-q9-vi'),
    T('9vii', 'Q9(vii)', 'B', P(8, 'What observations did the student make?'),
      [R('ice didn', 4)], 'phys-2-1', 'ice-under-hot-water-observation',
      SQ(15, 'What observations did the student make?'), 4, stem=[APP9], fig='q9-apparatus',
      id='phys-2021-hl-q9-vii-viii-fig', decision=bundled('(vii) and (viii)', '(vii)')),
    T('9viii', 'Q9(viii)', 'B', P(8, 'What conclusion could the student have made?'),
      [R('water is a poor conductor (of heat)', 4)], 'phys-2-1', 'water-poor-conductor',
      SQ(15, 'What conclusion could the student have made?'), 4, stem=[APP9], fig='q9-apparatus'),
    # ---------------------------------------------------------------- Q10 --
    T('10i', 'Q10(i)', 'B', P(9, 'What is a magnetic field?'),
      [R('the region where magnetic forces can be experienced', 3)], 'phys-3-4', 'magnetic-field',
      SQ(16, 'What is a magnetic field?'), 3, stem=[CURRENT10], id='phys-2021-hl-q10-i'),
    T('10ii', 'Q10(ii)', 'B', P(9, 'Describe an experiment to show the magnetic field around the conductor.'),
      items('apparatus, method, observation', 3, kinds=['criterion'] * 3), 'phys-3-4',
      'field-around-conductor-experiment',
      SQ(16, 'Describe an experiment to show the magnetic field around the conductor.'), 9, stem=[CURRENT10],
      decision='The bank had excluded this part. ' + EXPT + ' "(3 × 3)" against the one line: one criterion row per '
               'item, in the scheme\'s words.'),
    T('10iii', 'Q10(iii)', 'B', P(9, 'Draw the shape and direction of this magnetic field.'),
      [C('correct shape', 3), C('correct direction', 3)], 'phys-3-4', 'field-around-straight-conductor',
      SQ(16, 'Draw the shape and direction of this magnetic field.'), 6, stem=[CURRENT10],
      decision='The bank had excluded this part. The scheme prices "correct shape" and "correct direction" and draws '
               'nothing: two criterion rows.'),
    T('10iv', 'Q10(iv)', 'B', P(9, 'The magnitude of this force depends on a number of factors. Name three of them.'),
      [anyn(S('magnetic flux density, current, length, angle'), 3, 2, sep=',')],
      'phys-3-5', 'factors-affecting-force-on-conductor',
      SQ(16, 'The magnitude of this force depends on a number of factors. Name three of them.'), 6, stem=[FORCE10],
      id='phys-2021-hl-q10-iv'),
    T('10v', 'Q10(v)', 'B', P(9, 'Derive an expression for the force F experienced by a charge q travelling with velocity v',
                             'magnetic field of flux density B.'),
      [R('F = BIl', 3), R('I = q/t and l = vt', 3), R('F = qvB', 3)], 'phys-3-5', 'deriving-f-equals-qvb',
      SQ(16, 'Derive an expression for the force F experienced by a charge q travelling with velocity v',
         'magnetic field of flux density B.'), 9, id='phys-2021-hl-q10-v'),
    T('10vi', 'Q10(vi)', 'B', P(9, 'Use Faraday’s law of electromagnetic induction to calculate the average emf induced in the',
                               'loop as it enters the field.'),
      [pt(S('// V = dΦ/dt', piece=2, psep='//'), 3, note_sel=LEGEND),
       R('Φ = BA', 3, route='side-a'), R('t = s/v', 3, route='side-a'),
       pt(S('// V = BA/t', piece=2, psep='//'), 3, route='side-b'), pt(S('// V = Bsv', piece=2, psep='//'), 3,
                                                                      route='side-b'),
       pt(S('// V = 0.12 V', piece=2, psep='//'), 3)],
      'phys-3-6', 'emf-induced-in-square-loop',
      SQ(16, 'Use Faraday’s law of electromagnetic induction to calculate the average emf induced in the',
         'loop as it enters the field.'), 12, stem=[LOOP10], id='phys-2021-hl-q10-vi',
      decision='The scheme prints two methods side by side, separated by "//"; its first line (V = dΦ/dt) and last '
               '(V = 0.12 V) are printed identically on both sides, so they are common rows (lifted from the side '
               'that carries the cell), and the two middle lines of each side are routes inside the card.'),
    T('10vii', 'Q10(vii)', 'B', P(9, 'State Lenz’s law.'),
      [R('the direction of an induced current', 3), R('is such as to oppose the change that caused it', 3)],
      'phys-3-6', 'lenzs-law', SQ(16, 'State Lenz’s law.'), 6, id='phys-2021-hl-q10-vii'),
    T('10viii', 'Q10(viii)', 'B', P(9, 'Explain how Lenz’s law is a special case of the principle of conservation of energy.'),
      [R('otherwise energy would be created', 5)], 'phys-3-6', 'lenz-and-conservation-of-energy',
      SQ(16, 'Explain how Lenz’s law is a special case of the principle of conservation of energy.'), 5,
      id='phys-2021-hl-q10-viii'),
    # ---------------------------------------------------------------- Q11 --
    T('11i', 'Q11(i)', 'B', P(10, 'Write the nuclear equation for this event.'),
      [G('equation', page=17, clip=(80, 224, 215, 249), expect='Be⁹₄ + He⁴₂ → C¹²₆ + n¹₀', marks=11,
         note_sel=SPECIES, note_lead='The scheme prices the equation (11 × 1).')],
      'phys-4-4', 'chadwick-neutron-equation', SQ(17, 'Write the nuclear equation for this event.'), 11,
      stem=[NEUTRON11], fig='q11-photo',
      decision='The bank had excluded this part: the scheme sets the equation in CambriaMath with each nuclide\'s '
               'numbers stacked after its symbol. Read from where each number is printed: one row at the printed '
               '(11 × 1) = 11. (The reader leaves a space between He and its numbers: the span holding helium\'s '
               'atomic number ends in two spaces.)'),
    T('11ii', 'Q11(ii)', 'B', P(10, 'Calculate the increase in kinetic energy during this event.'),
      [R('E = mc²', 3), C('conversion between a.m.u. and kg', 3), C('mass defect calculation', 3),
       R('conversion to J', 3)], 'phys-4-5', 'kinetic-energy-gained',
      SQ(17, 'Calculate the increase in kinetic energy during this event.'), 12, stem=[NEUTRON11], fig='q11-photo',
      id='phys-2021-hl-q11-ii'),
    T('11iii', 'Q11(iii)', 'B', P(10, 'A G', 'What is this function?'),
      [R('to detect (ionising) radiation', 3)], 'phys-4-4', 'function-of-detectors',
      SQ(17, 'A G-M tube and a solid-state detector have the same function. What is this function?'), 3,
      stem=[GEIGER11], id='phys-2021-hl-q11-iii'),
    T('11iv', 'Q11(iv)', 'B', P(10, 'Describe, with the aid of a labelled diagram, the principle of operation of a detector of this',
                               'sort.'),
      [anyn(None, 3, 3, route='side-a', note_sel=LEGEND,
            options=[S('gas / anode'), S('ionisation'), S('current')]),
       anyn(None, 3, 3, route='side-b',
            options=[S('// semiconductor', piece=2, psep='//'), S('// electron-hole pair', piece=2, psep='//'),
                     S('// current', piece=2, psep='//')]),
       anyn(None, 3, 3, route='side-c', note_sel=S('(–1 if no diagram present)'),
            options=[S('// charged gold leaf electroscope', piece=2, psep='//'), S('// ionisation', piece=2, psep='//'),
                     S('// leaves collapse', piece=2, psep='//')])],
      'phys-4-4', 'detector-principle',
      SQ(17, 'Describe, with the aid of a labelled diagram, the principle of operation of a detector of this', 'sort.'),
      9, stem=[GEIGER11, M('(iii)', 10), P(10, 'A G', 'What is this function?')], id='phys-2021-hl-q11-iv',
      decision='The scheme prints three detectors in columns separated by "//" (G-M tube, solid-state detector, '
               'gold leaf electroscope), three lines each at (3). Routes inside the card, one per column; each '
               'column\'s three lines are one menu row of three claims at 3, so the card keeps within six rows.'),
    T('11v', 'Q11(v)', 'B', P(10, 'Describe with the aid of a labelled diagram the gold foil experiment.'),
      [R('alpha source and gold target', 3), R('flashes of light on detector', 3, note_sel=S('(–1 if no diagram present)'))],
      'phys-4-3', 'gold-foil-experiment',
      SQ(17, 'Describe with the aid of a labelled diagram the gold foil experiment.'), 6, stem=[GOLD11],
      id='phys-2021-hl-q11-v'),
    T('11vi', 'Q11(vi)', 'B', P(10, 'What observations were made during the experiment?'),
      [pt(S('most particles went straight through', 'straight back', piece=k, psep=','), 2) for k in (1, 2, 3)],
      'phys-4-3', 'gold-foil-observations', SQ(17, 'What observations were made during the experiment?'), 6,
      stem=[GOLD11], id='phys-2021-hl-q11-vi',
      decision='"(3 × 2)" against one statement of three observations: one row per observation, cut at the scheme\'s '
               'commas.'),
    T('11vii', 'Q11(vii)', 'B', P(10, 'What did Rutherford conclude about the structure of the atom?'),
      [R('mostly empty space with positive nucleus', 3)], 'phys-4-3', 'rutherford-conclusion',
      SQ(17, 'What did Rutherford conclude about the structure of the atom?'), 3, stem=[GOLD11],
      id='phys-2021-hl-q11-vii'),
    T('11viii', 'Q11(viii)', 'B', P(10, 'How did Niels Bohr improve Rutherford’s model to explain emission line spectra?'),
      [R('electrons in energy levels', 3), R('photon emitted when electrons move between energy levels', 3)],
      'phys-4-3', 'bohr-model', SQ(17, 'How did Niels Bohr improve Rutherford’s model to explain emission line spectra?'),
      6, id='phys-2021-hl-q11-viii'),
    # ---------------------------------------------------------------- Q12 --
    T('12i', 'Q12(i)', 'B', P(11, 'Describe a laboratory experiment to demonstrate charging', 'by induction.'),
      [R('charged object', 3), R('charged object brought close to conductor', 3), R('conductor earthed', 3),
       R('earth removed', 3,
         note_sel=S('(last 3 marks not awarded if charged object removed before or at the same time as earth)'))],
      'phys-3-1', 'charging-by-induction',
      SQ(18, 'Describe a laboratory experiment to demonstrate charging by induction.'), 12, id='phys-2021-hl-q12-i'),
    T('12ii', 'Q12(ii)', 'B', P(11, 'Explain how point discharge occurs.'),
      [R('charge accumulates at a point', 3), R('the air around the point is ionised / ions in the air neutralise the point', 3)],
      'phys-3-1', 'point-discharge', SQ(18, 'Explain how point discharge occurs.'), 6, id='phys-2021-hl-q12-ii'),
    T('12iii', 'Q12(iii)', 'B', P(11, 'Calculate the relative permittivity of the capacitor’s dielectric.'),
      [R('C = εA/d', 3), R('ε = 2.4', 3), R('εr = 2.71', 3)], 'phys-3-2', 'relative-permittivity',
      SQ(18, 'Calculate the relative permittivity of the capacitor’s dielectric.'), 9, stem=[CAP12],
      id='phys-2021-hl-q12-iii'),
    T('12iv', 'Q12(iv)', 'B', P(11, 'What would be the effect on the capacitance if the distance between the plates was',
                               'doubled?'),
      [R('decreased by a factor of 2', 3)], 'phys-3-2', 'doubling-plate-separation',
      SQ(18, 'What would be the effect on the capacitance if the distance between the plates was', 'doubled?'), 3,
      stem=[CAP12], id='phys-2021-hl-q12-iv'),
    T('12v', 'Q12(v)', 'B', P(11, 'Three such capacitors are connected in parallel as shown below.', 'is 9.6 pF.'),
      [R('(common) area increases by a factor of 3', 3)], 'phys-3-2', 'capacitors-in-parallel',
      SQ(18, 'Three such capacitors are connected in parallel as shown below. Explain why the effective',
         'is 9.6 pF.'), 3, stem=[CAP12], fig='physics-2021-hl-paper-p011-i0', id='phys-2021-hl-q12-v',
      decision='The card keeps its figure, the paper\'s circuit of three capacitors in parallel (opened and checked).'),
    T('12vi', 'Q12(vi)', 'B', P(11, 'Draw the electric field pattern in a charged parallel plate capacitor.'),
      [R('parallel field lines', 3), R('from +', 3)], 'phys-3-2', 'field-between-plates',
      SQ(18, 'Draw the electric field pattern in a charged parallel plate capacitor.'), 6, id='phys-2021-hl-q12-vi'),
    T('12vii', 'Q12(vii)', 'B', P(11, 'Why is the cathode of an X', 'tube hot?'),
      [R('for thermionic emission to occur / so that electrons will be released', 3)], 'phys-4-2', 'hot-cathode',
      SQ(18, 'Why is the cathode of an X-ray tube hot?'), 3, stem=[XRAY12], id='phys-2021-hl-q12-vii'),
    T('12viii', 'Q12(viii)', 'B', P(11, 'Calculate the maximum speed of an electron as it moves between the cathode and the',
                                   'anode.'),
      [R('½mv² / qV', 3), R('½mv² = qV', 3), R('v = 8.4', 3)], 'phys-4-2', 'speed-of-electron-in-x-ray-tube',
      SQ(18, 'Calculate the maximum speed of an electron as it moves between the cathode and the', 'anode.'), 9,
      stem=[XRAY12], id='phys-2021-hl-q12-viii'),
    T('12ix', 'Q12(ix)', 'B', P(11, 'What happens to the energy of the electrons when they hit the anode?'),
      [anyn(None, 2, 3, steps=[3, 2], note=ORDERED.format(cell='(3 + 2)'),
            options=[S('converted into heat'), S('converted into X')])], 'phys-4-2', 'energy-at-the-anode',
      SQ(18, 'What happens to the energy of the electrons when they hit the anode?'), 5, stem=[XRAY12],
      id='phys-2021-hl-q12-ix',
      decision='"(3 + 2)" against the two conversions, which the scheme prints in no order: a menu priced step by '
               'step.'),
    # ---------------------------------------------------------------- Q13 --
    T('13ai', 'Q13(a)(i)', 'B', P(12, 'State the quark composition of the proton.'),
      [R('up, up, down', 7)], 'phys-4-5', 'quark-composition-of-proton',
      SQ(19, 'State the quark composition of the proton.'), 7, id='phys-2021-hl-q13a-i'),
    T('13aii', 'Q13(a)(ii)', 'B', P(12, 'List the forces experienced by a proton in decreasing order of strength.'),
      items('strong, electromagnetic, weak, gravitational', 1) + [C('order', 3)], 'phys-4-5', 'forces-on-a-proton',
      SQ(19, 'List the forces experienced by a proton in decreasing order of strength.'), 7, id='phys-2021-hl-q13a-ii',
      decision='"(4 × 1)" against the four forces printed on one line: 1 each; then "order (3)", which names what '
               'earns the marks.'),
    T('13aiii', 'Q13(a)(iii)', 'B', P(12, 'The Planck constant relates energy and frequency.', 'kilograms and seconds.'),
      [R('kg m', 7)], 'phys-4-2', 'unit-of-planck-constant',
      SQ(19, 'The Planck constant relates energy and frequency.', 'kilograms and seconds.'), 7,
      id='phys-2021-hl-q13a-iii'),
    T('13aiv', 'Q13(a)(iv)', 'B', P(12, 'Write a nuclear equation for the pair annihilation of a proton and an antiproton.'),
      [G('equation', page=19, clip=(80, 427, 175, 452), expect='p¹₁ + p̅¹₋₁ = 2γ', marks=7,
         note_sel=SPECIES, note_lead='The scheme prices the equation (7 × 1).')],
      'phys-4-5', 'proton-antiproton-annihilation',
      SQ(19, 'Write a nuclear equation for the pair annihilation of a proton and an antiproton.'), 7,
      decision='The bank had excluded this part: the scheme sets the equation in CambriaMath with the numbers '
               'stacked after each symbol and the antiproton\'s bar as a glyph the text layer reads as a Malayalam '
               'letter (GLYPHS reads it as a combining overline). Read from where each number is printed: one row '
               'at the printed (7 × 1) = 7.'),
    T('13av', 'Q13(a)(v)', 'B', P(12, 'A photon produces a muon anti', 'photon in electronvolts.'),
      [R('E = mc²', 3), R('m = 2m', 3), R('m = 2 ×', 3), R('E = 3.388', 3), R('E = 2.115', 2)], 'phys-4-5',
      'muon-pair-production-energy',
      SQ(19, 'A photon produces a muon anti-muon pair. Calculate the minimum energy of the', 'photon in electronvolts.'),
      14, id='phys-2021-hl-q13a-v'),
    T('13avi', 'Q13(a)(vi)', 'B', P(12, 'In the Large Hadron Collider, how are the particles (a) accelerated, (b) maintained in',
                                   'circular motion?'),
      [R('(a) voltage / electric field / magnetic field', 4), R('(b) magnetic field', 3)], 'phys-3-5',
      'particles-in-the-lhc',
      SQ(19, 'In the Large Hadron Collider, how are the particles (a) accelerated, (b) maintained in',
         'circular motion?'), 7, id='phys-2021-hl-q13a-vi',
      decision='One cell "(4 + 3)" prices (a) and (b) of one ask: (a) 4 and (b) 3 in the order printed, each row '
               'with its printed marker.'),
    T('13avii', 'Q13(a)(vii)', 'B', P(12, 'In 1932 Walton and Cockcroft manufactured one of the first useful particle',
                                     'scientific significance.'),
      [anyn(None, 2, 4, steps=[4, 3], note=ORDERED.format(cell='(4 + 3)'),
            options=[S('first experimental verification of E'), S('first transmutation using artificially accelerated')])],
      'phys-4-5', 'walton-cockcroft-significance',
      SQ(19, 'In 1932 Walton and Cockcroft manufactured one of the first useful particle', 'scientific significance.'),
      7, id='phys-2021-hl-q13a-vii',
      decision='"(4 + 3)" against the two reasons, which the scheme prints in no order: a menu priced step by step.'),
    T('13bi', 'Q13(b)(i)', 'B', P(13, 'Explain how a photodiode works.'),
      [R('diode in reverse bias', 3), R('photons absorbed to create an electron-hole pair', 2), R('current flows', 2)],
      'phys-3-3', 'photodiode', SQ(20, 'Explain how a photodiode works.'), 7, id='phys-2021-hl-q13b-i'),
    T('13bii', 'Q13(b)(ii)', 'B', P(13, 'Diodes can be used to make a bridge rectifier.', 'rectifier.', end_nth=2),
      [R('four diodes', 4), C('correct arrangement shown', 3)], 'phys-3-3', 'bridge-rectifier-circuit',
      SQ(20, 'Diodes can be used to make a bridge rectifier. Draw a circuit diagram of a bridge'), 7,
      id='phys-2021-hl-q13b-ii', source_pages=[13], decision=LINKED.format(w='"a circuit diagram"', why=OWN)),
    T('13biii', 'Q13(b)(iii)', 'B', P(13, 'Sketch the input and output voltage patterns for a bridge rectifier.'),
      [R('axes labelled (V and t)', 3), R('a.c. input', 2), R('d.c. output', 2)], 'phys-3-3',
      'bridge-rectifier-voltages', SQ(20, 'Sketch the input and output voltage patterns for a bridge rectifier.'), 7,
      id='phys-2021-hl-q13b-iii'),
    T('13biv', 'Q13(b)(iv)', 'B', P(13, 'Draw the structure of a bi', 'polar transistor.'),
      [anyn(None, 3, 3, steps=[3, 2, 2], note=ORDERED.format(cell='(3 + 2 + 2)'),
            options=[S('n (collector) , p (base), n (emitter)', piece=i, psep=',') for i in (1, 2, 3)])],
      'phys-3-3', 'bipolar-transistor-structure', SQ(20, 'Draw the structure of a bi-polar transistor.'), 7,
      id='phys-2021-hl-q13b-iv',
      decision='"(3 + 2 + 2)" against the three regions printed on one line: a menu priced step by step, the 2024 '
               'Higher convention for the same line.'),
    T('13bv', 'Q13(b)(v)', 'B', P(13, 'Draw a circuit diagram of a voltage amplifier.', 'voltages.'),
      [R('symbol for a transistor', 3), R('source of voltage', 3), R('input voltage between base and emitter', 3),
       R('output voltage across load resistor', 3), R('bias resistor shown in correct position', 2)], 'phys-3-3',
      'voltage-amplifier-circuit',
      SQ(20, 'Draw a circuit diagram of a voltage amplifier. Indicate clearly the input and output', 'voltages.'), 14,
      id='phys-2021-hl-q13b-v', source_pages=[13], decision=LINKED.format(w='"a circuit diagram"', why=OWN)),
    T('13bvi', 'Q13(b)(vi)', 'B', P(13, 'In a voltage amplifier, what is the function of (a) the load resistor, (b) the bias',
                                   'bias resistor?'),
      [R('(a) converts a change in collector current to a large output voltage', 4),
       R('(b) ensures the base-emitter junction is forward biased', 3)], 'phys-3-3', 'load-and-bias-resistors',
      SQ(20, 'In a voltage amplifier, what is the function of (a) the load resistor, (b) the bias resistor?'), 7,
      id='phys-2021-hl-q13b-vi',
      decision='One cell "(4 + 3)" prices (a) and (b) of one ask: (a) 4 and (b) 3 in the order printed, each row '
               'with its printed marker.'),
    T('13bvii', 'Q13(b)(vii)', 'B', P(13, 'A transistor can be used in a circuit to act as a NOT gate.',
                                     'Draw a truth table for a NOT gate.'),
      [R('voltage inverter', 3), R('input 1 : output 0', 2), R('input 0 : output 1', 2)], 'phys-3-3',
      'not-gate-circuit-and-truth-table',
      SQ(20, 'A transistor can be used in a circuit to act as a NOT gate. What is the name of this',
         'Draw a truth table for a NOT gate.'), 7, id='phys-2021-hl-q13b-vii', source_pages=[13],
      decision=LINKED.format(w='"this circuit"', why='it is a circuit the student names, and the paper prints none')),
    # ---------------------------------------------------------------- Q14 --
    T('14ai', 'Q14(a)(i)', 'B', P(14, 'What is simple harmonic motion?'),
      [R('acceleration proportional to displacement / equation and notation', 3)], 'phys-1-3',
      'simple-harmonic-motion', SQ(21, 'What is simple harmonic motion?'), 3, stem=[SPHERE14],
      id='phys-2021-hl-q14a-i'),
    T('14aii', 'Q14(a)(ii)', 'B', P(14, 'Calculate the spring constant.'),
      [R('T = 2π/ω', 3), R('ω = 8.49', 3), R('ω² =', 3), R('k = 2.88', 3)], 'phys-1-3', 'spring-constant-from-period',
      SQ(21, 'Calculate the spring constant.'), 12, stem=[SPHERE14], id='phys-2021-hl-q14a-ii'),
    T('14aiii', 'Q14(a)(iii)', 'B', P(14, 'Calculate the acceleration of the sphere when its displacement is 18 mm from its',
                                     'equilibrium position.'),
      [R('a = ω', 3), R('a = 1.3', 3)], 'phys-1-3', 'acceleration-at-18-mm',
      SQ(21, 'Calculate the acceleration of the sphere when its displacement is 18 mm from its',
         'equilibrium position.'), 6, stem=[SPHERE14], id='phys-2021-hl-q14a-iii'),
    T('14aiv', 'Q14(a)(iv)', 'B', P(14, 'Calculate the mass of the magnet.'),
      [R('mg / kx', 3), R('mg = kx', 2), R('m = 4.4 g', 2)], 'phys-1-3', 'mass-of-magnet',
      SQ(21, 'Calculate the mass of the magnet.'), 7, stem=[SPHERE14, MAGNET14, G14], id='phys-2021-hl-q14a-iv'),
    T('14bi', 'Q14(b)(i)', 'B', P(14, 'What is the Doppler effect?'),
      [R('(apparent) change in frequency', 2), R('due to the relative motion between a source and an observer', 3)],
      'phys-2-7', 'doppler-effect', SQ(22, 'What is the Doppler effect?'), 5, stem=[HYDRO14],
      id='phys-2021-hl-q14b-i'),
    T('14bii', 'Q14(b)(ii)', 'B', P(14, 'Describe how the Doppler effect can be demonstrated in the laboratory.'),
      items('apparatus, method, observation', 3, kinds=['criterion'] * 3), 'phys-2-7', 'demonstrating-doppler-effect',
      SQ(22, 'Describe how the Doppler effect can be demonstrated in the laboratory.'), 9,
      decision='The bank had excluded this part. ' + EXPT + ' "(3 × 3)" against the one line: one criterion row per '
               'item, in the scheme\'s words.'),
    T('14biii', 'Q14(b)(iii)', 'B', P(14, 'Calculate the speed of the source.'),
      [R("f'", 3), C('substitution', 3), R('u = 11.02', 3)], 'phys-2-7', 'speed-of-underwater-source',
      SQ(22, 'Calculate the speed of the source.'), 9, stem=[SOURCE14, C14], id='phys-2021-hl-q14b-iii'),
    T('14biv', 'Q14(b)(iv)', 'B', P(14, 'Draw a ray diagram to show the refraction of a sound wave as it travels from water',
                                   'into air.'),
      [R('wave changing direction as it travels from water to air', 3), R('towards the normal', 2)], 'phys-2-3',
      'refraction-of-sound', SQ(22, 'Draw a ray diagram to show the refraction of a sound wave as it travels from water',
                                'into air.'), 5, stem=[REFR14], id='phys-2021-hl-q14b-iv'),
    T('14ci', 'Q14(c)(i)', 'B', [DESC14, M('(i)', 15), P(15, 'f > fₒ , f is constant and I is increasing,')],
      [R('more electrons emitted', 2), R('with the same energy/speed', 2)], 'phys-4-2', 'increasing-intensity-above-threshold',
      SQ(23, 'f > fₒ , f is constant and I is increasing,'), 4, stem=[PHOTO14], id='phys-2021-hl-q14c-i-iii',
      decision='The old card bundled (i), (ii) and (iii), which the scheme prices apart; it keeps its id for (i).'),
    T('14cii', 'Q14(c)(ii)', 'B', [DESC14, M('(ii)', 15), P(15, 'f > fₒ , f is increasing and I is constant,')],
      [R('same number of electrons emitted', 2), R('but with greater energy/speed', 2)], 'phys-4-2',
      'increasing-frequency-above-threshold', SQ(23, 'f > fₒ , f is increasing and I is constant,'), 4,
      stem=[PHOTO14]),
    T('14ciii', 'Q14(c)(iii)', 'B', [DESC14, M('(iii)', 15), P(15, 'f < fₒ , f is constant and I is increasing.')],
      [R('no electrons emitted', 4)], 'phys-4-2', 'below-threshold-frequency',
      SQ(23, 'f < fₒ , f is constant and I is increasing.'), 4, stem=[PHOTO14]),
    T('14civ', 'Q14(c)(iv)', 'B', P(15, 'Calculate the threshold frequency of the metal.'),
      [R('hf', 3), R('f₀ =', 3)], 'phys-4-2', 'threshold-frequency',
      SQ(23, 'Calculate the threshold frequency of the metal.'), 6, stem=[LIGHT14], id='phys-2021-hl-q14c-iv'),
    T('14cv', 'Q14(c)(v)', 'B', P(15, 'Calculate the maximum speed of the emitted electrons.'),
      [R('hf =', 3), R('c = fλ', 3), R('½mv² = 3.5', 2), R('v = 2.8', 2)], 'phys-4-2', 'maximum-speed-of-photoelectrons',
      SQ(23, 'Calculate the maximum speed of the emitted electrons.'), 10, stem=[LIGHT14], id='phys-2021-hl-q14c-v'),
    T('14di', 'Q14(d)(i)', 'B', P(15, 'The photograph shows the inverted image of', 'virtual?'),
      [R('converging lens', 3), R('object outside f', 3), C('correct rays shown', 3), R('the image is real', 3)],
      'phys-2-3', 'ray-diagram-inverted-image',
      SQ(24, 'The photograph shows the inverted image of a mountain formed in a ball lens.', 'virtual?'), 12,
      stem=BALL14[:1], fig='q14d-photo', id='phys-2021-hl-q14d-i-fig'),
    T('14dii', 'Q14(d)(ii)', 'B', P(15, 'What is meant by critical angle?'),
      [R('angle of incidence (in denser medium)', 3),
       R('such that angle of refraction is 90°', 3, end='/ greater than which total internal reflection occurs')],
      'phys-2-3', 'critical-angle', SQ(24, 'What is meant by critical angle?'), 6, id='phys-2021-hl-q14d-ii'),
    T('14diii', 'Q14(d)(iii)', 'B', P(15, 'Calculate the speed of light in the ball lens.'),
      [R('n = 1/sinC', 2), R('1/sinC', 2), R('c₂ =', 2)], 'phys-2-3', 'speed-of-light-in-ball-lens',
      SQ(24, 'Calculate the speed of light in the ball lens.'), 6, stem=[CRITANGLE14], id='phys-2021-hl-q14d-iii'),
    T('14div', 'Q14(d)(iv)', 'B', P(15, 'Explain why white light is dispersed as it passes through the ball lens.'),
      [R('different colours of light', 2, route='side-a'),
       R('travel at different speeds (in glass) / have different refractive indices', 2, route='side-a'),
       pt(S('(allow for 4 marks', piece=[2, 1], psep=['“', '”']), 4, route='side-b', note_sel=S('(allow for 4 marks'))],
      'phys-2-3', 'dispersion-in-ball-lens',
      SQ(24, 'Explain why white light is dispersed as it passes through the ball lens.'), 4, stem=BALL14,
      id='phys-2021-hl-q14d-iv',
      decision='The scheme prices two lines (2) (2) and then allows "the faces of the lens are not parallel" for the '
               'full 4: that answer is a second route inside the card, its row the quoted words with the scheme\'s '
               'direction as the note.'),
]

ANSWER_VARIANTS = {}
RETAINED = {}
WITHDRAW = {}

FIGURES = {
    # key suffix: (doc, page, rect in PDF points, credit, letters, alt, solution[, masks])
    'q1-table': ('paper', 2, (92, 254, 500, 313), SEC, [], 'Table of the recorded data: l (mm) 300, 400, 500, 600, 700, 800; t (s) 22.0, 25.4, 28.4, 31.1, 33.6, 35.9.', False),
    'q2-table': ('paper', 3, (210, 135, 386, 192), SEC, [], 'Table of the recorded data: u (cm) 20.0, 25.0; v (cm) 31.2, 23.2.', False),
    'q3-table': ('paper', 3, (92, 527, 500, 585), SEC, [], 'Table of the recorded data: f (Hz) 256, 320, 341, 427, 480, 512; T (N) 15, 24, 27, 43, 54, 61.', False),
    'q4-table': ('paper', 4, (92, 104, 500, 161), SEC, [], 'Table of the recorded data: θ (°C) 0, 20, 40, 60, 80, 100; R (Ω) 5.35, 5.60, 5.85, 6.04, 6.28, 6.51.', False),
    'q5-table': ('paper', 4, (92, 491, 500, 549), SEC, [], 'Table of the recorded data: I (A) 1.0, 1.5, 2.0, 2.5, 3.0, 3.5; Δθ (°C) 2.0, 4.6, 8.2, 12.6, 18.3, 25.0.', False),
    'q5-data': ('paper', 4, (92, 491, 500, 671), SEC, [], ('Table of the recorded data: I (A) 1.0, 1.5, 2.0, 2.5, 3.0, 3.5; Δθ (°C) 2.0, 4.6, 8.2, 12.6, 18.3, 25.0; '
                 'below it, the line the paper prints under the question: (specific heat capacity of water = '
                 '4180 J kg⁻¹ K⁻¹).'), False,
                [(92, 551, 500, 651)]),
    'q7-diagram': ('paper', 6, (344, 136, 545, 389), SEC, ['P', 'A', 'B'],
                   ('Diagram: a vertical string hangs from point P down to a sphere B; a block A on the right has an arrow '
                   'pointing left towards B, and a dashed curved arrow leads from B up and away to the left.'), False),
    'q9-picnic': ('paper', 8, (388, 72, 542, 222), 'amazon.co.uk; slideplayer.com (images on page 8)', [],
                  ('Photograph of a grey plastic picnic box with a white rim and a carrying handle, two ice packs standing '
                  'in front of it.'), False),
    'q9-apparatus': ('paper', 8, (130, 460, 440, 692), 'amazon.co.uk; slideplayer.com (images on page 8)', [],
                     ('Diagram: a test tube of water held at an angle, a piece of ice held at its closed lower end by a metal '
                     'weight, and a Bunsen burner heating the tube near the top of the water; labels Water, Metal '
                     'weight, Ice and Bunsen burner.'), False),
    'q11-photo': ('paper', 10, (248, 99, 541, 294), 'sciencesource.com (image on page 10)', [],
                  ('Black-and-white photograph of a group at an outdoor table laid with cups and saucers in front of a '
                  'hedge: five men seated and, behind them, two women in hats and two men standing.'), False),
    'q14d-photo': ('paper', 15, (341, 327, 542, 479), 'paulreiffer.com (image on page 15)', [],
                   ('Black-and-white photograph of a glass ball resting on pebbles at a shoreline with mountains behind; '
                   'the mountains and the sky appear upside down inside the ball.'), False),
}
