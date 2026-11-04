"""Independent review ledger: Leaving Certificate Geography 2018 Ordinary Level.

Sources (English editions, harvested Paper Trail corpus; sizes and SHA-256
pinned in EXPECTED_SOURCES and the generated audit): the examination paper
LC005GLP000EV (32 pages; one booklet printed Part One, answered in it, and
Part Two), marking scheme LC005GLP000EV (40 pages), and the common Sligo
companions shared with Higher Level — the 1:50 000 map LC005CLP003EV and its
legend LC005CLPC00EV (both JPEGs) and the aerial photograph LC005CLP004EV (a
one-page PDF). Part One is 100 marks (any ten of twelve @ 10), Part Two 300
(three questions @ 100).

Visual sweep (every page rendered and read on 2026-10-13):
  Paper p1 cover and examiner's grid; p2-p11 Part One Questions 1-12 (p4
  holds Q3 and Q4, p9 Q9 and Q10); p12 Part Two instructions; p13 Section 1
  divider; p14-p22 Q1-Q6 (p14 and p19 open with their dividers); p23
  Section 2 divider; p24-p30 Electives Q7-Q12 (p24 and p27 open with their
  elective dividers; p28 holds 11A and 11B, p29 11C); p31 and p32 "There
  is no examination material on this page" (p32 the back cover).
  Scheme p1 cover; p2-p3 notes; p4-p5 Geographical Investigation
  (coursework) and its presentation marks; p6-p7 Part One table (Q1-Q5,
  Q6-Q12); p8 Part Two instructions and Section 1 divider; p9-p34 Q1-Q12;
  p35 investigation topics; p36 Irish-language bonus marks; p37-p39
  printed "Blank Page"; p40 back cover.
  Companions: Sligo map extract; OS legend sheet; oblique aerial photograph
  of Sligo.

Boundaries and tariffs follow the 2019 Ordinary ledger: every priced roman
is a task, Q1's lettered true/false statements included; a matching table
under ONE printed instruction stays one task with a criterion per scheme
row, in the printed row order: Q1 Heat and pressure=C, Sedimentary rock=B,
Igneous rock=A; Q2 Focus=C, Epicentre=A, Fault line=D, Shock waves=B; Q3
Scree=D, Moraine=A, Calcite=B, Alluvium=E, Sand spit=C; Q4 The Paris
Basin=B, The Mediterranean=D, Ennis=E, Catalonia=A, South Wales
coalfields=C; Q5 Sea arch=D, Corrie/Cirque/Tarn=C, Interlocking spur=A,
Arete=B; Q11 prints sections A-E, priced (i)-(v) in the scheme; Part Two
1A(i) Soil creep B, Avalanche A, Rock fall D, Mudflow C; 2A(i) pushing
together Convergent, sliding past Transform, pulling apart Divergent. 7B's
"mass tourism or footloose industry" runs through three romans and the
scheme marks either alike, so each roman is one card with the printed
wording.

Tariffs as printed: twelve parts carry 40 marks (1C, 2B, 3B, 4B, 5C, 6B,
7B, 8B, 9B, 10C, 11C, 12C) and the rest 30. Scheme as printed: 1C(i)
prices three statements "@ 4m + 3m + 3m" (mark to the benefit of the
candidate); 4B(iii) reads "One challenged described"; both are carried
as printed.
"""

from geography_review import (
    Criterion, Lift, Route, SchemeSlice, Task, pool, fixed, slug, srp, steps, sums,
)

YEAR = 2018
LEVEL = 'ordinary'
PAPER_PAGES = {1: 32, 2: 32}
SCHEME_PAGES = 40
_FORTY = {'1C', '2B', '3B', '4B', '5C', '6B', '7B', '8B', '9B', '10C', '11C', '12C'}
QUESTION_TARIFFS = {1: {str(n): 10 for n in range(1, 13)},
                    2: {f'{n}{x}': (40 if f'{n}{x}' in _FORTY else 30)
                        for n in range(1, 13) for x in 'ABC'}}

EXPECTED_SOURCES = {
    'paper1': ('LC005GLP000EV.pdf', 1700593),
    'paper2': ('LC005GLP000EV.pdf', 1700593),
    'scheme': ('LC005GLP000EV.pdf', 389474),
    'map': ('LC005CLP003EV.jpg', 11172454),
    'legend': ('LC005CLPC00EV.jpg', 4184180),
    'aerial': ('LC005CLP004EV.pdf', 6573219),
}

_PAPER = {1: 'cover and examiner grid', **{p: 'question' for p in range(2, 12)},
          12: 'Part Two instructions', 13: 'section divider', **{p: 'question' for p in range(14, 23)},
          23: 'section divider', **{p: 'question' for p in range(24, 31)},
          31: 'no examination material', 32: 'back cover'}
PAGE_REVIEW = {
    # One booklet printed both parts.
    'paper1': _PAPER, 'paper2': _PAPER,
    'scheme': {1: 'cover', 2: 'notes', 3: 'notes', 4: 'geographical investigation (coursework)',
               5: 'presentation marks (coursework)', 6: 'Part One table', 7: 'Part One table',
               8: 'Part Two instructions and section divider',
               **{p: 'Part Two allocation' for p in range(9, 35)},
               35: 'investigation topics', 36: 'Irish-language bonus marks',
               37: 'blank', 38: 'blank', 39: 'blank', 40: 'back cover'},
}

EXPECTED_SELECTION_SCAN = [
    [1, 2, 'attempt any ten'], [1, 12, 'attempt three'], [1, 13, 'attempt two'], [1, 14, 'attempt one'],
    [1, 17, 'answer (i) or (ii)'], [1, 17, 'any two'], [1, 17, 'any two'], [1, 17, 'one of the following'],
    [1, 18, 'one of the following'],
    [1, 19, 'attempt one'],
    [1, 21, 'any two'],
    [1, 22, 'any two'],
    [1, 23, 'attempt one'],
    [1, 26, 'any two'],
    [1, 27, 'any two'],
    [1, 30, 'any three'],
]
SELECTION_REVIEW = [
    {'scan': [[1, 2, 'attempt any ten'], [1, 12, 'attempt three'], [1, 13, 'attempt two'], [1, 14, 'attempt one'],
              [1, 19, 'attempt one'], [1, 23, 'attempt one']],
     'kind': 'exam-attempt-rule',
     'reason': 'Part One any ten of twelve and Part Two three questions (one of Q1-3, one of Q4-6, one elective) are attempt rules; every question is carded.'},
    {'scan': [[1, 17, 'answer (i) or (ii)']], 'kind': 'closed-route',
     'reason': '2B: (i) or (ii) -> two routes, each with its own scheme allocation. 1B(iii) prints "igneous rocks ... or ... metamorphic rocks" under one allocation -> two routes.'},
    {'scan': [[1, 17, 'one of the following']], 'kind': 'closed-choose-one',
     'reason': '2C: one of four printed rock-cycle activities -> four routes.'},
    {'scan': [[1, 18, 'one of the following']], 'kind': 'closed-choose-one',
     'reason': '3C: one of three printed surface processes -> three routes.'},
    {'scan': [[1, 21, 'any two'], [1, 22, 'any two'], [1, 30, 'any three']], 'kind': 'choose-n-one-card',
     'reason': '5C any two of three printed activities, 6B(ii) any two of three printed factors and 12C any three of four printed urban problems -> one card each with every printed item (choice is not a route).'},
    {'scan': [[1, 17, 'any two'], [1, 17, 'any two'], [1, 26, 'any two'], [1, 27, 'any two']],
     'kind': 'open-response',
     'reason': 'No printed pool: 2B(i) any two landforms and 2B(ii) any two mass movement processes (the scheme prices two @ 20m); 9B(i) any two EU policies; 10B(i) any two land-uses.'},
]

P1, P2 = 1, 2
ID = 'geography-2018-ol-'
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

# ---------------------------------------------------------------- Part One --
TICK = 'Tick the correct box.'
TF1 = L(2, '(ii) State whether each of the following statements is true or false.')
PART_ONE = romans('1', P1, 2, L(2, 'Rock Cycle', nth=0),
                  (L(2, 'Examine the diagram of the rock cycle above and answer each of the following questions.'),),
                  ID + 'p1-q1', ('page',), [
    ('(i)', 6, L(2, '(i) Match each of the letters on the rock cycle A, B and C with the stage',
                 'most associated with it.'),
     S(6, 'Q1.(i)', 'Q.1(ii)'), rows(['Q1.(i) · C · 2m', '=B · 2m', '=A · 2m']), '0-1', RW,
     (L(2, 'Heat and pressure'), L(2, 'Sedimentary rock'), L(2, 'Igneous rock'))),
    ('(ii)(a)', 2, (TF1, L(2, '(a) Marble is an example of a metamorphic rock.')),
     S(6, 'Q.1(ii)', 'True · 2m · Total'), (fixed('Statement (a)', 2, 'Q.1(ii) · True · 2m'),), '0-1', RW),
    ('(ii)(b)', 2, (TF1, L(2, '(b) Fossils can be found in sedimentary rocks.')),
     S(6, 'True · 2m · Total', 'Q.2(i)'), (fixed('Statement (b)', 2, 'True · 2m · Total 10m'),), '0-1', RW),
])
PART_ONE += romans('2', P1, 3, L(3, 'Earthquakes'),
                   (L(3, 'Examine the diagram of an earthquake above and answer each of the following questions.'),),
                   ID + 'p1-q2', ('page',), [
    ('(i)', 8, L(3, '(i) Match each of the letters A, B, C and D on the diagram above with the correct term',
                 'table below.'),
     S(6, 'Q.2(i)', 'Richter'), rows(['Q.2(i) · C · 2m', '=A · 2m', '=D · 2m', '=B · 2m']), '0-7', EV,
     (L(3, 'Focus'), L(3, 'Epicentre'), L(3, 'Fault line'), L(3, 'Shock waves'))),
    ('(ii)', 2, L(3, '(ii) Name the scale used to measure the force/magnitude of an earthquake.'),
     S(6, 'Richter', 'Q.3'),
     (fixed('Scale', 2, ('Richter Scale/Mercalli or any', 'Q.2(ii) · 2m · Total 10m', 'valid scale')),), '0-7', EV),
])
PART_ONE += [
    T('p1-3', P1, '3', '', 10, 4, L(4, 'Physical Processes'),
      (L(4, 'Match the physical process with the term or feature most associated with it', 'in the table below.'),),
      (S(6, 'Q.3', 'Q.4'),), rows(['Q.3 · D · 2m', '=A · 2m', '=B · 2m', '=E · 2m', 'C · 2m · Total 10m']),
      '0-4', PS_SURFACE + RW, ID + 'p1-q3', ('page',),
      row_labels=(L(4, 'Scree'), L(4, 'Moraine'), L(4, 'Calcite'), L(4, 'Alluvium'), L(4, 'Sand spit'))),
    T('p1-4', P1, '4', '', 10, 4, L(4, 'Regions'),
      (L(4, 'Match the description of a region with the example of the region', 'in the table below.'),),
      (S(6, 'Q.4', 'Q.5(i)'),), rows(['Q.4 · B · 2m', '=D · 2m', '=E · 2m', '=A · 2m', 'C · 2m · Total 10m']),
      '1-0', IRL + EURO, ID + 'p1-q4', ('page',),
      row_labels=(L(4, 'The Paris Basin'), L(4, 'The Mediterranean'), L(4, 'Ennis, Co. Clare'),
                  L(4, 'Catalonia, Spain'), L(4, 'South Wales coalfields'))),
]
PART_ONE += romans('5', P1, 5, L(5, 'Surface Processes'),
                   (L(5, 'Examine the photographs above and answer each of the following questions.'),),
                   ID + 'p1-q5', ('page',), [
    ('(i)', 8, L(5, '(i) Match each of the photographs A, B, C and D with the landform', 'best matches it.'),
     S(6, 'Q.5(i)', 'Q.5(ii)'), rows(['Q.5(i) · D · 2m', '=C · 2m', '=A · 2m', '=B · 2m']), '0-4', PS_SURFACE,
     (L(5, 'Sea arch'), L(5, 'Corrie/Cirque/Tarn'), L(5, 'Interlocking spur'), L(5, 'Arête'))),
    ('(ii)', 2, L(5, '(ii) State whether processes of erosion or processes of deposition are most associated',
                  'table above.'),
     S(6, 'Q.5(ii)', None), (fixed('Erosion or deposition', 2, 'Q.5(ii) · Erosion · 2m · Total 10m'),),
     '0-4', PS_SURFACE),
])
PART_ONE += romans('6', P1, 6, L(6, 'Weather Chart'),
                   (L(6, 'Examine the weather chart and extract above and answer each of the following',
                      'questions.'),),
                   ID + 'p1-q6', ('page',), [
    ('(i)', 2, L(6, '(i) What type of weather front did Hurricane Ophelia originate from?'),
     S(7, 'Q.6', '(ii) 14 October'), (fixed('Weather front', 2, 'Q.6 · (i) Cold front · 2m'),), '2-7', WEATHER),
    ('(ii)', 2, L(6, '(ii) Where and when did hurricane Ophelia intensify into a major hurricane?'),
     S(7, '(ii) 14 October', '(iii) High'),
     (fixed('When', 1, '(ii) 14 October · 1m'), fixed('Where', 1, 'Azores/South of the Azores · 1m')),
     '2-7', WEATHER),
    ('(iii)', 2, L(6, '(iii) What does the letter H on the weather chart indicate?'),
     S(7, '(iii) High', '(iv) Calm'), (fixed('Meaning of H', 2, '(iii) High pressure/anticyclone · 2m'),),
     '2-7', WEATHER),
    ('(iv)', 2, (L(6, '(iv) In the weather chart above, is the weather in southern Europe wet and windy or', TICK),
                 L(6, 'Wet and windy'), L(6, 'Calm and dry')),
     S(7, '(iv) Calm', '(v) Appropriate'), (fixed('Weather', 2, '(iv) Calm and dry · 2m'),), '2-7', WEATHER),
    ('(v)', 2, L(6, '(v) In the box below, draw the weather chart symbol for a cold front.'),
     S(7, '(v) Appropriate', 'Q.7'), (fixed('Symbol', 2, '(v) Appropriate symbol · 2m · Total 10m'),),
     '2-7', WEATHER),
])
PART_ONE += romans('7', P1, 7, L(7, 'Human Processes'),
                   (L(7, 'Examine the table above showing the number of daily Irish speakers',
                      'Answer each of the following questions.'),),
                   ID + 'p1-q7', ('page',), [
    ('(i)', 2, L(7, '(i) Name the Gaeltacht area with the greatest number of daily Irish speakers in 2016.'),
     S(7, 'Q.7', '(ii) Meath'), (fixed('Gaeltacht area', 2, 'Q.7 · (i) Galway County · 2m'),), '2-0', GRAPH),
    ('(ii)', 2, L(7, '(ii) Name the Gaeltacht area with the least number of daily Irish speakers in 2011.'),
     S(7, '(ii) Meath', '(iii) 1,118'), (fixed('Gaeltacht area', 2, '(ii) Meath County · 2m'),), '2-0', GRAPH),
    ('(iii)', 2, L(7, '(iii) What was the decline in the number of daily Irish speakers in County Donegal',
                   '2011 and 2016?'),
     S(7, '(iii) 1,118', '(iv) Waterford'), (fixed('Decline', 2, '(iii) 1,118 · 2m'),), '2-0', GRAPH),
    ('(iv)', 2, L(7, '(iv) Name the Gaeltacht area which experienced the greatest increase in the number of',
                  '2011 and 2016.'),
     S(7, '(iv) Waterford', '(v) Valid answer'), (fixed('Gaeltacht area', 2, '(iv) Waterford County · 2m'),),
     '2-0', GRAPH),
    ('(v)', 2, L(7, '(v) Suggest one way that the Irish government could assist in increasing the number of',
                 'daily Irish speakers.'),
     S(7, '(v) Valid answer', 'Q.8'), (fixed('Suggestion', 2, '(v) Valid answer · 2m · Total 10m'),), '1-3', IRL),
])
PART_ONE += romans('8', P1, 8, L(8, 'Weather Statistics'),
                   (L(8, 'Examine the climate graph above and answer each of the following questions.'),),
                   ID + 'p1-q8', ('page',), [
    ('(i)', 2, L(8, '(i) Which month experienced the lowest mean temperature?'),
     S(7, 'Q.8', '(ii) August'), (fixed('Month', 2, 'Q.8 · (i) February · 2m'),), '2-7', GRAPH + WEATHER),
    ('(ii)', 2, L(8, '(ii) Which month experienced the highest mean temperature?'),
     S(7, '(ii) August', '(iii) 140'), (fixed('Month', 2, '(ii) August · 2m'),), '2-7', GRAPH + WEATHER),
    ('(iii)', 2, L(8, '(iii) What was the highest monthly rainfall level (mm) experienced?'),
     S(7, '(iii) 140', '(iv) 5'), (fixed('Rainfall', 2, '(iii) 140 (mm) · 2m'),), '2-7', GRAPH + WEATHER),
    ('(iv)', 2, L(8, '(iv) How many months had a rainfall level higher than 80 mm?'),
     S(7, '(iv) 5', '(v) Rain gauge'), (fixed('Number of months', 2, '(iv) 5 · 2m'),), '2-7', GRAPH + WEATHER),
    ('(v)', 2, L(8, '(v) Name the weather instrument used to measure rainfall.'),
     S(7, '(v) Rain gauge', 'Q.9'), (fixed('Instrument', 2, '(v) Rain gauge · 2m · Total 10m'),), '2-7', WEATHER),
])
Q9S = (L(9, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper and answer',
         'following questions.', nth=0),)
Q10S = (L(9, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper and answer',
          'following questions.', nth=1),)
PART_ONE += romans('9', P1, 9, L(9, 'Ordnance Survey Map', nth=0), Q9S, ID + 'p1-q9', ('map', 'legend'), [
    ('(i)', 5, (L(9, '(i) What is the length of the railway line from the train station at G 686 361', TICK),
                L(9, '1.4 km'), L(9, '0.9 km')),
     S(7, 'Q.9', '(ii) 597'), (fixed('Length', 5, 'Q.9 · (i) 1.4km · 5m'),), '2-6', MAP),
    ('(ii)', 5, L(9, '(ii) What is the height in metres of the highest point on the map?'),
     S(7, '(ii) 597', 'Q.10(i)'), (fixed('Height', 5, '(ii) 597 (m) · 5m · Total 10m'),), '2-6', MAP),
])
PART_ONE += romans('10', P1, 9, L(9, 'Ordnance Survey Map', nth=1), Q10S, ID + 'p1-q10', ('map', 'legend'), [
    ('(i)', 6, L(9, '(i) Name the features which can be found at each of the following grid references:'),
     S(7, 'Q.10(i)', 'Q.10(ii)'), rows(['Q.10(i) · Viewpoint · 2m', 'Parking · 2m', 'Crannóg · 2m']), '2-6', MAP,
     (L(9, 'G 743 359'), L(9, 'G 681 421'), L(9, 'G 736 432'))),
    ('(ii)', 2, L(9, '(ii) If you were to walk the Benbulben Walk from the Mound at G 673 461',
                  'would you be walking?'),
     S(7, 'Q.10(ii)', 'Q.10 (iii)'), (fixed('Direction', 2, 'Q.10(ii) · North East · 2m'),), '2-6', MAP),
    ('(iii)', 2, L(9, '(iii) In the box below, draw the Ordnance Survey map symbol for a County Boundary.'),
     S(7, 'Q.10 (iii)', 'Q.11'), (fixed('Symbol', 2, 'Q.10 (iii) · Appropriate symbol · 2m · Total 10m'),),
     '2-6', MAP),
])
PART_ONE += [
    T('p1-11', P1, '11', '', 10, 10, L(10, 'Aerial Photograph'),
      (L(10, 'Examine the aerial photograph accompanying this paper, and the sections from it below.'),
       L(10, 'Give the location of each of the sections from the aerial photograph', 'etc.).')),
      (S(7, 'Q.11', 'Q.12'),),
      (fixed('A', 2, 'Q.11 · (i) Left middleground · 2m'), fixed('B', 2, '(ii) Left foreground · 2m'),
       fixed('C', 2, '(iii) Centre foreground · 2m'), fixed('D', 2, '(iv) Left background · 2m'),
       fixed('E', 2, '(v) Right background · 2m · Total 10m')),
      '2-8', AER, ID + 'p1-q11', ('page', 'aerial')),
]
PART_ONE += romans('12', P1, 11, L(11, 'Tourism'),
                   (L(11, 'Examine the table above and answer each of the following questions.'),),
                   ID + 'p1-q12', ('page',), [
    ('(i)', 2, L(11, '(i) From which area of residence did the least number of visitors to Ireland come from',
                 'in 2014?'),
     S(7, 'Q.12', '(ii) Holiday'), (fixed('Area of residence', 2, 'Q.12 · (i) Italy · 2m'),), '2-0', GRAPH),
    ('(ii)', 2, L(11, '(ii) What was the main reason for the majority of people visiting Ireland in 2016?'),
     S(7, '(ii) Holiday', '(iii) Great'), (fixed('Reason', 2, '(ii) Holiday/leisure/recreation · 2m'),),
     '2-0', GRAPH),
    ('(iii)', 2, L(11, '(iii) From which area of residence did the number of visits increase the most between',
                   '2014 and 2016?'),
     S(7, '(iii) Great', '(iv) Tertiary'), (fixed('Area of residence', 2, '(iii) Great Britain · 2m'),),
     '2-0', GRAPH),
    ('(iv)', 2, L(11, '(iv) State whether tourism is a primary, secondary or tertiary economic activity.'),
     S(7, '(iv) Tertiary', '(v) Any valid'), (fixed('Economic activity', 2, '(iv) Tertiary · 2m'),), '3-0', ECON),
    ('(v)', 2, L(11, '(v) Name one Irish international ferry port and one Irish international airport.'),
     S(7, '(v) Any valid', None),
     (fixed('Ferry port and airport', 2, ('(v) Any valid international ferry', '1m + 1m · Total 10m',
                                          'port and international airport'), (0, 1, 2)),), '1-4', IRL),
])


# ---------------------------------------------------------------- Part Two --
def sketch(page, title, prompt, scheme_page, card_id, topic, atlas, sources, proportions, bullets):
    item = sums((0, 1, 3), (0, 2))
    return T(f'p2-{card_id.rsplit("-q", 1)[1]}', P2, card_id.rsplit('-q', 1)[1].upper(), '', 30, page,
             title, (prompt,), (S(scheme_page, 'Sketch Outline:', 'Total 30m'),),
             (fixed('Limits/frame', 1, ('Sketch Outline:', 'imits/')),
              fixed(f'Proportions ({proportions})', 2, f'Proportions ({proportions}) · 2m'),
              fixed('Overall impression', 2, '2m graded (2/1/0)', (0, 1, 2)),
              *(Criterion(f'Item {n}', 5, item, 'exact',
                          ('Five items shown and labelled as follows:', 'Showing · 3m graded (3/1/0)',
                           'Labelled · 2m')) for n in range(1, 6))),
             topic, atlas, card_id, sources,
             row_labels=(None, None, None, *(L(page, b) for b in bullets)))


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
SURFACE = ('River processes', 'Coastal processes', 'Mass movement processes.')
ROCK = ('Quarrying', 'Mining', 'Oil/Gas exploitation', 'Geothermal energy production.')

PART_TWO = romans('1A', P2, 14, L(14, 'Mass Movement'),
                  (L(14, 'Examine the photographs above and answer each of the following questions.'),),
                  ID + 'p2-q1a', ('page',), [
    ('(i)', 12, L(14, '(i) In your answer book, match each of the photographs A, B, C and D', 'Mudflow.'),
     S(9, '• Soil creep', '(ii) · Name one'),
     (fixed('Row 1', 3, '• Soil creep · B · 3m'), fixed('Row 2', 3, '• Avalanche · A · 3m'),
      fixed('Row 3', 3, '• Rock fall · D · 3m'), fixed('Row 4', 3, '• Mudflow. · C · 3m')), '0-8', RW,
     (L(14, 'Soil creep'), L(14, 'Avalanche'), L(14, 'Rock fall'), L(14, 'Mudflow'))),
    ('(ii)', 6, L(14, '(ii) Name one example of a fast mass movement process and one example of a slow',
                  'mass movement process.'),
     S(9, '(ii) · Name one', '(iii) · Explain briefly'),
     (fixed('Fast mass movement', 3, 'One valid fast mass movement · 3m'),
      fixed('Slow mass movement', 3, 'One valid slow mass movement · 3m')), '0-8', RW),
    ('(iii)', 6, L(14, '(iii) Explain briefly how slope affects the rate of mass movement.'),
     S(9, '(iii) · Explain briefly', '(iv) · Explain briefly'),
     (srp3('Brief explanation', 2, 'Brief explanation two SRP’s @ 3m each · 6m'),), '0-8', RW),
    ('(iv)', 6, L(14, '(iv) Explain briefly how water affects the rate of mass movement.'),
     S(9, '(iv) · Explain briefly', 'Total 30m'),
     (srp3('Brief explanation', 2, 'Brief explanation two SRP’s @ 3m each · 6m'),), '0-8', RW),
])
Q1BI = L(15, '(i) Name one example of an igneous rock and state one location where it can be', 'found.')
PART_TWO += romans('1B', P2, 15, L(15, 'Rocks'), (), ID + 'p2-q1b', (), [
    ('(i)', 6, Q1BI, S(10, '(i) · Name one example of an igneous', '(ii) · Name one example'),
     (fixed('Igneous rock named', 3, 'Igneous rock named · 3m'), fixed('Location', 3, 'Location · 3m')), '0-1', RW),
    ('(ii)', 6, L(15, '(ii) Name one example of a metamorphic rock and state one location where it can be', 'found.'),
     S(10, '(ii) · Name one example', '(iii) · Describe'),
     (fixed('Metamorphic rock named', 3, 'Metamorphic rock named · 3m'), fixed('Location', 3, 'Location · 3m')),
     '0-1', RW),
])
IGNEOUS = 'Describe and explain how igneous rocks are formed.'
METAMORPHIC = 'Describe and explain how metamorphic rocks are formed.'
PART_TWO += [
    T('p2-1b-iii', P2, '1B', '(iii)', 18, 15, L(15, 'Rocks'),
      (L(15, '(iii) Describe and explain how igneous rocks are formed.', METAMORPHIC),),
      (S(10, '(iii) · Describe', 'Total 30m'),),
      (srp3('Description/explanation', 6, 'Description/Explanation 6 SRP’s @ 3m each · 18m'),),
      '0-1', RW, ID + 'p2-q1b-iii-igneous-rocks',
      routes=(Route('igneous-rocks', 'Igneous rocks', ID + 'p2-q1b-iii-igneous-rocks', False, ((IGNEOUS, 'igneous'),)),
              Route('metamorphic-rocks', 'Metamorphic rocks', ID + 'p2-q1b-iii-metamorphic-rocks', False,
                    ((METAMORPHIC, 'metamorphic'),)))),
]
PART_TWO += romans('1C', P2, 15, L(15, 'Volcanoes'), (), ID + 'p2-q1c', (), [
    ('(i)', 10, L(15, '(i) State what is meant by each of the following types of volcano:', 'Dormant volcano.'),
     S(10, '(i) · State what is meant', '(ii) · Discuss the positive'),
     (fixed('Statement 1', 4, 'Three statements @ 4m + 3m + 3m · 10m'),
      fixed('Statement 2', 3, 'Three statements @ 4m + 3m + 3m · 10m'),
      fixed('Statement 3', 3, 'Three statements @ 4m + 3m + 3m · 10m')), '0-7', EV),
    ('(ii)', 15, L(15, '(ii) Discuss the positive effects of volcanoes.'),
     S(10, '(ii) · Discuss the positive', '(iii) · Discuss the negative'),
     (srp3('Discussion', 5, 'Discussion 5 SRP’s @ 3m each · 15m'),), '0-7', EV),
    ('(iii)', 15, L(15, '(iii) Discuss the negative effects of volcanoes.'),
     S(10, '(iii) · Discuss the negative', 'Total 40m'),
     (srp3('Discussion', 5, 'Discussion 5 SRP’s @ 3m each · 15m'),), '0-7', EV),
])

PART_TWO += romans('2A', P2, 16, L(16, 'Plate Boundaries'),
                   (L(16, 'Examine the diagrams above and answer each of the following questions.'),),
                   ID + 'p2-q2a', ('page',), [
    ('(i)', 12, L(16, '(i) In your answer book, match each of the plate boundaries named above',
                  'Plates pulling apart.'),
     S(11, '• Plates pushing together', '(ii) · State what'),
     (fixed('Row 1', 4, '• Plates pushing together · Convergent · 4m'),
      fixed('Row 2', 4, '• Plates sliding past each other · Transform · 4m'),
      fixed('Row 3', 4, '• Plates pulling apart. · Divergent · 4m')), '0-0', PS,
     (L(16, 'Plates pushing together'), L(16, 'Plates sliding past each other'), L(16, 'Plates pulling apart'))),
    ('(ii)', 3, L(16, '(ii) State what is meant by the term plate.'),
     S(11, '(ii) · State what', '(iii) · Explain briefly'), (fixed('Statement', 3, 'Valid statement · 3m'),),
     '0-0', PS),
    ('(iii)', 6, L(16, '(iii) Explain briefly how plates move.'),
     S(11, '(iii) · Explain briefly', '(iv) · At which'),
     (srp3('Brief explanation', 2, 'Brief explanation two SRP’s @3m each · 6m'),), '0-0', PS),
    ('(iv)', 3, L(16, '(iv) At which of the plate boundaries named on the diagram above do ocean ridges', 'form?'),
     S(11, '(iv) · At which', '(v) · At which'), (fixed('Plate boundary', 3, 'Divergent · 3m'),), '0-0', PS),
    ('(v)', 3, L(16, '(v) At which of the plate boundaries named on the diagram above do fold mountains', 'form?'),
     S(11, '(v) · At which', '(vi) · Name one'), (fixed('Plate boundary', 3, 'Convergent · 3m'),), '0-0', PS),
    ('(vi)', 3, L(16, '(vi) Name one example of an ocean ridge or name one example of a range of',
                  'fold mountains.'),
     S(11, '(vi) · Name one', 'Total 30m'),
     (fixed('Example', 3, 'Valid example (ocean ridge or range of fold mountains) · 3m'),), '0-0', PS),
])
PART_TWO += [
    T('p2-2b', P2, '2B', '', 40, 17, L(17, 'Landform Development'),
      (L(17, '(i) Explain, with the aid of diagrams, the formation of any two landforms.'),),
      (S(12, 'Formation of any two landforms @ 20m each.', 'Total 40m'),),
      two_of('Landform', 20, 'Formation of any two landforms @ 20m each.', 'For each landform:',
             ('Landform named · 1m', 'Diagram(s) two aspects @ 2m each · 4m',
              'Formation explained 5 SRP’s @ 3m each · 15m'),
             ((0, 1), (0, 2, 4), steps(15, 3))),
      '0-4', PS_SURFACE, ID + 'p2-q2b-route-i',
      routes=(
          Route('route-i', 'Route (i)', ID + 'p2-q2b-route-i', False),
          Route('route-ii', 'Route (ii)', ID + 'p2-q2b-route-ii', False,
                prompt=(L(17, '(ii) Describe and explain any two processes of mass movement.'),),
                scheme=(S(12, 'Any two processes @ 20m each', 'Total 40m'),),
                criteria=two_of('Process', 20, 'Any two processes @ 20m each', 'For each process:',
                                ('Process stated · 2m', 'Description / Explanation 6 SRP’s @ 3m each · 18m'),
                                ((0, 2), steps(18, 3))),
                topic='0-8', atlas=RW),
      )),
    T('p2-2c', P2, '2C', '', 30, 17, L(17, 'Human Interaction with the Rock Cycle'),
      (L(17, 'Discuss how humans interact with the rock cycle with reference to one of the following:',
         'Geothermal energy production.'),),
      (S(13, 'Discussion 10 SRP', 'Total 30m'),),
      (srp3('Discussion', 10, 'Discussion 10 SRP’s @ 3m each · 30m'),),
      '0-6', RW, ID + 'p2-q2c-quarrying', routes=bullet_routes('p2-q2c-', ROCK)),
]

PART_TWO.append(sketch(
    18, L(18, 'Ordnance Survey Map'),
    L(18, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper.',
      'The built up area of Sligo.'),
    14, ID + 'p2-q3a', '2-6', MAP + SEA + RIVERS, ('map', 'legend'), 'Portrait',
    ('The entire coastline', 'The Drumcliff River', 'Glencar Lough', 'The area of Cope’s Mountain above 200 metres',
     'The built up area of Sligo')))
PART_TWO += romans('3B', P2, 18, L(18, 'Karst Landscapes'), (), ID + 'p2-q3b', (), [
    ('(i)', 4, L(18, '(i) Name one example of a karst landscape.'),
     S(15, '(i) · Name one example of a karst', '(ii) · Explain, with the aid'),
     (fixed('Karst landscape named', 4, 'Karst landscape named · 4m'),), '0-3', KARST),
    ('(ii)', 18, L(18, '(ii) Explain, with the aid of a diagram, how one surface feature', 'was formed.'),
     S(15, '(ii) · Explain, with the aid', '(iii) · Explain, with the aid'),
     (fixed('Feature named', 2, 'Feature named · 2m'),
      fixed('Diagram', 4, 'Diagram(s) two aspects @ 2m each · 4m', (0, 2, 4)),
      srp3('Formation explained', 4, 'Formation explained 4 SRP’s @ 3m each · 12m')), '0-3', KARST),
    ('(iii)', 18, L(18, '(iii) Explain, with the aid of a diagram, how one underground feature', 'was formed.'),
     S(15, '(iii) · Explain, with the aid', 'Total 40m'),
     (fixed('Feature named', 2, 'Feature named · 2m'),
      fixed('Diagram', 4, 'Diagram(s) two aspects @ 2m each · 4m', (0, 2, 4)),
      srp3('Formation explained', 4, 'Formation explained 4 SRP’s @ 3m each · 12m')), '0-3', KARST),
])
PART_TWO.append(T(
    'p2-3c', P2, '3C', '', 30, 18, L(18, 'Human Interaction with Surface Processes'),
    (L(18, 'Explain how humans interact with one of the following surface processes:', 'Mass movement processes.'),),
    (S(15, 'Interaction identified · 3m', 'Total 30m'),),
    (fixed('Interaction identified', 3, 'Interaction identified · 3m'),
     srp3('Description/explanation', 9, 'Description / Explanation 9 SRP’s @ 3m each · 27m')),
    '0-6', RIVERS, ID + 'p2-q3c-river-processes',
    routes=bullet_routes('p2-q3c-', SURFACE, atlas=dict(zip(SURFACE, (RIVERS, SEA, RW))))))

PART_TWO.append(T(
    'p2-4a', P2, '4A', '', 30, 19, L(19, 'Map Skills'),
    (L(19, 'Draw a sketch map of a Continental / Sub-Continental region (not in Europe) that you',
       '(upland or lowland) in this region.'),),
    (S(16, 'Outline of Region', 'Total 30m'),),
    (fixed('Outline of region', 6, 'Outline of Region · 6m graded (6/4/2/0)', (0, 2, 4, 6)),
     Criterion('Urban area 1', 6, NAMED_SHOWN, 'exact', ('Urban area 1 · Named · 2m', f'={SHOWN}@0')),
     Criterion('Urban area 2', 6, NAMED_SHOWN, 'exact', ('Urban area 2 · Named · 2m', f'={SHOWN}@1')),
     Criterion('River', 6, NAMED_SHOWN, 'exact', ('River · Named · 2m', f'={SHOWN}@2')),
     Criterion('Relief (upland/lowland)', 6, NAMED_SHOWN, 'exact',
               ('Relief (upland/lowland) · Named · 2m', f'={SHOWN}@3'))),
    '1-6', CONT, ID + 'p2-q4a'))
Q4BS = (L(19, 'Answer each of the following questions with reference to an Irish region that you have',
          'studied.'),)
Q4BI = L(19, '(i) Name one example of a secondary economic activity in this region.')
PART_TWO += romans('4B', P2, 19, L(19, 'Secondary Economic Activity in an Irish Region'), Q4BS, ID + 'p2-q4b', (), [
    ('(i)', 4, Q4BI, S(17, '(i) · Name one example', '(ii) · Explain the advantages'),
     (fixed('Secondary economic activity named', 4, 'Example of secondary economic activity · 4m'),), '1-4', IRL),
    ('(ii)', 27, L(19, '(ii) Explain the advantages that this region has for the development of this secondary',
                   'economic activity.'),
     S(17, '(ii) · Explain the advantages', '(iii) · Describe one'),
     (srp3('Advantages explained', 9, 'Advantages explained 9 SRP’s @ 3m each · 27m'),), '1-4', IRL, (), (Q4BI,)),
    ('(iii)', 9, L(19, '(iii) Describe one challenge faced by this secondary economic activity in this region.'),
     S(17, '(iii) · Describe one', 'Total 40m'),
     (srp3('One challenge described', 3, 'One challenged described 3 SRP’s @ 3m each · 9m'),), '1-4', IRL, (),
     (Q4BI,)),
])
PART_TWO.append(T(
    'p2-4c', P2, '4C', '', 30, 19, L(19, 'Urban Growth in a European Region'),
    (L(19, 'Discuss the reasons for the growth of an urban area in a European region', 'that you have studied.'),),
    (S(17, 'Discussion 10 SRP', 'Total 30m'),),
    (srp3('Discussion', 10, 'Discussion 10 SRP’s @ 3m each · 30m'),),
    '1-5', EURO + URB, ID + 'p2-q4c'))

PART_TWO += romans('5A', P2, 20, L(20, 'Irish Trade'),
                   (L(20, 'Examine the chart and table above and answer each of the following questions.'),),
                   ID + 'p2-q5a', ('page',), [
    ('(i)', 3, L(20, '(i) The greatest value of Irish fish was exported to which region in 2016?'),
     S(18, '(i) · The greatest', '(ii) · Explain briefly'), (fixed('Region', 3, 'European Union · 3m'),),
     '2-0', GRAPH),
    ('(ii)', 6, L(20, '(ii) Explain briefly one reason why the greatest value of Irish fish was exported to this',
                  'region.'),
     S(18, '(ii) · Explain briefly', '(iii) · The value'),
     (srp3('Brief explanation', 2, 'Brief explanation 2 SRP’s @ 3m each · 6m'),), '3-3', EU),
    ('(iii)', 3, L(20, '(iii) The value of Irish fish exports to which region underwent the greatest percentage',
                   '2015 and 2016?'),
     S(18, '(iii) · The value', '(iv) · Calculate'), (fixed('Region', 3, 'Asia · 3m'),), '2-0', GRAPH),
    ('(iv)', 6, L(20, '(iv) Calculate the difference (in millions of euro), between the value of fish exports to',
                  'in 2015.'),
     S(18, '(iv) · Calculate', '(v) · Explain briefly'), (fixed('Difference', 6, '300 (million euro) · 6m'),),
     '2-0', GRAPH),
    ('(v)', 6, L(20, '(v) Explain briefly one advantage of exports to the Irish economy.'),
     S(18, '(v) · Explain briefly', '(vi) · State two'),
     (srp3('Brief explanation', 2, 'Brief explanation 2 SRP’s @ 3m each · 6m'),), '3-0', ECON),
    ('(vi)', 6, L(20, '(vi) State two advantages that Ireland has for fishing.'),
     S(18, '(vi) · State two', 'Total 30m'),
     (fixed('Two advantages', 6, 'Two advantages stated @ 3m each · 6m', (0, 3, 6)),), '1-4', IRL),
])
ACTIVITIES = ('The factors influencing agriculture in the region', 'The importance of manufacturing to the region',
              'The reasons why tourists are attracted to the region.')
PART_TWO += [
    T('p2-5b', P2, '5B', '', 30, 21, L(21, 'Tertiary Economic Activities – European Region'),
      (L(21, 'Discuss the development of two tertiary economic activities in a European region',
         'that you have studied.'),),
      (S(18, 'Two activities named', 'Total 30m'),),
      (fixed('Two activities named', 6, 'Two activities named @ 3m each · 6m', (0, 3, 6)),
       srp3('Activity one discussed', 4, 'Activity One discussed 4 SRP’s @ 3m each · 12m'),
       srp3('Activity two discussed', 4, 'Activity Two discussed 4 SRP’s @ 3m each · 12m')),
      '1-5', EURO, ID + 'p2-q5b'),
    T('p2-5c', P2, '5C', '', 40, 21, L(21, 'Economic Activities – Continental / Sub-Continental Region'),
      (L(21, 'Explain any two of the following with reference to a Continental / Sub-Continental region',
         'The reasons why tourists are attracted to the region.'),),
      (S(19, 'Activity 1 explained', 'Total 40m'),),
      (srp3('Activity 1 explained', 7, 'Activity 1 explained 7 SRP’s @ 3m each · 21m'),
       srp3('Activity 2 explained', 6, 'Activity 2 explained 6 SRP’s @ 3m each · 18m'),
       fixed('Region named', 1, 'Region named · 1m')),
      '1-6', CONT, ID + 'p2-q5c', absorbs=pool(ID + 'p2-q5c-', ACTIVITIES, 2)[1]),
]

FACTORS_6B = ('Climate', 'Relief and soils', 'Markets.')
PART_TWO.append(T(
    'p2-6a', P2, '6A', '', 30, 22, L(22, 'Irish Region'),
    (L(22, 'Draw a sketch map of Ireland.', 'One named town or city in this region.'),),
    (S(20, 'Outline of Ireland', 'Total 30m'),),
    (fixed('Outline of Ireland', 6, 'Outline of Ireland · 6m graded (6/4/2/0)', (0, 2, 4, 6)),
     Criterion('Region', 6, NAMED_SHOWN, 'exact', ('Region · Named · 2m', f'={SHOWN}@0')),
     Criterion('Relief (upland/lowland)', 6, NAMED_SHOWN, 'exact',
               ('Relief (upland/lowland) · Named · 2m', f'={SHOWN}@1')),
     Criterion('River', 6, NAMED_SHOWN, 'exact', ('River · Named · 2m', f'={SHOWN}@2')),
     Criterion('Town/City', 6, NAMED_SHOWN, 'exact', ('Town/City · Named · 2m', f'={SHOWN}@3'))),
    '1-4', IRL, ID + 'p2-q6a'))
Q6BS = (L(22, 'Answer each of the following questions with reference to a European region (not in Ireland)',
          'that you have studied.'),)
PART_TWO += [
    T('p2-6b-i', P2, '6B', '(i)', 4, 22, L(22, 'Agriculture in a European Region'),
      (L(22, '(i) Name two examples of agricultural activity practiced in this region.'),),
      (S(20, '(i) · Name two examples', '(ii) · Discuss how'),),
      (fixed('Two examples', 4, 'Two examples named @ 2m each · 4m', (0, 2, 4)),),
      '1-5', EURO, ID + 'p2-q6b', (), Q6BS),
    T('p2-6b-ii', P2, '6B', '(ii)', 36, 22, L(22, 'Agriculture in a European Region'),
      (L(22, '(ii) Discuss how any two of the following factors influence the development of', 'Markets.'),),
      (S(20, '(ii) · Discuss how', 'Total 40m'),),
      (srp3('Factor 1', 6, 'Factor 1 discussed 6 SRP’s @ 3m each · 18m'),
       srp3('Factor 2', 6, 'Factor 2 discussed 6 SRP’s @ 3m each · 18m')),
      '1-5', EURO, ID + 'p2-q6b-ii', (), Q6BS, absorbs=pool(ID + 'p2-q6b-ii-', FACTORS_6B, 2)[1]),
]
PART_TWO += romans('6C', P2, 22, L(22, 'Concept of a Region'), (), ID + 'p2-q6c', (), [
    ('(i)', 15, L(22, '(i) Name an example of a core region and explain why this region is a core region.'),
     S(21, '(i) · Name an example', '(ii) · Name an example'),
     (fixed('Core region named', 3, 'Core region named · 3m'),
      srp3('Explanation', 4, 'Explanation 4 SRP’s @ 3m each · 12m')), '1-0', IRL + EURO),
    ('(ii)', 15, L(22, '(ii) Name an example of a peripheral region and explain why this region is a peripheral',
                   'region.'),
     S(21, '(ii) · Name an example', 'Total 30m'),
     (fixed('Peripheral region named', 3, 'Peripheral region named · 3m'),
      srp3('Explanation', 4, 'Explanation 4 SRP’s @ 3m each · 12m')), '1-0', IRL + EURO),
])

PART_TWO += romans('7A', P2, 24, L(24, 'Economic Activity – The Environment'),
                   (L(24, 'Examine the table above and answer each of the following questions.'),),
                   ID + 'p2-q7a', ('page',), [
    ('(i)', 24, L(24, '(i) Using graph paper, draw a suitable graph to illustrate this data.'),
     S(23, 'Graph paper', '(ii) · In your answer book'), GRAPH_OL, '2-0', GRAPH),
    ('(ii)', 6, L(24, '(ii) In your answer book, state two ways that greenhouse gas emissions can be', 'reduced.'),
     S(23, '(ii) · In your answer book', 'Total 30m'),
     (fixed('Two ways', 6, 'Two valid statements @ 3m each · 6m', (0, 3, 6)),), '3-4', ENV),
])
Q7BI = L(24, '(i) Name one example of a developed economy that you have studied.')
PART_TWO += romans('7B', P2, 24, L(24, 'Economic Development – Developed Economy'), (), ID + 'p2-q7b', (), [
    ('(i)', 4, Q7BI, S(24, '(i) · Name one example of a developed', '(ii) · Explain the reasons'),
     (fixed('Developed economy named', 4, 'Developed economy named · 4m'),), '3-0', ECON),
    ('(ii)', 18, L(24, '(ii) Explain the reasons for the growth of mass tourism or footloose industry in the',
                   'part (i) above.'),
     S(24, '(ii) · Explain the reasons', '(iii) · Explain one benefit'),
     (srp3('Explanation', 6, 'Explanation 6 SRP’s @ 3m each · 18m'),), '3-0', ECON, (), (Q7BI,)),
    ('(iii)', 9, L(24, '(iii) Explain one benefit of mass tourism or footloose industry for developed economies.'),
     S(24, '(iii) · Explain one benefit', '(iv) · Explain one problem'),
     (srp3('Explanation', 3, 'Explanation 3 SRP’s @ 3m each · 9m'),), '3-0', ECON),
    ('(iv)', 9, L(24, '(iv) Explain one problem caused by mass tourism or footloose industry.'),
     S(24, '(iv) · Explain one problem', 'Total 40m'),
     (srp3('Explanation', 3, 'Explanation 3 SRP’s @ 3m each · 9m'),), '3-0', ECON),
])
Q7CI = L(24, '(i) Name one example of how the development of economic activities has resulted in',
         'conflict arising between people.')
PART_TWO += romans('7C', P2, 24, L(24, 'Economic Activity and Conflict'), (), ID + 'p2-q7c', (), [
    ('(i)', 3, Q7CI, S(24, '(i) · Name one example of how', '(ii) · Describe and explain'),
     (fixed('Example named', 3, 'Example named · 3m'),), '3-4', ENV),
    ('(ii)', 27, L(24, '(ii) Describe and explain this conflict.'),
     S(24, '(ii) · Describe and explain', 'Total 30m'),
     (srp3('Description/explanation', 9, 'Description/Explanation 9 SRP’s @ 3m each · 27m'),), '3-4', ENV, (),
     (Q7CI,)),
])

PART_TWO += romans('8A', P2, 25, L(25, 'Human Development Index', nth=0),
                   (L(25, 'Examine the table above and answer each of the following questions.'),),
                   ID + 'p2-q8a', ('page',), [
    ('(i)', 6, L(25, '(i) Name the two countries with the highest Human Development Indices.'),
     S(25, '(i) · Name the two', '(ii) · Calculate'),
     (fixed('Country 1', 3, 'Ireland · 3m'), fixed('Country 2', 3, 'USA · 3m')), '2-0', GRAPH + DEV),
    ('(ii)', 6, L(25, '(ii) Calculate the difference between the gross national income per capita in Ireland',
                  '(in $).'),
     S(25, '(ii) · Calculate', '(iii) · Explain briefly'), (fixed('Difference', 6, '5,713 ($) · 6m'),), '2-0', GRAPH),
    ('(iii)', 6, L(25, '(iii) Explain briefly one reason why life expectancy at birth is higher in some countries.'),
     S(25, '(iii) · Explain briefly', '(iv) · State two'),
     (srp3('Brief explanation', 2, 'Brief explanation 2 SRP’s @ 3m each · 6m'),), '3-1', DEV),
    ('(iv)', 6, L(25, '(iv) State two reasons why some countries have a lower HDI than other countries.'),
     S(25, '(iv) · State two', '(v) · The three'),
     (fixed('Two reasons', 6, 'Two reasons stated @ 3m each · 6m', (0, 3, 6)),), '3-1', DEV),
    ('(v)', 6, (L(25, '(v) The three countries with the highest number of expected years in school are the',
                  'Gross National Income.'),
                L(25, 'Explain briefly one reason why there may be a link between these two factors.')),
     S(25, '(v) · The three', 'Total 30m'),
     (srp3('Brief explanation', 2, 'Brief explanation 2 SRP’s @ 3m each · 6m'),), '3-1', DEV),
])
Q8BS = (L(25, 'Examine the aerial photograph of Sligo accompanying this paper.'),
        L(25, 'It is proposed to build a computer factory in the centre background', 'aerial photograph.'))
PART_TWO += romans('8B', P2, 25, L(25, 'Economic Activity – Aerial Photograph'), Q8BS, ID + 'p2-q8b', ('aerial',), [
    ('(i)', 15, L(25, '(i) Describe and explain the advantages of this location.'),
     S(26, '(i) · Describe and explain the advantages', '(ii) · Describe and explain the disadvantages'),
     (srp3('Description/explanation', 5, 'Description/Explanation 5 SRP’s @ 3m each · 15m'),), '3-0', ECON + AER),
    ('(ii)', 15, L(25, '(ii) Describe and explain the disadvantages of this location.'),
     S(26, '(ii) · Describe and explain the disadvantages', '(iii) · Using accepted'),
     (srp3('Description/explanation', 5, 'Description/Explanation 5 SRP’s @ 3m each · 15m'),), '3-0', ECON + AER),
    ('(iii)', 10, L(25, '(iii) Using accepted notation, suggest an alternative location for the new computer',
                    'alternative location.'),
     S(26, '(iii) · Using accepted', 'Total 40m'),
     (fixed('Location (accepted notation)', 4, 'Valid accepted notation for location · 4m'),
      srp3('Brief explanation', 2, 'Brief explanation 2 SRP’s @ 3m each · 6m')), '2-8', AER + ECON),
])
PART_TWO += romans('8C', P2, 25, L(25, 'Renewable Energy'), (), ID + 'p2-q8c', (), [
    ('(i)', 6, L(25, '(i) Name two examples of renewable energy.'),
     S(26, '(i) · Name two examples', '(ii) · Discuss the advantages'),
     (fixed('Two examples', 6, 'Two valid examples @ 3m each · 6m', (0, 3, 6)),), '3-5', ECON),
    ('(ii)', 24, L(25, '(ii) Discuss the advantages and disadvantages of renewable energy.'),
     S(26, '(ii) · Discuss the advantages', 'Total 30m'),
     (srp3('Discussion', 8, 'Discussion 8 SRP’s @ 3m each · 24m'),), '3-5', ECON),
])

PART_TWO.append(sketch(
    26, L(26, 'Ordnance Survey Map'),
    L(26, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper.',
      'north of the Garvoge River.'),
    27, ID + 'p2-q9a', '2-6', MAP + ECON, ('map', 'legend'), 'portrait',
    ('The N15', 'The N16', 'The R291', 'The railway line', 'The built up area of Sligo north of the Garvoge River')))
PART_TWO += romans('9B', P2, 26, L(26, 'European Union Policies'), (), ID + 'p2-q9b', (), [
    ('(i)', 4, L(26, '(i) Name any two European Union policies.'),
     S(28, '(i) · Name any two', '(ii) · Discuss the positive'),
     (fixed('Two policies', 4, 'Two policies named @ 2m each · 4m', (0, 2, 4)),), '3-3', EU),
    ('(ii)', 15, L(26, '(ii) Discuss the positive impacts of European Union policies.'),
     S(28, '(ii) · Discuss the positive', '(iii) · Discuss the negative'),
     (srp3('Discussion', 5, 'Discussion 5 SRP’s @ 3m each · 15m'),), '3-3', EU),
    ('(iii)', 15, L(26, '(iii) Discuss the negative impacts of European Union policies.'),
     S(28, '(iii) · Discuss the negative', '(iv) · State two'),
     (srp3('Discussion', 5, 'Discussion 5 SRP’s @ 3m each · 15m'),), '3-3', EU),
    ('(iv)', 6, L(26, '(iv) State two potential challenges facing the European Union in the future.'),
     S(28, '(iv) · State two', 'Total 40m'),
     (fixed('Two challenges', 6, 'Two challenges stated @ 3m each · 6m', (0, 3, 6)),), '3-3', EU + EURO),
])
Q9CI = L(26, '(i) Name one multinational company located in Ireland that you have studied.')
PART_TWO += romans('9C', P2, 26, L(26, 'Multinational Company (MNC)'), (), ID + 'p2-q9c', (), [
    ('(i)', 3, Q9CI, S(28, '(i) · Name one multinational', '(ii) · State where'),
     (fixed('MNC named', 3, 'MNC named · 3m'),), '3-2', MNC),
    ('(ii)', 3, L(26, '(ii) State where this multinational company is located in Ireland.'),
     S(28, '(ii) · State where', '(iii) · Name two markets'), (fixed('Location', 3, 'Location · 3m'),),
     '3-2', MNC, (), (Q9CI,)),
    ('(iii)', 6, L(26, '(iii) Name two markets outside Ireland where this multinational company sells its',
                   'products.'),
     S(28, '(iii) · Name two markets', '(iv) · Explain why'),
     (fixed('Two markets', 6, 'Two markets named @ 3m each · 6m', (0, 3, 6)),), '3-2', MNC, (), (Q9CI,)),
    ('(iv)', 18, L(26, '(iv) Explain why this multinational company may decide to relocate to another country.'),
     S(28, '(iv) · Explain why', 'Total 30m'),
     (srp3('Explanation', 6, 'Explanation 6 SRP’s @ 3m each · 18m'),), '3-2', MNC, (), (Q9CI,)),
])

PART_TWO.append(sketch(
    27, L(27, 'Aerial Photograph'),
    L(27, 'Examine the aerial photograph of Sligo accompanying this paper.', 'in the right background.'),
    29, ID + 'p2-q10a', '2-8', AER + URB, ('aerial',), 'landscape',
    ('The river', 'A bridge', 'Two connecting streets', 'A car park in the centre foreground',
     'A sports field in the right background')))
Q10BI = L(27, '(i) Name one urban area that you have studied and name any two land-uses in this', 'urban area.')
PART_TWO += romans('10B', P2, 27, L(27, 'Urban Land-Use'), (), ID + 'p2-q10b', (), [
    ('(i)', 9, Q10BI, S(30, '(i) · Name one urban', '(ii) · Describe and explain'),
     (fixed('Urban area named', 3, 'Urban area named · 3m'),
      fixed('Two land-uses', 6, 'Two land-uses named @ 3m each · 6m', (0, 3, 6))), '4-4', URB),
    ('(ii)', 21, L(27, '(ii) Describe and explain how land-use in this urban area has changed over time.'),
     S(30, '(ii) · Describe and explain', 'Total 30m'),
     (srp3('Description/explanation', 7, 'Description / Explanation 7 SRP’s @ 3m each · 21m'),), '4-4', URB, (),
     (Q10BI,)),
])
PART_TWO += romans('10C', P2, 27, L(27, 'Migration – Ireland'),
                   (L(27, 'Migration takes place due to push factors and pull factors.'),), ID + 'p2-q10c', (), [
    ('(i)', 4, L(27, '(i) Name one push factor and one pull factor associated with migration in Ireland.'),
     S(30, '(i) · Name one push', '(ii) · Discuss the positive'),
     (fixed('Push factor named', 2, 'Push factor named · 2m'), fixed('Pull factor named', 2, 'Pull factor named · 2m')),
     '4-2', POP),
    ('(ii)', 18, L(27, '(ii) Discuss the positive impacts of migration on Ireland.'),
     S(30, '(ii) · Discuss the positive', '(iii) · Discuss the negative'),
     (srp3('Discussion', 6, 'Discussion 6 SRP’s @ 3m each · 18m'),), '4-2', POP),
    ('(iii)', 18, L(27, '(iii) Discuss the negative impacts of migration on Ireland.'),
     S(30, '(iii) · Discuss the negative', 'Total 40m'),
     (srp3('Discussion', 6, 'Discussion 6 SRP’s @ 3m each · 18m'),), '4-2', POP),
])

PART_TWO += romans('11A', P2, 28, L(28, 'Traffic'),
                   (L(28, 'Examine the table above and answer each of the following questions.'),),
                   ID + 'p2-q11a', ('page',), [
    ('(i)', 3, L(28, '(i) What was the total number of people who crossed the canals while entering Dublin',
                 'in 2016?'),
     S(31, '(i) · What was the total', '(ii) · Calculate'), (fixed('Total', 3, '202,001 · 3m'),), '2-0', GRAPH),
    ('(ii)', 6, L(28, '(ii) Calculate the total number of people who crossed the canals by bicycle and walking',
                  'in 2016.'),
     S(31, '(ii) · Calculate', '(iii) · Name two'), (fixed('Total', 6, '33,562 · 6m'),), '2-0', GRAPH),
    ('(iii)', 6, L(28, '(iii) Name two examples of public transport available in cities such as Dublin.'),
     S(31, '(iii) · Name two', '(iv) · For which'),
     (fixed('Two examples', 6, 'Two valid examples @ 3m each · 6m', (0, 3, 6)),), '4-5', URB),
    ('(iv)', 6, L(28, '(iv) For which two modes of transport was there an increase in the number of people',
                  '2006 and 2016?'),
     S(31, '(iv) · For which', '(v) · Explain briefly'),
     (fixed('Two modes of transport', 6, 'Walking and cycling @ 3m each · 6m', (0, 3, 6)),), '2-0', GRAPH),
    ('(v)', 6, L(28, '(v) Explain briefly one reason for the increase in these two modes of transport.'),
     S(31, '(v) · Explain briefly', '(vi) · Suggest'),
     (srp3('Brief explanation', 2, 'Brief explanation 2 SRP’s @ 3m each · 6m'),), '4-5', URB),
    ('(vi)', 3, L(28, '(vi) Suggest one reason why there was a decrease in the number of people who crossed',
                  '2006 and 2010.'),
     S(31, '(vi) · Suggest', 'Total 30m'), (fixed('Reason', 3, 'One reason suggested · 3m'),), '4-5', URB),
])
PART_TWO.append(T(
    'p2-11b', P2, '11B', '', 30, 28, L(28, 'Population'),
    (L(28, 'By the year 2031, there will be nearly one million people over the age of 65 in Ireland.', 'since 2016.'),
     L(28, 'Discuss the challenges associated with an ageing population', 'can be planned for.')),
    (S(32, 'Discussion 10 SRP', 'Total 30m'),),
    (srp3('Discussion', 10, 'Discussion 10 SRP’s @ 3m each · 30m'),),
    '4-0', POP, ID + 'p2-q11b'))
Q11CS = (L(29, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper and',
           'following questions.'),)
PART_TWO += romans('11C', P2, 29, L(29, 'Settlement Distribution'), Q11CS, ID + 'p2-q11c', ('map', 'legend'), [
    ('(i)', 2, L(29, '(i) Give a grid reference for an area on the map where there is an absence of', 'settlement.'),
     S(32, '(i) · Give a grid', '(ii) · Explain in detail'), (fixed('Grid reference', 2, 'Grid reference · 2m'),),
     '4-3', URB + MAP),
    ('(ii)', 18, L(29, '(ii) Explain in detail, using evidence from the map, why there is an absence of',
                   'at this location.'),
     S(32, '(ii) · Explain in detail', '(iii) · Give a grid'),
     (srp3('Explanation', 6, 'Explanation 6 SRP’s @ 3m each · 18m'),), '4-3', URB + MAP),
    ('(iii)', 2, L(29, '(iii) Give a grid reference for an area on the map which has a relatively high density of',
                   'settlement.'),
     S(32, '(iii) · Give a grid', '(iv) · Explain in detail'), (fixed('Grid reference', 2, 'Grid reference · 2m'),),
     '4-3', URB + MAP),
    ('(iv)', 18, L(29, '(iv) Explain in detail, using evidence from the map, why there is a relatively high density',
                   'at this location.'),
     S(32, '(iv) · Explain in detail', 'Total 40m'),
     (srp3('Explanation', 6, 'Explanation 6 SRP’s @ 3m each · 18m'),), '4-3', URB + MAP),
])

TOWN_REASON = ('Three reasons @ 10m each as follows:', 'For each reason:', 'Ordnance Survey map evidence · 1m',
               'Description / Explanation 3 SRP’s @ 3m each · 9m')
PROBLEMS = ('Traffic congestion', 'Urban decay', 'Urban sprawl', 'Environmental quality.')
PART_TWO += romans('12A', P2, 30, L(30, 'Migration'),
                   (L(30, 'Examine the table above and answer each of the following questions.'),),
                   ID + 'p2-q12a', ('page',), [
    ('(i)', 24, L(30, '(i) Using graph paper, draw a suitable graph to illustrate this data.'),
     S(33, 'Graph paper', '(ii) · Explain briefly'), GRAPH_OL, '2-0', GRAPH),
    ('(ii)', 6, L(30, '(ii) Explain briefly one reason why people seek asylum in other countries.'),
     S(33, '(ii) · Explain briefly', 'Total 30m'),
     (srp3('Brief explanation', 2, 'Brief explanation 2 SRP’s @ 3m each · 6m'),), '4-2', POP),
])
PART_TWO += [
    T('p2-12b', P2, '12B', '', 30, 30, L(30, 'Urban Development'),
      (L(30, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper.'),
       L(30, 'Describe and explain three reasons why the town of Sligo developed at this location,',
         'support each reason.')),
      (S(33, 'Three reasons @ 10m each', 'Total 30m'),),
      tuple(Criterion(f'Reason {n}', 10, sums((0, 1), steps(9, 3)), 'srp', TOWN_REASON) for n in (1, 2, 3)),
      '4-3', URB + MAP, ID + 'p2-q12b', ('map', 'legend')),
    T('p2-12c', P2, '12C', '', 40, 30, L(30, 'Urban Problems'),
      (L(30, 'Problems can develop as a result of the growth of urban areas.'),
       L(30, 'Discuss any three of the following problems with reference to any urban area(s)',
         'Environmental quality.')),
      (S(34, 'Three problems discussed as follows:', 'Total 40m'),),
      (srp3('First problem discussed', 5, 'First problem discussed 5 SRP’s @ 3m each · 15m'),
       srp3('Second problem discussed', 4, 'Second problem discussed 4 SRP’s @ 3m each · 12m'),
       srp3('Third problem discussed', 4, 'Third problem discussed 4 SRP’s @ 3m each · 12m'),
       fixed('Urban area named', 1, 'Urban area named · 1m')),
      '4-5', URB, ID + 'p2-q12c', absorbs=pool(ID + 'p2-q12c-', PROBLEMS, 3)[1]),
]

TASKS = [*PART_ONE, *PART_TWO]

ID_CORRECTION_REASON = 'No 2018 Ordinary card shipped before this review; every card is new.'

# No 2018 Ordinary card was live on origin/main before this review.
LEGACY_IDS: list[str] = []
