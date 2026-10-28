"""Physics 2024 Higher Level — reviewed task ledger, correcting the sitting in place.

Independent visual sweep (2026-10-28), every page rendered and read:
  * The paper (LC021ALP000EV), 16 pages: p1 cover (the 2024 papers were adjusted for disruption
    to learning; "Answer three questions from Section A and five questions from Section B"),
    p2-p4 Section A Questions 1-5 (40 marks each, group marks printed after runs of romans),
    p5-p15 Section B Questions 6-14 (56 marks each), p16 acknowledgements (images on pages 5-15)
    and back cover.
  * The marking scheme, 24 pages: p1 cover, p2 note on published schemes, p3 points to note
    (solidus, double solidus, units, graphs, slips), p4 annotation symbols, p5 Irish-language
    bonus table, p6-p22 Questions 1-14 (each question reprinted in regular type, its answers in
    bold, the mark cells at the right margin), p23 blank, p24 back cover.

Every printed ask is carded at the scheme's own mark boundary: a roman, or a sub-letter inside a
roman where the scheme prices (a) and (b) apart (Q3(ii), Q4(iii), Q7(vii), Q13(i), (iv), (v),
Q14(a)(iv)). Where one cell prices a roman's sub-letters together (Q14(b)(ii) "[4 + 2]") the
roman is one card. Q6 is "Answer any eight of (a)-(l)" (best eight of twelve at 7 each = 56) and
prints (l) as two alternatives joined by "or": both are carded, as ROUTES of the leaf Q6(l). Q9 and
Q10 are letter-major ((a), (b), (c) with romans under them; PART_TOTALS). Q12 is "Answer either
part (a) or part (b)" (two 56s, both carded) and Q14 "Answer any two of (a), (b), (c), (d)" (four
28s, all carded). The paper's group marks inside a letter ((15)/(24) in Q10(a), (15)/(25)/(16) in
Q12(a), (27)/(11)/(18) in Q12(b), (13)/(15) in Q14(b), (14)/(14) in Q14(c), (8)/(20) in Q14(d))
cannot be keyed by GROUP_TOTALS (which reads a letter-major task by its letter) and were checked by
hand: every one adds up.

Maths read from glyph positions: stacked fractions with G('fraction'), the nuclear equations
(Q12(a)(vii), Q12(a)(xi), Q14(b)(i)) with G('equation'). The "//" sides of Q9(a)(iv) and Q12(a)(xi)
are routes inside their cards; Q2(iv)'s two methods (calculation, graph) are answer variants. The scheme's antineutrino in Q12(a)(vii)
is a Cambria glyph (id 3364) whose ToUnicode reads U+0D24, a Malayalam letter: looked at on the
rendered page, it is the bar over the nu, read as U+0305 COMBINING OVERLINE (GLYPHS), as the
bank's glyph map already reads its neighbour U+0D25. Two formulas put a fraction under a root whose
sign the text layer reads as a Sinhala letter (Q4(vi) "f = 1/2l root(T/mu)", Q6(c)
"T = 2 pi root(l/g)"); the reader maps it to the root sign and brackets what the root covers (its
overbar's reach, or the fraction straight after a tall sign). Q9(b)(iv)'s "x" is a Malayalam sign in the text layer (mapped
by the reader); its formula is shown as a crop as well. Q4(iv)'s "values for root-T" sets the root
in the Symbol font's private-use glyph U+F0D6 (SymbolMT glyph 151), read as the root sign by glyph id
(GLYPHS); the line with its table of values is the solution figure.

The sitting was already carded (119 authored cards, 118 shipped). Every task is re-derived from
the PDFs and the existing cards are corrected in place: every id is kept, mapped (`id=`) to the
task it was carding, or withdrawn onto its twin (Q6(h) was carded twice, with and without the
building photograph). The seven asks the bank had excluded (Q1(vi), Q8(ii), Q10(a)(ii), Q11(ii),
Q12(b)(iv), Q13(iii), Q13(vi)) and the four open ones (Q6(a), Q12(a)(vii), Q14(a)(iv), Q14(b)(i))
are carded, with Q3(ii)(b), Q4(iii)(b), Q6(l)'s second alternative and Q13(v)(c), which the old
cards had bundled or left out.
"""
from phys_review_lib import Q, SQ, S, M, G, pt, anyn, T, unprinted, drawn

YEAR, LEVEL = 2024, 'hl'
REVIEWED_AT = '2026-10-28'
BASELINE_COMMIT = '99ec7f0a0d6b243f4d5a1dc9b14a6a958e98095e'

SOURCES = {
    'paper': {'path': 'examiner-reports/physics/papers/2024-hl-paper.pdf', 'fileid': 'LC021ALP000EV.pdf',
              'sha256': '5d9da3b660536b38a60d1494dbf8d83dc6e66ae56e53366d932647cfecc153fc', 'pages': 16},
    'scheme': {'path': 'examiner-reports/physics/schemes/2024-hl.pdf', 'fileid': 'LC021ALP000EV.pdf',
               'sha256': 'df74412e93844119feb44c2770ec71490a57bfb80f360364be854fdc637eee5b', 'pages': 24},
}

PAGE_ROLES = {
    'paper': {1: 'cover', **{p: 'questions' for p in range(2, 16)}, 16: 'acknowledgements-back-cover'},
    'scheme': {1: 'cover', 2: 'note', 3: 'conventions', 4: 'annotations', 5: 'irish-bonus-table',
               **{p: 'marking' for p in range(6, 23)}, 23: 'blank', 24: 'back-cover'},
}

LETTERED = {6, 9, 10, 12, 14}

# Glyphs whose ToUnicode is wrong, each looked at on the rendered page (each id occurs only where
# named): the Cambria antineutrino bar (Q12(a)(vii), p18, glyph 3364, read as U+0D24, a Malayalam
# letter) is the bar over the nu; the SymbolMT radical (Q4(iv), p9, glyph 151, read as the private-use
# U+F0D6) is the root sign of "values for √T" and of the table's "√T" row.
GLYPHS = {'scheme': {'Cambria': {3364: '\u0305'}, 'SymbolMT': {151: '√'}}}

QUESTION_TOTALS = {**{n: 40 for n in range(1, 6)}, **{n: 56 for n in (6, 7, 8, 9, 10, 11, 13)},
                   12: 112,   # either (a) or (b), 56 each: both carded
                   14: 112}   # any two of (a)-(d), 28 each: all four carded
PART_TOTALS = {(9, 'a'): 22, (9, 'b'): 24, (9, 'c'): 10, (10, 'a'): 39, (10, 'b'): 17,
               (12, 'a'): 56, (12, 'b'): 56, **{(14, x): 28 for x in 'abcd'}}
BEST_OF = {6: (8, 7)}
GROUP_TOTALS = {
    (1, ('i', 'ii')): 19, (1, ('iii', 'iv', 'v', 'vi')): 21,
    (2, ('i', 'ii', 'iii')): 24, (2, ('iv', 'v')): 16,
    (3, ('i', 'ii')): 20, (3, ('iii', 'iv', 'v')): 20,
    (4, ('i', 'ii', 'iii')): 17, (4, ('iv', 'v', 'vi')): 23,
    (5, ('i', 'ii', 'iii')): 26, (5, ('iv', 'v')): 14,
    (7, ('i', 'ii', 'iii')): 21, (7, ('iv', 'v', 'vi', 'vii', 'viii')): 35,
    (8, ('i', 'ii', 'iii', 'iv')): 25, (8, ('v', 'vi', 'vii', 'viii', 'ix', 'x')): 31,
    (11, ('i', 'ii', 'iii')): 21, (11, ('iv', 'v')): 15, (11, ('vi', 'vii', 'viii')): 20,
    **{(13, (r,)): t for r, t in (('i', 7), ('ii', 7), ('iii', 7), ('iv', 14), ('v', 14), ('vi', 7))},
}
CHECKSUMS = {}

# Q6(l): "... State two reasons why their experiment was significant. or Draw a diagram to show how a
# galvanometer can be converted into a voltmeter." Two printed alternatives of the one 7-mark part.
ROUTES = {'Q6(l)': ['cockcroft-walton', 'galvanometer']}

SCAN_PAGES = {'paper': range(2, 16)}
SELECTION_SCAN = [
    ('paper', 2, 'the following', 'Q1 "The following data were recorded": a reference to the table.'),
    ('paper', 3, 'the following', 'Q2 "The following data were recorded": a reference to the table.'),
    ('paper', 3, 'the following', 'Q3 "The following data were recorded": a reference to the table.'),
    ('paper', 3, 'or', 'Q3(iv) "Hence, or otherwise": a method, one answer.'),
    ('paper', 4, 'the following', 'Q4 "The following data were recorded": a reference to the table.'),
    ('paper', 4, 'the following', 'Q5 "the following data were recorded": a reference to the table.'),
    ('paper', 4, 'the following', 'Q5 "The following additional data were recorded": a reference to the data.'),
    ('paper', 4, 'both', 'Q5(iv) "both the length and the diameter": both asked, one card (one cell [3 + 3]).'),
    ('paper', 5, 'the following', 'Q6 "Answer any eight of the following parts": best eight of twelve at 7; every '
                                  'part is carded (BEST_OF).'),
    ('paper', 5, 'or', 'Q6(l) "... significant. or Draw a diagram ...": two printed alternatives, each carded '
                       '(ROUTES).'),
    ('paper', 11, 'either', 'Q12 "Answer either part (a) or part (b)": whole-part choice; both parts are carded.'),
    ('paper', 11, 'or', 'Q12, the same choice.'),
    ('paper', 11, 'or', 'Q12(a) lead-in "one or more of the four fundamental forces": description.'),
    ('paper', 13, 'the following', 'Q13 "Read the following passage": a reference to the passage.'),
    ('paper', 13, 'any four', 'Q13(vi) "List any four other parts": the ask itself, one card ([4 x 1] and order).'),
    ('paper', 14, 'any two', 'Q14 "Answer any two of the following parts": every part is carded.'),
    ('paper', 14, 'the following', 'Q14, the same rubric.'),
]
ASK_SCAN_PAGES = {'paper': range(2, 16)}
ASK_EXEMPT = [
    (11, 'When it was observed that momentum did not appear to be conserved',
     'Q12(a) lead-in to (v)-(viii) ("When it was observed ... Pauli proposed ..."): a description, not an ask; '
     'lifted into those cards\' stem.'),
]

SEC = 'State Examinations Commission'
CRIT = 'The scheme prints no answer here, only what earns the marks.'
LEGEND = S('Answers that are separated by a double solidus, //, are answers which are mutually',
           'with a partial answer from the other side.', page=3)
NOLABEL = S('[–1 if no label present on diagram]')
FORCES = S('[–3 for additional/incorrect forces]')
SPECIES = S('[-3 for additional incorrect species]')
EXTR_LINE = S('extrinsic: doped // unequal number of electrons & holes // high conductivity')
EXTR = dict(EXTR_LINE, piece=1, psep='//')
EXTR_LABEL = dict(EXTR_LINE, piece=1, psep=':')
INTR = S('intrinsic: pure', piece=1, psep=':')
ORDERED = ('The scheme prints these items under one sum, {cell}, and names no order: a response earns '
           'the marks step by step.')
DOUBLE = 'Each line printed with its // side: one row per line, as printed.'


def P(page, start, end=None, **kw):
    return Q(page, start, end, **kw)


def R(text, marks, end=None, **kw):
    """A row lifted whole from the task's scheme page."""
    return pt(S(text, end), marks, **kw)


def C(text, marks, end=None, note=CRIT, **kw):
    """A criterion the scheme prices without printing an answer."""
    return pt(S(text, end), marks, kind='criterion', note=note, **kw)


def FR(page, clip, expect, marks, **kw):
    """A formula the scheme sets as a stacked fraction."""
    return G('fraction', page=page, clip=clip, expect=expect, marks=marks, **kw)


def pieces(sel, marks, sep, **kw):
    """One row per entry of a printed list, at the marks its cell prints for it in order."""
    return [pt(dict(sel, piece=i + 1, psep=sep), m, **kw) for i, m in enumerate(marks)]


# ------------------------------------------------------------------ stems --
STEM1 = [P(2, 'A student carried out a laboratory experiment to investigate the relationship between the',
           'associated acceleration.'), P(2, 'The following data were recorded.')]
STEM2 = [P(3, 'In an experiment to measure the focal length f of a converging lens, a student first found an',
           'object distance u.'), P(3, 'The following data were recorded.')]
# Q2's first sentence only: (i) and (v) ask nothing about the recorded distances.
STEM2A = [P(3, 'In an experiment to measure the focal length f of a converging lens, a student first found an',
            'value for the focal length.')]
STEM3 = [P(3, 'A student carried out an experiment to measure the specific latent heat of fusion of ice.'),
         P(3, 'The following data were recorded.', after='specific latent heat of fusion of ice.')]
DATA3 = P(3, 'specific heat capacity of water = 4180 J kg⁻¹ K⁻¹; specific heat capacity of copper = 390 J kg⁻¹ K⁻¹',
          br=True)
ICE = P(3, 'Ice for the experiment was taken from the freezer.', 'was added to the warm water.')
STEM4 = [P(4, 'A student investigated how the fundamental frequency f of a stretched string of length 70 cm',
           'the student varied the tension.'), P(4, 'The following data were recorded.')]
TAB4 = [P(4, 'f (Hz)', '512', br=True), P(4, 'T (N)', '115', br=True)]
STEM5 = [P(4, 'In an experiment to investigate the relationship between current I and potential difference V for a',
           'the following data were recorded.')]
DATA5 = [P(4, 'The student used their results to calculate the resistivity of the copper wire.',
           'additional data were recorded:'),
         P(4, 'length of wire', '= 65 cm', br=True), P(4, 'diameter of wire = 0.32 mm', br=True)]
G6 = P(5, 'acceleration due to gravity = 9.8 m s⁻²', br=True)
STEM7 = [P(6, 'The hammer throw is an athletics event where athletes', 'releasing it.')]
ATHLETE = P(6, 'An athlete rotates a ball of mass 4 kg in a circle of radius 1.25 m.', 'just before it is released.',
            after='(21)')
RELEASE = P(6, 'The velocity of the ball as it is released is at an angle of 36° above the horizontal.',
            'lands 3.79 s later.')
G7 = P(6, 'acceleration due to gravity = 9.8 m s⁻²', br=True)
INCONS = S('An inconsistency arises within the question, all valid alternative calculations & answers are acceptable.')
INCONS_CELLS = ('The note "An inconsistency arises within the question ..." is printed once, at the foot of Q7 (p13 '
                'line 51), after (vii)(b) and (viii): lifting it takes the check over the cells of the parts between. '
                'This part\'s own cells add to its total.')
STEM8 = [P(7, 'A moving-coil loudspeaker is based on the principle that a current-carrying conductor in a',
           'magnetic field experiences a force.')]
SPEAKER = P(7, 'A loudspeaker has three main components as shown in the', 'sound waves of frequency 512 Hz.')
AMP = P(7, 'The amplitude of the vibrations of the cone determines the', 'amplitude of the sound wave produced.')
POWER = P(7, 'A loudspeaker has a power of 80 mW.')
SPEED = P(7, 'speed of sound = 340 m s⁻¹', br=True)
Q8VIII = P(7, 'Calculate the sound intensity for a person standing 7 m from the loudspeaker.')
STEM9A = [P(8, 'The resistance of a semiconductor depends on multiple factors, one of which is temperature.',
            'temperature-dependent semiconductor.')]
STEM9B = [P(8, 'A current of 5 A flows in an electric drill when it is connected to the mains supply.',
            'dissipated as heat.')]
Q9BII = P(8, 'The drill has an electrical resistance of 22 Ω and it runs', 'produced by the drill.')
Q9BIII = P(8, 'Calculate the input power supplied to the drill by the 230 V', 'mains supply.')
STEM9C = [P(8, 'The mains supply is provided to homes at 230 V.', 'in power lines.')]
STEM10A = [P(9, 'Food irradiation is used to delay spoilage and', 'and gamma rays.')]
XRAY = P(9, 'X–rays used for food irradiation have a minimum wavelength of 1.02 × 10⁻¹¹ m.')
COBALT = P(9, 'Cobalt–60 is commonly used to produce gamma rays for food irradiation.', 'average energy of 1.25 MeV.')
STEM10B = [P(9, 'Cobalt–60 is a radioactive isotope.', 'artificially in nuclear fission reactors.')]
STEM11 = [P(10, 'A device that is designed to store energy when it holds a charge is called a capacitor.')]
PLATES = P(10, 'A parallel-plate capacitor with metal plates of area 0.0225 m² are placed 8 mm apart in a vacuum.')
TIMING = P(10, 'Capacitors and resistors can be combined to create timing circuits such as those used to create the',
           'given instant is 0.3 mA.')
STEM12A = [P(11, 'All matter and energy in the universe must abide by one or more of the four fundamental forces of',
             'nature.')]
PAULI = [P(11, 'When it was observed that momentum did not appear to be conserved', 'missing momentum and energy.'),
         P(11, 'Pauli wrote, “I have done something very bad today by proposing a particle',
           'no theorist should ever do”.')]
BARYONS = P(11, 'Neutrons involved in beta-decay are classified as baryons, while electrons and positrons are',
            'classified as leptons.')
STEM12B = [P(12, 'The mains electricity supply in Ireland is a.c. and operates at a frequency of 50 Hz.',
             'require d.c. to operate.')]
Q12BIII = P(12, 'Draw a circuit diagram of a half-wave rectifier that can be used to convert a.c. to d.c..')
INVERTER = P(12, 'A voltage inverter can be used to convert d.c. to a.c..', 'in a voltage inverter circuit.')
CALLAN = P(12, 'The induction coil was invented by Dr Nicolas Callan in 1836.')
PASSAGE = [P(13, 'Read the following passage and answer the accompanying questions.'),
           P(13, 'John Tyndall ranks as one of Ireland’s most successful scientists and',
             'first studies of atmospheric pollution in London.'),
           P(13, 'adapted from: ‘The Ascent of John Tyndall', br=True)]
BLUE = P(13, 'Blue is a primary colour of light.')
PRISM = P(13, 'A prism can be used to show dispersion of light.', 'dispersion of light.')
INDEX = P(13, 'The refractive index of a medium varies for different wavelengths of light.',
          'turned through different angles.')
SPECTRO = P(13, 'Tyndall also did work in the field of spectroscopy.', 'to a lower energy level.')
STEM14A = [P(14, 'Ireland’s Fittest Family is a competition where families compete across a range of different',
             'physics principles in action.')]
SLIDE = P(14, 'A man is competing in a race where participants are', 'above the water.')
G14 = P(14, 'acceleration due to gravity = 9.8 m s⁻²', br=True)
FORCE14 = P(14, 'Draw a force diagram for the man')
RADIUM = P(14, 'Ra–224 is an unstable nucleus of radium.')
LEAD = P(14, 'A sample of Ra–224 decays to form Pb–208, an isotope of lead.')
HALF = P(14, 'Ra–224 has a half-life of 3.6 days.')
OSC = P(15, 'A high-speed electron that strikes the screen of an', 'produces the green light that is seen.')
SPECTROMETER = P(15, 'A spectrometer can be used to measure the wavelength of light.')
GRATING = P(15, 'Green light of wavelength 530 nm is passed through a diffraction grating with', '400 lines per mm.')

TASKS = [
    # ============================================================ Section A ==
    # ---- Q1 force and acceleration ---------------------------------------------
    T('1i', 'Q1(i)', 'A', P(2, 'Draw a labelled diagram of how the apparatus was arranged in this experiment.'),
      [R('trolley', 4), R('applied force', 3), R('ticker timer/light gates', 3, note_sel=NOLABEL)],
      'phys-1-2', 'force-acceleration-apparatus',
      SQ(6, 'Draw a labelled diagram of how the apparatus was arranged in this experiment.'), 10, stem=STEM1[:1],
      id='phys-2024-hl-q1-i'),
    T('1ii', 'Q1(ii)', 'A', P(2, 'Describe how the student determined the acceleration of the body.'),
      [R('calculate initial velocity and final velocity', 3), R('measure distance/time interval between velocities', 3),
       R('use relevant formula', 3)], 'phys-1-2', 'determining-acceleration',
      SQ(6, 'Describe how the student determined the acceleration of the body.'), 9, stem=STEM1[:1],
      id='phys-2024-hl-q1-ii'),
    T('1iii', 'Q1(iii)', 'A', P(2, 'Draw a suitable graph to show the relationship between F and a.'),
      [C('labelled axes', 3), C('points plotted', 3), C('line of best fit', 3)], 'phys-1-2', 'force-acceleration-graph',
      SQ(6, 'Draw a suitable graph to show the relationship between F and a.'), 9, stem=STEM1, fig='q1-table',
      id='phys-2024-hl-q1-iii'),
    T('1iv', 'Q1(iv)', 'A', P(2, 'Explain how your graph verifies the relationship between F and a.'),
      [R('straight line through the origin shows F is proportional to a', 3)], 'phys-1-2',
      'graph-verifies-f-proportional-to-a',
      SQ(6, 'Explain how your graph verifies the relationship between F and a.'), 3, stem=STEM1, fig='q1-table',
      id='phys-2024-hl-q1-iv'),
    T('1v', 'Q1(v)', 'A', P(2, 'Use your graph to calculate the mass that had been accelerated.'),
      [C('slope formula', 3), R('m = 0.71 kg', 2)], 'phys-1-2', 'mass-from-graph',
      SQ(6, 'Use your graph to calculate the mass that had been accelerated.'), 5, stem=STEM1, fig='q1-table',
      id='phys-2024-hl-q1-v'),
    T('1vi', 'Q1(vi)', 'A', P(2, 'Sketch the graph that a student would get if they did not account for the presence of a',
                              'constant frictional force of less than 0.2 N.'),
      [drawn(4, 'The scheme answers with a sketch (shown at the reveal) and prices it [4]; it prints no words '
                'for it.')],
      'phys-1-2', 'graph-with-friction',
      SQ(6, 'Sketch the graph that a student would get if they did not account for the presence of a'), 4,
      stem=STEM1[:1], fig='q1vi-scheme',
      evidence='Paper p2 prints Q1(vi) "Sketch the graph that a student would get if they did not account for the '
               'presence of a constant frictional force of less than 0.2 N." Scheme p6 prints, under the reprint, '
               'a drawn sketch on axes a (m s⁻²) against F (N) and the cell [4], and no words.',
      decision='The bank had excluded this part. The scheme draws its answer and names it in no words: one '
               'drawn row restating the ask at the cell\'s 4, the scheme\'s drawing cropped as the solution figure.'),
    # ---- Q2 focal length of a converging lens ----------------------------------
    T('2i', 'Q2(i)', 'A', P(3, 'Describe how the student found an approximate value for the focal length.'),
      [R('focus the image of a distant object on a screen', 3), R('measure the distance from the screen to the lens', 3)],
      'phys-2-3', 'approximate-focal-length',
      SQ(7, 'Describe how the student found an approximate value for the focal length.'), 6, stem=STEM2A,
      id='phys-2024-hl-q2-i'),
    T('2ii', 'Q2(ii)', 'A', P(3, 'Draw a labelled diagram of the apparatus and clearly identify the distances u and v.'),
      [R('lens', 2), R('object', 2), R('screen', 2), C('u and v shown', 3)], 'phys-2-3', 'lens-apparatus',
      SQ(7, 'Draw a labelled diagram of the apparatus and clearly identify the distances u and v.'), 9,
      stem=STEM2, fig='q2-table', id='phys-2024-hl-q2-ii'),
    T('2iii', 'Q2(iii)', 'A', P(3, 'Describe, with reference to your diagram, how the values for v were determined and',
                                'measured.'),
      [R('move object/lens/screen', 3), R('until a sharp image is formed', 3), R('measure v with a meter stick', 3)],
      'phys-2-3', 'finding-image-distance',
      SQ(7, 'Describe, with reference to your diagram, how the values for v were determined and'), 9,
      stem=STEM2, fig='q2-table', id='phys-2024-hl-q2-iii'),
    T('2iv', 'Q2(iv)', 'A', P(3, 'Calculate the focal length of the lens using all of the data in the table.'),
      [pt(S('1/u + 1/v = 1/f', '// values for 1/u and 1/v', piece=1, psep='//'), 3),
       pt(S('1st calculation of f', '// labelled axes', piece=1, psep='//'), 3, kind='criterion', note=CRIT),
       pt(S('three further calculations for f', '// points and line of best fit', piece=1, psep='//'), 3,
          kind='criterion', note=CRIT),
       pt(S('average for f', '// value for f', piece=1, psep='//'), 3, kind='criterion', note=CRIT)],
      'phys-2-3', 'focal-length-from-data',
      SQ(7, 'Calculate the focal length of the lens using all of the data in the table.'), 12, stem=STEM2,
      fig='q2-table', id='phys-2024-hl-q2-iv',
      decision='The scheme prints two methods split by //, by calculation or by a graph of 1/u against 1/v, each '
               'line priced [3]: each is shown as its own answer set.'),
    T('2v', 'Q2(v)', 'A', P(3, 'The student also completed an experiment to measure the focal length of a concave mirror.',
                            'Why does the arrangement of the apparatus differ in this experiment?'),
      [R('reflection of light', 4)], 'phys-2-3', 'concave-mirror-arrangement',
      SQ(7, 'The student also completed an experiment to measure the focal length of a concave mirror.'), 4,
      stem=STEM2A, id='phys-2024-hl-q2-v'),
    # ---- Q3 specific latent heat of fusion of ice ------------------------------
    T('3i', 'Q3(i)', 'A', P(3, 'Draw a labelled diagram of the apparatus used in this experiment.'),
      [R('ice', 2), R('calorimeter with water', 2), R('balance', 2), R('thermometer', 2, note_sel=NOLABEL)],
      'phys-2-1', 'latent-heat-apparatus', SQ(8, 'Draw a labelled diagram of the apparatus used in this experiment.'), 8,
      stem=STEM3[:1], id='phys-2024-hl-q3-i'),
    T('3iia', 'Q3(ii)(a)', 'A', [ICE, M('(a)', 3), P(3, 'State two steps the student took to prepare the ice taken from the freezer.')],
      [R('crush the ice', 3), R('dry the ice', 3)], 'phys-2-1', 'preparing-the-ice',
      SQ(8, 'State two steps the student took to prepare the ice taken from the freezer.'), 6, stem=STEM3[:1],
      id='phys-2024-hl-q3-ii',
      decision='The scheme prices (a) and (b) apart, each line its own [3]: one card each. The old card bundled them.'),
    T('3iib', 'Q3(ii)(b)', 'A', [M('(b)', 3), P(3, 'Describe the importance of each step.')],
      [R('crush the ice: ensure the ice was at 0 °C / it would melt faster', 3, whole=True),
       R('dry the ice: no additional water added / only ice added', 3, whole=True)], 'phys-2-1',
      'why-prepare-the-ice', SQ(8, 'Describe the importance of each step.'), 6,
      stem=STEM3[:1] + [ICE, M('(a)', 3), P(3, 'State two steps the student took to prepare the ice taken from the freezer.')]),
    T('3iii', 'Q3(iii)', 'A', P(3, 'Use the data in the table to calculate the energy lost by the calorimeter after the ice was',
                                'added.'),
      [R('mc∆θ', 3), R('∆θcal = 9.4 (°C)', 1), R('305 J', 2)], 'phys-2-1', 'energy-lost-by-calorimeter',
      SQ(8, 'Use the data in the table to calculate the energy lost by the calorimeter after the ice was added.'), 6,
      stem=STEM3 + [DATA3], fig='q3-table', id='phys-2024-hl-q3-iii'),
    T('3iv', 'Q3(iv)', 'A', P(3, 'Hence, or otherwise, calculate the specific latent heat of fusion of ice.'),
      pieces(S('mwater = 49.7 (g); mice = 5.6 (g); ∆θice = 17.4 (°C)'), [1, 1, 1], '; ')
      + [R('ml', 3), R('(ml)ice + (mc∆θ)melted ice = (mc∆θ)cal + (mc∆θ)water', 2), R('l = 3.3 × 10⁵ J kg⁻¹', 2)],
      'phys-2-1', 'latent-heat-of-fusion',
      SQ(8, 'Hence, or otherwise, calculate the specific latent heat of fusion of ice.'), 10,
      stem=STEM3 + [M('(iii)', 3), P(3, 'Use the data in the table to calculate the energy lost by the calorimeter after the ice was',
                                     'added.'), DATA3], fig='q3-table', id='phys-2024-hl-q3-iv',
      decision='[1 + 1 + 1] against the three quantities printed on one line: 1 each, in the order printed.'),
    T('3v', 'Q3(v)', 'A', P(3, 'State two properties of a thermometer that would help improve the accuracy of the',
                            'experiment.'),
      [anyn(S('low heat capacity, reacts quickly, measures to at least 2 decimal places'), 2, 2, sep=',')],
      'phys-2-1', 'thermometer-properties',
      SQ(8, 'State two properties of a thermometer that would help improve the accuracy of the experiment.'), 4,
      stem=STEM3[:1], id='phys-2024-hl-q3-v', decision='Two of three printed properties at [2 + 2]: a menu.'),
    # ---- Q4 frequency and tension of a stretched string ------------------------
    T('4i', 'Q4(i)', 'A', P(4, 'Draw a labelled diagram of how the apparatus was arranged in this experiment.'),
      [R('stretched string', 2), R('newtonmeter / weights', 2), R('tuning fork / signal generator', 2),
       anyn(S('meter stick / bridges / paper rider'), 2, 2, note_sel=NOLABEL,
            note='The scheme prints "any two [2 + 2]" against this line.')],
      'phys-2-6', 'sonometer-apparatus',
      SQ(9, 'Draw a labelled diagram of how the apparatus was arranged in this experiment.'), 10, stem=STEM4[:1],
      id='phys-2024-hl-q4-i'),
    T('4ii', 'Q4(ii)', 'A', P(4, 'How did the student determine that resonance had occurred?'),
      [R('paper rider fell off / maximum displacement of the string observed', 3)], 'phys-2-6', 'detecting-resonance',
      SQ(9, 'How did the student determine that resonance had occurred?'), 3, stem=STEM4[:1], id='phys-2024-hl-q4-ii'),
    T('4iiia', 'Q4(iii)(a)', 'A', [P(4, 'Describe how the student determined'), M('(a)', 4), P(4, 'the frequency f,')],
      [R('read from tuning fork/signal generator', 2)], 'phys-2-6', 'determining-frequency',
      SQ(9, 'the frequency f,'), 2, stem=STEM4[:1], id='phys-2024-hl-q4-iii',
      decision='The scheme prices (a) and (b) apart, each its own [2]: one card each. The old card bundled them.'),
    T('4iiib', 'Q4(iii)(b)', 'A', [P(4, 'Describe how the student determined'), M('(b)', 4), P(4, 'the tension T.')],
      [R('read from newtonmeter/weights', 2)], 'phys-2-6', 'determining-tension',
      SQ(9, 'the tension T.'), 2, stem=STEM4[:1]),
    T('4iv', 'Q4(iv)', 'A', P(4, 'Draw a suitable graph to show the relationship between f and T.'),
      [pt(S('values for √T or f²'), 3, kind='criterion',
          note='The scheme prints the values it expects in the table shown in the figure.'),
       C('labelled axes', 3), C('correct points plotted', 3), C('line of best fit', 3)],
      'phys-2-6', 'frequency-tension-graph', SQ(9, 'Draw a suitable graph to show the relationship between f and T.'), 12,
      stem=STEM4 + TAB4, fig='q4iv-scheme', id='phys-2024-hl-q4-iv',
      decision='The scheme prints "values for √T or f²" over a table of the values (its root sign a SymbolMT '
               'glyph read by id, GLYPHS): one criterion row in its words, the line with its table the solution '
               'figure. The data table is lifted into the stem.'),
    T('4v', 'Q4(v)', 'A', P(4, 'State the relationship between f and T.'),
      [R('frequency is proportional to square root of tension', 3)], 'phys-2-6', 'frequency-tension-relationship',
      SQ(9, 'State the relationship between f and T.'), 3, stem=STEM4, fig='q4-table', id='phys-2024-hl-q4-v'),
    T('4vi', 'Q4(vi)', 'A', P(4, 'Use your graph to determine the mass per unit length of the string used in this experiment.'),
      [pt(S('slope formula, f =', piece=1, psep=','), 3, kind='criterion', note=CRIT),
       FR(9, (158, 623.5, 210, 650), 'f = 1/(2l) √(T/μ)', 2),
       R('μ = 2.2 × 10⁻⁴ kg m⁻¹', 3)],
      'phys-2-6', 'mass-per-unit-length', SQ(9, 'Use your graph to determine the mass per unit length of the string'), 8,
      stem=STEM4 + TAB4, id='phys-2024-hl-q4-vi',
      decision='"slope formula, f = 1/2l √(T/μ) [3 + 2]": slope formula 3, the formula 2, in the order printed. '
               'The root sign is a Sinhala letter in the text layer, read as the root sign; the root\'s overbar '
               'marks its reach, so the radicand T/μ is bracketed.'),
    # ---- Q5 resistance and resistivity of copper wire --------------------------
    T('5i', 'Q5(i)', 'A', P(4, 'Draw a circuit diagram for this experiment.'),
      [anyn(S('power supply, copper wire, ammeter, voltmeter'), 3, 1, sep=',',
            note='The scheme prints "[any 3 × 1]" against this line.'),
       R('power supply, copper wire and ammeter in series', 3), R('voltmeter in parallel with copper wire', 3),
       R('means of varying voltage', 3)],
      'phys-3-3', 'ohms-law-circuit', SQ(10, 'Draw a circuit diagram for this experiment.'), 12, stem=STEM5,
      id='phys-2024-hl-q5-i'),
    T('5ii', 'Q5(ii)', 'A', P(4, 'Draw a suitable graph to show the relationship between I and V.'),
      [C('labelled axes', 3), C('correct points plotted', 3), C('line of best fit', 3)], 'phys-3-3',
      'current-voltage-graph', SQ(10, 'Draw a suitable graph to show the relationship between I and V.'), 9,
      stem=STEM5, fig='q5-table', id='phys-2024-hl-q5-ii'),
    T('5iii', 'Q5(iii)', 'A', P(4, 'Use your graph to calculate the resistance R of the copper wire.'),
      [C('slope formula', 3), R('R = 7.03 Ω', 2)], 'phys-3-3', 'resistance-from-graph',
      SQ(10, 'Use your graph to calculate the resistance R of the copper wire.'), 5, stem=STEM5, fig='q5-table',
      id='phys-2024-hl-q5-iii'),
    T('5iv', 'Q5(iv)', 'A', P(4, 'Describe how the student determined both the length and the diameter of the copper wire.'),
      [R('length: meter stick', 3, whole=True), R('diameter: micrometer/digital callipers', 3, whole=True)],
      'phys-3-3', 'measuring-length-and-diameter',
      SQ(10, 'Describe how the student determined both the length and the diameter of the copper wire.'), 6,
      stem=STEM5 + DATA5, id='phys-2024-hl-q5-iv', decision='[3 + 3] against the two lines: 3 each.'),
    T('5v', 'Q5(v)', 'A', P(4, 'Calculate the resistivity of the copper wire.'),
      [FR(10, (80, 518, 113, 545), 'ρ = RA/l', 3), pt(S('ₗ , A = πr²', piece=2, psep=' , '), 2),
       R('ρ = 8.7 × 10⁻⁷ Ω m', 3)],
      'phys-3-3', 'resistivity-of-copper', SQ(10, 'Calculate the resistivity of the copper wire.'), 8,
      stem=STEM5 + DATA5, fig='q5-table', id='phys-2024-hl-q5-v',
      decision='"ρ = RA/l, A = πr² [3 + 2]": the two formulas 3 and 2, in the order printed.'),
    # ============================================================ Section B ==
    # ---- Q6 short questions: best eight of twelve at 7 --------------------------
    T('6a', 'Q6(a)', 'B', [P(5, 'A meter stick is suspended from', 'equilibrium.'),
                           P(5, 'Calculate the mass of the apple.'), G6],
      [R('M = Fd', 3), R('W = mg', 2), R('m = 0.11 kg', 2)], 'phys-1-2', 'mass-of-apple-from-moments',
      SQ(11, 'Calculate the mass of the apple.'), 7, fig='q6a-diagram',
      decision='The bank had left this part open: it is carded with the printed diagram, whose distances and '
               'weights the ask works from.'),
    T('6b', 'Q6(b)', 'B', P(5, 'Explain what is meant by a geostationary orbit and state a use of a satellite in geostationary orbit.'),
      [R('remains in the same position above earth / has a period of 24 hours', 4), C('any use', 3)],
      'phys-1-6', 'geostationary-orbit',
      SQ(11, 'Explain what is meant by a geostationary orbit and state a use of a satellite in geostationary'), 7,
      id='phys-2024-hl-q6-b'),
    T('6c', 'Q6(c)', 'B', [P(5, 'A simple pendulum has a period of 1.24 s. Calculate the length of the pendulum.'), G6],
      [FR(11, (80, 294, 140, 320), 'T = 2π√(l/g)', 4), R('l = 0.38 m', 3)],
      'phys-1-3', 'length-of-pendulum',
      SQ(11, 'A simple pendulum has a period of 1.24 s. Calculate the length of the pendulum.'), 7,
      id='phys-2024-hl-q6-c',
      decision='The scheme sets T = 2π√(l/g) with the root sign as a Sinhala letter in the text layer, drawn tall '
               'with no overbar of its own: the fraction printed straight after it is its radicand.'),
    T('6d', 'Q6(d)', 'B', P(5, 'Conduction and convection are methods of heat transfer.', 'and convection.'),
      [anyn(None, 2, 4, steps=[4, 3], note=ORDERED.format(cell='[4 + 3]'),
            options=[S('conduction is transfer of heat (by vibration) from particle to particle'),
                     S('convection is transfer of heat by means of circulating currents')])],
      'phys-2-1', 'conduction-and-convection',
      SQ(11, 'Conduction and convection are methods of heat transfer. Distinguish between conduction'), 7,
      id='phys-2024-hl-q6-d'),
    T('6e', 'Q6(e)', 'B', P(5, 'Describe an experiment to demonstrate that sound is a wave.'),
      [R('two coherent sound sources', 3), R('movement relative to the sources', 2), R('interference observed', 2)],
      'phys-2-6', 'sound-is-a-wave', SQ(11, 'Describe an experiment to demonstrate that sound is a wave.'), 7,
      id='phys-2024-hl-q6-e'),
    T('6f', 'Q6(f)', 'B', P(5, 'Explain what is meant by a stationary wave.'),
      [R('(superposition of) two waves of the same frequency and amplitude', 4),
       R('maximum amplitude at each point is constant / no net transfer of energy', 3)], 'phys-2-6',
      'stationary-wave', SQ(11, 'Explain what is meant by a stationary wave.'), 7, id='phys-2024-hl-q6-f',
      decision='[4 + 3] against the two lines of one definition: in the order printed.'),
    T('6g', 'Q6(g)', 'B', P(5, 'Define critical angle.'),
      [R('angle of incidence', 4), R('angle of refraction of 90°', 3)], 'phys-2-3', 'critical-angle',
      SQ(11, 'Define critical angle.'), 7, id='phys-2024-hl-q6-g',
      decision='[4 + 3] against the two lines of one definition: in the order printed.'),
    T('6h', 'Q6(h)', 'B', [P(5, 'A lightning conductor can be placed on top of a tall building as shown.'),
                           P(5, 'Explain how a lightning conductor works.')],
      [R('point discharge', 4), R('transfers charge to ground', 3)], 'phys-3-1', 'lightning-conductor',
      SQ(11, 'A lightning conductor can be placed on top of a tall building as shown. Explain how a'), 7,
      fig='q6h-building', id='phys-2024-hl-q6h-fig',
      decision='[4 + 3] against the two lines: in the order printed. Q6(h) was carded twice, with and without the '
               'photograph; this id carries the reviewed task and phys-2024-hl-q6-h is withdrawn onto it.'),
    T('6i', 'Q6(i)', 'B', P(5, 'A current of 6 A passes a point in a circuit.', 'every minute.'),
      [R('q = It', 3), R('q = 360 (C)', 2), R('2.25 × 10²¹ (electrons)', 2)], 'phys-3-3', 'electrons-per-minute',
      SQ(12, 'A current of 6 A passes a point in a circuit. Calculate the number of electrons that pass that'), 7,
      id='phys-2024-hl-q6-i'),
    T('6j', 'Q6(j)', 'B', P(5, 'Calculate the electrostatic force between two protons that are', 'apart in a vacuum.'),
      [FR(12, (80, 195, 145, 226), 'F = 1/(4πε) q₁q₂/d²', 4), R('7.36 N', 3)], 'phys-3-1', 'force-between-protons',
      SQ(12, 'Calculate the electrostatic force between two protons that are 5.6 x 10⁻¹⁵ m apart in a'), 7,
      id='phys-2024-hl-q6-j'),
    T('6k', 'Q6(k)', 'B', [P(5, 'Einstein’s photoelectric law is explained by the equation hf = φ + ½mv².'),
                           P(5, 'Explain what each of the symbols in the equation stands for.')],
      [anyn(None, 5, 2, steps=[2, 2, 1, 1, 1], note=ORDERED.format(cell='[2 + 2 + 1 + 1 + 1]'),
            options=[S('h = Planck constant'), S('f = frequency'), S('φ = work function'), S('m = mass'),
                     S('v = velocity')])],
      'phys-4-2', 'photoelectric-equation-symbols',
      SQ(12, 'Einstein’s photoelectric law is explained by the equation hf = φ + ½mv². Explain what each'), 7,
      id='phys-2024-hl-q6-k'),
    T('6l', 'Q6(l)', 'B', P(5, 'Cockcroft and Walton won a Nobel Prize for their experiment that bombarded a lithium',
                            'State two reasons why their experiment was significant.'),
      [anyn(S('first artificial splitting of nucleus, first transmutation using artificially accelerated particles,',
              'major step in the development of particle accelerators'), 2, 4, steps=[4, 3], sep=',',
            note=ORDERED.format(cell='[4 + 3]'))],
      'phys-4-5', 'cockcroft-walton-significance',
      SQ(12, 'Cockcroft and Walton won a Nobel Prize for their experiment that bombarded a lithium'), 7,
      route='cockcroft-walton', id='phys-2024-hl-q6-l',
      decision='Q6(l) prints two alternatives joined by "or": each is carded at the part\'s 7, as routes of the '
               'one leaf.'),
    T('6l2', 'Q6(l)', 'B', P(5, 'Draw a diagram to show how a galvanometer can be converted into a voltmeter.'),
      [R('galvanometer in series with', 4), R('(large valued) resistor/multiplier', 3)],
      'phys-3-3', 'galvanometer-to-voltmeter',
      SQ(12, 'Draw a diagram to show how a galvanometer can be converted into a voltmeter.'), 7,
      route='galvanometer',
      decision='The second alternative of Q6(l), which the old cards left out. [4 + 3] against the two lines: in '
               'the order printed.'),
    # ---- Q7 the hammer throw ---------------------------------------------------
    T('7i', 'Q7(i)', 'B', P(6, 'Derive the formula to show the relationship', 'uniform circular motion.'),
      [R('θ = s/r', 3, end='ω = θ/t'), C('combination of two formulae', 3), R('v = rω', 3)], 'phys-1-6',
      'deriving-v-equals-r-omega',
      SQ(13, 'Derive the formula to show the relationship between the radius, velocity and angular'), 9, stem=STEM7,
      id='phys-2024-hl-q7-i'),
    T('7ii', 'Q7(ii)', 'B', P(6, 'Explain what is meant by centripetal force.'),
      [R('force towards centre of circle', 3), R('(that keeps) object moving in a circle', 3)], 'phys-1-6',
      'centripetal-force', SQ(13, 'Explain what is meant by centripetal force.'), 6, id='phys-2024-hl-q7-ii'),
    T('7iii', 'Q7(iii)', 'B', P(6, 'Draw a force diagram to show the forces acting', 'just before it is released.'),
      [R('weight down', 3), R('tension towards centre', 3, note_sel=FORCES)], 'phys-1-6', 'forces-on-hammer',
      SQ(13, 'Draw a force diagram to show the forces acting on the ball just before it is released.'), 6,
      stem=STEM7, id='phys-2024-hl-q7-iii'),
    T('7iv', 'Q7(iv)', 'B', P(6, 'Calculate the centripetal force acting on the ball just before it is released.'),
      [R('F = mrω²', 3), R('F = 2332.8 N', 3)], 'phys-1-6', 'centripetal-force-on-ball',
      SQ(13, 'Calculate the centripetal force acting on the ball just before it is released.'), 6, stem=[ATHLETE],
      id='phys-2024-hl-q7-iv'),
    T('7v', 'Q7(v)', 'B', P(6, 'Calculate the magnitude of the velocity of the ball just as it is released.'),
      [R('(v = rω =) 27 m s⁻¹', 3)], 'phys-1-6', 'release-velocity',
      SQ(13, 'Calculate the magnitude of the velocity of the ball just as it is released.'), 3, stem=[ATHLETE],
      id='phys-2024-hl-q7-v'),
    T('7vi', 'Q7(vi)', 'B', P(6, 'With the aid of a labelled diagram, resolve the velocity of the ball into its horizontal and',
                              'vertical components.'),
      [C('diagram showing horizontal and vertical components', 3), R('uₓ = 27 cos 36°', 3), R('uy = 27 sin 36°', 3)],
      'phys-1-1', 'resolving-velocity',
      SQ(13, 'With the aid of a labelled diagram, resolve the velocity of the ball into its horizontal and'), 9,
      stem=[ATHLETE, RELEASE], id='phys-2024-hl-q7-vi'),
    T('7viia', 'Q7(vii)(a)', 'B', [P(6, 'Ignoring air resistance,'), M('(a)', 6),
                                   P(6, 'calculate the maximum height above the ground reached by the ball,')],
      [R('v² = u² + 2as', 3), R('sy = 12.85 (m)', 2), R('(above ground = 12.85 + 1.26 =) 14.11 m', 2, note_sel=INCONS)],
      'phys-1-1', 'maximum-height',
      SQ(13, 'calculate the maximum height above the ground reached by the ball,'), 7, stem=[ATHLETE, RELEASE, G7],
      id='phys-2024-hl-q7-vii-a', cells=INCONS_CELLS,
      decision='The scheme closes Q7 with "An inconsistency arises within the question, all valid alternative '
               'calculations & answers are acceptable.": it is the note on the final answer.'),
    T('7viib', 'Q7(vii)(b)', 'B', [P(6, 'Ignoring air resistance,'), M('(b)', 6),
                                   P(6, 'calculate the horizontal distance travelled by the ball in 3.79 s.')],
      [R('s = ut', 3), R('sₓ = 82.79 m', 2, note_sel=INCONS)], 'phys-1-1', 'horizontal-distance',
      SQ(13, 'calculate the horizontal distance travelled by the ball in 3.79 s.'), 5, stem=[ATHLETE, RELEASE],
      id='phys-2024-hl-q7-vii-b', cells=INCONS_CELLS),
    T('7viii', 'Q7(viii)', 'B', P(6, 'How would air resistance affect the path of the ball?'),
      [R('reduction in the horizontal and vertical distance travelled', 5)], 'phys-1-2', 'effect-of-air-resistance',
      SQ(13, 'How would air resistance affect the path of the ball?'), 5, stem=[RELEASE], id='phys-2024-hl-q7-viii'),
    # ---- Q8 the moving-coil loudspeaker ----------------------------------------
    T('8i', 'Q8(i)', 'B', P(7, 'State two quantities that affect the magnitude of the force on a current-carrying conductor',
                            'in a magnetic field.'),
      [anyn(S('magnetic flux density, current, length of conductor, angle'), 2, 2, sep=',')], 'phys-3-5',
      'factors-affecting-force-on-conductor',
      SQ(14, 'State two quantities that affect the magnitude of the force on a current-carrying conductor'), 4,
      stem=STEM8, id='phys-2024-hl-q8-i', decision='Two of four printed quantities at [2 + 2]: a menu.'),
    T('8ii', 'Q8(ii)', 'B', P(7, 'Describe a laboratory experiment to demonstrate that a current-carrying conductor in a',
                              'magnetic field experiences a force.'),
      [C('apparatus', 3), C('method', 3), C('observation', 3)], 'phys-3-5', 'current-balance-experiment',
      SQ(14, 'Describe a laboratory experiment to demonstrate that a current-carrying conductor in a'), 9, stem=STEM8,
      decision='The bank had excluded this part. The scheme prices "apparatus [3] method [3] observation [3]" and '
               'names only what earns the marks: three criterion rows.'),
    T('8iii', 'Q8(iii)', 'B', P(7, 'Draw a diagram of the magnetic field produced by a current flowing in a long straight wire.'),
      [C('shape', 3), C('direction', 3)], 'phys-3-4', 'field-around-straight-wire',
      SQ(14, 'Draw a diagram of the magnetic field produced by a current flowing in a long straight wire.'), 6,
      id='phys-2024-hl-q8-iii'),
    T('8iv', 'Q8(iv)', 'B', P(7, 'A wire of length 65 cm carrying a current of 3 A experiences a force of 7 mN when placed in',
                              'at right angles to the field.'),
      [R('F = BIl', 3), R('B = 0.0036 T', 3)], 'phys-3-5', 'magnetic-flux-density',
      SQ(14, 'A wire of length 65 cm carrying a current of 3 A experiences a force of 7 mN when placed in'), 6,
      id='phys-2024-hl-q8-iv'),
    T('8v', 'Q8(v)', 'B', P(7, 'What type of wave is sound?'),
      [R('longitudinal / mechanical', 3)], 'phys-2-5', 'type-of-sound-wave', SQ(14, 'What type of wave is sound?'), 3,
      stem=[SPEAKER], fig='q8-loudspeaker', id='phys-2024-hl-q8-v'),
    T('8vi', 'Q8(vi)', 'B', P(7, 'Calculate the wavelength of the sound wave produced.'),
      [R('c = fλ', 3), R('λ = 0.66 m', 3)], 'phys-2-5', 'wavelength-of-sound',
      SQ(14, 'Calculate the wavelength of the sound wave produced.'), 6, stem=[SPEAKER, SPEED], fig='q8-loudspeaker',
      id='phys-2024-hl-q8-vi'),
    T('8vii', 'Q8(vii)', 'B', P(7, 'What musical characteristic is determined by the', 'amplitude of the wave?'),
      [R('loudness/volume', 3)], 'phys-2-5', 'loudness-and-amplitude',
      SQ(14, 'What musical characteristic is determined by the amplitude of the wave?'), 3, stem=[AMP],
      id='phys-2024-hl-q8-vii'),
    T('8viii', 'Q8(viii)', 'B', Q8VIII,
      [R('I = P/A', 3), R('A = 4πr²', 3), R('I = 1.3 × 10⁻⁴ W m⁻²', 3)], 'phys-2-5', 'sound-intensity',
      SQ(14, 'Calculate the sound intensity for a person standing 7 m from the loudspeaker.'), 9, stem=[POWER],
      id='phys-2024-hl-q8-viii'),
    T('8ix', 'Q8(ix)', 'B', P(7, 'This sound intensity is halved for the person when they stand a distance d from the',
                              'Calculate d.'),
      [FR(14, (80, 660, 205, 688), 'I ∝ 1/d² / reference to √2', 3), R('9.9 m', 2)], 'phys-2-5',
      'distance-for-half-intensity',
      SQ(14, 'This sound intensity is halved for the person when they stand a distance d from the'), 5,
      stem=[POWER, M('(viii)', 7), Q8VIII], id='phys-2024-hl-q8-ix'),
    T('8x', 'Q8(x)', 'B', P(7, 'After this, the speaker of power 80 mW is replaced by a speaker of power 20 mW.',
                            'Calculate the decrease in sound intensity level.'),
      [R('reference to 3 dB', 2), R('6 dB', 3)], 'phys-2-5', 'decrease-in-intensity-level',
      SQ(14, 'After this, the speaker of power 80 mW is replaced by a speaker of power 20 mW. Calculate'), 5,
      stem=[POWER, M('(viii)', 7), Q8VIII], id='phys-2024-hl-q8-x'),
    # ---- Q9 semiconductors, Joule's law, transmission --------------------------
    T('9ai', 'Q9(a)(i)', 'B', P(8, 'What is a semiconductor?'),
      [R('material with a resistivity', 3),
       R('between that of a good conductor and a good insulator / that decreases with temperature', 3)],
      'phys-3-3', 'semiconductor', SQ(15, 'What is a semiconductor?'), 6, stem=STEM9A, id='phys-2024-hl-q9-a-i'),
    T('9aii', 'Q9(a)(ii)', 'B', P(8, 'Sketch a graph to show the relationship between temperature', 'for a thermistor.'),
      [C('axes labelled', 3), C('shape', 3)], 'phys-3-3', 'thermistor-graph',
      SQ(15, 'Sketch a graph to show the relationship between temperature and resistance for a'), 6, stem=STEM9A,
      id='phys-2024-hl-q9a-ii'),
    T('9aiii', 'Q9(a)(iii)', 'B', P(8, 'Explain the shape of the graph in terms of the charge carriers', 'in semiconductors.'),
      [R('as temperature increases, the number of electron hole pairs increase', 3), R('resistance decreases', 3)],
      'phys-3-3', 'charge-carriers-and-temperature',
      SQ(15, 'Explain the shape of the graph in terms of the charge carriers in semiconductors.'), 6,
      stem=STEM9A + [M('(ii)', 8), P(8, 'Sketch a graph to show the relationship between temperature', 'for a thermistor.')],
      id='phys-2024-hl-q9-a-iii'),
    T('9aiv', 'Q9(a)(iv)', 'B', P(8, 'Distinguish between intrinsic and extrinsic conduction in semiconductors.'),
      [R('intrinsic: pure', 2, whole=True, route='side-a', note_sel=LEGEND),
       pt(EXTR, 2, route='side-a'),
       pt(S('// equal number of electrons & holes', piece=2, psep='//'), 2, label=INTR, route='side-b'),
       pt(dict(EXTR_LINE, piece=2, psep='//'), 2,
          label=EXTR_LABEL, route='side-b'),
       pt(S('// low conductivity', piece=2, psep='//'), 2, label=INTR, route='side-c'),
       pt(dict(EXTR_LINE, piece=3, psep='//'), 2, label=EXTR_LABEL, route='side-c')],
      'phys-3-3', 'intrinsic-and-extrinsic-conduction',
      SQ(15, 'Distinguish between intrinsic and extrinsic conduction in semiconductors.'), 4, stem=STEM9A,
      id='phys-2024-hl-q9a-iv',
      decision='Each line prints three answers split by // (pure / doped, equal / unequal numbers of electrons '
               'and holes, low / high conductivity), [2] a line: each pairing is a route inside the card (claiming '
               'a row commits to its side), never answer variants whose labels would name the answer before the '
               'reveal.'),
    T('9bi', 'Q9(b)(i)', 'B', P(8, 'State Joule’s law.'),
      [pt(S('power is proportional to', '// P ∝ I²'), 3, note_sel=LEGEND),
       pt(S('the current squared & the resistance', '// notation & reference to constant resistance [3]',
            piece=1, psep=' ['), 3)],
      'phys-3-3', 'joules-law', SQ(15, 'State Joule’s law.'), 6, stem=STEM9B, id='phys-2024-hl-q9-b-i',
      decision=DOUBLE,
      cells='The scheme prints the second line\'s [3] inside the line\'s own text ("// notation & reference to '
            'constant resistance [3]", p15, rendered and looked at), so the reader takes no cell from it: the '
            'printed cells are [3] + [3] = 6. The row is cut at that [3].'),
    T('9bii', 'Q9(b)(ii)', 'B', Q9BII,
      [R('W = I²Rt', 3), R('W = 16 500 J', 3)], 'phys-3-3', 'heat-produced-by-drill',
      SQ(15, 'The drill has an electrical resistance of 22 Ω and it runs for 30 s. Calculate the heat energy'), 6,
      stem=STEM9B, id='phys-2024-hl-q9-b-ii'),
    T('9biii', 'Q9(b)(iii)', 'B', Q9BIII,
      [R('P = VI', 3), R('P = 1150 W', 3)], 'phys-3-3', 'input-power-of-drill',
      SQ(15, 'Calculate the input power supplied to the drill by the 230 V mains supply.'), 6, stem=STEM9B,
      id='phys-2024-hl-q9-b-iii'),
    T('9biv', 'Q9(b)(iv)', 'B', P(8, 'Calculate the percentage efficiency of the drill.'),
      [FR(15, (80, 572, 215, 600), '(Po × 100)/(Pi) or P = W/t', 3), R('52.2 %', 3)], 'phys-3-3',
      'efficiency-of-drill', SQ(15, 'Calculate the percentage efficiency of the drill.'), 6,
      stem=STEM9B + [M('(ii)', 8), Q9BII, M('(iii)', 8), Q9BIII], fig='q9biv-scheme', id='phys-2024-hl-q9b-iv',
      decision='The scheme\'s "×" is a Malayalam sign in the text layer (read by the bank\'s glyph map): the '
               'formula is also shown as a crop of the scheme.'),
    T('9ci', 'Q9(c)(i)', 'B', P(8, 'Explain why high voltages are used in the transmission of', 'electrical energy.'),
      [R('high voltage means low current and therefore less energy/heat loss', 6)], 'phys-3-3',
      'high-voltage-transmission',
      SQ(15, 'Explain why high voltages are used in the transmission of electrical energy.'), 6, stem=STEM9C,
      id='phys-2024-hl-q9-c-i'),
    T('9cii', 'Q9(c)(ii)', 'B', P(8, 'Name a device that is used to reduce the voltage from 300 kV', 'to 230 V.'),
      [R('transformer', 4)], 'phys-3-6', 'reducing-the-voltage',
      SQ(15, 'Name a device that is used to reduce the voltage from 300 kV to 230 V.'), 4, stem=STEM9C,
      id='phys-2024-hl-q9-c-ii'),
    # ---- Q10 food irradiation, fission -----------------------------------------
    T('10ai', 'Q10(a)(i)', 'B', P(9, 'Explain what is meant by ionisation.'),
      [R('loss/gain', 3), R('of an electron', 3)], 'phys-4-4', 'ionisation',
      SQ(16, 'Explain what is meant by ionisation.'), 6, stem=STEM10A, id='phys-2024-hl-q10-a-i'),
    T('10aii', 'Q10(a)(ii)', 'B', P(9, 'Describe a laboratory experiment to', 'nuclear radiation.'),
      [C('apparatus', 3), C('method', 3), C('observation', 3)], 'phys-4-4', 'ionising-ability-experiment',
      SQ(16, 'Describe a laboratory experiment to demonstrate the ionising ability of nuclear radiation.'), 9,
      stem=STEM10A,
      decision='The bank had excluded this part. The scheme prices "apparatus [3] method [3] observation [3]" and '
               'names only what earns the marks: three criterion rows.'),
    T('10aiii', 'Q10(a)(iii)', 'B', P(9, 'Explain how X–rays are produced.'),
      [R('high energy electrons', 3), R('strike a metal target', 3)], 'phys-4-2', 'producing-x-rays',
      SQ(16, 'Explain how X–rays are produced.'), 6, stem=[XRAY], id='phys-2024-hl-q10-a-iii'),
    T('10aiv', 'Q10(a)(iv)', 'B', P(9, 'Calculate the maximum energy of the X–rays used for food irradiation.'),
      [R('c = fλ and E = hf', 3), R('E = 1.95 × 10⁻¹⁴ J', 3)], 'phys-4-2', 'maximum-x-ray-energy',
      SQ(16, 'Calculate the maximum energy of the X–rays used for food irradiation.'), 6, stem=[XRAY],
      id='phys-2024-hl-q10-a-iv'),
    T('10av', 'Q10(a)(v)', 'B', P(9, 'Explain what is meant by gamma rays.'),
      [R('electromagnetic radiation of highest energy / electromagnetic radiation due to the', 6,
         end='radioactive decay of a nucleus')], 'phys-4-4', 'gamma-rays',
      SQ(16, 'Explain what is meant by gamma rays.'), 6, stem=[COBALT], id='phys-2024-hl-q10-a-v'),
    T('10avi', 'Q10(a)(vi)', 'B', P(9, 'How many times bigger is the average energy of the gamma rays than the maximum',
                                    'energy of the X–rays?'),
      [R('1 eV = 1.6 × 10⁻¹⁹ J', 3), R('10.28 times', 3)], 'phys-4-4', 'gamma-to-x-ray-energy-ratio',
      SQ(16, 'How many times bigger is the average energy of the gamma rays than the maximum energy'), 6,
      stem=[XRAY, COBALT], id='phys-2024-hl-q10-a-vi'),
    T('10bi', 'Q10(b)(i)', 'B', P(9, 'What are isotopes?'),
      [R('same atomic number', 3), R('different mass number', 3)], 'phys-4-4', 'isotopes',
      SQ(16, 'What are isotopes?'), 6, stem=STEM10B, id='phys-2024-hl-q10-b-i'),
    T('10bii', 'Q10(b)(ii)', 'B', P(9, 'Explain what is meant by nuclear fission.'),
      [R('breaking up of a large nucleus', 3),
       R('into two similar sized nuclei with the release of energy and neutrons', 3)], 'phys-4-6', 'nuclear-fission',
      SQ(16, 'Explain what is meant by nuclear fission.'), 6, stem=STEM10B, id='phys-2024-hl-q10-b-ii'),
    T('10biii', 'Q10(b)(iii)', 'B', P(9, 'Distinguish between the role of the', 'fission reactor.'),
      [anyn(None, 2, 3, steps=[3, 2], note=ORDERED.format(cell='[3 + 2]'),
            options=[S('moderator: slows the neutrons to allow for fission'),
                     S('control rods: absorbs neutrons to control the rate of fission')])],
      'phys-4-6', 'moderator-and-control-rods',
      SQ(16, 'Distinguish between the role of the moderator and the control rods in a nuclear fission reactor.'), 5,
      stem=STEM10B, id='phys-2024-hl-q10-b-iii'),
    # ---- Q11 capacitors --------------------------------------------------------
    T('11i', 'Q11(i)', 'B', P(10, 'Define capacitance.'),
      [pt(S('charge', '// formula'), 3, note_sel=LEGEND), pt(S('per unit voltage', '// notation'), 3)],
      'phys-3-2', 'capacitance', SQ(17, 'Define capacitance.'), 6, stem=STEM11, id='phys-2024-hl-q11-i',
      decision=DOUBLE),
    T('11ii', 'Q11(ii)', 'B', P(10, 'Describe an experiment to demonstrate that capacitance depends on the common area of',
                                'the plates of a parallel plate capacitor.'),
      [C('apparatus', 3), C('method', 3), C('observation', 3)], 'phys-3-2', 'capacitance-and-area-experiment',
      SQ(17, 'Describe an experiment to demonstrate that capacitance depends on the common area of'), 9, stem=STEM11,
      decision='The bank had excluded this part. The scheme prices "apparatus [3] method [3] observation [3]" and '
               'names only what earns the marks: three criterion rows.'),
    T('11iii', 'Q11(iii)', 'B', P(10, 'Sketch a suitable graph to show the relationship between capacitance C and the common',
                                  'parallel plate capacitor.'),
      [C('axes labelled', 3), C('correct shape', 3)], 'phys-3-2', 'capacitance-area-graph',
      SQ(17, 'Sketch a suitable graph to show the relationship between capacitance C and the common'), 6,
      id='phys-2024-hl-q11-iii'),
    T('11iv', 'Q11(iv)', 'B', P(10, 'A voltage of 3 kV is applied across the plates.', 'stored in the capacitor.'),
      [FR(17, (80, 360, 120, 388), 'C = εA/d', 3), FR(17, (80, 386, 140, 412), 'W = ½ CV²', 3),
       R('W = 1.12 × 10⁻⁴ J', 3)], 'phys-3-2', 'energy-stored-in-capacitor',
      SQ(17, 'A voltage of 3 kV is applied across the plates. Calculate the maximum potential energy stored'), 9,
      stem=[PLATES], id='phys-2024-hl-q11-iv'),
    T('11v', 'Q11(v)', 'B', P(10, 'A material with a relative permittivity of 2 is then inserted to completely fill the space',
                              'by the capacitor?'),
      [R('increases', 3), R('by factor of 2', 3)], 'phys-3-2', 'effect-of-dielectric',
      SQ(17, 'A material with a relative permittivity of 2 is then inserted to completely fill the space between'), 6,
      stem=[PLATES, M('(iv)', 10), P(10, 'A voltage of 3 kV is applied across the plates.', 'stored in the capacitor.')],
      id='phys-2024-hl-q11-v'),
    T('11vi', 'Q11(vi)', 'B', P(10, 'Calculate the potential difference across the resistor at this instant.'),
      [R('V = IR', 3), R('V = 7.5 V', 3)], 'phys-3-3', 'pd-across-resistor',
      SQ(17, 'Calculate the potential difference across the resistor at this instant.'), 6, stem=[TIMING],
      fig='q11-circuit', id='phys-2024-hl-q11-vi'),
    T('11vii', 'Q11(vii)', 'B', P(10, 'Calculate the charge held by the capacitor at this instant.'),
      [R('Vcapacitor = 30 – 7.5 = 22.5 (V)', 2), R('C = q/V', 3), R('q = 1.91 × 10⁻³ C', 3)], 'phys-3-2',
      'charge-on-capacitor', SQ(17, 'Calculate the charge held by the capacitor at this instant.'), 8, stem=[TIMING],
      fig='q11-circuit', id='phys-2024-hl-q11-vii'),
    T('11viii', 'Q11(viii)', 'B', P(10, 'Draw a diagram to show the electric field between the plates of the charged capacitor.',
                                    'charged capacitor.'),
      [C('shape', 3), C('direction', 3)], 'phys-3-2', 'field-between-capacitor-plates',
      SQ(17, 'Draw a diagram to show the electric field between the plates of the charged capacitor.'), 6,
      stem=[TIMING], fig='q11-circuit', id='phys-2024-hl-q11-viii'),
    # ---- Q12 (a) fundamental forces and particles -------------------------------
    T('12ai', 'Q12(a)(i)', 'B', P(11, 'Which force is the weakest of the four forces?'),
      [R('gravitational force', 3)], 'phys-4-4', 'weakest-force',
      SQ(18, 'Which force is the weakest of the four forces?'), 3, stem=STEM12A, id='phys-2024-hl-q12-a-i'),
    T('12aii', 'Q12(a)(ii)', 'B', P(11, 'Which force is responsible for binding the nucleus?'),
      [R('strong force', 3)], 'phys-4-4', 'force-binding-the-nucleus',
      SQ(18, 'Which force is responsible for binding the nucleus?'), 3, stem=STEM12A, id='phys-2024-hl-q12-a-ii'),
    T('12aiii', 'Q12(a)(iii)', 'B', P(11, 'State the two fundamental forces of nature that are based on inverse square laws.'),
      pieces(S('gravitational force, electromagnetic force'), [3, 3], ', '), 'phys-4-4', 'inverse-square-forces',
      SQ(18, 'State the two fundamental forces of nature that are based on inverse square laws.'), 6, stem=STEM12A,
      id='phys-2024-hl-q12-a-iii', decision='[3 + 3] against the two forces printed on one line: 3 each.'),
    T('12aiv', 'Q12(a)(iv)', 'B', P(11, 'Name the fundamental force that allows for beta-decay.'),
      [R('weak force', 3)], 'phys-4-4', 'force-of-beta-decay',
      SQ(18, 'Name the fundamental force that allows for beta-decay.'), 3, stem=STEM12A, id='phys-2024-hl-q12-a-iv'),
    T('12av', 'Q12(a)(v)', 'B', P(11, 'Identify the particle that Pauli proposed.'),
      [R('neutrino', 3)], 'phys-4-4', 'paulis-particle', SQ(18, 'Identify the particle that Pauli proposed.'), 3,
      stem=PAULI, id='phys-2024-hl-q12-a-v'),
    T('12avi', 'Q12(a)(vi)', 'B', P(11, 'Explain why it is difficult to detect this particle.'),
      pieces(S('very small mass, no charge'), [3, 3], ', '), 'phys-4-4', 'detecting-the-neutrino',
      SQ(18, 'Explain why it is difficult to detect this particle.'), 6,
      stem=PAULI + [M('(v)', 11), P(11, 'Identify the particle that Pauli proposed.')], id='phys-2024-hl-q12-a-vi',
      decision='[3 + 3] against the two reasons printed on one line: 3 each.'),
    T('12avii', 'Q12(a)(vii)', 'B', P(11, 'Write an equation to represent the decay of a neutron', 'beta-decay.'),
      [G('equation', page=18, clip=(80, 420, 175, 448), expect='¹₀n → ¹₁p + ⁰₋₁e + ν̅', marks=7, units=[1] * 7,
         note='[7 × 1]: the scheme prices the equation one mark at a time.', note_sel=SPECIES)],
      'phys-4-4', 'beta-decay-of-neutron',
      SQ(18, 'Write an equation to represent the decay of a neutron'), 7, qfig='q12a-vii-question',
      fig='q12a-vii-scheme',
      decision='The bank had left this part open. The paper prints the neutron with its numbers stacked, which the '
               'text layer reads "(n₀ ¹)": the ask is shown as printed. The scheme\'s equation is read from glyph '
               'positions (its antineutrino bar by glyph id, GLYPHS) and shown as a crop.'),
    T('12aviii', 'Q12(a)(viii)', 'B', P(11, 'Calculate the energy released during this beta-decay.'),
      [R('E = mc²', 3), R('change in mass = 1.395 × 10⁻³⁰ (kg)', 3), R('E = 1.25 × 10⁻¹³ J', 3)], 'phys-4-5',
      'energy-released-in-beta-decay', SQ(18, 'Calculate the energy released during this beta-decay.'), 9,
      qfig='q12a-viii-question', id='phys-2024-hl-q12-a-viii',
      decision='"this beta-decay" is the neutron decay of (vii), whose nuclide the text layer cannot read: the ask is '
               'shown as printed, with (vii) above it.'),
    T('12aix', 'Q12(a)(ix)', 'B', P(11, 'State a difference between baryons and leptons.'),
      [R('baryons are composed of smaller particles but leptons are fundamental particles /', 3,
         end='not subject to the strong force')], 'phys-4-4', 'baryons-and-leptons',
      SQ(18, 'State a difference between baryons and leptons.'), 3, stem=[BARYONS], id='phys-2024-hl-q12-a-ix'),
    T('12ax', 'Q12(a)(x)', 'B', P(11, 'Neutrons are neutral baryons. Show how the quark model explains this.'),
      [R('neutron = udd', 4), R('2/3 – 1/3 – 1/3 = 0', 3)], 'phys-4-4', 'quark-model-of-neutron',
      SQ(18, 'Neutrons are neutral baryons. Show how the quark model explains this.'), 7, stem=[BARYONS],
      id='phys-2024-hl-q12-a-x', decision='[4 + 3] against the two lines: in the order printed.'),
    T('12axi', 'Q12(a)(xi)', 'B', P(11, 'Pair annihilation occurs when an electron and a positron meet.',
                                    'represents this process.'),
      [G('equation', page=18, clip=(80, 718, 170, 742), expect='⁰₋₁e + ⁰₁e → 2γ', marks=6, note_sel=LEGEND,
         route='side-a'),
       pt(S('// 2mc² = 2hf', piece=2, psep='//'), 6, route='side-b')],
      'phys-4-5', 'pair-annihilation-equation',
      SQ(18, 'Pair annihilation occurs when an electron and a positron meet. Write an equation that'), 6,
      fig='q12a-xi-scheme', id='phys-2024-hl-q12a-xi',
      decision='The scheme prints the equation "// 2mc² = 2hf", one [6]: two mutually exclusive answers, each a '
               'route inside the card. The equation is read from glyph positions and shown as a crop of the scheme.'),
    # ---- Q12 (b) a.c., d.c. and the induction coil ------------------------------
    T('12bi', 'Q12(b)(i)', 'B', P(12, 'Distinguish between a.c. and d.c..'),
      [R('a.c. changes direction', 3), R('d.c. travels in one direction', 3)], 'phys-3-3', 'ac-and-dc',
      SQ(19, 'Distinguish between a.c. and d.c..'), 6, stem=STEM12B, id='phys-2024-hl-q12-b-i'),
    T('12bii', 'Q12(b)(ii)', 'B', P(12, 'Draw a voltage–time graph for an a.c. supply and a d.c. supply.'),
      [C('labelled axes', 3), C('a.c. shown', 3), C('d.c. shown', 3)], 'phys-3-3', 'ac-and-dc-graphs',
      SQ(19, 'Draw a voltage–time graph for an a.c. supply and a d.c. supply.'), 9, stem=STEM12B,
      id='phys-2024-hl-q12b-ii'),
    T('12biii', 'Q12(b)(iii)', 'B', Q12BIII,
      [R('diode', 3), C('input and output voltage labelled', 3), C('arrangement', 3)], 'phys-3-3',
      'half-wave-rectifier', SQ(19, 'Draw a circuit diagram of a half-wave rectifier that can be used to convert a.c. to d.c..'),
      9, stem=STEM12B, id='phys-2024-hl-q12b-iii'),
    T('12biv', 'Q12(b)(iv)', 'B', P(12, 'Sketch the graph of the output voltage of this circuit.'),
      [C('shape', 3)], 'phys-3-3', 'rectified-output-voltage',
      SQ(19, 'Sketch the graph of the output voltage of this circuit.'), 3, stem=[M('(iii)', 12), Q12BIII],
      decision='The bank had excluded this part. The scheme prices "shape [3]" and names only what earns the marks: '
               'one criterion row.'),
    T('12bv', 'Q12(b)(v)', 'B', P(12, 'Draw a labelled diagram of the structure of a', 'bi-polar transistor.'),
      [anyn(None, 3, 3, steps=[3, 2, 2], note=ORDERED.format(cell='[3 + 2 + 2]'),
            options=[S('n (collector), p (base), n (emitter)', piece=i, psep=', ') for i in (1, 2, 3)])],
      'phys-3-3', 'bipolar-transistor-structure',
      SQ(19, 'Draw a labelled diagram of the structure of a bi-polar transistor.'), 7, stem=[INVERTER],
      id='phys-2024-hl-q12b-v'),
    T('12bvi', 'Q12(b)(vi)', 'B', P(12, 'Draw a truth table for a NOT gate.'),
      [R('input 1 : output 0', 2), R('input 0 : output 1', 2)], 'phys-3-3', 'not-gate-truth-table',
      SQ(19, 'Draw a truth table for a NOT gate.'), 4, stem=[INVERTER], id='phys-2024-hl-q12b-vi'),
    T('12bvii', 'Q12(b)(vii)', 'B', P(12, 'Draw a labelled diagram showing the main components', 'of an induction coil.'),
      [R('coil and d.c power supply in primary circuit', 3), R('coil with more turns in secondary circuit', 3),
       R('labelled make and break mechanism and iron core', 3)], 'phys-3-6', 'induction-coil-diagram',
      SQ(19, 'Draw a labelled diagram showing the main components of an induction coil.'), 9, stem=[CALLAN],
      id='phys-2024-hl-q12b-vii'),
    T('12bviii', 'Q12(b)(viii)', 'B', P(12, 'Describe how an induction coil can be used to produce a', 'large d.c. voltage.'),
      [R('primary coil switches off', 3), R('changing magnetic field cutting secondary coil', 3),
       R('emf induced in secondary coil', 3)], 'phys-3-6', 'induction-coil-operation',
      SQ(19, 'Describe how an induction coil can be used to produce a large d.c. voltage.'), 9, stem=[CALLAN],
      id='phys-2024-hl-q12-b-viii'),
    # ---- Q13 John Tyndall --------------------------------------------------------
    T('13ia', 'Q13(i)(a)', 'B', [BLUE, M('(a)', 13), P(13, 'Name the two other primary colours of light.')],
      pieces(S('red, green'), [2, 2], ', '), 'phys-2-4', 'primary-colours',
      SQ(20, 'Name the two other primary colours of light.'), 4, stem=PASSAGE, id='phys-2024-hl-q13-i-a',
      decision='[2 + 2] against the two colours printed on one line: 2 each.'),
    T('13ib', 'Q13(i)(b)', 'B', [M('(b)', 13), P(13, 'Name the secondary colour produced by these two primary colours.')],
      [R('yellow', 3)], 'phys-2-4', 'secondary-colour',
      SQ(20, 'Name the secondary colour produced by these two primary colours.'), 3,
      stem=[BLUE, M('(a)', 13), P(13, 'Name the two other primary colours of light.')], id='phys-2024-hl-q13-i-b'),
    T('13ii', 'Q13(ii)', 'B', P(13, 'A prism can be used to show dispersion of light. What is meant by dispersion of light?'),
      [R('splitting of light', 4), R('into its different colours', 3)], 'phys-2-3', 'dispersion',
      SQ(20, 'What is meant by dispersion of light?'), 7, id='phys-2024-hl-q13-ii'),
    T('13iii', 'Q13(iii)', 'B', P(13, 'Name two other items that can cause dispersion of light.'),
      [C('two items', 7, units=[4, 3], note=CRIT + ' It prices the two items [4 + 3].')], 'phys-2-3',
      'causes-of-dispersion', SQ(20, 'Name two other items that can cause dispersion of light.'), 7, stem=[PRISM],
      decision='The bank had excluded this part. The scheme prints "two items [4 + 3]" and names none: one '
               'criterion row in its words at the cell\'s 7.'),
    T('13iva', 'Q13(iv)(a)', 'B', [INDEX, M('(a)', 13), P(13, 'Explain what is meant by refractive index.')],
      [pt(S('ratio of sine of the angle of incidence', '// formula'), 3, note_sel=LEGEND),
       pt(S('to sine of the angle of refraction', '// notation'), 3)], 'phys-2-3', 'refractive-index',
      SQ(20, 'Explain what is meant by refractive index.'), 6, id='phys-2024-hl-q13-iv-a', decision=DOUBLE),
    T('13ivb', 'Q13(iv)(b)', 'B', [M('(b)', 13),
                                   P(13, 'The refractive index of a block of glass for red light is 1.51 and for violet light is 1.53.',
                                     'light as they travel through the block of glass.')],
      [FR(20, (110, 455, 150, 482), 'n = c₁/c₂', 3)]
      + pieces(S('cred = 1.985 × 10⁸ (m s⁻¹) , cviolet = 1.959× 10⁸ (m s⁻¹)'), [2, 1], ' , ')
      + [R('difference = 2.6 × 10⁶ m s⁻¹', 2)], 'phys-2-3', 'speeds-of-red-and-violet-light',
      SQ(20, 'The refractive index of a block of glass for red light is 1.51 and for violet light is 1.53.'), 8,
      stem=[INDEX], id='phys-2024-hl-q13-iv-b',
      decision='[2 + 1] against the two speeds printed on one line: in the order printed.'),
    T('13va', 'Q13(v)(a)', 'B', [SPECTRO, M('(a)', 13), P(13, 'Calculate the energy of the lower energy level.')],
      [R('E₂ – E₁ = hf', 3), R('1.67 × 10⁻¹⁹ J', 3)], 'phys-4-3', 'lower-energy-level',
      SQ(20, 'Calculate the energy of the lower energy level.'), 6, id='phys-2024-hl-q13-v-a'),
    T('13vb', 'Q13(v)(b)', 'B', [M('(b)', 13), P(13, 'Distinguish between a line emission spectrum and a continuous emission spectrum.')],
      [R('line spectra: contain gaps / contain specific wavelengths and continuous spectra: no', 5,
         end='gaps / contain all wavelengths', whole=True)], 'phys-4-3', 'line-and-continuous-spectra',
      SQ(20, 'Distinguish between a line emission spectrum and a continuous emission spectrum.'), 5, stem=[SPECTRO],
      id='phys-2024-hl-q13-v-b'),
    T('13vc', 'Q13(v)(c)', 'B', [M('(c)', 13), P(13, 'State one use of spectroscopy as a tool in science.')],
      [C('one use', 3)], 'phys-4-3', 'uses-of-spectroscopy',
      SQ(20, 'State one use of spectroscopy as a tool in science.'), 3, stem=[SPECTRO],
      decision='The old cards carded (v)(a) and (b) and left (c) out.'),
    T('13vi', 'Q13(vi)', 'B', P(13, 'Infrared radiation is part of the electromagnetic spectrum.',
                                'in order of increasing frequency.'),
      [C('any 4 named', 4, units=[1, 1, 1, 1], note=CRIT + ' It prices them [4 × 1].'), C('order', 3)],
      'phys-2-4', 'electromagnetic-spectrum-order',
      SQ(20, 'Infrared radiation is part of the electromagnetic spectrum. List any four other parts of the'), 7,
      stem=PASSAGE,
      decision='The bank had excluded this part. The scheme prices "any 4 named [4 × 1]" and "order [3]" and names '
               'no part of the spectrum: two criterion rows in its words.'),
    # ---- Q14 (a) Ireland's Fittest Family -----------------------------------------
    T('14ai', 'Q14(a)(i)', 'B', P(14, 'State the law of conservation of energy.'),
      [R('energy cannot be created or destroyed', 4, kind='point')], 'phys-1-4', 'conservation-of-energy',
      SQ(21, 'State the law of conservation of energy.'), 4, stem=STEM14A, id='phys-2024-hl-q14-a-i'),
    T('14aii', 'Q14(a)(ii)', 'B', P(14, 'Calculate the height of the platform above the', 'surface of the water.'),
      [R('slide height = 2.4 sin 32° (= 1.27 m)', 3), R('total height = 1.27 + 0.9 = 2.17 m', 3)], 'phys-1-4',
      'height-of-platform', SQ(21, 'Calculate the height of the platform above the surface of the water.'), 6,
      stem=[SLIDE], fig='q14a-slide', id='phys-2024-hl-q14-a-ii'),
    T('14aiii', 'Q14(a)(iii)', 'B', [P(14, 'The man starts from rest. Calculate his velocity', 'as he enters the water.'),
                                     P(14, 'Assume that there is no friction on the slide.')],
      [R('mgh = ½mv²', 3), R('v = 6.52 m s⁻¹', 3)], 'phys-1-4', 'velocity-entering-water',
      SQ(21, 'The man starts from rest. Calculate his velocity as he enters the water.'), 6, stem=[SLIDE, G14],
      fig='q14a-slide', id='phys-2024-hl-q14-a-iii'),
    T('14aiva', 'Q14(a)(iv)(a)', 'B', [FORCE14, M('(a)', 14), P(14, 'as he slides down the slide,')],
      [R('weight down', 3), R('normal reaction perpendicular to surface', 3, note_sel=FORCES)], 'phys-1-2',
      'forces-on-the-sliding-man', SQ(21, 'as he slides down the slide,'), 6, stem=[SLIDE], fig='q14a-slide',
      cells='The note "[–3 for additional/incorrect forces]" is printed once, after (b)\'s rows (p21 line 29), and '
            'serves (a) and (b): lifting it takes the check over (b)\'s two [3] cells. (a)\'s own cells are '
            '[3] + [3] = 6.',
      decision='The bank had left (iv) open. The scheme prices (a) and (b) apart, [3] a line: one card each.'),
    T('14aivb', 'Q14(a)(iv)(b)', 'B', [FORCE14, M('(b)', 14), P(14, 'when he is floating in the water.')],
      [R('weight down', 3), R('upward force equal in size', 3, note_sel=FORCES)], 'phys-1-2',
      'forces-on-the-floating-man', SQ(21, 'when he is floating in the water.'), 6, stem=[SLIDE]),
    # ---- Q14 (b) radium-224 ----------------------------------------------------------
    T('14bi', 'Q14(b)(i)', 'B', P(14, 'Ra–224 decays by releasing an alpha-particle. Write a nuclear equation for this decay.'),
      [G('equation', page=21, clip=(80, 465, 200, 490), expect='²²⁴₈₈Ra → ⁴₂He + ²²⁰₈₆Rn', marks=7, units=[1] * 7,
         note='[7 × 1]: the scheme prices the equation one mark at a time.', note_sel=SPECIES)],
      'phys-4-4', 'alpha-decay-of-radium',
      SQ(21, 'Ra–224 decays by releasing an alpha-particle. Write a nuclear equation for this decay.'), 7,
      stem=[RADIUM], fig='q14bi-scheme',
      decision='The bank had left this part open. The equation is read from glyph positions and the scheme\'s print '
               'of it is the solution figure.'),
    T('14bii', 'Q14(b)(ii)', 'B', [LEAD, M('(a)', 14), P(14, 'How many alpha-particles are released?'), M('(b)', 14),
                                   P(14, 'How many beta-particles are released?')],
      [R('4', 4, label=S('(a)')), R('2', 2, label=S('(b)'))], 'phys-4-4', 'alpha-and-beta-particles-released',
      SQ(21, 'A sample of Ra–224 decays to form Pb–208, an isotope of lead.'), 6, stem=[RADIUM],
      id='phys-2024-hl-q14-b-ii',
      decision='One cell [4 + 2] prices (a) and (b) together: one card, (a) 4 and (b) 2 in the order printed.'),
    T('14biii', 'Q14(b)(iii)', 'B', P(14, 'Explain what is meant by the term half-life.'),
      [R('the time taken', 3), R('for half of the nuclei to decay', 3, note_sel=S('[-1 for incorrect reference to atoms]'))],
      'phys-4-4', 'half-life', SQ(21, 'Explain what is meant by the term half-life.'), 6, stem=[HALF],
      id='phys-2024-hl-q14-b-iii'),
    T('14biv', 'Q14(b)(iv)', 'B', P(14, 'Calculate the total number of alpha-particles emitted per second by a sample of',
                                    'atoms.'),
      [FR(21, (80, 705, 125, 733), 'T½ = ln2/λ', 3), R('A = λN', 3), R('A = 1.05 × 10⁹ (Bq)', 3)], 'phys-4-4',
      'activity-of-radium-sample',
      SQ(21, 'Calculate the total number of alpha-particles emitted per second by a sample of Ra–224'), 9,
      stem=[HALF], id='phys-2024-hl-q14-b-iv'),
    # ---- Q14 (c) thermionic emission ----------------------------------------------
    T('14ci', 'Q14(c)(i)', 'B', P(15, 'What is meant by thermionic emission?'),
      [R('emission of electrons', 3), R('from the surface of a hot metal', 3)], 'phys-4-1', 'thermionic-emission',
      SQ(22, 'What is meant by thermionic emission?'), 6, id='phys-2024-hl-q14-c-i'),
    T('14cii', 'Q14(c)(ii)', 'B', P(15, 'Draw a labelled diagram of a cathode ray tube.'),
      [R('heating coil', 2), R('voltage across cathode and anode', 2), R('labelled vacuum', 2), C('one other detail', 2)],
      'phys-4-1', 'cathode-ray-tube', SQ(22, 'Draw a labelled diagram of a cathode ray tube.'), 8,
      id='phys-2024-hl-q14c-ii'),
    T('14ciii', 'Q14(c)(iii)', 'B', P(15, 'Calculate the minimum voltage required', 'of 2.7 × 10⁷ m s⁻¹.'),
      [R('Eₖ = ½mv² or W = qV', 3), R('qV = ½mv²', 3), R('V = 2072 V', 3)], 'phys-4-1', 'accelerating-voltage',
      SQ(22, 'Calculate the minimum voltage required across the tube to give an electron a velocity of'), 9,
      stem=[OSC], id='phys-2024-hl-q14-c-iii'),
    T('14civ', 'Q14(c)(iv)', 'B', P(15, 'How does the photoelectric effect differ', 'from thermionic emission?'),
      [R('(energy needed) to release the electron is provided by light', 5)], 'phys-4-2',
      'photoelectric-and-thermionic', SQ(22, 'How does the photoelectric effect differ from thermionic emission?'), 5,
      id='phys-2024-hl-q14-c-iv'),
    # ---- Q14 (d) the spectrometer ------------------------------------------------
    T('14di', 'Q14(d)(i)', 'B', P(15, 'Draw a labelled diagram of a spectrometer.'),
      pieces(S('labelled collimator, table, telescope, other detail'), [2, 2, 2], ', ', kind='point')
      + [pt(S('labelled collimator, table, telescope, other detail', piece=4, psep=', '), 2, kind='criterion', note=CRIT)],
      'phys-2-6', 'spectrometer-diagram', SQ(22, 'Draw a labelled diagram of a spectrometer.'), 8,
      stem=[SPECTROMETER], id='phys-2024-hl-q14d-i',
      decision='[2 + 2 + 2 + 2] against the four items printed on one line: 2 each.'),
    T('14dii', 'Q14(d)(ii)', 'B', P(15, 'Calculate the angle of separation', 'between the second order images.'),
      [FR(22, (80, 497, 200, 523), 'd = 1/(number of lines per metre)', 3), R('nλ =dsinθ', 3), R('θ = 25.1', 3),
       R('angle of separation = 50.2°', 3)], 'phys-2-6', 'angle-of-separation',
      SQ(22, 'Calculate the angle of separation between the second order images.'), 12, stem=[GRATING],
      fig='q14d-grating', id='phys-2024-hl-q14-d-ii'),
    T('14diii', 'Q14(d)(iii)', 'B', P(15, 'Identify a different colour of light that', 'angle of separation.'),
      [R('red / orange / yellow', 4)], 'phys-2-6', 'colour-for-greater-angle',
      SQ(22, 'Identify a different colour of light that could be used to produce a greater angle of'), 4,
      stem=[GRATING], fig='q14d-grating', id='phys-2024-hl-q14-d-iii'),
    T('14div', 'Q14(d)(iv)', 'B', P(15, 'Explain how the number of lines per mm', 'of separation.'),
      [R('increased number of lines per mm means increased angle', 4)], 'phys-2-6', 'lines-per-mm-and-angle',
      SQ(22, 'Explain how the number of lines per mm on a diffraction grating affects the angle of'), 4,
      stem=[GRATING], fig='q14d-grating', id='phys-2024-hl-q14-d-iv'),
]

ANSWER_VARIANTS = {
    '2iv': [
        ('calculation', 'By calculation',
         [pt(S('1/u + 1/v = 1/f', '// values for 1/u and 1/v', piece=1, psep='//'), 3),
          pt(S('1st calculation of f', '// labelled axes', piece=1, psep='//'), 3, kind='criterion', note=CRIT),
          pt(S('three further calculations for f', '// points and line of best fit', piece=1, psep='//'), 3,
             kind='criterion', note=CRIT),
          pt(S('average for f', '// value for f', piece=1, psep='//'), 3, kind='criterion', note=CRIT)]),
        ('graph', 'By a graph',
         [pt(S('1/u + 1/v = 1/f', '// values for 1/u and 1/v', piece=2, psep='//'), 3, kind='criterion', note=CRIT),
          pt(S('1st calculation of f', '// labelled axes', piece=2, psep='//'), 3, kind='criterion', note=CRIT),
          pt(S('three further calculations for f', '// points and line of best fit', piece=2, psep='//'), 3,
             kind='criterion', note=CRIT),
          pt(S('average for f', '// value for f', piece=2, psep='//'), 3, kind='criterion', note=CRIT)]),
    ],
}

RETAINED = {
    'phys-2024-hl-q6-h': 'Never shipped: the figureless twin of phys-2024-hl-q6h-fig, which carries the reviewed '
                         'task and the building photograph.',
}
WITHDRAW = {'phys-2024-hl-q6-h': ('phys-2024-hl-q6h-fig', RETAINED['phys-2024-hl-q6-h'])}

P5 = 'State Examinations Commission; sarthaks.com (images on page 5)'

FIGURES = {
    # key suffix: (doc, page, rect in PDF points, credit, letters, alt, solution)
    'q1-table': ('paper', 2, (52, 238, 545, 310), SEC, [],
                 'Table of the recorded data: F (N) 0.2, 0.3, 0.4, 0.5, 0.6, 0.7; a (m s⁻²) 0.280, 0.422, 0.554, '
                 '0.702, 0.837, 0.982.', False),
    'q1vi-scheme': ('scheme', 6, (82, 576, 300, 650), SEC, [],
                    "The marking scheme's sketch: axes labelled a (m s⁻²) and F (N), with a straight line rising from "
                    "a point on the F axis to the right of the origin.", True),
    'q2-table': ('paper', 3, (52, 130, 545, 190), SEC, [],
                 'Table of the recorded data: u (cm) 20.0, 30.0, 40.0, 50.0; v (cm) 78.7, 35.2, 26.9, 23.4.', False),
    'q3-table': ('paper', 3, (52, 402, 545, 528), SEC, [],
                 'Table of the recorded data: mass of copper calorimeter 83.2 g; mass of calorimeter + water before '
                 'adding ice 132.9 g, after adding ice 138.5 g; temperature of water before adding ice 26.8 °C, after '
                 'adding ice 17.4 °C.', False),
    'q4-table': ('paper', 4, (52, 134, 545, 194), SEC, [],
                 'Table of the recorded data: f (Hz) 256, 320, 341, 426.5, 480, 512; T (N) 29, 44, 51, 79, 100, 115.',
                 False),
    'q4iv-scheme': ('scheme', 9, (82, 452, 545, 512), SEC, [],
                    "The marking scheme's line \"values for √T or f²\" [3] over its table of values: f² 65536, 102400, "
                    "116281, 181902, 230400, 262144; √T 5.39, 6.63, 7.14, 8.89, 10.00, 10.72.", True),
    'q5-table': ('paper', 4, (52, 449, 545, 510), SEC, [],
                 'Table of the recorded data: V (V) 1.0, 2.0, 3.0, 4.0, 5.0, 6.0; I (A) 0.14, 0.26, 0.43, 0.58, 0.70, '
                 '0.84.', False),
    'q6a-diagram': ('paper', 5, (262, 185, 545, 275), P5, [],
                    'Diagram of a metre stick hung at its 50 cm mark from a horizontal support: a 0.6 N weight hangs '
                    'at the 10 cm mark, a 1.3 N weight at the 35 cm mark, and an apple at the 90 cm mark.', False),
    'q6h-building': ('paper', 5, (474, 395, 543, 586), P5, [],
                     'Drawing of a tall rectangular building with rows of windows; a rod with a pointed tip stands on '
                     'its roof and a conductor runs from it down the outside of the building to the ground.', False),
    'q8-loudspeaker': ('paper', 7, (372, 266, 545, 450), 'explainthatstuff.com', [],
                       'Cutaway diagram of a moving-coil loudspeaker: a block labelled permanent magnet, a coil wound '
                       'around its centre with two leads and arrows out to the left, and a flared cone labelled cone, '
                       'with curved lines in front of it labelled cone vibrations.', False),
    'q9biv-scheme': ('scheme', 15, (82, 572, 215, 600), SEC, [],
                     "The marking scheme's formula: Po × 100 over Pi, set as a fraction, or P = W/t.", True),
    'q11-circuit': ('paper', 10, (150, 430, 445, 648), SEC, [],
                    'Circuit diagram: a 30 V supply of cells across the top, and along the bottom a capacitor '
                    'labelled 85 µF in series with a resistor labelled 25 kΩ.', False),
    'q12a-vii-question': ('paper', 11, (52, 345, 400, 381), SEC, [],
                          'The printed question: (vii) Write an equation to represent the decay of a neutron (n, '
                          'with mass number 1 above and atomic number 0 below) by beta-decay.', False),
    'q12a-viii-question': ('paper', 11, (52, 345, 440, 401), SEC, [],
                           'The printed questions: (vii) Write an equation to represent the decay of a neutron (n, '
                           'with mass number 1 above and atomic number 0 below) by beta-decay. (viii) Calculate the '
                           'energy released during this beta-decay.', False),
    'q12a-vii-scheme': ('scheme', 18, (82, 420, 172, 448), SEC, [],
                        "The marking scheme's equation: a neutron (1 above, 0 below the n) gives a proton (1 above, 1 "
                        "below the p) plus an electron (0 above, -1 below the e) plus an antineutrino (a nu with a bar "
                        "over it).", True),
    'q12a-xi-scheme': ('scheme', 18, (82, 720.5, 300, 742), SEC, [],
                       "The marking scheme's answer: an electron (0 above, -1 below the e) plus a positron (0 above, 1 "
                       "below the e) gives 2γ, and beside it, after a double solidus, 2mc² = 2hf.", True),
    'q14a-slide': ('paper', 14, (360, 278, 545, 392), SEC, [],
                   'Diagram of the slide: a horizontal platform at the top left, a straight slide running down to the '
                   'right at 32° below the dashed horizontal from the platform, and a vertical line from the end of the '
                   'slide down to the water.', False),
    'q14bi-scheme': ('scheme', 21, (82, 465, 188, 490), SEC, [],
                     "The marking scheme's equation: radium (224 above, 88 below the Ra) gives helium (4 above, 2 "
                     "below the He) plus radon (220 above, 86 below the Rn).", True),
    'q14d-grating': ('paper', 15, (338, 382, 545, 556), SEC, [],
                     'Diagram: a ray of light strikes a diffraction grating; two lines spread from the grating to a '
                     'white screen, and the angle between them is labelled angle of separation.', False),
}
