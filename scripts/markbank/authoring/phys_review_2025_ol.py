"""Physics 2025 Ordinary Level — reviewed task ledger, correcting the sitting in place.

Independent visual sweep (2026-10-28), every page rendered and read:
  * The paper (LC021GLP000EV), 16 pages: p1 cover (the 2025 papers were
    adjusted for disruption to learning), p2-p5 Section A Questions 1-5 (any
    three, 40 marks each), p6-p15 Section B Questions 6-14 (any five, 56 marks
    each), p16 acknowledgements (images on pages 6-11) and back cover.
  * The marking scheme, 25 pages: p1 cover, p2 note on published schemes, p3
    marking conventions (solidus, double solidus), p4 annotations, p5 Irish
    bonus table, p6-p23 Questions 1-14 ("Page 4" to "Page 21"), p24 blank,
    p25 back cover.

Every printed ask is carded. Section A prints a group mark after a run of
romans: GROUP_TOTALS. Q6 is any eight of (a)-(l) at 7 each (8 x 7): one card
per letter, (d) one card over its two romans (the scheme prices them in one
cell, [4 + 3]). Q12 prints (a) and (b), both compulsory (20 + 36). Q14 is any
two of (a)-(d): every part is carded. Most rows carry the scheme's partial
allowance ("[accept partial answer for 3]") as their note. A cell "[4 + 3]"
set against two answer lines is carded positionally, the first line 4 and the
second 3. Where the scheme prices "any two" with one cell and no per-answer
split (Q11(ii) and (v), [6]), the part is carded whole (questionTotal).

The paper sets 1/p (Q2(iv), (v)), the mirror formula (Q9(iii)) and the radon
and alpha nuclides (Q12(a)) in a mathematical font whose text layer is
unreadable: those asks are shown as printed (question figures).

The sitting was already carded (118 authored cards, 115 shipped). Every task
is re-derived from the PDFs at the scheme's own mark boundaries and the
existing cards are corrected in place: every id is kept, mapped (`id=`) to the
task it was carding, or withdrawn onto its twin (Q6(a), Q10(vii), Q10(viii)
were carded twice, once with and once without the figure). The six asks the
bank had excluded (Q6(h), Q8(i), Q8(viii), Q10(x), Q11(vii), Q14(b)(ii)) and
the eight open ones are carded.
"""
from phys_review_lib import Q, SQ, S, M, G, pt, anyn, T, L

YEAR, LEVEL = 2025, 'ol'
REVIEWED_AT = '2026-10-28'
BASELINE_COMMIT = '99ec7f0a0d6b243f4d5a1dc9b14a6a958e98095e'

SOURCES = {
    'paper': {'path': 'examiner-reports/physics/papers/2025-ol-paper.pdf', 'fileid': 'LC021GLP000EV.pdf',
              'sha256': 'e25bb683dbff1c207dc4092b8e2fefb1dda2b1f2c9e294785c37cd99a605fffa', 'pages': 16},
    'scheme': {'path': 'examiner-reports/physics/schemes/2025-ol.pdf', 'fileid': 'LC021GLP000EV.pdf',
               'sha256': 'bf8f2367d00286ae516dae6ded5ac311ec596df035f4cb53023decbb6dfc308e', 'pages': 25},
}

PAGE_ROLES = {
    'paper': {1: 'cover', **{p: 'questions' for p in range(2, 16)}, 16: 'acknowledgements-back-cover'},
    'scheme': {1: 'cover', 2: 'note', 3: 'conventions', 4: 'annotations', 5: 'irish-bonus',
               **{p: 'marking' for p in range(6, 24)}, 24: 'blank', 25: 'back-cover'},
}

LETTERED = {6, 12, 14}

QUESTION_TOTALS = {**{n: 40 for n in range(1, 6)}, **{n: 56 for n in range(6, 14)},
                   14: 112}   # any two of (a)-(d), 28 each: all four carded
PART_TOTALS = {(12, 'a'): 20, (12, 'b'): 36, **{(14, x): 28 for x in 'abcd'},
               (11, 'ii'): 6, (11, 'v'): 6}   # the scheme's [6] for each "any two"
BEST_OF = {6: (8, 7)}
GROUP_TOTALS = {
    (1, ('i', 'ii', 'iii')): 21, (1, ('iv', 'v', 'vi')): 19,
    (2, ('i', 'ii', 'iii')): 18, (2, ('iv', 'v', 'vi')): 22,
    (3, ('i', 'ii', 'iii')): 21, (3, ('iv', 'v', 'vi')): 19,
    (4, ('i', 'ii', 'iii')): 24, (4, ('iv', 'v', 'vi')): 16,
    (5, ('i', 'ii', 'iii')): 24, (5, ('iv', 'v', 'vi')): 16,
    (7, ('i', 'ii', 'iii', 'iv')): 18, (7, ('v', 'vi', 'vii', 'viii')): 21, (7, ('ix', 'x', 'xi', 'xii')): 17,
    (8, ('i', 'ii', 'iii')): 21, (8, ('iv', 'v')): 13, (8, ('vi', 'vii', 'viii')): 22,
    (9, ('i', 'ii', 'iii', 'iv', 'v')): 36, (9, ('vi', 'vii', 'viii', 'ix')): 20,
    (10, ('i', 'ii', 'iii', 'iv', 'v')): 26, (10, ('vi', 'vii', 'viii')): 14, (10, ('ix', 'x', 'xi')): 16,
    (11, ('i', 'ii')): 12, (11, ('iii', 'iv', 'v')): 19, (11, ('vi', 'vii', 'viii', 'ix')): 25,
    **{(13, (r,)): 7 for r in ('i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii')},
}
CHECKSUMS = {}

SCAN_PAGES = {'paper': range(2, 16)}
SELECTION_SCAN = [
    ('paper', 2, 'the following', 'Q1 "The following data were recorded": a reference to the table.'),
    ('paper', 2, 'the following', 'Q1 "the following formula": a reference to the formula printed.'),
    ('paper', 3, 'the following', 'Q2 "the following results": a reference to the table.'),
    ('paper', 3, 'both', 'Q2(ii) "both the pressure and the volume": both asked, one task.'),
    ('paper', 3, 'the following', 'Q3 "the following results": a reference to the table.'),
    ('paper', 4, 'the following', 'Q4 "The following results were recorded": a reference to the table.'),
    ('paper', 5, 'the following', 'Q5 "the following graph": a reference to the graph.'),
    ('paper', 6, 'the following', 'Q6 "Answer any eight of the following parts": a best-eight of (a)-(l) at 7 '
                                  'each (8 x 7); every part is carded.'),
    ('paper', 6, 'choose', 'Q6(d) "Choose, from the following list": the answer options; one card.'),
    ('paper', 6, 'the following', 'Q6(d), the same list.'),
    ('paper', 8, 'or', 'Q8(v) "in a solid or in air": the answer options.'),
    ('paper', 9, 'or', 'Q9 lead-in "real or virtual images": description.'),
    ('paper', 13, 'the following', 'Q13 "Read the following passage": a reference to the passage.'),
    ('paper', 13, 'the following', 'Q13(vi) "the following equation": a reference to the equation.'),
    ('paper', 14, 'any two', 'Q14 "Answer any two of the following parts": whole-part choice; every part is carded.'),
    ('paper', 14, 'the following', 'Q14, same rubric.'),
    ('paper', 14, 'or', 'Q14(b)(iii) "towards or moving away": the answer options.'),
]

ROUTES = {}
SEC = 'State Examinations Commission'

CRIT = 'The scheme prints no answer here, only what earns the marks.'
DRAWN = 'The scheme prints no drawing; this line names what the diagram must show.'
LEGEND = S('Answers that are separated by a double solidus, //, are answers which are mutually',
           'with a partial answer from the other side.', page=3)
NOLABEL = S('[-1 if no label is present on diagram]')
EACH = S('[accept partial answers for 2 in each case]')


def P(page, start, end=None, **kw):
    return Q(page, start, end, **kw)


def PA(n):
    """The scheme's partial allowance printed under a row."""
    return S(f'[accept partial answer for {n}]')


def R(text, marks, end=None, **kw):
    return pt(S(text, end), marks, **kw)


def C(text, marks, end=None, note=CRIT, **kw):
    return pt(S(text, end), marks, kind='criterion', note=note, **kw)


def FR(page, clip, expect, marks, **kw):
    return G('fraction', page=page, clip=clip, expect=expect, marks=marks, **kw)


def TK(page, clip, expect, marks, **kw):
    return G('tokens', page=page, clip=clip, expect=expect, marks=marks, **kw)


def TT(*a, cells=None, **kw):
    t = T(*a, **kw)
    if cells:
        t['cells'] = cells
    return t


def bundled(parts, keep):
    return f'The old card bundled {parts}, which the scheme prices apart; it keeps its id for {keep}.'


# ------------------------------------------------------------------ stems --
STEM1 = [P(2, 'A student carried out an experiment to verify the principle of conservation of momentum',
           'velocity, vfinal.'),
         P(2, 'She measured the mass of each trolley', 'velocities of the trolleys.')]
DATA1 = P(2, 'The following data were recorded.')
FORMULA1 = [P(2, 'She used the recorded data and the following formula', 'momentum.'),
            P(2, 'total momentum before = total momentum after'), P(2, '(mA × uA) + (mB × uB)')]
STEM2 = [P(3, 'In an experiment to verify Boyle’s law', 'the following results.')]
STEM3 = [P(3, 'In an experiment to calculate the refractive index n of glass', 'the angle i.')]
RESULTS3 = P(3, 'The student recorded the following results.')
STEM4 = [P(4, 'A student carried out an experiment to measure the specific latent heat', 'water.', end_nth=2),
         P(4, 'The following results were recorded.')]
LATENT = P(4, 'She calculated the latent heat released ΔE', '4600 J.')
STEM5 = [P(5, 'In an experiment to measure the resistivity', 'diameter d of the wire.')]
STEM7 = [P(7, 'In 1867, Isaac Newton published his ideas', 'the idea of ‘force’.')]
PLANE = P(7, 'A person wishes to go skydiving.', 'before take‐off.')
JUMP = P(7, 'Some time after take‐off, the skydiver jumps out', 'including the parachute.')
GRAPH7 = P(7, 'The graph shows how the velocity of the skydiver', 'the airplane.')
STEM8 = [P(8, 'Sound is produced when an object vibrates', 'detected by the ear of a nearby person.')]
SPEAKER = P(8, 'A speaker emits a sound wave with a frequency f of 220 Hz.')
DIFFR = P(8, 'Sound waves can undergo diffraction and interference.')
STEM9 = [P(9, 'A concave mirror can be used to form real or virtual images.')]
MIRROR = P(9, 'A concave mirror has a focal length f of 8 cm.', 'of 20 cm in front of the mirror.')
FIBRE9 = P(9, 'Fibre broadband uses fibre optic cables', 'internal reflection.')
GENERATOR = P(10, 'An electrical generator is based on the principle', 'towards a coil as shown.')
TRANSFORMER = P(10, 'A transformer is also based on the principle', 'to provide an input voltage.')
STEM11 = [P(11, 'An air to water system is one of the most common ways to heat modern homes.')]
MONITOR = P(11, 'Internal temperature monitors are used to record the indoor', 'living room is 292 K.')
UVALUE = P(11, 'A U‐value is the measure of the rate of heat loss in a house.')
SOLAR = P(11, 'In addition to air to water systems', 'renewable energy source.')
RADON = [P(12, 'Radon is a naturally occurring radioactive gas', 'found in rocks and soils.')]
FISSION = P(12, 'Nuclear fission reactors are used to generate electricity.')
EINSTEIN = P(12, 'Einstein’s equation E = mc² is used', 'reactor.')
FUSION = P(12, 'The Sun’s energy is produced by nuclear fusion.')
PASSAGE13 = [P(13, 'Domestic electricity refers to electrical circuits', 'earth wires.'),
             P(13, 'Circuit breakers are automatically operated', 'too much current to flow.'),
             P(13, 'The copper wiring in a house connects', 'has 230 V across it.'),
             P(13, 'Electricity meters measure the number of units', 'home.'),
             P(13, 'adapted from www.bbc.co.uk/bitesize')]
CRANE = [P(14, 'A crane lifts large objects from the ground.')]
TRAIN = [P(14, 'A moving train’s whistle emits a note', 'Doppler effect.')]
HIGHER = P(14, 'To the observer, the frequency of the note appears to be higher than 2.4 kHz.')
ELECTROSCOPE = [P(15, 'A gold leaf electroscope has many uses in the field of electrostatics.')]
XRAY = [P(15, 'X‐rays are produced when high speed electrons collide', 'the diagram.')]

TASKS = [
    # ============================================================ Section A ==
    # ---------------------------------------------------------------- Q1 --
    T('1i', 'Q1(i)', 'A', P(2, 'Draw a labelled diagram of the arrangement of the apparatus used in this experiment.'),
      [R('runway // airtrack', 3, note_sel=LEGEND), R('two trolleys // two riders', 3),
       R('timer / metre stick / mass balance', 3),
       C('means of coalescence', 3, note_sel=S('[-1 if no label is present on diagram}'))], 'phys-u2',
      'momentum-apparatus', SQ(6, 'Draw a labelled diagram of the arrangement of the apparatus'), 12,
      stem=STEM1, id='phys-2025-ol-q1-i'),
    T('1ii', 'Q1(ii)', 'A', P(2, 'Describe how the student measured the mass of each trolley.'),
      [R('(put on) mass balance', 3)], 'phys-u2', 'measuring-trolley-mass',
      SQ(6, 'Describe how the student measured the mass of each trolley.'), 3, stem=STEM1,
      id='phys-2025-ol-q1-ii'),
    T('1iii', 'Q1(iii)', 'A', P(2, 'State the formula used to calculate velocity.'),
      [FR(6, (84, 446, 115, 472), 'v = s/t', 6, note_sel=PA(3))], 'phys-1-1', 'velocity-formula',
      SQ(6, 'State the formula used to calculate the velocity.'), 6, stem=STEM1, id='phys-2025-ol-q1-iii'),
    T('1iva', 'Q1(iv)(a)', 'A', [P(2, 'Calculate'), M('(a)', 2), P(2, 'the total momentum before the collision,')],
      [R('momentum before = 0.63 kg m s⁻¹', 6, note_sel=PA(3))], 'phys-1-2', 'momentum-before',
      SQ(6, 'the total momentum before the collision'), 6, stem=STEM1 + [DATA1] + FORMULA1, fig='q1-table',
      id='phys-2025-ol-q1-iv', decision=bundled('(a) and (b)', '(a)')),
    T('1ivb', 'Q1(iv)(b)', 'A', [P(2, 'Calculate'), M('(b)', 2), P(2, 'the total momentum after the collision.')],
      [R('momentum after = 0.63 kg m s⁻¹', 6, note_sel=PA(3))], 'phys-1-2', 'momentum-after',
      SQ(6, 'the total momentum after the collision.'), 6, stem=STEM1 + [DATA1] + FORMULA1, fig='q1-table'),
    T('1v', 'Q1(v)', 'A', P(2, 'Explain how your calculations can be used to verify the principle', 'momentum.'),
      [R('momentum before ≈ momentum after', 3)], 'phys-1-2', 'verifying-conservation',
      SQ(6, 'Explain how your calculations can be used to verify the principle'), 3, stem=STEM1,
      id='phys-2025-ol-q1-v', decision='The scheme\'s reprint says "conversation" for the paper\'s '
                                       '"conservation": a misprint in the reprint only.'),
    T('1vi', 'Q1(vi)', 'A', P(2, 'How could the student have minimised the effect of friction?'),
      [R('using an air track, aerodynamic trolleys, etc.', 4, note_sel=PA(2))], 'phys-u2', 'minimising-friction',
      SQ(6, 'How could the student have minimised the effect of friction?'), 4, stem=STEM1,
      id='phys-2025-ol-q1-vi'),
    # ---------------------------------------------------------------- Q2 --
    T('2i', 'Q2(i)', 'A', P(3, 'Draw a labelled diagram of the arrangement of the apparatus used in this experiment.'),
      [anyn(S('any two of; enclosed volume of gas, pressure gauge, volume scale, means of altering the',
              'pressure/volume', piece=2, psep='; '), 2, 6, steps=[6, 3], sep=',', note='any two',
            note_sel=NOLABEL)], 'phys-u2', 'boyles-law-apparatus',
      SQ(7, 'Draw a labelled diagram of the arrangement of the apparatus'), 9, stem=STEM2, id='phys-2025-ol-q2-i',
      decision='"any two of" four at [6 + 3]: a menu, the first 6 and the second 3.'),
    T('2ii', 'Q2(ii)', 'A', P(3, 'Describe how the student measured both the pressure and the volume.'),
      [R('(read) pressure gauge', 3), R('(read) volume scale', 3)], 'phys-u2', 'measuring-pressure-and-volume',
      SQ(7, 'Describe how the student measured both the pressure and the volume.'), 6, stem=STEM2,
      id='phys-2025-ol-q2-ii'),
    T('2iii', 'Q2(iii)', 'A', P(3, 'State one quantity that must be kept constant during the experiment.'),
      [R('temperature / mass of gas', 3)], 'phys-u2', 'boyles-law-constant',
      SQ(7, 'State one quantity that must be kept constant during the experiment.'), 3, stem=STEM2,
      id='phys-2025-ol-q2-iii'),
    T('2iv', 'Q2(iv)', 'A', P(3, 'Copy and complete the table above into your answerbook by calculating the value of'),
      [TK(7, (355, 410, 400, 430), '18.52', 2, note='The scheme\'s completed table: the value for V = 20 cm³.'),
       TK(7, (420, 410, 465, 430), '23.26', 2, note='The scheme\'s completed table: the value for V = 25 cm³.'),
       TK(7, (485, 410, 530, 430), '28.57', 2, note='The scheme\'s completed table: the value for V = 30 cm³.')],
      'phys-u2', 'calculating-one-over-p',
      SQ(7, 'Copy and complete the table above into your answer book by calculating the value of'), 6,
      qfig='q2-iv-question', fig='q2-table', id='phys-2025-ol-q2-iv',
      decision='The paper sets 1/p as a stacked fraction in a font whose text layer is unreadable, so the ask is '
               'shown as printed. The scheme prints [3 x 2] against "calculations of 1/P values" and the three '
               'values in its completed table: a row per value, 2 each, read from the table.'),
    T('2v', 'Q2(v)', 'A', P(3, 'Plot a graph, on graph paper, of'),
      [C('labelled axis', 3), C('points plotted', 6, units=[1] * 6,
                                note='The scheme prints [6 x 1] against this line, which names what earns the marks.'),
       C('line of best fit', 3)], 'phys-u2', 'plotting-one-over-p',
      SQ(7, 'Plot a graph, on graph paper, of'), 12, qfig='q2-v-question', fig='q2-table',
      id='phys-2025-ol-q2-v',
      decision='The paper sets 1/p as a stacked fraction in a font whose text layer is unreadable, so the ask is '
               'shown as printed.'),
    T('2vi', 'Q2(vi)', 'A', P(3, 'Explain how your graph verifies Boyle’s law.'),
      [R('straight line graph through the origin / P is inversely proportional to V', 4, note_sel=PA(2))],
      'phys-u2', 'graph-verifies-boyles-law', SQ(7, 'Explain how your graph verifies Boyle’s Law.'), 4,
      stem=STEM2, id='phys-2025-ol-q2-vi'),
    # ---------------------------------------------------------------- Q3 --
    T('3i', 'Q3(i)', 'A', P(3, 'Draw a labelled diagram of the arrangement of the apparatus used in this experiment.',
                           after='refractive index n of glass'),
      [R('block', 3), R('ray box / laser / pins', 3), R('detail: ruler, protractor, paper, etc.', 3, note_sel=NOLABEL)],
      'phys-u2', 'refraction-apparatus', SQ(8, 'Draw a labelled diagram of the arrangement of the apparatus'), 9,
      stem=STEM3, id='phys-2025-ol-q3-i'),
    T('3ii', 'Q3(ii)', 'A', P(3, 'On your diagram, draw and label the incident ray', 'surface of the glass block.'),
      [C('incident ray', 3), C('refracted ray', 3), C('normal', 3, note_sel=NOLABEL)], 'phys-2-3',
      'incident-and-refracted-rays', SQ(8, 'On your diagram, draw and label the incident ray'), 9, stem=STEM3,
      id='phys-2025-ol-q3-ii'),
    T('3iii', 'Q3(iii)', 'A', P(3, 'What piece of equipment did the student use to measure the angles?'),
      [R('protractor', 3)], 'phys-u2', 'measuring-angles',
      SQ(8, 'What piece of equipment did the student use to measure the angles?'), 3, stem=STEM3,
      id='phys-2025-ol-q3-iii'),
    TT('3iv', 'Q3(iv)', 'A', P(3, 'Copy and complete the table above into your answerbook by calculating the missing',
                               'to 2 decimal places.'),
       [TK(8, (280, 450, 320, 500), '0.72 0.87', 2, label=S('calculations of sin i values')),
        TK(8, (375, 450, 415, 500), '0.47 0.57', 2, label=S('calculations of sin r values')),
        TK(8, (470, 420, 510, 500), '1.52 1.53 1.52', 3,
           note='The last column of the scheme\'s completed table, priced [3 x 1].')], 'phys-u2',
       'completing-the-sine-table',
       SQ(8, 'Copy and complete the table above into your answerbook by calculating the missing'), 7,
       stem=STEM3 + [RESULTS3], fig='q3-table', id='phys-2025-ol-q3-iv',
       cells='The [3 x 1] for the sin i / sin r values is printed against the scheme\'s line "calculations of '
             'sin i / sin r values" (p8, a stacked fraction), which no row lifts: the row is the values read from '
             'the table. The printed cells are [2 x 1] + [2 x 1] + [3 x 1] = 7.',
       decision='The scheme prints its computed values in its completed table, priced line by line under it: '
                'each row is a line\'s values read from the table.'),
    T('3v', 'Q3(v)', 'A', P(3, 'Use the data to calculate an average value for the refractive index n of the glass.'),
      [R('average calculation, n ≈ 1.5', 6, note_sel=PA(3))], 'phys-2-3', 'average-refractive-index',
      SQ(8, 'Use the data to calculate an average value for the refractive index'), 6, stem=STEM3 + [RESULTS3],
      fig='q3-table', id='phys-2025-ol-q3-v'),
    T('3vi', 'Q3(vi)', 'A', P(3, 'State one precaution the student should take when carrying out the experiment.'),
      [R('any valid precaution: use large angle values, etc.', 6, note_sel=PA(3))], 'phys-u2',
      'refraction-precaution', SQ(8, 'State one precaution the student should take'), 6, stem=STEM3,
      id='phys-2025-ol-q3-vi'),
    # ---------------------------------------------------------------- Q4 --
    T('4i', 'Q4(i)', 'A', P(4, 'Draw a labelled diagram of the apparatus used in the experiment.'),
      [R('calorimeter', 3), R('water', 3), R('steam generator', 3), R('thermometer / mass balance', 3),
       C('detail: lagging, lid, stirrer, steam trap, tubing, etc.', 2, note_sel=NOLABEL)], 'phys-u2',
      'latent-heat-apparatus', SQ(9, 'Draw a labelled diagram of the apparatus used in the experiment.'), 14,
      stem=STEM4[:1], id='phys-2025-ol-q4-i'),
    T('4ii', 'Q4(ii)', 'A', P(4, 'The initial temperature of the steam was 100 °C.', 'steam.'),
      [R('100 – 42 = 58 °C', 5, note_sel=PA(2))], 'phys-2-1', 'change-in-steam-temperature',
      SQ(9, 'The initial temperature of the steam was 100 °C.'), 5, stem=STEM4, fig='q4-table',
      id='phys-2025-ol-q4-ii'),
    T('4iii', 'Q4(iii)', 'A', P(4, 'Calculate the mass m of the steam added.'),
      [R('0.198 – 0.196 = 0.002 kg', 5, note_sel=PA(2))], 'phys-2-1', 'mass-of-steam',
      SQ(9, 'Calculate the mass m of the steam added.'), 5, stem=STEM4, fig='q4-table', id='phys-2025-ol-q4-iii'),
    T('4iv', 'Q4(iv)', 'A', P(4, 'Calculate, l, the specific latent heat of vaporisation of the water.'),
      [R('l = 2.3 × 10⁶ J kg⁻¹', 6, note_sel=PA(3))], 'phys-2-1', 'specific-latent-heat',
      SQ(9, 'Calculate, l, the specific latent heat of vaporisation of the water.'), 6,
      stem=STEM4 + [LATENT], fig='q4-table', id='phys-2025-ol-q4-iv'),
    T('4v', 'Q4(v)', 'A', P(4, 'Suggest a reason why the student used cold water at the start of the experiment.'),
      [R('so that the energy gained = energy lost', 6, end='steam condenses quicker', note_sel=PA(3))], 'phys-u2',
      'why-cold-water', SQ(9, 'Suggest a reason why the student used cold water'), 6, stem=STEM4[:1],
      id='phys-2025-ol-q4-v'),
    T('4vi', 'Q4(vi)', 'A', P(4, 'State one safety precaution the student should take', 'experiment.'),
      [R('wear heat proof gloves, safety glasses, etc.', 4, note_sel=PA(2))], 'phys-u2', 'latent-heat-safety',
      SQ(9, 'State one safety precaution the student should take'), 4, stem=STEM4[:1], id='phys-2025-ol-q4-vi'),
    # ---------------------------------------------------------------- Q5 --
    T('5ia', 'Q5(i)(a)', 'A', [P(5, 'Describe how the student measured'), M('(a)', 5), P(5, 'the length l of the wire,')],
      [R('metre stick', 6, note_sel=PA(3))], 'phys-u2', 'measuring-length-of-wire',
      SQ(10, 'the length l of the wire'), 6, stem=STEM5, id='phys-2025-ol-q5-i',
      decision=bundled('(a) and (b)', '(a)')),
    T('5ib', 'Q5(i)(b)', 'A', [P(5, 'Describe how the student measured'), M('(b)', 5), P(5, 'the resistance R of the wire.')],
      [R('ohmmeter', 6, note_sel=PA(3))], 'phys-u2', 'measuring-resistance-of-wire',
      SQ(10, 'the resistance R of the wire.'), 6, stem=STEM5),
    T('5ii', 'Q5(ii)', 'A', P(5, 'Describe the steps the student used to find the diameter of', 'the wire.'),
      [pt(S('measure diameter at several points along the wire using a micrometer/digital callipers [6]',
            piece=1, psep=' ['), 6, note_sel=PA(3))], 'phys-u2', 'measuring-diameter',
      SQ(10, 'Describe the steps the student used to find the diameter of the wire.'), 6, stem=STEM5,
      id='phys-2025-ol-q5-ii',
      decision='The text layer sets this line\'s [6] inside the line, not as a mark cell: the row is cut at it.'),
    T('5iii', 'Q5(iii)', 'A', P(5, 'The radius of the wire is 0.00124 m.', 'cross‐sectional area A of the wire.'),
      [R('A = 4.83 × 10⁻⁶ m²', 6, note_sel=PA(3))], 'phys-3-3', 'cross-sectional-area',
      SQ(10, 'The radius of the wire is 0.00124 m.'), 6, stem=STEM5, id='phys-2025-ol-q5-iii'),
    T('5iv', 'Q5(iv)', 'A', P(5, 'Describe the relationship between l and R shown in the graph.'),
      [R('(directly) proportional', 4, note_sel=PA(2))], 'phys-3-3', 'length-and-resistance',
      SQ(10, 'Describe the relationship between l and R shown in the graph.'), 4, stem=STEM5, fig='q5-graph',
      id='phys-2025-ol-q5-iv'),
    T('5v', 'Q5(v)', 'A', P(5, 'Calculate the slope of the graph.'),
      [R('m ≈ 0.33 Ω m⁻¹', 6, note_sel=PA(3))], 'phys-3-3', 'slope-of-resistance-graph',
      SQ(10, 'Calculate the slope of the graph.'), 6, stem=STEM5, fig='q5-graph'),
    T('5vi', 'Q5(vi)', 'A', P(5, 'Using the formula, ρ = slope × A, calculate the resistivity ρ of the wire.'),
      [R('ρ ≈ 1.6 × 10⁻⁶ Ω m', 6, note_sel=PA(3))], 'phys-3-3', 'resistivity',
      SQ(10, 'Using the formula, ρ = slope × A, calculate the resistivity'), 6, stem=STEM5, fig='q5-graph',
      id='phys-2025-ol-q5-vi'),
    # ============================================================ Section B ==
    # ---------------------------------------------------------------- Q6 --
    T('6a', 'Q6(a)', 'B', P(6, 'The diagram shows a force of 50 N applied to a', 'fulcrum at the centre of the nut.'),
      [R('moment = 7.5 N m', 7, note_sel=PA(4))], 'phys-1-2', 'moment-on-wrench',
      SQ(11, 'The diagram shows a force of 50 N applied to a wrench.'), 7, fig='q6a-wrench',
      id='phys-2025-ol-q6-a',
      decision='The scheme sets the [7] just left of its marks column (p11, beside the wrench drawing), so the '
               'reader takes no cell for this row; the [7] is printed on the next line, rendered and looked at.'),
    T('6b', 'Q6(b)', 'B', P(6, 'State one condition necessary for equilibrium.'),
      [R('forces up = forces down', 7, end='clockwise moments = anticlockwise moments', note_sel=PA(4))],
      'phys-1-2', 'condition-for-equilibrium', SQ(11, 'State one condition necessary for equilibrium.'), 7,
      id='phys-2025-ol-q6-b'),
    T('6c', 'Q6(c)', 'B', P(6, 'State the three primary colours of light.'),
      [pt(S('red, green, blue', piece=k, psep=', '), m) for k, m in ((1, 3), (2, 2), (3, 2))], 'phys-2-4',
      'primary-colours', SQ(11, 'State the three primary colours of light.'), 7, id='phys-2025-ol-q6-c',
      decision='[3 + 2 + 2] against the three colours printed on one line: in the order printed.'),
    T('6d', 'Q6(d)', 'B', [P(6, 'Choose, from the following list of apparatus, an instrument used to measure'),
                           M('(i)', 6), P(6, 'atmospheric pressure,'), M('(ii)', 6), P(6, 'potential difference.'),
                           P(6, 'barometer', br=True), P(6, 'joulemeter'), P(6, 'sound level meter'),
                           P(6, 'voltmeter')],
      [pt(S('barometer', nth=2), 4, label=S('(i)', after='voltmeter')),
       pt(S('voltmeter', nth=2), 3, label=S('(ii)', after='barometer'), note_sel=PA(4))], 'phys-u2',
      'choosing-instruments', SQ(11, 'Choose, from the following list of apparatus'), 7, id='phys-2025-ol-q6-d',
      decision='One of the eight 7-mark parts: the scheme prices (i) and (ii) in one cell [4 + 3], in order.'),
    T('6e', 'Q6(e)', 'B', P(6, 'Two resistors, 5 \u2126 and 10 \u2126, are connected in parallel.', 'two resistors.'),
      [R('R = 3.3', 7, note_sel=PA(4))], 'phys-3-3', 'resistors-in-parallel',
      SQ(11, 'Two resistors 5'), 7, id='phys-2025-ol-q6-e'),
    T('6f', 'Q6(f)', 'B', P(6, 'State two characteristics of a musical note.'),
      [anyn(S('any two of; loudness, pitch, quality', piece=2, psep='; '), 2, 4, steps=[4, 3], sep=',',
            note='any two')], 'phys-2-5', 'characteristics-of-a-note',
      SQ(11, 'State two characteristics of a musical note.'), 7, id='phys-2025-ol-q6-f',
      decision='"any two of" three at [4 + 3]: a menu, the first 4 and the second 3.'),
    T('6g', 'Q6(g)', 'B', P(6, 'Why does the north pole of a magnet, that is free to rotate, point north?'),
      [R('due to Earth’s magnetic field', 7, note_sel=PA(4))], 'phys-3-4', 'compass-points-north',
      SQ(11, 'Why does the north pole of a magnet'), 7, id='phys-2025-ol-q6-g'),
    T('6h', 'Q6(h)', 'B', P(6, 'Sketch the electric field due to a positive point charge.'),
      [C('correct shape', 4), C('correct direction', 3)], 'phys-3-2', 'field-of-point-charge',
      SQ(11, 'Sketch the electric field lines due to a positive point charge.'), 7,
      decision='[4 + 3] against the two criteria: in order. Excluded from the bank before review; carded.'),
    T('6i', 'Q6(i)', 'B', P(6, 'Explain what is meant by a semiconductor.'),
      [R('material whose resistivity lies between that of a good insulator or conductor', 7, kind='point',
         note_sel=PA(4))], 'phys-3-3', 'semiconductor', SQ(11, 'Explain what is meant by a semiconductor.'), 7,
      id='phys-2025-ol-q6-i'),
    T('6j', 'Q6(j)', 'B', P(6, 'The insulated conductor shown below is positively charged.', 'distribution of charge on it.'),
      [C('(charge throughout with) concentration at pointed end', 7, note=DRAWN, note_sel=PA(4))], 'phys-3-1',
      'charge-on-a-conductor', SQ(12, 'The insulated conductor shown below is positively charged.'), 7,
      fig='q6j-conductor'),
    T('6k', 'Q6(k)', 'B', P(6, 'Draw a labelled diagram of an atom.', 'subatomic particles of the atom.'),
      [C('diagram of nucleus containing protons and neutrons with electrons orbiting in shells', 7, note=DRAWN,
         note_sel=PA(4))], 'phys-4-3', 'diagram-of-an-atom', SQ(12, 'Draw a labelled diagram of an atom.'), 7,
      id='phys-2025-ol-q6-k'),
    T('6l', 'Q6(l)', 'B', P(6, 'Explain what is meant by the photoelectric effect.'),
      [R('emission of electrons from the surface of a metal when light of a suitable frequency shines', 7,
         end='on it', note_sel=PA(4))], 'phys-4-2', 'photoelectric-effect',
      SQ(12, 'Explain what is meant by the photoelectric effect.'), 7, id='phys-2025-ol-q6-l'),
    # ---------------------------------------------------------------- Q7 --
    T('7i', 'Q7(i)', 'B', P(7, 'Explain what is meant by force.'),
      [R('(force) causes acceleration', 6, note_sel=PA(3))], 'phys-1-2', 'force',
      SQ(13, 'Explain what is meant by force.'), 6, stem=STEM7, id='phys-2025-ol-q7-i-ii',
      decision=bundled('(i) and (ii)', '(i)')),
    T('7ii', 'Q7(ii)', 'B', P(7, 'State the SI unit for force.'),
      [R('newton', 3)], 'phys-1-2', 'unit-of-force', SQ(13, 'State the SI unit for force.'), 3, stem=STEM7),
    T('7iii', 'Q7(iii)', 'B', P(7, 'Force is a vector quantity. Explain what is meant by a vector quantity.'),
      [R('(magnitude and) direction', 6, note_sel=PA(3))], 'phys-1-1', 'vector-quantity',
      SQ(13, 'Force is a vector quantity. Explain what is meant by a vector quantity.'), 6,
      id='phys-2025-ol-q7-iii'),
    T('7iv', 'Q7(iv)', 'B', P(7, 'State another example of a vector quantity.'),
      [C('any valid example', 3)], 'phys-1-1', 'example-of-vector',
      SQ(13, 'State another example of a vector quantity.'), 3,
      stem=[M('(iii)', 7), P(7, 'Force is a vector quantity. Explain what is meant by a vector quantity.')],
      id='phys-2025-ol-q7-iv'),
    T('7v', 'Q7(v)', 'B', P(7, 'Calculate the horizontal acceleration of the airplane.'),
      [R('a = 3 m s⁻²', 6, note_sel=PA(3))], 'phys-1-1', 'acceleration-of-airplane',
      SQ(13, 'Calculate the horizontal acceleration of the airplane.'), 6, stem=[PLANE], id='phys-2025-ol-q7-v'),
    T('7vi', 'Q7(vi)', 'B', P(7, 'Calculate the total weight of the skydiver.'),
      [R('F = 686 N', 6, note_sel=PA(3))], 'phys-1-5', 'weight-of-skydiver',
      SQ(13, 'Calculate the total weight of the skydiver.'), 6, stem=[JUMP], id='phys-2025-ol-q7-vi'),
    T('7vii', 'Q7(vii)', 'B', P(7, 'What happens to the force of air resistance when the parachute is opened?'),
      [R('it increases', 3)], 'phys-1-2', 'air-resistance-with-parachute',
      SQ(13, 'What happens to the force of air resistance'), 3, stem=[JUMP], id='phys-2025-ol-q7-vii'),
    T('7viii', 'Q7(viii)', 'B', P(7, 'After the parachute has opened', 'forces now acting on the skydiver.'),
      [C('arrow up', 2), C('arrow down', 2), C('equal and opposite', 2)], 'phys-1-2', 'forces-on-skydiver',
      SQ(13, 'After the parachute has opened'), 6, id='phys-2025-ol-q7-viii'),
    T('7ix', 'Q7(ix)', 'B', P(7, 'How can we tell from the graph that the skydiver is accelerating between A and B?'),
      [R('positive slope', 6, note_sel=PA(3))], 'phys-1-1', 'accelerating-on-graph',
      SQ(13, 'How can we tell from the graph that the skydiver is'), 6, stem=[GRAPH7], fig='q7-graph'),
    T('7x', 'Q7(x)', 'B', P(7, 'Describe the skydiver’s velocity between B and C.'),
      [R('it is constant', 5)], 'phys-1-1', 'velocity-between-b-and-c',
      SQ(13, 'Describe the skydiver’s velocity between B and C.'), 5, stem=[GRAPH7], fig='q7-graph'),
    T('7xi', 'Q7(xi)', 'B', P(7, 'Identify the point that represents when the skydiver opens her parachute.'),
      [R('C', 3)], 'phys-1-1', 'parachute-opens',
      SQ(13, 'Identify the point that represents when the skydiver opens her parachute.'), 3, stem=[GRAPH7],
      fig='q7-graph'),
    T('7xii', 'Q7(xii)', 'B', P(7, 'Why is it safe for the skydiver to land after D?'),
      [R('as they have a small velocity', 3)], 'phys-1-1', 'safe-landing',
      SQ(13, 'Why is it safe for the skydiver to land after D?'), 3, stem=[GRAPH7], fig='q7-graph'),
    # ---------------------------------------------------------------- Q8 --
    T('8i', 'Q8(i)', 'B', P(8, 'Describe an experiment to show that sound requires', 'a medium to travel through.'),
      [C('apparatus', 4), C('method', 4), C('observation', 4, note_sel=EACH)], 'phys-2-5',
      'sound-needs-a-medium', SQ(14, 'Describe an experiment to show that sound requires a medium'), 12,
      stem=STEM8, decision='Excluded from the bank before review; carded with the scheme\'s three criteria.'),
    T('8ii', 'Q8(ii)', 'B', P(8, 'Explain what is meant by the frequency of a wave.'),
      [R('number of waves passing a point per second', 6, note_sel=PA(3))], 'phys-2-2', 'frequency',
      SQ(14, 'Explain what is meant by the frequency of a wave.'), 6, id='phys-2025-ol-q8-ii'),
    T('8iii', 'Q8(iii)', 'B', P(8, 'State the relationship between the frequency and the period of a wave.'),
      [R('inversely proportional', 3)], 'phys-2-2', 'frequency-and-period',
      SQ(14, 'State the relationship between the frequency and the period of a wave.'), 3,
      id='phys-2025-ol-q8-iii'),
    T('8iv', 'Q8(iv)', 'B', P(8, 'Calculate the speed of the sound wave produced.'),
      [R('c = 330 m s⁻¹', 7, note_sel=PA(4))], 'phys-2-2', 'speed-of-sound-wave',
      SQ(14, 'Calculate the speed of the sound wave produced.'), 7, stem=[SPEAKER], id='phys-2025-ol-q8-iv'),
    T('8v', 'Q8(v)', 'B', P(8, 'Does a sound wave travel faster in a solid or in air?'),
      [R('solid', 6)], 'phys-2-5', 'sound-in-solids', SQ(14, 'Does a sound wave travel faster in a solid or in air?'),
      6, id='phys-2025-ol-q8-v'),
    T('8vi', 'Q8(vi)', 'B', P(8, 'Explain what is meant by diffraction.'),
      [R('the (sideways) spreading out of a wave through a narrow gap/around an obstacle.', 6, note_sel=PA(3))],
      'phys-2-3', 'diffraction', SQ(14, 'Explain what is meant by diffraction.'), 6, stem=[DIFFR],
      id='phys-2025-ol-q8-vi'),
    T('8vii', 'Q8(vii)', 'B', P(8, 'Explain why a sound wave diffracts after passing through a doorway'),
      [C('reference to wavelength', 4, note_sel=PA(2))], 'phys-2-3', 'diffraction-and-wavelength',
      SQ(14, 'Explain why a sound wave diffracts after passing through a doorway'), 4, stem=[DIFFR],
      id='phys-2025-ol-q8-vii'),
    T('8viii', 'Q8(viii)', 'B', P(8, 'Describe an experiment to show that sound is a wave', 'interference.'),
      [C('apparatus', 4), C('method', 4), C('observation', 4, note_sel=EACH)], 'phys-2-6',
      'interference-of-sound', SQ(14, 'Describe an experiment to show that sound is a wave'), 12, stem=[DIFFR],
      decision='Excluded from the bank before review; carded with the scheme\'s three criteria.'),
    # ---------------------------------------------------------------- Q9 --
    T('9i', 'Q9(i)', 'B', P(9, 'Distinguish between a real image and a virtual image.'),
      [R('real image is formed by the actual intersection of light rays / virtual image is formed by the', 6,
         end='apparent intersection of light rays', note_sel=PA(3))], 'phys-2-3', 'real-and-virtual-images',
      SQ(15, 'Distinguish between a real and a virtual image.'), 6, stem=STEM9, id='phys-2025-ol-q9-i'),
    T('9ii', 'Q9(ii)', 'B', P(9, 'In your answer book, copy and complete the ray diagram below', 'concave mirror.'),
      [C('first incident ray', 3), C('first reflected ray', 3), C('second reflected ray', 3),
       C('image formed at intersection of rays', 2)], 'phys-2-3', 'ray-diagram-real-image',
      SQ(15, 'In your answer book, copy and complete the ray diagram below'), 11, fig='q9-ray',
      id='phys-2025-ol-q9-ii'),
    T('9iii', 'Q9(iii)', 'B', P(9, 'A concave mirror has a focal length f of 8 cm.', 'Using the formula'),
      [C('correct substitution of u or f', 3), FR(15, (84, 307, 140, 335), '1/v = 1/f − 1/u', 3),
       R('v = 13.3 cm', 3)], 'phys-2-3', 'image-distance',
      SQ(15, 'A concave mirror has a focal length f of 8 cm.'), 9, qfig='q9-iii-question',
      decision='The paper sets the mirror formula as stacked fractions in a font whose text layer is '
               'unreadable, so the ask is shown as printed.'),
    T('9iv', 'Q9(iv)', 'B', P(9, 'Calculate the magnification of the image produced.'),
      [R('magnification = 0.67', 6, note_sel=PA(3))], 'phys-2-3', 'magnification',
      SQ(15, 'Calculate the magnification of the image produced.'), 6, stem=[MIRROR], id='phys-2025-ol-q9-iv'),
    T('9v', 'Q9(v)', 'B', P(9, 'The concave mirror in the ray diagram is replaced with a convex lens.',
                           'ray diagram for the concave mirror.'),
      [R('refraction will occur / ray will pass through lens', 4, note_sel=PA(2))], 'phys-2-3', 'lens-and-mirror',
      SQ(15, 'The concave mirror in the ray diagram is replaced with a convex lens.'), 4, fig='q9-ray',
      id='phys-2025-ol-q9-v'),
    T('9vi', 'Q9(vi)', 'B', P(9, 'Draw a labelled diagram to show how a ray of light is transmitted',
                             'by total internal reflection.'),
      [C('two materials of the differing refractive index', 2), C('ray of light', 2),
       C('multiple internal reflections', 2, note_sel=NOLABEL)], 'phys-2-3', 'light-in-optical-fibre',
      SQ(15, 'Draw a labelled diagram to show how a ray of light is transmitted'), 6, stem=[FIBRE9],
      id='phys-2025-ol-q9-vi'),
    T('9vii', 'Q9(vii)', 'B', P(9, 'The critical angle C of the glass in a fibre optic cable is 42.8°.',
                               'Calculate the refractive index n of the glass.'),
      [R('n = 1.47', 6, note_sel=PA(3))], 'phys-2-3', 'refractive-index-from-critical-angle',
      SQ(15, 'The critical angle C of the glass in a fibre optic cable is 42.8°.'), 6, stem=[FIBRE9],
      id='phys-2025-ol-q9-vii'),
    T('9viii', 'Q9(viii)', 'B', P(9, 'State one advantage of using fibre optic cables instead of copper'),
      [R('greater bandwidth, etc.', 4)], 'phys-2-3', 'fibre-advantage',
      SQ(15, 'State one advantage of using fibre optic cables instead of copper'), 4, stem=[FIBRE9],
      id='phys-2025-ol-q9-viii'),
    T('9ix', 'Q9(ix)', 'B', P(9, 'State one other use of fibre optic cables.'),
      [R('endoscopy, broadband, Christmas decorations, etc.', 4)], 'phys-2-3', 'uses-of-optical-fibres',
      SQ(15, 'State one other use of fibre optic cables.'), 4, stem=[FIBRE9], id='phys-2025-ol-q9-ix'),
    # --------------------------------------------------------------- Q10 --
    T('10i', 'Q10(i)', 'B', P(10, 'Explain what is meant by a magnetic field.'),
      [R('a region in space in which a magnetic force can be felt', 6, note_sel=PA(3))], 'phys-3-4',
      'magnetic-field', SQ(16, 'Explain what is meant by a magnetic field.'), 6, id='phys-2025-ol-q10-i'),
    T('10ii', 'Q10(ii)', 'B', P(10, 'Draw a sketch of the magnetic field around a bar magnet.'),
      [C('magnetic field lines shown above and below a bar magnet', 4, note=DRAWN),
       C('travelling from north to south', 4, note=DRAWN)], 'phys-3-4', 'field-of-bar-magnet',
      SQ(16, 'Draw a sketch of the magnetic field around a bar magnet.'), 8, id='phys-2025-ol-q10-ii'),
    T('10iii', 'Q10(iii)', 'B', P(10, 'Explain what is meant by an electric current.'),
      [R('flow of electrons', 6, note_sel=PA(3))], 'phys-3-3', 'electric-current',
      SQ(16, 'Explain what is meant by an electric current.'), 6, id='phys-2025-ol-q10-iii'),
    T('10iv', 'Q10(iv)', 'B', P(10, 'Name an instrument used to measure electric current.'),
      [R('ammeter / galvanometer', 3)], 'phys-3-3', 'measuring-current',
      SQ(16, 'Name an instrument used to measure electric current.'), 3, id='phys-2025-ol-q10-iv'),
    T('10v', 'Q10(v)', 'B', P(10, 'State one effect of an electric current.'),
      [R('heating / chemical / magnetic', 3)], 'phys-3-3', 'effects-of-current',
      SQ(16, 'State one effect of an electric current.'), 3, id='phys-2025-ol-q10-v'),
    T('10vi', 'Q10(vi)', 'B', P(10, 'Explain what is meant by electromagnetic induction.'),
      [R('the production of an (induced) e.m.f. due to a changing magnetic field', 6, note_sel=PA(3))],
      'phys-3-6', 'electromagnetic-induction', SQ(16, 'Explain what is meant by electromagnetic induction.'), 6,
      stem=[GENERATOR], fig='q10-coil', id='phys-2025-ol-q10-vi'),
    T('10vii', 'Q10(vii)', 'B', P(10, 'What is observed on the meter when the magnet is moved in and out of the coil?'),
      [R('non-zero reading on meter', 4, note_sel=PA(2))], 'phys-3-6', 'magnet-moving-in-coil',
      SQ(16, 'What is observed on the meter when the magnet is moved in and out of the coil?'), 4,
      stem=[GENERATOR], fig='q10-coil', id='phys-2025-ol-q10vii-fig',
      decision='The old cards carded this ask twice, with and without the figure; this one keeps the id the '
               'build already ships (the figure twin).'),
    T('10viii', 'Q10(viii)', 'B', P(10, 'What is observed on the meter when the magnet is stationary within the coil?'),
      [R('constant 0 A reading', 4, note_sel=PA(2))], 'phys-3-6', 'magnet-stationary-in-coil',
      SQ(16, 'What is observed on the meter when the magnet is stationary within the coil?'), 4,
      stem=[GENERATOR], fig='q10-coil', id='phys-2025-ol-q10viii-fig',
      decision='The old cards carded this ask twice, with and without the figure; this one keeps the id the '
               'build already ships (the figure twin).'),
    T('10ix', 'Q10(ix)', 'B', P(10, 'The primary coil of a transformer has 200 turns',
                               'Calculate the output voltage across the secondary coil.'),
      [R('voltage output = 57.5 V', 6, note_sel=PA(3))], 'phys-3-6', 'transformer-output-voltage',
      SQ(16, 'The primary coil of a transformer has 200 turns'), 6, stem=[TRANSFORMER], fig='q10-transformer',
      id='phys-2025-ol-q10-ix'),
    T('10x', 'Q10(x)', 'B', P(10, 'Draw a sketch of a graph to show how an a.c. voltage V changes with time t.'),
      [C('labelled axis and curve shown', 6, note=DRAWN, note_sel=PA(3))], 'phys-3-6', 'ac-voltage-graph',
      SQ(16, 'Draw a sketch of a graph to show how an a.c. voltage V changes with time t.'), 6,
      decision='Excluded from the bank before review; carded with the scheme\'s criterion.'),
    T('10xi', 'Q10(xi)', 'B', P(10, 'State one use of a transformer.'),
      [R('charger, substations, etc.', 4)], 'phys-3-6', 'uses-of-transformers',
      SQ(16, 'State one use of a transformer.'), 4, stem=[TRANSFORMER], id='phys-2025-ol-q10-xi'),
    # --------------------------------------------------------------- Q11 --
    T('11i', 'Q11(i)', 'B', P(11, 'Distinguish between heat and temperature.'),
      [R('heat is a form of energy / temperature is a measure of the hotness (of a body)', 6, note_sel=PA(3))],
      'phys-2-1', 'heat-and-temperature', SQ(17, 'Distinguish between heat and temperature.'), 6, stem=STEM11,
      id='phys-2025-ol-q11-i'),
    T('11ii', 'Q11(ii)', 'B', P(11, 'State two methods by which heat can be transferred throughout', 'a home.'),
      [anyn(S('any two: conduction, convection, radiation', piece=2, psep=': '), 2, 3, sep=',', note='any two',
            note_sel=PA(3))], 'phys-2-1', 'methods-of-heat-transfer',
      SQ(17, 'State two methods by which heat can be transferred throughout a home.'), 6, stem=STEM11,
      tariff='questionTotal', id='phys-2025-ol-q11-ii',
      decision='"any two" at one cell [6], with no mark printed per method: the part is carded whole.'),
    T('11iii', 'Q11(iii)', 'B', P(11, 'Calculate the temperature of the living room in degrees celsius (°C).'),
      [R('292 – 273 = 19 °C', 6, note_sel=PA(3))], 'phys-2-1', 'kelvin-to-celsius',
      SQ(17, 'Calculate the temperature of the living room in degrees celsius (°C).'), 6, stem=[MONITOR],
      id='phys-2025-ol-q11-iii'),
    T('11iv', 'Q11(iv)', 'B', P(11, 'The internal temperature monitors are based on a thermometric',
                               'State one example of a thermometric property.'),
      [C('any valid named thermometric property', 7, note_sel=PA(4))], 'phys-2-1', 'thermometric-property',
      SQ(17, 'The internal temperature monitors are based on a thermometric property.'), 7, stem=[MONITOR],
      id='phys-2025-ol-q11-iv'),
    T('11v', 'Q11(v)', 'B', P(11, 'State two ways in which the U‐value of a house can be reduced.'),
      [pt(S('any two of: glazing, insulation, etc.'), 6, whole=True, note_sel=PA(3))], 'phys-2-1',
      'reducing-u-value', SQ(17, 'State two ways in which the U-value of a house can be reduced.'), 6,
      stem=[UVALUE], tariff='questionTotal', id='phys-2025-ol-q11-v',
      decision='"any two of" at one cell [6], with no mark printed per way, and the scheme\'s list closes on '
               '"etc.": the part is carded whole, its list one row as printed.'),
    T('11vi', 'Q11(vi)', 'B', P(11, 'Explain what is meant by the term renewable', 'energy source.'),
      [R('(an energy source) that doesn’t run out', 6, note_sel=PA(3))], 'phys-1-4', 'renewable-energy-source',
      SQ(17, 'Explain what is meant by the term renewable energy source.'), 6, stem=[SOLAR],
      id='phys-2025-ol-q11-vi'),
    T('11vii', 'Q11(vii)', 'B', P(11, 'State one advantage and one disadvantage of using', 'solar energy.'),
      [C('one advantage and one disadvantage', 7, note_sel=PA(4))], 'phys-1-4', 'solar-energy-pros-and-cons',
      SQ(17, 'State one advantage and one disadvantage of using solar energy.'), 7, stem=[SOLAR],
      decision='Excluded from the bank before review; carded with the scheme\'s criterion.'),
    T('11viii', 'Q11(viii)', 'B', P(11, 'State one other renewable source of energy.'),
      [R('wind, geothermal, biomass, etc.', 6, note_sel=PA(3))], 'phys-1-4', 'other-renewable-sources',
      SQ(17, 'State one other renewable source of energy.'), 6, stem=[SOLAR], id='phys-2025-ol-q11-viii'),
    T('11ix', 'Q11(ix)', 'B', P(11, 'A solar cell can be used to charge a mobile phone.',
                               'Calculate the time taken for the mobile phone to charge.'),
      [R('time = 1200 s', 6, note_sel=PA(3))], 'phys-1-4', 'charging-time',
      SQ(17, 'A solar cell can be used to charge a mobile phone.'), 6, id='phys-2025-ol-q11-ix'),
    # --------------------------------------------------------------- Q12 --
    T('12ai', 'Q12(a)(i)', 'B', P(12, 'Explain what is meant by radioactivity.'),
      [R('decay of a nucleus / nucleus emitting alpha, beta or gamma radiation', 6, kind='point', note_sel=PA(3))],
      'phys-4-4', 'radioactivity', SQ(18, 'Explain what is meant by radioactivity.'), 6, stem=RADON,
      id='phys-2025-ol-q12a-i'),
    T('12aii', 'Q12(a)(ii)', 'B', P(12, 'How many protons are in an atom of radon?'),
      [R('86', 4)], 'phys-4-3', 'protons-in-radon', SQ(18, 'How many protons in an atom of radon?'), 4,
      qfig='q12a-ii-question', id='phys-2025-ol-q12a-ii',
      decision='The paper prints the radon nuclide with its numbers in a font whose text layer is unreadable: '
               'the ask is shown as printed, with the nuclide.'),
    T('12aiii', 'Q12(a)(iii)', 'B', P(12, 'Calculate how many neutrons are in an atom of radon–222.'),
      [R('136', 4)], 'phys-4-3', 'neutrons-in-radon-222',
      SQ(18, 'Calculate how many neutrons are in an atom of radon-222.'), 4, stem=RADON,
      id='phys-2025-ol-q12a-iii'),
    T('12aiv', 'Q12(a)(iv)', 'B', P(12, 'Determine what element is formed after an alpha particle,',
                                    piece=1, psep=' α'),
      [R('Po', 6, note_sel=S('[accept 84 for 2] & [accept 218 for 2]'))], 'phys-4-4', 'alpha-decay-of-radon',
      SQ(18, 'Determine what element is formed after an alpha particle,'), 6, qfig='q12a-iv-question',
      id='phys-2025-ol-q12a-iv',
      decision='The paper prints the alpha particle and radon nuclides in a font whose text layer is '
               'unreadable: the ask is shown as printed, and its text is lifted up to the first nuclide.'),
    T('12bi', 'Q12(b)(i)', 'B', P(12, 'Explain what is meant by nuclear fission.'),
      [R('splitting of a (large) nucleus', 6, note_sel=PA(3))], 'phys-4-6', 'nuclear-fission',
      SQ(18, 'Explain what is meant by nuclear fission.'), 6, stem=[FISSION], id='phys-2025-ol-q12b-i'),
    T('12bii', 'Q12(b)(ii)', 'B', P(12, 'Explain what is meant by a chain reaction.'),
      [R('the products of the reaction continue the reaction', 6, note_sel=PA(3))], 'phys-4-6', 'chain-reaction',
      SQ(18, 'Explain what is meant by a chain reaction.'), 6, stem=[FISSION], id='phys-2025-ol-q12b-ii'),
    T('12biii', 'Q12(b)(iii)', 'B', P(12, 'State a suitable fuel used in a nuclear fission reactor.'),
      [R('uranium / plutonium', 3)], 'phys-4-6', 'fission-fuel',
      SQ(18, 'State a suitable fuel used in a nuclear fission reactor.'), 3, stem=[FISSION],
      id='phys-2025-ol-q12b-iii'),
    T('12biva', 'Q12(b)(iv)(a)', 'B', [P(12, 'State the function of'), M('(a)', 12), P(12, 'the moderator,')],
      [R('slows down (fast-moving) neutrons', 3, label=S('(a)', after='the shielding in a nuclear reactor.'))],
      'phys-4-6', 'moderator', SQ(18, 'State the function of'), 3, stem=[FISSION], id='phys-2025-ol-q12b-iv',
      decision=bundled('(a) and (b)', '(a)')),
    T('12bivb', 'Q12(b)(iv)(b)', 'B', [P(12, 'State the function of'), M('(b)', 12),
                                       P(12, 'the shielding in a nuclear reactor.')],
      [R('prevents escape of radiation', 3, label=S('(b)', after='slows down'))], 'phys-4-6', 'shielding',
      SQ(18, 'State the function of'), 3, stem=[FISSION]),
    T('12bv', 'Q12(b)(v)', 'B', P(12, 'Identify what the letters m and c stand for.'),
      [R('m = mass of object & c = speed of light', 6, whole=True, note_sel=PA(3))], 'phys-4-5', 'e-equals-mc2',
      SQ(18, 'Identify what the letters m and c stand for.'), 6, stem=[EINSTEIN], id='phys-2025-ol-q12b-v',
      decision='The scheme prices both letters in one cell [6] on one line: one row.'),
    T('12bvi', 'Q12(b)(vi)', 'B', P(12, 'Explain what is meant by nuclear fusion.'),
      [R('joining of two (small) nuclei', 6, note_sel=PA(3))], 'phys-4-6', 'nuclear-fusion',
      SQ(18, 'Explain what is meant by nuclear fusion.'), 6, stem=[FUSION], id='phys-2025-ol-q12b-vi'),
    T('12bvii', 'Q12(b)(vii)', 'B', P(12, 'State one advantage of using nuclear fusion over nuclear fission'),
      [C('any valid reference to fuel/products', 3)], 'phys-4-6', 'fusion-over-fission',
      SQ(18, 'State one advantage of using nuclear fusion over nuclear fission'), 3, stem=[FUSION],
      id='phys-2025-ol-q12b-vii'),
    # --------------------------------------------------------------- Q13 --
    T('13i', 'Q13(i)', 'B', P(13, 'Name a common material used to conduct electricity in an electrical cable.'),
      [R('copper', 7, note_sel=PA(4))], 'phys-3-3', 'cable-conductor',
      SQ(19, 'Name a common material used to conduct electricity in an electrical cable.'), 7, stem=PASSAGE13,
      id='phys-2025-ol-q13-i'),
    T('13ii', 'Q13(ii)', 'B', P(13, 'Explain the function of an earth wire.'),
      [R('provides a (low resistance) path to earth / safety feature', 7, note_sel=PA(4))], 'phys-3-3',
      'earth-wire', SQ(19, 'Explain the function of an earth wire'), 7, id='phys-2025-ol-q13-ii'),
    T('13iii', 'Q13(iii)', 'B', P(13, 'A fuse is a type of circuit breaker. Explain how', 'a fuse works.'),
      [R('melts / breaks if current is too high', 7, note_sel=PA(4))], 'phys-3-3', 'how-a-fuse-works',
      SQ(19, 'A fuse is a type of circuit breaker. Explain how a fuse works.'), 7, id='phys-2025-ol-q13-iii',
      decision='The scheme misprints this row\'s cell as "[7)" (p19, rendered and looked at), which the reader '
               'does not take as a cell; the paper prints (7) for the part.'),
    T('13iv', 'Q13(iv)', 'B', [P(13, 'An electric kettle has a power rating of 2300 W.', 'fuse that should be used.'),
                               P(13, '3 Amp', br=True), P(13, '5 Amp'), P(13, '13 Amp')],
      [R('13 A', 7, note_sel=PA(4))], 'phys-3-3', 'choosing-a-fuse',
      SQ(19, 'An electric kettle has a power rating of 2300 W.'), 7, id='phys-2025-ol-q13-iv'),
    T('13v', 'Q13(v)', 'B', [P(13, 'In an electric plug, state the colour of'), M('(a)', 13), P(13, 'the live wire,'),
                             M('(b)', 13), P(13, 'the neutral wire.')],
      [R('live - brown', 4, label=S('(a)')), R('neutral - blue', 3, label=S('(b)'), note_sel=PA(4))],
      'phys-3-3', 'plug-wire-colours', SQ(19, 'In an electric plug, state the colour of'), 7,
      id='phys-2025-ol-q13-v', decision='One cell [4 + 3] prices (a) and (b) together: one card, in order.'),
    T('13vi', 'Q13(vi)', 'B', [P(13, 'The cost of electricity is calculated using the following equation.'),
                               P(13, 'units (kW h) = power (kW) × time (h)'), P(13, 'The price of a unit is 30 cent.'),
                               P(13, 'Calculate the cost of using a 1.2 kW electric heater for 3 hours.')],
      [R('€1.08', 7, note_sel=PA(4))], 'phys-3-3', 'cost-of-electricity',
      SQ(19, 'The cost of electricity is calculated using the following equation.'), 7, id='phys-2025-ol-q13-vi'),
    T('13vii', 'Q13(vii)', 'B', P(13, 'Explain why appliances in the home are connected in parallel.'),
      [R('each appliance has 230 V across it / even if one appliance is off the rest of the appliances', 7,
         end='can still work', note_sel=PA(4))], 'phys-3-3', 'appliances-in-parallel',
      SQ(19, 'Explain why appliances in the home are connected in parallel.'), 7, id='phys-2025-ol-q13-vii'),
    T('13viii', 'Q13(viii)', 'B', P(13, 'Another device used in domestic circuits is a residual current device',
                                    'Explain the function of an RCD.'),
      [R('detects a current difference between the outgoing and incoming current / safety device /', 7,
         end='circuit breaker', note_sel=PA(4))], 'phys-3-3', 'rcd',
      SQ(19, 'Another device used in domestic circuits is a residual current device'), 7,
      id='phys-2025-ol-q13-viii'),
    # --------------------------------------------------------------- Q14 --
    T('14ai', 'Q14(a)(i)', 'B', P(14, 'Explain what is meant by energy.'),
      [R('the ability to do work', 6, note_sel=PA(3))], 'phys-1-4', 'energy',
      SQ(20, 'Explain what is meant by energy.'), 6, stem=CRANE, id='phys-2025-ol-q14a-i'),
    T('14aii', 'Q14(a)(ii)', 'B', P(14, 'State the principle of conservation of energy.'),
      [R('energy cannot be created or destroyed', 6, kind='point', note_sel=PA(3))], 'phys-1-4',
      'conservation-of-energy', SQ(20, 'State the principle of conservation of energy.'), 6, stem=CRANE,
      id='phys-2025-ol-q14a-ii'),
    T('14aiii', 'Q14(a)(iii)', 'B', P(14, 'Calculate the work done in lifting a weight of'),
      [R('W = 42', 6, note_sel=PA(3))], 'phys-1-4', 'work-done-lifting',
      SQ(20, 'Calculate the work done in lifting a weight of'), 6, stem=CRANE, id='phys-2025-ol-q14a-iii'),
    T('14aiv', 'Q14(a)(iv)', 'B', P(14, 'Calculate the power output required by the crane', 'of 12 seconds.'),
      [R('P = 3500 W', 6, note_sel=PA(3))], 'phys-1-4', 'power-output',
      SQ(20, 'Calculate the power output required by the crane'), 6, stem=CRANE, id='phys-2025-ol-q14a-iv'),
    T('14av', 'Q14(a)(v)', 'B', P(14, 'The input power of the crane is 5000 W.'),
      [R('% efficiency = 70 %', 4, note_sel=PA(2))], 'phys-1-4', 'efficiency',
      SQ(20, 'The input power of the crane is 5000 W.'), 4, stem=CRANE, id='phys-2025-ol-q14a-v'),
    T('14bi', 'Q14(b)(i)', 'B', P(14, 'Explain what is meant by the Doppler effect.'),
      [R('(apparent) change in frequency due to the change in motion between the source', 6,
         end='producing it and the observer', note_sel=PA(3))], 'phys-2-7', 'doppler-effect',
      SQ(21, 'Explain what is meant by the Doppler effect.'), 6, stem=TRAIN, id='phys-2025-ol-q14b-i'),
    T('14bii', 'Q14(b)(ii)', 'B', P(14, 'Describe a laboratory experiment to demonstrate the Doppler effect.'),
      [C('apparatus', 4), C('method', 4), C('observation', 4, note_sel=EACH)], 'phys-2-7',
      'demonstrating-doppler', SQ(21, 'Describe a laboratory experiment to demonstrate the Doppler effect.'), 12,
      stem=TRAIN, decision='Excluded from the bank before review; carded with the scheme\'s three criteria.'),
    T('14biii', 'Q14(b)(iii)', 'B', P(14, 'Is the train moving towards or moving away from the observer?'),
      [R('towards', 3)], 'phys-2-7', 'train-towards-or-away',
      SQ(21, 'Is the train moving towards or moving away from the observer?'), 3, stem=TRAIN + [HIGHER],
      id='phys-2025-ol-q14b-iii'),
    T('14biv', 'Q14(b)(iv)', 'B', P(14, 'Describe the frequency that the train driver hears.'),
      [R('hears the same note / 2.4 kHz', 3)], 'phys-2-7', 'driver-hears',
      SQ(21, 'Describe the frequency that the train driver hears.'), 3, stem=TRAIN + [HIGHER],
      id='phys-2025-ol-q14b-iv'),
    T('14bv', 'Q14(b)(v)', 'B', P(14, 'State one application of the Doppler effect.'),
      [R('speed gun, measuring red shift, ultrasonic scanners, weather forecasting, used to study', 4,
         end='heartbeat, blood flow, etc.', note_sel=PA(2))], 'phys-2-7', 'applications-of-doppler',
      SQ(21, 'State one an application of the Doppler effect.'), 4, stem=TRAIN, id='phys-2025-ol-q14b-v'),
    T('14ci', 'Q14(c)(i)', 'B', P(15, 'Identify the part labelled X on the', 'electroscope in the diagram.'),
      [R('gold / leaf', 6)], 'phys-3-1', 'gold-leaf',
      SQ(22, 'Identify the part labelled X on the electroscope in the diagram.'), 6, stem=ELECTROSCOPE,
      fig='q14c-electroscope', labels=[L('X', S('gold / leaf', page=22), True)]),
    T('14cii', 'Q14(c)(ii)', 'B', P(15, 'Describe how to charge an electroscope', 'negatively.'),
      [R('contact with negative conductor / brought close to positive charge and earthed', 6, note_sel=PA(3))],
      'phys-3-1', 'charging-negatively', SQ(22, 'Describe how to charge an electroscope negatively'), 6,
      stem=ELECTROSCOPE, fig='q14c-electroscope', id='phys-2025-ol-q14c-ii'),
    T('14ciii', 'Q14(c)(iii)', 'B', P(15, 'State one use of an electroscope.'),
      [R('detecting or measuring charge / potential difference / capacitance', 6, kind='point', note_sel=PA(3))],
      'phys-3-1', 'uses-of-electroscope', SQ(22, 'State one use of an electroscope.'), 6, stem=ELECTROSCOPE,
      id='phys-2025-ol-q14c-iii'),
    T('14civ', 'Q14(c)(iv)', 'B', P(15, 'State Coulomb’s law.'),
      [R('force proportional to product of charges', 3, end='// F ∝ q₁q₂', note_sel=LEGEND),
       FR(22, (84, 288, 490, 315), 'inversely proportional to the square of the distance between them // ∝ 1/d²', 3)],
      'phys-3-1', 'coulombs-law', SQ(22, 'State Coulomb’s law.'), 6, id='phys-2025-ol-q14c-iv',
      decision='Each line printed with its // side: one row per line, as printed.'),
    T('14cv', 'Q14(c)(v)', 'B', P(15, 'Describe a method used to remove the charge', 'from an electroscope.'),
      [R('connect metal cap of an electroscope to an earth', 4, note_sel=PA(2))], 'phys-3-1',
      'discharging-electroscope', SQ(22, 'Describe a method used to remove the charge from an electroscope.'), 4,
      stem=ELECTROSCOPE, fig='q14c-electroscope', id='phys-2025-ol-q14c-v'),
    T('14di', 'Q14(d)(i)', 'B', P(15, 'What are X‐rays?'),
      [R('high energy rays / electromagnetic radiation', 6, note_sel=PA(3))], 'phys-4-2', 'what-are-x-rays',
      SQ(23, 'What are X-rays?'), 6, stem=XRAY, fig='q14d-xray', id='phys-2025-ol-q14d-i'),
    T('14dii', 'Q14(d)(ii)', 'B', P(15, 'Identify a suitable material that could be used for the target.'),
      [R('material with a high melting point', 6, note_sel=PA(3))], 'phys-4-2', 'x-ray-target',
      SQ(23, 'Identify a suitable material that could be used for the target.'), 6, stem=XRAY, fig='q14d-xray',
      id='phys-2025-ol-q14d-ii'),
    T('14diii', 'Q14(d)(iii)', 'B', P(15, 'Describe how electrons are produced in the X‐ray tube.'),
      [R('thermionic emission', 6, note_sel=PA(3))], 'phys-4-1', 'producing-electrons',
      SQ(23, 'Describe how electrons are produced in the X-ray tube.'), 6, stem=XRAY, fig='q14d-xray',
      id='phys-2025-ol-q14d-iii'),
    T('14div', 'Q14(d)(iv)', 'B', P(15, 'Why is a lead casing put around an X‐ray tube?'),
      [R('for safety / to prevent radiation being released to surroundings', 6, note_sel=PA(3))], 'phys-4-2',
      'lead-casing', SQ(23, 'Why is a lead casing put around an X-ray tube?'), 6, stem=XRAY, fig='q14d-xray',
      id='phys-2025-ol-q14d-iv'),
    T('14dv', 'Q14(d)(v)', 'B', P(15, 'State one use of X‐rays.'),
      [R('check for broken bones, check for defects in parts, food irradiation, etc.', 4, note_sel=PA(2))],
      'phys-4-2', 'uses-of-x-rays', SQ(23, 'State one use of X-rays.'), 4, stem=XRAY, fig='q14d-xray', id='phys-2025-ol-q14d-v'),
]

ANSWER_VARIANTS = {}

RETAINED = {
    'phys-2025-ol-q6a-fig': 'A figure twin of phys-2025-ol-q6-a, which carries the reviewed task and its figure '
                            '(the build already drops this twin as superseded by its base).',
    'phys-2025-ol-q10-vii': 'Never shipped: the figureless twin of phys-2025-ol-q10vii-fig, which carries the '
                            'reviewed task and its figure.',
    'phys-2025-ol-q10-viii': 'Never shipped: the figureless twin of phys-2025-ol-q10viii-fig, which carries the '
                             'reviewed task and its figure.',
}
WITHDRAW = {'phys-2025-ol-q6a-fig': ('phys-2025-ol-q6-a', RETAINED['phys-2025-ol-q6a-fig']),
            'phys-2025-ol-q10-vii': ('phys-2025-ol-q10vii-fig', RETAINED['phys-2025-ol-q10-vii']),
            'phys-2025-ol-q10-viii': ('phys-2025-ol-q10viii-fig', RETAINED['phys-2025-ol-q10-viii'])}

FIGURES = {
    'q1-table': ('paper', 2, (52, 272, 545, 416), SEC, [], 'Table of the data recorded: mass of trolley A, mA, 0.34 kg; mass of trolley B, mB, 0.36 kg; velocity of trolley A before the collision, uA, 1.85 m s⁻¹; velocity of trolley B before the collision, uB, 0 m s⁻¹; velocity of trolley A and trolley B after the collision, vfinal, 0.90 m s⁻¹.', False),
    'q2-table': ('paper', 3, (52, 88, 545, 172), SEC, [], 'Table of results: V (cm³) 5, 10, 15, 20, 25, 30; p (MPa) 0.203, 0.108, 0.073, 0.054, 0.043, 0.035; a row for 1/p (MPa⁻¹) with 4.93, 9.26 and 13.70 filled in and its last three cells blank.', False),
    'q2-iv-question': ('paper', 3, (52, 239, 545, 277), SEC, [], 'The printed question: (iv) Copy and complete the table above into your answerbook by calculating the value of 1/p, set as a fraction, to 2 decimal places.', False),
    'q2-v-question': ('paper', 3, (52, 280, 545, 304), SEC, [], 'The printed question: (v) Plot a graph, on graph paper, of 1/p, set as a fraction, against V.', False),
    'q3-table': ('paper', 3, (52, 495, 545, 622), SEC, [], 'Table of results with columns i (degrees), r (degrees), sin i, sin r and n = sin i / sin r: the row 20, 13 has sin i 0.34 and sin r 0.22; the rows 46, 28 and 61, 35 have their sine cells blank, and the n column is blank in every row.', False),
    'q4-table': ('paper', 4, (52, 139, 545, 231), SEC, [], 'Table of results: mass of calorimeter + cold water 0.196 kg; mass of calorimeter + water + steam 0.198 kg; final temperature of calorimeter, water and added steam 42 °C.', False),
    'q5-graph': ('paper', 5, (55, 120, 535, 395), SEC, [], 'Graph of R (Ω), from 0.00 to 0.25, against l (m), from 0.00 to 0.65: six plotted points lie on a straight line drawn from the origin up to the last point at 0.60 m.', False),
    'q6a-wrench': ('paper', 6, (358, 160, 545, 262), SEC, [], 'Drawing of a wrench gripping a nut at one end; an arrow labelled force applied = 50 N points down on the handle, and a double-headed arrow labelled distance = 15 cm runs from the nut along the wrench.', False),
    'q6j-conductor': ('paper', 6, (150, 528, 445, 594), SEC, [], 'Outline of an insulated conductor, pointed at its left end and rounded at its right end, with an arrow from the label insulated conductor.', False),
    'q7-graph': ('paper', 7, (148, 395, 445, 535), SEC, ['A', 'B', 'C', 'D'], 'Sketch graph of velocity (m s⁻¹) against time (s): from A at the origin the curve rises and bends over to B, a horizontal line runs from B to C, the curve drops steeply from C to D, then runs at a low level before falling to the time axis.', False),
    'q9-ray': ('paper', 9, (85, 128, 505, 282), SEC, [], 'Ray diagram set-up: a principal axis drawn as a dashed line, an upright arrow labelled object standing on it, a point labelled f on the axis, and a concave mirror drawn as a curve on the right.', False),
    'q9-iii-question': ('paper', 9, (52, 286, 545, 326), SEC, [], 'The printed question: (iii) A concave mirror has a focal length f of 8 cm. An object is placed with an object distance u of 20 cm in front of the mirror. Using the formula 1/u + 1/v = 1/f, each term set as a fraction, calculate the image distance v.', False),
    'q10-coil': ('paper', 10, (222, 190, 382, 268), SEC, [], 'Diagram of a bar magnet, S on the left and N on the right, with an arrow pointing from its N end towards a coil; the coil is connected in a loop to a meter.', False),
    'q10-transformer': ('paper', 10, (138, 380, 428, 492), SEC, [], 'Diagram of a transformer: a primary coil and a secondary coil wound on opposite sides of a square core, with the input voltage terminals at the primary coil and the output voltage terminals at the secondary coil.', False),
    'q12a-ii-question': ('paper', 12, (52, 151, 545, 193), SEC, [], 'The printed lines: Rn²²²₈₆ is a radon atom. (ii) How many protons are in an atom of radon?', False),
    'q12a-iv-question': ('paper', 12, (52, 220, 545, 263), SEC, [], 'The printed lines: Rn²²²₈₆ emits an alpha particle. (iv) Determine what element is formed after an alpha particle, α⁴₂, is emitted from Rn²²²₈₆.', False),
    'q14c-electroscope': ('paper', 15, (345, 75, 545, 245), SEC, ['X'], 'Diagram of a gold leaf electroscope: a cap on a metal rod that passes through the insulation between the cap and the frame into an earthed box; a thin line hangs beside the rod inside the box, with arrow X pointing to it.', False),
    'q14d-xray': ('paper', 15, (78, 340, 472, 600), SEC, [], 'Diagram of an X-ray tube: a coiled filament on the left, joined to the low voltage terminals, faces a target on the right; the high voltage terminals connect the two ends, an arrow labelled high speed electrons points along the path between them, rays fan out downward from the target, and the tube sits inside a lead casing.', False),
}
