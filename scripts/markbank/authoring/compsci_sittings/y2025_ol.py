"""Computer Science 2025 Ordinary Level: all 42 printed asks, re-authored part by part.

29 cards shipped in August out of the automatic author; batch 1b rebuilds each
of them here, keeping its id, from lifts of the paper and the scheme, and the
8 residue cards sit among them in printed order. Paper pages 3-18 and Section
C pages 4-7, and scheme pages 3-23 were opened.

Three of the shipped cards were whole-question cards (cs-2025-ol-q13, -q14,
-q15, 38 marks each) shipped beside part cards for the same questions, so they
repeated those parts. The coordinator's ruling (5 Nov): each printed ask has
exactly one card. The parts no part card covered -- Q13(a)(ii), Q13(c), Q14(c),
Q15(b)(i), Q15(b)(ii) -- get cards of their own here, and the three whole ids
are withdrawn onto the first of them (WITHDRAWN; the lane coordinator writes
the aliases). Q3, Q7 and Q8 stay whole: no part cards exist for them, and each
is one 6-mark card with a row per part.

Q9's scheme prints its six answers as a bare list ("• False • False • True •
True • True • False") with no wording of its own, so each answer is paired
with the paper's statement by printed ORDER; both documents print six, and
the scheme page shows the list set beside nothing else.

Q15(a)(i): cs_scheme reads 8 for this part, but the scheme prints "(i) 9 (3, 3,
3) marks" and (a) as 15 (9, 6); the tariff is quoted. Q16(b)'s rubric is read
from the cells of scheme page 23.
"""
from compsci_lane import (C, P, Pair, S, T, anyn, crit, crop, ladder, ofpart, pt, stack, unprinted)  # noqa: F401

WITHDRAWN = {'cs-2025-ol-q13': 'cs-2025-ol-q13-a-ii',
             'cs-2025-ol-q14': 'cs-2025-ol-q14-c',
             'cs-2025-ol-q15': 'cs-2025-ol-q15-b-i'}

ITEMS = ('038', 13, (55, 104, 541, 309))
FIG7 = ('038', 16, (303, 75, 566, 267))
LISTING = ('040', 4, (76, 349, 541, 505))

CROPS = {
    'q1-code': stack([('038', 3, (104, 178, 481, 280)), ('038', 3, (129, 307, 470, 488))],
                     ref='2025 OL Q1',
                     alt='The seven-line Python program printed with Question 1 (age read as an '
                         'integer; print A if age > 16, B if age < 16, otherwise C), above the '
                         'table whose Column A lists the values 21, -1, 0, 16, 100 and 15 and '
                         'whose Column B (Program output) is blank.'),
    'q5-code': stack([('038', 5, (53, 97, 515, 174)), ('038', 5, (88, 239, 543, 425))],
                     ref='2025 OL Q5',
                     alt='The five-line Python program printed with Question 5 (name = "John", '
                         'age = 17, student = True, exam_marks = [71, 82, 75, 93, 65], '
                         'average_mark = 77.2), above the table whose Column A lists name, age, '
                         'student, exam_marks and average_mark and whose Column B (Python data '
                         'type) is blank.'),
    'q8-fig2': crop('038', 7, (383, 54, 541, 203), ref='2025 OL Q8',
                    alt='Figure 2, printed with Question 8: a photograph of the inside of a desktop '
                        'computer case, showing the motherboard with its processor, the power '
                        'supply and a drive cage.'),
    'q9-table': crop('038', 7, (68, 451, 515, 660), ref='2025 OL Q9',
                     alt='The six statements printed with Question 9, each with an empty True box '
                         'and an empty False box: The Internet and the World Wide Web are the same '
                         'thing; HTTP is a mark-up language for making web pages; A URL is an '
                         'address for a web page; Data is communicated over the World Wide Web '
                         'using HTTP; HTTPS is more secure than HTTP; The server sends the first '
                         'communication in the client-server model.'),
    'q11-boxes': crop('038', 9, (57, 163, 507, 371), ref='2025 OL Q11',
                      alt='The boxes printed with Question 11: an initial state of 13, 54, 4, '
                          '81, 92, 26, blank rows for Swaps 1 to 4, and Swap 5 (Final state) '
                          'filled in as 4, 13, 26, 54, 81, 92.'),
    'q14-items': crop(*ITEMS, ref='2025 OL Q14',
                      alt='The table printed with Question 14 (item code, item name, price in '
                          'euro: A1 Water, flavoured 1.5; A2 Water 1.2; B1 Oreos 2.5; C1 Crisps, '
                          'Salt & Vinegar 2; C2 Crisps, Cheese & Onion 2) beside Figure 6, a '
                          'drawing of a vending machine stocked with snacks.'),
    'q14a-code': stack([ITEMS, ('038', 13, (56, 408, 541, 484))], ref='2025 OL Q14(a)',
                       alt='The item table and Figure 6 printed with Question 14 (A1 Water, '
                           'flavoured 1.5; A2 Water 1.2; B1 Oreos 2.5; C1 Crisps, Salt & Vinegar '
                           '2; C2 Crisps, Cheese & Onion 2; a drawing of a vending machine), above '
                           'the five-line program of part (a): if money >= price: dispenseItem, '
                           'giveChange(money - price), else: print("Error – not enough money '
                           'inserted").'),
    'q14b-plan': stack([ITEMS, ('038', 14, (85, 340, 510, 512))], ref='2025 OL Q14(b)(ii)',
                       alt='The item table and Figure 6 printed with Question 14 (A1 Water, '
                           'flavoured 1.5; A2 Water 1.2; B1 Oreos 2.5; C1 Crisps, Salt & Vinegar '
                           '2; C2 Crisps, Cheese & Onion 2; a drawing of a vending machine), above '
                           'the test plan of part (b)(ii), columns Code entered, Money inserted '
                           'and Expected result: B1, 3, Oreos dispensed, 0.50 euro change given; '
                           'a blank code, 1.2, Water dispensed, no change given; C1, a blank '
                           'amount, Error – not enough money inserted; C2, 0.75 and a blank '
                           'result.'),
    's-q14b-ii': crop('scheme', 14, (118, 84, 541, 198), ref='2025 OL Q14(b)(ii)', solution=True,
                      alt='The marking scheme\'s completed test plan for Question 14(b)(ii): B1, '
                          '3, Oreos served, 0.50 euro change given; A2, 1.2, Water served, no '
                          'change given; C1, <2, Error – not enough money inserted; C2, 0.75, '
                          'Error – not enough money inserted. The three answers (A2, <2 and the C2 '
                          'result) are printed in red.'),
    's-q14c': crop('scheme', 15, (55, 364, 535, 656), ref='2025 OL Q14(c)', solution=True,
                   alt='The marking scheme\'s answer to Question 14(c). Pseudocode: START; User '
                       'inserts money and enters item code; IF stock is less than 1: Prompt user to '
                       'enter another code; IF stock is less than 3: (Dispense item) Send Email to '
                       'head office; ELSE: (stock must be 1 or more) Dispense item; STOP. Beside '
                       'it, a flowchart: Start; INPUT amount and item code; Stock < 1? No/False '
                       'leads to Dispense Item, Yes/True to INPUT item another code and then '
                       'Stock < 3?, whose Yes/True leads to Send Email to order more stock and '
                       'whose No/False joins the line from Dispense Item; Stop.'),
    'q15-figs': stack([FIG7, ('038', 17, (88, 345, 521, 484))], ref='2025 OL Q15(b)',
                      alt='Figure 7, a photograph of a museum information point, a touchscreen '
                          'table showing images of artwork, above Figure 8, a row of arrows for '
                          'the stages INVESTIGATE, PLAN, DESIGN, CREATE, EVALUATE and DOCUMENT, '
                          'with an ITERATE arrow looping back from EVALUATE to PLAN.'),
    'q16a-code': crop(*LISTING, ref='2025 OL Q16(a)',
                      alt='The eleven-line program Question16_A.py as printed in the Section C '
                          'booklet: two comment lines, print("The program"), length = '
                          'float(input("What length is the room?: ")), width = 20, area = length '
                          '* width, and print("The area of the floor is:", area).'),
    'q16a-vi': stack([LISTING, ('040', 6, (109, 118, 543, 250))], ref='2025 OL Q16(a)(vi)',
                     alt='The eleven-line program Question16_A.py (print("The program"), length '
                         'read as a float, width = 20, area = length * width, the area printed), '
                         'above the table printed with part (vi): cost more than 1000, You are '
                         'entitled to a 10% discount; cost between 100 and 1000 inclusive, You '
                         'are not entitled to a 10% discount; cost less than 100, Sorry, job is '
                         'too small.'),
    's-q16a': crop('scheme', 20, (52, 154, 563, 467), ref='2025 OL Q16(a)', solution=True,
                   alt='The marking scheme\'s possible solution to Question 16(a), lines 1 to 27: '
                       'print("Welcome to the Tilers Mate") marked (i); the width read with '
                       'float(input()) marked (iii); cost_per_square_metre = 15 marked (iv); the '
                       'length and width printed in metres, marked (ii) and (iii); the cost per '
                       'square metre printed, (iv); the total cost calculated and printed, (v); '
                       'and the discount messages for totals over 1000, from 100 to 1000, and '
                       'below 100, (vi).'),
    'q16b-output': crop('040', 7, (79, 495, 547, 680), ref='2025 OL Q16(b)',
                        alt='The sample output printed with Question 16(b): Tile Cost Calculator; '
                            'How much do the tiles cost per square metre? 19.75; How many rooms do '
                            'you want to tile? 3; then for Room 1, Room 2 and Room 3 the width and '
                            'length entered (12 and 8, 9 and 6, 8.5 and 6.5); The total cost is '
                            'EUR 4053.69.'),
    's-q16b': crop('scheme', 22, (56, 99, 562, 478), ref='2025 OL Q16(b)', solution=True,
                   alt='The marking scheme\'s 32-line possible solution for Question 16(b): print '
                       '"Tile Cost Calculator"; cost_per_sq_metre read as a float and num_rooms as '
                       'an int; total_cost = 0.0; for x in range(num_rooms) the room number is '
                       'printed, the width and length are read as floats, room_cost = width * '
                       'length * cost_per_sq_metre is added to total_cost; then print("The total '
                       'cost is EUR", round(total_cost,2)).'),
}

Q13A = P(10, 'The development of the world’s first computer, ENIAC', 'major milestone in computing.')
Q13B = P(11, 'Modern computer systems consist of the four layers shown in Figure 5 below.')
Q14_INTRO = [P(13, 'A vending machine, such as that in Figure 6', 'options available for users.'),
             P(13, 'Customers deposit coins into the vending machine', 'returns any necessary change.')]
Q14A = Q14_INTRO + [P(13, 'A section of the Python code for the vending machine program is shown below.')]
Q14B = Q14_INTRO + [P(14, 'The vending machine needs to be tested before it is released.')]
Q15A = P(16, 'A museum has an information point, such as that shown in Figure 7', 'on their own smart device.')
Q15B = [Q15A, P(17, 'The diagram in Figure 8 below illustrates', 'software development design process.')]
Q15C = [Q15A, P(18, 'One of the designers wants to build location tracking', 'where visitors go in the museum.')]
Q16A_STEM = C(4, 'The program below is the start of a program to help floor tilers', 'total area of the floor.')
CORRECT = S(20, 'Correct implementation using solution above or similar.')

CARDS = [
    # ── Section A ──────────────────────────────────────────────────────────
    dict(key=(1, None, None), topic='cs-2-2', qfigure='q1-code', total=6,
         why='p3: the output for six ages; the scheme prints each, 1 mark',
         ask=[P(3, 'The Python program below takes a person’s age', 'value entered for the person’s age.'),
              P(3, 'For each value in Column A', 'in Column B.')],
         rows=[pt(S(4, '21 A'), 1, note=S(4, 'Each correct item 1 mark', nth=1)),
               pt(S(4, '-1 B'), 1), pt(S(4, '0 B'), 1), pt(S(4, '16 C'), 1),
               pt(S(4, '100 A'), 1), pt(S(4, '15 B'), 1)]),
    dict(key=(2, None, None), topic='cs-2-3', total=6,
         replaces='batch 1b: the menu\'s head was its own first answer and each reason a fixed 3; '
                  'now any two reasons at 3 / 2, the accept line as instruction',
         why='p3: two reasons for cloud storage; the scheme lists six and accepts any relevant, '
             'each 3 / 2',
         ask=P(3, 'It is common for people to store files in the cloud.', 'rather than local storage.'),
         rows=[ladder([S(4, 'Accessibility: Cloud storage allows you', 'with an internet connection.'),
                       S(4, 'Backup and Security:', 'advanced security measures.'),
                       S(4, 'File Sharing and Collaboration:', 'collaborate with others.'),
                       S(4, 'Automatic Updates:', 'updates and maintenance.'),
                       S(4, 'Disaster Recovery:', 'safe and recoverable.'),
                       S(4, 'Cost Efficiency:', 'other local storage devices.')], [[2, 3], [2, 3]],
                      instruction=S(4, 'Accept any relevant answers given.'),
                      note=S(4, 'For each reason:', 'Fair description – limited understanding 2 marks'))]),
    dict(key=(3, None, None), topic='cs-2-3', qfigure='q3-fig0', total=6,
         replaces='batch 1b: the table header and scheme column titles were rows and nothing was '
                  'priced; now (a)\'s three matches at 1 and (b) any one reason at 3 / 2, on the '
                  'question\'s printed total',
         why='p4: whole question (no part cards): (a) match three bases, each correct item 1; '
             '(b) why binary, the scheme lists four and accepts any relevant, 3 / 2',
         ask=P(4, '(a) Choose the appropriate number system', 'rather than the decimal number system.'),
         rows=[ofpart(P(4, '(a)'), pt(S(5, '2 Binary'), 1, note=S(5, 'Each correct item 1 mark'))),
               ofpart(P(4, '(a)'), pt(S(5, '10 Decimal'), 1)), ofpart(P(4, '(a)'), pt(S(5, '16 Hexadecimal'), 1)),
               ofpart(P(4, '(b)'), ladder([S(5, 'Simplicity for Hardware:', 'on (1) and off (0).'),
                       S(5, 'Reliability: Using just two states', 'errors or misinterpretations.'),
                       S(5, 'Efficiency in Processing:', 'only needs to handle two states.'),
                       S(5, 'Compatibility with Logic:', 'decision-making in computers.')], [[2, 3]],
                      instruction=S(5, 'Accept any relevant answers given.'),
                      note=S(5, 'Good description – clear understanding demonstrated 3 marks',
                             'Fair description – limited understanding 2 marks')))]),
    dict(key=(4, None, None), topic='cs-2-3', total=6,
         replaces='batch 1b: one answer was the only row, all or nothing; now any one of the '
                  'scheme\'s five at 6 / 4 / 2',
         why='p4: one reason Unicode replaced ASCII; the scheme lists five and accepts any '
             'relevant, 6 / 4 / 2',
         ask=P(4, 'Unicode has largely replaced ASCII', 'Suggest one reason for this.'),
         rows=[ladder([S(5, 'Unicode supports a wide range of characters', 'international communication and content.'),
                       S(5, 'ASCII can only represent 128 characters', 'special characters used.'),
                       S(5, 'Unicode allows for new characters to be added over time', 'added in future.'),
                       S(5, 'Unicode provides a universal standard', 'without compatibility issues.'),
                       S(5, 'Modern software and web applications', 'wide range of applications.')], [[2, 4, 6]],
                      instruction=S(5, 'Accept any relevant answer provided.'),
                      note=S(5, 'Very good explanation - clear understanding demonstrated 6 marks',
                             'Fair explanation - limited understanding 2 marks'))]),
    dict(key=(5, None, None), topic='cs-2-4', qfigure='q5-code', total=6,
         why='p5: the data type of five variables; the scheme prints them, all correct 6 or '
             'each correct 1, so the fifth correct is worth 2',
         ask=P(5, 'There are a number of variable declarations', 'integer float bool list string'),
         rows=[anyn([S(6, 'name string'), S(6, 'age integer'), S(6, 'student bool'),
                     S(6, 'exam_marks list'), S(6, 'average_mark float')], 5, 1, steps=[1, 1, 1, 1, 2],
                    head=P(5, 'Choose the appropriate Python data type from the list below', 'in Column A.'),
                    note=S(6, 'All correct 6 marks or Each correct item 1 mark'))]),
    dict(key=(6, None, None), topic='cs-1-2', total=6,
         replaces='batch 1b: one concern was the only row, worth 6; now any two at 3 / 2; topic '
                  'Computers and society',
         why='p5: two social or ethical concerns of AR headsets; the scheme lists five and '
             'accepts any other valid, each 3 / 2; filed under Computers and society, not Data',
         ask=P(5, 'The Apple Vision Pro is a new augmented reality', 'concerns that this device may raise.'),
         rows=[ladder([S(6, 'Privacy Issues:', 'amounts of personal data.'),
                       S(6, 'Social Isolation:', 'weaken real-world relationships.'),
                       S(6, 'Addiction and Overuse:', 'sleep, and productivity.'),
                       S(6, 'Digital Divide:', 'and those who don\'t.'),
                       S(6, 'Impact on Mental Health:', 'distorted sense of self.')], [[2, 3], [2, 3]],
                      instruction=S(6, 'Accept any other valid answers.'),
                      note=S(6, 'For each explanation:', 'Fair description – limited understanding 2 marks'))]),
    dict(key=(7, None, None), topic='cs-2-1', qfigure='q7-fig0', total=6,
         replaces='batch 1b: the map was the answer figure and every map feature and half of '
                  'the definition were unpriced rows; now (a) any two at 1 and (b) 4 / 2, on the '
                  'question\'s printed total, the map beside the question',
         why='p6: whole question (no part cards): (a) two abstractions in the map, the scheme '
             'lists eight, each 1; (b) define abstraction, 4 / 2',
         stem=P(6, 'Abstraction is used in maps', 'read them with more ease.'),
         ask=P(6, '(a) List two ways in which abstraction', 'in relation to computer science?'),
         rows=[ofpart(P(6, '(a)'), anyn([S(7, 'Removing unnecessary details such as buildings, trees etc'), S(7, 'Simplified roads'),
                     S(7, 'Simplified river'), S(7, 'Simplified railway line'), S(7, 'Green areas'),
                     S(7, 'Text labels on street names / road numbers'), S(7, 'Symbols for bus stops'),
                     S(7, 'Place names for important buildings')], 2, 1,
                    head=S(7, 'Simplified items on the map are considered forms of abstraction such as:'),
                    instruction=S(7, 'Accept any other valid forms of validation given'),
                    note=S(7, 'Each correct item 1 mark', nth=1))),
               ofpart(P(6, '(b)'), crit(S(7, 'Abstraction means simplifying complex systems', 'hiding the unnecessary ones.'), 4, [2],
                    note=S(7, 'Good description – clear understanding demonstrated 4 marks',
                           'Fair description – limited understanding 2 marks')))]),
    dict(key=(8, None, None), topic='cs-2-3', qfigure='q8-fig2', total=6,
         replaces='batch 1b: the two answers were unpriced rows and Figure 2 was missing; now '
                  'each component 3 / 2, on the question\'s printed total, with Figure 2',
         why='p7: whole question (no part cards): the purpose of the CPU and of input devices; '
             'the scheme answers each, 3 / 2',
         stem=P(7, 'Jeremy is building a desktop computer', 'components of a desktop computer:'),
         ask=P(7, '(i) Central Processing Unit (CPU) (ii) Input devices'),
         rows=[ofpart(P(7, '(i)'), crit(S(7, 'CPU: The CPU (Central Processing Unit)', 'processing inside a computer'), 3, [2],
                    note=S(7, 'For each: Good description', 'Fair description – limited understanding 2 marks'))),
               ofpart(P(7, '(ii)'), crit(S(7, 'Input Devices: Input devices are components', 'into a computer system.'), 3, [2]))]),
    dict(key=(9, None, None), topic='cs-2-3', qfigure='q9-table', total=6,
         why='p7: six statements true or false; the scheme lists the answers in order, 1 each',
         ask=P(7, 'State whether each of the following statements is true or false', 'in the appropriate box.'),
         rows=[pt(Pair(P(7, 'The Internet and the World Wide Web are the same thing'), S(7, 'False', nth=1)), 1,
                  note=S(7, 'Each correct item 1 mark', nth=2)),
               pt(Pair(P(7, 'HTTP is a mark-up language for making web pages'), S(7, 'False', nth=2)), 1),
               pt(Pair(P(7, 'A URL is an address for a web page'), S(7, 'True', nth=1)), 1),
               pt(Pair(P(7, 'Data is communicated over the World Wide Web using HTTP'), S(7, 'True', nth=2)), 1),
               pt(Pair(P(7, 'HTTPS is more secure than HTTP'), S(7, 'True', nth=3)), 1),
               pt(Pair(P(7, 'The server sends the first communication in the client-server model'),
                       S(7, 'False', nth=3)), 1)]),
    dict(key=(10, None, None), topic='cs-2-2', qfigure='q10-fig0', total=6,
         replaces='batch 1b: the six output values were six unpriced rows and the flowchart the '
                  'answer figure; now the printed output at 6 / 4 / 2 with Figure 3 beside the '
                  'question',
         why='p8: the output of the flowchart; the scheme prints 0 2 4 6 8 10, fully correct 6, '
             'almost 4, any valid 2',
         ask=P(8, 'The flowchart, in Figure 3 below', 'Calculate the output of the algorithm.'),
         rows=[crit(S(8, '0 2 4 6 8 10'), 6, [2, 4], note=S(8, 'Fully correct 6 marks', 'Any valid response 2 marks'))]),
    dict(key=(11, None, None), topic='cs-2-2', qfigure='q11-boxes', total=6,
         why='p9: the list after swaps 1 to 4 of a selection sort; the scheme prints each, all '
             'rows 6, three 4, two 3, one 2',
         ask=P(9, 'A selection sort (simple sort), which repeatedly selects', 'List = [13, 54, 4, 81, 92, 26]'),
         rows=[anyn([S(8, 'Swap 1 4 54 13 81 92 26'), S(8, 'Swap 2 4 13 54 81 92 26'),
                     S(8, 'Swap 3 4 13 26 81 92 54'), S(8, 'Swap 4 4 13 26 54 92 81')], 4, 2, steps=[2, 1, 1, 2],
                    head=S(8, 'Initial state 13 54 4 81 92 26'),
                    note=S(8, 'All rows correct 6 marks', '1 row correct 2 marks'))]),
    dict(key=(12, None, None), topic='cs-2-2', qfigure='q12-code0', total=6,
         replaces='batch 1b: the listing was the answer figure and the answer all or nothing; now '
                  '6 / 4 / 2 with the listing beside the question',
         why='p9: why the TypeError occurs and the fix; the scheme answers it, 6 / 4 / 2',
         ask=P(9, 'A piece of Python code is displayed below.', 'how it could be fixed.'),
         rows=[ladder([S(8, 'This error has occurred as the code is trying', 'myNum to an integer.')], [[2, 4, 6]],
                      instruction=S(8, 'Any valid response'),
                      note=S(8, 'Very good explanation - clear understanding demonstrated 6 marks',
                             'Fair explanation - limited understanding 2 marks'))]),
    # ── Section B ──────────────────────────────────────────────────────────
    dict(key=(13, 'a', 'i'), topic='cs-2-3', total=6,
         replaces='batch 1b: the stem was the caption "Figure 4" and the row one development worth '
                  '6; now the ENIAC stem and any three of twelve at 2',
         why='p10: three computing developments; the scheme lists twelve and accepts other '
             'relevant answers, each 2',
         stem=Q13A, ask=P(10, 'List three other important computing developments', 'in the last 100 years.'),
         rows=[anyn([S(9, 'The development of the Turing Machine'),
                     S(9, 'The development of algorithms and software', 'programming language compilers'),
                     S(9, 'The invention of the internet'), S(9, 'The development of the personal computer (PC)'),
                     S(9, 'The advancement of artificial intelligence (AI)'), S(9, 'The creation of the World Wide Web'),
                     S(9, 'The development of mobile phones and smartphones'), S(9, 'The rise of cloud computing'),
                     S(9, 'The expansion of wireless networking (wi-fi and 5g)'),
                     S(9, 'The creation of graphical user interfaces (GUIs)'), S(9, 'The invention of the microprocessor'),
                     S(9, 'The rise of blockchain and cryptocurrencies')], 3, 2,
                    head=P(10, 'List three other important computing developments', 'in the last 100 years.'),
                    instruction=S(9, 'Accept other relevant answers'), note=S(9, 'Each valid answer 2 marks'))]),
    dict(key=(13, 'a', 'ii'), topic='cs-2-3', total=6,
         why='p10: explain one of the developments listed in (i); the scheme prints no answer, '
             'only that any one may be chosen, 6 / 3 (new part card: the shipped whole-question '
             'card cs-2025-ol-q13 is withdrawn onto it)',
         stem=Q13A, ask=P(10, 'Choose one of the developments from part (i) and explain its importance.'),
         rows=[unprinted(S(9, 'Candidates can select any one', 'Fair explanation - limited understanding 3 marks'))]),
    dict(key=(13, 'a', 'iii'), topic='cs-2-3', total=4,
         replaces='batch 1b: the stem was the caption "Figure 4" and the row one trend worth 4; '
                  'now any one of ten, named 1 and explained 3 / 2',
         why='p10: name and explain an emerging trend; the scheme lists ten and accepts any '
             'other valid, name 1 and explanation 3 / 2',
         stem=Q13A, ask=P(10, 'Artificial intelligence and machine learning are major trends', 'one other emerging trend in computing.'),
         rows=[ladder([S(10, 'Quantum computing:', 'drug discovery, etc.'), S(10, 'Edge Computing:', 'autonomous vehicles.'),
                       S(10, 'Self-Driving Cars:', 'needing a human driver.'), S(10, 'Smart Homes:', 'apps or voice commands.'),
                       S(10, '3D Printing:', 'and even houses.'), S(10, 'Blockchain:', '(cryptocurrencies) safer.'),
                       S(10, 'Extended Reality (XR):', 'remote collaboration.'), S(10, 'Robotics:', 'assist in hospitals.'),
                       S(10, 'Wearable Tech:', 'your health and activity.'), S(10, 'Drones:', 'exploring areas.')],
                      [[1, 2, 3, 4]], instruction=S(10, 'Accept any other valid answer'),
                      note=S(10, 'Valid name 1 mark', 'Fair explanation - limited understanding 2 marks'))]),
    dict(key=(13, 'b', 'i'), topic='cs-2-3', qfigure='q13-fig0', total=6,
         replaces='batch 1b: the stem was furniture ("Figure 5 This question continues...") and '
                  'the row the application layer alone, worth 6; now both layers at 3 / 2 with '
                  'Figure 5 beside the question',
         why='p11: the purpose of the application and hardware layers; the scheme answers each, '
             '3 / 2',
         stem=Q13B, ask=P(11, 'Explain the purpose of the application and hardware layers.'),
         rows=[crit(S(10, 'Application Layer: This is to provide', 'what we directly interact with.'), 3, [2],
                    note=S(10, 'For each: Good explanation', 'Fair description – limited understanding 2 mark')),
               crit(S(10, 'Hardware Layer: The purpose of the hardware layer', 'run and do tasks.'), 3, [2])]),
    dict(key=(13, 'b', 'ii'), topic='cs-2-3', qfigure='q13-fig0', total=6,
         replaces='batch 1b: the stem was furniture and the row one function worth 6; now any '
                  'three of nine at 2',
         why='p11: three functions of an operating system; the scheme lists nine and accepts '
             'other correct functions, each 2',
         stem=Q13B, ask=P(11, 'Apple iOS, Microsoft Windows, and Android OS', 'functions of an operating system.'),
         rows=[anyn([S(11, 'Managing Hardware'), S(11, 'Managing Resources'), S(11, 'Provides a User Interface'),
                     S(11, 'Running / Managing Applications'), S(11, 'File Management'), S(11, 'Memory Management'),
                     S(11, 'Security/ Access control'), S(11, 'Device Management'), S(11, 'Multitasking')], 3, 2,
                    head=P(11, 'List three functions of an operating system.'),
                    instruction=S(11, 'Accept other correct functions of the OS'),
                    note=S(11, 'Each valid answer 2 marks'))]),
    dict(key=(13, 'b', 'iii'), topic='cs-2-3', qfigure='q13-fig0', total=4,
         replaces='batch 1b: the stem was furniture and the row one example worth 4; now any two '
                  'of ten at 2 / 1',
         why='p12: two embedded systems in everyday life; the scheme lists ten and accepts any '
             'other correct, each 2 / 1 (name only 1)',
         stem=Q13B, ask=P(12, 'The enhancement of computers over the last few decades', 'embedded systems in our everyday lives.'),
         rows=[ladder([S(11, 'Washing Machines –', 'spin speeds.'), S(11, 'Microwave Ovens –', 'even heating.'),
                       S(11, 'Smartphones –', 'battery management.'), S(11, 'Cars –', 'GPS navigation.'),
                       S(11, 'Smart TVs –', 'app functionality.'), S(11, 'Fitness Trackers –', 'sleep patterns.'),
                       S(11, 'Home Security Systems –', 'motion sensors for safety.'),
                       S(11, 'Digital Cameras –', 'image processing.'), S(11, 'Printers –', 'printing tasks.'),
                       S(11, 'Thermostats –', 'temperature settings.')], [[1, 2], [1, 2]],
                      instruction=S(11, 'Accept any other correct answer.'),
                      note=S(11, 'For each: Good description', 'name only – limited understanding 1 mark'))]),
    dict(key=(13, 'c', None), topic='cs-1-2', total=6, printed=S(12, '(c) 6 (3,3) marks'),
         replaces='batch 1b fix: one ladder whose options read each career with its two '
                  '"o" sub-bullets run into one line; now the names and the activities '
                  'as two menus, one line each, the "o" bullet not read',
         why='p12: two careers with two activities each; the scheme lists eight careers with '
             'two activities each and prices each name 1 and each activity 1 (max 2), so '
             'the names are any two at 1 and the activities any four at 1, each named '
             'with its career (new part card)',
         ask=P(12, 'Name two computer-related careers', 'the person would undertake.'),
         rows=[anyn([S(12, 'Software Developer'),
                     S(12, 'Web Developer'),
                     S(12, 'Data Analyst'),
                     S(12, 'Cybersecurity Analyst'),
                     S(12, 'IT Support Specialist'),
                     S(12, 'Network Administrator'),
                     S(12, 'Game Developer'),
                     S(12, 'UX/UI Designer')], 2, 1,
                    head=S(12, 'Valid name 1 mark'),
                    note=S(12, 'For each: Valid name 1 mark', 'Each valid activity 1 mark (max 2)')),
               anyn([Pair(S(12, 'Software Developer'), S(12, 'Writing and testing code for applications.')),
                     Pair(S(12, 'Software Developer'), S(12, 'Collaborating with teams to design software solutions.')),
                     Pair(S(12, 'Web Developer'), S(12, 'Building and maintaining websites.')),
                     Pair(S(12, 'Web Developer'), S(12, 'Ensuring websites are optimized for performance and usability.')),
                     Pair(S(12, 'Data Analyst'), S(12, 'Analysing datasets to extract meaningful insights.')),
                     Pair(S(12, 'Data Analyst'), S(12, 'Creating visualisations and reports to present findings.')),
                     Pair(S(12, 'Cybersecurity Analyst'), S(12, 'Monitoring systems for security breaches.')),
                     Pair(S(12, 'Cybersecurity Analyst'), S(12, 'Implementing measures to protect sensitive data.')),
                     Pair(S(12, 'IT Support Specialist'), S(12, 'Troubleshooting hardware and software issues for users.')),
                     Pair(S(12, 'IT Support Specialist'), S(12, 'Installing and configuring computer systems.')),
                     Pair(S(12, 'Network Administrator'), S(12, 'Managing and maintaining computer networks.')),
                     Pair(S(12, 'Network Administrator'), S(12, 'Ensuring network security and performance.')),
                     Pair(S(12, 'Game Developer'), S(12, 'Designing and programming video games.')),
                     Pair(S(12, 'Game Developer'), S(12, 'Testing games for bugs and optimizing gameplay.')),
                     Pair(S(12, 'UX/UI Designer'), S(12, 'Creating wireframes and prototypes for software or websites.')),
                     Pair(S(12, 'UX/UI Designer'), S(12, 'Conducting user testing to improve product usability.'))], 4, 1,
                    head=S(12, 'Each valid activity 1 mark (max 2)'))]),
    dict(key=(14, 'a', 'i'), topic='cs-2-2', qfigure='q14a-code', total=5,
         replaces='batch 1b: the stem was "This question continues on the next page." and the '
                  'answer all or nothing; now the vending-machine stem, the table and code beside '
                  'the question, 5 / 3',
         why='p13: the purpose of the conditional on line 1; the scheme answers it, 5 / 3',
         stem=Q14A, ask=P(13, 'Line 1 of the code has a conditional statement.', 'purpose of this conditional statement.'),
         rows=[crit(S(13, 'It is to check that the user has entered enough money to buy the selected item'), 5, [3],
                    note=S(13, 'Good explanation – clear understanding demonstrated 5 marks',
                           'Fair description – limited understanding 3 marks'))]),
    dict(key=(14, 'a', 'ii'), topic='cs-2-2', qfigure='q14a-code', total=1,
         replaces='batch 1b: the stem was "This question continues on the next page."; now the '
                  'vending-machine stem with the table and code beside the question',
         why='p13: a data type for price; the scheme answers float, 1',
         stem=Q14A, ask=P(13, 'State a suitable data type for the variable price.'),
         rows=[pt(S(13, 'float'), 1)]),
    dict(key=(14, 'b', 'i'), topic='cs-2-5', qfigure='q14-items', total=4,
         replaces='batch 1b: the stem was the test plan as text and one test the only row, worth '
                  '4; now any one of six tests at 4 / 2',
         why='p14: describe a unit test; the scheme lists six and any similar, 4 / 2',
         stem=Q14B, ask=P(14, 'Describe a unit test that should take place for the vending machine.'),
         rows=[ladder([S(13, 'Verify that selecting a specific snack', 'correctly identifies the item'),
                       S(13, 'Check if the vending machine accepts and processes', 'for a €1.50 snack.'),
                       S(13, 'Check that the vending machine dispenses the correct change', 'too much money is entered'),
                       S(13, 'Check that the card facility for payment is working'),
                       S(13, 'Check that the vending machine doesn’t allow', 'if it is sold out'),
                       S(13, 'Check that the cancel button returns funds')], [[2, 4]],
                      instruction=S(13, 'Any similar valid response'),
                      note=S(13, 'Good description – clear understanding demonstrated 4 marks',
                             'Fair description – limited understanding 2 marks'))]),
    dict(key=(14, 'b', 'ii'), topic='cs-2-5', qfigure='q14b-plan', figure='s-q14b-ii', total=9,
         replaces='batch 1b: the one row was the table header worth 9; now the three completed '
                  'rows, each correct item 3, with the scheme\'s table; topic Evaluation and '
                  'testing',
         why='p14: fill the test plan\'s three blanks (A2, <2, the C2 error); the scheme prints '
             'the completed plan, each correct item 3; filed under Evaluation and testing, not '
             'Algorithms',
         stem=Q14B, ask=P(14, 'The table below shows a test plan', 'information in the blank spaces.'),
         rows=[pt(S(14, 'A2 1.2 Water served, no change given'), 3, note=S(14, 'Each correct item 3 marks')),
               pt(S(14, 'C1 <2 Error – not enough money inserted'), 3),
               pt(S(14, 'C2 0.75 Error – not enough money inserted'), 3)]),
    dict(key=(14, 'b', 'iii'), topic='cs-2-5', qfigure='q14-items', total=3,
         replaces='batch 1b: one stage was the only row, worth 3; now any one of six, named 1 '
                  'and explained 2 / 1; topic Evaluation and testing',
         why='p14: name and explain a stage of testing; the scheme lists six and any other '
             'valid, name 1 and description 2 / 1; filed under Evaluation and testing, not '
             'Computer systems',
         stem=Q14B, ask=P(14, 'Name and explain a stage of software testing', 'works as intended when it is released.'),
         rows=[ladder([S(14, 'Functional Testing.', 'the code button is entered.'),
                       S(14, 'Non-Functional Testing.', 'serve in an hour.'),
                       S(14, 'System Testing.', 'works together seamlessly.'),
                       S(14, 'User Acceptance Testing (UAT).', 'easy to use.'),
                       S(14, 'Alpha testing.', 'works as expected.'),
                       S(14, 'Beta testing.', 'might have missed.')], [[1, 2, 3]],
                      instruction=S(14, 'Any other valid stage of software testing is acceptable'),
                      note=S(14, 'Valid name 1 mark', 'Fair description – limited understanding 1 mark'))]),
    dict(key=(14, 'b', 'iv'), topic='cs-1-2', qfigure='q14-items', total=8,
         replaces='batch 1b: one feature was the only row, worth 8; now any two of six at 4 / 2; '
                  'topic Computers and society',
         why='p15: two accessibility features; the scheme lists six and any other valid, each '
             '4 / 2; filed under Computers and society (1.15, universal design), not Algorithms',
         stem=Q14B, ask=P(15, 'Describe two design features that could be incorporated', 'as many different types of users as possible.'),
         rows=[ladder([S(15, 'Large Buttons:', 'visual impairments.'), S(15, 'Braille:', 'make selections.'),
                       S(15, 'Audio:', 'visually impaired users.'), S(15, 'Height Position:', 'machine comfortably.'),
                       S(15, 'Touchscreen:', 'cognitive disabilities.'),
                       S(15, 'Multi-Language Support:', 'displayed on the machine.')], [[2, 4], [2, 4]],
                      instruction=S(15, 'Any other valid design feature'),
                      note=S(15, 'For each: Good description', 'Fair description – limited understanding 2 marks'))]),
    dict(key=(14, 'c', None), topic='cs-2-2', qfigure='q14-items', figure='s-q14c', total=8,
         printed=S(15, '(c) 8 marks'),
         why='p15: an algorithm or flowchart for the stock checks; the scheme prints pseudocode '
             'and a flowchart and prices two conditions 3 / 2 and coherence 2 / 1 (new part card: '
             'the shipped whole-question card cs-2025-ol-q14 is withdrawn onto it)',
         stem=Q14_INTRO, ask=P(15, 'When the user inserts the correct amount of money', 'order more stock for the vending machine.'),
         rows=[crit(S(15, 'Correctly deals with condition to check if any items available'), 3, [2],
                    note=S(15, 'Reasonable attempt at condition to check if any items available 2 marks')),
               crit(S(15, 'Correctly deals with condition to send email where stock is less than 3'), 3, [2],
                    note=S(15, 'Reasonable attempt at condition to send email where stock is less than 3 2 marks')),
               crit(S(15, 'Good overall coherence of flowchart/pseudocode'), 2, [1],
                    note=S(15, 'Fair overall coherence of flowchart/pseudocode 1 marks'))]),
    dict(key=(15, 'a', 'i'), topic='cs-1-3', qfigure='q15-fig0', total=9,
         printed=S(16, '(i) 9 (3, 3, 3) marks'),
         replaces='batch 1b: priced 8 (the scheme prints 9) with the stem the caption "Figure 7" '
                  'and one stakeholder\'s name as the row; now any three of ten, stakeholder 1 '
                  'and requirement 2; topic Designing and developing',
         why='p16: three stakeholders with a requirement each; the scheme lists ten and any '
             'other valid, stakeholder 1 and requirement 2; filed under Designing and developing '
             '(1.21, stakeholders), not Computer systems',
         stem=Q15A, ask=P(16, 'Identify three potential stakeholders for this app.', 'one requirement they have for the app.'),
         rows=[ladder([S(16, 'Museum Visitors Requirement:', 'as they explore the museum.'),
                       S(16, 'Museum Staff Requirement:', 'current and relevant.'),
                       S(16, 'Museum Administrators Requirement:', 'gather visitor insights.'),
                       S(16, 'Tour Guides Requirement:', 'without conflicting information.'),
                       S(16, 'External Sponsors or Partners', 'or dedicated sections.'),
                       S(16, 'Project Manager Requirement:', 'risks and resources effectively.'),
                       S(16, 'Team Leader (e.g., Lead Developer or Design Lead)', 'set by the project goals.'),
                       S(16, 'UX Designer Requirement:', 'accessible design principles.'),
                       S(16, 'Software Developer Requirement:', 'Android and iOS platforms.'),
                       S(16, 'IT Support Staff Requirement:', 'deploy and troubleshoot.')],
                      [[1, 2, 3], [1, 2, 3], [1, 2, 3]],
                      instruction=S(16, 'Any other valid stakeholder and requirement'),
                      note=S(16, 'For each: Valid stakeholder 1 mark Valid requirement 2 marks'))]),
    dict(key=(15, 'a', 'ii'), topic='cs-1-2', qfigure='q15-fig0', total=6,
         replaces='batch 1b: the stem was the caption "Figure 7" and one feature the only row, '
                  'worth 6; now any two of eight at 3 / 2; topic Computers and society',
         why='p17: two adaptive or assistive features; the scheme lists eight and accepts other '
             'valid technologies, each 3 / 2; filed under Computers and society (1.15), not '
             'Algorithms',
         stem=Q15A, ask=P(17, 'Describe two adaptive or assistive technology features', 'focus on for the project.'),
         rows=[ladder([S(17, 'Screen Reader Compatibility:', 'information effectively.'),
                       S(17, 'Text-to-Speech Option:', 'instead of reading it.'),
                       S(17, 'Adjustable Text Size and Contrast:', 'visual comfort.'),
                       S(17, 'Alternative Text for Images:', 'through screen readers.'),
                       S(17, 'Voice Command Navigation:', 'hands-free accessibility.'),
                       S(17, 'Multilingual Support:', 'diverse range of users.'),
                       S(17, 'Simplified Interface with Large Buttons:', 'limited dexterity.'),
                       S(17, 'Closed Captions for Audio/Video Content:', 'deaf or hard of hearing.')],
                      [[2, 3], [2, 3]],
                      instruction=S(17, 'Accept other valid technologies that have been described.'),
                      note=S(17, 'For each: Good description', 'Fair description – limited understanding 2 marks'))]),
    dict(key=(15, 'b', 'i'), topic='cs-1-3', qfigure='q15-figs', total=8,
         printed=S(17, '(i) 8 (2, 2, 2, 2) marks'),
         why='p17: one activity at each of four stages; the scheme lists five and any other '
             'valid per stage, each 2 (new part card: the shipped whole-question card '
             'cs-2025-ol-q15 is withdrawn onto it)',
         stem=Q15B, ask=P(17, 'Outline one activity that your team will undertake', 'listed in the answer box below.'),
         rows=[anyn([S(17, 'Identify stakeholders'), S(17, 'Gather requirements', nth=1), S(17, 'Conduct market research'),
                     S(17, 'Define project objectives'), S(17, 'Review current similar products'),
                     S(17, 'Any other valid activity', nth=1)], 1, 2, open_list=True, head=S(17, 'Investigate:'),
                    note=S(18, 'For each: Valid activity 2 marks')),
               anyn([S(17, 'Setout timeline'), S(17, 'Setout milestones'), S(17, 'Gather requirements', nth=2),
                     S(17, 'Assign roles & tasks'), S(17, 'Create project plan'),
                     S(17, 'Any other valid activity', nth=2)], 1, 2, open_list=True, head=S(17, 'Plan:')),
               anyn([S(18, 'Quality assurance'), S(18, 'Test results'), S(18, 'User feedback'),
                     S(18, 'Review success criteria'), S(18, 'Areas for improvement'),
                     S(18, 'Any other valid activity', nth=1)], 1, 2, open_list=True, head=S(18, 'Evaluate:')),
               anyn([S(18, 'Create user guide'), S(18, 'Create FAQa'), S(18, 'Installation / Setup guide'),
                     S(18, 'Troubleshooting support'), S(18, 'Project review'),
                     S(18, 'Any other valid activity', nth=2)], 1, 2, open_list=True, head=S(18, 'Document:'))]),
    dict(key=(15, 'b', 'ii'), topic='cs-1-3', qfigure='q15-figs', total=6,
         printed=S(18, '(ii) 6 (3, 3) marks'),
         why='p18: two arguments for keeping the iterative process; the scheme lists seven, '
             'each 3 / 2 (new part card)',
         stem=Q15B, ask=P(18, 'One of the team has suggested using a staged', 'retaining the iterative development process.'),
         rows=[ladder([S(18, 'Flexibility and adaptability:', 'delivering an unsuitable product.'),
                       S(18, 'Early detection of issues:', 'major failures later in development.'),
                       S(18, 'User involvement and satisfaction:', 'throughout the development process.'),
                       S(18, 'Risk management:', 'before they become major problems.'),
                       S(18, 'Improved quality and performance:', 'user-friendly product.'),
                       S(18, 'Encourages collaboration:', 'alignment with project goals.'),
                       S(18, 'Better cost and time management:', 'likelihood of project overruns.')], [[2, 3], [2, 3]],
                      note=S(18, 'For each argument:', 'Fair description – limited understanding 2 marks'))]),
    dict(key=(15, 'c', 'i'), topic='cs-2-4', qfigure='q15-fig0', total=5,
         replaces='batch 1b: the stem was "Space for extra work" pages and one benefit the only '
                  'row, worth 5; now the museum stem and any one of seven at 5 / 4',
         why='p18: one benefit of location tracking; the scheme lists seven and any other valid, '
             '5 / 4',
         stem=Q15C, ask=P(18, 'Describe one benefit of including this technology.'),
         rows=[ladder([S(19, 'Enhanced navigation:', 'their overall experience.'),
                       S(19, 'Personalised tours:', 'interactive visit.'),
                       S(19, 'Contextual information:', 'exhibits or landmarks.'),
                       S(19, 'Crowd management:', 'security and safety.'),
                       S(19, 'Interactive experiences:', 'more dynamic and fun.'),
                       S(19, 'Accessibility support:', 'based on their location.'),
                       S(19, 'Visitor insights:', 'plan future exhibits.')], [[4, 5]],
                      instruction=S(19, 'Any other valid benefit'),
                      note=S(19, 'Good description – clear understanding demonstrated 5 marks',
                             'Fair description – limited understanding 4 marks'))]),
    dict(key=(15, 'c', 'ii'), topic='cs-1-2', qfigure='q15-fig0', total=4,
         replaces='batch 1b: the stem was "Space for extra work" pages and one concern the only '
                  'row, worth 4; now the museum stem and any one of nine at 4 / 3',
         why='p18: one ethical concern of location tracking; the scheme lists nine, 4 / 3',
         stem=Q15C, ask=P(18, 'Describe one ethical concern of including this technology.'),
         rows=[ladder([S(19, 'Privacy and data collection:', 'stored, used, and shared.'),
                       S(19, 'Data security:', 'compromising user privacy.'),
                       S(19, 'Informed consent (GDPR):', 'opt-in and opt-out options.'),
                       S(19, 'Surveillance concerns:', 'mistrust among visitors.'),
                       S(19, 'Digital divide:', 'excluded or disadvantaged.'),
                       S(19, 'Bias in recommendations:', 'equally important displays.'),
                       S(19, 'Dependence on technology:', 'the physical environment.'),
                       S(19, 'Misuse by third parties:', 'applications of the data.'),
                       S(19, 'Impact on children:', 'parental consent is obtained.')], [[3, 4]],
                      note=S(19, 'Good description – clear understanding demonstrated 4 marks',
                             'Fair description – limited understanding 3 marks'))]),
    # ── Section C ──────────────────────────────────────────────────────────
    dict(key=(16, 'a', 'i'), topic='cs-2-2', qfigure='q16a-code', figure='s-q16a', total=10,
         why='040 p4: print the new welcome; the scheme marks line 4 #(i), A-10 scale',
         stem=Q16A_STEM,
         ask=C(4, 'Modify the program so that it first prints out', 'The area of the floor is: 200.0', end_nth=1),
         rows=[crit(CORRECT, 10, [5], note=S(20, '(i) 10 marks (A-10 scale)', 'Any other reasonable attempt.'))]),
    dict(key=(16, 'a', 'ii'), topic='cs-2-2', qfigure='q16a-code', figure='s-q16a', total=10,
         why='040 p4: display the length entered in metres; the scheme marks line 13 # (ii), '
             'B-10 scale',
         stem=Q16A_STEM,
         ask=C(4, 'Modify the program to display a message stating the length', 'The area of the floor is: 200.0', end_nth=1),
         rows=[crit(CORRECT, 10, [3, 7], note=S(20, '(ii) 10 marks (B-10 scale)', 'Any other reasonable attempt.'))]),
    dict(key=(16, 'a', 'iii'), topic='cs-2-2', qfigure='q16a-code', figure='s-q16a', total=10,
         why='040 p5: read and display the width; the scheme marks lines 7 and 14 # (iii), B-10 '
             'scale',
         stem=Q16A_STEM,
         ask=C(5, 'Currently, the width of the room is “hard-coded”', 'The area of the floor is: 30.0', end_nth=1),
         rows=[crit(CORRECT, 10, [3, 7], note=S(21, '(iii) 10 marks (B-10 scale)', 'Any other reasonable attempt.'))]),
    dict(key=(16, 'a', 'iv'), topic='cs-2-2', qfigure='q16a-code', figure='s-q16a', total=10,
         why='040 p5: a cost-per-square-metre variable, printed; the scheme marks lines 11 and '
             '16 (iv), C-10 scale',
         stem=Q16A_STEM,
         ask=C(5, 'Add a new variable with a suitable name for the cost per square metre',
               'The cost per square metre is: 15', end_nth=1),
         rows=[crit(CORRECT, 10, [3, 5, 8], note=S(21, '(iv) 10 marks (C-10 scale)', 'Any other reasonable attempt.'))]),
    dict(key=(16, 'a', 'v'), topic='cs-2-2', qfigure='q16a-code', figure='s-q16a', total=10,
         replaces='batch 1b: filed as section B with the copy-the-file instructions as its stem '
                  'and five 2-mark rows of scale furniture; now section C, the C-10 scale and the '
                  'scheme\'s lines 18-19',
         why='040 p5: calculate and print the total cost; the scheme marks lines 18-19 # (v), '
             'C-10 scale',
         stem=Q16A_STEM,
         ask=C(5, 'The total cost for tiling the floor can be found', 'The total cost is: 450.0'),
         rows=[crit(CORRECT, 10, [3, 5, 8], note=S(21, '(v) 10 marks (C-10 scale)', 'Any other reasonable attempt.'))]),
    dict(key=(16, 'a', 'vi'), topic='cs-2-2', qfigure='q16a-vi', figure='s-q16a', total=10,
         replaces='batch 1b: filed as section B with "10 marks Correct response" as its row; now '
                  'section C, the C-10 scale, the condition table beside the question and the '
                  'scheme\'s lines 21-27',
         why='040 p6: the discount messages from the printed table; the scheme marks lines '
             '21-27 # (vi), C-10 scale',
         stem=Q16A_STEM,
         ask=[C(6, 'If the total cost is greater than 1000', 'based on the following table:'),
              C(6, 'When the program is run the output may now look as follows:', 'You are not entitled to a 10% discount')],
         rows=[crit(CORRECT, 10, [3, 5, 8], note=S(21, '(vi) 10 marks (C-10 scale)', 'Any other reasonable attempt.'))]),
    dict(key=(16, 'b', None), topic='cs-2-2', qfigure='q16b-output', figure='s-q16b', total=20,
         replaces='batch 1b: filed as section B, its ask was "Open the program..." and its row '
                  '"Possible solution:" worth 20; now section C, the tile-cost task, the sample '
                  'output, and the rubric\'s four criteria at 5 / 4 / 3',
         why='040 p7: write the tile cost calculator; the scheme prints a possible solution and a '
             'rubric of four criteria at high / moderate / low, 5 / 4 / 3 each (cells of scheme '
             'p23)',
         ask=C(7, 'Write a Python program that will calculate the total cost of tiles', 'rounded to 2 decimal places.'),
         rows=[crit(T(23, 'User correctly prompted to enter each of the following', 'use of assignment statements'),
                    5, [3, 4], head=T(23, 'Program Inputs'),
                    note=[T(23, 'High level of achievement All of the following', 'correctly and efficiently'),
                          T(23, 'Moderate level of achievement Reasonable attempt', 'each of the following'),
                          T(23, 'Low level of achievement Poor attempt to complete any of the following')]),
               crit(T(23, 'Program loops through correct number of rooms', 'rounded to 2 decimal places'), 5, [3, 4],
                    head=T(23, 'Program Logic (Processing)')),
               crit(T(23, 'Program outputs “Tile Cost Calculator” at the start', 'in the correct format'), 5, [3, 4],
                    head=T(23, 'Program Outputs')),
               crit(T(23, 'Program executes correctly with no syntax or runtime errors', 'Meaningful variable/function names'),
                    5, [3, 4], head=T(23, 'Programming Standards'))]),
]
