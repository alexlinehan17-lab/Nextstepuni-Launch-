"""Independent review ledger: Leaving Certificate Geography 2024 Ordinary Level.

Sources (English editions, Paper Trail index; sizes and SHA-256 pinned in
EXPECTED_SOURCES and the generated audit): Part One and Answerbook
LC005GLP042EV (40 pages), Part Two LC005GLP043EV (20 pages), marking scheme
LC005GLP000EV (40 pages), and the common companions shared with Higher Level
— the 1:50 000 Bantry map LC005CLP003EV (fetched from Paper Trail storage),
its legend LC005CLPC00EV and the Bantry aerial photograph LC005CLP004EV
(published only as a JPEG).

Visual sweep (every page rendered and read on 2026-10-12):
  Part One booklet p1 cover (COVID-adjusted paper note); p2 instructions;
  p3-p12 Questions 1-12 (p7 holds Q5 and Q6, p8 holds Q7 and Q8); p13 Part
  Two answerbook instructions; p14-p17 graph-paper answer pages; p18-p39
  lined answer pages; p40 copyright/back cover.
  Part Two booklet p1 cover; p2 Part Two instructions ("attempt THREE");
  p3-p10 Sections 1-2 (Q1-Q6; p5 holds only 2C, p9 holds 5B and 5C); p11
  Section 3 divider; p12-p17 Electives (Q7-Q12); p18-p19 "Do not hand this
  up"; p20 copyright/back cover.
  Scheme p1 cover; p2-p3 notes; p4 annotation key; p5 Geographical
  Investigation (coursework, not a written-paper task); p6 presentation
  breakdown; p7-p8 Part One table; p9 the 2024 Part Two adjustment rule;
  p10-p22 Q1-Q6; p23 Section 3 divider; p24-p35 Q7-Q12; p36 investigation
  topics; p37 Irish-language bonus marks; p38-p39 blank; p40 back cover.
  Companions: Bantry map extract; OS legend sheet; oblique aerial
  photograph of Bantry.

Companions. Part One Q6 and Q7 (map, legend) and Q8 (aerial); Part Two 1A,
9B, 10A and 12C (map, legend), 7A and 11C (aerial) were held back before
this review because their companions were not wired. Each now carries the
exact official documents it names.

Boundaries follow the published allocation: at Ordinary Level the scheme
prices every printed roman of every A, B and C part, so each roman is its own
task. Part One romans and lettered true/false items are tasks; a matching
table under ONE printed instruction stays one task with a criterion per
scheme row, each row checked against the image: Q1 Mantle=D, Volcanic
activity=C, Subducting plate=B, Continental plate=A; Q2 Sandstone=B,
Limestone=A; Q3 Meander=C, Confluence=B, Tributary=A, Delta=D; Q4 Scree
slope=B, U-shaped valley=A, Terracette=C, Sand spit=D; Q5 Sambre Meuse=C,
London=B, Islamic World=A, Cool Temperate Oceanic=E, Meath County
Council=D; Q9 A Tertiary, B Primary, C Secondary, D Tertiary; Q10 Occluded
front=A, High=D, Low=B, Warm front=E, Isobar=C; Part Two 3A (i) C Mountain
range, A Volcanic island, B Rift valley and (ii) A Lava cooling, C Folding,
B Faulting. A part whose wording depends on an earlier part ("this
secondary economic activity", "this conflict", "this migration", "this
urban area", "this location") carries that earlier printed part in its stem.

Tariffs: an SRP is 3 marks at Ordinary Level; "a+b" lines are one criterion
with partial credit a; graded lines keep their printed grades; sketch items
are "showing 3 (3/1/0) + labelled 2"; 4A items are "named 2 + shown 4
(4/2/0)"; 11C reasons are "aerial photograph evidence 1 + 3 SRPs". Every
question totals 10 (Part One) or 100 (Part Two). In 2024 Question 12 prints
12B at 30 marks and 12C at 40 marks; the ledger follows the paper.
"""

import itertools

from geography_review import (
    Criterion, Lift, Route, SchemeSlice, Task, pool, fixed, slug, srp, steps, sums,
)

YEAR = 2024
LEVEL = 'ordinary'
PAPER_PAGES = {1: 40, 2: 20}
SCHEME_PAGES = 40
QUESTION_TARIFFS = {1: {str(n): 10 for n in range(1, 13)},
                    2: {**{f'{n}{x}': (40 if x == 'B' else 30)
                           for n in range(1, 13) for x in 'ABC'},
                        '12B': 30, '12C': 40}}

EXPECTED_SOURCES = {
    'paper1': ('LC005GLP042EV.pdf', 2977091),
    'paper2': ('LC005GLP043EV.pdf', 1800667),
    'scheme': ('LC005GLP000EV.pdf', 1355410),
    'map': ('LC005CLP003EV.pdf', 14358379),
    'legend': ('LC005CLPC00EV.pdf', 626267),
    'aerial': ('LC005CLP004EV.jpg', 5609640),
}

PAGE_REVIEW = {
    'paper1': {1: 'cover', 2: 'instructions', **{p: 'question' for p in range(3, 13)},
               13: 'answerbook instructions', **{p: 'graph-paper answer page' for p in range(14, 18)},
               **{p: 'lined answer page' for p in range(18, 40)}, 40: 'copyright/back cover'},
    'paper2': {1: 'cover', 2: 'Part Two instructions',
               **{p: 'question' for p in (3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17)},
               11: 'section divider', 18: 'do not hand this up', 19: 'do not hand this up',
               20: 'copyright/back cover'},
    'scheme': {1: 'cover', 2: 'notes', 3: 'notes', 4: 'annotation key',
               5: 'geographical investigation (coursework)', 6: 'investigation presentation breakdown',
               7: 'Part One table', 8: 'Part One table',
               9: 'Part Two adjustment rule (2024 additional choice)',
               **{p: 'Part Two allocation' for p in range(10, 23)}, 23: 'section divider',
               **{p: 'Part Two allocation' for p in range(24, 36)},
               36: 'investigation topics', 37: 'Irish-language bonus marks',
               38: 'blank', 39: 'blank', 40: 'back cover'},
}

EXPECTED_SELECTION_SCAN = [
    [1, 2, 'attempt any ten'], [1, 2, 'attempt three'], [1, 3, 'attempt any ten'],
    [1, 4, 'any two'],
    [2, 2, 'attempt three'],
    [2, 3, 'one of the following'],
    [2, 4, 'either'], [2, 4, 'answer (i) or (ii)'], [2, 4, 'any two'], [2, 4, 'any two'],
    [2, 5, 'one of the following'],
    [2, 7, 'any two'],
    [2, 9, 'any one'],
    [2, 10, 'any two'],
    [2, 12, 'any one'],
    [2, 13, 'one of the following'],
    [2, 17, 'any two'],
]
SELECTION_REVIEW = [
    {'scan': [[1, 2, 'attempt any ten'], [1, 2, 'attempt three'], [1, 3, 'attempt any ten'],
              [2, 2, 'attempt three']],
     'kind': 'exam-attempt-rule',
     'reason': 'Part One any ten of twelve and Part Two three questions are attempt rules; every question is carded.'},
    {'scan': [[2, 3, 'one of the following']], 'kind': 'closed-choose-one',
     'reason': '1C: one of three printed surface processes -> three routes.'},
    {'scan': [[2, 4, 'answer (i) or (ii)']], 'kind': 'closed-route',
     'reason': '2B: (i) or (ii) -> two routes, each with its own scheme allocation.'},
    {'scan': [[2, 5, 'one of the following']], 'kind': 'closed-choose-one',
     'reason': '2C: one of four printed bullets -> four routes.'},
    {'scan': [[2, 7, 'any two']], 'kind': 'choose-n-one-card',
     'reason': '4B: any two of three printed headings -> one card with every printed item (choice is not a route; the scheme marks each chosen item alike).'},
    {'scan': [[2, 10, 'any two']], 'kind': 'choose-n-one-card',
     'reason': '6C: any two of four printed region types -> one card with every printed item (choice is not a route; the scheme marks each chosen item alike).'},
    {'scan': [[2, 13, 'one of the following']], 'kind': 'closed-choose-one',
     'reason': '8C: one of three printed economic activities -> three routes.'},
    {'scan': [[2, 4, 'either']], 'kind': 'not-a-selection',
     'reason': '2A(ii) "found either side of the plate boundary" locates the plates; it offers no choice.'},
    {'scan': [[1, 4, 'any two'], [2, 4, 'any two'], [2, 4, 'any two'], [2, 9, 'any one'],
              [2, 12, 'any one'], [2, 17, 'any two']],
     'kind': 'open-response',
     'reason': 'No printed pool: Part One Q2(iii) any two metamorphic rocks; 2B(i) any two landforms and 2B(ii) any two mass movement processes (the scheme prices two @ 20m); 5C any one urban area in Ireland; 7C(i) any one EU policy; 12B(ii) any two functions. 3B "one surface feature" / "one underground feature" are open too.'},
]

P1, P2 = 1, 2
ID = 'geography-2024-ol-'
O = 'geography-ordinary-'
SRP3 = 3
SRPS = 'SRP’s'


def L(page, start, end=None, nth=None):
    return Lift(page, start, end, None, nth)


def S(page, start, end=None, clip=None, after=None, table=False):
    return SchemeSlice(page, start, end, clip, after, table)


def srp3(label, count, line):
    return srp(label, count, line, SRP3)


def T(key, part, q, sub, marks, page, title, prompt, scheme, criteria, topic, atlas, card_id,
      legacy, sources=(), stem=(), routes=(), row_labels=(), absorbs=()):
    return Task(key, part, q, sub, marks, page, title, prompt, scheme, criteria, topic, atlas,
                sources, card_id, legacy, stem=stem, routes=routes, row_labels=row_labels,
                absorbs=absorbs)


def rows(lines, marks=2):
    return tuple(fixed(f'Row {i}', marks, line) for i, line in enumerate(lines, 1))


def chosen(items, k):
    return [(combo, ' + '.join(item.rstrip('.') for item in combo),
             '-'.join(slug(item, 34) for item in combo))
            for combo in itertools.combinations(items, k)]


def bullet_routes(prefix, items, k=1, atlas=None, first_id=None):
    out = []
    for index, (combo, label, route_slug) in enumerate(chosen(items, k)):
        card_id = first_id if (first_id and index == 0) else ID + prefix + route_slug
        out.append(Route(route_slug, label, card_id, index == 0 or not first_id, keep_bullets=combo,
                         atlas=(atlas[combo[0]] if atlas else None)))
    return tuple(out)


TF = 'Indicate whether the following statement is true or false by ticking (✓) the correct box.'

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
PS_SURFACE = RIVERS + SEA + GLAC

# ---------------------------------------------------------------- Part One --
Q1S = (L(3, 'Examine the diagram above which shows a plate boundary', 'questions.'),)
Q2S = (L(4, 'Examine the map above showing the bedrock of Ireland', 'questions.'),)
Q3S = (L(5, 'Examine the diagram of a river profile above', 'following questions.'),)
Q4S = (L(6, 'Examine the photographs above and answer each of the following questions.'),)
Q6S = (L(7, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper, and',
         'following questions.'),)
Q7S = (L(8, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper and',
         'following questions.'),)
Q8S = (L(8, 'Examine the aerial photograph of Bantry accompanying this paper.'),
       L(8, 'Indicate whether the following statements are true or false', 'the correct box.'))
Q11S = (L(11, 'Examine the table above showing information on the area of forested land',
          'following questions.'),)
Q12S = (L(12, 'Examine the infographic above on housing in Ireland', 'following questions.'),)

PART_ONE = [
    T('p1-1-i', P1, '1', '(i)', 8, 3, L(3, 'Plate Tectonics'),
      (L(3, '(i) Match each of the letters A, B, C and D', 'below.'),),
      (S(7, 'Q.1 (i) · D', '(ii) · True'),),
      rows(['Q.1 (i) · D', 'C · 2m', 'B · 2m', 'A · 2m']), '0-0', PS, ID + 'p1-q1', True, ('page',), Q1S,
      row_labels=(L(3, 'Mantle'), L(3, 'Volcanic activity'), L(3, 'Subducting plate'), L(3, 'Continental plate'))),
    T('p1-1-ii', P1, '1', '(ii)', 2, 3, L(3, 'Plate Tectonics'),
      (L(3, '(ii) ' + TF), L(3, 'The diagram above shows an example of a destructive plate boundary.')),
      (S(7, '(ii) · True', 'Q.2 (i)'),),
      (fixed('True or false', 2, '(ii) · True'),), '0-0', PS, ID + 'p1-q1-ii', False, ('page',), Q1S),
    T('p1-2-i', P1, '2', '(i)', 4, 4, L(4, 'Rocks'),
      (L(4, '(i) Match each of the locations A and B on the map', 'rock type below.'),),
      (S(7, 'Q.2 (i) · B', '(ii) · Sedimentary'),),
      rows(['Q.2 (i) · B', 'A · 2m']), '0-1', RW, ID + 'p1-q2', True, ('page',), Q2S,
      row_labels=(L(4, 'Sandstone'), L(4, 'Limestone'))),
    T('p1-2-ii', P1, '2', '(ii)', 2, 4, L(4, 'Rocks'),
      (L(4, '(ii) Indicate, by ticking (✓) the correct box, whether limestone', 'sedimentary rocks.'),
       L(4, 'Igneous'), L(4, 'Sedimentary')),
      (S(7, '(ii) · Sedimentary', '(iii) · Two valid types'),),
      (fixed('Rock type', 2, '(ii) · Sedimentary · 2m'),), '0-1', RW, ID + 'p1-q2-ii', False, ('page',), Q2S),
    T('p1-2-iii', P1, '2', '(iii)', 4, 4, L(4, 'Rocks'),
      (L(4, '(iii) Name any two types of metamorphic rock.'),),
      (S(7, '(iii) · Two valid types', 'Q.3 (i)'),),
      (fixed('Two metamorphic rocks', 4, '(iii) · Two valid types · 2m+2m', (0, 2, 4)),),
      '0-1', RW, ID + 'p1-q2-iii', False, ('page',), Q2S),
    T('p1-3-i', P1, '3', '(i)', 8, 5, L(5, 'Rivers'),
      (L(5, '(i) Match each of the features labelled A, B, C and D', 'the table below.'),),
      (S(7, 'Q.3 (i) · C', '(ii) · False'),),
      rows(['Q.3 (i) · C', 'B · 2m', 'A · 2m', 'D · 2m']), '0-9', RIVERS, ID + 'p1-q3', True, ('page',), Q3S,
      row_labels=(L(5, 'Meander'), L(5, 'Confluence'), L(5, 'Tributary'), L(5, 'Delta'))),
    T('p1-3-ii', P1, '3', '(ii)', 2, 5, L(5, 'Rivers'),
      (L(5, '(ii) ' + TF), L(5, 'The part of the river profile labelled F above is called the upper course.')),
      (S(7, '(ii) · False', 'Q.4 (i)'),),
      (fixed('True or false', 2, '(ii) · False'),), '0-9', RIVERS, ID + 'p1-q3-ii', False, ('page',), Q3S),
    T('p1-4-i', P1, '4', '(i)', 8, 6, L(6, 'Surface Processes'),
      (L(6, '(i) Match each of the photographs A, B, C and D with the landform', 'that best matches it.'),),
      (S(7, 'Q.4 (i) · B', '(ii) · Erosion'),),
      rows(['Q.4 (i) · B', 'A · 2m', 'C · 2m', 'D · 2m']), '0-4', GLAC + SEA + RW, ID + 'p1-q4', True,
      ('page',), Q4S,
      row_labels=(L(6, 'Scree slope'), L(6, 'U-shaped valley', nth=0), L(6, 'Terracette'), L(6, 'Sand spit'))),
    T('p1-4-ii', P1, '4', '(ii)', 2, 6, L(6, 'Surface Processes'),
      (L(6, '(ii) Which of the following processes are most associated', 'Tick (✓) the correct box.'),
       L(6, 'Erosion'), L(6, 'Deposition')),
      (S(7, '(ii) · Erosion', 'Q.5'),),
      (fixed('Process', 2, '(ii) · Erosion · 2m'),), '0-11', GLAC, ID + 'p1-q4-ii', False, ('page',), Q4S),
    T('p1-5', P1, '5', '', 10, 7, L(7, 'Regions'),
      (L(7, 'Match the type of region with the example of the region', 'in the table below.'),),
      (S(7, 'Q.5 · C', 'Q.6 (i)'),),
      rows(['Q.5 · C', 'B · 2m', 'A · 2m', 'E · 2m', 'D · 2m · Total 10m']),
      '1-0', EURO + IRL, ID + 'p1-q5', True, ('page',),
      row_labels=(L(7, 'Sambre Meuse Valley'), L(7, 'London'), L(7, 'The Islamic World'),
                  L(7, 'Cool Temperate Oceanic'), L(7, 'Meath County Council'))),
    T('p1-6-i', P1, '6', '(i)', 5, 7, L(7, 'Map Skills'),
      (L(7, '(i) The town of Bantry is located in which area', 'Tick (✓) the correct box.'),
       L(7, 'South west'), L(7, 'South east')),
      (S(7, 'Q.6 (i)', '(ii) · 4.8 km'),),
      (fixed('Area of the map', 5, 'Q.6 (i) · South west · 5m'),), '2-6', MAP, ID + 'p1-q6', False,
      ('map', 'legend'), Q6S),
    T('p1-6-ii', P1, '6', '(ii)', 5, 7, L(7, 'Map Skills'),
      (L(7, '(ii) What is the length of the R584 road', 'Tick (✓) the correct box.'),
       L(7, '4.8 km'), L(7, '5.6 km')),
      (S(7, '(ii) · 4.8 km'),),
      (fixed('Length', 5, '(ii) · 4.8 km · 5m'),), '2-6', MAP, ID + 'p1-q6-ii', False, ('map', 'legend'), Q6S),
    T('p1-7-i', P1, '7', '(i)', 6, 8, L(8, 'Ordnance Survey Map'),
      (L(8, '(i) Name the feature shown at each of the following grid references:'),),
      (S(8, 'Q.7 (i)', '(ii) · 272'),),
      rows(['Q.7 (i) · 18hole golf', 'Parking · 2m', 'Standing stone · 2m']), '2-6', MAP, ID + 'p1-q7', False,
      ('map', 'legend'), Q7S,
      row_labels=(L(8, 'V 999 509:'), L(8, 'W 026 477:'), L(8, 'W 098 473:'))),
    T('p1-7-ii', P1, '7', '(ii)', 2, 8, L(8, 'Ordnance Survey Map'),
      (L(8, '(ii) What is the height, in metres, of the spot height at W 074 557?'),),
      (S(8, '(ii) · 272', '(iii) · Correctly drawn'),),
      (fixed('Spot height', 2, '(ii) · 272(m) · 2m'),), '2-6', MAP, ID + 'p1-q7-ii', False, ('map', 'legend'), Q7S),
    T('p1-7-iii', P1, '7', '(iii)', 2, 8, L(8, 'Ordnance Survey Map'),
      (L(8, '(iii) Draw the Ordnance Survey map symbol for boating activities in the space below.'),),
      (S(8, '(iii) · Correctly drawn symbol', 'Q.8 (i)'),),
      (fixed('Symbol', 2, '(iii) · Correctly drawn symbol · 2m'),), '2-6', MAP, ID + 'p1-q7-iii', False,
      ('map', 'legend'), Q7S),
]

for index, (roman, statement, start, nxt, answer) in enumerate([
        ('(i)', 'There is a harbour in the right foreground.', 'Q.8 (i) True', '(ii) · False', 'Q.8 (i) True · 2m'),
        ('(ii)', 'There is a housing estate in the left foreground.', '(ii) · False', '(iii) · True', '(ii) · False · 2m'),
        ('(iii)', 'There is agricultural land in the right middleground.', '(iii) · True', '(iv) · True',
         '(iii) · True · 2m'),
        ('(iv)', 'There is a car park in the centre middleground.', '(iv) · True', '(v) · False', '(iv) · True · 2m'),
        ('(v)', 'This aerial photograph is a vertical aerial photograph.', '(v) · False', 'Q.9 (i)',
         '(v) · False · 2m')]):
    PART_ONE.append(T(
        f'p1-8-{roman.strip("()")}', P1, '8', roman, 2, 8, L(8, 'Aerial Photograph'),
        (L(8, f'{roman} {statement}'),), (S(8, start, nxt),),
        (fixed('True or false', 2, answer),), '2-8', AER,
        ID + 'p1-q8' + ('' if index == 0 else f'-{roman.strip("()")}'), False, ('aerial',), Q8S))

PART_ONE += [
    T('p1-9-i', P1, '9', '(i)', 8, 9, L(9, 'Economic Activities'),
      (L(9, '(i) Examine the photographs above and indicate whether each', 'table below.'),),
      (S(8, 'Q.9 (i) · A Tertiary', '(ii) · Valid tertiary'),),
      (fixed('Photograph A', 2, 'Q.9 (i) · A Tertiary · 2m'), fixed('Photograph B', 2, 'B Primary · 2m'),
       fixed('Photograph C', 2, 'C Secondary · 2m'), fixed('Photograph D', 2, 'D Tertiary · 2m')),
      '3-0', ECON, ID + 'p1-q9', True, ('page',)),
    T('p1-9-ii', P1, '9', '(ii)', 2, 9, L(9, 'Economic Activities'),
      (L(9, '(ii) Name one tertiary economic activity NOT shown in the photographs above.'),),
      (S(8, '(ii) · Valid tertiary activity', 'Q.10'),),
      (fixed('Tertiary activity', 2, '(ii) · Valid tertiary activity · 2m'),), '3-0', ECON, ID + 'p1-q9-ii', False,
      ('page',)),
    T('p1-10', P1, '10', '', 10, 10, L(10, 'Weather Charts'),
      (L(10, 'Match each of the labels A to E', 'in the table below.'),),
      (S(8, 'Q.10 · A', 'Q.11 (i)'),),
      rows(['Q.10 · A', 'D · 2m', 'B · 2m', 'E · 2m', 'C · 2m · Total 10m']), '2-7', WEATHER, ID + 'p1-q10', True,
      ('page',), (L(10, 'Examine the weather chart above and answer the question that follows.'),),
      row_labels=(L(10, 'Occluded front'), L(10, 'Area of high pressure'), L(10, 'Area of low pressure'),
                  L(10, 'Warm front'), L(10, 'Isobar'))),
]

for index, (roman, prompt, start, nxt, answer, label, topic, atlas) in enumerate([
        ('(i)', '(i) What was the area of forested land (thousand hectares) in Spain?', 'Q.11 (i) 18,572',
         '(ii) · Germany', 'Q.11 (i) 18,572(thousand hectares) · 2m', 'Area', '2-0', GRAPH),
        ('(ii)', '(ii) Which country had 32% of its land covered by forestry?', '(ii) · Germany', '(iii) · Sweden',
         '(ii) · Germany · 2m', 'Country', '2-0', GRAPH),
        ('(iii)', '(iii) Which country had the largest area of forested land?', '(iii) · Sweden', '(iv) · Ireland',
         '(iii) · Sweden · 2m', 'Country', '2-0', GRAPH),
        ('(iv)', '(iv) Which country had the smallest percentage of its land covered by forestry?', '(iv) · Ireland',
         '(v) · Valid benefit', '(iv) · Ireland · 2m', 'Country', '2-0', GRAPH),
        ('(v)', '(v) Suggest one benefit to a country of having more of its land covered by forestry.',
         '(v) · Valid benefit', 'Q.12 (i)', '(v) · Valid benefit · 2m', 'One benefit', '3-4', ENV)]):
    PART_ONE.append(T(
        f'p1-11-{roman.strip("()")}', P1, '11', roman, 2, 11, L(11, 'Statistical Interpretation'),
        (L(11, prompt),), (S(8, start, nxt),), (fixed(label, 2, answer),), topic, atlas,
        ID + 'p1-q11' + ('' if index == 0 else f'-{roman.strip("()")}'), index == 0, ('page',), Q11S))

for index, (prompt, start, nxt, answer, label, topic, atlas) in enumerate([
        (L(12, '(i) Of the owner-occupied homes', 'without a loan or mortgage?'), 'Q.12 (i) Without a loan',
         '(ii) · 134', 'Q.12 (i) Without a loan or mortgage · 2m', 'Answer', '2-0', GRAPH),
        (L(12, '(ii) What was the average weekly rent (in €) paid in Donegal?'), '(ii) · 134', '(iii) · 119,300',
         '(ii) · 134 (€) · 2m', 'Rent', '2-0', GRAPH),
        (L(12, '(iii) How many homes in Ireland had solar panels?'), '(iii) · 119,300',
         '(iv) · Meath County Council', '(iii) · 119,300 · 2m', 'Homes', '2-0', GRAPH),
        (L(12, '(iv) Which county council had the highest number of homes with solar panels?'),
         '(iv) · Meath County Council', '(v) · Valid example', '(iv) · Meath County Council · 2m', 'County council',
         '2-0', GRAPH),
        (L(12, '(v) State one example of renewable energy, other than solar.'), '(v) · Valid example', None,
         '(v) · Valid example · 2m', 'One example', '3-5', ECON)]):
    roman = ('i', 'ii', 'iii', 'iv', 'v')[index]
    PART_ONE.append(T(
        f'p1-12-{roman}', P1, '12', f'({roman})', 2, 12, L(12, 'Graphical Interpretation'),
        (prompt,), (S(8, start, nxt),), (fixed(label, 2, answer),), topic, atlas,
        ID + 'p1-q12' + ('' if index == 0 else f'-{roman}'), index == 0, ('page',), Q12S))


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


def graph(paper_line):
    return (fixed('Graph paper', 3, paper_line, (0, 3)),
            fixed('Vertical axis labelled / circle', 3, 'Vertical axis labelled/Circle · 3m graded (3/1/0)', (0, 1, 3)),
            fixed('Horizontal axis labelled / centred', 3, 'Horizontal axis labelled/Centred · 3m graded (3/1/0)',
                  (0, 1, 3)),
            fixed('5 items illustrated', 15, '5 items @ 3m each graded (3/1/0) · 15m', sums(*[(0, 1, 3)] * 5)))


SURFACE = ('River processes', 'Coastal processes', 'Mass movement processes.')
PART_TWO = [
    sketch(3, L(3, 'Ordnance Survey Map'),
           L(3, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper.',
             'from W 031 556 to the coastline.'),
           10, ID + 'p2-q1a', '2-6', MAP, ('map', 'legend'),
           ('The coastline', 'Chapel Island', 'An area of coniferous plantation in the north west of the map',
            'The highest point on the Ordnance Survey map',
            'The course of the Owvane River from W 031 556 to the coastline')),
]
PART_TWO += romans('1B', 3, L(3, 'Volcanoes'), (), ID + 'p2-q1b', (), [
    ('(i)', 4, L(3, '(i) Name two examples of volcanoes.'),
     S(11, 'Two valid volcanoes named', '(ii) · Discuss'),
     (fixed('Two volcanoes', 4, 'Two valid volcanoes named @ 2m each · 4m', (0, 2, 4)),), '0-7', EV),
    ('(ii)', 18, L(3, '(ii) Discuss the positive effects of volcanoes.'),
     # The scheme prints 1B's diagram directions once, after (iii); they govern (ii) too.
     (S(11, 'Discussion · 6SRP', '(iii) · Discuss', after='(ii) · Discuss the positive'),
      S(11, 'Allow one SRP for relevant annotated diagram.', 'Total 40m', after='(iii) · Discuss the negative')),
     (srp3('Discussion', 6, f'Discussion · 6{SRPS} @ 3m each · 18m'),), '0-7', EV),
    ('(iii)', 18, L(3, '(iii) Discuss the negative effects of volcanoes.'),
     S(11, 'Discussion · 6SRP', 'Total 40m', after='(iii) · Discuss the negative'),
     (srp3('Discussion', 6, f'Discussion · 6{SRPS} @ 3m each · 18m'),), '0-7', EV),
])
PART_TWO.append(T(
    'p2-1c', P2, '1C', '', 30, 3, L(3, 'Human Interaction with Surface Processes'),
    (L(3, 'Examine how humans interact with one of the following surface processes:', 'Mass movement processes.'),),
    (S(11, 'Interaction identified · 3m', 'Total 30m'),),
    (fixed('Interaction identified', 3, 'Interaction identified · 3m'),
     srp3('Explanation', 9, f'Explanation 9 {SRPS} @ 3m each · 27m')),
    '0-6', RIVERS, ID + 'p2-q1c-river-processes', True,
    routes=bullet_routes('p2-q1c-', SURFACE, atlas=dict(zip(SURFACE, (RIVERS, SEA, RW))))))

Q2AS = (L(4, 'Examine the map of the world above showing plate boundaries', 'following questions.'),)
PART_TWO += romans('2A', 4, L(4, 'Plate Tectonics'), Q2AS, ID + 'p2-q2a', ('page',), [
    ('(i)', 3, L(4, '(i) Are the plates colliding or separating at A?'),
     S(12, 'Colliding · 3m', '(ii) · Name the two'), (fixed('Colliding or separating', 3, 'Colliding · 3m'),),
     '0-0', PS),
    ('(ii)', 6, L(4, '(ii) Name the two plates that are found either side', 'labelled A.'),
     S(12, 'Indian plate and Eurasian plate', '(iii) What type'),
     (fixed('Two plates', 6, 'Indian plate and Eurasian plate · 3m+3m', (0, 3, 6)),), '0-0', PS),
    ('(iii)', 3, L(4, '(iii) What type of plate boundary can be seen at B?'),
     S(12, 'Sliding/transverse', '(iv) · Name the most'),
     (fixed('Plate boundary', 3, 'Sliding/transverse/passive etc. · 3m'),), '0-0', PS),
    ('(iv)', 3, L(4, '(iv) Name the most southerly plate labelled on the map.'),
     S(12, 'Antarctic plate · 3m', '(v) · Name the ocean'), (fixed('Plate', 3, 'Antarctic plate · 3m'),), '0-0', PS),
    ('(v)', 3, L(4, '(v) Name the ocean ridge that runs along the plate boundary at C.'),
     S(12, 'Mid Atlantic ridge', '(vi) Explain'), (fixed('Ocean ridge', 3, 'Mid Atlantic ridge · 3m'),), '0-0', PS),
    ('(vi)', 6, L(4, '(vi) Explain briefly how this ocean ridge was formed.'),
     S(12, 'Brief explanation two SRP', '(vii) Explain', after='(vi) Explain briefly how'),
     (srp3('Brief explanation', 2, f'Brief explanation two {SRPS} @ 3m each · 6m'),), '0-0', PS),
    ('(vii)', 6, L(4, '(vii) Explain briefly the process of subduction.'),
     S(12, 'Brief explanation two SRP', 'Total 30m', after='(vii) Explain briefly the process'),
     (srp3('Brief explanation', 2, f'Brief explanation two {SRPS} @ 3m each · 6m'),), '0-0', PS),
])
ROCK = ('Quarrying', 'Mining', 'Oil/Gas exploitation', 'Geothermal energy production.')
PART_TWO += [
    T('p2-2b', P2, '2B', '', 40, 4, L(4, 'Surface Processes'),
      (L(4, '(i) Explain, with the aid of diagrams, the formation of any two landforms.'),),
      (S(13, 'Formation of any two landforms @ 20m each.', 'Or'),),
      two_of('Landform', 20, 'Formation of any two landforms @ 20m each.', 'For each landform:',
             ('Landform named · 1m', 'Diagram(s) two aspects @ 2m each · 4m',
              f'Formation explained 5 {SRPS} @ 3m each · 15m'),
             ((0, 1), (0, 2, 4), steps(15, 3))),
      '0-4', PS_SURFACE, ID + 'p2-q2b-route-i', True,
      routes=(
          Route('route-i', 'Route (i)', ID + 'p2-q2b-route-i', True),
          Route('route-ii', 'Route (ii)', ID + 'p2-q2b-route-ii', True,
                prompt=(L(4, '(ii) Describe and explain any two processes of mass movement.'),),
                scheme=(S(13, 'Any two processes @ 20m each', 'Total 40m'),),
                criteria=two_of('Process', 20, 'Any two processes @ 20m each', 'For each process:',
                                ('Process stated · 2m', f'Description / Explanation 6 {SRPS} @ 3m each · 18m'),
                                ((0, 2), steps(18, 3))),
                topic='0-8', atlas=RW),
      )),
    T('p2-2c', P2, '2C', '', 30, 5, L(5, 'Human Interaction with the Rock Cycle'),
      (L(5, 'Describe and explain how humans interact with the rock cycle with reference to',
         'Geothermal energy production.'),),
      (S(14, 'Description / explanation 10 SRP', 'Total 30m'),),
      (srp3('Description/explanation', 10, f'Description / explanation 10 {SRPS} @ 3m each.'),),
      '0-6', RW, ID + 'p2-q2c-quarrying', True, routes=bullet_routes('p2-q2c-', ROCK)),
]

Q3AS = (L(6, 'Examine the photographs above and answer each of the following questions.'),)
PART_TWO += romans('3A', 6, L(6, 'Surface Processes'), Q3AS, ID + 'p2-q3a', ('page',), [
    ('(i)', 9, L(6, '(i) In your answer book, match each of the letters A, B and C', 'Rift valley.'),
     S(15, '• C Mountain range', '(ii) · In your answer book'),
     rows(['• C Mountain range · 3m', '• A Volcanic island · 3m', '• B Rift valley. · 3m'], 3), '0-0', PS + EV + RW),
    ('(ii)', 9, L(6, '(ii) In your answer book, match each of the letters A, B and C', 'Faulting.'),
     S(15, '• A Lava cooling', '(iii) Name one process'),
     rows(['• A Lava cooling · 3m', '• C Folding · 3m', '• B Faulting. · 3m'], 3), '0-2', RW + EV),
    ('(iii)', 3, L(6, '(iii) Name one process of physical/mechanical weathering.'),
     S(15, 'Valid process named · 3m', '(iv) Name one mountain'),
     (fixed('Weathering process', 3, 'Valid process named · 3m'),), '0-8', RW),
    ('(iv)', 3, L(6, '(iv) Name one mountain range that you have studied.'),
     S(15, 'Valid mountain range named', '(v) Explain'),
     (fixed('Mountain range', 3, 'Valid mountain range named · 3m'),), '0-2', RW),
    ('(v)', 6, L(6, '(v) Explain briefly the process of folding.'),
     S(15, 'Brief explanation · 2 SRP', 'Total 30m'),
     (srp3('Brief explanation', 2, f'Brief explanation · 2 {SRPS} @ 3m each · 6m'),), '0-2', RW),
])
# 3A row labels follow the printed list order of each roman.
PART_TWO[-5] = Task(**{**PART_TWO[-5].__dict__,
                       'row_labels': (L(6, 'Mountain range'), L(6, 'Volcanic island'), L(6, 'Rift valley'))})
PART_TWO[-4] = Task(**{**PART_TWO[-4].__dict__,
                       'row_labels': (L(6, 'Lava cooling'), L(6, 'Folding'), L(6, 'Faulting'))})


def karst_feature():
    return (fixed('Feature named', 2, 'Feature named · 2m'),
            fixed('Diagram: two aspects', 4, 'Diagram · Two aspects @ 2m each · 4m', (0, 2, 4)),
            srp3('Explanation', 4, f'Explanation · 4 {SRPS} @ 3m each · 12m'))


PART_TWO += romans('3B', 6, L(6, 'Karst Landscapes'), (), ID + 'p2-q3b', (), [
    ('(i)', 4, L(6, '(i) Name one example of a karst landscape.'),
     S(16, 'One example named · 4m', '(ii) · Explain, with the aid'),
     (fixed('Karst landscape named', 4, 'One example named · 4m'),), '0-3', KARST),
    ('(ii)', 18, L(6, '(ii) Explain, with the aid of a diagram, how one surface feature', 'formed.'),
     S(16, 'Feature named · 2m', '(iii) Explain, with the aid', after='(ii) · Explain, with the aid'),
     karst_feature(), '0-3', KARST),
    ('(iii)', 18, L(6, '(iii) Explain, with the aid of a diagram, how one underground feature', 'was formed.'),
     S(16, 'Feature named · 2m', 'Total 40m', after='(iii) Explain, with the aid'),
     karst_feature(), '0-3', KARST),
])
PART_TWO += romans('3C', 6, L(6, 'Rocks'), (), ID + 'p2-q3c', (), [
    ('(i)', 6, L(6, '(i) Name one example of an igneous rock and state one location where it can be found.'),
     S(16, 'Igneous rock named', '(ii) Describe and explain'),
     (fixed('Igneous rock named', 3, 'Igneous rock named · 3m'),
      fixed('Location stated', 3, 'Valid location stated · 3m')), '0-1', RW),
    ('(ii)', 24, L(6, '(ii) Describe and explain how igneous rocks are formed.'),
     S(16, 'Description/Explanation 8 SRP', 'Total 30m'),
     (srp3('Description/explanation', 8, f'Description/Explanation 8 {SRPS} @ 3m each · 24m'),), '0-1', RW),
])

SHOWN = 'Shown · 4m graded (4/2/0)'
NAMED_SHOWN = sums((0, 2), (0, 2, 4))
PART_TWO.append(T(
    'p2-4a', P2, '4A', '', 30, 7, L(7, 'Irish Region'),
    (L(7, 'Draw a sketch map of Ireland.', 'in this region.'),),
    (S(17, 'Outline of Ireland', 'Total 30m'),),
    (fixed('Outline of Ireland', 6, 'Outline of Ireland · 6m graded (6/4/2/0)', (0, 2, 4, 6)),
     Criterion('Region', 6, NAMED_SHOWN, 'exact', ('Region: · Named · 2m', f'={SHOWN}@0')),
     Criterion('River', 6, NAMED_SHOWN, 'exact', ('River: · Named · 2m', f'={SHOWN}@1')),
     Criterion('Town/City', 6, NAMED_SHOWN, 'exact', ('Town/City: · Named · 2m', f'={SHOWN}@2')),
     Criterion('Relief (upland/lowland)', 6, NAMED_SHOWN, 'exact',
               ('Relief (upland/lowland): · Named · 2m', f'={SHOWN}@3'))),
    '1-4', IRL, ID + 'p2-q4a', True))
ACTIVITIES = ('The reasons why tourists are attracted to the region',
              'The importance of manufacturing to the region',
              'The development of transport in the region.')
PART_TWO.append(T(
    'p2-4b', P2, '4B', '', 40, 7, L(7, 'Economic Activities – Continental / Sub-Continental Region'),
    (L(7, 'Explain the development of any two of the following with reference to a',
       'The development of transport in the region.'),),
    (S(18, 'Region named · 1m', '4C.'),),
    (fixed('Region named', 1, 'Region named · 1m'),
     srp3('Activity 1 explained', 7, f'Activity 1 explained 7 {SRPS} @ 3m each · 21m'),
     srp3('Activity 2 explained', 6, f'Activity 2 explained 6 {SRPS} @ 3m each · 18m')),
    '1-6', CONT, *pool(ID + 'p2-q4b-', ACTIVITIES, 2)[:1], True, absorbs=pool(ID + 'p2-q4b-', ACTIVITIES, 2)[1]))
PART_TWO += romans('4C', 7, L(7, 'European Union Expansion'), (), ID + 'p2-q4c', (), [
    ('(i)', 6, L(7, '(i) Name two countries that have joined the European Union since Ireland joined in 1973.'),
     S(18, 'Two countries named @ 3m', '(ii) Explain the advantages'),
     (fixed('Two countries', 6, 'Two countries named @ 3m each · 6m', (0, 3, 6)),), '1-5', EURO + EU),
    ('(ii)', 24, L(7, '(ii) Explain the advantages and disadvantages of European Union expansion for Ireland.'),
     S(18, 'Explanation 8 SRP', 'Total 30m'),
     (srp3('Explanation', 8, f'Explanation 8 {SRPS} @ 3m each · 24m'),), '1-5', EURO + EU),
])

Q5AS = (L(8, 'Examine the infographic above which shows information about visitors', 'following questions.'),)
PART_TWO += romans('5A', 8, L(8, 'Tourism in Ireland'), Q5AS, ID + 'p2-q5a', ('page',), [
    ('(i)', 3, L(8, '(i) How many foreign resident overnight visitors', 'June 2023?'),
     S(19, '619,900 · 3m', '(ii) · What was'), (fixed('Visitors', 3, '619,900 · 3m'),), '2-0', GRAPH),
    ('(ii)', 3, L(8, '(ii) What was the reason 42.6% of visitors came for?'),
     S(19, 'Holiday or leisure', '(iii) How long'), (fixed('Reason', 3, 'Holiday or leisure · 3m'),), '2-0', GRAPH),
    ('(iii)', 3, L(8, '(iii) How long did a typical visit last?'),
     S(19, '7.3 nights · 3m', '(iv) How much'), (fixed('Length of visit', 3, '7.3 nights · 3m'),), '2-0', GRAPH),
    ('(iv)', 3, L(8, '(iv) How much (in €) did a typical visit cost?'),
     S(19, '1,357', '(v) · Calculate'), (fixed('Cost', 3, '1,357 (€) · 3m'),), '2-0', GRAPH),
    ('(v)', 6, L(8, '(v) Calculate the total percentage of visitors', 'States combined.'),
     S(19, '60.7', '(vi) Name two'), (fixed('Total percentage', 6, '60.7 (%) · 6m'),), '2-0', GRAPH),
    ('(vi)', 6, L(8, '(vi) Name two tourist attractions in Ireland.'),
     S(19, 'Two valid tourist attractions', '(vii) Explain'),
     (fixed('Two tourist attractions', 6, 'Two valid tourist attractions named · 3m+3m', (0, 3, 6)),), '1-4', IRL),
    ('(vii)', 6, L(8, '(vii) Explain briefly one advantage of tourism to the Irish economy.'),
     S(19, 'Brief explanation two SRP', 'Total 30m'),
     (srp3('Brief explanation', 2, f'Brief explanation two {SRPS} @ 3m each · 6m'),), '1-4', IRL),
])
Q5BS = (L(9, 'Answer each of the following questions with reference to a European region', 'that you have studied.'),)
Q5BI = L(9, '(i) Name one example of a secondary economic activity in this region.')
PART_TWO += romans('5B', 9, L(9, 'Secondary Economic Activity in a European Region'), Q5BS, ID + 'p2-q5b', (), [
    ('(i)', 4, Q5BI, S(20, 'One valid secondary economic activity named', '(ii) · Explain the advantages'),
     (fixed('Secondary economic activity named', 4, 'One valid secondary economic activity named · 4m'),),
     '1-5', EURO),
    ('(ii)', 27, L(9, '(ii) Explain the advantages that this region has for the development of this secondary',
                   'economic activity.'),
     S(20, 'Explanation 9 SRP', '(iii) Describe one challenge'),
     (srp3('Explanation', 9, f'Explanation 9 {SRPS} @ 3m each · 27m'),), '1-5', EURO, (Q5BI,)),
    ('(iii)', 9, L(9, '(iii) Describe one challenge faced by this secondary economic activity in this region.'),
     S(20, 'Description 3 SRP', 'Total 40m'),
     (srp3('Description', 3, f'Description 3 {SRPS} @ 3m each · 9m'),), '1-5', EURO, (Q5BI,)),
])
PART_TWO.append(T(
    'p2-5c', P2, '5C', '', 30, 9, L(9, 'Urban Regions'),
    (L(9, 'Describe and explain the reasons for the growth of any one urban area in Ireland', 'have studied.'),),
    (S(20, 'Description/explanation 10 SRP', 'Total 30m'),),
    (srp3('Description/explanation', 10, f'Description/explanation 10 {SRPS} @ 3m each'),),
    '1-3', IRL, ID + 'p2-q5c', True))

Q6AS = (L(10, 'Examine the table above showing the percentage of people unemployed', 'following questions.'),)
PART_TWO += romans('6A', 10, L(10, 'European Unemployment'), Q6AS, ID + 'p2-q6a', ('page',), [
    ('(i)', 3, L(10, '(i) Which country had the highest percentage of people unemployed in 2010?'),
     S(21, 'Spain · 3m', '(ii) · What was the percentage'), (fixed('Country', 3, 'Spain · 3m'),), '2-0', GRAPH),
    ('(ii)', 3, L(10, '(ii) What was the percentage of people unemployed in Poland in 2022?'),
     S(21, '2.8 (%) · 3m', '(iii) · Which two'), (fixed('Percentage', 3, '2.8 (%) · 3m'),), '2-0', GRAPH),
    ('(iii)', 6, L(10, '(iii) Which two countries experienced an increase', 'from 2010 to 2016?'),
     S(21, 'Greece and Italy', '(iv) · Calculate'),
     (fixed('Two countries', 6, 'Greece and Italy · 3m+3m', (0, 3, 6)),), '2-0', GRAPH),
    ('(iv)', 6, L(10, '(iv) Calculate the reduction in the percentage of people unemployed in Ireland',
                  '2010 and 2022.'),
     S(21, '9.6 (%)', '(v) · Explain briefly'), (fixed('Reduction', 6, '9.6 (%) · 6m'),), '2-0', GRAPH),
    ('(v)', 6, L(10, '(v) Explain briefly one disadvantage of a high level of unemployment.'),
     S(21, 'Brief explanation two SRP', '(vi) · Explain briefly', after='(v) · Explain briefly'),
     (srp3('Brief explanation', 2, f'Brief explanation two {SRPS} @ 3m each · 6m'),), '1-5', EURO),
    ('(vi)', 6, L(10, '(vi) Explain briefly one way to reduce unemployment levels.'),
     S(21, 'Brief explanation two SRP', 'Total 30m', after='(vi) · Explain briefly'),
     (srp3('Brief explanation', 2, f'Brief explanation two {SRPS} @ 3m each · 6m'),), '1-5', EURO),
])
Q6BS = (L(10, 'Answer each of the following questions with reference to an Irish region', 'studied.'),)
Q6BI = L(10, '(i) Name one primary economic activity that contributes to the economy of this region.')
PART_TWO += romans('6B', 10, L(10, 'Primary Economic Activity in an Irish Region'), Q6BS, ID + 'p2-q6b', (), [
    ('(i)', 4, Q6BI, S(22, 'One valid primary economic activity named', '(ii) · Explain the advantages'),
     (fixed('Primary economic activity named', 4, 'One valid primary economic activity named · 4m'),), '1-4', IRL),
    ('(ii)', 27, L(10, '(ii) Explain the advantages that this region has for the development of the primary',
                   'named in part (i) above.'),
     S(22, 'Explanation 9 SRP', '(iii) Describe one problem'),
     (srp3('Explanation', 9, f'Explanation 9 {SRPS} @ 3m each · 27m'),), '1-4', IRL, (Q6BI,)),
    ('(iii)', 9, L(10, '(iii) Describe one problem faced by this primary economic activity in this region.'),
     S(22, 'Description 3 SRP', 'Total 40m'),
     (srp3('Description', 3, f'Description 3 {SRPS} @ 3m each · 9m'),), '1-4', IRL, (Q6BI,)),
])
REGION_TYPES = ('Climatic regions', 'Geomorphological regions', 'Cultural regions defined by language',
                'Cultural regions defined by religion.')
PART_TWO.append(T(
    'p2-6c', P2, '6C', '', 30, 10, L(10, 'Concept of a region'),
    (L(10, 'Describe and explain, using examples, any two of the region types listed below:',
       'Cultural regions defined by religion.'),),
    (S(22, 'Region type 1', 'Total 30m'),),
    (srp3('Region type 1', 5, ('Region type 1', f'=Description/Explanation 5 {SRPS} @ 3m each · 15m@0')),
     srp3('Region type 2', 5, ('Region type 2', f'=Description/Explanation 5 {SRPS} @ 3m each · 15m@1'))),
    # The shipped id names the whole question; the other combinations it
    # absorbs were never shipped (this review had briefly split them).
    '1-0', IRL + EURO + CONT, ID + 'p2-q6c', True, absorbs=pool(ID + 'p2-q6c-', REGION_TYPES, 2)[1]))

PART_TWO.append(sketch(
    12, L(12, 'Aerial Photograph'),
    L(12, 'Examine the aerial photograph of Bantry accompanying this paper.', 'in the right middleground.'),
    24, ID + 'p2-q7a', '2-8', AER, ('aerial',),
    ('The coastline', 'A church', 'An industrial area in the centre foreground', 'A car park',
     'An agricultural area in the right middleground')))
Q7BI = L(12, '(i) Name one multinational company that you have studied', 'located in Ireland.')
PART_TWO += romans('7B', 12, L(12, 'Multinational Company (MNC)'), (), ID + 'p2-q7b', (), [
    ('(i)', 4, Q7BI, S(25, 'Valid MNC named', '(ii) · Name one raw'),
     (fixed('MNC named', 2, 'Valid MNC named · 2m'), fixed('Location stated', 2, 'Valid location stated · 2m')),
     '3-2', MNC),
    ('(ii)', 6, L(12, '(ii) Name one raw material required by this multinational company', 'by this multinational company.'),
     S(25, 'Valid raw material named', '(iii) Explain the advantages'),
     (fixed('Raw material named', 3, 'Valid raw material named · 3m'),
      fixed('Product named', 3, 'Valid product named · 3m')), '3-2', MNC, (Q7BI,)),
    ('(iii)', 21, L(12, '(iii) Explain the advantages of being located in Ireland for this multinational company.'),
     S(25, 'Explanation 7 SRP', '(iv) Explain one difficulty'),
     (srp3('Explanation', 7, f'Explanation 7 {SRPS} @ 3m each · 21m'),), '3-2', MNC, (Q7BI,)),
    ('(iv)', 9, L(12, '(iv) Explain one difficulty facing this multinational company in the future.'),
     S(25, 'Explanation 3 SRP', 'Total 40m'),
     (srp3('Explanation', 3, f'Explanation 3 {SRPS} @ 3m each · 9m'),), '3-2', MNC, (Q7BI,)),
])
PART_TWO += romans('7C', 12, L(12, 'Ireland and the European Union'), (), ID + 'p2-q7c', (), [
    ('(i)', 3, L(12, '(i) Name any one European Union policy which affects Ireland’s economy.'),
     S(25, 'Valid European Union policy', '(ii) · Describe and explain'),
     (fixed('Policy named', 3, 'Valid European Union policy · 3m'),), '3-3', EU),
    ('(ii)', 27, L(12, '(ii) Describe and explain the effects of European Union policy(ies) on Ireland’s economy.'),
     S(25, 'Description / Explanation 9 SRP', 'Total 30m'),
     (srp3('Description/explanation', 9, f'Description / Explanation 9 {SRPS} @ 3m each · 27m'),), '3-3', EU),
])

Q8AS = (L(13, 'Examine the pie chart above showing the destination of goods', 'following questions.'),)
PART_TWO += romans('8A', 13, L(13, 'Irish Trade'), Q8AS, ID + 'p2-q8a', ('page',), [
    ('(i)', 3, L(13, '(i) Which country did Ireland export 7% of goods to?'),
     S(26, 'China · 3m', '(ii) · What percentage'), (fixed('Country', 3, 'China · 3m'),), '2-0', GRAPH),
    ('(ii)', 3, L(13, '(ii) What percentage of goods went to the United Kingdom?'),
     S(26, '11 (%) · 3m', '(iii) Calculate'), (fixed('Percentage', 3, '11 (%) · 3m'),), '2-0', GRAPH),
    ('(iii)', 6, L(13, '(iii) Calculate X, the percentage of goods that went to', 'export destinations.'),
     S(26, '31 (%)', '(iv) Which country'), (fixed('Calculation', 6, '31 (%) · 6m'),), '2-0', GRAPH),
    ('(iv)', 3, L(13, '(iv) Which country received the largest amount of goods from Ireland in 2021?'),
     S(26, 'United States · 3m', '(v) · Name two'), (fixed('Country', 3, 'United States · 3m'),), '2-0', GRAPH),
    ('(v)', 6, L(13, '(v) Name two goods exported from Ireland.'),
     S(26, 'Two valid goods named', '(vi) State one'),
     (fixed('Two goods', 6, 'Two valid goods named · 3m+3m', (0, 3, 6)),), '3-0', ECON),
    ('(vi)', 3, L(13, '(vi) State one advantage of exports for the Irish economy.'),
     S(26, 'One valid advantage stated', '(vii) Explain'),
     (fixed('One advantage', 3, 'One valid advantage stated · 3m'),), '3-0', ECON),
    ('(vii)', 6, L(13, '(vii) Explain briefly one reason why the amount of goods exported to the UK', 'since 2020.'),
     S(26, 'Brief explanation two SRP', 'Total 30m'),
     (srp3('Brief explanation', 2, f'Brief explanation two {SRPS} @ 3m each · 6m'),), '3-3', EU),
])
Q8BI = L(13, '(i) Name one example of environmental pollution caused by economic activity.')
PART_TWO += romans('8B', 13, L(13, 'Economic Activity – Environmental Pollution'), (), ID + 'p2-q8b', (), [
    ('(i)', 4, Q8BI, S(27, 'Valid example named · 4m', '(ii) · Explain the causes'),
     (fixed('Example named', 4, 'Valid example named · 4m'),), '3-4', ENV),
    ('(ii)', 24, L(13, '(ii) Explain the causes and effects of this environmental pollution.'),
     S(27, 'Cause identified one SRP', '(iii) · Describe how'),
     (fixed('Cause identified', 3, 'Cause identified one SRP @ 3m each · 3m'),
      fixed('Effect identified', 3, 'Effect identified one SRP @ 3m each · 3m'),
      srp3('Explanation', 6, f'Explanation 6 {SRPS} @ 3m each · 18m')), '3-4', ENV, (Q8BI,)),
    ('(iii)', 12, L(13, '(iii) Describe how this environmental pollution could be reduced.'),
     S(27, 'Description 4 SRP', 'Total 40m'),
     (srp3('Description', 4, f'Description 4 {SRPS} @ 3m each · 12m'),), '3-4', ENV, (Q8BI,)),
])
PART_TWO.append(T(
    'p2-8c', P2, '8C', '', 30, 13, L(13, 'Economic Development – Developed Economy'),
    (L(13, 'Describe and explain the development of one of the following with reference to a developed',
       'Service and footloose industries.'),),
    (S(27, 'Named developed economy', 'Total 30m'),),
    (fixed('Named developed economy', 3, 'Named developed economy · 3m'),
     srp3('Description/explanation', 9, f'Description/explanation 9 {SRPS} @ 3m each · 27m')),
    '3-0', ECON, ID + 'p2-q8c-tourism', True,
    routes=bullet_routes('p2-q8c-', ('Tourism', 'Financial services', 'Service and footloose industries.'))))

Q9AS = (L(14, 'Examine the data above on GDP growth', 'following questions.'),)
PART_TWO += romans('9A', 14, L(14, 'Economic Development'), Q9AS, ID + 'p2-q9a', ('page',), [
    ('(i)', 24, L(14, '(i) Using graph paper, draw a suitable graph to illustrate this data.'),
     S(28, 'Graph paper 3m', '(ii) · In your answer book'), graph('Graph paper 3m'), '2-0', GRAPH),
    ('(ii)', 6, L(14, '(ii) In your answer book, explain briefly one benefit to a country of economic growth.'),
     S(28, 'Brief explanation 2 SRP', 'Total 30m'),
     (srp3('Brief explanation', 2, f'Brief explanation 2 {SRPS} @ 3m each · 6m'),), '3-0', ECON),
])
Q9BS = (L(14, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper. It is', 'V 998 506.'),)
PART_TWO += romans('9B', 14, L(14, 'Ordnance Survey Map'), Q9BS, ID + 'p2-q9b', ('map', 'legend'), [
    ('(i)', 15, L(14, '(i) Describe and explain the advantages of this location.'),
     S(29, 'Description/Explanation 5 SRP', '(ii) · Describe and explain the disadvantages',
       after='(i) · Describe and explain the advantages'),
     (srp3('Description/explanation', 5, f'Description/Explanation 5 {SRPS} @ 3m each · 15m'),), '3-0', ECON + MAP),
    ('(ii)', 15, L(14, '(ii) Describe and explain the disadvantages of this location.'),
     S(29, 'Description/Explanation 5 SRP', '(iii) Using a six-figure',
       after='(ii) · Describe and explain the disadvantages'),
     (srp3('Description/explanation', 5, f'Description/Explanation 5 {SRPS} @ 3m each · 15m'),), '3-0', ECON + MAP),
    ('(iii)', 10, L(14, '(iii) Using a six-figure grid reference, suggest an alternative location', 'alternative location.'),
     S(29, 'Valid accepted notation', 'Total 40m'),
     (fixed('Location (accepted notation)', 4, 'Valid accepted notation for location · 4m'),
      srp3('Brief explanation', 2, f'Brief explanation 2 {SRPS} @ 3m each · 6m')), '2-6', MAP + ECON),
], legacy_first=False)
Q9CI = L(14, '(i) Name one example of how the development of economic activities', 'conflict arising between people.')
PART_TWO += romans('9C', 14, L(14, 'Economic Activity and Conflict'), (), ID + 'p2-q9c', (), [
    ('(i)', 3, Q9CI, S(29, 'Valid example named · 3m', '(ii) · Describe and explain this'),
     (fixed('Example named', 3, 'Valid example named · 3m'),), '3-4', ENV),
    ('(ii)', 27, L(14, '(ii) Describe and explain this conflict.'),
     S(29, 'Description and explanation 9 SRP', 'Total 30m'),
     (srp3('Description and explanation', 9, f'Description and explanation 9 {SRPS} @ 3m each · 27m'),),
     '3-4', ENV, (Q9CI,)),
])

PART_TWO.append(sketch(
    15, L(15, 'Ordnance Survey Map'),
    L(15, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper.', 'The R584 regional road.'),
    30, ID + 'p2-q10a', '2-6', MAP + URB, ('map', 'legend'),
    ('The coastline', 'An area of clustered settlement', 'An area of linear settlement', 'A golf course',
     'The R584 regional road')))
Q10BI = L(15, '(i) State two reasons why people migrate from rural areas to urban areas.')
PART_TWO += romans('10B', 15, L(15, 'Migration – Rural to Urban'), (), ID + 'p2-q10b', (), [
    ('(i)', 4, Q10BI, S(31, 'Valid reasons stated', '(ii) · Describe and explain the effect'),
     (fixed('Two reasons', 4, 'Valid reasons stated · 2m + 2m', (0, 2, 4)),), '4-2', POP),
    ('(ii)', 18, L(15, '(ii) Describe and explain the effect of this migration on the urban areas', 'migrate to.'),
     S(31, 'Description/explanation 6 SRP', '(iii) Describe and explain the effect',
       after='(ii) · Describe and explain the effect'),
     (srp3('Description/explanation', 6, f'Description/explanation 6 {SRPS} @ 3m each · 18m'),), '4-2', POP, (Q10BI,)),
    ('(iii)', 18, L(15, '(iii) Describe and explain the effect of this migration on the rural areas they leave behind.'),
     S(31, 'Description/explanation 6 SRP', 'Total 40m', after='(iii) Describe and explain the effect'),
     (srp3('Description/explanation', 6, f'Description/explanation 6 {SRPS} @ 3m each · 18m'),), '4-2', POP, (Q10BI,)),
])
PART_TWO.append(T(
    'p2-10c', P2, '10C', '', 30, 15, L(15, 'Population'),
    (L(15, '‘Birth rates and death rates are influenced', 'medical technology.’'),
     L(15, 'Describe and explain the factors that influence birth rates and death rates.')),
    (S(31, 'Description/explanation 10 SRP', 'Total 30m'),),
    (srp3('Description/explanation', 10, f'Description/explanation 10 {SRPS} @ 3m each · 30m'),),
    '4-0', POP, ID + 'p2-q10c', True))

Q11AS = (L(16, 'Examine the data above on percentage of population aged over 65', 'following questions.'),)
PART_TWO += romans('11A', 16, L(16, 'Population', nth=0), Q11AS, ID + 'p2-q11a', ('page',), [
    ('(i)', 24, L(16, '(i) Using graph paper, draw a suitable graph to illustrate this data.'),
     S(32, 'Graph paper · 3m', '(ii) · In your answer book'), graph('Graph paper · 3m'), '2-0', GRAPH),
    ('(ii)', 6, L(16, '(ii) In your answer book, explain briefly one impact of a high percentage', 'aged over 65.'),
     S(32, 'Brief explanation 2 SRP', 'Total 30m'),
     (srp3('Brief explanation', 2, f'Brief explanation 2 {SRPS} @ 3m each · 6m'),), '4-1', POP),
])
Q11BI = L(16, '(i) Name one city in the developing world that is rapidly growing.')
PART_TWO += romans('11B', 16, L(16, 'Developing World City'), (), ID + 'p2-q11b', (), [
    ('(i)', 4, Q11BI, S(33, 'Valid developing world city named', '(ii) · Explain the reasons'),
     (fixed('Developing world city named', 4, 'Valid developing world city named · 4m'),), '4-5', URB),
    ('(ii)', 18, L(16, '(ii) Explain the reasons for the rapid growth of this developing world city.'),
     S(33, 'Explanation 6 SRP', '(iii) Describe the problems'),
     (srp3('Explanation', 6, f'Explanation 6 {SRPS} @ 3m each · 18m'),), '4-5', URB, (Q11BI,)),
    ('(iii)', 9, L(16, '(iii) Describe the problems caused by this rapid growth.'),
     S(33, 'Description 3 SRP', '(iv) Explain one solution'),
     (srp3('Description', 3, f'Description 3 {SRPS} @ 3m each · 9m'),), '4-5', URB, (Q11BI,)),
    ('(iv)', 9, L(16, '(iv) Explain one solution to these problems.'),
     S(33, 'Explanation 3 SRP', '11C.', after='(iv) Explain one solution'),
     (srp3('Explanation', 3, f'Explanation 3 {SRPS} @ 3m each · 9m'),), '4-5', URB, (Q11BI,)),
])
REASON = ('Three reasons @ 10m each · 30m', 'For each reason:', 'Aerial photograph evidence · 1m',
          f'Explanation 3 {SRPS} @ 3m each · 9m')
PART_TWO.append(T(
    'p2-11c', P2, '11C', '', 30, 16, L(16, 'Development of Urban Settlements'),
    (L(16, 'Examine the aerial photograph accompanying this paper.'),
     L(16, 'Explain three reasons why the town of Bantry developed', 'to support each reason.')),
    (S(33, 'Three reasons @ 10m each', 'Total 30m'),),
    tuple(Criterion(f'Reason {n}', 10, sums((0, 1), steps(9, 3)), 'srp', REASON) for n in (1, 2, 3)),
    '4-3', URB + AER, ID + 'p2-q11c', False, ('aerial',)))

Q12AS = (L(17, 'Examine the table above about Ireland’s largest towns', 'following questions.'),)
PART_TWO += romans('12A', 17, L(17, 'Urban Growth'), Q12AS, ID + 'p2-q12a', ('page',), [
    ('(i)', 3, L(17, '(i) What was Ireland’s largest town in 2022?'),
     S(34, 'Drogheda · 3m', '(ii) · What was'), (fixed('Town', 3, 'Drogheda · 3m'),), '2-0', GRAPH),
    ('(ii)', 3, L(17, '(ii) What was the population of Swords in 2016?'),
     S(34, '39,248 · 3m', '(iii) Which town'), (fixed('Population', 3, '39,248 · 3m'),), '2-0', GRAPH),
    ('(iii)', 6, L(17, '(iii) Which town had a population of less than 30,000 in 2011?'),
     S(34, 'Navan · 6m', '(iv) Calculate'), (fixed('Town', 6, 'Navan · 6m'),), '2-0', GRAPH),
    ('(iv)', 6, L(17, '(iv) Calculate the growth in Dundalk’s population from 2011 to 2022.'),
     S(34, '5,296', '(v) · Explain briefly'), (fixed('Growth', 6, '5,296 · 6m'),), '2-0', GRAPH),
    ('(v)', 6, L(17, '(v) Explain briefly one possible reason for the growth in population', 'table above.'),
     S(34, 'Brief explanation 2 SRP', '(vi) Explain briefly', after='(v) · Explain briefly'),
     (srp3('Brief explanation', 2, f'Brief explanation 2 {SRPS} @ 3m each · 6m'),), '4-3', URB),
    ('(vi)', 6, L(17, '(vi) Explain briefly one impact of the growth in population of these towns.'),
     S(34, 'Brief explanation 2 SRP', 'Total 30m', after='(vi) Explain briefly'),
     (srp3('Brief explanation', 2, f'Brief explanation 2 {SRPS} @ 3m each · 6m'),), '4-5', URB),
])
Q12BI = L(17, '(i) Name one urban area that you have studied.')
PART_TWO += romans('12B', 17, L(17, 'Urban Functions'), (), ID + 'p2-q12b', (), [
    ('(i)', 3, Q12BI, S(35, 'Valid urban area named', '(ii) · Name any two'),
     (fixed('Urban area named', 3, 'Valid urban area named · 3m'),), '4-3', URB),
    ('(ii)', 6, L(17, '(ii) Name any two functions of this urban area.'),
     S(35, 'Valid functions named', '(iii) · Describe'),
     (fixed('Two functions', 6, 'Valid functions named · 3m + 3m', (0, 3, 6)),), '4-3', URB, (Q12BI,)),
    ('(iii)', 21, L(17, '(iii) Describe and explain how the functions of this urban area have changed over time.'),
     S(35, 'Description/explanation 7 SRP', 'Total 30m'),
     (srp3('Description/explanation', 7, f'Description/explanation 7 {SRPS} @ 3m each · 21m'),), '4-3', URB, (Q12BI,)),
])
Q12CS = (L(17, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper and',
           'following questions.'),)
Q12CI = L(17, '(i) Give a grid reference for an area on the map where there is an absence of settlement.')
Q12CIII = L(17, '(iii) Give a grid reference for an area on the map which has a relatively high density of',
            'settlement.')
PART_TWO += romans('12C', 17, L(17, 'Settlement Distribution'), Q12CS, ID + 'p2-q12c', ('map', 'legend'), [
    ('(i)', 2, Q12CI, S(35, 'Grid reference · 2m', '(ii) · Explain in detail', after='(i) · Give a grid reference'),
     (fixed('Grid reference', 2, 'Grid reference · 2m'),), '2-6', MAP),
    ('(ii)', 18, L(17, '(ii) Explain in detail, using evidence from the map, why there is an absence', 'at this location.'),
     S(35, 'Explanation 6 SRP', '(iii) Give a grid reference', after='(ii) · Explain in detail'),
     (srp3('Explanation', 6, f'Explanation 6 {SRPS} @ 3m each · 18m'),), '4-3', URB + MAP, (Q12CI,)),
    ('(iii)', 2, Q12CIII, S(35, 'Grid reference · 2m', '(iv) Explain in detail', after='(iii) Give a grid reference'),
     (fixed('Grid reference', 2, 'Grid reference · 2m'),), '2-6', MAP),
    ('(iv)', 18, L(17, '(iv) Explain in detail, using evidence from the map, why there is a relatively high density',
                   'at this location.'),
     S(35, 'Explanation 6 SRP', 'Total 40m', after='(iv) Explain in detail'),
     (srp3('Explanation', 6, f'Explanation 6 {SRPS} @ 3m each · 18m'),), '4-3', URB + MAP, (Q12CIII,)),
], legacy_first=False)

TASKS = [*PART_ONE, *PART_TWO]

# Every 2024 Ordinary card id shipped before this review (49). Each must survive.
LEGACY_IDS = [
    'geography-2024-ol-p1-q1',
    'geography-2024-ol-p1-q2',
    'geography-2024-ol-p1-q3',
    'geography-2024-ol-p1-q4',
    'geography-2024-ol-p1-q5',
    'geography-2024-ol-p1-q9',
    'geography-2024-ol-p1-q10',
    'geography-2024-ol-p1-q11',
    'geography-2024-ol-p1-q12',
    'geography-2024-ol-p2-q1b',
    'geography-2024-ol-p2-q1c-river-processes',
    'geography-2024-ol-p2-q1c-coastal-processes',
    'geography-2024-ol-p2-q1c-mass-movement-processes',
    'geography-2024-ol-p2-q2a',
    'geography-2024-ol-p2-q2b-route-i',
    'geography-2024-ol-p2-q2b-route-ii',
    'geography-2024-ol-p2-q2c-quarrying',
    'geography-2024-ol-p2-q2c-mining',
    'geography-2024-ol-p2-q2c-oil-gas-exploitation',
    'geography-2024-ol-p2-q2c-geothermal-energy-production',
    'geography-2024-ol-p2-q3a',
    'geography-2024-ol-p2-q3b',
    'geography-2024-ol-p2-q3c',
    'geography-2024-ol-p2-q4a',
    'geography-2024-ol-p2-q4b-the-reasons-why-tourists-are-attra-the-importance-of-manufacturing-to',
    'geography-2024-ol-p2-q4b-the-reasons-why-tourists-are-attra-the-development-of-transport-in-th',
    'geography-2024-ol-p2-q4b-the-importance-of-manufacturing-to-the-development-of-transport-in-th',
    'geography-2024-ol-p2-q4c',
    'geography-2024-ol-p2-q5a',
    'geography-2024-ol-p2-q5b',
    'geography-2024-ol-p2-q5c',
    'geography-2024-ol-p2-q6a',
    'geography-2024-ol-p2-q6b',
    'geography-2024-ol-p2-q6c',
    'geography-2024-ol-p2-q7b',
    'geography-2024-ol-p2-q7c',
    'geography-2024-ol-p2-q8a',
    'geography-2024-ol-p2-q8b',
    'geography-2024-ol-p2-q8c-tourism',
    'geography-2024-ol-p2-q8c-financial-services',
    'geography-2024-ol-p2-q8c-service-and-footloose-industries',
    'geography-2024-ol-p2-q9a',
    'geography-2024-ol-p2-q9c',
    'geography-2024-ol-p2-q10b',
    'geography-2024-ol-p2-q10c',
    'geography-2024-ol-p2-q11a',
    'geography-2024-ol-p2-q11b',
    'geography-2024-ol-p2-q12a',
    'geography-2024-ol-p2-q12b',
]

ID_CORRECTION_REASON = (
    'The shipped card held every part of a question the scheme prices part by '
    'part. Its id is kept on the first separately priced part (or the first '
    'printed route); the other parts are new cards with their own published '
    'allocation.')
