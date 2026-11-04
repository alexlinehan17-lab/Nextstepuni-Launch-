"""Independent review ledger: Leaving Certificate Geography 2013 Higher Level.

Sources (English editions, harvested Paper Trail corpus; sizes and SHA-256
pinned in EXPECTED_SOURCES and the generated audit): the examination paper
LC005ALP000EV (32 pages; one booklet printed Part One, answered in it, and
Part Two), marking scheme LC005ALP000EV (48 pages), and the common
Enniscorthy companions as Paper Trail files them — the 1:50 000 map
LC005CLP003EV (one scanned 1379 x 1936 image in a one-page PDF), its legend
LC005CLPC00EV and the aerial photograph LC005CLP004EV (one-page PDFs, each a
single scanned image). Part One is 80 marks (any ten of twelve @ 8), Part
Two 320 (four questions @ 80).

Visual sweep (every page rendered and read on 2026-10-23):
  Paper p1 cover and examiner's grid; p2-p12 Part One Questions 1-12 (p6
  holds Q5 and Q6; Q1 prints a map of Atlantic Ocean crust ages, Q3 and Q7
  OS map extracts (Q7 with its cross-section), Q4 four photographs, Q8 a
  wind rose, Q9 a map of European public debt, Q10 four satellite images,
  Q11 a table of daily Irish speakers); p13 Part Two instructions; p14
  Section 1 divider; p15-p20 Q1-Q6 (p15 and p18 open with their dividers);
  p21 Section 2 divider; p22-p27 Electives Q7-Q12 (p22 and p25 open with
  their elective dividers; p26 prints the 1:2000 map of central
  Enniscorthy for 11A); p28 Section 3 divider and option note; p29-p30
  Options Q13-Q24; p31 and p32 printed "Blank Page".
  Scheme p1 cover; p2 note on marking schemes; p3 introduction; p4 Part One
  table (a centred tariff heading that prices each question, then two
  columns: Q1-Q6, Q7-Q12; the answer lines print no marks); p5 Part Two
  instructions and Section 1 divider; p6-p11 Q1-Q3 (p6 opens with its
  divider); p12-p17 Q4-Q6 (p12 opens with its divider); p18 Section 2
  divider; p19-p24 Q7-Q9; p25-p30 Q10-Q12 (p19 and p25 open with their
  elective dividers); p31 Section 3 divider; p32-p39 Options Q13-Q24 (no
  separate Overall Coherence table: each option prices coherence within its
  aspects); p40-p41 Geographical Investigation (coursework) and its
  presentation marks; p42 investigation topics; p43 Irish-language bonus
  marks; p44-p47 printed "Blank Page"; p48 back cover. The scheme reprints
  each Part Two question above its allocation; every slice starts at the
  allocation.
  Companions: Enniscorthy map extract (the River Slaney, the Boro River,
  Bree Hill, Oilgate); OS Discovery Series legend sheet; oblique aerial
  photograph of Enniscorthy (stored turned on its side: the River Slaney,
  the railway bridge and the cathedral spire).

The scheme sets its note bullets in Wingdings (private-use U+F0D8);
geography_review maps the glyph to its printed meaning, so the notes read
"•" as in every other sitting.

Part One prices each question in its heading: "Q1 Parts (i),(iii) & (iv)
@1m + 1m; Part (ii) @ 2m", "Q4 & 12 8 parts @ 1m each", "Q2 & 3 Part (i) 4
parts @ 1m; Part (ii) 2@ 1+1m", "Q5 Parts (i), (ii) & (iv) 1+1m; Part (iii)
2m", "Q6 & 11 Parts (i),(ii) & (iii) @ 2m; Part (iv) 1+ 1m" and "Q7, 8 9 and
10: 4 parts @ 2 marks each", so every Part One card carries its heading line
with the answer lines it prices. Matching tables, in the printed row order:
Q2 Focus C, Epicentre D, Seismic waves A, Fault line B; Q3 Hanging valley D,
Arête C, Tarn A, Truncated spur B; Q4 Scree D Freeze thaw action, Pebble
beach A Attrition, Blow hole C Air pressure, Terracettes B Soil creep; Q7
U-Shaped valley B, V-Shaped valley D, Third class road C, Concave slope A;
Q10 Deforestation D, Hydro electric power station C, Nuclear power station
B, River flooding A. Q12 completes two rock rows (Sandstone-Sedimentary-Mts
Munster-Quartzite, Granite-Igneous-Wicklow Mts-Gneiss), each of four
one-mark cells. Q4 answers (i) and (ii) in one table and is one card of
two-mark rows; Q7, Q10 and Q12 are one card each; Q2 and Q3 card (i) and
(ii) apart, as the heading prices them.

Part Two: 2A, 3A, 5A, 6A, 7A and 10A print each roman's marks; 9A and 12A
price a graph (16) and a definition (4). 12C prices its two issues "@ 8 + 7
SRPs" (16 + 14) and 5B its two factors 8 and 7 SRPs. The options print two
schemes, "3 @ 27 + 27 + 26" or "4 @ 20 marks each" (identifying aspect,
discussion and coherence inside each aspect), chosen by the number of
aspects the candidate discusses, so each is one criterion of 80; Q18 (any
three factors) prints only the three-aspect scheme and Q24 (four printed
phenomena) only the four-aspect one, so their aspects are criteria.

Printed choices: 2B (i) or (ii) is two routes; 2C (one of four activities)
and 7A(v) (one of two terms) are one route per printed option; 2A(ii)
"faulting at A or at B" and 3B "physical weathering or chemical weathering"
are two routes each. 5B (any two of three factors) and 18 (any three of
four factors) are pools, one card each.
"""

from geography_review import (
    Criterion, Lift, Route, SchemeSlice, Task, pool, evens, fixed, slug, srp, sums, upto,
)

YEAR = 2013
LEVEL = 'higher'
PAPER_PAGES = {1: 32, 2: 32}
SCHEME_PAGES = 48
QUESTION_TARIFFS = {1: {str(n): 8 for n in range(1, 13)},
                    2: {**{f'{n}{x}': (20 if x == 'A' else 30)
                           for n in range(1, 13) for x in 'ABC'},
                        **{str(n): 80 for n in range(13, 25)}}}

EXPECTED_SOURCES = {
    'paper1': ('LC005ALP000EV.pdf', 3686604),
    'paper2': ('LC005ALP000EV.pdf', 3686604),
    'scheme': ('LC005ALP000EV.pdf', 1035658),
    'map': ('LC005CLP003EV.pdf', 1340745),
    'legend': ('LC005CLPC00EV.pdf', 1167773),
    'aerial': ('LC005CLP004EV.pdf', 1646330),
}

_PAPER = {1: 'cover and examiner grid', **{p: 'question' for p in range(2, 13)},
          13: 'Part Two instructions', 14: 'section divider', **{p: 'question' for p in range(15, 21)},
          21: 'section divider', **{p: 'question' for p in range(22, 28)}, 28: 'section divider and option note',
          29: 'question', 30: 'question', 31: 'blank page', 32: 'blank page'}
PAGE_REVIEW = {
    # One booklet printed both parts.
    'paper1': _PAPER, 'paper2': _PAPER,
    'scheme': {1: 'cover', 2: 'notes', 3: 'notes', 4: 'Part One table',
               5: 'Part Two instructions and section divider',
               **{p: 'Part Two allocation' for p in range(6, 18)}, 18: 'section divider',
               **{p: 'Part Two allocation' for p in range(19, 31)}, 31: 'section divider',
               **{p: 'option allocation' for p in range(32, 40)},
               40: 'geographical investigation (coursework)',
               41: 'geographical investigation presentation marks', 42: 'investigation topics',
               43: 'Irish-language bonus marks', **{p: 'blank' for p in range(44, 48)}, 48: 'back cover'},
}

EXPECTED_SELECTION_SCAN = [
    [1, 2, 'attempt ten'], [1, 13, 'attempt four'], [1, 14, 'attempt two'], [1, 15, 'attempt one'],
    [1, 16, 'answer (i) or (ii)'], [1, 16, 'one of the following'], [1, 18, 'attempt one'],
    [1, 19, 'any two'], [1, 21, 'attempt one'], [1, 22, 'one of the following'], [1, 28, 'attempt one'],
    [1, 29, 'any three'],
]
SELECTION_REVIEW = [
    {'scan': [[1, 2, 'attempt ten'], [1, 13, 'attempt four'], [1, 14, 'attempt two'], [1, 15, 'attempt one'],
              [1, 18, 'attempt one'], [1, 21, 'attempt one'], [1, 28, 'attempt one']],
     'kind': 'exam-attempt-rule',
     'reason': 'Part One any ten of twelve and Part Two four questions (one of Q1-3, one of Q4-6, one elective, one option) are attempt rules; every question is carded.'},
    {'scan': [[1, 16, 'answer (i) or (ii)']], 'kind': 'closed-route',
     'reason': '2B: (i) or (ii) -> two routes, each with its own scheme allocation.'},
    {'scan': [[1, 16, 'one of the following'], [1, 22, 'one of the following']], 'kind': 'closed-choose-one',
     'reason': '2C one of four printed rock-cycle activities -> 4 routes; 7A(v) one of two printed terms (Balance of Trade, Balance of Payments) -> 2 routes.'},
    {'scan': [[1, 19, 'any two'], [1, 29, 'any three']], 'kind': 'choose-n-one-card',
     'reason': '5B any two of three printed factors and 18 any three of four printed factors -> one card each with every printed item (choice is not a route).'},
    {'scan': [], 'kind': 'inline-closed-route',
     'reason': '2A(ii) "the type of faulting at A or at B" -> 2 routes; 3B "physical weathering or chemical weathering" -> 2 routes (no directive word the scan reads; the route text is anchored on the paper).'},
    {'scan': [], 'kind': 'open-response',
     'reason': 'Open choices are not fanned out: 2B(i) "one landform of erosion", "one urban area", "one multinational company", "a developed economy", "a developing economy", "one biome", "one climate type", "example(s)", 10B three patterns, 12B three reasons, 12C two issues; 6C and 22 "and/or" are not a choice of one. Compulsory lists stay whole: 1A, 4A, 8A and 11A each bullet, 7B all three headings, 24 each printed phenomenon; Part One Q4(ii) and Q12 print answer options, not routes.'},
]

P1, P2 = 1, 2
LEFT = (0.0, 0.36, 0.47, 1.0)
RIGHT = (0.47, 0.36, 1.0, 1.0)
ID = 'geography-2013-hl-'
H = 'geography-higher-'
SRPS = 'SRPs'
# The Part One heading line that prices each question.
T1 = 'Q1 Parts (i),(iii) & (iv)'
T4 = 'Q4 & 12 8 parts'
T2 = 'Q2 & 3 Part (i)'
T5 = 'Q5 Parts (i), (ii) & (iv)'
T6 = 'Q6 & 11 Parts'
T7 = 'Q7, 8 9 and 10'


def L(page, start, end=None, nth=None):
    return Lift(page, start, end, None, nth)


def S(page, start, end=None, clip=None, after=None, table=False):
    return SchemeSlice(page, start, end, clip, after, table)


H1 = S(4, 'Q1 Parts', 'Q4 & 12')
H4 = S(4, 'Q4 & 12', 'Q2 & 3')
H2 = S(4, 'Q2 & 3', 'Q5 Parts')
H5 = S(4, 'Q5 Parts', 'Q6 & 11')
H6 = S(4, 'Q6 & 11', 'Q7, 8 9')
H7 = S(4, 'Q7, 8 9', 'No grading')


def T(key, part, q, sub, marks, page, title, prompt, scheme, criteria, topic, atlas, card_id,
      sources=(), stem=(), routes=(), row_labels=(), absorbs=()):
    return Task(key, part, q, sub, marks, page, title, prompt, scheme, criteria, topic, atlas,
                sources, card_id, False, stem=stem, routes=routes, row_labels=row_labels,
                absorbs=absorbs)


def priced_rows(tariff, lines, marks, permitted=None, labels=None):
    """Rows of a Part One table; the first carries the heading that prices them."""
    return tuple(fixed(labels[i - 1] if labels else f'Row {i}', marks,
                       (tariff, line) if i == 1 else line, permitted)
                 for i, line in enumerate(lines, 1))


def answer(label, tariff, line, marks=2, permitted=None):
    lines = (tariff, *line) if isinstance(line, tuple) else (tariff, line)
    return (fixed(label, marks, lines, permitted),)


def pair(line, label):
    return fixed(label, 4, line, (0, 2, 4))


def romans(q, part, page, title, stem, first_id, sources, parts):
    """parts: (sub, marks, prompt Lift(s), scheme slice(s), criteria, topic, atlas[, row labels[, extra stem]])."""
    out = []
    for index, item in enumerate(parts):
        sub, marks, prompt, scheme, criteria, topic, atlas = item[:7]
        labels = item[7] if len(item) > 7 else ()
        extra = item[8] if len(item) > 8 else ()
        key = sub.strip('()').replace(')(', '-')
        out.append(T(f'p{part}-{q.lower()}-{key}', part, q, sub, marks, page, title,
                     prompt if isinstance(prompt, tuple) else (prompt,),
                     scheme if isinstance(scheme, tuple) else (scheme,), criteria, topic, atlas,
                     first_id if index == 0 else f'{first_id}-{key}', sources, (*stem, *extra),
                     row_labels=labels))
    return out


def bullet_routes(prefix, items, topic=None, atlas=None):
    """One route per printed bullet of a choose-one list."""
    return tuple(Route(slug(item, 34), item.rstrip('.'), ID + prefix + slug(item, 34), False,
                       keep_bullets=(item,), topic=topic, atlas=atlas)
                 for item in items)


PS = (H + 'plate-tectonics',)
RW = (H + 'rocks-weathering-mass-movement',)
RIVERS = (H + 'rivers',)
SEA = (H + 'the-sea',)
GLAC = (H + 'glaciation',)
EV = (H + 'earthquakes-volcanoes',)
MAP = (H + 'mapwork',)
AER = (H + 'aerial-photos',)
TG = (H + 'tablesgraphs-questions',)
WX = (H + 'weather-climate',)
IRL = (H + 'regions-ireland',)
EURO = (H + 'regions-european',)
CONT = (H + 'regions-continental',)
POP = (H + 'human-population',)
URB = (H + 'human-urban-geography',)
ECON = (H + 'elective-economic',)
DEV = (H + 'economic-developing-economies',)
MNC = (H + 'economic-multinationals-globalisation',)
EU_ECON = (H + 'economic-european-union',)
ENERGY = (H + 'economic-energy',)
ENV = (H + 'economic-environmental-impact',)

# ---------------------------------------------------------------- Part One --
PART_ONE = romans('1', P1, 2, L(2, 'Plate Tectonics'),
                  (L(2, 'Examine the map above and answer the following questions.'),),
                  ID + 'p1-q1', ('page',), [
    ('(i)', 2, L(2, '(i) Name the plate at A and the plate at B.'),
     (H1, S(4, 'Q.1 (i)', '(ii) C = Basalt', LEFT)),
     answer('Plates at A and B', T1, 'Q.1 (i) A = North American', 2, (0, 1, 2)), '0-0', PS),
    ('(ii)', 2, L(2, '(ii) Name the type of igneous rock most frequently found at C.'),
     (H1, S(4, '(ii) C = Basalt', '(iii) C = 0', LEFT)),
     answer('Igneous rock at C', T1, '(ii) C = Basalt/Extrusive/Volcanic'), '0-1', RW + PS),
    ('(iii)', 2, L(2, '(iii) State the age range of the ocean crust at C and the age range of the',
                   'ocean crust at D.'),
     (H1, S(4, '(iii) C = 0', '(iv) Any valid reason', LEFT)),
     (fixed('Age range at C', 1, (T1, '(iii) C = 0 - 60 million')),
      fixed('Age range at D', 1, 'D = 120 - 180 million')), '0-0', PS),
    ('(iv)', 2, L(2, '(iv) Explain briefly why the ocean crust at D is older than the ocean crust at C.'),
     (H1, S(4, '(iv) Any valid reason', 'Q.2', LEFT)),
     answer('Explanation', T1, '(iv) Any valid reason explained', 2, (0, 1, 2)), '0-0', PS),
])
PART_ONE += romans('2', P1, 3, L(3, 'Earthquakes'), (), ID + 'p1-q2', ('page',), [
    ('(i)', 4, L(3, '(i) Match each of the letters A, B, C and D on the above diagram with the correct',
                 'in the table below.'),
     (H2, S(4, 'Q.2 (i)', '(ii) Any two valid', LEFT)),
     priced_rows(T2, ['Q.2 (i) C Focus', 'D Epicentre', 'A Seismic waves', 'B Fault line'], 1), '0-7', EV,
     (L(3, 'Focus'), L(3, 'Epicentre'), L(3, 'Seismic waves'), L(3, 'Fault line'))),
    ('(ii)', 4, L(3, '(ii) Explain briefly each of the following terms.'),
     (H2, S(4, '(ii) Any two valid explanations', 'Q.3', LEFT, 'Q.2 (i)')),
     priced_rows(T2, ['(ii) Any two valid explanations'] * 2, 2, (0, 1, 2)), '0-7', EV,
     (L(3, 'Seismologist'), L(3, 'Seismometer'))),
])
PART_ONE += romans('3', P1, 4, L(4, 'Glaciation'), (), ID + 'p1-q3', ('page',), [
    ('(i)', 4, L(4, '(i) Examine the Ordnance Survey extract above and match each of the letters',
                 'in the table below.'),
     (H2, S(4, 'Q.3 (i)', '(ii) Any two valid', LEFT)),
     priced_rows(T2, ['Q.3 (i) D Hanging Valley', 'C Arête', 'A Tarn', 'B Truncated spur'], 1),
     '0-11', GLAC + MAP,
     (L(4, 'Hanging valley'), L(4, 'Arête'), L(4, 'Tarn'), L(4, 'Truncated spur'))),
    ('(ii)', 4, L(4, '(ii) Explain briefly each of the following terms.'),
     (H2, S(4, '(ii) Any two valid explanations', 'Q.4', LEFT, 'Q.3 (i)')),
     priced_rows(T2, ['(ii) Any two valid explanations'] * 2, 2, (0, 1, 2)), '0-11', GLAC,
     (L(4, 'Plucking'), L(4, 'Abrasion'))),
])
PART_ONE.append(T(
    'p1-4', P1, '4', '', 8, 5, L(5, 'Physical Features and Processes'),
    (L(5, '(i) Insert the letter which best matches each of the photographs', 'correct description.'),
     L(5, '(ii) Insert the correct process from the following list', 'Soil creep.')),
    (H4, S(4, 'Q.4 D', 'Q.5', LEFT)),
    priced_rows(T4, ['Q.4 D Freeze thaw action', 'A Attrition', 'C Air pressure', 'B Soil creep'], 2, (0, 1, 2)),
    '0-4', RW + SEA, ID + 'p1-q4', ('page',),
    (L(5, 'Examine the photographs and answer each of the following questions in the table below.'),),
    row_labels=(L(5, 'Scree'), L(5, 'Pebble beach'), L(5, 'Blow hole'), L(5, 'Terracettes'))))
PART_ONE += romans('5', P1, 6, L(6, 'Ordnance Survey Map', nth=0),
                   (L(6, 'Using the 1:50000 Ordnance Survey map and legend that accompany this paper,',
                      'following questions.'),),
                   ID + 'p1-q5', ('map', 'legend'), [
    ('(i)', 2, L(6, '(i) Name and give a six-figure grid reference for an antiquity built by the Normans.'),
     (H5, S(4, 'Q.5 (i)', '(ii) Bree', LEFT)),
     answer('Name and grid reference', T5, 'Q.5 (i) Name + GR', 2, (0, 1, 2)), '2-6', MAP),
    ('(ii)', 2, L(6, '(ii) Name and give a six-figure grid reference for the highest point on the map.'),
     (H5, S(4, '(ii) Bree', '(iii) 96', LEFT)),
     answer('Name and grid reference', T5, '(ii) Bree Hill S934/5 329/330', 2, (0, 1, 2)), '2-6', MAP),
    ('(iii)', 2, L(6, '(iii) Calculate the area of the map which is west of easting T 00.'),
     (H5, S(4, '(iii) 96', '(iv) Any two named', LEFT)), answer('Area', T5, '(iii) 96sq km'), '2-6', MAP),
    ('(iv)', 2, L(6, '(iv) Name two ways that height is shown on an Ordnance Survey map.'),
     (H5, S(4, '(iv) Any two named', 'Q.6', LEFT)),
     answer('Two ways', T5, '(iv) Any two named', 2, (0, 1, 2)), '2-6', MAP),
])
PART_ONE += romans('6', P1, 6, L(6, 'Aerial Photograph and Ordnance Survey Map'),
                   (L(6, 'Using the aerial photograph, the 1:50000 Ordnance Survey map and legend',
                      'following questions.'),),
                   ID + 'p1-q6', ('aerial', 'map', 'legend'), [
    ('(i)', 2, L(6, '(i) In which direction was the camera pointed when the aerial photograph was taken?'),
     (H6, S(4, 'Q.6 (i)', '(ii) N11', LEFT)), answer('Direction', T6, 'Q.6 (i) North/North North East'),
     '2-8', AER + MAP),
    ('(ii)', 2, L(6, '(ii) Name the main road in the centre background of the aerial photograph.'),
     (H6, S(4, '(ii) N11', '(iii) Right', LEFT)), answer('Road', T6, '(ii) N11'), '2-8', AER + MAP),
    ('(iii)', 2, L(6, '(iii) The railway station is shown on the Ordnance Survey map at S 974 402.',
                   'shown on the aerial photograph.'),
     (H6, S(4, '(iii) Right', '(iv) Any valid explanation', LEFT)),
     answer('Location', T6, '(iii) Right Centre/Middle'), '2-8', AER + MAP),
    ('(iv)', 2, L(6, '(iv) Explain briefly why there is an absence of settlement in the area to the right of',
                  'centre of the aerial photograph.'),
     (H6, S(4, '(iv) Any valid explanation', 'Pa', LEFT)),
     answer('Explanation', T6, '(iv) Any valid explanation', 2, (0, 1, 2)), '4-3', URB + AER + MAP),
])
PART_ONE.append(T(
    'p1-7', P1, '7', '', 8, 7, L(7, 'Map Skills – Cross-Section'),
    (L(7, 'Match each of the letters A, B, C and D on the cross-section', 'in the table below.'),),
    (H7, S(4, 'Q.7', 'Q.8', RIGHT)),
    priced_rows(T7, ['Q.7 · B U Shaped valley', 'D V Shaped valley', 'C Third class road', 'A Concave slope'], 2),
    '2-6', MAP + GLAC + RIVERS, ID + 'p1-q7', ('page', 'legend'),
    (L(7, 'The blue line indicates the location of a trail X-Y', 'is also shown.'),
     L(7, 'Examine the Ordnance Survey extract and cross-section, and the Ordnance Survey legend',
       'accompanying this paper.')),
    row_labels=(L(7, 'U-Shaped valley'), L(7, 'V-Shaped valley'), L(7, 'Third class road'),
                L(7, 'Concave slope'))))
PART_ONE += romans('8', P1, 8, L(8, 'Graphical Interpretation - Weather'),
                   (L(8, 'Examine the wind rose above and answer each of the following questions.'),),
                   ID + 'p1-q8', ('page',), [
    ('(i)', 2, L(8, '(i) What percentage of wind blowing from the South West was at a speed of',
                 'between 1-9 km/h?'),
     (H7, S(4, 'Q.8', '(ii) 12%', RIGHT)), answer('Percentage', T7, 'Q.8 · (i) 12%'), '2-7', WX + TG),
    ('(ii)', 2, L(8, '(ii) What percentage of wind blew from the North West?'),
     (H7, S(4, '(ii) 12%', '(iii) SW', RIGHT)), answer('Percentage', T7, '(ii) 12%'), '2-7', WX + TG),
    ('(iii)', 2, L(8, '(iii) From what direction did the wind blow most frequently?'),
     (H7, S(4, '(iii) SW', '(iv) SE', RIGHT)), answer('Direction', T7, '(iii) SW'), '2-7', WX + TG),
    ('(iv)', 2, L(8, '(iv) From what direction did the wind blow least frequently?'),
     (H7, S(4, '(iv) SE', 'Q.9', RIGHT)), answer('Direction', T7, '(iv) SE'), '2-7', WX + TG),
])
PART_ONE += romans('9', P1, 9, L(9, 'European Economy'),
                   (L(9, 'Examine the map of Europe above showing public debt', 'ticking the correct box.'),),
                   ID + 'p1-q9', ('page',), [
    ('(i)', 2, L(9, '(i) Four EU member states had a public debt of over 100% of GDP in 2011.'),
     (H7, S(4, 'Q.9', '(ii) False', RIGHT)), answer('True or false', T7, 'Q.9 · (i) True'), '2-0', TG + EURO),
    ('(ii)', 2, L(9, '(ii) Portugal had a public debt of between 80-99% of GDP in 2011.'),
     (H7, S(4, '(ii) False', '(iii) True', RIGHT)), answer('True or false', T7, '(ii) False'), '2-0', TG + EURO),
    ('(iii)', 2, L(9, '(iii) Poland and Denmark had the same public debt as a percentage of GDP in 2011.'),
     (H7, S(4, '(iii) True', '(iv) True', RIGHT)), answer('True or false', T7, '(iii) True'), '2-0', TG + EURO),
    ('(iv)', 2, L(9, '(iv) Spain, Austria and Hungary had a public debt of 60-79% of GDP in 2011.'),
     (H7, S(4, '(iv) True', 'Q.10', RIGHT)), answer('True or false', T7, '(iv) True'), '2-0', TG + EURO),
])
PART_ONE.append(T(
    'p1-10', P1, '10', '', 8, 10, L(10, 'Satellite Image Interpretation'),
    (L(10, 'Match each of the letters A, B, C and D with the description in the table below that best',
       'matches it.'),),
    (H7, S(4, 'Q.10', 'Q.11', RIGHT)),
    priced_rows(T7, ['Q.10 · D Deforestation', 'C Hydroelectric power station', 'B Nuclear power station',
                     'A River flooding'], 2),
    '2-8', AER, ID + 'p1-q10', ('page',), (L(10, 'Examine the satellite images above.'),),
    row_labels=(L(10, 'Deforestation'), L(10, 'Hydro electric power station'), L(10, 'Nuclear power station'),
                L(10, 'River flooding'))))
PART_ONE += romans('11', P1, 11, L(11, 'Statistical Interpretation'),
                   (L(11, 'Examine the table above which shows Daily Irish Speakers in Gaeltacht Areas',
                      'answer the following questions.'),),
                   ID + 'p1-q11', ('page',), [
    ('(i)', 2, L(11, '(i) What was the percentage change in Daily Irish Speakers in All Gaeltacht Areas',
                 'between 2006 and 2011?'),
     (H6, S(4, 'Q.11', '(ii) 22', RIGHT)), answer('Percentage change', T6, 'Q.11 · (i) 2.9'), '2-0', TG),
    ('(ii)', 2, L(11, '(ii) Calculate X, the decrease in the total number of Daily Irish Speakers',
                  'between 2006 and 2011.'),
     (H6, S(4, '(ii) 22', '(iii) 5', RIGHT)), answer('X', T6, '(ii) 22'), '2-0', TG),
    ('(iii)', 2, L(11, '(iii) How many Gaeltacht areas had an increase in the number of Daily Irish Speakers',
                   'between 2006 and 2011?'),
     (H6, S(4, '(iii) 5', '(iv) Any valid reason', RIGHT)), answer('Number of areas', T6, '(iii) 5'), '2-0', TG),
    ('(iv)', 2, L(11, '(iv) Explain briefly one reason why the percentage of Daily Irish Speakers',
                  'fell by 8.5% between 2006 and 2011.'),
     (H6, S(4, '(iv) Any valid reason', 'Q.12', RIGHT)),
     answer('Reason', T6, '(iv) Any valid reason explained', 2, (0, 1, 2)), '1-3', IRL),
])
PART_ONE.append(T(
    'p1-12', P1, '12', '', 8, 12, L(12, 'Rocks'),
    (L(12, 'The table below contains information on rocks', 'One row of the table is completed for you.'),),
    (H4, S(4, 'Q.12', 'age 2 of 44', RIGHT)),
    priced_rows(T4, ['Q.12 · Sandstone-Sedimentary-Mts Munster-Quartzite', 'Granite-Igneous-Wicklow Mts-Gneiss'],
                4, upto(4), ('Completed row 1', 'Completed row 2')),
    '0-1', RW, ID + 'p1-q12', ('page',)))


# ---------------------------------------------------------------- Part Two --
def sketch(outline_line, outline_permitted, alloc, item_permitted, labels):
    return (fixed('Sketch outline' if 'ketch' in outline_line else 'Map outline', 4,
                  outline_line, outline_permitted),
            *(Criterion(f'Feature {n}', 4, item_permitted, 'exact', alloc) for n in range(1, labels + 1)))


SHOWN3 = sums((0, 1, 3), (0, 1))
GRAPH = (fixed('Title', 2, ('Bar Chart · Pie Chart', 'Title · 2 marks · 2 marks')),
         fixed('Axes named (bar chart) / circle and centre (pie chart)', 2,
               ('Vertical axis named', 'Horizontal axis named'), (0, 1, 2)),
         fixed('6 items illustrated', 12, '6 items illustrated', upto(12)))

PART_TWO = [
    T('p2-1a', P2, '1A', '', 20, 15, L(15, 'Ordnance Survey Map'),
      (L(15, 'Examine the 1:50000 Ordnance Survey map and legend that accompany this paper.',
         'An area of Natural Woodland.'),),
      (S(6, 'Sketch Outline:', None),),
      sketch('Sketch Outline: · 4 marks', (0, 4),
             ('4 features @ 4 marks each · Shown 3 marks (graded 3/1/0)', 'Named 1 mark'), SHOWN3, 4),
      '2-6', MAP + RIVERS, ID + 'p2-q1a', ('map', 'legend'),
      row_labels=(None, L(15, 'The complete course of the River Slaney'),
                  L(15, 'The confluence of the River Slaney and Boro River (mark it with an X on the sketch map)'),
                  L(15, 'An area of land above 170 metres'), L(15, 'An area of Natural Woodland.'))),
    T('p2-1b', P2, '1B', '', 30, 15, L(15, 'Rocks'),
      (L(15, 'Explain the formation of metamorphic rocks, with reference to examples from Ireland.'),),
      (S(7, 'Name two metamorphic', 'C. · Fluvial'),),
      (pair('Name two metamorphic rocks · 2 + 2 marks', 'Two metamorphic rocks named'),
       srp('Explanation', 13, f'Explanation · 13 x {SRPS}')),
      '0-1', RW, ID + 'p2-q1b'),
    T('p2-1c', P2, '1C', '', 30, 15, L(15, 'Fluvial Adjustment'),
      (L(15, 'Explain how rivers adjust to a change in base level', 'that you have studied.'),),
      (S(7, 'Adjustment identified', None),),
      (fixed('Adjustment identified', 2, 'Adjustment identified · 2 marks'),
       fixed('Example', 2, 'Example · 2 marks'), srp('Explanation', 13, f'Explanation · 13 x {SRPS}')),
      '0-5', RIVERS, ID + 'p2-q1c'),
]
Q2AT = L(16, 'Faulting and Landforms')
Q2AS = (L(16, 'Examine the diagrams above and answer the following questions.'),)
FAULT = 'at A or at B'
PART_TWO += romans('2A', P2, 16, Q2AT, Q2AS, ID + 'p2-q2a', ('page',), [
    ('(i)', 8, L(16, '(i) Name the type of fault at A and the type of fault at B.'),
     S(8, '(i) · A = Normal', '(ii) Any valid'),
     (fixed('Fault at A', 4, '(i) · A = Normal · 4 marks'), fixed('Fault at B', 4, 'B = Reverse · 4 marks')),
     '0-2', RW + PS),
])
PART_TWO.append(T(
    'p2-2a-ii', P2, '2A', '(ii)', 4, 16, Q2AT,
    (L(16, '(ii) Explain briefly what causes the type of faulting at A or at B.'),),
    (S(8, '(ii) Any valid', '(iii) C = Rift'),), (pair('(ii) Any valid explanation · 2 + 2 marks', 'Explanation'),),
    '0-2', RW + PS, ID + 'p2-q2a-ii-faulting-at-a', ('page',), Q2AS,
    routes=(Route('faulting-at-a', 'Faulting at A', ID + 'p2-q2a-ii-faulting-at-a', False, ((FAULT, 'at A'),)),
            Route('faulting-at-b', 'Faulting at B', ID + 'p2-q2a-ii-faulting-at-b', False, ((FAULT, 'at B'),)))))
PART_TWO += romans('2A', P2, 16, Q2AT, Q2AS, ID + 'p2-q2a-iii', ('page',), [
    ('(iii)', 8, L(16, '(iii) Name the landform at C and the landform at D that result from faulting.'),
     S(8, '(iii) C = Rift', None),
     (fixed('Landform at C', 4, '(iii) C = Rift Valley/Graben · 4 marks'),
      fixed('Landform at D', 4, 'D = Block Mountain/Horst 4 marks')), '0-2', RW),
])
ROCK = ('Mining', 'Extraction of building materials', 'Oil/gas exploration', 'Geothermal energy production.')
PART_TWO += [
    T('p2-2b', P2, '2B', '', 30, 16, L(16, 'Landform Development'),
      (L(16, '(i) Explain with the aid of a labelled diagram(s) the formation of one landform of',
         'that you have studied.'),),
      (S(9, 'Named landform', 'Or'),),
      (fixed('Named landform', 2, 'Named landform · 2 marks'),
       fixed('Labelled diagram', 4, 'Labelled diagram · 4 marks (graded 4/2/0)', (0, 2, 4)),
       srp('Explanation', 12, f'Explanation · 12 x {SRPS}')),
      '0-4', RIVERS + SEA + GLAC, ID + 'p2-q2b-route-i',
      routes=(
          Route('route-i', 'Route (i)', ID + 'p2-q2b-route-i', False, topic='0-4', atlas=RIVERS + SEA + GLAC),
          Route('route-ii', 'Route (ii)', ID + 'p2-q2b-route-ii', False,
                prompt=(L(16, '(ii) Describe and explain one process of mass movement that you have studied.'),),
                scheme=(S(9, 'Process named', 'C. · Human'),),
                criteria=(fixed('Process named', 2, 'Process named · 2 marks'),
                          srp('Explanation', 14, f'Explanation · 14 x {SRPS}')),
                topic='0-8', atlas=RW),
      )),
    T('p2-2c', P2, '2C', '', 30, 16, L(16, 'Human Interaction'),
      (L(16, 'Examine how humans interact with the rock cycle, with reference to one of the following:',
         'Geothermal energy production.'),),
      (S(9, 'Example · 2 marks', None),),
      (fixed('Example', 2, 'Example · 2 marks'), srp('Examination', 14, f'Examination · 14 x {SRPS}')),
      '0-6', RW, ID + 'p2-q2c-mining', routes=bullet_routes('p2-q2c-', ROCK)),
]
Q3AS = (L(17, 'Examine the map and legend above showing the extent of the materials deposited',
          'following questions.'),)
PART_TWO += romans('3A', P2, 17, L(17, 'Volcanoes', nth=0), Q3AS, ID + 'p2-q3a', ('page',), [
    ('(i)', 4, L(17, '(i) What were the most extensive deposits as a result of the eruption?'),
     S(10, '(i) · Lateral', '(ii) · North West'),
     (fixed('Deposits', 4, '(i) · Lateral blast deposits · 4 marks'),), '0-7', EV),
    ('(ii)', 4, L(17, '(ii) What was the direction of the pyroclastic flow deposits?'),
     S(10, '(ii) · North West', '(iii) · 5-5.2'), (fixed('Direction', 4, '(ii) · North West'),), '0-7', EV),
    ('(iii)', 4, L(17, '(iii) What distance did the pyroclastic flow deposits extend to?'),
     S(10, '(iii) · 5-5.2', '(iv) · Any two'), (fixed('Distance', 4, '(iii) · 5-5.2 miles · 4 marks'),), '0-7', EV),
    ('(iv)', 4, L(17, '(iv) Name two examples of pyroclastic materials.'),
     S(10, '(iv) · Any two', '(v) · Any valid'), (pair('(iv) · Any two named · 2 + 2 marks', 'Two examples'),),
     '0-7', EV),
    ('(v)', 4, L(17, '(v) Explain briefly why some volcanoes erupt violently.'),
     S(10, '(v) · Any valid', None), (pair('(v) · Any valid explanation · 2 + 2 marks', 'Explanation'),),
     '0-7', EV),
])
WEATHERING = 'the process(es) of physical weathering or the process(es) of chemical weathering'
PART_TWO += [
    T('p2-3b', P2, '3B', '', 30, 17, L(17, 'Weathering'),
      (L(17, 'Explain the process(es) of physical weathering or the process(es) of chemical weathering.'),),
      (S(11, 'Process named', 'C. · Earthquakes'),),
      (fixed('Process named', 2, 'Process named · 2 marks'), srp('Explanation', 14, f'Explanation · 14 x {SRPS}')),
      '0-8', RW, ID + 'p2-q3b-physical-weathering',
      routes=(Route('physical-weathering', 'Physical weathering', ID + 'p2-q3b-physical-weathering', False,
                    ((WEATHERING, 'physical weathering'),)),
              Route('chemical-weathering', 'Chemical weathering', ID + 'p2-q3b-chemical-weathering', False,
                    ((WEATHERING, 'chemical weathering'),)))),
    T('p2-3c', P2, '3C', '', 30, 17, L(17, 'Earthquakes and Volcanoes'),
      (L(17, 'Explain how the occurrence of earthquakes and volcanic eruptions can be monitored',
         'and predicted.'),),
      (S(11, 'Explanation · 15', None),), (srp('Explanation', 15, f'Explanation · 15 x {SRPS}'),),
      '0-7', EV, ID + 'p2-q3c'),
    T('p2-4a', P2, '4A', '', 20, 18, L(18, 'European Region'),
      (L(18, 'Draw an outline map of a European region (not in Ireland) that you have studied.',
         'Two named urban centres in the region.'),),
      (S(12, 'Map outline', None),),
      sketch('Map outline · 4 marks graded (4/2/0)', (0, 2, 4),
             ('4 features @ · 4 marks each:', 'Shown · 2 marks graded (2/1/0)', 'Named · 2 marks'),
             sums((0, 1, 2), (0, 2)), 4),
      '1-5', EURO, ID + 'p2-q4a',
      row_labels=(None, L(18, 'A named feature of relief in the region'), L(18, 'A named river in the region'),
                  L(18, 'Two named urban centres in the region.'), L(18, 'Two named urban centres in the region.'))),
    T('p2-4b', P2, '4B', '', 30, 18, L(18, 'Secondary Economic Activity in Ireland'),
      (L(18, 'Examine the factors that influence the development of secondary economic activity',
         'that you have studied.'),),
      (S(13, 'Named example of secondary', 'C. · Concept'),),
      (fixed('Named example of secondary economic activity', 2,
             'Named example of secondary economic activity · 2 marks'),
       pair('Factors named · 2 + 2 marks', 'Factors named'), srp('Examination', 12, f'Examination · 12 x {SRPS}')),
      '1-4', IRL, ID + 'p2-q4b'),
    T('p2-4c', P2, '4C', '', 30, 18, L(18, 'Concept of a Region'),
      (L(18, 'Examine how socio-economic factors can be used to define regions', 'that you have studied.'),),
      (S(13, 'Socio-economic factors named', None),),
      (pair('Socio-economic factors named · 2 + 2 marks', 'Socio-economic factors named'),
       pair('Examples of regions named · 2 + 2 marks', 'Examples of regions named'),
       srp('Examination', 11, f'Examination · 11 x {SRPS}')),
      '1-0', IRL + EURO + CONT, ID + 'p2-q4c'),
]
Q5AS = (L(19, 'Examine the graph above and answer the following questions.'),)
Q5A4 = L(19, '(iv) Which region had a disposable income per person above the State average in',
         'both 2008 and 2009?')
PART_TWO += romans('5A', P2, 19, L(19, 'Disposable Income of Irish Regions'), Q5AS, ID + 'p2-q5a', ('page',), [
    ('(i)', 4, L(19, '(i) How many regions had a disposable income per person below the State average', 'in 2008?'),
     S(14, '(i) · Six', '(ii) · Border'), (fixed('Number of regions', 4, '(i) · Six · 4 marks'),), '2-0', TG),
    ('(ii)', 4, L(19, '(ii) Which region had a disposable income per person 10% below the State average',
                  'in 2008?'),
     S(14, '(ii) · Border', '(iii) · Mid East'), (fixed('Region', 4, '(ii) · Border/Midland · 4 marks'),), '2-0', TG),
    ('(iii)', 4, L(19, '(iii) Which region', 'in both 2008 and 2009?'),
     S(14, '(iii) · Mid East', '(iv) · Dublin'), (fixed('Region', 4, '(iii) · Mid East · 4 marks'),), '2-0', TG),
    ('(iv)', 4, Q5A4, S(14, '(iv) · Dublin', '(v) · Any valid'), (fixed('Region', 4, '(iv) · Dublin · 4 marks'),),
     '2-0', TG),
    ('(v)', 4, L(19, '(v) Explain briefly why this region had', 'in both 2008 and 2009.'),
     S(14, '(v) · Any valid', None), (pair('(v) · Any valid explanation · 2 + 2 marks', 'Explanation'),),
     '1-4', IRL, (), (Q5A4,)),
])
PART_TWO += [
    T('p2-5b', P2, '5B', '', 30, 19, L(19, 'Agriculture in a Continental / Sub-Continental Region'),
      (L(19, 'Explain the development of agriculture in a Continental / Sub-Continental region', 'Relief.'),),
      (S(15, 'Discussion of Factor 1', 'C. · Population'),),
      (srp('Discussion of Factor 1', 8, f'Discussion of Factor 1 · 8 x {SRPS}'),
       srp('Discussion of Factor 2', 7, f'Discussion of Factor 2 · 7 x {SRPS}')),
      '1-6', CONT, ID + 'p2-q5b', absorbs=pool(ID + 'p2-q5b-', ('Soils', 'Markets', 'Relief.'), 2)[1]),
    T('p2-5c', P2, '5C', '', 30, 19, L(19, 'Population in a European Region'),
      (L(19, 'Account for the distribution of population throughout a European region', 'that you have studied.'),),
      (S(15, 'Examination · 15', None),), (srp('Examination', 15, f'Examination · 15 x {SRPS}'),),
      '1-5', EURO + POP, ID + 'p2-q5c'),
]
Q6AS = (L(20, 'Examine the table above and answer the following questions.'),)
PART_TWO += romans('6A', P2, 20, L(20, 'Tourism and Travel'), Q6AS, ID + 'p2-q6a', ('page',), [
    ('(i)', 4, L(20, '(i) How many overseas visitors came to Ireland in 2009?'),
     S(16, '(i) · 6,928,000', '(ii) · 2007'), (fixed('Number of visitors', 4, '(i) · 6,928,000 · 4 marks'),),
     '2-0', TG),
    ('(ii)', 4, L(20, '(ii) In which years did the number of overseas visitors to Ireland exceed the number',
                  'of visits abroad by Irish residents?'),
     S(16, '(ii) · 2007', '(iii) · 212'), (pair('(ii) · 2007 & 2011 · 2 + 2 marks', 'Two years'),), '2-0', TG),
    ('(iii)', 4, L(20, '(iii) Calculate the difference between the number of overseas visitors to Ireland and',
                   'Irish residents in 2011.'),
     S(16, '(iii) · 212', '(iv) · Any valid'), (fixed('Difference', 4, '(iii) · 212,000 · 4 marks'),), '2-0', TG),
    ('(iv)', 4, L(20, '(iv) Explain briefly one advantage of tourism to the Irish economy.'),
     S(16, '(iv) · Any valid', '(v) · Any valid'), (pair('(iv) · Any valid explanation · 2 + 2 marks', 'Advantage'),),
     '1-4', IRL),
    ('(v)', 4, L(20, '(v) Explain briefly why, after a steady decrease from 2007 to 2010, there was an',
                 'between 2010 and 2011.'),
     S(16, '(v) · Any valid', None), (pair('(v) · Any valid explanation · 2 + 2 marks', 'Explanation'),),
     '1-4', IRL),
])
PART_TWO += [
    T('p2-6b', P2, '6B', '', 30, 20, L(20, 'Urban Area in a Continental / Sub-Continental Region'),
      (L(20, 'With reference to one urban area in a Continental / Sub-Continental region',
         'at its present location.'),),
      (S(17, 'Urban area named', 'C. · Economic'),),
      (fixed('Urban area named', 2, 'Urban area named · 2 marks'), pair('Reasons Stated · 2 + 2 marks', 'Reasons stated'),
       srp('Examination', 12, f'Examination · 12 x {SRPS}')),
      '1-6', CONT + URB, ID + 'p2-q6b'),
    T('p2-6c', P2, '6C', '', 30, 20, L(20, 'Economic, Political and Cultural Activities'),
      (L(20, 'Examine the interaction between economic, political and/or cultural activities',
         'that you have studied.'),),
      (S(17, 'Examination · 15', None),), (srp('Examination', 15, f'Examination · 15 x {SRPS}'),),
      '1-3', IRL + EURO + CONT, ID + 'p2-q6c'),
]

Q7AT = L(22, 'International Trade')
Q7AS = (L(22, 'Examine the table above and answer the following questions.'),)
PART_TWO += romans('7A', P2, 22, Q7AT, Q7AS, ID + 'p2-q7a', ('page',), [
    ('(i)', 4, L(22, '(i) Which of the selected countries above had the highest value of imports and',
                 'in both 2009 and 2010?'),
     S(19, '(i) · Germany', '(ii) · Italy'), (fixed('Country', 4, '(i) · Germany · 4 marks'),), '2-0', TG),
    ('(ii)', 4, L(22, '(ii) Which of the selected countries above received the lowest value of exports from',
                  'in both 2009 and 2010?'),
     S(19, '(ii) · Italy', '(iii) · €17'), (fixed('Country', 4, '(ii) · Italy · 4 marks'),), '2-0', TG),
    ('(iii)', 4, L(22, '(iii) Calculate X, the total value of exports from Ireland to the selected EU countries',
                   'in 2010.'),
     S(19, '(iii) · €17', '(iv) · 15.8'), (fixed('X', 4, '(iii) · €17,781.8 million · 4 marks'),), '2-0', TG),
    ('(iv)', 4, L(22, '(iv) Calculate the percentage decrease in imports from Italy between 2009 and 2010.'),
     S(19, '(iv) · 15.8', '(v) · Any valid'), (fixed('Percentage decrease', 4, '(iv) · 15.8 - 16 · 4 marks'),),
     '2-0', TG),
])
PART_TWO += [
    T('p2-7a-v', P2, '7A', '(v)', 4, 22, Q7AT,
      (L(22, '(v) Explain briefly one of the following:', 'Balance of Payments.'),),
      (S(19, '(v) · Any valid', None),), (pair('(v) · Any valid explanation · 2 + 2 marks', 'Explanation'),),
      '3-0', ECON, ID + 'p2-q7a-v-balance-of-trade', ('page',), Q7AS,
      routes=bullet_routes('p2-q7a-v-', ('Balance of Trade', 'Balance of Payments.'))),
    T('p2-7b', P2, '7B', '', 30, 22, L(22, 'Tertiary Economic Activity'),
      (L(22, 'Using evidence from the 1:50000 Ordnance Survey map accompanying this paper,',
         'Services (excluding transport).'),),
      (S(20, '3 headings', 'C. · European'),),
      tuple(Criterion(f'Heading {n}', 10, evens(10), 'srp',
                      ('3 headings @ 10 marks each', 'For each Heading:', 'Map evidence · 2 marks',
                       f'Discussion · 4 x {SRPS}')) for n in (1, 2, 3)),
      '3-0', ECON + MAP, ID + 'p2-q7b', ('map', 'legend'),
      row_labels=(L(22, 'Accessibility'), L(22, 'Attractions'), L(22, 'Services (excluding transport).'))),
    T('p2-7c', P2, '7C', '', 30, 22, L(22, 'European Union', nth=0),
      (L(22, 'Examine the impact of membership of the European Union on the Irish economy.'),),
      (S(20, 'Impact Identified', None),),
      (fixed('Impact identified', 2, 'Impact Identified · 2 marks'), srp('Examination', 14, f'Examination · 14 x {SRPS}')),
      '3-3', EU_ECON + IRL, ID + 'p2-q7c'),
    T('p2-8a', P2, '8A', '', 20, 23, L(23, 'Aerial Photograph'),
      (L(23, 'Examine the aerial photograph of Enniscorthy accompanying this paper.',
         'in the centre of the aerial photograph.'),),
      (S(21, 'Sketch Outline:', None),),
      sketch('Sketch Outline: · 4 marks', (0, 4),
             ('4 features @ 4 marks each: · Shown 3 marks (graded 3/1/0)', 'Named 1 mark'), SHOWN3, 4),
      '2-8', AER + ECON, ID + 'p2-q8a', ('aerial',),
      row_labels=(None, L(23, 'The railway bridge'), L(23, 'Two connecting streets'), L(23, 'The river'),
                  L(23, 'The grain storage area in the centre of the aerial photograph.'))),
    T('p2-8b', P2, '8B', '', 30, 23, L(23, 'Environmental Impact'),
      (L(23, 'Examine the environmental impact of burning fossil fuels.'),),
      (S(22, 'Environmental Impact identified', 'C. · Economic'),),
      (fixed('Environmental impact identified', 2, 'Environmental Impact identified · 2 marks'),
       srp('Examination', 14, f'Examination · 14 x {SRPS}')),
      '3-4', ENV + ENERGY, ID + 'p2-q8b'),
    T('p2-8c', P2, '8C', '', 30, 23, L(23, 'Economic Development'),
      (L(23, 'With reference to a developed economy that you have studied, examine the factors that',
         'influence its level of economic development.'),),
      (S(22, 'Developed economy named', None),),
      (fixed('Developed economy named', 2, 'Developed economy named · 2 marks'),
       pair('Factors · 2 + 2 marks', 'Factors'), srp('Examination', 12, 'Examination · 12 x SRPS')),
      '3-0', ECON, ID + 'p2-q8c'),
]
Q9AS = (L(24, 'Examine the data in the table above showing oil production in 2011.'),)
PART_TWO += romans('9A', P2, 24, L(24, 'Oil Production', nth=0), Q9AS, ID + 'p2-q9a', ('page',), [
    ('(i)', 16, L(24, '(i) Using graph paper, draw a suitable graph to illustrate this data.'),
     S(23, 'Bar Chart · Pie Chart', '(ii) · Explain briefly'), GRAPH, '2-0', TG),
    ('(ii)', 4, L(24, '(ii) Explain briefly the term fossil fuel.'),
     S(23, 'Any valid explanation', None), (pair('Any valid explanation 2 + 2 marks.', 'Explanation'),),
     '3-5', ENERGY),
])
PART_TWO += [
    T('p2-9b', P2, '9B', '', 30, 24, L(24, 'Developing Economy'),
      (L(24, 'Examine the impact of globalisation on a developing economy that you have studied.'),),
      (S(24, 'Developing economy named', 'C. · Multinational'),),
      (fixed('Developing economy named', 2, 'Developing economy named · 2 marks'),
       fixed('Impact identified', 2, 'Impact identified · 2 marks'), srp('Examination', 13, f'Examination · 13 x {SRPS}')),
      '3-1', DEV + MNC, ID + 'p2-q9b'),
    T('p2-9c', P2, '9C', '', 30, 24, L(24, 'Multinational Company (MNC)'),
      (L(24, 'Examine the factors that influence the global distribution of one multinational company',
         'that you have studied.'),),
      (S(24, 'MNC named', None),),
      (fixed('MNC named', 2, 'MNC named · 2 marks'), pair('Factors named · 2 + 2 marks', 'Factors named'),
       fixed('Reference to two global locations', 2, 'Reference to two global locations · 2 marks'),
       srp('Examination', 11, 'Examination · 11 SRPs')),
      '3-2', MNC, ID + 'p2-q9c'),
]
Q10AS = (L(25, 'Examine the table above and answer the following questions.'),)
PART_TWO += romans('10A', P2, 25, L(25, 'Urban Growth'), Q10AS, ID + 'p2-q10a', ('page',), [
    ('(i)', 4, L(25, '(i) Calculate the increase in the total population of Newcastle, between 2006 and', '2011.'),
     S(25, '(i) · 1,153', '(ii) · 101'), (fixed('Increase', 4, '(i) · 1,153 · 4 marks'),), '2-0', TG),
    ('(ii)', 4, L(25, '(ii) Calculate X, the percentage change in Courtown Harbour', '2006 and 2011.'),
     S(25, '(ii) · 101', '(iii) · Any 2'), (fixed('X', 4, '(ii) · 101 · 4 marks'),), '2-0', TG),
    ('(iii)', 4, L(25, '(iii) State two reasons for the rapid growth of towns in South Dublin, between 2006',
                   'and 2011.'),
     S(25, '(iii) · Any 2', '(iv) · Any valid'), (pair('(iii) · Any 2 reasons stated · 2 + 2 marks', 'Two reasons'),),
     '4-5', URB),
    ('(iv)', 4, L(25, '(iv) Explain briefly one problem caused by the rapid growth of Irish towns.'),
     S(25, '(iv) · Any valid', '(v) · Any valid'), (pair('(iv) · Any valid explanation · 2 + 2 marks', 'Problem'),),
     '4-5', URB),
    ('(v)', 4, L(25, '(v) Explain briefly one reason why the Census of Population is important for urban',
                 'planning.'),
     S(25, '(v) · Any valid', None), (pair('(v) · Any valid explanation · 2 + 2 marks', 'Reason'),),
     '4-4', URB + POP),
])
PATTERN_10B = ('Three patterns @ 10 marks each', 'For each pattern:', 'Pattern named · 2 marks',
               'Map reference/evidence · 2 marks', f'Examination · 3 x {SRPS}')
PART_TWO += [
    T('p2-10b', P2, '10B', '', 30, 25, L(25, 'Rural Settlement Patterns'),
      (L(25, 'With reference to the 1:50000 Ordnance Survey map accompanying this paper, describe',
         'evident on the map.'),),
      (S(26, 'Three patterns', 'C. · Patterns'),),
      tuple(Criterion(f'Pattern {n}', 10, evens(10), 'srp', PATTERN_10B) for n in (1, 2, 3)),
      '4-3', URB + MAP, ID + 'p2-q10b', ('map', 'legend')),
    T('p2-10c', P2, '10C', '', 30, 25, L(25, 'Patterns of Migration'),
      (L(25, 'Describe and explain changes in the patterns of migration into and out of Ireland since',
         'the 1950s.'),),
      (S(26, 'Changing patterns identified into', None),),
      (fixed('Changing patterns identified into Ireland', 2, 'Changing patterns identified into Ireland · 2 marks'),
       fixed('Changing patterns identified out of Ireland', 2,
             'Changing patterns identified out of Ireland · 2 marks'),
       srp('Examination', 13, f'Examination · 13 x {SRPS}')),
      '4-2', POP, ID + 'p2-q10c'),
    T('p2-11a', P2, '11A', '', 20, 26, L(26, 'Map Skills'),
      (L(26, 'Examine the 1:2000 map of Enniscorthy shown above.', 'The Car Park.'),),
      (S(27, 'Sketch outline', None),),
      sketch('Sketch outline · 4 marks', (0, 4),
             ('4 features @ 4 marks each: · Shown 3 marks (graded 3/1/0)', 'Named 1 mark'), SHOWN3, 4),
      '2-6', MAP + URB, ID + 'p2-q11a', ('page',),
      row_labels=(None, L(26, 'Two connecting streets'), L(26, 'The Cathedral'), L(26, 'The Market Square'),
                  L(26, 'The Car Park.'))),
    T('p2-11b', P2, '11B', '', 30, 26, L(26, 'Population'),
      (L(26, 'Explain how the development of resources impacts on population change, with reference',
         'to examples that you have studied.'),),
      (S(28, 'Impact named', 'C. · Migration'),),
      (fixed('Impact named', 2, 'Impact named · 2 marks'), pair('Examples · 2 + 2 marks', 'Examples'),
       srp('Examination', 12, f'Examination · 12 x {SRPS}')),
      '4-1', POP, ID + 'p2-q11b'),
    T('p2-11c', P2, '11C', '', 30, 26, L(26, 'Migration'),
      (L(26, 'Examine how ethnic and religious issues can arise as a result of migration, with reference',
         'to example(s) that you have studied.'),),
      (S(28, 'Example named', None),),
      (fixed('Example named', 2, 'Example named · 2 marks'),
       fixed('Religious issue identified', 2, 'Religious issue identified · 2 marks'),
       fixed('Ethnic issue identified', 2, 'Ethnic issue identified · 2 marks'),
       srp('Examination', 12, f'Examination · 12 x {SRPS}')),
      '4-2', POP, ID + 'p2-q11c'),
]
Q12AS = (L(27, 'Examine the data in the table above showing the percentage of the population',
           'in 2001 and 2011.'),)
PART_TWO += romans('12A', P2, 27, L(27, 'Population', nth=0), Q12AS, ID + 'p2-q12a', ('page',), [
    ('(i)', 16, L(27, '(i) Using graph paper, draw a suitable graph to illustrate this data.'),
     S(29, 'Bar Chart · Pie Chart', '(ii) · Explain briefly'), GRAPH, '2-0', TG),
    ('(ii)', 4, L(27, '(ii) Explain briefly the term dependency ratio.'),
     S(29, 'Any valid explanation', None), (pair('Any valid explanation 2 + 2 marks.', 'Explanation'),),
     '4-0', POP),
])
REASON_12B = ('3 reasons @ 10 marks each', 'For each reason:', 'Reason stated · 2 marks',
              'Aerial photograph evidence · 2 marks', f'Examination · 3 x {SRPS}')
ISSUE_12C = ('Two issues @ 8 + 7 SRPs', 'For each issue:', 'Issue named · 2 marks', 'Issue examined · 7/6 x SRPs')
PART_TWO += [
    T('p2-12b', P2, '12B', '', 30, 27, L(27, 'Urban Development'),
      (L(27, 'With reference to the aerial photograph that accompanies this paper,', 'the town of Enniscorthy.'),),
      (S(30, '3 reasons', 'C. · Future'),),
      tuple(Criterion(f'Reason {n}', 10, evens(10), 'srp', REASON_12B) for n in (1, 2, 3)),
      '4-3', URB + AER, ID + 'p2-q12b', ('aerial',)),
    T('p2-12c', P2, '12C', '', 30, 27, L(27, 'Future Urbanisation'),
      (L(27, 'Discuss two issues facing cities in the future in the developed world.'),),
      (S(30, 'Two issues', None),),
      (Criterion('Issue 1 (8 SRPs)', 16, evens(16), 'srp', ISSUE_12C),
       Criterion('Issue 2 (7 SRPs)', 14, evens(14), 'srp', ISSUE_12C)),
      '4-5', URB, ID + 'p2-q12c'),
]

# ------------------------------------------------------------------ Options --
# Each option prints two schemes, chosen by the number of aspects discussed:
# 3 @ 27 + 27 + 26 or 4 @ 20 (identifying 4 marks, discussion 8 or 6 SRPs and
# coherence 7/6 or 4 marks graded inside each aspect).
ASPECT_LINES = ('Number of aspects:', 'Identifying aspect:', 'Discussion:', 'Overall coherence:')
# Either printed scheme gives the discussion 24 SRPs (48 marks) and identifying
# plus coherence 32 marks (3 x 4 + 7 + 7 + 6, or 4 x (4 + 4)), as in 2012.
OPTION_CRITERIA = (
    Criterion('Aspects identified and overall coherence (3 aspects: 4 + 7/6 marks each; 4 aspects: 4 + 4 marks each)',
              32, upto(32), 'exact', ('Number of aspects', 'Identifying aspect', 'Overall coherence')),
    Criterion('Discussion (3 aspects @ 8 x SRPs or 4 aspects @ 6 x SRPs)', 48, evens(48), 'srp', ('Discussion:',)),
)
THREE_FACTORS = (Criterion('Factor 1', 27, upto(27), 'srp', ASPECT_LINES),
                 Criterion('Factor 2', 27, upto(27), 'srp', ASPECT_LINES),
                 Criterion('Factor 3', 26, upto(26), 'srp', ASPECT_LINES))
FOUR_ASPECTS = tuple(Criterion(f'Aspect {n}', 20, upto(20), 'srp', ASPECT_LINES) for n in (1, 2, 3, 4))


def option(q, page, theme, note_nth, prompt, scheme_page, topic, atlas, after=None, end=None,
           criteria=OPTION_CRITERIA, absorbs=()):
    return T(f'p2-{q}', P2, q, '', 80, page, theme, prompt if isinstance(prompt, tuple) else (prompt,),
             (S(scheme_page, 'Number of aspects', end, None, after),), criteria,
             topic, (atlas,), ID + f'p2-q{q}',
             stem=(L(page, 'Note: It is better to discuss three or four aspects', 'large number of points.',
                     nth=note_nth),), absorbs=absorbs)


GI, GE = H + 'option-global-interdependence', H + 'option-geoecology'
CI, AO = H + 'option-culture-identity', H + 'option-atmosphere-ocean'
SOIL = ('Mineral matter', 'Air', 'Water', 'Organic matter.')
OPTIONS = [
    option('13', 29, L(29, 'Global Interdependence'), 0,
           L(29, 'Discuss why sustainable development is important for the future.'), 32, '5-3', GI,
           after='13.', end='14.'),
    option('14', 29, L(29, 'Global Interdependence'), 0,
           L(29, 'Examine the impact of global trading patterns in relation to both producer and',
             'that you have studied.'), 32, '5-1', GI, after='14.'),
    option('15', 29, L(29, 'Global Interdependence'), 0,
           L(29, 'Discuss the arguments for and against international aid.'), 33, '5-2', GI),
    option('16', 29, L(29, 'Geoecology'), 1,
           L(29, 'Examine how desertification and conservation have impacted on soil characteristics.'),
           34, '6-1', GE, after='16.', end='17.'),
    option('17', 29, L(29, 'Geoecology'), 1,
           L(29, 'With reference to one biome that you have studied, account for the type of climate',
             'within the biome.'), 34, '6-2', GE, after='17.'),
    option('18', 29, L(29, 'Geoecology'), 1,
           L(29, 'Discuss how soil development is influenced by any three of the following factors:',
             'Organic matter.'), 35, '6-0', GE,
           criteria=THREE_FACTORS, absorbs=pool(ID + 'p2-q18-', SOIL, 3)[1]),
    option('19', 30, L(30, 'Culture and Identity'), 0,
           L(30, 'Many cultural groups do not have a nation state of their own.', 'Discuss.'), 36, '7-1', CI,
           after='19.', end='20.'),
    option('20', 30, L(30, 'Culture and Identity'), 0,
           L(30, 'Examine how people express their culture and identity in everyday life.'), 36, '7-2', CI,
           after='20.'),
    option('21', 30, L(30, 'Culture and Identity'), 0,
           L(30, 'Identity as a concept entails a variety of cultural factors.', 'that you have studied.'),
           37, '7-2', CI),
    option('22', 30, L(30, 'The Atmosphere - Ocean Environment'), 1,
           L(30, 'Examine how circulation patterns in the atmosphere and/or the oceans affect',
             'at the earth’s surface.'), 38, '8-3', AO, after='22.', end='23.'),
    option('23', 30, L(30, 'The Atmosphere - Ocean Environment'), 1,
           L(30, 'Examine one climate type that you have studied.'), 38, '8-4', AO, after='23.'),
    option('24', 30, L(30, 'The Atmosphere - Ocean Environment'), 1,
           L(30, 'Give an account of how atmosphere-ocean phenomena are measured and examine the', 'humidity.'),
           39, '8-0', AO, criteria=FOUR_ASPECTS),
]

TASKS = [*PART_ONE, *PART_TWO, *OPTIONS]

ID_CORRECTION_REASON = 'No 2013 Higher card shipped before this review; every card is new.'

# No 2013 Higher card was live on origin/main before this review.
LEGACY_IDS: list[str] = []
