"""Independent review ledger: Leaving Certificate Geography 2015 Higher Level.

Sources (English editions, harvested Paper Trail corpus; sizes and SHA-256
pinned in EXPECTED_SOURCES and the generated audit): the examination paper
LC005ALP000EV (32 pages; one booklet printed Part One, answered in it, and
Part Two), marking scheme LC005ALP000EV (48 pages), and the common Kenmare
companions as Paper Trail files them — the 1:50 000 map LC005CLP003EV, its
legend LC005CLPC00EV and the aerial photograph LC005CLP004EV (one-page PDFs;
the legend and the photograph are each stored as stacked image strips that
render as one page). Part One is 80 marks (any ten of twelve @ 8), Part Two
320 (four questions @ 80).

Visual sweep (every page rendered and read on 2026-10-14):
  Paper p1 cover and examiner's grid; p2-p12 Part One Questions 1-12 (p8
  holds Q7 and Q8; Q9 prints a line on the map and its elevation profile,
  Q10 an OS map extract); p13 Part Two instructions; p14 Section 1 divider;
  p15-p20 Q1-Q6 (p15 and p18 open with their dividers); p21 Section 2
  divider; p22-p28 Electives Q7-Q12 (p22 and p25 open with their elective
  dividers; p27 holds 12A and 12B, p28 12C); p29 Section 3 divider and
  option note; p30-p31 Options Q13-Q24; p32 printed "Blank Page".
  Scheme p1 cover; p2-p3 notes; p4 Part One table (a centred tariff
  heading, then two columns: Q1-Q6, Q7-Q12; the answer lines print no
  marks); p5 Part Two instructions and Section 1 divider; p6-p12 Q1-Q3;
  p13-p18 Q4-Q6; p19 Section 2 divider; p20-p25 Q7-Q9; p26-p31 Q10-Q12;
  p32 Section 3 divider; p33 option outline and Overall Coherence
  descriptors; p34-p41 Q13-Q24; p42-p44 Geographical Investigation
  (coursework) and its presentation marks; p45 investigation topics; p46
  Irish-language bonus marks; p47 printed "Blank Page"; p48 back cover.
  Companions: Kenmare map extract (the Kenmare River, Letter South, the
  Béara Way); OS legend sheet; oblique aerial photograph of Kenmare.

Part One prices by question in the heading ("Q.1, 2, 6: 8 @ 1m each",
"Q.3, 4, 5, 7, 8, 9, 12: 4 @ 2m each", "Q.10: 6 @ 1 mark (ii) 1m + 1m",
"Q.11: 3 @ 2m each (iv) 1m + 1m"), so every Part One card carries its
heading line with the answer lines it prices. Matching tables, in the
printed row order: Q1 Sill C Plutonic, Pyroclastic sediment A Volcanic,
Dyke D Plutonic, Lava flow B Volcanic; Q2 Blow hole C Erosion, Sea stack
A Erosion, Bay-head beach D Deposition, Geo B Erosion; Q6 Rotational slump
D, Soil creep A, Landslide B, Mudflow C; Q10 Trellis drainage F, Even
slope B, Dendritic drainage C, Concave slope A, Drumlins D, Cut-off
meander E; Q12 Delta D, Open-cast mining B, Dust storm A, Forest fire C.
Q1 and Q2 answer (i) and (ii) in one table and are one card of two-mark
rows. Q3 and Q4 print four separately priced true/false romans.

Printed choices: 1B (i) or (ii), with (i)'s one fluvial, coastal or glacial
landform a route each; 3B (folding or faulting) and 3C (one of four
activities) are one route per printed option; 4C's transport or tourism
is two routes. 5C (any two of five human processes, printed as a table)
and 10B (any two of three problems) are pools, one card each.
"""

from geography_review import (
    Criterion, Lift, Route, SchemeSlice, Task, pool, evens, fixed, slug, srp, sums, upto,
)

YEAR = 2015
LEVEL = 'higher'
PAPER_PAGES = {1: 32, 2: 32}
SCHEME_PAGES = 48
QUESTION_TARIFFS = {1: {str(n): 8 for n in range(1, 13)},
                    2: {**{f'{n}{x}': (20 if x == 'A' else 30)
                           for n in range(1, 13) for x in 'ABC'},
                        **{str(n): 80 for n in range(13, 25)}}}

EXPECTED_SOURCES = {
    'paper1': ('LC005ALP000EV.pdf', 3601749),
    'paper2': ('LC005ALP000EV.pdf', 3601749),
    'scheme': ('LC005ALP000EV.pdf', 893788),
    'map': ('LC005CLP003EV.pdf', 6859305),
    'legend': ('LC005CLPC00EV.pdf', 2156988),
    'aerial': ('LC005CLP004EV.pdf', 2647375),
}

_PAPER = {1: 'cover and examiner grid', **{p: 'question' for p in range(2, 13)},
          13: 'Part Two instructions', 14: 'section divider', **{p: 'question' for p in range(15, 21)},
          21: 'section divider', **{p: 'question' for p in range(22, 29)}, 29: 'section divider and option note',
          30: 'question', 31: 'question', 32: 'blank page'}
PAGE_REVIEW = {
    # One booklet printed both parts.
    'paper1': _PAPER, 'paper2': _PAPER,
    'scheme': {1: 'cover', 2: 'notes', 3: 'notes', 4: 'Part One table', 5: 'Part Two instructions',
               **{p: 'Part Two allocation' for p in range(6, 19)}, 19: 'section divider',
               **{p: 'Part Two allocation' for p in range(20, 32)}, 32: 'section divider',
               33: 'option outline and coherence descriptors',
               **{p: 'option allocation' for p in range(34, 42)},
               **{p: 'geographical investigation (coursework)' for p in range(42, 45)},
               45: 'investigation topics', 46: 'Irish-language bonus marks', 47: 'blank', 48: 'back cover'},
}

EXPECTED_SELECTION_SCAN = [
    [1, 2, 'attempt any ten'], [1, 7, 'any two'], [1, 13, 'attempt four'], [1, 14, 'attempt two'],
    [1, 15, 'attempt one'], [1, 15, 'any two'], [1, 15, 'answer (i) or (ii)'],
    [1, 17, 'any two'], [1, 17, 'one of the following'], [1, 17, 'one of the following'],
    [1, 18, 'attempt one'],
    [1, 19, 'any two'],
    [1, 21, 'attempt one'],
    [1, 25, 'any two'],
    [1, 29, 'attempt one'],
]
SELECTION_REVIEW = [
    {'scan': [[1, 2, 'attempt any ten'], [1, 13, 'attempt four'], [1, 14, 'attempt two'], [1, 15, 'attempt one'],
              [1, 18, 'attempt one'], [1, 21, 'attempt one'], [1, 29, 'attempt one']],
     'kind': 'exam-attempt-rule',
     'reason': 'Part One any ten of twelve and Part Two four questions (one of Q1-3, one of Q4-6, one elective, one option) are attempt rules; every question is carded.'},
    {'scan': [[1, 15, 'answer (i) or (ii)']], 'kind': 'closed-route',
     'reason': '1B: (i) or (ii); (i) offers one fluvial, coastal or glacial landform -> 4 routes. 4C "transport or tourism" -> 2 routes (no directive word the scan reads; the route text is anchored on the paper).'},
    {'scan': [[1, 17, 'one of the following'], [1, 17, 'one of the following']], 'kind': 'closed-choose-one',
     'reason': '3B folding or faulting -> 2 routes; 3C one of four printed rock-cycle activities -> 4 routes.'},
    {'scan': [[1, 19, 'any two'], [1, 25, 'any two']], 'kind': 'choose-n-one-card',
     'reason': '5C any two of the five human processes printed in a table and 10B any two of three printed problems -> one card each with every printed item (choice is not a route).'},
    {'scan': [[1, 7, 'any two'], [1, 15, 'any two'], [1, 17, 'any two']], 'kind': 'open-response',
     'reason': 'No printed pool: Part One Q6(ii) any two factors, 1A(ii) any two processes of chemical weathering, 3A(iii) any two fluvioglacial landforms. Compulsory lists stay whole: 2A, 4A, 8A, 10A each item; option 13 each of three items.'},
]

P1, P2 = 1, 2
LEFT = (0.0, 0.30, 0.47, 1.0)
RIGHT = (0.47, 0.30, 1.0, 1.0)
ID = 'geography-2015-hl-'
H = 'geography-higher-'
SRPS = 'SRPs'
T1 = 'Q.1, 2, 6: 8 @ 1m each'
T2 = 'Q.3, 4, 5, 7, 8, 9, 12: 4 @ 2m each'
T10 = 'Q.10: 6 @ 1 mark (ii) 1m + 1m'
T11 = 'Q.11: 3 @ 2m each (iv) 1m + 1m'


def L(page, start, end=None, nth=None):
    return Lift(page, start, end, None, nth)


def S(page, start, end=None, clip=None, after=None, table=False):
    return SchemeSlice(page, start, end, clip, after, table)


# The Part One heading line that prices each question.
H1 = S(4, 'Q.1, 2, 6:', 'Q.3, 4, 5')
H2 = S(4, 'Q.3, 4, 5, 7', 'Q.10:')
H10 = S(4, 'Q.10:', 'Q.11:')
H11 = S(4, 'Q.11:', 'No grading')


def T(key, part, q, sub, marks, page, title, prompt, scheme, criteria, topic, atlas, card_id,
      sources=(), stem=(), routes=(), row_labels=(), absorbs=()):
    return Task(key, part, q, sub, marks, page, title, prompt, scheme, criteria, topic, atlas,
                sources, card_id, False, stem=stem, routes=routes, row_labels=row_labels,
                absorbs=absorbs)


def priced_rows(tariff, lines, marks, permitted=None):
    """Rows of a Part One table; the first carries the heading that prices them."""
    return tuple(fixed(f'Row {i}', marks, (tariff, line) if i == 1 else line, permitted)
                 for i, line in enumerate(lines, 1))


def answer(label, tariff, line, marks=2, permitted=None):
    lines = (tariff, *line) if isinstance(line, tuple) else (tariff, line)
    return (fixed(label, marks, lines, permitted),)


def pair(line, label):
    return fixed(label, 4, line, (0, 2, 4))


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
ENV = (H + 'economic-environmental-impact',)

# ---------------------------------------------------------------- Part One --
PART_ONE = [
    T('p1-1', P1, '1', '', 8, 2, L(2, 'Structure of a Volcano'),
      (L(2, '(i) Match each of the letters A, B, C and D with the feature that best matches it in the',
         'table below.'),
       L(2, '(ii) Indicate whether plutonic processes or volcanic processes are most associated',
         'in the table below.')),
      (H1, S(4, 'Q.1 C', 'Q.2', LEFT)),
      priced_rows(T1, ['Q.1 C Plutonic', 'A Volcanic', 'D Plutonic', 'B Volcanic'], 2, (0, 1, 2)),
      '0-7', EV + RW, ID + 'p1-q1', ('page',),
      (L(2, 'Examine the diagram above and answer each of the following questions.'),),
      row_labels=(L(2, 'Sill'), L(2, 'Pyroclastic sediment'), L(2, 'Dyke'), L(2, 'Lava flow'))),
    T('p1-2', P1, '2', '', 8, 3, L(3, 'Aerial Photograph'),
      (L(3, '(i) Match each of the letters A, B, C and D with the landform that best matches it in',
         'table below.'),
       L(3, '(ii) Indicate whether processes of coastal erosion or coastal deposition are most',
         'in the table below.')),
      (H1, S(4, 'Q.2 C', 'Q.3', LEFT)),
      priced_rows(T1, ['Q.2 C Erosion', 'A Erosion', 'D Deposition', 'B Erosion'], 2, (0, 1, 2)),
      '0-10', SEA, ID + 'p1-q2', ('page',),
      (L(3, 'Examine the aerial photograph above and answer each of the following questions.'),),
      row_labels=(L(3, 'Blow hole'), L(3, 'Sea stack'), L(3, 'Bay-head beach'), L(3, 'Geo'))),
]
Q3S = (L(4, 'Examine the map of Europe above showing the member states of the European Union and',
         'in each case.'),)
PART_ONE += romans('3', P1, 4, L(4, 'European Union', nth=0), Q3S, ID + 'p1-q3', ('page',), [
    ('(i)', 2, L(4, '(i) Only six countries joined the European Union in 2004.'),
     (H2, S(4, 'Q.3 (i)', '(ii) True', LEFT)), answer('True or false', T2, 'Q.3 (i) False'), '3-3', EU_ECON + EURO),
    ('(ii)', 2, L(4, '(ii) Belgium joined the European Union in the same year as the Netherlands.'),
     (H2, S(4, '(ii) True', '(iii) False', LEFT, 'Q.3 (i)')), answer('True or false', T2, '(ii) True'),
     '3-3', EU_ECON + EURO),
    ('(iii)', 2, L(4, '(iii) Denmark joined the European Union in 1971.'),
     (H2, S(4, '(iii) False', '(iv) False', LEFT, 'Q.3 (i)')), answer('True or false', T2, '(iii) False'),
     '3-3', EU_ECON + EURO),
    ('(iv)', 2, L(4, '(iv) Slovakia joined the European Union in 2013.'),
     (H2, S(4, '(iv) False', 'Q.4', LEFT, 'Q.3 (i)')), answer('True or false', T2, '(iv) False'),
     '3-3', EU_ECON + EURO),
])
Q4S = (L(5, 'Examine the weather chart above and indicate whether each of the following statements',
         'in each case.'),)
PART_ONE += romans('4', P1, 5, L(5, 'Weather Chart'), Q4S, ID + 'p1-q4', ('page',), [
    ('(i)', 2, L(5, '(i) The pressure over the south west coast of Ireland is 1022 hPa.'),
     (H2, S(4, 'Q.4 (i)', '(ii) True', LEFT)), answer('True or false', T2, 'Q.4 (i) False'), '2-7', WX),
    ('(ii)', 2, L(5, '(ii) There is a warm front located on the south coast of England.'),
     (H2, S(4, '(ii) True', '(iii) False', LEFT, 'Q.4 (i)')), answer('True or false', T2, '(ii) True'), '2-7', WX),
    ('(iii)', 2, L(5, '(iii) Ireland is under the influence of a north-easterly airflow.'),
     (H2, S(4, '(iii) False', '(iv) False', LEFT, 'Q.4 (i)')), answer('True or false', T2, '(iii) False'),
     '2-7', WX),
    ('(iv)', 2, L(5, '(iv) Winds over Ireland are strong to gale force.'),
     (H2, S(4, '(iv) False', 'Q.5', LEFT, 'Q.4 (i)')), answer('True or false', T2, '(iv) False'), '2-7', WX),
])
PART_ONE += romans('5', P1, 6, L(6, 'Plate Tectonics'),
                   (L(6, 'Examine the diagram above and answer each of the following questions.'),),
                   ID + 'p1-q5', ('page',), [
    ('(i)', 2, L(6, '(i) Name the type of plate boundary illustrated in the diagram above.'),
     (H2, S(4, 'Q.5 (i)', '(ii) Ocean', LEFT)), answer('Plate boundary', T2, 'Q.5 (i) Divergent/Constructive'),
     '0-0', PS),
    ('(ii)', 2, L(6, '(ii) Name the feature at A.'),
     (H2, S(4, '(ii) Ocean', '(iii) Any valid extrusive', LEFT)),
     answer('Feature', T2, '(ii) Ocean Ridge, Mid-Ocean ridge'), '0-0', PS),
    ('(iii)', 2, L(6, '(iii) Name an igneous rock formed at B.'),
     (H2, S(4, '(iii) Any valid extrusive', '(iv) Asthenosphere', LEFT)),
     answer('Igneous rock', T2, ('(iii) Any valid extrusive igneous rock', 'e.g. Basalt')), '0-1', RW + PS),
    ('(iv)', 2, L(6, '(iv) Name the part of the upper mantle at C.'),
     (H2, S(4, '(iv) Asthenosphere', 'Q.6', LEFT)), answer('Part of the upper mantle', T2, '(iv) Asthenosphere'),
     '0-0', PS),
])
PART_ONE += romans('6', P1, 7, L(7, 'Mass Movement'),
                   (L(7, 'Examine the photographs above and answer each of the following questions.'),),
                   ID + 'p1-q6', ('page',), [
    ('(i)', 4, L(7, '(i) Match each of the letters A, B, C and D with the process that best matches it in the',
                 'table below.'),
     (H1, S(4, 'Q.6 (i)', '(ii) Gravity', LEFT)),
     priced_rows(T1, ['Q.6 (i) D Rotational slump', 'A Soil creep', 'B Landslide', 'C Mudflow'], 1), '0-8', RW,
     (L(7, 'Rotational slump'), L(7, 'Soil creep'), L(7, 'Landslide'), L(7, 'Mudflow'))),
    ('(ii)', 2, L(7, '(ii) Name any two factors that influence the operation of mass movement processes.'),
     (H1, S(4, '(ii) Gravity', '(iii) Any two', LEFT)),
     answer('Two factors', T1, ('(ii) Gravity, slope, vegetation,', 'precipitation, water content etc.'), 2,
            (0, 1, 2)), '0-8', RW),
    ('(iii)', 2, L(7, '(iii) Name one example of a very rapid mass movement process and name one',
                   'very slow mass movement process.'),
     (H1, S(4, '(iii) Any two', None, LEFT)), answer('Two examples', T1, '(iii) Any two valid examples', 2, (0, 1, 2)),
     '0-8', RW),
])
PART_ONE += romans('7', P1, 8, L(8, 'Ordnance Survey Map', nth=0),
                   (L(8, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper and answer',
                      'following questions.'),),
                   ID + 'p1-q7', ('map', 'legend'), [
    ('(i)', 2, L(8, '(i) Measure the straight line distance, in kilometres, from the 18 hole golf course',
                 'V 862 773.'),
     (H2, S(4, 'Q.7', '(ii) 6 - 8', RIGHT)), answer('Distance', T2, 'Q.7 · (i) 6.1 – 6.4 km'), '2-6', MAP),
    ('(ii)', 2, L(8, '(ii) Calculate the approximate area of the Kenmare River west of Easting 88',
                  'shown on the map.'),
     (H2, S(4, '(ii) 6 - 8', '(iii) Any valid statement', RIGHT)), answer('Area', T2, '(ii) 6 - 8 km2'), '2-6', MAP),
    ('(iii)', 2, L(8, '(iii) State one piece of evidence to show there may be permeable rock present at V 92 77.'),
     (H2, S(4, '(iii) Any valid statement', '(iv) Any valid species', RIGHT)),
     answer('Evidence', T2, '(iii) Any valid statement'), '2-6', MAP + KARST),
    ('(iv)', 2, L(8, '(iv) Name one species of tree that may be found in the natural woodland at V 87 74.'),
     (H2, S(4, '(iv) Any valid species', 'Q.8', RIGHT)), answer('Species', T2, '(iv) Any valid species named'),
     '2-6', MAP),
])
PART_ONE += romans('8', P1, 8, L(8, 'Aerial Photograph and Ordnance Survey Map'),
                   (L(8, 'Examine the aerial photograph and the 1:50 000 Ordnance Survey map and legend',
                      'following questions.'),),
                   ID + 'p1-q8', ('aerial', 'map', 'legend'), [
    ('(i)', 2, L(8, '(i) Give a six-figure grid reference for the large church located in the centre',
                 'aerial photograph.'),
     (H2, S(4, 'Q.8', '(ii) South', RIGHT)), answer('Grid reference', T2, 'Q.8 · (i) V 909-911 711-713'),
     '2-8', AER + MAP),
    ('(ii)', 2, L(8, '(ii) In what direction was the camera pointed when the aerial photograph was taken?'),
     (H2, S(4, '(ii) South', '(iii) N71', RIGHT)), answer('Direction', T2, '(ii) South or South South West'),
     '2-8', AER + MAP),
    ('(iii)', 2, L(8, '(iii) Name the main road that runs through the aerial photograph from the centre',
                   'centre foreground.'),
     (H2, S(4, '(iii) N71', '(iv) Any valid statement', RIGHT)), answer('Road', T2, '(iii) N71'), '2-8', AER + MAP),
    ('(iv)', 2, L(8, '(iv) State one piece of evidence, from the Ordnance Survey map or the aerial',
                  'plantation town.'),
     (H2, S(4, '(iv) Any valid statement', 'Q.9', RIGHT)), answer('Evidence', T2, '(iv) Any valid statement'),
     '4-3', URB + AER + MAP),
])
PART_ONE += romans('9', P1, 9, L(9, 'Map Skills'),
                   (L(9, 'Figure 1 shows a line X-Y along Northing 76', 'line X-Y.'),
                    L(9, 'Using the 1:50 000 Ordnance Survey map and legend accompanying this paper and the',
                      'following questions.')),
                   ID + 'p1-q9', ('page', 'map', 'legend'), [
    ('(i)', 2, L(9, '(i) Name the road at A.'),
     (H2, S(4, 'Q.9', '(ii) The Kerry', RIGHT)), answer('Road', T2, 'Q.9 · (i) N71'), '2-6', MAP),
    ('(ii)', 2, L(9, '(ii) Name the waymarked walk at B.'),
     (H2, S(4, '(ii) The Kerry', '(iii) Cummeenboy', RIGHT)),
     answer('Waymarked walk', T2, '(ii) The Kerry Way (Sli Uibh Rathacht)'), '2-6', MAP),
    ('(iii)', 2, L(9, '(iii) Name the stream/river at C.'),
     (H2, S(4, '(iii) Cummeenboy', '(iv) 395', RIGHT)), answer('Stream/river', T2, '(iii) Cummeenboy'), '2-6', MAP),
    ('(iv)', 2, L(9, '(iv) Calculate the difference in the altitude between the road at A', 'Ordnance Survey map.'),
     (H2, S(4, '(iv) 395', 'Q.10', RIGHT)), answer('Difference in altitude', T2, '(iv) 395 - 405m'), '2-6', MAP),
])
PART_ONE += romans('10', P1, 10, L(10, 'Landform and Pattern Recognition'),
                   (L(10, 'Examine the Ordnance Survey map extract above and answer each of the following',
                      'questions.'),),
                   ID + 'p1-q10', ('page',), [
    ('(i)', 6, L(10, '(i) Match each of the letters A, B, C, D, E and F with the landform or pattern that',
                 'table below.'),
     (H10, S(4, 'Q.10', '(ii) Any valid explanation', RIGHT)),
     priced_rows(T10, ['Q.10 · (i) F Trellis', 'B Even slope', 'C Dendritic drainage', 'A Concave slope',
                       'D Drumlin', 'E Cut-off meander'], 1),
     '2-6', MAP + RIVERS + GLAC,
     (L(10, 'Trellis drainage'), L(10, 'Even slope'), L(10, 'Dendritic drainage'), L(10, 'Concave slope'),
      L(10, 'Drumlins'), L(10, 'Cut-off meander'))),
    ('(ii)', 2, L(10, '(ii) Explain briefly why the long-axis trend of the majority of the drumlins',
                  'map extract above.'),
     (H10, S(4, '(ii) Any valid explanation', 'Q.11', RIGHT)),
     answer('Explanation', T10, '(ii) Any valid explanation', 2, (0, 1, 2)), '0-11', GLAC),
])
PART_ONE += romans('11', P1, 11, L(11, 'Statistical Interpretation'),
                   (L(11, 'Examine the table above showing information regarding afforestation in Ireland',
                      'following questions.'),),
                   ID + 'p1-q11', ('page',), [
    ('(i)', 2, L(11, '(i) Calculate the difference between the number of hectares of trees planted privately',
                 'in 1983.'),
     (H11, S(4, 'Q.11', '(ii) 4,352', RIGHT)), answer('Difference', T11, 'Q.11 · (i) 5,371(hectares)'), '2-0', TG),
    ('(ii)', 2, L(11, '(ii) Calculate X, the total afforestation in 1953.'),
     (H11, S(4, '(ii) 4,352', '(iii) Increase', RIGHT)), answer('X', T11, '(ii) 4,352 hectares'), '2-0', TG),
    ('(iii)', 2, L(11, '(iii) What was the trend in private planting between 1923 and 2013?'),
     (H11, S(4, '(iii) Increase', '(iv) Any valid explanation', RIGHT, 'Q.11')),
     answer('Trend', T11, '(iii) Increase/rise etc.'), '2-0', TG),
    ('(iv)', 2, L(11, '(iv) Explain briefly one reason for this trend in private planting.'),
     (H11, S(4, '(iv) Any valid explanation', 'Q.12', RIGHT, 'Q.11')),
     answer('Reason', T11, '(iv) Any valid explanation', 2, (0, 1, 2)), '1-4', IRL),
])
PART_ONE.append(T(
    'p1-12', P1, '12', '', 8, 12, L(12, 'Satellite Interpretation'),
    (L(12, 'Match each of the letters A, B, C and D with the description that best matches it in the',
       'table below.'),),
    (H2, S(4, 'Q.12', None, RIGHT)),
    priced_rows(T2, ['Q.12 · D Delta', 'B Open-cast mining', 'A Dust storm', 'C Forest fire'], 2),
    '2-8', AER, ID + 'p1-q12', ('page',), (L(12, 'Examine the satellite images above.'),),
    row_labels=(L(12, 'Delta'), L(12, 'Open-cast mining'), L(12, 'Dust storm'), L(12, 'Forest fire'))))


# ---------------------------------------------------------------- Part Two --
def sketch(outline_line, outline_permitted, alloc, item_permitted, labels):
    return (fixed('Sketch outline' if 'Sketch' in outline_line else 'Map outline', 4,
                  outline_line, outline_permitted),
            *(Criterion(f'Feature {n}', 4, item_permitted, 'exact', alloc) for n in range(1, labels + 1)))


SHOWN3 = sums((0, 1, 3), (0, 1))
GRAPH = (fixed('Title', 2, ('Bar Chart etc. · Pie Chart', 'Title · 2 marks · 2 marks')),
         fixed('Axes named (bar chart) / circle and centre (pie chart)', 2,
               ('Vertical axis named', 'Horizontal axis named'), (0, 1, 2)),
         fixed('6 items illustrated', 12, '6 items illustrated', upto(12)))


def bullet_routes(prefix, items, atlas=None):
    return tuple(Route(slug(item, 34), item.rstrip('.'), ID + prefix + slug(item, 34), False,
                       keep_bullets=(item,), atlas=(atlas[item] if atlas else None))
                 for item in items)


Q1AS = (L(15, 'Examine the diagram above and answer each of the following questions.'),)
PART_TWO = romans('1A', P2, 15, L(15, 'Karst Landscapes'), Q1AS, ID + 'p2-q1a', ('page',), [
    ('(i)', 12, L(15, '(i) Name each of the landforms A, B, C, D, E and F.'),
     S(6, '(i) · A · Grike', '(ii) · Any two'),
     (fixed('A', 2, '(i) · A · Grike · 2 marks'), fixed('B', 2, 'B · Clint · 2 marks'),
      fixed('C', 2, 'C · Swallow Hole /Sink Hole · 2 marks'), fixed('D', 2, 'D · Stalactite · 2 marks'),
      fixed('E', 2, 'E · Stalagmite · 2 marks'), fixed('F', 2, 'F · Pillar/Column · 2 marks')), '0-3', KARST),
    ('(ii)', 4, L(15, '(ii) Name any two processes of chemical weathering.'),
     S(6, '(ii) · Any two', '(iii) · Any valid'),
     (pair('(ii) · Any two valid processes · 2 + 2 marks', 'Two processes'),), '0-8', RW + KARST),
    ('(iii)', 4, L(15, '(iii) State what is meant by the term permeable rock and name an example of a',
                   'permeable rock.'),
     S(6, '(iii) · Any valid', None), (pair('(iii) · Any valid statement & example · 2 + 2 marks',
                                            'Statement and example'),), '0-3', KARST + RW),
])
LANDFORMS = 'one fluvial, coastal or glacial landform'
PART_TWO += [
    T('p2-1b', P2, '1B', '', 30, 15, L(15, 'Surface Processes'),
      (L(15, '(i) Examine the impact of the processes of erosion on the formation of one fluvial,',
         'that you have studied.'),),
      (S(7, 'Processes of erosion named', 'Or'),),
      (pair('Processes of erosion named · 2 + 2 marks', 'Processes of erosion named'),
       fixed('Landform of erosion named', 2, 'Landform of erosion named · 2 marks'),
       srp('Examination', 12, f'Examination · 12 x {SRPS}')),
      '0-9', RIVERS, ID + 'p2-q1b-route-i-fluvial-landform',
      routes=(
          Route('route-i-fluvial-landform', 'Route (i) · one fluvial landform', ID + 'p2-q1b-route-i-fluvial-landform',
                False, ((LANDFORMS, 'one fluvial'),), topic='0-9', atlas=RIVERS),
          Route('route-i-coastal-landform', 'Route (i) · one coastal landform', ID + 'p2-q1b-route-i-coastal-landform',
                False, ((LANDFORMS, 'coastal'),), topic='0-10', atlas=SEA),
          Route('route-i-glacial-landform', 'Route (i) · one glacial landform', ID + 'p2-q1b-route-i-glacial-landform',
                False, ((LANDFORMS, 'glacial landform'),), topic='0-11', atlas=GLAC),
          Route('route-ii', 'Route (ii)', ID + 'p2-q1b-route-ii', False,
                prompt=(L(15, '(ii) Describe and explain the factors governing the operation of one mass',
                          'that you have studied.'),),
                scheme=(S(7, 'Factors identified', None),),
                criteria=(pair('Factors identified · 2 + 2 marks', 'Factors identified'),
                          fixed('Mass movement process named', 2, 'Mass movement process named · 2 marks'),
                          srp('Description/explanation', 12, f'Description/explanation · 12 x {SRPS}')),
                topic='0-8', atlas=RW),
      )),
    T('p2-1c', P2, '1C', '', 30, 15, L(15, 'Tectonic Activity – Irish Landscape Development'),
      (L(15, 'Examine the influence of tectonic activity on the development of the Irish landscape.'),),
      (S(8, 'Tectonic activity identified', None),),
      (fixed('Tectonic activity identified', 2, 'Tectonic activity identified · 2 marks'),
       srp('Examination', 14, f'Examination · 14 x {SRPS}')),
      '0-0', PS + EV + RW, ID + 'p2-q1c'),
    T('p2-2a', P2, '2A', '', 20, 16, L(16, 'Ordnance Survey Map'),
      (L(16, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper.',
         'Kenmare River shown on the map.'),),
      (S(9, 'Sketch outline:', None),),
      sketch('Sketch outline: · 4 marks', (0, 4),
             ('4 features @ 4 marks each: · Shown 3 marks (graded 3/1/0)', 'Label 1 mark'), SHOWN3, 4),
      '2-6', MAP + RIVERS, ID + 'p2-q2a', ('map', 'legend'),
      row_labels=(None, L(16, 'The entire route of the waymarked walk called the Béara Way shown on the map'),
                  L(16, 'The entire area of coniferous plantation at V 85 72'),
                  L(16, 'The entire area of land above 300 metres at Letter South'),
                  L(16, 'The entire area of the Kenmare River shown on the map.'))),
    T('p2-2b', P2, '2B', '', 30, 16, L(16, 'Sedimentary Rocks'),
      (L(16, 'Explain the formation of sedimentary rocks, with reference to Irish examples.'),),
      (S(10, 'Irish examples of sedimentary rocks · 2', 'C. · Isostasy'),),
      (pair('Irish examples of sedimentary rocks · 2 + 2 marks', 'Irish examples'),
       srp('Explanation of formation', 13, f'Explanation of formation · 13 x {SRPS}')),
      '0-1', RW, ID + 'p2-q2b'),
    T('p2-2c', P2, '2C', '', 30, 16, L(16, 'Isostacy'),
      (L(16, 'Examine how isostacy has impacted on the Irish landscape.'),),
      (S(10, 'Impact identified', None),),
      (fixed('Impact identified', 2, 'Impact identified · 2 marks'), srp('Examination', 14, f'Examination · 14 x {SRPS}')),
      '0-5', SEA + RIVERS, ID + 'p2-q2c'),
]
Q3AS = (L(17, 'Examine the diagram above and answer each of the following questions.'),)
PART_TWO += romans('3A', P2, 17, L(17, 'Glaciation'), Q3AS, ID + 'p2-q3a', ('page',), [
    ('(i)', 12, L(17, '(i) Name each of the landforms A, B, C, D, E and F.'),
     S(11, '(i) · A · Drumlin', '(ii) · Any valid'),
     (fixed('A', 2, '(i) · A · Drumlin · 2 marks'), fixed('B', 2, 'B · Terminal moraine · 2 marks'),
      fixed('C', 2, 'C · Outwash plain · 2 marks'), fixed('D', 2, 'D · Esker · 2 marks'),
      fixed('E', 2, 'E · Kettle hole · 2 marks'), fixed('F', 2, 'F · Kame · 2 marks')), '0-11', GLAC),
    ('(ii)', 4, L(17, '(ii) Explain briefly what is meant by a fluvioglacial process.'),
     S(11, '(ii) · Any valid', '(iii) · Any two'), (pair('(ii) · Any valid explanation · 2 + 2 marks', 'Explanation'),),
     '0-11', GLAC),
    ('(iii)', 4, L(17, '(iii) Name any two fluvioglacial landforms.'),
     S(11, '(iii) · Any two', None), (pair('(iii) · Any two valid landforms · 2 + 2 marks', 'Two landforms'),),
     '0-11', GLAC),
])
FOLDS = ('Folding', 'Faulting.')
ROCK = ('Mining', 'Extraction of building materials', 'Oil/gas exploitation', 'Geothermal energy production.')
SECTORS = 'transport or tourism'
PART_TWO += [
    T('p2-3b', P2, '3B', '', 30, 17, L(17, 'Landform Development'),
      (L(17, 'Explain how one of the following influences the development of landforms:', 'Faulting.'),),
      (S(12, 'Landform identified', 'C. · Human'),),
      (fixed('Landform identified', 2, 'Landform identified · 2 marks'),
       srp('Explanation', 14, f'Explanation · 14 x {SRPS}')),
      '0-2', RW + PS, ID + 'p2-q3b-folding', routes=bullet_routes('p2-q3b-', FOLDS)),
    T('p2-3c', P2, '3C', '', 30, 17, L(17, 'Human Interaction with the Rock Cycle'),
      (L(17, 'Examine how humans interact with the rock cycle, with reference to one of the',
         'Geothermal energy production.'),),
      (S(12, 'Examination · 15', None),), (srp('Examination', 15, f'Examination · 15 x {SRPS}'),),
      '0-6', RW, ID + 'p2-q3c-mining', routes=bullet_routes('p2-q3c-', ROCK)),
    T('p2-4a', P2, '4A', '', 20, 18, L(18, 'Map Skills'),
      (L(18, 'Draw an outline map of a European region (not in Ireland) that you have studied.',
         'A named river.'),),
      (S(13, 'Map outline', None),),
      sketch('Map outline · 4 marks graded (4/2/0)', (0, 2, 4),
             ('4 features @ 4 marks each: · Shown 2 marks graded (2/1/0)', 'Named 2 marks'),
             sums((0, 1, 2), (0, 2)), 4),
      '1-5', EURO, ID + 'p2-q4a',
      row_labels=(None, L(18, 'A named feature of relief'), L(18, 'A named urban centre'),
                  L(18, 'A named road or rail link'), L(18, 'A named river.'))),
    T('p2-4b', P2, '4B', '', 30, 18, L(18, 'Industrial Decline'),
      (L(18, 'Examine the causes and impacts of industrial decline with reference to any region(s)',
         'that you have studied.'),),
      (S(14, 'Cause identified', 'C. · Tertiary'),),
      (fixed('Cause identified', 2, 'Cause identified · 2 marks'), fixed('Impact identified', 2, 'Impact identified · 2 marks'),
       srp('Examination', 13, f'Examination · 13 x {SRPS}')),
      '1-1', IRL + EURO, ID + 'p2-q4b'),
    T('p2-4c', P2, '4C', '', 30, 18, L(18, 'Tertiary Activity in Ireland'),
      (L(18, 'Account for the development of transport or tourism in an Irish region that you have',
         'studied .'),),
      (S(14, 'Examination · 15', None),), (srp('Examination', 15, f'Examination · 15 x {SRPS}'),),
      '1-4', IRL, ID + 'p2-q4c-transport',
      routes=(Route('transport', 'transport', ID + 'p2-q4c-transport', False, ((SECTORS, 'transport'),)),
              Route('tourism', 'tourism', ID + 'p2-q4c-tourism', False, ((SECTORS, 'tourism'),)))),
]
Q5AS = (L(19, 'Using the information in the pie chart above, answer each of the following questions.'),)
PART_TWO += romans('5A', P2, 19, L(19, 'Irish Seafood Exports', nth=0), Q5AS, ID + 'p2-q5a', ('page',), [
    ('(i)', 4, L(19, '(i) Name the two European Union (EU) member states to which Ireland exported the',
                 'most seafood in 2012.'),
     S(15, '(i) · France', '(ii) · Russia'), (pair('(i) · France & United Kingdom · 2 + 2 marks', 'Two member states'),),
     '2-0', TG),
    ('(ii)', 4, L(19, '(ii) Name the two regions/countries to which Ireland exported the least seafood in 2012.'),
     S(15, '(ii) · Russia', '(iii) · 30'), (pair('(ii) · Russia & Other Non-EU · 2 + 2 marks', 'Two regions/countries'),),
     '2-0', TG),
    ('(iii)', 4, L(19, '(iii) Calculate the total percentage of seafood exports to non-EU regions/countries in',
                   '2012.'),
     S(15, '(iii) · 30', '(iv) · Any two'), (fixed('Total percentage', 4, '(iii) · 30 (%) · 4 marks'),), '2-0', TG),
    ('(iv)', 8, L(19, '(iv) Explain briefly two challenges facing the Irish fishing industry.'),
     S(15, '(iv) · Any two', None),
     (fixed('Challenge 1', 4, '(iv) · Any two valid challenges explained @ 4 marks each 2 + 2 marks', (0, 2, 4)),
      fixed('Challenge 2', 4, '=2 + 2 marks', (0, 2, 4))), '1-4', IRL),
])
HUMAN = ('Population dynamics', 'Language', 'Religion', 'Urban development', 'Rural development')
PART_TWO += [
    T('p2-5b', P2, '5B', '', 30, 19, L(19, 'Manufacturing in a European Region'),
      (L(19, 'Account for the development of manufacturing in a European region (not in Ireland) that',
         'you have studied.'),),
      (S(16, 'Examination · 15', 'C. · The Dynamics'),), (srp('Examination', 15, f'Examination · 15 x {SRPS}'),),
      '1-5', EURO, ID + 'p2-q5b'),
    T('p2-5c', P2, '5C', '', 30, 19, L(19, 'The Dynamics of Regions – Human Processes'),
      (Lift(19, 'Population dynamics', 'Rural development', row=True),
       L(19, 'Examine the influence of any two of the human processes in the table above',
         'that you have studied.')),
      (S(16, 'Process 1', None),),
      (fixed('Process 1 influence identified', 2, ('Process 1', 'Influence identified · 2 marks@0')),
       srp('Process 1 examination', 7, f'Examination · 7 x {SRPS}'),
       fixed('Process 2 influence identified', 2, ('Process 2', 'Influence identified · 2 marks@1')),
       srp('Process 2 examination', 6, f'Examination · 6 x {SRPS}')),
      '1-6', CONT, ID + 'p2-q5c', absorbs=pool(ID + 'p2-q5c-', HUMAN, 2)[1]),
]
Q6AS = (L(20, 'Examine the information above regarding immigration to Ireland and emigration from',
          'following questions.'),)
PART_TWO += romans('6A', P2, 20, L(20, 'Ireland - Population Dynamics'), Q6AS, ID + 'p2-q6a', ('page',), [
    ('(i)', 4, L(20, '(i) How many people immigrated to Ireland from Canada and how many people',
                 'from Ireland?'),
     S(17, '(i) · 1200', '(ii) · 22'), (pair('(i) · 1200 & 4700 · 2 + 2 marks', 'Two numbers'),), '2-0', TG + POP),
    ('(ii)', 4, L(20, '(ii) How many immigrants came from the ‘Rest of the World’?', 'within this area.'),
     S(17, '(ii) · 22', '(iii) · 50.3'), (pair('(ii) · 22 400 & valid example · 2 + 2 marks', 'Number and example'),),
     '2-0', TG + POP),
    ('(iii)', 4, L(20, '(iii) What percentage of the 81,900 people that emigrated from Ireland were not Irish',
                   'emigrated from Ireland.'),
     S(17, '(iii) · 50.3', '(iv) · Any two'),
     (pair('(iii) · 50.3(%) and any valid statement · 2 + 2 marks', 'Percentage and reason'),), '4-2', POP + TG),
    ('(iv)', 8, L(20, '(iv) Explain briefly two positive impacts of immigration on Ireland.'),
     S(17, '(iv) · Any two', None),
     (fixed('Impact 1', 4, '(iv) · Any two valid explanations · 2 + 2 marks', (0, 2, 4)),
      fixed('Impact 2', 4, '=2 + 2 marks', (0, 2, 4))), '4-2', POP),
])
PART_TWO += [
    T('p2-6b', P2, '6B', '', 30, 20, L(20, 'Primary Economic Activity – Continental / Sub-Continental Region'),
      (L(20, 'Examine the factors that influence the development of one primary economic activity',
         'that you have studied.'),),
      (S(18, 'Factors identified', 'C. · Dynamics'),),
      (pair('Factors identified · 2 + 2 marks', 'Factors identified'), srp('Examination', 13, f'Examination · 13 x {SRPS}')),
      '1-6', CONT, ID + 'p2-q6b'),
    T('p2-6c', P2, '6C', '', 30, 20, L(20, 'Dynamics of Regions – Climate'),
      (L(20, 'Describe and explain the challenges facing any region that you have studied, as a result',
         'its climate.'),),
      (S(18, 'Challenges identified', None),),
      (pair('Challenges identified · 2 + 2 marks', 'Challenges identified'),
       srp('Description/explanation', 13, f'Description/explanation · 13 x {SRPS}')),
      '1-1', IRL + EURO + CONT, ID + 'p2-q6c'),
]

Q7AS = (L(22, 'Read the extract above and answer each of the following questions.'),)
PART_TWO += romans('7A', P2, 22, L(22, 'Future Development of Economic Activities'), Q7AS, ID + 'p2-q7a', ('page',), [
    ('(i)', 4, L(22, '(i) Name two types of social media mentioned in the extract above.'),
     S(20, '(i) · Facebook', '(ii) · 25'), (pair('(i) · Facebook/Twitter/YouTube · 2 + 2 marks', 'Two types'),),
     '2-0', TG),
    ('(ii)', 4, L(22, '(ii) By what percentage were Irish enterprises ahead of the EU-28 average in the use',
                  'of social media?'),
     S(20, '(ii) · 25', '(iii) · 2nd'), (fixed('Percentage', 4, '(ii) · 25(%) · 4 marks'),), '2-0', TG),
    ('(iii)', 4, L(22, '(iii) Where was Ireland ranked in the EU-28 in the use of social media in 2014 and what',
                   'use of social media?'),
     S(20, '(iii) · 2nd', '(iv) · Any valid'), (pair('(iii) · 2nd & Malta · 2 + 2 marks', 'Rank and country'),),
     '2-0', TG),
    ('(iv)', 4, L(22, '(iv) Explain briefly what is meant by the term e-commerce.'),
     S(20, '(iv) · Any valid', '(v) · Any two'), (pair('(iv) · Any valid explanation · 2 + 2 marks', 'Explanation'),),
     '3-0', ECON),
    ('(v)', 4, L(22, '(v) State two advantages of developments such as social media and e-commerce for',
                 'economic activity.'),
     S(20, '(v) · Any two', None), (pair('(v) · Any two valid advantages stated · 2 + 2 marks', 'Two advantages'),),
     '3-0', ECON),
])
PART_TWO += [
    T('p2-7b', P2, '7B', '', 30, 22, L(22, 'Environmental Impact'),
      (L(22, 'Examine the environmental impact of economic activities at a local scale and on a global',
         'scale.'),),
      (S(21, 'Local environmental', 'C. · Colonialism'),),
      (fixed('Local environmental impact identified', 2, 'Local environmental impact identified · 2 marks'),
       fixed('Global environmental impact identified', 2, 'Global environmental impact identified · 2 marks'),
       srp('Examination', 13, f'Examination · 13 x {SRPS}')),
      '3-4', ENV, ID + 'p2-q7b'),
    T('p2-7c', P2, '7C', '', 30, 22, L(22, 'Colonialism'),
      (L(22, 'Examine the impact of colonialism on an economy in the developing world that you have',
         'studied.'),),
      (S(21, 'Developing economy named', None),),
      (fixed('Developing economy named', 2, 'Developing economy named · 2 marks'),
       fixed('Impact identified', 2, 'Impact identified · 2 marks'), srp('Examination', 13, f'Examination · 13 x {SRPS}')),
      '3-1', DEV, ID + 'p2-q7c'),
    T('p2-8a', P2, '8A', '', 20, 23, L(23, 'Aerial Photograph'),
      (L(23, 'Examine the aerial photograph accompanying this paper.', 'suitable for development.'),),
      (S(22, 'utline:', None),),
      sketch('Sketch 0utline: · 4 marks', (0, 4),
             ('4 features @ 4 marks each: · Shown 3 marks (graded 3/1/0)', 'Label 1 mark'), SHOWN3, 4),
      '2-8', AER + ECON, ID + 'p2-q8a', ('aerial',),
      row_labels=(None, L(23, 'A car park'),
                  L(23, 'The triangular street network in the middleground of the aerial photograph'),
                  L(23, 'A large commercial/industrial building in the foreground of the aerial photograph'),
                  L(23, 'An area of waste ground suitable for development.'))),
    T('p2-8b', P2, '8B', '', 30, 23, L(23, 'Mobility of Economic Activities'),
      (L(23, 'Examine the mobility of modern economic activities with reference to one multinational',
         'company that you have studied.'),),
      (S(23, 'MNC named', 'C. · Sustainable'),),
      (fixed('MNC named', 2, 'MNC named · 2 marks'), srp('Examination', 14, f'Examination · 14 x {SRPS}')),
      '3-2', MNC, ID + 'p2-q8b'),
    T('p2-8c', P2, '8C', '', 30, 23, L(23, 'Sustainable Development'),
      (L(23, 'Examine the role of sustainable development in controlling the environmental impact of',
         'economic activities.'),),
      (S(23, 'Examination · 15', None),), (srp('Examination', 15, f'Examination · 15 x {SRPS}'),),
      '3-4', ENV, ID + 'p2-q8c'),
]
Q9AS = (L(24, 'Examine the data above showing the total waste generated by households and businesses',
          '2004 and 2012.'),)
PART_TWO += romans('9A', P2, 24, L(24, 'The Environment'), Q9AS, ID + 'p2-q9a', ('page',), [
    ('(i)', 16, L(24, '(i) Using graph paper, draw a suitable graph to illustrate this data.'),
     S(24, 'Bar Chart etc.', '(ii) · Explain briefly'), GRAPH, '2-0', TG),
    ('(ii)', 4, L(24, '(ii) Explain briefly one reason why a charge is usually applied for the disposal of',
                  'waste.'),
     S(24, 'Any valid explanation', None), (pair('Any valid explanation · 2 + 2 marks', 'Reason'),), '3-4', ENV),
])
REASON_9B = ('Three reasons · @ 10 marks each', 'For each reason:', 'Reason stated · 2 marks',
             'Map reference / evidence · 2 marks', f'Explanation · 3 x {SRPS}')
PART_TWO += [
    T('p2-9b', P2, '9B', '', 30, 24, L(24, 'Location of Economic Activity'),
      (L(24, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper.'),
       L(24, 'Explain three reasons why it may be difficult to attract large foreign companies',
         'on the Ordnance Survey map.'),
       L(24, 'Use evidence from the Ordnance Survey map to support each reason.')),
      (S(25, 'Three reasons', 'C. · European'),),
      tuple(Criterion(f'Reason {n}', 10, evens(10), 'srp', REASON_9B) for n in (1, 2, 3)),
      '3-2', MNC + MAP, ID + 'p2-q9b', ('map', 'legend')),
    T('p2-9c', P2, '9C', '', 30, 24, L(24, 'European Union Policy'),
      (L(24, 'Examine the impact of European Union policy on the development of primary economic',
         'activity in Ireland.'),),
      (S(25, 'Impact on primary activity identified', None),),
      (fixed('Impact on primary activity identified', 2, 'Impact on primary activity identified · 2 marks'),
       srp('Examination', 14, f'Examination · 14 x {SRPS}')),
      '3-3', EU_ECON + IRL, ID + 'p2-q9c'),
]
TRAFFIC = 'Three different methods for managing traffic evident on the aerial photograph.'
PROBLEMS = ('Traffic congestion', 'Urban decay', 'Urban sprawl.')
PART_TWO += [
    T('p2-10a', P2, '10A', '', 20, 25, L(25, 'Aerial Photograph'),
      (L(25, 'Examine the aerial photograph accompanying this paper.', 'evident on the aerial photograph.'),),
      (S(26, 'Sketch outline:', None),),
      sketch('Sketch outline: · 4 marks', (0, 4),
             ('4 features @ 4 marks each · Shown 3 marks (graded 3/1/0)', 'Label 1 mark'), SHOWN3, 4),
      '2-8', AER + URB, ID + 'p2-q10a', ('aerial',),
      row_labels=(None, L(25, 'The triangular street network in the middleground of the aerial photograph'),
                  L(25, TRAFFIC), L(25, TRAFFIC), L(25, TRAFFIC))),
    T('p2-10b', P2, '10B', '', 30, 25, L(25, 'Urban Problems'),
      (L(25, 'Discuss how the growth of urban centres can lead to any two of the following problems,',
         'Urban sprawl.'),),
      (S(27, 'Example of urban centre', 'C. · Overpopulation'),),
      (fixed('Example of urban centre', 2, 'Example of urban centre · 2 marks'),
       srp('Discussion of problem 1', 7, f'Discussion of problem 1 · 7 x {SRPS}'),
       srp('Discussion of problem 2', 7, f'Discussion of problem 2 · 7 x {SRPS}')),
      '4-5', URB, ID + 'p2-q10b', absorbs=pool(ID + 'p2-q10b-', PROBLEMS, 2)[1]),
    T('p2-10c', P2, '10C', '', 30, 25, L(25, 'Overpopulation'),
      (L(25, 'Describe and explain the causes and effects of overpopulation, with reference to',
         'that you have studied.'),),
      (S(27, 'Cause identified', None),),
      (fixed('Cause identified', 2, 'Cause identified · 2 marks'), fixed('Effect identified', 2, 'Effect identified · 2 marks'),
       pair('Examples · 2 + 2 marks', 'Examples'),
       srp('Description/explanation', 11, f'Description/explanation · 11 x {SRPS}')),
      '4-1', POP, ID + 'p2-q10c'),
]
Q11AS = (L(26, 'Examine the data above showing Irish birth and death rates in 1950, 1990 and 2013.'),)
PART_TWO += romans('11A', P2, 26, L(26, 'Population Dynamics'), Q11AS, ID + 'p2-q11a', ('page',), [
    ('(i)', 16, L(26, '(i) Using graph paper, draw a suitable graph to illustrate this data.'),
     S(28, 'Bar Chart etc.', '(ii) · Explain briefly'), GRAPH, '2-0', TG),
    ('(ii)', 4, L(26, '(ii) Explain briefly one reason for the decline in Irish birth rates between 1950 and',
                  '2013.'),
     S(28, 'Any valid explanation', None), (pair('Any valid explanation · 2 + 2 marks', 'Reason'),), '4-0', POP),
])
PART_TWO += [
    T('p2-11b', P2, '11B', '', 30, 26, L(26, 'Urban Settlement'),
      (L(26, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper.'),
       L(26, '‘Transport and routeways have played a role', 'present day.’'),
       L(26, 'Discuss this statement, using evidence from the Ordnance Survey map to support your', 'answer.')),
      (S(29, 'Map evidence · 2 marks', 'C. · Migration'),),
      (fixed('Map evidence', 2, 'Map evidence · 2 marks'), srp('Discussion', 14, f'Discussion · 14 x {SRPS}')),
      '4-3', URB + MAP, ID + 'p2-q11b', ('map', 'legend')),
    T('p2-11c', P2, '11C', '', 30, 26, L(26, 'Migration'),
      (L(26, 'Examine the impact of migration on a city in the developing world that you have studied.'),),
      (S(29, 'Example of developing world city', None),),
      (fixed('Example of developing world city', 2, 'Example of developing world city · 2 marks'),
       fixed('Impact identified', 2, 'Impact identified · 2 marks'), srp('Examination', 13, f'Examination · 13 x {SRPS}')),
      '4-2', POP + URB, ID + 'p2-q11c'),
]
Q12AS = (L(27, 'Examine the population pyramids above and answer each of the following questions.'),)
PART_TWO += romans('12A', P2, 27, L(27, 'Population', nth=0), Q12AS, ID + 'p2-q12a', ('page',), [
    ('(i)', 4, L(27, '(i) What percentage of males in Pyramid A are in the 40-44 year age group and what',
                 '25-29 year age group?'),
     S(30, '(i) · 2 & 3', '(ii) · Pyramid B'), (pair('(i) · 2 & 3 (%) · 2 + 2 marks', 'Two percentages'),), '2-0', TG),
    ('(ii)', 4, L(27, '(ii) Are more people living longer in the area represented by Pyramid A or Pyramid B?',
                  'support your answer.'),
     S(30, '(ii) · Pyramid B', '(iii) · Pyramid A'),
     (pair('(ii) · Pyramid B & any valid piece of evidence · 2 + 2 marks', 'Pyramid and evidence'),), '4-0', POP),
    ('(iii)', 4, L(27, '(iii) Which of the pyramids, A or B, represents a developing economy?', 'developing economy.'),
     S(30, '(iii) · Pyramid A', '(iv) · Any two'),
     (pair('(iii) · Pyramid A & any valid named example · 2 + 2 marks', 'Pyramid and example'),), '4-0', POP),
    ('(iv)', 8, L(27, '(iv) Explain briefly two challenges facing an economy with a population pyramid',
                  'similar to Pyramid B.'),
     S(30, '(iv) · Any two', None),
     (fixed('Challenge 1', 4, '(iv) · Any two valid challenges explained · 2 + 2 marks', (0, 2, 4)),
      fixed('Challenge 2', 4, '=2 + 2 marks', (0, 2, 4))), '4-0', POP),
])
PART_TWO.append(T(
    'p2-12b', P2, '12B', '', 30, 27, L(27, 'Urban Planning'),
    (L(27, 'Examine the impact of urban planning strategies with reference to example(s) that you',
       'have studied.'),),
    (S(31, 'Impact identified', 'C. · Phases'),),
    (fixed('Impact identified', 2, 'Impact identified · 2 marks'), fixed('Example', 2, 'Example · 2 marks'),
     srp('Examination', 13, f'Examination · 13 x {SRPS}')),
    '4-4', LAND + URB, ID + 'p2-q12b'))
Q12CS = (L(28, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper and',
           'following questions.'),)
Q12CI = L(28, '(i) Name three different phases of historical settlement evident on the Ordnance', 'Survey map.')
PHASE = ('(iii) Explanation of each phase', '@ 4 marks each · 3 @ (2 + 2 marks)')
PART_TWO += romans('12C', P2, 28, L(28, 'Phases of Historical Settlement'), Q12CS, ID + 'p2-q12c', ('map', 'legend'), [
    ('(i)', 6, Q12CI, S(31, '(i) Three historical', '(ii) Examples'),
     (fixed('Three phases named', 6, '(i) Three historical phases named · 2 + 2 + 2 marks', (0, 2, 4, 6)),),
     '4-3', URB + MAP),
    ('(ii)', 12, L(28, '(ii) Name and locate, using six-figure grid references, examples of each of the three',
                   'named above.'),
     S(31, '(ii) Examples', '(iii) Explanation'),
     (fixed('Examples named', 6, '(ii) Examples of each phase named · 2 + 2 + 2 marks', (0, 2, 4, 6)),
      fixed('Examples located', 6, 'Loc/GR for each example · 2 + 2 + 2 marks', (0, 2, 4, 6))),
     '4-3', URB + MAP, (), (Q12CI,)),
    ('(iii)', 12, L(28, '(iii) Explain briefly each of the three phases of historical settlement named above.'),
     S(31, '(iii) Explanation', None),
     tuple(Criterion(f'Phase {n}', 4, (0, 2, 4), 'exact', PHASE) for n in (1, 2, 3)), '4-3', URB + MAP,
     (), (Q12CI,)),
])

# ------------------------------------------------------------------ Options --
OC = (S(33, '*Overall Coherence (20 marks)', None, table=True),)
COHERENCE = Criterion('Overall coherence', 20, (0, 6, 10, 14, 17, 20), 'exact',
                      ('Overall Coherence · 20 marks graded*', '*Overall Coherence (20 marks)', 'Excellent · 20',
                       'Very Good · 17', 'Good · 14', 'Fair · 10', 'Weak · 6', 'Poor · 0'))
OPTION_CRITERIA = (
    Criterion('Aspects (3 @ 20 marks or 4 @ 15 marks)', 60, upto(60), 'srp',
              ('Number of aspects', 'Identifying aspect', '8 x SRP')),
    COHERENCE)


def option(q, page, theme, note_nth, prompt, scheme_page, topic, atlas, after=None, end=None):
    return T(f'p2-{q}', P2, q, '', 80, page, theme, prompt if isinstance(prompt, tuple) else (prompt,),
             (S(scheme_page, 'Number of aspects', end, None, after), *OC), OPTION_CRITERIA,
             topic, (atlas,), ID + f'p2-q{q}',
             stem=(L(page, 'Note: It is better to discuss three or four aspects', 'large number of points.',
                     nth=note_nth),))


GI, GE = H + 'option-global-interdependence', H + 'option-geoecology'
CI, AO = H + 'option-culture-identity', H + 'option-atmosphere-ocean'
OPTIONS = [
    option('13', 30, L(30, 'Global Interdependence'), 0,
           L(30, '‘We live in an interdependent global economy.', 'Human rights issues.'), 34, '5-1', GI,
           after='13.', end='14.'),
    option('14', 30, L(30, 'Global Interdependence'), 0,
           L(30, '‘Empowering people is a way of linking economic growth with human development.’',
             'aid programmes.'), 34, '5-2', GI, after='14.'),
    option('15', 30, L(30, 'Global Interdependence'), 0,
           L(30, 'Discuss the potential impact of Fair Trade on human and economic development.'), 35, '5-3', GI),
    option('16', 30, L(30, 'Geoecology'), 1,
           L(30, 'Examine the influence of mineral matter, air, water and organic matter on soil', 'development.'),
           36, '6-0', GE, after='16.', end='17.'),
    option('17', 30, L(30, 'Geoecology'), 1,
           L(30, 'Discuss the impact of human activity on soil.'), 36, '6-1', GE, after='17.'),
    option('18', 30, L(30, 'Geoecology'), 1,
           L(30, 'Examine, with reference to one biome that you have studied, how plants and animals',
             'soil conditions.'), 37, '6-2', GE),
    option('19', 31, L(31, 'Culture and Identity'), 0,
           L(31, 'Examine the impact of colonialism and migration on ethnic/racial patterns.'), 38, '7-0', CI,
           after='19.', end='20.'),
    option('20', 31, L(31, 'Culture and Identity'), 0,
           L(31, '‘Identity as a concept entails a variety of cultural factors including nationality,',
             'Discuss.'), 38, '7-2', CI, after='20.'),
    option('21', 31, L(31, 'Culture and Identity'), 0,
           L(31, 'Examine the effects of political and/or physical boundaries on cultural groups.'), 39, '7-1', CI),
    option('22', 31, L(31, 'The Atmosphere – Ocean Environment'), 1,
           L(31, 'Account for the distinctive nature of one global climate type that you have studied.'),
           40, '8-4', AO, after='22.', end='23.'),
    option('23', 31, L(31, 'The Atmosphere – Ocean Environment'), 1,
           L(31, 'Examine how solar energy is transformed and redistributed through circulation',
             'atmosphere and oceans.'), 40, '8-1', AO, after='23.'),
    option('24', 31, L(31, 'The Atmosphere – Ocean Environment'), 1,
           L(31, 'Examine the formation of mid-latitude depressions and anticyclones, and the weather',
             'associated with them.'), 41, '8-3', AO),
]

TASKS = [*PART_ONE, *PART_TWO, *OPTIONS]

ID_CORRECTION_REASON = 'No 2015 Higher card shipped before this review; every card is new.'

# No 2015 Higher card was live on origin/main before this review.
LEGACY_IDS: list[str] = []
