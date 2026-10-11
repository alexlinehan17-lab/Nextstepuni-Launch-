"""Independent review ledger: Leaving Certificate Geography 2026 Higher Level.

Sources (English editions, Paper Trail index, sizes and SHA-256 pinned in
EXPECTED_SOURCES): Part One and Answerbook LC005ALP042EV (48 pages), Part Two
LC005ALP043EV (20 pages), marking scheme LC005ALP000EV (66 pages), and the
common companions — 1:50 000 Dundalk map LC005CLP003EV, its legend
LC005CLPC00EV and the Dundalk aerial photograph LC005CLP004EV.

Visual sweep (every page rendered and read on 2026-10-11):
  Part One booklet p1 cover; p2 instructions (Part One "Attempt any TEN",
  80 marks; Part Two "attempt FOUR", 320 marks); p3-p13 Questions 1-12 (p8
  holds Q6 and Q7); p14 Part Two answerbook instructions; p15-p18 graph-paper
  answer pages; p19-p47 lined answer pages; p48 copyright/back cover.
  Part Two booklet p1 cover; p2 Part Two instructions; p3-p5 Section 1
  (Q1-Q3); p6-p9 Section 2 (Q4-Q6); p10 Section 3 divider; p11-p16 Electives
  (Q7-Q12); p17 Section 4 divider; p18-p19 Options (Q13-Q24); p20 copyright.
  Scheme p1 cover; p2-p3 notes and annotation key; p4 Part One table (two
  columns: Q1-Q6, Q7-Q12); p5-p42 Part Two Q1-Q12 (one A/B/C task per page,
  2B route (ii) on p10); p43 Section 4 divider; p44 outline scheme and Overall
  Coherence descriptors; p45 option annotations; p46-p57 Q13-Q24; p58-p63
  Geographical Investigation (coursework, not a written-paper task); p64
  prescribed investigation topics; p65 Irish-language bonus marks; p66 blank.
  Companions: the map extract (Dundalk, eastings 01-13, northings 04-13), the
  OS legend sheet and the oblique aerial photograph of Dundalk. NOTE: the
  generator formerly attached CLPC00 as the "map extract" and CLP003 as the
  "legend"; the renders show the reverse, and the ids are corrected here.

Boundaries. Every printed part the scheme prices separately is its own task:
Part One (i), (ii) and lettered (ii)(a)/(b) true/false items; Part Two A-part
romans; every B/C task and every option. A part whose rows share ONE printed
instruction and ONE closed answer pool (the Part One matching and location
tables, A-part "Name each of the features labelled A, B, C and D") stays one
task with a criterion per scheme row: the rows have no printed address of
their own and could only be separated by writing new prompts. The scheme's
roman/letter rows follow the printed table rows; this was checked visually
for Q1-Q6 and Q9 (e.g. Q2 Oxbow lake=C, River braiding=B, Lateral
moraines=D, Fjord=A against the four photographs).

Tariffs are read off the scheme: an "a + b marks" line is one criterion of
a+b with partial a; "n x SRPs" is n SRPs at 2 marks; sketch features are
"shown 3 (3/1/0) + label 1" (map/aerial) or "shown 2 (2/1/0) + named 2"
(outline map); options are aspects (3 @ 20 or 4 @ 15, select to benefit) up
to 60 plus Overall Coherence graded 20/17/14/10/6/0. Every task total equals
the paper's printed tariff ([8m], [20m], [30m], [80m]) and the scheme's own
split where it prints one ([16m] + [4m] for 9A and 10A).

Examiner annotation tables (REF/I/N/Ex/Dg icons) restate allocations already
printed above them and are not carried into guidance.
"""

from geography_review import (
    Criterion, Lift, Route, SchemeSlice, Task, evens, fixed, srp, upto,
)

YEAR = 2026
LEVEL = 'higher'
PAPER_PAGES = {1: 48, 2: 20}
SCHEME_PAGES = 66
QUESTION_TARIFFS = {1: {str(n): 8 for n in range(1, 13)},
                    2: {**{f'{n}{x}': (20 if x == 'A' else 30)
                           for n in range(1, 13) for x in 'ABC'},
                        **{str(n): 80 for n in range(13, 25)}}}

EXPECTED_SOURCES = {
    'paper1': ('LC005ALP042EV.pdf', 14862721),
    'paper2': ('LC005ALP043EV.pdf', 6478560),
    'scheme': ('LC005ALP000EV.pdf', 6725463),
}

PAGE_REVIEW = {
    'paper1': {1: 'cover', 2: 'instructions', **{p: 'question' for p in range(3, 14)},
               14: 'answerbook instructions', **{p: 'graph-paper answer page' for p in range(15, 19)},
               **{p: 'lined answer page' for p in range(19, 48)}, 48: 'copyright/back cover'},
    'paper2': {1: 'cover', 2: 'Part Two instructions', **{p: 'question' for p in (3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 18, 19)},
               10: 'section divider', 17: 'section divider', 20: 'copyright/back cover'},
    'scheme': {1: 'cover', 2: 'notes', 3: 'notes and annotation key', 4: 'Part One table',
               **{p: 'Part Two allocation' for p in range(5, 43)}, 43: 'section divider',
               44: 'option outline and coherence descriptors', 45: 'option annotations',
               **{p: 'option allocation' for p in range(46, 58)},
               **{p: 'geographical investigation (coursework)' for p in range(58, 64)},
               64: 'prescribed investigation topics', 65: 'Irish-language bonus marks', 66: 'blank'},
}

# Raw selection directives found on the paper pages, each classified. The
# generator rescans the PDFs and fails if this list drifts in either direction.
EXPECTED_SELECTION_SCAN = [
    [1, 2, 'attempt any ten'], [1, 2, 'attempt four'], [1, 3, 'attempt any ten'],
    [2, 2, 'attempt four'],
    [2, 4, 'answer (i) or (ii)'], [2, 4, 'or one'], [2, 4, 'or one'],
    [2, 5, 'one of the following'],
    [2, 6, 'any two'],
    [2, 8, 'any two'],
    [2, 18, 'three of the following'],
]
SELECTION_REVIEW = [
    {'scan': [[1, 2, 'attempt any ten'], [1, 2, 'attempt four'], [1, 3, 'attempt any ten'], [2, 2, 'attempt four']],
     'kind': 'exam-attempt-rule',
     'reason': 'Part One any ten of twelve and Part Two four questions are examination attempt rules; every question is carded, none is a practice combination.'},
    {'scan': [[2, 4, 'answer (i) or (ii)'], [2, 4, 'or one'], [2, 4, 'or one']],
     'kind': 'closed-route',
     'reason': '2B: (i) or (ii); route (i) itself offers one fluvial OR one coastal OR one glacial landform. Four routes: (i) x 3 landform families + (ii).'},
    {'scan': [[2, 5, 'one of the following']], 'kind': 'closed-choose-one',
     'reason': '3B: one of three printed bullets -> three routes.'},
    {'scan': [[2, 8, 'any two']], 'kind': 'closed-choose-two',
     'reason': '5C: any two of four printed factors -> C(4,2) = 6 routes.'},
    {'scan': [[2, 18, 'three of the following']], 'kind': 'closed-choose-three',
     'reason': '14: three of four printed themes -> C(4,3) = 4 routes.'},
    {'scan': [[2, 6, 'any two']], 'kind': 'open-response',
     'reason': '4B "any two factors" names no printed factor list, so it is an open choice. Open choices are not fanned out: "two features" (2A ii), "two pyroclastic materials", "one example", "two factors" (4B), "example(s)", "any city" (10B), "one multinational company", "one biome", "one global climate type", "a European region", "one developing world city", "one tertiary economic activity", "one source of renewable energy", "two countries". Required lists are compulsory: 1C sedimentary AND metamorphic, the sketch-map feature bullets, 21 nationality, language and religion.'},
]

P1, P2 = 1, 2
LEFT = (0.0, 0.0, 0.52, 1.0)
RIGHT = (0.5, 0.0, 1.0, 1.0)
ID = 'geography-2026-hl-'
H = 'geography-higher-'


def L(page, start, end=None, nth=None):
    return Lift(page, start, end, None, nth)


def S(page, start, end=None, clip=None, after=None, table=False):
    return SchemeSlice(page, start, end, clip, after, table)


# ---------------------------------------------------------------- Part One --
def matching(label_lines, marks=1):
    return tuple(fixed(f'Row {i}', marks, line) for i, line in enumerate(label_lines, 1))


TRUE_FALSE = '(ii) Indicate whether each of the following statements is true or false by ticking (✓) the correct box.'

PART_ONE = [
    Task('p1-1', P1, '1', '', 8, 3, L(3, 'Landscape Identification'),
         (L(3, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper.', 'Confluence.'),),
         (S(4, 'Q.1 (i) Meander', 'Q.2', LEFT),),
         matching(['(i) Meander', '(ii) Trellised Drainage Pattern', '(iii) V-shaped valley', '(iv) Confluence'], 2),
         '2-6', (H + 'mapwork', H + 'rivers'), ('page', 'map', 'legend'), ID + 'p1-q1', True,
         row_labels=(L(3, 'J 02 12'), L(3, 'J 08 07'), L(3, 'J 11 12'), L(3, 'J 02 09'))),
    # Q2 Features and Processes
    Task('p1-2-i', P1, '2', '(i)', 4, 4, L(4, 'Features and Processes'),
         (L(4, '(i) Match each of the photographs A, B, C and D', 'in the table below.'),),
         (S(4, 'Q.2 (i) C', '(ii) (a) False', LEFT),),
         matching(['Q.2 (i) C', 'B 1 mark', 'D 1 mark', 'A 1 mark']),
         '0-4', (H + 'rivers', H + 'glaciation'), ('page',), ID + 'p1-q2', True,
         stem=(L(4, 'Examine the photographs above and answer each of the following questions.'),),
         row_labels=(L(4, 'Oxbow lake'), L(4, 'River braiding'), L(4, 'Lateral moraines'), L(4, 'Fjord'))),
    Task('p1-2-ii-a', P1, '2', '(ii)(a)', 2, 4, L(4, 'Features and Processes'),
         (L(4, TRUE_FALSE), L(4, '(a) U-shaped valleys are features of river deposition.')),
         (S(4, '(ii) (a) False', '(b) True', LEFT, after='Q.2 (i)'),),
         (fixed('Statement (a)', 2, '(ii) (a) False'),),
         '0-11', (H + 'glaciation',), ('page',), ID + 'p1-q2-ii-a', False,
         stem=(L(4, 'Examine the photographs above and answer each of the following questions.'),)),
    Task('p1-2-ii-b', P1, '2', '(ii)(b)', 2, 4, L(4, 'Features and Processes'),
         (L(4, TRUE_FALSE), L(4, '(b) Scratches or grooves carved into bedrock by moving glaciers are known as striations.')),
         (S(4, '(b) True', 'Q.3', LEFT, after='Q.2 (i)'),),
         (fixed('Statement (b)', 2, '(b) True'),),
         '0-11', (H + 'glaciation',), ('page',), ID + 'p1-q2-ii-b', False,
         stem=(L(4, 'Examine the photographs above and answer each of the following questions.'),)),
    # Q3 Isostasy
    Task('p1-3-i', P1, '3', '(i)', 4, 5, L(5, 'Isostasy'),
         (L(5, '(i) Match each of the letters A, B, C, and D', 'in the table below.'),),
         (S(4, 'Q.3 (i) C', '(ii) Valid answer', LEFT),),
         matching(['Q.3 (i) C', 'B 1 mark', 'D 1 mark', 'A 1 mark']),
         '0-5', (H + 'the-sea',), ('page',), ID + 'p1-q3', True,
         stem=(L(5, 'Examine the diagram above and answer each of the following questions.'),),
         row_labels=(L(5, 'Cave'), L(5, 'Raised Cliff'), L(5, 'Raised Beach'), L(5, 'Raised Platform'))),
    Task('p1-3-ii', P1, '3', '(ii)', 4, 5, L(5, 'Isostasy'),
         (L(5, '(ii) Isostatic uplift impacts rivers.', 'has on rivers.'),),
         (S(4, '(ii) Valid answer 2 +2 marks', 'Q.4', LEFT),),
         (fixed('Two effects on rivers', 4, '(ii) Valid answer 2 +2 marks', (0, 2, 4)),),
         '0-5', (H + 'rivers',), ('page',), ID + 'p1-q3-ii', False,
         stem=(L(5, 'Examine the diagram above and answer each of the following questions.'),)),
    # Q4 The Rock Cycle
    Task('p1-4-i', P1, '4', '(i)', 4, 6, L(6, 'The Rock Cycle'),
         (L(6, '(i) Match each of the images A, B, C and D', 'table below.'),),
         (S(4, 'Q.4 (i) C', '(ii) (a) False', LEFT),),
         matching(['Q.4 (i) C', 'D 1 mark', 'A 1 mark', 'B 1 mark']),
         '0-1', (H + 'rocks-weathering-mass-movement',), ('page',), ID + 'p1-q4', True,
         stem=(L(6, 'Examine the images above and answer each of the following questions.'),),
         row_labels=(L(6, 'Marble'), L(6, 'Limestone', nth=0), L(6, 'Basalt', nth=0), L(6, 'Sandstone'))),
    Task('p1-4-ii-a', P1, '4', '(ii)(a)', 2, 6, L(6, 'The Rock Cycle'),
         (L(6, TRUE_FALSE), L(6, '(a) Basalt is a plutonic igneous rock.')),
         (S(4, '(ii) (a) False', '(b) False', LEFT, after='Q.4 (i)'),),
         (fixed('Statement (a)', 2, '(ii) (a) False'),),
         '0-1', (H + 'rocks-weathering-mass-movement',), ('page',), ID + 'p1-q4-ii-a', False,
         stem=(L(6, 'Examine the images above and answer each of the following questions.'),)),
    Task('p1-4-ii-b', P1, '4', '(ii)(b)', 2, 6, L(6, 'The Rock Cycle'),
         (L(6, TRUE_FALSE), L(6, '(b) Limestone is transformed into quartzite when placed under great heat/pressure.')),
         (S(4, '(b) False', 'Q.5', LEFT, after='Q.4 (i)'),),
         (fixed('Statement (b)', 2, '(b) False'),),
         '0-1', (H + 'rocks-weathering-mass-movement',), ('page',), ID + 'p1-q4-ii-b', False,
         stem=(L(6, 'Examine the images above and answer each of the following questions.'),)),
    # Q5 Tectonic Cycle and Faulting
    Task('p1-5-i', P1, '5', '(i)', 4, 7, L(7, 'Tectonic Cycle and Faulting'),
         (L(7, '(i) Match each of the letters A, B, C and D', 'table below.'),),
         (S(4, 'Q.5 (i) C', '(ii) (a) True', LEFT),),
         matching(['Q.5 (i) C', 'D 1 mark', 'A 1 mark', 'B 1 mark']),
         '0-7', (H + 'earthquakes-volcanoes',), ('page',), ID + 'p1-q5', True,
         stem=(L(7, 'Examine the diagram above and answer each of the following questions.'),),
         row_labels=(L(7, 'Fault line'), L(7, 'Seismic Waves'), L(7, 'Epicentre'), L(7, 'Focus'))),
    Task('p1-5-ii-a', P1, '5', '(ii)(a)', 2, 7, L(7, 'Tectonic Cycle and Faulting'),
         (L(7, TRUE_FALSE), L(7, '(a) Reverse faults are caused by compression.')),
         (S(4, '(ii) (a) True', '(b) True', LEFT, after='Q.5 (i)'),),
         (fixed('Statement (a)', 2, '(ii) (a) True'),),
         '0-2', (H + 'rocks-weathering-mass-movement',), ('page',), ID + 'p1-q5-ii-a', False,
         stem=(L(7, 'Examine the diagram above and answer each of the following questions.'),)),
    Task('p1-5-ii-b', P1, '5', '(ii)(b)', 2, 7, L(7, 'Tectonic Cycle and Faulting'),
         (L(7, TRUE_FALSE), L(7, '(b) Doming occurs when layers of rock are pushed upwards.')),
         (S(4, '(b) True', 'Q.6', LEFT, after='Q.5 (i)'),),
         (fixed('Statement (b)', 2, '(b) True'),),
         '0-2', (H + 'rocks-weathering-mass-movement',), ('page',), ID + 'p1-q5-ii-b', False,
         stem=(L(7, 'Examine the diagram above and answer each of the following questions.'),)),
    # Q6 Concept of a Region
    Task('p1-6-i', P1, '6', '(i)', 4, 8, L(8, 'Concept of a Region'),
         (L(8, '(i) Match each of the following types of region', 'Administrative'),),
         (S(4, 'Q.6(i) Administrative', '(ii) Co. Longford', LEFT),),
         matching(['Q.6(i) Administrative', 'Cultural 1 mark', 'Urban 1 mark', 'Geomorphological 1 mark']),
         '1-0', (H + 'regions-ireland',), ('page',), ID + 'p1-q6', True,
         stem=(L(8, 'Answer each of the following questions in the table below.'),),
         row_labels=(L(8, 'A region involved in governing', 'of an area.'),
                     L(8, 'A region where people share', 'traditions etc.'),
                     L(8, 'A region with high population', 'cities and towns.'),
                     L(8, 'A region with a unique', 'structure or relief.'))),
    Task('p1-6-ii', P1, '6', '(ii)', 4, 8, L(8, 'Concept of a Region'),
         (L(8, '(ii) Match each of the following examples of regions', 'The Burren'),),
         (S(4, '(ii) Co. Longford', None, LEFT),),
         matching(['(ii) Co. Longford', 'The Gaeltacht 1 mark', 'Munich 1 mark', 'The Burren 1 mark']),
         '1-0', (H + 'regions-ireland',), ('page',), ID + 'p1-q6-ii', False,
         stem=(L(8, 'Answer each of the following questions in the table below.'),),
         row_labels=(L(8, 'A region involved in governing', 'of an area.'),
                     L(8, 'A region where people share', 'traditions etc.'),
                     L(8, 'A region with high population', 'cities and towns.'),
                     L(8, 'A region with a unique', 'structure or relief.'))),
]


def map_skill(key, sub, page, prompt, line, start, end, card_id, legacy, topic, atlas,
              title, stem, sources, label):
    return Task(key, P1, sub[0], sub[1], 2, page, title, (prompt,),
                (S(4, start, end, RIGHT),), (fixed(label, 2, line),),
                topic, atlas, sources, card_id, legacy, stem=stem)


Q7_STEM = (L(8, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper, and answer each of the following questions.'),)
Q8_STEM = (L(9, 'Locate point X, J 120 130', 'on the Ordnance Survey map.'),
           L(9, 'Using the 1:50 000 Ordnance Survey map and legend and the elevation profile above, answer each of the following questions.'))
Q10_STEM = (L(11, 'The Ultraviolet Index (UV Index) measures', 'answer the following questions.'),)
Q11_STEM = (L(12, 'Examine the extract above outlining', 'each of the following questions.'),)
Q12_STEM = (L(13, 'Examine the graph above showing persons aged 25-34', 'answer the following questions.'),)

PART_ONE += [
    # Q7 Map Skills (map + legend; the printed page carries only answer boxes)
    Task('p1-7-i', P1, '7', '(i)', 2, 8, L(8, 'Map Skills'),
         (L(8, '(i) Give a six-figure grid reference', 'in Dundalk.'),),
         (S(4, 'Q.7 (i)', '(ii) Graveyard', RIGHT),), (fixed('Grid reference', 2, 'Q.7 (i) J 042 069'),),
         '2-6', (H + 'mapwork',), ('map', 'legend'), ID + 'p1-q7', True, stem=Q7_STEM),
    Task('p1-7-ii', P1, '7', '(ii)', 2, 8, L(8, 'Map Skills'),
         (L(8, '(ii) Name the antiquity shown', 'J 010 065.'),),
         (S(4, '(ii) Graveyard', '(iii) 10.1', RIGHT),), (fixed('Antiquity', 2, '(ii) Graveyard'),),
         '2-6', (H + 'mapwork',), ('map', 'legend'), ID + 'p1-q7-ii', False, stem=Q7_STEM),
    Task('p1-7-iii', P1, '7', '(iii)', 2, 8, L(8, 'Map Skills'),
         (L(8, '(iii) Measure the length, in kilometres', 'at J 061 110.'),),
         (S(4, '(iii) 10.1', '(iv) 21', RIGHT),), (fixed('Length', 2, '(iii) 10.1 (km)'),),
         '2-6', (H + 'mapwork',), ('map', 'legend'), ID + 'p1-q7-iii', False, stem=Q7_STEM),
    Task('p1-7-iv', P1, '7', '(iv)', 2, 8, L(8, 'Map Skills'),
         (L(8, '(iv) Calculate the approximate area of land', 'on the map.'),),
         (S(4, '(iv) 21', 'Q.8', RIGHT),), (fixed('Area', 2, '(iv) 21 (km²)'),),
         '2-6', (H + 'mapwork',), ('map', 'legend'), ID + 'p1-q7-iv', False, stem=Q7_STEM),
    # Q8 Elevation Profile (Figure 1 on the page + map + legend)
    Task('p1-8-i', P1, '8', '(i)', 2, 9, L(9, 'Elevation Profile'),
         (L(9, '(i) What type of forestry is located at point A?'),),
         (S(4, 'Q.8 (i)', '(ii) The Táin Way', RIGHT),), (fixed('Forestry', 2, 'Q.8 (i) Coniferous'),),
         '2-6', (H + 'mapwork',), ('page', 'map', 'legend'), ID + 'p1-q8', True, stem=Q8_STEM),
    Task('p1-8-ii', P1, '8', '(ii)', 2, 9, L(9, 'Elevation Profile'),
         (L(9, '(ii) Name the tourist attraction at point B on the profile.'),),
         (S(4, '(ii) The Táin Way', '(iii) 100', RIGHT),), (fixed('Tourist attraction', 2, '(ii) The Táin Way'),),
         '2-6', (H + 'mapwork',), ('page', 'map', 'legend'), ID + 'p1-q8-ii', False, stem=Q8_STEM),
    Task('p1-8-iii', P1, '8', '(iii)', 2, 9, L(9, 'Elevation Profile'),
         (L(9, '(iii) What is the height of the land (in metres) at point C on the profile?'),),
         (S(4, '(iii) 100', '(iv) R174', RIGHT),), (fixed('Height', 2, '(iii) 100 (m)'),),
         '2-6', (H + 'mapwork',), ('page', 'map', 'legend'), ID + 'p1-q8-iii', False, stem=Q8_STEM),
    Task('p1-8-iv', P1, '8', '(iv)', 2, 9, L(9, 'Elevation Profile'),
         (L(9, '(iv) Name the road that crosses the profile at point D.'),),
         (S(4, '(iv) R174', 'Q.9', RIGHT),), (fixed('Road', 2, '(iv) R174'),),
         '2-6', (H + 'mapwork',), ('page', 'map', 'legend'), ID + 'p1-q8-iv', False, stem=Q8_STEM),
    # Q9 Aerial Photograph (satellite image on the page + aerial)
    Task('p1-9', P1, '9', '', 8, 10, L(10, 'Aerial Photograph', nth=0),
         (L(10, 'Examine the aerial photograph of Dundalk accompanying this paper and the satellite image', 'satellite image below.'),
          L(10, 'Locate each of the features labelled A, B, C, D and E above', 'One has been completed for you.')),
         (S(4, 'Q.9 A Right Background', 'Q.10', RIGHT),),
         (fixed('Row A', 2, 'Q.9 A Right Background'), fixed('Row B', 2, 'B Centre Foreground'),
          fixed('Row C', 2, 'C Left Middleground'), fixed('Row E', 2, 'E Centre Background')),
         '2-8', (H + 'aerial-photos',), ('page', 'aerial'), ID + 'p1-q9', True,
         row_labels=(L(10, 'A Bridge'), L(10, 'B Industrial Estate'), L(10, 'C Sports Stadium'), L(10, 'E Housing Estate'))),
    # Q10 Weather (UV chart on the page)
    Task('p1-10-i', P1, '10', '(i)', 2, 11, L(11, 'Weather'),
         (L(11, '(i) Which UV Index category is least prominent', 'Tick (✓) the correct box.'),
          L(11, 'Moderate High Low')),
         (S(4, 'Q.10 (i)', '(ii) Moderate', RIGHT),), (fixed('Category', 2, 'Q.10 (i) Low (1-2)'),),
         '2-7', (H + 'weather-climate',), ('page',), ID + 'p1-q10', True, stem=Q10_STEM),
    Task('p1-10-ii', P1, '10', '(ii)', 2, 11, L(11, 'Weather'),
         (L(11, '(ii) What was the UV index for Galway?'),),
         (S(4, '(ii) Moderate', '(iii) Isohels', RIGHT),), (fixed('Galway', 2, '(ii) Moderate (3-5)'),),
         '2-7', (H + 'weather-climate',), ('page',), ID + 'p1-q10-ii', False, stem=Q10_STEM),
    Task('p1-10-iii', P1, '10', '(iii)', 2, 11, L(11, 'Weather'),
         (L(11, '(iii) What is the name given to lines on a weather map', 'equal sunshine?'),),
         (S(4, '(iii) Isohels', '(iv) Valid answer 2 marks', RIGHT),), (fixed('Term', 2, '(iii) Isohels'),),
         '2-7', (H + 'weather-climate',), ('page',), ID + 'p1-q10-iii', False, stem=Q10_STEM),
    Task('p1-10-iv', P1, '10', '(iv)', 2, 11, L(11, 'Weather'),
         (L(11, '(iv) State one reason why the east of Ireland', 'west of Ireland.'),),
         (S(4, '(iv) Valid answer 2 marks', 'Q.11', RIGHT),), (fixed('Reason', 2, '(iv) Valid answer 2 marks'),),
         '2-7', (H + 'weather-climate',), ('page',), ID + 'p1-q10-iv', False, stem=Q10_STEM),
    # Q11 National Development Plan (extract on the page)
    Task('p1-11-i', P1, '11', '(i)', 2, 12, L(12, 'National Development Plan (NDP)'),
         (L(12, '(i) How much (€ billions) does the government plan', 'in the NDP?'),),
         (S(4, 'Q.11(i)', '(ii) €2', RIGHT),), (fixed('Total investment', 2, 'Q.11(i) €275.4 (bn)'),),
         '1-4', (H + 'regions-ireland',), ('page',), ID + 'p1-q11', True, stem=Q11_STEM),
    Task('p1-11-ii', P1, '11', '(ii)', 2, 12, L(12, 'National Development Plan (NDP)'),
         (L(12, '(ii) How much (€ billions) of the transport budget', 'in Dublin?'),),
         (S(4, '(ii) €2', '(iii) Valid answer 1 + 1', RIGHT),), (fixed('Metrolink', 2, '(ii) €2 (bn)'),),
         '1-4', (H + 'regions-ireland',), ('page',), ID + 'p1-q11-ii', False, stem=Q11_STEM),
    Task('p1-11-iii', P1, '11', '(iii)', 2, 12, L(12, 'National Development Plan (NDP)'),
         (L(12, '(iii) From the extract above, identify two areas', 'focus its investment on.'),),
         (S(4, '(iii) Valid answer 1 + 1', '(iv) Valid answer 1 + 1', RIGHT),),
         (fixed('Two areas', 2, '(iii) Valid answer 1 + 1 mark', (0, 1, 2)),),
         '1-4', (H + 'regions-ireland',), ('page',), ID + 'p1-q11-iii', False, stem=Q11_STEM),
    Task('p1-11-iv', P1, '11', '(iv)', 2, 12, L(12, 'National Development Plan (NDP)'),
         (L(12, '(iv) Explain briefly one advantage of having improved transport infrastructure in Dublin.'),),
         (S(4, '(iv) Valid answer 1 + 1', 'Q.12', RIGHT),),
         (fixed('Advantage', 2, '(iv) Valid answer 1 + 1 mark', (0, 1, 2)),),
         '4-5', (H + 'human-urban-geography',), ('page',), ID + 'p1-q11-iv', False, stem=Q11_STEM),
    # Q12 Graphical Interpretation (graph on the page)
    Task('p1-12-i', P1, '12', '(i)', 2, 13, L(13, 'Graphical Interpretation'),
         (L(13, '(i) What percentage (%) of people in Ireland', 'in 2024?'),),
         (S(4, '(i) 66', '(ii) Italy', RIGHT, after='Q.12'),), (fixed('Percentage', 2, '(i) 66 (%)'),),
         '2-0', (H + 'tablesgraphs-questions',), ('page',), ID + 'p1-q12', True, stem=Q12_STEM),
    Task('p1-12-ii', P1, '12', '(ii)', 2, 13, L(13, 'Graphical Interpretation'),
         (L(13, '(ii) Name two countries whose 2014 percentage', 'in 2014.'),),
         (S(4, '(ii) Italy', '(iii) Austria', RIGHT),),
         (fixed('Two countries', 2, '(ii) Italy/Cyprus/Germany 1+1 mark', (0, 1, 2)),),
         '2-0', (H + 'tablesgraphs-questions',), ('page',), ID + 'p1-q12-ii', False, stem=Q12_STEM),
    Task('p1-12-iii', P1, '12', '(iii)', 2, 13, L(13, 'Graphical Interpretation'),
         (L(13, '(iii) Which country had the smallest percentage increase', 'from 2014 to 2024?'),),
         (S(4, '(iii) Austria', '(iv) Valid answer 1+1', RIGHT),), (fixed('Country', 2, '(iii) Austria'),),
         '2-0', (H + 'tablesgraphs-questions',), ('page',), ID + 'p1-q12-iii', False, stem=Q12_STEM),
    Task('p1-12-iv', P1, '12', '(iv)', 2, 13, L(13, 'Graphical Interpretation'),
         (L(13, '(iv) Explain briefly one way that having a high percentage', 'benefit an economy.'),),
         (S(4, '(iv) Valid answer 1+1', None, RIGHT),),
         (fixed('Benefit', 2, '(iv) Valid answer 1+1 mark', (0, 1, 2)),),
         '3-0', (H + 'elective-economic',), ('page',), ID + 'p1-q12-iv', False, stem=Q12_STEM),
]


# ---------------------------------------------------------------- Part Two --
def T(key, q, sub, marks, page, title, prompt, scheme, criteria, topic, atlas, card_id,
      legacy, sources=(), stem=(), routes=(), row_labels=()):
    return Task(key, P2, q, sub, marks, page, title, prompt, scheme, criteria, topic, atlas,
                sources, card_id, legacy, stem=stem, routes=routes, row_labels=row_labels)


def roman_parts(q, page, title, stem, first_id, sources, parts):
    """A-part romans. parts: (sub, marks, prompt, scheme slices, criteria, topic, atlas)."""
    out = []
    for index, (sub, marks, prompt, scheme, criteria, topic, atlas) in enumerate(parts):
        roman = sub.strip('()')
        out.append(T(f'p2-{q.lower()}-{roman}', q, sub, marks, page, title, (prompt,), scheme,
                     criteria, topic, atlas, first_id if index == 0 else f'{first_id}-{roman}',
                     index == 0, sources, stem))
    return out


def sketch_criteria(outline_label, outline_line, outline_permitted, alloc_lines, feature_labels):
    return (fixed(outline_label, 4, outline_line, outline_permitted),
            *(fixed(label, 4, alloc_lines, upto(4)) for label in feature_labels))


OS_ALLOC = ('4 features @ 4 marks each', 'Label 1 mark')
GRAPH = (fixed('Title', 2, ('Bar Chart · Pie Chart', 'Title · 2 marks · 2 marks')),
         fixed('Axes named (bar chart) / circle and centre (pie chart)', 2,
               ('Vertical axis named', 'Horizontal axis named'), (0, 1, 2)),
         fixed('6 items illustrated', 12, '6 items illustrated', upto(12)))


def two_challenges(first_label, second_label, line):
    return (fixed(first_label, 4, line, (0, 2, 4)), fixed(second_label, 4, '=2 + 2 marks', (0, 2, 4)))


def three_reasons(label, head, named):
    lines = (head, f'For each {label.lower()}:', named, 'OS map evidence · 2 marks', 'Explanation · 3 x SRPs')
    return tuple(fixed(f'{label} {n}', 10, lines, evens(10), 'srp') for n in (1, 2, 3))


def chosen(items, k):
    import itertools
    from geography_review import slug as make_slug
    return [(combo, ' + '.join(item.rstrip('.') for item in combo),
             '-'.join(make_slug(item, 34) for item in combo))
            for combo in itertools.combinations(items, k)]


PART_TWO = [
    # Question 1
    T('p2-1a', '1A', '', 20, 3, L(3, 'Ordnance Survey Map'),
      (L(3, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper.', 'above 300 metres.'),),
      (S(5, 'Sketch Outline', None),),
      sketch_criteria('Sketch outline', 'Sketch Outline · 4 marks (4/0)', (0, 4), OS_ALLOC, ('f1', 'f2', 'f3', 'f4')),
      '2-6', (H + 'mapwork',), ID + 'p2-q1a', True, ('map', 'legend'),
      row_labels=(None, L(3, 'The coastline'), L(3, 'The railway line'),
                  L(3, 'The wind farm south of Dundalk town'), L(3, 'The entire area of land above 300 metres'))),
    T('p2-1b', '1B', '', 30, 3, L(3, 'Seismic Activity'),
      (L(3, 'Explain how the occurrence of earthquakes', 'effects reduced.'),),
      (S(6, 'Reference to prediction of earthquakes · 2 marks', 'Annotation'),),
      (fixed('Reference to prediction of earthquakes', 2, 'Reference to prediction of earthquakes · 2 marks'),
       fixed('Reference to reducing impacts of earthquakes', 2, 'Reference to reducing impacts of earthquakes · 2 marks'),
       srp('Explanation', 13, 'Explanation · 13 x SRPs')),
      '0-7', (H + 'earthquakes-volcanoes',), ID + 'p2-q1b', True),
    T('p2-1c', '1C', '', 30, 3, L(3, 'Rocks'),
      (L(3, 'Explain the formation of each of the following', 'One metamorphic rock.'),),
      (S(7, 'One sedimentary rock named', 'Annotation'),),
      (fixed('Sedimentary rock named', 2, 'One sedimentary rock named · 2 marks'),
       fixed('Metamorphic rock named', 2, 'One metamorphic rock named · 2 marks'),
       srp('Explanation of formation (6/7 and 7/6 SRPs)', 13,
           ('Explanation of formation of sedimentary rock · 6/7 x SRPs',
            'Explanation of formation of metamorphic rock · 7/6 x SRPs'))),
      '0-1', (H + 'rocks-weathering-mass-movement',), ID + 'p2-q1c', True),
]

Q2A_STEM = (L(4, 'Examine the photograph above of a section of limestone pavement', 'following questions.'),)
PART_TWO += roman_parts('2A', 4, L(4, 'Chemical Weathering'), Q2A_STEM, ID + 'p2-q2a', ('page',), [
    ('(i)', 8, L(4, '(i) Name each of the features labelled A, B, C and D.'),
     (S(8, '(i) · A – Grike', '(ii) · Valid features'),),
     (fixed('Feature A', 2, '(i) · A – Grike'), fixed('Feature B', 2, 'B – Fluting'),
      fixed('Feature C', 2, 'C – Karren'), fixed('Feature D', 2, 'D – Clint')),
     '0-3', (H + 'karst-regions',)),
    ('(ii)', 4, L(4, '(ii) Name two features formed below the surface', 'karst landscape.'),
     (S(8, '(ii) · Valid features', '(iii) · Carbonation'),),
     (fixed('Two features', 4, '(ii) · Valid features · 2 + 2 marks', (0, 2, 4)),), '0-3', (H + 'karst-regions',)),
    ('(iii)', 2, L(4, '(iii) What is the term used for the type of chemical weathering', 'photograph?'),
     (S(8, '(iii) · Carbonation', '(iv) · Bedding plane'),),
     (fixed('Term', 2, '(iii) · Carbonation'),), '0-3', (H + 'karst-regions',)),
    ('(iv)', 2, L(4, '(iv) What is the name given to the horizontal line', 'meet?'),
     (S(8, '(iv) · Bedding plane', '(v) · Valid explanation'),),
     (fixed('Name', 2, '(iv) · Bedding plane'),), '0-3', (H + 'karst-regions',)),
    ('(v)', 4, L(4, '(v) Explain briefly the term permeable rock.'),
     (S(8, '(v) · Valid explanation', None),),
     (fixed('Explanation', 4, '(v) · Valid explanation · 2 + 2 marks', (0, 2, 4)),), '0-3', (H + 'karst-regions',)),
])

LANDFORMS = 'one fluvial landform or one coastal landform or one glacial landform'
PART_TWO += [
    T('p2-2b', '2B', '', 30, 4, L(4, 'Landscape Development'),
      (L(4, '(i) Examine the role of the processes of erosion', 'that you have studied.'),),
      (S(9, 'Process of erosion identified · 2 marks', 'Annotation'),),
      (fixed('Process of erosion identified', 2, 'Process of erosion identified · 2 marks'),
       fixed('Landform named', 2, 'Landform named · 2 marks'),
       srp('Examination', 13, 'Examination · 13 x SRPs')),
      '0-9', (H + 'rivers',), ID + 'p2-q2b-route-i-fluvial-landform', True,
      routes=(
          Route('route-i-fluvial-landform', 'Route (i) · one fluvial landform',
                ID + 'p2-q2b-route-i-fluvial-landform', True, ((LANDFORMS, 'one fluvial landform'),),
                topic='0-9', atlas=(H + 'rivers',)),
          Route('route-i-coastal-landform', 'Route (i) · one coastal landform',
                ID + 'p2-q2b-route-i-coastal-landform', True, ((LANDFORMS, 'one coastal landform'),),
                topic='0-10', atlas=(H + 'the-sea',)),
          Route('route-i-glacial-landform', 'Route (i) · one glacial landform',
                ID + 'p2-q2b-route-i-glacial-landform', True, ((LANDFORMS, 'one glacial landform'),),
                topic='0-11', atlas=(H + 'glaciation',)),
          Route('route-ii', 'Route (ii)', ID + 'p2-q2b-route-ii', True,
                prompt=(L(4, '(ii) Describe and explain the factors governing', 'process that you have studied.'),),
                scheme=(S(10, 'Factors identified', 'Annotation'),),
                criteria=(fixed('Factors identified', 4, 'Factors identified · 2 + 2 marks', (0, 2, 4)),
                          fixed('Mass movement process named', 2, 'Mass movement process named · 2 marks'),
                          srp('Description/explanation', 12, 'Description/explanation · 12 x SRPs')),
                topic='0-8', atlas=(H + 'rocks-weathering-mass-movement',)),
      )),
    T('p2-2c', '2C', '', 30, 4, L(4, 'Plate Boundaries'),
      (L(4, 'Describe and explain constructive plate boundaries.'),),
      (S(11, 'Description/explanation', 'Annotation'),),
      (srp('Description/explanation', 15, 'Description/explanation · 15 x SRPs'),),
      '0-0', (H + 'plate-tectonics',), ID + 'p2-q2c', True),
]

Q3A_STEM = (L(5, 'Examine the diagram above which shows plutonic features', 'following questions.'),)
PART_TWO += roman_parts('3A', 5, L(5, 'The Tectonic Cycle'), Q3A_STEM, ID + 'p2-q3a', ('page',), [
    ('(i)', 8, L(5, '(i) Name each of the features labelled A, B, C and D.'),
     (S(12, '(i) · A – Lopolith', '(ii) · False'),),
     (fixed('Feature A', 2, '(i) · A – Lopolith'), fixed('Feature B', 2, 'B – Sill'),
      fixed('Feature C', 2, 'C – Dyke'), fixed('Feature D', 2, 'D – Laccolith')),
     '0-7', (H + 'earthquakes-volcanoes',)),
    ('(ii)', 2, L(5, '(ii) In your answerbook, state whether', 'exogenic processes.'),
     (S(12, '(ii) · False', '(iii) · Valid answer'),),
     (fixed('True or false', 2, '(ii) · False'),), '0-5', (H + 'rocks-weathering-mass-movement',)),
    ('(iii)', 4, L(5, '(iii) Name two pyroclastic materials', 'during an eruption.'),
     (S(12, '(iii) · Valid answer', '(iv) · Valid answer'),),
     (fixed('Two pyroclastic materials', 4, '(iii) · Valid answer · 2 + 2 marks', (0, 2, 4)),),
     '0-7', (H + 'earthquakes-volcanoes',)),
    ('(iv)', 2, L(5, '(iv) Name one example of a plutonic igneous rock.'),
     (S(12, '(iv) · Valid answer', '(v) · Valid explanation'),),
     (fixed('Plutonic igneous rock', 2, '(iv) · Valid answer · 2 marks'),), '0-1', (H + 'rocks-weathering-mass-movement',)),
    ('(v)', 4, L(5, '(v) Explain briefly the term convection current.'),
     (S(12, '(v) · Valid explanation', None),),
     (fixed('Explanation', 4, '(v) · Valid explanation · 2 + 2 marks', (0, 2, 4)),), '0-0', (H + 'plate-tectonics',)),
])

SURFACE = ('The impact of flood control measures on river processes',
           'The impact of coastal defence measures on coastal processes',
           'The impact of human activities on mass movement processes.')
PART_TWO += [
    T('p2-3b', '3B', '', 30, 5, L(5, 'Human Interaction with Surface Processes'),
      (L(5, 'Human activity impacts on surface processes.', 'mass movement processes.'),),
      (S(13, 'Impact on process identified · 2 marks', 'Annotation'),),
      (fixed('Impact on process identified', 2, 'Impact on process identified · 2 marks'),
       srp('Examination', 14, 'Examination · 14 x SRPs')),
      '0-6', (H + 'rivers',), ID + 'p2-q3b-the-impact-of-flood-control-measur', True,
      routes=tuple(
          Route(card.split('p2-q3b-')[1], item.rstrip('.'), card, True, keep_bullets=(item,), atlas=(atlas,))
          for item, card, atlas in zip(SURFACE, (
              ID + 'p2-q3b-the-impact-of-flood-control-measur',
              ID + 'p2-q3b-the-impact-of-coastal-defence-meas',
              ID + 'p2-q3b-the-impact-of-human-activities-on'), (
              H + 'rivers', H + 'the-sea', H + 'rocks-weathering-mass-movement')))),
    T('p2-3c', '3C', '', 30, 5, L(5, 'Weathering'),
      (L(5, 'Explain the role of temperature', 'mechanical weathering.'),),
      (S(14, 'Reference to role of temperature', 'Annotation'),),
      (fixed('Reference to role of temperature', 2, 'Reference to role of temperature · 2 marks'),
       srp('Explanation', 14, 'Explanation · 14 x SRPs')),
      '0-8', (H + 'rocks-weathering-mass-movement',), ID + 'p2-q3c', True),
    # Question 4
    T('p2-4a', '4A', '', 20, 6, L(6, 'Map Skills'),
      (L(6, 'Draw an outline map of a European region', '(upland or lowland).'),),
      (S(15, 'Map outline', None),),
      sketch_criteria('Map outline', 'Map outline · 4 marks graded (4/2/0)', (0, 2, 4),
                      ('4 features @ 4 marks each', 'Named 2 marks'),
                      ('First named urban centre', 'Second named urban centre', 'r', 'f')),
      '1-5', (H + 'regions-european',), ID + 'p2-q4a', True,
      row_labels=(None, None, None, L(6, 'The course of one named river'),
                  L(6, 'The outline of one named feature of relief (upland or lowland)'))),
    T('p2-4b', '4B', '', 30, 6, L(6, 'Primary Economic Activity'),
      (L(6, 'Explain any two factors that have influenced', 'that you have studied.'),),
      (S(16, 'Factors identified', 'Annotation'),),
      (fixed('Factors identified', 4, 'Factors identified · 2 + 2 marks', (0, 2, 4)),
       srp('Explanation of the two factors (7/6 and 6/7 SRPs)', 13,
           ('Explanation of Factor 1 · 7/6 x SRPs', 'Explanation of Factor 2 · 6/7 x SRPs'))),
      '1-4', (H + 'regions-ireland',), ID + 'p2-q4b', True),
    T('p2-4c', '4C', '', 30, 6, L(6, 'Complexity of Regions'),
      (L(6, 'Changes in boundaries over time', 'that you have studied.'),),
      (S(17, 'Reference to change in boundaries · 2 marks', 'Annotation'),),
      (fixed('Reference to change in boundaries', 2, 'Reference to change in boundaries · 2 marks'),
       fixed('Impact on cultural groups identified', 2, 'Impact on cultural groups identified · 2 marks'),
       fixed('Example', 2, 'Example · 2 marks'),
       srp('Examination', 12, 'Examination · 12 x SRPs')),
      '1-3', (H + 'regions-european', H + 'regions-ireland'), ID + 'p2-q4c', True),
]

Q5A_STEM = (L(7, 'Examine the map and text above that outline', 'following questions.'),)
EU = (H + 'regions-european',)
PART_TWO += roman_parts('5A', 7, L(7, 'Complexity of Regions'), Q5A_STEM, ID + 'p2-q5a', ('page',), [
    ('(i)', 2, L(7, '(i) In what year was the Maastricht Treaty signed?'),
     (S(18, '(i) · 1992', '(ii) · Lev'),), (fixed('Year', 2, '(i) · 1992'),), '1-3', EU),
    ('(ii)', 2, L(7, '(ii) Name the former currency of Bulgaria.'),
     (S(18, '(ii) · Lev', '(iii) · Valid countries'),), (fixed('Former currency', 2, '(ii) · Lev'),), '1-3', EU),
    ('(iii)', 4, L(7, '(iii) Name two countries, other than Bulgaria', 'use the Euro.'),
     (S(18, '(iii) · Valid countries', '(iv) · Valid benefits'),),
     (fixed('Two countries', 4, '(iii) · Valid countries', (0, 2, 4)),), '1-3', EU),
    ('(iv)', 4, L(7, '(iv) List two benefits of the common currency', 'eurozone.'),
     (S(18, '(iv) · Valid benefits', '(v) · Valid explanation'),),
     (fixed('Two benefits', 4, '(iv) · Valid benefits', (0, 2, 4)),), '1-3', EU),
    ('(v)', 4, L(7, '(v) Explain briefly one reason why all EU countries', 'eurozone.'),
     (S(18, '(v) · Valid explanation', '(vi) · Valid explanation'),),
     (fixed('Reason', 4, '(v) · Valid explanation', (0, 2, 4)),), '1-3', EU),
    ('(vi)', 4, L(7, '(vi) Explain briefly one benefit of further EU expansion.'),
     (S(18, '(vi) · Valid explanation', None),),
     (fixed('Benefit', 4, '(vi) · Valid explanation', (0, 2, 4)),), '1-3', EU),
])

FACTORS = ('Labour', 'Transport', 'Raw materials', 'Markets.')
PART_TWO += [
    T('p2-5b', '5B', '', 30, 8, L(8, 'Population Dynamics'),
      (L(8, 'Account for population distribution', 'that you have studied.'),),
      (S(19, 'Examination · 15 x SRPs', 'Annotation'),),
      (srp('Examination', 15, 'Examination · 15 x SRPs'),),
      '1-6', (H + 'regions-continental',), ID + 'p2-q5b', True),
    T('p2-5c', '5C', '', 30, 8, L(8, 'Secondary Economic Activity'),
      (L(8, 'Account for the development of secondary economic activity', 'Markets.'),),
      (S(20, 'Examination of Factor 1', 'Annotation'),),
      (srp('Examination of the two factors (8/7 and 7/8 SRPs)', 15,
           ('Examination of Factor 1 · 8/7 x SRPs', 'Examination of Factor 2 · 7/8 x SRPs')),),
      '1-5', (H + 'regions-european',), ID + 'p2-q5c-labour-transport', True,
      routes=tuple(Route(route_slug, label, ID + 'p2-q5c-' + route_slug, True, keep_bullets=combo)
                   for combo, label, route_slug in chosen(FACTORS, 2))),
]

Q6A_STEM = (L(9, 'Examine the charts above showing the value of Irish industrial production', 'following questions.'),)
TG = (H + 'tablesgraphs-questions',)
PART_TWO += roman_parts('6A', 9, L(9, 'Industry in Ireland'), Q6A_STEM, ID + 'p2-q6a', ('page',), [
    ('(i)', 2, L(9, '(i) Which sector had the lowest value', 'in 2021?'),
     (S(21, '(i) · Wood', '(ii) · 7'),), (fixed('Sector', 2, '(i) · Wood (Products)'),), '2-0', TG),
    ('(ii)', 2, L(9, '(ii) What was the value of Irish industrial production (%) for Electronic Products in 2023?'),
     (S(21, '(ii) · 7', '(iii) · 43'),), (fixed('Value', 2, '(ii) · 7 (%)'),), '2-0', TG),
    ('(iii)', 4, L(9, '(iii) Calculate X, the value (%) of pharmaceutical products in 2023.'),
     (S(21, '(iii) · 43', '(iv) · Pharmaceutical'),), (fixed('Calculation', 4, '(iii) · 43 (%) · 4 marks'),), '2-0', TG),
    ('(iv)', 2, L(9, '(iv) Name one sector that saw a decrease', '2021 to 2023.'),
     (S(21, '(iv) · Pharmaceutical', '(v) · Valid factor'),), (fixed('Sector', 2, '(iv) · Pharmaceutical / Food'),), '2-0', TG),
    ('(v)', 2, L(9, '(v) State one factor that attracts industries to Ireland.'),
     (S(21, '(v) · Valid factor', '(vi) · Valid explanation'),), (fixed('Factor', 2, '(v) · Valid factor'),),
     '1-4', (H + 'regions-ireland',)),
    ('(vi)', 8, L(9, '(vi) Explain briefly two challenges facing Irish industries.'),
     (S(21, '(vi) · Valid explanation', None),),
     two_challenges('First challenge', 'Second challenge', '(vi) · Valid explanation · 2 + 2 marks'),
     '1-4', (H + 'regions-ireland',)),
])

PART_TWO += [
    T('p2-6b', '6B', '', 30, 9, L(9, 'Socio-Economic Regions'),
      (L(9, 'Discuss how economic activity in core regions', 'you have studied.'),),
      (S(22, 'Discussion · 15 x SRPs', 'Annotation'),),
      (srp('Discussion', 15, 'Discussion · 15 x SRPs'),),
      '1-0', (H + 'regions-ireland', H + 'regions-european'), ID + 'p2-q6b', True),
    T('p2-6c', '6C', '', 30, 9, L(9, 'Tertiary Economic Activity'),
      (L(9, 'Account for the development of one tertiary economic activity', 'that you have studied.'),),
      (S(23, 'Examination · 15 x SRPs', 'Annotation'),),
      (srp('Examination', 15, 'Examination · 15 x SRPs'),),
      '1-6', (H + 'regions-continental',), ID + 'p2-q6c', True),
    # Question 7
    T('p2-7a', '7A', '', 20, 11, L(11, 'Aerial Photograph'),
      (L(11, 'Examine the aerial photograph of Dundalk accompanying the paper.', 'in the background.'),),
      (S(25, 'Sketch Outline', None),),
      sketch_criteria('Sketch outline', 'Sketch Outline · 4 marks (4/0)', (0, 4), OS_ALLOC, ('f1', 'f2', 'f3', 'f4')),
      '2-8', (H + 'aerial-photos',), ID + 'p2-q7a', True, ('aerial',),
      row_labels=(None, L(11, 'The river'), L(11, 'A railway bridge'),
                  L(11, 'Industrial buildings in the foreground'), L(11, 'Agricultural land use in the background'))),
    T('p2-7b', '7B', '', 30, 11, L(11, 'Economic Development'),
      (L(11, 'Discuss how levels of economic development', 'that you have studied.'),),
      (S(26, 'Developed economy named · 2 marks', 'Annotation'),),
      (fixed('Developed economy named', 2, 'Developed economy named · 2 marks'),
       fixed('Reference to change over time', 2, 'Reference to change over time · 2 marks'),
       srp('Discussion', 13, 'Discussion · 13 x SRPs')),
      '3-0', (H + 'elective-economic',), ID + 'p2-q7b', True),
    T('p2-7c', '7C', '', 30, 11, L(11, 'Multinational Company'),
      (L(11, 'Examine the mobility of modern economic activities', 'that you have studied.'),),
      (S(27, 'MNC named · 2 marks', 'Annotation'),),
      (fixed('MNC named', 2, 'MNC named · 2 marks'), srp('Examination', 14, 'Examination · 14 x SRPs')),
      '3-2', (H + 'economic-multinationals-globalisation',), ID + 'p2-q7c', True),
]

Q8A_STEM = (L(12, 'Examine the table above showing the percentage of renewable energy', 'following questions.'),)
ENERGY = (H + 'economic-energy',)
PART_TWO += roman_parts('8A', 12, L(12, 'Renewable Energy in the EU'), Q8A_STEM, ID + 'p2-q8a', ('page',), [
    ('(i)', 2, L(12, '(i) What percentage of renewable energy was used', 'Germany in 2020?'),
     (S(28, '(i) · 44.7', '(ii) · Estonia'),), (fixed('Percentage', 2, '(i) · 44.7 (%)'),), '2-0', TG),
    ('(ii)', 2, L(12, '(ii) Which country used the lowest percentage', 'in 2005?'),
     (S(28, '(ii) · Estonia', '(iii) · Denmark'),), (fixed('Country', 2, '(ii) · Estonia'),), '2-0', TG),
    ('(iii)', 2, L(12, '(iii) Which country had the highest percentage increase', '2005 to 2020?'),
     (S(28, '(iii) · Denmark', '(iv) · 26.4'),), (fixed('Country', 2, '(iii) · Denmark'),), '2-0', TG),
    ('(iv)', 4, L(12, '(iv) Calculate X', 'in 2020.'),
     (S(28, '(iv) · 26.4', '(v) · Valid source'),), (fixed('Calculation', 4, '(iv) · 26.4 (%) · 4 marks'),), '2-0', TG),
    ('(v)', 2, L(12, '(v) Name one source of renewable energy.'),
     (S(28, '(v) · Valid source', '(vi) · Valid explanation'),), (fixed('Source', 2, '(v) · Valid source'),), '3-5', ENERGY),
    ('(vi)', 8, L(12, '(vi) Explain briefly two advantages of renewable energy.'),
     (S(28, '(vi) · Valid explanation', None),),
     two_challenges('First advantage', 'Second advantage', '(vi) · Valid explanation · 2 + 2 marks'), '3-5', ENERGY),
])

PART_TWO += [
    T('p2-8b', '8B', '', 30, 12, L(12, 'Economic Development'),
      (L(12, 'Discuss how Gross National Product', 'that you have studied.'),),
      (S(29, 'Reference to GNP as measure', 'Annotation'),),
      (fixed('Reference to GNP as measure', 2, 'Reference to GNP as measure · 2 marks'),
       fixed('Reference to HDI as measure', 2, 'Reference to HDI as measure · 2 marks'),
       fixed('Example', 2, 'Example · 2 marks'),
       srp('Discussion', 12, 'Discussion · 12 x SRPs')),
      '3-0', (H + 'elective-economic',), ID + 'p2-q8b', True),
    T('p2-8c', '8C', '', 30, 12, L(12, 'European Union Policy'),
      (L(12, 'Examine the impact of European Union policy', 'activity in Ireland.'),),
      (S(30, 'Impact on primary activity identified', 'Annotation'),),
      (fixed('Impact on primary activity identified', 2, 'Impact on primary activity identified · 2 marks'),
       srp('Examination', 14, 'Examination · 14 x SRPs')),
      '3-3', (H + 'economic-european-union',), ID + 'p2-q8c', True),
]

Q9A_STEM = (L(13, 'Examine the data above showing the value of goods exported', 'following questions.'),)
PART_TWO += roman_parts('9A', 13, L(13, 'Economic Activity'), Q9A_STEM, ID + 'p2-q9a', ('page',), [
    ('(i)', 16, L(13, '(i) Using graph paper, draw a suitable graph to illustrate this data.'),
     (S(31, 'Bar Chart · Pie Chart', 'Annotation'),), GRAPH, '2-0', TG),
    ('(ii)', 4, L(13, '(ii) Explain briefly one advantage of having a large number of export partners.'),
     (S(31, 'Valid explanation · 2 + 2 marks', None),),
     (fixed('Advantage', 4, 'Valid explanation · 2 + 2 marks', (0, 2, 4)),),
     '3-2', (H + 'economic-multinationals-globalisation',)),
])

PART_TWO += [
    T('p2-9b', '9B', '', 30, 13, L(13, 'Conflict of Interest'),
      (L(13, 'Examine how conflict may arise', 'that you have studied.'),),
      (S(32, 'Example named', 'Annotation'),),
      (fixed('Example named', 2, 'Example named · 2 marks'), srp('Examination', 14, 'Examination · 14 x SRPs')),
      '3-4', (H + 'economic-environmental-impact',), ID + 'p2-q9b', True),
    T('p2-9c', '9C', '', 30, 13, L(13, 'Economic Development'),
      (L(13, 'Using evidence from the 1:50 000 Ordnance Survey map', 'Ordnance Survey map.'),),
      (S(33, 'Three factors @ 10 marks each', 'Annotation'),),
      three_reasons('Factor', 'Three factors @ 10 marks each', 'Factor named · 2 marks'),
      '3-0', (H + 'elective-economic', H + 'mapwork'), ID + 'p2-q9c', True, ('map', 'legend')),
]

Q10A_STEM = (L(14, 'Examine the data above showing the population of towns', 'following questions.'),)
POP = (H + 'human-population',)
PART_TWO += roman_parts('10A', 14, L(14, 'Urban Population'), Q10A_STEM, ID + 'p2-q10a', ('page',), [
    ('(i)', 16, L(14, '(i) Using graph paper, draw a suitable graph to illustrate this data.'),
     (S(34, 'Bar Chart · Pie Chart', 'Annotation'),), GRAPH, '2-0', TG),
    ('(ii)', 4, L(14, '(ii) Explain briefly one benefit of conducting a census', 'population.'),
     (S(34, 'Valid explanation · 2 + 2 marks', None),),
     (fixed('Benefit', 4, 'Valid explanation · 2 + 2 marks', (0, 2, 4)),), '4-0', POP),
])

PART_TWO += [
    T('p2-10b', '10B', '', 30, 14, L(14, 'Urban Land Use'),
      (L(14, 'Describe and explain the land-use zones in any city that you have studied.'),),
      (S(35, 'Land-use zones identified', 'Annotation'),),
      (fixed('Land-use zones identified', 4, 'Land-use zones identified · 2 + 2 marks', (0, 2, 4)),
       fixed('City named', 2, 'City named · 2 marks'),
       srp('Description/explanation', 12, 'Description/explanation · 12 x SRPs')),
      '4-4', (H + 'urban-land-uses',), ID + 'p2-q10b', True),
    T('p2-10c', '10C', '', 30, 14, L(14, 'Migration'),
      (L(14, 'Examine how ethnic and religious issues can arise as a result of migration.'),),
      (S(36, 'Ethnic issue identified · 2 marks', 'Annotation'),),
      (fixed('Ethnic issue identified', 2, 'Ethnic issue identified · 2 marks'),
       fixed('Religious issue identified', 2, 'Religious issue identified · 2 marks'),
       srp('Examination', 13, 'Examination · 13 x SRPs')),
      '4-2', POP, ID + 'p2-q10c', True),
]

Q11A_STEM = (L(15, 'Examine the chart above showing immigration and emigration', 'following questions.'),)
PART_TWO += roman_parts('11A', 15, L(15, 'Population Movement'), Q11A_STEM, ID + 'p2-q11a', ('page',), [
    ('(i)', 2, L(15, '(i) In which year did the highest number of people emigrate?'),
     (S(37, '(i) 2012', '(ii) 2014'),), (fixed('Year', 2, '(i) 2012 · 2 marks'),), '2-0', TG),
    ('(ii)', 2, L(15, '(ii) Which year had the smallest difference', 'emigration?'),
     (S(37, '(ii) 2014', '(iii) Five'),), (fixed('Year', 2, '(ii) 2014'),), '2-0', TG),
    ('(iii)', 4, L(15, '(iii) For how many of the years shown', 'high levels of immigration.'),
     (S(37, '(iii) Five', '(iv) 79'),),
     (fixed('Number of years', 2, '(iii) Five'), fixed('Reason for high immigration', 2, 'Valid reason · 2 marks')),
     '4-2', (H + 'tablesgraphs-questions', H + 'human-population')),
    ('(iv)', 4, L(15, '(iv) Calculate the net migration', 'in 2024.'),
     (S(37, '(iv) 79', '(v) Valid answer'),), (fixed('Net migration', 4, '(iv) 79 (thousand) · 4 marks'),), '2-0', TG),
    ('(v)', 4, L(15, '(v) State two barriers to migration.'),
     (S(37, '(v) Valid answer', '(vi) Valid explanation'),),
     (fixed('Two barriers', 4, '(v) Valid answer · 2 + 2 marks', (0, 2, 4)),), '4-2', POP),
    ('(vi)', 4, L(15, '(vi) Explain briefly one reason why young people', 'from Ireland.'),
     (S(37, '(vi) Valid explanation', None),),
     (fixed('Reason', 4, '(vi) Valid explanation · 2 + 2 marks', (0, 2, 4)),), '4-2', POP),
])

PART_TWO += [
    T('p2-11b', '11B', '', 30, 15, L(15, 'Population Characteristics'),
      (L(15, 'Examine how changing fertility and mortality rates', 'that you have studied.'),),
      (S(38, 'Impact of changing fertility rates identified', 'Annotation'),),
      (fixed('Impact of changing fertility rates identified', 2, 'Impact of changing fertility rates identified · 2 marks'),
       fixed('Impact of changing mortality rates identified', 2, 'Impact of changing mortality rates identified · 2 marks'),
       fixed('Example', 2, 'Example · 2 marks'),
       srp('Examination', 12, 'Examination · 12 x SRPs')),
      '4-0', POP, ID + 'p2-q11b', True),
    T('p2-11c', '11C', '', 30, 15, L(15, 'Urban Growth – Developing World City'),
      (L(15, 'Problems can develop from the growth', 'that you have studied.'),),
      (S(39, 'Problems identified', 'Annotation'),),
      (fixed('Problems identified', 4, 'Problems identified · 2 + 2 marks', (0, 2, 4)),
       fixed('Developing world city', 2, 'Developing world city · 2 marks'),
       srp('Discussion', 12, 'Discussion · 12 x SRPs')),
      '4-5', (H + 'human-urban-geography',), ID + 'p2-q11c', True),
    # Question 12
    T('p2-12a', '12A', '', 20, 16, L(16, 'Aerial Photograph'),
      (L(16, 'Examine the aerial photograph of Dundalk accompanying the paper.', 'recreational land-use.'),),
      (S(40, 'Sketch Outline', None),),
      sketch_criteria('Sketch outline', 'Sketch Outline · 4 marks (4/0)', (0, 4), OS_ALLOC, ('f1', 'f2', 'f3', 'f4')),
      '2-8', (H + 'aerial-photos',), ID + 'p2-q12a', True, ('aerial',),
      row_labels=(None, L(16, 'The river'), L(16, 'The railway line'),
                  L(16, 'An area of residential land-use'), L(16, 'An area of recreational land-use'))),
    T('p2-12b', '12B', '', 30, 16, L(16, 'Overpopulation'),
      (L(16, 'Examine the causes and effects of overpopulation', 'have studied.'),),
      (S(41, 'Cause identified · 2 marks', 'Annotation'),),
      (fixed('Cause identified', 2, 'Cause identified · 2 marks'),
       fixed('Effect identified', 2, 'Effect identified · 2 marks'),
       fixed('Example', 2, 'Example · 2 marks'),
       srp('Examination of causes', 6, 'Examination of causes · 6 x SRPs'),
       srp('Examination of effects', 6, 'Examination of effects · 6 x SRPs')),
      '4-1', POP, ID + 'p2-q12b', True),
    T('p2-12c', '12C', '', 30, 16, L(16, 'Urban Settlement'),
      (L(16, 'Examine the 1:50 000 Ordnance Survey map and legend accompanying this paper.', 'to support each reason.'),),
      (S(42, 'Three reasons @ 10 marks each', 'Annotation'),),
      three_reasons('Reason', 'Three reasons @ 10 marks each', 'Reason stated · 2 marks'),
      '4-3', (H + 'human-urban-geography', H + 'mapwork'), ID + 'p2-q12c', True, ('map', 'legend')),
]

# ------------------------------------------------------------------ Options --
OC = (S(44, '*Overall Coherence (20 marks)', None, table=True),)


def option(q, page, theme, note_nth, prompt, scheme_page, discussion, topic, atlas, routes=()):
    return T(f'p2-{q}', q, '', 80, page, theme, (prompt,),
             (S(scheme_page, 'Number of aspects', None), *OC),
             (Criterion('Aspects (3 @ 20 marks or 4 @ 15 marks)', 60, upto(60), 'srp',
                        ('Number of aspects', '?For each aspect:', 'Identifying aspect', discussion)),
              Criterion('Overall coherence', 20, (0, 6, 10, 14, 17, 20), 'exact',
                        ('Overall Coherence · 20 marks graded*', '*Overall Coherence (20 marks)', 'Excellent · 20', 'Very Good · 17',
                         'Good · 14', 'Fair · 10', 'Weak · 6', 'Poor · 0'))),
             topic, (atlas,), (routes[0].card_id if routes else ID + f'p2-q{q}'), True,
             stem=(L(page, 'Note: It is better to discuss three or four aspects', 'large number of points.', nth=note_nth),),
             routes=routes)


GI, GE = H + 'option-global-interdependence', H + 'option-geoecology'
CI, AO = H + 'option-culture-identity', H + 'option-atmosphere-ocean'
THEMES = ('Resource use', 'Fair trade', 'Justice issues', 'Self-reliance.')
OPTIONS = [
    option('13', 18, L(18, 'Global Interdependence'), 0, L(18, 'Views of development and underdevelopment', 'Discuss.'),
           46, 'Discussion · 8 x SRPs', '5-0', GI),
    option('14', 18, L(18, 'Global Interdependence'), 0, L(18, 'Sustainability is a model', 'Self-reliance.'),
           47, 'Discussion · 8 x SRPs', '5-3', GI,
           routes=tuple(Route(route_slug, label, ID + 'p2-q14-' + route_slug, True, keep_bullets=combo)
                        for combo, label, route_slug in chosen(THEMES, 3))),
    option('15', 18, L(18, 'Global Interdependence'), 0, L(18, 'Discuss the impact of global trading patterns', 'that you have studied.'),
           48, 'Discussion · 8 x SRPs', '5-1', GI),
    option('16', 18, L(18, 'Geoecology'), 1, L(18, 'Explain how soil characteristics impact on soil development.'),
           49, 'Examination · 8 x SRPs', '6-0', GE),
    option('17', 18, L(18, 'Geoecology'), 1, L(18, 'Discuss how human activity can have both positive and negative impacts on soil.'),
           50, 'Discussion · 8 x SRPs', '6-1', GE),
    option('18', 18, L(18, 'Geoecology'), 1, L(18, 'With reference to one biome', 'within the biome.'),
           51, 'Discussion · 8 x SRPs', '6-2', GE),
    option('19', 19, L(19, 'Culture and Identity'), 0, L(19, 'Examine the strategies that have been or could be implemented', 'minority languages.'),
           52, 'Discussion · 8 x SRPs', '7-0', CI),
    option('20', 19, L(19, 'Culture and Identity'), 0, L(19, 'Many cultural groups around the world', 'you have studied.'),
           53, 'Discussion · 8 x SRPs', '7-1', CI),
    option('21', 19, L(19, 'Culture and Identity'), 0, L(19, 'Identity as a concept entails', 'that you have studied.'),
           54, 'Discussion · 8 x SRPs', '7-2', CI),
    option('22', 19, L(19, 'The Atmosphere – Ocean Environment'), 1, L(19, 'Examine how solar energy is transformed', 'atmosphere and oceans.'),
           55, 'Discussion · 8 x SRPs', '8-1', AO),
    option('23', 19, L(19, 'The Atmosphere – Ocean Environment'), 1, L(19, 'Exchanges of water between oceans and atmosphere', 'Discuss.'),
           56, 'Discussion · 8 x SRPs', '8-2', AO),
    option('24', 19, L(19, 'The Atmosphere – Ocean Environment'), 1, L(19, 'Describe and account for the characteristics of one global climate type', 'studied.'),
           57, 'Discussion · 8 x SRPs', '8-4', AO),
]

TASKS = [*PART_ONE, *PART_TWO, *OPTIONS]

# Every 2026 Higher card id shipped before this review (73). Each must survive.
LEGACY_IDS = [
    'geography-2026-hl-p1-q1',
    'geography-2026-hl-p1-q2',
    'geography-2026-hl-p1-q3',
    'geography-2026-hl-p1-q4',
    'geography-2026-hl-p1-q5',
    'geography-2026-hl-p1-q6',
    'geography-2026-hl-p1-q7',
    'geography-2026-hl-p1-q8',
    'geography-2026-hl-p1-q9',
    'geography-2026-hl-p1-q10',
    'geography-2026-hl-p1-q11',
    'geography-2026-hl-p1-q12',
    'geography-2026-hl-p2-q1a',
    'geography-2026-hl-p2-q1b',
    'geography-2026-hl-p2-q1c',
    'geography-2026-hl-p2-q2a',
    'geography-2026-hl-p2-q2b-route-i-fluvial-landform',
    'geography-2026-hl-p2-q2b-route-i-coastal-landform',
    'geography-2026-hl-p2-q2b-route-i-glacial-landform',
    'geography-2026-hl-p2-q2b-route-ii',
    'geography-2026-hl-p2-q2c',
    'geography-2026-hl-p2-q3a',
    'geography-2026-hl-p2-q3b-the-impact-of-flood-control-measur',
    'geography-2026-hl-p2-q3b-the-impact-of-coastal-defence-meas',
    'geography-2026-hl-p2-q3b-the-impact-of-human-activities-on',
    'geography-2026-hl-p2-q3c',
    'geography-2026-hl-p2-q4a',
    'geography-2026-hl-p2-q4b',
    'geography-2026-hl-p2-q4c',
    'geography-2026-hl-p2-q5a',
    'geography-2026-hl-p2-q5b',
    'geography-2026-hl-p2-q5c-labour-transport',
    'geography-2026-hl-p2-q5c-labour-raw-materials',
    'geography-2026-hl-p2-q5c-labour-markets',
    'geography-2026-hl-p2-q5c-transport-raw-materials',
    'geography-2026-hl-p2-q5c-transport-markets',
    'geography-2026-hl-p2-q5c-raw-materials-markets',
    'geography-2026-hl-p2-q6a',
    'geography-2026-hl-p2-q6b',
    'geography-2026-hl-p2-q6c',
    'geography-2026-hl-p2-q7a',
    'geography-2026-hl-p2-q7b',
    'geography-2026-hl-p2-q7c',
    'geography-2026-hl-p2-q8a',
    'geography-2026-hl-p2-q8b',
    'geography-2026-hl-p2-q8c',
    'geography-2026-hl-p2-q9a',
    'geography-2026-hl-p2-q9b',
    'geography-2026-hl-p2-q9c',
    'geography-2026-hl-p2-q10a',
    'geography-2026-hl-p2-q10b',
    'geography-2026-hl-p2-q10c',
    'geography-2026-hl-p2-q11a',
    'geography-2026-hl-p2-q11b',
    'geography-2026-hl-p2-q11c',
    'geography-2026-hl-p2-q12a',
    'geography-2026-hl-p2-q12b',
    'geography-2026-hl-p2-q12c',
    'geography-2026-hl-p2-q13',
    'geography-2026-hl-p2-q14-resource-use-fair-trade-justice-issues',
    'geography-2026-hl-p2-q14-resource-use-fair-trade-self-reliance',
    'geography-2026-hl-p2-q14-resource-use-justice-issues-self-reliance',
    'geography-2026-hl-p2-q14-fair-trade-justice-issues-self-reliance',
    'geography-2026-hl-p2-q15',
    'geography-2026-hl-p2-q16',
    'geography-2026-hl-p2-q17',
    'geography-2026-hl-p2-q18',
    'geography-2026-hl-p2-q19',
    'geography-2026-hl-p2-q20',
    'geography-2026-hl-p2-q21',
    'geography-2026-hl-p2-q22',
    'geography-2026-hl-p2-q23',
    'geography-2026-hl-p2-q24',
]

# Where a shipped id named a whole printed question that the scheme prices in
# separately marked parts, the id now names the FIRST part and new ids carry
# the remaining parts. Saved progress stays on a real practice task.
ID_CORRECTION_REASON = (
    'The shipped card held every part of a question the scheme prices part by '
    'part. Its id is kept on the first separately priced part; the other parts '
    'are new cards with their own published allocation.')
