"""Independent review ledger: Leaving Certificate Geography 2011 Ordinary Level.

Sources (English editions, harvested Paper Trail corpus; sizes and SHA-256
pinned in EXPECTED_SOURCES and the generated audit): the examination paper
LC005GLP000EV (32 pages; one booklet printed Part One, answered in it, and
Part Two), marking scheme LC005GLP000EV (40 pages), and the common Dingle
companions shared with Higher Level — the 1:50 000 map LC005CLP003EV (one
landscape page holding a 7016 x 4961 pixel image of the Dingle extract,
grid squares Q/V 41-53 by 98-07, with no legend on the sheet: its margin
prints only Ordnance Survey Ireland's copyright and publication notes) and
the aerial photograph LC005CLP004EV (one page holding two images: a near-
white backing image and, drawn over it, the oblique photograph of Dingle /
An Daingean, harbour in the left foreground). The SEC legend sheet for 2011
is not in Paper Trail at all, so no task here carries 'legend'. Part One is
100 marks (any ten of twelve @ 10), Part Two 300 (three questions @ 100).

Visual sweep (every page rendered and read on 2026-10-23):
  Paper p1 cover and examiner's grid; p2-p10 Part One Questions 1-12 (p3
  holds Q2 and Q3, p9 Q9 and Q10, p10 Q11 and Q12; Q1 and Q7 print four
  photographs, Q5 a weather chart, Q8 a trend graph); p11 Part Two
  instructions; p12 Section 1 divider; p13-p18 Q1-Q6 (p13 and p16 open
  with their dividers; 2A prints a plate map, 3A the rock cycle, 5A a pie
  chart, 6B four transport photographs); p19 Section 2 divider; p20-p28
  Electives Q7-Q12 (p20 and p24 open with their elective dividers; p22
  holds 8C and its pollution photographs, p24 10A's world density map, p27
  11C's four urban photographs); p29-p32 printed "Blank Page".
  Scheme p1 cover; p2 blank inside cover; p3 note on marking schemes; p4
  Geographical Investigation (coursework); p5-p7 Part One table (Q1-Q4,
  Q5-Q8, Q9-Q12); p8 Part Two instructions; p9 Section 1 divider; p10-p21
  Q1-Q6; p22 Section 2 divider; p23-p34 Q7-Q12; p35 investigation topics;
  p36 Irish-language bonus marks; p37-p38 blank but for their printed page
  numbers ("Page 35 of 36", "Page 36 of 36"); p39 blank; p40 back cover.
  The scheme reprints most Part Two questions above their allocation;
  every slice starts at the allocation.
  Companions: the Dingle map extract (Dingle Harbour / Cuan an Daingin, the
  Milltown River, the Garfinny River, the N86, the Dingle Way / Slí Chorca
  Dhuibhne, Ballysitteragh, Slievanea, Connor Hill); the oblique aerial
  photograph of Dingle. No legend sheet exists for this sitting in Paper
  Trail (LC005CLPC00EV is absent from paper-trail-corpus/exampapers/2011).

Without a legend, every task that sends the candidate to "the map and
legend" was decided part by part. Held, because answering needs a symbol
meaning only the legend defines: Part One Q11(i) (an unlabelled "P" square
and a sailing-boat pictogram), Part Two 1A (a sketch whose "A lighthouse"
is shown only by an unlabelled pictogram beside the printed words "An
Scoth Tower") and 7A (a sketch whose coniferous plantation, tourist
information centre, independent holiday hostel and ferry route are shown
only by legend symbols). Carded on the map alone (its printed names, grid,
contours, spot heights and scale): Q10(i)-(ii) (the N86 and the Dingle Way
are printed, the start and end points are given as grid references),
Q11(ii) (the strand in V 48 98 is printed "Trá Chathail"), Q11(iii)-(iv)
(grid count; the steep high ground of Slievanea at Q 50 04), Q12(iii)
(Dingle Harbour is printed) and 12B (the town printed DINGLE, its streets,
"PO", "Sch" and "Hosp." against the contoured, named uplands). The printed
stems still read "map and legend accompanying this paper"; they are lifted
verbatim.

Part One prices every answer line itself ("2 marks", "5 marks"), so no
heading line is carried. Matching tables, in the printed row order: Q1 Sea
arch B, Blowhole D, Cliff C, Beach A; Q2 Limestone B, Granite E, Sandstone
A, Basalt C, Marble D; Q3 Freeze thaw B, Soil creep C, Abrasion A,
Attrition E, Subduction D; Q7 U-Shaped valley D, Pyramidal peak A, Erratic
B, Corrie lake C; Q9 Paris Basin B, Mediterranean D, South Wales or Sambre
Meuse C (the paper sets this cell over two lines around the row letter, so
its label is the scheme's "South Wales etc."), The Burren E, Irish
Gaeltacht A; Part Two 11C(i) Cities of the future B, Urban transport C,
Urban problems D, Heritage issues A (four matches @ 3).

The 2011 scheme prints "graded" without the steps later schemes print
("2 marks graded", "6 marks graded", "4 Items @ 4 marks each graded"), so a
graded line permits every whole mark up to its maximum. 12B prints its
grid reference and map evidence "4 marks graded" in (i)-(ii) but "4 marks"
in (iii)-(iv); each part follows its own line. 11B prices "* Understanding
of the concept of migration = 1 mark" outside the romans; it is carded with
part (i), the first part that asks about migration (as 2015 4B and 6C carry
"Naming a region"). The 2C scheme reprints "Coastal Processes" where the
paper prints "Sea processes"; the routes follow the paper.

Tariffs as printed: twelve parts carry 40 marks (1B, 2B, 3B, 4B, 5C, 6B,
7B, 8C, 9B, 10B, 11B, 12B) and the rest 30. Question 5 and Question 8 put
their 40-mark part at C, not B.
"""

from geography_review import (
    Criterion, Lift, Route, SchemeSlice, Task, pool, fixed, slug, srp, steps, sums, upto,
)

YEAR = 2011
LEVEL = 'ordinary'
PAPER_PAGES = {1: 32, 2: 32}
SCHEME_PAGES = 40
_FORTY = {'1B', '2B', '3B', '4B', '5C', '6B', '7B', '8C', '9B', '10B', '11B', '12B'}
QUESTION_TARIFFS = {1: {str(n): 10 for n in range(1, 13)},
                    2: {f'{n}{x}': (40 if f'{n}{x}' in _FORTY else 30)
                        for n in range(1, 13) for x in 'ABC'}}

# No legend: the SEC legend sheet for 2011 is not in Paper Trail.
EXPECTED_SOURCES = {
    'paper1': ('LC005GLP000EV.pdf', 1469613),
    'paper2': ('LC005GLP000EV.pdf', 1469613),
    'scheme': ('LC005GLP000EV.pdf', 347448),
    'map': ('LC005CLP003EV.pdf', 2360445),
    'aerial': ('LC005CLP004EV.pdf', 726238),
}

_PAPER = {1: 'cover and examiner grid', **{p: 'question' for p in range(2, 11)},
          11: 'Part Two instructions', 12: 'section divider', **{p: 'question' for p in range(13, 19)},
          19: 'section divider', **{p: 'question' for p in range(20, 29)},
          29: 'blank page', 30: 'blank page', 31: 'blank page', 32: 'blank page'}
PAGE_REVIEW = {
    # One booklet printed both parts.
    'paper1': _PAPER, 'paper2': _PAPER,
    'scheme': {1: 'cover', 2: 'blank', 3: 'notes', 4: 'geographical investigation (coursework)',
               5: 'Part One table', 6: 'Part One table', 7: 'Part One table',
               8: 'Part Two instructions', 9: 'section divider',
               **{p: 'Part Two allocation' for p in range(10, 22)}, 22: 'section divider',
               **{p: 'Part Two allocation' for p in range(23, 35)},
               35: 'investigation topics', 36: 'Irish-language bonus marks',
               37: 'blank', 38: 'blank', 39: 'blank', 40: 'back cover'},
}

EXPECTED_SELECTION_SCAN = [
    [1, 2, 'attempt ten'], [1, 11, 'attempt three'], [1, 12, 'attempt two'],
    [1, 13, 'attempt one'], [1, 13, 'answer (i) or (ii)'], [1, 13, 'any one'], [1, 13, 'any two'],
    [1, 13, 'any two'],
    [1, 14, 'any two'], [1, 14, 'any two'], [1, 14, 'or one'], [1, 14, 'attempt to'],
    [1, 14, 'one of the following'],
    [1, 15, 'any two'],
    [1, 16, 'attempt one'], [1, 16, 'any two'], [1, 16, 'any one'],
    [1, 17, 'any two'],
    [1, 18, 'any one'],
    [1, 19, 'attempt one'],
    [1, 21, 'any two'],
    [1, 23, 'any one'],
    [1, 24, 'any one'],
    [1, 27, 'any one'],
]
SELECTION_REVIEW = [
    {'scan': [[1, 2, 'attempt ten'], [1, 11, 'attempt three'], [1, 12, 'attempt two'], [1, 13, 'attempt one'],
              [1, 16, 'attempt one'], [1, 19, 'attempt one']],
     'kind': 'exam-attempt-rule',
     'reason': 'Part One any ten of twelve and Part Two three questions (one of Q1-3, one of Q4-6, one elective) are attempt rules; every question is carded or held.'},
    {'scan': [[1, 13, 'answer (i) or (ii)']], 'kind': 'closed-route',
     'reason': '1B: (i) or (ii) -> route (ii) plus one route per printed surface process under (i), each with its own scheme allocation. 7B "tourism OR financial services" runs through all four romans -> 2 routes on each (no directive word the scan reads; the route text is anchored on the paper).'},
    {'scan': [[1, 14, 'or one']], 'kind': 'closed-route',
     'reason': '2B(i) "an igneous rock OR one example of a metamorphic rock" and 2B(iii) "igneous rocks OR metamorphic rocks" -> 2 routes on each; 2B(ii) prints no choice and stays one card.'},
    {'scan': [[1, 13, 'any one'], [1, 14, 'one of the following'], [1, 27, 'any one']], 'kind': 'closed-choose-one',
     'reason': '1B(i) any one of three printed surface processes -> 3 routes; 2C one of three printed surface processes -> 3 routes; 11C(ii) any one of the four urban issues printed in (i) -> 4 routes.'},
    {'scan': [[1, 16, 'any two'], [1, 17, 'any two']], 'kind': 'choose-n-one-card',
     'reason': '4B any two of three printed activities and 5B any two of four printed factors -> one card each with every printed item (choice is not a route).'},
    {'scan': [[1, 13, 'any two'], [1, 13, 'any two'], [1, 14, 'any two'], [1, 14, 'any two'], [1, 15, 'any two'],
              [1, 16, 'any one'], [1, 18, 'any one'], [1, 21, 'any two'], [1, 23, 'any one'], [1, 24, 'any one']],
     'kind': 'open-response',
     'reason': 'No printed pool: 1B(i) any two Irish landforms and 1B(ii) any two processes of mass movement (the scheme prices two @ 20 marks); 2A(iii) any two volcanoes and 2A(iv) any two crustal plates; 3A(v) any two ways rocks are used; 4C any one Continental / Sub-Continental region; 6B any one European region; 8A(vi) any two products; 9C(i) any one EU policy; 10A(ii) any one country in the 0-9 category. Compulsory lists stay whole: 1A, 4A, 6A, 7A, 12A each item; 6C lists cultural factors as context and 10C(ii) asks how "any of" three factors influence birth rates (one allocation, not a choose-one), so neither is a route.'},
    {'scan': [[1, 14, 'attempt to']], 'kind': 'not-a-selection',
     'reason': '2C "how humans attempt to control" describes human activity, not a candidate choice.'},
]

_NO_LEGEND = ('The SEC legend sheet (LC005CLPC00EV) was not published with the 2011 materials Paper Trail '
              'holds, and the map sheet LC005CLP003EV carries none (its margin prints only Ordnance Survey '
              'Ireland’s copyright and publication notes), so')
HELD = [
    {'part': 1, 'question': '11', 'sub': '(i)', 'title': 'Ordnance Survey Map', 'marks': 4,
     'reason': ('The paper asks "(i) Name the feature/symbol which can be found at each of the following grid '
                'references: Q 442 010 ... Q 441 005" and the scheme prices "Parking · 2 marks" and "Boating '
                'activities · 2 marks". On the map extract (rendered and read 2026-10-23) Q 442 010 is an '
                'unlabelled white "P" on a blue square at the Dingle quay and Q 441 005 an unlabelled sailing-'
                'boat pictogram in Dingle Harbour: neither is named in print, so naming them needs symbol '
                f'meanings only the Ordnance Survey legend defines. {_NO_LEGEND} part (i) is held rather than '
                'carded against evidence the card cannot show. Parts (ii)-(iv) are carded from the map alone.')},
    {'part': 2, 'question': '1A', 'title': 'Ordnance Survey Map', 'marks': 30,
     'reason': ('The paper asks for a sketch map that shows and names "• The coastline • The Milltown River • '
                'A lighthouse • A named area of land above 400 metres • A corrie lake." and the scheme prices '
                'each item "Showing = 3 marks graded" and "Naming/identifying = 2 marks" within one 30-mark '
                'allocation. Four items are answerable from the map’s printed names, contours and heights '
                '("Milltown River" is printed; the lakes and the 400 m contours are drawn), but the map prints '
                'no lighthouse: the only candidate is an unlabelled pictorial symbol on the eastern shore of '
                'the harbour mouth at about V 454 990, beside the printed words "An Scoth Tower", and only the '
                f'legend defines that symbol as a lighthouse. {_NO_LEGEND} the sketch, priced as one part, is '
                'held.')},
    {'part': 2, 'question': '7A', 'title': 'Ordnance Survey Map', 'marks': 30,
     'reason': ('The paper asks for a sketch map that shows and names "• The entire N86 National Secondary Road '
                '• The ferry route in Dingle Harbour • An area of Coniferous Plantation • A Tourist Information '
                'centre • An Independent Holiday Hostel." and the scheme prices each item "Showing = 3 marks '
                'graded" and "Naming/identifying = 2 marks" within one 30-mark allocation. Four of the five '
                'items are shown on the map only by symbols the legend defines and are named nowhere in print: '
                'the ferry route (an unlabelled black dashed line down Dingle Harbour), the coniferous '
                'plantation (unlabelled tree symbols, e.g. north of Dingle around Q 43 05), the tourist '
                'information centre (an unlabelled "i" on a green square at about Q 443 010) and the '
                f'independent holiday hostel (one of the map’s unlabelled point symbols). {_NO_LEGEND} the '
                'sketch is held.')},
]

P1, P2 = 1, 2
ID = 'geography-2011-ol-'
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


def romans(q, part, page, title, stem, first_id, sources, parts, base=None):
    """Separately priced romans. parts: (sub, marks, prompt Lift(s), scheme slice(s), criteria, topic, atlas
    [, row labels[, extra stem Lifts]]). ``base`` names the later parts' ids when the first printed part
    is held (so the first carded part keeps its own address)."""
    out = []
    base = base or first_id
    for index, item in enumerate(parts):
        sub, marks, prompt, scheme, criteria, topic, atlas = item[:7]
        labels = item[7] if len(item) > 7 else ()
        extra = item[8] if len(item) > 8 else ()
        key = sub.strip('()').replace(')(', '-')
        out.append(T(f'p{part}-{q.lower()}-{key}', part, q, sub, marks, page, title,
                     prompt if isinstance(prompt, tuple) else (prompt,),
                     scheme if isinstance(scheme, tuple) else (scheme,), criteria, topic, atlas,
                     first_id if index == 0 else f'{base}-{key}', sources, (*stem, *extra),
                     row_labels=labels))
    return out


def bullet_routes(prefix, items, atlas=None):
    return tuple(Route(slug(item, 34), item.rstrip('.'), ID + prefix + slug(item, 34), False,
                       keep_bullets=(item,), atlas=(atlas[item] if atlas else None))
                 for item in items)


def two_of(label, count, head, each, lines, unit):
    per = sums(*unit)
    return tuple(Criterion(f'{label} {n}', count, per, 'srp', (head, each, *lines)) for n in (1, 2))


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
POP = (O + 'human-population',)
URB = (O + 'human-urban-geography',)
TOTAL10 = 'Total Marks 10'

# ---------------------------------------------------------------- Part One --
PART_ONE = romans('1', P1, 2, L(2, 'Coastal Landforms'), (), ID + 'p1-q1', ('page',), [
    ('(i)', 8, L(2, '(i) Examine the photographs of coastal landforms above and correctly match each of the',
                 'in the box below.'),
     S(5, '(i) · Sea Arch', '(ii) · Beach'),
     rows(['(i) · Sea Arch · B · 2 marks', 'Blowhole · D · 2 marks', 'Cliff · C · 2 marks', 'Beach · A · 2 marks']),
     '0-10', SEA, (L(2, 'Sea arch'), L(2, 'Blowhole'), L(2, 'Cliff'), L(2, 'Beach'))),
    ('(ii)', 2, L(2, '(ii) Which of the landforms named above was formed by the process of deposition?'),
     S(5, '(ii) · Beach', TOTAL10), (fixed('Landform', 2, '(ii) · Beach · 2 marks'),), '0-10', SEA),
])
PART_ONE += [
    T('p1-2', P1, '2', '', 10, 3, L(3, 'Rocks'),
      (L(3, 'Match the description of the rock with the name of the rock', 'provided.'),),
      (S(5, 'Limestone · B', TOTAL10),),
      rows(['Limestone · B · 2 marks', 'Granite · E · 2 marks', 'Sandstone · A · 2 marks', 'Basalt · C · 2 marks',
            'Marble · D · 2 marks']),
      '0-1', RW, ID + 'p1-q2', ('page',),
      row_labels=(L(3, 'Limestone'), L(3, 'Granite'), L(3, 'Sandstone'), L(3, 'Basalt'), L(3, 'Marble'))),
    T('p1-3', P1, '3', '', 10, 3, L(3, 'Processes of the Earth'),
      (L(3, 'Match the explanation of the process with the name of the process', 'provided.'),),
      (S(5, 'Freeze thaw · B', TOTAL10),),
      rows(['Freeze thaw · B · 2 marks', 'Soil creep · C · 2 marks', 'Abrasion · A · 2 marks',
            'Attrition · E · 2 marks', 'Subduction · D · 2 marks']),
      '0-4', RW + PS, ID + 'p1-q3', ('page',),
      row_labels=(L(3, 'Freeze thaw'), L(3, 'Soil creep'), L(3, 'Abrasion'), L(3, 'Attrition'),
                  L(3, 'Subduction'))),
]
PART_ONE += romans('4', P1, 4, L(4, 'Earthquakes', nth=0),
                   (L(4, 'Study the table above and answer the following questions:'),),
                   ID + 'p1-q4', ('page',), [
    ('(i)', 2, L(4, '(i) In what year was the largest number of earthquakes of magnitude between 8.0 and 9.9?'),
     S(5, '(i) · 2007', '(ii) · 2010'), (fixed('Year', 2, '(i) · 2007 · 2 marks'),), '0-7', EV),
    ('(ii)', 2, L(4, '(ii) In what year did the greatest estimated number of deaths occur?'),
     S(5, '(ii) · 2010', '(iii) · 8'), (fixed('Year', 2, '(ii) · 2010 · 2 marks'),), '0-7', EV),
    ('(iii)', 2, L(4, '(iii) How many earthquakes of the strongest magnitude occurred over the period shown?'),
     S(5, '(iii) · 8', '(iv) · Richter'), (fixed('Number', 2, '(iii) · 8 · 2 marks'),), '0-7', EV + GRAPH),
    ('(iv)', 2, L(4, '(iv) What is the name of the scale used for measuring the strength of an earthquake?'),
     S(5, '(iv) · Richter', '(v) · True'), (fixed('Scale', 2, '(iv) · Richter or Mercalli Scale · 2 marks'),),
     '0-7', EV),
    ('(v)', 2, (L(4, '(v) Read the statement below and place an X in the correct box.'),
                L(4, '“Earthquakes occur where plates collide.”')),
     S(5, '(v) · True', TOTAL10), (fixed('True or false', 2, '(v) · True · 2 marks'),), '0-7', EV + PS),
])
PART_ONE += romans('5', P1, 5, L(5, 'Weather Charts'),
                   (L(5, 'Examine the weather chart above and answer the following questions:'),),
                   ID + 'p1-q5', ('page',), [
    ('(i)', 2, L(5, '(i) Name the type of weather front at A.'),
     S(6, '(i) · Cold Front', '(ii) · 996'), (fixed('Weather front', 2, '(i) · Cold Front · 2 marks'),),
     '2-7', WEATHER),
    ('(ii)', 2, L(5, '(ii) What is the barometric pressure over the Atlantic to the north-west of Ireland?'),
     S(6, '(ii) · 996', '(iii) · Isobars'), (fixed('Pressure', 2, '(ii) · 996 · 2 marks'),), '2-7', WEATHER),
    ('(iii)', 2, L(5, '(iii) Lines joining places of equal barometric pressure are called:', 'Isobars'),
     S(6, '(iii) · Isobars', '(iv) · True'), (fixed('Name of the lines', 2, '(iii) · Isobars · 2 marks'),),
     '2-7', WEATHER),
    ('(iv)', 2, L(5, '(iv) Read the statement and place an X in the correct box below.', 'area of high pressure.”'),
     S(6, '(iv) · True', '(v) · True'), (fixed('True or false', 2, '(iv) · True · 2 marks'),), '2-7', WEATHER),
    ('(v)', 2, L(5, '(v) Read the statement and place an X in the correct box below.', 'dry settled weather.”'),
     S(6, '(v) · True', TOTAL10), (fixed('True or false', 2, '(v) · True · 2 marks'),), '2-7', WEATHER),
])
PART_ONE += romans('6', P1, 6, L(6, 'Ireland’s Climate'),
                   (L(6, 'Examine the table above showing the monthly and annual mean temperature at Valentia',
                      'answer the following questions:'),),
                   ID + 'p1-q6', ('page',), [
    ('(i)', 2, L(6, '(i) Which month had the lowest mean temperature?'),
     S(6, '(i) · February', '(ii) · July'), (fixed('Month', 2, '(i) · February · 2 marks'),),
     '2-7', WEATHER + GRAPH),
    ('(ii)', 4, L(6, '(ii) Which two months were the warmest?'),
     S(6, '(ii) · July', '(iii) · 10.4'),
     (fixed('Month 1', 2, '(ii) · July · 2 marks'), fixed('Month 2', 2, 'August · 2 marks')),
     '2-7', WEATHER + GRAPH, (L(6, 'Month 1'), L(6, 'Month 2'))),
    ('(iii)', 2, L(6, '(iii) What was the Annual Mean temperature recorded over the period 1961 to 1990?'),
     S(6, '(iii) · 10.4', '(iv) · Cool'), (fixed('Annual mean', 2, '(iii) · 10.4 · 2 marks'),),
     '2-7', WEATHER + GRAPH),
    ('(iv)', 2, L(6, '(iv) What is the name given to Ireland’s climate type?'),
     S(6, '(iv) · Cool', TOTAL10),
     (fixed('Climate type', 2, ('(iv) · Cool Temperate Oceanic/Maritime', 'West European Type · 2 marks')),),
     '2-7', WEATHER),
])
PART_ONE += romans('7', P1, 7, L(7, 'Glacial Landforms'), (), ID + 'p1-q7', ('page',), [
    ('(i)', 8, L(7, '(i) Examine the photographs and correctly match each of the letters on the photographs',
                 'in the box below.'),
     S(6, 'U-Shaped valley', '(ii)'),
     rows(['U-Shaped valley · D · 2 marks', 'Pyramidal peak · A · 2 marks', 'Erratic · B · 2 marks',
           'Corrie lake · C · 2 marks']), '0-11', GLAC,
     (L(7, 'U-Shaped valley'), L(7, 'Pyramidal peak'), L(7, 'Erratic'), L(7, 'Corrie lake'))),
    ('(ii)', 2, L(7, '(ii) Name one way in which glacial landscapes benefit the economy', 'are found.'),
     S(6, 'Benefit Named', TOTAL10), (fixed('Benefit', 2, 'Benefit Named · 2 marks'),), '0-11', GLAC),
])
PART_ONE += romans('8', P1, 8, L(8, 'Population', nth=0),
                   (L(8, 'Examine the trend graph above and answer the following questions:'),),
                   ID + 'p1-q8', ('page',), [
    ('(i)', 2, L(8, '(i) What was the population of the world in 1960?'),
     S(6, '(i) · 3 billion', '(ii) · 6.9'), (fixed('Population', 2, '(i) · 3 billion · 2 marks'),), '4-0', POP + GRAPH),
    ('(ii)', 2, L(8, '(ii) What was the population of the world in 2010?'),
     S(6, '(ii) · 6.9', '(iii) · 3.9'), (fixed('Population', 2, '(ii) · 6.9 billion · 2 marks'),), '4-0', POP + GRAPH),
    ('(iii)', 2, L(8, '(iii) What was the increase in population between 1960 and 2010?'),
     S(6, '(iii) · 3.9', '(iv) · Reason'), (fixed('Increase', 2, '(iii) · 3.9 billion · 2 marks'),),
     '4-0', POP + GRAPH),
    ('(iv)', 2, L(8, '(iv) State one reason why population increased between 1960 and 1990.'),
     S(6, '(iv) · Reason', '(v) · Impact'), (fixed('Reason', 2, '(iv) · Reason stated · 2 marks'),), '4-0', POP),
    ('(v)', 2, L(8, '(v) State one impact of the population increase between 1960 and 1990.'),
     S(6, '(v) · Impact', TOTAL10), (fixed('Impact', 2, '(v) · Impact stated · 2 marks'),), '4-1', POP),
])
PART_ONE.append(T(
    'p1-9', P1, '9', '', 10, 9, L(9, 'Regions'),
    (L(9, 'Match the description of the region with the example of the region', 'provided.'),),
    (S(7, 'Paris Basin · B', TOTAL10),),
    (fixed('Row 1', 2, 'Paris Basin · B · 2 marks'), fixed('Row 2', 2, 'Mediterranean · D · 2 marks'),
     # The paper sets this cell over two lines around the row letter; the
     # label is the scheme's own wording for the row.
     fixed('South Wales etc.', 2, 'South Wales etc. · C · 2 marks'),
     fixed('Row 4', 2, 'The Burren · E · 2 marks'), fixed('Row 5', 2, 'Irish Gaeltacht · A · 2 marks')),
    '1-0', IRL + EURO, ID + 'p1-q9', ('page',),
    row_labels=(L(9, 'Paris Basin'), L(9, 'Mediterranean'), None, L(9, 'The Burren'), L(9, 'Irish Gaeltacht'))))
PART_ONE += romans('10', P1, 9, L(9, 'Ordnance Survey Map'),
                   (L(9, 'Examine the 1:50000 Ordnance Survey map and legend accompanying this paper.'),),
                   ID + 'p1-q10', ('map',), [
    ('(i)', 5, L(9, '(i) Measure the distance in kilometres along the N86 from the Garda Station',
                 'Write the correct answer in the box below.'),
     S(7, '(i) · 10 kms', '(ii) · North East'), (fixed('Distance', 5, '(i) · 10 kms · 5 marks'),), '2-6', MAP),
    ('(ii)', 5, L(9, '(ii) Imagine that you are hiking along the Dingle Way', 'Write the correct answer in the box below.'),
     S(7, '(ii) · North East', TOTAL10), (fixed('Direction', 5, '(ii) · North East · 5 marks'),), '2-6', MAP),
])
# Q11(i) (the "P" and sailing-boat symbols) is held: see HELD.
PART_ONE += romans('11', P1, 10, L(10, 'Ordnance Survey Map', nth=0),
                   (L(10, 'Examine the 1:50000 Ordnance Survey map and legend accompanying this paper.'),),
                   ID + 'p1-q11-ii', ('map',), [
    ('(ii)', 2, L(10, '(ii) Name the feature formed by coastal deposition in grid square V 48 98.'),
     S(7, '(ii) · Beach', '(iii) · 108'), (fixed('Feature', 2, '(ii) · Beach · 2 marks'),), '2-6', MAP + SEA),
    ('(iii)', 2, L(10, '(iii) Calculate the total area of the map in square kilometres.'),
     S(7, '(iii) · 108', '(iv) · Reason'), (fixed('Total area', 2, '(iii) · 108 or 96 – 98 sq. kms · 2 marks'),),
     '2-6', MAP),
    ('(iv)', 2, L(10, '(iv) State one reason why there is no evidence of settlement in the area at Q 50 04.'),
     S(7, '(iv) · Reason', TOTAL10), (fixed('Reason', 2, '(iv) · Reason stated · 2 marks'),), '2-6', MAP + POP),
], base=ID + 'p1-q11')
Q12T = L(10, 'Aerial Photograph and Ordnance Survey Map')
PART_ONE += [
    T('p1-12-i', P1, '12', '(i)', 6, 10, Q12T,
      (L(10, '(i) Examine the aerial photograph of Dingle/An Daingean accompanying this paper',
         'answer the following questions:'),
       L(10, 'Is the aerial photograph vertical or oblique?'),
       L(10, 'Write the location of the following, using accepted notation (right background etc.):'),
       L(10, 'A football pitch'), L(10, 'A bus depot / garage')),
      (S(7, 'Oblique · 2 marks', '(ii)'),),
      (fixed('Vertical or oblique', 2, 'Oblique · 2 marks'),
       fixed('A football pitch', 2, 'Right Foreground/Right Middleground · 2 marks'),
       fixed('A bus depot / garage', 2, 'Centre Middleground/Centre Centre · 2 marks')),
      '2-8', AER, ID + 'p1-q12', ('aerial',),
      row_labels=(None, L(10, 'A football pitch'), L(10, 'A bus depot / garage'))),
    T('p1-12-ii', P1, '12', '(ii)', 2, 10, Q12T,
      (L(10, '(ii) State one piece of evidence from the aerial photograph that suggests that Dingle/An',
         'port.'),),
      (S(7, 'Evidence stated', '(iii)'),),
      (fixed('Evidence', 2, 'Evidence stated · 2 marks'),),
      '2-8', AER, ID + 'p1-q12-ii', ('aerial',)),
    T('p1-12-iii', P1, '12', '(iii)', 2, 10, Q12T,
      (L(10, '(iii) Using both the aerial photograph and the Ordnance Survey map', 'foreground of the aerial photograph.'),),
      (S(7, 'Cuan an Daingin', TOTAL10),),
      (fixed('Area of water', 2, ('Cuan an Daingin/Dingle Harbour · 2 marks', '=An Chois')),),
      '2-8', AER + MAP, ID + 'p1-q12-iii', ('aerial', 'map')),
]


# ---------------------------------------------------------------- Part Two --
NAMED_SHOWN = sums((0, 2), upto(4))
SHOWN = '=Shown · 4 marks graded'
GRAPH_OL = (fixed('Graph paper', 2, 'Graph paper · 2 marks'),
            fixed('Vertical axis labelled / circle', 3, 'Vertical Axis labelled - Circle · 3 marks graded', upto(3)),
            fixed('Horizontal axis labelled / centred', 3, 'Horizontal Axis labelled - Centred · 3 marks graded',
                  upto(3)),
            fixed('4 items illustrated', 16, '4 Items @ 4 marks each graded · 16 marks', sums(*[upto(4)] * 4)))
STATED_EXPLAINED = sums((0, 3), steps(6, 3))
SECTOR = 'tourism OR financial services'


def sector_routes(card_id):
    return (Route('tourism', 'tourism', card_id + '-tourism', False, ((SECTOR, 'tourism'),)),
            Route('financial-services', 'financial services', card_id + '-financial-services', False,
                  ((SECTOR, 'financial services'),)))


def rock_routes(card_id, text):
    return (Route('igneous', 'igneous', card_id + '-igneous', False, ((text, 'igneous'),)),
            Route('metamorphic', 'metamorphic', card_id + '-metamorphic', False, ((text, 'metamorphic'),)))


def karst(srps):
    return (fixed('Landform named', 1, 'Landform Named = · 1 mark'),
            fixed('Diagram(s)', 2, ('=Diagram(s)', 'Two aspects @ 1 mark each · 2 marks'), upto(2)),
            srp3('Formation explained', srps,
                 ('Formation of landform explained', f'{srps} SRPs @ 3 marks each · {srps * 3} marks')))


def two_reasons(first_srps, second_srps):
    return (Criterion('Reason 1', 9, STATED_EXPLAINED, 'srp',
                      ('Reason 1 stated · 3 marks', '=Explained@0', first_srps)),
            Criterion('Reason 2', 9, STATED_EXPLAINED, 'srp',
                      ('Reason 2 stated · 3 marks', '=Explained@1', second_srps)))


SURFACE = ('River processes', 'Sea processes', 'Mass movement.')
ACTIVITIES_4B = ('The reasons why tourists are attracted to this region', 'The type of farming practiced in this region',
                 'The importance of transport in this region.')
FACTORS_5B = ('Transport', 'Raw materials', 'Markets', 'Government and EU policies.')
URBAN_ISSUES = ('Cities of the future', 'Urban transport', 'Urban problems', 'Heritage issues.')

# 1A (sketch: "A lighthouse") is held: see HELD.
PART_TWO = [
    T('p2-1b', P2, '1B', '', 40, 13, L(13, 'Surface Processes'),
      (L(13, '(i) Select any one of the following surface processes:', 'Glacial action.'),
       L(13, 'Explain with the aid of a diagram(s) the formation of any two Irish landforms', 'selected process.')),
      (S(11, 'Formation of any two Irish landforms @ 20 marks', 'OR'),),
      two_of('Landform', 20, 'Formation of any two Irish landforms @ 20 marks', 'For each landform:',
             ('Formation by processes explained @ · 20 marks each', 'Landform Named = · 1 mark', 'Diagram (s)',
              'Two aspects @ 2 marks each · 4 marks', 'Formation of landform explained',
              '5 SRPs @ 3 marks each · 15 marks'),
             ((0, 1), (0, 2, 4), steps(15, 3))),
      '0-10', SEA, ID + 'p2-q1b-route-i-marine-action',
      routes=(
          Route('route-i-marine-action', 'Route (i) · Marine action', ID + 'p2-q1b-route-i-marine-action', False,
                keep_bullets=('Marine action',), topic='0-10', atlas=SEA),
          Route('route-i-river-action', 'Route (i) · River action', ID + 'p2-q1b-route-i-river-action', False,
                keep_bullets=('River action',), topic='0-9', atlas=RIVERS),
          Route('route-i-glacial-action', 'Route (i) · Glacial action', ID + 'p2-q1b-route-i-glacial-action', False,
                keep_bullets=('Glacial action.',), topic='0-11', atlas=GLAC),
          Route('route-ii', 'Route (ii)', ID + 'p2-q1b-route-ii', False,
                prompt=(L(13, '(ii) Describe and explain any two processes of mass movement.'),),
                scheme=(S(11, 'Explain any two processes @ 20 marks', 'Total Marks 40'),),
                criteria=two_of('Process', 20, 'Explain any two processes @ 20 marks each', 'For each process:',
                                ('Process stated = · 2 marks', '6 SRPs @ 3 marks each · 18 marks'),
                                ((0, 2), steps(18, 3))),
                topic='0-8', atlas=RW),
      )),
    T('p2-1c', P2, '1C', '', 30, 13, L(13, 'Volcanoes'),
      (L(13, 'Explain, with the aid of a diagram(s), how volcanic eruptions occur.'),),
      (S(11, 'Diagram', 'Total Marks 30', None, 'C. · Volcanoes'),),
      (fixed('Diagram', 6, ('=Diagram', 'Three @ 2 marks each · 6 marks'), (0, 2, 4, 6)),
       srp3('Explanation', 8, ('=Explanation', '8 SRPs @ 3 marks each · 24 marks'))),
      '0-7', EV, ID + 'p2-q1c'),
]
PART_TWO += romans('2A', P2, 14, L(14, 'Plate Tectonics'),
                   (L(14, 'Examine the map above and answer the following questions:'),),
                   ID + 'p2-q2a', ('page',), [
    ('(i)', 4, L(14, '(i) What is the name given to the region from X1, along the shaded line,', 'to X2?'),
     S(12, '(i) · Pacific Ring of Fire', '(ii) · Mid Atlantic'),
     (fixed('Region', 4, '(i) · Pacific Ring of Fire · 4 marks'),), '0-0', PS + EV),
    ('(ii)', 4, L(14, '(ii) Name the ridge running north from Y.'),
     S(12, '(ii) · Mid Atlantic', '(iii) · Volcano 1'), (fixed('Ridge', 4, '(ii) · Mid Atlantic Ridge · 4 marks'),),
     '0-0', PS),
    ('(iii)', 8, L(14, '(iii) Name any two volcanoes.'),
     S(12, '(iii) · Volcano 1', '(iv) · Plate 1'),
     (fixed('Volcano 1', 4, '(iii) · Volcano 1 named · 4 marks'), fixed('Volcano 2', 4, 'Volcano 2 named · 4 marks')),
     '0-7', EV),
    ('(iv)', 8, L(14, '(iv) Name any two crustal plates.'),
     S(12, '(iv) · Plate 1', '(v) · Brief'),
     (fixed('Plate 1', 4, '(iv) · Plate 1 · 4 marks'), fixed('Plate 2', 4, 'Plate 2 · 4 marks')), '0-0', PS),
    ('(v)', 6, L(14, '(v) Briefly explain what is meant by subduction.'),
     S(12, '(v) · Brief', 'Total Marks 30'),
     (srp3('Brief explanation', 2, ('(v) · Brief explanation', '2 SRPs @ 3 marks each · 6 marks')),), '0-0', PS),
])
ROCK_I = 'an igneous rock OR one example of a metamorphic rock'
ROCK_III = 'igneous rocks OR metamorphic rocks'
Q2BI = L(14, '(i) Name one example of an igneous rock OR one example of a metamorphic rock.')
PART_TWO += [
    T('p2-2b-i', P2, '2B', '(i)', 2, 14, L(14, 'Rocks'), (Q2BI,),
      (S(12, 'Rock named', '(ii) · Name a specific'),),
      (fixed('Rock named', 2, 'Rock named · 2 marks'),),
      '0-1', RW, ID + 'p2-q2b-igneous', routes=rock_routes(ID + 'p2-q2b', ROCK_I)),
    T('p2-2b-ii', P2, '2B', '(ii)', 2, 14, L(14, 'Rocks'),
      (L(14, '(ii) Name a specific location in Ireland where the rock you named above is found.'),),
      (S(12, 'Location named', '(iii) · Describe'),),
      (fixed('Location named', 2, 'Location named · 2 marks'),),
      '0-1', RW + IRL, ID + 'p2-q2b-ii', stem=(Q2BI,)),
    T('p2-2b-iii', P2, '2B', '(iii)', 36, 14, L(14, 'Rocks'),
      (L(14, '(iii) Describe how igneous rocks OR metamorphic rocks are formed.'),),
      (S(12, '12 SRPs', 'Total Marks 40'),),
      (srp3('Description', 12, '12 SRPs @ 3 marks each · 36 marks graded'),),
      '0-1', RW, ID + 'p2-q2b-iii-igneous', routes=rock_routes(ID + 'p2-q2b-iii', ROCK_III)),
    T('p2-2c', P2, '2C', '', 30, 14, L(14, 'Human Interaction'),
      (L(14, 'Describe and explain how humans attempt to control one of the following surface processes:',
         'Mass movement.'),),
      (S(13, 'Control named', 'Total Marks 30'),),
      (fixed('Control named', 3, 'Control named = · 3 marks'),
       srp3('Way explained/described', 9, ('Way explained/described', '9 SRPs @ 3 marks each · 27 marks'))),
      '0-6', RIVERS, ID + 'p2-q2c-river-processes',
      routes=bullet_routes('p2-q2c-', SURFACE, atlas=dict(zip(SURFACE, (RIVERS, SEA, RW))))),
]
PART_TWO += romans('3A', P2, 15, L(15, 'Rock Cycle'),
                   (L(15, 'Examine the diagram of the rock cycle above and answer each of the following questions:'),),
                   ID + 'p2-q3a', ('page',), [
    ('(i)', 6, L(15, '(i) Name the category of rock formed at X.'),
     S(14, '(i) · Igneous', '(ii) · Named example'), (fixed('Category X', 6, '(i) · Igneous · 6 marks'),), '0-1', RW),
    ('(ii)', 6, L(15, '(ii) Give an example of the category of rock formed at X.'),
     S(14, '(ii) · Named example', '(iii) · Sedimentary'), (fixed('Example', 6, '(ii) · Named example · 6 marks'),),
     '0-1', RW),
    ('(iii)', 6, L(15, '(iii) Name the category of rock formed at Y.'),
     S(14, '(iii) · Sedimentary', '(iv) · Named example'), (fixed('Category Y', 6, '(iii) · Sedimentary · 6 marks'),),
     '0-1', RW),
    ('(iv)', 6, L(15, '(iv) Give an example of the category of rock formed at Y.'),
     S(14, '(iv) · Named example', '(v) · Use 1'), (fixed('Example', 6, '(iv) · Named example · 6 marks'),),
     '0-1', RW),
    ('(v)', 6, L(15, '(v) Name any two ways rocks are used.'),
     S(14, '(v) · Use 1', 'Total Marks 30'),
     (fixed('Use 1', 3, '(v) · Use 1 · 3 marks'), fixed('Use 2', 3, 'Use 2 · 3 marks')), '0-6', RW),
])
PART_TWO += romans('3B', P2, 15, L(15, 'Karst Landscape - Limestone'), (), ID + 'p2-q3b', (), [
    ('(i)', 1, L(15, '(i) Name an example of a Karst region in Ireland.'),
     S(14, 'One named example in Ireland', '(ii) · Explain'),
     (fixed('Karst region named', 1, 'One named example in Ireland · 1 mark'),), '0-3', KARST + IRL),
    ('(ii)', 21, L(15, '(ii) Explain, with the aid of a diagram(s), how one surface feature in a Karst region is',
                   'formed.'),
     S(14, 'Landform Named', '(Sub-total 21)', None, 'one surface feature'), karst(6), '0-3', KARST),
    ('(iii)', 18, L(15, '(iii) Explain, with the aid of a diagram(s), how one underground feature, in a Karst',
                    'formed.'),
     S(14, 'Landform Named', '(Sub-total 18)', None, 'one underground feature'), karst(5), '0-3', KARST),
])
PART_TWO.append(T(
    'p2-3c', P2, '3C', '', 30, 15, L(15, 'Plate Tectonics'),
    (L(15, 'Describe and explain what happens at plate boundaries.'),),
    (S(15, 'Describing and explaining', 'Total Marks 30'),),
    (srp3('Description and explanation', 10,
          ('Describing and explaining = · 30 marks', '10 SRPs @ 3 marks each · 30 marks')),),
    '0-0', PS, ID + 'p2-q3c'))

PART_TWO += [
    T('p2-4a', P2, '4A', '', 30, 16, L(16, 'Ireland – Regions'),
      (L(16, 'Draw a sketch map of Ireland.', 'One named mountain range.'),),
      (S(16, 'Sketch map of Ireland outline', 'Total Marks 30'),),
      (fixed('Outline of Ireland', 6, 'Sketch map of Ireland outline = · 6 marks graded', upto(6)),
       Criterion('Region 1', 6, NAMED_SHOWN, 'exact',
                 ('Mark and identify 4 items @ 6 marks each', 'Region 1 named · Named · 2 marks', f'{SHOWN}@0')),
       Criterion('Region 2', 6, NAMED_SHOWN, 'exact', ('Region 2 named · Named · 2 marks', f'{SHOWN}@1')),
       Criterion('River', 6, NAMED_SHOWN, 'exact', ('Named river · Named · 2 marks', f'{SHOWN}@2')),
       Criterion('Mountain range', 6, NAMED_SHOWN, 'exact', ('Mountain range · Named · 2 marks', f'{SHOWN}@3'))),
      '1-4', IRL, ID + 'p2-q4a'),
    T('p2-4b', P2, '4B', '', 40, 16, L(16, 'Economic Activity – Irish Region'),
      (L(16, 'Name an Irish region you have studied and explain any two of the following:',
         'The importance of transport in this region.'),),
      (S(16, 'Naming the region', 'Total Marks 40'),),
      (fixed('Region named', 1, 'Naming the region · 1 mark'),
       srp3('Activity 1 explained', 7, ('Activity 1 explained', '7 SRPs @ 3 marks each · 21 marks')),
       srp3('Activity 2 explained', 6, ('Activity 2 explained', '6 SRPs @ 3 marks each · 18 marks'))),
      '1-4', IRL, ID + 'p2-q4b', absorbs=pool(ID + 'p2-q4b-', ACTIVITIES_4B, 2)[1]),
    T('p2-4c', P2, '4C', '', 30, 16, L(16, 'Continental / Sub-Continental Regions'),
      (L(16, 'Describe the development of manufacturing industry in any one',
         'Clearly state the name of the region in your answer.'),),
      (S(17, 'Naming the region', 'Total Marks 30'),),
      (fixed('Region named', 3, 'Naming the region · 3 marks'),
       srp3('Description', 9, ('Describing the development of manufacturing industry',
                               '9 SRPs @ 3 marks each · 27 marks'))),
      '1-6', CONT, ID + 'p2-q4c'),
]
PART_TWO += romans('5A', P2, 17, L(17, 'Irish Agriculture'),
                   (L(17, 'Examine the chart above and answer each of the following questions:'),),
                   ID + 'p2-q5a', ('page',), [
    ('(i)', 5, L(17, '(i) What percentage of agricultural land was used for the production of hay in 2000?'),
     S(18, '(i) · 6%', '(ii) · 11%'), (fixed('Percentage', 5, '(i) · 6% · 5 marks'),), '2-0', GRAPH),
    ('(ii)', 5, L(17, '(ii) Calculate X, the percentage of agricultural land used for rough grazing in 2000.'),
     S(18, '(ii) · 11%', '(iii) · 74%'), (fixed('X', 5, '(ii) · 11% · 5 marks'),), '2-0', GRAPH),
    ('(iii)', 5, L(17, '(iii) What total percentage of agricultural land was used for the production of pasture and',
                   'silage combined?'),
     S(18, '(iii) · 74%', '(iv) · Crop named'), (fixed('Total percentage', 5, '(iii) · 74% · 5 marks'),), '2-0', GRAPH),
    ('(iv)', 3, L(17, '(iv) Name one crop, not named in the chart above, that is grown in Ireland.'),
     S(18, '(iv) · Crop named', '(v) · Brief'), (fixed('Crop named', 3, '(iv) · Crop named · 3 marks'),), '1-4', IRL),
    ('(v)', 12, L(17, '(v) Give a brief description of pastoral farming.'),
     S(18, '(v) · Brief', 'Total Marks 30'),
     (srp3('Brief description', 4, ('(v) · Brief description of pastoral farming', '4 SRPs @ 3 marks each · 12 marks')),),
     '1-4', IRL),
])
PART_TWO += [
    T('p2-5b', P2, '5B', '', 30, 17, L(17, 'Manufacturing Industry in Ireland'),
      (L(17, 'Explain how any two of the following influence the development of manufacturing',
         'Government and EU policies.'),
       L(17, 'Clearly state the name of the region in your answer.', nth=0)),
      (S(18, 'Naming the region', 'Total Marks 30'),),
      (fixed('Region named', 3, 'Naming the region · 3 marks'),
       srp3('Factor 1 explained', 5, ('Two factors explained @ · 27 marks', 'Factor 1 explained',
                                      '5 SRPs @ 3 marks each · 15 marks')),
       srp3('Factor 2 explained', 4, ('Factor 2 explained', '4 SRPs @ 3 marks each · 12 marks'))),
      '1-4', IRL, ID + 'p2-q5b', absorbs=pool(ID + 'p2-q5b-', FACTORS_5B, 2)[1]),
    T('p2-5c', P2, '5C', '', 40, 17, L(17, 'Agriculture in Europe'),
      (L(17, 'Explain how physical and economic factors influence the development of agriculture',
         'Clearly state the name of the region in your answer.'),),
      (S(19, 'Naming the region', 'Total Marks 40'),),
      (fixed('Region named', 4, 'Naming the region · 4 marks'),
       srp3('Physical factors explained', 6,
            ('Physical factors explained', '=6 SRPs @ 3 marks each · 18 marks@0')),
       srp3('Economic factors explained', 6,
            ('Economic factors explained', '=6 SRPs @ 3 marks each · 18 marks@1'))),
      '1-5', EURO, ID + 'p2-q5c'),
    T('p2-6a', P2, '6A', '', 30, 18, L(18, 'Continental / Sub-Continental Region'),
      (L(18, 'Draw a sketch map of a Continental / Sub-Continental region', 'One named mountain range.'),),
      (S(20, 'Sketch map of region outline', 'Total Marks 30'),),
      (fixed('Outline of region', 6, 'Sketch map of region outline = · 6 marks graded', upto(6)),
       Criterion('City 1', 6, NAMED_SHOWN, 'exact',
                 ('Mark and identify 4 items @ 6 marks each', 'City 1 named · Named · 2 marks', f'{SHOWN}@0')),
       Criterion('City 2', 6, NAMED_SHOWN, 'exact', ('City 2 named · Named · 2 marks', f'{SHOWN}@1')),
       Criterion('River', 6, NAMED_SHOWN, 'exact', ('Named river · Named · 2 marks', f'{SHOWN}@2')),
       Criterion('Mountain range', 6, NAMED_SHOWN, 'exact', ('Mountain range · Named · 2 marks', f'{SHOWN}@3'))),
      '1-6', CONT, ID + 'p2-q6a'),
    T('p2-6b', P2, '6B', '', 40, 18, L(18, 'European Regions – Transport'),
      (L(18, 'Describe the development of transport in any one European region',
         'Clearly state the name of the region in your answer.'),),
      (S(20, 'Naming the region', 'Total Marks 40'),),
      (fixed('Region named', 1, 'Naming the region · 1 marks'),
       srp3('Description', 13, ('Describing the development of transport', '13 SRPs @ 3 marks each · 39 marks'))),
      '1-5', EURO, ID + 'p2-q6b', ('page',)),
    T('p2-6c', P2, '6C', '', 30, 18, L(18, 'Cultural Regions'),
      (L(18, 'A region’s culture can be defined by any of the following:', 'Games.'),
       L(18, 'Describe and explain the importance of culture in any region studied by you.'),
       L(18, 'Clearly state the name of the region in your answer.', nth=1)),
      (S(21, 'Naming the region', 'Total Marks 30'),),
      (fixed('Region named', 3, 'Naming the region · 3 marks'),
       srp3('Description and explanation', 9, ('Describe and explain the importance of culture',
                                               '9 SRPs @ 3 marks each · 27 marks'))),
      '1-3', IRL + EURO + CONT, ID + 'p2-q6c'),
]

# 7A (sketch: ferry route, coniferous plantation, tourist information centre,
# independent holiday hostel) is held: see HELD.
Q7BI = L(20, '(i) Name one developed economy where tourism OR financial services contribute to that', 'economy.')
PART_TWO += [
    T('p2-7b-i', P2, '7B', '(i)', 4, 20, L(20, 'Developed Economy'), (Q7BI,),
      (S(24, 'One developed economy named', '(ii) · Describe one reason'),),
      (fixed('Developed economy named', 4, 'One developed economy named · 4 marks'),),
      '3-0', ECON, ID + 'p2-q7b-tourism', routes=sector_routes(ID + 'p2-q7b')),
    T('p2-7b-ii', P2, '7B', '(ii)', 12, 20, L(20, 'Developed Economy'),
      (L(20, '(ii) Describe one reason for the growth of tourism OR financial services in the developed',
         'economy named.'),),
      (S(24, 'Reason stated', '(iii) · Explain one benefit'),),
      (fixed('Reason stated', 3, 'Reason stated · 3 marks'),
       srp3('Reason explained', 3, ('Reason explained', '3 SRPs @ 3 marks each · 9 marks'))),
      '3-0', ECON, ID + 'p2-q7b-ii-tourism', stem=(Q7BI,), routes=sector_routes(ID + 'p2-q7b-ii')),
    T('p2-7b-iii', P2, '7B', '(iii)', 12, 20, L(20, 'Developed Economy'),
      (L(20, '(iii) Explain one benefit that tourism OR financial services bring to the economies of',
         'developed countries.'),),
      (S(24, 'Benefit stated', '(iv) · Explain one problem'),),
      (fixed('Benefit stated', 3, 'Benefit stated · 3 marks'),
       srp3('Benefit explained', 3, ('Benefit explained', '3 SRPs @ 3 marks each · 9 marks'))),
      '3-0', ECON, ID + 'p2-q7b-iii-tourism', routes=sector_routes(ID + 'p2-q7b-iii')),
    T('p2-7b-iv', P2, '7B', '(iv)', 12, 20, L(20, 'Developed Economy'),
      (L(20, '(iv) Explain one problem caused by tourism OR financial services.'),),
      (S(24, 'Problem stated', 'Total Marks 40'),),
      (fixed('Problem stated', 3, 'Problem stated · 3 marks'),
       srp3('Problem explained', 3, ('Problem explained', '3 SRPs @ 3 marks each · 9 marks'))),
      '3-0', ECON, ID + 'p2-q7b-iv-tourism', routes=sector_routes(ID + 'p2-q7b-iv')),
]
Q7CI = L(20, '(i) Name two sources of renewable energy which are suitable for use in Ireland.')
PART_TWO += romans('7C', P2, 20, L(20, 'Renewable Energy'), (), ID + 'p2-q7c', (), [
    ('(i)', 6, Q7CI, S(24, 'Two sources named', '(ii) · Explain why'),
     (fixed('Two sources named', 6, 'Two sources named @ 3 marks each · 6 marks', (0, 3, 6)),), '3-5', ECON),
    ('(ii)', 24, L(20, '(ii) Explain why the two sources named above, are suitable for use in Ireland.'),
     S(24, 'Source 1 explained', 'Total Marks 30'),
     (srp3('Source 1 explained', 4, ('Source 1 explained', '=4 SRPs @ 3 marks each · 12 marks@0')),
      srp3('Source 2 explained', 4, ('Source 2 explained', '=4 SRPs @ 3 marks each · 12 marks@1'))),
     '3-5', ECON, (), (Q7CI,)),
])
Q8AIV = L(21, '(iv) What trading partners received the most Irish exports in 2009?')
PART_TWO += romans('8A', P2, 21, L(21, 'Irish Trade'),
                   (L(21, 'Study the table above and answer the following questions:'),),
                   ID + 'p2-q8a', ('page',), [
    ('(i)', 5, L(21, '(i) What was the total value of imports in 2009?'),
     S(25, '(i) · 44,835', '(ii) · 83,524'), (fixed('Imports', 5, '(i) · 44,835 · 5 marks'),), '2-0', GRAPH),
    ('(ii)', 5, L(21, '(ii) What was the total value of exports in 2009?'),
     S(25, '(ii) · 83,524', '(iii) · 38,689'), (fixed('Exports', 5, '(ii) · 83,524 · 5 marks'),), '2-0', GRAPH),
    ('(iii)', 5, L(21, '(iii) Calculate the difference between total value of imports and total value of exports',
                   'in 2009.'),
     S(25, '(iii) · 38,689', '(iv) · Other EU'), (fixed('Difference', 5, '(iii) · 38,689 · 5 marks'),), '2-0', GRAPH),
    ('(iv)', 5, Q8AIV,
     S(25, '(iv) · Other EU', '(v) · One reason'), (fixed('Trading partners', 5, '(iv) · Other EU countries · 5 marks'),),
     '2-0', GRAPH + EU),
    ('(v)', 5, L(21, '(v) State one reason why this is the case.'),
     S(25, '(v) · One reason', '(vi) · Product 1'), (fixed('Reason', 5, '(v) · One reason stated · 5 marks'),),
     '3-3', EU, (), (Q8AIV,)),
    ('(vi)', 5, L(21, '(vi) Name any two products exported from Ireland.'),
     S(25, '(vi) · Product 1', 'Total Marks 30'),
     (fixed('Product 1', 3, '(vi) · Product 1 · 3 marks'), fixed('Product 2', 2, 'Product 2 · 2 marks')),
     '3-0', ECON),
])
PART_TWO += romans('8B', P2, 21, L(21, 'Industrial Location'),
                   (L(21, 'Examine the aerial photograph accompanying this paper.'),
                    L(21, 'It is proposed to build a fish processing factory on the green field site in the centre',
                      'the aerial photograph.')),
                   ID + 'p2-q8b', ('aerial',), [
    ('(i)', 22, L(21, '(i) Describe two advantages this site has for the location of a fish processing', 'factory.'),
     S(25, 'Two advantages as follows:', '(Sub-total 22)'),
     two_of('Advantage', 11, 'Two advantages as follows:', 'Advantage stated · 2 marks',
            ('=Explained', '3 SRPs @ 3 marks each · 9 marks'), ((0, 2), steps(9, 3))),
     '3-0', ECON + AER),
    ('(ii)', 8, L(21, '(ii) Describe one problem that might arise as a result of building a fish processing',
                  'this site.'),
     S(25, 'One problem as follows:', '(Sub-total 8)'),
     (fixed('Problem stated', 2, ('One problem as follows:', 'Problem stated · 2 marks')),
      srp3('Problem explained', 2, ('=Explained', '2 SRPs @ 3 marks each · 6 marks'))),
     '3-4', ENV + AER),
])
Q8CI = L(22, '(i) Name two economic activities that could cause environmental pollution.')
PART_TWO += romans('8C', P2, 22, L(22, 'Environmental Pollution'),
                   (L(22, 'Pollution of the environment is a problem which can occur as a result of economic',
                      'activities.'),),
                   ID + 'p2-q8c', ('page',), [
    ('(i)', 4, Q8CI, S(26, 'Two activities named', '(Sub-total 4)'),
     (fixed('Two activities named', 4, 'Two activities named @ 2 marks each · 4 marks', (0, 2, 4)),), '3-4', ENV),
    ('(ii)', 18, L(22, '(ii) Explain one way that these economic activities cause environmental pollution.'),
     S(26, 'Way stated', '(Sub-total 18)'),
     (fixed('Way stated', 3, 'Way stated · 3 marks'),
      srp3('Way explained', 5, ('=Explained', '5 SRPs @ 3 marks each · 15 marks'))), '3-4', ENV, (), (Q8CI,)),
    ('(iii)', 18, L(22, '(iii) Explain one solution to environmental pollution.'),
     S(26, 'Solution stated', '(Sub-total 18)'),
     (fixed('Solution stated', 3, 'Solution stated · 3 marks'),
      srp3('Solution explained', 5, ('=Explained', '5 SRPs @ 3 marks each · 15 marks'))), '3-4', ENV),
])
PART_TWO += romans('9A', P2, 23, L(23, 'World Energy', nth=0),
                   (L(23, 'Examine the data above regarding world energy consumption in 2007.'),),
                   ID + 'p2-q9a', ('page',), [
    ('(i)', 24, L(23, '(i) Using graph paper, draw a suitable graph to illustrate this data.'),
     S(27, 'Graph paper', '(Sub-total 24)'), GRAPH_OL, '2-0', GRAPH),
    ('(ii)', 6, L(23, '(ii) In your answer book, name two types of energy which are not named in the table above.'),
     S(27, 'Two types of energy named', '(Sub-total 6)'),
     (fixed('Two types of energy', 6, 'Two types of energy named @ 3 marks each · 6 marks', (0, 3, 6)),),
     '3-5', ECON),
])
Q9BI = L(23, '(i) Name one multinational company (MNC) operating in Ireland and state where it is', 'located.')
PART_TWO += romans('9B', P2, 23, L(23, 'Multinational Companies'), (), ID + 'p2-q9b', (), [
    ('(i)', 6, Q9BI, S(27, 'MNC named', '(Sub-total 6)'),
     (fixed('MNC named', 2, 'MNC named · 2 marks'), fixed('MNC located', 4, 'MNC located · 4 marks')), '3-2', MNC),
    ('(ii)', 6, L(23, '(ii) Name one raw material used by this multinational company and state where the raw',
                  'is sourced.'),
     S(27, 'Raw material named', '(Sub-total 6)'),
     (fixed('Raw material named', 2, 'Raw material named · 2 marks'),
      fixed('Raw material sourced', 4, 'Raw material sourced · 4 marks')), '3-2', MNC, (), (Q9BI,)),
    ('(iii)', 10, L(23, '(iii) Name one product manufactured by this multinational company and name two markets',
                    'is sold.'),
     S(27, 'Product named', '(Sub-total 10)'),
     (fixed('Product named', 2, 'Product named · 2 marks'), fixed('Market 1 named', 4, 'Market 1 named · 4 marks'),
      fixed('Market 2 named', 4, 'Market 2 named · 4 marks')), '3-2', MNC, (), (Q9BI,)),
    ('(iv)', 18, L(23, '(iv) Explain one reason why some multinational companies leave Ireland to locate',
                   'elsewhere.'),
     S(27, 'Reason stated', '(Sub-total 18)'),
     (fixed('Reason stated', 3, 'Reason stated · 3 marks'),
      srp3('Reason explained', 5, 'Reason explained · 5 SRPs @ 3 marks each · 15 marks')), '3-2', MNC),
])
Q9CI = L(23, '(i) Name any one European Union policy which affects Ireland’s economy.')
PART_TWO += romans('9C', P2, 23, L(23, 'Ireland and the European Union'), (), ID + 'p2-q9c', (), [
    ('(i)', 6, Q9CI, S(28, 'European Union policy named', '(ii) · Describe and explain'),
     (fixed('EU policy named', 6, 'European Union policy named · 6 marks'),), '3-3', EU),
    ('(ii)', 24, L(23, '(ii) Describe and explain two effects of this policy on Ireland’s economy.'),
     S(28, 'Two effects', 'Total Marks 30'),
     two_of('Effect', 12, 'Two effects = · 24 marks', 'For each effect:',
            ('Effect stated · 3 marks', 'Described and explained', '3 SRPs @ 3 marks each · 9 marks'),
            ((0, 3), steps(9, 3))),
     '3-3', EU, (), (Q9CI,)),
])
BRIEF2 = 'Two SRPs @ 3 marks each · 6 marks'
PART_TWO += romans('10A', P2, 24, L(24, 'World Population', nth=0),
                   (L(24, 'Study the map above showing world population density and answer the following',
                      'questions:'),),
                   ID + 'p2-q10a', ('page',), [
    ('(i)', 6, L(24, '(i) In what category of population density is Ireland?'),
     S(29, '50-74', '(ii) · Name one country'), (fixed('Category', 6, '50-74 · 6 marks'),), '4-0', POP + GRAPH),
    ('(ii)', 6, L(24, '(ii) Name any one country in the 0-9 category of population density.'),
     S(29, 'Country named', '(iii) · Explain briefly'), (fixed('Country named', 6, 'Country named · 6 marks'),),
     '4-0', POP + GRAPH),
    ('(iii)', 6, L(24, '(iii) Explain briefly what is meant by population density.'),
     S(29, 'Explanation', '(iv) · Explain briefly'), (srp3('Explanation', 2, ('=Explanation', BRIEF2)),), '4-0', POP),
    ('(iv)', 6, L(24, '(iv) Explain briefly one negative effect of high population density.'),
     S(29, 'Effect explained', '(v) · Explain briefly', None, '(iv) · Explain briefly'),
     (srp3('Effect explained', 2, ('Effect explained', BRIEF2)),), '4-1', POP),
    ('(v)', 6, L(24, '(v) Explain briefly one negative effect of low population density.'),
     S(29, 'Effect explained', 'Total Marks 30', None, '(v) · Explain briefly'),
     (srp3('Effect explained', 2, ('Effect explained', BRIEF2)),), '4-1', POP),
])
Q10BI = L(25, '(i) Name one traffic problem experienced by cities that are growing rapidly.')
PART_TWO += romans('10B', P2, 25, L(25, 'Transport in Urban Areas'), (), ID + 'p2-q10b', (), [
    ('(i)', 5, Q10BI, S(30, 'One traffic problem named', '(ii) · Name one city'),
     (fixed('Traffic problem named', 5, 'One traffic problem named · 5 marks'),), '4-5', URB),
    ('(ii)', 5, L(25, '(ii) Name one city that has such a problem.'),
     S(30, 'One city named', '(iii) · Explain two reasons'), (fixed('City named', 5, 'One city named · 5 marks'),),
     '4-5', URB, (), (Q10BI,)),
    ('(iii)', 18, L(25, '(iii) Explain two reasons why this problem has developed.'),
     S(30, 'Reason 1 stated', '(Sub-total 18)'),
     two_reasons('2 SRPs @ 3 marks each · 6 marks', '2 SRPs @ 3 marks graded · 6 marks'), '4-5', URB, (), (Q10BI,)),
    ('(iv)', 12, L(25, '(iv) Explain one solution to this problem.'),
     S(30, 'Solution stated', '(Sub-total 12)'),
     (fixed('Solution stated', 3, 'Solution stated · 3 marks'),
      srp3('Solution explained', 3, ('=Explained', '3 SRPs @ 3 marks each · 9 marks'))), '4-5', URB, (), (Q10BI,)),
])
PART_TWO += romans('10C', P2, 25, L(25, 'Population'), (), ID + 'p2-q10c', (), [
    ('(i)', 9, L(25, '(i) Explain the term ‘birth rate’.'),
     S(30, 'Birth rate explained', '(Sub-total 9)'),
     (srp3('Birth rate explained', 3, ('Birth rate explained', '3 SRPs @ 3 marks each · 9 marks')),), '4-0', POP),
    ('(ii)', 21, L(25, '(ii) Explain how any of the following factors influences birth rates:', 'Income levels.'),
     S(30, 'Factor(s) explained', '(Sub-total 21)'),
     (srp3('Factor(s) explained', 7, ('Factor(s) explained', '7 SRPs @ 3 marks each · 21 marks')),), '4-0', POP),
])
PART_TWO += romans('11A', P2, 26, L(26, 'Population', nth=0),
                   (L(26, 'Examine the data above showing approximate figures for the population of a number of',
                      'counties.'),),
                   ID + 'p2-q11a', ('page',), [
    ('(i)', 24, L(26, '(i) Using graph paper, draw a graph to illustrate this data.'),
     S(31, 'Graph paper', '(Sub-total 24)'), GRAPH_OL, '2-0', GRAPH),
    ('(ii)', 6, L(26, '(ii) In your answer book, briefly explain why Co Dublin has the largest population.'),
     S(31, 'Explaining why Co Dublin', '(Sub-total 6)'),
     (srp3('Explanation', 2, ('Explaining why Co Dublin has the largest population', '2 SRPs @ 3 marks each · 6 marks')),),
     '4-0', POP),
])
Q11BI = L(26, '(i) Explain two reasons why people migrate from rural areas to cities.')
PART_TWO += romans('11B', P2, 26, L(26, 'Migration'), (), ID + 'p2-q11b', (), [
    # The question-wide "* Understanding of the concept of migration = 1 mark"
    # is carded with (i), the first part that asks about migration.
    ('(i)', 19, Q11BI,
     (S(31, 'Reason 1 stated', '(Sub-total 18)'),
      S(31, 'Understanding of the concept of migration', 'Total Marks 40')),
     (*two_reasons('2 SRPs @ 3 marks each · 6 marks', '2 SRPs @ 3 marks graded · 6 marks'),
      fixed('Understanding of the concept of migration', 1, 'Understanding of the concept of migration')),
     '4-2', POP),
    ('(ii)', 12, L(26, '(ii) Explain one effect this has on the rural areas they have left behind.'),
     S(31, 'Effect stated', '(Sub-total 12)'),
     (fixed('Effect stated', 3, 'Effect stated · 3 marks'),
      srp3('Effect explained', 3, ('=Explained', '3 SRPs @ 3 marks each · 9 marks'))), '4-2', POP, (), (Q11BI,)),
    ('(iii)', 9, L(26, '(iii) Explain one reason why large numbers of people are emigrating from Ireland in recent',
                   'times.'),
     S(31, 'Reason stated', '(Sub-total 9)'),
     (fixed('Reason stated', 3, 'Reason stated · 3 marks'),
      srp3('Reason explained', 2, ('=Explained', '2 SRPs @ 3 marks each · 6 marks'))), '4-2', POP),
])
MATCHED = ('Matching issues to photograph as above', '4 SRPs @ 3 marks each · 12 marks')
PART_TWO += [
    T('p2-11c-i', P2, '11C', '(i)', 12, 27, L(27, 'Urban Issues'),
      (L(27, '(i) Examine the photographs of urban issues shown above', 'Heritage issues.'),),
      (S(32, '• Cities of the future', 'Scheme'), S(32, 'Matching issues to photograph', '(ii) · Describe any one')),
      (fixed('Row 1', 3, ('Cities of the future · B', *MATCHED)),
       fixed('Row 2', 3, ('Urban transport · C', *MATCHED)),
       fixed('Row 3', 3, ('Urban problems · D', *MATCHED)),
       fixed('Row 4', 3, ('Heritage issues. · A', *MATCHED))),
      '4-5', URB, ID + 'p2-q11c', ('page',),
      row_labels=tuple(L(27, item) for item in URBAN_ISSUES)),
    T('p2-11c-ii', P2, '11C', '(ii)', 18, 27, L(27, 'Urban Issues'),
      (L(27, '• Cities of the future', 'Heritage issues.'),
       L(27, '(ii) Describe any one of the urban issues listed above.')),
      (S(32, 'Issue described', 'Total Marks 30'),),
      (srp3('Issue described', 6, ('Issue described', '6 SRPs @ 3 marks each · 18 marks')),),
      '4-5', URB, ID + 'p2-q11c-ii-cities-of-the-future', ('page',),
      routes=bullet_routes('p2-q11c-ii-', URBAN_ISSUES)),
    T('p2-12a', P2, '12A', '', 30, 28, L(28, 'Land-Use'),
      (L(28, 'Examine the aerial photograph accompanying this paper.', 'A housing estate.'),),
      (S(33, 'Sketch Map as follows:', 'Total Marks 30'),),
      (fixed('Limits/frame', 1, ('Sketch Map as follows:', 'Limits/frame = · 1 mark')),
       fixed('Proportions (landscape)', 2, 'Proportions (landscape) = · 2 marks graded', upto(2)),
       fixed('Overall impression', 2, 'Overall impression = · 2 marks graded', upto(2)),
       *(Criterion(f'Item {n}', 5, sums(upto(3), (0, 2)), 'exact',
                   ('Five items shown and named as follows:', 'Showing = · 3 marks graded',
                    'Naming/identifying = · 2 marks'))
         for n in range(1, 6))),
      '2-8', AER + URB, ID + 'p2-q12a', ('aerial',),
      row_labels=(None, None, None, L(28, 'A port area'), L(28, 'A carpark'), L(28, 'A main shopping street'),
                  L(28, 'A roundabout'), L(28, 'A housing estate.'))),
]
Q12BI = L(28, '(i) Give a 4 figure grid reference for an area on the map which has a high population density.')
Q12BIII = L(28, '(iii) Give a 4 figure grid reference for an area on the map with a low population density.')
PART_TWO += romans('12B', P2, 28, L(28, 'Population Density and Distribution'),
                   (L(28, 'Study the Ordnance Survey map and legend accompanying this paper and answer the following',
                      'questions:'),),
                   ID + 'p2-q12b', ('map',), [
    ('(i)', 4, Q12BI, S(34, 'Four/Six figure grid', '(ii) · Explain in detail', None, '(i) · Give a 4 figure'),
     (fixed('Grid reference', 4, 'Four/Six figure grid · 4 marks graded', upto(4)),), '4-0', POP + MAP),
    ('(ii)', 16, L(28, '(ii) Explain in detail, using map evidence, why there is a high density of population at',
                   'location.'),
     S(34, 'Explained', '(Sub-total 16)', None, '(ii) · Explain in detail'),
     (srp3('Explanation', 4, ('=Explained', '4 SRPs @ 3 marks each · 12 marks')),
      fixed('Map evidence', 4, 'Map evidence · 4 marks graded', upto(4))), '4-0', POP + MAP, (), (Q12BI,)),
    ('(iii)', 4, Q12BIII, S(34, 'Four/Six figure grid', '(iv) · Explain in detail', None, '(iii) · Give a 4 figure'),
     (fixed('Grid reference', 4, 'Four/Six figure grid · 4 marks'),), '4-0', POP + MAP),
    ('(iv)', 16, L(28, '(iv) Explain in detail, using map evidence, why there is a low density of population at',
                   'location.'),
     S(34, 'Explained', '(Sub-total 16)', None, '(iv) · Explain in detail'),
     (srp3('Explanation', 4, ('=Explained', '4 SRPs @ 3 marks each · 12 marks')),
      fixed('Map evidence', 4, 'Map evidence · 4 marks')), '4-0', POP + MAP, (), (Q12BIII,)),
])
PART_TWO.append(T(
    'p2-12c', P2, '12C', '', 30, 28, L(28, 'Urban Functions'),
    (L(28, 'Describe how the functions of any urban area studied by you have changed over time.',
       'Clearly state the name of the urban area in your answer.'),),
    (S(34, 'Naming the urban area', 'Total Marks 30'),),
    (fixed('Urban area named', 3, 'Naming the urban area · 3 marks'),
     srp3('Description of the functions', 9, ('Describe the functions', '9 SRPs @ 3 marks each · 27 marks'))),
    '4-3', URB, ID + 'p2-q12c'))

TASKS = [*PART_ONE, *PART_TWO]

ID_CORRECTION_REASON = 'No 2011 Ordinary card shipped before this review; every card is new.'

# No 2011 Ordinary card was live on origin/main before this review.
LEGACY_IDS: list[str] = []
