"""Independent review ledger: Leaving Certificate Geography 2019 Ordinary Level.

Sources (English editions, harvested Paper Trail corpus; sizes and SHA-256
pinned in EXPECTED_SOURCES and the generated audit): the examination paper
LC005GLP000EV (28 pages; one booklet printed Part One, answered in it, and
Part Two), marking scheme LC005GLP000EV (36 pages), and the common
companions shared with Higher Level — the 1:50 000 Templemore map
LC005CLP003EV (published only as a JPEG), its legend LC005CLPC00EV and the
Templemore aerial photograph LC005CLP004EV (a JPEG). Part One is 100 marks
(any ten of twelve @ 10), Part Two 300 (three questions @ 100).

Visual sweep (every page rendered and read on 2026-10-13):
  Paper p1 cover and examiner's grid; p2-p11 Part One Questions 1-12 (p6
  holds Q5 and Q6, p7 Q7 and Q8); p12 Part Two instructions; p13 Section 1
  divider; p14-p19 Q1-Q6 (p17 opens with the Regional Geography divider);
  p20 Section 2 divider; p21-p27 Electives Q7-Q12 (p21 and p25 open with
  their elective dividers; p22 holds 8A, p23 8B and 8C); p28 back cover
  ("There is no examination material on this page").
  Scheme p1 cover; p2-p3 notes; p4-p5 Geographical Investigation
  (coursework) and its presentation marks; p6-p7 Part One table (Q1-Q6,
  Q7-Q12); p8 Part Two instructions and Section 1 divider; p9-p33 Q1-Q12;
  p34 investigation topics; p35 Irish-language bonus marks; p36 back cover.
  Companions: Templemore map extract; OS legend sheet; oblique aerial
  photograph of Templemore.

Boundaries and tariffs follow the 2020 Ordinary ledger: every priced roman
is a task; a matching table under ONE printed instruction stays one task
with a criterion per scheme row, in the printed row order: Q1 Ash cloud=B,
Vent=D, Crater=C, Lava flow=A; Q2 Stalagmite=C, Passage=D, Pillar=A,
Stalactite=B; Q3 prints (i) and (ii) in one part-completed table: (i)
Meander=B, Waterfall=C, Delta=A (V-shaped valley D is printed), (ii)
V-shaped valley Erosion, Delta Deposition (the other two are printed); Q4
African=C, North American=A, Nazca=B, Eurasian=D; Q8 The Islamic World=B,
Cool Temperate Oceanic=E, Limerick=A, The Border, Midlands, West (BMW)
region=D, Wicklow Mountains=C; Q12 Sand dunes=B, Miyakejima=C, Crater
Lake=A, Oxbow lake=D; Part Two 3A(i) Beach C, U-shaped valley A, Basalt
columns B, 3A(ii) Lava cooling B, Longshore drift C, Plucking A. Q7's five
true/false statements are separately priced romans.

Tariffs as printed: twelve parts carry 40 marks (1B, 2C, 3B, 4B, 5C, 6B,
7C, 8B, 9B, 10C, 11B, 12C) and the rest 30. An SRP is 3 marks unless the
scheme says otherwise (10C(i) prices the donor region at 2 SRPs @ 2m).
12B(ii) prices "Two named land-uses · 6m" with no per-item split, so its
card offers the printed 0 or 6 and no invented half.
"""

from geography_review import (
    Criterion, Lift, Route, SchemeSlice, Task, pool, fixed, slug, srp, steps, sums,
)

YEAR = 2019
LEVEL = 'ordinary'
PAPER_PAGES = {1: 28, 2: 28}
SCHEME_PAGES = 36
_FORTY = {'1B', '2C', '3B', '4B', '5C', '6B', '7C', '8B', '9B', '10C', '11B', '12C'}
QUESTION_TARIFFS = {1: {str(n): 10 for n in range(1, 13)},
                    2: {f'{n}{x}': (40 if f'{n}{x}' in _FORTY else 30)
                        for n in range(1, 13) for x in 'ABC'}}

EXPECTED_SOURCES = {
    'paper1': ('LC005GLP000EV.pdf', 3739580),
    'paper2': ('LC005GLP000EV.pdf', 3739580),
    'scheme': ('LC005GLP000EV.pdf', 550626),
    'map': ('LC005CLP003EV.jpg', 7718516),
    'legend': ('LC005CLPC00EV.pdf', 836095),
    'aerial': ('LC005CLP004EV.jpg', 5264592),
}

_PAPER = {1: 'cover and examiner grid', **{p: 'question' for p in range(2, 12)},
          12: 'Part Two instructions', 13: 'section divider', **{p: 'question' for p in range(14, 20)},
          20: 'section divider', **{p: 'question' for p in range(21, 28)}, 28: 'back cover'}
PAGE_REVIEW = {
    # One booklet printed both parts.
    'paper1': _PAPER, 'paper2': _PAPER,
    'scheme': {1: 'cover', 2: 'notes', 3: 'notes', 4: 'geographical investigation (coursework)',
               5: 'presentation marks (coursework)', 6: 'Part One table', 7: 'Part One table',
               8: 'Part Two instructions and section divider',
               **{p: 'Part Two allocation' for p in range(9, 34)},
               34: 'investigation topics', 35: 'Irish-language bonus marks', 36: 'back cover'},
}

EXPECTED_SELECTION_SCAN = [
    [1, 2, 'attempt any ten'], [1, 12, 'attempt three'], [1, 13, 'attempt two'], [1, 14, 'attempt one'],
    [1, 14, 'answer (i) or (ii)'], [1, 14, 'any two'], [1, 14, 'any two'], [1, 14, 'one of the following'],
    [1, 15, 'one of the following'],
    [1, 16, 'any two'], [1, 16, 'any two'],
    [1, 17, 'attempt one'], [1, 17, 'any three'],
    [1, 18, 'any one'],
    [1, 20, 'attempt one'],
    [1, 21, 'one of the following'],
    [1, 23, 'choose'], [1, 23, 'any one'],
    [1, 26, 'any three'], [1, 26, 'any three'],
]
SELECTION_REVIEW = [
    {'scan': [[1, 2, 'attempt any ten'], [1, 12, 'attempt three'], [1, 13, 'attempt two'], [1, 14, 'attempt one'],
              [1, 17, 'attempt one'], [1, 20, 'attempt one']],
     'kind': 'exam-attempt-rule',
     'reason': 'Part One any ten of twelve and Part Two three questions (one of Q1-3, one of Q4-6, one elective) are attempt rules; every question is carded.'},
    {'scan': [[1, 14, 'answer (i) or (ii)']], 'kind': 'closed-route',
     'reason': '1B: (i) or (ii) -> two routes, each with its own scheme allocation.'},
    {'scan': [[1, 14, 'one of the following']], 'kind': 'closed-choose-one',
     'reason': '1C: one of four printed rock-cycle activities -> four routes.'},
    {'scan': [[1, 15, 'one of the following']], 'kind': 'closed-choose-one',
     'reason': '2B: one of three printed surface processes -> three routes.'},
    {'scan': [[1, 21, 'one of the following']], 'kind': 'closed-choose-one',
     'reason': '7B: one of three printed economic activities -> three routes.'},
    {'scan': [[1, 23, 'choose'], [1, 23, 'any one']], 'kind': 'closed-choose-one',
     'reason': '8C: "Choose any one of the European Union policies listed below" (four printed) -> four routes.'},
    {'scan': [[1, 16, 'any two'], [1, 17, 'any three'], [1, 26, 'any three']], 'kind': 'choose-n-one-card',
     'reason': '3B(ii) any two of three printed weathering types, 4C any three of five printed cultural factors and 11C any three of four printed population factors -> one card each with every printed item (choice is not a route). 6B(ii) "two of the factors listed below" (three printed on one row) is one card on the same rule.'},
    {'scan': [[1, 14, 'any two'], [1, 14, 'any two'], [1, 16, 'any two'], [1, 18, 'any one'], [1, 26, 'any three']],
     'kind': 'open-response',
     'reason': 'No printed pool: 1B(i) any two landforms and 1B(ii) any two mass movement processes (the scheme prices two @ 20m); 3B(i) any two factors; 5B any one urban area; 11B(iii) any three problems.'},
]

P1, P2 = 1, 2
ID = 'geography-2019-ol-'
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


def part_one_romans(q, page, title, stem, sources, parts):
    """Part One romans. parts: (roman, prompt Lifts, scheme start, scheme end, criteria, topic, atlas[, labels])."""
    out = []
    for index, part in enumerate(parts):
        roman, prompt, start, end, criteria, topic, atlas = part[:7]
        labels = part[7] if len(part) > 7 else ()
        key = roman.strip('()')
        out.append(T(f'p1-{q}-{key}', P1, q, roman, sum(c.max for c in criteria), page, title,
                     prompt if isinstance(prompt, tuple) else (prompt,),
                     (S(7 if int(q) >= 7 else 6, start, end),),
                     criteria, topic, atlas, ID + f'p1-q{q}' + ('' if index == 0 else f'-{key}'),
                     sources, stem, row_labels=labels))
    return out


# ---------------------------------------------------------------- Part One --
TICK = 'Tick the correct box.'
Q1S = (L(2, 'Examine the diagram above which shows the structure of a volcano', 'following questions.'),)
Q2S = (L(3, 'Examine the diagram above of underground features in a Karst region', 'following questions.'),)
Q3S = (L(4, 'Examine the photographs above.', 'completed for you.'),)
Q4S = (L(5, 'Examine the map above and answer each of the following questions.'),)
Q5S = (L(6, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper and answer',
         'following questions.', nth=0),)
Q6S = (L(6, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper and answer',
         'following questions.', nth=1),)
Q7S = (L(7, 'Examine the aerial photograph of Templemore accompanying this paper.', 'in each case.'),)
Q9S = (L(8, 'Examine the table above showing the year that each of the countries joined', 'following questions.'),)
Q10S = (L(9, 'Examine the weather graphic above, and with reference to the data provided', 'following questions.'),)
Q11S = (L(10, 'Examine the chart above and answer each of the following questions.'),)
Q12S = (L(11, 'Examine the satellite images above and answer each of the following questions.'),)

PART_ONE = part_one_romans('1', 2, L(2, 'Volcanoes'), Q1S, ('page',), [
    ('(i)', L(2, '(i) Match each of the letters A, B, C and D with the feature', 'table below.'),
     'Q1.(i)', 'Q.1(ii)', rows(['Q1.(i) · B · 2m', '=D · 2m', '=C · 2m', '=A · 2m']), '0-7', EV,
     (L(2, 'Ash cloud'), L(2, 'Vent'), L(2, 'Crater'), L(2, 'Lava flow'))),
    ('(ii)', L(2, '(ii) Name one example of an active volcano.'),
     'Q.1(ii)', 'Q.2(i)', (fixed('Active volcano', 2, 'Q.1(ii) · Any valid example · 2m · Total 10m'),), '0-7', EV),
])
PART_ONE += part_one_romans('2', 3, L(3, 'Karst Landscape'), Q2S, ('page',), [
    ('(i)', L(3, '(i) Match each of the letters A, B, C and D with the landform', 'table below.'),
     'Q.2(i)', 'Q.2(ii)', rows(['Q.2(i) · C · 2m', '=D · 2m', '=A · 2m', '=B · 2m']), '0-3', KARST,
     (L(3, 'Stalagmite'), L(3, 'Passage'), L(3, 'Pillar'), L(3, 'Stalactite'))),
    ('(ii)', L(3, '(ii) Are the landforms in the table above formed as a result of mechanical weathering',
               'chemical weathering?'),
     'Q.2(ii)', 'Q.3(i)', (fixed('Type of weathering', 2, 'Q.2(ii) · Chemical Weathering · 2m · Total 10m'),),
     '0-3', KARST + RW),
])
PART_ONE += [
    T('p1-3-i', P1, '3', '(i)', 6, 4, L(4, 'Rivers'),
      (L(4, '(i) Match each of the photographs A, B, C and D with the landform', 'table below.'),),
      (S(6, 'B (Both)', 'Q.4 (i)'),),
      (fixed('Row 1', 2, 'B (Both) · 2m'), fixed('Row 2', 2, 'C (Erosion) · 2m'),
       fixed('Row 3', 2, 'A Deposition · 2m + 2m · Total 10m')),
      '0-9', RIVERS, ID + 'p1-q3', ('page',), Q3S,
      row_labels=(L(4, 'Meander'), L(4, 'Waterfall'), L(4, 'Delta'))),
    T('p1-3-ii', P1, '3', '(ii)', 4, 4, L(4, 'Rivers'),
      (L(4, '(ii) State whether each of the landforms named in the table is formed by', 'erosion and deposition.'),),
      (S(6, 'Q.3(i)', 'B (Both)'), S(6, 'A Deposition', 'Q.4 (i)')),
      (fixed('Row 1', 2, 'Q.3(i) · (D) Q.3 (ii) Erosion · 2m'), fixed('Row 2', 2, 'A Deposition · 2m + 2m · Total 10m')),
      '0-9', RIVERS, ID + 'p1-q3-ii', ('page',), Q3S,
      row_labels=(L(4, 'V-shaped valley'), L(4, 'Delta'))),
]
PART_ONE += part_one_romans('4', 5, L(5, 'Plate Tectonics'), Q4S, ('page',), [
    ('(i)', L(5, '(i) Match each of the letters A, B, C and D with the named plate', 'table below.'),
     'Q.4 (i)', 'Q.4 (ii)', rows(['Q.4 (i) · C · 2m', '=A · 2m', '=B · 2m', '=D · 2m']), '0-0', PS,
     (L(5, 'African Plate'), L(5, 'North American Plate'), L(5, 'Nazca Plate'), L(5, 'Eurasian Plate'))),
    ('(ii)', L(5, '(ii) Name the volcanic island located at E.'),
     'Q.4 (ii)', 'Q.5(i)', (fixed('Volcanic island', 2, 'Q.4 (ii) · Iceland · 2m · Total 10m'),), '0-0', PS + EV),
])
PART_ONE += part_one_romans('5', 6, L(6, 'Ordnance Survey Map', nth=0), Q5S, ('map', 'legend'), [
    ('(i)', (L(6, '(i) Devilsbit Mountain and Kilduff Mountain are located in which area', TICK),
             L(6, 'North west'), L(6, 'North east')),
     'Q.5(i)', 'Q.5(ii)', (fixed('Area of the map', 5, 'Q.5(i) · North west · 5m'),), '2-6', MAP),
    ('(ii)', (L(6, '(ii) What is the length of the R 501 road', TICK), L(6, '6.6 km'), L(6, '7.0 km')),
     'Q.5(ii)', 'Q.6(i)', (fixed('Length', 5, 'Q.5(ii) · 7.0 km · 5m · Total 10m'),), '2-6', MAP),
])
PART_ONE += part_one_romans('6', 6, L(6, 'Ordnance Survey Map', nth=1), Q6S, ('map', 'legend'), [
    ('(i)', L(6, '(i) Name the features located at each of the following grid references.'),
     'Q.6(i)', 'Q.6(ii)', rows(['Q.6(i) · Golf course · 2m', 'Rifle Range · 2m', 'Railway Station · 2m']), '2-6', MAP,
     (L(6, 'S 108 707'), L(6, 'S 050 728'), L(6, 'S 120 707'))),
    ('(ii)', L(6, '(ii) What does the letter R stand for in relation to the R501 and the R433 roads?'),
     'Q.6(ii)', 'Q.6(iii)', (fixed('Letter R', 2, 'Q.6(ii) · Regional · 2m'),), '2-6', MAP),
    ('(iii)', L(6, '(iii) Draw the Ordnance Survey map symbol for a Triangulation Pillar in the box below.'),
     'Q.6(iii)', 'Page 4 of', (fixed('Symbol', 2, 'Q.6(iii) · Correct symbol · 2m · Total 10m'),), '2-6', MAP),
])
PART_ONE += part_one_romans('7', 7, L(7, 'Aerial Photograph'), Q7S, ('aerial',), [
    ('(i)', L(7, '(i) There is a roundabout in the centre foreground of the aerial photograph.'),
     'Q.7', '(ii) True', (fixed('True or false', 2, 'Q.7 · (i) False · 2m'),), '2-8', AER),
    ('(ii)', L(7, '(ii) There is a lake in the left middleground of the aerial photograph.'),
     '(ii) True', '(iii) False', (fixed('True or false', 2, '(ii) True · 2m'),), '2-8', AER),
    ('(iii)', L(7, '(iii) There is a running track in the right foreground of the aerial photograph.'),
     '(iii) False', '(iv) False', (fixed('True or false', 2, '(iii) False · 2m'),), '2-8', AER),
    ('(iv)', L(7, '(iv) There is a graveyard in the left foreground of the aerial photograph.'),
     '(iv) False', '(v) True', (fixed('True or false', 2, '(iv) False · 2m'),), '2-8', AER),
    ('(v)', L(7, '(v) Agriculture is an example of an economic activity in the centre background', 'aerial photograph.'),
     '(v) True', 'Q.8', (fixed('True or false', 2, '(v) True · 2m · Total 10m'),), '2-8', AER + ECON),
])
PART_ONE += [
    T('p1-8', P1, '8', '', 10, 7, L(7, 'Regions'),
      (L(7, 'Match the description of the region with the example of the region', 'in the table below.'),),
      (S(7, 'Q.8', 'Q.9 (i)'),), rows(['Q.8 · B · 2m', '=E · 2m', '=A · 2m', '=D · 2m', 'C · 2m · Total 10m']),
      '1-0', IRL + EURO, ID + 'p1-q8', ('page',),
      row_labels=(L(7, 'The Islamic World'), L(7, 'Cool Temperate Oceanic'), L(7, 'Limerick'),
                  L(7, 'The Border, Midlands, West'), L(7, 'Wicklow Mountains'))),
]
PART_ONE += part_one_romans('9', 8, L(8, 'European Union', nth=0), Q9S, ('page',), [
    ('(i)', L(8, '(i) In which year did Romania and Bulgaria join the European Union?'),
     'Q.9 (i)', '(ii) 10', (fixed('Year', 2, 'Q.9 (i) 2007 · 2m'),), '2-0', GRAPH + EU),
    ('(ii)', L(8, '(ii) How many countries joined the European Union in 2004?'),
     '(ii) 10', '(iii) Croatia', (fixed('Number of countries', 2, '(ii) 10 · 2m'),), '2-0', GRAPH + EU),
    ('(iii)', L(8, '(iii) What country is the most recent member of the European Union?'),
     '(iii) Croatia', '(iv) Southern', (fixed('Country', 2, '(iii) Croatia · 2m'),), '2-0', GRAPH + EU),
    ('(iv)', L(8, '(iv) Are the countries that joined the European Union in the 1980’s located in Northern',
               'Southern Europe?'),
     '(iv) Southern', '(v) Any valid', (fixed('Location', 2, '(iv) Southern Europe · 2m'),), '2-0', GRAPH + EU),
    ('(v)', L(8, '(v) State one advantage of membership of the European Union.'),
     '(v) Any valid', 'Q.10', (fixed('Advantage', 2, '(v) Any valid advantage · 2m · Total 10m'),), '3-3', EU),
])
PART_ONE += part_one_romans('10', 9, L(9, 'Weather Statistics'), Q10S, ('page',), [
    ('(i)', L(9, '(i) What was the lowest temperature (°C) experienced on January 17th?'),
     'Q.10 · (i)', '(ii) 27', (fixed('Temperature', 2, 'Q.10 · (i) 4 (°C) · 2m'),), '2-7', GRAPH + WEATHER),
    ('(ii)', L(9, '(ii) What was the wind speed (km/hr) at midnight (00:00 hours)?'),
     '(ii) 27', '(iii) 6', (fixed('Wind speed', 2, '(ii) 27 (km/hr) · 2m'),), '2-7', GRAPH + WEATHER),
    ('(iii)', L(9, '(iii) How many hours of rainfall were there between midnight and 10 o’clock?'),
     '(iii) 6', '(iv) 8', (fixed('Hours of rainfall', 2, '(iii) 6 (hrs) · 2m'),), '2-7', GRAPH + WEATHER),
    ('(iv)', L(9, '(iv) What was the highest temperature (°C) recorded on January 17th?'),
     '(iv) 8', '(v) Thermometer', (fixed('Temperature', 2, '(iv) 8 (°C) · 2m'),), '2-7', GRAPH + WEATHER),
    ('(v)', L(9, '(v) What is the name of the weather instrument used to measure temperature?'),
     '(v) Thermometer', 'Q.11', (fixed('Instrument', 2, '(v) Thermometer · 2m · Total 10m'),), '2-7', WEATHER),
])
PART_ONE += part_one_romans('11', 10, L(10, 'Communications in Ireland'), Q11S, ('page',), [
    ('(i)', L(10, '(i) In which year did 87% of Irish households have access to the internet?'),
     'Q.11 · (i)', '(ii) 9', (fixed('Year', 2, 'Q.11 · (i) 2016 · 2m'),), '2-0', GRAPH),
    ('(ii)', L(10, '(ii) What was the change in the percentage of Irish households with access to the',
               'between 2011 and 2016?'),
     '(ii) 9', '(iii) 2013', (fixed('Change', 2, '(ii) 9 (%) · 2m'),), '2-0', GRAPH),
    ('(iii)', L(10, '(iii) Between which two years was there no change in the percentage of Irish',
                'access to the internet?'),
     '(iii) 2013', '(iv) Increasing', (fixed('Two years', 2, '(iii) 2013 and 2014 · 2m'),), '2-0', GRAPH),
    ('(iv)', (L(10, '(iv) According to the chart, what was the trend in access to the internet', TICK),
              L(10, 'Increasing'), L(10, 'Decreasing')),
     '(iv) Increasing', '(v) 11', (fixed('Trend', 2, '(iv) Increasing · 2m'),), '2-0', GRAPH),
    ('(v)', L(10, '(v) What percentage of Irish households had no access to the internet in 2017?'),
     '(v) 11', 'Q.12', (fixed('Percentage', 2, '(v) 11 (%) · 2m · Total 10m'),), '2-0', GRAPH),
])
PART_ONE += part_one_romans('12', 11, L(11, 'Satellite Interpretation'), Q12S, ('page',), [
    ('(i)', L(11, '(i) Match each of the images A, B, C and D with the description', 'table below.'),
     'Q.12(i)', 'Q.12(ii)', rows(['Q.12(i) · B · 2m', '=C · 2m', '=A · 2m', '=D · 2m']), '2-8', AER,
     (L(11, 'Sand dunes, Sahara Desert'), L(11, 'Miyakejima Volcano, Japan'), L(11, 'Crater Lake, USA'),
      L(11, 'Oxbow lake on the Mississippi River'))),
    ('(ii)', L(11, '(ii) Which two landforms, named in the table above, are formed as a result of volcanic',
               'activity?'),
     'Q.12(ii)', 'Page 5 of',
     (fixed('Landform 1', 1, 'Q.12(ii) · Miyakejima Volcano, Japan · 1m'),
      fixed('Landform 2', 1, 'Crater Lake, USA · 1m · Total 10m')), '0-7', EV),
])


# ---------------------------------------------------------------- Part Two --
def romans(q, page, title, stem, first_id, sources, parts):
    """Separately priced romans of one A/B/C part.
    parts: (sub, marks, prompt Lift(s), scheme slice(s), criteria, topic, atlas[, extra stem Lifts[, row labels]])."""
    out = []
    for index, part in enumerate(parts):
        sub, marks, prompt, scheme, criteria, topic, atlas = part[:7]
        extra = part[7] if len(part) > 7 else ()
        labels = part[8] if len(part) > 8 else ()
        scheme = scheme if isinstance(scheme, tuple) else (scheme,)
        roman = sub.strip('()')
        out.append(T(f'p2-{q.lower()}-{roman}', P2, q, sub, marks, page, title,
                     prompt if isinstance(prompt, tuple) else (prompt,), scheme,
                     criteria, topic, atlas, first_id if index == 0 else f'{first_id}-{roman}',
                     sources, (*stem, *extra), row_labels=labels))
    return out


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


SURFACE = ('River processes', 'Coastal processes', 'Mass movement processes.')
ROCK = ('Quarrying', 'Mining', 'Oil/Gas exploitation', 'Geothermal energy production.')
PART_TWO = [
    sketch(14, L(14, 'Ordnance Survey Map'),
           L(14, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper.',
             'south of Templemore.'),
           9, ID + 'p2-q1a', '2-6', MAP + RIVERS, ('map', 'legend'), 'landscape',
           ('The highest point on the Ordnance Survey map', 'Templemore Lake',
            'The River Suir from S 132 728 to where it leaves the map at S 119 680',
            'An area of coniferous planation in the south east', 'An area of deciduous woodland south of Templemore')),
    T('p2-1b', P2, '1B', '', 40, 14, L(14, 'Landform Development'),
      (L(14, '(i) Explain, with the aid of diagrams, the formation of any two landforms.'),),
      (S(10, 'Formation of any two landforms @ 20m each.', 'Total 40m'),),
      two_of('Landform', 20, 'Formation of any two landforms @ 20m each.', 'For each landform:',
             ('Landform named · 1m', 'Diagram(s) two aspects @ 2m each · 4m',
              'Formation explained 5 SRP’s @ 3m each · 15m'),
             ((0, 1), (0, 2, 4), steps(15, 3))),
      '0-4', PS_SURFACE, ID + 'p2-q1b-route-i',
      routes=(
          Route('route-i', 'Route (i)', ID + 'p2-q1b-route-i', False),
          Route('route-ii', 'Route (ii)', ID + 'p2-q1b-route-ii', False,
                prompt=(L(14, '(ii) Describe and explain any two processes of mass movement.'),),
                scheme=(S(10, 'Any two processes @ 20m each', 'Total 40m'),),
                criteria=two_of('Process', 20, 'Any two processes @ 20m each', 'For each process:',
                                ('Process stated · 2m', 'Description / Explanation 6 SRP’s @ 3m each · 18m'),
                                ((0, 2), steps(18, 3))),
                topic='0-8', atlas=RW),
      )),
    T('p2-1c', P2, '1C', '', 30, 14, L(14, 'Human Interaction with the Rock Cycle'),
      (L(14, 'Describe and explain how humans interact with the rock cycle', 'Geothermal energy production.'),),
      (S(11, 'Description / explanation 10', 'Total 30m'),),
      (srp3('Description/explanation', 10, 'Description / explanation 10 SRP’s @ 3m each.'),),
      '0-6', RW, ID + 'p2-q1c-quarrying', routes=bullet_routes('p2-q1c-', ROCK)),
]

Q2AS = (L(15, 'Examine the information above and answer each of the following questions.'),)
PART_TWO += romans('2A', 15, L(15, 'Earthquakes'), Q2AS, ID + 'p2-q2a', ('page',), [
    ('(i)', 3, L(15, '(i) What name is given to the area where 80% of all earthquakes occur?'),
     S(12, '(i) · What name', '(ii) · Name the scale'),
     (fixed('Area', 3, 'Rim of Pacific Ocean/Ring of Fire · 3m'),), '0-7', EV),
    ('(ii)', 3, L(15, '(ii) Name the scale used to assign a magnitude rating to an earthquake.'),
     S(12, '(ii) · Name the scale', '(iii) · What range'), (fixed('Scale', 3, 'Valid scale named · 3m'),), '0-7', EV),
    ('(iii)', 3, L(15, '(iii) What range of magnitude is considered to be a moderate to strong earthquake?'),
     S(12, '(iii) · What range', '(iv) · Explain briefly'), (fixed('Range', 3, '5 to 7 · 3m'),), '0-7', EV),
    ('(iv)', 6, L(15, '(iv) Explain briefly what is meant by a fault zone.'),
     S(12, '(iv) · Explain briefly', '(v) · List three'),
     (srp3('Brief explanation', 2, 'Brief explanation two SRP’s @ 3m each · 6m'),), '0-7', EV + PS),
    ('(v)', 9, L(15, '(v) List three effects of an earthquake.'),
     S(12, '(v) · List three', '(vi) · Explain briefly'),
     (fixed('Three effects', 9, 'Three valid effects @ 3m each · 9m', (0, 3, 6, 9)),), '0-7', EV),
    ('(vi)', 6, L(15, '(vi) Explain briefly one way to limit the damage that an earthquake can cause.'),
     S(12, '(vi) · Explain briefly', 'Total 30m'),
     (srp3('Brief explanation', 2, 'Brief explanation 2 SRP’s @ 3m each · 6m'),), '0-7', EV),
])
PART_TWO.append(T(
    'p2-2b', P2, '2B', '', 30, 15, L(15, 'Human Interaction with Surface Processes'),
    (L(15, 'Examine how humans interact with one of the following surface processes:', 'Mass movement processes.'),),
    (S(12, 'Interaction identified · 3m', 'Total 30m'),),
    (fixed('Interaction identified', 3, 'Interaction identified · 3m'),
     srp3('Explanation', 9, 'Explanation 9 SRP’s @ 3m each · 27m')),
    '0-6', RIVERS, ID + 'p2-q2b-river-processes',
    routes=bullet_routes('p2-q2b-', SURFACE, atlas=dict(zip(SURFACE, (RIVERS, SEA, RW))))))
PART_TWO += romans('2C', 15, L(15, 'Rocks'), (), ID + 'p2-q2c', (), [
    ('(i)', 6, L(15, '(i) Name two examples of sedimentary rocks.'),
     S(13, '(i) · Name two examples', '(ii) · State two uses'),
     (fixed('Two sedimentary rocks', 6, 'Two sedimentary rocks named @ 3m each · 6m', (0, 3, 6)),), '0-1', RW),
    ('(ii)', 7, L(15, '(ii) State two uses of sedimentary rocks.'),
     S(13, '(ii) · State two uses', '(iii) · Describe and explain'),
     (fixed('Use 1', 4, 'Use 1 · 4m'), fixed('Use 2', 3, 'Use 2 · 3m')), '0-1', RW),
    ('(iii)', 27, L(15, '(iii) Describe and explain how sedimentary rocks are formed.'),
     S(13, '(iii) · Describe and explain', 'Total 40m'),
     (srp3('Description/explanation', 9, 'Description/Explanation 9 SRP’s @ 3m each · 27m'),), '0-1', RW),
])

Q3AS = (L(16, 'Examine the photographs above and answer each of the following questions.'),)
PART_TWO += romans('3A', 16, L(16, 'Landforms and Processes'), Q3AS, ID + 'p2-q3a', ('page',), [
    ('(i)', 9, L(16, '(i) In your answer book, match each of the letters A, B and C', 'Basalt columns.'),
     S(14, '• C Beach', '(ii) · In your answer book'),
     (fixed('Row 1', 3, '• C Beach · 3m'), fixed('Row 2', 3, '• A U-shaped valley · 3m'),
      fixed('Row 3', 3, '• B Basalt columns. · 3m')), '0-4', SEA + GLAC + RW, (),
     (L(16, 'Beach'), L(16, 'U-shaped valley'), L(16, 'Basalt columns'))),
    ('(ii)', 9, L(16, '(ii) In your answer book, match each of the letters A, B and C', 'Plucking.'),
     S(14, '• B Lava cooling', '(iii) · Explain briefly'),
     (fixed('Row 1', 3, '• B Lava cooling · 3m'), fixed('Row 2', 3, '• C Longshore drift · 3m'),
      fixed('Row 3', 3, '• A Plucking. · 3m')), '0-4', SEA + GLAC + RW, (),
     (L(16, 'Lava cooling'), L(16, 'Longshore drift', nth=0), L(16, 'Plucking', nth=0))),
    ('(iii)', 12, L(16, '(iii) Explain briefly each of the following:', 'Plucking.'),
     S(14, 'Two brief explanations', 'Total 30m'),
     (srp3('Explanation 1', 2, 'Two brief explanations - two SRP’s @ 3m each · 12m'),
      srp3('Explanation 2', 2, 'Two brief explanations - two SRP’s @ 3m each · 12m')), '0-4', SEA + GLAC, (),
     (L(16, 'Longshore drift', nth=1), L(16, 'Plucking', nth=1))),
])
WEATHERING = ('Onion weathering', 'Carbonation', 'Freeze-thaw action.')
PART_TWO += [
    T('p2-3b-i', P2, '3B', '(i)', 4, 16, L(16, 'Weathering'),
      (L(16, '(i) Name any two factors that influence weathering.'),),
      (S(14, '(i) · Name any two factors', '(ii) · Describe and explain'),),
      (fixed('Two factors', 4, 'Two valid factors named @ 2m each · 4m', (0, 2, 4)),),
      '0-8', RW, ID + 'p2-q3b'),
    T('p2-3b-ii', P2, '3B', '(ii)', 36, 16, L(16, 'Weathering'),
      (L(16, '(ii) Describe and explain any two of the following types of weathering:', 'Freeze-thaw action.'),),
      (S(14, '(ii) · Describe and explain', 'Total 40m'),),
      (srp3('Weathering type 1', 6, 'Weathering type 1 explained 6 SRP’s @ 3m each · 18m'),
       srp3('Weathering type 2', 6, 'Weathering type 2 explained 6 SRP’s @ 3m each · 18m')),
      '0-8', RW, ID + 'p2-q3b-ii', absorbs=pool(ID + 'p2-q3b-ii-', WEATHERING, 2)[1]),
    T('p2-3c', P2, '3C', '', 30, 16, L(16, 'Plate Boundaries'),
      (L(16, 'Describe and explain what happens at constructive (separating) plate boundaries',
         'destructive (colliding) plate boundaries.'),),
      (S(15, 'Description/explanation of constructive', 'Total 30m'),),
      (srp3('Constructive', 5, 'Description/explanation of constructive 5 SRP’s @ 3m each · 15m'),
       srp3('Destructive', 5, 'Description/explanation of destructive 5 SRP’s @ 3m each · 15m')),
      '0-0', PS + EV, ID + 'p2-q3c'),
]

SHOWN = 'Shown · 4m graded (4/2/0)'
NAMED_SHOWN = sums((0, 2), (0, 2, 4))
PART_TWO.append(T(
    'p2-4a', P2, '4A', '', 30, 17, L(17, 'European Region'),
    (L(17, 'Draw a sketch map of a European region (not in Ireland) that you have studied.',
       '(upland or lowland) in this region.'),),
    (S(16, 'Outline of Region', 'Total 30m'),),
    (fixed('Outline of region', 6, 'Outline of Region · 6m graded (6/4/2/0)', (0, 2, 4, 6)),
     Criterion('River', 6, NAMED_SHOWN, 'exact', ('River: · Named · 2m', f'={SHOWN}@0')),
     Criterion('Town/City 1', 6, NAMED_SHOWN, 'exact', ('Town/City 1: · Named · 2m', f'={SHOWN}@1')),
     Criterion('Town/City 2', 6, NAMED_SHOWN, 'exact', ('Town/City 2: · Named · 2m', f'={SHOWN}@2')),
     Criterion('Relief (upland/lowland)', 6, NAMED_SHOWN, 'exact',
               ('Relief (upland/lowland): · Named · 2m', f'={SHOWN}@3'))),
    '1-5', EURO, ID + 'p2-q4a'))
Q4BI = L(17, '(i) Name two types of transport in a Continental / Sub-Continental region', 'have studied.')
Q4BIII = L(17, '(iii) Give the names of two specific tourist attractions in a Continental', 'have studied.')
PART_TWO += romans('4B', 17, L(17, 'Tertiary Economic Activities – Continental / Sub-Continental Region'), (),
                   ID + 'p2-q4b', (), [
    ('(i)', 2, Q4BI, S(17, '(i) · Name two types', '(ii) · Describe and explain'),
     (fixed('Two transport types', 2, 'Two valid transport types named @ 1m each · 2m', (0, 1, 2)),), '1-6', CONT),
    ('(ii)', 18, L(17, '(ii) Describe and explain the importance of transport in this region.'),
     S(17, '(ii) · Describe and explain', '(iii) · Give the names'),
     (srp3('Description/explanation', 6, 'Description/explanation 6 SRP’s @ 3m each · 18m'),), '1-6', CONT, (Q4BI,)),
    ('(iii)', 2, Q4BIII, S(17, '(iii) · Give the names', '(iv) · Describe and explain'),
     (fixed('Two tourist attractions', 2, 'Two valid tourist attractions named @ 1m each · 2m', (0, 1, 2)),),
     '1-6', CONT),
    ('(iv)', 18, L(17, '(iv) Describe and explain the reasons why tourists are attracted to this region.'),
     S(17, '(iv) · Describe and explain', 'Total 40m'),
     (srp3('Description/explanation', 6, 'Description/explanation 6 SRP’s @ 3m each · 18m'),), '1-6', CONT,
     (Q4BIII,)),
])
CULTURE = ('Religion', 'Language', 'Politics', 'Music/Dance', 'Sport/Games.')
PART_TWO.append(T(
    'p2-4c', P2, '4C', '', 30, 17, L(17, 'Regions and Culture'),
    (L(17, 'The culture of a region can often be determined by the following factors:', 'Sport/Games.'),
     L(17, 'Describe and explain the importance of any three of these factors', 'that you have studied.')),
    (S(17, 'Description/explanation of three factors:', 'Total 30m'),),
    (srp3('Factor 1', 4, 'Factor 1: · 4 SRP’s @ 3m each · 12m'),
     srp3('Factor 2', 3, 'Factor 2: · 3 SRP’s @ 3m each · 9m'),
     srp3('Factor 3', 3, 'Factor 3: · 3 SRP’s @ 3m each · 9m')),
    '1-3', IRL + EURO, ID + 'p2-q4c', absorbs=pool(ID + 'p2-q4c-', CULTURE, 3)[1]))

Q5AS = (L(18, 'Examine the information above and answer each of the following questions.'),)
PART_TWO += romans('5A', 18, L(18, 'Transport', nth=0), Q5AS, ID + 'p2-q5a', ('page',), [
    ('(i)', 3, L(18, '(i) What percentage of people travelled by bus in 2010?'),
     S(18, '(i) · What percentage', '(ii) · By how much'), (fixed('Percentage', 3, '38.3(%) · 3m'),), '2-0', GRAPH),
    ('(ii)', 6, L(18, '(ii) By how much, did the percentage of people travelling by train decrease', '2016?'),
     S(18, '(ii) · By how much', '(iii) · Which form'), (fixed('Decrease', 6, '1.4(%) · 6m'),), '2-0', GRAPH),
    ('(iii)', 3, L(18, '(iii) Which form of transport was most popular in 2004?'),
     S(18, '(iii) · Which form', '(iv) · Which two'), (fixed('Form of transport', 3, 'Car · 3m'),), '2-0', GRAPH),
    ('(iv)', 6, L(18, '(iv) Which two forms of transport had the same trend in usage from 2004 to 2016?'),
     S(18, '(iv) · Which two', '(v) · Explain briefly'),
     (fixed('Two forms of transport', 6, 'Train and bus · 3m + 3m', (0, 3, 6)),), '2-0', GRAPH),
    ('(v)', 6, L(18, '(v) Explain briefly one environmental problem associated with an increase', 'travelling by car.'),
     S(18, '(v) · Explain briefly', '(vi) · Explain briefly'),
     (srp3('Brief explanation', 2, 'Brief explanation 2 SRP’s @ 3m each · 6m'),), '4-5', URB + ENV),
    ('(vi)', 6, L(18, '(vi) Explain briefly one way to reduce the number of people travelling by car.'),
     S(18, '(vi) · Explain briefly', 'Total 30m'),
     (srp3('Brief explanation', 2, 'Brief explanation 2 SRP’s @ 3m each · 6m'),), '4-5', URB),
])
PART_TWO.append(T(
    'p2-5b', P2, '5B', '', 30, 18, L(18, 'Urban Regions'),
    (L(18, 'Describe and explain the growth of any one urban area that you have studied.'),),
    (S(18, 'Description/explanation 10 SRP', 'Total 30m'),),
    (srp3('Description/explanation', 10, 'Description/explanation 10 SRP’s @ 3m each · 30m'),),
    '1-3', IRL + EURO + URB, ID + 'p2-q5b'))
Q5CS = (L(18, 'Answer each of the following questions with reference to a European region', 'have studied.'),)
Q5CI = L(18, '(i) Name one example of a secondary economic activity in this region.')
PART_TWO += romans('5C', 18, L(18, 'Secondary Economic Activity in a European Region'), Q5CS, ID + 'p2-q5c', (), [
    ('(i)', 4, Q5CI, S(19, '(i) · Name one example', '(ii) · Explain the advantages'),
     (fixed('Secondary economic activity named', 4, 'Named example · 4m'),), '1-5', EURO),
    ('(ii)', 27, L(18, '(ii) Explain the advantages this region has for the development of this secondary',
                   'economic activity.'),
     S(19, '(ii) · Explain the advantages', '(iii) · Describe one challenge'),
     (srp3('Explanation', 9, 'Explanation 9 SRP’s @ 3m each · 27m'),), '1-5', EURO, (Q5CI,)),
    ('(iii)', 9, L(18, '(iii) Describe one challenge faced by this secondary economic activity in this region.'),
     S(19, '(iii) · Describe one challenge', 'Total 40m'),
     (srp3('Description', 3, 'Description 3 SRP’s @ 3m each · 9m'),), '1-5', EURO, (Q5CI,)),
])

Q6AS = (L(19, 'Examine the information above and answer each of the following questions.'),)
PART_TWO += romans('6A', 19, L(19, 'European Union – Tourism'), Q6AS, ID + 'p2-q6a', ('page',), [
    ('(i)', 6, L(19, '(i) How many million trips were made by EU residents outside their own country',
                 'did this represent?'),
     S(20, '(i) · How many million', '(ii) · What was the total'),
     (fixed('Number of trips', 3, '308(million) · 3m'), fixed('Percentage', 3, '26(%) · 3m')), '2-0', GRAPH),
    ('(ii)', 3, L(19, '(ii) What was the total amount (€ billion) spent by EU residents on all trips', 'in 2016?'),
     S(20, '(ii) · What was the total', '(iii) · Explain briefly'),
     (fixed('Total spent', 3, '428(€ billion) · 3m'),), '2-0', GRAPH),
    ('(iii)', 6, L(19, '(iii) Explain briefly one possible reason why more money was spent on trips outside',
                   '(45%) in 2016.'),
     S(20, '(iii) · Explain briefly', '(iv) · Explain briefly'),
     (srp3('Brief explanation', 2, 'Brief explanation two SRP’s @ 3m each · 6m'),), '1-5', EURO),
    ('(iv)', 6, L(19, '(iv) Explain briefly one possible reason why Spain was the most popular destination',
                  'EU residents to visit.'),
     S(20, '(iv) · Explain briefly', '(v) · Which was the third'),
     (srp3('Brief explanation', 2, 'Brief explanation two SRP’s @ 3m each · 6m'),), '1-5', EURO),
    ('(v)', 3, L(19, '(v) Which was the third most popular destination for EU residents to visit in 2016?'),
     S(20, '(v) · Which was the third', '(vi) · Name one country'), (fixed('Destination', 3, 'France · 3m'),),
     '2-0', GRAPH),
    ('(vi)', 6, L(19, '(vi) Name one country in the ‘Other’ category', 'tourist attraction in this country.'),
     S(20, '(vi) · Name one country', 'Total 30m'),
     (fixed('Country named', 3, 'Named country · 3m'), fixed('Tourist attraction named', 3,
                                                              'One valid attraction named · 3m')), '1-5', EURO),
])
Q6BS = (L(19, 'Answer each of the following with reference to an Irish region that you have studied.'),)
Q6BI = L(19, '(i) Name one primary economic activity that contributes to the economy of this', 'region.')
FACTORS_6B = ('Climate', 'Relief and soils', 'Markets')
PART_TWO += [
    T('p2-6b-i', P2, '6B', '(i)', 4, 19, L(19, 'Primary Economic Activities – Irish Region'), (Q6BI,),
      (S(21, '(i) · Name one primary', '(ii) · Explain how two'),),
      (fixed('Primary economic activity named', 4, 'Named activity · 4m'),),
      '1-4', IRL, ID + 'p2-q6b', (), Q6BS),
    T('p2-6b-ii', P2, '6B', '(ii)', 36, 19, L(19, 'Primary Economic Activities – Irish Region'),
      (L(19, '(ii) Explain how two of the factors listed below influence the development of the',
         'part (i) above:'),
       Lift(19, 'Climate', 'Markets', row=True)),
      (S(21, '(ii) · Explain how two', 'Total 40m'),),
      (srp3('Factor 1', 6, 'Factor 1: · 6 SRP’s @ 3m each · 18m'),
       srp3('Factor 2', 6, 'Factor 2: · 6 SRP’s @ 3m each · 18m')),
      '1-4', IRL, ID + 'p2-q6b-ii', (), (*Q6BS, Q6BI),
      absorbs=pool(ID + 'p2-q6b-ii-', FACTORS_6B, 2)[1]),
    T('p2-6c', P2, '6C', '', 30, 19, L(19, 'Regional Problems'),
      (L(19, 'Describe and explain two problems faced by any region that you have studied.'),),
      (S(21, 'Description/Explanation 10 SRP', 'Total 30m'),),
      (srp3('Problem 1', 5, 'Problem 1: · 5 SRP’s @ 3m each · 15m'),
       srp3('Problem 2', 5, 'Problem 2: · 5 SRP’s @ 3m each · 15m')),
      '1-0', IRL + EURO, ID + 'p2-q6c'),
]

PART_TWO.append(sketch(
    21, L(21, 'Aerial Photograph'),
    L(21, 'Examine the aerial photograph of Templemore accompanying this paper.', 'in the left background.'),
    22, ID + 'p2-q7a', '2-8', AER + ECON, ('aerial',), 'landscape',
    ('The main street in the town', 'A car park', 'A field with animals in it, in the right middleground',
     'An industrial building in the left foreground', 'An area of recreational activity in the left background')))
ACTIVITIES = ('Tourism', 'Financial services', 'Service and footloose industries.')
PART_TWO.append(T(
    'p2-7b', P2, '7B', '', 30, 21, L(21, 'Economic Development – Developed Economy'),
    (L(21, 'Describe and explain the development of one of the following economic activities',
       'Service and footloose industries.'),),
    (S(23, 'Named developed economy · 3m', 'Total 30m'),),
    (fixed('Developed economy named', 3, 'Named developed economy · 3m'),
     srp3('Description and explanation', 9, 'Description and explanation 9 SRP’s @ 3m each · 27m')),
    '3-0', ECON, ID + 'p2-q7b-tourism', routes=bullet_routes('p2-q7b-', ACTIVITIES)))
Q7CI = L(21, '(i) Name one example of environmental pollution caused by economic activity.')
PART_TWO += romans('7C', 21, L(21, 'Economic Activity - Environmental Pollution'), (), ID + 'p2-q7c', (), [
    ('(i)', 4, Q7CI, S(23, '(i) · Name one example', '(ii) · Explain the causes'),
     (fixed('Example named', 4, 'Valid named example · 4m'),), '3-4', ENV),
    ('(ii)', 24, L(21, '(ii) Explain the causes and effects of this environmental pollution.'),
     S(23, '(ii) · Explain the causes', '(iii) · Describe how'),
     (fixed('Cause identified', 3, 'Cause identified one SRP @ 3m · 3m'),
      fixed('Effect identified', 3, 'Effect identified one SRP @ 3m · 3m'),
      srp3('Explanation', 6, 'Explanation 6 SRP’s @ 3m each · 18m')), '3-4', ENV, (Q7CI,)),
    ('(iii)', 12, L(21, '(iii) Describe how this environmental pollution could be reduced.'),
     S(23, '(iii) · Describe how', 'Total 40m'),
     (srp3('Description', 4, 'Description 4 SRP’s @ 3m each · 12m'),), '3-4', ENV, (Q7CI,)),
])

Q8AS = (L(22, 'Examine the information above and answer each of the following questions.'),)
PART_TWO += romans('8A', 22, L(22, 'Employment in Ireland'), Q8AS, ID + 'p2-q8a', ('page',), [
    ('(i)', 3, L(22, '(i) How many people were employed in foreign owned companies in the South-East', 'region?'),
     S(24, '(i) · How many people', '(ii) · Which region'), (fixed('Number employed', 3, '14,918 · 3m'),),
     '2-0', GRAPH),
    ('(ii)', 3, L(22, '(ii) Which region had the second highest number of people employed in foreign owned',
                  'companies?'),
     S(24, '(ii) · Which region', '(iii) · Calculate'), (fixed('Region', 3, 'South-West · 3m'),), '2-0', GRAPH),
    ('(iii)', 6, L(22, '(iii) Calculate the number of people employed in foreign owned companies in the',
                   'combined.'),
     S(24, '(iii) · Calculate', '(iv) · What do'), (fixed('Number employed', 6, '39,082 · 6m'),), '2-0', GRAPH),
    ('(iv)', 3, L(22, '(iv) What do the letters IDA stand for?'),
     S(24, '(iv) · What do', '(v) · State one'),
     (fixed('IDA', 3, 'Industrial Development Authority/Agency · 3m'),), '3-2', MNC),
    ('(v)', 3, L(22, '(v) State one responsibility of IDA Ireland referred to in the extract above.'),
     S(24, '(v) · State one', '(vi) · Explain briefly'),
     (fixed('Responsibility', 3, 'Any valid responsibility · 3m'),), '3-2', MNC),
    ('(vi)', 12, L(22, '(vi) Explain briefly two reasons why the Dublin & Mid-East region had the highest',
                   'foreign owned companies.'),
     S(24, '(vi) · Explain briefly', 'Total 30m'),
     (srp3('Reason 1', 2, 'Reason 1: · Brief explanation 2 SRP’s @ 3m each · 6m'),
      srp3('Reason 2', 2, 'Reason 2: · Brief explanation 2 SRP’s @ 3m each · 6m')), '3-2', MNC),
])
Q8BS = (L(23, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper.'),)
Q8BII = L(23, '(ii) Name two different economic activities (other than transport) that are evident', 'the map.')
PART_TWO += romans('8B', 23, L(23, 'Economic Activity', nth=0), Q8BS, ID + 'p2-q8b', ('map', 'legend'), [
    ('(i)', 4, L(23, '(i) Name two different modes of transport that are evident on the map.'),
     S(24, '(i) · Name two different modes', '(ii) · Name two different economic'),
     (fixed('Two modes of transport', 4, 'Two valid forms of transport named @ 2m each · 4m', (0, 2, 4)),),
     '2-6', MAP + ECON),
    ('(ii)', 6, Q8BII, S(24, '(ii) · Name two different economic', '(iii) · With reference'),
     (fixed('Two economic activities', 6, 'Two valid economic activities named @ 3m each · 6m', (0, 3, 6)),),
     '3-0', ECON + MAP),
    ('(iii)', 21, L(23, '(iii) With reference to one of the economic activities named by you in part (ii), explain',
                    'economic activity.'),
     S(24, '(iii) · With reference', '(iv) · Describe and explain'),
     (srp3('Explanation', 7, 'Explanation 7 SRP’s @ 3m each · 21m'),), '3-0', ECON + MAP, (Q8BII,)),
    ('(iv)', 9, L(23, '(iv) Describe and explain any problems that might occur as a result of the transport',
                  'network on the map.'),
     S(24, '(iv) · Describe and explain', 'Total 40m'),
     (srp3('Description/explanation', 3, 'Description / Explanation 3 SRP’s @ 3m each · 9m'),), '3-0', ECON + MAP),
])
POLICIES = ('Regional Development Funds', 'Common Fisheries Policy', 'Common Agricultural Policy', 'Social Funds.')
PART_TWO.append(T(
    'p2-8c', P2, '8C', '', 30, 23, L(23, 'European Union Policy'),
    (L(23, 'Choose any one of the European Union policies listed below', 'Social Funds.'),),
    (S(25, 'Description / Explanation 10 SRP', 'Total 30m'),),
    (srp3('Description/explanation', 10, 'Description / Explanation 10 SRP’s @ 3m each · 30m'),),
    '3-3', EU, ID + 'p2-q8c-regional-development-funds', routes=bullet_routes('p2-q8c-', POLICIES)))

GRAPH_OL = (fixed('Graph paper', 3, 'Graph paper · 3m', (0, 3)),
            fixed('Vertical axis labelled / circle', 3, 'Vertical axis labelled/Circle · 3m graded (3/1/0)', (0, 1, 3)),
            fixed('Horizontal axis labelled / centred', 3, 'Horizontal axis labelled/Centred · 3m graded (3/1/0)',
                  (0, 1, 3)),
            fixed('5 items illustrated', 15, '5 items @ 3m each graded (3/1/0) · 15m', sums(*[(0, 1, 3)] * 5)))
Q9AS = (L(24, 'Examine the table above showing the value of agricultural exports', 'following questions.'),)
PART_TWO += romans('9A', 24, L(24, 'European Union Trade'), Q9AS, ID + 'p2-q9a', ('page',), [
    ('(i)', 24, L(24, '(i) Using graph paper, draw a suitable graph to illustrate this data.'),
     S(26, 'Graph paper', '(ii) · In your answer book'), GRAPH_OL, '2-0', GRAPH),
    ('(ii)', 6, L(24, '(ii) In your answer book, name two specific agricultural products exported',
                  'rest of the world.'),
     S(26, '(ii) · In your answer book', 'Total 30m'),
     (fixed('Two products', 6, 'Two valid products named @ 3m each · 6m', (0, 3, 6)),), '3-3', EU),
])
Q9BI = L(24, '(i) Name one multinational company that you have studied and state where this',
         'located in Ireland.')
PART_TWO += romans('9B', 24, L(24, 'Multinational Company'), (), ID + 'p2-q9b', (), [
    ('(i)', 4, Q9BI, S(26, '(i) · Name one multinational', '(ii) · Name one raw'),
     (fixed('MNC named', 2, 'Named MNC · 2m'), fixed('Location in Ireland', 2, 'Location in Ireland · 2m')),
     '3-2', MNC),
    ('(ii)', 6, L(24, '(ii) Name one raw material required by this multinational company and name one',
                  'this multinational company.'),
     S(26, '(ii) · Name one raw', '(iii) · Explain the advantages'),
     (fixed('Raw material named', 3, 'Raw material named · 3m'), fixed('Product named', 3, 'Product named · 3m')),
     '3-2', MNC, (Q9BI,)),
    ('(iii)', 21, L(24, '(iii) Explain the advantages of being located in Ireland for this multinational company.'),
     S(26, '(iii) · Explain the advantages', '(iv) · Explain one difficulty'),
     (srp3('Explanation', 7, 'Explanation 7 SRP’s @ 3m each · 21m'),), '3-2', MNC, (Q9BI,)),
    ('(iv)', 9, L(24, '(iv) Explain one difficulty facing this multinational company in the future.'),
     S(26, '(iv) · Explain one difficulty', 'Total 40m'),
     (srp3('Explanation', 3, 'Explanation 3 SRP’s @ 3m each · 9m'),), '3-2', MNC, (Q9BI,)),
])
Q9CI = L(24, '(i) Name one developing economy which has been colonised and name the country',
         'that colonised it.')
PART_TWO += romans('9C', 24, L(24, 'Colonialism'), (), ID + 'p2-q9c', (), [
    ('(i)', 6, Q9CI, S(27, '(i) · Name one developing', '(ii) · Describe and explain'),
     (fixed('Colonised country', 3, 'Valid colonised country · 3m'),
      fixed('Colonising country', 3, 'Valid colonising country · 3m')), '3-1', DEV),
    ('(ii)', 24, L(24, '(ii) Describe and explain the effects that colonialism has had on this developing',
                   'economy.'),
     S(27, '(ii) · Describe and explain', 'Total 30m'),
     (srp3('Description/explanation', 8, 'Description / Explanation 8 SRP’s @ 3m each · 24m'),), '3-1', DEV,
     (Q9CI,)),
])

Q10AS = (L(25, 'Examine the table above showing the percentage of the world’s population living in urban',
           'following questions.'),)
PART_TWO += romans('10A', 25, L(25, 'Urban Settlement', nth=0), Q10AS, ID + 'p2-q10a', ('page',), [
    ('(i)', 24, L(25, '(i) Using graph paper, draw a suitable graph to illustrate this data.'),
     S(28, 'Graph paper', '(ii) · In your answer book'), GRAPH_OL, '2-0', GRAPH),
    ('(ii)', 6, L(25, '(ii) In your answer book, calculate the total percentage of the world’s population',
                  'in 2016.'),
     S(28, '(ii) · In your answer book', 'Total 30m'), (fixed('Total percentage', 6, '55(%) · 6m'),),
     '2-0', GRAPH + URB),
])
Q10BI = L(25, '(i) Name one example of an urban area where traffic congestion is a problem.')
PART_TWO += romans('10B', 25, L(25, 'Traffic Congestion'), (), ID + 'p2-q10b', (), [
    ('(i)', 3, Q10BI, S(28, '(i) · Name one example', '(ii) · Describe and explain'),
     (fixed('Urban area named', 3, 'Named example · 3m'),), '4-5', URB),
    ('(ii)', 27, L(25, '(ii) Describe and explain the measures that can be taken in urban areas to solve the',
                   'traffic congestion.'),
     S(28, '(ii) · Describe and explain', 'Total 30m'),
     (srp3('Description/explanation', 9, 'Description / Explanation 9 SRP’s @ 3m each · 27m'),), '4-5', URB),
])
PART_TWO += romans('10C', 25, L(25, 'Migration', nth=0), (), ID + 'p2-q10c', (), [
    ('(i)', 10, L(25, '(i) Explain briefly each of the following terms:', 'Receiver region in the context of migration.'),
     S(29, '(i) · Explain briefly', '(ii) · Discuss both'),
     (srp('Donor region explained', 2, 'Donor region explained 2 SRP’s @ 2m each · 4m', 2),
      srp3('Receiver region explained', 2, 'Receiver region explained 2 SRP’s @3m each · 6m')), '4-2', POP, (),
     (L(25, 'Donor region in the context of migration'), L(25, 'Receiver region in the context of migration'))),
    ('(ii)', 30, L(25, '(ii) Discuss both the positive and negative impacts of migration.'),
     S(29, '(ii) · Discuss both', 'Total 40m'),
     (srp3('Discussion', 10, 'Discussion 10 SRP’s @ 3m each · 30m'),), '4-2', POP),
])

PART_TWO.append(sketch(
    26, L(26, 'Aerial Photograph'),
    L(26, 'Examine the aerial photograph of Templemore accompanying this paper.', 'An area of recreational activity.'),
    30, ID + 'p2-q11a', '2-8', AER + URB, ('aerial',), 'landscape',
    ('A three storey building in the right foreground', 'The Central Business District (CBD)', 'A church',
     'An area of semi-detached housing in the left background', 'An area of recreational activity')))
Q11BI = L(26, '(i) Name one city in the developing world that is growing rapidly.')
PART_TWO += romans('11B', 26, L(26, 'Developing World City'), (), ID + 'p2-q11b', (), [
    ('(i)', 4, Q11BI, S(31, '(i) · Name one city', '(ii) · State three'),
     (fixed('Developing world city named', 4, 'Developing City named · 4m'),), '4-5', URB),
    ('(ii)', 9, L(26, '(ii) State three factors that influence the growth of this developing world city.'),
     S(31, '(ii) · State three', '(iii) · Describe and explain'),
     (fixed('Factor 1', 3, 'Factor 1: · 3m'), fixed('Factor 2', 3, 'Factor 2: · 3m'),
      fixed('Factor 3', 3, 'Factor 3: · 3m')), '4-5', URB, (Q11BI,)),
    ('(iii)', 27, L(26, '(iii) Describe and explain any three problems associated with the rapid growth of this',
                    'developing world city.'),
     S(31, '(iii) · Describe and explain', 'Total 40m'),
     (srp3('Description/explanation', 9, 'Description / Explanation 9 SRP’s @ 3m each · 27m'),), '4-5', URB,
     (Q11BI,)),
])
FACTORS_11C = ('Medical technology', 'Culture and society', 'Income levels', 'Resources.')
PART_TWO.append(T(
    'p2-11c', P2, '11C', '', 30, 26, L(26, 'Population Change'),
    (L(26, 'The characteristics of Ireland’s population have changed over time due to many factors.'),
     L(26, 'Explain how any three of the following factors have impacted on Ireland’s population', 'Resources.')),
    (S(31, 'Factor 1: · 4 SRP', 'Total 30m'),),
    (srp3('Factor 1', 4, 'Factor 1: · 4 SRP’s @ 3m each · 12m'),
     srp3('Factor 2', 3, 'Factor 2: · 3 SRP’s @ 3m each · 9m'),
     srp3('Factor 3', 3, 'Factor 3: · 3 SRP’s @ 3m each · 9m')),
    '4-1', POP, ID + 'p2-q11c', absorbs=pool(ID + 'p2-q11c-', FACTORS_11C, 3)[1]))

Q12AS = (L(27, 'Examine the table above and answer each of the following questions.'),)
PART_TWO += romans('12A', 27, L(27, 'Emigration - Ireland'), Q12AS, ID + 'p2-q12a', ('page',), [
    ('(i)', 3, L(27, '(i) How many Irish people emigrated to the UK in 2017?'),
     S(32, '(i) · How many Irish', '(ii) · To which'), (fixed('Number of emigrants', 3, '12,100 · 3m'),),
     '2-0', GRAPH),
    ('(ii)', 3, L(27, '(ii) To which destination was there a decrease in Irish emigrants between 2008 and 2013?'),
     S(32, '(ii) · To which', '(iii) · Calculate'), (fixed('Destination', 3, 'Australia · 3m'),), '2-0', GRAPH),
    ('(iii)', 6, L(27, '(iii) Calculate the total number of Irish emigrants to the USA in the three years', 'combined.'),
     S(32, '(iii) · Calculate', '(iv) · Where did'), (fixed('Total', 6, '21,800 · 6m'),), '2-0', GRAPH),
    ('(iv)', 3, L(27, '(iv) Where did the least number of people emigrate to in 2013?'),
     S(32, '(iv) · Where did', '(v) · Where did'), (fixed('Destination', 3, 'Australia · 3m'),), '2-0', GRAPH),
    ('(v)', 3, L(27, '(v) Where did the least number of people emigrate to in 2017?'),
     S(32, '(v) · Where did', '(vi) · Explain briefly'), (fixed('Destination', 3, 'USA · 3m'),), '2-0', GRAPH),
    ('(vi)', 6, L(27, '(vi) Explain briefly one reason why the total number of Irish emigrants was at its highest',
                  'in 2013.'),
     S(32, '(vi) · Explain briefly', '(vii) · Explain briefly'),
     (srp3('Brief explanation', 2, 'Brief explanation two SRP’s @ 3m each · 6m'),), '4-2', POP),
    ('(vii)', 6, L(27, '(vii) Explain briefly one positive impact of emigration on Ireland.'),
     S(32, '(vii) · Explain briefly', 'Total 30m'),
     (srp3('Brief explanation', 2, 'Brief explanation two SRP’s @ 3m each · 6m'),), '4-2', POP),
])
Q12BI = L(27, '(i) Name one urban area you have studied.')
PART_TWO += romans('12B', 27, L(27, 'Urban Land-Use'), (), ID + 'p2-q12b', (), [
    ('(i)', 3, Q12BI, S(32, '(i) · Name one urban', '(ii) · Name two land-uses'),
     (fixed('Urban area named', 3, 'Named urban area · 3m'),), '4-4', URB),
    ('(ii)', 6, L(27, '(ii) Name two land-uses in this urban area.'),
     S(32, '(ii) · Name two land-uses', '(iii) · Describe and explain'),
     (fixed('Two land-uses', 6, 'Two named land-uses · 6m'),), '4-4', URB, (Q12BI,)),
    ('(iii)', 21, L(27, '(iii) Describe and explain how these urban land-uses have changed over time.'),
     S(32, '(iii) · Describe and explain', 'Total 30m'),
     (srp3('Description/explanation', 7, 'Description / Explanation 7 SRP’s @ 3m each · 21m'),), '4-4', URB,
     (Q12BI,)),
])
Q12CS = (L(27, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper and',
           'following questions.'),)
Q12CI = L(27, '(i) Name three different rural settlement patterns evident on the map', 'an example of each.')
PART_TWO += romans('12C', 27, L(27, 'Rural Settlement Patterns'), Q12CS, ID + 'p2-q12c', ('map', 'legend'), [
    ('(i)', 22, Q12CI, S(33, '(i) · Name three different', '(ii) · Describe and explain'),
     (fixed('Pattern 1 named', 4, 'Pattern 1 named: · 4m'), fixed('Pattern 2 named', 3, 'Pattern 2 named: · 3m'),
      fixed('Pattern 3 named', 3, 'Pattern 3 named: · 3m'),
      *(fixed(f'Grid reference {n}', 4, f'Grid reference {n}: · 4m graded (4/2/0)', (0, 2, 4)) for n in (1, 2, 3))),
     '4-3', URB + MAP),
    ('(ii)', 18, L(27, '(ii) Describe and explain each of the three rural settlement patterns named by you in',
                   'part (i) above.'),
     S(33, '(ii) · Describe and explain', 'Total 40m'),
     tuple(srp3(f'Pattern {n}', 2, f'Pattern {n}: · 2 SRP’s @ 3m each · 6m') for n in (1, 2, 3)),
     '4-3', URB + MAP, (Q12CI,)),
])

TASKS = [*PART_ONE, *PART_TWO]

ID_CORRECTION_REASON = 'No 2019 Ordinary card shipped before this review; every card is new.'

# No 2019 Ordinary card was live on origin/main before this review.
LEGACY_IDS: list[str] = []
