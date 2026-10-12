"""Independent review ledger: Leaving Certificate Geography 2025 Ordinary Level.

Sources (English editions, Paper Trail index; sizes and SHA-256 pinned in
EXPECTED_SOURCES and the generated audit): Part One and Answerbook
LC005GLP042EV (40 pages), Part Two LC005GLP043EV (16 pages), marking scheme
LC005GLP000EV (36 pages), and the common companions shared with Higher Level
— the 1:50 000 Oughterard map LC005CLP003EV (fetched from Paper Trail
storage), its legend LC005CLPC00EV and the Oughterard aerial photograph
LC005CLP004EV (published only as a JPEG).

Visual sweep (every page rendered and read on 2026-10-11):
  Part One booklet p1 cover (COVID-adjusted paper note); p2 instructions;
  p3-p12 Questions 1-12 (p7 holds Q5 and Q6, p8 holds Q7 and Q8); p13 Part
  Two answerbook instructions; p14-p17 graph-paper answer pages; p18-p39
  lined answer pages; p40 copyright/back cover.
  Part Two booklet p1 cover; p2 Part Two instructions ("attempt THREE");
  p3-p8 Sections 1-2 (Q1-Q6); p9 Section 3 divider; p10-p15 Electives
  (Q7-Q12); p16 copyright/back cover.
  Scheme p1 cover; p2-p3 notes; p4 Geographical Investigation (coursework,
  not a written-paper task); p5 presentation breakdown; p6-p7 Part One
  table; p8 Part Two instructions; p9-p21 Q1-Q6 (each A/B/C roman priced);
  p22 Section 3 divider; p23-p34 Q7-Q12; p35 blank; p36 back cover.
  Companions: Oughterard map extract (Lough Corrib, the N59, Inishshanboe
  Island); OS legend sheet; oblique aerial photograph of Oughterard.

Companions. Part One Q5, Q6 (map, legend) and Q7 (aerial); Part Two 1A, 8B
and 12B (map, legend), 7A and 10A (aerial) were held back before this review
because their companions were not wired. Each now carries the exact official
documents it names.

Boundaries follow the published allocation: at Ordinary Level the scheme
prices every printed roman of every A, B and C part, so each roman is its own
task (3B (i) 4m is separate from the 36m choose-two weathering routes). Part
One romans and lettered true/false items are tasks; a matching table under
ONE printed instruction stays one task with a criterion per scheme row, each
row checked against the image: Q1 Convection current=B, Subducting plate=E,
Core=A, Continental crust=D, Separating plates=C; Q2 Stalagmite=C,
Column/Pillar=B, Stalactite=A; Q3 Glacial erratic=C, U-shaped valley=A, Sea
stack=B, V-shaped valley=D; Q4 Marble=B, Slate=C; Q8 Gaeltacht=B, Cool
Temperate Oceanic=E, Longford County Council=A, Brussels=D, The Burren=C;
Q10 Warm front=C, High pressure=D, Low pressure=A, Occluded front=B; Q12
Elbrus=D, Debby=A, Anak Krakatoa=C, Kura=B; Part Two 3A (i) B Waterfall,
C Landslide, A Beach and (ii) A Coastal deposition, B River erosion, C Mass
movement. A part whose wording depends on an earlier part ("this secondary
economic activity", "named in part (i) above", "this multinational
company") carries that earlier printed part in its stem.

Tariffs: an SRP is 3 marks at Ordinary Level; "a+b" lines are one criterion
with partial credit a; graded lines keep their printed grades; sketch items
are "showing 3 (3/1/0) + labelled 2"; 4A items are "named 2 + shown 4
(4/2/0)". Every question totals 10 (Part One) or 100 = 30 + 40 + 30 (Part
Two) as printed.

Wording: the paper wins where the scheme reprints it differently (1B title
"Landform Development", scheme "Surface Processes"; 7C "economic activities
with reference to"; 11A(v) "high birth rates." without "in Ireland").
"""

import itertools

from geography_review import (
    Criterion, Lift, Route, SchemeSlice, Task, fixed, slug, srp, steps, sums,
)

YEAR = 2025
LEVEL = 'ordinary'
PAPER_PAGES = {1: 40, 2: 16}
SCHEME_PAGES = 36
QUESTION_TARIFFS = {1: {str(n): 10 for n in range(1, 13)},
                    2: {f'{n}{x}': (40 if x == 'B' else 30)
                        for n in range(1, 13) for x in 'ABC'}}

EXPECTED_SOURCES = {
    'paper1': ('LC005GLP042EV.pdf', 7159483),
    'paper2': ('LC005GLP043EV.pdf', 3264105),
    'scheme': ('LC005GLP000EV.pdf', 1288974),
    'map': ('LC005CLP003EV.pdf', 19789910),
    'legend': ('LC005CLPC00EV.pdf', 4055991),
    'aerial': ('LC005CLP004EV.jpg', 5572138),
}

PAGE_REVIEW = {
    'paper1': {1: 'cover', 2: 'instructions', **{p: 'question' for p in range(3, 13)},
               13: 'answerbook instructions', **{p: 'graph-paper answer page' for p in range(14, 18)},
               **{p: 'lined answer page' for p in range(18, 40)}, 40: 'copyright/back cover'},
    'paper2': {1: 'cover', 2: 'Part Two instructions',
               **{p: 'question' for p in (3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15)},
               9: 'section divider', 16: 'copyright/back cover'},
    'scheme': {1: 'cover', 2: 'notes', 3: 'notes', 4: 'geographical investigation (coursework)',
               5: 'investigation presentation breakdown', 6: 'Part One table', 7: 'Part One table',
               8: 'Part Two instructions', **{p: 'Part Two allocation' for p in range(9, 22)},
               22: 'section divider', **{p: 'Part Two allocation' for p in range(23, 35)},
               35: 'blank', 36: 'back cover'},
}

EXPECTED_SELECTION_SCAN = [
    [1, 2, 'attempt any ten'], [1, 2, 'attempt three'], [1, 3, 'attempt any ten'],
    [2, 2, 'attempt three'],
    [2, 3, 'answer (i) or (ii)'], [2, 3, 'any two'], [2, 3, 'any two'], [2, 3, 'one of the following'],
    [2, 4, 'one of the following'],
    [2, 5, 'any two'], [2, 5, 'any two'],
    [2, 6, 'any one'],
    [2, 7, 'any two'],
    [2, 8, 'any one'],
    [2, 10, 'one of the following'],
    [2, 14, 'any three'],
]
SELECTION_REVIEW = [
    {'scan': [[1, 2, 'attempt any ten'], [1, 2, 'attempt three'], [1, 3, 'attempt any ten'],
              [2, 2, 'attempt three']],
     'kind': 'exam-attempt-rule',
     'reason': 'Part One any ten of twelve and Part Two three questions from two sections are attempt rules; every question is carded.'},
    {'scan': [[2, 3, 'answer (i) or (ii)']], 'kind': 'closed-route',
     'reason': '1B: (i) or (ii) -> two routes, each with its own scheme allocation.'},
    {'scan': [[2, 3, 'one of the following']], 'kind': 'closed-choose-one',
     'reason': '1C: one of four printed bullets -> four routes.'},
    {'scan': [[2, 4, 'one of the following']], 'kind': 'closed-choose-one',
     'reason': '2C: one of three printed surface processes -> three routes.'},
    {'scan': [[2, 5, 'any two']], 'kind': 'closed-choose-two',
     'reason': '3B(ii): any two of three printed types of weathering -> C(3,2) = 3 routes.'},
    {'scan': [[2, 7, 'any two']], 'kind': 'closed-choose-two',
     'reason': '5B: any two of three printed headings -> C(3,2) = 3 routes.'},
    {'scan': [[2, 10, 'one of the following']], 'kind': 'closed-choose-one',
     'reason': '7C: one of three printed economic activities -> three routes.'},
    {'scan': [[2, 3, 'any two'], [2, 3, 'any two'], [2, 5, 'any two'], [2, 6, 'any one'],
              [2, 8, 'any one'], [2, 14, 'any three']],
     'kind': 'open-response',
     'reason': 'No printed pool: 1B(i) any two landforms and 1B(ii) any two mass movement processes (the scheme prices two @ 20m); 3B(i) any two factors; 4C any one region (the factor box is illustrative, not a choice); 6C any one urban area; 11B(iii) any three problems. 5C "two problems" and 12B "three different rural settlement patterns" are open too; the scheme prices each one.'},
]

P1, P2 = 1, 2
ID = 'geography-2025-ol-'
O = 'geography-ordinary-'
SRP3 = 3


def L(page, start, end=None, nth=None):
    return Lift(page, start, end, None, nth)


def S(page, start, end=None, clip=None, after=None, table=False):
    return SchemeSlice(page, start, end, clip, after, table)


def srp3(label, count, line):
    return srp(label, count, line, SRP3)


def T(key, part, q, sub, marks, page, title, prompt, scheme, criteria, topic, atlas, card_id,
      legacy, sources=(), stem=(), routes=(), row_labels=()):
    return Task(key, part, q, sub, marks, page, title, prompt, scheme, criteria, topic, atlas,
                sources, card_id, legacy, stem=stem, routes=routes, row_labels=row_labels)


def rows(lines, marks=2):
    return tuple(fixed(f'Row {i}', marks, line) for i, line in enumerate(lines, 1))


def chosen(items, k):
    return [(combo, ' + '.join(item.rstrip('.') for item in combo),
             '-'.join(slug(item, 34) for item in combo))
            for combo in itertools.combinations(items, k)]


def bullet_routes(prefix, items, k=1, atlas=None):
    return tuple(Route(route_slug, label, ID + prefix + route_slug, True, keep_bullets=combo,
                       atlas=(atlas[combo[0]] if atlas else None))
                 for combo, label, route_slug in chosen(items, k))


TF = 'Indicate whether the following statements are true or false by ticking (✓) the correct'

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
Q1S = (L(3, 'Examine the diagram above which shows the structure of the earth', 'following question.'),)
Q2S = (L(4, 'Examine the photograph of karst features above', 'questions.'),)
Q2TF = L(4, '(ii) ' + TF, 'box.')
Q3S = (L(5, 'Examine the photographs above and answer each of the following questions.'),)
Q4S = (L(6, 'Examine the photographs above. Complete the table below', 'completed for you.'),)
Q5S = (L(7, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper, and',
         'following questions.', nth=0),)
Q6S = (L(7, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper, and',
         'following questions.', nth=1),)
Q7S = (L(8, 'Examine the aerial photograph of Oughterard accompanying this paper.'),
       L(8, TF + ' box.'))
Q9S = (L(9, 'Examine the table above showing the year that each of the current members', 'following questions.'),)
Q11S = (L(11, 'Examine the infographic above on employment, occupations and commuting', 'following questions.'),)
Q12S = (L(12, 'Examine the satellite images above and answer each of the following questions.'),)

PART_ONE = [
    T('p1-1', P1, '1', '', 10, 3, L(3, 'Plate Tectonics'),
      (L(3, 'Match each of the letters A, B, C, D and E', 'below.'),),
      (S(6, 'Q.1 · B', 'Q.2 (i)'),),
      rows(['Q.1 · B', 'E · 2m', 'A · 2m', 'D · 2m', 'C · 2m · Total 10m']), '0-0', PS, ID + 'p1-q1', True,
      ('page',), Q1S,
      row_labels=(L(3, 'Convection current'), L(3, 'Subducting plate'), L(3, 'Core'),
                  L(3, 'Continental crust'), L(3, 'Separating plates'))),
    T('p1-2-i', P1, '2', '(i)', 6, 4, L(4, 'Karst Landscape'),
      (L(4, '(i) Match each of the letters A, B and C', 'below.'),),
      (S(6, 'Q.2 (i)', '(ii)(a)'),),
      rows(['Q.2 (i) · C', 'B · 2m', 'A · 2m']), '0-3', KARST, ID + 'p1-q2', True, ('page',), Q2S,
      row_labels=(L(4, 'Stalagmite'), L(4, 'Column/Pillar'), L(4, 'Stalactite'))),
    T('p1-2-ii-a', P1, '2', '(ii)(a)', 2, 4, L(4, 'Karst Landscape'),
      (Q2TF, L(4, '(a) The features in the photograph above are formed as a result of',
               'physical/mechanical weathering.')),
      (S(6, '(ii)(a) · False', '(ii)(b)'),),
      (fixed('Statement (a)', 2, '(ii)(a) · False'),), '0-3', KARST, ID + 'p1-q2-ii-a', False, ('page',), Q2S),
    T('p1-2-ii-b', P1, '2', '(ii)(b)', 2, 4, L(4, 'Karst Landscape'),
      (Q2TF, L(4, '(b) The features in the photograph above are formed underground.')),
      (S(6, '(ii)(b) · True', 'Q.3 (i)'),),
      (fixed('Statement (b)', 2, '(ii)(b) · True'),), '0-3', KARST, ID + 'p1-q2-ii-b', False, ('page',), Q2S),
    T('p1-3-i', P1, '3', '(i)', 8, 5, L(5, 'Surface Processes'),
      (L(5, '(i) Match each of the photographs A, B, C and D', 'that best matches it.'),),
      (S(6, 'Q.3 (i)', '(ii) · Erosion'),),
      rows(['Q.3 (i) · C', 'A · 2m', 'B · 2m', 'D · 2m']), '0-4', PS_SURFACE, ID + 'p1-q3', True, ('page',), Q3S,
      row_labels=(L(5, 'Glacial erratic'), L(5, 'U-shaped valley'), L(5, 'Sea stack'), L(5, 'V-shaped valley'))),
    T('p1-3-ii', P1, '3', '(ii)', 2, 5, L(5, 'Surface Processes'),
      (L(5, '(ii) Which of the following processes is most associated', 'Tick (✓) the correct box.'),
       L(5, 'Erosion'), L(5, 'Deposition')),
      (S(6, '(ii) · Erosion', 'Q.4 (i)'),),
      (fixed('Process', 2, '(ii) · Erosion'),), '0-10', SEA, ID + 'p1-q3-ii', False, ('page',), Q3S),
    T('p1-4-i', P1, '4', '(i)', 4, 6, L(6, 'Rocks'),
      (L(6, '(i) Match each of the photographs A, B, C and D with the rock type', 'the table below.'),),
      (S(6, 'Q.4 (i)', '(ii) · Sedimentary'),),
      rows(['Q.4 (i) · B', 'C · 2m']), '0-1', RW, ID + 'p1-q4', True, ('page',), Q4S,
      row_labels=(L(6, 'Marble'), L(6, 'Slate'))),
    T('p1-4-ii', P1, '4', '(ii)', 6, 6, L(6, 'Rocks'),
      (L(6, '(ii) State whether each rock type is an igneous, sedimentary or metamorphic rock.'),),
      (S(6, '(ii) · Sedimentary', 'Q.5 (i)'),),
      rows(['(ii) · Sedimentary', 'Metamorphic · 2m', 'Igneous · 2m']), '0-1', RW, ID + 'p1-q4-ii', False,
      ('page',), Q4S, row_labels=(L(6, 'Sandstone'), L(6, 'Marble'), L(6, 'Granite'))),
    T('p1-5-i', P1, '5', '(i)', 5, 7, L(7, 'Map Skills'),
      (L(7, '(i) Lough Corrib is located in which area', 'Tick (✓) the correct box.'),
       L(7, 'South west'), L(7, 'North east')),
      (S(6, 'Q.5 (i)', '(ii) · 7 km'),),
      (fixed('Area of the map', 5, 'Q.5 (i) · North east · 5m'),), '2-6', MAP, ID + 'p1-q5', False,
      ('map', 'legend'), Q5S),
    T('p1-5-ii', P1, '5', '(ii)', 5, 7, L(7, 'Map Skills'),
      (L(7, '(ii) What is the approximate area of Lough Corrib', 'Tick (✓) the correct box.'),
       L(7, '7 km²'), L(7, '12 km²')),
      (S(6, '(ii) · 7 km', 'Q.6 (i)'),),
      (fixed('Area', 5, '(ii) · 7 km'),), '2-6', MAP, ID + 'p1-q5-ii', False, ('map', 'legend'), Q5S),
    T('p1-6-i', P1, '6', '(i)', 6, 7, L(7, 'Ordnance Survey Map'),
      (L(7, '(i) Name the feature shown at each of the following grid references:'),),
      (S(6, 'Q.6 (i)', '(ii) · National'),),
      rows(['Q.6 (i) · 18hole golf', 'Cycle route · 2m', 'Cillin · 2m']), '2-6', MAP, ID + 'p1-q6', False,
      ('map', 'legend'), Q6S,
      row_labels=(L(7, 'M 144 421:'), L(7, 'M 037 445:'), L(7, 'M 124 422:'))),
    T('p1-6-ii', P1, '6', '(ii)', 2, 7, L(7, 'Ordnance Survey Map'),
      (L(7, '(ii) What does the letter N stand for in relation to the N59 road?'),),
      (S(6, '(ii) · National (secondary)', '(iii) · Correctly drawn'),),
      (fixed('Meaning of N', 2, '(ii) · National (secondary) · 2m'),), '2-6', MAP, ID + 'p1-q6-ii', False,
      ('map', 'legend'), Q6S),
    T('p1-6-iii', P1, '6', '(iii)', 2, 7, L(7, 'Ordnance Survey Map'),
      (L(7, '(iii) Draw the Ordnance Survey map symbol for a viewpoint in the space below.'),),
      (S(6, '(iii) · Correctly drawn symbol'),),
      (fixed('Symbol', 2, '(iii) · Correctly drawn symbol · 2m'),), '2-6', MAP, ID + 'p1-q6-iii', False,
      ('map', 'legend'), Q6S),
]

for index, (roman, statement, start, nxt, answer) in enumerate([
        ('(i)', 'There is a lake in the right foreground.', 'Q.7 (i) False', '(ii) · False', 'Q.7 (i) False · 2m'),
        ('(ii)', 'There is a football pitch in the left background.', '(ii) · False', '(iii) · True', '(ii) · False · 2m'),
        ('(iii)', 'There is an area of woodland in the right foreground.', '(iii) · True', '(iv) · True', '(iii) · True · 2m'),
        ('(iv)', 'There is a car park in the right middleground.', '(iv) · True', '(v) · True', '(iv) · True · 2m'),
        ('(v)', 'There is a housing estate in the centre foreground.', '(v) · True', 'Q.8', '(v) · True · 2m')]):
    PART_ONE.append(T(
        f'p1-7-{roman.strip("()")}', P1, '7', roman, 2, 8, L(8, 'Aerial Photograph'),
        (L(8, f'{roman} {statement}'),), (S(7, start, nxt),),
        (fixed('True or false', 2, answer),), '2-8', AER,
        ID + 'p1-q7' + ('' if index == 0 else f'-{roman.strip("()")}'), False, ('aerial',), Q7S))

PART_ONE.append(T(
    'p1-8', P1, '8', '', 10, 8, L(8, 'Regions'),
    (L(8, 'Match the type of region with the example of the region', 'in the table below.'),),
    (S(7, 'Q.8 · B', 'Q.9 (i)'),),
    rows(['Q.8 · B', 'E · 2m', 'A · 2m', 'D · 2m', 'C · 2m · Total 10m']),
    '1-0', EURO + IRL, ID + 'p1-q8', True, ('page',),
    row_labels=(L(8, 'Gaeltacht'), L(8, 'Cool Temperate Oceanic'), L(8, 'Longford County Council'),
                L(8, 'Brussels'), L(8, 'The Burren'))))

for index, (roman, prompt, start, nxt, answer, label, topic, atlas) in enumerate([
        ('(i)', '(i) In what year did Ireland join the European Union?', 'Q.9 (i) 1973', '(ii) · 3 · 2m',
         'Q.9 (i) 1973 · 2m', 'Year', '2-0', GRAPH + EU),
        ('(ii)', '(ii) How many countries joined the European Union in 1995?', '(ii) · 3 · 2m', '(iii) · Croatia',
         '(ii) · 3 · 2m', 'Number of countries', '2-0', GRAPH + EU),
        ('(iii)', '(iii) What country is the most recent member of the European Union?', '(iii) · Croatia',
         '(iv) · 2004', '(iii) · Croatia · 2m', 'Country', '2-0', GRAPH + EU),
        ('(iv)', '(iv) In what year did ten countries join the European Union?', '(iv) · 2004',
         '(v) · Valid advantage', '(iv) · 2004 · 2m', 'Year', '2-0', GRAPH + EU),
        ('(v)', '(v) State one advantage of European Union membership.', '(v) · Valid advantage', 'Q.10 (i)',
         '(v) · Valid advantage · 2m', 'One advantage', '3-3', EU)]):
    PART_ONE.append(T(
        f'p1-9-{roman.strip("()")}', P1, '9', roman, 2, 9, L(9, 'European Union', nth=0),
        (L(9, prompt),), (S(7, start, nxt),), (fixed(label, 2, answer),), topic, atlas,
        ID + 'p1-q9' + ('' if index == 0 else f'-{roman.strip("()")}'), index == 0, ('page',), Q9S))

PART_ONE += [
    T('p1-10-i', P1, '10', '(i)', 8, 10, L(10, 'Weather Charts'),
      (L(10, '(i) Match each of the weather chart symbols', 'in the table below.'),),
      (S(7, 'Q.10 (i) · C', '(ii) · Anticyclone'),),
      rows(['Q.10 (i) · C', 'D · 2m', 'A · 2m', 'B · 2m']), '2-7', WEATHER, ID + 'p1-q10', True, ('page',),
      row_labels=(L(10, 'Warm front'), L(10, 'High pressure system'), L(10, 'Low pressure system'),
                  L(10, 'Occluded front'))),
    T('p1-10-ii', P1, '10', '(ii)', 2, 10, L(10, 'Weather Charts'),
      (L(10, '(ii) What is another name for a high pressure system?', 'Tick (✓) the correct box.'),
       L(10, 'Depression'), L(10, 'Anticyclone')),
      (S(7, '(ii) · Anticyclone', 'Q.11 (i)'),),
      (fixed('Name', 2, '(ii) · Anticyclone · 2m'),), '2-7', WEATHER, ID + 'p1-q10-ii', False, ('page',)),
]

for index, (roman, prompt, start, nxt, answer, label, topic, atlas) in enumerate([
        ('(i)', '(i) What percentage (%) of the Irish workforce were working from home?', 'Q.11 (i) 32 (%)',
         '(ii) · Monaghan', 'Q.11 (i) 32 (%) · 2m', 'Percentage', '2-0', GRAPH),
        ('(ii)', '(ii) Which area of Ireland had the lowest percentage (%) of people working from home?',
         '(ii) · Monaghan & Longford', '(iii) · Car', '(ii) · Monaghan & Longford · 2m', 'Area', '2-0', GRAPH),
        ('(iii)', '(iii) What was the main way of commuting to work?', '(iii) · Car', '(iv) · 2,320,297',
         '(iii) · Car · 2m', 'Main way', '2-0', GRAPH),
        ('(iv)', '(iv) How many people were employed in 2022?', '(iv) · 2,320,297', '(v) · Valid impact',
         '(iv) · 2,320,297 · 2m', 'People employed', '2-0', GRAPH),
        ('(v)', '(v) State one impact of Ireland having a large number of retired people.', '(v) · Valid impact',
         'Q.12 (i)', '(v) · Valid impact · 2m', 'One impact', '4-1', POP)]):
    PART_ONE.append(T(
        f'p1-11-{roman.strip("()")}', P1, '11', roman, 2, 11, L(11, 'Graphical Interpretation'),
        (L(11, prompt),), (S(7, start, nxt),), (fixed(label, 2, answer),), topic, atlas,
        ID + 'p1-q11' + ('' if index == 0 else f'-{roman.strip("()")}'), index == 0, ('page',), Q11S))

PART_ONE += [
    T('p1-12-i', P1, '12', '(i)', 8, 12, L(12, 'Satellite Interpretation'),
      (L(12, '(i) Match each of the images A, B, C and D with the description', 'table below.'),),
      (S(7, 'Q.12 (i) · D', '(ii) · Dormant'),),
      rows(['Q.12 (i) · D', 'A · 2m', 'C · 2m', 'B · 2m']), '2-8', AER, ID + 'p1-q12', True, ('page',), Q12S,
      row_labels=(L(12, 'Snowcapped Mount Elbrus, Russia'), L(12, 'Hurricane Debby, USA'),
                  L(12, 'Anak Krakatoa volcano, Indonesia'), L(12, 'River Kura, Azerbaijan'))),
    T('p1-12-ii', P1, '12', '(ii)', 2, 12, L(12, 'Satellite Interpretation'),
      (L(12, '(ii) What is the name given to a volcano that has not erupted', 'Tick (✓) the correct box.'),
       L(12, 'Dormant'), L(12, 'Extinct')),
      (S(7, '(ii) · Dormant'),),
      (fixed('Name', 2, '(ii) · Dormant · 2m'),), '0-7', EV, ID + 'p1-q12-ii', False, ('page',), Q12S),
]


# ---------------------------------------------------------------- Part Two --
def romans(q, page, title, stem, first_id, sources, parts, legacy_first=True):
    """Separately priced romans of one A/B/C part.
    parts: (sub, marks, prompt Lift, scheme slice(s), criteria, topic, atlas, extra stem Lifts)."""
    out = []
    for index, part in enumerate(parts):
        sub, marks, prompt, scheme, criteria, topic, atlas = part[:7]
        extra = part[7] if len(part) > 7 else ()
        scheme = scheme if isinstance(scheme, tuple) else (scheme,)
        roman = sub.strip('()')
        out.append(T(f'p2-{q.lower()}-{roman}', P2, q, sub, marks, page, title, (prompt,), scheme,
                     criteria, topic, atlas, first_id if index == 0 else f'{first_id}-{roman}',
                     index == 0 and legacy_first, sources, (*stem, *extra)))
    return out


def sketch(page, title, prompt, scheme_page, card_id, topic, atlas, sources, bullets):
    item = sums((0, 1, 3), (0, 2))
    return T(f'p2-{card_id.rsplit("-q", 1)[1]}', P2, card_id.rsplit('-q', 1)[1].upper(), '', 30, page,
             title, (prompt,), (S(scheme_page, 'Sketch Outline:', 'Total 30m'),),
             (fixed('Limits/frame', 1, ('Sketch Outline:', 'imits/')),
              fixed('Proportions (landscape)', 2, 'Proportions (landscape) · 2m'),
              fixed('Overall impression', 2, '2m graded (2/1/0)', (0, 1, 2)),
              *(Criterion(f'Item {n}', 5, item, 'exact',
                          ('Five items shown and labelled as follows:', 'Showing · 3m graded (3/1/0)',
                           'Labelled · 2m')) for n in range(1, 6))),
             topic, atlas, card_id, False, sources,
             row_labels=(None, None, None, *(L(page, b) for b in bullets)))


def two_of(label, count, head, each, lines, unit):
    per = sums(*unit)
    return tuple(Criterion(f'{label} {n}', count, per, 'srp', (head, each, *lines)) for n in (1, 2))


PART_TWO = [
    sketch(3, L(3, 'Ordnance Survey Map'),
           L(3, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper.', 'Inishshanboe Island.'),
           9, ID + 'p2-q1a', '2-6', MAP, ('map', 'legend'),
           ('Lough Corrib', 'The N59 road', 'An area of coniferous plantation in the south east of the map',
            'The entire area of land above 200 metres at M 03 42', 'Inishshanboe Island')),
    T('p2-1b', P2, '1B', '', 40, 3, L(3, 'Landform Development'),
      (L(3, '(i) Explain, with the aid of diagrams, the formation of any two landforms.'),),
      (S(10, 'Formation of any two landforms @ 20m each.', 'Or'),),
      two_of('Landform', 20, 'Formation of any two landforms @ 20m each.', 'For each landform:',
             ('Landform named · 1m', 'Diagram(s) two aspects @ 2m each · 4m',
              'Formation explained 5 SRP’s @ 3m each · 15m'),
             ((0, 1), (0, 2, 4), steps(15, 3))),
      '0-4', PS_SURFACE, ID + 'p2-q1b-route-i', True,
      routes=(
          Route('route-i', 'Route (i)', ID + 'p2-q1b-route-i', True),
          Route('route-ii', 'Route (ii)', ID + 'p2-q1b-route-ii', True,
                prompt=(L(3, '(ii) Describe and explain any two processes of mass movement.'),),
                scheme=(S(10, 'Any two processes @ 20m each', 'Total 40m'),),
                criteria=two_of('Process', 20, 'Any two processes @ 20m each', 'For each process:',
                                ('Process stated · 2m', 'Description / Explanation 6 SRP’s @ 3m each · 18m'),
                                ((0, 2), steps(18, 3))),
                topic='0-8', atlas=RW),
      )),
    T('p2-1c', P2, '1C', '', 30, 3, L(3, 'Human Interaction with the Rock Cycle'),
      (L(3, 'Describe and explain how humans interact with the rock cycle with reference to',
         'Geothermal energy production.'),),
      (S(11, 'Description / explanation 10 SRP’s @ 3m each.', 'Total 30m'),),
      (srp3('Description/explanation', 10, 'Description / explanation 10 SRP’s @ 3m each.'),),
      '0-6', RW, ID + 'p2-q1c-quarrying', True,
      routes=bullet_routes('p2-q1c-', ('Quarrying', 'Mining', 'Oil/Gas exploitation',
                                       'Geothermal energy production.'))),
]

Q2AS = (L(4, 'Examine the report above and answer each of the following questions.'),)
PART_TWO += romans('2A', 4, L(4, 'Volcanoes', nth=0), Q2AS, ID + 'p2-q2a', ('page',), [
    ('(i)', 6, L(4, '(i) In which ocean is Hawaii located?'),
     S(12, 'Pacific · 6m', '(ii) · What is responsible'), (fixed('Ocean', 6, 'Pacific · 6m'),), '0-7', EV),
    ('(ii)', 6, L(4, '(ii) What is responsible for the eruptions mentioned in the article?'),
     S(12, 'Hotspot · 6m', '(iii) How many times'), (fixed('Cause', 6, 'Hotspot · 6m'),), '0-7', EV),
    ('(iii)', 6, L(4, '(iii) How many times did Kilauea erupt in 2024?'),
     S(12, 'Three · 6m', '(iv) · List two effects'), (fixed('Number of eruptions', 6, 'Three · 6m'),), '0-7', EV),
    ('(iv)', 6, L(4, '(iv) List two effects of a volcanic eruption.'),
     S(12, 'Valid effects listed', '(v) · Explain briefly'),
     (fixed('Two effects', 6, 'Valid effects listed · 3m+3m', (0, 3, 6)),), '0-7', EV),
    ('(v)', 6, L(4, '(v) Explain briefly one way to limit the damage caused by a volcanic eruption.'),
     S(12, 'Brief explanation two SRP', 'Total 30m'),
     (srp3('Brief explanation', 2, 'Brief explanation two SRP’s @ 3m each · 6m'),), '0-7', EV),
])
PART_TWO += romans('2B', 4, L(4, 'Rocks'), (), ID + 'p2-q2b', (), [
    ('(i)', 6, L(4, '(i) Name two examples of sedimentary rocks.'),
     S(12, 'Sedimentary rocks named', '(ii) · State two uses'),
     (fixed('Two sedimentary rocks', 6, 'Sedimentary rocks named · 3m+3m', (0, 3, 6)),), '0-1', RW),
    ('(ii)', 7, L(4, '(ii) State two uses of sedimentary rocks.'),
     S(13, 'Valid uses stated', '(iii) Describe and explain'),
     (fixed('Two uses', 7, 'Valid uses stated · 4m+3m', (0, 3, 4, 7)),), '0-1', RW),
    ('(iii)', 27, L(4, '(iii) Describe and explain how sedimentary rocks are formed.'),
     S(13, 'Description/Explanation 9 SRP', 'Total 40m'),
     (srp3('Description/explanation', 9, 'Description/Explanation 9 SRP’s @ 3m each · 27m'),), '0-1', RW),
])
SURFACE = ('River processes', 'Coastal processes', 'Mass movement processes.')
PART_TWO.append(T(
    'p2-2c', P2, '2C', '', 30, 4, L(4, 'Human Interaction with Surface Processes'),
    (L(4, 'Examine how humans interact with one of the following surface processes:', 'Mass movement processes.'),),
    (S(13, 'Interaction identified · 3m', 'Total 30m'),),
    (fixed('Interaction identified', 3, 'Interaction identified · 3m'),
     srp3('Explanation', 9, 'Explanation 9 SRP’s @ 3m each · 27m')),
    '0-6', RIVERS, ID + 'p2-q2c-river-processes', True,
    routes=bullet_routes('p2-q2c-', SURFACE, atlas=dict(zip(SURFACE, (RIVERS, SEA, RW))))))

Q3AS = (L(5, 'Examine the photographs above and answer each of the following questions.'),)
PART_TWO += romans('3A', 5, L(5, 'Surface Processes'), Q3AS, ID + 'p2-q3a', ('page',), [
    ('(i)', 9, L(5, '(i) In your answer book, match each of the letters A, B and C', 'Beach.'),
     S(14, '• B Waterfall', '(ii) · In your answer book'),
     (fixed('Row 1', 3, ('• B Waterfall', '=3m@0')), fixed('Row 2', 3, ('• C Landslide', '=3m@1')),
      fixed('Row 3', 3, ('• A Beach.', '=3m@2'))), '0-4', RIVERS + SEA + RW),
    ('(ii)', 9, L(5, '(ii) In your answer book, match each of the letters A, B and C', 'Mass movement.'),
     S(14, '• A Coastal deposition', '(iii) Name one process'),
     (fixed('Row 1', 3, ('• A Coastal deposition', '=3m@0')), fixed('Row 2', 3, ('• B River erosion', '=3m@1')),
      fixed('Row 3', 3, ('• C Mass movement.', '=3m@2'))), '0-4', RIVERS + SEA + RW),
    ('(iii)', 6, L(5, '(iii) Name one process of river erosion.'),
     S(14, 'Valid process named', '(iv) Explain briefly'),
     (fixed('River erosion process', 6, 'Valid process named · 6m'),), '0-9', RIVERS),
    ('(iv)', 6, L(5, '(iv) Explain briefly the process of longshore drift.'),
     S(14, 'Brief explanation · 2 SRP', 'Total 30m'),
     (srp3('Brief explanation', 2, 'Brief explanation · 2 SRP’s @ 3m each · 6m'),), '0-10', SEA),
])
# 3A row labels follow the printed list order of each roman.
PART_TWO[-4] = Task(**{**PART_TWO[-4].__dict__, 'row_labels': (L(5, 'Waterfall'), L(5, 'Landslide'), L(5, 'Beach'))})
PART_TWO[-3] = Task(**{**PART_TWO[-3].__dict__, 'row_labels': (L(5, 'Coastal deposition'), L(5, 'River erosion'), L(5, 'Mass movement'))})

WEATHERING = ('Freeze-thaw action', 'Carbonation', 'Onion weathering.')
PART_TWO += [
    T('p2-3b-i', P2, '3B', '(i)', 4, 5, L(5, 'Weathering'),
      (L(5, '(i) Name any two factors that influence weathering.'),),
      (S(14, 'Two valid factors named @ 2m each'),),
      (fixed('Two factors', 4, 'Two valid factors named @ 2m each · 4m', (0, 2, 4)),),
      '0-8', RW, ID + 'p2-q3b-i', False),
    T('p2-3b-ii', P2, '3B', '(ii)', 36, 5, L(5, 'Weathering'),
      (L(5, '(ii) Describe and explain any two of the following types of weathering:', 'Onion weathering.'),),
      (S(15, 'Weathering type 1 explained', 'Total 40m'),),
      (srp3('Weathering type 1 explained', 6, 'Weathering type 1 explained 6 SRP’s @ 3m each · 18m'),
       srp3('Weathering type 2 explained', 6, 'Weathering type 2 explained 6 SRP’s @ 3m each · 18m')),
      '0-8', RW, ID + 'p2-q3b-freeze-thaw-action-carbonation', True,
      routes=bullet_routes('p2-q3b-', WEATHERING, 2)),
]
PART_TWO += romans('3C', 5, L(5, 'Plate Tectonics'), (), ID + 'p2-q3c', (), [
    ('(i)', 6, L(5, '(i) Name two examples of tectonic plates.'),
     S(15, 'Two valid tectonic plates named', '(ii) · Name two types'),
     (fixed('Two tectonic plates', 6, 'Two valid tectonic plates named · 3m+3m', (0, 3, 6)),), '0-0', PS),
    ('(ii)', 6, L(5, '(ii) Name two types of plate boundary.'),
     S(15, 'Two valid types of plate boundary named', '(iii) Describe and explain'),
     (fixed('Two types of plate boundary', 6, 'Two valid types of plate boundary named · 3m+3m', (0, 3, 6)),),
     '0-0', PS),
    ('(iii)', 18, L(5, '(iii) Describe and explain what happens at plate boundaries.'),
     S(15, 'Description / explanation 6 SRP', 'Total 30m'),
     (srp3('Description/explanation', 6, 'Description / explanation 6 SRP’s @ 3m each. · 18m'),), '0-0', PS),
])

SHOWN = 'Shown · 4m graded (4/2/0)'
NAMED_SHOWN = sums((0, 2), (0, 2, 4))
PART_TWO.append(T(
    'p2-4a', P2, '4A', '', 30, 6, L(6, 'European Region'),
    (L(6, 'Draw a sketch map of a European region (not in Ireland) that you have studied.', 'in this region.'),),
    (S(16, 'Outline of Region', 'Total 30m'),),
    (fixed('Outline of region', 6, 'Outline of Region · 6m graded (6/4/2/0)', (0, 2, 4, 6)),
     Criterion('River', 6, NAMED_SHOWN, 'exact', ('River: · Named · 2m', f'={SHOWN}@0')),
     Criterion('Town/City 1', 6, NAMED_SHOWN, 'exact', ('Town/City 1: · Named · 2m', f'={SHOWN}@1')),
     Criterion('Town/City 2', 6, NAMED_SHOWN, 'exact', ('Town/City 2: · Named · 2m', f'={SHOWN}@2')),
     Criterion('Relief (upland/lowland)', 6, NAMED_SHOWN, 'exact',
               ('Relief (upland/lowland): · Named · 2m', f'={SHOWN}@3'))),
    '1-5', EURO, ID + 'p2-q4a', True))

Q4BS = (L(6, 'Answer each of the following questions with reference to an Irish region', 'studied.'),)
Q4BI = L(6, '(i) Name one example of a secondary economic activity in this region.')
PART_TWO += romans('4B', 6, L(6, 'Secondary Economic Activity in an Irish Region'), Q4BS, ID + 'p2-q4b', (), [
    ('(i)', 4, Q4BI, S(16, 'One valid secondary economic activity named'),
     (fixed('Secondary economic activity named', 4, 'One valid secondary economic activity named · 4m'),),
     '1-4', IRL),
    ('(ii)', 27, L(6, '(ii) Explain the advantages that this region has for the development of this secondary',
                   'economic activity.'),
     S(17, 'Explanation 9 SRP', '(iii) Describe one challenge'),
     (srp3('Explanation', 9, 'Explanation 9 SRP’s @ 3m each · 27m'),), '1-4', IRL, (Q4BI,)),
    ('(iii)', 9, L(6, '(iii) Describe one challenge faced by this secondary economic activity in this region.'),
     S(17, 'Description 3 SRP', 'Total 40m'),
     (srp3('Description', 3, 'Description 3 SRP’s @ 3m each · 9m'),), '1-4', IRL, (Q4BI,)),
])
PART_TWO.append(T(
    'p2-4c', P2, '4C', '', 30, 6, L(6, 'Regions and Culture'),
    (L(6, 'The culture of a region can often be determined by the following factors:'),
     L(6, 'Religion', 'Sport/Games'),
     L(6, 'Describe and explain the importance of culture in any one region that you have studied.')),
    (S(17, 'Description/explanation 10 SRP', 'Total 30m'),),
    (srp3('Description/explanation', 10, 'Description/explanation 10 SRP’s @ 3m each'),),
    '1-3', IRL + EURO + CONT, ID + 'p2-q4c', True))

Q5AS = (L(7, 'Examine the chart above showing the average size of Irish farms', 'following questions.'),)
PART_TWO += romans('5A', 7, L(7, 'Agriculture in Ireland'), Q5AS, ID + 'p2-q5a', ('page',), [
    ('(i)', 6, L(7, '(i) Which farm type had the smallest average farm size?'),
     S(18, 'Cattle · 6m', '(ii) · What was the average'), (fixed('Farm type', 6, 'Cattle · 6m'),), '2-0', GRAPH),
    ('(ii)', 6, L(7, '(ii) What was the average size (in hectares) of tillage farms?'),
     S(18, '73 (ha) · 6m', '(iii) Calculate'), (fixed('Average size', 6, '73 (ha) · 6m'),), '2-0', GRAPH),
    ('(iii)', 6, L(7, '(iii) Calculate the difference (in hectares) between the average dairy farm size and the',
                   'average sheep farm size.'),
     S(18, '21 (ha) · 6m', '(iv) State two products'), (fixed('Difference', 6, '21 (ha) · 6m'),), '2-0', GRAPH),
    ('(iv)', 6, L(7, '(iv) State two products made from the output of a dairy farm.'),
     S(18, 'Two valid products stated', '(v) · Briefly explain'),
     (fixed('Two products', 6, 'Two valid products stated · 3m+3m', (0, 3, 6)),), '1-4', IRL),
    ('(v)', 6, L(7, '(v) Briefly explain the importance of farming to the Irish economy.'),
     S(18, 'Brief explanation · 2 SRP', 'Total 30m'),
     (srp3('Brief explanation', 2, 'Brief explanation · 2 SRP’s @ 3m each · 6m'),), '1-4', IRL),
])
ACTIVITIES = ('The reasons why tourists are attracted to the region',
              'The importance of manufacturing to the region',
              'The development of transport in the region.')
PART_TWO.append(T(
    'p2-5b', P2, '5B', '', 40, 7, L(7, 'Economic Activities – European Region'),
    (L(7, 'Explain the development of any two of the following with reference to a European region',
       'The development of transport in the region.'),),
    (S(19, 'Activity 1 explained', 'Total 40m'),),
    (srp3('Activity 1 explained', 7, 'Activity 1 explained 7 SRP’s @ 3m each · 21m'),
     srp3('Activity 2 explained', 6, 'Activity 2 explained 6 SRP’s @ 3m each · 18m'),
     fixed('Region named', 1, 'Region named · 1m')),
    '1-5', EURO, ID + 'p2-q5b-' + chosen(ACTIVITIES, 2)[0][2], True,
    routes=bullet_routes('p2-q5b-', ACTIVITIES, 2)))
PART_TWO.append(T(
    'p2-5c', P2, '5C', '', 30, 7, L(7, 'Regional Problems'),
    (L(7, 'Describe and explain two problems faced by any region that you have studied.'),),
    (S(19, 'Problem 1', 'Total 30m'),),
    (srp3('Problem 1', 5, ('Problem 1', '=Description/Explanation 5 SRP’s @ 3m each · 15m@0')),
     srp3('Problem 2', 5, ('Problem 2', '=Description/Explanation 5 SRP’s @ 3m each · 15m@1'))),
    '1-0', IRL + EURO + CONT, ID + 'p2-q5c', True))

Q6AS = (L(8, 'Examine the table above with information on the percentage (%) of working population in',
          'questions.'),)
PART_TWO += romans('6A', 8, L(8, 'Employment in Europe'), Q6AS, ID + 'p2-q6a', ('page',), [
    ('(i)', 6, L(8, '(i) What percentage (%) of Ireland’s male working population were in employment?'),
     S(20, '84 (%) · 6m', '(ii) · In which country'), (fixed('Percentage', 6, '84 (%) · 6m'),), '2-0', GRAPH),
    ('(ii)', 6, L(8, '(ii) In which country were 78% of the female working population in employment?'),
     S(20, 'Finland · 6m', '(iii) · Calculate'), (fixed('Country', 6, 'Finland · 6m'),), '2-0', GRAPH),
    ('(iii)', 6, L(8, '(iii) Calculate the difference between the percentage (%) of the male working population',
                   'employment in Italy.'),
     S(20, '19 (%) · 6m', '(iv) · State two benefits'), (fixed('Difference', 6, '19 (%) · 6m'),), '2-0', GRAPH),
    ('(iv)', 6, L(8, '(iv) State two benefits to a country of a high percentage of its working population',
                  'being in employment.'),
     S(20, 'Two valid benefits stated', '(v) · Explain briefly'),
     (fixed('Two benefits', 6, 'Two valid benefits stated · 3m+3m', (0, 3, 6)),), '1-5', EURO),
    ('(v)', 6, L(8, '(v) Explain briefly one reason why the percentage of males in employment is often higher',
                 'females in employment.'),
     S(20, 'Brief explanation · 2 SRP', 'Total 30m'),
     (srp3('Brief explanation', 2, 'Brief explanation · 2 SRP’s @ 3m each · 6m'),), '1-5', EURO),
])
Q6BS = (L(8, 'Answer each of the following questions with reference to a Continental / Sub-Continental',
          'that you have studied.'),)
Q6BI = L(8, '(i) Name one primary economic activity that contributes to the economy of this region.')
PART_TWO += romans('6B', 8, L(8, 'Primary Economic Activity in a Continental / Sub-Continental Region'), Q6BS,
                   ID + 'p2-q6b', (), [
    ('(i)', 4, Q6BI, S(21, 'One valid primary economic activity named', '(ii) · Explain the advantages'),
     (fixed('Primary economic activity named', 4, 'One valid primary economic activity named · 4m'),), '1-6', CONT),
    ('(ii)', 27, L(8, '(ii) Explain the advantages that this region has for the development of the primary',
                   'named in part (i) above.'),
     S(21, 'Explanation 9 SRP', '(iii) Describe one problem'),
     (srp3('Explanation', 9, 'Explanation 9 SRP’s @ 3m each · 27m'),), '1-6', CONT, (Q6BI,)),
    ('(iii)', 9, L(8, '(iii) Describe one problem faced by this primary economic activity in this region.'),
     S(21, 'Description 3 SRP', 'Total 40m'),
     (srp3('Description', 3, 'Description 3 SRP’s @ 3m each · 9m'),), '1-6', CONT, (Q6BI,)),
])
PART_TWO.append(T(
    'p2-6c', P2, '6C', '', 30, 8, L(8, 'Urban Regions'),
    (L(8, 'Describe and explain the reasons for the growth of any one urban area that you have', 'studied.'),),
    (S(21, 'Description/explanation 10 SRP', 'Total 30m'),),
    (srp3('Description/explanation', 10, 'Description/explanation 10 SRP’s @ 3m each'),),
    '1-3', IRL + EURO, ID + 'p2-q6c', True))

PART_TWO.append(sketch(
    10, L(10, 'Aerial Photograph'),
    L(10, 'Examine the aerial photograph of Oughterard accompanying this paper.', 'A sports ground.'),
    23, ID + 'p2-q7a', '2-8', AER, ('aerial',),
    ('A lake in the background', 'Two connecting streets in the left foreground',
     'A field used for agriculture in the right background', 'An industrial building in the centre middleground',
     'A sports ground')))
Q7BI = L(10, '(i) Name one example of environmental pollution caused by economic activity.')
PART_TWO += romans('7B', 10, L(10, 'Economic Activity - Environmental Pollution'), (), ID + 'p2-q7b', (), [
    ('(i)', 4, Q7BI, S(23, 'Valid example named · 4m', '(ii) · Explain the causes'),
     (fixed('Example named', 4, 'Valid example named · 4m'),), '3-4', ENV),
    ('(ii)', 24, L(10, '(ii) Explain the causes and effects of this environmental pollution.'),
     (S(23, 'Cause identified one SRP'), S(24, 'Effect identified one SRP', '(iii) Describe how')),
     (fixed('Cause identified', 3, 'Cause identified one SRP @ 3m each · 3m'),
      fixed('Effect identified', 3, 'Effect identified one SRP @ 3m each · 3m'),
      srp3('Explanation', 6, 'Explanation 6 SRP’s @ 3m each · 18m')), '3-4', ENV, (Q7BI,)),
    ('(iii)', 12, L(10, '(iii) Describe how this environmental pollution could be reduced.'),
     S(24, 'Description 4 SRP', 'Total 40m'),
     (srp3('Description', 4, 'Description 4 SRP’s @ 3m each · 12m'),), '3-4', ENV, (Q7BI,)),
])
PART_TWO.append(T(
    'p2-7c', P2, '7C', '', 30, 10, L(10, 'Economic Development – Developed Economy'),
    (L(10, 'Describe and explain the development of one of the following economic activities with',
       'Service and footloose industries.'),),
    (S(24, 'Named developed economy', 'Total 30m'),),
    (fixed('Named developed economy', 3, 'Named developed economy · 3m'),
     srp3('Description/explanation', 9, 'Description/explanation 9 SRP’s @ 3m each · 27m')),
    '3-0', ECON, ID + 'p2-q7c-tourism', True,
    routes=bullet_routes('p2-q7c-', ('Tourism', 'Financial services', 'Service and footloose industries.'))))

Q8AS = (L(11, 'Examine the table above showing the number of new jobs created by the IDA', 'following questions.'),)
PART_TWO += romans('8A', 11, L(11, 'Employment in Ireland'), Q8AS, ID + 'p2-q8a', ('page',), [
    ('(i)', 6, L(11, '(i) How many new jobs were created in Limerick in 2020?'),
     S(25, '787 · 6m', '(ii) · Which county'), (fixed('New jobs', 6, '787 · 6m'),), '2-0', GRAPH),
    ('(ii)', 6, L(11, '(ii) Which county had the lowest number of new jobs created in 2018?'),
     S(25, 'Cavan · 6m', '(iii) Which county'), (fixed('County', 6, 'Cavan · 6m'),), '2-0', GRAPH),
    ('(iii)', 6, L(11, '(iii) Which county had 126 new jobs created in 2022?'),
     S(25, 'Roscommon · 6m', '(iv) Calculate'), (fixed('County', 6, 'Roscommon · 6m'),), '2-0', GRAPH),
    ('(iv)', 6, L(11, '(iv) Calculate the difference between the number of new jobs created in Dublin in 2020',
                  'and 2022.'),
     S(25, '5,033 · 6m', '(v) · Explain briefly'), (fixed('Difference', 6, '5,033 · 6m'),), '2-0', GRAPH),
    ('(v)', 6, L(11, '(v) Explain briefly why the number of new jobs created in Dublin and Limerick is much',
                 'Cavan and Roscommon.'),
     S(25, 'Brief explanation · 2 SRP', 'Total 30m'),
     (srp3('Brief explanation', 2, 'Brief explanation · 2 SRP’s @ 3m each · 6m'),), '3-0', ECON),
])
Q8BS = (L(11, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper.'),
        L(11, 'Imagine you have been given the task', 'the area covered by the map.'))
Q8BI = L(11, '(i) State, using a six-figure grid reference, where you would locate the factory.')
PART_TWO += romans('8B', 11, L(11, 'Ordnance Survey Map'), Q8BS, ID + 'p2-q8b', ('map', 'legend'), [
    ('(i)', 4, Q8BI, S(25, 'Six-figure grid reference', '(ii) · Explain the reasons'),
     (fixed('Six-figure grid reference', 4, 'Six-figure grid reference · 4m graded (4/2/0)', (0, 2, 4)),),
     '2-6', MAP),
    ('(ii)', 27, L(11, '(ii) Explain the reasons why you chose this location.'),
     S(25, 'Reasons explained 9 SRP'),
     (srp3('Reasons explained', 9, 'Reasons explained 9 SRP’s @ 3m each · 27m'),), '3-0', ECON + MAP, (Q8BI,)),
    ('(iii)', 9, L(11, '(iii) Describe one disadvantage of locating the factory at this location.'),
     S(26, 'One disadvantage described', 'Total 40m'),
     (srp3('One disadvantage described', 3, 'One disadvantage described 3 SRP’s @ 3m each · 9m'),),
     '3-0', ECON + MAP, (Q8BI,)),
], legacy_first=False)
Q8CI = L(11, '(i) Name one developing economy which has been colonised and name the country', 'that colonised it.')
PART_TWO += romans('8C', 11, L(11, 'Colonialism'), (), ID + 'p2-q8c', (), [
    ('(i)', 6, Q8CI, S(26, 'Valid colonised country', '(ii) · Describe and explain'),
     (fixed('Colonised country', 3, 'Valid colonised country · 3m'),
      fixed('Colonising country', 3, 'Valid colonising country · 3m')), '3-1', DEV),
    ('(ii)', 24, L(11, '(ii) Describe and explain the effects that colonialism has had on this developing economy.'),
     S(26, 'Description / Explanation 8 SRP', 'Total 30m'),
     (srp3('Description/explanation', 8, 'Description / Explanation 8 SRP’s @ 3m each · 24m'),), '3-1', DEV, (Q8CI,)),
])

GRAPH_OL = (fixed('Graph paper', 3, 'Graph paper · 3m', (0, 3)),
            fixed('Vertical axis labelled / circle', 3, 'Vertical axis labelled/Circle · 3m graded (3/1/0)', (0, 1, 3)),
            fixed('Horizontal axis labelled / centred', 3, 'Horizontal axis labelled/Centred · 3m graded (3/1/0)', (0, 1, 3)),
            fixed('5 items illustrated', 15, '5 items @ 3m each graded (3/1/0) · 15m', sums(*[(0, 1, 3)] * 5)))
Q9AS = (L(12, 'Examine the data above on new car registrations in Ireland', 'following questions.'),)
PART_TWO += romans('9A', 12, L(12, 'Ireland’s Economy'), Q9AS, ID + 'p2-q9a', ('page',), [
    ('(i)', 24, L(12, '(i) Using graph paper, draw a suitable graph to illustrate this data.'),
     S(27, 'Graph paper · 3m', '(ii) · In your answer book'), GRAPH_OL, '2-0', GRAPH),
    ('(ii)', 6, L(12, '(ii) In your answer book, explain briefly what is meant by the term renewable energy.'),
     S(27, 'Brief explanation 2 SRP', 'Total 30m'),
     (srp3('Brief explanation', 2, 'Brief explanation 2 SRP’s @ 3m each · 6m'),), '3-5', ECON),
])
Q9BI = L(12, '(i) Name one multinational company that you have studied and state where this', 'located in Ireland.')
PART_TWO += romans('9B', 12, L(12, 'Multinational Company'), (), ID + 'p2-q9b', (), [
    ('(i)', 4, Q9BI, S(28, 'Valid MNC named', '(ii) · Name one product'),
     (fixed('MNC named', 2, 'Valid MNC named · 2m'), fixed('Location stated', 2, 'Valid location stated · 2m')),
     '3-2', MNC),
    ('(ii)', 6, L(12, '(ii) Name one product manufactured by this multinational company and name one',
                  'where this product is sold.'),
     S(28, 'Valid product named', '(iii) Explain the advantages'),
     (fixed('Product named', 3, 'Valid product named · 3m'), fixed('Country named', 3, 'Valid country named · 3m')),
     '3-2', MNC, (Q9BI,)),
    ('(iii)', 21, L(12, '(iii) Explain the advantages of being located in Ireland for this multinational company.'),
     S(28, 'Explanation 7 SRP', '(iv) Explain one reason'),
     (srp3('Explanation', 7, 'Explanation 7 SRP’s @ 3m each · 21m'),), '3-2', MNC, (Q9BI,)),
    ('(iv)', 9, L(12, '(iv) Explain one reason why this multinational company might decide to locate to another',
                  'country.'),
     S(28, 'Explanation 3 SRP', 'Total 40m'),
     (srp3('Explanation', 3, 'Explanation 3 SRP’s @ 3m each · 9m'),), '3-2', MNC, (Q9BI,)),
])
PART_TWO.append(T(
    'p2-9c', P2, '9C', '', 30, 12, L(12, 'Ireland and the European Union'),
    (L(12, 'Explain how being a member of the European Union has impacted on the Irish economy.'),),
    (S(28, 'Impact Identified 1 SRP', 'Total 30m'),),
    (fixed('Impact identified', 3, 'Impact Identified 1 SRP · 3m'),
     srp3('Explanation', 9, 'Explanation 9 SRP’s @ 3m each · 27m')),
    '3-3', EU, ID + 'p2-q9c', True))

PART_TWO.append(sketch(
    13, L(13, 'Aerial Photograph'),
    L(13, 'Examine the aerial photograph of Oughterard accompanying this paper.', 'An area of recreational activity.'),
    29, ID + 'p2-q10a', '2-8', AER, ('aerial',),
    ('A car park', 'The Central Business District (CBD)', 'A church',
     'An area of semi-detached housing in the centre foreground', 'An area of recreational activity')))
Q10BS = (L(13, 'Migration takes place due to push factors and pull factors.'),)
PART_TWO += romans('10B', 13, L(13, 'Migration – Ireland'), Q10BS, ID + 'p2-q10b', (), [
    ('(i)', 4, L(13, '(i) Name one push factor and one pull factor associated with migration.'),
     S(30, 'Push factor named', '(ii) · Discuss the positive'),
     (fixed('Push factor named', 2, 'Push factor named · 2m'), fixed('Pull factor named', 2, 'Pull factor named · 2m')),
     '4-2', POP),
    ('(ii)', 18, L(13, '(ii) Discuss the positive impacts of migration on Ireland.'),
     S(30, 'Discussion 6 SRP', '(iii) Discuss the negative', after='(ii) · Discuss the positive'),
     (srp3('Discussion', 6, 'Discussion 6 SRP’s @ 3m each · 18m'),), '4-2', POP),
    ('(iii)', 18, L(13, '(iii) Discuss the negative impacts of migration on Ireland.'),
     S(30, 'Discussion 6 SRP', 'Total 40m', after='(iii) Discuss the negative'),
     (srp3('Discussion', 6, 'Discussion 6 SRP’s @ 3m each · 18m'),), '4-2', POP),
])
PART_TWO += romans('10C', 13, L(13, 'Traffic Congestion'), (), ID + 'p2-q10c', (), [
    ('(i)', 3, L(13, '(i) Name one example of an urban area where traffic congestion is a problem.'),
     S(30, 'Named example · 3m', '(ii) · Describe and explain'),
     (fixed('Urban area named', 3, 'Named example · 3m'),), '4-5', URB),
    ('(ii)', 27, L(13, '(ii) Describe and explain the measures that can be taken in urban areas to solve the',
                   'problem of traffic congestion.'),
     S(30, 'Description / Explanation 9 SRP', 'Total 30m'),
     (srp3('Description/explanation', 9, 'Description / Explanation 9 SRP’s @ 3m each 27m'),), '4-5', URB),
])

Q11AS = (L(14, 'Examine the table above showing population figures for selected European Union countries',
           'following questions.'),)
PART_TWO += romans('11A', 14, L(14, 'Population Characteristics'), Q11AS, ID + 'p2-q11a', ('page',), [
    ('(i)', 6, L(14, '(i) What was the population (in millions) of Ireland?'),
     S(31, '5.2 (millions) · 6m', '(ii) · Which country'), (fixed('Population', 6, '5.2 (millions) · 6m'),), '2-0', GRAPH),
    ('(ii)', 6, L(14, '(ii) Which country had the highest population density?'),
     S(31, 'Belgium · 6m', '(iii) In which country'), (fixed('Country', 6, 'Belgium · 6m'),), '2-0', GRAPH),
    ('(iii)', 6, L(14, '(iii) In which country was the birth rate 7.3?'),
     S(31, 'Greece · 6m', '(iv) Calculate'), (fixed('Country', 6, 'Greece · 6m'),), '2-0', GRAPH),
    ('(iv)', 6, L(14, '(iv) Calculate the difference (in millions) between the total population of Lithuania and the',
                  'total population of Greece.'),
     S(31, '7.7 (millions) · 6m', '(v) · Explain briefly'), (fixed('Difference', 6, '7.7 (millions) · 6m'),),
     '2-0', GRAPH),
    ('(v)', 6, L(14, '(v) Explain briefly one impact of high birth rates.'),
     S(31, 'Brief explanation 2 SRP', 'Total 30m'),
     (srp3('Brief explanation', 2, 'Brief explanation 2 SRP’s @ 3m each · 6m'),), '4-1', POP),
])
Q11BI = L(14, '(i) Name one city in the developing world that is growing rapidly.')
PART_TWO += romans('11B', 14, L(14, 'Developing World City'), (), ID + 'p2-q11b', (), [
    ('(i)', 4, Q11BI, S(32, 'Developing City named', '(ii) · State three factors'),
     (fixed('Developing world city named', 4, 'Developing City named · 4m'),), '4-5', URB),
    ('(ii)', 9, L(14, '(ii) State three factors that influence the growth of this developing world city.'),
     S(32, 'Factor 1:', '(iii) · Describe and explain'),
     (fixed('Factor 1', 3, 'Factor 1: · 3m'), fixed('Factor 2', 3, 'Factor 2: · 3m'),
      fixed('Factor 3', 3, 'Factor 3: · 3m')), '4-5', URB, (Q11BI,)),
    ('(iii)', 27, L(14, '(iii) Describe and explain any three problems associated with the rapid growth of this',
                    'developing world city.'),
     S(32, 'Description / Explanation 9 SRP', 'Total 40m'),
     (srp3('Description/explanation', 9, 'Description / Explanation 9 SRP’s @ 3m each · 27m'),), '4-5', URB, (Q11BI,)),
])
PART_TWO.append(T(
    'p2-11c', P2, '11C', '', 30, 14, L(14, 'Population Dynamics'),
    (L(14, '‘Population change is influenced by many factors', 'medical technology.’'),
     L(14, 'Describe and explain the factors that influence population change.')),
    (S(32, 'Factor named · 3m', 'Total 30m'),),
    (fixed('Factor named', 3, 'Factor named · 3m'),
     srp3('Description/explanation', 9, 'Description/explanation 9 SRP’s @ 3m each · 27m')),
    '4-0', POP, ID + 'p2-q11c', True))

Q12AS = (L(15, 'Examine the table above showing the percentage (%) of the global population living in urban',
           'following questions.'),)
PART_TWO += romans('12A', 15, L(15, 'Urban Population'), Q12AS, ID + 'p2-q12a', ('page',), [
    ('(i)', 24, L(15, '(i) Using graph paper, draw a suitable graph to illustrate this data.'),
     S(33, 'Graph paper · 3m', '(ii) · In your answer book'), GRAPH_OL, '2-0', GRAPH),
    ('(ii)', 6, L(15, '(ii) In your answer book, explain briefly one impact of an increasing percentage (%) of the',
                  'living in urban areas.'),
     S(33, 'Brief explanation 2 SRP', 'Total 30m'),
     (srp3('Brief explanation', 2, 'Brief explanation 2 SRP’s @ 3m each · 6m'),), '4-5', URB),
])
Q12BS = (L(15, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper and',
           'following questions.'),)
Q12BI = L(15, '(i) Name three different rural settlement patterns evident on the map', 'example of each.')
PART_TWO += romans('12B', 15, L(15, 'Rural Settlement Patterns'), Q12BS, ID + 'p2-q12b', ('map', 'legend'), [
    ('(i)', 22, Q12BI, S(34, 'Pattern 1 named:', '(ii) · Describe and explain'),
     (fixed('Pattern 1 named', 4, 'Pattern 1 named: · 4m'), fixed('Pattern 2 named', 3, 'Pattern 2 named: · 3m'),
      fixed('Pattern 3 named', 3, 'Pattern 3 named: · 3m'),
      fixed('Grid reference 1', 4, 'Grid reference 1: · 4m graded (4/2/0)', (0, 2, 4)),
      fixed('Grid reference 2', 4, 'Grid reference 2: · 4m graded (4/2/0)', (0, 2, 4)),
      fixed('Grid reference 3', 4, 'Grid reference 3: · 4m graded (4/2/0)', (0, 2, 4))), '4-3', URB + MAP),
    ('(ii)', 18, L(15, '(ii) Describe and explain each of the three rural settlement patterns named by you in',
                   'part (i) above.'),
     S(34, 'Description/explanation for each pattern:', 'Total 40m'),
     tuple(srp3(f'Pattern {n}', 2, ('Description/explanation for each pattern:', f'Pattern {n}: 2 SRP’s @ 3m each · 6m'))
           for n in (1, 2, 3)), '4-3', URB + MAP, (Q12BI,)),
], legacy_first=False)
Q12CI = L(15, '(i) Name one urban area you have studied.')
PART_TWO += romans('12C', 15, L(15, 'Urban Land-Use'), (), ID + 'p2-q12c', (), [
    ('(i)', 3, Q12CI, S(34, 'Valid urban area named', '(ii) · Name two land-uses'),
     (fixed('Urban area named', 3, 'Valid urban area named · 3m'),), '4-4', URB),
    ('(ii)', 6, L(15, '(ii) Name two land-uses in this urban area.'),
     S(34, 'Valid land-uses named', '(iii) · Describe and explain'),
     (fixed('Two land-uses', 6, 'Valid land-uses named · 3m+3m', (0, 3, 6)),), '4-4', URB, (Q12CI,)),
    ('(iii)', 21, L(15, '(iii) Describe and explain how these urban land-uses have changed over time.'),
     S(34, 'Description/explanation 7 SRP', 'Total 30m'),
     (srp3('Description/explanation', 7, 'Description/explanation 7 SRP’s @ 3m each · 21m'),), '4-4', URB, (Q12CI,)),
])

TASKS = [*PART_ONE, *PART_TWO]

# Every 2025 Ordinary card id shipped before this review (52). Each must survive.
LEGACY_IDS = [
    'geography-2025-ol-p1-q1',
    'geography-2025-ol-p1-q2',
    'geography-2025-ol-p1-q3',
    'geography-2025-ol-p1-q4',
    'geography-2025-ol-p1-q8',
    'geography-2025-ol-p1-q9',
    'geography-2025-ol-p1-q10',
    'geography-2025-ol-p1-q11',
    'geography-2025-ol-p1-q12',
    'geography-2025-ol-p2-q1b-route-i',
    'geography-2025-ol-p2-q1b-route-ii',
    'geography-2025-ol-p2-q1c-quarrying',
    'geography-2025-ol-p2-q1c-mining',
    'geography-2025-ol-p2-q1c-oil-gas-exploitation',
    'geography-2025-ol-p2-q1c-geothermal-energy-production',
    'geography-2025-ol-p2-q2a',
    'geography-2025-ol-p2-q2b',
    'geography-2025-ol-p2-q2c-river-processes',
    'geography-2025-ol-p2-q2c-coastal-processes',
    'geography-2025-ol-p2-q2c-mass-movement-processes',
    'geography-2025-ol-p2-q3a',
    'geography-2025-ol-p2-q3b-freeze-thaw-action-carbonation',
    'geography-2025-ol-p2-q3b-freeze-thaw-action-onion-weathering',
    'geography-2025-ol-p2-q3b-carbonation-onion-weathering',
    'geography-2025-ol-p2-q3c',
    'geography-2025-ol-p2-q4a',
    'geography-2025-ol-p2-q4b',
    'geography-2025-ol-p2-q4c',
    'geography-2025-ol-p2-q5a',
    'geography-2025-ol-p2-q5b-the-reasons-why-tourists-are-attra-the-importance-of-manufacturing-to',
    'geography-2025-ol-p2-q5b-the-reasons-why-tourists-are-attra-the-development-of-transport-in-th',
    'geography-2025-ol-p2-q5b-the-importance-of-manufacturing-to-the-development-of-transport-in-th',
    'geography-2025-ol-p2-q5c',
    'geography-2025-ol-p2-q6a',
    'geography-2025-ol-p2-q6b',
    'geography-2025-ol-p2-q6c',
    'geography-2025-ol-p2-q7b',
    'geography-2025-ol-p2-q7c-tourism',
    'geography-2025-ol-p2-q7c-financial-services',
    'geography-2025-ol-p2-q7c-service-and-footloose-industries',
    'geography-2025-ol-p2-q8a',
    'geography-2025-ol-p2-q8c',
    'geography-2025-ol-p2-q9a',
    'geography-2025-ol-p2-q9b',
    'geography-2025-ol-p2-q9c',
    'geography-2025-ol-p2-q10b',
    'geography-2025-ol-p2-q10c',
    'geography-2025-ol-p2-q11a',
    'geography-2025-ol-p2-q11b',
    'geography-2025-ol-p2-q11c',
    'geography-2025-ol-p2-q12a',
    'geography-2025-ol-p2-q12c',
]

ID_CORRECTION_REASON = (
    'The shipped card held every part of a question the scheme prices part by '
    'part. Its id is kept on the first separately priced part; the other parts '
    'are new cards with their own published allocation. The three shipped 3B '
    'cards held the whole 40m part; they are kept on the choose-two weathering '
    'routes of 3B(ii), and the separately priced 3B(i) is a new card.')
