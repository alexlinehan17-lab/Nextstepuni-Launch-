"""Independent review ledger: Leaving Certificate Geography 2025 Higher Level, deferred sitting.

The SEC's deferred examination is a paper of its own. Sources (English
editions, harvested in paper-trail-corpus/deferredexams/2025 and
deferredmarkingschemes/2025, filed by Paper Trail as "<fileid>-deferred";
sizes pinned in EXPECTED_SOURCES and the generated audit): Part One and
Answerbook LC005ALP042EV (48 pages), Part Two LC005ALP043EV (20 pages),
marking scheme LC005ALP000EV (68 pages), and the sitting's own companions:
the 1:50 000 Longford map LC005CLP003EV, its legend LC005CLPC00EV and the
Longford aerial photograph LC005CLP004EV, published only as a JPEG.

Visual sweep (every page rendered and read on 2026-11-19):
  Part One booklet p1 cover; p2 instructions (Part One "Attempt any TEN",
  80 marks; Part Two "attempt FOUR"); p3-p13 Questions 1-12 (p8 holds Q6 and
  Q7); p14 Part Two answerbook instructions; p15-p18 graph paper; p19-p47
  lined answer pages; p48 back cover and copyright notice.
  Part Two booklet p1 cover; p2 Part Two instructions; p3-p8 Sections 1-2
  (Q1-Q6); p9 Section 3 divider; p10-p15 Electives (Q7-Q12); p16 Section 4
  divider and note; p17-p18 Options (Q13-Q24); p19 "Do not hand this up";
  p20 back cover and copyright notice.
  Scheme p1 cover; p2 the note on deferred marking schemes; p3 notes and
  annotation key; p4 Part One table (two columns, Q1-Q6 and Q7-Q12, each
  question's parts side by side); p5 the 2025 Part Two adjustment rule;
  p6-p24 Q1-Q6 (each reprints its question); p25 Electives divider; p26-p43
  Q7-Q12; p44 Options divider; p45 the options' Outline Marking Scheme and
  Overall Coherence descriptors (Questions 13-24); p46 option annotations;
  p47-p58 Q13-Q24; p59-p64 Geographical Investigation (coursework); p65
  investigation topics; p66 Irish-language bonus marks; p67-p68 blank.
  Companions: Longford map extract (the N4, the R198, the Camlin River);
  OS legend sheet; oblique aerial photograph of Longford.

This deferred scheme was "finalised only for the questions attempted by the
candidates" (its p2 note): it prints no allocation for 7A, 7B and 7C, which
are carded with one row, "The scheme prints no answer for this part.",
whose guidance is that note (p2). It prints its own outline for options 17,
18 and 21 only; every option is marked on the scheme's Outline Marking
Scheme and Overall Coherence descriptors for Questions 13-24 (p45), the
general criteria it sets for all of them. Every other part carries its
published allocation. The Part One table prints each question's parts side
by side; each part reads its own column. It numbers Q10's (iii)(a) and (b)
"(iii)" and "(iv)", and 5A's (iv) and (v) "(v)" and "(vi)"; each is placed by
its wording. Its Q3(ii) column reads Erosion, Erosion, Erosion, Deposition
down the printed rows (U-shaped valley, cirque, drumlin, pyramidal peak), and
is carried as printed. 8B prices "3 x reasons @ 10 marks each" over its two
printed parts: (i)'s two reasons and (ii)'s one. Finite printed choices are
routes: 1C, 3B, 7B and 12C one of the printed bullets; 2B (i) or (ii), with
(i)'s one fluvial or one coastal or one glacial landform. Choose-N-of-M pools
are one card with every printed item (4B two of four, 10C any two of three,
12B two of three, 13 and 16 three of four).
"""

from geography_review import (
    Criterion, Lift, Route, SchemeSlice, Task, evens, fixed, slug, srp, sums, upto,
)

YEAR = 2025
LEVEL = 'higher'
REVIEWED_AT = '2026-11-19'
PAPER_PAGES = {1: 48, 2: 20}
SCHEME_PAGES = 68
QUESTION_TARIFFS = {1: {str(n): 8 for n in range(1, 13)},
                    2: {**{f'{n}{x}': (20 if x == 'A' else 30)
                           for n in range(1, 13) for x in 'ABC'},
                        **{str(n): 80 for n in range(13, 25)}}}

EXPECTED_SOURCES = {
    'paper1': ('LC005ALP042EV.pdf', 6817377),
    'paper2': ('LC005ALP043EV.pdf', 3940457),
    'scheme': ('LC005ALP000EV.pdf', 928335),
    'map': ('LC005CLP003EV.pdf', 3493560),
    'legend': ('LC005CLPC00EV.pdf', 2235899),
    'aerial': ('LC005CLP004EV.jpg', 8125277),
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
               4: 'Part One table', 5: 'Part Two adjustment rule (2025 additional choice)',
               **{p: 'Part Two allocation' for p in range(6, 25)}, 25: 'section divider',
               **{p: 'Part Two allocation' for p in range(26, 44)}, 44: 'section divider',
               45: 'option outline and coherence descriptors', 46: 'option annotations',
               **{p: 'option allocation' for p in range(47, 59)},
               **{p: 'geographical investigation (coursework)' for p in range(59, 65)},
               65: 'investigation topics', 66: 'Irish-language bonus marks', 67: 'blank', 68: 'blank'},
}

EXPECTED_SELECTION_SCAN = [
    [1, 2, 'attempt any ten'], [1, 2, 'attempt four'], [1, 3, 'attempt any ten'], [1, 13, 'any two'],
    [2, 2, 'attempt four'],
    [2, 3, 'one of the following'],
    [2, 4, 'answer (i) or (ii)'], [2, 4, 'or one'], [2, 4, 'or one'],
    [2, 5, 'one of the following'],
    [2, 6, 'two of the following'],
    [2, 7, 'any two'],
    [2, 10, 'one of the following'],
    [2, 11, 'choose'], [2, 11, 'choose'],
    [2, 13, 'any two'],
    [2, 15, 'two of the following'], [2, 15, 'one of the following'],
    [2, 17, 'three of the following'], [2, 17, 'three of the following'], [2, 17, 'any one'],
]
SELECTION_REVIEW = [
    {'scan': [[1, 2, 'attempt any ten'], [1, 2, 'attempt four'], [1, 3, 'attempt any ten'],
              [2, 2, 'attempt four']],
     'kind': 'exam-attempt-rule',
     'reason': 'Part One any ten of twelve and Part Two four questions are attempt rules; every question is carded.'},
    {'scan': [[2, 3, 'one of the following'], [2, 5, 'one of the following'], [2, 10, 'one of the following'],
              [2, 15, 'one of the following']],
     'kind': 'closed-choose-one',
     'reason': '1C one of three printed features -> 3 routes; 3B one of four printed interactions -> 4 routes; '
               '7B one of three printed activities -> 3 routes; 12C one of two printed contexts -> 2 routes.'},
    {'scan': [[2, 4, 'answer (i) or (ii)'], [2, 4, 'or one'], [2, 4, 'or one']], 'kind': 'closed-route',
     'reason': '2B: (i) or (ii); (i) offers one fluvial OR one coastal OR one glacial landform -> 4 routes.'},
    {'scan': [[2, 11, 'choose'], [2, 11, 'choose']], 'kind': 'printed-wording',
     'reason': '8B: "a multinational company might choose to locate ... might choose not to locate" is the '
               'question\'s wording, not a choice offered to the candidate.'},
    {'scan': [[2, 6, 'two of the following'], [2, 13, 'any two'], [2, 15, 'two of the following'],
              [2, 17, 'three of the following'], [2, 17, 'three of the following']],
     'kind': 'choose-n-one-card',
     'reason': '4B two of four printed factors, 10C any two of three printed issues, 12B two of three printed '
               'land-uses, 13 three of four printed themes and 16 three of four printed processes -> one card '
               'each with every printed item (choice is not a route; the scheme marks each chosen item alike).'},
    {'scan': [[1, 13, 'any two'], [2, 7, 'any two'], [2, 17, 'any one']], 'kind': 'open-response',
     'reason': 'Part One Q12(iv) "any two examples of renewable energy", 5B "any two factors" and 17 "any one '
               'soil type" print no list, so they are open choices. Compulsory lists stay whole: 1A, 4A, 7A '
               'and 10A each bullet, 1B one sedimentary and one metamorphic rock, 15, 23 and 24 each printed item.'},
]

P1, P2 = 1, 2
LEFT = (0.0, 0.0, 0.5, 1.0)
RIGHT = (0.5, 0.0, 1.0, 1.0)
ID = 'geography-2025-hl-deferred-'
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



# The deferred scheme's own note (p2): a part it prints no allocation for is carded with this one row.
UNPRINTED = 'The scheme prints no answer for this part.'
NOTE_SLICE = (S(2, 'this means that the level of detail may vary by question', 'In the case of marking schemes'),)


def unprinted(marks):
    return (Criterion(UNPRINTED, marks, upto(marks), 'srp',
                      ('this means that the level of detail may vary by question',
                       'have been finalised for the questions attempted', '=examinations.')),)


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
ENERGY = (H + 'economic-energy',)

Q1S = (L(3, 'Examine the map above showing the bedrock geology of Ireland', 'following questions.'),)
Q1_ROWS = (L(3, 'Sandstone'), L(3, 'Quartzite'), L(3, 'Granite'), L(3, 'Basalt'))
Q2S = (L(4, 'Examine the diagram above and answer each of the following questions.'),)
Q2TF = L(4, '(ii) Examine the diagram above and indicate whether each of the following statements', 'correct box.')
Q3S = (L(5, 'Examine the photographs above and answer each of the following questions.'),)
Q3_ROWS = (L(5, 'U-shaped valley'), L(5, 'Cirque/Tarn/Corrie'), L(5, 'Drumlin'), L(5, 'Pyramidal peak'))
Q4S = (L(6, 'Examine the 1:50 000 Ordnance Survey map extract above', 'questions.'),)
Q4_ROWS = (L(6, 'Tombolo'), L(6, 'Wave cut platform'), L(6, 'Headland'), L(6, 'Beach'))
Q5TF = L(7, '(ii) Indicate whether each of the following statements is true or false', 'correct box.')
PART_ONE = [
    T('p1-1-i', P1, '1', '(i)', 4, 3, L(3, 'Rocks'),
      (L(3, '(i) Match each of the locations on the map A, B, C and D with the name of the rock', 'table below.'),),
      (S(4, 'Q1 (i) D 1m', None, clip(55, 108, 150, 165)),), rows(['Q1 (i) D 1m', 'A 1m', 'C 1m', 'B 1m']),
      '0-1', RW, ID + 'p1-q1', ('page',), Q1S, row_labels=Q1_ROWS),
    T('p1-1-ii', P1, '1', '(ii)', 4, 3, L(3, 'Rocks'),
      (L(3, '(ii) Indicate, by ticking (✓) the correct box, to which category each of the rocks belong.'),),
      (S(4, '(ii) Sedimentary 1m', None, clip(155, 108, 290, 165)),),
      rows(['(ii) Sedimentary 1m', 'Metamorphic 1m', '=Igneous 1m@0', '=Igneous 1m@1']),
      '0-1', RW, ID + 'p1-q1-ii', ('page',), Q1S, row_labels=Q1_ROWS),
    T('p1-2-i', P1, '2', '(i)', 4, 4, L(4, 'Plate Tectonics'),
      (L(4, '(i) Match each of the letters A, B, C and D with the term', 'below.'),),
      (S(4, 'Q2 (i) B 1m', None, clip(55, 187, 150, 245)),), rows(['Q2 (i) B 1m', 'C 1m', 'A 1m', 'D 1m']),
      '0-0', PS, ID + 'p1-q2', ('page',), Q2S,
      row_labels=(L(4, 'Continental crust'), L(4, 'Island arc'), L(4, 'Ocean ridge'), L(4, 'Subduction zone'))),
    T('p1-2-ii-a', P1, '2', '(ii)(a)', 2, 4, L(4, 'Plate Tectonics'),
      (Q2TF, L(4, '(a) The Mantle is located at X.')),
      (S(4, '(ii) False 2m', None, clip(155, 187, 290, 200)),), (fixed('Statement (a)', 2, '(ii) False 2m'),),
      '0-0', PS, ID + 'p1-q2-ii-a', ('page',), Q2S),
    T('p1-2-ii-b', P1, '2', '(ii)(b)', 2, 4, L(4, 'Plate Tectonics'),
      (Q2TF, L(4, '(b) There is a passive/transform plate boundary located at Y.')),
      (S(4, 'False 2m', None, clip(155, 200, 290, 215)),), (fixed('Statement (b)', 2, 'False 2m'),),
      '0-0', PS, ID + 'p1-q2-ii-b', ('page',), Q2S),
    T('p1-3-i', P1, '3', '(i)', 4, 5, L(5, 'Glaciation'),
      (L(5, '(i) Match each of the photographs A, B, C and D above with the feature', 'table below.'),),
      (S(4, '(i) D 1m', None, clip(55, 305, 150, 362)),), rows(['(i) D 1m', 'A 1m', 'B 1m', 'C 1m']),
      '0-11', GLAC, ID + 'p1-q3', ('page',), Q3S, row_labels=Q3_ROWS),
    T('p1-3-ii', P1, '3', '(ii)', 4, 5, L(5, 'Glaciation'),
      (L(5, '(ii) Indicate, by ticking (✓) the correct box, whether each feature listed', 'erosion or deposition.'),),
      (S(4, '(ii) Erosion 1m', None, clip(155, 305, 290, 362)),),
      rows(['(ii) Erosion 1m', '=Erosion 1m@0', '=Erosion 1m@1', '=Deposition 1m']),
      '0-11', GLAC, ID + 'p1-q3-ii', ('page',), Q3S, row_labels=Q3_ROWS),
    T('p1-4-i', P1, '4', '(i)', 4, 6, L(6, 'Physical Processes'),
      (L(6, '(i) Match each of the letters A, B, C and D with the feature', 'table below.'),),
      (S(4, 'A 1 mark', None, clip(55, 394, 170, 452)),), rows(['A 1 mark', 'C · 1 mark', 'D 1 mark', 'B 1 mark']),
      '0-10', SEA + MAP, ID + 'p1-q4', ('page',), Q4S, row_labels=Q4_ROWS),
    T('p1-4-ii', P1, '4', '(ii)', 4, 6, L(6, 'Physical Processes'),
      (L(6, '(ii) Indicate, by ticking (✓) the correct box, whether each of the features', 'erosion or deposition.'),),
      tuple(S(4, start, None, clip(175, y0, 290, y1)) for start, y0, y1 in (
          ('Deposition', 399, 405), ('Erosion', 414, 420), ('Erosion', 429, 435), ('Deposition', 444, 450))),
      rows(['=Deposition · 1 mark@0', '=Erosion · 1 mark@0', '=Erosion · 1 mark@1', '=Deposition · 1 mark@1']),
      '0-10', SEA, ID + 'p1-q4-ii', ('page',), Q4S, row_labels=Q4_ROWS),
    T('p1-5-i', P1, '5', '(i)', 6, 7, L(7, 'Concept of a Region'),
      (L(7, '(i) Complete the table below by matching each of the examples of regions', 'in the table.'),
       L(7, 'Examples of Regions:'), Lift(7, 'Munster Ridge and Valley', 'Sligo-Leitrim Constituency', row=True)),
      (S(4, '(i) Mediterranean', '(ii) True', clip(55, 500, 300, 620)),),
      rows(['(i) Mediterranean · 1m', 'Sambre Meuse 1m', 'Killarney 1m', 'Sligo-Leitrim Constituency 1m',
            'Basque Country 1m', 'Munster Ridge and Valley 1m']),
      '1-0', IRL + EURO, ID + 'p1-q5', ('page',),
      row_labels=(L(7, 'Climatic region'), L(7, 'Industrial decline region'), L(7, 'Urban region'),
                  L(7, 'Administrative region in Ireland'), L(7, 'Cultural region', nth=0), L(7, 'Geomorphological region'))),
    T('p1-5-ii-a', P1, '5', '(ii)(a)', 1, 7, L(7, 'Concept of a Region'),
      (Q5TF, L(7, '(a) Core regions experience net immigration.')),
      (S(4, '(ii) True 1m', None, clip(55, 590, 300, 604)),), (fixed('Statement (a)', 1, '(ii) True 1m'),),
      '1-1', IRL + EURO, ID + 'p1-q5-ii-a', ('page',)),
    T('p1-5-ii-b', P1, '5', '(ii)(b)', 1, 7, L(7, 'Concept of a Region'),
      (Q5TF, L(7, '(b) Cultural regions can be defined by religion.')),
      (S(4, 'True 1m', None, clip(55, 604, 300, 620)),), (fixed('Statement (b)', 1, 'True 1m'),),
      '1-3', IRL + EURO, ID + 'p1-q5-ii-b', ('page',)),
    T('p1-6', P1, '6', '', 8, 8, L(8, 'Landform Identification'),
      (L(8, 'In the table below, match each of the following landscape features', 'Confluence.'),),
      (S(4, '(i) Steep slope', None, clip(55, 635, 300, 692)),),
      rows(['(i) Steep slope 2 marks', '(ii) Confluence · 2 marks', '(iii) River source 2 marks',
            '(iv) Gentle slope · 2 marks'], 2),
      '2-6', MAP, ID + 'p1-q6', ('map', 'legend'),
      (L(8, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper.', nth=0),),
      row_labels=(L(8, 'N 18 83'), L(8, 'N 15 77'), L(8, 'N 12 81'), L(8, 'N 17 82'))),
]

Q7_COL = clip(300, 120, 595, 180)
PART_ONE += romans(P1, '7', 8, L(8, 'Ordnance Survey Map'),
                   (L(8, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper and',
                      'following questions.'),),
                   ID + 'p1-q7', ('map', 'legend'), [
    ('(i)', 2, L(8, '(i) Give a six-figure grid reference for the trail head in Longford.'),
     S(4, '(i) N134 748', '(ii) Holy', Q7_COL), (fixed('Grid reference', 2, '(i) N134 748 2 marks'),), '2-6', MAP),
    ('(ii)', 2, L(8, '(ii) Name the antiquity at N 145 828.'),
     S(4, '(ii) Holy Well', '(iii) 6.5', Q7_COL), (fixed('Antiquity', 2, '(ii) Holy Well 2 marks'),), '2-6', MAP),
    ('(iii)', 2, L(8, '(iii) Measure the full length, in kilometres, of the train line shown on the map.'),
     S(4, '(iii) 6.5', '(iv) 16', Q7_COL), (fixed('Length', 2, '(iii) 6.5 (km) 2 marks'),), '2-6', MAP),
    ('(iv)', 2, L(8, '(iv) Calculate the area (km2) south of the N4 national primary road.'),
     S(4, '(iv) 16', None, Q7_COL), (fixed('Area', 2, '(iv) 16 Km2 2 marks'),), '2-6', MAP),
])

Q8_COL = clip(300, 200, 595, 288)
Q8TF = L(9, '(ii) Indicate whether each of the following statements is true or false', 'correct box.')
PART_ONE += [
    T('p1-8-i', P1, '8', '(i)', 4, 9, L(9, 'Fluvial Landscape'),
      (L(9, '(i) Match each of the letters A, B, C and D with the feature', 'table below.'),),
      (S(4, '(i) D 1 marks', '(ii) False', Q8_COL),), rows(['(i) D 1 marks', 'C 1 marks', 'A 1 marks', 'B 1 marks']),
      '0-9', RIVERS, ID + 'p1-q8', ('page',),
      (L(9, 'Examine the photographs above and answer each of the following questions.'),),
      row_labels=(L(9, 'Delta'), L(9, 'Interlocking spurs'), L(9, 'Waterfall'), L(9, 'Meander'))),
    T('p1-8-ii-a', P1, '8', '(ii)(a)', 2, 9, L(9, 'Fluvial Landscape'),
      (Q8TF, L(9, '(a) Vertical erosion is most common in the mature stage of a river.')),
      (S(4, '(ii) False 2 marks', 'True 2 marks', Q8_COL),), (fixed('Statement (a)', 2, '(ii) False 2 marks'),),
      '0-9', RIVERS, ID + 'p1-q8-ii-a', ('page',),
      (L(9, 'Examine the photographs above and answer each of the following questions.'),)),
    T('p1-8-ii-b', P1, '8', '(ii)(b)', 2, 9, L(9, 'Fluvial Landscape'),
      (Q8TF, L(9, '(b) Deranged is a type of fluvial drainage pattern.')),
      (S(4, 'True 2 marks', None, Q8_COL),), (fixed('Statement (b)', 2, 'True 2 marks'),),
      '0-9', RIVERS, ID + 'p1-q8-ii-b', ('page',),
      (L(9, 'Examine the photographs above and answer each of the following questions.'),)),
    T('p1-9', P1, '9', '', 8, 10, L(10, 'Aerial Photograph', nth=0),
      (L(10, 'Using accepted notation, give the location on the aerial photograph', 'in the table below.'),),
      (S(4, 'A – Left Middleground', None, clip(300, 305, 595, 362)),),
      (fixed('A', 2, 'A – Left Middleground 2 marks'), fixed('B', 2, 'B – Right Background · 2 marks'),
       fixed('C', 2, 'C – Centre Middleground 2 marks'), fixed('D', 2, 'D – Centre Foreground 2 marks')),
      '2-8', AER, ID + 'p1-q9', ('page', 'aerial'),
      (L(10, 'Examine the aerial photograph of Longford accompanying this paper and the Google Street',
         'same area of Longford.'),)),
]

Q10_COL = clip(300, 394, 595, 452)
Q10TF = L(11, '(iii) Indicate whether the following statements are true or false', 'correct box.')
Q10S = (L(11, 'Examine the weather chart above and answer each of the following questions.'),)
PART_ONE += [
    T('p1-10-i', P1, '10', '(i)', 2, 11, L(11, 'Weather'),
      (L(11, '(i) What is the name of the weather system found at the area marked A', 'above?'),),
      (S(4, '(i) Anticyclone', '(ii) 1008', Q10_COL),), (fixed('Weather system', 2, '(i) Anticyclone/High pressure 2 marks'),),
      '2-7', WX, ID + 'p1-q10', ('page',), Q10S),
    T('p1-10-ii', P1, '10', '(ii)', 2, 11, L(11, 'Weather'),
      (L(11, '(ii) What is the barometric pressure (in hectopascals/millibars) on the line marked B', 'above?'),),
      (S(4, '(ii) 1008', '(iii) True', Q10_COL),), (fixed('Pressure', 2, '(ii) 1008 (mb/hPa) 2 marks'),),
      '2-7', WX, ID + 'p1-q10-ii', ('page',), Q10S),
    T('p1-10-iii-a', P1, '10', '(iii)(a)', 2, 11, L(11, 'Weather'),
      (Q10TF, L(11, '(a) Strong winds were experienced at the area marked C on the chart above.')),
      (S(4, '(iii) True', '(iv) True', Q10_COL),), (fixed('Statement (a)', 2, '(iii) True 2 marks'),),
      '2-7', WX, ID + 'p1-q10-iii-a', ('page',), Q10S),
    T('p1-10-iii-b', P1, '10', '(iii)(b)', 2, 11, L(11, 'Weather'),
      (Q10TF, L(11, '(b) A warm front is moving towards D on the chart above.')),
      (S(4, '(iv) True', None, Q10_COL),), (fixed('Statement (b)', 2, '(iv) True 2 marks'),),
      '2-7', WX, ID + 'p1-q10-iii-b', ('page',), Q10S),
]

Q11_COL = clip(300, 503, 595, 560)
PART_ONE += romans(P1, '11', 12, L(12, 'Statistical Interpretation'),
                   (L(12, 'Examine the table above which shows the mean temperature and long-term average',
                      'following questions.'),),
                   ID + 'p1-q11', ('page',), [
    ('(i)', 2, L(12, '(i) Which month was the warmest in 2023?'),
     S(4, '(i) June', '(ii) January', Q11_COL), (fixed('Month', 2, '(i) June 2 marks'),), '2-0', TG),
    ('(ii)', 2, L(12, '(ii) Which month had the coldest long-term average temperature?'),
     S(4, '(ii) January', '(iii) 12.8', Q11_COL), (fixed('Month', 2, '(ii) January 2 marks'),), '2-0', TG),
    ('(iii)', 2, L(12, '(iii) Calculate the temperature range for 2022.'),
     S(4, '(iii) 12.8', '(iv) 14.3', Q11_COL), (fixed('Range', 2, '(iii) 12.8 2 marks'),), '2-0', TG),
    ('(iv)', 2, L(12, '(iv) Calculate the average temperature (oC) for May, June, July and August in 2022.'),
     S(4, '(iv) 14.3', None, Q11_COL), (fixed('Average', 2, '(iv) 14.3 2 marks'),), '2-0', TG + WX),
])

Q12_COL = clip(300, 635, 595, 692)
PART_ONE += romans(P1, '12', 13, L(13, 'Graphical Interpretation'),
                   (L(13, 'Examine the infographic above which shows environmental indicators for Ireland',
                      'following questions.'),),
                   ID + 'p1-q12', ('page',), [
    ('(i)', 2, L(13, '(i) What was Ireland’s CO2 equivalent (tonnes) per capita in 2020?'),
     S(4, '(i) 11.6', '(ii) 67', Q12_COL), (fixed('CO2 per capita', 2, '(i) 11.6 (tonnes) 2 marks'),), '2-0', TG),
    ('(ii)', 2, L(13, '(ii) Calculate the percentage (%) of metered electricity', 'households in 2021.'),
     S(4, '(ii) 67', '(iii) 42', Q12_COL), (fixed('Percentage', 2, '(ii) 67(%) 2 marks'),), '2-0', TG),
    ('(iii)', 2, L(13, '(iii) What percentage (%) of electricity was generated from renewable sources in 2020?'),
     S(4, '(iii) 42', '(iv) Valid', Q12_COL), (fixed('Percentage', 2, '(iii) 42(%) 2 marks'),), '2-0', TG),
    ('(iv)', 2, L(13, '(iv) Name any two examples of renewable energy.'),
     S(4, '(iv) Valid renewables', None, Q12_COL),
     (fixed('Two examples', 2, '(iv) Valid renewables · 1+1 marks', (0, 1, 2)),), '3-5', ENERGY),
])

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
TECTONIC = ('Volcanoes', 'Earthquakes', 'Fold Mountains.')
ROCK_CYCLE = ('Mining', 'Extraction of building materials', 'Oil/gas exploitation',
              'Geothermal energy production.')
DEVELOPED = ('Footloose industries', 'Financial services', 'Mass tourism.')
MIGRATION = ('Migration policy in the European Union', 'Rural to urban migration in the developing world.')

PART_TWO = [
    T('p2-1a', P2, '1A', '', 20, 3, L(3, 'Ordnance Survey Map'),
      (L(3, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper.', 'land above 200m.'),),
      (S(6, 'Sketch Outline', None),),
      sketch('Sketch Outline · 4 marks (4/0)', (0, 4), ('4 features @ 4 marks each', 'Label 1 mark'),
             sums((0, 1, 3), (0, 1)), 4),
      '2-6', MAP, ID + 'p2-q1a', ('map', 'legend'),
      row_labels=(None, L(3, 'The entire built-up area of Longford town'), L(3, 'The entire length of the R198 regional road'),
                  L(3, 'An area of deciduous woodland east of Easting 16'), L(3, 'An area of land above 200m.'))),
    T('p2-1b', P2, '1B', '', 30, 3, L(3, 'Rocks'),
      (L(3, 'Examine the formation of each of the following', 'One metamorphic rock.'),),
      (S(7, 'Named sedimentary rock · 2 marks', 'Annotation'),),
      (fixed('Named sedimentary rock', 2, 'Named sedimentary rock · 2 marks'),
       fixed('Named metamorphic rock', 2, 'Named metamorphic rock · 2 marks'),
       split('Examination of the two rocks (7/6 and 6/7 SRPs)', 13,
             f'Examination of rock 1 · 7/6 {SRPS}', f'Examination of rock 2 · 6/7 {SRPS}')),
      '0-1', RW, ID + 'p2-q1b'),
    T('p2-1c', P2, '1C', '', 30, 3, L(3, 'The Tectonic Cycle'),
      (L(3, 'Explain how the tectonic cycle helps to explain the global distribution', 'Fold Mountains.'),),
      (S(8, 'Reference to geographical distribution · 2 marks', 'Annotation'),),
      (fixed('Reference to geographical distribution', 2, 'Reference to geographical distribution · 2 marks'),
       fixed('Impact of tectonic cycle', 2, 'Impact of tectonic cycle · 2 marks'),
       srp('Examination', 13, f'Examination · 13 {SRPS}')),
      '0-0', PS, first_route('p2-q1c-', TECTONIC[0]),
      routes=bullet_routes('p2-q1c-', TECTONIC, atlas=dict(zip(TECTONIC, (PS + EV, PS + EV, PS + RW))))),
]

PART_TWO += romans(P2, '2A', 4, L(4, 'Structure of the Earth'),
                   (L(4, 'Examine the diagram above and answer each of the following questions.'),),
                   ID + 'p2-q2a', ('page',), [
    ('(i)', 8, L(4, '(i) Name each of the Earth’s layers labelled A, B, C, and D.'),
     S(9, '(i) · A = Inner Core', '(ii) · Eurasian'),
     (fixed('A', 2, '(i) · A = Inner Core · 2 marks'), fixed('B', 2, 'B = Outer Core · 2 marks'),
      fixed('C', 2, 'C = Mantle · 2 marks'), fixed('D', 2, 'D = Crust/Lithosphere · 2 marks')), '0-0', PS),
    ('(ii)', 2, L(4, '(ii) Name the tectonic plate that Ireland sits on.'),
     S(9, '(ii) · Eurasian', '(iii) · True'), (fixed('Tectonic plate', 2, '(ii) · Eurasian · 2 marks'),), '0-0', PS),
    ('(iii)', 2, (L(4, '(iii) In your answerbook, state whether the following statement is true or false:'),
                  L(4, 'The asthenosphere is the semi-molten part of the upper mantle.')),
     S(9, '(iii) · True · 2', '(iv) · Valid'), (fixed('True or false', 2, '(iii) · True · 2'),), '0-0', PS),
    ('(iv)', 4, L(4, '(iv) Explain briefly what is meant by the term seafloor spreading.'),
     S(9, '(iv) · Valid explanation', '(v) · Valid'), (pair('(iv) · Valid explanation · 2 + 2 marks', 'Explanation'),),
     '0-0', PS),
    ('(v)', 4, L(4, '(v) Explain briefly what is meant by the term lava.'),
     S(9, '(v) · Valid explanation', None), (pair('(v) · Valid explanation · 2 + 2 marks', 'Explanation'),),
     '0-7', EV),
])

PART_TWO += [
    T('p2-2b', P2, '2B', '', 30, 4, L(4, 'Surface Processes'),
      (L(4, '(i) Examine the role of the process of deposition', 'that you have studied.'),),
      (S(10, 'Process of deposition identified · 2 marks', 'Annotation'),),
      (fixed('Process of deposition identified', 2, 'Process of deposition identified · 2 marks'),
       fixed('Landform named', 2, 'Landform named · 2 marks'), srp('Examination', 13, f'Examination · 13 x {SRPS}')),
      '0-9', RIVERS, ID + 'p2-q2b-route-i-fluvial-landform',
      routes=(
          Route('route-i-fluvial-landform', 'Route (i) · one fluvial landform',
                ID + 'p2-q2b-route-i-fluvial-landform', False, ((LANDFORMS, 'one fluvial landform'),),
                topic='0-9', atlas=RIVERS),
          Route('route-i-coastal-landform', 'Route (i) · one coastal landform',
                ID + 'p2-q2b-route-i-coastal-landform', False, ((LANDFORMS, 'one coastal landform'),),
                topic='0-10', atlas=SEA),
          Route('route-i-glacial-landform', 'Route (i) · one glacial landform',
                ID + 'p2-q2b-route-i-glacial-landform', False, ((LANDFORMS, 'one glacial landform'),),
                topic='0-11', atlas=GLAC),
          Route('route-ii', 'Route (ii)', ID + 'p2-q2b-route-ii', False,
                prompt=(L(4, '(ii) Describe and explain the factors governing', 'that you have studied.'),),
                scheme=(S(11, 'Factors identified', 'Annotation'),),
                criteria=(pair('Factors identified · 2 + 2 marks', 'Factors identified'),
                          fixed('Mass movement process named', 2, 'Mass movement process named · 2 marks'),
                          srp('Description/explanation', 12, f'Description/explanation · 12 {SRPS}')),
                topic='0-8', atlas=RW),
      )),
    T('p2-2c', P2, '2C', '', 30, 4, L(4, 'Landscape Development'),
      (L(4, 'Examine how different rock types produce distinctive landscapes in Ireland', 'that you have studied.'),),
      (S(12, 'Rock 1 and associated landscape named', 'Annotation'),),
      (pair('Rock 1 and associated landscape named · 2 + 2 marks', 'Rock 1 and its landscape'),
       pair('Rock 2 and associated landscape named · 2 + 2 marks', 'Rock 2 and its landscape'),
       srp('Examination', 11, f'Examination · 11 x {SRPS}')),
      '0-1', RW, ID + 'p2-q2c'),
]

PART_TWO += romans(P2, '3A', 5, L(5, 'Earthquakes'),
                   (L(5, 'Examine the article above which gives information on the Valdivia earthquake',
                      'following questions.'),),
                   ID + 'p2-q3a', ('page',), [
    ('(i)', 2, L(5, '(i) What was the greatest magnitude of seismic waves recorded from this earthquake?'),
     S(13, '(i) · 9.5', '(ii) · 15 hours'), (fixed('Magnitude', 2, '(i) · 9.5 · 2 marks'),), '0-7', EV),
    ('(ii)', 2, L(5, '(ii) How long did it take the tsunami wave to reach Crescent City?'),
     S(13, '(ii) · 15 hours', '(iii) · Impacts'), (fixed('Time', 2, '(ii) · 15 hours · 2 marks'),), '0-7', EV),
    ('(iii)', 4, L(5, '(iii) State two negative impacts of the earthquake referred to in the text above.'),
     S(13, '(iii) · Impacts stated', '(iv) · Valid'), (pair('(iii) · Impacts stated · 2 + 2 marks', 'Two impacts'),),
     '0-7', EV),
    ('(iv)', 4, L(5, '(iv) Explain briefly one way that earthquakes can be predicted.'),
     S(13, '(iv) · Valid explanation', '(v) · Valid'), (pair('(iv) · Valid explanation · 2 + 2 marks', 'Explanation'),),
     '0-7', EV),
    ('(v)', 4, L(5, '(v) Explain briefly the term epicentre.'),
     S(13, '(v) · Valid explanation', '(vi) · Valid'), (pair('(v) · Valid explanation · 2 + 2 marks', 'Explanation'),),
     '0-7', EV),
    ('(vi)', 4, L(5, '(vi) Explain briefly one way to reduce the effects of an earthquake.'),
     S(13, '(vi) · Valid explanation', None), (pair('(vi) · Valid explanation · 2 + 2 marks', 'Explanation'),),
     '0-7', EV),
])

PART_TWO += [
    T('p2-3b', P2, '3B', '', 30, 5, L(5, 'Human Interaction with the Rock Cycle'),
      (L(5, 'Examine how humans interact with the rock cycle', 'Geothermal energy production.'),),
      (S(14, f'Examination · 15 x {SRPS}', 'Annotation'),), (srp('Examination', 15, f'Examination · 15 x {SRPS}'),),
      '0-6', RW, first_route('p2-q3b-', ROCK_CYCLE[0]), routes=bullet_routes('p2-q3b-', ROCK_CYCLE)),
    T('p2-3c', P2, '3C', '', 30, 5, L(5, 'Isostasy'),
      (L(5, 'Examine how isostasy has impacted on the Irish landscape', 'coastal landscape.'),),
      (S(15, 'Impact / feature identified · 2 marks', 'Annotation'),),
      (fixed('Impact / feature identified', 2, 'Impact / feature identified · 2 marks'),
       srp('Examination', 14, 'Examination · 14 x SRPs')),
      '0-5', RIVERS + SEA, ID + 'p2-q3c'),
    # Question 4
    T('p2-4a', P2, '4A', '', 20, 6, L(6, 'Map Skills'),
      (L(6, 'Draw an outline map of Ireland.', 'One named river in the region.'),),
      (S(16, 'Map outline', None),),
      sketch('Map outline · 4 marks graded (4/2/0)', (0, 2, 4),
             ('4 features @ 4 marks each', 'Named 2 marks'), sums((0, 1, 2), (0, 2)), 4),
      '1-4', IRL, ID + 'p2-q4a',
      row_labels=(None, L(6, 'The outline of one named region'),
                  L(6, 'The outline of a named feature of relief (upland or lowland) in the region'),
                  L(6, 'One named urban centre in the region'), L(6, 'One named river in the region.'))),
    T('p2-4b', P2, '4B', '', 30, 6, L(6, 'Secondary Economic Activity'),
      (L(6, 'Examine the development of secondary economic activity in a European region', 'Government policy.'),),
      (S(17, 'Examination of Factor 1', 'Annotation'),),
      (split('Examination of the two factors (8/7 and 7/8 SRPs)', 15,
             f'Examination of Factor 1 · 8/7 x {SRPS}', f'Examination of Factor 2 · 7/8 x {SRPS}'),),
      '1-5', EURO, ID + 'p2-q4b'),
    T('p2-4c', P2, '4C', '', 30, 6, L(6, 'Industrial Decline'),
      (L(6, 'Examine the causes and impacts of industrial decline', 'you have studied.'),),
      (S(18, 'Cause identified · 2 marks', 'Annotation'),),
      (fixed('Cause identified', 2, 'Cause identified · 2 marks'), fixed('Impact identified', 2, 'Impact identified · 2 marks'),
       srp('Examination', 13, 'Examination · 13 x SRPs')),
      '1-1', IRL + EURO, ID + 'p2-q4c'),
]

# The scheme numbers 5A(iv) "(v)" and 5A(v) "(vi)".
PART_TWO += romans(P2, '5A', 7, L(7, 'Levels of Educational Attainment'),
                   (L(7, 'Examine the chart above showing the levels of educational attainment', 'following questions.'),),
                   ID + 'p2-q5a', ('page',), [
    ('(i)', 2, L(7, '(i) Name the country with the lowest level of high attainment.'),
     S(19, '(i) · Germany', '(ii) · 23%'), (fixed('Country', 2, '(i) · Germany · 2 marks'),), '2-0', TG),
    ('(ii)', 2, L(7, '(ii) What percentage (%) of the population in Spain had a medium level of attainment?'),
     S(19, '(ii) · 23%', '(iii) · 18%'), (fixed('Percentage', 2, '(ii) · 23% · 2 marks'),), '2-0', TG),
    ('(iii)', 4, L(7, '(iii) Calculate X, the percentage (%) of the EU average', 'attainment.'),
     S(19, '(iii) · 18%', '(v) · Valid'), (fixed('Calculation', 4, '(iii) · 18% · 4 marks'),), '2-0', TG),
    ('(iv)', 4, L(7, '(iv) Explain briefly how the level of educational attainment could be improved', 'countries.'),
     S(19, '(v) · Valid explanation', '(vi) · Valid'), (pair('(v) · Valid explanation · 2 + 2 marks', 'Explanation'),),
     '1-5', EURO),
    ('(v)', 8, L(7, '(v) Explain briefly two challenges faced by countries with a low level', 'attainment.'),
     S(19, '(vi) · Valid explanation', None),
     (pair('(vi) · Valid explanation · 2 + 2 marks', 'Challenge 1'), pair('=Valid explanation · 2 + 2 marks', 'Challenge 2')),
     '1-5', EURO),
])

PART_TWO += [
    T('p2-5b', P2, '5B', '', 30, 7, L(7, 'Primary Economic Activity'),
      (L(7, 'Explain any two factors that have influenced the development of one primary economic',
         'that you have studied.'),),
      (S(20, f'Examination · 15 x {SRPS}', 'Annotation'),), (srp('Examination', 15, f'Examination · 15 x {SRPS}'),),
      '1-4', IRL, ID + 'p2-q5b'),
    T('p2-5c', P2, '5C', '', 30, 7, L(7, 'Urban Development'),
      (L(7, 'Discuss the factors which influenced the development of one urban area', 'that you have studied.'),),
      (S(21, 'Urban area named · 2 marks', 'Annotation'),),
      (fixed('Urban area named', 2, 'Urban area named · 2 marks'), pair('Factors identified · 2 + 2marks', 'Factors identified'),
       srp('Discussion', 12, f'Discussion · 12 x {SRPS}')),
      '1-3', EURO, ID + 'p2-q5c'),
]

PART_TWO += romans(P2, '6A', 8, L(8, 'Population Statistics in Ireland'),
                   (L(8, 'Examine the data above showing the population statistics for Irish administrative regions',
                      'following questions.'),),
                   ID + 'p2-q6a', ('page',), [
    ('(i)', 2, L(8, '(i) Name the region with the lowest percentage of population.'),
     S(22, '(i) · Midland', '(ii) · Dublin'), (fixed('Region', 2, '(i) · Midland · 2 marks'),), '2-0', TG),
    ('(ii)', 4, L(8, '(ii) Name the region with the highest percentage of population', 'percentage (%).'),
     S(22, '(ii) · Dublin', '(iii) · 14%'), (pair('(ii) · Dublin, 28% · 2 + 2 marks', 'Region and percentage'),),
     '2-0', TG),
    ('(iii)', 4, L(8, '(iii) Calculate X, the percentage (%) of population for the South-West region.'),
     S(22, '(iii) · 14%', '(iv) · Valid'), (fixed('Calculation', 4, '(iii) · 14% · 4 marks'),), '2-0', TG),
    ('(iv)', 2, L(8, '(iv) Name one peripheral region in Ireland.'),
     S(22, '(iv) · Valid peripheral region', '(v) · Valid'), (fixed('Region', 2, '(iv) · Valid peripheral region named · 2 marks'),),
     '1-4', IRL),
    ('(v)', 4, L(8, '(v) Explain briefly one effect of low population in peripheral regions.'),
     S(22, '(v) · Valid explanation', '(vi) · Valid'), (pair('(v) · Valid explanation · 2 + 2 marks', 'Effect'),),
     '1-1', IRL),
    ('(vi)', 4, L(8, '(vi) Explain briefly why core regions have high populations.'),
     S(22, '(vi) · Valid explanation', None), (pair('(vi) · Valid explanation · 2 + 2 marks', 'Explanation'),),
     '1-1', IRL),
])

PART_TWO += [
    T('p2-6b', P2, '6B', '', 30, 8, L(8, 'Tertiary Economic Activity – Continental / Sub-Continental Region'),
      (L(8, 'Account for the development of one tertiary economic activity in a', 'that you have studied.'),),
      (S(23, f'Examination · 15 x {SRPS}', 'Annotation'),), (srp('Examination', 15, f'Examination · 15 x {SRPS}'),),
      '1-6', CONT, ID + 'p2-q6b'),
    T('p2-6c', P2, '6C', '', 30, 8, L(8, 'European Union', nth=0),
      (L(8, 'Discuss the potential challenges facing the future development of the European Union', 'sovereignty.'),),
      (S(24, 'Challenge named · 2 marks', 'Annotation'),),
      (fixed('Challenge named', 2, 'Challenge named · 2 marks'), srp('Explanation', 14, f'Explanation · 14 x {SRPS}')),
      '1-5', EURO, ID + 'p2-q6c'),
    # Question 7: the deferred scheme prints no allocation for any of its parts.
    T('p2-7a', P2, '7A', '', 20, 10, L(10, 'Aerial Photograph'),
      (L(10, 'Examine the aerial photograph of Longford accompanying this paper.', 'in the foreground.'),),
      NOTE_SLICE, unprinted(20), '2-8', AER, ID + 'p2-q7a', ('aerial',)),
    T('p2-7b', P2, '7B', '', 30, 10, L(10, 'Economic Development – Developed Economy'),
      (L(10, 'Examine the development of one of the following with reference to a developed economy', 'Mass tourism.'),),
      NOTE_SLICE, unprinted(30), '3-0', ECON, first_route('p2-q7b-', DEVELOPED[0]),
      routes=bullet_routes('p2-q7b-', DEVELOPED)),
    T('p2-7c', P2, '7C', '', 30, 10, L(10, 'Multinational Company'),
      (L(10, 'Examine how globalisation impacts on world trade', 'that you have studied.'),),
      NOTE_SLICE, unprinted(30), '3-2', MNC, ID + 'p2-q7c'),
]

PART_TWO += romans(P2, '8A', 11, L(11, 'Energy Imports', nth=0),
                   (L(11, 'Study the table above showing information on dependency on energy imports', 'following questions.'),),
                   ID + 'p2-q8a', ('page',), [
    ('(i)', 4, L(11, '(i) Name two countries that had a lower energy import dependency', 'each of the years shown.'),
     S(29, '(i) · Any two', '(ii) · Netherlands'), (pair('(i) · Any two: Poland/Estonia/Sweden 2 + 2 marks', 'Two countries'),),
     '2-0', TG),
    ('(ii)', 6, L(11, '(ii) Name the country with the largest increase in energy imports', 'percentage (%).'),
     S(29, '(ii) · Netherlands', '(iii) · Named'), (fixed('Country and increase', 6, '(ii) · Netherlands, 12% · 2 + 4 marks', (0, 2, 4, 6)),),
     '2-0', TG),
    ('(iii)', 2, L(11, '(iii) Name one source of fossil fuel.'),
     S(29, '(iii) · Named fossil fuel', '(iv) · Valid'), (fixed('Fossil fuel', 2, '(iii) · Named fossil fuel 2 marks'),),
     '3-5', ENERGY),
    ('(iv)', 8, L(11, '(iv) Explain briefly two challenges associated with a high dependency on energy imports.'),
     S(29, '(iv) · Valid explanation of challenges', None),
     (pair('(iv) · Valid explanation of challenges 2 + 2 marks', 'Challenge 1'), pair('=2 + 2 marks', 'Challenge 2')),
     '3-5', ENERGY),
])

REASON = ('3 x reasons @ 10 marks each.', 'For each reason:', 'Reason stated · 2 marks', 'Map evidence · 2 marks',
          f'Explanation · 3 x {SRPS}')
PART_TWO += [
    T('p2-8b-i', P2, '8B', '(i)', 20, 11, L(11, 'Location of Economic Activity'),
      (L(11, '(i) Explain two reasons why a multinational company might choose to locate', 'reason.'),),
      (S(30, '3 x reasons @ 10 marks each.', 'Annotation'),),
      (Criterion('Reason to locate 1', 10, evens(10), 'srp', REASON),
       Criterion('Reason to locate 2', 10, evens(10), 'srp', REASON)),
      '2-6', MAP + ECON, ID + 'p2-q8b', ('map', 'legend'),
      (L(11, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper and', 'following questions.'),)),
    T('p2-8b-ii', P2, '8B', '(ii)', 10, 11, L(11, 'Location of Economic Activity'),
      (L(11, '(ii) Using evidence from the Ordnance Survey map, explain one reason', 'this area.'),),
      (S(30, '3 x reasons @ 10 marks each.', 'Annotation'),),
      (Criterion('Reason not to locate', 10, evens(10), 'srp', REASON),),
      '2-6', MAP + ECON, ID + 'p2-q8b-ii', ('map', 'legend'),
      (L(11, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper and', 'following questions.'),)),
    T('p2-8c', P2, '8C', '', 30, 11, L(11, 'Globalisation'),
      (L(11, 'Explain the impact of globalisation on one developing economy that you have studied.'),),
      (S(31, 'Named Developing Economy · 2 marks', 'Annotation'),),
      (fixed('Named developing economy', 2, 'Named Developing Economy · 2 marks'),
       pair('Impacts identified · 2 + 2 marks', 'Impacts identified'), srp('Explanation', 12, 'Explanation · 12 x SRPs')),
      '3-1', DEV + MNC, ID + 'p2-q8c'),
]

PART_TWO += romans(P2, '9A', 12, L(12, 'Renewable Energy Sources'),
                   (L(12, 'Examine the data above showing the share of renewable energy sources', 'following questions.'),),
                   ID + 'p2-q9a', ('page',), [
    ('(i)', 16, L(12, '(i) Using graph paper, draw a suitable graph to illustrate this data.'),
     S(32, 'Bar Chart · Pie Chart', 'Annotation'), GRAPH, '2-0', TG),
    ('(ii)', 4, L(12, '(ii) Explain briefly one economic advantage of renewable sources of energy.'),
     S(32, 'Valid explanation · 2 + 2 marks', None), (pair('Valid explanation · 2 + 2 marks', 'Advantage'),),
     '3-5', ENERGY),
])

PART_TWO += [
    T('p2-9b', P2, '9B', '', 30, 12, L(12, 'European Union - Trade'),
      (L(12, 'Describe the current trading patterns of the European Union', 'these trading patterns.'),),
      (S(33, 'Internal trading pattern identified · 2 marks', 'Annotation'),),
      (fixed('Internal trading pattern identified', 2, 'Internal trading pattern identified · 2 marks'),
       fixed('External trading pattern identified', 2, 'External trading pattern identified · 2 marks'),
       pair('Factors influencing trading patterns identified · 2 + 2 marks', 'Factors identified'),
       srp('Description/explanation', 11, f'Description/explanation · 11 x {SRPS}')),
      '3-3', EU, ID + 'p2-q9b'),
    T('p2-9c', P2, '9C', '', 30, 12, L(12, 'Conflict of Interest'),
      (L(12, 'Examine how conflict may arise between the exploitation of natural resources', 'that you have studied.'),),
      (S(34, 'Example named · 2m', 'Annotation'),),
      (fixed('Example named', 2, 'Example named · 2m'), srp('Examination', 14, f'Examination · 14 x {SRPS}')),
      '3-4', ENV, ID + 'p2-q9c'),
    # Question 10
    T('p2-10a', P2, '10A', '', 20, 13, L(13, 'Aerial Photograph'),
      (L(13, 'Examine the aerial photograph of Longford accompanying this paper.', 'in the right foreground.'),),
      (S(35, 'Sketch Outline', None),),
      sketch('Sketch Outline · 4 marks (4/0)', (0, 4), ('4 features @ 4 marks each', 'Named 1 mark'),
             sums((0, 1, 3), (0, 1)), 4),
      '2-8', AER + URB, ID + 'p2-q10a', ('aerial',),
      row_labels=(None, L(13, 'A church'), L(13, 'A carpark in the foreground'), L(13, 'A bridge'),
                  L(13, 'A sports field in the right foreground.'))),
    T('p2-10b', P2, '10B', '', 30, 13, L(13, 'Population'),
      (L(13, 'Examine how changing fertility and mortality rates impact on population structure', 'have studied.'),),
      (S(36, 'Impact of changing fertility rates identified · 2 marks', 'Annotation'),),
      (fixed('Impact of changing fertility rates identified', 2, 'Impact of changing fertility rates identified · 2 marks'),
       fixed('Impact of changing mortality rates identified', 2, 'Impact of changing mortality rates identified · 2 marks'),
       fixed('Example', 2, 'Example · 2 marks'), srp('Examination', 12, f'Examination · 12 x {SRPS}')),
      '4-0', POP, ID + 'p2-q10b'),
    T('p2-10c', P2, '10C', '', 30, 13, L(13, 'Urban Issues'),
      (L(13, 'Discuss any two of the following issues that may arise', 'Environmental issues.'),),
      (S(37, 'Discussion of Issue 1', 'Annotation'),),
      (split('Discussion of the two issues (7/8 SRPs each)', 15,
             f'Discussion of Issue 1 · 7/8 x {SRPS}', f'Discussion of Issue 2 · 7/8 x {SRPS}'),),
      '4-5', URB, ID + 'p2-q10c'),
]

PART_TWO += romans(P2, '11A', 14, L(14, 'Traffic Congestion'),
                   (L(14, 'Examine the data above showing the hours lost to rush hour traffic', 'following questions.'),),
                   ID + 'p2-q11a', ('page',), [
    ('(i)', 2, L(14, '(i) How many hours on average did people lose in rush hour traffic in Dublin?'),
     S(38, '(i) · 158', '(ii) · Doha'), (fixed('Hours', 2, '(i) · 158 (hours) · 2 marks'),), '2-0', TG),
    ('(ii)', 2, L(14, '(ii) Which city lost the least amount of hours in rush hour traffic?'),
     S(38, '(ii) · Doha', '(iii) · 33'), (fixed('City', 2, '(ii) · Doha · 2 marks'),), '2-0', TG),
    ('(iii)', 4, L(14, '(iii) Calculate the difference in average vehicle speed', 'and London.'),
     S(38, '(iii) · 33', '(iv) · Valid'), (fixed('Difference', 4, '(iii) · 33 (km/hr) · 4 marks'),), '2-0', TG),
    ('(iv)', 4, L(14, '(iv) Explain briefly one environmental benefit of reduced traffic congestion.'),
     S(38, '(iv) · Valid explanation', '(v) · Valid'), (pair('(iv) · Valid explanation · 2 + 2 marks', 'Benefit'),),
     '4-5', URB),
    ('(v)', 8, L(14, '(v) Explain briefly two ways to reduce traffic congestion.'),
     S(38, '(v) · Valid explanations', None),
     (pair('(v) · Valid explanations · 2 + 2 marks', 'Way 1'), pair('=2 + 2 marks', 'Way 2')), '4-5', URB),
])

PATTERN = ('Three patterns @ 10 marks each', 'For each pattern:', 'Pattern named · 2 marks',
           'OS map evidence · 2 marks', f'Description/Explanation · 3 x {SRPS}')
PART_TWO += [
    T('p2-11b', P2, '11B', '', 30, 14, L(14, 'Population Characteristic – Ireland'),
      (L(14, 'Examine how the characteristics of Ireland’s population have changed since 1950.'),),
      (S(39, 'Change in pattern of migration to Ireland · 2 marks', 'Annotation'),),
      (fixed('Change in pattern of migration to Ireland', 2, 'Change in pattern of migration to Ireland · 2 marks'),
       fixed('Change in pattern of migration from Ireland', 2, 'Change in pattern of migration from Ireland · 2 marks'),
       srp('Description/explanation', 13, f'Description / Explanation · 13 x {SRPS}')),
      '4-0', POP, ID + 'p2-q11b'),
    T('p2-11c', P2, '11C', '', 30, 14, L(14, 'Rural Settlement Patterns'),
      (L(14, 'With reference to the 1:50 000 Ordnance Survey map accompanying this paper', 'evident on the map.'),),
      (S(40, 'Three patterns @ 10 marks each', 'Annotation'),),
      tuple(Criterion(f'Pattern {n}', 10, evens(10), 'srp', PATTERN) for n in (1, 2, 3)),
      '4-3', URB + MAP, ID + 'p2-q11c', ('map', 'legend')),
]

PART_TWO += romans(P2, '12A', 15, L(15, 'Population Dynamics'),
                   (L(15, 'Examine the data above showing the number of emigrants from Ireland', 'following questions.'),),
                   ID + 'p2-q12a', ('page',), [
    ('(i)', 16, L(15, '(i) Using graph paper, draw a suitable graph to illustrate this data.'),
     S(41, 'Bar Chart · Pie Chart', 'Annotation'), GRAPH, '2-0', TG),
    ('(ii)', 4, L(15, '(ii) Explain briefly one negative effect of emigration.'),
     S(41, 'Valid explanation · 2 + 2 marks', None), (pair('Valid explanation · 2 + 2 marks', 'Negative effect'),),
     '4-2', POP),
])

PART_TWO += [
    T('p2-12b', P2, '12B', '', 30, 15, L(15, 'Urban Land-Use'),
      (L(15, 'Examine how the location of two of the following land-uses has changed', 'Commercial land-use.'),),
      (S(42, 'Named Irish city · 2 marks', 'Annotation'),),
      (fixed('Named Irish city', 2, 'Named Irish city · 2 marks'),
       srp('Examination of land-use 1', 7, f'Examination of land-use 1 · 7 x {SRPS}'),
       srp('Examination of land-use 2', 7, f'Examination of land-use 2 · 7 x {SRPS}')),
      '4-4', LANDUSE + URB, ID + 'p2-q12b'),
    T('p2-12c', P2, '12C', '', 30, 15, L(15, 'Migration', nth=0),
      (L(15, 'Population movements have an impact on donor and receiver regions.', 'developing world.'),),
      (S(43, 'Impact on donor region identified · 2 marks', 'Annotation'),),
      (fixed('Impact on donor region identified', 2, 'Impact on donor region identified · 2 marks'),
       fixed('Impact on receiver region identified', 2, 'Impact on receiver region identified · 2 marks'),
       srp('Discussion', 13, f'Discussion · 13 x {SRPS}')),
      '4-2', POP, first_route('p2-q12c-', MIGRATION[0]), routes=bullet_routes('p2-q12c-', MIGRATION)),
]

# ------------------------------------------------------------------ Options --
OUTLINE = S(45, 'Number of aspects', 'Marking Descriptors')
OC = S(45, '*Overall Coherence (20 marks)', None, table=True)


def option(q, page, theme, note_nth, prompt, topic, atlas, scheme_page=None):
    """An option essay, marked on the scheme's own outline where it prints one, else on the outline it
    sets for Questions 13-24 (p45); the Overall Coherence descriptors are p45's."""
    scheme = (S(scheme_page, 'Number of aspects', None), OC) if scheme_page else (OUTLINE, OC)
    return T(f'p2-{q}', P2, q, '', 80, page, theme, (prompt,), scheme,
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
           L(17, 'Sustainability is a model for future development.', 'Self-reliance.'), '5-3', GI),
    option('14', 17, L(17, 'Global Interdependence'), 0,
           L(17, 'Examine how aid programmes can help and hinder development.'), '5-2', GI),
    option('15', 17, L(17, 'Global Interdependence'), 0,
           L(17, 'We live in an interdependent global economy.', 'Human rights issues.'), '5-1', GI),
    option('16', 17, L(17, 'Geoecology'), 1,
           L(17, 'Examine how the characteristics of one soil type you have studied can be impacted', 'Podzolisation.'),
           '6-1', GE),
    option('17', 17, L(17, 'Geoecology'), 1,
           L(17, 'Describe and explain the general composition and characteristics of any one soil type.'),
           '6-0', GE, scheme_page=51),
    option('18', 17, L(17, 'Geoecology'), 1,
           L(17, 'With reference to one biome that you have studied, account for the type of climate', 'within the biome.'),
           '6-2', GE, scheme_page=52),
    option('19', 18, L(18, 'Culture and Identity'), 0,
           L(18, 'Examine the strategies that have been or could be implemented', 'minority languages.'), '7-0', CI),
    option('20', 18, L(18, 'Culture and Identity'), 0,
           L(18, 'Examine how political and/or physical boundaries can have an effect on cultural groups.'), '7-1', CI),
    option('21', 18, L(18, 'Culture and Identity'), 0,
           L(18, 'Cultural identity is defined by many diverse factors.', 'you have'), '7-2', CI, scheme_page=55),
    option('22', 18, L(18, 'The Atmosphere – Ocean Environment'), 1,
           L(18, 'Give an account of how atmosphere-ocean phenomena', 'such measurements.'), '8-0', AO),
    option('23', 18, L(18, 'The Atmosphere – Ocean Environment'), 1,
           L(18, 'Climate characteristics have an influence on economic development.', 'Tourism.'), '8-5', AO),
    option('24', 18, L(18, 'The Atmosphere – Ocean Environment'), 1,
           L(18, 'Describe the formation of each of the following and discuss its impact', 'Land and sea breezes.'),
           '8-3', AO),
]

TASKS = [*PART_ONE, *PART_TWO, *OPTIONS]

ID_CORRECTION_REASON = 'No deferred card shipped before this review, so no id is re-scoped.'

# No 2025 Higher deferred card shipped before this review.
LEGACY_IDS: list[str] = []
