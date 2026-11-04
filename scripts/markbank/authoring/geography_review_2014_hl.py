"""Independent review ledger: Leaving Certificate Geography 2014 Higher Level.

Sources (English editions, harvested Paper Trail corpus; sizes and SHA-256
pinned in EXPECTED_SOURCES and the generated audit): the examination paper
LC005ALP000EV (32 pages; one booklet printed Part One, answered in it, and
Part Two), marking scheme LC005ALP000EV (48 pages), and the common Dungarvan
companions as Paper Trail files them — the 1:50 000 map LC005CLP003EV (eight
stacked image strips that render as one page), its legend LC005CLPC00EV and
the aerial photograph LC005CLP004EV (one-page PDFs). Part One is 80 marks
(any ten of twelve @ 8), Part Two 320 (four questions @ 80).

Visual sweep (every page rendered and read on 2026-10-23):
  Paper p1 cover and examiner's grid; p2-p12 Part One Questions 1-12 (p8
  holds Q7 and Q8; Q2 prints an OS map extract, Q9 a map of the Canary
  Islands and its elevation profile); p13 Part Two instructions; p14
  Section 1 divider; p15-p20 Q1-Q6 (p15 and p18 open with their dividers);
  p21 Section 2 divider; p22-p28 Electives Q7-Q12 (p22 and p25 open with
  their elective dividers; p26 holds 11A and 11B, p27 11C and its Central
  Place Theory diagram); p29 Section 3 divider and option note; p30-p31
  Options Q13-Q24; p32 printed "Blank Page".
  Scheme p1 cover; p2 note on marking schemes; p3 introduction; p4 Part One
  table (a centred tariff heading, then two columns: Q1-Q5, Q6-Q12; the
  answer lines print no marks); p5 Part Two instructions and Section 1
  divider; p6-p10 Q1-Q2; p11-p12 Q3; p13-p18 Q4-Q6; p19 Section 2 divider;
  p20-p25 Q7-Q9; p26-p31 Q10-Q12; p32 Section 3 divider; p33 option outline
  and Overall Coherence descriptors; p34-p41 Q13-Q24; p42-p44 Geographical
  Investigation (coursework) and its presentation marks; p45 investigation
  topics; p46 Irish-language bonus marks; p47 printed "Blank Page"; p48
  back cover. The scheme reprints each Part Two question above its
  allocation; every slice starts at the allocation.
  Companions: Dungarvan map extract (the Colligan River, the Cunnigar sand
  spit, Dungarvan Harbour); OS legend sheet; oblique aerial photograph of
  Dungarvan.

The scheme sets its note bullets in Wingdings, and its ToUnicode map reads
the arrowhead (glyph 190) as "¾"; geography_review repairs it from the glyph
id (glyphmap-geography.json, derived by geography_glyphs.py), so the notes
read "•" as in every other sitting.

Part One prices every question in one heading: "Each question: 4 parts @ 2
marks each or 8 parts @ 1 mark each" and "Q4(iv), Q9(iv), Q11(iv) & Q12(iv)
@ 1 + 1 mark", so every Part One card carries the heading line that prices
it with its answer lines. Q4(ii) is printed "Award 2m (ambiguous wording)":
that line is its guidance. Matching tables, in the printed row order: Q1
Groyne B Human, Offshore bar A Natural, Rock armour D Human, Cliff C
Natural; Q2 U-shaped valley D Glacial, Meander A Fluvial, Arête B Glacial,
V-shaped valley C Fluvial; Q3 Joint D, Syncline G, Volcano A, Coastal
deposits C, Bedding plane E, Magma chamber H, Weathering B, Anticline F; Q6
Urban Berlin Germany, Climate Mediterranean Southern Europe, Administrative
County Meath Ireland, Cultural Basque Lands Northern Spain (Geomorphological
is printed); Q10 Dendritic C, Deranged D, Trellis B, Radial A. Q1, Q2 and Q6
answer each printed row twice (a letter and a tick, or two cells) and are
one card of two-mark rows; Q3 and Q10 are one card each. Q5 prices its
three romans separately at one mark per answer.

Printed choices: 2B (i) or (ii) is two routes; 1C, 7C and 12C (one of
three printed options) are one route per option; 6C (any two of three
factors) and 8B (any two of three) are pools, one card each. 5B's "any
two contrasting European regions" prints no pool and stays open.
"""

from geography_review import (
    Criterion, Lift, Route, SchemeSlice, Task, pool, evens, fixed, slug, srp, sums, upto,
)

YEAR = 2014
LEVEL = 'higher'
PAPER_PAGES = {1: 32, 2: 32}
SCHEME_PAGES = 48
QUESTION_TARIFFS = {1: {str(n): 8 for n in range(1, 13)},
                    2: {**{f'{n}{x}': (20 if x == 'A' else 30)
                           for n in range(1, 13) for x in 'ABC'},
                        **{str(n): 80 for n in range(13, 25)}}}

EXPECTED_SOURCES = {
    'paper1': ('LC005ALP000EV.pdf', 1649594),
    'paper2': ('LC005ALP000EV.pdf', 1649594),
    'scheme': ('LC005ALP000EV.pdf', 456897),
    'map': ('LC005CLP003EV.pdf', 4043493),
    'legend': ('LC005CLPC00EV.pdf', 587436),
    'aerial': ('LC005CLP004EV.pdf', 2196383),
}

_PAPER = {1: 'cover and examiner grid', **{p: 'question' for p in range(2, 13)},
          13: 'Part Two instructions', 14: 'section divider', **{p: 'question' for p in range(15, 21)},
          21: 'section divider', **{p: 'question' for p in range(22, 29)}, 29: 'section divider and option note',
          30: 'question', 31: 'question', 32: 'blank page'}
PAGE_REVIEW = {
    # One booklet printed both parts.
    'paper1': _PAPER, 'paper2': _PAPER,
    'scheme': {1: 'cover', 2: 'notes', 3: 'notes', 4: 'Part One table',
               5: 'Part Two instructions and section divider',
               **{p: 'Part Two allocation' for p in range(6, 19)}, 19: 'section divider',
               **{p: 'Part Two allocation' for p in range(20, 32)}, 32: 'section divider',
               33: 'option outline and coherence descriptors',
               **{p: 'option allocation' for p in range(34, 42)},
               **{p: 'geographical investigation (coursework)' for p in range(42, 45)},
               45: 'investigation topics', 46: 'Irish-language bonus marks', 47: 'blank', 48: 'back cover'},
}

EXPECTED_SELECTION_SCAN = [
    [1, 2, 'attempt ten'], [1, 13, 'attempt four'], [1, 14, 'attempt two'], [1, 15, 'attempt one'],
    [1, 15, 'one of the following'], [1, 16, 'answer (i) or (ii)'], [1, 18, 'attempt one'],
    [1, 19, 'any two'], [1, 20, 'any two'], [1, 21, 'attempt one'], [1, 22, 'one of the following'],
    [1, 23, 'any two'], [1, 28, 'one of the following'], [1, 29, 'attempt one'],
]
SELECTION_REVIEW = [
    {'scan': [[1, 2, 'attempt ten'], [1, 13, 'attempt four'], [1, 14, 'attempt two'], [1, 15, 'attempt one'],
              [1, 18, 'attempt one'], [1, 21, 'attempt one'], [1, 29, 'attempt one']],
     'kind': 'exam-attempt-rule',
     'reason': 'Part One any ten of twelve and Part Two four questions (one of Q1-3, one of Q4-6, one elective, one option) are attempt rules; every question is carded.'},
    {'scan': [[1, 16, 'answer (i) or (ii)']], 'kind': 'closed-route',
     'reason': '2B: (i) or (ii) -> two routes, each with its own scheme allocation.'},
    {'scan': [[1, 15, 'one of the following'], [1, 22, 'one of the following'], [1, 28, 'one of the following']],
     'kind': 'closed-choose-one',
     'reason': '1C one of three human impacts on surface processes, 7C one of three activities, 12C one of three influences on population growth -> 3 routes each.'},
    {'scan': [[1, 20, 'any two'], [1, 23, 'any two']], 'kind': 'choose-n-one-card',
     'reason': '6C any two of three printed factors and 8B any two of three printed aspects of a multinational -> one card each with every printed item (choice is not a route).'},
    {'scan': [[1, 19, 'any two']], 'kind': 'open-response',
     'reason': '5B any two contrasting European regions prints no pool. Compulsory lists stay whole: 1A, 4A, 8A, 10A each item.'},
]

P1, P2 = 1, 2
LEFT = (0.0, 0.32, 0.472, 1.0)
RIGHT = (0.472, 0.32, 1.0, 1.0)
ID = 'geography-2014-hl-'
H = 'geography-higher-'
SRPS = 'SRPs'
EACH = '4 parts @ 2 marks each or 8 parts @ 1 mark each'
ONE1 = 'Q4(iv), Q9(iv), Q11(iv) & Q12(iv) @ 1 + 1 mark'


def L(page, start, end=None, nth=None):
    return Lift(page, start, end, None, nth)


def S(page, start, end=None, clip=None, after=None, table=False):
    return SchemeSlice(page, start, end, clip, after, table)


# The Part One heading lines that price each question.
HEAD = S(4, EACH, 'Q4(iv), Q9(iv)')
HEAD11 = S(4, ONE1, 'No grading')


def T(key, part, q, sub, marks, page, title, prompt, scheme, criteria, topic, atlas, card_id,
      sources=(), stem=(), routes=(), row_labels=(), absorbs=()):
    return Task(key, part, q, sub, marks, page, title, prompt, scheme, criteria, topic, atlas,
                sources, card_id, False, stem=stem, routes=routes, row_labels=row_labels,
                absorbs=absorbs)


def priced_rows(lines, marks, permitted=None, labels=None):
    """Rows of a Part One table; the first carries the heading that prices them."""
    return tuple(fixed(labels[i - 1] if labels else f'Row {i}', marks,
                       (EACH, line) if i == 1 else line, permitted)
                 for i, line in enumerate(lines, 1))


def answer(label, tariff, line, marks=2, permitted=None):
    lines = (tariff, *line) if isinstance(line, tuple) else (tariff, line)
    return (fixed(label, marks, lines, permitted),)


def pair(line, label):
    return fixed(label, 4, line, (0, 2, 4))


def split(label, total, first, second):
    return srp(label, total, (first, second))


def romans(q, part, page, title, stem, first_id, sources, parts):
    """parts: (sub, marks, prompt Lift(s), scheme slice(s), criteria, topic, atlas[, row labels[, extra stem]])."""
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


def choose_one(prefix, options):
    """One route per printed option: (printed item, id slug, topic, atlas)."""
    return tuple(Route(route_slug, item.rstrip('.'), ID + prefix + route_slug, False,
                       keep_bullets=(item,), topic=topic, atlas=atlas)
                 for item, route_slug, topic, atlas in options)


PS = (H + 'plate-tectonics',)
RW = (H + 'rocks-weathering-mass-movement',)
RIVERS = (H + 'rivers',)
SEA = (H + 'the-sea',)
GLAC = (H + 'glaciation',)
EV = (H + 'earthquakes-volcanoes',)
KARST = (H + 'karst-regions',)
MAP = (H + 'mapwork',)
AER = (H + 'aerial-photos',)
TG = (H + 'tablesgraphs-questions',)
WX = (H + 'weather-climate',)
IRL = (H + 'regions-ireland',)
EURO = (H + 'regions-european',)
CONT = (H + 'regions-continental',)
POP = (H + 'human-population',)
URB = (H + 'human-urban-geography',)
ECON = (H + 'elective-economic',)
DEV = (H + 'economic-developing-economies',)
MNC = (H + 'economic-multinationals-globalisation',)
EU_ECON = (H + 'economic-european-union',)
ENERGY = (H + 'economic-energy',)
ENV = (H + 'economic-environmental-impact',)

# ---------------------------------------------------------------- Part One --
PART_ONE = [
    T('p1-1', P1, '1', '', 8, 2, L(2, 'Coastal Features'),
      (L(2, '(i) Match each of the letters A, B, C and D with the feature', 'in the table below.'),
       L(2, '(ii) Indicate whether each of the features is a natural or human feature',
         'correct box in the table below.')),
      (HEAD, S(4, 'Q.1 B Human', 'Q.2', LEFT)),
      priced_rows(['Q.1 B Human', 'A Natural', 'D Human', 'C Natural'], 2, (0, 1, 2)),
      '0-10', SEA, ID + 'p1-q1', ('page',),
      (L(2, 'Examine the photograph above and answer each of the following questions.'),),
      row_labels=(L(2, 'Groyne'), L(2, 'Offshore bar'), L(2, 'Rock armour'), L(2, 'Cliff'))),
    T('p1-2', P1, '2', '', 8, 3, L(3, 'Glacial and Fluvial Landforms'),
      (L(3, '(i) Match each of the letters A, B, C and D with the landform', 'in the table below.'),
       L(3, '(ii) Indicate whether glacial processes or fluvial processes are most associated',
         'in the table below.')),
      (HEAD, S(4, 'Q.2 D Glacial processes', 'Q.3', LEFT)),
      priced_rows(['Q.2 D Glacial processes', 'A Fluvial processes', 'B Glacial processes',
                   'C Fluvial processes'], 2, (0, 1, 2)),
      '0-11', GLAC + RIVERS + MAP, ID + 'p1-q2', ('page',),
      (L(3, 'Examine the Ordnance Survey map extract above.'),),
      row_labels=(L(3, 'U-shaped valley'), L(3, 'Meander'), L(3, 'Arête'), L(3, 'V-shaped valley'))),
    T('p1-3', P1, '3', '', 8, 4, L(4, 'Patterns and Processes in the Physical Environment'),
      (L(4, 'Match each of the letters A, B, C, D, E, F, G and H with the feature or process',
         'in the table below.'),),
      (HEAD, S(4, 'Q.3 D Joint', 'Q.4', LEFT)),
      priced_rows(['Q.3 D Joint', 'G Syncline', 'A Volcano', 'C Coastal deposits', 'E Bedding plane',
                   'H Magma chamber', 'B Weathering', 'F Anticline'], 1),
      '0-1', RW + EV + SEA, ID + 'p1-q3', ('page',), (L(4, 'Examine the diagram above.'),),
      row_labels=(L(4, 'Joint'), L(4, 'Syncline'), L(4, 'Volcano'), L(4, 'Coastal deposits'),
                  L(4, 'Bedding plane'), L(4, 'Magma chamber'), L(4, 'Weathering'), L(4, 'Anticline'))),
]
PART_ONE += romans('4', P1, 5, L(5, 'Weather'),
                   (L(5, 'Examine the map above and answer each of the following questions.'),),
                   ID + 'p1-q4', ('page',), [
    ('(i)', 2, L(5, '(i) What is the mean daily temperature at A?'),
     (HEAD, S(4, 'Q.4 (i) 6°C', '(ii) Award', LEFT)), answer('Temperature', EACH, 'Q.4 (i) 6°C'), '2-7', WX),
    ('(ii)', 2, L(5, '(ii) Calculate the approximate mean daily temperature range in Co. Kerry.'),
     (HEAD, S(4, '(ii) Award 2m', '(iii) Isotherms', LEFT)),
     answer('Temperature range', EACH, '(ii) Award 2m (ambiguous wording)'), '2-7', WX),
    ('(iii)', 2, L(5, '(iii) What is the name given to lines on a weather map that join places of equal',
                   'temperature?'),
     (HEAD, S(4, '(iii) Isotherms', '(iv) Any valid explanation', LEFT)),
     answer('Name of the lines', EACH, '(iii) Isotherms'), '2-7', WX),
    ('(iv)', 2, L(5, '(iv) Explain briefly why temperatures in the west of Ireland are usually higher',
                  'in January.'),
     (HEAD11, S(4, '(iv) Any valid explanation', 'Q.5', LEFT)),
     answer('Explanation', ONE1, '(iv) Any valid explanation', 2, (0, 1, 2)), '2-7', WX),
])
PART_ONE += romans('5', P1, 6, L(6, 'Plate Tectonics'),
                   (L(6, 'Examine the map above and answer each of the following questions.'),),
                   ID + 'p1-q5', ('page',), [
    ('(i)', 4, L(6, '(i) Name each of the plates A, B, C and D.'),
     (HEAD, S(4, 'Q.5 (i) A North American', '(ii) E Constructive', LEFT)),
     priced_rows(['Q.5 (i) A North American', 'B Eurasian', 'C African', 'D South American'], 1,
                 labels=('Plate A', 'Plate B', 'Plate C', 'Plate D')), '0-0', PS),
    ('(ii)', 2, L(6, '(ii) Name the type of plate boundary at E and at F.'),
     (HEAD, S(4, '(ii) E Constructive', '(iii) True', LEFT)),
     (fixed('Boundary at E', 1, (EACH, '(ii) E Constructive/Diverging')),
      fixed('Boundary at F', 1, ('F Conservative /Neutral', 'Passive / Transform, etc'))), '0-0', PS),
    ('(iii)', 2, (L(6, '(iii) Circle the correct option in each of the following statements.'),
                  L(6, 'Volcanic mountains are formed at E.'), L(6, 'Fold mountains are formed at G.')),
     (HEAD, S(4, '(iii) True', 'Pag', LEFT)),
     (fixed('Statement 1', 1, (EACH, '(iii) True')), fixed('Statement 2', 1, '=True')), '0-0', PS + EV,
     (L(6, 'Volcanic mountains are formed at E.'), L(6, 'Fold mountains are formed at G.'))),
])
PART_ONE.append(T(
    'p1-6', P1, '6', '', 8, 7, L(7, 'Regions'),
    (L(7, 'The table below contains information on regions', 'One row of the table is completed for you.'),),
    (HEAD, S(4, 'Q.6 · Berlin', 'Q.7', RIGHT)),
    priced_rows(['Q.6 · Berlin Germany', 'Mediterranean Southern Europe', 'County Meath Ireland',
                 'Basque Lands Northern Spain'], 2, (0, 1, 2)),
    '1-0', IRL + EURO, ID + 'p1-q6', ('page',),
    row_labels=(L(7, 'Urban'), L(7, 'Climate'), L(7, 'Administrative'), L(7, 'Cultural'))))
PART_ONE += romans('7', P1, 8, L(8, 'Ordnance Survey Map', nth=0),
                   (L(8, 'Examine the 1:50 000 Ordnance Survey map and legend that accompany this paper and answer',
                      'following questions.'),),
                   ID + 'p1-q7', ('map', 'legend'), [
    ('(i)', 2, L(8, '(i) Give a six-figure grid reference for a mast shown on the Ordnance Survey map.'),
     (HEAD, S(4, 'Q.7 · (i) S 273 009', '(ii) 90 km2', RIGHT)),
     answer('Grid reference', EACH, 'Q.7 · (i) S 273 009'), '2-6', MAP),
    ('(ii)', 2, L(8, '(ii) Calculate the area of the Ordnance Survey map located in subzone X.'),
     (HEAD, S(4, '(ii) 90 km2', '(iii) North', RIGHT)), answer('Area', EACH, '(ii) 90 km2'), '2-6', MAP),
    ('(iii)', 2, L(8, '(iii) What is the aspect of the slope in grid box X 22 90?'),
     (HEAD, S(4, '(iii) North', '(iv) 6.8', RIGHT)),
     answer('Aspect', EACH, '(iii) North, North East, NNE'), '2-6', MAP),
    ('(iv)', 2, L(8, '(iv) Measure the straight line distance, in kilometres, from the 18 hole golf course',
                  'X 232 903.'),
     (HEAD, S(4, '(iv) 6.8', 'Q.8', RIGHT)), answer('Distance', EACH, '(iv) 6.8 (km)'), '2-6', MAP),
])
PART_ONE += romans('8', P1, 8, L(8, 'Aerial Photograph and Ordnance Survey Map'),
                   (L(8, 'Examine the aerial photograph, the 1:50 000 Ordnance Survey map and legend that',
                      'following questions.'),),
                   ID + 'p1-q8', ('aerial', 'map', 'legend'), [
    ('(i)', 2, L(8, '(i) Over which of the following points was the camera when the aerial photograph',
                 'X 255 930'),
     (HEAD, S(4, 'Q.8 · (i) X 255 930', '(ii) N25', RIGHT)),
     answer('Camera position', EACH, 'Q.8 · (i) X 255 930'), '2-8', AER + MAP),
    ('(ii)', 2, L(8, '(ii) Name the main road that passes through the large roundabout', 'aerial photograph.'),
     (HEAD, S(4, '(ii) N25', '(iii) Any valid statement', RIGHT)), answer('Road', EACH, '(ii) N25'),
     '2-8', AER + MAP),
    ('(iii)', 2, L(8, '(iii) State one way that the physical landscape impedes the development of Dungarvan',
                   'as a port.'),
     (HEAD, S(4, '(iii) Any valid statement', '(iv) Priory', RIGHT)),
     answer('Statement', EACH, '(iii) Any valid statement'), '4-3', URB + AER + MAP),
    ('(iv)', 2, L(8, '(iv) Name the religious antiquity in the right background of the aerial photograph.'),
     (HEAD, S(4, '(iv) Priory', 'Q.9', RIGHT)), answer('Religious antiquity', EACH, '(iv) Priory/Church'),
     '2-8', AER + MAP),
])
PART_ONE += romans('9', P1, 9, L(9, 'Map Skills'),
                   (L(9, 'The line X-Y on the map of the Canary Islands below indicates', 'is also shown.'),
                    L(9, 'Examine the map of the Canary Islands and the elevation profile X-Y',
                      'following questions.')),
                   ID + 'p1-q9', ('page',), [
    ('(i)', 2, L(9, '(i) Name the island at A on the elevation profile.'),
     (HEAD, S(4, 'Q.9 · (i) Gran Canaria', '(ii) 2,000m', RIGHT)),
     answer('Island', EACH, 'Q.9 · (i) Gran Canaria'), '2-6', MAP + TG),
    ('(ii)', 2, L(9, '(ii) What is the depth of the ocean at B on the elevation profile?'),
     (HEAD, S(4, '(ii) 2,000m', '(iii) 6,000m', RIGHT)), answer('Depth', EACH, '(ii) 2,000m'), '2-6', MAP + TG),
    ('(iii)', 2, L(9, '(iii) Calculate the difference in elevation between point C and point D on the profile,',
                   'to the nearest 1000 metres.'),
     (HEAD, S(4, '(iii) 6,000m', '(iv) Any valid explanation', RIGHT)),
     answer('Difference in elevation', EACH, '(iii) 6,000m'), '2-6', MAP + TG),
    ('(iv)', 2, L(9, '(iv) Briefly explain one economic advantage of living on a volcanic island.'),
     (HEAD11, S(4, '(iv) Any valid explanation', 'Q.10', RIGHT, 'Q.9')),
     answer('Explanation', ONE1, '(iv) Any valid explanation', 2, (0, 1, 2)), '0-7', EV),
])
PART_ONE.append(T(
    'p1-10', P1, '10', '', 8, 10, L(10, 'Pattern Recognition'),
    (L(10, 'Match each of the letters A, B, C and D with the correct drainage pattern', 'below.'),),
    (HEAD, S(4, 'Q.10 · C Dendritic', 'Q.11', RIGHT)),
    priced_rows(['Q.10 · C Dendritic', 'D Deranged', 'B Trellis', 'A Radial'], 2),
    '0-9', RIVERS, ID + 'p1-q10', ('page',),
    (L(10, 'Examine the diagrams above showing fluvial drainage patterns.'),),
    row_labels=(L(10, 'Dendritic'), L(10, 'Deranged'), L(10, 'Trellis'), L(10, 'Radial'))))
PART_ONE += romans('11', P1, 11, L(11, 'Statistical Interpretation'),
                   (L(11, 'Examine the table above which shows Irish population and migration estimates',
                      'following questions.'),),
                   ID + 'p1-q11', ('page',), [
    ('(i)', 2, L(11, '(i) What was the estimated increase in total population between April 2012 and',
                 'April 2013?'),
     (HEAD, S(4, 'Q.11 · (i) 7,700', '(ii) 10,500', RIGHT)), answer('Increase', EACH, 'Q.11 · (i) 7,700'),
     '2-0', TG + POP),
    ('(ii)', 2, L(11, '(ii) Calculate X, the estimated population change for year ending April 2012.'),
     (HEAD, S(4, '(ii) 10,500', '(iii) 40,800', RIGHT)), answer('X', EACH, '(ii) 10,500'), '2-0', TG + POP),
    ('(iii)', 2, L(11, '(iii) Calculate Y, the estimated natural increase for year ending April 2013.'),
     (HEAD, S(4, '(iii) 40,800', '(iv) Any valid explanation', RIGHT)), answer('Y', EACH, '(iii) 40,800'),
     '2-0', TG + POP),
    ('(iv)', 2, L(11, '(iv) Explain briefly what is meant by net migration.'),
     (HEAD11, S(4, '(iv) Any valid explanation', 'Q.12', RIGHT, 'Q.11')),
     answer('Explanation', ONE1, '(iv) Any valid explanation', 2, (0, 1, 2)), '4-2', POP),
])
PART_ONE += romans('12', P1, 12, L(12, 'Graphical Interpretation'),
                   (L(12, 'Examine the chart above which shows the consumption of renewable energy in the',
                      'following questions.'),),
                   ID + 'p1-q12', ('page',), [
    ('(i)', 2, L(12, '(i) What was the percentage of hydro power consumed?'),
     (HEAD, S(4, 'Q.12 · (i) 15.8', '(ii) 3.5', RIGHT)), answer('Percentage', EACH, 'Q.12 · (i) 15.8 (%)'),
     '2-0', TG + ENERGY),
    ('(ii)', 2, L(12, '(ii) Calculate X, the percentage of solar energy consumed.'),
     (HEAD, S(4, '(ii) 3.5', '(iii) 47.8', RIGHT)), answer('X', EACH, '(ii) 3.5 (%)'), '2-0', TG + ENERGY),
    ('(iii)', 2, L(12, '(iii) Calculate B, the percentage of biomass generated from wood and wood waste.'),
     (HEAD, S(4, '(iii) 47.8', '(iv) Any valid explanation', RIGHT, 'Q.12')),
     answer('B', EACH, '(iii) 47.8 (%)'), '2-0', TG + ENERGY),
    ('(iv)', 2, L(12, '(iv) Explain briefly what is meant by geothermal energy.'),
     (HEAD11, S(4, '(iv) Any valid explanation', 'ge 2 of 44', RIGHT, 'Q.12')),
     answer('Explanation', ONE1, '(iv) Any valid explanation', 2, (0, 1, 2)), '3-5', ENERGY),
])


# ---------------------------------------------------------------- Part Two --
def sketch(outline_line, outline_permitted, alloc, item_permitted, labels):
    return (fixed('Sketch outline' if 'Sketch' in outline_line else 'Map outline', 4,
                  outline_line, outline_permitted),
            *(Criterion(f'Feature {n}', 4, item_permitted, 'exact', alloc) for n in range(1, labels + 1)))


SHOWN3 = sums((0, 1, 3), (0, 1))
GRAPH = (fixed('Title', 2, ('Bar Chart · Pie Chart', 'Title · 2 marks · 2 marks')),
         fixed('Axes named (bar chart) / circle and centre (pie chart)', 2,
               ('Vertical axis named', 'Horizontal axis named'), (0, 1, 2)),
         fixed('6 items illustrated', 12, '6 items illustrated', upto(12)))
OS_SKETCH = sketch('Sketch Outline: · 4 marks', (0, 4),
                   ('4 features @ 4 marks each', 'Named 1 mark'), SHOWN3, 4)

PART_TWO = [
    T('p2-1a', P2, '1A', '', 20, 15, L(15, 'Ordnance Survey Map'),
      (L(15, 'Examine the 1:50 000 Ordnance Survey map and legend that accompany this paper.',
         'An area of land above 300 metres.'),),
      (S(6, 'Sketch Outline:', 'B. · Rocks'),), OS_SKETCH, '2-6', MAP + RIVERS + SEA, ID + 'p2-q1a',
      ('map', 'legend'),
      row_labels=(None, L(15, 'The complete course of the Colligan River'),
                  L(15, 'Locate a gorge on the Colligan River and mark it with an X on the sketch map'),
                  L(15, 'The Cunnigar sand spit'), L(15, 'An area of land above 300 metres.'))),
    T('p2-1b', P2, '1B', '', 30, 15, L(15, 'Rocks'),
      (L(15, 'Explain the formation of igneous rocks with reference to Irish examples.'),),
      (S(6, 'Two Irish igneous rocks named', None),),
      (pair('Two Irish igneous rocks named · 2 + 2 marks', 'Two Irish igneous rocks named'),
       srp('Explanation of formation', 13, f'Explanation of formation · 13 x {SRPS}')),
      '0-1', RW, ID + 'p2-q1b'),
    T('p2-1c', P2, '1C', '', 30, 15, L(15, 'Human Interaction with Surface Processes'),
      (L(15, 'Human activity impacts on surface processes.', 'The impact of human activity on mass movement.'),),
      (S(7, 'Impact on process identified', None),),
      (fixed('Impact on process identified', 2, 'Impact on process identified · 2 marks'),
       srp('Examination of impact on process', 14, f'Examination of impact on process · 14 x {SRPS}')),
      '0-6', RIVERS, ID + 'p2-q1c-dams',
      routes=choose_one('p2-q1c-', (
          ('The impact of dams on river processes', 'dams', '0-6', RIVERS),
          ('The impact of coastal defence work on coastal processes', 'coastal-defence', '0-6', SEA),
          ('The impact of human activity on mass movement.', 'mass-movement', '0-6', RW)))),
]
Q2AS = (L(16, 'Examine the diagram above showing the internal structure of the earth and answer each',
          'of the following questions.'),)
PART_TWO += romans('2A', P2, 16, L(16, 'Internal Structure of the Earth'), Q2AS, ID + 'p2-q2a', ('page',), [
    ('(i)', 12, L(16, '(i) Name each of the layers of the earth A, B, C, D, E and F.'),
     S(8, '(i) · A · Crust', '(ii) · Any valid description'),
     (fixed('A', 2, '(i) · A · Crust · 2 marks'), fixed('B', 2, 'B · Mantle · 2 marks'),
      fixed('C', 2, 'C · Asthenosphere · 2 marks'), fixed('D', 2, 'D · Lithosphere · 2 marks'),
      fixed('E', 2, 'E · Outer core · 2 marks'), fixed('F', 2, 'F · Inner core · 2 marks')), '0-0', PS),
    ('(ii)', 4, L(16, '(ii) Describe briefly the main difference between the composition of layer C and layer D.'),
     S(8, '(ii) · Any valid description', '(iii) · Any valid explanation'),
     (pair('(ii) · Any valid description · 2 + 2 marks', 'Description'),), '0-0', PS),
    ('(iii)', 4, L(16, '(iii) Explain briefly why plates move.'),
     S(8, '(iii) · Any valid explanation', None),
     (pair('(iii) · Any valid explanation · 2 + 2 marks', 'Explanation'),), '0-0', PS),
])
PART_TWO += [
    T('p2-2b', P2, '2B', '', 30, 16, L(16, 'Landform Development'),
      (L(16, '(i) Explain the formation of one landform of erosion and one landform of deposition',
         'that you have studied.'),),
      (S(9, 'Landform of erosion named', 'Or'),),
      (fixed('Landform of erosion named', 2, 'Landform of erosion named · 2 marks'),
       fixed('Landform of deposition named', 2, 'Landform of deposition named · 2 marks'),
       split('Formation of the two landforms (6/7 SRPs each)', 13,
             f'Formation landform of erosion · 6/7 x {SRPS}', f'Formation landform of deposition · 6/7 x {SRPS}')),
      '0-4', RIVERS + SEA + GLAC, ID + 'p2-q2b-route-i',
      routes=(
          Route('route-i', 'Route (i)', ID + 'p2-q2b-route-i', False, topic='0-4', atlas=RIVERS + SEA + GLAC),
          Route('route-ii', 'Route (ii)', ID + 'p2-q2b-route-ii', False,
                prompt=(L(16, '(ii) Describe and explain two processes of mass movement that you have studied.'),),
                scheme=(S(9, 'Two processes named', None),),
                criteria=(pair('Two processes named · 2 + 2 marks', 'Two processes named'),
                          split('Examination of the two processes (6/7 SRPs each)', 13,
                                f'Examination of process 1 · 6/7 x {SRPS}',
                                f'Examination of process 2 · 6/7 x {SRPS}')),
                topic='0-8', atlas=RW),
      )),
    T('p2-2c', P2, '2C', '', 30, 16, L(16, 'Rocks and Landscapes'),
      (L(16, 'Examine how different rock types produce distinctive landscapes, with reference to',
         'examples that you have studied.'),),
      (S(10, 'Rock 1 and assoc.', None),),
      (pair('Rock 1 and assoc. landscape named · 2 + 2 marks', 'Rock 1 and assoc. landscape named'),
       pair('Rock 2 and assoc. landscape named · 2 + 2 marks', 'Rock 2 and assoc. landscape named'),
       srp('Examination', 11, f'Examination · 11 x {SRPS}')),
      '0-1', RW + KARST, ID + 'p2-q2c'),
]
Q3AS = (L(17, 'Examine the diagram above which shows the stages in the cyclical development of a',
          'following questions.'),)
PART_TWO += romans('3A', P2, 17, L(17, 'Landscape Development'), Q3AS, ID + 'p2-q3a', ('page',), [
    ('(i)', 6, L(17, '(i) Name each of the stages A, B and C.'),
     S(11, '(i) · A · Youthful', '(ii) · A · Valid'),
     (fixed('A', 2, '(i) · A · Youthful / Young / Upper · 2 marks'), fixed('B', 2, 'B · Mature / Middle · 2 marks'),
      fixed('C', 2, 'C · Senile / Old age / Lower · 2 marks')), '0-9', RIVERS),
    ('(ii)', 6, L(17, '(ii) Name one fluvial landform from each of the stages A, B and C.'),
     S(11, '(ii) · A · Valid', '(iii) · Any valid'),
     (fixed('A', 2, '(ii) · A · Valid fluvial landform · 2 marks'), fixed('B', 2, 'B · Valid fluvial landform · 2 marks'),
      fixed('C', 2, 'C · Valid fluvial landform · 2 marks')), '0-9', RIVERS),
    ('(iii)', 4, L(17, '(iii) Explain briefly what is meant by peneplain.'),
     S(11, '(iii) · Any valid', '(iv) · Any valid'),
     (pair('(iii) · Any valid explanation · 2 + 2 marks', 'Explanation'),), '0-5', RIVERS),
    ('(iv)', 4, L(17, '(iv) Explain briefly what is meant by base level.'),
     S(11, '(iv) · Any valid', None),
     (pair('(iv) · Any valid explanation · 2 + 2 marks', 'Explanation'),), '0-9', RIVERS),
])
PART_TWO += [
    T('p2-3b', P2, '3B', '', 30, 17, L(17, 'Plate Tectonics'),
      (L(17, 'Describe and explain destructive plate boundaries.'),),
      (S(12, 'Examination · 15', 'C. · Sedimentary', None, 'B. · Plate Tectonics'),),
      (srp('Examination', 15, f'Examination · 15 x {SRPS}'),), '0-0', PS + EV, ID + 'p2-q3b'),
    T('p2-3c', P2, '3C', '', 30, 17, L(17, 'Sedimentary Structures'),
      (L(17, 'Examine how sedimentary structures, such as bedding planes and joints, influence the',
         'development of landforms.'),),
      (S(12, 'Examination · 15', None, None, 'C. · Sedimentary Structures'),),
      (srp('Examination', 15, f'Examination · 15 x {SRPS}'),), '0-3', KARST + RW + SEA, ID + 'p2-q3c'),
    T('p2-4a', P2, '4A', '', 20, 18, L(18, 'Map Skills'),
      (L(18, 'Draw an outline map of Ireland.', 'The outline of a named core region.'),),
      (S(13, 'Map outline', 'B. · European Union'),),
      sketch('Map outline · 4 marks graded (4/2/0)', (0, 2, 4),
             ('4 features @ 4 marks each: · Shown 2 marks graded (2/1/0)', 'Named 2 marks'),
             sums((0, 1, 2), (0, 2)), 4),
      '1-4', IRL, ID + 'p2-q4a',
      row_labels=(None, L(18, 'The outline of a named geomorphological region'),
                  L(18, 'A named urban centre in a peripheral region'),
                  L(18, 'The outline of a named cultural region'), L(18, 'The outline of a named core region.'))),
    T('p2-4b', P2, '4B', '', 30, 18, L(18, 'European Union', nth=0),
      (L(18, 'Examine how enlargement of the European Union impacts on existing member states.'),),
      (S(13, 'Impact identified', None),),
      (fixed('Impact identified', 2, 'Impact identified · 2 marks'), srp('Examination', 14, f'Examination · 14 x {SRPS}')),
      '1-3', EURO + EU_ECON, ID + 'p2-q4b'),
    T('p2-4c', P2, '4C', '', 30, 18, L(18, 'Population Dynamics'),
      (L(18, 'Account for the growth and distribution of population in a Continental / Sub-Continental',
         'that you have studied.'),),
      (S(14, 'Examination · 15', None),), (srp('Examination', 15, f'Examination · 15 x {SRPS}'),),
      '1-6', CONT + POP, ID + 'p2-q4c'),
]
Q5AS = (L(19, 'Examine the table above and answer each of the following questions.'),)
PART_TWO += romans('5A', P2, 19, L(19, 'Irish Trade'), Q5AS, ID + 'p2-q5a', ('page',), [
    ('(i)', 4, L(19, '(i) In which years did Ireland’s imports exceed €55 billion?'),
     S(15, '(i) · 2000 and 2008', '(ii) · €42,537'), (pair('(i) · 2000 and 2008 · 2 + 2 marks', 'Two years'),),
     '2-0', TG),
    ('(ii)', 4, L(19, '(ii) Calculate X, the value of Ireland’s trade surplus in 2012.'),
     S(15, '(ii) · €42,537', '(iii) · 19 or'), (fixed('X', 4, '(ii) · €42,537 million · 4 marks'),), '2-0', TG),
    ('(iii)', 4, L(19, '(iii) What was the percentage increase in Ireland’s trade surplus between', '2000 and 2004?'),
     S(15, '(iii) · 19 or', '(iv) · Any valid'), (fixed('Percentage increase', 4, '(iii) · 19 or 19.03 · 4 marks'),),
     '2-0', TG),
    ('(iv)', 4, L(19, '(iv) Explain briefly one advantage of having a trade surplus.'),
     S(15, '(iv) · Any valid', '(v) · Any two'), (pair('(iv) · Any valid explanation · 2 + 2 marks', 'Explanation'),),
     '2-0', TG + IRL),
    ('(v)', 4, L(19, '(v) Name two Irish agricultural exports.'),
     S(15, '(v) · Any two', None), (pair('(v) · Any two exports · 2 + 2 marks', 'Two exports'),), '1-4', IRL),
])
PART_TWO += [
    T('p2-5b', P2, '5B', '', 30, 19, L(19, 'European Regions'),
      (L(19, 'Examine the importance of relief to the economic development of any two contrasting',
         'that you have studied.'),),
      (S(16, 'Examination of Region 1', 'C. · Economic Activity'),),
      (split('Examination of the two regions (7/8 SRPs each)', 15,
             f'Examination of Region 1 · 7/8 x {SRPS}', f'Examination of Region 2 · 7/8 x {SRPS}'),),
      '1-5', EURO, ID + 'p2-q5b'),
    T('p2-5c', P2, '5C', '', 30, 19, L(19, 'Economic Activity'),
      (L(19, 'Discuss the factors that influence the development of secondary economic activity in a',
         'that you have studied.'),),
      (S(16, 'Factors identified', None),),
      (pair('Factors identified · 2 + 2 marks', 'Factors identified'), srp('Discussion', 13, f'Discussion · 13 x {SRPS}')),
      '1-6', CONT, ID + 'p2-q5c'),
]
Q6AS = (L(20, 'Examine the graph above and answer each of the following questions.'),)
PART_TWO += romans('6A', P2, 20, L(20, 'European Union Unemployment'), Q6AS, ID + 'p2-q6a', ('page',), [
    ('(i)', 4, L(20, '(i) Which country had the highest percentage unemployment between 2008 and 2012', '2012?'),
     S(17, '(i) · Spain and Netherlands', '(ii) · Greece'),
     (pair('(i) · Spain and Netherlands · 2 + 2 marks', 'Two countries'),), '2-0', TG + EURO),
    ('(ii)', 4, L(20, '(ii) Which country had the most significant increase in percentage unemployment',
                  'between 2010 and 2012?'),
     S(17, '(ii) · Greece', '(iii) · Any 2'), (fixed('Country', 4, '(ii) · Greece · 4 marks'),), '2-0', TG + EURO),
    ('(iii)', 4, L(20, '(iii) Name two countries where the percentage unemployment decreased between',
                   '2006 and 2007.'),
     S(17, '(iii) · Any 2', '(iv) · 1.5'), (pair('(iii) · Any 2 of Greece/Neth/Spain 2 + 2 marks', 'Two countries'),),
     '2-0', TG + EURO),
    ('(iv)', 4, L(20, '(iv) Calculate the increase in the percentage unemployment in the EU (27) between',
                  'reason for this increase.'),
     S(17, '(iv) · 1.5', '(v) · Any valid'),
     (fixed('Increase', 2, '(iv) · 1.5 (%) · 2 marks'), fixed('Reason', 2, 'Any valid reason stated · 2 marks')),
     '2-0', TG + EURO),
    ('(v)', 4, L(20, '(v) Explain briefly one economic effect of increased unemployment.'),
     S(17, '(v) · Any valid', None), (pair('(v) · Any valid explanation · 2 + 2 marks', 'Explanation'),),
     '1-5', EURO),
])
FACTORS = ('Relief', 'Climate', 'Markets.')
PART_TWO += [
    T('p2-6b', P2, '6B', '', 30, 20, L(20, 'Socio-Economic Regions'),
      (L(20, 'Economic activity in core regions differ from those in peripheral regions.',
         'examples that you have studied.'),),
      (S(18, 'Core and Peripheral', 'C. · Agriculture'),),
      (pair('Core and Peripheral regions named · 2 + 2 marks', 'Core and Peripheral regions named'),
       srp('Examination', 13, f'Examination · 13 x {SRPS}')),
      '1-0', IRL + EURO + CONT, ID + 'p2-q6b'),
    T('p2-6c', P2, '6C', '', 30, 20, L(20, 'Agriculture in Ireland'),
      (L(20, 'Account for the development of agriculture in an Irish region that you have studied, with',
         'Markets.'),),
      (S(18, 'Account of Factor 1', None),),
      (split('Account of the two factors (7/8 SRPs each)', 15,
             f'Account of Factor 1 · 7/8 x {SRPS}', f'Account of Factor 2 · 7/8 x {SRPS}'),),
      '1-4', IRL, ID + 'p2-q6c', absorbs=pool(ID + 'p2-q6c-', FACTORS, 2)[1]),
]

Q7AS = (L(22, 'Examine the table above and answer each of the following questions.'),)
PART_TWO += romans('7A', P2, 22, L(22, 'Economic Development'), Q7AS, ID + 'p2-q7a', ('page',), [
    ('(i)', 4, L(22, '(i) Calculate the difference in Gross National Income between the USA and China.'),
     S(20, '(i) · $35,535', '(ii) · Afghanistan'), (fixed('Difference', 4, '(i) · $35,535 · 4 marks'),), '2-0', TG),
    ('(ii)', 4, L(22, '(ii) Name the country with the lowest life expectancy at birth and name the country',
                  'with the highest life expectancy at birth.'),
     S(20, '(ii) · Afghanistan', '(iii) · Any valid'),
     (pair('(ii) · Afghanistan and Norway · 2 + 2 marks', 'Two countries'),), '2-0', TG),
    ('(iii)', 4, L(22, '(iii) Explain briefly one reason why life expectancy at birth is higher in some countries.'),
     S(20, '(iii) · Any valid', '(iv) · Education'), (pair('(iii) · Any valid explanation · 2 + 2 marks', 'Reason'),),
     '3-1', DEV),
    ('(iv)', 4, L(22, '(iv) Life expectancy and income levels are two factors used to calculate the Human',
                  'Name a third factor.'),
     S(20, '(iv) · Education', '(v) · Any valid'), (fixed('Third factor', 4, '(iv) · Education, etc. · 4 marks'),),
     '3-1', DEV),
    ('(v)', 4, L(22, '(v) Explain briefly one use of the Human Development Index.'),
     S(20, '(v) · Any valid', None), (pair('(v) · Any valid explanation · 2 + 2 marks', 'Use'),), '3-1', DEV),
])
PART_TWO += [
    T('p2-7b', P2, '7B', '', 30, 22, L(22, 'Renewable Energy'),
      (L(22, 'Examine the economic and environmental advantages of using renewable energy sources.'),),
      (S(21, 'Economic advantage identified', 'C. · Developed'),),
      (fixed('Economic advantage identified', 2, 'Economic advantage identified · 2 marks'),
       fixed('Environmental advantage identified', 2, 'Environmental advantage identified · 2 marks'),
       srp('Examination', 13, f'Examination · 13 x {SRPS}')),
      '3-5', ENERGY + ENV, ID + 'p2-q7b'),
    T('p2-7c', P2, '7C', '', 30, 22, L(22, 'Developed Economy'),
      (L(22, 'Examine the development of one of the following with reference to a developed economy',
         'Mass tourism.'),),
      (S(21, 'Developed economy named', None),),
      (fixed('Developed economy named', 2, 'Developed economy named · 2 marks'),
       srp('Examination', 14, f'Examination · 14 x {SRPS}')),
      '3-0', ECON, ID + 'p2-q7c-footloose-industries',
      routes=choose_one('p2-q7c-', (
          ('Footloose industries', 'footloose-industries', '3-0', ECON),
          ('Financial services', 'financial-services', '3-0', ECON),
          ('Mass tourism.', 'mass-tourism', '3-0', ECON)))),
    T('p2-8a', P2, '8A', '', 20, 23, L(23, 'Aerial Photograph'),
      (L(23, 'Examine the aerial photograph accompanying this paper.', 'suitable for development.'),),
      (S(22, 'Sketch Outline:', 'B. · Multinational'),),
      sketch('Sketch Outline: · 4 marks', (0, 4),
             ('4 features @ 4 marks each: · Shown 3 marks (graded 3/1/0)', 'Named 1 mark'), SHOWN3, 4),
      '2-8', AER + ECON, ID + 'p2-q8a', ('aerial',),
      row_labels=(None, L(23, 'A recreational area'), L(23, 'A large commercial/industrial building'),
                  L(23, 'A bridge'), L(23, 'An area of waste ground suitable for development.'))),
    T('p2-8b', P2, '8B', '', 30, 23, L(23, 'Multinational Company'),
      (L(23, 'With reference to one multinational company that you have studied, describe and explain',
         'Location of markets.'),),
      (S(22, 'MNC named', None),),
      (fixed('MNC named', 2, 'MNC named · 2 marks'), srp('Examination 1', 7, f'Examination 1 · 7 x {SRPS}'),
       srp('Examination 2', 7, f'Examination 2 · 7 x {SRPS}')),
      '3-2', MNC, ID + 'p2-q8b',
      absorbs=pool(ID + 'p2-q8b-', ('Sourcing of raw materials and components', 'Location of processing units',
                                    'Location of markets.'), 2)[1]),
    T('p2-8c', P2, '8C', '', 30, 23, L(23, 'Ireland and the European Union'),
      (L(23, 'Examine the impact of European Union policy on the Irish economy.'),),
      (S(23, 'Impact identified', None),),
      (fixed('Impact identified', 2, 'Impact identified · 2 marks'), fixed('Policy identified', 2, 'Policy identified · 2 marks'),
       srp('Examination', 13, f'Examination · 13 x {SRPS}')),
      '3-3', EU_ECON + IRL, ID + 'p2-q8c'),
]
Q9AS = (L(24, 'Examine the data in the table above showing the average annual percentage inflation rates',
          '2002 and 2012.'),)
PART_TWO += romans('9A', P2, 24, L(24, 'European Inflation', nth=0), Q9AS, ID + 'p2-q9a', ('page',), [
    ('(i)', 16, L(24, '(i) Using graph paper, draw a suitable graph to illustrate this data.'),
     S(24, 'Bar Chart · Pie Chart', '(ii) · Explain briefly'), GRAPH, '2-0', TG),
    ('(ii)', 4, L(24, '(ii) Explain briefly one effect of a high inflation rate.'),
     S(24, 'Any valid explanation', None), (pair('Any valid explanation · 2 + 2 marks', 'Effect'),), '3-0', ECON),
])
REASON_9B = ('Three reasons · @ 10 marks each', 'For each reason:', 'Reason stated · 2 marks',
             'Map reference / evidence · 2 marks', f'Examination · 3 x {SRPS}')
PART_TWO += [
    T('p2-9b', P2, '9B', '', 30, 24, L(24, 'Location of Economic Activity'),
      (L(24, 'Examine the 1:50 000 Ordnance Survey map and legend that accompany this paper.',
         'support each reason.'),),
      (S(25, 'Three reasons', 'C. · Conflict'),),
      tuple(Criterion(f'Reason {n}', 10, evens(10), 'srp', REASON_9B) for n in (1, 2, 3)),
      '3-2', MNC + MAP, ID + 'p2-q9b', ('map', 'legend')),
    T('p2-9c', P2, '9C', '', 30, 24, L(24, 'Conflict of Interest'),
      (L(24, 'Examine how conflict can arise between economic interests and environmental interests',
         'studied.'),),
      (S(25, 'Two examples', None),),
      (pair('Two examples · 2 + 2 marks', 'Two examples'), srp('Examination', 13, f'Examination · 13 x {SRPS}')),
      '3-4', ENV, ID + 'p2-q9c'),
    T('p2-10a', P2, '10A', '', 20, 25, L(25, 'Settlement Patterns'),
      (L(25, 'Examine the 1:50 000 Ordnance Survey map and legend that accompany this paper.',
         'An area of clustered rural settlement.'),),
      (S(26, 'Sketch Outline:', None),), OS_SKETCH, '2-6', MAP + URB, ID + 'p2-q10a', ('map', 'legend'),
      row_labels=(None, L(25, 'The built up area of Dungarvan'), L(25, 'An area of linear/ribbon rural settlement'),
                  L(25, 'An area of dispersed rural settlement'), L(25, 'An area of clustered rural settlement.'))),
    T('p2-10b', P2, '10B', '', 30, 25, L(25, 'Changing Urban Functions'),
      (L(25, 'Examine how the functions of urban centres can change over time, with reference',
         'to Irish example(s).'),),
      (S(27, 'Functions identified', 'C. · Migration'),),
      (pair('Functions identified · 2 + 2 marks', 'Functions identified'),
       fixed('Example Irish urban centre', 2, 'Example Irish urban centre · 2 marks'),
       srp('Examination', 12, f'Examination · 12 x {SRPS}')),
      '4-3', URB, ID + 'p2-q10b'),
    T('p2-10c', P2, '10C', '', 30, 25, L(25, 'Migration'),
      (L(25, 'With reference to a developed region that you have studied, explain the impact of',
         'donor and receiver regions.'),),
      (S(27, 'Named developed region', None),),
      (fixed('Named developed region', 2, 'Named developed region · 2 marks'),
       fixed('Impact on donor region identified', 2, 'Impact on donor region identified · 2 marks'),
       fixed('Impact on receiver region identified', 2, 'Impact on receiver region identified · 2 marks'),
       srp('Examination', 12, f'Examination · 12 x {SRPS}')),
      '4-2', POP, ID + 'p2-q10c'),
]
Q11AS = (L(26, 'Examine the diagram above showing the Demographic Transition Model and answer',
           'each of the following questions.'),)
PART_TWO += romans('11A', P2, 26, L(26, 'Population Dynamics'), Q11AS, ID + 'p2-q11a', ('page',), [
    ('(i)', 4, L(26, '(i) In which stage of the Demographic Transition Model is the total population at its',
                 'lowest?'),
     S(28, '(i) · Stage 1', '(ii) · Early'), (fixed('Stage', 4, '(i) · Stage 1 / High Stationary · 4 marks'),),
     '4-0', POP),
    ('(ii)', 4, L(26, '(ii) Name X, Stage 2 of the Demographic Transition Model and name an example of',
                  'a country in this stage.'),
     S(28, '(ii) · Early', '(iii) · Senile'),
     (fixed('Stage 2 named', 2, '(ii) · Early Expanding · 2 marks'), fixed('Example', 2, 'Any valid example · 2 marks')),
     '4-0', POP),
    ('(iii)', 4, L(26, '(iii) Name Y, Stage 5 of the Demographic Transition Model and name an example of',
                   'a country in this stage.'),
     S(28, '(iii) · Senile', '(iv) · Any valid'),
     (fixed('Stage 5 named', 2, '(iii) · Senile / declining / Old age · 2 marks'),
      fixed('Example', 2, 'Any valid example · 2 marks')), '4-0', POP),
    ('(iv)', 4, L(26, '(iv) Explain briefly one problem facing countries in Stage 5 of the Demographic',
                  'Transition Model.'),
     S(28, '(iv) · Any valid', '(v) · Any valid'), (pair('(iv) · Any valid explanation · 2 + 2 marks', 'Problem'),),
     '4-0', POP),
    ('(v)', 4, L(26, '(v) Explain briefly what is meant by natural increase.'),
     S(28, '(v) · Any valid', None), (pair('(v) · Any valid explanation · 2 + 2 marks', 'Explanation'),), '4-0', POP),
])
REASON_11B = ('Three reasons · @ 10 marks each', 'For each reason:', 'Reason stated · 2 marks',
              'Map evidence · 2 marks', f'Explanation · 3 x {SRPS}')
PART_TWO += [
    T('p2-11b', P2, '11B', '', 30, 26, L(26, 'Population Distribution'),
      (L(26, 'Examine the 1:50 000 Ordnance Survey map and legend that accompany this paper.',
         'support each reason.'),),
      (S(29, 'Three reasons', 'C. · Central'),),
      tuple(Criterion(f'Reason {n}', 10, evens(10), 'srp', REASON_11B) for n in (1, 2, 3)),
      '4-3', URB + MAP + POP, ID + 'p2-q11b', ('map', 'legend')),
    T('p2-11c', P2, '11C', '', 30, 27, L(27, 'Central Place Theory', nth=0),
      (L(27, 'Explain the importance of hierarchy and hinterland in Central Place Theory.'),),
      (S(29, 'Explanation · 15', None),), (srp('Explanation', 15, f'Explanation · 15 x {SRPS}'),),
      '4-3', URB, ID + 'p2-q11c', ('page',)),
]
Q12AS = (L(28, 'Examine the data above showing dependency ratios in a number of Irish regions in 2011.'),)
PART_TWO += romans('12A', P2, 28, L(28, 'Population Dynamics'), Q12AS, ID + 'p2-q12a', ('page',), [
    ('(i)', 16, L(28, '(i) Using graph paper, draw a suitable graph to illustrate this data.'),
     S(30, 'Bar Chart · Pie Chart', '(ii) · Explain briefly'), GRAPH, '2-0', TG),
    ('(ii)', 4, L(28, '(ii) Explain briefly one reason why dependency ratios are usually higher in rural', 'areas.'),
     S(30, 'Any valid explanation', None), (pair('Any valid explanation · 2 + 2 marks', 'Reason'),), '4-0', POP),
])
FUNCTION_12B = ('Three functions · @ 10 marks each', 'For each function:', 'Function named · 2 marks',
                'Aerial photo evidence · 2 marks', f'Examination · 3 x {SRPS}')
PART_TWO += [
    T('p2-12b', P2, '12B', '', 30, 28, L(28, 'Urban Functions'),
      (L(28, 'Examine the aerial photograph accompanying this paper.', 'illustrate each function.'),),
      (S(31, 'Three functions', 'C. · Population'),),
      tuple(Criterion(f'Function {n}', 10, evens(10), 'srp', FUNCTION_12B) for n in (1, 2, 3)),
      '4-3', URB + AER, ID + 'p2-q12b', ('aerial',)),
    T('p2-12c', P2, '12C', '', 30, 28, L(28, 'Population', nth=1),
      (L(28, 'Examine the influence/impact of one of the following on population growth:', 'Technology.'),),
      (S(31, 'Impact / influence identified', None),),
      (fixed('Impact / influence identified', 2, 'Impact / influence identified · 2 marks'),
       srp('Examination', 14, f'Examination · 14 x {SRPS}')),
      '4-1', POP, ID + 'p2-q12c-society-and-culture',
      routes=choose_one('p2-q12c-', (
          ('Society and culture', 'society-and-culture', '4-1', POP),
          ('Income levels', 'income-levels', '4-1', POP),
          ('Technology.', 'technology', '4-1', POP)))),
]

# ------------------------------------------------------------------ Options --
OC = (S(33, '*Overall Coherence (20 marks)', None, table=True),)
COHERENCE = Criterion('Overall coherence', 20, (0, 6, 10, 14, 17, 20), 'exact',
                      ('Overall Coherence · 20 marks graded*', '*Overall Coherence (20 marks)', 'Excellent · 20',
                       'Very Good · 17', 'Good · 14', 'Fair · 10', 'Weak · 6', 'Poor · 0'))
OPTION_CRITERIA = (
    Criterion('Aspects (3 @ 20 marks or 4 @ 15 marks)', 60, upto(60), 'srp',
              ('Number of aspects', 'Identifying aspect', '8 x SRP')),
    COHERENCE)


def option(q, page, theme, note_nth, prompt, scheme_page, topic, atlas, after=None, end=None):
    return T(f'p2-{q}', P2, q, '', 80, page, theme, prompt if isinstance(prompt, tuple) else (prompt,),
             (S(scheme_page, 'Number of aspects', end, None, after), *OC), OPTION_CRITERIA,
             topic, (atlas,), ID + f'p2-q{q}',
             stem=(L(page, 'Note: It is better to discuss three or four aspects', 'large number of points.',
                     nth=note_nth),))


GI, GE = H + 'option-global-interdependence', H + 'option-geoecology'
CI, AO = H + 'option-culture-identity', H + 'option-atmosphere-ocean'
OPTIONS = [
    option('13', 30, L(30, 'Global Interdependence'), 0,
           L(30, 'Views of development and underdevelopment are subject to change.', 'Discuss.'), 34, '5-0', GI,
           after='13.', end='14.'),
    option('14', 30, L(30, 'Global Interdependence'), 0,
           L(30, 'Examine how land ownership patterns have impacted on development.'), 34, '5-2', GI, after='14.'),
    option('15', 30, L(30, 'Global Interdependence'), 0,
           L(30, 'We live in an interdependent global economy.', 'with reference to global warming.'),
           35, '5-1', GI),
    option('16', 30, L(30, 'Geoecology'), 1,
           L(30, 'Explain how soil characteristics impact on soil development.'), 36, '6-0', GE,
           after='16.', end='17.'),
    option('17', 30, L(30, 'Geoecology'), 1,
           L(30, 'Soil profiles are the result of the operation of soil-forming processes.', 'Discuss.'),
           36, '6-1', GE, after='17.'),
    option('18', 30, L(30, 'Geoecology'), 1,
           L(30, 'Biomes are altered by human activity.', 'Discuss.'), 37, '6-3', GE),
    option('19', 31, L(31, 'Culture and Identity'), 0,
           L(31, 'Examine the importance of religion as a cultural indicator.'), 38, '7-0', CI,
           after='19.', end='20.'),
    option('20', 31, L(31, 'Culture and Identity'), 0,
           L(31, 'The existence of different cultural groups within state borders can lead to conflict.',
             'Discuss.'), 38, '7-1', CI, after='20.'),
    option('21', 31, L(31, 'Culture and Identity'), 0,
           L(31, 'Examine the strategies that have been or could be implemented to aid the survival of',
             'minority languages.'), 39, '7-0', CI),
    option('22', 31, L(31, 'The Atmosphere - Ocean Environment'), 1,
           L(31, 'Examine the uneven distribution of temperature over the earth’s surface.'),
           40, '8-1', AO, after='22.', end='23.'),
    option('23', 31, L(31, 'The Atmosphere - Ocean Environment'), 1,
           L(31, 'Exchanges of water between oceans and atmosphere, over the earth’s surface,', 'Discuss.'),
           40, '8-2', AO, after='23.'),
    option('24', 31, L(31, 'The Atmosphere - Ocean Environment'), 1,
           L(31, 'Climate characteristics impact on economic development.', 'Discuss.'), 41, '8-5', AO),
]

TASKS = [*PART_ONE, *PART_TWO, *OPTIONS]

ID_CORRECTION_REASON = 'No 2014 Higher card shipped before this review; every card is new.'

# No 2014 Higher card was live on origin/main before this review.
LEGACY_IDS: list[str] = []
