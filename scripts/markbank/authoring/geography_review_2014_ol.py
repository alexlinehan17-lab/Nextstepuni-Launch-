"""Independent review ledger: Leaving Certificate Geography 2014 Ordinary Level.

Sources (English editions, harvested Paper Trail corpus; sizes and SHA-256
pinned in EXPECTED_SOURCES and the generated audit): the examination paper
LC005GLP000EV (28 pages; one booklet printed Part One, answered in it, and
Part Two), marking scheme LC005GLP000EV (36 pages), and the common Dungarvan
companions shared with Higher Level as Paper Trail files them — the 1:50 000
map LC005CLP003EV (eight stacked image strips that render as one page), its
legend LC005CLPC00EV and the aerial photograph LC005CLP004EV (one-page
PDFs). Part One is 100 marks (any ten of twelve @ 10), Part Two 300 (three
questions @ 100).

Visual sweep (every page rendered and read on 2026-10-23):
  Paper p1 cover and examiner's grid; p2-p11 Part One Questions 1-12 (p2
  holds Q1 and Q2, p3 Q3 and Q4; Q5 prints an earthquake block diagram, Q6
  a world plates map, Q7 a county map, Q8 a Dublin climate graph, Q9 four
  photographs, Q10 four satellite images, Q11 an Irish migration graph);
  p12 Part Two instructions; p13 Section 1 divider; p14-p20 Q1-Q6 (p14 and
  p17 open with their dividers; 1A prints a newspaper article, 2A three
  photographs, 5A a map of EU member states by year of entry; p18 holds 5A,
  p19 5B and 5C); p21 Section 2 divider; p22-p27 Electives Q7-Q12 (p22 and
  p25 open with their elective dividers; 7A, 8A, 11A and 12A print tables);
  p28 printed "Blank Page".
  Scheme p1 cover; p2 note on marking schemes; p3 notes; p4 Geographical
  Investigation (coursework); p5-p7 Part One (Q1-Q4, Q5-Q8, Q9-Q12, each
  answer line priced beside it); p8 Part Two instructions and Section 1
  divider; p9-p20 Q1-Q6 (p9 and p15 open with their dividers); p21 Section
  2 divider; p22-p33 Q7-Q12 (p22 and p28 open with their elective
  dividers); p34 investigation topics; p35 Irish-language bonus marks; p36
  back cover. The scheme reprints each Part Two question above its
  allocation; every slice starts at the allocation.
  Companions: Dungarvan 1:50 000 Discovery Series extract (Crohaun 484 m,
  the Colligan River, Dungarvan Harbour); the bilingual OS legend sheet;
  oblique aerial photograph of Dungarvan town and harbour.

The scheme sets the arrowhead bullets of its Part Two instructions (p8) in
Wingdings; geography_review repairs them from the glyph id, and no slice
reaches that page. Its 10C allocation lines open with a stray tab glyph
(U+0003, Cambria) at the bullet position: those slices clip the left margin
(C10) so the guidance reads as printed.

Part One prices every answer line beside it (no pricing heading), so each
separately priced roman is a task. Q3 prints (ii) as one ask ("winter or
spring?" and "State one reason") and the scheme prices it as (ii) Spring and
(iii) Any valid reason: one task, two criteria. Matching tables, in the
printed row order: Q2(i) S 273 009 Mast, X 257 934 Post Office, X 282 952
Golf Course, X 232 903 Parking/Viewpoint; Q3(i) Circus Left Foreground,
Roundabout Left Background, Sandy beach (seven locations accepted); Q4 River
deposition D, Coastal deposition B, River erosion A, Glacial erosion E,
Glacial deposition C; Q5(i) Focus C, Shock waves A, Faultline B; Q6(i)
African B, North American A, Pacific C; Q7(i) Limestone Clare, Basalt
Antrim, Granite Wicklow; Q7(ii) Granite Igneous, Limestone Sedimentary;
Q9(i) A Primary, B Tertiary, C Secondary, D Primary; Q10(i) glacier B, hydro
electric power station D, Niagara Falls A, Trim Castle C (the scheme lists
them Niagara first; each row carries its own line); Q12 Fingal County
Council D, Paris E, Sambre Meuse A, Mezzogiorno B, The Mediterranean C.

Part Two tariffs as printed: twelve parts carry 40 marks (1B, 2B, 3B, 4B,
5C, 6B, 7C, 8B, 9B, 10C, 11C, 12B) and the rest 30. 5C and 6B open by asking
for an Irish region and the scheme prices it outside the romans ("Name an
Irish region · 1 mark", "Name one Irish region · 2 marks"); it is carded
with part (i), as in the 2015 Ordinary ledger. The scheme prints 5C's
second part as "(i)" (the paper's (ii)); the slice is scoped by its own
heading. 8A(i) prices "5 Items @ 3 marks each graded · 15 marks" without
printing the grades, so any mark 0-15 is permitted. 8C(ii)'s two reasons
are printed with a separate subtotal line "18 marks", which ends the slice.
3A's "Two named rivers" is two of the scheme's five items; 9A's and 10A's
"Two connecting streets" is one item of five, as printed.

Printed choices: 3B (i) or (ii), with (i)'s "any one" of three surface
processes, is four routes; 1C, 2C and 9C (one of four, three and four
printed options) are one route per option; 8B "tourism or financial
services" runs through all three romans and is two routes on each; 4B (any
two of four) is a pool, one card.
"""

from geography_review import (
    Criterion, Lift, Route, SchemeSlice, Task, pool, fixed, slug, srp, steps, sums, upto,
)

YEAR = 2014
LEVEL = 'ordinary'
PAPER_PAGES = {1: 28, 2: 28}
SCHEME_PAGES = 36
_FORTY = {'1B', '2B', '3B', '4B', '5C', '6B', '7C', '8B', '9B', '10C', '11C', '12B'}
QUESTION_TARIFFS = {1: {str(n): 10 for n in range(1, 13)},
                    2: {f'{n}{x}': (40 if f'{n}{x}' in _FORTY else 30)
                        for n in range(1, 13) for x in 'ABC'}}

EXPECTED_SOURCES = {
    'paper1': ('LC005GLP000EV.pdf', 2451016),
    'paper2': ('LC005GLP000EV.pdf', 2451016),
    'scheme': ('LC005GLP000EV.pdf', 156491),
    'map': ('LC005CLP003EV.pdf', 4043493),
    'legend': ('LC005CLPC00EV.pdf', 587436),
    'aerial': ('LC005CLP004EV.pdf', 2196383),
}

_PAPER = {1: 'cover and examiner grid', **{p: 'question' for p in range(2, 12)},
          12: 'Part Two instructions', 13: 'section divider', **{p: 'question' for p in range(14, 21)},
          21: 'section divider', **{p: 'question' for p in range(22, 28)}, 28: 'blank page'}
PAGE_REVIEW = {
    # One booklet printed both parts.
    'paper1': _PAPER, 'paper2': _PAPER,
    'scheme': {1: 'cover', 2: 'notes', 3: 'notes', 4: 'geographical investigation (coursework)',
               5: 'Part One table', 6: 'Part One table', 7: 'Part One table',
               8: 'Part Two instructions and section divider',
               **{p: 'Part Two allocation' for p in range(9, 21)}, 21: 'section divider',
               **{p: 'Part Two allocation' for p in range(22, 34)},
               34: 'investigation topics', 35: 'Irish-language bonus marks', 36: 'back cover'},
}

EXPECTED_SELECTION_SCAN = [
    [1, 2, 'attempt ten'], [1, 12, 'attempt three'], [1, 13, 'attempt two'],
    [1, 14, 'attempt one'], [1, 14, 'any one'],
    [1, 15, 'attempt to'], [1, 15, 'one of the following'],
    [1, 16, 'answer (i) or (ii)'], [1, 16, 'any one'], [1, 16, 'any two'], [1, 16, 'any two'],
    [1, 17, 'attempt one'], [1, 17, 'any two'],
    [1, 18, 'any two'],
    [1, 21, 'attempt one'],
    [1, 24, 'choose'], [1, 24, 'any one'],
    [1, 26, 'attempt to'],
]
SELECTION_REVIEW = [
    {'scan': [[1, 2, 'attempt ten'], [1, 12, 'attempt three'], [1, 13, 'attempt two'], [1, 14, 'attempt one'],
              [1, 17, 'attempt one'], [1, 21, 'attempt one']],
     'kind': 'exam-attempt-rule',
     'reason': 'Part One any ten of twelve and Part Two three questions (one of Q1-3, one of Q4-6, one elective) are attempt rules; every question is carded.'},
    {'scan': [[1, 16, 'answer (i) or (ii)'], [1, 16, 'any one']], 'kind': 'closed-route',
     'reason': '3B: (i) or (ii); (i) selects any one of three printed surface processes -> 4 routes, (i)\'s three under one allocation and (ii) under its own. 8B "tourism or financial services" runs through all three romans -> 2 routes on each (no directive word the scan reads; the route text is anchored on the paper).'},
    {'scan': [[1, 14, 'any one'], [1, 15, 'one of the following'], [1, 24, 'choose'], [1, 24, 'any one']],
     'kind': 'closed-choose-one',
     'reason': '1C any one of four printed interactions with the rock cycle -> 4 routes; 2C one of three printed surface processes -> 3 routes; 9C choose any one of four printed European Union policies -> 4 routes.'},
    {'scan': [[1, 17, 'any two']], 'kind': 'choose-n-one-card',
     'reason': '4B any two of four printed activities -> one card with every printed item (choice is not a route).'},
    {'scan': [[1, 16, 'any two'], [1, 16, 'any two'], [1, 18, 'any two']], 'kind': 'open-response',
     'reason': 'No printed pool: 3B(i) any two landforms and 3B(ii) any two mass movement processes (the scheme prices two @ 20 marks); 5A(i) any two founding member states is an answer read from the map. Compulsory lists stay whole: 3A, 4A, 6A, 9A, 10A each item.'},
    {'scan': [[1, 15, 'attempt to'], [1, 26, 'attempt to']], 'kind': 'not-a-selection',
     'reason': '2C "how humans attempt to control" and 11A(v) "ways authorities ... attempt to reduce" describe human activity, not a candidate choice.'},
]

P1, P2 = 1, 2
ID = 'geography-2014-ol-'
O = 'geography-ordinary-'
SRP3 = 3
# 10C's allocation lines open with a stray tab glyph at the bullet position.
C10 = (0.19, 0.3, 1.0, 1.0)


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


def rows(lines, marks=2, labels=None):
    return tuple(fixed(labels[i - 1] if labels else f'Row {i}', marks, line)
                 for i, line in enumerate(lines, 1))


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
BRIEF = 'Brief explanation 2 SRP’s @ 3 marks each · 6 marks'

# ---------------------------------------------------------------- Part One --
PART_ONE = romans('1', P1, 2, L(2, 'Ordnance Survey Map', nth=0),
                  (L(2, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper.', nth=0),),
                  ID + 'p1-q1', ('map', 'legend'), [
    ('(i)', 5, L(2, '(i) What is the height in metres of the highest point on the map?',
                 'Write the correct answer in the box below.'),
     S(5, '(i) · 484m', '(ii) · 6.5'), (fixed('Height', 5, '(i) · 484m · 5 marks'),), '2-6', MAP),
    ('(ii)', 5, L(2, '(ii) Measure the length in kilometres, of the N72 National Primary Road',
                  'Write the correct answer in the box below.'),
     S(5, '(ii) · 6.5', 'Total marks 10'), (fixed('Length', 5, '(ii) · 6.5-8.3 · 5 marks'),), '2-6', MAP),
])
PART_ONE += romans('2', P1, 2, L(2, 'Ordnance Survey Map', nth=1),
                   (L(2, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper.', nth=1),),
                   ID + 'p1-q2', ('map', 'legend'), [
    ('(i)', 8, L(2, '(i) Name the features which can be found at each of the following grid references.'),
     S(5, '(i) · Mast', '(ii) · Golf'),
     rows(['(i) · Mast · 2 marks', 'Post Office · 2 marks', 'Golf Course · 2 marks', 'Parking/Viewpoint · 2 marks']),
     '2-6', MAP, (L(2, 'S 273 009'), L(2, 'X 257 934'), L(2, 'X 282 952'), L(2, 'X 232 903'))),
    ('(ii)', 2, L(2, '(ii) Name two tourist amenities at Wyse’s Point, X 296 922.'),
     S(5, '(ii) · Golf', 'Total marks 10'),
     (fixed('Two tourist amenities', 2, '(ii) · Golf/Camping/Caravan Park · 1+1 mark', (0, 1, 2)),), '2-6', MAP),
])
PART_ONE += romans('3', P1, 3, L(3, 'Aerial Photograph'), (), ID + 'p1-q3', ('aerial',), [
    ('(i)', 6, L(3, '(i) Examine the aerial photograph accompanying this paper.',
                 'write the correct location of each of the following.'),
     S(5, '(i) · Left Foreground', '(ii) · Spring'),
     (fixed('Circus', 2, '(i) · Left Foreground · 2 marks'), fixed('Roundabout', 2, '=Left Background · 2 marks'),
      fixed('Sandy beach', 2, ('Centre Middleground/Right Background/Right Middleground · 2 marks',
                               'Left Middleground/Right Foreground/Left Background/', '=Centre Background'))),
     '2-8', AER, (L(3, 'A Circus'), L(3, 'A Roundabout'), L(3, 'A Sandy beach'))),
    ('(ii)', 4, (L(3, '(ii) Was this aerial photograph taken during winter or spring?'),
                 L(3, 'State one reason for your answer.')),
     S(5, '(ii) · Spring', 'Total marks 10'),
     (fixed('Winter or spring', 2, '(ii) · Spring · 2 marks'), fixed('Reason', 2, '(iii) · Any valid reason · 2 marks')),
     '2-8', AER),
])
PART_ONE.append(T(
    'p1-4', P1, '4', '', 10, 3, L(3, 'Physical Processes'),
    (L(3, 'Match each of the features with the process most associated with its formation, by',
       'in the table below.'),),
    (S(5, 'River deposition · D', 'Total marks 10'),),
    rows(['River deposition · D · 2 marks', 'Coastal deposition · B · 2 marks', 'River erosion · A · 2 marks',
          'Glacial erosion · E · 2 marks', 'Glacial deposition · C · 2 marks']),
    '0-4', PS_SURFACE, ID + 'p1-q4', ('page',),
    row_labels=(L(3, 'River deposition'), L(3, 'Coastal deposition'), L(3, 'River erosion'),
                L(3, 'Glacial erosion'), L(3, 'Glacial deposition'))))
PART_ONE += romans('5', P1, 4, L(4, 'Earthquakes'), (), ID + 'p1-q5', ('page',), [
    ('(i)', 6, L(4, '(i) Match each of the letters A, B and C in the diagram with the correct feature',
                 'in the table below.'),
     S(6, '(i) · Focus', '(ii) · Richter'),
     rows(['(i) · Focus · C · 2 marks', 'Shock Waves · A · 2 marks', 'Faultline · B · 2 marks']), '0-7', EV,
     (L(4, 'Focus'), L(4, 'Shock waves'), L(4, 'Faultline'))),
    ('(ii)', 2, L(4, '(ii) Name a scale used to measure earthquakes.'),
     S(6, '(ii) · Richter', '(iii) · Tsunami'), (fixed('Scale', 2, '(ii) · Richter scale/Mercalli scale · 2 marks'),),
     '0-7', EV),
    ('(iii)', 2, L(4, '(iii) What is the name given to a large wave caused by an earthquake under the water',
                   'in the ocean?'),
     S(6, '(iii) · Tsunami', 'Total marks 10'), (fixed('Name', 2, '(iii) · Tsunami · 2 marks'),), '0-7', EV),
])
PART_ONE += romans('6', P1, 5, L(5, 'Plate Tectonics'),
                   (L(5, 'Examine the map above and answer each of the following questions.'),),
                   ID + 'p1-q6', ('page',), [
    ('(i)', 6, L(5, '(i) Match each of the letters A, B and C on the map with the correct tectonic plate',
                 'in the table below.'),
     S(6, '(i) · African Plate', '(ii) · Eurasian'),
     rows(['(i) · African Plate · B · 2 marks', 'North American Plate · A · 2 marks', 'Pacific Plate · C · 2 marks']),
     '0-0', PS, (L(5, 'African Plate'), L(5, 'North American Plate'), L(5, 'Pacific Plate'))),
    ('(ii)', 2, L(5, '(ii) Name two plates that are colliding together.'),
     S(6, '(ii) · Eurasian', '(iii) · Eurasian'),
     (fixed('Two colliding plates', 2, ('(ii) · Eurasian/Indian OR Cocos/Caribbean', 'Nazca/South American · 2 marks')),),
     '0-0', PS),
    ('(iii)', 2, L(5, '(iii) Name the plate on which Ireland lies.'),
     S(6, '(iii) · Eurasian', 'Total marks 10'), (fixed('Plate', 2, '(iii) · Eurasian · 2 marks'),), '0-0', PS),
])
PART_ONE += romans('7', P1, 6, L(6, 'Irish Rocks'), (), ID + 'p1-q7', ('page',), [
    ('(i)', 6, L(6, '(i) Examine the map and write the correct county in the table below, to match the',
                 'in each case.'),
     S(6, '(i) · Limestone', '(ii) · Granite'),
     rows(['(i) · Limestone · Clare · 2 marks', 'Basalt · Antrim · 2 marks', 'Granite · Wicklow · 2 marks']), '0-1', RW,
     (L(6, 'Limestone', nth=0), L(6, 'Basalt'), L(6, 'Granite', nth=0))),
    ('(ii)', 4, L(6, '(ii) State whether each of the following is an igneous, a sedimentary or a',
                  'metamorphic rock.'),
     S(6, '(ii) · Granite', 'Total marks 10'),
     rows(['(ii) · Granite · Igneous · 2 marks', 'Limestone · Sedimentary · 2 marks']), '0-1', RW,
     (L(6, 'Granite', nth=1), L(6, 'Limestone', nth=1))),
])
PART_ONE += romans('8', P1, 7, L(7, 'Weather Statistics'),
                   (L(7, 'Examine the climate graph above showing average temperature and rainfall levels for',
                      'each of the following questions.'),),
                   ID + 'p1-q8', ('page',), [
    ('(i)', 2, L(7, '(i) Which month had the highest rainfall level?'),
     S(6, '(i) · November', '(ii) · July'), (fixed('Month', 2, '(i) · November · 2 marks'),), '2-0', GRAPH + WEATHER),
    ('(ii)', 2, L(7, '(ii) Which month had the lowest rainfall level?'),
     S(6, '(ii) · July', '(iii) · July'), (fixed('Month', 2, '(ii) · July · 2 marks'),), '2-0', GRAPH + WEATHER),
    ('(iii)', 2, L(7, '(iii) In which month was the highest average temperature recorded?'),
     S(6, '(iii) · July', '(iv) · No'), (fixed('Month', 2, '(iii) · July · 2 marks'),), '2-0', GRAPH + WEATHER),
    ('(iv)', 2, L(7, '(iv) Did the average temperature fall below 0°C in any month?'),
     S(6, '(iv) · No', '(v) · 10.1'), (fixed('Answer', 2, '(iv) · No · 2 marks'),), '2-0', GRAPH + WEATHER),
    ('(v)', 2, L(7, '(v) What was the average temperature range in degrees Celsius (°C)?'),
     S(6, '(v) · 10.1', 'Total marks 10'), (fixed('Temperature range', 2, '(v) · 10.1 · 2 marks'),),
     '2-0', GRAPH + WEATHER),
])
PART_ONE += romans('9', P1, 8, L(8, 'Economic Activity'), (), ID + 'p1-q9', ('page',), [
    ('(i)', 8, L(8, '(i) Examine the photographs and indicate whether each is an example of a Primary,',
                 'in the table below.'),
     S(7, '(i) · A · Primary', '(ii) · Mining'),
     rows(['(i) · A · Primary · 2 marks', 'B · Tertiary · 2 marks', 'C · Secondary · 2 marks', 'D · Primary · 2 marks'],
          labels=('Photograph A', 'Photograph B', 'Photograph C', 'Photograph D')), '3-0', ECON),
    ('(ii)', 2, L(8, '(ii) Name one primary economic activity NOT shown in the photographs above.'),
     S(7, '(ii) · Mining', 'Total marks 10'), (fixed('Primary activity', 2, '(ii) · Mining or Fishing · 2 marks'),),
     '3-0', ECON),
])
PART_ONE += romans('10', P1, 9, L(9, 'Satellite Image Interpretation'), (), ID + 'p1-q10', ('page',), [
    ('(i)', 8, L(9, '(i) Match each satellite image with the most suitable description, by writing the',
                 'in the table below.'),
     S(7, '(i) · Niagara', '(ii) · Use named'),
     rows(['A flowing glacier in Switzerland · B · 2 marks', 'Hydro Electric Power Station · D · 2 marks',
           '(i) · Niagara Falls, Canada · A · 2 marks', 'Trim Castle, Co Meath · C · 2 marks']), '2-8', AER,
     (L(9, 'A flowing glacier in Switzerland'), L(9, 'Hydro electric power station'), L(9, 'Niagara Falls, Canada'),
      L(9, 'Trim Castle, Co. Meath'))),
    ('(ii)', 2, L(9, '(ii) State one use of satellite images.'),
     S(7, '(ii) · Use named', 'Total marks 10'), (fixed('Use', 2, '(ii) · Use named · 2 marks'),), '2-8', AER),
])
PART_ONE += romans('11', P1, 10, L(10, 'Graphical Interpretation'),
                   (L(10, 'Examine the graph above and indicate whether each of the following statements is true or',
                      'circling the correct option in each case.'),),
                   ID + 'p1-q11', ('page',), [
    ('(i)', 2, L(10, '(i) Immigration was at its highest level in 2005.'),
     S(7, '(i) · False', '(ii) · False'), (fixed('True or false', 2, '(i) · False · 2 marks'),), '2-0', GRAPH + POP),
    ('(ii)', 2, L(10, '(ii) Emigration and immigration levels were equal in 2003.'),
     S(7, '(ii) · False', '(iii) · True'), (fixed('True or false', 2, '(ii) · False · 2 marks'),), '2-0', GRAPH + POP),
    ('(iii)', 2, L(10, '(iii) Net migration was at its highest level in 2007.'),
     S(7, '(iii) · True', '(iv) · True'), (fixed('True or false', 2, '(iii) · True · 2 marks'),), '2-0', GRAPH + POP),
    ('(iv)', 2, L(10, '(iv) Immigration is the movement of people into a country.'),
     S(7, '(iv) · True', '(v) · True'), (fixed('True or false', 2, '(iv) · True · 2 marks'),), '4-2', POP),
    ('(v)', 2, L(10, '(v) Net migration is the difference between immigration and', 'emigration.'),
     S(7, '(v) · True', 'Total marks 10'), (fixed('True or false', 2, '(v) · True · 2 marks'),), '4-2', POP),
])
PART_ONE.append(T(
    'p1-12', P1, '12', '', 10, 11, L(11, 'Regions'),
    (L(11, 'Match the description of a region with the example most associated with it, by writing',
       'in the table below.'),),
    (S(7, '(i) · Fingal', 'Total marks 10'),),
    rows(['(i) · Fingal County Council · D · 2 marks', '(ii) · Paris · E · 2 marks', '(iii) · The Sambre Meuse · A · 2 marks',
          '(iv) · Mezzogiorno, Southern Italy · B · 2 marks', '(v) · The Mediterranean · C · 2 marks']),
    '1-0', IRL + EURO, ID + 'p1-q12', ('page',),
    row_labels=(L(11, 'Fingal County Council'), L(11, 'Paris'), L(11, 'Sambre Meuse'),
                L(11, 'Mezzogiorno, Southern Italy'), L(11, 'The Mediterranean'))))


# ---------------------------------------------------------------- Part Two --
OUTLINE = (fixed('Limits/frame', 1, ('Sketch:', 'Limits/Frame · 1 mark')),
           fixed('Proportions', 2, 'Proportions · 2 marks graded (2/0)', (0, 2)),
           fixed('Overall impression', 2, ('Overall Impression · 2 marks graded (2/1/0)', '5 marks total'), (0, 1, 2)))


def aerial_sketch(q, page, prompt, scheme_page, topic, atlas, labels):
    """An aerial-photograph sketch: a 5-mark outline and five items (shown 3/1/0, named 2)."""
    item = sums((0, 1, 3), (0, 2))
    return T(f'p2-{q.lower()}', P2, q, '', 30, page, L(page, 'Aerial Photograph'), (prompt,),
             (S(scheme_page, 'Sketch:', 'Total marks 30'),),
             (*OUTLINE, *(Criterion(f'Item {n}', 5, item, 'exact',
                                    ('Five items shown and named as follows:', 'Showing · 3 marks graded (3/1/0)',
                                     'Naming · 2 marks'))
                          for n in range(1, 6))),
             topic, atlas, ID + f'p2-q{q.lower()}', ('aerial',),
             row_labels=(None, None, None, *(L(page, b) for b in labels)))


def two_of(label, count, head, each, lines, unit):
    per = sums(*unit)
    return tuple(Criterion(f'{label} {n}', count, per, 'srp', (head, each, *lines)) for n in (1, 2))


SHOWN = 'Shown · 4 marks graded (4/2/0)'
NAMED_SHOWN = sums((0, 2), (0, 2, 4))
ROCK = ('Quarrying', 'Mining', 'Oil/Gas exploitation', 'Geothermal energy production.')
SURFACE = ('River processes', 'Coastal processes', 'Mass movement.')
ACTIVITIES_4B = ('The importance of transport to this region', 'The reasons why tourists are attracted to this region',
                 'The type of farming practised in this region',
                 'The reasons for the development of industry in this region.')
POLICIES = ('Common Agricultural Policy', 'Common Fisheries Policy', 'Regional Development Funds', 'Social Funding.')

Q1AS = (L(14, 'Read the newspaper article above and answer each of the following questions.'),)
PART_TWO = romans('1A', P2, 14, L(14, 'Earthquakes'), Q1AS, ID + 'p2-q1a', ('page',), [
    ('(i)', 6, L(14, '(i) What direction from Dublin was the epicentre of the earthquake', 'from Dublin?'),
     S(9, 'Southeast of Dublin', '(ii) · Name two'),
     (fixed('Direction', 3, 'Southeast of Dublin · 3 marks'), fixed('Distance', 3, '97 km · 3 marks')), '0-7', EV),
    ('(ii)', 6, L(14, '(ii) Name two locations in Ireland where the earthquake was felt.'),
     S(9, 'Any two named locations', '(iii) · What is the term'),
     (fixed('Two locations', 6, 'Any two named locations @ 3 marks each · 6 marks', (0, 3, 6)),), '0-7', EV),
    ('(iii)', 6, L(14, '(iii) What is the term given to the smaller tremors which follow the main earthquake?'),
     S(9, 'Aftershocks', '(iv) · State two'), (fixed('Term', 6, 'Aftershocks · 6 marks'),), '0-7', EV),
    ('(iv)', 6, L(14, '(iv) State two effects of earthquakes.'),
     S(9, 'Any two effects stated', '(v) · Explain briefly'),
     (fixed('Two effects', 6, 'Any two effects stated · @ 3 marks each · 6 marks', (0, 3, 6)),), '0-7', EV),
    ('(v)', 6, L(14, '(v) Explain briefly why Ireland has not experienced major earthquakes.'),
     S(9, 'Brief explanation 2 SRP', 'Total marks 30'), (srp3('Brief explanation', 2, BRIEF),), '0-7', EV + PS),
])
PART_TWO += romans('1B', P2, 14, L(14, 'Volcanoes'), (), ID + 'p2-q1b', (), [
    ('(i)', 4, L(14, '(i) Name two examples of volcanoes.'),
     S(10, 'Two examples @ 2 marks', '(ii) · Describe the negative'),
     (fixed('Two examples', 4, 'Two examples @ 2 marks each · 4 marks', (0, 2, 4)),), '0-7', EV),
    ('(ii)', 18, L(14, '(ii) Describe the negative effects of volcanoes.'),
     S(10, '6 SRP', '(iii) · Describe the positive', None, '(ii) · Describe the negative'),
     (srp3('Description', 6, '6 SRP’s @ 3 marks each · 18 marks'),), '0-7', EV),
    ('(iii)', 18, L(14, '(iii) Describe the positive effects of volcanoes.'),
     S(10, '6 SRP', 'Total marks 40', None, '(iii) · Describe the positive'),
     (srp3('Description', 6, '6 SRP’s @ 3 marks each · 18 marks'),), '0-7', EV),
])
PART_TWO.append(T(
    'p2-1c', P2, '1C', '', 30, 14, L(14, 'Human Interaction with the Rock Cycle'),
    (L(14, 'Describe any one of the following examples of human interaction with the rock cycle:',
       'Geothermal energy production.'),),
    (S(10, '10 SRP', 'Total marks 30'),),
    (srp3('Description', 10, '10 SRP’s @ 3 marks each · 30 marks'),),
    '0-6', RW, ID + 'p2-q1c-quarrying', routes=bullet_routes('p2-q1c-', ROCK)))

Q2AS = (L(15, 'Examine the photographs above and answer each of the following questions.'),)
PART_TWO += romans('2A', P2, 15, L(15, 'Surface Processes'), Q2AS, ID + 'p2-q2a', ('page',), [
    ('(i)', 12, L(15, '(i) In your answer book, match each of photographs A, B and C with the term best',
                  'Waterfall.'),
     S(11, 'Scree · B', '(ii) · Process named'),
     rows(['Scree · B · 4 marks', 'U-Shaped Valley · C · 4 marks', 'Waterfall · A · 4 marks'], 4),
     '0-4', RW + GLAC + RIVERS, (L(15, 'Scree'), L(15, 'U-shaped valley'), L(15, 'Waterfall'))),
    ('(ii)', 12, L(15, '(ii) State which process, erosion or weathering, is most associated with the features',
                   'photographs A, B and C.'),
     S(11, 'A · Erosion', '(iii) · Explain briefly'),
     rows(['A · Erosion · 4 marks', 'B · Weathering · 4 marks', 'C · Erosion · 4 marks'], 4,
          ('Photograph A', 'Photograph B', 'Photograph C')), '0-4', RW + GLAC + RIVERS),
    ('(iii)', 6, L(15, '(iii) Explain briefly what is meant by the term weathering.'),
     S(11, 'Brief explanation 2 SRP', 'Total marks 30'),
     (srp3('Brief explanation', 2, 'Brief explanation 2 SRP’s @ 3 marks each'),), '0-8', RW),
])
KARST_FEATURE = (fixed('Diagram', 3, 'Diagram · 3 marks graded (3/1/0)', (0, 1, 3)),
                 srp3('Explanation', 5, ('Explanation:', '5 SRPs @ 3 marks each · 15 marks')))
PART_TWO += romans('2B', P2, 15, L(15, 'Karst Landscapes'), (), ID + 'p2-q2b', (), [
    ('(i)', 2, L(15, '(i) Name one example of a karst landscape that you have studied.'),
     S(11, 'Landscape named', '(ii) · Explain, with the aid'),
     (fixed('Landscape named', 2, 'Landscape named · 2 marks'),), '0-3', KARST),
    ('(ii)', 19, L(15, '(ii) Explain, with the aid of a diagram, how one surface feature in a karst landscape',
                   'is formed.'),
     S(11, 'Surface Feature named', '(iii) · Explain, with the aid'),
     (fixed('Surface feature named', 1, 'Surface Feature named · 1 mark'), *KARST_FEATURE), '0-3', KARST),
    ('(iii)', 19, L(15, '(iii) Explain, with the aid of a diagram, how one underground feature in a karst',
                    'landscape is formed.'),
     S(11, 'Underground Feature named', 'Total marks 40'),
     (fixed('Underground feature named', 1, 'Underground Feature named · 1 mark'), *KARST_FEATURE), '0-3', KARST),
])
PART_TWO.append(T(
    'p2-2c', P2, '2C', '', 30, 15, L(15, 'Human Interaction'),
    (L(15, 'Describe and explain how humans attempt to control one of the following surface', 'Mass movement.'),),
    (S(12, 'Control identified', 'Total marks 30'),),
    (fixed('Control identified', 3, 'Control identified · 3 marks'),
     srp3('Description and explanation', 9, ('Description and explanation:', '9 SRP’s @ 3 marks each · 27 marks'))),
    '0-6', RIVERS, ID + 'p2-q2c-river-processes',
    routes=bullet_routes('p2-q2c-', SURFACE, atlas=dict(zip(SURFACE, (RIVERS, SEA, RW))))))

PART_TWO.append(T(
    'p2-3a', P2, '3A', '', 30, 16, L(16, 'Ordnance Survey Map'),
    (L(16, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper.',
       'An area of coniferous plantation.'),),
    (S(13, 'Sketch:', 'Total marks 30'),),
    (*OUTLINE,
     Criterion('Item 1', 5, sums((0, 1, 3), (0, 2)), 'exact',
               ('Five items shown and named as follows:', 'An area of land over 300 metres · Showing',
                '=Named · 2 marks@0')),
     *(Criterion(f'Item {n}', 5, sums((0, 1, 2, 3), (0, 2)), 'exact',
                 ('Five items shown and named as follows:', 'All other items · Showing', '=Named · 2 marks@1'))
       for n in range(2, 6))),
    '2-6', MAP + RIVERS, ID + 'p2-q3a', ('map', 'legend'),
    row_labels=(None, None, None, L(16, 'An area of land above 300 metres'), L(16, 'Two named rivers'),
                L(16, 'Two named rivers'), L(16, 'The built up area of Dungarvan'),
                L(16, 'An area of coniferous plantation.'))))
LANDFORM_LINES = ('Formation by processes explained @ · 20 marks', 'Landform named · 1 mark', 'Diagram:',
                  'Two items · @ 2 marks each · 4 marks', 'Formation of landform explained:',
                  '5 SRP’s @ 3 marks each · 15 marks')
Q3B_I = (L(16, '(i) Select any one of the following surface processes:', 'Glacial processes.'),
         L(16, 'Explain, with the aid of diagrams, the formation of any two landforms', 'from your selected process.'))
PART_TWO += [
    T('p2-3b', P2, '3B', '', 40, 16, L(16, 'Surface Processes'), Q3B_I,
      (S(14, 'Formation of any two landforms', 'OR'),),
      two_of('Landform', 20, 'Formation of any two landforms @ 20 marks each · 40 marks', 'For each landform:',
             LANDFORM_LINES, ((0, 1), (0, 2, 4), steps(15, 3))),
      '0-10', SEA, ID + 'p2-q3b-route-i-coastal-processes',
      routes=(
          Route('route-i-coastal-processes', 'Route (i) · Coastal processes',
                ID + 'p2-q3b-route-i-coastal-processes', False, keep_bullets=('Coastal processes',),
                topic='0-10', atlas=SEA),
          Route('route-i-river-processes', 'Route (i) · River processes',
                ID + 'p2-q3b-route-i-river-processes', False, keep_bullets=('River processes',),
                topic='0-9', atlas=RIVERS),
          Route('route-i-glacial-processes', 'Route (i) · Glacial processes',
                ID + 'p2-q3b-route-i-glacial-processes', False, keep_bullets=('Glacial processes.',),
                topic='0-11', atlas=GLAC),
          Route('route-ii', 'Route (ii)', ID + 'p2-q3b-route-ii', False,
                prompt=(L(16, '(ii) Describe and explain any two processes of mass movement.'),),
                scheme=(S(14, 'Any two processes @ 20', 'Total marks 40'),),
                criteria=two_of('Process', 20, 'Any two processes @ 20 marks each · 40 marks', 'For each:',
                                ('Process stated · 2 marks', '6 SRP’s @ 3 marks each · 18 marks'),
                                ((0, 2), steps(18, 3))),
                topic='0-8', atlas=RW),
      )),
    T('p2-3c', P2, '3C', '', 30, 16, L(16, 'Plate Tectonics'),
      (L(16, 'Describe and explain what happens at plate boundaries.'),),
      (S(14, 'Description and explanation:', 'Total marks 30'),),
      (srp3('Description and explanation', 10, ('Description and explanation:', '10 SRP’s @ 3 marks each · 30 marks')),),
      '0-0', PS, ID + 'p2-q3c'),
]

PART_TWO += [
    T('p2-4a', P2, '4A', '', 30, 17, L(17, 'Continental / Sub-Continental Region'),
      (L(17, 'Draw a sketch map of a Continental / Sub-Continental region (not in Europe) that you',
         'Two named towns or cities.'),),
      (S(15, 'Sketch Map:', 'Total marks 30'),),
      (fixed('Outline of region', 6, ('Sketch Map:', 'Outline of Region · 6 marks graded (6/4/2/0)'), (0, 2, 4, 6)),
       Criterion('Area of relief (upland/lowland)', 6, NAMED_SHOWN, 'exact',
                 ('Upland/Lowland · Named · 2 marks', f'={SHOWN}@0')),
       Criterion('River', 6, NAMED_SHOWN, 'exact', ('One named river · Named · 2 marks', f'={SHOWN}@1')),
       Criterion('Town/City 1', 6, NAMED_SHOWN, 'exact', ('Town/City 1 · Named · 2 marks', f'={SHOWN}@2')),
       Criterion('Town/City 2', 6, NAMED_SHOWN, 'exact', ('Town/City 2 · Named · 2 marks', f'={SHOWN}@3'))),
      '1-6', CONT, ID + 'p2-q4a'),
    T('p2-4b', P2, '4B', '', 40, 17, L(17, 'Economic Activity in a European Region'),
      (L(17, 'Name a European region (not in Ireland) that you have studied and explain any two of',
         'development of industry in this region.'),),
      (S(16, 'Naming the region', 'Total marks 40'),),
      (fixed('Region named', 1, 'Naming the region · 1 mark'),
       srp3('Activity 1 explained', 7, ('Activity 1 explained:', '7 SRP’s @ 3 marks each · 21 marks')),
       srp3('Activity 2 explained', 6, ('Activity 2 explained:', '6 SRP’s @ 3 marks each · 18 marks'))),
      '1-5', EURO, ID + 'p2-q4b', absorbs=pool(ID + 'p2-q4b-', ACTIVITIES_4B, 2)[1]),
    T('p2-4c', P2, '4C', '', 30, 17, L(17, 'Urban Growth in Ireland'),
      (L(17, 'Describe and explain reasons for the growth of any Irish urban area that you have', 'studied.'),),
      (S(16, 'Naming an urban area', 'Total marks 30'),),
      (fixed('Urban area named', 3, 'Naming an urban area · 3 marks'),
       srp3('Description and explanation', 9, ('Description and Explanation:', '9 SRP’s @ 3 marks each · 27 marks'))),
      '1-1', IRL + URB, ID + 'p2-q4c'),
]
Q5AS = (L(18, 'Examine the map above showing the member states of the European Union and answer',
          'each of the following questions.'),)
BRIEF2 = ('Brief explanation:', '2 SRP’s @ 3 marks each · 6 marks')
PART_TWO += romans('5A', P2, 18, L(18, 'European Union', nth=0), Q5AS, ID + 'p2-q5a', ('page',), [
    ('(i)', 6, L(18, '(i) Name any two of the founding member states.'),
     S(17, 'Any two founding', '(ii) · In what year'),
     (fixed('Two founding member states', 6, 'Any two founding countries named @ 3 marks each · 6 marks', (0, 3, 6)),),
     '3-3', EU + EURO),
    ('(ii)', 6, L(18, '(ii) In what year did Ireland join the European Union and name one other country',
                  'that joined in the same year?'),
     S(17, '1973', '(iii) · Name the country'),
     (fixed('Year', 3, '1973 · 3 marks'), fixed('Other country', 3, 'United Kingdom/Denmark · 3 marks')),
     '3-3', EU + EURO),
    ('(iii)', 6, L(18, '(iii) Name the country labelled X, that joined the European Union in 2013.'),
     S(17, 'Croatia', '(iv) · Explain'), (fixed('Country X', 6, 'Croatia · 6 marks'),), '3-3', EU + EURO),
    ('(iv)', 6, L(18, '(iv) Explain briefly one advantage for member states of the enlargement of the',
                  'European Union.'),
     S(17, 'Brief explanation:', '(v) · Explain', None, '(iv) · Explain'),
     (srp3('Brief explanation', 2, BRIEF2),), '1-5', EURO + EU),
    ('(v)', 6, L(18, '(v) Explain briefly one disadvantage for member states of the enlargement of the',
                 'European Union.'),
     S(17, 'Brief explanation:', 'Total marks 30', None, '(v) · Explain'),
     (srp3('Brief explanation', 2, BRIEF2),), '1-5', EURO + EU),
])
PART_TWO.append(T(
    'p2-5b', P2, '5B', '', 30, 19, L(19, 'Secondary Economic Activity – Continental / Sub-Continental Region'),
    (L(19, 'Describe and explain the development of manufacturing industry in a', 'that you have studied.'),),
    (S(17, 'Naming the region', 'Total marks 30'),),
    (fixed('Region named', 3, 'Naming the region · 3 marks'),
     srp3('Description and explanation', 9, ('Description/Explanation:', '9 SRP’s @ 3 marks each · 27 marks'))),
    '1-6', CONT, ID + 'p2-q5b'))
Q5CS = (L(19, 'Name one Irish region that you have studied and answer each of the following questions.'),)
PART_TWO += romans('5C', P2, 19, L(19, 'Tourism in an Irish Region'), Q5CS, ID + 'p2-q5c', (), [
    ('(i)', 7, L(19, '(i) Name two tourist attractions in this region.'),
     (S(18, 'Name an Irish region', '(i) · Name two'), S(18, 'Two tourist attractions', '(i) · Explain the positive')),
     (fixed('Region named', 1, 'Name an Irish region · 1 mark'),
      fixed('Two tourist attractions', 6, 'Two tourist attractions named @ 3 marks each · 6 marks', (0, 3, 6))),
     '1-4', IRL),
    ('(ii)', 18, L(19, '(ii) Explain the positive impacts of tourism in this region.'),
     S(18, 'Explanation:', '(iii) Explain', None, '(i) · Explain the positive'),
     (srp3('Explanation', 6, ('Explanation:', '6 SRP’s @ 3 marks each 18 marks')),), '1-4', IRL),
    ('(iii)', 15, L(19, '(iii) Explain the negative impacts of tourism in this region.'),
     S(18, 'Explanation:', 'Total marks 40', None, '(iii) Explain the negative'),
     (srp3('Explanation', 5, ('Explanation:', '5 SRP’s @ 3 marks each · 15 marks')),), '1-4', IRL),
])
PART_TWO.append(T(
    'p2-6a', P2, '6A', '', 30, 20, L(20, 'European Region'),
    (L(20, 'Draw a sketch map of a European region (not in Ireland) that you have studied.',
       '(upland or lowland).'),),
    (S(19, 'Sketch map of region outline', 'Total marks 30'),),
    (fixed('Outline of region', 6, 'Sketch map of region outline · 6 marks graded (6/4/2/0)', (0, 2, 4, 6)),
     Criterion('Town/City 1', 6, NAMED_SHOWN, 'exact',
               ('Show and name 4 items @ 6 marks each', 'Town/City 1 · Named · 2 marks', f'={SHOWN}@0')),
     Criterion('Town/City 2', 6, NAMED_SHOWN, 'exact', ('Town/City 2 · Named · 2 marks', f'={SHOWN}@1')),
     Criterion('River', 6, NAMED_SHOWN, 'exact', ('Named River · Named · 2 marks', f'={SHOWN}@2')),
     Criterion('Area of relief', 6, NAMED_SHOWN, 'exact', ('Relief area · Named · 2 marks', f'={SHOWN}@3'))),
    '1-5', EURO, ID + 'p2-q6a'))
Q6BS = (L(20, 'Name one Irish region that you have studied and answer each of the following questions.'),)
PART_TWO += romans('6B', P2, 20, L(20, 'Agriculture in an Irish Region'), Q6BS, ID + 'p2-q6b', (), [
    ('(i)', 4, L(20, '(i) Name two types of agriculture practised in this region.'),
     (S(19, 'Name one Irish region', '(i) · Name two'), S(19, 'Any two types named', '(ii) · Explain the advantages')),
     (fixed('Region named', 2, 'Name one Irish region · 2 marks'),
      fixed('Two types of agriculture', 2, 'Any two types named @ 1 mark each · 2 marks', (0, 1, 2))), '1-4', IRL),
    ('(ii)', 18, L(20, '(ii) Explain the advantages that this region has for the development of agriculture.'),
     S(19, 'Advantages explained:', '(iii) · Describe'),
     (srp3('Advantages explained', 6, ('Advantages explained:', '6 SRP’s @ 3 marks each · 18 marks')),), '1-4', IRL),
    ('(iii)', 18, L(20, '(iii) Describe the challenges faced by agriculture in this region.'),
     S(19, 'Challenges described:', 'Total marks 40'),
     (srp3('Challenges described', 6, ('Challenges described:', '6 SRP’s @ 3 marks each · 18 marks')),), '1-4', IRL),
])
PART_TWO.append(T(
    'p2-6c', P2, '6C', '', 30, 20, L(20, 'Regions and Culture'),
    (L(20, 'The culture of a region is often defined by religion, language, music, dance and games.'),
     L(20, 'Describe and explain the importance of culture in any region that you have studied.')),
    (S(20, 'Naming the region', 'Total marks 30'),),
    (fixed('Region named', 3, 'Naming the region · 3 marks'),
     srp3('Description and explanation', 9, ('Description/Explanation:', '9 SRP’s @ 3 marks each · 27 marks'))),
    '1-3', IRL + EURO, ID + 'p2-q6c'))

Q7AS = (L(22, 'Examine the table above and answer each of the following questions.'),)
PART_TWO += romans('7A', P2, 22, L(22, 'Economic Development'), Q7AS, ID + 'p2-q7a', ('page',), [
    ('(i)', 6, L(22, '(i) Calculate the difference in the Gross National Income per capita (in dollars)',
                 'between Haiti and Ireland.'),
     S(22, '$27601', '(ii) · How many'), (fixed('Difference', 6, '$27601 · 6 marks'),), '2-0', GRAPH),
    ('(ii)', 6, L(22, '(ii) How many more years are Irish children expected to spend in school compared to',
                  'children in India?'),
     S(22, '7.6 Years', '(iii) · Explain'), (fixed('Years', 6, '7.6 Years · 6 marks'),), '2-0', GRAPH),
    ('(iii)', 6, L(22, '(iii) Explain briefly why life expectancy at birth is lower in some countries.'),
     S(22, 'Brief explanation:', '(iv) · Name'), (srp3('Brief explanation', 2, BRIEF2),), '3-1', DEV),
    ('(iv)', 6, L(22, '(iv) Name the country with the lowest Human Development Index value and name',
                  'Human Development Index value.'),
     S(22, 'Haiti · 3 marks', '(v) · List'),
     (fixed('Lowest HDI', 3, 'Haiti · 3 marks'), fixed('Highest HDI', 3, 'Ireland · 3 marks')), '2-0', GRAPH),
    ('(v)', 6, L(22, '(v) List two reasons why some countries have a higher Human Development Index',
                 'value than others.'),
     S(22, '2 reasons @', 'Total marks 30'),
     (fixed('Two reasons', 6, '2 reasons @ 3 marks each · 6 marks', (0, 3, 6)),), '3-0', ECON + DEV),
])
Q7BI = L(22, '(i) Name one example of how the development of economic activities has resulted in',
         'conflict arising between people.')
PART_TWO += romans('7B', P2, 22, L(22, 'Economic Activity and Conflict'), (), ID + 'p2-q7b', (), [
    ('(i)', 3, Q7BI, S(23, 'Named example', '(ii) · Describe and explain this'),
     (fixed('Example named', 3, 'Named example · 3 marks'),), '3-4', ENV),
    ('(ii)', 27, L(22, '(ii) Describe and explain this conflict.'),
     S(23, 'Description/Explanation:', 'Total marks 30', None, '(ii) · Describe and explain this conflict'),
     (srp3('Description and explanation', 9, ('Description/Explanation:', '9 SRP’s @ 3 marks each · 27 marks')),),
     '3-4', ENV, (), (Q7BI,)),
])
Q7CI = L(22, '(i) Name one multinational company that you have studied and name one location',
         'of this multinational company.')
PART_TWO += romans('7C', P2, 22, L(22, 'Multinational Company'), (), ID + 'p2-q7c', (), [
    ('(i)', 4, Q7CI, S(23, 'Name the MNC', '(ii) · Describe and explain why'),
     (fixed('MNC named', 2, 'Name the MNC · 2 marks'), fixed('Location stated', 2, 'State location · 2 marks')),
     '3-2', MNC),
    ('(ii)', 18, L(22, '(ii) Describe and explain why this multinational company was set up at this location.'),
     S(23, 'Description/Explanation:', '(iii) · Explain one reason', None, '(ii) · Describe and explain why'),
     (srp3('Description and explanation', 6, ('Description/Explanation:', '6 SRP’s @ 3 marks each · 18 marks')),),
     '3-2', MNC, (), (Q7CI,)),
    ('(iii)', 18, L(22, '(iii) Explain one reason why this multinational company might decide to locate to',
                    'another area.'),
     S(23, 'Explanation:', 'Total marks 40', None, '(iii) · Explain one reason'),
     (srp3('Explanation', 6, ('Explanation:', '6 SRP’s @ 3 marks each · 18 marks')),), '3-2', MNC, (), (Q7CI,)),
])

Q8AS = (L(23, 'Examine the table above which shows energy use in the home.'),)
GRAPH_8A = (fixed('Graph paper', 3, 'Graph Paper · 3 marks'),
            fixed('Vertical axis labelled / circle', 3, 'Vertical axis labelled / Circle · 3 marks graded (3/1/0)',
                  (0, 1, 3)),
            fixed('Horizontal axis labelled / centred', 3,
                  'Horizontal axis labelled / Centred · 3 marks graded (3/1/0)', (0, 1, 3)),
            # "graded" is printed without its grades: every mark up to 15 is permitted.
            fixed('5 items illustrated', 15, '5 Items @ 3 marks each graded · 15 marks', upto(15)))
PART_TWO += romans('8A', P2, 23, L(23, 'Energy Use', nth=0), Q8AS, ID + 'p2-q8a', ('page',), [
    ('(i)', 24, L(23, '(i) Using graph paper, draw a suitable graph to illustrate this data.'),
     S(24, 'Graph Paper', '(ii) · In your answer book'), GRAPH_8A, '2-0', GRAPH),
    ('(ii)', 6, L(23, '(ii) In your answer book, name two sources of renewable energy.'),
     S(24, '2 sources named', 'Total marks 30'),
     (fixed('Two sources', 6, '2 sources named @ 3 marks each · 6 marks', (0, 3, 6)),), '3-5', ECON),
])
SECTOR = 'tourism or financial services'


def sector_routes(card_id):
    return (Route('tourism', 'tourism', card_id + '-tourism', False, ((SECTOR, 'tourism'),)),
            Route('financial-services', 'financial services', card_id + '-financial-services', False,
                  ((SECTOR, 'financial services'),)))


Q8BI = L(23, '(i) Name one developed economy where tourism or financial services contribute to', 'that economy.')
PART_TWO += [
    T('p2-8b-i', P2, '8B', '(i)', 4, 23, L(23, 'Economic Development – Developed Economy'), (Q8BI,),
      (S(24, 'One developed economy named', '(ii) · Explain reasons'),),
      (fixed('Developed economy named', 4, 'One developed economy named · 4 marks'),),
      '3-0', ECON, ID + 'p2-q8b-tourism', routes=sector_routes(ID + 'p2-q8b')),
    T('p2-8b-ii', P2, '8B', '(ii)', 18, 23, L(23, 'Economic Development – Developed Economy'),
      (L(23, '(ii) Explain the reasons for the growth of tourism or financial services in the',
         'developed economy named.'),),
      (S(24, 'Explanation:', '(iii) · Describe one problem'),),
      (srp3('Explanation', 6, ('Explanation:', '6 SRP’s @ 3 marks each · 18 marks')),),
      '3-0', ECON, ID + 'p2-q8b-ii-tourism', stem=(Q8BI,), routes=sector_routes(ID + 'p2-q8b-ii')),
    T('p2-8b-iii', P2, '8B', '(iii)', 18, 23, L(23, 'Economic Development – Developed Economy'),
      (L(23, '(iii) Describe one problem resulting from the growth of tourism or financial services',
         'in the developed economy named.'),),
      (S(24, 'Problem stated', 'Total marks 40'),),
      (fixed('Problem stated', 3, 'Problem stated · 3 marks'), srp3('Description', 5, '5 SRP’s @ 3 marks · 15 marks')),
      '3-0', ECON, ID + 'p2-q8b-iii-tourism', stem=(Q8BI,), routes=sector_routes(ID + 'p2-q8b-iii')),
]
Q8CS = (L(23, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper.'),
        L(23, 'Imagine you have been given the task of finding a suitable location for a multinational',
          'within the area covered by the map.'))
Q8CI = L(23, '(i) State clearly, where you would locate the multinational company using a',
         'six-figure grid reference.')
PART_TWO += romans('8C', P2, 23, L(23, 'Ordnance Survey Map'), Q8CS, ID + 'p2-q8c', ('map', 'legend'), [
    ('(i)', 6, Q8CI, S(25, 'Six figure grid reference', '(ii) · Explain two'),
     (fixed('Six-figure grid reference', 6, 'Six figure grid reference · 6 marks graded (6/4/2/0)', (0, 2, 4, 6)),),
     '2-6', MAP + ECON),
    ('(ii)', 18, L(23, '(ii) Explain two reasons in favour of this location.'),
     S(25, 'Reason 1', '18 marks'),
     (srp3('Reason 1', 3, 'Reason 1 · 3 SRP’s @ 3 marks each'), srp3('Reason 2', 3, 'Reason 2 · 3 SRP’s @ 3 marks each')),
     '3-2', MNC + MAP, (), (Q8CI,)),
    ('(iii)', 6, L(23, '(iii) Explain one disadvantage of this location.'),
     S(25, 'One disadvantage explained', 'Total marks 30'),
     (srp3('One disadvantage explained', 2, ('One disadvantage explained:', '2 SRP’s @ 3 marks each · 6 marks')),),
     '3-2', MNC + MAP, (), (Q8CI,)),
])

PART_TWO.append(aerial_sketch(
    '9A', 24, L(24, 'Examine the aerial photograph accompanying this paper.', 'An area of waste ground.'), 26,
    '2-8', AER + ECON,
    ('Two connecting streets', 'A bridge', 'A car park', 'An industrial area', 'An area of waste ground.')))
Q9BI = L(24, '(i) Name one example of environmental pollution that you have studied.')
PART_TWO += romans('9B', P2, 24, L(24, 'Environmental Pollution'), (), ID + 'p2-q9b', (), [
    ('(i)', 4, Q9BI, S(26, 'Example Named', '(ii) · Explain the cause'),
     (fixed('Example named', 4, 'Example Named · 4 marks'),), '3-4', ENV),
    ('(ii)', 24, L(24, '(ii) Explain the cause and effects of this environmental pollution.'),
     S(26, 'Explanation 8 SRP', '(iii) · Describe how'),
     (srp3('Explanation', 8, 'Explanation 8 SRP’s @ 3 marks each · 24 marks'),), '3-4', ENV, (), (Q9BI,)),
    ('(iii)', 12, L(24, '(iii) Describe how this environmental pollution could be reduced.'),
     S(26, 'Description 4 SRP', 'Total marks 40'),
     (srp3('Description', 4, 'Description 4 SRP’s @ 3 marks · 12 marks'),), '3-4', ENV, (), (Q9BI,)),
])
PART_TWO.append(T(
    'p2-9c', P2, '9C', '', 30, 24, L(24, 'European Union Policy'),
    (L(24, 'Choose any one of the European Union policies listed below.', 'Social Funding.'),),
    (S(27, 'Description and Explanation:', 'Total marks 30'),),
    (srp3('Description and explanation', 10, ('Description and Explanation:', '10 SRP’s @ 3 marks each · 30 marks')),),
    '3-3', EU, ID + 'p2-q9c-common-agricultural-policy', routes=bullet_routes('p2-q9c-', POLICIES)))

PART_TWO.append(aerial_sketch(
    '10A', 25, L(25, 'Examine the aerial photograph accompanying this paper.', 'A shopping centre.'), 28,
    '2-8', AER + URB,
    ('Two connecting streets', 'A car park', 'A recreational area', 'A residential area', 'A shopping centre.')))
PART_TWO.append(T(
    'p2-10b', P2, '10B', '', 30, 25, L(25, 'Urban Functions'),
    (L(25, 'Describe and explain how the functions and services of urban areas change over time,',
       'that you have studied.'),),
    (S(29, 'Example · 3 marks', 'Total marks 30'),),
    (fixed('Example', 3, 'Example · 3 marks'),
     srp3('Description and explanation', 9, ('Description/Explanation:', '9 SRP’s @ 3 marks each · 27 marks'))),
    '4-3', URB, ID + 'p2-q10b'))
Q10CI = L(25, '(i) Name one region that experiences overpopulation.')
OVER = '4 SRP’s @ 3 marks each · 12 marks'
PART_TWO += romans('10C', P2, 25, L(25, 'Overpopulation'), (), ID + 'p2-q10c', (), [
    ('(i)', 4, Q10CI, S(29, 'Region named', 'ii) · Explain', C10),
     (fixed('Region named', 4, 'Region named · 4 marks'),), '4-1', POP),
    ('(ii)', 12, L(25, '(ii) Explain one cause of this overpopulation.'),
     S(29, 'Explanation:', 'iii) · Describe', C10),
     (srp3('Explanation', 4, ('Explanation:', OVER)),), '4-1', POP, (), (Q10CI,)),
    ('(iii)', 12, L(25, '(iii) Describe the problems that result from overpopulation in this region.'),
     S(29, 'Description:', 'iv) · Describe', C10, 'iii) · Describe'),
     (srp3('Description', 4, ('Description:', OVER)),), '4-1', POP, (), (Q10CI,)),
    ('(iv)', 12, L(25, '(iv) Describe one solution to the problem of overpopulation.'),
     S(29, 'Description:', 'Total marks 40', C10, 'iv) · Describe'),
     (srp3('Description', 4, ('Description:', OVER)),), '4-1', POP),
])

Q11AS = (L(26, 'The table shows the means by which people travel to work', 'each of the following questions.'),)
PART_TWO += romans('11A', P2, 26, L(26, 'Travel and Work'), Q11AS, ID + 'p2-q11a', ('page',), [
    ('(i)', 6, L(26, '(i) What was the most popular means of travelling to work?'),
     S(30, 'Car · 6 marks', '(ii) · Which region'), (fixed('Means of travel', 6, 'Car · 6 marks'),), '2-0', GRAPH),
    ('(ii)', 6, L(26, '(ii) Which region had the greatest total percentage of people travelling to work on',
                  'foot and by bicycle?'),
     S(30, 'Dublin · 6 marks', '(iii) · Explain briefly'), (fixed('Region', 6, 'Dublin · 6 marks'),), '2-0', GRAPH),
    ('(iii)', 6, L(26, '(iii) Explain briefly why the Dublin region had the highest percentage of people',
                   'travelling to work by bus and train.'),
     S(30, 'Brief explanation:', '(iv) · List two'), (srp3('Brief explanation', 2, BRIEF2),), '4-5', URB),
    ('(iv)', 6, L(26, '(iv) List two problems that may be experienced in urban areas where a high',
                  'travel to work by car.'),
     S(30, 'Name 2 problems', '(v) · List two'),
     (fixed('Two problems', 6, 'Name 2 problems @ 3 marks each · 6 marks', (0, 3, 6)),), '4-5', URB),
    ('(v)', 6, L(26, '(v) List two ways authorities in urban areas attempt to reduce the number of people',
                 'travelling to work by car.'),
     S(30, 'Name 2 ways', 'Total marks 30'),
     (fixed('Two ways', 6, 'Name 2 ways @ 3 marks each · 6 marks', (0, 3, 6)),), '4-5', URB),
])
Q11BS = (L(26, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper.'),)
Q11BI = L(26, '(i) Name and locate, using six-figure grid references, three different examples of',
          'evident on the Ordnance Survey map.')
SETTLE = '=2 SRP’s @ 3 marks each · 6 marks'
PART_TWO += romans('11B', P2, 26, L(26, 'Historic Settlement'), Q11BS, ID + 'p2-q11b', ('map', 'legend'), [
    ('(i)', 12, Q11BI, S(31, 'For each historic settlement:', '(ii) · Describe and explain each'),
     (fixed('Three settlements named', 6, ('For each historic settlement:', '3 settlements named'), (0, 2, 4, 6)),
      fixed('Three settlements located', 6, '3 settlements located', upto(6))), '2-6', MAP + URB),
    ('(ii)', 18, L(26, '(ii) Describe and explain each of the examples of historic settlement named in part (i)',
                   'above.'),
     S(31, 'Settlement 1 Description', 'Total marks 30'),
     tuple(srp3(f'Settlement {n}', 2, (f'Settlement {n} Description/Explanation:', f'{SETTLE}@{n - 1}'))
           for n in (1, 2, 3)), '4-3', URB + MAP, (), (Q11BI,)),
])
Q11CI = L(26, '(i) Name one city in the developing world.')
PART_TWO += romans('11C', P2, 26, L(26, 'Developing World City'), (), ID + 'p2-q11c', (), [
    ('(i)', 4, Q11CI, S(31, 'Developing world city named', '(ii) · Explain the problems'),
     (fixed('Developing world city named', 4, 'Developing world city named · 4 marks'),), '4-5', URB),
    ('(ii)', 24, L(26, '(ii) Explain the problems experienced in this named city.'),
     S(31, 'Problems explained:', '(iii) · Describe one solution'),
     (srp3('Problems explained', 8, ('Problems explained:', '8 SRP’s @ 3 marks each · 24 marks')),), '4-5', URB,
     (), (Q11CI,)),
    ('(iii)', 12, L(26, '(iii) Describe one solution to these problems.'),
     S(31, 'Solution described:', 'Total marks 40'),
     (srp3('Solution described', 4, ('Solution described:', '4 SRP’s @ 3 marks each · 12 marks')),), '4-5', URB,
     (), (Q11CI,)),
])

Q12AS = (L(27, 'Examine the data above showing the population of some of the most populous cities of',
           'the world in 2012.'),)
GRAPH_12A = (fixed('Graph paper', 2, 'Graph paper · 2 marks'),
             fixed('Vertical axis labelled', 3, 'Vertical Axis labelled · 3 marks graded (3/1/0)', (0, 1, 3)),
             fixed('Horizontal axis labelled', 3, 'Horizontal Axis labelled · 3 marks graded (3/1/0)', (0, 1, 3)),
             fixed('4 items illustrated', 16, '4 Items @ 4 marks each graded (4/2/0) · 16 marks',
                   sums(*[(0, 2, 4)] * 4)))
PART_TWO += romans('12A', P2, 27, L(27, 'World Cities'), Q12AS, ID + 'p2-q12a', ('page',), [
    ('(i)', 24, L(27, '(i) Using graph paper, draw a suitable graph to illustrate this data.'),
     S(32, 'Graph paper', '(ii) · In your answer book'), GRAPH_12A, '2-0', GRAPH),
    ('(ii)', 6, L(27, '(ii) In your answer book, explain briefly one problem associated with large cities.'),
     S(32, 'Explanation:', 'Total marks 30', None, '(ii) · In your answer book'),
     (srp3('Explanation', 2, ('Explanation:', '2 SRP’s @ 3 marks each · 6 marks')),), '4-5', URB),
])
Q12BI = L(27, '(i) State two reasons why people migrate from rural areas to urban areas.')
MIGRATE = ('Description/Explanation:', '6 SRP’s @ 3 marks each · 18 marks')
PART_TWO += romans('12B', P2, 27, L(27, 'Migration'), (), ID + 'p2-q12b', (), [
    ('(i)', 4, Q12BI, S(32, 'State two reasons @', '(ii) · Describe and explain the effect'),
     (fixed('Two reasons', 4, 'State two reasons @ 2 marks each · 4 marks', (0, 2, 4)),), '4-2', POP),
    ('(ii)', 18, L(27, '(ii) Describe and explain the effect of this migration on the urban areas that people',
                   'migrate to.'),
     S(32, 'Description/Explanation:', '(iii) · Describe and explain', None, '(ii) · Describe and explain the effect'),
     (srp3('Description and explanation', 6, MIGRATE),), '4-2', POP + URB, (), (Q12BI,)),
    ('(iii)', 18, L(27, '(iii) Describe and explain the effect of this migration on the rural areas they leave',
                    'behind.'),
     S(32, 'Description/Explanation:', 'Total marks 40', None, '(iii) · Describe and explain'),
     (srp3('Description and explanation', 6, MIGRATE),), '4-2', POP, (), (Q12BI,)),
])
PART_TWO.append(T(
    'p2-12c', P2, '12C', '', 30, 27, L(27, 'Development of Towns'),
    (L(27, 'Examine the aerial photograph accompanying this paper.'),
     L(27, 'Using evidence from the aerial photograph, explain three reasons why the town of',
       'developed at its present location.')),
    (S(33, 'Aerial Photograph evidence', 'Total marks 30'),),
    (fixed('Aerial photograph evidence', 3, 'Aerial Photograph evidence · 3 marks'),
     srp3('Reason 1', 3, 'Reason 1 3 SRP’s @ 3 marks each · 9 marks'),
     srp3('Reason 2', 3, 'Reason 2 3 SRP’s @ 3 marks each · 9 marks'),
     srp3('Reason 3', 3, 'Reason 3 3 SRP’s @ 3 marks · 9 marks')),
    '4-3', URB + AER, ID + 'p2-q12c', ('aerial',)))

TASKS = [*PART_ONE, *PART_TWO]

ID_CORRECTION_REASON = 'No 2014 Ordinary card shipped before this review; every card is new.'

# No 2014 Ordinary card was live on origin/main before this review.
LEGACY_IDS: list[str] = []
