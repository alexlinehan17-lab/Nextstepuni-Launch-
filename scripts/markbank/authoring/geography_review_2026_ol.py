"""Independent review ledger: Leaving Certificate Geography 2026 Ordinary Level.

Sources (English editions, Paper Trail index, sizes and SHA-256 pinned in
EXPECTED_SOURCES): Part One and Answerbook LC005GLP042EV (40 pages), Part Two
LC005GLP043EV (20 pages), marking scheme LC005GLP000EV (34 pages), and the
common companions shared with Higher Level — 1:50 000 Dundalk map
LC005CLP003EV, its legend LC005CLPC00EV and the Dundalk aerial photograph
LC005CLP004EV.

Visual sweep (every page rendered and read on 2026-10-11):
  Part One booklet p1 cover (400 marks); p2 instructions (Part One "Attempt
  any TEN", 100 marks; Part Two "attempt THREE", 300 marks); p3-p12
  Questions 1-12 (p8 holds Q6 and Q7, p9 holds Q8 and Q9); p13 Part Two
  answerbook instructions; p14-p17 graph-paper answer pages; p18-p39 lined
  answer pages; p40 copyright/back cover.
  Part Two booklet p1 cover; p2 Part Two instructions; p3-p6 Section 1
  (Q1-Q3; p5 holds only 2C); p7-p10 Section 2 (Q4-Q6); p11 Section 3 divider;
  p12-p17 Electives (Q7-Q12); p18-p19 "Do not hand this up" blanks; p20
  copyright/back cover.
  Scheme p1 cover; p2 notes; p3-p4 Geographical Investigation (coursework,
  not a written-paper task) and its presentation breakdown; p5-p6 Part One
  table; p7 Part Two instructions; p8-p32 Q1-Q12 (A/B/C, each roman priced);
  p33 Irish-language bonus marks; p34 blank.

Boundaries follow the published allocation: at Ordinary Level the scheme
prices every printed roman of every A, B and C part (e.g. 1C (i) 3m + 3m,
(ii) 3m, (iii) 7 SRPs @ 3m), so each roman is its own task. Part One romans
and lettered true/false items are tasks; a matching or location table under
ONE printed instruction stays one task with a criterion per scheme row (the
scheme's rows follow the printed table rows; each was checked against the
image: Q1 Inner core=D, Mantle=B, Crust=A, Outer core=C; Q4 Vent=D,
Crater=C, Ash Cloud=A, Magma chamber=B; Q5 Madeira=B, Baton Rouge=C, Port
Douglas=A, Sahara=D; Q9 Islamic World=B, Donegal County Council=D, Paris=E,
Sambre Meuse=A, Mediterranean=C; Q10 Isobar=B, high=C, warm front=A, low=D).
A part whose wording depends on an earlier part ("named in part (i) above",
"this multinational company") carries that earlier printed part in its stem.

Tariffs: an SRP is 3 marks at Ordinary Level; "a + b" lines are one criterion
with partial credit a; graded lines keep their printed grades; sketch items
are "showing 3 (3/1/0) + labelled 2"; 4A items are "named 2 + shown 4
(4/2/0)". Every question totals 10 (Part One) or 100 = 30 + 40 + 30 (Part
Two) as printed.

Wording: the paper wins where the scheme reprints it differently (1B
"labelled diagrams", 2B "with the aid of a diagram", 2A "Sea stack",
7B "Services and footloose industries.").
"""

from geography_review import (
    Criterion, Lift, Route, SchemeSlice, Task, pool, fixed, srp, steps, sums,
)

YEAR = 2026
LEVEL = 'ordinary'
PAPER_PAGES = {1: 40, 2: 20}
SCHEME_PAGES = 34
QUESTION_TARIFFS = {1: {str(n): 10 for n in range(1, 13)},
                    2: {f'{n}{x}': (40 if x == 'B' else 30)
                        for n in range(1, 13) for x in 'ABC'}}

EXPECTED_SOURCES = {
    'paper1': ('LC005GLP042EV.pdf', 6521540),
    'paper2': ('LC005GLP043EV.pdf', 4047293),
    'scheme': ('LC005GLP000EV.pdf', 2028337),
}

PAGE_REVIEW = {
    'paper1': {1: 'cover', 2: 'instructions', **{p: 'question' for p in range(3, 13)},
               13: 'answerbook instructions', **{p: 'graph-paper answer page' for p in range(14, 18)},
               **{p: 'lined answer page' for p in range(18, 40)}, 40: 'copyright/back cover'},
    'paper2': {1: 'cover', 2: 'Part Two instructions',
               **{p: 'question' for p in (3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17)},
               11: 'section divider', 18: 'blank (do not hand up)', 19: 'blank (do not hand up)',
               20: 'copyright/back cover'},
    'scheme': {1: 'cover', 2: 'notes', 3: 'geographical investigation (coursework)',
               4: 'investigation presentation breakdown', 5: 'Part One table', 6: 'Part One table',
               7: 'Part Two instructions', **{p: 'Part Two allocation' for p in range(8, 20)},
               20: 'section divider', **{p: 'Part Two allocation' for p in range(21, 33)},
               33: 'Irish-language bonus marks', 34: 'blank'},
}

EXPECTED_SELECTION_SCAN = [
    [1, 2, 'attempt any ten'], [1, 2, 'attempt three'], [1, 3, 'attempt any ten'],
    [1, 4, 'any two'],
    [2, 2, 'attempt three'],
    [2, 3, 'answer (i) or (ii)'], [2, 3, 'any two'], [2, 3, 'any two'],
    [2, 5, 'one of the following'],
    [2, 6, 'one of the following'],
    [2, 7, 'any one'],
    [2, 8, 'any two'],
    [2, 10, 'any one'],
    [2, 12, 'one of the following'], [2, 12, 'any one'],
]
SELECTION_REVIEW = [
    {'scan': [[1, 2, 'attempt any ten'], [1, 2, 'attempt three'], [1, 3, 'attempt any ten'],
              [2, 2, 'attempt three']],
     'kind': 'exam-attempt-rule',
     'reason': 'Part One any ten of twelve and Part Two three questions from two sections are attempt rules; every question is carded.'},
    {'scan': [[2, 3, 'answer (i) or (ii)']], 'kind': 'closed-route',
     'reason': '1B: (i) or (ii) -> two routes, each with its own scheme allocation.'},
    {'scan': [[2, 5, 'one of the following']], 'kind': 'closed-choose-one',
     'reason': '2C: one of four printed bullets -> four routes.'},
    {'scan': [[2, 6, 'one of the following']], 'kind': 'closed-choose-one',
     'reason': '3C: one of three printed surface processes -> three routes.'},
    {'scan': [[2, 8, 'any two']], 'kind': 'choose-n-one-card',
     'reason': '5B: any two of three printed activities -> one card with every printed item (choice is not a route; the scheme marks each chosen item alike).'},
    {'scan': [[2, 12, 'one of the following']], 'kind': 'closed-choose-one',
     'reason': '7B: one of three printed activities -> three routes.'},
    {'scan': [[1, 4, 'any two'], [2, 3, 'any two'], [2, 3, 'any two'], [2, 7, 'any one'],
              [2, 10, 'any one'], [2, 12, 'any one']],
     'kind': 'open-response',
     'reason': 'No printed pool: Part One Q2(iii) any two metamorphic rocks; 1B(i) any two landforms and 1B(ii) any two mass movement processes (the student chooses; the scheme prices two @ 20m); 4C any one region (the factor box is illustrative, not a choice); 6C any one urban area; 7C(i) any one EU policy.'},
]

P1, P2 = 1, 2
ID = 'geography-2026-ol-'
O = 'geography-ordinary-'
SRP3 = 3


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


TF = 'Indicate whether the following statement is true or false by ticking (✓) the correct box.'

# ---------------------------------------------------------------- Part One --
Q1S = (L(3, 'Examine the diagram above showing the different layers', 'following questions.'),)
Q2S = (L(4, 'Examine the photograph above and answer each of the following questions.'),)
Q2TF = L(4, '(ii) Indicate whether each of the following statements are true or false', 'correct box.')
Q3S = (L(5, 'Examine the photograph of a coastline above', 'following questions.'),)
Q4S = (L(6, 'Examine the diagram of a volcano above', 'following questions.'),)
Q5S = (L(7, 'Examine the satellite images above', 'following questions.'),)
Q6S = (L(8, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper, and answer each of the following questions.'),)
Q7S = (L(8, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper and answer the following questions.'),)
Q8S = (L(9, 'Examine the aerial photograph of Dundalk accompanying this paper.'),
       L(9, 'Indicate whether the following statements are true or false by ticking (✓) the correct box.'))
Q11S = (L(11, 'Examine the information above from Tourism Ireland 2023', 'following questions.'),)
Q12S = (L(12, 'Examine the table above which shows average monthly temperatures', 'following questions.'),)

PS = (O + 'plate-tectonics',)
RW = (O + 'rocks-weathering-mass-movement',)
SEA = (O + 'the-sea',)
EV = (O + 'earthquakes-volcanoes',)
MAP = (O + 'mapwork',)
AER = (O + 'aerial-photos',)
GRAPH = (O + 'graph-style-questions',)
WEATHER = (O + 'weather-climate',)

PART_ONE = [
    T('p1-1-i', P1, '1', '(i)', 8, 3, L(3, 'Layers of the Earth'),
      (L(3, '(i) Match each of the letters A, B, C and D', 'in the table below.'),),
      (S(5, 'Q.1 (i) · D', '(ii) · True · 2m · Total 10m'),),
      rows(['Q.1 (i) · D', 'B · 2m', 'A · 2m', 'C · 2m']), '0-0', PS, ID + 'p1-q1', True,
      ('page',), Q1S, row_labels=(L(3, 'Inner core'), L(3, 'Mantle', nth=0), L(3, 'Crust'), L(3, 'Outer core'))),
    T('p1-1-ii', P1, '1', '(ii)', 2, 3, L(3, 'Layers of the Earth'),
      (L(3, '(ii) ' + TF), L(3, 'Circular movements of semi-molten rock', 'convection currents.')),
      (S(5, '(ii) · True · 2m · Total 10m', 'Q.2 (i)', after='Q.1 (i)'),),
      (fixed('True or false', 2, '(ii) · True'),), '0-0', PS, ID + 'p1-q1-ii', False, ('page',), Q1S),
    T('p1-2-i', P1, '2', '(i)', 2, 4, L(4, 'Rocks'),
      (L(4, '(i) Which of the following is the location shown', 'Tick (✓) the correct box.'),
       L(4, 'The Burren, Co. Clare'), L(4, 'The Giant’s Causeway, Co. Antrim')),
      (S(5, 'Q.2 (i)', '(ii) (a) · False'),),
      (fixed('Location', 2, 'Q.2 (i) · The Giants Causeway'),), '0-1', RW, ID + 'p1-q2', True, ('page',), Q2S),
    T('p1-2-ii-a', P1, '2', '(ii)(a)', 2, 4, L(4, 'Rocks'),
      (Q2TF, L(4, '(a) Granite is an example of a sedimentary rock.')),
      (S(5, '(ii) (a) · False', '(b) · True'),),
      (fixed('Statement (a)', 2, '(ii) (a) · False'),), '0-1', RW, ID + 'p1-q2-ii-a', False, ('page',), Q2S),
    T('p1-2-ii-b', P1, '2', '(ii)(b)', 2, 4, L(4, 'Rocks'),
      (Q2TF, L(4, '(b) Fossils can be found in sedimentary rocks.')),
      (S(5, '(b) · True', '(iii) · Valid answer'),),
      (fixed('Statement (b)', 2, '(b) · True'),), '0-1', RW, ID + 'p1-q2-ii-b', False, ('page',), Q2S),
    T('p1-2-iii', P1, '2', '(iii)', 4, 4, L(4, 'Rocks'),
      (L(4, '(iii) Name any two types of metamorphic rock.'),),
      (S(5, '(iii) · Valid answer · 2m + 2m', 'Q.3 (i)'),),
      (fixed('Two metamorphic rocks', 4, ('(iii) · Valid answer · 2m + 2m', '(e.g. Marble'), (0, 2, 4)),),
      '0-1', RW, ID + 'p1-q2-iii', False, ('page',), Q2S),
    T('p1-3-i', P1, '3', '(i)', 2, 5, L(5, 'Coasts'),
      (L(5, '(i) Which of the following coastal defences', 'Tick (✓) the correct box.'), L(5, 'Groynes'), L(5, 'Rock Armour')),
      (S(5, 'Q.3 (i) · Rock Armour', '(ii) · Erosion'),),
      (fixed('Coastal defence', 2, 'Q.3 (i) · Rock Armour'),), '0-6', SEA, ID + 'p1-q3', True, ('page',), Q3S),
    T('p1-3-ii', P1, '3', '(ii)', 8, 5, L(5, 'Coasts'),
      (L(5, '(ii) Indicate, by ticking (✓) the correct box', 'processes of deposition.'),),
      (S(5, '(ii) · Erosion', 'Q.4 (i)'),),
      rows(['(ii) · Erosion', '=Deposition · 2m@0', '=Deposition · 2m@1', 'Erosion · 2m · Total 10m']),
      '0-10', SEA, ID + 'p1-q3-ii', False, ('page',), Q3S,
      row_labels=(L(5, 'Cliff'), L(5, 'Beach'), L(5, 'Sand Bar'), L(5, 'Blowhole'))),
    T('p1-4-i', P1, '4', '(i)', 8, 6, L(6, 'Volcanoes'),
      (L(6, '(i) Match each of the letters A, B, C and D', 'in the table below.'),),
      (S(5, 'Q.4 (i) · D', '(ii) · Valid answer · 2m · Total 10m'),),
      rows(['Q.4 (i) · D', 'C · 2m', 'A · 2m', 'B · 2m']), '0-7', EV, ID + 'p1-q4', True, ('page',), Q4S,
      row_labels=(L(6, 'Vent'), L(6, 'Crater'), L(6, 'Ash Cloud'), L(6, 'Magma chamber'))),
    T('p1-4-ii', P1, '4', '(ii)', 2, 6, L(6, 'Volcanoes'),
      (L(6, '(ii) State one way of predicting a volcanic eruption.'),),
      (S(5, '(ii) · Valid answer · 2m · Total 10m', 'Q.5 (i)'),),
      (fixed('One way', 2, '(ii) · Valid answer · 2m'),), '0-7', EV, ID + 'p1-q4-ii', False, ('page',), Q4S),
    T('p1-5-i', P1, '5', '(i)', 8, 7, L(7, 'Satellite Interpretation'),
      (L(7, '(i) Match each satellite image A, B, C and D', 'in the table below.'),),
      (S(5, 'Q.5 (i) · B', '(ii) · True · 2m · Total 10m', after='Q.5 (i)'),),
      rows(['Q.5 (i) · B', 'C · 2m', 'A · 2m', 'D · 2m']), '2-8', AER, ID + 'p1-q5', True, ('page',), Q5S,
      row_labels=(L(7, 'Wildfires on the island of Maderia'), L(7, 'River meanders in Baton Rouge'),
                  L(7, 'Cyclone approaching Port Douglas'), L(7, 'Dust cloud over the Sahara Desert'))),
    T('p1-5-ii', P1, '5', '(ii)', 2, 7, L(7, 'Satellite Interpretation'),
      (L(7, '(ii) ' + TF), L(7, 'Met Éireann can use satellite images to forecast and track storms.')),
      (S(5, '(ii) · True · 2m · Total 10m', 'Q.6 (i)', after='Q.5 (i)'),),
      (fixed('True or false', 2, '(ii) · True'),), '2-8', AER + WEATHER, ID + 'p1-q5-ii', False, ('page',), Q5S),
    T('p1-6-i', P1, '6', '(i)', 5, 8, L(8, 'Map Skills'),
      (L(8, '(i) What is the approximate area of Dundalk Bay', 'Tick (✓) the correct box.'), L(8, '18 km²'), L(8, '28 km²')),
      (S(5, 'Q.6 (i)', '(ii) · 10.2 km'),),
      (fixed('Area', 5, 'Q.6 (i) · 18 km2 · 5m'),), '2-6', MAP, ID + 'p1-q6', True, ('map', 'legend'), Q6S),
    T('p1-6-ii', P1, '6', '(ii)', 5, 8, L(8, 'Map Skills'),
      (L(8, '(ii) What is the length of the M1 Motorway', 'Tick (✓) the correct box.'), L(8, '5.2 km'), L(8, '10.2 km')),
      (S(5, '(ii) · 10.2 km', 'Total 10m', after='Q.6 (i)'),),
      (fixed('Length', 5, '(ii) · 10.2 km · 5m'),), '2-6', MAP, ID + 'p1-q6-ii', False, ('map', 'legend'), Q6S),
    T('p1-7-i', P1, '7', '(i)', 6, 8, L(8, 'Ordnance Survey Map'),
      (L(8, '(i) Name the feature shown at each of the following grid references:'),),
      (S(6, 'Q.7 (i)', '(ii) · 274m'),),
      rows(['Q.7 (i) · Lighthouse in use', 'Tourist Information Centre · 2m', 'Parking · 2m']),
      '2-6', MAP, ID + 'p1-q7', True, ('map', 'legend'), Q7S,
      row_labels=(L(8, 'J 118 044:'), L(8, 'J 071 063:'), L(8, 'J 058 125:'))),
    T('p1-7-ii', P1, '7', '(ii)', 2, 8, L(8, 'Ordnance Survey Map'),
      (L(8, '(ii) What is the height, in metres, of the spot height at J 099 127?'),),
      (S(6, '(ii) · 274m', '(iii) · Correct symbol'),),
      (fixed('Spot height', 2, '(ii) · 274m'),), '2-6', MAP, ID + 'p1-q7-ii', False, ('map', 'legend'), Q7S),
    T('p1-7-iii', P1, '7', '(iii)', 2, 8, L(8, 'Ordnance Survey Map'),
      (L(8, '(iii) Draw the Ordnance Survey map symbol for a Wind Farm', 'space below.'),),
      (S(6, '(iii) · Correct symbol', 'Q.8 (i)'),),
      (fixed('Symbol', 2, '(iii) · Correct symbol'),), '2-6', MAP, ID + 'p1-q7-iii', False, ('map', 'legend'), Q7S),
]

for index, (roman, start, nxt, answer) in enumerate([
        ('(i)', 'Q.8 (i) · False', '(ii) · True', 'Q.8 (i) · False'),
        ('(ii)', '(ii) · True', '(iii) · True', '(ii) · True'),
        ('(iii)', '(iii) · True', '(iv) · True', '(iii) · True'),
        ('(iv)', '(iv) · True', '(v) · False', '(iv) · True'),
        ('(v)', '(v) · False', 'Q.9', '(v) · False')]):
    statements = ['There is a church in the left foreground.',
                  'There is an industrial area in the centre foreground.',
                  'This aerial photograph is an oblique photograph.',
                  'There is a residential area in the right foreground.',
                  'There is a bridge crossing the river in the right middleground.']
    PART_ONE.append(T(
        f'p1-8-{roman.strip("()")}', P1, '8', roman, 2, 9, L(9, 'Aerial Photograph'),
        (L(9, f'{roman} {statements[index]}'),), (S(6, start, nxt),),
        (fixed('True or false', 2, answer),), '2-8', AER,
        ID + 'p1-q8' + ('' if index == 0 else f'-{roman.strip("()")}'), index == 0, ('aerial',), Q8S))

PART_ONE += [
    T('p1-9', P1, '9', '', 10, 9, L(9, 'Regions'),
      (L(9, 'Match the type of region with the example of the region', 'in the table below.'),),
      (S(6, 'Q.9 · B', 'Q.10 (i)'),),
      rows(['Q.9 · B', 'D · 2m', 'E · 2m', 'A · 2m', 'C · 2m · Total 10m']),
      '1-0', (O + 'regions-european', O + 'regions-ireland'), ID + 'p1-q9', True, ('page',),
      row_labels=(L(9, 'The Islamic World'), L(9, 'Donegal County Council'), L(9, 'Paris, France'),
                  L(9, 'Sambre Meuse Valley, Belgium'), L(9, 'Mediterranean'))),
    T('p1-10-i', P1, '10', '(i)', 8, 10, L(10, 'Weather Chart', nth=0),
      (L(10, '(i) Match each of the letters A, B, C and D with the weather chart feature', 'in the table below.'),),
      (S(6, 'Q.10 (i) · B', '(ii) · Correct symbol'),),
      rows(['Q.10 (i) · B', 'C · 2m', 'A · 2m', 'D · 2m']), '2-7', WEATHER, ID + 'p1-q10', True, ('page',),
      (L(10, 'Examine the weather chart above and answer the questions that follow.'),),
      row_labels=(L(10, 'Isobar'), L(10, 'Area of high pressure'), L(10, 'Warm Front'), L(10, 'Area of low pressure'))),
    T('p1-10-ii', P1, '10', '(ii)', 2, 10, L(10, 'Weather Chart', nth=0),
      (L(10, '(ii) Draw the weather chart symbol for a cold front', 'box below.'),),
      (S(6, '(ii) · Correct symbol', 'Q.11 (i)'),),
      (fixed('Symbol', 2, '(ii) · Correct symbol'),), '2-7', WEATHER, ID + 'p1-q10-ii', False, ('page',),
      (L(10, 'Examine the weather chart above and answer the questions that follow.'),)),
]

for index, (roman, prompt, start, nxt, topic, atlas) in enumerate([
        ('(i)', '(i) In 2023, how many tourists visited Ireland?', 'Q.11 (i)', '(ii) · €786', '2-0', GRAPH),
        ('(ii)', '(ii) What was the average spend per trip made by tourists?', '(ii) · €786', '(iii) · 7.6', '2-0', GRAPH),
        ('(iii)', '(iii) What was the average length of stay (in nights) by tourists?', '(iii) · 7.6', '(iv) · UK', '2-0', GRAPH),
        ('(iv)', '(iv) Where did most ferry passengers come from in 2023?', '(iv) · UK', '(v) · Valid answer', '2-0', GRAPH),
        ('(v)', '(v) Name one tourist attraction in Ireland.', '(v) · Valid answer', 'Q.12 (i)', '1-4', (O + 'regions-ireland',))]):
    answer = start if index else 'Q.11 (i) · 8.1 million'
    PART_ONE.append(T(
        f'p1-11-{roman.strip("()")}', P1, '11', roman, 2, 11, L(11, 'Tourism', nth=0),
        (L(11, prompt),), (S(6, start, nxt),), (fixed('Answer', 2, answer),), topic, atlas,
        ID + 'p1-q11' + ('' if index == 0 else f'-{roman.strip("()")}'), index == 0, ('page',), Q11S))

for index, (roman, prompt, start, nxt) in enumerate([
        ('(i)', '(i) What was the average temperature (°C) for June?', 'Q.12 (i)', '(ii) · January'),
        ('(ii)', '(ii) Which month had the lowest average temperature (°C)?', '(ii) · January', '(iii) · March'),
        ('(iii)', '(iii) Which month experienced the highest total rainfall (mm)?', '(iii) · March', '(iv) · 254.7'),
        ('(iv)', '(iv) Calculate the total rainfall (mm) for April, May and June.', '(iv) · 254.7', '(v) · Four'),
        ('(v)', '(v) For how many months was the total rainfall more than 100mm?', '(v) · Four', None)]):
    PART_ONE.append(T(
        f'p1-12-{roman.strip("()")}', P1, '12', roman, 2, 12, L(12, 'Weather Statistics'),
        (L(12, prompt),), (S(6, start, nxt),), (fixed('Answer', 2, start),), '2-0', GRAPH + WEATHER,
        ID + 'p1-q12' + ('' if index == 0 else f'-{roman.strip("()")}'), index == 0, ('page',), Q12S))


# ---------------------------------------------------------------- Part Two --
def romans(q, page, title, stem, first_id, sources, parts):
    """Separately priced romans of one A/B/C part.
    parts: (sub, marks, prompt Lift, scheme slice, criteria, topic, atlas, extra stem Lifts)."""
    out = []
    for index, part in enumerate(parts):
        sub, marks, prompt, scheme, criteria, topic, atlas = part[:7]
        extra = part[7] if len(part) > 7 else ()
        roman = sub.strip('()')
        out.append(T(f'p2-{q.lower()}-{roman}', P2, q, sub, marks, page, title, (prompt,), (scheme,),
                     criteria, topic, atlas, first_id if index == 0 else f'{first_id}-{roman}',
                     index == 0, sources, (*stem, *extra)))
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
             topic, atlas, card_id, True, sources,
             row_labels=(None, None, None, *(L(page, b) for b in bullets)))


def two_of(label, count, head, each, lines, unit):
    per = sums(*unit)
    return tuple(Criterion(f'{label} {n}', count, per, 'srp', (head, each, *lines)) for n in (1, 2))


PS_SURFACE = (O + 'rivers', O + 'the-sea', O + 'glaciation')
PART_TWO = [
    sketch(3, L(3, 'Ordnance Survey Map'),
           L(3, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper.', 'The Flurry River.'),
           8, ID + 'p2-q1a', '2-6', MAP, ('map', 'legend'),
           ('The coastline', 'An area of land over 200m in height', 'An area of deciduous woodland',
            'The railway line', 'The Flurry River')),
    T('p2-1b', P2, '1B', '', 40, 3, L(3, 'Landform Development'),
      (L(3, '(i) Explain, with the aid of labelled diagrams', 'any two landforms.'),),
      (S(9, 'Formation of any two landforms @ 20m each.', 'Or'),),
      two_of('Landform', 20, 'Formation of any two landforms @ 20m each.', 'For each landform:',
             ('Landform named · 1m', 'Diagram(s) two aspects @ 2m each · 4m', 'Formation explained 5 SRPs @ 3m each · 15m'),
             ((0, 1), (0, 2, 4), steps(15, 3))),
      '0-4', PS_SURFACE, ID + 'p2-q1b-route-i', True,
      routes=(
          Route('route-i', 'Route (i)', ID + 'p2-q1b-route-i', True),
          Route('route-ii', 'Route (ii)', ID + 'p2-q1b-route-ii', True,
                prompt=(L(3, '(ii) Describe and explain any two processes of mass movement.'),),
                scheme=(S(9, 'Any two processes @ 20m each', 'Total 40m'),),
                criteria=two_of('Process', 20, 'Any two processes @ 20m each', 'For each process:',
                                ('Process stated · 2m', 'Description / Explanation 6 SRPs @ 3m each · 18m'),
                                ((0, 2), steps(18, 3))),
                topic='0-8', atlas=RW),
      )),
]
PART_TWO += romans('1C', 3, L(3, 'Earthquakes'), (), ID + 'p2-q1c', (), [
    ('(i)', 6, L(3, '(i) Name two geographical locations where earthquakes have occurred.'),
     S(9, 'Two valid locations named', '(ii) · Name one scale'),
     (fixed('Two locations', 6, 'Two valid locations named · 3m + 3m', (0, 3, 6)),), '0-7', EV),
    ('(ii)', 3, L(3, '(ii) Name one scale used to measure earthquakes.'),
     S(9, 'One valid scale named', '(iii) · Explain how'),
     (fixed('Scale', 3, 'One valid scale named · 3m'),), '0-7', EV),
    ('(iii)', 21, L(3, '(iii) Explain how earthquakes occur and describe their main effects.'),
     S(9, 'Explanation/description 7 SRPs', 'Total 30m'),
     (srp3('Explanation/description', 7, 'Explanation/description 7 SRPs @ 3m each · 21m'),), '0-7', EV),
])

Q2AS = (L(4, 'Examine the photographs above and answer each of the following questions.'),)
PART_TWO += romans('2A', 4, L(4, 'Surface Processes'), Q2AS, ID + 'p2-q2a', ('page',), [
    ('(i)', 9, L(4, '(i) In your answer book, match each of the photographs A, B and C with the landform', 'Drumlin.'),
     S(10, '• B · Waterfall', '(ii) · In your answer book'),
     rows(['• B · Waterfall', '• A · Sea Stack', '• C · Drumlin'], 3), '0-4', PS_SURFACE),
    ('(ii)', 9, L(4, '(ii) In your answer book, match each of the photographs A, B and C with the process', 'River erosion.'),
     S(10, '• A · Coastal Erosion', '(iii) · Explain'),
     rows(['• A · Coastal Erosion', '• C · Glacial Deposition', '• B · River Erosion'], 3), '0-4', PS_SURFACE),
    ('(iii)', 12, L(4, '(iii) Explain briefly the processes of:', 'Abrasion.'),
     S(10, '• Hydraulic action Brief explanation', 'Total 30m'),
     (srp3('Hydraulic action', 2, '• Hydraulic action Brief explanation two SRPs @ 3m each · 6m'),
      srp3('Abrasion', 2, '• Abrasion Brief explanation two SRPs @ 3m each · 6m')), '0-4', (O + 'rivers', O + 'the-sea')),
])
# 2A row labels follow the printed list order of each roman.
PART_TWO[-3] = Task(**{**PART_TWO[-3].__dict__, 'row_labels': (L(4, 'Waterfall'), L(4, 'Sea stack'), L(4, 'Drumlin'))})
PART_TWO[-2] = Task(**{**PART_TWO[-2].__dict__, 'row_labels': (L(4, 'Coastal erosion'), L(4, 'Glacial deposition'), L(4, 'River erosion'))})

KARST = (O + 'karst-regions',)


def karst_feature(after):
    return (fixed('Feature named', 2, 'Feature named · 2m'),
            fixed('Diagram(s): two aspects', 4, 'Diagram(s) two aspects @ 2m each · 4m', (0, 2, 4)),
            srp3('Formation explained', 4, 'Formation explained 4 SRPs @ 3m each · 12m'))


PART_TWO += romans('2B', 4, L(4, 'Karst Landscapes'), (), ID + 'p2-q2b', (), [
    ('(i)', 4, L(4, '(i) Name one example of a karst landscape.'),
     S(11, 'Karst landscape named', '(ii) · Explain, with the aid'),
     (fixed('Karst landscape named', 4, 'Karst landscape named · 4m'),), '0-3', KARST),
    ('(ii)', 18, L(4, '(ii) Explain, with the aid of a diagram, how one surface feature', 'was formed.'),
     S(11, 'Feature named · 2m', '(iii) · Explain, with the aid', after='(ii) · Explain, with the aid'),
     karst_feature('(ii)'), '0-3', KARST),
    ('(iii)', 18, L(4, '(iii) Explain, with the aid of a diagram, how one underground feature', 'was formed.'),
     S(11, 'Feature named · 2m', 'Total 40m', after='(iii) · Explain, with the aid'),
     karst_feature('(iii)'), '0-3', KARST),
])

ROCK = ('Quarrying', 'Mining', 'Oil/Gas exploitation', 'Geothermal energy production.')
ROCK_IDS = ('quarrying', 'mining', 'oil-gas-exploitation', 'geothermal-energy-production')
PART_TWO.append(T(
    'p2-2c', P2, '2C', '', 30, 5, L(5, 'Human Interaction with the Rock Cycle'),
    (L(5, 'Describe and explain how humans interact with the rock cycle', 'Geothermal energy production.'),),
    (S(11, 'Description/explanation 10 SRPs @ 3m each.', 'Total 30m'),),
    (srp3('Description/explanation', 10, 'Description/explanation 10 SRPs @ 3m each.'),),
    '0-6', RW, ID + 'p2-q2c-quarrying', True,
    routes=tuple(Route(slug, item.rstrip('.'), ID + 'p2-q2c-' + slug, True, keep_bullets=(item,))
                 for item, slug in zip(ROCK, ROCK_IDS))))

Q3AS = (L(6, 'Examine the news article above that describes a glacier melting', 'following questions.'),)
PART_TWO += romans('3A', 6, L(6, 'Mass Movement'), Q3AS, ID + 'p2-q3a', ('page',), [
    ('(i)', 6, L(6, '(i) In which country did the landslide take place?'),
     S(12, 'Switzerland · 6m', '(ii) · What was the cause'), (fixed('Country', 6, 'Switzerland · 6m'),), '0-8', RW),
    ('(ii)', 6, L(6, '(ii) What was the cause of the landslide?'),
     S(12, 'Extra water from melting glaciers', '(iii) · Name one way'),
     (fixed('Cause', 6, 'Extra water from melting glaciers · 6m'),), '0-8', RW),
    ('(iii)', 6, L(6, '(iii) Name one way the residents had prepared for the landslide.'),
     S(12, 'The village was evacuated', '(iv) · List two'),
     (fixed('Preparation', 6, 'The village was evacuated before the landslide · 6m'),), '0-8', RW),
    ('(iv)', 6, L(6, '(iv) List two effects of the landslide.'),
     S(12, 'Two effects listed', '(v) · Explain briefly'),
     (fixed('Two effects', 6, 'Two effects listed @ 3m each · 3m + 3m', (0, 3, 6)),), '0-8', RW),
    ('(v)', 6, L(6, '(v) Explain briefly why there is now a flood risk', 'in the article.'),
     S(12, 'Brief explanation · 3m + 3m', '[30m]'),
     (fixed('Explanation', 6, 'Brief explanation · 3m + 3m', (0, 3, 6), 'srp'),), '0-8', RW),
])
PART_TWO += romans('3B', 6, L(6, 'Rocks', nth=0), (), ID + 'p2-q3b', (), [
    ('(i)', 3, L(6, '(i) Name one example of an igneous rock.'),
     S(13, 'Igneous rock named', '(ii) · State one location'), (fixed('Igneous rock named', 3, 'Igneous rock named · 3m'),), '0-1', RW),
    ('(ii)', 3, L(6, '(ii) State one location where igneous rock can be found.'),
     S(13, 'Valid location stated', '(iii) · State two uses'), (fixed('Location', 3, 'Valid location stated · 3m'),), '0-1', RW),
    ('(iii)', 7, L(6, '(iii) State two uses of igneous rocks.'),
     S(13, 'Valid uses stated', '(iv) · Describe and explain'),
     (fixed('Two uses', 7, 'Valid uses stated · 4m + 3m', (0, 3, 4, 7)),), '0-1', RW),
    ('(iv)', 27, L(6, '(iv) Describe and explain how igneous rocks are formed.'),
     S(13, 'Description/Explanation 9 SRPs', 'Total 40m'),
     (srp3('Description/explanation', 9, 'Description/Explanation 9 SRPs @ 3m · 27m'),), '0-1', RW),
])

SURFACE = ('River processes', 'Coastal processes', 'Mass movement processes.')
SURFACE_IDS = ('river-processes', 'coastal-processes', 'mass-movement-processes')
PART_TWO.append(T(
    'p2-3c', P2, '3C', '', 30, 6, L(6, 'Human Interaction with Surface Processes'),
    (L(6, 'Examine how humans interact with one of the following surface processes:', 'Mass movement processes.'),),
    (S(13, 'Interaction identified · 3m', 'Total 30m'),),
    (fixed('Interaction identified', 3, 'Interaction identified · 3m'),
     srp3('Explanation', 9, 'Explanation 9 SRPs @ 3m each · 27m')),
    '0-6', (O + 'rivers',), ID + 'p2-q3c-river-processes', True,
    routes=tuple(Route(slug, item.rstrip('.'), ID + 'p2-q3c-' + slug, True, keep_bullets=(item,), atlas=(atlas,))
                 for item, slug, atlas in zip(SURFACE, SURFACE_IDS,
                                              (O + 'rivers', O + 'the-sea', O + 'rocks-weathering-mass-movement')))))

CONT = (O + 'regions-continental',)
EURO = (O + 'regions-european',)
IRL = (O + 'regions-ireland',)
SHOWN = 'Shown · 4m graded (4/2/0)'
NAMED_SHOWN = sums((0, 2), (0, 2, 4))
PART_TWO.append(T(
    'p2-4a', P2, '4A', '', 30, 7, L(7, 'Map Skills'),
    (L(7, 'Draw a sketch map of a Continental / Sub-Continental region', 'in this region.'),),
    (S(14, 'Outline of Region', 'Total 30m'),),
    (fixed('Outline of region', 6, 'Outline of Region · 6m graded (6/4/2/0)', (0, 2, 4, 6)),
     Criterion('River', 6, NAMED_SHOWN, 'exact', ('River: · Named · 2m', f'={SHOWN}@0')),
     Criterion('Town/City 1', 6, NAMED_SHOWN, 'exact', ('Town/City 1: · Named · 2m', f'={SHOWN}@1')),
     Criterion('Town/City 2', 6, NAMED_SHOWN, 'exact', ('Town/City 2: · Named · 2m', f'={SHOWN}@2')),
     Criterion('Relief (upland/lowland)', 6, NAMED_SHOWN, 'exact',
               ('Relief (upland/lowland): · Named · 2m', f'={SHOWN}@3'))),
    '1-6', CONT, ID + 'p2-q4a', True))

Q4BS = (L(7, 'Answer each of the following questions with reference to a European region', 'that you have studied.'),)
Q4BI = L(7, '(i) Name one example of a primary economic activity', 'economy of this region.')
PART_TWO += romans('4B', 7, L(7, 'Primary Economic Activity in a European Region'), Q4BS, ID + 'p2-q4b', (), [
    ('(i)', 4, Q4BI, S(15, 'One valid primary economic activity named', '(ii) · Explain the advantages'),
     (fixed('Primary economic activity named', 4, 'One valid primary economic activity named · 4m'),), '1-5', EURO),
    ('(ii)', 27, L(7, '(ii) Explain the advantages that this region has', 'named in part (i) above.'),
     S(15, 'Explanation 9 SRPs @ 3m each', '(iii) Describe one challenge'),
     (srp3('Explanation', 9, 'Explanation 9 SRPs @ 3m each · 27m'),), '1-5', EURO, (Q4BI,)),
    ('(iii)', 9, L(7, '(iii) Describe one challenge faced by this primary economic activity in this region.'),
     S(15, 'Description 3 SRPs @ 3m each', 'Total 40m'),
     (srp3('Description', 3, 'Description 3 SRPs @ 3m each · 9m'),), '1-5', EURO, (Q4BI,)),
])
PART_TWO.append(T(
    'p2-4c', P2, '4C', '', 30, 7, L(7, 'Regions and Culture'),
    (L(7, 'The culture of a region can often be determined by the following factors:'),
     L(7, 'Religion Language Sport/Games Music/Dance'),
     L(7, 'Describe and explain the importance of culture in any one region that you have studied.')),
    (S(15, 'Description/explanation 10 SRPs @ 3m each', 'Total 30m'),),
    (srp3('Description/explanation', 10, 'Description/explanation 10 SRPs @ 3m each'),),
    '1-3', (O + 'regions-ireland', O + 'regions-european', O + 'regions-continental'), ID + 'p2-q4c', True))

Q5AS = (L(8, 'Examine the chart above showing selected languages', 'following questions.'),)
PART_TWO += romans('5A', 8, L(8, 'Language in Ireland'), Q5AS, ID + 'p2-q5a', ('page',), [
    ('(i)', 6, L(8, '(i) Which of the three age groups shown spoke the most Irish?'),
     S(16, '15-34 · 6m', '(ii) · In the 35-54'), (fixed('Age group', 6, '15-34 · 6m'),), '2-0', GRAPH),
    ('(ii)', 6, L(8, '(ii) In the 35-54 age group, what language was spoken least?'),
     S(16, 'German · 6m', '(iii) · Calculate'), (fixed('Language', 6, 'German · 6m'),), '2-0', GRAPH),
    ('(iii)', 6, L(8, '(iii) Calculate the total percentage of French', 'three age groups shown.'),
     S(16, '20% · 6m', '(iv) State one way'), (fixed('Total', 6, '20% · 6m'),), '2-0', GRAPH),
    ('(iv)', 6, L(8, '(iv) State one way that the Irish language could be promoted further.'),
     S(16, 'One way stated', '(v) · Explain briefly'), (fixed('One way', 6, 'One way stated · 6m'),), '1-3', IRL),
    ('(v)', 6, L(8, '(v) Explain briefly one advantage of speaking an additional language.'),
     S(16, 'Brief explanation · 2 SRPs', 'Total 30m'),
     (srp3('Brief explanation', 2, 'Brief explanation · 2 SRPs @ 3m each · 3m + 3m'),), '1-3', IRL),
])

ACTIVITIES = ('The factors influencing agriculture in the region',
              'The importance of manufacturing to the region',
              'The reasons why tourists are attracted to the region.')
ACTIVITY_IDS = (
    'the-factors-influencing-agricultur-the-importance-of-manufacturing-to',
    'the-factors-influencing-agricultur-the-reasons-why-tourists-are-attra',
    'the-importance-of-manufacturing-to-the-reasons-why-tourists-are-attra',
)
ACTIVITY_PAIRS = ((0, 1), (0, 2), (1, 2))
PART_TWO.append(T(
    'p2-5b', P2, '5B', '', 40, 8, L(8, 'Economic Activities – Continental / Sub-Continental Region'),
    (L(8, 'Explain the development of any two of the following', 'attracted to the region.'),),
    (S(17, 'Region named · 4m', 'Total 40m'),),
    (fixed('Region named', 4, 'Region named · 4m'),
     srp3('Activity 1 explained', 6, 'Activity 1 explained 6 SRPs @ 3m each · 18m'),
     srp3('Activity 2 explained', 6, 'Activity 2 explained 6 SRPs @ 3m each · 18m')),
    '1-6', CONT, ID + 'p2-q5b-' + ACTIVITY_IDS[0], True,
    absorbs=tuple(ID + 'p2-q5b-' + slug for slug in ACTIVITY_IDS[1:])))
PART_TWO += romans('5C', 8, L(8, 'Characteristics of Regions'), (), ID + 'p2-q5c', (), [
    ('(i)', 15, L(8, '(i) Name one example of a core region', 'is a core region.'),
     S(17, 'Valid core region named', '(ii) · Name one example of a peripheral'),
     (fixed('Core region named', 3, 'Valid core region named · 3m'),
      srp3('Explanation', 4, 'Explanation: 4 SRPs @ 3m each · 12m')), '1-0', IRL + EURO),
    ('(ii)', 15, L(8, '(ii) Name one example of a peripheral region', 'peripheral region.'),
     S(17, 'Valid peripheral region named', 'Total 30m'),
     (fixed('Peripheral region named', 3, 'Valid peripheral region named · 3m'),
      srp3('Explanation', 4, 'Explanation: 4 SRPs @ 3m each · 12m')), '1-0', IRL + EURO),
])

Q6AS = (L(9, 'Examine the map above showing official and former members', 'following questions.'),)
PART_TWO += romans('6A', 9, L(9, 'European Union (EU)', nth=0), Q6AS, ID + 'p2-q6a', ('page',), [
    ('(i)', 6, L(9, '(i) Name one former member of the European Union.'),
     S(18, 'U.K. · 6m', '(ii) · Name one country'), (fixed('Former member', 6, 'U.K. · 6m'),), '1-3', EURO),
    ('(ii)', 6, L(9, '(ii) Name one country, shown on the map', 'membership.'),
     S(18, 'Valid answer · 6m', '(iii) · State one reason', after='(ii) · Name one country'),
     (fixed('Candidate country', 6, 'Valid answer · 6m'),), '1-3', EURO),
    ('(iii)', 6, L(9, '(iii) State one reason why countries want to join the EU.'),
     S(18, 'Valid answer · 6m', '(iv) · State two', after='(iii) · State one reason'),
     (fixed('Reason', 6, 'Valid answer · 6m'),), '1-3', EURO),
    ('(iv)', 6, L(9, '(iv) State two advantages of European Union membership for Ireland.'),
     S(18, 'Two advantages stated', '(v) · Explain briefly'),
     (fixed('Two advantages', 6, 'Two advantages stated @ 3m each · 3m + 3m', (0, 3, 6)),),
     '3-3', (O + 'economic-ireland-the-eu',) + EURO),
    ('(v)', 6, L(9, '(v) Explain briefly one challenge facing the EU today.'),
     S(18, 'Brief explanation two SRPs', 'Total 30m'),
     (srp3('Brief explanation', 2, 'Brief explanation two SRPs @ 3m each · 3m + 3m'),), '1-3', EURO),
])

Q6BS = (L(10, 'Answer each of the following with reference to an Irish region that you have studied.'),)
Q6BI = L(10, '(i) Name one tertiary economic activity', 'economy of this region.')
PART_TWO += romans('6B', 10, L(10, 'Tertiary Economic Activities – Irish Region'), Q6BS, ID + 'p2-q6b', (), [
    ('(i)', 4, Q6BI, S(19, 'One valid tertiary economic activity named', '(ii) · Explain the advantages'),
     (fixed('Tertiary economic activity named', 4, 'One valid tertiary economic activity named · 4m'),), '1-4', IRL),
    ('(ii)', 27, L(10, '(ii) Explain the advantages that this region has', 'named in part (i) above.'),
     S(19, 'Explanation 9 SRPs @ 3m each', '(iii) · Describe one challenge'),
     (srp3('Explanation', 9, 'Explanation 9 SRPs @ 3m each · 27m'),), '1-4', IRL, (Q6BI,)),
    ('(iii)', 9, L(10, '(iii) Describe one challenge faced by this tertiary economic activity in this region.'),
     S(19, 'Description 3 SRPs @ 3m each', 'Total 40m'),
     (srp3('Description', 3, 'Description 3 SRPs @ 3m each · 9m'),), '1-4', IRL, (Q6BI,)),
])
PART_TWO.append(T(
    'p2-6c', P2, '6C', '', 30, 10, L(10, 'Urban Regions'),
    (L(10, 'Describe and explain the reasons for the growth of any one urban area', 'studied.'),),
    (S(19, 'Description/explanation 10 SRPs @ 3m each', 'Total 30m'),),
    (srp3('Description/explanation', 10, 'Description/explanation 10 SRPs @ 3m each'),),
    '1-3', IRL + EURO, ID + 'p2-q6c', True))

ECON = (O + 'elective-economic',)
PART_TWO.append(sketch(
    12, L(12, 'Aerial Photograph'),
    L(12, 'Examine the aerial photograph of Dundalk accompanying this paper.', 'in the centre foreground.'),
    21, ID + 'p2-q7a', '2-8', AER, ('aerial',),
    ('The river', 'A bridge', 'A recreational area', 'An agricultural area in the right foreground',
     'A warehouse in the centre foreground')))
DEVELOPED = ('Tourism', 'Financial services', 'Services and footloose industries.')
DEVELOPED_IDS = ('tourism', 'financial-services', 'services-and-footloose-industries')
PART_TWO.append(T(
    'p2-7b', P2, '7B', '', 40, 12, L(12, 'Economic Development – Developed Economy'),
    (L(12, 'Describe and explain the development of one of the following', 'Services and footloose industries.'),),
    (S(22, 'Named developed economy', 'Total 40m'),),
    (fixed('Named developed economy', 4, 'Named developed economy · 4m'),
     srp3('Description/explanation', 12, 'Description/explanation 12 SRPs @ 3m each · 36m')),
    '3-0', ECON, ID + 'p2-q7b-tourism', True,
    routes=tuple(Route(slug, item.rstrip('.'), ID + 'p2-q7b-' + slug, True, keep_bullets=(item,))
                 for item, slug in zip(DEVELOPED, DEVELOPED_IDS))))
EU = (O + 'economic-ireland-the-eu',)
PART_TWO += romans('7C', 12, L(12, 'Ireland and the European Union'), (), ID + 'p2-q7c', (), [
    ('(i)', 3, L(12, '(i) Name any one European Union policy that affects Ireland’s economy.'),
     S(22, 'Valid policy named', '(ii) · Describe and explain'), (fixed('Policy named', 3, 'Valid policy named · 3m'),), '3-3', EU),
    ('(ii)', 27, L(12, '(ii) Describe and explain the effects of European Union policy(ies) on Ireland’s economy.'),
     S(22, 'Effect identified 1 SRP @ 3m', 'Total 30m'),
     (fixed('Effect identified', 3, 'Effect identified 1 SRP @ 3m · 3m'),
      srp3('Description and explanation', 8, 'Description and explanation 8 SRPs @ 3m each · 24m')), '3-3', EU),
])

Q8AS = (L(13, 'Examine the article above about the installation of solar panels', 'following questions.'),)
PART_TWO += romans('8A', 13, L(13, 'Renewable Energy'), Q8AS, ID + 'p2-q8a', ('page',), [
    ('(i)', 6, L(13, '(i) How many solar panels will be installed at Emerald Park?'),
     S(23, '300 solar panels · 6m', '(ii) · How many kWh'), (fixed('Solar panels', 6, '300 solar panels · 6m'),), '3-5', ECON),
    ('(ii)', 6, L(13, '(ii) How many kWh of clean energy will be generated by the project?'),
     S(23, '128 kWh · 6m', '(iii) · State one benefit'), (fixed('Clean energy', 6, '128 kWh · 6m'),), '3-5', ECON),
    ('(iii)', 6, L(13, '(iii) State one benefit of having solar panels in Emerald Park.'),
     S(23, 'Valid benefit · 6m', '(iv) · Name two sources'), (fixed('Benefit', 6, 'Valid benefit · 6m'),), '3-5', ECON),
    ('(iv)', 6, L(13, '(iv) Name two sources of renewable energy.'),
     S(23, 'Two valid sources named', '(v) · Explain briefly'),
     (fixed('Two sources', 6, 'Two valid sources named · 3m + 3m', (0, 3, 6)),), '3-5', ECON),
    ('(v)', 6, L(13, '(v) Explain briefly one disadvantage of renewable energy.'),
     S(23, 'Brief explanation 2 SRPs', 'Total 30m'),
     (srp3('Brief explanation', 2, 'Brief explanation 2 SRPs @ 3m each · 3m + 3m'),), '3-5', ECON),
])

MNC = (O + 'economic-multinationals-globalisation',)
Q8BI = L(13, '(i) Name one multinational company that you have studied', 'located in Ireland.')
PART_TWO += romans('8B', 13, L(13, 'Multinational Company'), (), ID + 'p2-q8b', (), [
    ('(i)', 4, Q8BI, S(24, 'Valid MNC named', '(ii) · Name one raw material'),
     (fixed('MNC named', 2, 'Valid MNC named · 2m'), fixed('Location stated', 2, 'Valid location stated · 2m')), '3-2', MNC),
    ('(ii)', 6, L(13, '(ii) Name one raw material required by this multinational company', 'by this multinational company.'),
     S(24, 'Raw material named', '(iii) · Explain the advantages'),
     (fixed('Raw material named', 3, 'Raw material named · 3m'), fixed('Product named', 3, 'Valid product named · 3m')),
     '3-2', MNC, (Q8BI,)),
    ('(iii)', 21, L(13, '(iii) Explain the advantages of being located in Ireland for this multinational company.'),
     S(24, 'Explanation 7 SRPs', '(iv) Explain one difficulty'),
     (srp3('Explanation', 7, 'Explanation 7 SRPs @ 3m each · 21m'),), '3-2', MNC, (Q8BI,)),
    ('(iv)', 9, L(13, '(iv) Explain one difficulty facing this multinational company.'),
     S(24, 'Explanation 3 SRPs @ 3m each', 'Total 40m', after='(iv) Explain one difficulty'),
     (srp3('Explanation', 3, 'Explanation 3 SRPs @ 3m each · 9m'),), '3-2', MNC, (Q8BI,)),
])
ENV = (O + 'economic-environmental-impact',)
Q8CI = L(13, '(i) Name one example of how the development of economic activities', 'conflict arising between people.')
PART_TWO += romans('8C', 13, L(13, 'Economic Activity and Conflict'), (), ID + 'p2-q8c', (), [
    ('(i)', 3, Q8CI, S(24, 'Valid example named · 3m', '(ii) · Describe and explain this conflict'),
     (fixed('Example named', 3, 'Valid example named · 3m'),), '3-4', ENV),
    ('(ii)', 27, L(13, '(ii) Describe and explain this conflict.'),
     S(24, 'Description and Explanation 9 SRPs', 'Total 30m', after='8C.'),
     (srp3('Description and explanation', 9, 'Description and Explanation 9 SRPs @ 3m each · 27m'),), '3-4', ENV, (Q8CI,)),
])

GRAPH_OL = (fixed('Graph paper', 3, 'Graph paper · 3m', (0, 3)),
            fixed('Vertical axis labelled / circle', 3, 'Vertical axis labelled/Circle · 3m graded (3/1/0)', (0, 1, 3)),
            fixed('Horizontal axis labelled / centred', 3, 'Horizontal axis labelled/Centred · 3m graded (3/1/0)', (0, 1, 3)),
            fixed('5 items illustrated', 15, '5 items @ 3m each graded (3/1/0) · 15m', sums(*[(0, 1, 3)] * 5)))
Q9AS = (L(14, 'Examine the table above showing expected years of schooling', 'following questions.'),)
PART_TWO += romans('9A', 14, L(14, 'Economic Development'), Q9AS, ID + 'p2-q9a', ('page',), [
    ('(i)', 24, L(14, '(i) Using graph paper, draw a suitable graph to illustrate this data.'),
     S(25, 'Graph paper · 3m', '(ii) · In your answer book'), GRAPH_OL, '2-0', GRAPH),
    ('(ii)', 6, L(14, '(ii) In your answer book, state two reasons why the expected years', 'lower than others.'),
     S(25, 'Two reasons stated', 'Total 30m'),
     (fixed('Two reasons', 6, 'Two reasons stated @ 3m each · 6m', (0, 3, 6)),), '3-1', (O + 'economic-developing-economies',)),
])
Q9BS = (L(14, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper.'),
        L(14, 'Imagine you have been given the task', 'covered by the map.'))
Q9BI = L(14, '(i) State, using a six-figure grid reference, where you would locate the hotel.')
PART_TWO += romans('9B', 14, L(14, 'Economic Activity – Ordnance Survey Map'), Q9BS, ID + 'p2-q9b', ('map', 'legend'), [
    ('(i)', 4, Q9BI, S(26, 'Six-figure grid reference', '(ii) · Explain the reasons'),
     (fixed('Six-figure grid reference', 4, 'Six-figure grid reference · 4m graded (4/2/0)', (0, 2, 4)),), '2-6', MAP),
    ('(ii)', 27, L(14, '(ii) Explain the reasons why you chose this location.'),
     S(26, 'Reasons explained 9 SRPs', '(iii) · Describe one disadvantage'),
     (srp3('Reasons explained', 9, 'Reasons explained 9 SRPs @ 3m each · 27m'),), '3-0', ECON + MAP, (Q9BI,)),
    ('(iii)', 9, L(14, '(iii) Describe one disadvantage of locating the hotel at this location.'),
     S(26, 'One disadvantage described', '[40m]'),
     (srp3('One disadvantage described', 3, 'One disadvantage described 3 SRPs @ 3m each · 9m'),), '3-0', ECON + MAP, (Q9BI,)),
])
PART_TWO += romans('9C', 14, L(14, 'Fossil Fuels'), (), ID + 'p2-q9c', (), [
    ('(i)', 6, L(14, '(i) Name two fossil fuels.'),
     S(26, 'Two valid fossil fuels named', '(ii) · Describe and explain the impact'),
     (fixed('Two fossil fuels', 6, 'Two valid fossil fuels named · 3m + 3m', (0, 3, 6)),), '3-5', ECON),
    ('(ii)', 24, L(14, '(ii) Describe and explain the impact of burning fossil fuels on the environment.'),
     S(26, 'Impact Identified', 'Total 30m'),
     (fixed('Impact identified', 3, 'Impact Identified · 3m'),
      srp3('Description/explanation', 7, 'Description/explanation 7 SRPs @ 3m each · 21m')), '3-4', ENV),
])

POP = (O + 'human-population',)
URB = (O + 'human-urban-geography',)
PART_TWO.append(sketch(
    15, L(15, 'Aerial Photograph'),
    L(15, 'Examine the aerial photograph of Dundalk accompanying this paper.', 'in the left middleground.'),
    27, ID + 'p2-q10a', '2-8', AER, ('aerial',),
    ('The river', 'A car park', 'An industrial area in the background', 'A sports ground in the right middleground',
     'An area of terraced housing in the left middleground')))
PART_TWO.append(T(
    'p2-10b', P2, '10B', '', 40, 15, L(15, 'Population Dynamics'),
    (L(15, '‘Birth rates and death rates are influenced', 'birth rates and death rates.'),),
    (S(28, 'Factors named · 5m + 5m', 'Total 40m'),),
    (fixed('Factors named', 10, 'Factors named · 5m + 5m', (0, 5, 10)),
     srp3('Description/explanation', 10, 'Description/explanation 10 SRPs @ 3m each · 30m')),
    '4-0', POP, ID + 'p2-q10b', True))
Q10CI = L(15, '(i) Name one city where urban sprawl has occurred.')
PART_TWO += romans('10C', 15, L(15, 'Urban Sprawl'), (), ID + 'p2-q10c', (), [
    ('(i)', 3, Q10CI, S(28, 'City named · 3m', '(ii) · Explain the reasons'), (fixed('City named', 3, 'City named · 3m'),), '4-5', URB),
    ('(ii)', 18, L(15, '(ii) Explain the reasons why urban sprawl has occurred in this city.'),
     S(28, 'Explanation 6 SRPs @ 3m each', '(iii) · Describe one solution'),
     (srp3('Explanation', 6, 'Explanation 6 SRPs @ 3m each · 18m'),), '4-5', URB, (Q10CI,)),
    ('(iii)', 9, L(15, '(iii) Describe one solution to urban sprawl.'),
     S(28, 'Description 3 SRPs @ 3m each', 'Total 30m', after='(iii) · Describe one solution'),
     (srp3('Description', 3, 'Description 3 SRPs @ 3m each · 9m'),), '4-5', URB),
])

Q11AS = (L(16, 'Examine the data above showing population of Ireland', 'following questions.'),)
PART_TWO += romans('11A', 16, L(16, 'Population', nth=0), Q11AS, ID + 'p2-q11a', ('page',), [
    ('(i)', 24, L(16, '(i) Using graph paper, draw a suitable graph to illustrate this data.'),
     S(29, 'Graph paper · 3m', '(ii) · In your answer book'), GRAPH_OL, '2-0', GRAPH),
    ('(ii)', 6, L(16, '(ii) In your answer book, explain briefly one challenge', 'increase in population.'),
     S(29, 'Brief explanation 2 SRPs', 'Total 30m'),
     (srp3('Brief explanation', 2, 'Brief explanation 2 SRPs @ 3m each · 6m'),), '4-1', POP),
])
Q11BI = L(16, '(i) State two reasons why people migrate from rural areas to urban areas.')
PART_TWO += romans('11B', 16, L(16, 'Migration – Rural to Urban'), (), ID + 'p2-q11b', (), [
    ('(i)', 4, Q11BI, S(30, 'Valid reasons stated', '(ii) · Describe and explain the effect'),
     (fixed('Two reasons', 4, 'Valid reasons stated · 2m + 2m', (0, 2, 4)),), '4-2', POP),
    ('(ii)', 18, L(16, '(ii) Describe and explain the effect of this migration on the urban areas', 'migrate to.'),
     S(30, 'Description/explanation 6SRPs', '(iii) · Describe and explain the effect', after='(ii) · Describe and explain the effect'),
     (srp3('Description/explanation', 6, 'Description/explanation 6SRPs @ 3m each · 18m'),), '4-2', POP, (Q11BI,)),
    ('(iii)', 18, L(16, '(iii) Describe and explain the effect of this migration on the rural areas', 'leave behind.'),
     S(30, 'Description/explanation 6SRPs', 'Total 40m', after='(iii) · Describe and explain the effect'),
     (srp3('Description/explanation', 6, 'Description/explanation 6SRPs @ 3m each · 18m'),), '4-2', POP, (Q11BI,)),
])
Q11CS = (L(16, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper and answer each of the following questions.'),)
Q11CI = L(16, '(i) Give a grid reference for an area on the map where there is an absence of settlement.')
Q11CIII = L(16, '(iii) Give a grid reference for an area on the map that has a relatively high density of settlement.')
PART_TWO += romans('11C', 16, L(16, 'Settlement Distribution'), Q11CS, ID + 'p2-q11c', ('map', 'legend'), [
    ('(i)', 3, Q11CI, S(30, 'Grid reference · 3/1/0m', '(ii) · Explain in detail', after='11C.'),
     (fixed('Grid reference', 3, 'Grid reference · 3/1/0m', (0, 1, 3)),), '2-6', MAP),
    ('(ii)', 12, L(16, '(ii) Explain in detail, using evidence from the map, why there is an absence', 'at this location.'),
     S(30, 'Explanation 4 SRPs @ 3m each', '(iii) · Give a grid reference', after='(ii) · Explain in detail'),
     (srp3('Explanation', 4, 'Explanation 4 SRPs @ 3m each · 12m'),), '4-3', URB + MAP, (Q11CI,)),
    ('(iii)', 3, Q11CIII, S(30, 'Grid reference · 3/1/0m', '(iv) · Explain in detail', after='(iii) · Give a grid reference'),
     (fixed('Grid reference', 3, 'Grid reference · 3/1/0m', (0, 1, 3)),), '2-6', MAP),
    ('(iv)', 12, L(16, '(iv) Explain in detail, using evidence from the map, why there is a relatively high density', 'at this location.'),
     S(30, 'Explanation 4 SRPs @ 3m each', 'Total 30m', after='(iv) · Explain in detail'),
     (srp3('Explanation', 4, 'Explanation 4 SRPs @ 3m each · 12m'),), '4-3', URB + MAP, (Q11CIII,)),
])

Q12AS = (L(17, 'Examine the information above about the plans for Luas Cork', 'following questions.'),)
PART_TWO += romans('12A', 17, L(17, 'Urban Development'), Q12AS, ID + 'p2-q12a', ('page',), [
    ('(i)', 6, L(17, '(i) In which city is the new Luas proposed?'),
     S(31, 'Cork · 6m', '(ii) · By what percent'), (fixed('City', 6, 'Cork · 6m'),), '4-4', URB),
    ('(ii)', 6, L(17, '(ii) By what percent is the population projected to grow', 'next 20 years?'),
     S(31, 'Up to 60 percent · 6m', '(iii) · How many new homes'), (fixed('Percent', 6, 'Up to 60 percent · 6m'),), '4-4', URB),
    ('(iii)', 6, L(17, '(iii) How many new homes is this project expected to generate?'),
     S(31, '20,000 · 6m', '(iv) · State two reasons'), (fixed('New homes', 6, '20,000 · 6m'),), '4-4', URB),
    ('(iv)', 6, L(17, '(iv) State two reasons why more people in Ireland live in urban areas.'),
     S(31, 'State two reasons @ 3m each', '(v) · Explain briefly'),
     (fixed('Two reasons', 6, 'State two reasons @ 3m each · 3m + 3m', (0, 3, 6)),), '4-3', URB),
    ('(v)', 6, L(17, '(v) Explain briefly what is meant by the term urban renewal.'),
     S(31, 'Brief explanation 2 SRPs', 'Total 30m'),
     (srp3('Brief explanation', 2, 'Brief explanation 2 SRPs @ 3m each · 3m + 3m'),), '4-4', URB),
])
Q12BI = L(17, '(i) Name one city in the developing world that is rapidly growing.')
PART_TWO += romans('12B', 17, L(17, 'Developing World City'), (), ID + 'p2-q12b', (), [
    ('(i)', 4, Q12BI, S(32, 'Developing world city named', '(ii) · Explain the reasons'),
     (fixed('Developing world city named', 4, 'Developing world city named · 4m'),), '4-5', URB),
    ('(ii)', 15, L(17, '(ii) Explain the reasons for the rapid growth of this developing world city.'),
     S(32, 'Explanation 5SRPs', '(iii) · Describe the problems'),
     (srp3('Explanation', 5, 'Explanation 5SRPs @ 3m each · 15m'),), '4-5', URB, (Q12BI,)),
    ('(iii)', 12, L(17, '(iii) Describe the problems caused by this rapid growth.'),
     S(32, 'Description 4SRPs', '(iv) · Explain one solution'),
     (srp3('Description', 4, 'Description 4SRPs @ 3m each · 12m'),), '4-5', URB, (Q12BI,)),
    ('(iv)', 9, L(17, '(iv) Explain one solution to these problems.'),
     S(32, 'Explanation 3SRPs', 'Total 40m'),
     (srp3('Explanation', 3, 'Explanation 3SRPs @ 3m each · 9m'),), '4-5', URB, (Q12BI,)),
])
PART_TWO += romans('12C', 17, L(17, 'Overpopulation', nth=0), (), ID + 'p2-q12c', (), [
    ('(i)', 6, L(17, '(i) Explain briefly what is meant by the term overpopulation.'),
     S(32, 'Brief explanation 2 SRPs', '(ii) · Describe and explain the causes'),
     (srp3('Brief explanation', 2, 'Brief explanation 2 SRPs @ 3m each · 6m'),), '4-1', POP),
    ('(ii)', 24, L(17, '(ii) Describe and explain the causes and effects of overpopulation', 'that you have studied.'),
     S(32, 'Description / Explanation 8 SRPs', 'Total 30m', after='12C.'),
     (srp3('Description/explanation', 8, 'Description / Explanation 8 SRPs @ 3m each · 24m'),), '4-1', POP),
])

TASKS = [*PART_ONE, *PART_TWO]

# Every 2026 Ordinary card id shipped before this review (58). Each must survive.
LEGACY_IDS = [
    'geography-2026-ol-p1-q1',
    'geography-2026-ol-p1-q2',
    'geography-2026-ol-p1-q3',
    'geography-2026-ol-p1-q4',
    'geography-2026-ol-p1-q5',
    'geography-2026-ol-p1-q6',
    'geography-2026-ol-p1-q7',
    'geography-2026-ol-p1-q8',
    'geography-2026-ol-p1-q9',
    'geography-2026-ol-p1-q10',
    'geography-2026-ol-p1-q11',
    'geography-2026-ol-p1-q12',
    'geography-2026-ol-p2-q1a',
    'geography-2026-ol-p2-q1b-route-i',
    'geography-2026-ol-p2-q1b-route-ii',
    'geography-2026-ol-p2-q1c',
    'geography-2026-ol-p2-q2a',
    'geography-2026-ol-p2-q2b',
    'geography-2026-ol-p2-q2c-quarrying',
    'geography-2026-ol-p2-q2c-mining',
    'geography-2026-ol-p2-q2c-oil-gas-exploitation',
    'geography-2026-ol-p2-q2c-geothermal-energy-production',
    'geography-2026-ol-p2-q3a',
    'geography-2026-ol-p2-q3b',
    'geography-2026-ol-p2-q3c-river-processes',
    'geography-2026-ol-p2-q3c-coastal-processes',
    'geography-2026-ol-p2-q3c-mass-movement-processes',
    'geography-2026-ol-p2-q4a',
    'geography-2026-ol-p2-q4b',
    'geography-2026-ol-p2-q4c',
    'geography-2026-ol-p2-q5a',
    'geography-2026-ol-p2-q5b-the-factors-influencing-agricultur-the-importance-of-manufacturing-to',
    'geography-2026-ol-p2-q5b-the-factors-influencing-agricultur-the-reasons-why-tourists-are-attra',
    'geography-2026-ol-p2-q5b-the-importance-of-manufacturing-to-the-reasons-why-tourists-are-attra',
    'geography-2026-ol-p2-q5c',
    'geography-2026-ol-p2-q6a',
    'geography-2026-ol-p2-q6b',
    'geography-2026-ol-p2-q6c',
    'geography-2026-ol-p2-q7a',
    'geography-2026-ol-p2-q7b-tourism',
    'geography-2026-ol-p2-q7b-financial-services',
    'geography-2026-ol-p2-q7b-services-and-footloose-industries',
    'geography-2026-ol-p2-q7c',
    'geography-2026-ol-p2-q8a',
    'geography-2026-ol-p2-q8b',
    'geography-2026-ol-p2-q8c',
    'geography-2026-ol-p2-q9a',
    'geography-2026-ol-p2-q9b',
    'geography-2026-ol-p2-q9c',
    'geography-2026-ol-p2-q10a',
    'geography-2026-ol-p2-q10b',
    'geography-2026-ol-p2-q10c',
    'geography-2026-ol-p2-q11a',
    'geography-2026-ol-p2-q11b',
    'geography-2026-ol-p2-q11c',
    'geography-2026-ol-p2-q12a',
    'geography-2026-ol-p2-q12b',
    'geography-2026-ol-p2-q12c',
]

ID_CORRECTION_REASON = (
    'The shipped card held every part of a question the scheme prices part by '
    'part. Its id is kept on the first separately priced part; the other parts '
    'are new cards with their own published allocation.')
