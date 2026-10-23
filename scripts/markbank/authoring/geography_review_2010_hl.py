"""Independent review ledger: Leaving Certificate Geography 2010 Higher Level.

Sources (English editions, harvested Paper Trail corpus; sizes and SHA-256
pinned in EXPECTED_SOURCES and the generated audit): the examination paper
LC005ALP000EV (32 pages; one booklet printed Part One, answered in it, and
Part Two), marking scheme LC005ALP000EV (41 pages), and the common
Carrick-on-Suir companions, which Paper Trail holds only as JPEG images. In
2010 the SEC file names are swapped relative to later years (checked by eye):
LC005CLP004EV.jpg is the 1:50 000 map extract, LC005CLP003EV.jpg the oblique
aerial photograph, and LC005CLP000EV.jpg the OS legend sheet. Part One is 80
marks (any ten of twelve @ 8), Part Two 320 (four questions @ 80).

Visual sweep (every page rendered and read on 2026-10-23):
  Paper p1 cover and examiner's grid; p2-p11 Part One Questions 1-12 (p4
  holds Q3 and Q4, p7 Q7 and Q8; Q1 prints four landscape photographs, Q3
  four maps of Irish regions, Q5 an OS map extract of Coomasaharn Lake, Q6
  an Atlantic weather chart, Q8 a sketch map of the aerial photograph, Q9
  two rock photographs and a diagram, Q10 satellite images, Q11 a table, Q12
  a population pyramid); p12 Part Two instructions; p13 Section 1 divider;
  p14-p19 Q1-Q6 (p14 and p17 open with their dividers); p20 Section 2
  divider; p21-p26 Electives Q7-Q12 (p21 and p24 open with their elective
  dividers; p25 prints the 1830's map of Kilrush and a recent aerial
  photograph beside it); p27 Section 3 divider and option note; p28-p29
  Options Q13-Q24; p30-p32 printed "Blank Page".
  Scheme p1 cover; p2 blank; p3 Part One table (a centred tariff heading,
  then two columns: Q1-Q6, Q7-Q12; the answer lines print no marks); p4
  Part Two instructions; p5 Section 1 divider; p6-p18 Q1-Q6 (p6 and p13
  open with their dividers); p19 Section 2 divider; p20-p31 Q7-Q12 (p20 and
  p26 open with their dividers); p32 Section 3 divider and option note;
  p33-p36 Q13-Q24; p37 Geographical Investigation (coursework); p38 its
  presentation marks; p39 investigation topics; p40 Irish-language bonus
  marks; p41 back cover. The scheme reprints each Part Two question above
  its allocation; every slice starts at the allocation.
  Companions: Carrick-on-Suir map extract (the River Suir, the Glen River,
  the Lingaun River, the N24, the R697, the South Leinster Way, the railway
  and station); OS Discovery Series legend sheet; oblique aerial photograph
  of Carrick-on-Suir (the River Suir and its two bridges in the left
  background, the castle, sports fields and housing).

Part One prices every question in one heading, printed as two lines under
"Each question:": "4 parts @ 2 marks each" and "8 parts @ 1 mark each".
Every Part One card carries the heading line that prices it with its answer
lines: Q2 (eight answers across six romans: (iv) two antiquities and (vi)
two rivers) and Q7 (eight letters; the ninth, B = 1, is printed as the
worked example and is not carded) are priced at one mark per answer, the
rest at two marks a part. Matching tables, in the printed row order: Q1
Freeze-thaw B, Abrasion D, Human activity C, Carbonation A; Q3 Urban region
D, Cultural region A, Core region B, Political region C; Q7 A = 8, C = 9,
D = 2, E = 7, F = 3, G = 4, H = 6, I = 5; Q8 Old Bridge Left Background,
House Left Foreground, Wooded Island Right Foreground, Sports Field Centre
Background / Centre Middleground / Centre Centre; Q10 Sandstorm C, Icebergs
A, Island Arc D, Alpine Glacier B.

Q9(ii) prints its two answers as "(ii) 1" and, on the next line, a lone "2"
(Rock B forms at 2). The reader treats a bare one- or two-digit line as page
furniture, so its slice keeps bare numerals (SchemeSlice.keep_digits) and
ends at "Q10", above the page number.

Part Two A parts are priced by a heading over unpriced answer lines ("Five
answers @ 4 marks each" for 2A and 5A, "Four answers @ 5 marks each" for 3A,
7A and 12A, with "3 marks + 2 marks" printed on the explanation lines); each
roman card carries that heading. 5A(iii) accepts "59.7 / 12.6 / 2.0 / 7.2"
(the question's wording admits several readings): that line is its
guidance. 8A and 10A price the graph at 16 (title 2, scaled axis 2, six items
@ 2 graded) and (ii) at 4. 11B prints (i) and (ii) in one [30m] allocation
and is one card.

The options print no Overall Coherence table: coherence is graded inside
each aspect ("Number of aspects: 3 (27 + 27 + 26) / (4 @ 20 marks each)",
"Identifying aspect: 4 marks / 4 marks", "Discussion" or "Examination: 8 x
SRPs OR 6 x SRPs", "Overall coherence: 7/6 marks graded / 4 marks graded").
Either way the discussion is 24 SRPs (3 x 8 or 4 x 6), 48 marks, and
identifying plus coherence is 32 (3 x 4 + 7 + 7 + 6, or 4 x 4 + 4 x 4), so
each option card prices those two criteria, as the 2012 Higher ledger does.

Printed choices: 1B (i) or (ii), with (i)'s "landform of erosion or
deposition" a route each; 3B (one of three printed processes) and 6B (any
one of three printed factors) are one route per printed option; option 20
"either language or religion" is two routes. 8B's "one or more of the
following headings" lets the candidate combine headings and stays one card
with every heading printed.
"""

from geography_review import (
    Criterion, Lift, Route, SchemeSlice, Task, evens, fixed, srp, sums, upto,
)

YEAR = 2010
LEVEL = 'higher'
PAPER_PAGES = {1: 32, 2: 32}
SCHEME_PAGES = 41
QUESTION_TARIFFS = {1: {str(n): 8 for n in range(1, 13)},
                    2: {**{f'{n}{x}': (20 if x == 'A' else 30)
                           for n in range(1, 13) for x in 'ABC'},
                        **{str(n): 80 for n in range(13, 25)}}}

# 2010's companions are JPEGs whose SEC names are swapped against later
# years: CLP004 is the map extract and CLP003 the aerial photograph.
EXPECTED_SOURCES = {
    'paper1': ('LC005ALP000EV.pdf', 3619088),
    'paper2': ('LC005ALP000EV.pdf', 3619088),
    'scheme': ('LC005ALP000EV.pdf', 855544),
    'map': ('LC005CLP004EV.jpg', 2806497),
    'legend': ('LC005CLP000EV.jpg', 1636000),
    'aerial': ('LC005CLP003EV.jpg', 4062934),
}

_PAPER = {1: 'cover and examiner grid', **{p: 'question' for p in range(2, 12)},
          12: 'Part Two instructions', 13: 'section divider', **{p: 'question' for p in range(14, 20)},
          20: 'section divider', **{p: 'question' for p in range(21, 27)}, 27: 'section divider and option note',
          28: 'question', 29: 'question', 30: 'blank page', 31: 'blank page', 32: 'blank page'}
PAGE_REVIEW = {
    # One booklet printed both parts.
    'paper1': _PAPER, 'paper2': _PAPER,
    'scheme': {1: 'cover', 2: 'blank', 3: 'Part One table', 4: 'Part Two instructions',
               5: 'section divider', **{p: 'Part Two allocation' for p in range(6, 19)}, 19: 'section divider',
               **{p: 'Part Two allocation' for p in range(20, 32)}, 32: 'section divider and option note',
               **{p: 'option allocation' for p in range(33, 37)},
               37: 'geographical investigation (coursework)',
               38: 'geographical investigation presentation marks', 39: 'investigation topics',
               40: 'Irish-language bonus marks', 41: 'back cover'},
}

EXPECTED_SELECTION_SCAN = [
    [1, 2, 'attempt ten'], [1, 12, 'attempt four'], [1, 13, 'attempt two'], [1, 14, 'attempt one'],
    [1, 14, 'answer (i) or (ii)'], [1, 14, 'any one'], [1, 15, 'any one'], [1, 16, 'attempt to'],
    [1, 16, 'one of the following'], [1, 16, 'any one'], [1, 17, 'attempt one'], [1, 18, 'any two'],
    [1, 19, 'any two'], [1, 19, 'any two'], [1, 19, 'any one'], [1, 19, 'any two'],
    [1, 20, 'attempt one'], [1, 20, 'either'], [1, 22, 'any one'], [1, 23, 'any one'],
    [1, 27, 'attempt one'], [1, 28, 'any one'], [1, 29, 'either'],
]
SELECTION_REVIEW = [
    {'scan': [[1, 2, 'attempt ten'], [1, 12, 'attempt four'], [1, 13, 'attempt two'], [1, 14, 'attempt one'],
              [1, 17, 'attempt one'], [1, 20, 'attempt one'], [1, 20, 'either'], [1, 27, 'attempt one']],
     'kind': 'exam-attempt-rule',
     'reason': 'Part One any ten of twelve and Part Two four questions (one of Q1-3, one of Q4-6, one elective from EITHER Economic Activities OR the Human Environment, one option) are attempt rules; every question is carded.'},
    {'scan': [[1, 14, 'answer (i) or (ii)'], [1, 14, 'any one']], 'kind': 'closed-route',
     'reason': '1B: (i) or (ii); (i) "any one Irish landform of erosion or deposition" is a route each -> 3 routes.'},
    {'scan': [[1, 29, 'either']], 'kind': 'closed-route',
     'reason': 'Option 20: either language or religion -> 2 routes under one allocation.'},
    {'scan': [[1, 16, 'one of the following'], [1, 19, 'any one']], 'kind': 'closed-choose-one',
     'reason': '3B one of three printed processes (fluvial, marine, mass movement) and 6B any one of three printed factors (economic, human, physical) -> 3 routes each.'},
    {'scan': [[1, 15, 'any one'], [1, 16, 'any one'], [1, 18, 'any two'], [1, 19, 'any two'], [1, 19, 'any two'],
              [1, 19, 'any two'], [1, 22, 'any one'], [1, 23, 'any one'], [1, 28, 'any one']],
     'kind': 'open-response',
     'reason': 'No printed pool: 2C any one human interaction, 3C any one underground landform, 5C and 6C any two factors, 6A(i) any two physical features and 6A(ii) any two urban centres, 8B any one developed economy (its "one or more of the following headings" lets the candidate combine headings, so the card keeps every heading), 9B any one major EU policy, option 18 any one soil type. Compulsory lists stay whole: 1A, 9A, 11A each item; 4A each roman; 7B and 10C three items each.'},
    {'scan': [[1, 16, 'attempt to']], 'kind': 'not-a-selection',
     'reason': '3B "humans attempt to influence or control natural processes" describes human activity, not a candidate choice.'},
]

# Nothing is held: 2010 HL Part One Q9(ii)'s second answer is a lone printed "2",
# lifted with a slice that keeps bare numerals (SchemeSlice.keep_digits).
HELD: list[dict] = []

P1, P2 = 1, 2
LEFT = (0.0, 0.305, 0.52, 1.0)
RIGHT = (0.52, 0.305, 1.0, 1.0)
ID = 'geography-2010-hl-'
H = 'geography-higher-'
SRPS = 'SRPs'
EACH2 = '4 parts @ 2 marks each'
EACH1 = '8 parts @ 1 mark each'


def L(page, start, end=None, nth=None):
    return Lift(page, start, end, None, nth)


def S(page, start, end=None, clip=None, after=None, table=False):
    return SchemeSlice(page, start, end, clip, after, table)


# The Part One heading lines that price each question.
HEAD2 = S(3, EACH2, EACH1)
HEAD1 = S(3, EACH1, 'No grading')


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


def choose_one(prefix, options):
    """One route per printed option: (printed item, id slug, topic, atlas)."""
    return tuple(Route(route_slug, item.rstrip('.'), ID + prefix + route_slug, False,
                       keep_bullets=(item,), topic=topic, atlas=atlas)
                 for item, route_slug, topic, atlas in options)


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
PART_ONE = [
    T('p1-1', P1, '1', '', 8, 2, L(2, 'Surface Processes'),
      (L(2, 'Insert the correct letter in the spaces below to identify the process at work in each of',
         'photographs above.'),),
      (HEAD2, S(3, 'Q1', 'Q2', LEFT)),
      priced_rows(EACH2, ['Q1 · B', '=D', '=C', '=A'], 2),
      '0-4', RW + SEA + KARST, ID + 'p1-q1', ('page',),
      row_labels=(L(2, 'Freeze-thaw'), L(2, 'Abrasion'), L(2, 'Human activity'), L(2, 'Carbonation'))),
]
PART_ONE += romans('2', P1, 3, L(3, 'Ordnance Survey Map'),
                   (L(3, 'Examine the 1:50,000 Ordnance Survey map and legend that accompanies this paper.',
                      'in the spaces below:'),),
                   ID + 'p1-q2', ('map', 'legend'), [
    ('(i)', 1, L(3, '(i) Give the correct name for one type of boundary shown on the map.'),
     (HEAD1, S(3, 'Q2', '(ii) South', LEFT)),
     answer('Type of boundary', EACH1, ('Q2 · (i) County Boundary / Coniferous', 'Plantation / Natural Woodland /',
                                        'Mixed Woodland / Forest Park'), 1), '2-6', MAP),
    ('(ii)', 1, L(3, '(ii) Give the correct name for a ‘Waymarked Walk’ shown on the map.'),
     (HEAD1, S(3, '(ii) South', '(iii) S 401', LEFT)),
     answer('Waymarked Walk', EACH1, '(ii) South Leinster Way', 1), '2-6', MAP),
    ('(iii)', 1, L(3, '(iii) Give a six-figure grid reference for a ‘Mast’ shown on the map.'),
     (HEAD1, S(3, '(iii) S 401', '(iv) Megalithic', LEFT)),
     answer('Grid reference', EACH1, '(iii) S 401(2) 289/290(1)(2)', 1), '2-6', MAP),
    ('(iv)', 2, (L(3, '(iv) What Antiquities are found at the following grid references?'),
                 L(3, 'S 430 284'), L(3, 'S 419 197')),
     (HEAD1, S(3, '(iv) Megalithic', '(v) S 406', LEFT)),
     answer('Two antiquities', EACH1, '(iv) Megalithic Tomb & Ogham Stone', 2, (0, 1, 2)), '2-6', MAP),
    ('(v)', 1, L(3, '(v) Give a six-figure grid reference for the railway station in Carrick-on-Suir.'),
     (HEAD1, S(3, '(v) S 406', '(vi) River Suir', LEFT)),
     answer('Grid reference', EACH1, '(v) S 406(7) 220', 1), '2-6', MAP),
    ('(vi)', 2, L(3, '(vi) The point S 396 218 is the confluence point of which two rivers?'),
     (HEAD1, S(3, '(vi) River Suir', 'Q3', LEFT)),
     answer('Two rivers', EACH1, '(vi) River Suir & Glen River', 2, (0, 1, 2)), '2-6', MAP + RIVERS),
])
PART_ONE.append(T(
    'p1-3', P1, '3', '', 8, 4, L(4, 'Types of Region'),
    (L(4, 'Match each map to a type of region it represents by writing the correct letter in the table',
       'below.'),),
    (HEAD2, S(3, 'Q3', 'Q4', LEFT)),
    priced_rows(EACH2, ['Q3 · D', '=A', '=B', '=C'], 2),
    '1-0', IRL, ID + 'p1-q3', ('page',),
    row_labels=(L(4, 'Urban region'), L(4, 'Cultural region'), L(4, 'Core region'), L(4, 'Political region'))))
PART_ONE += romans('4', P1, 4, L(4, 'Aerial Photograph and Ordnance Survey Map'),
                   (L(4, 'Examine both the aerial photograph and the Ordnance Survey map that accompany this',
                      'answer for each of the following:'),),
                   ID + 'p1-q4', ('aerial', 'map', 'legend'), [
    ('(i)', 2, L(4, '(i) What is the name of the river which flows from the left background to the right',
                 'aerial photograph?'),
     (HEAD2, S(3, 'Q4', '(ii) Old Bridge', LEFT)), answer('River', EACH2, 'Q4 · (i) River Suir'), '2-8', AER + MAP),
    ('(ii)', 4, L(4, '(ii) What are the names of the two bridges in the aerial photograph?'),
     (HEAD2, S(3, '(ii) Old Bridge', '(iii) S 408', LEFT)),
     answer('Two bridges', EACH2, '(ii) Old Bridge & Dillon Bridge', 4, (0, 2, 4)), '2-8', AER + MAP),
    ('(iii)', 2, L(4, '(iii) Over which of the following points was the camera when the aerial photograph',
                   'S 405 229'),
     (HEAD2, S(3, '(iii) S 408', 'Q5', LEFT)), answer('Camera position', EACH2, '(iii) S 408 215'),
     '2-8', AER + MAP),
])
PART_ONE += romans('5', P1, 5, L(5, 'Glacial Landforms'),
                   (L(5, 'Examine the Ordnance Survey map extract below.', 'in the spaces provided.'),),
                   ID + 'p1-q5', ('page',), [
    ('(i)', 2, L(5, '(i) The height above sea level of the surface of Coomasaharn Lake is:'),
     (HEAD2, S(3, 'Q5', '(ii)Cirque', LEFT)), answer('Height', EACH2, 'Q5 · (i) 161'), '2-6', MAP + GLAC),
    ('(ii)', 2, L(5, '(ii) What type of glacial lake is Coomasaharn Lake?'),
     (HEAD2, S(3, '(ii)Cirque', '(iii) Arête', LEFT)),
     answer('Type of glacial lake', EACH2, '(ii)Cirque/Corrie/Tarn/Coom/Ribbon'), '0-11', GLAC + MAP),
    ('(iii)', 2, L(5, '(iii) What is the correct name for the feature found at X?', 'Pyramidal Peak'),
     (HEAD2, S(3, '(iii) Arête', '(iv) North', LEFT)), answer('Feature at X', EACH2, '(iii) Arête'),
     '0-11', GLAC + MAP),
    ('(iv)', 2, L(5, '(iv) The glacier which shaped Coomasaharn Lake moved out of the basin',
                  'South Eastwards'),
     (HEAD2, S(3, '(iv) North', 'Q6', LEFT)), answer('Direction', EACH2, '(iv) North Eastwards'),
     '0-11', GLAC + MAP),
])
PART_ONE += romans('6', P1, 6, L(6, 'Weather Chart', nth=0),
                   (L(6, 'The Atlantic Weather Chart below shows a weather situation in June.',
                      'questions which follow:'),),
                   ID + 'p1-q6', ('page',), [
    ('(i)', 2, L(6, '(i) Is Ireland under the influence of a Depression or an Anticyclone?'),
     (HEAD2, S(3, 'Q6', '(ii) Isobar', LEFT)), answer('Depression or anticyclone', EACH2, 'Q6 · (i) Anticyclone'),
     '2-7', WX),
    ('(ii)', 2, L(6, '(ii) Name the type of line at A on the map.'),
     (HEAD2, S(3, '(ii) Isobar', '(iii) 1012', LEFT)), answer('Type of line', EACH2, '(ii) Isobar'), '2-7', WX),
    ('(iii)', 2, L(6, '(iii) What is the barometric pressure at B on the map?'),
     (HEAD2, S(3, '(iii) 1012', '(iv) Calm', LEFT)),
     answer('Pressure', EACH2, '(iii) 1012 mb / hectopascals (hPa)'), '2-7', WX),
    ('(iv)', 2, L(6, '(iv) Which of the descriptions below best describe weather conditions over Ireland?',
                  'Calm dry weather with warm temperature.'),
     (HEAD2, S(3, '(iv) Calm', None, LEFT)),
     answer('Weather conditions', EACH2, ('(iv) Calm dry weather with warm', '=temperature')), '2-7', WX),
])
PART_ONE += [
    T('p1-7', P1, '7', '', 8, 7, L(7, 'Land-use'),
      (L(7, 'Match each of the land-use letters in Column X', 'One match has been made for you.'),),
      (HEAD1, S(3, 'Q7', 'B = 1', RIGHT), S(3, 'C = 9', 'Q8', RIGHT)),
      priced_rows(EACH1, ['Q7 · A = 8', 'C = 9', 'D = 2', 'E = 7', 'F = 3', 'G = 4', 'H = 6', 'I = 5'], 1),
      '4-4', LAND + URB, ID + 'p1-q7', ('page',),
      row_labels=(L(7, 'A House'), L(7, 'C Factory'), L(7, 'D School'), L(7, 'E Road'), L(7, 'F Church'),
                  L(7, 'G Town Hall'), L(7, 'H Sports Field'), L(7, 'I Bank'))),
    T('p1-8', P1, '8', '', 8, 7, L(7, 'Location on the Aerial Photograph'),
      (L(7, 'Study the sketch map below and the aerial photograph which accompanies this paper.',
         '(left background etc.).'),),
      (HEAD2, S(3, 'Q8', 'Q9', RIGHT)),
      priced_rows(EACH2, ['Q8 · Left Background', '=Left Foreground', '=Right Foreground',
                          ('Centre Background / Centre', 'Middleground / Centre Centre')], 2),
      '2-8', AER, ID + 'p1-q8', ('page', 'aerial'),
      row_labels=(L(7, 'Old Bridge', nth=1), L(7, 'House', nth=2), L(7, 'Wooded Island', nth=1),
                  L(7, 'Sports Field', nth=2))),
]
PART_ONE += romans('9', P1, 8, L(8, 'Rock Type'),
                   (L(8, 'Examine the photographs of the igneous rocks A and B shown below',
                      'questions which follow:'),),
                   ID + 'p1-q9', ('page',), [
    ('(i)', 4, L(8, '(i) Name each of the rocks.', 'spaces provided.'),
     (HEAD2, S(3, 'Q9', '(ii) 1', RIGHT)),
     (fixed('Rock A', 2, (EACH2, 'Q9 · (i) Basalt')), fixed('Rock B', 2, '=Granite')), '0-1', RW + EV),
    # The scheme prints the answers as "(ii) 1" and, beneath it, a lone "2".
    ('(ii)', 4, L(8, '(ii) Study the diagram below and identify the location where each of the rocks A and B',
                  'Tick the correct box in each case.'),
     (HEAD2, SchemeSlice(3, '(ii) 1', 'Q10', RIGHT, keep_digits=True)),
     (fixed('Rock A', 2, (EACH2, '(ii) 1')), fixed('Rock B', 2, '=2')), '0-1', RW + EV,
     (L(8, 'Rock A forms at 1 or 2'), L(8, 'Rock B forms at 1 or 2'))),
])
PART_ONE.append(T(
    'p1-10', P1, '10', '', 8, 9, L(9, 'Satellite Interpretation'),
    (L(9, 'Match each of the satellite images above with its description', 'spaces provided.'),),
    (HEAD2, S(3, 'Q10', 'Q11', RIGHT)),
    priced_rows(EACH2, ['Q10 · C', '=A', '=D', '=B'], 2),
    '2-8', AER, ID + 'p1-q10', ('page',),
    row_labels=(L(9, 'Sandstorm which is blowing from the Sahara to the Atlantic.'),
                L(9, 'Icebergs breaking away from the ice sheet in Greenland.'),
                L(9, 'The Island Arc of Indonesia.'), L(9, 'Alpine Glacier.'))))
PART_ONE += romans('11', P1, 10, L(10, 'Irish Fishery Statistics'),
                   (L(10, 'Examine the table below and answer the questions that follow:'),),
                   ID + 'p1-q11', ('page',), [
    ('(i)', 2, L(10, '(i) What was the value of Aquaculture in 2004?'),
     (HEAD2, S(3, 'Q11', '(ii) 54.2', RIGHT)), answer('Value', EACH2, 'Q11 · (i) 100.5'), '2-0', TG),
    ('(ii)', 2, L(10, '(ii) What was the change in the total production of fish between 2002 and 2004?'),
     (HEAD2, S(3, '(ii) 54.2', '(iii) Aquaculture', RIGHT)), answer('Change', EACH2, '(ii) 54.2'), '2-0', TG),
    ('(iii)', 2, L(10, '(iii) Which of the following sectors suffered a decline in production', 'Inland catches'),
     (HEAD2, S(3, '(iii) Aquaculture', '(iv) Plankton', RIGHT)), answer('Sector', EACH2, '(iii) Aquaculture'),
     '2-0', TG),
    ('(iv)', 2, L(10, '(iv) What is the name of the microscopic organisms that fish feed on, in the sea?'),
     (HEAD2, S(3, '(iv) Plankton', 'Q12', RIGHT)), answer('Organisms', EACH2, '(iv) Plankton'), '1-4', IRL),
])
PART_ONE += romans('12', P1, 11, L(11, 'Graphical Interpretation'),
                   (L(11, 'Examine the population graphic for the Republic of Ireland (State) and Cork-South',
                      'spaces provided.'),),
                   ID + 'p1-q12', ('page',), [
    ('(i)', 2, L(11, '(i) In which age group is the greatest overall percentage of population in the State?'),
     (HEAD2, S(3, 'Q12', '(ii) 7.0', RIGHT)), answer('Age group', EACH2, 'Q12 · (i) 25-29'), '2-0', TG + POP),
    ('(ii)', 2, L(11, '(ii) What is the total percentage of the population in the 35-39 age group in Cork',
                  'South-Central?'),
     (HEAD2, S(3, '(ii) 7.0', '(iii) 11.7', RIGHT)), answer('Percentage', EACH2, '(ii) 7.0'), '2-0', TG + POP),
    ('(iii)', 2, L(11, '(iii) What percentage of Cork South-Central’s population is over 65 years?'),
     (HEAD2, S(3, '(iii) 11.7', '(iv) 2.8%', RIGHT)), answer('Percentage', EACH2, '(iii) 11.7'), '2-0', TG + POP),
    ('(iv)', 2, L(11, '(iv) What is the difference in population in the 20-24 age group', 'the State?'),
     (HEAD2, S(3, '(iv) 2.8%', None, RIGHT)), answer('Difference', EACH2, '(iv) 2.8%'), '2-0', TG + POP),
])


# ---------------------------------------------------------------- Part Two --
def sketch(outline_label, outline_line, outline_permitted, alloc, item_permitted, labels):
    return (fixed(outline_label, 4, outline_line, outline_permitted),
            *(Criterion(f'Feature {n}', 4, item_permitted, 'exact', alloc) for n in range(1, labels + 1)))


SHOWN2 = sums((0, 1, 2), (0, 2))
OS_SKETCH = sketch('Proportion', 'Proportion: · 4 marks (Graded 4-2-0)', (0, 2, 4),
                   ('4 features @ 4 marks each (Shown 2 marks graded, Named 2 marks)',), SHOWN2, 4)
GRAPH = (fixed('Title', 2, ('Bar Chart · Pie Chart', 'Title: · 2 marks · 2 marks')),
         fixed('Scaled axis (bar chart) / circle and centre (pie chart)', 2,
               'Scaled axis: · 2 marks · 2 marks (Circle & Centred)'),
         fixed('6 items illustrated (2 marks each graded)', 12,
               '6 items illustrated: 2 marks each graded', upto(12)))
LANDFORM = 'erosion or deposition'

PART_TWO = [
    T('p2-1a', P2, '1A', '', 20, 14, L(14, 'Ordnance Survey Map'),
      (L(14, 'Examine the Ordnance Survey map that accompanies this paper.',
         'The complete course of the Glen River.'),),
      (S(6, 'Proportion:', None),), OS_SKETCH, '2-6', MAP + RIVERS, ID + 'p2-q1a', ('map', 'legend'),
      row_labels=(None, L(14, 'One landform created by the processes of river deposition'),
                  L(14, 'A V-Shaped river valley'), L(14, 'An area with a trellised drainage pattern'),
                  L(14, 'The complete course of the Glen River.'))),
    T('p2-1b', P2, '1B', '', 30, 14, L(14, 'Landform Development'),
      (L(14, '(i) Examine, with the aid of a labelled diagram or diagrams, the processes that have led',
         'of your choice.'),),
      (S(7, 'Landform identified:', 'OR'),),
      (fixed('Landform identified', 2, 'Landform identified: · 2 marks'),
       fixed('Named process', 2, 'Named process: · 2 marks'),
       fixed('Irish example', 2, 'Irish example: · 2 marks'),
       pair('Labelled diagram: · 2 marks + 2 marks', 'Labelled diagram'),
       srp('Examination', 10, f'Examination: · 10 x {SRPS}')),
      '0-4', RIVERS + SEA + GLAC, ID + 'p2-q1b-route-i-erosion',
      routes=(
          Route('route-i-erosion', 'Route (i) · landform of erosion', ID + 'p2-q1b-route-i-erosion', False,
                ((LANDFORM, 'erosion'),), topic='0-4', atlas=RIVERS + SEA + GLAC),
          Route('route-i-deposition', 'Route (i) · landform of deposition', ID + 'p2-q1b-route-i-deposition',
                False, ((LANDFORM, 'deposition'),), topic='0-4', atlas=RIVERS + SEA + GLAC),
          Route('route-ii', 'Route (ii)', ID + 'p2-q1b-route-ii', False,
                prompt=(L(14, '(ii) Describe and explain one mass movement process that you have studied.'),),
                scheme=(S(7, 'Mass Movement identified:', None),),
                criteria=(fixed('Mass movement identified', 2, 'Mass Movement identified: · 2 marks'),
                          srp('Examination', 14, f'Examination: · 14 x {SRPS}')),
                topic='0-8', atlas=RW),
      )),
    T('p2-1c', P2, '1C', '', 30, 14, L(14, 'Rocks'),
      (L(14, 'Examine, with reference to examples from Ireland, the formation of metamorphic rocks.'),),
      (S(8, 'Name two metamorphic rocks:', None),),
      (pair('Name two metamorphic rocks: · 2 + 2 marks', 'Two metamorphic rocks named'),
       pair('Name two associated Irish locations: · 2 + 2 marks', 'Two associated Irish locations named'),
       srp('Examination', 11, f'Examination: · 11 x {SRPS}')),
      '0-1', RW, ID + 'p2-q1c'),
]
H2A = S(9, 'Five answers @ 4 marks each', '(i) · A = Clint')
FIVE4 = 'Five answers @ 4 marks each'
PART_TWO += romans('2A', P2, 15, L(15, 'Karst Landscape'),
                   (L(15, 'Examine the photograph and answer the following questions in your answer book:'),),
                   ID + 'p2-q2a', ('page',), [
    ('(i)', 4, L(15, '(i) What is the name of the feature marked A?'),
     (H2A, S(9, '(i) · A = Clint', '(ii) · B = Grike')), answer('Feature A', FIVE4, '(i) · A = Clint', 4),
     '0-3', KARST),
    ('(ii)', 4, L(15, '(ii) What is the name of the feature marked B?'),
     (H2A, S(9, '(ii) · B = Grike', '(iii) Limestone')), answer('Feature B', FIVE4, '(ii) · B = Grike', 4),
     '0-3', KARST),
    ('(iii)', 4, L(15, '(iii) What is the name of the overall feature in the photograph?'),
     (H2A, S(9, '(iii) Limestone', '(iv) Any valid')),
     answer('Overall feature', FIVE4, '(iii) Limestone Pavement', 4), '0-3', KARST),
    ('(iv)', 4, L(15, '(iv) Name one process which helped to form these features.'),
     (H2A, S(9, '(iv) Any valid', '(v) · Limestone')), answer('Process', FIVE4, '(iv) Any valid process', 4),
     '0-3', KARST + RW),
    ('(v)', 4, L(15, '(v) Name the type of rock most associated with these features.'),
     (H2A, S(9, '(v) · Limestone', None)), answer('Rock type', FIVE4, '(v) · Limestone', 4), '0-3', KARST + RW),
])
PART_TWO += [
    T('p2-2b', P2, '2B', '', 30, 15, L(15, 'Folding'),
      (L(15, 'Explain how the study of plate tectonics has helped us to understand the global',
         'Fold Mountains.'),),
      (S(10, 'Reference to global distribution', 'C. · Human Interaction'),),
      (pair('Reference to global distribution: · 2 marks + 2 marks', 'Reference to global distribution'),
       pair('2 named Fold Mountains: · 2 marks + 2 marks', '2 named Fold Mountains'),
       srp('Plate tectonics examined', 11, f'Plate tectonics examined: · 11 x {SRPS}')),
      '0-2', PS + RW, ID + 'p2-q2b'),
    T('p2-2c', P2, '2C', '', 30, 15, L(15, 'Human Interaction'),
      (L(15, 'Humans interact with the rock cycle in many ways.', 'human interaction you have studied.'),),
      (S(10, 'Interaction identified', None),),
      (fixed('Interaction identified', 2, 'Interaction identified: · 2 marks'),
       fixed('Example', 2, 'Example: · 2 marks'), srp('Discussion', 13, f'Discussion: · 13 x {SRPS}')),
      '0-6', RW, ID + 'p2-q2c'),
]
H3A = S(11, 'Four answers @ 5 marks each', '(i) · 3 marks')
FOUR5 = 'Four answers @ 5 marks each'
SPLIT5 = sums((0, 3), (0, 2))
PART_TWO += romans('3A', P2, 16, L(16, 'Earthquakes'),
                   (L(16, 'Examine the map above relating to the earthquake in Haiti in January 2010',
                      'in your answer book:'),),
                   ID + 'p2-q3a', ('page',), [
    ('(i)', 5, L(16, '(i) Activity along which two plates resulted in the earthquake in Haiti?'),
     (H3A, S(11, '(i) · 3 marks', '(ii) · 5 marks')),
     answer('Two plates', FOUR5, '(i) · 3 marks + 2 marks', 5, SPLIT5), '0-0', PS + EV),
    ('(ii)', 5, L(16, '(ii) What type of fault caused the earthquake?'),
     (H3A, S(11, '(ii) · 5 marks', '(iii) 3 marks')), answer('Type of fault', FOUR5, '(ii) · 5 marks', 5),
     '0-7', EV + PS),
    ('(iii)', 5, L(16, '(iii) Describe the fault responsible for the earthquake.'),
     (H3A, S(11, '(iii) 3 marks', '(iv) 5 marks')),
     answer('Description', FOUR5, '(iii) 3 marks + 2 marks', 5, SPLIT5), '0-7', EV + PS),
    ('(iv)', 5, L(16, '(iv) What tectonic activity along the subduction zone created the island arc on the',
                  'map?'),
     (H3A, S(11, '(iv) 5 marks', None)), answer('Tectonic activity', FOUR5, '(iv) 5 marks', 5), '0-0', PS + EV),
])
PART_TWO += [
    T('p2-3b', P2, '3B', '', 30, 16, L(16, 'Human Interaction'),
      (L(16, 'With reference to an example you have studied, describe and account for one way',
         'Mass movement.'),),
      (S(12, 'Influence / Control identified', 'C. · Karst'),),
      (fixed('Influence / control identified', 2, 'Influence / Control identified: · 2 marks'),
       fixed('Named example / location', 2, 'Named Example / Location: · 2 marks'),
       fixed('Reference to natural process', 2, 'Reference to natural process: · 2 marks'),
       srp('Discussion', 12, f'Discussion: · 12 x {SRPS}')),
      '0-6', RIVERS, ID + 'p2-q3b-fluvial-processes',
      routes=choose_one('p2-q3b-', (
          ('Fluvial processes', 'fluvial-processes', '0-6', RIVERS),
          ('Marine processes', 'marine-processes', '0-6', SEA),
          ('Mass movement.', 'mass-movement', '0-6', RW)))),
    T('p2-3c', P2, '3C', '', 30, 16, L(16, 'Karst Landscape'),
      (L(16, 'With reference to the Irish landscape, examine the processes which have influenced the',
         'in a karst region.'),),
      (S(12, 'Named process', None),),
      (fixed('Named process', 2, 'Named process: · 2 marks'),
       fixed('Underground landform identified', 2, 'Underground landform identified: · 2 marks'),
       fixed('Irish example', 2, 'Irish example: · 2 marks'), srp('Discussion', 12, f'Discussion: · 12 x {SRPS}')),
      '0-3', KARST + RW, ID + 'p2-q3c'),
    T('p2-4a', P2, '4A', '', 20, 17, L(17, 'Irish Regions'),
      (L(17, 'In your answer book, draw an outline map of Ireland.', 'show and name the following:'),
       L(17, '(i) Two Irish regions you have studied'), L(17, '(ii) One urban centre in each region'),
       L(17, '(iii) One feature of the physical landscape in each region.')),
      (S(13, 'Map outline:', 'B. · Economic Activities'),),
      (fixed('Map outline', 2, 'Map outline: · 2 marks graded', (0, 1, 2)),
       fixed('Regions', 6, 'Showing and naming region: · 2 x (2 marks graded + 1 mark)', upto(6)),
       fixed('Urban centres', 6, 'Showing and naming urban centres: · 2 x (2 marks graded + 1 mark)', upto(6)),
       fixed('Physical features', 6, 'Showing and naming physical features: · 2 x (2 marks graded + 1 mark)',
             upto(6))),
      '1-4', IRL, ID + 'p2-q4a',
      row_labels=(None, L(17, '(i) Two Irish regions you have studied'), L(17, '(ii) One urban centre in each region'),
                  L(17, '(iii) One feature of the physical landscape in each region.'))),
    T('p2-4b', P2, '4B', '', 30, 17, L(17, 'Economic Activities'),
      (L(17, 'Examine the factors that influence the development of one tertiary economic activity',
         'that you have studied.'),),
      (S(13, 'Named tertiary economic activity', None),),
      (fixed('Named tertiary economic activity', 2, 'Named tertiary economic activity: · 2 marks'),
       pair('Two factors identified: · 2 marks + 2marks', 'Two factors identified'),
       fixed('Region named', 2, 'Region named: · 2 marks'), srp('Examination', 11, f'Examination: · 11 x {SRPS}')),
      '1-5', EURO, ID + 'p2-q4b'),
    T('p2-4c', P2, '4C', '', 30, 17, L(17, 'Culture'),
      (L(17, 'Describe and explain the importance of culture in defining any region studied by you.'),),
      (S(14, 'Region Named', None),),
      (fixed('Region named', 2, 'Region Named: · 2 marks'),
       fixed('Aspect of culture identified', 2, 'Aspect of culture identified: · 2 marks'),
       srp('Explanation', 13, f'Explanation: · 13 x {SRPS}')),
      '1-3', IRL + EURO + CONT, ID + 'p2-q4c'),
]
H5A = S(15, 'Five answers @ 4 marks each', '(i) · 4.6')
PART_TWO += romans('5A', P2, 18, L(18, 'Irish Unemployment', nth=0),
                   (L(18, 'Examine the data in the chart above which shows the monthly unemployment rates',
                      'answer the following questions:'),),
                   ID + 'p2-q5a', ('page',), [
    ('(i)', 4, L(18, '(i) By how much has the male unemployment rate increased from January to', 'September?'),
     (H5A, S(15, '(i) · 4.6', '(ii) · 2.6')), answer('Increase', FIVE4, '(i) · 4.6', 4), '2-0', TG),
    ('(ii)', 4, L(18, '(ii) By how much has the female unemployment rate increased from January to', 'September?'),
     (H5A, S(15, '(ii) · 2.6', '(iii) 59.7')), answer('Increase', FIVE4, '(ii) · 2.6', 4), '2-0', TG),
    ('(iii)', 4, L(18, '(iii) What is the difference between the total male and total female unemployment rate',
                   'September?'),
     (H5A, S(15, '(iii) 59.7', '(iv) August')), answer('Difference', FIVE4, '(iii) 59.7 / 12.6 / 2.0 / 7.2', 4),
     '2-0', TG),
    ('(iv)', 4, L(18, '(iv) In which month was the difference between the male and female unemployment',
                  'greatest?'),
     (H5A, S(15, '(iv) August', '(v) · Any valid')), answer('Month', FIVE4, '(iv) August or September', 4),
     '2-0', TG),
    ('(v)', 4, L(18, '(v) Briefly explain one reason why the percentage increase in unemployment for males',
                 'increase for females.'),
     (H5A, S(15, '(v) · Any valid', None)),
     answer('Reason', FIVE4, '(v) · Any valid explanation (2 marks + 2 marks)', 4, (0, 2, 4)), '1-4', IRL),
])
FACTORS_6B = (('Economic', 'economic', '1-4', IRL), ('Human', 'human', '1-4', IRL),
              ('Physical.', 'physical', '1-4', IRL))
PART_TWO += [
    T('p2-5b', P2, '5B', '', 30, 18, L(18, 'Urban Regions'),
      (L(18, 'Examine the development of one urban area in any Irish region studied by you.'),),
      (S(16, 'Region named', 'C. · Agriculture', None, 'B. · Urban Regions'),),
      (fixed('Region named', 2, 'Region named: · 2 marks'), fixed('Urban area named', 2, 'Urban area named: · 2 marks'),
       srp('Examination', 13, f'Examination: · 13 x {SRPS}')),
      '1-4', IRL + URB, ID + 'p2-q5b'),
    T('p2-5c', P2, '5C', '', 30, 18, L(18, 'Agriculture'),
      (L(18, 'Describe and explain any two factors that influence the development of agriculture',
         'that you have studied.'),),
      (S(16, 'Region named', None, None, 'C. · Agriculture'),),
      (fixed('Region named', 2, 'Region named: · 2 marks'),
       pair('Two named factors: · 2 marks + 2 marks', 'Two named factors'),
       srp('Examination (6 SRPs per factor)', 12, f'Examination: · 12 x {SRPS}')),
      '1-6', CONT, ID + 'p2-q5c'),
    T('p2-6a', P2, '6A', '', 20, 19, L(19, 'European Regions', nth=0),
      (L(19, 'In your answer book, draw an outline map of a European Region', 'show and name the following:'),
       L(19, '(i) Any two physical features in the region'), L(19, '(ii) Any two urban centres in the region.')),
      (S(17, 'Map outline:', 'B. · Irish Regions'),),
      (fixed('Map outline', 4, 'Map outline: · 4 marks graded', upto(4)),
       fixed('Physical features', 8, 'Showing and naming physical features: · 2 x (2 marks graded + 2 marks)',
             upto(8)),
       fixed('Urban centres', 8, 'Showing and naming urban centres: · 2 x (2 marks graded + 2 marks)', upto(8))),
      '1-5', EURO, ID + 'p2-q6a',
      row_labels=(None, L(19, '(i) Any two physical features in the region'),
                  L(19, '(ii) Any two urban centres in the region.'))),
    T('p2-6b', P2, '6B', '', 30, 19, L(19, 'Irish Regions'),
      (L(19, 'Regions can be defined by many factors including:', 'Physical.'),
       L(19, 'Explain how any one of the above factors has defined an Irish Region studied by you.')),
      (S(17, 'Region named', None),),
      (fixed('Region named', 2, 'Region named: · 2 marks'), srp('Examination', 14, f'Examination: · 14 x {SRPS}')),
      '1-4', IRL, ID + 'p2-q6b-economic', routes=choose_one('p2-q6b-', FACTORS_6B)),
    T('p2-6c', P2, '6C', '', 30, 19, L(19, 'European Regions', nth=1),
      (L(19, 'Describe and explain any two factors that influence the development of secondary',
         'that you have studied.'),),
      (S(18, 'Region named', None),),
      (fixed('Region named', 2, 'Region named: · 2 marks'),
       pair('Two named factors: · 2 marks + 2 marks', 'Two named factors'),
       srp('Examination (6 SRPs per factor)', 12, f'Examination: · 12 x {SRPS}')),
      '1-5', EURO, ID + 'p2-q6c'),
]

H7A = S(20, 'Four answers @ 5 marks each', '(i) · Carbon')
PART_TWO += romans('7A', P2, 21, L(21, 'Environmental Impact'),
                   (L(21, 'Examine the graph above and answer the following questions in your answer book:'),),
                   ID + 'p2-q7a', ('page',), [
    ('(i)', 5, L(21, '(i) Which Greenhouse gas makes up most of Ireland’s gas emissions?'),
     (H7A, S(20, '(i) · Carbon', '(ii) · 2001')), answer('Greenhouse gas', FOUR5, '(i) · Carbon Dioxide', 5),
     '2-0', TG + ENV),
    ('(ii)', 5, L(21, '(ii) In which year did Ireland emit 70,000 kilotonnes of greenhouse gas emissions?'),
     (H7A, S(20, '(ii) · 2001', '(iii) Increasing')), answer('Year', FOUR5, '(ii) · 2001', 5), '2-0', TG + ENV),
    ('(iii)', 5, L(21, '(iii) What was the trend in Ireland’s emissions between 1990 and 2001?'),
     (H7A, S(20, '(iii) Increasing', '(iv) Any valid')),
     answer('Trend', FOUR5, '(iii) Increasing / Rising / Growing / Upward', 5), '2-0', TG + ENV),
    ('(iv)', 5, L(21, '(iv) Explain one reason why Ireland should reduce its Greenhouse gas emissions.'),
     (H7A, S(20, '(iv) Any valid', None)),
     answer('Reason', FOUR5, '(iv) Any valid explanation (3 marks + 2 marks)', 5, SPLIT5), '3-4', ENV),
])
REASON_7B = ('3 reasons @ 10 marks each:', 'Reason identified: · 2 marks', 'Map / Photograph evidence: · 2 marks',
             f'Examination: · 3 x {SRPS}')
PART_TWO += [
    T('p2-7b', P2, '7B', '', 30, 21, L(21, 'Multinational Companies'),
      (L(21, 'Examine the aerial photograph and the Ordnance Survey map accompanying this paper.',
         'location for a multinational company.'),),
      (S(21, '3 reasons @ 10 marks each', 'C. · Globalisation'),),
      tuple(Criterion(f'Reason {n}', 10, evens(10), 'srp', REASON_7B) for n in (1, 2, 3)),
      '3-2', MNC + MAP + AER, ID + 'p2-q7b', ('aerial', 'map', 'legend')),
    T('p2-7c', P2, '7C', '', 30, 21, L(21, 'Globalisation'),
      (L(21, 'Explain the effects of globalisation on the economy of a developing country that you',
         'have studied.'),),
      (S(21, 'Named Developing Country', None),),
      (fixed('Named developing country', 2, 'Named Developing Country: · 2 marks'),
       pair('Effects identified: · 2 marks + 2 marks', 'Effects identified'),
       srp('Examination', 12, f'Examination: · 12 x {SRPS}')),
      '3-2', MNC + DEV, ID + 'p2-q7c'),
]
PART_TWO += romans('8A', P2, 22, L(22, 'Economic Development'),
                   (L(22, 'Examine the data in the above table showing the HDI for a number of countries',
                      'in 2007.'),),
                   ID + 'p2-q8a', ('page',), [
    ('(i)', 16, L(22, '(i) Use graph paper to draw a suitable graph to illustrate this data.'),
     S(22, 'Bar Chart · Pie Chart', '(ii) · Literacy'), GRAPH, '2-0', TG),
    ('(ii)', 4, L(22, '(ii) Literacy levels is one of the indicators used to calculate the HDI.',
                  'two other indicators used.'),
     S(22, 'Any two appropriate indicators', None),
     (pair('Any two appropriate indicators @ 2 marks each', 'Two indicators'),), '3-1', DEV),
])
PART_TWO += [
    T('p2-8b', P2, '8B', '', 30, 22, L(22, 'Developed Economy'),
      (L(22, 'Explain the growth of any one developed economy you have studied under one or more',
         'Industrial decline.'),),
      (S(23, 'Developed economy named', 'C. · Conflicts'),),
      (fixed('Developed economy named', 2, 'Developed economy named: · 2 marks'),
       srp('Examination', 14, f'Examination: · 14 x {SRPS}')),
      '3-0', ECON, ID + 'p2-q8b'),
    T('p2-8c', P2, '8C', '', 30, 22, L(22, 'Conflicts of Interest'),
      (L(22, 'Examine how conflict can arise between local interests and global interests',
         'that you have studied.'),),
      (S(23, 'Conflict identified', None),),
      (fixed('Conflict identified', 2, 'Conflict identified: · 2 marks'),
       fixed('Resource identified', 2, 'Resource identified: · 2 marks'),
       fixed('Reference to one example', 2, 'Reference to one example: · 2 marks'),
       srp('Examination', 12, f'Examination: · 12 x {SRPS}')),
      '3-4', ENV, ID + 'p2-q8c'),
    T('p2-9a', P2, '9A', '', 20, 23, L(23, 'Ordnance Survey Map and the Transport Network'),
      (L(23, 'Examine the Ordnance Survey map that accompanies this paper.', 'Railway line.'),),
      (S(24, 'Proportion:', 'B. · European Union Policy'),), OS_SKETCH, '2-6', MAP + ECON, ID + 'p2-q9a',
      ('map', 'legend'),
      row_labels=(None, L(23, 'Built-up area of Carrick-on-Suir'), L(23, 'N24 road'), L(23, 'R697 road'),
                  L(23, 'Railway line.'))),
    T('p2-9b', P2, '9B', '', 30, 23, L(23, 'European Union Policy'),
      (L(23, 'Examine how any one major policy of the European Union has influenced Ireland’s',
         'economic development.'),),
      (S(24, 'Major European policy named', None),),
      (fixed('Major European policy named', 2, 'Major European policy named: · 2 marks'),
       fixed('Influence on Ireland’s economic development', 2,
             'Influence to Ireland’s economic development: · 2 marks'),
       srp('Examination', 13, f'Examination: · 13 x {SRPS}')),
      '3-3', EU_ECON + IRL, ID + 'p2-q9b'),
    T('p2-9c', P2, '9C', '', 30, 23, L(23, 'Sustainable Development'),
      (L(23, 'Discuss the environmental and economic advantages of using renewable energy sources.'),),
      (S(25, 'Environmental advantage identified', None),),
      (fixed('Environmental advantage identified', 2, 'Environmental advantage identified: · 2 marks'),
       fixed('Economic advantage identified', 2, 'Economic advantage identified: · 2 marks'),
       pair('Renewable energy sources: · 2 marks + 2 marks', 'Renewable energy sources'),
       srp('Examination (6/5 SRPs per advantage)', 11, f'Examination: · 11 x {SRPS}')),
      '3-5', ENERGY + ENV, ID + 'p2-q9c'),
]
PART_TWO += romans('10A', P2, 24, L(24, 'Population', nth=0),
                   (L(24, 'Examine the data in the table above showing population density for a number of',
                      'in 2007.'),),
                   ID + 'p2-q10a', ('page',), [
    ('(i)', 16, L(24, '(i) Use graph paper to draw a suitable graph to illustrate this data.'),
     S(26, 'Bar Chart · Pie Chart', '(ii) · In your answer'), GRAPH, '2-0', TG),
    ('(ii)', 4, L(24, '(ii) In your answer book explain the term ‘population density’.'),
     S(26, 'Any valid explanation @ 4 marks', None),
     (pair('Any valid explanation @ 4 marks [2 marks + 2 marks]', 'Explanation'),), '4-0', POP),
])
SETTLEMENT_10C = ('3 historic settlements @ 10 marks each', 'Settlement identified: · 2 marks',
                  'Map reference: · 2 marks', f'Examination: · 3 x {SRPS}')
PART_TWO += [
    T('p2-10b', P2, '10B', '', 30, 24, L(24, 'Migration and Ireland'),
      (L(24, 'Examine two major changes in the patterns of Irish migration within the last one hundred',
         'years.'),),
      (S(27, 'Two changes named', 'C. · Historic'),),
      (pair('Two changes named: · 2 marks + 2 marks', 'Two changes named'),
       pair('Reference to two time periods: · 2 marks + 2 marks', 'Reference to two time periods'),
       srp('Examination (6/5 SRPs per change)', 11, f'Examination: · 11 x {SRPS}')),
      '4-2', POP, ID + 'p2-q10b'),
    T('p2-10c', P2, '10C', '', 30, 24, L(24, 'Historic Settlement'),
      (L(24, 'Examine the 1:50,000 Ordnance Survey map of Carrick-on-Suir that accompanies this',
         'examples of historic settlement.'),),
      (S(27, '3 historic settlements', None),),
      tuple(Criterion(f'Historic settlement {n}', 10, evens(10), 'srp', SETTLEMENT_10C) for n in (1, 2, 3)),
      '4-3', URB + MAP, ID + 'p2-q10c', ('map', 'legend')),
    T('p2-11a', P2, '11A', '', 20, 25, L(25, 'Dynamics of Settlement'),
      (L(25, 'Examine the 1830’s Ordnance Survey map extract of Kilrush', 'developed since the 1830’s.'),),
      (S(28, 'Outline:', None),),
      sketch('Outline', 'Outline: · 4 marks', (0, 4), ('Each of 4 items: · Shown 2 marks graded, Named 2 marks',),
             SHOWN2, 4),
      '2-8', AER + LAND, ID + 'p2-q11a', ('page',),
      row_labels=(None, L(25, 'The present day coastline'), L(25, 'A marina with boats'),
                  L(25, 'Two land-uses which have developed since the 1830’s.'),
                  L(25, 'Two land-uses which have developed since the 1830’s.'))),
    T('p2-11b', P2, '11B', '', 30, 25, L(25, 'Urban Problems'),
      (L(25, '(i) Explain the term ‘traffic congestion’.'),
       L(25, '(ii) Explain two methods used to overcome traffic congestion.', 'in your answer.')),
      (S(29, '(i) · Explanation', 'C. · Developing'),),
      (fixed('(i) Explanation', 2, '(i) · Explanation: · 2 marks graded', (0, 1, 2)),
       pair('(ii) · Two named methods: · 2 marks + 2 marks', '(ii) Two named methods'),
       pair('Named examples: · 2 marks + 2 marks', 'Named examples'),
       srp('Examination (5 SRPs per method)', 10, f'Examination: · 10 x {SRPS}')),
      '4-5', URB, ID + 'p2-q11b'),
    T('p2-11c', P2, '11C', '', 30, 25, L(25, 'Developing World Cities'),
      (L(25, '‘Problems can develop as urban centres expand and grow.’', 'that you have studied.'),),
      (S(29, 'Developing word city identified', None),),
      (fixed('Developing world city identified', 2, 'Developing word city identified: · 2 marks'),
       pair('Two problems identified: · 2 marks + 2 marks', 'Two problems identified'),
       srp('Examination', 12, f'Examination: · 12 x {SRPS}')),
      '4-5', URB, ID + 'p2-q11c'),
]
H12A = S(30, 'Four answers @ 5 marks each', '(i) 5 or')
PART_TWO += romans('12A', P2, 26, L(26, 'Population Change'),
                   (L(26, 'Examine the graph above and answer the following questions in your answer book:'),),
                   ID + 'p2-q12a', ('page',), [
    ('(i)', 5, L(26, '(i) What was the marriage rate per thousand in 1989?'),
     (H12A, S(30, '(i) 5 or', '(ii) · 1979')), answer('Marriage rate', FOUR5, '(i) 5 or 0.5%', 5), '2-0', TG + POP),
    ('(ii)', 5, L(26, '(ii) When did the death rate first drop below 10 per thousand?'),
     (H12A, S(30, '(ii) · 1979', '(iii) Any term')), answer('Year', FOUR5, '(ii) · 1979, 1980, 1981', 5),
     '2-0', TG + POP),
    ('(iii)', 5, L(26, '(iii) What was the general trend in the birth rate between 1983 and 1995?'),
     (H12A, S(30, '(iii) Any term', '(iv) Any valid')),
     answer('Trend', FOUR5, '(iii) Any term that indicates a decrease', 5), '2-0', TG + POP),
    ('(iv)', 5, L(26, '(iv) Briefly explain the term ‘natural increase’.'),
     (H12A, S(30, '(iv) Any valid', None)),
     answer('Explanation', FOUR5, '(iv) Any valid explanation (3 marks + 2 marks)', 5, SPLIT5), '4-0', POP),
])
PART_TWO += [
    T('p2-12b', P2, '12B', '', 30, 26, L(26, 'Migration'),
      (L(26, '‘Ethnic and religious issues can arise as a result of migration.’', 'you have studied.'),),
      (S(31, 'Ethnic issue identified', 'C. · Central'),),
      (fixed('Ethnic issue identified', 2, 'Ethnic issue identified: · 2 marks'),
       fixed('Religious issue identified', 2, 'Religious issue identified: · 2 marks'),
       fixed('Example', 2, 'Example: · 2 marks'), srp('Examination', 12, f'Examination: · 12 x {SRPS}')),
      '4-2', POP, ID + 'p2-q12b'),
    T('p2-12c', P2, '12C', '', 30, 26, L(26, 'Central Place', nth=0),
      (L(26, 'Examine the Ordnance Survey map and aerial photograph accompanying this paper.',
         'surrounding hinterland.'),),
      (S(31, 'Ordnance Survey Map evidence', None),),
      (fixed('Ordnance Survey map evidence', 2, 'Ordnance Survey Map evidence: · 2 marks'),
       fixed('Aerial photograph evidence', 2, 'Aerial Photograph evidence: · 2 marks'),
       srp('Examination', 13, f'Examination: · 13 x {SRPS}')),
      '4-3', URB + MAP + AER, ID + 'p2-q12c', ('aerial', 'map', 'legend')),
]

# ------------------------------------------------------------------ Options --
# Coherence is graded inside each aspect; either printed scheme gives the
# discussion 24 SRPs (48 marks) and identifying plus coherence 32 marks.
def option_criteria(word):
    return (
        Criterion('Aspects identified and overall coherence (3 aspects: 4 + 7/6 marks each; '
                  '4 aspects: 4 + 4 marks each)', 32, upto(32), 'exact',
                  ('Number of aspects', 'Identifying aspect', 'Overall coherence')),
        Criterion(f'{word} (3 aspects @ 8 x SRPs or 4 aspects @ 6 x SRPs)', 48, evens(48), 'srp',
                  (f'{word}: · 8 x SRPs · OR · 6 x SRPs',)),
    )


NOTE = L(27, 'N.B. It is better to discuss three or four aspects', 'large number of points.')


def option(q, page, theme, prompt, scheme_page, topic, atlas, word, after, end=None, routes=()):
    return T(f'p2-{q}', P2, q, '', 80, page, theme, prompt if isinstance(prompt, tuple) else (prompt,),
             (S(scheme_page, 'Number of aspects', end, None, after),), option_criteria(word),
             topic, (atlas,), routes[0].card_id if routes else ID + f'p2-q{q}', stem=(NOTE,), routes=routes)


GI, GE = H + 'option-global-interdependence', H + 'option-geoecology'
CI, AO = H + 'option-culture-identity', H + 'option-atmosphere-ocean'
INDICATOR = 'either language or religion'
OPTIONS = [
    option('13', 28, L(28, 'Global Interdependence'),
           L(28, 'Discuss how the operations of Multinational Companies may contribute to the widening',
             'developed countries.'), 33, '5-1', GI, 'Discussion', '13. ·', '14. ·'),
    option('14', 28, L(28, 'Global Interdependence'),
           L(28, 'Discuss the idea that Fair Trade not Aid is the best way to tackle economic inequality',
             'in the world.'), 33, '5-3', GI, 'Discussion', '14. ·', '15. ·'),
    option('15', 28, L(28, 'Global Interdependence'),
           L(28, 'Examine the causes and the impact of one global environmental issue studied by you.'),
           33, '5-1', GI, 'Examination', '15. ·'),
    option('16', 28, L(28, 'Geoecology'),
           L(28, 'Examine the influence of climate on the characteristics of one biome', 'have studied.'),
           34, '6-2', GE, 'Examination', '16. ·', '17. ·'),
    option('17', 28, L(28, 'Geoecology'),
           L(28, 'Examine two ways in which human activities have impacted on soils.'),
           34, '6-1', GE, 'Examination', '17. ·', '18. ·'),
    option('18', 28, L(28, 'Geoecology'),
           L(28, 'Describe and explain the characteristics of any one soil type studied by you.'),
           34, '6-0', GE, 'Examination', '18. ·'),
    option('19', 29, L(29, 'Culture and Identity'),
           L(29, 'The Gaeltacht areas are distinctive cultural regions. Discuss.'),
           35, '7-0', CI, 'Discussion', '19. ·', '20. ·'),
    option('20', 29, L(29, 'Culture and Identity'),
           L(29, 'Examine the significance of either language or religion as a cultural indicator.'),
           35, '7-0', CI, 'Examination', '20. ·', '21. ·',
           routes=(Route('language', 'language', ID + 'p2-q20-language', False, ((INDICATOR, 'language'),)),
                   Route('religion', 'religion', ID + 'p2-q20-religion', False, ((INDICATOR, 'religion'),)))),
    option('21', 29, L(29, 'Culture and Identity'),
           L(29, 'Discuss the role of migration in any European region you have studied.'),
           35, '7-0', CI, 'Examination', '21. ·'),
    option('22', 29, L(29, 'The Atmosphere-Ocean Environment'),
           L(29, 'Describe and explain why the characteristics of climate change over time.'),
           36, '8-4', AO, 'Examination', '22. ·', '23. ·'),
    option('23', 29, L(29, 'The Atmosphere-Ocean Environment'),
           L(29, 'Examine the impact of climate on the development of tourism in any region that',
             'have studied.'), 36, '8-5', AO, 'Examination', '23. ·', '24. ·'),
    option('24', 29, L(29, 'The Atmosphere-Ocean Environment'),
           L(29, 'Describe and explain the formation of mid-latitude depressions', 'associated with them.'),
           36, '8-3', AO, 'Examination', '24. ·'),
]

TASKS = [*PART_ONE, *PART_TWO, *OPTIONS]

ID_CORRECTION_REASON = 'No 2010 Higher card shipped before this review; every card is new.'

# No 2010 Higher card was live on origin/main before this review.
LEGACY_IDS: list[str] = []
