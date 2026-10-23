"""Independent review ledger: Leaving Certificate Geography 2010 Ordinary Level.

Sources (English editions, harvested Paper Trail corpus; sizes and SHA-256
pinned in EXPECTED_SOURCES and the generated audit): the examination paper
LC005GLP000EV (28 pages; one booklet printed Part One, answered in it, and
Part Two), marking scheme LC005GLP000EV (36 pages), and the common
Carrick-on-Suir companions shared with Higher Level, all published only as
JPEG images. In 2010 the SEC file names are swapped relative to later years:
LC005CLP004EV.jpg (2409 x 3507) is the 1:50 000 Ordnance Survey map extract
of Carrick-on-Suir, LC005CLP003EV.jpg (5000 x 3253) is the oblique aerial
photograph of the town, and LC005CLP000EV.jpg (2481 x 3508) is the Discovery
Series legend sheet. Each was rendered and identified by eye on 2026-10-23.
Part One is 100 marks (attempt ten of twelve @ 10), Part Two 300 (three
questions @ 100).

Visual sweep (every page rendered and read on 2026-10-23):
  Paper p1 cover and examiner's grid; p2-p10 Part One Questions 1-12 (p2
  opens with the Part One instructions; p4 holds Q3 and Q4, p5 Q5 and Q6,
  p6 Q7 and Q8); p11 Part Two instructions; p12 Section 1 divider; p13-p19
  Q1-Q6 (p13 and p17 open with their dividers; p13 holds 1A and 1B, p14
  1C); p20 Section 2 divider; p21-p27 Electives Q7-Q12 (p21 and p25 open
  with their elective dividers; p23 holds 9A and 9B, p24 9C); p28 printed
  "Blank Page".
  Scheme p1 cover; p2 blank inside cover; p3 Geographical Investigation
  (coursework); p4-p6 Part One (Q1-Q4, Q5-Q8, Q9-Q12); p7 Part Two
  instructions and Section 1 divider; p8-p19 Q1-Q6; p20 Section 2 divider
  and Q7A; p21-p31 Q7B-Q12C; p32 investigation topics; p33 Irish-language
  bonus marks; p34-p35 blank; p36 back cover. The scheme reprints every
  question above its allocation, so every slice starts at the allocation.

The 2010 layout differs from 2014-2016. Part One questions are priced part
by part in the scheme (2 marks a part, Q5 5 + 5), so every separately
priced roman or lettered part is a task (Q2(iii)(a)-(c) each), and a table
answered row by row is one card of rows. Matching tables, in the printed
row order: Q1 Outer Core B, Mantle convection current C, Inner Core D,
Mid-Ocean Ridge E, Ocean trench A; Q3 A 4, B 5, C 3, D 2, E 1; Q6(i)
S 415 220 Public Telephone, S 362 235 Enclosure etc., S 432 226 Parking,
S 402 203 18 Hole Golf Course; Q11 Hurricane F, A retreating glacier A, An
urban area E, A desert C, An erupting volcano B (Mount Everest D is printed
and the scheme prices it 0 marks); Q12(i) Waterfall C, Interlocking Spur B,
Meander A. Q8's five words are priced in the scheme's own completed
paragraph (LIMESTONE, CARBONATION, GRIKES, CLINTS, PAVEMENT; the last two
share one printed line).

Q4 (Volcanic Landforms) is held: the scheme answers it only with a copy of
the diagram carrying the five terms in its boxes (see HELD).

Part Two tariffs as printed: twelve parts carry 40 marks (1C, 2B, 3B, 4B,
5B, 6C, 7C, 8B, 9C, 10C, 11B, 12B) and the rest 30. Where the scheme
prints "graded" with no grades (sketch outline, proportions, showing, graph
axes and items, Q5(i) distance, 10C(i) locations) any whole mark up to the
line's maximum is permitted. Scheme anomalies, carded as the components
print them: 7A(i) and 11A(i) are headed "Drawing graph @ 21 marks graded"
but price 2 + 3 + 3 + 16 = 24 and print "(Sub Total 24)", which with (ii)'s
6 makes the paper's [30 marks]; the slices start at the priced lines. 5A's
reprint labels (iii) and (iv) as "(i)" and "(ii)"; its allocation table
labels them correctly.
"""

from geography_review import (
    Criterion, Lift, Route, SchemeSlice, Task, pool, fixed, slug, srp, steps, sums, upto,
)

YEAR = 2010
LEVEL = 'ordinary'
PAPER_PAGES = {1: 28, 2: 28}
SCHEME_PAGES = 36
_FORTY = {'1C', '2B', '3B', '4B', '5B', '6C', '7C', '8B', '9C', '10C', '11B', '12B'}
QUESTION_TARIFFS = {1: {str(n): 10 for n in range(1, 13)},
                    2: {f'{n}{x}': (40 if f'{n}{x}' in _FORTY else 30)
                        for n in range(1, 13) for x in 'ABC'}}

EXPECTED_SOURCES = {
    'paper1': ('LC005GLP000EV.pdf', 3266667),
    'paper2': ('LC005GLP000EV.pdf', 3266667),
    'scheme': ('LC005GLP000EV.pdf', 503193),
    # 2010's names are swapped: CLP004 is the map, CLP003 the aerial photograph.
    'map': ('LC005CLP004EV.jpg', 2806497),
    'legend': ('LC005CLP000EV.jpg', 1636000),
    'aerial': ('LC005CLP003EV.jpg', 4062934),
}

_PAPER = {1: 'cover and examiner grid', **{p: 'question' for p in range(2, 11)},
          11: 'Part Two instructions', 12: 'section divider', **{p: 'question' for p in range(13, 20)},
          20: 'section divider', **{p: 'question' for p in range(21, 28)}, 28: 'blank page'}
PAGE_REVIEW = {
    # One booklet printed both parts.
    'paper1': _PAPER, 'paper2': _PAPER,
    'scheme': {1: 'cover', 2: 'blank', 3: 'geographical investigation (coursework)',
               4: 'Part One allocation', 5: 'Part One allocation', 6: 'Part One allocation',
               7: 'Part Two instructions and section divider',
               **{p: 'Part Two allocation' for p in range(8, 20)},
               20: 'section divider and Part Two allocation',
               **{p: 'Part Two allocation' for p in range(21, 32)},
               32: 'investigation topics', 33: 'Irish-language bonus marks',
               34: 'blank', 35: 'blank', 36: 'back cover'},
}

EXPECTED_SELECTION_SCAN = [
    [1, 2, 'attempt ten'], [1, 11, 'attempt three'], [1, 12, 'attempt two'],
    [1, 13, 'attempt one'], [1, 13, 'answer (i) or (ii)'], [1, 13, 'any one'], [1, 13, 'any one'],
    [1, 13, 'any one'],
    [1, 15, 'attempt to'], [1, 15, 'one of the following'],
    [1, 16, 'any one'], [1, 16, 'any one'],
    [1, 17, 'attempt one'], [1, 17, 'any two'],
    [1, 19, 'any one'], [1, 19, 'one of the following'],
    [1, 20, 'attempt one'], [1, 20, 'either'],
    [1, 24, 'choose'], [1, 24, 'any one'],
    [1, 25, 'any two'],
    [1, 27, 'any one'],
]
SELECTION_REVIEW = [
    {'scan': [[1, 2, 'attempt ten'], [1, 11, 'attempt three'], [1, 12, 'attempt two'], [1, 13, 'attempt one'],
              [1, 17, 'attempt one'], [1, 20, 'attempt one'], [1, 20, 'either']],
     'kind': 'exam-attempt-rule',
     'reason': 'Part One ten of twelve and Part Two three questions (one of Q1-3, one of Q4-6, one elective from either elective) are attempt rules; every question is carded or held.'},
    {'scan': [[1, 13, 'answer (i) or (ii)']], 'kind': 'closed-route',
     'reason': '1B: (i) or (ii) -> route (i), and route (ii) splits by its printed choose-one list of three surface processes -> 4 routes, each route\'s scheme allocation its own.'},
    {'scan': [[1, 13, 'any one'], [1, 15, 'one of the following'], [1, 16, 'any one'],
              [1, 19, 'one of the following'], [1, 24, 'choose'], [1, 24, 'any one']],
     'kind': 'closed-choose-one',
     'reason': '1B(ii) any one of three printed surface processes -> 3 routes; 2C one of three printed processes -> 3 routes; 3C any one of two printed weathering processes -> 2 routes; 6B one of two printed activities -> 2 routes; 9C choose any one of three printed EU funds -> 3 routes. 1C "one of the interactions listed above" (four printed) -> 4 routes (no directive word the scan reads; the route text is anchored on the paper).'},
    {'scan': [[1, 17, 'any two']], 'kind': 'choose-n-one-card',
     'reason': '4B any two of four printed influences -> one card with every printed item (choice is not a route).'},
    {'scan': [[1, 13, 'any one'], [1, 13, 'any one'], [1, 16, 'any one'], [1, 19, 'any one'],
              [1, 25, 'any two'], [1, 27, 'any one']],
     'kind': 'open-response',
     'reason': 'No printed pool: 1B(i) any one process of mass movement; 1B(ii) any one Irish landform; 3B(i) any one type of sedimentary rock; 6B any one Continental / Sub-Continental region; 10C(i) any two rural settlement patterns on the map; 12B(i) any one over-populated region. Compulsory lists stay whole: 1A(i), 2A, 3A(i), 4A, 6A, 8A, 12A each item.'},
    {'scan': [[1, 15, 'attempt to']], 'kind': 'not-a-selection',
     'reason': '2C "how humans attempt to control" describes human activity, not a candidate choice.'},
]

HELD = [
    {'part': 1, 'question': '4', 'title': 'Volcanic Landforms', 'marks': 10,
     'reason': ('The paper asks candidates to "fill in the blanks on the diagram" with five printed terms '
                '(Vent, Crater, Magma chamber, Lava flow, Caldera lake). The scheme (page 4, printed '
                '"Page 2 of 31") prints "Five terms @ 2 marks each as follows:" above a copy of the '
                'diagram with the terms set in its boxes: Crater and Vent upper left, Caldera Lake right, '
                'Magma Chamber lower left, Lava Flow lower right. The answer is which box each term '
                'fills, and that exists only as the scheme\'s drawing; its text layer gives the five '
                'terms alone ("Crater", "Vent", "Caldera Lake", "Magma Chamber · Lava Flow"), the same '
                'words the paper already prints. A card can show the question page but not the '
                'scheme\'s drawing, so its guidance could not tell a correct label from a misplaced '
                'one; the question is held rather than carded without its answer.')},
]

P1, P2 = 1, 2
ID = 'geography-2010-ol-'
O = 'geography-ordinary-'
SRP3 = 3


def L(page, start, end=None, nth=None):
    return Lift(page, start, end, None, nth)


def S(page, start, end=None, clip=None, after=None, table=False):
    return SchemeSlice(page, start, end, clip, after, table)


def srp3(label, count, line):
    return srp(label, count, line, SRP3)


def T(key, part, q, sub, marks, page, title, prompt, scheme, criteria, topic, atlas, card_id,
      sources=(), stem=(), routes=(), row_labels=(), absorbs=()):
    return Task(key, part, q, sub, marks, page, title, prompt, scheme, criteria, topic, atlas,
                sources, card_id, False, stem=stem, routes=routes, row_labels=row_labels,
                absorbs=absorbs)


def rows(lines, marks=2):
    return tuple(fixed(f'Row {i}', marks, line) for i, line in enumerate(lines, 1))


def romans(q, part, page, title, stem, first_id, sources, parts):
    """Separately priced romans. parts: (sub, marks, prompt Lift(s), scheme slice(s), criteria, topic, atlas
    [, row labels[, extra stem Lifts]])."""
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


def bullet_routes(prefix, items, atlas=None, topic=None):
    return tuple(Route(slug(item, 34), item.rstrip('.'), ID + prefix + slug(item, 34), False,
                       keep_bullets=(item,), atlas=(atlas[item] if atlas else None),
                       topic=(topic[item] if topic else None))
                 for item in items)


PS = (O + 'plate-tectonics',)
RW = (O + 'rocks-weathering-mass-movement',)
SEA = (O + 'the-sea',)
RIVERS = (O + 'rivers',)
GLAC = (O + 'glaciation',)
EV = (O + 'earthquakes-volcanoes',)
KARST = (O + 'karst-regions',)
MAP = (O + 'mapwork',)
AER = (O + 'aerial-photos',)
GRAPH = (O + 'graph-style-questions',)
WEATHER = (O + 'weather-climate',)
CONT = (O + 'regions-continental',)
EURO = (O + 'regions-european',)
IRL = (O + 'regions-ireland',)
ECON = (O + 'elective-economic',)
EU = (O + 'economic-ireland-the-eu',)
MNC = (O + 'economic-multinationals-globalisation',)
ENV = (O + 'economic-environmental-impact',)
DEV = (O + 'economic-developing-economies',)
POP = (O + 'human-population',)
URB = (O + 'human-urban-geography',)

# ---------------------------------------------------------------- Part One --
PART_ONE = [
    T('p1-1', P1, '1', '', 10, 2, L(2, 'Cross-section of the Earth'),
      (L(2, 'Examine the diagram below and match each of the letters in the diagram with', 'in the box below.'),),
      (S(4, 'Outer Core · B', 'Total marks 10'),),
      rows(['Outer Core · B · 2 marks', 'Mantle convection current · C · 2 marks', 'Inner Core · D · 2 marks',
            'Mid-Ocean Ridge · E · 2 marks', 'Ocean trench · A · 2 marks']),
      '0-0', PS, ID + 'p1-q1', ('page',),
      row_labels=(L(2, 'Outer Core'), L(2, 'Mantle convection current'), L(2, 'Inner Core'),
                  L(2, 'Mid-Ocean Ridge'), L(2, 'Ocean Trench'))),
]
Q2III = L(3, '(iii) Examine the table below showing total rainfall for Claremorris', 'answer the following questions:')
PART_ONE += romans('2', P1, 3, L(3, 'Ireland’s Climate'),
                   (L(3, 'Examine the map showing annual rainfall in Ireland.'),), ID + 'p1-q2', ('page',), [
    ('(i)', 2, L(3, '(i) Read the statement below and circle the correct answer:', 'East / West.'),
     S(4, 'West · 2 marks', '(ii)'), (fixed('East or West', 2, 'West · 2 marks'),), '2-7', WEATHER),
    ('(ii)', 2, L(3, '(ii) Which of the following weather systems is responsible', 'Anticyclone'),
     S(4, 'Depression/Cyclone', '(iii)'), (fixed('Weather system', 2, 'Depression/Cyclone · 2 marks'),),
     '2-7', WEATHER),
    ('(iii)(a)', 2, (Q2III, L(3, '(a) Which month had the lowest rainfall?')),
     S(4, '(a) · February', '(b) · November'), (fixed('Month', 2, '(a) · February · 2 marks'),),
     '2-7', WEATHER + GRAPH),
    ('(iii)(b)', 2, (Q2III, L(3, '(b) Which month had the highest rainfall?')),
     S(4, '(b) · November', '(c) · Valid Name'), (fixed('Month', 2, '(b) · November · 2 marks'),),
     '2-7', WEATHER + GRAPH),
    ('(iii)(c)', 2, (Q2III, L(3, '(c) Name one consequence of the high level of rainfall in Ireland in November.')),
     S(4, '(c) · Valid Name', 'Total marks 10'), (fixed('Consequence', 2, '(c) · Valid Name · 2 marks'),),
     '2-7', WEATHER),
])
PART_ONE += [
    T('p1-3', P1, '3', '', 10, 4, L(4, 'Regions'),
      (L(4, 'Match the region type (letter) with a named example in Europe', 'in the box provided.'),),
      (S(4, 'A · 4 · 2 marks', 'Total marks 10'),),
      rows(['A · 4 · 2 marks', 'B · 5 · 2 marks', 'C · 3 · 2 marks', 'D · 2 · 2 marks', 'E · 1 · 2 marks']),
      '1-0', IRL + EURO, ID + 'p1-q3', ('page',),
      row_labels=(L(4, 'Cultural'), L(4, 'Urban'), L(4, 'Core Economic'), L(4, 'Geomorphological'),
                  L(4, 'Climatic'))),
]
PART_ONE += romans('5', P1, 5, L(5, 'Ordnance Survey Map', nth=0),
                   (L(5, 'Examine the 1:50,000 Ordnance Survey map and legend accompanying this paper.', nth=0),),
                   ID + 'p1-q5', ('map', 'legend'), [
    ('(i)', 5, L(5, '(i) Measure the distance along the R 697', 'Write the correct answer in the box below.'),
     S(5, 'Correct Distance', '(ii)'), (fixed('Distance', 5, 'Correct Distance · 5 marks graded', upto(5)),),
     '2-6', MAP),
    ('(ii)', 5, L(5, '(ii) Imagine that you are driving west along the N24', 'Write the correct answer in the box below.'),
     S(5, 'Coniferous · 5 marks', 'Total marks 10'), (fixed('Plantation', 5, 'Coniferous · 5 marks'),), '2-6', MAP),
])
PART_ONE += romans('6', P1, 5, L(5, 'Ordnance Survey Map', nth=1),
                   (L(5, 'Examine the 1:50,000 Ordnance Survey map and legend accompanying this paper.', nth=1),),
                   ID + 'p1-q6', ('map', 'legend'), [
    ('(i)', 8, L(5, '(i) Name the features which can be found at each of the following grid references:'),
     S(5, '• Public Telephone', '(ii) · 263'),
     rows(['• Public Telephone · 2 marks', '• Enclosure etc. · 2 marks', '• Parking · 2 marks',
           '• 18 Hole Golf Course · 2 marks']), '2-6', MAP,
     (L(5, 'S 415 220'), L(5, 'S 362 235'), L(5, 'S 432 226'), L(5, 'S 402 203'))),
    ('(ii)', 2, L(5, '(ii) What is the height of the land at the Triangulation Pillar', 'Write the correct answer in the box below.'),
     S(5, '(ii) · 263', 'Total marks 10'), (fixed('Height', 2, '(ii) · 263 · 2 marks'),), '2-6', MAP),
])
PART_ONE += [
    T('p1-7-i', P1, '7', '(i)', 6, 6, L(6, 'Aerial Photograph and Ordnance Survey Map'),
      (L(6, '(i) Examine the aerial photograph of Carrick-on-Suir accompanying this paper.', 'write the location of:'),),
      (S(5, 'Location · 2 marks', '(ii)', None, '7. Aerial Photograph'),),
      (fixed('Location 1', 2, '=Location · 2 marks@0'), fixed('Location 2', 2, '=Location · 2 marks@1'),
       fixed('Location 3', 2, '=Location · 2 marks@2')),
      '2-8', AER, ID + 'p1-q7', ('aerial',),
      row_labels=(L(6, 'A castle'), L(6, 'A church'), L(6, 'A marina with boats'))),
    T('p1-7-ii', P1, '7', '(ii)', 4, 6, L(6, 'Aerial Photograph and Ordnance Survey Map'),
      (L(6, '(ii) Use the aerial photograph and the 1:50,000 Ordnance Survey map', 'Write the correct answer in the box below.'),
       L(6, 'What is the six-figure grid reference for this bridge?', 'Write the correct answer in the box below.')),
      (S(5, 'Dillon Bridge', 'Total marks 10'),),
      (fixed('Bridge named', 2, 'Dillon Bridge · 2 marks'),
       fixed('Six-figure grid reference', 2, 'Correct Grid Reference · 2 marks')),
      '2-6', MAP + AER, ID + 'p1-q7-ii', ('aerial', 'map')),
    T('p1-8', P1, '8', '', 10, 6, L(6, 'Karst Landscape'),
      (L(6, 'Select the correct words from the table to complete the paragraph below.', 'Grikes Carbonation'),
       L(6, 'The sedimentary rock in the photograph is called', 'known as a Limestone ___________.')),
      (S(5, 'Five words @ 2 marks', 'Total marks 10'),),
      (fixed('Word 1', 2, ('Five words @ 2 marks each as follows:', 'LIMESTONE')),
       fixed('Word 2', 2, 'CARBONATION'), fixed('Word 3', 2, 'GRIKES'), fixed('Word 4', 2, 'CLINTS'),
       fixed('Word 5', 2, 'PAVEMENT')),
      '0-3', KARST, ID + 'p1-q8', ('page',)),
]
PART_ONE += romans('9', P1, 7, L(7, 'Coastal and Glacial Features'),
                   (L(7, 'Study the Ordnance Survey and photograph extracts below', 'questions that follow:'),),
                   ID + 'p1-q9', ('page',), [
    ('(i)', 2, L(7, '(i) Name the glacial feature marked X on the map.', 'Write its correct name in the box below.'),
     S(6, '(i) · Tarn', '(ii) Arête'), (fixed('Feature X', 2, '(i) · Tarn/corrie/ cirque lake · 2 marks'),),
     '0-11', GLAC + MAP),
    ('(ii)', 2, L(7, '(ii) Name the glacial feature marked Y on the photograph.', 'Write its correct name in the box below.'),
     S(6, '(ii) Arête', '(iii) Erosion'), (fixed('Feature Y', 2, '(ii) Arête · 2 marks'),), '0-11', GLAC),
    ('(iii)', 2, L(7, '(iii) Were features X and Y formed by the process', 'Write the correct answer in the box below.'),
     S(6, '(iii) Erosion', '(iv) Sand Spit'), (fixed('Erosion or deposition', 2, '(iii) Erosion · 2 marks'),),
     '0-11', GLAC),
    ('(iv)', 2, L(7, '(iv) Name the coastal feature marked Z on the photograph.', 'Write its correct name in the box below.'),
     S(6, '(iv) Sand Spit', '(v) · Deposition'), (fixed('Feature Z', 2, '(iv) Sand Spit etc · 2 marks'),),
     '0-10', SEA),
    ('(v)', 2, L(7, '(v) Was feature Z formed by the process', 'Write the correct answer in the box below.'),
     S(6, '(v) · Deposition', 'Total marks 10'), (fixed('Erosion or deposition', 2, '(v) · Deposition · 2 marks'),),
     '0-10', SEA),
])
PART_ONE += romans('10', P1, 8, L(8, 'World’s Religions'),
                   (L(8, 'Study the above chart which shows world religions in 2007', 'answer the following questions:'),),
                   ID + 'p1-q10', ('page',), [
    ('(i)', 2, L(8, '(i) What was the largest religion in 2007?'),
     S(6, '(i) · Christian', '(ii) Buddhist'), (fixed('Largest religion', 2, '(i) · Christian · 2 marks'),),
     '2-0', GRAPH),
    ('(ii)', 2, L(8, '(ii) Which was the smallest religion in 2007?'),
     S(6, '(ii) Buddhist', '(iii) 27'), (fixed('Smallest religion', 2, '(ii) Buddhist · 2 marks'),), '2-0', GRAPH),
    ('(iii)', 2, L(8, '(iii) What is the difference between the percentage of the largest religion', 'smallest religion in 2007?'),
     S(6, '(iii) 27', '(iv) 13'), (fixed('Difference', 2, '(iii) 27 · 2 marks'),), '2-0', GRAPH),
    ('(iv)', 2, L(8, '(iv) Calculate the percentage of Hindu, labelled X, in 2007.'),
     S(6, '(iv) 13', '(v) · Any valid graph'), (fixed('Percentage', 2, '(iv) 13 · 2 marks'),), '2-0', GRAPH),
    ('(v)', 2, L(8, '(v) Name another type of graph or chart that could be used to present this data.'),
     S(6, '(v) · Any valid graph', 'Total marks 10'), (fixed('Graph or chart', 2, '(v) · Any valid graph · 2 marks'),),
     '2-0', GRAPH),
])
PART_ONE += [
    T('p1-11', P1, '11', '', 10, 9, L(9, 'Satellite Images'),
      (L(9, 'Study the satellite images and match the description', 'One has been completed for you.'),),
      (S(6, 'Hurricane · F', 'Total marks 10'),),
      rows(['Hurricane · F · 2 marks', 'A retreating glacier · A · 2 marks', 'An urban area · E · 2 marks',
            'A desert · C · 2 marks', 'An erupting volcano · B · 2 marks']),
      '2-8', AER, ID + 'p1-q11', ('page',),
      row_labels=(L(9, 'Hurricane'), L(9, 'A retreating glacier'), L(9, 'An urban area'), L(9, 'A desert'),
                  L(9, 'An erupting volcano'))),
]
PART_ONE += romans('12', P1, 10, L(10, 'River Landforms'), (), ID + 'p1-q12', ('page',), [
    ('(i)', 6, L(10, '(i) Examine the photographs above and match each of the named landforms', 'letters on the photographs.'),
     S(6, 'Waterfall · C', '(ii)'),
     rows(['Waterfall · C · 2 marks', 'Interlocking Spur · B · 2 marks', 'Meander · A · 2 marks']), '0-9', RIVERS,
     (L(10, 'Waterfall'), L(10, 'Interlocking Spur'), L(10, 'Meander'))),
    ('(ii)', 2, L(10, '(ii) State one reason why farming might be popular in the floodplain of a river valley.'),
     S(6, 'Reason stated', '(iii)', None, '12. River Landforms'), (fixed('Reason', 2, 'Reason stated · 2 marks'),),
     '0-6', RIVERS),
    ('(iii)', 2, L(10, '(iii) State one reason why farming might not be popular in the floodplain of a river valley.'),
     S(6, 'Reason stated', 'Total marks 10', (0, 0.815, 1, 1)), (fixed('Reason', 2, 'Reason stated · 2 marks'),),
     '0-6', RIVERS),
])


# ---------------------------------------------------------------- Part Two --
ITEM = sums(upto(3), (0, 2))
ITEM_LINES = ('Mark and identify 5 items', 'Showing = · 3 marks graded', 'Naming/identifying · 2 marks')


def sketch(q, page, title, prompt, scheme_page, topic, atlas, sources, labels):
    """A sketch: a 5-mark outline (limits 1, proportions 2 graded, impression 2 graded) and five
    items @ 5 (showing 3 graded, naming 2)."""
    return T(f'p2-{q.lower()}', P2, q, '', 30, page, title, (prompt,),
             (S(scheme_page, 'Draw a sketch Map', 'Total marks 30'),),
             (fixed('Limits/frame', 1, ('Draw a sketch Map', 'Limits/frame')),
              fixed('Proportions', 2, 'Proportions', upto(2)),
              fixed('Overall impression', 2, 'Overall impression', upto(2)),
              *(Criterion(f'Item {n}', 5, ITEM, 'exact', ITEM_LINES) for n in range(1, 6))),
             topic, atlas, ID + f'p2-q{q.lower()}', sources,
             row_labels=(None, None, None, *(L(page, b) for b in labels)))


def region_sketch(q, page, title, prompt, scheme_page, outline, items, topic, atlas):
    """A regional sketch map: a 6-mark outline and four items @ 6 (named 2, shown 4 graded)."""
    return T(f'p2-{q.lower()}', P2, q, '', 30, page, title, (prompt,),
             (S(scheme_page, outline, 'Total marks 30'),),
             (fixed('Outline', 6, outline, upto(6)),
              *(Criterion(label, 6, sums((0, 2), upto(4)), 'exact',
                          ((('Mark and identify 4 items @ 6 marks graded',) if n == 0 else ())
                           + (named, f'=Shown · 4 marks graded@{n}')))
                for n, (label, named) in enumerate(items))),
             topic, atlas, ID + f'p2-q{q.lower()}')


def stated_explained(head, head_label, head_marks, first, second, first_srps, second_srps, explain):
    """A named item and two stated-and-explained items (the 2010 '3 + 3 + 12 + 3 + 9' allocation)."""
    out = (fixed(head_label, head_marks, head),) if head else ()
    return out + (
        fixed(f'{first[1]} stated', 3, first[0]),
        srp3(f'{first[1]} explained', first_srps, (f'{explain}@0', f'{first_srps} SRPs @ · 3 marks each')),
        fixed(f'{second[1]} stated', 3, second[0]),
        srp3(f'{second[1]} explained', second_srps, (f'{explain}@1', f'{second_srps} SRPs @ · 3 marks each')),
    )


GRAPH_OL = (fixed('Overall impression on graph paper', 2, 'Over Impression on graph paper · 2 marks'),
            fixed('Vertical axis labelled / circle', 3, 'Vertical Axis labelled - Circle · 3 marks graded', upto(3)),
            fixed('Horizontal axis labelled / centred', 3, 'Horizontal Axis labelled - Centred · 3 marks graded',
                  upto(3)),
            fixed('4 items illustrated', 16, '4 Items @ · 4 marks each graded · 16 marks', upto(16)))
SURFACE = ('Sea / marine action', 'River action', 'Glacial action.')
ROCK = ('Oil and gas exploration', 'Mining', 'Quarrying', 'Geothermal energy production.')
CONTROL = ('River processes', 'Sea processes', 'Mass movement.')
WEATHERING = ('Freeze Thaw Action', 'Carbonation.')
FARMING = ('Relief and soils', 'Climate', 'EU Policies', 'Markets.')
SECTORS = ('Tourism', 'Agriculture.')
FUNDS = ('Common Agricultural Policy', 'Common Fisheries Policy', 'Regional Development Fund.')

Q1AS = (L(13, 'Study the diagrams below and answer the following questions in your answer book:'),)
PART_TWO = romans('1A', P2, 13, L(13, 'Plate Boundaries'), Q1AS, ID + 'p2-q1a', ('page',), [
    ('(i)', 15, L(13, '(i) Match each of the descriptions below with the correct plate boundary above:',
                  'Plates pulling apart.'),
     S(8, 'Convergent · 5 marks', '(ii) · At which', None, '(i) · Match each'),
     rows(['Convergent · 5 marks', 'Transform · 5 marks', 'Divergent · 5 marks'], 5), '0-0', PS,
     (L(13, 'Plates pushing together'), L(13, 'Plates sliding past each other'), L(13, 'Plates pulling apart'))),
    ('(ii)', 5, L(13, '(ii) At which of the above plate boundaries is the Mid-Ocean Ridge?'),
     S(8, 'Divergent · 5 marks', '(iii) · At which', None, '(ii) · At which'),
     (fixed('Plate boundary', 5, 'Divergent · 5 marks'),), '0-0', PS),
    ('(iii)', 5, L(13, '(iii) At which of the above plate boundaries would you find Fold Mountains?'),
     S(8, 'Convergent · 5 marks', '(iv) · Name an example', None, '(iii) · At which'),
     (fixed('Plate boundary', 5, 'Convergent · 5 marks'),), '0-0', PS),
    ('(iv)', 5, L(13, '(iv) Name an example of Fold Mountains.'),
     S(8, 'Any named example', 'Total marks 30'), (fixed('Fold mountains named', 5, 'Any named example · 5 marks'),),
     '0-2', RW + PS),
])
PART_TWO += [
    T('p2-1b', P2, '1B', '', 30, 13, L(13, 'Surface Processes'),
      (L(13, '(i) Describe and explain any one process of mass movement.'),),
      (S(8, 'Explain any one process @ 30 marks', 'Total marks 30'),),
      (fixed('Process named', 3, ('Explain any one process @ 30 marks', 'Process Named = · 3 marks')),
       srp3('Description and explanation', 9, '9 SRPs @ · 3 marks each · 27 marks')),
      '0-8', RW, ID + 'p2-q1b-route-i',
      routes=(
          Route('route-i', 'Route (i)', ID + 'p2-q1b-route-i', False),
          *(Route(f'route-ii-{slug(item, 34)}', f'Route (ii) · {item.rstrip(".")}',
                  ID + f'p2-q1b-route-ii-{slug(item, 34)}', False, keep_bullets=(item,),
                  prompt=(L(13, '(ii) Select any one of the following surface processes:', 'Glacial action.'),
                          L(13, 'Explain with the aid of a diagram(s) the formation of any one Irish landform',
                            'resulting from your selected process.')),
                  scheme=(S(9, 'Formation of any one Irish landforms @ 30 marks', 'Total marks 30'),),
                  criteria=(fixed('Landform named', 2, ('Formation of any one Irish landforms @ 30 marks',
                                                         'Landform Named = · 2 marks')),
                            fixed('Diagram(s)', 4, ('Diagram/diagrams', 'Two aspects @ · 2 marks each · 4 marks'),
                                  (0, 2, 4)),
                            srp3('Formation explained', 8, ('Formation of landform explained',
                                                            '8 SRPs @ · 3 marks each · 24 marks'))),
                  topic=topic, atlas=atlas)
            for item, topic, atlas in zip(SURFACE, ('0-10', '0-9', '0-11'), (SEA, RIVERS, GLAC))),
      )),
    T('p2-1c', P2, '1C', '', 40, 14, L(14, 'Human Interaction with the Rock Cycle'),
      (L(14, 'Humans interact with the rock cycle in many ways.', 'Geothermal energy production.'),
       L(14, 'With reference to an example you have studied explain', 'above in detail.')),
      (S(9, 'Explanation twelve SRPs', 'Total marks 40'),),
      (srp3('Explanation', 12, 'Explanation twelve SRPs @ 3 marks each · 36 marks'),
       fixed('Example', 4, 'Example · 4 marks')),
      '0-6', RW, ID + 'p2-q1c-oil-and-gas-exploration', routes=bullet_routes('p2-q1c-', ROCK)),
    sketch('2A', 15, L(15, 'Ordnance Survey Map'),
           L(15, 'Examine the 1:50,000 Ordnance Survey map accompanying this paper.',
             '(Please mark on your sketch map with an X).'),
           10, '2-6', MAP + RIVERS, ('map', 'legend'),
           ('The River Suir', 'A named hill', 'A ‘Waymarked Walk’ called the South Leinster Way',
            'An area of land over 200 metres north of the River Suir', 'A meander on the River Suir')),
]
Q2BS = (L(15, 'Study the map of an earthquake in Italy and answer the following questions', 'in your answer book:'),)
PART_TWO += romans('2B', P2, 15, L(15, 'Earthquakes'), Q2BS, ID + 'p2-q2b', ('page',), [
    ('(i)', 2, L(15, '(i) What was the magnitude (strength) of the earthquake at the epicentre?'),
     S(10, 'Magnitude · Mark', '(ii) · At what time'), (fixed('Magnitude', 2, ('Magnitude · Mark', '6.3 · 2')),),
     '0-7', EV),
    ('(ii)', 2, L(15, '(ii) At what time did the earthquake take place?'),
     S(10, 'Time · Mark', '(iii) · How many'), (fixed('Time', 2, ('Time · Mark', '1.32pm · 2')),), '0-7', EV),
    ('(iii)', 3, L(15, '(iii) How many towns reported deaths as a result of the earthquake?'),
     S(10, 'Number of towns · Mark', '(iv) · Explain in detail'),
     (fixed('Number of towns', 3, ('Number of towns · Mark', '5 · 3')),), '0-7', EV),
    ('(iv)', 33, L(15, '(iv) Explain in detail how earthquakes occur.'),
     S(10, '11 SRPs @ 3 marks each', 'Total marks 40'),
     (srp3('Explanation', 11, '11 SRPs @ 3 marks each · 33 marks graded'),), '0-7', EV + PS),
])
PART_TWO.append(T(
    'p2-2c', P2, '2C', '', 30, 15, L(15, 'Human Interaction'),
    (L(15, 'With reference to an example which you have studied, describe and explain how', 'Mass movement.'),),
    (S(11, 'How humans attempt to control surface processes @ 30', 'Total marks 30'),),
    (fixed('Control named', 3, ('How humans attempt to control surface processes @ 30', 'Control named = · 3 marks')),
     srp3('Way explained/described', 9, ('Way explained/described', '9 SRPs @ · 3 marks each · 27 marks'))),
    '0-6', RIVERS, ID + 'p2-q2c-river-processes',
    routes=bullet_routes('p2-q2c-', CONTROL, atlas=dict(zip(CONTROL, (RIVERS, SEA, RW))))))
Q3AS = (L(16, 'Study the images of mass movement and weathering below.'), L(16, 'In your answer book:'))
TERMS = (L(16, 'Scree'), L(16, 'Soil Creep'), L(16, 'Avalanche'))
PART_TWO += romans('3A', P2, 16, L(16, 'Mass Movement and Weathering'), Q3AS, ID + 'p2-q3a', ('page',), [
    ('(i)', 15, L(16, '(i) Match each of the images with the correct term below:', 'Avalanche.'),
     S(12, '• C · 5 marks', '(ii) · State whether'),
     rows(['• C · 5 marks', '• A · 5 marks', '• B · 5 marks'], 5), '0-8', RW, TERMS),
    ('(ii)', 15, L(16, '(ii) State whether each image is as a result of mass movement or weathering.'),
     S(12, '• Scree · Weathering', 'Total marks 30'),
     rows(['• Scree · Weathering · 5 marks', '• Soil Creep · Mass Movement · 5 marks',
           '• Avalanche · Mass Movement · 5 marks'], 5), '0-8', RW, TERMS),
])
PART_TWO += romans('3B', P2, 16, L(16, 'Rocks'), (), ID + 'p2-q3b', (), [
    ('(i)', 2, L(16, '(i) Name any one type of sedimentary rock.'),
     S(12, 'One type of rock named', '(ii) · Give a specific'),
     (fixed('Sedimentary rock named', 2, 'One type of rock named · 2 marks'),), '0-1', RW),
    ('(ii)', 2, L(16, '(ii) Give a specific location in Ireland where this sedimentary rock can be found.'),
     S(12, 'Specific location in Ireland', '(iii) · Describe how'),
     (fixed('Irish location', 2, 'Specific location in Ireland · 2 marks'),), '0-1', RW + IRL),
    ('(iii)', 36, L(16, '(iii) Describe how sedimentary rock is formed.'),
     S(12, '12 SRPs @ 3 marks each', 'Total marks 40'),
     (srp3('Description', 12, '12 SRPs @ 3 marks each · 36 marks graded'),), '0-1', RW),
])
PART_TWO.append(T(
    'p2-3c', P2, '3C', '', 30, 16, L(16, 'Weathering', nth=1),
    (L(16, 'Weathering is the process where rock and soil is broken up', 'Carbonation.'),
     L(16, 'Describe and explain any one of these weathering processes.')),
    (S(13, 'Explaining any one weathering process', 'Total marks 30'),),
    (srp3('Description and explanation', 10, ('Explaining any one weathering process',
                                              '10 SRPs @ · 3 marks each · 30 marks')),),
    '0-8', RW, ID + 'p2-q3c-freeze-thaw-action', routes=bullet_routes('p2-q3c-', WEATHERING)))

PART_TWO += [
    region_sketch('4A', 17, L(17, 'Map Skills'),
                  L(17, 'Draw a sketch map of a Continental / Sub-Continental region', 'One named mountain.'),
                  14, 'Sketch map of region', (('River', 'Named river · Named · 2 marks'),
                                               ('Town/City 1', '=Town/City named · Named · 2 marks@0'),
                                               ('Town/City 2', '=Town/City named · Named · 2 marks@1'),
                                               ('Mountain', 'Named mountain · Named · 2 marks')),
                  '1-6', CONT),
    T('p2-4b', P2, '4B', '', 40, 17, L(17, 'Agriculture in Ireland'),
      (L(17, 'Explain how any two of the following influence the development of agriculture', 'Markets.'),
       L(17, 'Clearly state the name of the region in your answer.', nth=0)),
      (S(14, 'Naming the Irish region', 'Total marks 40'),),
      (fixed('Irish region named', 4, 'Naming the Irish region · 4 marks'),
       srp3('Factor 1 explained', 6, ('Two factors @ · 36 marks', 'Factor 1 explained',
                                      '6 SRPs @ · 3 marks each · 18 marks@0')),
       srp3('Factor 2 explained', 6, ('Factor 2 Explained', '6 SRPs @ · 3 marks each · 18 marks@1'))),
      '1-4', IRL, ID + 'p2-q4b', absorbs=pool(ID + 'p2-q4b-', FARMING, 2)[1]),
    T('p2-4c', P2, '4C', '', 30, 17, L(17, 'Tourism'),
      (L(17, 'Explain two advantages of tourism for the economy', 'you have studied.'),
       L(17, 'Clearly state the name of the region in your answer.', nth=1)),
      (S(15, 'Naming the region', 'Total marks 30'),),
      stated_explained('Naming the region · 3 mark', 'Region named', 3, ('Advantage 1 stated', 'Advantage 1'),
                       ('Advantage 2 stated', 'Advantage 2'), 4, 3, 'Explaining the advantage for the economy'),
      '1-5', EURO, ID + 'p2-q4c'),
]
Q5AS = (L(18, 'Examine the pie-chart above showing the percentage of European Union spending', 'in your answer book:'),)
HEAD5A = S(16, 'Five correctly identified', 'Answer · Mark')
EACH5A = 'Five correctly identified @ 6 marks each as follows:'
PART_TWO += romans('5A', P2, 18, L(18, 'European Union Policy'), Q5AS, ID + 'p2-q5a', ('page',), [
    ('(i)', 6, L(18, '(i) What do the letters CAP represent?'),
     (HEAD5A, S(16, '(i) · Common Agricultural Policy', '(ii) · 3%')),
     (fixed('CAP', 6, (EACH5A, '(i) · Common Agricultural Policy · 6')),), '3-3', EU + EURO),
    ('(ii)', 6, L(18, '(ii) Calculate the percentage of EU spending on CAP in Ireland', 'pie-chart.'),
     (HEAD5A, S(16, '(ii) · 3%', '(iii) · Any valid')), (fixed('Percentage X', 6, (EACH5A, '(ii) · 3% · 6')),),
     '2-0', GRAPH),
    ('(iii)', 6, L(18, '(iii) Name one other EU member state not named in the pie-chart above.'),
     (HEAD5A, S(16, '(iii) · Any valid named country', '(iv) · Way 1')),
     (fixed('Member state', 6, (EACH5A, '(iii) · Any valid named country · 6')),), '3-3', EU + EURO),
    ('(iv)', 12, L(18, '(iv) List two ways Ireland benefited from the CAP.'),
     (HEAD5A, S(16, '(iv) · Way 1', 'Total marks 30')),
     (fixed('Way 1', 6, (EACH5A, '(iv) · Way 1 · 6')), fixed('Way 2', 6, '=Way 2 · 6')), '3-3', EU + EURO),
])
PART_TWO += [
    T('p2-5b', P2, '5B', '', 40, 18, L(18, 'European Region'),
      (L(18, 'Describe the development of manufacturing industry', 'which you have studied.'),
       L(18, 'Clearly state the name of the region in your answer.')),
      (S(16, 'Naming the European region', 'Total marks 40'),),
      (fixed('European region named', 4, 'Naming the European region (not in Ireland) · 4 marks'),
       srp3('Description', 12, ('Describing the development of manufacturing industry · 36 marks',
                                '12 SRPs @ · 3 marks each'))),
      '1-5', EURO, ID + 'p2-q5b'),
    T('p2-5c', P2, '5C', '', 30, 18, L(18, 'Urban Regions'),
      (L(18, 'Explain two reasons for the growth of one urban area', 'you have studied.'),
       L(18, 'Clearly state the name of the urban area in your answer.')),
      (S(17, 'Naming the urban area', 'Total marks 30'),),
      stated_explained('Naming the urban area · 3 mark', 'Urban area named', 3, ('Reason 1stated', 'Reason 1'),
                       ('Reason 2 stated', 'Reason 2'), 4, 3, 'Explaining the factor'),
      '1-1', IRL + EURO + CONT + URB, ID + 'p2-q5c'),
    region_sketch('6A', 19, L(19, 'Ireland - Regions'),
                  L(19, 'Draw a sketch map of Ireland.', 'One airport or port in the region.'),
                  18, 'Sketch map of Ireland', (('Region', 'Region · Named · 2 marks'),
                                                ('River', 'River · Named · 2 marks'),
                                                ('Mountain', 'Mountain · Named · 2 marks'),
                                                ('Airport/Port', 'Airport/Port · Named · 2 marks')),
                  '1-4', IRL),
    T('p2-6b', P2, '6B', '', 30, 19, L(19, 'Continental / Sub-Continental Regions'),
      (L(19, 'Name any one Continental / Sub-Continental region that you have studied.'),
       L(19, 'Describe the development of one of the following in that region:', 'Agriculture.')),
      (S(18, 'Naming the Continental/Sub Continental region', 'Total marks 30'),),
      (fixed('Region named', 3, 'Naming the Continental/Sub Continental region · 3 marks'),
       srp3('Description', 9, ('Describing the development of tourism/agriculture · 27 marks',
                               '9 SRPs @ · 3 marks each'))),
      '1-6', CONT, ID + 'p2-q6b-tourism', routes=bullet_routes('p2-q6b-', SECTORS)),
]
PART_TWO += romans('6C', P2, 19, L(19, 'European Expansion and Ireland'),
                   (L(19, 'In 2004 ten new countries joined the European Union.'),), ID + 'p2-q6c', (), [
    ('(i)', 20, L(19, '(i) Name and describe one positive effect this has had on Ireland.'),
     S(19, '(i)Positive effect', '(ii)Problem'),
     (fixed('Positive effect named', 2, '(i)Positive effect on Ireland named · 2 marks'),
      srp3('Effect explained', 6, ('Effect explained', '6 SRPs @ · 3 marks each · 18 marks'))), '1-5', EURO + EU),
    ('(ii)', 20, L(19, '(ii) Name and describe one problem which this has created for Ireland.'),
     S(19, '(ii)Problem', 'Total marks 40'),
     (fixed('Problem named', 2, '(ii)Problem for Ireland named · 2 marks'),
      srp3('Problem explained', 6, ('Problem explained', '6 SRPs @ · 3 marks each · 18 marks'))), '1-5', EURO + EU),
])

Q7AS = (L(21, 'The table above shows the percentage of unemployed people in Ireland', 'predicted percentage for 2010.'),)
PART_TWO += romans('7A', P2, 21, L(21, 'Statistics'), Q7AS, ID + 'p2-q7a', ('page',), [
    ('(i)', 24, L(21, '(i) Use graph paper to draw a graph to represent this data.'),
     S(20, 'Over Impression on graph paper', '(Sub Total 24)'), GRAPH_OL, '2-0', GRAPH),
    ('(ii)', 6, L(21, '(ii) In your answer book briefly explain why unemployment in Ireland is rising.'),
     S(20, 'Explaining why unemployment is rising', '(Sub Total 6)'),
     (srp3('Explanation', 2, ('Explaining why unemployment is rising', '2 SRPs @ · 3 marks each · 6 marks')),),
     '3-0', ECON),
])
PART_TWO.append(T(
    'p2-7b', P2, '7B', '', 30, 21, L(21, 'Developing Economies'),
    (L(21, '‘Colonialism has hindered the economic development of some countries.’'),
     L(21, 'With reference to a developing country or region', 'limited that area’s development.')),
    (S(21, 'Naming the developing country/region', 'Total marks 30'),),
    stated_explained('Naming the developing country/region · 3 mark', 'Country/region named', 3,
                     ('Way 1 stated', 'Way 1'), ('Way 2 stated', 'Way 2'), 4, 3, 'Explaining the way'),
    '3-1', DEV, ID + 'p2-q7b'))
Q7CI = L(21, '(i) Give the name and location of one multinational company you have studied.')
PART_TWO += romans('7C', P2, 21, L(21, 'Multinational Companies'), (), ID + 'p2-q7c', (), [
    ('(i)', 8, Q7CI, S(21, 'Named · 4 marks', '(ii) · Name one product'),
     (fixed('Company named', 4, 'Named · 4 marks'), fixed('Location', 4, 'Location · 4 marks')), '3-2', MNC),
    ('(ii)', 5, L(21, '(ii) Name one product manufactured by your named multinational company.'),
     S(21, 'Product named', '(iii) · Describe and explain'), (fixed('Product named', 5, 'Product named · 5 marks'),),
     '3-2', MNC, (), (Q7CI,)),
    ('(iii)', 27, L(21, '(iii) Describe and explain two reasons why your named multinational company',
                    'located where it did.'),
     S(21, 'Reason 1 stated', 'Total marks 40'),
     stated_explained(None, None, 0, ('Reason 1 stated', 'Reason 1'), ('Reason 2 stated', 'Reason 2'), 4, 3,
                      '=Explained'),
     '3-2', MNC, (), (Q7CI,)),
])
PART_TWO += [
    sketch('8A', 22, L(22, 'Ordnance Survey Map'),
           L(22, 'Examine the 1:50,000 Ordnance Survey map and legend accompanying this paper.',
             'A mast in the north of the map.'),
           22, '2-6', MAP + ECON, ('map', 'legend'),
           ('The built up area of Carrick-on-Suir', 'The railway line', 'The N24 National Primary Road',
            'An electricity transmission line', 'A mast in the north of the map.')),
]
PART_TWO += romans('8B', P2, 22, L(22, 'Acid Rain'), (), ID + 'p2-q8b', (), [
    ('(i)', 6, L(22, '(i) Explain how acid rain occurs.'),
     S(22, 'Explaining how acid rain occurs', '(Sub Total 6)'),
     (srp3('Explanation', 2, ('Explaining how acid rain occurs', '2 SRPs @ 3 marks each · 6 marks')),), '3-4', ENV),
    ('(ii)', 22, L(22, '(ii) Name and describe two effects of acid rain.'),
     S(22, 'Two effects', '(Sub Total 22)'),
     (fixed('Effect 1 named', 2, ('Two effects', 'Effect 1', '=Named · 2 marks')),
      srp3('Effect 1 explained', 3, '=Explained 3 SRPs @ 3 marks each · 9 marks@0'),
      fixed('Effect 2 named', 2, ('Effect 2', 'Named · 2marks')),
      srp3('Effect 2 explained', 3, '=Explained 3 SRPs @ 3 marks each · 9 marks@1')), '3-4', ENV),
    ('(iii)', 12, L(22, '(iii) Suggest two actions that could be taken to reduce these effects.'),
     S(22, 'Two actions', '(Sub Total 12)'),
     (srp3('Action 1', 2, ('Two actions', 'Action 1', '2 SRPs @ 3 marks each · 6 marks@0')),
      srp3('Action 2', 2, ('Action 2', '2 SRPs @ 3 marks each · 6 marks@1'))), '3-4', ENV),
])
PART_TWO.append(T(
    'p2-8c', P2, '8C', '', 30, 22, L(22, 'Economic Activities and Conflict'),
    (L(22, '‘The development of economic activities', 'local interests.’'),
     L(22, 'Discuss this statement with reference to one example that you have studied.')),
    (S(23, 'Example named', 'Total marks 30'),),
    (fixed('Example named', 3, 'Example named · 3 marks'),
     srp3('Discussion', 9, ('Statement discussed · 27 marks', '9 SRPs @ · 3 marks each'))),
    '3-4', ENV, ID + 'p2-q8c', ('page',)))
Q9AS = (L(23, 'Study the map above and answer the following questions:'),)
PART_TWO += romans('9A', P2, 23, L(23, 'Economic Development'), Q9AS, ID + 'p2-q9a', ('page',), [
    ('(i)', 6, L(23, '(i) What do the letters HDI represent?'),
     S(24, 'Human Development Index · 6 marks', '(ii) · Name the three'),
     (fixed('HDI', 6, 'Human Development Index · 6 marks'),), '3-0', ECON + DEV),
    ('(ii)', 6, L(23, '(ii) Name the three variables used to calculate the HDI.'),
     S(24, 'Three variables @ 2 marks each', '(iii) · In which category'),
     (fixed('Three variables', 6, 'Three variables @ 2 marks each · 6 marks', (0, 2, 4, 6)),), '3-0', ECON + DEV),
    ('(iii)', 6, L(23, '(iii) In which category of HDI is Ireland?'),
     S(24, '0,90-0,96', '(iv) · Explain briefly'), (fixed('Category', 6, '0,90-0,96 · 6 marks'),), '3-0', ECON + DEV),
    ('(iv)', 6, L(23, '(iv) Explain briefly why the HDI for Africa is low.'),
     S(24, 'Explanation', '(v) · GDP'),
     (srp3('Explanation', 2, ('Explanation', '2 SRPs @ 3 marks each · 6 marks')),), '3-1', DEV),
    ('(v)', 6, L(23, '(v) GDP is another measure of economic development.', 'What do the letters GDP represent?'),
     S(24, 'Gross Domestic Product', 'Total marks 30'), (fixed('GDP', 6, 'Gross Domestic Product · 6 marks'),),
     '3-0', ECON),
])
Q9BS = (L(23, 'Examine the aerial photograph accompanying this paper.', 'near the town of Carrick-on-Suir.'),)
PART_TWO += romans('9B', P2, 23, L(23, 'Aerial Photograph'), Q9BS, ID + 'p2-q9b', ('aerial',), [
    ('(i)', 6, L(23, '(i) State clearly where you would locate the factory', 'background etc.).'),
     S(24, 'Correct location', '(ii) Explain one reason'), (fixed('Location', 6, 'Correct location · 6 marks'),),
     '2-8', AER + ECON),
    ('(ii)', 12, L(23, '(ii) Explain one reason in favour of this location.'),
     S(24, 'Stating reason in favour', '(iii) Explain one reason'),
     (fixed('Reason stated', 3, 'Stating reason in favour · 3 marks'),
      srp3('Reason explained', 3, ('Explaining the reason', '3 SRPs @ · 3 marks each · 9 marks'))),
     '3-2', MNC + AER),
    ('(iii)', 12, L(23, '(iii) Explain one reason why local people might object to the building of the factory.'),
     S(24, 'Stating reason to object', 'Total marks 30'),
     (fixed('Reason stated', 3, 'Stating reason to object · 3 marks'),
      srp3('Reason explained', 3, ('Explaining the reason', '3 SRPs @ · 3 marks each · 9 marks'))),
     '3-4', ENV + AER),
])
PART_TWO.append(T(
    'p2-9c', P2, '9C', '', 40, 24, L(24, 'Ireland and the European Union'),
    (L(24, 'The Irish economy receives funding from the European Union', 'Regional Development Fund.'),
     L(24, 'Choose any one of the above and explain in detail', 'economy.')),
    (S(25, 'Naming the policy', 'Total marks 40'),),
    (fixed('Policy named', 1, 'Naming the policy · 1 mark'),
     fixed('Way 1 stated', 3, 'Way1 stated · 3 marks'),
     srp3('Way 1 explained', 6, ('=Explained@0', '6 SRPs @ · 3 marks each · 18 marks')),
     fixed('Way 2 stated', 3, 'Way 2 stated · 3 marks'),
     srp3('Way 2 explained', 5, ('=Explained@1', '5 SRPs @ · 3 marks each · 15 marks'))),
    '3-3', EU, ID + 'p2-q9c-common-agricultural-policy', routes=bullet_routes('p2-q9c-', FUNDS)))

Q10AS = (L(25, 'Examine the population pyramid above for Cork City', 'questions:'),)
PART_TWO += romans('10A', P2, 25, L(25, 'Population Structure'), Q10AS, ID + 'p2-q10a', ('page',), [
    ('(i)', 6, L(25, '(i) What percentage of females is in the 10 - 14 year age group?'),
     S(26, '2.59 · 6 marks', '(ii) · Which age group'), (fixed('Percentage', 6, '2.59 · 6 marks'),), '2-0', GRAPH),
    ('(ii)', 6, L(25, '(ii) Which age group is the largest?'),
     S(26, '20-24 · 6 marks', '(iii) · Which is greater'), (fixed('Age group', 6, '20-24 · 6 marks'),), '2-0', GRAPH),
    ('(iii)', 6, L(25, '(iii) Which is greater the percentage of males or females in the 80 - 84 age group?'),
     S(26, 'Females · 6 marks', '(iv) · Calculate'), (fixed('Males or females', 6, 'Females · 6 marks'),),
     '2-0', GRAPH),
    ('(iv)', 6, L(25, '(iv) Calculate the percentage of children', 'age group.'),
     S(26, '4.74 · 6 marks', '(v) · Explain one way'), (fixed('Percentage', 6, '4.74 · 6 marks'),), '2-0', GRAPH),
    ('(v)', 6, L(25, '(v) Explain one way this population pyramid differs', 'developing world.'),
     S(26, 'Way explained · 6 marks', 'Total marks 30'),
     (Criterion('Way explained', 6, (0, 3, 6), 'srp', ('Way explained · 6 marks', 'Two SRPs @ 3 marks each')),),
     '4-0', POP),
])
PART_TWO += romans('10B', P2, 25, L(25, 'Migration'), (), ID + 'p2-q10b', (), [
    ('(i)', 15, L(25, '(i) Describe and explain one positive effect of people migrating.'),
     S(27, 'Positive effect stated', '(ii) · Describe and explain one negative'),
     (fixed('Positive effect stated', 3, 'Positive effect stated · 3 marks'),
      srp3('Description and explanation', 4, ('Described and explained', '4 SRPs @ · 3 marks each · 12 marks'))),
     '4-2', POP),
    ('(ii)', 15, L(25, '(ii) Describe and explain one negative effect of people migrating.'),
     S(27, 'Negative effect stated', 'Total marks 30'),
     (fixed('Negative effect stated', 3, 'Negative effect stated · 3 marks'),
      srp3('Description and explanation', 4, ('Described and explained', '4 SRPs @ · 3 marks each · 12 marks'))),
     '4-2', POP),
])
PART_TWO += romans('10C', P2, 25, L(25, 'Settlement Patterns'), (), ID + 'p2-q10c', ('map', 'legend'), [
    ('(i)', 16, L(25, '(i) Name and give the location by grid reference', 'accompanying this paper.'),
     S(27, 'Two patterns named', '(Sub Total 16 marks)'),
     (fixed('Two patterns named', 6, 'Two patterns named @ 3 marks each · 6 marks', (0, 3, 6)),
      fixed('Two patterns located', 10, 'Two patterns located @ 5 marks each · 10marks graded', upto(10))),
     '4-3', URB + MAP),
    ('(ii)', 24, L(25, '(ii) Explain the development of these patterns in detail.'),
     S(27, 'Two patterns explained', '(Sub Total 24 marks)'),
     (srp3('Pattern 1 explained', 4, ('Two patterns explained', 'Pattern 1',
                                      '=Four SRPs @ 3 marks each · 12 marks@0')),
      srp3('Pattern 2 explained', 4, ('Pattern 2', '=Four SRPs @ 3 marks each · 12 marks@1'))),
     '4-3', URB + MAP),
])
PART_TWO += romans('11A', P2, 26, L(26, 'Population Dynamics'), (L(26, 'Infant Mortality Rates, 2009'),),
                   ID + 'p2-q11a', ('page',), [
    ('(i)', 24, L(26, '(i) Use graph paper to draw a graph to represent this data.'),
     S(28, 'Over Impression on graph paper', '(Sub Total 24)'), GRAPH_OL, '2-0', GRAPH),
    ('(ii)', 6, L(26, '(ii) In your answer book explain why infant mortality rate is higher', 'such as Kenya?'),
     S(28, 'Explaining why infant mortality rates', '(Sub Total 6)'),
     (srp3('Explanation', 2, ('Explaining why infant mortality rates are higher in the developing world',
                              '2 SRPs @ · 3 marks each · 6 marks')),), '4-0', POP),
])
PART_TWO.append(T(
    'p2-11b', P2, '11B', '', 40, 26, L(26, 'Development of Towns'),
    (L(26, 'Examine the aerial photograph and the 1:50,000 Ordnance Survey map and legend', 'accompanying this paper.'),
     L(26, 'Using the map and the photograph explain three reasons', 'developed at its present location.')),
    (S(28, 'Reason 1', 'Total marks 40'),),
    (srp3('Reason 1 explained', 4, ('Reason 1', 'Explaining the reason@0', '4 SRPs @ · 3 marks each · 12 marks')),
     srp3('Reason 2 explained', 3, ('Reason 2', 'Explaining the reason@1', '=3 SRPs @ · 3 marks each · 9 mark')),
     srp3('Reason 3 explained', 3, ('Reason 3', 'Explaining the reason@2', '=3 SRPs @ · 3 marks each · 9 marks')),
     fixed('First evidence', 4, ('Three pieces of map or photo evidence', 'First evidence 4')),
     fixed('Second evidence', 3, 'Second evidence 3'),
     fixed('Third evidence', 3, 'Third evidence 3')),
    '4-3', URB + MAP + AER, ID + 'p2-q11b', ('map', 'legend', 'aerial')))
Q11CI = L(26, '(i) Name one city in the developing world which has grown rapidly in recent years.')
PART_TWO += romans('11C', P2, 26, L(26, 'Growth of Cities in the Developing World'), (), ID + 'p2-q11c', (), [
    ('(i)', 3, Q11CI, S(29, 'Any valid named city', '(ii) · State one reason'),
     (fixed('City named', 3, 'Any valid named city · 3 marks'),), '4-5', URB),
    ('(ii)', 3, L(26, '(ii) State one reason why this city has grown rapidly.'),
     S(29, 'Reason stated · 3 marks', '(iii) · Describe one problem'), (fixed('Reason', 3, 'Reason stated · 3 marks'),),
     '4-5', URB, (), (Q11CI,)),
    ('(iii)', 12, L(26, '(iii) Describe one problem caused by this rapid growth.'),
     S(29, 'Problem stated', '(iv) · Explain one solution'),
     (fixed('Problem stated', 3, 'Problem stated · 3 marks'),
      srp3('Description', 3, ('Described', 'Three SRPs @ 3 marks each · 9 marks'))), '4-5', URB, (), (Q11CI,)),
    ('(iv)', 12, L(26, '(iv) Explain one solution to this problem.'),
     S(29, 'Solution stated', 'Total marks 30'),
     (fixed('Solution stated', 3, 'Solution stated · 3 marks'),
      srp3('Explanation', 3, 'Three SRPs @ 3 marks each · 9 marks')), '4-5', URB, (), (Q11CI,)),
])
PART_TWO.append(sketch(
    '12A', 27, L(27, 'Land Use in Cities'),
    L(27, 'Examine the aerial photograph accompanying this paper.', 'A bridge.'),
    30, '2-8', AER + URB, ('aerial',),
    ('A church', 'A recreational (leisure) area', 'The main street (Central Business District)',
     'A modern residential (housing) area', 'A bridge.')))
Q12BS = (L(27, '‘Some parts of the world are over-populated.', 'standard of living.’'),)
Q12BI = L(27, '(i) Name any one region of the world that is over-populated.')
PART_TWO += romans('12B', P2, 27, L(27, 'Over-population', nth=0), Q12BS, ID + 'p2-q12b', (), [
    ('(i)', 4, Q12BI, S(30, 'Region named · 4 marks', '(ii) · Explain in detail'),
     (fixed('Region named', 4, 'Region named · 4 marks'),), '4-1', POP),
    ('(ii)', 15, L(27, '(ii) Explain in detail one cause of the over-population in the region you have named.'),
     S(30, 'Cause stated', '(iii) · Describe in detail'),
     (fixed('Cause stated', 3, 'Cause stated · 3 marks'),
      srp3('Explanation', 4, ('Explained', 'Four SRPs @ 3 marks each · 12 marks'))), '4-1', POP, (), (Q12BI,)),
    ('(iii)', 15, L(27, '(iii) Describe in detail one problem caused by over-population.'),
     S(30, 'Problem stated', '(iv) · Suggest one solution'),
     (fixed('Problem stated', 3, 'Problem stated · 3 marks'),
      srp3('Description', 4, ('Described', 'Four SRPs @ 3 marks each · 12 marks'))), '4-1', POP),
    ('(iv)', 6, L(27, '(iv) Suggest one solution to the problem of over-population.'),
     S(30, 'Solution suggested', 'Total marks 40'),
     (Criterion('Solution suggested', 6, (0, 3, 6), 'srp', ('Solution suggested · 6 marks',
                                                           'Two SRPs @ 3 marks each')),), '4-1', POP),
])
PART_TWO.append(T(
    'p2-12c', P2, '12C', '', 30, 27, L(27, 'Changing Urban Functions'),
    (L(27, 'Explain two functions of an urban area studied by you.'),
     L(27, 'Clearly state the name of the urban area in your answer.')),
    (S(31, 'Naming the urban area', 'Total marks 30'),),
    stated_explained('Naming the urban area · 3 mark', 'Urban area named', 3, ('Function 1stated', 'Function 1'),
                     ('Function 2 stated', 'Function 2'), 4, 3, 'Explaining the function'),
    '4-3', URB, ID + 'p2-q12c'))

TASKS = [*PART_ONE, *PART_TWO]

ID_CORRECTION_REASON = 'No 2010 Ordinary card shipped before this review; every card is new.'

# No 2010 Ordinary card was live on origin/main before this review.
LEGACY_IDS: list[str] = []
