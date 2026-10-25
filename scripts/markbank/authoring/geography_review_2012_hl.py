"""Independent review ledger: Leaving Certificate Geography 2012 Higher Level.

Sources (English editions, harvested Paper Trail corpus; sizes and SHA-256
pinned in EXPECTED_SOURCES and the generated audit): the examination paper
LC005ALP000EV (32 pages; one booklet printed Part One, answered in it, and
Part Two), marking scheme LC005ALP000EV (48 pages), and the common
Carrick-on-Shannon companions as Paper Trail files them — the 1:50 000 map
LC005CLP003EV, its legend LC005CLPC00EV and the aerial photograph
LC005CLP004EV (each a one-page PDF holding one image). Part One is 80 marks
(any ten of twelve @ 8), Part Two 320 (four questions @ 80).

Visual sweep (every page rendered and read on 2026-10-23):
  Paper p1 cover and examiner's grid; p2-p11 Part One Questions 1-12 (p6
  holds Q5 and Q6, p8 Q8 and Q9; Q2 prints an OS map extract, Q1 and Q7
  photographs, Q10 satellite images); p12 Part Two instructions; p13
  Section 1 divider; p14-p19 Q1-Q6 (p14 and p17 open with their dividers);
  p20 Section 2 divider; p21-p27 Electives Q7-Q12 (p21 and p24 open with
  their elective dividers; p24 holds 10A, its historical map of
  Carrick-on-Shannon, and 10B; p25 10C and its population graph); p28
  Section 3 divider and option note; p29-p30 Options Q13-Q24; p31-p32
  printed "Blank Page".
  Scheme p1 cover; p2 blank; p3 note on marking schemes; p4 Part One table
  (a centred tariff heading, then two columns: Q1-Q6, Q7-Q12; the answer
  lines print no marks); p5 Part Two instructions; p6 Section 1 divider;
  p7-p13 Q1-Q3 (p7 opens with its divider); p14-p19 Q4-Q6 (p14 opens with
  its divider); p20 Section 2 divider; p21-p25 Q7-Q9; p26-p32 Q10-Q12 (p21
  and p26 open with their dividers); p33 Section 3 divider and option note;
  p34-p41 Q13-Q24; p42 Geographical Investigation (coursework); p43 its
  presentation marks; p44 investigation topics; p45 Irish-language bonus
  marks; p46 blank but for its page footer; p47 blank; p48 back cover. The
  scheme reprints each Part Two question above its allocation; every slice
  starts at the allocation.
  Companions: Carrick-on-Shannon map extract (the River Shannon, Lough
  Eidin, Jamestown Canal, Drumsna, the N4); OS Discovery Series legend
  sheet; oblique aerial photograph of Carrick-on-Shannon (the Shannon, the
  bridge and marina, a cleared building site, car parks).

Part One prices every question in one heading, printed as two lines under
"Each question:": "4 parts @ 2 marks each" and "8 parts @ 1 mark each".
Every Part One card carries the heading line that prices it with its answer
lines: Q4 (eight letters), Q6(i) (four letters) and Q7 (four letters and
four processes) are priced at one mark per answer, the rest at two marks a
part. Q6(ii) prints its own "Two definitions @ 2marks each", which leaves
four marks for the four letters of Q6(i). Q11(iv) prints "Valid reason
1+1". Q12(iv) prints "Accept all answers for 2 marks": that line is its
guidance. Q8(ii) asks for two antiquities in one two-mark part; the scheme
prints no split, so it is awarded whole (0 or 2). Q12 prints
its tariff as "[8]". Matching tables, in the printed row order: Q1 A
Lateral moraine, B Arête, C Pyramidal peak, D Corrie/Coom/Cirque; Q2(i) Dry
river valley A, Dendritic drainage C, Swallow hole B; Q4 Vent G, Crater C,
Ash cloud B, Secondary cone H, Lava flow A, Magma chamber E, Volcanic bombs
D, Subsidiary vent F; Q6(i) The Central Plain of Ireland C, Wallonia D,
Mediterranean A, Berlin B; Q7 Incised meander D Tectonic uplift, Landslide
B Mass movement, Caldera A Volcanic activity, Limestone pavement C
Chemical weathering; Q10 The Aswan Dam D, A Hurricane C, A recent lava flow
A, Coastal sediments B. Q7 answers each printed row twice (a letter and a
process) and is one card of two-mark rows.

Part Two prices 2A unevenly but to the printed 20: (ii) "55 mm 2 marks" and
(iv) "Tsunami 4 marks" with "Any valid explanation 2 marks".

The options print no Overall Coherence table: coherence is graded inside
each aspect ("Number of aspects: 3 @ 27 + 27 + 26 / 4 @ 20 marks each",
"Identifying aspect: 4 marks / 4 marks", "Discussion: 8 x SRPs OR 6 x
SRPs", "Overall coherence: 7/6 marks graded / 4 marks graded"). Either way
the discussion is 24 SRPs (3 x 8 or 4 x 6), 48 marks, and identifying plus
coherence is 32 (3 x 4 + 7 + 7 + 6, or 4 x 4 + 4 x 4), so each option card
prices those two criteria. Option 18 prints only the three-aspect scheme
and is priced per aspect, 27 + 27 + 26.

Printed choices: 2B (i) or (ii) is two routes; 2C "either river, coastal or
mass movement processes" is three routes; 8C "footloose industries or
tourism" is two routes, each with its own printed allocation. 4B and 5C
(any two of three listed factors), 6C (any two of five human processes) and
option 18 (any three of four activities) are pools, one card each. 11B's
"any three different functions" prints no pool and stays open.
"""

from geography_review import (
    Criterion, Lift, Route, SchemeSlice, Task, pool, evens, fixed, slug, srp, sums, upto,
)

YEAR = 2012
LEVEL = 'higher'
PAPER_PAGES = {1: 32, 2: 32}
SCHEME_PAGES = 48
QUESTION_TARIFFS = {1: {str(n): 8 for n in range(1, 13)},
                    2: {**{f'{n}{x}': (20 if x == 'A' else 30)
                           for n in range(1, 13) for x in 'ABC'},
                        **{str(n): 80 for n in range(13, 25)}}}

EXPECTED_SOURCES = {
    'paper1': ('LC005ALP000EV.pdf', 2999085),
    'paper2': ('LC005ALP000EV.pdf', 2999085),
    'scheme': ('LC005ALP000EV.pdf', 1089373),
    'map': ('LC005CLP003EV.pdf', 1738631),
    'legend': ('LC005CLPC00EV.pdf', 267008),
    'aerial': ('LC005CLP004EV.pdf', 3193770),
}

_PAPER = {1: 'cover and examiner grid', **{p: 'question' for p in range(2, 12)},
          12: 'Part Two instructions', 13: 'section divider', **{p: 'question' for p in range(14, 20)},
          20: 'section divider', **{p: 'question' for p in range(21, 28)}, 28: 'section divider and option note',
          29: 'question', 30: 'question', 31: 'blank page', 32: 'blank page'}
PAGE_REVIEW = {
    # One booklet printed both parts.
    'paper1': _PAPER, 'paper2': _PAPER,
    'scheme': {1: 'cover', 2: 'blank', 3: 'notes', 4: 'Part One table', 5: 'Part Two instructions',
               6: 'section divider', **{p: 'Part Two allocation' for p in range(7, 20)}, 20: 'section divider',
               **{p: 'Part Two allocation' for p in range(21, 33)}, 33: 'section divider and option note',
               **{p: 'option allocation' for p in range(34, 42)},
               42: 'geographical investigation (coursework)',
               43: 'geographical investigation presentation marks', 44: 'investigation topics',
               45: 'Irish-language bonus marks', 46: 'blank', 47: 'blank', 48: 'back cover'},
}

EXPECTED_SELECTION_SCAN = [
    [1, 2, 'attempt ten'], [1, 12, 'attempt four'], [1, 13, 'attempt two'], [1, 14, 'attempt one'],
    [1, 15, 'answer (i) or (ii)'], [1, 15, 'either'], [1, 17, 'attempt one'], [1, 17, 'any two'],
    [1, 18, 'any two'], [1, 19, 'any two'], [1, 20, 'attempt one'], [1, 26, 'attempt to'],
    [1, 26, 'any three'], [1, 28, 'attempt one'], [1, 29, 'any three'],
]
SELECTION_REVIEW = [
    {'scan': [[1, 2, 'attempt ten'], [1, 12, 'attempt four'], [1, 13, 'attempt two'], [1, 14, 'attempt one'],
              [1, 17, 'attempt one'], [1, 20, 'attempt one'], [1, 28, 'attempt one']],
     'kind': 'exam-attempt-rule',
     'reason': 'Part One any ten of twelve and Part Two four questions (one of Q1-3, one of Q4-6, one elective, one option) are attempt rules; every question is carded.'},
    {'scan': [[1, 15, 'answer (i) or (ii)']], 'kind': 'closed-route',
     'reason': '2B: (i) or (ii) -> two routes, each with its own scheme allocation.'},
    {'scan': [[1, 15, 'either']], 'kind': 'closed-route',
     'reason': '2C: either river, coastal or mass movement processes -> 3 routes under one allocation.'},
    {'scan': [], 'kind': 'inline-closed-route',
     'reason': '8C "footloose industries or tourism" -> 2 routes, each with its own printed allocation (no directive word the scan reads; the route text is anchored on the paper).'},
    {'scan': [[1, 17, 'any two'], [1, 18, 'any two'], [1, 19, 'any two'], [1, 29, 'any three']],
     'kind': 'choose-n-one-card',
     'reason': '4B any two of three printed factors, 5C any two of three printed factors, 6C any two of the five human processes printed in a table and option 18 any three of four printed activities -> one card each with every printed item (choice is not a route).'},
    {'scan': [[1, 26, 'any three']], 'kind': 'open-response',
     'reason': '11B any three different functions of Carrick-on-Shannon prints no pool. Compulsory lists stay whole: 1A, 4A, 9A, 10A each item; 7B three factors; 10C three changes.'},
    {'scan': [[1, 26, 'attempt to']], 'kind': 'not-a-selection',
     'reason': '11A(v) "authorities attempt to solve" describes the authorities, not a candidate choice.'},
]

P1, P2 = 1, 2
LEFT = (0.0, 0.265, 0.46, 0.94)
RIGHT = (0.46, 0.265, 1.0, 0.94)
ID = 'geography-2012-hl-'
H = 'geography-higher-'
SRPS = 'SRPs'
EACH2 = '4 parts @ 2 marks each'
EACH1 = '8 parts @ 1 mark each'


def L(page, start, end=None, nth=None):
    return Lift(page, start, end, None, nth)


def S(page, start, end=None, clip=None, after=None, table=False):
    return SchemeSlice(page, start, end, clip, after, table)


# The Part One heading lines that price each question.
HEAD2 = S(4, EACH2, EACH1)
HEAD1 = S(4, EACH1, 'Q.1 A')


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
PART_ONE = [
    T('p1-1', P1, '1', '', 8, 2, L(2, 'Glacial Landforms'),
      (L(2, 'In the table below, match each of the letters A to D with the correct landform from the',
         'Pyramidal peak'),),
      (HEAD2, S(4, 'Q.1 A', 'Q.2', LEFT)),
      priced_rows(EACH2, ['Q.1 A = Lateral moraine', 'B = Arête', 'C = Pyramidal peak',
                          'D = Corrie/Coom/Cirque'], 2,
                  labels=('Letter A', 'Letter B', 'Letter C', 'Letter D')),
      '0-11', GLAC, ID + 'p1-q1', ('page',), (L(2, 'Examine the aerial photograph above.'),)),
]
PART_ONE += romans('2', P1, 3, L(3, 'Physical Features'),
                   (L(3, 'Examine the Ordnance Survey map extract above and answer the following questions.'),),
                   ID + 'p1-q2', ('page',), [
    ('(i)', 6, L(3, '(i) Match each of the letters A to C with the correct feature in the table below.'),
     (HEAD2, S(4, 'Q.2 (i) A', '(ii) Limestone', LEFT)),
     priced_rows(EACH2, ['Q.2 (i) A', '=C', '=B'], 2), '2-6', MAP + KARST + RIVERS,
     (L(3, 'Dry river valley'), L(3, 'Dendritic drainage'), L(3, 'Swallow hole'))),
    ('(ii)', 2, L(3, '(ii) The dry river valley and the swallow hole', 'Name this rock.'),
     (HEAD2, S(4, '(ii) Limestone', 'Q.3', LEFT)), answer('Rock', EACH2, '(ii) Limestone'), '0-3', KARST + MAP),
])
Q3S = (L(4, 'Examine the weather chart above.', 'by ticking the correct box.'),)
PART_ONE += romans('3', P1, 4, L(4, 'Weather Chart'), Q3S, ID + 'p1-q3', ('page',), [
    ('(i)', 2, L(4, '(i) There is a cold northerly airflow over Ireland.'),
     (HEAD2, S(4, 'Q.3 (i) True', '(ii) True', LEFT)), answer('True or false', EACH2, 'Q.3 (i) True'), '2-7', WX),
    ('(ii)', 2, L(4, '(ii) There is a cold front over the northern coast of France.'),
     (HEAD2, S(4, '(ii) True', '(iii) False', LEFT)), answer('True or false', EACH2, '(ii) True'), '2-7', WX),
    ('(iii)', 2, L(4, '(iii) There is an anticyclone over Scandinavia.'),
     (HEAD2, S(4, '(iii) False', '(iv) True', LEFT)), answer('True or false', EACH2, '(iii) False'), '2-7', WX),
    ('(iv)', 2, L(4, '(iv) The air pressure nearest to Latitude', 'hectopascals/millibars.'),
     (HEAD2, S(4, '(iv) True', 'Q.4', LEFT)), answer('True or false', EACH2, '(iv) True'), '2-7', WX),
])
PART_ONE.append(T(
    'p1-4', P1, '4', '', 8, 5, L(5, 'Structure of a Volcano'),
    (L(5, 'Match each of the letters A to H in the above diagram', 'in the table below.'),),
    (HEAD1, S(4, 'Q.4', 'Q.5', LEFT)),
    priced_rows(EACH1, ['Q.4 G', '=C', '=B', '=H', '=A', '=E', '=D', '=F'], 1),
    '0-7', EV, ID + 'p1-q4', ('page',),
    row_labels=(L(5, 'Vent'), L(5, 'Crater'), L(5, 'Ash cloud'), L(5, 'Secondary cone / parasitic cone'),
                L(5, 'Lava flow'), L(5, 'Magma chamber'), L(5, 'Volcanic bombs / lava bombs'),
                L(5, 'Subsidiary vent'))))
PART_ONE += romans('5', P1, 6, L(6, 'Plate Tectonics'),
                   (L(6, 'Examine the diagram above showing a plate boundary and answer the following questions.'),),
                   ID + 'p1-q5', ('page',), [
    ('(i)', 2, L(6, '(i) Name the type of plate boundary shown above.'),
     (HEAD2, S(4, 'Q.5 (i)', '(ii) Continental', LEFT)),
     answer('Plate boundary', EACH2, 'Q.5 (i) Destructive / Convergent'), '0-0', PS),
    ('(ii)', 2, L(6, '(ii) Name the type of plate at A.'),
     (HEAD2, S(4, '(ii) Continental', '(iii) Subduction', LEFT)), answer('Type of plate', EACH2, '(ii) Continental'),
     '0-0', PS),
    ('(iii)', 2, L(6, '(iii) Name the process taking place at B.'),
     (HEAD2, S(4, '(iii) Subduction', '(iv) Asthenosphere', LEFT)), answer('Process', EACH2, '(iii) Subduction'),
     '0-0', PS),
    ('(iv)', 2, L(6, '(iv) Name the part of the mantle at C.'),
     (HEAD2, S(4, '(iv) Asthenosphere', 'Q.6', LEFT)),
     answer('Part of the mantle', EACH2, '(iv) Asthenosphere / Upper mantle'), '0-0', PS),
])
PART_ONE += romans('6', P1, 6, L(6, 'Regions'), (), ID + 'p1-q6', ('page',), [
    ('(i)', 4, L(6, '(i) Examine the table below.', 'in the space provided.'),
     (HEAD1, S(4, 'Q.6 (i) C', '(ii) Two definitions', LEFT)),
     priced_rows(EACH1, ['Q.6 (i) C', '=D', '=A', '=B'], 1), '1-0', IRL + EURO,
     (L(6, 'The Central Plain of Ireland'), L(6, 'Wallonia'), L(6, 'Mediterranean'), L(6, 'Berlin'))),
    ('(ii)', 4, (L(6, '(ii) Briefly define each type of region listed below:'), L(6, 'Peripheral region'),
                 L(6, 'Administrative region')),
     S(4, '(ii) Two definitions', None, LEFT),
     (fixed('Peripheral region', 2, '(ii) Two definitions @ 2marks each'),
      fixed('Administrative region', 2, '(ii) Two definitions @ 2marks each')), '1-0', IRL + EURO,
     (L(6, 'Peripheral region'), L(6, 'Administrative region'))),
])
PART_ONE.append(T(
    'p1-7', P1, '7', '', 8, 7, L(7, 'Physical Processes'),
    (L(7, '(i) Insert the correct letter to match each of the photographs above', 'correct description.'),
     L(7, '(ii) Insert the correct process from the following list', 'Tectonic uplift.')),
    (HEAD1, S(4, 'Q.7', 'Q.8', RIGHT)),
    priced_rows(EACH1, ['Q.7 · D Tectonic uplift', 'B Mass movement', 'A Volcanic activity',
                        'C Chemical weathering'], 2, (0, 1, 2)),
    '0-4', RW + RIVERS + EV + KARST, ID + 'p1-q7', ('page',),
    (L(7, 'Examine the photographs above and answer the following questions in the table below.'),),
    row_labels=(L(7, 'Incised meander'), L(7, 'Landslide'), L(7, 'Caldera'), L(7, 'Limestone pavement'))))
PART_ONE += romans('8', P1, 8, L(8, 'Ordnance Survey Map', nth=0),
                   (L(8, 'Using the 1:50000 Ordnance Survey map and legend that accompany this paper,',
                      'in the spaces provided.'),),
                   ID + 'p1-q8', ('map', 'legend'), [
    ('(i)', 2, L(8, '(i) Name one artificial waterway evident on the Ordnance Survey map.'),
     (HEAD2, S(4, 'Q.8', '(ii) Crannóg', RIGHT)), answer('Artificial waterway', EACH2, 'Q.8 · (i) Jamestown canal'),
     '2-6', MAP),
    ('(ii)', 2, (L(8, '(ii) Which antiquities are found at the following grid references?'),
                 L(8, 'G 946 037'), L(8, 'M 906 950')),
     (HEAD2, S(4, '(ii) Crannóg', '(iii) Drumlin', RIGHT)),
     answer('Two antiquities', EACH2, ('(ii) Crannóg', 'Clós, Ráth, Lios, Ringfort'), 2),
     '2-6', MAP),
    ('(iii)', 2, L(8, '(iii) Name the feature of glacial deposition found in grid square M 94 95.'),
     (HEAD2, S(4, '(iii) Drumlin', '(iv) North East', RIGHT)), answer('Feature', EACH2, '(iii) Drumlin'),
     '2-6', MAP + GLAC),
    ('(iv)', 2, L(8, '(iv) Examine the long axis trend of the feature named in part (iii) above.',
                  'From which direction did the ice sheet originate?'),
     (HEAD2, S(4, '(iv) North East', 'Q.9', RIGHT)), answer('Direction', EACH2, '(iv) North East / NE'),
     '0-11', GLAC + MAP),
])
PART_ONE += romans('9', P1, 8, L(8, 'Aerial Photograph and Ordnance Survey Map'),
                   (L(8, 'Using the aerial photograph, the 1:50000 Ordnance Survey map and legend that',
                      'in the spaces provided.'),),
                   ID + 'p1-q9', ('aerial', 'map', 'legend'), [
    ('(i)', 2, L(8, '(i) State whether the following statement is true or false by ticking the correct box.',
                 'aerial photograph.'),
     (HEAD2, S(4, 'Q.9', '(ii) South', RIGHT)), answer('True or false', EACH2, 'Q.9 · (i) False'), '2-8', AER + MAP),
    ('(ii)', 2, L(8, '(ii) In which direction was the camera pointed when the aerial photograph was taken?'),
     (HEAD2, S(4, '(ii) South', '(iii) Killukin', RIGHT)), answer('Direction', EACH2, '(ii) South / SW / SSW'),
     '2-8', AER + MAP),
    ('(iii)', 2, L(8, '(iii) Name the small meandering river in the left background of the aerial photograph.'),
     (HEAD2, S(4, '(iii) Killukin', '(iv) M 940', RIGHT)), answer('River', EACH2, '(iii) Killukin River'),
     '2-8', AER + MAP),
    ('(iv)', 2, L(8, '(iv) Give a six-figure grid reference for the point where the river named',
                  'joins the River Shannon.'),
     (HEAD2, S(4, '(iv) M 940', 'Q.10', RIGHT)), answer('Grid reference', EACH2, '(iv) M 940/939 987/8'),
     '2-8', AER + MAP),
])
PART_ONE.append(T(
    'p1-10', P1, '10', '', 8, 9, L(9, 'Satellite Interpretation'),
    (L(9, 'Match each of the letters A to D with its correct description in the table below.'),),
    (HEAD2, S(4, 'Q.10', 'Q.11', RIGHT)),
    priced_rows(EACH2, ['Q.10 · D', '=C', '=A', '=B'], 2),
    '2-8', AER, ID + 'p1-q10', ('page',), (L(9, 'Examine the satellite images above.'),),
    row_labels=(L(9, 'The Aswan Dam'), L(9, 'A Hurricane'), L(9, 'A recent lava flow'), L(9, 'Coastal sediments'))))
PART_ONE += romans('11', P1, 10, L(10, 'Population - Ireland'),
                   (L(10, 'Examine the table above which shows the population of regional authority areas in',
                      'answer the following questions.'),),
                   ID + 'p1-q11', ('page',), [
    ('(i)', 2, L(10, '(i) What was the percentage change in the State’s population between 2006 and', '2011?'),
     (HEAD2, S(4, 'Q.11', '(ii) Mid-West', RIGHT)), answer('Percentage change', EACH2, 'Q.11 · (i) 8.1'),
     '2-0', TG + POP),
    ('(ii)', 2, L(10, '(ii) Which regional authority area had the lowest percentage change between 2006',
                  'and 2011?'),
     (HEAD2, S(4, '(ii) Mid-West', '(iii) 83,427', RIGHT)), answer('Regional authority area', EACH2, '(ii) Mid-West'),
     '2-0', TG + POP),
    ('(iii)', 2, L(10, '(iii) Calculate X, the total change in population in the Dublin regional authority area',
                   'between 2006 and 2011.'),
     (HEAD2, S(4, '(iii) 83,427', '(iv) Valid reason', RIGHT)), answer('X', EACH2, '(iii) 83,427'), '2-0', TG + POP),
    ('(iv)', 2, L(10, '(iv) Briefly explain one reason why the Midlands region had the largest percentage',
                  'increase between 2006 and 2011.'),
     (HEAD2, S(4, '(iv) Valid reason', 'Q.12', RIGHT)),
     answer('Reason', EACH2, '(iv) Valid reason 1+1', 2, (0, 1, 2)), '4-0', POP + IRL),
])
PART_ONE += romans('12', P1, 11, L(11, 'Graphical Interpretation'),
                   (L(11, 'Examine the bar graph above which shows the methods used for the disposal of waste by',
                      'answer the following questions.'),),
                   ID + 'p1-q12', ('page',), [
    ('(i)', 2, L(11, '(i) Which country sent 60% only of its waste to landfill?'),
     (HEAD2, S(4, 'Q.12', '(ii) Austria', RIGHT)), answer('Country', EACH2, 'Q.12 · (i) Finland'), '2-0', TG),
    ('(ii)', 2, L(11, '(ii) Which country recycled the largest percentage of its waste?'),
     (HEAD2, S(4, '(ii) Austria', '(iii) Denmark', RIGHT)), answer('Country', EACH2, '(ii) Austria'), '2-0', TG),
    ('(iii)', 2, L(11, '(iii) Which country incinerated the largest percentage of its waste?'),
     (HEAD2, S(4, '(iii) Denmark', '(iv) Accept', RIGHT)), answer('Country', EACH2, '(iii) Denmark'), '2-0', TG),
    ('(iv)', 2, L(11, '(iv) State one reason why Ireland has no waste incinerator at present.'),
     (HEAD2, S(4, '(iv) Accept', None, RIGHT)),
     answer('Reason', EACH2, '(iv) Accept all answers for 2 marks'), '3-4', ENV + TG),
])


# ---------------------------------------------------------------- Part Two --
def sketch(outline, outline_line, outline_permitted, alloc, item_permitted, labels):
    return (fixed(outline, 4, outline_line, outline_permitted),
            *(Criterion(f'Feature {n}', 4, item_permitted, 'exact', alloc) for n in range(1, labels + 1)))


SHOWN3 = sums((0, 1, 3), (0, 1))
FRAMED = ('4 features @ 4 marks each', 'Named 1 mark')


def graph(axis_line):
    return (fixed('Title', 2, ('Bar Chart · Pie Chart', 'Title · 2 marks · 2 marks')),
            fixed('Axes (bar chart) / circle and centre (pie chart)', 2, axis_line, (0, 1, 2)),
            fixed('6 items illustrated', 12, '6 items illustrated 2 marks each graded', upto(12)))


PART_TWO = [
    T('p2-1a', P2, '1A', '', 20, 14, L(14, 'Aerial Photograph'),
      (L(14, 'Examine the aerial photograph of Carrick-on-Shannon accompanying this paper.', 'A drumlin.'),),
      (S(7, 'Proportion + Frame', 'B. · Sedimentary'),),
      sketch('Proportion + frame', 'Proportion + Frame: · 2+2 marks', (0, 2, 4), FRAMED, SHOWN3, 4),
      '2-8', AER + RIVERS + GLAC, ID + 'p2-q1a', ('aerial',),
      row_labels=(None, L(14, 'The complete course of the largest river'),
                  L(14, 'The tributary river in the left background'),
                  L(14, 'Locate the confluence and mark it with an X on the sketch map'), L(14, 'A drumlin.'))),
    T('p2-1b', P2, '1B', '', 30, 14, L(14, 'Sedimentary and Metamorphic Rocks'),
      (L(14, 'Describe the formation of one sedimentary rock that you have studied', 'into a metamorphic rock.'),),
      (S(7, 'Name one sedimentary rock', None),),
      (fixed('Name one sedimentary rock', 2, 'Name one sedimentary rock · 2 marks'),
       fixed('Name the metamorphic rock', 2, 'Name the metamorphic rock · 2 marks'),
       srp('Formation of sedimentary rock', 11, f'Formation of sedimentary rock · 11 x {SRPS}'),
       srp('Formation of metamorphic rock', 2, f'Formation of metamorphic rock · 2 x {SRPS}')),
      '0-1', RW, ID + 'p2-q1b'),
    T('p2-1c', P2, '1C', '', 30, 14, L(14, 'Earthquakes'),
      (L(14, 'Explain, with reference to examples that you have studied, how the theory of',
         'around the world.'),),
      (S(8, 'Global examples', None),),
      (pair('Global examples/locations of earthquakes · 2+2 marks', 'Global examples/locations of earthquakes'),
       srp('Discussion', 13, f'Discussion · 13 x {SRPS}')),
      '0-7', EV + PS, ID + 'p2-q1c'),
]
Q2AS = (L(15, 'Examine the map above and answer the following questions.'),)
PART_TWO += romans('2A', P2, 15, L(15, 'Plate Tectonics – Earthquakes'), Q2AS, ID + 'p2-q2a', ('page',), [
    ('(i)', 4, L(15, '(i) Name the plates marked X and Y.'),
     S(9, '(i) · X = Eurasian', '(ii) · 55 mm'),
     (fixed('X', 2, '(i) · X = Eurasian · 2 marks'), fixed('Y', 2, 'Y = Pacific · 2 marks')), '0-0', PS),
    ('(ii)', 2, L(15, '(ii) What is the average annual movement of the Indo-Australian Plate?'),
     S(9, '(ii) · 55 mm', '(iii) · Any valid'), (fixed('Average annual movement', 2, '(ii) · 55 mm · 2 marks'),),
     '0-0', PS),
    ('(iii)', 4, L(15, '(iii) Explain what is meant by the term ‘epicentre’.'),
     S(9, '(iii) · Any valid', '(iv) · Tsunami'), (pair('(iii) · Any valid explanation · 2 + 2 marks', 'Explanation'),),
     '0-7', EV),
    ('(iv)', 6, L(15, '(iv) Given that the epicentre of the earthquake shown above is off shore,',
                  'effect of this earthquake on the sea.'),
     S(9, '(iv) · Tsunami', '(v) · Any two'),
     (fixed('Effect named', 4, '(iv) · Tsunami · 4 marks'), fixed('Explanation', 2, 'Any valid explanation · 2 marks')),
     '0-7', EV),
    ('(v)', 4, L(15, '(v) Name two scales that measure the magnitude/intensity of an earthquake.'),
     S(9, '(v) · Any two', None), (pair('(v) · Any two scales · 2 + 2 marks', 'Two scales'),), '0-7', EV),
])
SURFACE = 'either river, coastal or mass movement processes'
PART_TWO += [
    T('p2-2b', P2, '2B', '', 30, 15, L(15, 'Landform Development'),
      (L(15, '(i) Explain with the aid of a labelled diagram(s) the formation of one landform of',
         'that you have studied.'),),
      (S(10, 'Named landform', 'Or'),),
      (fixed('Named landform', 2, 'Named landform · 2 marks'),
       fixed('Labelled diagram', 4, 'Labelled diagram · 4 marks (graded 4/2/0)', (0, 2, 4)),
       srp('Explanation', 12, f'Explanation · 12 x {SRPS}')),
      '0-4', RIVERS + SEA + GLAC, ID + 'p2-q2b-route-i',
      routes=(
          Route('route-i', 'Route (i)', ID + 'p2-q2b-route-i', False, topic='0-4', atlas=RIVERS + SEA + GLAC),
          Route('route-ii', 'Route (ii)', ID + 'p2-q2b-route-ii', False,
                prompt=(L(15, '(ii) Describe and explain one process of mass movement that you have studied.'),),
                scheme=(S(10, 'Process named', None),),
                criteria=(fixed('Process named', 2, 'Process named · 2 marks'),
                          srp('Discussion', 14, f'Discussion · 14 x {SRPS}')),
                topic='0-8', atlas=RW),
      )),
    T('p2-2c', P2, '2C', '', 30, 15, L(15, 'Surface Processes'),
      (L(15, 'Examine, with reference to example(s) that you have studied, how human activities have',
         'mass movement processes.'),),
      (S(11, 'Human activity identified', None),),
      (fixed('Human activity identified', 2, 'Human activity identified · 2 marks'),
       fixed('Impact identified', 2, 'Impact identified · 2 marks'),
       fixed('Named example', 2, 'Named example · 2 marks'),
       srp('Examination', 12, f'Examination · 12 x {SRPS}')),
      '0-6', RIVERS, ID + 'p2-q2c-river-processes',
      routes=(Route('river-processes', 'river processes', ID + 'p2-q2c-river-processes', False,
                    ((SURFACE, 'river'),), topic='0-6', atlas=RIVERS),
              Route('coastal-processes', 'coastal processes', ID + 'p2-q2c-coastal-processes', False,
                    ((SURFACE, 'coastal'),), topic='0-6', atlas=SEA),
              Route('mass-movement-processes', 'mass movement processes',
                    ID + 'p2-q2c-mass-movement-processes', False,
                    ((SURFACE, 'mass movement processes'),), topic='0-6', atlas=RW))),
]
Q3AS = (L(16, 'Examine the diagram of the rock cycle above and answer the following questions.'),)
PART_TWO += romans('3A', P2, 16, L(16, 'Rock Cycle', nth=0), Q3AS, ID + 'p2-q3a', ('page',), [
    ('(i)', 4, L(16, '(i) Name the category of rock formed at A and name one example of this category of', 'rock.'),
     S(12, '(i) · A - Sedimentary', '(ii) · B - Metamorphic'),
     (fixed('Category of rock at A', 2, '(i) · A - Sedimentary · 2 marks'), fixed('Example', 2, 'Example · 2 marks')),
     '0-1', RW),
    ('(ii)', 4, L(16, '(ii) Name the category of rock formed at B and name one example of this category of', 'rock.'),
     S(12, '(ii) · B - Metamorphic', '(iii) · C - Any'),
     (fixed('Category of rock at B', 2, '(ii) · B - Metamorphic · 2 marks'), fixed('Example', 2, 'Example · 2 marks')),
     '0-1', RW),
    ('(iii)', 4, L(16, '(iii) Name one example of an igneous rock which is formed at C.'),
     S(12, '(iii) · C - Any', '(iv) · D - Any'), (fixed('Example', 4, '(iii) · C - Any valid example · 4 marks'),),
     '0-1', RW),
    ('(iv)', 4, L(16, '(iv) Name one example of an igneous rock which is formed at D.'),
     S(12, '(iv) · D - Any', '(v) · Any valid'), (fixed('Example', 4, '(iv) · D - Any valid example · 4 marks'),),
     '0-1', RW),
    ('(v)', 4, L(16, '(v) Briefly explain the difference between the process of weathering and the process',
                 'of erosion.'),
     S(12, '(v) · Any valid', None), (pair('(v) · Any valid explanation · 2 + 2 marks', 'Explanation'),), '0-8', RW),
])
PART_TWO += [
    T('p2-3b', P2, '3B', '', 30, 16, L(16, 'Limestone Pavement'),
      (L(16, 'With the aid of a diagram(s), explain how chemical weathering has shaped the limestone',
         'in a karst region.'),),
      (S(13, 'Named process', 'C. · Folding'),),
      (fixed('Named process', 2, 'Named process · 2 marks'),
       fixed('Labelled diagram(s)', 4, 'Labelled diagram(s) · 4 marks (graded 4/2/0)', (0, 2, 4)),
       srp('Explanation', 12, f'Explanation · 12 x {SRPS}')),
      '0-3', KARST + RW, ID + 'p2-q3b'),
    T('p2-3c', P2, '3C', '', 30, 16, L(16, 'Folding'),
      (L(16, 'Explain, with reference to examples that you have studied, how folding impacts on',
         'landscape development.'),),
      (S(13, 'Examples · 2 + 2', None),),
      (pair('Examples · 2 + 2 marks', 'Examples'), srp('Discussion', 13, f'Discussion · 13 x {SRPS}')),
      '0-2', RW + PS, ID + 'p2-q3c'),
    T('p2-4a', P2, '4A', '', 20, 17, L(17, 'Continental / Sub-Continental Region'),
      (L(17, 'Draw an outline map of a Continental / Sub-Continental region (not in Europe) that',
         'A major road or rail link.'),),
      (S(14, 'Map outline', 'B. · Agriculture'),),
      sketch('Map outline', 'Map outline · 4 marks graded (4/2/0)', (0, 2, 4),
             ('4 features @ · 4 marks each:', 'Shown · 2 marks graded (2/1/0)', 'Named · 2 marks'),
             sums((0, 1, 2), (0, 2)), 4),
      '1-6', CONT, ID + 'p2-q4a',
      row_labels=(None, L(17, 'A named feature of relief'), L(17, 'A named river'), L(17, 'A named urban centre'),
                  L(17, 'A major road or rail link.'))),
    T('p2-4b', P2, '4B', '', 30, 17, L(17, 'Agriculture in Europe'),
      (L(17, 'Account for the development of agriculture in a European region (not in Ireland) that',
         'Climate.'),),
      (S(14, 'Discussion of Factor 1', None),),
      (srp('Discussion of Factor 1', 8, f'Discussion of Factor 1 · 8 x {SRPS}'),
       srp('Discussion of Factor 2', 7, f'Discussion of Factor 2 · 7 x {SRPS}')),
      '1-5', EURO, ID + 'p2-q4b', absorbs=pool(ID + 'p2-q4b-', ('Relief', 'Markets', 'Climate.'), 2)[1]),
    T('p2-4c', P2, '4C', '', 30, 17, L(17, 'Population in Ireland'),
      (L(17, 'Account for the distribution of population throughout an Irish region that you have',
         'studied.'),),
      (S(15, 'Examination · 15', None),), (srp('Examination', 15, f'Examination · 15 x {SRPS}'),),
      '1-4', IRL + POP, ID + 'p2-q4c'),
]
Q5AS = (L(18, 'Examine the table above and answer the following questions.'),)
PART_TWO += romans('5A', P2, 18, L(18, 'Irish Agricultural Trade'), Q5AS, ID + 'p2-q5a', ('page',), [
    ('(i)', 4, L(18, '(i) Calculate X, the percentage change for Live animal exports, between 2009 and', '2010.'),
     S(16, '(i) · 15.02', '(ii) · Sheepmeat'), (fixed('X', 4, '(i) · 15.02/15 · 4 marks'),), '2-0', TG),
    ('(ii)', 4, L(18, '(ii) Which species had the lowest percentage increase between 2009 and 2010?'),
     S(16, '(ii) · Sheepmeat', '(iii) · €113'), (fixed('Species', 4, '(ii) · Sheepmeat · 4 marks'),), '2-0', TG),
    ('(iii)', 4, L(18, '(iii) What was the increase in the monetary value of beef exports between 2009',
                   'and 2010?'),
     S(16, '(iii) · €113', '(iv) · Valid'), (fixed('Increase', 4, '(iii) · €113 million · 4 marks'),), '2-0', TG),
    ('(iv)', 4, L(18, '(iv) Briefly explain one advantage of agricultural exports to the Irish economy.'),
     S(16, '(iv) · Valid', '(v) · Valid'), (pair('(iv) · Valid explanation · 2 + 2 marks', 'Advantage'),),
     '1-4', IRL),
    ('(v)', 4, L(18, '(v) Briefly explain one challenge that Irish agriculture will face in the future.'),
     S(16, '(v) · Valid', None), (pair('(v) · Valid explanation · 2+ 2 marks', 'Challenge'),), '1-4', IRL),
])
PART_TWO += [
    T('p2-5b', P2, '5B', '', 30, 18, L(18, 'Concept of a Region'),
      (L(18, 'Examine, with reference to examples that you have studied, how the physical landscape',
         'define regions.'),),
      (S(17, 'Named specific locations', 'C. · Economic Activities'),),
      (pair('Named specific locations · 2 + 2 marks', 'Named specific locations'),
       srp('Examination', 13, f'Examination · 13 x {SRPS}')),
      '1-0', IRL + EURO + CONT, ID + 'p2-q5b'),
    T('p2-5c', P2, '5C', '', 30, 18, L(18, 'Economic Activities'),
      (L(18, 'Examine how any two of the factors listed below have influenced the development of',
         'Primary economic activity.'),),
      (S(17, 'Urban area named', None),),
      (fixed('Urban area named', 2, 'Urban area named · 2 marks'),
       srp('Factor 1 examination', 7, f'Factor 1 examination · 7 x {SRPS}'),
       srp('Factor 2 examination', 7, f'Factor 2 examination · 7 x {SRPS}')),
      '1-5', EURO, ID + 'p2-q5c',
      absorbs=pool(ID + 'p2-q5c-', ('Transport', 'Location', 'Primary economic activity.'), 2)[1]),
]
Q6AS = (L(19, 'Examine the graph above and answer the following questions.'),)
PART_TWO += romans('6A', P2, 19, L(19, 'The European Union (EU) – ‘Euro Crisis’'), Q6AS, ID + 'p2-q6a', ('page',), [
    ('(i)', 4, L(19, '(i) How many euro-zone countries had a budget deficit greater than the euro-zone',
                 'average in 2010?'),
     S(18, '(i) · 6 ·', '(ii) · 9.2'), (fixed('Number of countries', 4, '(i) · 6 · 4 marks'),), '2-0', TG + EURO),
    ('(ii)', 4, L(19, '(ii) What was the difference in the budget deficit', 'between Ireland and Austria in 2010?'),
     S(18, '(ii) · 9.2', '(iii) · Any two'), (fixed('Difference', 4, '(ii) · 9.2 · 4 marks'),), '2-0', TG + EURO),
    ('(iii)', 4, L(19, '(iii) Name two of the six founding member states of what is now the EU.'),
     S(18, '(iii) · Any two', '(iv) · Any two'),
     (pair('(iii) · Any two founding member states · 2 + 2 marks', 'Two founding member states'),),
     '3-3', EU_ECON + EURO),
    ('(iv)', 4, L(19, '(iv) Name two EU member states not in the euro-zone.'),
     S(18, '(iv) · Any two', '(v) · Valid'),
     (pair('(iv) · Any two members not in euro-zone · 2 + 2 marks', 'Two member states'),), '3-3', EU_ECON + EURO),
    ('(v)', 4, L(19, '(v) Briefly explain what is meant by the ‘Euro Crisis’.'),
     S(18, '(v) · Valid', None), (pair('(v) · Valid explanation · 2 + 2 marks', 'Explanation'),),
     '3-3', EU_ECON + EURO),
])
HUMAN = ('Population dynamics', 'Language', 'Religion', 'Urban development', 'Rural development')
PART_TWO += [
    T('p2-6b', P2, '6B', '', 30, 19, L(19, 'Economic Activity'),
      (L(19, 'Discuss the factors that influence the development of one tertiary economic activity',
         'that you have studied.'),),
      (S(19, 'Named tertiary', 'C. · The Dynamics'),),
      (fixed('Named tertiary economic activity', 2, 'Named tertiary economic activity · 2 marks'),
       pair('Factors · 2 + 2 marks', 'Factors'), srp('Discussion', 12, f'Discussion · 12 x {SRPS}')),
      '1-4', IRL, ID + 'p2-q6b'),
    T('p2-6c', P2, '6C', '', 30, 19, L(19, 'The Dynamics of Regions – Human Processes'),
      (Lift(19, 'Population dynamics', 'Rural development', row=True),
       L(19, 'Examine the impact of any two of the above factors,', 'that you have studied.')),
      (S(19, 'Factor 1:', None),),
      (fixed('Factor 1 impact', 2, ('Factor 1:', 'Impact · 2 marks@0')),
       srp('Factor 1 examination', 7, f'Examination · 7 x {SRPS}'),
       fixed('Factor 2 impact', 2, ('=Factor 2', 'Impact · 2 marks@1')),
       srp('Factor 2 examination', 6, f'Examination · 6 x {SRPS}')),
      '1-6', CONT, ID + 'p2-q6c', absorbs=pool(ID + 'p2-q6c-', HUMAN, 2)[1]),
]

Q7AS = (L(21, 'Examine the information above and answer the following questions.'),)
PART_TWO += romans('7A', P2, 21, L(21, 'Greenhouse Effect'), Q7AS, ID + 'p2-q7a', ('page',), [
    ('(i)', 4, L(21, '(i) Which region had the highest CO2', 'emissions in 2009?'),
     S(21, '(i) · Highest', '(ii) · 10.5'),
     (fixed('Highest', 2, '(i) · Highest = Asia & Oceania · 2 marks'), fixed('Lowest', 2, 'Lowest =Africa · 2 marks')),
     '2-0', TG),
    ('(ii)', 4, L(21, '(ii) Calculate X, the percentage of greenhouse gas emissions generated by agriculture',
                  'in Europe in 2009.'),
     S(21, '(ii) · 10.5', '(iii) · Valid'), (fixed('X', 4, '(ii) · 10.5 · 4 marks'),), '2-0', TG),
    ('(iii)', 4, L(21, '(iii) Briefly explain one reason why Energy (excluding transport) was the sector which',
                   'in Europe in 2009.'),
     S(21, '(iii) · Valid', '(iv) · Two greenhouse'), (pair('(iii) · Valid explanation · 2 + 2 marks', 'Reason'),),
     '3-4', ENV + ENERGY),
    ('(iv)', 4, L(21, '(iv) Name two greenhouse gases other than CO2.'),
     S(21, '(iv) · Two greenhouse', '(v) · Two impacts'),
     (pair('(iv) · Two greenhouse gases · 2 + 2 marks', 'Two greenhouse gases'),), '3-4', ENV),
    ('(v)', 4, L(21, '(v) State two ways the greenhouse effect impacts on agriculture.'),
     S(21, '(v) · Two impacts', None), (pair('(v) · Two impacts stated · 2 + 2 marks', 'Two impacts'),), '3-4', ENV),
])
FACTOR_7B = ('3 factors @ 10 marks each', 'For each factor:', 'Named factor · 2 marks', 'Map evidence · 2 marks',
             f'Explanation · 3 x {SRPS}')
PART_TWO += [
    T('p2-7b', P2, '7B', '', 30, 21, L(21, 'Economic Development'),
      (L(21, 'Using evidence from the 1:50000 Ordnance Survey map, that accompanies this paper,',
         'area shown on the Ordnance Survey map.'),),
      (S(22, '3 factors @ 10', 'C. · European'),),
      tuple(Criterion(f'Factor {n}', 10, evens(10), 'srp', FACTOR_7B) for n in (1, 2, 3)),
      '3-0', ECON + MAP, ID + 'p2-q7b', ('map', 'legend')),
    T('p2-7c', P2, '7C', '', 30, 21, L(21, 'European Union Policy'),
      (L(21, 'Examine how European Union policy influences regional development in Ireland.'),),
      (S(22, 'Influence named', None),),
      (fixed('Influence named', 2, 'Influence named · 2 marks'), srp('Examination', 14, f'Examination · 14 x {SRPS}')),
      '3-3', EU_ECON + IRL, ID + 'p2-q7c'),
]
Q8AS = (L(22, 'Examine the data in the above table showing the estimated percentage of indigenous',
          'energy sources for Ireland in 2020.'),)
PART_TWO += romans('8A', P2, 22, L(22, 'Energy Sources'), Q8AS, ID + 'p2-q8a', ('page',), [
    ('(i)', 16, L(22, '(i) Using graph paper, draw a suitable graph to illustrate this data.'),
     S(23, 'Bar Chart · Pie Chart', '(ii) · Name two'), graph('Each axis scaled · 1+1 mark'), '2-0', TG),
    ('(ii)', 4, L(22, '(ii) Name two other sources of energy not named above.'),
     S(23, 'Two other sources named', None),
     (fixed('Two other sources', 4, 'Two other sources named @ 2 marks each', (0, 2, 4)),), '3-5', ENERGY),
])
TRADES = 'footloose industries or tourism'
PART_TWO += [
    T('p2-8b', P2, '8B', '', 30, 22, L(22, 'Developing Economies'),
      (L(22, 'Examine the positive and the negative impacts of colonialism on a developing country',
         'that you have studied.'),),
      (S(24, 'Positive impact identified', 'C. · Economic Activities'),),
      (fixed('Positive impact identified', 2, 'Positive impact identified · 2 marks'),
       fixed('Negative impact identified', 2, 'Negative impact identified · 2 marks'),
       fixed('Naming developing economy', 2, 'Naming developing economy · 2 marks'),
       srp('Examination', 12, f'Examination · 12 x {SRPS}')),
      '3-1', DEV, ID + 'p2-q8b'),
    T('p2-8c', P2, '8C', '', 30, 22, L(22, 'Economic Activities'),
      (L(22, 'Examine the factors that have influenced the development of footloose industries or',
         'developed economy that you have studied.'),),
      (S(24, 'Footloose industry named', 'Or'),),
      (fixed('Footloose industry named', 2, 'Footloose industry named · 2 marks'),
       fixed('Developed economy named', 2, 'Developed economy named · 2 marks'),
       pair('Factors · 2 + 2 marks', 'Factors'), srp('Examination', 11, 'Examination · 11 x SRPS')),
      '3-0', ECON, ID + 'p2-q8c-footloose-industries',
      routes=(Route('footloose-industries', 'footloose industries', ID + 'p2-q8c-footloose-industries', False,
                    ((TRADES, 'footloose industries'),)),
              Route('tourism', 'tourism', ID + 'p2-q8c-tourism', False, ((TRADES, 'tourism'),),
                    scheme=(S(24, 'Named Tourist Activity', None),),
                    criteria=(fixed('Named tourist activity', 2, 'Named Tourist Activity · 2 marks'),
                              fixed('Developed economy named', 2, 'Developed economy named · 2 marks'),
                              pair('Factors · 2 + 2 marks', 'Factors'),
                              srp('Examination', 11, f'Examination · 11 x {SRPS}'))))),
    T('p2-9a', P2, '9A', '', 20, 23, L(23, 'Aerial Photograph'),
      (L(23, 'Examine the aerial photograph of Carrick-on-Shannon accompanying this paper.',
         'An industrial area in the background.'),),
      (S(25, 'Proportion + Frame', 'B. · Multinational'),),
      sketch('Proportion + frame', 'Proportion + Frame: · 2+2 marks', (0, 2, 4), FRAMED, SHOWN3, 4),
      '2-8', AER + ECON, ID + 'p2-q9a', ('aerial',),
      row_labels=(None, L(23, 'A large building under construction'), L(23, 'The bridge'),
                  L(23, 'A large car park in the centre foreground'), L(23, 'An industrial area in the background.'))),
    T('p2-9b', P2, '9B', '', 30, 23, L(23, 'Multinational Companies (MNC)'),
      (L(23, 'Examine how corporate strategies influence the opening and the closing of branch plants',
         'that you have studied.'),),
      (S(25, 'Named MNC', 'C. · Conflict'),),
      (fixed('Named MNC', 2, 'Named MNC · 2 marks'), fixed('Corporate strategy named', 2, 'Corporate strategy named · 2 marks'),
       srp('Examination', 13, f'Examination · 13 x {SRPS}')),
      '3-2', MNC, ID + 'p2-q9b'),
    T('p2-9c', P2, '9C', '', 30, 23, L(23, 'Conflict of Interest'),
      (L(23, 'Examine how conflict may develop between economic interests and environmental',
         'that you have studied.'),),
      (S(25, 'Conflict identified', None),),
      (fixed('Conflict identified', 2, 'Conflict identified · 2 marks'),
       fixed('Reference to example', 2, 'Reference to example · 2 marks'),
       srp('Examination', 13, f'Examination · 13 x {SRPS}')),
      '3-4', ENV, ID + 'p2-q9c'),
    T('p2-10a', P2, '10A', '', 20, 24, L(24, 'Historical Map', nth=0),
      (L(24, 'Examine the historical map of Carrick-on-Shannon shown above.', 'An administrative building.'),),
      (S(26, 'Proportion + Frame', None),),
      sketch('Proportion + frame', 'Proportion + Frame · 2 + 2 marks', (0, 2, 4), FRAMED, SHOWN3, 4),
      '4-3', URB, ID + 'p2-q10a', ('page',),
      row_labels=(None, L(24, 'Two connecting roads / streets'), L(24, 'The Fair Green'), L(24, 'The school'),
                  L(24, 'An administrative building.'))),
    T('p2-10b', P2, '10B', '', 30, 24, L(24, 'Urbanisation'),
      (L(24, '‘Authorities in developing world cities', 'with reference to example(s) you have studied.'),),
      (S(27, 'Example named', None),),
      (fixed('Example named', 2, 'Example named · 2 marks'), srp('Examination', 14, f'Examination · 14 x {SRPS}')),
      '4-5', URB, ID + 'p2-q10b'),
    T('p2-10c', P2, '10C', '', 30, 25, L(25, 'Population Change'),
      (L(25, 'With reference to the graph above, describe and explain three changes in Ireland’s',
         'between 1956 and 2011.'),),
      (S(28, 'Three changes @ 10', None),),
      tuple(Criterion(f'Change {n}', 10, evens(10), 'srp',
                      ('Three changes @ 10 marks each', 'For each of the three changes:', 'Reference to graph · 2 marks',
                       f'Explanation · 4 x {SRPS}')) for n in (1, 2, 3)),
      '4-0', POP + TG, ID + 'p2-q10c', ('page',)),
]
Q11AS = (L(26, 'Examine the table above and answer the following questions.'),)
PART_TWO += romans('11A', P2, 26, L(26, 'Transport and Traffic'), Q11AS, ID + 'p2-q11a', ('page',), [
    ('(i)', 4, L(26, '(i) How many private vehicles were registered from January to August in 2009?'),
     S(29, '(i) · 49,142', '(ii) · 71.5'), (fixed('Number of vehicles', 4, '(i) · 49,142 · 4 marks'),), '2-0', TG),
    ('(ii)', 4, L(26, '(ii) What was the percentage decrease in goods vehicles registered from January to',
                  'between 2008 and 2009?'),
     S(29, '(ii) · 71.5', '(iii) · Valid'), (fixed('Percentage decrease', 4, '(ii) · 71.5/71.52 · 4 marks'),),
     '2-0', TG),
    ('(iii)', 4, L(26, '(iii) Briefly explain one reason for this decrease.'),
     S(29, '(iii) · Valid', '(iv) · Two causes'), (pair('(iii) · Valid reason explained · 2 + 2 marks', 'Reason'),),
     '2-0', TG + URB),
    ('(iv)', 4, L(26, '(iv) State two causes of traffic congestion.'),
     S(29, '(iv) · Two causes', '(v) · Valid'), (pair('(iv) · Two causes stated · 2 + 2 marks', 'Two causes'),),
     '4-5', URB),
    ('(v)', 4, L(26, '(v) Briefly explain one way authorities attempt to solve the problem of traffic',
                 'congestion.'),
     S(29, '(v) · Valid', None), (pair('(v) · Valid explanation · 2 + 2 marks', 'Explanation'),), '4-5', URB),
])
FUNCTION_11B = ('Three functions @ 10 marks each', 'For each of the three functions:', 'Named function · 2 marks',
                'Location of evidence on the aerial photograph · 2 marks', f'Explanation · 3 x {SRPS}')
PART_TWO += [
    T('p2-11b', P2, '11B', '', 30, 26, L(26, 'Urban Functions'),
      (L(26, 'Study the aerial photograph accompanying this paper.', 'to support your answer.'),),
      (S(30, 'Three functions @ 10', 'C. · Demographic'),),
      tuple(Criterion(f'Function {n}', 10, evens(10), 'srp', FUNCTION_11B) for n in (1, 2, 3)),
      '4-3', URB + AER, ID + 'p2-q11b', ('aerial',)),
    T('p2-11c', P2, '11C', '', 30, 26, L(26, 'Demographic Change'),
      (L(26, 'Explain how improvements in technology impact on population growth, with reference to',
         'that you have studied.'),),
      (S(30, 'Examples of specific improvements', None),),
      (pair('Examples of specific improvements in technology 2 + 2 marks', 'Examples of improvements in technology'),
       pair('Impacts named · 2 + 2 marks', 'Impacts named'), srp('Examination', 11, f'Examination · 11 x {SRPS}')),
      '4-1', POP, ID + 'p2-q11c'),
]
Q12AS = (L(27, 'Examine the data in the table above showing female life expectancy at birth in a number',
           'of European countries.'),)
PART_TWO += romans('12A', P2, 27, L(27, 'Life Expectancy', nth=0), Q12AS, ID + 'p2-q12a', ('page',), [
    ('(i)', 16, L(27, '(i) Using graph paper, draw a suitable graph to illustrate this data.'),
     S(31, 'Bar Chart · Pie Chart', '(ii) · State two'), graph('Each axis · 1+1 mark'), '2-0', TG),
    ('(ii)', 4, L(27, '(ii) State two reasons why life expectancy in general is increasing in Europe.'),
     S(31, 'Two reasons stated', None),
     (fixed('Two reasons', 4, 'Two reasons stated at 2 marks each', (0, 2, 4)),), '4-0', POP),
])
PART_TWO += [
    T('p2-12b', P2, '12B', '', 30, 27, L(27, 'Population Distribution'),
      (L(27, 'With reference to the Ordnance Survey map that accompanies this paper, use settlement',
         'shown on the map.'),),
      (S(32, 'Two map evidence', 'C. · Changing'),),
      (pair('Two map evidence · 2 + 2 marks', 'Map evidence'),
       pair('Two features of distribution · 2 + 2 marks', 'Features of distribution'),
       srp('Explanation', 11, f'Explanation · 11 x {SRPS}')),
      '4-3', URB + MAP + POP, ID + 'p2-q12b', ('map', 'legend')),
    T('p2-12c', P2, '12C', '', 30, 27, L(27, 'Changing Land-Use Patterns'),
      (L(27, 'Describe and explain the changing land-use patterns in an urban area that you have', 'studied.'),),
      (S(32, 'Land use patterns identified', None),),
      (pair('Land use patterns identified · 2 + 2 marks', 'Land use patterns identified'),
       fixed('Named urban area', 2, 'Named urban area · 2 marks'), srp('Examination', 12, f'Examination · 12 x {SRPS}')),
      '4-4', LAND + URB, ID + 'p2-q12c'),
]

# ------------------------------------------------------------------ Options --
# Coherence is graded inside each aspect; either printed scheme gives the
# discussion 24 SRPs (48 marks) and identifying plus coherence 32 marks.
OPTION_CRITERIA = (
    Criterion('Aspects identified and overall coherence (3 aspects: 4 + 7/6 marks each; 4 aspects: 4 + 4 marks each)',
              32, upto(32), 'exact', ('Number of aspects', 'Identifying aspect', 'Overall coherence')),
    Criterion('Discussion (3 aspects @ 8 x SRPs or 4 aspects @ 6 x SRPs)', 48, evens(48), 'srp', ('Discussion:',)),
)
# Option 18 prints three of four items and only the "3 @ 27 + 27 + 26" scheme.
ASPECT_18 = ('Number of aspects: · 3 @ 27 + 27 + 26', 'Identifying aspect: · 4 marks', 'Discussion: · 8 x SRPs',
             'Overall coherence: · 7/6 marks graded')
OPTION_CRITERIA_3 = (
    Criterion('Aspect 1 (identifying 4 + discussion 8 x SRPs + coherence 7)', 27, upto(27), 'srp', ASPECT_18),
    Criterion('Aspect 2 (identifying 4 + discussion 8 x SRPs + coherence 7)', 27, upto(27), 'srp', ASPECT_18),
    Criterion('Aspect 3 (identifying 4 + discussion 8 x SRPs + coherence 6)', 26, upto(26), 'srp', ASPECT_18),
)


def option(q, page, theme, note_nth, prompt, scheme_page, topic, atlas, after=None, end=None, absorbs=(),
           criteria=OPTION_CRITERIA):
    return T(f'p2-{q}', P2, q, '', 80, page, theme, prompt if isinstance(prompt, tuple) else (prompt,),
             (S(scheme_page, 'Number of aspects', end, None, after),), criteria,
             topic, (atlas,), ID + f'p2-q{q}',
             stem=(L(page, 'Note: It is better to discuss three or four aspects', 'large number of points.',
                     nth=note_nth),),
             absorbs=absorbs)


GI, GE = H + 'option-global-interdependence', H + 'option-geoecology'
CI, AO = H + 'option-culture-identity', H + 'option-atmosphere-ocean'
BIOMES = ('early settlement and the clearing of forests', 'the felling of tropical rain forests',
          'intensive agricultural practices', 'industrial development.')
OPTIONS = [
    option('13', 29, L(29, 'Global Interdependence'), 0,
           L(29, 'Examine the impact of Non-Governmental Organisations (NGOs) in empowering',
             'that you have studied.'), 34, '5-2', GI, after='13.', end='14.'),
    option('14', 29, L(29, 'Global Interdependence'), 0,
           L(29, 'Examine the role that national debt, fair trade and land ownership patterns play in the',
             'developing countries.'), 34, '5-2', GI, after='14.'),
    option('15', 29, L(29, 'Global Interdependence'), 0,
           L(29, 'Examine the causes and impacts of deforestation on a local and a global scale.'), 35, '5-1', GI),
    option('16', 29, L(29, 'Geoecology'), 1,
           L(29, 'Explain how weathering, leaching and podzolisation have impacted on the characteristics',
             'of soil.'), 36, '6-1', GE, after='16.', end='17.'),
    option('17', 29, L(29, 'Geoecology'), 1,
           L(29, 'Discuss how human activities can accelerate soil erosion.'), 36, '6-1', GE, after='17.'),
    option('18', 29, L(29, 'Geoecology'), 1,
           L(29, 'Examine how any three of the activities listed below can impact on biomes:',
             'industrial development.'), 37, '6-3', GE,
           absorbs=pool(ID + 'p2-q18-', BIOMES, 3)[1], criteria=OPTION_CRITERIA_3),
    option('19', 30, L(30, 'Culture and Identity'), 0,
           L(30, 'Conflicts can occur between national governments and cultural groups.', 'Discuss.'),
           38, '7-1', CI, after='19.', end='20.'),
    option('20', 30, L(30, 'Culture and Identity'), 0,
           L(30, 'Examine the impact of colonialism on racial distribution.'), 38, '7-0', CI, after='20.'),
    option('21', 30, L(30, 'Culture and Identity'), 0,
           L(30, 'Examine the importance of language as a cultural indicator.'), 39, '7-0', CI),
    option('22', 30, L(30, 'The Atmosphere - Ocean Environment'), 1,
           L(30, 'The characteristics of climate can change over time and space.',
             'with reference to examples that you have studied.'), 40, '8-4', AO, after='22.', end='23.'),
    option('23', 30, L(30, 'The Atmosphere - Ocean Environment'), 1,
           L(30, 'Examine the impact of rainfall on agriculture and on domestic water supplies.'),
           40, '8-5', AO, after='23.'),
    option('24', 30, L(30, 'The Atmosphere - Ocean Environment'), 1,
           L(30, 'Examine the exchange of water between the oceans and the atmosphere.'), 41, '8-2', AO),
]

TASKS = [*PART_ONE, *PART_TWO, *OPTIONS]

ID_CORRECTION_REASON = 'No 2012 Higher card shipped before this review; every card is new.'

# No 2012 Higher card was live on origin/main before this review.
LEGACY_IDS: list[str] = []
