"""Physics 2026 Higher Level — reviewed task ledger, carded from the paper for the first time.

Independent visual sweep (2026-10-28), every page rendered and read:
  * The paper (LC021ALP000EV), 20 pages: p1 cover ("Answer three questions from Section A and
    five questions from Section B"), p2-p6 Section A Questions 1-5 (experiments, 40 marks each,
    group marks printed after runs of romans), p7-p18 Section B Questions 6-14 (56 marks each),
    p19 acknowledgements (images on pages 7, 10, 14, 15, 17), p20 back cover.
  * The marking scheme, 27 pages: p1 cover, p2 note on published schemes, p3 points to note
    (solidus, double solidus, units, graphs, slips), p4 annotation symbols, p5 Irish-language
    bonus table, p6-p25 Questions 1-14 (each question reprinted in regular type, its answers in
    bold, the mark cells at the right margin), p26 blank, p27 back cover.

Every printed ask is carded at the scheme's own mark boundary: a roman, or a sub-letter inside a
roman where the scheme prices (a) and (b) apart. Where one cell prices a roman's sub-letters
together (Q11(ii) "[4 + 2]", Q12(iv) "[3 + 3]", Q13(iii)'s shared "label axes [3]") the roman
is one card. Q6 is "Answer any eight of (a)-(l)" (best eight of twelve at 7 each = 56) and
prints (l) as "(i) ... or (ii) ...": both alternatives are carded. Q14 is "Answer any two of
(a), (b), (c), (d)" (four 28s, 112 carded); its (d) is "Answer either part (a) or part (b)",
two printed alternatives carded as routes 'part-a' and 'part-b' of the census leaves Q14(d)(i)-
(iv) (Part (a) counts toward (d)'s printed 28: 16 + 12; Part (b)'s 10 + 18 is checked by hand).

The census read (paper_census) needed one gated entry (paper.PROSE_MARKER_BLOCKS, 2026 HL): Q4's
data-table unit cells "(g) 64.6" and Q14's letters printed inside romans had made phantom parts.

Mark cells: "[3 + 2]" printed against two lines (a formula and its step) gives each line its
mark in order; a list the scheme prints as interchangeable items under one sum ("any two lines
[4 + 3]", "resistance, current(squared), time [3 + 2 + 2]") is a menu priced step by step
(anyn steps). Stacked fractions are read with G('fraction'). Q2(v)'s "T = 2pi root(l/g)", whose root
the text layer breaks, is shown as a crop of the scheme beside the scheme's own words ("slope
formula"); Q13(iv)(c)'s "Vrms = Vpeak / root 2", whose "=" reads as a Malayalam sign (repaired by the
bank's glyph map at build), is read with G('fraction') and also shown as a crop.
"""
from phys_review_lib import Q, SQ, S, M, pt, anyn, allof, G, T, L, unprinted

YEAR, LEVEL = 2026, 'hl'
REVIEWED_AT = '2026-10-28'
LETTERED = {6, 14}

SOURCES = {
    'paper': {'path': 'examiner-reports/physics/papers/2026-hl-paper.pdf', 'fileid': 'LC021ALP000EV.pdf',
              'sha256': 'fd1ff3286d201f396a282c38d4bf0f40adf71a1fca80d9111e763a4141a200d5', 'pages': 20},
    'scheme': {'path': 'examiner-reports/physics/schemes/2026-hl.pdf', 'fileid': 'LC021ALP000EV.pdf',
               'sha256': '228dec63cad7a6c8653dfb8b84ac29e908ec34277869cafea69e9481ad199463', 'pages': 27},
}

PAGE_ROLES = {
    'paper': {1: 'cover', **{p: 'questions' for p in range(2, 19)}, 19: 'acknowledgements', 20: 'back-cover'},
    'scheme': {1: 'cover', 2: 'note', 3: 'conventions', 4: 'annotations', 5: 'irish-bonus-table',
               **{p: 'marking' for p in range(6, 26)}, 26: 'blank', 27: 'back-cover'},
}

QUESTION_TOTALS = {**{n: 40 for n in range(1, 6)}, **{n: 56 for n in range(6, 14)},
                   14: 112}   # Q14: any two of four 28s
PART_TOTALS = {(14, x): 28 for x in 'abcd'}
BEST_OF = {6: (8, 7)}
GROUP_TOTALS = {
    (1, ('i', 'ii')): 18, (1, ('iii', 'iv', 'v')): 22,
    (2, ('i', 'ii', 'iii')): 18, (2, ('iv', 'v')): 22,
    (3, ('i', 'ii')): 18, (3, ('iii', 'iv', 'v')): 22,
    (4, ('i', 'ii', 'iii', 'iv', 'v')): 21, (4, ('vi',)): 19,
    (5, ('i', 'ii', 'iii')): 21, (5, ('iv', 'v', 'vi')): 19,
    (7, ('i', 'ii')): 19, (7, ('iii', 'iv', 'v', 'vi')): 27, (7, ('vii',)): 10,
    (8, ('i', 'ii', 'iii')): 15, (8, ('iv', 'v', 'vi', 'vii')): 32, (8, ('viii',)): 9,
    (9, ('i', 'ii')): 15, (9, ('iii', 'iv', 'v')): 22, (9, ('vi', 'vii', 'viii')): 19,
    (10, ('i', 'ii', 'iii')): 26, (10, ('iv', 'v')): 18, (10, ('vi',)): 12,
    (11, ('i', 'ii', 'iii')): 22, (11, ('iv', 'v', 'vi', 'vii', 'viii')): 34,
    (12, ('i', 'ii', 'iii')): 24, (12, ('iv', 'v', 'vi', 'vii', 'viii')): 32,
    **{(13, (r,)): 7 for r in ('i', 'ii', 'iii', 'v', 'vi', 'vii')}, (13, ('iv',)): 14,
}
CHECKSUMS = {}

# Q14(d): "Answer either part (a) or part (b)." Each printed address under either part lists both
# alternatives, Part (a) first, so that Part (a) makes (d)'s printed 28 and Part (b) (the same 28:
# 6 + 4 + 9 + 6 + 3) counts once with it. Part (a) prints (iv)(a)/(b), Part (b) (iii)(a)/(b).
ROUTES = {f'Q14(d){r}': ['part-a', 'part-b']
          for r in ('(i)', '(ii)', '(iii)', '(iv)', '(iii)(a)', '(iii)(b)', '(iv)(a)', '(iv)(b)')}

SCAN_PAGES = {'paper': range(1, 19)}
SELECTION_SCAN = [
    ('paper', 2, 'the following', 'Q1 "The following data were recorded": a reference to the table.'),
    ('paper', 3, 'the following', 'Q2 "The following data were recorded": a reference to the table.'),
    ('paper', 4, 'both', 'Q3 lead-in "on both the left and right sides": description.'),
    ('paper', 4, 'the following', 'Q3 "The following data were recorded": a reference to the table.'),
    ('paper', 4, 'the following', 'Q3(iv) "each of the following changes": both changes asked, one card each.'),
    ('paper', 5, 'the following', 'Q4 "The following data were recorded": a reference to the table.'),
    ('paper', 6, 'the following', 'Q5 "The following data were recorded": a reference to the table.'),
    ('paper', 7, 'the following', 'Q6 "Answer any eight of the following parts": best eight of twelve; every '
                                  'part is carded (BEST_OF).'),
    ('paper', 8, 'or', 'Q6(l) "(i) ... or (ii) ...": two printed alternatives, each carded.'),
    ('paper', 9, 'both', 'Q7 stem "measure both the sound intensity and the sound intensity level": description.'),
    ('paper', 10, 'choose', 'Q8(iii) "a dentist may choose a concave mirror": description.'),
    ('paper', 11, 'both', 'Q9 stem "Both instruments generate stationary waves": description.'),
    ('paper', 11, 'both', 'Q9 stem "open at both ends": description.'),
    ('paper', 11, 'or', 'Q9 stem "open at both ends, or open at one end": description.'),
    ('paper', 11, 'both', 'Q9(vii) "open at both ends": description.'),
    ('paper', 12, 'the following', 'Q10 "shown in the following table": a reference to the table.'),
    ('paper', 13, 'or', 'Q11(v) "Fleming\'s left-hand rule, or otherwise": a method, one answer.'),
    ('paper', 14, 'the following', 'Q12(ii) "under the following headings": both headings asked, one card each.'),
    ('paper', 15, 'the following', 'Q13 "Read the following passage": a reference to the passage.'),
    ('paper', 15, 'or', 'Q13 passage "from the air or ground": passage text.'),
    ('paper', 15, 'or', 'Q13 passage "which uses AC, or sell electricity": passage text.'),
    ('paper', 16, 'any two', 'Q14 "Answer any two of the following parts": every part is carded.'),
    ('paper', 16, 'the following', 'Q14 "any two of the following parts": the same rubric.'),
    ('paper', 18, 'either', 'Q14(d) "Answer either part (a) or part (b)": ROUTES part-a and part-b.'),
    ('paper', 18, 'or', 'Q14(d), the same choice.'),
    ('paper', 18, 'the following', 'Q14(d) Part (a) "The following reaction": a reference to the equation.'),
]
ASK_SCAN_PAGES = {'paper': range(2, 19)}
ASK_EXEMPT = [
    (10, 'An underwater lamp is placed at a depth of 0.5 m',
     'Q8 lead-in to (v)-(vii) ("When the lamp is switched on at night ..."): a description, not an ask; lifted '
     'into those cards\' stem.'),
    (15, 'home’s energy system.', 'Q13 passage ("When electricity demand and prices are lower ..."): passage text, '
                                  'not an ask; lifted into the (iii), (iv)(b) and (iv)(c) stems.'),
    (16, 'When a sound-emitting source moves towards a stationary observer',
     'Q14(b) lead-in to (ii): a description, not an ask; lifted into its stem.'),
]

SEC = 'State Examinations Commission'
CRIT = 'The scheme prints no answer here, only what earns the marks.'
NOLABEL = S('[–1 if no label present on diagram]')
ORDERED = ('The scheme prints these items under one sum, {cell}, and names no order: a response earns '
           'the marks step by step.')


def crit(sel, marks, **kw):
    return pt(sel, marks, kind='criterion', note=CRIT, **kw)


def pieces(sel, marks, sep):
    """One row per entry of a printed list, each its own slice, at the marks the scheme's cell
    prints for it in order."""
    return [pt(dict(sel, piece=i + 1, psep=sep), m) for i, m in enumerate(marks)]


def dslash(sel_start, sel_end, side):
    """One side of a line the scheme prints as two answers separated by "//"."""
    return S(sel_start, sel_end, piece=side, psep='//')


# ------------------------------------------------------------------ stems --
Q1S = [Q(2, 'In an experiment to verify Boyle’s law', 'The temperature was kept constant.'),
       Q(2, 'The following data were recorded.'), Q(2, 'p (kPa)', '23')]
Q2S = [Q(3, 'A simple pendulum consisting of a light inextensible string',
         'This procedure was repeated for different values of l.'),
       Q(3, 'The following data were recorded.'), Q(3, 'l (cm)', '47.5')]
Q2IVA = Q(3, 'Draw a suitable graph to show the relationship between the period and the length of',
          'the simple pendulum.')
Q3S = [Q(4, 'In an experiment to measure the wavelength', 'A diffraction grating with 400 lines per mm was used.'),
       Q(4, 'The following data were recorded.'), Q(4, 'left', '28.3', after='The following data were recorded.')]
Q3IV = Q(4, 'Describe the effect that each of the following changes would have on the position of the',
         'bright images formed.')
Q4S = [Q(5, 'In an experiment to measure the specific latent heat',
         'the water was cooled to a temperature below room temperature.'),
       Q(5, 'The following data were recorded.'), Q(5, 'mass of copper calorimeter (g)', '21')]
Q4DATA = Q(5, 'specific heat capacity of water = 4180 J kg⁻¹ K⁻¹; specific heat capacity of copper = 385 J kg⁻¹ K⁻¹')
Q4VI = Q(5, 'Use the data given to calculate')
Q5S = [Q(6, 'In an experiment to investigate how the resistance R',
         'a student measured the resistance of a wire at different temperatures.'),
       Q(6, 'The following data were recorded.'), Q(6, 'θ (°C)', '35.5')]
Q5III = Q(6, 'Use your graph to determine the resistance of the wire when its temperature is 25 °C.')
Q5B = Q(6, 'The wire has a length of 37 cm. The diameter of the wire is 0.5 mm.')
Q7S = Q(9, 'A pile driver is used to sink steel rods', 'of a stationary steel rod.')
Q7SB = Q(9, 'After the steel block strikes the steel rod', 'vertically downwards into the ground.')
Q7G = Q(9, 'acceleration due to gravity = 9.8 m s⁻²')
Q7V = Q(9, 'Calculate the downward velocity of the steel rod immediately after the collision.')
Q7SC = Q(9, 'The pile driver generates a loud sound', 'level due to the sound generated.')
Q7VII = Q(9, 'The observer moves to a distance 4d from the pile driver. Describe the effect on')
Q8L = Q(10, 'Lenses work due to the refraction of light.')
Q8SB = Q(10, 'An underwater lamp is placed at a depth of 0.5 m',
         'on at night, a circular disc of light becomes visible on the surface of the water.')
Q8T = Q(10, 'Light travels as a transverse wave.')
Q9S = Q(11, 'The music produced by a violin', 'Each note has unique characteristics.')
Q9SB = Q(11, 'The fundamental frequency of a stretched string', 'two other factors.')
Q9IIIA = Q(11, 'Name these two factors.')
Q9SC = Q(11, 'In an organ the pipes can act as if they are open at both ends', 'other end.')
Q10S = Q(12, 'A parallel-plate capacitor consists of two metal plates',
         'dielectric. It is designed to store separated electric charge, and so store energy.')
Q10I = Q(12, 'Explain what is meant by')
Q10SB = Q(12, 'A student carried out an experiment to verify the relationship',
          'The student’s results are shown in the following table.')
Q10TAB = Q(12, 'd (m)', '1.64 × 10⁻¹²')
Q10SC = Q(12, 'The circuit diagram shows a 200 μF capacitor connected in series with', '130 μA.')
Q10VI = Q(12, 'Calculate', after='130 μA.')
Q10VIA = Q(12, 'the potential difference across the capacitor at that moment,')
Q11SA = Q(13, 'The principle involved in a cathode ray tube', 'Three beams of electrons were used to produce the primary colours on a screen.')
Q11III = Q(13, 'Explain how the primary colours of light can be combined to form')
Q11SB = Q(13, 'A positively charged particle enters a magnetic field', 'below.')
Q11SC = Q(13, 'An electron in a cathode ray tube starts from rest')
Q11SD = Q(13, 'An electron travels with a speed of 2.66 × 10⁷ m s⁻¹',
          'magnetic flux density of 2 mT perpendicular to its direction of motion.')
Q12S = Q(14, 'Radioactivity was first discovered by Henri Becquerel', 'gamma rays.')
Q12II = Q(14, 'Compare each type of radiation under the following headings:')
Q12IIIA = Q(14, 'Name one type of detector used to detect nuclear radiation.')
Q12SB = Q(14, 'In a radioactive decay series thorium–232 (Th–232) decays to thorium–228 (Th–228).')
Q12SC = Q(14, 'An alpha particle emitted by Th–232', 'it produces ion pairs by colliding with molecules of the air.')
Q12VI = Q(14, 'Explain what is meant by', after='kinetic energy.')
Q12SD = [Q(14, 'Polonium was discovered by Marie and Pierre Curie in 1898.'),
         Q(14, 'A 210 g sample of polonium–210 contains 6.0 × 10²³ nuclei.'),
         Q(14, 'The decay constant of polonium–210 is 5.8134 × 10⁻⁸ s⁻¹.')]
P13 = {k: Q(15, a, b) for k, a, b in [
    ('solar', 'Imagine arriving at your home', 'that reaches these solar panels is 1196 W m⁻².'),
    ('heat', 'Heat pumps quietly and efficiently', 'and use it to warm your living spaces.'),
    ('ev', 'Imagine parking your electrical vehicle', 'which uses AC, or sell electricity back to the grid.'),
    ('house', 'The house of 2030 will feature', 'reduce heat loss and help maintain a steady indoor temperature.'),
    ('led', 'The lighting in your home will be more efficient', 'efficient LEDs will be the standard.')]}
Q13II = Q(15, 'A 10 W LED bulb gives out the same light as a 60 W filament bulb.')
Q13IV = Q(15, 'The lithium-ion battery in an electric car has a capacity of',
          '75 kWh, which is sufficient to power a house during the night.')
Q14SA = Q(16, 'A river flows with a velocity of 1.5 m s⁻¹ downstream.', 'diagram.')
Q14BI = Q(16, 'Explain what is meant by', after='Describe a laboratory experiment to find the resultant of two vectors.')
Q14SB = Q(16, 'When a sound-emitting source moves towards a stationary observer', 'appears to change.')
Q14SB2 = [Q(16, 'A whistle which is emitting a note of frequency 1.1 kHz',
            'a string 1.3 m long with a constant angular velocity of 24 rad s⁻¹.'),
          Q(16, 'velocity of sound in air = 340 m s⁻¹')]
Q14SC = Q(17, 'A positive and a negative point charge are placed a distance apart in a vacuum',
          'electric field strength at X due to negative charge is 4.5 × 10³ N C⁻¹.')
Q14DA = Q(18, 'Two protons are at a distance of 1.5 fm from each other in a nucleus.')
Q14DIV = Q(18, 'Given that, at this distance, the strong nuclear force between the two protons is 120 times',
           'stronger than the force due to their charge, calculate')
Q14DB3 = Q(18, 'Draw a circuit diagram to show how a transistor can be used as a voltage amplifier.')

TASKS = [
    # ============================================================ Section A ==
    # ---- Q1 Boyle's law ------------------------------------------------------
    T('1ia', 'Q1(i)(a)', 'A', Q(2, 'Draw a labelled diagram to show how the apparatus was arranged in this experiment.'),
      [pt(S('trapped gas'), 3), pt(S('pressure gauge'), 3), pt(S('method of reading volume'), 3, note_sel=NOLABEL)],
      'phys-2-1', 'boyles-law-apparatus',
      SQ(6, 'Draw a labelled diagram to show how the apparatus was arranged in this', 'experiment.'), 9, stem=Q1S[:1]),
    T('1ib', 'Q1(i)(b)', 'A', Q(2, 'Describe the steps that the student could have used to determine the volume V and',
                                'the pressure p readings.'),
      [pt(S('open valve / move plunger'), 2), pt(S('volume: read graduated tube'), 2),
       pt(S('pressure: read pressure gauge'), 2)],
      'phys-2-1', 'boyles-law-readings',
      SQ(6, 'Describe the steps that the student could have used to determine the volume V',
         'and the pressure p readings.'), 6, stem=Q1S[:1]),
    T('1ii', 'Q1(ii)', 'A', Q(2, 'How could the student have ensured that the temperature of the gas was kept constant?'),
      [pt(S('allow time between readings'), 3)], 'phys-2-1', 'boyles-law-constant-temperature',
      SQ(6, 'How could the student have ensured that the temperature of the gas was kept', 'constant?'), 3,
      stem=Q1S[:1]),
    T('1iii', 'Q1(iii)', 'A', Q(2, 'Draw a suitable graph to show the relationship between the pressure and the volume of the',
                                'gas.'),
      [pt(S('calculations of 1/V or 1/p'), 3, kind='criterion',
          note='The scheme prints the values of 1/V it expects (shown in the figure).'),
       crit(S('axes labelled'), 3), crit(S('points plotted'), 3), crit(S('line of best fit'), 3)],
      'phys-2-1', 'boyles-law-graph',
      SQ(6, 'Draw a suitable graph to show the relationship between the pressure and the volume of the', 'gas.'),
      12, stem=Q1S, fig='q1iii-scheme-table'),
    T('1iv', 'Q1(iv)', 'A', Q(2, 'Explain how your graph verifies Boyle’s law.'),
      [pt(S('straight line through origin', 'p ∝ 1/V'), 5)], 'phys-2-1', 'boyles-law-graph-verifies',
      SQ(6, 'Explain how your graph verifies Boyle’s law.'), 5, stem=Q1S),
    T('1v', 'Q1(v)', 'A', Q(2, 'Sketch a graph to show the relationship between pV and p for the gas.'),
      [pt(S('labelled axes'), 5, kind='criterion',
          note='The scheme prices this part [3 + 2]: labelled axes, and the sketch it draws (shown in the figure). '
               'It names the sketch in no words of its own.')],
      'phys-2-1', 'boyles-law-pv-against-p',
      SQ(6, 'Sketch a graph to show the relationship between pV and p for the gas.'), 5, stem=Q1S[:1],
      fig='q1v-scheme-sketch',
      decision='The scheme prints "labelled axes" and draws the sketch, with one cell [3 + 2] for both; the '
               'sketch has no words to lift, so the part is one criterion row at the cell\'s 5 with the drawing '
               'cropped from the scheme.'),
    # ---- Q2 simple pendulum ---------------------------------------------------
    T('2i', 'Q2(i)', 'A', Q(3, 'Suggest a reason why the student measured the time for 25 oscillations instead of just one',
                            'oscillation.'),
      [pt(S('to get an average / to reduce error'), 3)], 'phys-1-5', 'why-time-25-oscillations',
      SQ(7, 'Suggest a reason why the student measured the time for 25 oscillations instead of just',
         'one oscillation.'), 3, stem=Q2S[:1]),
    T('2iia', 'Q2(ii)(a)', 'A', [Q(3, 'Describe, with the aid of a labelled diagram, how'),
                                 Q(3, 'the pendulum was set up so that it swung freely about a fixed point,')],
      [pt(S('split cork'), 3)], 'phys-1-5', 'pendulum-fixed-point',
      SQ(7, 'the pendulum was set up so that it swung freely about a fixed point,'), 3, stem=Q2S[:1]),
    T('2iib', 'Q2(ii)(b)', 'A', [Q(3, 'Describe, with the aid of a labelled diagram, how'),
                                 Q(3, 'the student determined the length of the pendulum.')],
      [pt(S('measure distance from fixed point to'), 3), pt(S('centre of bob'), 3, note_sel=NOLABEL)],
      'phys-1-5', 'pendulum-length', SQ(7, 'the student determined the length of the pendulum.'), 6,
      stem=Q2S[:1],
      decision='The scheme prints one phrase over two lines and prices each line [3]: two rows as printed. Its '
               '"[–1 if no label present on diagram]" closes (ii) and is shown on the second.'),
    T('2iiia', 'Q2(iii)(a)', 'A', [Q(3, 'Explain why'), Q(3, 'the student used a small heavy bob,')],
      [pt(S('to reduce air resistance / to keep string taut'), 3)], 'phys-1-5', 'why-small-heavy-bob',
      SQ(7, 'the student used a small heavy bob,'), 3, stem=Q2S[:1]),
    T('2iiib', 'Q2(iii)(b)', 'A', [Q(3, 'Explain why'), Q(3, 'the student used a small angle.')],
      [pt(S('the equation works for small angles'), 3)], 'phys-1-5', 'why-small-angle',
      SQ(7, 'the student used a small angle.'), 3, stem=Q2S[:1]),
    T('2iva', 'Q2(iv)(a)', 'A', Q2IVA,
      [pt(S('calculations of T²'), 3, kind='criterion',
          note='The scheme prints the values of T² it expects (shown in the figure).'),
       crit(S('axes labelled'), 3), crit(S('points plotted'), 3), crit(S('line of best fit'), 3)],
      'phys-1-5', 'pendulum-graph',
      SQ(7, 'Draw a suitable graph to show the relationship between the period and the',
         'length of the simple pendulum.'), 12, stem=Q2S, fig='q2iv-scheme-table'),
    T('2ivb', 'Q2(iv)(b)', 'A', Q(3, 'State this relationship.'),
      [pt(S('T² is proportional to l'), 3)], 'phys-1-5', 'period-length-relationship',
      SQ(7, 'State this relationship.'), 3, stem=Q2S[:1] + [M('(a)', 3), Q2IVA]),
    T('2v', 'Q2(v)', 'A', Q(3, 'Use your graph to calculate the acceleration due to gravity, g.'),
      [pt(S('slope formula'), 5, kind='criterion',
          note='The scheme prices [3 + 2] across this line and the formula for the period it prints under it '
               '(shown in the figure; the root sign does not survive in the text layer).'),
       pt(S('g ≈ 9.88 m s⁻²'), 2)],
      'phys-1-5', 'g-from-pendulum-graph',
      SQ(7, 'Use your graph to calculate the acceleration due to gravity, g.'), 7, stem=Q2S, fig='q2v-scheme-formula',
      decision='The scheme prints "slope formula", then the formula T = 2π√(l/g) as a stacked fraction under a '
               'root sign the text layer reads as a Sinhala letter, with one cell [3 + 2] for the two: one row in '
               'the scheme\'s own words at the cell\'s 5, the formula shown as a crop of the scheme.'),
    # ---- Q3 diffraction grating ----------------------------------------------
    T('3ia', 'Q3(i)(a)', 'A', Q(4, 'Draw a labelled diagram to show how the apparatus was arranged in this experiment.'),
      [pt(S('spectrometer / screen'), 3), pt(S('light source'), 3), pt(S('diffraction grating'), 3, note_sel=NOLABEL)],
      'phys-2-6', 'diffraction-grating-apparatus',
      SQ(8, 'Draw a labelled diagram to show how the apparatus was arranged in this', 'experiment.'), 9,
      stem=Q3S[:1]),
    T('3ib', 'Q3(i)(b)', 'A', Q(4, 'Describe the method the student used to obtain the data.'),
      [pt(dslash('rotate telescope to locate image on RHS of zero', 'grating to screen', 1), 2),
       pt(dslash('rotate telescope to locate image on LHS of zero', 'central image to other images', 1), 2),
       pt(dslash('reference to reading on circular scale', None, 1), 2)],
      'phys-2-6', 'diffraction-grating-method',
      SQ(8, 'Describe the method the student used to obtain the data.'), 6, stem=Q3S,
      decision='Each line prints two answers separated by "//", a spectrometer method and a screen method: '
               'answer variants, each on the scheme\'s own [2] per line.'),
    T('3ii', 'Q3(ii)', 'A', Q(4, 'State one precaution the student should take when carrying out the experiment.'),
      [pt(S('diffraction grating perpendicular to incident light', 'avoid parallax'), 3)], 'phys-2-6',
      'diffraction-grating-precaution',
      SQ(8, 'State one precaution the student should take when carrying out the experiment.'), 3, stem=Q3S[:1]),
    T('3iii', 'Q3(iii)', 'A', Q(4, 'Use all of the data to calculate an average value for the wavelength of the light.'),
      [pt(S('nλ = d Sinθ'), 3), pt(S('d = 2.5 × 10⁻⁶ m'), 3), crit(S('any one calculation of λ'), 3),
       pt(S('average λ = 593 nm'), 3)],
      'phys-2-6', 'wavelength-from-grating-data',
      SQ(8, 'Use all of the data to calculate an average value for the wavelength of the light.'), 12, stem=Q3S),
    T('3iva', 'Q3(iv)(a)', 'A', [Q3IV, Q(4, 'A light source with a shorter wavelength is used.', br=True)],
      [pt(S('images closer together'), 3)], 'phys-2-6', 'grating-shorter-wavelength',
      SQ(8, 'A light source with a shorter wavelength is used.'), 3, stem=Q3S[:1]),
    T('3ivb', 'Q3(iv)(b)', 'A', [Q3IV, Q(4, 'A diffraction grating with fewer lines per mm is used.', br=True)],
      [pt(S('images closer together'), 3)], 'phys-2-6', 'grating-fewer-lines',
      SQ(8, 'A diffraction grating with fewer lines per mm is used.'), 3, stem=Q3S[:1]),
    T('3v', 'Q3(v)', 'A', Q(4, 'Describe the pattern produced if a narrow beam of white light is used instead of the',
                            'monochromatic light.'),
      [pt(S('coloured fringes at the orders / white light at the zero order'), 4)], 'phys-2-6',
      'grating-white-light-pattern',
      SQ(8, 'Describe the pattern produced if a narrow beam of white light is used instead of the',
         'monochromatic light.'), 4, stem=Q3S[:1]),
    # ---- Q4 latent heat of vaporisation ----------------------------------------
    T('4i', 'Q4(i)', 'A', Q(5, 'Draw a labelled diagram of the apparatus used in the experiment.'),
      [pt(S('calorimeter with water'), 3), pt(S('steam generator'), 3),
       pt(S('point of detail e.g. steam trap / thermometer / lagging'), 3, note_sel=NOLABEL)],
      'phys-2-1', 'latent-heat-apparatus',
      SQ(9, 'Draw a labelled diagram of the apparatus used in the experiment.'), 9, stem=Q4S[:1]),
    T('4ii', 'Q4(ii)', 'A', Q(5, 'Why is it important to use dry steam in this experiment?'),
      [pt(S('only steam added / no water added'), 3)], 'phys-2-1', 'why-dry-steam',
      SQ(9, 'Why is it important to use dry steam in this experiment?'), 3, stem=Q4S[:1]),
    T('4iii', 'Q4(iii)', 'A', Q(5, 'How was the steam dried?'),
      [pt(S('steam trap / delivery tube sloped up / insulated delivery tube'), 3)], 'phys-2-1', 'drying-steam',
      SQ(9, 'How was the steam dried?'), 3, stem=Q4S[:1]),
    T('4iv', 'Q4(iv)', 'A', Q(5, 'Suggest a reason why the water in the calorimeter was initially cooled below room',
                              'temperature.'),
      [pt(S('heat gained = heat lost / a larger mass of steam could be used'), 3)], 'phys-2-1',
      'why-cool-water-below-room-temperature',
      SQ(9, 'Suggest a reason why the water in the calorimeter was initially cooled below room', 'temperature.'), 3,
      stem=Q4S[:1]),
    T('4v', 'Q4(v)', 'A', Q(5, 'Why is the rise in temperature the least accurate value?'),
      [pt(S('read to only one significant figure / temperature in the water may not be uniform'), 3)], 'phys-2-1',
      'temperature-rise-least-accurate',
      SQ(9, 'Why is the rise in temperature the least accurate value?'), 3, stem=Q4S),
    T('4via', 'Q4(vi)(a)', 'A', [Q4VI, Q(5, 'the energy gained by the calorimeter,')],
      [pt(S('mcΔθ'), 3), pt(S('198.97 J'), 3)], 'phys-2-1', 'energy-gained-by-calorimeter',
      SQ(9, 'the energy gained by the calorimeter,'), 6, stem=Q4S + [Q4DATA]),
    T('4vib', 'Q4(vi)(b)', 'A', [Q4VI, Q(5, 'the mass of steam used,')],
      [pt(S('0.0011 (kg)'), 3)], 'phys-2-1', 'mass-of-steam',
      SQ(9, 'the mass of steam used,'), 3, stem=Q4S),
    T('4vic', 'Q4(vi)(c)', 'A', [Q4VI, Q(5, 'the specific latent heat of vaporisation of water.')],
      pieces(S('mwater = 0.0801 (kg), Δθ = 79 (K), Δθ = 8 (K)'), [1, 1, 1], ',')
      + [pt(S('use of ml (& mcΔθ)'), 3), pt(S('l = 2.29 × 10⁶ J kg⁻¹'), 4)],
      'phys-2-1', 'specific-latent-heat-of-vaporisation',
      SQ(9, 'the specific latent heat of vaporisation of water.'), 10, stem=Q4S + [Q4DATA],
      decision='The scheme prints three values on one line priced [3 × 1]: one row each at 1.'),
    # ---- Q5 resistance and temperature -----------------------------------------
    T('5i', 'Q5(i)', 'A', Q(6, 'Draw a labelled diagram to show how the apparatus was arranged in this experiment.'),
      [pt(S('connected conductor in liquid'), 3), pt(S('thermometer'), 3), pt(S('ohmmeter'), 3, note_sel=NOLABEL)],
      'phys-3-3', 'resistance-temperature-apparatus',
      SQ(10, 'Draw a labelled diagram to show how the apparatus was arranged in this experiment.'), 9, stem=Q5S[:1]),
    T('5ii', 'Q5(ii)', 'A', Q(6, 'Draw a suitable graph to show the variation of R with θ.'),
      [crit(S('axes labelled'), 3), crit(S('points plotted'), 3), crit(S('line of best fit'), 3)],
      'phys-3-3', 'resistance-temperature-graph',
      SQ(10, 'Draw a suitable graph to show the variation of R with θ.'), 9, stem=Q5S),
    T('5iii', 'Q5(iii)', 'A', Q5III,
      [pt(S('≈ 31.3 × 10⁻³ (Ω)'), 3)], 'phys-3-3', 'resistance-at-25-degrees',
      SQ(10, 'Use your graph to determine the resistance of the wire when its temperature is 25 °C.'), 3, stem=Q5S),
    T('5iv', 'Q5(iv)', 'A', Q(6, 'Describe how the student measured the diameter of the wire.'),
      [pt(S('micrometer / digital calipers'), 3), pt(S('place wire between jaws and take readings'), 3)],
      'phys-3-3', 'measuring-wire-diameter',
      SQ(10, 'Describe how the student measured the diameter of the wire.'), 6, stem=Q5S[:1] + [Q5B]),
    T('5v', 'Q5(v)', 'A', Q(6, 'State one experimental precaution that should be taken when determining the length of the',
                            'wire.'),
      [pt(S('wire taut / no kinks / inside clips / constant temperature / no parallax'), 3)], 'phys-3-3',
      'precaution-measuring-wire-length',
      SQ(10, 'State one experimental precaution that should be taken when determining the length', 'of the wire.'),
      3, stem=Q5S[:1] + [Q5B]),
    T('5vi', 'Q5(vi)', 'A', Q(6, 'Calculate the resistivity of the wire at 25 °C.'),
      [G('fraction', page=10, clip=(95, 550, 200, 580), expect='ρ = RA/l', marks=3),
       pt(S('A = 1.96 × 10⁻⁷ (m²)'), 3), pt(S('ρ = 1.66 × 10⁻⁸ Ω m'), 4)],
      'phys-3-3', 'resistivity-of-wire',
      SQ(10, 'Calculate the resistivity of the wire at 25 °C.'), 10, stem=Q5S + [M('(iii)', 6), Q5III, Q5B]),
    # ============================================================ Section B ==
    # ---- Q6 short questions: best eight of twelve at 7 --------------------------
    T('6a', 'Q6(a)', 'B', Q(7, 'Draw a vector diagram to explain what is meant by friction.'),
      [anyn(None, 3, 3, steps=[3, 2, 2], note=ORDERED.format(cell='[3 + 2 + 2]'),
            options=[S('two surfaces shown'), S('direction of motion / applied force'),
                     S('frictional force opposing motion / frictional force opposing applied force')])],
      'phys-1-2', 'friction-vector-diagram', SQ(11, 'Draw a vector diagram to explain what is meant by friction.'), 7),
    T('6b', 'Q6(b)', 'B', [Q(7, 'The diagram shows weights hanging from a uniform wooden plank at given distances. The',
                             'centre of gravity of the plank. Calculate the mass of the plank.'),
                           Q(7, 'acceleration due to gravity = 9.8 m s⁻²', br=True)],
      [pt(S('M = F d', '840 + 0.3W = 900'), 3), pt(S('W = 200 (N)'), 2), pt(S('m = 20.4 kg'), 2)],
      'phys-1-2', 'mass-of-plank-from-moments',
      SQ(11, 'The diagram shows weights hanging from a uniform', 'of the plank. Calculate the mass of the plank.'), 7,
      fig='q6b-plank'),
    T('6c', 'Q6(c)', 'B', Q(7, 'Describe an experiment to demonstrate Archimedes’ principle.'),
      [pt(S('apparatus: overflow can, beaker, water, (newton) balance'), 3),
       pt(S('method: measure weight in air, measure weight in water'), 2),
       pt(S('result: (apparent) loss in weight = weight of displaced water'), 2)],
      'phys-1-2', 'archimedes-principle-experiment',
      SQ(11, 'Describe an experiment to demonstrate Archimedes’ principle.'), 7),
    T('6d', 'Q6(d)', 'B', Q(7, 'The motion of a body undergoing simple harmonic motion is described by the equation',
                            'a = –π²s. Calculate the period of its motion.'),
      [pt(S('a = (–)ω²s'), 3), pt(S('T = 2π/ω'), 2), pt(S('T = 2 s'), 2)],
      'phys-1-5', 'period-of-shm',
      SQ(11, 'The motion of a body undergoing simple harmonic motion is described by the',
         'equation a = –π²s. Calculate the period of its motion.'), 7),
    T('6e', 'Q6(e)', 'B', Q(7, 'Distinguish between heat and temperature.',
                            'Your answer should reference a distinguishing characteristic of each.'),
      [anyn(None, 2, 4, steps=[4, 3], note=ORDERED.format(cell='[4 + 3]'),
            options=[S('heat is a form of energy / joule'), S('temperature is a degree of hotness / kelvin')])],
      'phys-2-1', 'heat-and-temperature',
      SQ(11, 'Distinguish between heat and temperature.',
         'Your answer should reference a distinguishing characteristic of each.'), 7),
    T('6f', 'Q6(f)', 'B', [Q(7, '66 000 m³ of water goes over the Victoria Falls every minute.',
                             'Calculate the power generated by the water.'),
                           Q(7, 'acceleration due to gravity = 9.8 m s⁻²;', 'density of water = 1.0 × 10³ kg m⁻³', br=True)],
      [pt(S('m = ρV'), 3), pt(S('E = mgh'), 2), pt(S('P = 1.16 × 10⁹ W'), 2)],
      'phys-1-4', 'power-of-waterfall',
      SQ(11, '66 000 m³ of water goes over the Victoria Falls every minute.',
         'Calculate the power generated by the water.'), 7),
    T('6g', 'Q6(g)', 'B', Q(7, 'Explain why a strong magnet falling through a copper tube falls',
                            'falling through the same copper tube.'),
      [anyn(None, 2, 4, steps=[4, 3], note='The scheme prints "any two lines [4 + 3]".',
            options=[S('changing magnetic flux'), S('induces emf/current'), S('opposes the falling magnet')])],
      'phys-3-6', 'magnet-falling-through-copper-tube',
      SQ(12, 'Explain why a strong magnet falling through a copper tube falls more slowly than a',
         'similar-sized piece of non-magnetised steel falling through the same copper tube.'), 7),
    T('6h', 'Q6(h)', 'B', Q(8, 'Calculate the effective resistance of the arrangement of the resistors shown below.'),
      [pt(S('series formula', 'parallel formula'), 3), pt(S('parallel resistance = 19.6 Ω'), 2),
       pt(S('effective resistance = 27.6 Ω'), 2)],
      'phys-3-3', 'effective-resistance-network',
      SQ(12, 'Calculate the effective resistance of the arrangement of the resistors shown below.'), 7,
      fig='q6h-resistors'),
    T('6i', 'Q6(i)', 'B', Q(8, 'State three factors that affect the amount of heat produced in a current-carrying conductor.'),
      [anyn(None, 3, 3, steps=[3, 2, 2], note=ORDERED.format(cell='[3 + 2 + 2]'),
            options=[S('resistance, current(squared), time', piece=i, psep=',') for i in (1, 2, 3)])],
      'phys-3-3', 'heat-produced-in-conductor',
      SQ(12, 'State three factors that affect the amount of heat produced in a current-carrying', 'conductor.'), 7),
    T('6j', 'Q6(j)', 'B', [Q(8, 'Carbon–12 (C–12) which is necessary for life on Earth', 'nuclear equation.'),
                           Q(8, 'alpha particle mass = 6.644656 × 10⁻²⁷ kg; C–12 nucleus mass = 1.992101 × 10⁻²⁶ kg',
                             br=True),
                           Q(8, 'Calculate the energy released in this reaction.', br=True)],
      [pt(S('mass defect = 1.295 × 10⁻²⁹ (kg)'), 3), pt(S('E = mc²'), 2), pt(S('E = 1.166 × 10⁻¹² J'), 2)],
      'phys-4-5', 'energy-released-triple-alpha',
      SQ(12, 'Carbon–12 (C–12) which is necessary for life on Earth can be formed from alpha',
         'this simplified nuclear equation.'), 7, fig='q6j-equation',
      decision='The paper sets the nuclear equation with stacked mass and atomic numbers the text layer cannot '
               'order; it is shown as a crop of the printed line.'),
    T('6k', 'Q6(k)', 'B', Q(8, 'The energy of a photon of light is 3.75 × 10⁻¹⁹ J. Calculate the wavelength of the light.'),
      [pt(S('E = hf'), 3), pt(S('c = fλ'), 2), pt(S('λ = 5.3 × 10⁻⁷ m'), 2)],
      'phys-2-4', 'wavelength-of-photon',
      SQ(12, 'The energy of a photon of light is 3.75 × 10⁻¹⁹ J. Calculate the wavelength of the light.'), 7),
    T('6li', 'Q6(l)(i)', 'B', Q(8, 'State two reasons why it is difficult to detect a neutrino.'),
      [anyn(None, 2, 4, steps=[4, 3], note=ORDERED.format(cell='[4 + 3]'),
            options=[S('negligible mass'), S('no charge')])],
      'phys-4-4', 'detecting-neutrinos', SQ(12, 'State two reasons why it is difficult to detect a neutrino.'), 7,
      decision='Q6(l) prints "(i) ... or (ii) ...": each alternative is carded at the part\'s 7.'),
    T('6lii', 'Q6(l)(ii)', 'B', Q(8, 'State two factors that affect the efficiency of a transformer.'),
      [anyn(None, 2, 4, steps=[4, 3], open_list=True, note_sel=S('etc.'), note='— the scheme ends its list so: the list is open.',
            options=[S('resistance of the wires', 'currents in the core,', piece=i, psep=',') for i in (1, 2, 3)])],
      'phys-3-6', 'transformer-efficiency-factors',
      SQ(12, 'State two factors that affect the efficiency of a transformer.'), 7),
    # ---- Q7 momentum, pile driver, sound -------------------------------------
    T('7ia', 'Q7(i)(a)', 'B', [Q(9, 'Explain what is meant by'), Q(9, 'momentum,')],
      [pt(S('momentum = mass × velocity / p = mv with notation'), 4)], 'phys-1-2', 'momentum-definition',
      SQ(13, 'momentum,'), 4),
    T('7ib', 'Q7(i)(b)', 'B', [Q(9, 'Explain what is meant by'), Q(9, 'force.')],
      [pt(S('force causes acceleration / force causes change in velocity'), 4)], 'phys-1-2', 'force-definition',
      SQ(13, 'force.'), 4),
    T('7ii', 'Q7(ii)', 'B', Q(9, 'Use Newton’s second law of motion to derive the relationship between force, mass and',
                              'acceleration.'),
      [pt(S('force is proportional to rate of change of momentum'), 3),
       pt(S('force is proportional to mass × acceleration'), 3), pt(S('k = 1'), 2), pt(S('F = ma'), 3)],
      'phys-1-2', 'deriving-f-equals-ma',
      SQ(13, 'Use Newton’s second law of motion to derive the relationship between force, mass',
         'and acceleration.'), 11),
    T('7iii', 'Q7(iii)', 'B', Q(9, 'The steel block falls for 1.01 s before striking the steel rod. Calculate the distance that the',
                                'steel block has fallen.'),
      [pt(S('s = ut + ½ at²'), 3), pt(S('s = 4.998 m'), 3)], 'phys-1-1', 'distance-fallen-by-block',
      SQ(13, 'The steel block falls for 1.01 s before striking the steel rod. Calculate the distance that',
         'the steel block has fallen.'), 6, stem=[Q7S, Q7G]),
    T('7iv', 'Q7(iv)', 'B', Q(9, 'Calculate the upward velocity of the steel block immediately after the collision.'),
      [pt(S('v² = u² + 2as', '½ mv² =mgh'), 3), pt(S('v = 0.59 m s⁻¹'), 3)], 'phys-1-1',
      'rebound-velocity-of-block',
      SQ(13, 'Calculate the upward velocity of the steel block immediately after the collision.'), 6,
      stem=[Q7S, Q7SB, Q7G]),
    T('7v', 'Q7(v)', 'B', Q7V,
      [pt(S('p = mv or any reference to conservation of momentum or vbefore = 9.9 m s⁻¹'), 3),
       pt(S('(500 × 9.9) = (500 × –0.59) + (1500 × vafter)'), 3), pt(S('vafter = 3.5 m s⁻¹'), 3)],
      'phys-1-2', 'velocity-of-rod-after-collision',
      SQ(13, 'Calculate the downward velocity of the steel rod immediately after the collision.'), 9,
      stem=[Q7S, Q7SB, Q7G]),
    T('7vi', 'Q7(vi)', 'B', Q(9, 'The steel rod takes 2 ms to come to rest. Calculate the average force exerted by the ground',
                              'on the steel rod to bring it to rest.'),
      [pt(S('F = ma', 'v = u + at'), 3), pt(S('average force = 2.6 ×10⁶ N'), 3)], 'phys-1-2',
      'average-force-on-rod',
      SQ(13, 'The steel rod takes 2 ms to come to rest. Calculate the average force exerted by the',
         'ground on the steel rod to bring it to rest.'), 6, stem=[Q7S, Q7SB, M('(v)', 9), Q7V]),
    T('7viia', 'Q7(vii)(a)', 'B', [Q7VII, Q(9, 'the sound intensity measured,')],
      [pt(S('S.I. is proportional to 1/d²', 'sound intensity is reduced'), 4), pt(S('16 times less'), 2)],
      'phys-2-5', 'sound-intensity-at-4d', SQ(13, 'the sound intensity measured,'), 6, stem=[Q7SC]),
    T('7viib', 'Q7(vii)(b)', 'B', [Q7VII, Q(9, 'the sound intensity level measured.')],
      [pt(S('reference to 3 dB', 'sound intensity level reduced'), 2), pt(S('(–) 12 dB'), 2)],
      'phys-2-5', 'sound-intensity-level-at-4d', SQ(13, 'the sound intensity level measured.'), 4, stem=[Q7SC]),
    # ---- Q8 reflection and refraction ------------------------------------------
    T('8i', 'Q8(i)', 'B', Q(10, 'Explain what is meant by reflection of light.'),
      [pt(S('bouncing back of light from a surface'), 3)], 'phys-2-3', 'reflection-definition',
      SQ(14, 'Explain what is meant by reflection of light.'), 3),
    T('8ii', 'Q8(ii)', 'B', Q(10, 'An object is placed in front of a concave mirror which has a focal length of 20 cm. An image',
                              'Calculate the position of the object.'),
      [pt(S('1/u + 1/v = 1/f'), 3), pt(S('m = v/u'), 3), pt(S('position = 60 cm'), 3)], 'phys-2-3',
      'concave-mirror-object-position',
      SQ(14, 'An object is placed in front of a concave mirror which has a focal length of 20 cm. An',
         'Calculate the position of the object.'), 9),
    T('8iii', 'Q8(iii)', 'B', Q(10, 'Suggest a reason why a dentist may choose a concave mirror over a convex mirror when',
                                'examining teeth.'),
      [pt(S('concave mirror magnifies'), 3)], 'phys-2-3', 'dentist-concave-mirror',
      SQ(14, 'Suggest a reason why a dentist may choose a concave mirror over a convex mirror',
         'when examining teeth.'), 3),
    T('8iv', 'Q8(iv)', 'B', Q(10, 'Draw a ray diagram to show how a virtual image can be formed by a converging lens.'),
      [pt(S('object (inside focus)'), 3), crit(S('two correct rays drawn'), 3), crit(S('position of virtual image'), 3)],
      'phys-2-3', 'virtual-image-converging-lens-ray-diagram',
      SQ(14, 'Draw a ray diagram to show how a virtual image can be formed by a converging lens.'), 9, stem=[Q8L]),
    T('8v', 'Q8(v)', 'B', Q(10, 'Explain why the region on the surface of the water surrounding the circular disc of light',
                            'remains dark.'),
      [pt(S('total internal reflection occurs / critical angle has been exceeded'), 3)], 'phys-2-3',
      'dark-region-around-disc',
      SQ(14, 'Explain why the region on the surface of the water surrounding the circular disc of',
         'light remains dark.'), 3, stem=[Q8SB]),
    T('8vi', 'Q8(vi)', 'B', Q(10, 'The diameter of the circular disc is 1.14 m. Calculate the refractive index of the water.'),
      [pt(S('C = 48.74°'), 3), G('fraction', page=14, clip=(95, 526, 200, 554), expect='n = 1/(sin C)', marks=6),
       pt(S('n = 1.33'), 3)],
      'phys-2-3', 'refractive-index-from-disc',
      SQ(14, 'The diameter of the circular disc is 1.14 m. Calculate the refractive index of the water.'), 12,
      stem=[Q8SB]),
    T('8vii', 'Q8(vii)', 'B', Q(10, 'Using a labelled diagram explain why the underwater lamp does not appear to be at a depth',
                                'of 0.5 m when viewed by an observer outside the pool.'),
      [anyn(S('light refracted as it goes from water to air', 'image closer to the surface'), 2, 4, note_sel=NOLABEL)],
      'phys-2-3', 'apparent-depth-of-lamp',
      SQ(14, 'Using a labelled diagram explain why the underwater lamp does not appear to be at a',
         'depth of 0.5 m when viewed by an observer outside the pool.'), 8, stem=[Q8SB]),
    T('8viii', 'Q8(viii)', 'B', Q(10, 'Describe an experiment to demonstrate that light waves are transverse waves.'),
      [pt(S('apparatus: two pieces of polaroid and a light source'), 3),
       pt(S('method: rotate one piece of polaroid relative to the other'), 3),
       pt(S('observation: the light intensity decreases'), 3)],
      'phys-2-7', 'polarisation-experiment',
      SQ(14, 'Describe an experiment to demonstrate that light waves are transverse waves.'), 9, stem=[Q8T]),
    # ---- Q9 resonance, strings and pipes --------------------------------------
    T('9i', 'Q9(i)', 'B', Q(11, 'Explain what is meant by resonance.'),
      [pt(S('transfer of energy (between two systems)'), 3), pt(S('of the same (natural) frequencies'), 3)],
      'phys-2-5', 'resonance-definition', SQ(15, 'Explain what is meant by resonance.'), 6, stem=[Q9S]),
    T('9ii', 'Q9(ii)', 'B', Q(11, 'Describe an experiment to demonstrate resonance.'),
      [crit(S('apparatus'), 3), crit(S('method'), 3), crit(S('result'), 3)],
      'phys-2-5', 'resonance-experiment', SQ(15, 'Describe an experiment to demonstrate resonance.'), 9),
    T('9iiia', 'Q9(iii)(a)', 'B', Q9IIIA,
      pieces(S('length, mass per unit length'), [3, 3], ','), 'phys-2-6', 'factors-fundamental-frequency-string',
      SQ(15, 'Name these two factors.'), 6, stem=[Q9SB]),
    T('9iiib', 'Q9(iii)(b)', 'B', Q(11, 'State the relationship between the fundamental frequency and each of these two',
                                    'factors.'),
      pieces(S('inverse length, inverse of square root of mass per unit length'), [3, 3], ','), 'phys-2-6',
      'fundamental-frequency-relationships',
      SQ(15, 'State the relationship between the fundamental frequency and each of these', 'two factors.'), 6,
      stem=[Q9SB, M('(a)', 11), Q9IIIA]),
    T('9iv', 'Q9(iv)', 'B', Q(11, 'A violin string is initially tuned to a fundamental frequency of 250 Hz under a tension of 10 N.',
                              'the tension is the only factor being changed.'),
      [pt(S('f∝√T'), 3), pt(S('T = 22.5 N'), 3)], 'phys-2-6', 'new-tension-violin-string',
      SQ(15, 'A violin string is initially tuned to a fundamental frequency of 250 Hz under a tension',
         '375 Hz assuming the tension is the only factor being changed.'), 6),
    T('9v', 'Q9(v)', 'B', Q(11, 'State one condition necessary for a stationary wave to form on a stretched string.'),
      [pt(S('whole number of half wavelengths / constructive interference / two waves of the',
            'same frequency travelling in opposite directions meet'), 4)], 'phys-2-6', 'stationary-wave-condition',
      SQ(15, 'State one condition necessary for a stationary wave to form on a stretched string.'), 4),
    T('9vi', 'Q9(vi)', 'B', Q(11, 'Draw a labelled diagram to show the standing wave formed in a pipe that is open at one end',
                              'and closed at the other end when it is vibrating at its third harmonic.'),
      [pt(S('antinode at open end'), 3), pt(S('node at closed end'), 3), crit(S('correct shape'), 3, note_sel=NOLABEL)],
      'phys-2-6', 'third-harmonic-closed-pipe',
      SQ(15, 'Draw a labelled diagram to show the standing wave formed in a pipe that is open at',
         'one end and closed at the other end when it is vibrating at its third harmonic.'), 9, stem=[Q9SC]),
    T('9vii', 'Q9(vii)', 'B', Q(11, 'A pipe that is open at both ends has a length of 2.3 m and it generates a particular',
                                'Calculate the length of the second pipe.'),
      [pt(S('c = f λ'), 3), pt(S('l = 1.15 m'), 3)], 'phys-2-6', 'length-of-closed-pipe',
      SQ(15, 'A pipe that is open at both ends has a length of 2.3 m and it generates a particular',
         'Calculate the length of the second pipe.'), 6, stem=[Q9SC]),
    T('9viii', 'Q9(viii)', 'B', Q(11, 'Suggest a reason why the same musical note can have a different quality when played on',
                                  'different instruments.'),
      [pt(S('overtones / harmonics'), 4)], 'phys-2-5', 'quality-of-a-note',
      SQ(15, 'Suggest a reason why the same musical note can have a different quality when played',
         'on different instruments.'), 4),
    # ---- Q10 capacitors ---------------------------------------------------------
    T('10ia', 'Q10(i)(a)', 'B', [Q10I, Q(12, 'capacitance,')],
      [pt(dslash('charge', '// C = Q/V', 1), 3), pt(dslash('per unit voltage', '// notation', 1), 3)],
      'phys-3-2', 'capacitance-definition', SQ(16, 'capacitance,'), 6, stem=[Q10S],
      decision='The scheme sets the definition in words and, after "//", as a formula with notation: answer '
               'variants, each on the scheme\'s own [3] per line.'),
    T('10ib', 'Q10(i)(b)', 'B', [Q10I, Q(12, 'potential difference.')],
      [pt(dslash('work', '// V = W/q', 1), 3), pt(dslash('per unit charge', '// notation', 1), 3)],
      'phys-3-2', 'potential-difference-definition', SQ(16, 'potential difference.'), 6, stem=[Q10S],
      decision='Words, or after "//" a formula with notation: answer variants, as (a).'),
    T('10ii', 'Q10(ii)', 'B', Q(12, 'Describe the movement of electrons when an uncharged parallel-plate capacitor is',
                                'connected to a battery.'),
      [pt(S('electrons move away from negative terminal / electrons move towards positive', 'terminal'), 5)],
      'phys-3-2', 'electrons-charging-capacitor',
      SQ(16, 'Describe the movement of electrons when an uncharged parallel-plate capacitor is',
         'connected to a battery.'), 5, stem=[Q10S]),
    T('10iii', 'Q10(iii)', 'B', Q(12, 'Describe a demonstration to show that a charged capacitor can store energy.'),
      [crit(S('apparatus'), 3), crit(S('method'), 3), crit(S('result'), 3)],
      'phys-3-2', 'capacitor-stores-energy-demonstration',
      SQ(16, 'Describe a demonstration to show that a charged capacitor can store energy.'), 9),
    T('10iv', 'Q10(iv)', 'B', Q(12, 'Draw a suitable graph on graph paper to show the relationship between the C and d.'),
      [pt(S('calculated 1/d values'), 3, kind='criterion',
          note='The scheme prints the values of 1/d it expects (shown in the figure).'),
       crit(S('labelled axes and points plotted'), 3), crit(S('line of best fit'), 3)],
      'phys-3-2', 'capacitance-against-1-over-d-graph',
      SQ(16, 'Draw a suitable graph on graph paper to show the relationship between the C and d.'), 9,
      stem=[Q10SB, Q10TAB], fig='q10iv-scheme-table'),
    T('10v', 'Q10(v)', 'B', Q(12, 'Calculate the slope of the graph and use it to calculate A.'),
      [pt(S('slope formula'), 3), G('fraction', page=16, clip=(95, 553, 200, 581), expect='C = εA/d', marks=3),
       pt(S('A ≈ 2.3 ×10⁻² m²'), 3)],
      'phys-3-2', 'plate-area-from-slope',
      SQ(16, 'Calculate the slope of the graph and use it to calculate A.'), 9, stem=[Q10SB, Q10TAB],
      fig='q10iv-scheme-table',
      decision='"the graph" is the student\'s own, from (iv); the card carries the scheme\'s 1/d values it is drawn from.'),
    T('10via', 'Q10(vi)(a)', 'B', [Q10VI, Q10VIA],
      [pt(S('V = IR / 5.2 V'), 3), pt(S('V = 6.8 V'), 3)], 'phys-3-3', 'pd-across-capacitor-while-charging',
      SQ(16, 'the potential difference across the capacitor at that moment,'), 6, stem=[Q10SC], fig='q10-circuit'),
    T('10vib', 'Q10(vi)(b)', 'B', [Q10VI, Q(12, 'the energy stored in the capacitor at that moment.')],
      [pt(S('E = ½ CV²'), 3), pt(S('E = 4.6 × 10⁻³ J'), 3)], 'phys-3-2', 'energy-stored-in-capacitor',
      SQ(16, 'the energy stored in the capacitor at that moment.'), 6, stem=[Q10SC, M('(a)', 12), Q10VIA],
      fig='q10-circuit'),
    # ---- Q11 the electron ------------------------------------------------------
    T('11i', 'Q11(i)', 'B', Q(13, 'State two properties of an electron.'),
      [anyn(S('mass of 9.1×10⁻³¹ kg', 'fundamental particle'), 2, 4, steps=[4, 2], sep=',')],
      'phys-4-1', 'properties-of-electron', SQ(17, 'State two properties of an electron.'), 6),
    T('11ii', 'Q11(ii)', 'B', Q(13, 'For a cathode ray tube, describe', 'where the electrons are given a linear acceleration.'),
      [pt(S('cathode is heated / thermionic emission'), 4,
          label=S('(a)', after='where the electrons are given a linear acceleration.')),
       pt(S('between the cathode and the anode'), 2, label=S('(b)', after='cathode is heated / thermionic emission'))],
      'phys-4-1', 'cathode-ray-tube-beam', SQ(17, 'For a cathode ray tube, describe'), 6,
      decision='The scheme prices (a) and (b) in one cell [4 + 2] on (b)\'s line: one card for (ii), each '
               'answer its own row.'),
    T('11iiia', 'Q11(iii)(a)', 'B', [Q11III, Q(13, 'a yellow colour,')],
      pieces(S('red + green'), [2, 2], '+'), 'phys-2-4', 'yellow-from-primary-colours',
      SQ(17, 'a yellow colour,'), 4, stem=[Q11SA]),
    T('11iiib', 'Q11(iii)(b)', 'B', [Q11III, Q(13, 'a white colour.')],
      pieces(S('red + green + blue'), [2, 2, 2], '+'), 'phys-2-4', 'white-from-primary-colours',
      SQ(17, 'a white colour.'), 6, stem=[Q11SA]),
    T('11iv', 'Q11(iv)', 'B', Q(13, 'Derive the formula F = qvB for the force F acting on a particle with charge q moving with a',
                                'velocity v perpendicular to a magnetic field of magnetic flux density B.'),
      [pt(S('F = BIl'), 3), pt(S('I = q/t'), 3), pt(S('v = l/t'), 3)], 'phys-3-5', 'deriving-f-equals-qvb',
      SQ(17, 'Derive the formula F = qvB for the force F acting on a particle with charge q moving',
         'with a velocity v perpendicular to a magnetic field of magnetic flux density B.'), 9),
    T('11v', 'Q11(v)', 'B', Q(13, 'Using Fleming\'s left-hand rule, or otherwise, determine the direction of the magnetic field.'),
      [pt(S('into the page'), 3)], 'phys-3-5', 'direction-of-magnetic-field',
      SQ(17, 'Using Fleming\'s left-hand rule, or otherwise, determine the direction of the magnetic', 'field.'), 3,
      stem=[Q11SB], fig='q11-path'),
    T('11vi', 'Q11(vi)', 'B', Q(13, 'Calculate the voltage in the tube.'),
      [pt(S('Eₖ = ½ mv²'), 3), pt(S('W = qV'), 3), pt(S('V = 2011 V'), 3)], 'phys-4-1', 'voltage-in-crt',
      SQ(17, 'Calculate the voltage in the tube.'), 9, stem=[Q11SC]),
    T('11vii', 'Q11(vii)', 'B', Q(13, 'Calculate the force on the electron due to the magnetic field.'),
      [pt(S('F = qvB'), 2), pt(S('8.5 ×10⁻¹⁵ N'), 2)], 'phys-3-5', 'force-on-electron-in-field',
      SQ(17, 'Calculate the force on the electron due to the magnetic field.'), 4, stem=[Q11SD]),
    T('11viii', 'Q11(viii)', 'B', Q(13, 'Calculate the radius of curvature of the circular path followed by the electron.'),
      [G('fraction', page=17, clip=(95, 686, 160, 716), expect='Fc = mv²/r', marks=6), pt(S('r = 7.6 × 10⁻² m'), 3)],
      'phys-3-5', 'radius-of-electron-path',
      SQ(17, 'Calculate the radius of curvature of the circular path followed by the electron.'), 9, stem=[Q11SD]),
    # ---- Q12 radioactivity ------------------------------------------------------
    T('12i', 'Q12(i)', 'B', Q(14, 'Explain what is meant by each type of nuclear radiation: alpha, beta, and gamma.'),
      pieces(S('alpha: helium nucleus; beta: (high speed) electron; gamma: photon'), [2, 2, 2], ';'),
      'phys-4-4', 'alpha-beta-gamma', SQ(18, 'Explain what is meant by each type of nuclear radiation: alpha, beta, and gamma.'),
      6, stem=[Q12S]),
    T('12iia', 'Q12(ii)(a)', 'B', [Q12II, Q(14, 'ionising ability,')],
      pieces(S('alpha: strong; beta: moderate; gamma: poor'), [2, 2, 2], ';'), 'phys-4-4', 'ionising-ability',
      SQ(18, 'ionising ability,'), 6),
    T('12iib', 'Q12(ii)(b)', 'B', [Q12II, Q(14, 'deflection in a magnetic field.')],
      pieces(S('alpha: yes; beta: yes; gamma: no'), [2, 2, 2], ';'), 'phys-4-4', 'deflection-in-magnetic-field',
      SQ(18, 'deflection in a magnetic field.'), 6),
    T('12iiia', 'Q12(iii)(a)', 'B', Q12IIIA,
      [pt(dslash('Geiger-Muller tube', '// solid state detector', 1), 2)], 'phys-4-4', 'radiation-detector',
      SQ(18, 'Name one type of detector used to detect nuclear radiation.'), 2,
      decision='"Geiger-Muller tube // solid state detector": two detectors, each with its own principle in (b): '
               'answer variants.'),
    T('12iiib', 'Q12(iii)(b)', 'B', Q(14, 'Describe the principle of operation of the detector.'),
      [pt(dslash('ionisation', '// free electrons produced', 1), 2), pt(dslash('current flows', '// current flows', 1), 2)],
      'phys-4-4', 'detector-principle', SQ(18, 'Describe the principle of operation of the detector.'), 4,
      stem=[M('(a)', 14), Q12IIIA],
      decision='The principle of the detector named in (a): answer variants, Geiger-Muller tube and solid state.'),
    T('12iv', 'Q12(iv)', 'B', Q(14, 'Calculate how many', 'beta particles are emitted.'),
      pieces(S('one alpha particle; two beta particles'), [3, 3], ';'), 'phys-4-4', 'alpha-beta-in-decay-series',
      SQ(18, 'Calculate how many'), 6, stem=[Q12SB],
      decision='The scheme answers (a) and (b) on one line with one cell [3 + 3]: one card for (iv).'),
    T('12v', 'Q12(v)', 'B', Q(14, 'Given that the energy needed to create one ion pair is 5.6 × 10⁻¹⁸ J, calculate the maximum',
                              'number of ion pairs that could be produced by the alpha particle due to its kinetic energy.'),
      [pt(S('262 500 ion pairs'), 3)], 'phys-4-4', 'number-of-ion-pairs',
      SQ(18, 'Given that the energy needed to create one ion pair is 5.6 × 10⁻¹⁸ J, calculate the', 'kinetic energy.'),
      3, stem=[Q12SC]),
    T('12via', 'Q12(vi)(a)', 'B', [Q12VI, Q(14, 'half-life,')],
      [pt(S('time for half a sample to decay'), 3)], 'phys-4-4', 'half-life-definition', SQ(18, 'half-life,'), 3),
    T('12vib', 'Q12(vi)(b)', 'B', [Q12VI, Q(14, 'the becquerel (Bq).')],
      [pt(S('one disintegration per second'), 3)], 'phys-4-4', 'becquerel-definition', SQ(18, 'the becquerel (Bq).'), 3),
    T('12vii', 'Q12(vii)', 'B', Q(14, 'Calculate the activity of a 3.0 mg sample of', 'polonium–210.'),
      [pt(S('number of nuclei in 3 mg = 8.57 ×10¹⁸'), 3), pt(S('A = λN'), 3), pt(S('4.98 × 10¹¹ Bq'), 3)],
      'phys-4-4', 'activity-of-polonium-sample', SQ(18, 'Calculate the activity of a 3.0 mg sample of polonium–210.'),
      9, stem=Q12SD),
    T('12viii', 'Q12(viii)', 'B', Q(14, 'Estimate by calculation how many nuclei of', '276 days.'),
      [G('fraction', page=18, clip=(95, 694, 200, 722), expect='T 1/2 = ln2/λ', marks=4),
       pt(S('T1/2 = 1.19 × 10⁷ s / 138 days'), 2), pt(S('2.14 × 10¹⁸ nuclei'), 2)],
      'phys-4-4', 'nuclei-remaining-after-276-days',
      SQ(18, 'Estimate by calculation how many nuclei of polonium–210 remain in the 3.0 mg', 'sample after 276 days.'),
      8, stem=Q12SD),
    # ---- Q13 home of 2030 (passage) -------------------------------------------
    T('13i', 'Q13(i)', 'B', Q(15, 'Silicon is classed as a semiconductor. Explain what is meant by a semiconductor.'),
      [pt(S('resistivity'), 4), pt(dslash('between that of a conductor and an insulator', None, 1), 3)],
      'phys-3-3', 'semiconductor-definition',
      SQ(19, 'Silicon is classed as a semiconductor. Explain what is meant by a semiconductor.'), 7,
      stem=[P13['solar']],
      decision='"between that of a conductor and an insulator // decreases with temperature": answer variants, '
               'each with "resistivity".'),
    T('13iia', 'Q13(ii)(a)', 'B', Q(15, 'What do the letters in the acronym LED stand for?'),
      pieces(S('light, emitting, diode'), [1, 1, 1], ','), 'phys-3-3', 'led-acronym',
      SQ(19, 'What do the letters in the acronym LED stand for?'), 3, stem=[P13['led'], Q13II]),
    T('13iib', 'Q13(ii)(b)', 'B', Q(15, 'Calculate how much energy is saved in one hour by using a 10 W LED bulb in place of a',
                                    '60 W filament bulb.'),
      [pt(S('difference in power usage = 50 (W)'), 2), pt(S('180 000 J'), 2)], 'phys-3-3', 'energy-saved-by-led',
      SQ(19, 'Calculate how much energy is saved in one hour by using a 10 W LED bulb in',
         'place of a 60 W filament bulb.'), 4, stem=[P13['led'], Q13II]),
    T('13iii', 'Q13(iii)', 'B', Q(15, 'Sketch voltage-time graphs for', 'the input from the national grid, which is used in our homes.'),
      [crit(S('label axes'), 3),
       pt(S('sketch d.c.'), 2, kind='criterion', note=CRIT, label=S('(a)', after='label axes')),
       pt(S('sketch a.c.'), 2, kind='criterion', note=CRIT, label=S('(b)', after='sketch d.c.'))],
      'phys-3-3', 'dc-and-ac-voltage-time-graphs', SQ(19, 'Sketch voltage-time graphs for'), 7,
      stem=[P13['solar'], P13['ev']],
      decision='One "label axes [3]" serves both sketches, so (a) and (b) are one card for (iii).'),
    T('13iva', 'Q13(iv)(a)', 'B', Q(15, 'Calculate how long would it take to give an electric car', '75 kWh using a 7.2 kW home charger.'),
      [pt(S('75 kWh = 270 MJ', '75/7.2'), 2), pt(S('37500 s = 10.4 hours'), 2)], 'phys-3-3', 'ev-charging-time',
      SQ(20, 'Calculate how long would it take to give an electric car 75 kWh using a 7.2 kW', 'home charger.'), 4,
      stem=[Q13IV]),
    T('13ivb', 'Q13(iv)(b)', 'B', Q(15, 'What type of energy conversion takes place when the car', 'powers the home?'),
      [pt(S('chemical to'), 2), pt(S('electrical'), 2)], 'phys-3-3', 'ev-energy-conversion',
      SQ(20, 'What type of energy conversion takes place when the car powers the home?'), 4,
      stem=[P13['ev'], Q13IV]),
    T('13ivc', 'Q13(iv)(c)', 'B', Q(15, 'Calculate the average current drawn if the V2G provides a peak AC voltage of 328 V to',
                                    'power a 2 kW electric kettle.'),
      [G('fraction', page=20, clip=(125, 302, 200, 330), expect='Vrmsൌ Vₚₑₐₖ/(√2)', marks=2),
       pt(S('P = VI'), 2), pt(S('I = 8.62 A'), 2)],
      'phys-3-3', 'average-current-from-peak-voltage',
      SQ(20, 'Calculate the average current drawn if the V2G provides a peak AC voltage of 328',
         'V to power a 2 kW electric kettle.'), 6, stem=[P13['ev'], Q13IV], fig='q13ivc-scheme-formula',
      decision='The scheme sets the r.m.s. formula as a stacked fraction whose "=" the text layer reads as a '
               'Malayalam sign (repaired by the bank\'s glyph map): read with G(\'fraction\') and shown as a crop.'),
    T('13v', 'Q13(v)', 'B', Q(15, 'A single solar panel covers an area of 0.9 m². The efficiency of the solar panel is 25%.',
                              'Calculate the maximum power generated by the solar panel in Ireland.'),
      [pt(S('power for the panel = 1076.4 W'), 4), pt(S('25% = 269.1 W'), 3)], 'phys-2-4', 'solar-panel-power',
      SQ(20, 'A single solar panel covers an area of 0.9 m². The efficiency of the solar panel is 25%.',
         'Calculate the maximum power generated by the solar panel in Ireland.'), 7, stem=[P13['solar']]),
    T('13vi', 'Q13(vi)', 'B', Q(15, 'State two desirable properties of a refrigerant fluid used in a heat pump.'),
      [anyn(None, 2, 4, steps=[4, 3], note=ORDERED.format(cell='[4 + 3]'),
            options=[S('low boiling point'), S('high latent heat of vaporisation')])],
      'phys-2-1', 'refrigerant-properties',
      SQ(20, 'State two desirable properties of a refrigerant fluid used in a heat pump.'), 7, stem=[P13['heat']]),
    T('13vii', 'Q13(vii)', 'B', Q(15, 'The temperature inside the home described is 21 °C and the temperature outside is 10 °C.',
                                  'Calculate the average rate of heat loss per square metre.'),
      [pt(S('Δθ = 11 °C'), 3), pt(S('1.1 W'), 4)], 'phys-2-1', 'heat-loss-per-square-metre',
      SQ(20, 'The temperature inside the home described is 21 °C and the temperature outside is 10',
         '°C. Calculate the average rate of heat loss per square metre.'), 7, stem=[P13['house']]),
    # ---- Q14 any two of (a)-(d) ------------------------------------------------
    T('14ai', 'Q14(a)(i)', 'B', Q(16, 'Explain what is meant by a vector quantity.'),
      [pt(S('magnitude'), 3), pt(S('direction'), 3)], 'phys-1-1', 'vector-quantity',
      SQ(21, 'Explain what is meant by a vector quantity.'), 6),
    T('14aii', 'Q14(a)(ii)', 'B', Q(16, 'Describe a laboratory experiment to find the resultant of two vectors.'),
      [pt(S('apparatus: three newton balances'), 3), pt(S('method: read each force when the system is at rest'), 3),
       pt(S('result: vector sum of two forces = third force'), 3)],
      'phys-1-2', 'resultant-of-two-vectors-experiment',
      SQ(21, 'Describe a laboratory experiment to find the resultant of two vectors.'), 9),
    T('14aiiia', 'Q14(a)(iii)(a)', 'B', Q(16, 'Resolve the velocity of the boat into parallel and perpendicular components relative to',
                                          'the water flow.'),
      [pt(S('parallel component = 2.349 m s⁻¹'), 3), pt(S('perpendicular component = 0.855 m s⁻¹'), 3)],
      'phys-1-1', 'resolving-boat-velocity',
      SQ(21, 'Resolve the velocity of the boat into parallel and perpendicular components',
         'relative to the water flow.'), 6, stem=[Q14SA], fig='q14a-boat'),
    T('14aiiib', 'Q14(a)(iii)(b)', 'B', Q(16, 'Calculate the magnitude and the direction of the resultant velocity of the boat.'),
      [pt(S('magnitude of v = 3.94 m s⁻¹'), 4), pt(S('angle = 12.5°'), 3)], 'phys-1-1', 'resultant-velocity-of-boat',
      SQ(21, 'Calculate the magnitude and the direction of the resultant velocity of the boat.'), 7, stem=[Q14SA],
      fig='q14a-boat'),
    T('14bia', 'Q14(b)(i)(a)', 'B', [Q14BI, Q(16, 'angular velocity,')],
      [pt(dslash('rate of change', '// ω = θ/t', 1), 3), pt(dslash('of angle', '// notation', 1), 3)],
      'phys-1-6', 'angular-velocity-definition', SQ(22, 'angular velocity,'), 6,
      decision='Words, or after "//" a formula with notation: answer variants, each on the scheme\'s own [3] per line.'),
    T('14bib', 'Q14(b)(i)(b)', 'B', [Q14BI, Q(16, 'frequency.')],
      [pt(S('number of cycles per second / f = 1/T with notation'), 3)], 'phys-1-6', 'frequency-definition',
      SQ(22, 'frequency.'), 3),
    T('14bii', 'Q14(b)(ii)', 'B', Q(16, 'State the name of this phenomenon.'),
      [pt(S('Doppler effect'), 4)], 'phys-2-7', 'doppler-effect', SQ(22, 'State the name of this phenomenon.'), 4,
      stem=[Q14SB]),
    T('14biiia', 'Q14(b)(iii)(a)', 'B', Q(16, 'Calculate the minimum frequency heard by a person standing some distance away.'),
      [pt(S('v = rω'), 3), pt(S('v = 31.2 (m s⁻¹)'), 3),
       G('fraction', page=22, clip=(125, 416, 200, 444), expect="f' = fc/(c±u)", marks=3),
       pt(S('fmin = 1008 Hz'), 3)],
      'phys-2-7', 'minimum-frequency-whistle',
      SQ(22, 'Calculate the minimum frequency heard by a person standing some distance', 'away.'), 12, stem=Q14SB2),
    T('14biiib', 'Q14(b)(iii)(b)', 'B', Q(16, 'State the observed frequency at the centre of the circle.'),
      [pt(S('1100 Hz'), 3)], 'phys-2-7', 'frequency-at-centre-of-circle',
      SQ(22, 'State the observed frequency at the centre of the circle.'), 3, stem=Q14SB2[:1]),
    T('14ci', 'Q14(c)(i)', 'B', Q(17, 'Describe how charge is distributed on a pear-shaped conductor.'),
      [pt(S('charge is concentrated at the pointed end'), 4)], 'phys-3-1', 'charge-on-pear-shaped-conductor',
      SQ(23, 'Describe how charge is distributed on a pear-shaped conductor.'), 4),
    T('14cii', 'Q14(c)(ii)', 'B', Q(17, 'Describe an experiment that demonstrates how charge is distributed over the surface of a',
                                    'pear-shaped conductor.'),
      [pt(S('apparatus: proof plane, electroscope'), 3),
       pt(S('method: sample at different positions (on pear-shaped object)'), 3),
       pt(S('result: leaves open to varying degrees'), 3)],
      'phys-3-1', 'charge-distribution-experiment',
      SQ(23, 'Describe an experiment that demonstrates how charge is distributed over the surface',
         'of a pear-shaped conductor.'), 9),
    T('14ciii', 'Q14(c)(iii)', 'B', Q(17, 'Explain why it is not possible to charge the dome of a Van de Graaff generator to a very high',
                                      'voltage when a pointed object is attached to it.'),
      [pt(S('point discharge'), 6)], 'phys-3-1', 'point-discharge-van-de-graaff',
      SQ(23, 'Explain why it is not possible to charge the dome of a Van de Graaff generator to a',
         'very high voltage when a pointed object is attached to it.'), 6),
    T('14civ', 'Q14(c)(iv)', 'B', Q(17, 'Draw a diagram to show the electric field due to the two charges.'),
      [crit(S('shape'), 2), crit(S('direction'), 2)], 'phys-3-2', 'field-of-two-charges',
      SQ(23, 'Draw a diagram to show the electric field due to the two charges.'), 4, stem=[Q14SC], fig='q14c-charges'),
    T('14cv', 'Q14(c)(v)', 'B', Q(17, 'Calculate the electric field strength at X.'),
      [pt(S('6.8 × 10³ (N C⁻¹)'), 3), pt(S('towards the negative charge'), 2)], 'phys-3-2', 'field-strength-at-x',
      SQ(23, 'Calculate the electric field strength at X.'), 5, stem=[Q14SC], fig='q14c-charges'),
    # Q14(d) Part (a)
    T('14dia', 'Q14(d)(i)', 'B', Q(18, 'Explain what is meant by anti-matter.'),
      [pt(S('(made of particles with) the same mass but opposite charge (to that which make up', 'matter)'), 3)],
      'phys-4-5', 'anti-matter', SQ(24, 'Explain what is meant by anti-matter.'), 3, route='part-a'),
    T('14diia', 'Q14(d)(ii)', 'B', Q(18, 'Explain how the quark model can be used to predict the charge of an anti-proton.'),
      [pt(S('anti-up, anti-up, anti-down'), 3), pt(S('(–2/3) + (–2/3) + (+1/3) = –1'), 3)],
      'phys-4-5', 'quark-model-anti-proton-charge',
      SQ(24, 'Explain how the quark model can be used to predict the charge of an anti-proton.'), 6, route='part-a'),
    T('14diiia', 'Q14(d)(iii)', 'B', Q(18, 'Express the minimum frequency f of the gamma rays emitted during this pair annihilation, in',
                                       'terms of the mass of a proton m, the speed of light c, and the Planck constant h.'),
      [pt(S('hf and mc²'), 3), pt(S('f = mc²/h'), 4)], 'phys-4-5', 'gamma-frequency-pair-annihilation',
      SQ(24, 'Express the minimum frequency f of the gamma rays emitted during this pair', 'constant h.'), 7,
      fig='q14d-reaction', route='part-a',
      decision='The paper\'s lead-in names the anti-proton with an overbar the text layer cannot carry; the lead-in '
               'and its equation are shown as a crop of the page.'),
    T('14divaa', 'Q14(d)(iv)(a)', 'B', [Q14DIV, Q(18, 'the strong nuclear force between the two protons,')],
      [G('fraction', page=24, clip=(125, 478, 200, 506), expect='F = q₁q₂/(4πεd²)', marks=2),
       pt(S('103 (N)'), 2), pt(S('1.23 × 10⁴ N'), 2)],
      'phys-3-1', 'strong-force-between-protons', SQ(24, 'the strong nuclear force between the two protons,'), 6,
      stem=[Q14DA], route='part-a'),
    T('14divba', 'Q14(d)(iv)(b)', 'B', [Q14DIV, Q(18, 'how many times stronger this strong nuclear force is than the gravitational force',
                                                  'between the two protons.')],
      [G('fraction', page=24, clip=(125, 587, 200, 613), expect='F = G (m₁ m₂)/d²', marks=2),
       pt(S('8.3 × 10⁻³⁵ (N)'), 2), pt(S('ratio: 1.48 × 10³⁸'), 2)],
      'phys-1-5', 'strong-force-against-gravity',
      SQ(24, 'how many times stronger this strong nuclear force is than the gravitational force',
         'between the two protons.'), 6, stem=[Q14DA], route='part-a', fig='q14d-ivb-scheme-formula',
      decision='The scheme sets the squared distance with a bold digit two the reader cannot raise; the formula '
               'is also shown as a crop of the scheme.'),
    # Q14(d) Part (b)
    T('14dib', 'Q14(d)(i)', 'B', Q(18, 'Explain what is meant by a bi-polar transistor.'),
      [pt(S('consists of npn / pnp'), 6,
          note='The scheme prices this one line [2 + 2 + 2] and prints no split of it.')],
      'phys-3-3', 'bipolar-transistor', SQ(25, 'Explain what is meant by a bi-polar transistor.'), 6, route='part-b',
      decision='One printed answer line under one cell [2 + 2 + 2]: the scheme names no three elements to price '
               'apart, so the line is one row at the cell\'s 6.'),
    T('14diib', 'Q14(d)(ii)', 'B', Q(18, 'State the relationship between the base current, the collector current and the emitter',
                                      'current.'),
      [pt(S('Iₑ = Ic + Ib'), 4)], 'phys-3-3', 'transistor-current-relationship',
      SQ(25, 'State the relationship between the base current, the collector current and the emitter', 'current.'), 4,
      route='part-b'),
    T('14diiiab', 'Q14(d)(iii)(a)', 'B', Q14DB3,
      [pt(S('transistor'), 3), pt(S('base resistor'), 3), pt(S('load resistor'), 3)], 'phys-3-3',
      'transistor-voltage-amplifier-circuit',
      SQ(25, 'Draw a circuit diagram to show how a transistor can be used as a voltage', 'amplifier.'), 9,
      route='part-b', source_pages=[18]),
    T('14diiibb', 'Q14(d)(iii)(b)', 'B', Q(18, 'Label the input voltage and the output voltage in your circuit diagram.'),
      [pt(S('input across base resistor'), 3), pt(S('output across collector–emitter'), 3)], 'phys-3-3',
      'amplifier-input-and-output',
      SQ(25, 'Label the input voltage and the output voltage in your circuit diagram.'), 6,
      stem=[M('(a)', 18), Q14DB3], route='part-b', source_pages=[18]),
    T('14divb', 'Q14(d)(iv)', 'B', Q(18, 'State one example of a device that uses a voltage amplifier.'),
      [pt(S('microphone'), 3)], 'phys-3-3', 'voltage-amplifier-device',
      SQ(25, 'State one example of a device that uses a voltage amplifier.'), 3, route='part-b'),
]

ANSWER_VARIANTS = {
    '3ib': [
        ('spectrometer', 'Spectrometer',
         [pt(dslash('rotate telescope to locate image on RHS of zero', 'grating to screen', 1), 2),
          pt(dslash('rotate telescope to locate image on LHS of zero', 'central image to other images', 1), 2),
          pt(dslash('reference to reading on circular scale', None, 1), 2)]),
        ('screen', 'Screen',
         [pt(dslash('rotate telescope to locate image on RHS of zero', 'grating to screen', 2), 2),
          pt(dslash('rotate telescope to locate image on LHS of zero', 'central image to other images', 2), 2),
          pt(dslash('reference to reading on circular scale', None, 2), 2)]),
    ],
    '10ia': [
        ('words', 'In words', [pt(dslash('charge', '// C = Q/V', 1), 3), pt(dslash('per unit voltage', '// notation', 1), 3)]),
        ('formula', 'As a formula', [pt(dslash('charge', '// C = Q/V', 2), 3), pt(dslash('per unit voltage', '// notation', 2), 3)]),
    ],
    '10ib': [
        ('words', 'In words', [pt(dslash('work', '// V = W/q', 1), 3), pt(dslash('per unit charge', '// notation', 1), 3)]),
        ('formula', 'As a formula', [pt(dslash('work', '// V = W/q', 2), 3), pt(dslash('per unit charge', '// notation', 2), 3)]),
    ],
    '12iiia': [
        ('geiger-muller', 'Geiger-Muller tube', [pt(dslash('Geiger-Muller tube', '// solid state detector', 1), 2)]),
        ('solid-state', 'Solid state detector', [pt(dslash('Geiger-Muller tube', '// solid state detector', 2), 2)]),
    ],
    '12iiib': [
        ('geiger-muller', 'Geiger-Muller tube',
         [pt(dslash('ionisation', '// free electrons produced', 1), 2), pt(dslash('current flows', '// current flows', 1), 2)]),
        ('solid-state', 'Solid state detector',
         [pt(dslash('ionisation', '// free electrons produced', 2), 2), pt(dslash('current flows', '// current flows', 2), 2)]),
    ],
    '13i': [
        ('conductor-insulator', 'Between a conductor and an insulator',
         [pt(S('resistivity'), 4), pt(dslash('between that of a conductor and an insulator', None, 1), 3)]),
        ('temperature', 'Decreases with temperature',
         [pt(S('resistivity'), 4), pt(dslash('between that of a conductor and an insulator', None, 2), 3)]),
    ],
    '14bia': [
        ('words', 'In words', [pt(dslash('rate of change', '// ω = θ/t', 1), 3), pt(dslash('of angle', '// notation', 1), 3)]),
        ('formula', 'As a formula', [pt(dslash('rate of change', '// ω = θ/t', 2), 3), pt(dslash('of angle', '// notation', 2), 3)]),
    ],
}

FIGURES = {
    # key suffix: (doc, page, rect in PDF points, credit, letters, alt, solution[, masks])
    'q1iii-scheme-table': ('scheme', 6, (100, 441, 520, 461), SEC, [],
        'Scheme table of 1/V (cm⁻³) for the six readings: 0.019, 0.023, 0.027, 0.031, 0.034, 0.043.', True),
    'q1v-scheme-sketch': ('scheme', 6, (100, 600, 240, 664), SEC, [],
        'Scheme sketch: axes labelled pV (vertical) and p (horizontal), with a straight line drawn level, parallel to the p axis.', True),
    'q2iv-scheme-table': ('scheme', 7, (128, 494, 520, 514), SEC, [],
        'Scheme table of T² (sec²) for the six lengths: 1.64, 2.01, 2.41, 2.89, 3.21, 3.61.', True),
    'q2v-scheme-formula': ('scheme', 7, (96, 656, 200, 688), SEC, [],
        "The scheme's formula for the period: T equals 2π times the square root of l over g.", True),
    'q6b-plank': ('paper', 7, (125, 262, 472, 404), SEC, ['X'],
        'A horizontal plank balanced on a triangular block. A 300 N weight hangs from the left end and a 450 N weight from the right end. X marks the centre of gravity, 2.5 m from the left weight and 0.3 m to the left of the block; the right weight hangs 2.0 m to the right of the block.', False),
    'q6h-resistors': ('paper', 8, (190, 78, 405, 180), SEC, [],
        'A resistor network between two terminals: an 8 Ω resistor in series with a 900 Ω resistor, and across the 900 Ω resistor a branch of a 15 Ω resistor in series with a 5 Ω resistor.', False),
    'q6j-equation': ('paper', 8, (280, 264, 345, 290), SEC, [],
        'The nuclear equation as printed: three alpha particles (mass number 4, atomic number 2) give carbon-12 (mass number 12, atomic number 6).', False),
    'q10iv-scheme-table': ('scheme', 16, (74, 458, 532, 478), SEC, [],
        'Scheme table of 1/d (m⁻¹) for the six plate separations: 47.6, 23.8, 15.9, 11.9, 9.5, 8.1.', True),
    'q10-circuit': ('paper', 12, (410, 412, 536, 500), SEC, [],
        'A series circuit: a 200 μF capacitor, a 40 kΩ resistor, a switch and a 12 V battery in one loop.', False),
    'q11-path': ('paper', 13, (260, 370, 335, 415), SEC, [],
        'A circled positive charge moving to the right; its path curves upwards just after it enters the magnetic field.', False),
    'q13ivc-scheme-formula': ('scheme', 20, (125, 302, 200, 330), SEC, [],
        "The scheme's formula: V rms equals V peak divided by the square root of 2.", True),
    'q14a-boat': ('paper', 16, (355, 120, 535, 196), SEC, [],
        'Between two river banks: the water flow arrow, 1.5 m s⁻¹, points to the right; from a dot labelled boat an arrow labelled 2.5 m s⁻¹ points up and to the right at 20° to a dashed line drawn along the flow.', False),
    'q14c-charges': ('paper', 17, (110, 398, 485, 432), SEC, ['X'],
        'A positive point charge on the left and a negative point charge on the right, with a point X marked between them, nearer the positive charge.', False),
    'q14d-reaction': ('paper', 18, (55, 98, 500, 144), SEC, [],
        'Part (a)\'s lead-in as printed: "The following reaction represents the pair annihilation of a proton p, and an anti-proton" '
        'followed by the symbol p with a bar over it, over the reaction: p plus p-bar gives 2 gamma.', False),
    'q14d-ivb-scheme-formula': ('scheme', 24, (125, 587, 200, 613), SEC, [],
        "The scheme's formula for the gravitational force: F equals G times m₁ m₂ over d².", True),
}
