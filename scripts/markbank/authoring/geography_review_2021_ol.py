"""Independent review ledger: Leaving Certificate Geography 2021 Ordinary Level.

Sources (English editions, Paper Trail index; sizes and SHA-256 pinned in
EXPECTED_SOURCES and the generated audit): Part One and Answerbook
LC005GLP042EV (40 pages), Part Two LC005GLP043EV (20 pages), marking scheme
LC005GLP000EV (36 pages), and the common companions shared with Higher Level
in the harvested corpus — the 1:50 000 Foxford map LC005CLP003EV, its legend
LC005CLPC00EV (a PDF this year) and the Foxford aerial photograph
LC005CLP004EV (published only as a JPEG).

Visual sweep (every page rendered and read on 2026-10-12):
  Part One booklet p1 cover (2021: Part One 100 marks, Part Two 200, and the
  note that the 2021 papers were adjusted for COVID-19 disruption); p2
  instructions (Part One "Attempt any TEN"; Part Two "attempt TWO", each
  from a different section); p3-p12 Questions 1-12 (p6 holds Q4 and Q5, p7
  Q6 and Q7; Q8 prints four sections cut from the aerial photograph); p13
  Part Two answerbook instructions; p14-p17 graph paper; p18-p39 lined answer
  pages; p40 copyright/back cover.
  Part Two booklet p1 cover; p2 Part Two instructions; p3-p10 Sections 1-2
  (Q1-Q6; p5 holds only 2C, p9 only 5C); p11 Section 3 divider; p12-p17
  Electives (Q7-Q12); p18-p19 "Do not hand this up"; p20 copyright/back
  cover.
  Scheme p1 cover; p2-p3 notes; p4 Geographical Investigation (coursework,
  not a written-paper task); p5 presentation breakdown; p6-p7 Part One table;
  p8 Part Two instructions; p9-p20 Q1-Q6; p21 Section 3 divider; p22-p33
  Q7-Q12; p34 investigation topics; p35 Irish-language bonus marks; p36 back
  cover.
  Companions: Foxford map extract (Lough Cullin, the River Moy, the Clydagh
  River, Griffins Island); OS legend sheet; oblique aerial photograph of
  Foxford.

Companions. Part One Q6, Q7 (map, legend) and Q8 (page, aerial); Part Two
1A, 9B, 11C and 12C (map, legend), 8A and 10A (aerial) were held back
before this review because their companions were not wired. Each now
carries the exact official documents it names.

Tariffs as printed: twelve parts carry 40 marks (1B, 2B, 3B, 4B, 5C, 6B,
7B, 8B, 9B, 10B, 11B, 12C) and the rest 30 — 5B and 12B are 30 and 5C and
12C 40 — and QUESTION_TARIFFS follows each printed [Nm]. An SRP is 3 marks;
"a+b" lines are one criterion with partial credit a; graded lines keep
their printed grades; sketch items are "showing 3 (3/1/0) + labelled 2";
4A items are "named 2 + shown 4 (4/2/0)"; 11C reasons are "OS map evidence
1 + 3 SRPs". 10A prints four bullets, two of them plural ("Two connecting
streets", "Two churches"), and the scheme prices five items; the five item
criteria stay unlabelled rather than guess which bullet the scheme counts
twice.

Boundaries follow the 2022 Ordinary ledger: every priced roman is a task; a
matching table under ONE printed instruction stays one task with a criterion
per scheme row, the scheme listing its answers in the printed row order: Q1
Stalactite=B, Swallow hole=D, Cave/Cavern=A, Pillar/Column=C; Q2 prints (i)
and (ii) in one part-completed table: (i) Cliff=D, Beach=A, Sea arch=B (Sea
stump C is printed), (ii) Beach Deposition, Sea stump Erosion (the other two
ticks are printed); Q3 likewise: (i) Rock fall=A, Soil creep=D, Avalanche=C
(Mud flow B is printed), (ii) Soil creep Slow, Mud flow Fast; Q4
Drumlin=B, Clint=C, Spit=E, Waterfall=D, Levee=A; Q5 Paris=B, Cool
Temperate Oceanic=D, Wallonia=C, Westmeath County Council=A, Munster Ridge
and Valley=E; Q8(i) A Right background, B Left middleground, C Centre
middleground, D Right middleground; Q10(iv) Miner Primary, Teacher
Tertiary; Q12 San Quentin Glacier=B, Hurricane Dorian=E, Salt production=C,
Crop farming=D, Popocatepetl=A; Part Two 3A(i) B Scree slope, A Limestone
pavement, C Tombolo, 3A(ii) C Coastal deposition, B Physical/mechanical
weathering, A Chemical weathering.
"""

from geography_review import (
    Criterion, Lift, Route, SchemeSlice, Task, pool, fixed, slug, srp, steps, sums,
)

YEAR = 2021
LEVEL = 'ordinary'
PAPER_PAGES = {1: 40, 2: 20}
SCHEME_PAGES = 36
_FORTY = {'1B', '2B', '3B', '4B', '5C', '6B', '7B', '8B', '9B', '10B', '11B', '12C'}
QUESTION_TARIFFS = {1: {str(n): 10 for n in range(1, 13)},
                    2: {f'{n}{x}': (40 if f'{n}{x}' in _FORTY else 30)
                        for n in range(1, 13) for x in 'ABC'}}

EXPECTED_SOURCES = {
    'paper1': ('LC005GLP042EV.pdf', 3122464),
    'paper2': ('LC005GLP043EV.pdf', 1563288),
    'scheme': ('LC005GLP000EV.pdf', 377961),
    'map': ('LC005CLP003EV.pdf', 5155375),
    'legend': ('LC005CLPC00EV.pdf', 784643),
    'aerial': ('LC005CLP004EV.jpg', 5536812),
}

PAGE_REVIEW = {
    'paper1': {1: 'cover', 2: 'instructions', **{p: 'question' for p in range(3, 13)},
               13: 'answerbook instructions', **{p: 'graph-paper answer page' for p in range(14, 18)},
               **{p: 'lined answer page' for p in range(18, 40)}, 40: 'copyright/back cover'},
    'paper2': {1: 'cover', 2: 'Part Two instructions',
               **{p: 'question' for p in (*range(3, 11), *range(12, 18))},
               11: 'section divider', 18: 'do not hand this up', 19: 'do not hand this up',
               20: 'copyright/back cover'},
    'scheme': {1: 'cover', 2: 'notes', 3: 'notes', 4: 'geographical investigation (coursework)',
               5: 'investigation presentation breakdown', 6: 'Part One table', 7: 'Part One table',
               8: 'Part Two instructions', **{p: 'Part Two allocation' for p in range(9, 21)},
               21: 'section divider', **{p: 'Part Two allocation' for p in range(22, 34)},
               34: 'investigation topics', 35: 'Irish-language bonus marks', 36: 'back cover'},
}

EXPECTED_SELECTION_SCAN = [
    [1, 2, 'attempt any ten'], [1, 2, 'attempt two'], [1, 3, 'attempt any ten'],
    [2, 2, 'attempt two'],
    [2, 4, 'answer (i) or (ii)'], [2, 4, 'any two'], [2, 4, 'any two'],
    [2, 5, 'one of the following'],
    [2, 6, 'one of the following'],
    [2, 7, 'any two'],
    [2, 8, 'any one'],
    [2, 10, 'any two'],
    [2, 13, 'one of the following'],
    [2, 17, 'any two'],
]
SELECTION_REVIEW = [
    {'scan': [[1, 2, 'attempt any ten'], [1, 2, 'attempt two'], [1, 3, 'attempt any ten'],
              [2, 2, 'attempt two']],
     'kind': 'exam-attempt-rule',
     'reason': 'Part One any ten of twelve and Part Two two questions from different sections are attempt rules; every question is carded.'},
    {'scan': [[2, 4, 'answer (i) or (ii)']], 'kind': 'closed-route',
     'reason': '2B: (i) or (ii) -> two routes, each with its own scheme allocation.'},
    {'scan': [[2, 5, 'one of the following']], 'kind': 'closed-choose-one',
     'reason': '2C: one of four printed interactions with the rock cycle -> four routes.'},
    {'scan': [[2, 6, 'one of the following']], 'kind': 'closed-choose-one',
     'reason': '3C: one of three printed surface processes -> three routes.'},
    {'scan': [[2, 13, 'one of the following']], 'kind': 'closed-choose-one',
     'reason': '8C: one of three printed economic activities -> three routes.'},
    {'scan': [[2, 7, 'any two'], [2, 10, 'any two']], 'kind': 'choose-n-one-card',
     'reason': '4C any two of four printed region types and 6B any two of three printed headings -> one card each with every printed item (choice is not a route; the scheme marks each chosen item alike).'},
    {'scan': [[2, 4, 'any two'], [2, 4, 'any two'], [2, 8, 'any one'], [2, 17, 'any two']],
     'kind': 'open-response',
     'reason': 'No printed pool: 2B(i) any two landforms and 2B(ii) any two mass movement processes (the scheme prices two @ 20m); 5B any one urban area; 12B(ii) any two functions. 6C "two problems", 11C "three reasons" and 12C "three different rural settlement patterns" are open too.'},
]

P1, P2 = 1, 2
ID = 'geography-2021-ol-'
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


def bullet_routes(prefix, items, atlas=None):
    return tuple(Route(slug(item, 34), item.rstrip('.'), ID + prefix + slug(item, 34), True,
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


def part_one_romans(q, page, title, stem, first_legacy, sources, parts):
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
                     first_legacy and index == 0, sources, stem, row_labels=labels))
    return out


# ---------------------------------------------------------------- Part One --
TICK = 'Tick (✓) the correct box.'
Q1S = (L(3, 'Examine the diagram above which shows a karst landscape', 'following questions.'),)
Q2S = (L(4, 'Examine the photograph above.', 'completed for you.'),)
Q3S = (L(5, 'Examine the photographs above showing different types of mass movement.', 'completed for you.'),)
Q6S = (L(7, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper.', nth=0),)
Q7S = (L(7, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper.', nth=1),)
Q8S = (L(8, 'Examine the aerial photograph accompanying this paper, and the sections from it below',
         'following questions.'),)
Q9S = (L(9, 'Examine the weather chart above and answer each of the following questions.'),)
Q10S = (L(10, 'Examine the stacked bar chart above', 'following questions.'),)
Q11S = (L(11, 'Examine the table above showing the total monthly rainfall', 'following questions.'),)

PART_ONE = part_one_romans('1', 3, L(3, 'Karst Landscape'), Q1S, True, ('page',), [
    ('(i)', L(3, '(i) Match each of the letters A, B, C and D with the term', 'most associated with it.'),
     'Q1. (i)', 'Q.1 (ii)', rows(['Q1. (i) · B · 2m', '=D · 2m', '=A · 2m', '=C · 2m']), '0-3', KARST,
     (L(3, 'Stalactite'), L(3, 'Swallow hole'), L(3, 'Cave/Cavern'), L(3, 'Pillar/Column'))),
    ('(ii)', L(3, '(ii) Name one location in Ireland that has a karst landscape.'), 'Q.1 (ii)', 'Q.2 (i)',
     (fixed('Location', 2, 'Q.1 (ii) · Any valid location · 2m · Total 10m'),), '0-3', KARST),
])

PART_ONE += [
    T('p1-2-i', P1, '2', '(i)', 6, 4, L(4, 'Coasts'),
      (L(4, '(i) Match each of the letters A, B, C and D with the feature', 'table below.'),),
      (S(6, 'Q.2 (i)', '(C) Erosion'),),
      (fixed('Row 1', 2, 'Q.2 (i) · D Q.2 (ii) (Erosion) · 2m'), fixed('Row 2', 2, 'A Deposition · 2m + 2m'),
       fixed('Row 3', 2, 'B (Erosion) · 2m')),
      '0-10', SEA, ID + 'p1-q2', True, ('page',), Q2S,
      row_labels=(L(4, 'Cliff'), L(4, 'Beach'), L(4, 'Sea arch'))),
    T('p1-2-ii', P1, '2', '(ii)', 4, 4, L(4, 'Coasts'),
      (L(4, '(ii) Indicate, by ticking the correct box', 'the processes of deposition.'),),
      (S(6, 'A Deposition', 'B (Erosion)'), S(6, '(C) Erosion', 'Q.3')),
      (fixed('Row 1', 2, 'A Deposition · 2m + 2m'), fixed('Row 2', 2, '(C) Erosion · 2m · Total 10m')),
      '0-10', SEA, ID + 'p1-q2-ii', False, ('page',), Q2S,
      row_labels=(L(4, 'Beach'), L(4, 'Sea stump'))),
    T('p1-3-i', P1, '3', '(i)', 6, 5, L(5, 'Mass Movement'),
      (L(5, '(i) Match each of the photographs A, B, C, and D with the type of mass movement', 'table below.'),),
      (S(6, 'Q.3 (i)', '(B) Fast'),),
      (fixed('Row 1', 2, 'Q.3 (i) · A Q.3 (ii) (Fast) · 2m'), fixed('Row 2', 2, 'D Slow · 2m + 2m'),
       fixed('Row 3', 2, 'C (Fast) · 2m')),
      '0-8', RW, ID + 'p1-q3', True, ('page',), Q3S,
      row_labels=(L(5, 'Rock fall'), L(5, 'Soil creep'), L(5, 'Avalanche'))),
    T('p1-3-ii', P1, '3', '(ii)', 4, 5, L(5, 'Mass Movement'),
      (L(5, '(ii) Indicate, by ticking the correct box', 'fast or slow process.'),),
      (S(6, 'D Slow', 'C (Fast)'), S(6, '(B) Fast', 'Q.4')),
      (fixed('Row 1', 2, 'D Slow · 2m + 2m'), fixed('Row 2', 2, '(B) Fast · 2m · Total 10m')),
      '0-8', RW, ID + 'p1-q3-ii', False, ('page',), Q3S,
      row_labels=(L(5, 'Soil creep'), L(5, 'Mud flow'))),
    T('p1-4', P1, '4', '', 10, 6, L(6, 'Physical Processes'),
      (L(6, 'Match the physical process with the feature most associated with it', 'in the table below.'),),
      (S(6, 'Q.4', 'Q.5'),), rows(['Q.4 · B · 2m', '=C · 2m', '=E · 2m', '=D · 2m', 'A · 2m · Total 10m']),
      '0-4', GLAC + KARST + SEA + RIVERS + RW, ID + 'p1-q4', True, ('page',),
      row_labels=(L(6, 'Drumlin'), L(6, 'Clint'), L(6, 'Spit'), L(6, 'Waterfall'), L(6, 'Levee'))),
    T('p1-5', P1, '5', '', 10, 6, L(6, 'Regions'),
      (L(6, 'Match the type of region with the example of the region', 'in the table below.'),),
      (S(6, 'Q.5', 'Q.6 (i)'),), rows(['Q.5 · B · 2m', '=D · 2m', '=C · 2m', '=A · 2m', 'E · 2m · Total 10m']),
      '1-0', IRL + EURO, ID + 'p1-q5', True, ('page',),
      row_labels=(L(6, 'Paris'), L(6, 'Cool Temperate Oceanic'), L(6, 'Wallonia, Belgium'),
                  L(6, 'Westmeath County Council'), L(6, 'Munster Ridge and Valley'))),
]

PART_ONE += part_one_romans('6', 7, L(7, 'Ordnance Survey Map', nth=0), Q6S, False, ('map', 'legend'), [
    ('(i)', (L(7, '(i) What is the total area of the map?', TICK), L(7, '99 km2'), L(7, '108 km2')),
     'Q.6 (i)', '(ii) · 5.0 km', (fixed('Area', 5, 'Q.6 (i) · 108 km2 · 5m'),), '2-6', MAP),
    ('(ii)', (L(7, '(ii) What is the length of the railway', TICK), L(7, '3.5 km'), L(7, '5.0 km')),
     '(ii) · 5.0 km', None, (fixed('Length', 5, '(ii) · 5.0 km · 5m · Total 10m'),), '2-6', MAP),
])

PART_ONE += part_one_romans('7', 7, L(7, 'Ordnance Survey Map', nth=1), Q7S, False, ('map', 'legend'), [
    ('(i)', L(7, '(i) Name the antiquity that can be found at each of the following grid references:'),
     'Q.7 (i)', '(ii) · Mixed', rows(['Q.7 (i) · Castle · 2m', 'Crannog · 2m', 'Cillín · 2m']), '2-6', MAP,
     (L(7, 'G 262 009:'), L(7, 'G 301 033:'), L(7, 'G 263 063:'))),
    ('(ii)', (L(7, '(ii) Indicate the type of woodland found at G 287 043', 'the correct box.'),
              L(7, 'Coniferous plantation'), L(7, 'Deciduous woodland'), L(7, 'Mixed woodland')),
     '(ii) · Mixed woodland', '(iii) · Correctly', (fixed('Woodland', 2, '(ii) · Mixed woodland · 2m'),),
     '2-6', MAP),
    ('(iii)', L(7, '(iii) Draw the Ordnance Survey map symbol for a viewpoint in the space below.'),
     '(iii) · Correctly', 'Q.8 (i)', (fixed('Symbol', 2, '(iii) · Correctly drawn symbol · 2m · Total 10m'),),
     '2-6', MAP),
])

PART_ONE += part_one_romans('8', 8, L(8, 'Aerial Photograph'), Q8S, False, ('page', 'aerial'), [
    ('(i)', L(8, '(i) Give the location of each of the sections from the aerial photograph', 'etc.).'),
     'Q.8 (i)', '(ii) · Oblique',
     (fixed('A', 2, 'Q.8 (i) · Right background · 2m'), fixed('B', 2, 'Left middleground · 2m'),
      fixed('C', 2, 'Centre middleground · 2m'), fixed('D', 2, 'Right middleground · 2m')), '2-8', AER),
    ('(ii)', (L(8, '(ii) Indicate whether the aerial photograph accompanying this paper is a vertical',
                'the correct box.'), L(8, 'Vertical'), L(8, 'Oblique')),
     '(ii) · Oblique', 'Q.9', (fixed('Vertical or oblique', 2, '(ii) · Oblique · 2m · Total 10m'),), '2-8', AER),
])

PART_ONE += part_one_romans('9', 9, L(9, 'Weather Charts'), Q9S, True, ('page',), [
    ('(i)', L(9, '(i) What is the barometric pressure', 'marked X?'), 'Q.9 (i)', '(ii) · False',
     (fixed('Pressure', 2, 'Q.9 (i) 971 (hectopascals/millibars) · 2m'),), '2-7', WEATHER),
    ('(ii)', (L(9, '(ii) Indicate whether the following statement is true or false', 'the correct box.'),
              L(9, 'Ireland and Italy are experiencing the same type of weather conditions.')),
     '(ii) · False', '(iii) · High', (fixed('True or false', 2, '(ii) · False · 2m'),), '2-7', WEATHER),
    ('(iii)', L(9, '(iii) What does the letter H on the weather chart indicate?'), '(iii) · High', '(iv) · Correctly',
     (fixed('Meaning', 2, '(iii) · High pressure · 2m'),), '2-7', WEATHER),
    ('(iv)', L(9, '(iv) In the box below, draw the weather chart symbol for a cold front.'),
     '(iv) · Correctly', '(v) · Isobars', (fixed('Symbol', 2, '(iv) · Correctly drawn symbol · 2m'),),
     '2-7', WEATHER),
    ('(v)', (L(9, '(v) The black lines on this weather map', TICK), L(9, 'Isobars'), L(9, 'Isotherms')),
     '(v) · Isobars', 'Q.10', (fixed('Name', 2, '(v) · Isobars · 2m · Total 10m'),), '2-7', WEATHER),
])

PART_ONE += part_one_romans('10', 10, L(10, 'Economic Activities', nth=0), Q10S, True, ('page',), [
    ('(i)', L(10, '(i) What percentage of people in Australia are employed in secondary economic activities?'),
     'Q.10 (i)', '(ii) · Niger', (fixed('Percentage', 2, 'Q.10 (i) 21 (%) · 2m'),), '2-0', GRAPH),
    ('(ii)', L(10, '(ii) Which country has the highest percentage of people employed in primary economic',
               'activities?'),
     '(ii) · Niger', '(iii) · 41', (fixed('Country', 2, '(ii) · Niger · 2m'),), '2-0', GRAPH),
    ('(iii)', L(10, '(iii) Calculate the difference between the percentage', 'in Vietnam.'),
     '(iii) · 41', '(iv) · Primary', (fixed('Difference', 2, '(iii) · 41 (%) · 2m'),), '2-0', GRAPH),
    ('(iv)', L(10, '(iv) Indicate whether each of the following jobs', 'the correct box.'),
     '(iv) · Primary', 'Q.11', (fixed('Row 1', 2, '(iv) · Primary · 2m'), fixed('Row 2', 2, 'Tertiary · 2m · Total 10m')),
     '3-0', ECON, (L(10, 'Miner'), L(10, 'Teacher'))),
])

PART_ONE += part_one_romans('11', 11, L(11, 'Weather Statistics'), Q11S, True, ('page',), [
    ('(i)', L(11, '(i) What was the total monthly rainfall (in mm) for March 2019 at Ballyhaise', 'station?'),
     'Q.11 (i)', '(ii) · August', (fixed('Rainfall', 2, 'Q.11 (i) 149 (millimetres) · 2m'),), '2-0',
     GRAPH + WEATHER),
    ('(ii)', L(11, '(ii) In which month was rainfall the highest at Belmullet weather station in 2019?'),
     '(ii) · August', '(iii) · Four', (fixed('Month', 2, '(ii) · August · 2m'),), '2-0', GRAPH + WEATHER),
    ('(iii)', L(11, '(iii) At Ballyhaise weather station, how many months had a rainfall level', '60 mm?'),
     '(iii) · Four', '(iv) · Belmullet', (fixed('Number of months', 2, '(iii) · Four · 2m'),), '2-0',
     GRAPH + WEATHER),
    ('(iv)', L(11, '(iv) Which weather station had more rainfall in 2019?'), '(iv) · Belmullet', '(v) · Rain',
     (fixed('Weather station', 2, '(iv) · Belmullet · 2m'),), '2-0', GRAPH + WEATHER),
    ('(v)', L(11, '(v) Name the weather instrument used to measure rainfall.'), '(v) · Rain', 'Q.12',
     (fixed('Instrument', 2, '(v) · Rain gauge · 2m · Total 10m'),), '2-7', WEATHER),
])

PART_ONE.append(T(
    'p1-12', P1, '12', '', 10, 12, L(12, 'Satellite Interpretation'),
    (L(12, 'Match each satellite image, A to E, with the most suitable description', 'table below.'),),
    (S(7, 'Q.12', None),), rows(['Q.12 · B · 2m', '=E · 2m', '=C · 2m', '=D · 2m', 'A · 2m · Total 10m']),
    '2-8', AER, ID + 'p1-q12', True, ('page',),
    row_labels=(L(12, 'San Quentin Glacier, Chile'), L(12, 'Hurricane Dorian off the coast of Florida, USA'),
                L(12, 'Salt production in Thar Desert, India'), L(12, 'Crop farming in Minnesota, USA'),
                L(12, 'Popocatépetl Volcano Eruption, Mexico'))))


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


def sketch(page, title, prompt, scheme_page, card_id, topic, atlas, sources, proportions, bullets):
    item = sums((0, 1, 3), (0, 2))
    labels = (None, None, None, *(L(page, b) for b in bullets)) if bullets else ()
    return T(f'p2-{card_id.rsplit("-q", 1)[1]}', P2, card_id.rsplit('-q', 1)[1].upper(), '', 30, page,
             title, (prompt,), (S(scheme_page, 'Sketch Outline:', 'Total 30m'),),
             (fixed('Limits/frame', 1, ('Sketch Outline:', 'imits/')),
              fixed(f'Proportions ({proportions})', 2, f'Proportions ({proportions}) · 2m'),
              fixed('Overall impression', 2, '2m graded (2/1/0)', (0, 1, 2)),
              *(Criterion(f'Item {n}', 5, item, 'exact',
                          ('Five items shown and labelled as follows:', 'Showing · 3m graded (3/1/0)',
                           'Labelled · 2m')) for n in range(1, 6))),
             topic, atlas, card_id, False, sources, row_labels=labels)


def two_of(label, count, head, each, lines, unit):
    per = sums(*unit)
    return tuple(Criterion(f'{label} {n}', count, per, 'srp', (head, each, *lines)) for n in (1, 2))


PART_TWO = [
    sketch(3, L(3, 'Ordnance Survey Map'),
           L(3, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper.',
             'The entire course of the Clydagh River.'),
           9, ID + 'p2-q1a', '2-6', MAP, ('map', 'legend'), 'portrait',
           ('Lough Cullin', 'Griffins Island', 'An area of mixed woodland',
            'The entire area of land above 200 metres in the north-east of the map',
            'The entire course of the Clydagh River')),
]
PART_TWO += romans('1B', 3, L(3, 'Volcanoes'), (), ID + 'p2-q1b', (), [
    ('(i)', 4, L(3, '(i) Name two examples of volcanoes.'), S(10, '(i) · Name two examples', '(ii) · Discuss'),
     (fixed('Two examples', 4, 'Two examples @ 2m each · 4m', (0, 2, 4)),), '0-7', EV),
    ('(ii)', 18, L(3, '(ii) Discuss the positive effects of volcanoes.'),
     S(10, '(ii) · Discuss the positive', '(iii) Discuss'),
     (srp3('Discussion', 6, '6 SRP’s @ 3m each · 18m'),), '0-7', EV),
    ('(iii)', 18, L(3, '(iii) Discuss the negative effects of volcanoes.'),
     S(10, '(iii) Discuss the negative', '1C. Rocks'),
     (srp3('Discussion', 6, '6 SRP’s @ 3m each · 18m'),), '0-7', EV),
])
PART_TWO += romans('1C', 3, L(3, 'Rocks'), (), ID + 'p2-q1c', (), [
    ('(i)', 6, L(3, '(i) Name one example of a sedimentary rock and state an Irish location', 'found.'),
     S(10, '(i) · Name one example of a sedimentary', '(ii) · Describe'),
     (fixed('Sedimentary rock named', 3, 'Sedimentary rock named · 3m'),
      fixed('Irish location', 3, 'Valid location stated · 3m')), '0-1', RW),
    ('(ii)', 24, L(3, '(ii) Describe and explain how sedimentary rocks are formed.'),
     S(10, '(ii) · Describe and explain how sedimentary', 'Total 30m'),
     (srp3('Description/explanation', 8, 'Description/Explanation 8 SRP’s @ 3m each 24m'),), '0-1', RW),
])

Q2AS = (L(4, 'Examine the map of the world above showing plate boundaries', 'following questions.'),)
PART_TWO += romans('2A', 4, L(4, 'Plate Tectonics'), Q2AS, ID + 'p2-q2a', ('page',), [
    ('(i)', 3, L(4, '(i) Are the plates colliding or separating at A?'),
     S(11, '(i) · Are the plates', '(ii) · Name the ocean'), (fixed('Colliding or separating', 3, 'Separating · 3m'),),
     '0-0', PS),
    ('(ii)', 3, L(4, '(ii) Name the ocean ridge that runs North – South along the plate boundary at A.'),
     S(11, '(ii) · Name the ocean ridge', '(iii) Name the volcanic'), (fixed('Ocean ridge', 3, 'Mid Atlantic Ridge · 3m'),),
     '0-0', PS),
    ('(iii)', 3, L(4, '(iii) Name the volcanic island found at B.'),
     S(11, '(iii) Name the volcanic island', '(iv) Name the plate'), (fixed('Volcanic island', 3, 'Iceland · 3m'),),
     '0-0', PS + EV),
    ('(iv)', 3, L(4, '(iv) Name the plate on which Ireland lies.'),
     S(11, '(iv) Name the plate on which', '(v) · Name the two'), (fixed('Plate', 3, 'Eurasian · 3m'),), '0-0', PS),
    ('(v)', 6, L(4, '(v) Name the two plates that are colliding together at the boundary labelled C.'),
     S(11, '(v) · Name the two plates', '(vi) Name one landform'),
     (fixed('Two plates', 6, 'Nazca plate and South American plate · 3m + 3m', (0, 3, 6)),), '0-0', PS),
    ('(vi)', 6, L(4, '(vi) Name one landform that is formed at colliding plate boundaries and name one',
                  'example of this landform.'),
     S(11, '(vi) Name one landform', '(vii) Explain briefly'),
     (fixed('Landform', 3, 'One valid landform · 3m'), fixed('Example', 3, 'One valid example · 3m')), '0-0', PS),
    ('(vii)', 6, L(4, '(vii) Explain briefly how plates move.'),
     S(11, '(vii) Explain briefly how plates move.', '2B. Surface'),
     (srp3('Brief explanation', 2, 'Brief explanation two SRP’s @ 3m each · 6m'),), '0-0', PS),
])

ROCK = ('Quarrying', 'Mining', 'Oil/Gas exploitation', 'Geothermal energy production.')
PART_TWO += [
    T('p2-2b', P2, '2B', '', 40, 4, L(4, 'Surface Processes'),
      (L(4, '(i) Explain, with the aid of diagrams, the formation of any two landforms.'),),
      (S(11, 'Formation of any two landforms @ 20m each.', 'Total 40m'),),
      two_of('Landform', 20, 'Formation of any two landforms @ 20m each.', 'For each landform:',
             ('Landform named · 1m', 'Diagram(s) two aspects @ 2m each · 4m',
              'Formation explained 5 SRP’s @ 3m each · 15m'),
             ((0, 1), (0, 2, 4), steps(15, 3))),
      '0-4', PS_SURFACE, ID + 'p2-q2b-route-i', True,
      routes=(
          Route('route-i', 'Route (i)', ID + 'p2-q2b-route-i', True),
          Route('route-ii', 'Route (ii)', ID + 'p2-q2b-route-ii', True,
                prompt=(L(4, '(ii) Describe and explain any two processes of mass movement.'),),
                scheme=(S(12, 'Any two processes @ 20m each', 'Total 40m'),),
                criteria=two_of('Process', 20, 'Any two processes @ 20m each', 'For each process:',
                                ('Process stated · 2m', 'Description/explanation 6 SRP’s @ 3m each · 18m'),
                                ((0, 2), steps(18, 3))),
                topic='0-8', atlas=RW),
      )),
    T('p2-2c', P2, '2C', '', 30, 5, L(5, 'Human Interaction with the Rock Cycle'),
      (L(5, 'Describe and explain how humans interact with the rock cycle', 'Geothermal energy production.'),),
      (S(12, 'Description/explanation 10 SRP', 'Total 30m'),),
      (srp3('Description/explanation', 10, 'Description/explanation 10 SRP’s @ 3m each.'),),
      '0-6', RW, ID + 'p2-q2c-quarrying', True, routes=bullet_routes('p2-q2c-', ROCK)),
]

Q3AS = (L(6, 'Examine the photographs above and answer each of the following questions.'),)
PART_TWO += romans('3A', 6, L(6, 'Surface Processes', nth=0), Q3AS, ID + 'p2-q3a', ('page',), [
    ('(i)', 9, L(6, '(i) In your answer book, match each of the letters A, B and C', 'Tombolo.'),
     S(13, '• B Scree slope', '(ii) · In your answer book'),
     (fixed('Row 1', 3, '• B Scree slope · 3m'), fixed('Row 2', 3, '• A · Limestone pavement · 3m'),
      fixed('Row 3', 3, '• C Tombolo. · 3m')), '0-4', RW + KARST + SEA, (),
     (L(6, 'Scree slope'), L(6, 'Limestone pavement'), L(6, 'Tombolo'))),
    ('(ii)', 9, L(6, '(ii) In your answer book, match each of the letters A, B and C', 'Chemical weathering.'),
     S(13, '• C Coastal deposition', '(iii) Name one process'),
     (fixed('Row 1', 3, '• C Coastal deposition · 3m'), fixed('Row 2', 3, '• B Physical/mechanical weathering · 3m'),
      fixed('Row 3', 3, '• A Chemical weathering. · 3m')), '0-4', RW + KARST + SEA, (),
     (L(6, 'Coastal deposition'), L(6, 'Physical/mechanical weathering', nth=0),
      L(6, 'Chemical weathering', nth=0))),
    ('(iii)', 3, L(6, '(iii) Name one process of physical/mechanical weathering.'),
     S(13, '(iii) Name one process of physical', '(iv) Name one process'),
     (fixed('Process', 3, 'Valid process named · 3m'),), '0-8', RW),
    ('(iv)', 3, L(6, '(iv) Name one process of chemical weathering.'),
     S(13, '(iv) Name one process of chemical', '(v) · Explain briefly'),
     (fixed('Process', 3, 'Valid process named · 3m'),), '0-8', RW),
    ('(v)', 6, L(6, '(v) Explain briefly the process of hydraulic action.'),
     S(13, '(v) · Explain briefly the process', '3B. Earthquakes'),
     (srp3('Brief explanation', 2, 'Brief explanation two SRP’s @ 3m each · 6m'),), '0-4', RIVERS + SEA),
])

SURFACE = ('River processes', 'Coastal processes', 'Mass movement.')
PART_TWO += romans('3B', 6, L(6, 'Earthquakes'), (), ID + 'p2-q3b', (), [
    ('(i)', 6, L(6, '(i) Name two geographical locations where earthquakes have occurred.'),
     S(13, '(i) · Name two geographical', '(ii) · Name one scale'),
     (fixed('Two locations', 6, 'Two valid locations named · 3m + 3m', (0, 3, 6)),), '0-7', EV),
    ('(ii)', 4, L(6, '(ii) Name one scale used to measure earthquakes.'),
     S(13, '(ii) · Name one scale', '(iii) Explain how'), (fixed('Scale', 4, 'One valid scale named · 4m'),),
     '0-7', EV),
    ('(iii)', 30, L(6, '(iii) Explain how earthquakes occur and describe their main effects.'),
     S(13, '(iii) Explain how earthquakes occur', 'Total 40m'),
     (srp3('Explanation/description', 10, 'Explanation/description 10 SRP’s @ 3m each · 30m'),), '0-7', EV),
])
PART_TWO.append(T(
    'p2-3c', P2, '3C', '', 30, 6, L(6, 'Human Interaction with Surface Processes'),
    (L(6, 'Examine how humans interact with one of the following surface processes:', 'Mass movement.'),),
    (S(14, 'Interaction identified · 3m', 'Total 30m'),),
    (fixed('Interaction identified', 3, 'Interaction identified · 3m'),
     srp3('Examination', 9, 'Examination 9 SRP’s @ 3m each · 27m')),
    '0-6', RIVERS, ID + 'p2-q3c-river-processes', True,
    routes=bullet_routes('p2-q3c-', SURFACE, atlas=dict(zip(SURFACE, (RIVERS, SEA, RW))))))

SHOWN = 'Shown · 4m graded (4/2/0)'
NAMED_SHOWN = sums((0, 2), (0, 2, 4))
PART_TWO.append(T(
    'p2-4a', P2, '4A', '', 30, 7, L(7, 'Continental / Sub-Continental Region'),
    (L(7, 'Draw a sketch map of a Continental / Sub-Continental region (not in Europe)', 'in this region.'),),
    (S(15, 'Outline of Region', 'Total 30m'),),
    (fixed('Outline of region', 6, 'Outline of Region · 6m graded (6/4/2/0)', (0, 2, 4, 6)),
     Criterion('Relief (upland/lowland)', 6, NAMED_SHOWN, 'exact',
               ('Relief (upland/lowland): · Named · 2m', f'={SHOWN}@0')),
     Criterion('River', 6, NAMED_SHOWN, 'exact', ('River: · Named · 2m', f'={SHOWN}@1')),
     Criterion('Town/City 1', 6, NAMED_SHOWN, 'exact', ('Town/City 1: · Named · 2m', f'={SHOWN}@2')),
     Criterion('Town/City 2', 6, NAMED_SHOWN, 'exact', ('Town/City 2: · Named · 2m', f'={SHOWN}@3'))),
    '1-6', CONT, ID + 'p2-q4a', True))
Q4BS = (L(7, 'Answer each of the following questions with reference to an Irish region', 'studied.'),)
Q4BI = L(7, '(i) Name one example of a secondary economic activity in this region.')
PART_TWO += romans('4B', 7, L(7, 'Secondary Economic Activity in an Irish Region'), Q4BS, ID + 'p2-q4b', (), [
    ('(i)', 4, Q4BI, S(16, '(i) · Name one example of a secondary', '(ii) · Explain the advantages'),
     (fixed('Secondary economic activity named', 4, 'Named example · 4m'),), '1-4', IRL),
    ('(ii)', 27, L(7, '(ii) Explain the advantages that this region has for the development of this secondary',
                   'economic activity.'),
     S(16, '(ii) · Explain the advantages', '(iii) Describe one challenge'),
     (srp3('Explanation', 9, 'Explanation 9 SRP’s @ 3m each · 27m'),), '1-4', IRL, (Q4BI,)),
    ('(iii)', 9, L(7, '(iii) Describe one challenge faced by this secondary economic activity in this region.'),
     S(16, '(iii) Describe one challenge', 'Total 40m'),
     (srp3('Description', 3, 'Description 3 SRP’s @ 3m each · 9m'),), '1-4', IRL, (Q4BI,)),
])
REGION_TYPES = ('Climatic regions', 'Geomorphological regions', 'Cultural regions defined by language',
                'Cultural regions defined by religion.')
PART_TWO.append(T(
    'p2-4c', P2, '4C', '', 30, 7, L(7, 'Concept of a region'),
    (L(7, 'Describe and explain, using examples, any two of the region types listed below:',
       'Cultural regions defined by religion.'),),
    (S(16, 'Description/explanation 10 SRP', 'Total 30m'),),
    (srp3('Region 1', 5, 'Region 1: 5 SRP’s @ 3m each · 15m'), srp3('Region 2', 5, 'Region 2: 5 SRP’s @ 3m each · 15m')),
    # The shipped id names the whole question; the combinations it absorbs were never shipped.
    '1-0', IRL + EURO + CONT, ID + 'p2-q4c', True, absorbs=pool(ID + 'p2-q4c-', REGION_TYPES, 2)[1]))

Q5AS = (L(8, 'Examine the line graph above showing the area of land planted with trees', 'following questions.'),)
PART_TWO += romans('5A', 8, L(8, 'Forestry in Ireland'), Q5AS, ID + 'p2-q5a', ('page',), [
    ('(i)', 6, L(8, '(i) Name two counties that had more than 300 hectares of land planted with trees in', '2016.'),
     S(17, '(i) · Name two counties', '(ii) · In which year'),
     (fixed('Two counties', 6, 'Cavan/Leitrim/Mayo · 3m + 3m', (0, 3, 6)),), '2-0', GRAPH),
    ('(ii)', 3, L(8, '(ii) In which year between 2014 and 2018 was the most land in Wicklow planted with', 'trees?'),
     S(17, '(ii) · In which year', '(iii) Which county'), (fixed('Year', 3, '2016 · 3m'),), '2-0', GRAPH),
    ('(iii)', 3, L(8, '(iii) Which county had the most land planted with trees in 2018?'),
     S(17, '(iii) Which county', '(iv) Calculate'), (fixed('County', 3, 'Cavan · 3m'),), '2-0', GRAPH),
    ('(iv)', 6, L(8, '(iv) Calculate the difference between the land planted with trees', 'Mayo and Kildare.'),
     S(17, '(iv) Calculate', '(v) · State two'), (fixed('Difference', 6, '176 (hectares) · 6m'),), '2-0', GRAPH),
    ('(v)', 6, L(8, '(v) State two physical factors that make Ireland suitable for forestry.'),
     S(17, '(v) · State two', '(vi) Explain briefly'),
     (fixed('Two physical factors', 6, 'Two valid factors stated · 3m + 3m', (0, 3, 6)),), '1-4', IRL),
    ('(vi)', 6, L(8, '(vi) Explain briefly one advantage of forestry to the Irish economy.'),
     S(17, '(vi) Explain briefly', '5B. Urban'),
     (srp3('Brief explanation', 2, 'Brief explanation two SRP’s @ 3m each · 6m'),), '1-4', IRL),
])
PART_TWO.append(T(
    'p2-5b', P2, '5B', '', 30, 8, L(8, 'Urban Regions'),
    (L(8, 'Describe and explain the reasons for the growth of any one urban area that you have', 'studied.'),),
    (S(17, 'Description/explanation 10 SRP', 'Total 30m'),),
    (srp3('Description/explanation', 10, 'Description/explanation 10 SRP’s @ 3m each'),),
    '1-3', IRL + EURO + URB, ID + 'p2-q5b', True))
Q5CS = (L(9, 'Answer each of the following questions with reference to a Continental / Sub-Continental',
          'studied.'),)
Q5CI = L(9, '(i) Name one primary economic activity that contributes to the economy of this region.')
PART_TWO += romans('5C', 9, L(9, 'Primary Economic Activity in a Continental / Sub-Continental Region'), Q5CS,
                   ID + 'p2-q5c', (), [
    ('(i)', 4, Q5CI, S(18, '(i) · Name one primary', '(ii) · Explain the advantages'),
     (fixed('Primary economic activity named', 4, 'Named primary economic activity · 4m'),), '1-6', CONT),
    ('(ii)', 27, L(9, '(ii) Explain the advantages that this region has for the development of the primary',
                   'part (i) above.'),
     S(18, '(ii) · Explain the advantages', '(iii) Describe one problem'),
     (srp3('Explanation', 9, 'Explanation 9 SRP’s @ 3m each · 27m'),), '1-6', CONT, (Q5CI,)),
    ('(iii)', 9, L(9, '(iii) Describe one problem faced by this primary economic activity in this region.'),
     S(18, '(iii) Describe one problem', 'Total 40m'),
     (srp3('Description', 3, 'Description 3 SRP’s @ 3m each · 9m'),), '1-6', CONT, (Q5CI,)),
])

Q6AS = (L(10, 'Examine the table and chart above showing information on the amount of milk',
          'following questions.'),)
PART_TWO += romans('6A', 10, L(10, 'European Union – Agriculture'), Q6AS, ID + 'p2-q6a', ('page',), [
    ('(i)', 3, L(10, '(i) How much milk (in million tonnes) was produced in the Netherlands in 2018?'),
     S(19, '(i) · How much milk', '(ii) · Which country'), (fixed('Million tonnes', 3, '14 · 3m'),),
     '2-0', GRAPH + EURO),
    ('(ii)', 3, L(10, '(ii) Which country listed in the table above produced the most milk in 2018?'),
     S(19, '(ii) · Which country', '(iii) What percentage'), (fixed('Country', 3, 'Germany · 3m'),),
     '2-0', GRAPH + EURO),
    ('(iii)', 3, L(10, '(iii) What percentage of milk was used to make cream?'),
     S(19, '(iii) What percentage', '(iv) Calculate X'), (fixed('Percentage', 3, '12 (%) · 3m'),),
     '2-0', GRAPH + EURO),
    ('(iv)', 6, L(10, '(iv) Calculate X, the percentage of milk that was used to make butter.'),
     S(19, '(iv) Calculate X', '(v) · Which product'), (fixed('Percentage', 6, '29 (%) · 6m'),),
     '2-0', GRAPH + EURO),
    ('(v)', 3, L(10, '(v) Which product was milk most used for in 2018?'),
     S(19, '(v) · Which product', '(vi) · Name two'), (fixed('Product', 3, 'Cheese · 3m'),), '2-0', GRAPH + EURO),
    ('(vi)', 6, L(10, '(vi) Name two types of farm found in Ireland.'),
     S(19, '(vi) · Name two', '(vii) Explain briefly'),
     (fixed('Two types of farm', 6, 'Two valid types named · 3m + 3m', (0, 3, 6)),), '1-4', IRL),
    ('(vii)', 6, L(10, '(vii) Explain briefly one advantage of European Union membership for Irish farmers.'),
     S(19, '(vii) Explain briefly', '6B. Economic'),
     (srp3('Brief explanation', 2, 'Brief explanation two SRP’s @ 3m each · 6m'),), '3-3', EU),
])
ACTIVITIES = ('The reasons why tourists are attracted to the region', 'The importance of manufacturing to the region',
              'The development of transport in the region.')
PART_TWO += [
    T('p2-6b', P2, '6B', '', 40, 10, L(10, 'Economic Activities – European Region'),
      (L(10, 'Explain the development of any two of the following with reference to a European region',
         'The development of transport in the region.'),),
      (S(19, 'Activity 1 explained', 'Total 40m'),),
      (srp3('Activity 1 explained', 7, 'Activity 1 explained 7 SRP’s @ 3m each · 21m'),
       srp3('Activity 2 explained', 6, 'Activity 2 explained 6 SRP’s @ 3m each · 18m'),
       fixed('Region named', 1, 'Region named · 1m')),
      '1-5', EURO, *pool(ID + 'p2-q6b-', ACTIVITIES, 2)[:1], True, absorbs=pool(ID + 'p2-q6b-', ACTIVITIES, 2)[1]),
    T('p2-6c', P2, '6C', '', 30, 10, L(10, 'Regional Problems'),
      (L(10, 'Describe and explain two problems faced by any region that you have studied.'),),
      (S(20, 'Description/explanation of problem 1', 'Total 30m'),),
      (srp3('Problem 1', 5, 'Description/explanation of problem 1: 5 SRP’s @ 3m each · 15m'),
       srp3('Problem 2', 5, 'Description/explanation of problem 2: 5 SRP’s @ 3m each · 15m')),
      '1-0', IRL + EURO, ID + 'p2-q6c', True),
]

GRAPH_OL = (fixed('Graph paper', 3, 'Graph paper', (0, 3)),
            fixed('Vertical axis labelled / circle', 3, 'Vertical axis labelled/Circle · 3m graded (3/1/0)', (0, 1, 3)),
            fixed('Horizontal axis labelled / centred', 3, 'Horizontal axis labelled/Centred · 3m graded (3/1/0)',
                  (0, 1, 3)),
            fixed('5 items illustrated', 15, '5 items @ 3m each graded (3/1/0) · 15m', sums(*[(0, 1, 3)] * 5)))
Q7AS = (L(12, 'Examine the data above on energy related CO2 emissions', 'following questions.'),)
PART_TWO += romans('7A', 12, L(12, 'Energy Use in Ireland'), Q7AS, ID + 'p2-q7a', ('page',), [
    ('(i)', 24, L(12, '(i) Using graph paper, draw a suitable graph to illustrate this data.'),
     S(22, 'Graph paper 3m', '(ii) · In your answer book'), GRAPH_OL, '2-0', GRAPH),
    ('(ii)', 6, L(12, '(ii) In your answer book, explain briefly one negative impact of CO2 emissions.'),
     S(22, '(ii) · In your answer book', '7B. Multinational'),
     (srp3('Brief explanation', 2, 'Brief explanation 2 SRP’s @ 3m each · 6m'),), '3-4', ENV),
])
Q7BI = L(12, '(i) Name one multinational company operating in Ireland.')
PART_TWO += romans('7B', 12, L(12, 'Multinational Company (MNC)'), (), ID + 'p2-q7b', (), [
    ('(i)', 4, Q7BI, S(22, '(i) · Name one multinational', '(ii) · Name one raw'),
     (fixed('MNC named', 4, 'Valid MNC named · 4m'),), '3-2', MNC),
    ('(ii)', 6, L(12, '(ii) Name one raw material used by this multinational company and name the country',
                  'is sourced.'),
     S(22, '(ii) · Name one raw', '(iii) Name one product'),
     (fixed('Raw material named', 3, 'Valid raw material named · 3m'),
      fixed('Source country named', 3, 'Valid source country named · 3m')), '3-2', MNC, (Q7BI,)),
    ('(iii)', 3, L(12, '(iii) Name one product manufactured by this multinational company.'),
     S(22, '(iii) Name one product', '(iv) State where'), (fixed('Product named', 3, 'Valid product named · 3m'),),
     '3-2', MNC, (Q7BI,)),
    ('(iv)', 27, L(12, '(iv) State where this multinational company is located in Ireland and explain in detail',
                   'at this location.'),
     S(22, '(iv) State where', 'Total 40m'),
     (fixed('Location', 3, 'Valid location · 3m'), srp3('Explanation', 8, 'Explanation 8 SRP’s @ 3m each · 24m')),
     '3-2', MNC, (Q7BI,)),
])
PART_TWO.append(T(
    'p2-7c', P2, '7C', '', 30, 12, L(12, 'Ireland and the European Union'),
    (L(12, 'Explain how being a member of the European Union has impacted on the Irish economy.'),),
    (S(23, 'Impact Identified 1 SRP', 'Total 30m'),),
    (fixed('Impact identified', 3, 'Impact Identified 1 SRP · 3m'),
     srp3('Explanation', 9, 'Explanation 9 SRP’s @ 3m each · 27m')),
    '3-3', EU, ID + 'p2-q7c', True))

PART_TWO.append(sketch(
    13, L(13, 'Aerial Photograph'),
    L(13, 'Examine the aerial photograph of Foxford accompanying this paper.', 'in the right background.'),
    24, ID + 'p2-q8a', '2-8', AER, ('aerial',), 'landscape',
    ('The river', 'Two connecting streets', 'A bridge', 'An area of forest in the left background',
     'An area of waste ground in the right background')))
Q8BI = L(13, '(i) Name one example of environmental pollution caused by economic activity.')
PART_TWO += romans('8B', 13, L(13, 'Economic Activity – Environmental Pollution'), (), ID + 'p2-q8b', (), [
    ('(i)', 4, Q8BI, S(25, '(i) · Name one example of environmental', '(ii) · Explain the causes'),
     (fixed('Example named', 4, 'Valid example named · 4m'),), '3-4', ENV),
    ('(ii)', 27, L(13, '(ii) Explain the causes and effects of this environmental pollution.'),
     S(25, '(ii) · Explain the causes', '(iii) Describe how'),
     (fixed('Cause identified', 3, 'One cause identified · 3m'), fixed('Effect identified', 3, 'One effect identified · 3m'),
      srp3('Explanation', 7, 'Explanation 7 SRP’s @ 3m each · 21m')), '3-4', ENV, (Q8BI,)),
    ('(iii)', 9, L(13, '(iii) Describe how this environmental pollution could be reduced.'),
     S(25, '(iii) Describe how', 'Total 40m'),
     (srp3('Description', 3, 'Description 3 SRP’s @ 3m each · 9m'),), '3-4', ENV, (Q8BI,)),
])
DEVELOPED = ('Tourism', 'Financial services', 'Service and footloose industries.')
PART_TWO.append(T(
    'p2-8c', P2, '8C', '', 30, 13, L(13, 'Economic Development – Developed Economy'),
    (L(13, 'Describe and explain the development of one of the following with reference to a developed',
       'Service and footloose industries.'),),
    (S(25, 'Named developed economy', 'Total 30m'),),
    (fixed('Developed economy named', 3, 'Named developed economy · 3m'),
     srp3('Description/explanation', 9, 'Description/explanation 9 SRP’s @ 3m each · 27m')),
    '3-0', ECON, ID + 'p2-q8c-tourism', True, routes=bullet_routes('p2-q8c-', DEVELOPED)))

Q9AS = (L(14, 'Examine the table above and answer each of the following questions.'),)
PART_TWO += romans('9A', 14, L(14, 'Human Development Index', nth=0), Q9AS, ID + 'p2-q9a', ('page',), [
    ('(i)', 3, L(14, '(i) Which country had the highest Human Development Index value in 2018?'),
     S(26, '(i) · Which country', '(ii) · What was'), (fixed('Country', 3, 'Ireland · 3m'),), '2-0', GRAPH),
    ('(ii)', 3, L(14, '(ii) What was the gross national income per capita (in US$) for Australia in 2018?'),
     S(26, '(ii) · What was', '(iii) Which two'), (fixed('Gross national income per capita', 3, '44,097 (US$) · 3m'),),
     '2-0', GRAPH),
    ('(iii)', 6, L(14, '(iii) Which two countries had the lowest life expectancy at birth in 2018?'),
     S(26, '(iii) Which two', '(iv) Calculate'),
     (fixed('Two countries', 6, 'Mali and Mexico · 3m + 3m', (0, 3, 6)),), '2-0', GRAPH),
    ('(iv)', 6, L(14, '(iv) Calculate the difference between the gross national income per capita',
                  'Ireland and Mexico.'),
     S(26, '(iv) Calculate', '(v) · List two'), (fixed('Difference', 6, '38,032 (US$) · 6m'),), '2-0', GRAPH),
    ('(v)', 6, L(14, '(v) List two reasons why some countries have a higher Human Development Index value',
                 'than others.'),
     S(26, '(v) · List two', '(vi) Explain briefly'),
     (fixed('Two reasons', 6, 'Two valid reasons listed · 3m + 3m', (0, 3, 6)),), '3-1', DEV),
    ('(vi)', 6, L(14, '(vi) Explain briefly one factor that influences life expectancy.'),
     S(26, '(vi) Explain briefly', 'Total 30m'),
     (srp3('Brief explanation', 2, 'Brief explanation 2 SRP’s @ 3m each · 6m'),), '4-0', POP),
])
Q9BS = (L(14, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper.'),
        L(14, 'Imagine you have been given the task', 'the area covered by the map.'))
Q9BI = L(14, '(i) State, using a six-figure grid reference, where you would locate the factory.')
PART_TWO += romans('9B', 14, L(14, 'Ordnance Survey Map'), Q9BS, ID + 'p2-q9b', ('map', 'legend'), [
    ('(i)', 4, Q9BI, S(27, '(i) · State, using', '(ii) · Explain the reasons'),
     (fixed('Six-figure grid reference', 4, 'Six-figure grid reference · 4m graded (4/2/0)', (0, 2, 4)),),
     '2-6', MAP),
    ('(ii)', 27, L(14, '(ii) Explain the reasons why you chose this location.'),
     S(27, '(ii) · Explain the reasons', '(iii) Describe one'),
     (srp3('Reasons explained', 9, 'Reasons explained 9 SRP’s @ 3m each · 27m'),), '3-0', ECON + MAP, (Q9BI,)),
    ('(iii)', 9, L(14, '(iii) Describe one disadvantage of locating the factory at this location.'),
     S(27, '(iii) Describe one disadvantage', 'Total 40m'),
     (srp3('One disadvantage described', 3, 'One disadvantage described 3 SRP’s @ 3m each · 9m'),),
     '3-0', ECON + MAP, (Q9BI,)),
], legacy_first=False)
Q9CI = L(14, '(i) Name one developing economy that was colonised.')
PART_TWO += romans('9C', 14, L(14, 'Colonialism'), (), ID + 'p2-q9c', (), [
    ('(i)', 3, Q9CI, S(27, '(i) · Name one developing economy', '(ii) · Describe and explain'),
     (fixed('Developing economy named', 3, 'Named developing economy · 3m'),), '3-1', DEV),
    ('(ii)', 27, L(14, '(ii) Describe and explain the effects of colonialism on this developing economy.'),
     S(27, '(ii) · Describe and explain the effects', 'Total 30m'),
     (srp3('Description/explanation', 9, 'Description/explanation 9 SRP’s @ 3m each · 27m'),), '3-1', DEV, (Q9CI,)),
])

PART_TWO.append(sketch(
    15, L(15, 'Aerial Photograph'),
    L(15, 'Examine the aerial photograph of Foxford accompanying this paper.', 'in the right background.'),
    28, ID + 'p2-q10a', '2-8', AER + URB, ('aerial',), 'landscape', ()))
Q10BI = L(15, '(i) State two reasons why people migrate from rural areas to urban areas.')
PART_TWO += romans('10B', 15, L(15, 'Migration – Rural to Urban'), (), ID + 'p2-q10b', (), [
    ('(i)', 4, Q10BI, S(29, '(i) · State two reasons', '(ii) · Describe and explain'),
     (fixed('Two reasons', 4, 'Two valid reasons stated @ 2m + 2m · 4m', (0, 2, 4)),), '4-2', POP),
    ('(ii)', 18, L(15, '(ii) Describe and explain the effect of this migration on the urban areas that people',
                   'migrate to.'),
     S(29, '(ii) · Describe and explain the effect', '(iii) · Describe'),
     (srp3('Description/explanation', 6, 'Description/explanation 6 SRP’s @ 3m each · 18m'),), '4-2', POP,
     (Q10BI,)),
    ('(iii)', 18, L(15, '(iii) Describe and explain the effect of this migration on the rural areas they leave',
                    'behind.'),
     S(29, '(iii) · Describe and explain the effect', 'Total 40m'),
     (srp3('Description/explanation', 6, 'Description/explanation 6 SRP’s @ 3m each · 18m'),), '4-2', POP,
     (Q10BI,)),
])
PART_TWO += romans('10C', 15, L(15, 'Overpopulation'), (), ID + 'p2-q10c', (), [
    ('(i)', 6, L(15, '(i) Explain briefly what is meant by the term overpopulation.'),
     S(29, '(i) · Explain briefly what is meant', '(ii) · Describe and explain the causes'),
     (srp3('Brief explanation', 2, 'Brief explanation 2 SRP’s @ 3m each · 6m'),), '4-1', POP),
    ('(ii)', 24, L(15, '(ii) Describe and explain the causes and effects of overpopulation with reference to',
                   'example(s) that you have studied.'),
     S(29, '(ii) · Describe and explain the causes', 'Total 30m'),
     (fixed('Cause identified', 3, 'One cause identified · 3m'), fixed('Effect identified', 3, 'One effect identified · 3m'),
      srp3('Description/explanation', 6, 'Description/explanation 6 SRP’s @ 3m each · 18m')), '4-1', POP),
])

Q11AS = (L(16, 'Examine the table above showing information on the population in Ireland', 'following questions.'),)
PART_TWO += romans('11A', 16, L(16, 'Population Distribution'), Q11AS, ID + 'p2-q11a', ('page',), [
    ('(i)', 3, L(16, '(i) What was the population of Co. Louth in 2011?'),
     S(30, '(i) · What was the population', '(ii) · What percentage'), (fixed('Population', 3, '122,897 · 3m'),),
     '2-0', GRAPH),
    ('(ii)', 3, L(16, '(ii) What percentage of Ireland’s population lived in rural areas in 2016?'),
     S(30, '(ii) · What percentage', '(iii) Calculate'), (fixed('Percentage', 3, '37 (%) · 3m'),), '2-0', GRAPH),
    ('(iii)', 6, L(16, '(iii) Calculate the change in the population of Co. Sligo between 2011 and 2016.'),
     S(30, '(iii) Calculate', '(iv) Which county'), (fixed('Change', 6, '(+) 142 · 6m'),), '2-0', GRAPH),
    ('(iv)', 3, L(16, '(iv) Which county had the highest percentage of population living in rural areas in 2016?'),
     S(30, '(iv) Which county', '(v) · State two'), (fixed('County', 3, 'Co. Leitrim · 3m'),), '2-0', GRAPH),
    ('(v)', 6, L(16, '(v) State two reasons why more people in Ireland live in urban areas.'),
     S(30, '(v) · State two', '(vi) What percentage'),
     (fixed('Two reasons', 6, 'Two valid reasons stated · 3m + 3m', (0, 3, 6)),), '4-3', URB),
    ('(vi)', 3, L(16, '(vi) What percentage of Co. Dublin’s population lived in urban areas in 2016?'),
     S(30, '(vi) What percentage', '(vii) Briefly'), (fixed('Percentage', 3, '98 (%) · 3m'),), '2-0', GRAPH),
    ('(vii)', 6, L(16, '(vii) Briefly explain one reason why Ireland’s population is increasing.'),
     S(30, '(vii) Briefly', 'Total 30m'),
     (srp3('Brief explanation', 2, 'Brief explanation 2 SRP’s @ 3m each · 6m'),), '4-0', POP),
])
Q11BI = L(16, '(i) Name one city in the developing world that is rapidly growing.')
PART_TWO += romans('11B', 16, L(16, 'Developing World City'), (), ID + 'p2-q11b', (), [
    ('(i)', 4, Q11BI, S(31, '(i) · Name one city', '(ii) · Explain the reasons'),
     (fixed('Developing world city named', 4, 'Valid developing world city named · 4m'),), '4-5', URB),
    ('(ii)', 15, L(16, '(ii) Explain the reasons for the rapid growth of this developing world city.'),
     S(31, '(ii) · Explain the reasons', '(iii) Describe the problems'),
     (srp3('Explanation', 5, 'Explanation 5 SRP’s @ 3m each · 15m'),), '4-5', URB, (Q11BI,)),
    ('(iii)', 12, L(16, '(iii) Describe the problems caused by this rapid growth.'),
     S(31, '(iii) Describe the problems', '(iv) Explain one solution'),
     (srp3('Description', 4, 'Description 4 SRP’s @ 3m each · 12m'),), '4-5', URB, (Q11BI,)),
    ('(iv)', 9, L(16, '(iv) Explain one solution to these problems.'),
     S(31, '(iv) Explain one solution', 'Total 40m'),
     (srp3('Explanation', 3, 'Explanation 3 SRP’s @ 3m each · 9m'),), '4-5', URB, (Q11BI,)),
])
TOWN_REASON = ('Three reasons @ 10m each · 30m', 'For each reason:', 'Ordnance Survey map evidence · 1m',
               'Explanation 3 SRP’s @ 3m each · 9m')
PART_TWO.append(T(
    'p2-11c', P2, '11C', '', 30, 16, L(16, 'Development of Urban Settlements'),
    (L(16, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper.'),
     L(16, 'Explain three reasons why the town of Foxford developed at this location', 'support each reason.')),
    (S(31, 'Three reasons @ 10m each', 'Total 30m'),),
    tuple(Criterion(f'Reason {n}', 10, sums((0, 1), steps(9, 3)), 'srp', TOWN_REASON) for n in (1, 2, 3)),
    '4-3', URB + MAP, ID + 'p2-q11c', False, ('map', 'legend')))

Q12AS = (L(17, 'Examine the table above showing information on population density', 'following questions.'),)
PART_TWO += romans('12A', 17, L(17, 'Population Density', nth=0), Q12AS, ID + 'p2-q12a', ('page',), [
    ('(i)', 24, L(17, '(i) Using graph paper, draw a suitable graph or chart to illustrate this data.'),
     S(32, 'Graph paper', '(ii) · In your answer book'), GRAPH_OL, '2-0', GRAPH),
    ('(ii)', 6, L(17, '(ii) In your answer book, explain briefly one reason why some areas have low population',
                  'densities.'),
     S(32, '(ii) · In your answer book', '12B. Urban'),
     (srp3('Brief explanation', 2, 'Brief explanation 2 SRP’s @ 3m each · 6m'),), '4-0', POP),
])
Q12BI = L(17, '(i) Name one urban area that you have studied.')
PART_TWO += romans('12B', 17, L(17, 'Urban Functions'), (), ID + 'p2-q12b', (), [
    ('(i)', 3, Q12BI, S(32, '(i) · Name one urban area', '(ii) · Name any two'),
     (fixed('Urban area named', 3, 'Valid urban area named · 3m'),), '4-3', URB),
    ('(ii)', 6, L(17, '(ii) Name any two functions of this urban area.'),
     S(32, '(ii) · Name any two', '(iii) Describe and explain'),
     (fixed('Two functions', 6, 'Two valid functions named · 3m + 3m', (0, 3, 6)),), '4-3', URB, (Q12BI,)),
    ('(iii)', 21, L(17, '(iii) Describe and explain how the functions of this urban area have changed over time.'),
     S(32, '(iii) Describe and explain how the functions', 'Total 30m'),
     (srp3('Description/explanation', 7, 'Description/explanation 7 SRP’s @ 3m each · 21m'),), '4-3', URB,
     (Q12BI,)),
])
Q12CS = (L(17, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper.'),)
Q12CI = L(17, '(i) Name three different rural settlement patterns evident on the Ordnance Survey map',
          'an example of each.')
PART_TWO += romans('12C', 17, L(17, 'Rural Settlement Patterns'), Q12CS, ID + 'p2-q12c', ('map', 'legend'), [
    ('(i)', 22, Q12CI, S(33, '(i) · Name three different', '(ii) · Explain each'),
     (fixed('Pattern 1 named', 4, 'Pattern 1 named: · 4m'), fixed('Pattern 2 named', 3, 'Pattern 2 named: · 3m'),
      fixed('Pattern 3 named', 3, 'Pattern 3 named: · 3m'),
      *(fixed(f'Grid reference {n}', 4, f'Grid reference {n}: · 4m graded (4/2/0)', (0, 2, 4)) for n in (1, 2, 3))),
     '4-3', URB + MAP),
    ('(ii)', 18, L(17, '(ii) Explain each of the three rural settlement patterns named in part (i) above.'),
     S(33, '(ii) · Explain each', 'Total 40m'),
     tuple(srp3(f'Pattern {n}', 2, f'Pattern {n}: 2 SRP’s @ 3m each · 6m') for n in (1, 2, 3)),
     '4-3', URB + MAP, (Q12CI,)),
], legacy_first=False)

TASKS = [*PART_ONE, *PART_TWO]

ID_CORRECTION_REASON = (
    'The shipped card held every part of a question the scheme prices part by '
    'part. Its id is kept on the first separately priced part; the other parts '
    'are new cards with their own published allocation.')

# Every 2021 Ordinary card id live on origin/main before this review (49). Each must survive.
LEGACY_IDS = [
    'geography-2021-ol-p1-q1',
    'geography-2021-ol-p1-q2',
    'geography-2021-ol-p1-q3',
    'geography-2021-ol-p1-q4',
    'geography-2021-ol-p1-q5',
    'geography-2021-ol-p1-q9',
    'geography-2021-ol-p1-q10',
    'geography-2021-ol-p1-q11',
    'geography-2021-ol-p1-q12',
    'geography-2021-ol-p2-q1b',
    'geography-2021-ol-p2-q1c',
    'geography-2021-ol-p2-q2a',
    'geography-2021-ol-p2-q2b-route-i',
    'geography-2021-ol-p2-q2b-route-ii',
    'geography-2021-ol-p2-q2c-quarrying',
    'geography-2021-ol-p2-q2c-mining',
    'geography-2021-ol-p2-q2c-oil-gas-exploitation',
    'geography-2021-ol-p2-q2c-geothermal-energy-production',
    'geography-2021-ol-p2-q3a',
    'geography-2021-ol-p2-q3b',
    'geography-2021-ol-p2-q3c-river-processes',
    'geography-2021-ol-p2-q3c-coastal-processes',
    'geography-2021-ol-p2-q3c-mass-movement',
    'geography-2021-ol-p2-q4a',
    'geography-2021-ol-p2-q4b',
    'geography-2021-ol-p2-q4c',
    'geography-2021-ol-p2-q5a',
    'geography-2021-ol-p2-q5b',
    'geography-2021-ol-p2-q5c',
    'geography-2021-ol-p2-q6a',
    'geography-2021-ol-p2-q6b-the-reasons-why-tourists-are-attra-the-importance-of-manufacturing-to',
    'geography-2021-ol-p2-q6b-the-reasons-why-tourists-are-attra-the-development-of-transport-in-th',
    'geography-2021-ol-p2-q6b-the-importance-of-manufacturing-to-the-development-of-transport-in-th',
    'geography-2021-ol-p2-q6c',
    'geography-2021-ol-p2-q7a',
    'geography-2021-ol-p2-q7b',
    'geography-2021-ol-p2-q7c',
    'geography-2021-ol-p2-q8b',
    'geography-2021-ol-p2-q8c-tourism',
    'geography-2021-ol-p2-q8c-financial-services',
    'geography-2021-ol-p2-q8c-service-and-footloose-industries',
    'geography-2021-ol-p2-q9a',
    'geography-2021-ol-p2-q9c',
    'geography-2021-ol-p2-q10b',
    'geography-2021-ol-p2-q10c',
    'geography-2021-ol-p2-q11a',
    'geography-2021-ol-p2-q11b',
    'geography-2021-ol-p2-q12a',
    'geography-2021-ol-p2-q12b',
]
