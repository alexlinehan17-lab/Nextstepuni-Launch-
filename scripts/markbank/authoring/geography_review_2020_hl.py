"""Independent review ledger: Leaving Certificate Geography 2020 Higher Level.

Sources (English editions, harvested Paper Trail corpus; sizes and SHA-256
pinned in EXPECTED_SOURCES and the generated audit): Part One and Answerbook
LC005ALP042EV (48 pages), Part Two LC005ALP043EV (20 pages), marking scheme
LC005ALP000EV (52 pages), and the common companions — the 1:50 000 Arklow
map LC005CLP003EV, its legend LC005CLPC00EV and the Arklow aerial photograph
LC005CLP004EV (published only as a JPEG). 2020 is the first year Part One
and Part Two are separate booklets; Part One is 80 marks (any ten of twelve
@ 8), Part Two 320 (four questions @ 80).

Visual sweep (every page rendered and read on 2026-10-12):
  Part One booklet p1 cover; p2 instructions (Part One "Attempt any TEN";
  Part Two "attempt FOUR": one of Q1-3, one of Q4-6, one elective, one
  option); p3-p13 Questions 1-12 (p8 holds Q6 and Q7; Q8 prints four Google
  Street View images of Arklow; Q9 prints an elevation profile); p14 Part Two
  answerbook instructions; p15-p43 lined answer pages; p44-p47 graph paper;
  p48 copyright/back cover.
  Part Two booklet p1 cover; p2 Part Two instructions; p3 Section 1
  divider; p4-p9 Q1-Q6; p10 Section 2 divider; p11-p16 Electives Q7-Q12;
  p17 Section 3 divider and option note; p18-p19 Options Q13-Q24; p20 back
  cover ("Do not hand this up").
  Scheme p1 cover; p2-p3 notes and annotation key; p4 Part One table (two
  columns: Q1-Q6, Q7-Q12); p5 Part Two instructions; p6-p24 Q1-Q6; p25
  Section 2 divider; p26-p39 Q7-Q12; p40 Section 3 divider; p41 option
  outline and Overall Coherence descriptors; p42 option annotations; p43-p50
  Q13-Q24; p51 Irish-language bonus marks; p52 back cover.
  Companions: Arklow map extract (the Avoca River, the M11, the Glenart
  Walk); OS legend sheet; oblique aerial photograph of Arklow.

Boundaries and tariffs follow the 2021 Higher ledger: every part the scheme
prices separately is a task; a matching table under one printed instruction
is one task with a criterion per scheme row, in the printed row order: Q2(i)
Limestone (a) Shells and fishbones (b) Marble, Shale (a) Clay and silt (b)
Slate, Sandstone (a) Sand (b) Quartzite; Q3 prints (i) and (ii) side by
side: (i) Point bar=D, Terracettes=B, Scree=C, Sand dunes=A, (ii) Fluvial
Deposition, Soil Creep, Freeze Thaw Action, Coastal Deposition; Q4 likewise:
(i) Erratic=D, Cirque/Corrie=A, Drumlin=B, Outwash Plain=C, (ii) Glacial
Deposition, Glacial Erosion, Glacial Deposition, Fluvio-Glacial Processes;
Q5 (i) Geomorphological, Climatic, Core, Cultural and (ii) The Burren,
Mediterranean, GDA, Basque; Q6 T 24 82 V-shaped valley, T 19 77 River
braiding, T 27 76 Beach; Q8 A centre middleground, B right middleground,
C left background, D left foreground. Each column of the two-column Part
One table is read with its own clip. Q10's four true/false statements are
separately priced romans, so each is a task.

4A prints three bullets and the scheme prices four features: "Two named
urban centres" is two of them, so its two item criteria carry that bullet.
8C asks for evidence from "both" the map and the photograph; the scheme
prices "Aerial photograph OR OS map evidence" per reason, and the card
carries the scheme's line with all three documents.
"""

from geography_review import (
    Criterion, Lift, Route, SchemeSlice, Task, pool, evens, fixed, slug, srp, sums, upto,
)

YEAR = 2020
LEVEL = 'higher'
PAPER_PAGES = {1: 48, 2: 20}
SCHEME_PAGES = 52
QUESTION_TARIFFS = {1: {str(n): 8 for n in range(1, 13)},
                    2: {**{f'{n}{x}': (20 if x == 'A' else 30)
                           for n in range(1, 13) for x in 'ABC'},
                        **{str(n): 80 for n in range(13, 25)}}}

EXPECTED_SOURCES = {
    'paper1': ('LC005ALP042EV.pdf', 3120862),
    'paper2': ('LC005ALP043EV.pdf', 1127795),
    'scheme': ('LC005ALP000EV.pdf', 689712),
    'map': ('LC005CLP003EV.pdf', 4637231),
    'legend': ('LC005CLPC00EV.pdf', 869977),
    'aerial': ('LC005CLP004EV.jpg', 6218552),
}

PAGE_REVIEW = {
    'paper1': {1: 'cover', 2: 'instructions', **{p: 'question' for p in range(3, 14)},
               14: 'answerbook instructions', **{p: 'lined answer page' for p in range(15, 44)},
               **{p: 'graph-paper answer page' for p in range(44, 48)}, 48: 'copyright/back cover'},
    'paper2': {1: 'cover', 2: 'Part Two instructions', 3: 'section divider',
               **{p: 'question' for p in (*range(4, 10), *range(11, 17), 18, 19)},
               10: 'section divider', 17: 'section divider and option note',
               20: 'back cover (do not hand this up)'},
    'scheme': {1: 'cover', 2: 'notes', 3: 'notes and annotation key', 4: 'Part One table',
               5: 'Part Two instructions', **{p: 'Part Two allocation' for p in range(6, 25)},
               25: 'section divider', **{p: 'Part Two allocation' for p in range(26, 40)},
               40: 'section divider', 41: 'option outline and coherence descriptors',
               42: 'option annotations', **{p: 'option allocation' for p in range(43, 51)},
               51: 'Irish-language bonus marks', 52: 'back cover'},
}

EXPECTED_SELECTION_SCAN = [
    [1, 2, 'attempt any ten'], [1, 2, 'attempt four'], [1, 3, 'attempt any ten'],
    [2, 2, 'attempt four'], [2, 3, 'attempt two'], [2, 4, 'attempt one'],
    [2, 5, 'answer (i) or (ii)'], [2, 5, 'or one'], [2, 5, 'or one'],
    [2, 6, 'one of the following'],
    [2, 7, 'attempt one'], [2, 7, 'two of the following'],
    [2, 9, 'one of the following'],
    [2, 10, 'attempt one'],
    [2, 13, 'one of the following'],
    [2, 16, 'any one'],
    [2, 17, 'attempt one'],
    [2, 18, 'any two'], [2, 18, 'any one'],
]
SELECTION_REVIEW = [
    {'scan': [[1, 2, 'attempt any ten'], [1, 2, 'attempt four'], [1, 3, 'attempt any ten'],
              [2, 2, 'attempt four'], [2, 3, 'attempt two'], [2, 4, 'attempt one'],
              [2, 7, 'attempt one'], [2, 10, 'attempt one'], [2, 17, 'attempt one']],
     'kind': 'exam-attempt-rule',
     'reason': 'Part One any ten of twelve and Part Two four questions (one of Q1-3, one of Q4-6, one elective, one option) are attempt rules; every question is carded.'},
    {'scan': [[2, 5, 'answer (i) or (ii)'], [2, 5, 'or one'], [2, 5, 'or one']], 'kind': 'closed-route',
     'reason': '2B: (i) or (ii); (i) offers one fluvial OR one coastal OR one glacial landform -> 4 routes.'},
    {'scan': [[2, 6, 'one of the following']], 'kind': 'closed-choose-one',
     'reason': '3C one of four printed interactions with the rock cycle -> 4 routes.'},
    {'scan': [[2, 9, 'one of the following']], 'kind': 'closed-choose-one',
     'reason': '6C one of language or religion -> 2 routes.'},
    {'scan': [[2, 13, 'one of the following']], 'kind': 'closed-choose-one',
     'reason': '9B one of three printed activities -> 3 routes.'},
    {'scan': [[2, 16, 'any one']], 'kind': 'closed-choose-one',
     'reason': '12C any one of three printed factors -> 3 routes.'},
    {'scan': [[2, 7, 'two of the following'], [2, 18, 'any two']], 'kind': 'choose-n-one-card',
     'reason': '4B two of four printed factors and 14 any two of four printed themes -> one card each with every printed item (choice is not a route; the scheme marks each chosen item alike).'},
    {'scan': [[2, 18, 'any one']], 'kind': 'open-response',
     'reason': 'No printed pool: 17 any one soil type. Open choices are not fanned out: "one urban area", "one multinational company", "one developing economy", "example(s)". Compulsory lists stay whole: 1A, 4A, 7A and 10A each bullet, 1B each rock, 15 each heading.'},
]

P1, P2 = 1, 2
LEFT = (0.0, 0.0, 0.52, 1.0)
RIGHT = (0.52, 0.0, 1.0, 1.0)
# The two-column Part One table prints some answers in sub-columns.
Q2A_COL = (0.0, 0.29, 0.34, 0.345)
Q2B_COL = (0.34, 0.29, 0.52, 0.345)
Q3I_COL = (0.0, 0.40, 0.215, 0.47)
Q3II_COL = (0.215, 0.40, 0.52, 0.47)
Q4I_COL = (0.0, 0.505, 0.21, 0.575)
Q4II_COL = (0.21, 0.505, 0.52, 0.575)
Q5I_COL = (0.0, 0.61, 0.315, 0.68)
Q5II_COL = (0.315, 0.61, 0.52, 0.68)
ID = 'geography-2020-hl-'
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


def rows(lines, marks=1):
    return tuple(fixed(f'Row {i}', marks, line) for i, line in enumerate(lines, 1))


def pair(line, label):
    return fixed(label, 4, line, (0, 2, 4))


def one_plus_one(line, label):
    return fixed(label, 2, line, (0, 1, 2))


def romans(q, part, page, title, stem, first_id, sources, parts):
    """parts: (sub, marks, prompt Lift(s), scheme slice(s), criteria, topic, atlas[, row labels])."""
    out = []
    for index, item in enumerate(parts):
        sub, marks, prompt, scheme, criteria, topic, atlas = item[:7]
        labels = item[7] if len(item) > 7 else ()
        key = sub.strip('()').replace(')(', '-')
        out.append(T(f'p{part}-{q.lower()}-{key}', part, q, sub, marks, page, title,
                     prompt if isinstance(prompt, tuple) else (prompt,),
                     scheme if isinstance(scheme, tuple) else (scheme,), criteria, topic, atlas,
                     first_id if index == 0 else f'{first_id}-{key}', sources, stem,
                     row_labels=labels))
    return out


# ---------------------------------------------------------------- Part One --
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
ECON = (H + 'elective-economic',)
DEV = (H + 'economic-developing-economies',)
MNC = (H + 'economic-multinationals-globalisation',)
EU_ECON = (H + 'economic-european-union',)
ENERGY = (H + 'economic-energy',)
ENV = (H + 'economic-environmental-impact',)

Q1S = (L(3, 'Examine the map above showing the locations of all earthquakes', 'following questions.'),)
PART_ONE = romans('1', P1, 3, L(3, 'Earthquakes'), Q1S, ID + 'p1-q1', ('page',), [
    ('(i)', 2, L(3, '(i) What is the name of the area labelled X', 'occurred in 2018?'),
     S(4, 'Q1. (i)', '(ii) A =', LEFT), (fixed('Area', 2, 'Q1. (i) Pacific Ring of Fire · 2m'),), '0-7', EV + PS),
    ('(ii)', 2, L(3, '(ii) Name the tectonic plates labelled A and B in the map above.'),
     S(4, '(ii) A = Eurasian', '(iii) Transverse', LEFT),
     rows(['(ii) A = Eurasian · 1m', 'B = African · 1m']), '0-0', PS, (L(3, 'Plate A:'), L(3, 'Plate B:'))),
    ('(iii)', 2, L(3, '(iii) What type of plate boundary is located at C in the map above?'),
     S(4, '(iii) Transverse', '(iv) Seismograph', LEFT),
     (fixed('Plate boundary', 2, '(iii) Transverse/transform · 2m'),), '0-0', PS),
    ('(iv)', 2, L(3, '(iv) Name the instrument used to measure the force of an earthquake.'),
     S(4, '(iv) Seismograph', 'Q2. (i)', LEFT),
     (fixed('Instrument', 2, '(iv) Seismograph/seismometer · 2m'),), '0-7', EV),
])

PART_ONE += [
    T('p1-2-i', P1, '2', '(i)', 6, 4, L(4, 'Sedimentary Rocks'),
      (L(4, '(i) The list below contains a number of source materials', 'a number of metamorphic rocks.'),
       L(4, 'Slate'), L(4, 'Clay and silt'), L(4, 'Marble'), L(4, 'Shells and fishbones'), L(4, 'Sand', nth=0),
       L(4, 'Quartzite'),
       L(4, 'Complete the table below by inserting the correct terms from the list', 'most associated with it.', nth=0)),
      (S(4, '(a) Shells', None, Q2A_COL), S(4, '(b) Marble', None, Q2B_COL)),
      (fixed('Limestone: (a) source material', 1, '(a) Shells and fishbones 1m'),
       fixed('Limestone: (b) metamorphic rock', 1, '(b) Marble 1m'),
       fixed('Shale: (a) source material', 1, 'Clay and silt 1m'),
       fixed('Shale: (b) metamorphic rock', 1, 'Slate 1m'),
       fixed('Sandstone: (a) source material', 1, 'Sand · 1m'),
       fixed('Sandstone: (b) metamorphic rock', 1, 'Quartzite 1m')),
      '0-1', RW, ID + 'p1-q2', ('page',)),
    T('p1-2-ii', P1, '2', '(ii)', 2, 4, L(4, 'Sedimentary Rocks'),
      (L(4, '(ii) State whether the following statement is true or false.'),
       L(4, 'Silica is an example of an agent that binds', 'sedimentary rock together.')),
      (S(4, '(ii) True', 'Q3. (i)', LEFT),), (fixed('True or false', 2, '(ii) True 2m'),),
      '0-1', RW, ID + 'p1-q2-ii'),
]

Q3S = (L(5, 'Examine the photographs above and answer each of the following questions.'),)
Q3_ROWS = (L(5, 'Point bar'), L(5, 'Terracettes'), L(5, 'Scree', nth=0), L(5, 'Sand dunes'))
Q4S = (L(6, 'Examine the photographs above and answer each of the following questions.'),)
Q4_ROWS = (L(6, 'Erratic'), L(6, 'Cirque/Corrie'), L(6, 'Drumlin'), L(6, 'Outwash Plain'))
PART_ONE += [
    T('p1-3-i', P1, '3', '(i)', 4, 5, L(5, 'Physical Features and Processes'),
      (L(5, '(i) Match each of the photographs A, B, C and D with the feature', 'table below.', nth=0),),
      (S(4, 'Q3. (i)', None, Q3I_COL),), rows(['Q3. (i) D 1m', '=B 1m', '=C 1m', '=A 1m']),
      '0-4', RIVERS + RW + SEA, ID + 'p1-q3', ('page',), Q3S, row_labels=Q3_ROWS),
    T('p1-3-ii', P1, '3', '(ii)', 4, 5, L(5, 'Physical Features and Processes'),
      (L(5, '(ii) Match each of the following processes with the feature', 'Coastal deposition.'),),
      (S(4, '(ii) · Fluvial', None, Q3II_COL),),
      rows(['(ii) · Fluvial Deposition 1m', 'Soil Creep 1m', 'Freeze Thaw Action 1m', 'Coastal Deposition 1m']),
      '0-4', RIVERS + RW + SEA, ID + 'p1-q3-ii', ('page',), Q3S, row_labels=Q3_ROWS),
    T('p1-4-i', P1, '4', '(i)', 4, 6, L(6, 'Glaciation'),
      (L(6, '(i) Match each of the photographs A, B, C and D with the feature', 'table below.', nth=0),),
      (S(4, 'Q4. (i)', None, Q4I_COL),), rows(['Q4. (i) D 1m', '=A 1m', '=B 1m', '=C 1m']),
      '0-11', GLAC, ID + 'p1-q4', ('page',), Q4S, row_labels=Q4_ROWS),
    T('p1-4-ii', P1, '4', '(ii)', 4, 6, L(6, 'Glaciation'),
      (L(6, '(ii) Indicate, by ticking the correct box', 'glacial erosion or glacial deposition.'),),
      (S(4, '(ii) · Glacial Deposition', None, Q4II_COL),),
      rows(['(ii) · Glacial Deposition 1m', 'Glacial Erosion 1m', '=Glacial Deposition 1m',
            'Fluvio-Glacial Processes 1m']),
      '0-11', GLAC, ID + 'p1-q4-ii', ('page',), Q4S, row_labels=Q4_ROWS),
]

Q5_ROWS = (L(7, 'A region with a unique landscape based on rock type, structure or relief.'),
           L(7, 'A region with unique temperature and precipitation characteristics.'),
           L(7, 'A well-developed socio-economic region that attracts industry and people.'),
           L(7, 'A region where people share a specific language, religion and/or way of life.'))
Q5S = (L(7, 'Answer each of the following questions in the table below.'),)
PART_ONE += [
    T('p1-5-i', P1, '5', '(i)', 4, 7, L(7, 'Concept of a Region'),
      (L(7, '(i) Match each of the following types of region with the description', 'best matches it:'),
       L(7, 'Climatic', nth=0), L(7, 'Cultural', nth=0), L(7, 'Geomorphological', nth=0), L(7, 'Core', nth=0)),
      (S(4, 'Q5. (i)', None, Q5I_COL),),
      rows(['Q5. (i) Geomorphological 1m', 'Climatic 1m', 'Core 1m', 'Cultural · 1m']),
      '1-0', IRL + EURO, ID + 'p1-q5', ('page',), Q5S, row_labels=Q5_ROWS),
    T('p1-5-ii', P1, '5', '(ii)', 4, 7, L(7, 'Concept of a Region'),
      (L(7, '(ii) Match each of the following examples of regions with the description', 'best matches it:'),
       L(7, 'Basque Country'), L(7, 'The Burren'), L(7, 'Greater Dublin Area'), L(7, 'Mediterranean', nth=0)),
      (S(4, '(ii) The Burren', None, Q5II_COL),),
      rows(['(ii) The Burren 1m', 'Mediterranean 1m', 'GDA 1m', 'Basque · 1m']),
      '1-0', IRL + EURO, ID + 'p1-q5-ii', ('page',), Q5S, row_labels=Q5_ROWS),
]

Q6S = (L(8, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper and answer',
         'following questions.', nth=0),)
Q7S = (L(8, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper and answer',
         'following questions.', nth=1),)
PART_ONE += [
    T('p1-6-i', P1, '6', '(i)', 6, 8, L(8, 'Landscape Identification'),
      (L(8, '(i) In the table below, match each of the following features', 'V-shaped valley.'),),
      (S(4, 'Q6. · (i)', '(ii) · 266', LEFT),),
      rows(['Q6. · (i) · V-shaped valley 2m', 'River braiding 2m', 'Beach 2m'], 2),
      '2-6', MAP + RIVERS + SEA, ID + 'p1-q6', ('map', 'legend'), Q6S,
      row_labels=(L(8, 'T 24 82'), L(8, 'T 19 77'), L(8, 'T 27 76'))),
    T('p1-6-ii', P1, '6', '(ii)', 2, 8, L(8, 'Landscape Identification'),
      (L(8, '(ii) What is the height of the land, in metres, at the spot height located at T 239 804?'),),
      (S(4, '(ii) · 266', 'Page 2 of', LEFT),), (fixed('Height', 2, '(ii) · 266 (metres) 2m'),),
      '2-6', MAP, ID + 'p1-q6-ii', ('map', 'legend'), Q6S),
]
PART_ONE += romans('7', P1, 8, L(8, 'Ordnance Survey Map'), Q7S, ID + 'p1-q7', ('map', 'legend'), [
    ('(i)', 2, L(8, '(i) Name the public service located at T 256 742.'), S(4, 'Q7. · (i)', '(ii) · T 242', RIGHT),
     (fixed('Public service', 2, 'Q7. · (i) · Parking 2m'),), '2-6', MAP),
    ('(ii)', 2, L(8, '(ii) Give a six-figure grid reference for the railway station in Arklow.'),
     S(4, '(ii) · T 242', '(iii) · 6.2', RIGHT), (fixed('Grid reference', 2, '(ii) · T 242 729 2m'),), '2-6', MAP),
    ('(iii)', 2, L(8, '(iii) Measure the length, in kilometres, of the M11 motorway', 'T 229 710.'),
     S(4, '(iii) · 6.2', '(iv) 36', RIGHT), (fixed('Length', 2, '(iii) · 6.2 (km) 2m'),), '2-6', MAP),
    ('(iv)', 2, L(8, '(iv) Calculate the area, in square kilometres, of the land west of easting 22.'),
     S(4, '(iv) 36', 'Q8.', RIGHT), (fixed('Area', 2, '(iv) 36 (km2) 2m'),), '2-6', MAP),
])

PART_ONE.append(T(
    'p1-8', P1, '8', '', 8, 9, L(9, 'Aerial Photograph', nth=0),
    (L(9, 'Using accepted notation, give the location on the aerial photograph', 'in the table below.'),),
    (S(4, 'Q8.', 'Q9.', RIGHT),),
    rows(['Q8. · A = Centre / centre middleground 2m', 'B = Right middleground 2m', 'C = Left background 2m',
          'D = Left foreground 2m'], 2),
    '2-8', AER, ID + 'p1-q8', ('page', 'aerial'),
    (L(9, 'Examine the aerial photograph of Arklow accompanying this paper', 'same area of Arklow.'),),
    row_labels=(L(9, 'A', nth=1), L(9, 'B', nth=1), L(9, 'C', nth=1), L(9, 'D', nth=1))))

Q9S = (L(10, 'Locate point X, T 190 760', 'on the Ordnance Survey map.', nth=0),
       L(10, 'Using the 1:50 000 Ordnance Survey map and legend and the elevation profile above',
         'following questions.'))
PART_ONE += romans('9', P1, 10, L(10, 'Ordnance Survey Map'), Q9S, ID + 'p1-q9', ('page', 'map', 'legend'), [
    ('(i)', 2, L(10, '(i) What type of forestry is located at A?'), S(4, 'Q9. · (i)', '(ii) M11', RIGHT),
     (fixed('Forestry', 2, 'Q9. · (i) Mixed 2m'),), '2-6', MAP),
    ('(ii)', 2, L(10, '(ii) What is the name of the road located at B?'), S(4, '(ii) M11', '(iii) 140', RIGHT),
     (fixed('Road', 2, '(ii) M11 2m'),), '2-6', MAP),
    ('(iii)', 2, L(10, '(iii) What is the altitude, in metres, of the highest point along the elevation profile?'),
     S(4, '(iii) 140', '(iv) T 264', RIGHT), (fixed('Altitude', 2, '(iii) 140 (metres) 2m'),), '2-6', MAP),
    ('(iv)', 2, L(10, '(iv) Give a six-figure grid reference for the point on the R750 road located at C.'),
     S(4, '(iv) T 264', 'Q10.', RIGHT), (fixed('Grid reference', 2, '(iv) T 264 760 2m'),), '2-6', MAP),
])

Q10S = (L(11, 'Examine the weather chart above from Met Éireann.', 'true or false.'),)
PART_ONE += romans('10', P1, 11, L(11, 'Weather'), Q10S, ID + 'p1-q10', ('page',), [
    ('(i)', 2, L(11, '(i) There is an anticyclone located over Scandinavia.'),
     S(4, 'Q10. (i)', '(ii) · False', RIGHT), (fixed('True or false', 2, 'Q10. (i) · True 2m'),), '2-7', WX),
    ('(ii)', 2, L(11, '(ii) The barometric pressure over Dublin is 1016 hPa.'),
     S(4, '(ii) · False', '(iii) · True', RIGHT), (fixed('True or false', 2, '(ii) · False 2m'),), '2-7', WX),
    ('(iii)', 2, L(11, '(iii) There is little or no wind over Ireland.'),
     S(4, '(iii) · True', '(iv) · False', RIGHT), (fixed('True or false', 2, '(iii) · True 2m'),), '2-7', WX),
    ('(iv)', 2, L(11, '(iv) Lines on a weather map that join areas of equal atmospheric pressure', 'isohyets.'),
     S(4, '(iv) · False', 'Q11.', RIGHT), (fixed('True or false', 2, '(iv) · False 2m'),), '2-7', WX),
])

Q11S = (L(12, 'Examine the infographic above which shows population estimates', 'following questions.'),)
PART_ONE += romans('11', P1, 12, L(12, 'Population Statistics – Ireland'), Q11S, ID + 'p1-q11', ('page',), [
    ('(i)', 2, L(12, '(i) How many Irish nationals were estimated to live in Ireland in April 2019?'),
     S(4, 'Q11. (i)', '(ii) · 2,483', RIGHT), (fixed('Irish nationals', 2, 'Q11. (i) · 4,298,800 2m'),), '2-0', TG),
    ('(ii)', 2, L(12, '(ii) Calculate X, the number of females estimated to live in Ireland in April 2019.'),
     S(4, '(ii) · 2,483', '(iii) · 28.3', RIGHT), (fixed('Females', 2, '(ii) · 2,483,500 2m'),), '2-0', TG),
    ('(iii)', 2, L(12, '(iii) What percentage of the total population for Ireland was estimated to live in Dublin?'),
     S(4, '(iii) · 28.3', '(iv) · Two valid ways', RIGHT), (fixed('Percentage', 2, '(iii) · 28.3(%) 2m'),),
     '2-0', TG),
    ('(iv)', 2, L(12, '(iv) State two ways that population statistics can be used by the government.'),
     S(4, '(iv) · Two valid ways', 'Q12.', RIGHT),
     (one_plus_one('(iv) · Two valid ways 1m + 1m', 'Two ways'),), '4-0', POP),
])

Q12S = (L(13, 'Examine the map above showing the projected temperature increase', 'following questions.'),)
PART_ONE += romans('12', P1, 13, L(13, 'Statistical Interpretation'), Q12S, ID + 'p1-q12', ('page',), [
    ('(i)', 2, L(13, '(i) Name the city that is projected to have the highest increase', 'warmest month.'),
     S(4, 'Q12. (i)', '(ii) · 6.1', RIGHT), (fixed('City', 2, 'Q12. (i) · Ljubljana 2m'),), '2-0', TG + WX),
    ('(ii)', 2, L(13, '(ii) What is the projected temperature increase, in °C, for the warmest month in Paris?'),
     S(4, '(ii) · 6.1', '(iii) · 0.4', RIGHT), (fixed('Temperature increase', 2, '(ii) · 6.1 – 7.0 (°C) 2m'),),
     '2-0', TG + WX),
    ('(iii)', 2, L(13, '(iii) Calculate the difference in projected temperature increase', 'warmest month in London.'),
     S(4, '(iii) · 0.4', '(iv) · Two valid examples', RIGHT), (fixed('Difference', 2, '(iii) · 0.4 (°C) 2m'),),
     '2-0', TG + WX),
    ('(iv)', 2, L(13, '(iv) Many countries are investing in renewable energy', 'examples of renewable energy.'),
     S(4, '(iv) · Two valid examples', 'f 49', RIGHT),
     (one_plus_one('(iv) · Two valid examples 1m + 1m', 'Two examples'),), '3-5', ENERGY),
])


# ---------------------------------------------------------------- Part Two --
def sketch(outline_line, outline_permitted, alloc, item_permitted, labels):
    return (fixed('Sketch outline' if 'Sketch' in outline_line else 'Map outline', 4,
                  outline_line, outline_permitted),
            *(Criterion(f'Feature {n}', 4, item_permitted, 'exact', alloc) for n in range(1, labels + 1)))


OS_SKETCH = sketch('Sketch Outline · 4 marks (4/0)', (0, 4),
                   ('4 features @ 4 marks each:', 'Label 1 mark'), sums((0, 1, 3), (0, 1)), 4)
AERIAL_SKETCH = sketch('Sketch Outline · 4 marks (4/0)', (0, 4),
                       ('4 features @ 4 marks each', 'Named 1 mark'), sums((0, 1, 3), (0, 1)), 4)
BAR_GRAPH = (fixed('Title', 2, ('Bar Chart', 'Title · 2 marks')),
             fixed('Axes named', 2, ('Vertical axis named · 1 mark', 'Horizontal axis named · 1 mark'), (0, 1, 2)),
             fixed('6 items illustrated', 12, '6 items illustrated · 2 marks each graded (2/1/0)', upto(12)))
GRAPH = (fixed('Title', 2, ('Bar Chart · Pie Chart', 'Title · 2 marks · 2 marks')),
         fixed('Axes named (bar chart) / circle and centre (pie chart)', 2,
               ('Vertical axis named', 'Horizontal axis named'), (0, 1, 2)),
         fixed('6 items illustrated', 12, '6 items illustrated', upto(12)))


def split(label, total, first, second):
    return srp(label, total, (first, second))


def bullet_routes(prefix, items, atlas=None, topic=None):
    return tuple(Route(slug(item, 34), item.rstrip('.'), ID + prefix + slug(item, 34), False,
                       keep_bullets=(item,), atlas=(atlas[item] if atlas else None),
                       topic=(topic[item] if topic else None))
                 for item in items)


LANDFORMS = 'one fluvial landform or one coastal landform or one glacial landform'
PART_TWO = [
    T('p2-1a', P2, '1A', '', 20, 4, L(4, 'Ordnance Survey Map'),
      (L(4, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper.', 'in the north of the map.'),),
      (S(6, 'Sketch Outline', 'Annotation'),), OS_SKETCH, '2-6', MAP + RIVERS + SEA, ID + 'p2-q1a', ('map', 'legend'),
      row_labels=(None, L(4, 'The entire course of the Avoca River'), L(4, 'A feature of coastal deposition'),
                  L(4, 'The entire route of the waymarked walk named the Glenart Walk'),
                  L(4, 'The entire area of land above 200 metres at Ballydonnell in the north of the map.'))),
    T('p2-1b', P2, '1B', '', 30, 4, L(4, 'Rocks'),
      (L(4, 'Explain the formation of each of the following, with reference to examples', 'One metamorphic rock.'),),
      (S(7, 'One plutonic igneous rock named', 'Annotation'),),
      (fixed('One plutonic igneous rock named', 2, 'One plutonic igneous rock named · 2 marks'),
       fixed('One metamorphic rock named', 2, 'One metamorphic rock named · 2 marks'),
       split('Explanation of formation of the two rocks (6/7 SRPs each)', 13,
             f'Explanation of formation of plutonic igneous rock · 6/7 x {SRPS}',
             f'Explanation of formation of metamorphic rock · 6/7x {SRPS}')),
      '0-1', RW, ID + 'p2-q1b'),
    T('p2-1c', P2, '1C', '', 30, 4, L(4, 'Plate Boundaries'),
      (L(4, 'Describe and explain constructive plate boundaries.'),),
      (S(8, 'Description/Explanation · 15', 'Annotation'),),
      (srp('Description/explanation', 15, f'Description/Explanation · 15 x {SRPS}'),),
      '0-0', PS, ID + 'p2-q1c'),
]

Q2AS = (L(5, 'Examine the diagram above which shows the impact of folding', 'following questions.'),)
PART_TWO += romans('2A', P2, 5, L(5, 'Folding and Faulting'), Q2AS, ID + 'p2-q2a', ('page',), [
    ('(i)', 2, L(5, '(i) Name the part of a fold, labelled A', 'pushed upwards.'),
     S(9, '(i) · Anticline', '(ii) · Syncline'), (fixed('Part of a fold', 2, '(i) · Anticline · 2 marks'),), '0-2', RW + PS),
    ('(ii)', 2, L(5, '(ii) Name the part of a fold, labelled B', 'pushed downwards.'),
     S(9, '(ii) · Syncline', '(iii) Any valid'), (fixed('Part of a fold', 2, '(ii) · Syncline · 2 marks'),), '0-2', RW + PS),
    ('(iii)', 2, L(5, '(iii) Name one Irish mountain range that was formed as part of the Armorican folding.'),
     S(9, '(iii) Any valid', '(iv) Any valid'), (fixed('Mountain range', 2, '(iii) Any valid mountain range · 2 marks'),),
     '0-2', RW + PS),
    ('(iv)', 2, L(5, '(iv) Name a different period of fold mountain building', 'last 400 million years.'),
     S(9, '(iv) Any valid', '(v) · Valid brief'), (fixed('Period of fold mountain building', 2,
                                                         '(iv) Any valid orogeny · 2 marks'),), '0-2', RW + PS),
    ('(v)', 4, L(5, '(v) Explain briefly the term compression as it relates to folding.'),
     S(9, '(v) · Valid brief', '(vi) Two types'), (pair('(v) · Valid brief explanation · 2 + 2 marks', 'Explanation'),),
     '0-2', RW + PS),
    ('(vi)', 4, L(5, '(vi) Name two types of fault.'),
     S(9, '(vi) Two types', '(vii) Two features'), (pair('(vi) Two types named · 2 + 2 marks', 'Two types of fault'),),
     '0-2', RW + PS),
    ('(vii)', 4, L(5, '(vii) Name two landscape features formed by faulting.'),
     S(9, '(vii) Two features', 'Page 7 of'), (pair('(vii) Two features named · 2 + 2 marks', 'Two features'),),
     '0-2', RW + PS),
])

EROSION = (fixed('Process of erosion named', 2, 'Process of erosion named · 2 marks'),
           fixed('Landform named', 2, 'Landform named · 2 marks'),
           srp('Examination', 13, f'Examination · 13 x {SRPS}'))
ROCK_CYCLE = ('Mining', 'Extracting building materials', 'Oil/gas exploitation', 'Geothermal energy production.')
PART_TWO += [
    T('p2-2b', P2, '2B', '', 30, 5, L(5, 'Surface Processes'),
      (L(5, '(i) Examine the role of the processes of erosion on the formation', 'that you have studied.', nth=0),),
      (S(10, 'Process of erosion named · 2 marks', 'Annotation'),), EROSION,
      '0-9', RIVERS, ID + 'p2-q2b-route-i-fluvial-landform',
      routes=(
          Route('route-i-fluvial-landform', 'Route (i) · one fluvial landform',
                ID + 'p2-q2b-route-i-fluvial-landform', False, ((LANDFORMS, 'one fluvial landform'),),
                topic='0-9', atlas=RIVERS),
          Route('route-i-coastal-landform', 'Route (i) · one coastal landform',
                ID + 'p2-q2b-route-i-coastal-landform', False, ((LANDFORMS, 'one coastal landform'),),
                topic='0-10', atlas=SEA),
          Route('route-i-glacial-landform', 'Route (i) · one glacial landform',
                ID + 'p2-q2b-route-i-glacial-landform', False, ((LANDFORMS, 'one glacial landform'),),
                topic='0-11', atlas=GLAC),
          Route('route-ii', 'Route (ii)', ID + 'p2-q2b-route-ii', False,
                prompt=(L(5, '(ii) Describe and explain the factors governing the operation', 'that you have studied.',
                          nth=0),),
                scheme=(S(11, 'Mass movement process named', 'Annotation'),),
                criteria=(fixed('Mass movement process named', 2, 'Mass movement process named · 2 marks'),
                          pair('Factors identified · 2 + 2 marks', 'Factors identified'),
                          srp('Description/explanation of process', 12,
                              f'Description/Explanation of process · 12 x {SRPS}')),
                topic='0-8', atlas=RW),
      )),
    T('p2-2c', P2, '2C', '', 30, 5, L(5, 'Weathering'),
      (L(5, 'Explain one process of physical weathering and one process of chemical weathering.'),),
      (S(12, 'Physical weathering process named', 'Annotation'),),
      (fixed('Physical weathering process named', 2, 'Physical weathering process named · 2 marks'),
       fixed('Chemical weathering process named', 2, 'Chemical weathering process named · 2 marks'),
       split('Explanation of the two processes (6/7 SRPs each)', 13,
             f'Explanation of physical weathering · 6/7 x {SRPS}', f'Explanation of chemical weathering · 6/7 x {SRPS}')),
      '0-8', RW, ID + 'p2-q2c'),
]

Q3AS = (L(6, 'Examine the diagram above which shows a karst landscape', 'following questions.'),)
PART_TWO += romans('3A', P2, 6, L(6, 'Karst Landscapes'), Q3AS, ID + 'p2-q3a', ('page',), [
    ('(i)', 6, L(6, '(i) Name the features labelled A, B and C in the diagram above.'),
     S(13, '(i) · A = Stalactite', '(ii) · True'),
     (fixed('A', 2, '(i) · A = Stalactite · 2 marks'), fixed('B', 2, 'B = Stalagmite · 2 marks'),
      fixed('C', 2, 'C = Pillar/column · 2 marks')), '0-3', KARST),
    ('(ii)', 2, (L(6, '(ii) State whether the following statement is true or false.'),
                 L(6, 'A doline is the term that describes the feature', 'the area around D.')),
     S(13, '(ii) · True', '(iii) Two valid'), (fixed('True or false', 2, '(ii) · True · 2 marks'),), '0-3', KARST),
    ('(iii)', 4, L(6, '(iii) Name two features formed on the surface of a karst landscape.'),
     S(13, '(iii) Two valid', '(iv) Limestone'), (pair('(iii) Two valid features named · 2 + 2 marks', 'Two features'),),
     '0-3', KARST),
    ('(iv)', 2, L(6, '(iv) What type of rock is most associated with karst landscapes?'),
     S(13, '(iv) Limestone', '(v) · E ='), (fixed('Rock', 2, '(iv) Limestone · 2 marks'),), '0-3', KARST + RW),
    ('(v)', 2, L(6, '(v) What is the term given to the horizontal lines found in sedimentary rock, shown at E?'),
     S(13, '(v) · E =', '(vi) Carbonation'), (fixed('Term', 2, '(v) · E = Bedding planes · 2 marks'),), '0-3', KARST),
    ('(vi)', 2, L(6, '(vi) What type of chemical weathering is most associated with the formation', 'landscape?'),
     S(13, '(vi) Carbonation', '(vii) Valid'), (fixed('Chemical weathering', 2, '(vi) Carbonation · 2 marks'),),
     '0-3', KARST + RW),
    ('(vii)', 2, L(6, '(vii) State what is meant by the term permeable rock.'),
     S(13, '(vii) Valid', 'Page 11 of'), (fixed('Statement', 2, '(vii) Valid statement · 2 marks'),), '0-3', KARST + RW),
])

PART_TWO += [
    T('p2-3b', P2, '3B', '', 30, 6, L(6, 'Isostasy'),
      (L(6, 'Describe and explain how isostasy has shaped the Irish landscape.'),),
      (S(14, 'Impact / Feature identified', 'Annotation'),),
      (fixed('Impact / feature identified', 2, 'Impact / Feature identified · 2 marks'),
       srp('Description/explanation', 14, 'Description/Explanation · 14 x SRPs')),
      '0-5', RIVERS + SEA, ID + 'p2-q3b'),
    T('p2-3c', P2, '3C', '', 30, 6, L(6, 'Human Interaction with the Rock Cycle'),
      (L(6, 'Humans interact with the rock cycle in a number of ways.'),
       L(6, 'Describe and explain how this interaction with the rock cycle takes place', 'Geothermal energy production.')),
      (S(15, 'Description/Explanation · 15', 'Annotation'),),
      (srp('Description/explanation', 15, f'Description/Explanation · 15 x {SRPS}'),),
      '0-6', RW, ID + 'p2-q3c-mining', routes=bullet_routes('p2-q3c-', ROCK_CYCLE)),
]

FACTORS_4B = ('Raw materials', 'Markets', 'Infrastructure', 'Government policy.')
PART_TWO += [
    T('p2-4a', P2, '4A', '', 20, 7, L(7, 'Map Skills'),
      (L(7, 'Draw an outline map of a Continental / Sub-Continental region (not in Europe)', 'Two named urban centres.'),),
      (S(16, 'Map outline', 'Page 14 of'),),
      sketch('Map outline · 4 marks graded (4/2/0)', (0, 2, 4),
             ('4 features @ 4 marks each · Shown 2 marks graded (2/1/0)', 'Named 2 marks'), sums((0, 1, 2), (0, 2)), 4),
      '1-6', CONT, ID + 'p2-q4a',
      row_labels=(None, L(7, 'A named river'), L(7, 'The outline of a named feature of relief (upland or lowland)'),
                  L(7, 'Two named urban centres.'), L(7, 'Two named urban centres.'))),
    T('p2-4b', P2, '4B', '', 30, 7, L(7, 'Secondary Economic Activity'),
      (L(7, 'Examine the development of secondary economic activity in a European region', 'Government policy.'),),
      (S(17, 'Factor 1 examination', 'Annotation'),),
      (srp('Factor 1 examination', 8, f'Factor 1 examination · 8 x {SRPS}'),
       srp('Factor 2 examination', 7, f'Factor 2 examination · 7 x {SRPS}')),
      '1-5', EURO, ID + 'p2-q4b', absorbs=pool(ID + 'p2-q4b-', FACTORS_4B, 2)[1]),
    T('p2-4c', P2, '4C', '', 30, 7, L(7, 'Urban Development'),
      (L(7, 'Examine the factors that have influenced the development of one urban area in an Irish',
         'that you have studied.', nth=0),),
      (S(18, 'Urban area named · 2 marks', 'Annotation'),),
      (fixed('Urban area named', 2, 'Urban area named · 2 marks'), pair('Factors identified · 2 + 2 marks', 'Factors identified'),
       srp('Examination', 12, f'Examination · 12 x {SRPS}')),
      '1-4', IRL + URB, ID + 'p2-q4c'),
]

Q5AS = (L(8, 'Examine the graphic above showing Irish tourism data for 2017', 'following questions.'),)
PART_TWO += romans('5A', P2, 8, L(8, 'Tourism', nth=0), Q5AS, ID + 'p2-q5a', ('page',), [
    ('(i)', 2, L(8, '(i) How many trips were taken by Irish residents within the Republic of Ireland in 2017?'),
     S(19, '(i) · 9.6', '(ii) · 694'), (fixed('Trips', 2, '(i) · 9.6 million · 2 marks'),), '2-0', TG),
    ('(ii)', 2, L(8, '(ii) How much money (in € million) did overseas tourists spend on trips to the West?'),
     S(19, '(ii) · 694', '(iii) 65.6'), (fixed('Money spent', 2, '(ii) · 694 (€ million) · 2 marks'),), '2-0', TG),
    ('(iii)', 4, L(8, '(iii) What percentage of overseas tourists that visited the Republic of Ireland', 'Dublin?'),
     S(19, '(iii) 65.6', '(iv) Two valid'), (fixed('Percentage', 4, '(iii) 65.6 (%) · 4 marks'),), '2-0', TG),
    ('(iv)', 8, L(8, '(iv) Explain briefly two reasons why more overseas tourists visited Dublin', 'West.'),
     S(19, '(iv) Two valid', '(v) · Valid brief'),
     (pair('(iv) Two valid brief explanations 2 + 2 marks', 'First reason'), pair('=2 + 2 marks', 'Second reason')),
     '1-4', IRL),
    ('(v)', 4, L(8, '(v) Explain briefly one challenge facing the Irish tourist industry.'),
     S(19, '(v) · Valid brief', 'Page 17 of'), (pair('(v) · Valid brief explanation · 2 + 2 marks', 'Challenge'),),
     '1-4', IRL),
])
PART_TWO += [
    T('p2-5b', P2, '5B', '', 30, 8, L(8, 'Population Dynamics'),
      (L(8, 'Account for population distribution throughout a Continental / Sub-Continental region',
         'that you have studied.'),),
      (S(20, 'Examination · 15', 'Annotation'),), (srp('Examination', 15, f'Examination · 15 x {SRPS}'),),
      '1-6', CONT + POP, ID + 'p2-q5b'),
    T('p2-5c', P2, '5C', '', 30, 8, L(8, 'Socio-Economic Regions'),
      (L(8, 'Discuss how economic activity in core regions differs from economic activity in peripheral',
         'regions.'),),
      (S(21, 'Discussion · 15', 'Annotation'),), (srp('Discussion', 15, f'Discussion · 15 x {SRPS}'),),
      '1-0', IRL + EURO, ID + 'p2-q5c'),
]

Q6AS = (L(9, 'Examine the table above showing information on foreign multinational companies',
          'following questions.'),)
PART_TWO += romans('6A', P2, 9, L(9, 'Economic Activity', nth=0), Q6AS, ID + 'p2-q6a', ('page',), [
    ('(i)', 2, L(9, '(i) In what year was there a 0.7% growth in employment in MNCs?'),
     S(22, '(i) · 2014', '(ii) · 2,231'), (fixed('Year', 2, '(i) · 2014 · 2 marks'),), '2-0', TG),
    ('(ii)', 2, L(9, '(ii) What was the total employment (in thousands) in 2017?'),
     S(22, '(ii) · 2,231', '(iii) 14.4'), (fixed('Total employment', 2, '(ii) · 2,231 · 2 marks'),), '2-0', TG),
    ('(iii)', 4, L(9, '(iii) Calculate X, the percentage share of total employment attributed to MNCs in 2016.'),
     S(22, '(iii) 14.4', '(iv) Two valid'), (fixed('Percentage', 4, '(iii) 14.4 (%) · 4 marks'),), '2-0', TG),
    ('(iv)', 8, L(9, '(iv) Explain briefly two reasons why MNCs are attracted to set up in Ireland.'),
     S(22, '(iv) Two valid', '(v) · Valid brief'),
     (pair('(iv) Two valid brief explanations · 2 + 2 marks', 'First reason'), pair('=2 + 2 marks', 'Second reason')),
     '3-2', MNC + IRL),
    ('(v)', 4, L(9, '(v) Explain briefly one challenge facing MNCs located in Ireland.'),
     S(22, '(v) · Valid brief', 'Page 20 of'), (pair('(v) · Valid brief explanation · 2 + 2 marks', 'Challenge'),),
     '3-2', MNC + IRL),
])
CULTURE = ('Language', 'Religion.')
PART_TWO += [
    T('p2-6b', P2, '6B', '', 30, 9, L(9, 'Primary Economic Activity'),
      (L(9, 'Examine the physical factors that influence the development of agriculture in two',
         'that you have studied.'),),
      (S(23, 'Physical factors identified', 'Annotation'),),
      (pair('Physical factors identified · 2 + 2 marks', 'Physical factors identified'),
       srp('Examination', 13, f'Examination · 13 x {SRPS}')),
      '1-4', IRL, ID + 'p2-q6b'),
    T('p2-6c', P2, '6C', '', 30, 9, L(9, 'Concept of a Region'),
      (L(9, 'Examine how one of the following can be used to define cultural regions', 'Religion.'),),
      (S(24, 'Example of region defined by language/religion · 2 marks', 'Annotation'),),
      (fixed('Example of region defined by language/religion', 2,
             'Example of region defined by language/religion · 2 marks'),
       srp('Examination', 14, f'Examination · 14 x {SRPS}')),
      '1-3', IRL + EURO, ID + 'p2-q6c-language', routes=bullet_routes('p2-q6c-', CULTURE)),
]

PART_TWO += [
    T('p2-7a', P2, '7A', '', 20, 11, L(11, 'Ordnance Survey Map'),
      (L(11, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper.', 'The post office in Arklow.'),),
      (S(26, 'Sketch Outline', 'Annotation'),), OS_SKETCH, '2-6', MAP, ID + 'p2-q7a', ('map', 'legend'),
      row_labels=(None, L(11, 'The built up area of Arklow south of the Avoca River'),
                  L(11, 'The entire route of the M11 motorway'), L(11, 'The entire route of the railway line'),
                  L(11, 'The post office in Arklow.'))),
    T('p2-7b', P2, '7B', '', 30, 11, L(11, 'Multinational Company'),
      (L(11, 'Examine how globalisation impacts on world trade with reference to the operations of one',
         'that you have studied.'),),
      (S(27, 'Multinational company named · 2 marks', 'Annotation'),),
      (fixed('Multinational company named', 2, 'Multinational company named · 2 marks'),
       fixed('Impact of globalisation on world trade identified', 2,
             'Impact of globalisation on world trade identified · 2 marks'),
       srp('Examination', 13, f'Examination · 13 x {SRPS}')),
      '3-2', MNC, ID + 'p2-q7b'),
    T('p2-7c', P2, '7C', '', 30, 11, L(11, 'Ireland and the European Union'),
      (L(11, 'Examine the impact of membership of the European Union on the Irish economy.'),),
      (S(27, 'Impact identified · 2 marks', 'Annotation', after='7C.'),),
      (fixed('Impact identified', 2, 'Impact identified · 2 marks'), srp('Examination', 14, 'Examination · 14 x SRPs')),
      '3-3', EU_ECON, ID + 'p2-q7c'),
]

Q8AS = (L(12, 'Examine the data above showing the government debt of Eurozone countries', 'following questions.'),)
PART_TWO += romans('8A', P2, 12, L(12, 'Government Debt', nth=0), Q8AS, ID + 'p2-q8a', ('page',), [
    ('(i)', 16, L(12, '(i) Using graph paper, draw a suitable graph to illustrate this data.'),
     S(28, 'Bar Chart', '(ii) · Explain briefly'), BAR_GRAPH, '2-0', TG),
    ('(ii)', 4, L(12, '(ii) Explain briefly one reason why Ireland’s government has a large debt.'),
     S(28, '(ii) · Explain briefly', '[20m]', after='Bar Chart'),
     (pair('Valid explanation · 2 + 2 marks', 'Reason'),), '3-0', ECON),
])
REASON_8C = ('Three reasons @ 10 marks each', 'For each reason:', 'Reason stated · 2 marks',
             'Aerial photograph OR OS map evidence 2 marks', f'Examination · 3 x {SRPS}')
PART_TWO += [
    T('p2-8b', P2, '8B', '', 30, 12, L(12, 'Developing Economy'),
      (L(12, 'Examine the impact of global trading patterns on one developing economy you have studied.'),),
      (S(29, 'Developing economy named · 2 marks', 'Annotation'),),
      (fixed('Developing economy named', 2, 'Developing economy named · 2 marks'),
       fixed('Impact identified', 2, 'Impact identified · 2 marks'), srp('Examination', 13, 'Examination · 13 x SRPs')),
      '3-1', DEV, ID + 'p2-q8b'),
    T('p2-8c', P2, '8C', '', 30, 12, L(12, 'Location of Economic Activity'),
      (L(12, 'Examine the 1:50 000 Ordnance Survey map and aerial photograph accompanying this', 'paper.'),
       L(12, 'Discuss three reasons why the Arklow area is a suitable location', 'support your answer.')),
      (S(30, 'Three reasons @ 10 marks each', 'Annotation'),),
      tuple(Criterion(f'Reason {n}', 10, evens(10), 'srp', REASON_8C) for n in (1, 2, 3)),
      '3-0', ECON + MAP + AER, ID + 'p2-q8c', ('aerial', 'map', 'legend')),
]

Q9AS = (L(13, 'Examine the table above showing the Human Development Index (HDI) for selected',
          'following questions.'),)
PART_TWO += romans('9A', P2, 13, L(13, 'Measuring Development'), Q9AS, ID + 'p2-q9a', ('page',), [
    ('(i)', 2, L(13, '(i) What was the Human Development Index in China in 2000?'),
     S(31, '(i) · 0.594', '(ii) Norway'), (fixed('HDI', 2, '(i) · 0.594 · 2 marks'),), '2-0', TG),
    ('(ii)', 2, L(13, '(ii) Which country had the highest Human Development Index in 2017?'),
     S(31, '(ii) Norway', '(iii) 0.34'), (fixed('Country', 2, '(ii) Norway · 2 marks'),), '2-0', TG),
    ('(iii)', 4, L(13, '(iii) Calculate the difference between the Human Development Index in Brazil', 'in 2017.'),
     S(31, '(iii) 0.34', '(iv) Syria'), (fixed('Difference', 4, '(iii) 0.34 · 4 marks'),), '2-0', TG),
    ('(iv)', 4, L(13, '(iv) Name the country where the Human Development Index went down', 'for this decrease.'),
     S(31, '(iv) Syria', '(v) · Two indicators'),
     (fixed('Country', 2, '(iv) Syria · 2 marks'), fixed('Reason', 2, 'Valid reason stated · 2 marks')), '3-1', DEV),
    ('(v)', 4, L(13, '(v) Name two indicators used to calculate a country’s Human Development Index.'),
     S(31, '(v) · Two indicators', '(vi) Valid'), (pair('(v) · Two indicators named 2 + 2 marks', 'Two indicators'),),
     '3-1', DEV),
    ('(vi)', 4, L(13, '(vi) Explain briefly one advantage of using the Human Development Index', 'economic development.'),
     S(31, '(vi) Valid', 'Page 29 of'), (pair('(vi) Valid explanation · 2 + 2 marks', 'Advantage'),), '3-1', DEV),
])
DEVELOPED = ('Footloose industries', 'Financial services', 'Mass tourism.')
PART_TWO += [
    T('p2-9b', P2, '9B', '', 30, 13, L(13, 'Economic Activity in a Developed Economy'),
      (L(13, 'Examine the development of one of the following with reference to a developed economy', 'Mass tourism.'),),
      (S(32, 'Developed economy named', 'Annotation'),),
      (fixed('Developed economy named', 2, 'Developed economy named · 2 marks'),
       srp('Examination', 14, f'Examination · 14 x {SRPS}')),
      '3-0', ECON, ID + 'p2-q9b-footloose-industries', routes=bullet_routes('p2-q9b-', DEVELOPED)),
    T('p2-9c', P2, '9C', '', 30, 13, L(13, 'Environmental Impact'),
      (L(13, 'Examine the environmental impacts of burning fossil fuels.'),),
      (S(32, 'Environmental Impacts identified', 'Annotation', after='9C.'),),
      (pair('Environmental Impacts identified · 2 + 2 marks', 'Environmental impacts identified'),
       srp('Examination', 13, 'Examination · 13 x SRPs')),
      '3-4', ENV + ENERGY, ID + 'p2-q9c'),
]

PART_TWO += [
    T('p2-10a', P2, '10A', '', 20, 14, L(14, 'Aerial Photograph'),
      (L(14, 'Draw a sketch map of the aerial photograph, half the length and half the breadth.',
         'The lake in the left foreground.'),),
      (S(33, 'Sketch Outline', 'Annotation'),), AERIAL_SKETCH, '2-8', AER + URB, ID + 'p2-q10a', ('aerial',),
      row_labels=(None, L(14, 'The river'), L(14, 'The bridge'), L(14, 'The running track in the middleground'),
                  L(14, 'The lake in the left foreground.'))),
    T('p2-10b', P2, '10B', '', 30, 14, L(14, 'Future Urbanism'),
      (L(14, 'Discuss two issues facing cities of the future.'),),
      (S(34, 'Two issues identified', 'Annotation'),),
      (pair('Two issues identified · 2m + 2m', 'Two issues identified'),
       split('Discussion of the two issues (7/6 SRPs each)', 13,
             f'Discussion of issue one · 7/6 x {SRPS}', f'Discussion of issue two · 7/6 x {SRPS}')),
      '4-5', URB, ID + 'p2-q10b'),
    T('p2-10c', P2, '10C', '', 30, 14, L(14, 'Migration'),
      (L(14, 'Describe and explain changing patterns of migration in Ireland since 1950.'),),
      (S(34, 'Changing patterns identified', 'Annotation', after='10C.'),),
      (pair('Changing patterns identified · 2 + 2 marks', 'Changing patterns identified'),
       srp('Examination', 13, 'Examination · 13 x SRPs')),
      '4-2', POP, ID + 'p2-q10c'),
]

Q11AS = (L(15, 'Examine the chart above which shows the dependency ratio', 'following questions.'),)
PART_TWO += romans('11A', P2, 15, L(15, 'Irish Population'), Q11AS, ID + 'p2-q11a', ('page',), [
    ('(i)', 2, L(15, '(i) What was the dependency ratio (%) for Longford in 2011?'),
     S(35, '(i) · 55.6', '(ii) · Galway'), (fixed('Dependency ratio', 2, '(i) · 55.6 (%) · 2 marks'),), '2-0', TG),
    ('(ii)', 2, L(15, '(ii) Which county had the lowest dependency ratio in 2016?'),
     S(35, '(ii) · Galway', '(iii) 9.1'), (fixed('County', 2, '(ii) · Galway · 2 marks'),), '2-0', TG),
    ('(iii)', 4, L(15, '(iii) Calculate the difference in the dependency ratios (%) for Kildare and Donegal', '2016.'),
     S(35, '(iii) 9.1', '(iv) Valid'), (fixed('Difference', 4, '(iii) 9.1 (%) · 4 marks'),), '2-0', TG),
    ('(iv)', 4, L(15, '(iv) Explain briefly one reason why dependency ratios in urban areas', 'rural areas.'),
     S(35, '(iv) Valid', '(v) · Two valid'), (pair('(iv) Valid brief explanation · 2 + 2 marks', 'Reason'),),
     '4-0', POP),
    ('(v)', 8, L(15, '(v) Explain briefly two effects of an increase in the dependency ratio.'),
     S(35, '(v) · Two valid', 'Page 33 of'),
     (pair('(v) · Two valid brief explanations · 2 + 2 marks', 'First effect'), pair('=2 + 2 marks', 'Second effect')),
     '4-0', POP),
])
PATTERN_11C = ('Three patterns @ 10 marks each', 'For each pattern:', 'Pattern named · 2 marks',
               'Map reference/evidence · 2 marks', 'Examination · 3 x SRPs')
PART_TWO += [
    T('p2-11b', P2, '11B', '', 30, 15, L(15, 'Urban Expansion'),
      (L(15, 'As cities expand they impact on the surrounding areas.'),
       L(15, 'Discuss this statement with reference to example(s) that you have studied.')),
      (S(36, 'Impact identified · 2m', 'Annotation'),),
      (fixed('Impact identified', 2, 'Impact identified · 2m'), fixed('Example', 2, 'Example · 2m'),
       srp('Discussion', 13, f'Discussion · 13 x {SRPS}')),
      '4-5', URB, ID + 'p2-q11b'),
    T('p2-11c', P2, '11C', '', 30, 15, L(15, 'Rural Settlement Patterns'),
      (L(15, 'With reference to the 1:50 000 Ordnance Survey map accompanying this paper', 'evident on the map.'),),
      (S(37, 'Three patterns @ 10 marks each', 'Annotation'),),
      tuple(Criterion(f'Pattern {n}', 10, evens(10), 'srp', PATTERN_11C) for n in (1, 2, 3)),
      '4-3', URB + MAP, ID + 'p2-q11c', ('map', 'legend')),
]

Q12AS = (L(16, 'Examine the data above showing the nationality of asylum seekers', 'following questions.'),)
PART_TWO += romans('12A', P2, 16, L(16, 'Migration', nth=0), Q12AS, ID + 'p2-q12a', ('page',), [
    ('(i)', 16, L(16, '(i) Using graph paper, draw a suitable graph to illustrate this data.'),
     S(38, 'Bar Chart · Pie Chart', '(ii) · Explain briefly'), GRAPH, '2-0', TG),
    ('(ii)', 4, L(16, '(ii) Explain briefly one reason why people apply for asylum.'),
     S(38, '(ii) · Explain briefly', '[20m]', after='Bar Chart'),
     (pair('Valid explanation · 2 + 2 marks', 'Reason'),), '4-2', POP),
])
GROWTH = ('Income levels', 'Society and culture', 'Technology.')
PART_TWO += [
    T('p2-12b', P2, '12B', '', 30, 16, L(16, 'Urban Planning'),
      (L(16, 'Examine the effectiveness of urban planning strategies with reference to example(s)',
         'that you have studied.', nth=0),),
      (S(39, 'Effect identified · 2 marks', 'Annotation'),),
      (fixed('Effect identified', 2, 'Effect identified · 2 marks'), fixed('Example', 2, 'Example · 2 marks'),
       srp('Examination', 13, f'Examination · 13 x {SRPS}')),
      '4-5', URB, ID + 'p2-q12b'),
    T('p2-12c', P2, '12C', '', 30, 16, L(16, 'Population'),
      (L(16, 'Examine the influence/impact of any one of the following factors on levels of population',
         'Technology.'),),
      (S(39, 'Influence/impact identified · 2 marks', 'Annotation', after='12C.'),),
      (fixed('Influence/impact identified', 2, 'Influence/impact identified · 2 marks'),
       fixed('Example of location', 2, 'Example of location · 2 marks'),
       srp('Examination', 13, f'Examination · 13 x {SRPS}')),
      '4-1', POP, ID + 'p2-q12c-income-levels', routes=bullet_routes('p2-q12c-', GROWTH)),
]

# ------------------------------------------------------------------ Options --
OC = (S(41, '*Overall Coherence (20 marks)', None, table=True),)


def option(q, page, theme, note_nth, prompt, scheme_page, topic, atlas, after=None, end=None, absorbs=()):
    return T(f'p2-{q}', P2, q, '', 80, page, theme, prompt if isinstance(prompt, tuple) else (prompt,),
             (S(scheme_page, 'Number of aspects', end, None, after), *OC),
             (Criterion('Aspects (3 @ 20 marks or 4 @ 15 marks)', 60, upto(60), 'srp',
                        ('Number of aspects', '?For each aspect:', 'Identifying aspect', '8 x SRP')),
              Criterion('Overall coherence', 20, (0, 6, 10, 14, 17, 20), 'exact',
                        ('Overall Coherence · 20 marks graded*', '*Overall Coherence (20 marks)', 'Excellent · 20',
                         'Very Good · 17', 'Good · 14', 'Fair · 10', 'Weak · 6', 'Poor · 0'))),
             topic, (atlas,), ID + f'p2-q{q}',
             stem=(L(page, 'Note: It is better to discuss three or four aspects', 'large number of points.',
                     nth=note_nth),),
             absorbs=absorbs)


GI, GE = H + 'option-global-interdependence', H + 'option-geoecology'
CI, AO = H + 'option-culture-identity', H + 'option-atmosphere-ocean'
EMPOWER = ('National debt', 'Aid programmes', 'Land ownership patterns', 'Differing gender roles in society.')
OPTIONS = [
    option('13', 18, L(18, 'Global Interdependence'), 0,
           L(18, 'Examine the contribution that fair trade can make to sustainable development.'), 43, '5-3', GI),
    option('14', 18, L(18, 'Global Interdependence'), 0,
           L(18, 'Empowering people is a way of linking economic growth with human development.',
             'Differing gender roles in society.'), 44, '5-2', GI, after='14.', end='15.',
           absorbs=pool(ID + 'p2-q14-', EMPOWER, 2)[1]),
    option('15', 18, L(18, 'Global Interdependence'), 0,
           L(18, 'We live in an interdependent global economy.', 'Impact of social and political decisions.'),
           44, '5-1', GI, after='15.'),
    option('16', 18, L(18, 'Geoecology'), 1,
           L(18, 'Discuss how human activity can have both positive and negative impacts on soil.'), 45, '6-1', GE,
           after='16.', end='17.'),
    option('17', 18, L(18, 'Geoecology'), 1,
           L(18, 'Describe and explain the general composition and characteristics of any one soil type.'),
           45, '6-0', GE, after='17.'),
    option('18', 18, L(18, 'Geoecology'), 1,
           L(18, 'Describe the specific climatic characteristics experienced in one biome', 'in this biome.'),
           46, '6-2', GE),
    option('19', 19, L(19, 'Culture and Identity'), 0,
           L(19, 'Examine the strategies that have been or could be implemented', 'minority languages.'),
           47, '7-0', CI),
    option('20', 19, L(19, 'Culture and Identity'), 0,
           L(19, 'Identity as a concept entails a variety of cultural factors.', 'that you have studied.'),
           48, '7-2', CI, after='20.', end='21.'),
    option('21', 19, L(19, 'Culture and Identity'), 0,
           L(19, 'Many states have different cultural groups within their borders.', 'Discuss.'),
           48, '7-1', CI, after='21.'),
    option('22', 19, L(19, 'The Atmosphere – Ocean Environment'), 1,
           L(19, 'Examine how climate characteristics influence economic development.'), 49, '8-5', AO,
           after='22.', end='23.'),
    option('23', 19, L(19, 'The Atmosphere – Ocean Environment'), 1,
           L(19, 'Circulation in both the atmosphere and the oceans gives rise to different weather patterns.',
             'Discuss.'), 49, '8-3', AO, after='23.'),
    option('24', 19, L(19, 'The Atmosphere – Ocean Environment'), 1,
           L(19, 'Climate characteristics change over time and space.', 'Discuss.'), 50, '8-4', AO),
]

TASKS = [*PART_ONE, *PART_TWO, *OPTIONS]

ID_CORRECTION_REASON = 'No 2020 Higher card shipped before this review; every card is new.'

# No 2020 Higher card was live on origin/main before this review.
LEGACY_IDS: list[str] = []
