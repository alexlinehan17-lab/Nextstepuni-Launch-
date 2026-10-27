"""Independent review ledger: Leaving Certificate Geography 2020 Ordinary Level.

Sources (English editions, harvested Paper Trail corpus; sizes and SHA-256
pinned in EXPECTED_SOURCES and the generated audit): Part One and Answerbook
LC005GLP042EV (40 pages), Part Two LC005GLP043EV (20 pages), marking scheme
LC005GLP000EV (32 pages), and the common companions shared with Higher Level
— the 1:50 000 Arklow map LC005CLP003EV, its legend LC005CLPC00EV and the
Arklow aerial photograph LC005CLP004EV (published only as a JPEG). Part One
is 100 marks (any ten of twelve @ 10), Part Two 300 (three questions @ 100).

Visual sweep (every page rendered and read on 2026-10-12):
  Part One booklet p1 cover; p2 instructions (Part One "Attempt any TEN";
  Part Two "attempt THREE": one of Q1-3, one of Q4-6, one elective); p3-p12
  Questions 1-12 (p7 holds Q5 and Q6, p8 Q7 and Q8); p13 Part Two
  answerbook instructions; p14-p35 lined answer pages; p36-p39 graph
  paper; p40 copyright/back cover.
  Part Two booklet p1 cover; p2 Part Two instructions; p3 Section 1
  divider; p4-p9 Q1-Q6; p10 Section 2 divider; p11-p16 Electives Q7-Q12;
  p17-p19 "Do not hand this up"; p20 back cover.
  Scheme p1 cover; p2-p3 notes; p4-p5 Part One table; p6 Part Two
  instructions; p7-p19 Q1-Q6; p20-p25 Q7-Q9; p26-p31 Q10-Q12; p32 back
  cover.
  Companions: Arklow map extract; OS legend sheet; oblique aerial
  photograph of Arklow.

Tariffs as printed: twelve parts carry 40 marks (1B, 2B, 3B, 4B, 5C, 6B,
7B, 8B, 9B, 10C, 11C, 12C) and the rest 30. An SRP is 3 marks; "a+b" lines
are one criterion with partial credit a; graded lines keep their printed
grades; sketch items are "showing 3 (3/1/0) + labelled 2"; 4A items are
"named 2 + shown 4 (4/2/0)"; 10B reasons are "aerial photograph evidence 1 +
3 SRPs".

Boundaries follow the 2021 Ordinary ledger: every priced roman is a task; a
matching table under ONE printed instruction stays one task with a
criterion per scheme row, in the printed row order: Q1 Crust=A, Inner
Core=B, Mantle=D, Outer Core=C; Q2 Focus=B, Epicentre=D, Seismic waves=C,
Fault=A; Q3 prints (i) and (ii) in one part-completed table: (i) V-shaped
valley=D, Waterfall=B, Delta=A (Floodplain C is printed), (ii) Waterfall
Erosion, Floodplain Deposition (the other two are printed); Q4 Granite=C,
Basalt=B, Limestone=A, Sandstone=D; Q7 Right background=D, Right
middleground=A, Left foreground=B, Left background=C; Q8 A Departement=E,
Sambre-Meuse=D, Munster Ridge and Valley=C, Greater Dublin Area=B,
Mediterranean=A; Q9 A Secondary, B Tertiary, C Primary, D Primary; Q12
Byrd Glacier=A, Tombolo=D, Wildfire=B, Mt. Etna=C; Part Two 3A(i) Drumlin
B, Cliff A, Beach C, 3A(ii) Coastal deposition C, Coastal erosion A,
Glacial deposition B. 7B's "tourism or financial services" runs through
three romans and the scheme marks either alike, so each roman is one card
with the printed wording. Q2(ii)'s scheme prints "Richter scale /" and
"Moment magnitude scale" either side of its allocation line; both are kept.

Scheme as printed: 8B(ii) asks for the disadvantages of the hotel site and
its allocation line repeats "Description / explanation of the advantages 5
SRPs"; the card carries the line as printed.

9C: the paper prints [30m]; the scheme prices "Impact identified 1 SRP 3m"
and "Explanation 8 SRP's @ 3m each 24m" (27m) above "Total 30m", and
publishes no allocation for the other three marks (re-examined on the
rendered page; no Irish-language Ordinary scheme exists for 2020). The
card carries those two printed lines as its placements (3m and 24m, in
3-mark SRPs) against the printed total of 30, with a note saying so; the
missing three marks are never derived or redistributed, so the most the
card can place is 27.
"""

from geography_review import (
    Criterion, Lift, Route, SchemeSlice, Task, pool, fixed, slug, srp, steps, sums,
)

YEAR = 2020
LEVEL = 'ordinary'
PAPER_PAGES = {1: 40, 2: 20}
SCHEME_PAGES = 32
_FORTY = {'1B', '2B', '3B', '4B', '5C', '6B', '7B', '8B', '9B', '10C', '11C', '12C'}
QUESTION_TARIFFS = {1: {str(n): 10 for n in range(1, 13)},
                    2: {f'{n}{x}': (40 if f'{n}{x}' in _FORTY else 30)
                        for n in range(1, 13) for x in 'ABC'}}

EXPECTED_SOURCES = {
    'paper1': ('LC005GLP042EV.pdf', 2898940),
    'paper2': ('LC005GLP043EV.pdf', 1145514),
    'scheme': ('LC005GLP000EV.pdf', 319419),
    'map': ('LC005CLP003EV.pdf', 4637231),
    'legend': ('LC005CLPC00EV.pdf', 869977),
    'aerial': ('LC005CLP004EV.jpg', 6218552),
}

PAGE_REVIEW = {
    'paper1': {1: 'cover', 2: 'instructions', **{p: 'question' for p in range(3, 13)},
               13: 'answerbook instructions', **{p: 'lined answer page' for p in range(14, 36)},
               **{p: 'graph-paper answer page' for p in range(36, 40)}, 40: 'copyright/back cover'},
    'paper2': {1: 'cover', 2: 'Part Two instructions', 3: 'section divider',
               **{p: 'question' for p in (*range(4, 10), *range(11, 17))}, 10: 'section divider',
               17: 'do not hand this up', 18: 'do not hand this up', 19: 'do not hand this up',
               20: 'back cover'},
    'scheme': {1: 'cover', 2: 'notes', 3: 'notes', 4: 'Part One table', 5: 'Part One table',
               6: 'Part Two instructions', **{p: 'Part Two allocation' for p in range(7, 32)},
               32: 'back cover'},
}

EXPECTED_SELECTION_SCAN = [
    [1, 2, 'attempt any ten'], [1, 2, 'attempt three'], [1, 3, 'attempt any ten'],
    [2, 2, 'attempt three'], [2, 3, 'attempt two'], [2, 4, 'attempt one'],
    [2, 4, 'one of the following'],
    [2, 5, 'answer (i) or (ii)'], [2, 5, 'any two'], [2, 5, 'any two'], [2, 5, 'one of the following'],
    [2, 7, 'attempt one'],
    [2, 9, 'any two'], [2, 9, 'any two'],
    [2, 10, 'attempt one'],
    [2, 14, 'any three'],
    [2, 15, 'any two'],
    [2, 16, 'attempt to'],
]
SELECTION_REVIEW = [
    {'scan': [[1, 2, 'attempt any ten'], [1, 2, 'attempt three'], [1, 3, 'attempt any ten'],
              [2, 2, 'attempt three'], [2, 3, 'attempt two'], [2, 4, 'attempt one'],
              [2, 7, 'attempt one'], [2, 10, 'attempt one']],
     'kind': 'exam-attempt-rule',
     'reason': 'Part One any ten of twelve and Part Two three questions (one of Q1-3, one of Q4-6, one elective) are attempt rules; every question is carded.'},
    {'scan': [[2, 4, 'one of the following']], 'kind': 'closed-choose-one',
     'reason': '1C: one of three printed surface processes -> three routes.'},
    {'scan': [[2, 5, 'answer (i) or (ii)']], 'kind': 'closed-route',
     'reason': '2B: (i) or (ii) -> two routes, each with its own scheme allocation.'},
    {'scan': [[2, 5, 'one of the following']], 'kind': 'closed-choose-one',
     'reason': '2C: one of four printed interactions with the rock cycle -> four routes.'},
    {'scan': [[2, 9, 'any two']], 'kind': 'choose-n-one-card',
     'reason': '6B any two of three printed headings -> one card with every printed item (choice is not a route). 4C "two of the factors listed below" (three printed) is one card on the same rule.'},
    {'scan': [[2, 5, 'any two'], [2, 5, 'any two'], [2, 9, 'any two'], [2, 14, 'any three'], [2, 15, 'any two']],
     'kind': 'open-response',
     'reason': 'No printed pool: 2B(i) any two landforms and 2B(ii) any two mass movement processes (the scheme prices two @ 20m); 6A(iv) any two crops; 10C(iii) any three problems; 11B(ii) any two functions.'},
    {'scan': [[2, 16, 'attempt to']], 'kind': 'not-a-selection',
     'reason': '12A(v) "authorities in urban areas attempt to reduce" describes the authorities, not a candidate choice.'},
]

HELD: list[dict] = []
NOTE_9C = ('The published scheme prices 27 of the printed 30 marks ("Impact identified 1 SRP 3m" and '
           '"Explanation 8 SRP’s @ 3m each 24m" above "Total 30m") and publishes no allocation for the '
           'other 3, so this card can place at most 27 of the 30.')

P1, P2 = 1, 2
ID = 'geography-2020-ol-'
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
                     (S(5 if int(q) >= 7 else 4, start, end),),
                     criteria, topic, atlas, ID + f'p1-q{q}' + ('' if index == 0 else f'-{key}'),
                     sources, stem, row_labels=labels))
    return out


# ---------------------------------------------------------------- Part One --
TICK = 'Tick (✓) the correct box.'
Q1S = (L(3, 'Examine the diagram above showing the different layers of the earth', 'following questions.'),)
Q2S = (L(4, 'Examine the diagram above of an earthquake, and answer each of the following questions.'),)
Q3S = (L(5, 'Examine the photographs above.', 'completed for you.'),)
Q4S = (L(6, 'Examine the map above and answer each of the following questions.'),)
Q5S = (L(7, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper and answer',
         'following questions.', nth=0),)
Q6S = (L(7, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper and answer',
         'following questions.', nth=1),)
Q7S = (L(8, 'Examine the aerial photograph of Arklow accompanying this paper.'),)
Q10S = (L(10, 'Examine the table above which shows the mean monthly temperatures', 'following questions.'),)
Q11S = (L(11, 'Examine the chart above and answer each of the following questions.'),)
Q12S = (L(12, 'Examine the satellite images above and answer each of the following questions.'),)

PART_ONE = part_one_romans('1', 3, L(3, 'Layers of the Earth'), Q1S, ('page',), [
    ('(i)', L(3, '(i) Match each of the letters A, B, C and D with the feature', 'table below.'),
     'Q.1 (i)', 'Q.1 (ii)', rows(['Q.1 (i) · A · 2m', '=B · 2m', '=D · 2m', '=C · 2m']), '0-0', PS,
     (L(3, 'Crust'), L(3, 'Inner Core'), L(3, 'Mantle', nth=0), L(3, 'Outer Core'))),
    ('(ii)', (L(3, '(ii) What is the name of the molten rock found in the mantle?', TICK),
              L(3, 'Magma'), L(3, 'Lava')),
     'Q.1 (ii)', 'Q.2 (i)', (fixed('Molten rock', 2, 'Q.1 (ii) · Magma · 2m · Total 10m'),), '0-0', PS + EV),
])
PART_ONE += part_one_romans('2', 4, L(4, 'Earthquakes'), Q2S, ('page',), [
    ('(i)', L(4, '(i) Match each of the earthquake terms with the description', 'table below.'),
     'Q.2 (i)', 'Richter', rows(['Q.2 (i) · B · 2m', '=D · 2m', '=C · 2m', '=A · 2m']), '0-7', EV,
     (L(4, 'Focus', nth=1), L(4, 'Epicentre', nth=1), L(4, 'Seismic waves', nth=1), L(4, 'Fault', nth=1))),
    ('(ii)', L(4, '(ii) What scale is used to measure the magnitude (strength) of an earthquake?'),
     'Richter', 'Q.3 (i)',
     (fixed('Scale', 2, ('Richter scale /', 'Q.2 (ii) · 2m · Total 10m', 'Moment magnitude scale')),), '0-7', EV),
])
PART_ONE += [
    T('p1-3-i', P1, '3', '(i)', 6, 5, L(5, 'River Landforms'),
      (L(5, '(i) Match each of the photographs A, B, C and D with the landform', 'table below.'),),
      (S(4, 'Q.3 (i)', '(C) Deposition'), S(4, 'A (Deposition)', 'Q.4 (i)')),
      (fixed('Row 1', 2, 'Q.3 (i) · D Q.3 (ii) (Erosion) · 2m'), fixed('Row 2', 2, 'B Erosion · 2m + 2m'),
       fixed('Row 3', 2, 'A (Deposition) · 2m · Total 10m')),
      '0-9', RIVERS, ID + 'p1-q3', ('page',), Q3S,
      row_labels=(L(5, 'V-shaped valley'), L(5, 'Waterfall'), L(5, 'Delta'))),
    T('p1-3-ii', P1, '3', '(ii)', 4, 5, L(5, 'River Landforms'),
      (L(5, '(ii) State whether each of the landforms named in the table', 'erosion or deposition.'),),
      (S(4, 'B Erosion', 'A (Deposition)'),),
      (fixed('Row 1', 2, 'B Erosion · 2m + 2m'), fixed('Row 2', 2, '(C) Deposition · 2m')),
      '0-9', RIVERS, ID + 'p1-q3-ii', ('page',), Q3S,
      row_labels=(L(5, 'Waterfall'), L(5, 'Floodplain'))),
]
PART_ONE += part_one_romans('4', 6, L(6, 'Rock Types'), Q4S, ('page',), [
    ('(i)', L(6, '(i) Match each of the location letters A, B, C and D with the rock type', 'table below.'),
     'Q.4 (i)', 'Q.4 (ii)', rows(['Q.4 (i) · C · 2m', '=B · 2m', '=A · 2m', '=D · 2m']), '0-1', RW,
     (L(6, 'Granite'), L(6, 'Basalt'), L(6, 'Limestone'), L(6, 'Sandstone'))),
    ('(ii)', (L(6, '(ii) State whether the following statement is true or false.'),
              L(6, 'Marble is an example of a metamorphic rock.')),
     'Q.4 (ii)', 'Q.5 (i)', (fixed('True or false', 2, 'Q.4 (ii) · True · 2m · Total 10m'),), '0-1', RW),
])
PART_ONE += part_one_romans('5', 7, L(7, 'Ordnance Survey Map', nth=0), Q5S, ('map', 'legend'), [
    ('(i)', L(7, '(i) What is the height, in metres, of the highest point on the map?'),
     'Q.5 (i)', 'Q.5 (ii)', (fixed('Height', 5, 'Q.5 (i) · 280 (metres) · 5m'),), '2-6', MAP),
    ('(ii)', (L(7, '(ii) What is the length of the M11 motorway', TICK), L(7, '3.7 km'), L(7, '2.2 km')),
     'Q.5 (ii)', 'Q.6 (i)', (fixed('Length', 5, 'Q.5 (ii) · 3.7 km · 5m · Total 10m'),), '2-6', MAP),
])
PART_ONE += part_one_romans('6', 7, L(7, 'Ordnance Survey Map', nth=1), Q6S, ('map', 'legend'), [
    ('(i)', L(7, '(i) Name each of the features that can be found at each of the following grid references:'),
     'Q.6 (i)', 'Q.6 (ii)',
     rows(['Q.6 (i) · Railway Station · 2m', '18 hole golf course · 2m', 'Boating Activities · 2m',
           'Burial Ground · 2m']), '2-6', MAP,
     (L(7, 'T 242 728'), L(7, 'T 194 776'), L(7, 'T 256 733'), L(7, 'T 198 759'))),
    ('(ii)', L(7, '(ii) Draw the Ordnance Survey map symbol for Boating Activities in the box below.'),
     'Q.6 (ii)', 'Page 2 of', (fixed('Symbol', 2, 'Q.6 (ii) · Valid symbol · 2m · Total 10m'),), '2-6', MAP),
])
PART_ONE += part_one_romans('7', 8, L(8, 'Aerial Photograph'), Q7S, ('aerial',), [
    ('(i)', L(8, '(i) Match the feature with the location on the aerial photograph', 'in the table below.', nth=0),
     'Q.7 (i)', 'Q.7 (ii)', rows(['Q.7 (i) · D · 2m', '=A · 2m', '=B · 2m', '=C · 2m']), '2-8', AER,
     (L(8, 'Right background'), L(8, 'Right middleground'), L(8, 'Left foreground'), L(8, 'Left background'))),
    ('(ii)', (L(8, '(ii) Indicate whether the aerial photograph accompanying this paper is a vertical',
                'correct box.'), L(8, 'Vertical'), L(8, 'Oblique')),
     'Q.7 (ii)', 'Q.8', (fixed('Vertical or oblique', 2, 'Q.7 (ii) · Oblique · 2m · Total 10m'),), '2-8', AER),
])
PART_ONE += [
    T('p1-8', P1, '8', '', 10, 8, L(8, 'Regions'),
      (L(8, 'Match the description of the region with the example of the region', 'in the table below.'),),
      (S(5, 'Q.8', 'Q.9 (i)'),), rows(['Q.8 · E · 2m', '=D · 2m', '=C · 2m', '=B · 2m', 'A · 2m · Total 10m']),
      '1-0', IRL + EURO, ID + 'p1-q8', ('page',),
      row_labels=(L(8, 'A Département'), L(8, 'Sambre-Meuse, Belgium'), L(8, 'Munster Ridge and Valley'),
                  L(8, 'The Greater Dublin Area'), L(8, 'The Mediterranean'))),
]
PART_ONE += part_one_romans('9', 9, L(9, 'Economic Activities'), (), ('page',), [
    ('(i)', L(9, '(i) Examine the photographs above and indicate whether each is an example', 'table below.'),
     'Q.9 (i)', 'Q.9 (ii)',
     (fixed('A', 2, 'Q.9 (i) · Secondary · 2m'), fixed('B', 2, 'Tertiary · 2m'),
      fixed('C', 2, '=Primary · 2m@0'), fixed('D', 2, '=Primary · 2m@1')), '3-0', ECON),
    ('(ii)', L(9, '(ii) Name one primary economic activity NOT shown in the photographs above.'),
     'Q.9 (ii)', 'Q.10', (fixed('Primary economic activity', 2, 'Q.9 (ii) · Valid answer · 2m · Total 10m'),),
     '3-0', ECON),
])
PART_ONE += part_one_romans('10', 10, L(10, 'Weather'), Q10S, ('page',), [
    ('(i)', L(10, '(i) What was the highest mean monthly temperature (°C) at Knock Airport in 2019?'),
     'Q.10 · (i)', '(ii) 6', (fixed('Temperature', 2, 'Q.10 · (i) 15 (°C) · 2m'),), '2-0', GRAPH + WEATHER),
    ('(ii)', L(10, '(ii) What was the mean temperature (°C) for March?'),
     '(ii) 6', '(iii) August', (fixed('Temperature', 2, '(ii) 6 (°C) · 2m'),), '2-0', GRAPH + WEATHER),
    ('(iii)', L(10, '(iii) Which month experienced the highest level of rainfall?'),
     '(iii) August', '(iv) 5', (fixed('Month', 2, '(iii) August · 2m'),), '2-0', GRAPH + WEATHER),
    ('(iv)', L(10, '(iv) In how many months were the mean temperatures greater than 9°C?'),
     '(iv) 5', '(v) 408', (fixed('Number of months', 2, '(iv) 5 · 2m'),), '2-0', GRAPH + WEATHER),
    ('(v)', L(10, '(v) What was the total rainfall (mm) for June, July and August combined?'),
     '(v) 408', 'Q.11', (fixed('Total rainfall', 2, '(v) 408 (mm) · 2m · Total 10m'),), '2-0', GRAPH + WEATHER),
])
PART_ONE += part_one_romans('11', 11, L(11, 'Tourism in Ireland'), Q11S, ('page',), [
    ('(i)', L(11, '(i) Which region attracted 17% of overseas tourists in 2017?'),
     'Q.11 · (i)', '(ii) Midlands', (fixed('Region', 2, 'Q.11 · (i) South west · 2m'),), '2-0', GRAPH),
    ('(ii)', L(11, '(ii) Which region attracted the lowest percentage of overseas tourists in 2017?'),
     '(ii) Midlands', '(iii) 5', (fixed('Region', 2, '(ii) Midlands · 2m'),), '2-0', GRAPH),
    ('(iii)', L(11, '(iii) What percentage of overseas tourists visited the Border region?'),
     '(iii) 5', '(iv) One valid', (fixed('Percentage', 2, '(iii) 5 (%) · 2m'),), '2-0', GRAPH),
    ('(iv)', L(11, '(iv) Name one tourist attraction found in Dublin.'),
     '(iv) One valid', '(v) One valid', (fixed('Tourist attraction', 2, '(iv) One valid attraction · 2m'),),
     '1-4', IRL),
    ('(v)', L(11, '(v) State one problem associated with tourism.'),
     '(v) One valid', 'Q.12', (fixed('Problem', 2, '(v) One valid problem · 2m · Total 10m'),), '1-4', IRL),
])
PART_ONE += part_one_romans('12', 12, L(12, 'Satellite Interpretation'), Q12S, ('page',), [
    ('(i)', L(12, '(i) Match each of the images A, B, C and D with the description', 'table below.'),
     'Q.12 (i)', 'Q.12 (ii)', rows(['Q.12 (i) · A · 2m', '=D · 2m', '=B · 2m', '=C · 2m']), '2-8', AER,
     (L(12, 'Byrd Glacier, Antarctica'), L(12, 'Tombolo, Pakistan'), L(12, 'Wildfire in California'),
      L(12, 'Mt. Etna erupting'))),
    ('(ii)', (L(12, '(ii) State whether the following statement is true or false.'),
              L(12, 'Longshore drift is an important process in the formation of tombolos.')),
     'Q.12 (ii)', 'Page 3 of', (fixed('True or false', 2, 'Q.12 (ii) · True · 2m · Total 10m'),), '0-10', SEA),
])


# ---------------------------------------------------------------- Part Two --
def romans(q, page, title, stem, first_id, sources, parts):
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
PART_TWO = [
    sketch(4, L(4, 'Ordnance Survey Map'),
           L(4, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper.',
             'An area of land over 200m in height.'),
           7, ID + 'p2-q1a', '2-6', MAP + SEA + RIVERS, ('map', 'legend'), 'portrait',
           ('The coastline', 'A beach', 'An area of mixed woodland', 'The Avoca River',
            'An area of land over 200m in height')),
]
PART_TWO += romans('1B', 4, L(4, 'Rocks'), (), ID + 'p2-q1b', (), [
    ('(i)', 20, L(4, '(i) Name one example of an igneous rock', 'igneous rocks are formed.'),
     S(8, '(i) · Name one example of an igneous', '(ii) · Name one example of a sedimentary'),
     (fixed('Igneous rock named', 2, 'Name of igneous rock · 2m'),
      srp3('Description/explanation', 6, 'Description/explanation 6 SRPS @ 3m each · 18m')), '0-1', RW),
    ('(ii)', 20, L(4, '(ii) Name one example of a sedimentary rock', 'sedimentary rocks are formed.'),
     S(8, '(ii) · Name one example of a sedimentary', 'Total 40m'),
     (fixed('Sedimentary rock named', 2, 'Name of sedimentary rock · 2m'),
      srp3('Description/explanation', 6, 'Description/explanation 6 SRPS @ 3m each · 18m')), '0-1', RW),
])
PART_TWO.append(T(
    'p2-1c', P2, '1C', '', 30, 4, L(4, 'Human Interaction with Surface Processes'),
    (L(4, 'Examine how humans interact with one of the following surface processes:', 'Mass movement processes.'),),
    (S(8, 'Interaction identified · 3m', 'Total 30m'),),
    (fixed('Interaction identified', 3, 'Interaction identified · 3m'),
     srp3('Explanation', 9, 'Explanation 9 SRP’s @ 3m each · 27m')),
    '0-6', RIVERS, ID + 'p2-q1c-river-processes',
    routes=bullet_routes('p2-q1c-', SURFACE, atlas=dict(zip(SURFACE, (RIVERS, SEA, RW))))))

Q2AS = (L(5, 'Read the information above and answer each of the following questions.'),)
PART_TWO += romans('2A', 5, L(5, 'Volcanoes', nth=0), Q2AS, ID + 'p2-q2a', ('page',), [
    ('(i)', 6, L(5, '(i) Name two materials released by a volcano during a volcanic eruption.'),
     S(9, '(i) · Name two materials', '(ii) · What country'),
     (fixed('Two materials', 6, ('Two valid materials @ 3m each · 6m', 'Lava / gas / ash / rock'), (0, 3, 6)),),
     '0-7', EV),
    ('(ii)', 3, L(5, '(ii) What country, named in the text, had to evacuate at least 13,000 people',
                  'volcanic eruptions?'),
     S(9, '(ii) · What country', '(iii) List two'), (fixed('Country', 3, 'Indonesia · 3m'),), '0-7', EV),
    ('(iii)', 6, L(5, '(iii) List two effects of volcanic activity that are mentioned in the report.'),
     S(9, '(iii) List two', '(iv) Explain briefly'),
     (fixed('Two effects', 6, ('Two valid effects @ 3m each · 6m',
                               'Death/build and shape the land/create mountains/ create new seafloor/deposit',
                               'minerals and nutrients/enrich soil.'), (0, 3, 6)),), '0-7', EV),
    ('(iv)', 6, L(5, '(iv) Explain briefly one other positive effect of volcanic activity', 'in the report.'),
     S(9, '(iv) Explain briefly', '(v) · Name one'),
     (srp3('Brief explanation', 2, 'Brief explanation two SRP’s @ 3m each · 6m'),), '0-7', EV),
    ('(v)', 3, L(5, '(v) Name one example of a volcano that you have studied.'),
     S(9, '(v) · Name one', '(vi) Explain briefly'), (fixed('Volcano', 3, 'Valid example · 3m'),), '0-7', EV),
    ('(vi)', 6, L(5, '(vi) Explain briefly what is meant by the term dormant volcano.'),
     S(9, '(vi) Explain briefly', 'Total 30m'),
     (srp3('Brief explanation', 2, 'Brief explanation two SRP’s @ 3m each · 6m'),), '0-7', EV),
])

ROCK = ('Quarrying', 'Mining', 'Oil/Gas exploitation', 'Geothermal energy production.')
PART_TWO += [
    T('p2-2b', P2, '2B', '', 40, 5, L(5, 'Landform Development'),
      (L(5, '(i) Explain, with the aid of diagrams, the formation of any two landforms.'),),
      (S(10, 'Formation of any two landforms @ 20m each.', 'Total 40m'),),
      two_of('Landform', 20, 'Formation of any two landforms @ 20m each.', 'For each landform:',
             ('Landform named · 1m', 'Diagram(s) two aspects @ 2m each · 4m',
              'Formation explained 5 SRP’s @ 3m each · 15m'),
             ((0, 1), (0, 2, 4), steps(15, 3))),
      '0-4', PS_SURFACE, ID + 'p2-q2b-route-i',
      routes=(
          Route('route-i', 'Route (i)', ID + 'p2-q2b-route-i', False),
          Route('route-ii', 'Route (ii)', ID + 'p2-q2b-route-ii', False,
                prompt=(L(5, '(ii) Describe and explain any two processes of mass movement.'),),
                scheme=(S(10, 'Any two processes @ 20m each', 'Total 40m'),),
                criteria=two_of('Process', 20, 'Any two processes @ 20m each', 'For each process:',
                                ('Process stated · 2m', 'Description / Explanation 6 SRP’s @ 3m each · 18m'),
                                ((0, 2), steps(18, 3))),
                topic='0-8', atlas=RW),
      )),
    T('p2-2c', P2, '2C', '', 30, 5, L(5, 'Human Interaction with the Rock Cycle'),
      (L(5, 'Describe and explain how humans interact with the rock cycle', 'Geothermal energy production.'),),
      (S(11, 'Description / explanation 10', 'Total 30m'),),
      (srp3('Description/explanation', 10, 'Description / explanation 10 SRP’s @ 3m each · 30m'),),
      '0-6', RW, ID + 'p2-q2c-quarrying', routes=bullet_routes('p2-q2c-', ROCK)),
]

Q3AS = (L(6, 'Examine the photographs above and answer each of the following questions.'),)
PART_TWO += romans('3A', 6, L(6, 'Landforms and Processes'), Q3AS, ID + 'p2-q3a', ('page',), [
    ('(i)', 9, L(6, '(i) In your answer book, match each of the letters A, B and C', 'Beach.'),
     S(12, '• Drumlin', '(ii) · In your answer book'),
     (fixed('Row 1', 3, '• Drumlin · B · 3m'), fixed('Row 2', 3, '• Cliff · A · 3m'),
      fixed('Row 3', 3, '• Beach. · C · 3m')), '0-4', GLAC + SEA, (),
     (L(6, 'Drumlin'), L(6, 'Cliff'), L(6, 'Beach'))),
    ('(ii)', 9, L(6, '(ii) In your answer book, match each of the letters A, B and C', 'Glacial deposition.'),
     S(12, '• Coastal deposition', '(iii) · Explain briefly'),
     (fixed('Row 1', 3, '• Coastal deposition · C · 3m'), fixed('Row 2', 3, '• Coastal erosion · A · 3m'),
      fixed('Row 3', 3, '• Glacial deposition · B · 3m')), '0-4', GLAC + SEA, (),
     (L(6, 'Coastal deposition'), L(6, 'Coastal erosion'), L(6, 'Glacial deposition'))),
    ('(iii)', 12, L(6, '(iii) Explain briefly each of the following:', 'Abrasion.'),
     S(12, 'Two brief explanations', 'Total 30m'),
     (srp3('Explanation 1', 2, 'Two brief explanations - two SRP’s @ 3m each · 12m'),
      srp3('Explanation 2', 2, 'Two brief explanations - two SRP’s @ 3m each · 12m')), '0-4', RIVERS + SEA, (),
     (L(6, 'Hydraulic action'), L(6, 'Abrasion'))),
])
PART_TWO += romans('3B', 6, L(6, 'Karst Landscapes'), (), ID + 'p2-q3b', (), [
    ('(i)', 4, L(6, '(i) Name one example of a karst landscape.'),
     S(13, '(i) · Name one example of a karst', '(ii) · Explain'),
     (fixed('Karst landscape', 4, 'One valid example @ 4m · 4m'),), '0-3', KARST),
    ('(ii)', 18, L(6, '(ii) Explain, with the aid of a diagram, how one surface feature', 'was formed.'),
     S(13, '(ii) · Explain, with the aid', '(iii) Explain, with the aid'),
     (fixed('Feature named', 2, 'Feature named · 2m'),
      fixed('Diagram', 4, 'Diagram two aspects @ 2m each · 4m', (0, 2, 4)),
      srp3('Formation explained', 4, 'Formation explained 4 SRP’s @ 3m each · 12m')), '0-3', KARST),
    ('(iii)', 18, L(6, '(iii) Explain, with the aid of a diagram, how one underground feature', 'was formed.'),
     S(13, '(iii) Explain, with the aid', 'Total 40m'),
     (fixed('Feature named', 2, 'Feature named · 2m'),
      fixed('Diagram', 4, 'Diagram two aspects @ 2m each · 4m', (0, 2, 4)),
      srp3('Formation explained', 4, 'Formation explained 4 SRP’s @ 3m each · 12m')), '0-3', KARST),
])
PART_TWO.append(T(
    'p2-3c', P2, '3C', '', 30, 6, L(6, 'Fold Mountains'),
    (L(6, 'With the aid of a diagram(s), describe and explain how fold mountains are formed.'),),
    (S(13, 'Diagram two items', 'Total 30m'),),
    (fixed('Diagram', 6, 'Diagram two items @ 3m each · 6m', (0, 3, 6)),
     srp3('Description/explanation', 8, 'Description / explanation 8 SRP’s @ 3m each · 24m')),
    '0-2', RW + PS, ID + 'p2-q3c'))

SHOWN = 'Shown · 4m graded (4/2/0)'
NAMED_SHOWN = sums((0, 2), (0, 2, 4))
PART_TWO.append(T(
    'p2-4a', P2, '4A', '', 30, 7, L(7, 'Irish Region'),
    (L(7, 'Draw a sketch map of Ireland.', 'in this region.'),),
    (S(14, 'Outline of Ireland', 'Total 30m'),),
    (fixed('Outline of Ireland', 6, 'Outline of Ireland · 6m graded (6/4/2/0)', (0, 2, 4, 6)),
     Criterion('Region', 6, NAMED_SHOWN, 'exact', ('Region: · Named · 2m', f'={SHOWN}@0')),
     Criterion('River', 6, NAMED_SHOWN, 'exact', ('River: · Named · 2m', f'={SHOWN}@1')),
     Criterion('Town/City', 6, NAMED_SHOWN, 'exact', ('Town/City: · Named · 2m', f'={SHOWN}@2')),
     Criterion('Relief (upland/lowland)', 6, NAMED_SHOWN, 'exact',
               ('Relief (upland/lowland): · Named · 2m', f'={SHOWN}@3'))),
    '1-4', IRL, ID + 'p2-q4a'))
Q4BI = L(7, '(i) Name two countries that have joined the European Union since Ireland joined in 1973.')
PART_TWO += romans('4B', 7, L(7, 'European Union Expansion'), (), ID + 'p2-q4b', (), [
    ('(i)', 4, Q4BI, S(15, '(i) · Name two countries', '(ii) · Explain the advantages'),
     (fixed('Two countries', 4, 'Two countries named @ 2m each · 4m', (0, 2, 4)),), '1-5', EURO),
    ('(ii)', 18, L(7, '(ii) Explain the advantages of European Union expansion for Ireland.'),
     S(15, '(ii) · Explain the advantages', '(iii) Explain the disadvantages'),
     (srp3('Explanation', 6, 'Explanation 6 SRP’s @ 3m each · 18m'),), '1-5', EURO + EU),
    ('(iii)', 18, L(7, '(iii) Explain the disadvantages of European Union expansion for Ireland.'),
     S(15, '(iii) Explain the disadvantages', 'Total 40m'),
     (srp3('Explanation', 6, 'Explanation 6 SRP’s @ 3m each · 18m'),), '1-5', EURO + EU),
])
FACTORS_4C = ('Climate', 'Relief and soils', 'Markets.')
PART_TWO.append(T(
    'p2-4c', P2, '4C', '', 30, 7, L(7, 'Agriculture – European Region'),
    (L(7, 'Explain how two of the factors listed below influence the development of agriculture', 'Markets.'),),
    (S(15, 'Explanation of factor 1', 'Total 30m'),),
    (srp3('Factor 1', 5, 'Explanation of factor 1: · 5 SRP’s @ 3m each · 15m'),
     srp3('Factor 2', 5, 'Explanation of factor 2: · 5 SRP’s @ 3m each · 15m')),
    '1-5', EURO, ID + 'p2-q4c', absorbs=pool(ID + 'p2-q4c-', FACTORS_4C, 2)[1]))

Q5AS = (L(8, 'Examine the information above and answer each of the following questions.'),)
PART_TWO += romans('5A', 8, L(8, 'Life Expectancy in the European Union'), Q5AS, ID + 'p2-q5a', ('page',), [
    ('(i)', 3, L(8, '(i) In which country was the male life expectancy 78.8 in 2019?'),
     S(16, '(i) · In which country', '(ii) · In which country'), (fixed('Country', 3, 'Greece · 3m'),), '2-0', GRAPH),
    ('(ii)', 3, L(8, '(ii) In which country was female life expectancy the longest in 2019?'),
     S(16, '(ii) · In which country', '(iii) · Name two'), (fixed('Country', 3, 'Sweden · 3m'),), '2-0', GRAPH),
    ('(iii)', 6, L(8, '(iii) Name two countries whose male life expectancy is above the EU Average for males.'),
     S(16, '(iii) · Name two', '(iv) Calculate'),
     (fixed('Two countries', 6, ('Sweden/Netherlands/Ireland/Greece', 'Two @ 3m each · 6m'), (0, 3, 6)),),
     '2-0', GRAPH),
    ('(iv)', 6, L(8, '(iv) Calculate the difference in life expectancy for females', 'the EU Average.'),
     S(16, '(iv) Calculate', '(v) · Explain briefly'), (fixed('Difference', 6, '3.8 (years) · 6m'),), '2-0', GRAPH),
    ('(v)', 12, L(8, '(v) Explain briefly two reasons why some countries have lower life expectancies',
                  'other countries.'),
     S(16, '(v) · Explain briefly', 'Total 30m'),
     (srp3('Reason 1', 2, 'Brief explanation of reason 1: · 2 SRP’s @ 3m each · 6m'),
      srp3('Reason 2', 2, 'Brief explanation of reason 2: · 2 SRP’s @ 3m each · 6m')), '4-0', POP),
])
PART_TWO.append(T(
    'p2-5b', P2, '5B', '', 30, 8, L(8, 'Urban Growth in a European Region'),
    (L(8, 'Discuss the reasons for the growth of an urban area in a European region', 'that you have studied.'),),
    (S(16, 'Discussion 10 SRP', 'Total 30m'),),
    (srp3('Discussion', 10, 'Discussion 10 SRP’s @ 3m each · 30m'),),
    '1-5', EURO + URB, ID + 'p2-q5b'))
Q5CS = (L(8, 'Answer each of the following with reference to an Irish region that you have studied.'),)
Q5CI = L(8, '(i) Name one tertiary economic activity that contributes to the economy of this region.')
PART_TWO += romans('5C', 8, L(8, 'Tertiary Economic Activities – Irish Region'), Q5CS, ID + 'p2-q5c', (), [
    ('(i)', 4, Q5CI, S(17, '(i) · Name one tertiary', '(ii) · Explain the advantages'),
     (fixed('Tertiary economic activity named', 4, 'Tertiary economic activity named · 4m'),), '1-4', IRL),
    ('(ii)', 27, L(8, '(ii) Explain the advantages that this region has for the development of the tertiary',
                   'part (i) above.'),
     S(17, '(ii) · Explain the advantages', '(iii) Describe one challenge'),
     (srp3('Advantages explained', 9, 'Advantages explained 9 SRP’s @ 3m each · 27m'),), '1-4', IRL, (Q5CI,)),
    ('(iii)', 9, L(8, '(iii) Describe one challenge faced by this tertiary economic activity in this region.'),
     S(17, '(iii) Describe one challenge', 'Total 40m'),
     (srp3('One challenge described', 3, 'One challenge described 3 SRP’s @ 3m each · 9m'),), '1-4', IRL, (Q5CI,)),
])

Q6AS = (L(9, 'Examine the chart above showing the percentage of people employed', 'following questions.'),)
PART_TWO += romans('6A', 9, L(9, 'Irish Employment'), Q6AS, ID + 'p2-q6a', ('page',), [
    ('(i)', 3, L(9, '(i) Which category employed the most people in 2017?'),
     S(18, '(i) · Which category', '(ii) · Calculate'),
     (fixed('Category', 3, 'Agriculture, Forestry and Fishing · 3m'),), '2-0', GRAPH),
    ('(ii)', 6, L(9, '(ii) Calculate X the percentage (%) employed in the Food sector.'),
     S(18, '(ii) · Calculate', '(iii) · Which category'), (fixed('Percentage', 6, '30 (%) · 6m'),), '2-0', GRAPH),
    ('(iii)', 3, L(9, '(iii) Which category on the chart is an example of primary economic activity?'),
     S(18, '(iii) · Which category', '(iv) Name any two'),
     (fixed('Category', 3, 'Agriculture, Forestry and Fishing · 3m'),), '2-0', GRAPH),
    ('(iv)', 6, L(9, '(iv) Name any two crops grown in Ireland.'),
     S(18, '(iv) Name any two', '(v) · Name one Irish'),
     (fixed('Two crops', 6, 'Two crops named@ 3m each · 6m', (0, 3, 6)),), '1-4', IRL),
    ('(v)', 6, L(9, '(v) Name one Irish food product and name one Irish beverage product.'),
     S(18, '(v) · Name one Irish', '(vi) Explain briefly'),
     (fixed('Irish food product named', 3, 'Irish food product named · 3m'),
      fixed('Irish beverage product named', 3, 'Irish beverage product named · 3m')), '1-4', IRL),
    ('(vi)', 6, L(9, '(vi) Explain briefly one reason why there is only 2% employment', 'industry.'),
     S(18, '(vi) Explain briefly', 'Total 30m'),
     (srp3('Brief explanation', 2, 'Brief explanation two SRP’s @ 3m each · 6m'),), '1-4', IRL),
])
ACTIVITIES = ('The factors influencing agriculture in the region', 'The importance of manufacturing to the region',
              'The reasons why tourists are attracted to the region.')
PART_TWO += [
    T('p2-6b', P2, '6B', '', 40, 9, L(9, 'Economic Activities – Continental / Sub-Continental Region'),
      (L(9, 'Explain any two of the following with reference to a Continental / Sub-Continental region',
         'The reasons why tourists are attracted to the region.'),),
      (S(19, 'Region named · 1m', 'Total 40m'),),
      (fixed('Region named', 1, 'Region named · 1m'),
       srp3('Activity 1 explained', 7, 'Activity 1 explained 7 SRP’s @ 3m each · 21m'),
       srp3('Activity 2 explained', 6, 'Activity 2 explained 6 SRP’s @ 3m each · 18m')),
      '1-6', CONT, ID + 'p2-q6b', absorbs=pool(ID + 'p2-q6b-', ACTIVITIES, 2)[1]),
    T('p2-6c', P2, '6C', '', 30, 9, L(9, 'Regions and Culture'),
      (L(9, 'The culture of a region can often be determined by the following factors:'),
       Lift(9, 'Religion', 'Music/Dance', row=True),
       L(9, 'Describe and explain the importance of culture in any region that you have studied.')),
      (S(19, 'Description / explanation of region', 'Total 30m'),),
      (srp3('Description/explanation', 10, 'Description / explanation of region 10 SRP’s @ 3m each · 30m'),),
      '1-3', IRL + EURO, ID + 'p2-q6c'),
]

PART_TWO.append(sketch(
    11, L(11, 'Ordnance Survey Map'),
    L(11, 'Examine the Ordnance Survey map and legend accompanying this paper.', 'south of the Avoca River.'),
    20, ID + 'p2-q7a', '2-6', MAP, ('map', 'legend'), 'portrait',
    ('The entire route of the M11 motorway', 'The entire route of the railway line', 'An 18 hole golf course',
     'A post office', 'The built up area of Arklow south of the Avoca River')))
Q7BI = L(11, '(i) Name one example of a developed economy that you have studied.')
PART_TWO += romans('7B', 11, L(11, 'Economic Development – Developed Economy'), (), ID + 'p2-q7b', (), [
    ('(i)', 4, Q7BI, S(21, '(i) · Name one example of a developed', '(ii) · Explain the reasons'),
     (fixed('Developed economy named', 4, 'Developed economy named · 4m'),), '3-0', ECON),
    ('(ii)', 18, L(11, '(ii) Explain the reasons for the growth of tourism or financial services', 'part (i) above.'),
     S(21, '(ii) · Explain the reasons', '(iii) Explain one benefit'),
     (srp3('Explanation', 6, 'Explanation 6 SRP’s @ 3m each · 18m'),), '3-0', ECON, (Q7BI,)),
    ('(iii)', 9, L(11, '(iii) Explain one benefit that tourism or financial services brings to developed economies.'),
     S(21, 'Explanation 3 SRP', '(iv) Explain one problem', after='(iii) Explain one benefit'),
     (srp3('Explanation', 3, 'Explanation 3 SRP’s @ 3m each · 9m'),), '3-0', ECON),
    ('(iv)', 9, L(11, '(iv) Explain one problem caused by tourism or financial services.'),
     S(21, 'Explanation 3 SRP', 'Total 40m', after='(iv) Explain one problem'),
     (srp3('Explanation', 3, 'Explanation 3 SRP’s @ 3m each · 9m'),), '3-0', ECON),
])
PART_TWO += romans('7C', 11, L(11, 'Environmental Impact – Fossil Fuels'), (), ID + 'p2-q7c', (), [
    ('(i)', 6, L(11, '(i) Name two examples of fossil fuels.'),
     S(21, '(i) · Name two examples of fossil', '(ii) · Describe and explain'),
     (fixed('Two fossil fuels', 6, 'Two valid examples named @ 3m each · 6m', (0, 3, 6)),), '3-5', ECON),
    ('(ii)', 24, L(11, '(ii) Describe and explain the impact of burning fossil fuels on the environment.'),
     S(21, '(ii) · Describe and explain the impact', 'Total 30m'),
     (srp3('Description and explanation', 8, 'Description and explanation 8 SRP’s @ 3m each · 24m'),),
     '3-4', ENV),
])

GRAPH_OL = (fixed('Graph paper', 3, 'Graph paper · 3m', (0, 3)),
            fixed('Vertical axis labelled / circle', 3, 'Vertical axis labelled/Circle · 3m graded (3/1/0)', (0, 1, 3)),
            fixed('Horizontal axis labelled / centred', 3, 'Horizontal axis labelled/Centred · 3m graded (3/1/0)',
                  (0, 1, 3)),
            fixed('5 items illustrated', 15, '5 items @ 3m each graded (3/1/0) · 15m', sums(*[(0, 1, 3)] * 5)))
Q8AS = (L(12, 'Examine the table above showing the best performing multinational companies', 'following questions.'),)
PART_TWO += romans('8A', 12, L(12, 'Multinational Companies', nth=0), Q8AS, ID + 'p2-q8a', ('page',), [
    ('(i)', 24, L(12, '(i) Using graph paper, draw a suitable graph to illustrate this data.'),
     S(22, 'Graph paper', '(ii) · In your answer book'), GRAPH_OL, '2-0', GRAPH),
    ('(ii)', 6, L(12, '(ii) In your answer book, calculate the difference in market value',
                  'fifth ranked multinational company.'),
     S(22, '(ii) · In your answer book', 'Total 30m'), (fixed('Difference', 6, '440 ($US billion) · 6m'),),
     '2-0', GRAPH + MNC),
])
Q8BS = (L(12, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper.'),
        L(12, 'It is proposed to build a new hotel at the point T 253 735.'))
PART_TWO += romans('8B', 12, L(12, 'Ordnance Survey Map'), Q8BS, ID + 'p2-q8b', ('map', 'legend'), [
    ('(i)', 15, L(12, '(i) Describe and explain the advantages of this location.'),
     S(22, '(i) · Describe and explain the advantages', '(ii) · Describe and explain the disadvantages'),
     (srp3('Description/explanation of the advantages', 5,
           'Description / explanation of the advantages 5 SRPs @ 3m each · 15m'),), '3-0', ECON + MAP),
    ('(ii)', 15, L(12, '(ii) Describe and explain the disadvantages of this location.'),
     S(22, '(ii) · Describe and explain the disadvantages', '(iii) Using a six-figure'),
     (srp3('Description/explanation of the disadvantages', 5,
           'Description / explanation of the advantages 5 SRPs @ 3m each · 15m'),), '3-0', ECON + MAP),
    ('(iii)', 10, L(12, '(iii) Using a six-figure grid reference, suggest an alternative location', 'alternative location.'),
     S(22, '(iii) Using a six-figure', 'Total 40m'),
     (fixed('Six-figure grid reference', 4, 'Six-figure grid reference 4m graded · (4/2/0)', (0, 2, 4)),
      srp3('Reason briefly explained', 2, 'One reason briefly explained 2 SRPs @ 3m each · 6m')), '2-6', MAP + ECON),
])
Q8CI = L(12, '(i) Name one example of how the development of economic activities has resulted in',
         'conflict arising between people.')
PART_TWO += romans('8C', 12, L(12, 'Economic Activity and Conflict'), (), ID + 'p2-q8c', (), [
    ('(i)', 3, Q8CI, S(23, '(i) · Name one example', '(ii) · Describe and explain'),
     (fixed('Example named', 3, 'Valid example named · 3m'),), '3-4', ENV),
    ('(ii)', 27, L(12, '(ii) Describe and explain this conflict.'),
     S(23, '(ii) · Describe and explain', 'Total 30m'),
     (srp3('Description/explanation', 9, 'Description / explanation 9 SRP’s @ 3m each · 27m'),), '3-4', ENV, (Q8CI,)),
])

Q9AS = (L(13, 'Examine the chart above showing the percentage of primary energy supply', 'following questions.'),)
PART_TWO += romans('9A', 13, L(13, 'Energy in Ireland'), Q9AS, ID + 'p2-q9a', ('page',), [
    ('(i)', 3, L(13, '(i) Which fuel type provided the highest percentage of Ireland’s energy in 2017?'),
     S(24, '(i) · Which fuel type', '(ii) · What percentage'), (fixed('Fuel type', 3, 'Oil · 3m'),), '2-0', GRAPH),
    ('(ii)', 3, L(13, '(ii) What percentage of primary energy was provided by renewables in 2017?'),
     S(24, '(ii) · What percentage', '(iii) Calculate'), (fixed('Percentage', 3, '9 (%) · 3m'),), '2-0', GRAPH),
    ('(iii)', 6, L(13, '(iii) Calculate the percentage of primary energy provided by oil, gas and coal', '2017.'),
     S(24, '(iii) Calculate', '(iv) Name two'), (fixed('Percentage', 6, '85 (%) · 6m'),), '2-0', GRAPH),
    ('(iv)', 6, L(13, '(iv) Name two examples of renewable energy.'),
     S(24, '(iv) Name two', '(v) · Explain briefly'),
     (fixed('Two examples', 6, 'Two valid examples @ 3m each · 6m', (0, 3, 6)),), '3-5', ECON),
    ('(v)', 6, L(13, '(v) Explain briefly one advantage of renewable energy.'),
     S(24, 'One brief explanation', '(vi) Explain briefly', after='(v) · Explain briefly'),
     (srp3('Brief explanation', 2, 'One brief explanation two SRP’s @ 3m each · 6m'),), '3-5', ECON),
    ('(vi)', 6, L(13, '(vi) Explain briefly one disadvantage of renewable energy.'),
     S(24, 'One brief explanation', 'Total 30m', after='(vi) Explain briefly'),
     (srp3('Brief explanation', 2, 'One brief explanation two SRP’s @ 3m each · 6m'),), '3-5', ECON),
])
Q9BI = L(13, '(i) Name one multinational company located in Ireland that you have studied and name',
         'it manufactures.')
PART_TWO += romans('9B', 13, L(13, 'Multinational Company'), (), ID + 'p2-q9b', (), [
    ('(i)', 7, Q9BI, S(24, '(i) · Name one multinational', '(ii) · State where'),
     (fixed('MNC named', 4, 'Valid MNC named · 4m'), fixed('Product named', 3, 'One product named · 3m')),
     '3-2', MNC),
    ('(ii)', 21, L(13, '(ii) State where this multinational company is located in Ireland', 'at this location.'),
     S(24, '(ii) · State where', '(iii) · Explain one reason'),
     (fixed('Location', 3, 'Location · 3m'), srp3('Explanation', 6, 'Explanation 6 SRP’s @ 3m each · 18m')),
     '3-2', MNC, (Q9BI,)),
    ('(iii)', 12, L(13, '(iii) Explain one reason why this multinational company might decide to locate',
                    'country.'),
     S(24, '(iii) · Explain one reason', 'Total 40m'),
     (srp3('Explanation', 4, ('Explanation 4 SRP’s @ 3m each · 12m', 'Reason stated for one SRP')),),
     '3-2', MNC, (Q9BI,)),
])
# 9C: the scheme's two priced lines (3m + 24m) as printed, against the
# printed total of 30; the 3 marks the scheme allocates to no line stay
# unpriced (never derived or redistributed), so the card places at most 27.
PART_TWO.append(Task(
    'p2-9c', 2, '9C', '', 30, 13, L(13, 'European Union Policy'),
    (L(13, 'Explain how European Union policy has impacted on the Irish economy.'),),
    (S(25, 'Impact identified 1 SRP', None),),
    (srp3('Impact identified', 1, 'Impact identified 1 SRP · 3m'),
     srp3('Explanation', 8, 'Explanation 8 SRP’s @ 3m each · 24m')),
    '3-3', EU, (), ID + 'p2-q9c', False, note=NOTE_9C, unpriced=3))

GRAPH_10A = GRAPH_OL
Q10AS = (L(14, 'Examine the table above showing the estimated number of immigrants', 'following questions.'),)
TOWN_REASON = ('Three reasons @ 10m each', 'For each reason:', 'Aerial photograph evidence · 1m',
               'Explanation 3 SRP’s @ 3m each · 9m')
PART_TWO += romans('10A', 14, L(14, 'Immigration'), Q10AS, ID + 'p2-q10a', ('page',), [
    ('(i)', 24, L(14, '(i) Using graph paper, draw a suitable graph to illustrate this data.'),
     S(26, 'Graph paper', '(ii) · In your answer book'), GRAPH_10A, '2-0', GRAPH),
    ('(ii)', 6, L(14, '(ii) In your answer book, explain briefly one reason why the number of immigrants',
                  'risen since 2010.'),
     S(26, '(ii) · In your answer book', 'Total 30m'),
     (srp3('Brief explanation', 2, 'Brief explanation two SRP’s @ 3m each · 6m'),), '4-2', POP),
])
PART_TWO.append(T(
    'p2-10b', P2, '10B', '', 30, 14, L(14, 'Development of Urban Settlements'),
    (L(14, 'Examine the aerial photograph of Arklow accompanying this paper.'),
     L(14, 'Explain three reasons why the town of Arklow developed at this location', 'support each reason.')),
    (S(26, 'Three reasons @ 10m each', 'Total 30m'),),
    tuple(Criterion(f'Reason {n}', 10, sums((0, 1), steps(9, 3)), 'srp', TOWN_REASON) for n in (1, 2, 3)),
    '4-3', URB + AER, ID + 'p2-q10b', ('aerial',)))
Q10CI = L(14, '(i) Name one city in the developing world that is growing rapidly.')
PART_TWO += romans('10C', 14, L(14, 'Developing World City'), (), ID + 'p2-q10c', (), [
    ('(i)', 4, Q10CI, S(27, '(i) · Name one city', '(ii) · Explain one reason'),
     (fixed('Developing world city named', 4, 'Developing world city named · 4m'),), '4-5', URB),
    ('(ii)', 9, L(14, '(ii) Explain one reason for the rapid growth of the city named by you in part (i) above.'),
     S(27, '(ii) · Explain one reason', '(iii) Describe and explain'),
     (srp3('Explanation', 3, 'Explanation 3 SRP’s @3m each · 9m'),), '4-5', URB, (Q10CI,)),
    ('(iii)', 27, L(14, '(iii) Describe and explain any three problems associated with the rapid growth',
                    'developing world city.'),
     S(27, '(iii) Describe and explain', 'Total 40m'),
     (srp3('Description/explanation', 9, 'Description / explanation 9 SRP’s @3m each · 27m'),), '4-5', URB, (Q10CI,)),
])

PART_TWO.append(sketch(
    15, L(15, 'Aerial Photograph'),
    L(15, 'Examine the aerial photograph of Arklow accompanying this paper.', 'in the right background.'),
    28, ID + 'p2-q11a', '2-8', AER + URB, ('aerial',), 'landscape',
    ('The coastline', 'The river', 'A running track', 'A large car park in the centre middleground',
     'A housing estate in the right background')))
Q11BI = L(15, '(i) Name one urban area that you have studied.')
PART_TWO += romans('11B', 15, L(15, 'Urban Functions'), (), ID + 'p2-q11b', (), [
    ('(i)', 3, Q11BI, S(29, '(i) · Name one urban area', '(ii) · Name any two'),
     (fixed('Urban area named', 3, 'Urban area named · 3m'),), '4-3', URB),
    ('(ii)', 6, L(15, '(ii) Name any two functions of the urban area named by you in part (i) above.'),
     S(29, '(ii) · Name any two', '(iii) Describe and explain'),
     (fixed('Two functions', 6, 'Two valid functions named @ 3m each · 6m', (0, 3, 6)),), '4-3', URB, (Q11BI,)),
    ('(iii)', 21, L(15, '(iii) Describe and explain how the functions of this urban area have changed over time.'),
     S(29, '(iii) Describe and explain', 'Total 30m'),
     (srp3('Description/explanation', 7, 'Description / explanation 7 SRP’s @ 3m each · 21m'),), '4-3', URB,
     (Q11BI,)),
])
Q11CS = (L(15, 'Migration takes place due to push factors and pull factors.'),)
PART_TWO += romans('11C', 15, L(15, 'Migration – Ireland'), Q11CS, ID + 'p2-q11c', (), [
    ('(i)', 4, L(15, '(i) Name one push factor and one pull factor associated with migration in Ireland.'),
     S(29, '(i) · Name one push', '(ii) · Discuss the positive'),
     (fixed('Push factor named', 2, 'Valid push factor named · 2m'),
      fixed('Pull factor named', 2, 'Valid pull factor named · 2m')), '4-2', POP),
    ('(ii)', 18, L(15, '(ii) Discuss the positive impacts of migration on Ireland.'),
     S(29, '(ii) · Discuss the positive', '(iii) Discuss the negative'),
     (srp3('Discussion', 6, 'Discussion 6 SRP’s @ 3m each · 18m'),), '4-2', POP),
    ('(iii)', 18, L(15, '(iii) Discuss the negative impacts of migration on Ireland.'),
     S(29, '(iii) Discuss the negative', 'Total 40m'),
     (srp3('Discussion', 6, 'Discussion 6 SRP’s @ 3m each · 18m'),), '4-2', POP),
])

Q12AS = (L(16, 'Examine the table above showing the percentage distribution of journeys', 'following questions.'),)
PART_TWO += romans('12A', 16, L(16, 'Transport in Ireland'), Q12AS, ID + 'p2-q12a', ('page',), [
    ('(i)', 3, L(16, '(i) What percentage of journeys were made by car in 2014?'),
     S(30, '(i) · What percentage', '(ii) · What type'), (fixed('Percentage', 3, '75.3 (%) · 3m'),), '2-0', GRAPH),
    ('(ii)', 3, L(16, '(ii) What type of transport was used in the lowest percentage of journeys in 2016?'),
     S(30, '(ii) · What type', '(iii) · Calculate'), (fixed('Type of transport', 3, 'Bicycle · 3m'),), '2-0', GRAPH),
    ('(iii)', 6, L(16, '(iii) Calculate the total percentage of journeys made by car and public transport',
                   'in 2016.'),
     S(30, '(iii) · Calculate', '(iv) · Name two'), (fixed('Percentage', 6, '80.6 (%) · 6m'),), '2-0', GRAPH),
    ('(iv)', 6, L(16, '(iv) Name two examples of public transport available in cities such as Dublin.'),
     S(30, '(iv) · Name two', '(v) · List two'),
     (fixed('Two examples', 6, 'Two valid examples · 3m + 3m', (0, 3, 6)),), '4-5', URB),
    ('(v)', 6, L(16, '(v) List two ways authorities in urban areas attempt to reduce the amount of people',
                 'travelling by car.'),
     S(30, '(v) · List two', '(vi) · Explain briefly'),
     (fixed('Two ways', 6, 'Two valid ways · 3m + 3m', (0, 3, 6)),), '4-5', URB),
    ('(vi)', 6, L(16, '(vi) Explain briefly one problem that may be experienced in areas', 'journeys made by car.'),
     S(30, '(vi) · Explain briefly', 'Total 30m'),
     (srp3('Brief explanation', 2, 'One brief explanation two SRP’s @ 3m each · 6m'),), '4-5', URB),
])
Q12BI = L(16, '(i) Name one city where urban sprawl has occurred.')
PART_TWO += romans('12B', 16, L(16, 'Urban Sprawl'), (), ID + 'p2-q12b', (), [
    ('(i)', 3, Q12BI, S(30, '(i) · Name one city', '(ii) · Explain the reasons'),
     (fixed('City named', 3, 'City named · 3m'),), '4-5', URB),
    ('(ii)', 18, L(16, '(ii) Explain the reasons why urban sprawl has occurred in this city.'),
     S(30, '(ii) · Explain the reasons', '(iii) Describe one solution'),
     (srp3('Explanation', 6, 'Explanation 6 SRP’s @ 3m each · 18m'),), '4-5', URB, (Q12BI,)),
    ('(iii)', 9, L(16, '(iii) Describe one solution to urban sprawl.'),
     S(30, '(iii) Describe one solution', 'Total 30m', after='12B.'),
     (srp3('Description', 3, 'Description 3 SRP’s @ 3m each · 9m'),), '4-5', URB),
])
Q12CS = (L(16, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper and',
           'following questions.'),)
PART_TWO += romans('12C', 16, L(16, 'Settlement Distribution'), Q12CS, ID + 'p2-q12c', ('map', 'legend'), [
    ('(i)', 2, L(16, '(i) Give a grid reference for an area on the map where there is an absence of settlement.'),
     S(31, '(i) · Give a grid reference', '(ii) · Explain in detail'),
     (fixed('Grid reference', 2, 'Valid grid reference · 2m graded (2/1/0)', (0, 1, 2)),), '4-3', URB + MAP),
    ('(ii)', 18, L(16, '(ii) Explain in detail, using evidence from the map, why there is an absence of settlement',
                   'at this location.'),
     S(31, '(ii) · Explain in detail', '(iii) Give a grid'),
     (fixed('Map evidence', 3, 'Map evidence · 3m'), srp3('Explanation', 5, 'Explanation 5 SRP’s @ 3m each · 15m')),
     '4-3', URB + MAP),
    ('(iii)', 2, L(16, '(iii) Give a grid reference for an area on the map which has a relatively high density',
                   'settlement.'),
     S(31, '(iii) Give a grid', '(iv) Explain in detail'),
     (fixed('Grid reference', 2, 'Valid grid reference · 2m graded (2/1/0)', (0, 1, 2)),), '4-3', URB + MAP),
    ('(iv)', 18, L(16, '(iv) Explain in detail, using evidence from the map, why there is a relatively high',
                   'settlement at this location.'),
     S(31, '(iv) Explain in detail', 'Total 40m'),
     (fixed('Map evidence', 3, 'Map evidence · 3m'), srp3('Explanation', 5, 'Explanation 5 SRP’s @ 3m each · 15m')),
     '4-3', URB + MAP),
])

TASKS = [*PART_ONE, *PART_TWO]

ID_CORRECTION_REASON = 'No 2020 Ordinary card shipped before this review; every card is new.'

# No 2020 Ordinary card was live on origin/main before this review.
LEGACY_IDS: list[str] = []
