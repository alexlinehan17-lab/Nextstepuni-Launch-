"""Independent review ledger: Leaving Certificate Geography 2013 Ordinary Level.

Sources (English editions, harvested Paper Trail corpus; sizes and SHA-256
pinned in EXPECTED_SOURCES and the generated audit): the examination paper
LC005GLP000EV (28 pages; one booklet printed Part One, answered in it, and
Part Two), marking scheme LC005GLP000EV (32 pages), and the common
Enniscorthy companions shared with Higher Level — the 1:50 000 map
LC005CLP003EV (a 1379 x 1936 pixel image in a one-page PDF), its legend
LC005CLPC00EV and the aerial photograph LC005CLP004EV (one-page PDFs). Part
One is 100 marks (any ten of twelve @ 10), Part Two 300 (three questions @
100).

Visual sweep (every page rendered and read on 2026-10-23):
  Paper p1 cover and examiner's grid; p2-p10 Part One Questions 1-12 (p3
  holds Q2 and Q3, p5 Q5 and Q6, p6 Q7 and Q8; Q1 prints a volcano
  diagram, Q4 a limestone pavement photograph, Q9 four photographs, Q10
  five satellite images, Q11 a weather chart, Q12 a Malin Head table);
  p11 Part Two instructions; p12 Section 1 divider; p13-p18 Q1-Q6 (p13
  and p16 open with their dividers); p19 Section 2 divider; p20-p25
  Electives Q7-Q12 (p20 and p23 open with their elective dividers); p26-
  p28 printed "Blank Page".
  Scheme p1 cover; p2 note on marking schemes; p3 note on detail
  required; p4 Geographical Investigation (coursework); p5-p7 Part One
  (Q1-Q3, Q4-Q8, Q9-Q12); p8 Part Two instructions and Section 1 divider;
  p9-p18 Q1-Q6 (p9 and p14 open with their dividers); p19 Section 2
  divider; p20-p28 Q7-Q12 (p20 and p25 open with their elective
  dividers); p29 investigation topics; p30 Irish-language bonus marks;
  p31 printed "Blank Page"; p32 back cover. The scheme reprints each Part
  Two question above its allocation; every slice starts at the
  allocation.
  Companions: Enniscorthy map extract (ENNISCORTHY / Inis Córthaidh, the
  River Slaney, Bree Hill, the N11 and N30, the railway); the OSi
  Discovery Series legend sheet; an oblique aerial photograph of
  Enniscorthy (the Slaney, the cathedral spire, the railway bridge),
  printed sideways on its page and carrying no caption — the paper names
  the town.

Part One prices every answer on its own line ("2 marks", Q5 "5 marks")
under "All Questions carry equal marks"; no heading prices a question, so
no heading line is carried. Every priced roman is a task. Q11 and Q12
print their answer lines without roman labels, one priced line per printed
blank in roman order (Q11 1020-1029, Calm, Correct symbol, Isotherms,
Isobars; Q12 January, 3 months, December, July, 9.5), so each roman is a
task. Matching tables, in the printed row order: Q1 Magma Chamber E, Vent
D, Lava A, Ash Cloud B, Crater C; Q2(i) The Giant's Causeway C, The Burren
A, Connemara B; Q2(ii) Marble Metamorphic, Basalt Igneous; Q3 Freeze Thaw
Action D, River Erosion A, Chemical Weathering E, Plucking and Abrasion C,
Deposition B; Q4(i) Clint A, Grike B; Q6(i) T 001 313 Garda
Síochana/Police, S 962 359 Moated Site, S 974 402 Railway Station, S 978
419 Industrial Estate/Third Class road; Q7(i) A meander, A car park, A
recreational area, A bridge with cars (locations); Q8 The Islamic World
B, A Département A, The Mediterranean D, The Greater Dublin Area E, The
Gaeltacht C; Q9(i) Agriculture B, Tourism C, Mining A, Industry D; Q10 A
factory burning fossil fuels B, Fjords in Norway D, Mining in the desert
E, The San Andreas Fault A, Icebergs breaking from an ice sheet C.

The 2013 scheme prints "graded" without the grades (sketch proportions,
overall impression, showing and outlines; graph axes and items), so a
graded line permits every whole mark up to its tariff, as the 2014 Higher
ledger reads its unbroken "6 items illustrated".

Tariffs as printed: twelve parts carry 40 marks (1B, 2B, 3C, 4B, 5C, 6B,
7C, 8C, 9C, 10B, 11B, 12C) and the rest 30. Every published allocation
adds up to its printed tariff, so nothing is held. 6B prints "Two factors
explained @ 20 marks each" above the lines it actually prices (region 1,
influence 1 21, influence 2 18; 40 in all); the priced lines are carded
and the heading is carried with them as printed. 11B prices three reasons
(15 + 12 + 12) and "Understanding the concept of town growth 1 mark"; its
"3 pieces of map/photo evidence (2:1 or 1:2)" carries no marks and stays an
examiner direction.

Printed choices: 3C (i) or (ii) is two routes; 1C (one of four), 2C (one
of two) and 3B (one of three) are one route per printed option; 5B, 5C
and 6B (any two of three) are pools, one card each.
"""

from geography_review import (
    Criterion, Lift, Route, SchemeSlice, Task, pool, fixed, slug, srp, steps, sums, upto,
)

YEAR = 2013
LEVEL = 'ordinary'
PAPER_PAGES = {1: 28, 2: 28}
SCHEME_PAGES = 32
_FORTY = {'1B', '2B', '3C', '4B', '5C', '6B', '7C', '8C', '9C', '10B', '11B', '12C'}
QUESTION_TARIFFS = {1: {str(n): 10 for n in range(1, 13)},
                    2: {f'{n}{x}': (40 if f'{n}{x}' in _FORTY else 30)
                        for n in range(1, 13) for x in 'ABC'}}

EXPECTED_SOURCES = {
    'paper1': ('LC005GLP000EV.pdf', 3000630),
    'paper2': ('LC005GLP000EV.pdf', 3000630),
    'scheme': ('LC005GLP000EV.pdf', 493862),
    'map': ('LC005CLP003EV.pdf', 1340745),
    'legend': ('LC005CLPC00EV.pdf', 1167773),
    'aerial': ('LC005CLP004EV.pdf', 1646330),
}

_PAPER = {1: 'cover and examiner grid', **{p: 'question' for p in range(2, 11)},
          11: 'Part Two instructions', 12: 'section divider', **{p: 'question' for p in range(13, 19)},
          19: 'section divider', **{p: 'question' for p in range(20, 26)},
          26: 'blank page', 27: 'blank page', 28: 'blank page'}
PAGE_REVIEW = {
    # One booklet printed both parts.
    'paper1': _PAPER, 'paper2': _PAPER,
    'scheme': {1: 'cover', 2: 'notes', 3: 'notes', 4: 'geographical investigation (coursework)',
               5: 'Part One table', 6: 'Part One table', 7: 'Part One table',
               8: 'Part Two instructions and section divider',
               **{p: 'Part Two allocation' for p in range(9, 19)}, 19: 'section divider',
               **{p: 'Part Two allocation' for p in range(20, 29)},
               29: 'investigation topics', 30: 'Irish-language bonus marks', 31: 'blank', 32: 'back cover'},
}

EXPECTED_SELECTION_SCAN = [
    [1, 2, 'attempt ten'], [1, 11, 'attempt three'], [1, 12, 'attempt two'],
    [1, 13, 'attempt one'], [1, 13, 'any one'],
    [1, 14, 'any two'], [1, 14, 'any two'], [1, 14, 'any one'],
    [1, 15, 'attempt to'], [1, 15, 'one of the following'], [1, 15, 'answer (i) or (ii)'],
    [1, 15, 'any two'], [1, 15, 'any two'],
    [1, 16, 'attempt one'],
    [1, 17, 'any two'], [1, 17, 'any two'], [1, 17, 'any two'],
    [1, 18, 'any two'],
    [1, 19, 'attempt one'],
]
SELECTION_REVIEW = [
    {'scan': [[1, 2, 'attempt ten'], [1, 11, 'attempt three'], [1, 12, 'attempt two'], [1, 13, 'attempt one'],
              [1, 16, 'attempt one'], [1, 19, 'attempt one']],
     'kind': 'exam-attempt-rule',
     'reason': 'Part One any ten of twelve and Part Two three questions (one of Q1-3, one of Q4-6, one elective) are attempt rules; every question is carded.'},
    {'scan': [[1, 15, 'answer (i) or (ii)']], 'kind': 'closed-route',
     'reason': '3C: (i) or (ii) -> two routes, each with its own scheme allocation.'},
    {'scan': [[1, 13, 'any one'], [1, 14, 'any one'], [1, 15, 'one of the following']], 'kind': 'closed-choose-one',
     'reason': '1C one of four printed rock-cycle activities -> 4 routes; 2C one of two printed weathering processes -> 2 routes; 3B one of three printed surface processes -> 3 routes.'},
    {'scan': [[1, 17, 'any two'], [1, 17, 'any two'], [1, 18, 'any two']], 'kind': 'choose-n-one-card',
     'reason': '5B any two of three printed influences, 5C any two of three printed activities and 6B any two of three printed influences -> one card each with every printed item (choice is not a route).'},
    {'scan': [[1, 14, 'any two'], [1, 14, 'any two'], [1, 15, 'any two'], [1, 15, 'any two'], [1, 17, 'any two']],
     'kind': 'open-response',
     'reason': 'No printed pool: 2B(i) any two sedimentary rocks and 2B(ii) any two uses; 3C(i) any two landforms and 3C(ii) any two mass movement processes (the scheme prices two @ 20 marks); 5A(iv) any two crops. Compulsory lists stay whole: 2A, 3A, 4A, 6A, 7A, 10A each item; 6C lists the cultural factors as context, not a choice.'},
    {'scan': [[1, 15, 'attempt to']], 'kind': 'not-a-selection',
     'reason': '3B "how humans attempt to control" describes human activity, not a candidate choice.'},
]

P1, P2 = 1, 2
ID = 'geography-2013-ol-'
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
TWO_SRP = '2 SRP’s @ 3 marks each · 6 marks'

# ---------------------------------------------------------------- Part One --
PART_ONE = [
    T('p1-1', P1, '1', '', 10, 2, L(2, 'Volcano'),
      (L(2, 'Match each of the letters A, B, C, D', 'in the table below.'),),
      (S(5, 'Magma Chamber · E', 'Total 10 Marks'),),
      rows(['Magma Chamber · E · 2 marks', 'Vent · D · 2 marks', 'Lava · A · 2 marks', 'Ash Cloud · B · 2 marks',
            'Crater · C · 2 marks']),
      '0-7', EV, ID + 'p1-q1', ('page',),
      row_labels=(L(2, 'Magma Chamber'), L(2, 'Vent'), L(2, 'Lava'), L(2, 'Ash Cloud'), L(2, 'Crater'))),
]
PART_ONE += romans('2', P1, 3, L(3, 'Rocks'), (), ID + 'p1-q2', ('page',), [
    ('(i)', 6, L(3, '(i) Match the name of the rock with the location most associated with it, by',
                 'in the table below.'),
     S(5, '(i) · The Giants Causeway', '(ii) · Marble'),
     rows(['(i) · The Giants Causeway · C · 2 marks', 'The Burren · A · 2 marks', 'Connemara · B · 2 marks']),
     '0-1', RW, (L(3, 'The Giant’s Causeway'), L(3, 'The Burren'), L(3, 'Connemara'))),
    ('(ii)', 4, L(3, '(ii) State whether each of following rocks is an Igneous or Sedimentary or',
                  'Metamorphic rock.'),
     S(5, '(ii) · Marble', 'Total 10 Marks'),
     rows(['(ii) · Marble · Metamorphic · 2 marks', 'Basalt · Igneous · 2 marks']), '0-1', RW,
     (L(3, 'Marble', nth=1), L(3, 'Basalt', nth=1))),
])
PART_ONE.append(T(
    'p1-3', P1, '3', '', 10, 3, L(3, 'Physical Processes'),
    (L(3, 'Match each of the features below with the', 'in the table below.'),),
    (S(5, 'Freeze Thaw Action · D', 'Total 10 Marks'),),
    rows(['Freeze Thaw Action · D · 2 marks', 'River Erosion · A · 2 marks', 'Chemical Weathering · E · 2 marks',
          'Plucking and Abrasion · C · 2 marks', 'Deposition · B · 2 marks']),
    '0-4', RW + RIVERS + SEA + GLAC, ID + 'p1-q3', ('page',),
    row_labels=(L(3, 'Freeze Thaw Action'), L(3, 'River Erosion'), L(3, 'Chemical Weathering'),
                L(3, 'Plucking and Abrasion'), L(3, 'Deposition'))))
PART_ONE += romans('4', P1, 4, L(4, 'Karst Landscape'),
                   (L(4, 'Examine the photograph above showing a section of a limestone pavement and',
                      'answer the following questions.'),),
                   ID + 'p1-q4', ('page',), [
    ('(i)', 4, L(4, '(i) Name the limestone features A and B.'),
     S(6, '(i) · Clint', '(ii) · Any valid location'),
     (fixed('Feature A', 2, '(i) · Clint · A · 2 marks'), fixed('Feature B', 2, 'Grike · B · 2 marks')), '0-3', KARST),
    ('(ii)', 2, L(4, '(ii) Name one location in Ireland where features like these are found.'),
     S(6, '(ii) · Any valid location', '(iii) · 2 named features'),
     (fixed('Location', 2, '(ii) · Any valid location · 2 marks'),), '0-3', KARST),
    ('(iii)', 4, L(4, '(iii) Name two underground features which can be found in karst regions.'),
     S(6, '(iii) · 2 named features', 'Total 10 Marks'),
     (fixed('Two underground features', 4, ('(iii) · 2 named features @ 2 marks each · 4 marks', 'Cavern/Passage/'),
            (0, 2, 4)),), '0-3', KARST),
])
PART_ONE += romans('5', P1, 5, L(5, 'Ordnance Survey Map', nth=0),
                   (L(5, 'Examine the 1:50000 Ordnance Survey map and legend accompanying this paper.', nth=0),),
                   ID + 'p1-q5', ('map', 'legend'), [
    ('(i)', 5, L(5, '(i) Imagine that you are travelling from Bree Hill', 'Write the correct answer in the box below.'),
     S(6, '(i) · North East', '(ii) · 3.4'),
     (fixed('Direction', 5, '(i) · North East/ North North East · 5 marks'),), '2-6', MAP),
    ('(ii)', 5, L(5, '(ii) Measure the length in kilometres', 'Write the correct answer in the box below.'),
     S(6, '(ii) · 3.4', 'Total 10 Marks'), (fixed('Length', 5, '(ii) · 3.4 (range 3-4 km) · 5 marks'),), '2-6', MAP),
])
PART_ONE += romans('6', P1, 5, L(5, 'Ordnance Survey Map', nth=1),
                   (L(5, 'Examine the 1:50000 Ordnance Survey map and legend accompanying this paper.', nth=1),),
                   ID + 'p1-q6', ('map', 'legend'), [
    ('(i)', 8, L(5, '(i) Name the features which can be found at each of the following grid references.'),
     S(6, '(i) · Garda', '(ii) · Correct symbol'),
     rows(['(i) · Garda', 'Moated Site · 2 marks', 'Railway Station · 2 marks',
           'Industrial Estate/Third Class road · 2 marks']), '2-6', MAP,
     (L(5, 'T 001 313'), L(5, 'S 962 359'), L(5, 'S 974 402'), L(5, 'S 978 419'))),
    ('(ii)', 2, L(5, '(ii) Draw the Ordnance Survey map symbol for a Viewpoint, in the box below.'),
     S(6, '(ii) · Correct symbol', 'Total 10 Marks'), (fixed('Symbol', 2, '(ii) · Correct symbol drawn · 2 marks'),),
     '2-6', MAP),
])
PART_ONE += romans('7', P1, 6, L(6, 'Aerial Photograph'), (), ID + 'p1-q7', ('aerial',), [
    ('(i)', 8, L(6, '(i) Examine the aerial photograph of Enniscorthy accompanying this paper.',
                 'each of the following.'),
     S(6, 'Meander:', '(ii) · Oblique'),
     rows(['Meander:', 'Car Park:', 'Recreational area:', 'A bridge with cars:']), '2-8', AER,
     (L(6, 'A meander'), L(6, 'A car park'), L(6, 'A recreational area'), L(6, 'A bridge with cars'))),
    ('(ii)', 2, L(6, '(ii) Is the aerial photograph a vertical or an oblique photograph?'),
     S(6, '(ii) · Oblique', 'Total 10 Marks'), (fixed('Type of photograph', 2, '(ii) · Oblique · 2 marks'),),
     '2-8', AER),
])
PART_ONE += [
    T('p1-8', P1, '8', '', 10, 6, L(6, 'Regions'),
      (L(6, 'Match the description of a region with the example most associated with it, by',
         'in the table below.'),),
      (S(6, 'The Islamic World · B', 'Total 10 Marks'),),
      rows(['The Islamic World · B · 2 marks', 'A Departement · A · 2 marks', 'The Mediterranean · D · 2 marks',
            'The Greater Dublin Area · E · 2 marks', 'The Gaeltacht · C · 2 marks']),
      '1-0', IRL + EURO, ID + 'p1-q8', ('page',),
      row_labels=(L(6, 'The Islamic World'), L(6, 'A Département'), L(6, 'The Mediterranean'),
                  L(6, 'The Greater Dublin Area'), L(6, 'The Gaeltacht'))),
]
PART_ONE += romans('9', P1, 7, L(7, 'Economic Activity', nth=0), (), ID + 'p1-q9', ('page',), [
    ('(i)', 8, L(7, '(i) Examine the photographs above and correctly match each of the letters on the',
                 'in the table below.'),
     S(7, '(i) · Agriculture', '(ii) · D'),
     rows(['(i) · Agriculture · B · 2 marks', 'Tourism · C · 2 marks', 'Mining · A · 2 marks',
           'Industry · D · 2 marks']), '3-0', ECON,
     (L(7, 'Agriculture'), L(7, 'Tourism'), L(7, 'Mining'), L(7, 'Industry'))),
    ('(ii)', 2, L(7, '(ii) Examine the photographs above again.', 'Write the correct letter in the box below.'),
     S(7, '(ii) · D', 'Total 10 Marks'), (fixed('Image', 2, '(ii) · D · 2 marks'),), '3-0', ECON),
])
PART_ONE.append(T(
    'p1-10', P1, '10', '', 10, 8, L(8, 'Satellite Image Interpretation'),
    (L(8, 'Match each satellite image with the most suitable description below', 'in the table.'),),
    (S(7, 'A factory burning fossil fuels', 'Total 10 Marks'),),
    rows(['A factory burning fossil fuels · B · 2 marks', 'Fjords in Norway · D · 2 marks',
          'Mining in the desert · E · 2 marks', 'The San Andreas Fault · A · 2 marks',
          'Icebergs breaking from an ice sheet C · 2 marks']),
    '2-8', AER, ID + 'p1-q10', ('page',),
    row_labels=(L(8, 'A factory burning fossil fuels.'), L(8, 'Fjords in Norway.'), L(8, 'Mining in the desert.'),
                L(8, 'The San Andreas Fault.'), L(8, 'Icebergs breaking from an ice sheet.'))))
PART_ONE += romans('11', P1, 9, L(9, 'Weather Charts'),
                   (L(9, 'Examine the weather chart above and answer the following questions.'),),
                   ID + 'p1-q11', ('page',), [
    ('(i)', 2, L(9, '(i) What is the barometric pressure (in hectopascals/millibars) to the', 'South West of Ireland?'),
     S(7, '1020-1029', 'Calm'), (fixed('Pressure', 2, '1020-1029 · 2 marks'),), '2-7', WEATHER),
    ('(ii)', 2, L(9, '(ii) According to the weather chart, what type of weather is being experienced in',
                  'Windy Calm'),
     S(7, 'Calm', 'Correct symbol'), (fixed('Type of weather', 2, 'Calm · 2 marks'),), '2-7', WEATHER),
    ('(iii)', 2, L(9, '(iii) Draw the weather chart symbol for a cold front, in the box below.'),
     S(7, 'Correct symbol', 'Isotherms'), (fixed('Symbol', 2, 'Correct symbol · 2 marks'),), '2-7', WEATHER),
    ('(iv)', 4, L(9, '(iv) Complete the following sentences by inserting the correct word from the', 'Isotherms'),
     S(7, 'Isotherms', 'Total 10 Marks'), rows(['Isotherms · 2 marks', 'Isobars · 2 marks']), '2-7', WEATHER,
     (L(9, 'Lines joining places of equal temperature on a weather chart are called'),
      L(9, 'Lines joining places of equal pressure on a weather chart are called'))),
])
PART_ONE += romans('12', P1, 10, L(10, 'Weather Statistics'),
                   (L(10, 'Examine the table above showing the mean monthly temperature and rainfall at Malin',
                      'answer the following questions.'),),
                   ID + 'p1-q12', ('page',), [
    ('(i)', 2, L(10, '(i) In which month was the lowest temperature recorded?'),
     S(7, 'January', '3 months'), (fixed('Month', 2, 'January · 2 marks'),), '2-0', GRAPH + WEATHER),
    ('(ii)', 2, L(10, '(ii) For how many months was the highest temperature recorded?'),
     S(7, '3 months', 'December'), (fixed('Months', 2, '3 months · 2 marks'),), '2-0', GRAPH + WEATHER),
    ('(iii)', 2, L(10, '(iii) Which month had the highest amount of rainfall?'),
     S(7, 'December', 'July'), (fixed('Month', 2, 'December · 2 marks'),), '2-0', GRAPH + WEATHER),
    ('(iv)', 2, L(10, '(iv) In which month was the lowest rainfall level recorded?'),
     S(7, 'July', '9.5'), (fixed('Month', 2, 'July · 2 marks'),), '2-0', GRAPH + WEATHER),
    ('(v)', 2, L(10, '(v) What was the annual mean temperature for 2011?'),
     S(7, '9.5', 'Total 10 Marks'), (fixed('Annual mean temperature', 2, '9.5 · 2 marks'),), '2-0', GRAPH + WEATHER),
])


# ---------------------------------------------------------------- Part Two --
def sketch(page, title, prompt, scheme_page, card_id, topic, atlas, sources, frame, proportions, naming, labels):
    """Five sketch items @ 5 (showing 3 graded, naming 2) and a 5-mark outline."""
    item = sums(upto(3), (0, 2))
    return T(f'p2-{card_id.rsplit("-q", 1)[1]}', P2, card_id.rsplit('-q', 1)[1].upper(), '', 30, page,
             title, (prompt,), (S(scheme_page, frame[0], 'Total Marks 30'),),
             (fixed('Limits/frame', 1, frame),
              fixed(proportions[0], 2, proportions[1], upto(2)),
              fixed('Overall impression', 2, 'Overall impression · 2 marks graded', upto(2)),
              *(Criterion(f'Item {n}', 5, item, 'exact',
                          ('Five items shown and named as follows:', 'Showing · 3 marks graded', naming))
                for n in range(1, 6))),
             topic, atlas, card_id, sources,
             row_labels=(None, None, None, *(L(page, b) for b in labels)))


def two_of(label, count, lines, unit):
    per = sums(*unit)
    return tuple(Criterion(f'{label} {n}', count, per, 'srp', lines) for n in (1, 2))


GRAPH_OL = (fixed('Graph paper', 2, 'Graph paper · 2 marks'),
            fixed('Vertical axis labelled / circle', 3, 'Vertical Axis labelled - Circle · 3 marks graded', upto(3)),
            fixed('Horizontal axis labelled / centred', 3, 'Horizontal Axis labelled - Centred · 3 marks graded',
                  upto(3)),
            fixed('4 items illustrated', 16, '4 Items @ 4 marks each graded · 16 marks', upto(16)))
ROCK = ('Quarrying', 'Mining', 'Oil/Gas exploration', 'Geothermal energy production.')
WEATHERING = ('Freeze Thaw Action', 'Carbonation.')
SURFACE = ('River processes', 'Sea processes', 'Mass movement.')
INFLUENCES_5B = ('Relief and Soils', 'Climate', 'Markets.')
SECTORS_5C = ('The type of farming practised in the region',
              'The reasons for the development of industry in the region',
              'The reasons why tourists are attracted to the region.')
INFLUENCES_6B = ('Climate', 'Relief and Soils', 'Markets.')

Q1AS = (L(13, 'Examine the diagram above and answer the following questions.'),)
PART_TWO = romans('1A', P2, 13, L(13, 'Plate Tectonics'), Q1AS, ID + 'p2-q1a', ('page',), [
    ('(i)', 6, L(13, '(i) Describe briefly how the currents at A move.'),
     S(9, 'Brief explanation', '(ii) · Name the landform', None, '(i) · Describe briefly how'),
     (srp3('Brief explanation', 2, ('Brief explanation', TWO_SRP)),), '0-0', PS),
    ('(ii)', 6, L(13, '(ii) Name the landform at B which is found on the sea floor of the Atlantic Ocean.'),
     S(9, 'Mid Atlantic Ridge', '(iii) · Are the plates'), (fixed('Landform', 6, 'Mid Atlantic Ridge · 6 marks'),),
     '0-0', PS),
    ('(iii)', 6, L(13, '(iii) Are the plates colliding or separating at C?'),
     S(9, 'Separating', '(iv) · Explain briefly'), (fixed('Colliding or separating', 6, 'Separating · 6 marks'),),
     '0-0', PS),
    ('(iv)', 6, L(13, '(iv) Explain briefly the process of subduction.'),
     S(9, 'Brief explanation', '(v) · Describe briefly', None, '(iv) · Explain briefly the process'),
     (srp3('Brief explanation', 2, ('Brief explanation', TWO_SRP)),), '0-0', PS),
    ('(v)', 6, L(13, '(v) Describe briefly the difference between lava and magma.'),
     S(9, 'Brief explanation on each one', 'Total Marks 30'),
     (fixed('Lava', 3, 'Brief explanation on each one @ 3 marks · 6 marks', (0, 3)),
      fixed('Magma', 3, 'Brief explanation on each one @ 3 marks · 6 marks', (0, 3))), '0-7', EV + PS),
])
PART_TWO += romans('1B', P2, 13, L(13, 'Earthquakes'), (), ID + 'p2-q1b', (), [
    ('(i)', 2, L(13, '(i) Name one location where an earthquake has occurred.'),
     S(9, 'Named location', '(ii) · Name a scale'), (fixed('Location named', 2, 'Named location · 2 marks'),),
     '0-7', EV),
    ('(ii)', 2, L(13, '(ii) Name a scale used to measure the force of an earthquake.'),
     S(9, 'Named scale', '(iii) · Describe how'), (fixed('Scale named', 2, 'Named scale · 2 marks'),), '0-7', EV),
    ('(iii)', 36, L(13, '(iii) Describe how earthquakes occur and describe their main effects.'),
     S(9, 'Description', 'Total Marks 40'),
     (srp3('Description', 12, ('=Description', '12 SRP’s @ 3 marks each · 36 marks')),), '0-7', EV + PS),
])
PART_TWO.append(T(
    'p2-1c', P2, '1C', '', 30, 13, L(13, 'Human Interaction with the Rock Cycle'),
    (L(13, 'Describe any one of the following examples of how humans interact with the rock cycle:',
       'Geothermal energy production.'),),
    (S(10, 'Example named', 'Total Marks 30'),),
    (fixed('Example named', 3, 'Example named · 3 marks'),
     srp3('Description', 9, '9 SRP’s @3 marks each · 27 marks')),
    '0-6', RW, ID + 'p2-q1c-quarrying', routes=bullet_routes('p2-q1c-', ROCK)))

PART_TWO += romans('2A', P2, 14, L(14, 'Mass Movement'), (), ID + 'p2-q2a', ('page',), [
    ('(i)', 24, L(14, '(i) In your answer book, match each of the following examples of mass',
                  'from the images above:'),
     S(11, '(i) · Soil Creep', '(ii) · Explain briefly'),
     rows(['(i) · Soil Creep · D · 6 marks', 'Landslide · A · 6 marks', 'Rockfall · B · 6 marks',
           'Slumping · C · 6 marks'], 6), '0-8', RW,
     (L(14, 'Soil creep'), L(14, 'Landslide'), L(14, 'Rock fall'), L(14, 'Slumping.'))),
    ('(ii)', 6, L(14, '(ii) Explain briefly what is meant by mass movement.'),
     S(11, '2 SRP’s @3 marks each', 'Total Marks 30'),
     (srp3('Brief explanation', 2, '2 SRP’s @3 marks each · 6 marks'),), '0-8', RW),
])
PART_TWO += romans('2B', P2, 14, L(14, 'Rocks'), (), ID + 'p2-q2b', (), [
    ('(i)', 4, L(14, '(i) Name any two examples of sedimentary rock.'),
     S(11, 'Two examples named', '(ii) · Name any two uses'),
     (fixed('Two examples', 4, 'Two examples named @ 2 marks each · 4 marks', (0, 2, 4)),), '0-1', RW),
    ('(ii)', 6, L(14, '(ii) Name any two uses of the sedimentary rocks named above.'),
     S(11, 'Two uses named', '(iii) · Describe how'),
     (fixed('Two uses', 6, 'Two uses named @ 3 marks each · 6 marks', (0, 3, 6)),), '0-6', RW),
    ('(iii)', 30, L(14, '(iii) Describe how sedimentary rock is formed.'),
     S(11, '10 SRP’s @ 3 marks each · 30 marks', 'Total Marks 40', None, '(iii) · Describe how sedimentary'),
     (srp3('Description', 10, '10 SRP’s @ 3 marks each · 30 marks'),), '0-1', RW),
])
PART_TWO.append(T(
    'p2-2c', P2, '2C', '', 30, 14, L(14, 'Weathering'),
    (L(14, 'Describe and explain any one of the following weathering processes that', 'Carbonation.'),),
    (S(11, 'Explaining any one weathering process', 'Total Marks 30'),),
    (srp3('Explanation', 10, ('Explaining any one weathering process', '10 SRP’s @ 3 marks each · 30 marks')),),
    '0-8', RW, ID + 'p2-q2c-freeze-thaw-action',
    routes=bullet_routes('p2-q2c-', WEATHERING, atlas=dict(zip(WEATHERING, (RW, RW + KARST))))))

PART_TWO += [
    sketch(15, L(15, 'Ordnance Survey Map'),
           L(15, 'Examine the 1:50000 Ordnance Survey map and legend accompanying this paper.',
             'The built up area of Enniscorthy.'),
           12, ID + 'p2-q3a', '2-6', MAP + RIVERS, ('map', 'legend'), ('Limits/frame · 1 mark',),
           ('Proportions', 'Proportions · 2 marks graded'), 'Naming/Identifying · 2 marks',
           ('The River Slaney', 'An area of land above 100 metres', 'A railway line', 'The N11 road',
            'The built up area of Enniscorthy.')),
    T('p2-3b', P2, '3B', '', 30, 15, L(15, 'Human Interaction'),
      (L(15, 'Describe and explain how humans attempt to control one of the following surface',
         'Mass movement.'),),
      (S(12, 'Control named', 'Total Marks 30'),),
      (fixed('Control named', 3, 'Control named · 3 marks'),
       srp3('Description/explanation', 9, ('Description/Explanation', '9 SRPs @ 3 marks each · 27 marks'))),
      '0-6', RIVERS, ID + 'p2-q3b-river-processes',
      routes=bullet_routes('p2-q3b-', SURFACE, atlas=dict(zip(SURFACE, (RIVERS, SEA, RW))))),
    T('p2-3c', P2, '3C', '', 40, 15, L(15, 'Surface Processes'),
      (L(15, '(i) Explain, with the aid of diagrams, the formation of any two landforms that you',
         'have studied.'),),
      (S(13, 'Formation of any two landforms @ 20 marks each', 'OR'),),
      two_of('Landform', 20,
             ('Formation of any two landforms @ 20 marks each', 'For each landform:',
              'Formation by processes explained @', 'Landform named · 1 mark', '=Diagram(s)',
              'Two aspects @ 2 marks each · 4 marks', 'Formation of landform explained',
              '5 SRP’s @ 3 marks each · 15 marks'),
             ((0, 1), (0, 2, 4), steps(15, 3))),
      '0-4', PS_SURFACE, ID + 'p2-q3c-route-i',
      routes=(
          Route('route-i', 'Route (i)', ID + 'p2-q3c-route-i', False),
          Route('route-ii', 'Route (ii)', ID + 'p2-q3c-route-ii', False,
                prompt=(L(15, '(ii) Describe and explain any two processes of mass movement.'),),
                scheme=(S(13, 'Explain any two process @ 20 marks each', 'Total Marks 40'),),
                criteria=two_of('Process', 20,
                                ('Explain any two process @ 20 marks each', '=For each', 'Process stated · 2 marks',
                                 '6 SRP’s @ 3 marks each · 18 marks'),
                                ((0, 2), steps(18, 3))),
                topic='0-8', atlas=RW),
      )),
]

SHOWN2 = sums((0, 2), upto(2))
ITEMS_4A = ('Region 1', 'Region 2', 'Town/City 1', 'Town/City 2', 'River 1', 'River 2')
PART_TWO.append(T(
    'p2-4a', P2, '4A', '', 30, 16, L(16, 'Contrasting Regions in Ireland'),
    (L(16, 'Draw a sketch map of Ireland.', 'A named river in each region.'),),
    (S(14, 'Sketch map of Ireland outline', 'Total Marks 30'),),
    (fixed('Outline of Ireland', 6, 'Sketch map of Ireland outline · 6 marks graded', upto(6)),
     *(Criterion(item, 4, SHOWN2, 'exact',
                 ('Mark and identify 6 items @ 4 marks graded', f'={item}', f'=Named · 2 marks@{n}',
                  f'=Shown · 2 marks graded@{n}'))
       for n, item in enumerate(ITEMS_4A))),
    '1-4', IRL, ID + 'p2-q4a'))
PART_TWO += romans('4B', P2, 16, L(16, 'European Union Expansion'), (), ID + 'p2-q4b', (), [
    ('(i)', 20, L(16, '(i) Describe the advantages of European Union expansion for Ireland.'),
     S(15, 'Naming at least one advantage', '(ii) · Describe the disadvantages'),
     (fixed('Advantage named', 2, 'Naming at least one advantage · 2 marks'),
      srp3('Advantages explained', 6, ('Advantages explained', '6 SRP’s @ 3 marks each · 18 marks'))),
     '1-5', EURO + EU),
    ('(ii)', 20, L(16, '(ii) Describe the disadvantages of European Union expansion for Ireland.'),
     S(15, 'Naming at least one disadvantage', 'Total Marks 40'),
     (fixed('Disadvantage named', 2, 'Naming at least one disadvantage · 2 marks'),
      srp3('Disadvantages explained', 6, ('Disadvantages explained', '6 SRP’s @ 3 marks each · 18 marks'))),
     '1-5', EURO + EU),
])
REASON_4C = sums((0, 2), steps(12, 3))
PART_TWO.append(T(
    'p2-4c', P2, '4C', '', 30, 16, L(16, 'European Urban Growth'),
    (L(16, 'Name one urban area in a European region (not in Ireland) that you have studied.',
       'Explain two reasons for the growth of this urban area.'),),
    (S(15, 'Naming an urban area', 'Total Marks 30'),),
    (fixed('Urban area named', 2, 'Naming an urban area · 2 marks'),
     Criterion('Reason 1', 14, REASON_4C, 'srp',
               ('Reasons for growth:', 'Reason 1 named · 2 marks', '=Explanation@0',
                '=4 SRP’s @ 3 marks each · 12 marks@0')),
     Criterion('Reason 2', 14, REASON_4C, 'srp',
               ('Reason 2 named · 2 marks', '=Explanation@1', '=4 SRP’s @ 3 marks each · 12 marks@1'))),
    '1-5', EURO + URB, ID + 'p2-q4c'))

Q5AS = (L(17, 'Examine the pie charts above showing the percentage of Ireland’s livestock, crops and',
          'the following questions.'),)
PART_TWO += romans('5A', P2, 17, L(17, 'Agricultural Production – Ireland'), Q5AS, ID + 'p2-q5a', ('page',), [
    ('(i)', 6, L(17, '(i) What percentage of Irelands’ livestock was produced in the BMW region?'),
     S(16, '(i) · 42.3%', '(ii) · South'), (fixed('Percentage', 6, '(i) · 42.3% · 6 marks'),), '2-0', GRAPH + IRL),
    ('(ii)', 6, L(17, '(ii) Which region produced the most crops?'),
     S(16, '(ii) · South', '(iii) · 20.4%'), (fixed('Region', 6, '(ii) · South & East Region · 6 marks'),),
     '2-0', GRAPH + IRL),
    ('(iii)', 6, L(17, '(iii) Calculate X, the percentage of milk produced in the BMW region.'),
     S(16, '(iii) · 20.4%', '(iv) · Any two crops'), (fixed('X', 6, '(iii) · 20.4% · 6 marks'),), '2-0', GRAPH + IRL),
    ('(iv)', 6, L(17, '(iv) Name any two crops grown in Ireland.'),
     S(16, '(iv) · Any two crops', '(v) · Brief description'),
     (fixed('Two crops', 6, '(iv) · Any two crops named @ 3 marks each · 6 marks', (0, 3, 6)),), '1-4', IRL),
    ('(v)', 6, L(17, '(v) Explain briefly why agricultural production in the South and East region was',
                 'agricultural production in the BMW region.'),
     S(16, '(v) · Brief description', 'Total Marks 30'),
     (srp3('Brief description', 2, ('(v) · Brief description', TWO_SRP)),), '1-4', IRL),
])
PART_TWO += [
    T('p2-5b', P2, '5B', '', 30, 17, L(17, 'Agriculture in Europe'),
      (L(17, 'Explain how any two of the following influence the development of agriculture in a', 'Markets.'),),
      (S(16, 'Two influences explained', 'Total Marks 30'),),
      (srp3('Influence 1 explained', 5, ('Two influences explained @ 30 marks', 'Influence 1 explained',
                                         '=5 SRP’s @ 3 marks each · 15 marks@0')),
       srp3('Influence 2 explained', 5, ('Influence 2 explained', '=5 SRP’s @ 3 marks each · 15 marks@1'))),
      '1-5', EURO, ID + 'p2-q5b', absorbs=pool(ID + 'p2-q5b-', INFLUENCES_5B, 2)[1]),
    T('p2-5c', P2, '5C', '', 40, 17, L(17, 'Economic Activities in a Continental / Sub-Continental Region'),
      (L(17, 'Name a Continental / Sub-Continental region (not in Europe) that you have studied',
         'The reasons why tourists are attracted to the region.'),),
      (S(16, 'Naming the region', 'Total Marks 40'),),
      (fixed('Region named', 1, 'Naming the region · 1 mark'),
       srp3('Sector 1 explained', 7, ('Sector 1 explained', '7 SRP’s @ 3 marks each · 21 marks')),
       srp3('Sector 2 explained', 6, ('Sector 2 explained', '6 SRP’s @ 3 marks each · 18 marks'))),
      '1-6', CONT, ID + 'p2-q5c', absorbs=pool(ID + 'p2-q5c-', SECTORS_5C, 2)[1]),
]

SHOWN4 = sums((0, 2), upto(4))
PART_TWO += [
    T('p2-6a', P2, '6A', '', 30, 18, L(18, 'Continental / Sub-Continental Region'),
      (L(18, 'Draw a sketch map of a Continental / Sub-Continental region (not in Europe) that',
         'Two named towns or cities in the region.'),),
      (S(17, 'Sketch map of region outline', 'Total Marks 30'),),
      (fixed('Outline of region', 6, 'Sketch map of region outline · 6 marks graded', upto(6)),
       Criterion('River', 6, SHOWN4, 'exact',
                 ('Mark and identify 4 items @ 6 marks graded', 'River · Named · 2 marks', '=Shown · 4 marks graded@0')),
       Criterion('Upland area', 6, SHOWN4, 'exact', ('Upland Area · Named · 2 marks', '=Shown · 4 marks graded@1')),
       Criterion('Town/City 1', 6, SHOWN4, 'exact', ('Town/City 1 · Named · 2 marks', '=Shown · 4 marks graded@2')),
       Criterion('Town/City 2', 6, SHOWN4, 'exact', ('Town/City 2 · Named · 2 marks', '=Shown · 4 marks graded@3'))),
      '1-6', CONT, ID + 'p2-q6a'),
    T('p2-6b', P2, '6B', '', 40, 18, L(18, 'Agriculture in an Irish Region'),
      (L(18, 'Explain how any two of the following influence the development of agriculture', 'Markets.'),),
      (S(17, 'Two factors explained @ 20 marks each', 'Total Marks 40'),),
      (fixed('Region named', 1, 'Naming an Irish region · 1 mark'),
       srp3('Influence 1 explained', 7, ('Two factors explained @ 20 marks each',
                                         'Influence 1 explained 7 @ 3marks each · 21 marks')),
       srp3('Influence 2 explained', 6, ('Two factors explained @ 20 marks each',
                                         'Influence 2 explained · 6 @ 3 marks each · 18 marks'))),
      '1-4', IRL, ID + 'p2-q6b', absorbs=pool(ID + 'p2-q6b-', INFLUENCES_6B, 2)[1]),
    T('p2-6c', P2, '6C', '', 30, 18, L(18, 'Cultural Regions'),
      (L(18, 'A region’s culture can be defined by the following:', 'Games.'),
       L(18, 'Describe and explain the importance of culture in any region that you have studied.')),
      (S(18, 'Naming the region', 'Total Marks 30'),),
      (fixed('Region named', 3, 'Naming the region · 3 marks'),
       srp3('Description/explanation', 9, ('Description/Explanation', '9 SRP’s @ 3 marks each · 27 marks'))),
      '1-3', IRL + EURO, ID + 'p2-q6c'),
]

SKETCH_MAP = ('Sketch Map as follows:', 'Limits/frame · 1 mark')
LANDSCAPE = ('Proportions (landscape)', 'Proportions (landscape) · 2 marks graded')
PART_TWO.append(sketch(
    20, L(20, 'Aerial Photograph'),
    L(20, 'Examine the aerial photograph accompanying this paper.', 'A river.'),
    20, ID + 'p2-q7a', '2-8', AER + ECON, ('aerial',), SKETCH_MAP, LANDSCAPE, 'Naming/identifying · 2 marks',
    ('Two connecting streets', 'An industrial area', 'An agricultural area', 'A railway bridge', 'A river.')))
PART_TWO += romans('7B', P2, 20, L(20, 'Renewable Energy'), (), ID + 'p2-q7b', (), [
    ('(i)', 6, L(20, '(i) Name two sources of renewable energy which are suitable for use in Ireland.'),
     S(21, 'Two sources named', '(ii) · Describe and explain why'),
     (fixed('Two sources', 6, 'Two sources named @ 3 marks each · 6 marks', (0, 3, 6)),), '3-5', ECON),
    ('(ii)', 24, L(20, '(ii) Describe and explain why it is important to increase the use of renewable energy.'),
     S(21, 'Described and explained', 'Total Marks 30'),
     (srp3('Description/explanation', 8, ('Described and explained', '8 SRP’s @ 3 marks each · 24 marks')),),
     '3-5', ECON + ENV),
])
Q7CII = L(20, '(ii) Name one country that was colonised.')
PART_TWO += romans('7C', P2, 20, L(20, 'Colonisation'), (), ID + 'p2-q7c', (), [
    ('(i)', 6, L(20, '(i) Explain briefly the term colonisation.'),
     S(21, 'Brief explanation', '(ii) · Name one country'),
     (srp3('Brief explanation', 2, ('Brief explanation', TWO_SRP)),), '3-1', DEV),
    ('(ii)', 4, Q7CII, S(21, 'Named country', '(iii) · Describe and explain'),
     (fixed('Country named', 4, 'Named country · 4 marks'),), '3-1', DEV),
    ('(iii)', 30, L(20, '(iii) Describe and explain the impacts of colonisation.'),
     S(21, 'Description/Explanation', 'Total Marks 40'),
     (srp3('Description/explanation', 10, ('Description/Explanation', '10 SRP’s @ 3 marks each · 30 marks')),),
     '3-1', DEV),
])

Q8AS = (L(21, 'Examine the table above showing Ireland’s main trading partners and the value',
          'the following questions.'),)
PART_TWO += romans('8A', P2, 21, L(21, 'Irish Trade'), Q8AS, ID + 'p2-q8a', ('page',), [
    ('(i)', 6, L(21, '(i) What was the total value (in millions of euro) of imports in 2011?'),
     S(22, '(i) · 49,138m', '(ii) · USA'), (fixed('Total imports', 6, '(i) · 49,138m euro · 6 Marks'),), '2-0', GRAPH),
    ('(ii)', 6, L(21, '(ii) From which of the trading partners did Ireland’s imports decrease between',
                  '2009 and 2011?'),
     S(22, '(ii) · USA', '(iii) · 18,160m'), (fixed('Trading partner', 6, '(ii) · USA · 6 marks'),), '2-0', GRAPH),
    ('(iii)', 6, L(21, '(iii) What was the value (in millions of euro) of Irish exports to the USA in 2011?'),
     S(22, '(iii) · 18,160m', '(iv) · 575m'), (fixed('Exports to the USA', 6, '(iii) · 18,160m euro · 6 marks'),),
     '2-0', GRAPH),
    ('(iv)', 6, L(21, '(iv) Calculate the increase in the value', 'USA between 2009 and 2011.'),
     S(22, '(iv) · 575m', '(v) · Brief explanation'), (fixed('Increase', 6, '(iv) · 575m euro · 6 marks'),),
     '2-0', GRAPH),
    ('(v)', 6, L(21, '(v) Explain briefly why imports and exports are important to the Irish economy.'),
     S(22, '(v) · Brief explanation', 'Total Marks 30'),
     (srp3('Brief explanation', 2, ('(v) · Brief explanation', TWO_SRP)),), '3-0', ECON),
])
REASON_8B = sums((0, 1), steps(9, 3))
PART_TWO.append(T(
    'p2-8b', P2, '8B', '', 30, 21, L(21, 'Ordnance Survey Map'),
    (L(21, 'Examine the 1:50000 Ordnance Survey map and legend accompanying this paper.'),
     L(21, 'With reference to the Ordnance Survey map, explain three reasons why tourists', 'surrounding area.')),
    (S(22, '3 reasons explained @ 10 marks each', 'Total Marks 30'),),
    (Criterion('Reason 1', 10, REASON_8B, 'srp',
               ('3 reasons explained @ 10 marks each · 30 marks', '=Reason 1', '=Stating reason · 1 mark@0',
                '=3 SRP’s @ 3 marks each · 9 marks@0')),
     Criterion('Reason 2', 10, REASON_8B, 'srp',
               ('=Reason 2', '=Stating reason · 1 mark@1', '=3 SRP’s @ 3 marks each · 9 marks@1')),
     Criterion('Reason 3', 10, REASON_8B, 'srp',
               ('=Reason 3', '=Stating reason · 1 mark@2', '3SRP’s @ 3 marks each · 9 marks'))),
    '3-0', ECON + MAP, ID + 'p2-q8b', ('map', 'legend')))
Q8CI = L(21, '(i) Name one multinational company that you have studied and state where it is', 'located.')
PART_TWO += romans('8C', P2, 21, L(21, 'Multinational Company (MNC)'), (), ID + 'p2-q8c', (), [
    ('(i)', 4, Q8CI, S(23, 'Name the MNC', '(ii) · Describe and explain'),
     (fixed('MNC named', 2, 'Name the MNC · 2 marks'), fixed('Location stated', 2, 'State location · 2 marks')),
     '3-2', MNC),
    ('(ii)', 36, L(21, '(ii) Describe and explain reasons for its present location.'),
     S(23, 'Description/Explanation', 'Total Marks 40'),
     (srp3('Description/explanation', 12, ('Description/Explanation', '12 SRP’s @ 3 marks each · 36 marks')),),
     '3-2', MNC, (), (Q8CI,)),
])

PART_TWO += romans('9A', P2, 22, L(22, 'The Irish Construction Industry'),
                   (L(22, 'Examine the data above on housing construction in Ireland between 2005 and 2011.'),),
                   ID + 'p2-q9a', ('page',), [
    ('(i)', 24, L(22, '(i) Using graph paper, draw a suitable graph to illustrate this data.'),
     S(24, 'Graph paper', '(ii) · In your answer book'), GRAPH_OL, '2-0', GRAPH),
    ('(ii)', 6, L(22, '(ii) In your answer book, explain one reason for the decrease in the number of',
                  'houses built between 2005 and 2011.'),
     S(24, 'Brief explanation', 'Total Marks 30'),
     (srp3('Brief explanation', 2, ('Brief explanation', '2 SRPs @ 3 marks each · 6 Marks')),), '3-0', ECON),
])
PART_TWO += romans('9B', P2, 22, L(22, 'Fossil Fuels'), (), ID + 'p2-q9b', (), [
    ('(i)', 6, L(22, '(i) Name two fossil fuels.'),
     S(24, 'Two named examples', '(ii) · Describe and explain the environmental'),
     (fixed('Two fossil fuels', 6, 'Two named examples @ 3 marks each · 6 marks', (0, 3, 6)),), '3-5', ECON),
    ('(ii)', 24, L(22, '(ii) Describe and explain the environmental impact of burning fossil fuels.'),
     S(24, 'Description/Explanation', 'Total Marks 30'),
     (srp3('Description/explanation', 8, ('Description/Explanation', '8 SRP’s @ 3 marks each · 24 marks')),),
     '3-4', ENV),
])
PART_TWO += romans('9C', P2, 22, L(22, 'European Union Policy'), (), ID + 'p2-q9c', (), [
    ('(i)', 20, L(22, '(i) Describe the positive impact of European Union policy on Ireland.'),
     S(24, 'Stating one positive impact', '(ii) · Describe the negative'),
     (fixed('Positive impact stated', 2, 'Stating one positive impact · 2 marks'),
      srp3('Description', 6, ('=Description', '6 SRP’s @ 3 marks each · 18 marks'))), '3-3', EU),
    ('(ii)', 20, L(22, '(ii) Describe the negative impact of European Union policy on Ireland.'),
     S(24, 'Stating one negative impact', 'Total Marks 40'),
     (fixed('Negative impact stated', 2, 'Stating one negative impact · 2 marks'),
      srp3('Description', 6, ('=Description', '6 SRP’s @ 3 marks each · 18 marks'))), '3-3', EU),
])

PART_TWO.append(sketch(
    23, L(23, 'Land-Use in Irish Towns'),
    L(23, 'Examine the aerial photograph of Enniscorthy accompanying this paper.', 'A river.', nth=0),
    25, ID + 'p2-q10a', '2-8', AER + URB, ('aerial',), SKETCH_MAP, LANDSCAPE, 'Naming/identifying · 2 marks',
    ('The Central Business District (CBD)', 'An industrial area', 'A residential area', 'A religious building',
     'A river.')))
PART_TWO += romans('10B', P2, 23, L(23, 'Migration – Rural to Urban'), (), ID + 'p2-q10b', (), [
    ('(i)', 20, L(23, '(i) Describe the push factors which contribute to migration from rural to urban', 'areas.'),
     S(26, 'Naming one push factor', '(ii) · Describe the pull'),
     (fixed('Push factor named', 2, 'Naming one push factor · 2 marks'),
      srp3('Description', 6, ('=Description', '6 SRP’s @ 3 marks each · 18 marks'))), '4-2', POP),
    ('(ii)', 20, L(23, '(ii) Describe the pull factors which contribute to migration from rural to urban', 'areas.'),
     S(26, 'Naming one pull factor', 'Total Marks 40'),
     (fixed('Pull factor named', 2, 'Naming one pull factor · 2 marks'),
      srp3('Description', 6, ('=Description', '6 SRP’s @ 3 marks each · 18 marks'))), '4-2', POP),
])
Q10CS = (L(23, 'Examine the aerial photograph of Enniscorthy accompanying this paper and answer the',
           'following questions.'),)
Q10CI = L(23, '(i) Using correct notation (right background, etc.), suggest a suitable location for',
          'a new school.')
PART_TWO += romans('10C', P2, 23, L(23, 'Aerial Photograph'), Q10CS, ID + 'p2-q10c', ('aerial',), [
    ('(i)', 3, Q10CI, S(26, 'Correct location', '(ii) · Explain three reasons'),
     (fixed('Location', 3, 'Correct location · 3 marks'),), '2-8', AER + URB),
    ('(ii)', 27, L(23, '(ii) Explain three reasons why the location you chose in part (i) would be a',
                   'suitable location for a new school.'),
     S(26, 'Reason 1 explained', 'Total Marks 30'),
     tuple(srp3(f'Reason {n}', 3, (f'Reason {n} explained', f'=3 SRP’s @ 3 marks each · 9 marks@{n - 1}'))
           for n in (1, 2, 3)), '4-4', URB + AER, (), (Q10CI,)),
])

Q11AS = (L(24, 'Examine the population pyramid for Ireland in 2011 and answer the following', 'questions.'),)
PART_TWO += romans('11A', P2, 24, L(24, 'Ireland’s Population'), Q11AS, ID + 'p2-q11a', ('page',), [
    ('(i)', 6, L(24, '(i) What percentage of the population was male and in the 0 - 4 year age group?'),
     S(27, '(i) · 4%', '(ii) · 8%'), (fixed('Percentage', 6, '(i) · 4% · 6 marks'),), '2-0', GRAPH + POP),
    ('(ii)', 6, L(24, '(ii) What percentage of the total population was in the 35 - 39 year age group?'),
     S(27, '(ii) · 8%', '(iii) · Females'), (fixed('Percentage', 6, '(ii) · 8% · 6 marks'),), '2-0', GRAPH + POP),
    ('(iii)', 6, L(24, '(iii) Were there more males or females over 75 years of age?'),
     S(27, '(iii) · Females', '(iv) · Brief explanation'), (fixed('Males or females', 6, '(iii) · Females · 6 marks'),),
     '2-0', GRAPH + POP),
    ('(iv)', 6, L(24, '(iv) Explain briefly one way the shape of this population pyramid differs from the',
                  'population pyramid for a developing country.'),
     S(27, '(iv) · Brief explanation', '(v) · Name 2 ways'),
     (srp3('Brief explanation', 2, ('(iv) · Brief explanation', TWO_SRP)),), '4-0', POP),
    ('(v)', 6, L(24, '(v) Name two ways population pyramids are used.'),
     S(27, '(v) · Name 2 ways', 'Total Marks 30'),
     (fixed('Two ways', 6, '(v) · Name 2 ways @ 3 marks each · 6 marks', (0, 3, 6)),), '4-0', POP),
])
PART_TWO += [
    T('p2-11b', P2, '11B', '', 40, 24, L(24, 'Development of Towns'),
      (L(24, 'Using evidence from the Ordnance Survey map and the aerial photograph',
         'developed at its present location.'),),
      (S(27, 'Reason 1 explained', 'Total Marks 40'),),
      (srp3('Reason 1', 5, ('Reason 1 explained', '5 SRP’s @ 3 marks each · 15 marks')),
       srp3('Reason 2', 4, ('Reason 2 explained', '=4 SRP’s @ 3 marks each · 12 marks@0')),
       srp3('Reason 3', 4, ('Reason 3 explained', '=4 SRP’s @ 3 marks each · 12 marks@1')),
       fixed('Understanding the concept of town growth', 1, 'Understanding the concept of town growth · 1 mark')),
      '4-3', URB + MAP + AER, ID + 'p2-q11b', ('map', 'legend', 'aerial')),
    T('p2-11c', P2, '11C', '', 30, 24, L(24, 'Developing World Cities'),
      (L(24, 'Describe and explain the problems caused by the rapid growth of a developing world',
         'city that you have studied.'),),
      (S(27, 'Developing world city named', 'Total Marks 30'),),
      (fixed('Developing world city named', 3, 'Developing world city named · 3 marks'),
       srp3('Problems explained', 9, ('Problems explained', '9 SRP’s @ 3 marks each · 27 marks'))),
      '4-5', URB, ID + 'p2-q11c'),
]

PART_TWO += romans('12A', P2, 25, L(25, 'Ireland’s Urban Population'),
                   (L(25, 'Examine the data showing the population of a selection of Irish towns in 2011.'),),
                   ID + 'p2-q12a', ('page',), [
    ('(i)', 24, L(25, '(i) Using graph paper, draw a suitable graph to illustrate this data.'),
     S(28, 'Graph paper', '(ii) · In your answer book'), GRAPH_OL, '2-0', GRAPH),
    ('(ii)', 6, L(25, '(ii) In your answer book, state two reasons for the growth of Irish towns.'),
     S(28, 'Reasons stated', 'Total Marks 30'),
     (srp3('Reasons stated', 2, ('Reasons stated', '2 SRPs @ 3 Marks each · 6 Marks')),), '4-3', URB),
])
PART_TWO.append(T(
    'p2-12b', P2, '12B', '', 30, 25, L(25, 'Traffic Congestion'),
    (L(25, 'Describe and explain the measures being taken in towns and cities to solve the',
       'problem of traffic congestion.'),),
    (S(28, 'Explanation of measures', 'Total Marks 30'),),
    (srp3('Explanation of measures', 10, ('Explanation of measures', '10 SRP’s @ 3 marks each · 30 marks')),),
    '4-5', URB, ID + 'p2-q12b'))
REASON_12C = sums((0, 1), steps(9, 3))
MIGRATION_REASONS = (
    Criterion('Reason 1', 10, REASON_12C, 'srp',
              ('Reason 1 stated · 1 mark', '=Explanation@0', '=3 SRP’s @ 3 marks each · 9 marks@0')),
    Criterion('Reason 2', 10, REASON_12C, 'srp',
              ('Reason 2 stated · 1 mark', '=Explanation@1', '=3 SRP’s @ 3 marks each · 9 marks@1')))
PART_TWO += romans('12C', P2, 25, L(25, 'Patterns in Migration'), (), ID + 'p2-q12c', (), [
    ('(i)', 20, L(25, '(i) Explain two reasons why people immigrated (moved in) to Ireland in recent', 'times.'),
     S(28, 'Reason 1 stated', '(ii) · Explain two reasons why people are now', None,
       '(i) · Explain two reasons why people immigrated'),
     MIGRATION_REASONS, '4-2', POP),
    ('(ii)', 20, L(25, '(ii) Explain two reasons why people are now emigrating (moving out) of Ireland',
                   'in large numbers.'),
     S(28, 'Reason 1 stated', 'Total Marks 40', None, '(ii) · Explain two reasons why people are now'),
     MIGRATION_REASONS, '4-2', POP),
])

TASKS = [*PART_ONE, *PART_TWO]

ID_CORRECTION_REASON = 'No 2013 Ordinary card shipped before this review; every card is new.'

# No 2013 Ordinary card was live on origin/main before this review.
LEGACY_IDS: list[str] = []
