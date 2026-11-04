"""Independent review ledger: Leaving Certificate Geography 2019 Higher Level.

Sources (English editions, harvested Paper Trail corpus; sizes and SHA-256
pinned in EXPECTED_SOURCES and the generated audit): the examination paper
LC005ALP000EV (32 pages; one booklet printed Part One, answered in it, and
Part Two), marking scheme LC005ALP000EV (52 pages), and the common
companions — the 1:50 000 Templemore map LC005CLP003EV (published only as a
JPEG), its legend LC005CLPC00EV and the Templemore aerial photograph
LC005CLP004EV (a JPEG). Part One is 80 marks (any ten of twelve @ 8), Part
Two 320 (four questions @ 80).

Visual sweep (every page rendered and read on 2026-10-13):
  Paper p1 cover and examiner's grid; p2-p12 Part One Questions 1-12 (p7
  holds Q6 and Q7; Q9 prints a street map of part of Templemore); p13 Part
  Two instructions; p14 Section 1 divider; p15-p21 Q1-Q6 (p16 holds 2A, p17
  2B and 2C); p22 Section 2 divider; p23-p28 Electives Q7-Q12; p29 Section 3
  divider and option note; p30-p31 Options Q13-Q24; p32 back cover ("There
  is no examination material on this page").
  Scheme p1 cover; p2-p3 notes; p4 Part One table (two columns: Q1-Q6,
  Q7-Q12); p5 Part Two instructions; p6-p19 Q1-Q6; p20 Section 2 divider;
  p21-p32 Q7-Q12; p33 Section 3 divider; p34 option outline and Overall
  Coherence descriptors; p35-p42 Q13-Q24; p43-p46 Geographical
  Investigation (coursework); p47 investigation topics; p48 Irish-language
  bonus marks; p49-p51 printed "Blank Page"; p52 back cover.
  Companions: Templemore map extract (the River Suir, Templemore Lake, the
  N62, the railway); OS legend sheet; oblique aerial photograph of
  Templemore.

Boundaries and tariffs follow the 2020 Higher ledger. Matching tables, in
the printed row order: Q2 (i) Delta=C, Geo=A, Pyramidal peak=D, Drumlin=B
and (ii) Deposition, Erosion, Erosion, Deposition (each column read with
its own clip); Q3 Layers of lava and volcanic ash=E, Parasitic cone=C,
Vent=A, Crater=B, Subsidiary vent=D, Volcanic plug=F; Q5 Region of
industrial decline=Sambre Meuse valley, Karst landscape=The Burren,
Climatic=Mediterranean, Administrative=Co. Cavan, Granite landscape=Leinster
Batholith, Religion=Islamic world, and (ii)(a) True, (ii)(b) False, each
lettered statement a task; Q6 S 06 73 Even slope, S 10 73 Flat land, S 04
76 Concave slope, S 04 71 V-shaped valley; Q9 B centre middleground, C right
background, D left background, E centre background (A is printed, so four
rows are priced). 8A and 10A each price their sketch, items and added
feature as one roman (i) and the brief explanation as (ii). 6C "geomorphology
or climate" and option 15 "any one of the following" are printed routes.
"""

from geography_review import (
    Criterion, Lift, Route, SchemeSlice, Task, pool, evens, fixed, slug, srp, sums, upto,
)

YEAR = 2019
LEVEL = 'higher'
PAPER_PAGES = {1: 32, 2: 32}
SCHEME_PAGES = 52
QUESTION_TARIFFS = {1: {str(n): 8 for n in range(1, 13)},
                    2: {**{f'{n}{x}': (20 if x == 'A' else 30)
                           for n in range(1, 13) for x in 'ABC'},
                        **{str(n): 80 for n in range(13, 25)}}}

EXPECTED_SOURCES = {
    'paper1': ('LC005ALP000EV.pdf', 3445591),
    'paper2': ('LC005ALP000EV.pdf', 3445591),
    'scheme': ('LC005ALP000EV.pdf', 981191),
    'map': ('LC005CLP003EV.jpg', 7718516),
    'legend': ('LC005CLPC00EV.pdf', 836095),
    'aerial': ('LC005CLP004EV.jpg', 5264592),
}

_PAPER = {1: 'cover and examiner grid', **{p: 'question' for p in range(2, 13)},
          13: 'Part Two instructions', 14: 'section divider', **{p: 'question' for p in range(15, 22)},
          22: 'section divider', **{p: 'question' for p in range(23, 29)}, 29: 'section divider and option note',
          30: 'question', 31: 'question', 32: 'back cover'}
PAGE_REVIEW = {
    # One booklet printed both parts.
    'paper1': _PAPER, 'paper2': _PAPER,
    'scheme': {1: 'cover', 2: 'notes', 3: 'notes', 4: 'Part One table', 5: 'Part Two instructions',
               **{p: 'Part Two allocation' for p in range(6, 20)}, 20: 'section divider',
               **{p: 'Part Two allocation' for p in range(21, 33)}, 33: 'section divider',
               34: 'option outline and coherence descriptors',
               **{p: 'option allocation' for p in range(35, 43)},
               **{p: 'geographical investigation (coursework)' for p in range(43, 47)},
               47: 'investigation topics', 48: 'Irish-language bonus marks',
               49: 'blank', 50: 'blank', 51: 'blank', 52: 'back cover'},
}

EXPECTED_SELECTION_SCAN = [
    [1, 2, 'attempt any ten'], [1, 13, 'attempt four'], [1, 14, 'attempt two'], [1, 15, 'attempt one'],
    [1, 15, 'answer (i) or (ii)'], [1, 15, 'or one'], [1, 15, 'or one'],
    [1, 16, 'either'],
    [1, 17, 'one of the following'],
    [1, 19, 'attempt one'],
    [1, 21, 'any two'],
    [1, 22, 'attempt one'],
    [1, 23, 'any one'],
    [1, 27, 'two of the following'],
    [1, 28, 'any one'],
    [1, 29, 'attempt one'],
    [1, 30, 'any one'],
]
SELECTION_REVIEW = [
    {'scan': [[1, 2, 'attempt any ten'], [1, 13, 'attempt four'], [1, 14, 'attempt two'], [1, 15, 'attempt one'],
              [1, 19, 'attempt one'], [1, 22, 'attempt one'], [1, 29, 'attempt one']],
     'kind': 'exam-attempt-rule',
     'reason': 'Part One any ten of twelve and Part Two four questions (one of Q1-3, one of Q4-6, one elective, one option) are attempt rules; every question is carded.'},
    {'scan': [[1, 15, 'answer (i) or (ii)'], [1, 15, 'or one'], [1, 15, 'or one']], 'kind': 'closed-route',
     'reason': '1B: (i) or (ii); (i) offers one fluvial OR one coastal OR one glacial landform -> 4 routes.'},
    {'scan': [[1, 17, 'one of the following']], 'kind': 'closed-choose-one',
     'reason': '2C one of three printed human impacts -> 3 routes. 6C "geomorphology or climate" -> 2 routes.'},
    {'scan': [[1, 30, 'any one']], 'kind': 'closed-choose-one',
     'reason': 'Option 15 any one of three printed global environmental issues -> 3 routes.'},
    {'scan': [[1, 27, 'two of the following']], 'kind': 'choose-n-one-card',
     'reason': '11B two of three printed land-uses -> one card with every printed item (choice is not a route; the scheme marks each chosen land-use alike).'},
    {'scan': [[1, 16, 'either'], [1, 21, 'any two'], [1, 23, 'any one'], [1, 28, 'any one']],
     'kind': 'open-response',
     'reason': 'No printed pool: 2A\'s text "either destroyed or declared unsafe" describes buildings; 6B any two factors; 7C any one EU policy; 12A(ii) any one other factor. Compulsory lists stay whole: 1A, 4A, 8A, 10A each bullet, 2B each rock, 8C both advantages, 16 each activity.'},
]

P1, P2 = 1, 2
LEFT = (0.0, 0.0, 0.51, 1.0)
RIGHT = (0.51, 0.0, 1.0, 1.0)
Q2I_COL = (0.0, 0.27, 0.30, 0.345)
Q2II_COL = (0.30, 0.27, 0.51, 0.345)
ID = 'geography-2019-hl-'
H = 'geography-higher-'
SRPS = 'SRP’s'


def L(page, start, end=None, nth=None):
    return Lift(page, start, end, None, nth)


def S(page, start, end=None, clip=None, after=None, table=False):
    return SchemeSlice(page, start, end, clip, after, table)


def T(key, part, q, sub, marks, page, title, prompt, scheme, criteria, topic, atlas, card_id,
      sources=(), stem=(), routes=(), row_labels=(), absorbs=()):
    return Task(key, part, q, sub, marks, page, title, prompt, scheme, criteria, topic, atlas,
                sources, card_id, False, stem=stem, routes=routes, row_labels=row_labels,
                absorbs=absorbs)


def rows(lines, marks=1):
    return tuple(fixed(f'Row {i}', marks, line) for i, line in enumerate(lines, 1))


def pair(line, label):
    return fixed(label, 4, line, (0, 2, 4))


def one_plus_one(line, label):
    return fixed(label, 2, line, (0, 1, 2))


def romans(q, part, page, title, stem, first_id, sources, parts):
    """parts: (sub, marks, prompt Lift(s), scheme slice(s), criteria, topic, atlas[, row labels])."""
    out = []
    for index, item in enumerate(parts):
        sub, marks, prompt, scheme, criteria, topic, atlas = item[:7]
        labels = item[7] if len(item) > 7 else ()
        key = sub.strip('()').replace(')(', '-')
        out.append(T(f'p{part}-{q.lower()}-{key}', part, q, sub, marks, page, title,
                     prompt if isinstance(prompt, tuple) else (prompt,),
                     scheme if isinstance(scheme, tuple) else (scheme,), criteria, topic, atlas,
                     first_id if index == 0 else f'{first_id}-{key}', sources, stem,
                     row_labels=labels))
    return out


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
LAND = (H + 'urban-land-uses',)
ECON = (H + 'elective-economic',)
DEV = (H + 'economic-developing-economies',)
MNC = (H + 'economic-multinationals-globalisation',)
EU_ECON = (H + 'economic-european-union',)
ENERGY = (H + 'economic-energy',)
ENV = (H + 'economic-environmental-impact',)

# ---------------------------------------------------------------- Part One --
Q1S = (L(2, 'Examine the image above which illustrates erosion of a coastline', 'following questions.'),)
PART_ONE = romans('1', P1, 2, L(2, 'Coastal Processes'), Q1S, ID + 'p1-q1', ('page',), [
    ('(i)', 2, L(2, '(i) Calculate the average annual rate of erosion (in metres) between 2008 and 2018.'),
     S(4, '(i) · 1.65', '(ii) · 2 valid processes', LEFT), (fixed('Rate of erosion', 2, '(i) · 1.65 (metres) 2m'),),
     '0-10', SEA),
    ('(ii)', 2, L(2, '(ii) Name two processes of coastal erosion.'),
     S(4, '(ii) · 2 valid processes', '(iii) · 2 valid landforms', LEFT),
     (one_plus_one('(ii) · 2 valid processes 1m + 1m', 'Two processes'),), '0-10', SEA),
    ('(iii)', 2, L(2, '(iii) Name two landforms formed as a result of coastal erosion.'),
     S(4, '(iii) · 2 valid landforms', '(iv) · True', LEFT),
     (one_plus_one('(iii) · 2 valid landforms 1m + 1m', 'Two landforms'),), '0-10', SEA),
    ('(iv)', 2, (L(2, '(iv) State whether the following statement is true or false.'),
                 L(2, 'The strength of a destructive wave’s swash is weaker than its backwash.')),
     S(4, '(iv) · True', 'Q2', LEFT, 'Q1'), (fixed('True or false', 2, '(iv) · True 2m'),), '0-10', SEA),
])

Q2S = (L(3, 'Examine the photographs above and answer each of the following questions.'),)
Q2_ROWS = (L(3, 'Delta'), L(3, 'Geo', nth=0), L(3, 'Pyramidal peak'), L(3, 'Drumlin'))
PART_ONE += [
    T('p1-2-i', P1, '2', '(i)', 4, 3, L(3, 'The Physical Environment'),
      (L(3, '(i) Match each of the photographs A, B, C and D with the feature', 'table below.', nth=0),),
      (S(4, '(i) · C 1m', None, Q2I_COL),), rows(['(i) · C 1m', '=A 1m', '=D 1m', '=B 1m']),
      '0-4', RIVERS + SEA + GLAC, ID + 'p1-q2', ('page',), Q2S, row_labels=Q2_ROWS),
    T('p1-2-ii', P1, '2', '(ii)', 4, 3, L(3, 'The Physical Environment'),
      (L(3, '(ii) Indicate, by ticking the correct box', 'processes of deposition.'),),
      (S(4, '(ii) Deposition', None, Q2II_COL),),
      rows(['(ii) Deposition 1m', '=Erosion 1m@0', '=Erosion 1m@1', '=Deposition 1m']),
      '0-4', RIVERS + SEA + GLAC, ID + 'p1-q2-ii', ('page',), Q2S, row_labels=Q2_ROWS),
]

Q3S = (L(4, 'Examine the diagram of the structure of a volcano above', 'following questions.'),)
PART_ONE += romans('3', P1, 4, L(4, 'Structure of a Volcano'), Q3S, ID + 'p1-q3', ('page',), [
    ('(i)', 6, L(4, '(i) Match each of the letters A, B, C, D, E and F on the diagram', 'table below.'),
     S(4, '(i) · E 1m', '(ii) · True', LEFT, 'Q3'),
     rows(['(i) · E 1m', '=C 1m', '=A 1m', '=B 1m', '=D 1m', '=F 1m']), '0-7', EV,
     (L(4, 'Layers of lava and volcanic ash'), L(4, 'Parasitic cone'), L(4, 'Vent'), L(4, 'Crater'),
      L(4, 'Subsidiary vent'), L(4, 'Volcanic plug'))),
    ('(ii)', 2, (L(4, '(ii) State whether the following statement is true or false.'),
                 L(4, 'A shield volcano is formed by lava flows of low viscosity.')),
     S(4, '(ii) · True', 'Q4', LEFT, 'Q3'), (fixed('True or false', 2, '(ii) · True 2m'),), '0-7', EV),
])

Q4S = (L(5, 'Examine the map above showing isostatic adjustment per annum', 'following questions.'),)
PART_ONE += romans('4', P1, 5, L(5, 'Isostatic Processes'), Q4S, ID + 'p1-q4', ('page',), [
    ('(i)', 2, L(5, '(i) Name two coastal features formed due to isostatic adjustments', 'marked in red.'),
     S(4, '(i) · 2 valid answers', '(ii) · 2 valid answers', LEFT),
     (one_plus_one('(i) · 2 valid answers 1m+1m', 'Two coastal features'),), '0-5', SEA),
    ('(ii)', 2, L(5, '(ii) Name two coastal features formed due to isostatic adjustments', 'marked in blue.'),
     S(4, '(ii) · 2 valid answers', '(iii) · (River)', LEFT),
     (one_plus_one('(ii) · 2 valid answers 1m+1m', 'Two coastal features'),), '0-5', SEA),
    ('(iii)', 2, L(5, '(iii) What is the name of the process resulting in a renewal of erosive activity',
                   'old stage of a river?'),
     S(4, '(iii) · (River)', '(iv) · True', LEFT), (fixed('Process', 2, '(iii) · (River) Rejuvenation 2m'),),
     '0-5', RIVERS),
    ('(iv)', 2, (L(5, '(iv) State whether the following statement is true or false.'),
                 L(5, 'Endogenic forces are processes operating below the earth’s crust.')),
     S(4, '(iv) · True', 'Q.5', LEFT, 'Q4'), (fixed('True or false', 2, '(iv) · True 2m'),), '0-0', PS),
])

Q5_EXAMPLES = (L(6, 'Example of Region:'), L(6, 'The Burren'), L(6, 'Leinster Batholith'), L(6, 'Mediterranean'),
               L(6, 'Sambre Meuse Valley'), L(6, 'Co. Cavan'), L(6, 'Islamic World'))
TF5 = L(6, '(ii) State whether each of the following statements is true or false.')
PART_ONE += [
    T('p1-5-i', P1, '5', '(i)', 6, 6, L(6, 'Concept of a Region'),
      (L(6, '(i) Complete the table by matching each of the examples of regions', 'in the table.'), *Q5_EXAMPLES),
      (S(4, '(i) Sambre Meuse', '(ii)True', LEFT),),
      rows(['(i) Sambre Meuse valley 1m', 'The Burren 1m', 'Mediterranean 1m', 'Co. Cavan 1m',
            'Leinster Batholith 1m', 'Islamic world 1m']),
      '1-0', IRL + EURO, ID + 'p1-q5',
      row_labels=(L(6, 'Region of industrial decline'), L(6, 'Geomorphological region (Karst landscape)'),
                  L(6, 'Climatic region'), L(6, 'Administrative region'),
                  L(6, 'Geomorphological region (Granite landscape)'), L(6, 'Cultural region (Religion)'))),
    T('p1-5-ii-a', P1, '5', '(ii)(a)', 1, 6, L(6, 'Concept of a Region'),
      (TF5, L(6, '(a) The hinterland is the area beyond a major town or city.')),
      (S(4, '(ii)True', 'False 1m', LEFT),), (fixed('Statement (a)', 1, '(ii)True 1m'),),
      '1-0', IRL + EURO + URB, ID + 'p1-q5-ii-a'),
    T('p1-5-ii-b', P1, '5', '(ii)(b)', 1, 6, L(6, 'Concept of a Region'),
      (TF5, L(6, '(b) A nodal region is a region characterised by poor transport.')),
      (S(4, 'False 1m', 'Q6', LEFT),), (fixed('Statement (b)', 1, 'False 1m'),),
      '1-0', IRL + EURO, ID + 'p1-q5-ii-b'),
]

PART_ONE += [
    T('p1-6', P1, '6', '', 8, 7, L(7, 'Landscape Identification'),
      (L(7, 'In the table below, match each of the following landscape features', 'Flat land.'),),
      (S(4, 'Even 2m', 'Page 2', LEFT),), rows(['Even 2m', 'Flat 2m', 'Concave 2m', 'V shaped valley 2m'], 2),
      '2-6', MAP + RIVERS, ID + 'p1-q6', ('map', 'legend'),
      (L(7, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper.', nth=0),),
      row_labels=(L(7, 'S 06 73'), L(7, 'S 10 73'), L(7, 'S 04 76'), L(7, 'S 04 71'))),
]
Q7S = (L(7, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper, and answer',
         'following questions.'),)
PART_ONE += romans('7', P1, 7, L(7, 'Map Skills'), Q7S, ID + 'p1-q7', ('map', 'legend'), [
    ('(i)', 2, L(7, '(i) Name the antiquity located at S 083 688.'), S(4, '(i) · Burial', '(ii) · 8.0', RIGHT),
     (fixed('Antiquity', 2, '(i) · Burial ground 2m'),), '2-6', MAP),
    ('(ii)', 2, L(7, '(ii) Measure the length, in kilometres, of the entire railway line.'),
     S(4, '(ii) · 8.0', '(iii) · Coniferous', RIGHT), (fixed('Length', 2, '(ii) · 8.0 – 8.6(km) 2m'),), '2-6', MAP),
    ('(iii)', 2, L(7, '(iii) What type of forestry is present in grid box S 15 69?'),
     S(4, '(iii) · Coniferous', '(iv) · 7', RIGHT), (fixed('Forestry', 2, '(iii) · Coniferous 2m'),), '2-6', MAP),
    ('(iv)', 2, L(7, '(iv) Calculate the approximate area, in square kilometres', 'above 300 metres.'),
     S(4, '(iv) · 7', 'Q8', RIGHT), (fixed('Area', 2, '(iv) · 7 – 9 (km²) 2m'),), '2-6', MAP),
])
Q8S = (L(8, 'Examine the aerial photograph and the 1:50 000 Ordnance Survey map and legend', 'following questions.'),)
PART_ONE += romans('8', P1, 8, L(8, 'Aerial Photograph and Ordnance Survey Map'), Q8S, ID + 'p1-q8',
                   ('aerial', 'map', 'legend'), [
    ('(i)', 2, L(8, '(i) In what direction was the camera pointed when the aerial photograph was taken?'),
     S(4, '(i) · North-East', '(ii) · S 117', RIGHT), (fixed('Direction', 2, '(i) · North-East 2m'),), '2-8', AER),
    ('(ii)', 2, L(8, '(ii) Give a six-figure grid reference for the large church', 'aerial photograph.'),
     S(4, '(ii) · S 117', '(iii) · N62', RIGHT), (fixed('Grid reference', 2, '(ii) · S 117 717 2m'),),
     '2-8', AER + MAP),
    ('(iii)', 2, L(8, '(iii) Name the main road that runs through the aerial photograph', 'left background.'),
     S(4, '(iii) · N62', '(iv) · False', RIGHT), (fixed('Road', 2, '(iii) · N62 2m'),), '2-8', AER + MAP),
    ('(iv)', 2, (L(8, '(iv) Examine the aerial photograph, and state whether the following statement',
                   'true or false.'),
                 L(8, 'The wide street network in the town centre indicates', 'unplanned town.')),
     S(4, '(iv) · False', 'Q.9', RIGHT), (fixed('True or false', 2, '(iv) · False 2m'),), '2-8', AER + URB),
])
PART_ONE.append(T(
    'p1-9', P1, '9', '', 8, 9, L(9, 'Aerial Photograph', nth=0),
    (L(9, 'Locate each of the features labelled A, B, C, D and E above', 'One has been completed for you.'),),
    (S(4, 'B Centre / Middle', 'Q 10', RIGHT),),
    rows(['B Centre / Middle 2m', 'C Right Background 2m', 'D Left Background 2m', 'E Centre Background 2m'], 2),
    '2-8', AER + URB, ID + 'p1-q9', ('page', 'aerial'),
    (L(9, 'Examine the aerial photograph of Templemore accompanying this paper.'),
     L(9, 'Examine the street map below of part of the area covered by the aerial photograph.'),
     L(9, 'Note: The orientation of the aerial photograph', 'the street map below.')),
    row_labels=(L(9, 'B Town hall'), L(9, 'C Graveyard'), L(9, 'D Athletics track'), L(9, 'E Housing estate'))))

Q10S = (L(10, 'Examine the weather information above from Met Éireann', 'using the data provided.'),)
PART_ONE += romans('10', P1, 10, L(10, 'Graphical Interpretation'), Q10S, ID + 'p1-q10', ('page',), [
    ('(i)', 2, L(10, '(i) Calculate the total rainfall (in mm), over the three days.'),
     S(4, '(i) · 5.4', '(ii) · 8 (°C)', RIGHT), (fixed('Total rainfall', 2, '(i) · 5.4 (mm) 2m'),), '2-7', WX + TG),
    ('(ii)', 2, L(10, '(ii) Calculate the temperature range (°C), on Monday.'),
     S(4, '(ii) · 8 (°C)', '(iii) · 8 (km', RIGHT), (fixed('Temperature range', 2, '(ii) · 8 (°C) 2m'),),
     '2-7', WX + TG),
    ('(iii)', 2, L(10, '(iii) Calculate the mean wind speed (km/hr), on Wednesday.'),
     S(4, '(iii) · 8 (km', '(iv) · Prevailing', RIGHT), (fixed('Mean wind speed', 2, '(iii) · 8 (km/hr) 2m'),),
     '2-7', WX + TG),
    ('(iv)', 2, L(10, '(iv) What is the term used to describe the wind that blows most frequently over an area?'),
     S(4, '(iv) · Prevailing', 'Q11', RIGHT), (fixed('Term', 2, '(iv) · Prevailing 2m'),), '2-7', WX),
])
Q11S = (L(11, 'Examine the table above showing the number of Irish citizenship applications', 'following questions.'),)
PART_ONE += romans('11', P1, 11, L(11, 'Statistical Interpretation'), Q11S, ID + 'p1-q11', ('page',), [
    ('(i)', 2, L(11, '(i) Which country had the highest number of applications for Irish citizenship', 'age group?'),
     S(4, '(i) · India', '(ii) · 332', RIGHT), (fixed('Country', 2, '(i) · India 2m'),), '2-0', TG),
    ('(ii)', 2, L(11, '(ii) How many Romanians in the 18-34 year age group applied for Irish citizenship?'),
     S(4, '(ii) · 332', '(iii) · 26.28', RIGHT), (fixed('Number', 2, '(ii) · 332 2m'),), '2-0', TG),
    ('(iii)', 2, L(11, '(iii) Calculate the percentage of total applications from the United Kingdom', 'age group.'),
     S(4, '(iii) · 26.28', '(iv) · Two advantages', RIGHT), (fixed('Percentage', 2, '(iii) · 26.28 (%) 2m'),),
     '2-0', TG),
    ('(iv)', 2, (L(11, '(iv) The possible exit of the United Kingdom from the European Union', 'Irish citizenship.'),
                 L(11, 'State two advantages for citizens of the United Kingdom', 'leaves the European Union.')),
     S(4, '(iv) · Two advantages', 'Q12', RIGHT),
     (one_plus_one('(iv) · Two advantages 1m +1m', 'Two advantages'),), '4-2', POP + EU_ECON),
])
Q12S = (L(12, 'Read the extract above and answer each of the following questions.'),)
PART_ONE += romans('12', P1, 12, L(12, 'Economic Development'), Q12S, ID + 'p1-q12', ('page',), [
    ('(i)', 2, L(12, '(i) What proportion of new growth is planned for inside Dublin?'),
     S(4, '(i) · One quarter', '(ii) · 116', RIGHT), (fixed('Proportion', 2, '(i) · One quarter / 25% 2m'),),
     '1-4', IRL),
    ('(ii)', 2, L(12, '(ii) What is the planned investment (€ billion) under the National Development plan?'),
     S(4, '(ii) · 116', '(iii) · 50', RIGHT), (fixed('Investment', 2, '(ii) · 116 (€ billion) 2m'),), '1-4', IRL),
    ('(iii)', 2, L(12, '(iii) What percentage of the projected population growth is planned for towns', 'rural areas?'),
     S(4, '(iii) · 50', '(iv) · Border', RIGHT), (fixed('Percentage', 2, '(iii) · 50 (%) 2m'),), '1-4', IRL),
    ('(iv)', 2, L(12, '(iv) In order to Brexit-proof Ireland for the future', 'focus of investment?'),
     S(4, '(iv) · Border', 'of 46', RIGHT), (fixed('Regions', 2, '(iv) · Border Regions 2m'),), '1-4', IRL),
])


# ---------------------------------------------------------------- Part Two --
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
SHOWN_LABEL = sums((0, 1, 3), (0, 1))


def split(label, total, first, second):
    return srp(label, total, (first, second))


def bullet_routes(prefix, items, atlas=None):
    return tuple(Route(slug(item, 34), item.rstrip('.'), ID + prefix + slug(item, 34), False,
                       keep_bullets=(item,), atlas=(atlas[item] if atlas else None))
                 for item in items)


LANDFORMS = 'one fluvial landform or one coastal landform or one glacial landform'
IMPACTS = ('The impact of human activity on river processes', 'The impact of human activity on coastal processes',
           'The impact of human activity on mass movement processes.')
ROUTES_2C = bullet_routes('p2-q2c-', IMPACTS, atlas=dict(zip(IMPACTS, (RIVERS, SEA, RW))))
PART_TWO = [
    T('p2-1a', P2, '1A', '', 20, 15, L(15, 'Ordnance Survey Map'),
      (L(15, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper.',
         'The entire route of the railway line.'),),
      (S(6, 'Sketch Outline', None),), OS_SKETCH, '2-6', MAP + RIVERS, ID + 'p2-q1a', ('map', 'legend'),
      row_labels=(None, L(15, 'The course of the River Suir from S 132 728 to S 119 680'),
                  L(15, 'The entire area of land above 200 metres'), L(15, 'The entire area of Templemore Lake'),
                  L(15, 'The entire route of the railway line.'))),
    T('p2-1b', P2, '1B', '', 30, 15, L(15, 'Surface Processes'),
      (L(15, '(i) Examine the role of the process of deposition', 'that you have studied.', nth=0),),
      (S(7, 'Landform named · 2 marks', 'Or'),),
      (fixed('Landform named', 2, 'Landform named · 2 marks'), srp('Examination', 14, f'Examination · 14 x {SRPS}')),
      '0-9', RIVERS, ID + 'p2-q1b-route-i-fluvial-landform',
      routes=(
          Route('route-i-fluvial-landform', 'Route (i) · one fluvial landform', ID + 'p2-q1b-route-i-fluvial-landform',
                False, ((LANDFORMS, 'one fluvial landform'),), topic='0-9', atlas=RIVERS),
          Route('route-i-coastal-landform', 'Route (i) · one coastal landform', ID + 'p2-q1b-route-i-coastal-landform',
                False, ((LANDFORMS, 'one coastal landform'),), topic='0-10', atlas=SEA),
          Route('route-i-glacial-landform', 'Route (i) · one glacial landform', ID + 'p2-q1b-route-i-glacial-landform',
                False, ((LANDFORMS, 'one glacial landform'),), topic='0-11', atlas=GLAC),
          Route('route-ii', 'Route (ii)', ID + 'p2-q1b-route-ii', False,
                prompt=(L(15, '(ii) Describe and explain the factors governing the operation', 'that you have studied.',
                          nth=0),),
                scheme=(S(7, 'Factors identified', None),),
                criteria=(pair('Factors identified · 2 + 2 marks', 'Factors identified'),
                          fixed('Mass movement process named', 2, 'Mass movement process named 2 marks'),
                          srp('Description/explanation', 12, f'Description/explanation · 12 x {SRPS}')),
                topic='0-8', atlas=RW),
      )),
    T('p2-1c', P2, '1C', '', 30, 15, L(15, 'Tectonic Activity – Irish Landscape'),
      (L(15, 'Examine the impact of tectonic activity on the landscape of Ireland.'),),
      (S(8, 'Impact of tectonic activity', None),),
      (fixed('Impact identified', 2, 'Impact of tectonic activity on the Irish landscape identified · 2 marks'),
       srp('Examination', 14, f'Examination · 14 x {SRPS}')),
      '0-2', PS + RW, ID + 'p2-q1c'),
]

Q2AS = (L(16, 'Examine the information above and answer each of the following questions.'),)
PART_TWO += romans('2A', P2, 16, L(16, 'Earthquakes'), Q2AS, ID + 'p2-q2a', ('page',), [
    ('(i)', 2, L(16, '(i) What was the magnitude of the Northridge earthquake in 1994?'),
     S(10, '(i) · 6.7', '(ii) · Malibu'), (fixed('Magnitude', 2, '(i) · 6.7 · 2 marks'),), '0-7', EV),
    ('(ii)', 2, L(16, '(ii) Which of the named Los Angeles urban areas was closest to the earthquake’s epicentre?'),
     S(10, '(ii) · Malibu', '(iii) · 10'), (fixed('Urban area', 2, '(ii) · Malibu · 2 marks'),), '0-7', EV),
    ('(iii)', 2, L(16, '(iii) How long did it take (in seconds) for the effects of the earthquake', 'Ventura?'),
     S(10, '(iii) · 10', '(iv) · 90'), (fixed('Seconds', 2, '(iii) · 10 (seconds) 2 marks'),), '0-7', EV),
    ('(iv)', 4, L(16, '(iv) How many kilometres did the seismic waves travel from the epicentre to point X?'),
     S(10, '(iv) · 90', '(v) · Valid'), (fixed('Distance', 4, '(iv) · 90-105 (km) 4 marks'),), '0-7', EV),
    ('(v)', 2, L(16, '(v) State one negative impact of the earthquake, referred to in the text above.'),
     S(10, '(v) · Valid', '(vi) · Valid'), (fixed('Negative impact', 2, '(v) · Valid answer 2 marks'),), '0-7', EV),
    ('(vi)', 4, L(16, '(vi) Explain briefly one function of a seismic station.'),
     S(10, '(vi) · Valid', '(vii) · Valid'), (pair('(vi) · Valid answer 2 + 2 marks', 'Function'),), '0-7', EV),
    ('(vii)', 4, L(16, '(vii) Explain briefly one way of making infrastructure earthquake proof.'),
     S(10, '(vii) · Valid', '2B.'), (pair('(vii) · Valid answer 2 + 2 marks', 'Way'),), '0-7', EV),
])
PART_TWO += [
    T('p2-2b', P2, '2B', '', 30, 17, L(17, 'Rocks'),
      (L(17, 'Explain the formation of each of the following, with reference to examples', 'One metamorphic rock.'),),
      (S(10, 'One sedimentary rock named', None),),
      (fixed('One sedimentary rock named', 2, 'One sedimentary rock named · 2 marks'),
       fixed('One metamorphic rock named', 2, 'One metamorphic rock named · 2 marks'),
       split('Explanation of formation of the two rocks (6/7 SRPs each)', 13,
             f'Explanation of formation of sedimentary rock · 6/7 x {SRPS}',
             f'Explanation of formation of metamorphic rock · 6/7x {SRPS}')),
      '0-1', RW, ID + 'p2-q2b'),
    T('p2-2c', P2, '2C', '', 30, 17, L(17, 'Human Interaction with Surface Processes'),
      (L(17, 'Human activity impacts on surface processes.'),
       L(17, 'Examine this statement with reference to one of the following:', 'mass movement processes.')),
      (S(11, 'Impact on process identified', None),),
      (fixed('Impact on process identified', 2, 'Impact on process identified · 2 marks'),
       srp('Examination of impact on process', 14, f'Examination of impact on process · 14 x {SRPS}')),
      '0-6', RIVERS, ROUTES_2C[0].card_id, routes=ROUTES_2C),
]

Q3AS = (L(18, 'Examine the diagram of glacial landforms above', 'following questions.'),)
PART_TWO += romans('3A', P2, 18, L(18, 'Glacial Landforms'), Q3AS, ID + 'p2-q3a', ('page',), [
    ('(i)', 12, L(18, '(i) Name each of the glacial landforms labelled A, B, C, D, E and F.'),
     S(12, '(i) · A = Pyramidal', '(ii) · Valid'),
     (fixed('A', 2, '(i) · A = Pyramidal peak · 2 marks'), fixed('B', 2, 'B = Arête · 2 marks'),
      fixed('C', 2, 'C = Cirque/corrie/coom/tarn · 2 marks'), fixed('D', 2, 'D = Ribbon lake · 2 marks'),
      fixed('E', 2, 'E = Truncated spurs · 2 marks'), fixed('F', 2, 'F = Hanging valley · 2 marks')), '0-11', GLAC),
    ('(ii)', 4, L(18, '(ii) Explain briefly what is meant by the term plucking in relation to glaciation.'),
     S(12, '(ii) · Valid', '(iii) · Valid'), (pair('(ii) · Valid explanation · 2 + 2 marks', 'Explanation'),),
     '0-11', GLAC),
    ('(iii)', 4, L(18, '(iii) Explain briefly how glaciers move.'),
     S(12, '(iii) · Valid', None), (pair('(iii) · Valid explanation · 2 + 2 marks', 'Explanation'),),
     '0-11', GLAC),
])
PART_TWO += [
    T('p2-3b', P2, '3B', '', 30, 18, L(18, 'Landscape Development'),
      (L(18, 'Explain how different rock types produce distinctive landscapes in Ireland', 'that you have studied.'),),
      (S(13, 'Rock 1 and associated', '3C.'),),
      (pair('Rock 1 and associated landscape named · 2 + 2 marks', 'Rock 1 and associated landscape named'),
       pair('Rock 2 and associated landscape named · 2 + 2 marks', 'Rock 2 and associated landscape named'),
       srp('Explanation', 11, f'Explanation · 11 x {SRPS}')),
      '0-1', RW + KARST, ID + 'p2-q3b'),
    T('p2-3c', P2, '3C', '', 30, 18, L(18, 'Plate Tectonics'),
      (L(18, 'Discuss the theory of plate tectonics (the plate tectonics model).'),),
      (S(13, 'Discussion of theory of plate tectonics', None, after='3C.'),),
      (srp('Discussion', 15, f'Discussion of theory of plate tectonics · 15 x {SRPS}'),),
      '0-0', PS, ID + 'p2-q3c'),
]

PART_TWO += [
    T('p2-4a', P2, '4A', '', 20, 19, L(19, 'Map Skills'),
      (L(19, 'Draw an outline map of a European region (not in Ireland) that you have studied.',
         'Two named urban centres in the region.'),),
      (S(14, 'Map outline', None),),
      sketch('Map outline · 4 marks graded (4/2/0)', (0, 2, 4),
             ('4 features @ 4 marks each · Shown 2 marks graded (2/1/0)', 'Named 2 marks'), sums((0, 1, 2), (0, 2)), 4),
      '1-5', EURO, ID + 'p2-q4a',
      row_labels=(None, L(19, 'The course of a named river in the region'),
                  L(19, 'The outline of a named feature of relief (upland or lowland) in the region'),
                  L(19, 'Two named urban centres in the region.'), L(19, 'Two named urban centres in the region.'))),
    T('p2-4b', P2, '4B', '', 30, 19, L(19, 'Tertiary Economic Activity – Tourism'),
      (L(19, 'Examine two factors that have influenced the development of tourism in an Irish region',
         'that you have studied.'),),
      (S(15, 'Factors identified', '4C.'),),
      (pair('Factors identified · 2 + 2 marks', 'Factors identified'),
       split('Examination of the two factors (7/6 SRPs each)', 13,
             f'Examination of Factor 1 · 7/6 x {SRPS}', f'Examination of Factor 2 · 7/6 x {SRPS}')),
      '1-4', IRL, ID + 'p2-q4b'),
    T('p2-4c', P2, '4C', '', 30, 19, L(19, 'Complexity of Regions'),
      (L(19, 'Changes in boundaries over time can impact on cultural groups.'),
       L(19, 'Examine this statement with reference to example(s) that you have studied.')),
      (S(15, 'Impact on cultural groups identified', None, after='4C.'),),
      (fixed('Impact on cultural groups identified', 2, 'Impact on cultural groups identified · 2 marks'),
       fixed('Example', 2, 'Example · 2 marks'), srp('Examination', 13, f'Examination · 13 x {SRPS}')),
      '1-3', EURO + IRL, ID + 'p2-q4c'),
]

Q5AS = (L(20, 'Examine the charts above showing the percentage of passengers', 'following questions.'),)
PART_TWO += romans('5A', P2, 20, L(20, 'Irish Transport'), Q5AS, ID + 'p2-q5a', ('page',), [
    ('(i)', 2, L(20, '(i) By how many million did the total number of passengers at Irish airports increase',
                 '2012 and 2016?'),
     S(16, '(i) · 4 (million)', '(ii) · 6.8'), (fixed('Increase', 2, '(i) · 4 (million) · 2 marks'),), '2-0', TG),
    ('(ii)', 4, L(20, '(ii) Calculate X, the percentage of passengers at Cork airport in 2016.'),
     S(16, '(ii) · 6.8', '(iii) · Dublin'), (fixed('Percentage', 4, '(ii) · 6.8 (%) · 4 marks'),), '2-0', TG),
    ('(iii)', 10, L(20, '(iii) Name the airport that experienced an increase in the percentage', 'this increase.'),
     S(16, '(iii) · Dublin', '(iv) · Valid'),
     (fixed('Airport', 2, '(iii) · Dublin (airport) · 2 marks'),
      pair('Valid explanation · 2 + 2 marks', 'First reason'), pair('=2 + 2 marks', 'Second reason')), '1-4', IRL),
    ('(iv)', 4, L(20, '(iv) Explain briefly one impact of changes in European Union structure', 'Dublin airport.'),
     S(16, '(iv) · Valid', None), (pair('(iv) · Valid explanation · 2 + 2 marks', 'Impact'),), '1-4', IRL),
])
PART_TWO += [
    T('p2-5b', P2, '5B', '', 30, 20, L(20, 'Primary Economic Activity – Agriculture'),
      (L(20, 'Account for the development of agriculture in a Continental / Sub-Continental region',
         'that you have studied.'),),
      (S(17, 'Examination · 15', '5C.', after='5B.'),), (srp('Examination', 15, f'Examination · 15 x {SRPS}'),),
      '1-6', CONT, ID + 'p2-q5b'),
    T('p2-5c', P2, '5C', '', 30, 20, L(20, 'Population Dynamics'),
      (L(20, 'Account for the population distribution throughout a European region', 'that you have studied.'),),
      (S(17, 'Examination · 15', None, after='5C.'),), (srp('Examination', 15, f'Examination · 15 x {SRPS}'),),
      '1-5', EURO + POP, ID + 'p2-q5c'),
]

Q6AS = (L(21, 'Examine the table above, showing the production of cow’s milk', 'following questions.'),)
PART_TWO += romans('6A', P2, 21, L(21, 'European Agriculture'), Q6AS, ID + 'p2-q6a', ('page',), [
    ('(i)', 2, L(21, '(i) Which region experienced a decline in the production of cow’s milk from 2014 to 2016?'),
     S(18, '(i) · Paris Basin', '(ii) · 1,420'), (fixed('Region', 2, '(i) · Paris Basin · 2 marks'),), '2-0', TG),
    ('(ii)', 2, L(21, '(ii) Calculate the increase (in thousand tonnes)', 'between 2008 and 2016.'),
     S(18, '(ii) · 1,420', '(iii) · 18.69'), (fixed('Increase', 2, '(ii) · 1,420 (thousand tonnes) · 2 marks'),),
     '2-0', TG),
    ('(iii)', 4, L(21, '(iii) Calculate the percentage increase in the production of cow’s milk', '2014 to 2016.'),
     S(18, '(iii) · 18.69', '(iv) · Valid'), (fixed('Percentage increase', 4, '(iii) · 18.69 (%) · 4 marks'),),
     '2-0', TG),
    ('(iv)', 8, L(21, '(iv) Explain briefly two reasons why agricultural output is higher in core areas',
                  'such as the Mezzogiorno.'),
     S(18, '(iv) · Valid', '(v) · Valid'),
     (pair('(iv) · Valid explanation · 2 + 2 marks', 'First reason'), pair('=2 + 2 marks', 'Second reason')),
     '1-5', EURO),
    ('(v)', 4, L(21, '(v) Explain briefly one environmental problem that may result from increased numbers',
                 'cattle.'),
     S(18, '(v) · Valid', None), (pair('(v) · Valid explanation · 2 + 2 marks', 'Problem'),), '1-5', EURO),
])
PART_TWO += [
    T('p2-6b', P2, '6B', '', 30, 21, L(21, 'Secondary Economic Activity'),
      (L(21, 'Examine how any two factors have influenced the development of secondary economic activity',
         'that you have studied.'),),
      (S(19, 'Factors named', '6C.'),),
      (pair('Factors named · 2 + 2 marks', 'Factors named'),
       split('Examination of the two factors (7/6 SRPs each)', 13,
             f'Examination of Factor 1 · 7/6 x {SRPS}', f'Examination of Factor 2 · 7/6 x {SRPS}')),
      '1-6', CONT, ID + 'p2-q6b'),
    T('p2-6c', P2, '6C', '', 30, 21, L(21, 'Concept of a Region'),
      (L(21, 'Examine how geomorphology or climate can be used to define regions', 'that you have studied.'),),
      (S(19, 'Examples · 2 + 2 marks', None, after='6C.'),),
      (pair('Examples · 2 + 2 marks', 'Examples'), srp('Examination', 13, f'Examination · 13 x {SRPS}')),
      '1-0', IRL + EURO, ID + 'p2-q6c-geomorphology',
      routes=(Route('geomorphology', 'Geomorphology', ID + 'p2-q6c-geomorphology', False,
                    (('geomorphology or climate', 'geomorphology'),)),
              Route('climate', 'Climate', ID + 'p2-q6c-climate', False,
                    (('geomorphology or climate', 'climate'),)))),
]

PART_TWO += romans('7A', P2, 23, L(23, 'Economic Activity'),
                   (L(23, 'Examine the data above showing internet access using fixed broadband', 'following questions.'),),
                   ID + 'p2-q7a', ('page',), [
    ('(i)', 16, L(23, '(i) Using graph paper, draw a suitable graph to illustrate this data.'),
     S(21, 'Bar Chart · Pie Chart', '(ii) · Explain briefly'), GRAPH, '2-0', TG),
    ('(ii)', 4, L(23, '(ii) Explain briefly what is meant by the term e-commerce.'),
     S(21, '(ii) · Explain briefly', None), (pair('Any valid explanation · 2 + 2 marks', 'Explanation'),),
     '3-0', ECON),
])
PART_TWO += [
    T('p2-7b', P2, '7B', '', 30, 23, L(23, 'Colonialism'),
      (L(23, 'Examine the impact of colonialism on a developing economy that you have studied.'),),
      (S(22, 'Impact identified · 2 marks', '7C.'),),
      (fixed('Impact identified', 2, 'Impact identified · 2 marks'),
       fixed('Developing economy named', 2, 'Naming developing economy · 2 marks'),
       srp('Examination', 13, f'Examination · 13 x {SRPS}')),
      '3-1', DEV, ID + 'p2-q7b'),
    T('p2-7c', P2, '7C', '', 30, 23, L(23, 'Ireland and European Union Policy'),
      (L(23, 'Explain how any one European Union policy has influenced the Irish economy.'),),
      (S(22, 'Policy named', None, after='7C.'),),
      (fixed('Policy named', 2, 'Policy named · 2 marks'),
       fixed('Influence on the Irish economy identified', 2, 'Influence on the Irish economy identified · 2 marks'),
       srp('Explanation', 13, f'Explanation · 13 x {SRPS}')),
      '3-3', EU_ECON, ID + 'p2-q7c'),
]

Q8AS = (L(24, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper.'),)
PART_TWO += romans('8A', P2, 24, L(24, 'Ordnance Survey Map'), Q8AS, ID + 'p2-q8a', ('map', 'legend'), [
    ('(i)', 16, L(24, '(i) Draw a sketch map of the area shown to half scale.', 'congestion on the N62.'),
     S(23, '(a) · Proportion/Outline', '(ii) · Explain briefly'),
     (fixed('Proportion/outline', 4, '(a) · Proportion/Outline: · 4 marks (4/0)', (0, 4)),
      Criterion('Feature 1', 4, SHOWN_LABEL, 'exact',
                ('2 features @ 4 marks each: Shown 3 marks graded (3/1/0)', '=Label 1 mark@0')),
      Criterion('Feature 2', 4, SHOWN_LABEL, 'exact',
                ('2 features @ 4 marks each: Shown 3 marks graded (3/1/0)', '=Label 1 mark@0')),
      Criterion('By-pass', 4, SHOWN_LABEL, 'exact',
                ('(b) · Bypass · 4 marks: · Shown 3 marks graded (3/1/0)', '=Label 1 mark@1'))),
     '2-6', MAP + ECON, (None, L(24, 'The built-up area of Templemore'), L(24, 'The entire route of the N62 road.'),
                         None)),
    ('(ii)', 4, L(24, '(ii) Explain briefly one disadvantage of such a by-pass for Templemore.'),
     S(23, '(ii) · Explain briefly', None), (pair('Valid explanation: · 2m + 2m', 'Disadvantage'),),
     '3-0', ECON + MAP),
])
PART_TWO += [
    T('p2-8b', P2, '8B', '', 30, 24, L(24, 'The Global Economy'),
      (L(24, 'Examine the mobility of modern economic activity with reference to example(s)', 'that you have studied.'),),
      (S(24, 'Example of modern economic activity', '8C.'),),
      (fixed('Example of modern economic activity', 2, 'Example of modern economic activity · 2 marks'),
       srp('Examination', 14, f'Examination · 14 x {SRPS}')),
      '3-2', MNC, ID + 'p2-q8b'),
    T('p2-8c', P2, '8C', '', 30, 24, L(24, 'Renewable Energy'),
      (L(24, 'With reference to one specific renewable energy source', 'Environmental advantages.'),),
      (S(24, 'Renewable energy source identified', None, after='8C.'),),
      (fixed('Renewable energy source identified', 2, 'Renewable energy source identified · 2 marks'),
       srp('Explanation of economic advantages', 7, f'Explanation of Economic advantages · 7 x {SRPS}'),
       srp('Explanation of environmental advantages', 7, f'Explanation of Environmental advantages · 7 x {SRPS}')),
      '3-5', ENERGY, ID + 'p2-q8c'),
]

Q9AS = (L(25, 'Examine the graph above showing renewable energy as a percentage of total energy consumption',
          'following questions.'),)
PART_TWO += romans('9A', P2, 25, L(25, 'Renewable Energy', nth=0), Q9AS, ID + 'p2-q9a', ('page',), [
    ('(i)', 2, L(25, '(i) What was the difference between renewable energy as a percentage', 'Iceland in 2012?'),
     S(25, '(i) · 58', '(ii) · Denmark'), (fixed('Difference', 2, '(i) · 58 (%) · 2 marks'),), '2-0', TG),
    ('(ii)', 2, L(25, '(ii) Which country had the greatest increase in renewable energy', '2004 and 2016?'),
     S(25, '(ii) · Denmark', '(iii) · Iceland'), (fixed('Country', 2, '(ii) · Denmark · 2 marks'),), '2-0', TG),
    ('(iii)', 4, L(25, '(iii) Which country was exceeding its 2020 target by the greatest amount in 2016?'),
     S(25, '(iii) · Iceland', '(iv) · Valid'), (fixed('Country', 4, '(iii) · Iceland · 4 marks'),), '2-0', TG),
    ('(iv)', 8, L(25, '(iv) Explain briefly two reasons why Ireland was the country furthest', 'in 2016.'),
     S(25, '(iv) · Valid', '(v) · 2 valid'),
     (pair('(iv) · Valid explanation · 2 + 2 marks', 'First reason'), pair('=2 + 2 marks', 'Second reason')),
     '3-5', ENERGY),
    ('(v)', 4, L(25, '(v) Name two sources of renewable energy in Ireland.'),
     S(25, '(v) · 2 valid', None), (pair('(v) · 2 valid answers · 2 + 2 marks', 'Two sources'),), '3-5', ENERGY),
])
REASON_9B = ('3 reasons @ 10 marks each', 'For each reason:', 'Reason identified · 2 marks',
             'Map evidence / Aerial photograph evidence · 2 marks', f'Discussion · 3 x {SRPS}')
PART_TWO += [
    T('p2-9b', P2, '9B', '', 30, 25, L(25, 'Location of Economic Activity'),
      (L(25, 'Discuss three reasons why the Templemore area is a suitable location', 'secondary economic activity.'),
       L(25, 'Use evidence from the aerial photograph or the Ordnance Survey map to support each reason.')),
      (S(26, '3 reasons @ 10 marks each', '9C.'),),
      tuple(Criterion(f'Reason {n}', 10, evens(10), 'srp', REASON_9B) for n in (1, 2, 3)),
      '3-2', MNC + MAP + AER, ID + 'p2-q9b', ('aerial', 'map', 'legend')),
    T('p2-9c', P2, '9C', '', 30, 25, L(25, 'Economic Development – Developed Economy'),
      (L(25, 'Discuss how levels of economic development can change over time', 'that you have studied.'),),
      (S(26, 'Developed economy named', None, after='9C.'),),
      (fixed('Developed economy named', 2, 'Developed economy named · 2 marks'),
       srp('Discussion', 14, f'Discussion · 14 x {SRPS}')),
      '3-0', ECON, ID + 'p2-q9c'),
]

PART_TWO += romans('10A', P2, 26, L(26, 'Aerial Photograph'),
                   (L(26, 'Examine the aerial photograph accompanying this paper.'),), ID + 'p2-q10a', ('aerial',), [
    ('(i)', 16, L(26, '(i) Draw a sketch map of the aerial photograph, half the length and half the breadth.',
                  '(not named above).'),
     S(27, '(i) · (a) · Proportion/Outline', '(ii) · Valid'),
     (fixed('Proportion/outline', 4, '(i) · (a) · Proportion/Outline: · 4 marks (4/0)', (0, 4)),
      Criterion('Land-use 1', 4, SHOWN_LABEL, 'exact',
                ('2 features @ 4 marks each: Shown 3 marks graded (3/1/0)', '=Label 1 mark@0')),
      Criterion('Land-use 2', 4, SHOWN_LABEL, 'exact',
                ('2 features @ 4 marks each: Shown 3 marks graded (3/1/0)', '=Label 1 mark@0')),
      Criterion('Other land-use', 4, SHOWN_LABEL, 'exact',
                ('(b) · Land-use 4 marks · Shown 3 marks graded (3/1/0)', '=Label 1 mark@1'))),
     '2-8', AER + URB, (None, L(26, 'An ecclesiastical land-use'), L(26, 'A recreational land-use.'), None)),
    ('(ii)', 4, L(26, '(ii) With reference to the land-use shown and labelled by you in part (i)(b) above',
                  'for this land-use.'),
     S(27, '(ii) · Valid', None), (pair('(ii) · Valid explanation · 2m + 2m', 'Advantage'),), '4-3', URB + AER),
])
PART_TWO += [
    T('p2-10b', P2, '10B', '', 30, 26, L(26, 'Dynamics of Settlement'),
      (L(26, 'Examine Central Place Theory with reference to example(s) that you have studied.'),),
      (S(28, 'Example · 2 marks', '10C.'),),
      (fixed('Example', 2, 'Example · 2 marks'), srp('Examination', 14, f'Examination · 14 x {SRPS}')),
      '4-3', URB, ID + 'p2-q10b'),
    T('p2-10c', P2, '10C', '', 30, 26, L(26, 'Migration'),
      (L(26, 'Discuss the impact of migration on rural areas in Ireland.'),),
      (S(28, 'Impact identified · 2 marks', None, after='10C.'),),
      (fixed('Impact identified', 2, 'Impact identified · 2 marks'), srp('Discussion', 14, f'Discussion · 14 x {SRPS}')),
      '4-2', POP, ID + 'p2-q10c'),
]

Q11AS = (L(27, 'Examine the graph above showing the number of immigrants arriving to Ireland and Greece',
           'following questions.'),)
LAND_USES = ('Industrial land-use', 'Residential land-use', 'Commercial land-use.')
PART_TWO += romans('11A', P2, 27, L(27, 'European Immigration'), Q11AS, ID + 'p2-q11a', ('page',), [
    ('(i)', 2, L(27, '(i) In which year was immigration to Greece at its lowest?'),
     S(29, '(i) · 2014', '(ii) · 2011'), (fixed('Year', 2, '(i) · 2014 · 2 marks'),), '2-0', TG),
    ('(ii)', 4, L(27, '(ii) In which two years was immigration to Greece greater than immigration to Ireland?'),
     S(29, '(ii) · 2011', '(iii) · Valid'), (pair('(ii) · 2011 & 2016 · 2 + 2 marks', 'Two years'),), '2-0', TG),
    ('(iii)', 4, L(27, '(iii) Explain briefly one negative impact of the change in immigration to Greece',
                   '2014 to 2016.'),
     S(29, '(iii) · Valid', '(iv) · 48.68'), (pair('(iii) · Valid answer · 2 +2 marks', 'Negative impact'),),
     '4-2', POP),
    ('(iv)', 4, L(27, '(iv) Calculate the percentage change in immigration to Ireland from 2011 to 2016.'),
     S(29, '(iv) · 48.68', '(v) · Decreased'), (fixed('Percentage change', 4, '(iv) · 48.68 (%) · 4 marks'),),
     '2-0', TG),
    ('(v)', 6, L(27, '(v) What was the trend in immigration to Ireland between 2005 and 2011', 'this trend.'),
     S(29, '(v) · Decreased', None),
     (fixed('Trend', 2, '(v) · Decreased · 2 marks'), pair('One valid answer · 2 + 2 marks', 'Reason')), '4-2', POP),
])
PART_TWO += [
    T('p2-11b', P2, '11B', '', 30, 27, L(27, 'Urban Land-Use'),
      (L(27, 'Examine how the location of two of the following land-uses has changed', 'Commercial land-use.'),),
      (S(30, 'Named city', '11C.'),),
      (fixed('City named', 2, 'Named city · 2 marks'),
       srp('Examination of land-use 1', 7, f'Examination of land-use 1 · 7 x {SRPS}'),
       srp('Examination of land-use 2', 7, f'Examination of land-use 2 · 7 x {SRPS}')),
      '4-4', LAND + URB, ID + 'p2-q11b', absorbs=pool(ID + 'p2-q11b-', LAND_USES, 2)[1]),
    T('p2-11c', P2, '11C', '', 30, 27, L(27, 'Overpopulation'),
      (L(27, 'Describe and explain the causes of overpopulation.'),),
      (S(30, 'Causes identified', None, after='11C.'),),
      (pair('Causes identified · 2 + 2 marks', 'Causes identified'),
       srp('Description/explanation', 13, f'Description/explanation · 13 x {SRPS}')),
      '4-1', POP, ID + 'p2-q11c'),
]

Q12AS = (L(28, 'Examine the data above showing population change (in thousands) in Ireland', 'following questions.'),)
PART_TWO += romans('12A', P2, 28, L(28, 'Population Dynamics'), Q12AS, ID + 'p2-q12a', ('page',), [
    ('(i)', 16, L(28, '(i) Using graph paper, draw a suitable graph to illustrate this data.'),
     S(31, 'Bar Chart · Pie Chart', '(ii) · Birth'), GRAPH, '2-0', TG),
    ('(ii)', 4, (L(28, '(ii) Birth rates and death rates are factors that influence population change.'),
                 L(28, 'Explain briefly any one other factor that influenced population change', '2012 to 2018.')),
     S(31, '(ii) · Birth', None), (pair('Valid explanation · 2m + 2m', 'Factor'),), '4-0', POP),
])
PHASE = ('(ii) · Explanation of each phase', '@ 6 marks each · 3 @ (2 + 2 + 2 marks)')
Q12BS = (L(28, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper and answer',
           'following questions.'),)
Q12BI = L(28, '(i) Name and locate using six-figure grid references', 'Ordnance Survey map.')
PART_TWO += romans('12B', P2, 28, L(28, 'Historical Settlement'), Q12BS, ID + 'p2-q12b', ('map', 'legend'), [
    ('(i)', 12, Q12BI, S(32, '(i) · Three historical', '(ii) · Explanation'),
     (fixed('Three historical phases named', 6, '(i) · Three historical phases named · 2 + 2 + 2 marks', (0, 2, 4, 6)),
      fixed('Location of each phase', 6, 'Location of each phase named · 2 + 2 + 2 marks', (0, 2, 4, 6))),
     '4-3', URB + MAP),
    ('(ii)', 18, L(28, '(ii) Explain briefly each of the three phases of historical settlement', 'part (i) above.'),
     S(32, '(ii) · Explanation', '12C.'),
     tuple(Criterion(f'Phase {n}', 6, evens(6), 'srp', PHASE) for n in (1, 2, 3)), '4-3', URB + MAP),
])
PART_TWO.append(T(
    'p2-12c', P2, '12C', '', 30, 28, L(28, 'Urban Problems'),
    (L(28, 'Discuss the problems that can arise from the growth of cities in the developing world.'),),
    (S(32, 'Problems identified', None, after='12C.'),),
    (pair('Problems identified · 2 + 2 marks', 'Problems identified'), srp('Discussion', 13, f'Discussion · 13 x {SRPS}')),
    '4-5', URB, ID + 'p2-q12c'))
# 12B(ii) is introduced by (i) on the page; its card carries (i) as context.
PART_TWO[-2] = Task(**{**PART_TWO[-2].__dict__, 'stem': (*Q12BS, Q12BI)})

# ------------------------------------------------------------------ Options --
OC = (S(34, '*Overall Coherence (20 marks)', None, table=True),)
OPTION_CRITERIA = (
    Criterion('Aspects (3 @ 20 marks or 4 @ 15 marks)', 60, upto(60), 'srp',
              ('Number of aspects', '?For each aspect:', 'Identifying aspect', '8 x SRP')),
    Criterion('Overall coherence', 20, (0, 6, 10, 14, 17, 20), 'exact',
              ('Overall Coherence · 20 marks graded*', '*Overall Coherence (20 marks)', 'Excellent · 20',
               'Very Good · 17', 'Good · 14', 'Fair · 10', 'Weak · 6', 'Poor · 0')))


def option(q, page, theme, note_nth, prompt, scheme_page, topic, atlas, after=None, end=None, routes=(),
           card_id=None):
    return T(f'p2-{q}', P2, q, '', 80, page, theme, prompt if isinstance(prompt, tuple) else (prompt,),
             (S(scheme_page, 'Number of aspects', end, None, after), *OC), OPTION_CRITERIA,
             topic, (atlas,), card_id or ID + f'p2-q{q}',
             stem=(L(page, 'Note: It is better to discuss three or four aspects', 'large number of points.',
                     nth=note_nth),),
             routes=routes)


GI, GE = H + 'option-global-interdependence', H + 'option-geoecology'
CI, AO = H + 'option-culture-identity', H + 'option-atmosphere-ocean'
ISSUES = ('Deforestation', 'Global warming', 'Desertification.')
OPTIONS = [
    option('13', 30, L(30, 'Global Interdependence'), 0,
           L(30, 'Discuss the impact of global trading patterns in relation to both producer and consumer regions',
             'that you have studied.'), 35, '5-1', GI, after='13.', end='14.'),
    option('14', 30, L(30, 'Global Interdependence'), 0,
           L(30, 'Discuss how aid programmes can help and hinder development.'), 35, '5-2', GI, after='14.'),
    option('15', 30, L(30, 'Global Interdependence'), 0,
           L(30, 'Examine the causes and impacts of any one of the following global environmental issues:',
             'Desertification.'), 36, '5-1', GI,
           routes=bullet_routes('p2-q15-', ISSUES), card_id=ID + 'p2-q15-deforestation'),
    option('16', 30, L(30, 'Geoecology'), 1,
           L(30, 'Examine how each of the following impact on soil characteristics:', 'Conservation methods.'),
           37, '6-1', GE, after='16.', end='17.'),
    option('17', 30, L(30, 'Geoecology'), 1,
           L(30, 'Examine the influence of mineral matter, air, water and organic matter on soil development.'),
           37, '6-0', GE, after='17.'),
    option('18', 30, L(30, 'Geoecology'), 1,
           L(30, 'Biomes are altered by human activity.', 'Discuss.'), 38, '6-3', GE),
    option('19', 31, L(31, 'Culture and Identity'), 0,
           L(31, 'Identity as a concept entails a variety of cultural factors', 'that you have studied.'),
           39, '7-2', CI, after='19.', end='20.'),
    option('20', 31, L(31, 'Culture and Identity'), 0,
           L(31, 'Conflict can arise between political structures and cultural groups.', 'Discuss.'),
           39, '7-1', CI, after='20.'),
    option('21', 31, L(31, 'Culture and Identity'), 0,
           L(31, 'Examine the impact of the movement of people on racial patterns.'), 40, '7-0', CI),
    option('22', 31, L(31, 'The Atmosphere – Ocean Environment'), 1,
           L(31, 'Examine how solar energy is redistributed through circulation patterns', 'oceans.'),
           41, '8-3', AO, after='22.', end='23.'),
    option('23', 31, L(31, 'The Atmosphere – Ocean Environment'), 1,
           L(31, 'Exchanges of water between oceans and atmosphere', 'Discuss.'), 41, '8-2', AO, after='23.'),
    option('24', 31, L(31, 'The Atmosphere – Ocean Environment'), 1,
           L(31, 'Describe and account for the specific characteristics of one global climate type', 'studied.'),
           42, '8-4', AO),
]

TASKS = [*PART_ONE, *PART_TWO, *OPTIONS]

ID_CORRECTION_REASON = 'No 2019 Higher card shipped before this review; every card is new.'

# No 2019 Higher card was live on origin/main before this review.
LEGACY_IDS: list[str] = []
