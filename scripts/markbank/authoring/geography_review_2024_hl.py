"""Independent review ledger: Leaving Certificate Geography 2024 Higher Level.

Sources (English editions, Paper Trail index; sizes and SHA-256 pinned in
EXPECTED_SOURCES and the generated audit): Part One and Answerbook
LC005ALP042EV (48 pages), Part Two LC005ALP043EV (20 pages), marking scheme
LC005ALP000EV (64 pages), and the common companions — the 1:50 000 Bantry map
LC005CLP003EV (fetched from Paper Trail storage; not in the harvested
corpus), its legend LC005CLPC00EV and the Bantry aerial photograph
LC005CLP004EV, which the SEC publishes only as a JPEG.

Visual sweep (every page rendered and read on 2026-10-12):
  Part One booklet p1 cover (COVID-adjusted paper note); p2 instructions
  (Part One "Attempt any TEN", 80 marks; Part Two "attempt FOUR", 320 marks);
  p3-p13 Questions 1-12 (p8 holds Q6 and Q7); p14 Part Two answerbook
  instructions; p15-p18 graph paper; p19-p47 lined answer pages; p48 back.
  Part Two booklet p1 cover; p2 Part Two instructions; p3-p8 Sections 1-2
  (Q1-Q6); p9 Section 3 divider; p10-p15 Electives (Q7-Q12; 12A prints its
  own historical map of Bantry); p16 Section 4 divider and note; p17-p18
  Options (Q13-Q24); p19-p20 "Do not hand this up" and back.
  Scheme p1 cover; p2-p3 notes and annotation key; p4 Part One table (two
  columns: Q1-Q6, Q7-Q12); p5 the 2024 Part Two adjustment rule; p6-p24
  Q1-Q6 (2B route (ii) on p11); p25 divider; p26-p43 Q7-Q12 (10A(ii) on p36,
  12A's bullets run onto p42); p44 divider; p45 option outline and Overall
  Coherence descriptors; p46 option annotations; p47-p54 Q13-Q24; p55-p58
  Geographical Investigation (coursework); p59 investigation topics; p60
  Irish-language bonus marks; p61-p63 blank; p64 back cover.
  Companions: Bantry map extract (Bantry Bay, Mullaghmesha, the Mealagh
  river, the Sheep's Head Way); OS legend sheet; oblique aerial photograph
  of Bantry.

Companions. Part One Q1, Q7 and Q9 (map, legend), Q8 (aerial and the
printed street map); Part Two 1A, 7A and 8B (map, legend) and 10B (aerial
OR map) were held back before this review because their companions were not
wired. Each now carries the exact official documents it names; 10B's two
printed evidence routes each carry only their own evidence.

Boundaries and tariffs follow the 2025 Higher ledger: every part the scheme
prices separately is a task; a matching/location table under one printed
instruction is one task with a criterion per scheme row, each checked
against the paper: Q1 W 03 55 River Confluence, V 99 50 Headland, W 02 55 Ox
bow lake, W 08 50 Tarn (checked on the map extract); Q2 Carbonation=C,
Freeze-thaw=A, Exfoliation=B, Hydrolysis=D; Q3 Paired terraces=D, Incised
meander=B, Waterfall=A, Knickpoint=C; Q4 Sand bar=C, Tombolo=D, Lagoon=B,
Sand spit=A; Q5 Faultline=C, Focus=E, Seismic wave=F, Epicentre=D,
Liquefaction=B, Landslide=A; Q6 rows follow the printed descriptions; Q12
Cutaway peatlands=C, Meltwater pond=B, Nile=A, Rice fields=D. Q2 and Q6
print (i) and (ii) in one table but price them separately, so each is its
own task.
"""

import itertools

from geography_review import (
    Criterion, Lift, Route, SchemeSlice, Task, evens, fixed, slug, srp, sums, upto,
)

YEAR = 2024
LEVEL = 'higher'
PAPER_PAGES = {1: 48, 2: 20}
SCHEME_PAGES = 64
QUESTION_TARIFFS = {1: {str(n): 8 for n in range(1, 13)},
                    2: {**{f'{n}{x}': (20 if x == 'A' else 30)
                           for n in range(1, 13) for x in 'ABC'},
                        **{str(n): 80 for n in range(13, 25)}}}

EXPECTED_SOURCES = {
    'paper1': ('LC005ALP042EV.pdf', 3284219),
    'paper2': ('LC005ALP043EV.pdf', 2581654),
    'scheme': ('LC005ALP000EV.pdf', 2157023),
    'map': ('LC005CLP003EV.pdf', 14358379),
    'legend': ('LC005CLPC00EV.pdf', 626267),
    'aerial': ('LC005CLP004EV.jpg', 5609640),
}

PAGE_REVIEW = {
    'paper1': {1: 'cover', 2: 'instructions', **{p: 'question' for p in range(3, 14)},
               14: 'answerbook instructions', **{p: 'graph-paper answer page' for p in range(15, 19)},
               **{p: 'lined answer page' for p in range(19, 48)}, 48: 'copyright/back cover'},
    'paper2': {1: 'cover', 2: 'Part Two instructions',
               **{p: 'question' for p in (3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15, 17, 18)},
               9: 'section divider', 16: 'section divider and option note',
               19: 'do not hand this up', 20: 'copyright/back cover'},
    'scheme': {1: 'cover', 2: 'notes', 3: 'notes and annotation key', 4: 'Part One table',
               5: 'Part Two adjustment rule (2024 additional choice)',
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
    [2, 3, 'one of the following'],
    [2, 4, 'answer (i) or (ii)'], [2, 4, 'or one'], [2, 4, 'or one'],
    [2, 6, 'two of the following'],
    [2, 7, 'one of the following'],
    [2, 11, 'choose'], [2, 11, 'choose'],
    [2, 17, 'any three'],
]
SELECTION_REVIEW = [
    {'scan': [[1, 2, 'attempt any ten'], [1, 2, 'attempt four'], [1, 3, 'attempt any ten'],
              [2, 2, 'attempt four']],
     'kind': 'exam-attempt-rule',
     'reason': 'Part One any ten of twelve and Part Two four questions are attempt rules; every question is carded.'},
    {'scan': [[2, 3, 'one of the following']], 'kind': 'closed-choose-one',
     'reason': '1B one of three printed impacts -> 3 routes.'},
    {'scan': [[2, 4, 'answer (i) or (ii)'], [2, 4, 'or one'], [2, 4, 'or one']], 'kind': 'closed-route',
     'reason': '2B: (i) or (ii); (i) offers one fluvial OR one coastal OR one glacial landform -> 4 routes.'},
    {'scan': [[2, 6, 'two of the following']], 'kind': 'closed-choose-two',
     'reason': '4C two of four printed factors -> C(4,2) = 6 routes.'},
    {'scan': [[2, 7, 'one of the following']], 'kind': 'closed-choose-one',
     'reason': '5B one of two printed factors (climate, relief) -> 2 routes.'},
    {'scan': [[2, 17, 'any three']], 'kind': 'closed-choose-three',
     'reason': '17 any three of four printed characteristics -> C(4,3) = 4 routes.'},
    {'scan': [[2, 11, 'choose'], [2, 11, 'choose']], 'kind': 'not-a-selection',
     'reason': '8B "might choose to locate" / "might choose not to locate" describe the fish processing plant, not a candidate choice.'},
    {'scan': [], 'kind': 'inline-closed-route',
     'reason': '4B "culture or climate" -> 2 routes; 10B evidence "from the aerial photograph OR from the 1:50 000 Ordnance Survey map" -> 2 routes, each carrying only its own evidence (no directive word the scan reads; the route text is anchored on the paper).'},
    {'scan': [], 'kind': 'open-response',
     'reason': 'Open choices are not fanned out: "one urban area", "one multinational company", "example(s)", 6B "a Continental / Sub-Continental region", 11C "two challenges". Compulsory lists stay whole: 2C intrusive AND extrusive, 9C and 14 and 18 each bullet, 9B internal AND external trade.'},
]

P1, P2 = 1, 2
LEFT = (0.0, 0.0, 0.5, 1.0)
RIGHT = (0.5, 0.0, 1.0, 1.0)
# Q2 prints (i) and (ii) side by side in the left column of the Part One table.
Q2_I = (0.0, 0.0, 0.235, 1.0)
Q2_II = (0.235, 0.0, 0.5, 1.0)
ID = 'geography-2024-hl-'
H = 'geography-higher-'
SRPS = 'SRP’s'


def L(page, start, end=None, nth=None):
    return Lift(page, start, end, None, nth)


def S(page, start, end=None, clip=None, after=None, table=False):
    return SchemeSlice(page, start, end, clip, after, table)


def T(key, part, q, sub, marks, page, title, prompt, scheme, criteria, topic, atlas, card_id,
      legacy, sources=(), stem=(), routes=(), row_labels=()):
    return Task(key, part, q, sub, marks, page, title, prompt, scheme, criteria, topic, atlas,
                sources, card_id, legacy, stem=stem, routes=routes, row_labels=row_labels)


def rows(lines, marks=1):
    return tuple(fixed(f'Row {i}', marks, line) for i, line in enumerate(lines, 1))


def pair(line, label):
    return fixed(label, 4, line, (0, 2, 4))


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
MAP = (H + 'mapwork',)
AER = (H + 'aerial-photos',)
TG = (H + 'tablesgraphs-questions',)
WX = (H + 'weather-climate',)
IRL = (H + 'regions-ireland',)
EURO = (H + 'regions-european',)
CONT = (H + 'regions-continental',)

PART_ONE = [
    T('p1-1', P1, '1', '', 8, 3, L(3, 'Landscape Identification'),
      (L(3, 'In the table below, match each of the following features', 'River confluence.'),),
      (S(4, 'River Confluence', 'Q.2', LEFT),),
      rows(['River Confluence 2m', 'Headland 2m', 'Ox bow lake 2m', 'Tarn 2m'], 2),
      '2-6', MAP + RIVERS + SEA + GLAC, ID + 'p1-q1', False, ('map', 'legend'),
      (L(3, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper.'),),
      row_labels=(L(3, 'W 03 55'), L(3, 'V 99 50'), L(3, 'W 02 55'), L(3, 'W 08 50'))),
]

Q2S = (L(4, 'Examine the photographs above and answer each of the following questions.'),)
PART_ONE += [
    T('p1-2-i', P1, '2', '(i)', 4, 4, L(4, 'Weathering'),
      (L(4, '(i) Match each of the photographs A, B, C and D with the process', 'the table below.'),),
      (S(4, '(i) C 1m', 'Q.3', Q2_I, 'Q.2'),), rows(['(i) C 1m', 'A 1m', 'B 1m', 'D 1m']),
      '0-8', RW, ID + 'p1-q2', True, ('page',), Q2S,
      row_labels=(L(4, 'Carbonation'), L(4, 'Freeze-thaw action'), L(4, 'Exfoliation'), L(4, 'Hydrolysis'))),
    T('p1-2-ii', P1, '2', '(ii)', 4, 4, L(4, 'Weathering'),
      (L(4, '(ii) Indicate, by ticking (✓) the correct box', 'physical/mechanical weathering.'),),
      (S(4, '(ii) Chemical 1m', 'ation 2m', Q2_II),),
      rows(['(ii) Chemical 1m', '=Physical/Mechanical 1m@0', '=Physical/Mechanical 1m@1', '=Chemical 1m']),
      '0-8', RW, ID + 'p1-q2-ii', False, ('page',), Q2S,
      row_labels=(L(4, 'Carbonation'), L(4, 'Freeze-thaw action'), L(4, 'Exfoliation'), L(4, 'Hydrolysis'))),
]

Q3S = (L(5, 'Examine the diagram above of a landscape where a river has a new base level', 'following questions.'),)
PART_ONE += [
    T('p1-3-i', P1, '3', '(i)', 4, 5, L(5, 'Fluvial Adjustment'),
      (L(5, '(i) Match each of the items labelled A, B, C and D', 'in the table below.'),),
      (S(4, '(i) D 1m', '(ii) Rejuvenation', LEFT),), rows(['(i) D 1m', 'B 1m', 'A 1m', 'C 1m']),
      '0-9', RIVERS, ID + 'p1-q3', True, ('page',), Q3S,
      row_labels=(L(5, 'Paired terraces'), L(5, 'Incised meander'), L(5, 'Waterfall'), L(5, 'Knickpoint'))),
    T('p1-3-ii', P1, '3', '(ii)', 2, 5, L(5, 'Fluvial Adjustment'),
      (L(5, '(ii) What is the name of the process', 'change in base level?'),),
      (S(4, '(ii) Rejuvenation', '(iii) Valid reason', LEFT),), (fixed('Process', 2, '(ii) Rejuvenation 2m'),),
      '0-9', RIVERS, ID + 'p1-q3-ii', False, ('page',), Q3S),
    T('p1-3-iii', P1, '3', '(iii)', 2, 5, L(5, 'Fluvial Adjustment'),
      (L(5, '(iii) State one reason why a river’s base level can change.'),),
      (S(4, '(iii) Valid reason', 'Q.4', LEFT),), (fixed('Reason', 2, '(iii) Valid reason 2m'),),
      '0-9', RIVERS, ID + 'p1-q3-iii', False, ('page',), Q3S),
]

Q4S = (L(6, 'Examine the photographs above and answer each of the following questions.'),)
TF4 = L(6, '(ii) Indicate whether each of the following statements is true or false', 'correct box.')
PART_ONE += [
    T('p1-4-i', P1, '4', '(i)', 4, 6, L(6, 'Coastal Features and Processes'),
      (L(6, '(i) Match each of the letters A, B, C and D', 'table below.'),),
      (S(4, '(i) C 1m', '(ii) (a) True', LEFT, 'Q.4'),), rows(['(i) C 1m', 'D 1m', 'B 1m', 'A 1m']),
      '0-10', SEA, ID + 'p1-q4', True, ('page',), Q4S,
      row_labels=(L(6, 'Sand bar'), L(6, 'Tombolo'), L(6, 'Lagoon'), L(6, 'Sand spit'))),
    T('p1-4-ii-a', P1, '4', '(ii)(a)', 2, 6, L(6, 'Coastal Features and Processes'),
      (TF4, L(6, '(a) Longshore drift is a process involved', 'in part (i).')),
      (S(4, '(ii) (a) True', '(b) True', LEFT),), (fixed('Statement (a)', 2, '(ii) (a) True 2m'),),
      '0-10', SEA, ID + 'p1-q4-ii-a', False, ('page',), Q4S),
    T('p1-4-ii-b', P1, '4', '(ii)(b)', 2, 6, L(6, 'Coastal Features and Processes'),
      (TF4, L(6, '(b) Waves are known as constructive when the swash is greater than the backwash.')),
      (S(4, '(b) True', 'Q.5', LEFT),), (fixed('Statement (b)', 2, '(b) True 2m'),),
      '0-10', SEA, ID + 'p1-q4-ii-b', False, ('page',), Q4S),
]

Q5S = (L(7, 'Examine the diagram above of an earthquake and answer each of the following questions.'),)
PART_ONE += [
    T('p1-5-i', P1, '5', '(i)', 6, 7, L(7, 'Earthquakes'),
      (L(7, '(i) Match each of the items labelled on the diagram', 'in the table below.'),),
      (S(4, '(i) C 1m', '(ii) True', LEFT, 'Q.5'),), rows(['(i) C 1m', 'E 1m', 'F 1m', 'D 1m', 'B 1m', 'A 1m']),
      '0-7', EV, ID + 'p1-q5', True, ('page',), Q5S,
      row_labels=(L(7, 'Faultline'), L(7, 'Focus'), L(7, 'Seismic wave'), L(7, 'Epicentre'),
                  L(7, 'Liquefaction'), L(7, 'Landslide'))),
    T('p1-5-ii', P1, '5', '(ii)', 2, 7, L(7, 'Earthquakes'),
      (L(7, '(ii) Indicate whether the following statement is true or false', 'the correct box.'),
       L(7, 'The Pacific Ring of Fire is an area where many earthquakes occur.')),
      (S(4, '(ii) True', 'Q.6', LEFT),), (fixed('True or false', 2, '(ii) True 2m'),),
      '0-7', EV, ID + 'p1-q5-ii', False, ('page',), Q5S),
]

Q6S = (L(8, 'Answer each of the following questions in the table below.'),)
Q6_ROWS = (L(8, 'A region with high population', 'cities and towns.'),
           L(8, 'A region with a unique landscape', 'structure or relief.'),
           L(8, 'A region with unique temperature', 'characteristics.'),
           L(8, 'A region involved in governing', 'of an area.'))
REGIONS = (H + 'regions-ireland', H + 'regions-european')
PART_ONE += [
    T('p1-6-i', P1, '6', '(i)', 4, 8, L(8, 'Concept of a Region'),
      (L(8, '(i) Match each of the following types of region', 'matches it:'), L(8, 'Urban', 'Geomorphological')),
      (S(4, '(i) Urban', '(ii) Berlin', LEFT),),
      rows(['(i) Urban 1m', 'Geomorphological 1m', 'Climatic 1m', 'Administrative 1m']),
      '1-0', REGIONS, ID + 'p1-q6', True, ('page',), Q6S, row_labels=Q6_ROWS),
    T('p1-6-ii', P1, '6', '(ii)', 4, 8, L(8, 'Concept of a Region'),
      (L(8, '(ii) Match each of the following examples of regions', 'matches it:'), L(8, 'The Burren', 'Hot Desert')),
      (S(4, '(ii) Berlin', 'Page 4', LEFT),),
      rows(['(ii) Berlin 1m', 'The Burren 1m', 'Hot Desert 1m', 'Co. Leitrim 1m']),
      '1-0', REGIONS, ID + 'p1-q6-ii', False, ('page',), Q6S, row_labels=Q6_ROWS),
]

Q7S = (L(8, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper, and',
         'following questions.'),)
PART_ONE += p1_romans('7', 8, L(8, 'Map Skills'), Q7S, ID + 'p1-q7', False, ('map', 'legend'), [
    ('(i)', 2, L(8, '(i) Give a six-figure grid reference for the point where the R584 meets the N71.'),
     S(4, '(i) W 006 533', '(ii) 8.5', RIGHT), (fixed('Grid reference', 2, '(i) W 006 533 · 2m'),), '2-6', MAP),
    ('(ii)', 2, L(8, '(ii) Measure the straight-line distance', 'Knocknaveagh (W 015 475).'),
     S(4, '(ii) 8.5', '(iii) Star Shaped Fort', RIGHT), (fixed('Distance', 2, '(ii) 8.5 (km) 2m'),), '2-6', MAP),
    ('(iii)', 2, L(8, '(iii) Name the antiquity shown at grid reference V 996 493.'),
     S(4, '(iii) Star Shaped Fort', '(iv) 18', RIGHT), (fixed('Antiquity', 2, '(iii) Star Shaped Fort 2m'),), '2-6', MAP),
    ('(iv)', 2, L(8, '(iv) Calculate the area of subzone V', 'shown on the map.'),
     S(4, '(iv) 18', 'Q.8', RIGHT), (fixed('Area', 2, '(iv) 18 (km²) 2m'),), '2-6', MAP),
])

PART_ONE.append(T(
    'p1-8', P1, '8', '', 8, 9, L(9, 'Aerial Photograph', nth=0),
    (L(9, 'Locate each of the features labelled A, B, C, D and E above', 'accompanying this paper.'),
     L(9, 'Using accepted notation, give the location', 'One has been completed for you.')),
    (S(4, 'B Centre Middleground', 'Q.9', RIGHT),),
    (fixed('B', 2, 'B Centre Middleground 2m'), fixed('C', 2, 'C Right Foreground 2m'),
     fixed('D', 2, 'D Right Background 2m'), fixed('E', 2, 'E Left Middleground 2m')),
    '2-8', AER, ID + 'p1-q8', False, ('page', 'aerial'),
    (L(9, 'Examine the aerial photograph of Bantry accompanying this paper', 'covered by the aerial photograph.'),
     L(9, 'Note: The orientation of the aerial photograph', 'orientation of the street map below.')),
    row_labels=(L(9, 'Town square'), L(9, 'Pier'), L(9, 'Community College'), L(9, 'Housing'))))

Q9S = (L(10, 'Locate point X, W 090 550', 'Both points are on Easting 09.'),
       L(10, 'Figure 1 shows an elevation profile', 'on the Ordnance Survey map.'),
       L(10, 'Using the 1:50 000 Ordnance Survey map and legend and the elevation profile above,',
         'following questions.'))
PART_ONE += p1_romans('9', 10, L(10, 'Ordnance Survey Map'), Q9S, ID + 'p1-q9', False, ('page', 'map', 'legend'), [
    ('(i)', 2, L(10, '(i) Name the river that crosses the profile at A.'),
     S(4, '(i) Mealagh River', '(ii) Even', RIGHT), (fixed('River', 2, '(i) Mealagh River 2m'),), '2-6', MAP),
    ('(ii)', 2, L(10, '(ii) What type of slope is found between points B and C on the profile?'),
     S(4, '(ii) Even', '(iii) Glanaclougha Loop', RIGHT), (fixed('Slope', 2, '(ii) Even 2m'),), '2-6', MAP),
    ('(iii)', 2, (L(10, '(iii) Which of the following waymarked walks', 'labelled D?'), L(10, 'Beara-Breifne Way'),
                  L(10, 'Sheep’s Head Way East'), L(10, 'Glanaclougha Loop')),
     S(4, '(iii) Glanaclougha Loop', '(iv) Coniferous', RIGHT), (fixed('Waymarked walk', 2, '(iii) Glanaclougha Loop 2m'),),
     '2-6', MAP),
    ('(iv)', 2, L(10, '(iv) What type of forestry is located at E?'),
     S(4, '(iv) Coniferous', 'Q10', RIGHT), (fixed('Forestry', 2, '(iv) Coniferous (Plantation) 2m'),), '2-6', MAP),
])

Q10S = (L(11, 'Examine the map above showing the hours of sunshine', 'answer the following questions.'),)
PART_ONE += p1_romans('10', 11, L(11, 'Sunshine in Ireland'), Q10S, ID + 'p1-q10', True, ('page',), [
    ('(i)', 2, L(11, '(i) Which county has the lowest hours of sunshine?'),
     S(4, '(i) Mayo', '(ii) Four', RIGHT), (fixed('County', 2, '(i) Mayo 2m'),), '2-0', TG),
    ('(ii)', 2, L(11, '(ii) How many counties have more than 1,500 hours of sunshine?'),
     S(4, '(ii) Four', '(iii) 146', RIGHT), (fixed('Number', 2, '(ii) Four 2m'),), '2-0', TG),
    ('(iii)', 2, L(11, '(iii) Calculate the difference in hours of sunshine between Cork and Donegal.'),
     S(4, '(iii) 146', '(iv) Isohels', RIGHT), (fixed('Difference', 2, '(iii) 146 2m'),), '2-0', TG),
    ('(iv)', 2, L(11, '(iv) What is the name given to lines on a weather map', 'equal sunshine?'),
     S(4, '(iv) Isohels', 'Q11', RIGHT), (fixed('Term', 2, '(iv) Isohels 2m'),), '2-7', WX),
])

Q11S = (L(12, 'Examine the bar chart above showing statistics on afforestation', 'following questions.'),)
PART_ONE += p1_romans('11', 12, L(12, 'Statistical Interpretation'), Q11S, ID + 'p1-q11', True, ('page',), [
    ('(i)', 2, L(12, '(i) How many hectares of broadleaf trees were afforested in Ireland in 2018?'),
     S(4, '(i) 1070', '(ii) 2020', RIGHT), (fixed('Hectares', 2, '(i) 1070 · 2m'),), '2-0', TG),
    ('(ii)', 2, L(12, '(ii) Which year had a total afforestation of 2,435 hectares?'),
     S(4, '(ii) 2020', '(iii) 1314', RIGHT), (fixed('Year', 2, '(ii) 2020 · 2m'),), '2-0', TG),
    ('(iii)', 2, L(12, '(iii) Calculate X, the number of hectares planted with conifers in 2022.'),
     S(4, '(iii) 1314', '(iv) Valid explanation', RIGHT), (fixed('Calculation', 2, '(iii) 1314 2m'),), '2-0', TG),
    ('(iv)', 2, L(12, '(iv) Explain briefly one environmental benefit of increased afforestation.'),
     S(4, '(iv) Valid explanation', 'Q12', RIGHT),
     (fixed('Benefit', 2, '(iv) Valid explanation 1 + 1m', (0, 1, 2)),),
     '3-4', (H + 'economic-environmental-impact',)),
])

PART_ONE.append(T(
    'p1-12', P1, '12', '', 8, 13, L(13, 'Satellite Interpretation'),
    (L(13, 'Match each of the images A, B, C and D', 'below.'),),
    (S(4, 'C 2m', 'f 60', RIGHT, 'Q12'),), rows(['=C 2m', '=B 2m', '=A 2m', '=D 2m'], 2),
    '2-8', AER, ID + 'p1-q12', True, ('page',),
    (L(13, 'Examine the satellite images above and answer the question below.'),),
    row_labels=(L(13, 'Cutaway peatlands, Ireland'), L(13, 'Meltwater pond on Greenland glacier'),
                L(13, 'Farmland along the Nile Floodplain'), L(13, 'Flooded rice fields, Louisiana'))))


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
IMPACTS = ('The impact of flood control measures on river processes',
           'The impact of coastal defence measures on coastal processes',
           'The impact of human activities on mass movement processes.')

PART_TWO = [
    T('p2-1a', P2, '1A', '', 20, 3, L(3, 'Ordnance Survey Map'),
      (L(3, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper.', 'at Mullaghmesha.'),),
      (S(6, 'Sketch Outline', None),), OS_SKETCH, '2-6', MAP, ID + 'p2-q1a', False, ('map', 'legend'),
      row_labels=(None, L(3, 'The coastline'), L(3, 'The 18 hole golf course, north of Bantry town'),
                  L(3, 'The entire area of Lough Bofinna'),
                  L(3, 'The entire area of land above 400 metres at Mullaghmesha'))),
    T('p2-1b', P2, '1B', '', 30, 3, L(3, 'Human Interaction with Surface Processes'),
      (L(3, 'Human activity impacts on surface processes.'),
       L(3, 'Examine this statement with reference to one of the following:', 'mass movement processes.')),
      (S(7, 'Impact on process identified · 2 marks', 'Annotation'),),
      (fixed('Impact on process identified', 2, 'Impact on process identified · 2 marks'),
       srp('Examination', 14, f'Examination · 14 x {SRPS}')),
      '0-6', RIVERS, ID + 'p2-q1b-the-impact-of-flood-control-measur', True,
      routes=bullet_routes('p2-q1b-', IMPACTS, atlas=dict(zip(IMPACTS, (RIVERS, SEA, RW))))),
    T('p2-1c', P2, '1C', '', 30, 3, L(3, 'Destructive Plate Boundaries'),
      (L(3, 'Discuss the impacts of destructive plate boundaries', 'have studied.'),),
      (S(8, 'Impact identified · 2 marks', 'Annotation'),),
      (fixed('Impact identified', 2, 'Impact identified · 2 marks'), fixed('Example', 2, 'Example · 2 marks'),
       srp('Discussion', 13, f'Discussion · 13 x {SRPS}')),
      '0-0', PS + EV, ID + 'p2-q1c', True),
]

Q2AS = (L(4, 'Examine the diagram above which shows different faults', 'following questions.'),)
PART_TWO += romans('2A', 4, L(4, 'Landscape Deformation'), Q2AS, ID + 'p2-q2a', ('page',), [
    ('(i)', 4, L(4, '(i) Name each of the types of fault labelled A and B.'),
     (S(9, '(i) · A = Normal', '(ii) · C = Escarpment'),),
     (fixed('Fault A', 2, '(i) · A = Normal · 2 marks'), fixed('Fault B', 2, 'B = Reverse · 2 marks')), '0-2', RW),
    ('(ii)', 4, L(4, '(ii) Name each of the landforms created by faulting labelled C and D.'),
     (S(9, '(ii) · C = Escarpment', '(iii) · Tear'),),
     (fixed('Landform C', 2, '(ii) · C = Escarpment · 2 marks'), fixed('Landform D', 2, 'D = Block Mountain · 2 marks')),
     '0-2', RW),
    ('(iii)', 2, L(4, '(iii) What type of fault is found where the process of shearing occurs?'),
     (S(9, '(iii) · Tear', '(iv) · Valid explanation'),), (fixed('Fault type', 2, '(iii) · Tear · 2 marks'),), '0-2', RW),
    ('(iv)', 4, L(4, '(iv) Explain briefly what causes faulting.'),
     (S(9, '(iv) · Valid explanation', '(v) · Caledonian'),), (pair('(iv) · Valid explanation · 2 + 2 marks', 'Explanation'),),
     '0-2', RW),
    ('(v)', 4, L(4, '(v) Name two periods of fold mountain building', 'last 400 million years.'),
     (S(9, '(v) · Caledonian', '(vi) · False'),), (pair('(v) · Caledonian & Armorican · 2 + 2 marks', 'Two periods'),),
     '0-2', RW),
    ('(vi)', 2, L(4, '(vi) In your answerbook, state whether the following statement is true or false:', 'pushed upwards.'),
     (S(9, '(vi) · False', None),), (fixed('True or false', 2, '(vi) · False · 2 marks'),), '0-2', RW),
])

PART_TWO += [
    T('p2-2b', P2, '2B', '', 30, 4, L(4, 'Landscape Development'),
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
    T('p2-2c', P2, '2C', '', 30, 4, L(4, 'Volcanic Activity'),
      (L(4, 'Examine the influence of volcanic activity on the development of the Irish landscape', 'Extrusive features.'),),
      (S(12, 'Examination with reference to intrusive features', 'Annotation'),),
      (split('Examination of intrusive and extrusive features (8/7 and 7/8 SRPs)', 15,
             f'Examination with reference to intrusive features · 8/7 x {SRPS}',
             f'Examination with reference to extrusive features · 7/8 x {SRPS}'),),
      '0-7', EV, ID + 'p2-q2c', True),
]

Q3AS = (L(5, 'Examine the map and text above that highlight tectonic activity', 'following questions.'),)
PART_TWO += romans('3A', 5, L(5, 'Dynamic Boundaries'), Q3AS, ID + 'p2-q3a', ('page',), [
    ('(i)', 2, L(5, '(i) To what height, in metres, did the cone', 'seven days?'),
     (S(13, '(i) · 30 (metres)', '(ii) · Valid reason'),), (fixed('Height', 2, '(i) · 30 (metres) · 2 marks'),), '0-7', EV),
    ('(ii)', 2, L(5, '(ii) Give one reason, from the text above', 'after the eruption.'),
     (S(13, '(ii) · Valid reason', '(iii) · Valid gases'),), (fixed('Reason', 2, '(ii) · Valid reason · 2 marks'),), '0-7', EV),
    ('(iii)', 4, L(5, '(iii) Name two gases emitted from a volcano.'),
     (S(13, '(iii) · Valid gases', '(iv) · Eurasian'),), (pair('(iii) · Valid gases · 2 + 2 marks', 'Two gases'),), '0-7', EV),
    ('(iv)', 4, L(5, '(iv) Iceland is located on two tectonic plates. Name both plates.'),
     (S(13, '(iv) · Eurasian', '(v) · Valid explanation'),),
     (pair('(iv) · Eurasian & North American · 2 + 2 marks', 'Both plates'),), '0-0', PS),
    ('(v)', 4, L(5, '(v) Explain briefly one benefit of volcanic activity.'),
     (S(13, '(v) · Valid explanation', '(vi) · Valid explanation'),),
     (pair('(v) · Valid explanation · 2 + 2 marks', 'Benefit'),), '0-7', EV),
    ('(vi)', 4, L(5, '(vi) Explain briefly what is meant be the term caldera.'),
     (S(13, '(vi) · Valid explanation', None),), (pair('(vi) · Valid explanation · 2 + 2 marks', 'Explanation'),),
     '0-7', EV),
])

PART_TWO += [
    T('p2-3b', P2, '3B', '', 30, 5, L(5, 'Sedimentary Rocks'),
      (L(5, 'Examine the formation of sedimentary rocks, with reference to examples from Ireland.'),),
      (S(14, 'Sedimentary rocks named · 2 + 2', 'Annotation'),),
      (pair('Sedimentary rocks named · 2 + 2 marks', 'Sedimentary rocks named'),
       srp('Examination of formation', 13, f'Examination of formation · 13 x {SRPS}')),
      '0-1', RW, ID + 'p2-q3b', True),
    T('p2-3c', P2, '3C', '', 30, 5, L(5, 'Seismic Activity'),
      (L(5, 'Explain how the occurrence of earthquakes can be predicted and their effects reduced.'),),
      (S(15, 'Reference to prediction of earthquakes · 2 marks', 'Annotation'),),
      (fixed('Reference to prediction of earthquakes', 2, 'Reference to prediction of earthquakes · 2 marks'),
       fixed('Reference to reducing effects of earthquakes', 2, 'Reference to reducing effects of earthquakes · 2 marks'),
       srp('Explanation', 13, f'Explanation · 13 x {SRPS}')),
      '0-7', EV, ID + 'p2-q3c', True),
    # Question 4
    T('p2-4a', P2, '4A', '', 20, 6, L(6, 'Map Skills'),
      (L(6, 'Draw an outline map of a Continental / Sub-Continental region', '(upland or lowland).'),),
      (S(16, 'Map outline', None),),
      sketch('Map outline · 4 marks graded (4/2/0)', (0, 2, 4),
             ('4 features @ 4 marks each', 'Named 2 marks'), sums((0, 1, 2), (0, 2)), 4),
      '1-6', CONT, ID + 'p2-q4a', True,
      row_labels=(None, None, None, L(6, 'The course of a named river'),
                  L(6, 'The outline of a named feature of relief (upland or lowland)'))),
    T('p2-4b', P2, '4B', '', 30, 6, L(6, 'Concept of a Region'),
      (L(6, 'Examine how culture or climate can be used to define regions', 'that you have studied.'),),
      (S(17, 'Example · 2 marks', 'Annotation'),),
      (fixed('Example', 2, 'Example · 2 marks'), srp('Examination', 14, f'Examination · 14 x {SRPS}')),
      '1-0', IRL + EURO + CONT, ID + 'p2-q4b', True,
      routes=(Route('culture', 'culture', ID + 'p2-q4b', True, (('culture or climate', 'culture'),)),
              Route('climate', 'climate', ID + 'p2-q4b-climate', False, (('culture or climate', 'climate'),)))),
    T('p2-4c', P2, '4C', '', 30, 6, L(6, 'Secondary Economic Activity'),
      (L(6, 'Account for the development of secondary economic activity', 'Infrastructure.'),),
      (S(18, 'Examination of Factor 1', 'Annotation'),),
      (split('Examination of the two factors (8/7 and 7/8 SRPs)', 15,
             f'Examination of Factor 1 · 8/7 x {SRPS}', f'Examination of Factor 2 · 7/8 x {SRPS}'),),
      '1-4', IRL, ID + 'p2-q4c-government-policy-labour', True,
      routes=bullet_routes('p2-q4c-', ('Government policy', 'Labour', 'Markets', 'Infrastructure.'), 2)),
]

Q5AS = (L(7, 'Examine the map and text above that outline the development', 'following questions.'),)
PART_TWO += romans('5A', 7, L(7, 'Regional Disparity in the European Union'), Q5AS, ID + 'p2-q5a', ('page',), [
    ('(i)', 4, L(7, '(i) Other than Ireland, list the two countries', 'in 1973.'),
     (S(19, '(i) · UK and Denmark', '(ii) · Valid countries'),), (pair('(i) · UK and Denmark · 2 + 2 marks', 'Two countries'),),
     '1-5', EURO),
    ('(ii)', 4, L(7, '(ii) Name two countries that were original members of the EU.'),
     (S(19, '(ii) · Valid countries', '(iii) · Valid statement'),), (pair('(ii) · Valid countries · 2 + 2 marks', 'Two countries'),),
     '1-5', EURO),
    ('(iii)', 4, L(7, '(iii) State two purposes of the European Regional Development Fund.'),
     (S(19, '(iii) · Valid statement', '(iv) · Valid explanation'),),
     (pair('(iii) · Valid statement · 2 + 2 marks', 'Two purposes'),), '1-5', EURO),
    ('(iv)', 8, L(7, '(iv) Explain briefly two challenges facing the EU today.'),
     (S(19, '(iv) · Valid explanation', None),),
     (pair('(iv) · Valid explanation · 2 + 2 marks', 'First challenge'), pair('=2 + 2 marks', 'Second challenge')),
     '1-5', EURO),
])

PART_TWO += [
    T('p2-5b', P2, '5B', '', 30, 7, L(7, 'Primary Economic Activity'),
      (L(7, 'Examine the impact of one of the following on the development of primary economic', 'Relief.'),),
      (S(20, 'Examination of region 1', 'Annotation'),),
      (split('Examination of the two regions (8/7 and 7/8 SRPs)', 15,
             f'Examination of region 1 · 8/7 x {SRPS}', f'Examination of region 2 · 7/8 x {SRPS}'),),
      '1-5', EURO, ID + 'p2-q5b-climate', True, routes=bullet_routes('p2-q5b-', ('Climate', 'Relief.'))),
    T('p2-5c', P2, '5C', '', 30, 7, L(7, 'Urban Development'),
      (L(7, 'Examine the factors that have influenced the development of one urban area', 'that you have studied.'),),
      (S(21, 'Urban area named · 2 marks', 'Annotation'),),
      (fixed('Urban area named', 2, 'Urban area named · 2 marks'),
       pair('Factors identified · 2 + 2 marks', 'Factors identified'),
       srp('Examination', 12, f'Examination · 12 x {SRPS}')),
      '1-4', IRL, ID + 'p2-q5c', True),
]

Q6AS = (L(8, 'Examine the table above showing Ireland’s leading tourist attractions', 'following questions.'),)
PART_TWO += romans('6A', 8, L(8, 'Tourism in Ireland'), Q6AS, ID + 'p2-q6a', ('page',), [
    ('(i)', 4, L(8, '(i) Name the two most popular tourist attractions.'),
     (S(22, '(i) · Phoenix Park visitor centre', '(ii) · The Book of Kells'),),
     (pair('(i) · Phoenix Park visitor centre & Kilkenny Castle Parklands · 2 + 2 marks', 'Two attractions'),), '2-0', TG),
    ('(ii)', 2, L(8, '(ii) What tourist attraction had a total of 835,065 visitors?'),
     (S(22, '(ii) · The Book of Kells', '(iii) · Museum, Gallery'),),
     (fixed('Attraction', 2, '(ii) · The Book of Kells · 2 marks'),), '2-0', TG),
    ('(iii)', 2, L(8, '(iii) Which category had a 17% share of tourists?'),
     (S(22, '(iii) · Museum, Gallery', '(iv) · 14'),), (fixed('Category', 2, '(iii) · Museum, Gallery · 2 marks'),), '2-0', TG),
    ('(iv)', 4, L(8, '(iv) Calculate X, the percentage share', 'visitor/heritage centre.'),
     (S(22, '(iv) · 14', '(v) · Valid explanation'),), (fixed('Calculation', 4, '(iv) · 14 (%) · 4 marks'),), '2-0', TG),
    ('(v)', 4, L(8, '(v) The majority of attractions in the table', 'the country.'),
     (S(22, '(v) · Valid explanation', '(vi) · Valid explanation'),),
     (pair('(v) · Valid explanation · 2 + 2 marks', 'Reason'),), '1-4', IRL),
    ('(vi)', 4, L(8, '(vi) Explain briefly one possible negative impact of tourism.'),
     (S(22, '(vi) · Valid explanation', None),), (pair('(vi) · Valid explanation · 2 + 2 marks', 'Negative impact'),),
     '1-4', IRL),
])

ECON = (H + 'elective-economic',)
ENV = (H + 'economic-environmental-impact',)
DEV = (H + 'economic-developing-economies',)
PART_TWO += [
    T('p2-6b', P2, '6B', '', 30, 8, L(8, 'Population Dynamics'),
      (L(8, 'Account for population distribution throughout a Continental / Sub-Continental region',
         'that you have studied.'),),
      (S(23, 'Examination · 15', 'Annotation'),), (srp('Examination', 15, f'Examination · 15 x {SRPS}'),),
      '1-6', CONT, ID + 'p2-q6b', True),
    T('p2-6c', P2, '6C', '', 30, 8, L(8, 'Socio-Economic Regions'),
      (L(8, 'Discuss how economic activity in core regions differs', 'using examples you have studied.'),),
      (S(24, 'Discussion · 15', 'Annotation'),), (srp('Discussion', 15, f'Discussion · 15 x {SRPS}'),),
      '1-0', IRL + EURO + CONT, ID + 'p2-q6c', True),
    # Question 7
    T('p2-7a', P2, '7A', '', 20, 10, L(10, 'Ordnance Survey Map'),
      (L(10, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper.', 'The camping site.'),),
      (S(26, 'Sketch Outline', 'Annotation'),), OS_SKETCH, '2-6', MAP, ID + 'p2-q7a', False, ('map', 'legend'),
      row_labels=(None, L(10, 'The post office'), L(10, 'The electricity transmission line'),
                  L(10, 'The R584 road'), L(10, 'The camping site'))),
    T('p2-7b', P2, '7B', '', 30, 10, L(10, 'Economic Development'),
      (L(10, 'Discuss how Gross National Product (GNP) and the Human Development Index (HDI)', 'studied.'),),
      (S(27, 'Reference to GNP as measure', 'Annotation'),),
      (fixed('Reference to GNP as measure', 2, 'Reference to GNP as measure · 2 marks'),
       fixed('Reference to HDI as measure', 2, 'Reference to HDI as measure · 2 marks'),
       fixed('Example', 2, 'Example · 2 marks'), srp('Discussion', 12, f'Discussion · 12 x {SRPS}')),
      '3-1', ECON + DEV, ID + 'p2-q7b', True),
    T('p2-7c', P2, '7C', '', 30, 10, L(10, 'Sustainable Development'),
      (L(10, 'Examine how economic activities can be developed sustainably', 'environmental impact.'),),
      (S(28, 'Examination · 15', 'Annotation'),), (srp('Examination', 15, f'Examination · 15 x {SRPS}'),),
      '3-4', ENV, ID + 'p2-q7c', True),
]

Q8AS = (L(11, 'Examine the map above showing the numbers of historical colonies', 'following questions.'),)
PART_TWO += romans('8A', 11, L(11, 'Colonialism'), Q8AS, ID + 'p2-q8a', ('page',), [
    ('(i)', 2, L(11, '(i) Which country had the highest number of colonies?'),
     (S(29, '(i) · United Kingdom', '(ii) · Greece'),), (fixed('Country', 2, '(i) · United Kingdom · 2 marks'),), '2-0', TG),
    ('(ii)', 4, L(11, '(ii) Name two countries from the map that had only one colony.'),
     (S(29, '(ii) · Greece', '(iii) · Six'),), (pair('(ii) · Greece & Austria · 2 + 2 marks', 'Two countries'),), '2-0', TG),
    ('(iii)', 2, L(11, '(iii) How many countries shown on the map had more than 10 colonies?'),
     (S(29, '(iii) · Six', '(iv) · Valid colonised'),), (fixed('Number', 2, '(iii) · Six · 2 marks'),), '2-0', TG),
    ('(iv)', 4, L(11, '(iv) Name one country you have studied that was colonised', 'colonised it.'),
     (S(29, '(iv) · Valid colonised', '(v) · Valid explanation'),),
     (pair('(iv) · Valid colonised country & valid colonising country · 2 + 2 marks', 'Colonised and colonising country'),),
     '3-1', DEV),
    ('(v)', 4, L(11, '(v) Explain briefly what is meant by the term colonialism.'),
     (S(29, '(v) · Valid explanation', '(vi) · Valid explanation'),),
     (pair('(v) · Valid explanation · 2 + 2 marks', 'Explanation'),), '3-1', DEV),
    ('(vi)', 4, L(11, '(vi) Explain briefly one negative impact colonialism had', 'have studied.'),
     (S(29, '(vi) · Valid explanation', None),), (pair('(vi) · Valid explanation · 2 + 2 marks', 'Negative impact'),),
     '3-1', DEV),
])

REASON = ('For each reason: · Reason stated · 2 marks', 'Map evidence · 2 marks', f'Explanation · 3 x {SRPS}')
Q8BS = (L(11, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper and',
          'following questions.'),)
PART_TWO += romans('8B', 11, L(11, 'Development of Economic Activity'), Q8BS, ID + 'p2-q8b', ('map', 'legend'), [
    ('(i)', 20, L(11, '(i) Explain two reasons why a fish processing plant', 'support each reason.'),
     (S(30, '(i) · 2 x reasons', '(ii) · 1 x reason'), S(30, 'For each reason:', 'Annotation')),
     tuple(Criterion(f'Reason {n}', 10, evens(10), 'srp', ('(i) · 2 x reasons @ 10 marks each.', *REASON))
           for n in (1, 2)), '3-0', ECON + MAP),
    ('(ii)', 10, L(11, '(ii) Using evidence from the Ordnance Survey map, explain one reason', 'not to locate in this area.'),
     (S(30, '(ii) · 1 x reason', 'Annotation'),),
     (Criterion('Reason', 10, evens(10), 'srp', ('(ii) · 1 x reason @ 10 marks.', *REASON)),), '3-0', ECON + MAP),
], legacy_first=False)

ENERGY = (H + 'economic-energy',)
PART_TWO.append(T(
    'p2-8c', P2, '8C', '', 30, 11, L(11, 'Environmental Impact'),
    (L(11, 'Examine the environmental impact of burning fossil fuels.'),),
    (S(31, 'Environmental Impact identified · 2', 'Annotation'),),
    (fixed('Environmental impact identified', 2, 'Environmental Impact identified · 2 marks'),
     srp('Examination', 14, f'Examination · 14 x {SRPS}')),
    '3-4', ENV + ENERGY, ID + 'p2-q8c', True))

Q9AS = (L(12, 'Examine the data above showing the unemployment rate', 'following questions.'),)
PART_TWO += romans('9A', 12, L(12, 'Economic Activity'), Q9AS, ID + 'p2-q9a', ('page',), [
    ('(i)', 16, L(12, '(i) Using graph paper, draw a suitable graph to illustrate this data.'),
     (S(32, 'Bar Chart · Pie Chart', 'Annotation'),), GRAPH, '2-0', TG),
    ('(ii)', 4, L(12, '(ii) Explain briefly one way that high employment benefits the Irish economy.'),
     (S(32, 'Valid explanation · 2 + 2 marks', None),), (pair('Valid explanation · 2 + 2 marks', 'Benefit'),),
     '3-0', ECON),
])

PART_TWO += [
    T('p2-9b', P2, '9B', '', 30, 12, L(12, 'European Union – Trade'),
      (L(12, 'Describe the current trading patterns of the European Union', 'these trading patterns.'),),
      (S(33, 'Internal trading pattern identified · 2 marks', 'Annotation'),),
      (fixed('Internal trading pattern identified', 2, 'Internal trading pattern identified · 2 marks'),
       fixed('External trading pattern identified', 2, 'External trading pattern identified · 2 marks'),
       pair('Factors influencing trading patterns identified · 2 + 2 marks', 'Factors identified'),
       srp('Description/explanation', 11, f'Description/explanation · 11 x {SRPS}')),
      '3-3', (H + 'economic-european-union',), ID + 'p2-q9b', True),
    T('p2-9c', P2, '9C', '', 30, 12, L(12, 'Multinational Company'),
      (L(12, 'Examine the impact of each of the following on the operations of one multinational',
         'Developments in information technology.'),),
      (S(34, 'MNC named · 2 marks', 'Annotation'),),
      (fixed('MNC named', 2, 'MNC named · 2 marks'),
       srp('Examination factor 1', 7, f'Examination factor 1 · 7 x {SRPS}'),
       srp('Examination factor 2', 7, f'Examination factor 2 · 7 x {SRPS}')),
      '3-2', (H + 'economic-multinationals-globalisation',), ID + 'p2-q9c', True),
]

URB = (H + 'human-urban-geography',)
POP = (H + 'human-population',)
Q10AS = (L(13, 'Examine the data above showing the percentage of global population', 'following questions.'),)
PART_TWO += romans('10A', 13, L(13, 'Urban Density'), Q10AS, ID + 'p2-q10a', ('page',), [
    ('(i)', 16, L(13, '(i) Using graph paper, draw a suitable graph to illustrate this data.'),
     (S(35, 'Bar Chart · Pie Chart', 'Annotation'),), GRAPH, '2-0', TG),
    ('(ii)', 4, L(13, '(ii) Explain briefly one challenge associated with increasing urban populations.'),
     (S(36, 'Valid explanation · 2 + 2 marks', '10B.'),), (pair('Valid explanation · 2 + 2 marks', 'Challenge'),),
     '4-5', URB),
])

EVIDENCE = 'the aerial photograph OR from the 1:50 000 Ordnance Survey map and legend'
BANTRY_REASON = ('Three reasons @ 10 marks each', 'For each reason:', 'Reason stated · 2 marks',
                 'OS map / aerial photo evidence · 2 marks', 'Explanation · 3 x SRPs')
PART_TWO += [
    T('p2-10b', P2, '10B', '', 30, 13, L(13, 'Urban Settlement'),
      (L(13, 'Answer the following question using evidence from the aerial photograph OR', 'both in your answer.'),
       L(13, 'Explain three reasons why the town of Bantry developed at its present location.')),
      (S(36, 'Three reasons @ 10 marks each', 'Annotation'),),
      tuple(Criterion(f'Reason {n}', 10, evens(10), 'srp', BANTRY_REASON) for n in (1, 2, 3)),
      '4-3', URB + AER + MAP, ID + 'p2-q10b-aerial-photograph', False, ('aerial', 'map', 'legend'),
      routes=(Route('aerial-photograph', 'aerial photograph', ID + 'p2-q10b-aerial-photograph', False,
                    ((EVIDENCE, 'the aerial photograph'),), sources=('aerial',)),
              Route('ordnance-survey-map', 'Ordnance Survey map', ID + 'p2-q10b-ordnance-survey-map', False,
                    ((EVIDENCE, 'the 1:50 000 Ordnance Survey map and legend'),), sources=('map', 'legend')))),
    T('p2-10c', P2, '10C', '', 30, 13, L(13, 'Dynamics of Population'),
      (L(13, 'Examine how changing fertility and mortality rates impact on population structure',
         'that you have studied.'),),
      (S(37, 'Impact of changing fertility rates identified · 2', 'Annotation'),),
      (fixed('Impact of changing fertility rates identified', 2, 'Impact of changing fertility rates identified · 2 marks'),
       fixed('Impact of changing mortality rates identified', 2, 'Impact of changing mortality rates identified · 2 marks'),
       fixed('Example', 2, 'Example · 2 marks'), srp('Examination', 12, f'Examination · 12 x {SRPS}')),
      '4-0', POP, ID + 'p2-q10c', True),
]

Q11AS = (L(14, 'Examine the chart above showing the population of Ireland at each census', 'following questions.'),)
PART_TWO += romans('11A', 14, L(14, 'Population Characteristics'), Q11AS, ID + 'p2-q11a', ('page',), [
    ('(i)', 2, L(14, '(i) Which census year had the highest population?'),
     (S(38, '(i) · 1841 · 2 marks', '(ii) · 1961'),), (fixed('Census year', 2, '(i) · 1841 · 2 marks'),), '2-0', TG),
    ('(ii)', 2, L(14, '(ii) Which census year had the lowest population?'),
     (S(38, '(ii) · 1961', '(iii) · Increasing'),), (fixed('Census year', 2, '(ii) · 1961 · 2 marks'),), '2-0', TG),
    ('(iii)', 2, L(14, '(iii) Was the population increasing or decreasing from 1996 to 2022?'),
     (S(38, '(iii) · Increasing', '(iv) · Eight'),), (fixed('Trend', 2, '(iii) · Increasing · 2 marks'),), '2-0', TG),
    ('(iv)', 2, L(14, '(iv) In how many censuses was the population at or over 4 million people?'),
     (S(38, '(iv) · Eight', '(v) · 1,379,660'),), (fixed('Number of censuses', 2, '(iv) · Eight · 2 marks'),), '2-0', TG),
    ('(v)', 4, L(14, '(v) Calculate the change in Ireland’s population between 1841 and 2022.'),
     (S(38, '(v) · 1,379,660', '(vi) · Valid explanation'),), (fixed('Change', 4, '(v) · 1,379,660 · 4 marks'),), '2-0', TG),
    ('(vi)', 4, L(14, '(vi) Explain briefly one reason why Ireland’s population increased since 2011.'),
     (S(38, '(vi) · Valid explanation', '(vii) · Valid explanation'),),
     (pair('(vi) · Valid explanation · 2 + 2 marks', 'Reason'),), '4-0', POP),
    ('(vii)', 4, L(14, '(vii) Explain briefly the term natural change.'),
     (S(38, '(vii) · Valid explanation', None),), (pair('(vii) · Valid explanation · 2 + 2 marks', 'Explanation'),),
     '4-0', POP),
])

PART_TWO += [
    T('p2-11b', P2, '11B', '', 30, 14, L(14, 'Changing Urban Functions'),
      (L(14, 'Examine how the functions and/or services of urban centres can change over time',
         'that you have studied.'),),
      (S(39, 'Functions/services identified · 2 + 2', 'Annotation'),),
      (pair('Functions/services identified · 2 + 2 marks', 'Functions/services identified'),
       fixed('Example urban centre', 2, 'Example urban centre · 2 marks'),
       srp('Examination', 12, f'Examination · 12 x {SRPS}')),
      '4-3', URB, ID + 'p2-q11b', True),
    T('p2-11c', P2, '11C', '', 30, 14, L(14, 'Future Urbanism'),
      (L(14, 'Discuss two challenges facing cities of the future.'),),
      (S(40, 'Challenge identified · 2 + 2', 'Annotation'),),
      (pair('Challenge identified · 2 + 2 marks', 'Challenges identified'),
       split('Discussion of the two challenges (7/6 and 6/7 SRPs)', 13,
             f'Discussion of challenge one · 7/6 x {SRPS}', f'Discussion of challenge two · 6/7 x {SRPS}')),
      '4-5', URB, ID + 'p2-q11c', True),
    # Question 12
    T('p2-12a', P2, '12A', '', 20, 15, L(15, 'Historical Map', nth=0),
      (L(15, 'Examine the historical map of Bantry shown above.', 'The court house.'),),
      (S(41, 'Sketch Outline', None), S(42, '• There must be an attempt', '12B.')),
      sketch('Sketch Outline · 4 marks', (0, 4), ('4 features @ 4 marks each', 'Named 1 mark'),
             sums((0, 1, 3), (0, 1)), 4),
      '4-3', URB, ID + 'p2-q12a', True, ('page',),
      row_labels=(None, L(15, 'Bantry Harbour'), L(15, 'Two connecting roads/streets'), L(15, 'The school'),
                  L(15, 'The court house'))),
    T('p2-12b', P2, '12B', '', 30, 15, L(15, 'Migration', nth=0),
      (L(15, 'Discuss how recent trends in migration are impacting on migration policy in Europe.'),),
      (S(42, 'Impact on migration policy identified · 2 marks', 'Annotation'),),
      (fixed('Impact on migration policy identified', 2, 'Impact on migration policy identified · 2 marks'),
       srp('Discussion', 14, f'Discussion · 14 x {SRPS}')),
      '4-2', POP, ID + 'p2-q12b', True),
    T('p2-12c', P2, '12C', '', 30, 15, L(15, 'Overpopulation'),
      (L(15, 'Examine the causes and effects of overpopulation', 'have studied.'),),
      (S(43, 'Cause identified · 2 marks', 'Annotation'),),
      (fixed('Cause identified', 2, 'Cause identified · 2 marks'), fixed('Effect identified', 2, 'Effect identified · 2 marks'),
       fixed('Example', 2, 'Example · 2 marks'),
       srp('Examination of causes', 6, f'Examination of causes · 6 x {SRPS}'),
       srp('Examination of effects', 6, f'Examination of effects · 6 x {SRPS}')),
      '4-1', POP, ID + 'p2-q12c', True),
]

# ------------------------------------------------------------------ Options --
OC = (S(45, '*Overall Coherence (20 marks)', None, table=True),)


def option(q, page, theme, note_nth, prompt, scheme_page, topic, atlas, routes=(), after=None, end=None):
    return T(f'p2-{q}', P2, q, '', 80, page, theme, (prompt,),
             (S(scheme_page, 'Number of aspects', end, None, after), *OC),
             (Criterion('Aspects (3 @ 20 marks or 4 @ 15 marks)', 60, upto(60), 'srp',
                        ('Number of aspects', '?For each aspect:', 'Identifying aspect', '8 x SRP')),
              Criterion('Overall coherence', 20, (0, 6, 10, 14, 17, 20), 'exact',
                        ('Overall Coherence · 20 marks graded*', '*Overall Coherence (20 marks)', 'Excellent · 20',
                         'Very Good · 17', 'Good · 14', 'Fair · 10', 'Weak · 6', 'Poor · 0'))),
             topic, (atlas,), routes[0].card_id if routes else ID + f'p2-q{q}', True,
             stem=(L(page, 'Note: It is better to discuss three or four aspects', 'large number of points.',
                     nth=note_nth),),
             routes=routes)


GI, GE = H + 'option-global-interdependence', H + 'option-geoecology'
CI, AO = H + 'option-culture-identity', H + 'option-atmosphere-ocean'
OPTIONS = [
    option('13', 17, L(17, 'Global Interdependence'), 0,
           L(17, 'Sustainable development should be a priority', 'Discuss.'), 47, '5-3', GI),
    option('14', 17, L(17, 'Global Interdependence'), 0,
           L(17, 'We live in an interdependent global economy', 'Desertification.'), 48, '5-1', GI,
           after='14.', end='15. Views'),
    option('15', 17, L(17, 'Global Interdependence'), 0,
           L(17, 'Views of development and underdevelopment', 'developing ‘South’.'), 48, '5-0', GI, after='15. Views'),
    option('16', 17, L(17, 'Geoecology'), 1,
           L(17, 'Explain how soil characteristics impact on soil development.'), 49, '6-0', GE),
    option('17', 17, L(17, 'Geoecology'), 1,
           L(17, 'Examine the characteristics of one biome', 'Fauna.'), 50, '6-2', GE,
           routes=bullet_routes('p2-q17-', ('Climate', 'Soils', 'Flora', 'Fauna.'), 3), after='17.', end='18.'),
    option('18', 17, L(17, 'Geoecology'), 1,
           L(17, 'Examine how each of the following impact on soil characteristics:', 'Conservation methods.'),
           50, '6-1', GE, after='18.'),
    option('19', 18, L(18, 'Culture and Identity'), 0,
           L(18, 'Nationality and the nation state', 'cultural groups.'), 51, '7-1', CI),
    option('20', 18, L(18, 'Culture and Identity'), 0,
           L(18, 'Identity as a concept entails', 'that you have studied.'), 52, '7-2', CI, after='20.', end='21.'),
    option('21', 18, L(18, 'Culture and Identity'), 0,
           L(18, 'Examine the importance of language as a cultural indicator.'), 52, '7-0', CI, after='21.'),
    option('22', 18, L(18, 'The Atmosphere – Ocean Environment'), 1,
           L(18, 'Examine how exchanges of water', 'climate regimes.'), 53, '8-2', AO),
    option('23', 18, L(18, 'The Atmosphere – Ocean Environment'), 1,
           L(18, 'Identify and account for the characteristics', 'studied.'), 54, '8-4', AO, after='23.', end='24.'),
    option('24', 18, L(18, 'The Atmosphere – Ocean Environment'), 1,
           L(18, 'Examine how solar energy is transformed', 'atmosphere and oceans.'), 54, '8-1', AO, after='24.'),
]

TASKS = [*PART_ONE, *PART_TWO, *OPTIONS]

ID_CORRECTION_REASON = (
    'The shipped card held every part of a question the scheme prices part by '
    'part. Its id is kept on the first separately priced part; the other parts '
    'are new cards with their own published allocation.')

# Every 2024 Higher card id shipped before this review (66). Each must survive.
LEGACY_IDS = [
    'geography-2024-hl-p1-q2',
    'geography-2024-hl-p1-q3',
    'geography-2024-hl-p1-q4',
    'geography-2024-hl-p1-q5',
    'geography-2024-hl-p1-q6',
    'geography-2024-hl-p1-q10',
    'geography-2024-hl-p1-q11',
    'geography-2024-hl-p1-q12',
    'geography-2024-hl-p2-q1b-the-impact-of-flood-control-measur',
    'geography-2024-hl-p2-q1b-the-impact-of-coastal-defence-meas',
    'geography-2024-hl-p2-q1b-the-impact-of-human-activities-on',
    'geography-2024-hl-p2-q1c',
    'geography-2024-hl-p2-q2a',
    'geography-2024-hl-p2-q2b-route-i-fluvial-landform',
    'geography-2024-hl-p2-q2b-route-i-coastal-landform',
    'geography-2024-hl-p2-q2b-route-i-glacial-landform',
    'geography-2024-hl-p2-q2b-route-ii',
    'geography-2024-hl-p2-q2c',
    'geography-2024-hl-p2-q3a',
    'geography-2024-hl-p2-q3b',
    'geography-2024-hl-p2-q3c',
    'geography-2024-hl-p2-q4a',
    'geography-2024-hl-p2-q4b',
    'geography-2024-hl-p2-q4c-government-policy-labour',
    'geography-2024-hl-p2-q4c-government-policy-markets',
    'geography-2024-hl-p2-q4c-government-policy-infrastructure',
    'geography-2024-hl-p2-q4c-labour-markets',
    'geography-2024-hl-p2-q4c-labour-infrastructure',
    'geography-2024-hl-p2-q4c-markets-infrastructure',
    'geography-2024-hl-p2-q5a',
    'geography-2024-hl-p2-q5b-climate',
    'geography-2024-hl-p2-q5b-relief',
    'geography-2024-hl-p2-q5c',
    'geography-2024-hl-p2-q6a',
    'geography-2024-hl-p2-q6b',
    'geography-2024-hl-p2-q6c',
    'geography-2024-hl-p2-q7b',
    'geography-2024-hl-p2-q7c',
    'geography-2024-hl-p2-q8a',
    'geography-2024-hl-p2-q8c',
    'geography-2024-hl-p2-q9a',
    'geography-2024-hl-p2-q9b',
    'geography-2024-hl-p2-q9c',
    'geography-2024-hl-p2-q10a',
    'geography-2024-hl-p2-q10c',
    'geography-2024-hl-p2-q11a',
    'geography-2024-hl-p2-q11b',
    'geography-2024-hl-p2-q11c',
    'geography-2024-hl-p2-q12a',
    'geography-2024-hl-p2-q12b',
    'geography-2024-hl-p2-q12c',
    'geography-2024-hl-p2-q13',
    'geography-2024-hl-p2-q14',
    'geography-2024-hl-p2-q15',
    'geography-2024-hl-p2-q16',
    'geography-2024-hl-p2-q17-climate-soils-flora',
    'geography-2024-hl-p2-q17-climate-soils-fauna',
    'geography-2024-hl-p2-q17-climate-flora-fauna',
    'geography-2024-hl-p2-q17-soils-flora-fauna',
    'geography-2024-hl-p2-q18',
    'geography-2024-hl-p2-q19',
    'geography-2024-hl-p2-q20',
    'geography-2024-hl-p2-q21',
    'geography-2024-hl-p2-q22',
    'geography-2024-hl-p2-q23',
    'geography-2024-hl-p2-q24',
]
