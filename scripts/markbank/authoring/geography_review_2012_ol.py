"""Independent review ledger: Leaving Certificate Geography 2012 Ordinary Level.

Sources (English editions, harvested Paper Trail corpus; sizes and SHA-256
pinned in EXPECTED_SOURCES and the generated audit): the examination paper
LC005GLP000EV (28 pages; one booklet printed Part One, answered in it, and
Part Two), marking scheme LC005GLP000EV (36 pages), and the common
Carrick-on-Shannon companions shared with Higher Level — the 1:50 000 map
LC005CLP003EV, its legend LC005CLPC00EV and the aerial photograph
LC005CLP004EV (one-page PDFs, each holding one image). Part One is 100 marks
(any ten of twelve @ 10), Part Two 300 (three questions @ 100).

Visual sweep (every page rendered and read on 2026-10-23):
  Paper p1 cover and examiner's grid; p2-p10 Part One Questions 1-12 (p3
  holds Q2 and Q3, p4 Q4 and Q5, p5 Q6 and Q7; Q1 prints four volcanic
  photographs, Q8 four satellite images, Q9 a census table, Q10 a weather
  chart, Q11 a photograph of the Giant's Causeway); p11 Part Two
  instructions; p12 Section 1 divider; p13-p19 Q1-Q6 (p13 and p17 open with
  their dividers; p15 holds 3A and 3B, p16 3C and its karst diagram); p20
  Section 2 divider; p21-p26 Electives Q7-Q12 (p21 and p24 open with their
  elective dividers); p27-p28 printed "Blank Page".
  Scheme p1 cover; p2 blank; p3 note on marking schemes; p4 Geographical
  Investigation (coursework); p5-p7 Part One table (Q1-Q5, Q6-Q10,
  Q11-Q12); p8 Part Two instructions; p9 Section 1 divider; p10-p19 Q1-Q6
  (p10 and p15 open with their dividers); p20 Section 2 divider; p21-p30
  Q7-Q12 (p21 and p26 open with their elective dividers); p31 investigation
  topics; p32 Irish-language bonus marks; p33-p35 blank; p36 back cover.
  The scheme reprints most Part Two questions above their allocations;
  every slice starts at the allocation.
  Companions: Carrick-on-Shannon map extract (the River Shannon, Lough
  Eidin, Oakport Lough, the Jamestown Canal, Drumsna; Ordnance Survey
  Ireland 2012); OSi Discovery Series legend sheet; oblique aerial
  photograph of Carrick-on-Shannon (the marina, the bridge over the Shannon,
  the town centre and an unfinished building site).

Part One prices every answer on its own line ("2 marks", "5 marks"; Q10(i)
"1 mark" a front), so each separately answered roman is a task and every
matching table is one card of rows. Matching tables, in the printed row
order: Q1(i) Lava flow A, Ash cloud D, Geyser B, Crater C; Q2 Forestry
Primary, Tourism Tertiary, Manufacturing Secondary, Agriculture Primary,
Services Tertiary (Mining is printed); Q3 Swash and backwash D, Bog burst C,
Freeze-thaw A, Solution E, Abrasion B; Q5(i) M 936 996 Post Office, M 983
953 Ringfort, G 896 017 Crannóg, G 885 013 Golf course; Q7 Glacial
deposition E, River erosion A, Marine erosion D, Marine deposition C,
Glacial erosion B; Q8(i) A mine in the desert B, A major ferry port C, A
railway and bus station D, An industrial estate A; Q10(i) Cold Front B,
Warm Front A; Q12 The Alps E, Paris A, Mediterranean D, The South of
Italy/Mezzogiorno B, The Basque Region of Spain C.

The 2012 scheme prints "graded" without a scale on its sketch, outline,
axis, item and grid-reference lines; such a line allows every whole mark up
to its printed tariff (no grade is invented). 1A: the scheme notes that a
printing error omitted the forestry symbols from the candidates' legend and
prints "Mixed woodland shown and named · award 5 marks to all candidates";
that line is the item's guidance (the Paper Trail legend sheet does show the
three forestry symbols). 11B(i) prints "Two locations @ 3 marks each · 6
marks each"; the part is 6 marks (6 + 12 + 12 = Total Marks 30).

Printed choices: 2B (i) or (ii) is two routes; 1B(iii) "sedimentary rocks
or metamorphic rocks" two routes; 3B (one of three surface processes) and
9B (any one of four EU funds) one route per option; 4B, 4C and 6B (any two
of a printed list) are pools, one card each.

Tariffs as printed: twelve parts carry 40 marks (1B, 2B, 3C, 4C, 5B, 6B,
7B, 8C, 9C, 10B, 11C, 12B) and the rest 30.
"""

from geography_review import (
    Criterion, Lift, Route, SchemeSlice, Task, pool, fixed, slug, srp, steps, sums, upto,
)

YEAR = 2012
LEVEL = 'ordinary'
PAPER_PAGES = {1: 28, 2: 28}
SCHEME_PAGES = 36
_FORTY = {'1B', '2B', '3C', '4C', '5B', '6B', '7B', '8C', '9C', '10B', '11C', '12B'}
QUESTION_TARIFFS = {1: {str(n): 10 for n in range(1, 13)},
                    2: {f'{n}{x}': (40 if f'{n}{x}' in _FORTY else 30)
                        for n in range(1, 13) for x in 'ABC'}}

EXPECTED_SOURCES = {
    'paper1': ('LC005GLP000EV.pdf', 1496544),
    'paper2': ('LC005GLP000EV.pdf', 1496544),
    'scheme': ('LC005GLP000EV.pdf', 454708),
    'map': ('LC005CLP003EV.pdf', 1738631),
    'legend': ('LC005CLPC00EV.pdf', 267008),
    'aerial': ('LC005CLP004EV.pdf', 3193770),
}

_PAPER = {1: 'cover and examiner grid', **{p: 'question' for p in range(2, 11)},
          11: 'Part Two instructions', 12: 'section divider', **{p: 'question' for p in range(13, 20)},
          20: 'section divider', **{p: 'question' for p in range(21, 27)}, 27: 'blank page', 28: 'blank page'}
PAGE_REVIEW = {
    # One booklet printed both parts.
    'paper1': _PAPER, 'paper2': _PAPER,
    'scheme': {1: 'cover', 2: 'blank', 3: 'notes', 4: 'geographical investigation (coursework)',
               5: 'Part One table', 6: 'Part One table', 7: 'Part One table',
               8: 'Part Two instructions', 9: 'section divider',
               **{p: 'Part Two allocation' for p in range(10, 20)}, 20: 'section divider',
               **{p: 'Part Two allocation' for p in range(21, 31)},
               31: 'investigation topics', 32: 'Irish-language bonus marks',
               33: 'blank', 34: 'blank', 35: 'blank', 36: 'back cover'},
}

EXPECTED_SELECTION_SCAN = [
    [1, 2, 'attempt ten'], [1, 11, 'attempt three'], [1, 12, 'attempt two'], [1, 13, 'attempt one'],
    [1, 14, 'answer (i) or (ii)'], [1, 14, 'any two'], [1, 14, 'any two'],
    [1, 15, 'attempt to'], [1, 15, 'one of the following'],
    [1, 16, 'any one'],
    [1, 17, 'attempt one'], [1, 17, 'any two'], [1, 17, 'any two'],
    [1, 18, 'any two'],
    [1, 19, 'any two'],
    [1, 20, 'attempt one'],
    [1, 22, 'any one'],
    [1, 23, 'choose'], [1, 23, 'any one'],
]
SELECTION_REVIEW = [
    {'scan': [[1, 2, 'attempt ten'], [1, 11, 'attempt three'], [1, 12, 'attempt two'], [1, 13, 'attempt one'],
              [1, 17, 'attempt one'], [1, 20, 'attempt one']],
     'kind': 'exam-attempt-rule',
     'reason': 'Part One any ten of twelve and Part Two three questions (one of Q1-3, one of Q4-6, one elective) are attempt rules; every question is carded.'},
    {'scan': [[1, 14, 'answer (i) or (ii)']], 'kind': 'closed-route',
     'reason': '2B: (i) or (ii) -> two routes, each with its own scheme allocation.'},
    {'scan': [], 'kind': 'inline-closed-route',
     'reason': '1B(iii) "sedimentary rocks or metamorphic rocks" -> 2 routes under one allocation (no directive word the scan reads; the route text is anchored on the paper).'},
    {'scan': [[1, 15, 'one of the following'], [1, 23, 'choose'], [1, 23, 'any one']], 'kind': 'closed-choose-one',
     'reason': '3B one of three printed surface processes -> 3 routes; 9B "Choose any one of the above" four printed EU funds -> 4 routes.'},
    {'scan': [[1, 17, 'any two'], [1, 17, 'any two'], [1, 19, 'any two']], 'kind': 'choose-n-one-card',
     'reason': '4B any two of three printed influences, 4C any two of three printed activities and 6B any two of four printed influences -> one card each with every printed item (choice is not a route).'},
    {'scan': [[1, 14, 'any two'], [1, 14, 'any two'], [1, 16, 'any one'], [1, 18, 'any two'], [1, 22, 'any one']],
     'kind': 'open-response',
     'reason': 'No printed pool: 2B(i) any two Irish landforms and 2B(ii) any two mass movement processes (the scheme prices two @ 20 marks); 3C(iii) any one karst feature; 5A(iv) any two Irish tourist attractions; 8C(ii) any one of the causes the candidate named in (i). Open choices are not fanned out: Part One Q1(ii) "any volcano", 11C(i) "a developing or a developed city". Answer options are not routes: Part One Q11(i) igneous/sedimentary/metamorphic, Q11(iii) the Burren or the Giant’s Causeway. Compulsory lists stay whole: 1A, 4A, 6A, 7A, 11A each item; 2A(i) each layer.'},
    {'scan': [[1, 15, 'attempt to']], 'kind': 'not-a-selection',
     'reason': '3B "how humans attempt to control" describes human activity, not a candidate choice.'},
]

P1, P2 = 1, 2
ID = 'geography-2012-ol-'
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
    [, row labels[, extra stem Lifts[, sources]]])."""
    out = []
    for index, item in enumerate(parts):
        sub, marks, prompt, scheme, criteria, topic, atlas = item[:7]
        labels = item[7] if len(item) > 7 else ()
        extra = item[8] if len(item) > 8 else ()
        own = item[9] if len(item) > 9 else sources
        key = sub.strip('()').replace(')(', '-')
        out.append(T(f'p{part}-{q.lower()}-{key}', part, q, sub, marks, page, title,
                     prompt if isinstance(prompt, tuple) else (prompt,),
                     scheme if isinstance(scheme, tuple) else (scheme,), criteria, topic, atlas,
                     first_id if index == 0 else f'{first_id}-{key}', own, (*stem, *extra),
                     row_labels=labels))
    return out


def bullet_routes(prefix, items, atlas=None):
    return tuple(Route(slug(item, 34), item.rstrip('.'), ID + prefix + slug(item, 34), False,
                       keep_bullets=(item,), atlas=(atlas[item] if atlas else None))
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
PS_SURFACE = RIVERS + SEA + GLAC

# ---------------------------------------------------------------- Part One --
PART_ONE = romans('1', P1, 2, L(2, 'Volcanic Activity'), (), ID + 'p1-q1', ('page',), [
    ('(i)', 8, L(2, '(i) Examine the photographs above and correctly match each of the letters',
                 'in the table below.'),
     S(5, '(i) · Lava Flow', '(ii) · Named volcano'),
     rows(['(i) · Lava Flow · A · 2 marks', 'Ash Cloud · D · 2 marks', 'Geyser · B · 2 marks',
           'Crater · C · 2 marks']), '0-7', EV,
     (L(2, 'Lava flow'), L(2, 'Ash cloud'), L(2, 'Geyser'), L(2, 'Crater'))),
    ('(ii)', 2, L(2, '(ii) Write the name of any volcano in the space below.'),
     S(5, '(ii) · Named volcano', 'Total Marks 10'), (fixed('Volcano', 2, '(ii) · Named volcano · 2 marks'),),
     '0-7', EV),
])
PART_ONE += [
    T('p1-2', P1, '2', '', 10, 3, L(3, 'Economic Activities'),
      (L(3, 'In the table below, write the category (Primary/Secondary/Tertiary)', 'One has been completed for you.'),),
      (S(5, 'Forestry · Primary', 'Total Marks 10'),),
      rows(['Forestry · Primary · 2 marks', 'Tourism · Tertiary · 2 marks', 'Manufacturing · Secondary · 2 marks',
            'Agriculture · Primary · 2 marks', 'Services · Tertiary · 2 marks']),
      '3-0', ECON, ID + 'p1-q2', ('page',),
      row_labels=(L(3, 'Forestry'), L(3, 'Tourism'), L(3, 'Manufacturing'), L(3, 'Agriculture'),
                  L(3, 'Services'))),
    T('p1-3', P1, '3', '', 10, 3, L(3, 'Physical Processes'),
      (L(3, 'Match the explanation of the process with the name of the process', 'in the table below.'),),
      (S(5, 'Swash and backwash · D', 'Total Marks 10'),),
      rows(['Swash and backwash · D · 2 marks', 'Bog burst · C · 2 marks', 'Freeze-thaw · A · 2 marks',
            'Solution · E · 2 marks', 'Abrasion · B · 2 marks']),
      '0-4', RW + RIVERS + SEA, ID + 'p1-q3', ('page',),
      row_labels=(L(3, 'Swash and backwash'), L(3, 'Bog burst'), L(3, 'Freeze-thaw'), L(3, 'Solution'),
                  L(3, 'Abrasion'))),
]
OS4 = L(4, 'Examine the 1:50000 Ordnance Survey map and legend accompanying this paper.', nth=0)
OS5 = L(4, 'Examine the 1:50000 Ordnance Survey map and legend accompanying this paper.', nth=1)
PART_ONE += romans('4', P1, 4, L(4, 'Ordnance Survey Map', nth=0), (OS4,), ID + 'p1-q4', ('map', 'legend'), [
    ('(i)', 5, L(4, '(i) Calculate the area of the map in square kilometres.', 'Write the correct answer in the box below.'),
     S(5, '(i) · 108', '(ii) · 7.5'), (fixed('Area', 5, '(i) · 108 · 5 marks'),), '2-6', MAP),
    ('(ii)', 5, L(4, '(ii) Measure the length of the River Shannon', 'Write the correct answer in the box below.'),
     S(5, '(ii) · 7.5', 'Total Marks 10'), (fixed('Length', 5, '(ii) · 7.5 · (Range 7-8) · 5 marks'),), '2-6', MAP),
])
PART_ONE += romans('5', P1, 4, L(4, 'Ordnance Survey Map', nth=1), (OS5,), ID + 'p1-q5', ('map', 'legend'), [
    ('(i)', 8, L(4, '(i) Name the features which can be found at each of the following grid references.'),
     S(5, '(i) · Post Office', '(ii) · Symbol drawn'),
     rows(['(i) · Post Office · 2 marks', 'Ringfort /Rath/Lios/Enclosure/Clós · 2 marks', 'Crannóg · 2 marks',
           'Golf course · 2 marks']), '2-6', MAP,
     (L(4, 'M 936 996'), L(4, 'M 983 953'), L(4, 'G 896 017'), L(4, 'G 885 013'))),
    ('(ii)', 2, L(4, '(ii) Draw the Ordnance Survey map symbol for an Electricity Transmission Line', 'in the box below.'),
     S(5, '(ii) · Symbol drawn', 'Total Marks 10'), (fixed('Symbol', 2, '(ii) · Symbol drawn · 2 marks'),),
     '2-6', MAP),
])
PART_ONE += romans('6', P1, 5, L(5, 'Aerial Photograph and Ordnance Survey Map'), (), ID + 'p1-q6', ('aerial',), [
    ('(i)', 6, L(5, '(i) Examine the aerial photograph of Carrick-on-Shannon accompanying this paper.',
                 'write the location of each of the following:'),
     S(6, '(i) · Correct Location', '(ii) · North East'),
     (fixed('Location 1', 2, '(i) · Correct Location · 2 marks'),
      fixed('Location 2', 2, '=Correct Location · 2 marks@0'),
      fixed('Location 3', 2, '=Correct Location · 2 marks@1')), '2-8', AER,
     (L(5, 'A car park'), L(5, 'A bridge'), L(5, 'A church'))),
    ('(ii)', 2, L(5, '(ii) Examine the Ordnance Survey map accompanying this paper.',
                  'In what direction would you be travelling?'),
     S(6, '(ii) · North East', '(iii) · River/Marina'), (fixed('Direction', 2, '(ii) · North East · 2 marks'),),
     '2-6', MAP, (), (), ('map', 'legend')),
    ('(iii)', 2, L(5, '(iii) State one piece of evidence from the aerial photograph', 'is a tourist town.'),
     S(6, '(iii) · River/Marina', 'Total Marks 10'),
     (fixed('Evidence', 2, ('(iii) · River/Marina/holiday homes/', 'any valid evidence · 2 marks')),),
     '2-8', AER + URB),
])
PART_ONE += [
    T('p1-7', P1, '7', '', 10, 5, L(5, 'Physical Landforms'),
      (L(5, 'Match the landform with the name of the process responsible for its formation', 'in the table below.'),),
      (S(6, 'Glacial deposition · E', 'Total Marks 10'),),
      rows(['Glacial deposition · E · 2 marks', 'River erosion · A · 2 mark s', 'Marine erosion · D · 2 marks',
            'Marine deposition · C · 2 marks', 'Glacial erosion · B · 2 marks']),
      '0-4', PS_SURFACE, ID + 'p1-q7', ('page',),
      row_labels=(L(5, 'Glacial deposition'), L(5, 'River erosion'), L(5, 'Marine erosion'),
                  L(5, 'Marine deposition'), L(5, 'Glacial erosion'))),
]
PART_ONE += romans('8', P1, 6, L(6, 'Satellite Images'), (), ID + 'p1-q8', ('page',), [
    ('(i)', 8, L(6, '(i) Study the satellite images above and match the description below', 'in the table below.'),
     S(6, '(i) · A mine in the desert', '(ii) · Use named'),
     rows(['(i) · A mine in the desert · B · 2 marks', 'A major ferry port · C · 2 marks',
           'A railway and bus station · D · 2 marks', 'An industrial estate · A · 2 marks']), '2-8', AER,
     (L(6, 'A mine in the desert'), L(6, 'A major ferry port'), L(6, 'A railway and bus station'),
      L(6, 'An industrial estate'))),
    ('(ii)', 2, L(6, '(ii) Name one use of satellite images.'),
     S(6, '(ii) · Use named', 'Total Marks 10'), (fixed('Use', 2, '(ii) · Use named · 2 marks'),), '2-8', AER),
])
PART_ONE += romans('9', P1, 7, L(7, 'Irish Census'),
                   (L(7, 'Study the table above which shows the population of regional authority areas',
                      'answer the following questions.'),),
                   ID + 'p1-q9', ('page',), [
    ('(i)', 2, L(7, '(i) What was the total population of Ireland in 2006?'),
     S(6, '(i) · 4,252,000', '(ii) · 327,000'), (fixed('Population', 2, '(i) · 4,252,000 · 2 marks'),),
     '2-0', GRAPH + POP),
    ('(ii)', 2, L(7, '(ii) What was the increase in Ireland’s total population between 2006 and 2011?'),
     S(6, '(ii) · 327,000', '(iii) · South-West'), (fixed('Increase', 2, '(ii) · 327,000 · 2 mark s'),),
     '2-0', GRAPH + POP),
    ('(iii)', 2, L(7, '(iii) Which region, excluding the Dublin region,', 'in both 2006 and 2011?'),
     S(6, '(iii) · South-West', '(iv) · Mid-West'), (fixed('Region', 2, '(iii) · South-West · 2 marks'),),
     '2-0', GRAPH + POP),
    ('(iv)', 2, L(7, '(iv) Which region had the smallest population increase between 2006 and 2011?'),
     S(6, '(iv) · Mid-West', '(v) · Reason stated'), (fixed('Region', 2, '(iv) · Mid-West · 2 marks'),),
     '2-0', GRAPH + POP),
    ('(v)', 2, L(7, '(v) State one reason why the Dublin region was the region with the largest population.'),
     S(6, '(v) · Reason stated', 'Total Marks 10'), (fixed('Reason', 2, '(v) · Reason stated · 2 marks'),),
     '4-0', POP),
])
PART_ONE += romans('10', P1, 8, L(8, 'Weather Charts'),
                   (L(8, 'Examine the weather chart above and answer the following questions.'),),
                   ID + 'p1-q10', ('page',), [
    ('(i)', 2, L(8, '(i) Match the two letters, A and B, on the weather chart above', 'in the table below.'),
     S(6, '(i) · Cold Front', '(ii) · H · High'),
     (fixed('Cold Front', 1, '(i) · Cold Front · B · 1 mark'), fixed('Warm Front', 1, 'Warm Front · A · 1 mark')),
     '2-7', WEATHER, (L(8, 'Cold Front'), L(8, 'Warm Front'))),
    ('(ii)', 4, L(8, '(ii) What do the letters H and L on the weather chart above stand for?'),
     S(6, '(ii) · H · High', '(iii) · 987'),
     (fixed('H', 2, '(ii) · H · High · 2 marks'), fixed('L', 2, 'L · Low · 2 marks')), '2-7', WEATHER),
    ('(iii)', 2, L(8, '(iii) What is the lowest barometric pressure over the Atlantic', 'south-west of Ireland?'),
     S(6, '(iii) · 987', '(iv) · Named climate'), (fixed('Pressure', 2, '(iii) · 987 · 2 marks'),), '2-7', WEATHER),
    ('(iv)', 2, L(8, '(iv) What is the name usually given to Ireland’s climate?'),
     S(6, '(iv) · Named climate', 'Total Marks 10'), (fixed('Climate', 2, '(iv) · Named climate · 2 marks'),),
     '2-7', WEATHER),
])
TF11 = 'Read the statement below and place an X in the correct box.'
PART_ONE += romans('11', P1, 9, L(9, 'Rocks'),
                   (L(9, 'Examine the photograph above of a basalt area in Ireland', 'answer the following questions.'),),
                   ID + 'p1-q11', ('page',), [
    ('(i)', 2, L(9, '(i) Is basalt an igneous or a sedimentary or a metamorphic rock?'),
     S(7, '(i) · Igneous', '(ii) · True'), (fixed('Rock type', 2, '(i) · Igneous · 2 marks'),), '0-1', RW),
    ('(ii)', 2, (L(9, f'(ii) {TF11}'), L(9, '‘Basalt is formed by the cooling of lava on the Earth’s surface.’')),
     S(7, '(ii) · True', '(iii) · Giant'), (fixed('True or false', 2, '(ii) · True · 2 marks'),), '0-1', RW),
    ('(iii)', 2, L(9, '(iii) Was this photograph taken in the Burren, Co Clare', 'Co Antrim?'),
     S(7, '(iii) · Giant', '(iv) · False'), (fixed('Location', 2, '(iii) · Giant’s Causeway, Antrim · 2 marks'),),
     '0-1', RW),
    ('(iv)', 2, (L(9, f'(iv) {TF11}'), L(9, '‘Basalt consists of mainly large crystals.’')),
     S(7, '(iv) · False', '(v) · Use stated'), (fixed('True or false', 2, '(iv) · False · 2 marks'),), '0-1', RW),
    ('(v)', 2, L(9, '(v) Name one use of rocks.'),
     S(7, '(v) · Use stated', 'Total Marks 10'), (fixed('Use', 2, '(v) · Use stated · 2 marks'),), '0-6', RW),
])
PART_ONE.append(T(
    'p1-12', P1, '12', '', 10, 10, L(10, 'Regions'),
    (L(10, 'Match the description of a region with the example of a region', 'in the table below.'),),
    (S(7, 'The Alps · E', 'Total Marks 10'),),
    rows(['The Alps · E · 2 marks', 'Paris · A · 2 marks', 'Mediterranean · D · 2 marks',
          'The South of Italy/Mezzogiorno · B · 2 marks', 'The Basque region of Spain · C · 2 marks']),
    '1-0', EURO, ID + 'p1-q12', ('page',),
    row_labels=(L(10, 'The Alps'), L(10, 'Paris'), L(10, 'Mediterranean'), L(10, 'The South of Italy/Mezzogiorno'),
                L(10, 'The Basque Region of Spain'))))


# ---------------------------------------------------------------- Part Two --
def two_of(label, count, head, each, lines, unit):
    per = sums(*unit)
    return tuple(Criterion(f'{label} {n}', count, per, 'srp', (head, each, *lines)) for n in (1, 2))


def sketch(page, title, prompt, scheme_page, card_id, topic, atlas, sources, labels):
    """Five sketch items @ 5 (showing 3 graded, naming 2) and a 5-mark frame."""
    return T(f'p2-{card_id.rsplit("-q", 1)[1]}', P2, card_id.rsplit('-q', 1)[1].upper(), '', 30, page,
             title, (prompt,), (S(scheme_page, 'Sketch Map as follows:', 'Total Marks 30'),),
             (fixed('Limits/frame', 1, ('Sketch Map as follows:', 'Limits/frame · 1 mark')),
              fixed('Proportions (landscape)', 2, 'Proportions (landscape) · 2 marks graded', upto(2)),
              fixed('Overall impression', 2, 'Overall impression · 2 marks graded', upto(2)),
              *(Criterion(f'Item {n}', 5, upto(5), 'exact',
                          ('Five items shown and named as follows:', 'Showing · 3 marks graded',
                           'Naming/identifying · 2 marks'))
                for n in range(1, 6))),
             topic, atlas, card_id, sources,
             row_labels=(None, None, None, *(L(page, b) for b in labels)))


SHOWN = 'Shown · 4 marks graded'
NAMED_SHOWN = sums((0, 2), upto(4))
GRAPH_OL = (fixed('Graph paper', 2, 'Graph paper · 2 marks'),
            fixed('Vertical axis labelled / circle', 3, 'Vertical Axis labelled - Circle · 3 marks graded', upto(3)),
            fixed('Horizontal axis labelled / centred', 3, 'Horizontal Axis labelled - Centred · 3 marks graded',
                  upto(3)),
            fixed('4 items illustrated', 16, '4 Items @ · 4 marks each graded · 16 marks', upto(16)))
SURFACE = ('River processes', 'Sea processes', 'Mass movement.')
FUNDS = ('Common Agricultural Policy (CAP)', 'Common Fisheries Policy (CFP)', 'Regional Development Fund (RDF)',
         'Social Funding.')
INFLUENCES_4B = ('Relief and soils', 'Climate', 'Markets.')
ACTIVITIES_4C = ('Tourism', 'Transport', 'Manufacturing.')
INFLUENCES_6B = ('Transport', 'Raw materials', 'Markets', 'Government and European Union policies.')
ITEM_1A = ('Four other items shown and named as follows:', 'Showing · 3 marks graded', 'Naming/identifying · 2 marks')

PART_TWO = [
    T('p2-1a', P2, '1A', '', 30, 13, L(13, 'Ordnance Survey Map'),
      (L(13, 'Examine the 1:50000 Ordnance Survey map and legend accompanying this paper.',
         'in the north-east of the map.'),),
      (S(10, 'A printing error in the legend', 'Total Marks 30'),),
      (fixed('Limits/frame', 1, ('Sketch Map as follows', 'Limits/frame · 1 marks')),
       fixed('Proportions', 2, 'Proportions · 2 marks graded', upto(2)),
       fixed('Overall impression', 2, 'Overall impression · 2 marks graded', upto(2)),
       fixed('Mixed woodland', 5, 'Mixed woodland shown and named · award 5 marks to all candidates'),
       *(Criterion(f'Item {n}', 5, upto(5), 'exact', ITEM_1A) for n in range(1, 5))),
      '2-6', MAP + RIVERS, ID + 'p2-q1a', ('map', 'legend'),
      row_labels=(None, None, None, L(13, 'An area of mixed woodland'), L(13, 'The River Shannon'),
                  L(13, 'Oakport Lough'), L(13, 'The Jamestown Canal'),
                  L(13, 'An area of land over 120 metres above sea level in the north-east of the map.'))),
]
PART_TWO += romans('1B', P2, 13, L(13, 'Rocks'), (), ID + 'p2-q1b', (), [
    ('(i)', 5, L(13, '(i) Name one sedimentary rock and name one Irish location where this rock is found.'),
     S(11, 'Rock named', '(ii) · Name one metamorphic', None, '(i) · Name one sedimentary'),
     (fixed('Sedimentary rock named', 2, 'Rock named · 2 marks'), fixed('Irish location', 3, 'Irish Location · 3 marks')),
     '0-1', RW + IRL),
    ('(ii)', 5, L(13, '(ii) Name one metamorphic rock and name one Irish location where this rock is found.'),
     S(11, 'Rock named', '(iii) · Describe how', None, '(ii) · Name one metamorphic'),
     (fixed('Metamorphic rock named', 2, 'Rock named · 2 marks'), fixed('Irish location', 3, 'Irish Location · 3 marks')),
     '0-1', RW + IRL),
])
ROCKS = 'sedimentary rocks or metamorphic rocks'
PART_TWO += [
    T('p2-1b-iii', P2, '1B', '(iii)', 30, 13, L(13, 'Rocks'),
      (L(13, '(iii) Describe how sedimentary rocks or metamorphic rocks are formed.'),),
      (S(11, '10 SRPs @ 3 marks each', 'Total Marks 40'),),
      (srp3('Description', 10, '10 SRPs @ 3 marks each · 30 marks'),),
      '0-1', RW, ID + 'p2-q1b-iii-sedimentary-rocks',
      routes=(Route('sedimentary-rocks', 'sedimentary rocks', ID + 'p2-q1b-iii-sedimentary-rocks', False,
                    ((ROCKS, 'sedimentary rocks'),)),
              Route('metamorphic-rocks', 'metamorphic rocks', ID + 'p2-q1b-iii-metamorphic-rocks', False,
                    ((ROCKS, 'metamorphic rocks'),)))),
]
PART_TWO += romans('1C', P2, 13, L(13, 'Plate Tectonics'), (), ID + 'p2-q1c', (), [
    ('(i)', 3, L(13, '(i) Name one tectonic plate on the Earth’s crust.'),
     S(11, 'Plate named', '(ii) · What is the name'), (fixed('Plate named', 3, 'Plate named · 3 marks'),), '0-0', PS),
    ('(ii)', 3, L(13, '(ii) What is the name given to the area of earthquakes and volcanoes',
                  'around the Pacific Ocean?'),
     S(11, 'Pacific Ring of Fire', '(iii) · Describe in detail'),
     (fixed('Name', 3, 'Pacific Ring of Fire · 3 marks'),), '0-0', PS + EV),
    ('(iii)', 24, L(13, '(iii) Describe in detail how volcanoes occur.'),
     S(11, '8 SRPs @ 3 marks each', 'Total Marks 30'),
     (srp3('Description', 8, '8 SRPs @ 3 marks each · 24 marks'),), '0-7', EV + PS),
])
PART_TWO += romans('2A', P2, 14, L(14, 'Internal Structure of the Earth'), (), ID + 'p2-q2a', ('page',), [
    ('(i)', 24, L(14, '(i) In your answer book, match each of the following names', 'Inner Core.'),
     S(12, 'Four identified correctly', '(ii) · State two disadvantages'),
     (fixed('Layer 1', 6, ('Four identified correctly @ · 6 marks each', 'Crust · A')),
      fixed('Layer 2', 6, 'Outer Core · C'), fixed('Layer 3', 6, 'Mantle · B'), fixed('Layer 4', 6, 'Inner Core · D')),
     '0-0', PS, (L(14, 'Crust'), L(14, 'Outer Core'), L(14, 'Mantle'), L(14, 'Inner Core'))),
    ('(ii)', 6, L(14, '(ii) State two disadvantages of volcanoes.'),
     S(12, '2 SRPs @ 3 marks · 6 marks', 'Total Marks 30'),
     (srp3('Two disadvantages', 2, '2 SRPs @ 3 marks · 6 marks'),), '0-7', EV, (), (), ()),
])
PART_TWO.append(T(
    'p2-2b', P2, '2B', '', 40, 14, L(14, 'Surface Processes'),
    (L(14, '(i) Explain, with the aid of diagrams, the formation of any two different Irish',
       'landforms that you have studied.'),),
    (S(12, 'Formation of any two Irish landforms', 'OR'),),
    two_of('Landform', 20, 'Formation of any two Irish landforms @ 20 marks 40 marks', 'For each landform:',
           ('Formation by processes explained @ · 20 marks each', 'Landform Named · 1 mark', 'Diagram (s)',
            'Two aspects @ · 2 marks each · 4 marks', 'Formation of landform explained',
            '5 SRPs @ · 3 marks each · 15 marks'),
           ((0, 1), (0, 2, 4), steps(15, 3))),
    '0-4', PS_SURFACE, ID + 'p2-q2b-route-i',
    routes=(
        Route('route-i', 'Route (i)', ID + 'p2-q2b-route-i', False),
        Route('route-ii', 'Route (ii)', ID + 'p2-q2b-route-ii', False,
              prompt=(L(14, '(ii) Describe and explain any two processes of mass movement.'),),
              scheme=(S(12, 'Explain any two process @ 20 marks', 'Total Marks 40'),),
              criteria=two_of('Process', 20, 'Explain any two process @ 20 marks each · 40 marks', '=For each',
                              ('Process stated · 2 marks', '6 SRPs @ · 3 marks each · 18 marks'),
                              ((0, 2), steps(18, 3))),
              topic='0-8', atlas=RW),
    )))
PART_TWO += romans('2C', P2, 14, L(14, 'Fold Mountains'), (), ID + 'p2-q2c', (), [
    ('(i)', 3, L(14, '(i) Name one fold mountain that you have studied.'),
     S(13, 'Fold mountain named', '(ii) · With the aid'),
     (fixed('Fold mountain named', 3, 'Fold mountain named · 3 marks'),), '0-2', RW + PS),
    ('(ii)', 27, L(14, '(ii) With the aid of a diagram(s), explain how fold mountains are formed.'),
     S(13, 'Diagram', 'Total Marks 30'),
     (fixed('Diagram', 6, ('=Diagram', 'Three @ 2 marks each · 6 marks'), (0, 2, 4, 6)),
      srp3('Explanation', 7, ('=Explanation', '7 SRPs @ 3 marks each · 21 marks'))), '0-2', RW + PS),
])
PART_TWO += romans('3A', P2, 15, L(15, 'Earthquakes'),
                   (L(15, 'Read the report above on the earthquake in Japan', 'answer each of the following questions.'),),
                   ID + 'p2-q3a', ('page',), [
    ('(i)', 6, L(15, '(i) What was the magnitude of the earthquake?'),
     S(14, '(i) · 8.9', '(ii) · Sendai'), (fixed('Magnitude', 6, '(i) · 8.9 · 6 marks'),), '0-7', EV),
    ('(ii)', 6, L(15, '(ii) Name the city close to the earthquake.'),
     S(14, '(ii) · Sendai', '(iii) · 15'), (fixed('City', 6, '(ii) · Sendai · 6 marks'),), '0-7', EV),
    ('(iii)', 6, L(15, '(iii) At what depth did the earthquake occur?'),
     S(14, '(iii) · 15', '(iv) · 500'), (fixed('Depth', 6, '(iii) · 15 · 6 marks'),), '0-7', EV),
    ('(iv)', 6, L(15, '(iv) What speed did the tsunami reach as it moved across the Pacific Ocean?'),
     S(14, '(iv) · 500', '(v) · Brief'), (fixed('Speed', 6, '(iv) · 500 · 6 marks'),), '0-7', EV),
    ('(v)', 6, L(15, '(v) Briefly explain how a tsunami occurs.'),
     S(14, '(v) · Brief explanation', 'Total Marks 30'),
     (srp3('Brief explanation', 2, '(v) · Brief explanation 2 SRPs @ 3 marks each · 6 marks'),), '0-7', EV),
])
PART_TWO.append(T(
    'p2-3b', P2, '3B', '', 30, 15, L(15, 'Human Interaction'),
    (L(15, 'Describe and explain how humans attempt to control one of the following surface', 'Mass movement.'),),
    (S(14, 'Control named', 'Total Marks 30'),),
    (fixed('Control named', 3, 'Control named · 3 marks'),
     srp3('Description/explanation', 9, ('Description/Explanation', '9 SRPs @ · 3 marks each · 27 marks'))),
    '0-6', RIVERS, ID + 'p2-q3b-river-processes',
    routes=bullet_routes('p2-q3b-', SURFACE, atlas=dict(zip(SURFACE, (RIVERS, SEA, RW))))))
PART_TWO += romans('3C', P2, 16, L(16, 'Karst Landscape'),
                   (L(16, 'Study the diagram of a karst landscape above and answer the following questions.'),),
                   ID + 'p2-q3c', ('page',), [
    ('(i)', 9, L(16, '(i) Name the three features marked A, B and C.'),
     S(14, 'Three named @ 3 marks each', '(ii) · Name one other'),
     (fixed('Feature A', 3, ('Three named @ 3 marks each · 9 marks', 'A · Stalactite')),
      fixed('Feature B', 3, 'B · Pillar, Column'), fixed('Feature C', 3, 'C · Swallow hole')), '0-3', KARST),
    ('(ii)', 2, L(16, '(ii) Name one other feature found in karst landscapes.'),
     S(14, 'Feature named · 2 marks', '(iii) · Explain'), (fixed('Feature named', 2, 'Feature named · 2 marks'),),
     '0-3', KARST),
    ('(iii)', 29, L(16, '(iii) Explain, with the aid of a diagram, how any one feature, in a karst region is formed.'),
     S(14, 'Naming · 2 marks', 'Total Marks 40'),
     (fixed('Feature named', 2, 'Naming · 2 marks'),
      fixed('Diagram', 6, ('=Diagram', 'Three @ 2 marks each · 6 marks'), (0, 2, 4, 6)),
      srp3('Explanation', 7, ('=Explanation', '7 SRPs @ 3 marks each · 21 mark'))), '0-3', KARST),
])

PART_TWO += [
    T('p2-4a', P2, '4A', '', 30, 17, L(17, 'Map Skills'),
      (L(17, 'Draw a sketch map of a European region', 'One named mountain range.'),),
      (S(15, 'Sketch map of region outline', 'Total Marks 30'),),
      (fixed('Outline of region', 6, 'Sketch map of region outline · 6 marks graded', upto(6)),
       Criterion('River', 6, NAMED_SHOWN, 'exact',
                 ('Mark and identify 4 items @ 6 marks each', 'River · Named · 2 marks', f'={SHOWN}@0')),
       Criterion('City 1', 6, NAMED_SHOWN, 'exact', ('City 1 · Named · 2 marks', f'={SHOWN}@1')),
       Criterion('City 2', 6, NAMED_SHOWN, 'exact', ('City 2 · Named · 2 marks', f'={SHOWN}@2')),
       Criterion('Mountain range', 6, NAMED_SHOWN, 'exact', ('Mountain range · Named · 2 marks', f'={SHOWN}@3'))),
      '1-5', EURO, ID + 'p2-q4a'),
    T('p2-4b', P2, '4B', '', 30, 17, L(17, 'Agriculture in a Continental / Sub-Continental Region'),
      (L(17, 'Explain how any two of the following influence the development of agriculture', 'Markets.'),),
      (S(16, 'Two influences explained', 'Total Marks 30'),),
      (srp3('Influence 1 explained', 5, ('Two influences explained @ · 30 marks', 'Influence 1 explained',
                                         '=5 SRPs @ · 3 marks each · 15 marks@0')),
       srp3('Influence 2 explained', 5, ('Influence 2 explained', '=5 SRPs @ · 3 marks each · 15 marks@1'))),
      '1-6', CONT, ID + 'p2-q4b', absorbs=pool(ID + 'p2-q4b-', INFLUENCES_4B, 2)[1]),
    T('p2-4c', P2, '4C', '', 40, 17, L(17, 'Economic Activities in Ireland'),
      (L(17, '• Tourism', 'Manufacturing.'),
       L(17, 'Describe the importance of any two of the above activities', 'that you have studied.')),
      (S(16, 'Naming the region', 'Total Marks 40'),),
      (fixed('Region named', 1, 'Naming the region · 1 marks'),
       srp3('Activity 1 described', 7, ('Activity 1 described', '7 SRPs @ · 3 marks each · 21 marks')),
       srp3('Activity 2 described', 6, ('Activity 2 described', '6 SRPs @ · 3 marks each · 18 marks'))),
      '1-4', IRL, ID + 'p2-q4c', absorbs=pool(ID + 'p2-q4c-', ACTIVITIES_4C, 2)[1]),
]
PART_TWO += romans('5A', P2, 18, L(18, 'Irish Tourism'),
                   (L(18, 'Examine the chart above, which shows the number of tourists visiting Ireland',
                      'answer each of the following questions.'),),
                   ID + 'p2-q5a', ('page',), [
    ('(i)', 6, L(18, '(i) In which year did the greatest number of tourists visit Ireland?'),
     S(17, '(i) · 2007', '(ii) · 2010'), (fixed('Year', 6, '(i) · 2007 · 6 marks'),), '2-0', GRAPH),
    ('(ii)', 6, L(18, '(ii) In which year did the lowest number of tourists visit Ireland?'),
     S(17, '(ii) · 2010', '(iii) · 2 million'), (fixed('Year', 6, '(ii) · 2010 · 6 marks'),), '2-0', GRAPH),
    ('(iii)', 6, L(18, '(iii) Calculate the decrease in tourist numbers from the greatest year to the lowest year.'),
     S(17, '(iii) · 2 million', '(iv) · Two attractions'), (fixed('Decrease', 6, '(iii) · 2 million · 6 marks'),),
     '2-0', GRAPH),
    ('(iv)', 6, L(18, '(iv) Name any two Irish tourist attractions.'),
     S(17, '(iv) · Two attractions', '(v) · Brief description'),
     (fixed('Two attractions', 6, '(iv) · Two attractions named @ 3 marks each · 6 marks', (0, 3, 6)),), '1-4', IRL),
    ('(v)', 6, L(18, '(v) Briefly explain why the number of tourists visiting Ireland has fallen in recent years.'),
     S(17, '(v) · Brief description', 'Total Marks 30'),
     (srp3('Brief description', 2, ('(v) · Brief description', '2 SRPs @ 3 marks each · 6 marks')),), '1-4', IRL),
])
PART_TWO += romans('5B', P2, 18, L(18, 'European Union Expansion and Ireland since 2000'), (), ID + 'p2-q5b', (), [
    ('(i)', 4, L(18, '(i) Name two countries that joined the European Union since 2004.'),
     S(17, 'Two countries named', '(ii) · Explain one positive'),
     (fixed('Two countries', 4, 'Two countries named @ 2 marks each · 4 marks', (0, 2, 4)),), '1-5', EURO + EU),
    ('(ii)', 18, L(18, '(ii) Explain one positive impact of the expansion of the European Union on Ireland.'),
     S(17, 'Impact stated', '(iii) · Explain one negative', None, '(ii) · Explain one positive'),
     (fixed('Impact stated', 3, 'Impact stated · 3 marks'),
      srp3('Explanation', 5, ('=Explained', '5 SRPs @ 3 marks each · 15 marks'))), '1-5', EURO + EU),
    ('(iii)', 18, L(18, '(iii) Explain one negative impact of the expansion of the European Union on Ireland.'),
     S(17, 'Impact stated', 'Total Marks 40', None, '(iii) · Explain one negative'),
     (fixed('Impact stated', 3, 'Impact stated · 3 marks'),
      srp3('Explanation', 5, ('=Explained', '5 SRPs @ 3 marks each · 15 marks'))), '1-5', EURO + EU),
])
PART_TWO += [
    T('p2-5c', P2, '5C', '', 30, 18, L(18, 'Urban Regions'),
      (L(18, 'Describe two reasons for the growth of an urban area in any region that you have studied.'),),
      (S(17, 'Two reasons described', 'Total Marks 30'),),
      (srp3('Reason 1', 5, ('Two reasons described · 30 marks', '=Reason 1', '=5 SRPs @ · 3 marks each · 15 marks@0')),
       srp3('Reason 2', 5, ('=Reason 2', '=5 SRPs @ · 3 marks each · 15 marks@1'))),
      '1-1', IRL + EURO + URB, ID + 'p2-q5c'),
    T('p2-6a', P2, '6A', '', 30, 19, L(19, 'Ireland - Regions'),
      (L(19, 'Draw a sketch map of Ireland.', 'One named town or city in the region.'),),
      (S(18, 'Sketch map of Ireland outline', 'Total Marks 30'),),
      (fixed('Outline of Ireland', 6, 'Sketch map of Ireland outline · 6 marks graded', upto(6)),
       Criterion('Region', 6, NAMED_SHOWN, 'exact',
                 ('Mark and identify 4 items @ 6 marks each', 'Region · Named · 2 marks', f'={SHOWN}@0')),
       Criterion('River', 6, NAMED_SHOWN, 'exact', ('River · Named · 2 marks', f'={SHOWN}@1')),
       Criterion('Mountain', 6, NAMED_SHOWN, 'exact', ('Mountain · Named · 2 marks', f'={SHOWN}@2')),
       Criterion('Town/city', 6, NAMED_SHOWN, 'exact', ('Town/City · Named · 2 marks', f'={SHOWN}@3'))),
      '1-4', IRL, ID + 'p2-q6a'),
    T('p2-6b', P2, '6B', '', 40, 19, L(19, 'European Region'),
      (L(19, 'Explain how any two of the following influence the development of manufacturing',
         'Government and European Union policies.'),),
      (S(19, 'Naming the region', 'Total Marks 40'),),
      (fixed('Region named', 1, 'Naming the region · 1 marks'),
       srp3('Influence 1 explained', 7, ('Influence 1 explained', '7 SRPs @ · 3 marks each · 21 marks')),
       srp3('Influence 2 explained', 6, ('Influence 2 explained', '6 SRPs @ · 3 marks each · 18 marks'))),
      '1-5', EURO, ID + 'p2-q6b', absorbs=pool(ID + 'p2-q6b-', INFLUENCES_6B, 2)[1]),
    T('p2-6c', P2, '6C', '', 30, 19, L(19, 'Regional Problems'),
      (L(19, 'Describe two problems faced by any region that you have studied.'),),
      (S(19, 'Two problems described', 'Total Marks 30'),),
      (fixed('Problem 1 stated', 3, ('Two problems described @ · 30 marks', '=Problem 1', '=Stated · 3 marks@0')),
       srp3('Problem 1 described', 4, '=4 SRPs @ · 3 marks each · 12 marks@0'),
       fixed('Problem 2 stated', 3, ('=Problem 2', '=Stated · 3 marks@1')),
       srp3('Problem 2 described', 4, '=4 SRPs @ · 3 marks each · 12 marks@1')),
      '1-0', IRL + EURO, ID + 'p2-q6c'),
]

PART_TWO.append(sketch(
    21, L(21, 'Aerial Photograph'),
    L(21, 'Examine the aerial photograph accompanying this paper.', 'Two connecting roads.'),
    21, ID + 'p2-q7a', '2-8', AER + ECON, ('aerial',),
    ('A marina with boats', 'An industrial area', 'A bridge', 'A car park', 'Two connecting roads.')))
Q7BI = L(21, '(i) Name one multinational company operating in Ireland and state where it is located.')
PART_TWO += romans('7B', P2, 21, L(21, 'Multinational Companies (MNC)'), (), ID + 'p2-q7b', (), [
    ('(i)', 6, Q7BI, S(22, 'MNC named', '(ii) · Describe one reason'),
     (fixed('MNC named', 2, 'MNC named · 2 marks'), fixed('MNC located', 4, 'MNC located · 4 marks')), '3-2', MNC),
    ('(ii)', 12, L(21, '(ii) Describe one reason why the multinational company named in part (i) above chose',
                   'this location.'),
     S(22, 'Reason stated', '(iii) · Name one product'),
     (fixed('Reason stated', 3, 'Reason stated · 3 marks'),
      srp3('Reason described', 3, ('Reason described', '3 SRPs @ 3 marks each · 9 marks'))), '3-2', MNC, (), (Q7BI,)),
    ('(iii)', 10, L(21, '(iii) Name one product manufactured by this multinational company and name two markets',
                    'where the product is sold.'),
     S(22, 'Product named', '(iv) · Explain two ways'),
     (fixed('Product named', 2, 'Product named · 2 marks'), fixed('Market 1 named', 4, 'Market 1 named · 4 marks'),
      fixed('Market 2 named', 4, 'Market 2 named · 4 marks')), '3-2', MNC, (), (Q7BI,)),
    ('(iv)', 12, L(21, '(iv) Explain two ways the Irish government encourages multinational companies to set',
                   'up in Ireland.'),
     S(22, 'Explanation 1', 'Total Marks 40'),
     (srp3('Explanation 1', 2, ('=Explanation 1', '=2 SRPs @ · 3 marks each · 6 marks@0')),
      srp3('Explanation 2', 2, ('=Explanation 2', '=2 SRPs @ · 3 marks each · 6 marks@1'))), '3-2', MNC),
])
Q7CI = L(21, '(i) Name one developing economy you have studied.')
PART_TWO += romans('7C', P2, 21, L(21, 'Developing Economy'), (), ID + 'p2-q7c', (), [
    ('(i)', 6, Q7CI, S(22, 'Developing economy named', '(ii) · Describe the effects'),
     (fixed('Developing economy named', 6, 'Developing economy named · 6 marks'),), '3-1', DEV),
    ('(ii)', 24, L(21, '(ii) Describe the effects of colonialism on this developing economy.'),
     S(22, 'Description of the effects', 'Total Marks 30'),
     (srp3('Description of the effects', 8, ('Description of the effects', '8 SRPs @ · 3 marks each · 24 marks')),),
     '3-1', DEV, (), (Q7CI,)),
])

PART_TWO += romans('8A', P2, 22, L(22, 'Unemployment in Ireland'),
                   (L(22, 'Examine the data above on Irish unemployment rates.'),),
                   ID + 'p2-q8a', ('page',), [
    ('(i)', 24, L(22, '(i) Using graph paper, draw a suitable graph to illustrate this data.'),
     S(23, 'Graph paper', '(ii) · In your answer book'), GRAPH_OL, '2-0', GRAPH),
    ('(ii)', 6, L(22, '(ii) In your answer book, briefly explain one reason for the rise in unemployment in',
                  'Ireland.'),
     S(23, 'Brief explanation', 'Total Marks 30'),
     (srp3('Brief explanation', 2, ('Brief explanation', '2 SRPs @ 3 marks each · 6 marks')),), '3-0', ECON),
])
Q8BS = (L(22, 'Examine the 1:50000 Ordnance Survey map and legend accompanying this paper.'),
        L(22, 'Imagine you have the task of finding a suitable location', 'for the town.'))
Q8BI = L(22, '(i) State clearly where you would locate the recycling plant using a six-figure', 'grid reference.')
PART_TWO += romans('8B', P2, 22, L(22, 'Ordnance Survey Map'), Q8BS, ID + 'p2-q8b', ('map', 'legend'), [
    ('(i)', 6, Q8BI, S(23, 'Six-figure grid reference', '(ii) · Explain one reason in favour'),
     (fixed('Six-figure grid reference', 6, 'Six-figure grid reference · 6 marks graded', upto(6)),),
     '2-6', MAP + ENV),
    ('(ii)', 24, L(22, '(ii) Explain one reason in favour of this location and explain one reason against this',
                   'location.'),
     S(23, 'Reason in favour', 'Total Marks 30'),
     (srp3('Reason in favour', 4, ('Reason in favour', '=Explaining the reason@0',
                                   '=4 SRPs @ 3 marks each · 12 marks@0')),
      srp3('Reason against', 4, ('Reason against', '=Explaining the reason@1',
                                 '=4 SRPs @ 3 marks each · 12 marks@1'))), '3-4', ENV + MAP, (), (Q8BI,)),
])
Q8CS = (L(22, '‘Many scientists believe', 'activities of people.’'),)
Q8CI = L(22, '(i) Name two causes of climate change.')
PART_TWO += romans('8C', P2, 22, L(22, 'Climate Change'), Q8CS, ID + 'p2-q8c', (), [
    ('(i)', 4, Q8CI, S(24, 'Two named @ 2 marks each', '(ii) · Explain any one'),
     (fixed('Two causes', 4, 'Two named @ 2 marks each · 4 marks', (0, 2, 4)),), '3-4', ENV),
    ('(ii)', 18, L(22, '(ii) Explain any one of the causes of climate change named in part (i).'),
     S(24, 'Explanation', '(iii) · Describe one effect'),
     (srp3('Explanation', 6, ('=Explanation', '6 SRPs @ 3 marks each · 18 marks')),), '3-4', ENV, (), (Q8CI,)),
    ('(iii)', 18, L(22, '(iii) Describe one effect of climate change on the world today.'),
     S(24, 'Description', 'Total Marks 40'),
     (srp3('Description', 6, ('=Description', '6 SRPs @ 3 marks each · 18 marks')),), '3-4', ENV),
])

Q9AIV = L(23, '(iv) From the table above, name one country that is developing.')
PART_TWO += romans('9A', P2, 23, L(23, 'Economic Development'),
                   (L(23, 'Examine the table above and answer the following questions.'),),
                   ID + 'p2-q9a', ('page',), [
    ('(i)', 6, L(23, '(i) Which country had the lowest HDI?'),
     S(25, '(i) · Niger', '(ii) · Norway'), (fixed('Country', 6, '(i) · Niger · 6 marks'),), '2-0', GRAPH + DEV),
    ('(ii)', 6, L(23, '(ii) Which country had the highest life expectancy?'),
     S(25, '(ii) · Norway', '(iii) · Niger'), (fixed('Country', 6, '(ii) · Norway · 6 marks'),), '2-0', GRAPH + DEV),
    ('(iii)', 6, L(23, '(iii) Which country had the lowest expected years of schooling?'),
     S(25, '(iii) · Niger', '(iv) · Ethiopia'), (fixed('Country', 6, '(iii) · Niger · 6 marks'),), '2-0', GRAPH + DEV),
    ('(iv)', 6, Q9AIV, S(25, '(iv) · Ethiopia', '(v) · Brief'),
     (fixed('Developing country', 6, '(iv) · Ethiopia, Niger, Pakistan · 6 marks'),), '3-1', DEV + GRAPH),
    ('(v)', 6, L(23, '(v) Briefly explain the reason for your choice of country in part (iv).'),
     S(25, '(v) · Brief explanation', 'Total Marks 30'),
     (srp3('Brief explanation', 2, ('(v) · Brief explanation', '2 SRPs @ 3 marks each · 6 marks')),),
     '3-1', DEV, (), (Q9AIV,)),
])
PART_TWO.append(T(
    'p2-9b', P2, '9B', '', 30, 23, L(23, 'Ireland and the European Union'),
    (L(23, 'The Irish economy receives funding from the European Union through the following:', 'Social Funding.'),
     L(23, 'Choose any one of the above and explain in detail how it benefits the Irish economy.')),
    (S(25, 'Explanation', 'Total Marks 30'),),
    (srp3('Explanation', 10, ('=Explanation', '10 SRPs @ · 3 marks each')),),
    '3-3', EU, ID + 'p2-q9b-common-agricultural-policy-cap', routes=bullet_routes('p2-q9b-', FUNDS)))
Q9CS = (L(23, '‘The exploitation of natural resources', 'arising between people.’'),)
Q9CI = L(23, '(i) Name an example of one such conflict that you have studied.')
PART_TWO += romans('9C', P2, 23, L(23, 'Economic Activities and Conflict'), Q9CS, ID + 'p2-q9c', (), [
    ('(i)', 4, Q9CI, S(25, 'Example named', '(ii) · Describe why'),
     (fixed('Example named', 4, 'Example named · 4 marks'),), '3-4', ENV),
    ('(ii)', 18, L(23, '(ii) Describe why this conflict has arisen.'),
     S(25, 'Description', '(iii) · Describe one possible', None, '(ii) · Describe why'),
     (srp3('Description', 6, ('=Description', '6 SRPs @ 3 marks each · 18 marks')),), '3-4', ENV, (), (Q9CI,)),
    ('(iii)', 18, L(23, '(iii) Describe one possible solution to this conflict.'),
     S(25, 'Description', 'Total Marks 40', None, '(iii) · Describe one possible'),
     (srp3('Description', 6, ('=Description', '6 SRPs @ 3 marks each · 18 marks')),), '3-4', ENV, (), (Q9CI,)),
])

PART_TWO += romans('10A', P2, 24, L(24, 'Irish Emigration'),
                   (L(24, 'Examine the data above on Irish emigration.'),),
                   ID + 'p2-q10a', ('page',), [
    ('(i)', 24, L(24, '(i) Using graph paper, draw a suitable graph to illustrate this data.'),
     S(26, 'Graph paper', '(ii)'), GRAPH_OL, '2-0', GRAPH),
    ('(ii)', 6, L(24, '(ii) In your answer book, explain one reason for the increase in emigration.'),
     S(26, 'Reason explained', 'Total Marks 30'),
     (srp3('Reason explained', 2, ('Reason explained', '2 SRPs @ 3 marks each · 6 marks')),), '4-2', POP),
])
PART_TWO.append(T(
    'p2-10b', P2, '10B', '', 40, 24, L(24, 'Development of Towns'),
    (L(24, 'Examine the aerial photograph and the 1:50000', 'accompanying this paper.'),
     L(24, 'Using the Ordnance Survey map and the aerial photograph, explain three reasons why',
       'developed at its present location.')),
    (S(26, 'Reason 1 explained', 'Total Marks 40'),),
    (srp3('Reason 1', 5, ('Reason 1 explained', '5 SRPs @ · 3 marks each · 15 marks')),
     srp3('Reason 2', 4, ('Reason 2 explained', '=4 SRPs @ · 3 marks each · 12 marks@0')),
     srp3('Reason 3', 4, ('Reason 3 explained', '=4 SRPs @ · 3 marks each · 12 marks@1')),
     fixed('Understanding of town growth', 1, 'Understanding of the concept of town growth · 1 mark')),
    '4-3', URB + MAP + AER, ID + 'p2-q10b', ('map', 'legend', 'aerial')))
PART_TWO += romans('10C', P2, 24, L(24, 'Overpopulation'), (), ID + 'p2-q10c', (), [
    ('(i)', 6, L(24, '(i) Explain the meaning of the term ‘overpopulation’.'),
     S(27, '2 SRPs @ 3 marks each · 6 marks', '(ii) · Describe in detail'),
     (srp3('Explanation', 2, '2 SRPs @ 3 marks each · 6 marks'),), '4-1', POP),
    ('(ii)', 24, L(24, '(ii) Describe in detail two problems caused by overpopulation in any region that you',
                   'have studied.'),
     S(27, 'Region named', 'Subtotal'),
     (fixed('Region named', 3, 'Region named · 3 marks'),
      srp3('Problem 1', 4, ('Two problems described', 'Problem 1 = 4 SRPs @ 3 marks each · 12 marks')),
      srp3('Problem 2', 3, 'Problem 2 = 3 SRPs @ 3 marks each · 9 marks')), '4-1', POP),
])

PART_TWO.append(sketch(
    25, L(25, 'Land-Use in Irish towns'),
    L(25, 'Examine the aerial photograph accompanying this paper.', 'A recreational (leisure) area.', nth=0),
    28, ID + 'p2-q11a', '2-8', AER + URB, ('aerial',),
    ('An unfinished building', 'A row of modern apartments', 'A main shopping street', 'A church',
     'A recreational (leisure) area.')))
Q11BI = L(25, '(i) Using the usual notation (right background etc.), give two locations', 'in Carrick-on-Shannon.')
PART_TWO += romans('11B', P2, 25, L(25, 'Traffic Problems'),
                   (L(25, 'Examine the aerial photograph accompanying this paper.', nth=1),),
                   ID + 'p2-q11b', ('aerial',), [
    ('(i)', 6, Q11BI, S(29, 'Two locations @ 3 marks each', '(ii) · Select one'),
     (fixed('Two locations', 6, 'Two locations @ 3 marks each · 6 marks each', (0, 3, 6)),), '2-8', AER + URB),
    ('(ii)', 12, L(25, '(ii) Select one of the locations chosen in part (i)', 'might occur at this location.'),
     S(29, 'Explanation', '(iii) · Examine in detail'),
     (srp3('Explanation', 4, ('=Explanation', 'Four SRPs @ 3 marks each · 12 marks')),), '4-5', URB + AER, (),
     (Q11BI,)),
    ('(iii)', 12, L(25, '(iii) Examine in detail one possible solution to this traffic congestion.'),
     S(29, 'Examination', 'Total Marks 30'),
     (srp3('Examination', 4, ('=Examination', 'Four SRPs @ 3 marks each · 12 marks')),), '4-5', URB, (),
     (Q11BI,)),
])
Q11CI = L(25, '(i) Name a developing or a developed city that you have studied.')
Q11CII = L(25, '(ii) Explain two problems arising from the growth of the city named in part (i).')
EACH_PROBLEM = ('Two problems explained · 18 marks', 'Each problem:', '3 SRPs @ 3 marks each · 9 marks')
EACH_SOLUTION = ('Two solutions explained · 18 marks', 'Each solution:', '3 SRPs @ 3 marks each · 9 marks')
PART_TWO += romans('11C', P2, 25, L(25, 'Urban Problems'), (), ID + 'p2-q11c', (), [
    ('(i)', 4, Q11CI, S(29, 'City named', '(ii) · Explain two problems'),
     (fixed('City named', 4, 'City named · 4 marks'),), '4-5', URB),
    ('(ii)', 18, Q11CII, S(29, 'Two problems explained', '(iii) · Describe two solutions'),
     (srp3('Problem 1', 3, EACH_PROBLEM), srp3('Problem 2', 3, EACH_PROBLEM)), '4-5', URB, (), (Q11CI,)),
    ('(iii)', 18, L(25, '(iii) Describe two solutions to these problems.'),
     S(29, 'Two solutions explained', 'Total Marks 40'),
     (srp3('Solution 1', 3, EACH_SOLUTION), srp3('Solution 2', 3, EACH_SOLUTION)), '4-5', URB, (), (Q11CI, Q11CII)),
])

PART_TWO += romans('12A', P2, 26, L(26, 'Ireland’s Population', nth=0),
                   (L(26, 'Examine the chart above which shows Ireland’s population from 2000 to 2010',
                      'answer each of the following questions.'),),
                   ID + 'p2-q12a', ('page',), [
    ('(i)', 6, L(26, '(i) In which year did Ireland have the lowest population?'),
     S(30, '(i) · 2000', '(ii) · 4.1 million'), (fixed('Year', 6, '(i) · 2000 · 6 marks'),), '2-0', GRAPH + POP),
    ('(ii)', 6, L(26, '(ii) What was Ireland’s population in 2004?'),
     S(30, '(ii) · 4.1 million', '(iii) · 0.7 million'), (fixed('Population', 6, '(ii) · 4.1 million · 6 marks'),),
     '2-0', GRAPH + POP),
    ('(iii)', 6, L(26, '(iii) By how much has Ireland’s population increased between 2000 and 2010?'),
     S(30, '(iii) · 0.7 million', '(iv) · Brief explanation'),
     (fixed('Increase', 6, '(iii) · 0.7 million, 700,000 · 6 marks'),), '2-0', GRAPH + POP),
    ('(iv)', 6, L(26, '(iv) Explain one reason for this increase in population.'),
     S(30, '(iv) · Brief explanation', '(v) · Brief description'),
     (srp3('Brief explanation', 2, ('(iv) · Brief explanation', '2 SRPs @ 3 marks each · 6 marks')),), '4-0', POP),
    ('(v)', 6, L(26, '(v) Describe one problem this increase in population will cause for Irish governments.'),
     S(30, '(v) · Brief description', 'Total Marks 30'),
     (srp3('Brief description', 2, ('(v) · Brief description', '2 SRPs @ 3 marks each · 6 marks')),), '4-1', POP),
])
Q12BI = L(26, '(i) Explain two causes of urban sprawl in any city that you have studied.')
PART_TWO += romans('12B', P2, 26, L(26, 'Urban Sprawl'), (), ID + 'p2-q12b', (), [
    ('(i)', 22, Q12BI, S(30, 'Named city', '(ii) · Explain two problems'),
     (fixed('City named', 1, 'Named city · 1 mark'),
      srp3('Cause 1', 4, ('Two causes explained · 21 marks', 'Cause 1 = 4 SRPs @ 3 marks each')),
      srp3('Cause 2', 3, 'Cause 2 = 3 SRPs @3 marks each')), '4-5', URB),
    ('(ii)', 18, L(26, '(ii) Explain two problems caused by this urban sprawl.'),
     S(30, 'Two problems explained', 'Total Marks 40'),
     (srp3('Problem 1', 3, ('Two problems explained · 18 marks', 'Problem 1 = 3 SRPs @ 3 marks each')),
      srp3('Problem 2', 3, 'Problem 2 = 3 SRPs @ 3 marks each')), '4-5', URB, (), (Q12BI,)),
])
PART_TWO.append(T(
    'p2-12c', P2, '12C', '', 30, 26, L(26, 'Population', nth=3),
    (L(26, '‘One of the greatest challenges facing European governments', 'with ageing populations.’'),
     L(26, 'Describe the difficulties that an ageing population can cause.')),
    (S(30, '10 SRPs @ 3 marks each · 30 marks', 'Total Marks 30'),),
    (srp3('Description of the difficulties', 10, '10 SRPs @ 3 marks each · 30 marks'),),
    '4-0', POP, ID + 'p2-q12c'))

TASKS = [*PART_ONE, *PART_TWO]

ID_CORRECTION_REASON = 'No 2012 Ordinary card shipped before this review; every card is new.'

# No 2012 Ordinary card was live on origin/main before this review.
LEGACY_IDS: list[str] = []
