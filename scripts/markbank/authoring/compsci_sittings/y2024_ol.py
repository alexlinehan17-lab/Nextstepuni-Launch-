"""Computer Science 2024 Ordinary Level: all 44 printed asks, re-authored part by part.

33 cards shipped in August out of the automatic author; batch 1b rebuilds 32 of
them here, keeping their ids, from lifts of the paper and the scheme, and the 3
residue cards sit among them in printed order. Paper pages 3-19 and Section C
pages 4-6, and scheme pages 3-21 were opened.

The 33rd, cs-2024-ol-q16 (questionRef "2024 OL Q16", 80 marks), was a
whole-question card shipped beside cs-2024-ol-q16-b, so it repeated part (b).
The coordinator's ruling (5 Nov): each printed ask has exactly one card. Q16(a)'s
six parts get cards of their own here, on the Section C scales the scheme
prints for each, and the whole id is withdrawn onto the first of them
(WITHDRAWN; the lane coordinator writes the alias). Q2, Q3 and Q8 stay whole:
no part cards exist for them, and each is one 6-mark card with a row per part.

Shipped crops reused on the question side, each opened and clean: q1-code0,
q3-fig0, q6-fig0, q8-code0, q10-figure, q12-fig0, q13-code0 and q15-fig0.
q16-figure carries the paper's (i)-(iii) prose below the listing, so Q16(a) has
crops of its own. Q16(b)'s rubric is read from the cells of scheme page 21.
"""
from compsci_lane import (C, P, Pair, S, T, anyn, crit, crop, ladder, ofpart, pt, stack)  # noqa: F401

WITHDRAWN = {'cs-2024-ol-q16': 'cs-2024-ol-q16-a-i'}

LISTING16 = ('040', 4, (56, 350, 555, 477))

CROPS = {
    's-q3a': crop('scheme', 4, (57, 567, 506, 714), ref='2024 OL Q3(a)', solution=True,
                  alt='The marking scheme\'s completed table for Question 3(a): beside each '
                      'component image its name, Capacitor, Resistor and Transistor, in that '
                      'order.'),
    'q5-flow': stack([('038', 5, (56, 160, 560, 488)), ('038', 5, (55, 560, 508, 743))],
                     ref='2024 OL Q5',
                     alt='Figure 1: a flowchart. START, price = 20.00, Input age, Input student '
                         '(Yes/No), then a decision Is age < 16?; Yes leads to an empty box B and '
                         'on to an empty box D; No leads to an empty box A, whose Yes branch goes '
                         'through an empty box C to D and whose No branch goes straight to D. '
                         'Below it, the table '
                         'whose Column A lists PRINT(price), Is age < 21 AND student = "yes"?, '
                         'price = price – (20% of price) and price = price – (10% of price), and '
                         'whose Column B (Flowchart Letter) is blank.'),
    's-q6': crop('scheme', 6, (115, 84, 481, 331), ref='2024 OL Q6', solution=True,
                 alt='The marking scheme\'s completed table for Question 6: an AND gate with '
                     'inputs 1 and 1 outputs 1, an OR gate with inputs 1 and 0 outputs 1, and a '
                     'NOT gate with input 1 outputs 0.'),
    'q11-fig2': crop('038', 8, (284, 489, 541, 596), ref='2024 OL Q11',
                     alt='Figure 2: photographs of two single-board computers, a Raspberry Pi '
                         'and a micro:bit.'),
    'q13b-code': crop('038', 13, (143, 85, 452, 158), ref='2024 OL Q13(b)',
                      alt='The five-line linear search pseudo code printed with Question 13(b): for '
                          'each element in the list, if element equal target value then return its '
                          'index, if element is not found then print "Value not found".'),
    'q15d-table': crop('038', 19, (56, 89, 540, 129), ref='2024 OL Q15(d)',
                       alt='The wind warning table printed with Question 15(d): Yellow Wind Warning, '
                           'speed between 90 and 110km/h; Orange Wind Warning, speed between 111 '
                           'and 130km/h; Red Wind Warning, speed greater than 130km/h.'),
    'q16a-code': crop(*LISTING16, ref='2024 OL Q16(a)',
                      alt='The nine-line program Question16_A.py as printed in the Section C '
                          'booklet: two comment lines, print("The program"), age = '
                          'int(input("What age are you? ")), and if (age >= 17): print("You are '
                          'entitled to apply for a driving licence.").'),
    'q16a-vi': stack([LISTING16, ('040', 5, (55, 408, 541, 534))], ref='2024 OL Q16(a)(vi)',
                     alt='The nine-line program Question16_A.py (print("The program"), age read as '
                         'an int, and if age >= 17 the entitled message), above the table printed '
                         'with part (vi): age less than 17, Sarah you are not entitled to apply for '
                         'a driving licence; age between 17 and 74 inclusive, Sarah you are '
                         'entitled to apply for a driving licence; age more than 74, Sarah you are '
                         'entitled to apply for a three-year driving licence.'),
    's-q16a': crop('scheme', 17, (56, 171, 563, 378), ref='2024 OL Q16(a)', solution=True,
                   alt='The marking scheme\'s 18-line possible solution for Question 16(a): '
                       'print("Welcome to the driving licence eligibility checker") #(i); a '
                       'comment #(ii) explaining that the user is asked to input their age and it '
                       'is converted to an integer; age read as an int; print("You entered", age) '
                       '#(iii); name = input("Enter your name: ") #(v); and #(vi) if age > 74 the '
                       'three-year message, elif age < 17 #(iv) the not-entitled message, else the '
                       'entitled message, each printed with the name.'),
    'q16b-output': crop('040', 6, (79, 388, 547, 449), ref='2024 OL Q16(b)',
                        alt='The sample output printed with Question 16(b): Split Bill Calculator; '
                            'How much is the bill?: 100; How many people?: 5; You each owe 20.0.'),
    's-q16b': crop('scheme', 20, (56, 84, 541, 282), ref='2024 OL Q16(b)', solution=True,
                   alt='The marking scheme\'s 17-line possible solution for Question 16(b): '
                       'print("Split Bill Calculator"); myBill read as a float and numberOfPeople '
                       'as an int; bill_per_person = myBill / numberOfPeople; then print("You each '
                       'owe", bill_per_person), each step commented.'),
}

Q13A = P(11, 'The pseudo code below shows the step-by-step process', 'continues reading and executing.')
Q13B = P(12, 'The bottles are numbered and are stored electronically in a list.', '19 67 31')
Q14 = P(14, 'In April 2023, Snapchat began rolling out a new feature called My AI.', 'influence of AI in our daily lives.')
Q14B = [Q14, P(15, 'When creating a piece of software, the quality of the user experience', 'important design consideration.')]
Q15A = P(17, 'The Met Éireann app allows the Irish public', 'storms, floods and snow.')
Q15D = [Q15A, P(19, 'Met Éireann will issue a yellow, orange or red wind warning', 'criteria in the table below.')]
Q16A_STEM = C(4, 'The program below is the start of a program to check if a person is eligible',
              'checking if it meets a condition.')
CORRECT = S(17, 'Correct implementation using solution above or similar.')

CARDS = [
    # ── Section A ──────────────────────────────────────────────────────────
    dict(key=(1, None, None), topic='cs-2-2', qfigure='q1-code0', total=6,
         replaces='batch 1b: the listing was the answer figure and the one row "12" worth 6; now '
                  'the three printed lines at 2 each, the listing beside the question',
         why='p3: the output of three prints; the scheme answers 12, 27 and 3 or 3.0, each 2 '
             '(less 2 if all on one line)',
         ask=P(3, 'State the output from the following Python program in the box below.'),
         rows=[pt(S(4, '12'), 2, note=S(4, 'Each correct item 2 marks', 'presented on same line (12 27 3)')),
               pt(S(4, '27'), 2), pt(S(4, '3 or 3.0'), 2)]),
    dict(key=(2, None, None), topic='cs-2-3', total=6, printed=S(4, 'Question 2 2 + 4 marks'),
         tariff_note='the question prints 2 + 4 marks, 6 in all',
         replaces='batch 1b: the two answers were unpriced rows on a question total; now (a) at '
                  '2 and (b) at 4 / 2 / 1, the question kept whole',
         why='p3: whole question (no part cards): (a) the largest nibble, 1111 at 2; (b) its '
             'decimal value, 15 at 4, half 2, some valid 1',
         stem=P(3, 'In computer science four bits of binary data', 'known as a ‘nibble’.'),
         ask=P(3, '(a) What is the largest binary number', 'into a decimal value.'),
         rows=[ofpart(P(3, '(a)'), pt(S(4, '1111'), 2, note=S(4, 'Correct answer 2 marks'))),
               ofpart(P(3, '(b)'), crit(S(4, '15 (8+4+2+1)'), 4, [1, 2],
                    note=S(4, 'Correct conversion of (a) 4 marks', 'Some valid conversion 1 mark')))]),
    dict(key=(3, None, None), topic='cs-2-3', qfigure='q3-fig0', figure='s-q3a', total=6,
         printed=S(4, 'Question 3 3 + 3 marks'), tariff_note='the question prints 3 + 3 marks, 6 in all',
         replaces='batch 1b: the table headers, page furniture and three explanations were '
                  'unpriced rows on a question total; now (a) three names at 1 and (b) any one '
                  'explanation at 3 / 2, the question kept whole',
         why='p4: whole question (no part cards): (a) name three components, each 1, the scheme\'s '
             'table as the solution crop; (b) one component\'s purpose, 3 / 2',
         ask=P(4, '(a) Choose the appropriate electronic component', 'explain its purpose.'),
         rows=[ofpart(P(4, '(a)'), pt(S(4, 'Capacitor'), 1, note=S(4, 'Each correct item 1 mark'))),
               ofpart(P(4, '(a)'), pt(S(4, 'Resistor'), 1)), ofpart(P(4, '(a)'), pt(S(4, 'Transistor'), 1)),
               ofpart(P(4, '(b)'), ladder([S(5, 'Resistor – Creates resistance', 'Creates a voltage difference.'),
                       S(5, 'Transistor – Amplifies or switches', 'current or voltage flow.'),
                       S(5, 'Capacitor – Can build up and store energy', 'built up energy.')], [[2, 3]],
                      note=S(5, 'Good description – clear understanding demonstrated 3 marks',
                             'Fair description – limited understanding 2 marks')))]),
    dict(key=(4, None, None), topic='cs-2-3', total=6,
         replaces='batch 1b: the scheme\'s two answers were two fixed 3-mark points; now either '
                  'at 6 / 4 / 2',
         why='p4: the purpose of HTTP; the scheme gives two answers, 6 / 4 / 2',
         ask=P(4, 'HTTP stands for Hypertext Transfer Protocol.', 'Explain the purpose of this protocol.'),
         rows=[ladder([S(5, 'Enables the transfer of data over the internet', 'other online resources.'),
                       S(5, 'HTTP is important for web browsers', 'displayed correctly.')], [[2, 4, 6]],
                      note=S(5, 'Very good explanation - clear understanding demonstrated 6 marks',
                             'Fair explanation - limited understanding 2 marks'))]),
    dict(key=(5, None, None), topic='cs-2-2', qfigure='q5-flow', total=6,
         why='p5: match four statements to the flowchart\'s letters; the scheme prints them, 4 '
             'correct 6, 3 correct 5, 2 correct 3, 1 correct 2',
         ask=[P(5, 'There are three different ticket prices', 'some information missing.'),
              P(5, 'Select the appropriate letter from the flowchart', 'the correct statement in Column A.')],
         rows=[anyn([S(5, 'PRINT(price) D'), S(5, 'Is age < 21 AND student = “yes”? A'),
                     S(5, 'price = price – (20% of price) B'), S(5, 'price = price – (10% of price) C')],
                    4, 2, steps=[2, 1, 2, 1],
                    head=P(5, 'Select the appropriate letter from the flowchart', 'the correct statement in Column A.'),
                    note=S(5, '4 correct – 6 marks', '1 correct – 2 mark'))]),
    dict(key=(6, None, None), topic='cs-2-3', qfigure='q6-fig0', figure='s-q6', total=6,
         replaces='batch 1b: the gate table was the answer figure and the one row its header '
                  '"Column A Column B" worth 6; now the three outputs at 2 each with the scheme\'s '
                  'completed table',
         why='p6: the outputs of three logic gates; the scheme prints 1 1 0 beside the gates, '
             'each correct item 2',
         ask=P(6, 'Three different logic gates with inputs are shown', 'either 0 or 1, in Column B.'),
         rows=[crit(S(6, '1 1 0'), 6, [2, 4], note=S(6, 'Each correct item 2 marks'))]),
    dict(key=(7, None, None), topic='cs-1-3', total=6,
         replaces='batch 1b: one task was the only row, worth 6; now any three of seven, clear 2 '
                  'or fair 1 each',
         why='p6: three project manager tasks; the scheme lists seven and accepts any relevant '
             'task, each clear 2 or fair 1',
         ask=P(6, 'Jack has been selected as a project manager', 'responsible for on this project.'),
         rows=[ladder([S(6, 'Coming up with a time line / time plan'), S(6, 'Making decisions on the project'),
                       S(6, 'Leading the team'), S(6, 'Delegating tasks'), S(6, 'Identifying dependencies'),
                       S(6, 'Communicating/reporting to the team & stakeholders'), S(6, 'Managing budgets/resources')],
                      [[1, 2], [1, 2], [1, 2]],
                      instruction=S(6, 'Accept any relevant tasks that could be carried out by a Project Manager'),
                      note=S(6, 'Each valid task (clear) 2 marks', 'Each valid task (fair attempt) 1 mark'))]),
    dict(key=(8, None, None), topic='cs-2-4', qfigure='q8-code0', total=6,
         replaces='batch 1b: the listing was the answer figure and the rows unpriced on a question '
                  'total; now (a) any one reason at 3 / 2 and (b) the print statement at 3, the '
                  'question kept whole',
         why='p7: whole question (no part cards): (a) why int is used, the scheme lists three, '
             '3 / 2; (b) a print statement for line 8, the scheme answers that the numbers are '
             'equal, 3',
         stem=P(7, 'Examine the incomplete Python program below', 'answer the questions that follow.'),
         ask=P(7, '(a) Why is the int function used in lines 1 and 2?', 'could be entered in line 8?'),
         rows=[ofpart(P(7, '(a)'), ladder([S(6, 'Casts the input to an integer'),
                       S(6, 'int sets the data type to an integer/ number/ whole number'),
                       S(6, 'Only allows a number to be entered')], [[2, 3]],
                      note=S(6, 'Good description – clear understanding demonstrated 3 marks',
                             'Fair description – limited understanding 2 marks', nth=1))),
               ofpart(P(7, '(b)'), pt(S(7, 'Numbers are equal / the same / match'), 3, note=S(7, 'Valid print statement 3 marks')))]),
    dict(key=(9, None, None), topic='cs-1-2', total=6,
         replaces='batch 1b: the one row was the heading "Potential Positives:" worth 6; now a '
                  'positive and a negative, each any one at 3 / 2',
         why='p7: one positive and one negative impact of drones; the scheme lists three and '
             'five and accepts any other relevant, each 3 / 2',
         ask=P(7, 'Drones are an example of a computing technology', 'impact of drone technology on society.'),
         rows=[ladder([S(7, 'Fire & rescue services'), S(7, 'Delivery of parcels/medical supplies to remote areas'),
                       S(7, 'Photography')], [[2, 3]], head=S(7, 'Potential Positives:'),
                      instruction=S(7, 'Accept any other relevant positive impact'),
                      note=S(7, 'For each (positive/negative):', 'Fair explanation – limited understanding 2 marks')),
               ladder([S(7, 'Disruption of public transport systems'), S(7, 'Privacy of individuals and their property'),
                       S(7, 'Lethal weaponry (military/war)'), S(7, 'Safety (e.g. airports)'), S(7, 'Noise')], [[2, 3]],
                      head=S(7, 'Potential Negatives:'), instruction=S(7, 'Accept any other relevant negative impact'),
                      note=S(7, 'For each (positive/negative):', 'Fair explanation – limited understanding 2 marks'))]),
    dict(key=(10, None, None), topic='cs-3-2', qfigure='q10-figure', total=6,
         replaces='batch 1b: the data set was the answer figure and the one row its header; now '
                  'any three of five issues at 2, the data set beside the question',
         why='p8: three issues in the survey data; the scheme lists five, each valid issue 2',
         ask=[P(8, 'The data set below shows the raw data collected', 'how teachers travel to work.'),
              P(8, 'You want to use this data as part of a computer science project.', 'issues with the data in the data set.')],
         rows=[anyn([S(7, 'Duplicate data for Mr. Murray'), S(7, '“yes” entered instead of Y/N'),
                     S(7, 'Blank entry for Mode of Transport for Ms. Jones'),
                     S(7, '340 is unrealistic distance for Ms. Jones'),
                     S(7, '-18 is negative distance value for Ms. O’Neill')], 3, 2,
                    head=P(8, 'List three issues with the data in the data set.'),
                    note=S(7, 'Each valid issue 2 marks'))]),
    dict(key=(11, None, None), topic='cs-2-3', qfigure='q11-fig2', total=6,
         why='p8: one digital and one analogue input; the scheme lists both, each 3 / 2',
         ask=P(8, 'Provide one example of a digital input and one example of an analogue input',
               'such as those shown in Figure 2.'),
         rows=[ladder([S(8, 'Button'), S(8, 'On/ Off Switch'), S(8, 'Shake'), S(8, 'Pins')], [[2, 3]],
                      head=S(8, 'Digital Inputs:'), instruction=S(8, 'Accept any relevant digital input'),
                      note=S(8, 'For each (digital/analogue):', 'Fair example 2 marks')),
               ladder([S(8, 'Accelerometer'), S(8, 'Magnetometer'), S(8, 'Temperature Sensor'),
                       S(8, 'Light Sensor'), S(8, 'Moisture Sensor'), S(8, 'Sound Sensor'),
                       S(8, 'Pressure Sensor'), S(8, 'Distance Sensor')], [[2, 3]],
                      head=S(8, 'Analogue Inputs:'), instruction=S(8, 'Accept any relevant analogue input'),
                      note=S(8, 'For each (digital/analogue):', 'Fair example 2 marks'))]),
    dict(key=(12, None, None), topic='cs-2-5', qfigure='q12-fig0', total=6,
         replaces='batch 1b: the mockup was the answer figure and one method the only row, worth '
                  '6; now any three of five at 2, the mockup beside the question',
         why='p9: three validation methods for the form; the scheme lists five, each 2',
         ask=P(9, 'A teacher has asked you to design a website', 'eliminate any input errors.'),
         rows=[anyn([S(8, 'Student Name - presence check, character only'),
                     S(8, 'Year Group - presence check, range check', 'select menu, v'),
                     S(8, 'Contact Number - presence check', 'numbers only'),
                     S(8, 'Contact Email - presence check', '(contains @ , .com, etc.)'),
                     S(8, 'Permission Slip - presence check', '(yes/no value only)')], 3, 2,
                    head=P(9, 'Suggest three possible data validation methods', 'eliminate any input errors.'),
                    note=S(8, 'Each valid method 2 marks'))]),
    # ── Section B ──────────────────────────────────────────────────────────
    dict(key=(13, 'a', 'i'), topic='cs-2-2', qfigure='q13-code0', total=3,
         replaces='batch 1b: the stem was "This question continues on the next page." and the '
                  'listing the answer figure; three definitions were 1-mark points; now any one at '
                  '3 / 2 with the listing beside the question',
         why='p11: what a variable is; the scheme gives three answers, 3 / 2',
         stem=Q13A, ask=P(11, 'A and B are both variables. What is a variable?'),
         rows=[ladder([S(9, 'A variable is a named location in computer’s memory used to store data'),
                       S(9, 'A declaration of a value that can be changed'),
                       S(9, 'A term used as a placeholder for a value that can change')], [[2, 3]],
                      note=S(9, 'Good description – clear understanding demonstrated 3 marks',
                             'Fair description – limited understanding 2 marks'))]),
    dict(key=(13, 'a', 'ii'), topic='cs-2-4', qfigure='q13-code0', total=6,
         replaces='batch 1b: the stem was page furniture and A\'s type the only row, worth 6; now '
                  'A and B at 3 each',
         why='p11: data types for A and B; the scheme answers Integer and Boolean, 3 each',
         stem=Q13A, ask=P(11, 'Choose suitable data types for the variables A and B.'),
         rows=[pt(S(9, 'A – Int / Integer'), 3, note=S(9, 'A correct 3 marks B correct 3 marks')),
               pt(S(9, 'B – Bool/ Boolean'), 3)]),
    dict(key=(13, 'a', 'iii'), topic='cs-2-2', qfigure='q13-code0', total=2,
         replaces='batch 1b: the stem was page furniture and two answers 1-mark points; now either '
                  'at 2 / 1',
         why='p11: what initialised means; the scheme gives two answers, 2 / 1',
         stem=Q13A, ask=P(11, 'In lines 1 and 2 in this program the variables are initialised.', 'in relation to variables.'),
         rows=[ladder([S(9, 'An initialised variable is when a variable is given starting value'),
                       S(9, 'The initial value given to a variable the first time it is declared')], [[1, 2]],
                      note=S(9, 'Good description – clear understanding demonstrated 2 marks',
                             'Fair description – limited understanding 1 marks'))]),
    dict(key=(13, 'a', 'iv'), topic='cs-2-2', qfigure='q13-code0', total=4,
         replaces='batch 1b: the stem was "This question continues on the next page."; now the '
                  'question\'s stem with the listing beside it',
         why='p12: the line of the conditional; the scheme answers line 5, 4',
         stem=Q13A, ask=P(12, 'This program has a conditional statement.', 'is the conditional statement?'),
         rows=[pt(S(9, 'Line 5'), 4)]),
    dict(key=(13, 'a', 'v'), topic='cs-2-2', qfigure='q13-code0', total=5,
         replaces='batch 1b: the stem was page furniture and the answer all or nothing; now 5 / 3',
         why='p12: the infinite loop in the code; the scheme traces it, 5 / 3',
         stem=Q13A, ask=P(12, 'This program enters an “infinite loop”.', 'with reference to the code.'),
         rows=[crit(S(9, 'On line 4 the programme jumps to line 7.', 'will not impact the loop.'), 5, [3],
                    note=S(9, 'Good description – clear understanding demonstrated 5 marks',
                           'Fair description – limited understanding 3 marks'))]),
    dict(key=(13, 'a', 'vi'), topic='cs-2-2', qfigure='q13-code0', total=2,
         replaces='batch 1b: the stem was page furniture and the answer split over two 1-mark '
                  'lines; now the scheme\'s answer at 2 / 1',
         why='p12: logic error against syntax error; the scheme answers it, 2 / 1',
         stem=Q13A, ask=P(12, 'The infinite loop in the program above is an example', 'a logic error and a syntax error?'),
         rows=[crit(S(10, 'Syntax errors are mistakes in the code structure', 'compiles and runs successfully.'), 2, [1],
                    note=S(10, 'Good description – clear understanding demonstrated 2 marks',
                           'Fair description – limited understanding 1 mark'))]),
    dict(key=(13, 'b', 'i'), topic='cs-2-2', total=4,
         replaces='batch 1b: the stem was the list and pseudo code as text and the scheme\'s two '
                  'answers were 2-mark points; now either at 4 / 2; topic Algorithms',
         why='p12: why a linear search suits this list; the scheme gives two answers, 4 / 2; '
             'filed under Algorithms (searching), not Computer systems',
         stem=Q13B, ask=P(12, 'Why would a programmer use a linear search', 'from this list?'),
         rows=[ladder([S(10, 'The list in not in any sort of order', 'binary search will not work.'),
                       S(10, 'The list is short enough to justify the use of a linear search', '(no need to sort)')], [[2, 4]],
                      note=S(10, 'Good description – clear understanding demonstrated 4 marks',
                             'Fair description – limited understanding 2 marks'))]),
    dict(key=(13, 'b', 'ii'), topic='cs-2-2', qfigure='q13b-code', total=6,
         replaces='batch 1b: the stem was the list and pseudo code as text and the answer the '
                  'first step alone, all or nothing; now the four steps at 6 / 4 / 2 with the '
                  'pseudo code beside the question',
         why='p13: trace the search for 23; the scheme steps through it, all steps with the '
             'right index 6, without 4, limited 2',
         stem=Q13B, ask=P(13, 'The following pseudo code is a basic implementation of a linear search.', 'using this pseudo code.'),
         rows=[crit(S(10, 'The code will check the first item in the list (12)', 'the index of 3 will be returned.'), 6, [2, 4],
                    note=S(10, 'Very good - all steps demonstrated with correct index 6 marks',
                           'Fair – limited knowledge of linear search demonstrated 2 marks'))]),
    dict(key=(13, 'b', 'iii'), topic='cs-2-2', total=6,
         why='p13: one disadvantage of linear search on large data; the scheme answers it, 6 / 4',
         stem=Q13B,
         ask=P(13, 'Explain one disadvantage of the linear search algorithm', 'large data sets.'),
         rows=[crit(S(10, 'The linear search might have to check every item', 'take a lot more time.'), 6, [4],
                    note=S(10, 'Good description – clear understanding demonstrated 6 marks',
                           'Fair description – limited understanding 4 marks'))]),
    dict(key=(14, 'a', 'i'), topic='cs-1-2', total=6,
         replaces='batch 1b: the stem was the (ii) statements as text and one example the only '
                  'row, worth 6; now any three of nine at 2',
         why='p14: three uses of AI in daily life; the scheme lists nine and accepts other '
             'relevant answers, each 2',
         stem=Q14, ask=P(14, 'List three other examples of the use of AI in our day-to-day lives.'),
         rows=[anyn([S(11, 'Virtual assistants like Siri, Alexa, Google Assistant'),
                     S(11, 'Recommendations: Online platforms such as', 'Spotify and Amazon'),
                     S(11, 'Adverts on social media:', 'Instagram and TikTok'),
                     S(11, 'Navigation Apps: like Google Maps'), S(11, 'Facial recognition'),
                     S(11, 'Self-driving cars'), S(11, 'Online chat bots'),
                     S(11, 'AI games: like QuickDraw, AlphaGo'),
                     S(11, 'Online services: like ChatGPT & Bing image generator')], 3, 2,
                    head=P(14, 'List three other examples of the use of AI in our day-to-day lives.'),
                    instruction=S(11, 'Accept other relevant answers'), note=S(11, 'Each correct item 2 marks'))]),
    dict(key=(14, 'a', 'ii'), topic='cs-1-2', total=5,
         replaces='batch 1b: the stem was the statements as text and the five answers one 5-mark '
                  'row cut mid-sentence; now each statement with its answer, 1 each',
         why='p14: five statements true or false; the scheme prints the answer beside each, 1 '
             'each, paired with the paper\'s statement in printed order',
         stem=Q14, ask=P(14, 'State whether each of the following statements is true or false', 'in the appropriate box.'),
         rows=[pt(Pair(P(14, 'Artificial intelligence and machine learning are exactly the same thing.'),
                       S(11, 'False', nth=1)), 1, note=S(11, 'Each correct item 1 mark')),
               pt(Pair(P(14, 'There are some jobs that could potentially be replaced by AI in the future.'),
                       S(11, 'True', nth=1)), 1),
               pt(Pair(P(14, 'AI algorithms can make decisions based on patterns and data', 'for each single decision.'),
                       S(11, 'True', nth=2)), 1),
               pt(Pair(P(14, 'AI always makes fair and unbiased decisions.'), S(11, 'False', nth=2)), 1),
               pt(Pair(P(14, 'AI technology is commonly used in self-driving vehicles', 'make decisions on the road.'),
                       S(11, 'True', nth=3)), 1)]),
    dict(key=(14, 'a', 'iii'), topic='cs-1-2', total=4,
         replaces='batch 1b: the answer was split over 1-mark rows with two rows of page furniture '
                  '("Leaving Certificate 2024"); now the answer at 4 / 2',
         why='p14: what training a model means; the scheme answers it, 4 / 2',
         stem=Q14, ask=P(14, 'Artificial intelligence applications such as My AI and ChatGPT', 'train a machine learning model.'),
         rows=[crit(S(11, 'Training a machine learning model is the process', 'based on large data sets.'), 4, [2],
                    note=S(11, 'Good description – clear understanding demonstrated 4 marks',
                           'Fair description – limited understanding 2 marks'))]),
    dict(key=(14, 'b', 'i'), topic='cs-1-2', total=4,
         replaces='batch 1b: the stem was the quote and another part\'s ask, and one principle the '
                  'only row, worth 4; now any two of seven at 2 / 1',
         why='p15: two universal design principles for My AI; the scheme lists seven, each 2 / 1',
         stem=Q14B, ask=P(15, 'Universal design should be used to ensure a good level of user experience.', 'Snapchat’s My AI.'),
         rows=[ladder([S(12, 'Equitable Use - The app is usable', 'text to speech)'),
                       S(12, 'Flexibility in Use - The app can be changed', "kid's version)"),
                       S(12, 'Simple and Intuitive Use - The app is straight forward', 'has a help option'),
                       S(12, 'Perceptible Information - Making sure the information', 'number of different methods'),
                       S(12, 'Tolerance for Error - The app is designed to minimize the chance of errors'),
                       S(12, 'Low Physical Effort - The app is easy to use and not physically demanding'),
                       S(12, 'Size and Space for Approach and Use - The app can be used', 'in any environment')],
                      [[1, 2], [1, 2]],
                      note=S(12, 'For each principle:', 'Fair description – limited understanding 1 marks'))]),
    dict(key=(14, 'b', 'ii'), topic='cs-1-2', total=4,
         replaces='batch 1b: the stem was the quote\'s byline and this part\'s ask, and one risk '
                  'the only row, worth 4; now any one of five at 4 / 2',
         why='p15: one risk of an untested chatbot to children; the scheme lists five and accepts '
             'any appropriate answer, 4 / 2',
         stem=Q14B, ask=P(15, 'An article on the RTE website, published in April 2023', 'if it has not been properly tested.'),
         rows=[ladder([S(12, 'Safety risks - There might be flaws in the system that can be hacked'),
                       S(12, 'Privacy risks - Personal information might be shared'),
                       S(12, 'Content risks - Inappropriate content might be available on the app'),
                       S(12, 'Negative impact on well-being', 'bad life choices & decision making'),
                       S(12, 'Addictiveness - The app might be highly addictive for children')], [[2, 4]],
                      instruction=S(12, 'Accept any appropriate answer given'),
                      note=S(12, 'Good description – clear understanding demonstrated 4 marks',
                             'Fair description – limited understanding 2 marks'))]),
    dict(key=(14, 'b', 'iii'), topic='cs-2-5', total=3,
         replaces='batch 1b: the stem was another part\'s quote and ask and the answer all or '
                  'nothing; now 3 / 2; topic Evaluation and testing',
         why='p15: explain UAT; the scheme answers it, 3 / 2; filed under Evaluation and testing, '
             'not Data',
         stem=Q14B, ask=P(15, 'Snapchat conducted user acceptance testing (UAT)', 'Explain UAT?'),
         rows=[crit(S(12, 'User Acceptance Testing (UAT) is the final stage', 'works in real-life scenarios.'), 3, [2],
                    note=S(12, 'Good explanation – clear understanding demonstrated 3 marks',
                           'Fair explanation– limited understanding 2 marks'))]),
    dict(key=(14, 'c', None), topic='cs-1-2', total=12,
         replaces='batch 1b: the stem was the Q14 intro alone and each list was claimed whole at 6 '
                  'with its options joined into the head; now a positive and a negative, each any '
                  'one at 6 / 4',
         why='p16: the positive and negative impact of AI for students; the scheme lists eight of '
             'each, each side 6 / 4',
         stem=Q14, ask=P(16, 'In September 2023, it was announced that teacher-based assessment', 'for students in school.'),
         rows=[ladder([S(13, 'Personalised Learning'), S(13, 'Access to resources'), S(13, 'Assistance with homework'),
                       S(13, 'Enhanced accessibility Spell check work'), S(13, 'Suggest improvements on student work'),
                       S(13, 'Feedback on pieces of work'), S(13, 'Generate study notes for students'),
                       S(13, 'Create study tips / custom study timetables')], [[4, 6]], head=S(13, 'Positive impacts:'),
                      note=S(13, 'For each (positive/negative):', 'Fair discussion - limited understanding 4 marks')),
               ladder([S(13, 'Privacy concerns'), S(13, 'Bias Issues'), S(13, 'Overreliance on technology'),
                       S(13, 'Wrong information given'), S(13, 'Using AI to complete work'),
                       S(13, 'AI to assist in tasks may reduce critical thinking skills'),
                       S(13, 'Lack of independent research & effort levels'),
                       S(13, 'Reduction of problem-solving skills and logical thinking skills')], [[4, 6]],
                      head=S(13, 'Negative impacts:'),
                      note=S(13, 'For each (positive/negative):', 'Fair discussion - limited understanding 4 marks'))]),
    dict(key=(15, 'a', 'i'), topic='cs-3-3', total=5,
         replaces='batch 1b: the stem was page furniture, an unrelated table was attached, and the '
                  'examples were five 1-mark points; now any one example at 2 with its benefit 3 / 2; '
                  'topic Modelling and simulation',
         why='p17: another simulation and its benefit; the scheme lists five examples and accepts '
             'any relevant, example 2 and description 3 / 2; filed under Modelling and simulation, '
             'not Computational thinking',
         stem=Q15A, ask=P(17, 'Provide one other example of a computer simulation', 'benefit of using such a simulation.'),
         rows=[ladder([S(14, 'Flight simulation'), S(14, 'Natural disaster simulation'), S(14, 'Simulating traffic flow'),
                       S(14, 'Simulating structural movements'), S(14, 'Simulation of building evacuations')],
                      [[2, 3, 4, 5]], instruction=S(14, 'Accept any relevant example'),
                      note=S(14, 'Relevant example 2 mark', 'Fair description – limited understanding 2 marks'))]),
    dict(key=(15, 'a', 'ii'), topic='cs-2-3', total=6,
         replaces='batch 1b: the stem was page furniture, an unrelated table was attached, and the '
                  'one row "Examples:" worth 6; now any two developments, named 1 and explained '
                  '2 / 1',
         why='p17: two computing developments since 1948; the scheme lists five and any valid, '
             'each example 1 and description 2 / 1',
         stem=Q15A, ask=P(17, 'The first time that Met Éireann provided weather forecasts', 'weather information instantly.'),
         rows=[ladder([S(14, 'Ethernet'), S(14, 'World Wide Web'), S(14, 'WiFi'), S(14, 'GPS'),
                       S(14, 'Smart Phones / Apps')], [[1, 2, 3], [1, 2, 3]],
                      head=S(14, 'Examples:'), instruction=S(14, 'Any valid computing development since 1948'),
                      note=S(14, 'For each development:', 'Fair description – limited understanding 1 mark'))]),
    dict(key=(15, 'b', None), topic='cs-2-4', qfigure='q15-fig0', total=5,
         replaces='batch 1b: the stem was the table as text, the table the answer figure, and the '
                  'one row the header "Column A Column B Column C"; now the five completed rows at '
                  '1 each with the table beside the question',
         why='p18: five data types; the scheme completes the table (Float, List, Integer, Boolean, '
             'String), each 1',
         stem=Q15A, ask=P(18, 'In the design phase of the development of the app', 'The first row has been completed for you.'),
         rows=[pt(S(15, 'Temperature Should accept a decimal number Float'), 1, note=S(15, 'Each correct item 1 mark')),
               pt(S(15, 'Province Any one of the following:', 'Ulster] List'), 1),
               pt(S(15, 'Wind speed Should not be a decimal number Integer'), 1),
               pt(S(15, 'Issue weather warning Yes or No Boolean'), 1),
               pt(S(15, 'Weather description Written description', 'warm and sunny today String'), 1)]),
    dict(key=(15, 'c', None), topic='cs-1-2', total=6,
         replaces='batch 1b: an unrelated table was attached and one feature the only row, worth 6; '
                  'now any three of eleven at 2',
         why='p18: three accessibility features; the scheme lists eleven and accepts other '
             'relevant answers, each 2',
         stem=Q15A, ask=P(18, 'When designing an app such as this', 'increased accessibility for all users.'),
         rows=[anyn([S(15, 'Screen reader compatibility'), S(15, 'Translate language'), S(15, 'Increase font size'),
                     S(15, 'Consistent layout'), S(15, 'Good use of space'), S(15, 'High contrast colours'),
                     S(15, 'Easy navigation'), S(15, 'Search option'), S(15, 'Help option'),
                     S(15, 'Frequently Asked Questions'), S(15, 'Live chat')], 3, 2,
                    head=P(18, 'List three features that could be included', 'increased accessibility for all users.'),
                    instruction=S(15, 'Accept other relevant answers'),
                    note=S(15, 'Each correct item 2 marks (max 6 marks)'))]),
    dict(key=(15, 'd', 'i'), topic='cs-2-2', qfigure='q15d-table', total=11,
         replaces='batch 1b: the stem was the warning table as text and "Space for extra work", and '
                  'the pseudo code one 11-mark row; now each condition at 3 / 2 and the appearance '
                  'at 2 / 1, with the table beside the question',
         why='p19: an algorithm for the wind warnings; the scheme prints example pseudo code, each '
             'of three conditions 3 / 2 and the appearance 2 / 1',
         stem=Q15D, ask=P(19, 'Based on this information create an algorithm', 'what colour the warning should be.'),
         rows=[crit(S(16, 'IF speed > 90 and speed < 110: RETURN Yellow Wind Warning'), 3, [2],
                    note=S(16, 'For each condition (3 possible):', 'Reasonable implementation 2 mark')),
               crit(S(16, 'ELIF speed > 111 and speed <130: RETURN Orange Wind Warning'), 3, [2]),
               crit(S(16, 'ELIF speed > 130: RETURN Red Wind Warning'), 3, [2]),
               crit(S(16, 'Very good (correct indentation/decision shapes, etc.)'), 2, [1],
                    head=S(16, 'Overall pseudocode/flowchart appearance:'), note=S(16, 'Fair 1 mark'))]),
    dict(key=(15, 'd', 'ii'), topic='cs-2-5', qfigure='q15d-table', total=5,
         replaces='batch 1b: the stem was the table as text and furniture and the answer one 5-mark '
                  'row; now the choice at 2 and its justification at 3 / 2; topic Evaluation and '
                  'testing',
         why='p19: the best test data and why; the scheme ticks the first set, 2, and justifies '
             'it, 3 / 2; filed under Evaluation and testing (test data), not Algorithms',
         stem=Q15D, ask=P(19, 'Which of the following is the best set of data values', 'Justify your answer below.'),
         rows=[pt(S(16, '[89, 90, 100, 110, 111, 129, 130, 131]'), 2, note=S(16, 'Correct answer 2 marks')),
               crit(S(16, 'This covers and tests all of the conditions / boundaries from the algorithm.'), 3, [2],
                    note=S(16, 'Good description – clear understanding demonstrated 3 marks',
                           'Fair description – limited understanding 2 mark'))]),
    # ── Section C ──────────────────────────────────────────────────────────
    dict(key=(16, 'a', 'i'), topic='cs-2-2', qfigure='q16a-code', figure='s-q16a', total=10,
         printed=S(17, '(i) 10 marks (A-10 scale)'),
         why='040 p4: print the new welcome; the scheme marks line 4 #(i), A-10 scale (new part '
             'card: the shipped whole-question card cs-2024-ol-q16 is withdrawn onto it)',
         stem=Q16A_STEM, ask=C(4, 'Modify the program so that it first prints out', 'What age are you?'),
         rows=[crit(CORRECT, 10, [7], note=S(17, '(i) 10 marks (A-10 scale)', 'Any other reasonable attempt.'))]),
    dict(key=(16, 'a', 'ii'), topic='cs-2-2', qfigure='q16a-code', figure='s-q16a', total=5,
         printed=S(17, '(ii) 5 marks (B-5 scale)'),
         why='040 p4: comment line 6; the scheme marks line 6 #(ii), B-5 scale (new part card)',
         stem=Q16A_STEM, ask=C(4, 'Insert a comment in the code that explains what is happening on line 6.'),
         rows=[crit(CORRECT, 5, [2, 3], note=S(17, '(ii) 5 marks (B-5 scale)', 'Any other reasonable attempt.'))]),
    dict(key=(16, 'a', 'iii'), topic='cs-2-2', qfigure='q16a-code', figure='s-q16a', total=10,
         printed=S(18, '(iii) 10 marks (C-10 scale)'),
         why='040 p4: print the age entered; the scheme marks line 8 #(iii), C-10 scale; its '
             'descriptors for this part are printed twice over in the text layer, so the note is '
             'the part\'s heading (new part card)',
         stem=Q16A_STEM, ask=C(4, 'Print a message stating the age that the user entered.',
                               'You are entitled to apply for a driving licence.'),
         rows=[crit(CORRECT, 10, [3, 5, 7], note=S(18, '(iii) 10 marks (C-10 scale)'))]),
    dict(key=(16, 'a', 'iv'), topic='cs-2-2', qfigure='q16a-code', figure='s-q16a', total=15,
         printed=S(18, '(iv) 15 marks (C-15 scale)'),
         why='040 p5: a message for ages under 17; the scheme marks line 15 #(iv), C-15 scale '
             '(new part card)',
         stem=Q16A_STEM, ask=C(5, 'Currently the program will only output a message',
                               'You are not entitled to apply for a driving licence.'),
         rows=[crit(CORRECT, 15, [3, 7, 10], note=S(18, '(iv) 15 marks (C-15 scale)', 'Any other reasonable attempt.'))]),
    dict(key=(16, 'a', 'v'), topic='cs-2-2', qfigure='q16a-code', figure='s-q16a', total=10,
         printed=S(18, '(v) 10 marks (C-10 scale)'),
         why='040 p5: ask for and use the name; the scheme marks line 10 #(v), C-10 scale (new '
             'part card)',
         stem=Q16A_STEM, ask=C(5, 'Amend the program to ask for the user’s name.',
                               'Sarah you are not entitled to apply for a driving licence.'),
         rows=[crit(CORRECT, 10, [3, 5, 7], note=S(18, '(v) 10 marks (C-10 scale)', 'Any other reasonable attempt.'))]),
    dict(key=(16, 'a', 'vi'), topic='cs-2-2', qfigure='q16a-vi', figure='s-q16a', total=10,
         printed=S(19, '(vi) 10 marks (C-10 scale)'),
         why='040 p5: three messages from the age table; the scheme marks lines 12-18 #(vi), C-10 '
             'scale (new part card)',
         stem=Q16A_STEM,
         ask=[C(5, 'Update your program so that it outputs a message to the user', 'The name Sarah is used in the examples below.'),
              C(5, 'When the program is run the output may now look as follows:', 'three-year driving licence.', nth=3)],
         rows=[crit(CORRECT, 10, [3, 5, 7], note=S(19, '(vi) 10 marks (C-10 scale)', 'Any other reasonable attempt.'))]),
    dict(key=(16, 'b', None), topic='cs-2-2', qfigure='q16b-output', figure='s-q16b', total=20,
         replaces='batch 1b: filed as section B, its stem the copy-the-file instructions and its '
                  'row "Possible solution:" worth 20; now section C, the bill-splitting task, the '
                  'sample output, and the rubric\'s four criteria at 5 / 3 / 2',
         why='040 p6: write the split bill calculator; the scheme prints a possible solution and '
             'a rubric of four criteria at high / moderate / low, 5 / 3 / 2 each (cells of scheme '
             'p21)',
         ask=C(6, 'Implement a program that will help you to split a restaurant bill', 'printed with a suitable message.'),
         rows=[crit(T(21, 'Program executes with no syntax or runtime errors', 'Meaningful variable names'),
                    5, [2, 3], head=T(21, 'Programming Standards'),
                    note=[T(21, 'High level of achievement All of the following', 'correctly and efficiently'),
                          T(21, 'Moderate level of achievement Reasonable attempt', 'each of the following'),
                          T(21, 'Low level of achievement Poor attempt to complete any of the following')]),
               crit(T(21, 'User correctly prompted to enter a bill amount', 'use of assignment statements'), 5, [2, 3],
                    head=T(21, 'Program Inputs')),
               crit(T(21, 'Programme divides total bill by the number of people'), 5, [2, 3],
                    head=T(21, 'Program Logic (Processing)')),
               crit(T(21, 'Program outputs “Split Bill Calculator” at the start', 'owned amount correctly'), 5, [2, 3],
                    head=T(21, 'Program Outputs'))]),
]
