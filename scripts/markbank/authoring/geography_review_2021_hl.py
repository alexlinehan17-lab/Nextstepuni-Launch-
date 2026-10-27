"""Independent review ledger: Leaving Certificate Geography 2021 Higher Level.

Sources (English editions, Paper Trail index; sizes and SHA-256 pinned in
EXPECTED_SOURCES and the generated audit): Part One and Answerbook
LC005ALP042EV (48 pages), Part Two LC005ALP043EV (24 pages), marking scheme
LC005ALP000EV (64 pages), and the common companions in the harvested corpus —
the 1:50 000 Foxford map LC005CLP003EV, its legend LC005CLPC00EV and the
Foxford aerial photograph LC005CLP004EV (published only as a JPEG).

Visual sweep (every page rendered and read on 2026-10-12):
  Part One booklet p1 cover (2021: Part One 80 marks, Part Two 240); p2
  instructions (Part One "Attempt any TEN"; Part Two "attempt THREE", not
  all from one section); p3-p13 Questions 1-12 (p9 holds Q7 and Q8; Q9
  prints a vertical photograph of Foxford); p14 Part Two answerbook
  instructions; p15-p18 graph paper; p19-p47 lined answer pages; p48 back.
  Part Two booklet p1 cover; p2 Part Two instructions; p3-p9 Sections 1-2
  (Q1-Q6; p8 holds only 6A); p10 Section 3 divider; p11-p18 Electives
  (Q7-Q12; p13 holds only 8C, p17 11B and 11C); p19 Section 4 divider and
  note; p20-p21 Options (Q13-Q24); p22-p23 "Do not hand this up"; p24
  copyright/back cover.
  Scheme p1 cover; p2-p3 notes and annotation key; p4 Part One table (two
  columns: Q1-Q6, Q7-Q12); p5 the 2021 Part Two adjustment rule; p6-p24
  Q1-Q6 (6A's answers on p23); p25 divider; p26-p43 Q7-Q12; p44 divider;
  p45 option outline and Overall Coherence descriptors; p46 option
  annotations; p47-p54 Q13-Q24; p55-p58 Geographical Investigation
  (coursework); p59 investigation topics; p60 Irish-language bonus marks;
  p61-p63 printed "Blank Page"; p64 back cover.
  Companions: Foxford map extract (Lough Cullin, the River Moy, the N26);
  OS legend sheet; oblique aerial photograph of Foxford.

Companions. Part One Q1 and Q7 (map, legend), Q8 (aerial, map, legend) and
Q9 (page, aerial); Part Two 1A, 8C and 11C (map, legend), 7A and 10A
(aerial) were held back before this review because their companions were not
wired. Each now carries the exact official documents it names.

Boundaries and tariffs follow the 2022 Higher ledger: every part the scheme
prices separately is a task; a matching table under one printed instruction
is one task with a criterion per scheme row, the scheme listing its answers
in the printed row order: Q1 G 30 08 V-shaped valley, M 29 98 River
confluence (the scheme prints the grid reference as "M 28 98"), G 26 07
Levees, M 28 99 Oxbow lake formation; Q2 Convection currents=D, Ocean
trench=A, Fold mountains=C, Focus=B; Q3 prints (i) and (ii) in one table:
(i) Striations=C, Scree slope=B, Moraines=D, Limestone pavement=A and (ii)
Erosion, Weathering, Deposition, Weathering; Q4 likewise: (i)
Sandstone=C, Limestone=A, Granite=B and (ii) Sedimentary, Sedimentary,
Igneous (each column read with its own clip; Q4 (ii) with a band clip); Q5 Oceanic crust=D, Extinct
volcano visible=E, Active volcano=C, Asthenosphere=B, Oldest extinct
volcano=F, Plume of magma=A; Q6 Climatic=Cool Temperate Oceanic,
Urban=Milan, Peripheral=Mezzogiorno, Administrative=Sligo-Leitrim
Constituency, Geomorphological=Munster Ridge and Valley, Cultural=Basque;
Q9 wasteland=A, recreation=D, open space to residential=E, relief road=C
(industrial to residential B is printed, so the scheme's bold B row is not
priced: Q9 is [8m]). Lettered true/false statements, 6(ii) and 10(ii), are
tasks, as in 2022-2025.
"""

import itertools

from geography_review import (
    Criterion, Lift, Route, SchemeSlice, Task, pool, evens, fixed, slug, srp, sums, upto,
)

YEAR = 2021
LEVEL = 'higher'
PAPER_PAGES = {1: 48, 2: 24}
SCHEME_PAGES = 64
QUESTION_TARIFFS = {1: {str(n): 8 for n in range(1, 13)},
                    2: {**{f'{n}{x}': (20 if x == 'A' else 30)
                           for n in range(1, 13) for x in 'ABC'},
                        **{str(n): 80 for n in range(13, 25)}}}

EXPECTED_SOURCES = {
    'paper1': ('LC005ALP042EV.pdf', 2409626),
    'paper2': ('LC005ALP043EV.pdf', 2068047),
    'scheme': ('LC005ALP000EV.pdf', 1768308),
    'map': ('LC005CLP003EV.pdf', 5155375),
    'legend': ('LC005CLPC00EV.pdf', 784643),
    'aerial': ('LC005CLP004EV.jpg', 5536812),
}

PAGE_REVIEW = {
    'paper1': {1: 'cover', 2: 'instructions', **{p: 'question' for p in range(3, 14)},
               14: 'answerbook instructions', **{p: 'graph-paper answer page' for p in range(15, 19)},
               **{p: 'lined answer page' for p in range(19, 48)}, 48: 'copyright/back cover'},
    'paper2': {1: 'cover', 2: 'Part Two instructions',
               **{p: 'question' for p in (*range(3, 10), *range(11, 19), 20, 21)},
               10: 'section divider', 19: 'section divider and option note',
               22: 'do not hand this up', 23: 'do not hand this up', 24: 'copyright/back cover'},
    'scheme': {1: 'cover', 2: 'notes', 3: 'notes and annotation key', 4: 'Part One table',
               5: 'Part Two adjustment rule (2021 additional choice)',
               **{p: 'Part Two allocation' for p in range(6, 25)}, 25: 'section divider',
               **{p: 'Part Two allocation' for p in range(26, 44)}, 44: 'section divider',
               45: 'option outline and coherence descriptors', 46: 'option annotations',
               **{p: 'option allocation' for p in range(47, 55)},
               **{p: 'geographical investigation (coursework)' for p in range(55, 59)},
               59: 'investigation topics', 60: 'Irish-language bonus marks',
               61: 'blank', 62: 'blank', 63: 'blank', 64: 'back cover'},
}

EXPECTED_SELECTION_SCAN = [
    [1, 2, 'attempt any ten'], [1, 2, 'attempt three'], [1, 2, 'choose'], [1, 2, 'choose'],
    [1, 3, 'attempt any ten'],
    [2, 2, 'attempt three'], [2, 2, 'choose'], [2, 2, 'choose'],
    [2, 3, 'answer (i) or (ii)'], [2, 3, 'or one'], [2, 3, 'or one'],
    [2, 4, 'one of the following'],
    [2, 6, 'any two'],
    [2, 9, 'any two'], [2, 9, 'any two'],
    [2, 11, 'any two'],
    [2, 13, 'choose'], [2, 13, 'choose'],
    [2, 20, 'three of the following'], [2, 20, 'any three'],
]
SELECTION_REVIEW = [
    {'scan': [[1, 2, 'attempt any ten'], [1, 2, 'attempt three'], [1, 2, 'choose'], [1, 2, 'choose'],
              [1, 3, 'attempt any ten'], [2, 2, 'attempt three'], [2, 2, 'choose'], [2, 2, 'choose']],
     'kind': 'exam-attempt-rule',
     'reason': 'Part One any ten of twelve and Part Two three questions ("not allowed to choose all three from the same section") are attempt rules; every question is carded.'},
    {'scan': [[2, 3, 'answer (i) or (ii)'], [2, 3, 'or one'], [2, 3, 'or one']], 'kind': 'closed-route',
     'reason': '1B: (i) or (ii); (i) offers one fluvial OR one coastal OR one glacial landform -> 4 routes.'},
    {'scan': [[2, 4, 'one of the following']], 'kind': 'closed-choose-one',
     'reason': '2C one of three printed human impacts -> 3 routes.'},
    {'scan': [[2, 9, 'any two'], [2, 9, 'any two'], [2, 11, 'any two'], [2, 20, 'three of the following'],
              [2, 20, 'any three']],
     'kind': 'choose-n-one-card',
     'reason': '6B any two of three printed factors, 6C any two of five tabled factors, 7B any two of three printed headings, 14 three of four printed themes and 17 any three of four printed factors -> one card each with every printed item (choice is not a route; the scheme marks each chosen item alike).'},
    {'scan': [[2, 13, 'choose'], [2, 13, 'choose']], 'kind': 'not-a-selection',
     'reason': '8C "might choose to locate" / "might choose not to locate" describe the multinational company, not a candidate choice.'},
    {'scan': [[2, 6, 'any two']], 'kind': 'open-response',
     'reason': 'No printed pool: 4B any two factors. Open choices are not fanned out: "one urban area", "one multinational company", "example(s)". Compulsory lists stay whole: 1A, 4A, 7A and 10A each bullet, 4C both challenges, 7C both of the following, 10C each of rural and urban areas, 11B both problems, 18 each activity.'},
]

P1, P2 = 1, 2
LEFT = (0.0, 0.0, 0.5, 1.0)
RIGHT = (0.5, 0.0, 1.0, 1.0)
# Q3 and Q4 print (i) and (ii) side by side in the left column of the Part One table.
COL_I = (0.0, 0.0, 0.245, 1.0)
COL_II = (0.245, 0.0, 0.5, 1.0)
# Q4 (ii) shares its column with Q4 (iii) below; a band of the page holds only Q4 (ii).
Q4_II = (0.245, 0.46, 0.5, 0.535)
ID = 'geography-2021-hl-'
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
ENV = (H + 'economic-environmental-impact',)

PART_ONE = [
    T('p1-1', P1, '1', '', 8, 3, L(3, 'Landscape Identification'),
      (L(3, 'In the table below, match each of the following landscape features', 'River confluence.'),),
      (S(4, 'G 30 08 V-shaped valley', 'Q2', LEFT),),
      rows(['G 30 08 V-shaped valley · 2m', 'M 28 98 River confluence · 2m', 'G 26 07 Levees · 2m',
            'M 28 99 Oxbow lake formation 2m'], 2),
      '2-6', MAP + RIVERS, ID + 'p1-q1', False, ('map', 'legend'),
      (L(3, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper.'),),
      row_labels=(L(3, 'G 30 08'), L(3, 'M 29 98'), L(3, 'G 26 07'), L(3, 'M 28 99'))),
]

Q2S = (L(4, 'Examine the diagram above and answer each of the following questions.'),)
PART_ONE += [
    T('p1-2-i', P1, '2', '(i)', 4, 4, L(4, 'Plate Tectonics'),
      (L(4, '(i) Match each of the letters A, B, C and D with the term', 'table below.'),),
      (S(4, '(i) D · 1m', '(ii) Any valid mountain', LEFT, 'Q2'),), rows(['(i) D · 1m', '=A · 1m', '=C · 1m', '=B · 1m']),
      '0-0', PS, ID + 'p1-q2', True, ('page',), Q2S,
      row_labels=(L(4, 'Convection currents'), L(4, 'Ocean trench'), L(4, 'Fold mountains'),
                  L(4, 'Focus of an earthquake'))),
    T('p1-2-ii', P1, '2', '(ii)', 2, 4, L(4, 'Plate Tectonics'),
      (L(4, '(ii) Name one example of a mountain range formed by folding found outside of Ireland.'),),
      (S(4, '(ii) Any valid mountain range 2m', '(iii) Destructive', LEFT),),
      (fixed('Mountain range', 2, '(ii) Any valid mountain range 2m'),), '0-0', PS + RW, ID + 'p1-q2-ii', False,
      ('page',), Q2S),
    T('p1-2-iii', P1, '2', '(iii)', 2, 4, L(4, 'Plate Tectonics'),
      (L(4, '(iii) Name the type of plate boundary illustrated in the diagram above.'),),
      (S(4, '(iii) Destructive/ Convergent 2m', 'Q3', LEFT),),
      (fixed('Plate boundary', 2, '(iii) Destructive/ Convergent 2m'),), '0-0', PS, ID + 'p1-q2-iii', False,
      ('page',), Q2S),
]

Q3S = (L(5, 'Examine the photographs above and answer each of the following questions.'),)
Q3_ROWS = (L(5, 'Striations'), L(5, 'Scree slope'), L(5, 'Moraines'), L(5, 'Limestone pavement'))
Q4S = (L(6, 'Examine the map above and answer each of the following questions.'),)
Q4_ROWS = (L(6, 'Sandstone'), L(6, 'Limestone'), L(6, 'Granite'))
PART_ONE += [
    T('p1-3-i', P1, '3', '(i)', 4, 5, L(5, 'The Physical Environment'),
      (L(5, '(i) Match each of the photographs A, B, C and D', 'table below.'),),
      (S(4, '(i) C · 1m', 'Q4', COL_I, 'Q3'),), rows(['(i) C · 1m', '=B · 1m', '=D · 1m', '=A · 1m']),
      '0-4', GLAC + RW + KARST, ID + 'p1-q3', True, ('page',), Q3S, row_labels=Q3_ROWS),
    T('p1-3-ii', P1, '3', '(ii)', 4, 5, L(5, 'The Physical Environment'),
      (L(5, '(ii) Indicate, by ticking the correct box', 'erosion, deposition or weathering.'),),
      (S(4, '(ii) Erosion', '(ii) Sedimentary', COL_II),),
      rows(['(ii) Erosion · 1m', '=Weathering · 1m@0', 'Deposition · 1m', '=Weathering · 1m@1']),
      '0-4', GLAC + RW + KARST, ID + 'p1-q3-ii', False, ('page',), Q3S, row_labels=Q3_ROWS),
    T('p1-4-i', P1, '4', '(i)', 3, 6, L(6, 'Rocks'),
      (L(6, '(i) Match each of the locations A, B and C on the map above', 'table below.'),),
      (S(4, '(i) C · 1m', '(iii) Limes', COL_I, 'Q4'),), rows(['(i) C · 1m', '=A · 1m', '=B · 1m']),
      '0-1', RW, ID + 'p1-q4', True, ('page',), Q4S, row_labels=Q4_ROWS),
    T('p1-4-ii', P1, '4', '(ii)', 3, 6, L(6, 'Rocks'),
      (L(6, '(ii) Indicate, by ticking the correct box', 'igneous, sedimentary or metamorphic rock.'),),
      (S(4, '(ii) Sedimentary', None, Q4_II),),
      rows(['(ii) Sedimentary 1m', '=Sedimentary 1m', 'Igneous 1m']),
      '0-1', RW, ID + 'p1-q4-ii', False, ('page',), Q4S, row_labels=Q4_ROWS),
    T('p1-4-iii', P1, '4', '(iii)', 2, 6, L(6, 'Rocks'),
      (L(6, '(iii) Name the sedimentary rock that each of the following existed as', 'heat and/or pressure.'),),
      (S(4, '(iii) Limestone 1m', 'Q5', LEFT),), rows(['(iii) Limestone 1m', '=Sandstone 1m']),
      '0-1', RW, ID + 'p1-q4-iii', False, ('page',), Q4S, row_labels=(L(6, 'Marble:'), L(6, 'Quartzite:'))),
]

Q5S = (L(7, 'Examine the diagram above which illustrates the development of a volcanic hot spot',
         'following questions.'),)
PART_ONE += [
    T('p1-5-i', P1, '5', '(i)', 6, 7, L(7, 'Plate Tectonics - Hot Spot Activity'),
      (L(7, '(i) Match each of the letters A, B, C, D, E and F on the diagram', 'best matches it.'),),
      (S(4, '(i) D · 1m', '(ii) Any valid example', LEFT, 'Q5'),),
      rows(['(i) D · 1m', '=E · 1m', '=C · 1m', '=B · 1m', '=F · 1m', '=A · 1m']),
      '0-7', EV + PS, ID + 'p1-q5', True, ('page',), Q5S,
      row_labels=(L(7, 'Oceanic crust'), L(7, 'Extinct volcano visible above water’s surface'),
                  L(7, 'Active volcano'), L(7, 'Asthenosphere'), L(7, 'Oldest extinct volcano'),
                  L(7, 'Plume of magma'))),
    T('p1-5-ii', P1, '5', '(ii)', 2, 7, L(7, 'Plate Tectonics - Hot Spot Activity'),
      (L(7, '(ii) Name one example of a volcanic hot spot that you have studied.'),),
      (S(4, '(ii) Any valid example · 2m', 'Q6', LEFT),), (fixed('Hot spot', 2, '(ii) Any valid example · 2m'),),
      '0-7', EV, ID + 'p1-q5-ii', False, ('page',), Q5S),
]

TF6 = L(8, '(ii) Indicate whether each of the following statements is true or false', 'correct box.')
REGIONS = IRL + EURO
PART_ONE += [
    T('p1-6-i', P1, '6', '(i)', 6, 8, L(8, 'Concept of a Region'),
      (L(8, '(i) Complete the table below by matching each of the examples of regions', 'in the table.'),
       L(8, 'Examples of Regions:'), L(8, 'Munster Ridge and Valley region'), L(8, 'Basque Country'),
       L(8, 'Cool Temperate Oceanic region'), L(8, 'Milan'), L(8, 'Mezzogiorno'),
       L(8, 'Sligo-Leitrim Constituency')),
      (S(4, '(i) Cool Temperate Oceanic', '(ii) False', LEFT),),
      rows(['(i) Cool Temperate Oceanic · 1m', 'Milan · 1m', 'Mezzogiorno · 1m',
            'Sligo-Leitrim Constituency · 1m', 'Munster Ridge and Valley · 1m', 'Basque · 1m']),
      '1-0', REGIONS, ID + 'p1-q6', True, ('page',),
      row_labels=(L(8, 'Climatic region'), L(8, 'Urban region'), L(8, 'Peripheral region'),
                  L(8, 'Administrative region in Ireland'), L(8, 'Geomorphological region'),
                  L(8, 'Cultural region'))),
    T('p1-6-ii-a', P1, '6', '(ii)(a)', 1, 8, L(8, 'Concept of a Region'),
      (TF6, L(8, '(a) Core regions experience net emigration.')),
      (S(4, '(ii) False 1m', 'True · 1m', LEFT),), (fixed('Statement (a)', 1, '(ii) False 1m'),),
      '1-0', REGIONS, ID + 'p1-q6-ii-a', False, ('page',)),
    T('p1-6-ii-b', P1, '6', '(ii)(b)', 1, 8, L(8, 'Concept of a Region'),
      (TF6, L(8, '(b) High unemployment and abandoned factories', 'industrial decline.')),
      (S(4, 'True · 1m', 'Page 2', LEFT),), (fixed('Statement (b)', 1, 'True · 1m'),),
      '1-0', REGIONS, ID + 'p1-q6-ii-b', False, ('page',)),
]

Q7S = (L(9, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper, and',
         'following questions.'),)
PART_ONE += p1_romans('7', 9, L(9, 'Map Skills'), Q7S, ID + 'p1-q7', False, ('map', 'legend'), [
    ('(i)', 2, L(9, '(i) What is the height, in metres, at the spot height at G 314 083?'),
     S(4, '(i) 220m', '(ii) 5.2km', RIGHT), (fixed('Height', 2, '(i) 220m · 2m'),), '2-6', MAP),
    ('(ii)', 2, L(9, '(ii) Measure the length, in kilometres, of the N26', 'G 268 042.'),
     S(4, '(ii) 5.2km', '(iii) G 254', RIGHT), (fixed('Length', 2, '(ii) 5.2km 2m'),), '2-6', MAP),
    ('(iii)', 2, L(9, '(iii) Give a six-figure grid reference for the railway station.'),
     S(4, '(iii) G 254 044', '(iv) 28km', RIGHT), (fixed('Grid reference', 2, '(iii) G 254 044 · 2m'),), '2-6', MAP),
    ('(iv)', 2, L(9, '(iv) Calculate the approximate area of the map extract', 'west of the railway line.'),
     S(4, '(iv) 28km² 2m', 'Q8', RIGHT), (fixed('Area', 2, '(iv) 28km² 2m'),), '2-6', MAP),
])

Q8S = (L(9, 'Examine the aerial photograph of Foxford and the 1:50 000 Ordnance Survey map',
         'following questions.'),)
PART_ONE += p1_romans('8', 9, L(9, 'Aerial Photograph and Ordnance Survey Map'), Q8S, ID + 'p1-q8', False,
                      ('aerial', 'map', 'legend'), [
    ('(i)', 2, L(9, '(i) Name the road that enters the aerial photograph in the left foreground.'),
     S(4, '(i) N 58', '(ii) G 268', RIGHT), (fixed('Road', 2, '(i) N 58 · 2m'),), '2-8', AER + MAP),
    ('(ii)', 2, L(9, '(ii) Give a six-figure grid reference for the bridge', 'aerial photograph.'),
     S(4, '(ii) G 268 043', '(iii) NNE', RIGHT), (fixed('Grid reference', 2, '(ii) G 268 043 · 2m'),),
     '2-8', AER + MAP),
    ('(iii)', 2, L(9, '(iii) In what direction was the camera pointed when the aerial photograph was taken?'),
     S(4, '(iii) NNE', '(iv) False', RIGHT), (fixed('Direction', 2, '(iii) NNE · 2m'),), '2-8', AER + MAP),
    ('(iv)', 2, (L(9, '(iv) Indicate whether the following statement is true or false', 'correct box.'),
                 L(9, 'There is a church in the shape of a cross in the left foreground.')),
     S(4, '(iv) False', 'Q9', RIGHT, 'Q8'), (fixed('True or false', 2, '(iv) False · 2m'),), '2-8', AER),
])

PART_ONE.append(T(
    'p1-9', P1, '9', '', 8, 10, L(10, 'Aerial Photographs'),
    (L(10, 'Find each of the locations A, B, C, D and E', 'One has been completed for you.'),),
    (S(4, 'A · 2m', 'B 2m', RIGHT), S(4, 'C · 2m', 'Q10', RIGHT)),
    rows(['A · 2m', 'D · 2m', 'E · 2m', 'C · 2m'], 2),
    '2-8', AER + URB, ID + 'p1-q9', False, ('page', 'aerial'),
    (L(10, 'Examine the oblique aerial photograph of Foxford', 'vertical aerial photograph below.', nth=0),),
    row_labels=(L(10, 'From green space to wasteland'), L(10, 'From green space to recreation'),
                L(10, 'From open space to residential'), L(10, 'From agriculture to relief road'))))

Q10S = (L(11, 'Examine the weather map above showing the total monthly rainfall', 'following questions.'),)
TF10 = L(11, '(ii) Indicate whether the following statements are true or false', 'correct box.')
PART_ONE += [
    T('p1-10-i', P1, '10', '(i)', 2, 11, L(11, 'Weather Statistics'),
      (L(11, '(i) How much rain (in mm) fell at the area marked X on the map above?'),),
      (S(4, '(i) 50-74mm', '(ii) False', RIGHT),), (fixed('Rainfall', 2, '(i) 50-74mm 2m'),),
      '2-7', WX, ID + 'p1-q10', True, ('page',), Q10S),
    T('p1-10-ii-a', P1, '10', '(ii)(a)', 1, 11, L(11, 'Weather Statistics'),
      (TF10, L(11, '(a) In October 2020 more rain fell on the east coast', 'west coast.')),
      (S(4, '(ii) False · 1m', 'True · 1m', RIGHT),), (fixed('Statement (a)', 1, '(ii) False · 1m'),),
      '2-7', WX, ID + 'p1-q10-ii-a', False, ('page',), Q10S),
    T('p1-10-ii-b', P1, '10', '(ii)(b)', 1, 11, L(11, 'Weather Statistics'),
      (TF10, L(11, '(b) In October 2020 relief rain over mountains influenced where most rain fell.')),
      (S(4, 'True · 1m', '(iii) Isohyets', RIGHT),), (fixed('Statement (b)', 1, 'True · 1m'),),
      '2-7', WX, ID + 'p1-q10-ii-b', False, ('page',), Q10S),
    T('p1-10-iii', P1, '10', '(iii)', 2, 11, L(11, 'Weather Statistics'),
      (L(11, '(iii) What is the name given to the lines on a weather map', 'equal rainfall?'),),
      (S(4, '(iii) Isohyets', '(iv) Depression', RIGHT),), (fixed('Term', 2, '(iii) Isohyets 2m'),),
      '2-7', WX, ID + 'p1-q10-iii', False, ('page',), Q10S),
    T('p1-10-iv', P1, '10', '(iv)', 2, 11, L(11, 'Weather Statistics'),
      (L(11, '(iv) Is rainfall more likely during an anticyclone or a depression?'),),
      (S(4, '(iv) Depression', 'Q11', RIGHT),), (fixed('Anticyclone or depression', 2, '(iv) Depression 2m'),),
      '2-7', WX, ID + 'p1-q10-iv', False, ('page',), Q10S),
]

Q11S = (L(12, 'Examine the table above showing information on the production of selected crops',
          'following questions.'),)
PART_ONE += p1_romans('11', 12, L(12, 'Statistical Interpretation'), Q11S, ID + 'p1-q11', True, ('page',), [
    ('(i)', 2, L(12, '(i) How many thousand tonnes of potatoes were produced in Ireland in 2018?'),
     S(4, '(i) 273', '(ii) 2017', RIGHT), (fixed('Thousand tonnes', 2, '(i) 273 · 2m'),), '2-0', TG),
    ('(ii)', 2, L(12, '(ii) In which year listed in the table was the production of oats the highest?'),
     S(4, '(ii) 2017', '(iii) 173', RIGHT), (fixed('Year', 2, '(ii) 2017 · 2m'),), '2-0', TG),
    ('(iii)', 2, L(12, '(iii) Calculate the decrease in production of barley', 'between 2014 and 2019.'),
     S(4, '(iii) 173', '(iv) False', RIGHT), (fixed('Decrease', 2, '(iii) 173 2m'),), '2-0', TG),
    ('(iv)', 2, (L(12, '(iv) Indicate whether the following statement is true or false', 'correct box.'),
                 L(12, 'Pastoral farming involves growing crops, such as wheat and barley.')),
     S(4, '(iv) False · 2m', 'Q12', RIGHT, 'Q11'), (fixed('True or false', 2, '(iv) False · 2m'),),
     '3-0', (H + 'elective-economic',)),
])

Q12S = (L(13, 'Examine the infographic above on the differences between urban and rural living',
          'following questions.'),)
PART_ONE += p1_romans('12', 13, L(13, 'Graphical Interpretation'), Q12S, ID + 'p1-q12', True, ('page',), [
    ('(i)', 2, (L(13, '(i) According to the infographic, which of the following has the highest percentage',
                  'Tick (✓) the correct box.'),
                L(13, 'Cities', nth=1), L(13, 'Towns and suburbs', nth=1), L(13, 'Rural areas', nth=1)),
     S(4, '(i) Cities', '(ii) 70', RIGHT), (fixed('Area', 2, '(i) Cities · 2m'),), '2-0', TG),
    ('(ii)', 2, L(13, '(ii) What percentage of the EU population in rural areas access the internet', 'daily basis?'),
     S(4, '(ii) 70', '(iii) 7.1', RIGHT), (fixed('Percentage', 2, '(ii) 70 (%) · 2m'),), '2-0', TG),
    ('(iii)', 2, L(13, '(iii) What percentage of the EU population living in towns and suburbs are unemployed?'),
     S(4, '(iii) 7.1', '(iv) Any valid', RIGHT), (fixed('Percentage', 2, '(iii) 7.1 (%) · 2m'),), '2-0', TG),
    ('(iv)', 2, L(13, '(iv) Briefly explain one reason why more people live in urban areas', 'rural areas.'),
     S(4, '(iv) Any valid brief explanation', '2 of 58', RIGHT),
     (one_plus_one('(iv) Any valid brief explanation 1m + 1m', 'Reason'),), '4-3', URB),
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
    """One allocation printed as two parts examined as split SRPs."""
    return srp(label, total, (first, second))


LANDFORMS = 'one fluvial landform or one coastal landform or one glacial landform'
IMPACTS = ('The impact of flood control measures on river processes',
           'The impact of coastal defence measures on coastal processes',
           'The impact of human activities on mass movement processes.')

PART_TWO = [
    T('p2-1a', P2, '1A', '', 20, 3, L(3, 'Ordnance Survey Map'),
      (L(3, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper.', 'above 200 metres.'),),
      (S(6, 'Sketch Outline', None),), OS_SKETCH, '2-6', MAP, ID + 'p2-q1a', False, ('map', 'legend'),
      row_labels=(None, L(3, 'The entire area of Lough Cullin'),
                  L(3, 'The course of the River Moy between G 259 024 and G 269 090'),
                  L(3, 'Mark an X at the confluence of the River Moy and the Yellow River'),
                  L(3, 'The entire area of land above 200 metres.'))),
    T('p2-1b', P2, '1B', '', 30, 3, L(3, 'Surface Processes'),
      (L(3, '(i) Examine the role of the process of deposition', 'that you have studied.'),),
      (S(7, 'Landform named · 2 marks', 'Annotation'),),
      (fixed('Landform named', 2, 'Landform named · 2 marks'), srp('Examination', 14, f'Examination · 14 x {SRPS}')),
      '0-9', RIVERS, ID + 'p2-q1b-route-i-fluvial-landform', True,
      routes=(
          Route('route-i-fluvial-landform', 'Route (i) · one fluvial landform', ID + 'p2-q1b-route-i-fluvial-landform',
                True, ((LANDFORMS, 'one fluvial landform'),), topic='0-9', atlas=RIVERS),
          Route('route-i-coastal-landform', 'Route (i) · one coastal landform', ID + 'p2-q1b-route-i-coastal-landform',
                True, ((LANDFORMS, 'one coastal landform'),), topic='0-10', atlas=SEA),
          Route('route-i-glacial-landform', 'Route (i) · one glacial landform', ID + 'p2-q1b-route-i-glacial-landform',
                True, ((LANDFORMS, 'one glacial landform'),), topic='0-11', atlas=GLAC),
          Route('route-ii', 'Route (ii)', ID + 'p2-q1b-route-ii', True,
                prompt=(L(3, '(ii) Describe and explain the factors governing', 'process that you have studied.'),),
                scheme=(S(8, 'Factors identified', 'Annotation'),),
                criteria=(pair('Factors identified · 2 + 2 marks', 'Factors identified'),
                          fixed('Mass movement process named', 2, 'Mass movement process named · 2 marks'),
                          srp('Description/explanation', 12, f'Description/explanation · 12 x {SRPS}')),
                topic='0-8', atlas=RW),
      )),
    T('p2-1c', P2, '1C', '', 30, 3, L(3, 'Seismic Activity'),
      (L(3, 'Explain how the occurrence of earthquakes can be predicted and their effects reduced.'),),
      (S(9, 'Reference to prediction of earthquakes · 2 marks', 'Annotation'),),
      (fixed('Reference to prediction of earthquakes', 2, 'Reference to prediction of earthquakes · 2 marks'),
       fixed('Reference to reducing impacts of earthquakes', 2, 'Reference to reducing impacts of earthquakes · 2 marks'),
       srp('Explanation', 13, f'Explanation · 13 x {SRPS}')),
      '0-7', EV, ID + 'p2-q1c', True),
]

Q2AS = (L(4, 'Examine the photograph above and answer each of the following questions.'),)
PART_TWO += romans('2A', 4, L(4, 'Coastal Landforms'), Q2AS, ID + 'p2-q2a', ('page',), [
    ('(i)', 8, L(4, '(i) Name each of the landforms formed by coastal processes labelled A, B, C and D.'),
     (S(10, '(i) · A = Cliff', '(ii) · Specific processes'),),
     (fixed('A', 2, '(i) · A = Cliff · 2 marks'), fixed('B', 2, 'B = Wave-cut platform · 2 marks'),
      fixed('C', 2, 'C = Cave · 2 marks'), fixed('D', 2, 'D = Sea Stack · 2 marks')), '0-10', SEA),
    ('(ii)', 4, L(4, '(ii) Name two specific processes of coastal erosion.'),
     (S(10, '(ii) · Specific processes', '(iii) Valid explanation'),),
     (pair('(ii) · Specific processes named · 2 + 2 marks', 'Two processes'),), '0-10', SEA),
    ('(iii)', 4, L(4, '(iii) Explain briefly what is meant by constructive waves.'),
     (S(10, '(iii) Valid explanation', '(iv) Valid explanation'),),
     (pair('(iii) Valid explanation · 2 + 2 marks', 'Explanation'),), '0-10', SEA),
    ('(iv)', 4, L(4, '(iv) Explain briefly what is meant by wave refraction.'),
     (S(10, '(iv) Valid explanation', None),), (pair('(iv) Valid explanation · 2 + 2 marks', 'Explanation'),),
     '0-10', SEA),
])

PART_TWO += [
    T('p2-2b', P2, '2B', '', 30, 4, L(4, 'Landscape Development'),
      (L(4, 'Examine how different rock types produce distinctive landscapes', 'that you have studied.'),),
      (S(11, 'Rock 1 and associated landscape named', 'Annotation'),),
      (pair('Rock 1 and associated landscape named · 2 + 2 marks', 'Rock 1 and associated landscape named'),
       pair('Rock 2 and associated landscape named · 2 + 2 marks', 'Rock 2 and associated landscape named'),
       srp('Examination', 11, f'Examination · 11 x {SRPS}')),
      '0-1', RW + KARST, ID + 'p2-q2b', True),
    T('p2-2c', P2, '2C', '', 30, 4, L(4, 'Human Interaction with Surface Processes'),
      (L(4, 'Human activity impacts on surface processes.'),
       L(4, 'Examine this statement with reference to one of the following:', 'mass movement processes.')),
      (S(12, 'Impact on process identified · 2 marks', 'Annotation'),),
      (fixed('Impact on process identified', 2, 'Impact on process identified · 2 marks'),
       srp('Examination', 14, f'Examination · 14 x {SRPS}')),
      '0-6', RIVERS, ID + 'p2-q2c-the-impact-of-flood-control-measur', True,
      routes=bullet_routes('p2-q2c-', IMPACTS, atlas=dict(zip(IMPACTS, (RIVERS, SEA, RW))))),
]

Q3AS = (L(5, 'Examine the map and text above which give information on volcanoes in Indonesia',
          'following questions.'),)
PART_TWO += romans('3A', 5, L(5, 'Volcanoes', nth=0), Q3AS, ID + 'p2-q3a', ('page',), [
    ('(i)', 2, L(5, '(i) Name the volcano closest to Agung on the island of Bali.'),
     (S(13, '(i) Batur', '(ii) · North north east'),), (fixed('Volcano', 2, '(i) Batur · 2 marks'),), '0-7', EV),
    ('(ii)', 4, L(5, '(ii) In what direction is the Australian Plate moving', 'is it moving?'),
     (S(13, '(ii) · North north east', '(iii) · Pyroclastic'),),
     (pair('(ii) · North north east and 70mm/yr. · 2 + 2 marks', 'Direction and speed'),), '0-0', PS),
    ('(iii)', 4, L(5, '(iii) Name two pyroclastic materials that are ejected from a volcano during an eruption.'),
     (S(13, '(iii) · Pyroclastic', '(iv) · Caldera'),),
     (pair('(iii) · Pyroclastic material named · 2 + 2 marks', 'Two pyroclastic materials'),), '0-7', EV),
    ('(iv)', 2, L(5, '(iv) What is the name for a volcanic cone that has collapsed in on itself', 'eruption?'),
     (S(13, '(iv) · Caldera', '(v) · Valid explanation'),), (fixed('Name', 2, '(iv) · Caldera · 2 marks'),),
     '0-7', EV),
    ('(v)', 4, L(5, '(v) Explain briefly what is meant by the process of subduction.'),
     (S(13, '(v) · Valid explanation', '(vi) · Valid explanation'),),
     (pair('(v) · Valid explanation · 2 + 2 marks', 'Explanation'),), '0-0', PS),
    ('(vi)', 4, L(5, '(vi) Explain briefly what is meant by a dormant volcano.'),
     (S(13, '(vi) · Valid explanation', None),), (pair('(vi) · Valid explanation · 2 + 2 marks', 'Explanation'),),
     '0-7', EV),
])

PART_TWO += [
    T('p2-3b', P2, '3B', '', 30, 5, L(5, 'Fluvial Adjustment'),
      (L(5, 'Examine how the landscape is changed when a river adjusts', 'that you have studied.'),),
      (S(14, 'Change in landscape identified · 2 marks', 'Annotation'),),
      (fixed('Change in landscape identified', 2, 'Change in landscape identified · 2 marks'),
       fixed('Example', 2, 'Example · 2 marks'), srp('Examination', 13, f'Examination · 13 x {SRPS}')),
      '0-9', RIVERS, ID + 'p2-q3b', True),
    T('p2-3c', P2, '3C', '', 30, 5, L(5, 'Igneous Rock'),
      (L(5, 'Explain the formation of two igneous rocks, with reference to Irish examples.'),),
      (S(15, 'Two Irish igneous rocks named', 'Annotation'),),
      (pair('Two Irish igneous rocks named · 2 + 2 marks', 'Two Irish igneous rocks named'),
       split('Explanation of formation of the two rocks (6/7 SRPs each)', 13,
             f'Explanation of formation of rock 1 · 6/7 x {SRPS}', f'Explanation of formation of rock 2 · 6/7 x {SRPS}')),
      '0-1', RW, ID + 'p2-q3c', True),
    # Question 4
    T('p2-4a', P2, '4A', '', 20, 6, L(6, 'Map Skills'),
      (L(6, 'Draw an outline map of a Continental / Sub-Continental region (not in Europe)', 'The course of a named river.'),),
      (S(16, 'Map outline', None),),
      sketch('Map outline · 4 marks graded (4/2/0)', (0, 2, 4),
             ('4 features @ 4 marks each', 'Named 2 marks'), sums((0, 1, 2), (0, 2)), 4),
      '1-6', CONT, ID + 'p2-q4a', True,
      row_labels=(None, L(6, 'The outline of a named feature of relief (upland or lowland)'),
                  L(6, 'A named urban centre'), L(6, 'The outline of a named agricultural or industrial region'),
                  L(6, 'The course of a named river.'))),
    T('p2-4b', P2, '4B', '', 30, 6, L(6, 'Secondary Economic Activity'),
      (L(6, 'Explain any two factors that have influenced the development of secondary economic',
         'that you have studied.'),),
      (S(17, 'Factors identified · 2 + 2 marks', 'Annotation'),),
      (pair('Factors identified · 2 + 2 marks', 'Factors identified'),
       split('Explanation of the two factors (6/7 SRPs each)', 13,
             f'Explanation of Factor 1 · 6/7 x {SRPS}', f'Explanation of Factor 2 · 6/7 x {SRPS}')),
      '1-4', IRL, ID + 'p2-q4b', True),
    T('p2-4c', P2, '4C', '', 30, 6, L(6, 'The European Union'),
      (L(6, 'Explain each of the following challenges currently facing the European Union:', 'Economic challenges.'),),
      (S(18, 'Social challenge identified · 2 marks', 'Annotation'),),
      (fixed('Social challenge identified', 2, 'Social challenge identified · 2 marks'),
       fixed('Economic challenge identified', 2, 'Economic challenge identified · 2 marks'),
       split('Explanation of the two challenges (6/7 SRPs each)', 13,
             f'Explanation of social challenges · 6/7 x {SRPS}', f'Explanation of economic challenges · 6/7 x {SRPS}')),
      '1-5', EURO, ID + 'p2-q4c', True),
]

Q5AS = (L(7, 'Examine the table above showing the number of vessels in the European Union (EU) fishing',
          'following questions.'),)
PART_TWO += romans('5A', 7, L(7, 'Fishing in the European Union'), Q5AS, ID + 'p2-q5a', ('page',), [
    ('(i)', 2, L(7, '(i) Which single country from the table above had the highest percentage share', 'in 2017?'),
     (S(19, '(i) · Greece', '(ii) · Netherlands'),), (fixed('Country', 2, '(i) · Greece · 2 marks'),), '2-0', TG),
    ('(ii)', 2, L(7, '(ii) Which single country from the table above had an increase in its fleet', '2008 and 2017?'),
     (S(19, '(ii) · Netherlands', '(iii) · 15.93'),), (fixed('Country', 2, '(ii) · Netherlands · 2 marks'),),
     '2-0', TG),
    ('(iii)', 4, L(7, '(iii) What was Italy’s percentage share of the EU fishing fleet in 2008?'),
     (S(19, '(iii) · 15.93', '(iv) Irish fishing port'),), (fixed('Percentage', 4, '(iii) · 15.93 (%) · 4 marks'),),
     '2-0', TG),
    ('(iv)', 4, L(7, '(iv) Name two Irish fishing ports.'),
     (S(19, '(iv) Irish fishing port', '(v) · Valid explanation'),),
     (pair('(iv) Irish fishing port named · 2 + 2 marks', 'Two fishing ports'),), '1-4', IRL),
    ('(v)', 8, L(7, '(v) Briefly explain two reasons why there was a decrease in the number of fishing vessels',
                 '2008 and 2017.'),
     (S(19, '(v) · Valid explanation', None),),
     (pair('(v) · Valid explanation · 2 + 2 marks', 'First reason'), pair('=2 + 2 marks', 'Second reason')),
     '1-5', EURO),
])

PART_TWO += [
    T('p2-5b', P2, '5B', '', 30, 7, L(7, 'Tertiary Economic Activity'),
      (L(7, 'Examine two factors that have influenced the development of tourism', 'that you have studied.'),),
      (S(20, 'Factors identified · 2 + 2 marks', 'Annotation'),),
      (pair('Factors identified · 2 + 2 marks', 'Factors identified'),
       split('Examination of the two factors (7/6 SRPs each)', 13,
             f'Examination of Factor 1 · 7/6 x {SRPS}', f'Examination of Factor 2 · 7/6 x {SRPS}')),
      '1-6', CONT, ID + 'p2-q5b', True),
    T('p2-5c', P2, '5C', '', 30, 7, L(7, 'Urban Development'),
      (L(7, 'Discuss the factors which influenced the development of one urban area', 'that you have studied.'),),
      (S(21, 'Urban area named · 2m', 'Annotation'),),
      (fixed('Urban area named', 2, 'Urban area named · 2m'), pair('Factors identified · 2m + 2m', 'Factors identified'),
       srp('Discussion', 12, f'Discussion · 12 x {SRPS}')),
      '1-5', EURO + URB, ID + 'p2-q5c', True),
]

Q6AS = (L(8, 'Examine the information above and answer each of the following questions.'),)
PART_TWO += romans('6A', 8, L(8, 'Disposable Income of Irish Regions'), Q6AS, ID + 'p2-q6a', ('page',), [
    ('(i)', 4, L(8, '(i) What was the average disposable income (in €) for the South West region', 'in 2017?'),
     (S(23, '(i) · (€) 19,040', '(ii) · 7'),),
     (fixed('2016', 2, '(i) · (€) 19,040 – 2016 · 2 marks'), fixed('2017', 2, '(€) 19,893 – 2017 · 2 marks')),
     '2-0', TG),
    ('(ii)', 2, L(8, '(ii) How many regions had an average disposable income below the state average', '2016?'),
     (S(23, '(ii) · 7', '(iii) · (€) 2,202'),), (fixed('Number of regions', 2, '(ii) · 7 · 2 marks'),), '2-0', TG),
    ('(iii)', 4, L(8, '(iii) Calculate the difference between the average disposable income in the Midlands',
                   '2016 and 2017.'),
     (S(23, '(iii) · (€) 2,202', '(iv) · Border'),), (fixed('Difference', 4, '(iii) · (€) 2,202 · 4 marks'),),
     '2-0', TG),
    ('(iv)', 2, L(8, '(iv) Which region had the lowest average disposable income in both 2016 and 2017?'),
     (S(23, '(iv) · Border', '(v) · Valid explanation'),), (fixed('Region', 2, '(iv) · Border · 2 marks'),),
     '2-0', TG),
    ('(v)', 4, L(8, '(v) Explain briefly one reason why the Dublin region had the highest disposable income',
                 'the State.'),
     (S(23, '(v) · Valid explanation', '(vi) · Valid explanation'),),
     (pair('(v) · Valid explanation · 2 + 2 marks', 'Reason'),), '1-4', IRL),
    ('(vi)', 4, L(8, '(vi) Explain briefly one way that investment in Ireland’s transport infrastructure',
                  'regional incomes.'),
     (S(23, '(vi) · Valid explanation', '6B.'),),
     (pair('(vi) · Valid explanation · 2 + 2 marks', 'Way'),), '1-4', IRL),
])

FACTORS_6B = ('Relief', 'Climate', 'Markets.')
FACTORS_6C = ('Population dynamics', 'Language', 'Religion', 'Urban development', 'Rural development')
PART_TWO += [
    T('p2-6b', P2, '6B', '', 30, 9, L(9, 'Primary Economic Activity – Agriculture'),
      (L(9, 'Account for the development of agriculture in a European region', 'Markets.'),),
      (S(23, 'Account of Factor 1', 'Annotation'),),
      (split('Account of the two factors (8/7 SRPs each)', 15,
             f'Account of Factor 1 · 8/7 x {SRPS}', f'Account of Factor 2 · 8/7 x {SRPS}'),),
      '1-5', EURO, *pool(ID + 'p2-q6b-', FACTORS_6B, 2)[:1], True, absorbs=pool(ID + 'p2-q6b-', FACTORS_6B, 2)[1]),
    # The tabled pool keeps the bare 6C id it shipped with; every combination id aliases to it.
    T('p2-6c', P2, '6C', '', 30, 9, L(9, 'The Dynamics of Regions – Human Processes'),
      (Lift(9, 'Population dynamics', 'Rural development', row=True),
       L(9, 'Examine the impact of any two of the factors listed in the table above', 'that you have studied.')),
      (S(24, 'Process 1', 'Annotation'),),
      (fixed('Process 1 impact identified', 2, ('Process 1', '=Impact identified · 2 marks@0')),
       fixed('Process 2 impact identified', 2, ('Process 2', '=Impact identified · 2 marks@1')),
       srp('Examination of the two processes (7/6 SRPs each)', 13,
           ('=Examination · 7/6 x SRPs@0', '=Examination · 7/6 x SRPs@1'))),
      '1-6', CONT, ID + 'p2-q6c', True, absorbs=pool(ID + 'p2-q6c-', FACTORS_6C, 2)[1]),
]

ECON = (H + 'elective-economic',)
DEV = (H + 'economic-developing-economies',)
MNC = (H + 'economic-multinationals-globalisation',)
EU_ECON = (H + 'economic-european-union',)
ENERGY = (H + 'economic-energy',)
HEADINGS_7B = ('The product life cycle', 'Corporate strategies influencing the opening and closure of branch plants',
               'Developments in information technology.')
PART_TWO += [
    # Question 7
    T('p2-7a', P2, '7A', '', 20, 11, L(11, 'Aerial Photograph'),
      (L(11, 'Examine the aerial photograph of Foxford accompanying this paper.', 'in the right background.'),),
      (S(26, 'Sketch Outline', None),), AERIAL_SKETCH, '2-8', AER, ID + 'p2-q7a', False, ('aerial',),
      row_labels=(None, L(11, 'The river'), L(11, 'Two connecting streets'), L(11, 'An industrial building'),
                  L(11, 'An area of waste ground in the right background.'))),
    T('p2-7b', P2, '7B', '', 30, 11, L(11, 'Multinational Company'),
      (L(11, 'Examine the impact of any two of the following on one multinational company', 'information technology.'),),
      (S(27, 'MNC named · 2 marks', 'Annotation'),),
      (fixed('MNC named', 2, 'MNC named · 2 marks'),
       fixed('Impact identified for heading 1', 2, 'Impact identified for factor/heading 1 · 2 marks'),
       srp('Examination of heading 1', 6, 'Examination of factor/heading 1 · 6 x SRPs'),
       fixed('Impact identified for heading 2', 2, 'Impact identified for factor/heading 2 · 2 marks'),
       srp('Examination of heading 2', 6, 'Examination of factor/heading 2 · 6 x SRPs')),
      '3-2', MNC, *pool(ID + 'p2-q7b-', HEADINGS_7B, 2)[:1], True, absorbs=pool(ID + 'p2-q7b-', HEADINGS_7B, 2)[1]),
    T('p2-7c', P2, '7C', '', 30, 11, L(11, 'Renewable Energy'),
      (L(11, 'Examine how the development of renewable energy is crucial for both of the following:',
         'Ireland’s economy.'),),
      (S(28, 'Importance for Ireland’s environment identified · 2 marks', 'Annotation'),),
      (fixed('Importance for Ireland’s environment identified', 2,
             'Importance for Ireland’s environment identified · 2 marks'),
       fixed('Importance for Ireland’s economy identified', 2, 'Importance for Ireland’s economy identified · 2 marks'),
       split('Examination of environment and economy (6/7 SRPs each)', 13,
             f'Examination of Ireland’s environment · 6/7 x {SRPS}', f'Examination of Ireland’s economy · 6/7 x {SRPS}')),
      '3-5', ENERGY, ID + 'p2-q7c', True),
]

Q8AS = (L(12, 'Examine the bar chart above showing the value of European Union (EU) trade', 'following questions.'),)
PART_TWO += romans('8A', 12, L(12, 'International Trade'), Q8AS, ID + 'p2-q8a', ('page',), [
    ('(i)', 2, L(12, '(i) Which of the selected countries above received the highest value of exports', 'in 2018?'),
     (S(29, '(i) · China', '(ii) · Russia'),), (fixed('Country', 2, '(i) · China · 2 marks'),), '2-0', TG),
    ('(ii)', 2, L(12, '(ii) From which of the selected countries above did the EU receive the lowest value',
                  'in 2018?'),
     (S(29, '(ii) · Russia', '(iii) (€)5,698'),), (fixed('Country', 2, '(ii) · Russia · 2 marks'),), '2-0', TG),
    ('(iii)', 4, L(12, '(iii) Calculate the total value of imports into the EU in 2018', 'bar chart above.'),
     (S(29, '(iii) (€)5,698', '(iv) China/South'),), (fixed('Total', 4, '(iii) (€)5,698 (billion) · 4 marks'),),
     '2-0', TG),
    ('(iv)', 2, L(12, '(iv) Name one country that the EU had a trade surplus with in 2018.'),
     (S(29, '(iv) China/South', '(v) · Canada'),), (fixed('Country', 2, '(iv) China/South Korea/Russia · 2 marks'),),
     '2-0', TG),
    ('(v)', 2, L(12, '(v) Name one country that the EU had a trade deficit with in 2018.'),
     (S(29, '(v) · Canada', '(vi) Valid explanation'),), (fixed('Country', 2, '(v) · Canada/USA/Japan · 2 marks'),),
     '2-0', TG),
    ('(vi)', 4, L(12, '(vi) Explain briefly one disadvantage of having a trade deficit.'),
     (S(29, '(vi) Valid explanation', '(vii) Valid explanation'),),
     (pair('(vi) Valid explanation · 2 + 2 marks', 'Disadvantage'),), '3-3', EU_ECON),
    ('(vii)', 4, L(12, '(vii) Explain briefly one advantage of having a large number of export partners.'),
     (S(29, '(vii) Valid explanation', None),), (pair('(vii) Valid explanation · 2 + 2 marks', 'Advantage'),),
     '3-3', EU_ECON),
])

PART_TWO.append(T(
    'p2-8b', P2, '8B', '', 30, 12, L(12, 'Colonialism'),
    (L(12, 'Examine the challenges resulting from colonialism faced by a developing economy', 'studied.'),),
    (S(30, 'Challenges identified · 2 + 2 marks', 'Annotation'),),
    (pair('Challenges identified · 2 + 2 marks', 'Challenges identified'),
     fixed('Developing economy named', 2, 'Developing economy named · 2 marks'),
     srp('Examination', 12, f'Examination · 12 x {SRPS}')),
    '3-1', DEV, ID + 'p2-q8b', True))

REASON = ('For each reason: Reason stated · 2 marks', 'Map evidence · 2 marks', f'Explanation · 3 x {SRPS}')
Q8CS = (L(13, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper and',
          'following questions.'),)
PART_TWO += romans('8C', 13, L(13, 'Location of Economic Activity'), Q8CS, ID + 'p2-q8c', ('map', 'legend'), [
    ('(i)', 20, L(13, '(i) Explain two reasons why a multinational company might choose to locate', 'support each reason.'),
     (S(31, '(i) · 2 x reasons', '(ii) · 1 x reason'), S(31, 'For each reason:', 'Annotation')),
     tuple(Criterion(f'Reason {n}', 10, evens(10), 'srp', ('(i) · 2 x reasons @ 10 marks each.', *REASON))
           for n in (1, 2)), '3-2', MNC + MAP),
    ('(ii)', 10, L(13, '(ii) Using evidence from the Ordnance Survey map, explain one reason', 'in this area.'),
     (S(31, '(ii) · 1 x reason', 'For each reason:'), S(31, 'For each reason:', 'Annotation')),
     (Criterion('Reason', 10, evens(10), 'srp', ('(ii) · 1 x reason @ 10 marks.', *REASON)),), '3-2', MNC + MAP),
], legacy_first=False)

Q9AS = (L(14, 'Examine the data above showing the breakdown of tourist accommodation', 'following questions.'),)
PART_TWO += romans('9A', 14, L(14, 'Economic Activity'), Q9AS, ID + 'p2-q9a', ('page',), [
    ('(i)', 16, L(14, '(i) Using graph paper, draw a suitable graph to illustrate this data.'),
     (S(32, 'Bar Chart · Pie Chart', 'Annotation'),), GRAPH, '2-0', TG),
    ('(ii)', 4, L(14, '(ii) Explain briefly one reason why Ireland is a popular destination for tourists.'),
     (S(33, 'Any valid brief explanation · 2 + 2 marks', '9B.'),),
     (pair('Any valid brief explanation · 2 + 2 marks', 'Reason'),), '3-0', ECON),
])

PART_TWO += [
    T('p2-9b', P2, '9B', '', 30, 14, L(14, 'European Union Policy'),
      (L(14, 'Examine the impact of European Union policy on the development of primary economic',
         'activity in Ireland.'),),
      (S(33, 'Impact on primary activity identified', 'Annotation'),),
      (fixed('Impact on primary activity identified', 2, 'Impact on primary activity identified · 2 marks'),
       srp('Examination', 14, 'Examination · 14 x SRPs')),
      '3-3', EU_ECON, ID + 'p2-q9b', True),
    T('p2-9c', P2, '9C', '', 30, 14, L(14, 'Conflict of Interest'),
      (L(14, 'Examine how conflict may arise between the exploitation of natural resources', 'that you have studied.'),),
      (S(34, 'Example named · 2m', 'Annotation'),),
      (fixed('Example named', 2, 'Example named · 2m'), srp('Examination', 14, f'Examination · 14 x {SRPS}')),
      '3-4', ENV, ID + 'p2-q9c', True),
    # Question 10
    T('p2-10a', P2, '10A', '', 20, 15, L(15, 'Aerial Photograph'),
      (L(15, 'Examine the aerial photograph of Foxford accompanying this paper.', 'An off-street car park.'),),
      (S(35, 'Sketch Outline', None),), AERIAL_SKETCH, '2-8', AER + URB, ID + 'p2-q10a', False, ('aerial',),
      row_labels=(None, L(15, 'The river'), L(15, 'A sports field in the right background'), L(15, 'A church'),
                  L(15, 'An off-street car park.'))),
    T('p2-10b', P2, '10B', '', 30, 15, L(15, 'Dynamics of Population'),
      (L(15, 'Examine how changing fertility and mortality rates impact on population structure',
         'that you have studied.'),),
      (S(36, 'Impact of changing fertility rates identified', 'Annotation'),),
      (fixed('Impact of changing fertility rates identified', 2, 'Impact of changing fertility rates identified · 2 marks'),
       fixed('Impact of changing mortality rates identified', 2, 'Impact of changing mortality rates identified · 2 marks'),
       fixed('Example of where impacts occur', 2, 'Example of where impacts occur · 2 marks'),
       srp('Examination', 12, f'Examination · 12 x {SRPS}')),
      '4-0', POP, ID + 'p2-q10b', True),
    T('p2-10c', P2, '10C', '', 30, 15, L(15, 'Migration'),
      (L(15, 'With reference to a developed region that you have studied, explain the impact of migration',
         'Urban areas.'),),
      (S(37, 'Impact on rural region identified · 2 marks', 'Annotation'),),
      (fixed('Impact on rural region identified', 2, 'Impact on rural region identified · 2 marks'),
       srp('Explanation of impact on rural region', 6, f'Explanation of impact on rural region · 6 x {SRPS}'),
       fixed('Impact on urban region identified', 2, 'Impact on urban region identified · 2 marks'),
       srp('Explanation of impact on urban region', 6, f'Explanation of impact on urban region · 6 x {SRPS}'),
       fixed('Example of a developed region', 2, 'Example of a developed region · 2 marks')),
      '4-2', POP, ID + 'p2-q10c', True),
]

Q11AS = (L(16, 'Examine the graph above showing the components of population change', 'following questions.'),)
PART_TWO += romans('11A', 16, L(16, 'Population Change in Ireland'), Q11AS, ID + 'p2-q11a', ('page',), [
    ('(i)', 2, L(16, '(i) State whether the following statement is true or false:', 'than 50,000 people.'),
     (S(38, '(i) · True', '(ii) · Natural Increase'),), (fixed('True or false', 2, '(i) · True · 2 marks'),),
     '2-0', TG),
    ('(ii)', 2, L(16, '(ii) Was the main cause of population growth in the 2011-2016', 'net migration?'),
     (S(38, '(ii) · Natural Increase', '(iii) 1986-1991'),), (fixed('Main cause', 2, '(ii) · Natural Increase · 2 marks'),),
     '2-0', TG),
    ('(iii)', 2, L(16, '(iii) During which inter-censal period was there a population decrease?'),
     (S(38, '(iii) 1986-1991', '(iv) 1981-1986'),), (fixed('Period', 2, '(iii) 1986-1991 · 2 marks'),), '2-0', TG),
    ('(iv)', 4, L(16, '(iv) List two inter-censal periods when emigration was greater than immigration.'),
     (S(38, '(iv) 1981-1986', '(v) · 1991-1996'),),
     (pair('(iv) 1981-1986/1986-1991/2011-2016 · 2 + 2 marks', 'Two periods'),), '2-0', TG),
    ('(v)', 2, L(16, '(v) Which inter-censal period had the smallest natural increase?'),
     (S(38, '(v) · 1991-1996', '(vi) Valid explanation'),), (fixed('Period', 2, '(v) · 1991-1996 · 2 marks'),),
     '2-0', TG),
    ('(vi)', 4, L(16, '(vi) Explain briefly the term natural change.'),
     (S(38, '(vi) Valid explanation', '(vii) Valid explanation'),),
     (pair('(vi) Valid explanation · 2 + 2 marks', 'Explanation'),), '4-0', POP),
    ('(vii)', 4, L(16, '(vii) Explain briefly one reason why birth rates decrease.'),
     (S(38, '(vii) Valid explanation', None),), (pair('(vii) Valid explanation · 2 + 2 marks', 'Reason'),),
     '4-0', POP),
])

URBAN_REASON = ('Three reasons @ 10 marks each', 'For each reason:', 'Reason stated · 2 marks',
                'OS map evidence · 2 marks', 'Explanation · 3 x SRPs')
PART_TWO += [
    T('p2-11b', P2, '11B', '', 30, 17, L(17, 'Urban Problems – Developing World City'),
      (L(17, 'Discuss how the growth of urban centres can lead to both of the following problems', 'Urban sprawl.'),),
      (S(39, 'Example of urban centre · 2 marks', 'Annotation'),),
      (fixed('Example of urban centre', 2, 'Example of urban centre · 2 marks'),
       srp('Discussion of traffic congestion', 7, 'Discussion of traffic congestion · 7 x SRPs'),
       srp('Discussion of urban sprawl', 7, 'Discussion of urban sprawl · 7 x SRPs')),
      '4-5', URB, ID + 'p2-q11b', True),
    T('p2-11c', P2, '11C', '', 30, 17, L(17, 'Urban Settlement'),
      (L(17, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper.'),
       L(17, 'Explain three reasons why the town of Foxford developed at its present location.', 'support each reason.')),
      (S(40, 'Three reasons @ 10 marks each', 'Annotation'),),
      tuple(Criterion(f'Reason {n}', 10, evens(10), 'srp', URBAN_REASON) for n in (1, 2, 3)),
      '4-3', URB + MAP, ID + 'p2-q11c', False, ('map', 'legend')),
]

Q12AS = (L(18, 'Examine the data above showing population density in Ireland', 'following questions.'),)
PART_TWO += romans('12A', 18, L(18, 'Population Dynamics'), Q12AS, ID + 'p2-q12a', ('page',), [
    ('(i)', 16, L(18, '(i) Using graph paper, draw a suitable graph to illustrate this data.'),
     (S(41, 'Bar Chart · Pie Chart', 'Annotation'),), GRAPH, '2-0', TG),
    ('(ii)', 4, L(18, '(ii) Explain briefly one reason why the population density in Ireland is rising.'),
     (S(41, 'Any valid brief explanation · 2 + 2 marks', None),),
     (pair('Any valid brief explanation · 2 + 2 marks', 'Reason'),), '4-0', POP),
])

PART_TWO += [
    T('p2-12b', P2, '12B', '', 30, 18, L(18, 'Urban Land-Use'),
      (L(18, 'Describe and explain the land-use zones in any city that you have studied.'),),
      (S(42, 'Land-use zones identified', 'Annotation'),),
      (pair('Land-use zones identified · 2 + 2 marks', 'Land-use zones identified'),
       fixed('City named', 2, 'City named · 2 marks'),
       srp('Description/explanation', 12, f'Description/explanation · 12 x {SRPS}')),
      '4-4', (H + 'urban-land-uses',) + URB, ID + 'p2-q12b', True),
    T('p2-12c', P2, '12C', '', 30, 18, L(18, 'Overpopulation'),
      (L(18, 'Examine two causes of overpopulation, with reference to an example(s)', 'studied.'),),
      (S(43, 'Cause 1 identified', 'Annotation'),),
      (fixed('Cause 1 identified', 2, 'Cause 1 identified · 2 marks'),
       srp('Examination of cause 1', 6, f'Examination of cause 1 · 6 x {SRPS}'),
       fixed('Cause 2 identified', 2, 'Cause 2 identified · 2 marks'),
       srp('Examination of cause 2', 6, f'Examination of cause 2 · 6 x {SRPS}'),
       fixed('Example', 2, 'Example · 2 marks')),
      '4-1', POP, ID + 'p2-q12c', True),
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
    option('13', 20, L(20, 'Global Interdependence'), 0,
           L(20, 'We live in an interdependent global economy.', 'desertification and deforestation.'), 47, '5-1', GI),
    option('14', 20, L(20, 'Global Interdependence'), 0,
           L(20, 'Sustainability is a model for future human and economic development.', 'Self-reliance.'),
           48, '5-3', GI, after='14.', end='15.',
           choice=pool(ID + 'p2-q14-', ('Resource use', 'Fair trade', 'Justice issues', 'Self-reliance.'), 3)),
    option('15', 20, L(20, 'Global Interdependence'), 0,
           L(20, 'Views of development and underdevelopment are subject to change.', 'Discuss.'), 48, '5-0', GI,
           after='15.'),
    option('16', 20, L(20, 'Geoecology'), 1,
           L(20, 'Various soil patterns have developed because of the action', 'Discuss.'), 49, '6-1', GE),
    option('17', 20, L(20, 'Geoecology'), 1,
           L(20, 'Discuss how soil development is influenced by any three of the following factors:', 'Organic matter.'),
           50, '6-0', GE, after='17.', end='18.',
           choice=pool(ID + 'p2-q17-', ('Mineral matter', 'Air', 'Water', 'Organic matter.'), 3)),
    option('18', 20, L(20, 'Geoecology'), 1,
           L(20, 'Examine how each of the following activities impact on biomes:', 'Industrial development.'),
           50, '6-3', GE, after='18.'),
    option('19', 21, L(21, 'Culture and Identity'), 0,
           L(21, 'Examine how conflict can arise between political structures and cultural groups.'), 51, '7-1', CI,
           after='19.', end='20.'),
    option('20', 21, L(21, 'Culture and Identity'), 0,
           L(21, 'Examine the importance of language as a cultural indicator.'), 51, '7-0', CI, after='20.'),
    option('21', 21, L(21, 'Culture and Identity'), 0,
           L(21, 'Examine how people express their culture and identity in everyday life', 'that you have studied.'),
           52, '7-2', CI),
    option('22', 21, L(21, 'The Atmosphere – Ocean Environment'), 1,
           L(21, 'Examine the uneven distribution of temperature over the earth’s surface.'), 53, '8-1', AO),
    option('23', 21, L(21, 'The Atmosphere – Ocean Environment'), 1,
           L(21, 'Exchanges of water between oceans and atmosphere', 'Discuss.'), 54, '8-2', AO,
           after='23.', end='24.'),
    option('24', 21, L(21, 'The Atmosphere – Ocean Environment'), 1,
           L(21, 'Describe and account for the characteristics of one global climate type', 'studied.'), 54, '8-4', AO,
           after='24.'),
]

TASKS = [*PART_ONE, *PART_TWO, *OPTIONS]

ID_CORRECTION_REASON = (
    'The shipped card held every part of a question the scheme prices part by '
    'part. Its id is kept on the first separately priced part; the other parts '
    'are new cards with their own published allocation.')

# Every 2021 Higher card id live on origin/main before this review (75). Each must survive.
LEGACY_IDS = [
    'geography-2021-hl-p1-q2',
    'geography-2021-hl-p1-q3',
    'geography-2021-hl-p1-q4',
    'geography-2021-hl-p1-q5',
    'geography-2021-hl-p1-q6',
    'geography-2021-hl-p1-q10',
    'geography-2021-hl-p1-q11',
    'geography-2021-hl-p1-q12',
    'geography-2021-hl-p2-q1b-route-i-fluvial-landform',
    'geography-2021-hl-p2-q1b-route-i-coastal-landform',
    'geography-2021-hl-p2-q1b-route-i-glacial-landform',
    'geography-2021-hl-p2-q1b-route-ii',
    'geography-2021-hl-p2-q1c',
    'geography-2021-hl-p2-q2a',
    'geography-2021-hl-p2-q2b',
    'geography-2021-hl-p2-q2c-the-impact-of-flood-control-measur',
    'geography-2021-hl-p2-q2c-the-impact-of-coastal-defence-meas',
    'geography-2021-hl-p2-q2c-the-impact-of-human-activities-on',
    'geography-2021-hl-p2-q3a',
    'geography-2021-hl-p2-q3b',
    'geography-2021-hl-p2-q3c',
    'geography-2021-hl-p2-q4a',
    'geography-2021-hl-p2-q4b',
    'geography-2021-hl-p2-q4c',
    'geography-2021-hl-p2-q5a',
    'geography-2021-hl-p2-q5b',
    'geography-2021-hl-p2-q5c',
    'geography-2021-hl-p2-q6a',
    'geography-2021-hl-p2-q6b-relief-climate',
    'geography-2021-hl-p2-q6b-relief-markets',
    'geography-2021-hl-p2-q6b-climate-markets',
    'geography-2021-hl-p2-q6c',
    'geography-2021-hl-p2-q6c-population-dynamics-religion',
    'geography-2021-hl-p2-q6c-population-dynamics-urban-development',
    'geography-2021-hl-p2-q6c-population-dynamics-rural-development',
    'geography-2021-hl-p2-q6c-language-religion',
    'geography-2021-hl-p2-q6c-language-urban-development',
    'geography-2021-hl-p2-q6c-language-rural-development',
    'geography-2021-hl-p2-q6c-religion-urban-development',
    'geography-2021-hl-p2-q6c-religion-rural-development',
    'geography-2021-hl-p2-q6c-urban-development-rural-development',
    'geography-2021-hl-p2-q7b-the-product-life-cycle-corporate-strategies-influencing-t',
    'geography-2021-hl-p2-q7b-the-product-life-cycle-developments-in-information-techno',
    'geography-2021-hl-p2-q7b-corporate-strategies-influencing-t-developments-in-information-techno',
    'geography-2021-hl-p2-q7c',
    'geography-2021-hl-p2-q8a',
    'geography-2021-hl-p2-q8b',
    'geography-2021-hl-p2-q9a',
    'geography-2021-hl-p2-q9b',
    'geography-2021-hl-p2-q9c',
    'geography-2021-hl-p2-q10b',
    'geography-2021-hl-p2-q10c',
    'geography-2021-hl-p2-q11a',
    'geography-2021-hl-p2-q11b',
    'geography-2021-hl-p2-q12a',
    'geography-2021-hl-p2-q12b',
    'geography-2021-hl-p2-q12c',
    'geography-2021-hl-p2-q13',
    'geography-2021-hl-p2-q14-resource-use-fair-trade-justice-issues',
    'geography-2021-hl-p2-q14-resource-use-fair-trade-self-reliance',
    'geography-2021-hl-p2-q14-resource-use-justice-issues-self-reliance',
    'geography-2021-hl-p2-q14-fair-trade-justice-issues-self-reliance',
    'geography-2021-hl-p2-q15',
    'geography-2021-hl-p2-q16',
    'geography-2021-hl-p2-q17-mineral-matter-air-water',
    'geography-2021-hl-p2-q17-mineral-matter-air-organic-matter',
    'geography-2021-hl-p2-q17-mineral-matter-water-organic-matter',
    'geography-2021-hl-p2-q17-air-water-organic-matter',
    'geography-2021-hl-p2-q18',
    'geography-2021-hl-p2-q19',
    'geography-2021-hl-p2-q20',
    'geography-2021-hl-p2-q21',
    'geography-2021-hl-p2-q22',
    'geography-2021-hl-p2-q23',
    'geography-2021-hl-p2-q24',
]
