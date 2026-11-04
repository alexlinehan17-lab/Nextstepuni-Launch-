"""Independent review ledger: Leaving Certificate Geography 2022 Ordinary Level.

Sources (English editions, Paper Trail index; sizes and SHA-256 pinned in
EXPECTED_SOURCES and the generated audit): Part One and Answerbook
LC005GLP042EV (40 pages), Part Two LC005GLP043EV (24 pages), marking scheme
LC005GLP000EV (40 pages), and the common companions shared with Higher Level
in the harvested corpus — the 1:50 000 Clonmel map LC005CLP003EV, its legend
LC005CLPC00EV and the Clonmel aerial photograph LC005CLP004EV (in 2022 both
the legend and the photograph are published only as JPEGs).

Visual sweep (every page rendered and read on 2026-10-12):
  Part One booklet p1 cover (2022: Part One 100 marks, Part Two 200); p2
  instructions (Part One "Attempt any TEN"; Part Two "attempt TWO", each
  from a different section); p3-p11 Questions 1-12 (p5 holds Q3 and Q4, p8
  Q7 and Q8, p9 Q9 and Q10; Q2 prints its own OS map extract); p12 Part Two
  answerbook instructions; p13-p16 graph paper; p17-p39 lined answer pages;
  p40 copyright/back cover.
  Part Two booklet p1 cover; p2 Part Two instructions; p3-p11 Sections 1-2
  (Q1-Q6; p5 holds only 2C, p7 only 3C, p11 6B and 6C); p12 Section 3
  divider; p13-p20 Electives (Q7-Q12; p15 holds only 8C, p19 11B and 11C);
  p21-p23 "Do not hand this up"; p24 copyright/back cover.
  Scheme p1 cover; p2-p3 notes; p4 annotation key; p5 Geographical
  Investigation (coursework, not a written-paper task); p6 presentation
  breakdown; p7-p8 Part One table; p9-p22 Q1-Q6; p23 Section 3 divider;
  p24-p35 Q7-Q12; p36 investigation topics; p37 Irish-language bonus marks;
  p38-p39 blank; p40 back cover.
  Companions: Clonmel map extract (the River Suir, Lachtnafrankee, the N24);
  OS Discovery Series legend sheet; oblique aerial photograph of Clonmel.

Companions. Part One Q7, Q8 (map, legend) and Q9 (aerial); Part Two 1A, 8C
and 11C (map, legend), 7A, 10C and 12A (aerial) were held back before this
review because their companions were not wired. Each now carries the exact
official documents it names.

Tariffs as printed: in 2022 the Ordinary paper does not keep the usual
30/40/30 pattern — 2C, 6C, 7C, 8C and 12C carry 40 marks and 2B, 6B, 7B, 8B
and 12B 30 — and QUESTION_TARIFFS follows each printed [Nm]. An SRP is 3
marks; "a+b" lines are one criterion with partial credit a; graded lines
keep their printed grades; sketch items are "showing 3 (3/1/0) + labelled
2" (the scheme lists four of the five printed 7A and 12A items but prices
five); 4A items are "named 2 + shown 4 (4/2/0)"; 10C reasons are "aerial
photograph evidence 1 + 3 SRPs".

Boundaries follow the 2023 Ordinary ledger: every priced roman is a task; a
matching table under ONE printed instruction stays one task with a criterion
per scheme row, the scheme listing its answers in the printed row order: Q1
Shockwaves=C, Tsunami=B, Focus=A; Q2 prints (i) and (ii) in one
part-completed table: (i) V-shaped valley=A, Beach=C, Flood plain=B (Sea
stack D is printed), (ii) Beach Deposition, Sea stack Erosion (the other two
ticks are printed); Q3 Coastal deposition=E, Glacial deposition=D, Glacial
erosion=C, Freeze-thaw action=B, Chemical weathering=A; Q4 The Burren=D,
Greater Dublin Area=A, Mezzogiorno=B, Basque Country=C, Nord Département=E;
Q5 Sahara=B, Mississippi=D, Southern Alps=C, Typhoon Chanthu=A; Q6
Fishing=B, Manufacturing=A, Transport=D, Agriculture=C; Q10 Cold front=B,
High=D, Low=A, Warm front=C; Part Two 2A(v) Avalanche Fast, Soil creep Slow,
Mudflow Fast, Rockfall Fast; 2C(i) B Sandstone, C Limestone, A Marble; 3A(i)
C Magma chamber, A Crater, D Layers of ash and rock, B Ash cloud; 12C(i) B
Residential, D Commercial, A Transport, C Religious. 7C's "tourism or
financial services" runs through all four romans and the scheme marks either
alike, so each roman is one card with the printed wording.

Wording: the paper wins where the scheme reprints it differently (2C(iii)
"Name one igneous rock and give a location where it can be found", 6A(i)
"Portugal", 5A(vii) "caused by less tourists visiting Ireland").
"""

import itertools

from geography_review import (
    Criterion, Lift, Route, SchemeSlice, Task, pool, fixed, slug, srp, steps, sums,
)

YEAR = 2022
LEVEL = 'ordinary'
PAPER_PAGES = {1: 40, 2: 24}
SCHEME_PAGES = 40
_FORTY = {'1B', '2C', '3B', '4B', '5B', '6C', '7C', '8C', '9B', '10B', '11B', '12C'}
QUESTION_TARIFFS = {1: {str(n): 10 for n in range(1, 13)},
                    2: {f'{n}{x}': (40 if f'{n}{x}' in _FORTY else 30)
                        for n in range(1, 13) for x in 'ABC'}}

EXPECTED_SOURCES = {
    'paper1': ('LC005GLP042EV.pdf', 3276320),
    'paper2': ('LC005GLP043EV.pdf', 2437509),
    'scheme': ('LC005GLP000EV.pdf', 1912158),
    'map': ('LC005CLP003EV.pdf', 5462059),
    'legend': ('LC005CLPC00EV.jpg', 4251010),
    'aerial': ('LC005CLP004EV.jpg', 5185646),
}

PAGE_REVIEW = {
    'paper1': {1: 'cover', 2: 'instructions', **{p: 'question' for p in range(3, 12)},
               12: 'answerbook instructions', **{p: 'graph-paper answer page' for p in range(13, 17)},
               **{p: 'lined answer page' for p in range(17, 40)}, 40: 'copyright/back cover'},
    'paper2': {1: 'cover', 2: 'Part Two instructions',
               **{p: 'question' for p in (*range(3, 12), *range(13, 21))},
               12: 'section divider', 21: 'do not hand this up', 22: 'do not hand this up',
               23: 'do not hand this up', 24: 'copyright/back cover'},
    'scheme': {1: 'cover', 2: 'notes', 3: 'notes', 4: 'annotation key',
               5: 'geographical investigation (coursework)', 6: 'investigation presentation breakdown',
               7: 'Part One table', 8: 'Part One table',
               **{p: 'Part Two allocation' for p in range(9, 23)}, 23: 'section divider',
               **{p: 'Part Two allocation' for p in range(24, 36)},
               36: 'investigation topics', 37: 'Irish-language bonus marks',
               38: 'blank', 39: 'blank', 40: 'back cover'},
}

EXPECTED_SELECTION_SCAN = [
    [1, 2, 'attempt any ten'], [1, 2, 'attempt two'], [1, 3, 'attempt any ten'],
    [2, 2, 'attempt two'],
    [2, 3, 'answer (i) or (ii)'], [2, 3, 'any two'], [2, 3, 'any two'],
    [2, 4, 'one of the following'],
    [2, 6, 'any two'], [2, 6, 'any two'],
    [2, 7, 'one of the following'],
    [2, 9, 'any two'],
    [2, 11, 'any one'],
    [2, 16, 'any one'],
    [2, 19, 'any three'],
]
SELECTION_REVIEW = [
    {'scan': [[1, 2, 'attempt any ten'], [1, 2, 'attempt two'], [1, 3, 'attempt any ten'],
              [2, 2, 'attempt two']],
     'kind': 'exam-attempt-rule',
     'reason': 'Part One any ten of twelve and Part Two two questions from different sections are attempt rules; every question is carded.'},
    {'scan': [[2, 3, 'answer (i) or (ii)']], 'kind': 'closed-route',
     'reason': '1B: (i) or (ii) -> two routes, each with its own scheme allocation.'},
    {'scan': [[2, 4, 'one of the following']], 'kind': 'closed-choose-one',
     'reason': '2B: one of three printed surface processes -> three routes.'},
    {'scan': [[2, 7, 'one of the following']], 'kind': 'closed-choose-one',
     'reason': '3C: one of four printed interactions -> four routes.'},
    {'scan': [[2, 6, 'any two'], [2, 9, 'any two']], 'kind': 'choose-n-one-card',
     'reason': '3B(ii) any two of three printed types of weathering and 5B any two of three printed headings -> one card each with every printed item (choice is not a route; the scheme marks each chosen item alike).'},
    {'scan': [[2, 3, 'any two'], [2, 3, 'any two'], [2, 6, 'any two'], [2, 11, 'any one'],
              [2, 16, 'any one'], [2, 19, 'any three']],
     'kind': 'open-response',
     'reason': 'No printed pool: 1B(i) any two landforms and 1B(ii) any two mass movement processes (the scheme prices two @ 20m); 3B(i) any two factors; 6B any one urban area; 9C(i) any one EU policy; 11B(iii) any three problems. 7C "tourism or financial services" runs through all four romans and the scheme marks either alike, so each roman is one card with the printed wording; 10C "three reasons" and 11C "three different examples" are open too.'},
]

P1, P2 = 1, 2
ID = 'geography-2022-ol-'
O = 'geography-ordinary-'
SRP3 = 3


def L(page, start, end=None, nth=None):
    return Lift(page, start, end, None, nth)


def S(page, start, end=None, clip=None, after=None, table=False):
    return SchemeSlice(page, start, end, clip, after, table)


def srp3(label, count, line):
    return srp(label, count, line, SRP3)


def T(key, part, q, sub, marks, page, title, prompt, scheme, criteria, topic, atlas, card_id,
      legacy, sources=(), stem=(), routes=(), row_labels=(), absorbs=()):
    return Task(key, part, q, sub, marks, page, title, prompt, scheme, criteria, topic, atlas,
                sources, card_id, legacy, stem=stem, routes=routes, row_labels=row_labels,
                absorbs=absorbs)


def rows(lines, marks=2):
    return tuple(fixed(f'Row {i}', marks, line) for i, line in enumerate(lines, 1))


def chosen(items, k):
    return [(combo, ' + '.join(item.rstrip('.') for item in combo),
             '-'.join(slug(item, 34) for item in combo))
            for combo in itertools.combinations(items, k)]


def bullet_routes(prefix, items, k=1, atlas=None):
    return tuple(Route(route_slug, label, ID + prefix + route_slug, True, keep_bullets=combo,
                       atlas=(atlas[combo[0]] if atlas else None))
                 for combo, label, route_slug in chosen(items, k))


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


def part_one_romans(q, page, title, stem, first_legacy, sources, parts):
    """Part One romans. parts: (roman, prompt Lifts, scheme start, scheme end, criteria, topic, atlas)."""
    out = []
    for index, (roman, prompt, start, end, criteria, topic, atlas) in enumerate(parts):
        key = roman.strip('()')
        out.append(T(f'p1-{q}-{key}', P1, q, roman, sum(c.max for c in criteria), page, title,
                     prompt if isinstance(prompt, tuple) else (prompt,), (S(8 if int(q) > 6 else 7, start, end),),
                     criteria, topic, atlas, ID + f'p1-q{q}' + ('' if index == 0 else f'-{key}'),
                     first_legacy and index == 0, sources, stem))
    return out


# ---------------------------------------------------------------- Part One --
TF1 = 'Indicate whether the following statement is true or false by ticking (✓) the correct box.'
Q1S = (L(3, 'Examine the diagram above which shows an earthquake', 'following questions.'),)
Q2S = (L(4, 'Examine the Ordnance Survey map extract above.', 'completed for you.'),)
Q5S = (L(6, 'Examine the satellite images above and answer each of the following questions.'),)
Q6S = (L(7, 'Examine the photographs above showing examples of different economic activities',
         'following questions.'),)
Q7S = (L(8, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper and answer each',
         'following questions.', nth=0),)
Q8S = (L(8, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper and answer each',
         'following questions.', nth=1),)
Q9S = (L(9, 'Examine the aerial photograph of Clonmel accompanying this paper.'),
       L(9, 'Indicate whether each of the following statements is true or false', 'in each case.'))
Q11S = (L(10, 'Examine the table above showing the percentage share of exports', 'following questions.'),)
Q12S = (L(11, 'Examine the bar chart above which shows the population', 'following questions.'),)

PART_ONE = [
    T('p1-1-i', P1, '1', '(i)', 6, 3, L(3, 'Earthquakes'),
      (L(3, '(i) Match each of the letters A, B and C with the term', 'table below.'),),
      (S(7, 'Q1. (i)', 'Q.1 (ii)'),), rows(['Q1. (i) · C · 2m', '=B · 2m', '=A · 2m']),
      '0-7', EV, ID + 'p1-q1', True, ('page',), Q1S,
      row_labels=(L(3, 'Shockwaves'), L(3, 'Tsunami'), L(3, 'Focus'))),
    T('p1-1-ii', P1, '1', '(ii)', 2, 3, L(3, 'Earthquakes'),
      (L(3, '(ii) ' + TF1), L(3, 'A barometer is an instrument used to measure earthquakes.')),
      (S(7, 'Q.1 (ii)', 'Q.1 (iii)'),), (fixed('True or false', 2, 'Q.1 (ii) · False · 2m'),),
      '0-7', EV, ID + 'p1-q1-ii', False, ('page',), Q1S),
    T('p1-1-iii', P1, '1', '(iii)', 2, 3, L(3, 'Earthquakes'),
      (L(3, '(iii) ' + TF1), L(3, 'The Richter scale is used to show the magnitude', 'of an earthquake.')),
      (S(7, 'Q.1 (iii)', 'Q.2 (i)'),), (fixed('True or false', 2, 'Q.1 (iii) · True · 2m · Total 10m'),),
      '0-7', EV, ID + 'p1-q1-iii', False, ('page',), Q1S),
    T('p1-2-i', P1, '2', '(i)', 6, 4, L(4, 'Coastal and River Landforms and Processes'),
      (L(4, '(i) Match each of the labels A, B, C and D', 'table below.'),),
      (S(7, 'Q.2 (i)', '(D) Erosion'),),
      (fixed('Row 1', 2, 'Q.2 (i) · A Q.2 (ii) (Erosion) · 2m'), fixed('Row 2', 2, 'C Deposition · 2m+ 2m'),
       fixed('Row 3', 2, 'B (Deposition) · 2m')),
      '0-4', RIVERS + SEA + MAP, ID + 'p1-q2', True, ('page',), Q2S,
      row_labels=(L(4, 'V-shaped valley'), L(4, 'Beach'), L(4, 'Flood plain'))),
    T('p1-2-ii', P1, '2', '(ii)', 4, 4, L(4, 'Coastal and River Landforms and Processes'),
      (L(4, '(ii) Indicate, by ticking the correct box', 'the process of deposition.'),),
      (S(7, 'C Deposition', 'B (Deposition)'), S(7, '(D) Erosion', 'Q.3')),
      (fixed('Row 1', 2, 'C Deposition · 2m+ 2m'), fixed('Row 2', 2, '(D) Erosion · 2m · Total 10m')),
      '0-4', RIVERS + SEA, ID + 'p1-q2-ii', False, ('page',), Q2S,
      row_labels=(L(4, 'Beach'), L(4, 'Sea stack'))),
    T('p1-3', P1, '3', '', 10, 5, L(5, 'Physical Processes'),
      (L(5, 'Match each of the features below with the process most associated', 'in the table below.'),),
      (S(7, 'Q.3', 'Q.4'),),
      rows(['Q.3 · E · 2m', '=D · 2m', '=C · 2m', '=B · 2m', ('=2m', 'A · Total 10m')]),
      '0-4', RIVERS + SEA + GLAC + RW, ID + 'p1-q3', True, ('page',),
      row_labels=(L(5, 'Coastal deposition'), L(5, 'Glacial deposition'), L(5, 'Glacial erosion'),
                  L(5, 'Freeze-thaw action'), L(5, 'Chemical weathering'))),
    T('p1-4', P1, '4', '', 10, 5, L(5, 'Regions'),
      (L(5, 'Match the type of region with the example of the region', 'in the table below.'),),
      (S(7, 'Q.4', 'Q.5'),), rows(['Q.4 · D · 2m', '=A · 2m', '=B · 2m', '=C · 2m', 'E · 2m · Total 10m']),
      '1-0', IRL + EURO, ID + 'p1-q4', True, ('page',),
      row_labels=(L(5, 'The Burren'), L(5, 'Greater Dublin Area'), L(5, 'Mezzogiorno'), L(5, 'Basque Country'),
                  L(5, 'Nord Département'))),
    T('p1-5-i', P1, '5', '(i)', 8, 6, L(6, 'Satellite Interpretation'),
      (L(6, '(i) Match each of the images A, B, C and D with the description', 'table below.'),),
      (S(7, 'Q.5 (i)', '(ii) · False'),), rows(['Q.5 (i) · B · 2m', '=D · 2m', '=C · 2m', '=A · 2m']),
      '2-8', AER, ID + 'p1-q5', True, ('page',), Q5S,
      row_labels=(L(6, 'Sahara Desert sand dunes, Libya'), L(6, 'Mississippi River delta, USA'),
                  L(6, 'Southern Alps mountain range, New Zealand'), L(6, 'Typhoon Chanthu, Philippines'))),
    T('p1-5-ii', P1, '5', '(ii)', 2, 6, L(6, 'Satellite Interpretation'),
      (L(6, '(ii) ' + TF1), L(6, 'A river delta forms at the source of a river.')),
      (S(7, '(ii) · False · 2m · Total 10m', 'Q.6'),), (fixed('True or false', 2, '(ii) · False · 2m · Total 10m'),),
      '0-9', RIVERS + AER, ID + 'p1-q5-ii', False, ('page',), Q5S),
    T('p1-6-i', P1, '6', '(i)', 8, 7, L(7, 'Economic Activity', nth=0),
      (L(7, '(i) Match each of the photographs A, B, C and D with the economic activity', 'table below.'),),
      (S(7, 'Q.6 (i)', '(ii) · D'),), rows(['Q.6 (i) · B · 2m', '=A · 2m', '=D · 2m', '=C · 2m']),
      '3-0', ECON, ID + 'p1-q6', True, ('page',), Q6S,
      row_labels=(L(7, 'Fishing'), L(7, 'Manufacturing'), L(7, 'Transport'), L(7, 'Agriculture'))),
    T('p1-6-ii', P1, '6', '(ii)', 2, 7, L(7, 'Economic Activity', nth=0),
      (L(7, '(ii) Which photograph shows an example of a tertiary economic activity?'),),
      (S(7, '(ii) · D'),), (fixed('Photograph', 2, '(ii) · D · 2m · Total 10m'),),
      '3-0', ECON, ID + 'p1-q6-ii', False, ('page',), Q6S),
    T('p1-7-i', P1, '7', '(i)', 6, 8, L(8, 'Ordnance Survey Map', nth=0),
      (L(8, '(i) Name the feature shown at each of the following grid references:'),),
      (S(8, 'Q.7 (i)', '(ii) · Correctly drawn'),),
      rows(['Q.7 (i) · Castle · 2m', '18hole golf · 2m', 'Parking · 2m']),
      '2-6', MAP, ID + 'p1-q7', False, ('map', 'legend'), Q7S,
      row_labels=(L(8, 'S 143 268:'), L(8, 'S 242 205:'), L(8, 'S 218 239:'))),
    T('p1-7-ii', P1, '7', '(ii)', 2, 8, L(8, 'Ordnance Survey Map', nth=0),
      (L(8, '(ii) Draw the Ordnance Survey map symbol for a picnic site in the box below.'),),
      (S(8, '(ii) · Correctly drawn symbol', '(iii) · S 205'),),
      (fixed('Symbol', 2, '(ii) · Correctly drawn symbol · 2m'),), '2-6', MAP, ID + 'p1-q7-ii', False,
      ('map', 'legend'), Q7S),
    T('p1-7-iii', P1, '7', '(iii)', 2, 8, L(8, 'Ordnance Survey Map', nth=0),
      (L(8, '(iii) Give a six-figure grid reference for the railway station in Clonmel.'),),
      (S(8, '(iii) · S 205 234', 'Q.8'),), (fixed('Grid reference', 2, '(iii) · S 205 234 · 2m · Total 10m'),),
      '2-6', MAP, ID + 'p1-q7-iii', False, ('map', 'legend'), Q7S),
    T('p1-8-i', P1, '8', '(i)', 5, 8, L(8, 'Ordnance Survey Map', nth=1),
      (L(8, '(i) Long Hill and Lachtnafrankee are located in which area', 'Tick (✓) the correct box.'),
       L(8, 'North east'), L(8, 'South east')),
      (S(8, 'Q.8 (i)', '(ii) · 4.3km'),), (fixed('Area of the map', 5, 'Q.8 (i) · South east · 5m'),),
      '2-6', MAP, ID + 'p1-q8', False, ('map', 'legend'), Q8S),
    T('p1-8-ii', P1, '8', '(ii)', 5, 8, L(8, 'Ordnance Survey Map', nth=1),
      (L(8, '(ii) What is the length of the N24 road', 'Tick (✓) the correct box.'),
       L(8, '4.3 kilometres'), L(8, '2.8 kilometres')),
      (S(8, '(ii) · 4.3km', 'Q.9'),), (fixed('Length', 5, '(ii) · 4.3km · 5m · Total 10m'),),
      '2-6', MAP, ID + 'p1-q8-ii', False, ('map', 'legend'), Q8S),
]

PART_ONE += part_one_romans('9', 9, L(9, 'Aerial Photograph'), Q9S, False, ('aerial',), [
    ('(i)', L(9, '(i) There is a bridge located in the right background of the aerial photograph.'),
     'Q.9 (i)', '(ii) · True', (fixed('True or false', 2, 'Q.9 (i) True · 2m'),), '2-8', AER),
    ('(ii)', L(9, '(ii) There is a racetrack in the centre background of the aerial photograph.'),
     '(ii) · True', '(iii) · False', (fixed('True or false', 2, '(ii) · True · 2m'),), '2-8', AER),
    ('(iii)', L(9, '(iii) There are no car parks in the centre middleground.'),
     '(iii) · False', '(iv) · True', (fixed('True or false', 2, '(iii) · False · 2m'),), '2-8', AER),
    ('(iv)', L(9, '(iv) There is a church located in the right foreground of the aerial photograph.'),
     '(iv) · True', '(v) · False', (fixed('True or false', 2, '(iv) · True · 2m'),), '2-8', AER),
    ('(v)', L(9, '(v) The aerial photograph is a vertical aerial photograph.'),
     '(v) · False', 'Q.10', (fixed('True or false', 2, '(v) · False · 2m · Total 10m'),), '2-8', AER),
])

PART_ONE += [
    T('p1-10-i', P1, '10', '(i)', 8, 9, L(9, 'Weather Charts'),
      (L(9, '(i) Match each of the weather chart symbols with the feature of weather', 'in the table below.'),),
      (S(8, 'Q.10 (i)', '(ii) · Depression'),), rows(['Q.10 (i) · B · 2m', '=D · 2m', '=A · 2m', '=C · 2m']),
      '2-7', WEATHER, ID + 'p1-q10', True, ('page',),
      row_labels=(L(9, 'Cold front'), L(9, 'High pressure system'), L(9, 'Low pressure system'),
                  L(9, 'Warm front'))),
    T('p1-10-ii', P1, '10', '(ii)', 2, 9, L(9, 'Weather Charts'),
      (L(9, '(ii) What is another name for a low pressure system?', 'Tick (✓) the correct box.'),
       L(9, 'Depression'), L(9, 'Anticyclone')),
      (S(8, '(ii) · Depression', 'Q.11'),), (fixed('Name', 2, '(ii) · Depression · 2m · Total 10m'),),
      '2-7', WEATHER, ID + 'p1-q10-ii', False, ('page',)),
]

PART_ONE += part_one_romans('11', 10, L(10, 'Trade Statistics'), Q11S, True, ('page',), [
    ('(i)', L(10, '(i) What percentage of Irish exports went to Belgium in 2018?'), 'Q.11 (i)', '(ii) · Germany',
     (fixed('Percentage', 2, 'Q.11 (i) 13(%) · 2m'),), '2-0', GRAPH),
    ('(ii)', L(10, '(ii) Which country received 9% of Irish exports in 2019?'), '(ii) · Germany', '(iii) · 4(%)',
     (fixed('Country', 2, '(ii) · Germany · 2m'),), '2-0', GRAPH),
    ('(iii)', L(10, '(iii) Calculate the difference in the percentage of Irish exports received by the USA',
                '2017 and 2019.'),
     '(iii) · 4(%)', '(iv) · UK', (fixed('Difference', 2, '(iii) · 4(%) · 2m'),), '2-0', GRAPH),
    ('(iv)', L(10, '(iv) Name one country listed above that received a lower percentage', 'in 2017.'),
     '(iv) · UK', '(v) · One valid', (fixed('Country', 2, '(iv) · UK/Belgium/Switzerland · 2m'),), '2-0', GRAPH),
    ('(v)', L(10, '(v) Name one product that is exported from Ireland.'), '(v) · One valid', 'Q.12',
     (fixed('Product', 2, '(v) · One valid product named · 2m · Total 10m'),), '3-3', EU),
])

PART_ONE += part_one_romans('12', 11, L(11, 'Population Statistics'), Q12S, True, ('page',), [
    ('(i)', L(11, '(i) What was the population, in millions, of Sao Paulo in 2018?'), 'Q.12', 'Tokyo',
     (fixed('Population', 2, 'Q.12 · 21.7(m) · 2m'),), '2-0', GRAPH),
    ('(ii)', L(11, '(ii) Which city had the largest population in 2018?'), 'Tokyo · 2m', 'Beijing',
     (fixed('City', 2, 'Tokyo · 2m'),), '2-0', GRAPH),
    ('(iii)', L(11, '(iii) Which two cities had the same population in 2018?'), 'Beijing and Dhaka', 'Urban · 2m',
     (fixed('Two cities', 4, 'Beijing and Dhaka · 2m+ 2m', (0, 2, 4)),), '2-0', GRAPH),
    ('(iv)', (L(11, '(iv) Are cities urban or rural areas?', 'Tick (✓) the correct box.'),
              L(11, 'Urban'), L(11, 'Rural')),
     'Urban · 2m', None, (fixed('Urban or rural', 2, 'Urban · 2m · Total 10m'),), '4-3', URB),
])


# ---------------------------------------------------------------- Part Two --
def romans(q, page, title, stem, first_id, sources, parts, legacy_first=True):
    """Separately priced romans of one A/B/C part.
    parts: (sub, marks, prompt Lift, scheme slice(s), criteria, topic, atlas[, extra stem Lifts[, row labels]])."""
    out = []
    for index, part in enumerate(parts):
        sub, marks, prompt, scheme, criteria, topic, atlas = part[:7]
        extra = part[7] if len(part) > 7 else ()
        labels = part[8] if len(part) > 8 else ()
        scheme = scheme if isinstance(scheme, tuple) else (scheme,)
        roman = sub.strip('()')
        out.append(T(f'p2-{q.lower()}-{roman}', P2, q, sub, marks, page, title, (prompt,), scheme,
                     criteria, topic, atlas, first_id if index == 0 else f'{first_id}-{roman}',
                     index == 0 and legacy_first, sources, (*stem, *extra), row_labels=labels))
    return out


def sketch(page, title, prompt, scheme_page, card_id, topic, atlas, sources, bullets):
    item = sums((0, 1, 3), (0, 2))
    return T(f'p2-{card_id.rsplit("-q", 1)[1]}', P2, card_id.rsplit('-q', 1)[1].upper(), '', 30, page,
             title, (prompt,), (S(scheme_page, 'Sketch Outline:', 'Total 30m'),),
             (fixed('Limits/frame', 1, ('Sketch Outline:', 'imits/')),
              fixed('Proportions (landscape)', 2, 'Proportions (landscape) · 2m'),
              fixed('Overall impression', 2, '2m graded (2/1/0)', (0, 1, 2)),
              *(Criterion(f'Item {n}', 5, item, 'exact',
                          ('Five items shown and labelled as follows:', 'Showing · 3m graded (3/1/0)',
                           'Labelled · 2m')) for n in range(1, 6))),
             topic, atlas, card_id, False, sources,
             row_labels=(None, None, None, *(b if isinstance(b, Lift) else L(page, b) for b in bullets)))


def two_of(label, count, head, each, lines, unit):
    per = sums(*unit)
    return tuple(Criterion(f'{label} {n}', count, per, 'srp', (head, each, *lines)) for n in (1, 2))


PART_TWO = [
    sketch(3, L(3, 'Ordnance Survey Map'),
           L(3, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper.',
             'in the south west of the map.'),
           9, ID + 'p2-q1a', '2-6', MAP, ('map', 'legend'),
           ('The River Suir', 'The triangulation pillar at Lachtnafrankee', 'A viewpoint', 'The railway line',
            'An area of coniferous plantation in the south west of the map')),
    T('p2-1b', P2, '1B', '', 40, 3, L(3, 'Landform Development'),
      (L(3, '(i) Explain, with the aid of diagrams, the formation of any two landforms.'),),
      (S(10, 'Formation of any two landforms @ 20m each.', 'Or'),),
      two_of('Landform', 20, 'Formation of any two landforms @ 20m each.', 'For each landform:',
             ('Landform named · 1m', 'Diagram(s) two aspects @ 2m each · 4m',
              'Formation explained 5 SRP’s @ 3m each · 15m'),
             ((0, 1), (0, 2, 4), steps(15, 3))),
      '0-4', PS_SURFACE, ID + 'p2-q1b-route-i', True,
      routes=(
          Route('route-i', 'Route (i)', ID + 'p2-q1b-route-i', True),
          Route('route-ii', 'Route (ii)', ID + 'p2-q1b-route-ii', True,
                prompt=(L(3, '(ii) Describe and explain any two processes of mass movement.'),),
                scheme=(S(10, 'Any two processes @ 20m each', 'Total 40m'),),
                criteria=two_of('Process', 20, 'Any two processes @ 20m each', 'For each process:',
                                ('Process stated · 2m', 'Description / Explanation 6 SRP’s @ 3m each · 18m'),
                                ((0, 2), steps(18, 3))),
                topic='0-8', atlas=RW),
      )),
]
Q1CI = L(3, '(i) Name one example of a tectonic plate.')
PART_TWO += romans('1C', 3, L(3, 'Plate Tectonics'), (), ID + 'p2-q1c', (), [
    ('(i)', 3, Q1CI, S(11, 'Tectonic plate named', '(ii) · Describe and explain'),
     (fixed('Tectonic plate named', 3, 'Tectonic plate named · 3m'),), '0-0', PS),
    ('(ii)', 27, L(3, '(ii) Describe and explain what happens at plate boundaries.'),
     S(11, 'Description/Explanation 9 SRP', 'Total 30m'),
     (srp3('Description/explanation', 9, 'Description/Explanation 9 SRP’s @ 3m each · 27m'),), '0-0', PS),
])

Q2AS = (L(4, 'Examine the article above about a bogburst and answer each of the following questions.'),)
MASS = ('Avalanche', 'Soil creep', 'Mudflow', 'Rockfall.')
PART_TWO += romans('2A', 4, L(4, 'Mass Movement', nth=0), Q2AS, ID + 'p2-q2a', ('page',), [
    ('(i)', 3, L(4, '(i) In what county did the bogburst take place?'),
     S(12, 'Donegal · 3m', '(ii) · What did local residents'), (fixed('County', 3, 'Donegal · 3m'),), '0-8', RW),
    ('(ii)', 3, L(4, '(ii) What did local residents believe was the cause of the bogburst?'),
     S(12, 'Recent construction activity', '(iii) · Name one impact'),
     (fixed('Cause', 3, 'Recent construction activity at a nearby wind farm · 3m'),), '0-8', RW),
    ('(iii)', 3, L(4, '(iii) Name one impact of the bogburst mentioned in the article.'),
     S(12, 'River pollution · 3m', '(iv) · What is the energy'), (fixed('Impact', 3, 'River pollution · 3m'),),
     '0-8', RW),
    ('(iv)', 3, L(4, '(iv) What is the energy generated at the windfarm being used for?'),
     S(12, 'Supply energy to worldwide data centres', '(v) · In your answerbook'),
     (fixed('Use of the energy', 3, 'Supply energy to worldwide data centres · 3m'),), '0-8', RW),
    ('(v)', 12, L(4, '(v) In your answerbook, state whether each the following types of mass movement', 'Rockfall.'),
     S(12, '• Avalanche', '(vi) · Explain briefly'),
     (fixed('Row 1', 3, '• Avalanche · Fast · 3m'), fixed('Row 2', 3, '• Soil creep · Slow · 3m'),
      fixed('Row 3', 3, '• Mudflow · Fast · 3m'), fixed('Row 4', 3, '• Rockfall. · Fast · 3m')), '0-8', RW, (),
     (L(4, 'Avalanche'), L(4, 'Soil creep'), L(4, 'Mudflow'), L(4, 'Rockfall.'))),
    ('(vi)', 6, L(4, '(vi) Explain briefly one factor that influences mass movement, other than human activity.'),
     S(12, 'Brief explanation two SRP', 'Total 30m'),
     (srp3('Brief explanation', 2, 'Brief explanation two SRP’s @ 3m each · 6m'),), '0-8', RW),
])

SURFACE = ('River processes', 'Coastal processes', 'Mass movement.')
PART_TWO.append(T(
    'p2-2b', P2, '2B', '', 30, 4, L(4, 'Human Interaction with Surface Processes'),
    (L(4, 'Examine how humans interact with one of the following surface processes:', 'Mass movement.'),),
    (S(13, 'Interaction identified · 3m', 'Total 30m'),),
    (fixed('Interaction identified', 3, 'Interaction identified · 3m'),
     srp3('Explanation', 9, 'Explanation 9 SRP’s @ 3m each · 27m')),
    '0-6', RIVERS, ID + 'p2-q2b-river-processes', True,
    routes=bullet_routes('p2-q2b-', SURFACE, atlas=dict(zip(SURFACE, (RIVERS, SEA, RW))))))

Q2CI = L(5, '(iii) Name one igneous rock and give a location where it can be found.')
PART_TWO += romans('2C', 5, L(5, 'Rocks'), (), ID + 'p2-q2c', ('page',), [
    ('(i)', 9, L(5, '(i) In your answer book, match each of the photographs A, B and C with the rock', 'Marble.'),
     S(14, '• B Sandstone', '(ii) · State two ways'),
     (fixed('Row 1', 3, '• B Sandstone · 3m'), fixed('Row 2', 3, '• C Limestone · 3m'),
      fixed('Row 3', 3, '• A Marble · 3m')), '0-1', RW, (),
     (L(5, 'Sandstone'), L(5, 'Limestone'), L(5, 'Marble'))),
    ('(ii)', 6, L(5, '(ii) State two ways in which rocks are used.'),
     S(14, 'Two valid ways stated', '(iii) Name and give'),
     (fixed('Two ways', 6, 'Two valid ways stated · 3m + 3m', (0, 3, 6)),), '0-1', RW),
    ('(iii)', 7, Q2CI, S(14, 'One valid rock named', '(iv) Describe and explain'),
     (fixed('Igneous rock named', 4, 'One valid rock named · 4m'), fixed('Location', 3, 'One valid location named · 3m')),
     '0-1', RW),
    ('(iv)', 18, L(5, '(iv) Describe and explain how igneous rocks are formed.'),
     S(14, 'Description/Explanation 6 SRP', 'Total 40m'),
     (srp3('Description/explanation', 6, 'Description/Explanation 6 SRP’s @ 3m each · 18m'),), '0-1', RW),
], legacy_first=True)
# Only 2C(i) needs the printed photographs.
PART_TWO[-3:] = [Task(**{**task.__dict__, 'sources': ()}) for task in PART_TWO[-3:]]

Q3AS = (L(6, 'Examine the diagram above showing a volcanic eruption', 'following questions.'),)
PART_TWO += romans('3A', 6, L(6, 'Volcanic Activity'), Q3AS, ID + 'p2-q3a', ('page',), [
    ('(i)', 12, L(6, '(i) In your answer book use each of the terms in the list below', 'Ash cloud.'),
     S(15, '• C Magma chamber', '(ii) · In your answer book'),
     (fixed('Row 1', 3, '• C Magma chamber · 3m'), fixed('Row 2', 3, '• A Crater · 3m'),
      fixed('Row 3', 3, '• D Layers of ash and rock · 3m'), fixed('Row 4', 3, '• B Ash cloud. · 3m')),
     '0-7', EV, (), (L(6, 'Magma chamber'), L(6, 'Crater'), L(6, 'Layers of ash and rock'), L(6, 'Ash cloud'))),
    ('(ii)', 3, L(6, '(ii) State if the volcano shown above is active, dormant or extinct.'),
     S(15, 'Active · 3m', '(iii) Name one example'), (fixed('Active, dormant or extinct', 3, 'Active · 3m'),),
     '0-7', EV),
    ('(iii)', 3, L(6, '(iii) Name one example of a volcano that you have studied.'),
     S(15, 'Valid example named', '(iv) List two'), (fixed('Volcano', 3, 'Valid example named · 3m'),), '0-7', EV),
    ('(iv)', 6, L(6, '(iv) List two positive effects of volcanoes.'),
     S(15, 'Two valid effects listed', '(v) · Explain briefly'),
     (fixed('Two positive effects', 6, 'Two valid effects listed · 3m+3m', (0, 3, 6)),), '0-7', EV),
    ('(v)', 6, L(6, '(v) Explain briefly one negative effect of volcanoes.'),
     S(15, 'Brief explanation two SRP', 'Total 30m'),
     (srp3('Brief explanation', 2, 'Brief explanation two SRP’s @ 3m each · 6m'),), '0-7', EV),
])

WEATHERING = ('Onion weathering', 'Carbonation', 'Freeze-thaw action.')
WEATHER_TYPE = ('Two descriptions / explanations @18m each', 'For each weathering type:',
                'Description/Explanation 6 SRP’s @ 3m each · 36m')
ROCK = ('Quarrying', 'Mining', 'Oil/Gas exploitation', 'Geothermal energy production.')
PART_TWO += [
    T('p2-3b-i', P2, '3B', '(i)', 4, 6, L(6, 'Weathering'),
      (L(6, '(i) Name any two factors that influence weathering.'),),
      (S(16, 'Two valid factors named', '(ii) · Describe and explain'),),
      (fixed('Two factors', 4, 'Two valid factors named · 2m + 2m', (0, 2, 4)),),
      '0-8', RW, ID + 'p2-q3b-i', False),
    T('p2-3b-ii', P2, '3B', '(ii)', 36, 6, L(6, 'Weathering'),
      (L(6, '(ii) Describe and explain any two of the following types of weathering:', 'Freeze-thaw action.'),),
      (S(16, 'Two descriptions / explanations', 'Total 40m'),),
      tuple(Criterion(f'Weathering type {n}', 18, steps(18, 3), 'srp', WEATHER_TYPE) for n in (1, 2)),
      '0-8', RW, *pool(ID + 'p2-q3b-', WEATHERING, 2)[:1], True, absorbs=pool(ID + 'p2-q3b-', WEATHERING, 2)[1]),
    T('p2-3c', P2, '3C', '', 30, 7, L(7, 'Human Interaction with the Rock Cycle'),
      (L(7, 'Describe and explain how humans interact with the rock cycle', 'Geothermal energy production.'),),
      (S(16, 'Description / explanation 10 SRP', 'Total 30m'),),
      (srp3('Description/explanation', 10, 'Description / explanation 10 SRP’s @ 3m each · 30m'),),
      '0-6', RW, ID + 'p2-q3c-quarrying', True, routes=bullet_routes('p2-q3c-', ROCK)),
]

SHOWN = 'Shown · 4m graded (4/2/0)'
NAMED_SHOWN = sums((0, 2), (0, 2, 4))
PART_TWO.append(T(
    'p2-4a', P2, '4A', '', 30, 8, L(8, 'Map Skills'),
    (L(8, 'Draw a sketch map of a Continental / Sub-Continental region (not in Europe)', 'in this region.'),),
    (S(17, 'Outline of Region', 'Total 30m'),),
    (fixed('Outline of region', 6, 'Outline of Region · 6m graded (6/4/2/0)', (0, 2, 4, 6)),
     Criterion('River', 6, NAMED_SHOWN, 'exact', ('River: · Named · 2m', f'={SHOWN}@0')),
     Criterion('Relief (upland/lowland)', 6, NAMED_SHOWN, 'exact',
               ('Relief (upland/lowland): · Named · 2m', f'={SHOWN}@1')),
     Criterion('Town/City 1', 6, NAMED_SHOWN, 'exact', ('Town/City 1: · Named · 2m', f'={SHOWN}@2')),
     Criterion('Town/City 2', 6, NAMED_SHOWN, 'exact', ('Town/City 2: · Named · 2m', f'={SHOWN}@3'))),
    '1-6', CONT, ID + 'p2-q4a', True))
Q4BS = (L(8, 'Answer each of the following questions with reference to an Irish region', 'studied.', nth=0),)
PART_TWO += romans('4B', 8, L(8, 'Agriculture – Irish Region'), Q4BS, ID + 'p2-q4b', (), [
    ('(i)', 4, L(8, '(i) Name two types of agriculture practised in this region.'),
     S(17, 'Two valid types named', '(ii) · Explain the advantages'),
     (fixed('Two types of agriculture', 4, 'Two valid types named · 2m+2m', (0, 2, 4)),), '1-4', IRL),
    ('(ii)', 27, L(8, '(ii) Explain the advantages that this region has for the development of agriculture.'),
     S(17, 'Explanation 9 SRP'), (srp3('Explanation', 9, 'Explanation 9 SRP’s @ 3m each · 27m'),), '1-4', IRL),
    ('(iii)', 9, L(8, '(iii) Describe one challenge faced by agriculture in this region.'),
     S(18, 'Description 3 SRP', 'Total 40m'),
     (srp3('Description', 3, 'Description 3 SRP’s @ 3m each · 9m'),), '1-4', IRL),
])
Q4CS = (L(8, 'Answer each of the following questions with reference to a European region', 'studied.'),)
Q4CI = L(8, '(i) Name one example of a secondary economic activity in this region.')
PART_TWO += romans('4C', 8, L(8, 'Secondary Economic Activity in a European Region'), Q4CS, ID + 'p2-q4c', (), [
    ('(i)', 3, Q4CI, S(18, 'One valid example named', '(ii) · Describe and explain'),
     (fixed('Secondary economic activity named', 3, 'One valid example named · 3m'),), '1-5', EURO),
    ('(ii)', 27, L(8, '(ii) Describe and explain the development of manufacturing industry in this region.'),
     S(18, 'Description/explanation 9 SRP', 'Total 30m'),
     (srp3('Description/explanation', 9, 'Description/explanation 9 SRP’s @ 3m each · 27m'),), '1-5', EURO),
])

Q5AS = (L(9, 'Examine the pie charts above which show the number of people arriving to Ireland', 'following questions.'),)
PART_TWO += romans('5A', 9, L(9, 'Tertiary Economic Activity'), Q5AS, ID + 'p2-q5a', ('page',), [
    ('(i)', 3, L(9, '(i) How many people travelled to Ireland by a transatlantic route in 2019?'),
     S(19, '2,155,000', '(ii) · In which year'), (fixed('People', 3, '2,155,000 · 3m'),), '2-0', GRAPH),
    ('(ii)', 3, L(9, '(ii) In which year did 2,170,000 people travel to Ireland from continental Europe?'),
     S(19, '2020 · 3m', '(iii) Which route'), (fixed('Year', 3, '2020 · 3m'),), '2-0', GRAPH),
    ('(iii)', 3, L(9, '(iii) Which route was used by 781,000 people to travel to Ireland in 2021?'),
     S(19, 'Cross-Channel (UK)', '(iv) Calculate'), (fixed('Route', 3, 'Cross-Channel (UK) · 3m'),), '2-0', GRAPH),
    ('(iv)', 6, L(9, '(iv) Calculate the total number of people travelling to Ireland in 2021.'),
     S(19, '2,552,000', '(v) · Name one airport'), (fixed('Total', 6, '2,552,000 · 6m'),), '2-0', GRAPH),
    ('(v)', 3, L(9, '(v) Name one airport or seaport in Ireland.'),
     S(19, 'One valid airport or seaport', '(vi) Explain briefly'),
     (fixed('Airport or seaport', 3, 'One valid airport or seaport named · 3m'),), '1-4', IRL),
    ('(vi)', 6, L(9, '(vi) Explain briefly one reason why the number of arrivals into Ireland was lower', 'than in 2019.'),
     S(19, 'Brief explanation two SRP', '(vii) Explain one', after='(vi) Explain briefly'),
     (srp3('Brief explanation', 2, 'Brief explanation two SRP’s @ 3m each · 6m'),), '1-4', IRL),
    ('(vii)', 6, L(9, '(vii) Explain one challenge caused by less tourists visiting Ireland.'),
     S(19, 'Brief explanation two SRP', 'Total 30m', after='(vii) Explain one'),
     (srp3('Brief explanation', 2, 'Brief explanation two SRP’s @ 3m each · 6m'),), '1-4', IRL),
])
ACTIVITIES = ('The factors influencing agriculture in the region', 'The importance of manufacturing to the region',
              'The reasons why tourists are attracted to the region.')
PART_TWO.append(T(
    'p2-5b', P2, '5B', '', 40, 9, L(9, 'Economic Activities – Continental / Sub-Continental Region'),
    (L(9, 'Explain any two of the following with reference to a Continental / Sub-Continental region',
       'The reasons why tourists are attracted to the region.'),),
    (S(20, 'Activity 1 explained', 'Total 40m'),),
    (srp3('Activity 1 explained', 7, 'Activity 1 explained 7 SRP’s @ 3m each · 21m'),
     srp3('Activity 2 explained', 6, 'Activity 2 explained 6 SRP’s @ 3m each · 18m'),
     fixed('Region named', 1, 'Region named · 1m')),
    '1-6', CONT, *pool(ID + 'p2-q5b-', ACTIVITIES, 2)[:1], True, absorbs=pool(ID + 'p2-q5b-', ACTIVITIES, 2)[1]))
PART_TWO += romans('5C', 9, L(9, 'Characteristics of Regions'), (), ID + 'p2-q5c', (), [
    ('(i)', 15, L(9, '(i) Name one example of a core region and explain why this region is a core region.'),
     S(20, 'Valid core region named', '(ii) · Name one example of a peripheral'),
     (fixed('Core region named', 3, 'Valid core region named · 3m'),
      srp3('Explanation', 4, 'Explanation: 4 SRP’s @ 3m each · 12m')), '1-0', IRL + EURO + CONT),
    ('(ii)', 15, L(9, '(ii) Name one example of a peripheral region and explain why this region is a',
                   'peripheral region.'),
     S(20, 'Valid peripheral region named', 'Total 30m'),
     (fixed('Peripheral region named', 3, 'Valid peripheral region named · 3m'),
      srp3('Explanation', 4, 'Explanation: 4 SRP’s @ 3m each · 12m')), '1-0', IRL + EURO + CONT),
])

Q6AS = (L(10, 'Examine the map above showing the year current and former member states', 'following questions.'),)
PART_TWO += romans('6A', 10, L(10, 'European Union', nth=0), Q6AS, ID + 'p2-q6a', ('page',), [
    ('(i)', 3, L(10, '(i) In what year did Portugal join the European Union?'),
     S(21, '1986 · 3m', '(ii) · How many'), (fixed('Year', 3, '1986 · 3m'),), '2-0', GRAPH + EURO),
    ('(ii)', 3, L(10, '(ii) How many countries joined the European Union in 1995?'),
     S(21, 'Three · 3m', '(iii) · Which country'), (fixed('Number of countries', 3, 'Three · 3m'),), '2-0', GRAPH + EURO),
    ('(iii)', 3, L(10, '(iii) Which country joined the European Union the same year as Romania?'),
     S(21, 'Bulgaria · 3m', '(iv) · Name two'), (fixed('Country', 3, 'Bulgaria · 3m'),), '2-0', GRAPH + EURO),
    ('(iv)', 6, L(10, '(iv) Name two countries that joined the European Union in 2004.'),
     S(21, 'Two valid countries named', '(v) · Explain briefly'),
     (fixed('Two countries', 6, 'Two valid countries named · 3m + 3m', (0, 3, 6)),), '2-0', GRAPH + EURO),
    ('(v)', 6, L(10, '(v) Explain briefly one advantage of membership of the European Union.'),
     S(21, 'Brief explanation two SRP', '(vi) Which country', after='(v) · Explain briefly'),
     (srp3('Brief explanation', 2, 'Brief explanation two SRP’s @ 3m each · 6m'),), '1-5', EURO),
    ('(vi)', 3, L(10, '(vi) Which country, labelled X on the map, left the European Union in 2020?'),
     S(21, 'United Kingdom · 3m', '(vii) Explain briefly'), (fixed('Country', 3, 'United Kingdom · 3m'),),
     '2-0', GRAPH + EURO),
    ('(vii)', 6, L(10, '(vii) Explain briefly one challenge facing member states of the European Union.'),
     S(21, 'Brief explanation two SRP', 'Total 30m', after='(vii) Explain briefly'),
     (srp3('Brief explanation', 2, 'Brief explanation two SRP’s @ 3m each · 6m'),), '1-5', EURO),
])
PART_TWO.append(T(
    'p2-6b', P2, '6B', '', 30, 11, L(11, 'Urban Regions'),
    (L(11, 'Describe and explain the reasons for the growth of any one urban area that you have studied.'),),
    (S(22, 'Description/explanation 10 SRP', 'Total 30m'),),
    (srp3('Description/explanation', 10, 'Description/explanation 10 SRP’s @ 3m each'),),
    '1-3', IRL + EURO, ID + 'p2-q6b', True))
Q6CS = (L(11, 'Answer each of the following questions with reference to an Irish region', 'studied.'),)
PART_TWO += romans('6C', 11, L(11, 'Tourism in an Irish Region'), Q6CS, ID + 'p2-q6c', (), [
    ('(i)', 4, L(11, '(i) Name two tourist attractions in this region.'),
     S(22, 'Two valid attractions named', '(ii) · Explain the reasons'),
     (fixed('Two tourist attractions', 4, 'Two valid attractions named · 2m+2m', (0, 2, 4)),), '1-4', IRL),
    ('(ii)', 27, L(11, '(ii) Explain the reasons why tourists are attracted to this region.'),
     S(22, 'Explanation 9 SRP', '(iii) Describe one problem'),
     (srp3('Explanation', 9, 'Explanation 9 SRP’s @ 3m each · 27m'),), '1-4', IRL),
    ('(iii)', 9, L(11, '(iii) Describe one problem associated with tourism in this region.'),
     S(22, 'Description 3 SRP', 'Total 40m'),
     (srp3('Description', 3, 'Description 3 SRP’s @ 3m each · 9m'),), '1-4', IRL),
])

PART_TWO.append(sketch(
    13, L(13, 'Aerial Photograph'),
    L(13, 'Examine the aerial photograph of Clonmel accompanying this paper.', 'in the centre foreground.'),
    24, ID + 'p2-q7a', '2-8', AER, ('aerial',),
    ('The river', 'A bridge', 'Two connecting streets', 'A car park in the right middleground',
     'An industrial building in the centre foreground')))
PART_TWO += romans('7B', 13, L(13, 'Fossil Fuels'), (), ID + 'p2-q7b', (), [
    ('(i)', 6, L(13, '(i) Name two fossil fuels.'),
     S(25, 'Two valid fossil fuels named', '(ii) Describe and explain'),
     (fixed('Two fossil fuels', 6, 'Two valid fossil fuels named · 3m+3m', (0, 3, 6)),), '3-5', ECON + ENV),
    ('(ii)', 24, L(13, '(ii) Describe and explain the impact of burning fossil fuels on the environment.'),
     S(25, 'Impact Identified 1 SRP', 'Total 30m'),
     (fixed('Impact identified', 3, 'Impact Identified 1 SRP · 3m'),
      srp3('Description/explanation', 7, 'Description/explanation 7 SRP’s @ 3m each · 21m')), '3-4', ENV),
])
Q7CI = L(13, '(i) Name one developed economy where tourism or financial services contribute to', 'that economy.')
PART_TWO += romans('7C', 13, L(13, 'Developed Economy'), (), ID + 'p2-q7c', (), [
    ('(i)', 4, Q7CI, S(25, 'Developed economy named · 4m', '(ii) · Explain the reasons'),
     (fixed('Developed economy named', 4, 'Developed economy named · 4m'),), '3-0', ECON),
    ('(ii)', 18, L(13, '(ii) Explain the reasons for the growth of tourism or financial services', 'part (i) above.'),
     S(25, 'Explanation 6 SRP', '(iii) Explain one benefit'),
     (srp3('Explanation', 6, 'Explanation 6 SRP’s @ 3m each · 18m'),), '3-0', ECON, (Q7CI,)),
    ('(iii)', 9, L(13, '(iii) Explain one benefit that tourism or financial services bring to the economy',
                   'developed countries.'),
     S(25, 'Explanation 3 SRP', '(iv) Explain one problem', after='(iii) Explain one benefit'),
     (srp3('Explanation', 3, 'Explanation 3 SRP’s @ 3m each · 9m'),), '3-0', ECON),
    ('(iv)', 9, L(13, '(iv) Explain one problem caused by tourism or financial services.'),
     S(25, 'Explanation 3 SRP', 'Total 40m', after='(iv) Explain one problem'),
     (srp3('Explanation', 3, 'Explanation 3 SRP’s @ 3m each · 9m'),), '3-0', ECON),
])

Q8AS = (L(14, 'Examine the bar chart above showing the renewable energy capacity', 'following questions.'),)
PART_TWO += romans('8A', 14, L(14, 'Renewable Energy', nth=0), Q8AS, ID + 'p2-q8a', ('page',), [
    ('(i)', 3, L(14, '(i) What was the renewable energy capacity, in gigawatts, for India in 2020?'),
     S(26, '134 (gigawatts)', '(ii) · Which country'), (fixed('Capacity', 3, '134 (gigawatts) · 3m'),), '2-0', GRAPH),
    ('(ii)', 3, L(14, '(ii) Which country from the chart above had the largest renewable energy capacity', 'in 2020?'),
     S(26, 'China · 3m', '(iii) Calculate'), (fixed('Country', 3, 'China · 3m'),), '2-0', GRAPH),
    ('(iii)', 6, L(14, '(iii) Calculate the total renewable energy capacity, in gigawatts', 'Brazil combined.'),
     S(26, '1,337 (gigawatts)', '(iv) Name two'), (fixed('Total', 6, '1,337 (gigawatts) · 6m'),), '2-0', GRAPH),
    ('(iv)', 6, L(14, '(iv) Name two sources of renewable energy.'),
     S(26, 'Two valid sources named', '(v) · Briefly explain'),
     (fixed('Two sources', 6, 'Two valid sources named · 3m+3m', (0, 3, 6)),), '3-5', ECON),
    ('(v)', 12, L(14, '(v) Briefly explain two reasons why countries are investing more in renewable energy.'),
     S(26, 'Reason 1', 'Total 30m'),
     (srp3('Reason 1', 2, 'Reason 1 - Brief explanation two SRP’s @ 3m each · 6m'),
      srp3('Reason 2', 2, 'Reason 2 - Brief explanation two SRP’s @ 3m each · 6m')), '3-5', ECON),
])
Q8BI = L(14, '(i) Name one example of how the development of economic activities has resulted in',
         'conflict arising between people.')
PART_TWO += romans('8B', 14, L(14, 'Economic Activity and Conflict'), (), ID + 'p2-q8b', (), [
    ('(i)', 3, Q8BI, S(27, 'Valid example named · 3m', '(ii) · Describe and explain'),
     (fixed('Example named', 3, 'Valid example named · 3m'),), '3-4', ENV),
    ('(ii)', 27, L(14, '(ii) Describe and explain this conflict.'),
     S(27, 'Description and explanation 9 SRP', 'Total 30m'),
     (srp3('Description and explanation', 9, 'Description and explanation 9 SRP’s @ 3m each · 27m'),), '3-4', ENV,
     (Q8BI,)),
])
Q8CS = (L(15, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper.'),
        L(15, 'Imagine you have been given the task', 'the area covered by the map.'))
Q8CI = L(15, '(i) State, using a six-figure grid reference, where you would locate the hotel.')
PART_TWO += romans('8C', 15, L(15, 'Economic Activity – Ordnance Survey Map'), Q8CS, ID + 'p2-q8c', ('map', 'legend'), [
    ('(i)', 4, Q8CI, S(27, 'Six-figure grid reference', '(ii) · Explain the reasons'),
     (fixed('Six-figure grid reference', 4, 'Six-figure grid reference · 4m graded (4/2/0)', (0, 2, 4)),),
     '2-6', MAP),
    ('(ii)', 27, L(15, '(ii) Explain the reasons why you chose this location.'),
     S(27, 'Reasons explained 9 SRP', '(iii) · Describe one'),
     (srp3('Reasons explained', 9, 'Reasons explained 9 SRP’s @ 3m each · 27m'),), '3-0', ECON + MAP, (Q8CI,)),
    ('(iii)', 9, L(15, '(iii) Describe one disadvantage of locating the hotel at this location.'),
     S(27, 'One disadvantage described', 'Total 40m'),
     (srp3('One disadvantage described', 3, 'One disadvantage described 3 SRP’s @ 3m each · 9m'),),
     '3-0', ECON + MAP, (Q8CI,)),
], legacy_first=False)

GRAPH_OL = (fixed('Graph paper', 3, 'Graph paper 3m', (0, 3)),
            fixed('Vertical axis labelled / circle', 3, 'Vertical axis labelled/Circle · 3m graded (3/1/0)', (0, 1, 3)),
            fixed('Horizontal axis labelled / centred', 3, 'Horizontal axis labelled/Centred · 3m graded (3/1/0)', (0, 1, 3)),
            fixed('5 items illustrated', 15, '5 items @ 3m each graded (3/1/0) · 15m', sums(*[(0, 1, 3)] * 5)))
Q9AS = (L(16, 'Examine the table above showing the gross national product (GNP)', 'following questions.'),)
PART_TWO += romans('9A', 16, L(16, 'Economic Development'), Q9AS, ID + 'p2-q9a', ('page',), [
    ('(i)', 24, L(16, '(i) Using graph paper, draw a suitable graph to illustrate this data.'),
     S(28, 'Graph paper 3m', '(ii) · Explain briefly'), GRAPH_OL, '2-0', GRAPH),
    ('(ii)', 6, L(16, '(ii) In your answer book, explain briefly one advantage of a country having a high',
                  'gross national product.'),
     S(28, 'Brief explanation 2 SRP', 'Total 30m'),
     (srp3('Brief explanation', 2, 'Brief explanation 2 SRP’s @ 3m each · 6m'),), '3-0', ECON),
])
Q9BI = L(16, '(i) Name one multinational company located in Ireland that you have studied and name',
         'it manufactures.')
PART_TWO += romans('9B', 16, L(16, 'Multinational Company'), (), ID + 'p2-q9b', (), [
    ('(i)', 7, Q9BI, S(28, 'Valid MNC named', '(ii) · State where'),
     (fixed('MNC named', 4, 'Valid MNC named · 4m'), fixed('Product named', 3, 'Valid product named · 3m')),
     '3-2', MNC),
    ('(ii)', 24, L(16, '(ii) State where this multinational company is located in Ireland and explain why it set up',
                   'at this location.'),
     S(28, 'Valid location · 3m', '(iii) Explain one reason'),
     (fixed('Location', 3, 'Valid location · 3m'), srp3('Explanation', 7, 'Explanation 7 SRP’s @ 3m each · 21m')),
     '3-2', MNC, (Q9BI,)),
    ('(iii)', 9, L(16, '(iii) Explain one reason why this multinational company might decide to locate to another',
                   'country.'),
     S(28, 'Explanation 3 SRP', 'Total 40m'),
     (srp3('Explanation', 3, 'Explanation 3 SRP’s @ 3m each · 9m'),), '3-2', MNC, (Q9BI,)),
])
Q9CI = L(16, '(i) Name any one European Union policy which affects Ireland’s economy.')
PART_TWO += romans('9C', 16, L(16, 'Ireland and the European Union'), (), ID + 'p2-q9c', (), [
    ('(i)', 3, Q9CI, S(29, 'Valid policy named', '(ii) · Describe and explain'),
     (fixed('Policy named', 3, 'Valid policy named · 3m'),), '3-3', EU),
    ('(ii)', 27, L(16, '(ii) Describe and explain the effects of this policy on Ireland’s economy.'),
     S(29, 'Effect Identified 1 SRP', 'Total 30m'),
     (fixed('Effect identified', 3, 'Effect Identified 1 SRP · 3m'),
      srp3('Description and explanation', 8, 'Description and explanation 8 SRP’s @ 3m each · 24m')),
     '3-3', EU, (Q9CI,)),
])

Q10AS = (L(17, 'Examine the table above showing the traffic congestion level', 'following questions.'),)
PART_TWO += romans('10A', 17, L(17, 'Traffic Congestion', nth=0), Q10AS, ID + 'p2-q10a', ('page',), [
    ('(i)', 24, L(17, '(i) Using graph paper, draw a suitable graph to illustrate this data.'),
     S(30, 'Graph paper 3m', '(ii) · In your answer book'), GRAPH_OL, '2-0', GRAPH),
    ('(ii)', 6, L(17, '(ii) In your answer book, explain briefly one reason why Dublin experiences high levels',
                  'traffic congestion.'),
     S(30, 'Brief explanation 2 SRP', 'Total 30m'),
     (srp3('Brief explanation', 2, 'Brief explanation 2 SRP’s @ 3m each · 6m'),), '4-5', URB),
])
PART_TWO += romans('10B', 17, L(17, 'Migration – Ireland'), (), ID + 'p2-q10b', (), [
    ('(i)', 22, L(17, '(i) Describe and explain the reasons why people in Ireland migrate from rural areas',
                  'using examples you have studied.'),
     S(31, 'Reasons · 2m+2m', '(ii) · Explain one effect'),
     (fixed('Reasons', 4, 'Reasons · 2m+2m', (0, 2, 4)),
      srp3('Description/explanation', 6, 'Description/explanation 6 SRP’s @ 3m each · 18m')), '4-2', POP),
    ('(ii)', 9, L(17, '(ii) Explain one effect rural to urban migration has on rural areas.'),
     S(31, 'Explanation 3 SRP', '(iii) · Explain one barrier', after='(ii) · Explain one effect'),
     (srp3('Explanation', 3, 'Explanation 3 SRP’s @ 3m each · 9m'),), '4-2', POP),
    ('(iii)', 9, L(17, '(iii) Explain one barrier to migration.'),
     S(31, 'Explanation 3 SRP', 'Total 40m', after='(iii) · Explain one barrier'),
     (srp3('Explanation', 3, 'Explanation 3 SRP’s @ 3m each · 9m'),), '4-2', POP),
])
TOWN_REASON = ('Three reasons @ 10m each · 30m', 'For each reason:', 'Aerial photograph evidence · 1m',
               'Explanation 3 SRP’s @ 3m each · 9m')
PART_TWO.append(T(
    'p2-10c', P2, '10C', '', 30, 17, L(17, 'Development of Towns'),
    (L(17, 'Using evidence from the aerial photograph accompanying this paper', 'at its present location.'),),
    (S(31, 'Three reasons @ 10m each', 'Total 30m'),),
    tuple(Criterion(f'Reason {n}', 10, sums((0, 1), steps(9, 3)), 'srp', TOWN_REASON) for n in (1, 2, 3)),
    '4-3', URB + AER, ID + 'p2-q10c', False, ('aerial',)))

Q11AS = (L(18, 'Examine the population pyramid above showing the projected population structure',
           'following questions.'),)
PART_TWO += romans('11A', 18, L(18, 'Population Dynamics'), Q11AS, ID + 'p2-q11a', ('page',), [
    ('(i)', 3, L(18, '(i) What percentage of females are projected to be aged 20-24?'),
     S(32, '2.5(%)', '(ii) · Is there'), (fixed('Percentage', 3, '2.5(%) · 3m'),), '2-0', GRAPH),
    ('(ii)', 3, L(18, '(ii) Is there projected to be more males or females aged 85+?'),
     S(32, 'Females · 3m', '(iii) · What percentage'), (fixed('Males or females', 3, 'Females · 3m'),), '2-0', GRAPH),
    ('(iii)', 3, L(18, '(iii) What percentage of the total population in the 0-4 age group', 'to be male?'),
     S(32, '2.7(%)', '(iv) · Calculate'), (fixed('Percentage', 3, '2.7(%) · 3m'),), '2-0', GRAPH),
    ('(iv)', 6, L(18, '(iv) Calculate the percentage of the total population that is projected to be aged 65-69.'),
     S(32, '6.5(%)', '(v) · State one way'), (fixed('Percentage', 6, '6.5(%) · 6m'),), '2-0', GRAPH),
    ('(v)', 3, L(18, '(v) State one way that population pyramids are used.'),
     S(32, 'One valid way stated', '(vi) · Explain briefly'), (fixed('Use', 3, 'One valid way stated · 3m'),),
     '4-0', POP),
    ('(vi)', 6, L(18, '(vi) Explain briefly one reason why people in Ireland have a long life expectancy.'),
     S(32, 'Brief explanation 2 SRP', '(vii) Explain briefly', after='(vi) · Explain briefly'),
     (srp3('Brief explanation', 2, 'Brief explanation 2 SRP’s @ 3m each · 6m'),), '4-0', POP),
    ('(vii)', 6, L(18, '(vii) Explain briefly one way the shape of a population pyramid for a developed country',
                   'developing country.'),
     S(32, 'Brief explanation 2 SRP', None, after='(vii) Explain briefly'),
     (srp3('Brief explanation', 2, 'Brief explanation 2 SRP’s @ 3m each · 6m · Total 30m'),), '4-0', POP),
])
Q11BI = L(19, '(i) Name one city in the developing world that is growing rapidly.')
PROBLEM = ('Three problems @ 9m each', 'For each problem:', 'Description/explanation 3 SRP’s @ 3m each · 27m')
PART_TWO += romans('11B', 19, L(19, 'Developing World City'), (), ID + 'p2-q11b', (), [
    ('(i)', 4, Q11BI, S(33, 'Valid developing world city named', '(ii) · Explain one reason'),
     (fixed('Developing world city named', 4, 'Valid developing world city named · 4m'),), '4-5', URB),
    ('(ii)', 9, L(19, '(ii) Explain one reason for the rapid growth of the city named by you in part (i) above.'),
     S(33, 'Explanation 3 SRP', '(iii) Describe and explain'),
     (srp3('Explanation', 3, 'Explanation 3 SRP’s @ 3m each · 9m'),), '4-5', URB, (Q11BI,)),
    ('(iii)', 27, L(19, '(iii) Describe and explain any three problems associated with the rapid growth of this',
                    'developing world city.'),
     S(33, 'Three problems @ 9m each', 'Total 40m'),
     tuple(Criterion(f'Problem {n}', 9, steps(9, 3), 'srp', PROBLEM) for n in (1, 2, 3)), '4-5', URB, (Q11BI,)),
])
Q11CS = (L(19, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper.'),)
Q11CI = L(19, '(i) Name and give a six-figure grid reference for the location of three different examples',
          'evident on the Ordnance Survey map.')
NAMED = '3 settlements named @ 2 marks each · 6m'
LOCATED = '3 settlements located @ 2 marks each graded (2/1/0) · 6 marks'
DESCRIBED = ('For each historic settlement:', 'Description: 2 SRP’s @ 3 marks each · 18 marks')
PART_TWO += romans('11C', 19, L(19, 'Historic Settlement'), Q11CS, ID + 'p2-q11c', ('map', 'legend'), [
    ('(i)', 12, Q11CI, S(33, '3 settlements named', '(ii) · Describe each'),
     (*(fixed(f'Settlement {n} named', 2, (NAMED, f'Settlement {n} named · 2m')) for n in (1, 2, 3)),
      *(fixed(f'Location {n}', 2, (LOCATED, f'Location {n} named · 2/1/0m'), (0, 1, 2)) for n in (1, 2, 3))),
     '4-3', URB + MAP),
    ('(ii)', 18, L(19, '(ii) Describe each of the three historic settlements named in part (i) above.'),
     S(33, 'For each historic settlement:', 'Total 30m', after='11C.'),
     tuple(Criterion(f'Historic settlement {n}', 6, (0, 3, 6), 'srp', DESCRIBED) for n in (1, 2, 3)),
     '4-3', URB + MAP, (Q11CI,)),
], legacy_first=False)

PART_TWO += [
    sketch(20, L(20, 'Aerial Photograph'),
           L(20, 'Examine the aerial photograph of Clonmel accompanying this paper.', 'in the centre foreground.'),
           34, ID + 'p2-q12a', '2-8', AER + URB, ('aerial',),
           ('The river', 'A bridge', 'A recreational area', 'A church in the right foreground',
            'An area of terraced housing in the centre foreground')),
    T('p2-12b', P2, '12B', '', 30, 20, L(20, 'Population Dynamics'),
      (L(20, '‘Population change is influenced by many factors', 'medical technology.’'),
       L(20, 'Describe and explain the factors that influence population change.')),
      (S(34, 'Description/explanation 10 SRP', 'Total 30m'),),
      (srp3('Description/explanation', 10, 'Description/explanation 10 SRP’s @ 3m each · 30m'),),
      '4-0', POP, ID + 'p2-q12b', True),
]
PART_TWO += romans('12C', 20, L(20, 'Urban functions'), (), ID + 'p2-q12c', ('page',), [
    ('(i)', 12, L(20, '(i) Examine the photographs of different buildings labelled A, B, C and D', 'Religious.'),
     S(35, '• B Residential', '(ii) · “The functions'),
     (fixed('Row 1', 3, '• B Residential · 3m'), fixed('Row 2', 3, '• D Commercial · 3m'),
      fixed('Row 3', 3, '• A Transport · 3m'), fixed('Row 4', 3, '• C Religious · 3m')), '4-3', URB, (),
     (L(20, 'Residential'), L(20, 'Commercial'), L(20, 'Transport'), L(20, 'Religious'))),
    ('(ii)', 28, L(20, '(ii) ‘The functions of urban areas change over time.’', 'any urban area studied by you.'),
     S(35, 'Valid urban area named', 'Total 40m'),
     (fixed('Urban area named', 4, 'Valid urban area named · 4m'),
      srp3('Discussion', 8, 'Discussion 8 SRP’s @ 3m each · 24m')), '4-3', URB),
])
# Only 12C(i) needs the printed photographs.
PART_TWO[-1] = Task(**{**PART_TWO[-1].__dict__, 'sources': ()})

TASKS = [*PART_ONE, *PART_TWO]

ID_CORRECTION_REASON = (
    'The shipped card held every part of a question the scheme prices part by '
    'part. Its id is kept on the first separately priced part; the other parts '
    'are new cards with their own published allocation. The three shipped 3B '
    'cards held the whole 40m part, one per pair of weathering types; the first '
    'pair\'s id now holds 3B(ii) as one card showing all three printed types '
    '(choice is not a route), the other two alias to it, and the separately '
    'priced 3B(i) is a new card.')

# Every 2022 Ordinary card id live on origin/main before this review (49). Each must survive.
LEGACY_IDS = [
    'geography-2022-ol-p1-q1',
    'geography-2022-ol-p1-q2',
    'geography-2022-ol-p1-q3',
    'geography-2022-ol-p1-q4',
    'geography-2022-ol-p1-q5',
    'geography-2022-ol-p1-q6',
    'geography-2022-ol-p1-q10',
    'geography-2022-ol-p1-q11',
    'geography-2022-ol-p1-q12',
    'geography-2022-ol-p2-q1b-route-i',
    'geography-2022-ol-p2-q1b-route-ii',
    'geography-2022-ol-p2-q1c',
    'geography-2022-ol-p2-q2a',
    'geography-2022-ol-p2-q2b-river-processes',
    'geography-2022-ol-p2-q2b-coastal-processes',
    'geography-2022-ol-p2-q2b-mass-movement',
    'geography-2022-ol-p2-q2c',
    'geography-2022-ol-p2-q3a',
    'geography-2022-ol-p2-q3b-onion-weathering-carbonation',
    'geography-2022-ol-p2-q3b-onion-weathering-freeze-thaw-action',
    'geography-2022-ol-p2-q3b-carbonation-freeze-thaw-action',
    'geography-2022-ol-p2-q3c-quarrying',
    'geography-2022-ol-p2-q3c-mining',
    'geography-2022-ol-p2-q3c-oil-gas-exploitation',
    'geography-2022-ol-p2-q3c-geothermal-energy-production',
    'geography-2022-ol-p2-q4a',
    'geography-2022-ol-p2-q4b',
    'geography-2022-ol-p2-q4c',
    'geography-2022-ol-p2-q5a',
    'geography-2022-ol-p2-q5b-the-factors-influencing-agricultur-the-importance-of-manufacturing-to',
    'geography-2022-ol-p2-q5b-the-factors-influencing-agricultur-the-reasons-why-tourists-are-attra',
    'geography-2022-ol-p2-q5b-the-importance-of-manufacturing-to-the-reasons-why-tourists-are-attra',
    'geography-2022-ol-p2-q5c',
    'geography-2022-ol-p2-q6a',
    'geography-2022-ol-p2-q6b',
    'geography-2022-ol-p2-q6c',
    'geography-2022-ol-p2-q7b',
    'geography-2022-ol-p2-q7c',
    'geography-2022-ol-p2-q8a',
    'geography-2022-ol-p2-q8b',
    'geography-2022-ol-p2-q9a',
    'geography-2022-ol-p2-q9b',
    'geography-2022-ol-p2-q9c',
    'geography-2022-ol-p2-q10a',
    'geography-2022-ol-p2-q10b',
    'geography-2022-ol-p2-q11a',
    'geography-2022-ol-p2-q11b',
    'geography-2022-ol-p2-q12b',
    'geography-2022-ol-p2-q12c',
]
