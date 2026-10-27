"""Independent review ledger: Leaving Certificate Geography 2018 Higher Level.

Sources (English editions, harvested Paper Trail corpus; sizes and SHA-256
pinned in EXPECTED_SOURCES and the generated audit): the examination paper
LC005ALP000EV (32 pages; one booklet printed Part One, answered in it, and
Part Two), marking scheme LC005ALP000EV (48 pages), and the common
companions as Paper Trail files them — the 1:50 000 Sligo map LC005CLP003EV
and its legend LC005CLPC00EV (both published only as JPEGs) and the Sligo
aerial photograph LC005CLP004EV (a one-page PDF). Part One is 80 marks (any
ten of twelve @ 8), Part Two 320 (four questions @ 80).

Visual sweep (every page rendered and read on 2026-10-13):
  Paper p1 cover and examiner's grid; p2-p12 Part One Questions 1-12 (p5
  holds Q4 and Q5; Q2 prints three Google Street View images of Sligo);
  p13 Part Two instructions; p14 Section 1 divider; p15-p20 Q1-Q6 (p15
  and p18 open with their dividers); p21 Section 2 divider; p22-p28
  Electives Q7-Q12 (p22 and p26 open with their elective dividers; p24
  holds 9A and 9B, p25 9C); p29 Section 3 divider and option note;
  p30-p31 Options Q13-Q24; p32 back cover ("There is no examination
  material on this page").
  Scheme p1 cover; p2-p3 notes; p4 Part One table (two columns: Q1-Q6,
  Q7-Q12); p5 Part Two instructions and Section 1 divider; p6-p12 Q1-Q3;
  p13-p19 Q4-Q6; p20 Section 2 divider; p21-p26 Q7-Q9; p27-p32 Q10-Q12;
  p33 Section 3 divider; p34 option outline and Overall Coherence
  descriptors; p35-p42 Q13-Q24; p43-p45 Geographical Investigation
  (coursework) and its presentation marks; p46 investigation topics; p47
  Irish-language bonus marks; p48 back cover.
  Companions: Sligo map extract (Benbulbin, Kings Mountain, Glencar Lough,
  the Drumcliff River, Sligo Harbour); OS legend sheet; oblique aerial
  photograph of Sligo.

Boundaries and tariffs follow the 2019 Higher ledger. Matching tables, in
the printed row order: Q1 G 74 35 Plateau, G 74 46 Dendritic, G 68 39
Trellised, G 71 45 Swallow hole; Q2 A Left Foreground, B Centre
Middleground, C Right Background; Q5 (i) Geomorphological, Administrative,
Peripheral, Cultural and (ii) The Burren, Co. Wexford, Northern Norway,
Islamic world, each against the printed definitions; Q7 Limestone,
Basalt, Sandstone, Granite = (i) B, A, D, C and (ii) W, Y, Z, X; Q8
Reverse, Transform, Normal = (i) B, C, A and (ii) Compression, Shearing,
Tension; Q9 Interlocking spurs F, Drumlin E, Fjord A, Striations C,
Cirque/corrie/tarn B, Barchan dunes D. Q3's eight true/false statements
are separately priced romans; the scheme credits either answer to (vi)
("True or false 1m") and the card carries it as printed.

Printed choices: 1B "the coastal landscape or ... the fluvial landscape",
5B "tourism or transport", 2C (i) or (ii) and 3B one of four rock-cycle
interactions are routes; 8C is one route per printed activity (footloose
industries, financial services, mass tourism) and, within each, one card
for the two-of-three factor pool; 10B and options 15 and 23 are pools,
one card each (choice is not a route).
"""

from geography_review import (
    Criterion, Lift, Route, SchemeSlice, Task, pool, evens, fixed, slug, srp, sums, upto,
)

YEAR = 2018
LEVEL = 'higher'
PAPER_PAGES = {1: 32, 2: 32}
SCHEME_PAGES = 48
QUESTION_TARIFFS = {1: {str(n): 8 for n in range(1, 13)},
                    2: {**{f'{n}{x}': (20 if x == 'A' else 30)
                           for n in range(1, 13) for x in 'ABC'},
                        **{str(n): 80 for n in range(13, 25)}}}

EXPECTED_SOURCES = {
    'paper1': ('LC005ALP000EV.pdf', 2443729),
    'paper2': ('LC005ALP000EV.pdf', 2443729),
    'scheme': ('LC005ALP000EV.pdf', 774570),
    'map': ('LC005CLP003EV.jpg', 11172454),
    'legend': ('LC005CLPC00EV.jpg', 4184180),
    'aerial': ('LC005CLP004EV.pdf', 6573219),
}

_PAPER = {1: 'cover and examiner grid', **{p: 'question' for p in range(2, 13)},
          13: 'Part Two instructions', 14: 'section divider', **{p: 'question' for p in range(15, 21)},
          21: 'section divider', **{p: 'question' for p in range(22, 29)}, 29: 'section divider and option note',
          30: 'question', 31: 'question', 32: 'back cover'}
PAGE_REVIEW = {
    # One booklet printed both parts.
    'paper1': _PAPER, 'paper2': _PAPER,
    'scheme': {1: 'cover', 2: 'notes', 3: 'notes', 4: 'Part One table',
               5: 'Part Two instructions and section divider',
               **{p: 'Part Two allocation' for p in range(6, 20)}, 20: 'section divider',
               **{p: 'Part Two allocation' for p in range(21, 33)}, 33: 'section divider',
               34: 'option outline and coherence descriptors',
               **{p: 'option allocation' for p in range(35, 43)},
               **{p: 'geographical investigation (coursework)' for p in range(43, 46)},
               46: 'investigation topics', 47: 'Irish-language bonus marks', 48: 'back cover'},
}

EXPECTED_SELECTION_SCAN = [
    [1, 2, 'attempt any ten'], [1, 12, 'any two'], [1, 13, 'attempt four'], [1, 14, 'attempt two'],
    [1, 15, 'attempt one'], [1, 15, 'any two'],
    [1, 16, 'answer (i) or (ii)'], [1, 16, 'any one'], [1, 16, 'any one'],
    [1, 17, 'one of the following'],
    [1, 18, 'attempt one'],
    [1, 21, 'attempt one'],
    [1, 23, 'two of the following'],
    [1, 24, 'any two'],
    [1, 26, 'two of the following'],
    [1, 29, 'attempt one'],
    [1, 30, 'three of the following'], [1, 30, 'any three'], [1, 30, 'any one'],
    [1, 31, 'three of the following'],
]
SELECTION_REVIEW = [
    {'scan': [[1, 2, 'attempt any ten'], [1, 13, 'attempt four'], [1, 14, 'attempt two'], [1, 15, 'attempt one'],
              [1, 18, 'attempt one'], [1, 21, 'attempt one'], [1, 29, 'attempt one']],
     'kind': 'exam-attempt-rule',
     'reason': 'Part One any ten of twelve and Part Two four questions (one of Q1-3, one of Q4-6, one elective, one option) are attempt rules; every question is carded.'},
    {'scan': [[1, 16, 'answer (i) or (ii)']], 'kind': 'closed-route',
     'reason': '2C: (i) or (ii) -> two routes, each with its own scheme allocation. 1B "the coastal landscape or on the fluvial landscape" and 5B "tourism or transport" are printed routes too (the scheme marks both accounts and awards the higher).'},
    {'scan': [[1, 17, 'one of the following']], 'kind': 'closed-choose-one',
     'reason': '3B: one of four printed rock-cycle interactions -> four routes.'},
    {'scan': [[1, 23, 'two of the following']], 'kind': 'choose-n-one-card',
     'reason': '8C: footloose industries OR financial services OR mass tourism -> three routes; within each, two of three printed factors -> one card with every printed factor (choice is not a route).'},
    {'scan': [[1, 26, 'two of the following'], [1, 30, 'three of the following'], [1, 31, 'three of the following']],
     'kind': 'choose-n-one-card',
     'reason': '10B two of three printed urban problems, option 15 three of four printed themes and option 23 three of four printed factors -> one card each with every printed item (choice is not a route).'},
    {'scan': [[1, 12, 'any two'], [1, 15, 'any two'], [1, 16, 'any one'], [1, 16, 'any one'], [1, 24, 'any two'],
              [1, 30, 'any three'], [1, 30, 'any one']],
     'kind': 'open-response',
     'reason': 'No printed pool: Part One Q12(iv) any two countries; 1A(iv) any two processes; 2C(i) any one of the two features named and 2C(ii) any one mass movement process; 9A(iv) any two examples; option 16 any three soil processes; option 17 any one soil type. Compulsory lists stay whole: 3A, 4A, 7A, 10A each bullet, 5C, 7B, 13 and 22 each item.'},
]

P1, P2 = 1, 2
LEFT = (0.0, 0.0, 0.47, 1.0)
RIGHT = (0.47, 0.0, 1.0, 1.0)
ID = 'geography-2018-hl-'
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
ECON = (H + 'elective-economic',)
DEV = (H + 'economic-developing-economies',)
MNC = (H + 'economic-multinationals-globalisation',)
EU_ECON = (H + 'economic-european-union',)
ENERGY = (H + 'economic-energy',)
ENV = (H + 'economic-environmental-impact',)

# ---------------------------------------------------------------- Part One --
Q1S = (L(2, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper and answer',
         'following questions.'),)
PART_ONE = romans('1', P1, 2, L(2, 'Landscape Identification'), Q1S, ID + 'p1-q1', ('map', 'legend'), [
    ('(i)', 4, L(2, '(i) In the table below, match each of the following features with the grid reference',
                 'Plateau surface of 100 metres high.'),
     S(4, 'Q.1 · (i)', '(ii) · Any valid', LEFT),
     rows(['Q.1 · (i) · Plateau 1m', 'Dendritic 1m', 'Trellised 1m', 'Swallow hole 1m']), '2-6', MAP + RIVERS + KARST,
     (L(2, 'G 74 35'), L(2, 'G 74 46'), L(2, 'G 68 39'), L(2, 'G 71 45'))),
    ('(ii)', 2, L(2, '(ii) Name one other drainage pattern not named above.'),
     S(4, '(ii) · Any valid', '(iii) · Ribbon', LEFT), (fixed('Drainage pattern', 2, '(ii) · Any valid answer 2m'),),
     '0-9', RIVERS),
    ('(iii)', 2, L(2, '(iii) What type of lake is Glencar Lough, located at grid reference G 74 43?'),
     S(4, '(iii) · Ribbon', 'Q.2', LEFT), (fixed('Type of lake', 2, '(iii) · Ribbon/Paternoster lake 2m'),),
     '0-11', GLAC + MAP),
])

Q2S = (L(3, 'Examine the aerial photograph of Sligo accompanying this paper and the Google Street View',
         'Answer each of the following questions.'),)
PART_ONE += [
    T('p1-2-i', P1, '2', '(i)', 6, 3, L(3, 'Aerial Photography'),
      (L(3, '(i) In the table below, using accepted notation, give the location on the aerial',
         'images A, B and C.'),),
      (S(4, 'Q.2 · (i)', '(ii) · Oblique', LEFT),),
      (fixed('A', 2, 'Q.2 · (i) · A Left Foreground 2m'), fixed('B', 2, 'B Centre Middleground 2m'),
       fixed('C', 2, 'C Right Background 2m')),
      '2-8', AER + URB, ID + 'p1-q2', ('page', 'aerial'), Q2S),
    T('p1-2-ii', P1, '2', '(ii)', 2, 3, L(3, 'Aerial Photography'),
      (L(3, '(ii) State the type of aerial photography used for the aerial photograph accompanying',
         'this paper.'),),
      (S(4, '(ii) · Oblique', 'Q.3', LEFT),), (fixed('Type', 2, '(ii) · Oblique 2m'),),
      '2-8', AER, ID + 'p1-q2-ii', ('aerial',), Q2S),
]

Q3S = (L(4, 'Locate point X, G 730 470, and point Y', 'between point X and point Y.'),
       L(4, 'Using the 1:50 000 Ordnance Survey map and legend and the elevation profile above,', 'true or false.'))
Q3 = (('(i)', 'X is located in the Lisduff townland.', 'Q.3 · (i)', '(ii) · False', 'Q.3 · (i) · False 1m'),
      ('(ii)', 'The height at Y is 160 metres.', '(ii) · False', '(iii) · False', '(ii) · False 1m'),
      ('(iii)', 'The aspect of the slope between A and X is south.', '(iii) · False', '(iv) · True',
       '(iii) · False 1m'),
      ('(iv)', 'The Drumcliff River is located at C.', '(iv) · True', '(v) · False', '(iv) · True 1m'),
      ('(v)', 'The slope between B and C is convex.', '(v) · False', '(vi) · True or false', '(v) · False 1m'),
      ('(vi)', 'The N16 regional road is located at D.', '(vi) · True or false', '(vii) · False',
       '(vi) · True or false 1m'),
      ('(vii)', 'The land between E and F is on the eastern slope of Cope’s Mountain.', '(vii) · False',
       '(viii) True', '(vii) · False 1m'),
      ('(viii)', 'There is a coniferous plantation between G and H.', '(viii) True', 'Q.4', '(viii) True 1m'))
PART_ONE += romans('3', P1, 4, L(4, 'Elevation Profile', nth=0), Q3S, ID + 'p1-q3', ('page', 'map', 'legend'), [
    (roman, 1, L(4, f'{roman} {statement}'), S(4, start, end, LEFT), (fixed('True or false', 1, line),),
     '2-6', MAP) for roman, statement, start, end, line in Q3])

Q4S = (L(5, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper and answer',
         'following questions.'),)
PART_ONE += romans('4', P1, 5, L(5, 'Ordnance Survey Map'), Q4S, ID + 'p1-q4', ('map', 'legend'), [
    ('(i)', 2, L(5, '(i) What is the height, in metres, of the highest point shown on the map?'),
     S(4, 'Q.4 · (i)', '(ii) · G 685', LEFT), (fixed('Height', 2, 'Q.4 · (i) · 597 (m) 2m'),), '2-6', MAP),
    ('(ii)', 2, L(5, '(ii) Give a six-figure grid reference for an Independent Holiday Hostel in Sligo.'),
     S(4, '(ii) · G 685', '(iii) · 1.5', LEFT), (fixed('Grid reference', 2, '(ii) · G 685 365 / G 692 362 2m'),),
     '2-6', MAP),
    ('(iii)', 2, L(5, '(iii) Measure the length, in kilometres, of the dual carriageway on the N4 road.'),
     S(4, '(iii) · 1.5', '(iv) · 42', LEFT), (fixed('Length', 2, '(iii) · 1.5 (km) 2m'),), '2-6', MAP),
    ('(iv)', 2, L(5, '(iv) Calculate the approximate area, in km2, of the land west of easting 70.'),
     S(4, '(iv) · 42', 'Q.5(i)', LEFT), (fixed('Area', 2, '(iv) · 42 (km2) approx. 2m'),), '2-6', MAP),
])

Q5S = (L(5, 'Answer each of the following questions in the table below.'),)
Q5_DEFINITIONS = (L(5, 'A region characterised by physical characteristics such as rock type.'),
                  L(5, 'A region organised by local authorities.'),
                  L(5, 'A marginal region where there is an underdevelopment of economic activities.'),
                  L(5, 'A region with a distinct pattern in terms of religion.'))
PART_ONE += romans('5', P1, 5, L(5, 'Concept of a Region'), Q5S, ID + 'p1-q5', ('page',), [
    ('(i)', 4, (L(5, '(i) Match each of the following types of region with the definition', 'associated with it:'),
                Lift(5, 'Peripheral', 'Geomorphological', row=True)),
     S(4, 'Q.5(i)', 'Q.5(ii)', LEFT),
     rows(['Q.5(i) · Geomorphological 1m', 'Administrative 1m', 'Peripheral 1m', 'Cultural 1m']), '1-0',
     IRL + EURO, Q5_DEFINITIONS),
    ('(ii)', 4, (L(5, '(ii) Match each of the following examples of regions with the definition',
                   'associated with it:'),
                 Lift(5, 'Islamic World', 'The Burren', row=True)),
     S(4, 'Q.5(ii)', 'Q.6', LEFT),
     rows(['Q.5(ii) The Burren 1m', 'Co. Wexford 1m', 'Northern Norway 1m', 'Islamic world 1m']), '1-0',
     IRL + EURO, Q5_DEFINITIONS),
])

Q6S = (L(6, 'Examine the map above and answer each of the following questions.'),)
PART_ONE += romans('6', P1, 6, L(6, 'Plate Tectonics'), Q6S, ID + 'p1-q6', ('page',), [
    ('(i)', 2, L(6, '(i) Name each of the plates labelled A and B.'), S(4, 'Q.6 · (i)', '(ii) · South', LEFT),
     (fixed('A', 1, 'Q.6 · (i) · A. North American 1m'), fixed('B', 1, 'B. African 1m')), '0-0', PS),
    ('(ii)', 2, L(6, '(ii) Name the two plates that converged to form the Andes mountain range.'),
     S(4, '(ii) · South', '(iii) · Pacific', LEFT),
     (fixed('Plate 1', 1, '(ii) · South American 1m'), fixed('Plate 2', 1, 'Nazca 1m')), '0-0', PS),
    ('(iii)', 2, L(6, '(iii) What is the name given to the area X where earthquakes and volcanic eruptions', 'occur?'),
     S(4, '(iii) · Pacific', '(iv) · Constructive', LEFT), (fixed('Area', 2, '(iii) · Pacific Ring of Fire 2m'),),
     '0-7', EV + PS),
    ('(iv)', 2, L(6, '(iv) Name the type of plate boundary at Y.'),
     S(4, '(iv) · Constructive', None, LEFT), (fixed('Plate boundary', 2, '(iv) · Constructive/Divergent 2m'),),
     '0-0', PS),
])

Q7S = (L(7, 'Examine the map of Ireland and the photographs of rocks above', 'following questions.'),)
Q7_ROWS = (L(7, 'Limestone'), L(7, 'Basalt'), L(7, 'Sandstone'), L(7, 'Granite'))
PART_ONE += romans('7', P1, 7, L(7, 'Rocks in Ireland'), Q7S, ID + 'p1-q7', ('page',), [
    ('(i)', 4, L(7, '(i) Match each of the locations on the map, A, B, C and D with the example of the rock',
                 'most associated with it.'),
     S(4, 'Q.7(i)', 'Q.7(ii)', RIGHT), rows(['Q.7(i) · B · 1m', '=A · 1m', '=D · 1m', '=C · 1m']), '0-1', RW, Q7_ROWS),
    ('(ii)', 4, L(7, '(ii) Match each of the photographs W, X, Y and Z with the example of the rock',
                  'best matches it.'),
     S(4, 'Q.7(ii)', 'Q.8(i)', RIGHT), rows(['Q.7(ii) · W · 1m', '=Y · 1m', '=Z · 1m', '=X · 1m']), '0-1', RW,
     Q7_ROWS),
])

Q8S = (L(8, 'Examine the images above and answer each of the following questions.'),)
Q8_ROWS = (L(8, 'Reverse fault'), L(8, 'Transform fault'), L(8, 'Normal fault'))
PART_ONE += romans('8', P1, 8, L(8, 'Faulting'), Q8S, ID + 'p1-q8', ('page',), [
    ('(i)', 3, L(8, '(i) Match each of the images A, B, and C with the type of fault', 'best matches it.'),
     S(4, 'Q.8(i)', 'Q.8(ii)', RIGHT), rows(['Q.8(i) · B · 1m', '=C · 1m', '=A · 1m']), '0-2', PS + RW, Q8_ROWS),
    ('(ii)', 3, L(8, '(ii) Indicate, by ticking the correct box, whether each of the types of fault',
                  'compression, tension or shearing.'),
     S(4, 'Q.8(ii)', 'Q.8(iii)', RIGHT), rows(['Q.8(ii) · Compression · 1m', 'Shearing · 1m', 'Tension · 1m']),
     '0-2', PS + RW, Q8_ROWS),
    ('(iii)', 2, (L(8, '(iii) State whether the following statement is true or false.'),
                  L(8, 'Horsts and grabens are features associated with faulting.')),
     S(4, 'Q.8(iii)', 'Q.9(i)', RIGHT), (fixed('True or false', 2, 'Q.8(iii) True · 2m'),), '0-2', PS + RW),
])

Q9S = (L(9, 'Examine the images above and answer each of the following questions.'),)
PART_ONE += romans('9', P1, 9, L(9, 'Landscape – Image Interpretation'), Q9S, ID + 'p1-q9', ('page',), [
    ('(i)', 6, L(9, '(i) Match each of the images A, B, C, D, E and F with the landscape feature',
                 'best matches it.'),
     S(4, 'Q.9(i)', 'Q.9(ii)', RIGHT),
     rows(['Q.9(i) · F · 1m', '=E · 1m', '=A · 1m', '=C · 1m', '=B · 1m', '=D · 1m']), '0-4', RIVERS + GLAC,
     (L(9, 'Interlocking spurs'), L(9, 'Drumlin'), L(9, 'Fjord'), L(9, 'Striations'), L(9, 'Cirque/corrie/tarn'),
      L(9, 'Barchan dunes', nth=0))),
    ('(ii)', 2, (L(9, '(ii) State whether the following statement is true or false.'),
                 L(9, 'Barchan dunes are formed by wind deposition in deserts.')),
     S(4, 'Q.9(ii)', 'Q.10', RIGHT), (fixed('True or false', 2, 'Q.9(ii) · True · 2m'),), '0-4', RW),
])

Q10S = (L(10, 'Examine the synoptic weather chart above and answer each of the following questions.'),)
PART_ONE += romans('10', P1, 10, L(10, 'Weather'), Q10S, ID + 'p1-q10', ('page',), [
    ('(i)', 2, L(10, '(i) What is the lowest barometric pressure identified on the weather chart', 'millibars?'),
     S(4, 'Q.10', '(ii) Occluded', RIGHT), (fixed('Pressure', 2, 'Q.10 · (i) 998 (mb) · 2m'),), '2-7', WX),
    ('(ii)', 2, L(10, '(ii) Name the type of weather front over Iceland.'),
     S(4, '(ii) Occluded', '(iii) 1028', RIGHT), (fixed('Weather front', 2, '(ii) Occluded · 2m'),), '2-7', WX),
    ('(iii)', 2, L(10, '(iii) What is the highest barometric pressure of the anticyclone', 'millibars?'),
     S(4, '(iii) 1028', '(iv) False', RIGHT), (fixed('Pressure', 2, '(iii) 1028 (mb) 2m'),), '2-7', WX),
    ('(iv)', 2, (L(10, '(iv) State whether the following statement is true or false.'),
                 L(10, 'The wind speed over Norway is greater than the wind speed over Ireland.')),
     S(4, '(iv) False', 'Q.11', RIGHT), (fixed('True or false', 2, '(iv) False · 2m'),), '2-7', WX),
])

Q11S = (L(11, 'Read the extract above and answer each of the following questions.'),)
PART_ONE += romans('11', P1, 11, L(11, 'Irish Exports'), Q11S, ID + 'p1-q11', ('page',), [
    ('(i)', 2, L(11, '(i) State two reasons, referred to in the extract above, for the decline in trade',
                 'United Kingdom.'),
     S(4, 'Q.11', '(ii) Valid', RIGHT), (one_plus_one('Q.11 · (i) 2 reasons · 1m + 1m', 'Two reasons'),),
     '3-3', EU_ECON),
    ('(ii)', 2, L(11, '(ii) What offset the decline in trade with the United Kingdom?'),
     S(4, '(ii) Valid', '(iii) 515', RIGHT), (fixed('Offset', 2, '(ii) Valid ans. · 2m'),), '3-3', EU_ECON),
    ('(iii)', 2, L(11, '(iii) What was the difference between the value of exports to China and to the',
                   '(in € millions)?'),
     S(4, '(iii) 515', '(iv) Valid', RIGHT), (fixed('Difference', 2, '(iii) 515 · 2m'),), '2-0', TG),
    ('(iv)', 2, L(11, '(iv) Name two of the strongest performers in terms of export growth', 'extract.'),
     S(4, '(iv) Valid', 'Q.12', RIGHT, 'Q.11'),
     (one_plus_one('(iv) Valid ans. · 1m + 1m', 'Two strongest performers'),), '3-3', EU_ECON),
])

Q12S = (L(12, 'Examine the table above and answer each of the following questions.'),)
PART_ONE += romans('12', P1, 12, L(12, 'Statistical Interpretation'), Q12S, ID + 'p1-q12', ('page',), [
    ('(i)', 2, L(12, '(i) Which country had the lowest price level index for Restaurants & Hotels',
                 'EU-28 average?'),
     S(4, 'Q.12', '(ii) Germany', RIGHT), (fixed('Country', 2, 'Q.12 · (i) Czech Rep · 2m'),), '2-0', TG),
    ('(ii)', 2, L(12, '(ii) Which of the selected countries had a price level index for Communications',
                  'EU-28 average?'),
     S(4, '(ii) Germany', '(iii) 4', RIGHT), (fixed('Country', 2, '(ii) Germany · 2m'),), '2-0', TG),
    ('(iii)', 2, L(12, '(iii) In how many countries did the price level indices for Food', 'EU-28 average?'),
     S(4, '(iii) 4', '(iv) Valid', RIGHT, 'Q.12'), (fixed('Number of countries', 2, '(iii) 4 · 2m'),), '2-0', TG),
    ('(iv)', 2, L(12, '(iv) Name any two countries in the table above that are not in the euro area.'),
     S(4, '(iv) Valid', None, RIGHT, 'Q.12'), (one_plus_one('(iv) Valid ans. · 1m + 1m', 'Two countries'),),
     '3-3', TG + EU_ECON),
])


# ---------------------------------------------------------------- Part Two --
def sketch(outline_line, outline_permitted, alloc, item_permitted, labels):
    return (fixed('Sketch outline' if 'Sketch' in outline_line else 'Map outline', 4,
                  outline_line, outline_permitted),
            *(Criterion(f'Feature {n}', 4, item_permitted, 'exact', alloc) for n in range(1, labels + 1)))


OS_SKETCH = sketch('Sketch Outline · 4 marks (4/0)', (0, 4),
                   ('4 features @ 4 marks each', 'Label 1 mark'), sums((0, 1, 3), (0, 1)), 4)
GRAPH = (fixed('Title', 2, ('Bar Chart · Pie Chart', 'Title · 2 marks · 2 marks')),
         fixed('Axes named (bar chart) / circle and centre (pie chart)', 2,
               ('Vertical axis named', 'Horizontal axis named'), (0, 1, 2)),
         fixed('6 items illustrated', 12, '6 items illustrated', upto(12)))


def split(label, total, first, second):
    return srp(label, total, (first, second))


def bullet_routes(prefix, items, atlas=None):
    return tuple(Route(slug(item, 34), item.rstrip('.'), ID + prefix + slug(item, 34), False,
                       keep_bullets=(item,), atlas=(atlas[item] if atlas else None))
                 for item in items)


Q1AS = (L(15, 'Examine the diagram above and answer each of the following questions.'),)
Q1AIV = L(15, '(iv) Name any two processes of chemical weathering.')
PART_TWO = romans('1A', P2, 15, L(15, 'Karst Landscape'), Q1AS, ID + 'p2-q1a', ('page',), [
    ('(i)', 4, L(15, '(i) Name each of the features labelled A and B.'),
     S(6, '(i) · A = Stalagmite', '(ii) · Bedding'),
     (fixed('A', 2, '(i) · A = Stalagmite · 2m'), fixed('B', 2, 'B = Stalactite · 2m')), '0-3', KARST),
    ('(ii)', 2, L(15, '(ii) What is the term given to the horizontal lines at C found in limestone?'),
     S(6, '(ii) · Bedding', '(iii) · Joint'), (fixed('Term', 2, '(ii) · Bedding plane · 2m'),), '0-3', KARST),
    ('(iii)', 2, L(15, '(iii) What is the term given to the vertical lines at D found in limestone?'),
     S(6, '(iii) · Joint', '(iv) · Two valid'), (fixed('Term', 2, '(iii) · Joint · 2m'),), '0-3', KARST),
    ('(iv)', 4, Q1AIV, S(6, '(iv) · Two valid', '(v) · Valid brief'),
     (pair('(iv) · Two valid processes · 2m + 2m', 'Two processes'),), '0-3', KARST + RW),
    ('(v)', 4, L(15, '(v) Explain briefly one of the processes of chemical weathering named by you above.'),
     S(6, '(v) · Valid brief', '(vi) · Valid brief'),
     (pair('(v) · Valid brief explanation · 2m + 2m', 'Explanation'),), '0-3', KARST + RW, (), (Q1AIV,)),
    ('(vi)', 4, L(15, '(vi) Explain briefly what is meant by the ground water table.'),
     S(6, '(vi) · Valid brief', None), (pair('(vi) · Valid brief explanation · 2m + 2m', 'Explanation'),),
     '0-3', KARST),
])
LANDSCAPES = 'the coastal landscape or on the fluvial landscape'
PART_TWO += [
    T('p2-1b', P2, '1B', '', 30, 15, L(15, 'Isostasy'),
      (L(15, 'Describe and explain how isostasy impacts on the coastal landscape or on the fluvial', 'landscape.'),),
      (S(7, 'Impact identified · 2m', '1C.'),),
      (fixed('Impact identified', 2, 'Impact identified · 2m'),
       srp('Description/explanation', 14, f'Description/Explanation · 14 x {SRPS}')),
      '0-5', SEA, ID + 'p2-q1b-coastal-landscape',
      routes=(Route('coastal-landscape', 'The coastal landscape', ID + 'p2-q1b-coastal-landscape', False,
                    ((LANDSCAPES, 'the coastal landscape'),), topic='0-5', atlas=SEA),
              Route('fluvial-landscape', 'The fluvial landscape', ID + 'p2-q1b-fluvial-landscape', False,
                    ((LANDSCAPES, 'the fluvial landscape'),), topic='0-5', atlas=RIVERS))),
    T('p2-1c', P2, '1C', '', 30, 15, L(15, 'Volcanoes'),
      (L(15, 'Discuss the positive impacts of volcanoes.'),),
      (S(7, 'Positive impacts identified', None),),
      (pair('Positive impacts identified · 2m + 2m', 'Positive impacts identified'),
       srp('Discussion', 13, f'Discussion · 13 x {SRPS}')),
      '0-7', EV, ID + 'p2-q1c'),
]

Q2AS = (L(16, 'Examine the diagram above and answer each of the following questions.'),)
PART_TWO += romans('2A', P2, 16, L(16, 'Structure of the Earth'), Q2AS, ID + 'p2-q2a', ('page',), [
    ('(i)', 6, L(16, '(i) Name each of the layers of the earth labelled A, B and C.'),
     S(8, '(i) · A = Asthenosphere', '(ii) · Iron'),
     (fixed('A', 2, '(i) · A = Asthenosphere · 2m'), fixed('B', 2, 'B = Lithosphere · 2m'),
      fixed('C', 2, 'C = Mantle · 2m')), '0-0', PS),
    ('(ii)', 4, L(16, '(ii) Name the two main minerals found in the core.'), S(8, '(ii) · Iron', '(iii) · Moho'),
     (fixed('Mineral 1', 2, '(ii) · Iron · 2m'), fixed('Mineral 2', 2, 'Nickel · 2m')), '0-0', PS),
    ('(iii)', 2, L(16, '(iii) What is the name given to the boundary between the crust and the mantle?'),
     S(8, '(iii) · Moho', '(iv) · Valid'), (fixed('Boundary', 2, '(iii) · Moho discontinuity · 2m'),), '0-0', PS),
    ('(iv)', 4, L(16, '(iv) Explain briefly how plates move.'), S(8, '(iv) · Valid', '(v) · Valid'),
     (pair('(iv) · Valid brief explanation · 2m + 2m', 'Explanation'),), '0-0', PS),
    ('(v)', 4, L(16, '(v) Explain briefly what is meant by endogenic forces.'), S(8, '(v) · Valid', None),
     (pair('(v) · Valid brief explanation · 2m + 2m', 'Explanation'),), '0-0', PS),
])
Q2CS = (L(16, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper.'),)
PART_TWO += [
    T('p2-2b', P2, '2B', '', 30, 16, L(16, 'Weathering'),
      (L(16, 'Explain the role of temperature in the process of physical/mechanical weathering.'),),
      (S(9, 'Reference to temperature', '2C.'),),
      (fixed('Reference to temperature', 2, 'Reference to temperature · 2m'),
       srp('Explanation', 14, f'Explanation · 14 x {SRPS}')),
      '0-8', RW, ID + 'p2-q2b'),
    T('p2-2c', P2, '2C', '', 30, 16, L(16, 'Surface Processes'),
      (L(16, '(i) Name and identify using six-figure grid references, two features on the map',
         'any one of these features.'),),
      # The scheme prints "or" at the foot of the page before (ii) overleaf.
      (S(9, 'Features named', None, (0.0, 0.0, 1.0, 0.86)),),
      (pair('Features named · 2m + 2m', 'Features named'), pair('Grid references · 2m + 2m', 'Grid references'),
       srp('Explanation of formation of one feature', 11, f'Explanation of formation of one feature · 11 x {SRPS}')),
      '0-4', MAP + RIVERS + SEA + GLAC, ID + 'p2-q2c-route-i', ('map', 'legend'), Q2CS,
      routes=(
          Route('route-i', 'Route (i)', ID + 'p2-q2c-route-i', False),
          Route('route-ii', 'Route (ii)', ID + 'p2-q2c-route-ii', False,
                prompt=(L(16, '(ii) Using grid references, identify an area on the map which has a very steep slope',
                          'areas such as these.'),),
                scheme=(S(10, 'Grid references · 2m + 2m', None),),
                criteria=(pair('Grid references · 2m + 2m', 'Grid references'),
                          fixed('Mass movement process named', 2, 'Mass movement process named · 2m'),
                          srp('Description/explanation', 12, f'Description/Explanation · 12 x {SRPS}')),
                topic='0-8', atlas=RW + MAP),
      )),
]

ROCK = ('Mining', 'Extracting building materials', 'Oil/gas exploitation', 'Geothermal energy production.')
PART_TWO += [
    T('p2-3a', P2, '3A', '', 20, 17, L(17, 'Ordnance Survey Map'),
      (L(17, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper.',
         'south of northing 43.'),),
      (S(11, 'Sketch Outline', None),), OS_SKETCH, '2-6', MAP + RIVERS, ID + 'p2-q3a', ('map', 'legend'),
      row_labels=(None, L(17, 'The entire course of the Drumcliff River'), L(17, 'Two named lakes'),
                  L(17, 'Two named lakes'), L(17, 'The entire area of land above 300 metres south of northing 43.'))),
    T('p2-3b', P2, '3B', '', 30, 17, L(17, 'Human Interaction with the Rock Cycle'),
      (L(17, 'Humans interact with the rock cycle in a number of ways.'),
       L(17, 'Describe and explain how this interaction with the rock cycle takes place', 'Geothermal energy production.')),
      (S(12, 'Description/Explanation · 15', '3C.', after='3B.'),),
      (srp('Description/explanation', 15, f'Description/Explanation · 15 x {SRPS}'),),
      '0-6', RW, ID + 'p2-q3b-mining', routes=bullet_routes('p2-q3b-', ROCK)),
    T('p2-3c', P2, '3C', '', 30, 17, L(17, 'Plate Boundaries'),
      (L(17, 'Describe and explain destructive plate boundaries.'),),
      (S(12, 'Description/Explanation · 15', None, after='3C.'),),
      (srp('Description/explanation', 15, f'Description/Explanation · 15 x {SRPS}'),),
      '0-0', PS + EV, ID + 'p2-q3c'),
]

PART_TWO += [
    T('p2-4a', P2, '4A', '', 20, 18, L(18, 'Map Skills'),
      (L(18, 'Draw an outline map of an Irish region that you have studied.', 'Two named urban centres.'),),
      (S(13, 'Map outline', None),),
      sketch('Map outline · 4 marks graded (4/2/0)', (0, 2, 4),
             ('4 features @ 4 marks each · Shown 2 marks graded (2/1/0)', 'Named 2 marks'), sums((0, 1, 2), (0, 2)), 4),
      '1-4', IRL, ID + 'p2-q4a',
      row_labels=(None, L(18, 'A named river'), L(18, 'The outline of a named feature of relief (upland or lowland)'),
                  L(18, 'Two named urban centres.'), L(18, 'Two named urban centres.'))),
    T('p2-4b', P2, '4B', '', 30, 18, L(18, 'Concept of a Region'),
      (L(18, 'Examine how culture can be used to define regions, with reference to example(s)', 'have studied.'),),
      (S(14, 'Aspect of culture identified', '4C.'),),
      (fixed('Aspect of culture identified', 2, 'Aspect of culture identified · 2m'),
       fixed('Example of a region defined by culture', 2, 'Example of a region defined by culture · 2m'),
       srp('Examination', 13, f'Examination · 13 x {SRPS}')),
      '1-3', IRL + EURO, ID + 'p2-q4b'),
    T('p2-4c', P2, '4C', '', 30, 18, L(18, 'Primary Economic Activity – Agriculture'),
      (L(18, 'Explain the impact of climate on the development of agriculture in two contrasting',
         'that you have studied.'),),
      (S(14, 'Explanation Region 1', None),),
      (split('Explanation of the two regions (7/8 SRPs each)', 15,
             f'Explanation Region 1 · 7/8 x {SRPS}', f'Explanation Region 2 · 7/8 x {SRPS}'),),
      '1-5', EURO, ID + 'p2-q4c'),
]

Q5AS = (L(19, 'Examine the chart above showing the country of origin of first time asylum applicants',
          'following questions.'),)
PART_TWO += romans('5A', P2, 19, L(19, 'Population Dynamics'), Q5AS, ID + 'p2-q5a', ('page',), [
    ('(i)', 4, L(19, '(i) Name the two countries that had the highest percentage of first time asylum',
                 'EU in 2016.'),
     S(15, '(i) · Syria', '(ii) · Valid'),
     (fixed('Country 1', 2, '(i) · Syria · 2m'), fixed('Country 2', 2, 'Afghanistan · 2m')), '2-0', TG),
    ('(ii)', 4, L(19, '(ii) Explain briefly one reason why European Union member states are attractive',
                  'asylum applicants.'),
     S(15, '(ii) · Valid', '(iii) · 29'), (pair('(ii) · Valid brief explanation · 2m + 2m', 'Reason'),),
     '4-2', POP + EURO),
    ('(iii)', 4, L(19, '(iii) Calculate X, the percentage of first time asylum applicants in the category of',
                   'country of origin.'),
     S(15, '(iii) · 29', '(iv) · Two valid'), (fixed('X', 4, '(iii) · 29(%) · 4m'),), '2-0', TG),
    ('(iv)', 8, L(19, '(iv) Explain briefly two challenges faced by EU member states', 'seeking asylum in the EU.'),
     S(15, '(iv) · Two valid', None),
     (pair('(iv) · Two valid brief explanations · 2m + 2m', 'First challenge'), pair('=2m + 2m', 'Second challenge')),
     '4-2', POP + EURO),
])
ACCOUNTS = 'tourism or transport'
PART_TWO += [
    T('p2-5b', P2, '5B', '', 30, 19, L(19, 'Tertiary Economic Activity'),
      (L(19, 'Account for the development of tourism or transport in a Continental / Sub-Continental',
         'that you have studied.'),),
      (S(16, 'Examination · 15', None),), (srp('Examination', 15, f'Examination · 15 x {SRPS}'),),
      '1-6', CONT, ID + 'p2-q5b-tourism',
      routes=(Route('tourism', 'Tourism', ID + 'p2-q5b-tourism', False, ((ACCOUNTS, 'tourism'),)),
              Route('transport', 'Transport', ID + 'p2-q5b-transport', False, ((ACCOUNTS, 'transport'),)))),
    T('p2-5c', P2, '5C', '', 30, 19, L(19, 'Secondary Economic Activity'),
      (L(19, 'Examine the impact of each of the following on the development of secondary economic', 'Markets.'),),
      (S(17, 'Discussion of Factor 1', None),),
      (split('Discussion of the two factors (7/8 SRPs each)', 15,
             f'Discussion of Factor 1 · 7/8 x {SRPS}', f'Discussion of Factor 2 · 7/8 x {SRPS}'),),
      '1-4', IRL, ID + 'p2-q5c'),
]

Q6AS = (L(20, 'Examine the table above and answer each of the following questions.'),)
PART_TWO += romans('6A', P2, 20, L(20, 'Complexity of Regions'), Q6AS, ID + 'p2-q6a', ('page',), [
    ('(i)', 16, L(20, '(i) Using graph paper, draw a suitable graph to illustrate this data.'),
     S(18, 'Bar Chart · Pie Chart', '(ii) · Explain briefly'), GRAPH, '2-0', TG),
    ('(ii)', 4, L(20, '(ii) Explain briefly one strategy that could be used to address the decline',
                  'Gaeltacht areas.'),
     S(18, '(ii) · Explain briefly', None), (pair('Any valid brief explanation · 2m + 2m', 'Strategy'),),
     '1-3', IRL),
])
PART_TWO += [
    T('p2-6b', P2, '6B', '', 30, 20, L(20, 'Urban Development'),
      (L(20, 'Examine the factors that have influenced the development of one urban area in a',
         'that you have studied.'),),
      (S(19, 'Urban area named', '6C.'),),
      (fixed('Urban area named', 2, 'Urban area named · 2m'), pair('Factors identified · 2m + 2m', 'Factors identified'),
       srp('Examination', 12, f'Examination · 12 x {SRPS}')),
      '1-6', CONT + URB, ID + 'p2-q6b'),
    T('p2-6c', P2, '6C', '', 30, 20, L(20, 'European Union', nth=0),
      (L(20, 'Discuss the potential challenges facing the future development of the European Union',
         'sovereignty.'),),
      (S(19, 'Potential challenges identified', None),),
      (pair('Potential challenges identified · 2m + 2m', 'Potential challenges identified'),
       srp('Discussion', 13, f'Discussion · 13 x {SRPS}')),
      '1-3', EURO + EU_ECON, ID + 'p2-q6c'),
]

FACTORS_8C = ('Physical factors', 'Human factors', 'Political factors.')
ACTIVITY = 'footloose industries or financial services or mass tourism'
PART_TWO += [
    T('p2-7a', P2, '7A', '', 20, 22, L(22, 'Ordnance Survey Map'),
      (L(22, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper.', 'The reservoir.'),),
      (S(21, 'Sketch Outline', None),), OS_SKETCH, '2-6', MAP + ECON, ID + 'p2-q7a', ('map', 'legend'),
      row_labels=(None, L(22, 'The built up area of Sligo'), L(22, 'The entire route of the N16 road'),
                  L(22, 'The railway line'), L(22, 'The reservoir.'))),
    T('p2-7b', P2, '7B', '', 30, 22, L(22, 'Multinational Company'),
      (L(22, 'Examine the impact of each of the following on the operations of one multinational',
         'Developments in information technology.'),),
      (S(22, 'MNC named', '7C.'),),
      (fixed('MNC named', 2, 'MNC named · 2m'),
       srp('Examination of factor 1', 7, f'Examination factor 1 · 7 x {SRPS}'),
       srp('Examination of factor 2', 7, f'Examination factor 2 · 7 x {SRPS}')),
      '3-2', MNC, ID + 'p2-q7b'),
    T('p2-7c', P2, '7C', '', 30, 22, L(22, 'Economic Activities – Environmental Impact'),
      (L(22, 'Discuss how conflict may develop between economic interests and environmental interests',
         'that you have studied.'),),
      (S(22, 'Two examples named', None),),
      (pair('Two examples named · 2m + 2m', 'Two examples named'), srp('Discussion', 13, f'Discussion · 13 x {SRPS}')),
      '3-4', ENV, ID + 'p2-q7c'),
]

Q8AS = (L(23, 'Examine the information above and answer each of the following questions.'),)
PART_TWO += romans('8A', P2, 23, L(23, 'Energy', nth=0), Q8AS, ID + 'p2-q8a', ('page',), [
    ('(i)', 2, L(23, '(i) What percentage of EU-28 energy was consumed by transport in 2015?'),
     S(23, '(i) · 33.1', '(ii) · 13.5'), (fixed('Percentage', 2, '(i) · 33.1(%) · 2m'),), '2-0', TG),
    ('(ii)', 4, L(23, '(ii) Calculate X, the percentage of energy consumed by the services sector', 'in 2015.'),
     S(23, '(ii) · 13.5', '(iii) · Solid'), (fixed('X', 4, '(ii) · 13.5(%) · 4m'),), '2-0', TG),
    ('(iii)', 4, (L(23, '(iii) Which fuel was used to generate exactly 24.5% of EU-28 energy in 2015?'),
                  L(23, 'Name one example of this type of fuel.')),
     S(23, '(iii) · Solid', '(iv) · Renewables'),
     (fixed('Fuel', 2, '(iii) · Solid Fuel · 2m'), fixed('Example', 2, 'Any valid example · 2m')), '2-0', TG + ENERGY),
    ('(iv)', 2, L(23, '(iv) Which fuel was used to generate the highest percentage of energy in the EU-28', 'in 2015?'),
     S(23, '(iv) · Renewables', '(v) · Any two'), (fixed('Fuel', 2, '(iv) · Renewables · 2m'),), '2-0', TG),
    ('(v)', 4, L(23, '(v) Name two examples of renewable energy.'), S(23, '(v) · Any two', '(vi) · Valid'),
     (pair('(v) · Any two valid examples · 2m + 2m', 'Two examples'),), '3-5', ENERGY),
    ('(vi)', 4, L(23, '(vi) Explain briefly one reason why nuclear energy is not used in Ireland.'),
     S(23, '(vi) · Valid', None), (pair('(vi) · Valid brief explanation · 2m + 2m', 'Reason'),), '3-5', ENERGY),
])
PART_TWO += [
    T('p2-8b', P2, '8B', '', 30, 23, L(23, 'European Union – Trade'),
      (L(23, 'Describe the current trading patterns of the European Union', 'these trading patterns.'),),
      (S(24, 'Internal trading pattern', '8C.'),),
      (fixed('Internal trading pattern identified', 2, 'Internal trading pattern identified · 2m'),
       fixed('External trading pattern identified', 2, 'External trading pattern identified · 2m'),
       pair('Factors influencing trading patterns identified · 2m + 2m', 'Factors identified'),
       srp('Description/explanation', 11, f'Description/explanation · 11 x {SRPS}')),
      '3-3', EU_ECON, ID + 'p2-q8b'),
    T('p2-8c', P2, '8C', '', 30, 23, L(23, 'Economic Development – Developed Economy'),
      (L(23, 'Examine the impact of two of the following on the development of footloose industries',
         'Political factors.'),),
      (S(24, 'Named developed economy', None),),
      (fixed('Named developed economy', 2, 'Named developed economy · 2m'),
       srp('Examination of factor 1', 7, f'Examination of factor 1 · 7 x {SRPS}'),
       srp('Examination of factor 2', 7, f'Examination of factor 2 · 7 x {SRPS}')),
      '3-0', ECON, ID + 'p2-q8c-footloose-industries',
      # Choose ONE printed activity (a route each); the choose-two factor pool
      # within it is one card.
      routes=tuple(Route(slug(activity), activity, ID + f'p2-q8c-{slug(activity)}', False,
                         ((ACTIVITY, activity),),
                         absorbs=pool(ID + f'p2-q8c-{slug(activity)}-', FACTORS_8C, 2)[1])
                   for activity in ('footloose industries', 'financial services', 'mass tourism'))),
]

Q9AS = (L(24, 'Examine the table above and answer each of the following questions.'),)
PART_TWO += romans('9A', P2, 24, L(24, 'Irish Trade'), Q9AS, ID + 'p2-q9a', ('page',), [
    ('(i)', 4, L(24, '(i) Which category of export to Great Britain and Northern Ireland experienced a',
                 'January-July 2017?'),
     S(25, '(i) · Fishing', '(ii) · 35,923'), (fixed('Category', 4, '(i) · Fishing · 4m'),), '2-0', TG),
    ('(ii)', 2, L(24, '(ii) What was the total value of exports (€ millions) to European Union (EU) member',
                  'January-July 2017?'),
     S(25, '(ii) · 35,923', '(iii) · 6.09'), (fixed('Total value', 2, '(ii) · 35,923 (€ millions) · 2m'),),
     '2-0', TG),
    ('(iii)', 2, L(24, '(iii) What percentage of total exports were Agricultural exports in the period',
                   'January-July 2017?'),
     S(25, '(iii) · 6.09', '(iv) · Two valid'), (fixed('Percentage', 2, '(iii) · 6.09% · 2m'),), '2-0', TG),
    ('(iv)', 4, L(24, '(iv) Name any two examples of Irish exports in the category of Unclassified.'),
     S(25, '(iv) · Two valid', '(v) · Two valid'), (pair('(iv) · Two valid examples · 2m + 2m', 'Two examples'),),
     '3-3', ECON + EU_ECON),
    ('(v)', 8, L(24, '(v) Explain briefly two potential impacts of future changes to European Union',
                 'Irish trade.'),
     S(25, '(v) · Two valid', None),
     (pair('(v) · Two valid brief explanations 2m + 2m', 'First impact'), pair('=2m + 2m', 'Second impact')),
     '3-3', EU_ECON),
])
Q9CS = (L(25, 'Answer each of the following questions with reference to the 1:50 000 Ordnance Survey',
          'aerial photograph.'),)
Q9CI = L(25, '(i) Name two renewable energy sources that could be developed in the area', 'accepted notation.')
PART_TWO.append(T(
    'p2-9b', P2, '9B', '', 30, 24, L(24, 'Economic Development'),
    (L(24, 'Discuss the Human Development Index (HDI) and Gross National Product (GNP) as',
       'economic development.'),),
    (S(26, 'Reference to HDI', '9C.'),),
    (fixed('Reference to HDI as measure', 2, 'Reference to HDI as measure · 2m'),
     fixed('Reference to GNP as measure', 2, 'Reference to GNP as measure · 2m'),
     srp('Discussion', 13, f'Discussion · 13 x {SRPS}')),
    '3-1', DEV + ECON, ID + 'p2-q9b'))
PART_TWO += romans('9C', P2, 25, L(25, 'Location of Economic Activity'), Q9CS, ID + 'p2-q9c',
                   ('aerial', 'map', 'legend'), [
    ('(i)', 8, Q9CI, S(26, '(i) · Renewable energy named', '(ii) · Explanation'),
     (pair('(i) · Renewable energy named · 2m + 2m', 'Renewable energy sources named'),
      pair('Map or Photo Reference · 2m + 2m', 'Map or photograph references')), '3-5', ENERGY + MAP + AER),
    ('(ii)', 14, L(25, '(ii) With reference to one of the renewable energy sources named by you in part (i),',
                   'chosen location.'),
     S(26, '(ii) · Explanation', '(iii) · Explanation'), (srp('Explanation', 7, f'(ii) · Explanation · 7 x {SRPS}'),),
     '3-5', ENERGY + MAP + AER, (), (Q9CI,)),
    ('(iii)', 8, L(25, '(iii) Explain one reason why local people might object to this development.'),
     S(26, '(iii) · Explanation', None), (srp('Explanation', 4, f'(iii) · Explanation · 4 x {SRPS}'),),
     '3-5', ENERGY + ENV, (), (Q9CI,)),
])

PROBLEMS = ('Housing', 'Transport', 'Pollution.')
PART_TWO += [
    T('p2-10a', P2, '10A', '', 20, 26, L(26, 'Aerial Photograph'),
      (L(26, 'Draw a sketch map of the aerial photograph, half the length and half the breadth.',
         'A carpark in the left foreground.'),),
      (S(27, 'Sketch Outline', None),),
      sketch('Sketch Outline · 4 marks (4/0)', (0, 4),
             ('4 features @ 4 marks each · Shown 3 marks (graded 3/1/0)', 'Named 1 mark'), sums((0, 1, 3), (0, 1)), 4),
      '2-8', AER + URB, ID + 'p2-q10a', ('aerial',),
      row_labels=(None, L(26, 'The river'), L(26, 'A large historical ruin in the middle ground'),
                  L(26, 'Emergency services depot in the left background'), L(26, 'A carpark in the left foreground.'))),
    T('p2-10b', P2, '10B', '', 30, 26, L(26, 'Urban Planning'),
      (L(26, 'Examine the effectiveness of urban planning strategies in solving two of the following', 'Pollution.'),),
      (S(28, 'Examination of problem 1', '10C.'),),
      (srp('Examination of problem 1', 7, f'Examination of problem 1 · 7 x {SRPS}'),
       srp('Examination of problem 2', 7, f'Examination of problem 2 · 7 x {SRPS}'),
       fixed('Example of urban area', 2, 'Example of urban area · 2m')),
      '4-5', URB, ID + 'p2-q10b', absorbs=pool(ID + 'p2-q10b-', PROBLEMS, 2)[1]),
    T('p2-10c', P2, '10C', '', 30, 26, L(26, 'Migration'),
      (L(26, 'Discuss how recent trends in migration are impacting on migration policy in Europe.'),),
      (S(28, 'Impact on migration policy identified', None),),
      (fixed('Impact on migration policy identified', 2, 'Impact on migration policy identified · 2m'),
       srp('Discussion', 14, f'Discussion · 14 x {SRPS}')),
      '4-2', POP, ID + 'p2-q10c'),
]

Q11AS = (L(27, 'Examine the graph above and answer each of the following questions.'),)
PART_TWO += romans('11A', P2, 27, L(27, 'Irish Population'), Q11AS, ID + 'p2-q11a', ('page',), [
    ('(i)', 2, L(27, '(i) What will the old age dependency ratio (%) be in 2024?'),
     S(29, '(i) · 25', '(ii) · 1996 to'), (fixed('Ratio', 2, '(i) · 25 (%) · 2m'),), '2-0', TG),
    ('(ii)', 2, L(27, '(ii) In what period of years in the graph was the old age dependency ratio declining?'),
     S(29, '(ii) · 1996 to', '(iii) · 28'), (fixed('Period', 2, '(ii) · 1996 to 2008 · 2m'),), '2-0', TG),
    ('(iii)', 2, L(27, '(iii) How many years will it take for the old age dependency ratio to double from its',
                   '2016 level?'),
     S(29, '(iii) · 28', '(iv) · 2008'), (fixed('Years', 2, '(iii) · 28 (years) · 2m'),), '2-0', TG),
    ('(iv)', 2, L(27, '(iv) In which year in the graph was the old age dependency ratio at its most favourable',
                  'level economically?'),
     S(29, '(iv) · 2008', '(v) · Valid'), (fixed('Year', 2, '(iv) · 2008 · 2m'),), '2-0', TG),
    ('(v)', 4, L(27, '(v) Explain briefly one reason for an increase in the old age dependency ratio.'),
     S(29, '(v) · Valid', '(vi) · Two valid'), (pair('(v) · Valid brief explanation · 2m + 2m', 'Reason'),),
     '4-0', POP),
    ('(vi)', 8, L(27, '(vi) Explain briefly two effects of an increase in the old age dependency ratio.'),
     S(29, '(vi) · Two valid', None),
     (pair('(vi) · Two valid brief explanations 2m + 2m', 'First effect'), pair('=2m + 2m', 'Second effect')),
     '4-0', POP),
])
PART_TWO += [
    T('p2-11b', P2, '11B', '', 30, 27, L(27, 'Settlement Distribution'),
      (L(27, 'Examine the 1:50 000 Ordnance Survey map of Sligo accompanying this paper.'),
       L(27, 'Using evidence from the map, account for variations in settlement distribution', 'shown on the map.')),
      (S(30, 'Variations in settlement', '11C.'),),
      (pair('Variations in settlement distribution identified · 2m + 2m', 'Variations identified'),
       fixed('OS map evidence', 2, 'OS map evidence · 2m'), srp('Examination', 12, f'Examination · 12 x {SRPS}')),
      '4-3', URB + MAP, ID + 'p2-q11b', ('map', 'legend')),
    T('p2-11c', P2, '11C', '', 30, 27, L(27, 'Future Urbanism'),
      (L(27, 'Discuss two issues facing cities of the future in the developed world.'),),
      (S(30, 'Two issues identified', None),),
      (pair('Two issues identified · 2m + 2m', 'Two issues identified'),
       split('Discussion of the two issues (7/6 SRPs each)', 13,
             f'Discussion of issue one · 7/6 x {SRPS}', f'Discussion of issue two · 7/6 x {SRPS}')),
      '4-5', URB, ID + 'p2-q11c'),
]

Q12AS = (L(28, 'Examine the table above showing the number of people living in urban areas',
           'Answer each of the following questions.'),)
PART_TWO += romans('12A', P2, 28, L(28, 'Urbanisation', nth=0), Q12AS, ID + 'p2-q12a', ('page',), [
    ('(i)', 4, L(28, '(i) Which two regions will have the greatest percentage of their total population living',
                 'by 2050?'),
     S(31, '(i) · North America', '(ii) · 51.97'),
     (fixed('Region 1', 2, '(i) · North America · 2m'), fixed('Region 2', 2, 'Europe · 2m')), '2-0', TG),
    ('(ii)', 4, L(28, '(ii) Calculate the percentage change in the number of people living in urban areas in',
                  'between 2014 and 2050.'),
     S(31, '(ii) · 51.97', '(iii) · Valid'), (fixed('Percentage change', 4, '(ii) · 51.97 (%) · 4m'),), '2-0', TG),
    ('(iii)', 4, L(28, '(iii) Explain briefly one reason for this change in the number of people living in urban',
                   'areas in Ireland.'),
     S(31, '(iii) · Valid', '(iv) · Two valid'), (pair('(iii) · Valid brief explanation · 2m + 2m', 'Reason'),),
     '4-3', URB),
    ('(iv)', 8, (L(28, '(iv) According to the table, the number of people living in urban areas in Sub-Saharan',
                   'significantly by 2050.'),
                 L(28, 'Explain briefly two potential problems resulting from this increase.')),
     S(31, '(iv) · Two valid', None),
     (pair('(iv) · Two valid brief explanations 2m + 2m', 'First problem'), pair('=2m + 2m', 'Second problem')),
     '4-5', URB),
])
PART_TWO += [
    T('p2-12b', P2, '12B', '', 30, 28, L(28, 'Population Characteristics – Ireland'),
      (L(28, 'Describe and explain how the characteristics of Ireland’s population have changed', '1950’s.'),),
      (S(32, 'Change in population characteristics identified', '12C.'),),
      (fixed('Change in population characteristics identified', 2,
             'Change in population characteristics identified · 2m'),
       srp('Description/explanation', 14, f'Description / Explanation · 14 x {SRPS}')),
      '4-0', POP, ID + 'p2-q12b'),
    T('p2-12c', P2, '12C', '', 30, 28, L(28, 'Urban Expansion'),
      (L(28, 'As cities grow and expand they impact on the surrounding rural areas.'),
       L(28, 'Discuss this statement with reference to example(s) that you have studied.')),
      (S(32, 'Impact identified · 2m', None),),
      (fixed('Impact identified', 2, 'Impact identified · 2m'), fixed('Example', 2, 'Example · 2m'),
       srp('Discussion', 13, f'Discussion · 13 x {SRPS}')),
      '4-5', URB, ID + 'p2-q12c'),
]

# ------------------------------------------------------------------ Options --
OC = (S(34, '*Overall Coherence (20 marks)', None, table=True),)
OPTION_CRITERIA = (
    Criterion('Aspects (3 @ 20 marks or 4 @ 15 marks)', 60, upto(60), 'srp',
              ('Number of aspects', '?For each aspect:', 'Identifying aspect', '8 x SRP')),
    Criterion('Overall coherence', 20, (0, 6, 10, 14, 17, 20), 'exact',
              ('Overall Coherence · 20 marks graded*', '*Overall Coherence (20 marks)', 'Excellent · 20',
               'Very Good · 17', 'Good · 14', 'Fair · 10', 'Weak · 6', 'Poor · 0')))


def option(q, page, theme, note_nth, prompt, scheme_page, topic, atlas, after=None, end=None, absorbs=()):
    return T(f'p2-{q}', P2, q, '', 80, page, theme, prompt if isinstance(prompt, tuple) else (prompt,),
             (S(scheme_page, 'Number of aspects', end, None, after), *OC), OPTION_CRITERIA,
             topic, (atlas,), ID + f'p2-q{q}',
             stem=(L(page, 'Note: It is better to discuss three or four aspects', 'large number of points.',
                     nth=note_nth),),
             absorbs=absorbs)


GI, GE = H + 'option-global-interdependence', H + 'option-geoecology'
CI, AO = H + 'option-culture-identity', H + 'option-atmosphere-ocean'
SUSTAINABILITY = ('Resource use', 'Fair trade', 'Justice issues', 'Self-reliance.')
CLIMATE = ('Temperature', 'Precipitation', 'Location', 'Pressure belts (air circulation).')
OPTIONS = [
    option('13', 30, L(30, 'Global Interdependence'), 0,
           L(30, 'We live in an interdependent global economy.', 'Impact of social and political decisions.'),
           35, '5-1', GI),
    option('14', 30, L(30, 'Global Interdependence'), 0,
           L(30, 'Views of development and underdevelopment are subject to change.',
             'contrasting approaches to development.'), 36, '5-0', GI, after='14.', end='15.'),
    option('15', 30, L(30, 'Global Interdependence'), 0,
           L(30, 'Sustainability is a model for future development.', 'Self-reliance.'), 36, '5-3', GI,
           after='15.', absorbs=pool(ID + 'p2-q15-', SUSTAINABILITY, 3)[1]),
    option('16', 30, L(30, 'Geoecology'), 1,
           L(30, 'Soil characteristics are affected by a combination of processes', 'affect soil characteristics.'),
           37, '6-1', GE, after='16.', end='17.'),
    option('17', 30, L(30, 'Geoecology'), 1,
           L(30, 'Describe and explain the general composition and characteristics of any one soil type.'),
           37, '6-0', GE, after='17.'),
    option('18', 30, L(30, 'Geoecology'), 1,
           L(30, 'Describe the specific climatic and soil characteristics experienced in one biome',
             'vegetation in this biome.'), 38, '6-2', GE),
    option('19', 31, L(31, 'Culture and Identity'), 0,
           L(31, 'Examine the importance of religion as a cultural indicator.'), 39, '7-0', CI,
           after='19.', end='20.'),
    option('20', 31, L(31, 'Culture and Identity'), 0,
           L(31, 'Discuss the idea of multiculturalism as it applies to the modern world.'), 39, '7-2', CI,
           after='20.'),
    option('21', 31, L(31, 'Culture and Identity'), 0,
           L(31, 'Examine the influence of physical and political boundaries on the concept of identity.'),
           40, '7-1', CI),
    option('22', 31, L(31, 'The Atmosphere – Ocean Environment'), 1,
           L(31, 'Describe the formation of each of the following and discuss its impact on weather patterns:',
             'Land and sea breezes.'), 41, '8-3', AO),
    option('23', 31, L(31, 'The Atmosphere – Ocean Environment'), 1,
           L(31, 'Examine one distinctive global climate type that you have studied', 'Pressure belts (air circulation).'),
           42, '8-4', AO, after='23.', end='24.', absorbs=pool(ID + 'p2-q23-', CLIMATE, 3)[1]),
    option('24', 31, L(31, 'The Atmosphere – Ocean Environment'), 1,
           L(31, 'Climate changes over time and space.', 'Discuss.'), 42, '8-4', AO, after='24.'),
]

TASKS = [*PART_ONE, *PART_TWO, *OPTIONS]

ID_CORRECTION_REASON = 'No 2018 Higher card shipped before this review; every card is new.'

# No 2018 Higher card was live on origin/main before this review.
LEGACY_IDS: list[str] = []
