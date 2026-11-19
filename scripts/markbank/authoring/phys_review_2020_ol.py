"""Physics 2020 Ordinary Level — reviewed task ledger, carded from the paper for the first time.

Independent visual sweep (2026-10-28), every page rendered and read:
  * The paper (LC021GLP000EV), 12 pages: p1 cover ("Answer three questions from Section A and
    five questions from Section B"), p2-p3 Section A (120 marks) Questions 1-4 (experiments, 40
    marks each, group marks printed after runs of romans), p4-p11 Section B (280 marks) Questions
    5-12 (56 marks each), p11 also the acknowledgements (images on pages 4-10), p12 back cover.
  * The marking scheme, 20 pages: p1 cover, p2 note on published schemes, p3 points to note
    (solidus, double solidus, slips), p4-p16 Questions 1-12 (each part's ask reprinted in bold with
    its tariff at the right, "6 or 3" where a partial answer earns the second figure, and the
    answers under it in regular type, each with its cell; "partial answer ... (3)" is the partial
    credit and is never added), p17-p18 blank (footers [15]-[16]), p19-p20 blank.

Every printed ask is carded at the scheme's own mark boundary: a roman, or a letter (Q5 and Q11,
and the romans of Q12(a)-(d), letter-major). Q5 is "Answer any eight of (a)-(j)" (best eight of
ten at 7 each = 56); Q12 "Answer any two of (a), (b), (c), (d)" (four 28s, 112 carded).

The census read (paper_census) needed one gated entry (paper.FIGURE_BLOCKS, 2020 OL): the Q3
graph's vertical axis label "4" was read as the head of Question 4 and filed Q3(iii)-(vi) under
Q4's keys; 105 -> 109 leaves, no flag.

Tariffs: "6 or 3" is a full mark and a partial-credit alternative: the row carries the full mark
and its note the scheme's partial line ("partial answer (3)"), never added. "two lines 7 / one
line (4)", "any two 7 / any one (4)" price the number of lines or items given: a menu priced
step by step [4, 3]. "any four lines 4 x 3", "any two 2 x 3" are menus. "//" between answers on
one line of a one-answer ask is a menu of one; between columns of two lines (Q1(i), Q1(iv)) the
sides are routes inside the card.

The scheme's mathematics is set in Cambria with an identity text layer for some glyphs (the italic
letters of v = s/t, P, I, F, a, f and λ; the bold "sin C", "Rn", X, Z, A, α and bold digits) and
the bank's glyph map for the rest: GLYPHS sets each id by the character it draws, every id read on
the rendered page (a contact sheet of each glyph at its first use, 2026-10-28), and SymbolMT's x.
Stacked fractions are read with G('fraction'); the scheme's raised hyphen minus ("s‐1", "10‐7")
reads as a superscript minus.
"""
from phys_review_lib import Q, SQ, S, M, G, L, pt, anyn, T

YEAR, LEVEL = 2020, 'ol'
REVIEWED_AT = '2026-10-28'
LETTERED = {5, 11, 12}

SOURCES = {
    'paper': {'path': 'examiner-reports/physics/papers/2020-ol-paper.pdf', 'fileid': 'LC021GLP000EV.pdf',
              'sha256': 'f882399a7073efa548667ec51704b8ba9777937ffb91d553a49787095831094d', 'pages': 12},
    'scheme': {'path': 'examiner-reports/physics/schemes/2020-ol.pdf', 'fileid': 'LC021GLP000EV.pdf',
               'sha256': '73d70952c27b742801b3b1f31f9a12bf60e5567e37303a0bfd0b263a9550415d', 'pages': 20},
}

PAGE_ROLES = {
    'paper': {1: 'cover', **{p: 'questions' for p in range(2, 11)}, 11: 'questions-acknowledgements',
              12: 'back-cover'},
    'scheme': {1: 'cover', 2: 'note', 3: 'conventions', **{p: 'marking' for p in range(4, 17)},
               **{p: 'blank' for p in range(17, 21)}},
}

# Glyph ids each read on the rendered page (contact sheets, 2026-10-28). Scheme Cambria: italic
# capitals F I P R (1832, 1835, 1842, 3019), italic a f v (1853, 1858, 1874), italic λ (2019); bold
# upright R i n s ("Rn", "sin"); bold italic A C X Z n (2157, 2159, 2180, 2182, 2196); bold α (2745);
# bold digits 0 1 2 4 6 8. SymbolMT 117 is the multiplication sign of "4 x 3". Paper Cambria 3027 is
# the italic Z of Q12(d)'s equation.
GLYPHS = {'scheme': {'Cambria': {1792: 'R', 1809: 'i', 1814: 'n', 1819: 's', 1832: 'F', 1835: 'I', 1842: 'P',
                                 1853: 'a', 1858: 'f', 1874: 'v', 2019: 'λ', 2157: 'A', 2159: 'C', 2180: 'X',
                                 2182: 'Z', 2196: 'n', 2745: 'α', 2777: '0', 2778: '1', 2779: '2', 2781: '4',
                                 2783: '6', 2785: '8', 3019: 'R'},
                     'SymbolMT': {117: '×'}},
          'paper': {'Cambria': {3027: 'Z'}}}
VERIFIED_LINES = []

QUESTION_TOTALS = {**{n: 40 for n in range(1, 5)}, **{n: 56 for n in range(5, 12)},
                   12: 112}   # any two of (a)-(d), 28 each: all four carded
PART_TOTALS = {**{(11, x): 7 for x in 'abcdefgh'}, **{(12, x): 28 for x in 'abcd'}}
BEST_OF = {5: (8, 7)}
GROUP_TOTALS = {
    (1, ('i', 'ii')): 12, (1, ('iii', 'iv', 'v')): 15, (1, ('vi', 'vii', 'viii')): 13,
    (2, ('i',)): 12, (2, ('ii', 'iii', 'iv')): 18, (2, ('v', 'vi')): 10,
    (3, ('i', 'ii')): 16, (3, ('iii', 'iv', 'v', 'vi')): 24,
    (4, ('i', 'ii', 'iii')): 18, (4, ('iv',)): 12, (4, ('v',)): 6, (4, ('vi',)): 4,
    (6, ('i',)): 6, (6, ('ii', 'iii')): 15, (6, ('iv', 'v')): 9, (6, ('vi', 'vii', 'viii')): 18, (6, ('ix', 'x')): 8,
    (7, ('i', 'ii', 'iii')): 24, (7, ('iv', 'v', 'vi')): 16, (7, ('vii', 'viii', 'ix')): 16,
    (8, ('i',)): 9, (8, ('ii', 'iii', 'iv')): 15, (8, ('v', 'vi', 'vii')): 32,
    (9, ('i', 'ii')): 12, (9, ('iii',)): 12, (9, ('iv', 'v', 'vi')): 18, (9, ('vii', 'viii')): 14,
    (10, ('i', 'ii')): 6, (10, ('iii', 'iv', 'v', 'vi')): 24, (10, ('vii', 'viii', 'ix', 'x')): 26,
}
# Q12's group marks sit under letters, which GROUP_TOTALS cannot key: checked by hand (12a: 6+3+6, 9+4;
# 12b: 6+3+6+4, 9; 12c: 3+3+9, 6+7; 12d: 3+12, 3+3+3+4), and each letter's 28 by PART_TOTALS.
CHECKSUMS = {}
ROUTES = {}

SCAN_PAGES = {'paper': range(2, 12)}
SELECTION_SCAN = [
    ('paper', 3, 'the following', 'Q3 "The student completed the following graph": a reference to the graph.'),
    ('paper', 3, 'the following', 'Q4 "The student recorded the following data": a reference to the table.'),
    ('paper', 4, 'the following', 'Q5 "Answer any eight of the following parts": a best-eight of (a)-(j) at 7 each '
                                  '(8 x 7); every part is carded (BEST_OF).'),
    ('paper', 4, 'the following', 'Q5(c) "Which of the following is the SI unit": the ask\'s own options, one answer.'),
    ('paper', 4, 'or', 'Q5(e) "a 3 A fuse or a 13 A fuse": the ask\'s own alternatives, one answer.'),
    ('paper', 5, 'or', 'Q6 stem "remains at rest or moving at a constant velocity": description.'),
    ('paper', 9, 'the following', 'Q11 "Read the following passage": a reference to the passage.'),
    ('paper', 9, 'the following', 'Q11 passage "achieving the following by 2030": passage text.'),
    ('paper', 10, 'any two', 'Q12 "Answer any two of the following parts": every part is carded.'),
    ('paper', 10, 'the following', 'Q12, the same rubric.'),
    ('paper', 10, 'or', 'Q12(b) lead-in "no markings or numbers on it": description.'),
    ('paper', 11, 'or', 'Q12(d) lead-in "one or more types of radiation": description.'),
]
ASK_SCAN_PAGES = {'paper': range(2, 12)}
ASK_EXEMPT = [
    (7, 'When two different materials are rubbed together, they', 'Q8 lead-in to (ii) ("... they become electrically '
                                                               'charged."): a description, not an ask; lifted into '
                                                               'its stem.'),
    (9, 'WHAT ARE GREENHOUSE GASES?', 'Q11 passage title: a heading, not an ask.'),
    (11, 'When the nuclei in certain atoms undergo radioactive decay', 'Q12(d) lead-in: a description, not an ask; '
                                                                     'lifted into the (i) stem.'),
]

SEC = 'State Examinations Commission'
CRIT = 'The scheme prints no answer here, only what earns the marks.'
DSL = ('The scheme\'s "//" (page 3): the answers either side are mutually exclusive; a partial answer from one '
       'side may not be taken with one from the other.')
ORDERED = ('The scheme prints these items under one sum, {cell}, and names no order: a response earns the marks '
           'step by step.')
IMAGE = ('"the image distance" reads to the figure-pointer check as a printed figure; it is the distance the '
         'student calculates, so the card links its exam page.')
LINKED = ('{w} reads to the figure-pointer check as a printed figure; the ask is the student\'s own drawing, so the '
          'card links its exam page.')


def P(page, start, end=None, **kw):
    return Q(page, start, end, **kw)


def partial(full, part, sel='partial answer', nth=1, extra=''):
    """The scheme's partial-credit line under a "full or part" answer, as the row's note."""
    return dict(note_sel=S(sel, nth=nth), note_lead=f'The scheme prices this "{full} or {part}":',
                note=f'({part}).' + (f' {extra}' if extra else ''))


def R(text, marks, end=None, **kw):
    """A row lifted whole from the task's scheme page."""
    return pt(S(text, end), marks, **kw)


def C(text, marks, end=None, note=CRIT, **kw):
    """A criterion the scheme prices without printing an answer."""
    return pt(S(text, end), marks, kind='criterion', note=note, **kw)


def FR(page, clip, expect, marks=None, **kw):
    """A stacked fraction read from where its numerator and denominator are printed."""
    spec = G('fraction', page=page, clip=clip, expect=expect, **kw)
    if marks is not None:
        spec['marks'] = marks
    return spec


def menu(sel, claim, per, sep='//', steps=None, lead=None, **kw):
    """A menu ("any one", "A // B"), with an optional note_lead for its note_sel."""
    spec = anyn(sel, claim, per, steps=steps, sep=sep, **kw)
    if lead:
        spec['note_lead'] = lead
    return spec


def items(sel, n, sep=',', psep_first=None):
    """The first n entries of a printed list, each its own slice (a trailing "etc." is left out)."""
    if psep_first:
        return [dict(sel, piece=[2, k], psep=[psep_first, sep]) for k in range(1, n + 1)]
    return [dict(sel, piece=k, psep=sep) for k in range(1, n + 1)]


# ------------------------------------------------------------------ stems --
STEM1 = P(2, 'A student performed an experiment to investigate the principle of conservation of',
          'they travel along the track.')
MASS1 = [P(2, 'Before setting up the experiment, the student measured the mass of each trolley.'),
         P(2, 'Mass of trolley A = 0.38 kg'), P(2, 'Mass of trolley B = 0.35 kg')]
VEL1 = P(2, 'To calculate the velocity of the trolleys, the student measured distance and time.')
DATA1 = [P(2, 'Starting velocity of trolley A = 1.5 m s⁻¹.'), P(2, 'Starting velocity of trolley B = 0 m s⁻¹.'),
         P(2, 'Final velocity of trolleys A and B together = 0.78 m s⁻¹.'),
         P(2, 'The principle of conservation of momentum states that the momentum before the collision',
           'is equal to the momentum after the collision.'),
         P(2, 'The momentum of trolley A before the collision = 0.38 × 1.5 = 0.57 kg m s⁻¹.')]
STEM2 = P(2, 'A student carried out an experiment to measure the focal length of a concave mirror.')
Q2I = P(2, 'Draw a labelled diagram of the apparatus used in this experiment.', nth=2)
Q2III = P(2, 'On your diagram, indicate and label the measurements taken by the student.')
STEM3 = P(3, 'A student carried out an experiment to investigate how the fundamental frequency of a',
          'stretched string changes with length.')
Q3I = P(3, 'Draw a labelled diagram of the apparatus used in this experiment.')
GRAPH3 = P(3, 'The student completed the following graph to show the relationship between length and', 'frequency.')
STEM4 = P(3, 'A student performed an experiment to investigate how the resistance of a metallic',
          'conductor changes with temperature.')
TABLE4 = [P(3, 'The student recorded the following data:'), P(3, 'Temperature (°C)', '8.4')]
FIRST6 = P(5, 'Newton’s first law of motion states that a body remains at rest or moving',
           'unbalanced external force acts on it.')
SECOND6 = P(5, 'Newton’s second law of motion states that the force on an object is proportional to its rate',
            'of change of momentum.')
CAR6 = P(5, 'A car of mass 700 kg is at rest.', 'travelling at a velocity of 18 m s⁻¹.')
Q6VIII = P(5, 'Calculate the net force on the car as it accelerates.')
DRIVE6 = P(5, 'The engine of the car provides a driving force of 3000 N.')
REFR7 = P(6, 'Refraction is the bending of light as it passes from one medium into', 'another.')
CONV7 = P(6, 'A converging lens refracts light.')
LENS7 = P(6, 'A converging lens has focal length 15 cm (f = 15 cm). An object is placed 20 cm in front of',
          'the lens (u = 20 cm).')
GLE8 = P(7, 'A gold leaf electroscope is used to perform experiments', 'involving static electricity.')
RUB8 = P(7, 'When two different materials are rubbed together, they', 'become electrically charged.')
LIGHT9 = P(8, 'Light travels as a wave of electromagnetic radiation. The colour of the light depends on its', 'frequency.')
SOUND9 = P(8, 'Sound also travels as a wave. Sound is an example of a mechanical wave.')
REFL9 = P(8, 'Sound waves undergo reflection, refraction, diffraction and interference.')
AMB9 = P(8, 'As an ambulance passes a stationary observer, its siren emits a sound of a particular',
         'caused by the Doppler effect.')
STONEY10 = P(8, 'Irish physicist G.J. Stoney named the electron in 1891.', 'in 1897.')
THERM10 = P(8, 'Electrons are produced in a cathode ray tube by thermionic emission.')
PHOTO10 = P(8, 'The photoelectric effect is the emission of electrons', 'frequency falls on it.')
XRAY10 = P(8, 'The picture shows an X‐ray tube.')
GASES11 = P(9, 'A wide range of gases contribute to climate change.', 'effect by absorbing infrared radiation.')
IMPACT11 = P(9, 'The impact of greenhouse gas emissions on climate disruption must be addressed.',
             'point where these crises will get much worse.')
PLAN11 = P(9, 'Ireland’s climate change plan contains important measures',
           '• At least half a million electric vehicles on the road, with additional charging infrastructure.')
BUS12 = P(10, 'A bus travels 30 km in 28 minutes at a constant speed.')
Q12AI = P(10, 'Convert 30 km into metres.')
Q12AII = P(10, 'Convert 28 minutes into seconds.')
BRAKE12 = P(10, 'The driver applies the brakes and brings the bus to a stop in 30 seconds.')
THERMO12 = P(10, 'A thermometer is used to measure temperature.')
PROP12 = P(10, 'A thermometer is based on a particular thermometric property.')
UNCAL12 = P(10, 'An uncalibrated thermometer is one that has no markings or numbers on it.')
CURR12 = P(10, 'An electric current is a flow of electric charge. A material that allows electric charge to flow',
           'through it is called an electrical conductor.')
RAD12 = P(11, 'When the nuclei in certain atoms undergo radioactive decay, they emit one or more types of',
          'radiation – alpha, beta and gamma.')
EQ12 = P(11, 'The nuclear equation below shows the alpha decay of an isotope of radon.')

TASKS = [
    # ============================================================ Section A ==
    # ---------------------------------------------------------------- Q1 --
    T('1i', 'Q1(i)', 'A', P(2, 'Draw a labelled diagram of the apparatus used in this experiment.'),
      [pt(S('runway //air track', piece=1, psep='//'), 3, route='side-a', note=DSL),
       pt(S('two trolleys // two gliders/riders', piece=1, psep='//'), 3, route='side-a'),
       pt(S('runway //air track', piece=2, psep='//'), 3, route='side-b'),
       pt(S('two trolleys // two gliders/riders', piece=2, psep='//'), 3, route='side-b'),
       R('detail e.g. timer, sticking mechanism', 3,
         note_sel=S('NOTE: no labels deduct 2', 'accept valid alternatives e.g. data logging methods'))],
      'phys-u2', 'momentum-apparatus', SQ(4, 'Draw a labelled diagram of the apparatus used in this experiment.'), 9,
      stem=[STEM1],
      decision='"3 × 3": the first two lines print a runway and trolleys "//" an air track and gliders (each side a '
               'route at 3 + 3), the detail line is common.'),
    T('1ii', 'Q1(ii)', 'A', P(2, 'How did the student measure the masses of the trolleys?'),
      [R('used electronic balance / mass balance / weighing scales / weigh them', 3)], 'phys-u2', 'measuring-mass',
      SQ(4, 'How did the student measure the masses of the trolleys?'), 3, stem=[STEM1]),
    T('1iii', 'Q1(iii)', 'A', P(2, 'Describe how the distance was measured.'),
      [R('metre stick/ measuring tape', 3)], 'phys-u2', 'measuring-distance',
      SQ(4, 'Describe how the distance was measured.'), 3, stem=[STEM1, VEL1]),
    T('1iv', 'Q1(iv)', 'A', P(2, 'Describe how the time was measured.'),
      [pt(S('tickertape / timer'), 3, route='side-a', note=DSL),
       pt(S('time between dots is 0.02 s // difference between entry/exit times', piece=1, psep='//'), 3, route='side-a'),
       pt(S('// photogates / timer', piece=2, psep='//'), 3, route='side-b'),
       pt(S('time between dots is 0.02 s // difference between entry/exit times', piece=2, psep='//'), 3,
          route='side-b')],
      'phys-u2', 'measuring-time', SQ(4, 'Describe how the time was measured.'), 6, stem=[STEM1, VEL1],
      decision='"3 + 3": two columns separated by "//" (ticker tape, or photogates): each side a route at 3 + 3.'),
    T('1v', 'Q1(v)', 'A', P(2, 'How did the student use the distance and the time to calculate the velocity?'),
      [FR(4, (110, 443, 145, 466), 'v= s/t', 6, route='side-a', note_sel=S('partial answer'),
          note_lead='The scheme prices this "6 or 3":', note='(3). ' + DSL),
       pt(S('ₜ // slope of distance versus time graph', piece=2, psep='//'), 6, route='side-b', **partial(6, 3))],
      'phys-u2', 'calculating-velocity',
      SQ(4, 'How did the student use the distance and the time to calculate the velocity?'), 6, stem=[STEM1, VEL1],
      decision='"6 or 3": the formula "//" the slope of a distance-time graph, each side a route at 6; the partial '
               'answer (3) is each side\'s note.'),
    T('1vi', 'Q1(vi)', 'A', P(2, 'What is the momentum of trolley B before the collision?'),
      [R('0 kg m s⁻¹', 3)], 'phys-u2', 'momentum-of-b',
      SQ(4, 'What is the momentum of trolley B before the collision?'), 3, stem=MASS1 + DATA1),
    T('1vii', 'Q1(vii)', 'A', P(2, 'Calculate the combined momentum of trolleys A and B after the collision.',
                               '(Show your work.)'),
      [R('(0.38 + 0.35)(0.78) = 0.569 kg m s⁻¹', 6, **partial(6, 3))], 'phys-u2', 'momentum-after',
      SQ(4, 'Calculate the combined momentum of trolleys A and B after the collision.', '(Show your work.)'), 6,
      stem=MASS1 + DATA1),
    T('1viii', 'Q1(viii)', 'A', P(2, 'Was momentum conserved in this collision? Explain your answer.'),
      [R('yes', 2), R('momentum before was the same as momentum after', 2)], 'phys-u2', 'momentum-conserved',
      SQ(4, 'Was momentum conserved in this collision? Explain your answer.'), 4, stem=DATA1,
      decision='"2 + 2" against the two lines: in the order printed.'),
    # ---------------------------------------------------------------- Q2 --
    T('2i', 'Q2(i)', 'A', Q2I,
      [anyn(None, 4, 3, options=[S('concave mirror'), S('object e.g. crosswire'), S('image / screen'),
                                 S('correct arrangement'), S('detail e.g. optical bench, metre stick, ray‐box, etc.')],
            note_sel=S('any 4 lines correct', 'accept valid alternatives'))],
      'phys-u2', 'concave-mirror-apparatus',
      SQ(5, 'Draw a labelled diagram of the apparatus used in this experiment.'), 12, stem=[STEM2],
      decision='"labelled diagram to show:" five lines, "any 4 lines correct 4 × 3": a menu of four claims at 3; the '
               'scheme\'s notes (approximate method maximum 3 × 3, no labels deduct 2) are the row\'s note.'),
    T('2ii', 'Q2(ii)', 'A', P(2, 'State the formula used to calculate the focal length.'),
      [FR(5, (110, 274, 166, 299), '1/u + 1/v = 1/f', 6, **partial(6, 3))], 'phys-u2', 'mirror-formula',
      SQ(5, 'State the formula used to calculate the focal length.'), 6, stem=[STEM2]),
    T('2iii', 'Q2(iii)', 'A', Q2III,
      [R('correctly marked u and v distances', 6, **partial(6, 3))], 'phys-u2', 'marking-u-and-v',
      SQ(5, 'On your diagram, indicate and label the measurements taken by the student.'), 6,
      stem=[STEM2, M('(i)', 2), Q2I], source_pages=[2], decision=LINKED.format(w='"your diagram"')),
    T('2iv', 'Q2(iv)', 'A', P(2, 'What instrument was used to take these measurements?'),
      [menu(S('metre stick/ measuring tape // optical bench scale'), 1, 6)], 'phys-u2', 'measuring-instrument',
      SQ(5, 'What instrument was used to take these measurements?'), 6, stem=[STEM2, M('(iii)', 2), Q2III],
      decision='A "name one" ask printed "A // B": a menu of one.'),
    T('2v', 'Q2(v)', 'A', P(2, 'Why did the student measure the approximate focal length at the start of the',
                            'experiment?'),
      [menu(S('to ensure the object is placed outside the focal point // for a real image'), 1, 6,
            lead='The scheme prices this "6 or 3":', note_sel=S('partial answer'), note='(3).')],
      'phys-u2', 'approximate-focal-length',
      SQ(5, 'Why did the student measure the approximate focal length at the start of the', 'experiment?'), 6,
      stem=[STEM2]),
    T('2vi', 'Q2(vi)', 'A', P(2, 'The image distance is the less accurate measurement. Explain why.'),
      [R('difficult to decide location of sharpest image', 4)], 'phys-u2', 'image-distance-accuracy',
      SQ(5, 'The image distance is the less accurate measurement. Explain why.'), 4, stem=[STEM2], source_pages=[2],
      decision='"The image distance" reads to the figure-pointer check as a printed figure; it is the distance the '
               'student measures, so the card links its exam page.'),
    # ---------------------------------------------------------------- Q3 --
    T('3i', 'Q3(i)', 'A', Q3I,
      [anyn(None, 4, 3, options=[S('string'), S('means of changing frequency e.g. tuning forks / frequency generator'),
                                 S('means of varying length e.g. bridge'), S('means of measuring length'),
                                 S('means of detecting resonance /paper rider /magnet'),
                                 S('detail e.g. sonometer, means of tightening')],
            note_sel=S('any four lines', 'accept valid alternatives'))],
      'phys-u2', 'sonometer-apparatus', SQ(6, 'Draw a labelled diagram of the apparatus used in this experiment.'), 12,
      stem=[STEM3],
      decision='"labelled diagram to show:" six lines, "any four lines 4 × 3": a menu of four claims at 3.'),
    T('3ii', 'Q3(ii)', 'A', P(3, 'On your diagram, indicate and label the length measured by the student.'),
      [R('distance between the bridges shown on the diagram', 4)], 'phys-u2', 'length-measured',
      SQ(6, 'On your diagram, indicate and label the length measured by the student.'), 4,
      stem=[STEM3, M('(i)', 3), Q3I], source_pages=[3], decision=LINKED.format(w='"your diagram"')),
    T('3iii', 'Q3(iii)', 'A', P(3, 'How did the student measure the frequency values?'),
      [menu(S('noted it from tuning forks // read it from signal generator'), 1, 6,
            lead='The scheme prices this "6 or 3":', note_sel=S('partial answer'), note='(3).')],
      'phys-u2', 'measuring-frequency', SQ(6, 'How did the student measure the frequency values?'), 6, stem=[STEM3]),
    T('3iv', 'Q3(iv)', 'A', P(3, 'How did the student set the string vibrating?'),
      [menu(S('placed a vibrating tuning fork on bridge // varied the frequency of the signal generator'), 1, 6,
            lead='The scheme prices this "6 or 3":', note_sel=S('partial answer'), note='(3).')],
      'phys-u2', 'setting-the-string-vibrating', SQ(6, 'How did the student set the string vibrating?'), 6,
      stem=[STEM3]),
    T('3v', 'Q3(v)', 'A', P(3, 'The length between the bridges is adjusted until resonance occurs.',
                            'Describe how the student knew that resonance had occurred.'),
      [menu(S('paper rider falls off // loudest sound'), 1, 6,
            lead='The scheme prices this "6 or 3":', note_sel=S('partial answer'), note='(3).')],
      'phys-u2', 'detecting-resonance',
      SQ(6, 'The length between the bridges is adjusted until resonance occurs. Describe how the',
         'student knew that resonance had occurred.'), 6, stem=[STEM3]),
    T('3vi', 'Q3(vi)', 'A', P(3, 'State the relationship between the resonance frequency and the length.'),
      [menu(None, 1, 6, lead='The scheme prices this "6 or 3":', note_sel=S('partial answer'), note='(3).',
            options=[FR(6, (110, 712, 150, 735), 'f ∝ 1/l'),
                     S('ₗ / frequency is inversely proportional to the length // fl = constant', piece=[2, 1],
                       psep=[' / ', '//']),
                     S('ₗ / frequency is inversely proportional to the length // fl = constant', piece=2, psep='//')])],
      'phys-u2', 'frequency-length-relationship',
      SQ(6, 'State the relationship between the resonance frequency and the length.'), 6, stem=[STEM3, GRAPH3],
      fig='q3-graph',
      decision='Three printed statements of the one relationship ("/" then "//"): a menu of one at 6.'),
    # ---------------------------------------------------------------- Q4 --
    T('4i', 'Q4(i)', 'A', P(3, 'Name the instrument used to measure resistance.'),
      [R('ohmmeter', 6, **partial(6, 3, sel='partial e.g. multimeter'))], 'phys-u2', 'measuring-resistance',
      SQ(7, 'Name the instrument used to measure resistance.'), 6, stem=[STEM4]),
    T('4ii', 'Q4(ii)', 'A', P(3, 'Name the instrument used to measure temperature.'),
      [R('thermometer / temperature probe', 6)], 'phys-u2', 'measuring-temperature',
      SQ(7, 'Name the instrument used to measure temperature.'), 6, stem=[STEM4]),
    T('4iii', 'Q4(iii)', 'A', P(3, 'How did the student change the temperature of the metallic conductor?'),
      [R('placed in liquid', 3), R('source of heat', 3)], 'phys-u2', 'changing-the-temperature',
      SQ(7, 'How did the student change the temperature of the metallic conductor?'), 6, stem=[STEM4],
      decision='"2 × 3" against the two lines: one row each at 3.'),
    T('4iv', 'Q4(iv)', 'A', P(3, 'Use the data to plot a graph to show the relationship between resistance and',
                              'temperature.'),
      [C('label axes correctly, (name / symbol / unit acceptable)', 3),
       C('plot six points correctly', 6, note_sel=S('‐1 for each error thereafter')),
       C('straight line', 3, note_sel=S('if graph paper is not used, maximum mark 3 × 3'))],
      'phys-u2', 'resistance-temperature-graph',
      SQ(7, 'Use the data to plot a graph to show the relationship between resistance and', 'temperature.'), 12,
      stem=[STEM4] + TABLE4, fig='q4iv-scheme-graph',
      decision='"3 + 6 + 3" against the three criteria, in the order printed; the scheme draws the graph (the '
               'solution figure). The data table is lifted into the stem.'),
    T('4v', 'Q4(v)', 'A', P(3, 'Describe the relationship between resistance and temperature.'),
      [menu(S('resistance increases with temperature // linear'), 1, 6,
            lead='The scheme prices this "6 or 3":', note_sel=S('partial answer'), note='(3).')],
      'phys-u2', 'resistance-temperature-relationship',
      SQ(7, 'Describe the relationship between resistance and temperature.'), 6, stem=[STEM4] + TABLE4),
    T('4vi', 'Q4(vi)', 'A', P(3, 'State one safety precaution that the student should have taken.'),
      [R('use a tongs / avoid being burnt, etc.', 4, **partial(4, 2))], 'phys-u2', 'safety-precaution',
      SQ(7, 'State one safety precaution that the student should have taken.'), 4, stem=[STEM4]),
    # ============================================================ Section B ==
    # ---------------------------------------------------------------- Q5 --
    T('5a', 'Q5(a)', 'B', [P(4, 'Explain Archimedes’ principle.'), P(4, 'The diagram may help you answer.', br=True)],
      [menu(None, 2, 4, steps=[4, 3], lead='The scheme prices', note_sel=S('two lines'), note='7; one line (4).',
            options=[S('upthrust (apparent loss in weight) ='), S('weight of displaced fluid')])],
      'phys-1-2', 'archimedes-principle', SQ(8, 'Explain Archimedes’ principle.'), 7, fig='q5a-diagram',
      decision='"two lines 7, one line (4)": each printed line is an option, a menu priced step by step [4, 3].'),
    T('5b', 'Q5(b)', 'B', P(4, 'What is meant by latent heat?'),
      [R('heat/energy needed to change state', 7, **partial(7, 4))], 'phys-2-1', 'latent-heat',
      SQ(8, 'What is meant by latent heat?'), 7),
    T('5c', 'Q5(c)', 'B', [P(4, 'Which of the following is the SI unit of capacitance?'), P(4, 'ampere', 'volt', br=True)],
      [R('farad', 7)], 'phys-3-2', 'unit-of-capacitance',
      SQ(8, 'Which of the following is the SI unit of capacitance?'), 7,
      decision='The scheme reprints the four options and sets the answer, farad, in bold: the row is that option.'),
    T('5d', 'Q5(d)', 'B', P(4, 'State Boyle’s law.'),
      [menu(None, 1, 7, lead='The scheme prices this "7 or 4":', note_sel=S('partial answer'), note='(4).',
            options=[S('pressure and volume are inversely proportional // PV = k // P∝', piece=1, psep='//'),
                     S('pressure and volume are inversely proportional // PV = k // P∝', piece=2, psep='//'),
                     FR(8, (385, 262, 412, 286), 'P∝ 1/V')])],
      'phys-2-1', 'boyles-law', SQ(8, 'State Boyle’s law.'), 7,
      decision='Three statements of the law separated by "//": a menu of one at 7.'),
    T('5e', 'Q5(e)', 'B', P(4, 'An electric heater has a power rating of 1500 W.', 'Justify your answer.'),
      [menu(None, 2, 4, steps=[4, 3], lead='The scheme prices', note_sel=S('two lines'), note='7; one line (4).',
            options=[S('13 A'), FR(8, (110, 351, 410, 376),
                                   '1500/230 / 6.5 A / I= P/V / P = VI / current too big ./ fuse would blow')])],
      'phys-3-3', 'choosing-a-fuse',
      SQ(8, 'An electric heater has a power rating of 1500 W. It uses a voltage of', 'Justify your answer.'), 7,
      decision='"two lines 7, one line (4)": the fuse and its justification, each line an option, a menu priced '
               'step by step [4, 3].'),
    T('5f', 'Q5(f)', 'B', P(4, 'What is a magnetic field?'),
      [menu(None, 2, 4, steps=[4, 3], lead='The scheme prices', note_sel=S('two lines'), note='7; one line (4).',
            options=[S('region/space'), S('where magnetic forces can be experienced')])],
      'phys-3-4', 'magnetic-field', SQ(8, 'What is a magnetic field?'), 7,
      decision='"two lines 7, one line (4)": each printed line is an option, a menu priced step by step [4, 3].'),
    T('5g', 'Q5(g)', 'B', P(4, 'Ultraviolet light is on the electromagnetic spectrum. State two properties of',
                            'ultraviolet light.'),
      [menu(None, 2, 4, steps=[4, 3], lead='The list ends "etc." (open); the scheme prices', open_list=True,
            note_sel=S('any two'), note='7; any one (4).',
            options=items(S('travels at c, high energy/frequency, causes ionisation, etc.'), 3))],
      'phys-2-4', 'properties-of-ultraviolet',
      SQ(8, 'Ultraviolet light is on the electromagnetic spectrum. State two properties of', 'ultraviolet light.'), 7,
      decision='"any two 7, any one (4)": a menu priced step by step [4, 3].'),
    T('5h', 'Q5(h)', 'B', P(4, 'A pair of complementary colours consists of a primary colour and a secondary',
                            'Name a pair of complementary colours.'),
      [menu(S('blue and yellow // red and turquoise/cyan // green and magenta'), 1, 7,
            lead='The scheme prices this "7 or 4":', note_sel=S('partial answer'), note='(4).')],
      'phys-2-4', 'complementary-colours',
      SQ(8, 'A pair of complementary colours consists of a primary colour and a secondary',
         'Name a pair of complementary colours.'), 7),
    T('5i', 'Q5(i)', 'B', P(4, 'Name the piece of equipment on the right.'),
      [R('spectrometer', 7, **partial(7, 4, sel='partial answer e.g. collimator, turntable, telescope'))],
      'phys-2-6', 'spectrometer', SQ(8, 'Name the piece of equipment on the right.'), 7, fig='q5i-spectrometer'),
    T('5j', 'Q5(j)', 'B', P(4, 'What is nuclear fusion?'),
      [R('joining of two nuclei with the release of energy', 7, **partial(7, 4))], 'phys-4-6', 'nuclear-fusion',
      SQ(8, 'What is nuclear fusion?'), 7),
    # ---------------------------------------------------------------- Q6 --
    T('6i', 'Q6(i)', 'B', P(5, 'A block weighs 400 N. A crane lifts the block so that it moves upwards with constant',
                            'block.'),
      [R('(crane force up = weight of block down = )400 N', 6,
         **partial(6, 3, sel='partial answer e.g. zero acceleration'))],
      'phys-1-2', 'force-from-first-law',
      SQ(9, 'A block weighs 400 N. A crane lifts the block so that it moves upwards', 'puts on the block.'), 6,
      stem=[FIRST6]),
    T('6ii', 'Q6(ii)', 'B', P(5, 'Calculate the resultant (net) force on the 9 kg object in the diagram above.',
                              'In what direction does it act?'),
      [R('2 N to the right', 6, **partial(6, 3))], 'phys-1-2', 'resultant-force',
      SQ(9, 'Calculate the resultant (net) force on', 'In what direction does it act?'), 6, stem=[SECOND6],
      fig='q6-forces'),
    T('6iii', 'Q6(iii)', 'B', P(5, 'Calculate the acceleration of the 9 kg object.'),
      [FR(9, (110, 330, 235, 352), '(a= F/m = 2/9 =) 0.22 m s⁻²', 9,
          note='The scheme prices this "9 or 6 or 3": one error (6), partial answer (3).')],
      'phys-1-2', 'acceleration-of-object', SQ(9, 'Calculate the acceleration of the 9 kg object.'), 9,
      stem=[SECOND6], fig='q6-forces'),
    T('6iv', 'Q6(iv)', 'B', P(5, 'State Newton’s third law of motion.'),
      [R('to every action there is an equal but opposite reaction', 6, **partial(6, 3))], 'phys-1-2',
      'newtons-third-law', SQ(9, 'State Newton’s third law of motion.'), 6),
    T('6v', 'Q6(v)', 'B', P(5, 'Use Newton’s third law to explain how a rocket takes off. (A labelled diagram may',
                            'help your answer.)'),
      [R('when the rocket forces gas down, the gas applies a force up on the rocket', 3)], 'phys-1-2',
      'rocket-take-off',
      SQ(9, 'Use Newton’s third law to explain how a rocket takes off. (A labelled diagram', 'may help your answer.)'), 3,
      decision='The scheme prints the part\'s tariff "3" and the row\'s cell in brackets, "(3)": the full mark.'),
    T('6vi', 'Q6(vi)', 'B', P(5, 'Calculate the kinetic energy of the car when it is travelling at 18 m s⁻¹.'),
      [R('(E = ½mv² = ½(700)(18)² = ) 113400 J', 6, **partial(6, 3))], 'phys-1-4', 'kinetic-energy-of-car',
      SQ(9, 'Calculate the kinetic energy of the car when it is travelling at 18 m s⁻¹.'), 6, stem=[CAR6]),
    T('6vii', 'Q6(vii)', 'B', P(5, 'Calculate the acceleration of the car.'),
      [FR(9, (108, 564, 228, 584.5), '(a= (v−u)/t = (18−0)/6 =) 3 m s⁻²', 6, **partial(6, 3))],
      'phys-1-1', 'acceleration-of-car', SQ(9, 'Calculate the acceleration of the car.'), 6, stem=[CAR6]),
    T('6viii', 'Q6(viii)', 'B', Q6VIII,
      [R('(F = ma = (700)(3)=) 2100 N', 6, **partial(6, 3))], 'phys-1-2', 'net-force-on-car',
      SQ(9, 'Calculate the net force on the car as it accelerates.'), 6, stem=[CAR6]),
    T('6ix', 'Q6(ix)', 'B', P(5, 'Calculate the friction acting on the car.'),
      [R('(3000 – 2100 = )900 N', 4)], 'phys-1-2', 'friction-on-car',
      SQ(9, 'Calculate the friction acting on the car.'), 4, stem=[CAR6, M('(viii)', 5), Q6VIII, DRIVE6]),
    T('6x', 'Q6(x)', 'B', P(5, 'State one method of reducing friction.'),
      [menu(S('oil moving parts // smooth road surface, etc.'), 1, 4, open_list=True,
            note='The scheme ends its list "etc.": the list is open.')],
      'phys-1-2', 'reducing-friction', SQ(9, 'State one method of reducing friction.'), 4),
    # ---------------------------------------------------------------- Q7 --
    T('7i', 'Q7(i)', 'B', P(6, 'State Snell’s law of refraction.'),
      [menu(None, 1, 6, lead='The scheme prices this "6 or 3":', note_sel=S('partial answer'), note='(3).',
            options=[S('sine of the angle of incidence is proportional to sine of the angle of refraction //', piece=1,
                       psep='//'),
                     FR(10, (110, 134, 185, 159), 'sini/(sinr) = constant'),
                     S('sinr= constant // sin i ∝ sin r', piece=2, psep='//')])],
      'phys-2-3', 'snells-law', SQ(10, 'State Snell’s law of refraction.'), 6, stem=[REFR7],
      decision='The law in words "//" as a ratio "//" as a proportion: a menu of one at 6.'),
    T('7ii', 'Q7(ii)', 'B', P(6, 'Describe an experiment to demonstrate Snell’s law.'),
      [R('apparatus: glass/plastic block', 3), R('ray box / laser / optical pins / protractor', 3),
       R('procedure: draw refracted rays and measure values for i and r', 3),
       R('observation /conclusion: Sin i ∝ sin r', 3)],
      'phys-2-3', 'snells-law-experiment', SQ(10, 'Describe an experiment to demonstrate Snell’s law.'), 12,
      stem=[REFR7], decision='"4 × 3" against the four lines: one row each.'),
    T('7iii', 'Q7(iii)', 'B', P(6, 'A beam of light travelling from air strikes the surface of water.', 'index of water.'),
      [FR(10, (110, 293.5, 230, 315), '(n = sin36/(sin26) = 0.588/0.438 =) 1.34', 6, **partial(6, 3))],
      'phys-2-3', 'refractive-index-of-water',
      SQ(10, 'A beam of light travelling from air strikes the surface of water. The angle of incidence',
         'index of water.'), 6, stem=[REFR7]),
    T('7iv', 'Q7(iv)', 'B', P(6, 'What does C stand for in the formula written above?'),
      [R('critical angle', 6, **partial(6, 3))], 'phys-2-3', 'critical-angle',
      SQ(10, 'What does C stand for in the formula written above?'), 6, qfig='q7iv-question',
      decision='The paper sets n = 1/sin C as a stacked fraction the text layer breaks: the ask is shown as printed '
               'with the formula above it.'),
    T('7v', 'Q7(v)', 'B', P(6, 'Copy and complete the diagram below to show the paths of the rays of light after they',
                            'strike the converging lens.'),
      [C('correct diagram', 6, note=CRIT + ' The scheme prices this "6 or 3": partial answer (3).')],
      'phys-2-3', 'rays-through-converging-lens',
      SQ(10, 'Copy and complete the diagram below to show the paths of the rays of light after they',
         'strike the converging lens.'), 6, stem=[CONV7], qfig='q7v-question', fig='q7v-scheme',
      decision='The ask is shown as printed with its lens; the scheme prices "correct diagram" and draws it (the '
               'solution figure).'),
    T('7vi', 'Q7(vi)', 'B', P(6, 'Explain the underlined term.'),
      [menu(S('one formed by the apparent intersection of rays // image not formed on screen'), 1, 4)],
      'phys-2-3', 'virtual-image', SQ(10, 'Explain the underlined term.'), 4,
      stem=[P(6, 'A converging lens can be used to produce a magnified virtual image.')], qfig='q7vi-question',
      decision='The ask points at the underlined word, which the text layer does not mark: shown as printed.'),
    T('7vii', 'Q7(vii)', 'B', P(6, 'Calculate the image distance, v.'),
      [FR(10, (110, 622, 335, 645), '( 1/v = 1/f − 1/u = 1/15 − 1/20 = 1/60 ) v = 60 cm', 6, **partial(6, 3))],
      'phys-2-3', 'image-distance', SQ(10, 'Calculate the image distance, v.'), 6, stem=[LENS7], source_pages=[6],
      decision=IMAGE),
    T('7viii', 'Q7(viii)', 'B', P(6, 'Calculate the magnification, m.'),
      [FR(10, (110, 672, 180, 696), '(m = v/u = 60/20 =) 3', 6, **partial(6, 3))], 'phys-2-3', 'magnification',
      SQ(10, 'Calculate the magnification, m.'), 6,
      stem=[LENS7, M('(vii)', 6), P(6, 'Calculate the image distance, v.')], source_pages=[6], decision=IMAGE),
    T('7ix', 'Q7(ix)', 'B', P(6, 'State one use of a lens.'),
      [menu(None, 1, 4, open_list=True, note_sel=S('any one'), lead='The list ends "etc." (open); the scheme prices',
            note='4.', options=items(S('magnifying glass, eye glasses /spectacles, camera, telescope etc.'), 3)
            + [S('magnifying glass, eye glasses /spectacles, camera, telescope etc.', piece=[4, 1],
                 psep=[',', ' etc.'])])],
      'phys-2-3', 'use-of-a-lens', SQ(10, 'State one use of a lens.'), 4,
      decision='"any one 4" against a list ending "etc.": an open menu of one.'),
    # ---------------------------------------------------------------- Q8 --
    T('8i', 'Q8(i)', 'B', P(7, 'Name the parts of the gold leaf electroscope', 'labelled A, B and C.'),
      [R('A = (metal) cap / disc', 3), R('B = insulation', 3), R('C = (gold) leaf', 3)], 'phys-3-1',
      'parts-of-electroscope', SQ(11, 'Name the parts of the gold leaf electroscope labelled A, B and C.'), 9,
      stem=[GLE8], fig='q8-electroscope',
      labels=[L('A', S('A = (metal) cap / disc', piece=2, psep=' = ', page=11), True),
              L('B', S('B = insulation', piece=2, psep=' = ', page=11), True),
              L('C', S('C = (gold) leaf', piece=2, psep=' = ', page=11), True)]),
    T('8ii', 'Q8(ii)', 'B', P(7, 'Describe how a student would charge a plastic rod.'),
      [R('rub with a (dry) cloth / fur', 6, **partial(6, 3))], 'phys-3-1', 'charging-a-rod',
      SQ(11, 'Describe how a student would charge a plastic rod.'), 6, stem=[RUB8]),
    T('8iii', 'Q8(iii)', 'B', P(7, 'How would the student use a gold leaf electroscope to show that the rod is charged?'),
      [menu(S('bring the charged rod close to the cap // touch the cap with the charged rod'), 1, 3),
       R('leaf moves', 3, note_sel=S('partial answer'), note_lead='The scheme prints under this line:',
         note='(3).')],
      'phys-3-1', 'showing-the-rod-is-charged',
      SQ(11, 'How would the student use a gold leaf electroscope to show that the rod is charged?'), 6,
      decision='"2 × 3": the first line prints two ways separated by "//" (a menu of one at 3), then "leaf moves" '
               '[3]; the scheme\'s partial line "(3)" is the second row\'s note.'),
    T('8iv', 'Q8(iv)', 'B', P(7, 'State the SI unit of electric charge.'),
      [R('coulomb', 3)], 'phys-3-1', 'unit-of-charge', SQ(11, 'State the SI unit of electric charge.'), 3,
      decision='The scheme prints the part\'s tariff "3" and the row\'s cell in brackets, "(3)": the full mark.'),
    T('8v', 'Q8(v)', 'B', P(7, 'The photograph above shows a charged plastic rod attracting small pieces of paper',
                            'to it. Explain how this happens.'),
      [R('charged rod induces opposite charge on the paper', 6, **partial(6, 3)),
       R('opposite charges attract', 6, **partial(6, 3, nth=2))],
      'phys-3-1', 'charged-rod-attracts-paper',
      SQ(11, 'The photograph above shows a charged plastic rod attracting', 'small pieces of paper to it. Explain how this happens.'),
      12, fig='q8v-photo', decision='"2(6 or 3)": two answers, each 6 with its own partial (3).'),
    T('8vi', 'Q8(vi)', 'B', P(7, 'Describe, with the aid of a labelled diagram, an experiment to show an electric field',
                              'including its direction.'),
      [R('dish of (castor) oil', 3), R('high voltage source', 3), R('two electrodes/plates', 3),
       R('semolina forms electric field pattern', 3),
       R('field lines go from positive to negative', 3, note_sel=S('a labelled diagram may merit full marks'))],
      'phys-3-2', 'electric-field-pattern-experiment',
      SQ(11, 'Describe, with the aid of a labelled diagram, an experiment to show an electric field',
         'including its direction.'), 15, fig='q8vi-scheme',
      cells='The [3] printed against "high voltage source" shares its baseline with the label "castor oil" of the '
            'diagram drawn beside it, so the reader gives the cell to the label: the scheme prints 5 × 3 against '
            'these five rows.',
      decision='"5 × 3" against the five lines; the scheme draws the arrangement (the solution figure).'),
    T('8vii', 'Q8(vii)', 'B', P(7, 'Coulomb’s law describes the force between static charges. It is an example of an',
                                'State another example of an inverse square law.'),
      [menu(None, 1, 5, lead='The scheme prices this "5 or 3":', note_sel=S('partial answer'), note='(3).',
            options=[S('Newton’s law of universal gravitation // F∝', piece=1, psep='//'),
                     FR(11, (274, 698, 312, 721), 'F∝ Mm/d²')])],
      'phys-1-5', 'another-inverse-square-law',
      SQ(11, 'Coulomb’s law describes the force between static charges. It is an example of an',
         'State another example of an inverse square law.'), 5,
      decision='The law in words "//" as a proportion: a menu of one at 5.'),
    # ---------------------------------------------------------------- Q9 --
    T('9i', 'Q9(i)', 'B', [P(8, 'Light is an example of a transverse wave. Explain what is meant by a transverse wave.'),
                           P(8, '(A labelled diagram may help your answer.)', br=True)],
      [R('disturbance is perpendicular to direction of propagation of the wave', 6, **partial(6, 3))],
      'phys-2-2', 'transverse-wave',
      SQ(12, 'Light is an example of a transverse wave. Explain what is meant by a transverse wave.'), 6,
      stem=[LIGHT9]),
    T('9ii', 'Q9(ii)', 'B', P(8, 'Orange light has a frequency of 5 × 10¹⁴ Hz. The speed of light is 3 × 10⁸ m s⁻¹.',
                              'Calculate the wavelength of the orange light.'),
      [FR(12, (110, 182, 260, 206), '(λ= c/f = (3 ×10⁸)/(5 ×10¹⁴) =) 6 × 10⁻⁷ m', 6, **partial(6, 3))],
      'phys-2-2', 'wavelength-of-orange-light',
      SQ(12, 'Orange light has a frequency of 5 × 10¹⁴ Hz. The speed of light is 3 × 10⁸ m s⁻¹.',
         'Calculate the wavelength of the orange light.'), 6, stem=[LIGHT9]),
    T('9iii', 'Q9(iii)', 'B', P(8, 'Describe an experiment to show that sound needs a medium to travel through.'),
      [menu(None, 2, 3, note_sel=S('any two'), lead='The apparatus line:', note='2 × 3.',
            options=items(S('apparatus: bell jar with electric bell, battery, vacuum pump'), 3, psep_first=': ')),
       R('procedure: turn on pump', 3),
       R('observation/conclusion: no sound heard when air removed / sound needs a medium', 3,
         note_sel=S('accept valid alternatives', 'a labelled diagram may merit full marks'))],
      'phys-2-5', 'sound-needs-a-medium',
      SQ(12, 'Describe an experiment to show that sound needs a medium to travel through.'), 12, stem=[SOUND9],
      decision='"4 × 3": the apparatus line is "any two 2 × 3" (a menu of two claims at 3), then the procedure and '
               'observation lines at 3.'),
    T('9iv', 'Q9(iv)', 'B', P(8, 'What is meant by reflection?'),
      [R('waves rebounding /bouncing off a surface', 6, **partial(6, 3))], 'phys-2-3', 'reflection',
      SQ(12, 'What is meant by reflection?'), 6, stem=[REFL9]),
    T('9v', 'Q9(v)', 'B', P(8, 'Describe an experiment to show the interference of sound waves.'),
      [R('apparatus: tuning fork', 3), R('procedure: strike the tuning fork and rotate it close to your ear', 3),
       R('observation/ conclusion: the emitted sound increases and decreases in loudness', 3,
         end='due to interference', note_sel=S('accept valid alternatives'))],
      'phys-2-6', 'interference-of-sound', SQ(12, 'Describe an experiment to show the interference of sound waves.'), 9,
      stem=[REFL9]),
    T('9vi', 'Q9(vi)', 'B', P(8, 'Sound waves do not undergo polarisation. Explain why.'),
      [menu(S('longitudinal // not transverse'), 1, 3)], 'phys-2-7', 'sound-not-polarised',
      SQ(12, 'Sound waves do not undergo polarisation. Explain why.'), 3),
    T('9vii', 'Q9(vii)', 'B', P(8, 'Describe a laboratory experiment to demonstrate the Doppler effect.'),
      [R('apparatus: buzzer/sound source', 3), R('procedure: turn on sound source and rotate using string', 3),
       R('observation/conclusion: frequency /pitch changes (as sound source moves closer/away)', 3)],
      'phys-2-7', 'doppler-effect-experiment',
      SQ(12, 'Describe a laboratory experiment to demonstrate the Doppler effect.'), 9, stem=[AMB9]),
    T('9viii', 'Q9(viii)', 'B', P(8, 'State one use of the Doppler effect.'),
      [menu(None, 1, 5, open_list=True, lead='The list ends "etc." (open; "any one 5"); the scheme prices this "5 or 3":',
            note_sel=S('partial answer e.g. general use such as medicine, radar, sonar'), note='(3).',
            options=items(S('measuring speed / speed gun', 'weather forecasting, etc.'), 6))],
      'phys-2-7', 'use-of-doppler-effect', SQ(12, 'State one use of the Doppler effect.'), 5, stem=[AMB9],
      decision='"any one 5" against a list over two lines ending "etc.": an open menu of one; the list\'s entries '
               'are cut at the scheme\'s own commas ("imaging" and "used to study blood flow" stand on two lines with '
               'no comma between them, so they are one entry).'),
    # ---------------------------------------------------------------- Q10 --
    T('10i', 'Q10(i)', 'B', P(8, 'Where in the atom is the electron found?'),
      [R('(obits) outside the nucleus', 3)], 'phys-4-1', 'where-the-electron-is',
      SQ(13, 'Where in the atom is the electron found?'), 3, stem=[STONEY10],
      decision='The scheme prints "(obits)" (a misprint of orbits): lifted as printed.'),
    T('10ii', 'Q10(ii)', 'B', P(8, 'Compare the mass of an electron to the mass of a proton.'),
      [menu(S('electron has smaller mass // 9.1×10⁻³¹ versus 1.67×10⁻²⁷'), 1, 3)],
      'phys-4-1', 'electron-and-proton-mass',
      SQ(13, 'Compare the mass of an electron to the mass of a proton.'), 3, stem=[STONEY10]),
    T('10iii', 'Q10(iii)', 'B', P(8, 'What is meant by thermionic emission?'),
      [R('release of electrons from the surface of a hot metal', 6, **partial(6, 3))], 'phys-4-1',
      'thermionic-emission', SQ(13, 'What is meant by thermionic emission?'), 6, stem=[THERM10]),
    T('10iv', 'Q10(iv)', 'B', P(8, 'Draw a labelled diagram of a cathode ray tube.'),
      [menu(S('(heated)cathode, anode, high voltage, vacuum, deflection plates'), 4, 3, sep=',',
            note_sel=S('any four'), lead='The scheme prices', note='4 × 3.')],
      'phys-4-1', 'cathode-ray-tube-diagram', SQ(13, 'Draw a labelled diagram of a cathode ray tube.'), 12,
      stem=[THERM10], fig='q10iv-scheme',
      decision='"any four 4 × 3" against five parts printed on one line: a menu of four claims at 3; the scheme '
               'draws the tube (the solution figure).'),
    T('10v', 'Q10(v)', 'B', P(8, 'How are the electrons detected in a cathode ray tube?'),
      [R('flashes of light / scintillations (on fluorescent screen)', 3)], 'phys-4-1', 'detecting-electrons',
      SQ(13, 'How are the electrons detected in a cathode ray tube?'), 3),
    T('10vi', 'Q10(vi)', 'B', P(8, 'State one use of a cathode ray tube.'),
      [anyn(None, 1, 3, open_list=True, note='The scheme ends its list "etc.": the list is open.',
            options=items(S('CRO, old TV monitors, ECG screens, etc.'), 3))],
      'phys-4-1', 'use-of-cathode-ray-tube', SQ(13, 'State one use of a cathode ray tube.'), 3),
    T('10vii', 'Q10(vii)', 'B', P(8, 'Describe an experiment to demonstrate the', 'photoelectric effect.'),
      [R('apparatus: (gold leaf) electroscope', 3), R('UV lamp', 3),
       R('procedure: place a zinc plate on the cap of the electroscope / charge the electroscope', 3,
         end='negatively / shine the UV lamp on the zinc plate'),
       R('observation /conclusion: the leaf collapses /electrons emitted', 3,
         note_sel=S('marks may be obtained from a diagram', 'accept valid alternatives'))],
      'phys-4-2', 'photoelectric-effect-experiment',
      SQ(13, 'Describe an experiment to demonstrate the photoelectric effect.'), 12, stem=[PHOTO10],
      decision='"4 × 3" against the four lines: one row each.'),
    T('10viii', 'Q10(viii)', 'B', P(8, 'What is an X‐ray?'),
      [R('high energy/frequency electromagnetic radiation', 6, **partial(6, 3))], 'phys-4-2', 'what-is-an-x-ray',
      SQ(13, 'What is an X‐ray?'), 6, stem=[XRAY10], fig='q10viii-xray'),
    T('10ix', 'Q10(ix)', 'B', P(8, 'Explain why the production of X‐rays can be considered to be the opposite of the',
                                'photoelectric effect.'),
      [R('fast electrons produce X‐radiation while high frequency radiation produces electrons', 4, **partial(4, 2))],
      'phys-4-2', 'x-rays-opposite-of-photoelectric',
      SQ(13, 'Explain why the production of X‐rays can be considered to be the opposite of the',
         'photoelectric effect.'), 4),
    T('10x', 'Q10(x)', 'B', P(8, 'State one danger associated with X‐rays.'),
      [menu(None, 1, 4, open_list=True, lead='The list ends "etc." (open; "any one 4"); the scheme prices this "4 or 2":',
            note_sel=S('partial answer'), note='(2).',
            options=items(S('can cause skin burns, cancer, ionise cells, death, etc.'), 4))],
      'phys-4-2', 'danger-of-x-rays', SQ(13, 'State one danger associated with X‐rays.'), 4),
    # ---------------------------------------------------------------- Q11 --
    T('11a', 'Q11(a)', 'B', P(9, 'Name two greenhouse gases that are contributing to climate change.'),
      [menu(S('carbon dioxide/CO₂, methane / CH₄, nitrous oxide/N₂O'), 2, 4, sep=',', steps=[4, 3],
            lead='The scheme prices', note_sel=S('any two'), note='7; any one (4).')],
      'phys-2-4', 'greenhouse-gases', SQ(14, 'Name two greenhouse gases that are contributing to climate change.'), 7,
      stem=[GASES11], decision='"any two 7, any one (4)": a menu priced step by step [4, 3].'),
    T('11b', 'Q11(b)', 'B', P(9, 'State one of the impacts of climate change that Ireland has experienced.'),
      [menu(S('flooding, drought, heavy snow'), 1, 7, sep=',', note_sel=S('any one'), lead='The scheme prices',
            note='7.')], 'phys-2-4',
      'impact-of-climate-change',
      SQ(14, 'State one of the impacts of climate change that Ireland has experienced.'), 7, stem=[IMPACT11]),
    T('11c', 'Q11(c)', 'B', P(9, 'An electric car uses a battery to make the car move. What energy conversion takes place',
                              'when this happens?'),
      [menu(S('chemical to kinetic // chemical to electric // electric to kinetic'), 1, 7,
            lead='"any one"; the scheme prices this "7 or 4":', note_sel=S('partial answer'), note='(4).')],
      'phys-1-4', 'energy-conversion-in-electric-car',
      SQ(14, 'An electric car uses a battery to make the car move. What energy conversion takes place',
         'when this happens?'), 7),
    T('11d', 'Q11(d)', 'B', P(9, 'What is renewable power?'),
      [R('power from a source that does not get depleted', 7)], 'phys-1-4', 'renewable-power',
      SQ(14, 'What is renewable power?'), 7, stem=[PLAN11]),
    T('11e', 'Q11(e)', 'B', P(9, 'What is the SI unit of power?'),
      [R('watt', 7)], 'phys-1-4', 'unit-of-power', SQ(14, 'What is the SI unit of power?'), 7),
    T('11f', 'Q11(f)', 'B', P(9, 'The BER rating of a home is dependent on the U‐value of the materials used.',
                              'What is meant by U‐value?'),
      [R('energy passing through a material per m² per K per s', 7, **partial(7, 4))], 'phys-2-1', 'u-value',
      SQ(14, 'The BER rating of a home is dependent on the U‐value of the materials used.',
         'What is meant by U‐value?'), 7, stem=[PLAN11]),
    T('11g', 'Q11(g)', 'B', P(9, 'Wind energy is a significant source of renewable power in Ireland. A wind turbine generates',
                              'Calculate the power of the turbine.'),
      [FR(14, (82, 596, 242, 621), '(P= E/t = (90 ×10⁶)/60 =) 1.5 × 10⁶ W', 7, **partial(7, 4))], 'phys-1-4',
      'power-of-wind-turbine',
      SQ(14, 'Wind energy is a significant source of renewable power in Ireland. A wind turbine',
         'Calculate the power of the turbine.'), 7),
    T('11h', 'Q11(h)', 'B', P(9, 'Other than wind energy, name two other sources of renewable power used in Irish', 'homes.'),
      [menu(S('solar, wave, tidal, hydro, geothermal, biomass'), 2, 4, sep=',', steps=[4, 3],
            lead='The scheme prices', note_sel=S('any two'), note='7; any one (4).')],
      'phys-1-4', 'sources-of-renewable-power',
      SQ(14, 'Other than wind energy, name two other sources of renewable power used in Irish homes.'), 7,
      decision='"any two 7, any one (4)": a menu priced step by step [4, 3].'),
    # ---------------------------------------------------------------- Q12 --
    T('12ai', 'Q12(a)(i)', 'B', Q12AI, [R('30000 m', 6)], 'phys-1-1', 'kilometres-to-metres',
      SQ(15, 'Convert 30 km into metres.'), 6, stem=[BUS12]),
    T('12aii', 'Q12(a)(ii)', 'B', Q12AII, [R('(28 × 60 =) 1680 s', 3)], 'phys-1-1', 'minutes-to-seconds',
      SQ(15, 'Convert 28 minutes into seconds.'), 3, stem=[BUS12]),
    T('12aiii', 'Q12(a)(iii)', 'B', P(10, 'Use your answers to (i) and (ii) to calculate the speed of', 'the bus in m s⁻¹.'),
      [FR(15, (110, 183, 260, 208), '(v= s/t = (30 000)/1680 =) 17.86 m s⁻¹', 6, **partial(6, 3))],
      'phys-1-1', 'speed-of-bus',
      SQ(15, 'Use your answers to (i) and (ii) to calculate the speed of the bus in m s⁻¹.'), 6,
      stem=[BUS12, M('(i)', 10), Q12AI, M('(ii)', 10), Q12AII]),
    T('12aiv', 'Q12(a)(iv)', 'B', P(10, 'Sketch a velocity‐time graph of the bus’s journey.'),
      [C('labelled axes', 3), R('constant speed (horizontal line) for most of the journey', 3),
       R('sharp deceleration to zero shown', 3)],
      'phys-1-1', 'velocity-time-graph-of-bus', SQ(15, 'Sketch a velocity‐time graph of the bus’s journey.'), 9,
      stem=[BUS12, BRAKE12], fig='q12aiv-scheme',
      decision='"3 × 3" against the three lines; the scheme sketches the graph (the solution figure).'),
    T('12av', 'Q12(a)(v)', 'B', P(10, 'What is the difference between speed and velocity?'),
      [R('velocity is the speed in a given direction', 4)], 'phys-1-1', 'speed-and-velocity',
      SQ(15, 'What is the difference between speed and velocity?'), 4,
      decision='The scheme prints the part\'s tariff "4" and the row\'s cell in brackets, "(4)": the full mark.'),
    T('12bi', 'Q12(b)(i)', 'B', P(10, 'What is meant by temperature?'),
      [menu(S('degree of hotness // measure of how hot or cold a body is'), 1, 6,
            lead='The scheme prices this "6 or 3":', note_sel=S('partial answer e.g. the heat in a body'), note='(3).')],
      'phys-2-1', 'temperature', SQ(15, 'What is meant by temperature?'), 6, stem=[THERMO12]),
    T('12bii', 'Q12(b)(ii)', 'B', P(10, 'Body temperature is 37 °C. Convert this to kelvin (K).'),
      [R('(37 + 273 = ) 310 K', 3)], 'phys-2-1', 'celsius-to-kelvin',
      SQ(15, 'Body temperature is 37 °C. Convert this to kelvin (K).'), 3, stem=[THERMO12]),
    T('12biii', 'Q12(b)(iii)', 'B', P(10, 'What is a thermometric property?'),
      [R('one that changes measurably with (changing) temperature', 6, **partial(6, 3))], 'phys-2-1',
      'thermometric-property', SQ(15, 'What is a thermometric property?'), 6, stem=[PROP12]),
    T('12biv', 'Q12(b)(iv)', 'B', P(10, 'Name one example of a thermometric property.'),
      [menu(None, 1, 4, open_list=True, note_sel=S('any one'), lead='The list ends "etc." (open); the scheme prices',
            note='4.', options=items(S('colour, resistance, pressure, volume, emf, voltage, etc.'), 6))],
      'phys-2-1', 'example-of-thermometric-property', SQ(15, 'Name one example of a thermometric property.'), 4,
      stem=[PROP12], decision='"any one 4" against a list ending "etc.": an open menu of one.'),
    T('12bv', 'Q12(b)(v)', 'B', P(10, 'Describe an experiment to calibrate a thermometer.'),
      [R('apparatus: beaker of water, heat source, calibrated and uncalibrated thermometers', 3),
       R('procedure: measure thermometric property at different reference temperatures', 3),
       R('observation/conclusion: draw a scale/ graph', 3)],
      'phys-2-1', 'calibrating-a-thermometer', SQ(15, 'Describe an experiment to calibrate a thermometer.'), 9,
      stem=[UNCAL12]),
    T('12ci', 'Q12(c)(i)', 'B', P(10, 'Name a material that is an electrical conductor.'),
      [R('metal', 3)], 'phys-3-3', 'electrical-conductor', SQ(16, 'Name a material that is an electrical conductor.'),
      3, stem=[CURR12]),
    T('12cii', 'Q12(c)(ii)', 'B', P(10, 'What is the name given to a material that does not allow electric charge to flow',
                                   'through it?'),
      [R('insulator', 3)], 'phys-3-3', 'insulator',
      SQ(16, 'What is the name given to a material that does not allow electric charge to flow', 'through it?'), 3,
      stem=[CURR12]),
    T('12ciii', 'Q12(c)(iii)', 'B', P(10, 'Describe an experiment to show that a material is an electrical conductor.'),
      [R('apparatus: circuit to show power source, ammeter/ bulb, leads, contacts', 3),
       R('procedure: connect the circuit and place item between contacts', 3),
       R('observation/conclusion: bulb lights / item conductor', 3)],
      'phys-3-3', 'showing-a-conductor',
      SQ(16, 'Describe an experiment to show that a material is an electrical conductor.'), 9, stem=[CURR12],
      cells='The [3] printed against "observation/conclusion: bulb lights / item conductor" shares its baseline with '
            'the "12 V" label of the circuit drawn beside it, so the reader gives the cell to the label: the scheme '
            'prints 3 × 3 against these three rows.'),
    T('12civ', 'Q12(c)(iv)', 'B', P(10, 'Calculate the total resistance in the circuit shown above.'),
      [R('(6 + 8 =) 14 Ω', 6)], 'phys-3-3', 'total-resistance',
      SQ(16, 'Calculate the total resistance in the circuit shown above.'), 6, fig='q12c-circuit'),
    T('12cv', 'Q12(c)(v)', 'B', P(10, 'Calculate the current flowing in the circuit.'),
      [FR(16, (110, 308, 215, 331), '(I= V/R = 12/14 =) 0.86 A', 7, **partial(7, 4))], 'phys-3-3',
      'current-in-circuit', SQ(16, 'Calculate the current flowing in the circuit.'), 7, fig='q12c-circuit'),
    T('12di', 'Q12(d)(i)', 'B', P(11, 'Which type of radiation is the most penetrating?'),
      [R('gamma', 3)], 'phys-4-4', 'most-penetrating-radiation',
      SQ(16, 'Which type of radiation is the most penetrating?'), 3, stem=[RAD12]),
    T('12dii', 'Q12(d)(ii)', 'B', P(11, 'Describe an experiment to compare the penetrating power of alpha, beta and gamma',
                                   'radiation.'),
      [menu(None, 2, 3, note_sel=S('any two'), lead='The apparatus line:', note='2 × 3.',
            options=items(S('apparatus: radioactive sources, barriers, detector/GM tube'), 3, psep_first=': ')),
       R('procedure: place different barriers between the sources and the detector', 3),
       menu(None, 1, 3, note='The scheme\'s observation/conclusion line: two conclusions separated by "//".',
            options=[S('observation/conclusion: alpha is stopped first // gamma penetrates best', piece=[2, k],
                       psep=[': ', '//']) for k in (1, 2)])],
      'phys-4-4', 'comparing-penetrating-power',
      SQ(16, 'Describe an experiment to compare the penetrating power of alpha, beta and', 'gamma radiation.'), 12,
      stem=[RAD12],
      decision='"4 × 3": the apparatus line is "any two 2 × 3" (a menu of two claims at 3), the procedure 3, and the '
               'observation printed as two conclusions separated by "//" (a menu of one at 3).'),
    T('12diii', 'Q12(d)(iii)', 'B', P(11, 'Calculate the atomic number, A, of the unknown element X.'),
      [R('84', 3)], 'phys-4-4', 'atomic-number-of-x',
      SQ(16, 'Calculate the atomic number, A, of the unknown element X.'), 3, stem=[EQ12], fig='q12d-equation'),
    T('12div', 'Q12(d)(iv)', 'B', P(11, 'Calculate the mass number, Z.'),
      [R('216', 3)], 'phys-4-4', 'mass-number-of-x', SQ(16, 'Calculate the mass number, Z.'), 3, stem=[EQ12],
      fig='q12d-equation'),
    T('12dv', 'Q12(d)(v)', 'B', P(11, 'Name element X.'),
      [R('Polonium / Po', 3)], 'phys-4-4', 'naming-element-x', SQ(16, 'Name element X.'), 3, stem=[EQ12],
      fig='q12d-equation'),
    T('12dvi', 'Q12(d)(vi)', 'B', P(11, 'State one use of nuclear radiation.'),
      [menu(None, 1, 4, open_list=True, lead='The list ends "etc." (open; "any one"); the scheme prices this "4 or 2":',
            note_sel=S('partial answer'), note='(2).',
            options=items(S('sterilise food, sterilise medical equipment, cancer therapy, energy source, etc. any one'),
                          4))],
      'phys-4-4', 'use-of-nuclear-radiation', SQ(16, 'State one use of nuclear radiation.'), 4),
]

FIGURES = {
    # key suffix: (doc, page, rect in PDF points, credit, letters, alt, solution[, masks])
    'q3-graph': ('paper', 3, (115, 168, 503, 400), SEC, [], 'Graph of 1/length (m⁻¹), 0 to 4.5, against frequency (Hz), 0 to 600: eight points from about 255 Hz to about 510 Hz on a dotted straight line through the origin.', False),
    'q5a-diagram': ('paper', 4, (355, 162, 545, 279), 'britannica.com; halfords.ie; edmundoptics.eu', [], 'A spring balance reading 5 N holds an object in air above a beaker; a second balance reading 3 N holds the object in the water of a full beaker, the spilled water caught in a dish beside it and labelled 2 N of water.', False),
    'q5i-spectrometer': ('paper', 4, (344, 590, 541, 680), 'britannica.com; halfords.ie; edmundoptics.eu', [], 'Photograph of the piece of equipment: two horizontal tubes on arms either side of a round base that carries a small table on top.',
                         False),
    'q6-forces': ('paper', 5, (170, 244, 425, 312), SEC, [], 'An oval object labelled 9 kg with three force arrows: 6 N pointing to the left; 5 N and 3 N pointing to the right.', False),
    'q7iv-question': ('paper', 6, (80, 203, 425, 251), SEC, [], 'The printed lines: "Refractive index can also be calculated using the formula n = 1/sin C", the fraction stacked, then "(iv) What does C stand for in the formula written above?"', False),
    'q7v-question': ('paper', 6, (80, 278, 545, 447), SEC, [], 'The printed ask "(v) Copy and complete the diagram below to show the paths of the rays of light after they strike the converging lens." over its diagram: three parallel horizontal rays arriving from the left at a converging lens.', False),
    'q7vi-question': ('paper', 6, (80, 446, 425, 485), SEC, [], 'The printed lines "A converging lens can be used to produce a magnified virtual image.", the word virtual underlined, and "(vi) Explain the underlined term."', False),
    'q8-electroscope': ('paper', 7, (388, 56, 542, 186), 'physicsmax.com; State Examinations Commission',
                        ['A', 'B', 'C'], 'Diagram of a gold leaf electroscope in a box-shaped case: arrows point to three parts labelled A (at the top), B (where the rod enters the case) and C (near the bottom of the rod), and to parts labelled Metal case, Rod and Plate.', False),
    'q8v-photo': ('paper', 7, (143, 236, 452, 436), 'physicsmax.com; State Examinations Commission', [], 'Photograph of a white plastic rod held over a wooden surface, small pieces of paper stuck to the rod and more pieces lying on the surface below it.', False),
    'q10viii-xray': ('paper', 8, (350, 584, 555, 693), 'orau.org', [], 'Photograph of an X-ray tube: a glass envelope holding metal electrodes, with a lead coming out of one end.', False),
    'q12c-circuit': ('paper', 10, (205, 550, 385, 660), SEC, [], 'Circuit diagram: a 12 V cell in one loop with a 6 Ω resistor and an 8 Ω resistor in series.', False),
    'q12d-equation': ('paper', 11, (250, 165, 365, 190), SEC, [], 'The printed nuclear equation: Rn with 220 raised and 86 lowered after it, an arrow, X with Z raised and A lowered after it, plus alpha with 4 raised and 2 lowered after it.', False),
    'q4iv-scheme-graph': ('scheme', 7, (66, 386, 525, 668), SEC, [], "The marking scheme's graph, Resistance versus Temperature: resistance (Ω) from 0 to 9 against temperature (°C) from 0 to 70, the seven points from 4.8 Ω at 10 °C to 8.4 Ω at 70 °C on a straight line that meets the resistance axis at about 4.2 Ω.", True),
    'q7v-scheme': ('scheme', 10, (300, 436, 460, 533), SEC, [], "The marking scheme's completed diagram: the three parallel rays pass through the converging lens and cross at one point beyond it.", True),
    'q8vi-scheme': ('scheme', 11, (190, 494, 482, 667), SEC, [], "The marking scheme's diagram: a dish of oil drawn as a circle with two electrodes inside, joined to a 5 kV supply (+ on the left, − on the right); dashed red arrows run from the + electrode to the − electrode; labels semolina, castor oil, electrode and dish of oil.", True,
                    [(190, 494, 268, 553), (190, 646, 275, 662)]),
    'q10iv-scheme': ('scheme', 13, (115, 250, 465, 340), SEC, [], "The marking scheme's diagram of a cathode ray tube: a heated cathode and an anode joined to a high voltage (− and +), a dashed beam passing between two deflection plates to a screen at the far end, the inside labelled Vacuum.", True),
    'q12aiv-scheme': ('scheme', 15, (362, 244, 465, 312), SEC, [], "The marking scheme's sketch: velocity v against time t, a horizontal line for most of the journey, then a straight line falling steeply to zero.", True),
}
