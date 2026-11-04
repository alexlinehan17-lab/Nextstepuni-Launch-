"""Independent review ledger: Leaving Certificate Geography 2015 Ordinary Level.

Sources (English editions, harvested Paper Trail corpus; sizes and SHA-256
pinned in EXPECTED_SOURCES and the generated audit): the examination paper
LC005GLP000EV (28 pages; one booklet printed Part One, answered in it, and
Part Two), marking scheme LC005GLP000EV (40 pages), and the common Kenmare
companions shared with Higher Level — the 1:50 000 map LC005CLP003EV, its
legend LC005CLPC00EV and the aerial photograph LC005CLP004EV. Part One is
100 marks (any ten of twelve @ 10), Part Two 300 (three questions @ 100).

Visual sweep (every page rendered and read on 2026-10-14):
  Paper p1 cover and examiner's grid; p2-p11 Part One Questions 1-12 (p6
  holds Q5 and Q6, p8 Q8 and Q9; Q7 prints six sections cut from the
  aerial photograph); p12 Part Two instructions; p13 Section 1 divider;
  p14-p19 Q1-Q6 (p14 and p17 open with their dividers); p20 Section 2
  divider; p21-p26 Electives Q7-Q12 (p21 and p24 open with their elective
  dividers); p27-p28 printed "Blank Page".
  Scheme p1 cover; p2-p3 notes; p4-p5 Geographical Investigation
  (coursework) and its presentation marks; p6-p7 Part One table; p8 Part
  Two instructions and Section 1 divider; p9-p21 Q1-Q6; p22 Section 2
  divider; p23-p34 Q7-Q12; p35 investigation topics; p36 Irish-language
  bonus marks; p37-p39 printed "Blank Page"; p40 back cover.

Boundaries and tariffs follow the 2016 Ordinary ledger: every priced roman
is a task, and so is every lettered statement priced on its own (Q3(ii)(a)-
(b)). Matching tables, in the printed row order: Q1 Sea stack C, Sea arch
B, Sea cave D, Sea cliff A; Q2 Levée D, Floodplain C, Meander B, Oxbow
lake A; Q3 Pillar/column C, Clint A, Stalactite B; Q6 V 862 773 Parking,
V 918 718 Golf course, V 877 676 Public telephone, V 909 706 Post office;
Q7 Left Foreground False, Centre Middleground True, Right Middleground
True, Right Background False, Left Background True (Centre Background is
printed); Q8 Paris E, Antrim-Derry Plateau C, Sambre Meuse A, Mezzogiorno
B, Longford County Council D; Q9 Farmer Primary, Hotel receptionist
Tertiary, Baker Secondary, Furniture maker Secondary, Doctor Tertiary
(Forestry worker is printed); Q10 Temperature D, Rainfall C, Cloud A,
Pressure B; Q11 Pie chart B, Wind rose D, Bar chart A, Trend graph C; Q12
Viewpoint C, National Secondary Road D, Picnic Site B, Coniferous
Plantation A.

4B and 6C open by asking for a region and the scheme prices "Naming a
region · 1m" outside the romans; it is carded with part (i), the first
part that asks about that region.

Tariffs as printed: twelve parts carry 40 marks (1B, 2B, 3B, 4B, 5B, 6C,
7B, 8B, 9C, 10B, 11B, 12C) and the rest 30.
"""

from geography_review import (
    Criterion, Lift, Route, SchemeSlice, Task, pool, fixed, slug, srp, steps, sums,
)

YEAR = 2015
LEVEL = 'ordinary'
PAPER_PAGES = {1: 28, 2: 28}
SCHEME_PAGES = 40
_FORTY = {'1B', '2B', '3B', '4B', '5B', '6C', '7B', '8B', '9C', '10B', '11B', '12C'}
QUESTION_TARIFFS = {1: {str(n): 10 for n in range(1, 13)},
                    2: {f'{n}{x}': (40 if f'{n}{x}' in _FORTY else 30)
                        for n in range(1, 13) for x in 'ABC'}}

EXPECTED_SOURCES = {
    'paper1': ('LC005GLP000EV.pdf', 2955016),
    'paper2': ('LC005GLP000EV.pdf', 2955016),
    'scheme': ('LC005GLP000EV.pdf', 568844),
    'map': ('LC005CLP003EV.pdf', 6859305),
    'legend': ('LC005CLPC00EV.pdf', 2156988),
    'aerial': ('LC005CLP004EV.pdf', 2647375),
}

_PAPER = {1: 'cover and examiner grid', **{p: 'question' for p in range(2, 12)},
          12: 'Part Two instructions', 13: 'section divider', **{p: 'question' for p in range(14, 20)},
          20: 'section divider', **{p: 'question' for p in range(21, 27)}, 27: 'blank page', 28: 'blank page'}
PAGE_REVIEW = {
    # One booklet printed both parts.
    'paper1': _PAPER, 'paper2': _PAPER,
    'scheme': {1: 'cover', 2: 'notes', 3: 'notes', 4: 'geographical investigation (coursework)',
               5: 'presentation marks (coursework)', 6: 'Part One table', 7: 'Part One table',
               8: 'Part Two instructions and section divider',
               **{p: 'Part Two allocation' for p in range(9, 22)}, 22: 'section divider',
               **{p: 'Part Two allocation' for p in range(23, 35)},
               35: 'investigation topics', 36: 'Irish-language bonus marks',
               37: 'blank', 38: 'blank', 39: 'blank', 40: 'back cover'},
}

EXPECTED_SELECTION_SCAN = [
    [1, 2, 'attempt any ten'], [1, 12, 'attempt three'], [1, 13, 'attempt two'],
    [1, 14, 'attempt one'], [1, 14, 'answer (i) or (ii)'], [1, 14, 'any two'], [1, 14, 'any two'],
    [1, 16, 'any two'], [1, 16, 'one of the following'],
    [1, 17, 'attempt one'],
    [1, 18, 'any two'],
    [1, 20, 'attempt one'],
    [1, 22, 'one of the following'],
]
SELECTION_REVIEW = [
    {'scan': [[1, 2, 'attempt any ten'], [1, 12, 'attempt three'], [1, 13, 'attempt two'], [1, 14, 'attempt one'],
              [1, 17, 'attempt one'], [1, 20, 'attempt one']],
     'kind': 'exam-attempt-rule',
     'reason': 'Part One any ten of twelve and Part Two three questions (one of Q1-3, one of Q4-6, one elective) are attempt rules; every question is carded.'},
    {'scan': [[1, 14, 'answer (i) or (ii)']], 'kind': 'closed-route',
     'reason': '1B: (i) or (ii) -> two routes, each with its own scheme allocation.'},
    {'scan': [[1, 16, 'one of the following'], [1, 22, 'one of the following']], 'kind': 'closed-choose-one',
     'reason': '3C one of three printed surface processes -> 3 routes; 8C one of three printed activities -> 3 routes.'},
    {'scan': [[1, 18, 'any two']], 'kind': 'choose-n-one-card',
     'reason': '5B any two of four printed factors -> one card with every printed item (choice is not a route).'},
    {'scan': [[1, 14, 'any two'], [1, 14, 'any two'], [1, 16, 'any two']], 'kind': 'open-response',
     'reason': 'No printed pool: 1B(i) any two landforms and 1B(ii) any two mass movement processes (the scheme prices two @ 20m); 3A(iii) any two ways rocks are used. Compulsory lists stay whole: 1A, 4A, 6A, 7A, 11A each item; 3B(i) each volcano type.'},
]

P1, P2 = 1, 2
ID = 'geography-2015-ol-'
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
BRIEF = 'Brief explanation 2 SRP’s @ 3m each · 6m'

# ---------------------------------------------------------------- Part One --
PART_ONE = romans('1', P1, 2, L(2, 'Coastal Landforms'), (), ID + 'p1-q1', ('page',), [
    ('(i)', 8, L(2, '(i) Examine the photograph above showing coastal landforms and match each of the',
                 'in the table below.'),
     S(6, 'Q.1 (i)', '(ii) False'),
     rows(['Q.1 (i) Sea stack · C · 2m', 'Sea arch · B · 2m', 'Sea cave · D · 2m', 'Sea cliff · A · 2m']), '0-10', SEA,
     (L(2, 'Sea stack'), L(2, 'Sea arch'), L(2, 'Sea cave'), L(2, 'Sea cliff'))),
    ('(ii)', 2, (L(2, '(ii) Indicate whether the statement below is true or false, by ticking the correct box.'),
                 L(2, 'All of the landforms named above are formed by coastal deposition.')),
     S(6, '(ii) False', 'Q.2 (i)'), (fixed('True or false', 2, '(ii) False · 2m · Total 10m'),), '0-10', SEA),
])
PART_ONE += romans('2', P1, 3, L(3, 'River Landforms'),
                   (L(3, 'Examine the diagram above showing river landforms and answer each of the following',
                      'questions.'),),
                   ID + 'p1-q2', ('page',), [
    ('(i)', 8, L(3, '(i) Match each of the letters A, B, C and D with the landform that best matches it,',
                 'in the table below.'),
     S(6, 'Q.2 (i)', '(ii) Old age'),
     rows(['Q.2 (i) Leveé · D · 2m', 'Floodplain · C · 2m', 'Meander · B · 2m', 'Oxbow lake · A · 2m']), '0-9', RIVERS,
     (L(3, 'Levée'), L(3, 'Floodplain'), L(3, 'Meander'), L(3, 'Oxbow lake'))),
    ('(ii)', 2, L(3, '(ii) Indicate whether the landforms named above are most associated with the youthful',
                  'Old age stage'),
     S(6, '(ii) Old age', 'Q.3 (i)'), (fixed('Stage', 2, '(ii) Old age stage · 2m · Total 10m'),), '0-9', RIVERS),
])
TF3 = L(4, '(ii) Indicate whether each of the statements below is true or false, by ticking the', 'correct box.')
PART_ONE += romans('3', P1, 4, L(4, 'Karst Landscape'),
                   (L(4, 'Examine the diagram of a karst landscape above and answer each of the following',
                      'questions.'),),
                   ID + 'p1-q3', ('page',), [
    ('(i)', 6, L(4, '(i) Match each of the letters A, B and C in the diagram above with the landform that',
                 'in the table below.'),
     S(6, 'Q.3 (i)', '(ii) (a) False'),
     rows(['Q.3 (i) Pillar/column · C · 2m', 'Clint · A · 2m', 'Stalactite · B · 2m']), '0-3', KARST,
     (L(4, 'Pillar/column'), L(4, 'Clint'), L(4, 'Stalactite'))),
    ('(ii)(a)', 2, (TF3, L(4, '(a) The Giant’s Causeway is an example of a karst landscape.')),
     S(6, '(ii) (a) False', '(b) True'), (fixed('Statement (a)', 2, '(ii) (a) False · 2m'),), '0-3', KARST),
    ('(ii)(b)', 2, (TF3, L(4, '(b) Permeable rock allows water to pass through it easily.')),
     S(6, '(b) True', 'Q.4'), (fixed('Statement (b)', 2, '(b) True · 2m · Total 10m'),), '0-3', KARST + RW),
])
PART_ONE += romans('4', P1, 5, L(5, 'Earthquakes', nth=0),
                   (L(5, 'Examine the table above and answer each of the following questions.'),),
                   ID + 'p1-q4', ('page',), [
    ('(i)', 2, L(5, '(i) What was the magnitude of the earthquake in Southern Sumatra in 2009?'),
     S(6, 'Q.4(i)', '(ii) 2011'), (fixed('Magnitude', 2, 'Q.4(i) 7.5 · 2m'),), '0-7', EV),
    ('(ii)', 2, L(5, '(ii) In which year was the largest earthquake?'),
     S(6, '(ii) 2011', '(iii) Haiti'), (fixed('Year', 2, '(ii) 2011 · 2m'),), '0-7', EV),
    ('(iii)', 2, L(5, '(iii) Where was the earthquake with the greatest number of fatalities?'),
     S(6, '(iii) Haiti', '(iv) Epicentre'), (fixed('Place', 2, '(iii) Haiti · 2m'),), '0-7', EV),
    ('(iv)', 2, L(5, '(iv) What is the name given to the point on the earth’s surface directly above the',
                  'an earthquake?'),
     S(6, '(iv) Epicentre', '(v) True'), (fixed('Name', 2, '(iv) Epicentre · 2m'),), '0-7', EV),
    ('(v)', 2, (L(5, '(v) Indicate whether the statement below is true or false, by ticking the correct box.'),
                L(5, 'Earthquakes occur where plates collide.')),
     S(6, '(v) True', 'Q.5'), (fixed('True or false', 2, '(v) True · 2m · Total 10m'),), '0-7', EV + PS),
])
PART_ONE += romans('5', P1, 6, L(6, 'Ordnance Survey Map', nth=0),
                   (L(6, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper.', nth=0),),
                   ID + 'p1-q5', ('map', 'legend'), [
    ('(i)', 5, L(6, '(i) Imagine that you are travelling from Kenmare at V 906 713', 'would you be travelling?'),
     S(6, 'Q.5 (i)', '(ii) 5.8'), (fixed('Direction', 5, ('Q.5 (i) North West', 'North North West · 5m')),),
     '2-6', MAP),
    ('(ii)', 5, L(6, '(ii) The length of the N70 road', 'Tick the correct box.'),
     S(6, '(ii) 5.8', 'Q.6 (i)'), (fixed('Length', 5, '(ii) 5.8km · 5m · Total 10m'),), '2-6', MAP),
])
PART_ONE += romans('6', P1, 6, L(6, 'Ordnance Survey Map', nth=1),
                   (L(6, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper.', nth=1),),
                   ID + 'p1-q6', ('map', 'legend'), [
    ('(i)', 8, L(6, '(i) Name the features which can be found at each of the following grid references.'),
     S(6, 'Q.6 (i)', '(ii) Clustered'),
     rows(['Q.6 (i) Parking/car park · 2m', 'Golf course · 2m', 'Public telephone · 2m', 'Post office · 2m']),
     '2-6', MAP, (L(6, 'V 862 773'), L(6, 'V 918 718'), L(6, 'V 877 676'), L(6, 'V 909 706'))),
    ('(ii)', 2, L(6, '(ii) Indicate the rural settlement pattern found at V 898 719', 'Clustered/Nucleated'),
     S(6, '(ii) Clustered', None), (fixed('Settlement pattern', 2, '(ii) Clustered/Nucleated · 2m · Total 10m'),),
     '4-3', URB + MAP),
])
PART_ONE += [
    T('p1-7', P1, '7', '', 10, 7, L(7, 'Aerial Photograph - Location'),
      (L(7, 'Indicate whether the descriptions of the locations of each of the sections',
         'One has been completed for you.'),),
      (S(7, 'Q.7', 'Q.8'),),
      rows(['Q.7 · Left Foreground · False · 2m', 'Centre Middleground · True · 2m', 'Right Middleground · True · 2m',
            'Right Background · False · 2m', 'Left Background · True · 2m · Total 10m']),
      '2-8', AER, ID + 'p1-q7', ('page', 'aerial'),
      (L(7, 'Examine the aerial photograph accompanying this paper, and the sections taken from it below.'),),
      row_labels=(L(7, 'Left Foreground'), L(7, 'Centre Middleground'), L(7, 'Right Middleground'),
                  L(7, 'Right Background'), L(7, 'Left Background'))),
    T('p1-8', P1, '8', '', 10, 8, L(8, 'Regions'),
      (L(8, 'Match the description of a region with the example of the region most associated',
         'in the table below.'),),
      (S(7, 'Q.8', 'Q.9'),),
      rows(['Q.8 · Paris · E · 2m', 'Antrim-Derry Plateau · C · 2m', 'Sambre Meuse · A · 2m', 'Mezzogiorno · B · 2m',
            'Longford Co Council · D · 2m · Total 10m']),
      '1-0', IRL + EURO, ID + 'p1-q8', ('page',),
      row_labels=(L(8, 'Paris'), L(8, 'Antrim-Derry Plateau'), L(8, 'Sambre Meuse, Belgium'), L(8, 'Mezzogiorno'),
                  L(8, 'Longford County Council'))),
    T('p1-9', P1, '9', '', 10, 8, L(8, 'Economic Activities'),
      (L(8, 'Write the category of economic activity (Primary, Secondary or Tertiary)', 'One has been completed for you.'),),
      (S(7, 'Q.9', 'Q.10(i)'),),
      rows(['Q.9 · Farmer · Primary · 2m', 'Hotel receptionist · Tertiary · 2m', 'Baker · Secondary · 2m',
            'Furniture maker · Secondary · 2m', 'Doctor · Tertiary · 2m · Total 10m']),
      '3-0', ECON, ID + 'p1-q9', ('page',),
      row_labels=(L(8, 'Farmer'), L(8, 'Hotel receptionist'), L(8, 'Baker'), L(8, 'Furniture maker'), L(8, 'Doctor'))),
]
PART_ONE += romans('10', P1, 9, L(9, 'Weather Charts'),
                   (L(9, 'Examine the weather charts above and answer each of the following questions.'),),
                   ID + 'p1-q10', ('page',), [
    ('(i)', 8, L(9, '(i) Match each weather chart with the element of weather that it represents',
                 'in the table below.'),
     S(7, 'Q.10(i)', '(ii) True'),
     rows(['Q.10(i) Temperature · D · 2m', 'Rainfall · C · 2m', 'Cloud · A · 2m', 'Pressure · B · 2m']), '2-7', WEATHER,
     (L(9, 'Temperature'), L(9, 'Rainfall'), L(9, 'Cloud'), L(9, 'Pressure'))),
    ('(ii)', 2, (L(9, '(ii) Indicate whether the statement below is true or false, by ticking the correct box.'),
                 L(9, 'Isobars are lines joining places of equal pressure on a weather chart.')),
     S(7, '(ii) True', 'Q.11(i)'), (fixed('True or false', 2, '(ii) True · 2m · Total 10m'),), '2-7', WEATHER),
])
PART_ONE += romans('11', P1, 10, L(10, 'Statistical Charts'), (), ID + 'p1-q11', ('page',), [
    ('(i)', 8, L(10, '(i) Match each statistical chart with the most suitable title in the table below',
                 'in each case.'),
     S(7, 'Q.11(i)', '(ii) Valid'),
     rows(['Q.11(i) Pie chart · B · 2m', 'Wind rose · D · 2m', 'Bar chart · A · 2m', 'Trend graph · C · 2m']),
     '2-0', GRAPH, (L(10, 'Pie chart'), L(10, 'Wind rose'), L(10, 'Bar chart'), L(10, 'Trend graph'))),
    ('(ii)', 2, L(10, '(ii) State one advantage of using a graph to present information.'),
     S(7, '(ii) Valid', 'Q.12(i)'), (fixed('Advantage', 2, '(ii) Valid statement · 2m · Total 10m'),), '2-0', GRAPH),
])
PART_ONE += romans('12', P1, 11, L(11, 'Symbol Recognition and Scale'),
                   (L(11, 'Examine the Ordnance Survey map and legend accompanying this paper.'),),
                   ID + 'p1-q12', ('page', 'map', 'legend'), [
    ('(i)', 8, L(11, '(i) Match each of the map symbols with the name that best matches it', 'in the table below.'),
     S(7, 'Q.12(i)', '(ii) 1:50'),
     rows(['Q.12(i) Viewpoint · C · 2m', 'National Secondary Road · D · 2m', 'Picnic Site · B · 2m',
           'Coniferous Plantation · A · 2m']), '2-6', MAP,
     (L(11, 'Viewpoint'), L(11, 'National Secondary Road'), L(11, 'Picnic Site'), L(11, 'Coniferous Plantation'))),
    ('(ii)', 2, L(11, '(ii) What is the scale of the Ordnance Survey map accompanying this paper?'),
     S(7, '(ii) 1:50', None), (fixed('Scale', 2, '(ii) 1:50 000, 2cm to 1km · 2m · Total 10m'),), '2-6', MAP),
])


# ---------------------------------------------------------------- Part Two --
def sketch(page, title, prompt, scheme_page, card_id, topic, atlas, sources, showing, show_permitted, label_line,
           labels):
    """A sketch: 5-mark outline and five items (showing graded, labelling 2)."""
    item = sums(show_permitted, (0, 2))
    return T(f'p2-{card_id.rsplit("-q", 1)[1]}', P2, card_id.rsplit('-q', 1)[1].upper(), '', 30, page,
             title, (prompt,), (S(scheme_page, 'Sketch Outline:', 'Total 30m'),),
             (fixed('Limits/frame', 1, ('Sketch Outline:', 'Limits/frame · 1m')),
              fixed('Proportions', 2, 'Proportions · 2m (2/0)'),
              fixed('Overall impression', 2, 'Overall impression · 2m graded (2/1/0)', (0, 1, 2)),
              *(Criterion(f'Item {n}', 5, item, 'exact', ('Five items shown and', showing, label_line))
                for n in range(1, 6))),
             topic, atlas, card_id, sources,
             row_labels=(None, None, None, *(L(page, b) for b in labels)))


def two_of(label, count, head, each, lines, unit):
    per = sums(*unit)
    return tuple(Criterion(f'{label} {n}', count, per, 'srp', (head, each, *lines)) for n in (1, 2))


SHOWN = 'Shown · 4m graded (4/2/0)'
NAMED_SHOWN = sums((0, 2), (0, 2, 4))
GRAPH_OL = (fixed('Graph paper', 2, 'Graph paper · 2m', (0, 2)),
            fixed('Vertical axis labelled / circle', 3, 'Vertical Axis labelled / Circle · 3m graded (3/1/0)',
                  (0, 1, 3)),
            fixed('Horizontal axis labelled / centred', 3, 'Horizontal Axis labelled / Centred · 3m graded (3/1/0)',
                  (0, 1, 3)),
            fixed('4 items illustrated', 16, '4 Items @ 4m each graded (4/2/0) · 16m', sums(*[(0, 2, 4)] * 4)))
SURFACE = ('River processes', 'Coastal processes', 'Mass movement processes.')
DEVELOPED = ('Tourism', 'Financial services', 'Service and footloose industries.')
FACTORS_5B = ('Availability of transport networks', 'Access to raw materials', 'Markets',
              'Government and European Union Policies.')

PART_TWO = [
    sketch(14, L(14, 'Ordnance Survey Map'),
           L(14, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper.', 'A named lake.'),
           9, ID + 'p2-q1a', '2-6', MAP + SEA, ('map', 'legend'), 'Showing · 3m graded (3/2/1/0)', (0, 1, 2, 3),
           'Labelled · 2m',
           ('An area of natural woodland', 'An area of land above 400 metres', 'Dinish Island', 'The Kenmare River',
            'A named lake.')),
    T('p2-1b', P2, '1B', '', 40, 14, L(14, 'Surface Processes'),
      (L(14, '(i) Explain, with the aid of diagrams, the formation of any two landforms.'),),
      (S(10, 'Formation of any two landforms @ 20m each', 'Total 40m'),),
      two_of('Landform', 20, 'Formation of any two landforms @ 20m each', 'For each landform:',
             ('Landform named · 1m', 'Diagram(s) two aspects @ 2m each · 4m',
              'Formation explained 5 SRPs @ 3m each · 15m'),
             ((0, 1), (0, 2, 4), steps(15, 3))),
      '0-4', PS_SURFACE, ID + 'p2-q1b-route-i',
      routes=(
          Route('route-i', 'Route (i)', ID + 'p2-q1b-route-i', False),
          Route('route-ii', 'Route (ii)', ID + 'p2-q1b-route-ii', False,
                prompt=(L(14, '(ii) Describe and explain any two processes of mass movement.'),),
                scheme=(S(10, 'Any two processes @ 20m each', 'Total 40m'),),
                criteria=two_of('Process', 20, 'Any two processes @ 20m each', 'For each process:',
                                ('Process named/stated · 2m', 'Description and explanation 6 SRPs @ 3m each · 18m'),
                                ((0, 2), steps(18, 3))),
                topic='0-8', atlas=RW),
      )),
    T('p2-1c', P2, '1C', '', 30, 14, L(14, 'Plate Tectonics'),
      (L(14, 'Describe and explain the theory of plate tectonics.'),),
      (S(11, 'Description and explanation 10', 'Total 30m'),),
      (srp3('Description and explanation', 10, 'Description and explanation 10 SRP’s @ 3m each · 30m'),),
      '0-0', PS, ID + 'p2-q1c'),
]
Q2AS = (L(15, 'Examine the diagram of the structure of the earth above and answer each of the following',
          'questions.'),)
PART_TWO += romans('2A', P2, 15, L(15, 'Structure of the Earth'), Q2AS, ID + 'p2-q2a', ('page',), [
    ('(i)', 18, L(15, '(i) In your answer book, name each of the layers of the earth labelled A, B and C.'),
     S(12, 'A · Inner Core', '(ii) · Explain briefly what is meant'),
     (fixed('A', 6, 'A · Inner Core · 6m'), fixed('B', 6, 'B · Mantle · 6m'), fixed('C', 6, 'C · Crust · 6m')),
     '0-0', PS),
    ('(ii)', 6, L(15, '(ii) Explain briefly what is meant by the term plate.'),
     S(12, 'Brief explanation 2 SRP', '(iii) · Explain briefly what causes', None, '(ii) · Explain briefly what is meant'),
     (srp3('Brief explanation', 2, BRIEF),), '0-0', PS),
    ('(iii)', 6, L(15, '(iii) Explain briefly what causes plates to move.'),
     S(12, 'Brief explanation 2 SRP', 'Total 30m', None, '(iii) · Explain briefly what causes'),
     (srp3('Brief explanation', 2, BRIEF),), '0-0', PS),
])
PART_TWO += romans('2B', P2, 15, L(15, 'Rocks'), (), ID + 'p2-q2b', (), [
    ('(i)', 6, L(15, '(i) Name one igneous rock, and name one metamorphic rock.'),
     S(12, 'Igneous rock named', '(ii) · Name one sedimentary'),
     (fixed('Igneous rock named', 3, 'Igneous rock named · 3m'),
      fixed('Metamorphic rock named', 3, 'Metamorphic rock named · 3m')), '0-1', RW),
    ('(ii)', 7, L(15, '(ii) Name one sedimentary rock, and name one Irish location where this rock is found.'),
     S(12, 'Sedimentary rock named', '(iii) · Describe'),
     (fixed('Sedimentary rock named', 3, 'Sedimentary rock named · 3m'),
      fixed('Irish location named', 4, 'Irish location named · 4m')), '0-1', RW + IRL),
    ('(iii)', 27, L(15, '(iii) Describe how sedimentary rocks are formed.'),
     S(12, '9 SRP’s @ 3m each · 27m', 'Total 40m'),
     (srp3('Description', 9, '9 SRP’s @ 3m each · 27m'),), '0-1', RW),
])
PART_TWO += romans('2C', P2, 15, L(15, 'Fold Mountains'), (), ID + 'p2-q2c', (), [
    ('(i)', 3, L(15, '(i) Name one example of fold mountains.'),
     S(13, 'Example of fold mountain', '(i) · With the aid'),
     (fixed('Fold mountains named', 3, 'Example of fold mountain named · 3m'),), '0-2', RW + PS),
    ('(ii)', 27, L(15, '(ii) With the aid of a diagram(s), explain how fold mountains are formed.'),
     S(13, 'Diagram three items', 'Total 30m'),
     (fixed('Diagram', 6, 'Diagram three items @ 2m each · 6m', (0, 2, 4, 6)),
      srp3('Explanation', 7, 'Explanation 7 SRP’s @ 3m each · 21m')), '0-2', RW + PS),
])
Q3AS = (L(16, 'Examine the diagram of the rock cycle above and answer each of the following', 'questions.'),)
PART_TWO += romans('3A', P2, 16, L(16, 'Rock Cycle'), Q3AS, ID + 'p2-q3a', ('page',), [
    ('(i)', 12, L(16, '(i) Name the category of rock at X and name one rock in this category.'),
     S(14, 'Category X', '(ii) · Name the category'),
     (fixed('Category X', 6, 'Category X: Sedimentary rock · 6m'),
      fixed('Example', 6, 'Example: Sandstone, limestone etc. · 6m')), '0-1', RW),
    ('(ii)', 12, L(16, '(ii) Name the category of rock at Y and name one rock in this category.'),
     S(14, 'Category Y', '(iii) · Name any two'),
     (fixed('Category Y', 6, 'Category Y: Metamorphic rock · 6m'),
      fixed('Example', 6, 'Example: Marble, quartzite etc. · 6m')), '0-1', RW),
    ('(iii)', 6, L(16, '(iii) Name any two ways rocks are used.'),
     S(14, 'Any two uses named', 'Total 30m'),
     (fixed('Two uses', 6, 'Any two uses named @ 3m each · 6m', (0, 3, 6)),), '0-6', RW),
])
PART_TWO += romans('3B', P2, 16, L(16, 'Volcanoes'), (), ID + 'p2-q3b', (), [
    ('(i)', 16, L(16, '(i) Define and name an example of each of the volcano types listed below:', 'Extinct volcano.'),
     S(14, 'Three volcano types', '(ii) · Explain in detail'),
     (fixed('Volcano 1', 6, ('Three volcano types @ 6m + 5m + 5m', 'Volcano 1 · Definition · 3m', '=Example · 3m'),
            sums((0, 3), (0, 3))),
      fixed('Volcano 2', 5, ('Volcano 2 · Definition · 3m', '=Example · 2m@0'), sums((0, 3), (0, 2))),
      fixed('Volcano 3', 5, ('Volcano 3 · Definition · 3m', '=Example · 2m@1'), sums((0, 3), (0, 2)))),
     '0-7', EV),
    ('(ii)', 24, L(16, '(ii) Explain in detail how volcanoes occur.'),
     S(14, 'Explanation 8 SRP', 'Total 40m'),
     (srp3('Explanation', 8, 'Explanation 8 SRP’s @ 3m each · 24m'),), '0-7', EV + PS),
])
PART_TWO.append(T(
    'p2-3c', P2, '3C', '', 30, 16, L(16, 'Human Interaction with Surface Processes'),
    (L(16, 'Examine how humans interact with one of the following surface processes:', 'Mass movement processes.'),),
    (S(15, 'Interaction named', 'Total 30m'),),
    (fixed('Interaction named', 3, 'Interaction named · 3m'),
     srp3('Examination', 9, 'Examination 9 SRP’s @ 3m each · 27m')),
    '0-6', RIVERS, ID + 'p2-q3c-river-processes',
    routes=bullet_routes('p2-q3c-', SURFACE, atlas=dict(zip(SURFACE, (RIVERS, SEA, RW))))))

PART_TWO.append(T(
    'p2-4a', P2, '4A', '', 30, 17, L(17, 'Irish Region'),
    (L(17, 'Draw a sketch map of Ireland.', '(upland or lowland) in this region.'),),
    (S(16, 'Sketch map of Ireland outline', 'Total 30m'),),
    (fixed('Outline of Ireland', 6, 'Sketch map of Ireland outline · 6m graded (6/4/2/0)', (0, 2, 4, 6)),
     Criterion('Region', 6, NAMED_SHOWN, 'exact',
               ('Show and name 4 items @ 6m each:', 'Region named · 2m', 'Region shown · 4m graded (4/2/0)')),
     Criterion('Town/city', 6, NAMED_SHOWN, 'exact', ('Town/city named · 2m', 'Town/city shown · 4m graded (4/2/0)')),
     Criterion('River', 6, NAMED_SHOWN, 'exact', ('River named · 2m', 'River shown · 4m graded (4/2/0)')),
     Criterion('Area of relief', 6, NAMED_SHOWN, 'exact',
               ('Area of relief named · 2m', 'Area of relief shown · 4m graded (4/2/0)'))),
    '1-4', IRL, ID + 'p2-q4a'))
Q4BS = (L(17, 'Name a European region (not in Ireland), that you have studied and answer each of the',
          'following questions.'),)
PART_TWO += romans('4B', P2, 17, L(17, 'Tourism in a European Region'), Q4BS, ID + 'p2-q4b', (), [
    ('(i)', 4, L(17, '(i) Name two tourist attractions in this region.'),
     (S(17, 'Naming a region', '(i) · Name two'), S(17, 'One tourist attraction named @ 2m', '(ii) · Explain')),
     (fixed('Region named', 1, 'Naming a region · 1m'),
      fixed('Tourist attraction 1', 2, 'One tourist attraction named @ 2m'),
      fixed('Tourist attraction 2', 1, 'One tourist attraction named @ 1m · 3m')), '1-5', EURO),
    ('(ii)', 27, L(17, '(ii) Explain the reasons why tourists are attracted to this region.'),
     S(17, 'Explanation 9 SRP', '(iii) · Describe'), (srp3('Explanation', 9, 'Explanation 9 SRP’s @ 3m each · 27m'),),
     '1-5', EURO),
    ('(iii)', 9, L(17, '(iii) Describe one problem associated with tourism in this region.'),
     S(17, 'One problem 3 SRP', 'Total 40m'), (srp3('One problem', 3, 'One problem 3 SRP’s @ 3m each · 9m'),),
     '1-5', EURO),
])
PART_TWO.append(T(
    'p2-4c', P2, '4C', '', 30, 17, L(17, 'Urban Growth in a Continental / Sub-Continental Region'),
    (L(17, 'Describe and explain the reasons for the growth of any urban area in a', 'that you have studied.'),),
    (S(17, 'Naming an urban area', 'Total 30m'),),
    (fixed('Urban area named', 3, 'Naming an urban area · 3m'),
     srp3('Description and explanation', 9, 'Description and explanation 9 SRP’s @ 3m each · 27m')),
    '1-6', CONT + URB, ID + 'p2-q4c'))
Q5AS = (L(18, 'Examine the charts above and answer each of the following questions.'),)
PART_TWO += romans('5A', P2, 18, L(18, 'Types of Regions'), Q5AS, ID + 'p2-q5a', ('page',), [
    ('(i)', 6, L(18, '(i) Calculate X, the percentage of tertiary economic activity in Region B.'),
     S(18, 'X = 60%', '(ii) · Is Region'), (fixed('X', 6, 'X = 60% · 6m'),), '2-0', GRAPH),
    ('(ii)', 6, L(18, '(ii) Is Region B a Core or a Peripheral region?'),
     S(18, 'Core · 6m', '(iii) · Name an example'), (fixed('Core or peripheral', 6, 'Core · 6m'),), '1-0', IRL + EURO),
    ('(iii)', 6, L(18, '(iii) Name an example of a Core region and an example of a Peripheral region.'),
     S(18, 'Example of core region', '(iv) · Briefly'),
     (fixed('Core region', 3, 'Example of core region · 3m'),
      fixed('Peripheral region', 3, 'Example of peripheral region · 3m')), '1-0', IRL + EURO),
    ('(iv)', 6, L(18, '(iv) Briefly describe one characteristic of a Core region.'),
     S(18, 'Brief description 2 SRP', '(v) · Briefly', None, '(iv) · Briefly'),
     (srp3('Brief description', 2, 'Brief description 2 SRP’s @ 3m each · 6m'),), '1-0', IRL + EURO),
    ('(v)', 6, L(18, '(v) Briefly describe one characteristic of a Peripheral region.'),
     S(18, 'Brief description 2 SRP', 'Total 30m', None, '(v) · Briefly'),
     (srp3('Brief description', 2, 'Brief description 2 SRP’s @ 3m each · 6m'),), '1-0', IRL + EURO),
])
PART_TWO += [
    T('p2-5b', P2, '5B', '', 40, 18, L(18, 'Secondary Economic Activities – Irish Region'),
      (L(18, 'Discuss how any two of the following factors influence the development of',
         'Government and European Union Policies.'),),
      (S(18, 'Region named', 'Total 40m'),),
      (fixed('Region named', 1, 'Region named · 1m'),
       srp3('Factor 1 explained', 7, 'Factor 1 explained 7 SRP’s @ 3m each · 21m'),
       srp3('Factor 2 explained', 6, 'Factor 2 explained 6 SRP’s @ 3m each · 18m')),
      '1-4', IRL, ID + 'p2-q5b', absorbs=pool(ID + 'p2-q5b-', FACTORS_5B, 2)[1]),
    T('p2-5c', P2, '5C', '', 30, 18, L(18, 'Regional Development'),
      (L(18, 'Describe and explain two problems faced by any region that you have studied.'),),
      (S(19, 'Problem 1', 'Total 30m'),),
      (srp3('Problem 1', 5, ('Problem 1', '=Description and explanation 5 SRP’s @ 3m each · 15m@0')),
       srp3('Problem 2', 5, ('Problem 2', '=Description and explanation 5 SRP’s @ 3m each · 15m@1'))),
      '1-0', IRL + EURO, ID + 'p2-q5c'),
    T('p2-6a', P2, '6A', '', 30, 19, L(19, 'European Region'),
      (L(19, 'Draw a sketch map of a European region (not in Ireland) that you have studied.',
         '(upland or lowland).'),),
      (S(20, 'Sketch map of European region outline', 'Total 30m'),),
      (fixed('Outline of region', 6, 'Sketch map of European region outline · 6m graded (6/4/2/0)', (0, 2, 4, 6)),
       Criterion('Town/City 1', 6, NAMED_SHOWN, 'exact',
                 ('Show and name 4 items @ 6m each:', 'Town/City 1 · Named · 2m', f'={SHOWN}@0')),
       Criterion('Town/City 2', 6, NAMED_SHOWN, 'exact', ('Town /City 2 · Named · 2m', f'={SHOWN}@1')),
       Criterion('River', 6, NAMED_SHOWN, 'exact', ('River · Named · 2m', f'={SHOWN}@2')),
       Criterion('Area of relief', 6, NAMED_SHOWN, 'exact', ('Area of relief · Named · 2m', f'={SHOWN}@3'))),
      '1-5', EURO, ID + 'p2-q6a'),
    T('p2-6b', P2, '6B', '', 30, 19, L(19, 'European Union Expansion'),
      (L(19, 'Describe and explain the impacts of European Union expansion on Ireland.'),),
      (S(20, 'Description and explanation 10', 'Total 30m'),),
      (srp3('Description and explanation', 10, 'Description and explanation 10 SRP’s @ 3m each · 30m'),),
      '1-5', EURO + EU, ID + 'p2-q6b'),
]
Q6CS = (L(19, 'Name a Continental / Sub-Continental region (not in Europe), that you have studied',
          'following questions.'),)
Q6CI = L(19, '(i) Name one primary economic activity that contributes to the economy of this', 'region.')
PART_TWO += romans('6C', P2, 19, L(19, 'Primary Economic Activity in a Continental / Sub-Continental Region'), Q6CS,
                   ID + 'p2-q6c', (), [
    ('(i)', 4, Q6CI,
     (S(21, 'Naming a region', '(i) · Name one primary'), S(21, 'Primary economic activity named', '(ii) · Explain')),
     (fixed('Region named', 1, 'Naming a region · 1m'),
      fixed('Primary economic activity named', 3, 'Primary economic activity named · 3m')), '1-6', CONT),
    ('(ii)', 27, L(19, '(ii) Explain the advantages that this region has for the development of the primary',
                   'part (i) above.'),
     S(21, 'Advantages explained', '(iii) · Describe'),
     (srp3('Advantages explained', 9, 'Advantages explained 9 SRP’s @ 3m each · 27m'),), '1-6', CONT, (), (Q6CI,)),
    ('(iii)', 9, L(19, '(iii) Describe one problem faced by this primary economic activity in this region.'),
     S(21, 'One problem described', 'Total 40m'),
     (srp3('One problem described', 3, 'One problem described 3 SRP’s @ 3m each · 9m'),), '1-6', CONT, (), (Q6CI,)),
])

PART_TWO.append(sketch(
    21, L(21, 'Aerial Photograph'),
    L(21, 'Examine the aerial photograph of Kenmare accompanying this paper.', 'An area of waste ground.'),
    23, ID + 'p2-q7a', '2-8', AER + ECON, ('aerial',), 'Showing · 3 marks graded (3/1/0)', (0, 1, 3),
    'Labelled · 2 marks',
    ('An area of agricultural land', 'Two connecting streets', 'A roundabout', 'A car park',
     'An area of waste ground.')))
PART_TWO += romans('7B', P2, 21, L(21, 'European Union Policy'), (), ID + 'p2-q7b', (), [
    ('(i)', 20, L(21, '(i) Examine the positive impacts of European Union policy/policies on Ireland.'),
     S(24, 'Impact named', '(ii) · Examine the negative', None, '(i) · Examine the positive'),
     (fixed('Impact named', 2, 'Impact named · 2m'),
      srp3('Positive impacts examined', 6, 'Positive impacts examined 6 SRP’s @ 3m each · 18m')), '3-3', EU),
    ('(ii)', 20, L(21, '(ii) Examine the negative impacts of European Union policy/policies on Ireland.'),
     S(24, 'Impact named', 'Total 40m', None, '(ii) · Examine the negative'),
     (fixed('Impact named', 2, 'Impact named · 2m'),
      srp3('Negative impacts examined', 6, 'Negative impacts examined 6 SRP’s @ 3m each · 18m')), '3-3', EU),
])
Q7CI = L(21, '(i) Name one developing economy that was colonised.')
PART_TWO += romans('7C', P2, 21, L(21, 'Colonialism'), (), ID + 'p2-q7c', (), [
    ('(i)', 3, Q7CI, S(24, 'Named developing economy', '(ii) · Describe'),
     (fixed('Developing economy named', 3, 'Named developing economy · 3m'),), '3-1', DEV),
    ('(ii)', 27, L(21, '(ii) Describe and explain the effects of colonialism on this developing economy.'),
     S(24, 'Description and explanation 9', 'Total 30m'),
     (srp3('Description and explanation', 9, 'Description and explanation 9 SRP’s @ 3m each · 27m'),), '3-1', DEV,
     (), (Q7CI,)),
])
Q8AS = (L(22, 'Examine the charts above and answer each of the following questions.'),)
PART_TWO += romans('8A', P2, 22, L(22, 'Energy', nth=0), Q8AS, ID + 'p2-q8a', ('page',), [
    ('(i)', 6, L(22, '(i) Calculate X, the percentage of energy produced by gas in 2010.'),
     S(25, 'X = 20%', '(ii) · Which fuel'), (fixed('X', 6, 'X = 20% · 6m'),), '2-0', GRAPH),
    ('(ii)', 6, L(22, '(ii) Which fuel increased its energy production the most between 1995 and 2010?'),
     S(25, 'Renewables · 6m', '(iii) · Explain briefly'), (fixed('Fuel', 6, 'Renewables · 6m'),), '2-0', GRAPH),
    ('(iii)', 6, L(22, '(iii) Explain briefly why energy production using this fuel type increased.'),
     S(25, 'Brief explanation 2 SRP', '(iv) · Name two'), (srp3('Brief explanation', 2, BRIEF),), '3-5', ECON),
    ('(iv)', 6, L(22, '(iv) Name two sources of renewable energy.'),
     S(25, 'Two named sources', '(v) · State two'),
     (fixed('Two sources', 6, 'Two named sources @ 3m each · 6m', (0, 3, 6)),), '3-5', ECON),
    ('(v)', 6, L(22, '(v) State two effects of burning fossil fuels on the environment.'),
     S(25, 'Two effects stated', 'Total 30m'),
     (fixed('Two effects', 6, 'Two effects stated @ 3m each · 6m', (0, 3, 6)),), '3-4', ENV),
])
Q8BI = L(22, '(i) Name one multinational company located in Ireland.')
PART_TWO += romans('8B', P2, 22, L(22, 'Multinational Company (MNC)'), (), ID + 'p2-q8b', (), [
    ('(i)', 4, Q8BI, S(25, 'Named MNC', '(ii) · Name one product'), (fixed('MNC named', 4, 'Named MNC · 4m'),),
     '3-2', MNC),
    ('(ii)', 8, L(22, '(ii) Name one product manufactured by this multinational company and name one',
                  'where this product is sold.'),
     S(25, 'Product named', '(iii) · State where'),
     (fixed('Product named', 4, 'Product named · 4m'), fixed('Country named', 4, 'Country named · 4m')),
     '3-2', MNC, (), (Q8BI,)),
    ('(iii)', 28, L(22, '(iii) State where this multinational company is located in Ireland and explain in detail',
                    'at this location.'),
     S(25, 'Location stated', 'Total 40m'),
     (fixed('Location stated', 4, 'Location stated · 4m'), srp3('Explanation', 8, 'Explanation 8 SRP’s @ 3m each · 24m')),
     '3-2', MNC, (), (Q8BI,)),
])
PART_TWO.append(T(
    'p2-8c', P2, '8C', '', 30, 22, L(22, 'Economic Development – Developed Economy'),
    (L(22, 'Describe and explain the development of one of the following with reference to a',
       'Service and footloose industries.'),),
    (S(26, 'Named developed economy', 'Total 30m'),),
    (fixed('Developed economy named', 3, 'Named developed economy · 3m'),
     srp3('Description and explanation', 9, 'Description and explanation 9 SRP’s @ 3m each · 27m')),
    '3-0', ECON, ID + 'p2-q8c-tourism', routes=bullet_routes('p2-q8c-', DEVELOPED)))
Q9AS = (L(23, 'Examine the table above showing the Human Development Index (HDI) for a number of',
          'countries.'),)
PART_TWO += romans('9A', P2, 23, L(23, 'Economic Development', nth=0), Q9AS, ID + 'p2-q9a', ('page',), [
    ('(i)', 24, L(23, '(i) Using graph paper, draw a suitable graph to illustrate this data.'),
     S(27, 'Graph paper', '(ii) · In your answer book'), GRAPH_OL, '2-0', GRAPH),
    ('(ii)', 6, L(23, '(ii) In your answer book, explain briefly one reason why some countries have a high',
                  'human development index.'),
     S(27, 'Brief explanation 2 SRPs', 'Total 30m'),
     (srp3('Brief explanation', 2, 'Brief explanation 2 SRPs @ 3m each · 6m'),), '3-0', ECON + DEV),
])
Q9CS = (L(23, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper.'),)
Q9CI = L(23, '(i) State clearly, using a six-figure grid reference, where you would locate a',
         'pharmaceutical company.')
PART_TWO.append(T(
    'p2-9b', P2, '9B', '', 30, 23, L(23, 'Environmental Impact'),
    (L(23, 'Describe and explain how economic activities impact on the environment, with reference',
       'that you have studied.'),),
    (S(27, 'Examples named', 'Total 30m'),),
    (fixed('Examples named', 6, 'Examples named · 3m + 3m', (0, 3, 6)),
     srp3('Description and explanation', 8, 'Description and explanation 8 SRP’s @ 3m each · 24m')),
    '3-4', ENV, ID + 'p2-q9b'))
PART_TWO += romans('9C', P2, 23, L(23, 'Economic Activity and Conflict'), Q9CS, ID + 'p2-q9c', ('map', 'legend'), [
    ('(i)', 4, Q9CI, S(28, 'Six figure grid reference', '(ii) · Using evidence'),
     (fixed('Six-figure grid reference', 4, 'Six figure grid reference · 4m graded (4/2/0)', (0, 2, 4)),),
     '2-6', MAP + ECON),
    ('(ii)', 24, L(23, '(ii) Using evidence from the Ordnance Survey map, explain why you selected this',
                   'location.'),
     S(28, 'Map evidence', '(iii) · Describe'),
     (fixed('Map evidence', 3, 'Map evidence · 3m'), srp3('Explanation', 7, 'Explanation 7 SRP’s @ 3m each · 21m')),
     '3-2', MNC + MAP, (), (Q9CI,)),
    ('(iii)', 12, L(23, '(iii) Describe how conflict may arise as a result of locating the pharmaceutical',
                    'company in this area.'),
     S(28, 'Description 4 SRP', 'Total 40m'),
     (srp3('Description', 4, 'Description 4 SRP’s @ 3m each · 12m'),), '3-4', ENV + MAP, (), (Q9CI,)),
])

Q10AS = (L(24, 'Examine the table above showing Ireland’s population by age group in 2014.'),)
PART_TWO += romans('10A', P2, 24, L(24, 'Irish Population', nth=0), Q10AS, ID + 'p2-q10a', ('page',), [
    ('(i)', 24, L(24, '(i) Using graph paper, draw a suitable graph to illustrate this data.'),
     S(29, 'Graph paper', '(ii) · In your answer book'), GRAPH_OL, '2-0', GRAPH),
    ('(ii)', 6, L(24, '(ii) In your answer book, state two ways that population statistics are used.'),
     S(29, '2 ways stated', 'Total 30m'), (fixed('Two ways', 6, '2 ways stated @ 3m each · 6m', (0, 3, 6)),),
     '4-0', POP),
])
Q10BS = (L(24, 'Migration takes place due to push factors and pull factors.'),)
PART_TWO += romans('10B', P2, 24, L(24, 'Migration', nth=0), Q10BS, ID + 'p2-q10b', (), [
    ('(i)', 4, L(24, '(i) Name one push factor and one pull factor associated with migration.'),
     S(30, 'Push factor named', '(ii) · Describe'),
     (fixed('Push factor named', 2, 'Push factor named · 2m'), fixed('Pull factor named', 2, 'Pull factor named · 2m')),
     '4-2', POP),
    ('(ii)', 18, L(24, '(ii) Describe and explain the positive impacts of migration on Ireland.'),
     S(30, 'Impact named', '(iii) · Describe', None, '(ii) · Describe'),
     (fixed('Impact named', 3, 'Impact named · 3m'),
      srp3('Description and explanation', 5, 'Description and explanation 5 SRP’s @ 3m each · 15m')), '4-2', POP),
    ('(iii)', 18, L(24, '(iii) Describe and explain the negative impacts of migration on Ireland.'),
     S(30, 'Impact named', 'Total 40m', None, '(iii) · Describe'),
     (fixed('Impact named', 3, 'Impact named · 3m'),
      srp3('Description and explanation', 5, 'Description and explanation 5 SRP’s @ 3m each · 15m')), '4-2', POP),
])
TOWN_REASON = ('Three reasons @ 10m each', 'For each reason:', 'Map evidence · 1m',
               'Explanation 3 SRP’s @ 3m each · 9m')
PART_TWO.append(T(
    'p2-10c', P2, '10C', '', 30, 24, L(24, 'Development of Urban Settlements'),
    (L(24, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper.'),
     L(24, 'Explain three reasons why the town of Kenmare developed at this location', 'support each reason.')),
    (S(30, 'Three reasons @ 10m each', 'Total 30m'),),
    tuple(Criterion(f'Reason {n}', 10, sums((0, 1), steps(9, 3)), 'srp', TOWN_REASON) for n in (1, 2, 3)),
    '4-3', URB + MAP, ID + 'p2-q10c', ('map', 'legend')))
PART_TWO.append(sketch(
    25, L(25, 'Ordnance Survey Map - Historic Settlement'),
    L(25, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper.',
      'historic settlement evident on the map.'),
    31, ID + 'p2-q11a', '2-6', MAP + URB, ('map', 'legend'), 'Showing · 3m graded (3/1/0)', (0, 1, 3), 'Naming · 2m',
    ('The built up area of Kenmare', 'Four different examples of historic settlement evident on the map.',
     'Four different examples of historic settlement evident on the map.',
     'Four different examples of historic settlement evident on the map.',
     'Four different examples of historic settlement evident on the map.')))
Q11BI = L(25, '(i) Name one city where traffic congestion is a problem.')
PART_TWO += romans('11B', P2, 25, L(25, 'Traffic in Urban Areas'), (), ID + 'p2-q11b', (), [
    ('(i)', 4, Q11BI, S(32, 'City named', '(ii) · Explain'), (fixed('City named', 4, 'City named · 4m'),), '4-5', URB),
    ('(ii)', 27, L(25, '(ii) Explain the reasons why traffic congestion occurs in this city.'),
     S(32, 'Explanation 9 SRP', '(iii) · Describe'), (srp3('Explanation', 9, 'Explanation 9 SRP’s @ 3m each · 27m'),),
     '4-5', URB, (), (Q11BI,)),
    ('(iii)', 9, L(25, '(iii) Describe one solution to traffic congestion.'),
     S(32, 'One solution described', 'Total 40m'),
     (srp3('One solution described', 3, 'One solution described 3 SRP’s @ 3m each · 9m'),), '4-5', URB),
])
PART_TWO.append(T(
    'p2-11c', P2, '11C', '', 30, 25, L(25, 'Population', nth=0),
    (L(25, '‘Birth rates are influenced by many factors', 'medical technology.’'),
     L(25, 'Describe and explain the factors that influence birth rates.')),
    (S(32, 'Factor named', 'Total 30m'),),
    (fixed('Factor named', 3, 'Factor named · 3m'),
     srp3('Description and explanation', 9, 'Description and explanation 9 SRP’s @ 3m each · 27m')),
    '4-0', POP, ID + 'p2-q11c'))
Q12AS = (L(26, 'Read the article above and answer each of the following questions.'),)
PART_TWO += romans('12A', P2, 26, L(26, 'Population Growth'), Q12AS, ID + 'p2-q12a', ('page',), [
    ('(i)', 6, L(26, '(i) According to the article, what is the current size of the Earth’s population',
                 'population by 2100?'),
     S(33, 'Current 7.2', '(ii) · Calculate'),
     (fixed('Current population', 3, 'Current 7.2 billion · 3m'),
      fixed('Predicted population', 3, 'Predicted by 2100 12.3 billion · 3m')), '4-0', POP),
    ('(ii)', 6, L(26, '(ii) Calculate the predicted increase in the Earth’s population by 2100.'),
     S(33, '5.1 billion', '(iii) · Name one'), (fixed('Increase', 6, '5.1 billion · 6m'),), '4-0', POP + GRAPH),
    ('(iii)', 3, L(26, '(iii) Name one problem mentioned in the article that could be made worse by this',
                   'increase in population.'),
     S(33, 'One problem named', '(iv) · Where'), (fixed('Problem', 3, 'One problem named · 3m'),), '4-1', POP),
    ('(iv)', 3, L(26, '(iv) Where is most of the population growth expected to take place?'),
     S(33, 'Africa · 3m', '(v) · Explain'), (fixed('Area', 3, 'Africa · 3m'),), '4-0', POP),
    ('(v)', 6, L(26, '(v) Explain briefly why this area is predicted to have the most growth in population.'),
     S(33, 'Brief explanation 2 SRP', '(vi) · Explain', None, '(v) · Explain'),
     (srp3('Brief explanation', 2, 'Brief explanation 2 SRP’s · 3m + 3m'),), '4-0', POP),
    ('(vi)', 6, L(26, '(vi) Explain briefly one advantage of predicting population figures.'),
     S(33, 'Brief explanation 2 SRP', 'Total 30m', None, '(vi) · Explain'),
     (srp3('Brief explanation', 2, 'Brief explanation 2 SRP’s · 3m + 3m'),), '4-0', POP),
])
Q12BI = L(26, '(i) Name one city in the developing world.')
PART_TWO += romans('12B', P2, 26, L(26, 'Developing World City'), (), ID + 'p2-q12b', (), [
    ('(i)', 3, Q12BI, S(33, 'Developing world city named', '(ii) · Describe'),
     (fixed('Developing world city named', 3, 'Developing world city named · 3m'),), '4-5', URB),
    ('(ii)', 27, L(26, '(ii) Describe and explain reasons for the rapid growth of this city.'),
     S(33, 'Description and explanation 9', 'Total 30m', None, 'B. · Developing'),
     (srp3('Description and explanation', 9, 'Description and explanation 9 SRP’s @ 3m each · 27m'),), '4-5', URB,
     (), (Q12BI,)),
])
Q12CS = (L(26, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper and answer',
           'following questions.'),)
PART_TWO += romans('12C', P2, 26, L(26, 'Population Density and Distribution'), Q12CS, ID + 'p2-q12c',
                   ('map', 'legend'), [
    ('(i)', 2, L(26, '(i) Give a four-figure grid reference for an area on the map where there is an',
                 'absence of settlement.'),
     S(34, 'Grid reference', '(ii) · Explain', None, '(i) · Give'),
     (fixed('Grid reference', 2, 'Grid reference · 2m graded (2/1/0)', (0, 1, 2)),), '4-0', POP + MAP),
    ('(ii)', 18, L(26, '(ii) Explain in detail, using map evidence, why there is an absence of settlement at',
                   'this location.'),
     S(34, 'Map evidence', '(iii) · Give', None, '(ii) · Explain'),
     (fixed('Map evidence', 3, 'Map evidence · 3m'), srp3('Explanation', 5, 'Explanation 5 SRP’s @ 3m each · 15m')),
     '4-0', POP + MAP),
    ('(iii)', 2, L(26, '(iii) Give a four-figure grid reference for an area on the map which has a relatively',
                   'high population density.'),
     S(34, 'Grid reference', '(iv) · Explain', None, '(iii) · Give'),
     (fixed('Grid reference', 2, 'Grid reference · 2m graded (2/1/0)', (0, 1, 2)),), '4-0', POP + MAP),
    ('(iv)', 18, L(26, '(iv) Explain in detail, using map evidence, why there is a relatively high population',
                   'density at this location.'),
     S(34, 'Map evidence', 'Total 40m', None, '(iv) · Explain'),
     (fixed('Map evidence', 3, 'Map evidence · 3m'), srp3('Explanation', 5, 'Explanation 5 SRP’s @ 3m each · 15m')),
     '4-0', POP + MAP),
])

TASKS = [*PART_ONE, *PART_TWO]

ID_CORRECTION_REASON = 'No 2015 Ordinary card shipped before this review; every card is new.'

# No 2015 Ordinary card was live on origin/main before this review.
LEGACY_IDS: list[str] = []
