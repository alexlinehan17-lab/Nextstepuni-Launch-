"""Physics 2025 Higher Level — reviewed task ledger, correcting the sitting in place.

Independent visual sweep (2026-10-28), every page rendered and read:
  * The paper (LC021ALP000EV), 20 pages: p1 cover (the 2025 papers were
    adjusted for disruption to learning), p2-p6 Section A Questions 1-5 (any
    three, 40 marks each), p7-p18 Section B Questions 6-14 (any five, 56 marks
    each), p19 acknowledgements (images on pages 7, 9 and 17), p20 back cover.
  * The marking scheme, 27 pages: p1 cover, p2 note on published schemes, p3
    marking conventions (solidus, double solidus), p4 annotations, p5 Irish
    bonus table, p6-p25 Questions 1-14 ("Page 5" to "Page 24"), p26 blank, p27
    back cover.

Every printed ask is carded. Section A prints a group mark after a run of
romans ("(15)" closing Q1(i)-(iv)): GROUP_TOTALS. Q6 is any eight of (a)-(l)
at 7 each (8 x 7): one card per letter, (g) and (h) each one card over their
two romans because the scheme prices each letter in one cell ([2 + 2 + 2 + 1],
[4 + 3]). Q12 is either (a) or (b), and Q14 any two of (a)-(d): every part is
carded. The scheme prints a mark cell against every answer line; a cell
"[4 + 2]" set against two answer lines is carded positionally, the first line
4 and the second 2.

Formulae the scheme sets as stacked fractions are read with G('fraction')
(numerator and denominator from where they are printed, written with a
solidus); nuclear equations, whose nuclides carry their mass and atomic numbers
stacked, are read on their main line with G('tokens') and shown whole in a
solution figure cropped from the scheme. The scheme's theta in Q10(iii) is a
Times New Roman "Ɵ", which the text layer's ligature map reads "ti": that
row is read from glyph positions instead.

The sitting was already carded (118 authored cards, all shipped). Every task
is re-derived from the PDFs at the scheme's own mark boundaries and the
existing cards are corrected in place: every shipped id is kept, mapped
(`id=`) to the task it was carding. The four cards citing Q14(d) were orphans
only because the census mis-keyed Q14(d) (paper.py PROSE_MARKER_BLOCKS,
gated to this sitting); they keep their refs. Q6(h)'s two cards become one
(the part is one 7-mark letter of "any eight").
"""
from phys_review_lib import Q, SQ, S, M, G, pt, anyn, T, unprinted

YEAR, LEVEL = 2025, 'hl'
REVIEWED_AT = '2026-10-28'
BASELINE_COMMIT = '99ec7f0a0d6b243f4d5a1dc9b14a6a958e98095e'

SOURCES = {
    'paper': {'path': 'examiner-reports/physics/papers/2025-hl-paper.pdf', 'fileid': 'LC021ALP000EV.pdf',
              'sha256': 'bd8d60f621d8d952e0aaefb054a5e064ea81d6fafcee0501bad5cf10b2ddbf27', 'pages': 20},
    'scheme': {'path': 'examiner-reports/physics/schemes/2025-hl.pdf', 'fileid': 'LC021ALP000EV.pdf',
               'sha256': 'f0928d59d20bb0ea168dc17dcaf180b5c68389e8c9fecbf171a17ee90e21ffa2', 'pages': 27},
}

PAGE_ROLES = {
    'paper': {1: 'cover', **{p: 'questions' for p in range(2, 19)}, 19: 'acknowledgements', 20: 'back-cover'},
    'scheme': {1: 'cover', 2: 'note', 3: 'conventions', 4: 'annotations', 5: 'irish-bonus',
               **{p: 'marking' for p in range(6, 26)}, 26: 'blank', 27: 'back-cover'},
}

LETTERED = {6, 12, 14}

QUESTION_TOTALS = {**{n: 40 for n in range(1, 6)}, **{n: 56 for n in (6, 7, 8, 9, 10, 11, 13)},
                   12: 112,   # either (a) or (b), 56 each: both carded
                   14: 112}   # any two of (a)-(d), 28 each: all four carded
PART_TOTALS = {(12, 'a'): 56, (12, 'b'): 56, **{(14, x): 28 for x in 'abcd'}}
BEST_OF = {6: (8, 7)}
GROUP_TOTALS = {
    (1, ('i', 'ii', 'iii', 'iv')): 15, (1, ('v', 'vi', 'vii')): 25,
    (2, ('i', 'ii', 'iii', 'iv', 'v')): 27, (2, ('vi', 'vii')): 13,
    (3, ('i', 'ii', 'iii')): 21, (3, ('iv', 'v', 'vi')): 19,
    (4, ('i',)): 12, (4, ('ii', 'iii', 'iv')): 21, (4, ('v', 'vi')): 7,
    (5, ('i', 'ii', 'iii')): 25, (5, ('iv', 'v')): 15,
    (7, ('i', 'ii', 'iii')): 21, (7, ('iv', 'v', 'vi')): 23, (7, ('vii', 'viii', 'ix')): 12,
    (8, ('i', 'ii', 'iii')): 21, (8, ('iv', 'v', 'vi', 'vii', 'viii')): 35,
    (9, ('i', 'ii')): 18, (9, ('iii', 'iv')): 30, (9, ('v', 'vi')): 8,
    (10, ('i',)): 12, (10, ('ii',)): 21, (10, ('iii', 'iv', 'v', 'vi')): 23,
    (11, ('i', 'ii')): 21, (11, ('iii', 'iv', 'v')): 16, (11, ('vi', 'vii', 'viii')): 19,
    **{(13, (r,)): t for r, t in (('i', 7), ('ii', 7), ('iii', 14), ('iv', 7), ('v', 7), ('vi', 7), ('vii', 7))},
}
CHECKSUMS = {}

SCAN_PAGES = {'paper': range(2, 19)}
SELECTION_SCAN = [
    ('paper', 2, 'the following', 'Q1 "The following additional data were recorded": a reference to the table.'),
    ('paper', 3, 'both', 'Q2 lead-in "both trolleys moved": description.'),
    ('paper', 3, 'the following', 'Q2 "The following data were recorded": a reference to the table.'),
    ('paper', 4, 'the following', 'Q3 "the following graph": a reference to the graph.'),
    ('paper', 5, 'the following', 'Q4 "The following data were recorded": a reference to the table.'),
    ('paper', 6, 'the following', 'Q5 "The following data were recorded": a reference to the table.'),
    ('paper', 7, 'the following', 'Q6 "Answer any eight of the following parts": a best-eight of (a)-(l) at 7 '
                                  'each (8 x 7); every part is carded.'),
    ('paper', 13, 'the following', 'Q11(ii) "as shown in the following diagram": a reference to the diagram.'),
    ('paper', 14, 'either', 'Q12 "Answer either part (a) or part (b)": whole-part choice; both parts are carded.'),
    ('paper', 14, 'or', 'Q12, same choice.'),
    ('paper', 16, 'the following', 'Q13 "Read the following passage": a reference to the passage.'),
    ('paper', 16, 'or', 'Q13 passage "lines of force" or "field lines": passage text.'),
    ('paper', 17, 'any two', 'Q14 "Answer any two of the following parts": whole-part choice; every part is carded.'),
    ('paper', 17, 'the following', 'Q14, same rubric.'),
    ('paper', 17, 'the following', 'Q14(b) "The following table": a reference to the table.'),
    ('paper', 17, 'or', 'Q14(b)(i) "glass Y or Z": the answer options; one answer.'),
]

ROUTES = {}
SEC = 'State Examinations Commission'

CRIT = 'The scheme prints no answer here, only what earns the marks.'
LEGEND = S('Answers that are separated by a double solidus, //, are answers which are mutually',
           'with a partial answer from the other side.', page=3)
EACH = 'One card per separately priced part.'


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


def TK(page, clip, expect, marks, **kw):
    return G('tokens', page=page, clip=clip, expect=expect, marks=marks, **kw)


def TT(*a, cells=None, **kw):
    """T(), with the reviewer's reason for a mark cell that prices something else."""
    t = T(*a, **kw)
    if cells:
        t['cells'] = cells
    return t


def bundled(parts, keep):
    return f'The old card bundled {parts}, which the scheme prices apart; it keeps its id for {keep}.'


# ------------------------------------------------------------------ stems --
STEM1 = [P(2, 'A student investigated the laws of equilibrium', 'was acting.'),
         P(2, 'The following additional data were recorded.')]
STEM2 = [P(3, 'In an experiment to verify the principle of conservation of momentum', 'spring between them.'),
         P(3, 'When the spring was released, both trolleys moved'),
         P(3, 'Trolley A travelled a distance'), P(3, 'The following data were recorded.')]
Q2VI = P(3, 'External forces acting on the trolleys were minimised in the experiment.')
STEM3 = [P(4, 'In an experiment to measure the speed of sound in air', 'based on his recorded data.')]
STEM3A = [P(4, 'In an experiment to measure the speed of sound in air', 'for each tuning fork.')]
STEM4 = [P(5, 'In an experiment to verify Snell’s law', 'rectangular glass block.'),
         P(5, 'The experiment was repeated for different values of the angle of incidence.'),
         P(5, 'The following data were recorded.')]
STEM5 = [P(6, 'A student investigated the variation of the current', 'values of potential difference V.'),
         P(6, 'The following data were recorded.')]
MOON = P(9, 'The distance from the centre of the Earth', 'orbits the Earth every 27.3 days.')
DATA7 = P(9, 'mass of the Earth = 5.97', 'acceleration due to gravity = 9.8 m s⁻².')
PERSON = P(9, 'A person of mass 80 kg is standing at the equator', 'at the equator.')
STEM8 = [P(10, 'Light and all other electromagnetic radiation', 'interference.')]
DESTR = P(10, 'Destructive interference can be observed when waves meet.')
LASER = P(10, 'Laser light of wavelength 691 nm', 'diagram.')
STEM9 = [P(11, 'In 1887, Henrich Hertz discovered the photoelectric effect.', 'groundbreaking work.')]
PCELL = P(11, 'Monochromatic radiation falls on a photocell', 'observed is 0.005 mA.')
STEAM = P(12, 'Dry steam at 100 °C was passed', 'was 20 °C.')
DATA10 = P(12, 'specific heat capacity of copper = 390',
           'specific latent heat of vaporisation of water = 2.3 x 10⁶ J kg⁻¹.')
KELVIN = P(12, 'The SI unit of temperature is the kelvin.')
SWITCH = P(13, 'The circuit diagram to the right shows three resistors connected', 'to a 12 V power supply.')
DIVIDER = P(13, 'The diagram below shows a potential divider circuit', 'thermostat.')
STEM12A = [P(14, 'In an experiment conducted in 1932, Cockcroft and Walton', 'equivalent.')]
ANDERSON = P(14, 'Also in 1932, the American physicist Carl Anderson', 'proposed in 1928.')
PET = P(14, 'A PET scanner is used to see how cancer patients', 'emits a positron as it decays.')
PASSAGE = [P(16, 'The work of Michael Faraday', 'by Joseph Henry in 1838.'),
           P(16, 'Adapted from “Physics: Teacher’s Reference Handbook”')]
VECTOR = P(16, 'A magnetic field is described as a vector field.')
WIRE = P(16, 'The diagram shows a 5 cm long nichrome wire with', 'flux density 150 mT.')
COIL = P(16, 'A coil consists of 150 turns of wire', 'over a time of 1.1 ms.')
SPRING = P(17, 'A mass attached to a spring hangs vertically at rest.', 'pulled down and released.')
MASS150 = P(17, 'A 150 g mass is attached to a spring', '25 N m⁻¹.')
FIBRE = [P(17, 'National Broadband Ireland is responsible', 'premises to local exchanges.'),
         P(17, 'An optical fibre consists of a core made from glass', 'refractive index for three types of glass.')]
FIBRE_A = [FIBRE[0], P(17, 'An optical fibre consists of a core made from glass', 'different type of glass.')]
IODINE = [P(18, 'In 2011, an accident in the Fukushima nuclear power station', 'beta particles and gamma rays.')]
SAMPLE = P(18, 'A sample of Iodine–131 contains 2 × 10¹⁵ atoms.')
SPHERE = P(18, 'An insulated metal sphere has a diameter of 10 cm', 'N C ⁻¹.')

ROUTE_NOTE = ('The two sides of the scheme\'s // are mutually exclusive routes: each is shown as its own '
              'answer set.')

TASKS = [
    # ============================================================ Section A ==
    # ---------------------------------------------------------------- Q1 --
    T('1i', 'Q1(i)', 'A', P(2, 'Describe how the student found the centre of gravity of the metre stick.'),
      [R('balance on a pivot', 3)], 'phys-1-2', 'finding-centre-of-gravity',
      SQ(6, 'Describe how the student found the centre of gravity of the metre stick.'), 3, stem=STEM1[:1],
      id='phys-2025-hl-q1-i'),
    T('1ii', 'Q1(ii)', 'A', P(2, 'How did the student know that the metre stick was in equilibrium?'),
      [R('not accelerating', 3)], 'phys-1-2', 'recognising-equilibrium',
      SQ(6, 'How did the student know that the metre stick was in equilibrium?'), 3, stem=STEM1[:1],
      id='phys-2025-hl-q1-ii'),
    T('1iii', 'Q1(iii)', 'A', P(2, 'Draw a labelled diagram to show all the forces acting on the metre stick.'),
      [C('two forces up and four forces down with weight arrow labelled', 6, units=[1] * 6,
         note='The scheme prints [6 x 1] against this line, which names what the diagram must show.')],
      'phys-1-2', 'forces-on-metre-stick',
      SQ(6, 'Draw a labelled diagram to show all the forces acting on the metre stick.'), 6, stem=STEM1,
      fig='q1-table', id='phys-2025-hl-q1-iii',
      decision='A drawing priced [6 x 1] on one printed line: one criterion row of six 1-mark units.'),
    T('1iv', 'Q1(iv)', 'A', P(2, 'Why was it important to have the forces applied vertically to the metre stick?'),
      [R('(distance to each force position is) a perpendicular distance', 3)], 'phys-1-2',
      'why-vertical-forces', SQ(6, 'Why was it important to have the forces applied vertically'), 3,
      stem=STEM1[:1], id='phys-2025-hl-q1-iv'),
    T('1v', 'Q1(v)', 'A', P(2, 'Using the given data, calculate the net force acting on the metre stick.'),
      [R('forces up = 8.9 (N)', 3), R('forces down = 8.96 (N)', 3), R('net force ( = 0.06 N ) ≈ 0', 3)],
      'phys-1-2', 'net-force-on-metre-stick',
      SQ(6, 'Using the given data, calculate the net force acting on the metre stick.'), 9, stem=STEM1,
      fig='q1-table', id='phys-2025-hl-q1-v'),
    T('1vi', 'Q1(vi)', 'A', [P(2, 'Using an axis at the 5 cm mark on the metre stick, calculate'), M('(a)', 2),
                             P(2, 'the sum of the clockwise moments,'), M('(b)', 2),
                             P(2, 'the sum of the anticlockwise moments.')],
      [R('M = Fd', 3), C('any one moment calculated', 3), C('clockwise moments calculated', 3),
       C('anticlockwise moments calculated', 3)], 'phys-1-2', 'sum-of-moments',
      SQ(6, 'Using an axis at the 5 cm mark on the metre stick, calculate'), 12, stem=STEM1,
      fig='q1-table', id='phys-2025-hl-q1-vi',
      decision='The scheme prices (a) and (b) together (M = Fd and "any one moment" serve both): one card.'),
    T('1vii', 'Q1(vii)', 'A', P(2, 'Use your results to verify the laws of equilibrium for a set of co-planar forces.'),
      [R('(total) force up ≈ (total) force down', 2),
       R('(total) clockwise moment ≈ (total) anticlockwise moment', 2)], 'phys-1-2',
      'verifying-laws-of-equilibrium', SQ(6, 'Use your results to verify the laws of equilibrium'), 4,
      stem=STEM1, fig='q1-table', id='phys-2025-hl-q1-vii',
      decision='[2 + 2] against the two lines: 2 each, in the order printed.'),
    # ---------------------------------------------------------------- Q2 --
    T('2i', 'Q2(i)', 'A', P(3, 'Explain how the masses could have been measured.'),
      [R('(electronic) balance', 3)], 'phys-1-2', 'measuring-mass',
      SQ(7, 'Explain how the masses could have been measured.'), 3, stem=STEM2, fig='q2-table',
      id='phys-2025-hl-q2-i'),
    T('2ii', 'Q2(ii)', 'A', P(3, 'Describe how the constant velocity of a trolley can be determined.'),
      [pt(S('(measure) length l of card', '// (measure) distance between dots', piece=1, psep='//'), 3),
       pt(S('(measure) time for l', '// (measure) time between dots', piece=1, psep='//'), 3),
       R('v = l/t', 3)], 'phys-1-1', 'measuring-constant-velocity',
      SQ(7, 'Describe how the constant velocity of a trolley can be determined.'), 9, stem=STEM2[:3],
      id='phys-2025-hl-q2-ii',
      decision='The scheme prints two routes split by //: card and timer, or dots on tape; both close on '
               'v = l/t. ' + ROUTE_NOTE),
    T('2iii', 'Q2(iii)', 'A', P(3, 'Calculate the velocity of trolley A and the velocity of trolley B after'),
      [pt(S('vA = 0.54 m s⁻¹ , vB = 0.42 m s⁻¹', piece=1, psep=','), 2),
       pt(S('vA = 0.54 m s⁻¹ , vB = 0.42 m s⁻¹', piece=2, psep=','), 1)], 'phys-1-1', 'trolley-velocities',
      SQ(7, 'Calculate the velocity of trolley A and the velocity of trolley B'), 3, stem=STEM2, fig='q2-table',
      id='phys-2025-hl-q2-iii',
      decision='[2 + 1] against the line holding both velocities: vA 2, vB 1, in the order printed.'),
    T('2iv', 'Q2(iv)', 'A', P(3, 'What is the total momentum of the trolleys before they are released?'),
      [R('zero', 3)], 'phys-1-2', 'momentum-before-release',
      SQ(7, 'What is the total momentum of the trolleys before they are released?'), 3, stem=STEM2[:3],
      id='phys-2025-hl-q2-iv'),
    T('2v', 'Q2(v)', 'A', P(3, 'Use the data to show that this experiment verifies the principle', 'momentum.'),
      [R('p = mv', 3), R('pA = 0.108 (kg m s⁻¹) / pB = 0.105 (kg m s⁻¹)', 3, whole=True),
       R('pₜₒₜₐₗ ( = 0.003 kg m s⁻¹ ) ≈ 0', 3)], 'phys-1-2', 'verifying-conservation-of-momentum',
      SQ(7, 'Use the data to show that this experiment verifies the principle of conservation of'), 9,
      stem=STEM2, fig='q2-table', id='phys-2025-hl-q2-v',
      decision='The scheme prices both momenta in one 3-mark cell: one row.'),
    T('2via', 'Q2(vi)(a)', 'A', [Q2VI, M('(a)', 3), P(3, 'State two principal external forces that should be minimised.')],
      [pt(S('frictional, gravitational', piece=1, psep=','), 3),
       pt(S('frictional, gravitational', piece=2, psep=','), 3)], 'phys-1-2', 'external-forces',
      SQ(7, 'State two principal external forces that should be minimised.'), 6, stem=STEM2[:3],
      id='phys-2025-hl-q2-vi-a', decision='[3 + 3] against the two forces printed on one line: 3 each.'),
    T('2vib', 'Q2(vi)(b)', 'A', [Q2VI, M('(b)', 3), P(3, 'Describe how the effect of these forces could be minimised.')],
      [pt(S('cushion of air or clean air track', '// oil wheels or clean track', piece=1, psep='//'), 2),
       pt(S('horizontal air track', '// slope track', piece=1, psep='//'), 2,
          note_sel=S('[allow 4 marks for adjust the track until frictional force = gravitational force]'))],
      'phys-1-2', 'minimising-external-forces',
      SQ(7, 'Describe how the effect of these forces could be minimised.'), 4, stem=STEM2[:3],
      id='phys-2025-hl-q2-vi-b',
      decision='Two routes split by //: an air track, or a track with oiled wheels. ' + ROUTE_NOTE),
    T('2vii', 'Q2(vii)', 'A', P(3, 'State one other way to improve the accuracy of the experiment.'),
      [pt(S('e.g. repeat the experiment / reduce the error of parallax / more accurate balance/timer [3]',
            piece=1, psep=' ['), 3)], 'phys-1-2', 'improving-accuracy',
      SQ(7, 'State one other way to improve the accuracy of the experiment.'), 3, stem=STEM2[:3],
      id='phys-2025-hl-q2-vii',
      decision='The text layer sets this line\'s [3] inside the line, not as a mark cell: the row is cut at '
               'it, and the 3 is the printed cell.'),
    # ---------------------------------------------------------------- Q3 --
    T('3i', 'Q3(i)', 'A', P(4, 'Draw a labelled diagram of the arrangement of the apparatus used in this experiment.'),
      [C('tube', 4), C('means of varying length l', 4),
       C('tuning fork / metre stick', 4, note_sel=S('[–1 if no label present on diagram]'))],
      'phys-2-5', 'resonance-tube-apparatus',
      SQ(8, 'Draw a labelled diagram of the arrangement of the apparatus used in this experiment.'), 12,
      stem=STEM3A, id='phys-2025-hl-q3-i'),
    T('3ii', 'Q3(ii)', 'A', P(4, 'Describe how the first position of resonance was found.'),
      [R('increase length of the pipe (from l = 0 cm)', 3), R('until (loud) sound is heard', 3)],
      'phys-2-5', 'finding-first-resonance', SQ(8, 'Describe how the first position of resonance was found.'),
      6, stem=STEM3A, id='phys-2025-hl-q3-ii'),
    T('3iii', 'Q3(iii)', 'A', P(4, 'Describe how the frequency values were determined.'),
      [R('(read) the tuning fork(s)', 3)], 'phys-2-5', 'tuning-fork-frequency',
      SQ(8, 'Describe how the frequency values were determined.'), 3, stem=STEM3A, id='phys-2025-hl-q3-iii'),
    T('3iv', 'Q3(iv)', 'A', P(4, 'Use the graph to calculate the speed of sound in air.'),
      [C('slope formula', 3), C('calculate slope', 3), R('v = 4 × slope', 3, end='c = fλ'),
       R('v ≈ 343.7 m s⁻¹', 3)], 'phys-2-5', 'speed-of-sound-from-graph',
      SQ(8, 'Use the graph to calculate the speed of sound in air.'), 12, stem=STEM3, fig='q3-graph',
      id='phys-2025-hl-q3-iv'),
    T('3v', 'Q3(v)', 'A', P(4, 'Why does the student’s graph not go through the origin?'),
      [R('end correction / antinode forms outside opening of pipe', 3)], 'phys-2-5', 'end-correction',
      SQ(8, 'Why does the student’s graph not go through the origin?'), 3, stem=STEM3, fig='q3-graph',
      id='phys-2025-hl-q3-v'),
    T('3vi', 'Q3(vi)', 'A', P(4, 'Identify the frequency of the tuning fork that had the lowest frequency.'),
      [R('f = 200 Hz', 4)], 'phys-2-5', 'lowest-frequency-from-graph',
      SQ(8, 'Identify the frequency of the tuning fork that had the lowest frequency.'), 4, stem=STEM3,
      fig='q3-graph'),
    # ---------------------------------------------------------------- Q4 --
    T('4i', 'Q4(i)', 'A', P(5, 'Copy the above diagram into your answerbook', 'refraction, r.'),
      [C('normal drawn at point of entry', 3), C('ray refracted (towards normal)', 3), C('emergent ray', 3),
       C('angle r indicated', 3)], 'phys-2-3', 'ray-through-glass-block',
      SQ(9, 'Copy the above diagram into your answerbook'), 12, stem=STEM4[:2], fig='q4-block'),
    T('4ii', 'Q4(ii)', 'A', P(5, 'Draw a suitable graph, on graph paper, to show the relationship between i and r.'),
      [TK(9, (85, 345, 545, 397),
          'sin i 0.342 0.500 0.643 0.766 0.866 0.940 sin r 0.225 0.326 0.454 0.500 0.574 0.629', 3,
          label=S('values of sin i and sin r')),
       C('axes labelled', 3), C('points plotted', 3), C('line of best fit', 3)], 'phys-2-3', 'snells-law-graph',
      SQ(9, 'Draw a suitable graph, on graph paper, to show the relationship between i and r.'), 12,
      stem=STEM4, fig='q4-table', id='phys-2025-hl-q4-ii',
      decision='The scheme prints its sin i and sin r values as a table under the row "values of sin i and '
               'sin r": read from the table, row by row.'),
    T('4iii', 'Q4(iii)', 'A', P(5, 'Explain how your graph verifies Snell’s law.'),
      [R('straight line through origin / sin i ∝ sin r', 3)], 'phys-2-3', 'graph-verifies-snells-law',
      SQ(9, 'Explain how your graph verifies Snell’s law.'), 3, stem=STEM4[:2], id='phys-2025-hl-q4-iii'),
    T('4iv', 'Q4(iv)', 'A', P(5, 'Use your graph to calculate the refractive index of the glass.'),
      [C('slope formula', 3), R('n = 1.5', 3)], 'phys-2-3', 'refractive-index-from-graph',
      SQ(9, 'Use your graph to calculate the refractive index of the glass.'), 6, stem=STEM4, fig='q4-table',
      id='phys-2025-hl-q4-iv'),
    T('4v', 'Q4(v)', 'A', P(5, 'Explain why the student placed the glass block flat on a sheet of paper',
                           'not on one of its narrow faces.'),
      [R('reduce (percentage) error (in r)', 3)], 'phys-2-3', 'block-flat-on-paper',
      SQ(9, 'Explain why the student placed the glass block flat on a sheet of paper'), 3, stem=STEM4[:2],
      fig='q4-sheet', id='phys-2025-hl-q4-v'),
    T('4vi', 'Q4(vi)', 'A', P(5, 'Describe what the student would observe if the incident ray of light', 'block.'),
      [R('ray would pass straight through', 4)], 'phys-2-3', 'ray-along-normal',
      SQ(9, 'Describe what the student would observe if the incident ray of light'), 4, stem=STEM4[:2],
      id='phys-2025-hl-q4-vi'),
    # ---------------------------------------------------------------- Q5 --
    T('5i', 'Q5(i)', 'A', P(6, 'Draw a circuit diagram for this experiment.'),
      [C('power supply', 3), C('voltmeter in parallel with filament bulb', 3),
       C('ammeter in series with filament bulb', 3), C('means of changing voltage', 3)], 'phys-3-3',
      'filament-bulb-circuit', SQ(10, 'Draw a circuit diagram for this experiment.'), 12, stem=STEM5[:1],
      id='phys-2025-hl-q5-i'),
    T('5ii', 'Q5(ii)', 'A', P(6, 'Draw a suitable graph, on graph paper, to show the relationship between V and I.'),
      [C('axes labelled', 3), C('points plotted', 3), C('curve of best fit drawn', 3)], 'phys-3-3',
      'filament-bulb-graph', SQ(10, 'Draw a suitable graph, on graph paper, to show the relationship between V'),
      9, stem=STEM5, fig='q5-table', id='phys-2025-hl-q5-ii'),
    T('5iii', 'Q5(iii)', 'A', P(6, 'Does the graph show that Ohm’s law is obeyed for the filament bulb?'),
      [R('no', 2), R('not a straight line', 2)], 'phys-3-3', 'ohms-law-filament-bulb',
      SQ(10, 'Does the graph show that Ohm’s law is obeyed for the filament bulb?'), 4, stem=STEM5,
      fig='q5-table', id='phys-2025-hl-q5-iii'),
    T('5iv', 'Q5(iv)', 'A', [P(6, 'Calculate the resistance of the bulb when the current is'), M('(a)', 6),
                             P(6, '40 mA,'), M('(b)', 6), P(6, '90 mA.')],
      [R('R = V/I', 3), R('R ≈ 43 Ω', 2, label=S('(a)', after='R = V/I')),
       R('R ≈ 54 Ω', 2, label=S('(b)', after='R ≈ 43 Ω'))], 'phys-3-3', 'resistance-of-filament',
      SQ(10, 'Calculate the resistance of the bulb when the current is'), 7, stem=STEM5, fig='q5-table',
      id='phys-2025-hl-q5-iv', decision='R = V/I serves (a) and (b): one card.'),
    T('5v', 'Q5(v)', 'A', P(6, 'Explain what happens to the resistance of the filament bulb as the current increases.'),
      [R('(increase in current causes) increase in temperature', 4),
       R('(increase in temperature causes) increase in resistance', 4)], 'phys-3-3', 'filament-heating',
      SQ(10, 'Explain what happens to the resistance of the filament bulb as the current increases.'), 8,
      stem=STEM5[:1], id='phys-2025-hl-q5-v'),
    # ============================================================ Section B ==
    # ---------------------------------------------------------------- Q6 --
    T('6a', 'Q6(a)', 'B', P(7, 'State the function of a hydrometer and state a practical example of its use.'),
      [R('density', 4), C('example given', 3)], 'phys-1-2', 'hydrometer',
      SQ(11, 'State the function of a hydrometer and state a practical example of its use.'), 7,
      id='phys-2025-hl-q6-a'),
    T('6b', 'Q6(b)', 'B', [P(7, 'A car is driving up a hill', 'constant frictional force.'),
                           P(7, 'Draw a labelled vector diagram to show the forces acting on the car.')],
      [pt(S('applied force, frictional force, gravitational force, normal/reaction force', piece=k, psep=', '),
          m, kind='criterion',
          **({'note_sel': S('[–1 mark if no label present on diagram] & [–1 mark for additional incorrect forces]')}
             if k == 4 else {}))
       for k, m in ((1, 2), (2, 2), (3, 2), (4, 1))], 'phys-1-2', 'forces-on-car-on-incline',
      SQ(11, 'Draw a labelled vector diagram to show the forces acting on the car.'), 7, id='phys-2025-hl-q6-b',
      decision='[2 + 2 + 2 + 1] against the four forces printed on one line: in the order printed.'),
    T('6c', 'Q6(c)', 'B', [P(7, 'Using the diagram, calculate the time it takes for the two', 'particles to meet.'),
                           P(7, 'acceleration due to gravity = 9.8 m s⁻²')],
      [R('equation of motion given; e.g. s = ut + ½ at²', 3), R('sX = 15t + ½(–9.8)t²', 2, end='sY = 5t + ½(9.8)t²'),
       R('t = 1 s', 2)], 'phys-1-1', 'particles-meeting',
      SQ(11, 'Using the diagram, calculate the time it takes for the two particles to meet.'), 7,
      stem=[P(7, 'The diagram on the right shows a smooth particle X being', 'a velocity of 5 m s⁻¹.')],
      fig='q6c-diagram', id='phys-2025-hl-q6-c'),
    T('6d', 'Q6(d)', 'B', P(7, 'Explain what is meant by complementary colours of light.', 'complementary colours.'),
      [R('a primary and a secondary colour that combine to give white light', 4),
       R('blue–yellow / green–magenta / red–cyan', 3)], 'phys-2-4', 'complementary-colours',
      SQ(11, 'Explain what is meant by complementary colours of light.'), 7, id='phys-2025-hl-q6-d'),
    T('6e', 'Q6(e)', 'B', P(7, 'Draw a ray diagram to show the formation of a virtual image using a concave mirror.'),
      [C('object (inside focus)', 3), C('two reflected rays', 2), C('magnified virtual image', 2)], 'phys-2-3',
      'virtual-image-concave-mirror',
      SQ(11, 'Draw a ray diagram to show the formation of a virtual image using a concave mirror.'), 7,
      id='phys-2025-hl-q6-e'),
    T('6f', 'Q6(f)', 'B', [P(7, 'The Atlantis XII is a submarine', 'this depth.'),
                           P(7, 'acceleration due to gravity = 9.8 m s⁻²;', 'atmospheric pressure = 101 kPa.')],
      [R('P = ρgh', 3), R('P = 301350 (Pa)', 2), R('Pₜₒₜₐₗ = (301350 + 101000) = 402350 Pa', 2)], 'phys-1-2',
      'pressure-at-depth', SQ(11, 'Calculate the total pressure on the submarine at this depth.'), 7,
      id='phys-2025-hl-q6-f'),
    T('6g', 'Q6(g)', 'B', [P(8, 'A 12 µF parallel-plate capacitor is connected to a 2 V cell.'), P(8, 'Calculate'),
                           M('(i)', 8), P(8, 'the charge stored on one of the plates,'), M('(ii)', 8),
                           P(8, 'the energy stored by the capacitor.')],
      [FR(12, (110, 130, 160, 156), 'C = q/V', 2), R('q = 2.4 ×10⁻⁵ C', 2), R('E = ½ CV²', 2),
       R('E = 2.4 ×10⁻⁵ J', 1)], 'phys-3-2', 'capacitor-charge-and-energy',
      SQ(12, 'A 12 µF parallel-plate capacitor is connected to a 2 V cell.'), 7, id='phys-2025-hl-q6-g',
      decision='One of the eight 7-mark parts: the scheme prices (i) and (ii) in one cell [2 + 2 + 2 + 1], '
               'in the order printed.'),
    T('6h', 'Q6(h)', 'B', [P(8, 'A guitar string is vibrating at its first harmonic'), M('(i)', 8),
                           P(8, 'Draw a diagram of the string vibrating at its third harmonic.'), M('(ii)', 8),
                           P(8, 'Determine the frequency of the third harmonic.')],
      [C('four nodes, three antinodes on a string fixed at both ends', 4,
         note='The scheme prints no drawing; this line names what the diagram must show.'),
       R('f = 588 Hz', 3)], 'phys-2-6', 'third-harmonic',
      SQ(12, 'A guitar string is vibrating at its first harmonic'), 7, id='phys-2025-hl-q6-h-i',
      decision='One of the eight 7-mark parts: the scheme prices (i) and (ii) in one cell [4 + 3]. The old '
               'cards carded (i) and (ii) apart; Q6(h)(ii)\'s card is withdrawn onto this one.'),
    T('6i', 'Q6(i)', 'B', [P(8, 'A spectral line in a distant galaxy', 'frequency of 7.59 × 10¹⁴ Hz.'),
                           P(8, 'Calculate the velocity of the galaxy.')],
      [FR(12, (84, 400, 130, 426), "f' = fc/(c±u)", 4), R('u = 1.89 x 10⁷ m s⁻¹', 3)], 'phys-2-7',
      'red-shift-velocity', SQ(12, 'Calculate the velocity of the galaxy.'), 7, id='phys-2025-hl-q6-i'),
    T('6j', 'Q6(j)', 'B', P(8, 'Indicate on a diagram the sections of a p-n junction', 'charged and neutral.'),
      [C('p-n junction with depletion layer', 4)]
      + [pt(S('negatively charged section, positively charged section, neutral section', piece=k, psep=', '), 1,
            kind='criterion') for k in (1, 2, 3)], 'phys-3-3', 'p-n-junction',
      SQ(12, 'Indicate on a diagram the sections of a p-n junction'), 7, id='phys-2025-hl-q6-j',
      decision='[1 + 1 + 1] against the three sections printed on one line: 1 each.'),
    T('6k', 'Q6(k)', 'B', P(8, 'Explain the principle of the source of the Sun’s energy.'),
      [R('fusion', 7, note_sel=S('[award 4 marks for reference to nuclear reactions / E = mc²]'))], 'phys-4-6',
      'source-of-suns-energy', SQ(12, 'Explain the principle of the source of the Sun’s energy.'), 7,
      id='phys-2025-hl-q6-k'),
    T('6l', 'Q6(l)', 'B', [P(8, 'Under Rutherford’s supervision', 'thin film of gold.'),
                           P(8, 'State two conclusions drawn from their experiment', 'charge in the atom.')],
      [anyn(S('any two: mass concentrated at centre, nucleus positively charged, atom mostly empty space',
              piece=2, psep=': '), 2, 4, steps=[4, 3], sep=',', note='any two')], 'phys-4-3',
      'geiger-marsden-conclusions', SQ(12, 'State two conclusions drawn from their experiment'), 7,
      id='phys-2025-hl-q6-l', decision='"any two" of three at [4 + 3]: a menu, the first 4 and the second 3.'),
    # ---------------------------------------------------------------- Q7 --
    T('7ia', 'Q7(i)(a)', 'B', [P(9, 'Explain what is meant by'), M('(a)', 9), P(9, 'weight,')],
      [R('gravitational force acting on a mass // W = mg & notation', 3, whole=True, note_sel=LEGEND)],
      'phys-1-5', 'weight', SQ(13, 'weight,'), 3, id='phys-2025-hl-q7-i-a',
      decision='One 3-mark line with its two sides: one row, as printed.'),
    T('7ib', 'Q7(i)(b)', 'B', [P(9, 'Explain what is meant by'), M('(b)', 9), P(9, 'centripetal force.')],
      [R('force towards centre of circle', 3),
       R('(that keeps) object moving in a circle', 3,
         note='The scheme also allows 3 marks for the centripetal force formula, printed under these rows.')],
      'phys-1-6', 'centripetal-force', SQ(13, 'centripetal force.'), 6, id='phys-2025-hl-q7-i-b'),
    T('7ii', 'Q7(ii)', 'B', P(9, 'State Newton’s law of universal gravitation.'),
      [FR(13, (84, 197, 475, 221),
          'gravitational force is proportional to the product of two masses // F ∝ (m₁ m₂)/d²', 3,
          note_sel=LEGEND),
       R('inversely proportional to square of distance between them', 3, end='// notation')], 'phys-1-5',
      'law-of-universal-gravitation', SQ(13, 'State Newton’s law of universal gravitation.'), 6,
      id='phys-2025-hl-q7-ii', decision='Each line printed with its // side: one row per line, as printed.'),
    T('7iii', 'Q7(iii)', 'B', P(9, 'Derive an equation for the angular velocity', 'the object moves in a circle.'),
      [FR(13, (84, 266, 345, 292), 'θ = s/r or v = s/t or ω = θ/t', 2), C('combination of two formulae', 2),
       FR(13, (84, 300, 118, 325), 'ω = v/r', 2)], 'phys-1-6', 'deriving-angular-velocity',
      SQ(13, 'Derive an equation for the angular velocity of an object'), 6),
    T('7iva', 'Q7(iv)(a)', 'B', [P(9, 'Calculate'), M('(a)', 9), P(9, 'the angular velocity of the Moon,')],
      [R('θ = 2π', 3), R('ω = 2.664 x 10⁻⁶ rad s⁻¹', 3)], 'phys-1-6', 'angular-velocity-of-moon',
      SQ(13, 'the angular velocity of the Moon,'), 6, stem=[MOON], id='phys-2025-hl-q7-iv',
      decision=bundled('(a) and (b)', '(a)')),
    T('7ivb', 'Q7(iv)(b)', 'B', [P(9, 'Calculate'), M('(b)', 9), P(9, 'the linear velocity of the Moon.')],
      [R('v = rω', 3), R('v = 1023 m s⁻¹', 3)], 'phys-1-6', 'linear-velocity-of-moon',
      SQ(13, 'the linear velocity of the Moon.'), 6,
      stem=[MOON, M('(a)', 9), P(9, 'the angular velocity of the Moon,')]),
    T('7v', 'Q7(v)', 'B', P(9, 'Calculate the force of gravity that the Earth exerts', 'universal gravitation.'),
      [FR(13, (84, 496, 140, 522), 'F = G (m₁ m₂)/d²', 3),
       R('force of earth on moon = 1.986 x 10²⁰ N (towards the centre of the Earth)', 3)], 'phys-1-5',
      'force-of-earth-on-moon', SQ(13, 'Calculate the force of gravity that the Earth exerts on the Moon'), 6,
      stem=[MOON, DATA7], id='phys-2025-hl-q7-v'),
    T('7vi', 'Q7(vi)', 'B', P(9, 'Why does the Moon not fall down to Earth?'),
      [R('(tangential) velocity', 5, end='// gravitational force is too weak', note_sel=LEGEND)], 'phys-1-6',
      'why-moon-does-not-fall', SQ(13, 'Why does the Moon not fall down to Earth?'), 5, id='phys-2025-hl-q7-vi'),
    T('7vii', 'Q7(vii)', 'B', P(9, 'Calculate the centripetal force needed to keep the person moving'),
      [FR(13, (75, 600, 162, 628), 'Fcentripetal = mv²/r', 2), R('Fcentripetal = 2.68 N', 2)], 'phys-1-6',
      'centripetal-force-at-equator',
      SQ(13, '(vii)', bare=True, welded=True,
         paired='The scheme reprints no ask for (vii): its marker opens the answer\'s own line.'), 4,
      stem=[PERSON, DATA7]),
    T('7viii', 'Q7(viii)', 'B', P(9, 'Calculate the resultant normal reaction force acting on the person.'),
      [R('W = mg', 2), R('Fnormal = (W – Fcentripetal) = 781.32 N', 2)], 'phys-1-6', 'normal-reaction-at-equator',
      SQ(13, '(viii)', bare=True, welded=True,
         paired='The scheme reprints no ask for (viii): its marker opens the answer\'s own line.'), 4,
      stem=[PERSON, M('(vii)', 9), P(9, 'Calculate the centripetal force needed to keep the person moving'), DATA7],
      id='phys-2025-hl-q7-viii'),
    T('7ix', 'Q7(ix)', 'B', P(9, 'Draw a labelled diagram to show the forces acting on the person.'),
      [C('weight', 2), C('(approximately) equals normal/reaction force', 2,
                         note_sel=S('[–1 mark if no label present on diagram] & [–1 mark for additional incorrect forces]'))],
      'phys-1-6', 'forces-on-person-at-equator',
      SQ(13, '(ix)', bare=True, welded=True,
         paired='The scheme reprints no ask for (ix): its marker opens the answer\'s own line.'), 4,
      stem=[PERSON], id='phys-2025-hl-q7-ix', decision='[2 + 2] against the two lines: 2 each.'),
    # ---------------------------------------------------------------- Q8 --
    T('8i', 'Q8(i)', 'B', P(10, 'Explain what is meant by a transverse wave.'),
      [R('vibration is perpendicular', 3), R('to the direction of travel', 3)], 'phys-2-2', 'transverse-wave',
      SQ(14, 'Explain what is meant by a transverse wave.'), 6, stem=STEM8, id='phys-2025-hl-q8-i'),
    T('8ii', 'Q8(ii)', 'B', P(10, 'Describe an experiment to demonstrate that light waves are transverse waves.'),
      [R('apparatus: two pieces of polaroid material and a light source', 3, whole=True),
       R('method: rotate one polaroid relative to the other', 3, whole=True),
       R('result: light intensity decreases', 3, whole=True)], 'phys-2-2', 'polarisation-experiment',
      SQ(14, 'Describe an experiment to demonstrate that light waves are transverse waves.'), 9, stem=STEM8,
      id='phys-2025-hl-q8-ii'),
    T('8iii', 'Q8(iii)', 'B', P(10, 'State two conditions necessary for total destructive interference to occur.'),
      [R('same amplitude', 4), R('crest meets trough', 2)], 'phys-2-6', 'total-destructive-interference',
      SQ(14, 'State two conditions necessary for total destructive interference to occur.'), 6,
      stem=[DESTR], id='phys-2025-hl-q8-iii', decision='[4 + 2] against the two lines: in the order printed.'),
    T('8iv', 'Q8(iv)', 'B', P(10, 'Explain how this pattern is formed from the laser light.'),
      [R('each slit acts as a source / waves diffract / waves meet', 6),
       R('constructive interference gives bright fringes', 3)], 'phys-2-6', 'forming-the-pattern',
      SQ(14, 'Explain how this pattern is formed from the laser light.'), 9, stem=[LASER], fig='q8-diagram',
      id='phys-2025-hl-q8-iv', decision='[6 + 3] against the two lines: in the order printed.'),
    T('8v', 'Q8(v)', 'B', P(10, 'Calculate the number of lines per mm on the diffraction grating.'),
      [R('nλ = d sin θ', 6), R('θ = 24.5°', 3), R('number of lines/mm = 300', 3)], 'phys-2-6',
      'lines-per-mm', SQ(14, 'Calculate the number of lines per mm on the diffraction grating.'), 12,
      stem=[LASER], fig='q8-diagram'),
    T('8vi', 'Q8(vi)', 'B', P(10, 'Calculate the maximum number of images that could be observed.'),
      [R('nₘₐₓ = d/λ', 3), R('nₘₐₓ = 4', 2), R('maximum number of images = ( 4 + 1 + 4 ) = 9', 1)], 'phys-2-6',
      'maximum-number-of-images', SQ(14, 'Calculate the maximum number of images that could be observed.'), 6,
      stem=[LASER], fig='q8-diagram', id='phys-2025-hl-q8-vi'),
    T('8vii', 'Q8(vii)', 'B', [P(10, 'Describe the effect on the pattern when'), M('(a)', 10),
                               P(10, 'the wavelength of the laser light is increased,'), M('(b)', 10),
                               P(10, 'a diffraction grating of more lines per mm is used.')],
      [R('distance between fringes increases / less images produced', 4,
         label=S('(a)', after='a diffraction grating of more lines per mm is used.')),
       pt(S('distance between fringes increases / less images produced', nth=2), 2,
          label=S('(b)', after='distance between fringes increases'))], 'phys-2-6', 'changing-the-pattern',
      SQ(14, 'Describe the effect on the pattern when'), 6, stem=[LASER], fig='q8-diagram',
      id='phys-2025-hl-q8-vii',
      decision='One cell [4 + 2] prices (a) and (b) together: one card, (a) 4 and (b) 2 in the order printed.'),
    T('8viii', 'Q8(viii)', 'B', P(10, 'State one type of electromagnetic radiation that has a shorter wavelength'),
      [R('UV / X-rays / gamma rays', 2)], 'phys-2-4', 'shorter-wavelength-than-light',
      SQ(14, 'State one type of electromagnetic radiation that has a shorter wavelength'), 2, stem=STEM8,
      id='phys-2025-hl-q8-viii'),
    # ---------------------------------------------------------------- Q9 --
    T('9ia', 'Q9(i)(a)', 'B', [P(11, 'Explain what is meant by'), M('(a)', 11), P(11, 'a photon,')],
      [R('a bundle of energy', 3, end='// E = hf & notation', note_sel=LEGEND)], 'phys-4-2', 'photon',
      SQ(15, 'a photon,'), 3, stem=STEM9, id='phys-2025-hl-q9-i-a',
      decision='One 3-mark line with its two sides: one row, as printed.'),
    T('9ib', 'Q9(i)(b)', 'B', [P(11, 'Explain what is meant by'), M('(b)', 11), P(11, 'the photoelectric effect.')],
      [R('emission of electrons from metal surface', 3),
       R('by electromagnetic radiation of a suitable frequency', 3)], 'phys-4-2', 'photoelectric-effect',
      SQ(15, 'the photoelectric effect.'), 6, stem=STEM9, id='phys-2025-hl-q9-i-b'),
    T('9ii', 'Q9(ii)', 'B', P(11, 'Outline Einstein’s explanation of the photoelectric effect.'),
      [R('electromagnetic radiation consists of photons', 3), R('an electron absorbs the energy of one photon only', 3),
       R('energy gained by electron ≥ work function / formula & notation', 3)], 'phys-4-2',
      'einsteins-explanation', SQ(15, 'Outline Einstein’s explanation of the photoelectric effect.'), 9,
      stem=STEM9, id='phys-2025-hl-q9-ii'),
    T('9iii', 'Q9(iii)', 'B', P(11, 'Draw a labelled diagram of the structure of a photocell.'),
      [pt(S('vacuum in tube, cathode, anode', piece=k, psep=', '), 3, kind='criterion',
          **({'note_sel': S('[–1 if no label present on diagram]')} if k == 3 else {})) for k in (1, 2, 3)],
      'phys-4-2', 'photocell-structure', SQ(15, 'Draw a labelled diagram of the structure of a photocell.'), 9,
      id='phys-2025-hl-q9-iii', decision='[3 + 3 + 3] against the three parts printed on one line: 3 each.'),
    T('9iva', 'Q9(iv)(a)', 'B', [P(11, 'Calculate'), M('(a)', 11), P(11, 'the energy of a photon falling on the photocell,')],
      [R('Φ = 4.33 x 10⁻¹⁹ (J)', 3), FR(15, (110, 445, 190, 472), 'E = Φ + 1/2 mv²', 3),
       R('E = 6.57 x 10⁻¹⁹ J', 3)], 'phys-4-2', 'photon-energy',
      SQ(15, 'the energy of a photon falling on the photocell,'), 9, stem=[PCELL], id='phys-2025-hl-q9-iv-ab',
      decision=bundled('(a) and (b)', '(a)')),
    T('9ivb', 'Q9(iv)(b)', 'B', [P(11, 'Calculate'), M('(b)', 11), P(11, 'the frequency of the photon,')],
      [FR(15, (110, 508, 190, 535), 'fₚₕₒₜₒₙ = Eₚₕₒₜₒₙ/h', 3), R('fₚₕₒₜₒₙ = 9.91 x 10¹⁴ Hz', 3)], 'phys-4-2',
      'photon-frequency', SQ(15, 'the frequency of the photon,'), 6,
      stem=[PCELL, M('(a)', 11), P(11, 'the energy of a photon falling on the photocell,')]),
    T('9ivc', 'Q9(iv)(c)', 'B', [P(11, 'Calculate'), M('(c)', 11), P(11, 'the number of electrons emitted per second.')],
      [R('q = It', 3), R('number of electrons emitted per second = 3.12 x 10¹³', 3)], 'phys-4-2',
      'electrons-per-second', SQ(15, 'the number of electrons emitted per second.'), 6, stem=[PCELL],
      id='phys-2025-hl-q9-iv-c'),
    T('9v', 'Q9(v)', 'B', P(11, 'Explain how thermionic emission differs from photoelectric emission.'),
      [R('thermionic emission due to heat', 2), R('photoelectric effect due to electromagnetic radiation', 2)],
      'phys-4-1', 'thermionic-and-photoelectric',
      SQ(15, 'Explain how thermionic emission differs from photoelectric emission.'), 4, stem=STEM9,
      id='phys-2025-hl-q9-v'),
    T('9vi', 'Q9(vi)', 'B', P(11, 'Explain why X-ray production can be described', 'photoelectric effect.'),
      [R('X-ray production: electrons produce X-rays', 2, whole=True),
       R('photoelectric effect: X-rays produces electrons', 2, whole=True)], 'phys-4-2',
      'x-rays-inverse-photoelectric', SQ(15, 'Explain why X-ray production can be described as the inverse'), 4,
      stem=STEM9, id='phys-2025-hl-q9-vi'),
    # --------------------------------------------------------------- Q10 --
    T('10ia', 'Q10(i)(a)', 'B', [P(12, 'Explain what is meant by'), M('(a)', 12), P(12, 'specific heat capacity,')],
      [FR(16, (110, 89, 460, 111), 'energy // c = ΔE/(mΔθ)', 3, note_sel=LEGEND),
       R('required to raise the temperature of 1 kg by 1 K', 3, end='// notation')], 'phys-2-1',
      'specific-heat-capacity', SQ(16, 'specific heat capacity,'), 6, id='phys-2025-hl-q10-i-a',
      decision='Each line printed with its // side: one row per line, as printed.'),
    T('10ib', 'Q10(i)(b)', 'B', [P(12, 'Explain what is meant by'), M('(b)', 12), P(12, 'specific latent heat.')],
      [FR(16, (110, 141, 445, 164), 'energy // l = ΔE/m', 3, note_sel=LEGEND),
       R('required to change the state of 1 kg of substance', 3, end='// notation')], 'phys-2-1',
      'specific-latent-heat', SQ(16, 'specific latent heat.'), 6, id='phys-2025-hl-q10-i-b',
      decision='Each line printed with its // side: one row per line, as printed.'),
    T('10iia', 'Q10(ii)(a)', 'B', [P(12, 'Calculate'), M('(a)', 12), P(12, 'the energy gained by the calorimeter,')],
      [R('ΔEcal = mcΔθ', 3), R('ΔEcal = 1560 J', 3)], 'phys-2-1', 'energy-gained-by-calorimeter',
      SQ(16, 'the energy gained by the calorimeter,'), 6, stem=[STEAM, DATA10], id='phys-2025-hl-q10-ii-ab',
      decision=bundled('(a) and (b)', '(a)')),
    T('10iib', 'Q10(ii)(b)', 'B', [P(12, 'Calculate'), M('(b)', 12), P(12, 'the energy needed to melt the ice,')],
      [R('ΔEice = mlice', 3), R('ΔEice = 16500 J', 3)], 'phys-2-1', 'energy-to-melt-ice',
      SQ(16, 'the energy needed to melt the ice,'), 6, stem=[STEAM, DATA10]),
    TT('10iic', 'Q10(ii)(c)', 'B', [P(12, 'Calculate'), M('(c)', 12),
                                    P(12, 'the mass of steam added to the water in the calorimeter.')],
       [R('ΔEₛₜₑₐₘ = ( 1560 + 16500 + (0.5)(4180)(20) ) = 59860 (J)', 3), R('(ml)ₛₜₑₐₘ = 2.3 × 10⁶ m', 2),
        R('(mcΔθ)condensed steam = 334400 m', 2), R('mₛₜₑₐₘ = 0.0227 kg', 2)], 'phys-2-1', 'mass-of-steam',
       SQ(16, 'the mass of steam added to the water in the calorimeter.'), 9,
       stem=[STEAM, M('(a)', 12), P(12, 'the energy gained by the calorimeter,'), M('(b)', 12),
             P(12, 'the energy needed to melt the ice,'), DATA10],
       cells='The scheme prints the [2] for "(mcΔθ)condensed steam = 334400 m" beside the line at x 298 (p16, '
             'rendered and looked at), not in the marks column, so the reader does not take it as a cell: the '
             'printed cells are [3] + [2] + [2] + [2] = 9.'),
    T('10iii', 'Q10(iii)', 'B', P(12, 'State the equation that defines temperature on the Celsius scale.'),
      [TK(16, (84, 459, 200, 476), 'θ/°C = T/K – 273.15', 6,
          note_sel=S('[accept reference to 273(.15) for 3 marks]'))], 'phys-2-1', 'celsius-scale-equation',
      SQ(16, 'State the equation that defines temperature on the Celsius scale.'), 6, stem=[KELVIN],
      id='phys-2025-hl-q10-iii',
      decision='The scheme prints the theta as a Times New Roman "Ɵ" (U+019F, cropped and looked at: a '
               'bold italic theta); the runner reads a standalone "Ɵ" as θ, never as the "ti" ligature.'),
    T('10iv', 'Q10(iv)', 'B', P(12, 'Suggest a reason why the Celsius scale is used for most everyday purposes.'),
      [R('developed before Kelvin scale / based on melting & freezing point of water', 3)], 'phys-2-1',
      'why-celsius', SQ(16, 'Suggest a reason why the Celsius scale is used for most everyday purposes.'), 3,
      stem=[KELVIN], id='phys-2025-hl-q10-iv'),
    T('10v', 'Q10(v)', 'B', P(12, 'When a mercury-in-glass thermometer with no markings', 'water at 42 °C.'),
      [pt(S('100 units = 27 (cm)', '// axes labelled', piece=1, psep='//'), 3),
       pt(S('1 units = 0.27 (cm)', '// points plotted', piece=1, psep='//'), 3),
       pt(S('42 units = 11.34 (cm)', '// line of best fit', piece=1, psep='//'), 2),
       pt(S('length = ( 11.34 + 3 ) = 14.34 cm', '// length ≈ 14.34 cm', piece=1, psep='//'), 2)],
      'phys-2-1', 'mercury-thermometer-length',
      SQ(16, 'When a mercury-in-glass thermometer with no markings is placed in melting ice'), 10,
      id='phys-2025-hl-q10-v',
      decision='Two routes split by //: by calculation, or by a graph. ' + ROUTE_NOTE),
    T('10vi', 'Q10(vi)', 'B', P(12, 'Explain why it is necessary to have a standard thermometer.'),
      [R('different thermometers have different thermometric properties', 4)], 'phys-2-1',
      'standard-thermometer', SQ(16, 'Explain why it is necessary to have a standard thermometer.'), 4,
      id='phys-2025-hl-q10-vi'),
    # --------------------------------------------------------------- Q11 --
    T('11ia', 'Q11(i)(a)', 'B', [P(13, 'Explain what is meant by'), M('(a)', 13), P(13, 'resistance,')],
      [R('voltage', 4, end='// R = V/I', note_sel=LEGEND), R('per unit current', 2, end='// notation')],
      'phys-3-3', 'resistance', SQ(17, 'resistance,'), 6, id='phys-2025-hl-q11-i-a',
      decision='[4 + 2] against the two lines, each printed with its // side: 4 then 2.'),
    T('11ib', 'Q11(i)(b)', 'B', [P(13, 'Explain what is meant by'), M('(b)', 13), P(13, 'potential difference.')],
      [R('work done', 4, end='// V = W/q', note_sel=LEGEND), R('per unit charge', 2, end='// notation')],
      'phys-3-3', 'potential-difference', SQ(17, 'potential difference.'), 6, id='phys-2025-hl-q11-i-b',
      decision='[4 + 2] against the two lines, each printed with its // side: 4 then 2.'),
    T('11ii', 'Q11(ii)', 'B', P(13, 'Derive an expression for the total resistance of resistors', 'diagram.'),
      [R('Iₜₒₜ = I₁ + I₂', 3), FR(17, (235, 224, 270, 250), 'I = V/R', 3),
       FR(17, (235, 245, 305, 275), '1/Rₜₒₜ = 1/R₁ + 1/R₂', 3)], 'phys-3-3', 'resistors-in-parallel',
      SQ(17, 'Derive an expression for the total resistance of resistors'), 9, fig='q11-parallel'),
    T('11iii', 'Q11(iii)', 'B', P(13, 'Calculate the total resistance of the circuit when the', 'switch is closed.'),
      [R('Rparallel = 2.67 (Ω)', 3), R('Rcircuit = 10.67 Ω', 3)], 'phys-3-3', 'total-resistance-switch-closed',
      SQ(17, 'Calculate the total resistance of the circuit when the'), 6, stem=[SWITCH], fig='q11-switch'),
    T('11iv', 'Q11(iv)', 'B', P(13, 'Calculate the potential difference between X and Y when', 'the switch is closed.'),
      [FR(17, (80, 370, 400, 397), 'I = ( V/R = 12/10.67 ) =1.125 (A) // 2.67/10.67', 3, note_sel=LEGEND),
       R('VXY = ( R × I = 2.67 x 1.125 ) = 3 V', 3, end='// ( 0.25 x 12 ) = 3 V')], 'phys-3-3',
      'potential-difference-x-y', SQ(17, 'Calculate the potential difference between X and Y when the switch'),
      6, stem=[SWITCH], fig='q11-switch',
      decision='Each line printed with its // side: one row per line, as printed.'),
    T('11v', 'Q11(v)', 'B', P(13, 'What happens to the potential difference between X and', 'switch is opened?'),
      [R('potential difference increases', 4)], 'phys-3-3', 'switch-opened',
      SQ(17, 'What happens to the potential difference between X and Y when the switch is opened?'), 4,
      stem=[SWITCH], fig='q11-switch'),
    T('11vi', 'Q11(vi)', 'B', P(13, 'Explain what is meant by a thermistor.'),
      [R('resistance changes', 3), R('(significantly) with temperature', 3)], 'phys-3-3', 'thermistor',
      SQ(17, 'Explain what is meant by a thermistor.'), 6, stem=[DIVIDER], fig='q11-thermistor',
      id='phys-2025-hl-q11-vi'),
    T('11vii', 'Q11(vii)', 'B', P(13, 'The thermostat switches on an electric heater when the',
                                 'required to switch on the heater.'),
      [FR(17, (80, 597, 122, 625), 'R₂/R₁ = V₂/V₁', 3), FR(17, (80, 622, 160, 648), 'R₂ = 5000( 8/4 )', 3),
       R('R₂ = 10000 Ω', 3)], 'phys-3-3', 'thermistor-resistance',
      SQ(17, 'The thermostat switches on an electric heater when the output potential difference'), 9,
      stem=[DIVIDER], fig='q11-thermistor'),
    T('11viii', 'Q11(viii)', 'B', P(13, 'What change must be made to the resistance of the', 'higher temperature?'),
      [R('resistance must decrease', 4,
         note_sel=S('Note: valid reference to PTC thermistor acceptable for full marks'))], 'phys-3-3',
      'variable-resistor-change', SQ(17, 'What change must be made to the resistance of the variable resistor'), 4,
      stem=[DIVIDER], fig='q11-thermistor', id='phys-2025-hl-q11-viii'),
    # --------------------------------------------------------------- Q12 --
    T('12ai', 'Q12(a)(i)', 'B', P(14, 'State the nuclear equation for the reaction in the experiment.'),
      [G('equation', page=18, clip=(84, 140, 190, 168), expect='¹₁H + ⁷₃Li → ⁴₂He + ⁴₂He', marks=8,
         units=[2, 2, 2, 2], note='[4 × 2]: the scheme prices the four nuclei.',
         note_sel=S('[–2 additional incorrect species]'))],
      'phys-4-5', 'cockcroft-walton-equation',
      SQ(18, 'State the nuclear equation for the reaction in the experiment.'), 8, stem=STEM12A,
      fig='q12a-i-scheme', id='phys-2025-hl-q12a-i',
      decision='The nuclides carry their numbers stacked, which no line reading keeps: the row reads the '
               'equation\'s main line and the scheme\'s equation is the solution figure.'),
    T('12aii', 'Q12(a)(ii)', 'B', P(14, 'In addition to mass and energy, state two other properties', 'reaction.'),
      [R('momentum', 3), R('charge', 3)], 'phys-4-5', 'conserved-properties',
      SQ(18, 'In addition to mass and energy, state two other properties'), 6, stem=STEM12A,
      id='phys-2025-hl-q12a-ii'),
    T('12aiii', 'Q12(a)(iii)', 'B', P(14, 'A proton is an example of a baryon.', 'Justify your answer.'),
      [R('neutron', 3), R('no charge', 3)], 'phys-4-5', 'baryon-not-used',
      SQ(18, 'A proton is an example of a baryon.'), 6, stem=STEM12A, id='phys-2025-hl-q12a-iii'),
    T('12aiv', 'Q12(a)(iv)', 'B', P(14, 'Protons were accelerated through a potential difference of 1 MV.',
                                    'incident proton in joules.'),
      [R('E = qV', 3), R('E = 1.60218 x 10⁻¹³ J', 3)], 'phys-4-5', 'energy-of-incident-proton',
      SQ(18, 'Protons were accelerated through a potential difference of 1 MV.'), 6, stem=STEM12A,
      id='phys-2025-hl-q12a-iv'),
    T('12av', 'Q12(a)(v)', 'B', P(14, 'Given that the mass of the lithium nucleus', 'released due to the nuclear reaction.'),
      [R('mₚ = 1.67262 x 10⁻²⁷ (kg), mα = 6.64466 x 10⁻²⁷ (kg)', 3, whole=True), R('Δm = 2.938 x 10⁻²⁹ (kg)', 3),
       R('E = mc²', 3), R('E = 2.641 x 10⁻¹² J', 3)], 'phys-4-5', 'energy-released',
      SQ(18, 'Given that the mass of the lithium nucleus'), 12, stem=STEM12A, id='phys-2025-hl-q12a-v'),
    T('12avi', 'Q12(a)(vi)', 'B', P(14, 'Given that the alpha particles produced had a kinetic energy', 'are equivalent.'),
      [R('reference to energy of incident proton / reference to energy released in the reaction', 4),
       R('( 1.60218 x 10⁻¹³ + 2.64053 x 10⁻¹² ) = 2.801 × 10⁻¹² J', 2)], 'phys-4-5', 'verifying-mass-energy',
      SQ(18, 'Given that the alpha particles produced had a kinetic energy'), 6, stem=STEM12A,
      id='phys-2025-hl-q12a-vi', decision='[4 + 2] against the two lines: in the order printed.'),
    T('12avii', 'Q12(a)(vii)', 'B', P(14, 'Name the English physicist who proposed the existence of anti-particles'),
      [R('Dirac', 2)], 'phys-4-5', 'dirac', SQ(18, 'Name the English physicist who proposed'), 2,
      stem=[ANDERSON], id='phys-2025-hl-q12a-vii'),
    T('12aviii', 'Q12(a)(viii)', 'B', P(14, 'State a difference between an electron and a positron.'),
      [R('electron has a negative charge; positron has a positive charge // opposite charge', 3, note_sel=LEGEND)],
      'phys-4-5', 'electron-and-positron', SQ(18, 'State a difference between an electron and a positron.'), 3,
      stem=[ANDERSON], id='phys-2025-hl-q12a-viii',
      decision='One 3-mark line with its two sides: one row, as printed.'),
    T('12aix', 'Q12(a)(ix)', 'B', P(14, 'Write a nuclear equation for this decay.'),
      [G('equation', page=18, clip=(84, 738, 175, 766), expect='¹⁸₉F → ¹⁸₈O + ⁰₊₁e', marks=7,
         note='[7 × 1]: the scheme prices the equation one mark at a time.',
         note_sel=S('[–3 additional incorrect species]'))],
      'phys-4-4', 'positron-emission-equation', SQ(18, 'Write a nuclear equation for this decay.'), 7,
      stem=[PET], fig='q12a-ix-scheme', id='phys-2025-hl-q12a-ix',
      decision='The nuclides carry their numbers stacked, which no line reading keeps: the row reads the '
               'equation\'s main line and the scheme\'s equation is the solution figure.'),
    T('12bi', 'Q12(b)(i)', 'B', P(15, 'Draw a labelled diagram of an a.c. generator.'),
      [C('magnet', 3), C('coil', 3), C('slip rings and brushes', 3)], 'phys-3-6', 'ac-generator',
      SQ(19, 'Draw a labelled diagram of an a.c. generator.'), 9, id='phys-2025-hl-q12b-i'),
    T('12bii', 'Q12(b)(ii)', 'B', P(15, 'What is the principal energy transformation that takes place'),
      [R('kinetic', 3), R('to electrical', 3)], 'phys-3-6', 'generator-energy-transformation',
      SQ(19, 'What is the principal energy transformation that takes place'), 6, id='phys-2025-hl-q12b-ii'),
    T('12biii', 'Q12(b)(iii)', 'B', P(15, 'Draw a circuit diagram showing how a smooth d.c. output', 'a.c. source.'),
      [C('four diodes', 3), C('arrangement as bridge rectifier', 3), C('smoothing capacitor', 3)], 'phys-3-3',
      'smooth-dc-from-ac', SQ(19, 'Draw a circuit diagram showing how a smooth d.c. output'), 9,
      id='phys-2025-hl-q12b-iii'),
    T('12biv', 'Q12(b)(iv)', 'B', P(15, 'State the principle on which the induction motor is based.'),
      [R('electromagnetic induction', 6)], 'phys-3-6', 'induction-motor-principle',
      SQ(19, 'State the principle on which the induction motor is based.'), 6, id='phys-2025-hl-q12b-iv'),
    T('12bv', 'Q12(b)(v)', 'B', P(15, 'State one advantage of an induction motor over a simple d.c. motor.'),
      [R('no brushes', 3)], 'phys-3-6', 'induction-motor-advantage',
      SQ(19, 'State one advantage of an induction motor over a simple d.c. motor.'), 3, id='phys-2025-hl-q12b-v'),
    T('12bvi', 'Q12(b)(vi)', 'B', P(15, 'A simple induction motor is connected to a 50 Hz a.c. supply.',
                                    'number of revolutions per minute of the motor.'),
      [R('3000 rpm', 6)], 'phys-3-6', 'induction-motor-rpm',
      SQ(19, 'A simple induction motor is connected to a 50 Hz a.c. supply.'), 6, id='phys-2025-hl-q12b-vi'),
    T('12bvii', 'Q12(b)(vii)', 'B', P(15, 'List three principal components of a moving-coil galvanometer.'),
      [R('magnet', 2), R('coil', 2), R('spring', 2)], 'phys-3-5', 'galvanometer-components',
      SQ(19, 'List three principal components of a moving-coil galvanometer.'), 6, id='phys-2025-hl-q12b-vii'),
    T('12bviii', 'Q12(b)(viii)', 'B', P(15, 'A galvanometer has a resistance of 40 Ω.', 'across its terminals.'),
      [R('V = RI', 3), R('V = 0.08 V', 2)], 'phys-3-3', 'galvanometer-maximum-pd',
      SQ(19, 'A galvanometer has a resistance of 40 Ω.'), 5, id='phys-2025-hl-q12b-viii'),
    T('12bix', 'Q12(b)(ix)', 'B', P(15, 'Draw a circuit diagram to show how a galvanometer can be converted'),
      [C('large resistor', 3), C('in series with the galvanometer', 3)], 'phys-3-3', 'galvanometer-to-voltmeter',
      SQ(19, 'Draw a circuit diagram to show how a galvanometer can be converted to a voltmeter.'), 6,
      id='phys-2025-hl-q12b-ix'),
    # --------------------------------------------------------------- Q13 --
    T('13i', 'Q13(i)', 'B', P(16, 'Explain what is meant by (a) a magnetic field (b) a magnetic field line.'),
      [R('space in which magnetic force is experienced', 4, label=S('(a)')),
       R('line showing direction of magnetic field', 3, label=S('(b)'))], 'phys-3-4', 'magnetic-field',
      SQ(20, 'Explain what is meant by (a) a magnetic field'), 7, stem=PASSAGE, id='phys-2025-hl-q13-i',
      decision='One cell [4 + 3] prices (a) and (b) together: one card, (a) 4 and (b) 3 in the order printed.'),
    T('13ii', 'Q13(ii)', 'B', P(16, 'Distinguish between scalar and vector quantities.'),
      [R('scalar has magnitude only', 4), R('vector has magnitude and direction', 3)], 'phys-1-1',
      'scalars-and-vectors', SQ(20, 'Distinguish between scalar and vector quantities.'), 7,
      stem=PASSAGE + [VECTOR], id='phys-2025-hl-q13-ii', decision='[4 + 3] against the two lines: in order.'),
    TT('13iiia', 'Q13(iii)(a)', 'B', [WIRE, P(16, 'Calculate', after='flux density 150 mT.'), M('(a)', 16),
                                      P(16, 'the resistance of the wire,')],
       [R('A = 1.119 × 10⁻⁷ (m²)', 2), R('p = RA/l', 2), R('R = 0.5 Ω', 2)], 'phys-3-3', 'resistance-of-wire',
       SQ(20, 'the resistance of the wire,'), 6, fig='q13-wire', id='phys-2025-hl-q13-iii-a',
       cells='The scheme prints [2] against "A = 1.119 × 10⁻⁷ (m²)" (p20, y 411); the diagram\'s "0.225 V" '
             'label shares that baseline, so the reader files the cell under the label (rendered and looked at): '
             'the printed cells are [2] + [2] + [2] = 6.'),
    T('13iiib', 'Q13(iii)(b)', 'B', [WIRE, P(16, 'Calculate', after='flux density 150 mT.'), M('(b)', 16),
                                     P(16, 'the force acting on the wire.')],
      [R('I = V/R = 0.45 (A)', 2), R('F = BIl', 2), R('F = 3.375 × 10⁻³ N', 2), R('out of the page', 2)],
      'phys-3-5', 'force-on-wire', SQ(20, 'the force acting on the wire.'), 8, fig='q13-wire'),
    T('13iv', 'Q13(iv)', 'B', P(16, 'Calculate the average EMF induced in the coil.'),
      [FR(20, (80, 592, 135, 620), 'E = (-) dΦ/(dt)', 4), R('E = 61.4 V', 3)], 'phys-3-6', 'average-emf',
      SQ(20, 'Calculate the average EMF induced in the coil.'), 7, stem=[COIL], id='phys-2025-hl-q13-iv'),
    T('13va', 'Q13(v)(a)', 'B', P(16, 'Explain what is meant by self-induction.'),
      [R('changing current in a coil / changing magnetic field produced by a coil', 3),
       R('induces a (back) emf in the coil itself', 2)], 'phys-3-6', 'self-induction',
      SQ(20, 'Explain what is meant by self-induction.'), 5, id='phys-2025-hl-q13-v',
      decision=bundled('(a) and (b)', '(a)')),
    T('13vb', 'Q13(v)(b)', 'B', P(16, 'State one practical use of self-induction.'),
      [R('examples : smoothing in power supply units / tuning circuits / stage lighting', 2, whole=True)],
      'phys-3-6', 'uses-of-self-induction', SQ(20, 'State one practical use of self-induction.'), 2,
      stem=[M('(a)', 16), P(16, 'Explain what is meant by self-induction.')]),
    T('13via', 'Q13(vi)(a)', 'B', P(16, 'A step-down transformer converts 345 kV to 230 V.',
                                    'turns in the primary coil to the number of turns in the secondary coil.'),
      [FR(21, (110, 94, 130, 122), 'Nₛ/Nₚ', 3), R('1500:1', 2)], 'phys-3-6', 'transformer-turns-ratio',
      SQ(21, 'A step-down transformer converts 345 kV to 230 V.'), 5),
    T('13vib', 'Q13(vi)(b)', 'B', P(16, 'Explain why a transformer does not work with direct current.'),
      [R('no changing current / no changing magnetic field', 2)], 'phys-3-6', 'transformer-and-dc',
      SQ(21, 'Explain why a transformer does not work with direct current.'), 2, id='phys-2025-hl-q13-vi-b'),
    T('13vii', 'Q13(vii)', 'B', P(16, 'The diagram shows a graph of current I', 'appliance.', end_nth=2),
      [FR(21, (300, 265, 360, 300), 'Irms = I₀/(√2)', 4), R('Irms = 5.65 A', 3)], 'phys-3-6', 'rms-current',
      SQ(21, 'Calculate the RMS current flowing in the'), 7, qfig='q13-vii-question', fig='q13-vii-scheme',
      decision='The ask points at the graph printed beside it: the question is shown as printed, with the '
               'graph. The formula is read from where it is printed (the root sign\'s own overbar is not '
               'a fraction bar); the scheme\'s print of it is the solution figure.'),
    # --------------------------------------------------------------- Q14 --
    T('14ai', 'Q14(a)(i)', 'B', P(17, 'State Hooke’s law.'),
      [R('(restoring) force', 2, end='// F = (–)ks', note_sel=LEGEND), R('proportional to displacement', 2, end='// notation')],
      'phys-1-3', 'hookes-law', SQ(22, 'State Hooke’s law.'), 4, id='phys-2025-hl-q14a-i',
      decision='Each line printed with its // side: one row per line, as printed.'),
    T('14aii', 'Q14(a)(ii)', 'B', P(17, 'Using Hooke’s law, show that the mass executes simple harmonic motion.'),
      [R('F = ma', 3), R('F = (–)ks', 3), R('(k & m are constant means) a ∝ (–)s', 3)], 'phys-1-3',
      'hookes-law-gives-shm', SQ(22, 'Using Hooke’s law, show that the mass executes simple harmonic motion.'), 9,
      stem=[SPRING], id='phys-2025-hl-q14a-ii'),
    T('14aiii', 'Q14(a)(iii)', 'B', P(17, 'For a mass undergoing simple harmonic motion, explain what is meant by amplitude.'),
      [R('maximum displacement', 6,
         note_sel=S('[accept reference to equilibrium position or extreme positions for 3 marks]'))],
      'phys-1-3', 'amplitude', SQ(22, 'For a mass undergoing simple harmonic motion, explain what is meant'), 6,
      id='phys-2025-hl-q14a-iii'),
    T('14aiv', 'Q14(a)(iv)', 'B', P(17, 'Calculate the period of the oscillation.'),
      [FR(22, (84, 402, 265, 430), 'a = (–)ω²s or ω² = k/m', 3), FR(22, (84, 430, 120, 458), 'T = 2π/ω', 3),
       R('T = 0.49 s', 3)], 'phys-1-3', 'period-of-oscillation',
      SQ(22, 'Calculate the period of the oscillation.'), 9, stem=[MASS150], id='phys-2025-hl-q14a-iv'),
    T('14bi', 'Q14(b)(i)', 'B', P(17, 'State which glass Y or Z would be suitable for the cladding.', 'Justify your answer.'),
      [R('Y', 4), R('(lower refractive index in cladding allows) total internal reflection', 2)], 'phys-2-3',
      'choosing-the-cladding', SQ(23, 'State which glass Y or Z would be suitable for the cladding.'), 6,
      stem=FIBRE, fig='q14b-table', id='phys-2025-hl-q14b-i', decision='[4 + 2] against the two lines: in order.'),
    T('14bii', 'Q14(b)(ii)', 'B', P(17, 'Explain what is meant by critical angle.'),
      [R('angle of incidence (in denser medium causing)', 4), R('angle of refraction of 90°', 2)], 'phys-2-3',
      'critical-angle', SQ(23, 'Explain what is meant by critical angle.'), 6, id='phys-2025-hl-q14b-ii',
      decision='[4 + 2] against the two lines: in order.'),
    T('14biii', 'Q14(b)(iii)', 'B', P(17, 'Explain, with the aid of a labelled diagram, how a signal is transmitted'),
      [C('light ray showing reflection in fibre', 4), R('stated: i > C', 2, end='total internal reflection', whole=True)],
      'phys-2-3', 'signal-in-optical-fibre',
      SQ(23, 'Explain, with the aid of a labelled diagram, how a signal is transmitted'), 6, stem=FIBRE_A,
      id='phys-2025-hl-q14b-iii', decision='[4 + 2] against the two lines: in order.'),
    T('14biv', 'Q14(b)(iv)', 'B', P(17, 'Calculate the critical angle between the core and the cladding.'),
      [FR(23, (84, 405, 220, 433), 'n = (sin i)/(sin r) or n = 1/(sin C)', 3), R('C = 78.4°', 3)], 'phys-2-3',
      'critical-angle-calculation', SQ(23, 'Calculate the critical angle between the core and the cladding.'), 6,
      stem=FIBRE, fig='q14b-table', id='phys-2025-hl-q14b-iv'),
    T('14bv', 'Q14(b)(v)', 'B', P(17, 'Identify the type of glass, from the table, in which light travels fastest.'),
      [R('Y', 4, note_sel=S('[accept n = c₁/c₂ for 3 marks]'))], 'phys-2-3', 'fastest-glass',
      SQ(23, 'Identify the type of glass, from the table, in which light travels fastest.'), 4, stem=FIBRE,
      fig='q14b-table', id='phys-2025-hl-q14b-v'),
    T('14ci', 'Q14(c)(i)', 'B', P(18, 'Determine the number of neutrons in an atom of Iodine–131.'),
      [R('number of neutrons = 131 – 53 = 78', 4)], 'phys-4-4', 'neutrons-in-iodine-131',
      SQ(24, 'Determine the number of neutrons in an atom of Iodine–131.'), 4, stem=IODINE,
      id='phys-2025-hl-q14c-i'),
    T('14cii', 'Q14(c)(ii)', 'B', P(18, 'Write a nuclear equation to represent the beta decay of Iodine–131.'),
      [G('equation', page=24, clip=(84, 182, 190, 206), expect='¹³¹₅₃I → ¹³¹₅₄Xe + ⁰₋₁β', marks=7,
         note='[7 × 1]: the scheme prices the equation one mark at a time.',
         note_sel=S('[–3 additional incorrect species]'))],
      'phys-4-4', 'beta-decay-of-iodine-131',
      SQ(24, 'Write a nuclear equation to represent the beta decay of Iodine–131.'), 7, stem=IODINE,
      fig='q14c-ii-scheme', id='phys-2025-hl-q14c-ii',
      decision='The nuclides carry their numbers stacked, which no line reading keeps: the row reads the '
               'equation\'s main line and the scheme\'s equation is the solution figure.'),
    T('14ciii', 'Q14(c)(iii)', 'B', P(18, 'Calculate the decay constant of Iodine–131.'),
      [FR(24, (84, 256, 126, 286), 'T 1/2 = ln2/λ', 3), R('λ = 1.0028 x 10⁻⁶ s⁻¹', 3)], 'phys-4-4',
      'decay-constant', SQ(24, 'Calculate the decay constant of Iodine–131.'), 6, stem=IODINE,
      id='phys-2025-hl-q14c-iii'),
    T('14civa', 'Q14(c)(iv)(a)', 'B', [SAMPLE, P(18, 'Calculate', after='contains 2 × 10¹⁵ atoms.'), M('(a)', 18),
                                       P(18, 'the rate of decay of the sample,')],
      [R('A = (–)λN', 3), R('A = 2.01 x 10⁹ s⁻¹', 2)], 'phys-4-4', 'rate-of-decay',
      SQ(24, 'the rate of decay of the sample,'), 5, stem=IODINE, id='phys-2025-hl-q14c-iv',
      decision=bundled('(a) and (b)', '(a)')),
    T('14civb', 'Q14(c)(iv)(b)', 'B', [SAMPLE, P(18, 'Calculate', after='contains 2 × 10¹⁵ atoms.'), M('(b)', 18),
                                       P(18, 'how long it would take for 1.75 × 10¹⁵ nuclei to decay.')],
      [R('reference to ⅛', 3), R('24 days', 3)], 'phys-4-4', 'time-for-nuclei-to-decay',
      SQ(24, 'how long it would take for 1.75 × 10¹⁵ nuclei to decay.'), 6, stem=IODINE),
    T('14di', 'Q14(d)(i)', 'B', P(18, 'State Coulomb’s law.'),
      [FR(25, (84, 77, 490, 103),
          'force between two charges is proportional to product of the charges // F ∝ q₁q₂/d²', 3,
          note_sel=LEGEND),
       R('and inversely proportional to the square of distance between them', 3, end='// notation')],
      'phys-3-1', 'coulombs-law', SQ(25, 'State Coulomb’s law.'), 6, id='phys-2025-hl-q14d-i',
      decision='Each line printed with its // side: one row per line, as printed. The old card cited Q14(d)(i), '
               'which the paper prints; it was an orphan only because the census mis-keyed Q14(d).'),
    T('14dii', 'Q14(d)(ii)', 'B', P(18, 'Explain what is meant by electric field strength.'),
      [FR(25, (84, 150, 325, 177), 'force per // E = F/q', 2, note_sel=LEGEND),
       R('unit charge', 2, end='// notation')], 'phys-3-2', 'electric-field-strength',
      SQ(25, 'Explain what is meant by electric field strength.'), 4, id='phys-2025-hl-q14d-ii',
      decision='Each line printed with its // side: one row per line, as printed. The old card cited '
               'Q14(d)(ii), which the paper prints; it was an orphan only because the census mis-keyed Q14(d).'),
    T('14diii', 'Q14(d)(iii)', 'B', P(18, 'Describe how an electric field pattern may be demonstrated'),
      [R('apparatus: oil and semolina/seeds', 2, whole=True),
       R('method: high voltage connected to two plates', 2, whole=True),
       R('observation: lines of semolina/seeds show electric field pattern', 2, whole=True)], 'phys-3-2',
      'demonstrating-field-patterns', SQ(25, 'Describe how an electric field pattern may be demonstrated'), 6,
      id='phys-2025-hl-q14d-iii',
      decision='The old card cited Q14(d)(iii), which the paper prints; it was an orphan only because the '
               'census mis-keyed Q14(d).'),
    T('14div', 'Q14(d)(iv)', 'B', P(18, 'Draw a diagram to show the electric field pattern around the sphere.'),
      [C('radial lines from surface', 3), C('direction away (from surface)', 3)], 'phys-3-2',
      'field-around-charged-sphere', SQ(25, 'Draw a diagram to show the electric field pattern around the sphere.'),
      6, stem=[SPHERE]),
    T('14dv', 'Q14(d)(v)', 'B', P(18, 'Calculate the total charge on the sphere.'),
      [FR(25, (84, 425, 340, 455), 'F = q₁q₂/(4πε₀d²) or E = F/q or E = q/(4πε₀d²)', 3),
       R('q = 1.77 x 10⁻⁸ C', 3)], 'phys-3-2', 'charge-on-sphere',
      SQ(25, 'Calculate the total charge on the sphere.'), 6, stem=[SPHERE], id='phys-2025-hl-q14d-v',
      decision='The old card cited Q14(d)(v), which the paper prints; it was an orphan only because the census '
               'mis-keyed Q14(d).'),
]

ANSWER_VARIANTS = {
    '2ii': [
        ('card', 'Length of card and its time',
         [pt(S('(measure) length l of card', '// (measure) distance between dots', piece=1, psep='//'), 3),
          pt(S('(measure) time for l', '// (measure) time between dots', piece=1, psep='//'), 3),
          R('v = l/t', 3)]),
        ('dots', 'Distance and time between dots',
         [pt(S('(measure) length l of card', '// (measure) distance between dots', piece=2, psep='//'), 3),
          pt(S('(measure) time for l', '// (measure) time between dots', piece=2, psep='//'), 3),
          R('v = l/t', 3)]),
    ],
    '2vib': [
        ('air-track', 'Air track',
         [pt(S('cushion of air or clean air track', '// oil wheels or clean track', piece=1, psep='//'), 2),
          pt(S('horizontal air track', '// slope track', piece=1, psep='//'), 2,
             note_sel=S('[allow 4 marks for adjust the track until frictional force = gravitational force]'))]),
        ('track', 'Track with wheels',
         [pt(S('cushion of air or clean air track', '// oil wheels or clean track', piece=2, psep='//'), 2),
          pt(S('horizontal air track', '// slope track', piece=2, psep='//'), 2,
             note_sel=S('[allow 4 marks for adjust the track until frictional force = gravitational force]'))]),
    ],
    '10v': [
        ('calculation', 'By calculation',
         [pt(S('100 units = 27 (cm)', '// axes labelled', piece=1, psep='//'), 3),
          pt(S('1 units = 0.27 (cm)', '// points plotted', piece=1, psep='//'), 3),
          pt(S('42 units = 11.34 (cm)', '// line of best fit', piece=1, psep='//'), 2),
          pt(S('length = ( 11.34 + 3 ) = 14.34 cm', '// length ≈ 14.34 cm', piece=1, psep='//'), 2)]),
        ('graph', 'By a graph',
         [pt(S('100 units = 27 (cm)', '// axes labelled', piece=2, psep='//'), 3, kind='criterion'),
          pt(S('1 units = 0.27 (cm)', '// points plotted', piece=2, psep='//'), 3, kind='criterion'),
          pt(S('42 units = 11.34 (cm)', '// line of best fit', piece=2, psep='//'), 2, kind='criterion'),
          pt(S('length = ( 11.34 + 3 ) = 14.34 cm', '// length ≈ 14.34 cm', piece=2, psep='//'), 2)]),
    ],
}

RETAINED = {
    'phys-2025-hl-q6-h-ii': 'Q6(h) is one of the eight 7-mark parts of "Answer any eight" (8 x 7), and the scheme '
                            'prices (i) and (ii) in one cell [4 + 3]: one card for the part, phys-2025-hl-q6-h-i.',
}
WITHDRAW = {'phys-2025-hl-q6-h-ii': ('phys-2025-hl-q6-h-i', RETAINED['phys-2025-hl-q6-h-ii'])}

FIGURES = {
    # key suffix: (doc, page, rect in PDF points, credit, letters, alt, solution)
    'q1-table': ('paper', 2, (52, 322, 545, 413), SEC, [], 'Table of the metre stick data: position of force on metre stick (cm) 2.0, 11.2, 40.1, 72.7, 82.9; force (N) 3.4, 3.0, 2.0, 5.5, 3.0; direction up, down, down, up, down.', False),
    'q2-table': ('paper', 3, (52, 161, 544, 225), SEC, [], 'Table of the trolley data: mass of A 200 g, mass of B 250 g, sA 10 cm, tA 185 ms, sB 8 cm, tB 190 ms.', False),
    'q3-graph': ('paper', 4, (62, 146, 534, 507), SEC, [], 'Graph of l (m), from -0.10 to 0.50, against 1/f (Hz⁻¹), from 0.000 to 0.006: six plotted points lie on a straight line drawn from just below the origin up to the last point at 0.005.', False),
    'q4-table': ('paper', 5, (52, 138, 530, 202), SEC, [], 'Table of the angles recorded: i (°) 20, 30, 40, 50, 60, 70; r (°) 13, 19, 27, 30, 35, 39.', False),
    'q4-block': ('paper', 5, (236, 220, 358, 316), SEC, [], 'Diagram of a rectangle, the glass block seen from above, with a ray drawn as an arrow coming down from the upper left to meet its top face.', False),
    'q4-sheet': ('paper', 5, (210, 500, 386, 614), SEC, [], 'Line drawing in perspective of a rectangular glass block lying flat on its largest face on a square sheet of paper.', False),
    'q5-table': ('paper', 6, (52, 115, 545, 179), SEC, [], 'Table of the readings: V (V) 1, 2, 3, 4, 5, 6, 7; I (mA) 25, 47, 68, 80, 91, 100, 104.', False),
    'q6c-diagram': ('paper', 7, (430, 262, 548, 405), SEC, ['X', 'Y'], 'Diagram of two horizontal lines 20 m apart: particle Y on the upper line with a short arrow pointing down, labelled 5 m s⁻¹, and particle X on the lower line, the ground, with an arrow pointing up, labelled 15 m s⁻¹.', False),
    'q8-diagram': ('paper', 10, (155, 222, 440, 392), SEC, [], 'Diagram of a laser beam passing through a diffraction grating to a white screen; dashed lines from the grating, with the angle between them marked 49°, reach the two images marked n = 2 on the screen, with a column of marks between them.', False),
    'q11-parallel': ('paper', 13, (160, 160, 415, 262), SEC, [], 'Circuit diagram of two resistors, R1 and R2, connected in parallel between two leads.', False),
    'q11-switch': ('paper', 13, (378, 300, 547, 433), SEC, ['X', 'Y'], 'Circuit diagram: a 12 V supply connected across an 8 Ω resistor and a second 8 Ω resistor in series; point X lies between them, and a switch from X leads to a 4 Ω resistor that joins point Y at the bottom of the lower 8 Ω resistor.', False),
    'q11-thermistor': ('paper', 13, (395, 515, 552, 690), SEC, [], 'Potential divider between 12 V and 0 V: a variable resistor above a thermistor, with the output Vout taken across the thermistor.', False),
    'q13-wire': ('paper', 16, (380, 325, 545, 445), SEC, ['S', 'N'], 'Diagram of a straight wire lying between an S pole above and an N pole below, with five field arrows pointing up from N to S across it; the wire is connected in a loop to a 0.225 V cell.', False),
    'q13-vii-question': ('paper', 16, (52, 634, 545, 746), SEC, [], 'The printed question: (vii) The diagram shows a graph of current I against time t for an alternating current flowing through an appliance. Calculate the RMS current flowing in the appliance. (7) Beside it, a graph of I (A), from -10 to 10, against t (s), from 0.00 to 0.02, showing one full cycle of a sine-shaped curve.', False),
    'q14b-table': ('paper', 17, (52, 413, 545, 477), SEC, [], 'Table of the refractive index of three types of glass: core 1.47, Y 1.44, Z 1.50.', False),
    'q12a-i-scheme': ('scheme', 18, (80, 141, 195, 170), SEC, [], "The marking scheme's equation: ¹₁H + ⁷₃Li → ⁴₂He + ⁴₂He, each nucleus printed with its mass number above and its atomic number below.", True),
    'q12a-ix-scheme': ('scheme', 18, (80, 738, 170, 766), SEC, [], "The marking scheme's equation: ¹⁸₉F → ¹⁸₈O + ⁰₊₁e, each particle printed with its mass number above and its atomic number below.", True),
    'q14c-ii-scheme': ('scheme', 24, (80, 176, 175, 210), SEC, [], "The marking scheme's equation: ¹³¹₅₃I → ¹³¹₅₄Xe + ⁰₋₁β, each particle printed with its mass number above and its atomic number below.", True),
    'q13-vii-scheme': ('scheme', 21, (300, 264, 356, 295), SEC, [], "The marking scheme's formula: I rms (rms as a subscript) equals I0 over the square root of 2, set as a fraction.", True),
}
