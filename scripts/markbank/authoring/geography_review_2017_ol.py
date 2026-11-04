"""Independent review ledger: Leaving Certificate Geography 2017 Ordinary Level.

Sources (English editions, harvested Paper Trail corpus; sizes and SHA-256
pinned in EXPECTED_SOURCES and the generated audit): the examination paper
LC005GLP000EV (28 pages; one booklet printed Part One, answered in it, and
Part Two), marking scheme LC005GLP000EV (40 pages), and the common Macroom
companions shared with Higher Level — the 1:50 000 map LC005CLP003EV (a
1136 x 784 pixel image in a one-page PDF), its legend LC005CLPC00EV and the
aerial photograph LC005CLP004EV. Part One is 100 marks (any ten of twelve
@ 10), Part Two 300 (three questions @ 100).

Visual sweep (every page rendered and read on 2026-10-14):
  Paper p1 cover and examiner's grid; p2-p11 Part One Questions 1-12 (p6
  holds Q5 and Q6, p8 Q8 and Q9; Q2 prints an OS map extract of a coast);
  p12 Part Two instructions; p13 Section 1 divider; p14-p19 Q1-Q6 (p14 and
  p17 open with their dividers); p20 Section 2 divider; p21-p27 Electives
  Q7-Q12 (p21 and p24 open with their elective dividers; p26 holds 12A,
  p27 12B and 12C); p28 printed "Blank Page".
  Scheme p1 cover; p2-p3 notes; p4-p5 Geographical Investigation
  (coursework) and its presentation marks; p6-p7 Part One table (Q1-Q6,
  Q7-Q12); p8 Part Two instructions and Section 1 divider; p9-p34 Q1-Q12;
  p35 investigation topics; p36 Irish-language bonus marks; p37-p39
  printed "Blank Page"; p40 back cover.

Boundaries and tariffs follow the 2018 Ordinary ledger: every priced roman
is a task, and so is every lettered statement priced on its own (Q4(i)(a)-
(d), Q11(iv)(a)-(b)). Matching tables, in the printed row order: Q1 Outer
core C, Crust A, Inner core D, Mantle B; Q2 Sea stack D, Beach A, Cliff B,
Headland C; Q3 prints (i) and (ii) in one part-completed table: (i) Ox-bow
lake C, Cirque/Corrie/Tarn A, V-Shaped valley B (U-Shaped valley D is
printed), (ii) U-Shaped valley Glacial, V-Shaped valley River (the other
two are printed); Q6(i) W 333 692 Dispersed, W 366 721 Nucleated, W 317
722 Linear; Q8 The Greater Dublin Area B, Munster Ridge and Valley C, Cool
Temperate Oceanic E, The Basque region A, Departement D; Q9 Mining
Primary, Banking Tertiary, Construction Secondary, Manufacturing
Secondary, Forestry Primary (Tourism Tertiary is printed); Q12 Airport
runway C, Pyramids in Egypt D, Grand Canyon A, Flooding B; Part Two 3A(i)
Freeze-thaw action C, Carbonation A, Onion weathering B and (ii) Physical,
Chemical, Physical. The scheme credits either answer to Q7(i) ("True/
False 2m") and the card carries it as printed.

Tariffs as printed: twelve parts carry 40 marks (1B, 2B, 3B, 4B, 5B, 6B,
7C, 8B, 9C, 10C, 11B, 12C) and the rest 30.
"""

from geography_review import (
    Criterion, Lift, Route, SchemeSlice, Task, pool, fixed, slug, srp, steps, sums,
)

YEAR = 2017
LEVEL = 'ordinary'
PAPER_PAGES = {1: 28, 2: 28}
SCHEME_PAGES = 40
_FORTY = {'1B', '2B', '3B', '4B', '5B', '6B', '7C', '8B', '9C', '10C', '11B', '12C'}
QUESTION_TARIFFS = {1: {str(n): 10 for n in range(1, 13)},
                    2: {f'{n}{x}': (40 if f'{n}{x}' in _FORTY else 30)
                        for n in range(1, 13) for x in 'ABC'}}

EXPECTED_SOURCES = {
    'paper1': ('LC005GLP000EV.pdf', 2623267),
    'paper2': ('LC005GLP000EV.pdf', 2623267),
    'scheme': ('LC005GLP000EV.pdf', 603572),
    'map': ('LC005CLP003EV.pdf', 352988),
    'legend': ('LC005CLPC00EV.pdf', 745443),
    'aerial': ('LC005CLP004EV.pdf', 602913),
}

_PAPER = {1: 'cover and examiner grid', **{p: 'question' for p in range(2, 12)},
          12: 'Part Two instructions', 13: 'section divider', **{p: 'question' for p in range(14, 20)},
          20: 'section divider', **{p: 'question' for p in range(21, 28)}, 28: 'blank page'}
PAGE_REVIEW = {
    # One booklet printed both parts.
    'paper1': _PAPER, 'paper2': _PAPER,
    'scheme': {1: 'cover', 2: 'notes', 3: 'notes', 4: 'geographical investigation (coursework)',
               5: 'presentation marks (coursework)', 6: 'Part One table', 7: 'Part One table',
               8: 'Part Two instructions and section divider',
               **{p: 'Part Two allocation' for p in range(9, 35)},
               35: 'investigation topics', 36: 'Irish-language bonus marks',
               37: 'blank', 38: 'blank', 39: 'blank', 40: 'back cover'},
}

EXPECTED_SELECTION_SCAN = [
    [1, 2, 'attempt any ten'], [1, 5, 'choose'], [1, 12, 'attempt three'], [1, 13, 'attempt two'],
    [1, 14, 'attempt one'],
    [1, 15, 'answer (i) or (ii)'], [1, 15, 'any two'], [1, 15, 'any two'], [1, 15, 'one of the following'],
    [1, 16, 'any two'], [1, 16, 'one of the following'],
    [1, 17, 'attempt one'],
    [1, 18, 'any two'],
    [1, 20, 'attempt one'],
    [1, 23, 'one of the following'],
    [1, 25, 'any three'],
]
SELECTION_REVIEW = [
    {'scan': [[1, 2, 'attempt any ten'], [1, 12, 'attempt three'], [1, 13, 'attempt two'], [1, 14, 'attempt one'],
              [1, 17, 'attempt one'], [1, 20, 'attempt one']],
     'kind': 'exam-attempt-rule',
     'reason': 'Part One any ten of twelve and Part Two three questions (one of Q1-3, one of Q4-6, one elective) are attempt rules; every question is carded.'},
    {'scan': [[1, 15, 'answer (i) or (ii)']], 'kind': 'closed-route',
     'reason': '2B: (i) or (ii) -> two routes, each with its own scheme allocation.'},
    {'scan': [[1, 15, 'one of the following'], [1, 16, 'one of the following'], [1, 23, 'one of the following']],
     'kind': 'closed-choose-one',
     'reason': '2C one of four printed rock-cycle activities -> 4 routes; 3C one of three printed surface processes -> 3 routes; 9B one of three printed activities -> 3 routes.'},
    {'scan': [[1, 18, 'any two'], [1, 25, 'any three']], 'kind': 'choose-n-one-card',
     'reason': '5B any two of three printed activities and 11C any three of four printed factors -> one card each with every printed item (choice is not a route). 4C "two of the factors listed below" (three printed) is one card on the same rule.'},
    {'scan': [[1, 15, 'any two'], [1, 15, 'any two'], [1, 16, 'any two']], 'kind': 'open-response',
     'reason': 'No printed pool: 2B(i) any two landforms and 2B(ii) any two mass movement processes (the scheme prices two @ 20m); 3A(iii) any two factors.'},
    {'scan': [[1, 5, 'choose']], 'kind': 'not-a-selection',
     'reason': 'Part One Q4(i) "Choose the correct option in each of the following statements": each lettered statement is a priced answer, not a candidate route.'},
]

P1, P2 = 1, 2
ID = 'geography-2017-ol-'
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

# ---------------------------------------------------------------- Part One --
TICK = 'Tick the correct box.'
PART_ONE = romans('1', P1, 2, L(2, 'Layers of the Earth'),
                  (L(2, 'Examine the diagram above which shows the different layers of the earth', 'following questions.'),),
                  ID + 'p1-q1', ('page',), [
    ('(i)', 8, L(2, '(i) Match each of the letters A, B, C and D with the correct layer in the table below.'),
     S(6, 'Q1.(i)', 'Q.1(ii)'), rows(['Q1.(i) · C · 2m', '=A · 2m', '=D · 2m', '=B · 2m']), '0-0', PS,
     (L(2, 'Outer core'), L(2, 'Crust'), L(2, 'Inner core'), L(2, 'Mantle'))),
    ('(ii)', 2, L(2, '(ii) What term is given to the molten rock found in the mantle?'),
     S(6, 'Q.1(ii)', 'Q.2(i)'), (fixed('Molten rock', 2, 'Q.1(ii) · Magma · 2m · Total 10m'),), '0-0', PS + EV),
])
PART_ONE += romans('2', P1, 3, L(3, 'Coastal Landforms and Processes'),
                   (L(3, 'Examine the Ordnance Survey map extract above and answer each of the following questions.'),),
                   ID + 'p1-q2', ('page',), [
    ('(i)', 8, L(3, '(i) Match each of the letters A, B, C and D with the landform that best matches it', 'table below.'),
     S(6, 'Q.2(i)', 'Q.2(ii)'), rows(['Q.2(i) · D · 2m', '=A · 2m', '=B · 2m', '=C · 2m']), '0-10', SEA,
     (L(3, 'Sea stack'), L(3, 'Beach'), L(3, 'Cliff'), L(3, 'Headland'))),
    ('(ii)', 2, L(3, '(ii) Which one of the landforms in the table above is formed as a result of coastal',
                  'deposition?'),
     S(6, 'Q.2(ii)', 'Q.3(i)'), (fixed('Landform', 2, 'Q.2(ii) · Beach / A · 2m · Total 10m'),), '0-10', SEA),
])
Q3S = (L(4, 'Examine the photographs above and complete the table', 'completed for you.'),)
PART_ONE += [
    T('p1-3-i', P1, '3', '(i)', 6, 4, L(4, 'Rivers and Glaciation'),
      (L(4, '(i) Match each of the photographs A, B and C with the landform that best matches', 'table below.'),),
      # The U-shaped valley row prints D on the paper; its scheme line "D
      # Glacial · 2m" prices the (ii) answer only, so it is not part of (i).
      (S(6, 'Q.3(i)', 'D Glacial'), S(6, 'A (Glacial)', 'Q.4(i)')),
      (fixed('Row 1', 2, 'Q.3(i) · C Q.3 (ii) (River) · 2m'), fixed('Row 2', 2, 'A (Glacial) · 2m'),
       fixed('Row 3', 2, 'B River · 2m + 2m · Total 10m')),
      '0-9', RIVERS + GLAC, ID + 'p1-q3', ('page',), Q3S,
      row_labels=(L(4, 'Ox-bow lake'), L(4, 'Cirque/Corrie/Tarn'), L(4, 'V-Shaped valley'))),
    T('p1-3-ii', P1, '3', '(ii)', 4, 4, L(4, 'Rivers and Glaciation'),
      (L(4, '(ii) State whether each of the landforms named in the table is formed by', 'glacial processes.'),),
      (S(6, 'D Glacial', 'A (Glacial)'), S(6, 'B River', 'Q.4(i)')),
      (fixed('Row 1', 2, 'D Glacial · 2m'), fixed('Row 2', 2, 'B River · 2m + 2m · Total 10m')),
      '0-9', RIVERS + GLAC, ID + 'p1-q3-ii', ('page',), Q3S,
      row_labels=(L(4, 'U-Shaped valley'), L(4, 'V-Shaped valley'))),
]
Q4I = L(5, '(i) Choose the correct option in each of the following statements and write the', 'spaces provided.')
PART_ONE += romans('4', P1, 5, L(5, 'Rocks'),
                   (L(5, 'Examine the photograph above of a basalt area in Ireland', 'following questions.'),),
                   ID + 'p1-q4', ('page',), [
    ('(i)(a)', 2, (Q4I, L(5, '(a) Basalt is an example of a metamorphic rock or an igneous rock.')),
     S(6, 'Q.4(i)', '(b) cooling'), (fixed('Statement (a)', 2, 'Q.4(i) · (a) Igneous · 2m'),), '0-1', RW),
    ('(i)(b)', 2, (Q4I, L(5, '(b) Basalt most commonly forms as a result of the cooling of lava near the',
                          'far below the earth’s surface.')),
     S(6, '(b) cooling', '(c) small'), (fixed('Statement (b)', 2, '(b) cooling lava near surface · 2m'),), '0-1', RW),
    ('(i)(c)', 2, (Q4I, L(5, '(c) Basalt consists mainly of small crystals or large crystals.')),
     S(6, '(c) small', '(d) The Giant'), (fixed('Statement (c)', 2, '(c) small crystals · 2m'),), '0-1', RW),
    ('(i)(d)', 2, (Q4I, L(5, '(d) Basalt can be found in the Wicklow Mountains or The Giant’s Causeway.')),
     S(6, '(d) The Giant', 'Q.4(ii)'), (fixed('Statement (d)', 2, '(d) The Giant’s Causeway · 2m'),), '0-1', RW),
    ('(ii)', 2, L(5, '(ii) Name one use of rocks.'),
     S(6, 'Q.4(ii)', 'Q.5(i)'), (fixed('Use of rocks', 2, 'Q.4(ii) · One valid use · 2m · Total 10m'),), '0-1', RW),
])
Q5S = (L(6, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper and', 'following questions.',
         nth=0),)
Q6S = (L(6, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper and', 'following questions.',
         nth=1),)
PART_ONE += romans('5', P1, 6, L(6, 'Ordnance Survey Map', nth=0), Q5S, ID + 'p1-q5', ('map', 'legend'), [
    ('(i)', 5, (L(6, '(i) What is the length of the R587 regional road', TICK), L(6, '4.1 km'), L(6, '6.7 km')),
     S(6, 'Q.5(i)', 'Q.5(ii)'), (fixed('Length', 5, 'Q.5(i) · 6.7 km · 5m'),), '2-6', MAP),
    ('(ii)', 5, (L(6, '(ii) If a person travelled from the school in Dromleigh W 284 652', TICK),
                 L(6, 'North', nth=0), L(6, 'North-east')),
     S(6, 'Q.5(ii)', 'Q.6(i)'), (fixed('Direction', 5, 'Q.5(ii) · North-east · 5m · Total 10m'),), '2-6', MAP),
])
PART_ONE += romans('6', P1, 6, L(6, 'Ordnance Survey Map', nth=1), Q6S, ID + 'p1-q6', ('map', 'legend'), [
    ('(i)', 6, L(6, '(i) State whether the settlement pattern at each of the following grid references',
                 'settlement pattern.'),
     S(6, 'Q.6(i)', 'Q.6(ii)'), rows(['Q.6(i) · Dispersed/scattered · 2m', 'Nucleated/clustered · 2m',
                                      'Linear/ribbon · 2m']), '4-3', URB + MAP,
     (L(6, 'W 333 692'), L(6, 'W 366 721'), L(6, 'W 317 722'))),
    ('(ii)', 2, L(6, '(ii) Name the antiquity that can be found at W 364 688.'),
     S(6, 'Q.6(ii)', 'Q.6(iii)'), (fixed('Antiquity', 2, 'Q.6(ii) · Standing Stone · 2m'),), '2-6', MAP),
    ('(iii)', 2, L(6, '(iii) Draw the Ordnance Survey map symbol for a Ringfort in the box below.'),
     S(6, 'Q.6(iii)', None), (fixed('Symbol', 2, 'Q.6(iii) · Correct symbol · 2m · Total 10m'),), '2-6', MAP),
])
Q7 = (('(i)', 'There is a graveyard in the left background of the aerial photograph.', 'Q.7', '(ii) True',
       'Q.7 · (i) True/ False · 2m'),
      ('(ii)', 'There is a roundabout in the left foreground of the aerial photograph.', '(ii) True', '(iii) False',
       '(ii) True · 2m'),
      ('(iii)', 'The bridging point of the river is in the left middleground of the aerial', '(iii) False', '(iv) True',
       '(iii) False · 2m'),
      ('(iv)', 'The Central Business District (CBD) is in the centre middleground of the aerial', '(iv) True',
       '(v) False', '(iv) True · 2m'),
      ('(v)', 'This aerial photograph is a vertical aerial photograph.', '(v) False', 'Q.8',
       '(v) False · 2m · Total 10m'))
PART_ONE += romans('7', P1, 7, L(7, 'Aerial Photograph'),
                   (L(7, 'Examine the aerial photograph of Macroom accompanying this paper.'),
                    L(7, 'State whether each of the following statements is True or False.')),
                   ID + 'p1-q7', ('aerial',), [
    (roman, 2, L(7, f'{roman} {statement}', None if statement.endswith('.') else 'photograph.'),
     S(7, start, end), (fixed('True or false', 2, line),), '2-8', AER) for roman, statement, start, end, line in Q7])
PART_ONE += [
    T('p1-8', P1, '8', '', 10, 8, L(8, 'Regions'),
      (L(8, 'Match the description of a region with the example of the region', 'in the table below.'),),
      (S(7, 'Q.8', 'Q.9'),), rows(['Q.8 · B · 2m', '=C · 2m', '=E · 2m', '=A · 2m', 'D · 2m · Total 10m']),
      '1-0', IRL + EURO, ID + 'p1-q8', ('page',),
      row_labels=(L(8, 'The Greater Dublin Area'), L(8, 'Munster Ridge and Valley'), L(8, 'Cool Temperate Oceanic'),
                  L(8, 'The Basque region'), L(8, 'Département'))),
    T('p1-9', P1, '9', '', 10, 8, L(8, 'Economic Activities'),
      (L(8, 'Write the category of economic activity, Primary, Secondary or Tertiary', 'One is completed for you.'),),
      (S(7, 'Q.9', 'Q.10'),),
      rows(['Q.9 · Primary · 2m', '=Tertiary · 2m', '=Secondary · 2m@0', '=Secondary · 2m@1',
            'Primary · 2m · Total 10m']),
      '3-0', ECON, ID + 'p1-q9', ('page',),
      row_labels=(L(8, 'Mining'), L(8, 'Banking'), L(8, 'Construction'), L(8, 'Manufacturing'), L(8, 'Forestry'))),
]
PART_ONE += romans('10', P1, 9, L(9, 'Population', nth=0),
                   (L(9, 'Examine the table above showing the projected population', 'following questions.'),),
                   ID + 'p1-q10', ('page',), [
    ('(i)', 2, L(9, '(i) Name the city with the largest population in 2011.'),
     S(7, 'Q.10', '(ii) Rio'), (fixed('City', 2, 'Q.10 · (i) Tokyo · 2m'),), '2-0', GRAPH),
    ('(ii)', 2, L(9, '(ii) Which city is projected to have the smallest population in 2025?'),
     S(7, '(ii) Rio', '(iii) Mumbai'), (fixed('City', 2, '(ii) Rio de Janeiro · 2m'),), '2-0', GRAPH),
    ('(iii)', 2, L(9, '(iii) Which city is projected to have the highest percentage growth in population',
                   '2011 and 2025?'),
     S(7, '(iii) Mumbai', '(iv) Mexico'), (fixed('City', 2, '(iii) Mumbai · 2m'),), '2-0', GRAPH),
    ('(iv)', 2, L(9, '(iv) Which city is projected to have the second highest percentage growth in', '2011 and 2025?'),
     S(7, '(iv) Mexico', '(v) 4'), (fixed('City', 2, '(iv) Mexico City · 2m'),), '2-0', GRAPH),
    ('(v)', 2, L(9, '(v) By how many million people is the population of New York projected to grow',
                 '2011 and 2025?'),
     S(7, '(v) 4', 'Q.11'), (fixed('Growth', 2, '(v) 4 · 2m · Total 10m'),), '2-0', GRAPH + URB),
])
Q11IV = (L(10, '(iv) Complete the following sentences by inserting the correct word from the list', 'in each case.'),
         L(10, 'Isotherms Isohyets'))
PART_ONE += romans('11', P1, 10, L(10, 'Weather', nth=0),
                   (L(10, 'Examine the weather chart above and answer each of the following questions.'),),
                   ID + 'p1-q11', ('page',), [
    ('(i)', 2, L(10, '(i) What is the barometric pressure (in hectopascals/millibars) to the north of', 'Spain?'),
     S(7, 'Q.11', '(ii) Correct'), (fixed('Pressure', 2, 'Q.11 · (i) 994 · 2m'),), '2-7', WEATHER),
    ('(ii)', 2, L(10, '(ii) Draw the weather chart symbol for a warm front, in the box below.'),
     S(7, '(ii) Correct', '(iii) Calm'), (fixed('Symbol', 2, '(ii) Correct symbol · 2m'),), '2-7', WEATHER),
    ('(iii)', 2, (L(10, '(iii) According to the weather chart, what type of wind conditions is Ireland', TICK),
                  L(10, 'Calm'), L(10, 'Stormy')),
     S(7, '(iii) Calm', '(iv) (a)'), (fixed('Wind conditions', 2, '(iii) Calm · 2m'),), '2-7', WEATHER),
    ('(iv)(a)', 2, (*Q11IV, L(10, '(a) Lines joining places of equal rainfall on a weather chart are called')),
     S(7, '(iv) (a)', '(b) Isotherms'), (fixed('Term', 2, '(iv) (a) Isohyets · 2m'),), '2-7', WEATHER),
    ('(iv)(b)', 2, (*Q11IV, L(10, '(b) Lines joining places of equal temperature on a weather chart are called')),
     S(7, '(b) Isotherms', 'Q.12(i)'), (fixed('Term', 2, '(b) Isotherms · 2m · Total 10m'),), '2-7', WEATHER),
])
PART_ONE += romans('12', P1, 11, L(11, 'Satellite Interpretation'),
                   (L(11, 'Examine the satellite images above and answer each of the following questions.'),),
                   ID + 'p1-q12', ('page',), [
    ('(i)', 8, L(11, '(i) Match each of the images A, B, C and D with the description that best matches', 'table below.'),
     S(7, 'Q.12(i)', 'Q.12(ii)'), rows(['Q.12(i) · C · 2m', '=D · 2m', '=A · 2m', '=B · 2m']), '2-8', AER,
     (L(11, 'Airport runway'), L(11, 'Pyramids in Egypt'), L(11, 'Grand Canyon'), L(11, 'Flooding'))),
    ('(ii)', 2, L(11, '(ii) State one use of satellite images.'),
     S(7, 'Q.12(ii)', None), (fixed('Use', 2, 'Q.12(ii) · Valid use · 2m · Total 10m'),), '2-8', AER),
])


# ---------------------------------------------------------------- Part Two --
def sketch(page, title, prompt, scheme_page, card_id, topic, atlas, sources, proportions, bullets):
    item = sums((0, 1, 3), (0, 2))
    return T(f'p2-{card_id.rsplit("-q", 1)[1]}', P2, card_id.rsplit('-q', 1)[1].upper(), '', 30, page,
             title, (prompt,), (S(scheme_page, 'Sketch Outline:', 'Total 30m'),),
             (fixed('Limits/frame', 1, ('Sketch Outline:', 'imits/')),
              fixed(f'Proportions ({proportions})', 2, f'Proportions ({proportions}) · 2m'),
              fixed('Overall impression', 2, '2m graded (2/1/0)', (0, 1, 2)),
              *(Criterion(f'Item {n}', 5, item, 'exact',
                          ('Five items shown and labelled as follows:', 'Showing · 3m graded (3/1/0)',
                           'Labelled · 2m')) for n in range(1, 6))),
             topic, atlas, card_id, sources,
             row_labels=(None, None, None, *(L(page, b) for b in bullets)))


def two_of(label, count, head, each, lines, unit):
    per = sums(*unit)
    return tuple(Criterion(f'{label} {n}', count, per, 'srp', (head, each, *lines)) for n in (1, 2))


SHOWN = 'Shown · 4m graded (4/2/0)'
NAMED_SHOWN = sums((0, 2), (0, 2, 4))
GRAPH_OL = (fixed('Graph paper', 3, 'Graph paper · 3m', (0, 3)),
            fixed('Vertical axis labelled / circle', 3, 'Vertical axis labelled/Circle · 3m graded (3/1/0)', (0, 1, 3)),
            fixed('Horizontal axis labelled / centred', 3, 'Horizontal axis labelled/Centred · 3m graded (3/1/0)',
                  (0, 1, 3)),
            fixed('5 items illustrated', 15, '5 items @ 3m each graded (3/1/0) · 15m', sums(*[(0, 1, 3)] * 5)))
SURFACE = ('River processes', 'Coastal processes', 'Mass movement processes.')
ROCK = ('Quarrying', 'Mining', 'Oil/Gas exploitation', 'Geothermal energy production.')

PART_TWO = [
    sketch(14, L(14, 'Ordnance Survey Map'),
           L(14, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper.',
             'The built up area of Macroom.'),
           9, ID + 'p2-q1a', '2-6', MAP + RIVERS, ('map', 'legend'), 'landscape',
           ('The entire area of the Reservoir east of Lee Bridge (W 342 713)',
            'An area of land above 200 metres at Cill na Martra in the north-west of the map', 'The Sullane River',
            'An area of coniferous plantation in the south-west of the map', 'The built up area of Macroom')),
]
PART_TWO += romans('1B', P2, 14, L(14, 'Rocks'), (), ID + 'p2-q1b', (), [
    ('(i)', 6, L(14, '(i) Name two examples of sedimentary rocks.'),
     S(10, '(i) · Name two examples', '(ii) · State two'),
     (fixed('Two sedimentary rocks', 6, 'Two sedimentary rocks named @ 3m each · 6m', (0, 3, 6)),), '0-1', RW),
    ('(ii)', 7, L(14, '(ii) State two different Irish locations where sedimentary rocks are found.'),
     S(10, '(ii) · State two', '(iii) · Describe'),
     (fixed('Location 1', 4, 'Location 1 · 4m'), fixed('Location 2', 3, 'Location 2 · 3m')), '0-1', RW + IRL),
    ('(iii)', 27, L(14, '(iii) Describe and explain how sedimentary rocks are formed.'),
     S(10, '(iii) · Describe', 'Total 40m'),
     (srp3('Description/explanation', 9, 'Description/Explanation 9 SRP’s @ 3m each · 27m'),), '0-1', RW),
])
PART_TWO.append(T(
    'p2-1c', P2, '1C', '', 30, 14, L(14, 'Fold Mountains', nth=0),
    (L(14, 'With the aid of a diagram(s), describe and explain how Fold Mountains are formed.'),),
    (S(10, 'Diagram two items', 'Total 30m'),),
    (fixed('Diagram', 6, 'Diagram two items @ 3m each · 6m', (0, 3, 6)),
     srp3('Explanation', 8, 'Explanation 8 SRP’s @ 3m each · 24m')),
    '0-2', RW + PS, ID + 'p2-q1c'))

PART_TWO += romans('2A', P2, 15, L(15, 'Volcanoes', nth=0),
                   (L(15, 'Read the extract above and answer each of the following questions.'),),
                   ID + 'p2-q2a', ('page',), [
    ('(i)', 3, L(15, '(i) What percentage of volcanoes exist within the Pacific Ring of Fire?'),
     S(11, '(i) · What percentage', '(ii) · State what'), (fixed('Percentage', 3, '90 (%) · 3m'),), '0-7', EV),
    ('(ii)', 3, L(15, '(ii) State what is meant by the name Pacific Ring of Fire.'),
     S(11, '(ii) · State what', '(iii) · Name two'), (fixed('Statement', 3, 'Valid statement · 3m'),), '0-7', EV + PS),
    ('(iii)', 6, L(15, '(iii) Name two materials that are emitted into the air when volcanoes erupt.'),
     S(11, '(iii) · Name two', '(iv) · Explain briefly'),
     (fixed('Two materials', 6, 'Two valid materials named @ 3m each · 6m', (0, 3, 6)),), '0-7', EV),
    ('(iv)', 6, L(15, '(iv) Explain briefly what is meant by the term extinct volcano.'),
     S(11, '(iv) · Explain briefly', '(v) · List two'),
     (srp3('Brief explanation', 2, 'Brief explanation two SRP’s @ 3m each · 6m'),), '0-7', EV),
    ('(v)', 6, L(15, '(v) List two negative effects of volcanoes.'),
     S(11, '(v) · List two', '(vi) · Explain briefly'),
     (fixed('Two negative effects', 6, 'Two valid negative effects @ 3m each · 6m', (0, 3, 6)),), '0-7', EV),
    ('(vi)', 6, L(15, '(vi) Explain briefly one positive effect of volcanoes.'),
     S(11, '(vi) · Explain briefly', 'Total 30m'),
     (srp3('Brief explanation', 2, 'Brief explanation two SRP’s @ 3m each · 6m'),), '0-7', EV),
])
PART_TWO += [
    T('p2-2b', P2, '2B', '', 40, 15, L(15, 'Landform Development'),
      (L(15, '(i) Explain, with the aid of diagrams, the formation of any two landforms.'),),
      (S(12, 'Formation of any two landforms @ 20m each.', 'Total 40m'),),
      two_of('Landform', 20, 'Formation of any two landforms @ 20m each.', 'For each landform:',
             ('Landform named · 1m', 'Diagram(s) two aspects @ 2m each · 4m',
              'Formation explained 5 SRP’s @ 3m each · 15m'),
             ((0, 1), (0, 2, 4), steps(15, 3))),
      '0-4', PS_SURFACE, ID + 'p2-q2b-route-i',
      routes=(
          Route('route-i', 'Route (i)', ID + 'p2-q2b-route-i', False),
          Route('route-ii', 'Route (ii)', ID + 'p2-q2b-route-ii', False,
                prompt=(L(15, '(ii) Describe and explain any two processes of mass movement.'),),
                scheme=(S(12, 'Any two processes @ 20m each', 'Total 40m'),),
                criteria=two_of('Process', 20, 'Any two processes @ 20m each', 'For each process:',
                                ('Process stated · 2m', 'Description / Explanation 6 SRP’s @ 3m each · 18m'),
                                ((0, 2), steps(18, 3))),
                topic='0-8', atlas=RW),
      )),
    T('p2-2c', P2, '2C', '', 30, 15, L(15, 'Human Interaction with the Rock Cycle'),
      (L(15, 'Describe and explain how humans interact with the rock cycle with reference to',
         'Geothermal energy production.'),),
      (S(13, 'Description / explanation 10', 'Total 30m'),),
      (srp3('Description/explanation', 10, 'Description / explanation 10 SRP’s @ 3m each · 30m'),),
      '0-6', RW, ID + 'p2-q2c-quarrying', routes=bullet_routes('p2-q2c-', ROCK)),
]

Q3AS = (L(16, 'Examine the photographs above and answer each of the following questions.'),)
WEATHERING_ROWS = (L(16, 'Freeze-thaw action'), L(16, 'Carbonation'), L(16, 'Onion weathering (exfoliation)'))
PART_TWO += romans('3A', P2, 16, L(16, 'Weathering'), Q3AS, ID + 'p2-q3a', ('page',), [
    ('(i)', 9, L(16, '(i) In your answer book, match each of the photographs A, B and C with the process',
                 'Onion weathering (exfoliation).'),
     S(14, 'C · Freeze-thaw', '(ii) · State whether'),
     (fixed('Row 1', 3, 'C · Freeze-thaw action · 3m'), fixed('Row 2', 3, 'A · Carbonation · 3m'),
      fixed('Row 3', 3, 'B · Onion weathering (exfoliation) · 3m')), '0-8', RW, WEATHERING_ROWS),
    ('(ii)', 9, L(16, '(ii) State whether each of the processes of weathering listed above are examples of',
                  'physical/mechanical weathering.'),
     S(14, 'Freeze-thaw action · Physical', '(iii) · Name any two'),
     (fixed('Row 1', 3, 'Freeze-thaw action · Physical/mechanical weathering · 3m'),
      fixed('Row 2', 3, 'Carbonation · Chemical weathering · 3m'),
      fixed('Row 3', 3, 'Onion weathering (exfoliation) · Physical/mechanical weathering · 3m')), '0-8', RW,
     WEATHERING_ROWS),
    ('(iii)', 6, L(16, '(iii) Name any two factors that influence weathering.'),
     S(14, '(iii) · Name any two', '(iv) · Explain briefly'),
     (fixed('Two factors', 6, 'Two valid factors named at 3m each · 6m', (0, 3, 6)),), '0-8', RW),
    ('(iv)', 6, L(16, '(iv) Explain briefly what is meant by the term scree.'),
     S(14, '(iv) · Explain briefly', 'Total 30m'),
     (srp3('Brief explanation', 2, 'Brief explanation two SRP’s @ 3m each · 6m'),), '0-8', RW),
])
PART_TWO += romans('3B', P2, 16, L(16, 'Earthquakes'), (), ID + 'p2-q3b', (), [
    ('(i)', 6, L(16, '(i) Name two examples of different locations where earthquakes have occurred.'),
     S(14, '(i) · Name two examples', '(ii) · Name a scale'),
     (fixed('Two locations', 6, 'Two different locations named @ 3m each · 6m', (0, 3, 6)),), '0-7', EV),
    ('(ii)', 4, L(16, '(ii) Name a scale used to measure the force of an earthquake.'),
     S(14, '(ii) · Name a scale', '(iii) · Explain how'), (fixed('Scale', 4, 'Valid scale named @ 4m · 4m'),),
     '0-7', EV),
    ('(iii)', 30, L(16, '(iii) Explain how earthquakes occur and describe their main effects.'),
     S(14, '(iii) · Explain how', 'Total 40m'),
     (srp3('Explanation/description', 10, 'Explanation/description 10 SRP’s @ 3m each · 30m'),), '0-7', EV + PS),
])
PART_TWO.append(T(
    'p2-3c', P2, '3C', '', 30, 16, L(16, 'Human Interaction with Surface Processes'),
    (L(16, 'Examine how humans interact with one of the following surface processes:', 'Mass movement processes.'),),
    (S(15, 'Interaction identified · 3m', 'Total 30m'),),
    (fixed('Interaction identified', 3, 'Interaction identified · 3m'),
     srp3('Explanation', 9, 'Explanation 9 SRP’s @ 3m each · 27m')),
    '0-6', RIVERS, ID + 'p2-q3c-river-processes',
    routes=bullet_routes('p2-q3c-', SURFACE, atlas=dict(zip(SURFACE, (RIVERS, SEA, RW))))))

PART_TWO.append(T(
    'p2-4a', P2, '4A', '', 30, 17, L(17, 'European Region'),
    (L(17, 'Draw a sketch map of a European region (not in Ireland) that you have studied.',
       '(upland or lowland) in this region.'),),
    (S(16, 'Outline of Region', 'Total 30m'),),
    (fixed('Outline of region', 6, 'Outline of Region · 6m graded (6/4/2/0)', (0, 2, 4, 6)),
     Criterion('River', 6, NAMED_SHOWN, 'exact', ('River · Named · 2m', f'={SHOWN}@0')),
     Criterion('Town/City 1', 6, NAMED_SHOWN, 'exact', ('Town/City 1 · Named · 2m', f'={SHOWN}@1')),
     Criterion('Town/City 2', 6, NAMED_SHOWN, 'exact', ('Town/City 2 · Named · 2m', f'={SHOWN}@2')),
     Criterion('Relief (upland/lowland)', 6, NAMED_SHOWN, 'exact',
               ('Relief (upland/lowland) · Named · 2m', f'={SHOWN}@3'))),
    '1-5', EURO, ID + 'p2-q4a'))
Q4BS = (L(17, 'Answer each of the following with reference to an Irish region that you have studied.'),)
Q4BI = L(17, '(i) Name one tertiary economic activity that contributes to the economy of this', 'region.')
FACTORS_4C = ('Climate', 'Relief and soils', 'Markets.')
PART_TWO += romans('4B', P2, 17, L(17, 'Tertiary Economic Activities – Irish Region'), Q4BS, ID + 'p2-q4b', (), [
    ('(i)', 4, Q4BI, S(17, '(i) · Name one tertiary', '(ii) · Explain the advantages'),
     (fixed('Tertiary economic activity named', 4, 'Tertiary economic activity named · 4m'),), '1-4', IRL),
    ('(ii)', 27, L(17, '(ii) Explain the advantages that this region has for the development of the tertiary',
                   'part (i) above.'),
     S(17, '(ii) · Explain the advantages', '(iii) · Describe one'),
     (srp3('Explanation', 9, 'Explanation 9 SRP’s @ 3m each · 27m'),), '1-4', IRL, (), (Q4BI,)),
    ('(iii)', 9, L(17, '(iii) Describe one challenge faced by this tertiary economic activity in this region.'),
     S(17, '(iii) · Describe one', 'Total 40m'),
     (srp3('Description', 3, 'Description 3 SRP’s @ 3m each · 9m'),), '1-4', IRL, (), (Q4BI,)),
])
PART_TWO.append(T(
    'p2-4c', P2, '4C', '', 30, 17, L(17, 'Agriculture – Continental / Sub-Continental Region'),
    (L(17, 'Explain how two of the factors listed below influence the development of agriculture in', 'Markets.'),),
    (S(17, 'Factor 1 explained', 'Total 30m'),),
    (srp3('Factor 1', 5, 'Factor 1 explained 5 SRP’s @ 3m each · 15m'),
     srp3('Factor 2', 5, 'Factor 2 explained 5 SRP’s @ 3m each · 15m')),
    '1-6', CONT, ID + 'p2-q4c', absorbs=pool(ID + 'p2-q4c-', FACTORS_4C, 2)[1]))

PART_TWO += romans('5A', P2, 18, L(18, 'Agriculture in Ireland', nth=0),
                   (L(18, 'Examine the information above regarding the Irish agri-food and drink sector in 2015',
                      'following questions.'),),
                   ID + 'p2-q5a', ('page',), [
    ('(i)', 3, L(18, '(i) What percentage of Ireland’s population is employed in the agri-food and drink', 'sector?'),
     S(18, '(i) · What percentage', '(ii) · What was the value'), (fixed('Percentage', 3, '8.6 (%) · 3m'),),
     '2-0', GRAPH),
    ('(ii)', 3, L(18, '(ii) What was the value of exports (€) from the Irish agri-food and drink sector in 2015?'),
     S(18, '(ii) · What was the value', '(iii) · Calculate X'), (fixed('Value of exports', 3, '10.8 billion · 3m'),),
     '2-0', GRAPH),
    ('(iii)', 6, L(18, '(iii) Calculate X, the percentage of Irish agri-food and drink exported to the UK in 2015.'),
     S(18, '(iii) · Calculate X', '(iv) · How many'), (fixed('X', 6, '41 (%) · 6m'),), '2-0', GRAPH),
    ('(iv)', 6, L(18, '(iv) How many hectares of land is used for agriculture and how many hectares of',
                  'used for forestry?'),
     S(18, '(iv) · How many', '(v) · Explain briefly'),
     (fixed('Agriculture', 3, '4.5 million (hectares) · 3m'), fixed('Forestry', 3, '730,000 (hectares) · 3m')),
     '2-0', GRAPH),
    ('(v)', 6, L(18, '(v) Explain briefly one advantage of European Union membership for Ireland’s agri-food',
                 'drink sector.'),
     S(18, '(v) · Explain briefly', '(vi) · Explain briefly'),
     (srp3('Brief explanation', 2, 'Brief explanation two SRP’s @ 3m each · 6m'),), '3-3', EU),
    ('(vi)', 6, L(18, '(vi) Explain briefly one disadvantage of European Union membership for Ireland’s',
                  'drink sector.'),
     S(18, '(vi) · Explain briefly', 'Total 30m'),
     (srp3('Brief explanation', 2, 'Brief explanation two SRP’s @ 3m each · 6m'),), '3-3', EU),
])
ACTIVITIES_5B = ('The reasons why tourists are attracted to the region', 'The importance of manufacturing to the region',
                 'The development of transport in the region.')
PART_TWO += [
    T('p2-5b', P2, '5B', '', 40, 18, L(18, 'Economic Activities – European Region'),
      (L(18, 'Explain the development of any two of the following with reference to a European region',
         'The development of transport in the region.'),),
      (S(18, 'Activity 1 explained', 'Total 40m'),),
      (srp3('Activity 1 explained', 7, 'Activity 1 explained 7 SRP’s @ 3m each · 21m'),
       srp3('Activity 2 explained', 6, 'Activity 2 explained 6 SRP’s @ 3m each · 18m'),
       fixed('Region named', 1, 'Region named · 1m')),
      '1-5', EURO, ID + 'p2-q5b', absorbs=pool(ID + 'p2-q5b-', ACTIVITIES_5B, 2)[1]),
    T('p2-5c', P2, '5C', '', 30, 18, L(18, 'Urban Growth – Continental / Sub-Continental Region'),
      (L(18, 'Describe and explain the reasons for the growth of an urban area in a', 'that you have studied.'),),
      (S(19, 'Description / Explanation 10', 'Total 30m'),),
      (srp3('Description/explanation', 10, 'Description / Explanation 10 SRP’s @ 3m each · 30m'),),
      '1-6', CONT + URB, ID + 'p2-q5c'),
]

PART_TWO += romans('6A', P2, 19, L(19, 'European Unemployment'),
                   (L(19, 'Examine the table above showing the percentage of people unemployed in selected',
                      'following questions.'),),
                   ID + 'p2-q6a', ('page',), [
    ('(i)', 3, L(19, '(i) Which country had the highest percentage of people unemployed in 2015?'),
     S(20, '(i) · Which country', '(ii) · Which two'), (fixed('Country', 3, 'Greece · 3m'),), '2-0', GRAPH),
    ('(ii)', 6, L(19, '(ii) Which two countries experienced a decrease in the percentage of people',
                  'from 2005 to 2015?'),
     S(20, '(ii) · Which two', '(iii) · In which year'),
     (fixed('Country 1', 3, 'Germany · 3m'), fixed('Country 2', 3, 'Poland · 3m')), '2-0', GRAPH),
    ('(iii)', 9, L(19, '(iii) In which year was the percentage of people unemployed in Ireland lower than the',
                   'reason for this.'),
     S(20, '(iii) · In which year', '(iv) · Explain briefly'),
     (fixed('Year', 3, '2005 · 3m'), srp3('Brief explanation', 2, 'Brief explanation two SRP’s @ 3m each · 6m')),
     '1-4', IRL + GRAPH),
    ('(iv)', 6, L(19, '(iv) Explain briefly one possible reason why Poland’s percentage of people',
                  'from 2005 to 2015.'),
     S(20, '(iv) · Explain briefly', '(v) · Explain briefly'),
     (srp3('Brief explanation', 2, 'Brief explanation two SRP’s @ 3m each · 6m'),), '1-5', EURO),
    ('(v)', 6, L(19, '(v) Explain briefly one way of reducing unemployment levels.'),
     S(20, '(v) · Explain briefly', 'Total 30m'),
     (srp3('Brief explanation', 2, 'Brief explanation two SRP’s @ 3m each · 6m'),), '1-5', EURO),
])
PART_TWO += romans('6B', P2, 19, L(19, 'European Union Expansion'), (), ID + 'p2-q6b', (), [
    ('(i)', 4, L(19, '(i) Name two countries that joined the European Union since 2000.'),
     S(20, '(i) · Name two countries', '(ii) · Explain the advantages'),
     (fixed('Two countries', 4, 'Two valid countries named at 2m each · 4m', (0, 2, 4)),), '1-5', EURO),
    ('(ii)', 18, L(19, '(ii) Explain the advantages of European Union expansion for Ireland.'),
     S(20, '(ii) · Explain the advantages', '(iii) · Explain the disadvantages'),
     (srp3('Explanation', 6, 'Explanation 6 SRP’s @ 3m each · 18m'),), '1-5', EURO + EU),
    ('(iii)', 18, L(19, '(iii) Explain the disadvantages of European Union expansion for Ireland.'),
     S(20, '(iii) · Explain the disadvantages', 'Total 40m'),
     (srp3('Explanation', 6, 'Explanation 6 SRP’s @ 3m each · 18m'),), '1-5', EURO + EU),
])
PART_TWO.append(T(
    'p2-6c', P2, '6C', '', 30, 19, L(19, 'Regional Development'),
    (L(19, 'Describe and explain two problems faced by any region that you have studied.'),),
    (S(21, 'Problem 1', 'Total 30m'),),
    (srp3('Problem 1', 5, ('Problem 1', '=Description/Explanation 5 SRP’s @ 3m each · 15m@0')),
     srp3('Problem 2', 5, ('Problem 2', '=Description/Explanation 5 SRP’s @ 3m each · 15m@1'))),
    '1-0', IRL + EURO, ID + 'p2-q6c'))

PART_TWO.append(sketch(
    21, L(21, 'Ordnance Survey Map'),
    L(21, 'Examine the Ordnance Survey map and legend accompanying this paper.', 'A post office.'),
    23, ID + 'p2-q7a', '2-6', MAP + ECON, ('map', 'legend'), 'landscape',
    ('The built up area of Macroom', 'The entire route of the N22 national primary road',
     'The entire route of the R584 regional road', 'The electricity transmission line in the north-east of the map',
     'A post office')))
Q7CI = L(21, '(i) Name one example of environmental pollution that you have studied.')
PART_TWO += [
    T('p2-7b', P2, '7B', '', 30, 21, L(21, 'European Union', nth=0),
      (L(21, 'Explain how European Union policies have impacted on the Irish economy.'),),
      (S(24, 'Impact Identified', 'C. · Environmental Pollution'),),
      (fixed('Impact identified', 3, 'Impact Identified 1 SRP · 3m'),
       srp3('Explanation', 9, 'Explanation 9 SRP’s @ 3m each · 27m')),
      '3-3', EU, ID + 'p2-q7b'),
]
PART_TWO += romans('7C', P2, 21, L(21, 'Environmental Pollution'), (), ID + 'p2-q7c', (), [
    ('(i)', 4, Q7CI, S(24, '(i) · Name one example', '(ii) · Explain the cause'),
     (fixed('Example named', 4, 'Valid example named · 4m'),), '3-4', ENV),
    ('(ii)', 24, L(21, '(ii) Explain the cause and effects of this environmental pollution.'),
     S(24, '(ii) · Explain the cause', '(iii) · Describe how'),
     (fixed('Cause identified', 3, 'Cause identified one SRP @ 3m each · 3m'),
      fixed('Effect identified', 3, 'Effect identified one SRP @ 3m each · 3m'),
      srp3('Explanation', 6, 'Explanation 6 SRP’s @ 3m each · 18m')), '3-4', ENV, (), (Q7CI,)),
    ('(iii)', 12, L(21, '(iii) Describe how this environmental pollution could be reduced.'),
     S(24, '(iii) · Describe how', 'Total 40m'),
     (srp3('Description', 4, 'Description 4 SRP’s @ 3m each · 12m'),), '3-4', ENV, (), (Q7CI,)),
])

PART_TWO += romans('8A', P2, 22, L(22, 'Energy Consumption', nth=0),
                   (L(22, 'Examine the information above relating to energy consumption in Ireland by fuel source',
                      'following questions.'),),
                   ID + 'p2-q8a', ('page',), [
    ('(i)', 3, L(22, '(i) What percentage of energy consumed in 1990 was generated from coal?'),
     S(25, '(i) · What percentage', '(ii) · What percentage'), (fixed('Percentage', 3, '41.7 (%) · 3m'),),
     '2-0', GRAPH),
    ('(ii)', 3, L(22, '(ii) What percentage of energy consumed in 2015 was generated from coal?'),
     S(25, '(ii) · What percentage', '(iii) · Explain briefly'), (fixed('Percentage', 3, '16.9 (%) · 3m'),),
     '2-0', GRAPH),
    ('(iii)', 6, L(22, '(iii) Explain briefly what is meant by the term fossil fuel.'),
     S(25, '(iii) · Explain briefly', '(iv) · Calculate'),
     (srp3('Brief explanation', 2, 'Brief explanation two SRP’s @ 3m each · 6m'),), '3-5', ECON),
    ('(iv)', 6, L(22, '(iv) Calculate the percentage of energy consumed in 1990 that was generated from',
                  'fossil fuels.'),
     S(25, '(iv) · Calculate', '(v) · Explain briefly'), (fixed('Percentage', 6, '95.1 (%) · 6m'),), '2-0', GRAPH),
    ('(v)', 6, L(22, '(v) Explain briefly what is meant by the term renewable energy.'),
     S(25, '(v) · Explain briefly', '(vi) · Explain briefly'),
     (srp3('Brief explanation', 2, 'Brief explanation two SRP’s @ 3m each · 6m'),), '3-5', ECON),
    ('(vi)', 6, L(22, '(vi) Explain briefly one reason for the increase in the use of wind as an energy source.'),
     S(25, '(vi) · Explain briefly', 'Total 30m'),
     (srp3('Brief explanation', 2, 'Brief explanation two SRP’s @ 3m each · 6m'),), '3-5', ECON),
])
Q8BI = L(22, '(i) Name one multinational company operating in Ireland.')
PART_TWO += romans('8B', P2, 22, L(22, 'Multinational Company (MNC)'), (), ID + 'p2-q8b', (), [
    ('(i)', 4, Q8BI, S(25, '(i) · Name one multinational', '(ii) · Name one raw'),
     (fixed('MNC named', 4, 'Valid MNC named · 4m'),), '3-2', MNC),
    ('(ii)', 6, L(22, '(ii) Name one raw material used by this multinational company and name the',
                  'raw material is sourced.'),
     S(25, '(ii) · Name one raw', '(iii) · Name one product'),
     (fixed('Raw material named', 3, 'Valid raw material named · 3m'),
      fixed('Source country named', 3, 'Valid source country named · 3m')), '3-2', MNC, (), (Q8BI,)),
    ('(iii)', 3, L(22, '(iii) Name one product manufactured by this multinational company.'),
     S(25, '(iii) · Name one product', '(iv) · State where'), (fixed('Product named', 3, 'Valid product named · 3m'),),
     '3-2', MNC, (), (Q8BI,)),
    ('(iv)', 27, L(22, '(iv) State where this multinational company is located in Ireland and explain in detail',
                   'at this location.'),
     S(25, '(iv) · State where', 'Total 40m'),
     (fixed('Location', 3, 'Valid location · 3m'), srp3('Explanation', 8, 'Explanation 8 SRP’s @ 3m each · 24m')),
     '3-2', MNC, (), (Q8BI,)),
])
Q8CI = L(22, '(i) Name one developing economy which has been colonised.')
PART_TWO += romans('8C', P2, 22, L(22, 'Colonialism – Developing Economy'), (), ID + 'p2-q8c', (), [
    ('(i)', 3, Q8CI, S(26, '(i) · Name one developing', '(ii) · Explain the impacts'),
     (fixed('Developing economy named', 3, 'Named developing economy · 3m'),), '3-1', DEV),
    ('(ii)', 27, L(22, '(ii) Explain the impacts of colonialism on this developing economy.'),
     S(26, '(ii) · Explain the impacts', 'Total 30m'),
     (srp3('Explanation', 9, 'Explanation 9 SRP’s @ 3m each · 27m'),), '3-1', DEV, (), (Q8CI,)),
])

PART_TWO += romans('9A', P2, 23, L(23, 'Economic Development', nth=0),
                   (L(23, 'Examine the table above showing the Gross Domestic Product (GDP) per capita in $US',
                      'following questions.'),),
                   ID + 'p2-q9a', ('page',), [
    ('(i)', 24, L(23, '(i) Using graph paper, draw a suitable graph to illustrate this data.'),
     S(27, 'Graph paper', '(ii) · In your answer book'), GRAPH_OL, '2-0', GRAPH),
    ('(ii)', 6, L(23, '(ii) In your answer book, state two reasons why the Gross Domestic Product (GDP)',
                  'higher than for others.'),
     S(27, '(ii) · In your answer book', 'Total 30m'),
     (fixed('Two reasons', 6, 'Two valid reasons stated @ 3m each · 6m', (0, 3, 6)),), '3-1', DEV + ECON),
])
ACTIVITIES_9B = ('Tourism', 'Financial services', 'Service and footloose industries.')
PART_TWO.append(T(
    'p2-9b', P2, '9B', '', 30, 23, L(23, 'Economic Development – Developed Economy'),
    (L(23, 'Describe and explain the development of one of the following with reference to a',
       'Service and footloose industries.'),),
    (S(27, 'Named developed economy · 3m', 'Total 30m'),),
    (fixed('Developed economy named', 3, 'Named developed economy · 3m'),
     srp3('Description and explanation', 9, 'Description and explanation 9 SRP’s @ 3m each · 27m')),
    '3-0', ECON, ID + 'p2-q9b-tourism', routes=bullet_routes('p2-q9b-', ACTIVITIES_9B)))
Q9CS = (L(23, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper.'),)
Q9CI = L(23, '(i) Using a six-figure grid reference, state clearly where you would locate a wind', 'farm.')
PART_TWO += romans('9C', P2, 23, L(23, 'Economic Activity and Conflict'), Q9CS, ID + 'p2-q9c', ('map', 'legend'), [
    ('(i)', 4, Q9CI, S(28, '(i) · Using a six-figure', '(ii) · Using evidence'),
     (fixed('Six-figure grid reference', 4, 'Six-figure grid reference · 4m graded (4/2/0)', (0, 2, 4)),),
     '2-6', MAP + ECON),
    ('(ii)', 24, L(23, '(ii) Using evidence from the Ordnance Survey map, explain why you selected this',
                   'for the wind farm.'),
     S(28, '(ii) · Using evidence', '(iii) · Describe and explain'),
     (fixed('Map evidence', 3, 'Map evidence · 3m'), srp3('Explanation', 7, 'Explanation 7 SRP’s @ 3m each · 21m')),
     '3-5', ECON + MAP, (), (Q9CI,)),
    ('(iii)', 12, L(23, '(iii) Describe and explain how conflict may arise as a result of locating the wind farm',
                    'at this location.'),
     S(28, '(iii) · Describe and explain', 'Total 40m'),
     (srp3('Description', 4, 'Description 4 SRP’s @ 3m each · 12m'),), '3-4', ENV, (), (Q9CI,)),
])

PART_TWO += romans('10A', P2, 24, L(24, 'Population Dynamics'),
                   (L(24, 'Examine the table above showing life expectancy at birth for selected countries',
                      'following questions.'),),
                   ID + 'p2-q10a', ('page',), [
    ('(i)', 24, L(24, '(i) Using graph paper, draw a suitable graph to illustrate this data.'),
     S(29, 'Graph paper', '(ii) · In your answer book'), GRAPH_OL, '2-0', GRAPH),
    ('(ii)', 6, L(24, '(ii) In your answer book, state two ways that life expectancy could be increased in',
                  'Mali and Sudan.'),
     S(29, '(ii) · In your answer book', 'Total 30m'),
     (fixed('Two ways', 6, 'Two valid statements @ 3m each · 6m', (0, 3, 6)),), '4-0', POP),
])
HISTORIC = ('For each historic settlement:', 'Description: 2 SRP’s @ 3 marks each · 18 marks')
Q10BS = (L(24, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper.'),)
Q10BI = L(24, '(i) Name and give a six-figure grid reference for the location of three different',
          'Ordnance Survey map.')
PART_TWO += romans('10B', P2, 24, L(24, 'Historic Settlement'), Q10BS, ID + 'p2-q10b', ('map', 'legend'), [
    ('(i)', 12, Q10BI, S(29, '(i) · Name and give', '(ii) · Describe each'),
     (fixed('Three settlements named', 6, '3 settlements named @ 2 marks each · 6 marks', (0, 2, 4, 6)),
      fixed('Three settlements located', 6, '3 settlements located @ 2 marks each graded (2/1/0) · 6 marks',
            tuple(range(7)))), '4-3', URB + MAP),
    ('(ii)', 18, L(24, '(ii) Describe each of the three historic settlements named in part (i) above.'),
     S(29, '(ii) · Describe each', 'Total 30m'),
     tuple(Criterion(f'Settlement {n}', 6, steps(6, 3), 'srp', HISTORIC) for n in (1, 2, 3)), '4-3', URB + MAP,
     (), (Q10BI,)),
])
Q10CI = L(24, '(i) Name one city where urban sprawl has occurred.')
PART_TWO += romans('10C', P2, 24, L(24, 'Urban Sprawl'), (), ID + 'p2-q10c', (), [
    ('(i)', 4, Q10CI, S(30, '(i) · Name one city', '(ii) · Explain the reasons'),
     (fixed('City named', 4, 'Named city · 4m'),), '4-5', URB),
    ('(ii)', 27, L(24, '(ii) Explain the reasons why urban sprawl has occurred in this city.'),
     S(30, '(ii) · Explain the reasons', '(iii) · Describe one'),
     (srp3('Explanation', 9, 'Explanation 9 SRP’s @ 3m each · 27m'),), '4-5', URB, (), (Q10CI,)),
    ('(iii)', 9, L(24, '(iii) Describe one solution to urban sprawl.'),
     S(30, '(iii) · Describe one', 'Total 40m'),
     (srp3('One solution described', 3, 'One solution described 3 SRP’s @ 3m each · 9m'),), '4-5', URB),
])

PART_TWO.append(sketch(
    25, L(25, 'Aerial Photograph'),
    L(25, 'Examine the aerial photograph of Macroom accompanying this paper.', 'A recreational area.'),
    31, ID + 'p2-q11a', '2-8', AER + URB, ('aerial',), 'landscape',
    ('Two connecting streets', 'The river', 'The church in the left middleground',
     'An area of warehousing in the left foreground', 'A recreational area')))
IDENTIFIED = sums((0, 3), (0, 2))
FACTORS_11C = ('Resources', 'Society and culture', 'Income levels', 'Technology.')
PART_TWO += romans('11B', P2, 25, L(25, 'Migration – Rural to Urban'), (), ID + 'p2-q11b', (), [
    ('(i)', 20, L(25, '(i) Explain the reasons why people migrate from rural areas to urban areas.'),
     S(32, '(i) · Explain the reasons', '(ii) · Explain the problems'),
     (Criterion('Two reasons identified', 5, IDENTIFIED, 'exact', ('Two reasons identified @ 3m + 2m · 5m',)),
      srp3('Explanation', 5, 'Explanation 5 SRP’s @ 3m each · 15m')), '4-2', POP),
    ('(ii)', 20, L(25, '(ii) Explain the problems experienced in urban areas as a result of this migration.'),
     S(32, '(ii) · Explain the problems', 'Total 40m'),
     (Criterion('Two problems identified', 5, IDENTIFIED, 'exact', ('Two problems identified @ 3m + 2m · 5m',)),
      srp3('Explanation', 5, 'Explanation 5 SRP’s @ 3m each · 15m')), '4-5', URB + POP),
])
PART_TWO.append(T(
    'p2-11c', P2, '11C', '', 30, 25, L(25, 'Population Dynamics'),
    (L(25, 'Explain how any three of the following factors influence population:', 'Technology.'),),
    (S(32, 'Explanation of three factors:', 'Total 30m'),),
    (srp3('First factor', 4, 'First factor explained 4 SRP’s @ 3m each · 12m'),
     srp3('Second factor', 3, 'Second factor explained 3 SRP’s @ 3m each · 9m'),
     srp3('Third factor', 3, 'Third factor explained 3 SRP’s @3m each · 9m')),
    '4-1', POP, ID + 'p2-q11c', absorbs=pool(ID + 'p2-q11c-', FACTORS_11C, 3)[1]))

TOWN_REASON = ('Three reasons @ 10m each · 30m', 'For each reason:', 'Ordnance Survey map evidence · 1m',
               'Explanation 3 SRP’s @ 3m each · 9m')
Q12CI = L(27, '(i) Name one city in the developing world that is rapidly growing.')
PART_TWO += romans('12A', P2, 26, L(26, 'Migration', nth=0),
                   (L(26, 'Examine the graph above showing the number of migrants rescued by the Irish Naval',
                      'following questions.'),),
                   ID + 'p2-q12a', ('page',), [
    ('(i)', 6, L(26, '(i) How many migrants were rescued in May 2015 and how many migrants were', 'May 2016?'),
     S(33, '(i) · How many', '(ii) · Calculate'),
     (fixed('May 2015', 3, '2015: 501 migrants · 3m'), fixed('May 2016', 3, '2016: 522 migrants · 3m')), '2-0', GRAPH),
    ('(ii)', 6, L(26, '(ii) Calculate the total number of migrants rescued in 2016', 'May, June and July combined.'),
     S(33, '(ii) · Calculate', '(iii) · Name two'), (fixed('Total', 6, '1,334 migrants · 6m'),), '2-0', GRAPH),
    ('(iii)', 6, L(26, '(iii) Name two pull factors that result in people migrating to Europe.'),
     S(33, '(iii) · Name two', '(iv) · Explain briefly'),
     (fixed('Two pull factors', 6, 'Two valid pull factors named @ 3m each · 6m', (0, 3, 6)),), '4-2', POP),
    ('(iv)', 6, L(26, '(iv) Explain briefly one of the pull factors named in part (iii) above.'),
     S(33, '(iv) · Explain briefly', '(v) · Explain briefly'),
     (srp3('Brief explanation', 2, 'Brief explanation two SRP’s @ 3m each · 6m'),), '4-2', POP),
    ('(v)', 6, L(26, '(v) Explain briefly one positive impact for the European Union of receiving these',
                 'migrants.'),
     S(33, '(v) · Explain briefly', 'Total 30m'),
     (srp3('Brief explanation', 2, 'Brief explanation two SRP’s @ 3m each · 6m'),), '4-2', POP),
])
PART_TWO.append(T(
    'p2-12b', P2, '12B', '', 30, 27, L(27, 'Development of Urban Settlements'),
    (L(27, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper.'),
     L(27, 'Explain three reasons why the town of Macroom developed at this location', 'support each reason.')),
    (S(34, 'Three reasons @ 10m each', 'Total 30m'),),
    tuple(Criterion(f'Reason {n}', 10, sums((0, 1), steps(9, 3)), 'srp', TOWN_REASON) for n in (1, 2, 3)),
    '4-3', URB + MAP, ID + 'p2-q12b', ('map', 'legend')))
PART_TWO += romans('12C', P2, 27, L(27, 'Developing World City'), (), ID + 'p2-q12c', (), [
    ('(i)', 4, Q12CI, S(34, '(i) · Name one city', '(ii) · Explain the reasons'),
     (fixed('Developing world city named', 4, 'Developing City named · 4m'),), '4-5', URB),
    ('(ii)', 15, L(27, '(ii) Explain the reasons for the rapid growth of this developing world city.'),
     S(34, '(ii) · Explain the reasons', '(iii) · Describe the problems'),
     (srp3('Explanation', 5, 'Explanation 5 SRP’s @ 3m each · 15m'),), '4-5', URB, (), (Q12CI,)),
    ('(iii)', 12, L(27, '(iii) Describe the problems caused by this rapid growth.'),
     S(34, '(iii) · Describe the problems', '(iv) · Explain one'),
     (srp3('Description', 4, 'Description 4 SRP’s @ 3m each · 12m'),), '4-5', URB, (), (Q12CI,)),
    ('(iv)', 9, L(27, '(iv) Explain one solution to these problems.'),
     S(34, '(iv) · Explain one', 'Total 40m'),
     (srp3('Explanation', 3, 'Explanation 3 SRP’s @ 3m each · 9m'),), '4-5', URB, (), (Q12CI,)),
])

TASKS = [*PART_ONE, *PART_TWO]

ID_CORRECTION_REASON = 'No 2017 Ordinary card shipped before this review; every card is new.'

# No 2017 Ordinary card was live on origin/main before this review.
LEGACY_IDS: list[str] = []
