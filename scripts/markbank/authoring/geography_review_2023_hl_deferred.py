"""Independent review ledger: Leaving Certificate Geography 2023 Higher Level, deferred sitting.

The SEC's deferred examination is a paper of its own. Sources (English
editions, harvested in paper-trail-corpus/deferredexams/2023 and
deferredmarkingschemes/2023, filed by Paper Trail as "<fileid>-deferred";
sizes pinned in EXPECTED_SOURCES and the generated audit): Part One and
Answerbook LC005ALP042EV (48 pages), Part Two LC005ALP043EV (20 pages),
marking scheme LC005ALP000EV (64 pages), and the sitting's own companions:
the 1:50 000 Listowel map LC005CLP003EV, its legend LC005CLPC00EV and the
Listowel aerial photograph LC005CLP004EV, published only as a JPEG.

Visual sweep (every page rendered and read on 2026-11-19):
  Part One booklet p1 cover; p2 instructions (Part One "Attempt any TEN",
  80 marks; Part Two "attempt FOUR", 320 marks); p3-p13 Questions 1-12 (p8
  holds Q6 and Q7); p14 Part Two answerbook instructions; p15-p18 graph
  paper; p19-p47 lined answer pages; p48 back cover.
  Part Two booklet p1 cover; p2 Part Two instructions; p3-p8 Sections 1-2
  (Q1-Q6); p9 Section 3 divider; p10-p15 Electives (Q7-Q12); p16 Section 4
  divider and note; p17-p18 Options (Q13-Q24); p19 "Do not hand this up";
  p20 back cover and copyright notice.
  Scheme p1 cover; p2 the note on deferred marking schemes; p3 notes and
  annotation key; p4 Part One table (two columns, Q1-Q6 and Q7-Q12, each
  question's parts side by side); p5 the notes and annotation key again;
  p6-p24 Q1-Q6 (each reprints its question); p25 Electives divider; p26-p43
  Q7-Q12; p44 Options divider; p45 option outline and Overall Coherence
  descriptors; p46 option annotations; p47-p54 Q13-Q24; p55-p58
  Geographical Investigation (coursework); p59 investigation topics; p60
  Irish-language bonus marks; p61-p64 blank.
  Companions: Listowel map extract (the River Feale and the Smearlagh River,
  the N69 and R523); OS legend sheet; oblique aerial photograph of Listowel.

The deferred scheme sets out every printed part, so every part is carded
with its own published allocation. Its Part One table prints each
question's parts side by side; each part reads its own column (Q1, Q3 and
Q4's letters and their process/landform columns). It heads Question 11
"Q1" and prints 8A(ii) as "(i)" under the graph; both are placed by their
position and wording. Part Two follows the June 2023 ledger: every A-part
roman is a task; B, C and options are one task each, except 11B, whose (i)
and (ii) the scheme prices separately. Finite printed choices are routes:
1C, 2C and 8B one of the printed bullets; 3B (i) or (ii), with (i)'s one
fluvial or one coastal or one glacial landform. Choose-N-of-M pools are one
card with every printed item (9B any two, 11C two of three, 17 and 18 any
three of four). 10B's two printed areas and 24's three printed features are
compulsory.
"""

from geography_review import (
    Criterion, Lift, Route, SchemeSlice, Task, evens, fixed, slug, srp, sums, upto,
)

YEAR = 2023
LEVEL = 'higher'
REVIEWED_AT = '2026-11-19'
PAPER_PAGES = {1: 48, 2: 20}
SCHEME_PAGES = 64
QUESTION_TARIFFS = {1: {str(n): 8 for n in range(1, 13)},
                    2: {**{f'{n}{x}': (20 if x == 'A' else 30)
                           for n in range(1, 13) for x in 'ABC'},
                        **{str(n): 80 for n in range(13, 25)}}}

EXPECTED_SOURCES = {
    'paper1': ('LC005ALP042EV.pdf', 6140988),
    'paper2': ('LC005ALP043EV.pdf', 2120291),
    'scheme': ('LC005ALP000EV.pdf', 1706198),
    'map': ('LC005CLP003EV.pdf', 3320889),
    'legend': ('LC005CLPC00EV.pdf', 890021),
    'aerial': ('LC005CLP004EV.jpg', 4958503),
}

PAGE_REVIEW = {
    'paper1': {1: 'cover', 2: 'instructions', **{p: 'question' for p in range(3, 14)},
               14: 'answerbook instructions', **{p: 'graph-paper answer page' for p in range(15, 19)},
               **{p: 'lined answer page' for p in range(19, 48)}, 48: 'copyright/back cover'},
    'paper2': {1: 'cover', 2: 'Part Two instructions',
               **{p: 'question' for p in (3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15, 17, 18)},
               9: 'section divider', 16: 'section divider and option note',
               19: 'do not hand this up', 20: 'copyright/back cover'},
    'scheme': {1: 'cover', 2: 'note on deferred marking schemes', 3: 'notes and annotation key',
               4: 'Part One table', 5: 'notes and annotation key (repeated)',
               **{p: 'Part Two allocation' for p in range(6, 25)}, 25: 'section divider',
               **{p: 'Part Two allocation' for p in range(26, 44)}, 44: 'section divider',
               45: 'option outline and coherence descriptors', 46: 'option annotations',
               **{p: 'option allocation' for p in range(47, 55)},
               **{p: 'geographical investigation (coursework)' for p in range(55, 59)},
               59: 'investigation topics', 60: 'Irish-language bonus marks',
               61: 'blank', 62: 'blank', 63: 'blank', 64: 'blank'},
}

EXPECTED_SELECTION_SCAN = [
    [1, 2, 'attempt any ten'], [1, 2, 'attempt four'], [1, 3, 'attempt any ten'],
    [2, 2, 'attempt four'],
    [2, 3, 'one of the following'],
    [2, 4, 'one of the following'],
    [2, 5, 'answer (i) or (ii)'], [2, 5, 'or one'], [2, 5, 'or one'],
    [2, 11, 'one of the following'], [2, 11, 'choose'], [2, 11, 'choose'],
    [2, 12, 'any two'],
    [2, 14, 'two of the following'],
    [2, 17, 'any three'], [2, 17, 'any three'],
]
SELECTION_REVIEW = [
    {'scan': [[1, 2, 'attempt any ten'], [1, 2, 'attempt four'], [1, 3, 'attempt any ten'],
              [2, 2, 'attempt four']],
     'kind': 'exam-attempt-rule',
     'reason': 'Part One any ten of twelve and Part Two four questions are attempt rules; every question is carded.'},
    {'scan': [[2, 3, 'one of the following'], [2, 4, 'one of the following'], [2, 11, 'one of the following']],
     'kind': 'closed-choose-one',
     'reason': '1C one of three printed impacts -> 3 routes; 2C one of four printed interactions -> 4 routes; '
               '8B one of three printed activities -> 3 routes.'},
    {'scan': [[2, 5, 'answer (i) or (ii)'], [2, 5, 'or one'], [2, 5, 'or one']], 'kind': 'closed-route',
     'reason': '3B: (i) or (ii); (i) offers one fluvial OR one coastal OR one glacial landform -> 4 routes.'},
    {'scan': [[2, 11, 'choose'], [2, 11, 'choose']], 'kind': 'printed-wording',
     'reason': '8C: "a computer factory might choose to locate ... might choose not to locate" is the '
               'question\'s wording, not a choice offered to the candidate.'},
    {'scan': [[2, 12, 'any two'], [2, 14, 'two of the following'], [2, 17, 'any three'], [2, 17, 'any three']],
     'kind': 'choose-n-one-card',
     'reason': '9B any two of three printed activities, 11C two of three printed land-uses, 17 any three of '
               'four printed processes and 18 any three of four printed characteristics -> one card each '
               'with every printed item (choice is not a route; the scheme marks each chosen item alike). '
               'Open choices are not fanned out: "one Irish soil type", "one biome", "one global climate '
               'type", "example(s)". Compulsory lists stay whole: 1A, 4A, 7A and 10A each bullet, 10B '
               'rural and urban areas, 24 each printed feature.'},
]

P1, P2 = 1, 2
LEFT = (0.0, 0.0, 0.5, 1.0)
RIGHT = (0.5, 0.0, 1.0, 1.0)
ID = 'geography-2023-hl-deferred-'
H = 'geography-higher-'
SRPS = 'SRP’s'


def L(page, start, end=None, nth=None):
    return Lift(page, start, end, None, nth)


def S(page, start, end=None, clip=None, after=None, table=False):
    return SchemeSlice(page, start, end, clip, after, table)


def T(key, part, q, sub, marks, page, title, prompt, scheme, criteria, topic, atlas, card_id,
      sources=(), stem=(), routes=(), row_labels=()):
    """A task of this sitting: no deferred card shipped before this review, so none is legacy."""
    return Task(key, part, q, sub, marks, page, title, prompt, scheme, criteria, topic, atlas,
                sources, card_id, False, stem=stem, routes=routes, row_labels=row_labels)


def rows(lines, marks=1):
    return tuple(fixed(f'Row {i}', marks, line) for i, line in enumerate(lines, 1))


def pair(line, label):
    return fixed(label, 4, line, (0, 2, 4))


def romans(part, q, page, title, stem, first_id, sources, parts):
    """Separately priced romans. parts: (sub, marks, prompt, scheme slices, criteria, topic, atlas)."""
    out = []
    for index, (sub, marks, prompt, scheme, criteria, topic, atlas) in enumerate(parts):
        roman = sub.strip('()')
        out.append(T(f'p{part}-{q.lower()}-{roman}', part, q, sub, marks, page, title,
                     prompt if isinstance(prompt, tuple) else (prompt,),
                     scheme if isinstance(scheme, tuple) else (scheme,), criteria, topic, atlas,
                     first_id if index == 0 else f'{first_id}-{roman}', sources, stem))
    return out


def clip(x0, y0, x1, y1):
    """A rectangle of the Part One table in PDF points (page 595 x 842), as page fractions."""
    return (x0 / 595, y0 / 842, x1 / 595, y1 / 842)


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
POP = (H + 'human-population',)
URB = (H + 'human-urban-geography',)
LANDUSE = (H + 'urban-land-uses',)
ECON = (H + 'elective-economic',)
DEV = (H + 'economic-developing-economies',)
MNC = (H + 'economic-multinationals-globalisation',)
EU = (H + 'economic-european-union',)
ENV = (H + 'economic-environmental-impact',)

Q1S = (L(3, 'Examine the Ordnance Survey map extract above and answer each of the following questions.'),)
Q1_ROWS = (L(3, 'V-shaped valley'), L(3, 'Sea cliff'), L(3, 'Beach'), L(3, 'Arête'))
Q3S = (L(5, 'Examine the photographs above and answer each of the following questions.'),)
Q3_ROWS = (L(5, 'Hydraulic action'), L(5, 'Delta'), L(5, 'Tor formation'), L(5, 'Corrie/Cirque'))
Q4S = (L(6, 'Examine the diagram above showing a cross section of a volcano', 'following questions.'),)
Q4_ROWS = (L(6, 'Sill'), L(6, 'Batholith'), L(6, 'Crater'))
PART_ONE = [
    T('p1-1-i', P1, '1', '(i)', 4, 3, L(3, 'Physical Processes'),
      (L(3, '(i) Match each of the letters A, B, C and D with the landform', 'table below.'),),
      (S(4, 'Q1 (i) A 1m', None, clip(0, 100, 149, 165)),), rows(['Q1 (i) A 1m', 'C 1m', 'D 1m', 'B 1m']),
      '0-4', RIVERS + SEA + GLAC, ID + 'p1-q1', ('page',), Q1S, row_labels=Q1_ROWS),
    T('p1-1-ii', P1, '1', '(ii)', 4, 3, L(3, 'Physical Processes'),
      (L(3, '(ii) Indicate, by ticking (✓) the correct box, whether the formation', 'glacial processes.'),),
      (S(4, '(ii) Fluvial 1m', None, clip(149, 100, 297, 165)),),
      rows(['(ii) Fluvial 1m', '=Coastal 1m@0', '=Coastal 1m@1', '=Glacial 1m']),
      '0-4', RIVERS + SEA + GLAC, ID + 'p1-q1-ii', ('page',), Q1S, row_labels=Q1_ROWS),
    T('p1-2-i', P1, '2', '(i)', 6, 4, L(4, 'Rocks and Deformation'),
      (L(4, '(i) Match each of the letters A, B and C with the feature', 'below.'),),
      (S(4, 'Q2 (i) C · 2m', None, clip(0, 186, 149, 227)),), rows(['Q2 (i) C · 2m', 'A · 2m', 'B · 2m'], 2),
      '0-2', RW, ID + 'p1-q2', ('page',),
      (L(4, 'Examine the diagram above which shows a cross section', 'following questions.'),),
      row_labels=(L(4, 'Fault line'), L(4, 'Volcanic intrusion'), L(4, 'Youngest layer of rock'))),
    T('p1-2-ii', P1, '2', '(ii)', 2, 4, L(4, 'Rocks and Deformation'),
      (L(4, '(ii) Indicate whether the following statement is true or false', 'box.'),
       L(4, 'The fault line in the diagram above is an example of a normal fault.')),
      (S(4, '(ii) True 2 marks', None, clip(149, 186, 297, 200)),),
      (fixed('True or false', 2, '(ii) True 2 marks'),), '0-2', RW, ID + 'p1-q2-ii', ('page',),
      (L(4, 'Examine the diagram above which shows a cross section', 'following questions.'),)),
    T('p1-3-i', P1, '3', '(i)', 4, 5, L(5, 'The Physical Environment'),
      (L(5, '(i) Match each of the photographs A, B, C and D', 'table below.'),),
      (S(4, 'Q3 (i) D 1m', None, clip(0, 245, 149, 303)),), rows(['Q3 (i) D 1m', 'B 1m', 'C 1m', 'A 1m']),
      '0-4', RIVERS + GLAC + RW, ID + 'p1-q3', ('page',), Q3S, row_labels=Q3_ROWS),
    T('p1-3-ii', P1, '3', '(ii)', 4, 5, L(5, 'The Physical Environment'),
      (L(5, '(ii) Indicate, by ticking (✓) the correct box, whether each feature/process', 'weathering.'),),
      (S(4, '(ii) Erosion 1m', None, clip(149, 245, 297, 303)),),
      rows(['(ii) Erosion 1m', '=Deposition 1m', '=Weathering 1m', '=Erosion 1m']),
      '0-4', RIVERS + GLAC + RW, ID + 'p1-q3-ii', ('page',), Q3S, row_labels=Q3_ROWS),
    T('p1-4-i', P1, '4', '(i)', 3, 6, L(6, 'Volcanic Activity'),
      (L(6, '(i) Match each of the locations A, B and C on the diagram above', 'table below.'),),
      (S(4, 'Q4 (i) B · 1m', None, clip(0, 376, 149, 421)),), rows(['Q4 (i) B · 1m', 'C 1m', 'A 1m']),
      '0-7', EV, ID + 'p1-q4', ('page',), Q4S, row_labels=Q4_ROWS),
    T('p1-4-ii', P1, '4', '(ii)', 3, 6, L(6, 'Volcanic Activity'),
      (L(6, '(ii) Indicate, by ticking (✓) the correct box, whether each landform', 'extrusive landform.'),),
      (S(4, '(ii) Intrusive 1m', None, clip(149, 376, 297, 421)),),
      rows(['(ii) Intrusive 1m', '=Intrusive 1m', '=Extrusive 1m']),
      '0-7', EV, ID + 'p1-q4-ii', ('page',), Q4S, row_labels=Q4_ROWS),
    T('p1-4-iii', P1, '4', '(iii)', 2, 6, L(6, 'Volcanic Activity'),
      (L(6, '(iii) Name the igneous rock type most associated with each of the following labels', 'A: B:'),),
      (S(4, '(iii) A – Valid example 1m', None, clip(0, 438, 297, 480)),),
      (fixed('A', 1, '(iii) A – Valid example 1m'), fixed('B', 1, 'B – Valid example 1m')),
      '0-1', EV + RW, ID + 'p1-q4-iii', ('page',), Q4S),
]

PART_ONE += romans(P1, '5', 7, L(7, 'Weather'),
                   (L(7, 'Examine the weather chart above from Met Éireann', 'following questions.'),),
                   ID + 'p1-q5', ('page',), [
    ('(i)', 2, (L(7, '(i) Which of the following type of front can be seen over Iceland?', 'Tick (✓) the correct box.'),
                L(7, 'Warm front'), L(7, 'Cold front'), L(7, 'Occluded front')),
     S(4, 'Q5 (i) Warm front', '(ii) 1024', LEFT), (fixed('Front', 2, 'Q5 (i) Warm front 2 marks'),), '2-7', WX),
    ('(ii)', 2, L(7, '(ii) What is the barometric pressure', 'south west of Ireland?'),
     S(4, '(ii) 1024', '(iii) Calm', LEFT), (fixed('Pressure', 2, '(ii) 1024 (mb / hPa) · 2 marks'),), '2-7', WX),
    ('(iii)', 2, (L(7, '(iii) Which of the descriptions below best describe weather conditions over Ireland?',
                    'Tick (✓) the correct box.'),
                  L(7, 'Continuous light or heavy rain'), L(7, 'Calm and dry weather'), L(7, 'Showers with strong winds')),
     S(4, '(iii) Calm dry weather', '(iv) Prevailing', LEFT),
     (fixed('Weather conditions', 2, '(iii) Calm dry weather 2 marks'),), '2-7', WX),
    ('(iv)', 2, L(7, '(iv) What is the term used to describe the wind that blows most frequently over an area?'),
     S(4, '(iv) Prevailing', 'Q6', LEFT), (fixed('Term', 2, '(iv) Prevailing (wind) 2 marks'),), '2-7', WX),
])

PART_ONE += romans(P1, '6', 8, L(8, 'Ordnance Survey Map', nth=0),
                   (L(8, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper and',
                      'following questions.'),),
                   ID + 'p1-q6', ('map', 'legend'), [
    ('(i)', 2, L(8, '(i) What is the height, in metres, at the triangulation pillar at R 055 257?'),
     S(4, 'Q6 (i) 261', '(ii) R 031', LEFT), (fixed('Height', 2, 'Q6 (i) 261 (m) · 2 marks'),), '2-6', MAP),
    ('(ii)', 2, L(8, '(ii) Give a six-figure grid reference for the confluence', 'River.'),
     S(4, '(ii) R 031 329', '(iii) 4.6', LEFT), (fixed('Grid reference', 2, '(ii) R 031 329 · 2 marks'),), '2-6', MAP),
    ('(iii)', 2, L(8, '(iii) Measure the distance, in kilometres, along the R523', 'at R 016 340.'),
     S(4, '(iii) 4.6', '(iv) Convex', LEFT), (fixed('Distance', 2, '(iii) 4.6 (km) 2 marks'),), '2-6', MAP),
    ('(iv)', 2, L(8, '(iv) Name the type of slope that is found from Q 992 327 to Q 992 319 (Slievecahill).'),
     S(4, '(iv) Convex', None, LEFT), (fixed('Slope', 2, '(iv) Convex 2 marks'),), '2-6', MAP),
])

PART_ONE += romans(P1, '7', 8, L(8, 'Aerial Photograph and Ordnance Survey Map'),
                   (L(8, 'Examine the aerial photograph of Listowel and the 1:50 000 Ordnance Survey map and',
                      'following questions.'),),
                   ID + 'p1-q7', ('aerial', 'map', 'legend'), [
    ('(i)', 2, (L(8, '(i) Indicate whether the following statement is true or false', 'correct box.'),
                L(8, 'The main land-use in the centre background is recreational.')),
     S(4, 'Q7 (i) True', '(ii) N69', RIGHT), (fixed('True or false', 2, 'Q7 (i) True · 2 marks'),), '2-8', AER),
    ('(ii)', 2, L(8, '(ii) Name the road that enters the aerial photograph in the left foreground.'),
     S(4, '(ii) N69', '(iii) Footbridge', RIGHT), (fixed('Road', 2, '(ii) N69 2 marks'),), '2-8', AER + MAP),
    ('(iii)', 2, (L(8, '(iii) Which of the following type of bridge can be seen', 'Tick (✓) the correct box.'),
                  L(8, 'Railway bridge Road bridge Footbridge')),
     S(4, '(iii) Footbridge', '(iv) SW', RIGHT), (fixed('Bridge', 2, '(iii) Footbridge 2 marks'),), '2-8', AER),
    ('(iv)', 2, L(8, '(iv) In what direction was the camera pointed', 'was taken?'),
     S(4, '(iv) SW', 'Q8', RIGHT), (fixed('Direction', 2, '(iv) SW · 2 marks'),), '2-8', AER),
])

PART_ONE += [
    T('p1-8', P1, '8', '', 8, 9, L(9, 'Aerial Photograph', nth=0),
      (L(9, 'Using accepted notation, give the location on the aerial photograph', 'in the table below.'),),
      (S(4, 'Q8 A – Left Foreground', 'Q9', RIGHT),),
      (fixed('A', 2, 'Q8 A – Left Foreground · 2 marks'), fixed('B', 2, 'B – Right Foreground · 2 marks'),
       fixed('C', 2, 'C – Centre Middleground 2 marks'), fixed('D', 2, 'D – Right Middleground 2 marks')),
      '2-8', AER, ID + 'p1-q8', ('page', 'aerial'),
      (L(9, 'Examine the aerial photograph of Listowel accompanying this paper and the Google Street',
         'same area of Listowel.'),)),
    T('p1-9-i', P1, '9', '(i)', 6, 10, L(10, 'Regions', nth=0),
      (L(10, '(i) Complete the table, by matching each of the examples of regions', 'most associated with it.'),
       L(10, 'Examples of Regions:'), Lift(10, 'Naples', 'Cool Temperate Oceanic', row=True)),
      (S(4, 'Q9 (i) The Burren', '(ii) (a)', RIGHT),),
      rows(['Q9 (i) The Burren 1m', 'Naples 1m', 'Cool Temperate Oceanic 1m', 'Fingal County Council 1m',
            'The Gaeltacht 1m', 'The Islamic World 1m']),
      '1-0', IRL + EURO, ID + 'p1-q9', ('page',),
      row_labels=(L(10, 'Geomorphological'), L(10, 'Urban'), L(10, 'Climate'), L(10, 'Administrative'),
                  L(10, 'Cultural (Language)'), L(10, 'Cultural (Religion)'))),
    T('p1-9-ii-a', P1, '9', '(ii)(a)', 1, 10, L(10, 'Regions', nth=0),
      (L(10, '(ii) Indicate whether each of the following statements is true or false', 'correct box.'),
       L(10, '(a) Core regions experience net emigration.')),
      (S(4, '(ii) (a) False', '(b) True', RIGHT),), (fixed('Statement (a)', 1, '(ii) (a) False 1m'),),
      '1-1', IRL + EURO, ID + 'p1-q9-ii-a', ('page',)),
    T('p1-9-ii-b', P1, '9', '(ii)(b)', 1, 10, L(10, 'Regions', nth=0),
      (L(10, '(ii) Indicate whether each of the following statements is true or false', 'correct box.'),
       L(10, '(b) High unemployment and abandoned factories', 'industrial decline.')),
      (S(4, '(b) True 1m', 'Q10', RIGHT),), (fixed('Statement (b)', 1, '(b) True 1m'),),
      '1-1', IRL + EURO, ID + 'p1-q9-ii-b', ('page',)),
]

PART_ONE += romans(P1, '10', 11, L(11, 'Fluvial Adjustment'),
                   (L(11, 'Examine the diagrams above, which show how a landscape can change', 'correct box.'),),
                   ID + 'p1-q10', ('page',), [
    ('(i)', 2, (L(11, '(i) Which of the following processes did the river use', 'above?'),
                L(11, 'Vertical erosion'), L(11, 'Headward erosion')),
     S(4, 'Q10 (i) Vertical Erosion', '(ii) Plateau', RIGHT), (fixed('Process', 2, 'Q10 (i) Vertical Erosion · 2 marks'),),
     '0-5', RIVERS),
    ('(ii)', 2, (L(11, '(ii) Which of the following is the name for a flat landscape formed from tectonic uplift?'),
                 L(11, 'Peneplain'), L(11, 'Plateau')),
     S(4, '(ii) Plateau', '(iii) Rejuvenation', RIGHT), (fixed('Name', 2, '(ii) Plateau · 2 marks'),), '0-5', RIVERS),
    ('(iii)', 2, (L(11, '(iii) What is a rivers response to tectonic uplift called?'),
                  L(11, 'Rejuvenation'), L(11, 'Subduction')),
     S(4, '(iii) Rejuvenation', '(iv) Incised', RIGHT), (fixed('Term', 2, '(iii) Rejuvenation 2 marks'),), '0-5', RIVERS),
    ('(iv)', 2, (L(11, '(iv) Which of the following is a feature formed as a result of a change', 'level?'),
                 L(11, 'Incised meander'), L(11, 'Delta')),
     S(4, '(iv) Incised Meander', 'Q1 (i) Norway', RIGHT), (fixed('Feature', 2, '(iv) Incised Meander 2 marks'),),
     '0-5', RIVERS),
])

# The scheme heads Question 11 "Q1".
PART_ONE += romans(P1, '11', 12, L(12, 'Statistical Interpretation'),
                   (L(12, 'Examine the table above which shows information on employment', 'following questions.'),),
                   ID + 'p1-q11', ('page',), [
    ('(i)', 2, L(12, '(i) Which country had the lowest percentage of people employed in Agriculture?'),
     S(4, 'Q1 (i) Norway', '(ii) 3', RIGHT), (fixed('Country', 2, 'Q1 (i) Norway · 2 marks'),), '2-0', TG),
    ('(ii)', 2, L(12, '(ii) In how many countries was the percentage of people employed in Industry', 'EU-27?'),
     S(4, '(ii) 3 2 marks', '(iii) 14', RIGHT), (fixed('Number of countries', 2, '(ii) 3 2 marks'),), '2-0', TG),
    ('(iii)', 2, L(12, '(iii) Calculate the difference between the percentage (%)', 'Bulgaria and the EU-27.'),
     S(4, '(iii) 14', '(iv) Norway', RIGHT), (fixed('Difference', 2, '(iii) 14 2 marks'),), '2-0', TG),
    ('(iv)', 2, L(12, '(iv) Name the country listed in the table which is not a member of the EU-27.'),
     S(4, '(iv) Norway', 'Q12(i)', RIGHT), (fixed('Country', 2, '(iv) Norway · 2 marks'),), '1-5', TG + EURO),
])

PART_ONE.append(T(
    'p1-12', P1, '12', '', 8, 13, L(13, 'Satellite Image Interpretation'),
    (L(13, 'Match each of the letters A, B, C and D with the', 'table below.'),),
    (S(4, 'Q12(i) D', None, RIGHT),), rows(['Q12(i) D · 2 marks', '(ii) C · 2 marks', '(iii) B · 2 marks',
                                           '(iv) A 2 marks'], 2),
    '2-8', AER, ID + 'p1-q12', ('page',), (L(13, 'Examine the satellite images above.'),),
    row_labels=(L(13, 'San Andreas Fault'), L(13, 'Shanty town'), L(13, 'Rainforest deforestation'),
                L(13, 'Retreating glacier'))))


# ---------------------------------------------------------------- Part Two --
def sketch(outline_line, outline_permitted, alloc, item_permitted, labels):
    return (fixed('Sketch outline' if 'Sketch' in outline_line else 'Map outline', 4,
                  outline_line, outline_permitted),
            *(Criterion(f'Feature {n}', 4, item_permitted, 'exact', alloc) for n in range(1, labels + 1)))


OS_SKETCH = sketch('Sketch Outline · 4 marks (4/0)', (0, 4),
                   ('4 features @ 4 marks each', 'Label 1 mark'), sums((0, 1, 3), (0, 1)), 4)
AERIAL_SKETCH = sketch('Sketch Outline · 4 marks (4/0)', (0, 4),
                       ('4 features @ 4 marks each', 'Named 1 mark'), sums((0, 1, 3), (0, 1)), 4)
GRAPH = (fixed('Title', 2, ('Bar Chart · Pie Chart', 'Title · 2 marks · 2 marks')),
         fixed('Axes named (bar chart) / circle and centre (pie chart)', 2,
               ('Vertical axis named', 'Horizontal axis named'), (0, 1, 2)),
         fixed('6 items illustrated', 12, '6 items illustrated', upto(12)))


def bullet_routes(prefix, items, atlas=None):
    return tuple(Route(slug(item, 34), item.rstrip('.'), ID + prefix + slug(item, 34), False,
                       keep_bullets=(item,), atlas=(atlas[item] if atlas else None))
                 for item in items)


def first_route(prefix, item):
    return ID + prefix + slug(item, 34)


def split(label, total, first, second):
    """One allocation printed as two parts examined 7/6 and 6/7 SRPs."""
    return srp(label, total, (first, second))


LANDFORMS = 'one fluvial landform or one coastal landform or one glacial landform'
SURFACE = ('The impact of flood control measures on river processes',
           'The impact of coastal defence work on coastal processes',
           'The impact of human activity on mass movement.')
ROCK_CYCLE = ('Mining', 'Extraction of building materials', 'Oil/gas exploitation',
              'Geothermal energy production.')
DEVELOPED = ('Footloose industries', 'Financial services', 'Mass tourism.')

PART_TWO = [
    T('p2-1a', P2, '1A', '', 20, 3, L(3, 'Ordnance Survey Map'),
      (L(3, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper.', 'east of easting 02.'),),
      (S(6, 'Sketch Outline', None),), OS_SKETCH, '2-6', MAP, ID + 'p2-q1a', ('map', 'legend'),
      row_labels=(None, L(3, 'The complete course of the River Feale'),
                  L(3, 'Mark on your sketch map with the letter X', 'Smearlagh River'),
                  L(3, 'An area of coniferous plantation to the north west of Listowel'),
                  L(3, 'An area of land above 200 metres east of easting 02.'))),
    T('p2-1b', P2, '1B', '', 30, 3, L(3, 'Rocks'),
      (L(3, 'Examine the formation of two sedimentary rocks, with reference to examples from Ireland.'),),
      (S(7, 'Two Irish sedimentary rocks named', 'Annotation'),),
      (pair('Two Irish sedimentary rocks named · 2 + 2 marks', 'Two Irish sedimentary rocks named'),
       split('Examination of formation of the two rocks (7/6 and 6/7 SRPs)', 13,
             f'Examination of formation of rock 1 · 7/6 x {SRPS}',
             f'Examination of formation of rock 2 · 6/7 x {SRPS}')),
      '0-1', RW, ID + 'p2-q1b'),
    T('p2-1c', P2, '1C', '', 30, 3, L(3, 'Human Interaction with Surface Processes'),
      (L(3, 'Examine how human activity impacts on surface processes', 'mass movement.'),),
      (S(8, 'Impact on process identified · 2 marks', 'Annotation'),),
      (fixed('Impact on process identified', 2, 'Impact on process identified · 2 marks'),
       srp('Examination', 14, f'Examination · 14 x {SRPS}')),
      '0-6', RW, first_route('p2-q1c-', SURFACE[0]),
      routes=bullet_routes('p2-q1c-', SURFACE, atlas=dict(zip(SURFACE, (RIVERS, SEA, RW))))),
]

PART_TWO += romans(P2, '2A', 4, L(4, 'Coastal Landforms'),
                   (L(4, 'Examine the photograph above which shows a coastal area', 'questions.'),),
                   ID + 'p2-q2a', ('page',), [
    ('(i)', 8, L(4, '(i) Name the coastal landforms labelled A, B, C and D above.'),
     S(9, '(i) · A = Cliff', '(ii) · Longshore'),
     (fixed('A', 2, '(i) · A = Cliff · 2 marks'), fixed('B', 2, 'B = Sea Stack / Stump · 2 marks'),
      fixed('C', 2, 'C = Wave Cut Platform · 2 marks'), fixed('D', 2, 'D = Sea Arch · 2 marks')), '0-10', SEA),
    ('(ii)', 2, L(4, '(ii) What is the name for the process that transports eroded material along the coastline?'),
     S(9, '(ii) · Longshore Drift', '(iii) · Valid'), (fixed('Process', 2, '(ii) · Longshore Drift · 2 marks'),),
     '0-10', SEA),
    ('(iii)', 4, L(4, '(iii) Explain briefly what is meant by destructive waves.'),
     S(9, '(iii) · Valid explanation', '(iv) · Process named'),
     (pair('(iii) · Valid explanation · 2 + 2 marks', 'Explanation'),), '0-10', SEA),
    ('(iv)', 6, L(4, '(iv) Name and explain briefly one process of coastal erosion.'),
     S(9, '(iv) · Process named', None),
     (fixed('Process named', 2, '(iv) · Process named · 2 marks'), pair('Valid explanation · 2 + 2 marks', 'Explanation')),
     '0-10', SEA),
])

PART_TWO += [
    T('p2-2b', P2, '2B', '', 30, 4, L(4, 'Earthquakes'),
      (L(4, 'With reference to example(s) you have studied, explain how the occurrence of earthquakes',
         'effects reduced.'),),
      (S(10, 'Reference to prediction of earthquakes · 2 marks', 'Annotation'),),
      (fixed('Reference to prediction of earthquakes', 2, 'Reference to prediction of earthquakes · 2 marks'),
       fixed('Reference to reducing effects of earthquakes', 2,
             'Reference to reducing effects of earthquakes · 2 marks'),
       fixed('Example', 2, 'Example · 2 marks'), srp('Explanation', 12, f'Explanation · 12 x {SRPS}')),
      '0-7', EV, ID + 'p2-q2b'),
    T('p2-2c', P2, '2C', '', 30, 4, L(4, 'Human Interaction with the Rock Cycle'),
      (L(4, 'Examine how humans interact with the rock cycle', 'Geothermal energy production.'),),
      (S(11, f'Examination · 15 x {SRPS}', 'Annotation'),), (srp('Examination', 15, f'Examination · 15 x {SRPS}'),),
      '0-6', RW, first_route('p2-q2c-', ROCK_CYCLE[0]), routes=bullet_routes('p2-q2c-', ROCK_CYCLE)),
]

PART_TWO += romans(P2, '3A', 5, L(5, 'Hot Spots'),
                   (L(5, 'Examine the map and diagram above and answer each of the following questions.'),),
                   ID + 'p2-q3a', ('page',), [
    ('(i)', 4, L(5, '(i) What is the name of the youngest volcanic island', 'shown above?'),
     S(12, '(i) · Youngest = Hawaii', '(ii) · NW'),
     (fixed('Youngest island', 2, '(i) · Youngest = Hawaii · 2 marks'), fixed('Oldest island', 2, 'Oldest = Kaua’l · 2 marks')),
     '0-7', EV + PS),
    ('(ii)', 2, L(5, '(ii) In which direction is the Pacific plate moving?'),
     S(12, '(ii) · NW', '(iii) · 3 million'), (fixed('Direction', 2, '(ii) · NW · 2 marks'),), '0-0', PS),
    ('(iii)', 2, L(5, '(iii) How many years ago did the volcanic island of Oahu form?'),
     S(12, '(iii) · 3 million', '(iv) · Any valid'), (fixed('Years', 2, '(iii) · 3 million · 2 marks'),), '0-7', EV),
    ('(iv)', 4, L(5, '(iv) Name two materials that are ejected from a volcano during an eruption.'),
     S(12, '(iv) · Any valid materials', '(v) · Valid'), (pair('(iv) · Any valid materials · 2 + 2 marks', 'Two materials'),),
     '0-7', EV),
    ('(v)', 4, L(5, '(v) Explain briefly the term lithosphere.'),
     S(12, '(v) · Valid explanation', '(vi) · Valid'), (pair('(v) · Valid explanation · 2 + 2 marks', 'Explanation'),),
     '0-0', PS),
    ('(vi)', 4, L(5, '(vi) Explain briefly what is meant by basic lava.'),
     S(12, '(vi) · Valid explanation', None), (pair('(vi) · Valid explanation · 2 + 2 marks', 'Explanation'),),
     '0-7', EV),
])

PART_TWO += [
    T('p2-3b', P2, '3B', '', 30, 5, L(5, 'Surface Processes'),
      (L(5, '(i) Examine the role of the process of deposition', 'that you have studied.'),),
      (S(13, 'Landform named · 2 marks', 'Annotation'),),
      (fixed('Landform named', 2, 'Landform named · 2 marks'), srp('Examination', 14, f'Examination · 14 x {SRPS}')),
      '0-9', RIVERS, ID + 'p2-q3b-route-i-fluvial-landform',
      routes=(
          Route('route-i-fluvial-landform', 'Route (i) · one fluvial landform',
                ID + 'p2-q3b-route-i-fluvial-landform', False, ((LANDFORMS, 'one fluvial landform'),),
                topic='0-9', atlas=RIVERS),
          Route('route-i-coastal-landform', 'Route (i) · one coastal landform',
                ID + 'p2-q3b-route-i-coastal-landform', False, ((LANDFORMS, 'one coastal landform'),),
                topic='0-10', atlas=SEA),
          Route('route-i-glacial-landform', 'Route (i) · one glacial landform',
                ID + 'p2-q3b-route-i-glacial-landform', False, ((LANDFORMS, 'one glacial landform'),),
                topic='0-11', atlas=GLAC),
          Route('route-ii', 'Route (ii)', ID + 'p2-q3b-route-ii', False,
                prompt=(L(5, '(ii) Describe and explain the factors governing', 'that you have studied.'),),
                scheme=(S(14, 'Factors identified', 'Annotation'),),
                criteria=(pair('Factors identified · 2 + 2 marks', 'Factors identified'),
                          fixed('Mass movement process named', 2, 'Mass movement process named · 2 marks'),
                          srp('Description/explanation', 12, f'Description/explanation · 12 x {SRPS}')),
                topic='0-8', atlas=RW),
      )),
    T('p2-3c', P2, '3C', '', 30, 5, L(5, 'Plate Boundaries'),
      (L(5, 'Describe and explain destructive plate boundaries.'),),
      (S(15, f'Description/Explanation · 15 x {SRPS}', 'Annotation'),),
      (srp('Description/explanation', 15, f'Description/Explanation · 15 x {SRPS}'),),
      '0-0', PS, ID + 'p2-q3c'),
    # Question 4
    T('p2-4a', P2, '4A', '', 20, 6, L(6, 'Map Skills'),
      (L(6, 'Draw an outline map of a European region (not in Ireland) that you have studied.',
         'transport route/feature.'),),
      (S(16, 'Map outline', None),),
      sketch('Map outline · 4 marks graded (4/2/0)', (0, 2, 4),
             ('4 features @ 4 marks each', 'Named 2 marks'), sums((0, 1, 2), (0, 2)), 4),
      '1-5', EURO, ID + 'p2-q4a',
      row_labels=(None, L(6, 'The outline of one named feature of relief (upland or lowland)'),
                  L(6, 'One named urban centre'), L(6, 'The course of one named river'),
                  L(6, 'One named transport route/feature.'))),
    T('p2-4b', P2, '4B', '', 30, 6, L(6, 'Secondary Economic Activity'),
      (L(6, 'Account for the development of one secondary economic activity in an Irish region', 'have studied.'),),
      (S(17, f'Examination · 15 x {SRPS}', 'Annotation'),), (srp('Examination', 15, f'Examination · 15 x {SRPS}'),),
      '1-4', IRL, ID + 'p2-q4b'),
    T('p2-4c', P2, '4C', '', 30, 6, L(6, 'Population Dynamics'),
      (L(6, 'Account for population distribution throughout a Continental', 'that you have studied.'),),
      (S(18, f'Examination · 15 x {SRPS}', 'Annotation'),), (srp('Examination', 15, f'Examination · 15 x {SRPS}'),),
      '1-6', CONT, ID + 'p2-q4c'),
]

PART_TWO += romans(P2, '5A', 7, L(7, 'Irish Transport'),
                   (L(7, 'Examine the bar chart above which shows information on transport in Ireland',
                      'answer the following questions.'),),
                   ID + 'p2-q5a', ('page',), [
    ('(i)', 2, L(7, '(i) Which mode of transport carried the most passengers in 2019?'),
     S(19, '(i) · Bus', '(ii) · Luas'), (fixed('Mode of transport', 2, '(i) · Bus · 2 marks'),), '2-0', TG),
    ('(ii)', 2, L(7, '(ii) Which mode of transport had the largest growth between 2018 and 2019?'),
     S(19, '(ii) · Luas', '(iii) · 29'), (fixed('Mode of transport', 2, '(ii) · Luas · 2 marks'),), '2-0', TG),
    ('(iii)', 4, L(7, '(iii) Calculate the difference between the number of passengers', 'in 2019 and 2020.'),
     S(19, '(iii) · 29', '(iv) · Valid'), (fixed('Difference', 4, '(iii) · 29 (million) · 4 marks'),), '2-0', TG),
    ('(iv)', 4, L(7, '(iv) Name two international passenger ferry terminals in Ireland.'),
     S(19, '(iv) · Valid ferry terminal names', '(v) · Valid'),
     (pair('(iv) · Valid ferry terminal names · 2 + 2 marks', 'Two ferry terminals'),), '1-4', IRL),
    ('(v)', 4, L(7, '(v) Explain briefly one reason why the number of passengers', 'in 2020.'),
     S(19, '(v) · Valid explanation', '(vi) · Valid'), (pair('(v) · Valid explanation · 2 + 2 marks', 'Reason'),),
     '1-4', IRL),
    ('(vi)', 4, L(7, '(vi) Explain briefly one benefit of more people using public transport.'),
     S(19, '(vi) · Valid explanation', None), (pair('(vi) · Valid explanation · 2 + 2 marks', 'Benefit'),),
     '1-4', IRL),
])

PART_TWO += [
    T('p2-5b', P2, '5B', '', 30, 7, L(7, 'Primary Economic Activity'),
      (L(7, 'Explain two factors that influenced the development of one primary economic activity',
         'that you have studied.'),),
      (S(20, 'Factors identified · 2 + 2 marks', 'Annotation'),),
      (pair('Factors identified · 2 + 2 marks', 'Factors identified'),
       split('Explanation of the two factors (7/6 and 6/7 SRPs)', 13,
             'Explanation of Factor 1 · 7/6 x SRPs', 'Explanation of Factor 2 · 6/7 x SRPs')),
      '1-6', CONT, ID + 'p2-q5b'),
    T('p2-5c', P2, '5C', '', 30, 7, L(7, 'Industrial Decline'),
      (L(7, 'Examine the causes and impacts of industrial decline', 'you have studied.'),),
      (S(21, 'Cause identified · 2 marks', 'Annotation'),),
      (fixed('Cause identified', 2, 'Cause identified · 2 marks'), fixed('Impact identified', 2, 'Impact identified · 2 marks'),
       srp('Examination', 13, 'Examination · 13 x SRPs')),
      '1-1', IRL + EURO, ID + 'p2-q5c'),
]

PART_TWO += romans(P2, '6A', 8, L(8, 'Irish Agriculture'),
                   (L(8, 'Examine the stacked bar chart above showing the percentage composition', 'following questions.'),),
                   ID + 'p2-q6a', ('page',), [
    ('(i)', 2, L(8, '(i) Which region had the highest percentage output of cattle in 2020?'),
     S(22, '(i) · West', '(ii) · Sheep'), (fixed('Region', 2, '(i) · West · 2 marks'),), '2-0', TG),
    ('(ii)', 2, L(8, '(ii) What output had the smallest percentage share in the Mid-West region?'),
     S(22, '(ii) · Sheep', '(iii) · South East'), (fixed('Output', 2, '(ii) · Sheep · 2 marks'),), '2-0', TG),
    ('(iii)', 4, L(8, '(iii) Name the two regions that had the highest percentage output in crops.'),
     S(22, '(iii) · South East', '(iv) · Valid crop'),
     (fixed('Region 1', 2, '(iii) · South East · 2 marks'), fixed('Region 2', 2, 'Dublin & Mid East · 2 marks')),
     '2-0', TG),
    ('(iv)', 2, L(8, '(iv) Name one crop commonly grown in Ireland.'),
     S(22, '(iv) · Valid crop', '(v) · Valid'), (fixed('Crop', 2, '(iv) · Valid crop · 2 marks'),), '1-4', IRL),
    ('(v)', 4, L(8, '(v) Explain briefly what is meant by the term market gardening.'),
     S(22, '(v) · Valid explanation', '(vi) · Valid Policy'), (pair('(v) · Valid explanation · 2 + 2 marks', 'Explanation'),),
     '1-4', IRL),
    ('(vi)', 6, L(8, '(vi) Name and explain briefly one European Union policy', 'of agriculture.'),
     S(22, '(vi) · Valid Policy Name', None),
     (fixed('Policy named', 2, '(vi) · Valid Policy Name · 2 marks'), pair('Valid explanation · 2 + 2 marks', 'Explanation')),
     '3-3', EU + IRL),
])

PART_TWO += [
    T('p2-6b', P2, '6B', '', 30, 8, L(8, 'Socio-Economic Regions'),
      (L(8, 'Examine how the characteristics of core regions', 'have studied.'),),
      (S(23, 'Impact on economic activity in core region identified', 'Annotation'),),
      (fixed('Impact in core region identified', 2, 'Impact on economic activity in core region identified · 2 marks'),
       fixed('Impact in peripheral region identified', 2,
             'Impact on economic activity in peripheral region identified · 2 marks'),
       split('Examination of the core and peripheral regions (7/6 and 6/7 SRPs)', 13,
             f'Examination of core region · 7/6 x {SRPS}', f'Examination of peripheral region · 6/7 x {SRPS}')),
      '1-1', EURO, ID + 'p2-q6b'),
    T('p2-6c', P2, '6C', '', 30, 8, L(8, 'Cultural Regions'),
      (L(8, 'Examine how culture can be used to define regions', 'have studied.'),),
      (S(24, 'Example · 2 marks', 'Annotation'),),
      (fixed('Example', 2, 'Example · 2 marks'), srp('Examination', 14, f'Examination · 14 x {SRPS}')),
      '1-3', IRL + EURO + CONT, ID + 'p2-q6c'),
    # Question 7
    T('p2-7a', P2, '7A', '', 20, 10, L(10, 'Aerial Photograph'),
      (L(10, 'Examine the aerial photograph of Listowel accompanying this paper.', 'suitable for redevelopment.'),),
      (S(26, 'Sketch Outline', None),), AERIAL_SKETCH, '2-8', AER, ID + 'p2-q7a', ('aerial',),
      row_labels=(None, L(10, 'The river'), L(10, 'A bridge'), L(10, 'An industrial area in the left background'),
                  L(10, 'A brownfield site suitable for redevelopment.'))),
    T('p2-7b', P2, '7B', '', 30, 10, L(10, 'Developing Economy'),
      (L(10, 'Examine the challenges resulting from colonisation', 'that you have studied.'),),
      (S(27, 'Developing economy named · 2 marks', 'Annotation'),),
      (fixed('Developing economy named', 2, 'Developing economy named · 2 marks'),
       pair('Challenges identified · 2 + 2 marks', 'Challenges identified'),
       srp('Examination', 12, f'Examination · 12 x {SRPS}')),
      '3-1', DEV, ID + 'p2-q7b'),
    T('p2-7c', P2, '7C', '', 30, 10, L(10, 'European Union Policy'),
      (L(10, 'Examine the impact of European Union policy on regional development in Ireland.'),),
      (S(28, 'Impact on regional development identified · 2 marks', 'Annotation'),),
      (fixed('Impact on regional development identified', 2, 'Impact on regional development identified · 2 marks'),
       srp('Examination', 14, f'Examination · 14 x {SRPS}')),
      '3-3', EU, ID + 'p2-q7c'),
]

# The scheme prints 8A(ii) as "(i)", below the graph's annotation table.
PART_TWO += romans(P2, '8A', 11, L(11, 'Gross Domestic Product', nth=0),
                   (L(11, 'Examine the data above showing the breakdown of the Gross Domestic Product',
                      'following questions.'),),
                   ID + 'p2-q8a', ('page',), [
    ('(i)', 16, L(11, '(i) Using graph paper, draw a suitable graph to illustrate this data.'),
     S(29, 'Bar Chart · Pie Chart', 'Annotation'), GRAPH, '2-0', TG),
    ('(ii)', 4, L(11, '(ii) Explain briefly what is meant by Gross Domestic Product per Capita (GDP).'),
     S(29, 'Valid explanation · 2 + 2 marks', None), (pair('Valid explanation · 2 + 2 marks', 'Explanation'),),
     '3-0', ECON),
])

REASON = ('Three reasons @ 10 marks each.', 'For each reason:', 'Reason stated · 2 marks',
          'OS map evidence · 2 marks', f'Explanation · 3 x {SRPS}')
PART_TWO += [
    T('p2-8b', P2, '8B', '', 30, 11, L(11, 'Economic Development – Developed Economy'),
      (L(11, 'Examine the development of one of the following with reference to a developed economy', 'Mass tourism.'),),
      (S(30, 'Developed economy named · 2 marks', 'Annotation'),),
      (fixed('Developed economy named', 2, 'Developed economy named · 2 marks'),
       srp('Examination', 14, f'Examination · 14 x {SRPS}')),
      '3-0', ECON, first_route('p2-q8b-', DEVELOPED[0]), routes=bullet_routes('p2-q8b-', DEVELOPED)),
    T('p2-8c', P2, '8C', '', 30, 11, L(11, 'Location of Economic Activity'),
      (L(11, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper.',
         'to support each reason.'),),
      (S(31, 'Three reasons @ 10 marks each.', 'Annotation'),),
      (Criterion('Reason to locate 1', 10, evens(10), 'srp', REASON),
       Criterion('Reason to locate 2', 10, evens(10), 'srp', REASON),
       Criterion('Reason not to locate', 10, evens(10), 'srp', REASON)),
      '2-6', MAP + ECON, ID + 'p2-q8c', ('map', 'legend')),
]

PART_TWO += romans(P2, '9A', 12, L(12, 'Irish Trade'),
                   (L(12, 'Study the infographic above showing information on Irish trade', 'following questions.'),),
                   ID + 'p2-q9a', ('page',), [
    ('(i)', 2, L(12, '(i) What was the value (in €billion) of Ireland’s imported goods that came from the UK?'),
     S(32, '(i) · 19.5', '(ii) · Pure'), (fixed('Value', 2, '(i) · 19.5 (€billion) · 2 marks'),), '2-0', TG),
    ('(ii)', 2, L(12, '(ii) Name one product shown on the infographic that was exported from Ireland in 2021.'),
     S(32, '(ii) · Pure breeding', '(iii) · 53,000'), (fixed('Product', 2, '(ii) · Pure breeding horses / beer · 2 marks'),),
     '2-0', TG),
    ('(iii)', 2, L(12, '(iii) What was the quantity of potatoes (in tonnes) imported into Ireland in 2021?'),
     S(32, '(iii) · 53,000', '(iv) · Valid'), (fixed('Quantity', 2, '(iii) · 53,000 (tonnes) · 2 marks'),), '2-0', TG),
    ('(iv)', 4, L(12, '(iv) Name two examples of services exported from Ireland.'),
     S(32, '(iv) · Valid services', '(v) · 61.9'), (pair('(iv) · Valid services named · 2 + 2 marks', 'Two services'),),
     '3-0', ECON),
    ('(v)', 4, L(12, '(v) Calculate Ireland’s balance of trade for 2021 (in €billion).'),
     S(32, '(v) · 61.9', '(vi) · Trade'), (fixed('Balance of trade', 4, '(v) · 61.9 (€billion) · 4 marks'),), '2-0', TG),
    ('(vi)', 2, L(12, '(vi) State whether Ireland’s balance of trade for 2021 was a trade deficit or trade surplus.'),
     S(32, '(vi) · Trade surplus', '(vii) Valid'), (fixed('Deficit or surplus', 2, '(vi) · Trade surplus · 2 marks'),),
     '3-0', ECON),
    ('(vii)', 4, L(12, '(vii) Explain briefly one way that Brexit has impacted on Ireland’s trade patterns.'),
     S(32, '(vii) Valid explanation', None), (pair('(vii) Valid explanation · 2 + 2 marks', 'Impact of Brexit'),),
     '3-3', ECON + EU),
])

PART_TWO += [
    T('p2-9b', P2, '9B', '', 30, 12, L(12, 'Multinational Company'),
      (L(12, 'With reference to one multinational company that you have studied', 'Location of markets.'),),
      (S(33, 'MNC Named · 2 marks', 'Annotation'),),
      (fixed('MNC named', 2, 'MNC Named · 2 marks'),
       srp('Description and explanation 1', 7, f'Description and explanation 1 · 7 x {SRPS}'),
       srp('Description and explanation 2', 7, f'Description and explanation 2 · 7 x {SRPS}')),
      '3-2', MNC, ID + 'p2-q9b'),
    T('p2-9c', P2, '9C', '', 30, 12, L(12, 'Conflict of Interest'),
      (L(12, 'Examine how conflict can arise between economic interests', 'that you have studied.'),),
      (S(34, 'Example · 2 marks', 'Annotation'),),
      (fixed('Example', 2, 'Example · 2 marks'), srp('Examination', 14, f'Examination · 14 x {SRPS}')),
      '3-4', ENV, ID + 'p2-q9c'),
    # Question 10
    T('p2-10a', P2, '10A', '', 20, 13, L(13, 'Aerial Photograph'),
      (L(13, 'Examine the aerial photograph of Listowel accompanying this paper.', 'An off-street carpark.'),),
      (S(35, 'Sketch Outline', None),), AERIAL_SKETCH, '2-8', AER + URB, ID + 'p2-q10a', ('aerial',),
      row_labels=(None, L(13, 'The river'), L(13, 'A graveyard in the left foreground'),
                  L(13, 'An ecclesiastical building in the left middleground'), L(13, 'An off-street carpark.'))),
    T('p2-10b', P2, '10B', '', 30, 13, L(13, 'Migration'),
      (L(13, 'With reference to a developed region that you have studied', 'Urban areas'),),
      (S(36, 'Impact on rural area identified · 2 marks', 'Annotation'),),
      (fixed('Impact on rural area identified', 2, 'Impact on rural area identified · 2 marks'),
       fixed('Impact on urban area identified', 2, 'Impact on urban area identified · 2 marks'),
       split('Explanation of the two impacts (7/6 and 6/7 SRPs)', 13,
             f'Explanation of impact on rural area · 7/6 x {SRPS}',
             f'Explanation of impact on urban area · 6/7 x {SRPS}')),
      '4-2', POP, ID + 'p2-q10b'),
    T('p2-10c', P2, '10C', '', 30, 13, L(13, 'Central Place Theory', nth=0),
      (L(13, 'Describe and explain Central Place Theory with reference to example(s)', 'studied.'),),
      (S(37, 'Example · 2 marks', 'Annotation'),),
      (fixed('Example', 2, 'Example · 2 marks'),
       srp('Description/explanation', 14, 'Description/Explanation · 14 x SRPs')),
      '4-3', URB, ID + 'p2-q10c'),
]

PART_TWO += romans(P2, '11A', 14, L(14, 'Displaced Populations'),
                   (L(14, 'Examine the data above showing the origin of the world’s displaced population',
                      'following questions.'),),
                   ID + 'p2-q11a', ('page',), [
    ('(i)', 16, L(14, '(i) Using graph paper, draw a suitable graph to illustrate this data.'),
     S(38, 'Bar Chart · Pie Chart', 'Annotation'), GRAPH, '2-0', TG),
    ('(ii)', 4, L(14, '(ii) Explain briefly one push factor that forces people to leave their homes.'),
     S(38, 'Valid explanation · 2 + 2 marks', None), (pair('Valid explanation · 2 + 2 marks', 'Push factor'),),
     '4-2', POP),
])

PHASE = ('(ii) · Explanation of each phase', '@ 6 marks each · 3 @ (2 + 2 + 2 marks)')
PART_TWO += romans(P2, '11B', 14, L(14, 'Historical Settlement'),
                   (L(14, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper and',
                      'following questions.'),),
                   ID + 'p2-q11b', ('map', 'legend'), [
    ('(i)', 12, L(14, '(i) Name and locate using six-figure grid references', 'Ordnance Survey map.'),
     S(39, '(i) · Three historical phases named', '(ii) · Explanation'),
     (fixed('Three historical phases named', 6, '(i) · Three historical phases named · 2 + 2 + 2 marks', (0, 2, 4, 6)),
      fixed('Location of map evidence', 6, 'Location of map evidence · 2 + 2 + 2 marks', (0, 2, 4, 6))),
     '4-3', URB + MAP),
    ('(ii)', 18, L(14, '(ii) Explain briefly each of the three phases', '(i) above.'),
     S(39, '(ii) · Explanation of each phase', 'Annotation'),
     tuple(Criterion(f'Phase {n}', 6, (0, 2, 4, 6), 'srp', PHASE) for n in (1, 2, 3)),
     '4-3', URB + MAP),
])

PART_TWO += [
    T('p2-11c', P2, '11C', '', 30, 14, L(14, 'Urban Land-use'),
      (L(14, 'Examine how the location of two of the following land-uses has changed', 'Commercial land-use.'),),
      (S(40, 'Irish city named · 2 marks', 'Annotation'),),
      (fixed('Irish city named', 2, 'Irish city named · 2 marks'),
       srp('Examination of land use 1', 7, f'Examination of land use 1 · 7 x {SRPS}'),
       srp('Examination of land use 2', 7, f'Examination of land use 2 · 7 x {SRPS}')),
      '4-4', LANDUSE + URB, ID + 'p2-q11c'),
]

PART_TWO += romans(P2, '12A', 15, L(15, 'Population Change in Ireland'),
                   (L(15, 'Examine the infographic above showing the population and migration estimates', 'following questions.'),),
                   ID + 'p2-q12a', ('page',), [
    ('(i)', 2, L(15, '(i) What percentage (%) of Ireland’s population lived in Dublin according to estimates?'),
     S(41, '(i) · 28.4', '(ii) · 120,700'), (fixed('Percentage', 2, '(i) · 28.4(%) · 2 marks'),), '4-0', POP + TG),
    ('(ii)', 2, L(15, '(ii) What was the estimated total number of immigrants', 'April 2022?'),
     S(41, '(ii) · 120,700', '(iii) · 4,331,300'), (fixed('Immigrants', 2, '(ii) · 120,700 · 2 marks'),), '4-2', POP),
    ('(iii)', 4, L(15, '(iii) Calculate the estimated number of people living in Ireland', 'years of age.'),
     S(41, '(iii) · 4,331,300', '(iv) · Valid'), (fixed('Calculation', 4, '(iii) · 4,331,300 · 4 marks'),),
     '4-0', POP + TG),
    ('(iv)', 4, L(15, '(iv) State two reasons why Irish people emigrate.'),
     S(41, '(iv) · Valid reasons', '(v) · Valid'), (pair('(iv) · Valid reasons · 2 + 2 marks', 'Two reasons'),),
     '4-2', POP),
    ('(v)', 4, L(15, '(v) Explain briefly one challenge created by having more people aged 65 and over.'),
     S(41, '(v) · Valid explanation', '(vi) · Valid'), (pair('(v) · Valid explanation · 2 + 2 marks', 'Challenge'),),
     '4-1', POP),
    ('(vi)', 4, L(15, '(vi) Explain briefly one benefit to Ireland of inward migration.'),
     S(41, '(vi) · Valid explanation', None), (pair('(vi) · Valid explanation · 2 + 2 marks', 'Benefit'),),
     '4-2', POP),
])

PART_TWO += [
    T('p2-12b', P2, '12B', '', 30, 15, L(15, 'Urban Growth – Developing World City'),
      (L(15, 'Problems can develop from the growth and expansion of urban centres.', 'that you have studied.'),),
      (S(42, 'Problems identified · 2 + 2 marks', 'Annotation'),),
      (pair('Problems identified · 2 + 2 marks', 'Problems identified'),
       fixed('Developing world city', 2, 'Developing world city · 2 marks'),
       srp('Discussion', 12, f'Discussion · 12 x {SRPS}')),
      '4-5', URB, ID + 'p2-q12b'),
    T('p2-12c', P2, '12C', '', 30, 15, L(15, 'Overpopulation'),
      (L(15, 'Examine one cause and one effect of overpopulation', 'have studied.'),),
      (S(43, 'Cause identified · 2 marks', 'Annotation'),),
      (fixed('Cause identified', 2, 'Cause identified · 2 marks'),
       srp('Examination of cause', 6, f'Examination of cause · 6 x {SRPS}'),
       fixed('Effect identified', 2, 'Effect identified · 2 marks'),
       srp('Examination of effect', 6, f'Examination of effect · 6 x {SRPS}'),
       fixed('Example', 2, 'Example · 2 marks')),
      '4-1', POP, ID + 'p2-q12c'),
]

# ------------------------------------------------------------------ Options --
OC = (S(45, '*Overall Coherence (20 marks)', None, table=True),)


def option(q, page, theme, note_nth, prompt, scheme_page, topic, atlas, after=None, end=None):
    return T(f'p2-{q}', P2, q, '', 80, page, theme, (prompt,),
             (S(scheme_page, 'Number of aspects', end, None, after), *OC),
             (Criterion('Aspects (3 @ 20 marks or 4 @ 15 marks)', 60, upto(60), 'srp',
                        ('Number of aspects', '?For each aspect:', 'Identifying aspect', '8 x SRP')),
              Criterion('Overall coherence', 20, (0, 6, 10, 14, 17, 20), 'exact',
                        ('Overall Coherence · 20 marks graded*', '*Overall Coherence (20 marks)', 'Excellent · 20',
                         'Very Good · 17', 'Good · 14', 'Fair · 10', 'Weak · 6', 'Poor · 0'))),
             topic, (atlas,), ID + f'p2-q{q}',
             stem=(L(page, 'Note: It is better to discuss three or four aspects', 'large number of points.',
                     nth=note_nth),))


GI, GE = H + 'option-global-interdependence', H + 'option-geoecology'
CI, AO = H + 'option-culture-identity', H + 'option-atmosphere-ocean'
OPTIONS = [
    option('13', 17, L(17, 'Global Interdependence'), 0,
           L(17, 'Discuss the causes and impacts of one global environmental issue that you have studied.'),
           47, '5-3', GI),
    option('14', 17, L(17, 'Global Interdependence'), 0,
           L(17, 'Examine the influence of Eurocentric thinking', 'underdevelopment.'), 48, '5-0', GI,
           after='14.', end='15.'),
    option('15', 17, L(17, 'Global Interdependence'), 0,
           L(17, 'Sustainable exploitation of resources represents', 'Discuss.'), 48, '5-3', GI, after='15.'),
    option('16', 17, L(17, 'Geoecology'), 1,
           L(17, 'Describe and explain the composition and characteristics of one Irish soil type', 'studied.'),
           49, '6-0', GE),
    option('17', 17, L(17, 'Geoecology'), 1,
           L(17, 'Examine how any three of the processes below have influenced soil formation', 'Soil erosion.'),
           50, '6-1', GE, after='17.', end='18.'),
    option('18', 17, L(17, 'Geoecology'), 1,
           L(17, 'Examine the characteristics of one biome that you have studied', 'Fauna.'), 50, '6-2', GE,
           after='18.'),
    option('19', 18, L(18, 'Culture and Identity'), 0,
           L(18, 'Examine the strategies that have been or could be implemented', 'minority languages.'),
           51, '7-0', CI),
    option('20', 18, L(18, 'Culture and Identity'), 0,
           L(18, 'Conflicts can occur between political structures and cultural groups.', 'Discuss.'),
           52, '7-1', CI, after='20.', end='21.'),
    option('21', 18, L(18, 'Culture and Identity'), 0,
           L(18, 'Examine the impact of colonialism and migration on ethnic/racial patterns.'), 52, '7-0', CI,
           after='21.'),
    option('22', 18, L(18, 'The Atmosphere – Ocean Environment'), 1,
           L(18, 'Describe and account for the specific characteristics of one global climate type', 'studied.'),
           53, '8-4', AO),
    option('23', 18, L(18, 'The Atmosphere – Ocean Environment'), 1,
           L(18, 'Exchanges of water between oceans and atmosphere', 'Discuss.'), 54, '8-2', AO,
           after='23.', end='24.'),
    option('24', 18, L(18, 'The Atmosphere – Ocean Environment'), 1,
           L(18, 'Describe the formation of each of the following and discuss its impact', 'Land and sea breezes.'),
           54, '8-3', AO, after='24.'),
]

TASKS = [*PART_ONE, *PART_TWO, *OPTIONS]

ID_CORRECTION_REASON = 'No deferred card shipped before this review, so no id is re-scoped.'

# No 2023 Higher deferred card shipped before this review.
LEGACY_IDS: list[str] = []
