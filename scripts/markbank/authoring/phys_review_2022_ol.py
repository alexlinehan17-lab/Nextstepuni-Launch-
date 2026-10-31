"""Physics 2022 Ordinary Level — reviewed task ledger, correcting the sitting in place.

Independent visual sweep (2026-10-28), every page rendered and read:
  * The paper (LC021GLP000EV), 16 pages: p1 cover ("Answer two questions from
    Section A and four questions from Section B"; the 2022 papers were adjusted
    for disruption to learning due to COVID-19), p2-p4 Section A (80 marks)
    Questions 1-5 (any two, 40 marks each), p5-p14 Section B (224 marks)
    Questions 6-14 (any four, 56 marks each), p15 acknowledgements (images on
    pages 5-14), p16 back cover.
  * The marking scheme, 28 pages: p1 cover, p2 note on published schemes, p3
    points to note (solidus, double solidus, slips), p4 annotation symbols, p5
    Irish-language bonus table (Tábla 304), p6-p23 Questions 1-14 (each question
    reprinted in regular type, its answers in bold, the mark cells at the right
    margin), p24-p26 blank (footer only), p27 blank, p28 back cover.

The census reader's marks checksum for this sitting reads "224" against "280"
for 2023-2026: it reads the Section B head, which the 2022 paper prints as
"SECTION B (224 MARKS) Answer four questions from this section. Each question
carries 56 marks." (4 x 56), where 2023-2026 print five questions (280). The
2022 rubric explains it; no ask is lost and the census needed no fix (125
leaves, every one printed).

Every printed ask is carded. The paper prints a group mark after a run of romans
("(12)" closing Q1(i)): GROUP_TOTALS. Q6 is any eight of (a)-(l) at 7 each
(8 x 7): one card per letter. Q14 is any two of (a)-(d): every part is carded.
Q12(iv) and Q14(b)(iii) print (a) and (b) priced apart: one card each. Most rows
carry the scheme's partial allowance ("[accept partial answer for 3]") as their
note. A list of interchangeable items under one sum ("runway / air-track, car /
rider, ticker-tape ... [6 + 3 + 3]", "red, blue, green [4 + 2 + 1]") is a menu
priced step by step (the 2023 Ordinary convention); "e.g. ..." examples are open
menus.

The paper and scheme set Q3's "1/l" (the (viii) ask and the table's third row)
as a raised 1, a slash and a lowered l, and the slash is glyph 3415 of a Cambria
subset whose ToUnicode map gives it U+0D57, a Malayalam vowel sign: the deck
build dropped the old Q3 cards for that character. GLYPHS sets the glyph to "/",
looked at on the rendered pages; the text layer still hands the slash back after
the l ("1 l/"), so no card lifts that fraction as text: Q3(viii)'s ask is shown
as a printed crop (question figure), and Q3(vii)'s values are lifted cell by cell,
each labelled with its length l. The radium nuclide of Q14(d)(iii) and (iv) is
set as stacked numbers after the symbol: those asks are shown as printed crops,
and the scheme's answer nuclide "Po" is read with G('equation').

The sitting was already carded (120 authored cards, 116 shipped). Every task is
re-derived from the PDFs at the scheme's own mark boundaries and every authored
id is kept, mapped (`id=`) to the task it was carding. The asks the bank had
left open (Q3(i), (ii), (vii), (viii), the four the build dropped; Q8(i), (ii);
Q14(b)(i); Q14(c)(i), (ii), (iv)) are carded, and Q12(iv) is split at (a) and (b).
"""
from phys_review_lib import Q, SQ, S, M, G, pt, anyn, T

YEAR, LEVEL = 2022, 'ol'
REVIEWED_AT = '2026-10-28'
BASELINE_COMMIT = '99ec7f0a0d6b243f4d5a1dc9b14a6a958e98095e'

SOURCES = {
    'paper': {'path': 'examiner-reports/physics/papers/2022-ol-paper.pdf', 'fileid': 'LC021GLP000EV.pdf',
              'sha256': '5246af9fbc8607914806b471a78ca0805a19cb3e3b038fce7ae45c4e99c9bbd5', 'pages': 16},
    'scheme': {'path': 'examiner-reports/physics/schemes/2022-ol.pdf', 'fileid': 'LC021GLP000EV.pdf',
               'sha256': '7b0ddda535e9dc2a1be382949bced3daf0abc0c3cce10578880a8724fd46fd8d', 'pages': 28},
}

PAGE_ROLES = {
    'paper': {1: 'cover', **{p: 'questions' for p in range(2, 15)}, 15: 'acknowledgements', 16: 'back-cover'},
    'scheme': {1: 'cover', 2: 'note', 3: 'conventions', 4: 'annotations', 5: 'irish-bonus',
               **{p: 'marking' for p in range(6, 24)}, 24: 'blank', 25: 'blank', 26: 'blank', 27: 'blank',
               28: 'back-cover'},
}

LETTERED = {6, 14}

# Glyph 3415 of the Cambria subsets is the slash of the "1/l" fraction (paper p3 Q3(viii) and table; scheme
# p8 Q3(viii) and both table rows), read on the rendered pages at 400 dpi; its ToUnicode gives U+0D57.
GLYPHS = {'paper': {'Cambria': {3415: '/'}}, 'scheme': {'CambriaMath': {3415: '/'}}}
VERIFIED_LINES = []

QUESTION_TOTALS = {**{n: 40 for n in range(1, 6)}, **{n: 56 for n in range(6, 14)},
                   14: 112}   # any two of (a)-(d), 28 each: all four carded
PART_TOTALS = {(14, x): 28 for x in 'abcd'}
BEST_OF = {6: (8, 7)}
GROUP_TOTALS = {
    (1, ('i',)): 12, (1, ('ii', 'iii', 'iv')): 12, (1, ('v', 'vi', 'vii', 'viii')): 16,
    (2, ('i', 'ii')): 18, (2, ('iii', 'iv', 'v', 'vi', 'vii')): 22,
    (3, ('i', 'ii', 'iii', 'iv')): 15, (3, ('v', 'vi', 'vii', 'viii')): 25,
    (4, ('i', 'ii')): 12, (4, ('iii', 'iv')): 12, (4, ('v', 'vi')): 16,
    (5, ('i', 'ii', 'iii')): 18, (5, ('iv', 'v', 'vi')): 22,
    (7, ('i', 'ii', 'iii', 'iv', 'v')): 30, (7, ('vi', 'vii', 'viii', 'ix')): 26,
    (8, ('i', 'ii', 'iii', 'iv', 'v')): 33, (8, ('vi', 'vii', 'viii')): 23,
    (9, ('i', 'ii', 'iii')): 18, (9, ('iv', 'v')): 18, (9, ('vi', 'vii', 'viii', 'ix')): 20,
    (10, ('i', 'ii')): 18, (10, ('iii', 'iv', 'v')): 21, (10, ('vi', 'vii', 'viii')): 17,
    (11, ('i', 'ii', 'iii', 'iv', 'v')): 27, (11, ('vi', 'vii', 'viii')): 21, (11, ('ix', 'x')): 8,
    (12, ('i', 'ii')): 17, (12, ('iii', 'iv')): 15, (12, ('v', 'vi', 'vii', 'viii')): 24,
    **{(13, (r,)): 7 for r in ('i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii')},
}
CHECKSUMS = {}
ROUTES = {}

SCAN_PAGES = {'paper': range(2, 15)}
SELECTION_SCAN = [
    ('paper', 2, 'either', 'Q1(viii) "to improve the accuracy of either of these experiments": the ask\'s own wording, '
                           'not a choice.'),
    ('paper', 3, 'the following', 'Q3 "The student recorded the following results": a reference to the table.'),
    ('paper', 4, 'the following', 'Q4 "The following results were recorded": a reference to the results.'),
    ('paper', 4, 'both', 'Q5 lead-in "were both kept constant": description.'),
    ('paper', 4, 'the following', 'Q5 "The student recorded the following results": a reference to the table.'),
    ('paper', 5, 'the following', 'Q6 "Answer any eight of the following parts": a best-eight of (a)-(l) at 7 '
                                  'each (8 x 7); every part is carded (BEST_OF).'),
    ('paper', 8, 'or', 'Q9 lead-in "the image produced may be real or virtual": description.'),
    ('paper', 12, 'the following', 'Q13 "Read the following passage": a reference to the passage.'),
    ('paper', 12, 'both', 'Q13 passage "Both types of eclipse": description.'),
    ('paper', 12, 'either', 'Q13 passage "either total or partial": description.'),
    ('paper', 12, 'or', 'Q13 passage, the same sentence.'),
    ('paper', 12, 'or', 'Q13 passage "the Earth or the Moon gets completely in the way": description.'),
    ('paper', 12, 'either', 'Q13 passage "only a part of either the Earth or the Moon": description.'),
    ('paper', 12, 'or', 'Q13 passage, the same phrase.'),
    ('paper', 13, 'any two', 'Q14 "Answer any two of the following parts": whole-part choice; every part is carded.'),
    ('paper', 13, 'the following', 'Q14, the same rubric.'),
]
ASK_SCAN_PAGES = {'paper': range(2, 15)}
ASK_EXEMPT = [
    (8, 'When light is reflected from a concave mirror', 'Q9 lead-in: a description, not an ask; lifted into the stems.'),
    (9, 'When a person sings, their vocal chords vibrate.', 'Q10 lead-in: a description, not an ask; lifted into the '
                                                          'stems.'),
]

SEC = 'State Examinations Commission'
CRIT = 'The scheme prints no answer here, only what earns the marks.'
NOLABEL = S('[–1 if no label present on diagram]')
ORDERED = ('The scheme prints these items under one sum, {cell}, and names no order: a response earns the marks '
           'step by step.')
LINKED = ('{w} reads to the figure-pointer check as a printed figure; the ask is the student\'s own drawing, so the '
          'card links its exam page.')
EXPT = 'A "describe an experiment" part: the scheme prices apparatus, method and observation.'


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


def EG(line, n, end=None, last=None):
    """The n examples of an "e.g. a, b, ... etc." line, cut at its own commas: the first without its "e.g.",
    the last (`last`) without its closing word."""
    base = S(line, end)
    out = [dict(base, piece=[1, 2], psep=[',', 'e.g. '])]
    for k in range(2, n + 1):
        if k == n and last:
            out.append(dict(base, piece=[k, 1], psep=[',', last]))
        else:
            out.append(dict(base, piece=k, psep=','))
    return out


def bundled(parts, keep):
    return f'The old card bundled {parts}, which the scheme prices apart; it keeps its id for {keep}.'


# ------------------------------------------------------------------ stems --
STEM1 = P(2, 'A student carried out an experiment to measure the velocity of an object.')
ACC1 = P(2, 'The student then used the apparatus to measure the acceleration of the object.')
STEM2 = [P(2, 'A student carried out an experiment to verify Snell’s Law', 'a different values of i.')]
TABLE2 = P(2, 'Her results are shown in the table below.')
STEM3 = P(3, 'A student carried out an experiment to investigate how the fundamental frequency f of a',
          'throughout the experiment.')
RESULTS3 = P(3, 'The student recorded the following results.')
STEM4 = [P(4, 'A student carried out an experiment to measure c, the specific heat capacity of water.',
           'He added heat energy to water in a copper calorimeter.')]
RES4 = [P(4, 'The following results were recorded.'), P(4, 'Mass of empty copper calorimeter', '= 1703 J')]
SHC4 = P(4, '(specific heat capacity of copper = 390 J kg⁻¹ K⁻¹)')
STEM5 = [P(4, 'In an experiment to verify Joule’s law, a constant current I was passed through a heating coil',
           'for which the current was flowing were both kept constant.')]
RESULTS5 = P(4, 'The student recorded the following results.')
TRAIN7 = P(6, 'A train of mass 420000 kg started from rest and', 'minutes.')
CRUISE7 = P(6, 'The train then maintained this speed of 25 m s⁻¹ for a further 15 minutes.')
GRAPH8 = P(7, 'The graph shows how the temperature and state of water change as the water is heated up.')
THERMO8 = P(7, 'The temperature of the water needs to be measured throughout this experiment.',
            'It is measured using a thermometer.')
MIRROR9 = P(8, 'When light is reflected from a concave mirror, the image produced may be real or virtual.')
OBJECT9 = P(8, 'The object is 20 cm in front of the concave mirror.')
CONVEX9 = P(8, 'Light is also reflected by convex mirrors.')
SING10 = P(9, 'When a person sings, their vocal chords vibrate.', 'through the air to the listener’s ears.')
WAVES10 = P(9, 'Sound waves can undergo reflection, refraction, diffraction and interference.')
EAR10 = P(9, 'The human ear is most sensitive to sounds with frequencies between 2 kHz and 4 kHz.', 'canal.')
PIPE10 = P(9, 'The ear canal can be thought of as a pipe open at one end.')
FRANKLIN11 = P(10, 'Benjamin Franklin began experimenting with electricity during the', '18th century.')
WIRE11 = P(10, 'A piece of wire of length 1.5 m has a resistance of 12 Ω.')
STONEY12 = P(11, 'The Irish physicist George Stoney is most famous for introducing the', 'term electron.')
PHOTO12 = P(11, 'The photoelectric effect is the release of electrons from the surface', 'falls on it.')
THRESHOLD12 = P(11, 'To ensure the photoelectric effect occurs, the light must be of a suitable frequency to',
                'must be above the threshold frequency.')
ZINC12 = P(11, 'The threshold frequency for zinc is 6.5 × 10¹⁴ Hz.')
XRAY12 = P(11, 'X–ray production is the inverse process of the photoelectric effect.', 'electrons hit a target')
SOLAR13 = P(12, 'Total solar eclipses are the most dramatic of all eclipses.', 'either the Earth or the Moon is in shadow.')
LUNAR13 = P(12, 'Lunar eclipses are far more common than solar eclipses.', 'result in the Moon appearing red.')
STONE14 = P(13, 'A boy picks up a stone of mass 5 g and throws it vertically upwards with an initial',
            'it loses kinetic energy.')
G14 = P(13, '(acceleration due to gravity = 9.8 m s⁻²)')
MIRAGE14 = P(13, 'In order for an observer to see a mirage on a hot day, total', 'hot air.')
EYE14 = P(13, 'To see an object clearly, light from an object must enter the eye through the pupil and', 'retina.')
GLASSES14 = P(13, 'A certain person’s eye has a power of 62 m⁻¹.', 'The lens of their glasses has a power of –2 m⁻¹.')
STICK14 = P(14, 'The diagram shows a metre stick which is suspended from its mid‐point (50 cm) with',
            'The metre stick is in equilibrium.')
BECQ14 = P(14, 'Henri Becquerel was the first person to discover evidence of', 'of the decay of atomic nuclei.')
RADIUM14 = P(14, 'Radium (Ra₈₈', 'is an alpha emitter.')

TASKS = [
    # ============================================================ Section A ==
    # ---------------------------------------------------------------- Q1 --
    T('1i', 'Q1(i)', 'A', P(2, 'Draw a labelled diagram of the apparatus used to measure constant velocity.'),
      [anyn(None, 3, 6, steps=[6, 3, 3], note_sel=NOLABEL, note=ORDERED.format(cell='[6 + 3 + 3]'),
            options=[S('runway / air-track'), S('car / rider'), S('ticker-tape / light-gate / timer')])],
      'phys-u2', 'constant-velocity-apparatus',
      SQ(6, 'Draw a labelled diagram of the apparatus used to measure constant velocity.'), 12, stem=[STEM1],
      id='phys-2022-ol-q1-i'),
    T('1ii', 'Q1(ii)', 'A', P(2, 'Indicate on the diagram what distance the student measured.'),
      [R('length of tape / length of rider or card / distance travelled by car/rider', 3)], 'phys-u2',
      'distance-measured', SQ(6, 'Indicate on the diagram what distance the student measured.'), 3, stem=[STEM1],
      source_pages=[2], id='phys-2022-ol-q1-ii', decision=LINKED.format(w='"the diagram"')),
    T('1iii', 'Q1(iii)', 'A', P(2, 'Describe how the student measured the time.'),
      [R('number of gaps × 0.02 s / from (electronic) timer', 3)], 'phys-u2', 'measuring-the-time',
      SQ(6, 'Describe how the student measured the time.'), 3, stem=[STEM1], id='phys-2022-ol-q1-iii'),
    T('1iv', 'Q1(iv)', 'A', P(2, 'State the formula used to calculate the velocity.'),
      [R('s ÷ t', 6, note_sel=PA(3))], 'phys-1-1', 'velocity-formula',
      SQ(6, 'State the formula used to calculate the velocity.'), 6, stem=[STEM1], id='phys-2022-ol-q1-iv'),
    T('1v', 'Q1(v)', 'A', P(2, 'What changes did the student make to the apparatus?'),
      [R('changed slope / applied force / second light-gate', 4)], 'phys-u2', 'changes-for-acceleration',
      SQ(6, 'What changes did the student make to the apparatus?'), 4, stem=[STEM1, ACC1], id='phys-2022-ol-q1-v'),
    T('1vi', 'Q1(vi)', 'A', P(2, 'What measurements did the student take to calculate acceleration?'),
      [R('two distances/times/velocities / distance or time between measurements', 4)], 'phys-u2',
      'measurements-for-acceleration', SQ(6, 'What measurements did the student take to calculate acceleration?'), 4,
      stem=[STEM1, ACC1], id='phys-2022-ol-q1-vi'),
    T('1vii', 'Q1(vii)', 'A', P(2, 'How did the student use these measurements to calculate acceleration?'),
      [R('(v – u) ÷ t or (v² – u²) ÷ 2s', 4, note_sel=PA(2))], 'phys-1-1', 'calculating-acceleration',
      SQ(6, 'How did the student use these measurements to calculate acceleration?'), 4, stem=[STEM1, ACC1],
      id='phys-2022-ol-q1-vii'),
    T('1viii', 'Q1(viii)', 'A', P(2, 'State two precautions that could be taken to improve the accuracy of either of these',
                                 'experiments.'),
      [anyn(None, 2, 3, steps=[3, 1], open_list=True, note=ORDERED.format(cell='[3 + 1]'),
            options=EG('e.g. polish, oil, remove dirt', 7, end='avoid error of parallax etc.', last=' etc.'))],
      'phys-u2', 'precautions-for-accuracy',
      SQ(6, 'State two precautions that could be taken to improve the accuracy of either of these', 'experiments.'), 4,
      stem=[STEM1, ACC1], id='phys-2022-ol-q1-viii',
      decision='The scheme prints examples ("e.g. ... etc.") for two precautions at [3 + 1]: an open menu of two, '
               'priced step by step.'),
    # ---------------------------------------------------------------- Q2 --
    T('2i', 'Q2(i)', 'A', P(2, 'Draw a labelled diagram of the apparatus used in this experiment.'),
      [anyn(None, 3, 6, steps=[6, 3, 3], note_sel=NOLABEL, note=ORDERED.format(cell='[6 + 3 + 3]'),
            options=[S('transparent block'), S('ray-box / laser / pins'),
                     S('detail e.g. paper, ruler, pencil, protractor, etc.')])],
      'phys-u2', 'snells-law-apparatus', SQ(7, 'Draw a labelled diagram of the apparatus used in this experiment.'), 12,
      stem=STEM2, id='phys-2022-ol-q2-i'),
    T('2ii', 'Q2(ii)', 'A', P(2, 'On your diagram, label the angles measured by the student.'),
      [C('both angles labelled', 6, note_sel=PA(3))], 'phys-u2', 'labelling-the-angles',
      SQ(7, 'On your diagram, label the angles measured by the student.'), 6, stem=STEM2, id='phys-2022-ol-q2-ii'),
    T('2iii', 'Q2(iii)', 'A', P(2, 'Name the instrument used to measure these angles.'),
      [R('protractor', 3)], 'phys-u2', 'instrument-for-angles', SQ(7, 'Name the instrument used to measure these angles.'),
      3, stem=STEM2, id='phys-2022-ol-q2-iii'),
    T('2iv', 'Q2(iv)', 'A', P(2, 'State the formula used to calculate n.'),
      [R('sin i ÷ sin r', 4, note_sel=PA(2))], 'phys-2-3', 'refractive-index-formula',
      SQ(7, 'State the formula used to calculate n.'), 4, stem=STEM2, id='phys-2022-ol-q2-iv'),
    T('2v', 'Q2(v)', 'A', P(2, 'Use all of the results in the table to calculate an average value for n.'),
      [pt(S('one calculation of n', '// graph of sin i against sin r', piece=1, psep='//'), 3, kind='criterion',
          note=CRIT, route='side-a'),
       pt(S('average calculated', '// slope calculated', piece=1, psep='//'), 3, kind='criterion', note=CRIT,
          route='side-a'),
       pt(S('one calculation of n', '// graph of sin i against sin r', piece=2, psep='//'), 3, kind='criterion',
          note=CRIT, route='side-b'),
       pt(S('average calculated', '// slope calculated', piece=2, psep='//'), 3, kind='criterion', note=CRIT,
          route='side-b')],
      'phys-2-3', 'average-refractive-index',
      SQ(7, 'Use all of the results in the table to calculate an average value for n.'), 6, stem=STEM2 + [TABLE2],
      fig='q2-table', id='phys-2022-ol-q2-v',
      decision='The scheme prints two methods side by side, separated by "//" (calculations, or a graph): routes '
               'inside the card, each [3] [3].'),
    T('2vi', 'Q2(vi)', 'A', P(2, 'Do your calculations verify Snell’s law? Explain your answer.'),
      [R('yes [or answer consistent with calculations]', 3),
       R('explanation, e.g. calculations all close to average, straight line through origin', 3)], 'phys-2-3',
      'verifying-snells-law', SQ(7, 'Do your calculations verify Snell’s law? Explain your answer.'), 6, stem=STEM2,
      id='phys-2022-ol-q2-vi'),
    T('2vii', 'Q2(vii)', 'A', P(2, 'State one precaution used to improve the accuracy of the experiment.'),
      [anyn(None, 1, 3, open_list=True, options=EG('e.g. thinner pencil, avoid error of parallax, etc.', 2))],
      'phys-u2', 'snells-law-precaution', SQ(7, 'State one precaution used to improve the accuracy of the experiment.'),
      3, stem=STEM2, id='phys-2022-ol-q2-vii',
      decision='The scheme prints two examples ("e.g. ... etc.") for one precaution at [3]: an open menu of one.'),
    # ---------------------------------------------------------------- Q3 --
    T('3i', 'Q3(i)', 'A', P(3, 'Draw a labelled diagram of the apparatus used in this experiment.'),
      [R('sonometer / stretched string', 3),
       R('detail, e.g. metre stick, tuning fork, bridge, paper rider, etc.', 3, note_sel=NOLABEL)], 'phys-u2',
      'sonometer-apparatus', SQ(8, 'Draw a labelled diagram of the apparatus used in this experiment.'), 6,
      stem=[STEM3], id='phys-2022-ol-q3-i',
      decision='The bank\'s card was never shipped: the deck build dropped it for the broken "1/l" glyph (U+0D57) in '
               'the table its stem carried. The stem is now the lead-in alone.'),
    T('3ii', 'Q3(ii)', 'A', P(3, 'Indicate on your diagram the length of string the student measured.'),
      [R('length between two bridges / any valid length', 3)], 'phys-u2', 'length-of-string-measured',
      SQ(8, 'Indicate on your diagram the length of string the student measured.'), 3, stem=[STEM3],
      id='phys-2022-ol-q3-ii',
      decision='The bank\'s card was never shipped (the broken "1/l" glyph in its stem); the stem is the lead-in alone.'),
    T('3iii', 'Q3(iii)', 'A', P(3, 'Name the instrument used to measure length.'),
      [R('sonometer / metre stick', 3)], 'phys-u2', 'instrument-for-length',
      SQ(8, 'Name the instrument used to measure length.'), 3, stem=[STEM3], id='phys-2022-ol-q3-iii'),
    T('3iv', 'Q3(iv)', 'A', P(3, 'Explain why the tension of the string must be kept constant.'),
      [R('frequency depends on tension [state or imply]', 3)], 'phys-2-6', 'constant-tension',
      SQ(8, 'Explain why the tension of the string must be kept constant.'), 3, stem=[STEM3], id='phys-2022-ol-q3-iv'),
    T('3v', 'Q3(v)', 'A', P(3, 'How did the student find the frequency values?'),
      [R('from tuning forks / from signal generator', 3)], 'phys-u2', 'finding-frequency-values',
      SQ(8, 'How did the student find the frequency values?'), 3, stem=[STEM3, RESULTS3], id='phys-2022-ol-q3-v'),
    T('3vi', 'Q3(vi)', 'A', P(3, 'Describe how the student knew that resonance had occurred.'),
      [R('paper rider jumps / loud sound', 4, note_sel=PA(2))], 'phys-2-6', 'recognising-resonance',
      SQ(8, 'Describe how the student knew that resonance had occurred.'), 4, stem=[STEM3], id='phys-2022-ol-q3-vi'),
    T('3vii', 'Q3(vii)', 'A', P(3, 'In your answerbook, copy and complete the table above.'),
      [pt(S(v), 1, label=S(l, after='l (cm)'),
          **({'note': 'The scheme prints the six values of 1/l (cm⁻¹) [6 × 1], each under its length l (cm): 1 mark '
                      'each.'} if k == 0 else {}))
       for k, (l, v) in enumerate((('22', '0.045'), ('18', '0.056'), ('17', '0.059'), ('13', '0.077'),
                                   ('12', '0.083'), ('11', '0.091')))],
      'phys-u2', 'values-of-one-over-l', SQ(8, 'In your answerbook, copy and complete the table above.'), 6,
      stem=[STEM3, RESULTS3], fig='q3-table', id='phys-2022-ol-q3-vii',
      decision='The bank\'s card was never shipped: its rows carried the broken "1/l" glyph. The scheme prints the six '
               'values as a table row headed "1/l (cm⁻¹)": one row per value, labelled with the length l printed '
               'above it in the scheme\'s reprint of the table; the paper\'s table is the figure.'),
    T('3viii', 'Q3(viii)', 'A', P(3, 'Use the data to plot a graph of f against 1 l/.', piece=1, psep=' 1 l/'),
      [C('labelled axis', 3), C('points plotted', 6, units=[1] * 6,
                                note=CRIT + ' It prices them [6 × 1]: 1 mark per point.'),
       C('line of best fit', 3)], 'phys-u2', 'graph-of-f-against-one-over-l',
      SQ(8, 'Use the data to plot a graph of f against'), 12, qfig='q3viii-question', id='phys-2022-ol-q3-viii',
      decision='The bank\'s card was never shipped: its question carried the broken "1/l" glyph (U+0D57). The ask ends '
               'in that fraction, which the text layer reads out of order even with the glyph set right ("1 l/"): '
               'the question text is the ask up to the fraction, and the question is shown as printed, Q3 with its '
               'table. "points plotted [6 × 1]": one row of six 1-mark units.'),
    # ---------------------------------------------------------------- Q4 --
    T('4i', 'Q4(i)', 'A', P(4, 'Draw a labelled diagram of the apparatus used in this experiment.'),
      [anyn(None, 3, 3, open_list=True, note_sel=NOLABEL, note='The scheme prints "[any 3 × 3]".',
            options=[S('calorimeter, water, appropriate source of heat, thermometer, mass balance,', piece=k, psep=',')
                     for k in range(1, 6)]
            + [S('joulemeter, detail e.g. lagging, lid, stirrer etc.', piece=1, psep=','),
               S('joulemeter, detail e.g. lagging, lid, stirrer etc.', piece=2, psep='joulemeter, ')])],
      'phys-u2', 'specific-heat-capacity-apparatus',
      SQ(9, 'Draw a labelled diagram of the apparatus used in this experiment.'), 9, stem=STEM4, id='phys-2022-ol-q4-i',
      decision='Seven items, the last a "detail" with its examples, priced "[any 3 × 3]": a menu of three claims at 3.'),
    T('4ii', 'Q4(ii)', 'A', P(4, 'How did the student supply the heat energy?'),
      [R('joulemeter / hot copper / heating element [state or imply]', 3)], 'phys-u2', 'supplying-heat-energy',
      SQ(9, 'How did the student supply the heat energy?'), 3, stem=STEM4, id='phys-2022-ol-q4-ii'),
    T('4iii', 'Q4(iii)', 'A', P(4, 'Calculate the mass of the water.'),
      [R('0.1498 – 0.0745 = 0.0753 kg', 6, note_sel=PA(3))], 'phys-2-1', 'mass-of-water',
      SQ(9, 'Calculate the mass of the water.'), 6, stem=STEM4 + RES4, id='phys-2022-ol-q4-iii'),
    T('4iv', 'Q4(iv)', 'A', P(4, 'Calculate the increase in temperature of the calorimeter and cold water.'),
      [R('23 – 18 = 5 °C', 6, note_sel=PA(3))], 'phys-2-1', 'increase-in-temperature',
      SQ(9, 'Calculate the increase in temperature of the calorimeter and cold water.'), 6, stem=STEM4 + RES4,
      id='phys-2022-ol-q4-iv'),
    T('4v', 'Q4(v)', 'A', P(4, 'State the formula used to calculate the heat gained by a material as it changes',
                           'temperature.'),
      [R('mcΔθ', 4, note_sel=S('[accept partial answer for 2, e.g. CΔθ]'))], 'phys-2-1', 'heat-gained-formula',
      SQ(9, 'State the formula used to calculate the heat gained by a material as it changes', 'temperature.'), 4,
      stem=STEM4, id='phys-2022-ol-q4-v'),
    T('4vi', 'Q4(vi)', 'A', [P(4, 'Use your answers for (iii), (iv) and (v) to calculate c, the specific heat capacity of water.'),
                             P(4, 'Note: Heat energy added = Heat energy gained by water + calorimeter.')],
      [R('1703 = (0.0745 × 390 × 5) + (0.0753 × c × 5)', 10, units=[6, 2, 2],
         note='The scheme prices this line [6 + 2 + 2] and prints no split of it.'),
       R('c = 4137.4 [J kg⁻¹ K⁻¹]', 2)], 'phys-2-1', 'specific-heat-capacity-of-water',
      SQ(9, 'Use your answers for (iii), (iv) and (v) to calculate c, the specific heat capacity of water.'), 12,
      stem=STEM4 + RES4 + [SHC4], id='phys-2022-ol-q4-vi',
      decision='"[6 + 2 + 2]" is printed against the one equation line: one row at 10, its units as printed.'),
    # ---------------------------------------------------------------- Q5 --
    T('5i', 'Q5(i)', 'A', P(4, 'Draw a labelled diagram of the apparatus used in this experiment.', nth=2),
      [anyn(None, 3, 3, open_list=True, note_sel=NOLABEL, note='The scheme prints "[any 3 × 3]".',
            options=[S('container, water, heating coil, ammeter/multimeter, thermometer,', piece=k, psep=',')
                     for k in range(1, 6)]
            + [S('detail e.g. mass balance, stopwatch, lagging, lid, stirrer etc.')])],
      'phys-u2', 'joules-law-apparatus', SQ(10, 'Draw a labelled diagram of the apparatus used in this experiment.'),
      9, stem=STEM5, id='phys-2022-ol-q5-i',
      decision='Six items, the last a "detail" with its examples, priced "[any 3 × 3]": a menu of three claims at 3.'),
    T('5ii', 'Q5(ii)', 'A', P(4, 'Why were the mass and the time kept constant?'),
      [R('Δθ depends on mass and/or time [state or imply]', 3)], 'phys-3-3', 'mass-and-time-constant',
      SQ(10, 'Why were the mass and the time kept constant?'), 3, stem=STEM5, id='phys-2022-ol-q5-ii'),
    T('5iii', 'Q5(iii)', 'A', P(4, 'In your answerbook, copy and complete the table above.'),
      [G('tokens', page=10, clip=clip, expect=v, marks=1, label=S(i, after='I (A)'),
         **({'note': 'The scheme prints the six values of I² (A²) [6 × 1], each under its current I (A): 1 mark '
                     'each.'} if k == 0 else {}))
       for k, (i, v, clip) in enumerate((('1', '1', (170, 346, 200, 370)), ('1.5', '2.25', (225, 346, 275, 370)),
                                         ('2', '4', (295, 346, 330, 370)), ('2.5', '6.25', (355, 346, 400, 370)),
                                         ('3', '9', (425, 346, 460, 370)), ('3.5', '12.25', (485, 346, 530, 370))))],
      'phys-u2', 'values-of-i-squared', SQ(10, 'In your answerbook, copy and complete the table above.'), 6,
      stem=STEM5 + [RESULTS5], fig='q5-table', id='phys-2022-ol-q5-iii',
      decision='The scheme prints the six values of I² as a table row: one row per value, read from its cell, '
               'labelled with the current printed above it in the scheme\'s reprint of the table.'),
    T('5iv', 'Q5(iv)', 'A', P(4, 'Use all of the data to plot a graph of I² against Δθ.'),
      [C('labelled axis', 3), C('points plotted', 6, units=[1] * 6,
                                note=CRIT + ' It prices them [6 × 1]: 1 mark per point.'),
       C('line of best fit', 3)], 'phys-u2', 'joules-law-graph',
      SQ(10, 'Use all of the data to plot a graph of I² against Δθ.'), 12, stem=STEM5 + [RESULTS5], fig='q5-table',
      id='phys-2022-ol-q5-iv'),
    T('5v', 'Q5(v)', 'A', P(4, 'Use your graph to find the current that caused a change in temperature of 6 °C.'),
      [R('reading for I² [≈ 5]', 3), R('I ≈ 2.2 A', 3, note_sel=S('[accept partial answer for 3, e.g graph not used]'))],
      'phys-u2', 'current-from-graph',
      SQ(10, 'Use your graph to find the current that caused a change in temperature of 6 °C.'), 6, stem=STEM5,
      id='phys-2022-ol-q5-v'),
    T('5vi', 'Q5(vi)', 'A', P(4, 'Explain how your graph verifies Joule’s law.'),
      [R('I² proportional to Δθ', 4, note_sel=PA(2))], 'phys-3-3', 'graph-verifies-joules-law',
      SQ(10, 'Explain how your graph verifies Joule’s law.'), 4, stem=STEM5, id='phys-2022-ol-q5-vi'),
    # ============================================================ Section B ==
    # ---------------------------------------------------------------- Q6 --
    T('6a', 'Q6(a)', 'B', P(5, 'State Newton’s first law of motion.'),
      [R('a body remains at rest [or moving at constant velocity] unless an [unbalanced,', 7,
         end='external] force acts on it',
         note_sel=S('[accept partial answer for 4, e.g Newton’s second law of motion]'))], 'phys-1-2',
      'newtons-first-law', SQ(11, 'State Newton’s first law of motion.'), 7, id='phys-2022-ol-q6-a'),
    T('6b', 'Q6(b)', 'B', P(5, 'A boy applies a force of 20 N to pull his sleigh for 150 m.', 'by the boy.'),
      [R('20 × 150 = 3000 J', 7, note_sel=PA(4))], 'phys-1-4', 'work-done-pulling-sleigh',
      SQ(11, 'A boy applies a force of 20 N to pull his sleigh for 150 m.', 'the boy.'), 7, id='phys-2022-ol-q6-b'),
    T('6c', 'Q6(c)', 'B', P(5, 'What is the difference between heat and temperature?'),
      [R('heat is a form of energy / temperature is a measure of hotness [state or imply]', 7, note_sel=PA(4))],
      'phys-2-1', 'heat-and-temperature', SQ(11, 'What is the difference between heat and temperature?'), 7,
      id='phys-2022-ol-q6-c'),
    T('6d', 'Q6(d)', 'B', P(5, 'Draw a labelled diagram to show how light travels through an optical fibre.'),
      [C('total internal refraction shown', 7,
         note_sel=S('[–1 if no label present on diagram]', '[accept partial answer for 4]'))], 'phys-2-3',
      'light-in-optical-fibre',
      SQ(11, 'Draw a labelled diagram to show how light travels through an optical fibre.'), 7,
      id='phys-2022-ol-q6-d',
      decision='The scheme prints "total internal refraction shown" (as printed; the phenomenon is total internal '
               'reflection): one criterion row in its words.'),
    T('6e', 'Q6(e)', 'B', P(5, 'Describe how to charge an electroscope.'),
      [R('touch with charged object / bring charged object close and earth electroscope', 7, note_sel=PA(4))],
      'phys-3-1', 'charging-an-electroscope', SQ(11, 'Describe how to charge an electroscope.'), 7,
      id='phys-2022-ol-q6-e'),
    T('6f', 'Q6(f)', 'B', P(5, 'Two resistors of resistance 4 Ω and 7 Ω are connected in series.',
                           'Calculate the combined resistance of the two resistors.'),
      [R('4 + 7 = 11 Ω', 7, note_sel=PA(4))], 'phys-3-3', 'resistors-in-series',
      SQ(11, 'Two resistors of resistance 4 Ω and 7 Ω are connected in series.',
         'Calculate the combined resistance of the two resistors.'), 7, id='phys-2022-ol-q6-f'),
    T('6g', 'Q6(g)', 'B', P(5, 'When the frequency of a sound wave increases, its pitch also increases.',
                           'observed to happen to a sound when its amplitude increases?'),
      [R('it gets louder', 7, note_sel=PA(4))], 'phys-2-5', 'amplitude-and-loudness',
      SQ(12, 'When the frequency of a sound wave increases, its pitch also increases.',
         'observed to happen to a sound when its amplitude increases?'), 7, id='phys-2022-ol-q6-g'),
    T('6h', 'Q6(h)', 'B', P(5, 'Describe how to show the magnetic field of a bar magnet.'),
      [R('distribute iron filings / move compass', 7, note_sel=PA(4))], 'phys-3-4', 'magnetic-field-of-bar-magnet',
      SQ(12, 'Describe how to show the magnetic field of a bar magnet.'), 7, id='phys-2022-ol-q6-h'),
    T('6i', 'Q6(i)', 'B', P(5, 'Name the three primary colours of light.'),
      [anyn(S('red, blue, green'), 3, 4, steps=[4, 2, 1], sep=',', note=ORDERED.format(cell='[4 + 2 + 1]'))],
      'phys-2-4', 'primary-colours', SQ(12, 'Name the three primary colours of light.'), 7, id='phys-2022-ol-q6-i',
      decision='The three colours share one cell [4 + 2 + 1]: a menu priced step by step.'),
    T('6j', 'Q6(j)', 'B', P(5, 'What is meant by nuclear fission?'),
      [R('splitting a nucleus [by a neutron, releasing energy]', 7, note_sel=PA(4))], 'phys-4-6', 'nuclear-fission',
      SQ(12, 'What is meant by nuclear fission?'), 7, id='phys-2022-ol-q6-j'),
    T('6k', 'Q6(k)', 'B', P(5, 'A fuse is a safety device used in an electrical plug. Describe how a fuse works.'),
      [R('melts/breaks when current is too high', 7, note_sel=PA(4))], 'phys-3-3', 'how-a-fuse-works',
      SQ(12, 'A fuse is a safety device used in an electrical plug. Describe how a fuse works.'), 7,
      id='phys-2022-ol-q6-k'),
    T('6l', 'Q6(l)', 'B', P(5, 'Explain what is meant by the half‐life of a radioactive sample.'),
      [R('the time for half the sample to decay / the time for its activity to halve', 7, note_sel=PA(4))],
      'phys-4-4', 'half-life', SQ(12, 'Explain what is meant by the half-life of a radioactive sample.'), 7,
      id='phys-2022-ol-q6-l'),
    # ---------------------------------------------------------------- Q7 --
    T('7i', 'Q7(i)', 'B', P(6, 'What is meant by velocity?'),
      [R('rate of change of displacement / speed in a given direction / s ÷ t', 6,
         note_sel=S('[–1 if “distance” used instead of “displacement”]', '[accept partial answer for 3]'))],
      'phys-1-1', 'velocity', SQ(13, 'What is meant by velocity?'), 6, stem=[TRAIN7], id='phys-2022-ol-q7-i'),
    T('7ii', 'Q7(ii)', 'B', P(6, 'Convert 6 minutes into seconds.'),
      [R('6 × 60 = 360 s', 6, note_sel=S('[accept partial answer for 3, e.g. reference to 60 s in a minute]'))],
      'phys-1-1', 'minutes-to-seconds', SQ(13, 'Convert 6 minutes into seconds.'), 6, stem=[TRAIN7],
      id='phys-2022-ol-q7-ii'),
    T('7iii', 'Q7(iii)', 'B', P(6, 'Calculate the acceleration of the train.', 'Include units in your answer.'),
      [R('25 ÷ 360 = 0.069', 4, note_sel=S('[accept partial answer for 2, e.g. a = (v-u)/t]')), R('m s⁻²', 2)],
      'phys-1-1', 'acceleration-of-train',
      SQ(13, 'Calculate the acceleration of the train. Include units in your answer.'), 6, stem=[TRAIN7],
      id='phys-2022-ol-q7-iii'),
    T('7iv', 'Q7(iv)', 'B', P(6, 'Calculate the force required to accelerate the train.'),
      [R('420000 × 0.069 = 29166.7 N', 6, note_sel=S('[accept partial answer for 3, e.g. F = ma]'))], 'phys-1-2',
      'force-on-train', SQ(13, 'Calculate the force required to accelerate the train.'), 6, stem=[TRAIN7],
      id='phys-2022-ol-q7-iv'),
    T('7v', 'Q7(v)', 'B', P(6, 'Calculate the distance the train travelled in 6 minutes.'),
      [R('4500 m', 6, note_sel=S('[accept partial answer for 3, e.g. s = ut + ½at²]'))], 'phys-1-1',
      'distance-while-accelerating', SQ(13, 'Calculate the distance the train travelled in 6 minutes.'), 6,
      stem=[TRAIN7], id='phys-2022-ol-q7-v'),
    T('7vi', 'Q7(vi)', 'B', P(6, 'Calculate the distance the train travelled during this 15 minute interval.'),
      [R('25 × 15 × 60 = 22500 m', 6, note_sel=S('[accept partial answer for 3, e.g. formula for distance]'))],
      'phys-1-1', 'distance-at-constant-speed',
      SQ(13, 'Calculate the distance the train travelled during this 15 minute interval.'), 6,
      stem=[TRAIN7, CRUISE7], id='phys-2022-ol-q7-vi'),
    T('7vii', 'Q7(vii)', 'B', P(6, 'Draw a labelled diagram to show the forces acting on the train while it is moving with',
                               'constant speed.'),
      [C('four correct forces', 9, note_sel=S('[–1 for each omitted force]'))], 'phys-1-2', 'forces-on-train',
      SQ(13, 'Draw a labelled diagram to show the forces acting on', 'the train while it is moving with constant speed.'),
      9, stem=[TRAIN7, CRUISE7], fig='q7vii-scheme', id='phys-2022-ol-q7-vii',
      decision='The scheme prices "four correct forces" [9] and draws them beside it (the solution figure).'),
    T('7viii', 'Q7(viii)', 'B', P(6, 'An object may have a constant speed but not a constant velocity. Explain why.'),
      [R('it is changing direction', 3)], 'phys-1-1', 'constant-speed-not-velocity',
      SQ(13, 'An object may have a constant speed but not a constant', 'velocity. Explain why.'), 3,
      id='phys-2022-ol-q7-viii'),
    T('7ix', 'Q7(ix)', 'B', P(6, 'Draw a speed‐time graph for the train during the first 21 minutes of its journey.'),
      [C('labelled axis', 2), C('correct shape', 6, note_sel=S('[for shape, accept partial answer for 3]'))],
      'phys-1-1', 'speed-time-graph',
      SQ(13, 'Draw a speed-time graph for the train during the first 21 minutes of its journey.'), 8,
      stem=[TRAIN7, CRUISE7], fig='q7ix-scheme', id='phys-2022-ol-q7-ix',
      decision='The scheme names the graph\'s features as criteria and draws the sketch beside them (the solution '
               'figure).'),
    # ---------------------------------------------------------------- Q8 --
    T('8i', 'Q8(i)', 'B', P(7, 'Explain the shape of the graph at part X.'),
      [R('increase in temperature', 6, end='/ no change of state', note_sel=PA(3))], 'phys-2-1', 'shape-at-x',
      SQ(14, 'Explain the shape of the graph at', 'part X.'), 6, stem=[GRAPH8], fig='q8-graph',
      decision='The bank had left this part open. The scheme prints its answer over two lines in a narrow column '
               'beside the graph, "increase in temperature / no change of state", and its [6] there in the text, '
               'not in the margin: one row.'),
    T('8ii', 'Q8(ii)', 'B', P(7, 'Explain the shape of the graph at part Y.'),
      [R('change of state / evaporation / no change in temperature', 6, note_sel=PA(3))], 'phys-2-1', 'shape-at-y',
      SQ(14, 'Explain the shape of the graph at', 'part Y.', nth=2), 6, stem=[GRAPH8], fig='q8-graph',
      decision='The bank had left this part open.'),
    T('8iii', 'Q8(iii)', 'B', P(7, 'Describe how the energy could have been supplied to the water.'),
      [anyn(None, 1, 6, open_list=True,
            options=EG('e.g. joulemeter, element, coil, electricity, hot plate etc.', 5, last=' etc.')),
       R('detail, e.g. in the water, under the container of water as appropriate', 3, note_sel=PA(3))], 'phys-2-1',
      'supplying-energy-to-water', SQ(14, 'Describe how the energy could have been supplied to the water.'), 9,
      stem=[GRAPH8], fig='q8-graph', id='phys-2022-ol-q8-iii',
      decision='"[6 + 3]" against the two lines: the source of energy (examples, "e.g. ... etc.": an open menu of '
               'one) 6, then its detail 3, in the order printed.'),
    T('8iv', 'Q8(iv)', 'B', P(7, 'Ice has a latent heat of 330000 J kg⁻¹.', 'change 0.2 kg of ice to water.'),
      [R('330000 × 0.2 = 66000 J', 6, note_sel=PA(3))], 'phys-2-1', 'latent-heat-of-ice',
      SQ(14, 'Ice has a latent heat of 330000 J kg⁻¹.', 'change 0.2 kg of ice to water.'), 6,
      id='phys-2022-ol-q8-iv'),
    T('8v', 'Q8(v)', 'B', P(7, 'Explain why a steam burn is more dangerous than a burn from boiling water.'),
      [R('steam has more energy / steam may have higher temperature', 6, note_sel=PA(3))], 'phys-2-1', 'steam-burns',
      SQ(14, 'Explain why a steam burn is more dangerous than a burn from boiling water.'), 6,
      id='phys-2022-ol-q8-v'),
    T('8vi', 'Q8(vi)', 'B', P(7, 'A thermometer uses a particular thermometric property to measure temperature.',
                             'What is meant by a thermometric property?'),
      [R('one that changes [measurably] with heat/temperature', 5, note_sel=PA(3))], 'phys-2-1',
      'thermometric-property',
      SQ(14, 'A thermometer uses a particular thermometric property to measure temperature.',
         'What is meant by a thermometric property?'), 5, stem=[THERMO8], id='phys-2022-ol-q8-vi'),
    T('8vii', 'Q8(vii)', 'B', P(7, 'State two examples of thermometric properties.'),
      [anyn(None, 2, 4, steps=[4, 2], open_list=True, note=ORDERED.format(cell='[4 + 2]'),
            options=[S('e.g volume, emf, pressure, height, resistance etc.', piece=[1, 2], psep=[',', 'e.g '])]
            + [S('e.g volume, emf, pressure, height, resistance etc.', piece=k, psep=',') for k in (2, 3, 4)]
            + [S('e.g volume, emf, pressure, height, resistance etc.', piece=[5, 1], psep=[',', ' etc.'])])],
      'phys-2-1', 'examples-of-thermometric-properties', SQ(14, 'State two examples of thermometric properties.'), 6,
      stem=[THERMO8], id='phys-2022-ol-q8-vii',
      decision='The scheme prints examples ("e.g ... etc.") for two properties at [4 + 2]: an open menu of two, '
               'priced step by step.'),
    T('8viii', 'Q8(viii)', 'B', P(7, 'Describe, with the aid of labelled diagram, a laboratory experiment to calibrate a',
                                 'thermometer.'),
      [R('calibrated thermometer', 3), R('uncalibrated thermometer', 3), R('source of heat', 3),
       C('method', 3, note_sel=NOLABEL)], 'phys-2-1', 'calibrating-a-thermometer',
      SQ(14, 'Describe, with the aid of labelled diagram, a laboratory experiment to calibrate a', 'thermometer.'), 12,
      stem=[THERMO8], id='phys-2022-ol-q8-viii', decision=EXPT + ' "method" names what earns its marks only.'),
    # ---------------------------------------------------------------- Q9 --
    T('9i', 'Q9(i)', 'B', P(8, 'What is meant by reflection?'),
      [R('rebounding of a wave off a surface', 3)], 'phys-2-3', 'reflection', SQ(15, 'What is meant by reflection?'),
      3, id='phys-2022-ol-q9-i'),
    T('9ii', 'Q9(ii)', 'B', P(8, 'In your answerbook, copy and complete the ray diagram below to show how a',
                             'magnified image is formed in a concave mirror.'),
      [C('first reflected ray', 5), C('second reflected ray', 2), C('intersection of rays', 2)], 'phys-2-3',
      'concave-mirror-ray-diagram',
      SQ(15, 'In your answerbook, copy and complete the ray diagram below to show how a',
         'magnified image is formed in a concave mirror.'), 9, stem=[MIRROR9], fig='q9-diagram',
      id='phys-2022-ol-q9-ii'),
    T('9iii', 'Q9(iii)', 'B', P(8, 'The image formed is real. Explain what is meant by a real image.'),
      [pt(S('one formed by the intersection of', 'rays / one formed on a screen [6]', piece=1, psep=' [6]'), 6,
          note_sel=PA(3))], 'phys-2-3', 'real-image',
      SQ(15, 'The image formed is real. Explain', 'what is meant by a real image.'), 6, stem=[MIRROR9],
      fig='q9-diagram', id='phys-2022-ol-q9-iii',
      decision='The scheme sets (ii)\'s rows and (iii) in a narrow column beside its copy of the diagram; (iii)\'s [6] '
               'is printed in the answer\'s own line, not in the margin.'),
    T('9iv', 'Q9(iv)', 'B', P(8, 'Calculate the position of the real image formed.'),
      [R('1/u + 1/v = 1/f', 6), C('substitution', 3), R('v = 30 cm', 3, note_sel=PA(3))], 'phys-2-3',
      'position-of-real-image', SQ(15, 'Calculate the position of the real image formed.'), 12,
      stem=[MIRROR9, OBJECT9], fig='q9-diagram', id='phys-2022-ol-q9-iv'),
    T('9v', 'Q9(v)', 'B', P(8, 'The object has a height of 4 cm. Calculate the height of the image.'),
      [R('m = v/u = 1.5', 3), R('image height = 4 × 1.5 = 6 cm', 3, note_sel=PA(3))], 'phys-2-3',
      'height-of-image', SQ(15, 'The object has a height of 4 cm. Calculate the height of the image.'), 6,
      stem=[OBJECT9], fig='q9-diagram', id='phys-2022-ol-q9-v'),
    T('9vi', 'Q9(vi)', 'B', P(8, 'State one use for a concave mirror.'),
      [anyn(None, 1, 4, open_list=True, note_sel=PA(2),
            options=EG('e.g. shaving, dentistry, headlights, searchlights, satellite dishes, etc.', 5))],
      'phys-2-3', 'use-of-concave-mirror', SQ(15, 'State one use for a concave mirror.'), 4,
      id='phys-2022-ol-q9-vi',
      decision='The scheme prints examples ("e.g. ... etc.") for one use at [4]: an open menu of one.'),
    T('9vii', 'Q9(vii)', 'B', P(8, 'Sketch a convex mirror. Indicate which side of the mirror reflects light.'),
      [C('shape', 3), C('side', 3)], 'phys-2-3', 'sketching-a-convex-mirror',
      SQ(15, 'Sketch a convex mirror. Indicate which side of the mirror reflects light.'), 6, stem=[CONVEX9],
      id='phys-2022-ol-q9-vii'),
    T('9viii', 'Q9(viii)', 'B', P(8, 'The image produced in a convex mirror is always virtual.', 'virtual image.'),
      [R('one formed by the apparent intersection of rays / one not formed on a screen', 6, note_sel=PA(3))],
      'phys-2-3', 'virtual-image',
      SQ(15, 'The image produced in a convex mirror is always virtual.', 'virtual image.'), 6, stem=[CONVEX9],
      source_pages=[8], id='phys-2022-ol-q9-viii',
      decision='"The image" (the mirror\'s optical image) reads to the figure-pointer check as a printed figure: the '
               'card links its exam page.'),
    T('9ix', 'Q9(ix)', 'B', P(8, 'State one use for a convex mirror.'),
      [anyn(None, 1, 4, open_list=True, note_sel=PA(2), options=EG('e.g. cars, shops, roads, etc.', 3))],
      'phys-2-3', 'use-of-convex-mirror', SQ(15, 'State one use for a convex mirror.'), 4, stem=[CONVEX9],
      id='phys-2022-ol-q9-ix',
      decision='The scheme prints examples ("e.g. ... etc.") for one use at [4]: an open menu of one.'),
    # ---------------------------------------------------------------- Q10 --
    T('10i', 'Q10(i)', 'B', P(9, 'Sound is an example of a mechanical wave which therefore needs a', 'sound is a mechanical wave.'),
      [R('apparatus, e.g. source of sound, bell jar', 3), R('method 1: e.g. place source of sound in jar', 3),
       R('method 2: e.g. turn on vacuum pump', 3), C('observation', 3)], 'phys-2-5', 'sound-needs-a-medium',
      SQ(16, 'Sound is an example of a mechanical wave which therefore needs a medium to travel', 'through.'), 12,
      stem=[SING10], id='phys-2022-ol-q10-i', decision=EXPT + ' "observation" names what earns its marks only.'),
    T('10ii', 'Q10(ii)', 'B', P(9, 'Sound is also an example of a longitudinal wave.', 'longitudinal wave?'),
      [R('wave displacement is parallel to direction of wave', 6, note_sel=PA(3))], 'phys-2-2', 'longitudinal-wave',
      SQ(16, 'Sound is also an example of a longitudinal wave. What is a longitudinal wave?'), 6,
      id='phys-2022-ol-q10-ii'),
    T('10iii', 'Q10(iii)', 'B', P(9, 'A doorway may cause a sound wave to diffract but it will not cause a light wave to do',
                                 'so. Explain why.'),
      [C('appropriate reference to width of doorway and wavelength of sound/light', 6, note_sel=PA(3))], 'phys-2-3',
      'diffraction-through-a-doorway',
      SQ(16, 'A doorway may cause a sound wave to diffract but it will not cause a light wave to do', 'so. Explain why.'),
      6, stem=[WAVES10], id='phys-2022-ol-q10-iii'),
    T('10iv', 'Q10(iv)', 'B', P(9, 'Describe an experiment to show that sound waves undergo interference.'),
      [R('apparatus, e.g. two speakers (emitting the same sound)', 3), R('method, e.g. walk between the speakers', 3),
       C('observation', 3)], 'phys-2-6', 'interference-of-sound',
      SQ(16, 'Describe an experiment to show that sound waves undergo interference.'), 9, stem=[WAVES10],
      id='phys-2022-ol-q10-iv', decision=EXPT + ' "observation" names what earns its marks only.'),
    T('10v', 'Q10(v)', 'B', P(9, 'Sound waves do not undergo polarisation but light waves do.', 'polarisation?'),
      [R('wave vibrations restricted to one plane', 6, note_sel=PA(3))], 'phys-2-7', 'polarisation',
      SQ(16, 'Sound waves do not undergo polarisation but light waves do. What is meant by', 'polarisation?'), 6,
      id='phys-2022-ol-q10-v'),
    T('10vi', 'Q10(vi)', 'B', P(9, 'What is meant by resonance?'),
      [R('transfer of energy between two objects of similar natural frequency', 6, note_sel=PA(3))], 'phys-2-6',
      'resonance', SQ(16, 'What is meant by resonance?'), 6, stem=[EAR10], id='phys-2022-ol-q10-vi'),
    T('10vii', 'Q10(vii)', 'B', P(9, 'Draw a labelled diagram to show the first position of resonance',
                                 'for a sound wave in a pipe open at one end.'),
      [R('node at closed end, anti-node at open end, no other nodes or antinodes', 6,
         note_sel=S('[–1 if no label present on diagram]', '[accept partial answer for 3]'))], 'phys-2-6',
      'first-position-of-resonance',
      SQ(16, 'Draw a labelled diagram to show the first position of resonance for a sound wave in a',
         'pipe open at one end.'), 6, stem=[PIPE10], id='phys-2022-ol-q10-vii'),
    T('10viii', 'Q10(viii)', 'B', P(9, 'The frequency of a sound wave is 2800 Hz and it has a',
                                   'wavelength of 0.12 m. Calculate the speed of the wave.'),
      [R('2800 × 0.12 = 336 m s⁻¹', 5, note_sel=S('[accept partial answer for 3, e.g. c = fλ]'))], 'phys-2-2',
      'speed-of-sound-wave',
      SQ(16, 'The frequency of a sound wave is 2800 Hz and it has a wavelength of 0.12 m. Calculate',
         'the speed of the wave.'), 5, id='phys-2022-ol-q10-viii'),
    # ---------------------------------------------------------------- Q11 --
    T('11i', 'Q11(i)', 'B', P(10, 'What is electric current?'),
      [R('flow of charge', 6, note_sel=PA(3))], 'phys-3-3', 'electric-current', SQ(17, 'What is electric current?'), 6,
      stem=[FRANKLIN11], id='phys-2022-ol-q11-i'),
    T('11ii', 'Q11(ii)', 'B', P(10, 'Name an instrument used to measure electric current.'),
      [R('ammeter /galvanometer / multimeter', 6, note_sel=S('[accept partial answer for 3, e.g. voltmeter, ohmmeter]'))],
      'phys-3-3', 'instrument-for-current', SQ(17, 'Name an instrument used to measure electric current.'), 6,
      id='phys-2022-ol-q11-ii'),
    T('11iii', 'Q11(iii)', 'B', [P(10, 'A torch contains a battery, a light bulb and a switch. Draw a circuit',
                                   'diagram to show how these components are connected in a torch.'),
                                 P(10, '(You may refer to the electrical circuit symbols on pages 72 to 78 of the booklet of',
                                   'Formulae and Tables.)')],
      [C('component symbols', 3, units=[1, 1, 1], note=CRIT + ' It prices them [3 × 1]: 1 mark per symbol.'),
       R('connected in series', 3)], 'phys-3-3', 'torch-circuit',
      SQ(17, 'A torch contains a battery, a light bulb and a switch. Draw a circuit diagram to show',
         'how these components are connected in a torch.'), 6, source_pages=[10], id='phys-2022-ol-q11-iii',
      decision='"component symbols [3 × 1]": one row of three 1-mark units. '
               + LINKED.format(w='"a circuit diagram"')),
    T('11iv', 'Q11(iv)', 'B', P(10, 'The wires in a circuit are made of metal. Explain why.'),
      [R('conductor', 3)], 'phys-3-3', 'metal-wires', SQ(17, 'The wires in a circuit are made of metal. Explain why.'),
      3, id='phys-2022-ol-q11-iv'),
    T('11v', 'Q11(v)', 'B', P(10, 'Name the subatomic particle that is the charge carrier in a metal.'),
      [R('electron', 6, note_sel=S('[accept partial answer for 3, e.g. proton, neutron]'))], 'phys-3-3',
      'charge-carrier-in-metal', SQ(17, 'Name the subatomic particle that is the charge carrier in a metal.'), 6,
      id='phys-2022-ol-q11-v'),
    T('11vi', 'Q11(vi)', 'B', P(10, 'A charge of 30 C passes through a wire in a time of 6 s.', 'the wire.'),
      [R('30 ÷ 6 = 5 A', 6, note_sel=PA(3))], 'phys-3-3', 'current-from-charge-and-time',
      SQ(17, 'A charge of 30 C passes through a wire in a time of 6 s.', 'the wire.'), 6, id='phys-2022-ol-q11-vi'),
    T('11vii', 'Q11(vii)', 'B', P(10, 'The wire has a resistance of 3 Ω.', 'wire.'),
      [R('5 × 3 = 15 V', 6, note_sel=PA(3))], 'phys-3-3', 'potential-difference-across-wire',
      SQ(17, 'The wire has a resistance of 3 Ω.', 'wire.'), 6,
      stem=[M('(vi)', 10), P(10, 'A charge of 30 C passes through a wire in a time of 6 s.', 'the wire.')],
      id='phys-2022-ol-q11-vii'),
    T('11viii', 'Q11(viii)', 'B', P(10, 'The 3 Ω wire is connected in parallel with another wire of resistance 2 Ω.',
                                   'total resistance of the two wires in parallel.'),
      [R('1/R₁ + 1/R₂ = 1/RT', 3), C('substitution', 3), R('RT = 1.2 Ω', 3, note_sel=PA(3))], 'phys-3-3',
      'resistors-in-parallel',
      SQ(17, 'The 3 Ω wire is connected in parallel with another wire of resistance 2 Ω.',
         'total resistance of the two wires in parallel.'), 9, id='phys-2022-ol-q11-viii'),
    T('11ix', 'Q11(ix)', 'B', P(10, 'What is the resistance of a 3 m piece of the same wire?'),
      [R('24 Ω / double', 4, note_sel=PA(2))], 'phys-3-3', 'resistance-and-length',
      SQ(17, 'What is the resistance of a 3 m piece of the same wire?'), 4, stem=[WIRE11], id='phys-2022-ol-q11-ix'),
    T('11x', 'Q11(x)', 'B', P(10, 'State the relationship between the resistance of a wire and its cross‐sectional area.',
                             'cross‐sectional area.'),
      [R('inversely proportional', 4, note_sel=PA(2))], 'phys-3-3', 'resistance-and-cross-sectional-area',
      SQ(17, 'State the relationship between the resistance of a wire and its cross-sectional area.'), 4,
      stem=[WIRE11], id='phys-2022-ol-q11-x'),
    # ---------------------------------------------------------------- Q12 --
    T('12i', 'Q12(i)', 'B', P(11, 'State two properties of the electron.'),
      [anyn(None, 2, 4, open_list=True, note='The scheme prints "[4 + 4]".',
            options=EG('e.g. negative charge, small mass etc.', 2, last=' etc.'))], 'phys-4-1',
      'properties-of-the-electron', SQ(18, 'State two properties of the electron.'), 8, stem=[STONEY12],
      id='phys-2022-ol-q12-i',
      decision='The scheme prints two examples ("e.g. ... etc.") for two properties at [4 + 4]: an open menu of two at 4.'),
    T('12ii', 'Q12(ii)', 'B', P(11, 'Describe an experiment to demonstrate the photoelectric', 'effect.'),
      [R('apparatus [e.g. electroscope, zinc plate, uv lamp]', 3), C('method', 3), C('observation', 3)], 'phys-4-2',
      'photoelectric-effect-experiment', SQ(18, 'Describe an experiment to demonstrate the photoelectric effect.'), 9,
      stem=[PHOTO12], id='phys-2022-ol-q12-ii', decision=EXPT + ' "method" and "observation" name what earns only.'),
    T('12iii', 'Q12(iii)', 'B', P(11, 'Describe what happens if the frequency of the incident light is below the threshold',
                                 'frequency.'),
      [R('photoelectric effect does not occur', 3)], 'phys-4-2', 'below-threshold-frequency',
      SQ(18, 'Describe what happens if the frequency of the incident light is below the threshold', 'frequency.'), 3,
      stem=[THRESHOLD12], id='phys-2022-ol-q12-iii'),
    T('12iva', 'Q12(iv)(a)', 'B', P(11, 'Calculate the wavelength of light of this frequency.'),
      [R('(3 × 10⁸) ÷ (6.5 × 10¹⁴) = 4.6 × 10⁻⁷ m', 6, note_sel=PA(3))], 'phys-4-2', 'wavelength-at-threshold',
      SQ(18, 'Calculate the wavelength of light of this frequency.'), 6, stem=[ZINC12], id='phys-2022-ol-q12-iv',
      decision=bundled('(a) and (b)', '(a)')),
    T('12ivb', 'Q12(iv)(b)', 'B', P(11, 'Calculate the energy of a photon of this frequency.'),
      [R('(6.6 × 10⁻³⁴) × (6.5 × 10¹⁴) = 4.3 × 10⁻¹⁹ J', 6, note_sel=PA(3))], 'phys-4-2', 'photon-energy-at-threshold',
      SQ(18, 'Calculate the energy of a photon of this frequency.'), 6, stem=[ZINC12]),
    T('12v', 'Q12(v)', 'B', P(11, 'How are electrons produced in an X–ray tube?'),
      [R('thermionic emission / hot cathode', 6, note_sel=PA(3))], 'phys-4-2', 'electrons-in-x-ray-tube',
      SQ(18, 'How are electrons produced in an X–ray tube?'), 6, stem=[XRAY12], id='phys-2022-ol-q12-v'),
    T('12vi', 'Q12(vi)', 'B', P(11, 'How are electrons accelerated in an X–ray tube?'),
      [R('[high] voltage', 6, note_sel=PA(3))], 'phys-4-2', 'accelerating-electrons',
      SQ(18, 'How are electrons accelerated in an X–ray tube?'), 6, stem=[XRAY12], id='phys-2022-ol-q12-vi'),
    T('12vii', 'Q12(vii)', 'B', P(11, 'Tungsten is often used as the target in an X–ray tube.',
                                 'that makes it suitable to use as the target.'),
      [anyn(None, 1, 6, open_list=True, note_sel=PA(3),
            options=EG('e.g. high melting point, high specific heat capacity', 2))], 'phys-4-2', 'tungsten-target',
      SQ(18, 'Tungsten is often used as the target in an X–ray tube.', 'that makes it suitable to use as the target.'),
      6, stem=[XRAY12], id='phys-2022-ol-q12-vii',
      decision='The scheme prints two examples ("e.g.") for one property at [6]: an open menu of one.'),
    T('12viii', 'Q12(viii)', 'B', P(11, 'What material could be used to ensure that the X–rays do not escape from the X–ray',
                                   'tube?'),
      [R('lead', 6, note_sel=PA(3))], 'phys-4-2', 'shielding-x-rays',
      SQ(18, 'What material could be used to ensure that the X–rays do not escape from the X–ray', 'tube?'), 6,
      stem=[XRAY12], id='phys-2022-ol-q12-viii'),
    # ---------------------------------------------------------------- Q13 --
    T('13i', 'Q13(i)', 'B', P(12, 'Describe what happens during a solar eclipse.'),
      [R('light from the Sun is blocked by the Moon', 7, note_sel=PA(4))], 'phys-2-3', 'solar-eclipse',
      SQ(19, 'Describe what happens during a solar eclipse.'), 7, stem=[SOLAR13], id='phys-2022-ol-q13-i'),
    T('13ii', 'Q13(ii)', 'B', P(12, 'Lunar eclipses are more common than solar eclipses. Explain why.'),
      [R('the Earth’s shadow is bigger than the Moon’s shadow', 7, note_sel=PA(4))], 'phys-2-3',
      'lunar-eclipses-more-common', SQ(19, 'Lunar eclipses are more common than solar eclipses. Explain why.'), 7,
      stem=[LUNAR13], id='phys-2022-ol-q13-ii'),
    T('13iii', 'Q13(iii)', 'B', P(12, 'The light from the Sun is refracted as it passes through the Earth’s atmosphere.',
                                 'Explain what is meant by refraction.'),
      [R('bending of a wave as it travels from one medium to another', 7, note_sel=PA(4))], 'phys-2-3', 'refraction',
      SQ(19, 'The light from the Sun is refracted as it passes through the Earth’s atmosphere.',
         'Explain what is meant by refraction.'), 7, id='phys-2022-ol-q13-iii'),
    T('13iv', 'Q13(iv)', 'B', P(12, 'Name two pieces of laboratory equipment that can be used to disperse light.'),
      [anyn(None, 2, 4, steps=[4, 3], open_list=True, note=ORDERED.format(cell='[4 + 3]'),
            options=EG('e.g. prism, diffraction grating etc.', 2, last=' etc.'))], 'phys-2-3', 'dispersing-light',
      SQ(19, 'Name two pieces of laboratory equipment that can be used to disperse light.'), 7, stem=[LUNAR13],
      id='phys-2022-ol-q13-iv',
      decision='The scheme prints two examples ("e.g. ... etc.") for two pieces of equipment at [4 + 3]: an open menu '
               'of two, priced step by step.'),
    T('13v', 'Q13(v)', 'B', P(12, 'The Moon has a mass of 7.3 × 10²² kg and a radius of 1.7 × 10⁶ m.',
                             'acceleration due to gravity on the Moon.'),
      [R('(6.7 × 10⁻¹¹) × (7.3 × 10²²) ÷ (1.7 × 10⁶)² = 1.7 m s⁻²', 7, note_sel=PA(4))], 'phys-1-5',
      'gravity-on-the-moon',
      SQ(19, 'The Moon has a mass of 7.3 × 10²² kg and a radius of 1.7 × 10⁶ m.',
         'acceleration due to gravity on the Moon.'), 7, id='phys-2022-ol-q13-v'),
    T('13vi', 'Q13(vi)', 'B', P(12, 'An astronaut weighs less on the Moon than she does on Earth.', 'and weight.'),
      [R('mass is how much matter is in something / weight is force of gravity', 7, note_sel=PA(4))], 'phys-1-5',
      'mass-and-weight',
      SQ(19, 'An astronaut weighs less on the Moon than she does on Earth. Distinguish between mass', 'and weight.'), 7,
      id='phys-2022-ol-q13-vi'),
    T('13vii', 'Q13(vii)', 'B', P(12, 'Infrared radiation lies just beyond red light in the electromagnetic spectrum, with a slightly',
                                 'How can infrared radiation be detected?'),
      [anyn(None, 1, 7, open_list=True, note_sel=PA(4),
            options=EG('e.g. blackened thermometer, [digital] camera etc.', 2, last=' etc.'))], 'phys-2-4',
      'detecting-infrared',
      SQ(19, 'Infrared radiation lies just beyond red light in the electromagnetic spectrum, with a slightly',
         'How can infrared radiation be detected?'), 7, id='phys-2022-ol-q13-vii',
      decision='The scheme prints two examples ("e.g. ... etc.") for one detector at [7]: an open menu of one.'),
    T('13viii', 'Q13(viii)', 'B', P(12, 'Name the type of electromagnetic radiation that has a slightly shorter wavelength than',
                                   'visible light.'),
      [R('ultraviolet / uv', 7, note_sel=PA(4))], 'phys-2-4', 'ultraviolet',
      SQ(19, 'Name the type of electromagnetic radiation that has a slightly shorter wavelength than', 'visible light.'),
      7, id='phys-2022-ol-q13-viii'),
    # ---------------------------------------------------------------- Q14 --
    T('14ai', 'Q14(a)(i)', 'B', P(13, 'What is meant by kinetic energy?'),
      [R('energy due to motion', 3)], 'phys-1-4', 'kinetic-energy', SQ(20, 'What is meant by kinetic energy?'), 3,
      stem=[STONE14], id='phys-2022-ol-q14-a-i'),
    T('14aii', 'Q14(a)(ii)', 'B', P(13, 'State the principle of conservation of energy.'),
      [R('energy cannot be created or destroyed', 6, note_sel=PA(3))], 'phys-1-4', 'conservation-of-energy',
      SQ(20, 'State the principle of conservation of energy.'), 6, id='phys-2022-ol-q14-a-ii'),
    T('14aiii', 'Q14(a)(iii)', 'B', P(13, 'What is the main type of energy that the stone’s kinetic energy is being',
                                     'converted into as it travels upwards?'),
      [R('potential energy', 6, note_sel=PA(3))], 'phys-1-4', 'kinetic-to-potential-energy',
      SQ(20, 'What is the main type of energy that the stone’s kinetic energy is being',
         'converted into as it travels upwards?'), 6, stem=[STONE14], id='phys-2022-ol-q14-a-iii'),
    T('14aiv', 'Q14(a)(iv)', 'B', P(13, 'Calculate the kinetic energy of the stone when it is thrown.'),
      [R('½ × 0.005 × 15² = 0.5625 J', 5, note_sel=PA(3))], 'phys-1-4', 'kinetic-energy-of-stone',
      SQ(20, 'Calculate the kinetic energy of the stone when it is thrown.'), 5, stem=[STONE14],
      id='phys-2022-ol-q14a-iv'),
    T('14av', 'Q14(a)(v)', 'B', P(13, 'Calculate the maximum height reached by the stone.'),
      [pt(S('0.5625 ÷ (0.005 × 9.8) = 11.5 m', '// 15² ÷ (2 × 9.8) = 11.5 m', piece=1, psep='//'), 5,
          note_sel=PA(3), route='side-a'),
       pt(S('0.5625 ÷ (0.005 × 9.8) = 11.5 m', '// 15² ÷ (2 × 9.8) = 11.5 m', piece=2, psep='//'), 5,
          route='side-b')],
      'phys-1-4', 'maximum-height-of-stone', SQ(20, 'Calculate the maximum height reached by the stone.'), 5,
      stem=[STONE14, G14], id='phys-2022-ol-q14a-v',
      decision='The scheme prints two methods separated by "//", each the whole answer at [5]: routes inside the card.'),
    T('14avi', 'Q14(a)(vi)', 'B', P(13, 'What is the unit of energy?'),
      [R('Joule / J', 3)], 'phys-1-4', 'unit-of-energy', SQ(20, 'What is the unit of energy?'), 3,
      id='phys-2022-ol-q14-a-vi'),
    T('14bi', 'Q14(b)(i)', 'B', P(13, 'Describe an experiment to demonstrate total internal reflection.'),
      [R('apparatus 1, e.g. ray box / laser', 3), R('apparatus 2, 3.g. semi-circular glass block', 3), C('method', 3),
       C('observation', 3)], 'phys-2-3', 'total-internal-reflection-experiment',
      SQ(21, 'Describe an experiment to demonstrate total internal reflection.'), 12, stem=[MIRAGE14],
      decision='The bank had no card for this part. ' + EXPT + ' The scheme prints "3.g." for "e.g." in its second '
               'apparatus line: lifted as printed.'),
    T('14bii', 'Q14(b)(ii)', 'B', P(13, 'If the light from a distant object comes to focus in front of the retina, the person',
                                   'What type of lens is used to correct short sightedness?'),
      [R('concave / diverging', 6, note_sel=PA(3))], 'phys-2-3', 'correcting-short-sight',
      SQ(21, 'If the light from a distant object comes to focus in front of the retina, the person',
         'What type of lens is used to correct short sightedness?'), 6, stem=[EYE14], id='phys-2022-ol-q14-b-ii'),
    T('14biiia', 'Q14(b)(iii)(a)', 'B', P(13, 'Calculate the power of the combination of the eye and the lens.'),
      [R('P = 62 + (–2) = 60 m⁻¹', 5, note_sel=PA(3))], 'phys-2-3', 'power-of-combination',
      SQ(21, 'Calculate the power of the combination of the eye and the lens.'), 5, stem=[GLASSES14],
      id='phys-2022-ol-q14-b-iiia'),
    T('14biiib', 'Q14(b)(iii)(b)', 'B', P(13, 'Calculate the focal length of the lens in the glasses.'),
      [R('f = 1 ÷ 2 = 0.5 m', 5, note_sel=PA(3))], 'phys-2-3', 'focal-length-of-glasses',
      SQ(21, 'Calculate the focal length of the lens in the glasses.'), 5, stem=[GLASSES14],
      id='phys-2022-ol-q14-b-iiib'),
    T('14ci', 'Q14(c)(i)', 'B', P(14, 'A moment is a turning effect caused by a force.',
                                 'the total clockwise moment about the midpoint of the metre stick.'),
      [R('(2 × 0.1) + (4 × 0.3) = 1.4 N m', 6, note_sel=PA(3))], 'phys-1-2', 'clockwise-moment',
      SQ(22, 'A moment is a turning effect caused by a force.',
         'the total clockwise moment about the midpoint of the metre stick.'), 6, stem=[STICK14], fig='q14c-diagram',
      decision='The bank had no card for this part.'),
    T('14cii', 'Q14(c)(ii)', 'B', P(14, 'The 7 N force results in an anticlockwise moment about the midpoint of the',
                                   'metre stick.', end_nth=2),
      [R('7 × 0.2 = 1.4 N m', 6, note_sel=PA(3))], 'phys-1-2', 'anticlockwise-moment',
      SQ(22, 'The 7 N force results in an anticlockwise moment about the midpoint of the', 'metre stick.', ), 6,
      stem=[STICK14], fig='q14c-diagram', decision='The bank had no card for this part.'),
    T('14ciii', 'Q14(c)(iii)', 'B', P(14, 'State the law of equilibrium verified by the calculations in (i) and (ii).'),
      [R('clockwise moments = anti-clockwise moments', 6, note_sel=PA(3))], 'phys-1-2', 'law-of-equilibrium',
      SQ(22, 'State the law of equilibrium verified by the calculations in (i) and (ii).'), 6, stem=[STICK14],
      fig='q14c-diagram', id='phys-2022-ol-q14-c-iii'),
    T('14civ', 'Q14(c)(iv)', 'B', P(14, 'The upward force on the metre stick is 15 N.', 'stick.'),
      [R('15 – (7 + 2 + 4) = 2 N', 6, note_sel=PA(3))], 'phys-1-2', 'weight-of-metre-stick',
      SQ(22, 'The upward force on the metre stick is 15 N.', 'stick.'), 6, stem=[STICK14], fig='q14c-diagram',
      decision='The bank had no card for this part.'),
    T('14cv', 'Q14(c)(v)', 'B', P(14, 'Your calculations assume that the centre of gravity of the metre stick acts at the',
                                 'invalid?'),
      [R('e.g. chipped metre stick etc.', 4, note_sel=PA(2))], 'phys-1-2', 'centre-of-gravity-assumption',
      SQ(22, 'Your calculations assume that the centre of gravity of the metre stick acts at the',
         'What might cause this assumption to be invalid?'), 4, stem=[STICK14], fig='q14c-diagram',
      id='phys-2022-ol-q14-c-v'),
    T('14di', 'Q14(d)(i)', 'B', P(14, 'Alpha radiation is one of the three types of radiation.',
                                 'Name the other two types of radiation.'),
      [R('beta/β', 3), R('gamma/γ', 3)], 'phys-4-4', 'other-types-of-radiation',
      SQ(23, 'Alpha radiation is one of the three types of radiation.', 'Name the other two types of radiation.'), 6,
      stem=[BECQ14], id='phys-2022-ol-q14-d-i'),
    T('14dii', 'Q14(d)(ii)', 'B', P(14, 'Alpha radiation is the least penetrating of the three types of',
                                   'types of radiation have different penetrating powers.'),
      [R('apparatus 1: source of radiation', 3), R('apparatus 2: barrier[s]', 3), C('method', 3),
       R('observation / detector', 3)], 'phys-4-4', 'penetrating-power-experiment',
      SQ(23, 'Alpha radiation is the least penetrating of the three types of radiation.', 'penetrating powers.'), 12,
      stem=[BECQ14], id='phys-2022-ol-q14d-ii', decision=EXPT + ' "method" names what earns its marks only.'),
    T('14diii', 'Q14(d)(iii)', 'B', P(14, 'How many neutrons are there in an atom of', '²²⁶?'),
      [R('226 – 88 = 138', 6, note_sel=S('[accept partial answer for 3, e.g. number of protons]'))], 'phys-4-4',
      'neutrons-in-radium-226', SQ(23, 'How many neutrons are there in an atom of', '²²⁶?'), 6, stem=[RADIUM14],
      qfig='q14diii-question', id='phys-2022-ol-q14-d-iii',
      decision='The radium nuclide is printed with its mass number above its atomic number after the symbol, which '
               'the text layer reads as two lines ("Ra₈₈ ²²⁶"): the question is shown as printed.'),
    T('14div', 'Q14(d)(iv)', 'B', P(14, 'What is the daughter nucleus when an atom of', 'particles?'),
      [G('equation', page=23, clip=(135, 356, 180, 386), expect='Po²¹⁸₈₄', marks=4, units=[2, 1, 1],
         note_sel=PA(2), note_lead='The scheme prices the nuclide [2 + 1 + 1].')],
      'phys-4-4', 'daughter-of-radium-226', SQ(23, 'What is the daughter nucleus when an atom of', 'particles?'), 4,
      stem=[RADIUM14], qfig='q14div-question', id='phys-2022-ol-q14-d-iv',
      decision='The scheme prints the polonium nuclide with its numbers stacked after the symbol: read from where '
               'they are printed, one row at the printed [2 + 1 + 1] = 4. The radium nuclide in the ask is printed '
               'the same way: the question is shown as printed.'),
]

ANSWER_VARIANTS = {}
RETAINED = {}
WITHDRAW = {}

FIGURES = {
    # key suffix: (doc, page, rect in PDF points, credit, letters, alt, solution)
    'q2-table': ('paper', 2, (90, 497, 505, 554), SEC, [],
                 'Table of the results: i (degrees) 30, 40, 50, 60; r (degrees) 19, 25, 31, 35.', False),
    'q3-table': ('paper', 3, (84, 233, 541, 334), SEC, [],
                 'Table of the results: f (Hz) 256, 320, 341, 427, 480, 512; l (cm) 22, 18, 17, 13, 12, 11; and a '
                 'third row headed 1 over l (cm⁻¹), set as a fraction, with its six cells left empty.', False),
    'q3viii-question': ('paper', 3, (25, 52, 548, 430), SEC, [],
                        'The printed Question 3: the stretched-string experiment, parts (i) to (iv), its table of f (Hz) '
                        '256, 320, 341, 427, 480, 512 against l (cm) 22, 18, 17, 13, 12, 11 with an empty row for 1 '
                        'over l, and parts (v) to (viii), (viii) asking for a graph of f against 1 over l, set as a '
                        'fraction.', False),
    'q5-table': ('paper', 4, (82, 526, 541, 610), SEC, [],
                 'Table of the results: I (A) 1, 1.5, 2, 2.5, 3, 3.5; an empty row for I² (A²); Δθ (°C) 1.2, 2.7, 4.8, '
                 '7.5, 10.8, 14.7.', False),
    'q7vii-scheme': ('scheme', 13, (398, 465, 541, 535), SEC, ['F', 'R', 'W'],
                     "The marking scheme's force diagram: a box with four arrows, F pointing left, Fr. pointing "
                     "right, R pointing up and W pointing down.", True),
    'q7ix-scheme': ('scheme', 13, (112, 593, 268, 663), SEC, [],
                    "The marking scheme's sketch: speed against time, a dashed line rising straight from the origin "
                    "and then running level.", True),
    'q8-graph': ('paper', 7, (135, 72, 450, 266), SEC, ['X', 'Y'],
                 'Graph of temperature against heat added: a line rising from the origin through a stretch labelled '
                 'solid, a level stretch labelled melting, a rising stretch labelled X, a long level stretch labelled '
                 'Y, and a final rising stretch labelled gas.', False),
    'q9-diagram': ('paper', 8, (85, 140, 507, 294), SEC, [],
                   'Ray diagram to complete: a dashed principal axis with an upright arrow labelled object on the left, '
                   'a point labelled f on the axis to its right, and a concave mirror curving across the axis further '
                   'right.', False),
    'q14c-diagram': ('paper', 14, (110, 89, 485, 228), SEC, [],
                     'Diagram of a metre stick marked 10 cm to 90 cm, held up by an arrow pointing up at 50, with arrows '
                     'pointing down at 30 (7 N), 60 (2 N) and 80 (4 N).', False),
    'q14diii-question': ('paper', 14, (100, 612, 450, 657), SEC, [],
                         'The printed lines: "Radium (Ra, with 226 above 88 after the symbol) is an alpha emitter." and '
                         'part (iii), "How many neutrons are there in an atom of" the same radium nuclide.', False),
    'q14div-question': ('paper', 14, (100, 612, 500, 697), SEC, [],
                        'The printed lines: "Radium (Ra, with 226 above 88 after the symbol) is an alpha emitter.", '
                        'part (iii), and part (iv), "What is the daughter nucleus when an atom of" the same radium '
                        'nuclide "emits two alpha particles?"', False),
}
