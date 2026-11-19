"""Physics 2023 Higher Level — reviewed task ledger, correcting the sitting in place.

Independent visual sweep (2026-10-28), every page rendered and read:
  * The paper (LC021ALP000EV), 16 pages: p1 cover (the 2023 papers were
    adjusted for disruption to learning), p2-p4 Section A Questions 1-5 (any
    three, 40 marks each), p5-p15 Section B Questions 6-14 (any five, 56 marks
    each), p15 also the acknowledgements (images on pages 5-12, 14, 15), p16
    back cover.
  * The marking scheme, 28 pages: p1 cover, p2 note on published schemes, p3
    marking conventions (solidus, double solidus), p4 annotations, p5 Irish
    bonus table, p6-p25 Questions 1-14, p26 blank (footer only), p27 blank,
    p28 back cover.

Every printed ask is carded. Section A and most of Section B print a group mark
after a run of romans ("(18)" closing Q1(i)-(iii)): GROUP_TOTALS. Q6 is any
eight of (a)-(l) at 7 each (8 x 7): one card per letter. Q12 is either (a) or
(b) and Q14 any two of (a)-(d): every part is carded. A part whose sub-asks the
scheme prices in cells of their own (Q3(v)(a)-(c), Q7(iv)(a)-(b), Q8(iii) and
(iv) (a)-(c), Q12(a)(iv) and (ix), Q12(b)(i), Q13(i) and (iv)) is carded per
sub-ask; one cell over several ("[4 + 3]" for Q13(ii)) keeps the part whole.
Q4's census leaves (ii)-(v) are the inline asks "How did the student (ii) cool
the water, (iii) dry the steam?" and "Why did the student (iv) ..., (v) ...?":
each card's question is that printed line cut at its own marker.

The scheme sets Q7(ii), Q7(iii) and the plutonium nuclide of Q9(i) in
CambriaMath whose ToUnicode map gives several glyphs one character (glyph 2204
v, 2203 u and 2195 m all read "m"; 2183 a reads "k"; the bold digits 2779-2786
read "9" and "2"): GLYPHS sets each by the glyph id, every one checked against
the rendered page. Stacked fractions are read with G('fraction').

The sitting was already carded (110 authored cards, all shipped). Every task is
re-derived from the PDFs at the scheme's own mark boundaries and every shipped
id is kept, mapped (`id=`) to the task it was carding. The six asks the bank had
excluded (Q8(ii), Q10(ii), Q11(iv), Q12(b)(iii), Q13(iii), Q14(d)(ii)) and the
three open ones (Q7(ii)-(iv)) are carded: the "describe an experiment" parts
with the scheme's own criteria (apparatus, method, observation).
"""
from phys_review_lib import Q, SQ, S, M, G, pt, anyn, T, L

YEAR, LEVEL = 2023, 'hl'
REVIEWED_AT = '2026-10-28'
BASELINE_COMMIT = '99ec7f0a0d6b243f4d5a1dc9b14a6a958e98095e'

SOURCES = {
    'paper': {'path': 'examiner-reports/physics/papers/2023-hl-paper.pdf', 'fileid': 'LC021ALP000EV.pdf',
              'sha256': 'aabc53d82a590d2c96556ee256a80f130cea2c2fea7b2b0bbae3f67065dab2a1', 'pages': 16},
    'scheme': {'path': 'examiner-reports/physics/schemes/2023-hl.pdf', 'fileid': 'LC021ALP000EV.pdf',
               'sha256': '9f610bf3f7ce51bdd7ad7b438cd0d5e92ee9cbd6aa10c3f961b081528aac8020', 'pages': 28},
}

PAGE_ROLES = {
    'paper': {1: 'cover', **{p: 'questions' for p in range(2, 15)}, 15: 'questions-acknowledgements',
              16: 'back-cover'},
    'scheme': {1: 'cover', 2: 'note', 3: 'conventions', 4: 'annotations', 5: 'irish-bonus',
               **{p: 'marking' for p in range(6, 26)}, 26: 'blank', 27: 'blank', 28: 'back-cover'},
}

LETTERED = {6, 12, 14}

# Glyph-id corrections for the scheme's CambriaMath (phys_review_lib._page_dict),
# each glyph found with get_texttrace and read on the rendered page.
GLYPHS = {'scheme': {'CambriaMath': {
    2162: 'F',   # p13 Q7(ii), (iii): the F of "F ∝", "F ="
    2193: 'k',   # p13 Q7(ii): the k of "F = k(mv – mu)/t" and "F = kma"
    2195: 'm',   # p13 Q7(ii), (iii): the m of mv, mu, kma (rawdict hands it back as "k" in "kma")
    2202: 't',   # p13 Q7(ii), (iii): the denominator t
    2203: 'u',   # p13 Q7(ii), (iii): the u of mu; p15 Q9(i): the u of Pu (both read "m")
    2204: 'v',   # p13 Q7(ii), (iii): the v of mv (reads "m")
    2183: 'a',   # p13 Q7(ii): the a of "F = kma" (reads "k")
    2172: 'P',   # p15 Q9(i): the P of Pu; p23 Q14(b)(v): the P of "I ∝ P"
    2165: 'I',   # p23 Q14(b)(v): the I of "I ∝ P"
    2779: '2',   # p15 Q9(i): mass number 238, first digit (reads "2")
    2780: '3',   # p15 Q9(i): mass number 238, second digit (reads "2")
    2785: '8',   # p15 Q9(i): mass number 238, third digit (reads "2")
    2786: '9',   # p15 Q9(i): atomic number 94, first digit (reads "9")
    2781: '4',   # p15 Q9(i): atomic number 94, second digit (reads "9")
}}}
# Lines set in the doubled maths font, lifted as text after reading them on the rendered page.
VERIFIED_LINES = [
    ('scheme', 13, 'F= kma'),
    ('scheme', 23, 'reference to 3 dB / doubling / I ∝P'),
]

QUESTION_TOTALS = {**{n: 40 for n in range(1, 6)}, **{n: 56 for n in (6, 7, 8, 9, 10, 11, 13)},
                   12: 112,   # either (a) or (b), 56 each: both carded
                   14: 112}   # any two of (a)-(d), 28 each: all four carded
PART_TOTALS = {(12, 'a'): 56, (12, 'b'): 56, **{(14, x): 28 for x in 'abcd'}}
BEST_OF = {6: (8, 7)}
GROUP_TOTALS = {
    (1, ('i', 'ii', 'iii')): 18, (1, ('iv', 'v')): 18, (1, ('vi',)): 4,
    (2, ('i', 'ii')): 12, (2, ('iii', 'iv', 'v')): 28,
    (3, ('i', 'ii')): 15, (3, ('iii', 'iv')): 15, (3, ('v',)): 10,
    (4, ('i', 'ii', 'iii', 'iv', 'v')): 24, (4, ('vi',)): 16,
    (5, ('i', 'ii')): 21, (5, ('iii',)): 6, (5, ('iv', 'v')): 13,
    (7, ('i', 'ii', 'iii')): 24, (7, ('iv', 'v', 'vi')): 24, (7, ('vii',)): 8,
    (8, ('i', 'ii')): 15, (8, ('iii', 'iv')): 24, (8, ('v', 'vi', 'vii')): 17,
    (9, ('i', 'ii')): 23, (9, ('iii', 'iv')): 12, (9, ('v', 'vi', 'vii')): 21,
    (10, ('i', 'ii')): 18, (10, ('iii', 'iv', 'v')): 21, (10, ('vi', 'vii')): 17,
    (11, ('i',)): 12, (11, ('ii', 'iii', 'iv')): 21, (11, ('v', 'vi', 'vii')): 23,
    **{(13, (r,)): t for r, t in (('i', 14), ('ii', 7), ('iii', 7), ('iv', 14), ('v', 7), ('vi', 7))},
}
CHECKSUMS = {}

SCAN_PAGES = {'paper': range(2, 16)}
SELECTION_SCAN = [
    ('paper', 2, 'the following', 'Q1 "The following data were recorded": a reference to the table.'),
    ('paper', 3, 'the following', 'Q2 "The following data were recorded": a reference to the table.'),
    ('paper', 4, 'the following', 'Q4 "The following data were recorded": a reference to the table.'),
    ('paper', 4, 'the following', 'Q5 "The following data were recorded": a reference to the table.'),
    ('paper', 5, 'the following', 'Q6 "Answer any eight of the following parts": a best-eight of (a)-(l) at 7 '
                                  'each (8 x 7); every part is carded.'),
    ('paper', 7, 'the following', 'Q8(iii) "For each of the following pairs of variables": three graphs, each '
                                  'priced on its own; one card each.'),
    ('paper', 7, 'the following', 'Q8(iv) "For each of the following variables": three effects, each priced on '
                                  'its own; one card each.'),
    ('paper', 10, 'either', 'Q11(iv) "demonstrate either one of these laws": the scheme prices one experiment '
                            '(apparatus, method, observation) for whichever law is chosen: one card.'),
    ('paper', 11, 'either', 'Q12 "Answer either part (a) or part (b)": whole-part choice; both parts are carded.'),
    ('paper', 11, 'or', 'Q12, the same choice.'),
    ('paper', 11, 'or', 'Q12(a)(viii) "baryons or mesons": the ask\'s own wording, not a choice.'),
    ('paper', 12, 'the following', 'Q13 "Read the following passage": a reference to the passage.'),
    ('paper', 14, 'any two', 'Q14 "Answer any two of the following parts": whole-part choice; every part is carded.'),
    ('paper', 14, 'the following', 'Q14, the same rubric.'),
    ('paper', 14, 'both', 'Q14(b) lead-in "can measure both the sound intensity and ...": description.'),
]
ASK_SCAN_PAGES = {'paper': range(2, 16)}
ASK_EXEMPT = [
    (8, 'generators. When the spacecraft were launched', 'Q9 lead-in ("When the spacecraft were launched, each '
                                                       'generator contained ..."): a description, not an ask; lifted '
                                                       'into the stems.'),
    (14, 'A spring has a natural length of 15.0 cm. When a block', 'Q14(a) lead-in to (ii) and (iii): a description, '
                                                               'not an ask; lifted into their stems.'),
    (15, 'State Examinations Commission; learn.sparkfun.com', 'Acknowledgements: an image credit, not an ask.'),
    (15, 'State Examinations Commission', 'Acknowledgements: an image credit, not an ask.'),
]

ROUTES = {}
SEC = 'State Examinations Commission'

CRIT = 'The scheme prints no answer here, only what earns the marks.'
NOLABEL = S('[–1 if no label present on diagram]')
LEGEND = S('Answers that are separated by a double solidus, //, are answers which are mutually',
           'with a partial answer from the other side.', page=3)
EXPT = 'A "describe an experiment" part: the scheme prices apparatus, method and observation and prints no answer.'


LINKED = ('{w} reads to the figure-pointer check as a printed figure; the ask is the student\'s own, so the card '
          'links its exam page.')


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


def bundled(parts, keep):
    return f'The old card bundled {parts}, which the scheme prices apart; it keeps its id for {keep}.'


# ------------------------------------------------------------------ stems --
STEM1 = [P(2, 'In an experiment to determine the acceleration due to gravity g', 'of s.'),
         P(2, 'The following data were recorded.')]
TABLE1 = P(2, 's (cm)', '43')
STEM2 = [P(3, 'In an experiment to determine the focal length f of a concave mirror', 'object distances u.')]
DATA2 = P(3, 'The following data were recorded.')
STEM3 = [P(3, 'In an experiment to determine the wavelength of monochromatic red light', 'apart.')]
STEM4 = [P(4, 'In an experiment to determine the specific latent heat of vaporisation of water', 'water.')]
DATA4 = P(4, 'The following data were recorded.')
SHC4 = P(4, 'specific heat capacity of water = 4180')
HOW4 = 'How did the student (ii) cool the water, (iii) dry the steam?'
WHY4 = 'Why did the student (iv) cool the water, (v) dry the steam?'
STEM5 = [P(4, 'A student investigated the variation of current I with potential difference V for a semiconductor',
           'diode in forward bias.'), P(4, 'The following data were recorded.', nth=2)]
TABLE5 = P(4, 'V (V)', '220')
REVERSE = P(4, 'The student then investigated the variation of current I with potential difference V for a diode in',
            'made to the circuit.')
G6 = P(5, 'acceleration due to gravity = 9.8 m s⁻²')
GOLF = P(6, 'A force of 6.8 kN is applied to a golf ball at rest by the head of a golf club.', 'of 0.51 ms.')
Q7III = [M('(iii)', 6), P(6, 'Calculate the velocity of the ball immediately after impact.')]
ANGLE = P(6, 'The velocity of the ball immediately after impact is at an angle of 15° to the horizontal.')
WIND = P(6, 'A wind blows as the ball travels through the air.', 'north.')
G7 = P(6, 'acceleration due to gravity = 9.8 m s⁻²')
GUITAR = P(7, 'The strings of a guitar can be plucked so that they vibrate at certain', 'vibrate due to resonance.')
STRING = P(7, 'The frequency f of a stretched string depends on its length l, tension T and',
           'linear density (mass per unit length) µ.')
GRAPHS8 = P(7, 'For each of the following pairs of variables, sketch a suitable graph to show the relationship',
            'between them.')
EFFECT8 = P(7, 'For each of the following variables, state the effect on the frequency f if the variable is',
            'increased by a factor of four.')
HARM = P(7, 'A string is stretched between two fixed points which are 62 cm apart.', 'is 380 m s⁻¹.')
STEM9 = [P(8, 'Voyager I and Voyager II are spacecraft that were launched in 1977 to', 'outer planets of our solar system.'),
         P(8, 'The spacecraft are powered with radioisotope thermoelectric', 'kg.')]
Q9I = [M('(i)', 8), P(8, 'Write a nuclear equation for the alpha decay of plutonium–238.')]
THERMO = P(8, 'The energy released by the decay is converted into electrical energy in thermocouples.')
HALF = P(8, 'Plutonium–238 has a half')
VOY = P(8, 'The Voyager spacecraft are now beyond our solar system', 'velocities.')
STEM10 = [P(9, 'The Van de Graaff generator is named after the American physicist Robert J.', 'rays.'),
          P(9, 'In a Van de Graaff generator, point discharge is used to move charge on to a',
            'belt at the lower comb in the generator.')]
DOME = P(9, 'The dome of a Van de Graaff generator has a diameter of 32 cm.', 'charge of +200 nC.')
XRAY = P(9, 'A voltage of 70 kV is applied across an X')
STEM11 = P(10, 'Metal detectors are used in treasure hunting and in airport security.',
           'supplied with an alternating current.')
LAWS = P(10, 'The magnitude and direction of an induced emf are determined by', 'electromagnetic induction.')
COIL = [P(10, 'A circular coil of 500 turns and radius 6.0 cm enters a magnetic field moving with a constant',
          'perpendicular to the field.'), P(10, 'The resistance of the coil is 2.3 Ω')]
ANTI = P(11, 'Anti', 'per gram.')
POS = P(11, 'A positron is an example of anti')
Q12AIII = [M('(iii)', 11), P(11, 'Write an equation to show the pair production of an electron')]
LHC = P(11, 'In the Large Hadron Collider researchers are investigating the pair annihilation of a proton', 'pair.')
LEDS = P(11, 'Light emitting diodes and bridge rectifiers are examples of diodes in use.')
RELAY = P(11, 'Electromagnetic relays are sometimes used with transistors.')
PUMPED = P(12, '• Pumped storage: e.g. Turlough Hill', 'attached to electric generators along the way.')
PASSAGE = [P(12, 'The electric power grid operates based on a delicate balance between supply and demand.',
             'periods of low production and high demand.'),
           P(12, 'Energy can be stored in a variety of ways, including:'), PUMPED,
           P(12, '• Flywheels: electricity is used to accelerate', 'kinetic energy.'),
           P(12, '• Batteries: similar to common rechargeable batteries', 'electricity.', end_nth=1),
           P(12, 'Adapted from:')]
DATA13 = P(13, 'acceleration due to gravity = 9.8 m s⁻²; density of water')
RES13 = [P(13, 'Assume that the upper reservoir in Turlough Hill is full.'), P(13, 'Calculate')]
FLY = [P(13, 'A flywheel of diameter 1.4 m rotates with 5000 revolutions per minute.'), P(13, 'Calculate', nth=2)]
HOOKE = P(14, 'In 1660 Robert Hooke investigated the elasticity of materials, including springs.',
          'His work led to Hooke’s law.')
SPRING = P(14, 'A spring has a natural length of 15.0 cm.', 'released and begins to oscillate.')
G14 = P(14, 'acceleration due to gravity = 9.8 m s⁻²')
BOYLE = P(14, 'In 1665 Hooke, working as an assistant to Robert Boyle', 'led to Boyle’s law.')
SPEAKER = P(14, 'A speaker emits a sound of fixed frequency.', 'frequency emitted.')
SOUND = P(14, 'speed of sound in air = 340 m s⁻¹')
POWER = P(14, 'A fixed speaker of power P is emitting sound.', 'speaker.', end_nth=1)
WIRE = P(15, 'A metal wire has length l, resistance R and cross')
ZINC = P(15, 'Electrons of maximum velocity 0.023c are emitted', 'work function of 4.3 eV.')

TASKS = [
    # ============================================================ Section A ==
    # ---------------------------------------------------------------- Q1 --
    T('1i', 'Q1(i)', 'A', P(2, 'Draw a labelled diagram of the apparatus used in the experiment.'),
      [anyn(S('object, release mechanism, pressure plate/trapdoor, means of measuring distance/time'), 3, 3, sep=',',
            note_sel=NOLABEL, note='The scheme prints "[any three correct items merit 3 × 3]".')],
      'phys-1-5', 'free-fall-apparatus', SQ(6, 'Draw a labelled diagram of the apparatus used in the experiment.'), 9,
      stem=STEM1[:1], id='phys-2023-hl-q1-i',
      decision='The scheme names four items and prices any three at 3 each ("[any three correct items merit '
               '3 × 3]"): a menu, with its "[–1 if no label present on diagram]" rule in the notes.'),
    T('1ii', 'Q1(ii)', 'A', P(2, 'Indicate the distance s on your diagram.'),
      [R('(bottom of) the object to the plate', 3)], 'phys-1-5', 'free-fall-distance',
      SQ(6, 'Indicate the distance s on your diagram.'), 3, stem=STEM1[:1], id='phys-2023-hl-q1-ii'),
    T('1iii', 'Q1(iii)', 'A', P(2, 'Describe how the time interval t was measured.'),
      [R('(electronic) timer', 3), R('started when object is released and stops when object hits plate', 3)],
      'phys-1-5', 'free-fall-timing', SQ(6, 'Describe how the time interval t was measured.'), 6, stem=STEM1[:1],
      id='phys-2023-hl-q1-iii'),
    T('1iv', 'Q1(iv)', 'A', P(2, 'Draw a suitable graph to show the relationship between s and t.'),
      [pt(S('s (m)', '0.1849'), 3, label=S('t² values')), C('labelled axes', 3), C('6 points plotted', 3),
       C('straight line with good fit', 3)], 'phys-1-5', 'free-fall-graph',
      SQ(6, 'Draw a suitable graph to show the relationship between s and t.'), 12, stem=STEM1 + [TABLE1],
      fig='q1iv-scheme-graph', id='phys-2023-hl-q1-iv',
      decision='The scheme prints its t² values as a table under "t² values" (read row by row) and draws the graph '
               '(the solution figure); the data table is lifted into the stem.'),
    T('1v', 'Q1(v)', 'A', P(2, 'Use the graph to calculate a value for g.'),
      [R('slope formula / s = ut + ½ at²', 3), R('g ≈ 9.8 m s⁻² from calculation', 3)], 'phys-1-5', 'g-from-graph',
      SQ(6, 'Use the graph to calculate a value for g.'), 6, stem=STEM1, fig='q1-table', id='phys-2023-hl-q1-v'),
    T('1vi', 'Q1(vi)', 'A', P(2, 'The object used was a smooth metal sphere. Explain why.'),
      [R('to reduce air resistance', 2), R('high density / magnetic / conductor', 2)], 'phys-1-5',
      'why-smooth-metal-sphere', SQ(6, 'The object used was a smooth metal sphere. Explain why.'), 4,
      stem=STEM1[:1], id='phys-2023-hl-q1-vi'),
    # ---------------------------------------------------------------- Q2 --
    T('2i', 'Q2(i)', 'A', P(3, 'How did the student find an approximate value for f?'),
      [R('focus the image of a distant object on a screen', 6), R('measure the distance from the screen to the mirror', 3)],
      'phys-2-3', 'approximate-focal-length', SQ(7, 'How did the student find an approximate value for f?'), 9,
      stem=STEM2, id='phys-2023-hl-q2-i', source_pages=[3], decision=LINKED.format(w='"the image distance"')),
    T('2ii', 'Q2(ii)', 'A', P(3, 'Why did the student find an approximate value for f?'),
      [R('object must be outside focal point / to get an image on the screen / to check answer', 3)], 'phys-2-3',
      'why-approximate-focal-length', SQ(7, 'Why did the student find an approximate value for f?'), 3,
      stem=STEM2, id='phys-2023-hl-q2-ii', source_pages=[3], decision=LINKED.format(w='"the image distance"')),
    T('2iii', 'Q2(iii)', 'A', P(3, 'Draw a labelled diagram of the apparatus used in this experiment.',
                               'Show u and v on your diagram.'),
      [C('object, screen, mirror', 3), C('u shown', 3), C('v shown', 3)], 'phys-2-3', 'concave-mirror-apparatus',
      SQ(7, 'Draw a labelled diagram of the apparatus used in this experiment.'), 9, stem=STEM2,
      id='phys-2023-hl-q2-iii', source_pages=[3], decision=LINKED.format(w='"the image distance"')),
    T('2iv', 'Q2(iv)', 'A', P(3, 'Describe how the student determined and measured v.'),
      [R('move object/screen/mirror', 3), R('until a (sharp) image is formed on the screen', 3),
       R('measure v with a metre stick', 3)], 'phys-2-3', 'measuring-image-distance',
      SQ(7, 'Describe how the student determined and measured v.'), 9, stem=STEM2, id='phys-2023-hl-q2-iv', source_pages=[3], decision=LINKED.format(w='"the image distance"')),
    T('2v', 'Q2(v)', 'A', P(3, 'Use all of the data to calculate f.'),
      [R('1/u + 1/v = 1/f', 2), C('substitution for u and v (once)', 2), C('first calculation of f', 2),
       C('two further calculations for f', 2, units=[1, 1]), R('average of values for f = 15.4 cm', 2)],
      'phys-2-3', 'focal-length-calculation', SQ(7, 'Use all of the data to calculate f.'), 10,
      stem=STEM2 + [DATA2], fig='q2-table', id='phys-2023-hl-q2-v',
      decision='"two further calculations for f [2 × 1]": one row of two 1-mark units.'),
    # ---------------------------------------------------------------- Q3 --
    T('3i', 'Q3(i)', 'A', P(3, 'Draw a labelled diagram of how the apparatus was arranged in this experiment.'),
      [C('source of light', 3), C('screen/spectrometer', 3), C('diffraction grating', 3),
       C('arrangement', 3, note_sel=NOLABEL)], 'phys-2-6', 'diffraction-grating-apparatus',
      SQ(8, 'Draw a labelled diagram of how the apparatus was arranged in this experiment.'), 12, stem=STEM3,
      id='phys-2023-hl-q3-i'),
    T('3ii', 'Q3(ii)', 'A', P(3, 'How were the third order images identified?'),
      [R('third image on both sides of central image', 3)], 'phys-2-6', 'identifying-third-order-images',
      SQ(8, 'How were the third order images identified?'), 3, stem=STEM3, id='phys-2023-hl-q3-ii'),
    T('3iii', 'Q3(iii)', 'A', P(3, 'Calculate the grating constant d.'),
      [R('1/300000 ≈ 3.33 × 10⁻⁶ m', 3)], 'phys-2-6', 'grating-constant',
      SQ(8, 'Calculate the grating constant d.'), 3, stem=STEM3, id='phys-2023-hl-q3-iii'),
    T('3iv', 'Q3(iv)', 'A', P(3, 'Calculate the wavelength of the red light.'),
      [R('nλ = d sinθ', 3), R('1.04/2 = 0.52 (m)', 3), R('θ = 34.74°', 3), R('λ = 6.33 × 10⁻⁷ m', 3)], 'phys-2-6',
      'wavelength-of-red-light', SQ(8, 'Calculate the wavelength of the red light.'), 12, stem=STEM3,
      id='phys-2023-hl-q3-iv'),
    T('3va', 'Q3(v)(a)', 'A', [P(3, 'Describe how the pattern observed on the screen changes when:'), M('(a)', 3),
                               P(3, 'the diffraction grating is replaced with a diffraction grating of fewer lines per mm,')],
      [R('images are closer together', 4)], 'phys-2-6', 'fewer-lines-per-mm',
      SQ(8, 'the diffraction grating is replaced with a diffraction grating of fewer lines per mm,'), 4, stem=STEM3,
      id='phys-2023-hl-q3-v', decision=bundled('(a), (b) and (c)', '(a)')),
    T('3vb', 'Q3(v)(b)', 'A', [P(3, 'Describe how the pattern observed on the screen changes when:'), M('(b)', 3),
                               P(3, 'the red light is replaced with green light,')],
      [R('images are closer together', 4)], 'phys-2-6', 'green-light-pattern',
      SQ(8, 'the red light is replaced with green light,'), 4, stem=STEM3),
    T('3vc', 'Q3(v)(c)', 'A', [P(3, 'Describe how the pattern observed on the screen changes when:'), M('(c)', 3),
                               P(3, 'the screen is moved further away from the grating.')],
      [R('images are further apart', 2)], 'phys-2-6', 'screen-moved-further-away',
      SQ(8, 'the screen is moved further away from the grating.'), 2, stem=STEM3),
    # ---------------------------------------------------------------- Q4 --
    T('4i', 'Q4(i)', 'A', P(4, 'Draw a labelled diagram of how the apparatus was arranged in this experiment.'),
      [R('steam generator and delivery tube', 3), R('calorimeter with water', 3), R('thermometer', 3),
       C('arrangement', 3, note_sel=NOLABEL)], 'phys-2-1', 'latent-heat-apparatus',
      SQ(9, 'Draw a labelled diagram of how the apparatus was arranged in this experiment.'), 12, stem=STEM4,
      id='phys-2023-hl-q4-i'),
    T('4ii', 'Q4(ii)', 'A', P(4, HOW4, piece=1, psep=', (iii)'),
      [R('refrigeration / ice bucket / adding ice which was allowed to melt completely / etc.', 3)], 'phys-2-1',
      'cooling-the-water', SQ(9, HOW4), 3, stem=STEM4, id='phys-2023-hl-q4-ii-iii',
      decision='The paper prints (ii) and (iii) inside one sentence, priced [3] each: the question is the printed '
               'line cut at its own markers. ' + bundled('(ii) and (iii)', '(ii)')),
    T('4iii', 'Q4(iii)', 'A', [P(4, HOW4, piece=1, psep=' (ii) cool the water, '),
                               P(4, HOW4, piece=2, psep=' (ii) cool the water, ')],
      [R('steam trap / delivery tube sloped upwards / insulated delivery tube', 3)], 'phys-2-1', 'drying-the-steam',
      SQ(9, HOW4), 3, stem=STEM4,
      decision='The paper prints (ii) and (iii) inside one sentence: the question is that line without (ii)\'s words.'),
    T('4iv', 'Q4(iv)', 'A', P(4, WHY4, piece=1, psep=', (v)'),
      [R('to make sure that the energy lost to surroundings cancelled the energy gained from', 3,
         end='condensed more quickly')], 'phys-2-1', 'why-cool-the-water', SQ(9, WHY4), 3, stem=STEM4,
      id='phys-2023-hl-q4-iv-v',
      decision='The paper prints (iv) and (v) inside one sentence, priced [3] each: the question is the printed '
               'line cut at its own markers. ' + bundled('(iv) and (v)', '(iv)')),
    T('4v', 'Q4(v)', 'A', [P(4, WHY4, piece=1, psep=' (iv) cool the water, '),
                           P(4, WHY4, piece=2, psep=' (iv) cool the water, ')],
      [R('to make sure that the steam had not lost its latent heat', 3, end='to make sure no water is added')],
      'phys-2-1', 'why-dry-the-steam', SQ(9, WHY4), 3, stem=STEM4,
      decision='The paper prints (iv) and (v) inside one sentence: the question is that line without (iv)\'s words.'),
    T('4vi', 'Q4(vi)', 'A', P(4, 'Use the data to calculate the specific latent heat of vaporisation of water.'),
      [pt(S('mcΔθ; ml', piece=1, psep=';'), 6), pt(S('mcΔθ; ml', piece=2, psep=';'), 3),
       anyn(S('mw = 45.8 (g); mₛ = 2.7 (g); Δθw = 30.9 (°C); Δθₛ = 63.6 (°C)'), 4, 1, sep=';',
            note='The scheme prices the four values [4 × 1]: 1 mark each.'),
       R('l = 2.22 × 10⁶ J kg⁻¹', 3)], 'phys-2-1', 'latent-heat-calculation',
      SQ(9, 'Use the data to calculate the specific latent heat of vaporisation of water.'), 16,
      stem=STEM4 + [DATA4, SHC4], fig='q4-table', id='phys-2023-hl-q4-vi',
      decision='"mcΔθ; ml [6 + 3]": the two expressions 6 then 3, in the order printed; the four values are '
               'priced [4 × 1], one claim each.'),
    # ---------------------------------------------------------------- Q5 --
    T('5i', 'Q5(i)', 'A', P(4, 'Draw a circuit diagram for this experiment with the diode in forward bias.'),
      [C('source of voltage', 3), C('diode in forward bias', 3), C('voltmeter across the diode', 3),
       C('(milli)ammeter in series', 3)], 'phys-3-3', 'forward-bias-circuit',
      SQ(10, 'Draw a circuit diagram for this experiment with the diode in forward bias.'), 12, stem=STEM5[:1],
      id='phys-2023-hl-q5-i', source_pages=[4], decision=LINKED.format(w='"a circuit diagram"')),
    T('5ii', 'Q5(ii)', 'A', P(4, 'Draw a suitable graph to show the relationship between I and V for a diode in forward',
                             'bias.'),
      [C('labelled axes', 3), C('6 points plotted', 3), C('curve with good fit', 3)], 'phys-3-3',
      'forward-bias-graph', SQ(10, 'Draw a suitable graph to show the relationship between I and V'), 9,
      stem=STEM5 + [TABLE5], fig='q5ii-scheme-graph', id='phys-2023-hl-q5-ii',
      decision='The scheme draws the graph (the solution figure); the data table is lifted into the stem.'),
    T('5iii', 'Q5(iii)', 'A', P(4, 'Is Ohm’s law obeyed for this diode? Justify your answer.'),
      [R('no', 3), R('not a straight line', 3)], 'phys-3-3', 'ohms-law-diode',
      SQ(10, 'Is Ohm’s law obeyed for this diode? Justify your answer.'), 6, stem=STEM5, fig='q5-table',
      id='phys-2023-hl-q5-iii'),
    T('5iv', 'Q5(iv)', 'A', P(4, 'Draw a circuit diagram for this experiment with the diode in reverse bias.'),
      [C('diode in reverse bias', 3), C('voltmeter across the diode and (micro)ammeter', 3)], 'phys-3-3',
      'reverse-bias-circuit', SQ(10, 'Draw a circuit diagram for this experiment with the diode in reverse bias.'), 6,
      stem=STEM5[:1] + [REVERSE], id='phys-2023-hl-q5-iv', source_pages=[4],
      decision=LINKED.format(w='"the circuit"')),
    T('5v', 'Q5(v)', 'A', P(4, 'Sketch a graph to show the relationship between I and V for a diode in reverse bias.'),
      [C('axes labelled', 3), C('correct shape', 4)], 'phys-3-3', 'reverse-bias-graph',
      SQ(10, 'Sketch a graph to show the relationship between I and V for a diode in reverse bias.'), 7,
      stem=STEM5[:1] + [REVERSE], id='phys-2023-hl-q5-v', source_pages=[4],
      decision='The scheme names the shape as "correct shape" and draws no reverse-bias graph: two criterion rows. '
               + LINKED.format(w='"the circuit"')),
    # ============================================================ Section B ==
    # ---------------------------------------------------------------- Q6 --
    T('6a', 'Q6(a)', 'B', P(5, 'An airplane starts from rest on a runway and', 'acceleration due to gravity.'),
      [R('v = 80.56 (m s⁻¹)', 2), R('v = u + at', 2), R('a = 2.44 (m s⁻²)', 2), R('a = 0.25 g', 1)], 'phys-1-1',
      'airplane-acceleration-in-g', SQ(11, 'An airplane starts from rest on a runway and reaches a velocity'), 7,
      stem=[G6], id='phys-2023-hl-q6-a'),
    T('6b', 'Q6(b)', 'B', P(5, 'Explain the term solar constant.'),
      [R('(solar) energy falling normally on the Earth', 3), R('per second', 2), R('per m²', 2)], 'phys-2-4',
      'solar-constant', SQ(11, 'Explain the term solar constant.'), 7, id='phys-2023-hl-q6-b'),
    T('6c', 'Q6(c)', 'B', P(5, 'A converging lens of focal length 15 cm is placed', 'Calculate the power of the combination.'),
      [pt(S('P = 1/f ; PT = P₁ + P₂', piece=1, psep=';'), 3), pt(S('P = 1/f ; PT = P₁ + P₂', piece=2, psep=';'), 2),
       R('PT = –13.33 m⁻¹', 2)], 'phys-2-3', 'power-of-lens-combination',
      SQ(11, 'A converging lens of focal length 15 cm is placed in combination with a diverging lens of'), 7,
      id='phys-2023-hl-q6-c', decision='"[3 + 2]" against the two formulae printed on one line: 3 then 2.'),
    T('6d', 'Q6(d)', 'B', P(5, 'Uranus has a mass of 8.7 × 10²⁵ kg and a radius of 25 400 km.',
                           'Calculate the acceleration due to gravity on Uranus.'),
      [R('g = GM/d²', 4), R('g = 8.99 m s⁻²', 3)], 'phys-1-5', 'gravity-on-uranus',
      SQ(11, 'Uranus has a mass of 8.7 × 10²⁵ kg and a radius of 25 400 km.'), 7, id='phys-2023-hl-q6-d'),
    T('6e', 'Q6(e)', 'B', P(5, 'Draw a diagram to show how a ray of light can be turned through 90°', 'prism.'),
      [C('ray entering normally at one short face', 2), C('ray exiting at the other short face', 2),
       C('total internal reflection', 3)], 'phys-2-3', 'prism-turns-ray-90',
      SQ(11, 'Draw a diagram to show how a ray of light can be turned through 90°'), 7, id='phys-2023-hl-q6-e'),
    T('6f', 'Q6(f)', 'B', P(5, 'State one application of stress polarisation.'),
      [R('e.g. to identify weaknesses in plastics', 7)], 'phys-2-7', 'stress-polarisation',
      SQ(11, 'State one application of stress polarisation.'), 7, id='phys-2023-hl-q6-f'),
    T('6g', 'Q6(g)', 'B', P(5, 'What is meant by potential difference?'),
      [R('work done', 4, end='// formula', note_sel=LEGEND), R('per unit charge (moved between two points)', 3,
                                                                 end='// notation')],
      'phys-3-3', 'potential-difference', SQ(11, 'What is meant by potential difference?'), 7, id='phys-2023-hl-q6-g',
      decision='Each line printed with its // side ("// formula", "// notation"; the scheme prints no formula): '
               'one row per line, as printed.'),
    T('6h', 'Q6(h)', 'B', P(5, 'Calculate the power output of a resistor of resistance 3.4 Ω when a',
                           'maintained across it.'),
      [pt(S('P = VI; V = IR', piece=1, psep=';'), 3), pt(S('P = VI; V = IR', piece=2, psep=';'), 2),
       R('P = 889.7 W', 2)], 'phys-3-3', 'power-in-resistor',
      SQ(11, 'Calculate the power output of a resistor of resistance 3.4 Ω'), 7, id='phys-2023-hl-q6-h',
      decision='"[3 + 2]" against the two formulae printed on one line: 3 then 2.'),
    T('6i', 'Q6(i)', 'B', P(5, 'The peak voltage of an a.c. supply is 311 V. Calculate its rms voltage.'),
      [R('Vrms = Vₚₑₐₖ/√2', 4), R('Vrms = 219.9 V', 3)], 'phys-3-6', 'rms-voltage',
      SQ(11, 'The peak voltage of an a.c. supply is 311 V. Calculate its rms voltage.'), 7, id='phys-2023-hl-q6-i'),
    T('6j', 'Q6(j)', 'B', P(5, 'A proton experiences a force of 4.59 × 10⁻¹⁶ N when it moves with velocity v perpendicular',
                           'Calculate v.'),
      [R('F = qvB', 4), R('v = 1.55 × 10⁵ m s⁻¹', 3)], 'phys-3-5', 'proton-velocity-in-field',
      SQ(11, 'A proton experiences a force of 4.59 × 10⁻¹⁶ N'), 7, id='phys-2023-hl-q6-j'),
    T('6k', 'Q6(k)', 'B', P(5, 'Explain what is meant by a chain reaction in nuclear fission.'),
      [R('neutrons', 4), R('from one reaction initiate subsequent reactions / cause a self-sustaining reaction', 3)],
      'phys-4-6', 'chain-reaction', SQ(12, 'Explain what is meant by a chain reaction in nuclear fission.'), 7,
      id='phys-2023-hl-q6-k'),
    T('6l', 'Q6(l)', 'B', P(5, 'The equation to describe an emission line spectrum is hf = E₂ – E₁.',
                           'symbols in this equation stands for.'),
      [R('h = Planck constant', 2), R('f = frequency', 2),
       pt(S('E₂ = higher energy; E₁ = lower energy', piece=1, psep=';'), 2),
       pt(S('E₂ = higher energy; E₁ = lower energy', piece=2, psep=';'), 1)], 'phys-4-3', 'emission-line-spectrum',
      SQ(12, 'The equation to describe an emission line spectrum is hf = E₂ – E₁.'), 7, id='phys-2023-hl-q6-l',
      decision='"[2 + 1]" against the two meanings printed on one line: 2 then 1.'),
    # ---------------------------------------------------------------- Q7 --
    T('7i', 'Q7(i)', 'B', P(6, 'State Newton’s third law of motion.'),
      [R('when object A applies a force on object B', 3, end='// every action', note_sel=LEGEND),
       pt(S('object B applies an equal but opposite force on object A // equal but opposite reaction [3]',
            piece=1, psep=' ['), 3)], 'phys-1-2', 'newtons-third-law',
      SQ(13, 'State Newton’s third law of motion.'), 6, id='phys-2023-hl-q7-i',
      decision='Each line printed with its // side: one row per line, as printed.',
      cells='The scheme sets the second line\'s "[3]" inside that line\'s text (p13, rendered and looked at), so '
            'the reader takes no cell from it: the printed cells are [3] + [3] = 6.'),
    T('7ii', 'Q7(ii)', 'B', P(6, 'Show that F = ma is a special case of Newton’s second law of motion.'),
      [FR(13, (84, 122, 165, 150), 'F∝ (mv−mu)/t', 3), FR(13, (84, 146, 165, 172), 'F= (k(mv – mu))/t', 3),
       R('F= kma', 3), R('k = 1 from the definition of the newton', 3)], 'phys-1-2', 'f-equals-ma',
      SQ(13, 'Show that F = ma is a special case of Newton’s second law of motion.'), 12,
      decision='The scheme sets the derivation in CambriaMath, its v, u and a mis-mapped (GLYPHS): the fractions '
               'are read with G(\'fraction\'), "F = kma" from its corrected line.'),
    T('7iii', 'Q7(iii)', 'B', P(6, 'Calculate the velocity of the ball immediately after impact.'),
      [FR(13, (84, 252, 165, 276), 'F= (mv−mu)/t', 3), R('v = 76.05 m s⁻¹', 3)], 'phys-1-2', 'velocity-after-impact',
      SQ(13, 'Calculate the velocity of the ball immediately after impact.'), 6, stem=[GOLF]),
    T('7iva', 'Q7(iv)(a)', 'B', [P(6, 'Draw separate diagrams to show the forces acting on the ball'), M('(a)', 6),
                                 P(6, 'during impact,')],
      [C('weight down', 3), C('force applied by club', 3)], 'phys-1-2', 'forces-during-impact',
      SQ(13, 'during impact,'), 6, stem=[GOLF, ANGLE]),
    T('7ivb', 'Q7(iv)(b)', 'B', [P(6, 'Draw separate diagrams to show the forces acting on the ball'), M('(b)', 6),
                                 P(6, 'immediately after impact.')],
      [C('weight down', 3)], 'phys-1-2', 'forces-after-impact', SQ(13, 'immediately after impact.'), 3,
      stem=[GOLF, ANGLE]),
    T('7v', 'Q7(v)', 'B', P(6, 'Calculate the maximum height reached by the ball.'),
      [R('uy = 76.05 sin 15°', 3), R('v² = u² + 2as', 3), R('s = 19.77 m', 3)], 'phys-1-1', 'maximum-height',
      SQ(13, 'Calculate the maximum height reached by the ball.'), 9, stem=[GOLF] + Q7III + [ANGLE, G7],
      id='phys-2023-hl-q7-v'),
    T('7vi', 'Q7(vi)', 'B', P(6, 'Calculate the time it takes for the ball to travel a horizontal distance of 280 m.'),
      [R('vₓ = 76.05 cos 15°', 2), R('v = s/t', 2), R('t = 3.81 s', 2)], 'phys-1-1', 'time-for-horizontal-distance',
      SQ(13, 'Calculate the time it takes for the ball to travel a horizontal distance of 280 m.'), 6,
      stem=[GOLF] + Q7III + [ANGLE], id='phys-2023-hl-q7-vi'),
    T('7vii', 'Q7(vii)', 'B', P(6, 'Calculate the magnitude and direction of the velocity of the wind.'),
      [R('a² = b² + c²', 2), R('v = 9.0 (m s⁻¹)', 2), R('tan θ = opposite/adjacent', 2), R('θ = 24.3° (N of E)', 2)],
      'phys-1-1', 'wind-velocity', SQ(13, 'Calculate the magnitude and direction of the velocity of the wind.'), 8,
      stem=[WIND], id='phys-2023-hl-q7-vii'),
    # ---------------------------------------------------------------- Q8 --
    T('8i', 'Q8(i)', 'B', P(7, 'What is resonance?'),
      [R('the transfer of energy', 3), R('between two systems with the same (natural) frequency', 3)], 'phys-2-5',
      'resonance', SQ(14, 'What is resonance?'), 6, stem=[GUITAR], id='phys-2023-hl-q8-i'),
    T('8ii', 'Q8(ii)', 'B', P(7, 'Describe a laboratory experiment to demonstrate resonance.'),
      [C('apparatus', 3), C('method', 3), C('observation', 3)], 'phys-2-5', 'demonstrating-resonance',
      SQ(14, 'Describe a laboratory experiment to demonstrate resonance.'), 9, stem=[GUITAR], decision=EXPT),
    T('8iiia', 'Q8(iii)(a)', 'B', [GRAPHS8, M('(a)', 7), P(7, 'f and T')],
      [R('labelled axis f and √T', 2), pt(S('straight line through the origin', after='labelled axis f and √T'), 2)],
      'phys-2-6', 'f-against-tension', SQ(14, 'f and T'), 4, stem=[STRING], id='phys-2023-hl-q8-iii-t',
      decision='The scheme prices each of the three graphs in cells of its own: one card each.'),
    T('8iiib', 'Q8(iii)(b)', 'B', [GRAPHS8, M('(b)', 7), P(7, 'f and l')],
      [R('labelled axis f and 1/l', 2), pt(S('straight line through the origin', after='labelled axis f and 1/l'), 2)],
      'phys-2-6', 'f-against-length', SQ(14, 'f and l'), 4, stem=[STRING], id='phys-2023-hl-q8-iii-l',
      decision='The scheme prices each of the three graphs in cells of its own: one card each.'),
    T('8iiic', 'Q8(iii)(c)', 'B', [GRAPHS8, M('(c)', 7), P(7, 'f and µ')],
      [R('labelled axis f and 1/√μ', 2), pt(S('straight line through the origin', after='labelled axis f and 1/√μ'), 2)],
      'phys-2-6', 'f-against-linear-density', SQ(14, 'f and µ'), 4, stem=[STRING], id='phys-2023-hl-q8-iii-mu',
      decision='The scheme prices each of the three graphs in cells of its own: one card each.'),
    T('8iva', 'Q8(iv)(a)', 'B', [EFFECT8, M('(a)', 7), P(7, 'T', after='increased by a factor of four.')],
      [R('increases', 2), R('by a factor of 2', 2)], 'phys-2-6', 'tension-increased-fourfold',
      SQ(14, 'For each of the following variables, state the effect on the frequency f if the variable is'), 4,
      stem=[STRING], id='phys-2023-hl-q8-iv-ab', decision=bundled('(a) and (b)', '(a)')),
    T('8ivb', 'Q8(iv)(b)', 'B', [EFFECT8, M('(b)', 7), P(7, 'l', after='increased by a factor of four.')],
      [R('decreases', 2), R('by a factor of 4', 2)], 'phys-2-6', 'length-increased-fourfold',
      SQ(14, 'For each of the following variables, state the effect on the frequency f if the variable is'), 4,
      stem=[STRING]),
    T('8ivc', 'Q8(iv)(c)', 'B', [EFFECT8, M('(c)', 7), P(7, 'µ', after='increased by a factor of four.')],
      [pt(S('decreases', nth=2), 2), pt(S('by a factor of 2', nth=2), 2)], 'phys-2-6',
      'linear-density-increased-fourfold',
      SQ(14, 'For each of the following variables, state the effect on the frequency f if the variable is'), 4,
      stem=[STRING], id='phys-2023-hl-q8-iv-c'),
    T('8v', 'Q8(v)', 'B', P(7, 'What are harmonics?'),
      [R('frequencies', 3), R('which are multiples of the fundamental', 2)], 'phys-2-6', 'harmonics',
      SQ(14, 'What are harmonics?'), 5, stem=[HARM], id='phys-2023-hl-q8-v'),
    T('8vi', 'Q8(vi)', 'B', P(7, 'Draw a diagram to show the string vibrating at its third harmonic.'),
      [C('node at both ends', 3), C('two additional nodes in correct arrangement', 3)], 'phys-2-6',
      'third-harmonic-diagram', SQ(14, 'Draw a diagram to show the string vibrating at its third harmonic.'), 6,
      stem=[HARM], id='phys-2023-hl-q8a-vi'),
    T('8vii', 'Q8(vii)', 'B', P(7, 'Calculate the frequency of the string when it is vibrating at its third harmonic.'),
      [R('λ = 0.62/1.5 = 0.4133 (m)', 2), R('c = fλ', 2), R('f = 919.4 Hz', 2)], 'phys-2-6',
      'third-harmonic-frequency',
      SQ(14, 'Calculate the frequency of the string when it is vibrating at its third harmonic.'), 6, stem=[HARM],
      id='phys-2023-hl-q8-vii'),
    # ---------------------------------------------------------------- Q9 --
    T('9i', 'Q9(i)', 'B', P(8, 'Write a nuclear equation for the alpha decay of plutonium–238.'),
      [G('equation', page=15, clip=(84, 148, 180, 172), expect='²³⁸₉₄Pu → ²³⁴₉₂U + ⁴₂He', marks=8, units=[1] * 8,
         note='[8 × 1]: the scheme prices the equation one mark at a time.',
         note_sel=S('[–3 for each additional incorrect species]'))],
      'phys-4-4', 'alpha-decay-of-plutonium', SQ(15, 'Write a nuclear equation for the alpha decay of plutonium–238.'),
      8, stem=STEM9, fig='q9i-scheme', id='phys-2023-hl-q9-i',
      decision='The scheme sets the plutonium nuclide in CambriaMath with mis-mapped glyphs (GLYPHS); the equation '
               'is read with G(\'equation\') and the scheme\'s print of it is the solution figure.'),
    T('9ii', 'Q9(ii)', 'B', P(8, 'Calculate the energy released during each decay of plutonium–238, in MeV.'),
      [C('conversion from u to kg', 3), R('mass defect (= 9.95757 × 10⁻³⁰ kg)', 3), R('E = mc²', 3),
       R('E = 8.95 × 10⁻¹³ (J)', 3), R('E = 5.6 (MeV)', 3)], 'phys-4-5', 'energy-released-per-decay',
      SQ(15, 'Calculate the energy released during each decay of plutonium–238, in MeV.'), 15, stem=STEM9 + Q9I,
      id='phys-2023-hl-q9-ii'),
    T('9iii', 'Q9(iii)', 'B', P(8, 'State the thermometric property of a thermocouple.'),
      [R('emf / voltage', 3)], 'phys-2-1', 'thermocouple-property',
      SQ(15, 'State the thermometric property of a thermocouple.'), 3, stem=[THERMO], id='phys-2023-hl-q9-iii'),
    T('9iv', 'Q9(iv)', 'B', P(8, 'Draw a labelled diagram of the arrangement of a thermocouple.'),
      [C('two different metals', 3), C('first junction at one temperature', 3),
       C('second junction at a different temperature', 3, note_sel=NOLABEL)], 'phys-2-1', 'thermocouple-diagram',
      SQ(15, 'Draw a labelled diagram of the arrangement of a thermocouple.'), 9, stem=[THERMO],
      id='phys-2023-hl-q9-iv'),
    T('9v', 'Q9(v)', 'B', P(8, 'Calculate the rate of decay of the plutonium in each generator in 1977.'),
      [R('λ = ln 2/T½', 3), R('A = λN', 3), R('T½ = 87.8 × 365.25 × 24 × 60 × 60 = 2.77 × 10⁹ (s)', 3),
       R('N = 4/3.9529085 × 10⁻²⁵ = 1.012 × 10²⁵ (atoms)', 3), R('A = 2.53 × 10¹⁵ Bq', 2)], 'phys-4-4',
      'rate-of-decay-1977', SQ(15, 'Calculate the rate of decay of the plutonium in each generator in 1977.'), 14,
      stem=STEM9 + [HALF], id='phys-2023-hl-q9-v'),
    T('9vi', 'Q9(vi)', 'B', P(8, 'Calculate the year when only 1 kg of the plutonium will remain in each generator.'),
      [R('reference to two half-lives', 2), R('1977 + 2 × 87.8 = 2152', 2)], 'phys-4-4', 'year-1-kg-remains',
      SQ(15, 'Calculate the year when only 1 kg of the plutonium will remain in each generator.'), 4,
      stem=STEM9 + [HALF], id='phys-2023-hl-q9-vi'),
    T('9vii', 'Q9(vii)', 'B', P(8, 'Use one of Newton’s laws to explain why the spacecraft maintain constant velocities.'),
      [R('no force acting on it', 3)], 'phys-1-2', 'constant-velocity-newton',
      SQ(15, 'Use one of Newton’s laws to explain why the spacecraft maintain constant velocities.'), 3, stem=[VOY],
      id='phys-2023-hl-q9-vii'),
    # --------------------------------------------------------------- Q10 --
    T('10i', 'Q10(i)', 'B', P(9, 'Describe how point discharge occurs.'),
      [R('accumulation of charge at a point', 3), R('large electric field generated / ionisation of the air', 3),
       R('unlike charges attract and like charges repel', 3)], 'phys-3-2', 'point-discharge',
      SQ(16, 'Describe how point discharge occurs.'), 9, stem=STEM10, id='phys-2023-hl-q10-i'),
    T('10ii', 'Q10(ii)', 'B', P(9, 'Describe a laboratory experiment to demonstrate point discharge.'),
      [C('apparatus', 3), C('method', 3), C('observation', 3)], 'phys-3-2', 'demonstrating-point-discharge',
      SQ(16, 'Describe a laboratory experiment to demonstrate point discharge.'), 9, stem=STEM10[1:], decision=EXPT),
    T('10iii', 'Q10(iii)', 'B', P(9, 'Draw the electric field around the dome.'),
      [C('radial field lines', 3), C('away from the dome', 3)], 'phys-3-2', 'field-around-dome',
      SQ(16, 'Draw the electric field around the dome.'), 6, stem=[DOME], id='phys-2023-hl-q10-iii'),
    T('10iv', 'Q10(iv)', 'B', P(9, 'Calculate the electric field strength at the surface of the dome.'),
      [R('F = q₁q₂/4πεd²', 3), R('r = 16 (cm)', 3), R('E = 7.0 × 10⁴ N C⁻¹', 3)], 'phys-3-2',
      'field-strength-at-dome', SQ(16, 'Calculate the electric field strength at the surface of the dome.'), 9,
      stem=[DOME], id='phys-2023-hl-q10-iv'),
    T('10v', 'Q10(v)', 'B', P(9, 'Calculate the force experienced by an electron placed at the surface of the dome.'),
      [R('E = F/q', 3), R('F = 1.12 × 10⁻¹⁴ N towards the centre of the dome', 3)], 'phys-3-2', 'force-on-electron',
      SQ(16, 'Calculate the force experienced by an electron placed at the surface of the dome.'), 6,
      stem=[DOME, M('(iv)', 9), P(9, 'Calculate the electric field strength at the surface of the dome.')],
      id='phys-2023-hl-q10-v'),
    T('10vi', 'Q10(vi)', 'B', P(9, 'Calculate the maximum speed of the electrons produced in the tube.'),
      [R('qV / ½mv²', 3), R('qV = ½mv²', 3), R('v = 1.57 × 10⁸ m s⁻¹', 3)], 'phys-4-2', 'electron-speed-in-x-ray-tube',
      SQ(16, 'Calculate the maximum speed of the electrons produced in the tube.'), 9, stem=[XRAY],
      id='phys-2023-hl-q10-vi'),
    T('10vii', 'Q10(vii)', 'B', P(9, 'Draw a labelled diagram of an X'),
      [C('low voltage filament / heating coil', 2), C('cathode & anode/target', 2),
       C('(high) voltage (between cathode & anode)', 2), C('cooling / shielding / window / (partial) vacuum', 2)],
      'phys-4-2', 'x-ray-tube-diagram', SQ(16, 'Draw a labelled diagram of an X-ray tube.'), 8,
      id='phys-2023-hl-q10-vii'),
    # --------------------------------------------------------------- Q11 --
    T('11i', 'Q11(i)', 'B', P(10, 'Give a detailed explanation of how a current is induced in the',
                             'metal that is being detected.'),
      [R('changing magnetic field', 3), R('cutting the metal', 3), R('emf induced', 3), R('current flows', 3)],
      'phys-3-6', 'metal-detector-induction',
      SQ(17, 'Give a detailed explanation of how a current is induced in the metal that is being detected.'), 12,
      stem=[STEM11], id='phys-2023-hl-q11-i'),
    T('11ii', 'Q11(ii)', 'B', P(10, 'State Faraday’s law of electromagnetic induction.'),
      [R('(size of) emf induced is proportional to', 3, end='// formula', note_sel=LEGEND),
       R('the rate of change of magnetic flux', 3, end='// notation')], 'phys-3-6', 'faradays-law',
      SQ(17, 'State Faraday’s law of electromagnetic induction.'), 6, stem=[LAWS], id='phys-2023-hl-q11-ii',
      decision='Each line printed with its // side ("// formula", "// notation"; the scheme prints no formula): '
               'one row per line, as printed.'),
    T('11iii', 'Q11(iii)', 'B', P(10, 'State Lenz’s law of electromagnetic induction.'),
      [R('direction of an induced current/emf', 3), R('is such as to oppose the change causing it', 3)], 'phys-3-6',
      'lenzs-law', SQ(17, 'State Lenz’s law of electromagnetic induction.'), 6, stem=[LAWS],
      id='phys-2023-hl-q11-iii'),
    T('11iv', 'Q11(iv)', 'B', P(10, 'Describe a laboratory experiment to demonstrate either one of these laws.'),
      [C('apparatus', 3), C('method', 3), C('observation', 3)], 'phys-3-6', 'demonstrating-induction-law',
      SQ(17, 'Describe a laboratory experiment to demonstrate either one of these laws.'), 9, stem=[LAWS],
      decision=EXPT + ' "Either one of these laws" is a choice inside the ask, priced as one experiment.'),
    T('11v', 'Q11(v)', 'B', P(10, 'Calculate the time taken for the coil to fully enter the field.'),
      [R('v = s/t', 3), R('t = 0.015 s', 3)], 'phys-3-6', 'time-to-enter-field',
      SQ(17, 'Calculate the time taken for the coil to fully enter the field.'), 6, stem=COIL, id='phys-2023-hl-q11-v'),
    T('11vi', 'Q11(vi)', 'B', P(10, 'Calculate the average emf induced as the coil enters the field.'),
      [R('A = πr²', 3), R('Ø = BA', 3), R('E =(-)ΔØ/Δt', 3), R('E = 1.70 V', 3)], 'phys-3-6', 'average-emf',
      SQ(17, 'Calculate the average emf induced as the coil enters the field.'), 12,
      stem=COIL + [M('(v)', 10), P(10, 'Calculate the time taken for the coil to fully enter the field.')],
      id='phys-2023-hl-q11-vi'),
    T('11vii', 'Q11(vii)', 'B', P(10, 'Calculate the average current in the coil as it enters the field.'),
      [R('V = IR', 3), R('I = 0.74 A', 2)], 'phys-3-6', 'average-current',
      SQ(17, 'Calculate the average current in the coil as it enters the field.'), 5,
      stem=COIL + [M('(vi)', 10), P(10, 'Calculate the average emf induced as the coil enters the field.')],
      id='phys-2023-hl-q11-vii'),
    # --------------------------------------------------------------- Q12 --
    T('12ai', 'Q12(a)(i)', 'B', P(11, 'What is anti'),
      [R('same mass', 3), R('opposite charge', 3)], 'phys-4-5', 'anti-matter',
      SQ(18, 'What is anti-matter?'), 6, stem=[ANTI], id='phys-2023-hl-q12a-i'),
    T('12aii', 'Q12(a)(ii)', 'B', P(11, 'Who made a mathematical prediction of the existence of', 'matter?'),
      [R('Dirac', 3)], 'phys-4-5', 'prediction-of-anti-matter',
      SQ(18, 'Who made a mathematical prediction of the existence of anti-matter?'), 3, stem=[ANTI],
      id='phys-2023-hl-q12a-ii'),
    T('12aiii', 'Q12(a)(iii)', 'B', P(11, 'Write an equation to show the pair production of an electron'),
      [R('hf = / γ =', 3),
       G('equation', page=18, clip=(84, 236, 160, 256), expect='2mₑc² / ⁰₋₁e + ⁰₁e', marks=3)],
      'phys-4-5', 'pair-production-equation',
      SQ(18, 'Write an equation to show the pair production of an electron-positron pair.'), 6, stem=[POS],
      fig='q12aiii-scheme', id='phys-2023-hl-q12a-iii',
      decision='The scheme prints the left side ("hf = / γ =", [3]) and the right side ("2mₑc² / ⁰₋₁e+⁰₁e", [3]) '
               'on two lines; the electron and positron carry their numbers stacked, read with G(\'equation\'), '
               'and the scheme\'s print of both lines is the solution figure.'),
    T('12aiva', 'Q12(a)(iv)(a)', 'B', [P(11, 'Explain how (a) charge, (b) momentum are conserved in this interaction.',
                                        piece=1, psep=', (b) momentum'),
                                      P(11, 'Explain how (a) charge, (b) momentum are conserved in this interaction.',
                                        piece=2, psep=', (b) momentum')],
      [R('charge before = charge after = 0', 3)], 'phys-4-5', 'charge-conserved',
      SQ(18, 'Explain how (a) charge, (b) momentum are conserved in this interaction.'), 3, stem=[POS] + Q12AIII,
      id='phys-2023-hl-q12a-iv',
      decision='The paper prints (a) and (b) inside one sentence and the scheme prices each [3]: the question is '
               'that line without (b)\'s word. ' + bundled('(a) and (b)', '(a)')),
    T('12aivb', 'Q12(a)(iv)(b)', 'B', [P(11, 'Explain how (a) charge, (b) momentum are conserved in this interaction.',
                                        piece=1, psep=' (a) charge,'),
                                      P(11, 'Explain how (a) charge, (b) momentum are conserved in this interaction.',
                                        piece=2, psep=' (a) charge,')],
      [pt(S('momentum before = momentum after ≈ 0 / particles move in opposing directions [3]', piece=1, psep=' ['),
          3)], 'phys-4-5', 'momentum-conserved',
      SQ(18, 'Explain how (a) charge, (b) momentum are conserved in this interaction.'), 3, stem=[POS] + Q12AIII,
      decision='The paper prints (a) and (b) inside one sentence: the question is that line without (a)\'s word. '
               'The scheme sets this line\'s "[3]" inside its text, so the row is cut at it.'),
    T('12av', 'Q12(a)(v)', 'B', P(11, 'List the fundamental forces, in order of increasing strength, that a positron'),
      [pt(S('gravitational, weak, electromagnetic', piece=k, psep=','), 1) for k in (1, 2, 3)]
      + [C('correct order', 3)], 'phys-4-5', 'forces-on-positron',
      SQ(18, 'List the fundamental forces, in order of increasing strength, that a positron experiences.'), 6,
      stem=[POS], id='phys-2023-hl-q12a-v',
      decision='"[3 × 1]" against the three forces printed on one line: 1 each; then "correct order [3]".'),
    T('12avi', 'Q12(a)(vi)', 'B', P(11, 'Name the fundamental force that a positron does not experience.'),
      [R('strong (nuclear)', 3)], 'phys-4-5', 'force-positron-does-not-experience',
      SQ(18, 'Name the fundamental force that a positron does not experience.'), 3, stem=[POS],
      id='phys-2023-hl-q12a-vi'),
    T('12avii', 'Q12(a)(vii)', 'B', P(11, 'Calculate the wavelength of the electromagnetic radiation produced when a proton and',
                                      'annihilate.'),
      [R('E = mc²', 3), R('E = hf', 3), R('c = fλ', 3), R('λ = 1.32 × 10⁻¹⁵ m', 3)], 'phys-4-5',
      'annihilation-wavelength', SQ(18, 'Calculate the wavelength of the electromagnetic radiation produced'), 12,
      stem=[LHC], id='phys-2023-hl-q12a-vii'),
    T('12aviii', 'Q12(a)(viii)', 'B', P(11, 'Hadrons can be classified as baryons or mesons.'),
      [R('a baryon contains three quarks', 2), R('a meson contains a quark and an anti-quark', 2)], 'phys-4-5',
      'baryons-and-mesons', SQ(18, 'Hadrons can be classified as baryons or mesons.'), 4, id='phys-2023-hl-q12a-viii'),
    T('12aixa', 'Q12(a)(ix)(a)', 'B', P(11, 'State the quark composition of (a) a proton', piece=1, psep=', (b)'),
      [R('up, up, down', 3, whole=True)], 'phys-4-5', 'quarks-of-proton',
      SQ(18, 'State the quark composition of (a) a proton, (b) an anti-proton.'), 3, id='phys-2023-hl-q12a-ix',
      decision='The paper prints (a) and (b) inside one sentence and the scheme prices each [3]: the question is '
               'that line cut at its own markers. ' + bundled('(a) and (b)', '(a)')),
    T('12aixb', 'Q12(a)(ix)(b)', 'B', [P(11, 'State the quark composition of (a) a proton', piece=1, psep=' (a) a proton, '),
                                      P(11, 'State the quark composition of (a) a proton', piece=2, psep=' (a) a proton, ')],
      [R('anti-up, anti-up, anti-down', 3, whole=True)], 'phys-4-5', 'quarks-of-anti-proton',
      SQ(18, 'State the quark composition of (a) a proton, (b) an anti-proton.'), 3,
      decision='The paper prints (a) and (b) inside one sentence: the question is that line without (a)\'s words.'),
    T('12ax', 'Q12(a)(x)', 'B', P(11, 'The Large Hadron Collider is an example of a modern particle accelerator.',
                                  'Cockroft and Walton.'),
      [R('e.g. circular', 4)], 'phys-4-5', 'lhc-and-cockcroft-walton',
      SQ(18, 'The Large Hadron Collider is an example of a modern particle accelerator.'), 4,
      id='phys-2023-hl-q12a-x'),
    T('12bia', 'Q12(b)(i)(a)', 'B', P(11, 'Draw labelled diagrams to show the basic structure of (a) the semiconductor diode,'),
      [C('p-type connected to n-type', 6)], 'phys-3-3', 'semiconductor-diode-structure',
      SQ(19, 'Draw labelled diagrams to show the basic structure of (a) the semiconductor diode,'), 6,
      id='phys-2023-hl-q12b-i', decision=bundled('(a) and (b)', '(a)')),
    T('12bib', 'Q12(b)(i)(b)', 'B', [P(11, 'Draw labelled diagrams to show the basic structure of (a) the semiconductor diode,',
                                       piece=1, psep=' (a) the semiconductor diode,'), P(11, '(b) the transistor.')],
      [R('n-type – p-type – n-type', 6)], 'phys-3-3', 'transistor-structure',
      SQ(19, 'Draw labelled diagrams to show the basic structure of (a) the semiconductor diode,'), 6,
      decision='The paper prints (a) and (b) inside one sentence: the question is that sentence without (a)\'s words.'),
    T('12bii', 'Q12(b)(ii)', 'B', P(11, 'Describe the principle of operation of a light emitting diode.'),
      [R('diode in forward bias', 3), R('an electron recombines with a hole', 3), R('releasing a photon', 3)],
      'phys-3-3', 'led-operation', SQ(19, 'Describe the principle of operation of a light emitting diode.'), 9,
      stem=[LEDS], id='phys-2023-hl-q12b-ii'),
    T('12biii', 'Q12(b)(iii)', 'B', P(11, 'State one use of a light emitting diode.'),
      [C('any valid use', 3)], 'phys-3-3', 'led-use', SQ(19, 'State one use of a light emitting diode.'), 3,
      stem=[LEDS],
      decision='The scheme prints "any valid use [3]" and names no use: one criterion row in its words.'),
    T('12biv', 'Q12(b)(iv)', 'B', P(11, 'Draw a circuit diagram, including a bridge rectifier and a capacitor, that can',
                                    'convert a.c. to d.c..'),
      [C('four diodes in correct arrangement', 3), C('output resistor', 3),
       C('capacitor in parallel with output resistor', 3)], 'phys-3-3', 'bridge-rectifier-circuit',
      SQ(19, 'Draw a circuit diagram, including a bridge rectifier and a capacitor, that can be used to'), 9,
      stem=[LEDS], id='phys-2023-hl-q12b-iv', source_pages=[11], decision=LINKED.format(w='"a circuit diagram"')),
    T('12bv', 'Q12(b)(v)', 'B', P(11, 'Draw a circuit diagram to show how a transistor can be used as a voltage inverter.'),
      [C('transistor and resistor in series', 3), C('input voltage indicated', 3), C('output voltage indicated', 3)],
      'phys-3-3', 'transistor-voltage-inverter',
      SQ(19, 'Draw a circuit diagram to show how a transistor can be used as a voltage inverter.'), 9,
      id='phys-2023-hl-q12b-v', source_pages=[11], decision=LINKED.format(w='"a circuit diagram"')),
    T('12bvi', 'Q12(b)(vi)', 'B', P(11, 'A voltage inverter is a NOT gate. Draw its truth table.'),
      [R('input 0, output 1', 3, whole=True), R('input 1, output 0', 3, whole=True)], 'phys-3-3', 'not-gate-truth-table',
      SQ(19, 'A voltage inverter is a NOT gate. Draw its truth table.'), 6, id='phys-2023-hl-q12b-vi'),
    T('12bvii', 'Q12(b)(vii)', 'B', P(11, 'Draw a labelled diagram of an electromagnetic relay.'),
      [C('coil and core', 2), C('armature', 2), C('make-break mechanism', 2, note_sel=NOLABEL)], 'phys-3-4',
      'electromagnetic-relay-diagram', SQ(19, 'Draw a labelled diagram of an electromagnetic relay.'), 6,
      stem=[RELAY], id='phys-2023-hl-q12b-vii'),
    T('12bviii', 'Q12(b)(viii)', 'B', P(11, 'What is the function of an electromagnetic relay?'),
      [R('switch', 2)], 'phys-3-4', 'function-of-relay', SQ(19, 'What is the function of an electromagnetic relay?'), 2,
      stem=[RELAY], id='phys-2023-hl-q12b-viii'),
    # --------------------------------------------------------------- Q13 --
    T('13ia', 'Q13(i)(a)', 'B', RES13 + [M('(a)', 13), P(13, 'the mass (in kg) of water in this reservoir,')],
      [R('ρ = m/V', 3), R('m = 2.29 × 10⁹ (kg)', 3)], 'phys-1-4', 'mass-of-water-in-reservoir',
      SQ(20, 'the mass (in kg) of water in this reservoir,'), 6, stem=[PUMPED, DATA13], id='phys-2023-hl-q13-i-a'),
    T('13ib', 'Q13(i)(b)', 'B', RES13 + [M('(b)', 13), P(13, 'the potential energy (in J) stored in this reservoir,')],
      [R('E = mgh', 2), R('E = 7.21 × 10¹² (J)', 2)], 'phys-1-4', 'potential-energy-in-reservoir',
      SQ(20, 'the potential energy (in J) stored in this reservoir,'), 4,
      stem=[PUMPED, M('(a)', 13), P(13, 'the mass (in kg) of water in this reservoir,'), DATA13],
      id='phys-2023-hl-q13-i-b'),
    T('13ic', 'Q13(i)(c)', 'B', RES13 + [M('(c)', 13), P(13, 'the maximum power (in W) that could be generated if the',
                                                        'emptied in 24 hours.')],
      [R('P = E/t', 2), R('P = 8.35 × 10⁷ (W)', 2)], 'phys-1-4', 'maximum-power-generated',
      SQ(20, 'the maximum power (in W) that could be generated if the reservoir was fully emptied'), 4,
      stem=[PUMPED, M('(b)', 13), P(13, 'the potential energy (in J) stored in this reservoir,'), DATA13],
      id='phys-2023-hl-q13-i-c'),
    T('13ii', 'Q13(ii)', 'B', P(13, 'State the main energy conversion that takes place (a) as the water flows down through',
                               'generator at position B.'),
      [R('gravitational/potential to kinetic', 4, label=S('a')), R('kinetic to electrical', 3, label=S('b'))],
      'phys-1-4', 'energy-conversions-a-b',
      SQ(20, 'State the main energy conversion that takes place (a) as the water flows down through the'), 7,
      stem=[PUMPED], fig='q13-diagram', id='phys-2023-hl-q13-ii',
      labels=[L('A', P(13, 'the pipe at position A and (b) as the water flows through the generator at position B.',
                       piece=[1, 1], psep=[' and (b) as the water flows through ', ' at position A']), True),
              L('B', P(13, 'the pipe at position A and (b) as the water flows through the generator at position B.',
                       piece=[2, 1], psep=[' and (b) as the water flows through ', ' at position B.']), True)],
      decision='One cell "[4 + 3]" prices (a) and (b) together: one card, (a) 4 and (b) 3 in the order printed. '
               'The label key names A and B from the question\'s own words.'),
    T('13iii', 'Q13(iii)', 'B', P(13, 'A motor operates on the principle that a current carrying conductor in a magnetic field',
                                 'Describe a laboratory experiment to demonstrate this principle.'),
      [C('apparatus', 3), C('method', 2), C('observation', 2)], 'phys-3-5', 'demonstrating-force-on-conductor',
      SQ(20, 'A motor operates on the principle that a current carrying conductor in a magnetic field'), 7,
      decision=EXPT),
    T('13iva', 'Q13(iv)(a)', 'B', FLY + [M('(a)', 13), P(13, 'the period (in s) of the flywheel’s motion,')],
      [R('T = 1/f', 3), R('T = 0.012 (s)', 3)], 'phys-1-6', 'flywheel-period',
      SQ(21, 'the period (in s) of the flywheel’s motion,'), 6, id='phys-2023-hl-q13-iv-a'),
    T('13ivb', 'Q13(iv)(b)', 'B', FLY[1:] + [M('(b)', 13), P(13, 'the angular velocity of the flywheel,')],
      [R('T = 2π/ω', 2), R('ω = 523.6 (radians) s⁻¹', 2)], 'phys-1-6', 'flywheel-angular-velocity',
      SQ(21, 'the angular velocity of the flywheel,'), 4,
      stem=FLY[:1] + [M('(a)', 13), P(13, 'the period (in s) of the flywheel’s motion,')], id='phys-2023-hl-q13-iv-b'),
    T('13ivc', 'Q13(iv)(c)', 'B', FLY[1:] + [M('(c)', 13), P(13, 'the centripetal acceleration at the circumference of the flywheel.')],
      [R('a = rω²', 2), R('a = 1.9 × 10⁵ m s⁻² (towards the centre)', 2)], 'phys-1-6', 'flywheel-centripetal-acceleration',
      SQ(21, 'the centripetal acceleration at the circumference of the flywheel.'), 4,
      stem=FLY[:1] + [M('(a)', 13), P(13, 'the period (in s) of the flywheel’s motion,'), M('(b)', 13),
                      P(13, 'the angular velocity of the flywheel,')], id='phys-2023-hl-q13-iv-c'),
    T('13v', 'Q13(v)', 'B', P(13, 'A battery is a source of emf. Name two other sources of emf.'),
      [anyn(None, 2, 4, steps=[4, 3], open_list=True,
            note='The scheme prints "[4 + 3]" against examples ("e.g. ... etc."): the first source 4, the second 3.',
            options=[S('e.g. mains, solar cell, thermocouple, etc.', piece=[1, 2], psep=[',', 'e.g. ']),
                     S('e.g. mains, solar cell, thermocouple, etc.', piece=2, psep=','),
                     S('e.g. mains, solar cell, thermocouple, etc.', piece=3, psep=',')])],
      'phys-3-3', 'sources-of-emf', SQ(21, 'A battery is a source of emf. Name two other sources of emf.'), 7,
      id='phys-2023-hl-q13-v'),
    T('13vi', 'Q13(vi)', 'B', P(13, 'As we move away from generating electricity using non', 'the text. Explain why.'),
      [pt(S('renewable sources are more likely to vary in the rate at which they produce electricity [7]',
            piece=1, psep=' ['), 7)], 'phys-1-4', 'why-energy-storage',
      SQ(21, 'As we move away from generating electricity using non-renewable sources'), 7, stem=PASSAGE,
      id='phys-2023-hl-q13-vi',
      decision='The scheme sets this line\'s "[7]" inside its text, so the row is cut at it.'),
    # --------------------------------------------------------------- Q14 --
    T('14ai', 'Q14(a)(i)', 'B', P(14, 'State Hooke’s law.'),
      [R('(restoring) force', 3, end='// equation', note_sel=LEGEND),
       R('proportional to displacement', 3, end='// notation')], 'phys-1-3', 'hookes-law',
      SQ(22, 'State Hooke’s law.'), 6, stem=[HOOKE], id='phys-2023-hl-q14a-i',
      decision='Each line printed with its // side ("// equation", "// notation"; the scheme prints no equation): '
               'one row per line, as printed.'),
    T('14aii', 'Q14(a)(ii)', 'B', P(14, 'Calculate the elastic constant of the spring.'),
      [R('mg = ks', 3), R('k = 196 N m⁻¹', 3)], 'phys-1-3', 'elastic-constant',
      SQ(22, 'Calculate the elastic constant of the spring.'), 6, stem=[SPRING, G14], id='phys-2023-hl-q14a-ii'),
    T('14aiii', 'Q14(a)(iii)', 'B', P(14, 'Calculate the period of oscillation of the block.'),
      [R('T = 2π/ω', 3), R('ω = √(k/m)', 3), R('T = 0.32 s', 3)], 'phys-1-3', 'period-of-oscillation',
      SQ(22, 'Calculate the period of oscillation of the block.'), 9,
      stem=[SPRING, M('(ii)', 14), P(14, 'Calculate the elastic constant of the spring.'), G14],
      id='phys-2023-hl-q14a-iii'),
    T('14aiv', 'Q14(a)(iv)', 'B', P(14, 'Sketch a graph that explains Boyle’s law. Label the axes on your graph.'),
      [R('axes labelled as p and 1/V', 5, units=[3, 2]), R('straight line through the origin', 2)], 'phys-2-1',
      'boyles-law-graph', SQ(22, 'Sketch a graph that explains Boyle’s law. Label the axes on your graph.'), 7,
      stem=[BOYLE], id='phys-2023-hl-q14a-iv',
      decision='"[3 + 2]" prices the one printed line naming both axes: one row of 5 (units 3 and 2).'),
    T('14bi', 'Q14(b)(i)', 'B', P(14, 'Name the effect which causes this increase in frequency.'),
      [R('Doppler', 3)], 'phys-2-7', 'doppler-effect', SQ(23, 'Name the effect which causes this increase in frequency.'),
      3, stem=[SPEAKER], id='phys-2023-hl-q14b-i'),
    T('14bii', 'Q14(b)(ii)', 'B', P(14, 'Calculate the speed of the speaker.'),
      [R('f\' = cf/(c ± u)', 3), C('substitution', 3), R('u = 56.7 m s⁻¹', 3)], 'phys-2-7', 'speed-of-speaker',
      SQ(23, 'Calculate the speed of the speaker.'), 9, stem=[SPEAKER, SOUND], id='phys-2023-hl-q14b-ii'),
    T('14biii', 'Q14(b)(iii)', 'B', P(14, 'Red shift in astronomy is also due to this effect.', 'universe?'),
      [R('it is expanding', 4)], 'phys-2-7', 'red-shift', SQ(23, 'Red shift in astronomy is also due to this effect.'),
      4, id='phys-2023-hl-q14b-iii'),
    T('14biv', 'Q14(b)(iv)', 'B', P(14, 'Distinguish between sound intensity and sound intensity level.'),
      [R('sound intensity is measured in W m⁻²', 3), R('sound intensity level is measured in dB', 3)], 'phys-2-5',
      'intensity-and-intensity-level', SQ(23, 'Distinguish between sound intensity and sound intensity level.'), 6,
      stem=[POWER], id='phys-2023-hl-q14b-iv'),
    T('14bv', 'Q14(b)(v)', 'B', P(14, 'The speaker of power P is replaced by a speaker of power 4P.', 'level measured.'),
      [R('reference to 3 dB / doubling / I ∝P', 3), R('6 dB', 3)], 'phys-2-5', 'increase-in-intensity-level',
      SQ(23, 'The speaker of power P is replaced by a speaker of power 4P.'), 6, stem=[POWER],
      id='phys-2023-hl-q14b-v'),
    T('14ci', 'Q14(c)(i)', 'B', P(15, 'State the relationship between R and A for the wire.'),
      [R('inversely proportional', 4)], 'phys-3-3', 'resistance-and-area',
      SQ(24, 'State the relationship between R and A for the wire.'), 4, stem=[WIRE], id='phys-2023-hl-q14c-i'),
    T('14cii', 'Q14(c)(ii)', 'B', P(15, 'Using an appropriate diagram, derive an expression for the effective resistance RT',
                                    'in series.'),
      [C('circuit diagram showing resistors in series', 3), R('VT = V₁ + V₂', 3), R('IRT = IR₁ + IR₂', 3),
       R('RT = R₁ + R₂', 3)], 'phys-3-3', 'resistors-in-series',
      SQ(24, 'Using an appropriate diagram, derive an expression for the effective resistance RT'), 12,
      id='phys-2023-hl-q14c-ii'),
    T('14ciii', 'Q14(c)(iii)', 'B', P(15, 'Calculate the total resistance of the circuit shown below.'),
      [R('1/Rₚ = 1/R₁ + 1/R₂', 3), R('Rₚ = 2.5 (Ω)', 3), R('RT = 7.5 Ω', 3)], 'phys-3-3', 'total-resistance',
      SQ(24, 'Calculate the total resistance of the circuit shown below.'), 9, fig='q14c-circuit',
      id='phys-2023-hl-q14c-iii'),
    T('14civ', 'Q14(c)(iv)', 'B', P(15, 'Describe how a fourth 5 Ω resistor could be added to the circuit so as to reduce the',
                                    'total effective resistance of the circuit.'),
      [R('in parallel', 3)], 'phys-3-3', 'reducing-total-resistance',
      SQ(24, 'Describe how a fourth 5 Ω resistor could be added to the circuit'), 3, fig='q14c-circuit',
      id='phys-2023-hl-q14c-iv'),
    T('14di', 'Q14(d)(i)', 'B', P(15, 'Distinguish between thermionic emission and the photoelectric effect.'),
      [R('thermionic emission is caused by heat', 3), R('the photoelectric effect is caused by light', 3)],
      'phys-4-2', 'thermionic-and-photoelectric',
      SQ(25, 'Distinguish between thermionic emission and the photoelectric effect.'), 6, id='phys-2023-hl-q14d-i'),
    T('14dii', 'Q14(d)(ii)', 'B', P(15, 'Describe a laboratory experiment to demonstrate the photoelectric effect.'),
      [C('apparatus', 3), C('method', 3), C('observation', 3)], 'phys-4-2', 'demonstrating-photoelectric-effect',
      SQ(25, 'Describe a laboratory experiment to demonstrate the photoelectric effect.'), 9, decision=EXPT),
    T('14diii', 'Q14(d)(iii)', 'B', P(15, 'Calculate the frequency of the incident radiation.'),
      [R('hf = Ø + Eₖ', 3), R('Eₖ = ½mv²', 3), R('Ø = 4.3 × 1.6 × 10⁻¹⁹ = 6.88 × 10⁻¹⁹ (J)', 2),
       R('v = 6.9 × 10⁶ (m s⁻¹)', 2), R('f = 3.37 × 10¹⁶ Hz', 3)], 'phys-4-2', 'frequency-of-incident-radiation',
      SQ(25, 'Calculate the frequency of the incident radiation.'), 13, stem=[ZINC], id='phys-2023-hl-q14d-iii'),
]

ANSWER_VARIANTS = {}
RETAINED = {}
WITHDRAW = {}

FIGURES = {
    # key suffix: (doc, page, rect in PDF points, credit, letters, alt, solution)
    'q1-table': ('paper', 2, (52, 240, 545, 300), SEC, [],
                 'Table of the recorded data: s (cm) 40, 50, 60, 70, 80, 90; t (cs) 29, 32, 35, 38, 40, 43.', False),
    'q1iv-scheme-graph': ('scheme', 6, (80, 480, 540, 668), SEC, [],
                          "The marking scheme's graph: s (m), from 0 to 1, against t² (s²), from 0 to 0.2, with six "
                          "plotted points from 0.4 m to 0.9 m on a dotted straight line drawn from the origin.", True),
    'q2-table': ('paper', 3, (180, 128, 416, 190), SEC, [],
                 'Table of the recorded data: u (cm) 20.0, 30.0, 40.0; v (cm) 66.3, 31.1, 25.2.', False),
    'q4-table': ('paper', 4, (52, 128, 545, 268), SEC, [],
                 'Table of the recorded data: mass of calorimeter 65.8 g; mass of calorimeter + water 111.6 g before '
                 'adding steam and 114.3 g after; temperature of water 5.5 °C before adding steam and 36.4 °C after.',
                 False),
    'q5-table': ('paper', 4, (52, 478, 545, 538), SEC, [],
                 'Table of the recorded data: V (V) 0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7; I (mA) 0, 0, 0, 0, 5, 20, '
                 '70, 220.', False),
    'q5ii-scheme-graph': ('scheme', 10, (80, 322, 450, 545), SEC, [],
                          "The marking scheme's graph: I (mA), from -50 to 250, against V (V), from 0 to 0.8; the curve "
                          "runs along zero to about 0.3 V, rises slowly, then turns steeply up to 220 mA at 0.7 V.", True),
    'q9i-scheme': ('scheme', 15, (80, 151.5, 185, 174), SEC, [],
                   "The marking scheme's equation: plutonium (238 above, 94 below) gives uranium (234 above, 92 below) "
                   "plus helium (4 above, 2 below), each nucleus printed with its mass number above its atomic number.",
                   True),
    'q12aiii-scheme': ('scheme', 18, (80, 216, 165, 258), SEC, [],
                       "The marking scheme's two lines: hf = / γ =, then 2mₑc² / an electron (0 above, -1 below) plus a "
                       "positron (0 above, 1 below), each printed with its numbers stacked before the e.", True),
    'q13-diagram': ('paper', 12, (115, 298, 508, 500), 'esbarchives.ie', ['A', 'B'],
                    'Cross-section of a hillside: a pipe runs from a reservoir at the top left down the slope, with the '
                    'letter A beside it, to a wheel-shaped machine near the foot marked B, which opens into a lower '
                    'reservoir on the right.', False),
    'q14c-circuit': ('paper', 15, (212, 155, 410, 305), SEC, [],
                     'Circuit diagram: a cell in a rectangular loop with a 5 Ω resistor along the bottom, joined to two '
                     '5 Ω resistors side by side between the same two wires on the right.', False),
}
