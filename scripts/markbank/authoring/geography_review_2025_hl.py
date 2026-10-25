"""Independent review ledger: Leaving Certificate Geography 2025 Higher Level.

Sources (English editions, Paper Trail index; sizes and SHA-256 pinned in
EXPECTED_SOURCES and the generated audit): Part One and Answerbook
LC005ALP042EV (48 pages), Part Two LC005ALP043EV (20 pages), marking scheme
LC005ALP000EV (70 pages), and the common companions — 1:50 000 Oughterard map
LC005CLP003EV (fetched from Paper Trail storage; not in the harvested corpus),
its legend LC005CLPC00EV and the Oughterard aerial photograph LC005CLP004EV,
which the SEC publishes only as a JPEG.

Visual sweep (every page rendered and read on 2026-10-11):
  Part One booklet p1 cover (COVID-adjusted paper note); p2 instructions
  (Part One "Attempt any TEN", 80 marks; Part Two "attempt FOUR", 320 marks);
  p3-p13 Questions 1-12 (p9 holds Q7 and Q8); p14 Part Two answerbook
  instructions; p15-p18 graph paper; p19-p47 lined answer pages; p48 back.
  Part Two booklet p1 cover; p2 Part Two instructions; p3-p8 Sections 1-2
  (Q1-Q6); p9 Section 3 divider; p10-p16 Electives (Q7-Q12; Q11 runs onto
  p15); p17 Section 4 divider and note; p18-p19 Options (Q13-Q24); p20 back.
  Scheme p1 cover; p2-p3 notes and annotation key; p4 Part One table (two
  columns: Q1-Q6, Q7-Q12); p5-p23 Q1-Q6 (2B route (ii) on p10); p24 divider;
  p25-p45 Q7-Q12 (9A(ii) on p32, 11A answers on p39, 12A(ii) on p43); p46
  divider; p47 option outline and Overall Coherence descriptors; p48 option
  annotations; p49-p60 Q13-Q24; p61-p66 Geographical Investigation
  (coursework); p67 investigation topics; p68 Irish-language bonus marks;
  p69-p70 blank. Companions: Oughterard map extract with Lough Corrib and the
  Owenriff river; OS legend sheet; oblique aerial photograph of Oughterard.

Companions. Part One Q7 (map, legend), Q8 (aerial, map, legend), Q9
(aerial); Part Two 1A, 7A, 8B and 12B (map, legend) and 10A (aerial) were
held back before this review because their companions were not wired. Each
now carries the exact official documents it names.

Boundaries and tariffs follow the 2026 Higher ledger: every part the scheme
prices separately is a task; a matching/location table under one printed
instruction is one task with a criterion per scheme row (rows checked
visually: Q2 Tarn=B, Arete=D, Dendritic=A, Concave=C against the map extract;
Q3 Bedding plane=A, Clint=D, Karren=B, Grike=C; Q5 Soil creep=D, Rockfall=A,
Avalanche=B, Lahar=C; Q6 rows follow the printed Type-of-Region order). The
Q4 table's blank rows are labelled by position, never by the answer.
"""

import itertools

from geography_review import (
    Criterion, Lift, Route, SchemeSlice, Task, pool, evens, fixed, slug, srp, sums, upto,
)

YEAR = 2025
LEVEL = 'higher'
PAPER_PAGES = {1: 48, 2: 20}
SCHEME_PAGES = 70
QUESTION_TARIFFS = {1: {str(n): 8 for n in range(1, 13)},
                    2: {**{f'{n}{x}': (20 if x == 'A' else 30)
                           for n in range(1, 13) for x in 'ABC'},
                        **{str(n): 80 for n in range(13, 25)}}}

EXPECTED_SOURCES = {
    'paper1': ('LC005ALP042EV.pdf', 15398165),
    'paper2': ('LC005ALP043EV.pdf', 2261223),
    'scheme': ('LC005ALP000EV.pdf', 2031559),
    'map': ('LC005CLP003EV.pdf', 19789910),
    'legend': ('LC005CLPC00EV.pdf', 4055991),
    'aerial': ('LC005CLP004EV.jpg', 5572138),
}

PAGE_REVIEW = {
    'paper1': {1: 'cover', 2: 'instructions', **{p: 'question' for p in range(3, 14)},
               14: 'answerbook instructions', **{p: 'graph-paper answer page' for p in range(15, 19)},
               **{p: 'lined answer page' for p in range(19, 48)}, 48: 'copyright/back cover'},
    'paper2': {1: 'cover', 2: 'Part Two instructions',
               **{p: 'question' for p in (3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15, 16, 18, 19)},
               9: 'section divider', 17: 'section divider and option note', 20: 'copyright/back cover'},
    'scheme': {1: 'cover', 2: 'notes', 3: 'notes and annotation key', 4: 'Part One table',
               **{p: 'Part Two allocation' for p in range(5, 24)}, 24: 'section divider',
               **{p: 'Part Two allocation' for p in range(25, 46)}, 46: 'section divider',
               47: 'option outline and coherence descriptors', 48: 'option annotations',
               **{p: 'option allocation' for p in range(49, 61)},
               **{p: 'geographical investigation (coursework)' for p in range(61, 67)},
               67: 'investigation topics', 68: 'Irish-language bonus marks', 69: 'blank', 70: 'blank'},
}

EXPECTED_SELECTION_SCAN = [
    [1, 2, 'attempt any ten'], [1, 2, 'attempt four'], [1, 3, 'attempt any ten'],
    [1, 7, 'any two'],
    [2, 2, 'attempt four'],
    [2, 4, 'answer (i) or (ii)'], [2, 4, 'or one'], [2, 4, 'or one'],
    [2, 5, 'one of the following'], [2, 5, 'one of the following'],
    [2, 10, 'any two'],
    [2, 12, 'two of the following'],
    [2, 13, 'two of the following'],
    [2, 15, 'any one'],
    [2, 18, 'any three'], [2, 18, 'any three'],
]
SELECTION_REVIEW = [
    {'scan': [[1, 2, 'attempt any ten'], [1, 2, 'attempt four'], [1, 3, 'attempt any ten'],
              [2, 2, 'attempt four']],
     'kind': 'exam-attempt-rule',
     'reason': 'Part One any ten of twelve and Part Two four questions are attempt rules; every question is carded.'},
    {'scan': [[2, 4, 'answer (i) or (ii)'], [2, 4, 'or one'], [2, 4, 'or one']], 'kind': 'closed-route',
     'reason': '2B: (i) or (ii); (i) offers one fluvial OR one coastal OR one glacial landform -> 4 routes.'},
    {'scan': [[2, 5, 'one of the following'], [2, 5, 'one of the following']], 'kind': 'closed-choose-one',
     'reason': '3B one of four printed bullets -> 4 routes; 3C one of two (folding, faulting) -> 2 routes.'},
    {'scan': [[2, 10, 'any two']], 'kind': 'choose-n-one-card',
     'reason': '7B any two of three printed headings -> one card with every printed item (choice is not a route; the scheme marks each chosen item alike).'},
    {'scan': [[2, 12, 'two of the following']], 'kind': 'closed-choose-one-x-choose-n-one-card',
     'reason': '9B footloose industries OR financial services OR mass tourism -> 3 routes; within each, two of three printed factors -> one card with every printed factor (choice is not a route).'},
    {'scan': [[2, 13, 'two of the following']], 'kind': 'choose-n-one-card',
     'reason': '10B two of three printed urban problems -> one card with every printed item (choice is not a route; the scheme marks each chosen item alike).'},
    {'scan': [[2, 15, 'any one']], 'kind': 'closed-choose-one',
     'reason': '11C any one of three printed factors -> 3 routes.'},
    {'scan': [[2, 18, 'any three'], [2, 18, 'any three']], 'kind': 'choose-n-one-card',
     'reason': '14 any three of four themes and 16 any three of four processes -> one card each with every printed item (choice is not a route; the scheme marks each chosen aspect alike).'},
    {'scan': [], 'kind': 'inline-closed-route',
     'reason': '5C "climate or geomorphology" -> 2 routes (no directive word the scan reads; the route text is anchored on the paper).'},
    {'scan': [[1, 7, 'any two']], 'kind': 'open-response',
     'reason': 'Part One Q5(ii) any two factors has no printed pool. Open choices are not fanned out: "two factors" (4B, 5B, 6B), "one tertiary economic activity", "one urban area", "one multinational company", "one specific renewable energy source", "example(s)". Compulsory lists stay whole: 1C, 2C physical AND chemical, 4C each challenge, 9C each advantage, 10C donor AND receiver, 13, 18 and 22 each bullet, 8B all three headings; 11A(iv) offers answer options, not routes.'},
]

P1, P2 = 1, 2
LEFT = (0.0, 0.0, 0.56, 1.0)
RIGHT = (0.56, 0.0, 1.0, 1.0)
ID = 'geography-2025-hl-'
H = 'geography-higher-'
TF2 = '(ii) State whether each of the following statements is true or false by ticking (✓) the correct box.'


def L(page, start, end=None, nth=None):
    return Lift(page, start, end, None, nth)


def S(page, start, end=None, clip=None, after=None, table=False):
    return SchemeSlice(page, start, end, clip, after, table)


def T(key, part, q, sub, marks, page, title, prompt, scheme, criteria, topic, atlas, card_id,
      legacy, sources=(), stem=(), routes=(), row_labels=(), absorbs=()):
    return Task(key, part, q, sub, marks, page, title, prompt, scheme, criteria, topic, atlas,
                sources, card_id, legacy, stem=stem, routes=routes, row_labels=row_labels,
                absorbs=absorbs)


def rows(lines, marks=1):
    return tuple(fixed(f'Row {i}', marks, line) for i, line in enumerate(lines, 1))


def p1_romans(q, page, title, stem, first_id, first_legacy, sources, parts, clip):
    """Part One romans. parts: (sub, marks, prompt, scheme start, scheme end, criteria, topic, atlas)."""
    out = []
    for index, (sub, marks, prompt, start, end, criteria, topic, atlas) in enumerate(parts):
        key = sub.strip('()').replace(')(', '-')
        out.append(T(f'p1-{q}-{key}', P1, q, sub, marks, page, title,
                     prompt if isinstance(prompt, tuple) else (prompt,),
                     (S(4, start, end, clip),), criteria, topic, atlas,
                     first_id if index == 0 else f'{first_id}-{key}',
                     first_legacy and index == 0, sources, stem))
    return out


# ---------------------------------------------------------------- Part One --
PS = (H + 'plate-tectonics',)
RW = (H + 'rocks-weathering-mass-movement',)
MAP = (H + 'mapwork',)
AER = (H + 'aerial-photos',)
TG = (H + 'tablesgraphs-questions',)

Q1S = (L(3, 'Examine the diagram above showing tectonic activity', 'following questions.'),)
PART_ONE = p1_romans('1', 3, L(3, 'The Tectonic Cycle'), Q1S, ID + 'p1-q1', True, ('page',), [
    ('(i)', 2, L(3, '(i) What type of current is shown at A?'), 'Q.1 (i)', '(ii) Subduction',
     (fixed('Current', 2, 'Q.1 (i) Convection Current 2 marks'),), '0-0', PS),
    ('(ii)', 2, L(3, '(ii) Name the process occurring at B.'), '(ii) Subduction', '(iii) Ocean Trench',
     (fixed('Process', 2, '(ii) Subduction 2 marks'),), '0-0', PS),
    ('(iii)', 2, L(3, '(iii) Name the feature that is formed', 'shown at C.'), '(iii) Ocean Trench', '(iv) Lithosphere',
     (fixed('Feature', 2, '(iii) Ocean Trench 2 marks'),), '0-0', PS),
    ('(iv)', 2, L(3, '(iv) Name the layer of the earth at D', 'mantle and crust.'), '(iv) Lithosphere', 'Q.2',
     (fixed('Layer', 2, '(iv) Lithosphere 2 marks'),), '0-0', PS),
], LEFT)

Q2S = (L(4, 'Examine the 1:50 000 Ordnance Survey map extract above', 'following questions.'),)
PART_ONE += [
    T('p1-2-i', P1, '2', '(i)', 4, 4, L(4, 'Feature Identification'),
      (L(4, '(i) Match each of the features labelled A, B, C and D', 'in the table below.'),),
      (S(4, 'Q.2 (i) B', '(ii) (a) True', LEFT),),
      rows(['Q.2 (i) B 1 mark', 'D 1 mark', 'A 1 mark', 'C 1 mark']),
      '2-6', MAP + (H + 'glaciation', H + 'rivers'), ID + 'p1-q2', True, ('page',), Q2S,
      row_labels=(L(4, 'Tarn'), L(4, 'Arête'), L(4, 'Dendritic Drainage'), L(4, 'Concave Slope'))),
    T('p1-2-ii-a', P1, '2', '(ii)(a)', 2, 4, L(4, 'Feature Identification'),
      (L(4, TF2), L(4, '(a) Eskers are features formed by fluvio-glacial deposition.')),
      (S(4, '(ii) (a) True', '(b) True', LEFT),), (fixed('Statement (a)', 2, '(ii) (a) True 2 marks'),),
      '0-11', (H + 'glaciation',), ID + 'p1-q2-ii-a', False, ('page',), Q2S),
    T('p1-2-ii-b', P1, '2', '(ii)(b)', 2, 4, L(4, 'Feature Identification'),
      (L(4, TF2), L(4, '(b) Deranged drainage patterns are common in areas of glacial deposition.')),
      (S(4, '(b) True', 'Q.3', LEFT),), (fixed('Statement (b)', 2, '(b) True 2 marks'),),
      '0-11', (H + 'glaciation', H + 'rivers'), ID + 'p1-q2-ii-b', False, ('page',), Q2S),
]

Q3S = (L(5, 'Examine the diagram of a karst landscape above', 'following questions.'),)
KARST = (H + 'karst-regions',)
PART_ONE += [
    T('p1-3-i', P1, '3', '(i)', 4, 5, L(5, 'Karst Landscape'),
      (L(5, '(i) Match each of the letters A, B, C and D', 'in the table below.'),),
      (S(4, 'Q.3 (i) A', '(ii) Valid answer 2 marks', LEFT),),
      rows(['Q.3 (i) A 1 mark', 'D 1 mark', 'B 1 mark', 'C 1 mark']),
      '0-3', KARST, ID + 'p1-q3', True, ('page',), Q3S,
      row_labels=(L(5, 'Bedding plane'), L(5, 'Clint'), L(5, 'Karren'), L(5, 'Grike'))),
    T('p1-3-ii', P1, '3', '(ii)', 2, 5, L(5, 'Karst Landscape'),
      (L(5, '(ii) Name one form of chemical weathering.'),),
      (S(4, '(ii) Valid answer 2 marks', '(iii) Valid answer', LEFT),),
      (fixed('Chemical weathering', 2, '(ii) Valid answer 2 marks'),),
      '0-8', RW, ID + 'p1-q3-ii', False, ('page',), Q3S),
    T('p1-3-iii', P1, '3', '(iii)', 2, 5, L(5, 'Karst Landscape'),
      (L(5, '(iii) State what is meant by the term permeable rock.'),),
      (S(4, '(iii) Valid answer 2 marks', 'Q.4', LEFT),),
      (fixed('Meaning', 2, '(iii) Valid answer 2 marks'),),
      '0-3', KARST, ID + 'p1-q3-iii', False, ('page',), Q3S),
]

Q4S = (L(6, 'The word box below contains source materials', 'following questions.'),)
Q4_HEAD = ('Q.4 (i) @ 1 mark each', 'Source · Igneous/Sedimentary · Metamorphic', 'Material · Rock · Rock')
PART_ONE += [
    T('p1-4-i', P1, '4', '(i)', 6, 6, L(6, 'Rocks', nth=0),
      (L(6, '(i) Complete the table below', 'completed for you.'),),
      (S(4, 'Q.4 (i) @ 1 mark each', '(ii) Valid answer 1+1', LEFT),),
      (Criterion('Row 2', 3, upto(3), 'exact', (*Q4_HEAD, 'Sand · Sandstone · Quartzite')),
       Criterion('Row 3', 3, upto(3), 'exact', (*Q4_HEAD, 'Molten · Basalt · Schist', '=Rock'))),
      '0-1', RW, ID + 'p1-q4', True, ('page',), Q4S),
    T('p1-4-ii', P1, '4', '(ii)', 2, 6, L(6, 'Rocks', nth=0),
      (L(6, '(ii) State two factors that cause rocks to become metamorphosed.'),),
      (S(4, '(ii) Valid answer 1+1', 'Q.5', LEFT),),
      (fixed('Two factors', 2, '(ii) Valid answer 1+1 mark', (0, 1, 2)),),
      '0-1', RW, ID + 'p1-q4-ii', False, ('page',), Q4S),
]

Q5S = (L(7, 'Examine the photographs above and answer each of the following questions.'),)
PART_ONE += [
    T('p1-5-i', P1, '5', '(i)', 4, 7, L(7, 'Mass Movement'),
      (L(7, '(i) Match each of the photographs A, B, C and D', 'in the table below.'),),
      (S(4, 'Q.5 (i) D', '(ii) Valid answer 2 + 2', LEFT),),
      rows(['Q.5 (i) D 1 mark', 'A 1 mark', 'B 1 mark', 'C 1 mark']),
      '0-8', RW, ID + 'p1-q5', True, ('page',), Q5S,
      row_labels=(L(7, 'Soil Creep'), L(7, 'Rockfall'), L(7, 'Avalanche'), L(7, 'Lahar'))),
    T('p1-5-ii', P1, '5', '(ii)', 4, 7, L(7, 'Mass Movement'),
      (L(7, '(ii) State any two factors', 'mass movement processes.'),),
      (S(4, '(ii) Valid answer 2 + 2', 'Q.6', LEFT),),
      (fixed('Two factors', 4, '(ii) Valid answer 2 + 2 marks', (0, 2, 4)),),
      '0-8', RW, ID + 'p1-q5-ii', False, ('page',), Q5S),
    T('p1-6', P1, '6', '', 8, 8, L(8, 'Concept of a Region'),
      (L(8, 'Examine the information below in the word box', 'One row has been completed for you.'),),
      (S(4, 'Q.6 @ 1 mark each', None, LEFT),),
      tuple(Criterion(f'Row {i}', 2, upto(2), 'exact', ('Q.6 @ 1 mark each', 'Example · Location', line))
            for i, line in enumerate(('Dingle · Co. Kerry', 'Ruhr Valley · Germany',
                                      'Wicklow Mountains · Leinster', 'Paris Basin · France'), 1)),
      '1-0', (H + 'regions-ireland', H + 'regions-european'), ID + 'p1-q6', True, ('page',),
      row_labels=(L(8, 'Cultural region (Language)'), L(8, 'Region of Industrial Decline'),
                  L(8, 'Geomorphological region'), L(8, 'Core Region'))),
]

Q7S = (L(9, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper, and answer each of the following questions.'),)
PART_ONE += p1_romans('7', 9, L(9, 'Map Skills'), Q7S, ID + 'p1-q7', False, ('map', 'legend'), [
    ('(i)', 2, L(9, '(i) Give a six-figure grid reference for the Independent Holiday Hostel in Oughterard.'),
     'Q.7 (i)', '(ii) 6 - 7', (fixed('Grid reference', 2, 'Q.7 (i) M 123 432 2 marks'),), '2-6', MAP),
    ('(ii)', 2, L(9, '(ii) Calculate the approximate area', 'map extract.'),
     '(ii) 6 - 7', '(iii) 7.8', (fixed('Area', 2, '(ii) 6 - 7 (km²) 2 marks'),), '2-6', MAP),
    ('(iii)', 2, L(9, '(iii) Measure the length', 'M 080 416.'),
     '(iii) 7.8', '(iv) Irish Speaking Area', (fixed('Length', 2, '(iii) 7.8 (km) 2 marks'),), '2-6', MAP),
    ('(iv)', 2, L(9, '(iv) What type of cultural area', 'highlighted line?'),
     '(iv) Irish Speaking Area', 'Q.8', (fixed('Cultural area', 2, '(iv) Irish Speaking Area 2 marks'),), '2-6', MAP),
], RIGHT)

Q8S = (L(9, 'Examine the aerial photograph of Oughterard and the 1:50 000', 'following questions.'),)
PART_ONE += p1_romans('8', 9, L(9, 'Aerial Photograph and Ordnance Survey Map'), Q8S, ID + 'p1-q8', False,
                      ('aerial', 'map', 'legend'), [
    ('(i)', 2, L(9, '(i) Name the river shown on the aerial photograph.'),
     'Q.8 (i)', '(ii) M 122 427', (fixed('River', 2, 'Q.8 (i) Owenriff river 2 marks'),), '2-8', AER + MAP),
    ('(ii)', 2, L(9, '(ii) Give a six-figure grid reference for the church', 'aerial photograph.'),
     '(ii) M 122 427', '(iii) N59', (fixed('Grid reference', 2, '(ii) M 122 427 2 marks'),), '2-8', AER + MAP),
    ('(iii)', 2, L(9, '(iii) Name the main road', 'aerial photograph.'),
     '(iii) N59', '(iv) North East', (fixed('Road', 2, '(iii) N59 2 marks'),), '2-8', AER + MAP),
    ('(iv)', 2, L(9, '(iv) In what direction', 'was taken?'),
     '(iv) North East', 'Q.9', (fixed('Direction', 2, '(iv) North East 2 marks'),), '2-8', AER + MAP),
], RIGHT)

PART_ONE.append(T(
    'p1-9', P1, '9', '', 8, 10, L(10, 'Aerial Photograph', nth=0),
    (L(10, 'Examine the aerial photograph of Oughterard accompanying this paper', 'area of Oughterard.'),
     L(10, 'Using accepted notation', 'in the table below.')),
    (S(4, 'Q.9 A Centre foreground', 'Q.10', RIGHT),),
    (fixed('Image A', 2, 'Q.9 A Centre foreground 2 marks'), fixed('Image B', 2, 'B Right background 2 marks'),
     fixed('Image C', 2, 'C Left foreground 2 marks'), fixed('Image D', 2, 'D Left middleground 2 marks')),
    '2-8', AER, ID + 'p1-q9', False, ('page', 'aerial')))

WX = (H + 'weather-climate',)
Q10S = (L(11, 'Examine the Met Éireann Surface Analysis Chart', 'following questions.'),)
PART_ONE += p1_romans('10', 11, L(11, 'Weather', nth=0), Q10S, ID + 'p1-q10', True, ('page',), [
    ('(i)', 2, L(11, '(i) What is the pressure', 'at X?'), 'Q.10 (i)', '(ii) False',
     (fixed('Pressure', 2, 'Q.10 (i) 1013 2 marks'),), '2-7', WX),
    ('(ii)', 2, L(11, '(ii) State whether the following statement is true or false', 'strong winds.'),
     '(ii) False', '(iii) Isobars', (fixed('True or false', 2, '(ii) False 2 marks'),), '2-7', WX),
    ('(iii)', 2, L(11, '(iii) What is the name given to the lines', 'equal pressure?'),
     '(iii) Isobars', '(iv) Occluded', (fixed('Term', 2, '(iii) Isobars 2 marks'),), '2-7', WX),
    ('(iv)', 2, L(11, '(iv) Name the type of weather front around Storm Ashley.'),
     '(iv) Occluded', 'Q.11', (fixed('Front', 2, '(iv) Occluded 2 marks'),), '2-7', WX),
], RIGHT)

Q11S = (L(12, 'Examine the infographic above', 'following questions.'),)
PART_ONE += p1_romans('11', 12, L(12, 'Graphical Interpretation'), Q11S, ID + 'p1-q11', True, ('page',), [
    ('(i)', 2, L(12, '(i) Which nationality', 'speak Irish?'), 'Q.11(i)', '(ii) 1,034,132',
     (fixed('Nationality', 2, 'Q.11(i) Australian 2 marks'),), '2-0', TG),
    ('(ii)', 2, L(12, '(ii) How many people responded', 'speak Irish well?'), '(ii) 1,034,132', '(iii) 34.4',
     (fixed('Number', 2, '(ii) 1,034,132 2 marks'),), '2-0', TG),
    ('(iii)', 2, L(12, '(iii) The Census in 2022', 'third level education.'), '(iii) 34.4', '(iv) Valid answer 2 marks',
     (fixed('Percentage', 2, '(iii) 34.4 (%) 2 marks'),), '2-0', TG),
    ('(iv)', 2, L(12, '(iv) State one way that the Irish government', 'speaking of Irish.'),
     '(iv) Valid answer 2 marks', 'Q.12', (fixed('One way', 2, '(iv) Valid answer 2 marks'),),
     '1-3', (H + 'regions-ireland',)),
], RIGHT)

Q12S = (L(13, 'Examine the pie charts above', 'following questions.'),)
PART_ONE += p1_romans('12', 13, L(13, 'Graphical Interpretation'), Q12S, ID + 'p1-q12', True, ('page',), [
    ('(i)', 2, L(13, '(i) What percentage (%) of cars purchased in 2020 were electric?'),
     'Q.12 (i)', '(ii) 13', (fixed('Percentage', 2, 'Q.12 (i) 3 (%) 2 marks'),), '2-0', TG),
    ('(ii)', 2, L(13, '(ii) Calculate X', 'purchased in 2020.'),
     '(ii) 13', '(iii) True', (fixed('Calculation', 2, '(ii) 13 (%) 2 marks'),), '2-0', TG),
    ('(iii)', 2, L(13, '(iii) State whether the following statement is true or false', 'from 2020 to 2024.'),
     '(iii) True', '(iv) Valid answer 1 +1', (fixed('True or false', 2, '(iii) True 2 marks'),), '2-0', TG),
    ('(iv)', 2, L(13, '(iv) Explain briefly one way to encourage increased electric car ownership.'),
     '(iv) Valid answer 1 +1', None, (fixed('One way', 2, '(iv) Valid answer 1 +1 mark', (0, 1, 2)),),
     '3-5', (H + 'economic-energy',)),
], RIGHT)


# ---------------------------------------------------------------- Part Two --
def romans(q, page, title, stem, first_id, sources, parts):
    """A-part romans. parts: (sub, marks, prompt, scheme slices, criteria, topic, atlas)."""
    out = []
    for index, (sub, marks, prompt, scheme, criteria, topic, atlas) in enumerate(parts):
        roman = sub.strip('()')
        out.append(T(f'p2-{q.lower()}-{roman}', P2, q, sub, marks, page, title, (prompt,), scheme,
                     criteria, topic, atlas, first_id if index == 0 else f'{first_id}-{roman}',
                     index == 0, sources, stem))
    return out


def sketch(outline_line, outline_permitted, alloc, item_permitted, labels):
    return (fixed('Sketch outline' if 'Sketch' in outline_line else 'Map outline', 4,
                  outline_line, outline_permitted),
            *(Criterion(f'Feature {n}', 4, item_permitted, 'exact', alloc) for n in range(1, labels + 1)))


OS_SKETCH = sketch('Sketch Outline · 4 marks (4/0)', (0, 4),
                   ('4 features @ 4 marks each', 'Label 1 mark'), sums((0, 1, 3), (0, 1)), 4)
GRAPH = (fixed('Title', 2, ('Bar Chart · Pie Chart', 'Title · 2 marks · 2 marks')),
         fixed('Axes named (bar chart) / circle and centre (pie chart)', 2,
               ('Vertical axis named', 'Horizontal axis named'), (0, 1, 2)),
         fixed('6 items illustrated', 12, '6 items illustrated', upto(12)))


def pair(line, label):
    return fixed(label, 4, line, (0, 2, 4))


def chosen(items, k):
    return [(combo, ' + '.join(item.rstrip('.') for item in combo),
             '-'.join(slug(item, 34) for item in combo))
            for combo in itertools.combinations(items, k)]


def bullet_routes(prefix, items, k=1, atlas=None):
    return tuple(Route(route_slug, label, ID + prefix + route_slug, True, keep_bullets=combo,
                       atlas=(atlas[combo[0]] if atlas else None))
                 for combo, label, route_slug in chosen(items, k))


def factors_two(page, head='Factors identified'):
    return ((S(page, head, 'Annotation'),),
            (pair('Factors identified · 2 + 2 marks', 'Factors identified'),
             srp('Examination of the two factors (7/6 and 6/7 SRPs)', 13,
                 ('Examination of Factor 1 · 7/6 x SRPs', 'Examination of Factor 2 · 6/7 x SRPs'))))


LANDFORMS = 'one fluvial landform or one coastal landform or one glacial landform'
EV = (H + 'earthquakes-volcanoes',)
SEA = (H + 'the-sea',)

PART_TWO = [
    T('p2-1a', P2, '1A', '', 20, 3, L(3, 'Ordnance Survey Map'),
      (L(3, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper.', 'route of the N59 road.'),),
      (S(5, 'Sketch Outline', None),), OS_SKETCH, '2-6', MAP, ID + 'p2-q1a', False, ('map', 'legend'),
      row_labels=(None, L(3, 'The entire area of Lough Corrib'),
                  L(3, 'The course of the Owenriff river from M 089 417 to where it enters Lough Corrib'),
                  L(3, 'Buffy Lough'), L(3, 'The entire route of the N59 road'))),
    T('p2-1b', P2, '1B', '', 30, 3, L(3, 'Rocks and Landscapes'),
      (L(3, 'Examine how different rock types produce distinctive landscapes', 'that you have studied.'),),
      (S(6, 'Rock 1 and associated landscape named', 'Annotation'),),
      (pair('Rock 1 and associated landscape named · 2 + 2 marks', 'Rock 1 and associated landscape named'),
       pair('Rock 2 and associated landscape named · 2 + 2 marks', 'Rock 2 and associated landscape named'),
       srp('Examination', 11, 'Examination · 11 x SRPs')),
      '0-1', RW, ID + 'p2-q1b', True),
    T('p2-1c', P2, '1C', '', 30, 3, L(3, 'Isostasy'),
      (L(3, 'Describe and explain how isostasy has shaped the Irish landscape.'),),
      (S(7, 'Impact/feature identified · 2 marks', 'Annotation'),),
      (fixed('Impact/feature identified', 2, 'Impact/feature identified · 2 marks'),
       srp('Description/explanation', 14, 'Description/explanation · 14 x SRPs')),
      '0-5', SEA + (H + 'rivers',), ID + 'p2-q1c', True),
]

Q2AS = (L(4, 'Examine the image and text above relating to the Tonga', 'following questions.'),)
PART_TWO += romans('2A', 4, L(4, 'The Tectonic Cycle'), Q2AS, ID + 'p2-q2a', ('page',), [
    ('(i)', 2, L(4, '(i) To what height, in metres, did the tsunami waves reach?'),
     (S(8, '(i) · 15', '(ii) · Valid impact'),), (fixed('Height', 2, '(i) · 15 (metres) · 2 marks'),), '0-7', EV),
    ('(ii)', 2, L(4, '(ii) Give one impact on the Tongan islands', 'and tsunami.'),
     (S(8, '(ii) · Valid impact', '(iii) · Four'),), (fixed('Impact', 2, '(ii) · Valid impact · 2 marks'),), '0-7', EV),
    ('(iii)', 2, L(4, '(iii) How many people died', 'and tsunami?'),
     (S(8, '(iii) · Four', '(iv) · Valid answer'),), (fixed('Deaths', 2, '(iii) · Four · 2 marks'),), '0-7', EV),
    ('(iv)', 4, L(4, '(iv) State two ways in which volcanic eruptions can be predicted.'),
     (S(8, '(iv) · Valid answer', '(v) · Seismograph'),), (pair('(iv) · Valid answer · 2 + 2 marks', 'Two ways'),), '0-7', EV),
    ('(v)', 2, L(4, '(v) A tsunami can also be triggered', 'earthquake activity.'),
     (S(8, '(v) · Seismograph', '(vi) · Valid explanation'),), (fixed('Instrument', 2, '(v) · Seismograph · 2 marks'),), '0-7', EV),
    ('(vi)', 8, L(4, '(vi) Explain briefly two ways to limit the impact of earthquakes.'),
     (S(8, '(vi) · Valid explanation', None),),
     (pair('(vi) · Valid explanation · 2 + 2 marks', 'First way'), pair('=2 + 2 marks', 'Second way')), '0-7', EV),
])

MNC_HEADINGS = ('Sourcing of raw materials and components', 'Location of processing units', 'Location of markets.')
URBAN_PROBLEMS = ('Pollution', 'Transport', 'Housing.')
PART_TWO += [
    T('p2-2b', P2, '2B', '', 30, 4, L(4, 'Surface Processes'),
      (L(4, '(i) Examine the role of the process of deposition', 'that you have studied.'),),
      (S(9, 'Landform named · 2 marks', 'Annotation'),),
      (fixed('Landform named', 2, 'Landform named · 2 marks'), srp('Examination', 14, 'Examination · 14 x SRPs')),
      '0-9', (H + 'rivers',), ID + 'p2-q2b-route-i-fluvial-landform', True,
      routes=(
          Route('route-i-fluvial-landform', 'Route (i) · one fluvial landform', ID + 'p2-q2b-route-i-fluvial-landform',
                True, ((LANDFORMS, 'one fluvial landform'),), topic='0-9', atlas=(H + 'rivers',)),
          Route('route-i-coastal-landform', 'Route (i) · one coastal landform', ID + 'p2-q2b-route-i-coastal-landform',
                True, ((LANDFORMS, 'one coastal landform'),), topic='0-10', atlas=SEA),
          Route('route-i-glacial-landform', 'Route (i) · one glacial landform', ID + 'p2-q2b-route-i-glacial-landform',
                True, ((LANDFORMS, 'one glacial landform'),), topic='0-11', atlas=(H + 'glaciation',)),
          Route('route-ii', 'Route (ii)', ID + 'p2-q2b-route-ii', True,
                prompt=(L(4, '(ii) Describe and explain the factors governing', 'process that you have studied.'),),
                scheme=(S(10, 'Factors identified', 'Annotation'),),
                criteria=(pair('Factors identified · 2 + 2 marks', 'Factors identified'),
                          fixed('Mass movement process named', 2, 'Mass movement process named · 2 marks'),
                          srp('Description/explanation', 12, 'Description/explanation · 12 x SRPs')),
                topic='0-8', atlas=RW),
      )),
    T('p2-2c', P2, '2C', '', 30, 4, L(4, 'Weathering'),
      (L(4, 'Explain one process of physical weathering and one process of chemical weathering.'),),
      (S(11, 'Physical weathering process named', 'Annotation'),),
      (fixed('Physical weathering process named', 2, 'Physical weathering process named · 2 marks'),
       fixed('Chemical weathering process named', 2, 'Chemical weathering process named · 2 marks'),
       srp('Explanation of the two processes (7/6 and 6/7 SRPs)', 13,
           ('Explanation of physical weathering · 7/6 x SRPs', 'Explanation of chemical weathering · 6/7 x SRPs'))),
      '0-8', RW, ID + 'p2-q2c', True),
]

Q3AS = (L(5, 'Examine the diagram above and answer each of the following questions.'),)
PART_TWO += romans('3A', 5, L(5, 'Coastal Landforms'), Q3AS, ID + 'p2-q3a', ('page',), [
    ('(i)', 12, L(5, '(i) Name each of the landforms formed by coastal processes', 'E and F.'),
     (S(12, '(i) · A = Headland', '(ii) · Specific processes'),),
     tuple(fixed(f'Landform {x}', 2, line) for x, line in zip('ABCDEF', (
         '(i) · A = Headland', 'B = Blowhole', 'C = Bay', 'D = Sea Stack', 'E = Wave-cut platform', 'F = Cave'))),
     '0-10', SEA),
    ('(ii)', 4, L(5, '(ii) Name two specific processes of coastal erosion.'),
     (S(12, '(ii) · Specific processes', '(iii) Valid explanation'),),
     (pair('(ii) · Specific processes named · 2 + 2 marks', 'Two processes'),), '0-10', SEA),
    ('(iii)', 4, L(5, '(iii) Explain briefly what is meant by wave refraction.'),
     (S(12, '(iii) Valid explanation', None),), (pair('(iii) Valid explanation · 2 + 2 marks', 'Explanation'),), '0-10', SEA),
])

ROCK = ('Mining', 'Extraction of building materials', 'Oil/Gas exploitation', 'Geothermal energy production.')
PART_TWO += [
    T('p2-3b', P2, '3B', '', 30, 5, L(5, 'Human Interaction with the Rock Cycle'),
      (L(5, 'Describe and explain how humans interact with the rock cycle', 'Geothermal energy production.'),),
      (S(13, 'Description/Explanation · 15 x SRPs', 'Annotation'),),
      (srp('Description/explanation', 15, 'Description/Explanation · 15 x SRPs'),),
      '0-6', RW, ID + 'p2-q3b-mining', True, routes=bullet_routes('p2-q3b-', ROCK)),
    T('p2-3c', P2, '3C', '', 30, 5, L(5, 'Landform Development'),
      (L(5, 'Examine how one of the following influences the development of landforms:', 'Faulting.'),),
      (S(14, 'Landform identified · 2 marks', 'Annotation'),),
      (fixed('Landform identified', 2, 'Landform identified · 2 marks'), srp('Examination', 14, 'Examination · 14 x SRPs')),
      '0-2', RW, ID + 'p2-q3c-folding', True, routes=bullet_routes('p2-q3c-', ('Folding', 'Faulting.'))),
    # Question 4
    T('p2-4a', P2, '4A', '', 20, 6, L(6, 'Map Skills'),
      (L(6, 'Draw an outline map of Ireland.', 'in that region.'),),
      (S(15, 'Map outline', None),),
      sketch('Map outline · 4 marks graded (4/2/0)', (0, 2, 4),
             ('4 features @ 4 marks each', 'Named 2 marks'), sums((0, 1, 2), (0, 2)), 4),
      '1-4', (H + 'regions-ireland',), ID + 'p2-q4a', True,
      row_labels=(None, L(6, 'The outline of one named region'), L(6, 'One named urban centre in that region'),
                  L(6, 'One named river in that region'),
                  L(6, 'The outline of one named feature of relief (upland or lowland) in that region'))),
    T('p2-4b', P2, '4B', '', 30, 6, L(6, 'Primary Economic Activity'),
      (L(6, 'Examine two factors that have influenced the development of primary economic activity', 'that you have studied.'),),
      *factors_two(16), '1-6', (H + 'regions-continental',), ID + 'p2-q4b', True),
    T('p2-4c', P2, '4C', '', 30, 6, L(6, 'European Union', nth=0),
      (L(6, 'Explain each of the following challenges', 'Economic challenges.'),),
      (S(17, 'Social challenge identified · 2 marks', 'Annotation'),),
      (fixed('Social challenge identified', 2, 'Social challenge identified · 2 marks'),
       fixed('Economic challenge identified', 2, 'Economic challenge identified · 2 marks'),
       srp('Explanation of the social and economic challenges (7/6 and 6/7 SRPs)', 13,
           ('Explanation of social challenges · 7/6 x SRPs', 'Explanation of economic challenges · 6/7 x SRPs'))),
      '1-3', (H + 'regions-european',), ID + 'p2-q4c', True),
]

Q5AS = (L(7, 'Examine the graph above showing first time asylum applications', 'following questions.'),)
POP = (H + 'human-population',)
PART_TWO += romans('5A', 7, L(7, 'European Union', nth=0), Q5AS, ID + 'p2-q5a', ('page',), [
    ('(i)', 2, L(7, '(i) Which country received the highest number', 'period shown?'),
     (S(18, '(i) · Germany', '(ii) · Spain'),), (fixed('Country', 2, '(i) · Germany · 2 marks'),), '2-0', TG),
    ('(ii)', 2, L(7, '(ii) Which country had a larger number', 'compared to January?'),
     (S(18, '(ii) · Spain', '(iii) · 1,775'),), (fixed('Country', 2, '(ii) · Spain · 2 marks'),), '2-0', TG),
    ('(iii)', 2, L(7, '(iii) How many new first time applications', 'January 2024?'),
     (S(18, '(iii) · 1,775', '(iv) · 13,324'),), (fixed('Applications', 2, '(iii) · 1,775 · 2 marks'),), '2-0', TG),
    ('(iv)', 4, L(7, '(iv) Calculate the average asylum applications', 'countries shown.'),
     (S(18, '(iv) · 13,324', '(v) · Valid reason'),), (fixed('Average', 4, '(iv) · 13,324 · 4 marks'),), '2-0', TG),
    ('(v)', 2, L(7, '(v) State one possible reason why migration into the EU is high.'),
     (S(18, '(v) · Valid reason', '(vi) · Valid explanation'),), (fixed('Reason', 2, '(v) · Valid reason · 2 marks'),), '4-2', POP),
    ('(vi)', 4, L(7, '(vi) Explain briefly one benefit of increased migration for the European Union.'),
     (S(18, '(vi) · Valid explanation', '(vii) Valid explanation'),),
     (pair('(vi) · Valid explanation · 2 + 2 marks', 'Benefit'),), '4-2', POP),
    ('(vii)', 4, L(7, '(vii) Explain briefly one challenge that the European Union faces', 'inward migration.'),
     (S(18, '(vii) Valid explanation', None),), (pair('(vii) Valid explanation · 2 + 2 marks', 'Challenge'),), '4-2', POP),
])

PART_TWO += [
    T('p2-5b', P2, '5B', '', 30, 7, L(7, 'Tertiary Economic Activity'),
      (L(7, 'Examine two factors that have influenced the development of one tertiary economic activity', 'that you have studied.'),),
      *factors_two(19), '1-4', (H + 'regions-ireland',), ID + 'p2-q5b', True),
    T('p2-5c', P2, '5C', '', 30, 7, L(7, 'Concept of a Region'),
      (L(7, 'Examine how climate or geomorphology can be used to define regions', 'that you have studied.'),),
      (S(20, 'Example · 2 marks', 'Annotation'),),
      (fixed('Example', 2, 'Example · 2 marks'), srp('Examination', 14, 'Examination · 14 x SRPs')),
      '1-0', (H + 'regions-european', H + 'regions-ireland'), ID + 'p2-q5c-climate', True,
      routes=(Route('climate', 'climate', ID + 'p2-q5c-climate', True, (('climate or geomorphology', 'climate'),)),
              Route('geomorphology', 'geomorphology', ID + 'p2-q5c-geomorphology', True,
                    (('climate or geomorphology', 'geomorphology'),)))),
]

Q6AS = (L(8, 'Examine the table above showing information on the seafood sector', 'following questions.'),)
IRL = (H + 'regions-ireland',)
PART_TWO += romans('6A', 8, L(8, 'Coastal Employment in Ireland'), Q6AS, ID + 'p2-q6a', ('page',), [
    ('(i)', 2, L(8, '(i) Which region had the highest coastal population?'),
     (S(21, '(i) · South', '(ii) · 4'),), (fixed('Region', 2, '(i) · South · 2 marks'),), '2-0', TG),
    ('(ii)', 2, L(8, '(ii) In the South East region what percentage', 'seafood sector?'),
     (S(21, '(ii) · 4', '(iii) · 3'),), (fixed('Percentage', 2, '(ii) · 4 (%) · 2 marks'),), '2-0', TG),
    ('(iii)', 4, L(8, '(iii) Calculate X', 'North East region.'),
     (S(21, '(iii) · 3', '(iv) · North and North West'),), (fixed('Calculation', 4, '(iii) · 3 (%) · 4 marks'),), '2-0', TG),
    ('(iv)', 4, L(8, '(iv) Name two regions where the percentage', 'national average.'),
     (S(21, '(iv) · North and North West', '(v) · Valid example'),),
     (pair('(iv) · North and North West · 2 + 2 marks', 'Two regions'),), '2-0', TG),
    ('(v)', 4, L(8, '(v) Name two Irish fishing ports.'),
     (S(21, '(v) · Valid example', '(vi) · Valid explanation'),), (pair('(v) · Valid example · 2 + 2 marks', 'Two ports'),), '1-4', IRL),
    ('(vi)', 4, L(8, '(vi) Explain briefly one challenge facing the seafood sector.'),
     (S(21, '(vi) · Valid explanation', None),), (pair('(vi) · Valid explanation · 2 + 2 marks', 'Challenge'),), '1-4', IRL),
])

PART_TWO += [
    T('p2-6b', P2, '6B', '', 30, 8, L(8, 'Secondary Economic Activity'),
      (L(8, 'Examine two factors that have influenced the development of secondary economic activity', 'that you have studied.'),),
      *factors_two(22), '1-5', (H + 'regions-european',), ID + 'p2-q6b', True),
    T('p2-6c', P2, '6C', '', 30, 8, L(8, 'Urban Development'),
      (L(8, 'Examine the factors that have influenced the development of one urban area', 'that you have studied.'),),
      (S(23, 'Urban area named · 2 marks', 'Annotation'),),
      (fixed('Urban area named', 2, 'Urban area named · 2 marks'),
       pair('Factors identified · 2 + 2 marks', 'Factors identified'),
       srp('Examination', 12, 'Examination · 12 x SRPs')),
      '1-6', (H + 'regions-continental',), ID + 'p2-q6c', True),
    # Question 7
    T('p2-7a', P2, '7A', '', 20, 10, L(10, 'Ordnance Survey Map'),
      (L(10, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper.', 'south of northing 40.'),),
      (S(25, 'Sketch Outline', None),), OS_SKETCH, '2-6', MAP, ID + 'p2-q7a', False, ('map', 'legend'),
      row_labels=(None, L(10, 'The golf course'), L(10, 'The viewpoint'),
                  L(10, 'The cycle route in the north west of the map'), L(10, 'An area of forestry south of northing 40'))),
    T('p2-7b', P2, '7B', '', 30, 10, L(10, 'Multinational Company'),
      (L(10, 'With reference to one multinational company', 'Location of markets.'),),
      (S(26, 'MNC named · 2 marks', 'Annotation'),),
      (fixed('MNC named', 2, 'MNC named · 2 marks'),
       srp('Description and explanation 1', 7, 'Description and explanation 1 · 7 x SRPs'),
       srp('Description and explanation 2', 7, 'Description and explanation 2 · 7 x SRPs')),
      '3-2', (H + 'economic-multinationals-globalisation',),
      *pool(ID + 'p2-q7b-', MNC_HEADINGS, 2)[:1], True, absorbs=pool(ID + 'p2-q7b-', MNC_HEADINGS, 2)[1]),
    T('p2-7c', P2, '7C', '', 30, 10, L(10, 'Colonialism'),
      (L(10, 'Examine the challenges resulting from colonialism', 'have studied.'),),
      (S(27, 'Challenges identified · 2 + 2 marks', 'Annotation'),),
      (pair('Challenges identified · 2 + 2 marks', 'Challenges identified'),
       fixed('Developing economy named', 2, 'Developing economy named · 2 marks'),
       srp('Examination', 12, 'Examination · 12 x SRPs')),
      '3-1', (H + 'economic-developing-economies',), ID + 'p2-q7c', True),
]

Q8AS = (L(11, 'Examine the charts above showing electricity generation', 'following questions.'),)
ENERGY = (H + 'economic-energy',)
PART_TWO += romans('8A', 11, L(11, 'Electricity Generation', nth=0), Q8AS, ID + 'p2-q8a', ('page',), [
    ('(i)', 2, L(11, '(i) What was the largest fuel source', 'in 2022?'),
     (S(28, '(i) Gas', '(ii) Hydro'),), (fixed('Largest source', 2, '(i) Gas · 2 marks'),), '2-0', TG),
    ('(ii)', 2, L(11, '(ii) What was the smallest fuel source', 'in 2012?'),
     (S(28, '(ii) Hydro', '(iii) Peat and Coal'),), (fixed('Smallest source', 2, '(ii) Hydro · 2 marks'),), '2-0', TG),
    ('(iii)', 4, L(11, '(iii) Name two sources of electricity generation that declined', '2012 to 2022.'),
     (S(28, '(iii) Peat and Coal', '(iv) 13'),), (pair('(iii) Peat and Coal · 2 + 2 marks', 'Two sources'),), '2-0', TG),
    ('(iv)', 2, L(11, '(iv) By what percentage (%) did wind increase', '2012 to 2022?'),
     (S(28, '(iv) 13', '(v) 12'),), (fixed('Increase', 2, '(iv) 13 (%) · 2 marks'),), '2-0', TG),
    ('(v)', 4, L(11, '(v) Calculate X', 'from coal in 2022.'),
     (S(28, '(v) 12', '(vi) Valid source'),), (fixed('Calculation', 4, '(v) 12 (%) · 4 marks'),), '2-0', TG),
    ('(vi)', 2, L(11, '(vi) Other than hydro and wind', 'renewable energy.'),
     (S(28, '(vi) Valid source', '(vii) Valid explanation'),), (fixed('Renewable source', 2, '(vi) Valid source · 2 marks'),), '3-5', ENERGY),
    ('(vii)', 4, L(11, '(vii) Explain briefly one negative impact', 'electricity generation.'),
     (S(28, '(vii) Valid explanation', None),), (pair('(vii) Valid explanation · 2 + 2 marks', 'Negative impact'),),
     '3-4', (H + 'economic-environmental-impact',)),
])

HEADING = ('Three headings @ 10 marks each', 'For each of the three headings:', 'Named example · 2 marks',
           'Map evidence · 2 marks', 'Discussion · 3 x SRPs')
PART_TWO += [
    T('p2-8b', P2, '8B', '', 30, 11, L(11, 'Tertiary Economic Activities'),
      (L(11, 'Using evidence from the 1:50 000 Ordnance Survey map of Oughterard', 'Attractions.'),),
      (S(29, 'Three headings @ 10 marks each', 'Annotation'),),
      tuple(Criterion(f'Heading {n}', 10, evens(10), 'srp', HEADING) for n in (1, 2, 3)),
      '3-0', (H + 'elective-economic', H + 'mapwork'), ID + 'p2-q8b', False, ('map', 'legend'),
      row_labels=(L(11, 'Accessibility'), L(11, 'Services (excluding transport)'), L(11, 'Attractions.'))),
    T('p2-8c', P2, '8C', '', 30, 11, L(11, 'European Union Policy'),
      (L(11, 'Examine how European Union policy/policies impact on the Irish economy.'),),
      (S(30, 'Impact on the Irish economy identified', 'Annotation'),),
      (fixed('Impact on the Irish economy identified', 2, 'Impact on the Irish economy identified · 2 marks'),
       fixed('Reference to EU policy', 2, 'Reference to EU policy · 2 marks'),
       srp('Examination', 13, 'Examination · 13 x SRPs')),
      '3-3', (H + 'economic-european-union',), ID + 'p2-q8c', True),
]

Q9AS = (L(12, 'Examine the data above showing the average life expectancy', 'following questions.'),)
PART_TWO += romans('9A', 12, L(12, 'HDI – Life Expectancy'), Q9AS, ID + 'p2-q9a', ('page',), [
    ('(i)', 16, L(12, '(i) Using graph paper, draw a suitable graph to illustrate this data.'),
     (S(31, 'Bar Chart · Pie Chart', 'Annotation'),), GRAPH, '2-0', TG),
    ('(ii)', 4, L(12, '(ii) Explain briefly one reason why life expectancy is lowest in Africa.'),
     (S(32, 'Valid explanation · 2 + 2 marks', None),), (pair('Valid explanation · 2 + 2 marks', 'Reason'),),
     '3-1', (H + 'economic-developing-economies',)),
])

FACTORS = ('Physical factors', 'Political factors', 'Human factors.')
ACTIVITY = 'footloose industries or financial services or mass tourism'
PART_TWO += [
    T('p2-9b', P2, '9B', '', 30, 12, L(12, 'Economic Development – Developed Economy'),
      (L(12, 'Examine the impact of two of the following on the development', 'Human factors.'),),
      (S(33, 'Named developed economy', 'Annotation'),),
      (fixed('Named developed economy', 2, 'Named developed economy · 2 marks'),
       srp('Examination of factor 1', 7, 'Examination of factor 1 · 7 x SRPs'),
       srp('Examination of factor 2', 7, 'Examination of factor 2 · 7 x SRPs')),
      '3-0', (H + 'elective-economic',), ID + 'p2-q9b-footloose-industries-physical-factors-political-factors', True,
      # Choose ONE printed activity (a route each); the choose-two factor pool
      # within it is one card.
      routes=tuple(Route(f'{slug(activity)}-{pool("", FACTORS, 2)[0]}', activity,
                         ID + f'p2-q9b-{slug(activity)}-{pool("", FACTORS, 2)[0]}', True, ((ACTIVITY, activity),),
                         absorbs=pool(ID + f'p2-q9b-{slug(activity)}-', FACTORS, 2)[1])
                   for activity in ('footloose industries', 'financial services', 'mass tourism'))),
    T('p2-9c', P2, '9C', '', 30, 12, L(12, 'Renewable Energy', nth=0),
      (L(12, 'With reference to one specific renewable energy source', 'Environmental advantages.'),),
      (S(34, 'Renewable energy source named · 2 marks', 'Annotation'),),
      (fixed('Renewable energy source named', 2, 'Renewable energy source named · 2 marks'),
       srp('Explanation of economic advantages', 7, 'Explanation of Economic advantages · 7 x SRPs'),
       srp('Explanation of environmental advantages', 7, 'Explanation of Environmental advantages · 7 x SRPs')),
      '3-5', ENERGY, ID + 'p2-q9c', True),
    # Question 10
    T('p2-10a', P2, '10A', '', 20, 13, L(13, 'Aerial Photograph'),
      (L(13, 'Examine the aerial photograph of Oughterard accompanying this paper.', 'in the foreground.'),),
      (S(35, 'Sketch Outline', None),), OS_SKETCH, '2-8', AER, ID + 'p2-q10a', False, ('aerial',),
      row_labels=(None, L(13, 'A sports field'), L(13, 'A bridge'), L(13, 'A church'),
                  L(13, 'A housing estate in the foreground'))),
    T('p2-10b', P2, '10B', '', 30, 13, L(13, 'Urban Planning'),
      (L(13, 'Examine the effectiveness of urban planning strategies', 'Housing.'),),
      (S(36, 'Example · 2 marks', 'Annotation'),),
      (fixed('Example', 2, 'Example · 2 marks'),
       srp('Examination of problem 1', 7, 'Examination of problem 1 · 7 x SRPs'),
       srp('Examination of problem 2', 7, 'Examination of problem 2 · 7 x SRPs')),
      '4-5', (H + 'human-urban-geography',), *pool(ID + 'p2-q10b-', URBAN_PROBLEMS, 2)[:1], True,
      absorbs=pool(ID + 'p2-q10b-', URBAN_PROBLEMS, 2)[1]),
    T('p2-10c', P2, '10C', '', 30, 13, L(13, 'Migration', nth=0),
      (L(13, 'Population movements have an impact on donor and receiver regions.', 'that you have studied.'),),
      (S(37, 'Impact on donor region identified · 2 marks', 'Annotation'),),
      (fixed('Impact on donor region identified', 2, 'Impact on donor region identified · 2 marks'),
       srp('Examination of impact on donor region', 6, 'Examination of impact on donor region · 6 x SRPs'),
       fixed('Impact on receiver region identified', 2, 'Impact on receiver region identified · 2 marks'),
       srp('Examination of impact on receiver region', 6, 'Examination of impact on receiver region · 6 x SRPs'),
       fixed('Example of a donor/receiver region', 2, 'Example of a donor/receiver region · 2 marks')),
      '4-2', POP, ID + 'p2-q10c', True),
]

Q11AS = (L(14, 'Examine the population pyramid above', 'following questions.'),)
PART_TWO += romans('11A', 14, L(14, 'Population', nth=0), Q11AS, ID + 'p2-q11a', ('page',), [
    ('(i)', 2, L(14, '(i) What percentage (%) of females', '70-74 age group?'),
     (S(39, '(i) 2', '(ii) 40-44'),), (fixed('Percentage', 2, '(i) 2 (%) · 2 marks'),), '2-0', TG),
    ('(ii)', 2, L(14, '(ii) Which age group has the largest number of males and females?'),
     (S(39, '(ii) 40-44', '(iii) Female'),), (fixed('Age group', 2, '(ii) 40-44 · 2 marks'),), '2-0', TG),
    ('(iii)', 4, L(14, '(iii) Do males or females live longer', 'support your answer.'),
     (S(39, '(iii) Female', '(iv) 15'),), (pair('(iii) Female + Valid evidence · 2 + 2 marks', 'Answer and evidence'),),
     '4-0', TG + POP),
    ('(iv)', 4, L(14, '(iv) Which of the following represents', '11% or 15% or 19%?'),
     (S(39, '(iv) 15', '(v) Valid explanation'),), (fixed('Percentage', 4, '(iv) 15 (%) · 4 marks'),), '2-0', TG),
    ('(v)', 4, L(14, '(v) Explain briefly what is meant by the term Dependency Ratio.'),
     (S(39, '(v) Valid explanation', '(vi) Valid explanation'),), (pair('(v) Valid explanation · 2 + 2 marks', 'Explanation'),), '4-0', POP),
    ('(vi)', 4, L(14, "(vi) Explain briefly one effect of the projected increase", 'dependency ratio.'),
     (S(39, '(vi) Valid explanation', None),), (pair('(vi) Valid explanation · 2 + 2 marks', 'Effect'),), '4-1', POP),
])

URB = (H + 'human-urban-geography',)
PART_TWO += [
    T('p2-11b', P2, '11B', '', 30, 15, L(15, 'Central Place Theory', nth=0),
      (L(15, 'Describe and explain Central Place Theory with reference to example(s) you have studied.'),),
      (S(40, 'Example · 2 marks', 'Annotation'),),
      (fixed('Example', 2, 'Example · 2 marks'), srp('Description/explanation', 14, 'Description/Explanation · 14 x SRPs')),
      '4-3', URB, ID + 'p2-q11b', True),
    T('p2-11c', P2, '11C', '', 30, 15, L(15, 'Dynamics of Population'),
      (L(15, 'Examine the impact/influence of any one of the following factors', 'Technology.'),),
      (S(41, 'Impact/influence identified', 'Annotation'),),
      (fixed('Impact/influence identified', 2, 'Impact/influence identified · 2 marks'),
       fixed('Example of location', 2, 'Example of location · 2 marks'),
       srp('Examination', 13, 'Examination · 13 x SRPs')),
      '4-0', POP, ID + 'p2-q11c-the-development-of-resources', True,
      routes=bullet_routes('p2-q11c-', ('The development of resources', 'Society and culture', 'Technology.'))),
]

Q12AS = (L(16, 'Examine the data above showing the number of UNESCO World Heritage sites', 'following questions.'),)
PART_TWO += romans('12A', 16, L(16, 'Heritage', nth=0), Q12AS, ID + 'p2-q12a', ('page',), [
    ('(i)', 16, L(16, '(i) Using graph paper, draw a suitable graph to illustrate this data.'),
     (S(42, 'Bar Chart · Pie Chart', 'Annotation'),), GRAPH, '2-0', TG),
    ('(ii)', 4, L(16, '(ii) Explain briefly one benefit of having a heritage site in an urban area.'),
     (S(43, 'Valid explanation · 2 + 2 marks', None),), (pair('Valid explanation · 2 + 2 marks', 'Benefit'),),
     '4-4', (H + 'urban-land-uses',)),
])

PART_TWO += [
    T('p2-12b', P2, '12B', '', 30, 16, L(16, 'Settlement Distribution'),
      (L(16, 'Examine the 1:50 000 Ordnance Survey map of Oughterard accompanying this paper.'),
       L(16, 'Using evidence from the map, account for variations', 'shown on the map.')),
      (S(44, 'Variations in settlement distribution identified', 'Annotation'),),
      (pair('Variations in settlement distribution identified · 2 + 2 marks', 'Variations identified'),
       fixed('OS map evidence', 2, 'OS map evidence · 2 marks'),
       srp('Examination', 12, 'Examination · 12 x SRPs')),
      '4-3', URB + MAP, ID + 'p2-q12b', False, ('map', 'legend')),
    T('p2-12c', P2, '12C', '', 30, 16, L(16, 'Urban Expansion'),
      (L(16, 'As cities grow and expand they impact on the surrounding areas.', 'that you have studied.'),),
      (S(45, 'Impact identified · 2 marks', 'Annotation'),),
      (fixed('Impact identified', 2, 'Impact identified · 2 marks'), fixed('Example', 2, 'Example · 2 marks'),
       srp('Discussion', 13, 'Discussion · 13 x SRPs')),
      '4-5', URB, ID + 'p2-q12c', True),
]

# ------------------------------------------------------------------ Options --
OC = (S(47, '*Overall Coherence (20 marks)', None, table=True),)
NOTE_P17 = L(17, 'Note: It is better to discuss', 'large number of points.')


def option(q, page, theme, note, prompt, scheme_page, topic, atlas, choice=None):
    card_id, absorbs = choice or (ID + f'p2-q{q}', ())
    return T(f'p2-{q}', P2, q, '', 80, page, theme, (prompt,),
             (S(scheme_page, 'Number of aspects', None), *OC),
             (Criterion('Aspects (3 @ 20 marks or 4 @ 15 marks)', 60, upto(60), 'srp',
                        ('Number of aspects', '?For each aspect:', 'Identifying aspect', 'Discussion · 8 x SRPs')),
              Criterion('Overall coherence', 20, (0, 6, 10, 14, 17, 20), 'exact',
                        ('Overall Coherence · 20 marks graded*', '*Overall Coherence (20 marks)', 'Excellent · 20',
                         'Very Good · 17', 'Good · 14', 'Fair · 10', 'Weak · 6', 'Poor · 0'))),
             topic, (atlas,), card_id, True, stem=(note,), absorbs=absorbs)


GI, GE = H + 'option-global-interdependence', H + 'option-geoecology'
CI, AO = H + 'option-culture-identity', H + 'option-atmosphere-ocean'
OPTIONS = [
    option('13', 18, L(18, 'Global Interdependence'), NOTE_P17,
           L(18, 'We live in an interdependent global economy.', 'Human rights issues.'), 49, '5-1', GI),
    option('14', 18, L(18, 'Global Interdependence'), NOTE_P17,
           L(18, 'Empowering people is a way of linking', 'Differing gender roles in society.'), 50, '5-2', GI,
           choice=pool(ID + 'p2-q14-', ('National debt', 'Aid programmes',
                                        'Levels of exploitation at local and global scales',
                                        'Differing gender roles in society.'), 3)),
    option('15', 18, L(18, 'Global Interdependence'), NOTE_P17,
           L(18, 'Examine sustainable development as a model for future development.'), 51, '5-3', GI),
    option('16', 18, L(18, 'Geoecology'), L(18, 'Note: It is better to discuss', 'large number of points.'),
           L(18, 'Examine how any three of the following processes', 'Soil erosion.'), 52, '6-1', GE,
           choice=pool(ID + 'p2-q16-', ('Weathering', 'Podzolisation', 'Calcification', 'Soil erosion.'), 3)),
    option('17', 18, L(18, 'Geoecology'), L(18, 'Note: It is better to discuss', 'large number of points.'),
           L(18, 'Examine the influence of mineral matter', 'soil development.'), 53, '6-0', GE),
    option('18', 18, L(18, 'Geoecology'), L(18, 'Note: It is better to discuss', 'large number of points.'),
           L(18, 'Biomes are altered by human activity.', 'Industrial development.'), 54, '6-3', GE),
    option('19', 19, L(19, 'Culture and Identity'), L(19, 'Note: It is better to discuss', 'large number of points.', nth=0),
           L(19, 'Examine the importance of religion as a cultural indicator.'), 55, '7-0', CI),
    option('20', 19, L(19, 'Culture and Identity'), L(19, 'Note: It is better to discuss', 'large number of points.', nth=0),
           L(19, 'Examine how different cultural groups', 'you have studied.'), 56, '7-1', CI),
    option('21', 19, L(19, 'Culture and Identity'), L(19, 'Note: It is better to discuss', 'large number of points.', nth=0),
           L(19, '‘Cultural identity is defined by many diverse factors’.', 'you have studied.'), 57, '7-2', CI),
    option('22', 19, L(19, 'The Atmosphere – Ocean Environment'), L(19, 'Note: It is better to discuss', 'large number of points.', nth=1),
           L(19, 'Describe the formation of each of the following', 'Land and sea breezes.'), 58, '8-3', AO),
    option('23', 19, L(19, 'The Atmosphere – Ocean Environment'), L(19, 'Note: It is better to discuss', 'large number of points.', nth=1),
           L(19, 'Give an account of how atmosphere-ocean phenomena', 'such measurements.'), 59, '8-0', AO),
    option('24', 19, L(19, 'The Atmosphere – Ocean Environment'), L(19, 'Note: It is better to discuss', 'large number of points.', nth=1),
           L(19, 'Examine how climate characteristics influence economic development.'), 60, '8-5', AO),
]

TASKS = [*PART_ONE, *PART_TWO, *OPTIONS]

ID_CORRECTION_REASON = (
    'The shipped card held every part of a question the scheme prices part by '
    'part. Its id is kept on the first separately priced part; the other parts '
    'are new cards with their own published allocation.')

# Every 2025 Higher card id shipped before this review (80). Each must survive.
LEGACY_IDS = [
    'geography-2025-hl-p1-q1',
    'geography-2025-hl-p1-q2',
    'geography-2025-hl-p1-q3',
    'geography-2025-hl-p1-q4',
    'geography-2025-hl-p1-q5',
    'geography-2025-hl-p1-q6',
    'geography-2025-hl-p1-q10',
    'geography-2025-hl-p1-q11',
    'geography-2025-hl-p1-q12',
    'geography-2025-hl-p2-q1b',
    'geography-2025-hl-p2-q1c',
    'geography-2025-hl-p2-q2a',
    'geography-2025-hl-p2-q2b-route-i-fluvial-landform',
    'geography-2025-hl-p2-q2b-route-i-coastal-landform',
    'geography-2025-hl-p2-q2b-route-i-glacial-landform',
    'geography-2025-hl-p2-q2b-route-ii',
    'geography-2025-hl-p2-q2c',
    'geography-2025-hl-p2-q3a',
    'geography-2025-hl-p2-q3b-mining',
    'geography-2025-hl-p2-q3b-extraction-of-building-materials',
    'geography-2025-hl-p2-q3b-oil-gas-exploitation',
    'geography-2025-hl-p2-q3b-geothermal-energy-production',
    'geography-2025-hl-p2-q3c-folding',
    'geography-2025-hl-p2-q3c-faulting',
    'geography-2025-hl-p2-q4a',
    'geography-2025-hl-p2-q4b',
    'geography-2025-hl-p2-q4c',
    'geography-2025-hl-p2-q5a',
    'geography-2025-hl-p2-q5b',
    'geography-2025-hl-p2-q5c-climate',
    'geography-2025-hl-p2-q5c-geomorphology',
    'geography-2025-hl-p2-q6a',
    'geography-2025-hl-p2-q6b',
    'geography-2025-hl-p2-q6c',
    'geography-2025-hl-p2-q7b-sourcing-of-raw-materials-and-comp-location-of-processing-units',
    'geography-2025-hl-p2-q7b-sourcing-of-raw-materials-and-comp-location-of-markets',
    'geography-2025-hl-p2-q7b-location-of-processing-units-location-of-markets',
    'geography-2025-hl-p2-q7c',
    'geography-2025-hl-p2-q8a',
    'geography-2025-hl-p2-q8c',
    'geography-2025-hl-p2-q9a',
    'geography-2025-hl-p2-q9b-footloose-industries-physical-factors-political-factors',
    'geography-2025-hl-p2-q9b-footloose-industries-physical-factors-human-factors',
    'geography-2025-hl-p2-q9b-footloose-industries-political-factors-human-factors',
    'geography-2025-hl-p2-q9b-financial-services-physical-factors-political-factors',
    'geography-2025-hl-p2-q9b-financial-services-physical-factors-human-factors',
    'geography-2025-hl-p2-q9b-financial-services-political-factors-human-factors',
    'geography-2025-hl-p2-q9b-mass-tourism-physical-factors-political-factors',
    'geography-2025-hl-p2-q9b-mass-tourism-physical-factors-human-factors',
    'geography-2025-hl-p2-q9b-mass-tourism-political-factors-human-factors',
    'geography-2025-hl-p2-q9c',
    'geography-2025-hl-p2-q10b-pollution-transport',
    'geography-2025-hl-p2-q10b-pollution-housing',
    'geography-2025-hl-p2-q10b-transport-housing',
    'geography-2025-hl-p2-q10c',
    'geography-2025-hl-p2-q11a',
    'geography-2025-hl-p2-q11b',
    'geography-2025-hl-p2-q11c-the-development-of-resources',
    'geography-2025-hl-p2-q11c-society-and-culture',
    'geography-2025-hl-p2-q11c-technology',
    'geography-2025-hl-p2-q12a',
    'geography-2025-hl-p2-q12c',
    'geography-2025-hl-p2-q13',
    'geography-2025-hl-p2-q14-national-debt-aid-programmes-levels-of-exploitation-at-local-an',
    'geography-2025-hl-p2-q14-national-debt-aid-programmes-differing-gender-roles-in-society',
    'geography-2025-hl-p2-q14-national-debt-levels-of-exploitation-at-local-an-differing-gender-roles-in-society',
    'geography-2025-hl-p2-q14-aid-programmes-levels-of-exploitation-at-local-an-differing-gender-roles-in-society',
    'geography-2025-hl-p2-q15',
    'geography-2025-hl-p2-q16-weathering-podzolisation-calcification',
    'geography-2025-hl-p2-q16-weathering-podzolisation-soil-erosion',
    'geography-2025-hl-p2-q16-weathering-calcification-soil-erosion',
    'geography-2025-hl-p2-q16-podzolisation-calcification-soil-erosion',
    'geography-2025-hl-p2-q17',
    'geography-2025-hl-p2-q18',
    'geography-2025-hl-p2-q19',
    'geography-2025-hl-p2-q20',
    'geography-2025-hl-p2-q21',
    'geography-2025-hl-p2-q22',
    'geography-2025-hl-p2-q23',
    'geography-2025-hl-p2-q24',
]
