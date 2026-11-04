"""Independent review ledger: Leaving Certificate Geography 2016 Higher Level.

Sources (English editions, harvested Paper Trail corpus; sizes and SHA-256
pinned in EXPECTED_SOURCES and the generated audit): the examination paper
LC005ALP000EV (32 pages; one booklet printed Part One, answered in it, and
Part Two), marking scheme LC005ALP000EV (48 pages), and the common Westport
companions as Paper Trail files them — the 1:50 000 map LC005CLP003EV (a
one-page PDF holding a 1135 x 783 pixel image: legible at full size, but
lower resolution than later years), its legend LC005CLPC00EV and the aerial
photograph LC005CLP004EV (one-page PDFs). Part One is 80 marks (any ten of
twelve @ 8), Part Two 320 (four questions @ 80).

Visual sweep (every page rendered and read on 2026-10-14):
  Paper p1 cover and examiner's grid; p2-p12 Part One Questions 1-12 (p6
  holds Q5 and Q6; Q7 prints an elevation profile, Q8 a street map of
  Westport, Q9 four weather charts and four cloud charts); p13 Part Two
  instructions; p14 Section 1 divider; p15-p20 Q1-Q6 (p15 and p18 open
  with their dividers); p21 Section 2 divider; p22-p27 Electives Q7-Q12
  (p22 and p25 open with their elective dividers); p28 Section 3 divider
  and option note; p29-p30 Options Q13-Q24; p31-p32 printed "Blank Page".
  Scheme p1 cover; p2-p3 notes; p4 Part One table (two columns: Q1-Q6,
  Q7-Q12; Q4, Q5 and Q7 print two answers to a row); p5 Part Two
  instructions and Section 1 divider; p6-p12 Q1-Q3; p13-p18 Q4-Q6; p19
  Section 2 divider; p20-p25 Q7-Q9; p26-p31 Q10-Q12; p32 Section 3 divider;
  p33 option outline and Overall Coherence descriptors; p34-p41 Q13-Q24;
  p42-p44 Geographical Investigation (coursework) and its presentation
  marks; p45 investigation topics; p46 Irish-language bonus marks; p47
  printed "Blank Page"; p48 back cover.
  Companions: Westport map extract (Westport Bay, the Owenwee River,
  Kinlooey Lough, the Croagh Patrick Heritage Trail); OS legend sheet;
  oblique aerial photograph of Westport.

Boundaries and tariffs follow the 2017 Higher ledger. Matching tables, in
the printed row order: Q1 Continental crust E, Oceanic trench D, Mountain
range F, Oceanic crust B, Subduction zone A, Magma chamber C; Q2
Pyroclastic flow B, Lava fissure eruption C, Ash cloud D, Lava vent
eruption A; Q3 Joint B, Wave-cut platform C, Rock fall A, Sea cave F,
Headland E, Bedding plane D; Q4(i) Sandstone Sand/Quartzite, Limestone
Shells etc./Marble, Granite Magma/Gneiss; Q5 L 95 78 Cut Off meander
Fluvial, L 93 78 V-shaped valley Fluvial, L 94 83 Lagoon Coastal, L 92 85
Drumlin Glacial; Q7 R335 D Cultural, Owenwee River A Physical, Conical
Peak B Physical, Waymarked Walk C Cultural; Q8 B Left middleground/Left
centre, C Centre middleground, D Centre middleground, E Right
middleground/Right centre (A is printed); Q9 (i) D, (ii) A, (iii) C, (iv)
B. Q4, Q5 and Q7 answer (i) and (ii) in one table and the scheme prices
each printed row with both its answers, so each is one card of four (Q4
three) two-mark rows. Lettered statements priced on their own are tasks
(Q2(ii)(a)-(b), Q4(ii)(a)-(b)).

Printed choices: 2B (i) or (ii) and 5C's culture or the physical landscape
are one route per printed option. 4C, 5B, 6C and 9B (two of the printed
factors) and option 18 (three of four) are pools, one card each. Option 18
prints only the "3 @ 20 marks each" outline and is carded with it.
"""

from geography_review import (
    Criterion, Lift, Route, SchemeSlice, Task, pool, evens, fixed, slug, srp, sums, upto,
)

YEAR = 2016
LEVEL = 'higher'
PAPER_PAGES = {1: 32, 2: 32}
SCHEME_PAGES = 48
QUESTION_TARIFFS = {1: {str(n): 8 for n in range(1, 13)},
                    2: {**{f'{n}{x}': (20 if x == 'A' else 30)
                           for n in range(1, 13) for x in 'ABC'},
                        **{str(n): 80 for n in range(13, 25)}}}

EXPECTED_SOURCES = {
    'paper1': ('LC005ALP000EV.pdf', 2378315),
    'paper2': ('LC005ALP000EV.pdf', 2378315),
    'scheme': ('LC005ALP000EV.pdf', 1250063),
    'map': ('LC005CLP003EV.pdf', 327650),
    'legend': ('LC005CLPC00EV.pdf', 745443),
    'aerial': ('LC005CLP004EV.pdf', 5761875),
}

_PAPER = {1: 'cover and examiner grid', **{p: 'question' for p in range(2, 13)},
          13: 'Part Two instructions', 14: 'section divider', **{p: 'question' for p in range(15, 21)},
          21: 'section divider', **{p: 'question' for p in range(22, 28)}, 28: 'section divider and option note',
          29: 'question', 30: 'question', 31: 'blank page', 32: 'blank page'}
PAGE_REVIEW = {
    # One booklet printed both parts.
    'paper1': _PAPER, 'paper2': _PAPER,
    'scheme': {1: 'cover', 2: 'notes', 3: 'notes', 4: 'Part One table', 5: 'Part Two instructions',
               **{p: 'Part Two allocation' for p in range(6, 19)}, 19: 'section divider',
               **{p: 'Part Two allocation' for p in range(20, 32)}, 32: 'section divider',
               33: 'option outline and coherence descriptors',
               **{p: 'option allocation' for p in range(34, 42)},
               **{p: 'geographical investigation (coursework)' for p in range(42, 45)},
               45: 'investigation topics', 46: 'Irish-language bonus marks', 47: 'blank', 48: 'back cover'},
}

EXPECTED_SELECTION_SCAN = [
    [1, 2, 'attempt any ten'], [1, 13, 'attempt four'], [1, 14, 'attempt two'], [1, 15, 'attempt one'],
    [1, 16, 'answer (i) or (ii)'], [1, 16, 'any one'], [1, 16, 'any one'],
    [1, 18, 'attempt one'], [1, 18, 'any two'],
    [1, 19, 'any two'],
    [1, 20, 'any two'], [1, 20, 'two of the following'],
    [1, 21, 'attempt one'],
    [1, 22, 'any one'],
    [1, 24, 'two of the following'],
    [1, 28, 'attempt one'],
    [1, 29, 'any one'], [1, 29, 'any three'],
]
SELECTION_REVIEW = [
    {'scan': [[1, 2, 'attempt any ten'], [1, 13, 'attempt four'], [1, 14, 'attempt two'], [1, 15, 'attempt one'],
              [1, 18, 'attempt one'], [1, 21, 'attempt one'], [1, 28, 'attempt one']],
     'kind': 'exam-attempt-rule',
     'reason': 'Part One any ten of twelve and Part Two four questions (one of Q1-3, one of Q4-6, one elective, one option) are attempt rules; every question is carded.'},
    {'scan': [[1, 16, 'answer (i) or (ii)']], 'kind': 'closed-route',
     'reason': '2B: (i) or (ii) -> 2 routes. 5C "culture or the physical landscape" -> 2 routes (no directive word the scan reads; the route text is anchored on the paper).'},
    {'scan': [[1, 18, 'any two'], [1, 19, 'any two'], [1, 20, 'two of the following'], [1, 24, 'two of the following'],
              [1, 29, 'any three']],
     'kind': 'choose-n-one-card',
     'reason': '4C any two of four printed factors, 5B any two of three printed factors, 6C two of three printed factors, 9B two of four printed factors, option 18 any three of four printed characteristics -> one card each with every printed item (choice is not a route).'},
    {'scan': [[1, 16, 'any one'], [1, 16, 'any one'], [1, 20, 'any two'], [1, 22, 'any one'], [1, 29, 'any one']],
     'kind': 'open-response',
     'reason': 'No printed pool: 2B(i) any one landform, 2B(ii) any one mass movement process, 6B any two contrasting European regions, 7B any one multinational company, option 16 any one soil type. Compulsory lists stay whole: 1A, 4A, 7A, 8C and 11A each item.'},
]

P1, P2 = 1, 2
LEFT = (0.0, 0.0, 0.495, 1.0)
RIGHT = (0.495, 0.0, 1.0, 1.0)
ID = 'geography-2016-hl-'
H = 'geography-higher-'
SRPS = 'SRP’s'


def L(page, start, end=None, nth=None):
    return Lift(page, start, end, None, nth)


def S(page, start, end=None, clip=None, after=None, table=False):
    return SchemeSlice(page, start, end, clip, after, table)


def T(key, part, q, sub, marks, page, title, prompt, scheme, criteria, topic, atlas, card_id,
      sources=(), stem=(), routes=(), row_labels=(), absorbs=()):
    return Task(key, part, q, sub, marks, page, title, prompt, scheme, criteria, topic, atlas,
                sources, card_id, False, stem=stem, routes=routes, row_labels=row_labels,
                absorbs=absorbs)


def rows(lines, marks=1, permitted=None):
    return tuple(fixed(f'Row {i}', marks, line, permitted) for i, line in enumerate(lines, 1))


def pair(line, label):
    return fixed(label, 4, line, (0, 2, 4))


def one_plus_one(line, label):
    return fixed(label, 2, line, (0, 1, 2))


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


PS = (H + 'plate-tectonics',)
RW = (H + 'rocks-weathering-mass-movement',)
RIVERS = (H + 'rivers',)
SEA = (H + 'the-sea',)
GLAC = (H + 'glaciation',)
EV = (H + 'earthquakes-volcanoes',)
KARST = (H + 'karst-regions',)
MAP = (H + 'mapwork',)
AER = (H + 'aerial-photos',)
TG = (H + 'tablesgraphs-questions',)
WX = (H + 'weather-climate',)
IRL = (H + 'regions-ireland',)
EURO = (H + 'regions-european',)
CONT = (H + 'regions-continental',)
POP = (H + 'human-population',)
URB = (H + 'human-urban-geography',)
LAND = (H + 'urban-land-uses',)
ECON = (H + 'elective-economic',)
DEV = (H + 'economic-developing-economies',)
MNC = (H + 'economic-multinationals-globalisation',)
EU_ECON = (H + 'economic-european-union',)
ENERGY = (H + 'economic-energy',)
ENV = (H + 'economic-environmental-impact',)

# ---------------------------------------------------------------- Part One --
PART_ONE = romans('1', P1, 2, L(2, 'The Tectonic Cycle'),
                  (L(2, 'Examine the diagram above and answer each of the following questions.'),),
                  ID + 'p1-q1', ('page',), [
    ('(i)', 6, L(2, '(i) Match each of the letters A, B, C, D, E and F with the feature that best matches it',
                 'table below.'),
     S(4, 'Q.1 · (i)', '(ii) · True', LEFT),
     rows(['Q.1 · (i) · E 1m', '=D 1m', '=F 1m', '=B 1m', '=A 1m', '=C 1m']), '0-0', PS,
     (L(2, 'Continental crust'), L(2, 'Oceanic trench'), L(2, 'Mountain range'), L(2, 'Oceanic crust'),
      L(2, 'Subduction zone'), L(2, 'Magma chamber'))),
    ('(ii)', 2, (L(2, '(ii) Indicate whether the following statement is true or false, by circling the correct',
                   'option.'),
                 L(2, 'Plutonic igneous rocks are formed at C.')),
     S(4, '(ii) · True', 'Q.2', LEFT), (fixed('True or false', 2, '(ii) · True 2m'),), '0-0', PS + RW),
])
TF2 = L(3, '(ii) Indicate whether each of the following statements is true or false, by circling the',
        'correct option in each case.')
PART_ONE += romans('2', P1, 3, L(3, 'Volcanic Activity'),
                   (L(3, 'Examine the photographs above and answer each of the following questions.'),),
                   ID + 'p1-q2', ('page',), [
    ('(i)', 4, L(3, '(i) Match each of the photographs A, B, C and D with the feature or process',
                 'table below.'),
     S(4, 'Q.2 (i)', '(ii) · (a) False', LEFT), rows(['Q.2 (i) · B 1m', '=C 1m', '=D 1m', '=A 1m']), '0-7', EV,
     (L(3, 'Pyroclastic flow'), L(3, 'Lava fissure eruption'), L(3, 'Ash cloud'), L(3, 'Lava vent eruption'))),
    ('(ii)(a)', 2, (TF2, L(3, '(a) Basic lava has a very high silica content.')),
     S(4, '(ii) · (a) False', '(b) True', LEFT), (fixed('Statement (a)', 2, '(ii) · (a) False 2m'),), '0-7', EV),
    ('(ii)(b)', 2, (TF2, L(3, '(b) Lava with a high silica content is most associated with explosive eruptions.')),
     S(4, '(b) True', 'Q.3', LEFT), (fixed('Statement (b)', 2, '(b) True 2m'),), '0-7', EV),
])
PART_ONE += romans('3', P1, 4, L(4, 'Coastal Landforms and Rock Structures'),
                   (L(4, 'Examine the photograph above and answer each of the following questions.'),),
                   ID + 'p1-q3', ('page',), [
    ('(i)', 6, L(4, '(i) Match each of the letters A, B, C, D, E and F with the coastal landform or rock',
                 'table below.'),
     S(4, 'Q.3 (i)', '(ii) · False', LEFT),
     rows(['Q.3 (i) · B 1m', '=C 1m', '=A 1m', '=F 1m', '=E 1m', '=D 1m']), '0-10', SEA,
     (L(4, 'Joint'), L(4, 'Wave-cut platform'), L(4, 'Rock fall'), L(4, 'Sea cave'), L(4, 'Headland'),
      L(4, 'Bedding plane'))),
    ('(ii)', 2, (L(4, '(ii) Indicate whether the following statement is true or false by circling the correct',
                   'option.'),
                 L(4, 'Rock structures such as joints and bedding planes are most associated with igneous rocks.')),
     S(4, '(ii) · False', 'Q.4', LEFT), (fixed('True or false', 2, '(ii) · False 2m'),), '0-1', RW),
])
Q4II = L(5, '(ii) Name the rocks most associated with each of the following Irish locations.')
PART_ONE += romans('4', P1, 5, L(5, 'Rocks'), (), ID + 'p1-q4', ('page',), [
    ('(i)', 6, (L(5, '(i) The list below contains a number of source materials from which rocks are formed',
                  'metamorphic rocks.'),
                Lift(5, 'Sand · Marble', 'Magma · Quartzite', row=True),
                L(5, 'Complete the table below by inserting the correct terms from the list',
                  'the metamorphic rock most associated with it.')),
     S(4, 'Q.4 (i)', '(ii) · (a) Basalt', LEFT),
     rows(['Q.4 (i) · Sand 1m Quartzite 1m', 'Shells etc. 1m Marble 1m', 'Magma 1m Gneiss 1m'], 2, (0, 1, 2)),
     '0-1', RW, (L(5, 'Sandstone'), L(5, 'Limestone'), L(5, 'Granite'))),
    ('(ii)(a)', 1, (Q4II, L(5, '(a) The Antrim Plateau')),
     S(4, '(ii) · (a) Basalt', '(b) Limestone', LEFT), (fixed('Rock', 1, '(ii) · (a) Basalt 1m'),), '0-1', RW),
    ('(ii)(b)', 1, (Q4II, L(5, '(b) The Burren')),
     S(4, '(b) Limestone', 'Q.5', LEFT), (fixed('Rock', 1, '(b) Limestone 1m'),), '0-1', RW + KARST),
])
PART_ONE.append(T(
    'p1-5', P1, '5', '', 8, 6, L(6, 'Landforms'),
    (L(6, '(i) Match each of the following landforms with the grid reference that best matches', 'Lagoon.'),
     L(6, '(ii) Indicate whether glacial processes or fluvial processes or coastal processes are',
       'the table below.')),
    (S(4, 'Q.5', 'Q.6', LEFT),),
    rows(['Q.5 Cut Off meander 1m Fluvial 1m', 'V-shaped valley 1m Fluvial 1m', 'Lagoon 1m Coastal 1m',
          'Drumlin 1m Glacial 1m'], 2, (0, 1, 2)),
    '2-6', MAP + RIVERS + SEA + GLAC, ID + 'p1-q5', ('map', 'legend'),
    (L(6, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper and answer each of the '
          'following questions in the table below.'),),
    row_labels=(L(6, 'L 95 78'), L(6, 'L 93 78'), L(6, 'L 94 83'), L(6, 'L 92 85'))))
PART_ONE += romans('6', P1, 6, L(6, 'Ordnance Survey Map'),
                   (L(6, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper and answer '
                         'each of the following questions.'),),
                   ID + 'p1-q6', ('map', 'legend'), [
    ('(i)', 2, L(6, '(i) Calculate the approximate area, in square kilometres, of Westport Bay',
                 'west of easting 95.'),
     S(4, 'Q.6 (i)', '(ii) · North West', LEFT), (fixed('Area', 2, 'Q.6 (i) · 6-8 (km²) 2m'),), '2-6', MAP),
    ('(ii)', 2, L(6, '(ii) What is the aspect of the slope at M 037 784?'),
     S(4, '(ii) · North West', '(iii) 5.3', LEFT), (fixed('Aspect', 2, '(ii) · North West/NW/NNW 2m'),), '2-6', MAP),
    ('(iii)', 2, L(6, '(iii) Measure the straight line distance, in kilometres, from the Post Office in Westport',
                   'Post Office at M 033 804.'),
     S(4, '(iii) 5.3', '(iv) L 972', LEFT), (fixed('Distance', 2, '(iii) 5.3-5.7 (km) 2m'),), '2-6', MAP),
    ('(iv)', 2, L(6, '(iv) Give a six-figure grid reference for the Trailhead on the waymarked walk',
                  'south of the Ordnance Survey map.'),
     S(4, '(iv) L 972', 'Page', LEFT), (fixed('Grid reference', 2, '(iv) L 972/3 793/4 2m'),), '2-6', MAP),
])
PART_ONE.append(T(
    'p1-7', P1, '7', '', 8, 7, L(7, 'Map Skills'),
    (L(7, '(i) Match each of the letters A, B, C and D on the elevation profile above',
       'best matches it in the table below.'),
     L(7, '(ii) Indicate whether each feature in the table below is part of the physical landscape',
       'by ticking the correct box.')),
    (S(4, 'Q.7', 'Q.8', RIGHT),),
    rows(['Q.7 · D 1m · Cultural 1m', 'A 1m · Physical 1m', 'B 1m · Physical 1m', 'C 1m · Cultural 1m'], 2,
         (0, 1, 2)),
    '2-6', MAP, ID + 'p1-q7', ('page', 'map', 'legend'),
    (L(7, 'Locate point X, L 936 781, and point Y, L 937 825', 'map accompanying this paper.'),
     L(7, 'Figure 1 shows an elevation profile of the cross section', 'on the Ordnance Survey map.'),
     L(7, 'Using the 1:50 000 Ordnance Survey map and legend and the elevation profile above',
       'following questions.')),
    row_labels=(L(7, 'R335'), L(7, 'Owenwee River'), L(7, 'Conical Peak'), L(7, 'Waymarked Walk'))))
PART_ONE.append(T(
    'p1-8', P1, '8', '', 8, 8, L(8, 'Aerial Photograph – Location'),
    (L(8, 'Locate each of the features A, B, C, D and E labelled above', 'One has been completed for you.'),),
    (S(4, 'Q.8', 'Q.9', RIGHT),),
    rows(['Q.8 · B · Left middleground/Left centre 2m', 'C · Centre middleground 2m', 'D · Centre middleground 2m',
          'E · Right middleground/Right centre 2m'], 2),
    '2-8', AER + URB, ID + 'p1-q8', ('page', 'aerial'),
    (L(8, 'Examine the street map of Westport below and the aerial photograph accompanying this paper.'),
     L(8, 'N.B. The orientation of the aerial photograph', 'looking southwards across the town.')),
    row_labels=(L(8, 'B Fairgreen'), L(8, 'C Car Park'), L(8, 'D North Mall'), L(8, 'E Leisure Centre'))))
PART_ONE.append(T(
    'p1-9', P1, '9', '', 8, 9, L(9, 'Weather Charts'),
    (L(9, 'Match each of the weather charts A, B, C and D with the cloud chart most associated',
       'in each case.'),),
    (S(4, 'Q.9', 'Q.10', RIGHT),),
    rows(['Q.9 · (i) D 2m', '(ii) A 2m', '(iii) C 2m', '(iv) B 2m'], 2),
    '2-7', WX, ID + 'p1-q9', ('page',),
    (L(9, 'Examine the weather charts above and the cloud charts below.'),),
    row_labels=(L(9, '(i) Letter'), L(9, '(ii) Letter'), L(9, '(iii) Letter'), L(9, '(iv) Letter'))))
PART_ONE += romans('10', P1, 10, L(10, 'The European Union'),
                   (L(10, 'Examine the map above showing the Eurozone area in 2015', 'following questions.'),),
                   ID + 'p1-q10', ('page',), [
    ('(i)', 2, L(10, '(i) Name the most northerly European Union (EU) member state in the Eurozone area in 2015.'),
     S(4, 'Q.10 (i)', '(ii) · 19', RIGHT), (fixed('Member state', 2, 'Q.10 (i) · Finland 2m'),), '3-3', EU_ECON + EURO),
    ('(ii)', 2, L(10, '(ii) Indicate the total number of European Union member states in the Eurozone area',
                  '12 19 28'),
     S(4, '(ii) · 19', '(iii) · Two valid', RIGHT), (fixed('Number', 2, '(ii) · 19 2m'),), '3-3', EU_ECON + EURO),
    ('(iii)', 2, L(10, '(iii) Name two European Union member states not in the Eurozone area in 2015.'),
     S(4, '(iii) · Two valid', '(iv) · Two valid', RIGHT),
     (one_plus_one('(iii) · Two valid answers 1+1m', 'Two member states'),), '3-3', EU_ECON + EURO),
    ('(iv)', 2, L(10, '(iv) Name two non-European Union member states using the Euro in 2015.'),
     S(4, '(iv) · Two valid', 'Q.11', RIGHT),
     (one_plus_one('(iv) · Two valid answers 1+1m', 'Two non-EU states'),), '3-3', EU_ECON + EURO),
])
PART_ONE += romans('11', P1, 11, L(11, 'Statistical Interpretation'),
                   (L(11, 'Examine the table above which shows the number of Irish born people living abroad',
                      'following questions.'),),
                   ID + 'p1-q11', ('page',), [
    ('(i)', 2, L(11, '(i) Which region in the table above had the largest number of Irish born residents in 2013?'),
     S(4, 'Q.11', '(ii) · 6,597', RIGHT), (fixed('Region', 2, 'Q.11 · (i) · UK 2m'),), '2-0', TG),
    ('(ii)', 2, L(11, '(ii) How many Irish born people were living in New Zealand in 2000?'),
     S(4, '(ii) · 6,597', '(iii) · 8,062', RIGHT), (fixed('Number', 2, '(ii) · 6,597 2m'),), '2-0', TG),
    ('(iii)', 2, L(11, '(iii) Calculate the increase in the number of Irish born people living in Poland',
                   'between 2000 and 2013.'),
     S(4, '(iii) · 8,062', '(iv) · Any valid', RIGHT), (fixed('Increase', 2, '(iii) · 8,062 2m'),), '2-0', TG),
    ('(iv)', 2, L(11, '(iv) Explain briefly one reason for the increase in the number of Irish born people',
                  'between 2000 and 2013.'),
     S(4, '(iv) · Any valid explanation', 'Q.12', RIGHT, 'Q.11'),
     (one_plus_one('(iv) · Any valid explanation 1+1m', 'Reason'),), '4-2', POP),
])
PART_ONE += romans('12', P1, 12, L(12, 'Graphical Interpretation'),
                   (L(12, 'Examine the charts above showing the percentage share of total passengers by main airport',
                      'following questions.'),),
                   ID + 'p1-q12', ('page',), [
    ('(i)', 2, L(12, '(i) Which airport had the largest percentage share of total passengers in 2013?'),
     S(4, 'Q.12 (i)', '(ii) · Shannon', RIGHT), (fixed('Airport', 2, 'Q.12 (i) · Dublin 2m'),), '2-0', TG),
    ('(ii)', 2, L(12, '(ii) Which airport had the second largest percentage share of total passengers in 2005?'),
     S(4, '(ii) · Shannon', '(iii) · 7.6', RIGHT), (fixed('Airport', 2, '(ii) · Shannon 2m'),), '2-0', TG),
    ('(iii)', 2, L(12, '(iii) Calculate the decrease in Shannon Airport’s percentage share of total passengers',
                   'between 2005 and 2013.'),
     S(4, '(iii) · 7.6', '(iv) · Any valid', RIGHT), (fixed('Decrease', 2, '(iii) · 7.6(%) 2m'),), '2-0', TG),
    ('(iv)', 2, L(12, '(iv) Explain briefly one economic effect of a decrease in passenger numbers',
                  'on the Shannon Region.'),
     S(4, '(iv) · Any valid explanation', '2 of 44', RIGHT, 'Q.12'),
     (one_plus_one('(iv) · Any valid explanation 1+1m', 'Economic effect'),), '1-4', IRL),
])


# ---------------------------------------------------------------- Part Two --
def sketch(outline_line, outline_permitted, alloc, item_permitted, labels):
    return (fixed('Sketch outline' if 'Sketch' in outline_line else 'Map outline', 4,
                  outline_line, outline_permitted),
            *(Criterion(f'Feature {n}', 4, item_permitted, 'exact', alloc) for n in range(1, labels + 1)))


OS_SKETCH = sketch('Sketch Outline · 4 marks', (0, 4),
                   ('4 features @ 4 marks each: · Shown 3 marks (graded 3/1/0)', 'Label 1 mark'),
                   sums((0, 1, 3), (0, 1)), 4)
GRAPH = (fixed('Title', 2, ('Bar Chart · Pie Chart', 'Title · 2 marks · 2 marks')),
         fixed('Axes named (bar chart) / circle and centre (pie chart)', 2,
               ('Vertical axis named', 'Horizontal axis named'), (0, 1, 2)),
         fixed('6 items illustrated', 12, ('6 items illustrated', '(2/1/0) · (2/1/0)'), upto(12)))


def split(label, total, first, second):
    return srp(label, total, (first, second))


PART_TWO = [
    T('p2-1a', P2, '1A', '', 20, 15, L(15, 'Ordnance Survey Map'),
      (L(15, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper.',
         'in the south-west of the map.'),),
      (S(6, 'Sketch Outline', None),), OS_SKETCH, '2-6', MAP + RIVERS, ID + 'p2-q1a', ('map', 'legend'),
      row_labels=(None, L(15, 'Westport Bay'), L(15, 'The entire course of the Owenwee River'),
                  L(15, 'The entire area of Kinlooey Lough at M 03 81'),
                  L(15, 'The entire area of land above 200 metres in the south-west of the map.'))),
    T('p2-1b', P2, '1B', '', 30, 15, L(15, 'Rocks'),
      (L(15, 'Explain the formation of one igneous rock and one metamorphic rock, with reference to Irish',
         'examples.'),),
      (S(7, 'One Irish igneous rock named', 'C. · Weathering'),),
      (fixed('One Irish igneous rock named', 2, 'One Irish igneous rock named · 2 marks'),
       fixed('One Irish metamorphic rock named', 2, 'One Irish metamorphic rock named · 2 marks'),
       split('Explanation of formation of igneous and metamorphic rock (6/7 SRPs each)', 13,
             'Explanation of formation of igneous rock', 'Explanation of formation of metamorphic rock')),
      '0-1', RW, ID + 'p2-q1b'),
    T('p2-1c', P2, '1C', '', 30, 15, L(15, 'Weathering'),
      (L(15, 'Explain one process of physical weathering and one process of chemical weathering.'),),
      (S(7, 'Physical weathering process named', None),),
      (fixed('Physical weathering process named', 2, 'Physical weathering process named · 2 marks'),
       fixed('Chemical weathering process named', 2, 'Chemical weathering process named · 2 marks'),
       split('Explanation of physical and chemical weathering (6/7 SRPs each)', 13,
             'Explanation of physical weathering', 'Explanation of chemical weathering')),
      '0-8', RW, ID + 'p2-q1c'),
]

Q2AS = (L(16, 'Examine the diagram above and answer each of the following questions.'),)
PART_TWO += romans('2A', P2, 16, L(16, 'Earthquakes'), Q2AS, ID + 'p2-q2a', ('page',), [
    ('(i)', 2, L(16, '(i) What was the magnitude of the earthquake in Nepal in 2015?'),
     S(8, '(i) · 7.8', '(ii) · Indian'), (fixed('Magnitude', 2, '(i) · 7.8 · 2 marks'),), '0-7', EV),
    ('(ii)', 4, L(16, '(ii) The movement of which two plates resulted in the earthquake in Nepal?'),
     S(8, '(ii) · Indian', '(iii) · Converging'), (pair('(ii) · Indian and Eurasian · 2 + 2 marks', 'Two plates'),),
     '0-0', PS),
    ('(iii)', 2, L(16, '(iii) What type of plate boundary is shown above?'),
     S(8, '(iii) · Converging', '(iv) · Diverging'),
     (fixed('Plate boundary', 2, '(iii) · Converging/Destructive · 2 marks'),), '0-0', PS),
    ('(iv)', 4, L(16, '(iv) Name two other types of plate boundaries.'),
     S(8, '(iv) · Diverging', '(v) · Valid'),
     (pair('(iv) · Diverging etc. & Neutral etc. · 2 + 2 marks', 'Two plate boundaries'),), '0-0', PS),
    ('(v)', 4, L(16, '(v) Explain briefly what is meant by the term epicentre.'),
     S(8, '(v) · Valid', '(vi) · Valid'), (pair('(v) · Valid explanation · 2 + 2 marks', 'Explanation'),),
     '0-7', EV),
    ('(vi)', 4, L(16, '(vi) Explain briefly one way of reducing the impact of earthquakes.'),
     S(8, '(vi) · Valid', None), (pair('(vi) · Valid explanation · 2 + 2 marks', 'Way of reducing impact'),),
     '0-7', EV),
])
PART_TWO += [
    T('p2-2b', P2, '2B', '', 30, 16, L(16, 'Landform Development'),
      (L(16, '(i) Examine the role of the processes of deposition on the formation of any one landform',
         'that you have studied.'),),
      (S(9, 'Landform named', 'Or'),),
      (fixed('Landform named', 2, 'Landform named · 2 marks'), srp('Examination', 14, f'Examination · 14 x {SRPS}')),
      '0-4', RIVERS + SEA + GLAC, ID + 'p2-q2b-route-i',
      routes=(
          Route('route-i', 'Route (i)', ID + 'p2-q2b-route-i', False),
          Route('route-ii', 'Route (ii)', ID + 'p2-q2b-route-ii', False,
                prompt=(L(16, '(ii) Describe and explain the factors governing the operation of any one mass',
                          'that you have studied.'),),
                scheme=(S(9, 'Mass movement process named', None),),
                criteria=(fixed('Mass movement process named', 2, 'Mass movement process named · 2 marks'),
                          pair('Factors identified · 2 + 2 marks', 'Factors identified'),
                          srp('Description/explanation of process', 12,
                              f'Description/Explanation of process · 12 x {SRPS}')),
                topic='0-8', atlas=RW),
      )),
    T('p2-2c', P2, '2C', '', 30, 16, L(16, 'Fluvial Adjustment'),
      (L(16, 'Examine how changes in base level impact on geomorphic processes and landforms in a fluvial',
         'environment.'),),
      (S(10, 'Impact on processes identified', None),),
      (fixed('Impact on processes identified', 2, 'Impact on processes identified · 2 marks'),
       fixed('Impact on landform identified', 2, 'Impact on landform identified · 2 marks'),
       srp('Examination', 13, f'Examination · 13 x {SRPS}')),
      '0-5', RIVERS, ID + 'p2-q2c'),
]

Q3AS = (L(17, 'Examine the diagram above and answer each of the following questions.'),)
PART_TWO += romans('3A', P2, 17, L(17, 'Fluvial landforms'), Q3AS, ID + 'p2-q3a', ('page',), [
    ('(i)', 12, L(17, '(i) Name each of the fluvial landforms A, B, C, D, E and F.'),
     S(11, '(i) · A · Flood', '(ii) · Any valid'),
     (fixed('A', 2, '(i) · A · Flood Plain · 2 marks'), fixed('B', 2, 'B · Meander · 2 marks'),
      fixed('C', 2, 'C · Ox-bow lake · 2 marks'), fixed('D', 2, 'D · River cliff/cut bank etc. · 2 marks'),
      fixed('E', 2, 'E · Point Bar/river beach etc. · 2 marks'), fixed('F', 2, 'F · Levees · 2 marks')),
     '0-9', RIVERS),
    ('(ii)', 4, L(17, '(ii) Explain briefly what is meant by the term bedrock.'),
     S(11, '(ii) · Any valid', '(iii) · Any valid'),
     (pair('(ii) · Any valid explanation · 2 + 2 marks', 'Explanation'),), '0-9', RIVERS),
    ('(iii)', 4, L(17, '(iii) Explain briefly what is meant by the term alluvium.'),
     S(11, '(iii) · Any valid', None), (pair('(iii) · Any valid explanation · 2 + 2 marks', 'Explanation'),),
     '0-9', RIVERS),
])
PART_TWO += [
    T('p2-3b', P2, '3B', '', 30, 17, L(17, 'Landscape Development'),
      (L(17, 'Examine how different rock types produce distinctive landscapes, with reference to examples',
         'that you have studied.'),),
      (S(12, 'Rock 1 and associated', 'C. · Constructive'),),
      (fixed('Rock 1 and associated landscape named', 2, 'Rock 1 and associated landscape named · 2 marks'),
       fixed('Rock 2 and associated landscape named', 2, 'Rock 2 and associated landscape named · 2 marks'),
       srp('Examination', 13, f'Examination · 13 x {SRPS}')),
      '0-1', RW + KARST, ID + 'p2-q3b'),
    T('p2-3c', P2, '3C', '', 30, 17, L(17, 'Constructive Plate Boundaries'),
      (L(17, 'Discuss the geographical distribution and the impacts of constructive plate boundaries.'),),
      (S(12, 'Impact identified', None),),
      (fixed('Impact identified', 2, 'Impact identified · 2 marks'),
       fixed('Reference to geographical distribution', 2, 'Reference to geographical distribution · 2 marks'),
       srp('Discussion', 13, f'Discussion · 13 x {SRPS}')),
      '0-0', PS + EV, ID + 'p2-q3c'),
]

FACTORS_4C = ('Raw materials', 'Transport', 'Labour', 'Markets.')
PART_TWO += [
    T('p2-4a', P2, '4A', '', 20, 18, L(18, 'Map Skills'),
      (L(18, 'Draw an outline map of a Continental / Sub-Continental region (not in Europe) that you have',
         'The course of a named river.'),),
      (S(13, 'Map outline', None),),
      sketch('Map outline · 4 marks graded (4/2/0)', (0, 2, 4),
             ('4 features @ 4 marks each · Shown 2 marks graded (2/1/0)', 'Named 2 marks'), sums((0, 1, 2), (0, 2)), 4),
      '1-6', CONT, ID + 'p2-q4a',
      row_labels=(None, L(18, 'The outline of a named feature of relief (upland or lowland)'),
                  L(18, 'A named urban centre'), L(18, 'The outline of a named agricultural or industrial region'),
                  L(18, 'The course of a named river.'))),
    T('p2-4b', P2, '4B', '', 30, 18, L(18, 'European Union', nth=0),
      (L(18, 'Examine the impact of the expansion of the European Union on member states, with reference to',
         'economic and social impacts.'),),
      (S(14, 'Economic impact identified', 'C. · Secondary'),),
      (fixed('Economic impact identified', 2, 'Economic impact identified · 2 marks'),
       fixed('Social impact identified', 2, 'Social impact identified · 2 marks'),
       srp('Examination', 13, f'Examination · 13 x {SRPS}')),
      '1-3', EURO + EU_ECON, ID + 'p2-q4b'),
    T('p2-4c', P2, '4C', '', 30, 18, L(18, 'Secondary Economic Activity'),
      (L(18, 'Examine the development of secondary economic activity in an Irish region that you have studied,',
         'Markets.'),),
      (S(14, 'Factor 1 examination', None),),
      (srp('Factor 1 examination', 8, f'Factor 1 examination · 8 x {SRPS}'),
       srp('Factor 2 examination', 7, f'Factor 2 examination · 7 x {SRPS}')),
      '1-4', IRL, ID + 'p2-q4c', absorbs=pool(ID + 'p2-q4c-', FACTORS_4C, 2)[1]),
]

Q5AS = (L(19, 'Examine the charts above showing the main aquaculture producers in the European Union',
          'following questions.'),)
PART_TWO += romans('5A', P2, 19, L(19, 'Economic Activity'), Q5AS, ID + 'p2-q5a', ('page',), [
    ('(i)', 4, L(19, '(i) Calculate X, the percentage of EU-28 aquaculture produced by the UK in 2012.'),
     S(15, '(i) · 17', '(ii) · Spain'), (fixed('X', 4, '(i) · 17(%) · 4 marks'),), '2-0', TG),
    ('(ii)', 4, L(19, '(ii) Which single country produced over one-fifth of EU-28 aquaculture production in',
                  'produce in 1995?'),
     S(15, '(ii) · Spain', '(iii) · Netherlands'),
     (pair('(ii) · Spain and 19(%) · 2 + 2 marks', 'Country and percentage'),), '2-0', TG),
    ('(iii)', 4, L(19, '(iii) With reference to the charts above, which country was no longer one of the main',
                   'which country replaced it?'),
     S(15, '(iii) · Netherlands', '(iv) · Any valid'),
     (pair('(iii) · Netherlands and Greece · 2 + 2 marks', 'Two countries'),), '2-0', TG),
    ('(iv)', 4, L(19, '(iv) Explain briefly one positive impact of European Union policy on the fishing industry.'),
     S(15, '(iv) · Any valid', '(v) · Any valid'),
     (pair('(iv) · Any valid explanation · 2 + 2 marks', 'Positive impact'),), '3-3', EU_ECON + EURO),
    ('(v)', 4, L(19, '(v) Explain briefly one negative impact of European Union policy on the fishing industry.'),
     S(15, '(v) · Any valid', None),
     (pair('(v) · Any valid explanation · 2 + 2 marks', 'Negative impact'),), '3-3', EU_ECON + EURO),
])
FACTORS_5B = ('Soil', 'Relief', 'Climate.')
REGION_DEFINERS = 'culture or the physical landscape'
PART_TWO += [
    T('p2-5b', P2, '5B', '', 30, 19, L(19, 'Agriculture in a Continental / Sub-Continental Region'),
      (L(19, 'Account for the development of agriculture in a Continental / Sub-Continental region',
         'Climate.'),),
      (S(16, 'Account of Factor 1', 'C. · Concept'),),
      (srp('Account of Factor 1', 8, f'Account of Factor 1 · 8 x {SRPS}'),
       srp('Account of Factor 2', 7, f'Account of Factor 2 · 7 x {SRPS}')),
      '1-6', CONT, ID + 'p2-q5b', absorbs=pool(ID + 'p2-q5b-', FACTORS_5B, 2)[1]),
    T('p2-5c', P2, '5C', '', 30, 19, L(19, 'Concept of a Region'),
      (L(19, 'Examine how culture or the physical landscape can be used to define regions, with reference to',
         'that you have studied.'),),
      (S(16, 'Example of region', None),),
      (fixed('Example of region', 2, 'Example of region · 2 marks'),
       srp('Examination', 14, f'Examination · 14 x {SRPS}')),
      '1-0', IRL + EURO, ID + 'p2-q5c-culture',
      routes=(Route('culture', 'culture', ID + 'p2-q5c-culture', False, ((REGION_DEFINERS, 'culture'),)),
              Route('the-physical-landscape', 'the physical landscape', ID + 'p2-q5c-the-physical-landscape',
                    False, ((REGION_DEFINERS, 'the physical landscape'),)))),
]

Q6AS = (L(20, 'Examine the table above showing unemployment as a percentage of total population',
          'following questions.'),)
PART_TWO += romans('6A', P2, 20, L(20, 'Unemployment', nth=0), Q6AS, ID + 'p2-q6a', ('page',), [
    ('(i)', 4, L(20, '(i) Which two countries had the same percentage of total population unemployed in 2008?'),
     S(17, '(i) · Germany and France', '(ii) · Increasing'),
     (pair('(i) · Germany and France · 2 + 2 marks', 'Two countries'),), '2-0', TG),
    ('(ii)', 2, L(20, '(ii) What was the trend in the percentage of total population unemployed in Ireland',
                  'between 2008 and 2014?'),
     S(17, '(ii) · Increasing', '(iii) · Any valid'), (fixed('Trend', 2, '(ii) · Increasing, rising etc. · 2 marks'),),
     '2-0', TG),
    ('(iii)', 4, L(20, '(iii) Explain briefly one reason for this trend.'),
     S(17, '(iii) · Any valid', '(iv) · Germany'), (pair('(iii) · Any valid explanation · 2 + 2 marks', 'Reason'),),
     '1-4', IRL),
    ('(iv)', 2, L(20, '(iv) Which country’s youth unemployment, as a percentage of active population, decreased',
                  'between 2008 and 2014?'),
     S(17, '(iv) · Germany', '(v) · Greece'), (fixed('Country', 2, '(iv) · Germany · 2 marks'),), '2-0', TG),
    ('(v)', 4, L(20, '(v) Which country had the greatest increase in its youth unemployment',
                 'between 2008 and 2014?'),
     S(17, '(v) · Greece', '(vi) · Declining'), (fixed('Country', 4, '(v) · Greece · 4 marks'),), '2-0', TG),
    ('(vi)', 4, L(20, '(vi) What has been the trend in Ireland’s youth unemployment', 'State one reason for this trend.'),
     S(17, '(vi) · Declining', None),
     (fixed('Trend', 2, '(vi) · Declining/falling etc. · 2 marks'),
      fixed('Reason', 2, 'Any valid reason stated · 2 marks')), '2-0', TG + IRL),
])
FACTORS_6C = ('Transport', 'Location', 'Primary economic activity.')
PART_TWO += [
    T('p2-6b', P2, '6B', '', 30, 20, L(20, 'Dynamics of Regions - Climate'),
      (L(20, 'Examine the importance of climate to the economic development of any two contrasting European',
         'that you have studied.'),),
      (S(18, 'Examination of region 1', 'C. · Urban'),),
      (srp('Examination of region 1', 8, f'Examination of region 1 · 8 x {SRPS}'),
       srp('Examination of region 2', 7, f'Examination of region 2 · 7 x {SRPS}')),
      '1-5', EURO, ID + 'p2-q6b'),
    T('p2-6c', P2, '6C', '', 30, 20, L(20, 'Urban Development'),
      (L(20, 'Examine how two of the following factors have influenced the development of any urban area',
         'Primary economic activity.'),),
      (S(18, 'Named urban area', None),),
      (fixed('Named urban area', 2, 'Named urban area · 2 marks'),
       srp('Factor 1 examination', 7, f'Factor 1 examination · 7 x {SRPS}'),
       srp('Factor 2 examination', 7, f'Factor 2 examination · 7 x {SRPS}')),
      '1-1', IRL + EURO + URB, ID + 'p2-q6c', absorbs=pool(ID + 'p2-q6c-', FACTORS_6C, 2)[1]),
]

HEADING_8C = ('Three headings @ 10 marks each', 'For each of the three headings:', 'Map evidence/location · 2 marks',
              f'Discussion · 4 x {SRPS}')
PART_TWO += [
    T('p2-7a', P2, '7A', '', 20, 22, L(22, 'Ordnance Survey Map'),
      (L(22, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper.',
         'The built up area of Westport.'),),
      (S(20, 'Sketch Outline', None),), OS_SKETCH, '2-6', MAP + ECON, ID + 'p2-q7a', ('map', 'legend'),
      row_labels=(None, L(22, 'A railway line'), L(22, 'The N59'), L(22, 'The R335'),
                  L(22, 'The built up area of Westport.'))),
    T('p2-7b', P2, '7B', '', 30, 22, L(22, 'Multinational Company'),
      (L(22, 'Explain the factors that influence the operations of any one multinational company that you',
         'have studied.'),),
      (S(21, 'MNC named', 'C. · Economic Activity'),),
      (fixed('MNC named', 2, 'MNC named · 2 marks'), pair('Factors identified · 2 + 2 marks', 'Factors identified'),
       srp('Explanation', 12, f'Explanation · 12 x {SRPS}')),
      '3-2', MNC, ID + 'p2-q7b'),
    T('p2-7c', P2, '7C', '', 30, 22, L(22, 'Economic Activity - Conflict'),
      (L(22, 'Examine how conflict may arise between the exploitation of natural resources and the need to',
         'that you have studied.'),),
      (S(21, 'Example · 2 marks', None),),
      (fixed('Example', 2, 'Example · 2 marks'), srp('Examination', 14, f'Examination · 14 x {SRPS}')),
      '3-4', ENV, ID + 'p2-q7c'),
]

Q8AS = (L(23, 'Examine the table above showing Human Development Index data for selected regions',
          'following questions.'),)
PART_TWO += romans('8A', P2, 23, L(23, 'Human Development Index', nth=0), Q8AS, ID + 'p2-q8a', ('page',), [
    ('(i)', 4, L(23, '(i) Which region had the highest Human Development Index in 1990', 'in 2014?'),
     S(22, '(i) · USA and Norway', '(ii) · ($)63,409'), (pair('(i) · USA and Norway · 2 + 2 marks', 'Two regions'),),
     '2-0', TG),
    ('(ii)', 4, L(23, '(ii) Calculate the difference (in dollars) between the gross national income in Norway',
                  'Mali in 2014.'),
     S(22, '(ii) · ($)63,409', '(iii) · USA'), (fixed('Difference', 4, '(ii) · ($)63,409 · 4 marks'),), '2-0', TG),
    ('(iii)', 2, L(23, '(iii) Which region had the highest mean years of schooling in 2014?'),
     S(22, '(iii) · USA', '(iv) · Any valid'), (fixed('Region', 2, '(iii) · USA · 2 marks'),), '2-0', TG),
    ('(iv)', 4, L(23, '(iv) Explain briefly one reason why the mean years of schooling are higher in countries',
                  'Norway and Ireland.'),
     S(22, '(iv) · Any valid', '(v) · Any valid'), (pair('(iv) · Any valid explanation · 2 + 2 marks', 'Reason'),),
     '3-0', ECON),
    ('(v)', 2, L(23, '(v) Name one indicator used to calculate the Human Development Index.'),
     S(22, '(v) · Any valid', '(vi) · Any valid'), (fixed('Indicator', 2, '(v) · Any valid indicator · 2 marks'),),
     '3-0', ECON),
    ('(vi)', 4, L(23, '(vi) Explain briefly one advantage of using the Human Development Index as a measure',
                  'economic development.'),
     S(22, '(vi) · Any valid', None), (pair('(vi) · Any valid explanation · 2 + 2 marks', 'Advantage'),),
     '3-0', ECON),
])
PART_TWO += [
    T('p2-8b', P2, '8B', '', 30, 23, L(23, 'Renewable Energy'),
      (L(23, 'Examine how the development of renewable energy is crucial for Ireland’s environment and',
         'economy.'),),
      (S(23, 'Importance for Ireland’s environment identified', 'C. · Tertiary'),),
      (fixed('Importance for Ireland’s environment identified', 2,
             'Importance for Ireland’s environment identified · 2 marks'),
       fixed('Importance for Ireland’s economy identified', 2, 'Importance for Ireland’s economy identified · 2 marks'),
       srp('Examination', 13, f'Examination · 13 x {SRPS}')),
      '3-5', ENERGY, ID + 'p2-q8b'),
    T('p2-8c', P2, '8C', '', 30, 23, L(23, 'Tertiary Economic Activity'),
      (L(23, 'Using evidence from the 1:50 000 Ordnance Survey map accompanying this paper, discuss',
         'Services (excluding transport).'),),
      (S(23, 'Three headings @ 10 marks each', None),),
      tuple(Criterion(f'Heading {n}', 10, evens(10), 'srp', HEADING_8C) for n in (1, 2, 3)),
      '3-0', ECON + MAP, ID + 'p2-q8c', ('map', 'legend'),
      row_labels=(L(23, 'Accessibility'), L(23, 'Attractions'), L(23, 'Services (excluding transport).'))),
]

Q9AS = (L(24, 'Examine the data above showing Ireland’s top export partners in 2014', 'following questions.'),)
PART_TWO += romans('9A', P2, 24, L(24, 'Irish Trade'), Q9AS, ID + 'p2-q9a', ('page',), [
    ('(i)', 16, L(24, '(i) Using graph paper, draw a suitable graph to illustrate this data.'),
     S(24, 'Bar Chart · Pie Chart', '(ii) · Explain briefly'), GRAPH, '2-0', TG),
    ('(ii)', 4, L(24, '(ii) Explain briefly one advantage for a country of having a large number of export partners.'),
     S(24, 'Any valid explanation', None), (pair('Any valid explanation · 2 + 2 marks', 'Advantage'),), '3-0', ECON),
])
FACTORS_9B = ('Physical factors', 'Social factors', 'Cultural factors', 'Political factors.')
PART_TWO += [
    T('p2-9b', P2, '9B', '', 30, 24, L(24, 'Economic Development'),
      (L(24, 'Examine how two of the following factors influence the level of economic development in any',
         'Political factors.'),),
      (S(25, 'Developing economy named', 'C. · European'),),
      (fixed('Developing economy named', 2, 'Developing economy named · 2 marks'),
       srp('Factor 1 examined', 7, f'Factor 1 examined · 7 x {SRPS}'),
       srp('Factor 2 examined', 7, f'Factor 2 examined · 7 x {SRPS}')),
      '3-1', DEV, ID + 'p2-q9b', absorbs=pool(ID + 'p2-q9b-', FACTORS_9B, 2)[1]),
    T('p2-9c', P2, '9C', '', 30, 24, L(24, 'European Union Policy', nth=0),
      (L(24, 'Examine how European Union Policy influences economic activity in Ireland.'),),
      (S(25, 'Influence on economic activity identified', None),),
      (fixed('Influence on economic activity identified', 2, 'Influence on economic activity identified · 2 marks'),
       srp('Examination', 14, f'Examination · 14 x {SRPS}')),
      '3-3', EU_ECON + IRL, ID + 'p2-q9c'),
]

Q10AS = (L(25, 'Examine the data above showing the predicted Irish population', 'following questions.'),)
PART_TWO += romans('10A', P2, 25, L(25, 'Population - Ireland'), Q10AS, ID + 'p2-q10a', ('page',), [
    ('(i)', 16, L(25, '(i) Using graph paper, draw a suitable graph to illustrate this data.'),
     S(26, 'Bar Chart · Pie Chart', '(ii) · Explain briefly'), GRAPH, '2-0', TG),
    ('(ii)', 4, L(25, '(ii) Explain briefly one advantage of predicting future population characteristics.'),
     S(26, 'Any valid explanation', None), (pair('Any valid explanation · 2 + 2 marks', 'Advantage'),), '4-0', POP),
])
FUNCTION_10B = ('Three different urban functions @ 10 marks each', 'For each urban function:',
                'Function named · 2 marks', 'Function located · 2 marks', f'Function explained · 3 x {SRPS}')
PART_TWO += [
    T('p2-10b', P2, '10B', '', 30, 25, L(25, 'Urban Functions'),
      (L(25, 'Name, locate (using accepted notation) and explain three different urban functions evident on',
         'accompanying this paper.'),),
      (S(27, 'Three different urban functions', 'C. · Population'),),
      tuple(Criterion(f'Urban function {n}', 10, evens(10), 'srp', FUNCTION_10B) for n in (1, 2, 3)),
      '4-3', URB + AER, ID + 'p2-q10b', ('aerial',)),
    T('p2-10c', P2, '10C', '', 30, 25, L(25, 'Population', nth=2),
      (L(25, 'Examine how levels of development are influenced by population characteristics',
         'that you have studied.'),),
      (S(27, 'Examples · 2 + 2', None),),
      (pair('Examples · 2 + 2 marks', 'Examples'), srp('Examination', 13, f'Examination · 13 x {SRPS}')),
      '4-1', POP, ID + 'p2-q10c'),
    T('p2-11a', P2, '11A', '', 20, 26, L(26, 'Aerial Photograph'),
      (L(26, 'Examine the aerial photograph of Westport accompanying this paper.',
         'from the centre foreground to the right background.'),),
      (S(28, 'Sketch Outline', 'B. · Irish Migration'),),
      sketch('Sketch Outline · 4 marks', (0, 4),
             ('4 features @ 4 marks each · Shown 3 marks (graded 3/1/0)', 'Named 1 mark'), sums((0, 1, 3), (0, 1)), 4),
      '2-8', AER + URB, ID + 'p2-q11a', ('aerial',),
      row_labels=(None, L(26, 'The river'), L(26, 'A bridge'), L(26, 'A large car park in the background'),
                  L(26, 'The main road running from the centre foreground to the right background.'))),
    T('p2-11b', P2, '11B', '', 30, 26, L(26, 'Irish Migration'),
      (L(26, 'Describe and explain changes in patterns of migration to and from Ireland over time.'),),
      (S(28, 'Changing pattern to Ireland identified', None),),
      (fixed('Changing pattern to Ireland identified', 2, 'Changing pattern to Ireland identified · 2 marks'),
       fixed('Changing pattern from Ireland identified', 2, 'Changing pattern from Ireland identified · 2 marks'),
       srp('Description/explanation', 13, f'Description/Explanation · 13 x {SRPS}')),
      '4-2', POP, ID + 'p2-q11b'),
    T('p2-11c', P2, '11C', '', 30, 26, L(26, 'Urban Growth – Developing World City'),
      (L(26, 'Problems can develop from the growth and expansion of urban centres.'),
       L(26, 'Discuss this statement with reference to one developing world city that you have studied.')),
      (S(29, 'Example of developing world city', None),),
      (fixed('Example of developing world city', 2, 'Example of developing world city · 2 marks'),
       pair('Problems identified · 2 + 2 marks', 'Problems identified'),
       srp('Discussion', 12, f'Discussion · 12 x {SRPS}')),
      '4-5', URB, ID + 'p2-q11c'),
]

Q12AS = (L(27, 'Examine the chart above showing the confirmed number of places pledged by selected',
           'following questions.'),)
PART_TWO += romans('12A', P2, 27, L(27, 'Migration'), Q12AS, ID + 'p2-q12a', ('page',), [
    ('(i)', 2, L(27, '(i) How many places did Ireland pledge to Syrian refugees', '2015?'),
     S(30, '(i) · 610', '(ii) · Canada'), (fixed('Places', 2, '(i) · 610 · 2 marks'),), '2-0', TG),
    ('(ii)', 2, L(27, '(ii) Which country, that is not a member of the European Union, pledged the most',
                  'number of places?'),
     S(30, '(ii) · Canada', '(iii) · 46,490'), (fixed('Country', 2, '(ii) · Canada · 2 marks'),), '2-0', TG),
    ('(iii)', 4, L(27, '(iii) Calculate the total number of places pledged by the European Union member states',
                   'listed above.'),
     S(30, '(iii) · 46,490', '(iv) · Any two'), (fixed('Total', 4, '(iii) · 46,490 · 4 marks'),), '2-0', TG),
    ('(iv)', 4, L(27, '(iv) List two push factors that result in people migrating.'),
     S(30, '(iv) · Any two', '(v) · Any valid'),
     (pair('(iv) · Any two push factors listed · 2 + 2 marks', 'Two push factors'),), '4-2', POP),
    ('(v)', 4, L(27, '(v) Explain briefly one challenge faced by countries receiving large numbers of migrants.'),
     S(30, '(v) · Any valid', '(vi) · Any valid'),
     (pair('(v) · Any valid explanation · 2 + 2 marks', 'Challenge'),), '4-2', POP),
    ('(vi)', 4, L(27, '(vi) Explain briefly one positive impact of immigration for the receiving country.'),
     S(30, '(vi) · Any valid', None), (pair('(vi) · Any valid explanation · 2 + 2 marks', 'Positive impact'),),
     '4-2', POP),
])
PART_TWO += [
    T('p2-12b', P2, '12B', '', 30, 27, L(27, 'Central Place Theory', nth=0),
      (L(27, 'Describe and explain Central Place Theory with reference to example(s) that you have studied.'),),
      (S(31, 'Example · 2 marks', 'C. · Urban', None, 'B. · Central'),),
      (fixed('Example', 2, 'Example · 2 marks'),
       srp('Description/explanation', 14, f'Description/Explanation · 14 x {SRPS}')),
      '4-3', URB, ID + 'p2-q12b'),
    T('p2-12c', P2, '12C', '', 30, 27, L(27, 'Urban Development'),
      (L(27, 'Examine how urban centres change over time with reference to example(s) that you have studied.'),),
      (S(31, 'Change identified', None),),
      (fixed('Change identified', 2, 'Change identified · 2 marks'), fixed('Example', 2, 'Example · 2 marks'),
       srp('Examination', 13, f'Examination · 13 x {SRPS}')),
      '4-4', LAND + URB, ID + 'p2-q12c'),
]

# ------------------------------------------------------------------ Options --
OC = (S(33, '*Overall Coherence (20 marks)', None, table=True),)
COHERENCE = Criterion('Overall coherence', 20, (0, 6, 10, 14, 17, 20), 'exact',
                      ('Overall Coherence · 20 marks graded*', '*Overall Coherence (20 marks)', 'Excellent · 20',
                       'Very Good · 17', 'Good · 14', 'Fair · 10', 'Weak · 6', 'Poor · 0'))
OPTION_CRITERIA = (
    Criterion('Aspects (3 @ 20 marks or 4 @ 15 marks)', 60, upto(60), 'srp',
              ('Number of aspects', 'Identifying aspect', '8 x SRP')),
    COHERENCE)
# Option 18 prints three of four items and only the "3 @ 20 marks each" outline.
OPTION_CRITERIA_3 = (
    Criterion('Aspects (3 @ 20 marks)', 60, evens(60), 'srp',
              ('Number of aspects · 3 @ 20 marks each', 'Identifying aspect · 4 marks', 'Discussion · 8 x SRP')),
    COHERENCE)


def option(q, page, theme, note_nth, prompt, scheme_page, topic, atlas, after=None, end=None, absorbs=(),
           criteria=OPTION_CRITERIA):
    return T(f'p2-{q}', P2, q, '', 80, page, theme, prompt if isinstance(prompt, tuple) else (prompt,),
             (S(scheme_page, 'Number of aspects', end, None, after), *OC), criteria,
             topic, (atlas,), ID + f'p2-q{q}',
             stem=(L(page, 'Note: It is better to discuss three or four aspects', 'large number of points.',
                     nth=note_nth),),
             absorbs=absorbs)


GI, GE = H + 'option-global-interdependence', H + 'option-geoecology'
CI, AO = H + 'option-culture-identity', H + 'option-atmosphere-ocean'
BIOME = ('Climate', 'Soils', 'Flora', 'Fauna.')
OPTIONS = [
    option('13', 29, L(29, 'Global Interdependence'), 0,
           L(29, 'Views of development and underdevelopment involve contrasting models and', 'Discuss.'),
           34, '5-0', GI, after='13.', end='14.'),
    option('14', 29, L(29, 'Global Interdependence'), 0,
           L(29, 'Examine sustainable development as a model for future development.'), 34, '5-3', GI, after='14.'),
    option('15', 29, L(29, 'Global Interdependence'), 0,
           L(29, 'Discuss the human and natural causes of desertification and of deforestation.'), 35, '5-1', GI),
    option('16', 29, L(29, 'Geoecology'), 1,
           L(29, 'Examine the general composition and characteristics of any one soil type.'),
           36, '6-0', GE, after='16.', end='17.'),
    option('17', 29, L(29, 'Geoecology'), 1,
           L(29, 'Various soil patterns have developed in different regions of the world', 'Discuss.'),
           36, '6-1', GE, after='17.'),
    option('18', 29, L(29, 'Geoecology'), 1,
           L(29, 'Examine the characteristics of one biome that you have studied, with reference to any',
             'Fauna.'), 37, '6-2', GE, absorbs=pool(ID + 'p2-q18-', BIOME, 3)[1], criteria=OPTION_CRITERIA_3),
    option('19', 30, L(30, 'Culture and Identity'), 0,
           L(30, 'Examine the importance of religion as an indicator of culture.'), 38, '7-0', CI,
           after='19.', end='20.'),
    option('20', 30, L(30, 'Culture and Identity'), 0,
           L(30, 'Many states have different cultural groups within their borders.', 'Discuss.'), 38, '7-1', CI,
           after='20.'),
    option('21', 30, L(30, 'Culture and Identity'), 0,
           L(30, 'Identity as a concept entails a variety of cultural factors.', 'that you have studied.'),
           39, '7-2', CI),
    option('22', 30, L(30, 'The Atmosphere - Ocean Environment'), 1,
           L(30, 'Circulation in both the atmosphere and the oceans gives rise to different weather patterns.',
             'Discuss.'), 40, '8-3', AO, after='22.', end='23.'),
    option('23', 30, L(30, 'The Atmosphere - Ocean Environment'), 1,
           L(30, 'Climate characteristics change over time and space.', 'Discuss.'), 40, '8-4', AO, after='23.'),
    option('24', 30, L(30, 'The Atmosphere - Ocean Environment'), 1,
           L(30, 'Examine how climate characteristics influence economic development.'), 41, '8-5', AO),
]

TASKS = [*PART_ONE, *PART_TWO, *OPTIONS]

ID_CORRECTION_REASON = 'No 2016 Higher card shipped before this review; every card is new.'

# No 2016 Higher card was live on origin/main before this review.
LEGACY_IDS: list[str] = []
