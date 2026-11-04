"""Independent review ledger: Leaving Certificate Geography 2016 Ordinary Level.

Sources (English editions, harvested Paper Trail corpus; sizes and SHA-256
pinned in EXPECTED_SOURCES and the generated audit): the examination paper
LC005GLP000EV (32 pages; one booklet printed Part One, answered in it, and
Part Two), marking scheme LC005GLP000EV (40 pages), and the common Westport
companions shared with Higher Level — the 1:50 000 map LC005CLP003EV (a
1135 x 783 pixel image in a one-page PDF), its legend LC005CLPC00EV and the
aerial photograph LC005CLP004EV. Part One is 100 marks (any ten of twelve
@ 10), Part Two 300 (three questions @ 100).

Visual sweep (every page rendered and read on 2026-10-14):
  Paper p1 cover and examiner's grid; p2-p11 Part One Questions 1-12 (p3
  holds Q2 and Q3, p7 Q7 and Q8); p12 Part Two instructions; p13 Section 1
  divider; p14-p21 Q1-Q6 (p14 and p18 open with their dividers; p16 holds
  3A and 3B, p17 3C, p20 6A and 6B, p21 6C); p22 Section 2 divider;
  p23-p28 Electives Q7-Q12 (p23 and p26 open with their elective
  dividers); p29-p32 printed "Blank Page".
  Scheme p1 cover; p2-p3 notes; p4-p5 Geographical Investigation
  (coursework) and its presentation marks; p6-p7 Part One table (Q1-Q6,
  Q7-Q12); p8 Part Two instructions; p9 Section 1 divider; p10-p22 Q1-Q6;
  p23 Section 2 divider; p24-p35 Q7-Q12; p36 investigation topics; p37
  Irish-language bonus marks; p38-p39 printed "Blank Page"; p40 back cover.

Boundaries and tariffs follow the 2017 Ordinary ledger: every priced roman
is a task, and so is every lettered statement priced on its own (Q1(i)(a)-
(d), Q6(i)(a)-(d)). Matching tables, in the printed row order: Q3 L 981 846
Parking, L 971 857 18 hole Golf Course, L 972 793 Waymarked Walk/Trailhead,
M 037 868 Fulacht Fia/River/Stream; Q4 Crater C, Secondary volcanic cone A,
Magma chamber D, Vent B; Q5 A Waterfall Erosion, B (Erratic printed)
Deposition, C Sea Arch (Erosion printed), D (Tombolo printed) Deposition;
Q7 High Pressure System C, Cold Front D, Low Pressure System B, Warm Front
A; Q8 Onion weathering E, Hydraulic action D, Freeze-thaw action A,
Longshore drift C, Plucking B; Q10 Solar power plant C, Japan tsunami E,
Copacabana Beach B, Atlantic storm A, Retreating glacier F (Forest fires D
is printed); Q12 The Gaeltacht B, Mezzogiorno D, Islamic World E, Greater
Dublin Area C, Cool Temperate Oceanic A. Q5 answers (i) and (ii) in one
part-completed table and the scheme prices each row, so it is one card.

The sketch maps price five items: 2A's five are Westport Bay, the Owenwee
River, the two named lakes and the coniferous plantation; 7A prints five
bullets; 10A prints four, and its "Two churches" is read as two items
(7A and 2017 carry "Two connecting streets" as one).

Tariffs as printed: twelve parts carry 40 marks (1B, 2B, 3C, 4B, 5B, 6C,
7C, 8B, 9C, 10B, 11C, 12C) and the rest 30.
"""

from geography_review import (
    Criterion, Lift, Route, SchemeSlice, Task, pool, fixed, slug, srp, steps, sums,
)

YEAR = 2016
LEVEL = 'ordinary'
PAPER_PAGES = {1: 32, 2: 32}
SCHEME_PAGES = 40
_FORTY = {'1B', '2B', '3C', '4B', '5B', '6C', '7C', '8B', '9C', '10B', '11C', '12C'}
QUESTION_TARIFFS = {1: {str(n): 10 for n in range(1, 13)},
                    2: {f'{n}{x}': (40 if f'{n}{x}' in _FORTY else 30)
                        for n in range(1, 13) for x in 'ABC'}}

EXPECTED_SOURCES = {
    'paper1': ('LC005GLP000EV.pdf', 3794462),
    'paper2': ('LC005GLP000EV.pdf', 3794462),
    'scheme': ('LC005GLP000EV.pdf', 437943),
    'map': ('LC005CLP003EV.pdf', 327650),
    'legend': ('LC005CLPC00EV.pdf', 745443),
    'aerial': ('LC005CLP004EV.pdf', 5761875),
}

_PAPER = {1: 'cover and examiner grid', **{p: 'question' for p in range(2, 12)},
          12: 'Part Two instructions', 13: 'section divider', **{p: 'question' for p in range(14, 22)},
          22: 'section divider', **{p: 'question' for p in range(23, 29)},
          29: 'blank page', 30: 'blank page', 31: 'blank page', 32: 'blank page'}
PAGE_REVIEW = {
    # One booklet printed both parts.
    'paper1': _PAPER, 'paper2': _PAPER,
    'scheme': {1: 'cover', 2: 'notes', 3: 'notes', 4: 'geographical investigation (coursework)',
               5: 'presentation marks (coursework)', 6: 'Part One table', 7: 'Part One table',
               8: 'Part Two instructions', 9: 'section divider',
               **{p: 'Part Two allocation' for p in range(10, 23)}, 23: 'section divider',
               **{p: 'Part Two allocation' for p in range(24, 36)},
               36: 'investigation topics', 37: 'Irish-language bonus marks',
               38: 'blank', 39: 'blank', 40: 'back cover'},
}

EXPECTED_SELECTION_SCAN = [
    [1, 2, 'attempt any ten'], [1, 12, 'attempt three'], [1, 13, 'attempt two'],
    [1, 14, 'attempt one'], [1, 14, 'answer (i) or (ii)'], [1, 14, 'any two'], [1, 14, 'any two'],
    [1, 14, 'attempt to'], [1, 14, 'either'],
    [1, 16, 'one of the following'],
    [1, 18, 'attempt one'], [1, 18, 'any two'],
    [1, 19, 'any two'],
    [1, 22, 'attempt one'],
    [1, 24, 'any two'],
    [1, 26, 'any two'],
]
SELECTION_REVIEW = [
    {'scan': [[1, 2, 'attempt any ten'], [1, 12, 'attempt three'], [1, 13, 'attempt two'], [1, 14, 'attempt one'],
              [1, 18, 'attempt one'], [1, 22, 'attempt one']],
     'kind': 'exam-attempt-rule',
     'reason': 'Part One any ten of twelve and Part Two three questions (one of Q1-3, one of Q4-6, one elective) are attempt rules; every question is carded.'},
    {'scan': [[1, 14, 'answer (i) or (ii)']], 'kind': 'closed-route',
     'reason': '1B: (i) or (ii) -> two routes, each with its own scheme allocation. 8B "tourism or financial services" runs through all four romans -> 2 routes on each (no directive word the scan reads; the route text is anchored on the paper).'},
    {'scan': [[1, 14, 'either']], 'kind': 'closed-route',
     'reason': '1C: either river processes or coastal processes or mass movement processes -> 3 routes under one allocation.'},
    {'scan': [[1, 16, 'one of the following']], 'kind': 'closed-choose-one',
     'reason': '3B one of four printed rock-cycle activities -> 4 routes.'},
    {'scan': [[1, 18, 'any two'], [1, 19, 'any two']], 'kind': 'choose-n-one-card',
     'reason': '4B(ii) any two of three printed factors and 5B any two of three printed activities -> one card each with every printed item (choice is not a route).'},
    {'scan': [[1, 14, 'any two'], [1, 14, 'any two'], [1, 24, 'any two'], [1, 26, 'any two']],
     'kind': 'open-response',
     'reason': 'No printed pool: 1B(i) any two landforms and 1B(ii) any two mass movement processes (the scheme prices two @ 20m); 8A(iii) any two HDI factors; 10C(i) any two functions. Compulsory lists stay whole: 2A, 4A, 7A, 10A each item; 4C lists the cultural factors as context, not a choice.'},
    {'scan': [[1, 14, 'attempt to']], 'kind': 'not-a-selection',
     'reason': '1C "how humans attempt to control" describes human activity, not a candidate choice.'},
]

P1, P2 = 1, 2
ID = 'geography-2016-ol-'
O = 'geography-ordinary-'
SRP3 = 3


def L(page, start, end=None, nth=None):
    return Lift(page, start, end, None, nth)


def S(page, start, end=None, clip=None, after=None, table=False):
    return SchemeSlice(page, start, end, clip, after, table)


def srp3(label, count, line):
    return srp(label, count, line, SRP3)


def T(key, part, q, sub, marks, page, title, prompt, scheme, criteria, topic, atlas, card_id,
      sources=(), stem=(), routes=(), row_labels=(), absorbs=()):
    return Task(key, part, q, sub, marks, page, title, prompt, scheme, criteria, topic, atlas,
                sources, card_id, False, stem=stem, routes=routes, row_labels=row_labels,
                absorbs=absorbs)


def rows(lines, marks=2):
    return tuple(fixed(f'Row {i}', marks, line) for i, line in enumerate(lines, 1))


def romans(q, part, page, title, stem, first_id, sources, parts):
    """Separately priced romans. parts: (sub, marks, prompt Lift(s), scheme slice(s), criteria, topic, atlas
    [, row labels[, extra stem Lifts]])."""
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


def bullet_routes(prefix, items, atlas=None):
    return tuple(Route(slug(item, 34), item.rstrip('.'), ID + prefix + slug(item, 34), False,
                       keep_bullets=(item,), atlas=(atlas[item] if atlas else None))
                 for item in items)


PS = (O + 'plate-tectonics',)
RW = (O + 'rocks-weathering-mass-movement',)
SEA = (O + 'the-sea',)
RIVERS = (O + 'rivers',)
GLAC = (O + 'glaciation',)
EV = (O + 'earthquakes-volcanoes',)
KARST = (O + 'karst-regions',)
MAP = (O + 'mapwork',)
AER = (O + 'aerial-photos',)
GRAPH = (O + 'graph-style-questions',)
WEATHER = (O + 'weather-climate',)
CONT = (O + 'regions-continental',)
EURO = (O + 'regions-european',)
IRL = (O + 'regions-ireland',)
ECON = (O + 'elective-economic',)
EU = (O + 'economic-ireland-the-eu',)
MNC = (O + 'economic-multinationals-globalisation',)
ENV = (O + 'economic-environmental-impact',)
DEV = (O + 'economic-developing-economies',)
POP = (O + 'human-population',)
URB = (O + 'human-urban-geography',)
PS_SURFACE = RIVERS + SEA + GLAC
BRIEF = 'Brief explanation 2 SRP’s @ 3m each · 6m'

# ---------------------------------------------------------------- Part One --
TF1 = L(2, '(i) Indicate whether each of the following statements is true or false, by circling the',
        'correct option in each case.')
PART_ONE = romans('1', P1, 2, L(2, 'Aerial Photograph'),
                  (L(2, 'Examine the aerial photograph of Westport accompanying this paper and answer each of',
                     'following questions.'),),
                  ID + 'p1-q1', ('aerial',), [
    ('(i)(a)', 2, (TF1, L(2, '(a) There is a river meander in the right background.')),
     S(6, 'Q1. (i)', '(b) True'), (fixed('Statement (a)', 2, 'Q1. (i) · (a) False · 2m'),), '2-8', AER),
    ('(i)(b)', 2, (TF1, L(2, '(b) There is a bridge crossing the river in the centre middleground.')),
     S(6, '(b) True', '(c) True', None, 'Q1. (i)'), (fixed('Statement (b)', 2, '(b) True · 2m'),), '2-8', AER),
    ('(i)(c)', 2, (TF1, L(2, '(c) There is a church located in the centre foreground.')),
     S(6, '(c) True', '(d) False', None, 'Q1. (i)'), (fixed('Statement (c)', 2, '(c) True · 2m'),), '2-8', AER),
    ('(i)(d)', 2, (TF1, L(2, '(d) There is a large playing field in the left foreground.')),
     S(6, '(d) False', 'Q.1 (ii)', None, 'Q1. (i)'), (fixed('Statement (d)', 2, '(d) False · 2m'),), '2-8', AER),
    ('(ii)', 2, L(2, '(ii) Indicate whether the aerial photograph accompanying this paper is a vertical or',
                  'Vertical Oblique'),
     S(6, 'Q.1 (ii)', 'Q.2 (i)'), (fixed('Type of photograph', 2, 'Q.1 (ii) · Oblique · 2m · Total 10m'),),
     '2-8', AER),
])
OS3 = L(3, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper.', nth=1)
PART_ONE += romans('2', P1, 3, L(3, 'Ordnance Survey Map', nth=0),
                   (L(3, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper.', nth=0),),
                   ID + 'p1-q2', ('map', 'legend'), [
    ('(i)', 5, L(3, '(i) What is the total area of the map?', '108 km2'),
     S(6, 'Q.2 (i)', 'Q.2 (ii)'), (fixed('Area', 5, 'Q.2 (i) · 108 km2 · 5m'),), '2-6', MAP),
    ('(ii)', 5, L(3, '(ii) The length of the N5 road', 'Tick the correct box.'),
     S(6, 'Q.2 (ii)', 'Q.3 (i)'), (fixed('Length', 5, 'Q.2 (ii) · 4.4 km · 5m · Total 10m'),), '2-6', MAP),
])
PART_ONE += romans('3', P1, 3, L(3, 'Ordnance Survey Map', nth=1), (OS3,), ID + 'p1-q3', ('map', 'legend'), [
    ('(i)', 8, L(3, '(i) Name the features which can be found at each of the following grid references:'),
     S(6, 'Q.3 (i)', 'Q.3 (ii)'),
     rows(['Q.3 (i) · Parking · 2m', '18 hole Golf Course · 2m', 'Waymarked Walk/Trailhead · 2m',
           'Fulacht Fia/River/Stream · 2m']), '2-6', MAP,
     (L(3, 'L 981 846'), L(3, 'L 971 857'), L(3, 'L 972 793'), L(3, 'M 037 868'))),
    ('(ii)', 2, L(3, '(ii) Draw the Ordnance Survey map symbol for a Picnic Site in the box below.'),
     S(6, 'Q.3 (ii)', 'Q.4 (i)'), (fixed('Symbol', 2, 'Q.3 (ii) · Correct symbol · 2m · Total 10m'),), '2-6', MAP),
])
PART_ONE += romans('4', P1, 4, L(4, 'Volcanoes'),
                   (L(4, 'Examine the diagram of a volcano above and answer each of the following questions.'),),
                   ID + 'p1-q4', ('page',), [
    ('(i)', 8, L(4, '(i) Match each of the letters A, B, C and D with the feature that best matches it in the',
                 'table below.'),
     S(6, 'Q.4 (i)', 'Q.4 (ii)'), rows(['Q.4 (i) · C · 2m', '=A · 2m', '=D · 2m', '=B · 2m']), '0-7', EV,
     (L(4, 'Crater'), L(4, 'Secondary volcanic cone'), L(4, 'Magma chamber'), L(4, 'Vent'))),
    ('(ii)', 2, L(4, '(ii) What name is given to a volcano that has not erupted in many hundreds of years',
                  'Dormant Active'),
     S(6, 'Q.4 (ii)', 'Q.5'), (fixed('Name', 2, 'Q.4 (ii) · Dormant · 2m · Total 10m'),), '0-7', EV),
])
PART_ONE.append(T(
    'p1-5', P1, '5', '', 10, 5, L(5, 'Physical Landforms and Processes'),
    (L(5, 'Examine the photographs and complete the table below by answering each of the following questions.',
       'Some of the table is completed for you.'),
     L(5, '(i) Name each of the landforms in the photographs above.'),
     L(5, '(ii) State whether the process of erosion or the process of deposition is most associated',
       'formation of each landform.')),
    (S(6, 'Q.5', 'Q.6 (i)'),),
    (fixed('Photograph A', 4, 'Q.5 · Waterfall Erosion · 2m + 2m', (0, 2, 4)),
     fixed('Photograph B', 2, 'Erratic Deposition · 2m'),
     fixed('Photograph C', 2, 'Sea Arch Erosion · 2m'),
     fixed('Photograph D', 2, 'Tombolo Deposition · 2m · Total 10m')),
    '0-4', PS_SURFACE, ID + 'p1-q5', ('page',)))
TF6 = L(6, '(i) Indicate whether each of the following statements is true or false, by circling the',
        'correct option in each case.')
PART_ONE += romans('6', P1, 6, L(6, 'Rocks'),
                   (L(6, 'Examine the photographs below and answer each of the following questions.'),),
                   ID + 'p1-q6', ('page',), [
    ('(i)(a)', 2, (TF6, L(6, '(a) The rock type in the photograph is limestone and it is a permeable rock.')),
     S(6, 'Q.6 (i)', '(b) False'), (fixed('Statement (a)', 2, 'Q.6 (i) · (a) True · 2m'),), '0-1', RW + KARST),
    ('(i)(b)', 2, (TF6, L(6, '(b) The rock type in the photograph is slate and it was formed from lava cooling.')),
     S(6, '(b) False', '(c) True', None, 'Q.6 (i)'), (fixed('Statement (b)', 2, '(b) False · 2m'),), '0-1', RW),
    ('(i)(c)', 2, (TF6, L(6, '(c) The rock type in the photograph is marble', 'heat and/or pressure.')),
     S(6, '(c) True', '(d) True', None, 'Q.6 (i)'), (fixed('Statement (c)', 2, '(c) True · 2m'),), '0-1', RW),
    ('(i)(d)', 2, (TF6, L(6, '(d) The rock type in the photograph is basalt and it can be found in Co. Antrim.')),
     S(6, '(d) True', 'Q.6 (ii)', None, 'Q.6 (i)'), (fixed('Statement (d)', 2, '(d) True · 2m'),), '0-1', RW),
    ('(ii)', 2, L(6, '(ii) Is basalt an igneous, sedimentary or metamorphic rock?'),
     S(6, 'Q.6 (ii)', None), (fixed('Rock type', 2, 'Q.6 (ii) · Igneous rock · 2m'),), '0-1', RW),
])
PART_ONE += romans('7', P1, 7, L(7, 'Weather Charts'), (), ID + 'p1-q7', ('page',), [
    ('(i)', 8, L(7, '(i) Match each of the weather chart symbols with the feature of weather that best',
                 'in the table below.'),
     S(7, 'Q.7 (i)', 'Q.7 (ii)'), rows(['Q.7 (i) · C · 2m', '=D · 2m', '=B · 2m', '=A · 2m']), '2-7', WEATHER,
     (L(7, 'High Pressure System'), L(7, 'Cold Front'), L(7, 'Low Pressure System'), L(7, 'Warm Front'))),
    ('(ii)', 2, (L(7, '(ii) Indicate whether the following statement is true or false, by circling the correct',
                   'option.'),
                 L(7, 'Isotherms are lines that join places of equal temperature on a weather chart.')),
     S(7, 'Q.7 (ii)', 'Q.8'), (fixed('True or false', 2, 'Q.7 (ii) · True · 2m · Total 10m'),), '2-7', WEATHER),
])
PART_ONE.append(T(
    'p1-8', P1, '8', '', 10, 7, L(7, 'Weathering and Erosion'),
    (L(7, 'Match the explanation of the process with the name of the process most associated',
       'in the table below.'),),
    (S(7, 'Q.8', 'Q.9'),),
    rows(['Q.8 · E · 2m', '=D · 2m', '=A · 2m', '=C · 2m', '=B · 2m · Total 10m']),
    '0-4', RW + RIVERS + SEA + GLAC, ID + 'p1-q8', ('page',),
    row_labels=(L(7, 'Onion weathering'), L(7, 'Hydraulic action'), L(7, 'Freeze-thaw action'),
                L(7, 'Longshore drift'), L(7, 'Plucking'))))
PART_ONE += romans('9', P1, 8, L(8, 'Economic Activities', nth=0),
                   (L(8, 'Examine the chart above and answer each of the following questions.'),),
                   ID + 'p1-q9', ('page',), [
    ('(i)', 2, L(8, '(i) Which country has the highest percentage of primary economic activities?'),
     S(7, 'Q.9', '(ii) 47%'), (fixed('Country', 2, 'Q.9 · (i) Nepal · 2m'),), '2-0', GRAPH),
    ('(ii)', 2, L(8, '(ii) Calculate the total percentage of primary and secondary economic activities',
                  'in Brazil.'),
     S(7, '(ii) 47%', '(iii) Ireland'), (fixed('Percentage', 2, '(ii) 47% · 2m'),), '2-0', GRAPH),
    ('(iii)', 2, L(8, '(iii) Which of the three countries, Ireland, Brazil or Nepal, has the most developed',
                   'economy?'),
     S(7, '(iii) Ireland', '(iv) Tertiary'), (fixed('Country', 2, '(iii) Ireland · 2m'),), '3-0', ECON + GRAPH),
    ('(iv)', 4, L(8, '(iv) State whether each of the following is an example of a primary, secondary or',
                  'economic activity.'),
     S(7, '(iv) Tertiary', 'Q.10'), rows(['(iv) Tertiary · 2m', 'Primary · 2m · Total 10m']), '3-0', ECON,
     (L(8, 'Teaching'), L(8, 'Fishing'))),
])
PART_ONE.append(T(
    'p1-10', P1, '10', '', 10, 9, L(9, 'Satellite Image Interpretation'),
    (L(9, 'Match each satellite image with the most suitable description', 'One has been completed for you.'),),
    (S(7, 'Q.10', 'Q.11'),),
    rows(['Q.10 · C · 2m', '=E · 2m', '=B · 2m', '=A · 2m', '=F · 2m · Total 10m']),
    '2-8', AER, ID + 'p1-q10', ('page',),
    row_labels=(L(9, 'Solar power plant in the desert'), L(9, 'Before and after Japan tsunami 2011'),
                L(9, 'Copacabana Beach, Rio de Janeiro'), L(9, 'Atlantic storm'), L(9, 'Retreating glacier'))))
PART_ONE += romans('11', P1, 10, L(10, 'Weather Statistics'),
                   (L(10, 'Examine the table above and answer each of the following questions.'),),
                   ID + 'p1-q11', ('page',), [
    ('(i)', 2, L(10, '(i) What was the highest mean monthly temperature (oC) at Shannon airport in 2014?'),
     S(7, 'Q.11', '(ii) 7'), (fixed('Temperature', 2, 'Q.11 · (i) 17.1 (°C) · 2m'),), '2-0', GRAPH + WEATHER),
    ('(ii)', 2, L(10, '(ii) In how many months were the mean temperatures greater than 10°C?'),
     S(7, '(ii) 7', '(iii) 11.0'), (fixed('Months', 2, '(ii) 7 · 2m'),), '2-0', GRAPH + WEATHER),
    ('(iii)', 2, L(10, '(iii) What was the annual mean temperature (oC) at Shannon airport in 2014?'),
     S(7, '(iii) 11.0', '(iv) Feb'), (fixed('Temperature', 2, '(iii) 11.0 (°C)/10.98(°C) · 2m'),),
     '2-0', GRAPH + WEATHER),
    ('(iv)', 2, L(10, '(iv) In which month was the highest level of rainfall?'),
     S(7, '(iv) Feb', '(v) 167'), (fixed('Month', 2, '(iv) Feb · 2m'),), '2-0', GRAPH + WEATHER),
    ('(v)', 2, L(10, '(v) What was the total rainfall (mm) for June, July and August combined?'),
     S(7, '(v) 167', 'Q.12'), (fixed('Total rainfall', 2, '(v) 167 (mm) · 2m · Total 10m'),),
     '2-0', GRAPH + WEATHER),
])
PART_ONE.append(T(
    'p1-12', P1, '12', '', 10, 11, L(11, 'Regions'),
    (L(11, 'Match the description of a region with the example of the region most associated',
       'in the table below.'),),
    (S(7, 'Q.12', None),),
    rows(['Q.12 · B · 2m', '=D · 2m', '=E · 2m', '=C · 2m', '=A · 2m · Total 10m']),
    '1-0', IRL + EURO, ID + 'p1-q12', ('page',),
    row_labels=(L(11, 'The Gaeltacht'), L(11, 'Mezzogiorno, Southern Italy'), L(11, 'Islamic World'),
                L(11, 'Greater Dublin Area'), L(11, 'Cool Temperate Oceanic'))))


# ---------------------------------------------------------------- Part Two --
def sketch(page, title, prompt, scheme_page, card_id, topic, atlas, sources, heading, labels):
    """Five sketch items @ 5 (shown 3 graded 3/1/0, labelled 2) and a 5-mark outline."""
    item = sums((0, 1, 3), (0, 2))
    return T(f'p2-{card_id.rsplit("-q", 1)[1]}', P2, card_id.rsplit('-q', 1)[1].upper(), '', 30, page,
             title, (prompt,), (S(scheme_page, heading, 'Total 30m'),),
             (fixed('Limits/frame', 1, (heading, 'imits/')),
              fixed('Proportions (landscape)', 2, 'Proportions (landscape) · 2m'),
              fixed('Overall impression', 2, '2m graded (2/1/0)', (0, 1, 2)),
              *(Criterion(f'Item {n}', 5, item, 'exact',
                          ('Five items shown and', 'Showing · 3m graded (3/1/0)', 'Labelled · 2m'))
                for n in range(1, 6))),
             topic, atlas, card_id, sources,
             row_labels=(None, None, None, *(L(page, b) for b in labels)))


def two_of(label, count, head, each, lines, unit):
    per = sums(*unit)
    return tuple(Criterion(f'{label} {n}', count, per, 'srp', (head, each, *lines)) for n in (1, 2))


SHOWN = 'Shown · 4m graded (4/2/0)'
NAMED_SHOWN = sums((0, 2), (0, 2, 4))
GRAPH_OL = (fixed('Graph paper', 3, 'Graph paper · 3m', (0, 3)),
            fixed('Vertical axis labelled / circle', 3, 'Vertical axis labelled/Circle · 3m graded (3/1/0)', (0, 1, 3)),
            fixed('Horizontal axis labelled / centred', 3, 'Horizontal axis labelled/Centred · 3m graded (3/1/0)',
                  (0, 1, 3)),
            fixed('5 items illustrated', 15, '5 items @ 3m each graded (3/1/0) · 15m', sums(*[(0, 1, 3)] * 5)))
CONTROLS = 'river processes or coastal processes or mass movement processes'
ROCK = ('Quarrying', 'Mining', 'Oil/Gas exploitation', 'Geothermal energy production.')

Q1AS = (L(14, 'Examine the map above and answer each of the following questions.'),)
PART_TWO = romans('1A', P2, 14, L(14, 'Plate Tectonics'), Q1AS, ID + 'p2-q1a', ('page',), [
    ('(i)', 3, L(14, '(i) What is the name given to the area marked A where a large number of earthquakes',
                 'volcanic eruptions occur?'),
     S(10, 'Pacific Ring of Fire', '(ii) · Name X'), (fixed('Name', 3, 'Pacific Ring of Fire · 3m'),), '0-0', PS + EV),
    ('(ii)', 3, L(14, '(ii) Name X, the plate on which Ireland lies.'),
     S(10, 'Eurasian plate', '(iii) · Explain'), (fixed('Plate', 3, 'Eurasian plate · 3m'),), '0-0', PS),
    ('(iii)', 6, L(14, '(iii) Explain briefly what is meant by the term plate.'),
     S(10, 'Brief Explanation 2 SRP', '(iv) · Are the plates', None, '(iii) · Explain'),
     (srp3('Brief explanation', 2, 'Brief Explanation 2 SRP’s @ 3m each · 6m'),), '0-0', PS),
    ('(iv)', 3, L(14, '(iv) Are the plates colliding or separating at Y?'),
     S(10, 'Colliding', '(v) · Name the ocean'), (fixed('Colliding or separating', 3, 'Colliding · 3m'),), '0-0', PS),
    ('(v)', 3, L(14, '(v) Name the ocean ridge running north from B along the plate boundary.'),
     S(10, 'Mid-Atlantic Ridge', '(vi) · Explain'),
     (fixed('Ocean ridge', 3, 'Mid-Atlantic Ridge / North Atlantic Ridge · 3m'),), '0-0', PS),
    ('(vi)', 6, L(14, '(vi) Explain briefly how this ocean ridge was formed.'),
     S(10, 'Brief Explanation 2 SRP', '(vii) · Name two', None, '(vi) · Explain'),
     (srp3('Brief explanation', 2, 'Brief Explanation 2 SRP’s @ 3m each · 6m'),), '0-0', PS),
    ('(vii)', 6, L(14, '(vii) Name two other landforms resulting from plates moving.'),
     S(10, '2 landforms named', 'Total 30m'),
     (fixed('Two landforms', 6, '2 landforms named @ 3m each · 6m', (0, 3, 6)),), '0-0', PS + EV),
])
PART_TWO += [
    T('p2-1b', P2, '1B', '', 40, 14, L(14, 'Landform Development'),
      (L(14, '(i) Explain, with the aid of diagrams, the formation of any two landforms.'),),
      (S(11, 'Formation of any two landforms @ 20m each.', 'Total 40m'),),
      two_of('Landform', 20, 'Formation of any two landforms @ 20m each.', 'For each landform:',
             ('Landform named · 1m', 'Diagram(s) two aspects @ 2m each · 4m',
              'Formation explained 5 SRP’s @ 3m each · 15m'),
             ((0, 1), (0, 2, 4), steps(15, 3))),
      '0-4', PS_SURFACE, ID + 'p2-q1b-route-i',
      routes=(
          Route('route-i', 'Route (i)', ID + 'p2-q1b-route-i', False),
          Route('route-ii', 'Route (ii)', ID + 'p2-q1b-route-ii', False,
                prompt=(L(14, '(ii) Describe and explain any two processes of mass movement.'),),
                scheme=(S(11, 'Any two processes @ 20m each', 'Total 40m'),),
                criteria=two_of('Process', 20, 'Any two processes @ 20m each', 'For each process:',
                                ('Process stated · 2m', 'Description / Explanation 6 SRP’s @ 3m each · 18m'),
                                ((0, 2), steps(18, 3))),
                topic='0-8', atlas=RW),
      )),
    T('p2-1c', P2, '1C', '', 30, 14, L(14, 'Human Interaction with Surface Processes'),
      (L(14, 'Describe and explain how humans attempt to control either river processes or coastal',
         'mass movement processes.'),),
      (S(12, 'Control named', 'Total 30m'),),
      (fixed('Control named', 3, 'Control named · 3m'),
       srp3('Description/explanation', 9, 'Description / explanation 9 SRP’s @ 3m each · 27m')),
      '0-6', RIVERS, ID + 'p2-q1c-river-processes',
      routes=(Route('river-processes', 'river processes', ID + 'p2-q1c-river-processes', False,
                    ((CONTROLS, 'river processes'),), atlas=RIVERS),
              Route('coastal-processes', 'coastal processes', ID + 'p2-q1c-coastal-processes', False,
                    ((CONTROLS, 'coastal processes'),), atlas=SEA),
              Route('mass-movement-processes', 'mass movement processes', ID + 'p2-q1c-mass-movement-processes',
                    False, ((CONTROLS, 'mass movement processes'),), atlas=RW))),
    sketch(15, L(15, 'Ordnance Survey Map'),
           L(15, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper.',
             'An area of Coniferous Plantation.'),
           13, ID + 'p2-q2a', '2-6', MAP + SEA + RIVERS, ('map', 'legend'), 'Sketch Outline:',
           ('Westport Bay', 'The Owenwee River', 'Two named lakes', 'Two named lakes',
            'An area of Coniferous Plantation.')),
]
PART_TWO += romans('2B', P2, 15, L(15, 'Rocks'), (), ID + 'p2-q2b', (), [
    ('(i)', 5, L(15, '(i) Name one example of an igneous rock and name an Irish location where it can be',
                 'found.'),
     S(14, 'Igneous rock named', '(ii) · Describe how igneous'),
     (fixed('Igneous rock named', 3, 'Igneous rock named · 3m'), fixed('Irish location named', 2,
                                                                         'Irish location named · 2m')),
     '0-1', RW + IRL),
    ('(ii)', 15, L(15, '(ii) Describe how igneous rocks are formed.'),
     S(14, 'Formation described 5 SRP', '(iii) · Name one example', None, '(ii) · Describe how igneous'),
     (srp3('Formation described', 5, 'Formation described 5 SRP’s @ 3m each · 15m'),), '0-1', RW),
    ('(iii)', 5, L(15, '(iii) Name one example of a metamorphic rock and name an Irish location where it',
                   'can be found.'),
     S(14, 'Metamorphic rock named', '(iv) · Describe how'),
     (fixed('Metamorphic rock named', 3, 'Metamorphic rock named · 3m'),
      fixed('Irish location named', 2, 'Irish location named · 2m')), '0-1', RW + IRL),
    ('(iv)', 15, L(15, '(iv) Describe how metamorphic rocks are formed.'),
     S(14, 'Formation described 5 SRP', 'Total 40m', None, '(iv) · Describe how'),
     (srp3('Formation described', 5, 'Formation described 5 SRP’s @ 3m each · 15m'),), '0-1', RW),
])
PART_TWO += romans('2C', P2, 15, L(15, 'Weathering'), (), ID + 'p2-q2c', ('page',), [
    ('(i)', 6, L(15, '(i) In your answer book, match each of the photographs A and B with the weathering',
                 'Freeze-thaw action.'),
     S(15, 'Carbonation · B', '(ii) · With the aid'),
     (fixed('Carbonation', 3, 'Carbonation · B · 3m'), fixed('Freeze-thaw action', 3, 'Freeze-thaw action · A · 3m')),
     '0-8', RW, (L(15, 'Carbonation'), L(15, 'Freeze-thaw action'))),
    ('(ii)', 24, L(15, '(ii) With the aid of a diagram(s), explain how rocks are weathered by freeze-thaw',
                   'action.'),
     S(15, 'Explanation 6 SRP', 'Total 30m'),
     (srp3('Explanation', 6, 'Explanation 6 SRP’s @ 3m each · 18m'),
      srp3('Diagram(s)', 2, 'Diagram(s) 2 SRP’s @ 3m each · 6m')), '0-8', RW),
])
Q3AS = (L(16, 'Read the newspaper extract above and answer each of the following questions.'),)
PART_TWO += romans('3A', P2, 16, L(16, 'Earthquakes'), Q3AS, ID + 'p2-q3a', ('page',), [
    ('(i)', 3, L(16, '(i) What was the magnitude of the earthquake in Nepal?'),
     S(16, '7.9 · 3m', '(ii) · At what'), (fixed('Magnitude', 3, '7.9 · 3m'),), '0-7', EV),
    ('(ii)', 3, L(16, '(ii) At what depth (in kilometres) did the earthquake occur?'),
     S(16, '15 (km', '(iii) · State'), (fixed('Depth', 3, '15 (km ) · 3m'),), '0-7', EV),
    ('(iii)', 3, L(16, '(iii) State what is meant by the term aftershock.'),
     S(16, 'Any valid statement', '(iv) · List three'), (fixed('Statement', 3, 'Any valid statement · 3m'),),
     '0-7', EV),
    ('(iv)', 9, L(16, '(iv) List three effects of earthquakes referred to in the newspaper extract above.'),
     S(16, 'Any three effects', '(v) · State two'),
     (fixed('Three effects', 9, 'Any three effects @ 3m each · 9m', (0, 3, 6, 9)),), '0-7', EV),
    ('(v)', 6, L(16, '(v) State two ways that the effects of earthquakes could be reduced.'),
     S(16, 'Two ways stated', '(vi) · Explain'),
     (fixed('Two ways', 6, 'Two ways stated @ 3m each · 6m', (0, 3, 6)),), '0-7', EV),
    ('(vi)', 6, L(16, '(vi) Explain briefly the term epicentre.'),
     S(16, 'Brief explanation 2 SRP', 'Total 30m'), (srp3('Brief explanation', 2, BRIEF),), '0-7', EV),
])
PART_TWO.append(T(
    'p2-3b', P2, '3B', '', 30, 16, L(16, 'Human Interaction with the Rock Cycle'),
    (L(16, 'Explain how humans interact with the rock cycle with reference to one of the following:',
       'Geothermal energy production.'),),
    (S(16, 'Explanation 10 SRP', 'Total 30m'),),
    (srp3('Explanation', 10, 'Explanation 10 SRP’s @ 3m each · 30m'),),
    '0-6', RW, ID + 'p2-q3b-quarrying', routes=bullet_routes('p2-q3b-', ROCK)))
Q3CS = (L(17, 'Examine the photographs of karst landscape features above and answer each of the',
          'following questions.'),)
KARST_CRITERIA = (fixed('Karst feature named', 1, 'Karst feature named · 1m'),
                  fixed('Diagram(s)', 4, 'Diagram(s) two aspects @ 2m each · 4m', (0, 2, 4)),
                  srp3('Formation explained', 5, 'Formation explained 5 SRP’s @ 3m each · 15m'))
PART_TWO += romans('3C', P2, 17, L(17, 'Karst Landscape'), Q3CS, ID + 'p2-q3c', ('page',), [
    ('(i)', 20, L(17, '(i) Name one surface karst feature evident in photograph A and explain',
                  'how this surface feature was formed.'),
     S(17, 'Karst feature named', '(ii) · Name one underground', None, '(i) · Name one surface'),
     KARST_CRITERIA, '0-3', KARST),
    ('(ii)', 20, L(17, '(ii) Name one underground karst feature evident in photograph B and explain',
                   'how this underground feature was formed.'),
     S(17, 'Karst feature named', 'Total 40m', None, '(ii) · Name one underground'), KARST_CRITERIA, '0-3', KARST),
])

PART_TWO.append(T(
    'p2-4a', P2, '4A', '', 30, 18, L(18, 'Continental / Sub-Continental Region'),
    (L(18, 'Draw a sketch map of a Continental / Sub-Continental region (not in Europe) that you',
       '(upland or lowland) in this region.'),),
    (S(18, 'Outline of Region', 'Total 30m'),),
    (fixed('Outline of region', 6, 'Outline of Region · 6m graded (6/4/2/0)', (0, 2, 4, 6)),
     Criterion('Town/City 1', 6, NAMED_SHOWN, 'exact', ('Town/City 1 · Named · 2m', f'={SHOWN}@0')),
     Criterion('Town/City 2', 6, NAMED_SHOWN, 'exact', ('Town/City 2 · Named · 2m', f'={SHOWN}@1')),
     Criterion('Named river', 6, NAMED_SHOWN, 'exact', ('Named River · Named · 2m', f'={SHOWN}@2')),
     Criterion('Relief (upland/lowland)', 6, NAMED_SHOWN, 'exact',
               ('Relief Upland/Lowland · Named · 2m', f'={SHOWN}@3'))),
    '1-6', CONT, ID + 'p2-q4a'))
FACTORS_4B = ('Relief and soils', 'Markets', 'Climate.')
PART_TWO += [
    T('p2-4b-i', P2, '4B', '(i)', 4, 18, L(18, 'Agriculture in Ireland'),
      (L(18, '(i) Name two types of farming in Ireland.'),),
      (S(19, 'Two types of farming named', '(ii) · Explain how'),),
      (fixed('Two types of farming', 4, 'Two types of farming named @ 2m each · 4m', (0, 2, 4)),),
      '1-4', IRL, ID + 'p2-q4b'),
    T('p2-4b-ii', P2, '4B', '(ii)', 36, 18, L(18, 'Agriculture in Ireland'),
      (L(18, '(ii) Explain how any two of the following factors influence the development of', 'Climate.'),),
      (S(19, 'Explanation Factor 1', 'Total 40m'),),
      (srp3('Factor 1', 6, 'Explanation Factor 1 6 SRP’s @ 3m each · 18m'),
       srp3('Factor 2', 6, 'Explanation Factor 2 6 SRP’s @ 3m each · 18m')),
      '1-4', IRL, ID + 'p2-q4b-ii', absorbs=pool(ID + 'p2-q4b-ii-', FACTORS_4B, 2)[1]),
    T('p2-4c', P2, '4C', '', 30, 18, L(18, 'Regions and Culture'),
      (L(18, 'The culture of a region can often be determined by the following factors:', 'Sport/Games.'),
       L(18, 'Describe and explain the importance of culture in any region that you have studied.')),
      (S(19, 'Description / Explanation 10', 'Total 30m'),),
      (srp3('Description/explanation', 10, 'Description / Explanation 10 SRP’s @ 3m each · 30m'),),
      '1-0', IRL + EURO, ID + 'p2-q4c'),
]

Q5AS = (L(19, 'Examine the map above showing the Eurozone area in 2015 and answer each of the',
          'following questions.'),)
PART_TWO += romans('5A', P2, 19, L(19, 'European Union', nth=0), Q5AS, ID + 'p2-q5a', ('page',), [
    ('(i)', 6, L(19, '(i) In what year did Ireland join the Eurozone area and how many countries',
                 'joined that year?'),
     S(20, '1999 · 3m', '(ii) · Name two'),
     (fixed('Year', 3, '1999 · 3m'), fixed('Number of countries', 3, '11 countries · 3m')), '3-3', EU + EURO),
    ('(ii)', 6, L(19, '(ii) Name two European Union (EU) member states not in the Eurozone area in 2015.'),
     S(20, 'Two EU member states', '(iii) · Calculate'),
     (fixed('Two member states', 6, 'Two EU member states named @ 3m each · 6m', (0, 3, 6)),), '3-3', EU + EURO),
    ('(iii)', 6, L(19, '(iii) Calculate the total number of European Union member states in the Eurozone',
                   'area in 2015.'),
     S(20, '19 · 6m', '(iv) · Explain'), (fixed('Total', 6, '19 · 6m'),), '3-3', EU + EURO),
    ('(iv)', 12, L(19, '(iv) Explain briefly two advantages of being part of the Eurozone area.'),
     S(20, 'Advantage 1 explained', 'Total 30m'),
     (srp3('Advantage 1', 2, 'Advantage 1 explained 2 SRP’s @ 3m each · 6m'),
      srp3('Advantage 2', 2, 'Advantage 2 explained 2 SRP’s @ 3m each · 6m')), '3-3', EU + EURO),
])
ACTIVITIES_5B = ('The role of tourism in the economy of this region',
                 'The reasons for the development of industry in this region',
                 'The problems facing agriculture in this region.')
PART_TWO += [
    T('p2-5b', P2, '5B', '', 40, 19, L(19, 'Economic Activity in an Irish Region'),
      (L(19, 'Explain any two of the following with reference to an Irish region that you have studied:',
         'The problems facing agriculture in this region.'),),
      (S(20, 'Activity 1 explained', 'Total 40m'),),
      (srp3('Activity 1 explained', 7, 'Activity 1 explained 7 SRP’s @ 3m each · 21m'),
       srp3('Activity 2 explained', 6, 'Activity 2 explained 6 SRP’s @ 3m each · 18m'),
       fixed('Region named', 1, 'Naming the region · 1m')),
      '1-4', IRL, ID + 'p2-q5b', absorbs=pool(ID + 'p2-q5b-', ACTIVITIES_5B, 2)[1]),
    T('p2-5c', P2, '5C', '', 30, 19, L(19, 'Urban Growth'),
      (L(19, 'Explain the reasons for the growth of any urban area that you have studied.'),),
      (S(20, 'Explanation 10 SRP', 'Total 30m'),),
      (srp3('Explanation', 10, 'Explanation 10 SRP’s @ 3m each · 30m'),),
      '1-1', IRL + EURO + URB, ID + 'p2-q5c'),
]

Q6AS = (L(20, 'Examine the chart above showing information regarding popular Irish tourist attractions',
          'following questions.'),)
PART_TWO += romans('6A', P2, 20, L(20, 'Tourism in Ireland'), Q6AS, ID + 'p2-q6a', ('page',), [
    ('(i)', 6, L(20, '(i) Name the two most popular Irish tourist attractions in 2013.'),
     S(21, 'Guinness Storehouse', '(ii) · Name the tourist'),
     (fixed('Attraction 1', 3, 'Guinness Storehouse · 3m'), fixed('Attraction 2', 3, 'Dublin Zoo · 3m')),
     '2-0', GRAPH),
    ('(ii)', 6, L(20, '(ii) Name the tourist attraction with the least number of visitors', 'visitors it received.'),
     S(21, 'Fota Wildlife Park', '(iii) · Calculate'),
     (fixed('Attraction', 3, 'Fota Wildlife Park · 3m'), fixed('Visitors', 3, '365,396 · 3m')), '2-0', GRAPH),
    ('(iii)', 6, L(20, '(iii) Calculate the difference between the number of tourists that visited the National',
                   'Tayto Park in 2013.'),
     S(21, '115,000', '(iv) · Explain'), (fixed('Difference', 6, '115,000 · 6m'),), '2-0', GRAPH),
    ('(iv)', 6, L(20, '(iv) Explain briefly one positive effect of tourism on Ireland.'),
     S(21, 'Brief explanation 2 SRP', '(v) · Explain', None, '(iv) · Explain'),
     (srp3('Brief explanation', 2, BRIEF),), '1-4', IRL),
    ('(v)', 6, L(20, '(v) Explain briefly one negative effect of tourism on Ireland.'),
     S(21, 'Brief explanation 2 SRP', 'Total 30m', None, '(v) · Explain'),
     (srp3('Brief explanation', 2, BRIEF),), '1-4', IRL),
])
PART_TWO.append(T(
    'p2-6b', P2, '6B', '', 30, 20, L(20, 'Manufacturing in a Continental / Sub-Continental Region'),
    (L(20, 'Describe and explain the development of manufacturing in a Continental /', 'that you have studied.'),),
    (S(21, 'Description / Explanation 10', 'Total 30m'),),
    (srp3('Description/explanation', 10, 'Description / Explanation 10 SRP’s @ 3m each · 30m'),),
    '1-6', CONT, ID + 'p2-q6b'))
Q6CS = (L(21, 'Answer each of the following questions with reference to a European region',
          'that you have studied.'),)
Q6CI = L(21, '(i) Name one primary economic activity that contributes to the economy of this', 'region.')
PART_TWO += romans('6C', P2, 21, L(21, 'Primary Economic Activity in a European Region'), Q6CS, ID + 'p2-q6c', (), [
    ('(i)', 4, Q6CI, S(22, 'Primary economic activity named', '(ii) · Explain the advantages'),
     (fixed('Primary economic activity named', 4, 'Primary economic activity named · 4m'),), '1-5', EURO),
    ('(ii)', 27, L(21, '(ii) Explain the advantages that this region has for the development of the primary',
                   'part (i) above.'),
     S(22, 'Explanation 9 SRP', '(iii) · Describe'),
     (srp3('Explanation', 9, 'Explanation 9 SRP’s @ 3m each · 27m'),), '1-5', EURO, (), (Q6CI,)),
    ('(iii)', 9, L(21, '(iii) Describe one challenge faced by this primary economic activity in this region.'),
     S(22, 'Description 3 SRP', 'Total 40m'),
     (srp3('Description', 3, 'Description 3 SRP’s @ 3m each · 9m'),), '1-5', EURO, (), (Q6CI,)),
])

PART_TWO.append(sketch(
    23, L(23, 'Aerial Photograph'),
    L(23, 'Examine the aerial photograph of Westport accompanying this paper.', 'in the background.'),
    24, ID + 'p2-q7a', '2-8', AER + ECON, ('aerial',), 'Sketch Outline:',
    ('A bridge', 'Two connecting streets', 'A car park in the foreground',
     'An industrial area in the left middleground', 'An area of waste ground in the background.')))
PART_TWO += romans('7B', P2, 23, L(23, 'Environmental Impact - Fossil Fuels'), (), ID + 'p2-q7b', (), [
    ('(i)', 6, L(23, '(i) Name two examples of fossil fuels.'),
     S(25, 'Two examples named', '(ii) · Describe'),
     (fixed('Two fossil fuels', 6, 'Two examples named @ 3m each · 6m', (0, 3, 6)),), '3-5', ECON),
    ('(ii)', 24, L(23, '(ii) Describe and explain the impact of burning fossil fuels on the environment.'),
     S(25, 'Description / explanation 8', 'Total 30m'),
     (srp3('Description/explanation', 8, 'Description / explanation 8 SRP’s @ 3m each · 24m'),), '3-4', ENV),
])
Q7CI = L(23, '(i) Name one multinational company located in Ireland that you have studied and',
         'manufactures.')
PART_TWO += romans('7C', P2, 23, L(23, 'Multinational Company (MNC)'), (), ID + 'p2-q7c', (), [
    ('(i)', 4, Q7CI, S(25, 'MNC named', '(ii) · State where'),
     (fixed('MNC named', 2, 'MNC named · 2m'), fixed('Product named', 2, 'Product named · 2m')), '3-2', MNC),
    ('(ii)', 24, L(23, '(ii) State where this multinational company is located in Ireland and explain why',
                   'at this location.'),
     S(25, 'Location · 3m', '(iii) · Explain one'),
     (fixed('Location', 3, 'Location · 3m'), srp3('Explanation', 7, 'Explanation 7 SRP’s @ 3m each · 21m')),
     '3-2', MNC, (), (Q7CI,)),
    ('(iii)', 12, L(23, '(iii) Explain one reason why this multinational company might decide to locate',
                    'another country.'),
     S(25, 'Explanation 4 SRP', 'Total 40m'),
     (srp3('Explanation', 4, 'Explanation 4 SRP’s @ 3m each · 12m'),), '3-2', MNC, (), (Q7CI,)),
])

PART_TWO += romans('8A', P2, 24, L(24, 'Economic Development'),
                   (L(24, 'Examine the information above and answer each of the following questions.'),),
                   ID + 'p2-q8a', ('page',), [
    ('(i)', 6, L(24, '(i) Name two countries with a high Human Development Index.'),
     S(26, 'Two countries named', '(ii) · Which continent'),
     (fixed('Two countries', 6, 'Two countries named @ 3m each · 6m', (0, 3, 6)),), '2-0', GRAPH),
    ('(ii)', 6, L(24, '(ii) Which continent has the greatest number of countries with a low Human',
                  'state one reason for this.'),
     S(26, 'Africa · 3m', '(iii) · Name any two'),
     (fixed('Continent', 3, 'Africa · 3m'), fixed('Reason', 3, 'Reason stated · 3m')), '3-1', DEV + GRAPH),
    ('(iii)', 6, L(24, '(iii) Name any two factors used to calculate the Human Development Index.'),
     S(26, 'Two factors named', '(iv) · Explain'),
     (fixed('Two factors', 6, 'Two factors named @ 3m each · 6m', (0, 3, 6)),), '3-0', ECON),
    ('(iv)', 6, L(24, '(iv) Explain briefly one reason why the Human Development Index for some',
                  'higher than others.'),
     S(26, 'Brief explanation 2 SRP', '(v) · Explain', None, '(iv) · Explain briefly'),
     (srp3('Brief explanation', 2, BRIEF),), '3-0', ECON),
    ('(v)', 6, L(24, '(v) Explain briefly one way that Human Development Index information is used.'),
     S(26, 'Brief explanation 2 SRP', 'Total 30m', None, '(v) · Explain'),
     (srp3('Brief explanation', 2, BRIEF),), '3-0', ECON),
])
SECTOR = 'tourism or financial services'


def sector_routes(card_id):
    return (Route('tourism', 'tourism', card_id + '-tourism', False, ((SECTOR, 'tourism'),)),
            Route('financial-services', 'financial services', card_id + '-financial-services', False,
                  ((SECTOR, 'financial services'),)))


Q8BI = L(24, '(i) Name one developed economy where tourism or financial services contribute to', 'that economy.')
PART_TWO += [
    T('p2-8b-i', P2, '8B', '(i)', 4, 24, L(24, 'Developed Economy'), (Q8BI,),
      (S(26, 'Developed economy named', '(ii) · Explain the reasons'),),
      (fixed('Developed economy named', 4, 'Developed economy named · 4m'),),
      '3-0', ECON, ID + 'p2-q8b-tourism', routes=sector_routes(ID + 'p2-q8b')),
    T('p2-8b-ii', P2, '8B', '(ii)', 18, 24, L(24, 'Developed Economy'),
      (L(24, '(ii) Explain the reasons for the growth of tourism or financial services in the',
         'part (i) above.'),),
      (S(26, '6 SRP’s @ 3m each · 18m', '(iii) · Explain one benefit'),),
      (srp3('Explanation', 6, '6 SRP’s @ 3m each · 18m'),),
      '3-0', ECON, ID + 'p2-q8b-ii-tourism', stem=(Q8BI,), routes=sector_routes(ID + 'p2-q8b-ii')),
    T('p2-8b-iii', P2, '8B', '(iii)', 9, 24, L(24, 'Developed Economy'),
      (L(24, '(iii) Explain one benefit that tourism or financial services bring to the economy of',
         'developed countries.'),),
      (S(26, '3 SRP’s @ 3m each · 9m', '(iv) · Explain one problem', None, '(iii) · Explain one benefit'),),
      (srp3('Explanation', 3, '3 SRP’s @ 3m each · 9m'),),
      '3-0', ECON, ID + 'p2-q8b-iii-tourism', routes=sector_routes(ID + 'p2-q8b-iii')),
    T('p2-8b-iv', P2, '8B', '(iv)', 9, 24, L(24, 'Developed Economy'),
      (L(24, '(iv) Explain one problem caused by tourism or financial services.'),),
      (S(26, '3 SRP’s @ 3m each · 9m', 'Total 40m', None, '(iv) · Explain one problem'),),
      (srp3('Explanation', 3, '3 SRP’s @ 3m each · 9m'),),
      '3-0', ECON, ID + 'p2-q8b-iv-tourism', routes=sector_routes(ID + 'p2-q8b-iv')),
]
Q8CI = L(24, '(i) Name one example of how the development of economic activities and the',
         'conflict arising between people.')
PART_TWO += romans('8C', P2, 24, L(24, 'Economic Activity and Conflict'), (), ID + 'p2-q8c', (), [
    ('(i)', 3, Q8CI, S(27, 'Example named', '(ii) · Describe'),
     (fixed('Example named', 3, 'Example named · 3m'),), '3-4', ENV),
    ('(ii)', 27, L(24, '(ii) Describe and explain this conflict.'),
     S(27, 'Description / Explanation 9', 'Total 30m'),
     (srp3('Description/explanation', 9, 'Description / Explanation 9 SRP’s @ 3m each · 27m'),), '3-4', ENV,
     (), (Q8CI,)),
])

PART_TWO += romans('9A', P2, 25, L(25, 'Energy Consumption', nth=0),
                   (L(25, 'Examine the table above showing estimated global energy consumption by 2030',
                      'following questions.'),),
                   ID + 'p2-q9a', ('page',), [
    ('(i)', 24, L(25, '(i) Using graph paper, draw a suitable graph to illustrate this data.'),
     S(28, 'Graph paper', '(ii) · In your answer book'), GRAPH_OL, '2-0', GRAPH),
    ('(ii)', 6, L(25, '(ii) In your answer book, explain briefly what is meant by the term renewable energy.'),
     S(28, '2 SRP’s @ 3m each · 6m', 'Total 30m'),
     (srp3('Brief explanation', 2, '2 SRP’s @ 3m each · 6m'),), '3-5', ECON),
])
Q9CS = (L(25, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper.'),
        L(25, 'Imagine you have been given the task of finding a suitable location for a new large hotel',
          'within the area covered by the map.'))
Q9CI = L(25, '(i) State, using a six-figure grid reference, where you would locate the hotel.')
PART_TWO += [
    T('p2-9b', P2, '9B', '', 30, 25, L(25, 'European Union Policy'),
      (L(25, 'Explain how European Union policies have impacted on the Irish economy.'),),
      (S(28, 'Explanation 9 SRP', 'Total 30m'),),
      (fixed('Impact identified', 3, 'Impact identified 1 SRP · 3m'),
       srp3('Explanation', 9, 'Explanation 9 SRP’s @ 3m each · 27m')),
      '3-3', EU, ID + 'p2-q9b'),
]
PART_TWO += romans('9C', P2, 25, L(25, 'Ordnance Survey Map'), Q9CS, ID + 'p2-q9c', ('map', 'legend'), [
    ('(i)', 7, Q9CI, S(29, 'Six-figure grid reference', '(ii) · Explain'),
     (fixed('Six-figure grid reference', 7, 'Six-figure grid reference · 7m graded (7/4/0)', (0, 4, 7)),),
     '2-6', MAP + ECON),
    ('(ii)', 24, L(25, '(ii) Explain the reasons why you chose this location.'),
     S(29, 'Reasons explained 8', '(iii) · Describe'),
     (srp3('Reasons explained', 8, 'Reasons explained 8 SRP’s @ 3m each · 24m'),), '3-0', ECON + MAP, (), (Q9CI,)),
    ('(iii)', 9, L(25, '(iii) Describe one disadvantage of locating the hotel at this location.'),
     S(29, 'One disadvantage described', 'Total 40m'),
     (srp3('One disadvantage described', 3, 'One disadvantage described 3 SRP’s @ 3m each · 9m'),),
     '3-0', ECON + MAP, (), (Q9CI,)),
])

PART_TWO.append(sketch(
    26, L(26, 'Aerial Photograph'),
    L(26, 'Examine the aerial photograph of Westport accompanying this paper.', 'in the centre background.'),
    30, ID + 'p2-q10a', '2-8', AER + URB, ('aerial',), 'Sketch:',
    ('A bridge', 'Two churches', 'Two churches', 'Two connecting streets',
     'A large car park in the centre background.')))
PART_TWO += romans('10B', P2, 26, L(26, 'Migration – Rural to Urban'), (), ID + 'p2-q10b', (), [
    ('(i)', 20, L(26, '(i) Explain the push factors associated with migration from rural to urban areas.'),
     S(31, 'First Push factor', '(ii) · Explain the pull'),
     (fixed('First push factor identified', 3, 'First Push factor identified · 3m'),
      fixed('Second push factor identified', 2, 'Second Push factor identified · 2m'),
      srp3('Explanation', 5, 'Explanation 5 SRP’s @ 3m each · 15m')), '4-2', POP),
    ('(ii)', 20, L(26, '(ii) Explain the pull factors associated with migration from rural to urban areas.'),
     S(31, 'First Pull factor', 'Total 40m'),
     (fixed('First pull factor identified', 3, 'First Pull factor identified · 3m'),
      fixed('Second pull factor identified', 2, 'Second Pull factor identified · 2m'),
      srp3('Explanation', 5, 'Explanation 5 SRP’s @ 3m each · 15m')), '4-2', POP),
])
Q10CI = L(26, '(i) Name one urban area that you have studied and name any two functions of this', 'urban area.')
PART_TWO += romans('10C', P2, 26, L(26, 'Urban Functions'), (), ID + 'p2-q10c', (), [
    ('(i)', 9, Q10CI, S(31, 'Urban area named', '(ii) · Describe and explain how'),
     (fixed('Urban area named', 3, 'Urban area named · 3m'),
      fixed('Two functions named', 6, 'Two functions named 2 SRP’s @ 3m each · 6m', (0, 3, 6))), '4-3', URB),
    ('(ii)', 21, L(26, '(ii) Describe and explain how the functions of this urban area have changed over', 'time.'),
     S(31, 'Reference to change stated', 'Total 30m'),
     (fixed('Reference to change stated', 3, 'Reference to change stated 1 SRP @ 3m · 3m'),
      srp3('Description/explanation', 6, 'Description / explanation 6SRP’s @ 3m each · 18m')), '4-3', URB,
     (), (Q10CI,)),
])

TOWN_REASON = ('Three reasons @ 10m each · 30m', 'For each reason:', 'Aerial photograph evidence · 1m',
               'Explanation 3 SRP’s @ 3m each · 9m')
PART_TWO += romans('11A', P2, 27, L(27, 'Irish Emigration'),
                   (L(27, 'Examine the table above showing information regarding emigration from Ireland by',
                      'following questions.'),),
                   ID + 'p2-q11a', ('page',), [
    ('(i)', 24, L(27, '(i) Using graph paper, draw a suitable graph to illustrate this data.'),
     S(32, 'Graph paper', '(ii) · In your answer book'), GRAPH_OL, '2-0', GRAPH),
    ('(ii)', 6, L(27, '(ii) In your answer book, explain briefly one reason why people are emigrating from',
                  'Ireland.'),
     S(32, 'Brief explanation 2 SRP', 'Total 30m'), (srp3('Brief explanation', 2, BRIEF),), '4-2', POP),
])
PART_TWO.append(T(
    'p2-11b', P2, '11B', '', 30, 27, L(27, 'Development of Urban Settlements'),
    (L(27, 'Examine the aerial photograph of Westport accompanying this paper.'),
     L(27, 'Explain three reasons why the town of Westport developed at this location', 'support each reason.')),
    (S(32, 'Three reasons @ 10m each', 'Total 30m'),),
    tuple(Criterion(f'Reason {n}', 10, sums((0, 1), steps(9, 3)), 'srp', TOWN_REASON) for n in (1, 2, 3)),
    '4-3', URB + AER, ID + 'p2-q11b', ('aerial',)))
Q11CI = L(27, '(i) Name one city in the developing world that has grown rapidly.')
PART_TWO += romans('11C', P2, 27, L(27, 'Urban Growth - Developing World City'), (), ID + 'p2-q11c', (), [
    ('(i)', 4, Q11CI, S(33, 'Developing world city named', '(ii) · Explain why'),
     (fixed('Developing world city named', 4, 'Developing world city named · 4m'),), '4-5', URB),
    ('(ii)', 27, L(27, '(ii) Explain why this city has grown rapidly and describe the problems associated',
                   'rapid growth.'),
     S(33, 'Reason for growth stated', '(iii) · Describe one'),
     (fixed('Reason for growth stated', 3, 'Reason for growth stated 1 SRP @ 3m · 3m'),
      fixed('Problem stated', 3, 'Problem stated 1 SRP @ 3m · 3m'),
      srp3('Description/explanation', 7, 'Description / explanation 7 SRP’s @ 3m each · 21m')), '4-5', URB,
     (), (Q11CI,)),
    ('(iii)', 9, L(27, '(iii) Describe one solution to the problems experienced as a result of this rapid',
                   'growth.'),
     S(33, 'One solution 3 SRP', 'Total 40m'),
     (srp3('One solution', 3, 'One solution 3 SRP’s @ 3m each · 9m'),), '4-5', URB, (), (Q11CI,)),
])

PART_TWO += romans('12A', P2, 28, L(28, 'Urban Growth'),
                   (L(28, 'Read the article above and answer each of the following questions.'),),
                   ID + 'p2-q12a', ('page',), [
    ('(i)', 3, L(28, '(i) What percentage of the world’s urban population is resident in the world’s largest',
                 'cities?'),
     S(34, '51%', '(ii) · Where are'), (fixed('Percentage', 3, '51% · 3m'),), '2-0', GRAPH + URB),
    ('(ii)', 6, L(28, '(ii) Where are the world’s largest cities increasingly concentrated',
                  'located in this area?'),
     S(34, 'Asia · 3m', '(iii) · Name the three'),
     (fixed('Area', 3, 'Asia · 3m'), fixed('Percentage', 3, '56% · 3m')), '2-0', GRAPH + URB),
    ('(iii)', 9, L(28, '(iii) Name the three high income world cities ranked in the top ten',
                   'largest cities.'),
     S(34, 'Tokyo · 3m', '(iv) · Explain'),
     (fixed('City 1', 3, 'Tokyo · 3m'), fixed('City 2', 3, 'Seoul · 3m'), fixed('City 3', 3, 'New York · 3m')),
     '2-0', GRAPH + URB),
    ('(iv)', 6, L(28, '(iv) Explain briefly what is meant by the term population density.'),
     S(34, 'Brief explanation 2 SRP', '(v) · Explain', None, '(iv) · Explain'),
     (srp3('Brief explanation', 2, BRIEF),), '4-0', POP),
    ('(v)', 6, L(28, '(v) Explain briefly one problem experienced in cities with high population densities.'),
     S(34, 'Brief explanation 2 SRP', 'Total 30m', None, '(v) · Explain'),
     (srp3('Brief explanation', 2, BRIEF),), '4-5', URB),
])
PART_TWO += romans('12B', P2, 28, L(28, 'Overpopulation'), (), ID + 'p2-q12b', (), [
    ('(i)', 6, L(28, '(i) Explain briefly what is meant by the term overpopulation.'),
     S(34, 'Brief explanation 2 SRP', '(ii) · Describe and explain the causes', None, 'B. · Overpopulation'),
     (srp3('Brief explanation', 2, BRIEF),), '4-1', POP),
    ('(ii)', 24, L(28, '(ii) Describe and explain the causes and effects of overpopulation with reference',
                   'that you have studied.'),
     S(34, 'One cause stated', 'Total 30m'),
     (fixed('One cause stated', 3, 'One cause stated · 3m'), fixed('One effect stated', 3, 'One effect stated · 3m'),
      fixed('One example stated', 3, 'One example stated · 3m'),
      srp3('Description/explanation', 5, 'Description/Explanation 5 SRP’s @ 3m each · 15m')), '4-1', POP),
])
PATTERN = ('Three rural settlement patterns:', 'Named · 4m + 3m + 3m', 'Located · 4m + 4m + 4m',
           '(4m graded 4/2/0)')
EXPLAIN_PATTERN = ('For each rural settlement pattern:', 'Brief explanation 2 SRP’s @ 3m each · 6m + 6m + 6m')
Q12CS = (L(28, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper.'),)
Q12CI = L(28, '(i) Name three different rural settlement patterns evident on the Ordnance Survey',
          'example of each.')
PART_TWO += romans('12C', P2, 28, L(28, 'Rural Settlement Patterns'), Q12CS, ID + 'p2-q12c', ('map', 'legend'), [
    ('(i)', 22, Q12CI, S(35, 'Three rural settlement patterns:', '(ii) · Explain each'),
     (Criterion('Pattern 1', 8, sums((0, 4), (0, 2, 4)), 'exact', PATTERN),
      Criterion('Pattern 2', 7, sums((0, 3), (0, 2, 4)), 'exact', PATTERN),
      Criterion('Pattern 3', 7, sums((0, 3), (0, 2, 4)), 'exact', PATTERN)), '4-3', URB + MAP),
    ('(ii)', 18, L(28, '(ii) Explain each of the three rural settlement patterns named in part (i) above.'),
     S(35, 'For each rural settlement pattern:', 'Total 40m'),
     tuple(Criterion(f'Pattern {n}', 6, steps(6, 3), 'srp', EXPLAIN_PATTERN) for n in (1, 2, 3)),
     '4-3', URB + MAP, (), (Q12CI,)),
])

TASKS = [*PART_ONE, *PART_TWO]

ID_CORRECTION_REASON = 'No 2016 Ordinary card shipped before this review; every card is new.'

# No 2016 Ordinary card was live on origin/main before this review.
LEGACY_IDS: list[str] = []
