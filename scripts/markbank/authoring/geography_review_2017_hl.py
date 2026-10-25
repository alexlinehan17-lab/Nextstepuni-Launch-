"""Independent review ledger: Leaving Certificate Geography 2017 Higher Level.

Sources (English editions, harvested Paper Trail corpus; sizes and SHA-256
pinned in EXPECTED_SOURCES and the generated audit): the examination paper
LC005ALP000EV (32 pages; one booklet printed Part One, answered in it, and
Part Two), marking scheme LC005ALP000EV (52 pages), and the common Macroom
companions as Paper Trail files them — the 1:50 000 map LC005CLP003EV (a
one-page PDF holding a 1136 x 784 pixel image: legible at full size, but
lower resolution than later years), its legend LC005CLPC00EV and the aerial
photograph LC005CLP004EV (one-page PDFs). Part One is 80 marks (any ten of
twelve @ 8), Part Two 320 (four questions @ 80).

Visual sweep (every page rendered and read on 2026-10-14):
  Paper p1 cover and examiner's grid; p2-p13 Part One Questions 1-12, one a
  page (Q8 prints an elevation profile, Q9 a street map of part of
  Macroom); p14 Part Two instructions; p15 Section 1 divider; p16-p21
  Q1-Q6 (p16 and p19 open with their dividers); p22 Section 2 divider;
  p23-p28 Electives Q7-Q12 (p23 and p26 open with their elective
  dividers); p29 Section 3 divider and option note; p30-p31 Options
  Q13-Q24; p32 printed "Blank Page".
  Scheme p1 cover; p2-p3 notes; p4 Part One table (two columns: Q1-Q6,
  Q7-Q12; Q2 and Q4 print (i) and (ii) side by side); p5 Part Two
  instructions and Section 1 divider; p6-p13 Q1-Q3; p14-p19 Q4-Q6; p20
  Section 2 divider; p21-p26 Q7-Q9; p27-p32 Q10-Q12; p33 Section 3
  divider; p34 option outline and Overall Coherence descriptors; p35-p42
  Q13-Q24; p43-p46 Geographical Investigation (coursework); p47
  investigation topics; p48 Irish-language bonus marks; p49-p51 printed
  "Blank Page"; p52 back cover.
  Companions: Macroom map extract (the River Lee, the Reservoir, Lee
  Bridge, Cill na Martra); OS legend sheet; oblique aerial photograph of
  Macroom.

Boundaries and tariffs follow the 2018 Higher ledger. Matching tables, in
the printed row order: Q1 Asymmetrical fold B, Overthrust fold A,
Symmetrical fold D (Unfolded strata C is printed); Q2 Pater noster lake,
Ox-bow lake, Tarn, Turlough = (i) B, A, D, C and (ii) Glacial, Fluvial,
Glacial, Karst; Q3 Sand spit D, Tombolo A, Sand dunes C, Lagoon B; Q4
Oxidation, Carbonation, Exfoliation/Onion weathering, Freeze-thaw action =
(i) D, A, B, C and (ii) Chemical, Chemical, Phy/Mech, Phy/Mech; Q5 by the
printed types: The Burren, Northern European Plain, Wallonia, Rotterdam,
Pas de Calais, Waterford Co Council, Islamic World, Temperate Oceanic; Q6
W 29 69 River braiding, W 36 72 "V-shaped valley or Meander" (as printed),
W 34 72 Plateau, W 28 73 Meander; Q9 B Centre foreground, C Left
middleground, D Centre middleground, E Centre background (A is printed).
Q8's eight true/false statements are separately priced romans.

Printed choices: 1C, 2B, 2C, 9B and 11C are one route per printed option;
3A(v) thermal or regional metamorphism and 12C's evidence (the aerial
photograph OR the Ordnance Survey map) are routes; 3B (i) or (ii), with
(i)'s one fluvial, coastal or glacial landform a route each. 6B (two of
four factors), 10C (two of three issues) and options 13 and 16 (three of
four) are pools, one card each. Options 13, 16 and 18 print only the
"3 @ 20 marks" outline and are carded with it.

Scheme as printed: 9A(ii) prices "($) 400 billion · 4 marks or ($) 400 ·
2 marks", so its card offers 0, 2 or 4.
"""

from geography_review import (
    Criterion, Lift, Route, SchemeSlice, Task, pool, evens, fixed, slug, srp, sums, upto,
)

YEAR = 2017
LEVEL = 'higher'
PAPER_PAGES = {1: 32, 2: 32}
SCHEME_PAGES = 52
QUESTION_TARIFFS = {1: {str(n): 8 for n in range(1, 13)},
                    2: {**{f'{n}{x}': (20 if x == 'A' else 30)
                           for n in range(1, 13) for x in 'ABC'},
                        **{str(n): 80 for n in range(13, 25)}}}

EXPECTED_SOURCES = {
    'paper1': ('LC005ALP000EV.pdf', 4054502),
    'paper2': ('LC005ALP000EV.pdf', 4054502),
    'scheme': ('LC005ALP000EV.pdf', 1065118),
    'map': ('LC005CLP003EV.pdf', 352988),
    'legend': ('LC005CLPC00EV.pdf', 745443),
    'aerial': ('LC005CLP004EV.pdf', 602913),
}

_PAPER = {1: 'cover and examiner grid', **{p: 'question' for p in range(2, 14)},
          14: 'Part Two instructions', 15: 'section divider', **{p: 'question' for p in range(16, 22)},
          22: 'section divider', **{p: 'question' for p in range(23, 29)}, 29: 'section divider and option note',
          30: 'question', 31: 'question', 32: 'blank page'}
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
    [1, 2, 'attempt any ten'], [1, 7, 'any two'], [1, 14, 'attempt four'], [1, 15, 'attempt two'],
    [1, 16, 'attempt one'], [1, 16, 'one of the following'],
    [1, 17, 'one of the following'], [1, 17, 'one of the following'],
    [1, 18, 'either'], [1, 18, 'answer (i) or (ii)'],
    [1, 19, 'attempt one'],
    [1, 21, 'two of the following'],
    [1, 22, 'attempt one'],
    [1, 23, 'choose'], [1, 23, 'choose'],
    [1, 25, 'one of the following'],
    [1, 26, 'any two'],
    [1, 27, 'any one'],
    [1, 29, 'attempt one'],
    [1, 30, 'any three'], [1, 30, 'any three'],
]
SELECTION_REVIEW = [
    {'scan': [[1, 2, 'attempt any ten'], [1, 14, 'attempt four'], [1, 15, 'attempt two'], [1, 16, 'attempt one'],
              [1, 19, 'attempt one'], [1, 22, 'attempt one'], [1, 29, 'attempt one']],
     'kind': 'exam-attempt-rule',
     'reason': 'Part One any ten of twelve and Part Two four questions (one of Q1-3, one of Q4-6, one elective, one option) are attempt rules; every question is carded.'},
    {'scan': [[1, 18, 'answer (i) or (ii)']], 'kind': 'closed-route',
     'reason': '3B: (i) or (ii); (i) offers one fluvial, coastal or glacial landform -> 4 routes. 12C (evidence from the aerial photograph OR the Ordnance Survey map, not both) -> 2 routes, each with its own evidence.'},
    {'scan': [[1, 18, 'either']], 'kind': 'closed-route',
     'reason': '3A(v): either thermal metamorphism or regional metamorphism -> 2 routes under one allocation.'},
    {'scan': [[1, 16, 'one of the following'], [1, 17, 'one of the following'], [1, 17, 'one of the following'],
              [1, 25, 'one of the following'], [1, 27, 'any one']],
     'kind': 'closed-choose-one',
     'reason': '1C one of three printed impacts -> 3 routes; 2B the surface or the underground karst landscape -> 2 routes; 2C one of three printed features -> 3 routes; 9B one of three printed activities -> 3 routes; 11C any one of four printed factors -> 4 routes.'},
    {'scan': [[1, 21, 'two of the following'], [1, 26, 'any two'], [1, 30, 'any three'], [1, 30, 'any three']],
     'kind': 'choose-n-one-card',
     'reason': '6B two of four printed factors, 10C any two of three printed issues, options 13 and 16 any three of four printed items -> one card each with every printed item (choice is not a route).'},
    {'scan': [[1, 7, 'any two']], 'kind': 'open-response',
     'reason': 'No printed pool: Part One Q6(iii) any two river drainage patterns. Compulsory lists stay whole: 1A, 4A, 8A, 10A each bullet, 1B, 5C and 18 each item.'},
    {'scan': [[1, 23, 'choose'], [1, 23, 'choose']], 'kind': 'not-a-selection',
     'reason': '7B "might choose to locate" / "might choose not to locate" describes the company, not a candidate choice.'},
]

P1, P2 = 1, 2
LEFT = (0.0, 0.0, 0.455, 1.0)
RIGHT = (0.455, 0.0, 1.0, 1.0)
Q2I = (0.0, 0.30, 0.25, 0.39)
Q2II = (0.25, 0.30, 0.455, 0.39)
Q4I = (0.0, 0.565, 0.24, 0.65)
Q4II = (0.24, 0.565, 0.455, 0.65)
ID = 'geography-2017-hl-'
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
    """parts: (sub, marks, prompt Lift(s), scheme slice(s), criteria, topic, atlas[, row labels[, extra stem]])."""
    out = []
    for index, item in enumerate(parts):
        sub, marks, prompt, scheme, criteria, topic, atlas = item[:7]
        labels = item[7] if len(item) > 7 else ()
        extra = item[8] if len(item) > 8 else ()
        key = sub.strip('()').replace(')(', '-')
        out.append(T(f'p{part}-{q.lower()}-{key}', part, q, sub, marks, page, title,
                     prompt if isinstance(prompt, tuple) else (prompt,),
                     scheme if isinstance(scheme, tuple) else (scheme,), criteria, topic, atlas,
                     first_id if index == 0 else f'{first_id}-{key}', sources, (*stem, *extra),
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
PART_ONE = romans('1', P1, 2, L(2, 'Folding'),
                  (L(2, 'Examine the diagrams above and answer each of the following questions.'),),
                  ID + 'p1-q1', ('page',), [
    ('(i)', 6, L(2, '(i) Match each of the diagrams A, B, C and D with the type of fold', 'One is completed for you.'),
     S(4, 'Q.1 · (i)', '(ii) · Caledonian', LEFT), rows(['Q.1 · (i) · B 2m', '=A 2m', '=D 2m'], 2), '0-2', PS + RW,
     (L(2, 'Asymmetrical fold'), L(2, 'Overthrust fold'), L(2, 'Symmetrical fold'))),
    ('(ii)', 2, L(2, '(ii) Name two periods of Fold Mountain building', '400 million years.'),
     S(4, '(ii) · Caledonian', 'Q.2', LEFT),
     (fixed('Period 1', 1, '(ii) · Caledonian 1m'), fixed('Period 2', 1, 'Armorican 1m')), '0-2', PS + RW),
])
Q2_ROWS = (L(3, 'Pater noster lake'), L(3, 'Ox-bow lake'), L(3, 'Tarn'), L(3, 'Turlough'))
PART_ONE += romans('2', P1, 3, L(3, 'The Physical Environment'),
                   (L(3, 'Examine the photographs above and answer each of the following questions.'),),
                   ID + 'p1-q2', ('page',), [
    ('(i)', 4, L(3, '(i) Match each of the photographs A, B, C and D with the type of lake', 'table below.'),
     S(4, 'Q.2 · (i)', None, Q2I), rows(['Q.2 · (i) · B 1m', '=A 1m', '=D 1m', '=C 1m']), '0-4',
     GLAC + RIVERS + KARST, Q2_ROWS),
    ('(ii)', 4, L(3, '(ii) Indicate, by ticking the correct box whether each of the types of lake',
                  'karst landscapes.'),
     S(4, '(ii) Glacial', None, Q2II), rows(['(ii) Glacial 1m', '=Fluvial 1m', '=Glacial 1m', '=Karst 1m']), '0-4',
     GLAC + RIVERS + KARST, Q2_ROWS),
])
PART_ONE += romans('3', P1, 4, L(4, 'Coastal Landscape'),
                   (L(4, 'Examine the aerial photographs above and answer each of the following questions.'),),
                   ID + 'p1-q3', ('page',), [
    ('(i)', 4, L(4, '(i) Match each of the aerial photographs A, B, C and D with the landform', 'table below.'),
     S(4, 'Q.3 · (i)', '(ii) · Any valid', LEFT), rows(['Q.3 · (i) · D 1m', '=A 1m', '=C 1m', '=B 1m']), '0-10', SEA,
     (L(4, 'Sand spit'), L(4, 'Tombolo'), L(4, 'Sand dunes'), L(4, 'Lagoon'))),
    ('(ii)', 2, L(4, '(ii) Name one process of coastal transportation associated with the formation of sand spits',
                  'tombolos.'),
     S(4, '(ii) · Any valid', '(iii) · Groynes', LEFT), (fixed('Process', 2, '(ii) · Any valid process 2m'),),
     '0-10', SEA),
    ('(iii)', 2, L(4, '(iii) Name the coastal defence structures shown at X in photograph D.'),
     S(4, '(iii) · Groynes', 'Q.4', LEFT), (fixed('Structures', 2, '(iii) · Groynes 2m'),), '0-10', SEA),
])
Q4_ROWS = (L(5, 'Oxidation'), L(5, 'Carbonation'), L(5, 'Exfoliation/Onion weathering'), L(5, 'Freeze-thaw action'))
PART_ONE += romans('4', P1, 5, L(5, 'Weathering', nth=0),
                   (L(5, 'Examine the photographs above and answer each of the following questions.'),),
                   ID + 'p1-q4', ('page',), [
    ('(i)', 4, L(5, '(i) Match each of the photographs A, B, C and D with the process of weathering',
                 'table below.'),
     S(4, 'Q.4 · (i)', None, Q4I), rows(['Q.4 · (i) · D 1m', '=A 1m', '=B 1m', '=C 1m']), '0-8', RW, Q4_ROWS),
    ('(ii)', 4, L(5, '(ii) Indicate, by ticking the correct box whether each of the processes of weathering',
                  'physical/mechanical weathering.'),
     S(4, '(ii) Chemical', None, Q4II),
     rows(['(ii) Chemical 1m', '=Chemical 1m', '=Phy/Mech 1m@0', '=Phy/Mech 1m@1']), '0-8', RW, Q4_ROWS),
])
PART_ONE.append(T(
    'p1-5', P1, '5', '', 8, 6, L(6, 'Regions'),
    (L(6, 'Complete the table by matching each of the examples of regions in the list below',
       'most associated with it.'),
     Lift(6, 'Wallonia', 'Northern European Plain', row=True)),
    (S(4, 'Q.5', 'Q.6', LEFT),),
    rows(['Q.5 · The Burren 1m', 'Northern European Plain 1m', 'Wallonia 1m', 'Rotterdam 1m', 'Pas de Calais 1m',
          'Waterford Co Council 1m', 'Islamic World 1m', 'Temperate Oceanic 1m']),
    '1-0', IRL + EURO, ID + 'p1-q5', ('page',),
    row_labels=(L(6, 'Geomorphological', nth=0), L(6, 'Geomorphological', nth=1), L(6, 'Cultural (Language)'),
                L(6, 'Nodal'), L(6, 'Administrative', nth=0), L(6, 'Administrative', nth=1),
                L(6, 'Cultural (Religion)'), L(6, 'Climatic'))))
PART_ONE += romans('6', P1, 7, L(7, 'Landscape Identification'), (), ID + 'p1-q6', ('map', 'legend'), [
    ('(i)', 4, L(7, '(i) Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper.', 'Meander.'),
     S(4, 'Q.6 · (i)', '(ii) · North West', LEFT),
     rows(['Q.6 · (i) · River braiding 1m', 'V-shaped valley or Meander 1m', 'Plateau 1m', '=Meander 1m']), '2-6',
     MAP + RIVERS, (L(7, 'W 29 69'), L(7, 'W 36 72'), L(7, 'W 34 72'), L(7, 'W 28 73'))),
    ('(ii)', 2, L(7, '(ii) What is the aspect of the slope at W 308 652', 'accompanying this paper?'),
     S(4, '(ii) · North West', '(iii) · Two valid', LEFT), (fixed('Aspect', 2, '(ii) · North West 2m'),), '2-6', MAP),
    ('(iii)', 2, L(7, '(iii) Name any two river drainage patterns.'),
     S(4, '(iii) · Two valid', None, LEFT), (one_plus_one('(iii) · Two valid patterns 1+1m', 'Two drainage patterns'),),
     '0-9', RIVERS),
])
PART_ONE += romans('7', P1, 8, L(8, 'Ordnance Survey Map'),
                   (L(8, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper and answer',
                      'following questions.'),),
                   ID + 'p1-q7', ('map', 'legend'), [
    ('(i)', 2, L(8, '(i) Name the antiquity located at W 293 734.'),
     S(4, 'Q.7 · (i)', '(ii) · Nature', RIGHT), (fixed('Antiquity', 2, 'Q.7 · (i) · Castle 2m'),), '2-6', MAP),
    ('(ii)', 2, L(8, '(ii) What does the Ordnance Survey map symbol at W 328 712 represent?'),
     S(4, '(ii) · Nature', '(iii) · 1.8', RIGHT), (fixed('Symbol', 2, '(ii) · Nature Reserve 2m'),), '2-6', MAP),
    ('(iii)', 2, L(8, '(iii) Measure the length of the R618 road, in kilometres', 'W 353 725.'),
     S(4, '(iii) · 1.8', '(iv) · 10-12', RIGHT), (fixed('Length', 2, '(iii) · 1.8 – 2.2 (km) 2m'),), '2-6', MAP),
    ('(iv)', 2, L(8, '(iv) Calculate the approximate area of the map', '(in square kilometres).'),
     S(4, '(iv) · 10-12', 'Q.8', RIGHT), (fixed('Area', 2, '(iv) · 10-12 (km2) 2m'),), '2-6', MAP),
])
Q8S = (L(9, 'Locate point X, W 340 740, and point Y', 'between point X and point Y.'),
       L(9, 'Using the 1:50 000 Ordnance Survey map and legend and the elevation profile above', 'in each case.'))
Q8 = (('(i)', 'The river Lee is located at A.', 'Q.8 · (i)', '(ii) · False', 'Q.8 · (i) · False 1m'),
      ('(ii)', 'B is located in the Sleveen West townland.', '(ii) · False', '(iii) · True', '(ii) · False 1m'),
      ('(iii)', 'The R584 regional road is located at C.', '(iii) · True', '(iv) · False', '(iii) · True 1m'),
      ('(iv)', 'The slope between B and C is concave.', '(iv) · False', '(v) · True', '(iv) · False 1m'),
      ('(v)', 'Part of the built up area of Macroom lies on a concave slope.', '(v) · True', '(vi) · True',
       '(v) · True 1m'),
      ('(vi)', 'The slope of the cross section between C and D is zero.', '(vi) · True', '(vii) · False',
       '(vi) · True 1m'),
      ('(vii)', 'The height at F is 160 metres.', '(vii) · False', '(viii) · True', '(vii) · False 1m'),
      ('(viii)', 'There is a constant or even slope between E and F.', '(viii) · True', 'Q.9', '(viii) · True 1m'))
PART_ONE += romans('8', P1, 9, L(9, 'Elevation profile'), Q8S, ID + 'p1-q8', ('page', 'map', 'legend'), [
    (roman, 1, L(9, f'{roman} {statement}'), S(4, start, end, RIGHT, 'Q.8'), (fixed('True or false', 1, line),),
     '2-6', MAP) for roman, statement, start, end, line in Q8])
PART_ONE.append(T(
    'p1-9', P1, '9', '', 8, 10, L(10, 'Aerial Photograph – Location'),
    (L(10, 'Locate each of the features labelled A, B, C, D and E above', 'One has been completed for you.'),),
    (S(4, 'Q.9', 'Q.10 (i)', RIGHT),),
    rows(['Q.9 · B · Centre foreground 2m', 'C · Left middleground 2m', 'D · Centre middleground 2m',
          'E · Centre background 2m'], 2),
    '2-8', AER + URB, ID + 'p1-q9', ('page', 'aerial'),
    (L(10, 'Examine the aerial photograph of Macroom accompanying this paper.'),
     L(10, 'Examine the street map below of part of the area covered by the aerial photograph.'),
     L(10, 'Note: The orientation of the aerial photograph', 'street map below.')),
    row_labels=(L(10, 'B Terraced housing'), L(10, 'C St Joseph’s Primary School'), L(10, 'D South Square'),
                L(10, 'E Road'))))
PART_ONE += romans('10', P1, 11, L(11, 'Weather'),
                   (L(11, 'Examine the rainfall forecast charts for a period from 00:00 hours to 18:00 hours',
                      'following questions.'),),
                   ID + 'p1-q10', ('page',), [
    ('(i)', 2, L(11, '(i) Which province is forecast to receive the least amount of rainfall over the period?'),
     S(4, 'Q.10 (i)', '(ii) · False', RIGHT), (fixed('Province', 2, 'Q.10 (i) · Ulster 2m'),), '2-7', WX),
    ('(ii)', 2, (L(11, '(ii) Indicate whether the following statement is true or false by circling the correct option.'),
                 L(11, 'Rainfall is spreading from the south-east at 06:00 hours.')),
     S(4, '(ii) · False 2m', '(iii) · Depressions', RIGHT), (fixed('True or false', 2, '(ii) · False 2m'),), '2-7', WX),
    ('(iii)', 2, L(11, '(iii) Is rainfall most associated with anticyclones or depressions?'),
     S(4, '(iii) · Depressions', '(iv) · Isohyets', RIGHT), (fixed('Pressure system', 2, '(iii) · Depressions 2m'),),
     '2-7', WX),
    ('(iv)', 2, L(11, '(iv) What term is used to describe lines on a weather map joining places of equal rainfall?'),
     S(4, '(iv) · Isohyets', 'Q.11', RIGHT), (fixed('Term', 2, '(iv) · Isohyets 2m'),), '2-7', WX),
])
PART_ONE += romans('11', P1, 12, L(12, 'Statistical Interpretation'),
                   (L(12, 'Examine the table above showing the percentage of the population in selected regions',
                      'following questions.'),),
                   ID + 'p1-q11', ('page',), [
    ('(i)', 2, L(12, '(i) Which region had the lowest percentage of its population using the internet in 2010?'),
     S(4, 'Q.11 (i)', '(ii) · West', RIGHT), (fixed('Region', 2, 'Q.11 (i) · Border 2m'),), '2-0', TG),
    ('(ii)', 2, L(12, '(ii) In which region did the percentage of the population using the internet remain the same',
                  '2012 and 2015?'),
     S(4, '(ii) · West', '(iii) · Dublin', RIGHT), (fixed('Region', 2, '(ii) · West 2m'),), '2-0', TG),
    ('(iii)', 2, L(12, '(iii) Which two regions had the highest percentage of their population using the internet',
                   'table above?'),
     S(4, '(iii) · Dublin', '(iv) · Valid explanation', RIGHT),
     (fixed('Region 1', 1, '(iii) · Dublin 1m'), fixed('Region 2', 1, 'Mid-East 1m')), '2-0', TG),
    ('(iv)', 2, L(12, '(iv) Explain briefly one reason why the percentage of the population using the internet in',
                  'the other regions.'),
     S(4, '(iv) · Valid explanation', 'Q.12', RIGHT), (one_plus_one('(iv) · Valid explanation 1+1m', 'Explanation'),),
     '1-4', IRL),
])
PART_ONE += romans('12', P1, 13, L(13, 'Housing Statistics – Ireland'),
                   (L(13, 'Examine the statistics above from the preliminary results of the 2016 Census',
                      'following questions.'),),
                   ID + 'p1-q12', ('page',), [
    ('(i)', 2, L(13, '(i) What was the total number of housing units in 2016?'),
     S(4, 'Q.12 (i)', '(ii) · 18,981', RIGHT), (fixed('Housing units', 2, 'Q.12 (i) · 2,022,895 2m'),), '2-0', TG),
    ('(ii)', 2, L(13, '(ii) Calculate X, the total change in the number of housing units between 2011 and 2016.'),
     S(4, '(ii) · 18,981', '(iii) · 6.3', RIGHT), (fixed('X', 2, '(ii) · 18,981 2m'),), '2-0', TG),
    ('(iii)', 2, L(13, '(iii) What percentage of housing units were vacant in Kildare?'),
     S(4, '(iii) · 6.3', '(iv) · Two valid', RIGHT), (fixed('Percentage', 2, '(iii) · 6.3 (%) 2m'),), '2-0', TG),
    ('(iv)', 2, L(13, '(iv) State two possible reasons why Leitrim had the highest percentage of vacant housing units.'),
     S(4, '(iv) · Two valid', None, RIGHT), (one_plus_one('(iv) · Two valid reasons 1+1m', 'Two reasons'),),
     '1-4', IRL),
])


# ---------------------------------------------------------------- Part Two --
def sketch(outline_line, outline_permitted, alloc, item_permitted, labels):
    return (fixed('Sketch outline' if 'Sketch' in outline_line else 'Map outline', 4,
                  outline_line, outline_permitted),
            *(Criterion(f'Feature {n}', 4, item_permitted, 'exact', alloc) for n in range(1, labels + 1)))


OS_SKETCH = sketch('Sketch Outline · 4 marks (4/0)', (0, 4),
                   ('4 features @ 4 marks each', 'Label 1 mark'), sums((0, 1, 3), (0, 1)), 4)
GRAPH = (fixed('Title', 2, ('Bar Chart · Pie Chart', 'Title · 2 marks · 2 marks')),
         fixed('Axes named (bar chart) / circle and centre (pie chart)', 2,
               ('Vertical axis named', 'Horizontal axis named'), (0, 1, 2)),
         fixed('6 items illustrated', 12, '6 items illustrated', upto(12)))


def split(label, total, first, second):
    return srp(label, total, (first, second))


def bullet_routes(prefix, items, atlas=None, labels=None):
    return tuple(Route(slug((labels or {}).get(item, item), 34), (labels or {}).get(item, item.rstrip('.')),
                       ID + prefix + slug((labels or {}).get(item, item), 34), False,
                       keep_bullets=(item,), atlas=(atlas[item] if atlas else None))
                 for item in items)


IMPACTS = ('The impact of flood control measures on river processes',
           'The impact of coastal defence measures on coastal processes',
           'The impact of human activities on mass movement processes.')
ROUTES_1C = bullet_routes('p2-q1c-', IMPACTS, atlas=dict(zip(IMPACTS, (RIVERS, SEA, RW))))
PART_TWO = [
    T('p2-1a', P2, '1A', '', 20, 16, L(16, 'Ordnance Survey Map'),
      (L(16, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper.', 'plantation at W 25 66.'),),
      (S(6, 'Sketch Outline', None),), OS_SKETCH, '2-6', MAP + RIVERS, ID + 'p2-q1a', ('map', 'legend'),
      row_labels=(None, L(16, 'The area of the Reservoir west of Lee Bridge'),
                  L(16, 'The course of the River Lee from W 250 667 to W 314 709'),
                  L(16, 'The entire area of land above 200 metres at Cill na Martra'),
                  L(16, 'The entire area of coniferous plantation at W 25 66'))),
    T('p2-1b', P2, '1B', '', 30, 16, L(16, 'Volcanic Activity'),
      (L(16, 'Examine the influence of volcanic activity on the development of the Irish landscape',
         'Extrusive features.'),),
      (S(7, 'Examination with reference to intrusive', None),),
      (split('Examination of intrusive and extrusive features (7/8 SRPs each)', 15,
             f'Examination with reference to intrusive features · 7/8 x {SRPS}',
             f'Examination with reference to extrusive features · 7/8 x {SRPS}'),),
      '0-7', EV, ID + 'p2-q1b'),
    T('p2-1c', P2, '1C', '', 30, 16, L(16, 'Human Interaction with Surface Processes'),
      (L(16, 'Human activity impacts on surface processes.'),
       L(16, 'Examine this statement with reference to one of the following:', 'mass movement processes.')),
      (S(8, 'Impact on process identified', None),),
      (fixed('Impact on process identified', 2, 'Impact on process identified · 2 marks'),
       srp('Examination', 14, f'Examination · 14 x {SRPS}')),
      '0-6', RIVERS, ROUTES_1C[0].card_id, routes=ROUTES_1C),
]

Q2AS = (L(17, 'Examine the diagram above and answer each of the following questions.'),)
PART_TWO += romans('2A', P2, 17, L(17, 'Adjustment to Base Level'), Q2AS, ID + 'p2-q2a', ('page',), [
    ('(i)', 8, L(17, '(i) Explain briefly two reasons why river rejuvenation occurs.'),
     S(9, '(i) · Reason 1', '(ii) · Valid'),
     (pair('(i) · Reason 1 explained · 2 + 2 marks', 'Reason 1'), pair('Reason 2 explained · 2 + 2 marks', 'Reason 2')),
     '0-9', RIVERS),
    ('(ii)', 4, L(17, '(ii) Explain briefly what is meant by the term knickpoint.'),
     S(9, '(ii) · Valid', '(iii) · Two features'), (pair('(ii) · Valid explanation · 2 + 2 marks', 'Explanation'),),
     '0-9', RIVERS),
    ('(iii)', 4, L(17, '(iii) Name two features of river rejuvenation not shown in the diagram above.'),
     S(9, '(iii) · Two features', '(iv) · Two ·'), (pair('(iii) · Two features named · 2 + 2 marks', 'Two features'),),
     '0-9', RIVERS),
    ('(iv)', 4, L(17, '(iv) How many times has river rejuvenation taken place in the diagram above?'),
     S(9, '(iv) · Two ·', None), (fixed('Number of times', 4, '(iv) · Two · 4 marks'),), '0-9', RIVERS),
])
KARST_ROUTES = ('The surface karst landscape or', 'The underground karst landscape.')
FEATURES_2C = ('Volcanoes', 'Earthquakes', 'Fold Mountains.')
PART_TWO += [
    T('p2-2b', P2, '2B', '', 30, 17, L(17, 'Chemical Weathering'),
      (L(17, 'With the aid of a labelled diagram(s), explain how chemical weathering has shaped one of the',
         'The underground karst landscape.'),),
      (S(10, 'Labelled diagram', '2C.'),),
      (fixed('Labelled diagram', 4, 'Labelled diagram · 4 marks (4/0)', (0, 4)),
       srp('Explanation', 13, f'Explanation · 13 x {SRPS}')),
      '0-3', KARST + RW, ID + 'p2-q2b-the-surface-karst-landscape',
      routes=bullet_routes('p2-q2b-', KARST_ROUTES,
                           labels={'The surface karst landscape or': 'The surface karst landscape',
                                   'The underground karst landscape.': 'The underground karst landscape'})),
    T('p2-2c', P2, '2C', '', 30, 17, L(17, 'The Tectonic Cycle'),
      (L(17, 'Examine how the tectonic cycle helps to explain the global distribution of one of the following:',
         'Fold Mountains.'),),
      (S(10, 'Reference to global distribution', None),),
      (pair('Reference to global distribution · 2 + 2 marks', 'Reference to global distribution'),
       srp('Examination', 13, f'Examination · 13 x {SRPS}')),
      '0-0', PS, ID + 'p2-q2c-volcanoes',
      routes=bullet_routes('p2-q2c-', FEATURES_2C, atlas=dict(zip(FEATURES_2C, (PS + EV, PS + EV, PS + RW))))),
]

Q3AS = (L(18, 'Examine the diagram of the rock cycle above and answer each of the following questions.'),)
METAMORPHISM = 'thermal metamorphism or regional metamorphism'
PART_TWO += romans('3A', P2, 18, L(18, 'Rock Cycle'), Q3AS, ID + 'p2-q3a', ('page',), [
    ('(i)', 4, L(18, '(i) Name the category of rock formed at A and the category of rock formed at B.'),
     S(11, '(i) · A · Igneous', '(ii) · C · Metamorphic'),
     (fixed('A', 2, '(i) · A · Igneous rock · 2 marks'), fixed('B', 2, 'B · Sedimentary rock · 2 marks')), '0-1', RW),
    ('(ii)', 4, L(18, '(ii) Name the category of rock formed at C and name one specific Irish location', 'can be found.'),
     S(11, '(ii) · C · Metamorphic', '(iii) · Valid'),
     (fixed('C', 2, '(ii) · C · Metamorphic rock · 2 marks'), fixed('Irish location', 2, 'One Irish location · 2 marks')),
     '0-1', RW),
    ('(iii)', 4, L(18, '(iii) Explain briefly what is meant by the term lithification.'),
     S(11, '(iii) · Valid', '(iv) · Valid'), (pair('(iii) · Valid explanation · 2 + 2 marks', 'Explanation'),),
     '0-1', RW),
    ('(iv)', 4, L(18, '(iv) Explain briefly what is meant by the term plutonic rock.'),
     S(11, '(iv) · Valid', '(v) · Valid'), (pair('(iv) · Valid explanation · 2 + 2 marks', 'Explanation'),),
     '0-1', RW),
])
PART_TWO.append(T(
    'p2-3a-v', P2, '3A', '(v)', 4, 18, L(18, 'Rock Cycle'),
    (L(18, '(v) Explain briefly how rocks are changed by either thermal metamorphism or regional', 'metamorphism.'),),
    (S(11, '(v) · Valid', None),), (pair('(v) · Valid explanation · 2 + 2 marks', 'Explanation'),),
    '0-1', RW, ID + 'p2-q3a-v-thermal-metamorphism', ('page',), Q3AS,
    routes=(Route('thermal-metamorphism', 'Thermal metamorphism', ID + 'p2-q3a-v-thermal-metamorphism', False,
                  ((METAMORPHISM, 'thermal metamorphism'),)),
            Route('regional-metamorphism', 'Regional metamorphism', ID + 'p2-q3a-v-regional-metamorphism', False,
                  ((METAMORPHISM, 'regional metamorphism'),)))))
LANDFORMS = 'one fluvial landform, coastal landform or glacial landform'
PART_TWO += [
    T('p2-3b', P2, '3B', '', 30, 18, L(18, 'Surface Processes'),
      (L(18, '(i) Examine the impact of the processes of erosion on the formation of one fluvial landform,',
         'that you have studied.'),),
      (S(12, 'Process of erosion named', 'Or'),),
      (fixed('Process of erosion named', 2, 'Process of erosion named · 2 marks'),
       fixed('Landform named', 2, 'Landform named · 2 marks'), srp('Examination', 13, f'Examination · 13 x {SRPS}')),
      '0-9', RIVERS, ID + 'p2-q3b-route-i-fluvial-landform',
      routes=(
          Route('route-i-fluvial-landform', 'Route (i) · one fluvial landform', ID + 'p2-q3b-route-i-fluvial-landform',
                False, ((LANDFORMS, 'one fluvial landform'),), topic='0-9', atlas=RIVERS),
          Route('route-i-coastal-landform', 'Route (i) · one coastal landform', ID + 'p2-q3b-route-i-coastal-landform',
                False, ((LANDFORMS, 'coastal landform'),), topic='0-10', atlas=SEA),
          Route('route-i-glacial-landform', 'Route (i) · one glacial landform', ID + 'p2-q3b-route-i-glacial-landform',
                False, ((LANDFORMS, 'glacial landform'),), topic='0-11', atlas=GLAC),
          Route('route-ii', 'Route (ii)', ID + 'p2-q3b-route-ii', False,
                prompt=(L(18, '(ii) Describe and explain the factors governing the operation of one mass movement',
                          'that you have studied.'),),
                scheme=(S(12, 'Mass movement process named', None),),
                criteria=(fixed('Mass movement process named', 2, 'Mass movement process named · 2 marks'),
                          pair('Factors identified · 2 + 2 marks', 'Factors identified'),
                          srp('Description/explanation of process', 12,
                              f'Description/Explanation of process · 12 x {SRPS}')),
                topic='0-8', atlas=RW),
      )),
    T('p2-3c', P2, '3C', '', 30, 18, L(18, 'Seismic Activity'),
      (L(18, 'Explain how the occurrence of seismic activity can be predicted and its effects reduced.'),),
      (S(13, 'Reference to prediction', None),),
      (fixed('Reference to prediction', 2, 'Reference to prediction of seismic activity · 2 marks'),
       fixed('Reference to reducing impacts', 2, 'Reference to reducing impacts of seismic activity · 2 marks'),
       srp('Explanation', 13, f'Explanation · 13 x {SRPS}')),
      '0-7', EV, ID + 'p2-q3c'),
]

PART_TWO += [
    T('p2-4a', P2, '4A', '', 20, 19, L(19, 'Map Skills'),
      (L(19, 'Draw an outline map of a Continental / Sub-Continental region (not in Europe) that you have',
         'Two named urban centres in the region.'),),
      (S(14, 'Map outline', None),),
      sketch('Map outline · 4 marks graded (4/2/0)', (0, 2, 4),
             ('4 features @ 4 marks each · Shown 2 marks graded (2/1/0)', 'Named 2 marks'), sums((0, 1, 2), (0, 2)), 4),
      '1-6', CONT, ID + 'p2-q4a',
      row_labels=(None, L(19, 'The course of a named river in the region'),
                  L(19, 'The outline of a named feature of relief (upland or lowland) in the region'),
                  L(19, 'Two named urban centres in the region.'), L(19, 'Two named urban centres in the region.'))),
    T('p2-4b', P2, '4B', '', 30, 19, L(19, 'Tertiary Economic Activity – European Region'),
      (L(19, 'Account for the development of one tertiary economic activity in a European region',
         'that you have studied.'),),
      (S(15, 'Examination · 15', '4C.'),), (srp('Examination', 15, f'Examination · 15 x {SRPS}'),),
      '1-5', EURO, ID + 'p2-q4b'),
    T('p2-4c', P2, '4C', '', 30, 19, L(19, 'Primary Economic Activity – Irish Region'),
      (L(19, 'Examine the physical factors that influence the development of one primary economic activity',
         'that you have studied.'),),
      (S(15, 'Physical factors identified', None),),
      (pair('Physical factors identified · 2 + 2 marks', 'Physical factors identified'),
       srp('Examination', 13, f'Examination · 13 x {SRPS}')),
      '1-4', IRL, ID + 'p2-q4c'),
]

Q5AS = (L(20, 'Examine the table above showing the number of trips into and out of Ireland', 'following questions.'),)
PART_TWO += romans('5A', P2, 20, L(20, 'Overseas Travel', nth=0), Q5AS, ID + 'p2-q5a', ('page',), [
    ('(i)', 2, L(20, '(i) In which year did trips into Ireland first exceed trips overseas by Irish residents?'),
     S(16, '(i) · 2011', '(ii) · Great Britain'), (fixed('Year', 2, '(i) · 2011 · 2 marks'),), '2-0', TG),
    ('(ii)', 6, L(20, '(ii) Which area of residence had the highest number of trips to Ireland',
                  'State two reasons for this.'),
     S(16, '(ii) · Great Britain', '(iii) · Increasing'),
     (fixed('Area of residence', 2, '(ii) · Great Britain · 2 marks'), pair('Two reasons stated 2 + 2 marks', 'Two reasons')),
     '1-4', IRL + TG),
    ('(iii)', 4, L(20, '(iii) What was the trend in the number of Irish residents’ trips overseas between 2013 and',
                   'State one reason for this trend.'),
     S(16, '(iii) · Increasing', '(iv) · Factor 1'),
     (fixed('Trend', 2, '(iii) · Increasing · 2 marks'), fixed('Reason', 2, 'Reason stated · 2 marks')), '2-0', TG),
    ('(iv)', 8, L(20, '(iv) Explain briefly two factors that impact on overseas travel.'),
     S(16, '(iv) · Factor 1', None),
     (pair('(iv) · Factor 1 explained · 2 + 2 marks', 'Factor 1'), pair('Factor 2 explained · 2 + 2 marks', 'Factor 2')),
     '1-4', IRL),
])
PART_TWO += [
    T('p2-5b', P2, '5B', '', 30, 20, L(20, 'Population Distribution – Continental / Sub-Continental Region'),
      (L(20, 'Account for the distribution of population throughout a Continental / Sub-Continental region',
         'that you have studied.'),),
      (S(17, 'Examination · 15', '5C.'),), (srp('Examination', 15, f'Examination · 15 x {SRPS}'),),
      '1-6', CONT + POP, ID + 'p2-q5b'),
    T('p2-5c', P2, '5C', '', 30, 20, L(20, 'The European Union'),
      (L(20, 'Explain each of the following challenges currently facing European Union member states:',
         'Economic challenges.'),),
      (S(17, 'Social challenge identified', None),),
      (fixed('Social challenge identified', 2, 'Social challenge identified · 2 marks'),
       fixed('Economic challenge identified', 2, 'Economic challenge identified · 2 marks'),
       split('Explanation of social and economic challenges (6/7 SRPs each)', 13,
             f'Explanation of social challenges · 6/7 x {SRPS}', f'Explanation of economic challenges · 6/7 x {SRPS}')),
      '1-3', EURO + EU_ECON, ID + 'p2-q5c'),
]

Q6AS = (L(21, 'Examine the chart above showing the age structure of the population of the European Union',
          'following questions.'),)
PART_TWO += romans('6A', P2, 21, L(21, 'European Union Population'), Q6AS, ID + 'p2-q6a', ('page',), [
    ('(i)', 4, L(21, '(i) Calculate X, the percentage of the EU (28) population aged between 20 and 64 years in 2015.'),
     S(18, '(i) · X · 60.3', '(ii) · 80'), (fixed('X', 4, '(i) · X · 60.3 (%) · 4 marks'),), '2-0', TG),
    ('(ii)', 4, L(21, '(ii) In which age group is the percentage of the population projected to almost double',
                  'State one reason for this projected increase.'),
     S(18, '(ii) · 80', '(iii) · 0-19'),
     (fixed('Age group', 2, '(ii) · 80 (years) or over · 2 marks'), fixed('Reason', 2, 'One reason stated · 2 marks')),
     '4-0', POP + EURO),
    ('(iii)', 4, L(21, '(iii) In which two age groups is the percentage of the population projected to decline',
                   '2002 to 2030?'),
     S(18, '(iii) · 0-19', '(iv) · Challenge'),
     (pair('(iii) · 0-19 (years) & 20 to 64 (years) · 2 + 2 marks', 'Two age groups'),), '2-0', TG),
    ('(iv)', 8, L(21, '(iv) Explain briefly two challenges presented by the projected decline', 'these two age groups.'),
     S(18, '(iv) · Challenge', None),
     (pair('(iv) · Challenge one explained · 2 + 2 marks', 'Challenge 1'),
      pair('Challenge two explained · 2 + 2 marks', 'Challenge 2')), '4-0', POP + EURO),
])
FACTORS_6B = ('Markets', 'Infrastructure', 'Government policy', 'Raw materials.')
PART_TWO += [
    T('p2-6b', P2, '6B', '', 30, 21, L(21, 'Secondary Economic Activity – Continental / Sub-Continental Region'),
      (L(21, 'Examine the development of secondary economic activity in a Continental / Sub-Continental',
         'Raw materials.'),),
      (S(19, 'Factor 1 examination', '6C.'),),
      (srp('Factor 1 examination', 8, f'Factor 1 examination · 8 x {SRPS}'),
       srp('Factor 2 examination', 7, f'Factor 2 examination · 7 x {SRPS}')),
      '1-6', CONT, ID + 'p2-q6b', absorbs=pool(ID + 'p2-q6b-', FACTORS_6B, 2)[1]),
    T('p2-6c', P2, '6C', '', 30, 21, L(21, 'Concept of a Region'),
      (L(21, 'Explain three differences between the characteristics of core regions', 'that you have studied.'),),
      (S(19, 'Core region named', None),),
      (fixed('Core region named', 2, 'Core region named · 2 marks'),
       fixed('Peripheral region named', 2, 'Peripheral region named · 2 marks'),
       srp('Three differences explained', 13, f'Three differences explained · 13 x {SRPS} (5/4/4 x {SRPS})')),
      '1-0', IRL + EURO, ID + 'p2-q6c'),
]

REASON_7B = ('Three reasons @ 10 marks each.', 'For each reason: · Reason stated · 2 marks', 'Map evidence · 2 marks',
             f'Explanation · 3 x {SRPS}')
PART_TWO += romans('7A', P2, 23, L(23, 'Energy Production'),
                   (L(23, 'Examine the data above showing the electricity generation mix', 'following questions.'),),
                   ID + 'p2-q7a', ('page',), [
    ('(i)', 16, L(23, '(i) Using graph paper, draw a suitable graph to illustrate this data.'),
     S(21, 'Bar Chart · Pie Chart', '(ii) · Explain briefly'), GRAPH, '2-0', TG),
    ('(ii)', 4, L(23, '(ii) Explain briefly one advantage of using energy sources other than fossil fuels.'),
     S(21, '(ii) · Explain briefly', None), (pair('Valid explanation · 2 + 2 marks', 'Advantage'),), '3-5', ENERGY),
])
PART_TWO += [
    T('p2-7b', P2, '7B', '', 30, 23, L(23, 'Location of Economic Activity'),
      (L(23, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper.'),
       L(23, 'Explain two reasons why a multinational company might choose to locate in the area', 'in this area.'),
       L(23, 'Use evidence from the Ordnance Survey map to support each reason.')),
      (S(22, 'Three reasons @ 10 marks each.', '7C.'),),
      (Criterion('Reason to locate 1', 10, evens(10), 'srp', REASON_7B),
       Criterion('Reason to locate 2', 10, evens(10), 'srp', REASON_7B),
       Criterion('Reason not to locate', 10, evens(10), 'srp', REASON_7B)),
      '3-2', MNC + MAP, ID + 'p2-q7b', ('map', 'legend')),
    T('p2-7c', P2, '7C', '', 30, 23, L(23, 'Colonialism'),
      (L(23, 'Examine the challenges resulting from colonialism faced by a developing economy', 'studied.'),),
      (S(22, 'Challenges identified', None),),
      (pair('Challenges identified · 2 + 2 marks', 'Challenges identified'),
       fixed('Developing economy named', 2, 'Developing economy named · 2 marks'),
       srp('Examination', 12, f'Examination · 12 x {SRPS}')),
      '3-1', DEV, ID + 'p2-q7c'),
    T('p2-8a', P2, '8A', '', 20, 24, L(24, 'Ordnance Survey Map'),
      (L(24, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper.',
         'An electricity transmission line.'),),
      (S(23, 'Sketch Outline', None),), OS_SKETCH, '2-6', MAP + ECON, ID + 'p2-q8a', ('map', 'legend'),
      row_labels=(None, L(24, 'The built up area of Macroom'), L(24, 'The entire route of the R584 road'),
                  L(24, 'The entire route of the N22 road'), L(24, 'An electricity transmission line.'))),
    T('p2-8b', P2, '8B', '', 30, 24, L(24, 'Multinational Company and Globalisation'),
      (L(24, 'Examine how globalisation impacts on world trade with reference to the operations of one',
         'that you have studied.'),),
      (S(24, 'Multinational company named', '8C.'),),
      (fixed('Multinational company named', 2, 'Multinational company named · 2 marks'),
       fixed('Impact of globalisation identified', 2, 'Impact of globalisation on world trade identified · 2 marks'),
       srp('Examination', 13, f'Examination · 13 x {SRPS}')),
      '3-2', MNC, ID + 'p2-q8b'),
    T('p2-8c', P2, '8C', '', 30, 24, L(24, 'Economic Activity – Environmental Impact'),
      (L(24, 'Discuss how the environmental impact of economic activity can be controlled',
         'approach to development.'),),
      (S(24, 'Examination · 15', None),), (srp('Examination', 15, f'Examination · 15 x {SRPS}'),),
      '3-4', ENV, ID + 'p2-q8c'),
]

Q9AS = (L(25, 'Examine the graph above showing information regarding international trade of services',
          'following questions.'),)
PART_TWO += romans('9A', P2, 25, L(25, 'International Trade', nth=0), Q9AS, ID + 'p2-q9a', ('page',), [
    ('(i)', 4, L(25, '(i) Which two countries had the highest value of services exported?'),
     S(25, '(i) · United States', '(ii) · ($)'),
     (pair('(i) · United States and United Kingdom 2 + 2 marks', 'Two countries'),), '2-0', TG),
    ('(ii)', 4, L(25, '(ii) Calculate the difference (in $US) between the value of services exported from China and',
                  'United States.'),
     S(25, '(ii) · ($)', '(iii) · Two countries'),
     (fixed('Difference', 4, ('(ii) · ($) 400 billion · 4 marks or', '($) 400 · 2 marks'), (0, 2, 4)),), '2-0', TG),
    ('(iii)', 4, L(25, '(iii) Name two countries with a trade surplus.'),
     S(25, '(iii) · Two countries', '(iv) · Valid'),
     (pair('(iii) · Two countries named · 2 + 2 marks', 'Two countries'),), '2-0', TG),
    ('(iv)', 4, L(25, '(iv) Explain briefly one disadvantage of a trade deficit.'),
     S(25, '(iv) · Valid', '(v) · Two services'), (pair('(iv) · Valid explanation · 2 + 2 marks', 'Disadvantage'),),
     '3-0', ECON),
    ('(v)', 4, L(25, '(v) Name two services exported from Ireland.'),
     S(25, '(v) · Two services', None), (pair('(v) · Two services named · 2 + 2 marks', 'Two services'),),
     '3-0', ECON),
])
ACTIVITIES_9B = ('Footloose industries', 'Financial services', 'Mass tourism.')
PART_TWO += [
    T('p2-9b', P2, '9B', '', 30, 25, L(25, 'Economic Activity in a Developed Economy'),
      (L(25, 'Examine the development of one of the following with reference to a developed economy',
         'Mass tourism.'),),
      (S(26, 'Developed economy named', '9C.'),),
      (fixed('Developed economy named', 2, 'Developed economy named · 2 marks'),
       srp('Examination', 14, f'Examination · 14 x {SRPS}')),
      '3-0', ECON, ID + 'p2-q9b-footloose-industries', routes=bullet_routes('p2-q9b-', ACTIVITIES_9B)),
    T('p2-9c', P2, '9C', '', 30, 25, L(25, 'European Union Policy'),
      (L(25, 'Examine the impact of European Union policy on regional development in Ireland.'),),
      (S(26, 'Impact on regional development', None),),
      (fixed('Impact on regional development identified', 2, 'Impact on regional development identified 2 marks'),
       srp('Examination', 14, f'Examination · 14 x {SRPS}')),
      '3-3', EU_ECON + IRL, ID + 'p2-q9c'),
]

ISSUES_10C = ('Heritage issues', 'Planning issues', 'Environmental issues.')
PART_TWO += [
    T('p2-10a', P2, '10A', '', 20, 26, L(26, 'Aerial Photograph'),
      (L(26, 'Draw a sketch map of the aerial photograph, half the length and half the breadth.',
         'in the left middleground.'),),
      (S(27, 'Sketch Outline', None),),
      sketch('Sketch Outline · 4 marks (4/0)', (0, 4),
             ('4 features @ 4 marks each · Shown 3 marks (graded 3/1/0)', 'Named 1 mark'), sums((0, 1, 3), (0, 1)), 4),
      '2-8', AER + URB, ID + 'p2-q10a', ('aerial',),
      row_labels=(None, L(26, 'The river'), L(26, 'A large sports field'),
                  L(26, 'The triangular street pattern in the centre middleground'),
                  L(26, 'An ecclesiastical building in the left middleground.'))),
    T('p2-10b', P2, '10B', '', 30, 26, L(26, 'Dynamics of Population'),
      (L(26, 'Examine how changing fertility and mortality rates impact on population structure',
         'that you have studied.'),),
      (S(28, 'Impact of changing fertility', '10C.'),),
      (fixed('Impact of changing fertility rates identified', 2, 'Impact of changing fertility rates identified · 2 marks'),
       fixed('Impact of changing mortality rates identified', 2, 'Impact of changing mortality rates identified · 2 marks'),
       fixed('Example', 2, 'Example of where impacts occur · 2 marks'), srp('Examination', 12, f'Examination · 12 x {SRPS}')),
      '4-0', POP, ID + 'p2-q10b'),
    T('p2-10c', P2, '10C', '', 30, 26, L(26, 'Urban Issues'),
      (L(26, 'Discuss any two of the following issues that may arise from the growth of urban settlements:',
         'Environmental issues.'),),
      (S(28, 'Discussion of Issue 1', None),),
      (split('Discussion of the two issues (7/8 SRPs each)', 15,
             f'Discussion of Issue 1 · 7/8 x {SRPS}', f'Discussion of Issue 2 · 7/8 x {SRPS}'),),
      '4-5', URB, ID + 'p2-q10c', absorbs=pool(ID + 'p2-q10c-', ISSUES_10C, 2)[1]),
]

Q11AS = (L(27, 'Examine the graph of Irish migration above and answer each of the following questions.'),)
PART_TWO += romans('11A', P2, 27, L(27, 'Irish Migration', nth=0), Q11AS, ID + 'p2-q11a', ('page',), [
    ('(i)', 2, L(27, '(i) In which year was the number of people immigrating equal to the number of people', 'emigrating?'),
     S(29, '(i) · 2009', '(ii) · 2007'), (fixed('Year', 2, '(i) · 2009 · 2 marks'),), '2-0', TG),
    ('(ii)', 2, L(27, '(ii) When did immigration exceed emigration by more than 100,000?'),
     S(29, '(ii) · 2007', '(iii) · Six'), (fixed('Year', 2, '(ii) · 2007 · 2 marks'),), '2-0', TG),
    ('(iii)', 4, L(27, '(iii) In how many years was emigration greater than immigration?'),
     S(29, '(iii) · Six', '(iv) · Valid'), (fixed('Number of years', 4, '(iii) · Six · 4 marks'),), '2-0', TG),
    ('(iv)', 4, L(27, '(iv) Explain briefly one reason why immigration declined between 2007 and 2010.'),
     S(29, '(iv) · Valid', '(v) · Valid'), (pair('(iv) · Valid explanation · 2 + 2 marks', 'Reason'),), '4-2', POP),
    ('(v)', 4, L(27, '(v) Explain briefly the term net migration.'),
     S(29, '(v) · Valid', '(vi) · Two barriers'), (pair('(v) · Valid explanation · 2 + 2 marks', 'Explanation'),),
     '4-2', POP),
    ('(vi)', 4, L(27, '(vi) Name two barriers to migration.'),
     S(29, '(vi) · Two barriers', None), (pair('(vi) · Two barriers named 2 + 2 marks', 'Two barriers'),), '4-2', POP),
])
FACTORS_11C = ('Development of resources', 'Income levels', 'Society and culture', 'Technology.')
PART_TWO += [
    T('p2-11b', P2, '11B', '', 30, 27, L(27, 'Urban Land Use'),
      (L(27, 'Describe and explain the land-use zones in any city that you have studied.'),),
      (S(30, 'Land-use zones identified', '11C.'),),
      (pair('Land-use zones identified · 2 + 2 marks', 'Land-use zones identified'),
       fixed('City named', 2, 'City named · 2 marks'),
       srp('Description/explanation', 12, f'Description/explanation · 12 x {SRPS}')),
      '4-4', LAND + URB, ID + 'p2-q11b'),
    T('p2-11c', P2, '11C', '', 30, 27, L(27, 'Dynamics of Population', nth=0),
      (L(27, 'Examine the impact of any one of the following factors on levels of population growth', 'Technology.'),),
      (S(30, 'Impact on population growth identified', None),),
      (fixed('Impact on population growth identified', 2, 'Impact on population growth identified · 2 marks'),
       fixed('Example of location', 2, 'Example of location · 2 marks'),
       srp('Examination', 13, f'Examination · 13 x {SRPS}')),
      '4-1', POP, ID + 'p2-q11c-development-of-resources', routes=bullet_routes('p2-q11c-', FACTORS_11C)),
]

Q12AS = (L(28, 'Examine the data above showing rural population as a percentage of the total population',
           'in 1960 and 2015.'),)
PART_TWO += romans('12A', P2, 28, L(28, 'Population Dynamics'), Q12AS, ID + 'p2-q12a', ('page',), [
    ('(i)', 16, L(28, '(i) Using graph paper, draw a suitable graph to illustrate this data.'),
     S(31, 'Bar Chart · Pie Chart', '(ii) · Explain briefly'), GRAPH, '2-0', TG),
    ('(ii)', 4, L(28, '(ii) Explain briefly one reason for the trend in rural population indicated in the table above.'),
     S(31, '(ii) · Explain briefly', None), (pair('Valid explanation · 2 + 2 marks', 'Reason'),), '4-3', URB),
])
EVIDENCE = 'the aerial photograph OR from the 1:50 000 Ordnance Survey map and legend'
REASON_12C = ('Three reasons @ 10 marks each', 'For each reason:', 'Reason stated · 2 marks',
              'Aerial photograph OR OS map evidence · 2 marks', f'Examination · 3 x {SRPS}')
PART_TWO += [
    T('p2-12b', P2, '12B', '', 30, 28, L(28, 'Migration'),
      (L(28, 'Examine how ethnic and religious issues can arise as a result of migration.'),),
      (S(32, 'Ethnic issue identified', '12C.'),),
      (fixed('Ethnic issue identified', 2, 'Ethnic issue identified · 2 marks'),
       fixed('Religious issue identified', 2, 'Religious issue identified · 2 marks'),
       srp('Examination', 13, 'Examination · 13 x SRPs')),
      '4-2', POP, ID + 'p2-q12b'),
    T('p2-12c', P2, '12C', '', 30, 28, L(28, 'Urban settlement'),
      (L(28, 'Answer the following question using evidence from the aerial photograph OR', 'both in your answer.'),
       L(28, 'Explain three reasons why the town of Macroom developed at its present location.')),
      (S(32, 'Three reasons @ 10 marks each', None),),
      tuple(Criterion(f'Reason {n}', 10, evens(10), 'srp', REASON_12C) for n in (1, 2, 3)),
      '4-3', URB + AER + MAP, ID + 'p2-q12c-aerial-photograph', ('aerial', 'map', 'legend'),
      routes=(Route('aerial-photograph', 'aerial photograph', ID + 'p2-q12c-aerial-photograph', False,
                    ((EVIDENCE, 'the aerial photograph'),), sources=('aerial',), atlas=URB + AER),
              Route('ordnance-survey-map', 'Ordnance Survey map', ID + 'p2-q12c-ordnance-survey-map', False,
                    ((EVIDENCE, 'the 1:50 000 Ordnance Survey map and legend'),), sources=('map', 'legend'),
                    atlas=URB + MAP))),
]

# ------------------------------------------------------------------ Options --
OC = (S(34, '*Overall Coherence (20 marks)', None, table=True),)
COHERENCE = Criterion('Overall coherence', 20, (0, 6, 10, 14, 17, 20), 'exact',
                      ('Overall Coherence · 20 marks graded*', '*Overall Coherence (20 marks)', 'Excellent · 20',
                       'Very Good · 17', 'Good · 14', 'Fair · 10', 'Weak · 6', 'Poor · 0'))
OPTION_CRITERIA = (
    Criterion('Aspects (3 @ 20 marks or 4 @ 15 marks)', 60, upto(60), 'srp',
              ('Number of aspects', '?For each aspect:', 'Identifying aspect', '8 x SRP')),
    COHERENCE)
# Options 13, 16 and 18 print three items and only the "3 @ 20 marks" outline.
OPTION_CRITERIA_3 = (
    Criterion('Aspects (3 @ 20 marks)', 60, evens(60), 'srp',
              ('Number of aspects · 3 @ 20 marks each', 'For each aspect:', 'Identifying aspect · 4 marks',
               'Discussion · 8 x SRP')),
    COHERENCE)


def option(q, page, theme, note_nth, prompt, scheme_page, topic, atlas, after=None, end=None, absorbs=(),
           criteria=OPTION_CRITERIA):
    return T(f'p2-{q}', P2, q, '', 80, page, theme, prompt if isinstance(prompt, tuple) else (prompt,),
             (S(scheme_page, 'Number of aspects', end, None, after), *OC), criteria,
             topic, (atlas,), ID + f'p2-q{q}',
             stem=(L(page, 'Note: It is better to discuss three or four aspects', 'large number of points.',
                     nth=note_nth),),
             absorbs=absorbs)


GI, GE = H + 'option-global-interdependence', H + 'option-geoecology'
CI, AO = H + 'option-culture-identity', H + 'option-atmosphere-ocean'
EMPOWERING = ('National debt', 'Aid programmes', 'Land ownership patterns', 'Differing gender roles in society.')
SOIL = ('Mineral matter', 'Air', 'Water', 'Organic matter.')
OPTIONS = [
    option('13', 30, L(30, 'Global Interdependence'), 0,
           L(30, 'Empowering people is a way of linking economic growth with human development.',
             'Differing gender roles in society.'), 35, '5-2', GI, after='13.', end='14.',
           absorbs=pool(ID + 'p2-q13-', EMPOWERING, 3)[1], criteria=OPTION_CRITERIA_3),
    option('14', 30, L(30, 'Global Interdependence'), 0,
           L(30, 'Discuss the causes and impacts of one global environmental issue that you have studied.'),
           35, '5-1', GI, after='14.'),
    option('15', 30, L(30, 'Global Interdependence'), 0,
           L(30, 'Examine the contribution that fair trade can make to sustainable development.'), 36, '5-3', GI),
    option('16', 30, L(30, 'Geoecology'), 1,
           L(30, 'Discuss how soil development is influenced by any three of the following factors:', 'Organic matter.'),
           37, '6-0', GE, after='16.', end='17.', absorbs=pool(ID + 'p2-q16-', SOIL, 3)[1],
           criteria=OPTION_CRITERIA_3),
    option('17', 30, L(30, 'Geoecology'), 1,
           L(30, 'Discuss how human activity can have both positive and negative impacts on soil characteristics.'),
           37, '6-1', GE, after='17.'),
    option('18', 30, L(30, 'Geoecology'), 1,
           L(30, 'Examine how each of the following activities impact on biomes:', 'Industrial development.'),
           38, '6-3', GE, criteria=OPTION_CRITERIA_3),
    option('19', 31, L(31, 'Culture and Identity'), 0,
           L(31, 'Conflicts can occur between political structures and cultural groups.', 'Discuss.'),
           39, '7-1', CI, after='19.', end='20.'),
    option('20', 31, L(31, 'Culture and Identity'), 0,
           L(31, 'Examine the importance of language as a cultural indicator.'), 39, '7-0', CI, after='20.'),
    option('21', 31, L(31, 'Culture and Identity'), 0,
           L(31, 'Examine how people express their culture and identity in everyday life.'), 40, '7-2', CI),
    option('22', 31, L(31, 'The Atmosphere – Ocean Environment'), 1,
           L(31, 'Examine how exchanges of water between oceans and atmosphere', 'climate regimes.'),
           41, '8-2', AO, after='22.', end='23.'),
    option('23', 31, L(31, 'The Atmosphere – Ocean Environment'), 1,
           L(31, 'Give an account of how atmosphere-ocean phenomena', 'importance of such measurements.'),
           41, '8-0', AO, after='23.'),
    option('24', 31, L(31, 'The Atmosphere – Ocean Environment'), 1,
           L(31, 'Describe and account for the specific characteristics of one global climate type you have studied.'),
           42, '8-4', AO),
]

TASKS = [*PART_ONE, *PART_TWO, *OPTIONS]

ID_CORRECTION_REASON = 'No 2017 Higher card shipped before this review; every card is new.'

# No 2017 Higher card was live on origin/main before this review.
LEGACY_IDS: list[str] = []
