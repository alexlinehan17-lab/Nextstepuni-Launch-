"""Independent review ledger: Leaving Certificate Geography 2022 Higher Level.

Sources (English editions, Paper Trail index; sizes and SHA-256 pinned in
EXPECTED_SOURCES and the generated audit): Part One and Answerbook
LC005ALP042EV (48 pages), Part Two LC005ALP043EV (20 pages), marking scheme
LC005ALP000EV (64 pages), and the common companions in the harvested corpus —
the 1:50 000 Clonmel map LC005CLP003EV, its legend LC005CLPC00EV and the
Clonmel aerial photograph LC005CLP004EV. In 2022 the SEC publishes both the
legend and the aerial photograph only as JPEGs.

Visual sweep (every page rendered and read on 2026-10-12):
  Part One booklet p1 cover (2022: Part One 80 marks, Part Two 240); p2
  instructions (Part One "Attempt any TEN"; Part Two "attempt THREE", not
  all from one section); p3-p14 Questions 1-12 (Q4 prints its own OS map
  extract, Q7 its elevation profile, Q8 its street map); p15 Part Two
  answerbook instructions; p16-p19 graph paper; p20-p47 lined answer pages;
  p48 back.
  Part Two booklet p1 cover; p2 Part Two instructions; p3-p9 Sections 1-2
  (Q1-Q6); p10 Section 3 divider; p11-p16 Electives (Q7-Q12); p17 Section 4
  divider and note; p18-p19 Options (Q13-Q24); p20 copyright and back.
  Scheme p1 cover; p2-p3 notes and annotation key; p4 Part One table (two
  columns: Q1-Q6, Q7-Q12); p5 the 2022 Part Two adjustment rule; p6-p24
  Q1-Q6; p25 divider; p26-p43 Q7-Q12; p44 divider; p45 option outline and
  Overall Coherence descriptors; p46 option annotations; p47-p54 Q13-Q24;
  p55-p58 Geographical Investigation (coursework); p59 investigation topics;
  p60 Irish-language bonus marks; p61-p63 blank; p64 back cover.
  Companions: Clonmel map extract (the River Suir, the N24, the Waterford
  Cycling Trails); OS Discovery Series legend sheet; oblique aerial
  photograph of Clonmel.

Companions. Part One Q6 (map, legend), Q7 (page, map, legend) and Q8 (page,
aerial); Part Two 1A, 7A, 8C and 12C (map, legend) and 10A (aerial) were held
back before this review because their companions were not wired. Each now
carries the exact official documents it names.

Boundaries and tariffs follow the 2023 Higher ledger: every part the scheme
prices separately is a task; a matching table under one printed instruction
is one task with a criterion per scheme row, the scheme listing its answers
in the printed row order: Q1 Asthenosphere=D, Inner core=F, Oceanic
crust=B, Lithosphere=C, Continental crust=A, Outer core=E; Q2 prints (i) and
(ii) in one table: (i) Tear/Transform=B, Normal=C, Thrust=A and (ii)
Shearing, Tension, Compression (each column read with its own clip); Q4
Blowhole=B, Meander=C, V-shaped valley=D, Beach=A; Q8 Bridge, Church, Sports
pitch, Shopping Centre (Vacant yard is printed); Q9 (i) Geomorphological,
Cultural, Administrative, Peripheral and (ii) A, C, D, B down the printed
descriptions. Q10 prints four romans the scheme prices 2 marks each, so each
is a task.

Glyphs: the 2022 papers print their ticks in Wingdings 2 (U+F050) and set a
Symbol-font space after some bullets; geography_review.GLYPHS maps both to
their printed meaning.
"""

import itertools

from geography_review import (
    Criterion, Lift, Route, SchemeSlice, Task, pool, evens, fixed, slug, srp, sums, upto,
)

YEAR = 2022
LEVEL = 'higher'
PAPER_PAGES = {1: 48, 2: 20}
SCHEME_PAGES = 64
QUESTION_TARIFFS = {1: {str(n): 8 for n in range(1, 13)},
                    2: {**{f'{n}{x}': (20 if x == 'A' else 30)
                           for n in range(1, 13) for x in 'ABC'},
                        **{str(n): 80 for n in range(13, 25)}}}

EXPECTED_SOURCES = {
    'paper1': ('LC005ALP042EV.pdf', 3979853),
    'paper2': ('LC005ALP043EV.pdf', 1534633),
    'scheme': ('LC005ALP000EV.pdf', 1037022),
    'map': ('LC005CLP003EV.pdf', 5462059),
    'legend': ('LC005CLPC00EV.jpg', 4251010),
    'aerial': ('LC005CLP004EV.jpg', 5185646),
}

PAGE_REVIEW = {
    'paper1': {1: 'cover', 2: 'instructions', **{p: 'question' for p in range(3, 15)},
               15: 'answerbook instructions', **{p: 'graph-paper answer page' for p in range(16, 20)},
               **{p: 'lined answer page' for p in range(20, 48)}, 48: 'copyright/back cover'},
    'paper2': {1: 'cover', 2: 'Part Two instructions',
               **{p: 'question' for p in (3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 18, 19)},
               10: 'section divider', 17: 'section divider and option note',
               20: 'copyright/back cover'},
    'scheme': {1: 'cover', 2: 'notes', 3: 'notes and annotation key', 4: 'Part One table',
               5: 'Part Two adjustment rule (2022 additional choice)',
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
    [1, 5, 'one of the following'],
    [2, 2, 'attempt three'], [2, 2, 'choose'], [2, 2, 'choose'],
    [2, 3, 'one of the following'],
    [2, 4, 'answer (i) or (ii)'], [2, 4, 'or one'], [2, 4, 'or one'],
    [2, 5, 'one of the following'],
    [2, 6, 'any two'],
    [2, 7, 'any two'],
    [2, 9, 'any two'],
    [2, 11, 'any two'],
    [2, 13, 'two of the following'],
    [2, 14, 'one of the following'],
]
SELECTION_REVIEW = [
    {'scan': [[1, 2, 'attempt any ten'], [1, 2, 'attempt three'], [1, 2, 'choose'], [1, 2, 'choose'],
              [1, 3, 'attempt any ten'], [2, 2, 'attempt three'], [2, 2, 'choose'], [2, 2, 'choose']],
     'kind': 'exam-attempt-rule',
     'reason': 'Part One any ten of twelve and Part Two three questions ("not allowed to choose all three from the same section") are attempt rules; every question is carded.'},
    {'scan': [[1, 5, 'one of the following']], 'kind': 'not-a-selection',
     'reason': 'Part One Q3(ii) "Which one of the following processes" is a closed tick-box answer, not a candidate choice.'},
    {'scan': [[2, 3, 'one of the following']], 'kind': 'closed-choose-one',
     'reason': '1C one of four printed interactions -> 4 routes.'},
    {'scan': [[2, 4, 'answer (i) or (ii)'], [2, 4, 'or one'], [2, 4, 'or one']], 'kind': 'closed-route',
     'reason': '2B: (i) or (ii); (i) offers one fluvial OR one coastal OR one glacial landform -> 4 routes.'},
    {'scan': [[2, 5, 'one of the following']], 'kind': 'closed-choose-one',
     'reason': '3C one of three printed human impacts -> 3 routes.'},
    {'scan': [[2, 14, 'one of the following']], 'kind': 'closed-choose-one',
     'reason': '10B one of two printed migration contexts -> 2 routes.'},
    {'scan': [[2, 9, 'any two'], [2, 11, 'any two'], [2, 13, 'two of the following']],
     'kind': 'choose-n-one-card',
     'reason': '6B any two of three printed factors and 7B any two of three printed headings -> one card each; 9B two of three printed factors within each printed activity -> one card per activity (choice is not a route; the scheme marks each chosen item alike).'},
    {'scan': [], 'kind': 'inline-closed-route',
     'reason': '4C "culture or climate" -> 2 routes; 9B "footloose industries or financial services or mass tourism" -> 3 routes (no directive word the scan reads; the route text is anchored on the paper).'},
    {'scan': [[2, 6, 'any two'], [2, 7, 'any two']], 'kind': 'open-response',
     'reason': 'No printed pool: 4B any two contrasting European regions; 5B any two factors. Open choices are not fanned out: "one multinational company", "one developing economy", "example(s)". Compulsory lists stay whole: 1A, 4A, 7A and 10A each bullet, 8C each of three headings, 14, 22 and 23 each printed item.'},
]

P1, P2 = 1, 2
LEFT = (0.0, 0.0, 0.5, 1.0)
RIGHT = (0.5, 0.0, 1.0, 1.0)
# Q2 prints (i) and (ii) side by side in the left column of the Part One table.
Q2_I = (0.0, 0.0, 0.27, 1.0)
Q2_II = (0.27, 0.0, 0.5, 1.0)
ID = 'geography-2022-hl-'
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

Q1S = (L(3, 'Examine the diagram above which shows different layers of the earth', 'following questions.'),)
PART_ONE = [
    T('p1-1-i', P1, '1', '(i)', 6, 3, L(3, 'Structure of the Earth'),
      (L(3, '(i) Match each of the layers of the earth labelled A to F', 'table below.'),),
      (S(4, 'Q1 (i) D 1m', '(ii) True', LEFT),), rows(['Q1 (i) D 1m', 'F 1m', 'B 1m', 'C 1m', 'A 1m', 'E 1m']),
      '0-0', PS, ID + 'p1-q1', True, ('page',), Q1S,
      row_labels=(L(3, 'Asthenosphere'), L(3, 'Inner core'), L(3, 'Oceanic crust'), L(3, 'Lithosphere'),
                  L(3, 'Continental crust'), L(3, 'Outer core'))),
    T('p1-1-ii', P1, '1', '(ii)', 2, 3, L(3, 'Structure of the Earth'),
      (L(3, '(ii) State whether the following statement is true or false', 'correct box.'),
       L(3, 'Endogenic forces are those forces that act inside the earth.')),
      (S(4, '(ii) True 2m', 'Q2', LEFT),), (fixed('True or false', 2, '(ii) True 2m'),),
      '0-0', PS, ID + 'p1-q1-ii', False, ('page',), Q1S),
]

Q2S = (L(4, 'Examine the diagrams above which show different types of fault.', 'following questions.'),)
Q2_ROWS = (L(4, 'Tear/Transform fault'), L(4, 'Normal fault'), L(4, 'Thrust fault'))
PART_ONE += [
    T('p1-2-i', P1, '2', '(i)', 3, 4, L(4, 'Faulting'),
      (L(4, '(i) Match each of the diagrams A, B, and C', 'table below.'),),
      (S(4, 'Q2 (i) B · 1m', '(iii) Valid landfo', Q2_I),), rows(['Q2 (i) B · 1m', 'C · 1m', 'A · 1m']),
      '0-2', RW, ID + 'p1-q2', True, ('page',), Q2S, row_labels=Q2_ROWS),
    T('p1-2-ii', P1, '2', '(ii)', 3, 4, L(4, 'Faulting'),
      (L(4, '(ii) Indicate, by ticking (✓) the correct box', 'tension, compression or shearing.'),),
      (S(4, '(ii) Shearing 1m', 'orm · 2m', Q2_II),), rows(['(ii) Shearing 1m', 'Tension 1m', 'Compression 1m']),
      '0-2', RW, ID + 'p1-q2-ii', False, ('page',), Q2S, row_labels=Q2_ROWS),
    T('p1-2-iii', P1, '2', '(iii)', 2, 4, L(4, 'Faulting'),
      (L(4, '(iii) Name one landform formed by faulting.'),),
      (S(4, '(iii) Valid landform · 2m', 'Q3', LEFT),), (fixed('Landform', 2, '(iii) Valid landform · 2m'),),
      '0-2', RW, ID + 'p1-q2-iii', False, ('page',), Q2S),
]

Q3S = (L(5, 'The photographs above show the position of the Stein Glacier’s snout', 'following questions.'),)
PART_ONE += p1_romans('3', 5, L(5, 'Glaciation', nth=0), Q3S, ID + 'p1-q3', True, ('page',), [
    ('(i)', 2, (L(5, '(i) Did the Stein Glacier advance or retreat', 'Tick (✓) the correct box.'),
                L(5, 'Advance'), L(5, 'Retreat')),
     S(4, '(i) Retreat 2m', '(ii) Accumulation', LEFT), (fixed('Advance or retreat', 2, '(i) Retreat 2m'),),
     '0-11', GLAC),
    ('(ii)', 2, (L(5, '(ii) Which one of the following processes', 'Tick (✓) the correct box.'),
                 L(5, 'Plucking'), L(5, 'Melting'), L(5, 'Accumulation'), L(5, 'Abrasion')),
     S(4, '(ii) Accumulation 2m', '(iii) 54', LEFT), (fixed('Process', 2, '(ii) Accumulation 2m'),), '0-11', GLAC),
    ('(iii)', 2, L(5, '(iii) The snout of the Stein Glacier moved 540 metres', 'in metres, between 2006 and 2015.'),
     S(4, '(iii) 54 · 2m', '(iv) Valid landform', LEFT), (fixed('Annual rate', 2, '(iii) 54 · 2m'),), '2-0', TG + GLAC),
    ('(iv)', 2, L(5, '(iv) Name two landforms formed by glacial deposition.'),
     S(4, '(iv) Valid landform 1+1m', 'Q4', LEFT), (one_plus_one('(iv) Valid landform 1+1m', 'Two landforms'),),
     '0-11', GLAC),
])

Q4S = (L(6, 'Examine the 1:50 000 Ordnance Survey map extract above', 'following questions.'),)
PART_ONE += [
    T('p1-4-i', P1, '4', '(i)', 4, 6, L(6, 'Physical Processes'),
      (L(6, '(i) Match each of the features labelled A to D', 'table below.'),),
      (S(4, '(i) B · 1m', '(ii)E', LEFT, 'Q4'),), rows(['(i) B · 1m', '=C 1m', '=D 1m', '=A 1m']),
      '0-4', MAP + RIVERS + SEA, ID + 'p1-q4', True, ('page',), Q4S,
      row_labels=(L(6, 'Blowhole'), L(6, 'Meander'), L(6, 'V-shaped valley'), L(6, 'Beach'))),
    T('p1-4-ii', P1, '4', '(ii)', 4, 6, L(6, 'Physical Processes'),
      (L(6, '(ii) Name the drainage pattern that best matches the one seen in the area labelled E', 'labelled F.'),),
      (S(4, '(ii)E', 'Q5', LEFT),),
      (fixed('E', 2, '(ii)E – Trellised 2m'), fixed('F', 2, 'F – Dendritic 2m')),
      '0-9', RIVERS + MAP, ID + 'p1-q4-ii', False, ('page',), Q4S),
]

Q5S = (L(7, 'Examine the diagram above which shows an underground area in a karst landscape', 'following questions.'),)
PART_ONE += [
    T('p1-5-i', P1, '5', '(i)', 6, 7, L(7, 'Karst Landscapes'),
      (L(7, '(i) Name the underground features labelled A, B and C on the diagram above.'),),
      (S(4, '(i) A – Stalactite', '(ii) True 1m', LEFT),),
      (fixed('A', 2, '(i) A – Stalactite · 2m'), fixed('B', 2, 'B – Pillar/Column 2m'),
       fixed('C', 2, 'C - Stalagmite · 2m')),
      '0-3', KARST, ID + 'p1-q5', True, ('page',), Q5S),
    T('p1-5-ii', P1, '5', '(ii)', 2, 7, L(7, 'Karst Landscapes'),
      (L(7, '(ii) State whether each of the following statements is true or false', 'correct box.'),
       L(7, 'Percolation is the downward movement of water through rock or soil.'),
       L(7, 'A river of resurgence is one that disappears underground.')),
      (S(4, '(ii) True 1m', 'Q6', LEFT),), rows(['(ii) True 1m', 'False 1m']),
      '0-3', KARST, ID + 'p1-q5-ii', False, ('page',), Q5S,
      row_labels=(L(7, 'Percolation is the downward movement of water through rock or soil.'),
                  L(7, 'A river of resurgence is one that disappears underground.'))),
]

Q6S = (L(8, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper and answer',
         'following questions.'),)
PART_ONE += p1_romans('6', 8, L(8, 'Ordnance Survey Map'), Q6S, ID + 'p1-q6', False, ('map', 'legend'), [
    ('(i)', 2, L(8, '(i) Name the antiquity at S 226 248.'),
     S(4, '(i) Castle 2m', '(ii) S 206', LEFT), (fixed('Antiquity', 2, '(i) Castle 2m'),), '2-6', MAP),
    ('(ii)', 2, L(8, '(ii) Give a six-figure grid reference for the Garda Station in Clonmel.'),
     S(4, '(ii) S 206 225 · 2m', '(iii) 3.9', LEFT), (fixed('Grid reference', 2, '(ii) S 206 225 · 2m'),),
     '2-6', MAP),
    ('(iii)', 2, L(8, '(iii) Measure the length, in kilometres, of the R688 regional road', 'S 198 236.'),
     S(4, '(iii) 3.9 (km) 2m', '(iv) 41', LEFT), (fixed('Length', 2, '(iii) 3.9 (km) 2m'),), '2-6', MAP),
    ('(iv)', 2, L(8, '(iv) Estimate the area, in square kilometres, of the land north of the N24.'),
     S(4, '(iv) 41 (km²) · 2m', 'Page 3', LEFT), (fixed('Area', 2, '(iv) 41 (km²) · 2m'),), '2-6', MAP),
])

Q7S = (L(9, 'Locate point X, S 140 200, and point Y, S 260 200', 'Both points are on northing 20.'),
       L(9, 'Figure 1 shows an elevation profile', 'on the Ordnance Survey map.'),
       L(9, 'Using the 1:50 000 Ordnance Survey map and legend and the elevation profile above,',
         'following questions.'))
PART_ONE += p1_romans('7', 9, L(9, 'Ordnance Survey Map'), Q7S, ID + 'p1-q7', False, ('page', 'map', 'legend'), [
    ('(i)', 2, L(9, '(i) Name the river that crosses the profile at A.'),
     S(4, '(i) River Suir', '(ii) Waterford', RIGHT), (fixed('River', 2, '(i) River Suir · 2m'),), '2-6', MAP),
    ('(ii)', 2, L(9, '(ii) What is the name of the cycling trail located at B?'),
     S(4, '(ii) Waterford Cycling Trail 2m', '(iii) Forestry', RIGHT),
     (fixed('Cycling trail', 2, '(ii) Waterford Cycling Trail 2m'),), '2-6', MAP),
    ('(iii)', 2, L(9, '(iii) What is the land use at C?'),
     S(4, '(iii) Forestry', '(iv) R671', RIGHT), (fixed('Land use', 2, '(iii) Forestry · 2m'),), '2-6', MAP),
    ('(iv)', 2, L(9, '(iv) Name one regional road that is found on the area of the map', 'elevation profile.'),
     S(4, '(iv) R671 or R678 2m', 'Q8', RIGHT), (fixed('Regional road', 2, '(iv) R671 or R678 2m'),), '2-6', MAP),
])

PART_ONE.append(T(
    'p1-8', P1, '8', '', 8, 10, L(10, 'Aerial Photograph', nth=0),
    (L(10, 'Locate each of the features labelled A, B, C, D and E above', 'One has been completed for you.'),),
    (S(4, 'B - Right Backround', 'Q9', RIGHT),),
    (fixed('B', 2, 'B - Right Backround · 2m'), fixed('C', 2, 'C – Right Foreground · 2m'),
     fixed('D', 2, 'D – Left Middleground 2m'), fixed('E', 2, 'E – Centre Backround 2m')),
    '2-8', AER, ID + 'p1-q8', False, ('page', 'aerial'),
    (L(10, 'Examine the aerial photograph of Clonmel accompanying this paper', 'covered by the aerial photograph.'),
     L(10, 'Note: The orientation of the aerial photograph', 'orientation of the street map below.')),
    row_labels=(L(10, 'Bridge'), L(10, 'Church'), L(10, 'Sports pitch'), L(10, 'Shopping Centre'))))

Q9_GEO = 'A region in Ireland with a unique landscape based on rock type, structure or relief.'
Q9_ADMIN = 'A region in Europe with specific boundaries managed by an authority such as a local government.'
Q9_POOR = 'A poorer region in Europe where there is an underdevelopment of economic activities.'
REGIONS = IRL + EURO
PART_ONE += [
    T('p1-9-i', P1, '9', '(i)', 4, 11, L(11, 'Regions'),
      (L(11, '(i) Match each of the following types of region', 'best matches it.'),
       L(11, 'Peripheral'), L(11, 'Administrative'), L(11, 'Cultural'), L(11, 'Geomorphological')),
      (S(4, 'Q9 (i) Geomorphological 1m', '(ii) A (The Burren)', RIGHT),),
      rows(['Q9 (i) Geomorphological 1m', 'Cultural 1m', 'Administrative 1m', 'Peripheral 1m']),
      '1-0', REGIONS, ID + 'p1-q9', True, ('page',),
      row_labels=(L(11, Q9_GEO, nth=0),
                  L(11, 'A region in Ireland where people share a specific language, religion and/or way of life.'),
                  L(11, Q9_ADMIN, nth=0), L(11, Q9_POOR, nth=0))),
    T('p1-9-ii', P1, '9', '(ii)', 4, 11, L(11, 'Regions'),
      (L(11, '(ii) Examine each of the maps below showing examples of different types of regions.',
         'best matches it.'),),
      (S(4, '(ii) A (The Burren)', 'Q10', RIGHT),),
      rows(['(ii) A (The Burren) 1m', 'C (Gaeltachts) 1m', 'D (Départements) 1m', 'B (The Mezzogiorno) 1m']),
      '1-0', REGIONS, ID + 'p1-q9-ii', False, ('page',),
      row_labels=(L(11, Q9_GEO, nth=1), L(11, 'A region in Ireland where people share a specific language.'),
                  L(11, Q9_ADMIN, nth=1), L(11, Q9_POOR, nth=1))),
]

Q10S = (L(12, 'Examine the weather charts above and state whether each', 'correct box.'),)
PART_ONE += p1_romans('10', 12, L(12, 'Weather', nth=0), Q10S, ID + 'p1-q10', True, ('page',), [
    ('(i)', 2, L(12, '(i) The mean air temperature between 6th and 12th September', '16.5 °C.'),
     S(4, '(i) True · 2m', '(ii) False', RIGHT), (fixed('True or false', 2, '(i) True · 2m'),), '2-7', WX),
    ('(ii)', 2, L(12, '(ii) There were more than 25 hours of accumulated sunshine', 'September.'),
     S(4, '(ii) False 2m', '(iii) False', RIGHT), (fixed('True or false', 2, '(ii) False 2m'),), '2-7', WX),
    ('(iii)', 2, L(12, '(iii) The area marked X received the highest levels of rainfall', 'September.'),
     S(4, '(iii) False 2m', '(iv) True', RIGHT), (fixed('True or false', 2, '(iii) False 2m'),), '2-7', WX),
    ('(iv)', 2, L(12, '(iv) Lines on a weather map that join areas of equal sunshine are called isohels.'),
     S(4, '(iv) True · 2m', 'Q11', RIGHT), (fixed('True or false', 2, '(iv) True · 2m'),), '2-7', WX),
])

Q11S = (L(13, 'Examine the bar chart above which shows the percentage of land covered by forests',
          'following questions.'),)
ENV = (H + 'economic-environmental-impact',)
PART_ONE += p1_romans('11', 13, L(13, 'Statistical Interpretation'), Q11S, ID + 'p1-q11', True, ('page',), [
    ('(i)', 2, L(13, '(i) How many countries had a higher percentage of land covered by forests', 'in 2019?'),
     S(4, '(i) 4 · 2m', '(ii) Sweden', RIGHT), (fixed('Number of countries', 2, '(i) 4 · 2m'),), '2-0', TG),
    ('(ii)', 2, L(13, '(ii) Name one country that had twice as much land covered by forests as Germany in 2019.'),
     S(4, '(ii) Sweden · 2m', '(iii) 42.1', RIGHT), (fixed('Country', 2, '(ii) Sweden · 2m'),), '2-0', TG),
    ('(iii)', 2, L(13, '(iii) Calculate the average percentage of land covered by forests', 'chart above.'),
     S(4, '(iii) 42.1 2m', '(iv) Benefit stated', RIGHT), (fixed('Average', 2, '(iii) 42.1 2m'),), '2-0', TG),
    ('(iv)', 2, L(13, '(iv) State two benefits of a country having a large area of land covered by forest.'),
     S(4, '(iv) Benefit stated · 1+1m', 'Q12', RIGHT), (one_plus_one('(iv) Benefit stated · 1+1m', 'Two benefits'),),
     '3-4', ENV),
])

Q12S = (L(14, 'Examine the infographic above which shows where Ireland ranked', 'following questions.'),)
PART_ONE += p1_romans('12', 14, L(14, 'Graphical Interpretation'), Q12S, ID + 'p1-q12', True, ('page',), [
    ('(i)', 2, L(14, '(i) What percentage of its GDP did Ireland spend on health care in 2019?'),
     S(4, '(i) 6.9 (%)', '(ii) Luxembourg', RIGHT), (fixed('Percentage', 2, '(i) 6.9 (%) · 2m'),), '2-0', TG),
    ('(ii)', 2, L(14, '(ii) Which country was ranked 27th in two of the metrics?'),
     S(4, '(ii) Luxembourg · 2m', '(iii) 82,652,147', RIGHT), (fixed('Country', 2, '(ii) Luxembourg · 2m'),),
     '2-0', TG),
    ('(iii)', 2, L(14, '(iii) Calculate the difference in number of persons between the lowest', 'population.'),
     S(4, '(iii) 82,652,147 · 2m', '(iv) Valid explanation', RIGHT), (fixed('Difference', 2, '(iii) 82,652,147 · 2m'),),
     '2-0', TG),
    ('(iv)', 2, (L(14, '(iv) Ireland is ranked highest in the EU for the number of STEM graduates', 'of this high rank.'),),
     S(4, '(iv) Valid explanation 1m + 1m', '3 of 59', RIGHT),
     (one_plus_one('(iv) Valid explanation 1m + 1m', 'Advantage'),), '1-4', IRL),
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
ROCK = ('Mining', 'Extraction of building materials', 'Oil/gas exploitation', 'Geothermal energy production.')

PART_TWO = [
    T('p2-1a', P2, '1A', '', 20, 3, L(3, 'Ordnance Survey Map'),
      (L(3, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper.', 'west of Easting 17.'),),
      (S(6, 'Sketch Outline', None),), OS_SKETCH, '2-6', MAP, ID + 'p2-q1a', False, ('map', 'legend'),
      row_labels=(None, L(3, 'The entire course of the River Suir'), L(3, 'An area of land over 400m'),
                  L(3, 'The Waterford Cycling Trails cycle route from S 148 180 to S 200 218'),
                  L(3, 'An area of coniferous plantation north of Northing 24 and west of Easting 17.'))),
    T('p2-1b', P2, '1B', '', 30, 3, L(3, 'Tectonic Activity – Irish Landscape'),
      (L(3, 'Examine how tectonic activity has influenced the development of the Irish landscape.'),),
      (S(7, 'Influence of tectonic activity on the Irish landscape identified', 'Annotation'),),
      (fixed('Influence on the Irish landscape identified', 2,
             'Influence of tectonic activity on the Irish landscape identified 2 marks'),
       srp('Examination', 14, f'Examination · 14 x {SRPS}')),
      '0-2', RW + PS, ID + 'p2-q1b', True),
    T('p2-1c', P2, '1C', '', 30, 3, L(3, 'Human Interaction with the Rock Cycle'),
      (L(3, 'Examine how humans interact with the rock cycle', 'Geothermal energy production.'),),
      (S(8, f'Examination · 15 x {SRPS}', 'Annotation'),), (srp('Examination', 15, f'Examination · 15 x {SRPS}'),),
      '0-6', RW, ID + 'p2-q1c-mining', True, routes=bullet_routes('p2-q1c-', ROCK)),
]

Q2AS = (L(4, 'Examine the diagrams above which show a fluvial landscape before and after rejuvenation.',
          'following questions.'),)
PART_TWO += romans('2A', 4, L(4, 'Adjustment to Base Level'), Q2AS, ID + 'p2-q2a', ('page',), [
    ('(i)', 4, L(4, '(i) Name the fluvial landforms labelled A and B in Figure 1.'),
     (S(9, '(i) · A = Floodplain', '(ii) · C = Knickpoint'),),
     (fixed('A', 2, '(i) · A = Floodplain · 2 marks'), fixed('B', 2, 'B = Levee · 2 marks')), '0-9', RIVERS),
    ('(ii)', 4, L(4, '(ii) Name the landforms of river rejuvenation labelled C and D in Figure 2.'),
     (S(9, '(ii) · C = Knickpoint', '(iii) · Valid landforms'),),
     (fixed('C', 2, '(ii) · C = Knickpoint · 2 marks'), fixed('D', 2, 'D = Paired Terraces · 2 marks')),
     '0-9', RIVERS),
    ('(iii)', 4, L(4, '(iii) Name two coastal landforms that form as a result of an adjustment to base level.'),
     (S(9, '(iii) · Valid landforms', '(iv) · Valid explanation'),),
     (pair('(iii) · Valid landforms · 2 + 2 marks', 'Two coastal landforms'),), '0-10', SEA),
    ('(iv)', 4, L(4, '(iv) Explain briefly one cause of river rejuvenation.'),
     (S(9, '(iv) · Valid explanation', '(v) · Valid explanation'),),
     (pair('(iv) · Valid explanation · 2 + 2 marks', 'Cause'),), '0-9', RIVERS),
    ('(v)', 4, L(4, '(v) Explain briefly what is meant by peneplain.'),
     (S(9, '(v) · Valid explanation', None),), (pair('(v) · Valid explanation · 2 + 2 marks', 'Explanation'),),
     '0-5', RIVERS),
])

PART_TWO += [
    T('p2-2b', P2, '2B', '', 30, 4, L(4, 'Surface Processes'),
      (L(4, '(i) Examine the role of the processes of erosion', 'that you have studied.'),),
      (S(10, 'Process of erosion identified · 2 marks', 'Annotation'),),
      (fixed('Process of erosion identified', 2, 'Process of erosion identified · 2 marks'),
       fixed('Landform named', 2, 'Landform named · 2 marks'), srp('Examination', 13, f'Examination · 13 x {SRPS}')),
      '0-9', RIVERS, ID + 'p2-q2b-route-i-fluvial-landform', True,
      routes=(
          Route('route-i-fluvial-landform', 'Route (i) · one fluvial landform', ID + 'p2-q2b-route-i-fluvial-landform',
                True, ((LANDFORMS, 'one fluvial landform'),), topic='0-9', atlas=RIVERS),
          Route('route-i-coastal-landform', 'Route (i) · one coastal landform', ID + 'p2-q2b-route-i-coastal-landform',
                True, ((LANDFORMS, 'one coastal landform'),), topic='0-10', atlas=SEA),
          Route('route-i-glacial-landform', 'Route (i) · one glacial landform', ID + 'p2-q2b-route-i-glacial-landform',
                True, ((LANDFORMS, 'one glacial landform'),), topic='0-11', atlas=GLAC),
          Route('route-ii', 'Route (ii)', ID + 'p2-q2b-route-ii', True,
                prompt=(L(4, '(ii) Describe and explain the factors governing', 'process that you have studied.'),),
                scheme=(S(11, 'Factors identified', 'Annotation'),),
                criteria=(pair('Factors identified · 2 + 2 marks', 'Factors identified'),
                          fixed('Mass movement process named', 2, 'Mass movement process named · 2 marks'),
                          srp('Description/explanation', 12, f'Description/explanation · 12 x {SRPS}')),
                topic='0-8', atlas=RW),
      )),
    T('p2-2c', P2, '2C', '', 30, 4, L(4, 'Metamorphic Rocks'),
      (L(4, 'Examine the formation of metamorphic rocks, with reference to examples from Ireland.'),),
      (S(12, 'Named Irish metamorphic rocks', 'Annotation'),),
      (pair('Named Irish metamorphic rocks · 2 + 2 marks', 'Two Irish metamorphic rocks named'),
       srp('Examination of formation', 13, 'Examination of formation · 13 x SRPs')),
      '0-1', RW, ID + 'p2-q2c', True),
]

Q3AS = (L(5, 'Examine the image above which shows a plate boundary in the North Atlantic Ocean', 'following questions.'),)
PART_TWO += romans('3A', 5, L(5, 'Plate Tectonics'), Q3AS, ID + 'p2-q3a', ('page',), [
    ('(i)', 4, L(5, '(i) Name each of the tectonic plates labelled A and B.'),
     (S(13, '(i) · A = North American', '(ii) · C = Iceland'),),
     (fixed('A', 2, '(i) · A = North American · 2 marks'), fixed('B', 2, 'B = Eurasian · 2 marks')), '0-0', PS),
    ('(ii)', 2, L(5, '(ii) Name the country labelled C which is located along the Mid-Atlantic Ridge.'),
     (S(13, '(ii) · C = Iceland', '(iii) · D = 23'),), (fixed('Country', 2, '(ii) · C = Iceland · 2 marks'),),
     '0-0', PS),
    ('(iii)', 4, L(5, '(iii) State the age range for the oceanic crust at each of the locations labelled D and E.'),
     (S(13, '(iii) · D = 23', '(iv) · Basalt'),),
     (fixed('D', 2, '(iii) · D = 23 - 66 · 2 marks'), fixed('E', 2, 'E = 145 - 180 · 2 marks')), '0-0', PS),
    ('(iv)', 2, L(5, '(iv) What type of igneous rock is most commonly formed along mid-ocean ridges?'),
     (S(13, '(iv) · Basalt', '(v) · Valid explanation'),), (fixed('Igneous rock', 2, '(iv) · Basalt · 2 marks'),),
     '0-1', RW),
    ('(v)', 4, L(5, '(v) Explain briefly why the ocean crust found at E is older', 'found at D.'),
     (S(13, '(v) · Valid explanation', '(vi) · Valid explanation'),),
     (pair('(v) · Valid explanation · 2 + 2 marks', 'Explanation'),), '0-0', PS),
    ('(vi)', 4, L(5, '(vi) Explain briefly what is meant by the term Moho line.'),
     (S(13, '(vi) · Valid explanation', None),), (pair('(vi) · Valid explanation · 2 + 2 marks', 'Explanation'),),
     '0-0', PS),
])

IMPACTS = ('The impact of dams on river processes', 'The impact of coastal defence work on coastal processes',
           'The impact of human activity on mass movement.')
PART_TWO += [
    T('p2-3b', P2, '3B', '', 30, 5, L(5, 'Weathering'),
      (L(5, 'Explain the role of temperature in the process(es) of physical/mechanical weathering.'),),
      (S(14, 'Reference to temperature · 2m', 'Annotation'),),
      (fixed('Reference to temperature', 2, 'Reference to temperature · 2m'),
       srp('Explanation', 14, f'Explanation · 14 x {SRPS}')),
      '0-8', RW, ID + 'p2-q3b', True),
    T('p2-3c', P2, '3C', '', 30, 5, L(5, 'Human Interaction with Surface Processes'),
      (L(5, '‘Human activity impacts on surface processes.’'),
       L(5, 'Examine this statement with reference to one of the following:', 'on mass movement.')),
      (S(15, 'Impact on process identified · 2 marks', 'Annotation'),),
      (fixed('Impact on process identified', 2, 'Impact on process identified · 2 marks'),
       srp('Examination', 14, f'Examination · 14 x {SRPS}')),
      '0-6', RIVERS, ID + 'p2-q3c-the-impact-of-dams-on-river-proces', True,
      routes=bullet_routes('p2-q3c-', IMPACTS, atlas=dict(zip(IMPACTS, (RIVERS, SEA, RW))))),
    # Question 4
    T('p2-4a', P2, '4A', '', 20, 6, L(6, 'Map Skills'),
      (L(6, 'Draw an outline map of Ireland.', 'One named river in that region.'),),
      (S(16, 'Map outline', None),),
      sketch('Map outline · 4 marks graded (4/2/0)', (0, 2, 4),
             ('4 features @ 4 marks each', 'Named 2 marks'), sums((0, 1, 2), (0, 2)), 4),
      '1-4', IRL, ID + 'p2-q4a', True,
      row_labels=(None, L(6, 'The outline of one named region'),
                  L(6, 'The outline of a named feature of relief (upland or lowland) within that region'),
                  L(6, 'One named urban centre in that region'), L(6, 'One named river in that region.'))),
    T('p2-4b', P2, '4B', '', 30, 6, L(6, 'Dynamics of Regions – Transport'),
      (L(6, 'Examine the importance of transport to the economic development', 'that you have studied.'),),
      (S(17, 'Examination of region 1', 'Annotation'),),
      (split('Examination of the two regions (8/7 and 7/8 SRPs)', 15,
             f'Examination of region 1 · 8/7 x {SRPS}', f'Examination of region 2 · 7/8 x {SRPS}'),),
      '1-5', EURO, ID + 'p2-q4b', True),
    T('p2-4c', P2, '4C', '', 30, 6, L(6, 'Concept of a Region'),
      (L(6, 'Examine how culture or climate can be used to define regions', 'that you have studied.'),),
      (S(18, 'Example · 2 marks', 'Annotation'),),
      (fixed('Example', 2, 'Example · 2 marks'), srp('Examination', 14, f'Examination · 14 x {SRPS}')),
      '1-0', IRL + EURO + CONT, ID + 'p2-q4c', True,
      routes=(Route('culture', 'culture', ID + 'p2-q4c', True, (('culture or climate', 'culture'),)),
              Route('climate', 'climate', ID + 'p2-q4c-climate', False, (('culture or climate', 'climate'),)))),
]

Q5AS = (L(7, 'Examine the bar chart above showing the number of cattle, pigs and sheep', 'following questions.'),)
PART_TWO += romans('5A', 7, L(7, 'Agriculture in the European Union'), Q5AS, ID + 'p2-q5a', ('page',), [
    ('(i)', 2, L(7, '(i) Which animal did Greece have the highest number of in 2019?'),
     (S(19, '(i) · Sheep', '(ii) · Italy/Hungary'),), (fixed('Animal', 2, '(i) · Sheep · 2 marks'),), '2-0', TG),
    ('(ii)', 4, L(7, '(ii) Name two countries from the chart above that had more than 2 million pigs in 2019.'),
     (S(19, '(ii) · Italy/Hungary', '(iii) · Italy'),),
     (pair('(ii) · Italy/Hungary/Netherlands/Portugal · 2 + 2 marks', 'Two countries'),), '2-0', TG),
    ('(iii)', 2, L(7, '(iii) Which country, from the chart above, had more than 6 million', 'in 2020?'),
     (S(19, '(iii) · Italy', '(iv) · Decrease'),), (fixed('Country', 2, '(iii) · Italy · 2 marks'),), '2-0', TG),
    ('(iv)', 2, L(7, '(iv) Was there an increase or decrease in the number of pigs', '2019 and 2020?'),
     (S(19, '(iv) · Decrease', '(v) · Valid policy'),), (fixed('Increase or decrease', 2, '(iv) · Decrease · 2 marks'),),
     '2-0', TG),
    ('(v)', 2, L(7, '(v) Name one specific European Union policy', 'agriculture.'),
     (S(19, '(v) · Valid policy', '(vi) · Valid explanation'),), (fixed('Policy', 2, '(v) · Valid policy named · 2 marks'),),
     '1-5', EURO),
    ('(vi)', 4, L(7, '(vi) Explain briefly one benefit of Ireland having large numbers of cattle.'),
     (S(19, '(vi) · Valid explanation', '(vii) Valid explanation'),),
     (pair('(vi) · Valid explanation · 2 + 2 marks', 'Benefit'),), '1-4', IRL),
    ('(vii)', 4, L(7, '(vii) Explain briefly one environmental problem associated with', 'livestock.'),
     (S(19, '(vii) Valid explanation', None),), (pair('(vii) Valid explanation · 2 + 2 marks', 'Environmental problem'),),
     '3-4', ENV),
])

PART_TWO += [
    T('p2-5b', P2, '5B', '', 30, 7, L(7, 'Secondary Economic Activity – Continental / Sub-Continental Region'),
      (L(7, 'Examine how any two factors have influenced the development of secondary economic', 'that you have studied.'),),
      (S(20, 'Factors named · 2 + 2 marks', 'Annotation'),),
      (pair('Factors named · 2 + 2 marks', 'Factors named'),
       split('Examination of the two factors (7/6 and 6/7 SRPs)', 13,
             f'Examination of Factor 1 · 7/6 x {SRPS}', f'Examination of Factor 2 · 6/7 x {SRPS}')),
      '1-6', CONT, ID + 'p2-q5b', True),
    T('p2-5c', P2, '5C', '', 30, 7, L(7, 'Population Dynamics'),
      (L(7, 'Account for population distribution throughout a European region', 'have studied.'),),
      (S(21, f'Examination · 15 x {SRPS}', 'Annotation'),), (srp('Examination', 15, f'Examination · 15 x {SRPS}'),),
      '1-5', EURO + POP, ID + 'p2-q5c', True),
]

Q6AS = (L(8, 'Examine the table above showing the percentage of 25-34 year olds', 'following questions.'),)
PART_TWO += romans('6A', 8, L(8, 'Education in European Countries'), Q6AS, ID + 'p2-q6a', ('page',), [
    ('(i)', 2, L(8, '(i) What was the percentage of 25-34 year olds with third level education in Hungary', '2016?'),
     (S(22, '(i) · 30.4', '(ii) · Italy'),), (fixed('Percentage', 2, '(i) · 30.4 (%) · 2 marks'),), '2-0', TG),
    ('(ii)', 2, L(8, '(ii) Which country had the lowest percentage of 25-34 year olds', 'in 2012?'),
     (S(22, '(ii) · Italy', '(iii) · Ireland/Spain'),), (fixed('Country', 2, '(ii) · Italy · 2 marks'),), '2-0', TG),
    ('(iii)', 4, L(8, '(iii) List two countries where the percentage of 25-34 year olds', 'EU Average for 2020.'),
     (S(22, '(iii) · Ireland/Spain', '(iv) · Rise'),),
     (pair('(iii) · Ireland/Spain/France/Lithuania/Netherlands 2 + 2 marks', 'Two countries'),), '2-0', TG),
    ('(iv)', 2, L(8, '(iv) Did the percentage of 25-34 year olds with third level education for each', '2012 and 2020?'),
     (S(22, '(iv) · Rise', '(v) · 29.5'),), (fixed('Rise or fall', 2, '(iv) · Rise · 2 marks'),), '2-0', TG),
    ('(v)', 4, L(8, '(v) Calculate the difference between the country with the highest percentage', 'in 2020.'),
     (S(22, '(v) · 29.5', '(vi) · Third level'),), (fixed('Difference', 4, '(v) · 29.5 · 4 marks'),), '2-0', TG),
    ('(vi)', 2, L(8, '(vi) Name one third level institution in Ireland where students receive tertiary education.'),
     (S(22, '(vi) · Third level institution named', '(vii) Valid explanation'),),
     (fixed('Institution', 2, '(vi) · Third level institution named · 2 marks'),), '1-4', IRL),
    ('(vii)', 4, L(8, '(vii) Explain briefly one benefit of a region having large numbers of people', 'third level education.'),
     (S(22, '(vii) Valid explanation', None),), (pair('(vii) Valid explanation · 2 + 2 marks', 'Benefit'),),
     '1-5', EURO),
])

FACTORS_6B = ('Relief', 'Climate', 'Markets.')
PART_TWO += [
    T('p2-6b', P2, '6B', '', 30, 9, L(9, 'Agriculture in Ireland'),
      (L(9, 'Account for the development of agriculture in an Irish region that you have studied', 'Markets.'),),
      (S(23, 'Account of Factor 1', 'Annotation'),),
      (split('Account of the two factors (8/7 and 7/8 SRPs)', 15,
             'Account of Factor 1 · 8/7 x SRPs', 'Account of Factor 2 · 7/8 x SRPs'),),
      '1-4', IRL, *pool(ID + 'p2-q6b-', FACTORS_6B, 2)[:1], True, absorbs=pool(ID + 'p2-q6b-', FACTORS_6B, 2)[1]),
    T('p2-6c', P2, '6C', '', 30, 9, L(9, 'Socio-Economic Regions'),
      (L(9, 'Examine the causes and impacts of industrial decline', 'that you have studied.'),),
      (S(24, 'Cause identified · 2 marks', 'Annotation'),),
      (fixed('Cause identified', 2, 'Cause identified · 2 marks'), fixed('Impact identified', 2, 'Impact identified · 2 marks'),
       srp('Examination', 13, 'Examination · 13 x SRPs')),
      '1-1', IRL + EURO, ID + 'p2-q6c', True),
]

ECON = (H + 'elective-economic',)
DEV = (H + 'economic-developing-economies',)
MNC = (H + 'economic-multinationals-globalisation',)
EU_ECON = (H + 'economic-european-union',)
HEADINGS_7B = ('Sourcing of raw materials and components', 'Location of processing units', 'Location of markets.')
PART_TWO += [
    # Question 7
    T('p2-7a', P2, '7A', '', 20, 11, L(11, 'Ordnance Survey Map'),
      (L(11, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper.', 'A car park.'),),
      (S(26, 'Sketch Outline', None),), OS_SKETCH, '2-6', MAP, ID + 'p2-q7a', False, ('map', 'legend'),
      row_labels=(None, L(11, 'The entire route of the N24'), L(11, 'The entire route of the railway line'),
                  L(11, 'A post office'), L(11, 'A car park.'))),
    T('p2-7b', P2, '7B', '', 30, 11, L(11, 'Multinational Company'),
      (L(11, 'With reference to one multinational company that you have studied', 'Location of markets.'),),
      (S(27, 'MNC named · 2 marks', 'Annotation'),),
      (fixed('MNC named', 2, 'MNC named · 2 marks'),
       srp('Description and explanation 1', 7, 'Description and explanation 1 · 7 x SRPs'),
       srp('Description and explanation 2', 7, 'Description and explanation 2 · 7 x SRPs')),
      '3-2', MNC, *pool(ID + 'p2-q7b-', HEADINGS_7B, 2)[:1], True, absorbs=pool(ID + 'p2-q7b-', HEADINGS_7B, 2)[1]),
    T('p2-7c', P2, '7C', '', 30, 11, L(11, 'Sustainable Development'),
      (L(11, 'Examine how economic activities can be developed sustainably', 'environmental impact.'),),
      (S(28, 'Examination · 15 x SRPs', 'Annotation'),), (srp('Examination', 15, 'Examination · 15 x SRPs'),),
      '3-4', ENV, ID + 'p2-q7c', True),
]

Q8AS = (L(12, 'Examine the data above showing Ireland’s top export partners in 2020', 'following questions.'),)
PART_TWO += romans('8A', 12, L(12, 'Irish Trade'), Q8AS, ID + 'p2-q8a', ('page',), [
    ('(i)', 16, L(12, '(i) Using graph paper, draw a suitable graph to illustrate this data.'),
     (S(29, 'Bar Chart · Pie Chart', 'Annotation'),), GRAPH, '2-0', TG),
    ('(ii)', 4, L(12, '(ii) Explain briefly what is meant by the term balance of payments.'),
     (S(29, 'Valid explanation · 2 + 2 marks', None),), (pair('Valid explanation · 2 + 2 marks', 'Explanation'),),
     '3-0', ECON),
])

TOURISM_HEADING = ('Three headings @ 10 marks each', 'For each of the three headings:', 'Named example · 2 marks',
                   'Map evidence · 2 marks', f'Discussion · 3 x {SRPS}')
PART_TWO += [
    T('p2-8b', P2, '8B', '', 30, 12, L(12, 'Globalisation'),
      (L(12, 'Explain the impact of globalisation on one developing economy that you have studied.'),),
      (S(30, 'Named Developing Economy · 2 marks', 'Annotation'),),
      (fixed('Developing economy named', 2, 'Named Developing Economy · 2 marks'),
       pair('Impacts identified · 2 + 2 marks', 'Impacts identified'), srp('Explanation', 12, 'Explanation · 12 x SRPs')),
      '3-1', DEV + MNC, ID + 'p2-q8b', True),
    T('p2-8c', P2, '8C', '', 30, 12, L(12, 'Tertiary Economic Activities'),
      (L(12, 'Using evidence from the 1:50 000 Ordnance Survey map of Clonmel', 'Attractions.'),),
      (S(31, 'Three headings @ 10 marks each', 'Annotation'),),
      tuple(Criterion(f'Heading {n}', 10, evens(10), 'srp', TOURISM_HEADING) for n in (1, 2, 3)),
      '3-0', ECON + MAP, ID + 'p2-q8c', False, ('map', 'legend'),
      row_labels=(L(12, 'Accessibility'), L(12, 'Services (excluding transport)'), L(12, 'Attractions.'))),
]

Q9AS = (L(13, 'Examine the table above showing the Human Development Index (HDI)', 'following questions.'),)
PART_TWO += romans('9A', 13, L(13, 'Measuring Development'), Q9AS, ID + 'p2-q9a', ('page',), [
    ('(i)', 2, L(13, '(i) Which country had the longest life expectancy at birth in 2019?'),
     (S(32, '(i) · Australia', '(ii) · 0.551'),), (fixed('Country', 2, '(i) · Australia · 2 marks'),), '2-0', TG),
    ('(ii)', 2, L(13, '(ii) What was the Human Development Index (HDI) for Bolivia in 1990?'),
     (S(32, '(ii) · 0.551', '(iii) · 6.3'),), (fixed('HDI', 2, '(ii) · 0.551 · 2 marks'),), '2-0', TG),
    ('(iii)', 2, L(13, '(iii) What was the mean years of schooling in 2019 for Cameroon?'),
     (S(32, '(iii) · 6.3', '(iv) · Vietnam'),), (fixed('Mean years', 2, '(iii) · 6.3 · 2 marks'),), '2-0', TG),
    ('(iv)', 4, L(13, '(iv) Which country had the greater increase in HDI', 'Ireland or Vietnam?'),
     (S(32, '(iv) · Vietnam', '(v) · Valid explanation'),), (fixed('Country', 4, '(iv) · Vietnam · 4 marks'),),
     '2-0', TG),
    ('(v)', 4, L(13, '(v) Explain briefly one reason why life expectancy in some countries is lower', 'in others.'),
     (S(32, '(v) · Valid explanation', '(vi) · Valid factor'),), (pair('(v) · Valid explanation · 2 + 2 marks', 'Reason'),),
     '3-1', DEV),
    ('(vi)', 2, L(13, '(vi) Life expectancy and mean years of schooling are two factors', 'Name a third factor.'),
     (S(32, '(vi) · Valid factor', '(vii) Valid explanation'),), (fixed('Third factor', 2, '(vi) · Valid factor named · 2 marks'),),
     '3-1', ECON + DEV),
    ('(vii)', 4, L(13, '(vii) Explain briefly one advantage of using the Human Development Index', 'economic development.'),
     (S(32, '(vii) Valid explanation', None),), (pair('(vii) Valid explanation · 2 + 2 marks', 'Advantage'),),
     '3-1', ECON + DEV),
])

ACTIVITY = 'footloose industries or financial services or mass tourism'
FACTORS_9B = ('Physical factors', 'Human factors', 'Political factors.')
PART_TWO += [
    T('p2-9b', P2, '9B', '', 30, 13, L(13, 'Economic Development – Developed Economy'),
      (L(13, 'Examine the impact of two of the following on the development', 'Political factors.'),),
      (S(33, 'Named developed economy · 2m', 'Annotation'),),
      (fixed('Named developed economy', 2, 'Named developed economy · 2m'),
       srp('Examination of factor 1', 7, f'Examination of factor 1 · 7 x {SRPS}'),
       srp('Examination of factor 2', 7, f'Examination of factor 2 · 7 x {SRPS}')),
      '3-0', ECON, ID + 'p2-q9b-footloose-industries-physical-factors-human-factors', True,
      # Choose ONE printed activity (a route each); the choose-two factor pool
      # within it is one card.
      routes=tuple(Route(f'{slug(activity)}-{pool("", FACTORS_9B, 2)[0]}', activity,
                         ID + f'p2-q9b-{slug(activity)}-{pool("", FACTORS_9B, 2)[0]}', True, ((ACTIVITY, activity),),
                         absorbs=pool(ID + f'p2-q9b-{slug(activity)}-', FACTORS_9B, 2)[1])
                   for activity in ('footloose industries', 'financial services', 'mass tourism'))),
    T('p2-9c', P2, '9C', '', 30, 13, L(13, 'European Union Policy'),
      (L(13, 'Examine how different European Union policies impact on the Irish economy.'),),
      (S(34, 'Impact on the Irish economy identified', 'Annotation'),),
      (fixed('Impact on the Irish economy identified', 2, 'Impact on the Irish economy identified · 2 marks'),
       pair('EU policy named · 2 + 2 marks', 'EU policies named'), srp('Examination', 12, 'Examination · 12 x SRPs')),
      '3-3', EU_ECON, ID + 'p2-q9c', True),
    # Question 10
    T('p2-10a', P2, '10A', '', 20, 14, L(14, 'Aerial Photograph'),
      (L(14, 'Examine the aerial photograph of Clonmel accompanying this paper.', 'An area of residential land-use.'),),
      (S(35, 'Sketch Outline', None),), AERIAL_SKETCH, '2-8', AER + URB, ID + 'p2-q10a', False, ('aerial',),
      row_labels=(None, L(14, 'Two connecting streets'), L(14, 'An area of recreational land-use'),
                  L(14, 'An area of ecclesiastical land-use'), L(14, 'An area of residential land-use.'))),
]

MIGRATION = ('Migration policy in the European Union', 'Rural to urban migration in the developing world.')
PART_TWO += [
    T('p2-10b', P2, '10B', '', 30, 14, L(14, 'Migration', nth=0),
      (L(14, '‘Population movements have an impact on donor and receiver regions.’'),
       L(14, 'Discuss this statement with reference to one of the following:', 'in the developing world.')),
      (S(36, 'Impact on donor region identified · 2 marks', 'Annotation'),),
      (fixed('Impact on donor region identified', 2, 'Impact on donor region identified · 2 marks'),
       fixed('Impact on receiver region identified', 2, 'Impact on receiver region identified · 2 marks'),
       srp('Discussion', 13, f'Discussion · 13 x {SRPS}')),
      '4-2', POP, ID + 'p2-q10b-migration-policy-in-the-european-u', True,
      routes=bullet_routes('p2-q10b-', MIGRATION)),
    T('p2-10c', P2, '10C', '', 30, 14, L(14, 'Central Place Theory', nth=0),
      (L(14, 'Describe and explain Central Place Theory with reference to example(s)', 'studied.'),),
      (S(37, 'Example · 2 marks', 'Annotation'),),
      (fixed('Example', 2, 'Example · 2 marks'), srp('Description/explanation', 14, 'Description/Explanation · 14 x SRPs')),
      '4-3', URB, ID + 'p2-q10c', True),
]

Q11AS = (L(15, 'Examine the table above showing the total population, total land area', 'following questions.'),)
PART_TWO += romans('11A', 15, L(15, 'Population Density', nth=0), Q11AS, ID + 'p2-q11a', ('page',), [
    ('(i)', 2, L(15, '(i) What was the population density, people per km2, for Italy in 2020?'),
     (S(38, '(i) · 199.9', '(ii) · Iceland'),), (fixed('Population density', 2, '(i) · 199.9 · 2 marks'),), '2-0', TG),
    ('(ii)', 2, L(15, '(ii) Which country had the lowest population in 2020?'),
     (S(38, '(ii) · Iceland', '(iii) · Spain'),), (fixed('Country', 2, '(ii) · Iceland · 2 marks'),), '2-0', TG),
    ('(iii)', 2, L(15, '(iii) Which country has the largest total area?'),
     (S(38, '(iii) · Spain', '(iv) · Three'),), (fixed('Country', 2, '(iii) · Spain · 2 marks'),), '2-0', TG),
    ('(iv)', 2, L(15, '(iv) How many countries have a total area that is smaller than Ireland?'),
     (S(38, '(iv) · Three', '(v) · 70.6'),), (fixed('Number of countries', 2, '(iv) · Three · 2 marks'),), '2-0', TG),
    ('(v)', 4, L(15, '(v) Calculate X, the population density, people per km², for Ireland in 2020.'),
     (S(38, '(v) · 70.6', '(vi) · Valid explanation'),), (fixed('Population density', 4, '(v) · 70.6 · 4 marks'),),
     '2-0', TG),
    ('(vi)', 8, L(15, '(vi) Explain briefly two reasons why some areas have a low population density.'),
     (S(38, '(vi) · Valid explanation', None),),
     (pair('(vi) · Valid explanation · 2 + 2 marks', 'First reason'), pair('=2 + 2 marks', 'Second reason')),
     '4-0', POP),
])

PART_TWO += [
    T('p2-11b', P2, '11B', '', 30, 15, L(15, 'Changing Urban Functions'),
      (L(15, 'Examine how the functions of urban centres can change over time', 'Irish example(s).'),),
      (S(39, 'Functions identified · 2 + 2 marks', 'Annotation'),),
      (pair('Functions identified · 2 + 2 marks', 'Functions identified'),
       fixed('Example Irish urban centre', 2, 'Example Irish urban centre · 2 marks'),
       srp('Examination', 12, 'Examination · 12 x SRPs')),
      '4-3', URB, ID + 'p2-q11b', True),
    T('p2-11c', P2, '11C', '', 30, 15, L(15, 'Population Characteristics – Ireland'),
      (L(15, 'Describe and explain how the characteristics of Ireland’s population have changed', '1950’s.'),),
      (S(40, 'Change in population characteristics identified · 2m', 'Annotation'),),
      (fixed('Change in population characteristics identified', 2, 'Change in population characteristics identified · 2m'),
       srp('Description/explanation', 14, f'Description / Explanation · 14 x {SRPS}')),
      '4-0', POP, ID + 'p2-q11c', True),
]

Q12AS = (L(16, 'Examine the table above showing the percentage of people aged over 65', 'following questions.'),)
PART_TWO += romans('12A', 16, L(16, 'Population', nth=0), Q12AS, ID + 'p2-q12a', ('page',), [
    ('(i)', 16, L(16, '(i) Using graph paper, draw a suitable graph to illustrate this data.'),
     (S(41, 'Bar Chart · Pie Chart', 'Annotation'),), GRAPH, '2-0', TG),
    ('(ii)', 4, L(16, '(ii) Explain briefly one challenge faced by countries with high numbers of people', 'over 65 years.'),
     (S(41, 'Valid explanation · 2 + 2 marks', None),), (pair('Valid explanation · 2 + 2 marks', 'Challenge'),),
     '4-0', POP),
])

PART_TWO += [
    T('p2-12b', P2, '12B', '', 30, 16, L(16, 'Future Urbanism'),
      (L(16, 'Discuss two issues facing cities of the future in the developed world.'),),
      (S(42, 'Two issues identified', 'Annotation'),),
      (pair('Two issues identified · 2m + 2m', 'Two issues identified'),
       srp('Discussion of the two issues (7/6 SRPs each)', 13,
           (f'Discussion of issue one · 7/6 x {SRPS}', f'Discussion of issue two · 7/6 x {SRPS}'))),
      '4-5', URB, ID + 'p2-q12b', True),
    T('p2-12c', P2, '12C', '', 30, 16, L(16, 'Settlement Distribution'),
      (L(16, 'Examine the 1:50 000 Ordnance Survey map of Clonmel accompanying this paper.'),
       L(16, 'Using evidence from the map, account for variations in settlement distribution', 'Northing 21.')),
      (S(43, 'Variations in settlement distribution identified · 2m + 2m', 'Annotation'),),
      (pair('Variations in settlement distribution identified · 2m + 2m', 'Variations identified'),
       fixed('OS map evidence', 2, 'OS map evidence · 2m'), srp('Examination', 12, f'Examination · 12 x {SRPS}')),
      '4-3', URB + MAP, ID + 'p2-q12c', False, ('map', 'legend')),
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
           L(18, '‘Empowering people is a way of linking economic growth', 'their impact on development.'), 47, '5-2', GI),
    option('14', 18, L(18, 'Global Interdependence'), 0,
           L(18, 'Examine how social and/or political decisions', 'Human rights issues.'), 48, '5-1', GI,
           after='14.', end='15.'),
    option('15', 18, L(18, 'Global Interdependence'), 0,
           L(18, 'Examine sustainable development as a model for future development.'), 48, '5-3', GI, after='15.'),
    option('16', 18, L(18, 'Geoecology'), 1,
           L(18, 'Explain how soil characteristics impact on soil development.'), 49, '6-0', GE),
    option('17', 18, L(18, 'Geoecology'), 1,
           L(18, 'With reference to one biome that you have studied', 'within the biome.'), 50, '6-2', GE,
           after='17.', end='18.'),
    option('18', 18, L(18, 'Geoecology'), 1,
           L(18, 'Examine how desertification and conservation have impacted on soil.'), 50, '6-1', GE, after='18.'),
    option('19', 19, L(19, 'Culture and Identity'), 0,
           L(19, 'Examine the importance of religion as a cultural indicator.'), 51, '7-0', CI),
    option('20', 19, L(19, 'Culture and Identity'), 0,
           L(19, 'Examine the effects of political and/or physical boundaries on cultural groups.'), 52, '7-1', CI,
           after='20.', end='21.'),
    option('21', 19, L(19, 'Culture and Identity'), 0,
           L(19, '‘Cultural identity is defined by many diverse factors’.', 'European region you have studied.'),
           52, '7-2', CI, after='21.'),
    option('22', 19, L(19, 'The Atmosphere – Ocean Environment'), 1,
           L(19, '‘Climate characteristics have an influence on economic development.’', 'Tourism.'), 53, '8-5', AO),
    option('23', 19, L(19, 'The Atmosphere – Ocean Environment'), 1,
           L(19, 'Describe the formation of each of the following', 'Land and sea breezes.'), 54, '8-3', AO,
           after='23.', end='24.'),
    option('24', 19, L(19, 'The Atmosphere – Ocean Environment'), 1,
           L(19, 'Climate characteristics change over space and time. Discuss.'), 54, '8-4', AO, after='24.'),
]

TASKS = [*PART_ONE, *PART_TWO, *OPTIONS]

ID_CORRECTION_REASON = (
    'The shipped card held every part of a question the scheme prices part by '
    'part. Its id is kept on the first separately priced part; the other parts '
    'are new cards with their own published allocation.')

# Every 2022 Higher card id live on origin/main before this review (73). Each must survive.
LEGACY_IDS = [
    'geography-2022-hl-p1-q1',
    'geography-2022-hl-p1-q2',
    'geography-2022-hl-p1-q3',
    'geography-2022-hl-p1-q4',
    'geography-2022-hl-p1-q5',
    'geography-2022-hl-p1-q9',
    'geography-2022-hl-p1-q10',
    'geography-2022-hl-p1-q11',
    'geography-2022-hl-p1-q12',
    'geography-2022-hl-p2-q1b',
    'geography-2022-hl-p2-q1c-mining',
    'geography-2022-hl-p2-q1c-extraction-of-building-materials',
    'geography-2022-hl-p2-q1c-oil-gas-exploitation',
    'geography-2022-hl-p2-q1c-geothermal-energy-production',
    'geography-2022-hl-p2-q2a',
    'geography-2022-hl-p2-q2b-route-i-fluvial-landform',
    'geography-2022-hl-p2-q2b-route-i-coastal-landform',
    'geography-2022-hl-p2-q2b-route-i-glacial-landform',
    'geography-2022-hl-p2-q2b-route-ii',
    'geography-2022-hl-p2-q2c',
    'geography-2022-hl-p2-q3a',
    'geography-2022-hl-p2-q3b',
    'geography-2022-hl-p2-q3c-the-impact-of-dams-on-river-proces',
    'geography-2022-hl-p2-q3c-the-impact-of-coastal-defence-work',
    'geography-2022-hl-p2-q3c-the-impact-of-human-activity-on-ma',
    'geography-2022-hl-p2-q4a',
    'geography-2022-hl-p2-q4b',
    'geography-2022-hl-p2-q4c',
    'geography-2022-hl-p2-q5a',
    'geography-2022-hl-p2-q5b',
    'geography-2022-hl-p2-q5c',
    'geography-2022-hl-p2-q6a',
    'geography-2022-hl-p2-q6b-relief-climate',
    'geography-2022-hl-p2-q6b-relief-markets',
    'geography-2022-hl-p2-q6b-climate-markets',
    'geography-2022-hl-p2-q6c',
    'geography-2022-hl-p2-q7b-sourcing-of-raw-materials-and-comp-location-of-processing-units',
    'geography-2022-hl-p2-q7b-sourcing-of-raw-materials-and-comp-location-of-markets',
    'geography-2022-hl-p2-q7b-location-of-processing-units-location-of-markets',
    'geography-2022-hl-p2-q7c',
    'geography-2022-hl-p2-q8a',
    'geography-2022-hl-p2-q8b',
    'geography-2022-hl-p2-q9a',
    'geography-2022-hl-p2-q9b-footloose-industries-physical-factors-human-factors',
    'geography-2022-hl-p2-q9b-footloose-industries-physical-factors-political-factors',
    'geography-2022-hl-p2-q9b-footloose-industries-human-factors-political-factors',
    'geography-2022-hl-p2-q9b-financial-services-physical-factors-human-factors',
    'geography-2022-hl-p2-q9b-financial-services-physical-factors-political-factors',
    'geography-2022-hl-p2-q9b-financial-services-human-factors-political-factors',
    'geography-2022-hl-p2-q9b-mass-tourism-physical-factors-human-factors',
    'geography-2022-hl-p2-q9b-mass-tourism-physical-factors-political-factors',
    'geography-2022-hl-p2-q9b-mass-tourism-human-factors-political-factors',
    'geography-2022-hl-p2-q9c',
    'geography-2022-hl-p2-q10b-migration-policy-in-the-european-u',
    'geography-2022-hl-p2-q10b-rural-to-urban-migration-in-the-de',
    'geography-2022-hl-p2-q10c',
    'geography-2022-hl-p2-q11a',
    'geography-2022-hl-p2-q11b',
    'geography-2022-hl-p2-q11c',
    'geography-2022-hl-p2-q12a',
    'geography-2022-hl-p2-q12b',
    'geography-2022-hl-p2-q13',
    'geography-2022-hl-p2-q14',
    'geography-2022-hl-p2-q15',
    'geography-2022-hl-p2-q16',
    'geography-2022-hl-p2-q17',
    'geography-2022-hl-p2-q18',
    'geography-2022-hl-p2-q19',
    'geography-2022-hl-p2-q20',
    'geography-2022-hl-p2-q21',
    'geography-2022-hl-p2-q22',
    'geography-2022-hl-p2-q23',
    'geography-2022-hl-p2-q24',
]
