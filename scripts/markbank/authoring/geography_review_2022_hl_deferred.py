"""Independent review ledger: Leaving Certificate Geography 2022 Higher Level, deferred sitting.

The SEC's deferred examination is a paper of its own. Sources (English
editions, harvested in paper-trail-corpus/deferredexams/2022 and
deferredmarkingschemes/2022, filed by Paper Trail as "<fileid>-deferred";
sizes pinned in EXPECTED_SOURCES and the generated audit): Part One and
Answerbook LC005ALP042EV (48 pages), Part Two LC005ALP043EV (20 pages),
marking scheme LC005ALP000EV (62 pages), and the sitting's own companions:
the 1:50 000 Caher map LC005CLP003EV, its legend LC005CLPC00EV and the Caher
aerial photograph LC005CLP004EV, which the SEC publishes only as a JPEG.

Visual sweep (every page rendered and read on 2026-11-19):
  Part One booklet p1 cover; p2 instructions (Part One "Attempt any TEN",
  80 marks; Part Two "attempt THREE", 240 marks); p3-p12 Questions 1-12 (p7
  holds Q5 and Q6, p8 Q7 and Q8); p13 Part Two answerbook instructions;
  p14-p17 graph paper; p18-p47 lined answer pages; p48 back cover.
  Part Two booklet p1 cover; p2 Part Two instructions; p3-p8 Sections 1-2
  (Q1-Q6); p9 Section 3 divider; p10-p15 Electives (Q7-Q12); p16 Section 4
  divider and note; p17-p18 Options (Q13-Q24); p19 "Do not hand this up";
  p20 back cover and copyright notice.
  Scheme p1 cover; p2 the note on deferred marking schemes; p3 notes and
  annotation key; p4 Part One table (two columns: Q1-Q6, Q7-Q12); p5-p23
  Q1-Q6 (each reprints its question; 2B route (i) on p9, route (ii) on p10);
  p24 Electives divider; p25-p43 Q7-Q12 (7A(ii) on p26, 12A(ii) at the foot
  of p41); p44 Options divider; p45 option outline and Overall Coherence
  descriptors; p46 option annotations; p47-p54 Q13-Q24; p55-p58
  Geographical Investigation (coursework); p59 investigation topics; p60
  Irish-language bonus marks; p61-p62 blank.
  Companions: Caher map extract (the River Suir and the River Aherlow, the
  M8 and N24, Caher Castle); OS legend sheet; oblique aerial photograph of
  Caher.

The deferred scheme is as detailed as June's: it sets out every printed
part, so every part is carded with its own published allocation. Part One
prices every part separately (Q1(i) four letters at 1 mark each, Q2(i)
letters and Q2(ii) processes 1 mark per row, read from their own columns of
the scheme table; Q9 four letters at 2; Q11 each region row 1 + 1). Part
Two follows the June 2023 ledger: every A-part roman is a task; B, C and
options are one task each. Finite printed choices are routes: 2B (i) or
(ii), with (i)'s any one fluvial, coastal or glacial landform (the scheme's
one row "Landform of erosion or deposition named" leaves erosion or
deposition to the landform chosen); 3B either volcanic structures or
structures of deformation; 3C and 9B one of the printed bullets; 6B
physical factors or human factors (an inline choice, as June's "culture or
climate"). Open choices ("any two factors", "example(s)", "one
multinational company") stay one card. 9A(v) prints two advantages the
scheme prices 2 + 2 marks each, so it carries two criteria.
"""

from geography_review import (
    Criterion, Lift, Route, SchemeSlice, Task, evens, fixed, slug, srp, sums, upto,
)

YEAR = 2022
LEVEL = 'higher'
REVIEWED_AT = '2026-11-19'
PAPER_PAGES = {1: 48, 2: 20}
SCHEME_PAGES = 62
QUESTION_TARIFFS = {1: {str(n): 8 for n in range(1, 13)},
                    2: {**{f'{n}{x}': (20 if x == 'A' else 30)
                           for n in range(1, 13) for x in 'ABC'},
                        **{str(n): 80 for n in range(13, 25)}}}

EXPECTED_SOURCES = {
    'paper1': ('LC005ALP042EV.pdf', 2290175),
    'paper2': ('LC005ALP043EV.pdf', 1871063),
    'scheme': ('LC005ALP000EV.pdf', 1530207),
    'map': ('LC005CLP003EV.pdf', 3484232),
    'legend': ('LC005CLPC00EV.pdf', 763003),
    'aerial': ('LC005CLP004EV.jpg', 6002664),
}

PAGE_REVIEW = {
    'paper1': {1: 'cover', 2: 'instructions', **{p: 'question' for p in range(3, 13)},
               13: 'answerbook instructions', **{p: 'graph-paper answer page' for p in range(14, 18)},
               **{p: 'lined answer page' for p in range(18, 48)}, 48: 'copyright/back cover'},
    'paper2': {1: 'cover', 2: 'Part Two instructions',
               **{p: 'question' for p in (3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15, 17, 18)},
               9: 'section divider', 16: 'section divider and option note',
               19: 'do not hand this up', 20: 'copyright/back cover'},
    'scheme': {1: 'cover', 2: 'note on deferred marking schemes', 3: 'notes and annotation key',
               4: 'Part One table',
               **{p: 'Part Two allocation' for p in range(5, 24)}, 24: 'section divider',
               **{p: 'Part Two allocation' for p in range(25, 44)}, 44: 'section divider',
               45: 'option outline and coherence descriptors', 46: 'option annotations',
               **{p: 'option allocation' for p in range(47, 55)},
               **{p: 'geographical investigation (coursework)' for p in range(55, 59)},
               59: 'investigation topics', 60: 'Irish-language bonus marks',
               61: 'blank', 62: 'blank'},
}

EXPECTED_SELECTION_SCAN = [
    [1, 2, 'attempt any ten'], [1, 2, 'attempt three'], [1, 2, 'choose'], [1, 2, 'choose'],
    [1, 3, 'attempt any ten'],
    [2, 2, 'attempt three'], [2, 2, 'choose'], [2, 2, 'choose'],
    [2, 4, 'answer (i) or (ii)'], [2, 4, 'any one'],
    [2, 5, 'either'], [2, 5, 'one of the following'],
    [2, 6, 'any two'],
    [2, 12, 'one of the following'],
]
SELECTION_REVIEW = [
    {'scan': [[1, 2, 'attempt any ten'], [1, 2, 'attempt three'], [1, 2, 'choose'], [1, 2, 'choose'],
              [1, 3, 'attempt any ten'], [2, 2, 'attempt three'], [2, 2, 'choose'], [2, 2, 'choose']],
     'kind': 'exam-attempt-rule',
     'reason': 'Part One any ten of twelve and Part Two three questions ("not allowed to choose all '
               'three questions from the same section") are attempt rules; every question is carded.'},
    {'scan': [[2, 4, 'answer (i) or (ii)'], [2, 4, 'any one']], 'kind': 'closed-route',
     'reason': '2B: (i) or (ii); (i) any one fluvial, coastal or glacial landform -> 4 routes.'},
    {'scan': [[2, 5, 'either']], 'kind': 'closed-choose-one',
     'reason': '3B either volcanic structures or structures of deformation -> 2 routes.'},
    {'scan': [[2, 5, 'one of the following'], [2, 12, 'one of the following']], 'kind': 'closed-choose-one',
     'reason': '3C one of three printed impacts -> 3 routes; 9B one of two printed economic activities '
               '-> 2 routes.'},
    {'scan': [[2, 6, 'any two']], 'kind': 'open-response',
     'reason': '4B "any two factors" prints no list, so it is an open choice. Open choices are not '
               'fanned out: "example(s)", "one multinational company", "one developing world city". '
               '6B "physical factors or human factors" is an inline closed choice -> 2 routes. '
               'Compulsory lists stay whole: 1A, 4A, 8A and 10A each bullet, 16 and 18 each process.'},
]

P1, P2 = 1, 2
LEFT = (0.0, 0.0, 0.5, 1.0)
RIGHT = (0.5, 0.0, 1.0, 1.0)
ID = 'geography-2022-hl-deferred-'
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


def one_plus_one(line, label):
    return fixed(label, 2, line, (0, 1, 2))


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
ECON = (H + 'elective-economic',)
DEV = (H + 'economic-developing-economies',)
MNC = (H + 'economic-multinationals-globalisation',)
EU = (H + 'economic-european-union',)
ENV = (H + 'economic-environmental-impact',)
ENERGY = (H + 'economic-energy',)

# Q2's letters and processes share the scheme table's rows: each part reads its own column.
Q2_LETTERS = (0.0, 0.283, 0.27, 0.355)
Q2_PROCESSES = (0.27, 0.283, 0.5, 0.355)

Q1S = (L(3, 'Examine the diagram above and answer each of the following questions.'),)
PART_ONE = [
    T('p1-1-i', P1, '1', '(i)', 4, 3, L(3, 'Volcanic Activity'),
      (L(3, '(i) Match each of the letters A, B, C and D with the feature', 'table below.'),),
      (S(4, '(i) D · 1m', '(ii) True', LEFT),), rows(['(i) D · 1m', '=A 1m', '=B 1m', '=C 1m']),
      '0-7', EV, ID + 'p1-q1', ('page',), Q1S,
      row_labels=(L(3, 'Magma chamber'), L(3, 'Sill'), L(3, 'Laccolith'), L(3, 'Dyke'))),
    T('p1-1-ii', P1, '1', '(ii)', 2, 3, L(3, 'Volcanic Activity'),
      (L(3, '(ii) Indicate whether the following statement is true or false', 'intrusive volcanic features.'),),
      (S(4, '(ii) True 2m', '(iii) Valid explanation', LEFT, after='Q1'),), (fixed('True or false', 2, '(ii) True 2m'),),
      '0-7', EV, ID + 'p1-q1-ii', ('page',), Q1S),
    T('p1-1-iii', P1, '1', '(iii)', 2, 3, L(3, 'Volcanic Activity'),
      (L(3, '(iii) Explain briefly what is meant by the term hot spot with regard to volcanic activity.'),),
      (S(4, '(iii) Valid explanation 1+1m', 'Q2', LEFT),),
      (one_plus_one('(iii) Valid explanation 1+1m', 'Explanation'),), '0-7', EV + PS, ID + 'p1-q1-iii',
      ('page',), Q1S),
]

Q2S = (L(4, 'Examine the map above and answer each of the following questions.'),)
Q2_ROWS = (L(4, 'Sea stack'), L(4, 'Sand spit'), L(4, 'Beach'), L(4, 'Headland'))
PART_ONE += [
    T('p1-2-i', P1, '2', '(i)', 4, 4, L(4, 'Coastal Landforms'),
      (L(4, '(i) Match each of the letters A, B, C and D with the landform', 'table below.'),),
      (S(4, '(i) C · 1m', None, Q2_LETTERS),), rows(['(i) C · 1m', 'A · 1m', 'B · 1m', '=D 1m']),
      '0-10', SEA, ID + 'p1-q2', ('page',), Q2S, row_labels=Q2_ROWS),
    T('p1-2-ii', P1, '2', '(ii)', 4, 4, L(4, 'Coastal Landforms'),
      (L(4, '(ii) Indicate whether processes of coastal erosion or coastal deposition', 'table below.'),),
      (S(4, '(ii) Erosion 1m', None, Q2_PROCESSES),),
      rows(['(ii) Erosion 1m', '=Deposition 1m@0', '=Deposition 1m@1', '=Erosion 1m']),
      '0-10', SEA, ID + 'p1-q2-ii', ('page',), Q2S, row_labels=Q2_ROWS),
]

Q3S = (L(5, 'Examine the photograph above and answer each of the following questions.'),)
PART_ONE += [
    T('p1-3-i', P1, '3', '(i)', 6, 5, L(5, 'Glacial and River Landforms'),
      (L(5, '(i) Match each of the letters A, B, C, D, E and F', 'table below.'),),
      (S(4, 'B 1m', '(ii) Valid processes', LEFT, after='Q3 (i)'),),
      rows(['B 1m', 'F 1m', 'E 1m', 'C 1m', 'D 1m', 'A 1m']),
      '0-11', GLAC + RIVERS, ID + 'p1-q3', ('page',), Q3S,
      row_labels=(L(5, 'Moraine dammed lake'), L(5, 'Braiding'), L(5, 'Meander'), L(5, 'Lateral moraine'),
                  L(5, 'Crevasses'), L(5, 'Retreating glacier'))),
    T('p1-3-ii', P1, '3', '(ii)', 2, 5, L(5, 'Glacial and River Landforms'),
      (L(5, '(ii) State two processes of glacial erosion.'),),
      (S(4, '(ii) Valid processes 1+1m', 'Q4', LEFT),),
      (one_plus_one('(ii) Valid processes 1+1m', 'Two processes'),),
      '0-11', GLAC, ID + 'p1-q3-ii', ('page',), Q3S),
]

PART_ONE += romans(P1, '4', 6, L(6, 'Rock Cycle'),
                   (L(6, 'Examine the diagram of the rock cycle above and answer each of the following questions.'),),
                   ID + 'p1-q4', ('page',), [
    ('(i)', 2, L(6, '(i) Name the category of rock at X', 'where this rock is found.'),
     S(4, '(i) Igneous 1m', '(ii) Sedimentary', LEFT),
     (fixed('Category', 1, '(i) Igneous 1m'), fixed('Irish location', 1, 'Valid Irish location 1m')), '0-1', RW),
    ('(ii)', 2, L(6, '(ii) Name the category of rock at Y', 'where this rock is found.'),
     S(4, '(ii) Sedimentary 1m', '(iii) Valid factor', LEFT),
     (fixed('Category', 1, '(ii) Sedimentary 1m'), fixed('Irish location', 1, 'Valid Irish location 1m')),
     '0-1', RW),
    ('(iii)', 2, L(6, '(iii) Name two factors that result in metamorphism.'),
     S(4, '(iii) Valid factor 1+1m', '(iv) Valid explanation', LEFT),
     (one_plus_one('(iii) Valid factor 1+1m', 'Two factors'),), '0-1', RW),
    ('(iv)', 2, L(6, '(iv) Explain briefly the term lithification.'),
     S(4, '(iv) Valid explanation 1+1m', 'Q5', LEFT),
     (one_plus_one('(iv) Valid explanation 1+1m', 'Explanation'),), '0-1', RW),
])

PART_ONE += romans(P1, '5', 7, L(7, 'Weather Chart'),
                   (L(7, 'Examine the weather chart above and indicate whether', 'in each case.'),),
                   ID + 'p1-q5', ('page',), [
    ('(i)', 2, L(7, '(i) The barometric pressure over the United Kingdom is 975 hPa.'),
     S(4, '(i) False 2m', '(ii) True', LEFT, after='Q5'), (fixed('True or false', 2, '(i) False 2m'),), '2-7', WX),
    ('(ii)', 2, L(7, '(ii) A cold front is approaching Ireland from the south-west.'),
     S(4, '(ii) True 2m', '(iii) False', LEFT, after='Q5'), (fixed('True or false', 2, '(ii) True 2m'),), '2-7', WX),
    ('(iii)', 2, L(7, '(iii) There are strong winds over Ireland.'),
     S(4, '(iii) False 2m', '(iv) False', LEFT, after='Q5'), (fixed('True or false', 2, '(iii) False 2m'),),
     '2-7', WX),
    ('(iv)', 2, L(7, '(iv) Lines joining areas of equal rainfall are called isotherms.'),
     S(4, '(iv) False 2m', 'Q6', LEFT, after='Q5'), (fixed('True or false', 2, '(iv) False 2m'),), '2-7', WX),
])

PART_ONE += romans(P1, '6', 7, L(7, 'Folding and Faulting'),
                   (L(7, 'Indicate whether each of the following statements is true or false', 'in each case.'),),
                   ID + 'p1-q6', ('page',), [
    ('(i)', 2, L(7, '(i) Caledonian folding occurred 400 million years ago.'),
     S(4, '(i) True 2m', '(ii) True', LEFT, after='Q6'), (fixed('True or false', 2, '(i) True 2m'),), '0-2', RW),
    ('(ii)', 2, L(7, '(ii) An anticline is an upfold in rock.'),
     S(4, '(ii) True 2m', '(iii) False', LEFT, after='Q6'), (fixed('True or false', 2, '(ii) True 2m'),), '0-2', RW),
    ('(iii)', 2, L(7, '(iii) Normal faults occur when two blocks of rock are pushed together.'),
     S(4, '(iii) False 2m', '(iv) True', LEFT, after='Q6'), (fixed('True or false', 2, '(iii) False 2m'),),
     '0-2', RW),
    ('(iv)', 2, L(7, '(iv) A block mountain is also known as a horst.'),
     S(4, '(iv) True 2m', None, LEFT, after='Q6'), (fixed('True or false', 2, '(iv) True 2m'),), '0-2', RW),
])

PART_ONE += romans(P1, '7', 8, L(8, 'Ordnance Survey Map', nth=0),
                   (L(8, 'Examine the 1:50 000 Ordnance Survey map and legend that accompany this paper and',
                      'following questions.'),),
                   ID + 'p1-q7', ('map', 'legend'), [
    ('(i)', 2, L(8, '(i) Give a six-figure grid reference for the Garda Station on the map.'),
     S(4, '(i) S 055 248 · 2m', '(ii) Roundabout', RIGHT), (fixed('Grid reference', 2, '(i) S 055 248 · 2m'),),
     '2-6', MAP),
    ('(ii)', 2, L(8, '(ii) The transport feature on the N24 road at S 061 275 is a:'),
     S(4, '(ii) Roundabout 2m', '(iii) Concave', RIGHT), (fixed('Transport feature', 2, '(ii) Roundabout 2m'),),
     '2-6', MAP),
    ('(iii)', 2, (L(8, '(iii) Indicate the type of slope that is found between S 013 258', 'correct box below.'),
                  L(8, 'Concave Convex Even')),
     S(4, '(iii) Concave · 2m', '(iv) 7.9', RIGHT), (fixed('Slope', 2, '(iii) Concave · 2m'),), '2-6', MAP),
    ('(iv)', 2, L(8, '(iv) Measure the distance, in kilometres, along the M8 motorway', 'at R 998 226.'),
     S(4, '(iv) 7.9 (km) 2m', 'Q8', RIGHT), (fixed('Distance', 2, '(iv) 7.9 (km) 2m'),), '2-6', MAP),
])

PART_ONE += romans(P1, '8', 8, L(8, 'Aerial Photograph and Ordnance Survey Map'),
                   (L(8, 'Examine the aerial photograph, the 1:50 000 Ordnance Survey map and legend that',
                      'following questions.'),),
                   ID + 'p1-q8', ('aerial', 'map', 'legend'), [
    ('(i)', 2, L(8, '(i) Name the bridge crossing the river in the centre background', 'aerial photograph.'),
     S(4, '(i) Suir Bridge · 2m', '(ii) S 052', RIGHT), (fixed('Bridge', 2, '(i) Suir Bridge · 2m'),), '2-8', AER),
    ('(ii)', 2, L(8, '(ii) Give a six-figure grid reference for the location of this bridge on the map.'),
     S(4, '(ii) S 052 252 2m', '(iii) Castle', RIGHT), (fixed('Grid reference', 2, '(ii) S 052 252 2m'),),
     '2-8', AER + MAP),
    ('(iii)', 2, L(8, '(iii) Name the antiquity in the centre middleground', 'defence function.'),
     S(4, '(iii) Castle · 2m', '(iv) North', RIGHT), (fixed('Antiquity', 2, '(iii) Castle · 2m'),), '2-8', AER),
    ('(iv)', 2, L(8, '(iv) In what direction was the camera pointed', 'was taken?'),
     S(4, '(iv) North 2m', 'Q9', RIGHT), (fixed('Direction', 2, '(iv) North 2m'),), '2-8', AER),
])

PART_ONE.append(T(
    'p1-9', P1, '9', '', 8, 9, L(9, 'Satellite Image Interpretation'),
    (L(9, 'Match each of the letters A, B, C and D with the description', 'table below.'),),
    (S(4, 'C 2m', 'Q10', RIGHT, after='Q9'),), rows(['C 2m', 'A 2m', 'D 2m', 'B 2m'], 2),
    '2-8', AER, ID + 'p1-q9', ('page',), (L(9, 'Examine the satellite images above.'),),
    row_labels=(L(9, 'Hurricane'), L(9, 'Opencast mining'), L(9, 'Flooding'), L(9, 'Delta'))))

PART_ONE += romans(P1, '10', 10, L(10, 'Graphical Interpretation'),
                   (L(10, 'Examine the climate graph and statistics above and answer each of the following questions.'),),
                   ID + 'p1-q10', ('page',), [
    ('(i)', 2, L(10, '(i) Calculate the total annual rainfall (mm).'),
     S(4, '(i) 587 (mm) 2m', '(ii) 15', RIGHT), (fixed('Total', 2, '(i) 587 (mm) 2m'),), '2-0', TG),
    ('(ii)', 2, L(10, '(ii) Calculate the annual temperature range (oC).'),
     S(4, '(ii) 15 (°C) 2m', '(iii) July', RIGHT), (fixed('Range', 2, '(ii) 15 (°C) 2m'),), '2-0', TG),
    ('(iii)', 2, L(10, '(iii) Which month experienced the highest temperature but the lowest rainfall level?'),
     S(4, '(iii) July 2m', '(iv) Temperate', RIGHT), (fixed('Month', 2, '(iii) July 2m'),), '2-0', TG),
    ('(iv)', 2, (L(10, '(iv) Which of the following climate types', 'Tick (✓) the correct box.'),
                 L(10, 'Temperate Oceanic Hot Desert Equatorial')),
     S(4, '(iv) Temperate Oceanic 2m', 'Q11', RIGHT), (fixed('Climate type', 2, '(iv) Temperate Oceanic 2m'),),
     '2-0', TG + WX),
])

PART_ONE.append(T(
    'p1-11', P1, '11', '', 8, 11, L(11, 'Regions'),
    (L(11, 'The table below contains information on regions', 'One row of the table is completed for you.'),
     Lift(11, 'Mediterranean', 'County Tipperary', row=True)),
    (S(4, 'Milan 1m', 'Q12', RIGHT),),
    (one_plus_one('Milan 1m Northern Italy 1m', 'Urban'),
     one_plus_one('Mediterranean 1m Southern Europe 1m', 'Climate'),
     one_plus_one('Co. Tipperary 1m Ireland 1m', 'Administrative'),
     one_plus_one('Basque Lands 1m Northern Spain 1m', 'Cultural')),
    '1-0', EURO + IRL, ID + 'p1-q11', ('page',),
    row_labels=(L(11, 'Urban'), L(11, 'Climate'), L(11, 'Administrative'), L(11, 'Cultural'))))

PART_ONE += romans(P1, '12', 12, L(12, 'The European Union'),
                   (L(12, 'Examine the map above showing the year current and former member states joined the',
                      'answer the following questions.'),),
                   ID + 'p1-q12', ('page',), [
    ('(i)', 2, L(12, '(i) Name one country that was a member when the EU was created in 1957.'),
     S(4, '(i) Valid country 2m', '(ii) 2007', RIGHT), (fixed('Country', 2, '(i) Valid country 2m'),), '1-5', EURO),
    ('(ii)', 2, L(12, '(ii) In what year did Bulgaria join the EU?'),
     S(4, '(ii) 2007 2m', '(iii) Valid country', RIGHT), (fixed('Year', 2, '(ii) 2007 2m'),), '1-5', EURO),
    ('(iii)', 2, L(12, '(iii) Malta joined the EU in 2004, name one other country that joined in that year.'),
     S(4, '(iii) Valid country 2m', '(iv) Three', RIGHT), (fixed('Country', 2, '(iii) Valid country 2m'),),
     '1-5', EURO),
    ('(iv)', 2, L(12, '(iv) How many countries joined the EU in 1973?'),
     S(4, '(iv) Three 2m', None, RIGHT), (fixed('Number', 2, '(iv) Three 2m'),), '1-5', EURO),
])


# ---------------------------------------------------------------- Part Two --
def sketch(outline_line, outline_permitted, alloc, item_permitted, labels):
    return (fixed('Sketch outline' if 'Sketch' in outline_line else 'Map outline', 4,
                  outline_line, outline_permitted),
            *(Criterion(f'Feature {n}', 4, item_permitted, 'exact', alloc) for n in range(1, labels + 1)))


OS_SKETCH = sketch('Sketch Outline · 4 marks (4/0)', (0, 4),
                   ('4 features @ 4 marks each', 'Label 1m'), sums((0, 1, 3), (0, 1)), 4)
AERIAL_SKETCH = sketch('Sketch Outline · 4 marks (4/0)', (0, 4),
                       ('4 features @ 4 marks each', 'Label 1 mark'), sums((0, 1, 3), (0, 1)), 4)
GRAPH = (fixed('Title', 2, ('Bar Chart · Pie Chart', 'Title · 2 marks · 2 marks')),
         fixed('Axes named (bar chart) / circle and centre (pie chart)', 2,
               ('Vertical axis named', 'Horizontal axis named'), (0, 1, 2)),
         fixed('6 items illustrated', 12, '6 items illustrated', upto(12)))


def bullet_routes(prefix, items, atlas=None):
    return tuple(Route(slug(item, 34), item.rstrip('.'), ID + prefix + slug(item, 34), False,
                       keep_bullets=(item,), atlas=(atlas[item] if atlas else None))
                 for item in items)


def split(label, total, first, second):
    """One allocation printed as two parts examined 6/7 and 7/6 SRPs."""
    return srp(label, total, (first, second))


LANDFORMS = 'any one fluvial, coastal or glacial landform'
TECTONIC = 'either volcanic structures or structures of deformation'
FACTORS = 'physical factors or human factors'

PART_TWO = [
    T('p2-1a', P2, '1A', '', 20, 3, L(3, 'Ordnance Survey Map'),
      (L(3, 'Examine the 1:50 000 Ordnance Survey map and legend that accompany this paper.', 'River Suir.'),),
      (S(5, 'Sketch Outline', None),), OS_SKETCH, '2-6', MAP, ID + 'p2-q1a', ('map', 'legend'),
      row_labels=(None, L(3, 'The complete course of the River Suir'),
                  L(3, 'The entire area of land above 400 metres east of easting 00'),
                  L(3, 'A V-shaped valley (mark on your sketch map with the letter X)'),
                  L(3, 'The entire area of deciduous woodland', 'River Suir.'))),
    T('p2-1b', P2, '1B', '', 30, 3, L(3, 'Rocks'),
      (L(3, 'Examine the formation of sedimentary rocks', 'that you have studied.'),),
      (S(6, 'Sedimentary rocks named', 'Annotation'),),
      (pair('Sedimentary rocks named · 2 + 2 marks', 'Sedimentary rocks named'),
       srp('Examination', 13, 'Examination · 13 x SRPs')),
      '0-1', RW, ID + 'p2-q1b'),
    T('p2-1c', P2, '1C', '', 30, 3, L(3, 'Isostasy'),
      (L(3, 'Examine how isostasy has impacted on the Irish landscape.'),),
      (S(7, 'Impact identified · 2 marks', 'Annotation'),),
      (fixed('Impact identified', 2, 'Impact identified · 2 marks'),
       srp('Examination', 14, 'Examination · 14 x SRPs')),
      '0-5', RIVERS + SEA, ID + 'p2-q1c'),
]

PART_TWO += romans(P2, '2A', 4, L(4, 'Plate Tectonics'),
                   (L(4, 'Examine the map above and answer each of the following questions.'),),
                   ID + 'p2-q2a', ('page',), [
    ('(i)', 8, L(4, '(i) Name each of the tectonic plates A, B, C and D.'),
     S(8, '(i) · A · Eurasian', '(ii) · X'),
     (fixed('A', 2, 'A · Eurasian · 2 marks'), fixed('B', 2, 'B · South American · 2 marks'),
      fixed('C', 2, 'C · Nazca · 2 marks'), fixed('D', 2, 'D · African · 2 marks')), '0-0', PS),
    ('(ii)', 4, L(4, '(ii) Name the type of plate boundary at X and the type of plate boundary at Y.'),
     S(8, '(ii) · X', '(iii) · Valid'),
     (fixed('X', 2, 'X · Destructive/Convergent · 2 marks'), fixed('Y', 2, 'Y · Conservative/Passive · 2 marks')),
     '0-0', PS),
    ('(iii)', 4, L(4, '(iii) Explain briefly what is meant by the term sea floor spreading.'),
     S(8, '(iii) · Valid explanation', '(iv) · Valid'),
     (pair('(iii) · Valid explanation · 2 + 2 marks', 'Explanation'),), '0-0', PS),
    ('(iv)', 4, L(4, '(iv) Name two examples of tectonic landforms resulting from sea floor spreading.'),
     S(8, '(iv) · Valid examples', None), (pair('(iv) · Valid examples · 2 + 2 marks', 'Two examples'),),
     '0-0', PS),
])

ROUTE_I = (fixed('Landform named', 2, 'Landform of erosion or deposition named · 2 marks'),
           fixed('Impact of processes', 2, 'Impact of processes · 2 marks'),
           fixed('Diagram', 2, 'Diagram · 2 marks'),
           srp('Examination', 12, f'Examination · 12 x {SRPS}'))
PART_TWO += [
    T('p2-2b', P2, '2B', '', 30, 4, L(4, 'Landform Development'),
      (L(4, '(i) Examine, with the aid of a labelled diagram(s)', 'that you have studied.'),),
      (S(9, 'Landform of erosion or deposition named', 'Annotation'),), ROUTE_I,
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
                scheme=(S(10, 'Factors identified', 'Annotation'),),
                criteria=(pair('Factors identified · 2 + 2 marks', 'Factors identified'),
                          fixed('Mass movement process named', 2, 'Mass movement process named · 2 marks'),
                          srp('Description/explanation', 12, f'Description/explanation · 12 x {SRPS}')),
                topic='0-8', atlas=RW),
      )),
    T('p2-2c', P2, '2C', '', 30, 4, L(4, 'Rocks and Landscapes'),
      (L(4, 'Examine how different rock types produce distinctive landscapes', 'that you have studied.'),),
      (S(11, 'Rock 1 named', 'Annotation'),),
      (pair('Rock 1 named and example of associated landscape · 2 + 2 marks', 'Rock 1 and its landscape'),
       pair('Rock 2 named and example of associated landscape · 2 + 2 marks', 'Rock 2 and its landscape'),
       srp('Examination', 11, f'Examination · 11 x {SRPS}')),
      '0-1', RW, ID + 'p2-q2c'),
]

PART_TWO += romans(P2, '3A', 5, L(5, 'Weathering'),
                   (L(5, 'Examine the photographs above showing evidence of weathering', 'following questions.'),),
                   ID + 'p2-q3a', ('page',), [
    ('(i)', 8, (L(5, '(i) In your answer book, match each of the letters A, B, C and D', 'best matches it.'),
                L(5, 'Exfoliation'), L(5, '(onion weathering)'), L(5, 'Oxidation'), L(5, 'Freeze-thaw'),
                L(5, 'Carbonation')),
     S(12, '(i) · A · Carbonation', '(ii) · Oxidation'),
     (fixed('A', 2, 'A · Carbonation · 2 marks'), fixed('B', 2, 'B · Oxidation · 2 marks'),
      fixed('C', 2, 'C · Freeze-thaw · 2 marks'), fixed('D', 2, 'D · Exfoliation (onion weathering) · 2 marks')),
     '0-8', RW),
    ('(ii)', 8, L(5, '(ii) State whether each of the weathering processes in the list above', 'mechanical weathering.'),
     S(12, '(ii) · Oxidation', '(iii) · Valid'),
     (fixed('Oxidation', 2, '(ii) · Oxidation · Chemical · 2 marks'),
      fixed('Freeze-thaw', 2, 'Freeze-thaw · Mechanical · 2 marks'),
      fixed('Exfoliation (onion weathering)', 2, 'Exfoliation (onion weathering) · Mechanical · 2 marks'),
      fixed('Carbonation', 2, 'Carbonation · Chemical · 2 marks')), '0-8', RW),
    ('(iii)', 4, L(5, '(iii) Explain briefly what is meant by the term hydrolysis.'),
     S(12, '(iii) · Valid explanation', None), (pair('(iii) · Valid explanation · 2 + 2 marks', 'Explanation'),),
     '0-8', RW),
])

PART_TWO += [
    T('p2-3b', P2, '3B', '', 30, 5, L(5, 'The Tectonic Cycle'),
      (L(5, 'Explain how the development of landforms has resulted', 'faulting etc.).'),),
      (S(13, 'Landform named · 2 marks', 'Annotation'),),
      (fixed('Landform named', 2, 'Landform named · 2 marks'), srp('Explanation', 14, f'Explanation · 14 x {SRPS}')),
      '0-0', PS, ID + 'p2-q3b-volcanic-structures',
      routes=(
          Route('volcanic-structures', 'volcanic structures', ID + 'p2-q3b-volcanic-structures', False,
                ((TECTONIC, 'volcanic structures'),), topic='0-7', atlas=PS + EV),
          Route('structures-of-deformation', 'structures of deformation',
                ID + 'p2-q3b-structures-of-deformation', False,
                ((TECTONIC, 'structures of deformation'),), topic='0-2', atlas=PS + RW),
      )),
    T('p2-3c', P2, '3C', '', 30, 5, L(5, 'Human Interaction with Surface Processes'),
      (L(5, 'Examine how human activity impacts on surface processes', 'mass movement.'),),
      (S(14, 'Impact on process identified · 2 marks', 'Annotation'),),
      (fixed('Impact on process identified', 2, 'Impact on process identified · 2 marks'),
       srp('Examination of impact on process', 14, f'Examination of impact on process · 14 x {SRPS}')),
      '0-6', RW, ID + 'p2-q3c-' + slug('The impact of flood control measures on river processes', 34),
      routes=bullet_routes('p2-q3c-', (
          'The impact of flood control measures on river processes',
          'The impact of coastal defence work on coastal processes',
          'The impact of human activity on mass movement.'),
          atlas={'The impact of flood control measures on river processes': RIVERS,
                 'The impact of coastal defence work on coastal processes': SEA,
                 'The impact of human activity on mass movement.': RW})),
    # Question 4
    T('p2-4a', P2, '4A', '', 20, 6, L(6, 'Irish Region'),
      (L(6, 'Draw an outline map of Ireland.', 'feature of relief (upland or lowland).'),),
      (S(15, 'Map outline', None),),
      sketch('Map outline · 4 marks graded (4/2/0)', (0, 2, 4),
             ('4 features @ 4 marks each', 'Named 2 marks'), sums((0, 1, 2), (0, 2)), 4),
      '1-4', IRL, ID + 'p2-q4a',
      row_labels=(None, L(6, 'The outline of one named region'), L(6, 'One named river within the region'),
                  L(6, 'One named urban centre within the region'),
                  L(6, 'The outline of one named feature of relief (upland or lowland).'))),
    T('p2-4b', P2, '4B', '', 30, 6, L(6, 'Secondary Economic Activity'),
      (L(6, 'Discuss any two factors that influence the development of secondary economic activity',
         'that you have studied.'),),
      (S(16, 'Factors · 2 + 2 marks', 'Annotation'),),
      (pair('Factors · 2 + 2 marks', 'Factors'),
       split('Discussion of the two factors (6/7 and 7/6 SRPs)', 13,
             f'Discussion of Factor 1 · 6/7 x {SRPS}', f'Discussion of Factor 2 · 6/7 x {SRPS}')),
      '1-6', CONT, ID + 'p2-q4b'),
    T('p2-4c', P2, '4C', '', 30, 6, L(6, 'Tertiary Economic Activity'),
      (L(6, 'Describe and explain the growth of one tertiary economic activity', 'that you have studied.'),),
      (S(17, f'Description/Explanation · 15 x {SRPS}', 'Annotation'),),
      (srp('Description/explanation', 15, f'Description/Explanation · 15 x {SRPS}'),),
      '1-5', EURO, ID + 'p2-q4c'),
]

PART_TWO += romans(P2, '5A', 7, L(7, 'Irish Tourism'),
                   (L(7, 'Examine the table above showing the number of overseas visitors', 'following questions.'),),
                   ID + 'p2-q5a', ('page',), [
    ('(i)', 2, L(7, '(i) What was the total number of overseas visitors to Ireland in 2012?'),
     S(18, '(i) · 6,287,000', '(ii) · 2,870,000'), (fixed('Total', 2, '(i) · 6,287,000 · 2 marks'),), '2-0', TG),
    ('(ii)', 2, L(7, '(ii) How many visitors to Ireland came from Britain in 2013?'),
     S(18, '(ii) · 2,870,000', '(iii) · 2014'), (fixed('Visitors', 2, '(ii) · 2,870,000 · 2 marks'),), '2-0', TG),
    ('(iii)', 2, L(7, '(iii) In which year did the total overseas visitors to Ireland reach 7 million?'),
     S(18, '(iii) · 2014', '(iv) · 6.3'), (fixed('Year', 2, '(iii) · 2014 · 2 marks'),), '2-0', TG),
    ('(iv)', 2, L(7, '(iv) What was the percentage change in the total number of visitors', '2013 and 2014?'),
     S(18, '(iv) · 6.3', '(v) · 10'), (fixed('Percentage change', 2, '(iv) · 6.3 (%) · 2 marks'),), '2-0', TG),
    ('(v)', 4, L(7, '(v) Calculate X, the percentage change in visitors from North America', '2014.'),
     S(18, '(v) · 10/10.2/10.3', '(vi) · Valid'), (fixed('Calculation', 4, '(v) · 10/10.2/10.3 (%) · 4 marks'),),
     '2-0', TG),
    ('(vi)', 4, L(7, '(vi) Explain briefly one reason for this change.'),
     S(18, '(vi) · Valid explanation', '(vii) · Valid'), (pair('(vi) · Valid explanation · 2 + 2 marks', 'Reason'),),
     '1-4', IRL),
    ('(vii)', 4, L(7, '(vii) Explain briefly one challenge facing the Irish tourist industry', 'visitors to Ireland.'),
     S(18, '(vii) · Valid explanation', None), (pair('(vii) · Valid explanation · 2 + 2 marks', 'Challenge'),),
     '1-4', IRL),
])

PART_TWO += [
    T('p2-5b', P2, '5B', '', 30, 7, L(7, 'Socio-Economic Regions'),
      (L(7, 'Examine how economic activity in core regions differs', 'that you have studied.'),),
      (S(19, 'Difference identified · 2 marks', 'Annotation'),),
      (fixed('Difference identified', 2, 'Difference identified · 2 marks'),
       srp('Examination', 14, f'Examination · 14 x {SRPS}')),
      '1-1', IRL + EURO, ID + 'p2-q5b'),
    T('p2-5c', P2, '5C', '', 30, 7, L(7, 'Population Dynamics'),
      (L(7, 'Account for the distribution of population in a Continental', 'that you have studied.'),),
      (S(20, f'Examination · 15 x {SRPS}', 'Annotation'),), (srp('Examination', 15, f'Examination · 15 x {SRPS}'),),
      '1-6', CONT, ID + 'p2-q5c'),
]

PART_TWO += romans(P2, '6A', 8, L(8, 'Industrial production'),
                   (L(8, 'Examine the pie charts above which show the value of industrial production',
                      'following questions.'),),
                   ID + 'p2-q6a', ('page',), [
    ('(i)', 2, L(8, '(i) Which country had the highest value of industrial production', '2020?'),
     S(21, '(i) · Germany', '(ii) · 18'), (fixed('Country', 2, '(i) · Germany · 2 marks'),), '2-0', TG),
    ('(ii)', 4, L(8, '(ii) Calculate X, the value of industrial production (in %) for Italy in 2020.'),
     S(21, '(ii) · 18', '(iii) · France'), (fixed('Calculation', 4, '(ii) · 18 (%) · 4 marks'),), '2-0', TG),
    ('(iii)', 2, L(8, '(iii) Name one country that had no change', 'and 2020.'),
     S(21, '(iii) · France', '(iv) · Valid'), (fixed('Country', 2, '(iii) · France · 2 marks'),), '2-0', TG),
    ('(iv)', 4, L(8, '(iv) Give two examples of products manufactured in Ireland.'),
     S(21, '(iv) · Valid examples', '(v) · Valid'), (pair('(iv) · Valid examples · 2 + 2 marks', 'Two products'),),
     '1-4', IRL),
    ('(v)', 4, L(8, '(v) In 2020 the United Kingdom left the European Union.', 'remaining member states.'),
     S(21, '(v) · Valid explanation', '(vi) · Valid'), (pair('(v) · Valid explanation · 2 + 2 marks', 'Impact'),),
     '1-5', EURO),
    ('(vi)', 4, L(8, '(vi) Briefly explain one advantage for a country of having a large industrial sector.'),
     S(21, '(vi) · Valid explanation', None), (pair('(vi) · Valid explanation · 2 + 2 marks', 'Advantage'),),
     '1-5', EURO),
])

PART_TWO += [
    T('p2-6b', P2, '6B', '', 30, 8, L(8, 'Agriculture in Ireland'),
      (L(8, 'Examine the impact of physical factors or human factors', 'that you have studied.'),),
      (S(22, 'Physical or Human factors named', 'Annotation'),),
      (pair('Physical or Human factors named · 2 + 2 marks', 'Factors named'),
       srp('Examination', 13, f'Examination · 13 x {SRPS}')),
      '1-4', IRL, ID + 'p2-q6b-physical-factors',
      routes=(
          Route('physical-factors', 'physical factors', ID + 'p2-q6b-physical-factors', False,
                ((FACTORS, 'physical factors'),)),
          Route('human-factors', 'human factors', ID + 'p2-q6b-human-factors', False,
                ((FACTORS, 'human factors'),)),
      )),
    T('p2-6c', P2, '6C', '', 30, 8, L(8, 'Culture'),
      (L(8, 'Describe and explain the importance of culture in defining any region that you have studied.'),),
      (S(23, 'Example · 2 marks', 'Annotation'),),
      (fixed('Example', 2, 'Example · 2 marks'),
       srp('Description/explanation', 14, f'Description/Explanation · 14 x {SRPS}')),
      '1-3', IRL + EURO + CONT, ID + 'p2-q6c'),
]

PART_TWO += romans(P2, '7A', 10, L(10, 'Human Development Index', nth=0),
                   (L(10, 'Examine the data in the table above showing the Human Development Index', 'of countries.'),),
                   ID + 'p2-q7a', ('page',), [
    ('(i)', 16, L(10, '(i) Using graph paper, draw a suitable graph to illustrate this data.'),
     S(25, 'Bar Chart · Pie Chart', 'Annotation'), GRAPH, '2-0', TG),
    ('(ii)', 4, L(10, '(ii) Gross National Product is one of the indicators', 'Human Development Index.'),
     S(26, 'Valid indicators · 2m + 2m', None), (pair('Valid indicators · 2m + 2m', 'Two indicators'),),
     '3-1', DEV),
])

PART_TWO += [
    T('p2-7b', P2, '7B', '', 30, 10, L(10, 'Economic Activity'),
      (L(10, 'Examine the 1:50 000 Ordnance Survey map and legend that accompany this paper.',
         'to support your answer.'),),
      (S(27, 'Three different types of economic activity @ 10 marks each', 'Annotation'),),
      tuple(Criterion(f'Economic activity {n}', 10, evens(10), 'srp',
                      ('Three different types of economic activity @ 10 marks each',
                       'For each type of economic activity:', 'Economic activity identified · 2 marks',
                       'Map evidence · 2 marks', f'Description/explanation · 3 x {SRPS}'))
            for n in (1, 2, 3)),
      '2-6', MAP + ECON, ID + 'p2-q7b', ('map', 'legend')),
    T('p2-7c', P2, '7C', '', 30, 10, L(10, 'Economic Development'),
      (L(10, 'Examine the impact of colonisation on a developing economy that you have studied.'),),
      (S(28, 'Impact identified · 2 marks', 'Annotation'),),
      (fixed('Impact identified', 2, 'Impact identified · 2 marks'),
       fixed('Named developing economy', 2, 'Named developing economy · 2 marks'),
       srp('Examination', 13, f'Examination · 13 x {SRPS}')),
      '3-1', DEV, ID + 'p2-q7c'),
    # Question 8
    T('p2-8a', P2, '8A', '', 20, 11, L(11, 'Ordnance Survey Map'),
      (L(11, 'Examine the 1:50 000 Ordnance Survey map and legend that accompany this paper.', 'The railway line.'),),
      (S(29, 'Sketch Outline', None),), OS_SKETCH, '2-6', MAP, ID + 'p2-q8a', ('map', 'legend'),
      row_labels=(None, L(11, 'The built up area of Caher'), L(11, 'The M8 motorway'),
                  L(11, 'An electricity transmission line'), L(11, 'The railway line.'))),
    T('p2-8b', P2, '8B', '', 30, 11, L(11, 'Multinational Company'),
      (L(11, 'Examine the mobility of modern economic activities', 'that you have studied.'),),
      (S(30, 'Named MNC · 2 marks', 'Annotation'),),
      (fixed('Named MNC', 2, 'Named MNC · 2 marks'), srp('Examination', 14, f'Examination · 14 x {SRPS}')),
      '3-2', MNC, ID + 'p2-q8b'),
    T('p2-8c', P2, '8C', '', 30, 11, L(11, 'Economic Development'),
      (L(11, 'Examine how service industries dominate in one developed economy that you have studied.'),),
      (S(31, 'Developed economy named · 2 marks', 'Annotation'),),
      (fixed('Developed economy named', 2, 'Developed economy named · 2 marks'),
       srp('Examination', 14, f'Examination · 14 x {SRPS}')),
      '3-0', ECON, ID + 'p2-q8c'),
]

PART_TWO += romans(P2, '9A', 12, L(12, 'Renewable Energy', nth=0),
                   (L(12, 'Study the map above showing the percentage of energy consumed in 2015',
                      'following questions.'),),
                   ID + 'p2-q9a', ('page',), [
    ('(i)', 4, L(12, '(i) Name two countries in which 20-30% of the energy consumed was renewable energy.'),
     S(32, '(i) · Valid countries', '(ii) · Iceland'), (pair('(i) · Valid countries named · 2 + 2 marks', 'Two countries'),),
     '2-0', TG + ENERGY),
    ('(ii)', 2, L(12, '(ii) Name one country where over 60% of energy consumed was renewable energy.'),
     S(32, '(ii) · Iceland or Norway', '(iii) · 5-10'), (fixed('Country', 2, '(ii) · Iceland or Norway · 2 marks'),),
     '2-0', TG + ENERGY),
    ('(iii)', 2, L(12, '(iii) What percentage range of energy consumed in Ireland was renewable energy?'),
     S(32, '(iii) · 5-10', '(iv) · Valid sources'), (fixed('Range', 2, '(iii) · 5-10 (%) · 2 marks'),),
     '2-0', TG + ENERGY),
    ('(iv)', 4, L(12, '(iv) Name two sources of renewable energy.'),
     S(32, '(iv) · Valid sources', '(v) · Valid'),
     (pair('(iv) · Valid sources of renewable energy 2 + 2 marks', 'Two sources'),), '3-5', ENERGY),
    ('(v)', 8, L(12, '(v) Explain briefly two advantages of renewable energy.'),
     S(32, '(v) · Valid explanations', None),
     (pair('(v) · Valid explanations · 2 + 2 marks', 'Advantage 1'), pair('=2 + 2 marks', 'Advantage 2')),
     '3-5', ENERGY),
])

PART_TWO += [
    T('p2-9b', P2, '9B', '', 30, 12, L(12, 'Ireland and the European Union'),
      (L(12, 'Examine how European Union policy has influenced', 'Secondary economic activity.'),),
      (S(33, 'Influence on either primary', 'Annotation'),),
      (fixed('Influence identified', 2,
             'Influence on either primary or secondary economic activity identified · 2 marks'),
       fixed('EU policy named', 2, 'EU policy named · 2 marks'),
       srp('Examination', 13, f'Examination · 13 x {SRPS}')),
      '3-3', EU, ID + 'p2-q9b-' + slug('Primary economic activity', 34),
      routes=bullet_routes('p2-q9b-', ('Primary economic activity', 'Secondary economic activity.'))),
    T('p2-9c', P2, '9C', '', 30, 12, L(12, 'Conflict of Interest'),
      (L(12, 'Discuss how conflict may arise between economic interests', 'that you have studied.'),),
      (S(34, 'Example · 2 marks', 'Annotation'),),
      (fixed('Example', 2, 'Example · 2 marks'), srp('Discussion', 14, f'Discussion · 14 x {SRPS}')),
      '3-4', ENV, ID + 'p2-q9c'),
    # Question 10
    T('p2-10a', P2, '10A', '', 20, 13, L(13, 'Aerial Photograph'),
      (L(13, 'Examine the aerial photograph accompanying this paper.', 'in the background.'),),
      (S(35, 'Sketch Outline', None),), AERIAL_SKETCH, '2-8', AER + URB, ID + 'p2-q10a', ('aerial',),
      row_labels=(None, L(13, 'A weir'), L(13, 'A church'), L(13, 'A recreational area'),
                  L(13, 'A modern housing estate in the background.'))),
    T('p2-10b', P2, '10B', '', 30, 13, L(13, 'Overpopulation'),
      (L(13, 'Examine one cause and one effect of overpopulation', 'have studied.'),),
      (S(36, 'Cause identified · 2 marks', 'Annotation'),),
      (fixed('Cause identified', 2, 'Cause identified · 2 marks'),
       fixed('Effect identified', 2, 'Effect identified · 2 marks'),
       fixed('Example', 2, 'Example · 2 marks'),
       srp('Examination of causes', 6, f'Examination of causes · 6 x {SRPS}'),
       srp('Examination of effects', 6, f'Examination of effects · 6 x {SRPS}')),
      '4-1', POP, ID + 'p2-q10b'),
    T('p2-10c', P2, '10C', '', 30, 13, L(13, 'Central Place Theory', nth=0),
      (L(13, 'Describe and explain Central Place Theory with reference to example(s)', 'studied.'),),
      (S(37, 'Example · 2 marks', 'Annotation'),),
      (fixed('Example', 2, 'Example · 2 marks'),
       srp('Description and explanation', 14, f'Description and explanation · 14 x {SRPS}')),
      '4-3', URB, ID + 'p2-q10c'),
]

PART_TWO += romans(P2, '11A', 14, L(14, 'Population Dynamics'),
                   (L(14, 'Examine the population pyramid above showing the predicted population structure for',
                      'following questions.'),),
                   ID + 'p2-q11a', ('page',), [
    ('(i)', 2, L(14, '(i) What percentage of the male population is predicted to be in the 0-4 age group?'),
     S(38, '(i) · 2.6', '(ii) · 3'), (fixed('Percentage', 2, '(i) · 2.6 (%) · 2 marks'),), '4-0', POP),
    ('(ii)', 2, L(14, '(ii) What percentage of the female population is predicted to be in the 50-54 age group?'),
     S(38, '(ii) · 3 (%)', '(iii) · 7.8'), (fixed('Percentage', 2, '(ii) · 3 (%) · 2 marks'),), '4-0', POP),
    ('(iii)', 4, L(14, '(iii) Calculate the percentage of the total population', 'group?'),
     S(38, '(iii) · 7.8', '(iv) · Females'), (fixed('Calculation', 4, '(iii) · 7.8 (%) · 4 marks'),), '4-0', POP),
    ('(iv)', 4, L(14, '(iv) Which gender is predicted to live longest?', 'to support your answer.'),
     S(38, '(iv) · Females', '(v) · Valid'),
     (fixed('Gender', 2, '(iv) · Females · 2 marks'), fixed('Evidence', 2, 'Valid piece of evidence · 2 marks')),
     '4-0', POP),
    ('(v)', 4, L(14, '(v) Explain briefly one reason why life expectancy is predicted to be longer in 2050.'),
     S(38, '(v) · Valid explanation', '(vi) · Valid'), (pair('(v) · Valid explanation · 2 + 2 marks', 'Reason'),),
     '4-0', POP),
    ('(vi)', 4, L(14, '(vi) Explain briefly one challenge resulting from this predicted longer life expectancy.'),
     S(38, '(vi) · Valid explanation', None), (pair('(vi) · Valid explanation · 2 + 2 marks', 'Challenge'),),
     '4-1', POP),
])

REASON = ('Three reasons @ 10 marks each', 'For each reason:', 'Reason stated · 2 marks',
          'Map evidence · 2 marks', f'Explanation · 3 x {SRPS}')
PART_TWO += [
    T('p2-11b', P2, '11B', '', 30, 14, L(14, 'Development of Towns'),
      (L(14, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper.',
         'to support each reason.'),),
      (S(39, 'Three reasons @ 10 marks each', 'Annotation'),),
      tuple(Criterion(f'Reason {n}', 10, evens(10), 'srp', REASON) for n in (1, 2, 3)),
      '4-3', URB + MAP, ID + 'p2-q11b', ('map', 'legend')),
    T('p2-11c', P2, '11C', '', 30, 14, L(14, 'Developing World Cities'),
      (L(14, 'Problems can develop as urban centres expand.', 'that you have studied.'),),
      (S(40, 'Problems identified · 2 + 2 marks', 'Annotation'),),
      (pair('Problems identified · 2 + 2 marks', 'Problems identified'),
       fixed('Developing world city', 2, 'Developing world city · 2 marks'),
       srp('Discussion', 12, f'Discussion · 12 x {SRPS}')),
      '4-5', URB, ID + 'p2-q11c'),
]

PART_TWO += romans(P2, '12A', 15, L(15, 'Urban Growth'),
                   (L(15, 'Examine the data above showing the projected population growth', 'growing megacities.'),),
                   ID + 'p2-q12a', ('page',), [
    ('(i)', 16, L(15, '(i) Using graph paper, draw a suitable graph to illustrate this data.'),
     S(41, 'Bar Chart · Pie Chart', 'Annotation'), GRAPH, '2-0', TG),
    ('(ii)', 4, L(15, '(ii) Explain briefly one challenge facing these cities.'),
     S(41, 'Valid explanation · 2m + 2m', None), (pair('Valid explanation · 2m + 2m', 'Challenge'),), '4-5', URB),
])

PART_TWO += [
    T('p2-12b', P2, '12B', '', 30, 15, L(15, 'Migration', nth=0),
      (L(15, 'Migration continues to play an important role', 'receiver regions.'),),
      (S(42, 'Impact on donor region identified · 2m', 'Annotation'),),
      (fixed('Impact on donor region identified', 2, 'Impact on donor region identified · 2m'),
       fixed('Impact on receiver region identified', 2, 'Impact on receiver region identified · 2m'),
       split('Examination of the two impacts (6/7 and 7/6 SRPs)', 13,
             f'Examination of impact on donor region · 6/7 x {SRPS}',
             f'Examination of impact on receiver region · 6/7 x {SRPS}')),
      '4-2', POP, ID + 'p2-q12b'),
    T('p2-12c', P2, '12C', '', 30, 15, L(15, 'Changing Urban Functions - Ireland'),
      (L(15, 'Examine how the functions of urban centres can change over time', 'that you have studied.'),),
      (S(43, 'Functions identified · 2 + 2 marks', 'Annotation'),),
      (pair('Functions identified · 2 + 2 marks', 'Functions identified'),
       fixed('Example Irish urban centre', 2, 'Example Irish urban centre · 2 marks'),
       srp('Examination', 12, 'Examination · 12 x SRPs')),
      '4-3', URB, ID + 'p2-q12c'),
]

# ------------------------------------------------------------------ Options --
OC = (S(45, '*Overall Coherence (20 marks)', None, table=True),)


def option(q, page, theme, note_nth, prompt, scheme_page, topic, atlas, after=None, end=None):
    return T(f'p2-{q}', P2, q, '', 80, page, theme, (prompt,),
             (S(scheme_page, 'Number of aspects', end, None, after), *OC),
             (Criterion('Aspects (3 @ 20 marks or 4 @ 15 marks)', 60, upto(60), 'srp',
                        ('Number of aspects', 'Identifying aspect', '8 x SRP')),
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
           L(17, 'Global warming and desertification are environmental issues', 'Discuss.'),
           47, '5-3', GI, after='13.', end='14.'),
    option('14', 17, L(17, 'Global Interdependence'), 0,
           L(17, 'Examine the positive and negative impacts of aid on developing economies.'),
           47, '5-2', GI, after='14.'),
    option('15', 17, L(17, 'Global Interdependence'), 0,
           L(17, 'Discuss how the sustainable use of resources is important', 'development.'), 48, '5-3', GI),
    option('16', 17, L(17, 'Geoecology'), 1,
           L(17, 'Explain how weathering, leaching and podzolisation have impacted', 'soils.'), 49, '6-1', GE,
           after='16.', end='17.'),
    option('17', 17, L(17, 'Geoecology'), 1,
           L(17, 'Biomes are altered by human activity.', 'Discuss.'), 49, '6-3', GE, after='17.'),
    option('18', 17, L(17, 'Geoecology'), 1,
           L(17, 'Examine the influence of mineral matter, air, water and organic matter on soil development.'),
           50, '6-0', GE),
    option('19', 18, L(18, 'Culture and Identity'), 0,
           L(18, 'Examine the importance of language as a cultural indicator.'), 51, '7-0', CI,
           after='19.', end='20.'),
    option('20', 18, L(18, 'Culture and Identity'), 0,
           L(18, 'The existence of different cultural groups within state borders can lead to conflict.',
             'Discuss.'), 51, '7-1', CI, after='20.'),
    option('21', 18, L(18, 'Culture and Identity'), 0,
           L(18, 'Identity as a concept entails a variety of cultural factors.', 'that you have studied.'),
           52, '7-2', CI),
    option('22', 18, L(18, 'The Atmosphere – Ocean Environment'), 1,
           L(18, 'Examine the uneven distribution of solar energy over the earth’s surface.'), 53, '8-1', AO,
           after='22.', end='23.'),
    option('23', 18, L(18, 'The Atmosphere – Ocean Environment'), 1,
           L(18, 'Exchanges of water between oceans and atmosphere', 'Discuss.'), 53, '8-2', AO, after='23.'),
    option('24', 18, L(18, 'The Atmosphere – Ocean Environment'), 1,
           L(18, 'Discuss the characteristics of one distinctive global climate', 'economic development.'),
           54, '8-5', AO),
]

TASKS = [*PART_ONE, *PART_TWO, *OPTIONS]

ID_CORRECTION_REASON = 'No deferred card shipped before this review, so no id is re-scoped.'

# No 2022 Higher deferred card shipped before this review.
LEGACY_IDS: list[str] = []
