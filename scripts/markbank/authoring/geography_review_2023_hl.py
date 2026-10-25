"""Independent review ledger: Leaving Certificate Geography 2023 Higher Level.

Sources (English editions, Paper Trail index; sizes and SHA-256 pinned in
EXPECTED_SOURCES and the generated audit): Part One and Answerbook
LC005ALP042EV (48 pages), Part Two LC005ALP043EV (20 pages), marking scheme
LC005ALP000EV (64 pages), and the common companions in the harvested corpus —
the 1:50 000 Cavan map LC005CLP003EV, its legend LC005CLPC00EV and the Cavan
aerial photograph LC005CLP004EV, which the SEC publishes only as a JPEG.

Visual sweep (every page rendered and read on 2026-10-12):
  Part One booklet p1 cover; p2 instructions (Part One "Attempt any TEN",
  80 marks; Part Two "attempt FOUR", 320 marks); p3-p13 Questions 1-12 (p9
  holds Q7 and Q8); p14 Part Two answerbook instructions; p15-p18 graph
  paper; p19-p47 lined answer pages; p48 back.
  Part Two booklet p1 cover; p2 Part Two instructions; p3-p9 Sections 1-2
  (Q1-Q6); p10 Section 3 divider; p11-p16 Electives (Q7-Q12); p17 Section 4
  divider and note; p18-p19 Options (Q13-Q24); p20 copyright and back.
  Scheme p1 cover; p2-p3 notes and annotation key; p4 Part One table (two
  columns: Q1-Q6, Q7-Q12); p5 the 2023 Part Two adjustment rule; p6-p24
  Q1-Q6 (2A's answers and 2B route (i) on p10, route (ii) on p11); p25
  divider; p26-p43 Q7-Q12 (9A(ii) and 9B on p33); p44 divider; p45 option
  outline and Overall Coherence descriptors; p46 option annotations; p47-p54
  Q13-Q24; p55-p58 Geographical Investigation (coursework); p59
  investigation topics; p60 Irish-language bonus marks; p61-p63 blank; p64
  back cover.
  Companions: Cavan map extract (Lisnananagh Lough, the Stradone River,
  Fleming's Folly); OS legend sheet; oblique aerial photograph of Cavan
  (cathedral, lake in the right foreground, waste ground in the centre
  foreground).

Companions. Part One Q1 and Q7 (map, legend), Q8 (aerial, map and legend),
Q9 (aerial and the printed Street View images); Part Two 1A, 8C and 12B
(map, legend), 7A and 10A (aerial) were held back before this review because
their companions were not wired. Each now carries the exact official
documents it names.

Boundaries and tariffs follow the 2024 Higher ledger: every part the scheme
prices separately is a task; a matching table under one printed instruction
is one task with a criterion per scheme row, the scheme listing its answers
in the printed row order: Q1 H 50 05 Confluence, H 39 01 Drumlin, H 45 01
Concave slope; Q2 Layers of lava and volcanic ash=C, Crater=F, Secondary
vent=D, Magma chamber=B, Main vent=A, Volcanic bomb=E; Q3 Lagoon=C, Sand
dunes=A, Sea arch=D, Sand spit=B, then Deposition, Deposition, Erosion,
Deposition; Q4 Crystallisation of magma=3, Weathering and erosion=1,
Compaction and cementation=2; Q5 Convection currents=C, Inner core=E, Outer
core=B, Nazca plate=F, Volcanic island=A, Divergent plate boundary=D; Q6
Urban=London, Peripheral=West of Ireland, Climatic=Cool Temperate Oceanic,
Geomorphological=North European Plain, Administrative=Co. Meath, Region of
industrial decline=Sambre Meuse Valley. Q6(ii) prints two statements the
scheme prices 1 mark each, so (a) and (b) are tasks, as in 2024 and 2025.
"""

import itertools

from geography_review import (
    Criterion, Lift, Route, SchemeSlice, Task, pool, evens, fixed, slug, srp, sums, upto,
)

YEAR = 2023
LEVEL = 'higher'
PAPER_PAGES = {1: 48, 2: 20}
SCHEME_PAGES = 64
QUESTION_TARIFFS = {1: {str(n): 8 for n in range(1, 13)},
                    2: {**{f'{n}{x}': (20 if x == 'A' else 30)
                           for n in range(1, 13) for x in 'ABC'},
                        **{str(n): 80 for n in range(13, 25)}}}

EXPECTED_SOURCES = {
    'paper1': ('LC005ALP042EV.pdf', 2451953),
    'paper2': ('LC005ALP043EV.pdf', 1618833),
    'scheme': ('LC005ALP000EV.pdf', 1304649),
    'map': ('LC005CLP003EV.pdf', 4959287),
    'legend': ('LC005CLPC00EV.pdf', 836095),
    'aerial': ('LC005CLP004EV.jpg', 5597283),
}

PAGE_REVIEW = {
    'paper1': {1: 'cover', 2: 'instructions', **{p: 'question' for p in range(3, 14)},
               14: 'answerbook instructions', **{p: 'graph-paper answer page' for p in range(15, 19)},
               **{p: 'lined answer page' for p in range(19, 48)}, 48: 'copyright/back cover'},
    'paper2': {1: 'cover', 2: 'Part Two instructions',
               **{p: 'question' for p in (3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 18, 19)},
               10: 'section divider', 17: 'section divider and option note',
               20: 'copyright/back cover'},
    'scheme': {1: 'cover', 2: 'notes', 3: 'notes and annotation key', 4: 'Part One table',
               5: 'Part Two adjustment rule (2023 additional choice)',
               **{p: 'Part Two allocation' for p in range(6, 25)}, 25: 'section divider',
               **{p: 'Part Two allocation' for p in range(26, 44)}, 44: 'section divider',
               45: 'option outline and coherence descriptors', 46: 'option annotations',
               **{p: 'option allocation' for p in range(47, 55)},
               **{p: 'geographical investigation (coursework)' for p in range(55, 59)},
               59: 'investigation topics', 60: 'Irish-language bonus marks',
               61: 'blank', 62: 'blank', 63: 'blank', 64: 'back cover'},
}

EXPECTED_SELECTION_SCAN = [
    [1, 2, 'attempt any ten'], [1, 2, 'attempt four'], [1, 3, 'attempt any ten'],
    [2, 2, 'attempt four'],
    [2, 5, 'answer (i) or (ii)'], [2, 5, 'or one'], [2, 5, 'or one'],
    [2, 5, 'one of the following'],
    [2, 6, 'any one'], [2, 6, 'one of the following'],
    [2, 7, 'two of the following'],
    [2, 8, 'any two'],
    [2, 9, 'any two'],
    [2, 12, 'one of the following'],
    [2, 14, 'any two'],
    [2, 15, 'any one'],
    [2, 18, 'any two'], [2, 18, 'any three'], [2, 18, 'any one'],
]
SELECTION_REVIEW = [
    {'scan': [[1, 2, 'attempt any ten'], [1, 2, 'attempt four'], [1, 3, 'attempt any ten'],
              [2, 2, 'attempt four']],
     'kind': 'exam-attempt-rule',
     'reason': 'Part One any ten of twelve and Part Two four questions are attempt rules; every question is carded.'},
    {'scan': [[2, 5, 'answer (i) or (ii)'], [2, 5, 'or one'], [2, 5, 'or one']], 'kind': 'closed-route',
     'reason': '2B: (i) or (ii); (i) offers one fluvial OR one coastal OR one glacial landform -> 4 routes.'},
    {'scan': [[2, 5, 'one of the following']], 'kind': 'closed-choose-one',
     'reason': '2C one of two printed karst landscapes (surface, underground) -> 2 routes.'},
    {'scan': [[2, 6, 'any one'], [2, 6, 'one of the following']], 'kind': 'closed-choose-one',
     'reason': '3B any one of three printed distributions -> 3 routes; 3C one of four printed interactions -> 4 routes.'},
    {'scan': [[2, 12, 'one of the following'], [2, 15, 'any one']], 'kind': 'closed-choose-one',
     'reason': '8B one of three printed activities -> 3 routes; 11B any one of three printed factors -> 3 routes.'},
    {'scan': [[2, 7, 'two of the following'], [2, 9, 'any two'], [2, 14, 'any two'],
              [2, 18, 'any two'], [2, 18, 'any three']],
     'kind': 'choose-n-one-card',
     'reason': '4C two of three printed factors, 6B any two of four printed factors, 10B any two of three '
               'printed issues, 13 any two of three printed themes and 16 any three of four printed '
               'processes -> one card each with every printed item (choice is not a route; the scheme '
               'marks each chosen item alike).'},
    {'scan': [[2, 8, 'any two'], [2, 18, 'any one']], 'kind': 'open-response',
     'reason': '5B "any two factors" and 18 "any one soil type" print no list, so they are open choices. '
               'Open choices are not fanned out: "one urban area", "one multinational company", '
               '"example(s)", "one developing world city". Compulsory lists stay whole: 1A, 4A, 7A and 10A '
               'each bullet, 15 each of three printed themes, 1C fluvial and/or coastal.'},
]

P1, P2 = 1, 2
LEFT = (0.0, 0.0, 0.5, 1.0)
RIGHT = (0.5, 0.0, 1.0, 1.0)
ID = 'geography-2023-hl-'
H = 'geography-higher-'
SRPS = 'SRP’s'


def L(page, start, end=None, nth=None):
    return Lift(page, start, end, None, nth)


def S(page, start, end=None, clip=None, after=None, table=False):
    return SchemeSlice(page, start, end, clip, after, table)


def T(key, part, q, sub, marks, page, title, prompt, scheme, criteria, topic, atlas, card_id,
      legacy, sources=(), stem=(), routes=(), row_labels=(), absorbs=()):
    return Task(key, part, q, sub, marks, page, title, prompt, scheme, criteria, topic, atlas,
                sources, card_id, legacy, stem=stem, routes=routes, row_labels=row_labels,
                absorbs=absorbs)


def rows(lines, marks=1):
    return tuple(fixed(f'Row {i}', marks, line) for i, line in enumerate(lines, 1))


def pair(line, label):
    return fixed(label, 4, line, (0, 2, 4))


def one_plus_one(line, label):
    return fixed(label, 2, line, (0, 1, 2))


def p1_romans(q, page, title, stem, first_id, first_legacy, sources, parts):
    """Part One romans. parts: (sub, marks, prompt, scheme slice, criteria, topic, atlas)."""
    out = []
    for index, (sub, marks, prompt, scheme, criteria, topic, atlas) in enumerate(parts):
        key = sub.strip('()').replace(')(', '-').replace(') (', '-')
        out.append(T(f'p1-{q}-{key}', P1, q, sub, marks, page, title,
                     prompt if isinstance(prompt, tuple) else (prompt,), (scheme,), criteria,
                     topic, atlas, first_id if index == 0 else f'{first_id}-{key}',
                     first_legacy and index == 0, sources, stem))
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

Q1S = (L(3, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper.'),)
PART_ONE = [
    T('p1-1-i', P1, '1', '(i)', 6, 3, L(3, 'Landscape Identification'),
      (L(3, '(i) In the table below, match each of the following landscape features', 'Confluence.'),),
      (S(4, 'Q.1 (i) Confluence 2m', '(ii) Valid lake', LEFT),),
      rows(['Q.1 (i) Confluence 2m', 'Drumlin 2m', 'Concave slope 2m'], 2),
      '2-6', MAP + RIVERS + GLAC, ID + 'p1-q1', False, ('map', 'legend'), Q1S,
      row_labels=(L(3, 'H 50 05'), L(3, 'H 39 01'), L(3, 'H 45 01'))),
    T('p1-1-ii', P1, '1', '(ii)', 2, 3, L(3, 'Landscape Identification'),
      (L(3, '(ii) Name two lakes found on the map that are north of Northing 03.'),),
      (S(4, '(ii) Valid lake 1+1m', 'Q.2', LEFT),), (one_plus_one('(ii) Valid lake 1+1m', 'Two lakes'),),
      '2-6', MAP, ID + 'p1-q1-ii', False, ('map', 'legend'), Q1S),
]

Q2S = (L(4, 'Examine the diagram of an erupting volcano above', 'questions.'),)
PART_ONE += [
    T('p1-2-i', P1, '2', '(i)', 6, 4, L(4, 'Volcanic Activity'),
      (L(4, '(i) Match each of the letters A, B, C, D, E and F', 'table below.'),),
      (S(4, 'Q.2 (i) C 1m', '(ii) Valid feature', LEFT),),
      rows(['Q.2 (i) C 1m', 'F 1m', 'D 1m', 'B 1m', 'A 1m', 'E 1m']),
      '0-7', EV, ID + 'p1-q2', True, ('page',), Q2S,
      row_labels=(L(4, 'Layers of lava and volcanic ash'), L(4, 'Crater'), L(4, 'Secondary vent'),
                  L(4, 'Magma chamber'), L(4, 'Main vent'), L(4, 'Volcanic bomb'))),
    T('p1-2-ii', P1, '2', '(ii)', 2, 4, L(4, 'Volcanic Activity'),
      (L(4, '(ii) Name two plutonic features that form when magma cools.'),),
      (S(4, '(ii) Valid feature 1+1m', 'Q.3', LEFT),),
      (one_plus_one('(ii) Valid feature 1+1m', 'Two plutonic features'),),
      '0-7', EV, ID + 'p1-q2-ii', False, ('page',), Q2S),
]

Q3S = (L(5, 'Examine the photographs above and answer each of the following questions.'),)
Q3_ROWS = (L(5, 'Lagoon'), L(5, 'Sand dunes'), L(5, 'Sea arch'), L(5, 'Sand spit'))
PART_ONE += [
    T('p1-3-i', P1, '3', '(i)', 4, 5, L(5, 'Coastal Landscape'),
      (L(5, '(i) Match each of the photographs A, B, C and D', 'in the table below.'),),
      (S(4, 'Q.3 (i) C 1m', '(ii) Deposition', LEFT),), rows(['Q.3 (i) C 1m', 'A 1m', 'D 1m', 'B 1m']),
      '0-10', SEA, ID + 'p1-q3', True, ('page',), Q3S, row_labels=Q3_ROWS),
    T('p1-3-ii', P1, '3', '(ii)', 4, 5, L(5, 'Coastal Landscape'),
      (L(5, '(ii) Indicate, by ticking the correct box', 'process of deposition.'),),
      (S(4, '(ii) Deposition 1m', 'Q.4', LEFT),),
      rows(['(ii) Deposition 1m', '=Deposition 1m@0', 'Erosion 1m', '=Deposition 1m@1']),
      '0-10', SEA, ID + 'p1-q3-ii', False, ('page',), Q3S, row_labels=Q3_ROWS),
]

Q4S = (L(6, 'Examine the diagram of the rock cycle above and answer each of the following questions.'),)
PART_ONE += [
    T('p1-4-i', P1, '4', '(i)', 6, 6, L(6, 'Rocks'),
      (L(6, '(i) Match each of the numbers on the diagram', 'the table below.'),),
      (S(4, 'Q.4 (i) 3 2m', '(ii) Valid sedimentary', LEFT),), rows(['Q.4 (i) 3 2m', '=1 2m', '=2 2m'], 2),
      '0-1', RW, ID + 'p1-q4', True, ('page',), Q4S,
      row_labels=(L(6, 'Crystallisation of magma'), L(6, 'Weathering and erosion'),
                  L(6, 'Compaction and cementation'))),
    T('p1-4-ii', P1, '4', '(ii)', 2, 6, L(6, 'Rocks'),
      (L(6, '(ii) Name one example of a sedimentary rock and one example of a metamorphic rock.'),),
      (S(4, '(ii) Valid sedimentary rock 1m', 'Q.5', LEFT),),
      (fixed('Sedimentary rock', 1, '(ii) Valid sedimentary rock 1m'),
       fixed('Metamorphic rock', 1, 'Valid metamorphic rock 1m')),
      '0-1', RW, ID + 'p1-q4-ii', False, ('page',), Q4S),
]

Q5S = (L(7, 'Examine the diagram of the earth above and answer each of the following questions.'),)
PART_ONE += [
    T('p1-5-i', P1, '5', '(i)', 6, 7, L(7, 'Plate Tectonics'),
      (L(7, '(i) Match each of the letters A, B, C, D, E and F', 'table below.'),),
      (S(4, 'Q.5 (i) C 1m', '(ii) Lithosphere', LEFT),), rows(['Q.5 (i) C 1m', 'E 1m', 'B 1m', 'F 1m', 'A 1m', 'D 1m']),
      '0-0', PS, ID + 'p1-q5', True, ('page',), Q5S,
      row_labels=(L(7, 'Convection currents'), L(7, 'Inner core'), L(7, 'Outer core'), L(7, 'Nazca plate'),
                  L(7, 'Volcanic island'), L(7, 'Divergent plate boundary'))),
    T('p1-5-ii', P1, '5', '(ii)', 2, 7, L(7, 'Plate Tectonics'),
      (L(7, '(ii) What is the name for the solid layer of rock', 'and the crust?'),),
      (S(4, '(ii) Lithosphere 2m', 'Q.6', LEFT),), (fixed('Layer', 2, '(ii) Lithosphere 2m'),),
      '0-0', PS, ID + 'p1-q5-ii', False, ('page',), Q5S),
]

TF6 = L(8, '(ii) Indicate whether each of the following statements is true or false', 'correct box.')
REGIONS = IRL + EURO
PART_ONE += [
    T('p1-6-i', P1, '6', '(i)', 6, 8, L(8, 'Concept of a Region'),
      (L(8, '(i) Complete the table below by matching each of the examples of regions', 'in the table.'),
       L(8, 'Examples of Regions:'), L(8, 'West of Ireland'), L(8, 'North European Plain'),
       L(8, 'Cool Temperate Oceanic region'), L(8, 'London'), L(8, 'Sambre Meuse Valley'),
       L(8, 'County Meath')),
      (S(4, 'Q.6 (i) London 1m', '(ii) (a) True', LEFT),),
      rows(['Q.6 (i) London 1m', 'West of Ireland 1m', 'Cool Temperate Oceanic 1m', 'North European Plain 1m',
            'Co. Meath 1m', 'Sambre Meuse Valley 1m']),
      '1-0', REGIONS, ID + 'p1-q6', True, ('page',),
      row_labels=(L(8, 'Urban region'), L(8, 'Peripheral region', nth=0), L(8, 'Climatic region'),
                  L(8, 'Geomorphological region'), L(8, 'Administrative region'),
                  L(8, 'Region of industrial decline'))),
    T('p1-6-ii-a', P1, '6', '(ii)(a)', 1, 8, L(8, 'Concept of a Region'),
      (TF6, L(8, '(a) Core regions are usually well-developed', 'attract industry.')),
      (S(4, '(ii) (a) True 1m', '(b) False', LEFT),), (fixed('Statement (a)', 1, '(ii) (a) True 1m'),),
      '1-0', REGIONS, ID + 'p1-q6-ii-a', False, ('page',)),
    T('p1-6-ii-b', P1, '6', '(ii)(b)', 1, 8, L(8, 'Concept of a Region'),
      (TF6, L(8, '(b) Peripheral regions experience net immigration.')),
      (S(4, '(b) False 1m', 'Page 3', LEFT),), (fixed('Statement (b)', 1, '(b) False 1m'),),
      '1-0', REGIONS, ID + 'p1-q6-ii-b', False, ('page',)),
]

Q7S = (L(9, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper, and',
         'following questions.'),)
PART_ONE += p1_romans('7', 9, L(9, 'Map Skills'), Q7S, ID + 'p1-q7', False, ('map', 'legend'), [
    ('(i)', 2, L(9, '(i) What is the height (in metres) at the triangulation pillar at H 462 008?'),
     S(4, 'Q.7 (i) 320 (m)', '(ii) 2.5', RIGHT), (fixed('Height', 2, 'Q.7 (i) 320 (m) · 2m'),), '2-6', MAP),
    ('(ii)', 2, L(9, '(ii) Measure the straight-line distance', 'H 435 041.'),
     S(4, '(ii) 2.5 (km) 2m', '(iii) N 510', RIGHT), (fixed('Distance', 2, '(ii) 2.5 (km) 2m'),), '2-6', MAP),
    ('(iii)', 2, L(9, '(iii) Give a six-figure grid reference for the exact point', 'in the southeast.'),
     S(4, '(iii) N 510 994 2m', '(iv) 96', RIGHT), (fixed('Grid reference', 2, '(iii) N 510 994 2m'),), '2-6', MAP),
    ('(iv)', 2, L(9, '(iv) Calculate the area (in km2) of the map extract which is north of Northing 00.'),
     S(4, '(iv) 96 (km²) 2m', 'Q.8', RIGHT), (fixed('Area', 2, '(iv) 96 (km²) 2m'),), '2-6', MAP),
])

Q8S = (L(9, 'Examine the aerial photograph of Cavan and the 1:50 000 Ordnance Survey map',
         'following questions.'),)
PART_ONE += p1_romans('8', 9, L(9, 'Aerial Photograph and Ordnance Survey Map'), Q8S, ID + 'p1-q8', False,
                      ('aerial', 'map', 'legend'), [
    ('(i)', 2, L(9, '(i) In what direction was the camera pointed when the aerial photograph was taken?'),
     S(4, 'Q.8 (i) North west 2m', '(ii) H 42 04', RIGHT), (fixed('Direction', 2, 'Q.8 (i) North west 2m'),),
     '2-8', AER + MAP),
    ('(ii)', 2, L(9, '(ii) Give a four-figure grid reference for the lake', 'aerial photograph.'),
     S(4, '(ii) H 42 04 2m', '(iii) R 198', RIGHT), (fixed('Grid reference', 2, '(ii) H 42 04 2m'),),
     '2-8', AER + MAP),
    ('(iii)', 2, (L(9, '(iii) Which of the following regional roads', 'Tick (✓) the correct box.'),
                  L(9, 'R 212'), L(9, 'R 188'), L(9, 'R 198'), L(9, 'R 165')),
     S(4, '(iii) R 198 2m', '(iv) Oblique', RIGHT), (fixed('Regional road', 2, '(iii) R 198 2m'),),
     '2-8', AER + MAP),
    ('(iv)', 2, L(9, '(iv) State the type of aerial photography used', 'this paper.'),
     S(4, '(iv) Oblique 2m', 'Q.9', RIGHT), (fixed('Type of aerial photography', 2, '(iv) Oblique 2m'),),
     '2-8', AER),
])

PART_ONE.append(T(
    'p1-9', P1, '9', '', 8, 10, L(10, 'Aerial Photograph', nth=0),
    (L(10, 'Using accepted notation, give the location on the aerial photograph', 'in the table below.'),),
    (S(4, 'A Left Middleground 2m', 'Q10', RIGHT),),
    (fixed('A', 2, 'A Left Middleground 2m'), fixed('B', 2, 'B Left Foreground 2m'),
     fixed('C', 2, 'C Centre Foreground 2m'), fixed('D', 2, 'D Centre Middleground 2m')),
    '2-8', AER, ID + 'p1-q9', False, ('page', 'aerial'),
    (L(10, 'Examine the aerial photograph of Cavan accompanying this paper and the Google Street',
       'same area of Cavan.'),)))

Q10S = (L(11, 'Examine the weather chart above', 'following questions.'),)
PART_ONE += p1_romans('10', 11, L(11, 'Weather'), Q10S, ID + 'p1-q10', True, ('page',), [
    ('(i)', 2, (L(11, '(i) Which of the following types of front is labelled X', 'Tick (✓) the correct box.'),
                L(11, 'Warm front'), L(11, 'Cold front'), L(11, 'Occluded front')),
     S(4, '(i) Occluded front 2m', '(ii) 1024', RIGHT), (fixed('Front', 2, '(i) Occluded front 2m'),), '2-7', WX),
    ('(ii)', 2, L(11, '(ii) What is the barometric pressure', 'on the weather chart?'),
     S(4, '(ii) 1024(mb) 2m', '(iii) True', RIGHT), (fixed('Pressure', 2, '(ii) 1024(mb) 2m'),), '2-7', WX),
    ('(iii)', 2, (L(11, '(iii) Indicate whether the following statement is true or false', 'correct box.'),
                  L(11, 'Winds over the area marked X are stronger', 'marked Y.')),
     S(4, '(iii) True 2m', '(iv) Prevailing', RIGHT), (fixed('True or false', 2, '(iii) True 2m'),), '2-7', WX),
    ('(iv)', 2, L(11, '(iv) What is the term used to describe the wind', 'over an area?'),
     S(4, '(iv) Prevailing 2m', 'Q11', RIGHT), (fixed('Term', 2, '(iv) Prevailing 2m'),), '2-7', WX),
])

Q11S = (L(12, 'Examine the table above showing information on towns', 'following questions.'),)
PART_ONE += p1_romans('11', 12, L(12, 'Statistical Interpretation'), Q11S, ID + 'p1-q11', True, ('page',), [
    ('(i)', 2, L(12, '(i) Which town from the table above is in Co. Galway?'),
     S(4, '(i) An Cheathrú Rua', '(ii) 53', RIGHT), (fixed('Town', 2, '(i) An Cheathrú Rua · 2m'),), '2-0', TG),
    ('(ii)', 2, L(12, '(ii) What was the percentage of daily Irish speakers in An Bun Beag-Doirí Beaga?'),
     S(4, '(ii) 53 (%)', '(iii) Rann', RIGHT), (fixed('Percentage', 2, '(ii) 53 (%) · 2m'),), '2-0', TG),
    ('(iii)', 2, L(12, '(iii) Which town from the table above had the lowest number of people in 2016?'),
     S(4, '(iii) Rann na Feirste 2m', '(iv) 292', RIGHT), (fixed('Town', 2, '(iii) Rann na Feirste 2m'),), '2-0', TG),
    ('(iv)', 2, L(12, '(iv) Calculate X the number of people living in Mín Lárach', 'speakers.'),
     S(4, '(iv) 292 2m', 'Q12', RIGHT), (fixed('Calculation', 2, '(iv) 292 2m'),), '2-0', TG),
])

Q12S = (L(13, 'Examine the infographic above on preliminary results of Census 2022', 'following questions.'),)
PART_ONE += p1_romans('12', 13, L(13, 'Graphical Interpretation'), Q12S, ID + 'p1-q12', True, ('page',), [
    ('(i)', 2, L(13, '(i) How many homes in Ireland were vacant in 2022?'),
     S(4, '(i) 166,752 2m', '(ii) Dublin', RIGHT), (fixed('Vacant homes', 2, '(i) 166,752 2m'),), '2-0', TG),
    ('(ii)', 2, L(13, '(ii) Which county had the largest inward migration in 2022?'),
     S(4, '(ii) Dublin 2m', '(iii) 361,671', RIGHT), (fixed('County', 2, '(ii) Dublin 2m'),), '2-0', TG),
    ('(iii)', 2, L(13, '(iii) By how many people did the population of Ireland increase between 2016 and 2022?'),
     S(4, '(iii) 361,671 2m', '(iv) Valid ways', RIGHT), (fixed('Increase', 2, '(iii) 361,671 2m'),), '2-0', TG),
    ('(iv)', 2, L(13, '(iv) State two ways that census data can be used by governments.'),
     S(4, '(iv) Valid ways 1+1m', '3 of 59', RIGHT), (one_plus_one('(iv) Valid ways 1+1m', 'Two ways'),),
     '4-0', TG + POP),
])


# ---------------------------------------------------------------- Part Two --
def romans(q, page, title, stem, first_id, sources, parts, legacy_first=True):
    """A-part romans. parts: (sub, marks, prompt, scheme slices, criteria, topic, atlas)."""
    out = []
    for index, (sub, marks, prompt, scheme, criteria, topic, atlas) in enumerate(parts):
        roman = sub.strip('()')
        out.append(T(f'p2-{q.lower()}-{roman}', P2, q, sub, marks, page, title,
                     prompt if isinstance(prompt, tuple) else (prompt,), scheme,
                     criteria, topic, atlas, first_id if index == 0 else f'{first_id}-{roman}',
                     legacy_first and index == 0, sources, stem))
    return out


def sketch(outline_line, outline_permitted, alloc, item_permitted, labels):
    return (fixed('Sketch outline' if 'Sketch' in outline_line else 'Map outline', 4,
                  outline_line, outline_permitted),
            *(Criterion(f'Feature {n}', 4, item_permitted, 'exact', alloc) for n in range(1, labels + 1)))


OS_SKETCH = sketch('Sketch Outline · 4 marks (4/0)', (0, 4),
                   ('4 features @ 4 marks each', 'Label 1m'), sums((0, 1, 3), (0, 1)), 4)
AERIAL_SKETCH = sketch('Sketch Outline · 4 marks (4/0)', (0, 4),
                       ('4 features @ 4 marks each', 'Named 1 mark'), sums((0, 1, 3), (0, 1)), 4)
GRAPH = (fixed('Title', 2, ('Bar Chart · Pie Chart', 'Title · 2 marks · 2 marks')),
         fixed('Axes named (bar chart) / circle and centre (pie chart)', 2,
               ('Vertical axis named', 'Horizontal axis named'), (0, 1, 2)),
         fixed('6 items illustrated', 12, '6 items illustrated', upto(12)))


def chosen(items, k):
    return [(combo, ' + '.join(item.rstrip('.') for item in combo),
             '-'.join(slug(item, 34) for item in combo))
            for combo in itertools.combinations(items, k)]


def bullet_routes(prefix, items, k=1, atlas=None):
    return tuple(Route(route_slug, label, ID + prefix + route_slug, True, keep_bullets=combo,
                       atlas=(atlas[combo[0]] if atlas else None))
                 for combo, label, route_slug in chosen(items, k))


def split(label, total, first, second):
    """One allocation printed as two parts examined 8/7 and 7/8 (or 7/6 and 6/7) SRPs."""
    return srp(label, total, (first, second))


LANDFORMS = 'one fluvial landform or one coastal landform or one glacial landform'

PART_TWO = [
    T('p2-1a', P2, '1A', '', 20, 3, L(3, 'Ordnance Survey Map'),
      (L(3, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper.', 'above 300 metres.'),),
      (S(6, 'Sketch Outline', None),), OS_SKETCH, '2-6', MAP, ID + 'p2-q1a', False, ('map', 'legend'),
      row_labels=(None, L(3, 'The entire area of Lisnananagh Lough'),
                  L(3, 'The course of the Stradone River', 'H 505 056.'),
                  L(3, 'The triangulation pillar at Fleming’s Folly in the south west of the map'),
                  L(3, 'The entire area of land above 300 metres.'))),
    T('p2-1b', P2, '1B', '', 30, 3, L(3, 'Igneous Rocks'),
      (L(3, 'Explain the formation of two igneous rocks, with reference to Irish examples.'),),
      (S(7, 'Two Irish igneous rocks named', 'Annotation'),),
      (pair('Two Irish igneous rocks named · 2 + 2 marks', 'Two Irish igneous rocks named'),
       split('Explanation of formation of the two rocks (7/6 and 6/7 SRPs)', 13,
             f'Explanation of formation of rock 1 · 7/6 x {SRPS}',
             f'Explanation of formation of rock 2 · 6/7 x {SRPS}')),
      '0-1', RW, ID + 'p2-q1b', True),
    T('p2-1c', P2, '1C', '', 30, 3, L(3, 'Isostasy'),
      (L(3, 'Examine how isostasy has impacted on the Irish landscape', 'the coastal landscape.'),),
      (S(8, 'Impact / feature identified · 2 marks', 'Annotation'),),
      (fixed('Impact / feature identified', 2, 'Impact / feature identified · 2 marks'),
       srp('Examination', 14, 'Examination · 14 x SRPs')),
      '0-5', RIVERS + SEA, ID + 'p2-q1c', True),
]

Q2AS = (L(4, 'Examine the map and legend above which gives information on an earthquake in',
          'following questions.'),)
PART_TWO += romans('2A', 4, L(4, 'Earthquakes'), Q2AS, ID + 'p2-q2a', ('page',), [
    ('(i)', 2, L(4, '(i) What was the Modified Mercalli Scale Intensity (MMI)', 'this earthquake?'),
     (S(10, '(i) · 6.5 (MMI)', '(ii) · Valid settlement'),), (fixed('Intensity', 2, '(i) · 6.5 (MMI) · 2 marks'),),
     '0-7', EV),
    ('(ii)', 4, L(4, '(ii) Name two settlements that experienced an MMI of 5.0 or higher.'),
     (S(10, '(ii) · Valid settlement', '(iii) · Pakistan'),),
     (pair('(ii) · Valid settlement · 2 + 2 marks', 'Two settlements'),), '0-7', EV),
    ('(iii)', 2, L(4, '(iii) On Afghanistan’s border with which other country', 'take place?'),
     (S(10, '(iii) · Pakistan', '(iv) · Richter Scale'),), (fixed('Country', 2, '(iii) · Pakistan · 2 marks'),),
     '0-7', EV),
    ('(iv)', 2, L(4, '(iv) Other than the Modified Mercalli Scale, name one scale used to measure earthquakes.'),
     (S(10, '(iv) · Richter Scale', '(v) · Valid instrument'),), (fixed('Scale', 2, '(iv) · Richter Scale · 2 marks'),),
     '0-7', EV),
    ('(v)', 2, L(4, '(v) Name one instrument used to measure earthquakes.'),
     (S(10, '(v) · Valid instrument', '(vi) · Valid explanation'),),
     (fixed('Instrument', 2, '(v) · Valid instrument · 2 marks'),), '0-7', EV),
    ('(vi)', 4, L(4, '(vi) Explain briefly the term focus, in relation to earthquakes.'),
     (S(10, '(vi) · Valid explanation', '(vii) · Valid explanation'),),
     (pair('(vi) · Valid explanation · 2 + 2 marks', 'Explanation'),), '0-7', EV),
    ('(vii)', 4, L(4, '(vii) Explain briefly one way to reduce the effects of an earthquake.'),
     (S(10, '(vii) · Valid explanation', '2B.'),),
     (pair('(vii) · Valid explanation · 2 + 2 marks', 'Way to reduce the effects'),), '0-7', EV),
])

PART_TWO += [
    T('p2-2b', P2, '2B', '', 30, 5, L(5, 'Surface Processes'),
      (L(5, '(i) Examine the role of the process of deposition', 'that you have studied.'),),
      (S(10, 'Landform named · 2 marks', 'Annotation'),),
      (fixed('Landform named', 2, 'Landform named · 2 marks'), srp('Examination', 14, f'Examination · 14 x {SRPS}')),
      '0-9', RIVERS, ID + 'p2-q2b-route-i-fluvial-landform', True,
      routes=(
          Route('route-i-fluvial-landform', 'Route (i) · one fluvial landform', ID + 'p2-q2b-route-i-fluvial-landform',
                True, ((LANDFORMS, 'one fluvial landform'),), topic='0-9', atlas=RIVERS),
          Route('route-i-coastal-landform', 'Route (i) · one coastal landform', ID + 'p2-q2b-route-i-coastal-landform',
                True, ((LANDFORMS, 'one coastal landform'),), topic='0-10', atlas=SEA),
          Route('route-i-glacial-landform', 'Route (i) · one glacial landform', ID + 'p2-q2b-route-i-glacial-landform',
                True, ((LANDFORMS, 'one glacial landform'),), topic='0-11', atlas=GLAC),
          Route('route-ii', 'Route (ii)', ID + 'p2-q2b-route-ii', True,
                prompt=(L(5, '(ii) Describe and explain the factors governing', 'process that you have studied.'),),
                scheme=(S(11, 'Factors identified', 'Annotation'),),
                criteria=(pair('Factors identified · 2 + 2 marks', 'Factors identified'),
                          fixed('Mass movement process named', 2, 'Mass movement process named · 2 marks'),
                          srp('Description/explanation', 12, f'Description/explanation · 12 x {SRPS}')),
                topic='0-8', atlas=RW),
      )),
    T('p2-2c', P2, '2C', '', 30, 5, L(5, 'Chemical Weathering'),
      (L(5, 'Explain, with the aid of a labelled diagram(s), how chemical weathering', 'underground karst landscape.'),),
      (S(12, 'Labelled diagram · 2 marks', 'Annotation'),),
      (fixed('Labelled diagram', 2, 'Labelled diagram · 2 marks'), srp('Explanation', 14, f'Explanation · 14 x {SRPS}')),
      '0-3', KARST, ID + 'p2-q2c-the-surface-karst-landscape', True,
      routes=bullet_routes('p2-q2c-', ('The surface karst landscape', 'The underground karst landscape.'))),
]

Q3AS = (L(6, 'Examine the article above which gives information on a glacier avalanche', 'following questions.'),)
PART_TWO += romans('3A', 6, L(6, 'Mass Movement'), Q3AS, ID + 'p2-q3a', ('page',), [
    ('(i)', 2, L(6, '(i) In which country are the Dolomite Mountains located?'),
     (S(13, '(i) · Italy', '(ii) · 3,300'),), (fixed('Country', 2, '(i) · Italy · 2 marks'),), '0-8', RW),
    ('(ii)', 2, L(6, '(ii) What height (in metres) is the Marmolada mountain?'),
     (S(13, '(ii) · 3,300', '(iii) · 80'),), (fixed('Height', 2, '(ii) · 3,300(m) · 2 marks'),), '0-8', RW),
    ('(iii)', 2, L(6, '(iii) By what estimated percentage has the volume', 'last 72 years?'),
     (S(13, '(iii) · 80', '(iv) · Valid example'),), (fixed('Percentage', 2, '(iii) · 80(%) · 2 marks'),), '0-8', RW),
    ('(iv)', 2, L(6, '(iv) Name one example of a slow type of mass movement.'),
     (S(13, '(iv) · Valid example', '(v) · Valid explanation'),),
     (fixed('Example', 2, '(iv) · Valid example · 2 marks'),), '0-8', RW),
    ('(v)', 4, L(6, '(v) Explain briefly the term regolith.'),
     (S(13, '(v) · Valid explanation', '(vi) · Valid factors'),),
     (pair('(v) · Valid explanation · 2 + 2 marks', 'Explanation'),), '0-8', RW),
    ('(vi)', 4, L(6, '(vi) List two factors that influence the speed of mass movement.'),
     (S(13, '(vi) · Valid factors', '(vii) · Valid explanation'),),
     (pair('(vi) · Valid factors · 2 + 2 marks', 'Two factors'),), '0-8', RW),
    ('(vii)', 4, L(6, '(vii) Explain briefly how one of these factors influences the speed of mass movement.'),
     (S(13, '(vii) · Valid explanation', None),),
     (pair('(vii) · Valid explanation · 2 + 2 marks', 'Explanation'),), '0-8', RW),
])

PART_TWO += [
    T('p2-3b', P2, '3B', '', 30, 6, L(6, 'The Tectonic Cycle'),
      (L(6, 'Explain how the study of plate tectonics has helped us', 'Fold mountains'),),
      (S(14, 'Example · 2 + 2 marks', 'Annotation'),),
      (pair('Example · 2 + 2 marks', 'Examples'), srp('Explanation', 13, f'Explanation · 13 x {SRPS}')),
      '0-0', PS, ID + 'p2-q3b-earthquakes', True,
      routes=bullet_routes('p2-q3b-', ('Earthquakes', 'Volcanoes', 'Fold mountains'),
                           atlas={'Earthquakes': PS + EV, 'Volcanoes': PS + EV, 'Fold mountains': PS + RW})),
    T('p2-3c', P2, '3C', '', 30, 6, L(6, 'Human Interaction with the Rock Cycle'),
      (L(6, 'Examine how humans interact with the rock cycle', 'Geothermal energy production.'),),
      (S(15, f'Examination · 15 x {SRPS}', 'Annotation'),), (srp('Examination', 15, f'Examination · 15 x {SRPS}'),),
      '0-6', RW, ID + 'p2-q3c-mining', True,
      routes=bullet_routes('p2-q3c-', ('Mining', 'Extraction of building materials', 'Oil/gas exploitation',
                                       'Geothermal energy production.'))),
    # Question 4
    T('p2-4a', P2, '4A', '', 20, 7, L(7, 'Map Skills'),
      (L(7, 'Draw an outline map of a European region (not in Ireland) that you have studied.',
         'The course of a named river.'),),
      (S(16, 'Map outline', None),),
      sketch('Map outline · 4 marks graded (4/2/0)', (0, 2, 4),
             ('4 features @ 4 marks each', 'Named 2 marks'), sums((0, 1, 2), (0, 2)), 4),
      '1-5', EURO, ID + 'p2-q4a', True,
      row_labels=(None, L(7, 'The outline of a named feature of relief (upland or lowland)'),
                  L(7, 'A named urban centre'), L(7, 'The outline of a named agricultural or industrial region'),
                  L(7, 'The course of a named river.'))),
    T('p2-4b', P2, '4B', '', 30, 7, L(7, 'Tertiary Economic Activity – Continental / Sub-Continental Region'),
      (L(7, 'Account for the development of one tertiary economic activity in a', 'that you have studied.'),),
      (S(17, f'Examination · 15 x {SRPS}', 'Annotation'),), (srp('Examination', 15, f'Examination · 15 x {SRPS}'),),
      '1-6', CONT, ID + 'p2-q4b', True),
    T('p2-4c', P2, '4C', '', 30, 7, L(7, 'Urban Development'),
      (L(7, 'Examine how two of the following factors have influenced', 'Primary economic activity.'),),
      (S(18, 'Urban area named · 2 marks', 'Annotation'),),
      (fixed('Urban area named', 2, 'Urban area named · 2 marks'),
       fixed('Influence on development identified', 2, 'Influence on development identified · 2 marks'),
       split('Examination of the two factors (7/6 and 6/7 SRPs)', 13,
             f'Examination of factor 1 · 7/6 x {SRPS}', f'Examination of factor 2 · 6/7 x {SRPS}')),
      '1-3', IRL + EURO, *pool(ID + 'p2-q4c-', ('Transport', 'Location', 'Primary economic activity.'), 2)[:1],
      True, absorbs=pool(ID + 'p2-q4c-', ('Transport', 'Location', 'Primary economic activity.'), 2)[1]),
]

Q5AS = (L(8, 'Examine the table above showing the goods transported by air in Europe', 'following questions.'),)
ENV = (H + 'economic-environmental-impact',)
PART_TWO += romans('5A', 8, L(8, 'European Air Transport'), Q5AS, ID + 'p2-q5a', ('page',), [
    ('(i)', 2, L(8, '(i) Which country transported 242,000 tonnes', 'in 2018?'),
     (S(19, '(i) · Denmark', '(ii) · Portugal'),), (fixed('Country', 2, '(i) · Denmark · 2 marks'),), '2-0', TG),
    ('(ii)', 2, L(8, '(ii) Which country had the lowest amount', 'in 2015?'),
     (S(19, '(ii) · Portugal', '(iii) · France'),), (fixed('Country', 2, '(ii) · Portugal · 2 marks'),), '2-0', TG),
    ('(iii)', 2, L(8, '(iii) Name one country that had a decline', '2021.'),
     (S(19, '(iii) · France', '(iv) · 33.5'),), (fixed('Country', 2, '(iii) · France/Switzerland · 2 marks'),),
     '2-0', TG),
    ('(iv)', 4, L(8, '(iv) Calculate the percentage of EU 27 goods', 'accounted for by Germany.'),
     (S(19, '(iv) · 33.5', '(v) · Switzerland'),), (fixed('Calculation', 4, '(iv) · 33.5 (%) · 4 marks'),),
     '2-0', TG),
    ('(v)', 2, L(8, '(v) Which country from the table above is not a member of the EU?'),
     (S(19, '(v) · Switzerland', '(vi) · Valid explanation'),), (fixed('Country', 2, '(v) · Switzerland · 2 marks'),),
     '1-5', EURO),
    ('(vi)', 4, L(8, '(vi) Explain briefly one advantage of transporting goods by air.'),
     (S(19, '(vi) · Valid explanation', '(vii) · Valid explanation'),),
     (pair('(vi) · Valid explanation · 2 + 2 marks', 'Advantage'),), '1-5', EURO),
    ('(vii)', 4, L(8, '(vii) Explain briefly one environmental challenge caused by air transport.'),
     (S(19, '(vii) · Valid explanation', None),),
     (pair('(vii) · Valid explanation · 2 + 2 marks', 'Environmental challenge'),), '3-4', ENV),
])

PART_TWO += [
    T('p2-5b', P2, '5B', '', 30, 8, L(8, 'Primary Economic Activity'),
      (L(8, 'Explain any two factors that have influenced the development of one primary economic',
         'that you have studied.'),),
      (S(20, 'Factors identified · 2 + 2 marks', 'Annotation'),),
      (pair('Factors identified · 2 + 2 marks', 'Factors identified'),
       split('Explanation of the two factors (7/6 and 6/7 SRPs)', 13,
             f'Explanation of Factor 1 · 7/6 x {SRPS}', f'Explanation of Factor 2 · 6/7 x {SRPS}')),
      '1-4', IRL, ID + 'p2-q5b', True),
    T('p2-5c', P2, '5C', '', 30, 8, L(8, 'The European Union'),
      (L(8, 'Discuss the potential challenges facing the future development', 'and sovereignty.'),),
      (S(21, 'Potential challenges identified', 'Annotation'),),
      (pair('Potential challenges identified · 2 + 2 marks', 'Potential challenges identified'),
       srp('Discussion', 13, f'Discussion · 13 x {SRPS}')),
      '1-5', EURO, ID + 'p2-q5c', True),
]

Q6AS = (L(9, 'Examine the clustered bar chart above showing the male and female unemployment rates in',
          'following questions.'),)
PART_TWO += romans('6A', 9, L(9, 'Irish Unemployment'), Q6AS, ID + 'p2-q6a', ('page',), [
    ('(i)', 2, L(9, '(i) What was the female unemployment rate (%) for March 2021?'),
     (S(22, '(i) · 7.8', '(ii) · August'),), (fixed('Rate', 2, '(i) · 7.8 (%) · 2 marks'),), '2-0', TG),
    ('(ii)', 2, L(9, '(ii) In which month were the male and female unemployment rates the same?'),
     (S(22, '(ii) · August', '(iii) · Three'),), (fixed('Month', 2, '(ii) · August · 2 marks'),), '2-0', TG),
    ('(iii)', 2, L(9, '(iii) For how many months was the female unemployment rate higher', 'unemployment rate?'),
     (S(22, '(iii) · Three', '(iv) · Decreasing'),), (fixed('Months', 2, '(iii) · Three · 2 marks'),), '2-0', TG),
    ('(iv)', 2, L(9, '(iv) Was the unemployment rate for males increasing or decreasing', 'September?'),
     (S(22, '(iv) · Decreasing', '(v) · 6.5'),), (fixed('Trend', 2, '(iv) · Decreasing · 2 marks'),), '2-0', TG),
    ('(v)', 4, L(9, '(v) Calculate the average unemployment rate (%) for females', 'the chart above.'),
     (S(22, '(v) · 6.5', '(vi) · Valid explanation'),), (fixed('Average', 4, '(v) · 6.5 (%) · 4 marks'),),
     '2-0', TG),
    ('(vi)', 8, L(9, '(vi) Explain briefly two benefits of having a low unemployment rate.'),
     (S(22, '(vi) · Valid explanation', None),),
     (pair('(vi) · Valid explanation · 2 + 2 marks', 'First benefit'), pair('=2 + 2 marks', 'Second benefit')),
     '1-4', IRL),
])

PART_TWO += [
    T('p2-6b', P2, '6B', '', 30, 9, L(9, 'Secondary Economic Activity'),
      (L(9, 'Account for the development of secondary economic activity in a European region', 'Markets.'),),
      (S(23, 'Examination of Factor 1', 'Annotation'),),
      (split('Examination of the two factors (8/7 and 7/8 SRPs)', 15,
             f'Examination of Factor 1 · 8/7 x {SRPS}', f'Examination of Factor 2 · 7/8 x {SRPS}'),),
      '1-5', EURO, *pool(ID + 'p2-q6b-', ('Labour', 'Transport', 'Raw materials', 'Markets.'), 2)[:1], True,
      absorbs=pool(ID + 'p2-q6b-', ('Labour', 'Transport', 'Raw materials', 'Markets.'), 2)[1]),
    T('p2-6c', P2, '6C', '', 30, 9, L(9, 'Population in Ireland'),
      (L(9, 'Account for the distribution of population throughout an Irish region that you have studied.'),),
      (S(24, f'Examination · 15 x {SRPS}', 'Annotation'),), (srp('Examination', 15, f'Examination · 15 x {SRPS}'),),
      '1-4', IRL + POP, ID + 'p2-q6c', True),
]

ECON = (H + 'elective-economic',)
DEV = (H + 'economic-developing-economies',)
MNC = (H + 'economic-multinationals-globalisation',)
EU_TRADE = (H + 'economic-european-union',)
ENERGY = (H + 'economic-energy',)
FACTOR = ('Three factors @ 10 marks each', 'For each factor:', 'Factor named · 2 marks',
          'OS map evidence · 2 marks', f'Explanation · 3 x {SRPS}')
PART_TWO += [
    # Question 7
    T('p2-7a', P2, '7A', '', 20, 11, L(11, 'Aerial Photograph'),
      (L(11, 'Examine the aerial photograph accompanying this paper.', 'Industrial buildings in the left background'),),
      (S(26, 'Sketch Outline', None),), AERIAL_SKETCH, '2-8', AER, ID + 'p2-q7a', False, ('aerial',),
      row_labels=(None, L(11, 'The lake'), L(11, 'Two connecting streets'),
                  L(11, 'An area of waste ground in the centre foreground.'),
                  L(11, 'Industrial buildings in the left background'))),
    T('p2-7b', P2, '7B', '', 30, 11, L(11, 'Mobility of Economic Activities'),
      (L(11, 'Examine the mobility of modern economic activities', 'that you have studied.'),),
      (S(27, 'MNC named · 2 marks', 'Annotation'),),
      (fixed('MNC named', 2, 'MNC named · 2 marks'), srp('Examination', 14, f'Examination · 14 x {SRPS}')),
      '3-2', MNC, ID + 'p2-q7b', True),
    T('p2-7c', P2, '7C', '', 30, 11, L(11, 'Environmental Impact'),
      (L(11, 'Examine how economic activities can have an environmental impact', 'a global scale.'),),
      (S(28, 'Environmental impact identified · 2 marks', 'Annotation'),),
      (fixed('Environmental impact identified', 2, 'Environmental impact identified · 2 marks'),
       pair('Examples · 2 + 2 marks', 'Examples'), srp('Examination', 12, f'Examination · 12 x {SRPS}')),
      '3-4', ENV, ID + 'p2-q7c', True),
]

Q8AS = (L(12, 'Examine the pie charts above showing European Union (EU) trade in goods partners',
          'following questions.'),)
PART_TWO += romans('8A', 12, L(12, 'European Union Trade'), Q8AS, ID + 'p2-q8a', ('page',), [
    ('(i)', 2, L(12, '(i) Which country did the EU import 6% of all imported goods from?'),
     (S(29, '(i) · Switzerland', '(ii) · 18'),), (fixed('Country', 2, '(i) · Switzerland · 2 marks'),), '2-0', TG),
    ('(ii)', 2, L(12, '(ii) What percentage of EU exports went to the United States?'),
     (S(29, '(ii) · 18', '(iii) · 6'),), (fixed('Percentage', 2, '(ii) · 18 (%) · 2 marks'),), '2-0', TG),
    ('(iii)', 2, L(12, '(iii) What was the percentage difference in exports and imports', 'in 2021?'),
     (S(29, '(iii) · 6', '(iv) · USA'),), (fixed('Difference', 2, '(iii) · 6 (%) · 2 marks'),), '2-0', TG),
    ('(iv)', 2, L(12, '(iv) Name one country shown above that the EU had a trade surplus with in 2021.'),
     (S(29, '(iv) · USA', '(v) · 8'),), (fixed('Country', 2, '(iv) · USA/Switzerland/UK · 2 marks'),), '2-0', TG),
    ('(v)', 4, L(12, '(v) Calculate X, the percentage of imports to the EU that came from Russia in 2021.'),
     (S(29, '(v) · 8', '(vi) · Valid explanation'),), (fixed('Calculation', 4, '(v) · 8 (%) · 4 marks'),),
     '2-0', TG),
    ('(vi)', 4, L(12, '(vi) Explain briefly the term balance of trade.'),
     (S(29, '(vi) · Valid explanation', '(vii) · Valid explanation'),),
     (pair('(vi) · Valid explanation · 2 + 2 marks', 'Explanation'),), '3-3', EU_TRADE),
    ('(vii)', 4, L(12, '(vii) Explain briefly one way that change in EU membership', 'EU trade.'),
     (S(29, '(vii) · Valid explanation', None),),
     (pair('(vii) · Valid explanation · 2 + 2 marks', 'Impact on EU trade'),), '3-3', EU_TRADE),
])

PART_TWO += [
    T('p2-8b', P2, '8B', '', 30, 12, L(12, 'Economic Development – Developed Economy'),
      (L(12, 'Examine the development of one of the following with reference to a developed economy',
         'Mass tourism.'),),
      (S(30, 'Developed economy named · 2 marks', 'Annotation'),),
      (fixed('Developed economy named', 2, 'Developed economy named · 2 marks'),
       srp('Examination', 14, f'Examination · 14 x {SRPS}')),
      '3-0', ECON, ID + 'p2-q8b-footloose-industries', True,
      routes=bullet_routes('p2-q8b-', ('Footloose industries', 'Financial services', 'Mass tourism.'))),
    T('p2-8c', P2, '8C', '', 30, 12, L(12, 'Economic Development', nth=1),
      (L(12, 'Using evidence from the 1:50 000 Ordnance Survey map that accompanies this paper,',
         'shown on the Ordnance Survey map.'),),
      (S(31, 'Three factors @ 10 marks each', 'Annotation'),),
      tuple(Criterion(f'Factor {n}', 10, evens(10), 'srp', FACTOR) for n in (1, 2, 3)),
      '3-0', ECON + MAP, ID + 'p2-q8c', False, ('map', 'legend')),
]

Q9AS = (L(13, 'Examine the data above showing the average total years of schooling', 'following questions.'),)
PART_TWO += romans('9A', 13, L(13, 'Economic Development'), Q9AS, ID + 'p2-q9a', ('page',), [
    ('(i)', 16, L(13, '(i) Using graph paper, draw a suitable graph to illustrate this data.'),
     (S(32, 'Bar Chart · Pie Chart', 'Annotation'),), GRAPH, '2-0', TG),
    ('(ii)', 4, L(13, '(ii) Explain briefly one disadvantage of using the Human Development Index (HDI)',
                  'economic development.'),
     (S(33, 'Valid explanation · 2 + 2 marks', '9B.'),), (pair('Valid explanation · 2 + 2 marks', 'Disadvantage'),),
     '3-1', ECON + DEV),
])

PART_TWO += [
    T('p2-9b', P2, '9B', '', 30, 13, L(13, 'Colonialism'),
      (L(13, 'Examine the impact of colonialism on a developing economy that you have studied.'),),
      (S(33, 'Impact identified · 2 marks', 'Annotation'),),
      (fixed('Impact identified', 2, 'Impact identified · 2 marks'),
       fixed('Developing economy named', 2, 'Developing economy named · 2 marks'),
       srp('Examination', 13, f'Examination · 13 x {SRPS}')),
      '3-1', DEV, ID + 'p2-q9b', True),
    T('p2-9c', P2, '9C', '', 30, 13, L(13, 'Renewable Energy'),
      (L(13, 'Examine how the development of renewable energy is crucial', 'economy.'),),
      (S(34, 'Importance for Ireland’s environment identified', 'Annotation'),),
      (fixed('Importance for Ireland’s environment identified', 2,
             'Importance for Ireland’s environment identified · 2 marks'),
       fixed('Importance for Ireland’s economy identified', 2,
             'Importance for Ireland’s economy identified · 2 marks'),
       srp('Examination', 13, f'Examination · 13 x {SRPS}')),
      '3-5', ENERGY, ID + 'p2-q9c', True),
    # Question 10
    T('p2-10a', P2, '10A', '', 20, 14, L(14, 'Aerial Photograph'),
      (L(14, 'Examine the aerial photograph of Cavan accompanying this paper.',
         'A residential land-use in the background.'),),
      (S(35, 'Sketch Outline', None),), AERIAL_SKETCH, '2-8', AER + URB, ID + 'p2-q10a', False, ('aerial',),
      row_labels=(None, L(14, 'The lake'), L(14, 'An ecclesiastical land-use'), L(14, 'A carpark'),
                  L(14, 'A residential land-use in the background.'))),
    T('p2-10b', P2, '10B', '', 30, 14, L(14, 'Urban Issues'),
      (L(14, 'Discuss any two of the following issues that may arise', 'Environmental issues.'),),
      (S(36, 'Discussion of issue one', 'Annotation'),),
      (split('Discussion of the two issues (8/7 and 7/8 SRPs)', 15,
             f'Discussion of issue one · 8/7 x {SRPS}', f'Discussion of issue two · 7/8 x {SRPS}'),),
      '4-5', URB,
      *pool(ID + 'p2-q10b-', ('Urban decay and absence of community', 'Urban sprawl', 'Environmental issues.'),
            2)[:1], True,
      absorbs=pool(ID + 'p2-q10b-', ('Urban decay and absence of community', 'Urban sprawl',
                                     'Environmental issues.'), 2)[1]),
    T('p2-10c', P2, '10C', '', 30, 14, L(14, 'Migration'),
      (L(14, 'Describe and explain changes in patterns of migration to and from Ireland since 1950.'),),
      (S(37, 'Change in pattern of migration to Ireland · 2 marks', 'Annotation'),),
      (fixed('Change in pattern of migration to Ireland', 2, 'Change in pattern of migration to Ireland · 2 marks'),
       fixed('Change in pattern of migration from Ireland', 2,
             'Change in pattern of migration from Ireland · 2 marks'),
       srp('Description / explanation', 13, f'Description / Explanation · 13 x {SRPS}')),
      '4-2', POP, ID + 'p2-q10c', True),
]

Q11AS = (L(15, 'Examine the data above showing the percentage of all asylum applications', 'following questions.'),)
PART_TWO += romans('11A', 15, L(15, 'Asylum Applications in the EU'), Q11AS, ID + 'p2-q11a', ('page',), [
    ('(i)', 16, L(15, '(i) Using graph paper, draw a suitable graph to illustrate this data.'),
     (S(38, 'Bar Chart · Pie Chart', 'Annotation'),), GRAPH, '2-0', TG),
    ('(ii)', 4, L(15, '(ii) Explain briefly one reason why people seek asylum.'),
     (S(38, 'Valid explanation · 2 + 2 marks', None),), (pair('Valid explanation · 2 + 2 marks', 'Reason'),),
     '4-2', POP),
])

PART_TWO += [
    T('p2-11b', P2, '11B', '', 30, 15, L(15, 'Dynamics of Population'),
      (L(15, 'Examine the impact of any one of the following factors on levels of population change',
         'Technology.'),),
      (S(39, 'Impact identified · 2 marks', 'Annotation'),),
      (fixed('Impact identified', 2, 'Impact identified · 2 marks'),
       fixed('Example of location', 2, 'Example of location · 2 marks'),
       srp('Examination', 13, f'Examination · 13 x {SRPS}')),
      '4-0', POP, ID + 'p2-q11b-the-development-of-resources', True,
      routes=bullet_routes('p2-q11b-', ('The development of resources', 'Income levels', 'Technology.'))),
    T('p2-11c', P2, '11C', '', 30, 15, L(15, 'Urban Land-Use'),
      (L(15, 'Describe and explain the land-use zones in any city that you have studied.'),),
      (S(40, 'Land-use zones identified', 'Annotation'),),
      (pair('Land-use zones identified · 2 + 2 marks', 'Land-use zones identified'),
       fixed('City named', 2, 'City named · 2 marks'),
       srp('Description/explanation', 12, f'Description/explanation · 12 x {SRPS}')),
      '4-4', (H + 'urban-land-uses',) + URB, ID + 'p2-q11c', True),
]

Q12AS = (L(16, 'Examine the diagram above showing the Demographic Transition Model', 'following questions.'),)
PART_TWO += romans('12A', 16, L(16, 'Population Dynamics'), Q12AS, ID + 'p2-q12a', ('page',), [
    ('(i)', 2, L(16, '(i) Name X, Stage 1 of the Demographic Transition Model.'),
     (S(41, '(i) · High Stationary', '(ii) · Early Expanding'),),
     (fixed('Stage 1', 2, '(i) · High Stationary · 2 marks'),), '4-0', POP),
    ('(ii)', 4, L(16, '(ii) Name Y, Stage 2 of the Demographic Transition Model and name an example', 'in this stage.'),
     (S(41, '(ii) · Early Expanding', '(iii) · Stage 4'),),
     (pair('(ii) · Early Expanding +Valid country · 2 +2 marks', 'Stage 2 and an example country'),), '4-0', POP),
    ('(iii)', 2, L(16, '(iii) What stage of the Demographic Transition Model is Ireland currently in?'),
     (S(41, '(iii) · Stage 4', '(iv) · Stage 2'),), (fixed('Stage', 2, '(iii) · Stage 4 · 2 marks'),), '4-0', POP),
    ('(iv)', 2, L(16, '(iv) In which stage of the Demographic Transition Model does the death rate', 'most?'),
     (S(41, '(iv) · Stage 2', '(v) · Valid reason'),), (fixed('Stage', 2, '(iv) · Stage 2 · 2 marks'),), '4-0', POP),
    ('(v)', 2, L(16, '(v) State one reason why the birth rate starts to decrease after stage 2.'),
     (S(41, '(v) · Valid reason', '(vi) · Valid explanation'),),
     (fixed('Reason', 2, '(v) · Valid reason stated · 2 marks'),), '4-0', POP),
    ('(vi)', 4, L(16, '(vi) Explain briefly one challenge facing countries in Stage 5', 'Model.'),
     (S(41, '(vi) · Valid explanation', '(vii) · Valid explanation'),),
     (pair('(vi) · Valid explanation · 2 + 2 marks', 'Challenge'),), '4-0', POP),
    ('(vii)', 4, L(16, '(vii) Explain briefly the term natural change.'),
     (S(41, '(vii) · Valid explanation', None),),
     (pair('(vii) · Valid explanation · 2 + 2 marks', 'Explanation'),), '4-0', POP),
])

PATTERN = ('Three patterns @ 10 marks each', 'For each pattern:', 'Pattern named · 2 marks',
           'OS map evidence · 2 marks', f'Description/Explanation · 3 x {SRPS}')
PART_TWO += [
    T('p2-12b', P2, '12B', '', 30, 16, L(16, 'Rural Settlement Patterns'),
      (L(16, 'Using evidence from the 1:50 000 Ordnance Survey map of Cavan', 'evident on the map.'),),
      (S(42, 'Three patterns @ 10 marks each', 'Annotation'),),
      tuple(Criterion(f'Pattern {n}', 10, evens(10), 'srp', PATTERN) for n in (1, 2, 3)),
      '4-3', URB + MAP, ID + 'p2-q12b', False, ('map', 'legend')),
    T('p2-12c', P2, '12C', '', 30, 16, L(16, 'Urban Growth – Developing World City'),
      (L(16, 'Problems can develop from the growth and expansion of urban centres.', 'that you have studied.'),),
      (S(43, 'Problems identified', 'Annotation'),),
      (pair('Problems identified · 2 + 2 marks', 'Problems identified'),
       fixed('Developing world city', 2, 'Developing world city · 2 marks'),
       srp('Discussion', 12, f'Discussion · 12 x {SRPS}')),
      '4-5', URB, ID + 'p2-q12c', True),
]

# ------------------------------------------------------------------ Options --
OC = (S(45, '*Overall Coherence (20 marks)', None, table=True),)


def option(q, page, theme, note_nth, prompt, scheme_page, topic, atlas, choice=None, after=None, end=None):
    card_id, absorbs = choice or (ID + f'p2-q{q}', ())
    return T(f'p2-{q}', P2, q, '', 80, page, theme, (prompt,),
             (S(scheme_page, 'Number of aspects', end, None, after), *OC),
             (Criterion('Aspects (3 @ 20 marks or 4 @ 15 marks)', 60, upto(60), 'srp',
                        ('Number of aspects', '?For each aspect:', 'Identifying aspect', '8 x SRP')),
              Criterion('Overall coherence', 20, (0, 6, 10, 14, 17, 20), 'exact',
                        ('Overall Coherence · 20 marks graded*', '*Overall Coherence (20 marks)', 'Excellent · 20',
                         'Very Good · 17', 'Good · 14', 'Fair · 10', 'Weak · 6', 'Poor · 0'))),
             topic, (atlas,), card_id, True,
             stem=(L(page, 'Note: It is better to discuss three or four aspects', 'large number of points.',
                     nth=note_nth),),
             absorbs=absorbs)


GI, GE = H + 'option-global-interdependence', H + 'option-geoecology'
CI, AO = H + 'option-culture-identity', H + 'option-atmosphere-ocean'
OPTIONS = [
    option('13', 18, L(18, 'Global Interdependence'), 0,
           L(18, 'Empowering people is a way of linking economic growth', 'Differing gender roles in society.'),
           47, '5-2', GI,
           choice=pool(ID + 'p2-q13-', ('Aid programmes', 'Land ownership patterns',
                                        'Differing gender roles in society.'), 2)),
    option('14', 18, L(18, 'Global Interdependence'), 0,
           L(18, 'Views of development and underdevelopment involve contrasting models', 'Discuss.'),
           48, '5-0', GI, after='14.', end='15.'),
    option('15', 18, L(18, 'Global Interdependence'), 0,
           L(18, 'We live in an interdependent global economy.', 'Human rights issues.'), 48, '5-1', GI, after='15.'),
    option('16', 18, L(18, 'Geoecology'), 1,
           L(18, 'Soil characteristics are affected by a combination', 'Podzolisation.'), 49, '6-1', GE,
           choice=pool(ID + 'p2-q16-', ('Weathering', 'Soil erosion', 'Leaching', 'Podzolisation.'), 3)),
    option('17', 18, L(18, 'Geoecology'), 1,
           L(18, 'Biomes are altered by human activities. Discuss.'), 50, '6-3', GE, after='17.', end='18.'),
    option('18', 18, L(18, 'Geoecology'), 1,
           L(18, 'Describe and explain the general composition and characteristics of any one soil type.'),
           50, '6-0', GE, after='18.'),
    option('19', 19, L(19, 'Culture and Identity'), 0,
           L(19, 'Many cultural groups around the world do not have a nation state', 'you have studied.'),
           51, '7-1', CI),
    option('20', 19, L(19, 'Culture and Identity'), 0,
           L(19, 'Examine how people express their culture and identity in everyday life.'), 52, '7-2', CI,
           after='20.', end='21.'),
    option('21', 19, L(19, 'Culture and Identity'), 0,
           L(19, 'Examine the strategies that have been or could be implemented', 'minority languages.'),
           52, '7-0', CI, after='21.'),
    option('22', 19, L(19, 'The Atmosphere – Ocean Environment'), 1,
           L(19, 'Examine how solar energy is transformed and redistributed', 'atmosphere and oceans.'), 53, '8-1', AO),
    option('23', 19, L(19, 'The Atmosphere – Ocean Environment'), 1,
           L(19, 'Give an account of how atmosphere-ocean phenomena', 'such measurements.'), 54, '8-0', AO,
           after='23.', end='24.'),
    option('24', 19, L(19, 'The Atmosphere – Ocean Environment'), 1,
           L(19, 'Examine how climate characteristics influence economic development.'), 54, '8-5', AO, after='24.'),
]

TASKS = [*PART_ONE, *PART_TWO, *OPTIONS]

ID_CORRECTION_REASON = (
    'The shipped card held every part of a question the scheme prices part by '
    'part. Its id is kept on the first separately priced part; the other parts '
    'are new cards with their own published allocation.')

# Every 2023 Higher card id shipped before this review (78). Each must survive.
LEGACY_IDS = [
    'geography-2023-hl-p1-q2',
    'geography-2023-hl-p1-q3',
    'geography-2023-hl-p1-q4',
    'geography-2023-hl-p1-q5',
    'geography-2023-hl-p1-q6',
    'geography-2023-hl-p1-q10',
    'geography-2023-hl-p1-q11',
    'geography-2023-hl-p1-q12',
    'geography-2023-hl-p2-q1b',
    'geography-2023-hl-p2-q1c',
    'geography-2023-hl-p2-q2a',
    'geography-2023-hl-p2-q2b-route-i-fluvial-landform',
    'geography-2023-hl-p2-q2b-route-i-coastal-landform',
    'geography-2023-hl-p2-q2b-route-i-glacial-landform',
    'geography-2023-hl-p2-q2b-route-ii',
    'geography-2023-hl-p2-q2c-the-surface-karst-landscape',
    'geography-2023-hl-p2-q2c-the-underground-karst-landscape',
    'geography-2023-hl-p2-q3a',
    'geography-2023-hl-p2-q3b-earthquakes',
    'geography-2023-hl-p2-q3b-volcanoes',
    'geography-2023-hl-p2-q3b-fold-mountains',
    'geography-2023-hl-p2-q3c-mining',
    'geography-2023-hl-p2-q3c-extraction-of-building-materials',
    'geography-2023-hl-p2-q3c-oil-gas-exploitation',
    'geography-2023-hl-p2-q3c-geothermal-energy-production',
    'geography-2023-hl-p2-q4a',
    'geography-2023-hl-p2-q4b',
    'geography-2023-hl-p2-q4c-transport-location',
    'geography-2023-hl-p2-q4c-transport-primary-economic-activity',
    'geography-2023-hl-p2-q4c-location-primary-economic-activity',
    'geography-2023-hl-p2-q5a',
    'geography-2023-hl-p2-q5b',
    'geography-2023-hl-p2-q5c',
    'geography-2023-hl-p2-q6a',
    'geography-2023-hl-p2-q6b-labour-transport',
    'geography-2023-hl-p2-q6b-labour-raw-materials',
    'geography-2023-hl-p2-q6b-labour-markets',
    'geography-2023-hl-p2-q6b-transport-raw-materials',
    'geography-2023-hl-p2-q6b-transport-markets',
    'geography-2023-hl-p2-q6b-raw-materials-markets',
    'geography-2023-hl-p2-q6c',
    'geography-2023-hl-p2-q7b',
    'geography-2023-hl-p2-q7c',
    'geography-2023-hl-p2-q8a',
    'geography-2023-hl-p2-q8b-footloose-industries',
    'geography-2023-hl-p2-q8b-financial-services',
    'geography-2023-hl-p2-q8b-mass-tourism',
    'geography-2023-hl-p2-q9a',
    'geography-2023-hl-p2-q9b',
    'geography-2023-hl-p2-q9c',
    'geography-2023-hl-p2-q10b-urban-decay-and-absence-of-communi-urban-sprawl',
    'geography-2023-hl-p2-q10b-urban-decay-and-absence-of-communi-environmental-issues',
    'geography-2023-hl-p2-q10b-urban-sprawl-environmental-issues',
    'geography-2023-hl-p2-q10c',
    'geography-2023-hl-p2-q11a',
    'geography-2023-hl-p2-q11b-the-development-of-resources',
    'geography-2023-hl-p2-q11b-income-levels',
    'geography-2023-hl-p2-q11b-technology',
    'geography-2023-hl-p2-q11c',
    'geography-2023-hl-p2-q12a',
    'geography-2023-hl-p2-q12c',
    'geography-2023-hl-p2-q13-aid-programmes-land-ownership-patterns',
    'geography-2023-hl-p2-q13-aid-programmes-differing-gender-roles-in-society',
    'geography-2023-hl-p2-q13-land-ownership-patterns-differing-gender-roles-in-society',
    'geography-2023-hl-p2-q14',
    'geography-2023-hl-p2-q15',
    'geography-2023-hl-p2-q16-weathering-soil-erosion-leaching',
    'geography-2023-hl-p2-q16-weathering-soil-erosion-podzolisation',
    'geography-2023-hl-p2-q16-weathering-leaching-podzolisation',
    'geography-2023-hl-p2-q16-soil-erosion-leaching-podzolisation',
    'geography-2023-hl-p2-q17',
    'geography-2023-hl-p2-q18',
    'geography-2023-hl-p2-q19',
    'geography-2023-hl-p2-q20',
    'geography-2023-hl-p2-q21',
    'geography-2023-hl-p2-q22',
    'geography-2023-hl-p2-q23',
    'geography-2023-hl-p2-q24',
]
