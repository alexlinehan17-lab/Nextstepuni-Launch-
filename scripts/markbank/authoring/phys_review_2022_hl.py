"""Physics 2022 Higher Level — reviewed task ledger, correcting the sitting in place.

Independent visual sweep (2026-10-28), every page rendered and read:
  * The paper (LC021ALP000EV), 16 pages: p1 cover ("Answer two questions from
    Section A and four questions from Section B"; the 2022 papers were adjusted
    for disruption to learning due to COVID-19), p2-p4 Section A (80 marks)
    Questions 1-5 (any two, 40 marks each), p5-p15 Section B (224 marks)
    Questions 6-14 (any four, 56 marks each), p15 also the acknowledgements
    (images on pages 5-15), p16 back cover.
  * The marking scheme, 24 pages: p1 cover, p2 note on published schemes, p3
    points to note (solidus, double solidus, units, graphs, slips), p4 annotation
    symbols, p5 Irish-language bonus table (Tábla 304), p6-p22 Questions 1-14
    (each question reprinted in regular type, its answers in bold, the mark cells
    at the right margin), p23 blank, p24 back cover.

The census reader's marks checksum for this sitting reads "224" against "280"
for 2023-2026: it reads the Section B head, which the 2022 paper prints as
"SECTION B (224 MARKS) Answer four questions from this section. Each question
carries 56 marks." (4 x 56), where 2023-2026 print five questions (280). The
2022 rubric explains it; no ask is lost and the census needed no fix (118
leaves, every one printed).

Every printed ask is carded at the scheme's own mark boundary: a roman, or a
sub-letter inside a roman where the scheme prices (a) and (b) apart (Q1(i),
Q7(vii), Q9(b)(ii), Q9(c)(ii), Q10(i), Q13(ii), Q13(v)). Section A and most of
Section B print a group mark after a run of romans ("(10)" closing Q1(i)-(ii)):
GROUP_TOTALS. Q6 is any eight of (a)-(l) at 7 each (8 x 7): one card per
letter, and (l) prints two alternatives joined by "or", both carded as ROUTES of
the one leaf. Q12 is either (a) or (b), and Q14 any two of (a)-(d): every part is
carded. A mark cell "[4 + 2]" set against the two lines of one statement or calculation
is carded in the order printed (the 2025 convention); set against interchangeable items
(Q1(viii)'s two conditions, Q6(c)'s two forces, Q11(iv)'s two features) it is a menu
priced step by step (the 2023 Ordinary and 2026 Higher convention); "[any 3 x 3]" menus
are anyn. Definitions the
scheme prints as words "//" a formula with its notation (Q7(i), Q11(i),
Q14(d)(i)) are answer variants labelled "In words" / "As a formula"; the two
methods of Q12(b)(vi) are routes inside the card.

The scheme sets the nuclear equations of Q10(ii), Q10(iii) and Q12(a)(ii) in a
bold CambriaMath that draws every glyph twice and whose ToUnicode map gives
several glyphs one character ("Pu" reads "PP", "239" reads "222", "94" reads
"99"): GLYPHS sets each glyph by its id, every id read against the rendered
page, and the equations are read with G('equation').

The sitting was already carded (114 authored cards, all shipped). Every task is
re-derived from the PDFs and every shipped id is kept, mapped (`id=`) to the
task it was carding. The asks the bank had excluded (Q4(iii), the stacked 1/f in
its ask; Q10(ii), Q10(iii) and Q12(a)(ii), the nuclear equations) and the one it
had left open (Q9(c)(ii)) are carded, with the bundled parts split and Q6(l)'s
second alternative added.
"""
from phys_review_lib import Q, SQ, S, M, G, pt, anyn, T

YEAR, LEVEL = 2022, 'hl'
REVIEWED_AT = '2026-10-28'
BASELINE_COMMIT = '99ec7f0a0d6b243f4d5a1dc9b14a6a958e98095e'

SOURCES = {
    'paper': {'path': 'examiner-reports/physics/papers/2022-hl-paper.pdf', 'fileid': 'LC021ALP000EV.pdf',
              'sha256': '8b9b84d905e1d09691e115178f3d563116233928d075fcea9ffdafe387f26798', 'pages': 16},
    'scheme': {'path': 'examiner-reports/physics/schemes/2022-hl.pdf', 'fileid': 'LC021ALP000EV.pdf',
               'sha256': '7fd0309754396d9091b6dd2d15523d099a469c8d09078a43f145ef2c775e64b3', 'pages': 24},
}

PAGE_ROLES = {
    'paper': {1: 'cover', **{p: 'questions' for p in range(2, 15)}, 15: 'questions-acknowledgements',
              16: 'back-cover'},
    'scheme': {1: 'cover', 2: 'note', 3: 'conventions', 4: 'annotations', 5: 'irish-bonus',
               **{p: 'marking' for p in range(6, 23)}, 23: 'blank', 24: 'back-cover'},
}

LETTERED = {6, 9, 12, 14}

# Glyph-id corrections for the scheme's bold CambriaMath (phys_review_lib._page_dict): the nuclear
# equations of Q10(ii), Q10(iii) (p16) and Q12(a)(ii) (p18). Each id found with get_texttrace at the
# glyph's own origin and read on the rendered page (peeked at 300 dpi).
GLYPHS = {'scheme': {'CambriaMath': {
    2172: 'P',   # p16: the P of Pu (reads "P")
    2203: 'u',   # p16: the u of Pu (reads "P")
    2157: 'A',   # p16 Q10(iii): the A of Am (reads "A")
    2195: 'm',   # p16 Q10(iii): the m of Am (reads "A")
    2187: 'e',   # p16 Q10(iii): the beta particle's e; p18: the e of He
    2196: 'n',   # p16 Q10(ii): the neutron's n
    2168: 'L',   # p18: the L of Li (reads "L")
    2191: 'i',   # p18: the i of Li (reads "L")
    2164: 'H',   # p18: the H of He (reads "H")
    2198: 'p',   # p18: the proton's p
    2777: '0',   # p16: the 0 of the neutron's and the beta particle's numbers
    2778: '1',   # p16: the 1 of 241 and of the neutron's and beta's numbers; p18: the proton's 1 and 1
    2779: '2',   # p16: the first digit of 239 and 241, the 2 of "2n"; p18: the 2 of "2He" and He's 2
    2780: '3',   # p16: the 3 of 239; p18: lithium's 3 (each reads "2")
    2781: '4',   # p16: the 4 of 94 and of 241; p18: helium's 4 (each reads "9")
    2782: '5',   # p16 Q10(iii): the 5 of 95 (reads "9")
    2784: '7',   # p18: lithium's 7
    2786: '9',   # p16: the 9 of 239, 94 and 95
}}}
# No line set in the doubled maths font is lifted as text: the three equations are read with
# G('equation') and an expect.
VERIFIED_LINES = []

QUESTION_TOTALS = {**{n: 40 for n in range(1, 6)}, **{n: 56 for n in (6, 7, 8, 9, 10, 11, 13)},
                   12: 112,   # either (a) or (b), 56 each: both carded
                   14: 112}   # any two of (a)-(d), 28 each: all four carded
PART_TOTALS = {(9, 'a'): 15, (9, 'b'): 20, (9, 'c'): 21, (12, 'a'): 56, (12, 'b'): 56,
               **{(14, x): 28 for x in 'abcd'}}
BEST_OF = {6: (8, 7)}
GROUP_TOTALS = {
    (1, ('i', 'ii')): 10, (1, ('iii', 'iv', 'v')): 12, (1, ('vi', 'vii', 'viii')): 18,
    (2, ('i', 'ii', 'iii')): 18, (2, ('iv', 'v')): 15, (2, ('vi', 'vii')): 7,
    (3, ('i', 'ii')): 18, (3, ('iii', 'iv', 'v')): 22,
    (4, ('i', 'ii')): 18, (4, ('iii', 'iv', 'v')): 22,
    (5, ('i', 'ii')): 15, (5, ('iii', 'iv', 'v')): 25,
    (7, ('i', 'ii', 'iii', 'iv', 'v')): 28, (7, ('vi', 'vii', 'viii', 'ix')): 28,
    (8, ('i', 'ii', 'iii')): 18, (8, ('iv', 'v')): 18, (8, ('vi', 'vii', 'viii')): 20,
    (10, ('i', 'ii', 'iii')): 22, (10, ('iv', 'v', 'vi', 'vii')): 17, (10, ('viii', 'ix', 'x')): 17,
    (11, ('i', 'ii', 'iii')): 24, (11, ('iv', 'v', 'vi')): 22, (11, ('vii', 'viii')): 10,
    **{(13, (r,)): t for r, t in (('i', 7), ('ii', 14), ('iii', 7), ('iv', 7), ('v', 21))},
}
CHECKSUMS = {}

# Q6(l): "... Write an equation for this annihilation. or Draw the symbol for an AND gate. Write out the
# truth table for an AND gate." Two printed alternatives of the one 7-mark part.
ROUTES = {'Q6(l)': ['pair-annihilation', 'and-gate']}

SCAN_PAGES = {'paper': range(2, 16)}
SELECTION_SCAN = [
    ('paper', 2, 'the following', 'Q1 "The following data were recorded": a reference to the table.'),
    ('paper', 3, 'the following', 'Q2 "The following data were recorded": a reference to the table.'),
    ('paper', 3, 'the following', 'Q3 "The following data were recorded": a reference to the table.'),
    ('paper', 4, 'the following', 'Q4 "The following data were recorded": a reference to the table.'),
    ('paper', 4, 'the following', 'Q5 "The following data were recorded": a reference to the table.'),
    ('paper', 5, 'the following', 'Q6 "Answer any eight of the following parts": a best-eight of (a)-(l) at 7 '
                                  'each (8 x 7); every part is carded (BEST_OF).'),
    ('paper', 5, 'or', 'Q6(l) "... annihilation. or Draw the symbol for an AND gate ...": two printed '
                       'alternatives, each carded (ROUTES).'),
    ('paper', 8, 'or', 'Q9(b)(ii) "In terms of some or all of the symbols given": the ask\'s own wording, not a '
                       'choice.'),
    ('paper', 10, 'both', 'Q11(vii) "C–14 and C–12 are both isotopes of carbon": description.'),
    ('paper', 11, 'either', 'Q12 "Answer either part (a) or part (b)": whole-part choice; both parts are carded.'),
    ('paper', 11, 'or', 'Q12, the same choice.'),
    ('paper', 13, 'the following', 'Q13 "Read the following passage": a reference to the passage.'),
    ('paper', 14, 'any two', 'Q14 "Answer any two of the following parts": whole-part choice; every part is carded.'),
    ('paper', 14, 'the following', 'Q14, the same rubric.'),
]
ASK_SCAN_PAGES = {'paper': range(2, 16)}
ASK_EXEMPT = [
    (6, 'A spring of natural length 150 mm obeys Hooke’s law.', 'Q7 lead-in ("... When an object of mass 200 g is '
                                                              'attached ..."): a description, not an ask; lifted into '
                                                              'the stems.'),
    (7, 'Associated with every diode is a voltage called its junction voltage.', 'Q8 lead-in to (vi)-(viii) ("When a '
                                                                              'variable voltage is applied ..."): a '
                                                                              'description, not an ask; lifted into '
                                                                              'the stems.'),
    (15, 'State Examinations Commission', 'Acknowledgements: an image credit, not an ask.'),
]

SEC = 'State Examinations Commission'
CRIT = 'The scheme prints no answer here, only what earns the marks.'
NOLABEL = S('[–1 if no label present on diagram]')
VALUES = 'The scheme prints the values it expects in the table shown in the figure.'
SPECIES = S('[–3 for each additional incorrect species]')
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


def dslash(sel_start, sel_end, side):
    """One side of a line the scheme prints as two answers separated by "//"."""
    return S(sel_start, sel_end, piece=side, psep='//')


def bundled(parts, keep):
    return f'The old card bundled {parts}, which the scheme prices apart; it keeps its id for {keep}.'


# ------------------------------------------------------------------ stems --
STEM1 = P(2, 'A student used a metre stick to investigate the laws of equilibrium', '50.6 cm position.')
APPLIED1 = P(2, 'He then applied vertical forces to the metre stick and adjusted them until the metre stick was',
             'horizontal and in equilibrium.')
Q1I = P(2, 'Describe how the student determined (a) the centre of gravity and (b) the weight of', 'the metre stick.')
STEM2 = P(3, 'In an experiment to verify Boyle’s law, a student measured the length l of a column of air of fixed',
          'different values of air pressure p.')
TABLE2 = P(3, 'l (cm)', '136')
INCONSISTENT = P(3, 'One of the data points is inconsistent with the other data points.')
STEM3 = P(3, 'In an experiment to verify Snell’s law, a student measured the angle of incidence i and the angle of',
          'different values of i.')
TABLE3 = P(3, 'i (degrees)', '44')
STEM4 = P(4, 'In an experiment to determine the speed of sound in air a student measured the length l of a',
          'six different values of f.')
TABLE4 = P(4, 'f (Hz)', '13.7')
STEM5 = [P(4, 'A student performed a single experiment to (a) verify Joule’s law', 'temperature θ of the oil was determined.'),
         P(4, 'This process was repeated for six different values of I.')]
TABLE5 = [P(4, 'Room temperature = 17.0 °C'), P(4, 'I (A)', '62.1')]
SHM7 = P(6, 'The object is pulled down until the spring has a length of 200 mm.', 'simple harmonic motion.')
SPRING7 = P(6, 'A spring of natural length 150 mm obeys Hooke’s law.', 'increases to 185 mm.')
CIRCLE7 = P(6, 'The object is now detached from the spring and attached to the end of a string of fixed length',
            'of 0.5 s.')
G7 = P(6, '(acceleration due to gravity = 9.8 m s⁻²)')
Q7VII = P(6, 'Calculate (a) the angular velocity, (b) the linear velocity of the object.')
DOPING8 = [P(7, 'Semiconductors can be converted into p-type', 'n-type semiconductors by doping.'),
           P(7, 'A p-n junction is used in a diode.')]
DEPLETION8 = P(7, 'A depletion layer exists in a p-n junction.')
JUNCTION8 = P(7, 'Associated with every diode is a voltage called its junction voltage.', 'voltage is reached.')
SPHERE9 = P(8, 'A metal sphere of diameter 5 cm holds a charge of –6 μC.')
CAP9 = P(8, 'A device that is designed to store energy when it holds a specific charge is called a capacitor.')
PLATES9 = P(8, 'A parallel-plate capacitor has a dielectric of permittivity ε and its plates have an area of',
            'the capacitor stores energy W.')
Q9BII = P(8, 'In terms of some or all of the symbols given, write an expression for (a) the charge on',
          'each plate of the capacitor, (b) the distance between the plates.')
CIRCUIT9 = P(8, 'Three resistors X, Y and Z are arranged in a circuit as shown below.')
Q9CII = P(8, 'Calculate the current flowing (a) in resistor X, (b) in resistor Y.')
AM10 = P(9, 'Americium–241, a radioactive substance, is the key', 'plutonium–239 in nuclear reactors.')
Q10I = P(9, 'What is meant by (a) radioactivity, (b) ionisation?')
PU10 = P(9, 'A nucleus of plutonium–239 can absorb two neutrons to produce plutonium–241.',
         'beta decay to produce americium–241.')
FISSION10 = P(9, 'At present, nuclear reactors are fission reactors.')
MODERATOR10 = P(9, 'Fission reactors usually contain moderators.')
DETECTOR10 = [P(9, 'Americium–241 undergoes alpha decay in a smoke detector.', 'contains 6.0 × 10²³ nuclei.'),
              P(9, 'A typical smoke detector contains 0.29 μg of americium–241.')]
BRONZE11 = P(10, 'The Bronze Age began about 5000 years ago.', 'the culture and technology of the Bronze Age.')
FULACHT11 = [P(10, 'During the Bronze Age in Ireland, a fulacht fiadh was', 'placed into the water.'),
             P(10, 'A particular fulacht fiadh contained 750 litres of', 'heat capacity of 8.5 kJ K⁻¹ each.')]
LYRE11 = P(10, 'The earliest harps and lyres were produced in the Bronze Age.', 'and different diameters.')
STRING11 = P(10, 'A 65 cm string of mass 0.21 g is stretched between two points of a lyre', 'frequency of 440 Hz.')
CARBON11 = P(10, 'Archaeologists often use radiocarbon dating to estimate the age of wooden objects.',
             'carbon in a living tree.')
DATA11 = P(10, '(for water at 4 °C, 1 litre = 1 kg; specific heat capacity of water = 4180 J kg⁻¹ K⁻¹;',
           'half-life of carbon–14 = 5730 years)')
CW12 = P(11, 'In 1932 Ernest Walton and John Cockcroft verified', 'lithium metal.')
NUCLIDE12 = P(11, 'The mass of the ¹H nuclide is given on page 83 of the Formulae and Tables booklet as', '1.007825 u.')
CALC12 = P(11, 'Calculate')
GALV12 = P(12, 'A moving-coil galvanometer is a device for detecting and measuring', 'electric current.')
MULT12 = P(12, 'A resistor called a multiplier is used to convert a galvanometer into a voltmeter.')
SPEAKER12 = P(12, 'A loudspeaker also contains a moving coil.')
WAVE13 = P(13, 'Draw a labelled diagram of an experiment to demonstrate the wave nature of', 'light.')
TITAN13 = P(13, 'Titan orbits Saturn every 15.9 Earth days.', 'Saturn.')
CALC13 = P(13, 'Calculate', after='(v)')
DATA13 = P(13, '(acceleration due to gravity on Earth = 9.8 m s⁻²; radius of Saturn = 58200 km;',
           'radius of Titan = 2570 km)')
PROJ14 = P(14, 'An object is released with an initial velocity of 150 m s⁻¹ at an angle of 20° to the horizontal.')
G14 = P(14, '(acceleration due to gravity = 9.8 m s⁻²)')
PIERRE14 = [P(14, 'Pierre drops a child’s toy which emits sound of fixed frequency 500 Hz', 'from the top of the Eiffel tower.'),
            P(14, '(speed of sound in air = 340 m s⁻¹;', 'acceleration due to gravity = 9.8 m s⁻²)')]
PHOTO14 = P(15, 'The explanation of the photoelectric effect by Albert Einstein led to the quantum revolution',
            'in physics.')
LIGHT14 = P(15, 'Light of wavelength 450 nm is incident on a metal that has a work function of 2.4 eV.')
OBSERVED14 = P(15, 'It is observed that as the wavelength of the incident light increases, the speed of the emitted',
               'no electrons are emitted.')
MAGNET14 = P(15, 'A strong magnet is suspended from the end of a string and', 'with a constant amplitude.')

TASKS = [
    # ============================================================ Section A ==
    # ---------------------------------------------------------------- Q1 --
    T('1ia', 'Q1(i)(a)', 'A', dict(Q1I, piece=1, psep=' and (b)'),
      [R('suspended from a thread / balanced on a pivot', 3)], 'phys-1-2', 'finding-centre-of-gravity',
      SQ(6, 'Describe how the student determined (a) the centre of gravity and (b) the weight of', 'the metre stick.'),
      3, stem=[STEM1], id='phys-2022-hl-q1-i',
      decision='The paper prints (a) and (b) inside one sentence, priced [3] each: the question is the printed '
               'sentence cut at its own markers. ' + bundled('(a) and (b)', '(a)')),
    T('1ib', 'Q1(i)(b)', 'A', [dict(Q1I, piece=1, psep=' (a) the centre of gravity and '),
                               dict(Q1I, piece=2, psep=' (a) the centre of gravity and ')],
      [R('weighing scales / mass balance × g', 3)], 'phys-1-2', 'finding-weight-of-metre-stick',
      SQ(6, 'Describe how the student determined (a) the centre of gravity and (b) the weight of', 'the metre stick.'),
      3, stem=[STEM1],
      decision='The paper prints (a) and (b) inside one sentence: the question is that sentence without (a)\'s words.'),
    T('1ii', 'Q1(ii)', 'A', P(2, 'Why was it necessary to determine the centre of gravity of the metre stick?'),
      [R('to know where the weight acted / to calculate the moment [state/imply]', 4)], 'phys-1-2',
      'why-centre-of-gravity', SQ(6, 'Why was it necessary to determine the centre of gravity of the metre stick?'), 4,
      stem=[STEM1], id='phys-2022-hl-q1-ii'),
    T('1iii', 'Q1(iii)', 'A', P(2, 'Indicate on a labelled diagram how these vertical forces were applied to the metre stick.'),
      [R('weights', 2, end='[for downward forces]'),
       R('newtonmeters / weights and pulleys', 2, end='[for upward forces]', note_sel=NOLABEL)], 'phys-1-2',
      'applying-vertical-forces',
      SQ(6, 'Indicate on a labelled diagram how these vertical forces were applied to the metre stick.'), 4,
      stem=[STEM1, APPLIED1], id='phys-2022-hl-q1-iii',
      decision='Each apparatus row is printed beside its bracketed direction ("[for downward forces]"): one row each, '
               'with the direction.'),
    T('1iv', 'Q1(iv)', 'A', P(2, 'How was it ensured that the metre stick was in equilibrium?'),
      [R('not moving', 4)], 'phys-1-2', 'ensuring-equilibrium',
      SQ(6, 'How was it ensured that the metre stick was in equilibrium?'), 4, stem=[STEM1, APPLIED1],
      id='phys-2022-hl-q1-iv'),
    T('1v', 'Q1(v)', 'A', P(2, 'What was the principal advantage of ensuring that the metre stick was horizontal?'),
      [R('distances read are perpendicular/correct / trigonometry not needed', 4)], 'phys-1-2',
      'why-horizontal', SQ(6, 'What was the principal advantage of ensuring that the metre stick was horizontal?'), 4,
      stem=[STEM1, APPLIED1], id='phys-2022-hl-q1-v'),
    T('1vi', 'Q1(vi)', 'A', P(2, 'Calculate the net moment about the 0 cm position.'),
      [R('(2 × 0.321) + (1.2 × 0.506) + (3 × 0.722) = 3.4152 [N m]', 3,
         note_sel=S('[accept partial answer for 3, e.g. moment = force × distance, any moment calculated]')),
       R('(2.85 × 0.225) + (3.4 × 0.813) = 3.40545 [N m]', 3),
       R('3.4152 – 3.40545 = 0.00975 N m', 3, note_sel=S('[–1 if incorrect fulcrum used]'))],
      'phys-1-2', 'net-moment', SQ(6, 'Calculate the net moment about the 0 cm position.'), 9,
      stem=[STEM1, APPLIED1], fig='q1-table', id='phys-2022-hl-q1-vi'),
    T('1vii', 'Q1(vii)', 'A', P(2, 'Calculate the net vertical force acting on the metre stick.'),
      [R('2.85 + 3.4 – 2 – 3 – 1.2 = 0.05 N [upwards]', 3)], 'phys-1-2', 'net-vertical-force',
      SQ(6, 'Calculate the net vertical force acting on the metre stick.'), 3, stem=[STEM1, APPLIED1], fig='q1-table',
      id='phys-2022-hl-q1-vii',
      decision='The old card\'s only row was the ask itself; the row is the scheme\'s calculation.'),
    T('1viii', 'Q1(viii)', 'A', P(2, 'Explain how these results verify the laws of equilibrium.'),
      [anyn(None, 2, 4, steps=[4, 2], note=ORDERED.format(cell='[4 + 2]'),
            options=[S('net moment ≈ 0'), S('net force ≈ 0')])], 'phys-1-2', 'verifying-laws-of-equilibrium',
      SQ(6, 'Explain how these results verify the laws of equilibrium.'), 6, stem=[STEM1, APPLIED1], fig='q1-table',
      id='phys-2022-hl-q1-viii',
      decision='"[4 + 2]" against the two conditions, which the scheme prints in no order: a menu priced step by '
               'step.'),
    # ---------------------------------------------------------------- Q2 --
    T('2i', 'Q2(i)', 'A', P(3, 'State Boyle’s law.'),
      [R('p is inversely proportional to V / pV = constant', 4), R('for a fixed mass of gas at constant temperature', 2)],
      'phys-2-1', 'boyles-law', SQ(7, 'State Boyle’s law.'), 6, id='phys-2022-hl-q2-i',
      decision='[4 + 2] against the two lines: in the order printed.'),
    T('2ii', 'Q2(ii)', 'A', P(3, 'Draw a labelled diagram of how the apparatus was arranged in this experiment.'),
      [C('means of measuring p', 3), C('means of measuring V or l', 3), C('means of changing p or V or l', 3,
                                                                          note_sel=NOLABEL)],
      'phys-2-1', 'boyles-law-apparatus',
      SQ(7, 'Draw a labelled diagram of how the apparatus was arranged in this experiment.'), 9, stem=[STEM2],
      id='phys-2022-hl-q2-ii'),
    T('2iii', 'Q2(iii)', 'A', P(3, 'Why is it necessary for the column of air to have a uniform diameter?'),
      [R('so that V is proportional to l [state/imply]', 3)], 'phys-2-1', 'uniform-diameter',
      SQ(7, 'Why is it necessary for the column of air to have a uniform diameter?'), 3, stem=[STEM2],
      id='phys-2022-hl-q2-iii'),
    T('2iv', 'Q2(iv)', 'A', P(3, 'Draw a suitable graph to verify Boyle’s law.'),
      [C('values for 1/l or 1/p', 3, note=VALUES), C('labelled axes', 3), C('correct points plotted', 3),
       C('line of best fit', 3)], 'phys-2-1', 'boyles-law-graph',
      SQ(7, 'Draw a suitable graph to verify Boyle’s law.'), 12, stem=[STEM2, TABLE2], fig='q2iv-scheme-table',
      id='phys-2022-hl-q2-iv',
      decision='The scheme prints "values for 1/l or 1/p" over a table of the values: one criterion row in its words, '
               'the table the solution figure. The data table is lifted into the stem.'),
    T('2v', 'Q2(v)', 'A', P(3, 'Explain how your graph verifies Boyle’s law.'),
      [R('straight line through origin', 3)], 'phys-2-1', 'graph-verifies-boyles-law',
      SQ(7, 'Explain how your graph verifies Boyle’s law.'), 3, stem=[STEM2], id='phys-2022-hl-q2-v'),
    T('2vi', 'Q2(vi)', 'A', P(3, 'Which of the data points is inconsistent with the others?'),
      [R('the second data point, i.e. when l = 20.0 cm', 3)], 'phys-2-1', 'inconsistent-data-point',
      SQ(7, 'Which of the data points is inconsistent with the others?'), 3, stem=[STEM2, INCONSISTENT],
      fig='q2-table', id='phys-2022-hl-q2-vi'),
    T('2vii', 'Q2(vii)', 'A', P(3, 'How did you treat this data point when you drew your graph?'),
      [R('ignored it', 4)], 'phys-2-1', 'treating-the-inconsistent-point',
      SQ(7, 'How did you treat this data point when you drew your graph?'), 4, stem=[STEM2, INCONSISTENT],
      fig='q2-table', id='phys-2022-hl-q2-vii'),
    # ---------------------------------------------------------------- Q3 --
    T('3i', 'Q3(i)', 'A', P(3, 'Draw a labelled diagram of how the apparatus was arranged in this experiment.', nth=2),
      [R('transparent block', 3), R('ray box / laser / pins', 3),
       R('detail e.g. paper, ruler, protractor', 3, note_sel=NOLABEL)], 'phys-2-3', 'snells-law-apparatus',
      SQ(8, 'Draw a labelled diagram of how the apparatus was arranged in this experiment.'), 9, stem=[STEM3],
      id='phys-2022-hl-q3-i'),
    T('3ii', 'Q3(ii)', 'A', P(3, 'Describe how the student determined the angle of refraction.'),
      [anyn(None, 3, 3, note='The scheme prints "[any 3 × 3]".',
            options=[S('draw incident/emergent ray'), S('draw refracted ray'), S('draw normal [at point of incidence]'),
                     S('measure angle with protractor')])],
      'phys-2-3', 'measuring-angle-of-refraction',
      SQ(8, 'Describe how the student determined the angle of refraction.'), 9, stem=[STEM3], id='phys-2022-hl-q3-ii',
      decision='Four steps priced "[any 3 × 3]": a menu of three claims at 3.'),
    T('3iii', 'Q3(iii)', 'A', P(3, 'Draw a suitable graph to verify Snell’s law.'),
      [C('values for sin i and sin r', 3, note=VALUES), C('labelled axes', 3), C('correct points plotted', 3),
       C('line of best fit', 3)], 'phys-2-3', 'snells-law-graph',
      SQ(8, 'Draw a suitable graph to verify Snell’s law.'), 12, stem=[STEM3, TABLE3], fig='q3iii-scheme-table',
      id='phys-2022-hl-q3-iii',
      decision='The scheme prints "values for sin i and sin r" over a table of the values: one criterion row in its '
               'words, the table the solution figure. The data table is lifted into the stem.'),
    T('3iv', 'Q3(iv)', 'A', P(3, 'Use your graph to calculate the refractive index of the glass.'),
      [C('slope formula', 3), R('n = 1.4', 3)], 'phys-2-3', 'refractive-index-from-graph',
      SQ(8, 'Use your graph to calculate the refractive index of the glass.'), 6, stem=[STEM3], fig='q3-table',
      id='phys-2022-hl-q3-iv'),
    T('3v', 'Q3(v)', 'A', P(3, 'What would be observed if the angle of incidence was zero degrees?'),
      [R('no refraction / ray travels straight through', 4)], 'phys-2-3', 'zero-angle-of-incidence',
      SQ(8, 'What would be observed if the angle of incidence was zero degrees?'), 4, stem=[STEM3],
      id='phys-2022-hl-q3-v'),
    # ---------------------------------------------------------------- Q4 --
    T('4i', 'Q4(i)', 'A', P(4, 'Draw a labelled diagram of how the apparatus was arranged in this experiment.'),
      [R('tube', 3), C('means of changing length', 3), C('means of measuring length', 3),
       R('tuning fork[s]', 3, note_sel=NOLABEL)], 'phys-2-6', 'resonance-tube-apparatus',
      SQ(9, 'Draw a labelled diagram of how the apparatus was arranged in this experiment.'), 12, stem=[STEM4],
      id='phys-2022-hl-q4-i'),
    T('4ii', 'Q4(ii)', 'A', P(4, 'How did the student determine the length of the column of air for a particular',
                             'frequency?'),
      [anyn(None, 2, 3, note='The scheme prints "[any 2 × 3]".',
            options=[S('hold [vibrating] tuning fork over the mouth of the pipe'), S('change the length of the pipe'),
                     S('until [the loudest] sound is heard'), S('measure length from closed end to open end of the pipe')])],
      'phys-2-6', 'finding-resonant-length',
      SQ(9, 'How did the student determine the length of the column of air for a particular frequency?'), 6,
      stem=[STEM4], id='phys-2022-hl-q4-ii',
      decision='Four steps priced "[any 2 × 3]": a menu of two claims at 3.'),
    T('4iii', 'Q4(iii)', 'A', [P(4, 'Draw a graph to show the relationship between l and'),
                               P(4, '(Note: the line of best fit on your graph should not go through the origin.)',
                                 br=True)],
      [C('values for 1/f', 3, note=VALUES), C('labelled axes', 3), C('correct points plotted', 3),
       C('line of best fit', 3)], 'phys-2-6', 'length-against-one-over-f-graph',
      SQ(9, 'Draw a graph to show the relationship between l and'), 12, qfig='q4iii-question',
      fig='q4iii-scheme-table',
      decision='The bank had excluded this part for the stacked "1/f" in its ask. The ask ends in that fraction, '
               'which the text layer breaks: the question is shown as printed, Q4 with its table and parts (i) to '
               '(iii). The scheme prints "values for 1/f" over a table of the values: one criterion row in its '
               'words, the table the solution figure.'),
    T('4iv', 'Q4(iv)', 'A', P(4, 'Use your graph to calculate the speed of sound in air.'),
      [C('slope formula', 3), R('c = 4 × 85 = 340 m s⁻¹', 3)], 'phys-2-6', 'speed-of-sound-from-graph',
      SQ(9, 'Use your graph to calculate the speed of sound in air.'), 6, stem=[STEM4], fig='q4-table',
      id='phys-2022-hl-q4-iv'),
    T('4v', 'Q4(v)', 'A', P(4, 'Explain why the line of best fit on the graph does not go through the origin.'),
      [R('end correction term / wave exists above the opening of the pipe', 4)], 'phys-2-6', 'end-correction',
      SQ(9, 'Explain why the line of best fit on the graph does not go through the origin.'), 4, stem=[STEM4],
      source_pages=[4], id='phys-2022-hl-q4-v', decision=LINKED.format(w='"the graph"')),
    # ---------------------------------------------------------------- Q5 --
    T('5i', 'Q5(i)', 'A', P(4, 'Draw a labelled diagram of how the apparatus was arranged in this experiment.', nth=2),
      [R('heating coil', 3), R('power supply / battery', 3), R('ammeter in series', 3),
       R('thermometer', 3, note_sel=NOLABEL)], 'phys-3-3', 'joules-law-apparatus',
      SQ(10, 'Draw a labelled diagram of how the apparatus was arranged in this experiment.'), 12, stem=STEM5,
      id='phys-2022-hl-q5-i'),
    T('5ii', 'Q5(ii)', 'A', P(4, 'How was the mass of the olive oil determined?'),
      [R('subtract mass of empty calorimeter from mass of full calorimeter / tare mass of empty', 3,
         end='calorimeter before adding oil')], 'phys-2-1', 'mass-of-olive-oil',
      SQ(10, 'How was the mass of the olive oil determined?'), 3, stem=STEM5, id='phys-2022-hl-q5-ii'),
    T('5iii', 'Q5(iii)', 'A', P(4, 'Draw a suitable graph to verify Joule’s law.'),
      [C('values for I²', 3, note=VALUES), C('labelled axes', 3), C('correct points plotted', 3),
       C('line of best fit', 3)], 'phys-3-3', 'joules-law-graph',
      SQ(10, 'Draw a suitable graph to verify Joule’s law.'), 12, stem=STEM5 + TABLE5, fig='q5iii-scheme-table',
      id='phys-2022-hl-q5-iii',
      decision='The scheme prints "values for I²" over a table of I² and Δθ: one criterion row in its words, the table '
               'the solution figure. The data table is lifted into the stem.'),
    T('5iv', 'Q5(iv)', 'A', P(4, 'Calculate the slope of your graph.'),
      [C('slope formula', 3), R('m = 0.447 [no units required]', 3)], 'phys-3-3', 'slope-of-joules-law-graph',
      SQ(10, 'Calculate the slope of your graph.'), 6, stem=STEM5, fig='q5-table', id='phys-2022-hl-q5-iv'),
    T('5v', 'Q5(v)', 'A', P(4, 'Hence calculate the specific heat capacity of olive oil.'),
      [R('mcΔθ / I²Rt', 4), R('(0.447)(8.5)(180)/0.35 = 1954 J kg⁻¹ K⁻¹', 3)], 'phys-2-1',
      'specific-heat-capacity-of-olive-oil', SQ(10, 'Hence calculate the specific heat capacity of olive oil.'), 7,
      stem=STEM5, id='phys-2022-hl-q5-v'),
    # ============================================================ Section B ==
    # ---------------------------------------------------------------- Q6 --
    T('6a', 'Q6(a)', 'B', P(5, 'Iron has a density of 7.87 g cm⁻³.', 'the sphere in cm.'),
      [R('ρ = m/V or V = (4/3)πr³', 3), R('V = 500/7.87 = 63.53 [cm³]', 2), R('r = 2.475 [cm]', 2)], 'phys-1-2',
      'radius-of-iron-sphere', SQ(11, 'Iron has a density of 7.87 g cm⁻³.', 'the sphere in cm.'), 7,
      id='phys-2022-hl-q6-a'),
    T('6b', 'Q6(b)', 'B', P(5, 'Calculate how many electronvolts are in a kilowatt-hour.'),
      [R('1 eV = 1.6 × 10⁻¹⁹ [J]', 3), R('1 kW-hour = 1000(60)(60) = 3.6 × 10⁶ [J]', 2),
       R('3.6 × 10⁶/1.6 × 10⁻¹⁹ = 2.25 × 10²⁵', 2)], 'phys-1-4', 'electronvolts-in-a-kilowatt-hour',
      SQ(11, 'Calculate how many electronvolts are in a kilowatt-hour.'), 7, id='phys-2022-hl-q6-b',
      decision='[3 + 2] against the two conversions printed side by side: in the order printed.'),
    T('6c', 'Q6(c)', 'B', P(5, 'Draw a labelled diagram to show the forces acting on a piece of wood floating at rest.'),
      [anyn(None, 2, 3, steps=[3, 2], note=ORDERED.format(cell='[3 + 2]'),
            options=[S('weight labelled [downwards]'), S('buoyancy/upthrust labelled [upwards]')]),
       R('equal and opposite force vectors', 2)], 'phys-1-2', 'forces-on-floating-wood',
      SQ(11, 'Draw a labelled diagram to show the forces acting on a piece of wood floating at rest.'), 7,
      id='phys-2022-hl-q6-c',
      decision='"[3 + 2]" against the two forces printed side by side: a menu priced step by step; the vectors [2].'),
    T('6d', 'Q6(d)', 'B', P(5, 'State the thermometric property of (i) a thermocouple, (ii) a mercury thermometer.'),
      [pt(S('voltage/emf'), 4, label=S('(i)')), pt(S('height/length/volume'), 3, label=S('(ii)'))], 'phys-2-1',
      'thermometric-properties',
      SQ(11, 'State the thermometric property of (i) a thermocouple, (ii) a mercury thermometer.'), 7,
      id='phys-2022-hl-q6-d',
      decision='One of the eight 7-mark parts: one cell [4 + 3] prices (i) and (ii) together, (i) 4 and (ii) 3 in the '
               'order printed.'),
    T('6e', 'Q6(e)', 'B', P(5, 'Transverse waves can be polarised. Explain what is meant by polarisation.'),
      [R('oscillations/vibrations', 4), R('in one plane', 3)], 'phys-2-7', 'polarisation',
      SQ(11, 'Transverse waves can be polarised. Explain what is meant by polarisation.'), 7, id='phys-2022-hl-q6-e',
      decision='[4 + 3] against the two lines: in the order printed.'),
    T('6f', 'Q6(f)', 'B', P(5, 'The sound intensity is 0.18 mW m⁻² at a distance of 3 m', 'Calculate the power of the source.'),
      [R('P = IA', 3), R('A = 4π(3²) = 113.1 [m²]', 2), R('P = 0.02 W', 2)], 'phys-2-5', 'power-of-sound-source',
      SQ(11, 'The sound intensity is 0.18 mW m⁻² at a distance of 3 m', 'Calculate the power of the source.'), 7,
      id='phys-2022-hl-q6-f'),
    T('6g', 'Q6(g)', 'B', P(5, 'Describe how an insulated metal sphere can be charged by', 'induction using a nearby charged rod.'),
      [R('earth sphere [when rod is close]', 3), R('de-earth sphere [while rod is close]', 2),
       R('then remove rod', 2, note_sel=S('[–2 for each additional incorrect step]'))], 'phys-3-1',
      'charging-by-induction',
      SQ(12, 'Describe how an insulated metal sphere can be charged by induction using a nearby charged', 'rod.'), 7,
      id='phys-2022-hl-q6-g'),
    T('6h', 'Q6(h)', 'B', P(5, 'A current-carrying wire of length 20 cm is placed in a',
                           'Calculate the magnetic flux density of the field.'),
      [R('F = BIl', 4), R('B = 0.00013/(0.2 × 0.055) = 0.0118 T', 3)], 'phys-3-5', 'magnetic-flux-density',
      SQ(12, 'A current-carrying wire of length 20 cm is placed in a magnetic field.',
         'magnetic flux density of the field.'), 7, id='phys-2022-hl-q6-h'),
    T('6i', 'Q6(i)', 'B', P(5, 'A tungsten cube of side 2 cm has a resistance of 2.8 μΩ.', 'Calculate the resistivity of tungsten.'),
      [R('ρ = RA/l', 4), R('ρ = 0.0000028 × 0.02 = 5.6 × 10⁻⁸ Ω m', 3)], 'phys-3-3', 'resistivity-of-tungsten',
      SQ(12, 'A tungsten cube of side 2 cm has a resistance of 2.8 μΩ. Calculate the resistivity of tungsten.'), 7,
      id='phys-2022-hl-q6-i'),
    T('6j', 'Q6(j)', 'B', P(5, 'Describe how the Bohr model of the atom explains emission line spectra.'),
      [R('[electron] falling from one energy level to another / E₂ – E₁ / ΔE', 4),
       R('produces light of a [particular] frequency/wavelength/energy/colour/hf', 3)], 'phys-4-3',
      'bohr-model-line-spectra', SQ(12, 'Describe how the Bohr model of the atom explains emission line spectra.'), 7,
      id='phys-2022-hl-q6-j', decision='[4 + 3] against the two lines: in the order printed.'),
    T('6k', 'Q6(k)', 'B', P(5, 'What is thermionic emission? Where does it occur in an X-ray tube?'),
      [R('emission of electrons', 2), R('from a hot surface', 2), R('cathode', 3)], 'phys-4-2', 'thermionic-emission',
      SQ(12, 'What is thermionic emission? Where does it occur in an X-ray tube?'), 7, id='phys-2022-hl-q6-k'),
    T('6l', 'Q6(l)', 'B', P(5, 'Pair annihilation of an electron and a positron occurs in a positron emission tomography',
                           'Write an equation for this annihilation.'),
      [R('e⁻ + e⁺ / 2mₑc²', 4), R('= 2γ / 2hf', 3)], 'phys-4-5', 'pair-annihilation-equation',
      SQ(12, 'Pair annihilation of an electron and a positron occurs in a positron emission tomography',
         '(PET) scanner. Write an equation for this annihilation.'), 7, route='pair-annihilation',
      id='phys-2022-hl-q6-l',
      decision='Q6(l) prints two alternatives joined by "or": each is carded at the part\'s 7, as routes of the one '
               'leaf. [4 + 3] against the equation\'s two printed lines: in the order printed.'),
    T('6l2', 'Q6(l)', 'B', P(5, 'Draw the symbol for an AND gate. Write out the truth table for an AND gate.'),
      [pt(S('Draw the symbol for an AND gate. Write out the truth table for an AND gate.',
            after='(PET) scanner. Write an equation for this annihilation.', piece=1, psep='. Write'), 3,
          kind='criterion',
          note='The scheme draws the symbol (two printed forms, shown in the figure) and prints no words for it, '
               'only its cell [3].'),
       G('tokens', page=12, clip=(85, 584, 160, 603), expect='0 0 0', marks=1,
         note='The scheme prints the truth table without headings, each row two inputs and then the output, priced '
              '[4 × 1]: one mark per row.'),
       G('tokens', page=12, clip=(85, 603, 160, 622), expect='1 0 0', marks=1),
       G('tokens', page=12, clip=(85, 622, 160, 641), expect='0 1 0', marks=1),
       G('tokens', page=12, clip=(85, 641, 160, 660), expect='1 1 1', marks=1)],
      'phys-3-3', 'and-gate-symbol-and-truth-table',
      SQ(12, 'Draw the symbol for an AND gate. Write out the truth table for an AND gate.'), 7, route='and-gate',
      fig='q6l-scheme-gate',
      decision='The second alternative of Q6(l), which the old cards left out. The symbol is priced [3] and drawn in '
               'two forms with no words: one criterion row naming it in the scheme\'s own reprint, the drawing the '
               'solution figure. The truth table is priced [4 × 1]: one row per printed row, read from where its '
               'digits are printed.'),
    # ---------------------------------------------------------------- Q7 --
    T('7i', 'Q7(i)', 'B', P(6, 'State Hooke’s law.'),
      [pt(dslash('extension', '// F = –kx', 1), 2), pt(dslash('proportional to force', '// notation', 1), 2)],
      'phys-1-3', 'hookes-law', SQ(13, 'State Hooke’s law.'), 4, stem=[SPRING7], id='phys-2022-hl-q7-i',
      decision='The scheme sets the law in words and, after "//", as a formula with notation: answer variants, each '
               'on the scheme\'s own [2] per line.'),
    T('7ii', 'Q7(ii)', 'B', P(6, 'Calculate the elastic constant of the spring.'),
      [R('F = –kx', 2), R('(0.2)(9.8) = k(0.185 – 0.15)', 2), R('k = 56 N m⁻¹', 2)], 'phys-1-3', 'elastic-constant',
      SQ(13, 'Calculate the elastic constant of the spring.'), 6, stem=[SPRING7, G7], id='phys-2022-hl-q7-ii'),
    T('7iii', 'Q7(iii)', 'B', P(6, 'Calculate the period of oscillation of the object.'),
      [R('T = 2π/ω', 3), R('ω = √(k/m) or ω = √280 = 16.73 [s⁻¹]', 3), R('T = 2π/16.73 = 0.375 s', 3)], 'phys-1-3',
      'period-of-oscillation', SQ(13, 'Calculate the period of oscillation of the object.'), 9, stem=[SPRING7, SHM7],
      id='phys-2022-hl-q7-iii'),
    T('7iv', 'Q7(iv)', 'B', P(6, 'Calculate the maximum acceleration of the object.'),
      [R('a = –ω²x', 3), R('amax. = (280)(0.2 – 0.185) = 4.2 m s⁻²', 3)], 'phys-1-3', 'maximum-acceleration-shm',
      SQ(13, 'Calculate the maximum acceleration of the object.'), 6, stem=[SPRING7, SHM7], id='phys-2022-hl-q7-iv'),
    T('7v', 'Q7(v)', 'B', P(6, 'What is the speed of the body when it has maximum acceleration?'),
      [R('zero', 3)], 'phys-1-3', 'speed-at-maximum-acceleration',
      SQ(13, 'What is the speed of the body when it has maximum acceleration?'), 3, stem=[SPRING7, SHM7],
      id='phys-2022-hl-q7-v'),
    T('7vi', 'Q7(vi)', 'B', P(6, 'Derive an expression for the linear velocity of an object moving in circular motion in terms of',
                             'its angular velocity and the radius of the circle.'),
      [R('θ = s/r', 3), R('v = s/t = rθ/t', 3),
       R('ω = θ/t so v = rω', 3, note_sel=S('[accept v = rω as partial answer for 3]'))], 'phys-1-6',
      'deriving-v-equals-r-omega',
      SQ(13, 'Derive an expression for the linear velocity of an object moving in circular motion in terms of',
         'its angular velocity and the radius of the circle.'), 9, id='phys-2022-hl-q7-vi'),
    T('7viia', 'Q7(vii)(a)', 'B', dict(Q7VII, piece=1, psep=', (b)'),
      [R('T = 2π/ω', 3), R('ω = 2π/0.5 = 12.57 rad s⁻¹', 3)], 'phys-1-6', 'angular-velocity',
      SQ(13, 'Calculate (a) the angular velocity, (b) the linear velocity of the object.'), 6, stem=[SPRING7, CIRCLE7],
      id='phys-2022-hl-q7-vii',
      decision='The paper prints (a) and (b) inside one line, priced apart ([3] [3] and [3]): the question is the '
               'printed line cut at its own markers. ' + bundled('(a) and (b)', '(a)')),
    T('7viib', 'Q7(vii)(b)', 'B', [dict(Q7VII, piece=1, psep=' (a) the angular velocity, '),
                                   dict(Q7VII, piece=2, psep=' (a) the angular velocity, ')],
      [R('v = 0.11 × 12.57 = 1.38 m s⁻¹', 3)], 'phys-1-6', 'linear-velocity',
      SQ(13, 'Calculate (a) the angular velocity, (b) the linear velocity of the object.'), 3, stem=[SPRING7, CIRCLE7],
      decision='The paper prints (a) and (b) inside one line: the question is that line without (a)\'s words.'),
    T('7viii', 'Q7(viii)', 'B', P(6, 'Calculate the minimum tension in the string.'),
      [R('FC = mrω² / FC = mv²/r', 3), R('Tmin. = (0.2 × 0.11 × 12.56²) – (0.2 × 9.8) = 3.47 – 1.96 = 1.51 N', 3)],
      'phys-1-6', 'minimum-tension', SQ(13, 'Calculate the minimum tension in the string.'), 6,
      stem=[SPRING7, CIRCLE7, G7], id='phys-2022-hl-q7-viii'),
    T('7ix', 'Q7(ix)', 'B', P(6, 'Draw a labelled diagram of the forces acting on the object when the string has its',
                             'minimum tension.'),
      [R('weight acting downwards', 2,
         note_sel=S('[–2 for each additional incorrect force; ignore references to centripetal force]')),
       R('tension acting downwards', 2, note_sel=S('[ –1 if no label present on diagram]'))], 'phys-1-6',
      'forces-at-minimum-tension',
      SQ(13, 'Draw a labelled diagram of the forces acting on the object when the string has its', 'minimum tension.'),
      4, stem=[SPRING7, CIRCLE7], id='phys-2022-hl-q7-ix'),
    # ---------------------------------------------------------------- Q8 --
    T('8i', 'Q8(i)', 'B', P(7, 'Distinguish between conductors, insulators and semiconductors.'),
      [R('conductors are good at allowing current to flow / high conductivity / low resistivity', 2),
       R('insulators are poor at allowing current to flow / low conductivity / high resistivity', 2),
       R('semiconductors are in-between', 2)], 'phys-3-3', 'conductors-insulators-semiconductors',
      SQ(14, 'Distinguish between conductors, insulators and semiconductors.'), 6, id='phys-2022-hl-q8-i'),
    T('8ii', 'Q8(ii)', 'B', P(7, 'What is meant by doping?'),
      [R('addition of [a small amount of] impurity', 3), R('to increase conductivity / to decrease resistivity', 3)],
      'phys-3-3', 'doping', SQ(14, 'What is meant by doping?'), 6, stem=DOPING8, id='phys-2022-hl-q8-ii'),
    T('8iii', 'Q8(iii)', 'B', P(7, 'How does p-type doping differ from n-type doping?'),
      [R('p-type doping introduces [excess] holes / e.g. adding B', 3),
       R('n-type doping introduces [excess] electrons / e.g. adding P', 3)], 'phys-3-3', 'p-type-and-n-type-doping',
      SQ(14, 'How does p-type doping differ from n-type doping?'), 6, stem=DOPING8, id='phys-2022-hl-q8-iii'),
    T('8iv', 'Q8(iv)', 'B', P(7, 'Describe a depletion layer and explain how it forms.'),
      [R('insulating region / region with no free charge carriers', 3), R('between p-type and n-type semiconductors', 3),
       R('holes/electrons migrate', 3), R('and combine/neutralise each other', 3)], 'phys-3-3', 'depletion-layer',
      SQ(14, 'Describe a depletion layer and explain how it forms.'), 12, stem=[DEPLETION8], id='phys-2022-hl-q8-iv'),
    T('8v', 'Q8(v)', 'B', P(7, 'Indicate on a diagram the sections of a p-n junction that are positively charged, negatively',
                           'charged and neutral.'),
      [R('negatively charged in p-type close to the interface', 2),
       R('positively charged in n-type close to the interface', 2), R('neutral in remainder', 2)], 'phys-3-3',
      'charges-across-pn-junction',
      SQ(14, 'Indicate on a diagram the sections of a p-n junction that are positively charged, negatively',
         'charged and neutral.'), 6, stem=[DEPLETION8], fig='q8v-scheme', id='phys-2022-hl-q8-v',
      cells='The scheme prints a [2] on each of the three lines; the second and third share their baselines with the '
            'labels of the diagram drawn beside them ("+", "neutral"), so the reader attaches those two cells to the '
            'diagram, not to these rows.',
      decision='The scheme draws the junction with its charges and neutral regions (the solution figure).'),
    T('8vi', 'Q8(vi)', 'B', P(7, 'Draw a circuit diagram to show this arrangement.'),
      [R('diode in forward bias', 3), R('[variable] voltage source', 3)], 'phys-3-3', 'forward-bias-circuit',
      SQ(14, 'Draw a circuit diagram to show this arrangement.'), 6, stem=[JUNCTION8], source_pages=[7],
      id='phys-2022-hl-q8-vi', decision=LINKED.format(w='"a circuit diagram"')),
    T('8vii', 'Q8(vii)', 'B', P(7, 'Sketch a graph to show the variation of current with voltage for this arrangement.',
                               'the junction voltage on your graph.'),
      [C('axes labelled', 3), C('correct shape', 3), C('junction voltage indicated', 3)], 'phys-3-3',
      'forward-bias-graph',
      SQ(14, 'Sketch a graph to show the variation of current with voltage for this arrangement.',
         'the junction voltage on your graph.'), 9, stem=[JUNCTION8], fig='q8vii-scheme', id='phys-2022-hl-q8-vii',
      decision='The scheme names the graph\'s features as criteria and draws the sketch beside them (the solution '
               'figure).'),
    T('8viii', 'Q8(viii)', 'B', P(7, 'In many electric circuits a resistor is placed in series with a diode.', 'necessary.'),
      [R('to protect the diode / to limit the current / to prevent overheating', 5)], 'phys-3-3',
      'resistor-in-series-with-diode',
      SQ(14, 'In many electric circuits a resistor is placed in series with a diode.', 'necessary.'), 5,
      id='phys-2022-hl-q8-viii'),
    # ---------------------------------------------------------------- Q9 --
    T('9ai', 'Q9(a)(i)', 'B', P(8, 'Draw the electric field around the sphere.'),
      [R('radial shape of field', 3), R('direction of field towards centre', 3)], 'phys-3-2',
      'field-around-charged-sphere', SQ(15, 'Draw the electric field around the sphere.'), 6, stem=[SPHERE9],
      id='phys-2022-hl-q9a-i'),
    T('9aii', 'Q9(a)(ii)', 'B', P(8, 'Calculate the electric field strength at a distance of 3 cm from the surface of',
                                 'the sphere.'),
      [R('F = q₁q₂/4πεd²', 3), R('E = F/q', 3),
       R('E = (6 × 10⁻⁶)/(4π × 8.854 × 10⁻¹² × 0.055²) = 1.78 × 10⁷ N C⁻¹', 3)], 'phys-3-2',
      'electric-field-strength',
      SQ(15, 'Calculate the electric field strength at a distance of 3 cm from the surface of', 'the sphere.'), 9,
      stem=[SPHERE9], id='phys-2022-hl-q9a-ii'),
    T('9bi', 'Q9(b)(i)', 'B', P(8, 'Describe an experiment to demonstrate that a charged capacitor stores energy.'),
      [R('method to charge capacitor e.g. across battery', 4), R('method to discharge capacitor e.g. across bulb/buzzer', 4),
       C('observation', 4)], 'phys-3-2', 'capacitor-stores-energy',
      SQ(15, 'Describe an experiment to demonstrate that a charged capacitor stores energy.'), 12, stem=[CAP9],
      id='phys-2022-hl-q9b-i',
      decision='A "describe an experiment" part: two method rows with the scheme\'s examples, and "observation", '
               'which the scheme names without an answer.'),
    T('9biia', 'Q9(b)(ii)(a)', 'B', dict(Q9BII, piece=1, psep=', (b)'),
      [R('2W/V', 4)], 'phys-3-2', 'charge-on-capacitor-plate',
      SQ(15, 'In terms of some or all of the symbols given, write an expression for (a) the charge on',
         'each plate of the capacitor, (b) the distance between the plates.'), 4, stem=[CAP9, PLATES9],
      id='phys-2022-hl-q9b-ii',
      decision='The paper prints (a) and (b) inside one sentence, priced [4] each: the question is the printed '
               'sentence cut at its own markers. ' + bundled('(a) and (b)', '(a)')),
    T('9biib', 'Q9(b)(ii)(b)', 'B', [dict(Q9BII, piece=1, psep=' (a) the charge on each plate of the capacitor, '),
                                     dict(Q9BII, piece=2, psep=' (a) the charge on each plate of the capacitor, ')],
      [R('εAV²/2W', 4)], 'phys-3-2', 'distance-between-capacitor-plates',
      SQ(15, 'In terms of some or all of the symbols given, write an expression for (a) the charge on',
         'each plate of the capacitor, (b) the distance between the plates.'), 4, stem=[CAP9, PLATES9],
      decision='The paper prints (a) and (b) inside one sentence: the question is that sentence without (a)\'s words.'),
    T('9ci', 'Q9(c)(i)', 'B', P(8, 'Derive an expression for the effective resistance of two resistors in parallel.'),
      [R('IT = I₁ + I₂', 3), R('V/RT = V/R₁ + V/R₂', 3), R('1/RT = 1/R₁ + 1/R₂', 3)], 'phys-3-3',
      'resistors-in-parallel', SQ(15, 'Derive an expression for the effective resistance of two resistors in parallel.'),
      9, id='phys-2022-hl-q9c-i'),
    T('9ciia', 'Q9(c)(ii)(a)', 'B', dict(Q9CII, piece=1, psep=', (b)'),
      [R('RYZ = 1/(⅙ + ⅓) = 2 [Ω]', 3), R('RXYZ = 1 + 2 = 3 [Ω]', 3), R('I = 12/3 = 4 A', 3)], 'phys-3-3',
      'current-in-resistor-x', SQ(15, 'Calculate the current flowing', '(b) in resistor Y.'), 9, stem=[CIRCUIT9],
      fig='q9c-circuit',
      decision='The bank had left Q9(c)(ii) open. The paper prints (a) and (b) inside one line, priced apart: the '
               'question is the printed line cut at its own markers; the circuit is the figure.'),
    T('9ciib', 'Q9(c)(ii)(b)', 'B', [dict(Q9CII, piece=1, psep=' (a) in resistor X, '),
                                     dict(Q9CII, piece=2, psep=' (a) in resistor X, ')],
      [R('(4)(1/3) = 1.33 A', 3)], 'phys-3-3', 'current-in-resistor-y',
      SQ(15, 'Calculate the current flowing', '(b) in resistor Y.'), 3, stem=[CIRCUIT9], fig='q9c-circuit',
      decision='The paper prints (a) and (b) inside one line: the question is that line without (a)\'s words.'),
    # ---------------------------------------------------------------- Q10 --
    T('10ia', 'Q10(i)(a)', 'B', dict(Q10I, piece=1, psep=', (b)'),
      [R('[spontaneous] emission of [one or more types of] radiation', 3),
       R('from a nucleus', 3, note_sel=S('[–1 for “atom” instead of “nucleus”]'))], 'phys-4-4', 'radioactivity',
      SQ(16, 'What is meant by (a) radioactivity, (b) ionisation?',
         paired='The scheme reprints the whole line, (a) and (b); the card asks (a), the line cut at its own marker.'),
      6, stem=[AM10], id='phys-2022-hl-q10-i',
      decision='The paper prints (a) and (b) inside one line, priced apart ([3] [3] and [3]): the question is the '
               'printed line cut at its own markers. ' + bundled('(a) and (b)', '(a)')),
    T('10ib', 'Q10(i)(b)', 'B', [dict(Q10I, piece=1, psep=' (a) radioactivity, '),
                                 dict(Q10I, piece=2, psep=' (a) radioactivity, ')],
      [R('removing/adding electron(s) from/to an atom / charging a particle', 3)], 'phys-4-4', 'ionisation',
      SQ(16, 'What is meant by (a) radioactivity, (b) ionisation?'), 3, stem=[AM10],
      decision='The paper prints (a) and (b) inside one line: the question is that line without (a)\'s words.'),
    T('10ii', 'Q10(ii)', 'B', P(9, 'Write a nuclear equation for the conversion of plutonium–239 into plutonium–241.'),
      [G('equation', page=16, clip=(80, 238, 210, 262), expect='²³⁹₉₄Pu + 2¹₀n → ²⁴¹₉₄Pu', marks=6,
         note_sel=SPECIES, note_lead='The scheme prices the equation [(5 × 1) + 1].')],
      'phys-4-4', 'plutonium-239-to-241-equation',
      SQ(16, 'Write a nuclear equation for the conversion of plutonium–239 into plutonium–241.'), 6,
      stem=[AM10, PU10],
      decision='The bank had excluded this part: the scheme sets the equation in a doubled maths font. Read from '
               'where each nuclide\'s numbers are printed (GLYPHS sets each glyph by its id): one row at the printed '
               '[(5 × 1) + 1] = 6.'),
    T('10iii', 'Q10(iii)', 'B', P(9, 'Write a nuclear equation for the conversion of plutonium–241 into americium–241.'),
      [G('equation', page=16, clip=(80, 292, 210, 316), expect='²⁴¹₉₄Pu → ²⁴¹₉₅Am + ⁰₋₁e', marks=7,
         note_sel=SPECIES, note_lead='The scheme prices the equation [7 × 1].')],
      'phys-4-4', 'beta-decay-of-plutonium-241',
      SQ(16, 'Write a nuclear equation for the conversion of plutonium–241 into americium–241.'), 7,
      stem=[AM10, PU10],
      decision='The bank had excluded this part: the scheme sets the equation in a doubled maths font. Read from '
               'where each nuclide\'s numbers are printed (GLYPHS): one row at the printed [7 × 1] = 7.'),
    T('10iv', 'Q10(iv)', 'B', P(9, 'Outline the differences between nuclear fission and nuclear fusion.'),
      [R('fission is splitting of a nucleus', 3),
       R('fusion is joining of [two] nuclei', 3, note_sel=S('[–1 for “atom” instead of “nucleus” (once)]'))],
      'phys-4-6', 'fission-and-fusion', SQ(16, 'Outline the differences between nuclear fission and nuclear fusion.'),
      6, stem=[FISSION10], id='phys-2022-hl-q10-iv'),
    T('10v', 'Q10(v)', 'B', P(9, 'What is the function of a moderator?'),
      [R('slows down neutrons / increases the rate of fission', 4)], 'phys-4-6', 'function-of-moderator',
      SQ(16, 'What is the function of a moderator?'), 4, stem=[MODERATOR10], id='phys-2022-hl-q10-v'),
    T('10vi', 'Q10(vi)', 'B', P(9, 'State one example of a moderator.'),
      [R('water / graphite / beryllium', 4)], 'phys-4-6', 'example-of-moderator',
      SQ(16, 'State one example of a moderator.'), 4, stem=[MODERATOR10], id='phys-2022-hl-q10-vi'),
    T('10vii', 'Q10(vii)', 'B', P(9, 'Why are nuclear fusion reactors not yet viable?'),
      [R('too much energy needed [to overcome electrostatic repulsion between nuclei] /', 3, end='scarcity of tritium')],
      'phys-4-6', 'fusion-not-yet-viable', SQ(16, 'Why are nuclear fusion reactors not yet viable?'), 3,
      stem=[FISSION10], id='phys-2022-hl-q10-vii'),
    T('10viii', 'Q10(viii)', 'B', P(9, 'Why are the alpha particles produced in the detector not considered a health hazard?'),
      [R('easily stopped / not very penetrating / short range', 3)], 'phys-4-4', 'alpha-particles-not-a-hazard',
      SQ(16, 'Why are the alpha particles produced in the detector not considered a health hazard?'), 3,
      stem=DETECTOR10, id='phys-2022-hl-q10-viii'),
    T('10ix', 'Q10(ix)', 'B', P(9, 'Calculate the decay constant for americium–241.'),
      [R('T½ = (ln 2)/λ', 3), R('λ = 0.693/(432 × 365 × 24 × 60 × 60) = 5.09 × 10⁻¹¹ s⁻¹', 3)], 'phys-4-4',
      'decay-constant', SQ(16, 'Calculate the decay constant for americium–241.'), 6, stem=DETECTOR10,
      id='phys-2022-hl-q10-ix'),
    T('10x', 'Q10(x)', 'B', P(9, 'Calculate the activity of the americium in the smoke detector.'),
      [R('A = λN', 3), R('0.29 μg has (0.29 × 10⁻⁶/241)(6.0 × 10²³) = 7.22 × 10¹⁴ [nuclei]', 3),
       R('(5.09 × 10⁻¹¹) × (7.22 × 10¹⁴) = 3.67 × 10⁴ Bq [or s⁻¹]', 2)], 'phys-4-4', 'activity-of-smoke-detector',
      SQ(16, 'Calculate the activity of the americium in the smoke detector.'), 8, stem=DETECTOR10,
      id='phys-2022-hl-q10-x'),
    # ---------------------------------------------------------------- Q11 --
    T('11i', 'Q11(i)', 'B', P(10, 'What is meant by (a) heat capacity, (b) specific heat capacity?'),
      [pt(S('energy to change the temperature of an object by 1 K'), 6, label=S('(a)')),
       pt(S('energy to change the temperature of 1 kg', '// E/mΔθ', piece=[1, 1], psep=['//', ' [6 + 3]']), 3,
          label=S('(b)'))],
      'phys-2-1', 'heat-capacity-definitions', SQ(17, 'What is meant by (a) heat capacity, (b) specific heat capacity?'),
      9, stem=[BRONZE11], id='phys-2022-hl-q11-i',
      cells='The words side is priced "[6 + 3]", printed inside (b)\'s line; the [3] cells at the margin price the '
            '"//" formula side (E/Δθ, E/mΔθ, and "// notation [3]", whose cell is printed inside its line), the '
            'mutually exclusive alternative.',
      decision='The scheme sets both definitions in words, priced together [6 + 3] ((a) 6 and (b) 3 in the order '
               'printed), and after "//" as formulae with notation, [3] each: answer variants. One cell over (a) and '
               '(b) keeps the roman whole.'),
    T('11ii', 'Q11(ii)', 'B', P(10, 'Calculate the highest temperature the water could have reached.'),
      [R('mcΔθ', 6), R('(750)(4180)(x – 4) or (50)(8500)(280 – x)', 3), R('x = 36.95 °C', 3)], 'phys-2-1',
      'highest-water-temperature', SQ(17, 'Calculate the highest temperature the water could have reached.'), 12,
      stem=FULACHT11 + [DATA11], id='phys-2022-hl-q11-ii',
      decision='[6 + 3 + 3] against the three lines: in the order printed.'),
    T('11iii', 'Q11(iii)', 'B', P(10, 'Suggest a way of improving the design of the fulacht fiadh to make it more efficient.'),
      [R('e.g. lid, fire closer to the water etc.', 3)], 'phys-2-1', 'improving-the-fulacht-fiadh',
      SQ(17, 'Suggest a way of improving the design of the fulacht fiadh to make it more efficient.'), 3,
      stem=FULACHT11, id='phys-2022-hl-q11-iii'),
    T('11iv', 'Q11(iv)', 'B', P(10, 'Draw a labelled diagram to represent a stretched string vibrating at', 'its third harmonic.'),
      [anyn(None, 2, 4, steps=[4, 2], note=ORDERED.format(cell='[4 + 2]'),
            options=[S('node at both ends'), S('three anti-nodes')])], 'phys-2-6', 'third-harmonic-diagram',
      SQ(17, 'Draw a labelled diagram to represent a stretched string vibrating at its third harmonic.'), 6,
      stem=[LYRE11], id='phys-2022-hl-q11-iv',
      decision='"[4 + 2]" against the two features of the drawing, which the scheme prints in no order: a menu priced '
               'step by step.'),
    T('11v', 'Q11(v)', 'B', P(10, 'Calculate the tension that is applied to the string.'),
      [R('f = (1/2l)√(T/μ)', 6), R('μ = m/l [ = 0.00021/0.65 = 0.000323 kg m⁻¹]', 3), R('T = 29.1 N', 3)], 'phys-2-6',
      'tension-in-lyre-string', SQ(17, 'Calculate the tension that is applied to the string.'), 12,
      stem=[LYRE11, STRING11], id='phys-2022-hl-q11-v',
      decision='[6 + 3 + 3] against the three lines: in the order printed.'),
    T('11vi', 'Q11(vi)', 'B', P(10, 'Determine the frequency of the string if the tension is now reduced', 'by a factor of four.'),
      [R('220 Hz', 4, note_sel=S('[accept partial answer for 2, e.g. any use of factor of two]'))], 'phys-2-6',
      'frequency-with-quarter-tension',
      SQ(17, 'Determine the frequency of the string if the tension is now reduced by a factor of four.'), 4,
      stem=[STRING11], id='phys-2022-hl-q11-vi'),
    T('11vii', 'Q11(vii)', 'B', P(10, 'C–14 and C–12 are both isotopes of carbon. What are isotopes?'),
      [R('atoms with the same number of protons / atoms with the same atomic number / atoms', 3,
         end='of the same element'),
       R('with different number of neutrons / with different mass number', 3)], 'phys-4-4', 'isotopes',
      SQ(17, 'C–14 and C–12 are both isotopes of carbon. What are isotopes?'), 6, stem=[CARBON11],
      id='phys-2022-hl-q11-vii'),
    T('11viii', 'Q11(viii)', 'B', P(10, 'The ratio of C–14 to C–12 in a sample from an archaeological artefact is found to be one',
                                   'answer.'),
      [R('no', 2), R('two half-lives [> time since the beginning of the Bronze Age]', 2)], 'phys-4-4',
      'radiocarbon-dating-bronze-age',
      SQ(17, 'The ratio of C–14 to C–12 in a sample from an archaeological artefact is found to be one', 'answer.'), 4,
      stem=[BRONZE11, CARBON11, DATA11], id='phys-2022-hl-q11-viii'),
    # ---------------------------------------------------------------- Q12 --
    T('12ai', 'Q12(a)(i)', 'B', P(11, 'Draw a labelled diagram of their apparatus.'),
      [R('hydrogen discharge tube', 3), R('linear accelerator with voltage applied correctly', 3),
       R('target [at 45°]', 3), R('screen/scintillations/microscope', 3)], 'phys-4-5', 'cockcroft-walton-apparatus',
      SQ(18, 'Draw a labelled diagram of their apparatus.'), 12, stem=[CW12], id='phys-2022-hl-q12a-i'),
    T('12aii', 'Q12(a)(ii)', 'B', P(11, 'Write a nuclear equation for the interaction', 'between a proton and a nucleus of lithium–7.'),
      [G('equation', page=18, clip=(80, 224, 180, 247), expect='⁷₃Li + ¹₁p → 2⁴₂He', marks=9,
         note_sel=SPECIES, note_lead='The scheme prices the equation [9 × 1].')],
      'phys-4-5', 'proton-lithium-equation',
      SQ(18, 'Write a nuclear equation for the interaction between a proton and a nucleus of lithium–7.'), 9,
      stem=[CW12],
      decision='The bank had excluded this part: the scheme sets the equation in a doubled maths font. Read from '
               'where each nuclide\'s numbers are printed (GLYPHS): one row at the printed [9 × 1] = 9.'),
    T('12aiii', 'Q12(a)(iii)', 'B', P(11, 'Convert this mass to kg. (Give your answer to six decimal places.)'),
      [R('(1.007825)(1.6605402 × 10⁻²⁷) = 1.673534 × 10⁻²⁷ [kg]', 3)], 'phys-4-5', 'nuclide-mass-in-kg',
      SQ(18, 'Convert this mass to kg. (Give your answer to six decimal places.)'), 3, stem=[NUCLIDE12],
      id='phys-2022-hl-q12a-iii'),
    T('12aiv', 'Q12(a)(iv)', 'B', P(11, 'Explain the discrepancy between the value you have calculated and the value given for',
                                   'the mass of the proton on page 47 of the Formulae and Tables booklet.'),
      [R('the nuclide mass [on page 83] contains the mass of the electron', 3)], 'phys-4-5',
      'nuclide-mass-and-proton-mass',
      SQ(18, 'Explain the discrepancy between the value you have calculated and the value given for the',
         'mass of the proton on page 47 of the Formulae and Tables booklet.'), 3, stem=[NUCLIDE12],
      id='phys-2022-hl-q12a-iv'),
    T('12av', 'Q12(a)(v)', 'B', [CALC12, M('(v)', 11), P(11, 'the kinetic energy of the proton as it collided with the metal,')],
      [R('E = qV', 3), R('(1.60217653 × 10⁻¹⁹)(70000) = 1.12152357 × 10⁻¹⁴ J', 3)], 'phys-4-5',
      'kinetic-energy-of-proton', SQ(18, 'the kinetic energy of the proton as it collided with the metal,'), 6,
      stem=[CW12], id='phys-2022-hl-q12a-v'),
    T('12avi', 'Q12(a)(vi)', 'B', [CALC12, M('(vi)', 11), P(11, 'the mass lost (in kg) during the interaction,')],
      [R('7.016005 + 1.007825 – 2(4.002603) = 0.018624 [u]', 3),
       R('(0.018624)(1.6605402 × 10⁻²⁷) = 3.09259007 × 10⁻²⁹ [kg]', 3)], 'phys-4-5', 'mass-lost',
      SQ(18, 'the mass lost (in kg) during the interaction,'), 6, stem=[CW12], id='phys-2022-hl-q12a-vi'),
    T('12avii', 'Q12(a)(vii)', 'B', [CALC12, M('(vii)', 11), P(11, 'the energy produced (in J) during the interaction,')],
      [R('E = mc²', 3), R('(3.09259007 × 10⁻²⁹)(2.99792458 × 10⁸)² = 2.77948134 × 10⁻¹² [J]', 3)], 'phys-4-5',
      'energy-produced', SQ(18, 'the energy produced (in J) during the interaction,'), 6, stem=[CW12],
      id='phys-2022-hl-q12a-vii'),
    T('12aviii', 'Q12(a)(viii)', 'B', [CALC12, M('(viii)', 11),
                                       P(11, 'the speed of the alpha particles formed during the interaction.')],
      [R('E = ½mv²', 3), R('v = 2.05 × 10⁷ m s⁻¹', 3)], 'phys-4-5', 'speed-of-alpha-particles',
      SQ(18, 'the speed of the alpha particles formed during the interaction.'), 6, stem=[CW12],
      id='phys-2022-hl-q12a-viii'),
    T('12aix', 'Q12(a)(ix)', 'B', P(11, 'A proton may be classified as a hadron. Explain why.'),
      [R('it experiences the strong force / it is composed of quarks', 3)], 'phys-4-5', 'proton-is-a-hadron',
      SQ(18, 'A proton may be classified as a hadron. Explain why.'), 3, id='phys-2022-hl-q12a-ix'),
    T('12ax', 'Q12(a)(x)', 'B', P(11, 'A proton may also be classified as a baryon. Explain why.'),
      [R('baryons are composed of three quarks', 2)], 'phys-4-5', 'proton-is-a-baryon',
      SQ(18, 'A proton may also be classified as a baryon. Explain why.'), 2, id='phys-2022-hl-q12a-x'),
    T('12bi', 'Q12(b)(i)', 'B', P(12, 'What is electric current?'),
      [R('the flow of charge', 3)], 'phys-3-3', 'electric-current', SQ(19, 'What is electric current?'), 3,
      stem=[GALV12], id='phys-2022-hl-q12b-i'),
    T('12bii', 'Q12(b)(ii)', 'B', P(12, 'Draw a labelled diagram of a moving-coil galvanometer.'),
      [R('magnet', 3), R('coil', 3), R('[soft] iron core', 3), R('scale and pointer', 3, note_sel=NOLABEL)],
      'phys-3-5', 'galvanometer-diagram', SQ(19, 'Draw a labelled diagram of a moving-coil galvanometer.'), 12,
      stem=[GALV12], id='phys-2022-hl-q12b-ii'),
    T('12biii', 'Q12(b)(iii)', 'B', P(12, 'Describe, with the aid of your diagram, the principle of',
                                     'operation of a moving-coil galvanometer.'),
      [R('current in coil', 3), R('force/torque', 3), R('deflection of pointer', 3)], 'phys-3-5',
      'galvanometer-principle',
      SQ(19, 'Describe, with the aid of your diagram, the principle of operation of a moving-coil', 'galvanometer.'), 9,
      stem=[GALV12], id='phys-2022-hl-q12b-iii'),
    T('12biv', 'Q12(b)(iv)', 'B', P(12, 'Draw a circuit diagram to demonstrate how a galvanometer can be converted into an',
                                   'ammeter.'),
      [R('[low resistance] resistor/shunt', 3), R('in parallel with galvanometer', 3)], 'phys-3-3',
      'galvanometer-to-ammeter',
      SQ(19, 'Draw a circuit diagram to demonstrate how a galvanometer can be converted into an', 'ammeter.'), 6,
      stem=[GALV12], source_pages=[12], id='phys-2022-hl-q12b-iv', decision=LINKED.format(w='"a circuit diagram"')),
    T('12bv', 'Q12(b)(v)', 'B', P(12, 'Draw a circuit diagram to demonstrate how a galvanometer can be converted into an',
                                 'ohmmeter.', nth=2),
      [R('variable resistor in series with galvanometer', 3), R('power supply', 3)], 'phys-3-3',
      'galvanometer-to-ohmmeter',
      SQ(19, 'Draw a circuit diagram to demonstrate how a galvanometer can be converted into an', 'ohmmeter.', nth=2), 6,
      stem=[GALV12], source_pages=[12], id='phys-2022-hl-q12b-v', decision=LINKED.format(w='"a circuit diagram"')),
    T('12bvi', 'Q12(b)(vi)', 'B', P(12, 'A galvanometer has a full scale deflection of 50 mA and a resistance of 0.7 Ω.',
                                   'into a voltmeter which can read up to 10 V.'),
      [R('V = IR', 3),
       R('10 ÷ 0.05 = 200 [Ω]', 3, route='side-a'), R('200 – 0.7 = 199.3 Ω', 3, route='side-a'),
       pt(S('// 10 – (0.05 × 0.7) = 9.965 [V]', piece=2, psep='//'), 3, route='side-b'),
       pt(S('// 9.965 ÷ 0.05 = 199.3 Ω', piece=2, psep='//'), 3, route='side-b')],
      'phys-3-3', 'multiplier-resistance',
      SQ(19, 'A galvanometer has a full scale deflection of 50 mA and a resistance of 0.7 Ω.',
         'into a voltmeter which can read up to 10 V.'), 9, stem=[MULT12], id='phys-2022-hl-q12b-vi',
      decision='"V = IR" is common; the scheme then prints two methods side by side, separated by "//": routes inside '
               'the card, each [3] [3].'),
    T('12bvii', 'Q12(b)(vii)', 'B', P(12, 'Explain, with the aid of a labelled diagram, how a loudspeaker produces sound.'),
      [R('current in the coil', 3), R('creates a magnetic field', 3),
       R('force produced from the interaction between the two magnetic fields', 3),
       R('cone vibrates [to produce sound]', 2, note_sel=NOLABEL)], 'phys-3-5', 'loudspeaker',
      SQ(19, 'Explain, with the aid of a labelled diagram, how a loudspeaker produces sound.'), 11, stem=[SPEAKER12],
      id='phys-2022-hl-q12b-vii'),
    # ---------------------------------------------------------------- Q13 --
    T('13i', 'Q13(i)', 'B', P(13, 'Diffraction is one of the wave properties of light. What is meant by diffraction?'),
      [R('spreading [of a wave]', 4), R('around an obstacle / through a gap', 3)], 'phys-2-3', 'diffraction',
      SQ(20, 'Diffraction is one of the wave properties of light. What is meant by diffraction?'), 7,
      id='phys-2022-hl-q13-i', decision='[4 + 3] against the two lines: in the order printed.'),
    T('13iia', 'Q13(ii)(a)', 'B', WAVE13,
      [R('light source', 2), R('diffraction grating', 2), R('screen/spectrometer', 2, note_sel=NOLABEL)], 'phys-2-6',
      'wave-nature-of-light-apparatus',
      SQ(20, 'Draw a labelled diagram of an experiment to demonstrate the wave nature of light.'), 6,
      decision='The old card bundled (b) and (c) and left (a) out; the scheme prices (a), (b) and (c) apart.'),
    T('13iib', 'Q13(ii)(b)', 'B', P(13, 'What is observed in this experiment?'),
      [R('series of fringes', 4)], 'phys-2-6', 'fringes-observed', SQ(20, 'What is observed in this experiment?'), 4,
      stem=[M('(a)', 13), WAVE13], id='phys-2022-hl-q13-ii-bc', decision=bundled('(b) and (c)', '(b)')),
    T('13iic', 'Q13(ii)(c)', 'B', P(13, 'How do the observations demonstrate the wave nature of light?'),
      [R('interference', 4)], 'phys-2-6', 'interference-shows-wave-nature',
      SQ(20, 'How do the observations demonstrate the wave nature of light?'), 4, stem=[M('(a)', 13), WAVE13]),
    T('13iii', 'Q13(iii)', 'B', P(13, 'The eyepiece lens of Huygens’ telescope was a converging lens arranged so as to',
                                 'produce a virtual image.', end_nth=2),
      [R('converging lens', 2), R('object inside focal point', 2), R('apparent intersection of rays to form virtual image', 3)],
      'phys-2-3', 'virtual-image-ray-diagram',
      SQ(20, 'The eyepiece lens of Huygens’ telescope was a converging lens arranged so as to produce a', 'image.'), 7,
      id='phys-2022-hl-q13c-iii',
      decision='The old card cited Q13(iii) under the id "q13c-iii" and carried two of the three rows; the third '
               '(apparent intersection of rays [3]) is added.'),
    T('13iv', 'Q13(iv)', 'B', P(13, 'The pendulum of Huygens’ clock oscillated with a period of 2 s.', 'this pendulum.'),
      [R('T = 2π√(l/g)', 4), R('l = 0.993 m', 3)], 'phys-1-5', 'length-of-pendulum',
      SQ(20, 'The pendulum of Huygens’ clock oscillated with a period of 2 s.', 'pendulum.'), 7, stem=[DATA13],
      id='phys-2022-hl-q13-iv'),
    T('13va', 'Q13(v)(a)', 'B', [CALC13, M('(a)', 13), P(13, 'the mass of Saturn,')],
      [R('T² = 4π²R³/GM', 6),
       pt(S('R = 1.16 × 10⁹ + 58200000 + 2570000 = 1.22 × 10⁹ [m] or', 'T = 15.9 × 24 × 60 × 60 = 1373760 [s]'), 3),
       R('M = 4π²(1.22 × 10⁹)³/(6.6742 × 10⁻¹¹ × 1373760²) = 5.7 × 10²⁶ kg', 3)], 'phys-1-5', 'mass-of-saturn',
      SQ(20, 'the mass of Saturn,'), 12, stem=[TITAN13, DATA13],
      decision='The old cards left (a) out. [6 + 3 + 3] against the formula, the "R ... or T ..." step (one row, '
               'its "or" kept) and the answer: in the order printed.'),
    T('13vb', 'Q13(v)(b)', 'B', [CALC13, M('(b)', 13), P(13, 'the acceleration due to gravity on the surface of Saturn,')],
      [R('g = GM/d²', 3), R('g = (6.6742 × 10⁻¹¹ × 5.7 × 10²⁶)/(58200000)² = 11.2 m s⁻²', 3)], 'phys-1-5',
      'gravity-on-saturn', SQ(20, 'the acceleration due to gravity on the surface of Saturn,'), 6,
      stem=[TITAN13, DATA13], id='phys-2022-hl-q13-v-b'),
    T('13vc', 'Q13(v)(c)', 'B', [CALC13, M('(c)', 13),
                                 P(13, 'the period that Huygens’ clock would have on the surface of Saturn.')],
      [R('T = 2π√(0.993/11.2) = 1.87 s', 3)], 'phys-1-5', 'pendulum-period-on-saturn',
      SQ(20, 'the period that Huygens’ clock would have on the surface of Saturn.'), 3, stem=[TITAN13, DATA13],
      id='phys-2022-hl-q13-v-c'),
    # ---------------------------------------------------------------- Q14 --
    T('14ai', 'Q14(a)(i)', 'B', P(14, 'Distinguish between a vector and scalar.'),
      [R('vector has [magnitude and] direction', 2), R('scalar has magnitude only / scalar has no direction', 2)],
      'phys-1-1', 'vector-and-scalar', SQ(21, 'Distinguish between a vector and scalar.'), 4,
      id='phys-2022-hl-q14a-i'),
    T('14aii', 'Q14(a)(ii)', 'B', P(14, 'Draw a labelled diagram of the arrangement of the apparatus in an experiment to find',
                                   'the resultant of two vectors.'),
      [pt(S('three newtonmeters / three systems of weights and pulleys / three displacements [3]', piece=1,
            psep=' [3]'), 3),
       C('correct arrangement', 3)], 'phys-1-2', 'resultant-of-two-vectors-apparatus',
      SQ(21, 'Draw a labelled diagram of the arrangement of the apparatus in an experiment to find',
         'the resultant of two vectors.'), 6, id='phys-2022-hl-q14a-ii',
      cells='The first line\'s [3] is printed inside the line\'s own text ("... three displacements [3]"), where the '
            'reader keeps it; only the second line\'s [3] stands in the margin.',
      decision='The scheme prices the apparatus [3] (three alternatives, one row) and "correct arrangement" [3].'),
    T('14aiii', 'Q14(a)(iii)', 'B', P(14, 'Resolve the velocity into horizontal and vertical components.'),
      [R('vH = 150cos20° [= 141 m s⁻¹]', 3), R('vV = 150sin20° [= 51.3 m s⁻¹]', 3)], 'phys-1-1',
      'resolving-velocity', SQ(21, 'Resolve the velocity into horizontal and vertical components.'), 6,
      stem=[PROJ14], id='phys-2022-hl-q14a-iii'),
    T('14aiv', 'Q14(a)(iv)', 'B', P(14, 'Calculate the magnitude and direction of the velocity of the object after 8 s.'),
      [R('vH = 150cos20° [= 141 m s⁻¹]', 4), R('v = u + at / vV = 51.3 – (9.8 × 8) = –27.1 [m s⁻¹]', 4),
       R('|v| = 143.5 m s⁻¹', 2), R('10.9° [below the horizontal]', 2)], 'phys-1-1', 'velocity-after-8-seconds',
      SQ(21, 'Calculate the magnitude and direction of the velocity of the object after 8 s.'), 12,
      stem=[PROJ14, G14], id='phys-2022-hl-q14a-iv'),
    T('14bi', 'Q14(b)(i)', 'B', P(14, 'What is the Doppler effect?'),
      [R('[apparent] change in frequency [of a wave]', 3),
       R('due to the [relative] motion between the source and the observer', 3)], 'phys-2-7', 'doppler-effect',
      SQ(21, 'What is the Doppler effect?'), 6, id='phys-2022-hl-q14b-i'),
    T('14bii', 'Q14(b)(ii)', 'B', P(14, 'Describe, with the aid of labelled diagrams, how the Doppler', 'effect occurs.'),
      [R('concentric/non-concentric circles drawn [representing wavefronts]', 3),
       R('motion of wave source towards/away from observer', 3),
       R('shorter wavelength as source approaches observer [or vice versa]', 2),
       R('therefore greater frequency [or vice versa]', 2)], 'phys-2-7', 'how-the-doppler-effect-occurs',
      SQ(21, 'Describe, with the aid of labelled diagrams, how the Doppler effect occurs.'), 10,
      id='phys-2022-hl-q14b-ii', decision='The old card left out the fourth row (therefore greater frequency [2]).'),
    T('14biii', 'Q14(b)(iii)', 'B', P(14, 'Calculate the frequency Pierre observes after 3 seconds.'),
      [R('v = u + at [ = (9.8)(3) = 29.4 m s⁻¹]', 6), R('f’ = fc/(c ± u)', 3), R('f’ = 460.2 Hz', 3)], 'phys-2-7',
      'frequency-of-falling-toy', SQ(21, 'Calculate the frequency Pierre observes after 3 seconds.'), 12,
      stem=PIERRE14, id='phys-2022-hl-q14b-iii',
      decision='[6 + 3 + 3] against the three lines: in the order printed.'),
    T('14ci', 'Q14(c)(i)', 'B', P(15, 'Describe a laboratory experiment to demonstrate the photoelectric effect.'),
      [R('apparatus [e.g. gold leaf electroscope, metal plate, light source]', 3),
       R('method [e.g. charge electroscope, place plate on cap, shine light on plate]', 3),
       R('observation [e.g. leaves collapse]', 3)], 'phys-4-2', 'photoelectric-effect-experiment',
      SQ(22, 'Describe a laboratory experiment to demonstrate the photoelectric effect.'), 9, stem=[PHOTO14],
      id='phys-2022-hl-q14c-i'),
    T('14cii', 'Q14(c)(ii)', 'B', P(15, 'Calculate the maximum speed of the emitted electrons.'),
      [R('hf = Φ + ½mv²', 6), R('c = fλ or f = (3 × 10⁸)/(450 ×10⁻⁹) = 6.67 × 10¹⁴ [Hz]', 3),
       R('Φ = (2.4)(1.6 ×10⁻¹⁹)= 3.84 ×10⁻¹⁹ [J]', 3), R('v = 3.56 ×10⁵ m s⁻¹', 3)], 'phys-4-2',
      'maximum-speed-of-photoelectrons', SQ(22, 'Calculate the maximum speed of the emitted electrons.'), 15,
      stem=[LIGHT14], id='phys-2022-hl-q14c-ii',
      decision='[6 + 3 + 3 + 3] against the four lines: in the order printed.'),
    T('14ciii', 'Q14(c)(iii)', 'B', P(15, 'Explain these observations.'),
      [R('incident energy decreases', 2),
       R('until the incident energy is below the work function / until the incident frequency', 2,
         end='is below the threshold frequency')], 'phys-4-2', 'threshold-frequency',
      SQ(22, 'Explain these observations.'), 4, stem=[LIGHT14, OBSERVED14], id='phys-2022-hl-q14c-iii'),
    T('14di', 'Q14(d)(i)', 'B', P(15, 'State the laws of electromagnetic induction.'),
      [pt(dslash('induced emf', '// E = dφ/dt', 1), 3),
       pt(dslash('proportional to rate of change of flux', '// notation', 1), 3),
       R('direction of induced current/emf', 3), R('is such as to oppose the change that caused it', 3)],
      'phys-3-6', 'laws-of-electromagnetic-induction', SQ(22, 'State the laws of electromagnetic induction.'), 12,
      id='phys-2022-hl-q14d-i',
      decision='Faraday\'s law is set in words and, after "//", as a formula with notation: answer variants, each on '
               'the scheme\'s own [3] per line; Lenz\'s law\'s two lines are common to both.'),
    T('14dii', 'Q14(d)(ii)', 'B', P(15, 'Describe what is observed when a sheet of copper', 'this observation.'),
      [R('amplitude of oscillations decreases', 4), R('[magnetic field from induced] currents in copper', 4)],
      'phys-3-6', 'magnet-over-copper-sheet',
      SQ(22, 'Describe what is observed when a sheet of copper metal is placed under the oscillating', 'magnet.'),
      8, stem=[MAGNET14], id='phys-2022-hl-q14d-ii'),
    T('14diii', 'Q14(d)(iii)', 'B', P(15, 'Describe what would be observed if instead of the', 'Explain this observation.'),
      [R('oscillations continue', 4), R('no currents flow in plastic', 4)], 'phys-3-6', 'magnet-over-plastic-sheet',
      SQ(22, 'Describe what would be observed if instead of the copper, a sheet of plastic was',
         'placed under the oscillating magnet. Explain this observation.'), 8, stem=[MAGNET14],
      id='phys-2022-hl-q14d-iii'),
]

ANSWER_VARIANTS = {
    '7i': [
        ('words', 'In words', [pt(dslash('extension', '// F = –kx', 1), 2),
                               pt(dslash('proportional to force', '// notation', 1), 2)]),
        ('formula', 'As a formula', [pt(dslash('extension', '// F = –kx', 2), 2),
                                     pt(dslash('proportional to force', '// notation', 2), 2, kind='criterion',
                                        note=CRIT)]),
    ],
    '11i': [
        ('words', 'In words', [
            pt(S('energy to change the temperature of an object by 1 K'), 6, label=S('(a)')),
            pt(S('energy to change the temperature of 1 kg', '// E/mΔθ', piece=[1, 1], psep=['//', ' [6 + 3]']), 3,
               label=S('(b)'))]),
        ('formula', 'As a formula', [
            pt(S('// E/Δθ', piece=2, psep='//'), 3, label=S('(a)')),
            pt(S('energy to change the temperature of 1 kg', '// E/mΔθ', piece=2, psep='//'), 3, label=S('(b)')),
            pt(S('// notation [3]', piece=[2, 1], psep=['//', ' [']), 3, kind='criterion', note=CRIT)]),
    ],
    '14di': [
        ('words', 'In words', [pt(dslash('induced emf', '// E = dφ/dt', 1), 3),
                               pt(dslash('proportional to rate of change of flux', '// notation', 1), 3),
                               R('direction of induced current/emf', 3),
                               R('is such as to oppose the change that caused it', 3)]),
        ('formula', 'As a formula', [pt(dslash('induced emf', '// E = dφ/dt', 2), 3),
                                     pt(dslash('proportional to rate of change of flux', '// notation', 2), 3,
                                        kind='criterion', note=CRIT),
                                     R('direction of induced current/emf', 3),
                                     R('is such as to oppose the change that caused it', 3)]),
    ],
}
RETAINED = {}
WITHDRAW = {}

FIGURES = {
    # key suffix: (doc, page, rect in PDF points, credit, letters, alt, solution)
    'q1-table': ('paper', 2, (84, 410, 513, 517), SEC, [],
                 'Table of the recorded data: position on metre stick 22.5 cm, 32.1 cm, 72.2 cm, 81.3 cm; force (N) '
                 '2.85, 2.00, 3.00, 3.40; direction upwards, downwards, downwards, upwards.', False),
    'q2-table': ('paper', 3, (98, 120, 499, 178), SEC, [],
                 'Table of the recorded data: l (cm) 15.0, 20.0, 25.0, 30.0, 35.0, 40.0; p (kPa) 360, 227, 214, 178, '
                 '154, 136.', False),
    'q2iv-scheme-table': ('scheme', 7, (90, 384, 505, 433), SEC, [],
                          "The marking scheme's table of values: 1/l (cm⁻¹) 0.067, 0.05, 0.04, 0.033, 0.029, 0.025; "
                          "1/p (kPa⁻¹) 0.0028, 0.0044, 0.0047, 0.0056, 0.0065, 0.0074.", True),
    'q3-table': ('paper', 3, (98, 485, 498, 542), SEC, [],
                 'Table of the recorded data: i (degrees) 30, 40, 50, 60, 70, 80; r (degrees) 19, 27, 32, 36, 40, 44.',
                 False),
    'q3iii-scheme-table': ('scheme', 8, (98, 386, 492, 426), SEC, [],
                           "The marking scheme's table of values: sin i 0.5, 0.64, 0.77, 0.87, 0.94, 0.98; sin r 0.33, "
                           "0.45, 0.53, 0.59, 0.64, 0.69.", True),
    'q4iii-question': ('paper', 4, (25, 52, 548, 304), SEC, [],
                       'The printed Question 4 up to part (iii): the speed of sound experiment, its table of f (Hz) 256, '
                       '288, 320, 341, 384, 480 against l (cm) 29.2, 25.5, 22.6, 20.9, 18.1, 13.7, and parts (i) to (iii), '
                       '(iii) asking for a graph of l against 1 over f, set as a fraction, with its note that the line '
                       'of best fit should not go through the origin.', False),
    'q4iii-scheme-table': ('scheme', 9, (98, 437, 494, 462), SEC, [],
                           "The marking scheme's table of values: 1/f (Hz⁻¹) 0.0039, 0.0035, 0.0031, 0.0029, 0.0026, "
                           "0.0021.", True),
    'q4-table': ('paper', 4, (98, 136, 499, 193), SEC, [],
                 'Table of the recorded data: f (Hz) 256, 288, 320, 341, 384, 480; l (cm) 29.2, 25.5, 22.6, 20.9, 18.1, '
                 '13.7.', False),
    'q5iii-scheme-table': ('scheme', 10, (98, 445, 500, 496), SEC, [],
                           "The marking scheme's table of values: I² (A²) 1.0, 4.0, 9.0, 12.25, 16.0, 20.25; Δθ (K) 2.2, "
                           "9.1, 19.6, 27.4, 36.1, 45.1.", True),
    'q5-table': ('paper', 4, (98, 528, 499, 613), SEC, [],
                 'Room temperature = 17.0 °C, then the table of the recorded data: I (A) 1.0, 2.0, 3.0, 3.5, 4.0, 4.5; '
                 'θ (°C) 19.2, 26.1, 36.6, 44.4, 53.1, 62.1.', False),
    'q6l-scheme-gate': ('scheme', 12, (80, 521, 272, 584), SEC, [],
                        "The marking scheme's two drawings of the AND gate symbol, separated by a slash: a D-shaped gate "
                        "with two inputs on the left and one output on the right, and a square box marked & with two "
                        "inputs and one output.", True),
    'q8v-scheme': ('scheme', 14, (364, 428, 494, 491), SEC, ['P', 'N'],
                   "The marking scheme's diagram of a p-n junction: a block with P on the left and N on the right, a "
                   "column of minus signs on the p side of the interface and a column of plus signs on the n side, and "
                   "arrows from the word neutral to the outer part of each side.", True),
    'q8vii-scheme': ('scheme', 14, (261, 606, 356, 678), SEC, ['I', 'V'],
                     "The marking scheme's sketch: current I against voltage V, the current staying at zero and then "
                     "rising in a dashed curve, with an arrow pointing down to the voltage where the curve leaves the "
                     "axis.", True),
    'q9c-circuit': ('paper', 8, (145, 340, 450, 574), SEC, ['X', 'Y', 'Z'],
                    'Circuit diagram: a 12 V battery in a loop with a resistor X = 1 Ω in series with two resistors in '
                    'parallel, Y = 6 Ω on the upper branch and Z = 3 Ω on the lower branch.', False),
}
