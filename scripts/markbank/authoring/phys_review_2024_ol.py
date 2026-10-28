"""Physics 2024 Ordinary Level — reviewed task ledger, correcting the sitting in place.

Independent visual sweep (2026-10-28), every page rendered and read:
  * The paper (LC021GLP000EV), 16 pages: p1 cover (the 2024 papers were adjusted for disruption
    to learning; "Answer three questions from Section A and five questions from Section B"),
    p2-p4 Section A Questions 1-5 (40 marks each, group marks printed after runs of romans),
    p5-p14 Section B Questions 6-14 (56 marks each), p15 acknowledgements (images on pages 2,
    4, 5, 6, 7, 9, 10, 11, 12, 13, 14), p16 back cover.
  * The marking scheme, 24 pages: p1 cover, p2 note on published schemes, p3 points to note
    (solidus, double solidus, slips), p4 annotation symbols, p5 Irish-language bonus table,
    p6-p22 Questions 1-14 (each question reprinted, its answers in bold, the mark cells at the
    right margin, most rows followed by the scheme's partial allowance "[accept partial answer
    for 3]"), p23 blank, p24 back cover.

Every printed ask is carded at the scheme's own mark boundary: a roman, or a sub-letter where the
scheme prices (a) and (b) apart (Q11(vii), Q14(b)(iv)). Where one cell prices a roman's sub-letters
together (Q12(ii) "[6+3]") the roman is one card. Q6 is "Answer any eight of (a)-(l)" (best eight of
twelve at 7 each = 56). Q13 prints (a)-(h) at 7 each. Q14 is "Answer any two of (a), (b), (c), (d)"
(four 28s, all carded); the group marks inside each letter ((13)/(15), (18)/(10) three times) were
checked by hand against the tasks: every one adds up. The partial allowance printed under a row is
that row's note.

The census read (paper_census) needed one gated entry (paper.PROSE_MARKER_BLOCKS, 2024 OL): Q14(b)(iv)
prints "(a)" and "(b)" inside the roman, which had been read as top-level letters (Q14(b)(iv) read
empty, flag empty-leaf).

Maths read from glyph positions: stacked fractions with G('fraction'), the scheme's daughter nucleus
in Q12(vi) with G('equation'). The paper sets 1/l (Q4(v), (vi)), lambda/4 (Q10(vi)) and the
plutonium and alpha nuclides (Q12(vi)) as stacked text the text layer cannot order: those asks are
shown as printed (question figures).

The sitting was already carded (109 authored cards, 108 shipped). Every task is re-derived from the
PDFs and the existing cards are corrected in place: every id is kept, mapped (`id=`) to the task it
was carding, or withdrawn onto its twin (Q6(c) was carded twice, with and without the diagram). The
seven asks the bank had excluded (Q2(vi), Q6(d), Q6(k), Q6(l), Q8(iv), Q10(ii), Q14(d)(ii)) and the
ten open ones (Q2(v), Q6(h), Q9(ii), Q9(v), Q10(iii), Q10(vi), Q11(viii), Q11(ix), Q14(b)(iv),
Q14(c)(iii)) are carded, with Q11(vii)(a), which the old cards had left out.
"""
from phys_review_lib import Q, SQ, S, M, G, pt, anyn, allof, T, L

YEAR, LEVEL = 2024, 'ol'
REVIEWED_AT = '2026-10-28'
BASELINE_COMMIT = '99ec7f0a0d6b243f4d5a1dc9b14a6a958e98095e'

SOURCES = {
    'paper': {'path': 'examiner-reports/physics/papers/2024-ol-paper.pdf', 'fileid': 'LC021GLP000EV.pdf',
              'sha256': '60ef2b1b94f5c60c5589fd019b6ee590fdb0b6253eb2e77d891562255b74314b', 'pages': 16},
    'scheme': {'path': 'examiner-reports/physics/schemes/2024-ol.pdf', 'fileid': 'LC021GLP000EV.pdf',
               'sha256': '13577ca8546caf7e616343950217bebe589aeb71245348318f65c5622146ca51', 'pages': 24},
}

PAGE_ROLES = {
    'paper': {1: 'cover', **{p: 'questions' for p in range(2, 15)}, 15: 'acknowledgements', 16: 'back-cover'},
    'scheme': {1: 'cover', 2: 'note', 3: 'conventions', 4: 'annotations', 5: 'irish-bonus-table',
               **{p: 'marking' for p in range(6, 23)}, 23: 'blank', 24: 'back-cover'},
}

LETTERED = {6, 13, 14}

QUESTION_TOTALS = {**{n: 40 for n in range(1, 6)}, **{n: 56 for n in range(6, 14)},
                   14: 112}   # any two of (a)-(d), 28 each: all four carded
PART_TOTALS = {**{(14, x): 28 for x in 'abcd'}, **{(13, x): 7 for x in 'abcdefgh'}}
BEST_OF = {6: (8, 7)}
GROUP_TOTALS = {
    (1, ('i', 'ii', 'iii')): 18, (1, ('iv', 'v', 'vi', 'vii')): 22,
    (2, ('i', 'ii')): 18, (2, ('iii', 'iv', 'v', 'vi')): 22,
    (3, ('i', 'ii')): 16, (3, ('iii', 'iv')): 12, (3, ('v',)): 12,
    (4, ('i', 'ii', 'iii', 'iv')): 24, (4, ('v', 'vi')): 16,
    (5, ('i', 'ii', 'iii')): 22, (5, ('iv', 'v', 'vi')): 18,
    (7, ('i', 'ii', 'iii')): 18, (7, ('iv', 'v', 'vi')): 21, (7, ('vii', 'viii')): 17,
    (8, ('i', 'ii', 'iii', 'iv')): 27, (8, ('v', 'vi', 'vii', 'viii')): 29,
    (9, ('i', 'ii', 'iii', 'iv')): 24, (9, ('v', 'vi', 'vii')): 18, (9, ('viii', 'ix', 'x')): 14,
    (10, ('i', 'ii')): 18, (10, ('iii', 'iv', 'v', 'vi', 'vii')): 27, (10, ('viii', 'ix')): 11,
    (11, ('i', 'ii', 'iii', 'iv', 'v', 'vi')): 32, (11, ('vii', 'viii', 'ix')): 24,
    (12, ('i', 'ii', 'iii')): 18, (12, ('iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x')): 38,
}
CHECKSUMS = {}
ROUTES = {}

SCAN_PAGES = {'paper': range(2, 15)}
SELECTION_SCAN = [
    ('paper', 3, 'the following', 'Q2 "The following results were recorded": a reference to the table.'),
    ('paper', 3, 'the following', 'Q3 "The following results were recorded": a reference to the data.'),
    ('paper', 3, 'the following', 'Q3(v) "complete the following calculations": a reference to the layout printed.'),
    ('paper', 4, 'the following', 'Q4 "the following results": a reference to the table.'),
    ('paper', 4, 'the following', 'Q5 "the following data": a reference to the table.'),
    ('paper', 5, 'the following', 'Q6 "Answer any eight of the following parts": best eight of twelve at 7; every '
                                  'part is carded (BEST_OF).'),
    ('paper', 8, 'or', 'Q9 lead-in "heated or cooled": description.'),
    ('paper', 9, 'both', 'Q10 lead-in "open at both ends": description.'),
    ('paper', 9, 'both', 'Q10(viii) "a pipe open at both ends": description.'),
    ('paper', 9, 'both', 'Q10(ix) "open at both ends": description.'),
    ('paper', 10, 'or', 'Q11(vii)(a) "X or Y": the answer options; one answer.'),
    ('paper', 12, 'the following', 'Q13 "Read the following passage": a reference to the passage.'),
    ('paper', 13, 'any two', 'Q14 "Answer any two of the following parts": every part is carded.'),
    ('paper', 13, 'the following', 'Q14, the same rubric.'),
    ('paper', 13, 'or', 'Q14(b)(iv)(b) "lighting or not": the answer options; one answer.'),
    ('paper', 14, 'or', 'Q14(d) lead-in "gains or loses electrons": description.'),
    ('paper', 14, 'or', 'Q14(d)(iv) "gained or lost electrons": the answer options; one answer.'),
]
ASK_SCAN_PAGES = {'paper': range(2, 15)}
ASK_EXEMPT = [
    (9, 'When a person sings, their vocal chords vibrate.',
     'Q10 lead-in ("When a person sings, their vocal chords vibrate. ..."): a description, not an ask; lifted into '
     'the (i) and (ii) stems.'),
    (11, 'When uranium undergoes nuclear fission, neutrons are produced',
     'Q12 lead-in to (vii)-(viii): a description, not an ask; lifted into their stems.'),
    (14, 'When white light is passed through the diffraction grating',
     'Q14(c) lead-in to (iv)-(v): a description, not an ask; lifted into their stems.'),
]

SEC = 'State Examinations Commission'
CRIT = 'The scheme prints no answer here, only what earns the marks.'
DRAWN = 'The scheme prints no drawing; this line names what the diagram must show.'
NOLABEL = S('[–1 if no label present on diagram]')
NOLABEL_IS = S('[–1 if no label is present on diagram]')
EACH = S('[accept partial answers for 2 in each case]')
ORDERED = ('The scheme prints these items under one sum, {cell}, and names no order: a response earns '
           'the marks step by step.')


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


def FR(page, clip, expect, marks, **kw):
    """A formula the scheme sets as a stacked fraction."""
    return G('fraction', page=page, clip=clip, expect=expect, marks=marks, **kw)


def pieces(sel, marks, sep, **kw):
    """One row per entry of a printed list, at the marks its cell prints for it in order."""
    return [pt(dict(sel, piece=i + 1, psep=sep), m, **kw) for i, m in enumerate(marks)]


# ------------------------------------------------------------------ stems --
STEM1 = [P(2, 'A student carried out an experiment to investigate the laws of equilibrium.',
           'until it was balanced and level.'),
         P(2, 'Before setting up the experiment, the student took two measurements.',
           'centre of gravity at the 50 cm mark.'),
         P(2, 'His results are shown in the tables below.')]
LAW1 = P(2, 'The first law of equilibrium states that the sum of the upward forces equals the sum of the',
         'downward forces.')
LAW2 = P(2, 'The second law of equilibrium states that the sum of the clockwise moments equals the sum',
         '(Remember: Moment = Force × Distance)')
STEM2 = [P(3, 'A student carried out an experiment to measure f, the focal length of a converging lens.')]
OUTSIDE = P(3, 'The student ensured that the object was placed outside the focal length of the lens.')
RESULTS2 = P(3, 'The following results were recorded.')
STEM3 = [P(3, 'A student carried out an experiment to measure cwater, the specific heat capacity of water.'),
         P(3, 'She added heat energy ∆E to water in a copper calorimeter.')]
DATA3 = [P(3, 'The following results were recorded.', after='She added heat energy'),
         P(3, 'Mass of empty copper calorimeter, mcalorimeter', '0.106 kg', br=True),
         P(3, 'Mass of calorimeter and cold water', '0.262 kg', br=True),
         P(3, 'Initial temperature of cold water and calorimeter', '18 °C', br=True),
         P(3, 'Final temperature of water and calorimeter', '23 °C', br=True),
         P(3, 'Heat energy added, ∆E', '3467 J', br=True)]
Q3III = P(3, 'Calculate A, the mass of the water mwater.')
Q3IV = P(3, 'Calculate B, the increase in temperature of the calorimeter and the cold water.')
STEM4 = [P(4, 'A student carried out an experiment to investigate how the fundamental frequency f of a',
           'throughout the experiment.'),
         P(4, 'On the right is a diagram', 'this experiment.')]
RESULTS4 = P(4, 'The student recorded the following results.')
STEM5 = [P(4, 'A student carried out an experiment to investigate how the resistance R of a metallic',
           'changes with temperature T.')]
DATA5 = P(4, 'The student recorded the following data.')
LIQUID = P(4, 'The student used the apparatus to estimate the temperature of an unknown liquid.',
           'resistance was measured as 5.5 Ω.')
STEM7 = [P(6, 'Oleksii Novikov from Ukraine broke the world record in 2020 in the',
           'from the ground to a height of 46 cm.')]
G7 = P(6, 'acceleration due to gravity g = 9.8 m s⁻²', br=True)
Q7II = P(6, 'Calculate the weight of a 537.5 kg mass.')
DEADLIFT = P(6, 'To successfully complete the deadlift, a lifter has to bring the bar to a height of 46 cm and',
             'lowered to the ground.')
BUS = P(6, 'In 2020, Novikov won the World’s Strongest Man competition.', 'The bus has a mass of 19 000 kg.')
COURSE = P(6, 'It took one man 52 s to complete the course.', 'for the bus to roll to a stop.')
STEM8 = [P(7, 'Light can be reflected by many different surfaces.'),
         P(7, 'The picture on the right shows light being reflected', 'An image is formed.')]
LAW8 = P(7, 'One of the laws of reflection of light states that the angle of incidence equals the angle of',
         'reflection.')
CURVED = P(7, 'Light is also reflected from curved mirrors.')
PICTURE = P(7, 'The picture on the right shows images in a', 'concave mirror.')
MAG = P(7, 'An object is placed 20 cm in front of a', '40 cm in front of the mirror.')
Q8VII = P(7, 'Calculate the magnification m of this', 'image.')
STEM9 = [P(8, 'Solids, liquids and gases can change state when they are heated or cooled.',
           'from a liquid to a gas.')]
STEM9A = [P(8, 'Solids, liquids and gases can change state when they are heated or cooled.',
            'as it changes state.')]
BACK = P(8, 'The heat pump also turns the gas back into a liquid.')
THERMO = P(8, 'The temperature of the refrigerant can be measured using a thermometer.')
STEM10 = [P(9, 'When a person sings, their vocal chords vibrate.', 'if resonance occurs.')]
CLARINET = P(9, 'A clarinet is an instrument that can be thought of as a pipe closed at one end.')
AMPL = P(9, 'If a musician increases the loudness of the note she plays, she has increased the amplitude',
         'of the sound wave.')
FLUTE = P(9, 'A flute is an instrument that can be thought of as a pipe that is open at both ends.')
STEM11 = [P(10, 'Electric current is the movement of charged particles through a conductor.')]
FUSE = P(10, 'A fuse is used as a safety precaution.')
MCB = P(10, 'A miniature circuit breaker (MCB) is another device used for safety.')
OHM = P(10, 'The circuit below is used in an experiment to demonstrate Ohm’s law.')
Q11VIIA = P(10, 'Which of the devices, X or Y is a', 'Explain your answer.')
PREV = P(10, 'Previous results from the experiment have shown the resistance of the coil of wire is 2.5 Ω.')
RODS = P(11, 'The control rods and the moderator play a very', 'fission.')
FUELS = P(11, 'The fuels typically used in a nuclear fission reactor are isotopes of plutonium and uranium.')
PU = P(11, 'Pu–239 is an isotope of plutonium.', '24 110 years.')
NEUTRONS = P(11, 'When uranium undergoes nuclear fission, neutrons are produced in the reaction.',
             'Neutrons are sub-atomic particles.')
FUSION = P(11, 'Nuclear fusion is another type of nuclear reaction.')
PASSAGE = [P(12, 'Read the following passage and answer the questions below.'),
           P(12, 'Every year astronauts go to the International Space', 'during spaceflight.'),
           P(12, 'Adapted from: www.ScienceJournalForKids.org', br=True)]
STEM14A = [P(13, 'Newton’s three laws of motion describe the relationship between the motion of an',
             'forces acting on it.'),
           P(13, 'A 1900 kg car is moving at 20 m s⁻¹ to the right on a horizontal road.',
             'opposite directions as shown.')]
SECOND = [P(13, 'Newton’s second law of motion states that the rate of change of momentum of an',
            'net force applied to it.'),
          P(13, 'The same car is still moving at 20 m s⁻¹ to the right but it now has unbalanced forces',
            'acting on it as shown.')]
STEM14B = [P(13, 'A thermistor is a type of resistor made of semiconductor material whose',
             'dependent on temperature.')]
NOTE14 = P(13, 'Note: You may refer to the electrical circuit symbols on pages 72 to 78 of the Formulae',
           'when answering part (iv).')
Q14BIVA = P(13, 'Draw a circuit diagram to show a semiconductor diode connected in series', 'with a filament bulb.')
STEM14C = [P(14, 'A laser light is shone at right angles to a diffraction grating as shown in the diagram',
             'be seen on the screen.')]
GRATING = P(14, 'The diffraction grating has a grating constant d of 2.5 × 10⁻⁶ m.',
            'from the straight through position.')
WHITE = P(14, 'When white light is passed through the diffraction grating, it is split into its constituent',
          'colours.')
STEM14D = [P(14, 'Objects with opposite charges attract each other and objects with the', 'repel each other.')]
GAIN = P(14, 'An object becomes charged when it gains or loses electrons.')
PEAR = P(14, 'A student performed an experiment to investigate how charge is', 'pear-shaped conductor.')

# Q3(i)'s list, one printed sentence over two lines; its options are cut at the scheme's own commas,
# keeping "(e.g. hot copper, heating coil)" and "e.g. lagging, lid, stirrer, etc." with their items.
LIST3 = S('calorimeter, water, source of heat (e.g. hot copper, heating coil), thermometer, mass', 'stirrer, etc.')

TASKS = [
    # ============================================================ Section A ==
    # ---- Q1 laws of equilibrium -------------------------------------------------
    T('1i', 'Q1(i)', 'A', P(2, 'How did the student measure the weight of the metre stick?'),
      [R('using a Newton balance / using a mass balance (and multiplying by g)', 6, kind='point', note_sel=PA(3))],
      'phys-u2', 'measuring-weight-of-metre-stick',
      SQ(6, 'How did the student measure the weight of the metre stick?'), 6, stem=STEM1[:2], fig='q1-tables',
      id='phys-2024-ol-q1-i'),
    T('1ii', 'Q1(ii)', 'A', P(2, 'Describe how he found the centre of gravity of the metre stick.'),
      [R('balance on a pivot', 6, note_sel=PA(3))], 'phys-u2', 'finding-centre-of-gravity',
      SQ(6, 'Describe how he found the centre of gravity of the metre stick.'), 6, stem=STEM1[:2], fig='q1-tables',
      id='phys-2024-ol-q1-ii'),
    T('1iii', 'Q1(iii)', 'A', [P(2, 'Copy the diagram of the metre stick below into your answerbook.', 'have been included.'),
                               P(2, 'Complete your diagram to show all upward and downward forces and their positions.')],
      [R('upward force of 4 N at 70 cm', 2), R('downward force of 5 N at 26 cm', 2), R('downward force of 2 N at 60 cm', 2)],
      'phys-1-2', 'forces-on-metre-stick',
      SQ(6, 'Copy the diagram of the metre stick below into your answerbook.'), 6, stem=STEM1,
      qfig='q1iii-question', fig='q1-tables', id='phys-2024-ol-q1-iii-fig',
      decision='[3×2] against the three forces printed one a line: 2 each. The ask is shown as printed, with the '
               'metre stick to be copied; the results tables are the figure.'),
    T('1iv', 'Q1(iv)', 'A', P(2, 'Use the data to show that the first law of equilibrium is verified in this experiment.'),
      [allof([(None, S('upward forces = 6 + 4 = 10 N')), (None, S('downward forces = 5 + 2 + 3 = 10 N'))], 6,
             note_sel=PA(3))],
      'phys-1-2', 'first-law-of-equilibrium',
      SQ(6, 'Use the data to show that the first law of equilibrium is verified in this experiment.'), 6,
      stem=STEM1 + [LAW1], fig='q1-tables', id='phys-2024-ol-q1-iv',
      decision='One cell [6] prices the two sums printed on two lines together: one row holding both.'),
    T('1v', 'Q1(v)', 'A', P(2, 'Use the data to calculate the clockwise moments on the metre stick about the', '0 cm mark.'),
      [R('(5 × 26) + (3 × 50) + (2 × 60) = 400 N cm', 6, note_sel=PA(3))], 'phys-1-2', 'clockwise-moments',
      SQ(6, 'Use the data to calculate the clockwise moments on the metre stick about the 0 cm'), 6,
      stem=STEM1 + [LAW2], fig='q1-tables', id='phys-2024-ol-q1-v'),
    T('1vi', 'Q1(vi)', 'A', P(2, 'Use the data to calculate the anticlockwise moments on the metre stick about the',
                              '0 cm mark.'),
      [R('(6 × 20) + (4 × 70) = 400 N cm', 6, note_sel=PA(3))], 'phys-1-2', 'anticlockwise-moments',
      SQ(6, 'Use the data to calculate the anticlockwise moments on the metre stick about the'), 6,
      stem=STEM1 + [LAW2], fig='q1-tables', id='phys-2024-ol-q1-vi'),
    T('1vii', 'Q1(vii)', 'A', P(2, 'Use your calculations to show that the second law of equilibrium is verified in this',
                                'experiment.'),
      [R('(the sum of) clockwise moments are equal to anticlockwise moments', 4, note_sel=PA(2))], 'phys-1-2',
      'second-law-of-equilibrium',
      SQ(6, 'Use your calculations to show that the second law of equilibrium is verified in this'), 4,
      stem=[LAW2], id='phys-2024-ol-q1-vii'),
    # ---- Q2 focal length of a converging lens -----------------------------------
    T('2i', 'Q2(i)', 'A', P(3, 'Draw a labelled diagram of the arrangement of the apparatus used in this experiment.'),
      [C('converging lens', 4), C('object', 4), C('screen', 2), C('correct arrangement', 2, note_sel=NOLABEL_IS)],
      'phys-u2', 'lens-apparatus',
      SQ(7, 'Draw a labelled diagram of the arrangement of the apparatus used in this experiment.'), 12, stem=STEM2,
      id='phys-2024-ol-q2-i', decision='[4+4+2+2] against the four lines: in the order printed.'),
    T('2ii', 'Q2(ii)', 'A', P(3, 'On your diagram, indicate and label the object distance u and the image distance v.'),
      [C('both distances indicated correctly', 6, units=[4, 2], note_sel=PA(3),
         note=CRIT + ' It prices the line [4+2].')],
      'phys-u2', 'marking-u-and-v',
      SQ(7, 'On your diagram, indicate and label the object distance u and the image distance v.'), 6, stem=STEM2,
      id='phys-2024-ol-q2-ii'),
    T('2iii', 'Q2(iii)', 'A', P(3, 'Explain why the student had to place the object outside the focal length of the lens.'),
      [R('to get an image on the screen / to get a real image', 6, kind='point', note_sel=PA(3))], 'phys-u2',
      'object-outside-focal-length',
      SQ(7, 'Explain why the student had to place the object outside the focal length of the lens.'), 6,
      stem=STEM2 + [OUTSIDE], id='phys-2024-ol-q2-iii'),
    T('2iv', 'Q2(iv)', 'A', P(3, 'How did the student know that the correct image distance had been found?'),
      [R('focussed image', 6, note_sel=PA(3))], 'phys-u2', 'finding-the-image',
      SQ(7, 'How did the student know that the correct image distance had been found?'), 6, stem=STEM2 + [OUTSIDE],
      id='phys-2024-ol-q2-iv'),
    T('2v', 'Q2(v)', 'A', P(3, 'Using the Formulae and Tables booklet, write the lens formula used to calculate f.'),
      [FR(7, (110, 446, 155, 473), '1/f = 1/u + 1/v', 4, note_sel=PA(2))], 'phys-2-3', 'lens-formula',
      SQ(7, 'Using the formulae and tables booklet, write the lens formula used to calculate f.'), 4, stem=STEM2,
      decision='The bank had left this part open: the formula is read from where the scheme prints it.'),
    T('2vi', 'Q2(vi)', 'A', P(3, 'Use the formula and the data in the table to calculate f.'),
      [C('calculation of f', 6, note_sel=PA(3))], 'phys-2-3', 'focal-length-from-data',
      SQ(7, 'Use the formula and the data in the table to calculate f'), 6, stem=STEM2 + [RESULTS2], fig='q2-table',
      decision='The bank had excluded this part. The scheme prints "calculation of f [6]" and no value: one '
               'criterion row in its words.'),
    # ---- Q3 specific heat capacity of water --------------------------------------
    T('3i', 'Q3(i)', 'A', P(3, 'Draw a labelled diagram of the apparatus used in this experiment.'),
      [anyn(None, 4, 4, steps=[4, 2, 2, 2], open_list=True, note_sel=NOLABEL,
            note='The scheme prints "[any 4: 4+2+2+2]" under this list: any four, the first 4 and the rest 2 each.',
            options=[dict(LIST3, piece=1, psep=', '), dict(LIST3, piece=2, psep=', '),
                     dict(LIST3, piece=[2, 1], psep=['water, ', ', thermometer']),
                     dict(LIST3, piece=[2, 1], psep=['), ', ', ']), dict(LIST3, piece=[2, 2], psep=['), ', ', ']),
                     dict(LIST3, piece=[2, 3], psep=['), ', ', ']), dict(LIST3, piece=2, psep='joulemeter, ')])],
      'phys-u2', 'calorimetry-apparatus', SQ(8, 'Draw a labelled diagram of the apparatus used in this experiment.'), 10,
      stem=STEM3, id='phys-2024-ol-q3-i'),
    T('3ii', 'Q3(ii)', 'A', P(3, 'How did the student supply the heat energy needed to increase the temperature of',
                              'the water and the calorimeter?'),
      [C('any heat source', 6, note_sel=PA(3))], 'phys-u2', 'supplying-heat-energy',
      SQ(8, 'How did the student supply the heat energy to increase the temperature of the water'), 6, stem=STEM3,
      id='phys-2024-ol-q3-ii'),
    T('3iii', 'Q3(iii)', 'A', Q3III,
      [R('0.262 – 0.106 = 0.156 kg', 6, note_sel=PA(3))], 'phys-u2', 'mass-of-water',
      SQ(8, 'Calculate A, the mass of the water.'), 6, stem=STEM3 + DATA3, id='phys-2024-ol-q3-iii'),
    T('3iv', 'Q3(iv)', 'A', Q3IV,
      [R('23 – 18 = 5 ℃', 6, note_sel=PA(3))], 'phys-u2', 'temperature-rise',
      SQ(8, 'Calculate B, the increase in temperature of the calorimeter and cold water.'), 6, stem=STEM3 + DATA3,
      id='phys-2024-ol-q3-iv'),
    T('3v', 'Q3(v)', 'A', P(3, 'Using your answers for A and B, and given that the specific heat capacity of copper',
                            'find a value of cwater.'),
      [C('substitution for A', 4), C('substitution for B', 4), R('c = 4179.98 J kg⁻¹ K⁻¹', 4)], 'phys-2-1',
      'specific-heat-capacity-of-water',
      SQ(8, 'Use your answers for A and B to complete the following calculations to find c.',
         paired='The scheme reprints the ask shorter ("to find c"); the paper names cwater and the copper value.'),
      12, stem=STEM3 + DATA3 + [M('(iii)', 3), Q3III, M('(iv)', 3), Q3IV], fig='q3-calc', id='phys-2024-ol-q3-v',
      decision='The paper prints the calculation to complete as a layout of three lines (the figure).'),
    # ---- Q4 frequency and length of a stretched string ----------------------------
    T('4i', 'Q4(i)', 'A', P(4, 'How did the student set the string vibrating?'),
      [R('using a tuning fork / using a frequency generator / pluck the string', 6, kind='point', note_sel=PA(3))],
      'phys-u2', 'setting-the-string-vibrating', SQ(9, 'How did the student set the string vibrating?'), 6,
      stem=STEM4, fig='q4-sonometer', id='phys-2024-ol-q4-i'),
    T('4ii', 'Q4(ii)', 'A', P(4, 'Describe what length l of string the student should measure.'),
      [R('distance between the bridges', 6, note_sel=PA(3))], 'phys-u2', 'length-to-measure',
      SQ(9, 'Describe what length l of string the student should measure.'), 6, stem=STEM4, fig='q4-sonometer',
      id='phys-2024-ol-q4-ii'),
    T('4iii', 'Q4(iii)', 'A', P(4, 'Explain why the tension of the string was kept constant.'),
      [R('frequency depends on tension [state or imply] / fair test', 6, kind='point', note_sel=PA(3))], 'phys-u2',
      'constant-tension', SQ(9, 'Explain why the tension of the string was kept constant.'), 6, stem=STEM4,
      fig='q4-sonometer', id='phys-2024-ol-q4-iii'),
    T('4iv', 'Q4(iv)', 'A', P(4, 'What was the function of the paper rider?'),
      [R('indicates that resonance has occurred [state or imply]', 6, kind='point', note_sel=PA(3))], 'phys-u2', 'paper-rider',
      SQ(9, 'What is the function of the paper rider?'), 6, stem=STEM4, fig='q4-sonometer', id='phys-2024-ol-q4-iv'),
    T('4v', 'Q4(v)', 'A', P(4, 'Copy and complete the table above into your answerbook by calculating the value',
                            'to 2 decimal places.'),
      [R('6.25', 1, note='The four values the scheme prints for the empty cells of the table, in the order printed.'),
       R('7.87', 1), R('8.77', 1), R('9.35', 1)],
      'phys-u2', 'completing-the-table',
      SQ(9, 'Copy and complete the table above into your answerbook by calculating the value'), 4,
      stem=STEM4[:1] + [RESULTS4], qfig='q4v-question', fig='q4-table', id='phys-2024-ol-q4-v',
      decision='[4×1] against the four values: 1 each. The paper sets 1/l as a stacked fraction the text layer '
               'cannot order: the ask is shown as printed. The scheme heads its row (cm⁻¹) where the paper prints '
               '(m⁻¹).'),
    T('4vi', 'Q4(vi)', 'A', P(4, 'Use the data to plot a graph of', 'against f.'),
      [C('labelled axis', 3), C('points plotted', 6, units=[1] * 6, note=CRIT + ' It prices them [6×1].'),
       C('line of best fit', 3)], 'phys-u2', 'graph-of-one-over-l-against-f',
      SQ(9, 'Use the data to plot a graph of f against'), 12, stem=STEM4[:1] + [RESULTS4], qfig='q4vi-question',
      fig='q4-table', id='phys-2024-ol-q4-vi',
      decision='The paper sets 1/l as a stacked fraction: the ask is shown as printed. The scheme reprints it as "a '
               'graph of f against 1/l".'),
    # ---- Q5 resistance and temperature -----------------------------------------
    T('5i', 'Q5(i)', 'A', P(4, 'Draw a labelled diagram of the arrangement of the apparatus used in this experiment.'),
      [C('conductor', 4), C('ohmmeter', 4), C('thermometer', 2), C('arrangement', 2, note_sel=NOLABEL)],
      'phys-u2', 'resistance-temperature-apparatus',
      SQ(10, 'Draw a labelled diagram of the arrangement of the apparatus used in this experiment.'), 12, stem=STEM5,
      id='phys-2024-ol-q5-i', decision='[4+4+2+2] against the four lines: in the order printed.'),
    T('5ii', 'Q5(ii)', 'A', P(4, 'How did the student vary the temperature of the metallic conductor?'),
      [C('any appropriate heat source', 6, note_sel=PA(3))], 'phys-u2', 'varying-the-temperature',
      SQ(10, 'How did the student vary the temperature of the metallic conductor?'), 6, stem=STEM5,
      id='phys-2024-ol-q5-ii'),
    T('5iii', 'Q5(iii)', 'A', P(4, 'State one safety precaution that the student should have taken.'),
      [C('any safety precaution', 4, note_sel=PA(2))], 'phys-u2', 'safety-precaution',
      SQ(10, 'State one safety precaution that the student should have taken.'), 4, stem=STEM5,
      id='phys-2024-ol-q5-iii'),
    T('5iv', 'Q5(iv)', 'A', P(4, 'Use the data to plot a graph to show the relationship between T and R.'),
      [C('labelled axis', 3), C('points plotted', 6, units=[1] * 6, note=CRIT + ' It prices them [6×1].'),
       C('line of best fit', 3)], 'phys-u2', 'resistance-temperature-graph',
      SQ(10, 'Use the data to plot a graph to show the relationship between T and R.'), 12, stem=STEM5 + [DATA5],
      fig='q5-table', id='phys-2024-ol-q5-iv'),
    T('5v', 'Q5(v)', 'A', P(4, 'Describe the relationship between T and R.'),
      [R('resistance increases with temperature', 3)], 'phys-3-3', 'resistance-temperature-relationship',
      SQ(10, 'Describe the relationship between T and R.'), 3, stem=STEM5 + [DATA5], fig='q5-table',
      id='phys-2024-ol-q5-v'),
    T('5vi', 'Q5(vi)', 'A', P(4, 'Use your graph to estimate the temperature of the unknown liquid.'),
      [R('14.4 ℃', 3)], 'phys-3-3', 'temperature-of-unknown-liquid',
      SQ(10, 'Use your graph to estimate the temperature of the unknown liquid.'), 3, stem=STEM5 + [DATA5, LIQUID],
      fig='q5-table', id='phys-2024-ol-q5-vi'),
    # ============================================================ Section B ==
    # ---- Q6 short questions: best eight of twelve at 7 --------------------------
    T('6a', 'Q6(a)', 'B', P(5, 'State the principle of conservation of momentum.'),
      [R('(in a closed system, the total) momentum before (interaction) = (the total)', 7,
         end='m₁u₁ + m₂u₂ = m₁v₁ + m₂v₂', note_sel=S('[accept partial answer for 4 e.g. p=mv]'))],
      'phys-1-2', 'conservation-of-momentum', SQ(11, 'State the principle of conservation of momentum.'), 7,
      id='phys-2024-ol-q6-a'),
    T('6b', 'Q6(b)', 'B', P(5, 'What is the difference between a scalar quantity', 'and a vector quantity?'),
      [R('a scalar quantity has magnitude only / a vector quantity has magnitude and direction', 7, note_sel=PA(4))],
      'phys-1-1', 'scalars-and-vectors',
      SQ(11, 'What is the difference between a scalar quantity and a vector quantity?'), 7, id='phys-2024-ol-q6-b'),
    T('6c', 'Q6(c)', 'B', [P(5, 'Explain Archimedes’ principle.'), P(5, 'The diagram on the right may help your answer.')],
      [R('upthrust = weight of the fluid displaced / upthrust 5 – 3 = 2 N, weight of fluid = 2 N', 7, note_sel=PA(4))],
      'phys-1-2', 'archimedes-principle', SQ(11, 'Explain Archimedes’ principle.'), 7, fig='q6c-diagram',
      id='phys-2024-ol-q6-c-fig',
      decision='Q6(c) was carded twice, with and without the diagram; this id carries the reviewed task and '
               'phys-2024-ol-q6-c is withdrawn onto it.'),
    T('6d', 'Q6(d)', 'B', P(5, 'Describe an experiment to compare the rates of', 'different solids.'),
      [C('apparatus', 3), C('method', 2), C('observation', 2)], 'phys-2-1', 'comparing-conduction',
      SQ(11, 'Describe an experiment to compare the rates of conduction of heat through solids.'), 7,
      decision='The bank had excluded this part. The scheme prices "apparatus method observation [3+2+2]" and names '
               'only what earns the marks: three criterion rows, in the order printed.'),
    T('6e', 'Q6(e)', 'B', P(5, 'State one difference between light waves and sound waves.'),
      [R('e.g. light waves do not need a medium to travel through / sound waves need a', 7,
         end='medium to travel through, etc.', note_sel=PA(4))], 'phys-2-2', 'light-and-sound-waves',
      SQ(11, 'State one difference between light waves and sound waves.'), 7, id='phys-2024-ol-q6-e'),
    T('6f', 'Q6(f)', 'B', [P(5, 'The Doppler effect is used in a radar system to detect the speed of cars.', 'Doppler effect?'),
                           P(5, 'A labelled diagram may help you answer.')],
      [R('(apparent) change in frequency due to the movement of the source/observer', 7, note_sel=PA(4))],
      'phys-2-7', 'doppler-effect',
      SQ(11, 'The Doppler effect is used in a radar system to detect the speed of cars. What is the'), 7,
      id='phys-2024-ol-q6-f'),
    T('6g', 'Q6(g)', 'B', P(5, 'The solar constant (solar irradiance) is a measure of how much radiation from the Sun',
                            'on an area of 72 m².'),
      [R('1360 × 72 = 97920 W', 7, note_sel=PA(4))], 'phys-2-4', 'solar-energy-per-second',
      SQ(12, 'The solar constant (solar irradiance) is a measure of how much radiation from the Sun'), 7,
      id='phys-2024-ol-q6-g',
      decision='The scheme\'s reprint says "the Earth\'s surface" and "a 72 m² garden" where the paper prints '
               '"the Earth\'s atmosphere" and "an area of 72 m²": the paper\'s wording is the question.'),
    T('6h', 'Q6(h)', 'B', P(5, 'What is meant by capacitance?'),
      [FR(12, (110, 172, 150, 199), 'C= Q/V', 7, note_sel=PA(4))], 'phys-3-2', 'capacitance',
      SQ(12, 'What is meant by capacitance?'), 7,
      decision='The bank had left this part open: the scheme\'s answer is a formula set as a stacked fraction, read '
               'from where it is printed.'),
    T('6i', 'Q6(i)', 'B', P(5, 'State a safety precaution that should be taken when working with radioactive', 'materials.'),
      [R('e.g. use appropriate shielding for the type of radiation, distance yourself', 7,
         end='wear protective clothing, etc.', note_sel=PA(4))], 'phys-4-4', 'radiation-safety',
      SQ(12, 'State a safety precaution that should be taken when working with radioactive'), 7,
      id='phys-2024-ol-q6-i'),
    T('6j', 'Q6(j)', 'B', P(5, 'The critical angle of diamond is 24.4°. Calculate n, the refractive index of the diamond.'),
      [R('n = 2.42', 7, note_sel=PA(4))], 'phys-2-3', 'refractive-index-of-diamond',
      SQ(12, 'The critical angle of diamond is 24.4°. Calculate n, the refractive index of the diamond.'), 7,
      id='phys-2024-ol-q6-j'),
    T('6k', 'Q6(k)', 'B', P(5, 'Name one part of the eye. Explain its function.'),
      [C('named part of the eye', 4), C('function', 3)], 'phys-2-3', 'part-of-the-eye',
      SQ(12, 'Name one part of the eye. Explain its function.'), 7,
      decision='The bank had excluded this part. The scheme prices "named part of the eye function [4+3]" and names '
               'none: two criterion rows, in the order printed.'),
    T('6l', 'Q6(l)', 'B', P(5, 'Draw the magnetic field around a bar magnet.'),
      [C('shape', 4), C('direction', 3)], 'phys-3-4', 'field-of-bar-magnet',
      SQ(12, 'Draw the magnetic field of a bar magnet.'), 7,
      decision='The bank had excluded this part. The scheme prices "shape direction [4+3]": two criterion rows, in '
               'the order printed.'),
    # ---- Q7 the deadlift and the bus pull ------------------------------------------
    T('7i', 'Q7(i)', 'B', P(6, 'Explain the difference between mass and weight.'),
      [R('e.g. mass is measure in kg / weight is measure in N, etc.', 6, kind='point', note_sel=PA(3))], 'phys-1-5',
      'mass-and-weight', SQ(13, 'Explain the difference between mass and weight.'), 6, stem=STEM7,
      id='phys-2024-ol-q7-i'),
    T('7ii', 'Q7(ii)', 'B', Q7II,
      [R('F = 537.5 × 9.8 = 5267.5 N', 6, note_sel=S('[accept partial answer for 3, e.g. F = ma]'))], 'phys-1-5',
      'weight-of-mass', SQ(13, 'Calculate the weight of a 537.5 kg mass.'), 6, stem=STEM7 + [G7],
      id='phys-2024-ol-q7-ii'),
    T('7iii', 'Q7(iii)', 'B', P(6, 'Calculate the work done in lifting this weight from the ground', 'to a height of 46 cm.'),
      [R('W = 5267.5 × 0.46 = 2423.05 J', 6, note_sel=S('[accept partial answer for 3, e.g. W = Fs]'))], 'phys-1-4',
      'work-done-lifting',
      SQ(13, 'Calculate the work done in lifting a mass of 537.5 kg from the ground to the required'), 6,
      stem=STEM7 + [M('(ii)', 6), Q7II, G7], id='phys-2024-ol-q7-iii'),
    T('7iv', 'Q7(iv)', 'B', P(6, 'Draw a diagram of the forces acting on the bar when it is held at a height of 46 cm.'),
      [C('arrow up', 4), C('arrow down', 4), C('same length', 1)], 'phys-1-2', 'forces-on-the-bar',
      SQ(13, 'Draw a diagram of the forces acting on the bar when it is at a height of 46 cm.'), 9, stem=[DEADLIFT],
      id='phys-2024-ol-q7-iv', decision='[4+4+1] against the three lines: in the order printed.'),
    T('7v', 'Q7(v)', 'B', P(6, 'Momentum is important when moving the bus. What is meant by momentum?'),
      [R('mass × velocity / mv', 6, note_sel=PA(3))], 'phys-1-2', 'momentum',
      SQ(13, 'Momentum is important when moving the bus. What is meant by momentum?'), 6, stem=[BUS],
      id='phys-2024-ol-q7-v'),
    T('7vi', 'Q7(vi)', 'B', P(6, 'Calculate the momentum of the bus when its speed is 0.6 m s⁻¹.', 'Include units in your answer.'),
      [R('19000 × 0.6 = 11 400', 4, note_sel=PA(2)), R('kg ms⁻¹', 2)], 'phys-1-2', 'momentum-of-bus',
      SQ(13, 'Calculate the momentum of the bus at a speed of 0.6 m s⁻¹. Include units in your'), 6, stem=[BUS],
      id='phys-2024-ol-q7-vi'),
    T('7vii', 'Q7(vii)', 'B', P(6, 'Suggest a reason that the bus rolled to a stop.'),
      [R('friction', 5, note_sel=PA(3))], 'phys-1-2', 'why-the-bus-stopped',
      SQ(13, 'Suggest a reason that the bus rolled to a stop.'), 5, stem=[COURSE], id='phys-2024-ol-q7-vii'),
    T('7viii', 'Q7(viii)', 'B', P(6, 'Draw a velocity–time graph for the motion of the bus during the 52 s.'),
      [C('labelled axis', 3), C('acceleration shown', 3), C('constant velocity shown', 3), C('deceleration shown', 3)],
      'phys-1-1', 'velocity-time-graph-of-bus',
      SQ(13, 'Draw a velocity-time graph for the motion of the bus during the 52 s.'), 12, stem=[COURSE],
      fig='q7viii-scheme', id='phys-2024-ol-q7-viii',
      decision='The scheme draws the graph beside its four criteria: the drawing is the solution figure.'),
    # ---- Q8 reflection ----------------------------------------------------------------
    T('8i', 'Q8(i)', 'B', P(7, 'Explain what is meant by an image.'),
      [R('intersection of rays', 6, note_sel=PA(3))], 'phys-2-3', 'image', SQ(14, 'Explain what is meant by an image.'),
      6, stem=STEM8, fig='q8-plane-mirror', id='phys-2024-ol-q8-i'),
    T('8ii', 'Q8(ii)', 'B', P(7, 'State one property of the image produced by a', 'plane mirror.'),
      [R('e.g. same size, lateral inversion, etc.', 6, note_sel=PA(3))], 'phys-2-3', 'plane-mirror-image',
      SQ(14, 'State one property of the image produced by a plane mirror.'), 6, stem=STEM8, fig='q8-plane-mirror',
      id='phys-2024-ol-q8-ii'),
    T('8iii', 'Q8(iii)', 'B', P(7, 'State one use of a plane mirror.'),
      [R('e.g. to see yourself, etc.', 3)], 'phys-2-3', 'use-of-plane-mirror', SQ(14, 'State one use of a plane mirror.'),
      3, stem=STEM8, fig='q8-plane-mirror', id='phys-2024-ol-q8-iii'),
    T('8iv', 'Q8(iv)', 'B', P(7, 'Describe an experiment to demonstrate this law of reflection.'),
      [C('apparatus', 4), C('method', 4), C('observation', 4, note_sel=EACH)], 'phys-2-3',
      'law-of-reflection-experiment', SQ(14, 'Describe an experiment to show this law of reflection.'), 12,
      stem=[LAW8],
      decision='The bank had excluded this part. The scheme prices "apparatus [4] method [4] observation [4]" and '
               'names only what earns the marks: three criterion rows.'),
    T('8v', 'Q8(v)', 'B', P(7, 'In your answerbook, copy and complete the ray diagram below to show how a',
                            'magnified image is formed in a concave mirror.'),
      [C('first incident ray', 3), C('first reflected ray', 3), C('second reflected ray', 3), C('image formed', 2)],
      'phys-2-3', 'concave-mirror-ray-diagram',
      SQ(14, 'In your answerbook, copy and complete the ray diagram below to show how a'), 11, stem=[CURVED],
      fig='q8-ray-diagram', id='phys-2024-ol-q8-v'),
    T('8vi', 'Q8(vi)', 'B', P(7, 'Explain why the image of person A in', 'is upside down.'),
      [R('person A is upright because they are inside the focal point of the mirror /', 6,
         end='outside the focal point of the mirror', note_sel=PA(3))], 'phys-2-3', 'upright-and-inverted-images',
      SQ(14, 'Explain why the image of person A in the picture is upright but the image of person B is'), 6,
      stem=[PICTURE], fig='q8-concave-photo', id='phys-2024-ol-q8-vi-fig'),
    T('8vii', 'Q8(vii)', 'B', Q8VII,
      [FR(14, (110, 640, 200, 668), 'm = 40/20 = 2 cm', 6, note_sel=PA(3))], 'phys-2-3', 'magnification',
      SQ(14, 'Calculate the magnification m of this image.'), 6, stem=[MAG], id='phys-2024-ol-q8-vii',
      decision='The scheme gives the magnification a unit, "= 2 cm"; it is lifted as printed.'),
    T('8viii', 'Q8(viii)', 'B', P(7, 'If the object is 5 cm high, calculate the height of the image.'),
      [R('5 × 2 = 10 cm', 6, note_sel=PA(3))], 'phys-2-3', 'height-of-image',
      SQ(14, 'If the object is 5 cm high, calculate the height of the image.'), 6, stem=[MAG, M('(vii)', 7), Q8VII],
      id='phys-2024-ol-q8-viii'),
    # ---- Q9 latent heat and the heat pump ---------------------------------------------
    T('9i', 'Q9(i)', 'B', P(8, 'What is meant by latent heat?'),
      [R('heat energy needed to change state', 6, note_sel=PA(3))], 'phys-2-1', 'latent-heat',
      SQ(15, 'What is meant by latent heat?'), 6, stem=STEM9A, id='phys-2024-ol-q9-i'),
    T('9ii', 'Q9(ii)', 'B', P(8, 'Explain why the graph flattens out at A.'),
      [R('changing state / no temperature change', 6, note_sel=PA(3))], 'phys-2-1', 'why-the-graph-flattens',
      SQ(15, 'Explain why the graph flattens out at A.'), 6, stem=STEM9, fig='q9-graph',
      decision='The bank had left this part open: it is carded with the printed graph.'),
    T('9iii', 'Q9(iii)', 'B', P(8, 'The specific latent heat of vaporisation of the refrigerant is 141 100 J kg⁻¹.',
                                'from liquid to gas.'),
      [R('∆E= 0.3 × 141 100 = 42 330 J', 6, note_sel=S('[accept partial answer for 3 e.g. ∆E=ml]'))], 'phys-2-1',
      'heat-to-vaporise-refrigerant',
      SQ(15, 'The specific latent heat of vaporisation of the refrigerant is 141 100 J kg⁻¹. Calculate'), 6,
      stem=STEM9A, id='phys-2024-ol-q9-iii'),
    T('9iv', 'Q9(iv)', 'B', P(8, 'What happens to the temperature inside a freezer when the liquid changes state to',
                              'become a gas?'),
      [R('it decreases', 6)], 'phys-2-1', 'freezer-temperature',
      SQ(15, 'What happens to the temperature inside the fridge when the liquid changes state to'), 6, stem=STEM9A,
      id='phys-2024-ol-q9-iv'),
    T('9v', 'Q9(v)', 'B', P(8, 'According to the graph, what temperature does this happen at?'),
      [R('65 ℃', 3)], 'phys-2-1', 'condensing-temperature-from-graph',
      SQ(15, 'According to the graph, what temperature does this happen at?'), 3, stem=STEM9 + [BACK], fig='q9-graph',
      decision='The bank had left this part open: it is carded with the printed graph.'),
    T('9vi', 'Q9(vi)', 'B', P(8, 'What is the process called when a gas changes into a liquid?'),
      [R('condensation', 6, note_sel=PA(3))], 'phys-2-1', 'condensation',
      SQ(15, 'What is the process called when a gas changes into a liquid?'), 6, stem=[BACK], id='phys-2024-ol-q9-vi'),
    T('9vii', 'Q9(vii)', 'B', P(8, 'Draw a labelled diagram of a heat pump.'),
      [C('closed system', 3), C('circulating fluid', 3), C('compressor/expansion valve', 3, note_sel=NOLABEL)],
      'phys-2-1', 'heat-pump-diagram', SQ(15, 'Draw a labelled diagram of a heat pump.'), 9, stem=STEM9A,
      id='phys-2024-ol-q9-vii'),
    T('9viii', 'Q9(viii)', 'B', P(8, 'Different thermometers are based on different thermometric properties.',
                                  'meant by a thermometric property?'),
      [R('property that changes (measurably) with temperature', 6, note_sel=PA(3))], 'phys-2-1',
      'thermometric-property', SQ(15, 'What is meant by a thermometric property?'), 6, stem=[THERMO],
      id='phys-2024-ol-q9-viii'),
    T('9ix', 'Q9(ix)', 'B', P(8, 'What is the thermometric property of an alcohol-in-glass thermometer?'),
      [R('length', 4, note_sel=PA(2))], 'phys-2-1', 'alcohol-thermometer-property',
      SQ(15, 'What is the thermometric property of an alcohol-in-glass thermometer?'), 4, id='phys-2024-ol-q9-ix'),
    T('9x', 'Q9(x)', 'B', P(8, 'State one everyday use of a thermometer.'),
      [R('e.g. body temperature, cooking, etc.', 4, note_sel=PA(2))], 'phys-2-1', 'everyday-use-of-thermometer',
      SQ(15, 'State one everyday use of a thermometer.'), 4, id='phys-2024-ol-q9-x'),
    # ---- Q10 resonance and pipes -----------------------------------------------------
    T('10i', 'Q10(i)', 'B', P(9, 'What is meant by resonance?'),
      [R('transfer of energy between bodies at the same frequency', 6, note_sel=PA(3))], 'phys-2-5', 'resonance',
      SQ(16, 'What is meant by resonance?'), 6, stem=STEM10, id='phys-2024-ol-q10-i'),
    T('10ii', 'Q10(ii)', 'B', P(9, 'Describe a laboratory experiment to demonstrate resonance.'),
      [C('apparatus', 4), C('method', 4), C('observation', 4, note_sel=EACH)], 'phys-2-5', 'resonance-experiment',
      SQ(16, 'Describe a laboratory experiment to demonstrate resonance.'), 12, stem=STEM10,
      decision='The bank had excluded this part. The scheme prices "apparatus [4] method [4] observation [4]" and '
               'names only what earns the marks: three criterion rows.'),
    T('10iii', 'Q10(iii)', 'B', P(9, 'The diagram on the right shows a sound wave vibrating at its', 'labelled X and Y.'),
      [R('X = antinode', 3), R('Y = node', 3, note_sel=PA(3))], 'phys-2-6', 'node-and-antinode',
      SQ(16, 'The diagram on the right shows the fundamental frequency in a pipe'), 6, stem=[CLARINET],
      fig='q10-pipe', labels=[L('X', S('X = antinode', piece=2, psep=' = ', page=16), True),
                              L('Y', S('Y = node', piece=2, psep=' = ', page=16), True)],
      decision='The bank had left this part open: it is carded with the printed pipe and its letters.'),
    T('10iv', 'Q10(iv)', 'B', P(9, 'Draw a diagram, in your answerbook, to show the next harmonic for',
                                'a sound wave in the same pipe.'),
      [C('node at closed end and two antinodes', 6, note=DRAWN, note_sel=PA(3))], 'phys-2-6', 'next-harmonic',
      SQ(16, 'Draw a diagram, in your answerbook, to show the next harmonic for a'), 6, stem=[CLARINET],
      fig='q10-pipe', id='phys-2024-ol-q10-iv'),
    T('10v', 'Q10(v)', 'B', P(9, 'The speed of sound in air c is 336 m s⁻¹ and the frequency f of the',
                              'Calculate the wavelength λ of the sound wave.'),
      [FR(16, (110, 390, 205, 417), 'λ= 336/320 =1.05 m', 6,
          note_sel=S('[accept partial answer for 3 e.g. c =fλ]'))], 'phys-2-5', 'wavelength-of-sound',
      SQ(16, 'The speed of sound in air c is 336 m s⁻¹ and frequency f of the wave is 320 Hz.'), 6, stem=[CLARINET],
      id='phys-2024-ol-q10-v'),
    T('10vi', 'Q10(vi)', 'B', P(9, 'The distance from X to Y is taken as', 'Calculate the length of the pipe.'),
      [FR(16, (110, 446, 220, 473), 'l= 1.05/4 = 0.2625 m', 3)], 'phys-2-6', 'length-of-pipe',
      SQ(16, 'If the distance from X to Y is taken as'), 3, stem=[CLARINET], qfig='q10vi-question', fig='q10-pipe',
      decision='The bank had left this part open. The paper sets λ/4 as a stacked fraction the text layer cannot '
               'order: the ask is shown as printed, with the pipe as the figure.'),
    T('10vii', 'Q10(vii)', 'B', P(9, 'What property of the wave needs to change to affect the pitch of the note?'),
      [R('frequency', 6, note_sel=PA(3))], 'phys-2-5', 'pitch-and-frequency',
      SQ(16, 'What property of the wave needs to change to affect the pitch of the note played by'), 6,
      stem=[CLARINET, AMPL], id='phys-2024-ol-q10-vii'),
    T('10viii', 'Q10(viii)', 'B', P(9, 'Draw a diagram to show a sound wave vibrating at', 'ends.'),
      [C('antinode at both ends with one node at the centre', 6, note=DRAWN, note_sel=PA(3))], 'phys-2-6',
      'pipe-open-at-both-ends',
      SQ(16, 'Draw a labelled diagram to show the fundamental frequency for a sound wave in a'), 6, stem=[FLUTE],
      id='phys-2024-ol-q10-viii'),
    T('10ix', 'Q10(ix)', 'B', P(9, 'A sound wave vibrates at its fundamental frequency', 'wave.'),
      [R('λ= 1.2 m', 5, note_sel=PA(3))], 'phys-2-6', 'wavelength-in-open-pipe',
      SQ(16, 'A sound wave vibrates at its fundamental frequency in a pipe of length 60 cm which is'), 5,
      stem=[FLUTE], id='phys-2024-ol-q10-ix'),
    # ---- Q11 electricity in the home, Ohm's law ----------------------------------------
    T('11i', 'Q11(i)', 'B', P(10, 'State an example of an electrical', 'conductor.'),
      [C('any named conductor', 5)], 'phys-3-3', 'electrical-conductor',
      SQ(17, 'Give an example of an electrical conductor'), 5, stem=STEM11, id='phys-2024-ol-q11-i'),
    T('11ii', 'Q11(ii)', 'B', P(10, 'Name an instrument used to measure', 'electric current.'),
      [R('ammeter/galvanometer', 6, note_sel=PA(3))], 'phys-3-3', 'measuring-current',
      SQ(17, 'Name an instrument used to measure electric current.'), 6, stem=STEM11, id='phys-2024-ol-q11-ii'),
    T('11iii', 'Q11(iii)', 'B', P(10, 'The diagram on the right shows the parts', 'labelled A and B.'),
      [R('A = earth wire', 3), R('B = live wire', 3, note_sel=PA(3))], 'phys-3-3', 'wires-in-a-plug',
      SQ(17, 'The diagram on the right shows the parts of an electrical plug. Name the wires'), 6,
      fig='q11-plug', labels=[L('A', S('A = earth wire', piece=2, psep=' = ', page=17), True),
                              L('B', S('B = live wire', piece=2, psep=' = ', page=17), True)],
      id='phys-2024-ol-q11-iii-fig'),
    T('11iv', 'Q11(iv)', 'B', P(10, 'Describe how a fuse works.'),
      [R('melts/breaks if current is too high', 6, note_sel=PA(3))], 'phys-3-3', 'how-a-fuse-works',
      SQ(17, 'Describe how a fuse works.'), 6, stem=[FUSE], id='phys-2024-ol-q11-iv'),
    T('11v', 'Q11(v)', 'B', P(10, 'What is an advantage of using a MCB instead of a fuse in a domestic circuit?'),
      [pt(S('e.g. more sensitive to current than a fuse, can be reset rather than replaced, etc. [6]',
            piece=1, psep=' ['), 6, note_sel=PA(3))], 'phys-3-3', 'mcb-advantage',
      SQ(17, 'What is the advantage of using a MCB instead of a fuse in a domestic circuit?'), 6, stem=[MCB],
      id='phys-2024-ol-q11-v',
      decision='The scheme prints this line\'s [6] inside the line\'s own text (p17, rendered and looked at): the row '
               'is cut at it, and the 6 is the printed cell.'),
    T('11vi', 'Q11(vi)', 'B', P(10, 'Name another safety feature used in domestic circuits.'),
      [R('e.g. earthing, bonding, RCD, etc.', 3)], 'phys-3-3', 'domestic-safety-feature',
      SQ(17, 'Name another safety feature used in domestic cicruits.'), 3, stem=[MCB], id='phys-2024-ol-q11-vi'),
    T('11viia', 'Q11(vii)(a)', 'B', Q11VIIA,
      [R('X as it is wired in parallel', 6, note_sel=PA(3))], 'phys-3-3', 'which-is-the-voltmeter',
      SQ(17, 'Which of the devices, X or Y is a voltmeter?'), 6, stem=[OHM], fig='q11-circuit',
      decision='The scheme prices (a) [6] and (b) [3] apart: one card each. The old cards carded (b) alone.'),
    T('11viib', 'Q11(vii)(b)', 'B', [M('(b)', 10), P(10, 'The electrical component Z is a', 'law.')],
      [R('to adjust the voltage/current in the circuit', 3)], 'phys-3-3', 'why-a-variable-resistor',
      SQ(17, 'The electrical component Z is a variable resistor.'), 3, stem=[OHM], fig='q11-circuit',
      id='phys-2024-ol-q11-viib'),
    T('11viii', 'Q11(viii)', 'B', P(10, 'Verify that the resistance is 2.5 Ω by calculating the resistance R when the voltage V is',
                                    '2 V and the current I is 0.8 A.'),
      [FR(17, (110, 607, 200, 634), 'R= 2/0.8 = 2.5 Ω', 6, note_sel=S('[accept partial answer for 3 e.g. V=IR]'))],
      'phys-3-3', 'verifying-resistance',
      SQ(17, 'Verfy that the resistance is 2.5 Ω by calculating the resistance when the voltage'), 6, stem=[PREV],
      decision='The bank had left this part open: the answer is a stacked fraction, read from where it is printed.'),
    T('11ix', 'Q11(ix)', 'B', P(10, 'The resistance of the coil of wire is 2.5 Ω and the resistance of device X is 20 000 Ω.',
                                'parallel combination.'),
      [FR(17, (110, 680, 182, 708), '1/(RT) = 1/R₁ + 1/R₂', 3),
       FR(17, (110, 706, 200, 733), '1/(RT) = 1/2.5 + 1/(20 000)', 3),
       R('RT = 2.5 Ω', 3, note_sel=S('[accept partial answer for 3 e.g. RT=R₁+R₂]'))], 'phys-3-3',
      'parallel-resistance',
      SQ(17, 'The resistance of the coil of wire as 2.5 Ω and the resistance of device X is'), 9, fig='q11-circuit',
      decision='The bank had left this part open: the two formulas are stacked fractions, read from where they are '
               'printed.'),
    # ---- Q12 nuclear fission and fusion ------------------------------------------------
    T('12i', 'Q12(i)', 'B', P(11, 'What is meant by nuclear fission?'),
      [R('the splitting of a nucleus', 6, note_sel=PA(3))], 'phys-4-6', 'nuclear-fission',
      SQ(18, 'What is meant by nuclear fission?'), 6, id='phys-2024-ol-q12-i'),
    T('12ii', 'Q12(ii)', 'B', [P(11, 'Explain the function of'), M('(a)', 11), P(11, 'the control rods,'), M('(b)', 11),
                               P(11, 'the moderator.')],
      [R('absorbs neutrons', 6, label=S('(a) the control rods')),
       R('slows down neutrons', 3, label=S('(b) the moderator'), note_sel=PA(3))],
      'phys-4-6', 'control-rods-and-moderator', SQ(18, 'Explain the function of'), 9, stem=[RODS],
      id='phys-2024-ol-q12-ii',
      decision='One cell [6+3] prices (a) and (b) together: one card, (a) 6 and (b) 3 in the order printed.'),
    T('12iii', 'Q12(iii)', 'B', P(11, 'The fission reactor must also have a shield.', 'shield?'),
      [R('e.g. lead, etc.', 3)], 'phys-4-6', 'reactor-shield',
      SQ(18, 'The fission reactor must also have a shield. What material could be used to make the'), 3,
      id='phys-2024-ol-q12-iii'),
    T('12iv', 'Q12(iv)', 'B', P(11, 'What are isotopes?'),
      [R('atoms of the same element with different number of neutrons', 6, note_sel=PA(3))], 'phys-4-3', 'isotopes',
      SQ(18, 'What are isotopes?'), 6, stem=[FUELS], id='phys-2024-ol-q12-iv'),
    T('12v', 'Q12(v)', 'B', P(11, 'What fraction of the isotope will remain after 72 330 years?'),
      [FR(18, (110, 434, 125, 460), '1/8', 6, note_sel=PA(3))], 'phys-4-4', 'fraction-remaining',
      SQ(18, 'What fraction of the isotope will remain after 72 330 years?'), 6, stem=[PU], id='phys-2024-ol-q12-v'),
    T('12vi', 'Q12(vi)', 'B', P(11, 'When Pu–239 decays, it emits alpha particles', '?'),
      [G('equation', page=18, clip=(110, 508, 145, 530), expect='U²³⁵₉₂', marks=6, units=[2, 2, 2],
         note='[3 × 2]: the scheme prices the nucleus in three items, 2 each.')],
      'phys-4-4', 'daughter-nucleus-of-plutonium',
      SQ(18, 'When Pu-239 decays, it emits alpha particles'), 6, stem=[PU], qfig='q12vi-question',
      fig='q12vi-scheme', id='phys-2024-ol-q12-vi',
      decision='The paper prints the nuclides with their numbers stacked, which the text layer cannot order: the ask '
               'is shown as printed. The scheme\'s nucleus is read from glyph positions and shown as a crop.'),
    T('12vii', 'Q12(vii)', 'B', P(11, 'Draw a diagram of an atom and indicate where the neutrons are located.'),
      [C('diagram of atom indicating neutrons in the nucleus', 6, note=DRAWN, note_sel=PA(3))], 'phys-4-3',
      'atom-diagram', SQ(18, 'Draw a diagram of an atom and indicate where the neutrons are located.'), 6,
      stem=[NEUTRONS], id='phys-2024-ol-q12-vii'),
    T('12viii', 'Q12(viii)', 'B', P(11, 'Name another sub-atomic particle.'),
      [R('e.g. proton, electron, etc.', 6, note_sel=PA(3))], 'phys-4-3', 'sub-atomic-particle',
      SQ(18, 'Name another sub-atomic particle.'), 6, stem=[NEUTRONS], id='phys-2024-ol-q12-viii'),
    T('12ix', 'Q12(ix)', 'B', P(11, 'What is meant by nuclear fusion?'),
      [R('joining of two nuclei', 4, note_sel=PA(2))], 'phys-4-6', 'nuclear-fusion',
      SQ(18, 'What is meant by nuclear fusion?'), 4, stem=[FUSION], id='phys-2024-ol-q12-ix'),
    T('12x', 'Q12(x)', 'B', P(11, 'State one advantage of a nuclear fusion reactor over a nuclear fission reactor.'),
      [R('e.g. less radioactive waste, etc.', 4, note_sel=PA(2))], 'phys-4-6', 'fusion-advantage',
      SQ(18, 'Give one advantage of a nuclear fusion reactor over a nuclear fission reactor.'), 4, stem=[FUSION],
      id='phys-2024-ol-q12-x'),
    # ---- Q13 the International Space Station ----------------------------------------
    T('13a', 'Q13(a)', 'B', P(12, 'How high above the Earth is the ISS?'),
      [R('322 km', 7)], 'phys-1-5', 'height-of-iss', SQ(19, 'How high above the Earth is the ISS?'), 7, stem=PASSAGE,
      id='phys-2024-ol-q13a'),
    T('13b', 'Q13(b)', 'B', P(12, 'How many full orbits of the Earth does the ISS make in 24 hours?'),
      [R('16 full orbits', 7, note_sel=PA(4))], 'phys-1-5', 'orbits-per-day',
      SQ(19, 'How many full orbits of the Earth does the ISS make in 24 hours?'), 7, stem=PASSAGE,
      id='phys-2024-ol-q13-b'),
    T('13c', 'Q13(c)', 'B', P(12, 'Describe how acceleration due to gravity changes as the distance from the centre of',
                              'the Earth increases.'),
      [R('it decreases', 7)], 'phys-1-5', 'gravity-and-distance',
      SQ(19, 'Describe how acceleration due to gravity changes as the distance from the centre of'), 7,
      id='phys-2024-ol-q13-c'),
    T('13d', 'Q13(d)', 'B', [P(12, 'A CT scanner uses X-rays to produce images of the inside of the body.'),
                             P(12, 'What are X-rays?')],
      [R('high energy waves / electromagnetic radiation', 7, note_sel=PA(4))], 'phys-4-2', 'x-rays',
      SQ(19, 'A CT scanner uses x-rays to produce images of the inside of the body. What are'), 7,
      id='phys-2024-ol-q13-d'),
    T('13e', 'Q13(e)', 'B', P(12, 'Draw a labelled diagram of an X-ray tube.'),
      [C('heating filament', 3), C('cathode and anode target / high voltage', 2),
       C('shielding / glass tube', 2, note_sel=NOLABEL_IS)], 'phys-4-2', 'x-ray-tube',
      SQ(19, 'Draw a labelled diagram of the x-ray tube.'), 7, id='phys-2024-ol-q13e',
      decision='[3+2+2] against the three lines: in the order printed.'),
    T('13f', 'Q13(f)', 'B', P(12, 'The bone density of an astronaut was 1.39 g cm⁻³ before leaving Earth.',
                              'Calculate the total mass of her bones at that time.'),
      [R('m = 1.39 × 7140 = 9924.6 g', 7, note_sel=S('[accept partial answer for 4 e.g. ρ=', piece=1, psep=' e.g.'))],
      'phys-1-2', 'mass-of-bones',
      SQ(19, 'The bone density of an astronaut was 1.39 g cm⁻³ before leaving Earth. The total'), 7,
      id='phys-2024-ol-q13-f',
      decision='The scheme\'s partial allowance closes with an example formula set as a stacked fraction ("e.g. '
               'ρ = m/V"), which the text layer cannot order: the note keeps the allowance and is cut before the '
               'example.'),
    T('13g', 'Q13(g)', 'B', P(12, 'The temperature outside the ISS is 116 K. Convert this temperature to Celsius (°C).'),
      [R('116 – 273.15 = –157.15 ℃', 7, note_sel=PA(4))], 'phys-2-1', 'kelvin-to-celsius',
      SQ(19, 'The temperature outside the ISS is 116 K. Convert this temperature to Celsius (℃).'), 7,
      id='phys-2024-ol-q13-g'),
    T('13h', 'Q13(h)', 'B', P(12, 'Why do astronauts spend a lot of their time doing exercise while on the ISS?'),
      [R('to reduce loss in bone mass / due to spending time in microgravity', 7, note_sel=PA(4))], 'phys-1-5',
      'why-astronauts-exercise',
      SQ(19, 'Why do astronauts spend a lot of their time doing exercise while on the ISS?'), 7, stem=PASSAGE,
      id='phys-2024-ol-q13-h'),
    # ---- Q14 (a) Newton's laws -----------------------------------------------------------
    T('14ai', 'Q14(a)(i)', 'B', P(13, 'Calculate the net horizontal force acting on the car.'),
      [R('520 – 520 = 0 N', 4, note_sel=PA(2))], 'phys-1-2', 'net-force-balanced',
      SQ(20, 'Calculate the net horizontal force acting on the car.'), 4, stem=STEM14A, fig='q14a-balanced',
      id='phys-2024-ol-q14a-i'),
    T('14aii', 'Q14(a)(ii)', 'B', P(13, 'What is the acceleration of the car?'),
      [R('0 m s⁻²', 2)], 'phys-1-2', 'acceleration-balanced', SQ(20, 'What is the acceleration of the car?'), 2,
      stem=STEM14A, fig='q14a-balanced', id='phys-2024-ol-q14a-ii'),
    T('14aiii', 'Q14(a)(iii)', 'B', P(13, 'What is the velocity of the car 12 s later?'),
      [R('20 m s⁻¹', 2)], 'phys-1-1', 'velocity-balanced', SQ(20, 'What is the velocity of the car 12 s later?'), 2,
      stem=STEM14A, fig='q14a-balanced', id='phys-2024-ol-q14a-iii'),
    T('14aiv', 'Q14(a)(iv)', 'B', P(13, 'State Newton’s first law of motion.'),
      [R('a body remains at rest (or moving at a constant velocity) unless an (unbalanced', 5,
         end='external) force acts on it', kind='point', note_sel=PA(3))], 'phys-1-2', 'newtons-first-law',
      SQ(20, 'State Newton’s first law of motion.'), 5, stem=STEM14A[:1], id='phys-2024-ol-q14a-iv'),
    T('14av', 'Q14(a)(v)', 'B', P(13, 'Calculate the net horizontal force acting on the car.', nth=2),
      [R('680 – 520 = 160 N (right)', 5, note_sel=PA(3))], 'phys-1-2', 'net-force-unbalanced',
      SQ(20, 'Calculate the net horizontal force acting on the car.', nth=2), 5, stem=SECOND,
      fig='q14a-unbalanced', id='phys-2024-ol-q14a-v'),
    T('14avi', 'Q14(a)(vi)', 'B', P(13, 'Calculate the acceleration of the car.'),
      [FR(20, (138, 562, 262, 588), 'a= 160/1900 = 0.084 m s⁻²', 5,
          note_sel=S('[accept partial answer for 3 e.g. F=ma]'))], 'phys-1-2', 'acceleration-unbalanced',
      SQ(20, 'Calculate is the acceleration of the car.'), 5, stem=SECOND, fig='q14a-unbalanced',
      id='phys-2024-ol-q14a-vi'),
    T('14avii', 'Q14(a)(vii)', 'B', P(13, 'Calculate the velocity of the car after 12 s when the unbalanced forces are acting',
                                      'on the car.'),
      [R('v = 20 + (0.084)(12) = 21 m s⁻¹', 5, note_sel=S('[accept partial answer for 3 e.g. v=u+at]'))], 'phys-1-1',
      'velocity-unbalanced',
      SQ(20, 'Calculate the velocity of the car after 12 s when the unbalanced forces are acting'), 5, stem=SECOND,
      fig='q14a-unbalanced', id='phys-2024-ol-q14a-vii'),
    # ---- Q14 (b) the thermistor ----------------------------------------------------------
    T('14bi', 'Q14(b)(i)', 'B', P(13, 'Name an instrument used to measure resistance.'),
      [R('ohmmeter', 6, note_sel=PA(3))], 'phys-3-3', 'measuring-resistance',
      SQ(21, 'Name an instrument used to measure resistance'), 6, stem=STEM14B, id='phys-2024-ol-q14b-i'),
    T('14bii', 'Q14(b)(ii)', 'B', P(13, 'Sketch a graph to show the relationship between resistance and',
                                    'temperature for a thermistor.'),
      [C('labelled axis', 3), C('correct shape', 3)], 'phys-3-3', 'thermistor-graph',
      SQ(21, 'Sketch a graph to show the relationship between resistance and temperature for'), 6, stem=STEM14B,
      id='phys-2024-ol-q14b-ii'),
    T('14biii', 'Q14(b)(iii)', 'B', P(13, 'A thermistor is a semiconductor. What is meant by a semiconductor?'),
      [R('material with resistivity between an insulator and a conductor', 6, note_sel=PA(3))], 'phys-3-3',
      'semiconductor', SQ(21, 'A thermistor is a semiconductor. What is meant by a semiconductor?'), 6,
      stem=STEM14B, id='phys-2024-ol-q14b-iii'),
    T('14biva', 'Q14(b)(iv)(a)', 'B', [M('(a)', 13), Q14BIVA],
      [pt(S('symbol for battery/cell, symbol for bulb, symbol for semiconductor diode [3×2]', piece=[1, k],
            psep=[' [', ', ']), 2, kind='criterion', note=CRIT) for k in (1, 2, 3)]
      + [C('connected in series', 2)], 'phys-3-3', 'diode-circuit',
      SQ(21, 'Draw a circuit diagram to show a semiconductor diode connected in series'), 8, stem=[NOTE14],
      cells='The scheme prints the [3×2] for the three symbols inside the line\'s own text (p21 line 21, rendered and '
            'looked at), so the reader takes no cell from it: the printed cells are [3×2] + [2] = 8.',
      decision='The bank had left (iv) open. The scheme prices (a) and (b) apart: one card each. [3×2] against the '
               'three symbols printed on one line: 2 each.'),
    T('14bivb', 'Q14(b)(iv)(b)', 'B', [M('(b)', 13), P(13, 'Indicate if the bulb is lighting or not.')],
      [C('answer consistent with circuit drawn in (a)', 2)], 'phys-3-3', 'is-the-bulb-lit',
      SQ(21, 'Indicate if the bulb is lighting or not.'), 2, stem=[NOTE14, M('(a)', 13), Q14BIVA]),
    # ---- Q14 (c) diffraction and colour -----------------------------------------------------
    T('14ci', 'Q14(c)(i)', 'B', P(14, 'What is meant by diffraction?'),
      [R('spreading of a wave as it passes through a gap/around an object', 6, note_sel=PA(3))], 'phys-2-6',
      'diffraction', SQ(21, 'What is meant by diffraction?'), 6, stem=STEM14C, fig='q14c-grating',
      id='phys-2024-ol-q14c-i'),
    T('14cii', 'Q14(c)(ii)', 'B', [P(14, 'Constructive and destructive interference occurs to produce the interference',
                                      'pattern on the screen.'),
                                    P(14, 'Distinguish between constructive and destructive interference.')],
      [R('e.g. constructive interference: bright spots / destructive interference: dark', 6, end='spots, etc.',
         whole=True, note_sel=PA(3))], 'phys-2-6', 'constructive-and-destructive',
      SQ(21, 'Constructive and destructive interference occurs to produce the interference'), 6, stem=STEM14C,
      fig='q14c-grating', id='phys-2024-ol-q14c-ii'),
    T('14ciii', 'Q14(c)(iii)', 'B', P(14, 'Using the formula n λ = d sin θ, calculate the wavelength λ of the laser light.'),
      [R('λ=(2.5×10⁻⁶)(sin 14.6°)= 6.3×10⁻⁷m', 6, note_sel=PA(3),
         note='The scheme\'s line is shown in the figure.')], 'phys-2-6', 'wavelength-of-laser',
      SQ(21, 'Using the formula n λ = d sin θ, calculate the wavelength λ of the laser light.'), 6,
      stem=[GRATING], fig='q14ciii-scheme',
      decision='The bank had left this part open. The scheme sets the line in a maths font whose text layer puts a '
               'space after each decimal point ("2.5"); it is lifted as the text layer reads it and shown as a crop '
               'of the scheme.'),
    T('14civ', 'Q14(c)(iv)', 'B', P(14, 'Name the 3 primary colours of light.'),
      pieces(S('red, green, blue'), [2, 2, 2], ', '), 'phys-2-4', 'primary-colours',
      SQ(21, 'Name the 3 primary colours of light.'), 6, stem=[WHITE], id='phys-2024-ol-q14c-iv',
      decision='[3×2] against the three colours printed on one line: 2 each.'),
    T('14cv', 'Q14(c)(v)', 'B', P(14, 'Name a pair of complementary colours of light.'),
      [R('red and cyan / green and magenta / blue and yellow', 4, units=[2, 2],
         note='The scheme prices the pair [2+2].')], 'phys-2-4', 'complementary-colours',
      SQ(21, 'Name a pair of complementary colours of light.'), 4, stem=[WHITE], id='phys-2024-ol-q14c-v'),
    # ---- Q14 (d) static electricity ------------------------------------------------------
    T('14di', 'Q14(d)(i)', 'B', P(14, 'Describe how an object can become charged by contact.'),
      [R('(when two materials are brought into contact) electrons can transfer from one', 6, end='to the other',
         note_sel=PA(3))], 'phys-3-1', 'charging-by-contact',
      SQ(22, 'Describe how an object can become charged by contact.'), 6, stem=STEM14D, id='phys-2024-ol-q14d-i'),
    T('14dii', 'Q14(d)(ii)', 'B', P(14, 'Describe an experiment to show that opposite charges attract and', 'like charges repel.'),
      [C('apparatus', 4), C('method', 4), C('observation', 4, note_sel=EACH)], 'phys-3-1',
      'attraction-and-repulsion-experiment',
      SQ(22, 'Describe an experiment to show that opposite charges attract and like charges'), 12, stem=STEM14D,
      decision='The bank had excluded this part. The scheme prices "apparatus [4] method [4] observation [4]" and '
               'names only what earns the marks: three criterion rows.'),
    T('14diii', 'Q14(d)(iii)', 'B', P(14, 'What type of charge does an electron have?'),
      [R('negative', 3)], 'phys-3-1', 'charge-of-electron', SQ(22, 'What type of charge does an electron have?'), 3,
      stem=[GAIN], id='phys-2024-ol-q14d-iii'),
    T('14div', 'Q14(d)(iv)', 'B', P(14, 'Has a positively charged object gained or lost electrons?'),
      [R('lost electrons', 3)], 'phys-3-1', 'positive-charge',
      SQ(22, 'Has a positively charged object gained or lost electrons?'), 3, stem=[GAIN], id='phys-2024-ol-q14d-iv'),
    T('14dv', 'Q14(d)(v)', 'B', P(14, 'Draw a diagram to show how charge is distributed on a', 'pear-shaped conductor.'),
      [C('charges accumulated at the pointed end', 4, note=DRAWN, note_sel=PA(2))], 'phys-3-1',
      'charge-on-pear-shaped-conductor',
      SQ(22, 'Draw a diagram to show how charge is distributed on a pear-shaped conductor.'), 4, stem=[PEAR],
      fig='q14d-pear', id='phys-2024-ol-q14d-v'),
]

RETAINED = {
    'phys-2024-ol-q6-c': 'Never shipped: the figureless twin of phys-2024-ol-q6-c-fig, which carries the reviewed task '
                         'and the diagram.',
}
WITHDRAW = {'phys-2024-ol-q6-c': ('phys-2024-ol-q6-c-fig', RETAINED['phys-2024-ol-q6-c'])}

P7 = 'maggiesscienceconnection.weebly.com/'

FIGURES = {
    # key suffix: (doc, page, rect in PDF points, credit, letters, alt, solution[, masks])
    'q1-tables': ('paper', 2, (85, 255, 545, 334), SEC, [],
                  'Two tables of the results. Newton Spring Balances: upward forces (N) 6 and 4 at positions (cm) 20 '
                  'and 70. Weights: downward forces (N) 5 and 2 at positions (cm) 26 and 60.', False),
    'q1iii-question': ('paper', 2, (80, 373, 545, 532), SEC, [],
                       'The printed question: (iii) Copy the diagram of the metre stick below into your answerbook. '
                       'Two of the forces have been included. Complete your diagram to show all upward and downward '
                       'forces and their positions. (18) Below it, a metre stick marked from 10 cm to 90 cm, with an '
                       'upward arrow labelled 6 N at the 20 cm mark and a downward arrow labelled 3 N at the 50 cm '
                       'mark.', False),
    'q2-table': ('paper', 3, (85, 196, 545, 252), SEC, [],
                 'Table of the results: u (cm) 18, 25, 30; v (cm) 90, 38, 30.', False),
    'q3-calc': ('paper', 3, (95, 600, 545, 680), SEC, [],
                'The calculation printed for completion: Heat energy added = Heat gained by water and calorimeter; '
                'ΔE = m(water) c(water) Δθ(water) + m(calorimeter) c(copper) Δθ(calorimeter); 3467 = A × c(water) × B '
                '+ 0.106 × 390 × B.', False),
    'q4-sonometer': ('paper', 4, (222, 110, 545, 252), SEC, [],
                     'Diagram of the apparatus: a string stretched along the top of a long box over two bridges, with '
                     'a paper rider on the string between them, passing over a pulley at the right-hand end to '
                     'hanging weights.', False, [(222, 197, 448, 252)]),
    'q4-table': ('paper', 4, (85, 297, 545, 390), SEC, [],
                 'Table of the results: f (Hz) 256, 320, 341, 427, 480, 512; l (m) 0.214, 0.171, 0.160, 0.127, '
                 '0.114, 0.107; 1/l (m⁻¹) 4.67, 5.85, and four empty cells.', False),
    'q4v-question': ('paper', 4, (80, 391, 520, 430), SEC, [],
                     'The printed question: (v) Copy and complete the table above into your answerbook by '
                     'calculating the value of 1/l to 2 decimal places.', False),
    'q4vi-question': ('paper', 4, (80, 428, 520, 453), SEC, [],
                      'The printed question: (vi) Use the data to plot a graph of 1/l against f.', False),
    'q5-table': ('paper', 4, (85, 585, 545, 625), SEC, [],
                 'Table of the data: T (°C) 10, 20, 30, 40, 50, 60; R (Ω) 5.2, 5.9, 6.5, 7.2, 7.9, 8.5.', False),
    'q6c-diagram': ('paper', 5, (372, 188, 542, 302), 'www.britannica.com/science/', [],
                    'Diagram: a spring balance reading 5 N holds a weight above a container of water; beside it, a '
                    'balance reading 3 N holds the same weight under the water in a full container, the overflow '
                    'running into a small dish labelled 2 N of water.', False),
    'q7viii-scheme': ('scheme', 13, (100, 665, 270, 736), SEC, [],
                      "The marking scheme's sketch: velocity against time, a straight rise from the origin, a level "
                      "section, then a steep straight fall to the time axis, then a level line along the axis.", True),
    'q8-plane-mirror': ('paper', 7, (376, 64, 545, 183), P7, [],
                        'Photograph of a small plane mirror standing upright on a sheet of paper, held by a bulldog '
                        'clip, with a word printed on the paper in front of it and the word\'s image in the mirror.',
                        False),
    'q8-ray-diagram': ('paper', 7, (84, 322, 500, 478), SEC, [],
                       'Ray diagram to copy: a principal axis drawn as a dashed line, an upright arrow labelled object '
                       'standing on the axis, a point labelled f on the axis between the object and the mirror, and a '
                       'concave mirror drawn as a curve at the right.', False),
    'q8-concave-photo': ('paper', 7, (312, 495, 541, 660), P7, ['A', 'B'],
                         'Photograph of a large round concave mirror on a wall: a child labelled B stands beside it, a '
                         'child labelled A stands close in front of it, and their images appear in the mirror.', False),
    'q9-graph': ('paper', 8, (78, 130, 518, 345), SEC, ['A'],
                 'Graph of temperature (°C), from 0 to 100, against heat added (J): plotted points rise in a straight '
                 'line through the part labelled liquid, run level for three points where an arrow labelled A points, '
                 'then rise again through the part labelled gas.', False),
    'q10-pipe': ('paper', 9, (462, 168, 545, 310), SEC, ['X', 'Y'],
                 'Diagram of a pipe closed at the bottom and open at the top, with a curve drawn inside it for the '
                 'wave; an arrow labelled X points to the open top and an arrow labelled Y points to the closed '
                 'bottom.', False),
    'q10vi-question': ('paper', 9, (80, 312, 465, 337), SEC, [],
                       'The printed question: (vi) The distance from X to Y is taken as λ/4. Calculate the length of '
                       'the pipe.', False),
    'q11-plug': ('paper', 10, (322, 72, 542, 215), 'shutterstock.com', ['A', 'B'],
                 'Diagram of the inside of a three-pin plug with its parts labelled: a wire labelled A, a wire labelled '
                 'neutral, a wire labelled B, the fuse, the cable grip and the cable.', False),
    'q11-circuit': ('paper', 10, (322, 345, 512, 492), SEC, ['X', 'Y', 'Z'],
                    'Circuit diagram: a coil of wire with a meter X connected in parallel across it, in series with a '
                    'meter Y, a variable resistor labelled Z and a battery of cells.', False),
    'q12vi-question': ('paper', 11, (80, 352, 530, 412), SEC, [],
                       'The printed question: (vi) When Pu–239 decays, it emits alpha particles (α with 4 above and 2 '
                       'below). What is the daughter nucleus X in the nuclear reaction below when an atom of Pu (239 '
                       'above, 94 below) emits an alpha particle? Below it: Pu (239 above, 94 below) → X + α (4 above, '
                       '2 below), the numbers set after each symbol.', False),
    'q12vi-scheme': ('scheme', 18, (110, 508, 145, 530), SEC, [],
                     "The marking scheme's answer: U with 235 above and 92 below, set after the symbol.", True),
    'q14a-balanced': ('paper', 13, (110, 160, 375, 196), SEC, [],
                      'Diagram of a box labelled 1900 kg with a force arrow labelled 520 N pointing left and a force '
                      'arrow labelled 520 N pointing right.', False),
    'q14a-unbalanced': ('paper', 13, (110, 366, 380, 402), SEC, [],
                        'Diagram of a box labelled 1900 kg with a force arrow labelled 520 N pointing left and a force '
                        'arrow labelled 680 N pointing right.', False),
    'q14c-grating': ('paper', 14, (180, 106, 445, 255), SEC, [],
                     'Diagram: a laser sends a ray of light to a diffraction grating; lines spread from the grating to '
                     'a white screen marked with bright spots labelled n = 2, n = 1, n = 0, n = 1, n = 2 from top to '
                     'bottom.', False),
    'q14ciii-scheme': ('scheme', 21, (138, 642, 380, 662), SEC, [],
                       "The marking scheme's line: λ = (2.5 × 10⁻⁶)(sin 14.6°) = 6.3 × 10⁻⁷ m.", True),
    'q14d-pear': ('paper', 14, (463, 630, 542, 723), 'www.curiousscience.com/', [],
                  'Photograph of a pear-shaped metal conductor, rounded at one end and pointed at the other, mounted '
                  'on an insulating stand.', False),
}
