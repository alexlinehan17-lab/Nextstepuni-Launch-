"""Physics 2023 Ordinary Level — reviewed task ledger, correcting the sitting in place.

Independent visual sweep (2026-10-28), every page rendered and read:
  * The paper (LC021GLP000EV), 16 pages: p1 cover (the 2023 papers were
    adjusted for disruption to learning), p2-p4 Section A Questions 1-5 (any
    three, 40 marks each), p5-p14 Section B Questions 6-14 (any five, 56 marks
    each), p15 acknowledgements (images on pages 3, 5-14), p16 back cover.
  * The marking scheme, 24 pages: p1 cover, p2 note on published schemes, p3
    marking conventions (solidus, double solidus), p4 annotations, p5 Irish
    bonus table, p6-p21 Questions 1-14, p22 blank (footer only), p23 blank,
    p24 back cover.

Every printed ask is carded. The paper prints a group mark after a run of
romans ("(12)" closing Q1(i)): GROUP_TOTALS. Q6 is any eight of (a)-(l) at 7
each (8 x 7): one card per letter. Q14 is any two of (a)-(d): every part is
carded. Most rows carry the scheme's partial allowance ("[accept partial answer
for 3]") as their note. A list of items under one sum with no order ("object,
mirror, screen [6 + 3 + 3]") is a menu priced step by step. Q5(i)'s inline
(a), (b), (c) are priced [3] each: one card each. Q13(iv)'s (a) and (b) share
one cell [4 + 3]: one card.

The paper sets 1/l (Q4(v), (vi)) as a stacked fraction whose glyphs the text
layer breaks, the tritium nuclide (Q13(iv), (v)) as stacked numbers, and
Q3(ix)'s note "E = m_ice l + m_ice c_water Δθ_ice" with subscript words the text
layer cannot lower: those asks are shown as printed crops (question figures).

The sitting was already carded (108 authored cards, all shipped). Every task is
re-derived from the PDFs at the scheme's own mark boundaries and every shipped
id is kept, mapped (`id=`) to the task it was carding. The five asks the bank
had excluded (Q10(iii), Q11(viii), Q14(b)(ii), Q14(c)(iii), Q14(d)(ii)) and the
six open ones (Q3(i), (ii), Q4(v), (vi), Q8(ii), (iii)) are carded.
"""
from phys_review_lib import Q, SQ, S, M, G, pt, anyn, T, L

YEAR, LEVEL = 2023, 'ol'
REVIEWED_AT = '2026-10-28'
BASELINE_COMMIT = '99ec7f0a0d6b243f4d5a1dc9b14a6a958e98095e'

SOURCES = {
    'paper': {'path': 'examiner-reports/physics/papers/2023-ol-paper.pdf', 'fileid': 'LC021GLP000EV.pdf',
              'sha256': 'd6dff89c7bd732fffcd14557a3d16d71cf17f516ca380ae7234af028997e4511', 'pages': 16},
    'scheme': {'path': 'examiner-reports/physics/schemes/2023-ol.pdf', 'fileid': 'LC021GLP000EV.pdf',
               'sha256': '8bd4e67afb47942be5dc8087860322d606b05a71009d89d2715a0f8fc7ab4b48', 'pages': 24},
}

PAGE_ROLES = {
    'paper': {1: 'cover', **{p: 'questions' for p in range(2, 15)}, 15: 'acknowledgements', 16: 'back-cover'},
    'scheme': {1: 'cover', 2: 'note', 3: 'conventions', 4: 'annotations', 5: 'irish-bonus',
               **{p: 'marking' for p in range(6, 22)}, 22: 'blank', 23: 'blank', 24: 'back-cover'},
}

LETTERED = {6, 14}

QUESTION_TOTALS = {**{n: 40 for n in range(1, 6)}, **{n: 56 for n in range(6, 14)},
                   14: 112}   # any two of (a)-(d), 28 each: all four carded
PART_TOTALS = {**{(14, x): 28 for x in 'abcd'}}
BEST_OF = {6: (8, 7)}
GROUP_TOTALS = {
    (1, ('i',)): 12, (1, ('ii', 'iii')): 10, (1, ('iv', 'v')): 18,
    (2, ('i', 'ii')): 18, (2, ('iii', 'iv', 'v', 'vi')): 22,
    (3, ('i', 'ii')): 6, (3, ('iii', 'iv')): 8, (3, ('v', 'vi')): 8, (3, ('vii',)): 9, (3, ('viii', 'ix')): 9,
    (4, ('i', 'ii')): 15, (4, ('iii', 'iv')): 12, (4, ('v', 'vi')): 13,
    (5, ('i', 'ii')): 15, (5, ('iii',)): 13, (5, ('iv', 'v')): 12,
    (7, ('i', 'ii', 'iii')): 21, (7, ('iv', 'v', 'vi')): 21, (7, ('vii', 'viii')): 14,
    (8, ('i', 'ii')): 15, (8, ('iii', 'iv')): 15, (8, ('v', 'vi', 'vii')): 26,
    (9, ('i', 'ii', 'iii')): 21, (9, ('iv', 'v', 'vi')): 20, (9, ('vii', 'viii', 'ix')): 15,
    (10, ('i', 'ii', 'iii', 'iv', 'v')): 36, (10, ('vi', 'vii', 'viii', 'ix')): 20,
    (11, ('i', 'ii', 'iii', 'iv')): 24, (11, ('v', 'vi')): 15, (11, ('vii', 'viii', 'ix')): 17,
    (12, ('i', 'ii', 'iii')): 15, (12, ('iv', 'v', 'vi')): 18, (12, ('vii', 'viii', 'ix', 'x')): 23,
    **{(13, (r,)): 7 for r in ('i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii')},
}
CHECKSUMS = {}

SCAN_PAGES = {'paper': range(2, 15)}
SELECTION_SCAN = [
    ('paper', 2, 'the following', 'Q1 "The student recorded the following results": a reference to the table.'),
    ('paper', 3, 'the following', 'Q3 "The following results were recorded": a reference to the results.'),
    ('paper', 4, 'the following', 'Q4 "The student recorded the following results": a reference to the table.'),
    ('paper', 4, 'the following', 'Q5 "The student recorded the following results": a reference to the table.'),
    ('paper', 5, 'the following', 'Q6 "Answer any eight of the following parts": a best-eight of (a)-(l) at 7 '
                                  'each (8 x 7); every part is carded.'),
    ('paper', 5, 'the following', 'Q6(d) "Which of the following is the unit of work?": the ask\'s own options; '
                                  'one answer.'),
    ('paper', 8, 'or', 'Q9(vi) "side, A, B or C": the ask\'s own options; one answer.'),
    ('paper', 9, 'or', 'Q10 lead-in "a doorway or a window": description.'),
    ('paper', 12, 'the following', 'Q13 "Read the following passage": a reference to the passage.'),
    ('paper', 13, 'any two', 'Q14 "Answer any two of the following parts": whole-part choice; every part is carded.'),
    ('paper', 13, 'the following', 'Q14, the same rubric.'),
]
ASK_SCAN_PAGES = {'paper': range(2, 15)}
ASK_EXEMPT = [
    (9, 'When two sound waves meet they can undergo interference.',
     'Q10 lead-in to (iii): a description, not an ask; lifted into its stem.'),
    (12, 'normal hydrogen but a different mass number. When tritium', 'Q13 passage text, not an ask; lifted into the stems.'),
    (14, 'When a current-carrying conductor is placed in', 'Q14(d) lead-in to (iii): a description, not an ask; lifted '
                                                         'into its stem.'),
]

ROUTES = {}
SEC = 'State Examinations Commission'

CRIT = 'The scheme prints no answer here, only what earns the marks.'
NOLABEL = S('[–1 if no label present on diagram]')
LEGEND = S('Answers that are separated by a double solidus, //, are answers which are mutually',
           'with a partial answer from the other side.', page=3)
EXPT = 'A "describe an experiment" part: the scheme prices apparatus, method and observation and prints no answer.'
ORDERED = ('The scheme prints these items under one sum, {cell}, and names no order: a response earns the marks '
           'step by step.')
LINKED = ('{w} reads to the figure-pointer check as a printed figure; the ask is the student\'s own, so the card '
          'links its exam page.')


def PA(n):
    """The scheme's partial allowance printed under a row."""
    return S(f'[accept partial answer for {n}]')


def P(page, start, end=None, **kw):
    return Q(page, start, end, **kw)


def R(text, marks, end=None, **kw):
    """A row lifted whole from the task's scheme page."""
    return pt(S(text, end), marks, **kw)


def C(text, marks, end=None, note=CRIT, **kw):
    """A criterion the scheme prices without printing an answer."""
    return pt(S(text, end), marks, kind='criterion', note=note, **kw)


def PIECES(line, marks, kind=None, sep=', ', last_note=None):
    """One row per item of a list the scheme prints on one line under one cell
    ("convection, radiation [2 × 3]"), each at its own printed mark."""
    rows = []
    for k, m in enumerate(marks, 1):
        extra = {'note_sel': last_note} if (last_note and k == len(marks)) else {}
        if kind == 'criterion':
            rows.append(pt(S(line, piece=k, psep=sep), m, kind='criterion', note=CRIT, **extra))
        else:
            rows.append(pt(S(line, piece=k, psep=sep), m, **extra))
    return rows


def bundled(parts, keep):
    return f'The old card bundled {parts}, which the scheme prices apart; it keeps its id for {keep}.'


# ------------------------------------------------------------------ stems --
STEM1 = [P(2, 'A student carried out an experiment to show that the acceleration a of an object is',
           'proportional to the force F applied.')]
DATA1 = [P(2, 'The student recorded the following results.'), P(2, 'F (N)', '4.22')]
STEM2 = [P(2, 'A student carried out an experiment to measure the focal length f of a concave mirror.',
           'image distance v to be 61 cm.')]
STEM3 = [P(3, 'A student carried out an experiment to measure the specific latent heat of fusion of ice.',
           'water in a copper calorimeter.')]
RES3 = [P(3, 'The following results were recorded.'), P(3, 'Mass of empty copper calorimeter', '= 16 °C')]
BELOW3 = P(3, 'Below is a diagram of the apparatus used in this experiment.')
SHC3 = P(3, 'specific heat capacity of copper = 390')
STEM4 = [P(4, 'A student carried out an experiment to determine the speed of sound in air.',
           'repeated for different frequencies.')]
STEM5 = [P(4, 'In an experiment to determine the resistivity of a nichrome wire', 'measured the diameter d of the wire.')]
DATA5 = [P(4, 'The student recorded the following results.', nth=2), P(4, 'l (cm)', '2', end_nth=6)]
Q5I = 'Name the apparatus used in this experiment to measure (a) the length of the wire'
Q5I2 = '(b) the resistance of the wire and (c) the diameter of the wire.'
STEM7 = P(6, 'A big drop is an amusement ride where a carriage with', 'comes to rest.')
G7 = P(6, 'acceleration due to gravity')
Q7III = [M('(iii)', 6), P(6, 'The carriage is dropped from a height of 37 m above', 'was dropped.')]
STEM8 = P(7, 'The diagram below shows how a ray of light travels through a rectangular glass block.')
LENS = P(7, 'Refraction also occurs when light travels through a lens.')
STEM9 = P(8, 'Brick is considered one of the best construction materials', 'other building materials.')
BRICK = [P(8, 'Another reason for bricks being such a popular building material', 'the diagram.'),
         P(8, 'The brick has a mass of 2 kg.')]
SUST = P(8, 'Brick is a sustainable material.', 'alternative energy sources instead.')
HEAT9 = P(8, 'Bricks alone are not enough to meet today’s heat retention standards.')
SOUND = P(9, 'The source of every sound is a vibration.', 'one of which is reflection.')
REFR = P(9, 'Sound also undergoes refraction as it moves from one medium to another.')
INTF = P(9, 'When two sound waves meet they can undergo interference.')
DIFF = P(9, 'Sounds waves can undergo diffraction', 'hear around corners.')
POL = P(9, 'Light waves can undergo polarisation but sound waves cannot.')
WAVE = P(9, 'A standing wave is set up on a string as shown', 'speed of 400 m s⁻¹.')
CUR = P(10, 'Electric current is the movement of charged particles through a conductor.')
NOTE11 = P(10, 'Note: You may refer to the electrical circuit symbols on', 'parts (iii) and (iv).')
Q11V = [M('(v)', 10), P(10, 'Two light bulbs connected in parallel have resistances', 'total resistance of the two light bulbs.')]
GRAPH11 = P(10, 'The relationship between current and voltage for a filament bulb is shown in the graph', 'below.')
ELEC = P(11, 'An electron is a negatively charged subatomic particle.')
CRT = P(11, 'The picture on the right is of a cathode ray tube.', 'electrons is produced in a cathode ray tube.')
XT = P(11, 'The picture on the right is of an X-ray tube.', 'electrons is used to produce X-rays in an X-ray tube.')
PASS13 = [P(12, 'It was recently announced that a team of researchers at the', 'energy.'),
          P(12, 'If researchers can harness nuclear fusion', 'able to reach this goal.'),
          P(12, 'To break the energy record', 'involving deuterium only.'),
          P(12, 'In this experiment, 59 MJ of energy was produced during a fusion pulse', 'record for nuclear fusion.'),
          P(12, 'Adapted from: www.nature.com')]
TRAIN = P(13, 'A train has a mass of')
CARR = P(13, 'The train then joins together with a carriage')
ACC14 = P(13, 'The train then accelerates to a speed of 22 m s⁻¹.', '8 minutes.')
FIBRE = P(13, 'Light travels through an optical fibre using', 'total internal reflection.')
FIELD = P(14, 'The diagram shows the electric field around two oppositely', 'charged particles.')
COUL = P(14, 'The force between two electric charges is calculated using Coulomb’s law.', 'inverse square law.')
VDG = P(14, 'Electric charge builds up on the dome of a Van de Graaff generator.')
MAG = P(14, 'A current-carrying conductor has a magnetic', 'field around it.')
FORCE14 = [P(14, 'When a current-carrying conductor is placed in', 'force.'),
           P(14, 'The magnitude of the force F is proportional', 'F = IlB.')]

PAE2 = S('[accept partial answers for 2 in each case]')

TASKS = [
    # ============================================================ Section A ==
    # ---------------------------------------------------------------- Q1 --
    T('1i', 'Q1(i)', 'A', P(2, 'Draw a labelled diagram of the apparatus used in this experiment.'),
      [C('runway', 3), C('trolley', 3), C('means of applying/measuring force', 3),
       C('means of measuring distance/velocity/time', 3, note_sel=NOLABEL)], 'phys-u2', 'force-acceleration-apparatus',
      SQ(6, 'Draw a labelled diagram of the apparatus used in this experiment.'), 12, stem=STEM1, id='phys-2023-ol-q1-i'),
    T('1ii', 'Q1(ii)', 'A', P(2, 'What measurements did the student take to calculate acceleration?'),
      [anyn(S('first distance/velocity, second distance/velocity, time (any two)'), 2, 3, sep=',')], 'phys-u2',
      'measurements-for-acceleration', SQ(6, 'What measurements did the student take to calculate acceleration?'), 6,
      stem=STEM1, id='phys-2023-ol-q1-ii', decision='"(any two) [2 × 3]": a menu of three, any two at 3 each.'),
    T('1iii', 'Q1(iii)', 'A', P(2, 'State one precaution the student took to ensure an accurate result.'),
      [anyn(None, 1, 4, open_list=True, note_sel=PA(2),
            options=[S('e.g. avoid error of parallax, smooth runway', piece=[1, 2], psep=[',', 'e.g. ']),
                     S('e.g. avoid error of parallax, smooth runway', piece=2, psep=',')])], 'phys-u2',
      'precaution-for-accuracy', SQ(6, 'State one precaution the student took to ensure an accurate result.'), 4,
      stem=STEM1, id='phys-2023-ol-q1-iii',
      decision='The scheme prints two examples ("e.g.") for one precaution at [4]: a menu of one.'),
    T('1iv', 'Q1(iv)', 'A', P(2, 'Use the data in the table to draw a graph on graph paper of F against a.'),
      [C('labelled axis', 3), C('points plotted', 6, units=[1] * 6), C('line of best fit', 3)], 'phys-u2',
      'force-acceleration-graph', SQ(6, 'Use the data in the table to draw a graph on graph paper of F against a.'),
      12, stem=STEM1 + DATA1, fig='q1iv-scheme-graph', id='phys-2023-ol-q1-iv',
      decision='"points plotted [6 × 1]": one row of six 1-mark units. The scheme draws the graph (the solution '
               'figure); the data table is lifted into the stem.'),
    T('1v', 'Q1(v)', 'A', P(2, 'Explain how your graph shows that acceleration is proportional to force.'),
      [R('straight line (through the origin)', 6, note_sel=PA(3))], 'phys-1-2', 'graph-shows-proportionality',
      SQ(6, 'Explain how your graph shows that acceleration is proportional to force.'), 6, stem=STEM1,
      id='phys-2023-ol-q1-v'),
    # ---------------------------------------------------------------- Q2 --
    T('2i', 'Q2(i)', 'A', P(2, 'Draw a labelled diagram of the apparatus used in this experiment.', nth=2),
      [anyn(S('object, mirror, screen'), 3, 6, steps=[6, 3, 3], sep=',', note_sel=NOLABEL,
            note=ORDERED.format(cell='[6 + 3 + 3]'))], 'phys-u2', 'concave-mirror-apparatus',
      SQ(7, 'Draw a labelled diagram of the apparatus used in this experiment.'), 12, stem=STEM2,
      id='phys-2023-ol-q2-i', source_pages=[2], decision=LINKED.format(w='"the image distance"')),
    T('2ii', 'Q2(ii)', 'A', P(2, 'On your diagram, indicate the object distance u and the image distance v.'),
      [C('u shown', 3), C('v shown', 3, note_sel=PA(3))], 'phys-u2', 'showing-u-and-v',
      SQ(7, 'On your diagram, indicate the object distance u and the image distance v.'), 6, stem=STEM2,
      id='phys-2023-ol-q2-ii', source_pages=[2], decision=LINKED.format(w='"the image distance"')),
    T('2iii', 'Q2(iii)', 'A', P(2, 'Describe how the student found the position of the image.'),
      [R('move screen/mirror/object / sharpest image is formed', 6, note_sel=PA(3))], 'phys-u2',
      'finding-the-image', SQ(7, 'Describe how the student found the position of the image.'), 6, stem=STEM2,
      id='phys-2023-ol-q2-iii', source_pages=[2], decision=LINKED.format(w='"the image distance"')),
    T('2iv', 'Q2(iv)', 'A', P(2, 'State the formula used to calculate the focal length f.'),
      [R('1/u + 1/v = 1/f', 6, note_sel=PA(3))], 'phys-2-3', 'mirror-formula',
      SQ(7, 'State the formula used to calculate the focal length f.'), 6, stem=STEM2, id='phys-2023-ol-q2-iv',
      source_pages=[2], decision=LINKED.format(w='"the image distance"')),
    T('2v', 'Q2(v)', 'A', P(2, 'Calculate f.'),
      [R('f = 15.1 cm', 6, note_sel=PA(3))], 'phys-2-3', 'focal-length', SQ(7, 'Calculate f.'), 6, stem=STEM2,
      id='phys-2023-ol-q2-v', source_pages=[2], decision=LINKED.format(w='"the image distance"')),
    T('2vi', 'Q2(vi)', 'A', P(2, 'Describe how the student could have improved the experiment.'),
      [R('e.g. repeat and average', 4, note_sel=PA(2))], 'phys-u2', 'improving-the-experiment',
      SQ(7, 'Describe how the student could have improved the experiment.'), 4, stem=STEM2, id='phys-2023-ol-q2-vi',
      source_pages=[2], decision=LINKED.format(w='"the image distance"')),
    # ---------------------------------------------------------------- Q3 --
    T('3i', 'Q3(i)', 'A', P(3, 'Name the piece of equipment labelled A.'),
      [R('thermometer', 3)], 'phys-u2', 'equipment-a', SQ(8, 'Name the piece of equipment labelled A.'), 3,
      stem=STEM3 + [BELOW3], fig='q3-diagram', labels=[L('A', S('thermometer', page=8), True)]),
    T('3ii', 'Q3(ii)', 'A', P(3, 'Name the piece of equipment labelled B.'),
      [R('lagging/insulation', 3)], 'phys-u2', 'equipment-b', SQ(8, 'Name the piece of equipment labelled B.'), 3,
      stem=STEM3 + [BELOW3], fig='q3-diagram', labels=[L('B', S('lagging/insulation', page=8), True)]),
    T('3iii', 'Q3(iii)', 'A', P(3, 'Why did the student crush the ice before adding it to the calorimeter?'),
      [R('melts faster / increase surface area / all at the same temperature/0 °C', 4, note_sel=PA(2))], 'phys-u2',
      'why-crush-the-ice', SQ(8, 'Why did the student crush the ice before adding it to the calorimeter?'), 4,
      stem=STEM3, id='phys-2023-ol-q3-iii'),
    T('3iv', 'Q3(iv)', 'A', P(3, 'What was the cloth used for in this experiment?'),
      [R('to dry the ice', 4, note_sel=PA(2))], 'phys-u2', 'use-of-the-cloth',
      SQ(8, 'What was the cloth used for in this experiment?'), 4, stem=STEM3 + [BELOW3], fig='q3-diagram',
      id='phys-2023-ol-q3-iv'),
    T('3v', 'Q3(v)', 'A', P(3, 'Calculate the fall in temperature of the calorimeter and water.'),
      [R('23 – 16 = 7 °C', 4, note_sel=PA(2))], 'phys-2-1', 'fall-in-temperature',
      SQ(8, 'Calculate the fall in temperature of the calorimeter and water.'), 4, stem=STEM3 + RES3,
      id='phys-2023-ol-q3-v'),
    T('3vi', 'Q3(vi)', 'A', P(3, 'Calculate the mass of the water.'),
      [R('0.181 – 0.083 = 0.098 kg', 4, note_sel=PA(2))], 'phys-2-1', 'mass-of-water',
      SQ(8, 'Calculate the mass of the water.'), 4, stem=STEM3 + RES3, id='phys-2023-ol-q3-vi'),
    T('3vii', 'Q3(vii)', 'A', P(3, 'Using the formula mcΔθ and your answers to (v) and (vi), calculate E, the heat lost by',
                               'the water and the calorimeter.'),
      [R('(0.098 × 4180 × 7)', 3), R('(0.083 × 390 × 7)', 3), R('= 3094.07 J', 3, note_sel=PA(3))], 'phys-2-1',
      'heat-lost-by-water-and-calorimeter',
      SQ(8, 'Using the formula mcΔθ and your answers to (v) and (vi), calculate E, the heat lost by'), 9,
      stem=STEM3 + RES3 + [SHC3], id='phys-2023-ol-q3-vii'),
    T('3viii', 'Q3(viii)', 'A', P(3, 'Calculate the rise in temperature of the ice.'),
      [R('16 °C', 3)], 'phys-2-1', 'rise-in-temperature-of-ice', SQ(8, 'Calculate the rise in temperature of the ice.'),
      3, stem=STEM3 + RES3, id='phys-2023-ol-q3-viii'),
    T('3ix', 'Q3(ix)', 'A', P(3, 'Calculate the value for l, the specific latent heat of fusion of ice.'),
      [R('0.008l + (0.008 × 4180 ×16) = 3094.07 so l = 319880 J kg⁻¹', 6, note_sel=PA(3))], 'phys-2-1',
      'latent-heat-of-fusion', SQ(8, 'Calculate the value for l, the specific latent heat of fusion of ice.'), 6,
      qfig='q3ix-question', id='phys-2023-ol-q3-ix',
      decision='The ask\'s note "E = m_ice l + m_ice c_water Δθ_ice" sets its subscripts as lowered words the text '
               'layer cannot lower ("micel"): the question is shown as printed, the whole of Q3 with its data.'),
    # ---------------------------------------------------------------- Q4 --
    T('4i', 'Q4(i)', 'A', P(4, 'Draw a labelled diagram of the apparatus used in this experiment.'),
      [anyn(S('tube, tuning fork, means of changing length, metre stick (any three)'), 3, 6, steps=[6, 3, 3],
            sep=',', note_sel=NOLABEL, note=ORDERED.format(cell='[6 + 3 + 3]'))], 'phys-u2',
      'resonance-tube-apparatus', SQ(9, 'Draw a labelled diagram of the apparatus used in this experiment.'), 12,
      stem=STEM4, id='phys-2023-ol-q4-i'),
    T('4ii', 'Q4(ii)', 'A', P(4, 'Indicate on your diagram the length that the student measured.'),
      [C('valid length shown', 3)], 'phys-u2', 'length-measured',
      SQ(9, 'Indicate on your diagram the length that the student measured.'), 3, stem=STEM4, id='phys-2023-ol-q4-ii'),
    T('4iii', 'Q4(iii)', 'A', P(4, 'How did the student find the frequency values?'),
      [R('from tuning fork', 6, note_sel=PA(3))], 'phys-u2', 'frequency-values',
      SQ(9, 'How did the student find the frequency values?'), 6, stem=STEM4, id='phys-2023-ol-q4-iii'),
    T('4iv', 'Q4(iv)', 'A', P(4, 'The student knew that the column of air was vibrating at its fundamental frequency',
                             'How did the student know that resonance had occurred?'),
      [R('loud sound', 6, note_sel=PA(3))], 'phys-2-5', 'recognising-resonance',
      SQ(9, 'The student knew that the column of air was vibrating at its fundamental frequency'), 6, stem=STEM4,
      id='phys-2023-ol-q4-iv'),
    T('4v', 'Q4(v)', 'A', P(4, 'For each value of l in the table above, calculate the value of'),
      [pt(S(v), 1, label=S(l, after='ₗ to 2 decimal places.'),
          **({'note': 'The scheme prints the six values [6 × 1]: 1 mark each.'} if k == 0 else {}))
       for k, (l, v) in enumerate((('0.33', '3.03'), ('0.29', '3.45'), ('0.27', '3.70'), ('0.25', '4.00'),
                                   ('0.22', '4.55'), ('0.18', '5.56')))],
      'phys-u2', 'values-of-1-over-l', SQ(9, 'For each value of l in the table above, calculate the value of'), 6,
      qfig='q4v-question',
      decision='The paper sets "1/l" as a stacked fraction the text layer breaks: the question is shown as printed, '
               'Q4 with its table. The scheme prints the values as a table: one row per value, labelled with its '
               'length.'),
    T('4vi', 'Q4(vi)', 'A', P(4, 'Draw a graph on graph paper of f against'),
      [C('labelled axis', 2), C('points plotted', 3), C('line of best fit', 2)], 'phys-u2', 'graph-f-against-1-over-l',
      SQ(9, 'Draw a graph on graph paper of f against'), 7, qfig='q4vi-question', fig='q4vi-scheme-graph',
      decision='The ask ends in the stacked fraction "1/l": the question is shown as printed, Q4 with its table; the '
               'scheme draws the graph (the solution figure).'),
    # ---------------------------------------------------------------- Q5 --
    T('5ia', 'Q5(i)(a)', 'A', P(4, Q5I),
      [R('metre stick', 3)], 'phys-u2', 'measuring-length-of-wire', SQ(10, Q5I), 3, stem=STEM5, id='phys-2023-ol-q5-i',
      decision='The paper prints (a), (b) and (c) inside one sentence, priced [3] each: the question is that sentence '
               'cut at its own markers. ' + bundled('(a), (b) and (c)', '(a)')),
    T('5ib', 'Q5(i)(b)', 'A', [P(4, Q5I, piece=1, psep=' (a) the length of the wire'), P(4, Q5I2, piece=1, psep=' and (c)')],
      [R('ohmmeter', 3)], 'phys-u2', 'measuring-resistance-of-wire', SQ(10, Q5I), 3, stem=STEM5,
      decision='The paper prints (a), (b) and (c) inside one sentence: the question is that sentence without the '
               'other markers\' words.'),
    T('5ic', 'Q5(i)(c)', 'A', [P(4, Q5I, piece=1, psep=' (a) the length of the wire'), P(4, Q5I2, piece=2, psep=' and ')],
      [R('micrometer', 3)], 'phys-u2', 'measuring-diameter-of-wire', SQ(10, Q5I), 3, stem=STEM5,
      decision='The paper prints (a), (b) and (c) inside one sentence: the question is that sentence without the '
               'other markers\' words.'),
    T('5ii', 'Q5(ii)', 'A', P(4, 'How did the student check that the wire had the same diameter throughout its length?'),
      [R('checked the diameter at various points', 6, note_sel=PA(3))], 'phys-u2', 'checking-uniform-diameter',
      SQ(10, 'How did the student check that the wire had the same diameter throughout its length?'), 6, stem=STEM5,
      id='phys-2023-ol-q5-ii'),
    T('5iii', 'Q5(iii)', 'A', P(4, 'Use the data in the table to draw a graph on graph paper of length l against',
                               'resistance R.'),
      [C('labelled axis', 4), C('points plotted', 6, units=[1] * 6), C('line of best fit', 3)], 'phys-u2',
      'length-resistance-graph', SQ(10, 'Use the data in the table to draw a graph on graph paper of length l against'),
      13, stem=STEM5 + DATA5, fig='q5iii-scheme-graph', id='phys-2023-ol-q5-iii',
      decision='"points plotted [6 × 1]": one row of six 1-mark units. The scheme draws the graph (the solution '
               'figure); the data table is lifted into the stem.'),
    T('5iv', 'Q5(iv)', 'A', P(4, 'State the relationship between l and R.'),
      [R('proportional', 6, note_sel=PA(3))], 'phys-3-3', 'length-resistance-relationship',
      SQ(10, 'State the relationship between l and R.'), 6, stem=STEM5 + DATA5, id='phys-2023-ol-q5-iv'),
    T('5v', 'Q5(v)', 'A', P(4, 'State the formula used to calculate ρ, the resistivity of the wire.'),
      [R('ρ = RA/l', 6, note_sel=PA(3))], 'phys-3-3', 'resistivity-formula',
      SQ(10, 'State the formula used to calculate ρ, the resistivity of the wire.'), 6, stem=STEM5,
      id='phys-2023-ol-q5-v'),
    # ============================================================ Section B ==
    # ---------------------------------------------------------------- Q6 --
    T('6a', 'Q6(a)', 'B', P(5, 'What is meant by the moment of a force?'),
      [R('force × distance (to fulcrum) / the turning effect of the force', 7, note_sel=PA(4))], 'phys-1-2',
      'moment-of-a-force', SQ(11, 'What is meant by the moment of a force?'), 7, id='phys-2023-ol-q6-a'),
    T('6b', 'Q6(b)', 'B', P(5, 'A car accelerates from a speed of 17 m s⁻¹', 'Calculate the acceleration of the car.'),
      [R('(28 – 17)/8 = 1.375 m s⁻²', 7, note_sel=PA(4))], 'phys-1-1', 'acceleration-of-car',
      SQ(11, 'A car accelerates from a speed of 17 m s⁻¹ to a speed of 28 m s⁻¹ in a time of 8 s.'), 7,
      id='phys-2023-ol-q6-b'),
    T('6c', 'Q6(c)', 'B', P(5, 'Convert 30 °C into kelvin (K).'),
      [R('30 + 273 = 303 K', 7, note_sel=PA(4))], 'phys-2-1', 'celsius-to-kelvin',
      SQ(11, 'Convert 30 °C into kelvin (K).'), 7, id='phys-2023-ol-q6-c'),
    T('6d', 'Q6(d)', 'B', [P(5, 'Which of the following is the unit of work?'), P(5, 'joule', br=True),
                           P(5, 'watt', br=True), P(5, 'farad', br=True), P(5, 'metre', br=True)],
      [R('joule', 7)], 'phys-1-4', 'unit-of-work', SQ(11, 'Which of the following is the unit of work?'), 7,
      id='phys-2023-ol-q6-d',
      decision='The scheme reprints the four options and strikes through watt, farad and metre (drawn lines, '
               'rendered and looked at), leaving joule: the row is the option it leaves, at the [7] printed under it.'),
    T('6e', 'Q6(e)', 'B', P(5, 'Name an instrument used to measure voltage.'),
      [R('voltmeter', 7, note_sel=PA(4))], 'phys-3-3', 'measuring-voltage',
      SQ(11, 'Name an instrument used to measure voltage.'), 7, id='phys-2023-ol-q6-e'),
    T('6f', 'Q6(f)', 'B', P(5, 'An object has a height of 2 cm.', 'Calculate the object’s magnification.'),
      [R('5 ÷ 2 = 2.5', 7, note_sel=PA(4))], 'phys-2-3', 'magnification',
      SQ(11, 'An object has a height of 2 cm. Its image in a mirror has a height of 5 cm.'), 7, id='phys-2023-ol-q6-f'),
    T('6g', 'Q6(g)', 'B', P(5, 'Explain the difference between heat and temperature.'),
      [R('heat is a form of energy / temperature is a measure of hotness', 7, note_sel=PA(4))], 'phys-2-1',
      'heat-and-temperature', SQ(11, 'Explain the difference between heat and temperature.'), 7,
      id='phys-2023-ol-q6-g'),
    T('6h', 'Q6(h)', 'B', P(5, 'What are complementary colours of light?'),
      [R('a primary and a secondary colour / colours that combine to give white light', 7, note_sel=PA(4))],
      'phys-2-4', 'complementary-colours', SQ(11, 'What are complementary colours of light?'), 7,
      id='phys-2023-ol-q6-h'),
    T('6i', 'Q6(i)', 'B', P(5, 'Describe how infrared radiation can be detected.'),
      [R('heating effect, etc.', 7, note_sel=PA(4))], 'phys-2-4', 'detecting-infrared',
      SQ(11, 'Describe how infrared radiation can be detected.'), 7, id='phys-2023-ol-q6-i'),
    T('6j', 'Q6(j)', 'B', P(5, 'What is meant by capacitance?'),
      [R('ratio of charge to voltage', 7, note_sel=PA(4))], 'phys-3-2', 'capacitance',
      SQ(11, 'What is meant by capacitance?'), 7, id='phys-2023-ol-q6-j'),
    T('6k', 'Q6(k)', 'B', P(5, 'Describe how white light can be separated into its constituent colours.'),
      [R('prism / diffraction grating / etc.', 7, note_sel=PA(4))], 'phys-2-3', 'separating-white-light',
      SQ(11, 'Describe how white light can be separated into its constituent colours.'), 7, id='phys-2023-ol-q6-k'),
    T('6l', 'Q6(l)', 'B', P(5, 'State what each letter in Einstein’s famous equation E = mc² stands for.'),
      PIECES('E = energy, m = mass, c = speed of light', [3, 2, 2]), 'phys-4-5', 'e-equals-mc-squared',
      SQ(11, 'State what each letter in Einstein’s famous equation E = mc² stands for.'), 7, id='phys-2023-ol-q6-l',
      decision='"[3 + 2 + 2]" against the three meanings printed on one line: in the order printed.'),
    # ---------------------------------------------------------------- Q7 --
    T('7i', 'Q7(i)', 'B', P(6, 'As the carriage travels to the top, the carriage is gaining',
                           'What is meant by potential energy?'),
      [R('energy due to position in a force field', 6, note_sel=PA(3))], 'phys-1-4', 'potential-energy',
      SQ(12, 'As the carriage travels to the top, the carriage is gaining potential energy.'), 6, stem=[STEM7],
      id='phys-2023-ol-q7-i'),
    T('7ii', 'Q7(ii)', 'B', P(6, 'Draw a diagram of the forces acting on the carriage as it',
                             'travels up the tower at a constant velocity.'),
      [C('arrow down', 3), C('equal arrow up', 3, note_sel=S('[–1 if arrows are clearly not equal]'))], 'phys-1-2',
      'forces-at-constant-velocity',
      SQ(12, 'Draw a diagram of the forces acting on the carriage as it travels up the tower at a'), 6, stem=[STEM7],
      id='phys-2023-ol-q7-ii'),
    T('7iii', 'Q7(iii)', 'B', P(6, 'The carriage is dropped from a height of 37 m above', 'was dropped.'),
      [R('mgh', 3), R('6200 × 9.8 × 37', 3), R('= 2248120 J', 3, note_sel=PA(3))], 'phys-1-4',
      'potential-energy-before-drop', SQ(12, 'The carriage is dropped from a height of 37 m above the braking zone.'),
      9, stem=[STEM7, G7], id='phys-2023-ol-q7-iii'),
    T('7iv', 'Q7(iv)', 'B', P(6, 'What is the main energy conversion that takes place as the carriage falls?'),
      [R('potential energy to kinetic energy', 6, note_sel=PA(3))], 'phys-1-4', 'energy-conversion-in-fall',
      SQ(12, 'What is the main energy conversion that takes place as the carriage falls?'), 6, stem=[STEM7],
      id='phys-2023-ol-q7-iv'),
    T('7v', 'Q7(v)', 'B', P(6, 'Calculate the velocity of the carriage when it has fallen 37 m.'),
      [R('Eₖ = ½mv²', 3, end='// v² = u² + 2as', note_sel=LEGEND), C('substitution', 3),
       R('v = 26.9 m s⁻¹', 3, note_sel=PA(3))], 'phys-1-4', 'velocity-after-fall',
      SQ(12, 'Calculate the velocity of the carriage when it has fallen 37 m.'), 9, stem=[STEM7] + Q7III + [G7],
      id='phys-2023-ol-q7-v',
      decision='The first line is printed with its // side (an energy route or an equation of motion): one row, as '
               'printed.'),
    T('7vi', 'Q7(vi)', 'B', P(6, 'Calculate the time it takes the carriage to fall 37 m.'),
      [R('26.9 ÷ 9.8 = 2.75 s', 6, note_sel=PA(3))], 'phys-1-1', 'time-to-fall',
      SQ(12, 'Calculate the time it takes the carriage to fall 37 m.'), 6,
      stem=[STEM7, M('(v)', 6), P(6, 'Calculate the velocity of the carriage when it has fallen 37 m.'), G7],
      id='phys-2023-ol-q7-vi'),
    T('7vii', 'Q7(vii)', 'B', P(6, 'Draw a diagram of the forces acting on the carriage as it falls.'),
      [C('arrow down', 6, note_sel=PA(3))], 'phys-1-2', 'forces-while-falling',
      SQ(12, 'Draw a diagram of the forces acting on the carriage as it falls.'), 6, stem=[STEM7],
      id='phys-2023-ol-q7-vii'),
    T('7viii', 'Q7(viii)', 'B', P(6, 'Draw a velocity-time graph for the motion of the carriage from when it was dropped to',
                                 'when it comes to rest.'),
      [C('axis labelled', 2), C('acceleration shown', 3),
       C('deceleration shown', 3, note_sel=S('[–1 if incorrect acceleration shown]'))], 'phys-1-1',
      'velocity-time-graph', SQ(12, 'Draw a velocity-time graph for the motion of the carriage'), 8, stem=[STEM7],
      id='phys-2023-ol-q7-viii'),
    # ---------------------------------------------------------------- Q8 --
    T('8i', 'Q8(i)', 'B', P(7, 'What is meant by refraction of light?'),
      [R('the bending of light (as it travels from one medium to another)', 6, note_sel=PA(3))], 'phys-2-3',
      'refraction', SQ(13, 'What is meant by refraction of light?'), 6, id='phys-2023-ol-q8-i'),
    T('8ii', 'Q8(ii)', 'B', P(7, 'Name A, B and C.'),
      [R('incident ray', 3, label=S('A')), R('refracted ray', 3, label=S('B')), R('normal', 3, label=S('C'))],
      'phys-2-3', 'naming-a-b-c', SQ(13, 'Name A, B and C.'), 9, stem=[STEM8], fig='q8-diagram'),
    T('8iii', 'Q8(iii)', 'B', P(7, 'Copy the diagram into your answerbook and label the angle of incidence i and the',
                               'angle of refraction r.'),
      [C('angles labelled', 6, units=[3, 3], note_sel=PA(3))], 'phys-2-3', 'labelling-angles',
      SQ(13, 'Copy the diagram into your answerbook and label the angle of incidence i and the'), 6, stem=[STEM8],
      fig='q8-diagram', decision='"angles labelled [2 × 3]": one row of two 3-mark units.'),
    T('8iv', 'Q8(iv)', 'B', P(7, 'The refractive index of the glass block is 1.5.', 'the angle of incidence is 35°.'),
      [R('n = sin i/sin r', 3), C('substitution', 3), R('r = 22.5°', 3, note_sel=PA(3))], 'phys-2-3',
      'angle-of-refraction', SQ(13, 'The refractive index of the glass block is 1.5.'), 9, stem=[STEM8],
      fig='q8-diagram', id='phys-2023-ol-q8-iv'),
    T('8v', 'Q8(v)', 'B', P(7, 'Draw a converging lens and draw a ray diagram to show how the lens forms a real', 'image.'),
      [C('converging lens', 3)] + PIECES('object, incident ray(s), image formed', [3, 3, 3], kind='criterion'),
      'phys-2-3', 'real-image-ray-diagram',
      SQ(13, 'Draw a converging lens and draw a ray diagram to show how the lens forms a real'), 12, stem=[LENS],
      id='phys-2023-ol-q8-v', decision='"[3 × 3]" against the three items printed on one line: 3 each.'),
    T('8vi', 'Q8(vi)', 'B', P(7, 'An object is placed 25 cm in front of a converging lens of focal length 15 cm.',
                             'Calculate the position of the image formed.'),
      [R('1/u + 1/v = 1/f', 3), C('substitution', 3), R('v = 37.5 cm', 3, note_sel=PA(3))], 'phys-2-3',
      'image-position', SQ(13, 'An object is placed 25 cm in front of a converging lens of focal length 15 cm.'), 9,
      stem=[LENS], id='phys-2023-ol-q8-vi', source_pages=[7], decision=LINKED.format(w='"the image formed"')),
    T('8vii', 'Q8(vii)', 'B', P(7, 'Converging lenses can be used in glasses to correct a sight', 'lens?'),
      [R('long-sightedness / hypermetropia / hyperopia', 5, note_sel=PA(3))], 'phys-2-3', 'sight-defect',
      SQ(13, 'Converging lenses can be used in glasses to correct a sight defect.'), 5, stem=[LENS],
      id='phys-2023-ol-q8-vii'),
    # ---------------------------------------------------------------- Q9 --
    T('9i', 'Q9(i)', 'B', P(8, 'Heat is transferred through a wall by conduction.', 'can be transferred.'),
      PIECES('convection, radiation', [3, 3]), 'phys-2-1', 'heat-transfer',
      SQ(14, 'Heat is transferred through a wall by conduction.'), 6, stem=[STEM9], id='phys-2023-ol-q9-i',
      decision='"[2 × 3]" against the two ways printed on one line: 3 each.'),
    T('9ii', 'Q9(ii)', 'B', P(8, 'What is meant by the U-value of a material?'),
      [R('measure of the conducting/insulating property /', 6,
         end='temperature difference of 1 K between the two sides)', note_sel=PA(3))], 'phys-2-1', 'u-value',
      SQ(14, 'What is meant by the U-value of a material?'), 6, stem=[STEM9], id='phys-2023-ol-q9-ii'),
    T('9iii', 'Q9(iii)', 'B', P(8, 'A wall has an area of 66 m² and a U-value of 0.31 W m⁻² K⁻¹.',
                               'transmitted through the wall every second.'),
      [R('66 × 0.31 × 15', 6), R('306.9 J', 3, note_sel=PA(3))], 'phys-2-1', 'heat-through-wall',
      SQ(14, 'A wall has an area of 66 m² and a U-value of 0.31 W m⁻² K⁻¹.'), 9, stem=[STEM9],
      id='phys-2023-ol-q9-iii'),
    T('9iv', 'Q9(iv)', 'B', P(8, 'Calculate the volume of the brick in cm³.'),
      [R('20 × 9 × 6 = 1080 cm³', 6, note_sel=PA(3))], 'phys-1-2', 'volume-of-brick',
      SQ(14, 'Calculate the volume of the brick in cm³.'), 6, stem=BRICK, fig='q9-brick', id='phys-2023-ol-q9-iv'),
    T('9v', 'Q9(v)', 'B', P(8, 'Calculate the density of the brick in g cm⁻³.'),
      [pt(S('conversion to grams; 2000 ÷ 1080 = 1.85 g cm⁻³', piece=1, psep=';'), 4, kind='criterion', note=CRIT),
       pt(S('conversion to grams; 2000 ÷ 1080 = 1.85 g cm⁻³', piece=2, psep=';'), 2, note_sel=PA(3))],
      'phys-1-2', 'density-of-brick', SQ(14, 'Calculate the density of the brick in g cm⁻³.'), 6,
      stem=BRICK + [M('(iv)', 8), P(8, 'Calculate the volume of the brick in cm³.')], fig='q9-brick',
      id='phys-2023-ol-q9-v', decision='"[4 + 2]" against the two steps printed on one line: 4 then 2.'),
    T('9vi', 'Q9(vi)', 'B', P(8, 'The bricks are stacked to build a wall.', 'Explain your answer.'),
      [R('B', 4), R('greatest area', 4)], 'phys-1-2', 'least-pressure-side',
      SQ(14, 'The bricks are stacked to build a wall.'), 8, stem=BRICK, fig='q9-brick', id='phys-2023-ol-q9vi-fig'),
    T('9vii', 'Q9(vii)', 'B', P(8, 'What is meant by non-renewable energy?'),
      [R('energy that is not replaced as it is used', 6, note_sel=PA(3))], 'phys-1-4', 'non-renewable-energy',
      SQ(14, 'What is meant by non-renewable energy?'), 6, stem=[SUST], id='phys-2023-ol-q9-vii'),
    T('9viii', 'Q9(viii)', 'B', P(8, 'State an example of a renewable energy source.'),
      [R('e.g. solar', 3)], 'phys-1-4', 'renewable-energy-source',
      SQ(14, 'State an example of a renewable energy source.'), 3, stem=[SUST], id='phys-2023-ol-q9-viii'),
    T('9ix', 'Q9(ix)', 'B', P(8, 'State two ways in which you can reduce heat loss from your home.'),
      [anyn(None, 2, 3, open_list=True,
            note='The scheme prints two examples ("e.g.") at "[2 × 3]": 3 each.',
            options=[S('e.g. double-glazed windows, insulated attic', piece=[1, 2], psep=[',', 'e.g. ']),
                     S('e.g. double-glazed windows, insulated attic', piece=2, psep=',')])], 'phys-2-1',
      'reducing-heat-loss', SQ(14, 'State two ways in which you can reduce heat loss from your home.'), 6,
      stem=[HEAT9], id='phys-2023-ol-q9-ix'),
    # --------------------------------------------------------------- Q10 --
    T('10i', 'Q10(i)', 'B', P(9, 'What is meant by reflection?'),
      [R('bouncing of a wave off a surface', 6, note_sel=PA(3))], 'phys-2-3', 'reflection',
      SQ(15, 'What is meant by reflection?'), 6, stem=[SOUND], id='phys-2023-ol-q10-i'),
    T('10ii', 'Q10(ii)', 'B', P(9, 'What causes sound to refract as it moves from one medium to another?'),
      [R('change in speed / change in (optical) density', 6, note_sel=PA(3))], 'phys-2-3', 'cause-of-refraction',
      SQ(15, 'What causes sound to refract as it moves from one medium to another?'), 6, stem=[REFR],
      id='phys-2023-ol-q10-ii'),
    T('10iii', 'Q10(iii)', 'B', P(9, 'Describe a laboratory experiment to show that sound waves undergo interference.'),
      [C('apparatus', 4), C('method', 4), C('observation', 4, note_sel=PAE2)], 'phys-2-6',
      'demonstrating-sound-interference',
      SQ(15, 'Describe a laboratory experiment to show that sound waves undergo interference.'), 12, stem=[INTF],
      decision=EXPT),
    T('10iv', 'Q10(iv)', 'B', P(9, 'What is meant by diffraction?'),
      [R('spreading of a wave as it passes through a gap/around an object', 6, note_sel=PA(3))], 'phys-2-3',
      'diffraction', SQ(15, 'What is meant by diffraction?'), 6, stem=[DIFF], id='phys-2023-ol-q10-iv'),
    T('10v', 'Q10(v)', 'B', P(9, 'Why do sound waves not undergo polarisation?'),
      [R('sound waves are longitudinal', 6, note_sel=PA(3))], 'phys-2-2', 'sound-not-polarised',
      SQ(15, 'Why do sound waves not undergo polarisation?'), 6, stem=[POL], id='phys-2023-ol-q10-v'),
    T('10vi', 'Q10(vi)', 'B', P(9, 'What name is given to points A and B?'),
      [R('nodes', 4, note_sel=PA(2))], 'phys-2-6', 'nodes', SQ(15, 'What name is given to points A and B?'), 4,
      stem=[WAVE], fig='q10-wave', id='phys-2023-ol-q10-vi'),
    T('10vii', 'Q10(vii)', 'B', P(9, 'What name is given to height h?'),
      [R('amplitude', 4, note_sel=PA(2))], 'phys-2-6', 'amplitude', SQ(15, 'What name is given to height h?'), 4,
      stem=[WAVE], fig='q10-wave', id='phys-2023-ol-q10-vii'),
    T('10viii', 'Q10(viii)', 'B', P(9, 'Calculate the wavelength of the wave.'),
      [R('2 × 45 = 90 cm', 6, note_sel=PA(3))], 'phys-2-6', 'wavelength-of-standing-wave',
      SQ(15, 'Calculate the wavelength of the wave.'), 6, stem=[WAVE], fig='q10-wave', id='phys-2023-ol-q10-viii'),
    T('10ix', 'Q10(ix)', 'B', P(9, 'Calculate the frequency of the wave.'),
      [R('400 ÷ 0.9 = 444.4 Hz', 6, note_sel=PA(3))], 'phys-2-6', 'frequency-of-wave',
      SQ(15, 'Calculate the frequency of the wave.'), 6,
      stem=[WAVE, M('(viii)', 9), P(9, 'Calculate the wavelength of the wave.')], fig='q10-wave',
      id='phys-2023-ol-q10-ix'),
    # --------------------------------------------------------------- Q11 --
    T('11i', 'Q11(i)', 'B', P(10, 'What is an electrical conductor?'),
      [R('a material that allows current to flow', 3)], 'phys-3-3', 'electrical-conductor',
      SQ(16, 'What is an electrical conductor?'), 3, stem=[CUR], id='phys-2023-ol-q11-i'),
    T('11ii', 'Q11(ii)', 'B', P(10, 'Name an instrument used to measure electric current.'),
      [R('ammeter', 6, note_sel=PA(3))], 'phys-3-3', 'measuring-current',
      SQ(16, 'Name an instrument used to measure electric current.'), 6, stem=[CUR], id='phys-2023-ol-q11-ii'),
    T('11iii', 'Q11(iii)', 'B', P(10, 'Draw a circuit diagram for the arrangement of',
                                 'apparatus shown in the diagram on the right.'),
      PIECES('symbol for battery/cell, symbol for bulb, connected in series', [3, 3, 3], kind='criterion'),
      'phys-3-3', 'bulb-and-battery-circuit',
      SQ(16, 'Draw a circuit diagram for the arrangement of apparatus shown in the diagram on the'), 9,
      stem=[NOTE11], fig='q11-bulb', id='phys-2023-ol-q11iii-fig',
      decision='"[3 × 3]" against the three items printed on one line: 3 each.'),
    T('11iv', 'Q11(iv)', 'B', P(10, 'Draw a circuit diagram to show two light bulbs', 'connected in parallel across a battery.'),
      [C('second bulb', 3), C('in parallel', 3)], 'phys-3-3', 'bulbs-in-parallel',
      SQ(16, 'Draw a circuit diagram to show two light bulbs connected in parallel across a battery.'), 6,
      stem=[NOTE11], id='phys-2023-ol-q11-iv', source_pages=[10], decision=LINKED.format(w='"a circuit diagram"')),
    T('11v', 'Q11(v)', 'B', P(10, 'Two light bulbs connected in parallel have resistances', 'total resistance of the two light bulbs.'),
      [R('1/RT = 1/R₁ + 1/R₂', 3), C('substitution', 3), R('RT = 2.22 Ω', 3, note_sel=PA(3))], 'phys-3-3',
      'parallel-resistance', SQ(16, 'Two light bulbs connected in parallel have resistances of 5 Ω and 4 Ω.'), 9,
      id='phys-2023-ol-q11-v'),
    T('11vi', 'Q11(vi)', 'B', P(10, 'Calculate the total current flowing in this circuit if the battery had a voltage of 12 V.'),
      [R('12 ÷ 2.22 = 5.4 A', 6, note_sel=PA(3))], 'phys-3-3', 'total-current',
      SQ(16, 'Calculate the total current flowing in this circuit if the battery had a voltage of 12 V.'), 6,
      stem=Q11V, id='phys-2023-ol-q11-vi', source_pages=[10], decision=LINKED.format(w='"this circuit"')),
    T('11vii', 'Q11(vii)', 'B', P(10, 'Explain the shape of the graph.'),
      [R('the resistance is greater at high current / due to the heating effect / as voltage', 6,
         end='increases, the current increases', note_sel=PA(3))], 'phys-3-3', 'filament-bulb-graph-shape',
      SQ(16, 'Explain the shape of the graph.'), 6, stem=[GRAPH11], fig='q11-graph', id='phys-2023-ol-q11-vii'),
    T('11viii', 'Q11(viii)', 'B', P(10, 'Sketch the graph of current against voltage for a metallic conductor held at constant',
                                   'temperature.'),
      [C('axis labelled', 3), C('correct shape', 3)], 'phys-3-3', 'metallic-conductor-graph',
      SQ(16, 'Sketch the graph of current against voltage for a metallic conductor held at constant'), 6,
      stem=[GRAPH11], fig='q11-graph',
      decision='The scheme names the shape as "correct shape" and draws none: two criterion rows. The filament '
               'bulb\'s printed graph is shown as the question\'s context.'),
    T('11ix', 'Q11(ix)', 'B', P(10, 'The charged particles that carry current through a metallic conductor are electrons.',
                               'sulfate solution?'),
      [R('ions', 5, note_sel=PA(3))], 'phys-3-3', 'charge-carriers-in-solution',
      SQ(16, 'The charged particles that carry current through a metallic conductor are electrons.'), 5,
      id='phys-2023-ol-q11-ix'),
    # --------------------------------------------------------------- Q12 --
    T('12i', 'Q12(i)', 'B', P(11, 'Name a positively charged subatomic particle.'),
      [R('proton', 3)], 'phys-4-3', 'positive-particle', SQ(17, 'Name a positively charged subatomic particle.'), 3,
      stem=[ELEC], id='phys-2023-ol-q12-i'),
    T('12ii', 'Q12(ii)', 'B', P(11, 'Name a neutral subatomic particle.'),
      [R('neutron', 3)], 'phys-4-3', 'neutral-particle', SQ(17, 'Name a neutral subatomic particle.'), 3,
      stem=[ELEC], id='phys-2023-ol-q12-ii'),
    T('12iii', 'Q12(iii)', 'B', P(11, 'Draw a labelled diagram of an atom.', 'of the subatomic particles of the atom.'),
      [C('location of proton(s)/neutron(s)', 3), C('electron', 3), C('location of electron(s)', 3)], 'phys-4-3',
      'atom-diagram', SQ(17, 'Draw a labelled diagram of an atom.'), 9, id='phys-2023-ol-q12-iii'),
    T('12iv', 'Q12(iv)', 'B', P(11, 'How are the electrons produced in a cathode ray tube?'),
      [R('thermionic emission', 6, note_sel=PA(3))], 'phys-4-1', 'producing-electrons-in-crt',
      SQ(17, 'How are the electrons produced in a cathode ray tube?'), 6, stem=[CRT], fig='q12-crt',
      id='phys-2023-ol-q12-iv'),
    T('12v', 'Q12(v)', 'B', P(11, 'How can the beam of electrons be deflected in a cathode ray', 'tube?'),
      [R('electric/magnetic field', 6, note_sel=PA(3))], 'phys-4-1', 'deflecting-the-beam',
      SQ(17, 'How can the beam of electrons be deflected in a cathode ray tube?'), 6, stem=[CRT], fig='q12-crt',
      id='phys-2023-ol-q12-v'),
    T('12vi', 'Q12(vi)', 'B', P(11, 'How is the beam of electrons detected in a cathode ray tube?'),
      [R('light on a screen', 6, note_sel=PA(3))], 'phys-4-1', 'detecting-the-beam',
      SQ(17, 'How is the beam of electrons detected in a cathode ray tube?'), 6, stem=[CRT], fig='q12-crt',
      id='phys-2023-ol-q12-vi'),
    T('12vii', 'Q12(vii)', 'B', P(11, 'How are the electrons accelerated to high speeds in an', 'X-ray tube?'),
      [R('(high) voltage', 6, note_sel=PA(3))], 'phys-4-2', 'accelerating-electrons',
      SQ(17, 'How are the electrons accelerated to high speeds in an X-ray tube?'), 6, stem=[XT], fig='q12-xray',
      id='phys-2023-ol-q12-vii'),
    T('12viii', 'Q12(viii)', 'B', P(11, 'Tungsten is often used as the target in an X-ray tube', 'a high melting point?'),
      [R('heat is produced', 6, note_sel=PA(3))], 'phys-4-2', 'target-melting-point',
      SQ(17, 'Tungsten is often used as the target in an X-ray tube because it has a high melting'), 6, stem=[XT],
      fig='q12-xray', id='phys-2023-ol-q12-viii'),
    T('12ix', 'Q12(ix)', 'B', P(11, 'X-rays are a type of electromagnetic radiation.', 'frequency of 5.5 × 10¹⁷ Hz.'),
      [R('(3 × 10⁸) ÷ (5.5 × 10¹⁷) = 5.45 × 10⁻¹⁰ m', 6, note_sel=PA(3))], 'phys-2-4', 'x-ray-wavelength',
      SQ(17, 'X-rays are a type of electromagnetic radiation.'), 6, id='phys-2023-ol-q12-ix'),
    T('12x', 'Q12(x)', 'B', P(11, 'Name one other type of electromagnetic radiation.'),
      [R('e.g. gamma', 5, note_sel=PA(3))], 'phys-2-4', 'other-em-radiation',
      SQ(17, 'Name one other type of electromagnetic radiation.'), 5,
      stem=[M('(ix)', 11), P(11, 'X-rays are a type of electromagnetic radiation.', 'frequency of 5.5 × 10¹⁷ Hz.')],
      id='phys-2023-ol-q12-x'),
    # --------------------------------------------------------------- Q13 --
    T('13i', 'Q13(i)', 'B', P(12, 'What is meant by nuclear fusion?'),
      [R('joining of two nuclei', 7, note_sel=PA(4))], 'phys-4-6', 'nuclear-fusion',
      SQ(18, 'What is meant by nuclear fusion?'), 7, stem=PASS13, id='phys-2023-ol-q13-i'),
    T('13ii', 'Q13(ii)', 'B', P(12, 'Why is there a huge force of electrostatic repulsion between two nuclei that are',
                               'brought close to each other?'),
      [R('they are both positively charged', 7, note_sel=PA(4))], 'phys-3-1', 'repulsion-between-nuclei',
      SQ(18, 'Why is there a huge force of electrostatic repulsion between two nuclei that are'), 7, stem=PASS13,
      id='phys-2023-ol-q13-ii'),
    T('13iii', 'Q13(iii)', 'B', P(12, 'The scientists used isotopes of hydrogen in this experiment.', 'What are isotopes?'),
      [R('atoms of the same atomic number but with different mass numbers', 7, note_sel=PA(4))], 'phys-4-4',
      'isotopes', SQ(18, 'The scientists used isotopes of hydrogen in this experiment.'), 7, stem=PASS13,
      id='phys-2023-ol-q13-iii'),
    T('13iv', 'Q13(iv)', 'B', [P(12, 'The symbol for tritium is H'), M('(a)', 12),
                               P(12, 'How many protons are in an atom of tritium?'), M('(b)', 12),
                               P(12, 'How many neutrons are in an atom of tritium?')],
      [pt(S('1', after='How many protons are in an atom of tritium?'), 4, label=S('(a)')),
       pt(S('2', after='How many neutrons are in an atom of tritium?'), 3, label=S('(b)'))], 'phys-4-4',
      'protons-and-neutrons-in-tritium', SQ(18, 'The symbol for tritium is H'), 7, qfig='q13iv-question',
      id='phys-2023-ol-q13-iv',
      decision='One cell "[4 + 3]" prices (a) and (b) together: one card, (a) 4 and (b) 3 in the order printed. The '
               'paper sets the tritium nuclide with stacked numbers: the question is shown as printed.'),
    T('13v', 'Q13(v)', 'B', P(12, 'Tritium decays by beta emission.', 'a beta particle?'),
      [G('equation', page=18, clip=(80, 539, 115, 563), expect='He³₂', marks=7, units=[3, 2, 2],
         note='[3 + 2 + 2]: the scheme prices the nuclide\'s symbol and its two numbers.')], 'phys-4-4',
      'beta-decay-daughter', SQ(18, 'Tritium decays by beta emission.'), 7, qfig='q13v-question',
      fig='q13v-scheme', id='phys-2023-ol-q13b-v',
      decision='The paper sets the tritium nuclide with stacked numbers: the question is shown as printed. The '
               'scheme prints the daughter nucleus with its numbers stacked after the symbol, read with '
               'G(\'equation\'); its print is the solution figure.'),
    T('13vi', 'Q13(vi)', 'B', P(12, 'In this experiment, 59 MJ of energy was produced during 5 s.',
                               'Calculate the power generated.'),
      [R('59 ÷ 5 = 11.8 MW', 7, note_sel=PA(4))], 'phys-1-4', 'power-generated',
      SQ(18, 'In this experiment, 59 MJ of energy was produced during 5 s.'), 7, stem=PASS13,
      id='phys-2023-ol-q13-vi'),
    T('13vii', 'Q13(vii)', 'B', P(12, 'Nuclear power plants currently use nuclear fission, not nuclear fusion.',
                                 'What is meant by nuclear fission?'),
      [R('the splitting of a nucleus', 7, note_sel=PA(4))], 'phys-4-6', 'nuclear-fission',
      SQ(18, 'Nuclear power plants currently use nuclear fission, not nuclear fusion.'), 7, stem=PASS13,
      id='phys-2023-ol-q13-vii'),
    T('13viii', 'Q13(viii)', 'B', P(12, 'Large amounts of money are being invested into nuclear fusion research.',
                                   'replacing nuclear fission with nuclear fusion?'),
      [C('any valid reference to fuel/products/etc.', 7, note_sel=PA(4))], 'phys-4-6', 'why-fusion-research',
      SQ(18, 'Large amounts of money are being invested into nuclear fusion research.'), 7, stem=PASS13,
      id='phys-2023-ol-q13b-viii'),
    # --------------------------------------------------------------- Q14 --
    T('14ai', 'Q14(a)(i)', 'B', P(13, 'Calculate the momentum of the train. Include units in your answer.'),
      [R('720 000', 6, note_sel=PA(3)), R('kg m s⁻¹', 3)], 'phys-1-2', 'momentum-of-train',
      SQ(19, 'Calculate the momentum of the train. Include units in your answer.'), 9, stem=[TRAIN],
      id='phys-2023-ol-q14-a-i'),
    T('14aii', 'Q14(a)(ii)', 'B', P(13, 'What is the momentum of the carriage before the coupling?', 'Explain your answer.'),
      [R('0', 3), R('because it has zero velocity', 3)], 'phys-1-2', 'momentum-of-carriage',
      SQ(19, 'What is the momentum of the carriage before the coupling?'), 6, stem=[TRAIN, CARR],
      id='phys-2023-ol-q14-a-ii'),
    T('14aiii', 'Q14(a)(iii)', 'B', P(13, 'Calculate the initial velocity of the train after it joins with the carriage.'),
      [R('720 000 ÷ 265 000 = 2.72 m s⁻¹', 6, note_sel=PA(3))], 'phys-1-2', 'velocity-after-coupling',
      SQ(19, 'Calculate the initial velocity of the train after it joins with the carriage.'), 6,
      stem=[TRAIN, CARR], id='phys-2023-ol-q14-a-iii'),
    T('14aiv', 'Q14(a)(iv)', 'B', P(13, 'Calculate the distance travelled by the train over the 8 minutes.'),
      [R('22 × 8 × 60 = 10560 m', 7, note_sel=PA(4))], 'phys-1-1', 'distance-travelled',
      SQ(19, 'Calculate the distance travelled by the train over the 8 minutes.'), 7, stem=[ACC14],
      id='phys-2023-ol-q14-a-iv'),
    T('14bi', 'Q14(b)(i)', 'B', P(13, 'Sketch the path of a ray of light through an optical', 'fibre.'),
      [C('internal reflection shown in path of ray in fibre', 6, note_sel=PA(3))], 'phys-2-3', 'ray-in-optical-fibre',
      SQ(19, 'Sketch the path of a ray of light through an optical fibre.'), 6, stem=[FIBRE],
      id='phys-2023-ol-q14-b-i'),
    T('14bii', 'Q14(b)(ii)', 'B', P(13, 'Describe a laboratory experiment to demonstrate total internal reflection.'),
      [C('apparatus', 4), C('method', 4), C('observation', 4, note_sel=PAE2)], 'phys-2-3',
      'demonstrating-total-internal-reflection',
      SQ(19, 'Describe a laboratory experiment to demonstrate total internal reflection.'), 12, stem=[FIBRE],
      decision=EXPT),
    T('14biii', 'Q14(b)(iii)', 'B', P(13, 'The critical angle of the glass in an optical fibre is 43.6°.',
                                     'refractive index of the glass.'),
      [R('1/sin 43.6° = 1.45', 6, note_sel=PA(3))], 'phys-2-3', 'refractive-index-from-critical-angle',
      SQ(19, 'The critical angle of the glass in an optical fibre is 43.6°.'), 6, id='phys-2023-ol-q14-b-iii'),
    T('14biv', 'Q14(b)(iv)', 'B', P(13, 'State one use of an optical fibre.'),
      [R('e.g. microsurgery', 4, note_sel=PA(2))], 'phys-2-3', 'use-of-optical-fibre',
      SQ(19, 'State one use of an optical fibre.'), 4, id='phys-2023-ol-q14-b-iv'),
    T('14ci', 'Q14(c)(i)', 'B', P(14, 'Draw the electric field lines around two positively charged',
                                   'particles held close to each other.'),
      [C('shape', 3), C('direction', 3)], 'phys-3-2', 'field-between-positive-charges',
      SQ(20, 'Draw the electric field lines around two positively charged particles held close to'), 6,
      stem=[FIELD], fig='q14c-field', id='phys-2023-ol-q14ci-fig'),
    T('14cii', 'Q14(c)(ii)', 'B', P(14, 'Describe what is meant by an inverse square law.'),
      [R('e.g. as one quantity doubles, the other quantity decreases by a factor of 4', 6, note_sel=PA(3))],
      'phys-3-1', 'inverse-square-law', SQ(20, 'Describe what is meant by an inverse square law.'), 6, stem=[COUL],
      id='phys-2023-ol-q14-c-ii'),
    T('14ciii', 'Q14(c)(iii)', 'B', P(14, 'Describe a laboratory experiment that uses a Van de Graaff',
                                     'hollow metal conductor.'),
      [C('apparatus', 4), C('method', 4), C('observation', 4, note_sel=PAE2)], 'phys-3-1',
      'charge-on-outside-of-conductor',
      SQ(20, 'Describe a laboratory experiment that uses a Van de Graaff generator to show'), 12, stem=[VDG],
      decision=EXPT),
    T('14civ', 'Q14(c)(iv)', 'B', P(14, 'The picture on the right shows a student touching a Van de',
                                   'Explain why her hair is standing up.'),
      [R('hair is charged (and like charges repel)', 4, note_sel=PA(2))], 'phys-3-1', 'hair-standing-up',
      SQ(20, 'The picture on the right shows a student touching a Van de Graaff generator.'), 4, stem=[VDG],
      fig='q14c-vdg', id='phys-2023-ol-q14-c-iv'),
    T('14di', 'Q14(d)(i)', 'B', P(14, 'What is a magnetic field?'),
      [R('region where magnetic forces can be felt', 6, note_sel=PA(3))], 'phys-3-4', 'magnetic-field',
      SQ(21, 'What is a magnetic field?'), 6, stem=[MAG], id='phys-2023-ol-q14-d-i'),
    T('14dii', 'Q14(d)(ii)', 'B', P(14, 'Describe a laboratory experiment to plot', 'current-carrying conductor.'),
      [C('apparatus', 6), C('method', 6, note_sel=S('[accept partial answers for 3 in each case]'))], 'phys-3-4',
      'plotting-field-around-conductor',
      SQ(21, 'Describe a laboratory experiment to plot the magnetic field around a'), 12, stem=[MAG],
      decision='A "describe an experiment" part: the scheme prices apparatus and method and prints no answer.'),
    T('14diii', 'Q14(d)(iii)', 'B', P(14, 'A straight piece of wire of length 1.8 m carrying a current of 3 A experiences a',
                                     'Calculate the magnetic flux density.'),
      [R('11 ÷ (3 × 1.8) = 2.04 T', 6, note_sel=PA(3))], 'phys-3-5', 'magnetic-flux-density',
      SQ(21, 'A straight piece of wire of length 1.8 m carrying a current of 3 A experiences a'), 6, stem=FORCE14,
      id='phys-2023-ol-q14-d-iii'),
    T('14div', 'Q14(d)(iv)', 'B', P(14, 'Magnetic flux density is an example of a vector quantity.',
                                   'Name another example of a vector quantity.'),
      [R('e.g. force', 4)], 'phys-1-1', 'vector-quantity',
      SQ(21, 'Magnetic flux density is an example of a vector quantity.'), 4, id='phys-2023-ol-q14-d-iv'),
]

ANSWER_VARIANTS = {}
RETAINED = {}
WITHDRAW = {}

FIGURES = {
    # key suffix: (doc, page, rect in PDF points, credit, letters, alt, solution)
    'q1iv-scheme-graph': ('scheme', 6, (140, 415, 512, 640), SEC, [], "The marking scheme's graph: a (m s⁻²), from 0 to 4.5, against F (N), from 0 to 1.4, with six plotted points from 0.2 N to 1.2 N on a straight line drawn from the origin.", True),
    'q3-diagram': ('paper', 3, (100, 242, 545, 452), SEC, ['A', 'B'], 'Diagram of the apparatus: a calorimeter of water with crushed ice standing in a larger container, the outer container pointed to by an arrow labelled B; a long rod with a bulb at its lower end dips into the water, pointed to by an arrow labelled A; beside it a dark cloth holding crushed ice.', False),
    'q3ix-question': ('paper', 3, (52, 55, 548, 685), SEC, ['A', 'B'], 'The printed Question 3: the latent heat of fusion experiment with its results (masses 0.083 kg, 0.181 kg and 0.008 kg; temperatures 23 °C and 16 °C), the apparatus diagram with A and B, and parts (i) to (ix), the last with its note E = m(ice) l + m(ice) c(water) Δθ(ice), the words in brackets printed as subscripts.', False),
    'q4v-question': ('paper', 4, (52, 55, 548, 335), SEC, [], 'The printed Question 4 up to part (v): the speed of sound experiment, its table of f (Hz) 256, 288, 320, 341, 384, 480 against l (m) 0.33, 0.29, 0.27, 0.25, 0.22, 0.18, and parts (i) to (v), (v) asking for the value of 1 over l, set as a fraction, to 2 decimal places.', False),
    'q4vi-question': ('paper', 4, (52, 55, 548, 362), SEC, [], 'The printed Question 4 up to part (vi): the speed of sound experiment, its table of f (Hz) 256, 288, 320, 341, 384, 480 against l (m) 0.33, 0.29, 0.27, 0.25, 0.22, 0.18, and parts (i) to (vi), (vi) asking for a graph of f against 1 over l, set as a fraction.', False),
    'q4vi-scheme-graph': ('scheme', 9, (112, 556, 484, 782), SEC, [], "The marking scheme's graph: 1/l (m⁻¹), from 0 to 6, against f (Hz), from 0 to 600, with six plotted points from about 3.0 to 5.6 on a straight line that meets the vertical axis just above zero.", True),
    'q5iii-scheme-graph': ('scheme', 10, (140, 411, 512, 637), SEC, [], "The marking scheme's graph: R (Ω), from 0 to 0.35, against l (m), from 0 to 0.8, with six plotted points from 0.2 m to 0.7 m on a dotted straight line drawn from the origin.", True),
    'q8-diagram': ('paper', 7, (140, 75, 420, 300), SEC, ['A', 'B', 'C'], 'Diagram of a ray of light passing through a rectangular glass block: the ray arriving at the top face is pointed to by an arrow labelled A, a dashed vertical line at the point of entry by an arrow labelled C, and the ray inside the block by an arrow labelled B; the ray leaves through the bottom face.', False),
    'q9-brick': ('paper', 8, (314, 240, 545, 347), 'willamettegraystone.com', ['A', 'B', 'C'], 'Photograph of a rectangular brick with three faces lettered: A on the small end face, B on the top face and C on the long side face; its dimensions are marked w = 9 cm, h = 6 cm and l = 20 cm.', False, [(314, 298, 326, 322)]),
    'q10-wave': ('paper', 9, (80, 360, 546, 442), SEC, ['A', 'B'], 'Diagram of a standing wave on a string fixed between two posts: a solid and a dotted curve cross at the points marked A and B, and a double arrow labelled h marks the height of one loop.', False),
    'q11-bulb': ('paper', 10, (360, 120, 545, 222), 'electricityforum.com', [], 'Drawing of a light bulb joined by two wires to the + and – ends of a battery, labelled light bulb and battery.', False),
    'q11-graph': ('paper', 10, (95, 365, 560, 578), SEC, [], 'Graph of current (mA), from 0 to 60, against voltage (V), from 0 to 6, for a filament bulb: a curve rising from the origin, steep at first and levelling off near 56 mA at 6 V.', False),
    'q12-crt': ('paper', 11, (417, 158, 541, 248), 'wikipedia.org', [], 'Photograph of a cathode ray tube: a glass tube with electrodes inside, widening at one end into a flat, square screen.', False),
    'q12-xray': ('paper', 11, (417, 276, 541, 360), 'wikipedia.org', [], 'Photograph of an X-ray tube: a glass tube with metal electrodes, a finned metal cap at one end and wire leads at the other.', False),
    'q13iv-question': ('paper', 12, (52, 452, 548, 503), SEC, [], 'The printed part (iv): The symbol for tritium is H, with 3 above and 1 below. (a) How many protons are in an atom of tritium? (b) How many neutrons are in an atom of tritium? (7)', False),
    'q13v-question': ('paper', 12, (52, 507, 548, 541), SEC, [], 'The printed part (v): Tritium decays by beta emission. What is the daughter nucleus when an atom of H, with 3 above and 1 below, emits a beta particle? (7)', False),
    'q13v-scheme': ('scheme', 18, (80, 539, 115, 563), SEC, [], "The marking scheme's answer: He with 3 above and 2 below, the two numbers printed after the symbol.", True),
    'q14c-field': ('paper', 14, (440, 53, 542, 131), 'wikipedia.org', [], 'Diagram of the electric field around a positive and a negative charge side by side: curved field lines with arrows run from the + charge to the – charge, and outer lines spread away from + and in towards –.', False),
    'q14c-vdg': ('paper', 14, (448, 208, 540, 301), 'fishersci.com', [], 'Photograph of a student with her hand on the dome of a Van de Graaff generator, her hair standing out from her head.', False),
}
