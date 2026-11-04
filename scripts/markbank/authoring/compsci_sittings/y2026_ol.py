"""Computer Science 2026 Ordinary Level: every printed ask, 41 of 41.

Paper: Sections A & B booklet (-038-, 20 pages) and Section C booklet (-040-,
12 pages). Scheme: LC219GLP000EV 2026, 28 pages. Every page of both booklets
and scheme pages 3-23 were opened before this module was written.

Section A prices each question at 6 marks and, unlike Higher Level, prints no
split for a question's parts, so the part's own printed price is quoted with
`printed=` ("Correct answer 2 marks", "Each correct item 2 marks (max 4
marks)"). The scheme answers four tables in their other column -- Q4 and Q12
with a tick, Q15(a)(ii) and Q15(b)(i) with a word -- and those are read off
the page: Q4 and Q12 by the tick's x position against the column headers
(page 5: Yes (ML) at x 404-450, No (Not ML) at x 473-537; page 8: Can be
encoded at x 170-263, Cannot be encoded at x 312-411), confirmed on the
rendered page; Q15 from the table cells (cells block p16, p17), confirmed on
the rendered page.
"""
from compsci_lane import (At, C, P, Pair, S, T, anyn, crit, crop, pt,  # noqa: F401
                          stack)

CROPS = {
    'q1-code': stack([('038', 3, (183, 162, 420, 306)), ('038', 3, (126, 341, 467, 499))], ref='2026 OL Q1',
                    alt='The ten-line Python program printed with Question 1 (v = 6, w = 4, '
                        'x = 2, y = 4, z = 5, then a = v + 2, b = w - 1, c = x * y, d = y / 2 '
                        'and e = z % 2), above the table whose Column A lists the variables a, '
                        'b, c, d and e and whose Column B (Value) is blank.'),
    'q5-fig1': crop('038', 5, (185, 93, 410, 266), ref='2026 OL Q5',
                    alt='Figure 1: a box labelled Information System holding a System Core '
                        'joined by a double arrow to Data Storage below it, and by arrows to '
                        'three users outside the box labelled Admin, Manager and Reader, each '
                        'beside a computer screen.'),
    'q7-passes': crop('038', 6, (85, 120, 485, 362), ref='2026 OL Q7',
                      alt='The list 43, 22, 12, 15, 17, 8, then five rows of six boxes. Pass 1 '
                          'is filled in as 22, 43, 12, 15, 17, 8; Passes 2, 3 and 4 are blank; '
                          'Pass 5 is filled in as 8, 12, 15, 17, 22, 43.'),
    'q9-fig2': crop('038', 7, (140, 68, 455, 270), ref='2026 OL Q9',
                    alt='Figure 2: the Von Neumann architecture. An Input Device box points '
                        'into a Central Processing Unit holding a Control Unit and an '
                        'Arithmetic/Logic Unit, which points out to an Output Device box; '
                        'arrows run both ways between the processing unit and a Memory Unit '
                        'below it.'),
    'q11-code': crop('038', 8, (144, 138, 476, 228), ref='2026 OL Q11',
                     alt='The six-line Python program printed with Question 11: line 1 num1 = '
                         'input("Enter a number: "), line 2 num2 = input("Enter another '
                         'number: ", line 3 blank, line 4 total = num1 + num2, line 5 blank, '
                         'line 6 print("The total is: " total).'),
    'q12-table': crop('038', 8, (80, 505, 420, 690), ref='2026 OL Q12',
                      alt='The table printed with Question 12: the characters e, R, a smiling '
                          'face emoji, ?, 4 and a tick mark, each with an empty box under Can '
                          'be encoded and another under Cannot be encoded.'),
    'q13-code': crop('038', 9, (52, 185, 550, 384), ref='2026 OL Q13(a)',
                     alt='The fourteen-line linear search program printed with Question 13(a): '
                         'a list fruits of Apple, Cherry, Banana, Orange, Grape and Plum; target '
                         'read from the user and converted with lower(); position = 0, found = '
                         'False and steps = 0; a while loop that runs while not found and '
                         'position < len(fruits), adding 1 to steps and comparing '
                         'fruits[position].lower() with target, setting found = True and '
                         'position = len(fruits) on a match and otherwise adding 1 to position; '
                         'then, if found, print(target, "found after", steps, "steps.").'),
    'q13a-i': stack([('038', 9, (52, 185, 550, 384)), ('038', 9, (132, 419, 473, 552))],
                    ref='2026 OL Q13(a)(i)',
                    alt='The fourteen-line linear search program printed with Question 13(a), '
                        'above the table whose Column A lists the variables fruits, target, '
                        'position and found and whose Column B (Datatype) is blank.'),
    'q13b-list': crop('038', 10, (54, 82, 542, 114), ref='2026 OL Q13(b)',
                      alt='A row of seven boxes holding the counties Carlow, Dublin, Galway, '
                          'Limerick, Monaghan, Roscommon and Waterford, in alphabetical order.'),
    'q15a-ii': crop('038', 15, (68, 455, 528, 636), ref='2026 OL Q15(a)(ii)',
                    alt='The table printed with Question 15(a)(ii): Column A (Hardware) lists a '
                        'power button on a dishwasher, a microphone receiving sound, a '
                        'temperature sensor, a security switch to detect if a door is open or '
                        'closed, an outdoor motion detection light and a street light that turns '
                        'on based on darkness levels; Column B (Digital or Analogue) is blank.'),
    'q15b-code': crop('038', 16, (52, 97, 550, 336), ref='2026 OL Q15(b)',
                      alt='The seventeen-line pseudocode printed with Question 15(b): LOOP '
                          'FOREVER, READ temperature, READ humidity; IF temperature < 5 AND '
                          'humidity > 70 THEN dehumidifier ON, cooler OFF, alarm ON; ELSE IF '
                          'temperature between 5 and 15 AND humidity between 40 and 70 THEN '
                          'dehumidifier OFF, cooler OFF, alarm OFF; ELSE dehumidifier OFF, '
                          'cooler ON, alarm ON; END IF; END LOOP.'),
    'q15b-i': stack([('038', 16, (52, 97, 550, 336)), ('038', 16, (53, 382, 550, 556))],
                    ref='2026 OL Q15(b)(i)',
                    alt='The seventeen-line pseudocode printed with Question 15(b), above the '
                        'table whose Column A lists three conditions (temperature 12°C with '
                        'humidity 55%, temperature 3°C with humidity 80%, temperature 18°C with '
                        'humidity 30%) and whose Column B has blank Dehumidifier, Cooler and '
                        'Alarm lines for each.'),
    'q15c-table': crop('038', 17, (78, 82, 517, 189), ref='2026 OL Q15(c)',
                       alt='The table printed with Question 15(c): readings at 09:00, 10:00, '
                           '11:00, 12:00 and 13:00 with columns Temperature (°C), Humidity (%), '
                           'Dehumidifier State, Cooler State and Alarm State. The 11:00 '
                           'temperature is a dash and the 12:00 humidity reads Error; the '
                           'dehumidifier is OFF and the cooler and alarm ON throughout.'),
    'q16a-code': crop('040', 4, (78, 418, 542, 538), ref='2026 OL Q16(a)',
                      alt='The eight-line program Question16_A.py as printed in the Section C '
                          'booklet: two comment lines, print("Score"), then team_a_goals = 3, '
                          'team_a_points = 5 and team_a_total = 0.'),
    'q16b-output': crop('040', 7, (104, 369, 548, 583), ref='2026 OL Q16(b)',
                        alt='The sample output printed for Question 16(b): Team Data App; Enter '
                            'team name: Rovers; five results W, W, D, W and L; then *** Rovers - '
                            'results *** with Win: 3, Loss: 1 and Draw: 1.'),
    # The scheme's answers that are tables of ticks, a diagram or a program.
    's-q4': crop('scheme', 5, (55, 55, 555, 325), ref='2026 OL Q4', solution=True,
                 alt='The marking scheme\'s table for Question 4: ticks under Yes (ML) for the '
                     'spam filter, the voice assistant and the photo app, and under No (Not ML) '
                     'for the programmer sorting numbers, the calculator and the traffic '
                     'lights.'),
    's-q12': crop('scheme', 8, (80, 357, 420, 545), ref='2026 OL Q12', solution=True,
                  alt='The marking scheme\'s table for Question 12: ticks under Can be encoded '
                      'for e, R, ? and 4, and under Cannot be encoded for the smiling face emoji '
                      'and the tick mark.'),
    's-q13b-i': crop('scheme', 10, (52, 98, 525, 338), ref='2026 OL Q13(b)(i)', solution=True,
                     alt='The marking scheme\'s answer to Question 13(b)(i): REPEAT, SELECT the '
                         'middle element, COMPARE it with "Galway", STOP if they are equal, '
                         'discard all items above it if it is greater and all items below it if '
                         'it is less; then a diagram of the seven counties indexed 0 to 6 with '
                         'arcs marking step 1 at Limerick (3), step 2 at Dublin (1) and step 3 '
                         'at Galway (2).'),
    's-q16a': crop('scheme', 19, (52, 156, 543, 444), ref='2026 OL Q16(a)', solution=True,
                   alt='The marking scheme\'s possible solution to Question 16(a), lines 1 to '
                       '25: print("GAA Scoreboard Calculator") marked (i); Team A\'s goals and '
                       'points read with int(input()) marked (iii); team_a_total = '
                       'team_a_goals * 3 + team_a_points and its print marked (ii); the same '
                       'for Team B, marked (iv); then an if, elif and else that prints which '
                       'team wins with the winning margin (the difference of the totals), or '
                       'that it was a draw.'),
    's-q16b': crop('scheme', 22, (52, 100, 563, 516), ref='2026 OL Q16(b)', solution=True,
                   alt='The marking scheme\'s possible solution to Question 16(b), lines 1 to '
                       '33: print "Team Data App", read the team name, set wins, losses and '
                       'draws to 0, then a for loop over range(5) reading each result and '
                       'adding 1 to wins, losses or draws for W, L or D; finally print the '
                       'team name between asterisks and the three counts.'),
}

SEC_A = S(4, 'Section A Short Answer Questions 54 marks')
NOTE_Q5A = S(5, 'Good explanation – clear understanding demonstrated 3 marks',
             'Fair explanation – limited understanding 2 marks')
NOTE_Q5B = S(5, 'Good response – clear understanding demonstrated 3 marks',
             'Fair response – limited understanding 2 marks')
NOTE_Q14A = S(12, 'For each valid answer:', 'limited understanding 2 marks')
NOTE_Q14C = S(15, 'For each valid argument:', 'limited understanding 5 marks')
CORRECT = S(19, 'Correct implementation using solution above or similar.')
Q16A_STEM = C(4, 'In GAA sports, players can score goals and points.', 'work out which team is the winner.')
Q15_STEM = P(15, 'An embedded system is a computer system built into another device', 'and fitness trackers.')

CARDS = [
    # ── Section A ─────────────────────────────────────────────────────────
    dict(key=(1, None, None), topic='cs-2-2', qfigure='q1-code', total=6,
         why='p3: the final value of five variables; the scheme prints them, the first '
             'correct 2 and each further one 1',
         ask=[P(3, 'The Python code below includes', 'arithmetic operations.'),
              P(3, 'For each variable in Column A', 'after the program runs.')],
         rows=[anyn([S(4, 'a 8'), S(4, 'b 3'), S(4, 'c 8'), S(4, 'd 2 or 2.0'), S(4, 'e 1')],
                    5, 2, steps=[2, 1, 1, 1, 1], head=S(4, 'Column A Column B Variable Output'),
                    note=S(4, 'First correct response 2 marks', 'Each subsequent correct response 1 mark'))]),
    dict(key=(2, None, None), topic='cs-2-3', total=6,
         why='p3: convert 1110 to decimal; the scheme prints 14 at 6, half right 4, some merit 2',
         ask=P(3, 'Convert the 4-bit binary number below to a decimal number. 1110'),
         rows=[crit(S(4, '14'), 6, [2, 4],
                    note=S(4, 'Correct answer 6 marks', 'Response with some merit 2 marks'))]),
    dict(key=(3, 'a', None), topic='cs-1-3', total=2, printed=S(4, 'Correct answer 2 marks'),
         why='p4: who the end users are; the scheme prints two, 2 marks',
         stem=P(4, 'A group of secondary school students', 'maths multiplication game.'),
         ask=P(4, 'One of the requirements is that the game', 'end users in this scenario?'),
         rows=[anyn([S(4, 'Primary school children'), S(4, 'Teachers')], 1, 2,
                    head=P(4, 'Who are the end users in this scenario?'))]),
    dict(key=(3, 'b', None), topic='cs-1-3', total=4,
         printed=S(4, 'Each correct item 2 marks (max 4 marks)'),
         why='p4: two evaluation-stage tasks; the scheme prints two and any similar, 2 each',
         stem=P(4, 'A group of secondary school students', 'maths multiplication game.'),
         ask=P(4, 'The group are following a software development process.', 'during the evaluation stage.'),
         rows=[anyn([S(4, 'Test the software for errors', '(debugging/user acceptance testing etc)'),
                     S(4, 'Check the program meets the original requirements'),
                     S(4, 'Any similar acceptable task')], 2, 2, open_list=True,
                    head=P(4, 'List two tasks that the group should undertake during the evaluation stage.'))]),
    dict(key=(4, None, None), topic='cs-1-2', figure='s-q4', total=6,
         why='p4: six scenarios, machine learning or not; the scheme ticks each, 1 mark',
         ask=P(4, 'Machine learning (ML) is the development of computer systems', 'no matter how many cars are waiting.'),
         rows=[pt(Pair(P(4, 'A spam filter gets better', 'mark messages as spam.'), S(5, 'Yes (ML)')), 1,
                  note=S(5, 'Each correct answer 1 mark')),
               pt(Pair(P(4, 'A programmer writes code to sort numbers into order.'), S(5, 'No (Not ML)')), 1),
               pt(Pair(P(4, 'A calculator uses a formula', 'square root of a number.'), S(5, 'No (Not ML)')), 1),
               pt(Pair(P(4, 'A voice assistant (like Siri or Alexa)', 'your accent over time.'), S(5, 'Yes (ML)')), 1),
               pt(Pair(P(4, 'A photo app groups pictures', 'by recognising faces.'), S(5, 'Yes (ML)')), 1),
               pt(Pair(P(4, 'Traffic lights are programmed', 'how many cars are waiting.'), S(5, 'No (Not ML)')), 1)]),
    dict(key=(5, 'a', None), topic='cs-2-1', qfigure='q5-fig1', total=3, printed=NOTE_Q5A,
         why='p5: why Figure 1 is an abstract model; the scheme lists reasons, 3 / 2',
         stem=P(5, 'Figure 1 below is an abstract model of an information system.'),
         ask=P(5, 'Explain why this diagram is considered an abstract model.'),
         rows=[anyn([S(5, 'It shows only the main parts of the system.'), S(5, 'It leaves out unnecessary details.'),
                     S(5, 'It uses a diagram instead of showing the real system.'),
                     S(5, 'It focuses on how parts link together, not how they are built.'),
                     S(5, 'Any other valid response')], 1, 3, open_list=True,
                    head=P(5, 'Explain why this diagram is considered an abstract model.'), note=NOTE_Q5A)]),
    dict(key=(5, 'b', None), topic='cs-2-1', qfigure='q5-fig1', total=3, printed=NOTE_Q5B,
         why='p5: one advantage of an abstract model; the scheme lists advantages, 3 / 2',
         stem=P(5, 'Figure 1 below is an abstract model of an information system.'),
         ask=P(5, 'Outline one advantage of using an abstract model', 'an information system.'),
         rows=[anyn([S(5, 'It makes the system easier to understand.'),
                     S(5, 'It helps designers focus on important parts only.'),
                     S(5, 'It reduces complexity by leaving out details.'), S(5, 'It makes planning the system easier.'),
                     S(5, 'It helps explain the system to others.'), S(5, 'Any other valid advantage')],
                    1, 3, open_list=True, note=NOTE_Q5B,
                    head=P(5, 'Outline one advantage of using an abstract model', 'an information system.'))]),
    dict(key=(6, None, None), topic='cs-3-3', total=6,
         why='p5: two reasons for computer modelling; the scheme lists three, each 3 / 2',
         ask=P(5, 'Computer modelling is often used in areas such as weather', 'in these situations.'),
         rows=[anyn([S(6, 'Computer modelling is safer because', 'severe weather conditions.'),
                     S(6, 'It is cheaper as simulations can be run', 'building full prototypes.'),
                     S(6, 'It is faster as the process and be sped up and repeated instantly.'),
                     S(6, 'Any other valid reason')], 2, 3, open_list=True,
                    head=P(5, 'Outline two reasons why computer modelling is used', 'in these situations.'),
                    note=S(6, 'For each valid reason:', 'Fair – limited understanding 2 marks'))]),
    dict(key=(7, None, None), topic='cs-2-2', qfigure='q7-passes', total=6,
         why='p6: passes 2 to 4 of an insertion sort; the scheme prints each row, 2 marks',
         ask=P(6, 'The insertion sort algorithm is applied', 'correct number in each box.'),
         rows=[pt(S(6, 'Pass 2 12 22 43 15 17 8'), 2), pt(S(6, 'Pass 3 12 15 22 43 17 8'), 2),
               pt(S(6, 'Pass 4 12 15 17 22 43 8'), 2)]),
    dict(key=(8, None, None), topic='cs-1-2', total=6,
         why='p6: one argument for and one against phones ruining relationships; the scheme '
             'lists both, each 3 / 2',
         stem=P(6, '“We sit together in the same room', 'Kate Middleton, Princess of Wales'),
         ask=P(6, 'Considering the quote above', 'society and relationships.'),
         rows=[anyn([S(6, 'Reduce face-to-face communication'), S(6, 'Cause people to ignore those physically present'),
                     S(6, 'Increase distraction and lack of attention'), S(6, 'Lower quality of conversations'),
                     S(6, 'Encourage addiction and constant checking'), S(6, 'Any valid argument for')],
                    1, 3, head=S(6, 'Arguments for:'), open_list=True,
                    note=S(6, 'For each valid argument:', 'Fair – limited understanding 2 marks')),
               anyn([S(6, 'Allow people to stay in touch easily'), S(6, 'Help maintain long-distance relationships'),
                     S(6, 'Enable instant communication in emergencies'),
                     S(6, 'Support social connections through messaging and video calls'),
                     S(6, 'Help people feel less lonely'), S(6, 'Allow families and friends to share experiences'),
                     S(6, 'Any valid argument against')],
                    1, 3, head=S(6, 'Arguments against:'), open_list=True,
                    note=S(6, 'For each valid argument:', 'Fair – limited understanding 2 marks'))]),
    dict(key=(9, None, None), topic='cs-2-3', qfigure='q9-fig2', total=6,
         why='p7: two input and two output devices; the scheme lists both, first 2 and second 1',
         ask=P(7, 'Figure 2 above shows the Von Neumann Architecture Model.', 'commonly found in this model.'),
         rows=[anyn([S(7, 'Keyboard'), S(7, 'Mouse'), S(7, 'Microphone'), S(7, 'Scanner'), S(7, 'Webcam'),
                     S(7, 'Touchscreen'), S(7, 'Any other valid input device')], 2, 2, steps=[2, 1],
                    head=S(7, 'Input devices:'), open_list=True,
                    note=S(7, 'For input/output: First correct 2 marks', 'Second correct 1 mark')),
               anyn([S(7, 'Monitor'), S(7, 'Printer'), S(7, 'Speakers'), S(7, 'Headphones'), S(7, 'Projector'),
                     S(7, 'Any other valid output device')], 2, 2, steps=[2, 1],
                    head=S(7, 'Output devices:'), open_list=True,
                    note=S(7, 'For input/output: First correct 2 marks', 'Second correct 1 mark'))]),
    dict(key=(10, 'a', None), topic='cs-2-4', total=4,
         printed=S(7, 'Each correct example 2 marks (max. 4 marks)'),
         why='p7: one discrete and one continuous example; the scheme lists both, 2 each',
         stem=P(7, 'A fitness watch collects different types of data', 'other data is continuous.'),
         ask=P(7, 'State one example of discrete data and one example of continuous data',
               'a fitness watch might record.'),
         rows=[anyn([S(7, 'Number of steps taken'), S(7, 'number of floors climbed'), S(7, 'number of workouts'),
                     S(7, 'number of calories burned'), S(7, 'number of notifications')], 1, 2,
                    head=S(7, 'Discrete Data Example:'), open_list=True,
                    note=S(7, 'Each correct example 2 marks (max. 4 marks)')),
               anyn([S(7, 'Heart rate'), S(7, 'body temperature'), S(7, 'running speed'),
                     S(7, 'distance travelled'), S(7, 'time duration'), S(7, 'GPS position')], 1, 2,
                    head=S(7, 'Continuous Data Example:'), open_list=True)]),
    dict(key=(10, 'b', None), topic='cs-2-4', total=2, printed=S(7, 'Correct valid example 2 marks'),
         why='p7: one example of data stored in a list; the scheme lists five and any valid, 2',
         stem=P(7, 'A fitness watch collects different types of data', 'other data is continuous.'),
         ask=P(7, 'State one example of data that might be stored in a list on the watch.'),
         rows=[anyn([S(7, 'A list of daily step counts.'), S(7, 'A list of heart rate readings over time.'),
                     S(7, 'A list of distances travelled for each workout.'), S(7, 'A list of calories burned each day.'),
                     S(7, 'A list of recorded temperatures during an activity.'),
                     S(7, 'Any other valid example of a list')], 1, 2, open_list=True,
                    head=P(7, 'State one example of data that might be stored in a list on the watch.'))]),
    dict(key=(11, None, None), topic='cs-2-5', qfigure='q11-code', total=6,
         why='p8: any two of the three errors with line, explanation and fix; the scheme '
             'prints all three, each line, explanation and fix 1 mark',
         ask=P(8, 'The Python code below was written to accept two numbers', 'any two such errors.'),
         rows=[anyn([S(8, 'Line 2 Missing bracket close bracket'),
                     S(8, 'Line 6 No concatenation', 'missing use of +'),
                     S(8, 'Line 4 This concatenates 2 strings', 'part of addition expression).')],
                    2, 3, head=S(8, 'Syntax errors:'),
                    note=S(8, 'Each correct line identified 1 mark', 'Each correct solution to fix 1 mark'))]),
    dict(key=(12, None, None), topic='cs-2-4', qfigure='q12-table', figure='s-q12', total=6,
         why='p8: six characters, ASCII-encodable or not; the scheme ticks each, 1 mark',
         ask=P(8, 'ASCII stands for American Standard Code', 'encoded using 7-bit ASCII.'),
         rows=[pt(Pair(At('038', 8, (100, 529, 140, 549)), S(8, 'Can be encoded')), 1,
                  note=S(8, 'Each correct item 1 mark')),
               pt(Pair(At('038', 8, (100, 557, 140, 577)), S(8, 'Can be encoded')), 1),
               pt(Pair(At('038', 8, (100, 586, 140, 606)), S(8, 'Cannot be encoded')), 1),
               pt(Pair(At('038', 8, (100, 614, 140, 634)), S(8, 'Can be encoded')), 1),
               pt(Pair(At('038', 8, (100, 641, 140, 661)), S(8, 'Can be encoded')), 1),
               pt(Pair(At('038', 8, (100, 665, 140, 686)), S(8, 'Cannot be encoded')), 1)]),

    # ── Section B: Question 13, linear and binary search ──────────────────
    dict(key=(13, 'a', 'i'), topic='cs-2-4', qfigure='q13a-i', total=13,
         printed=S(9, '(a) 19 marks (13, 4 ,2)'),
         why='p9: the datatype of four variables; the scheme prints them, 5, 4, 2 and 2',
         stem=[P(9, 'Two common search algorithms are linear search and binary search.'),
               P(9, 'The Python program below shows a linear search algorithm.')],
         ask=P(9, 'In the table below record the datatype in Column B', 'listed in Column A.'),
         rows=[anyn([S(9, 'fruits list'), S(9, 'target string'), S(9, 'position Integer / int'),
                     S(9, 'found Boolean / Bool')], 4, 5, steps=[5, 4, 2, 2],
                    head=S(9, 'Column A Column B Variable Datatype'),
                    note=S(9, 'First correct response 5 marks', 'Fourth correct response 2 marks'))]),
    dict(key=(13, 'a', 'ii'), topic='cs-2-2', qfigure='q13-code', total=4,
         why='p9: the output for "Orange"; the scheme prints it at 4, some merit 3',
         stem=[P(9, 'Two common search algorithms are linear search and binary search.'),
               P(9, 'The Python program below shows a linear search algorithm.')],
         ask=P(9, 'State the output of the program if the user enters', 'a fruit to search for.'),
         rows=[crit(S(9, 'orange found after 4 steps.'), 4, [3],
                    note=S(9, 'Correct answer 4 marks', 'Response of some merit 3 marks'))]),
    dict(key=(13, 'a', 'iii'), topic='cs-2-2', qfigure='q13-code', total=2,
         why='p9: why lower() is used; the scheme answers it, 2 / 1',
         stem=[P(9, 'Two common search algorithms are linear search and binary search.'),
               P(9, 'The Python program below shows a linear search algorithm.')],
         ask=P(9, 'Explain why the programmer has used the lower()function in this program.'),
         rows=[crit(S(9, 'lower() is used to convert the user input', 'comparing lowercase to lowercase.'),
                    2, [1], note=S(9, 'Good explanation - clear understanding demonstrated 2 marks',
                                   'Fair explanation - limited understanding 1 mark'))]),
    dict(key=(13, 'b', 'i'), topic='cs-2-2', qfigure='q13b-list', figure='s-q13b-i', total=3,
         why='p10: the steps of a binary search for "Galway"; the scheme prints them and a '
             'diagram, 3 / 2 / 1',
         stem=P(10, 'Several Irish counties have been stored into a list.', 'This list is displayed below.'),
         ask=P(10, 'In the space below, explain the steps', 'using diagrams or in writing.'),
         rows=[crit(S(10, 'REPEAT SELECT the middle element', 'DISCARD all items below middle element'),
                    3, [1, 2], note=S(10, 'Correct answer 3 marks', 'Response with some merit 1 marks'))]),
    dict(key=(13, 'b', 'ii'), topic='cs-2-2', total=4,
         why='p11: two differences between linear and binary search; the scheme prints four '
             'paired statements, each difference 2 / 1',
         stem=P(10, 'Several Irish counties have been stored into a list.', 'This list is displayed below.'),
         ask=P(11, 'Outline two differences between the linear search and binary search algorithms.'),
         rows=[anyn([S(10, 'Linear search works on unsorted data.', 'requires the data to be sorted.'),
                     S(10, 'Linear search checks each item one by one.', 'halves the list each time.'),
                     S(10, 'Linear search is slower for large lists.', 'is faster for large lists.'),
                     S(10, 'Linear search may check every item.', 'checks far fewer items.')], 2, 2,
                    head=P(11, 'Outline two differences between the linear search and binary search algorithms.'),
                    note=S(10, 'For each difference:', 'limited understanding 1 marks'))]),
    dict(key=(13, 'c', None), topic='cs-1-2', total=12,
         why='p11: one example of companies using sorting and one of searching; the scheme '
             'lists both, each 6 / 5',
         ask=P(11, 'We are surrounded by sorting and searching algorithms', 'how they use searching algorithms.'),
         rows=[anyn([S(11, 'Amazon sorts items by delivery speed', '(“Prime First”).'),
                     S(11, 'Netflix sorts content into categories', '“Trending Now”).'),
                     S(11, 'eBay sorts auctions by ending soonest or lowest price.'),
                     S(11, 'Booking.com sorts hotels by rating or cheapest first.'),
                     S(11, 'Accept other relevant answers.', nth=1)], 1, 6,
                    head=S(11, 'Sorting Algorithms:'), open_list=True,
                    note=S(11, 'For each algorithm:', 'lacks clarity 5 mark')),
               anyn([S(11, 'Netflix uses searching so users', 'title, actor, or genre.'),
                     S(11, 'Spotify uses searching to find songs', 'playlists instantly.'),
                     S(11, 'Google Maps uses searching to find locations or businesses.'),
                     S(11, 'Accept other relevant answers.', nth=2)], 1, 6,
                    head=S(11, 'Searching Algorithms:'), open_list=True,
                    note=S(11, 'For each algorithm:', 'lacks clarity 5 mark'))]),

    # ── Question 14, electronic voting ────────────────────────────────────
    dict(key=(14, 'a', 'i'), topic='cs-1-1', total=6,
         why='p12: one benefit and one cost of electronic voting; the scheme lists both, each '
             '3 / 2',
         stem=[P(12, 'The Irish Presidential Election was held', 'at a large cost to the state.'),
               P(12, 'Over the past few decades technology has been used to automate many manual processes.')],
         ask=P(12, 'In relation to electronic voting machines, explain one potential benefit', 'this automated process.'),
         rows=[anyn([S(12, 'Faster vote counting', 'counting paper ballots.'),
                     S(12, 'Reduced human error', 'manual counting.'),
                     S(12, 'More efficient elections', 'count votes.'),
                     S(12, 'Accessibility – can be designed', 'with disabilities.'),
                     S(12, 'Less paper used', 'environmentally friendly.'),
                     S(12, 'Immediate results', 'election outcomes.'),
                     S(12, 'Any other valid benefit.')], 1, 3, head=S(12, 'Possible benefits:'),
                    open_list=True, note=NOTE_Q14A),
               anyn([S(12, 'High financial cost', 'update machines.'),
                     S(12, 'Security risks', 'software faults.'),
                     S(12, 'Technical failures', 'on election day.'),
                     S(12, 'Lack of public trust', 'as paper ballots.'),
                     S(12, 'Training required', 'manage the machines.'),
                     S(12, 'Any other valid cost.')], 1, 3, head=S(12, 'Possible costs:'),
                    open_list=True, note=NOTE_Q14A)]),
    dict(key=(14, 'a', 'ii'), topic='cs-1-3', total=4,
         why='p12: two stakeholders, each with a requirement; the scheme lists four, each '
             'stakeholder 1 and requirement 1',
         stem=[P(12, 'The Irish Presidential Election was held', 'at a large cost to the state.'),
               P(12, 'Over the past few decades technology has been used to automate many manual processes.')],
         ask=P(12, 'Stakeholder engagement is vitally important', 'one requirement from the system.'),
         rows=[anyn([S(12, 'Voters – machines are easy to use', 'trustworthy/ confidential'),
                     S(12, 'Government – machines are secure', 'affordable'),
                     S(12, 'Polling Staff – machines are easy to set up', 'count accurately'),
                     S(12, 'Political Parties – machines are fair', 'can’t be hacked or tampered')], 2, 2,
                    head=P(12, 'Identify two stakeholders that could have been consulted', 'electronic voting machines.'),
                    note=S(12, 'Each stakeholder identified 1 mark', 'Each valid requirement explained 1 mark'))]),
    dict(key=(14, 'b', 'i'), topic='cs-1-2', total=4,
         why='p13: two Universal Design principles applied to the machines; the scheme '
             'describes all seven, each principle 1 and description 1',
         stem=[P(12, 'The Irish Presidential Election was held', 'at a large cost to the state.'),
               P(13, 'The Principles of Universal Design are important', 'independence for everyone.')],
         ask=P(13, 'Name two of the principles', 'electronic voting machines.'),
         rows=[anyn([S(13, 'Equitable Use - The design is useful', 'adjustable in height for wheelchair users.'),
                     S(13, 'Flexibility in Use -', 'voice control, etc.'),
                     S(13, 'Simple and Intuitive Use -', 'to vote without confusion.'),
                     S(13, 'Perceptible Information -', 'or visual cues.'),
                     S(13, 'Tolerance for Error -', 'before final submission.'),
                     S(13, 'Low Physical Effort -', 'rather than buttons'),
                     S(13, 'Size and Space for Approach and Use -', 'operate it without obstruction.')], 2, 2,
                    head=P(13, 'Name two of the principles', 'electronic voting machines.'),
                    note=S(13, 'For each response:', 'understanding demonstrated 1 mark'))]),
    dict(key=(14, 'b', 'ii'), topic='cs-1-2', total=4,
         why='p13: two accessibility features for a voting app; the scheme lists eight and any '
             'valid, each 2 / 1',
         stem=[P(12, 'The Irish Presidential Election was held', 'at a large cost to the state.'),
               P(13, 'The Principles of Universal Design are important', 'independence for everyone.')],
         ask=P(13, 'As well as voting machines it might be possible', 'could be built into the app.'),
         rows=[anyn([S(14, 'Screen reader / text-to-speech support', 'visually impaired users.'),
                     S(14, 'Adjustable text size', 'easier reading.'),
                     S(14, 'High-contrast mode', 'colour blindness.'),
                     S(14, 'Voice control', 'instead of touch.'),
                     S(14, 'Simple, uncluttered interface', 'confusion and mistakes.'),
                     S(14, 'Audio instructions', 'struggle with reading.'),
                     S(14, 'Confirmation and review screen', 'before submitting.'),
                     S(14, 'Multiple language options', 'is not English.'),
                     S(14, 'Any other valid answer.')], 2, 2, open_list=True,
                    head=P(13, 'Describe two accessibility features that could be built into the app.'),
                    note=S(14, 'For each accessibility feature:', 'limited understanding 1 mark'))]),
    dict(key=(14, 'b', 'iii'), topic='cs-1-2', total=4,
         why='p13: one ethical concern with a voting app; the scheme lists four, 4 / 3',
         stem=[P(12, 'The Irish Presidential Election was held', 'at a large cost to the state.'),
               P(13, 'The Principles of Universal Design are important', 'independence for everyone.')],
         ask=P(13, 'Outline one ethical concern with regards to developing an app for voting.'),
         rows=[anyn([S(14, 'Security and privacy of voter data', 'manipulation of results.'),
                     S(14, 'Accessibility and fairness', 'exclude certain groups.'),
                     S(14, 'Integrity of the election', 'the democratic process.'),
                     S(14, 'Proof of identity', 'cast their vote.')], 1, 4,
                    head=P(13, 'Outline one ethical concern with regards to developing an app for voting.'),
                    note=S(14, 'Good explanation – clear understanding demonstrated 4 marks',
                           'Fair explanation – limited understanding 3 marks'))]),
    dict(key=(14, 'c', 'i'), topic='cs-1-2', total=4, printed=S(15, '(c) 16 (4, 12) marks (i) 4 marks'),
         why='p14: how social media algorithms shape political content; the scheme lists four '
             'and any valid, 4 / 3',
         stem=[P(12, 'The Irish Presidential Election was held', 'at a large cost to the state.'),
               P(14, 'Social media played an important role', 'presidential elections.')],
         ask=P(14, 'Describe one way social media algorithms might influence', 'a voter sees.'),
         rows=[anyn([S(15, 'Algorithms prioritise content the user has interacted with before.'),
                     S(15, 'Algorithms push content that is popular or highly shared.'),
                     S(15, 'Algorithms create a “filter bubble”.'),
                     S(15, 'Algorithms use personal data to target political ads.'),
                     S(15, 'Any other valid answer.')], 1, 4, open_list=True,
                    head=P(14, 'Describe one way social media algorithms might influence', 'a voter sees.'),
                    note=S(15, 'Good description – clear understanding demonstrated 4 marks',
                           'Fair description – limited understanding 3 marks'))]),
    dict(key=(14, 'c', 'ii'), topic='cs-1-2', total=12,
         why='p14: one argument for and one against an under-16 social media ban; the scheme '
             'lists both, each 6 / 5',
         stem=[P(12, 'The Irish Presidential Election was held', 'at a large cost to the state.'),
               P(14, 'Social media played an important role', 'presidential elections.')],
         ask=P(14, 'Social media has recently been banned in Australia', 'one argument against this policy.'),
         rows=[anyn([S(15, 'Protects mental health -', 'likes, followers, and comparisons.'),
                     S(15, 'Reduces cyberbullying -', 'online harassment and abuse.'),
                     S(15, 'Protects children from harmful content -', 'or online predators.'),
                     S(15, 'Improves focus and education -', 'better concentration.'),
                     S(15, 'Encourages healthier lifestyles -', 'and physical activity.'),
                     S(15, 'Increased social skills -', 'with people in person.'),
                     S(15, 'Any other valid argument for.')], 1, 6, head=S(15, 'Arguments For:'),
                    open_list=True, note=NOTE_Q14C),
               anyn([S(15, 'Limits freedom of expression -', 'express themselves is restricted.'),
                     S(15, 'Difficult to enforce -', 'someone else’s account.'),
                     S(15, 'Social exclusion -', 'and they cannot.'),
                     S(15, 'Loss of positive uses -', 'friends and family.'),
                     S(15, 'Better regulation instead of bans -', 'than a full ban.'),
                     S(15, 'Any other valid argument against.')], 1, 6, head=S(15, 'Arguments Against:'),
                    open_list=True, note=NOTE_Q14C)]),

    # ── Question 15, embedded systems ─────────────────────────────────────
    dict(key=(15, 'a', 'i'), topic='cs-3-4', total=10, printed=S(16, '(a) 19 (10, 9) marks (i) 10 (4, 4, 2) marks'),
         why='p15: three advantages of embedded systems; the scheme lists seven and any valid, '
             '4, 4 and 2',
         stem=[Q15_STEM, P(15, 'Embedded systems are different to the general-purpose laptops', 'on a daily basis.')],
         ask=P(15, 'State three advantages of embedded systems over general-purpose computers.'),
         rows=[anyn([S(16, 'Embedded systems do one specific task', 'can do many tasks.'),
                     S(16, 'Embedded systems run one fixed program', 'install lots of software.'),
                     S(16, 'Embedded systems use limited hardware', 'and lots of RAM.'),
                     S(16, 'Embedded systems often have little or no user interface', 'and operating systems.'),
                     S(16, 'Embedded systems are built into another device', 'as standalone machines.'),
                     S(16, 'Embedded systems must respond in real time', 'strict timing.'),
                     S(16, 'Embedded systems are usually cheaper and smaller', 'larger and more expensive.'),
                     S(16, 'Any other valid advantage.')], 3, 4, steps=[4, 4, 2], open_list=True,
                    head=P(15, 'State three advantages of embedded systems over general-purpose computers.'),
                    note=S(16, 'First correct response 4 marks', 'Third correct response 2 marks'))]),
    dict(key=(15, 'a', 'ii'), topic='cs-2-3', qfigure='q15a-ii', total=9,
         printed=S(16, '(ii) 9 marks'),
         why='p15: digital or analogue for six hardware items; the scheme answers each in its '
             'Column B, the first three correct 2 each and the others 1',
         stem=[Q15_STEM, P(15, 'Embedded systems are different to the general-purpose laptops', 'on a daily basis.')],
         ask=P(15, 'Embedded systems can take in both digital and analogue inputs.', 'a digital input or an analogue input.'),
         rows=[anyn([Pair(T(16, 'Power button on a dishwasher'), T(16, 'Digital', nth=1)),
                     Pair(T(16, 'A microphone receiving sound'), T(16, 'Analogue', nth=1)),
                     Pair(T(16, 'A temperature sensor'), T(16, 'Analogue', nth=1)),
                     Pair(T(16, 'A security switch to detect if a door is open or closed'), T(16, 'Digital', nth=1)),
                     Pair(T(16, 'An outdoor motion detection light'), T(16, 'Digital', nth=1)),
                     Pair(T(16, 'A street light that turns on based on darkness levels'), T(16, 'Analogue', nth=1))],
                    6, 2, steps=[2, 2, 2, 1, 1, 1], head=T(16, 'Column B Digital or Analogue'),
                    note=S(16, 'First three correct answers 2 marks each', 'mark each (max. 3)'))]),
    dict(key=(15, 'b', 'i'), topic='cs-3-4', qfigure='q15b-i', total=9,
         printed=S(17, '(b) 13 marks (9, 4) (i) 9 marks'),
         why='p16: the state of three devices under three conditions; the scheme prints each, '
             'one mark per correct state',
         stem=[Q15_STEM, P(16, 'An embedded system is being set up for a laboratory', 'The pseudocode for the system is shown below.')],
         ask=P(16, 'In the table below, use Column B to state the status', 'conditions in Column A.'),
         rows=[crit(Pair(T(17, 'Temperature = 12°C, Humidity = 55%'), T(17, 'Dehumidifier: OFF Cooler: OFF Alarm: OFF')),
                    3, [1, 2], note=S(17, 'Each correct ON / OFF state 1 mark')),
               crit(Pair(T(17, 'Temperature = 3°C, Humidity = 80%'), T(17, 'Dehumidifier: ON Cooler: OFF Alarm: ON')),
                    3, [1, 2]),
               crit(Pair(T(17, 'Temperature = 18°C, Humidity = 30%'), T(17, 'Dehumidifier: OFF Cooler: ON Alarm: ON')),
                    3, [1, 2])]),
    dict(key=(15, 'b', 'ii'), topic='cs-3-4', qfigure='q15b-code', total=4,
         printed=S(17, '(ii) 4 marks'),
         why='p16: two input and two output devices of the system; the scheme lists both, 1 '
             'mark each',
         stem=[Q15_STEM, P(16, 'An embedded system is being set up for a laboratory', 'The pseudocode for the system is shown below.')],
         ask=P(16, 'Identify two input devices and two output devices used by this embedded system.'),
         rows=[anyn([S(17, 'Temperature sensor / thermometer'), S(17, 'Humidity sensor')], 2, 1,
                    head=S(17, 'Inputs:'), note=S(17, 'Each correct device identified 1 mark')),
               anyn([S(17, 'Dehumidifier', nth=4), S(17, 'Cooler', nth=4), S(17, 'Alarm', nth=4)], 2, 1,
                    head=S(17, 'Outputs:'))]),
    dict(key=(15, 'c', 'i'), topic='cs-3-2', qfigure='q15c-table', total=4,
         why='p17: two problems a missing or erroneous reading causes; the scheme lists five and '
             'any valid, each 2 / 1',
         stem=[Q15_STEM, P(17, 'The data from the embedded system is collected in a table and presented below.')],
         ask=P(17, 'The temperature reading at 11:00 is missing', 'could cause for the laboratory.'),
         rows=[anyn([S(18, 'Incorrect system decisions', 'at the correct time.'),
                     S(18, 'System acting unnecessarily', 'when it is not needed.'),
                     S(18, 'Increased energy', 'wasting electricity.'),
                     S(18, 'Reduced reliability of the system', 'the monitoring system.'),
                     S(18, 'Delayed fault detection', 'missing or incorrect.'),
                     S(18, 'Any other valid problem.')], 2, 2, open_list=True,
                    head=P(17, 'Describe two problems that issues like these could cause for the laboratory.'),
                    note=S(18, 'For each valid answer:', 'limited understanding 1 mark'))]),
    dict(key=(15, 'c', 'ii'), topic='cs-3-2', qfigure='q15c-table', total=2,
         why='p17: one way to handle the bad readings; the scheme lists four and any valid, 2 / 1',
         stem=[Q15_STEM, P(17, 'The data from the embedded system is collected in a table and presented below.')],
         ask=P(17, 'Suggest one method the system could use', 'stored dataset reliable.'),
         rows=[anyn([S(18, 'Data validation check', 'invalid data like “Error”.'),
                     S(18, 'Automatic re-reading of sensors', 'another reading immediately.'),
                     S(18, 'Use the last valid reading or average reading', 'an average of all values'),
                     S(18, 'Alert the user', 'fixed quickly.'),
                     S(18, 'Any other valid suggestions.')], 1, 2, open_list=True,
                    head=P(17, 'Suggest one method the system could use', 'stored dataset reliable.'),
                    note=S(18, 'Good description – clear understanding demonstrated 2 marks',
                           'Fair description – limited understanding 1 mark', nth=2))]),

    # ── Section C: Question 16 ────────────────────────────────────────────
    dict(key=(16, 'a', 'i'), topic='cs-2-2', qfigure='q16a-code', figure='s-q16a', total=15,
         why='040 p4: print the new title; the scheme marks line 4 #(i), A-15 scale',
         stem=Q16A_STEM,
         ask=C(4, 'Modify the program so that it prints out "GAA Scoreboard Calculator"', 'look as follows: GAA Scoreboard Calculator'),
         rows=[crit(CORRECT, 15, [8], note=S(19, '(i) 15 marks (A-15 scale)', 'Any other reasonable attempt.'))]),
    dict(key=(16, 'a', 'ii'), topic='cs-2-2', qfigure='q16a-code', figure='s-q16a', total=10,
         why='040 p5: calculate and print Team A\'s total; the scheme marks lines 8-9 #(ii), '
             'B-10 scale',
         stem=Q16A_STEM,
         ask=C(5, 'Calculate the team’s total score', 'Team A total score: 14'),
         rows=[crit(CORRECT, 10, [3, 7], note=S(19, '(ii) 10 marks (B-10 scale)', 'Any other reasonable attempt.'))]),
    dict(key=(16, 'a', 'iii'), topic='cs-2-2', qfigure='q16a-code', figure='s-q16a', total=10,
         why='040 p5: read Team A\'s goals and points; the scheme marks lines 6-8 #(iii), C-10 '
             'scale',
         stem=Q16A_STEM,
         ask=C(5, 'Currently, the vales for team_a_goals', 'Team A total score: 13', end_nth=1),
         rows=[crit(CORRECT, 10, [3, 5, 8], note=S(20, '(iii) 10 marks (C-10 scale)', 'Any other reasonable attempt.'))]),
    dict(key=(16, 'a', 'iv'), topic='cs-2-2', qfigure='q16a-code', figure='s-q16a', total=10,
         why='040 p5: read and report Team B\'s score; the scheme marks line 11 #(iv), C-10 scale',
         stem=Q16A_STEM,
         ask=C(5, 'Modify the code, by adding new variables', 'Team B Total Score: 12', end_nth=1),
         rows=[crit(CORRECT, 10, [3, 5, 8], note=S(20, '(iv) 10 marks (C-10 scale)', 'Any other reasonable attempt.'))]),
    dict(key=(16, 'a', 'v'), topic='cs-2-2', qfigure='q16a-code', figure='s-q16a', total=10,
         why='040 p5-6: compare the totals and report the winner or a draw; the scheme\'s '
             'solution lines 16-25, C-10 scale',
         stem=Q16A_STEM,
         ask=[C(5, 'Modify the code so the program compares the total scores', 'Result: Team A wins'),
              C(6, 'Example 2:', 'Result: Draw')],
         rows=[crit(CORRECT, 10, [3, 5, 8], note=S(20, '(v) 10 marks (C-10 scale)', 'Any other reasonable attempt.'))]),
    dict(key=(16, 'a', 'vi'), topic='cs-2-2', qfigure='q16a-code', figure='s-q16a', total=5,
         why='040 p6: report the winning margin; the scheme\'s solution lines 17-23, B-5 scale',
         stem=Q16A_STEM,
         ask=C(6, 'Modify the code so that if the match is not a draw', 'Winning margin: 4'),
         rows=[crit(CORRECT, 5, [2, 3], note=S(21, '(vi) 5 marks (B-5 scale)', 'Any other reasonable attempt.'))]),
    dict(key=(16, 'b', None), topic='cs-2-2', qfigure='q16b-output', figure='s-q16b', total=20,
         why='040 p7: write the team data app; the scheme prints a possible solution and a '
             'rubric of four criteria at 5 / 4 / 3',
         ask=C(7, 'Implement a program that will allow team managers', 'as shown in the sample output below.'),
         rows=[crit(T(23, '• Team name read in correctly', 'and use of assignment statements'), 5, [3, 4],
                    head=T(23, 'Program Inputs'),
                    note=[T(23, 'High level of achievement All of the following', 'correctly and efficiently'),
                          T(23, 'Moderate level of achievement Reasonable attempt', 'each of the following'),
                          T(23, 'Low level of achievement Poor attempt to complete any of the following')]),
               crit(T(23, '• Correct logic to count wins', 'Correct logic to count draws'), 5, [3, 4],
                    head=T(23, 'Processing & Logic')),
               crit(T(23, '• Program displays “Team Data App”', 'wins, losses and draws'), 5, [3, 4],
                    head=T(23, 'Program Output')),
               crit(T(23, '• Program executes correctly', 'Program design is well explained with comments'),
                    5, [3, 4], head=T(23, 'Programming Standards'))]),
]
