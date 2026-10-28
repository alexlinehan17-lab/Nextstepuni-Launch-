"""Physics 2021 Ordinary Level — reviewed task ledger, correcting the sitting in place.

Independent visual sweep (2026-10-28), every page rendered and read:
  * The paper (LC021GLP000EV), 16 pages: p1 cover ("Answer two questions from
    Section A and four questions from Section B"; the 2021 papers were adjusted
    to compensate for disruptions to learning due to COVID-19), p2-p4 Section A
    (80 marks) Questions 1-5 (any two, 40 marks each), p5-p14 Section B (224
    marks) Questions 6-14 (any four, 56 marks each), p15 acknowledgements
    (images on pages 5-14), p16 back cover (copyright notice).
  * The marking scheme, 24 pages: p1 cover, p2 note on published schemes, p3
    points to note (solidus, double solidus, units, slips), p4 annotation
    symbols, p5 Irish-language bonus table, p6-p22 Questions 1-14 (each part's
    reprint in bold with its tariff, "4 × 3", "6 or 3", "10 or 7 or 4", shaded at
    the right margin; each answer line with its own mark, a partial mark in
    brackets), p23 blank, p24 back cover.

Every printed ask is carded at the scheme's own mark boundary, one card per roman
(Q6 and Q13 per letter). The paper prints a group mark after a run of romans
("(14)" closing Q1(ii)-(iv)): GROUP_TOTALS. Q6 is any eight of (a)-(l) at 7 each
(8 x 7): one card per letter. Q14 is any two of (a)-(d): every part is carded.
The scheme prices most parts "6 or 3": the answer at 6 and a partial answer at
(3); the partial mark is a note on the answer row, never a row of its own. A line
the scheme prices once for several things ("force, charge and distance ... three
correct 7", "any two 3") is one row at its price. "A // B" against one mark is a
menu of the alternatives (claim one); "e.g. a, b, etc." examples are open menus;
"any 4 lines (4 × 3)" is a menu of four claims. Q7(ii) and Q14(a)(iii) print an
answer in words "//" as a formula: routes inside the card.

The scheme sets its working as CambriaMath stacked fractions; they are read with
G('fraction'), Q1(v)'s and Q9(v)'s full workings included (a span that starts under
a fraction bar and ends past it belongs to the line, not the fraction). The paper sets 1/V (Q2(iv), (v)), g = 2s/t² (Q1(v)), Coulomb's
law (Q6(g)) and the curium nuclide (Q12(x)) in a maths font whose text layer is
out of order: those asks are shown as printed (question figures), the question
text cut before the formula. Q12(v)'s meitnerium nuclide is read with
G('equation').

The sitting was already carded (121 authored cards, 116 shipped). Every task is
re-derived from the PDFs and the existing cards are corrected in place: every id
is kept, mapped (`id=`) to the task it was carding, or withdrawn. Q6(i), Q9(iii),
Q9(ix) and Q14(d)(iii) were each carded twice (once with, once without a
figure; the build shipped one): one task each, the other id withdrawn. Q14(d)(iv)
and (v) were carded both together and apart: the parts keep their own cards and
the bundle is withdrawn. Q11(vii), never shipped (its figure key named no crop),
has its garden diagram cropped anew. The asks the bank had excluded (Q11(x),
Q13(e), Q13(g), Q14(c)(iii)) and left open (Q3(ii), Q9(vi)-(viii), Q10(iv),
Q11(vii)) are carded, and the bundled parts (Q9(iv)-(v), Q10(vii)-(viii),
Q11(iv)-(v), Q14(a)(iv)-(vi)) are split.
"""
from phys_review_lib import Q, SQ, S, M, G, pt, anyn, T, L, drawn

YEAR, LEVEL = 2021, 'ol'
REVIEWED_AT = '2026-10-28'
BASELINE_COMMIT = '99ec7f0a0d6b243f4d5a1dc9b14a6a958e98095e'

SOURCES = {
    'paper': {'path': 'examiner-reports/physics/papers/2021-ol-paper.pdf', 'fileid': 'LC021GLP000EV.pdf',
              'sha256': 'd31e6b959913c35b4700d5d1ec83b554dd1c3e00a7adbe642fdd032204145c1e', 'pages': 16},
    'scheme': {'path': 'examiner-reports/physics/schemes/2021-ol.pdf', 'fileid': 'LC021GLP000EV.pdf',
               'sha256': '228f3336be97ed97331f782625f8238c94b8bd19513519721cf261141c2f7686', 'pages': 24},
}

PAGE_ROLES = {
    'paper': {1: 'cover', **{p: 'questions' for p in range(2, 15)}, 15: 'acknowledgements', 16: 'back-cover'},
    'scheme': {1: 'cover', 2: 'note', 3: 'conventions', 4: 'annotations', 5: 'irish-bonus',
               **{p: 'marking' for p in range(6, 23)}, 23: 'blank', 24: 'back-cover'},
}

LETTERED = {6, 13, 14}

QUESTION_TOTALS = {**{n: 40 for n in range(1, 6)}, **{n: 56 for n in range(6, 14)},
                   14: 112}   # any two of (a)-(d), 28 each: all four carded
PART_TOTALS = {(14, x): 28 for x in 'abcd'}
BEST_OF = {6: (8, 7)}
GROUP_TOTALS = {
    (1, ('i',)): 12, (1, ('ii', 'iii', 'iv')): 14, (1, ('v', 'vi', 'vii')): 14,
    (2, ('i', 'ii', 'iii')): 18, (2, ('iv', 'v', 'vi')): 22,
    (3, ('i', 'ii')): 18, (3, ('iii', 'iv', 'v', 'vi', 'vii')): 22,
    (4, ('i',)): 12, (4, ('ii', 'iii', 'iv', 'v')): 16, (4, ('vi',)): 12,
    (5, ('i', 'ii', 'iii')): 18, (5, ('iv', 'v', 'vi')): 22,
    (7, ('i', 'ii', 'iii', 'iv', 'v')): 28, (7, ('vi', 'vii', 'viii', 'ix', 'x')): 28,
    (8, ('i', 'ii', 'iii', 'iv')): 28, (8, ('v', 'vi', 'vii', 'viii', 'ix')): 28,
    (9, ('i', 'ii')): 12, (9, ('iii', 'iv', 'v')): 18, (9, ('vi', 'vii', 'viii')): 18, (9, ('ix', 'x')): 8,
    (10, ('i', 'ii', 'iii')): 28, (10, ('iv', 'v', 'vi', 'vii', 'viii')): 28,
    (11, ('i', 'ii', 'iii', 'iv', 'v', 'vi')): 28, (11, ('vii', 'viii', 'ix', 'x', 'xi')): 28,
    (12, ('i', 'ii', 'iii', 'iv', 'v')): 28, (12, ('vi', 'vii', 'viii', 'ix', 'x')): 28,
}
CHECKSUMS = {}
ROUTES = {}

SCAN_PAGES = {'paper': range(2, 15)}
SELECTION_SCAN = [
    ('paper', 2, 'the following', 'Q1 "The student recorded the following results": a reference to the table.'),
    ('paper', 3, 'the following', 'Q2 "The student recorded the following results": a reference to the table.'),
    ('paper', 4, 'the following', 'Q4 "The student recorded the following results": a reference to the results.'),
    ('paper', 4, 'the following', 'Q4(vi) "complete the following calculations": a reference to the calculation.'),
    ('paper', 4, 'the following', 'Q5 "The student recorded the following results": a reference to the table.'),
    ('paper', 5, 'the following', 'Q6 "Answer any eight of the following parts": a best-eight of (a)-(l) at 7 '
                                  'each (8 x 7); every part is carded (BEST_OF).'),
    ('paper', 6, 'or', 'Q7(v) "cause its speed to increase or to decrease?": the answer options.'),
    ('paper', 7, 'either', 'Q8(iii) "either transverse or longitudinal": description.'),
    ('paper', 7, 'or', 'Q8(iii), the same phrase.'),
    ('paper', 7, 'both', 'Q8 lead-in "Light and sound waves both display": description.'),
    ('paper', 10, 'both', 'Q11(vi) "both thermometers are working correctly": description.'),
    ('paper', 12, 'the following', 'Q13 "Read the following passage": a reference to the passage.'),
    ('paper', 12, 'or', 'Q13(f) "no longer moved up or down": description.'),
    ('paper', 12, 'or', 'Q13(h) "not moving up or down": description.'),
    ('paper', 13, 'any two', 'Q14 "Answer any two of the following parts": whole-part choice; every part is carded.'),
    ('paper', 13, 'the following', 'Q14, the same rubric.'),
    ('paper', 14, 'or', 'Q14(c) lead-in "attract or repel each other": description.'),
]
ASK_SCAN_PAGES = {'paper': range(2, 15)}
ASK_EXEMPT = [
    (8, 'The photograph shows a rheostat', 'Q9 lead-in to (iii) ("When the sliding contact is moved, the current flows '
                                          'through a different length of wire ..."): a description, not an ask; '
                                          'lifted into the stem of (iii).'),
    (14, 'Waves on a stretched string travel at a speed of 380 m', 'Q14(d) lead-in to (iv)-(v) ("When a stationary '
                                                                   'wave is set up on a string ..."): a description, '
                                                                   'not an ask; lifted into their stems.'),
]

SEC = 'State Examinations Commission'
CRIT = 'The scheme prints no answer here, only what earns the marks.'
EXPT = 'A "describe an experiment" part: the scheme prices apparatus, method and observation and prints no answer.'
LEGEND = S('Answers that are separated by a double solidus, //, are answers which are mutually',
           'answer from the other side.', page=3)
MENU = ('The scheme prints {what} against one mark: a menu, any one of them claimed.')
LINKED = ('{w} reads to the figure-pointer check as a printed figure; {why}, so the card links its exam '
          'page.')
OWN = 'the ask is the student\'s own drawing'


def P(page, start, end=None, **kw):
    return Q(page, start, end, **kw)


def R(text, marks, end=None, **kw):
    """A row lifted whole from the task's scheme page."""
    return pt(S(text, end), marks, **kw)


def C(text, marks, end=None, note=CRIT, **kw):
    """A criterion the scheme prices without printing an answer."""
    return pt(S(text, end), marks, kind='criterion', note=note, **kw)


def PB(n):
    """The scheme's bare "partial answer" line, whose mark is printed in its own cell."""
    return f'The scheme gives ({n}) for a partial answer.'


def PX(n, start):
    """A "partial answer e.g. ..." line, lifted, as a row's note."""
    return {'note_sel': S(start), 'note_lead': f'Partial credit ({n}):'}


def pieces(line, ks, sep=',', end=None, first=None):
    """The items of one printed list, cut at the scheme's own separator; `first` cuts a lead ("e.g. ",
    "apparatus: ") off the first item."""
    out = []
    for k in ks:
        if k == 1 and first:
            out.append(S(line, end, piece=[1, 2], psep=[sep, first]))
        else:
            out.append(S(line, end, piece=k, psep=sep))
    return out


def bundled(parts, keep):
    return f'The old card bundled {parts}, which the scheme prices apart; it keeps its id for {keep}.'


# ------------------------------------------------------------------ stems --
STEM1 = P(2, 'A student carried out an experiment to measure the acceleration due to gravity g.',
          'the time t for the fall was measured.')
TABLE1 = [P(2, 'The student recorded the following results.'), P(2, 's (m)', '0.43')]
GVAL1 = P(2, 'The value for g, the acceleration due to gravity near the surface of the Earth, is 9.8 m s⁻².')
STEM2 = P(3, 'A student performed an experiment to verify Boyle’s law', 'fixed mass of gas.')
TABLE2 = [P(3, 'The student recorded the following results.'), P(3, 'V (cm³)', '223')]
STEM3 = P(3, 'A student carried out an experiment to measure f, the focal length of a converging lens.')
Q3I = P(3, 'Draw a labelled diagram of the apparatus used in this experiment.', nth=2)
STEM4 = P(4, 'A student carried out an experiment to measure l, the specific latent heat of vaporisation of',
          'copper calorimeter.')
RESULTS4 = [P(4, 'The student recorded the following results.'), P(4, 'Mass of empty calorimeter', '= 0.1341 kg')]
STEM5 = P(4, 'A student performed an experiment to investigate the variation of current I with potential',
          'for a metallic conductor.')
TABLE5 = [P(4, 'The student recorded the following results.', nth=2), P(4, 'I (A)', '6', end_nth=3)]
BAGGER7 = P(6, 'The Bagger 293 excavator is the world’s largest land', 'Bagger 293 has a maximum speed of 0.17 m s⁻¹.')
TRAINS7 = P(6, 'Toy train X has a mass of 133 g', 'move down the track together.')
RHEOSTAT9 = P(8, 'The photograph shows a rheostat', 'resistance of the rheostat.')
WIRE9 = P(8, 'A 4.8 m length of circular nichrome wire', 'Ω m.')
CIRCUIT9 = P(8, 'Examine the circuit diagram shown on the right.')
PLUG9 = P(8, 'The diagram on the left shows the parts of an', 'electrical plug.')
PERISCOPE10 = P(9, 'A periscope is used on a submarine.', 'surface of the water.')
OBJECT10 = [P(9, 'An object of height 2 cm is placed 17 cm in front of a concave mirror.'),
            P(9, 'An image with a height of 3 cm is formed.')]
TEMP11 = P(10, 'The normal human body temperature is 37 °C.', 'fighting an infection.')
SOLAR11 = P(10, 'The solar constant (solar irradiance) is a measure of how much', 'kW m⁻².')
GARDEN11 = P(10, 'The diagram on the right shows a rectangular garden.', 'exactly 12 hours.')
MT12 = P(11, 'Meitner never won a Nobel Prize for her discovery', 'meitnerium, Mt.')
CURIE12 = P(11, 'Marie Curie also has an element named after her', 'radioactivity.')
THREE12 = P(11, 'There are three types of nuclear radiation: alpha, beta and gamma.')
FALCON14 = P(13, 'A SpaceX Falcon 9 rocket carrying two astronauts', 'International Space Station (ISS).')
ISS14 = P(13, 'The ISS is located 400 km above the Earth’s surface.', 'measured to be 85 kg.')
G14 = P(13, '(acceleration due to gravity on Earth’s surface = 9.8 m s⁻²)')
LIGHTNING14 = P(13, 'Lightning is a naturally occurring electrostatic discharge.', 'usually a cloud and the ground.')
STATIC14 = P(13, 'Static electricity builds up in the cloud and releases 0.9 GJ', 'as it discharges.')
MAGNET14 = P(14, 'Magnetism is the force exerted by magnets when they attract or repel each other.')
VIBRATE14 = P(14, 'Sounds are produced when something vibrates.')
WAVE14 = P(14, 'Waves on a stretched string travel at a speed of 380 m s⁻¹.', 'adjacent nodes is 40 cm.')

TASKS = [
    # ============================================================ Section A ==
    # ---------------------------------------------------------------- Q1 --
    T('1i', 'Q1(i)', 'A', P(2, 'Draw a labelled diagram of the apparatus used in this experiment.'),
      [R('falling object e.g. (metal) ball', 3), R('starting mechanism e.g. release mechanism', 3),
       R('stopping mechanism e.g. trapdoor', 3),
       R('means of measuring time e.g. timing circuit/ (electronic) timer', 3,
         note_sel=S('NOTE: no labels deduct 2'), note=PB(3))],
      'phys-u2', 'free-fall-apparatus', SQ(6, 'Draw a labelled diagram of the apparatus used in this experiment.'), 12,
      stem=[STEM1], id='phys-2021-ol-q1-i'),
    T('1ii', 'Q1(ii)', 'A', P(2, 'How did the student measure the distance s?'),
      [R('metre stick / ruler / measuring tape', 6, **PX(3, 'partial answer e.g. from the bottom'))], 'phys-u2',
      'measuring-the-distance', SQ(6, 'How did the student measure the distance s?'), 6, stem=[STEM1],
      id='phys-2021-ol-q1-ii'),
    T('1iii', 'Q1(iii)', 'A', P(2, 'How did the student measure the time t for the object to fall?'),
      [R('timer', 5, **PX(3, 'partial e.g. from when ball starts'))], 'phys-u2', 'measuring-the-time',
      SQ(6, 'How did the student measure the time t for the object to fall?'), 5, stem=[STEM1],
      id='phys-2021-ol-q1-iii'),
    T('1iv', 'Q1(iv)', 'A', P(2, 'How did the student improve the accuracy of the time t that was used?'),
      [anyn(None, 1, 3, open_list=True,
            options=pieces('take the smallest time for t, repeat', range(1, 7), end='electronic timer, etc.'))],
      'phys-u2', 'improving-the-time', SQ(6, 'How did the student improve the accuracy of the time t that was used?'),
      3, stem=[STEM1], id='phys-2021-ol-q1-iv',
      decision=MENU.format(what='six ways, cut at its own commas, then "etc."')),
    T('1v', 'Q1(v)', 'A', P(2, 'From the table, when the distance s is 0.4 m the time t is 0.29 s.', 'formula g =',
                         piece=1, psep=' g ='),
      [G('fraction', page=6, clip=(108, 573.4, 290, 596), expect='(g= 2s/t² = 2(0.4)/(0.29)² = 0.8/0.0841 =)9.5 m s⁻²',
         marks=6, note=PB(3))], 'phys-1-5', 'g-from-one-reading',
      SQ(6, 'From the table, when the distance s is 0.4 m the time t is 0.29 s. Use this data and the'), 6,
      stem=[STEM1] + TABLE1 + [GVAL1], qfig='q1v-question', id='phys-2021-ol-q1-v',
      decision='The ask ends in the formula g = 2s/t², which the paper sets as a stacked fraction the text layer '
               'reads out of order: the question text stops before it and the ask is shown as printed. The '
               'scheme\'s working is read with G(\'fraction\').'),
    T('1vi', 'Q1(vi)', 'A', P(2, 'Use the results to calculate two other values for g and calculate their average.'),
      [R('9.76 m s', 3, end='any two'), R('average of any two above', 3)], 'phys-1-5', 'average-value-of-g',
      SQ(6, 'Use the results to calculate two other values for g and calculate their average.'), 6,
      stem=[STEM1] + TABLE1, id='phys-2021-ol-q1-vi',
      decision='The scheme prints five values and prices "any two" of them together (3): one row at its price; then '
               'the average (3).'),
    T('1vii', 'Q1(vii)', 'A', P(2, 'The maximum distance used is 0.9 m.', 'distance?'),
      [anyn(None, 1, 2, open_list=True,
            options=pieces('difficult to measure with metre stick', (1, 2)))], 'phys-u2', 'why-not-a-greater-distance',
      SQ(6, 'The maximum distance used is 0.9 m. Why does the student not use a greater distance?'), 2, stem=[STEM1],
      id='phys-2021-ol-q1-vii', decision=MENU.format(what='two reasons, then "etc."')),
    # ---------------------------------------------------------------- Q2 --
    T('2i', 'Q2(i)', 'A', P(3, 'Draw a labelled diagram of the apparatus used in this experiment.'),
      [anyn(None, 4, 3, note_sel=S('NOTE: no labels deduct 2, accept valid alternatives'),
            options=[S('enclosed volume of gas'), S('means of measuring/reading the volume scale'),
                     S('means of measuring/ reading the pressure e.g. pressure gauge'),
                     S('means of altering the pressure/volume e.g. pump'), S('detail e.g. correct arrangement')])],
      'phys-u2', 'boyles-law-apparatus', SQ(7, 'Draw a labelled diagram of the apparatus used in this experiment.'),
      12, stem=[STEM2], id='phys-2021-ol-q2-i',
      decision='Five lines priced "any 4 lines (4 × 3)": a menu of four claims at 3.'),
    T('2ii', 'Q2(ii)', 'A', P(3, 'How is the pressure varied in this experiment?'),
      [anyn(S('pump / valve // piston'), 1, 3, sep='//')], 'phys-u2', 'varying-the-pressure',
      SQ(7, 'How is the pressure varied in this experiment?'), 3, stem=[STEM2], id='phys-2021-ol-q2-ii',
      decision=MENU.format(what='"pump / valve // piston"')),
    T('2iii', 'Q2(iii)', 'A', P(3, 'Each time the pressure is changed, the student must wait before taking the reading for',
                               'Explain why.'),
      [R('to allow the gas to settle (to room temperature/ to cool)', 3)], 'phys-u2', 'waiting-before-reading',
      SQ(7, 'Each time the pressure is changed, the student must wait before taking the reading for', 'Explain why.'),
      3, stem=[STEM2], id='phys-2021-ol-q2-iii'),
    T('2iv', 'Q2(iv)', 'A', P(3, 'Boyle’s law states that for a fixed mass of gas, pressure is inversely proportional to',
                             'calculate'),
      [pt(S(v), 1, label=S(vol, after='V (cm³)'),
          **({'note': 'The scheme prints the six values of 1/V (cm⁻³), (6 × 1), each under its volume V (cm³): '
                      '1 mark each.'} if k == 0 else {}))
       for k, (vol, v) in enumerate((('19', '0.053'), ('17', '0.059'), ('15', '0.067'), ('13', '0.077'),
                                     ('11', '0.091'), ('9', '0.111')))],
      'phys-u2', 'values-of-one-over-v',
      SQ(7, 'Boyle’s law states that for a fixed mass of gas, pressure is inversely proportional to volume.'), 6,
      stem=[STEM2] + TABLE2, qfig='q2iv-question', id='phys-2021-ol-q2-iv',
      decision='The ask ends in "1/V", which the paper sets as a stacked fraction the text layer reads out of order: '
               'the question text stops before it and the ask is shown as printed. The scheme prints the six values '
               'as a table row: one row per value, labelled with the volume printed above it.'),
    T('2v', 'Q2(v)', 'A', P(3, 'Plot a graph on graph paper of p against'),
      [C('label axes correctly, (name / symbol / unit acceptable)', 3),
       C('plot six points correctly', 6, units=[1] * 6, note=CRIT + ' It prices them (6 × 1): 1 mark per point.'),
       R('straight line', 3, note_sel=S('if graph paper is not used, maximum mark 3 × 3'))],
      'phys-u2', 'graph-of-p-against-one-over-v', SQ(7, 'Plot a graph on graph paper of p against'), 12,
      stem=[STEM2] + TABLE2, qfig='q2v-question', fig='q2v-scheme-graph', id='phys-2021-ol-q2-v',
      decision='The ask ends in "1/V", set as a stacked fraction: the question text stops before it and the ask is '
               'shown as printed. The scheme draws its graph (the solution figure).'),
    T('2vi', 'Q2(vi)', 'A', P(3, 'Use your graph to calculate the volume of the gas when its pressure is 140 kPa.'),
      [G('fraction', page=7, clip=(108, 703, 272, 726), expect='reads 1/V value from graph e.g. 0.07', marks=2),
       R('invert value to get V e.g. V= 14.3 cm³', 2)], 'phys-u2', 'volume-from-graph',
      SQ(7, 'Use your graph to calculate the volume of the gas when its pressure is 140 kPa.'), 4, stem=[STEM2],
      source_pages=[3], id='phys-2021-ol-q2-vi',
      decision=LINKED.format(w='"your graph"', why='the graph is the student\'s own')),
    # ---------------------------------------------------------------- Q3 --
    T('3i', 'Q3(i)', 'A', Q3I,
      [R('object e.g. crosswire, raybox', 3), R('(converging) lens', 3), R('screen', 3),
       R('detail e.g. correct arrangement, optical bench, metre stick, etc.', 3,
         note_sel=S('NOTE: no labels deduct 2, accept valid alternatives'))],
      'phys-u2', 'converging-lens-apparatus', SQ(8, 'Draw a labelled diagram of the apparatus used in this experiment.'),
      12, stem=[STEM3], id='phys-2021-ol-q3-i'),
    T('3ii', 'Q3(ii)', 'A', P(3, 'On your diagram, indicate and label the object distance u and the image', 'distance v.'),
      [C('correctly marked u and v distances', 6, **PX(3, 'partial answer e.g. one correct'))], 'phys-u2',
      'marking-u-and-v', SQ(8, 'On your diagram, indicate and label the object distance u and the image distance v'),
      6, stem=[STEM3, M('(i)', 3), Q3I], source_pages=[3],
      decision='The bank had left this part open. ' + LINKED.format(w='"the image distance"',
                                                                     why='it is the image the lens forms, and the '
                                                                         'paper prints no figure for it')),
    T('3iii', 'Q3(iii)', 'A', P(3, 'Name the instrument used to measure the object distance and the image distance.'),
      [anyn(S('metre stick, measuring tape, optical bench with scale, ruler'), 1, 3, sep=',')], 'phys-u2',
      'measuring-u-and-v', SQ(8, 'Name the instrument used to measure the object distance and the image distance.'),
      3, stem=[STEM3], source_pages=[3], id='phys-2021-ol-q3-iii',
      decision=MENU.format(what='four instruments, cut at its own commas,') + ' ' +
               LINKED.format(w='"the image distance"', why='it is the image the lens forms, and the paper prints no '
                                                          'figure for it')),
    T('3iv', 'Q3(iv)', 'A', P(3, 'How did the student know that the correct image distance had been found?'),
      [R('image in sharp focus', 3)], 'phys-u2', 'finding-the-image',
      SQ(8, 'How did the student know that the correct image distance had been found?'), 3, stem=[STEM3],
      source_pages=[3], id='phys-2021-ol-q3-iv',
      decision=LINKED.format(w='"the correct image distance"', why='it is the image the lens forms, and the paper '
                                                                   'prints no figure for it')),
    T('3v', 'Q3(v)', 'A', P(3, 'State the formula used to calculate f.'),
      [G('fraction', page=8, clip=(102, 371, 158, 394), expect='1/u + 1/v = 1/f', marks=6,
         note='The scheme gives (3) for "one error".')], 'phys-2-3', 'lens-formula',
      SQ(8, 'State the formula used to calculate f.'), 6, stem=[STEM3], id='phys-2021-ol-q3-v'),
    T('3vi', 'Q3(vi)', 'A', P(3, 'The student placed an object 16 cm in front of the converging lens.',
                             'Calculate the focal length of this lens.'),
      [G('fraction', page=8, clip=(102, 449, 250, 473), expect='( 1/16 + 1/48 = 1/12 ⇒ f =) 12 cm', marks=6,
         **PX(3, 'partial answer e.g. correct substitution'))], 'phys-2-3', 'focal-length-calculation',
      SQ(8, 'The student placed an object 16 cm in front of the converging lens. It produced an image',
         'Calculate the focal length of this lens.'), 6, id='phys-2021-ol-q3-vi'),
    T('3vii', 'Q3(vii)', 'A', P(3, 'Why will this experiment not work if the object is placed very close to the lens?'),
      [R('virtual image (formed when u< f ), cannot form image on screen', 4, note=PB(2))], 'phys-2-3',
      'object-too-close', SQ(8, 'Why will this experiment not work if the object is placed very close to the lens?'),
      4, stem=[STEM3], id='phys-2021-ol-q3-vii'),
    # ---------------------------------------------------------------- Q4 --
    T('4i', 'Q4(i)', 'A', P(4, 'Draw a labelled diagram of the apparatus used in this experiment.'),
      [anyn(None, 4, 3, note_sel=S('NOTE: no labels deduct 2, incorrect experiment maximum mark'),
            options=[S('calorimeter with water'), S('steam source'), S('thermometer'), S('insulation'),
                     S('steam trap')])],
      'phys-u2', 'latent-heat-apparatus', SQ(9, 'Draw a labelled diagram of the apparatus used in this experiment.'),
      12, stem=[STEM4], id='phys-2021-ol-q4-i',
      decision='Five lines priced "any 4 lines (4 × 3)": a menu of four claims at 3.'),
    T('4ii', 'Q4(ii)', 'A', P(4, 'Calculate the mass of the cold water (A).'),
      [R('(0.1327', 4)], 'phys-u2', 'mass-of-cold-water', SQ(9, 'Calculate the mass of the cold water (A).'), 4,
      stem=[STEM4] + RESULTS4, id='phys-2021-ol-q4-ii'),
    T('4iii', 'Q4(iii)', 'A', P(4, 'Calculate the mass of the added steam (B).'),
      [R('(0.1341', 4)], 'phys-u2', 'mass-of-added-steam', SQ(9, 'Calculate the mass of the added steam (B).'), 4,
      stem=[STEM4] + RESULTS4, id='phys-2021-ol-q4-iii'),
    T('4iv', 'Q4(iv)', 'A', P(4, 'Calculate the increase in temperature of the calorimeter and cold water (C).'),
      [R('(36', 4)], 'phys-u2', 'temperature-rise-of-water',
      SQ(9, 'Calculate the increase in temperature of the calorimeter and cold water (C).'), 4,
      stem=[STEM4] + RESULTS4, id='phys-2021-ol-q4-iv'),
    T('4v', 'Q4(v)', 'A', P(4, 'Calculate the decrease in temperature of the steam (D).'),
      [R('(100', 4)], 'phys-u2', 'temperature-fall-of-steam',
      SQ(9, 'Calculate the decrease in temperature of the steam (D).'), 4, stem=[STEM4] + RESULTS4,
      id='phys-2021-ol-q4-v'),
    T('4vi', 'Q4(vi)', 'A', P(4, 'Use your values for A, B, C and D to complete the following calculations to find l.'),
      [R('(0.0014) l +', 2), R('(0.0014)(4200)(64)', 2), R('= (0.0433)(4200)(16)', 2),
       R('+ (0.0894)(390)(16)', 2, note_sel=S('correct substitutions')),
       pt(S('(0.0014) l', '10⁶ J kg⁻¹', nth=2), 4)],
      'phys-2-1', 'latent-heat-of-vaporisation',
      SQ(9, 'Use your values for A, B, C and D to complete the following calculations to find l.'), 12,
      stem=[STEM4] + RESULTS4, fig='q4-calc', id='phys-2021-ol-q4-vi',
      decision='"correct substitutions (4 × 2)" against the four printed terms of the equation: one row per term, '
               '2 each; then the answer (4).'),
    # ---------------------------------------------------------------- Q5 --
    T('5i', 'Q5(i)', 'A', P(4, 'Name the instrument used to measure voltage.'),
      [R('voltmeter', 6, **PX(3, 'partial answer e.g. multimeter'))], 'phys-u2', 'measuring-voltage',
      SQ(10, 'Name the instrument used to measure voltage.'), 6, stem=[STEM5], id='phys-2021-ol-q5-i'),
    T('5ii', 'Q5(ii)', 'A', P(4, 'Name the instrument used to measure current.'),
      [R('ammeter', 6, **PX(3, 'partial answer e.g. multimeter'))], 'phys-u2', 'measuring-current',
      SQ(10, 'Name the instrument used to measure current.'), 6, stem=[STEM5], id='phys-2021-ol-q5-ii'),
    T('5iii', 'Q5(iii)', 'A', P(4, 'How did the student change the voltage across the conductor?'),
      [anyn(S('adjust variable voltage // adjust the variable resistor'), 1, 6, sep='//', note=PB(3))], 'phys-u2',
      'changing-the-voltage', SQ(10, 'How did the student change the voltage across the conductor?'), 6,
      stem=[STEM5], id='phys-2021-ol-q5-iii', decision=MENU.format(what='two ways separated by "//"')),
    T('5iv', 'Q5(iv)', 'A', P(4, 'Use the data to plot a graph on graph paper to show the relationship between I and V.'),
      [C('label axes correctly, (name / symbol / unit acceptable)', 3),
       C('plot six points correctly', 6, units=[1] * 6, note=CRIT + ' It prices them (6 × 1): 1 mark per point.'),
       R('straight line', 3, note_sel=S('if graph paper is not used, maximum mark 3 × 3'))],
      'phys-u2', 'current-voltage-graph',
      SQ(10, 'Use the data to plot a graph on graph paper to show the relationship between I and V.'), 12,
      stem=[STEM5] + TABLE5, fig='q5iv-scheme-graph', id='phys-2021-ol-q5-iv',
      decision='The scheme draws its graph (the solution figure); the data table is lifted into the stem.'),
    T('5v', 'Q5(v)', 'A', P(4, 'Describe the relationship between current and voltage for this conductor.'),
      [dict(anyn(S('V ∝ I // proportional'), 1, 6, sep='//'), **PX(3, 'partial answer e.g. linear'))], 'phys-3-3',
      'current-and-voltage', SQ(10, 'Describe the relationship between current and voltage for this conductor.'), 6,
      stem=[STEM5], id='phys-2021-ol-q5-v', decision=MENU.format(what='two forms separated by "//"')),
    T('5vi', 'Q5(vi)', 'A', P(4, 'What would you notice if the experiment was repeated using a filament bulb instead',
                             'of a metallic conductor?'),
      [anyn(S('bulb would get hot // not proportional/curved graph'), 1, 4, sep='//', note=PB(2))], 'phys-3-3',
      'filament-bulb', SQ(10, 'What would you notice if the experiment was repeated using a filament bulb instead',
                          'of a metallic conductor?'), 4, stem=[STEM5], id='phys-2021-ol-q5-vi',
      decision=MENU.format(what='two observations separated by "//"')),
    # ============================================================ Section B ==
    # ---------------------------------------------------------------- Q6 --
    T('6a', 'Q6(a)', 'B', P(5, 'A student arranges a metre stick so that it is in equilibrium.',
                           'Explain the underlined term.'),
      [R('no movement / no acceleration / nett force zero / balanced', 7, **PX(4, 'partial answer e.g. no force acts'))],
      'phys-1-2', 'equilibrium', SQ(11, 'A student arranges a metre stick so that it is in equilibrium. Explain the',
                                     'underlined term.'), 7, qfig='q6a-question', id='phys-2021-ol-q6-a',
      decision='The ask names "the underlined term", and the underline does not survive as text: the ask is shown as '
               'printed.'),
    T('6b', 'Q6(b)', 'B', P(5, 'A car starts from rest and has an acceleration of 6 m s⁻².', 'travels in 12 s.'),
      [G('fraction', page=11, clip=(108, 177, 318, 201), expect='(s= ut+ ½ at² = 0 + ½ (6)(12)² =)432 m', marks=7,
         **PX(4, 'partial answer e.g. states equation of motion'))],
      'phys-1-1', 'distance-from-rest', SQ(11, 'A car starts from rest and has an acceleration of 6 m s⁻².',
                                           'It travels in 12 s.'), 7, id='phys-2021-ol-q6-b'),
    T('6c', 'Q6(c)', 'B', P(5, 'Water has a density of 997 kg m⁻³.', 'of 214 m.'),
      [R('(P=', 7, note=PB(4))], 'phys-1-2', 'pressure-at-depth',
      SQ(11, 'Water has a density of 997 kg m⁻³. Calculate the pressure due to water at a depth', 'Of 214 m.'), 7,
      id='phys-2021-ol-q6-c'),
    T('6d', 'Q6(d)', 'B', P(5, 'Complimentary colours mix to form white light.', 'to form white light.', end_nth=2),
      [R('turquoise / cyan', 7)], 'phys-2-4', 'complementary-of-red',
      SQ(11, 'Complimentary colours mix to form white light. Name the secondary colour',
         'which mixes with red light to form white light.'), 7, id='phys-2021-ol-q6-d'),
    T('6e', 'Q6(e)', 'B', P(5, 'What is the Doppler effect?'),
      [R('(apparent) change in (wave) frequency /wavelength due to moving source/observer', 7, note=PB(4))],
      'phys-2-7', 'doppler-effect', SQ(11, 'What is the Doppler effect?'), 7, id='phys-2021-ol-q6-e'),
    T('6f', 'Q6(f)', 'B', P(5, 'Draw a diagram to show how light is transmitted along an optical fibre.'),
      [R('diagram showing fibre and', 7, end='multiple internal reflections', note=PB(4))], 'phys-2-3',
      'optical-fibre', SQ(11, 'Draw a diagram to show how light is transmitted along an optical fibre.'), 7,
      fig='q6f-scheme', id='phys-2021-ol-q6f',
      decision='The scheme draws its diagram beside the row (the solution figure).'),
    T('6g', 'Q6(g)', 'B', [P(5, 'Coulomb’s law may be written as', piece=1, psep=' F='),
                          P(5, 'What do the letters', 'stand for in this expression?', br=True)],
      [R('force, charge and distance (between charges)', 7, end='three correct', **PX(4, 'any one correct'))],
      'phys-3-1', 'coulombs-law-symbols', SQ(11, 'Coulomb’s law may be written as'), 7, qfig='q6g-question',
      id='phys-2021-ol-q6-g',
      cells='The "(4)" printed against "any one correct" is the mark given instead of the 7 when only one is right, '
            'not added to it (the reader adds only a line opening "partial").',
      decision='The paper sets the law as stacked fractions the text layer reads out of order: the ask is shown as '
               'printed. The scheme prices the three meanings together, "three correct 7": one row at its price.'),
    T('6h', 'Q6(h)', 'B', P(5, 'State the SI unit of (i) magnetic flux density,', '(ii) capacitance.'),
      [R('(i) tesla/T (ii) farad/F', 7, **PX(4, 'partial answer e.g. one correct'))], 'phys-3-2', 'si-units',
      SQ(11, 'State the SI unit of (i) magnetic flux density, (ii) capacitance.'), 7, id='phys-2021-ol-q6-h',
      decision='The scheme prices both units together (7): one row at its price.'),
    T('6i', 'Q6(i)', 'B', P(5, 'The picture on the right is an X', 'tungsten makes it suitable for this use?'),
      [anyn(S('high melting point'), 1, 7, sep='//', note=PB(4))], 'phys-4-2', 'tungsten-target',
      SQ(11, 'The picture on the right is an X', 'tungsten makes it suitable for this use?'), 7, fig='q6i-xray',
      id='phys-2021-ol-q6i-fig', decision=MENU.format(what='three properties separated by "//"')),
    T('6j', 'Q6(j)', 'B', P(5, 'Silicon is an example of a semiconductor.', 'What is a semiconductor?'),
      [R('substance whose resistivity/conductivity is between that of a conductor and insulator', 7, note=PB(4))],
      'phys-3-3', 'semiconductor', SQ(11, 'Silicon is an example of a semiconductor. What is a semiconductor?'), 7,
      id='phys-2021-ol-q6-j'),
    T('6k', 'Q6(k)', 'B', P(5, 'Draw a diagram to outline the Bohr model of the atom.'),
      [R('diagram showing nucleus, electron shell, another electron shell', 7, end='any two', note=PB(4))],
      'phys-4-3', 'bohr-model', SQ(11, 'Draw a diagram to outline the Bohr model of the atom.'), 7, fig='q6k-scheme',
      id='phys-2021-ol-q6k',
      decision='The scheme prices "any two" of the three features together (7): one row at its price; its drawing '
               'is the solution figure.'),
    T('6l', 'Q6(l)', 'B', P(5, 'What is the photoelectric effect?'),
      [R('emission of electrons (from a metal surface) by (incident) light', 7, note=PB(4))], 'phys-4-2',
      'photoelectric-effect', SQ(11, 'What is the photoelectric effect?'), 7, id='phys-2021-ol-q6-l'),
    # ---------------------------------------------------------------- Q7 --
    T('7i', 'Q7(i)', 'B', P(6, 'Bagger 293 has a large momentum.', 'by momentum?'),
      [R('mass multiplied by velocity / mv', 6, note=PB(3))], 'phys-1-2', 'momentum',
      SQ(12, 'Bagger 293 has a large momentum. What is meant by momentum?'), 6, id='phys-2021-ol-q7-i'),
    T('7ii', 'Q7(ii)', 'B', P(6, 'State the principle of conservation of momentum.'),
      [R('(in a closed system the total) momentum before', 6, route='side-a', note_sel=LEGEND),
       pt(S('// m₁u₁', piece=2, psep='//'), 6, route='side-b', note=PB(3))],
      'phys-1-2', 'conservation-of-momentum', SQ(12, 'State the principle of conservation of momentum.'), 6,
      id='phys-2021-ol-q7-ii',
      decision='The scheme prints the principle in words and, after "//", as an equation: routes inside the card, '
               'each 6.'),
    T('7iii', 'Q7(iii)', 'B', P(6, 'Explain why Newton’s second law of motion is consistent with the principle of',
                               'conservation of momentum.'),
      [anyn(S('no force acting implies no change in momentum'), 1, 4, sep='//', note=PB(2))], 'phys-1-2',
      'newtons-second-law-and-momentum',
      SQ(12, 'Explain why Newton’s second law of motion is consistent with the principle of conservation',
         'of momentum.'), 4, id='phys-2021-ol-q7-iii', decision=MENU.format(what='two answers separated by "//"')),
    T('7iv', 'Q7(iv)', 'B', P(6, 'Calculate the momentum of Bagger 293 when it is moving at its maximum speed.'),
      [R('(mv = (14200', 6, note=PB(3))], 'phys-1-2', 'momentum-of-bagger',
      SQ(12, 'Calculate the momentum of Bagger 293 when it is moving at its maximum speed.'), 6, stem=[BAGGER7],
      id='phys-2021-ol-q7-iv'),
    T('7v', 'Q7(v)', 'B', P(6, 'Bagger 293 is moving when it picks up a stationary load of 2700 tonnes.',
                           'Explain your answer.'),
      [R('decrease due to extra mass', 6, note=PB(3))], 'phys-1-2', 'picking-up-a-load',
      SQ(12, 'Bagger 293 is moving when it picks up a stationary load of 2700 tonnes. Would this',
         'Explain your answer.'), 6, stem=[BAGGER7], id='phys-2021-ol-q7-v'),
    T('7vi', 'Q7(vi)', 'B', P(6, 'Calculate the initial momentum of train X.'),
      [R('(mv = (0.133)', 6, note=PB(3))], 'phys-1-2', 'momentum-of-train-x',
      SQ(12, 'Calculate the initial momentum of train X.'), 6, stem=[TRAINS7], id='phys-2021-ol-q7-vi'),
    T('7vii', 'Q7(vii)', 'B', P(6, 'Calculate the speed of the two trains immediately after the collision.'),
      [R('(6.65', 6, **PX(3, 'partial answer e.g. addition of masses'))], 'phys-1-2', 'speed-after-collision',
      SQ(12, 'Calculate the speed of the two trains immediately after the collision.'), 6, stem=[TRAINS7],
      id='phys-2021-ol-q7-vii'),
    T('7viii', 'Q7(viii)', 'B', P(6, 'In which direction do the two trains move after the collision?'),
      [anyn(S('to the right // in the same direction as the moving train'), 1, 4, sep='//')], 'phys-1-2',
      'direction-after-collision', SQ(12, 'In which direction do the two trains move after the collision?'), 4,
      stem=[TRAINS7], id='phys-2021-ol-q7-viii', decision=MENU.format(what='two answers separated by "//"')),
    T('7ix', 'Q7(ix)', 'B', P(6, 'Calculate the loss in kinetic energy during this collision.'),
      [G('fraction', page=12, clip=(108, 622, 318, 644), expect='KE before = ½ (0.133)(0.05)² = 1.66 × 10⁻⁴ J',
         marks=3),
       G('fraction', page=12, clip=(108, 640, 320, 662), expect='KE after = ½ (0.179)(0.037)² = 1.22 × 10⁻⁴ J',
         marks=3),
       R('kinetic energy lost', 3, note=PB(3))], 'phys-1-4', 'kinetic-energy-lost',
      SQ(12, 'Calculate the loss in kinetic energy during this collision.'), 9, stem=[TRAINS7],
      id='phys-2021-ol-q7-ix'),
    T('7x', 'Q7(x)', 'B', P(6, 'What happened to the kinetic energy that was lost in the collision?'),
      [anyn(S('converted into heat // converted into other forms'), 1, 3, sep='//')], 'phys-1-4',
      'where-the-energy-went', SQ(12, 'What happened to the kinetic energy that was lost in the collision?'), 3,
      stem=[TRAINS7], id='phys-2021-ol-q7-x', decision=MENU.format(what='two answers separated by "//"')),
    # ---------------------------------------------------------------- Q8 --
    T('8i', 'Q8(i)', 'B', P(7, 'Describe an experiment to show that sound waves need a', 'medium to travel through.'),
      [anyn(None, 2, 3, note='The scheme prints "any two" (2 × 3) against the apparatus line.',
            options=pieces('apparatus: bell jar with electric bell, battery, vacuum pump', (1, 2, 3), first=': ')),
       R('procedure: turn on pump', 3),
       R('observation/conclusion: no sound heard when air removed / sound needs a medium', 3,
         note_sel=S('accept valid alternatives'))],
      'phys-2-5', 'sound-needs-a-medium',
      SQ(13, 'Describe an experiment to show that sound waves need a medium to travel through.'), 12,
      id='phys-2021-ol-q8-i',
      cells='The apparatus line\'s cell "2 × 3" is printed with a multiplication sign the text layer drops ("2  3", '
            'two bare numbers), so the reader does not take it for a cell; the rendered page p13 prints "2 × 3" at the '
            'margin.'),
    T('8ii', 'Q8(ii)', 'B', P(7, 'What type of waves do not need a medium to travel through?'),
      [R('light / electromagnetic', 4)], 'phys-2-4', 'waves-without-a-medium',
      SQ(13, 'What type of waves do not need a medium to travel through?'), 4, id='phys-2021-ol-q8-ii'),
    T('8iii', 'Q8(iii)', 'B', P(7, 'Waves can be classified as either transverse or longitudinal.',
                               '(A labelled diagram may help your answer.)'),
      [R('the disturbance is parallel to the direction of motion for longitudinal waves', 3),
       R('the disturbance is perpendicular to the direction of motion for transverse waves', 3,
         note_sel=S('partial answer e.g. longitudinal waves need a medium'))],
      'phys-2-2', 'transverse-and-longitudinal',
      SQ(13, 'Waves can be classified as either transverse or longitudinal. Distinguish between',
         '(A labelled diagram may help your answer.)'), 6, id='phys-2021-ol-q8-iii'),
    T('8iv', 'Q8(iv)', 'B', P(7, 'The frequency of a certain radio station is 107 MHz.',
                             'Calculate the speed of the radio waves.'),
      [R('(v = f', 6, note=PB(3))], 'phys-2-2', 'speed-of-radio-waves',
      SQ(13, 'The frequency of a certain radio station is 107 MHz. It broadcasts waves of',
         'Calculate the speed of the radio waves.'), 6, id='phys-2021-ol-q8-iv'),
    T('8v', 'Q8(v)', 'B', P(7, 'Describe one example of the reflection of sound waves.'),
      [R('(When sound is reflected from a distant obstacle it produces) an echo', 4)], 'phys-2-5', 'echo',
      SQ(13, 'Describe one example of the reflection of sound waves.'), 4, id='phys-2021-ol-q8-v'),
    T('8vi', 'Q8(vi)', 'B', P(7, 'Light strikes a glass block with an angle of incidence of 23°.',
                             'Calculate the refractive index of the glass.'),
      [G('fraction', page=13, clip=(108, 453, 245, 477), expect='(n= sini/(sinr) = 0.3907/0.2588 = ) 1.51', marks=6,
         note=PB(3))], 'phys-2-3', 'refractive-index',
      SQ(13, 'Light strikes a glass block with an angle of incidence of 23°. The light undergoes refraction',
         'refractive index of the glass.'), 6, id='phys-2021-ol-q8-vi'),
    T('8vii', 'Q8(vii)', 'B', P(7, 'The wave fronts shown below diffract as they pass through the gap.',
                               'undergoing diffraction.'),
      [R('diagram to show: waves spreading out from the slit', 6, note=PB(3))], 'phys-2-3', 'diffraction-at-a-gap',
      SQ(13, 'The wave fronts shown below diffract as they pass through the gap.'), 6, qfig='q8vii-question',
      fig='q8vii-scheme', id='phys-2021-ol-q8-vii',
      decision='The ask is to complete the printed diagram: it is shown as printed, the scheme\'s drawing the '
               'solution figure.'),
    T('8viii', 'Q8(viii)', 'B', P(7, 'Describe an experiment to show that sound undergoes interference.'),
      [R('method: e.g. slowly rotate vibrating tuning fork near the ear', 3),
       R('observation/conclusion: e.g. change in loudness due to interference', 3, note=PB(3))], 'phys-2-6',
      'interference-of-sound', SQ(13, 'Describe an experiment to show that sound undergoes interference.'), 6,
      id='phys-2021-ol-q8-viii'),
    T('8ix', 'Q8(ix)', 'B', P(7, 'Light waves undergo polarisation but sound waves do not.',
                             'what is meant by polarisation.'),
      [R('labelled diagram to show the restriction of (transverse) wave vibrations to a single plane', 6,
         note_sel=S('NOTE: no labels deduct 2'), note=PB(3))], 'phys-2-7', 'polarisation',
      SQ(13, 'Light waves undergo polarisation but sound waves do not.', 'what is meant by polarisation.'), 6,
      id='phys-2021-ol-q8-ix'),
    # ---------------------------------------------------------------- Q9 --
    T('9i', 'Q9(i)', 'B', P(8, 'Define resistance.'),
      [G('fraction', page=14, clip=(108, 119, 140, 142), expect='R = V/I', marks=6, note=PB(3))], 'phys-3-3',
      'resistance', SQ(14, 'Define resistance.'), 6, id='phys-2021-ol-q9-i'),
    T('9ii', 'Q9(ii)', 'B', P(8, 'Name the instrument used to measure resistance.'),
      [R('ohmmeter', 6, **PX(3, 'partial answer e.g. multimeter'))], 'phys-3-3', 'measuring-resistance',
      SQ(14, 'Name the instrument used to measure resistance.'), 6, id='phys-2021-ol-q9-ii'),
    T('9iii', 'Q9(iii)', 'B', P(8, 'State the relationship between resistance and length.'),
      [R('R ∝ l / proportional', 6, note=PB(3))], 'phys-3-3', 'resistance-and-length',
      SQ(14, 'State the relationship between resistance and length.'), 6, stem=[RHEOSTAT9], fig='q9-rheostat',
      id='phys-2021-ol-q9iii-fig'),
    T('9iv', 'Q9(iv)', 'B', P(8, 'Calculate the circular cross', 'sectional area of the wire.'),
      [R('(A=', 6, note=PB(3))], 'phys-3-3', 'cross-sectional-area',
      SQ(14, 'Calculate the circular cross-sectional area of the wire.'), 6, stem=[WIRE9],
      id='phys-2021-ol-q9-iv-v', decision=bundled('(iv) and (v)', '(iv)')),
    T('9v', 'Q9(v)', 'B', P(8, 'Calculate the resistance of the wire.'),
      [G('fraction', page=14, clip=(108, 368, 275, 393),
         expect='(R= ρl/A = ((1.1 ×10⁻⁶)(4.8))/(1.2566×10⁻⁷) = ) 42 Ω', marks=6, note=PB(3))],
      'phys-3-3', 'resistance-of-wire', SQ(14, 'Calculate the resistance of the wire.'), 6, stem=[WIRE9]),
    T('9vi', 'Q9(vi)', 'B', P(8, 'Show that the combined resistance of the', 'is 1.05 Ω.'),
      [G('fraction', page=14, clip=(108, 447, 280, 470), expect='( 1/R = ⅕ + ½ + ¼ = 19/20 ⇒) R= 1.05 Ω',
         marks=6, **PX(3, 'partial answer e.g. correct equation'))], 'phys-3-3', 'resistors-in-parallel',
      SQ(14, 'Show that the combined resistance of the three resistors in parallel', 'is 1.05 Ω.'), 6,
      stem=[CIRCUIT9], fig='q9-circuit', decision='The bank had left this part open.'),
    T('9vii', 'Q9(vii)', 'B', P(8, 'Calculate the total resistance in the circuit.'),
      [R('RT = 3', 6, note=PB(3))], 'phys-3-3', 'total-resistance',
      SQ(14, 'Calculate the total resistance in the circuit.'), 6, stem=[CIRCUIT9], fig='q9-circuit',
      decision='The bank had left this part open.'),
    T('9viii', 'Q9(viii)', 'B', P(8, 'Calculate the current flowing through the', 'ammeter, A.'),
      [G('fraction', page=14, clip=(108, 540, 230, 564), expect='(I= V/R = 12/4.05 =) 2.96 A', marks=6, note=PB(3))],
      'phys-3-3', 'current-through-ammeter', SQ(14, 'Calculate the total current flowing through the ammeter, A.',
                                                paired='The scheme reprints "the total current"; the paper prints '
                                                       '"the current".'), 6,
      stem=[CIRCUIT9], fig='q9-circuit', decision='The bank had left this part open.'),
    T('9ix', 'Q9(ix)', 'B', P(8, 'The wire labelled P is yellow and green.', 'What is the function of this wire?'),
      [R('safety/ earth (the equipment)', 4)], 'phys-3-3', 'earth-wire',
      SQ(14, 'The wire labelled P is yellow and green. What is the function of this wire?'), 4, stem=[PLUG9],
      fig='physics-2021-ol-paper-p008-i1', labels=[L('P', S('safety/ earth (the equipment)', page=14), True)],
      id='phys-2021-ol-q9-ix',
      decision='The card keeps its figure, the paper\'s labelled plug (opened and checked).'),
    T('9x', 'Q9(x)', 'B', P(8, 'Name the wire labelled Q.'),
      [R('live', 4, **PX(2, 'partial answer e.g. brown'))], 'phys-3-3', 'live-wire',
      SQ(14, 'Name the wire labelled Q.'), 4, stem=[PLUG9], fig='physics-2021-ol-paper-p008-i1',
      labels=[L('Q', S('live', page=14), True)], id='phys-2021-ol-q9x-fig',
      decision='The card keeps its figure, the paper\'s labelled plug (opened and checked).'),
    # ---------------------------------------------------------------- Q10 --
    T('10i', 'Q10(i)', 'B', P(9, 'Describe how a periscope works.', 'through the periscope.'),
      [R('diagram showing incident ray, two reflections and emerging ray', 10,
         note_sel=S('Note: no labels deduct 2, no diagram maximum mark 7'),
         note='The scheme gives (7) for "one error" and (4) for a partial answer.')],
      'phys-2-3', 'how-a-periscope-works', SQ(15, 'Describe how a periscope works.', 'through the periscope.'), 10,
      stem=[PERISCOPE10], id='phys-2021-ol-q10-i',
      cells='The "(7)" printed against "one error" is the mark given instead of the 10 when the diagram has one error, '
            'not added to it.'),
    T('10ii', 'Q10(ii)', 'B', P(9, 'State the laws of reflection of light.'),
      [R('the incident ray, the normal and the reflected ray are in the same plane', 3),
       R('the angle of incidence is equal to the angle of reflection', 3, note=PB(3))], 'phys-2-3',
      'laws-of-reflection', SQ(15, 'State the laws of reflection of light.'), 6, id='phys-2021-ol-q10-ii'),
    T('10iii', 'Q10(iii)', 'B', P(9, 'Describe an experiment to demonstrate the laws of reflection.'),
      [anyn(None, 2, 3, note='The scheme prints "any two (2 × 3)" against the apparatus line, and "any one (3)".',
            options=pieces('apparatus: plane mirror, sheet of paper, raybox / pins, protractor', (1, 2, 3, 4),
                           first=': ')),
       R('procedure: draw the incident ray, normal and reflected ray // measure I and r', 3, note_sel=LEGEND),
       R('observation / conclusion: the angle of incidence is always equal to the angle of reflection', 3)],
      'phys-2-3', 'laws-of-reflection-experiment',
      SQ(15, 'Describe an experiment to demonstrate the laws of reflection.'), 12, id='phys-2021-ol-q10-iii',
      cells='"any one (3)" is the mark for the apparatus when only one item is given, instead of the "any two '
            '(2 × 3)", not added to it.'),
    T('10iv', 'Q10(iv)', 'B', P(9, 'Copy the ray diagram below into your answerbook and complete it to show how a real',
                               'concave mirror.'),
      [R('correct diagram showing two', 10, end='correct rays and an inverted image',
         note='The scheme gives (7) for "one error" and (4) for a partial answer.')],
      'phys-2-3', 'real-image-in-concave-mirror',
      SQ(15, 'Copy the ray diagram below into your answerbook and complete it to show how a real', 'concave mirror.'),
      10, qfig='q10iv-question', fig='q10iv-scheme',
      decision='The bank had left this part open. The ask is to complete the printed diagram: it is shown as printed, '
               'the scheme\'s drawing the solution figure.'),
    T('10v', 'Q10(v)', 'B', P(9, 'Calculate the magnification.'),
      [G('fraction', page=15, clip=(108, 583, 172, 606), expect='(M = v/u =) 3/2', marks=6, note=PB(3))],
      'phys-2-3', 'magnification', SQ(15, 'Calculate the magnification.'), 6, stem=OBJECT10, id='phys-2021-ol-q10-v'),
    T('10vi', 'Q10(vi)', 'B', P(9, 'Calculate the image distance.'),
      [G('fraction', page=15, clip=(108, 635, 340, 658), expect='( v/u = 3/2 ⟹v= 1.5u= (1.5)(17) = ) 25.5 cm',
         marks=6, note=PB(3))], 'phys-2-3', 'image-distance', SQ(15, 'Calculate the image distance.'), 6,
      stem=OBJECT10, id='phys-2021-ol-q10-vi', source_pages=[9],
      decision=LINKED.format(w='"the image distance"', why='it is the image the mirror forms, and the paper prints '
                                                           'no figure for it')),
    T('10vii', 'Q10(vii)', 'B', P(9, 'State one use of a concave mirror.'),
      [anyn(None, 1, 3, open_list=True, options=pieces('cosmetics, shaving mirror, dentist, etc.', (1, 2, 3)))],
      'phys-2-3', 'use-of-concave-mirror', SQ(15, 'State one use of a concave mirror.'), 3,
      id='phys-2021-ol-q10-vii-viii', decision=bundled('(vii) and (viii)', '(vii)') + ' ' +
                                               MENU.format(what='three uses, then "etc."')),
    T('10viii', 'Q10(viii)', 'B', P(9, 'State one use of a convex mirror.'),
      [anyn(None, 1, 3, open_list=True,
            options=pieces('car mirror, security mirror in shops, road reflectors, etc.', (1, 2, 3)))],
      'phys-2-3', 'use-of-convex-mirror', SQ(15, 'State one use of a convex mirror.'), 3,
      decision=MENU.format(what='three uses, then "etc."')),
    # ---------------------------------------------------------------- Q11 --
    T('11i', 'Q11(i)', 'B', P(10, 'Heat may be transferred by radiation and by conduction.', 'may be transferred.'),
      [R('convection', 3)], 'phys-2-1', 'convection',
      SQ(16, 'Heat may be transferred by radiation and by conduction. Name the other way in which heat',
         'may be transferred.'), 3, id='phys-2021-ol-q11-i'),
    T('11ii', 'Q11(ii)', 'B', P(10, 'Distinguish between heat and temperature.'),
      [R('heat is a measure of the energy in a body while temperature is a degree of hotness', 6, note=PB(3))],
      'phys-2-1', 'heat-and-temperature', SQ(16, 'Distinguish between heat and temperature.'), 6,
      id='phys-2021-ol-q11-ii'),
    T('11iii', 'Q11(iii)', 'B', P(10, 'Convert the normal human body temperature from degrees Celcius (°C) into kelvin (K).'),
      [R('(37 °C', 6, **PX(3, 'partial answer e.g. 37-273'))], 'phys-2-1', 'body-temperature-in-kelvin',
      SQ(16, 'Convert the normal human body temperature from degrees Celsius (°C) into kelvin (K).'), 6,
      stem=[TEMP11], id='phys-2021-ol-q11-iii'),
    T('11iv', 'Q11(iv)', 'B', P(10, 'Thermometers are designed to make use of thermometric properties.',
                               'What is a thermometric property?'),
      [R('(measurable) property which changes with temperature change', 6, note=PB(3))], 'phys-2-1',
      'thermometric-property',
      SQ(16, 'Thermometers are designed to make use of thermometric properties. What is a', 'thermometric property?'),
      6, id='phys-2021-ol-q11-iv-v', decision=bundled('(iv) and (v)', '(iv)')),
    T('11v', 'Q11(v)', 'B', P(10, 'State one example of a thermometric property.'),
      [anyn(None, 1, 3, open_list=True, note_sel=S('any one'),
            options=pieces('colour, voltage, volume, pressure, resistance, etc.', (1, 2, 3, 4, 5)))],
      'phys-2-1', 'example-of-thermometric-property', SQ(16, 'State one example of a thermometric property.'), 3,
      decision=MENU.format(what='five properties, then "etc."')),
    T('11vi', 'Q11(vi)', 'B', P(10, 'Two thermometers may not give the same reading for a person’s temperature, even',
                               'Explain why this is the case.'),
      [R('different thermometric properties behave differently with changing temperature', 4, note=PB(2))],
      'phys-2-1', 'thermometers-disagree',
      SQ(16, 'Two thermometers may not give the same reading for a person’s temperature, even',
         'Explain why this is the case.'), 4, id='phys-2021-ol-q11-vi'),
    T('11vii', 'Q11(vii)', 'B', P(10, 'Calculate the area of the garden.'),
      [R('(A=(6)(9)', 4)], 'phys-2-4', 'area-of-garden', SQ(16, 'Calculate the area of the garden.'), 4,
      stem=[GARDEN11], fig='q11-garden', id='phys-2021-ol-q11-vii',
      decision='The bank had left this part open (its old card named a figure that was never cropped). The garden '
               'diagram is cropped from the paper.'),
    T('11viii', 'Q11(viii)', 'B', P(10, 'Calculate how many seconds there are in 12 hours.'),
      [R('((12)(60)(60)', 3)], 'phys-2-4', 'seconds-in-12-hours',
      SQ(16, 'Calculate how many seconds there are in 12 hours.'), 3, id='phys-2021-ol-q11-viii'),
    T('11ix', 'Q11(ix)', 'B', P(10, 'Calculate how much energy will fall on the garden in the 12 hours.'),
      [R('E=(1.36', 6, note=PB(3))], 'phys-2-4', 'solar-energy-on-garden',
      SQ(16, 'Calculate how much energy will fall on the garden in the 12 hours.'), 6, stem=[SOLAR11, GARDEN11],
      fig='q11-garden', id='phys-2021-ol-q11-ix'),
    T('11x', 'Q11(x)', 'B', P(10, 'Heat is transferred at different rates depending on the material it is moving through.',
                             'compare the rate of conduction through different solids.'),
      [C('apparatus', 3), C('method', 3), C('observation/conclusion', 3, note=CRIT + ' ' + PB(3))], 'phys-2-1',
      'comparing-conduction',
      SQ(16, 'Heat is transferred at different rates depending on the material it is moving through.',
         'compare the rate of conduction through different solids.'), 9,
      decision='The bank had excluded this part. ' + EXPT),
    T('11xi', 'Q11(xi)', 'B', P(10, 'U−value is a measure of the rate of heat loss through walls and windows.',
                               'Describe two ways of reducing heat loss from a building.'),
      [R('Insulation and double glazing', 6, note=PB(3))], 'phys-2-1', 'reducing-heat-loss',
      SQ(16, 'U−value is a measure of the rate of heat loss through walls and windows.',
         'Describe two ways of reducing heat loss from a building.'), 6, id='phys-2021-ol-q11-xi',
      decision='The scheme prices the two ways together (6): one row at its price.'),
    # ---------------------------------------------------------------- Q12 --
    T('12i', 'Q12(i)', 'B', P(11, 'What is nuclear fission?'),
      [R('splitting up of a nucleus ( into two parts) with the emission of particles /energy', 6, note=PB(3))],
      'phys-4-6', 'nuclear-fission', SQ(17, 'What is nuclear fission?'), 6, id='phys-2021-ol-q12-i'),
    T('12ii', 'Q12(ii)', 'B', P(11, 'What is the function of the control rods in a fission reactor?'),
      [anyn(S('absorb neutrons // slow down the rate of fission/reaction'), 1, 6, sep='//', note=PB(3))], 'phys-4-6',
      'control-rods', SQ(17, 'What is the function of the control rods in a fission reactor?'), 6,
      id='phys-2021-ol-q12-ii', decision=MENU.format(what='two answers separated by "//"')),
    T('12iii', 'Q12(iii)', 'B', P(11, 'A fission reactor is surrounded by shielding.', 'What material is used as shielding?'),
      [R('protection / safety /prevent radiation escaping', 3), R('lead / concrete', 3)], 'phys-4-6', 'shielding',
      SQ(17, 'A fission reactor is surrounded by shielding. What is the purpose of the shielding?',
         'What material is used as shielding?'), 6, id='phys-2021-ol-q12-iii'),
    T('12iv', 'Q12(iv)', 'B', P(11, 'State one disadvantage of nuclear fission.'),
      [R('radioactive waste/ explosions/nuclear accidents', 6, note=PB(3))], 'phys-4-6', 'disadvantage-of-fission',
      SQ(17, 'State one disadvantage of nuclear fission.'), 6, id='phys-2021-ol-q12-iv'),
    T('12v', 'Q12(v)', 'B', P(11, 'How many electrons are in an atom of Mt?', 'Tables booklet.)'),
      [G('equation', page=17, clip=(108, 380, 235, 401), expect='(Mt²⁶⁸₁₀₉ = ) 109 electrons', marks=4)],
      'phys-4-4', 'electrons-in-meitnerium',
      SQ(17, 'How many electrons are in an atom of Mt? (Refer to page 79 of the Formulae and Tables', 'booklet.)'), 4,
      stem=[MT12], id='phys-2021-ol-q12-v',
      decision='The scheme sets the nuclide in CambriaMath with its numbers stacked after the symbol: read from where '
               'they are printed.'),
    T('12vi', 'Q12(vi)', 'B', P(11, 'What is meant by radioactivity?'),
      [R('(spontaneous) emission of (alpha and beta particles and gamma) rays from unstable nuclei', 6, note=PB(3))],
      'phys-4-4', 'radioactivity', SQ(17, 'What is meant by radioactivity?'), 6, stem=[CURIE12],
      id='phys-2021-ol-q12-vi'),
    T('12vii', 'Q12(vii)', 'B', P(11, 'Which type of nuclear radiation is the most penetrating?'),
      [R('gamma', 4)], 'phys-4-4', 'most-penetrating-radiation',
      SQ(17, 'Which type of nuclear radiation is the most penetrating?'), 4, stem=[THREE12],
      id='phys-2021-ol-q12-vii'),
    T('12viii', 'Q12(viii)', 'B', P(11, 'Describe an experiment to compare the penetrating power of the three types of',
                                   'nuclear radiation.'),
      [R('apparatus: radioactive sources, barriers, detector/GM tube', 3, end='any two'),
       R('procedure: place different barriers between the sources and the detector', 3),
       R('observation/conclusion: alpha is stopped first // gamma penetrates best', 3, note_sel=LEGEND)],
      'phys-4-4', 'penetrating-power-experiment',
      SQ(17, 'Describe an experiment to compare the penetrating power of the three types of nuclear', 'radiation.'), 9,
      stem=[THREE12], id='phys-2021-ol-q12-viii',
      decision='The scheme prices "any two" of the apparatus together (3): one row at its price.'),
    T('12ix', 'Q12(ix)', 'B', P(11, 'What are isotopes?'),
      [R('atoms of the same element with different numbers of neutrons', 6, **PX(3, 'partial answer e.g. named isotope'))],
      'phys-4-4', 'isotopes', SQ(17, 'What are isotopes?'), 6, id='phys-2021-ol-q12-ix'),
    T('12x', 'Q12(x)', 'B', P(11, 'One isotope of curium is Cm', 'How many neutrons are in this isotope?'),
      [R('(247', 3)], 'phys-4-4', 'neutrons-in-curium-247', SQ(17, 'One isotope of curium is Cm'), 3,
      qfig='q12x-question', id='phys-2021-ol-q12-x',
      decision='The paper sets the nuclide with its numbers stacked after the symbol, which the text layer splits '
               'across two lines: the ask is shown as printed.'),
    # ---------------------------------------------------------------- Q13 --
    T('13a', 'Q13(a)', 'B', P(12, 'What did Millikan determine with his 1909 oil drop experiment?'),
      [R('size of the charge on an electron/there was a smallest unit charge', 7)], 'phys-4-1',
      'what-millikan-determined', SQ(18, 'What did Millikan determine with his 1909 oil drop experiment?'), 7,
      id='phys-2021-ol-q13-a'),
    T('13b', 'Q13(b)', 'B', P(12, 'What is the size of the charge on one electron?'),
      [R('1.6 ×', 7)], 'phys-4-1', 'charge-on-electron', SQ(18, 'What is the size of the charge on one electron?'), 7,
      id='phys-2021-ol-q13-b'),
    T('13c', 'Q13(c)', 'B', P(12, 'X‐rays are made by accelerating electrons', 'produced in an X‐ray tube?'),
      [anyn(S('thermionic emission // hot cathode'), 1, 7, sep='//', note=PB(4))], 'phys-4-2',
      'electrons-in-x-ray-tube', SQ(18, 'X-rays are made by accelerating electrons across an X-ray tube. How are the electrons',
                                    'produced in an X-ray tube?'), 7, id='phys-2021-ol-q13-c',
      decision=MENU.format(what='two answers separated by "//"')),
    T('13d', 'Q13(d)', 'B', P(12, 'A drop has a volume of 2.03 × 10⁻¹⁷ m³ and a density of 886 kg m⁻³.', 'mass of the drop.'),
      [R('(M = ρV', 7, note=PB(4))], 'phys-4-1', 'mass-of-oil-drop',
      SQ(18, 'A drop has a volume of 2.03 × 10⁻¹⁷ m³ and a density of 886 kg m⁻³. Calculate the mass',
         'of the drop.'), 7, id='phys-2021-ol-q13-d'),
    T('13e', 'Q13(e)', 'B', P(12, 'Draw the circuit symbol for a battery.'),
      [drawn(7, 'The scheme draws the symbol (shown at the reveal) and prices it 7; it prints no words for it. It '
                'gives (4) for "partial answer e.g. capacitor //supply symbol".')],
      'phys-3-3', 'battery-symbol', SQ(18, 'Draw the circuit symbol for a battery.'), 7, fig='q13e-scheme',
      decision='The bank had excluded this part. The scheme draws its answer and names it in no words: one drawn row '
               'restating the ask at its 7, the scheme\'s drawing the solution figure.'),
    T('13f', 'Q13(f)', 'B', P(12, 'In the oil drop experiment, Millikan applied an electric field between the plates until',
                             'What is an electric field?'),
      [R('region/space around a charge in which another charged particle will experience a force', 7, note=PB(4))],
      'phys-3-2', 'electric-field',
      SQ(18, 'In the oil drop experiment, Millikan applied an electric field between the plates until the',
         'What is an electric field?'), 7, id='phys-2021-ol-q13-f'),
    T('13g', 'Q13(g)', 'B', P(12, 'Sketch the electric field that is formed between two oppositely charged parallel',
                             'plates.'),
      [C('correct diagram', 7, note=CRIT + ' ' + PB(4))], 'phys-3-2', 'field-between-plates',
      SQ(18, 'Sketch the electric field that is formed between two oppositely charged parallel plates.'), 7,
      fig='q13g-scheme',
      decision='The bank had excluded this part. The scheme prices "correct diagram" and draws it: one criterion row '
               'in its words, the drawing the solution figure.'),
    T('13h', 'Q13(h)', 'B', P(12, 'Show the forces acting on the drop when it is not moving up or down.'),
      [R('labelled diagram to show electric force acting up and gravity down', 7, note=PB(4))], 'phys-1-2',
      'forces-on-oil-drop', SQ(18, 'Show the forces acting on the drop when it is not moving up or down.'), 7,
      id='phys-2021-ol-q13h'),
    # ---------------------------------------------------------------- Q14 --
    T('14ai', 'Q14(a)(i)', 'B', P(13, 'The rocket was visible in Irish skies 15 minutes after',
                                 'during this part of the journey.'),
      [G('fraction', page=19, clip=(136, 168, 292, 193), expect='(v= s/t = (6484 ×10³)/((15)(60)) =) 7.2 km s⁻¹',
         marks=6, note=PB(3))], 'phys-1-1', 'average-speed-of-rocket',
      SQ(19, 'The rocket was visible in Irish skies 15 minutes after take-off. At that time it had',
         'of the journey.'), 6, stem=[FALCON14], id='phys-2021-ol-q14a-i'),
    T('14aii', 'Q14(a)(ii)', 'B', P(13, 'The rocket later docked on the ISS.', 'complete each day?'),
      [G('fraction', page=19, clip=(136, 249, 342, 273), expect='(number of orbits = (24)(60)/93 = 15.48 = ) 15',
         marks=6, note=PB(3))], 'phys-1-5', 'orbits-per-day',
      SQ(19, 'The rocket later docked on the ISS. The ISS orbits the Earth every 93 minutes.', 'complete each day?'),
      6, stem=[FALCON14], id='phys-2021-ol-q14a-ii'),
    T('14aiii', 'Q14(a)(iii)', 'B', P(13, 'Newton’s law of universal gravitation describes the force of attraction between',
                                     'State Newton’s law of universal gravitation.'),
      [R('Force of attraction between two point masses is proportional to the product of the', 6,
         end='square of the distance between them', route='side-a', note_sel=LEGEND),
       G('fraction', page=19, clip=(136, 352, 212, 380), expect='// F∝ m₁m₂/d²', marks=6, route='side-b'),
       G('fraction', page=19, clip=(212, 352, 300, 380), expect='//F= G m₁m₂/d²', marks=6, route='side-c',
         note=PB(3))],
      'phys-1-5', 'universal-gravitation',
      SQ(19, 'Newton’s law of universal gravitation describes the force of attraction between',
         'State Newton’s law of universal gravitation.'), 6, id='phys-2021-ol-q14a-iii',
      decision='The scheme prints the law in words and, after "//", as two formulae: routes inside the card, each 6; '
               'the formulae are read from where the scheme prints their fractions.'),
    T('14aiv', 'Q14(a)(iv)', 'B', P(13, 'Calculate the astronaut’s weight on Earth.'),
      [R('(weight = mg', 4, note=PB(2))], 'phys-1-5', 'weight-on-earth',
      SQ(19, 'Calculate the astronaut’s weight on Earth.'), 4, stem=[ISS14, G14], id='phys-2021-ol-q14a-iv-vi',
      decision=bundled('(iv), (v) and (vi)', '(iv)')),
    T('14av', 'Q14(a)(v)', 'B', P(13, 'What is the astronaut’s mass at the altitude of the ISS?'),
      [R('(mass does not change) 85 kg', 3)], 'phys-1-5', 'mass-at-altitude',
      SQ(19, 'What is the astronaut’s mass at the altitude of the ISS?'), 3, stem=[ISS14]),
    T('14avi', 'Q14(a)(vi)', 'B', P(13, 'Calculate the astronaut’s weight at the altitude of the ISS.'),
      [R('((0.9)(833)', 3)], 'phys-1-5', 'weight-at-altitude',
      SQ(19, 'Calculate the astronaut’s weight at the altitude of the ISS.'), 3, stem=[ISS14, G14]),
    T('14bi', 'Q14(b)(i)', 'B', P(13, 'As charge builds up on a cloud, the cloud induces a charge on objects on Earth.',
                                 '(A labelled diagram may help your answer.)'),
      [R('a charged object A is brought near to', 10, end='object B is then earthed.',
         note='The scheme gives 10 for "three lines correct", (7) for "two lines correct" and (4) for a partial answer; '
              'marks may be obtained from a diagram.')],
      'phys-3-1', 'charging-by-induction',
      SQ(20, 'As charge builds up on a cloud, the cloud induces a charge on objects on Earth. Explain',
         '(A labelled diagram may help your answer.)'), 10, stem=[LIGHTNING14], fig='q14bi-scheme',
      id='phys-2021-ol-q14b-i',
      decision='The scheme prices its three lines together ("three lines correct 10"): one row at its price; its '
               'drawing of objects A and B is the solution figure.'),
    T('14bii', 'Q14(b)(ii)', 'B', P(13, 'Calculate the power generated when lightning', 'discharges.'),
      [G('fraction', page=20, clip=(136, 373, 292, 398), expect='(P= E/t = (0.9 ×10⁹)/(3 × 10⁻⁴) =) 3× 10¹² W', marks=6,
         note=PB(3))], 'phys-1-4', 'power-of-lightning',
      SQ(20, 'Calculate the power generated when lightning discharges.'), 6, stem=[STATIC14],
      id='phys-2021-ol-q14b-ii'),
    T('14biii', 'Q14(b)(iii)', 'B', P(13, 'Draw a diagram to show the distribution of charge', 'conductor.'),
      [R('diagram showing more concentration at point', 6, note=PB(3))], 'phys-3-1', 'charge-on-pear-shaped-conductor',
      SQ(20, 'Draw a diagram to show the distribution of charge', 'conductor'), 6, fig='q14biii-scheme',
      id='phys-2021-ol-q14b-iii-fig',
      decision='The scheme draws its diagram beside the row (the solution figure).'),
    T('14biv', 'Q14(b)(iv)', 'B', P(13, 'Describe an experiment to show that static charge', 'outside of a metal object.'),
      [R('apparatus: e.g. charged hollow conductor, proof plane, GLE', 2),
       R('procedure: e.g. touch the proof plane against the inside of the charged conductor and', 2,
         end='the charged conductor.'),
       R('observation/conclusion: the leaf of the GLE deflects/moves when the proof plane was', 2,
         end='but not the inside.')],
      'phys-3-1', 'charge-on-the-outside',
      SQ(20, 'Describe an experiment to show that static charge accumulates on the outside', 'of a metal object.'), 6,
      id='phys-2021-ol-q14b-iv'),
    T('14ci', 'Q14(c)(i)', 'B', P(14, 'What is a magnetic field?'),
      [R('region/space around a magnet where magnetic forces act', 6, note=PB(3))], 'phys-3-4', 'magnetic-field',
      SQ(21, 'What is a magnetic field?'), 6, stem=[MAGNET14], id='phys-2021-ol-q14c-i'),
    T('14cii', 'Q14(c)(ii)', 'B', P(14, 'Describe an experiment to plot the magnetic field around a bar magnet.'),
      [R('apparatus: magnet, plotting) compass / iron filings', 2),
       R('procedure: use the apparatus to locate the field lines e.g. (place the compass on', 2,
         end='// sprinkle filings', note_sel=LEGEND),
       R('observation/conclusion: join the dots/ show field lines / lines go from north to south/', 2,
         end='// tap filings', note_sel=S('marks may be obtained from a diagram'))],
      'phys-3-4', 'plotting-a-magnetic-field',
      SQ(21, 'Describe an experiment to plot the magnetic field around a bar magnet.'), 6, id='phys-2021-ol-q14c-ii',
      decision='Each line printed with its "//" side (compass // filings): one row per line, as printed, with the '
               'scheme\'s own "//" rule.'),
    T('14ciii', 'Q14(c)(iii)', 'B', P(14, 'Draw a diagram to show the magnetic field around a current', 'conductor.'),
      [C('correct diagram', 6, note=CRIT + ' ' + PB(3))], 'phys-3-4', 'field-around-a-conductor',
      SQ(21, 'Draw a diagram to show the magnetic field around a current-carrying conductor.'), 6,
      fig='q14ciii-scheme',
      decision='The bank had excluded this part. The scheme prices "correct diagram" and draws it: one criterion row '
               'in its words, the drawing the solution figure. (Its "(3)" for a partial answer is printed beside the '
               'drawing\'s label, not on the "partial answer" line.)'),
    T('14civ', 'Q14(c)(iv)', 'B', P(14, 'How could a student show that a current', 'in a magnetic field?'),
      [R('apparatus: current carrying conductor e.g. 6V battery, tin foil, magnet, leads', 2),
       R('procedure: (briefly) connect the circuit', 2),
       R('observation/conclusion: e.g. tin foil moves when magnet is near', 2,
         note_sel=S('marks may be obtained from a diagram'))],
      'phys-3-5', 'force-on-a-conductor',
      SQ(21, 'How could a student show that a current-carrying conductor experiences a',
         'force in a magnetic field?'), 6, id='phys-2021-ol-q14c-iv'),
    T('14cv', 'Q14(c)(v)', 'B', P(14, 'State one use of magnets.'),
      [dict(anyn(None, 1, 4, open_list=True, note='The scheme prints them as "specific use e.g. ...".',
                 options=pieces('specific use e.g. in compass for direction, to seal fridge door, etc', (1, 2),
                                first='e.g. ')),
            **PX(2, 'general use e.g. in radio, cars, etc'))],
      'phys-3-4', 'use-of-magnets', SQ(21, 'State one use of magnets.'), 4, id='phys-2021-ol-q14c-v',
      cells='The "(2)" printed against "general use e.g. in radio, cars, etc" is the mark given instead of the 4 for a '
            'general use, not added to it.',
      decision=MENU.format(what='two specific uses, then "etc"')),
    T('14di', 'Q14(d)(i)', 'B', P(14, 'What is the unit of sound intensity level?'),
      [R('bel / B / decibel / dB', 3)], 'phys-2-5', 'unit-of-sound-intensity-level',
      SQ(22, 'What is the unit of sound intensity level?'), 3, id='phys-2021-ol-q14d-i'),
    T('14dii', 'Q14(d)(ii)', 'B', P(14, 'Resonance is the transfer of energy between two bodies with the same natural',
                                   'Describe an experiment to demonstrate resonance.'),
      [R('apparatus: two objects with the same natural frequency e.g. two mounted tuning forks', 3,
         end='(of the same frequency)'),
       R('procedure: e.g. set one vibrating and bring the other close', 3),
       R('observation/conclusion: energy transfer e.g. the second tuning fork vibrates', 3, note=PB(3))],
      'phys-2-6', 'demonstrating-resonance',
      SQ(22, 'Resonance is the transfer of energy between two bodies with the same natural',
         'Describe an experiment to demonstrate resonance.'), 9, stem=[VIBRATE14], id='phys-2021-ol-q14d-ii'),
    T('14diii', 'Q14(d)(iii)', 'B', P(14, 'A sonometer, shown above, can be used to investigate the relationship between',
                                     'State this relationship.'),
      [anyn(None, 1, 6, note=PB(3),
            options=[S('frequency is inversely proportional to the length', piece=k, psep='//') for k in (1, 2)]
            + [G('fraction', page=22, clip=(410, 343, 440, 366), expect='f∝ 1/l')])],
      'phys-2-6', 'frequency-and-length',
      SQ(22, 'A sonometer, shown above, can be used to investigate the relationship between the',
         'State this relationship.'), 6, fig='q14d-sonometer', id='phys-2021-ol-q14d-iii',
      decision=MENU.format(what='the relationship in words and two formulae, separated by "//",') +
               ' The last is read from where its fraction is printed.'),
    T('14div', 'Q14(d)(iv)', 'B', P(14, 'Calculate the wavelength of the wave.'),
      [R('(λ = 2(0.4)', 6, note=PB(3))], 'phys-2-6', 'wavelength-from-nodes',
      SQ(22, 'Calculate the wavelength of the wave.'), 6, stem=[WAVE14], fig='q14d-wave', id='phys-2021-ol-q14d-iv-fig'),
    T('14dv', 'Q14(d)(v)', 'B', P(14, 'Calculate the frequency of the wave.'),
      [G('fraction', page=22, clip=(136, 583, 256, 607), expect='(f= v/λ = 380/0.8 =) 475 Hz', marks=4, note=PB(2))],
      'phys-2-6', 'frequency-of-wave', SQ(22, 'Calculate the frequency of the wave.'), 4, stem=[WAVE14],
      fig='q14d-wave', id='phys-2021-ol-q14d-v-fig'),
]

ANSWER_VARIANTS = {}
RETAINED = {
    'phys-2021-ol-q6-i': 'Never shipped: the figureless twin of phys-2021-ol-q6i-fig, which carries the reviewed task '
                         'and the X-ray tube photograph.',
    'phys-2021-ol-q9-iii': 'Never shipped: the figureless twin of phys-2021-ol-q9iii-fig, which carries the reviewed '
                           'task and the rheostat photograph.',
    'phys-2021-ol-q9ix-fig': 'Never shipped: a figure twin of phys-2021-ol-q9-ix, which carries the reviewed task and '
                             'the labelled plug.',
    'phys-2021-ol-q14d-iii-fig': 'Never shipped: a figure twin of phys-2021-ol-q14d-iii, which carries the reviewed '
                                 'task and the sonometer photograph.',
    'phys-2021-ol-q14d-iv-v': 'Bundled Q14(d)(iv) and (v), which the scheme prices apart and which are carded on their '
                              'own (phys-2021-ol-q14d-iv-fig, phys-2021-ol-q14d-v-fig).',
}
WITHDRAW = {k: ({'phys-2021-ol-q6-i': 'phys-2021-ol-q6i-fig', 'phys-2021-ol-q9-iii': 'phys-2021-ol-q9iii-fig',
                 'phys-2021-ol-q9ix-fig': 'phys-2021-ol-q9-ix', 'phys-2021-ol-q14d-iii-fig': 'phys-2021-ol-q14d-iii',
                 'phys-2021-ol-q14d-iv-v': 'phys-2021-ol-q14d-iv-fig'}[k], v) for k, v in RETAINED.items()}

P14 = 'indiamart.com; State Examinations Commission (images on page 14)'

FIGURES = {
    # key suffix: (doc, page, rect in PDF points, credit, letters, alt, solution[, masks])
    'q1v-question': ('paper', 2, (80, 380, 545, 421), SEC, [], 'The printed question: (v) From the table, when the distance s is 0.4 m the time t is 0.29 s. Use this data and the formula g = 2s over t squared, set as a fraction, to calculate a value for g.', False),
    'q2iv-question': ('paper', 3, (80, 260, 545, 300), SEC, [], "The printed question: (iv) Boyle's law states that for a fixed mass of gas, pressure is inversely proportional to volume. For each value of V in the table above, calculate 1 over V, set as a fraction, to three decimal places.", False),
    'q2v-question': ('paper', 3, (80, 305, 545, 328), SEC, [], 'The printed question: (v) Plot a graph on graph paper of p against 1 over V, set as a fraction.', False),
    'q2v-scheme-graph': ('scheme', 7, (96, 493, 515, 692), SEC, [], "The marking scheme's graph titled Pressure against 1/Volume: 1/V from 0 to 0.12 on the vertical axis against pressure in kPa from 0 to 250, six points on a straight line through the origin, and red dashed arrows reading 1/V at 140 kPa.",
                         True, [(96, 493, 332, 513)]),
    'q4-calc': ('paper', 4, (60, 335, 540, 430), SEC, [], 'The printed calculation: Heat lost by steam = Heat gained by water and calorimeter; m(steam) l + m(steam) c(water) Δθ(steam) = m(water) c(water) Δθ(water) + m(cal.) c(copper) Δθ(cal.); B × l + B × 4200 × D = A × 4200 × C + 0.0894 × 390 × C; then the specific heat capacities of water (4200 J kg⁻¹ K⁻¹) and copper (390 J kg⁻¹ K⁻¹).', False),
    'q5iv-scheme-graph': ('scheme', 10, (100, 413, 492, 578), SEC, [], "The marking scheme's graph: I / A from 0 to 0.4 on the vertical axis against V / V from 0 to 7, six points on a straight red line through the origin.",
                          True),
    'q6a-question': ('paper', 5, (80, 192, 412, 228), SEC, [], 'The printed question: (a) A student arranges a metre stick so that it is in equilibrium, the word equilibrium underlined. Explain the underlined term.', False),
    'q6f-scheme': ('scheme', 11, (283, 372, 500, 430), SEC, [], "The marking scheme's diagram: a red ray enters an optical fibre drawn as two parallel black lines and zigzags along it, reflecting off each side in turn before leaving at the far end, labelled Light ray and Optic fibre.", True,
                   [(283, 413, 345, 430)]),
    'q6g-question': ('paper', 5, (80, 420, 545, 461), SEC, [], "The printed question: (g) Coulomb's law may be written as F = 1 over 4πε times q₁q₂ over d squared, set as fractions. What do the letters F, q, and d stand for in this expression?", False),
    'q6i-xray': ('paper', 5, (398, 476, 542, 552), 'illustoon.com; orau.org (images on page 5)', [],
                 'Photograph of an X-ray tube: a long glass envelope with a metal electrode assembly inside, a cylinder at one end and a coiled lead at the other.', False),
    'q6k-scheme': ('scheme', 11, (398, 640, 478, 712), SEC, [], "The marking scheme's drawing: a red dot at the centre ringed in green, two dashed circles around it, and blue dots on the circles.", True),
    'q8vii-question': ('paper', 7, (80, 352, 545, 590), SEC, [], 'The printed question: (vii) The wave fronts shown below diffract as they pass through the gap. Copy and complete the diagram to show this wave undergoing diffraction. Below it, four curved grey wave fronts approach a black barrier with a gap in its middle.',
                       False),
    'q8vii-scheme': ('scheme', 13, (112, 520, 158, 592), SEC, [], "The marking scheme's drawing: three vertical black lines, the last with a gap, and three blue semicircular arcs on the far side of the gap, centred on it.",
                     True),
    'q9-rheostat': ('paper', 8, (427, 146, 542, 226),
                    'electronics-tutorials.ws; State Examinations Commission; shutterstock.com (images on page 8)', [],
                    'Photograph of a laboratory rheostat: a coil of wire wound on a tube between two end mounts, with a sliding contact on a bar above it and terminals at the ends.', False),
    'q9-circuit': ('paper', 8, (334, 302, 542, 470), SEC, [], 'Circuit diagram: a 12 V supply and an ammeter A in series with a resistor R₄ = 3 Ω and three resistors in parallel, R₁ = 5 Ω, R₂ = 2 Ω and R₃ = 4 Ω.', False),
    'q10iv-question': ('paper', 9, (80, 224, 545, 420), SEC, [], 'The printed question: (iv) Copy the ray diagram below into your answerbook and complete it to show how a real image is formed in a concave mirror. Below it, an upright arrow labelled Object stands on a dashed principal axis, a point f is marked on the axis, and a curved concave mirror is drawn on the right.',
                       False),
    'q10iv-scheme': ('scheme', 15, (250, 449, 482, 536), SEC, [], 'The marking scheme\'s ray diagram: from the top of the Object arrow a blue ray runs parallel to the axis to the mirror and is reflected back through the point f, and a red ray passes through f to the mirror and is reflected back parallel to the axis; they meet below the axis at the tip of an inverted blue arrow labelled Image.',
                     True, [(250, 449, 274, 491)]),
    'q11-garden': ('paper', 10, (438, 318, 540, 432), SEC, [], 'Diagram of a rectangular garden drawn as a grey rectangle, a dashed arrow above it marked 6 m and a dashed arrow beside it marked 9 m.', False),
    'q12x-question': ('paper', 11, (80, 518, 545, 542), SEC, [], 'The printed question: (x) One isotope of curium is Cm with 247 written above and 96 below after the symbol. How many neutrons are in this isotope? (28)',
                      False),
    'q13e-scheme': ('scheme', 18, (298, 512, 420, 542), SEC, [], "The marking scheme's drawing of a circuit symbol: a pair of long and short parallel plates, a dashed line, and a second pair of long and short plates, with a wire leading out at each end.",
                    True),
    'q13g-scheme': ('scheme', 18, (236, 636, 356, 683), SEC, [], "The marking scheme's drawing: two parallel plates, the left one marked with red plus signs and the right one with red minus signs, joined by straight blue field lines with arrows pointing from the plus plate to the minus plate.",
                    True),
    'q14bi-scheme': ('scheme', 20, (190, 136, 312, 209), SEC, ['A', 'B'],
                     "The marking scheme's drawing: two objects on stands, A on the left with red plus signs around it and B on the right with none.", True),
    'q14biii-scheme': ('scheme', 20, (372, 436.5, 488, 508), SEC, [], "The marking scheme's drawing: a pear-shaped conductor outlined in grey with blue plus signs around it, more of them bunched at the pointed end.",
                       True),
    'q14ciii-scheme': ('scheme', 21, (230, 273, 468, 389), SEC, [], "The marking scheme's drawing: a vertical orange arrow labelled current carrying conductor passes through three dashed concentric ellipses labelled magnetic field, each with an arrowhead showing direction.",
                       True),
    'q14d-sonometer': ('paper', 14, (214, 328, 452, 449), P14, [], 'Photograph of a sonometer: a long wooden box with a wire stretched along its top over two bridges, a tension key at one end and pegs at the other.',
                       False),
    'q14d-wave': ('paper', 14, (165, 517, 520, 598), SEC, [], 'Diagram of a stationary wave: two curves cross at a point near each end and bow apart between them, with a dashed double-headed arrow below marked 40 cm running between the two crossing points.', False),
}
