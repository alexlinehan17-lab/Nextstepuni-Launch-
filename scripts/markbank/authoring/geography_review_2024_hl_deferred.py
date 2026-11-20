"""Independent review ledger: Leaving Certificate Geography 2024 Higher Level, deferred sitting.

The SEC's deferred examination is a paper of its own. Sources (English
editions, harvested in paper-trail-corpus/deferredexams/2024 and
deferredmarkingschemes/2024, filed by Paper Trail as "<fileid>-deferred";
sizes pinned in EXPECTED_SOURCES and the generated audit): Part One and
Answerbook LC005ALP042EV (48 pages), Part Two LC005ALP043EV (20 pages),
marking scheme LC005ALP000EV (54 pages), and the sitting's own companions:
the 1:50 000 Castlebar map LC005CLP003EV, its legend LC005CLPC00EV and the
Castlebar aerial photograph LC005CLP004EV, published only as a JPEG.

Visual sweep (every page rendered and read on 2026-11-19):
  Part One booklet p1 cover; p2 instructions (Part One "Attempt any TEN",
  80 marks; Part Two "attempt FOUR", 320 marks); p3-p13 Questions 1-12 (p9
  holds Q7 and Q8); p14 Part Two answerbook instructions; p15-p18 graph
  paper; p19-p47 lined answer pages; p48 back cover and copyright notice.
  Part Two booklet p1 cover; p2 Part Two instructions; p3-p8 Sections 1-2
  (Q1-Q6); p9 Section 3 divider; p10-p15 Electives (Q7-Q12); p16 Section 4
  divider and note; p17-p18 Options (Q13-Q24); p19-p20 "Do not hand this up"
  and the copyright notice.
  Scheme p1 cover; p2 the note on deferred marking schemes; p3 Part One
  table (two columns, Q1-Q6 and Q7-Q12), running on to the top of p4 (Q6(iv)
  and Q12(iv)); p4-p22 Q1-Q6 (each reprints its question; no annotation
  tables); p23 Electives divider; p24-p41 Q7-Q12; p42 Options divider and
  note; p43-p46 Q13-Q24; p47-p51 Geographical Investigation (coursework);
  p52 investigation topics; p53 Irish-language bonus marks; p54 blank.
  Companions: Castlebar map extract (Lough Rusheen, Lannagh/Castlebar
  Lough, the N5); OS legend sheet; oblique aerial photograph of Castlebar.

This deferred scheme was "finalised only for the questions attempted by the
candidates" (its p2 note) and prints no allocation for 10C, 12B, 12C and
options 13, 14, 15, 18, 20, 21, 22, 23 and 24: it reprints each question
and its tariff and nothing more. Each is carded with one row, "The scheme
prints no answer for this part.", whose guidance is that note (p2), so the
student marks it on its printed tariff and the scheme's own reason is
shown. Every other part carries its published allocation. The Part One
table prints Q2's and Q4's two parts side by side (letter and setting,
location and photograph); each part reads its own column. It numbers Q1's
(ii) and (iii) "(ii) (a)" and "(b)", and Q4's (iii) "(ii)"; each is placed
by its wording. Q9 prints the four locations with no per-row marks (the
question's 8 marks), so it is one criterion. 2A prices (v) at 2 and (vi) at
4, as printed. The options' Overall Coherence is "20 marks graded*" with no
descriptor table in this scheme, so its marks are not stepped. Finite
printed choices are routes: 2B, 4B, 9C, 10C and 14 one of the printed
bullets; 3C (i) or (ii), with (i)'s one fluvial or one coastal or one
glacial landform. Choose-N-of-M pools are one card with every printed item
(10B any two, 11B two of three, 15 three of four). 3B "the coastal
landscape and/or the fluvial landscape" is open (either or both), one card.
"""

from geography_review import (
    Criterion, Lift, Route, SchemeSlice, Task, evens, fixed, slug, srp, sums, upto,
)

YEAR = 2024
LEVEL = 'higher'
REVIEWED_AT = '2026-11-19'
PAPER_PAGES = {1: 48, 2: 20}
SCHEME_PAGES = 54
QUESTION_TARIFFS = {1: {str(n): 8 for n in range(1, 13)},
                    2: {**{f'{n}{x}': (20 if x == 'A' else 30)
                           for n in range(1, 13) for x in 'ABC'},
                        **{str(n): 80 for n in range(13, 25)}}}

EXPECTED_SOURCES = {
    'paper1': ('LC005ALP042EV.pdf', 3688449),
    'paper2': ('LC005ALP043EV.pdf', 1321410),
    'scheme': ('LC005ALP000EV.pdf', 972404),
    'map': ('LC005CLP003EV.pdf', 4631383),
    'legend': ('LC005CLPC00EV.pdf', 890021),
    'aerial': ('LC005CLP004EV.jpg', 4932403),
}

PAGE_REVIEW = {
    'paper1': {1: 'cover', 2: 'instructions', **{p: 'question' for p in range(3, 14)},
               14: 'answerbook instructions', **{p: 'graph-paper answer page' for p in range(15, 19)},
               **{p: 'lined answer page' for p in range(19, 48)}, 48: 'copyright/back cover'},
    'paper2': {1: 'cover', 2: 'Part Two instructions',
               **{p: 'question' for p in (3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15, 17, 18)},
               9: 'section divider', 16: 'section divider and option note',
               19: 'do not hand this up', 20: 'copyright/back cover'},
    'scheme': {1: 'cover', 2: 'note on deferred marking schemes', 3: 'Part One table',
               **{p: 'Part Two allocation' for p in range(4, 23)}, 23: 'section divider',
               **{p: 'Part Two allocation' for p in range(24, 42)}, 42: 'section divider and option note',
               **{p: 'option allocation' for p in range(43, 47)},
               **{p: 'geographical investigation (coursework)' for p in range(47, 52)},
               52: 'investigation topics', 53: 'Irish-language bonus marks', 54: 'blank'},
}

EXPECTED_SELECTION_SCAN = [
    [1, 2, 'attempt any ten'], [1, 2, 'attempt four'], [1, 3, 'attempt any ten'],
    [2, 2, 'attempt four'],
    [2, 4, 'one of the following'],
    [2, 5, 'answer (i) or (ii)'], [2, 5, 'or one'], [2, 5, 'or one'],
    [2, 6, 'one of the following'],
    [2, 12, 'one of the following'],
    [2, 13, 'any two'], [2, 13, 'any one'],
    [2, 14, 'two of the following'],
    [2, 17, 'any one'], [2, 17, 'three of the following'],
]
SELECTION_REVIEW = [
    {'scan': [[1, 2, 'attempt any ten'], [1, 2, 'attempt four'], [1, 3, 'attempt any ten'],
              [2, 2, 'attempt four']],
     'kind': 'exam-attempt-rule',
     'reason': 'Part One any ten of twelve and Part Two four questions are attempt rules; every question is carded.'},
    {'scan': [[2, 4, 'one of the following'], [2, 6, 'one of the following'], [2, 12, 'one of the following'],
              [2, 13, 'any one'], [2, 17, 'any one']],
     'kind': 'closed-choose-one',
     'reason': '2B one of three printed impacts -> 3 routes; 4B one of two printed indicators -> 2 routes; '
               '9C one of three printed activities -> 3 routes; 10C any one of three printed factors -> 3 '
               'routes; 14 any one of three printed issues -> 3 routes.'},
    {'scan': [[2, 5, 'answer (i) or (ii)'], [2, 5, 'or one'], [2, 5, 'or one']], 'kind': 'closed-route',
     'reason': '3C: (i) or (ii); (i) offers one fluvial OR one coastal OR one glacial landform -> 4 routes.'},
    {'scan': [[2, 13, 'any two'], [2, 14, 'two of the following'], [2, 17, 'three of the following']],
     'kind': 'choose-n-one-card',
     'reason': '10B any two of three printed problems, 11B two of three printed land-uses and 15 three of '
               'four printed themes -> one card each with every printed item (choice is not a route; the '
               'scheme marks each chosen item alike). Open choices are not fanned out: "one urban area", '
               '"one multi-national company", "example(s)", "one global climate type"; 3B "and/or" is '
               'open. Compulsory lists stay whole: 1A, 4A, 7A and 10A each bullet, 6B both challenges, 17 '
               'each activity.'},
]

P1, P2 = 1, 2
LEFT = (0.0, 0.0, 0.5, 1.0)
RIGHT = (0.5, 0.0, 1.0, 1.0)
ID = 'geography-2024-hl-deferred-'
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


FOOT = 'Leaving Certificate Examination 2024'
L_COL = (55, 312, 144, 365)
R_COL = (149, 312, 300, 365)

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
LANDUSE = (H + 'urban-land-uses',)
ECON = (H + 'elective-economic',)
DEV = (H + 'economic-developing-economies',)
MNC = (H + 'economic-multinationals-globalisation',)
EU = (H + 'economic-european-union',)
ENV = (H + 'economic-environmental-impact',)
ENERGY = (H + 'economic-energy',)

TICK = L(3, 'Answer the questions below by ticking (✓) the correct box for each.')
Q1S = (L(3, 'Examine the diagram above and answer the following questions.'),)
Q2S = (L(4, 'Examine the photographs above and answer the following questions.'),)
Q2_ROWS = (L(4, 'Slumping'), L(4, 'Compression'), L(4, 'Braiding'), L(4, 'Avalanche'))
Q3S = (L(5, 'Examine the 1:50 000 Ordnance Survey map extract above', 'questions.'),)
Q4S = (L(6, 'Examine the map of Ireland and the photographs of rocks above', 'following questions.'),)
Q4_ROWS = (L(6, 'Sandstone'), L(6, 'Granite'), L(6, 'Basalt'))
PART_ONE = [
    T('p1-1-i', P1, '1', '(i)', 4, 3, L(3, 'Landscape Identification'),
      (L(3, '(i) Match each of the letters, A, B, C and D in the diagram above', 'table below.'),),
      (S(3, '(i) B Fault scarp', None, clip(55, 226, 200, 277)),),
      rows(['(i) B Fault scarp 1m', 'D Focus 1m', 'C Epicentre 1m', 'A Seismic wave 1m']),
      '0-7', EV, ID + 'p1-q1', ('page',), Q1S,
      row_labels=(L(3, 'Fault scarp'), L(3, 'Focus'), L(3, 'Epicentre'), L(3, 'Seismic wave'))),
    T('p1-1-ii', P1, '1', '(ii)', 2, 3, L(3, 'Landscape Identification'),
      (TICK, L(3, '(ii) What is the instrument used to measure the strength of an earthquake known as?'),
       L(3, 'Barograph Tiltmeter Seismograph')),
      (S(3, '(ii) (a) Seismograph', None, clip(55, 277, 200, 289)),),
      (fixed('Instrument', 2, '(ii) (a) Seismograph 2m'),), '0-7', EV, ID + 'p1-q1-ii', ('page',), Q1S),
    T('p1-1-iii', P1, '1', '(iii)', 2, 3, L(3, 'Landscape Identification'),
      (TICK, L(3, '(iii) Which of the following types of fault is shown in the diagram above?'),
       L(3, 'Normal Fault Reverse Fault Transverse Fault')),
      (S(3, '(b) Normal Fault', None, clip(55, 289, 200, 301)),),
      (fixed('Type of fault', 2, '(b) Normal Fault 2m'),), '0-2', RW + EV, ID + 'p1-q1-iii', ('page',), Q1S),
    T('p1-2-i', P1, '2', '(i)', 4, 4, L(4, 'Physical Processes'),
      (L(4, '(i) Match each of the photographs, A, B, C and D with the process', 'table below.'),),
      (S(3, 'B Slumping', None, clip(*L_COL)),),
      rows(['B Slumping 1m', 'C Compression 1m', 'D Braiding 1m', 'A Avalanche 1m']),
      '0-4', RW + SEA + RIVERS, ID + 'p1-q2', ('page',), Q2S, row_labels=Q2_ROWS),
    T('p1-2-ii', P1, '2', '(ii)', 4, 4, L(4, 'Physical Processes'),
      (L(4, '(ii) Indicate, by ticking (✓) the correct box, whether each of the processes', 'mass movement setting.'),),
      (S(3, '& Mass movement 1m', None, clip(149, 305, 300, 327)), S(3, '& Coastal 1m', None, clip(149, 327, 300, 365))),
      rows(['=& Mass movement 1m@0', '& Coastal 1m', '& Fluvial 1m', '=& Mass movement 1m@1']),
      '0-4', RW + SEA + RIVERS, ID + 'p1-q2-ii', ('page',), Q2S, row_labels=Q2_ROWS),
    T('p1-3-i', P1, '3', '(i)', 4, 5, L(5, 'Landscape Identification'),
      (L(5, '(i) Match each of the features, A, B, C and D on the map', 'table below.'),),
      (S(3, '(i) · C Arete', '(ii) · Southeast', clip(55, 386, 300, 460)),),
      rows(['(i) · C Arete 1m', 'A Lagoon 1m', 'D Corrie Lake/Tarn 1m', 'B Confluence 1m']),
      '2-6', MAP + GLAC + SEA, ID + 'p1-q3', ('page',), Q3S,
      row_labels=(L(5, 'Arête'), L(5, 'Lagoon'), L(5, 'Corrie lake/tarn'), L(5, 'Confluence'))),
    T('p1-3-ii', P1, '3', '(ii)', 2, 5, L(5, 'Landscape Identification'),
      (L(5, '(ii) In which direction is the river flowing from the feature labelled D?'),),
      (S(3, '(ii) · Southeast', '(iii) · Coastal', clip(55, 386, 300, 460)),),
      (fixed('Direction', 2, '(ii) · Southeast/south-southeast 2m'),), '2-6', MAP, ID + 'p1-q3-ii', ('page',), Q3S),
    T('p1-3-iii', P1, '3', '(iii)', 2, 5, L(5, 'Landscape Identification'),
      (L(5, '(iii) Which of the following processes is primarily involved', 'correct box.'),
       L(5, 'Glacial Fluvial Coastal')),
      (S(3, '(iii) · Coastal', None, clip(55, 386, 300, 460)),),
      (fixed('Process', 2, '(iii) · Coastal 2m'),), '0-10', SEA, ID + 'p1-q3-iii', ('page',), Q3S),
    T('p1-4-i', P1, '4', '(i)', 3, 6, L(6, 'Rocks in Ireland'),
      (L(6, '(i) Match each of the locations on the map, A, B and C', 'most associated with it.'),),
      (S(3, '(i) · B Sandstone', None, clip(55, 486, 186, 520)),),
      rows(['(i) · B Sandstone 1m', 'C Granite 1m', 'A Basalt 1m']),
      '0-1', RW, ID + 'p1-q4', ('page',), Q4S, row_labels=Q4_ROWS),
    T('p1-4-ii', P1, '4', '(ii)', 3, 6, L(6, 'Rocks in Ireland'),
      (L(6, '(ii) Match each of the photographs, 1, 2 and 3', 'best matches it.'),),
      (S(3, '& 2 1m', None, clip(190, 486, 300, 520)),),
      rows(['& 2 1m', '& 1 1m', '& 3 1m']),
      '0-1', RW, ID + 'p1-q4-ii', ('page',), Q4S, row_labels=Q4_ROWS),
    T('p1-4-iii', P1, '4', '(iii)', 2, 6, L(6, 'Rocks in Ireland'),
      (L(6, '(iii) Name the metamorphic rock that is formed when sandstone', 'heat and pressure.'),),
      (S(3, '(ii) · Quartzite', None, clip(55, 520, 300, 536)),),
      (fixed('Metamorphic rock', 2, '(ii) · Quartzite 2m'),), '0-1', RW, ID + 'p1-q4-iii', ('page',), Q4S),
    T('p1-5', P1, '5', '', 8, 7, L(7, 'Concept of a Region'),
      (L(7, 'Complete the table below by matching each of the examples of regions', 'in the table.'),
       L(7, 'Examples of Regions:'), Lift(7, 'Cool Temperate Oceanic', 'Munich', row=True)),
      (S(3, 'Climatic Cool Temperate Oceanic', None, clip(55, 555, 300, 700)),),
      (fixed('Climatic region', 1, 'Climatic Cool Temperate Oceanic 1m'),
       fixed('Geomorphological region', 1, 'Geomorphological Antrim'),
       fixed('Administrative region in Ireland', 1, 'Administrative/Ireland Wicklow County Council 1m'),
       fixed('Core region', 1, ('Core Paris Basin', '=1m@0')),
       fixed('Urban region', 1, ('Urban Munich', '=1m@1')),
       fixed('Cultural region in Ireland', 1, 'Cultural/Ireland Gaeltacht 1m'),
       fixed('Peripheral region', 1, ('Peripheral Mezzogiorno', '=1m@2')),
       fixed('Administrative region in France', 1, 'Administrative/France Pas de Calais Department 1m')),
      '1-0', IRL + EURO, ID + 'p1-q5', ('page',),
      row_labels=(L(7, 'Climatic region'), L(7, 'Geomorphological region'), L(7, 'Administrative region in Ireland'),
                  L(7, 'Core region'), L(7, 'Urban region'), L(7, 'Cultural region in Ireland'),
                  L(7, 'Peripheral region'), L(7, 'Administrative region in France'))),
]

PART_ONE += romans(P1, '6', 8, L(8, 'Weather Map'),
                   (L(8, 'Examine the weather map above and answer each of the following questions.',
                      'correct box for each.'),),
                   ID + 'p1-q6', ('page',), [
    ('(i)', 2, L(8, '(i) The barometric pressure over the area labelled X is 1026', 'hectopascals/millibars.'),
     S(3, '(i) True 2m', '(ii) False', clip(55, 715, 300, 760)), (fixed('True or false', 2, '(i) True 2m'),), '2-7', WX),
    ('(ii)', 2, L(8, '(ii) There is a cold front over the area labelled Y.'),
     S(3, '(ii) False 2m', '(iii) False', clip(55, 715, 300, 760)), (fixed('True or false', 2, '(ii) False 2m'),),
     '2-7', WX),
    ('(iii)', 2, L(8, '(iii) Ireland is experiencing strong winds.'),
     S(3, '(iii) False 2m', None, clip(55, 715, 300, 760)), (fixed('True or false', 2, '(iii) False 2m'),),
     '2-7', WX),
    ('(iv)', 2, L(8, '(iv) Lines on a weather map that join areas of equal atmospheric', 'are called isobars.'),
     S(4, '(iv) True 2m', None, clip(0, 0, 297, 84)), (fixed('True or false', 2, '(iv) True 2m'),), '2-7', WX),
])

Q7_COL = clip(300, 225, 595, 275)
PART_ONE += romans(P1, '7', 9, L(9, 'Map Skills'),
                   (L(9, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper and',
                      'following questions.'),),
                   ID + 'p1-q7', ('map', 'legend'), [
    ('(i)', 2, L(9, '(i) What is the height, in metres, at the triangulation pillar at M 098 983?'),
     S(3, '(i) · 430', '(ii) · 5.6', Q7_COL), (fixed('Height', 2, '(i) · 430 (m) 2m'),), '2-6', MAP),
    ('(ii)', 2, L(9, '(ii) Measure the length, in kilometres, of the entire railway line.'),
     S(3, '(ii) · 5.6', '(iii) · Coniferous', Q7_COL), (fixed('Length', 2, '(ii) · 5.6 (kms) 2m'),), '2-6', MAP),
    ('(iii)', 2, L(9, '(iii) Name the type of forestry at M 10 97.'),
     S(3, '(iii) · Coniferous', '(iv) · 14', Q7_COL), (fixed('Forestry', 2, '(iii) · Coniferous 2m'),), '2-6', MAP),
    ('(iv)', 2, L(9, '(iv) Calculate the approximate area of the map extract', 'National Primary Road.'),
     S(3, '(iv) · 14', None, Q7_COL), (fixed('Area', 2, '(iv) · 14 (Km 2) 2m'),), '2-6', MAP),
])

Q8_COL = clip(300, 310, 595, 365)
PART_ONE += romans(P1, '8', 9, L(9, 'Aerial Photograph and Ordnance Survey Map'),
                   (L(9, 'Examine the aerial photograph of Castlebar and the 1:50 000', 'following questions.'),),
                   ID + 'p1-q8', ('aerial', 'map', 'legend'), [
    ('(i)', 2, L(9, '(i) In what direction was the camera pointed', 'was taken?'),
     S(3, '(i) · South East', '(ii) · Saleen', Q8_COL), (fixed('Direction', 2, '(i) · South East 2m'),), '2-8', AER),
    ('(ii)', 2, (L(9, '(ii) Which of the following lakes can be seen', 'Tick (✓) the correct box.'),
                 L(9, 'Lough Mallard Saleen Lough Tuckers Lough')),
     S(3, '(ii) · Saleen Lough', '(iii) M 145', Q8_COL), (fixed('Lake', 2, '(ii) · Saleen Lough 2m'),), '2-8', AER + MAP),
    ('(iii)', 2, L(9, '(iii) Give a six-figure grid reference for the large church', 'photograph.'),
     S(3, '(iii) M 145 903', '(iv) Castlebar', Q8_COL), (fixed('Grid reference', 2, '(iii) M 145 903 2m'),),
     '2-8', AER + MAP),
    ('(iv)', 2, L(9, '(iv) What is the name of the river', 'aerial photograph?'),
     S(3, '(iv) Castlebar river', None, Q8_COL), (fixed('River', 2, '(iv) Castlebar river 2m'),), '2-8', AER + MAP),
])

PART_ONE += [
    T('p1-9', P1, '9', '', 8, 10, L(10, 'Aerial Photographs'),
      (L(10, 'Locate each of the features labelled A, B, C, D and E above', 'completed for you.'),),
      (S(3, 'B Left background', None, clip(300, 385, 595, 433)),),
      (Criterion('Locations of B, C, D and E', 8, upto(8), 'exact',
                 ('B Left background', 'C Right middleground', 'D Right foreground', 'E · Centre middleground')),),
      '2-8', AER, ID + 'p1-q9', ('page', 'aerial'),
      (L(10, 'Examine the oblique aerial photograph of Castlebar accompanying this paper and the',
         'of Castlebar below.'),)),
]

Q10_COL = clip(300, 484, 595, 536)
PART_ONE += romans(P1, '10', 11, L(11, 'Graphical Interpretation'),
                   (L(11, 'Examine the infographic above showing the highest levels of education', 'following questions.'),),
                   ID + 'p1-q10', ('page',), [
    ('(i)', 2, L(11, '(i) What percentage of people aged between 25 and 64 years had primary only', 'formal education?'),
     S(3, '(i) 3 (%)', '(ii) 25', Q10_COL), (fixed('Percentage', 2, '(i) 3 (%) 2m'),), '2-0', TG),
    ('(ii)', 2, L(11, '(ii) What percentage of people in Dublin', 'secondary school education only?'),
     S(3, '(ii) 25 (%)', '(iii) Above', Q10_COL), (fixed('Percentage', 2, '(ii) 25 (%) 2m'),), '2-0', TG),
    ('(iii)', 2, L(11, '(iii) Was Ireland’s percentage of people with third level education', '27 average?'),
     S(3, '(iii) Above', '(iv) Any valid', Q10_COL), (fixed('Above or below', 2, '(iii) Above 2m'),), '2-0', TG),
    ('(iv)', 2, L(11, '(iv) Briefly explain one benefit for Ireland', 'third level education.'),
     S(3, '(iv) Any valid explanation', None, Q10_COL),
     (fixed('Explanation', 2, '(iv) Any valid explanation 1m + 1m', (0, 1, 2)),), '1-4', IRL),
])

Q11_COL = clip(300, 555, 595, 610)
PART_ONE += romans(P1, '11', 12, L(12, 'Statistical Interpretation'),
                   (L(12, 'Examine the Human Development Index statistics above and answer the following', 'questions.'),),
                   ID + 'p1-q11', ('page',), [
    ('(i)', 2, L(12, '(i) Which country has a life expectancy at birth of 76.5 years?'),
     S(3, '(i) · Poland', '(ii) · 6.7', Q11_COL), (fixed('Country', 2, '(i) · Poland 2m'),), '2-0', TG),
    ('(ii)', 2, L(12, '(ii) What is the mean number of years of schooling in India?'),
     S(3, '(ii) · 6.7', '(iii) · 75,401', Q11_COL), (fixed('Years', 2, '(ii) · 6.7 2m'),), '2-0', TG),
    ('(iii)', 2, L(12, '(iii) Calculate the difference in income ($) between the country with the highest', 'per capita.'),
     S(3, '(iii) · 75,401', '(iv) · False', Q11_COL), (fixed('Difference', 2, '(iii) · 75,401 2m'),), '2-0', TG),
    ('(iv)', 2, (L(12, '(iv) Ireland has the highest rank in each of the three categories', 'table above.'),
                 L(12, 'Tick (✓) the correct box.')),
     S(3, '(iv) · False', None, Q11_COL), (fixed('True or false', 2, '(iv) · False 2m'),), '2-0', TG),
])

PART_ONE.append(T(
    'p1-12', P1, '12', '', 8, 13, L(13, 'Satellite Imagery'),
    (L(13, 'Match each of the letters, A, B, C and D on the images', 'best matches it.'),),
    (S(3, '(i) · B 2m', None, clip(300, 715, 595, 760)), S(4, '(iv) · A 2m', None, clip(300, 0, 595, 84))),
    rows(['(i) · B 2m', '(ii) · D 2m', '(iii) · C 2m', '(iv) · A 2m'], 2),
    '2-8', AER, ID + 'p1-q12', ('page',), (L(13, 'Examine the satellite images below and answer the following question.'),),
    row_labels=(L(13, 'Deforestation'), L(13, 'Volcanic eruption'), L(13, 'Delta'), L(13, 'Forest fires'))))

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
         # This scheme wraps the item allocation's grading onto a line of its own.
         fixed('6 items illustrated', 12, ('6 items illustrated', 'graded (2/1/0)'), upto(12)))


def bullet_routes(prefix, items, atlas=None):
    return tuple(Route(slug(item, 34), item.rstrip('.'), ID + prefix + slug(item, 34), False,
                       keep_bullets=(item,), atlas=(atlas[item] if atlas else None))
                 for item in items)


def first_route(prefix, item):
    return ID + prefix + slug(item, 34)


def split(label, total, first, second):
    """One allocation printed as two parts examined 7/6 and 6/7 SRPs."""
    return srp(label, total, (first, second))



SKETCH_ALLOC = ('4 features @ 4 marks each', 'Named 1 mark')


def proportion_sketch():
    """The 2024 scheme heads the sketch outline "Proportion · 4 marks (Graded 4/0)"."""
    return (fixed('Proportion (sketch outline)', 4, 'Proportion · 4 marks (Graded 4/0)', (0, 4)),
            *(Criterion(f'Feature {n}', 4, sums((0, 1, 3), (0, 1)), 'exact', SKETCH_ALLOC) for n in (1, 2, 3, 4)))


LANDFORMS = 'one fluvial landform or one coastal landform or one glacial landform'
SURFACE = ('The impact of flood control measures on river processes',
           'The impact of coastal defence measures on coastal processes',
           'The impact of human activities on mass movement processes.')
CULTURE = ('Language', 'Religion.')
DEVELOPED = ('Footloose industries', 'Financial services', 'Mass tourism.')
POPULATION = ('Development of resources', 'Income levels', 'Society and culture.')
ISSUES = ('Global warming', 'Deforestation', 'Desertification.')

PART_TWO = [
    T('p2-1a', P2, '1A', '', 20, 3, L(3, 'Ordnance Survey Map'),
      (L(3, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper.', 'Castlebar Lough.'),),
      (S(4, 'Proportion', FOOT),), proportion_sketch(), '2-6', MAP, ID + 'p2-q1a', ('map', 'legend'),
      row_labels=(None, L(3, 'The entire area of Lough Rusheen in the centre of the map'),
                  L(3, 'The entire area of land above 300 metres west of Easting 12'),
                  L(3, 'An area of deciduous woodland in the southwest of the map'),
                  L(3, 'The entire course of the Castlebar River', 'Castlebar Lough.'))),
    T('p2-1b', P2, '1B', '', 30, 3, L(3, 'Metamorphic Rocks'),
      (L(3, 'Examine the formation of metamorphic rocks, with reference to examples from Ireland.'),),
      (S(5, 'Metamorphic rock named', FOOT),),
      (pair('Metamorphic rock named · 2 + 2 marks', 'Metamorphic rocks named'),
       srp('Examination of formation', 13, f'Examination of formation · 13 x {SRPS}')),
      '0-1', RW, ID + 'p2-q1b'),
    T('p2-1c', P2, '1C', '', 30, 3, L(3, 'Plate Boundaries'),
      (L(3, 'Describe and explain destructive plate boundaries', 'studied.'),),
      (S(6, f'Description/Explanation · 15 x {SRPS}', FOOT),),
      (srp('Description/explanation', 15, f'Description/Explanation · 15 x {SRPS}'),),
      '0-0', PS, ID + 'p2-q1c'),
]

PART_TWO += romans(P2, '2A', 4, L(4, 'Karst Landscapes'),
                   (L(4, 'Examine the diagram above showing a karst landscape', 'questions.'),),
                   ID + 'p2-q2a', ('page',), [
    ('(i)', 4, L(4, '(i) Name each of the surface features labelled A and B in the diagram above.'),
     S(7, '(i) · A · Clint', '(ii) · C'),
     (fixed('A', 2, '(i) · A · Clint · 2 marks'), fixed('B', 2, 'B · Grike · 2 marks')), '0-3', KARST),
    ('(ii)', 6, L(4, '(ii) Name the underground features labelled C, D and E in the diagram above.'),
     S(7, '(ii) · C · Stalactite', '(iii) · False'),
     (fixed('C', 2, '(ii) · C · Stalactite · 2 marks'), fixed('D', 2, 'D · Stalagmite · 2 marks'),
      fixed('E', 2, 'E · Pillar/Column · 2 marks')), '0-3', KARST),
    ('(iii)', 2, (L(4, '(iii) State whether the following statement is true or false:'),
                  L(4, 'The type of river at F is a river of resurgence.')),
     S(7, '(iii) · False', '(iv) · Carbonation'), (fixed('True or false', 2, '(iii) · False · 2 marks'),), '0-3', KARST),
    ('(iv)', 2, L(4, '(iv) Name the type of chemical weathering most associated', 'landscape.'),
     S(7, '(iv) · Carbonation', '(v) · Any valid'), (fixed('Weathering', 2, '(iv) · Carbonation · 2 marks'),),
     '0-3', KARST),
    ('(v)', 2, L(4, '(v) State what is meant by the term permeable rock.'),
     S(7, '(v) · Any valid explanation', '(vi) · Joints'), (fixed('Explanation', 2, '(v) · Any valid explanation · 2 marks'),),
     '0-3', KARST),
    ('(vi)', 4, L(4, '(vi) What is the term given to vertical cracks found in limestone?'),
     S(7, '(vi) · Joints', FOOT), (fixed('Term', 4, '(vi) · Joints · 4 marks'),), '0-3', KARST),
])

PART_TWO += [
    T('p2-2b', P2, '2B', '', 30, 4, L(4, 'Human Interaction with Surface Processes'),
      (L(4, '‘Human activity impacts on surface processes.’', 'mass movement processes.'),),
      (S(8, 'Impact on process identified · 2 marks', FOOT),),
      (fixed('Impact on process identified', 2, 'Impact on process identified · 2 marks'),
       srp('Examination', 14, f'Examination · 14 x {SRPS}')),
      '0-6', RW, first_route('p2-q2b-', SURFACE[0]),
      routes=bullet_routes('p2-q2b-', SURFACE, atlas=dict(zip(SURFACE, (RIVERS, SEA, RW))))),
    T('p2-2c', P2, '2C', '', 30, 4, L(4, 'Tectonic Activity – Irish Landscape'),
      (L(4, 'Examine the impact of tectonic activity on the Irish landscape.'),),
      (S(9, 'Impact of tectonic activity on the Irish landscape identified', FOOT),),
      (fixed('Impact identified', 2, 'Impact of tectonic activity on the Irish landscape identified · 2 marks'),
       srp('Examination', 14, f'Examination · 14 x {SRPS}')),
      '0-0', PS + RW, ID + 'p2-q2c'),
]

PART_TWO += romans(P2, '3A', 5, L(5, 'Structure of the Earth'),
                   (L(5, 'Examine the diagram of the structure of the earth above', 'questions.'),),
                   ID + 'p2-q3a', ('page',), [
    ('(i)', 8, L(5, '(i) Name each of the layers of the earth labelled A, B, C and D.'),
     S(10, '(i) · A · Crust', '(ii) · Any valid'),
     (fixed('A', 2, '(i) · A · Crust · 2 marks'), fixed('B', 2, 'B · Inner core · 2 marks'),
      fixed('C', 2, 'C · Outer core · 2 marks'), fixed('D', 2, 'D · Mantle · 2 marks')), '0-0', PS),
    ('(ii)', 2, L(5, '(ii) Name one tectonic plate that you have studied.'),
     S(10, '(ii) · Any valid answer', '(iii) · Magma'), (fixed('Tectonic plate', 2, '(ii) · Any valid answer · 2 marks'),),
     '0-0', PS),
    ('(iii)', 2, L(5, '(iii) What is the term for molten rock under the surface of the earth?'),
     S(10, '(iii) · Magma', '(iv) · Iron'), (fixed('Term', 2, '(iii) · Magma · 2 marks'),), '0-7', EV),
    ('(iv)', 2, L(5, '(iv) Name one of the main minerals that make up the part of the earth labelled B above.'),
     S(10, '(iv) · Iron', '(v) · Subduction'), (fixed('Mineral', 2, '(iv) · Iron / Nickel · 2 marks'),), '0-0', PS),
    ('(v)', 2, L(5, '(v) Name the process by which one tectonic plate is forced under another.'),
     S(10, '(v) · Subduction', '(vi) · Any valid'), (fixed('Process', 2, '(v) · Subduction · 2 marks'),), '0-0', PS),
    ('(vi)', 4, L(5, '(vi) Explain briefly how tectonic plates move.'),
     S(10, '(vi) · Any valid explanation', FOOT), (pair('(vi) · Any valid explanation · 2 + 2 marks', 'Explanation'),),
     '0-0', PS),
])

PART_TWO += [
    T('p2-3b', P2, '3B', '', 30, 5, L(5, 'Isostasy'),
      (L(5, 'Examine how isostasy impacts on the coastal landscape and/or on the fluvial landscape.'),),
      (S(11, 'Impact identified · 2 marks', FOOT),),
      (fixed('Impact identified', 2, 'Impact identified · 2 marks'), srp('Examination', 14, f'Examination · 14 x {SRPS}')),
      '0-5', RIVERS + SEA, ID + 'p2-q3b'),
    T('p2-3c', P2, '3C', '', 30, 5, L(5, 'Surface Processes'),
      (L(5, '(i) Examine the role of the processes of erosion', 'that you have studied.'),),
      (S(12, 'Process of erosion identified · 2 marks', FOOT),),
      (fixed('Process of erosion identified', 2, 'Process of erosion identified · 2 marks'),
       fixed('Landform named', 2, 'Landform named · 2 marks'), srp('Examination', 13, f'Examination · 13 x {SRPS}')),
      '0-9', RIVERS, ID + 'p2-q3c-route-i-fluvial-landform',
      routes=(
          Route('route-i-fluvial-landform', 'Route (i) · one fluvial landform',
                ID + 'p2-q3c-route-i-fluvial-landform', False, ((LANDFORMS, 'one fluvial landform'),),
                topic='0-9', atlas=RIVERS),
          Route('route-i-coastal-landform', 'Route (i) · one coastal landform',
                ID + 'p2-q3c-route-i-coastal-landform', False, ((LANDFORMS, 'one coastal landform'),),
                topic='0-10', atlas=SEA),
          Route('route-i-glacial-landform', 'Route (i) · one glacial landform',
                ID + 'p2-q3c-route-i-glacial-landform', False, ((LANDFORMS, 'one glacial landform'),),
                topic='0-11', atlas=GLAC),
          Route('route-ii', 'Route (ii)', ID + 'p2-q3c-route-ii', False,
                prompt=(L(5, '(ii) Describe and explain the factors governing', 'that you have studied.'),),
                scheme=(S(13, 'Factors identified', FOOT),),
                criteria=(pair('Factors identified · 2 + 2 marks', 'Factors identified'),
                          fixed('Mass movement process named', 2, 'Mass movement process named · 2 marks'),
                          srp('Description/explanation', 12, f'Description/explanation · 12 x {SRPS}')),
                topic='0-8', atlas=RW),
      )),
    # Question 4
    T('p2-4a', P2, '4A', '', 20, 6, L(6, 'Map Skills'),
      (L(6, 'Draw an outline map of a Continental / Sub-Continental region that you have studied.',
         'The course of a named river.'),),
      (S(14, 'Map outline', FOOT),),
      sketch('Map outline · 4 marks graded (4/2/0)', (0, 2, 4),
             ('4 features @ 4 marks each', 'Named 2 marks'), sums((0, 1, 2), (0, 2)), 4),
      '1-6', CONT, ID + 'p2-q4a',
      row_labels=(None, L(6, 'The outline of a named feature of relief (upland or lowland)'),
                  L(6, 'A named urban centre'), L(6, 'A named road or rail link'), L(6, 'The course of a named river.'))),
    T('p2-4b', P2, '4B', '', 30, 6, L(6, 'Concept of a Region'),
      (L(6, 'Examine how one of the following can be used to define cultural regions', 'Religion.'),),
      (S(15, 'Example · 2 marks', FOOT),),
      (fixed('Example', 2, 'Example · 2 marks'), srp('Examination', 14, f'Examination · 14 x {SRPS}')),
      '1-3', IRL + EURO + CONT, first_route('p2-q4b-', CULTURE[0]), routes=bullet_routes('p2-q4b-', CULTURE)),
    T('p2-4c', P2, '4C', '', 30, 6, L(6, 'Economic Activity'),
      (L(6, 'Examine two factors that influence the development of one tertiary economic activity',
         'that you have studied.'),),
      (S(16, 'Factors identified · 2 + 2 marks', FOOT),),
      (pair('Factors identified · 2 + 2 marks', 'Factors identified'),
       split('Examination of the two factors (7/6 and 6/7 SRPs)', 13,
             f'Examination of Factor 1 · 7/6 x {SRPS}', f'Examination of Factor 2 · 6/7 x {SRPS}')),
      '1-5', EURO, ID + 'p2-q4c'),
]

PART_TWO += romans(P2, '5A', 7, L(7, 'Transport in the European Union'),
                   (L(7, 'Examine the table above showing passenger numbers in selected EU airports',
                      'following questions.'),),
                   ID + 'p2-q5a', ('page',), [
    ('(i)', 2, L(7, '(i) Which airport had the highest number of passengers in 2019?'),
     S(17, '(i) · Charles de Gaulle', '(ii) · 16'), (fixed('Airport', 2, '(i) · Charles de Gaulle Paris · 2 marks'),),
     '2-0', TG),
    ('(ii)', 2, L(7, '(ii) How many passengers (in millions) did Orly-Paris airport have in 2021?'),
     S(17, '(ii) · 16', '(iii) · Frankfurt'), (fixed('Passengers', 2, '(ii) · 16 (million) · 2 marks'),), '2-0', TG),
    ('(iii)', 4, L(7, '(iii) Name the two airports that had the same number of passengers (in millions) in 2021.'),
     S(17, '(iii) · Frankfurt', '(iv) · 27.3'),
     (pair('(iii) · Frankfurt & Schiphol-Amsterdam · 2 + 2 marks', 'Two airports'),), '2-0', TG),
    ('(iv)', 4, L(7, '(iv) Calculate the mean (average) passenger numbers', '2019, 2020 and 2021.'),
     S(17, '(iv) · 27.3', '(v) · Any valid'), (fixed('Mean', 4, '(iv) · 27.3 (million) · 4 marks'),), '2-0', TG),
    ('(v)', 4, L(7, '(v) Explain briefly one reason why passenger numbers fell in 2020.'),
     S(17, '(v) · Any valid explanation', '(vi) · Any valid'), (pair('(v) · Any valid explanation · 2 + 2 marks', 'Reason'),),
     '1-5', EURO),
    ('(vi)', 4, L(7, '(vi) Explain briefly one reason why air transport is important to Ireland.'),
     S(17, '(vi) · Any valid explanation', FOOT), (pair('(vi) · Any valid explanation · 2 + 2 marks', 'Reason'),),
     '1-4', IRL),
])

PART_TWO += [
    T('p2-5b', P2, '5B', '', 30, 7, L(7, 'Socio-Economic Regions'),
      (L(7, 'Examine the causes and impacts of industrial decline', 'you have studied.'),),
      (S(18, 'Cause identified · 2 marks', FOOT),),
      (fixed('Cause identified', 2, 'Cause identified · 2 marks'), fixed('Impact identified', 2, 'Impact identified · 2 marks'),
       split('Examination of cause and impact (7/6 and 6/7 SRPs)', 13,
             f'Examination of cause · 7/6 x {SRPS}', f'Examination of impact · 6//7 x {SRPS}')),
      '1-1', IRL + EURO, ID + 'p2-q5b'),
    T('p2-5c', P2, '5C', '', 30, 7, L(7, 'Primary Economic Activity - Agriculture'),
      (L(7, 'Account for the development of agriculture in a Continental', 'that you have studied.'),),
      (S(19, f'Examination · 15 x {SRPS}', FOOT),), (srp('Examination', 15, f'Examination · 15 x {SRPS}'),),
      '1-6', CONT, ID + 'p2-q5c'),
]

PART_TWO += romans(P2, '6A', 8, L(8, 'Farm Incomes by farm type', nth=0),
                   (L(8, 'Examine the graphic above which shows family farm incomes by sector', 'following questions.'),),
                   ID + 'p2-q6a', ('page',), [
    ('(i)', 2, L(8, '(i) What was the farm income (in €) for arable farmers in 2020?'),
     S(20, '(i) · €33,300', '(ii) · Cattle'), (fixed('Income', 2, '(i) · €33,300 · 2 marks'),), '2-0', TG),
    ('(ii)', 4, L(8, '(ii) Name two types of farm where income declined from 2021 to 2022.'),
     S(20, '(ii) · Cattle & sheep', '(iii) · €81,000'), (pair('(ii) · Cattle & sheep · 2 + 2 marks', 'Two farm types'),),
     '2-0', TG),
    ('(iii)', 2, L(8, '(iii) By how much (in €) did dairy farm incomes increase between 2019 and 2022?'),
     S(20, '(iii) · €81,000', '(iv) · €1,500'), (fixed('Increase', 2, '(iii) · €81,000 · 2 marks'),), '2-0', TG),
    ('(iv)', 4, L(8, '(iv) Calculate the change in sheep farm income between 2019 and 2022.'),
     S(20, '(iv) · €1,500', '(v) · Any valid'), (fixed('Change', 4, '(iv) · €1,500 · 4 marks'),), '2-0', TG),
    ('(v)', 4, L(8, '(v) Explain briefly what is meant by the term arable farming.'),
     S(20, '(v) · Any valid explanation', '(vi) · Any valid'), (pair('(v) · Any valid explanation · 2 + 2 marks', 'Explanation'),),
     '1-4', IRL),
    ('(vi)', 4, L(8, '(vi) Explain briefly how higher farm incomes benefit Ireland.'),
     S(20, '(vi) · Any valid explanation', FOOT), (pair('(vi) · Any valid explanation · 2 + 2 marks', 'Benefit'),),
     '1-4', IRL),
])

PART_TWO += [
    T('p2-6b', P2, '6B', '', 30, 8, L(8, 'The European Union'),
      (L(8, 'Explain each of the following challenges currently facing the European Union', 'Economic challenges.'),),
      (S(21, 'Social challenge identified · 2 marks', FOOT),),
      (fixed('Social challenge identified', 2, 'Social challenge identified · 2 marks'),
       fixed('Economic challenge identified', 2, 'Economic challenge identified · 2 marks'),
       split('Explanation of the two challenges (7/6 and 6/7 SRPs)', 13,
             f'Explanation of social challenges · 7/6 x {SRPS}', f'Explanation of economic challenges · 6/7 x {SRPS}')),
      '1-5', EURO, ID + 'p2-q6b'),
    T('p2-6c', P2, '6C', '', 30, 8, L(8, 'Urban Development'),
      (L(8, 'Examine the factors that have influenced the development of one urban area', 'have studied.'),),
      (S(22, 'Urban area named · 2 marks', FOOT),),
      (fixed('Urban area named', 2, 'Urban area named · 2 marks'), pair('Factors identified · 2 + 2 marks', 'Factors identified'),
       srp('Examination', 12, f'Examination · 12 x {SRPS}')),
      '1-3', IRL + EURO + CONT, ID + 'p2-q6c'),
    # Question 7
    T('p2-7a', P2, '7A', '', 20, 10, L(10, 'Aerial Photograph'),
      (L(10, 'Examine the aerial photograph of Castlebar accompanying this paper.', 'A sports stadium.'),),
      (S(24, 'Proportion', FOOT),), proportion_sketch(), '2-8', AER, ID + 'p2-q7a', ('aerial',),
      row_labels=(None, L(10, 'A lake'), L(10, 'Two connecting streets'), L(10, 'A carpark in the left foreground'),
                  L(10, 'A sports stadium.'))),
    T('p2-7b', P2, '7B', '', 30, 10, L(10, 'Multinational Company'),
      (L(10, 'Examine how globalisation impacts on world trade', 'which you have studied.'),),
      (S(25, 'Multinational company named · 2 marks', FOOT),),
      (fixed('Multinational company named', 2, 'Multinational company named · 2 marks'),
       fixed('Impact on world trade identified', 2, 'Impact of globalisation on world trade identified · 2 marks'),
       srp('Examination', 13, f'Examination · 13 x {SRPS}')),
      '3-2', MNC, ID + 'p2-q7b'),
    T('p2-7c', P2, '7C', '', 30, 10, L(10, 'European Union Policy'),
      (L(10, 'Examine the impact of European Union policy on the development of primary economic', 'activity in Ireland.'),),
      (S(26, 'Impact on primary activity identified · 2 marks', FOOT),),
      (fixed('Impact on primary activity identified', 2, 'Impact on primary activity identified · 2 marks'),
       srp('Examination', 14, f'Examination · 14 x {SRPS}')),
      '3-3', EU, ID + 'p2-q7c'),
]

PART_TWO += romans(P2, '8A', 11, L(11, 'Energy Consumption', nth=0),
                   (L(11, 'Examine the table above showing European Union (EU) energy consumption', 'following questions.'),),
                   ID + 'p2-q8a', ('page',), [
    ('(i)', 2, L(11, '(i) Which fuel type was used the most in 2006?'),
     S(27, '(i) · Oil', '(ii) · Nuclear'), (fixed('Fuel type', 2, '(i) · Oil · 2 marks'),), '2-0', TG),
    ('(ii)', 4, L(11, '(ii) Name two fuel types that had a decrease', '2006 and 2021.'),
     S(27, '(ii) · Nuclear', '(iii) · 21.9'),
     (pair('(ii) · Nuclear, Oil, Solid fossil fuels (any two) · 2 + 2 marks', 'Two fuel types'),), '2-0', TG),
    ('(iii)', 4, L(11, '(iii) Calculate X, the total energy consumption (%) of natural gas in 2016.'),
     S(27, '(iii) · 21.9', '(iv) · Any valid'), (fixed('Calculation', 4, '(iii) · 21.9 (%) · 4 marks'),), '2-0', TG),
    ('(iv)', 2, L(11, '(iv) Give one example of renewable energy.'),
     S(27, '(iv) · Any valid example', '(v) · Any valid'), (fixed('Example', 2, '(iv) · Any valid example · 2 marks'),),
     '3-5', ENERGY),
    ('(v)', 8, L(11, '(v) Explain briefly two reasons why renewables and biofuels', 'from 2006 to 2021.'),
     S(27, '(v) · Any valid explanation', FOOT),
     (pair('(v) · Any valid explanation · 2 + 2 marks', 'Reason 1'), pair('=2 + 2 marks', 'Reason 2')), '3-5', ENERGY),
])

REASON = ('Three reasons @ 10 marks each', 'For each reason:', 'Reason stated · 2 marks',
          'OS map evidence · 2 marks', f'Discussion · 3 x {SRPS}')
PART_TWO += [
    T('p2-8b', P2, '8B', '', 30, 11, L(11, 'Colonialism'),
      (L(11, 'Examine the challenges resulting from colonialism faced by a developing economy', 'have studied.'),),
      (S(28, 'Challenges identified · 2 + 2 marks', FOOT),),
      (pair('Challenges identified · 2 + 2 marks', 'Challenges identified'),
       fixed('Developing economy named', 2, 'Developing economy named · 2 marks'),
       srp('Examination', 12, f'Examination · 12 x {SRPS}')),
      '3-1', DEV, ID + 'p2-q8b'),
    T('p2-8c', P2, '8C', '', 30, 11, L(11, 'Location of Economic Activity'),
      (L(11, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper and',
         'to support each reason.'),),
      (S(29, 'Three reasons @ 10 marks each', FOOT),),
      tuple(Criterion(f'Reason {n}', 10, evens(10), 'srp', REASON) for n in (1, 2, 3)),
      '2-6', MAP + ECON, ID + 'p2-q8c', ('map', 'legend')),
]

PART_TWO += romans(P2, '9A', 12, L(12, 'Economic Activity', nth=0),
                   (L(12, 'Examine the data above showing the number of new cars registered', 'following questions.'),),
                   ID + 'p2-q9a', ('page',), [
    ('(i)', 16, L(12, '(i) Using graph paper, draw a suitable graph to illustrate this data.'),
     S(30, 'Bar Chart · Pie Chart', '(ii) · Explain briefly'), GRAPH, '2-0', TG),
    ('(ii)', 4, L(12, '(ii) Explain briefly one reason why new car registration', 'economic prosperity.'),
     S(30, 'Any valid explanation · 2 + 2 marks', FOOT), (pair('Any valid explanation · 2 + 2 marks', 'Reason'),),
     '3-0', ECON),
])

PART_TWO += [
    T('p2-9b', P2, '9B', '', 30, 12, L(12, 'Sustainable Development'),
      (L(12, 'Examine how economic activities can be developed sustainably', 'environmental impact.'),),
      (S(31, f'Examination · 15 x {SRPS}', FOOT),), (srp('Examination', 15, f'Examination · 15 x {SRPS}'),),
      '3-4', ENV, ID + 'p2-q9b'),
    T('p2-9c', P2, '9C', '', 30, 12, L(12, 'Economic Activity in a Developed Economy'),
      (L(12, 'Examine the development of one of the following with reference to a developed economy', 'Mass tourism.'),),
      (S(32, 'Developed economy named · 2 marks', FOOT),),
      (fixed('Developed economy named', 2, 'Developed economy named · 2 marks'),
       srp('Examination', 14, f'Examination · 14 x {SRPS}')),
      '3-0', ECON, first_route('p2-q9c-', DEVELOPED[0]), routes=bullet_routes('p2-q9c-', DEVELOPED)),
    # Question 10
    T('p2-10a', P2, '10A', '', 20, 13, L(13, 'Aerial Photograph'),
      (L(13, 'Examine the aerial photograph of Castlebar accompanying this paper.', 'A bridge.'),),
      (S(33, 'Proportion', FOOT),), proportion_sketch(), '2-8', AER + URB, ID + 'p2-q10a', ('aerial',),
      row_labels=(None, L(13, 'A river'), L(13, 'A church'), L(13, 'A roundabout'), L(13, 'A bridge.'))),
    T('p2-10b', P2, '10B', '', 30, 13, L(13, 'Urban Problems'),
      (L(13, 'Discuss how the growth of urban centres can lead to any two of the following problems', 'Urban sprawl.'),),
      (S(34, 'Example of urban centre · 2 marks', FOOT),),
      (fixed('Example of urban centre', 2, 'Example of urban centre · 2 marks'),
       srp('Discussion of problem one', 7, f'Discussion of problem one · 7 x {SRPS}'),
       srp('Discussion of problem two', 7, f'Discussion of problem two · 7 x {SRPS}')),
      '4-5', URB, ID + 'p2-q10b'),
    T('p2-10c', P2, '10C', '', 30, 13, L(13, 'The Dynamics of Population'),
      (L(13, 'Examine the influence / impact of any one of the following factors', 'Society and culture.'),),
      NOTE_SLICE, unprinted(30), '4-0', POP, first_route('p2-q10c-', POPULATION[0]),
      routes=bullet_routes('p2-q10c-', POPULATION)),
]

PART_TWO += romans(P2, '11A', 14, L(14, 'Population Pyramids'),
                   (L(14, 'Examine the population pyramids above and answer the questions that follow.'),),
                   ID + 'p2-q11a', ('page',), [
    ('(i)', 2, L(14, '(i) Which pyramid has a higher percentage of people in the 50-54 age group?'),
     S(36, '(i) · Pyramid B', '(ii) · 0-4'), (fixed('Pyramid', 2, '(i) · Pyramid B · 2 marks'),), '4-0', POP),
    ('(ii)', 2, L(14, '(ii) For Pyramid A, which age group has the highest percentage of the males?'),
     S(36, '(ii) · 0-4', '(iii) · Pyramid A'), (fixed('Age group', 2, '(ii) · 0-4 · 2 marks'),), '4-0', POP),
    ('(iii)', 4, L(14, '(iii) Which population pyramid has a higher death rate', 'support your'),
     S(36, '(iii) · Pyramid A', '(iv) · Pyramid B'),
     (fixed('Pyramid', 2, '(iii) · Pyramid A · 2 Marks'), fixed('Evidence', 2, 'Any valid evidence · 2 marks')), '4-0', POP),
    ('(iv)', 4, L(14, '(iv) Which of the Pyramids, A or B, represents a country', 'developed country.'),
     S(36, '(iv) · Pyramid B', '(v) · Any valid'),
     (fixed('Pyramid', 2, '(iv) · Pyramid B · 2 marks'), fixed('Developed country', 2, 'Valid example · 2 marks')),
     '4-1', POP),
    ('(v)', 8, L(14, '(v) Explain briefly two challenges facing a country', 'Pyramid A.'),
     S(36, '(v) · Any valid explanation', FOOT),
     (pair('(v) · Any valid explanation · 2 + 2 marks', 'Challenge 1'),
      pair('=Any valid explanation · 2 + 2 marks', 'Challenge 2')), '4-1', POP),
])

SETTLEMENT = ('Three reasons for variations in settlement distribution @ 10 marks each',
              'For each of the three reasons:', 'Named reason · 2 marks', 'OS map evidence · 2 marks',
              f'Examination · 3 x {SRPS}')
PART_TWO += [
    T('p2-11b', P2, '11B', '', 30, 14, L(14, 'Urban Land-Use'),
      (L(14, 'Examine how the location of two of the following land-uses has changed', 'Commercial land-use.'),),
      (S(37, 'Named Irish city · 2 marks', FOOT),),
      (fixed('Named Irish city', 2, 'Named Irish city · 2 marks'),
       srp('Examination of land-use 1', 7, f'Examination of land-use 1 · 7 x {SRPS}'),
       srp('Examination of land-use 2', 7, f'Examination of land-use 2 · 7 x {SRPS}')),
      '4-4', LANDUSE + URB, ID + 'p2-q11b'),
    T('p2-11c', P2, '11C', '', 30, 14, L(14, 'Settlement Distribution'),
      (L(14, 'Examine the 1:50 000 Ordnance Survey map of Castlebar accompanying this paper.', 'south of Northing 93.'),),
      (S(38, 'Three reasons for variations', FOOT),),
      tuple(Criterion(f'Reason {n}', 10, evens(10), 'srp', SETTLEMENT) for n in (1, 2, 3)),
      '4-3', URB + MAP, ID + 'p2-q11c', ('map', 'legend')),
]

PART_TWO += romans(P2, '12A', 15, L(15, 'Urban Population'),
                   (L(15, 'Examine the data above showing urban population as a percentage', 'countries in 2020.'),),
                   ID + 'p2-q12a', ('page',), [
    ('(i)', 16, L(15, '(i) Using graph paper, draw a suitable graph to illustrate this data.'),
     S(39, 'Bar Chart · Pie Chart', '(ii) Explain'), GRAPH, '2-0', TG),
    ('(ii)', 4, L(15, '(ii) Explain briefly one challenge facing countries with a high proportion', 'urban areas.'),
     S(39, 'Any valid explanation · 2 + 2 marks', FOOT), (pair('Any valid explanation · 2 + 2 marks', 'Challenge'),),
     '4-5', URB),
])

PART_TWO += [
    T('p2-12b', P2, '12B', '', 30, 15, L(15, 'Migration'),
      (L(15, 'Describe and explain changes in patterns of migration to and from Ireland since 1950.'),),
      NOTE_SLICE, unprinted(30), '4-2', POP, ID + 'p2-q12b'),
    T('p2-12c', P2, '12C', '', 30, 15, L(15, 'Central Place Theory', nth=0),
      (L(15, 'Describe and explain Central Place Theory with reference to example(s) you have studied.'),),
      NOTE_SLICE, unprinted(30), '4-3', URB, ID + 'p2-q12c'),
]

# ------------------------------------------------------------------ Options --
ASPECTS = ('Number of aspects: · 3 @ 20 marks each', 'Identifying aspect: · 4 marks', 'Discussion: · 8 x SRPs')


def option(q, page, theme, note_nth, prompt, topic, atlas, scheme_page=None, after=None, end=None, routes=()):
    """An option essay: its printed outline where the scheme prints one, else the unprinted row."""
    if scheme_page is None:
        scheme, criteria = NOTE_SLICE, unprinted(80)
    else:
        scheme = (S(scheme_page, 'Number of aspects', end or FOOT, None, after),)
        criteria = (Criterion('Aspects (3 @ 20 marks or 4 @ 15 marks)', 60, upto(60), 'srp', ASPECTS),
                    Criterion('Overall coherence', 20, upto(20), 'srp', ('Overall Coherence: · 20 marks graded*',)))
    card_id = routes[0].card_id if routes else ID + f'p2-q{q}'
    return T(f'p2-{q}', P2, q, '', 80, page, theme, (prompt,), scheme, criteria, topic, (atlas,), card_id,
             stem=(L(page, 'Note: It is better to discuss three or four aspects', 'large number of points.',
                     nth=note_nth),), routes=routes)


GI, GE = H + 'option-global-interdependence', H + 'option-geoecology'
CI, AO = H + 'option-culture-identity', H + 'option-atmosphere-ocean'
OPTIONS = [
    option('13', 17, L(17, 'Global Interdependence'), 0,
           L(17, 'Examine the impact that aid can have on development.'), '5-2', GI),
    option('14', 17, L(17, 'Global Interdependence'), 0,
           L(17, 'Examine the causes and impacts of any one of the following global environmental issues:',
             'Desertification.'), '5-3', GI, routes=bullet_routes('p2-q14-', ISSUES)),
    option('15', 17, L(17, 'Global Interdependence'), 0,
           L(17, 'Sustainability is a model for future development.', 'Self-reliance.'), '5-3', GI),
    option('16', 17, L(17, 'Geoecology'), 1,
           L(17, 'Examine the influence of mineral matter, air, water, and organic matter', 'development.'),
           '6-0', GE, scheme_page=44, after='16.', end='17.'),
    option('17', 17, L(17, 'Geoecology'), 1,
           L(17, 'Examine how each of the following activities impact on biomes:', 'Industrial development.'),
           '6-3', GE, scheme_page=44, after='17.', end='18.'),
    option('18', 17, L(17, 'Geoecology'), 1,
           L(17, 'Various soil patterns have developed because of the action', 'Discuss.'), '6-1', GE),
    option('19', 18, L(18, 'Culture and Identity'), 0,
           L(18, 'Examine the effects of political and/or physical boundaries on cultural groups.'),
           '7-1', CI, scheme_page=45, after='19.', end='20.'),
    option('20', 18, L(18, 'Culture and Identity'), 0,
           L(18, '‘Cultural identity is defined by many diverse factors’.', 'you have'), '7-2', CI),
    option('21', 18, L(18, 'Culture and Identity'), 0,
           L(18, 'Examine the strategies that have been or could be implemented', 'minority languages.'), '7-0', CI),
    option('22', 18, L(18, 'The Atmosphere – Ocean Environment'), 1,
           L(18, 'Describe and account for the specific characteristics of one global climate type', 'studied.'),
           '8-4', AO),
    option('23', 18, L(18, 'The Atmosphere – Ocean Environment'), 1,
           L(18, 'Exchanges of water between oceans and atmosphere', 'Discuss.'), '8-2', AO),
    option('24', 18, L(18, 'The Atmosphere – Ocean Environment'), 1,
           L(18, 'Climate characteristics have an influence on economic development.', 'with reference to agriculture.'),
           '8-5', AO),
]

TASKS = [*PART_ONE, *PART_TWO, *OPTIONS]

ID_CORRECTION_REASON = 'No deferred card shipped before this review, so no id is re-scoped.'

# No 2024 Higher deferred card shipped before this review.
LEGACY_IDS: list[str] = []
