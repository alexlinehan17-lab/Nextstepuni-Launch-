"""Independent review ledger: Leaving Certificate Geography 2023 Ordinary Level.

Sources (English editions, Paper Trail index; sizes and SHA-256 pinned in
EXPECTED_SOURCES and the generated audit): Part One and Answerbook
LC005GLP042EV (40 pages), Part Two LC005GLP043EV (20 pages), marking scheme
LC005GLP000EV (40 pages), and the common companions shared with Higher Level
in the harvested corpus — the 1:50 000 Cavan map LC005CLP003EV, its legend
LC005CLPC00EV and the Cavan aerial photograph LC005CLP004EV (published only
as a JPEG).

Visual sweep (every page rendered and read on 2026-10-12):
  Part One booklet p1 cover; p2 instructions (Part One "Attempt any TEN",
  100 marks; Part Two "attempt three", 300 marks); p3-p12 Questions 1-12 (p6
  holds Q4 and Q5, p7 holds Q6 and Q7); p13 Part Two answerbook
  instructions; p14-p17 graph-paper answer pages; p18-p39 lined answer
  pages; p40 copyright/back cover.
  Part Two booklet p1 cover; p2 Part Two instructions; p3-p10 Sections 1-2
  (Q1-Q6; p5 holds only 2C, p9 holds only 5C); p11 Section 3 divider;
  p12-p18 Electives (Q7-Q12; p15 holds only 9C); p19 "Do not hand this up";
  p20 copyright/back cover.
  Scheme p1 cover; p2-p3 notes; p4 annotation key; p5 Geographical
  Investigation (coursework, not a written-paper task); p6 presentation
  breakdown; p7-p8 Part One table; p9 the 2023 Part Two adjustment rule;
  p10-p22 Q1-Q6; p23 Section 3 divider; p24-p35 Q7-Q12; p36 investigation
  topics; p37 Irish-language bonus marks; p38-p39 blank; p40 back cover.
  Companions: Cavan map extract (Slieve Glah, Lisnananagh Lough, the
  Stradone River, Sweelan Lough); OS legend sheet; oblique aerial
  photograph of Cavan.

Companions. Part One Q6 and Q7 (map, legend) and Q8 (aerial and the
printed sections of it); Part Two 1A, 8B and 11B (map, legend), 7A and 10A
(aerial) were held back before this review because their companions were
not wired. Each now carries the exact official documents it names.

Boundaries follow the published allocation: at Ordinary Level the scheme
prices every printed roman of every A, B and C part, so each roman is its own
task (2B (i) 4m is separate from the 36m choose-two weathering card). Part
One romans are tasks; a matching table under ONE printed instruction stays
one task with a criterion per scheme row, the scheme listing its answers in
the printed row order: Q1 Inner core=B, Outer core=A, Crust=D, Mantle=C; Q2
prints (i) and (ii) in one part-completed table: (i) Limestone=A,
Granite=D (Basalt C and Quartzite B are printed), (ii) Basalt Igneous,
Limestone Sedimentary, Quartzite Metamorphic (Granite Igneous is printed);
Q3 Magma chamber=D, Crater=C, Crust=B, Flowing lava=A; Q4 Drumlin=C,
Levee=E, Interlocking spurs=A, Sea cliff=B, Scree=D; Q5 Warm Temperate
Oceanic=C, Limerick City=A, Sambre Meuse Valley=E, Gaeltacht=D, The
Burren=B; Q10 Ruapehu=C, Adirondack=D, Isles of Scilly=B, Chihuahuan
Desert=A; Part Two 2A (i) C Sea arch, A U-shaped valley, B Meander and (ii)
A Glacial erosion, C Coastal erosion, B River erosion and deposition. A part
whose wording depends on an earlier part ("this developing economy", "named
in part (i) above", "this multinational company", "this city") carries that
earlier printed part in its stem.

Tariffs: an SRP is 3 marks at Ordinary Level; "a+b" lines are one criterion
with partial credit a; graded lines keep their printed grades; sketch items
are "showing 3 (3/1/0) + labelled 2"; 4A items are "named 2 + shown 4
(4/2/0)". Every question totals 10 (Part One) or 100 = 30 + 40 + 30 (Part
Two) as printed.

Wording: the paper wins where the scheme reprints it differently (9A(v)
"Name one example", scheme "Name one other example"); the scheme's 8B(iii)
line reads "One advantage described" against the paper's "disadvantage" and
is shown as printed.
"""

import itertools

from geography_review import (
    Criterion, Lift, Route, SchemeSlice, Task, pool, fixed, slug, srp, steps, sums,
)

YEAR = 2023
LEVEL = 'ordinary'
PAPER_PAGES = {1: 40, 2: 20}
SCHEME_PAGES = 40
QUESTION_TARIFFS = {1: {str(n): 10 for n in range(1, 13)},
                    2: {f'{n}{x}': (40 if x == 'B' else 30)
                        for n in range(1, 13) for x in 'ABC'}}

EXPECTED_SOURCES = {
    'paper1': ('LC005GLP042EV.pdf', 3346821),
    'paper2': ('LC005GLP043EV.pdf', 3033788),
    'scheme': ('LC005GLP000EV.pdf', 2309289),
    'map': ('LC005CLP003EV.pdf', 4959287),
    'legend': ('LC005CLPC00EV.pdf', 836095),
    'aerial': ('LC005CLP004EV.jpg', 5597283),
}

PAGE_REVIEW = {
    'paper1': {1: 'cover', 2: 'instructions', **{p: 'question' for p in range(3, 13)},
               13: 'answerbook instructions', **{p: 'graph-paper answer page' for p in range(14, 18)},
               **{p: 'lined answer page' for p in range(18, 40)}, 40: 'copyright/back cover'},
    'paper2': {1: 'cover', 2: 'Part Two instructions',
               **{p: 'question' for p in (3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17, 18)},
               11: 'section divider', 19: 'do not hand this up', 20: 'copyright/back cover'},
    'scheme': {1: 'cover', 2: 'notes', 3: 'notes', 4: 'annotation key',
               5: 'geographical investigation (coursework)', 6: 'investigation presentation breakdown',
               7: 'Part One table', 8: 'Part One table',
               9: 'Part Two adjustment rule (2023 additional choice)',
               **{p: 'Part Two allocation' for p in range(10, 23)}, 23: 'section divider',
               **{p: 'Part Two allocation' for p in range(24, 36)},
               36: 'investigation topics', 37: 'Irish-language bonus marks',
               38: 'blank', 39: 'blank', 40: 'back cover'},
}

EXPECTED_SELECTION_SCAN = [
    [1, 2, 'attempt any ten'], [1, 2, 'attempt three'], [1, 3, 'attempt any ten'],
    [2, 2, 'attempt three'],
    [2, 4, 'any two'], [2, 4, 'any two'],
    [2, 5, 'one of the following'],
    [2, 6, 'answer (i) or (ii)'], [2, 6, 'any two'], [2, 6, 'any two'], [2, 6, 'one of the following'],
    [2, 7, 'any two'], [2, 7, 'any one'],
    [2, 15, 'one of the following'],
    [2, 18, 'any three'],
]
SELECTION_REVIEW = [
    {'scan': [[1, 2, 'attempt any ten'], [1, 2, 'attempt three'], [1, 3, 'attempt any ten'],
              [2, 2, 'attempt three']],
     'kind': 'exam-attempt-rule',
     'reason': 'Part One any ten of twelve and Part Two three questions from two sections are attempt rules; every question is carded.'},
    {'scan': [[2, 5, 'one of the following']], 'kind': 'closed-choose-one',
     'reason': '2C: one of four printed interactions -> four routes.'},
    {'scan': [[2, 6, 'answer (i) or (ii)']], 'kind': 'closed-route',
     'reason': '3B: (i) or (ii) -> two routes, each with its own scheme allocation.'},
    {'scan': [[2, 6, 'one of the following']], 'kind': 'closed-choose-one',
     'reason': '3C: one of three printed surface processes -> three routes.'},
    {'scan': [[2, 15, 'one of the following']], 'kind': 'closed-choose-one',
     'reason': '9C: one of three printed economic activities -> three routes.'},
    {'scan': [[2, 4, 'any two'], [2, 7, 'any two']], 'kind': 'choose-n-one-card',
     'reason': '2B(ii) any two of three printed types of weathering and 4B any two of three printed headings -> one card each with every printed item (choice is not a route; the scheme marks each chosen item alike).'},
    {'scan': [[2, 4, 'any two'], [2, 6, 'any two'], [2, 6, 'any two'], [2, 7, 'any one'], [2, 18, 'any three']],
     'kind': 'open-response',
     'reason': 'No printed pool: 2B(i) any two factors; 3B(i) any two landforms and 3B(ii) any two mass movement processes (the scheme prices two @ 20m); 4C any one region (the factor box is illustrative, not a choice); 12B(iii) any three problems. 6C "two problems" and 11B "three different rural settlement patterns" are open too; the scheme prices each one.'},
]

P1, P2 = 1, 2
ID = 'geography-2023-ol-'
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


def chosen(items, k):
    return [(combo, ' + '.join(item.rstrip('.') for item in combo),
             '-'.join(slug(item, 34) for item in combo))
            for combo in itertools.combinations(items, k)]


def bullet_routes(prefix, items, k=1, atlas=None):
    return tuple(Route(route_slug, label, ID + prefix + route_slug, True, keep_bullets=combo,
                       atlas=(atlas[combo[0]] if atlas else None))
                 for combo, label, route_slug in chosen(items, k))


PS = (O + 'plate-tectonics',)
RW = (O + 'rocks-weathering-mass-movement',)
SEA = (O + 'the-sea',)
RIVERS = (O + 'rivers',)
GLAC = (O + 'glaciation',)
EV = (O + 'earthquakes-volcanoes',)
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


def part_one_romans(q, page, title, stem, first_legacy, sources, parts):
    """Part One romans. parts: (roman, prompt Lifts, scheme start, scheme end, criteria, topic, atlas)."""
    out = []
    for index, (roman, prompt, start, end, criteria, topic, atlas) in enumerate(parts):
        key = roman.strip('()')
        out.append(T(f'p1-{q}-{key}', P1, q, roman, sum(c.max for c in criteria), page, title,
                     prompt if isinstance(prompt, tuple) else (prompt,), (S(8 if int(q) > 6 else 7, start, end),),
                     criteria, topic, atlas, ID + f'p1-q{q}' + ('' if index == 0 else f'-{key}'),
                     first_legacy and index == 0, sources, stem))
    return out


# ---------------------------------------------------------------- Part One --
Q1S = (L(3, 'Examine the diagram above showing the different layers of the earth', 'following questions.'),)
Q2S = (L(4, 'Examine the photographs above. Complete the table by answering', 'completed for you.'),)
Q3S = (L(5, 'Examine the diagram of a volcano above and answer each of the following questions.'),)
Q6S = (L(7, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper and answer the',
         'following questions.'),)
Q7S = (L(7, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper and answer each',
         'following questions.'),)
Q8S = (L(8, 'Examine the aerial photograph accompanying this paper, and the sections from it below',
         'following questions.'),)
Q9S = (L(9, 'Examine the table above which shows the mean monthly temperatures', 'following questions.'),)
Q10S = (L(10, 'Examine the satellite images above and answer each of the following questions.'),)
Q11S = (L(11, 'Examine the stacked bar chart above', 'following questions.'),)
Q12S = (L(12, 'Examine the weather chart above and answer each of the following questions.'),)

PART_ONE = [
    T('p1-1-i', P1, '1', '(i)', 8, 3, L(3, 'Layers of the Earth'),
      (L(3, '(i) Match each of the letters A, B, C and D with the feature', 'table below.'),),
      (S(7, 'Q.1 (i)', '(ii) · Eurasian'),), rows(['Q.1 (i) · B · 2m', 'A · 2m', 'D · 2m', 'C · 2m']),
      '0-0', PS, ID + 'p1-q1', True, ('page',), Q1S,
      row_labels=(L(3, 'Inner core'), L(3, 'Outer core'), L(3, 'Crust'), L(3, 'Mantle'))),
    T('p1-1-ii', P1, '1', '(ii)', 2, 3, L(3, 'Layers of the Earth'),
      (L(3, '(ii) Which tectonic plate is Ireland part of?', 'Tick (✓) the correct box.'),
       L(3, 'Nazca'), L(3, 'Eurasian')),
      (S(7, '(ii) · Eurasian', 'Q.2 (i)'),), (fixed('Tectonic plate', 2, '(ii) · Eurasian · 2m · Total 10m'),),
      '0-0', PS, ID + 'p1-q1-ii', False, ('page',), Q1S),
    T('p1-2-i', P1, '2', '(i)', 4, 4, L(4, 'Rocks'),
      (L(4, '(i) Match each of the photographs A, B, C and D with the rock type', 'the table below.'),),
      (S(7, 'A Sedimentary', '(B) Metamorphic'),),
      (fixed('Row 1', 2, 'A Sedimentary · 2m+ 2m'), fixed('Row 2', 2, 'D (Igneous) · 2m')),
      '0-1', RW, ID + 'p1-q2', True, ('page',), Q2S,
      row_labels=(L(4, 'Limestone'), L(4, 'Granite'))),
    T('p1-2-ii', P1, '2', '(ii)', 6, 4, L(4, 'Rocks'),
      (L(4, '(ii) State whether each rock type is an igneous, sedimentary or a metamorphic rock.'),),
      (S(7, 'Q.2 (i)', 'D (Igneous)'), S(7, '(B) Metamorphic', 'Q.3 (i)')),
      (fixed('Row 1', 2, 'Q.2 (ii) Igneous · 2m'), fixed('Row 2', 2, 'A Sedimentary · 2m+ 2m'),
       fixed('Row 3', 2, '(B) Metamorphic · 2m')),
      '0-1', RW, ID + 'p1-q2-ii', False, ('page',), Q2S,
      row_labels=(L(4, 'Basalt'), L(4, 'Limestone'), L(4, 'Quartzite'))),
    T('p1-3-i', P1, '3', '(i)', 8, 5, L(5, 'Volcanoes'),
      (L(5, '(i) Match each of the letters A, B, C and D with the feature', 'table below.'),),
      (S(7, 'Q.3 (i)', '(ii) · Dormant'),), rows(['Q.3 (i) · D · 2m', 'C · 2m', 'B · 2m', 'A · 2m']),
      '0-7', EV, ID + 'p1-q3', True, ('page',), Q3S,
      row_labels=(L(5, 'Magma chamber'), L(5, 'Crater'), L(5, 'Crust'), L(5, 'Flowing lava'))),
    T('p1-3-ii', P1, '3', '(ii)', 2, 5, L(5, 'Volcanoes'),
      (L(5, '(ii) Which of the following is the name given to a volcano', 'Tick (✓) the correct box.'),
       L(5, 'Active'), L(5, 'Dormant')),
      (S(7, '(ii) · Dormant', 'Q.4'),), (fixed('Name', 2, '(ii) · Dormant · 2m · Total 10m'),),
      '0-7', EV, ID + 'p1-q3-ii', False, ('page',), Q3S),
    T('p1-4', P1, '4', '', 10, 6, L(6, 'Physical Processes'),
      (L(6, 'Match each of the physical processes below with the feature', 'in the table below.', nth=0),),
      (S(7, 'Q.4', 'Q.5'),), rows(['Q.4 · C · 2m', '=E · 2m', '=A · 2m', '=B · 2m', 'D · 2m · Total 10m']),
      '0-4', RIVERS + SEA + GLAC + RW, ID + 'p1-q4', True, ('page',),
      row_labels=(L(6, 'Drumlin'), L(6, 'Levee'), L(6, 'Interlocking spurs'), L(6, 'Sea cliff'), L(6, 'Scree'))),
    T('p1-5', P1, '5', '', 10, 6, L(6, 'Regions'),
      (L(6, 'Match the type of region with the example of the region', 'in the table below.'),),
      (S(7, 'Q.5', 'Q.6'),), rows(['Q.5 · C · 2m', '=A · 2m', '=E · 2m', '=D · 2m', 'B · 2m · Total 10m']),
      '1-0', IRL + EURO, ID + 'p1-q5', True, ('page',),
      row_labels=(L(6, 'Warm Temperate Oceanic'), L(6, 'Limerick City'), L(6, 'Sambre Meuse Valley'),
                  L(6, 'Gaeltacht'), L(6, 'The Burren'))),
    T('p1-6-i', P1, '6', '(i)', 6, 7, L(7, 'Ordnance Survey Map', nth=0),
      (L(7, '(i) Name the feature shown at each of the following grid references:'),),
      (S(7, 'Q.6 (i)', '(ii) · National'),),
      rows(['Q.6 (i) · 18hole golf course · 2m', 'Holy Well · 2m', 'Garda Station · 2m']),
      '2-6', MAP, ID + 'p1-q6', False, ('map', 'legend'), Q6S,
      row_labels=(L(7, 'H 391 061:'), L(7, 'H 419 066:'), L(7, 'H 503 037:'))),
    T('p1-6-ii', P1, '6', '(ii)', 2, 7, L(7, 'Ordnance Survey Map', nth=0),
      (L(7, '(ii) What does the letter N stand for in relation to the N3 and the N55 roads?'),),
      (S(7, '(ii) · National', '(iii) · Correctly drawn'),),
      (fixed('Meaning of N', 2, '(ii) · National (Primary Road) · 2m'),), '2-6', MAP, ID + 'p1-q6-ii', False,
      ('map', 'legend'), Q6S),
    T('p1-6-iii', P1, '6', '(iii)', 2, 7, L(7, 'Ordnance Survey Map', nth=0),
      (L(7, '(iii) Draw the Ordnance Survey map symbol for Parking in the space below.'),),
      (S(7, '(iii) · Correctly drawn symbol'),),
      (fixed('Symbol', 2, '(iii) · Correctly drawn symbol · 2m'),), '2-6', MAP, ID + 'p1-q6-iii', False,
      ('map', 'legend'), Q6S),
    T('p1-7-i', P1, '7', '(i)', 5, 7, L(7, 'Ordnance Survey Map', nth=1),
      (L(7, '(i) What is the length of the N3', 'Tick (✓) the correct box.'), L(7, '4.2km'), L(7, '3.2km')),
      (S(8, 'Q.7 (i)', '(ii) · 320m'),), (fixed('Length', 5, 'Q.7 (i) · 4.2km · 5m'),),
      '2-6', MAP, ID + 'p1-q7', False, ('map', 'legend'), Q7S),
    T('p1-7-ii', P1, '7', '(ii)', 5, 7, L(7, 'Ordnance Survey Map', nth=1),
      (L(7, '(ii) What is the height of the highest point on the map?', 'Tick (✓) the correct box.'),
       L(7, '218m'), L(7, '320m')),
      (S(8, '(ii) · 320m', 'Q.8'),), (fixed('Height', 5, '(ii) · 320m · 5m'),),
      '2-6', MAP, ID + 'p1-q7-ii', False, ('map', 'legend'), Q7S),
    T('p1-8-i', P1, '8', '(i)', 8, 8, L(8, 'Aerial Photograph'),
      (L(8, '(i) Give the location of each of the sections from the aerial photograph', 'centre foreground, etc.).'),),
      (S(8, 'Q.8 (i)', '(ii) · Oblique'),),
      (fixed('A', 2, 'Q.8 (i) · Right foreground · 2m'), fixed('B', 2, 'Centre middleground · 2m'),
       fixed('C', 2, 'Right centreground · 2m'), fixed('D', 2, 'Left background · 2m')),
      '2-8', AER, ID + 'p1-q8', False, ('page', 'aerial'), Q8S),
    T('p1-8-ii', P1, '8', '(ii)', 2, 8, L(8, 'Aerial Photograph'),
      (L(8, '(ii) Indicate whether the aerial photograph accompanying this paper is a vertical', 'correct box.'),
       L(8, 'Vertical'), L(8, 'Oblique')),
      (S(8, '(ii) · Oblique', 'Q.9'),), (fixed('Type', 2, '(ii) · Oblique · 2m · Total 10m'),),
      '2-8', AER, ID + 'p1-q8-ii', False, ('aerial',), Q8S),
]

PART_ONE += part_one_romans('9', 9, L(9, 'Weather Statistics'), Q9S, True, ('page',), [
    ('(i)', L(9, '(i) What was the mean temperature (°C) for October?'), 'Q.9 (i)', '(ii) · 17.7',
     (fixed('Temperature', 2, 'Q.9 (i) 11.9 (°C) · 2m'),), '2-0', GRAPH + WEATHER),
    ('(ii)', L(9, '(ii) What was the highest mean monthly temperature (°C)?'), '(ii) · 17.7', '(iii) · May',
     (fixed('Temperature', 2, '(ii) · 17.7 (°C) · 2m'),), '2-0', GRAPH + WEATHER),
    ('(iii)', L(9, '(iii) Which month experienced the highest total rainfall?'), '(iii) · May', '(iv) · 5',
     (fixed('Month', 2, '(iii) · May · 2m'),), '2-0', GRAPH + WEATHER),
    ('(iv)', L(9, '(iv) In how many months were the mean temperatures greater than 10°C?'), '(iv) · 5 · 2m',
     '(v) · 233', (fixed('Months', 2, '(iv) · 5 · 2m'),), '2-0', GRAPH + WEATHER),
    ('(v)', L(9, '(v) What was the total rainfall (mm) for January, February and March combined?'), '(v) · 233',
     'Q.10', (fixed('Total rainfall', 2, '(v) · 233 (mm) · 2m · Total 10m'),), '2-0', GRAPH + WEATHER),
])

PART_ONE += [
    T('p1-10-i', P1, '10', '(i)', 8, 10, L(10, 'Satellite Interpretation'),
      (L(10, '(i) Match each of the images A, B, C and D with the description', 'table below.'),),
      (S(8, 'Q.10 (i)', '(ii) · True'),), rows(['Q.10 (i) · C · 2m', '=D · 2m', '=B · 2m', '=A · 2m']),
      '2-8', AER, ID + 'p1-q10', True, ('page',), Q10S,
      row_labels=(L(10, 'Mount Ruapehu volcano, New Zealand'), L(10, 'Autumn in the Adirondack mountains, USA'),
                  L(10, 'Isles of Scilly, off the coast of Cornwall, UK'),
                  L(10, 'Chihuahuan Desert agriculture, Mexico'))),
    T('p1-10-ii', P1, '10', '(ii)', 2, 10, L(10, 'Satellite Interpretation'),
      (L(10, '(ii) Indicate whether the following statement is true or false', 'correct box.'),
       L(10, 'The supply of water to crops to help growth is called irrigation.')),
      (S(8, '(ii) · True', 'Q.11'),), (fixed('True or false', 2, '(ii) · True · 2m · Total 10m'),),
      '2-8', AER, ID + 'p1-q10-ii', False, ('page',), Q10S),
]

PART_ONE += part_one_romans('11', 11, L(11, 'European Union Population'), Q11S, True, ('page',), [
    ('(i)', L(11, '(i) What percentage of the EU population was aged between 0-19 years in 2017?'), 'Q.11 (i)',
     '(ii) · 80 and over', (fixed('Percentage', 2, 'Q.11 (i) 21(%) · 2m'),), '2-0', GRAPH + POP),
    ('(ii)', L(11, '(ii) Which age group had the lowest percentage of population in 2020?'), '(ii) · 80 and over',
     '(iii) · 20-64', (fixed('Age group', 2, '(ii) · 80 and over · 2m'),), '2-0', GRAPH + POP),
    ('(iii)', L(11, '(iii) Which age group is projected to have the highest percentage of population in 2030?'),
     '(iii) · 20-64', '(iv) · 2040', (fixed('Age group', 2, '(iii) · 20-64 · 2m'),), '2-0', GRAPH + POP),
    ('(iv)', L(11, '(iv) In what year is the EU projected to have 9% of its population', 'age group?'),
     '(iv) · 2040', '(v) · 0-19', (fixed('Year', 2, '(iv) · 2040 · 2m'),), '2-0', GRAPH + POP),
    ('(v)', L(11, '(v) State one age group that had no change in percentage between 2017 and 2020.'),
     '(v) · 0-19', 'Q.12', (fixed('Age group', 2, '(v) · 0-19 OR 65-79 · 2m · Total 10m'),), '2-0', GRAPH + POP),
])

PART_ONE += part_one_romans('12', 12, L(12, 'Weather'), Q12S, True, ('page',), [
    ('(i)', L(12, '(i) What does L on the weather chart indicate?'), 'Q.12 (i)', '(ii) · Calm',
     (fixed('Meaning of L', 2, 'Q.12 (i) Low pressure or Depression · 2m'),), '2-7', WEATHER),
    ('(ii)', (L(12, '(ii) In the weather chart above, is the weather over Ireland likely', 'Tick (✓) the correct box.'),
              L(12, 'Wet and windy'), L(12, 'Calm and dry')),
     '(ii) · Calm', '(iii) · 1008', (fixed('Weather', 2, '(ii) · Calm and dry · 2m'),), '2-7', WEATHER),
    ('(iii)', L(12, '(iii) What is the barometric pressure (in millibars/hectopascals) at the point labelled X?'),
     '(iii) · 1008', '(iv) · Correctly', (fixed('Pressure', 2, '(iii) · 1008 (mb) · 2m'),), '2-7', WEATHER),
    ('(iv)', L(12, '(iv) Draw the weather chart symbol for a cold front in the box below.'),
     '(iv) · Correctly drawn symbol', '(v) · Isobars', (fixed('Symbol', 2, '(iv) · Correctly drawn symbol · 2m'),),
     '2-7', WEATHER),
    ('(v)', (L(12, '(v) What is the name for the lines on a weather chart that join places', 'Tick (✓) the correct box.'),
             L(12, 'Isotherms'), L(12, 'Isobars')),
     '(v) · Isobars', None, (fixed('Name', 2, '(v) · Isobars · 2m · Total 10m'),), '2-7', WEATHER),
])


# ---------------------------------------------------------------- Part Two --
def romans(q, page, title, stem, first_id, sources, parts, legacy_first=True):
    """Separately priced romans of one A/B/C part.
    parts: (sub, marks, prompt Lift, scheme slice(s), criteria, topic, atlas[, extra stem Lifts[, row labels]])."""
    out = []
    for index, part in enumerate(parts):
        sub, marks, prompt, scheme, criteria, topic, atlas = part[:7]
        extra = part[7] if len(part) > 7 else ()
        labels = part[8] if len(part) > 8 else ()
        scheme = scheme if isinstance(scheme, tuple) else (scheme,)
        roman = sub.strip('()')
        out.append(T(f'p2-{q.lower()}-{roman}', P2, q, sub, marks, page, title, (prompt,), scheme,
                     criteria, topic, atlas, first_id if index == 0 else f'{first_id}-{roman}',
                     index == 0 and legacy_first, sources, (*stem, *extra), row_labels=labels))
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
             row_labels=(None, None, None, *(b if isinstance(b, Lift) else L(page, b) for b in bullets)))


def two_of(label, count, head, each, lines, unit):
    per = sums(*unit)
    return tuple(Criterion(f'{label} {n}', count, per, 'srp', (head, each, *lines)) for n in (1, 2))


PART_TWO = [
    sketch(3, L(3, 'Ordnance Survey Map'),
           L(3, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper.', 'Sweelan Lough.'),
           10, ID + 'p2-q1a', '2-6', MAP, ('map', 'legend'),
           ('The triangulation pillar at Slieve Glah', 'The entire area of coniferous plantation at H 46 07',
            L(3, 'Lisnananagh Lough', nth=0), 'The course of the Stradone River from Lisnananagh Lough to H 510 068',
            'Sweelan Lough')),
]
PART_TWO += romans('1B', 3, L(3, 'Rocks'), (), ID + 'p2-q1b', (), [
    ('(i)', 6, L(3, '(i) Name two examples of sedimentary rocks.'),
     S(11, 'Two sedimentary rocks named', '(ii) · State two'),
     (fixed('Two sedimentary rocks', 6, 'Two sedimentary rocks named @ 3m each · 6m', (0, 3, 6)),), '0-1', RW),
    ('(ii)', 7, L(3, '(ii) State two different Irish locations where sedimentary rocks are found.'),
     S(11, 'Location 1 · 4m', '(iii) · Describe and explain'),
     (fixed('Location 1', 4, 'Location 1 · 4m'), fixed('Location 2', 3, 'Location 2 · 3m')), '0-1', RW),
    ('(iii)', 27, L(3, '(iii) Describe and explain how sedimentary rocks are formed.'),
     S(11, 'Description/Explanation 9 SRP', 'Total 40m'),
     (srp3('Description/explanation', 9, 'Description/Explanation 9 SRP’s @ 3m each · 27m'),), '0-1', RW),
])
PART_TWO.append(T(
    'p2-1c', P2, '1C', '', 30, 3, L(3, 'Fold Mountains'),
    (L(3, 'With the aid of a diagram(s), describe and explain how fold mountains are formed.'),),
    (S(11, 'Diagram two items', 'Total 30m'),),
    (fixed('Diagram (two items)', 6, 'Diagram two items @ 3m each · 6m', (0, 3, 6)),
     srp3('Description/explanation', 8, 'Description/Explanation 8 SRP’s @ 3m each · 24m')),
    '0-2', RW + PS, ID + 'p2-q1c', True))

Q2AS = (L(4, 'Examine the photographs above and answer each of the following questions.'),)
SURFACE_FORMS = PS_SURFACE
PART_TWO += romans('2A', 4, L(4, 'Landforms and Processes'), Q2AS, ID + 'p2-q2a', ('page',), [
    ('(i)', 9, L(4, '(i) In your answer book, match each of the photographs A, B and C with the landform', 'Meander.'),
     S(12, '• C Sea arch', '(ii) · In your answer book'),
     (fixed('Row 1', 3, ('• C Sea arch', '=3m@0')), fixed('Row 2', 3, ('• A U-shaped valley', '=3m@1')),
      fixed('Row 3', 3, ('• B Meander.', '=3m@2'))), '0-4', SURFACE_FORMS, (),
     (L(4, 'Sea arch'), L(4, 'U-shaped valley'), L(4, 'Meander'))),
    ('(ii)', 9, L(4, '(ii) In your answer book, match each of the photographs A, B and C with the process',
                  'River erosion and deposition.'),
     S(12, '• A Glacial erosion', '(iii) Explain briefly'),
     (fixed('Row 1', 3, ('• A Glacial erosion', '=3m@0')), fixed('Row 2', 3, ('• C Coastal erosion', '=3m@1')),
      fixed('Row 3', 3, ('• B River erosion and deposition.', '=3m@2'))), '0-4', SURFACE_FORMS, (),
     (L(4, 'Glacial erosion'), L(4, 'Coastal erosion'), L(4, 'River erosion and deposition'))),
    ('(iii)', 12, L(4, '(iii) Explain briefly each of the following:', 'Plucking.'),
     S(12, 'Brief explanation 1', 'Total 30m'),
     (srp3('Brief explanation 1', 2, 'Brief explanation 1 = 2SRP’s @ 3m each · 6m'),
      srp3('Brief explanation 2', 2, 'Brief explanation 2 = 2SRP’s @ 3m each · 6m')), '0-4', SEA + GLAC, (),
     (L(4, 'Longshore drift'), L(4, 'Plucking'))),
])

WEATHERING = ('Onion weathering', 'Carbonation', 'Freeze-thaw action.')
PART_TWO += [
    T('p2-2b-i', P2, '2B', '(i)', 4, 4, L(4, 'Weathering'),
      (L(4, '(i) Name any two factors that influence weathering.'),),
      (S(13, 'Two valid factors named', '(ii) · Describe and explain'),),
      (fixed('Two factors', 4, 'Two valid factors named @ 2m each · 4m', (0, 2, 4)),),
      '0-8', RW, ID + 'p2-q2b-i', False),
    T('p2-2b-ii', P2, '2B', '(ii)', 36, 4, L(4, 'Weathering'),
      (L(4, '(ii) Describe and explain any two of the following types of weathering:', 'Freeze-thaw action.'),),
      (S(13, 'Weathering type 1 explained', 'Total 40m'),),
      (srp3('Weathering type 1 explained', 6, 'Weathering type 1 explained 6 SRP’s @ 3m each · 18m'),
       srp3('Weathering type 2 explained', 6, 'Weathering type 2 explained 6 SRP’s @ 3m each · 18m')),
      '0-8', RW, *pool(ID + 'p2-q2b-', WEATHERING, 2)[:1], True, absorbs=pool(ID + 'p2-q2b-', WEATHERING, 2)[1]),
    T('p2-2c', P2, '2C', '', 30, 5, L(5, 'Human Interaction with the Rock Cycle'),
      (L(5, 'Describe and explain how humans interact with the rock cycle', 'Geothermal energy production.'),),
      (S(13, 'Description / explanation 10 SRP', 'Total 30m'),),
      (srp3('Description/explanation', 10, 'Description / explanation 10 SRP’s @ 3m each.'),),
      '0-6', RW, ID + 'p2-q2c-quarrying', True,
      routes=bullet_routes('p2-q2c-', ('Quarrying', 'Mining', 'Oil/Gas exploitation',
                                       'Geothermal energy production.'))),
]

Q3AS = (L(6, 'Examine the article above about an earthquake in Afghanistan in 2022', 'following questions.'),)
PART_TWO += romans('3A', 6, L(6, 'Earthquakes'), Q3AS, ID + 'p2-q3a', ('page',), [
    ('(i)', 3, L(6, '(i) What was the magnitude of the earthquake in Afghanistan?'),
     S(14, '6.1 · 3m', '(ii) · Name the two'), (fixed('Magnitude', 3, '6.1 · 3m'),), '0-7', EV),
    ('(ii)', 6, L(6, '(ii) Name the two tectonic plates mentioned in the article.'),
     S(14, 'Indian plate and Eurasian plate', '(iii) · List three'),
     (fixed('Two tectonic plates', 6, 'Indian plate and Eurasian plate · 3m+3m', (0, 3, 6)),), '0-0', PS + EV),
    ('(iii)', 9, L(6, '(iii) List three effects of earthquakes referred to in the article above.'),
     S(14, 'People killed', '(iv) · Explain briefly'),
     (fixed('Effect 1', 3, 'People killed · 3m'), fixed('Effect 2', 3, 'People injured · 3m'),
      fixed('Effect 3', 3, 'Homes destroyed · 3m')), '0-7', EV),
    ('(iv)', 6, L(6, '(iv) Explain briefly the term epicentre.'),
     S(14, 'Brief explanation two SRP', '(v) · Explain briefly', after='(iv) · Explain briefly'),
     (srp3('Brief explanation', 2, 'Brief explanation two SRP’s @ 3m each · 6m'),), '0-7', EV),
    ('(v)', 6, L(6, '(v) Explain briefly one way to limit the damage that earthquakes can cause.'),
     S(14, 'Brief explanation two SRP', 'Total 30m', after='(v) · Explain briefly'),
     (srp3('Brief explanation', 2, 'Brief explanation two SRP’s @ 3m each · 6m'),), '0-7', EV),
])

SURFACE = ('River processes', 'Coastal processes', 'Mass movement processes.')
PART_TWO += [
    T('p2-3b', P2, '3B', '', 40, 6, L(6, 'Landform Development'),
      (L(6, '(i) Explain, with the aid of diagrams, the formation of any two landforms.'),),
      (S(15, 'Formation of any two landforms @ 20m each.', 'Or'),),
      two_of('Landform', 20, 'Formation of any two landforms @ 20m each.', 'For each landform:',
             ('Landform named · 1m', 'Diagram(s) two aspects @ 2m each · 4m',
              'Formation explained 5 SRP’s @ 3m each · 15m'),
             ((0, 1), (0, 2, 4), steps(15, 3))),
      '0-4', PS_SURFACE, ID + 'p2-q3b-route-i', True,
      routes=(
          Route('route-i', 'Route (i)', ID + 'p2-q3b-route-i', True),
          Route('route-ii', 'Route (ii)', ID + 'p2-q3b-route-ii', True,
                prompt=(L(6, '(ii) Describe and explain any two processes of mass movement.'),),
                scheme=(S(15, 'Any two processes @ 20m each', 'Total 40m'),),
                criteria=two_of('Process', 20, 'Any two processes @ 20m each', 'For each process:',
                                ('Process stated · 2m', 'Description / Explanation 6 SRP’s @ 3m each · 18m'),
                                ((0, 2), steps(18, 3))),
                topic='0-8', atlas=RW),
      )),
    T('p2-3c', P2, '3C', '', 30, 6, L(6, 'Human Interaction with Surface Processes'),
      (L(6, 'Examine how humans interact with one of the following surface processes:', 'Mass movement processes.'),),
      (S(16, 'Interaction identified · 3m', 'Total 30m'),),
      (fixed('Interaction identified', 3, 'Interaction identified · 3m'),
       srp3('Explanation', 9, 'Explanation 9 SRP’s @ 3m each · 27m')),
      '0-6', RIVERS, ID + 'p2-q3c-river-processes', True,
      routes=bullet_routes('p2-q3c-', SURFACE, atlas=dict(zip(SURFACE, (RIVERS, SEA, RW))))),
]

SHOWN = 'Shown · 4m graded (4/2/0)'
NAMED_SHOWN = sums((0, 2), (0, 2, 4))
ACTIVITIES = ('The reasons why tourists are attracted to the region',
              'The importance of manufacturing to the region',
              'The development of transport in the region.')
PART_TWO += [
    T('p2-4a', P2, '4A', '', 30, 7, L(7, 'European Region'),
      (L(7, 'Draw a sketch map of a European region (not in Ireland) that you have studied.', 'in this region.'),),
      (S(17, 'Outline of Region', 'Total 30m'),),
      (fixed('Outline of region', 6, 'Outline of Region · 6m graded (6/4/2/0)', (0, 2, 4, 6)),
       Criterion('River', 6, NAMED_SHOWN, 'exact', ('River: · Named · 2m', f'={SHOWN}@0')),
       Criterion('Town/City 1', 6, NAMED_SHOWN, 'exact', ('Town/City 1: · Named · 2m', f'={SHOWN}@1')),
       Criterion('Town/City 2', 6, NAMED_SHOWN, 'exact', ('Town/City 2: · Named · 2m', f'={SHOWN}@2')),
       Criterion('Relief (upland/lowland)', 6, NAMED_SHOWN, 'exact',
                 ('Relief (upland/lowland): · Named · 2m', f'={SHOWN}@3'))),
      '1-5', EURO, ID + 'p2-q4a', True),
    T('p2-4b', P2, '4B', '', 40, 7, L(7, 'Economic Activities – Irish Region'),
      (L(7, 'Explain the development of any two of the following with reference to an Irish region',
         'The development of transport in the region.'),),
      (S(17, 'Region named · 1m', 'Total 40m'),),
      (fixed('Region named', 1, 'Region named · 1m'),
       srp3('Activity 1 explained', 7, 'Activity 1 explained 7 SRP’s @ 3m each · 21m'),
       srp3('Activity 2 explained', 6, 'Activity 2 explained 6 SRP’s @ 3m each · 18m')),
      '1-4', IRL, *pool(ID + 'p2-q4b-', ACTIVITIES, 2)[:1], True, absorbs=pool(ID + 'p2-q4b-', ACTIVITIES, 2)[1]),
    T('p2-4c', P2, '4C', '', 30, 7, L(7, 'Regions and Culture'),
      (L(7, 'The culture of a region can often be determined by the following factors:'),
       L(7, 'Religion'), L(7, 'Language'), L(7, 'Politics'), L(7, 'Music/Dance'), L(7, 'Sport/Games'),
       L(7, 'Describe and explain the importance of culture in any one region that you have studied.')),
      (S(18, 'Description/explanation 10 SRP', 'Total 30m'),),
      (srp3('Description/explanation', 10, 'Description/explanation 10 SRP’s @ 3m each'),),
      '1-3', IRL + EURO + CONT, ID + 'p2-q4c', True),
]

Q5AS = (L(8, 'Examine the infographic above which shows information about the Irish seafood economy',
          'following questions.'),)
PART_TWO += romans('5A', 8, L(8, 'Fishing in Ireland'), Q5AS, ID + 'p2-q5a', ('page',), [
    ('(i)', 3, L(8, '(i) How many people were employed in the Irish fishing sector in 2021?'),
     S(19, '16,647', '(ii) · What was the value'), (fixed('People employed', 3, '16,647 · 3m'),), '2-0', GRAPH),
    ('(ii)', 3, L(8, '(ii) What was the value (in €million) of seafood imported into Ireland in 2021?'),
     S(19, '281 (€million)', '(iii) · Calculate'), (fixed('Value', 3, '281 (€million) · 3m'),), '2-0', GRAPH),
    ('(iii)', 6, L(8, '(iii) Calculate the combined value of the seafood exports', 'the UK.'),
     S(19, '556 (€million)', '(iv) · Name the two'), (fixed('Combined value', 6, '556 (€million) · 6m'),),
     '2-0', GRAPH),
    ('(iv)', 6, L(8, '(iv) Name the two top selling species of fish in Ireland in 2021.'),
     S(19, 'Cod and salmon', '(v) · Name two fishing'),
     (fixed('Two species', 6, 'Cod and salmon · 3m+3m', (0, 3, 6)),), '2-0', GRAPH),
    ('(v)', 6, L(8, '(v) Name two fishing ports in Ireland.'),
     S(19, 'Two valid fishing ports', '(vi) · Explain briefly'),
     (fixed('Two fishing ports', 6, 'Two valid fishing ports named · 3m+3m', (0, 3, 6)),), '1-4', IRL),
    ('(vi)', 6, L(8, '(vi) Explain briefly one advantage of fishing to the Irish economy.'),
     S(19, 'Brief explanation two SRP', 'Total 30m'),
     (srp3('Brief explanation', 2, 'Brief explanation two SRP’s @ 3m each · 6m'),), '1-4', IRL),
])
Q5BS = (L(8, 'Answer each of the following questions with reference to a European region', 'that you have studied.'),)
PART_TWO += romans('5B', 8, L(8, 'Tourism in a European Region'), Q5BS, ID + 'p2-q5b', (), [
    ('(i)', 4, L(8, '(i) Name two tourist attractions in this region.'),
     S(20, 'Two valid attractions named', '(ii) · Explain the positive'),
     (fixed('Two tourist attractions', 4, 'Two valid attractions named · 2m+2m', (0, 2, 4)),), '1-5', EURO),
    ('(ii)', 18, L(8, '(ii) Explain the positive impacts of tourism in this region.'),
     S(20, 'Explanation 6 SRP', '(iii) · Explain the negative', after='(ii) · Explain the positive'),
     (srp3('Explanation', 6, 'Explanation 6 SRP’s @ 3m each · 18m'),), '1-5', EURO),
    ('(iii)', 18, L(8, '(iii) Explain the negative impacts of tourism in this region.'),
     S(20, 'Explanation 6 SRP', 'Total 40m', after='(iii) · Explain the negative'),
     (srp3('Explanation', 6, 'Explanation 6 SRP’s @ 3m each · 18m'),), '1-5', EURO),
])
PART_TWO.append(T(
    'p2-5c', P2, '5C', '', 30, 9, L(9, 'Urban Growth – Continental / Sub-Continental Region'),
    (L(9, 'Describe and explain the reasons for the growth of an urban area in a', 'that you have studied.'),),
    (S(20, 'Description/explanation 10 SRP', 'Total 30m'),),
    (srp3('Description/explanation', 10, 'Description/explanation 10 SRP’s @ 3m each'),),
    '1-6', CONT, ID + 'p2-q5c', True))

Q6AS = (L(10, 'Examine the chart above with information on life expectancy', 'following questions.'),)
PART_TWO += romans('6A', 10, L(10, 'Life Expectancy in the European Union'), Q6AS, ID + 'p2-q6a', ('page',), [
    ('(i)', 3, L(10, '(i) In which country was the female life expectancy 83.5 years in 2020?'),
     S(21, 'Germany · 3m', '(ii) · In which country'), (fixed('Country', 3, 'Germany · 3m'),), '2-0', GRAPH),
    ('(ii)', 3, L(10, '(ii) In which country was male life expectancy the highest in 2020?'),
     S(21, 'Ireland · 3m', '(iii) · Name two'), (fixed('Country', 3, 'Ireland · 3m'),), '2-0', GRAPH),
    ('(iii)', 6, L(10, '(iii) Name two countries whose female life expectancy is below the EU Average', 'females.'),
     S(21, 'Poland and Bulgaria', '(iv) · Calculate'),
     (fixed('Two countries', 6, 'Poland and Bulgaria · 3m+3m', (0, 3, 6)),), '2-0', GRAPH),
    ('(iv)', 6, L(10, '(iv) Calculate the difference in life expectancy for males', 'the EU Average.'),
     S(21, '7.5 (years)', '(v) · Explain briefly'), (fixed('Difference', 6, '7.5 (years) · 6m'),), '2-0', GRAPH),
    ('(v)', 12, L(10, '(v) Explain briefly two reasons why some countries have higher life expectancies',
                  'other countries.'),
     S(21, 'Reason 1', 'Total 30m'),
     (srp3('Reason 1', 2, 'Reason 1 - Brief explanation two SRP’s @ 3m each · 6m'),
      srp3('Reason 2', 2, 'Reason 2 - Brief explanation two SRP’s @ 3m each · 6m')), '4-0', POP + EURO),
])
Q6BS = (L(10, 'Answer each of the following questions with reference to a Continental / Sub-Continental',
          'that you have studied.'),)
Q6BI = L(10, '(i) Name one primary economic activity that contributes to the economy of this region.')
PART_TWO += romans('6B', 10, L(10, 'Primary Economic Activity in a Continental / Sub-Continental Region'), Q6BS,
                   ID + 'p2-q6b', (), [
    ('(i)', 4, Q6BI, S(22, 'One valid primary economic activity named', '(ii) · Explain the advantages'),
     (fixed('Primary economic activity named', 4, 'One valid primary economic activity named · 4m'),), '1-6', CONT),
    ('(ii)', 27, L(10, '(ii) Explain the advantages that this region has for the development of the primary',
                   'named in part (i) above.'),
     S(22, 'Explanation 9 SRP', '(iii) · Describe one problem'),
     (srp3('Explanation', 9, 'Explanation 9 SRP’s @ 3m each · 27m'),), '1-6', CONT, (Q6BI,)),
    ('(iii)', 9, L(10, '(iii) Describe one problem faced by this primary economic activity in this region.'),
     S(22, 'Description 3 SRP', 'Total 40m'),
     (srp3('Description', 3, 'Description 3 SRP’s @ 3m each · 9m'),), '1-6', CONT, (Q6BI,)),
])
PART_TWO.append(T(
    'p2-6c', P2, '6C', '', 30, 10, L(10, 'Regional Development'),
    (L(10, 'Describe and explain two problems faced by any region that you have studied.'),),
    (S(22, 'Problem 1', 'Total 30m'),),
    (srp3('Problem 1', 5, ('Problem 1', '=Description/Explanation 5 SRP’s @ 3m each 15m@0')),
     srp3('Problem 2', 5, ('Problem 2', '=Description/Explanation 5 SRP’s @ 3m each 15m@1'))),
    '1-0', IRL + EURO + CONT, ID + 'p2-q6c', True))

PART_TWO.append(sketch(
    12, L(12, 'Aerial Photograph'),
    L(12, 'Examine the aerial photograph of Cavan accompanying this paper.', 'Two connecting streets.'),
    24, ID + 'p2-q7a', '2-8', AER, ('aerial',),
    ('A lake', 'A church', 'An area of waste ground in the centre foreground', 'A car park',
     'Two connecting streets.')))
Q7BI = L(12, '(i) Name one example of environmental pollution caused by economic activity.')
PART_TWO += romans('7B', 12, L(12, 'Economic Activity – Environmental Pollution'), (), ID + 'p2-q7b', (), [
    ('(i)', 4, Q7BI, S(25, 'Valid example named · 4m', '(ii) · Explain the causes'),
     (fixed('Example named', 4, 'Valid example named · 4m'),), '3-4', ENV),
    ('(ii)', 24, L(12, '(ii) Explain the causes and effects of this environmental pollution.'),
     S(25, 'Cause identified one SRP', '(iii) · Describe how'),
     (fixed('Cause identified', 3, 'Cause identified one SRP @ 3m each · 3m'),
      fixed('Effect identified', 3, 'Effect identified one S RP @ 3m each · 3m'),
      srp3('Explanation', 6, 'Explanation 6 SRP’s @ 3m each · 18m')), '3-4', ENV, (Q7BI,)),
    ('(iii)', 12, L(12, '(iii) Describe how this environmental pollution could be reduced.'),
     S(25, 'Description 4 SRP', 'Total 40m'),
     (srp3('Description', 4, 'Description 4 SRP’s @ 3m each · 12m'),), '3-4', ENV, (Q7BI,)),
])
Q7CI = L(12, '(i) Name one developing economy that was colonised.')
PART_TWO += romans('7C', 12, L(12, 'Colonialism'), (), ID + 'p2-q7c', (), [
    ('(i)', 3, Q7CI, S(25, 'Valid colonised country', '(ii) · Describe and explain'),
     (fixed('Colonised country', 3, 'Valid colonised country · 3m'),), '3-1', DEV),
    ('(ii)', 27, L(12, '(ii) Describe and explain the impacts of colonialism on this developing economy.'),
     S(25, 'Description / Explanation 9 SRP', 'Total 30m'),
     (srp3('Description/explanation', 9, 'Description / Explanation 9 SRP’s @ 3m each · 27m'),), '3-1', DEV,
     (Q7CI,)),
])

GRAPH_OL = (fixed('Graph paper', 3, 'Graph paper 3m', (0, 3)),
            fixed('Vertical axis labelled / circle', 3, 'Vertical axis labelled/Circle · 3m graded (3/1/0)', (0, 1, 3)),
            fixed('Horizontal axis labelled / centred', 3, 'Horizontal axis labelled/Centred · 3m graded (3/1/0)', (0, 1, 3)),
            fixed('5 items illustrated', 15, '5 items @ 3m each graded (3/1/0) · 15m', sums(*[(0, 1, 3)] * 5)))
Q8AS = (L(13, 'Examine the table above showing the expected years of schooling', 'following questions.'),)
PART_TWO += romans('8A', 13, L(13, 'Economic Development'), Q8AS, ID + 'p2-q8a', ('page',), [
    ('(i)', 24, L(13, '(i) Using graph paper, draw a suitable graph to illustrate this data.'),
     S(26, 'Graph paper 3m', '(ii) · In your answer book'), GRAPH_OL, '2-0', GRAPH),
    ('(ii)', 6, L(13, '(ii) In your answer book, explain briefly one way that an educated workforce',
                  'economy of a country.'),
     S(26, 'Brief explanation 2 SRP', 'Total 30m'),
     (srp3('Brief explanation', 2, 'Brief explanation 2 SRP’s @ 3m each · 6m'),), '3-0', ECON),
])
Q8BS = (L(13, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper.'),
        L(13, 'Imagine you have been given the task', 'the area covered by the map.'))
Q8BI = L(13, '(i) State, using a six-figure grid reference, where you would locate the factory.')
PART_TWO += romans('8B', 13, L(13, 'Ordnance Survey Map'), Q8BS, ID + 'p2-q8b', ('map', 'legend'), [
    ('(i)', 4, Q8BI, S(27, 'Six-figure grid reference', '(ii) · Explain the reasons'),
     (fixed('Six-figure grid reference', 4, 'Six-figure grid reference · 4m graded (4/2/0)', (0, 2, 4)),),
     '2-6', MAP),
    ('(ii)', 27, L(13, '(ii) Explain the reasons why you chose this location.'),
     S(27, 'Reasons explained 9 SRP', '(iii) · Describe one'),
     (srp3('Reasons explained', 9, 'Reasons explained 9 SRP’s @ 3m each · 27m'),), '3-0', ECON + MAP, (Q8BI,)),
    ('(iii)', 9, L(13, '(iii) Describe one disadvantage of locating the factory at this location.'),
     S(27, 'One advantage described', '8C.'),
     (srp3('Description', 3, 'One advantage described 3 SRP’s @ 3m each · 9m'),), '3-0', ECON + MAP, (Q8BI,)),
], legacy_first=False)
PART_TWO.append(T(
    'p2-8c', P2, '8C', '', 30, 13, L(13, 'Ireland and the European Union'),
    (L(13, 'Explain how being a member of the European Union has impacted on the Irish economy.'),),
    (S(27, 'Impact Identified 1 SRP', 'Total 30m'),),
    (fixed('Impact identified', 3, 'Impact Identified 1 SRP · 3m'),
     srp3('Explanation', 9, 'Explanation 9 SRP’s @ 3m each · 27m')),
    '3-3', EU, ID + 'p2-q8c', True))

Q9AS = (L(14, 'Examine the article above about the opening of a solar farm', 'following questions.'),)
PART_TWO += romans('9A', 14, L(14, 'Renewable Energy'), Q9AS, ID + 'p2-q9a', ('page',), [
    ('(i)', 3, L(14, '(i) In which county is this solar farm located?'),
     S(28, 'Wicklow · 3m', '(ii) What is the area'), (fixed('County', 3, 'Wicklow · 3m'),), '3-5', ECON),
    ('(ii)', 3, L(14, '(ii) What is the area of land (in hectares) of Millvale solar farm?'),
     S(28, '25 (hectares)', '(iii) · How many tonnes'), (fixed('Area', 3, '25 (hectares) · 3m'),), '3-5', ECON),
    ('(iii)', 3, L(14, '(iii) How many tonnes of greenhouse gas emissions', 'each year?'),
     S(28, '4,800 (tonnes)', '(iv) · Name two benefits'), (fixed('Tonnes', 3, '4,800 (tonnes) · 3m'),),
     '3-5', ECON),
    ('(iv)', 6, L(14, '(iv) Name two benefits of this solar farm that were stated in the article by Eamon Ryan.'),
     S(28, 'Two valid benefits named', '(v) · Name one'),
     (fixed('Two benefits', 6, 'Two valid benefits named · 3m+3m', (0, 3, 6)),), '3-5', ECON),
    ('(v)', 3, L(14, '(v) Name one example of renewable energy, apart from solar power.'),
     S(28, 'One valid example named', '(vi) · Explain briefly'),
     (fixed('Example', 3, 'One valid example named · 3m'),), '3-5', ECON),
    ('(vi)', 6, L(14, '(vi) Explain briefly what is meant by the term fossil fuels.'),
     S(28, 'Brief explanation two SRP', '(vii) · Explain briefly', after='(vi) · Explain briefly'),
     (srp3('Brief explanation', 2, 'Brief explanation two SRP’s @ 3m each · 6m'),), '3-5', ECON),
    ('(vii)', 6, L(14, '(vii) Explain briefly one disadvantage of renewable energy.'),
     S(28, 'Brief explanation two SRP', 'Total 30m', after='(vii) · Explain briefly'),
     (srp3('Brief explanation', 2, 'Brief explanation two SRP’s @ 3m each · 6m'),), '3-5', ECON),
])
Q9BI = L(14, '(i) Name one multinational company located in Ireland that you have studied and name',
         'it manufactures.')
PART_TWO += romans('9B', 14, L(14, 'Multinational Company'), (), ID + 'p2-q9b', (), [
    ('(i)', 7, Q9BI, S(29, 'Valid MNC named', '(ii) · State where'),
     (fixed('MNC named', 4, 'Valid MNC named · 4m'), fixed('Product named', 3, 'Valid product named · 3m')),
     '3-2', MNC),
    ('(ii)', 24, L(14, '(ii) State where this multinational company is located in Ireland and explain why it set up',
                   'at this location.'),
     S(29, 'Valid location · 3m', '(iii) · Explain one reason'),
     (fixed('Location', 3, 'Valid location · 3m'), srp3('Explanation', 7, 'Explanation 7 SRP’s @ 3m each · 21m')),
     '3-2', MNC, (Q9BI,)),
    ('(iii)', 9, L(14, '(iii) Explain one reason why this multinational company might decide to locate to another',
                   'country.'),
     S(29, 'Explanation 3 SRP', '9C.'),
     (srp3('Explanation', 3, 'Explanation 3 SRP’s @ 3m each · 9m'),), '3-2', MNC, (Q9BI,)),
])
PART_TWO.append(T(
    'p2-9c', P2, '9C', '', 30, 15, L(15, 'Economic Development – Developed Economy'),
    (L(15, 'Describe and explain the development of one of the following', 'Service and footloose industries.'),),
    (S(29, 'Named developed economy', 'Total 30m'),),
    (fixed('Named developed economy', 3, 'Named developed economy · 3m'),
     srp3('Description/explanation', 9, 'Description/explanation 9 SRP’s @ 3m each · 27m')),
    '3-0', ECON, ID + 'p2-q9c-tourism', True,
    routes=bullet_routes('p2-q9c-', ('Tourism', 'Financial services', 'Service and footloose industries.'))))

PART_TWO.append(sketch(
    16, L(16, 'Aerial Photograph'),
    L(16, 'Examine the aerial photograph of Cavan accompanying this paper.', 'in the left background.'),
    30, ID + 'p2-q10a', '2-8', AER + URB, ('aerial',),
    ('A lake', 'A church', 'Tennis courts', 'A roundabout', 'Industrial buildings in the left background.')))
Q10BS = (L(16, 'Migration takes place due to push factors and pull factors.'),)
PART_TWO += romans('10B', 16, L(16, 'Migration – Ireland'), Q10BS, ID + 'p2-q10b', (), [
    ('(i)', 4, L(16, '(i) Name one push factor and one pull factor associated with migration.'),
     S(31, 'Push factor named', '(ii) · Discuss the positive'),
     (fixed('Push factor named', 2, 'Push factor named · 2m'), fixed('Pull factor named', 2, 'Pull factor named · 2m')),
     '4-2', POP),
    ('(ii)', 18, L(16, '(ii) Discuss the positive impacts of migration on Ireland.'),
     S(31, 'Discussion 6 SRP', '(iii) · Discuss the negative', after='(ii) · Discuss the positive'),
     (srp3('Discussion', 6, 'Discussion 6 SRP’s @ 3m each · 18m'),), '4-2', POP),
    ('(iii)', 18, L(16, '(iii) Discuss the negative impacts of migration on Ireland.'),
     S(31, 'Discussion 6 SRP', 'Total 40m', after='(iii) · Discuss the negative'),
     (srp3('Discussion', 6, 'Discussion 6 SRP’s @ 3m each · 18m'),), '4-2', POP),
])
PART_TWO += romans('10C', 16, L(16, 'Traffic Congestion'), (), ID + 'p2-q10c', (), [
    ('(i)', 3, L(16, '(i) Name one example of an urban area where traffic congestion is a problem.'),
     S(31, 'Named example 3m', '(ii) · Describe and explain'),
     (fixed('Urban area named', 3, 'Named example 3m'),), '4-5', URB),
    ('(ii)', 27, L(16, '(ii) Describe and explain the measures that can be taken in urban areas to solve the',
                   'problem of traffic congestion.'),
     S(31, 'Description / Explanation 9 SRP', 'Total 30m'),
     (srp3('Description/explanation', 9, 'Description / Explanation 9 SRP’s @ 3m each · 27m'),), '4-5', URB),
])

Q11AS = (L(17, 'Examine the table above showing the population increase (%) in selected Irish counties',
           'following questions.'),)
PART_TWO += romans('11A', 17, L(17, 'Population Dynamics'), Q11AS, ID + 'p2-q11a', ('page',), [
    ('(i)', 24, L(17, '(i) Using graph paper, draw a suitable graph to illustrate this data.'),
     S(32, 'Graph paper 3m', '(ii) · In your answer book'), GRAPH_OL, '2-0', GRAPH),
    ('(ii)', 6, L(17, '(ii) In your answer book, explain briefly one challenge associated with an increase in',
                  'population.'),
     S(32, 'Brief explanation 2 SRP', 'Total 30m'),
     (srp3('Brief explanation', 2, 'Brief explanation 2 SRP’s @ 3m each · 6m'),), '4-0', POP),
])
Q11BS = (L(17, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper.'),)
Q11BI = L(17, '(i) Name three different rural settlement patterns evident on the Ordnance Survey map',
          'example of each.')
PART_TWO += romans('11B', 17, L(17, 'Rural Settlement Patterns'), Q11BS, ID + 'p2-q11b', ('map', 'legend'), [
    ('(i)', 22, Q11BI, S(33, 'Pattern 1 named:', '(ii) · Explain each'),
     (fixed('Pattern 1 named', 4, 'Pattern 1 named: · 4m'), fixed('Pattern 2 named', 3, 'Pattern 2 named: · 3m'),
      fixed('Pattern 3 named', 3, 'Pattern 3 named: · 3m'),
      fixed('Grid reference 1', 4, 'Grid reference 1: · 4m graded (4/2/0)', (0, 2, 4)),
      fixed('Grid reference 2', 4, 'Grid reference 2: · 4m graded (4/2/0)', (0, 2, 4)),
      fixed('Grid reference 3', 4, 'Grid reference 3: · 4m graded (4/2/0)', (0, 2, 4))), '4-3', URB + MAP),
    ('(ii)', 18, L(17, '(ii) Explain each of the three rural settlement patterns named in part (i) above.'),
     S(33, 'Explanation for each pattern:', 'Total 40m'),
     tuple(srp3(f'Pattern {n}', 2, ('Explanation for each pattern:', f'Pattern {n}: 2 SRP’s @ 3m each · 6m'))
           for n in (1, 2, 3)), '4-3', URB + MAP, (Q11BI,)),
], legacy_first=False)
Q11CI = L(17, '(i) Name one city where urban sprawl has occurred.')
PART_TWO += romans('11C', 17, L(17, 'Urban Sprawl'), (), ID + 'p2-q11c', (), [
    ('(i)', 3, Q11CI, S(33, 'City named · 3m', '(ii) · Explain the reasons'),
     (fixed('City named', 3, 'City named · 3m'),), '4-5', URB),
    ('(ii)', 18, L(17, '(ii) Explain the reasons why urban sprawl has occurred in this city.'),
     S(33, 'Explanation 6 SRP', '(iii) · Describe one solution'),
     (srp3('Explanation', 6, 'Explanation 6 SRP’s @ 3m each · 18m'),), '4-5', URB, (Q11CI,)),
    ('(iii)', 9, L(17, '(iii) Describe one solution to urban sprawl.'),
     S(33, 'Description 3 SRP', 'Total 30m'),
     (srp3('Description', 3, 'Description 3 SRP’s @ 3m each · 9m'),), '4-5', URB, (Q11CI,)),
])

Q12AS = (L(18, 'Examine the article above about Dublin Port and answer each of the following questions.'),)
PART_TWO += romans('12A', 18, L(18, 'Changing Landuse Patterns'), Q12AS, ID + 'p2-q12a', ('page',), [
    ('(i)', 3, L(18, '(i) Who submitted a proposal calling for the relocation of Dublin Port?'),
     S(34, 'The Docklands Business Forum · 3m', '(ii) · In what month'),
     (fixed('Who', 3, 'The Docklands Business Forum · 3m'),), '4-4', URB),
    ('(ii)', 3, L(18, '(ii) In what month during 2022 was this proposal submitted?'),
     S(34, 'February · 3m', '(iii) · How much land'), (fixed('Month', 3, 'February · 3m'),), '4-4', URB),
    ('(iii)', 3, L(18, '(iii) How much land (in hectares) does Dublin Port currently occupy?'),
     S(34, '200 (hectares)', '(iv) · Why did'), (fixed('Land', 3, '200 (hectares) · 3m'),), '4-4', URB),
    ('(iv)', 3, L(18, '(iv) Why did Dublin City Council reject the proposal?'),
     S(34, 'It would violate EU environmental law', '(v) · State two reasons'),
     (fixed('Reason', 3, 'It would violate EU environmental law · 3m'),), '4-4', URB),
    ('(v)', 6, L(18, '(v) State two reasons, mentioned in the article, why Dublin Port will continue',
                 'site for expansion.'),
     S(34, 'The housing crisis and difficulty', '(vi) · Explain briefly'),
     (fixed('Two reasons', 6, 'The housing crisis and difficulty finding office space 3m+3m', (0, 3, 6)),),
     '4-4', URB),
    ('(vi)', 6, L(18, '(vi) Explain briefly what is meant by the term urban redevelopment.'),
     S(34, 'Brief explanation 2 SRP', '(vii) · Explain briefly', after='(vi) · Explain briefly'),
     (srp3('Brief explanation', 2, 'Brief explanation 2 SRP’s @ 3m each · 6m'),), '4-4', URB),
    ('(vii)', 6, L(18, '(vii) Explain briefly one reason why towns/cities develop near ports.'),
     S(34, 'Brief explanation 2 SRP', 'Total 30m', after='(vii) · Explain briefly'),
     (srp3('Brief explanation', 2, 'Brief explanation 2 SRP’s @ 3m each · 6m'),), '4-3', URB),
])
Q12BI = L(18, '(i) Name one city in the developing world that is growing rapidly.')
PART_TWO += romans('12B', 18, L(18, 'Developing World City'), (), ID + 'p2-q12b', (), [
    ('(i)', 4, Q12BI, S(35, 'Developing City named', '(ii) · State three factors'),
     (fixed('Developing world city named', 4, 'Developing City named · 4m'),), '4-5', URB),
    ('(ii)', 9, L(18, '(ii) State three factors that influence the growth of this developing world city.'),
     S(35, 'Factor 1:', '(iii) · Describe and explain'),
     (fixed('Factor 1', 3, 'Factor 1: · 3m'), fixed('Factor 2', 3, 'Factor 2: · 3m'),
      fixed('Factor 3', 3, 'Factor 3: · 3m')), '4-5', URB, (Q12BI,)),
    ('(iii)', 27, L(18, '(iii) Describe and explain any three problems associated with the rapid growth of this',
                    'developing world city.'),
     S(35, 'Description / Explanation 9 SRP', 'Total 40m'),
     (srp3('Description/explanation', 9, 'Description / Explanation 9 SRP’s @ 3m each · 27m'),), '4-5', URB,
     (Q12BI,)),
])
PART_TWO += romans('12C', 18, L(18, 'Overpopulation'), (), ID + 'p2-q12c', (), [
    ('(i)', 6, L(18, '(i) Explain briefly what is meant by the term overpopulation.'),
     S(35, 'Brief explanation 2 SRP', '(ii) · Describe and explain'),
     (srp3('Brief explanation', 2, 'Brief explanation 2 SRP’s @ 3m each · 6m'),), '4-1', POP),
    ('(ii)', 24, L(18, '(ii) Describe and explain the causes and effects of overpopulation',
                   'example(s) that you have studied.'),
     S(35, 'Description / Explanation 8 SRP', 'Total 30m'),
     (srp3('Description/explanation', 8, 'Description / Explanation 8 SRP’s @ 3m each · 24m'),), '4-1', POP),
])

TASKS = [*PART_ONE, *PART_TWO]

ID_CORRECTION_REASON = (
    'The shipped card held every part of a question the scheme prices part by '
    'part. Its id is kept on the first separately priced part; the other parts '
    'are new cards with their own published allocation. The three shipped 2B '
    'cards held the whole 40m part, one per pair of weathering types; the first '
    'pair\'s id now holds 2B(ii) as one card showing all three printed types '
    '(choice is not a route), the other two alias to it, and the separately '
    'priced 2B(i) is a new card.')

# Every 2023 Ordinary card id shipped before this review (52). Each must survive.
LEGACY_IDS = [
    'geography-2023-ol-p1-q1',
    'geography-2023-ol-p1-q2',
    'geography-2023-ol-p1-q3',
    'geography-2023-ol-p1-q4',
    'geography-2023-ol-p1-q5',
    'geography-2023-ol-p1-q9',
    'geography-2023-ol-p1-q10',
    'geography-2023-ol-p1-q11',
    'geography-2023-ol-p1-q12',
    'geography-2023-ol-p2-q1b',
    'geography-2023-ol-p2-q1c',
    'geography-2023-ol-p2-q2a',
    'geography-2023-ol-p2-q2b-onion-weathering-carbonation',
    'geography-2023-ol-p2-q2b-onion-weathering-freeze-thaw-action',
    'geography-2023-ol-p2-q2b-carbonation-freeze-thaw-action',
    'geography-2023-ol-p2-q2c-quarrying',
    'geography-2023-ol-p2-q2c-mining',
    'geography-2023-ol-p2-q2c-oil-gas-exploitation',
    'geography-2023-ol-p2-q2c-geothermal-energy-production',
    'geography-2023-ol-p2-q3a',
    'geography-2023-ol-p2-q3b-route-i',
    'geography-2023-ol-p2-q3b-route-ii',
    'geography-2023-ol-p2-q3c-river-processes',
    'geography-2023-ol-p2-q3c-coastal-processes',
    'geography-2023-ol-p2-q3c-mass-movement-processes',
    'geography-2023-ol-p2-q4a',
    'geography-2023-ol-p2-q4b-the-reasons-why-tourists-are-attra-the-importance-of-manufacturing-to',
    'geography-2023-ol-p2-q4b-the-reasons-why-tourists-are-attra-the-development-of-transport-in-th',
    'geography-2023-ol-p2-q4b-the-importance-of-manufacturing-to-the-development-of-transport-in-th',
    'geography-2023-ol-p2-q4c',
    'geography-2023-ol-p2-q5a',
    'geography-2023-ol-p2-q5b',
    'geography-2023-ol-p2-q5c',
    'geography-2023-ol-p2-q6a',
    'geography-2023-ol-p2-q6b',
    'geography-2023-ol-p2-q6c',
    'geography-2023-ol-p2-q7b',
    'geography-2023-ol-p2-q7c',
    'geography-2023-ol-p2-q8a',
    'geography-2023-ol-p2-q8c',
    'geography-2023-ol-p2-q9a',
    'geography-2023-ol-p2-q9b',
    'geography-2023-ol-p2-q9c-tourism',
    'geography-2023-ol-p2-q9c-financial-services',
    'geography-2023-ol-p2-q9c-service-and-footloose-industries',
    'geography-2023-ol-p2-q10b',
    'geography-2023-ol-p2-q10c',
    'geography-2023-ol-p2-q11a',
    'geography-2023-ol-p2-q11c',
    'geography-2023-ol-p2-q12a',
    'geography-2023-ol-p2-q12b',
    'geography-2023-ol-p2-q12c',
]
