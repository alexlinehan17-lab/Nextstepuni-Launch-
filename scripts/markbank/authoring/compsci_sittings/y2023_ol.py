"""Computer Science 2023 Ordinary Level: every card of the sitting, lifted from the page.

The 23 cards shipped in August are re-authored here under their own ids (batch
1b), and the 10 the lane added for the asks they missed are kept, converted to
the ladder and instruction rules of 5 Nov. Paper pages 3-18 (Sections A and B)
and Section C pages 4-7, and scheme pages 4-21 were opened.

cs-2023-ol-q2, -q8 and -q11 are shipped as whole questions (Q2(a)+(b),
Q8(a)+(b), Q11(a)-(c)); each keeps that unit and carries every part's
answer. cs-2023-ol-q13 is shipped as the whole of Q13 but its parts (a)(i),
(a)(ii) and (c)(ii) have cards of their own; it holds the five asks no other
card holds, (b)(i)-(iv) and (c)(i), at their printed 12 and 6.

Q13(a)(i)'s table and Q16(b)'s rubric are read from the scheme's table cells
(pages 10 and 21, compsci_lane.append_cells): the flat text welds the first
definition around its answer ("... elements of the Array same data type") and
reads the rubric across its three levels.

Q15(c) is answered in the scheme by its marking criteria alone (name 1,
explanation 5 / 2, for the benefit and for the danger), with no example
technology; the card carries those criteria as the components the student
places marks on, in the scheme's own words.
"""
from compsci_lane import (C, P, S, T, Pair, anyn, crit, crop, ladder, pt, stack)  # noqa: F401

CROPS = {
    'q1-table': crop('038', 3, (126, 183, 456, 483), ref='2023 OL Q1',
                     alt='The declarations printed with Question 1, a = 21 and b = 10, above a '
                         'table whose Column A lists six print statements, print(a == b), '
                         'print(b != a), print(a > b), print(b <= a), print(a == 10) and '
                         'print(b != 21), and whose Column B, True or False, is blank.'),
    'q5-fig1': crop('038', 5, (352, 74, 542, 253), ref='2023 OL Q5',
                    alt='Figure 1: a street photograph of a woman cycling past a white '
                        'car, with three labelled boxes drawn on it: Person around the cyclist, '
                        'Bicycle around the bike and Car around the car.'),
    'q6-table': crop('038', 5, (92, 532, 516, 733), ref='2023 OL Q6',
                     alt='The table printed with Question 6: Column A lists Member Name, Member '
                         'Age, Amount Paid, Most Popular Days to Visit and Member Completed '
                         'Induction – Yes/No; Column B (Data Type) is blank.'),
    'q9-table': crop('038', 7, (54, 125, 507, 377), ref='2023 OL Q9',
                     alt='The table printed with Question 9: Column A lists the number of players '
                         'in a football squad, the number of students in a class, the speed of a '
                         'school bus, the temperature of a classroom, the number of days it rained '
                         'in March and the weight of a box; Column B (Discrete or Continuous) is '
                         'blank.'),
    'q10-fig3': crop('038', 7, (135, 430, 455, 707), ref='2023 OL Q10',
                     alt='Figure 3: an OR gate with inputs A and B. Below it, the truth table with '
                         'columns A, B and out (A OR B); the A and B columns read 0 0, 0 1, 1 0 and '
                         '1 1, and the out column is blank.'),
    'q13a-table': crop('038', 10, (80, 218, 543, 402), ref='2023 OL Q13(a)(i)',
                       alt='The table printed with Question 13(a)(i): Column A lists four '
                           'definitions, a data structure that can store a collection of '
                           'elements of the same data type, a character that represents a '
                           'mathematical or logical action, a command for handling a decision, '
                           'and a memory location that can store a value; Column B, Term, is '
                           'blank.'),
    'q13a-trace': crop('038', 10, (88, 462, 507, 726), ref='2023 OL Q13(a)(ii)',
                       alt='The six-line program printed with Question 13(a)(ii): i = 1, j = 10, '
                           'while i < j: print(i), i = i + 1, j = j - 1. Below it, a trace '
                           'table with columns i, j, while i < j and print(i) and rows 1 to 6; '
                           'row 1 reads 1, 10, True, 1 and rows 2 to 6 are blank.'),
    'q13b-fig4': crop('038', 11, (54, 120, 553, 393), ref='2023 OL Q13(b)',
                      alt='Figure 4: the flowchart of the charging cost algorithm. Start, then '
                          'BatteryLevel = Check car battery charge; if BatteryLevel < 30% Cost = '
                          '€5, otherwise if BatteryLevel < 70% Cost = €4, otherwise Cost = €3. '
                          'Then Loyalty Card Presented?: Yes sets Cost = Cost - €1; both paths '
                          'reach Print Cost, then End.'),
    'q16a-code': crop('040', 4, (76, 341, 540, 497), ref='2023 OL Q16(a)',
                      alt='The eleven-line program Question16_A.py as printed in the Section C '
                          'booklet: two comment lines, print("Multiplication program"), number = '
                          '7, print("Multiplications of ", number), then for i in range(10): '
                          'print(number*i).'),
    'q16b-table': crop('040', 7, (127, 398, 511, 547), ref='2023 OL Q16(b)',
                       alt='The table printed with Question 16(b), columns Condition and Output: '
                           'temperature is less than 20, Too cold. Turn up heating.; temperature '
                           'between 20 – 24, Temperature is just right.; temperature is more '
                           'than 24, Too warm. Turn down heating.'),
    's-q3': crop('scheme', 5, (52, 74, 545, 442), ref='2023 OL Q3', solution=True,
                 alt='The marking scheme\'s examples for Question 3. Pseudocode: input num1, input '
                     'num2, input num3, average = (num1 + num2 + num3) /3, print average. A '
                     'flowchart that does the same: Start, three inputs, the average calculated, '
                     'the average output, Stop.'),
    's-q4': crop('scheme', 5, (55, 574, 400, 668), ref='2023 OL Q4', solution=True,
                 alt='The marking scheme\'s two workings for Question 4: repeated division, 14/2 '
                     '= 7 remainder 0, 7/2 = 3 remainder 1, 3/2 = 1 remainder 1, 1/2 = 0 '
                     'remainder 1, Ans: 1110; or place values, 14 = 8 + 4 + 2 + 0 with the '
                     'digits 1 1 1 0 beneath, Ans: 1110.'),
    's-q13a-ii': crop('scheme', 10, (88, 463, 507, 633), ref='2023 OL Q13(a)(ii)', solution=True,
                      alt='The marking scheme\'s completed trace table for Question 13(a)(ii): '
                          'row 1 1, 10, True, 1 as printed; row 2 2, 9, True, 2; row 3 3, 8, '
                          'True, 3; row 4 4, 7, True, 4; row 5 5, 6, True, 5; row 6 6, 5, False, '
                          'and 6 or blank under print(i).'),
    's-q15a-ii': crop('scheme', 15, (160, 386, 380, 543), ref='2023 OL Q15(a)(ii)', solution=True,
                      alt='The marking scheme\'s example diagram of the client-server model: a '
                          'laptop, a phone and a desktop computer labelled Clients, joined '
                          'through a cloud labelled Internet to a machine labelled Server.'),
    's-q16a': crop('scheme', 17, (53, 154, 542, 351), ref='2023 OL Q16(a)', solution=True,
                   alt='The marking scheme\'s possible solution to Question 16(a), lines 1 to 14: '
                       'rows of asterisks printed above and below "Times Table program" (marked '
                       '(ii) and (i)); number read with int(input()) (iii); a negative number '
                       'refused with an error message (iv); and a for loop over range(13) (v) '
                       'printing i, "x", number, "=", number*i (vi).'),
    's-q16b': crop('scheme', 20, (53, 84, 543, 328), ref='2023 OL Q16(b)', solution=True,
                   alt='The marking scheme\'s possible solution to Question 16(b), lines 1 to 19: '
                       'a welcome message printed; temperature read with int(input()); then if '
                       'temperature < 20 print Too cold. Turn up heating., elif temperature >= 20 '
                       'and temperature <= 24 print Temperature is just right., else print Too '
                       'warm. Turn down heating., each step explained by a comment.'),
}

Q8_STEM = P(6, 'Below is a sorted list of student names.', 'Julie Kevin Senan')
Q11_STEM = P(8, 'The Python code below is being used', 'answer the questions below.')
Q13C_STEM = P(12, 'Three cars arrive at an electric vehicle', 'which car is being charged.')
Q14A_STEM = P(13, 'RTÉ Player was first launched in 2009', 'many different people involved.')
Q14B = [Q14A_STEM, P(14, 'The diagram, in Figure 5 below, shows a typical software development lifecycle.')]
Q14C = [Q14A_STEM, P(15, 'As part of the development of the new app it is planned to conduct testing.')]
Q15_STEM = P(16, 'A local school stores student details on their computer network.', 'information held on the network.')
Q16A_STEM = C(4, 'The program below produces a times table', 'ten times in total.')
CORRECT = 'Correct implementation using solution above or similar.'
RUBRIC = [T(21, 'High level of achievement All of the following', 'correctly and efficiently'),
          T(21, 'Moderate level of achievement Reasonable attempt', 'each of the following'),
          T(21, 'Low level of achievement Poor attempt to complete any of the following')]

CARDS = [
    # ── Section A ──────────────────────────────────────────────────────────
    dict(key=(1, None, None), topic='cs-2-2', qfigure='q1-table', total=6,
         replaces='batch 1b: the row was the table header "Column A Column B" worth 6; the six '
                  'answers were never rows; the figure held the ask and sat on the answer side',
         why='p3: the Boolean result of six print statements; the scheme prints each, 1 mark',
         ask=P(3, 'Given the following variable declarations', 'in the table below.'),
         rows=[pt(S(4, 'print(a == b) False'), 1, note=S(4, 'Each correct item 1 mark')),
               pt(S(4, 'print(b != a) True'), 1), pt(S(4, 'print(a > b) True'), 1),
               pt(S(4, 'print(b <= a) True'), 1), pt(S(4, 'print(a == 10) False'), 1),
               pt(S(4, 'print(b != 21) True'), 1)]),
    dict(key=(2, None, None), topic='cs-2-3', total=6,
         replaces='batch 1b: the stem was Q1\'s table; (a)\'s three answers were unpriced '
                  'question-total rows and (b)\'s row welded its direction to "Valid example"',
         why='p3: shipped as the whole of Q2. (a) the difference between a general-purpose '
             'computer and an embedded system, three answers on a 4 / 2 ladder; (b) one '
             'embedded system at home, any valid example 2',
         ask=P(3, '(a) Describe the main difference', 'you might find in your home.'),
         rows=[ladder([S(4, 'General-purpose computers can have many uses', 'limited or specific number of uses'),
                       S(4, 'General-purpose computers can be easily reprogrammed', 'can’t easily be upgraded'),
                       S(4, 'General-purpose computers are generally higher cost', 'relatively low cost')], [[2, 4]],
                      note=S(4, 'Good description – clear understanding demonstrated 4 marks',
                             'Fair description – limited understanding 2 mark')),
               pt(S(4, 'Examples of Embedded Systems can be any digital device', 'dish washers, etc.'), 2,
                  note=S(4, 'Do not accept Micro:bit, Raspberry Pi as valid examples', 'Valid example 2 marks'))]),
    dict(key=(3, None, None), topic='cs-2-2', figure='s-q3', total=6,
         why='p4: an averaging algorithm in pseudocode or a flowchart; the scheme gives both and '
             'prices input 2/1, average 2/1, output 1 and logical order 1',
         ask=P(4, 'Using either a flowchart or pseudocode', 'Print the average of the 3 numbers'),
         rows=[crit(S(5, '3 separate numbers input'), 2, [1],
                    note=S(5, 'Attempt to input number(s) 1 mark OR 3 separate numbers input 2 marks')),
               crit(S(5, 'average calculated correctly'), 2, [1],
                    note=S(5, 'Attempt at calculating average 1 mark OR average calculated correctly 2 marks')),
               pt(S(5, 'Print / output of average'), 1),
               pt(S(5, 'All steps in correct logical order'), 1)]),
    dict(key=(4, None, None), topic='cs-2-3', figure='s-q4', total=6,
         replaces='batch 1b: the rows were lines of working with no marks (a question total) '
                  'and the stem repeated the ask; the answer is now claimable on 6 / 4 / 2',
         why='p4: 14 in binary; the scheme answers 1110 by two workings, 6 / 4 / 2',
         ask=P(4, 'Convert the decimal number 14 to a binary number.'),
         rows=[crit(S(5, 'Ans: 1110'), 6, [2, 4],
                    note=S(5, 'Correct answer 6 marks', 'Any valid conversion 2 marks'))]),
    dict(key=(5, None, None), topic='cs-2-1', qfigure='q5-fig1', total=6,
         replaces='batch 1b: one example was the only answer, all or nothing at 6; the figure '
                  'held the ask and sat on the answer side',
         why='p5: pattern recognition in machine learning, with an example; the scheme gives '
             'three examples, any other relevant one accepted, 6 / 4 / 2',
         ask=P(5, 'The computational thinking skill of pattern recognition', 'might be used by such algorithms.'),
         rows=[ladder([S(6, 'Bicycle – pattern recognition could be used', 'shape, 2 wheels, handlebars.'),
                       S(6, 'Human - pattern recognition could be used', '2 legs, 2 arms, height.'),
                       S(6, 'Car - pattern recognition could be used', '4 wheels, speed of movement.')], [[2, 4, 6]],
                      instruction=S(6, 'Other relevant examples & explanations can be used',
                                    'finger print recognition on finger print scanners.'),
                      note=S(6, 'Valid example and very good description 6 marks',
                             'Valid example OR fair description 2 marks'))]),
    dict(key=(6, None, None), topic='cs-2-4', qfigure='q6-table', total=6,
         why='p5: a data type for five variables; the scheme prints them, the first correct 2 '
             'and each further one 1',
         ask=P(5, 'Flying Fit is a fitness club', 'Float Integer Boolean String List'),
         rows=[anyn([S(6, 'Member Name String'), S(6, 'Member Age Integer'), S(6, 'Amount Paid Float'),
                     S(6, 'Most Popular Days to Visit List'), S(6, 'Member Completed Induction – Yes/No Boolean')],
                    5, 2, steps=[2, 1, 1, 1, 1], head=S(6, 'Variable Description Data Type'),
                    note=S(6, 'First correct item 2 marks', 'Additional correct items 1 mark'))]),
    dict(key=(7, None, None), topic='cs-2-3', total=6,
         replaces='batch 1b: three alternative answers were three rows of 2, so a student could '
                  'not claim 4 or 6 for one answer; the CPU photograph (Figure 2, which the ask '
                  'does not use) was filed as the answer figure and is dropped',
         why='p6: the role of the CPU; the scheme gives three answers, 6 / 4 / 2',
         ask=P(6, 'The Central Processing Unit (CPU) is considered', 'What is the role of the CPU?'),
         rows=[ladder([S(6, 'Process data and instructions and to control the rest of the computer system'),
                       S(6, 'The CPU is often compared to the brain', 'outputs of a computer system'),
                       S(6, 'The CPU processes all data on a computer system', 'fetch, decode, execute cycle')],
                      [[2, 4, 6]],
                      note=S(6, 'Very good explanation - clear understanding demonstrated 6 marks',
                             'Fair explanation - limited understanding 2 mark'))]),
    dict(key=(8, None, None), topic='cs-2-2', total=6,
         replaces='batch 1b: unpriced question-total rows; (b)\'s two answers were separate '
                  'rows; topic was Computer systems',
         why='p6: shipped as the whole of Q8. (a) the first mid item, Dara, 2; (b) why binary '
             'search is divide and conquer, two answers on a 4 / 2 ladder. Filed under '
             'Algorithms (searching), not Computer systems',
         stem=Q8_STEM,
         ask=P(6, '(a) If a binary search algorithm', 'divide and conquer” method?'),
         rows=[pt(S(7, 'Dara'), 2, note=S(7, 'Correct answer 2 marks')),
               ladder([S(7, 'Binary search looks at the middle item', 'nothing left to search.'),
                       S(7, 'Binary search works by dividing the list into two halves', 'repeating this process.')],
                      [[2, 4]],
                      note=S(7, 'Good explanation – clear understanding demonstrated 4 marks',
                             'Fair explanation – limited understanding 2 mark'))]),
    dict(key=(9, None, None), topic='cs-2-4', qfigure='q9-table', total=6,
         why='p7: discrete or continuous for six examples; the scheme prints each, 1 mark',
         ask=P(7, 'Numeric data can be categorised as either discrete data or continuous data.',
               'enter whether it is “discrete” or “continuous” in Column B.'),
         rows=[pt(S(7, 'The number of players in a football squad Discrete'), 1, note=S(7, 'Each correct item 1 mark')),
               pt(S(7, 'The number of students in a class Discrete'), 1),
               pt(S(7, 'The speed of a school bus Continuous'), 1),
               pt(S(7, 'The temperature of a classroom Continuous'), 1),
               pt(S(7, 'The number of days it rained in March Discrete'), 1),
               pt(S(7, 'The weight of a box Continuous'), 1)]),
    dict(key=(10, None, None), topic='cs-2-3', qfigure='q10-fig3', total=6,
         why='p7: the OR truth table; the scheme prints the four rows, 1 correct 2, 2 correct 3, '
             '3 correct 4, all 6',
         ask=P(7, 'Complete the truth table for the OR logic gate, shown below in Figure 3.'),
         rows=[anyn([S(8, '0 0 0'), S(8, '0 1 1'), S(8, '1 0 1'), S(8, '1 1 1')], 4, 2, steps=[2, 1, 1, 2],
                    head=S(8, 'A B out (A OR B)'),
                    instruction=S(8, 'Accept False (for 0) and True (for 1);'),
                    note=S(8, 'Do not accept either A or B as a valid response', 'All correct answers 6 marks'))]),
    dict(key=(11, None, None), topic='cs-2-2', qfigure='q11-code0', total=6,
         replaces='batch 1b: unpriced question-total rows; (c)\'s two answers were separate rows; '
                  'the listing sat on the answer side',
         why='p8: shipped as the whole of Q11. (a) output for 19, Not Graded, 2; (b) output for '
             '110, Distinction, 2; (c) the purpose of int, two answers on a 2 / 1 ladder. The '
             'shipped crop of the 17-line listing was opened and is complete',
         stem=Q11_STEM,
         ask=P(8, '(a) What is the output of the program if the user enters 19', 'in line 1 of the code?'),
         rows=[pt(S(8, 'Not Graded'), 2, note=S(8, 'Correct answer 2 marks')),
               pt(S(8, 'Distinction'), 2),
               ladder([S(8, 'Converts (casts) the text entered to an integer'),
                       S(8, 'Ensures that the datatype of the variable percentage will be an integer')], [[1, 2]],
                      note=S(8, 'Good explanation – clear understanding demonstrated 2 marks',
                             'Fair explanation – limited understanding 1 mark'))]),
    dict(key=(12, None, None), topic='cs-2-3', total=6,
         replaces='batch 1b: one example was the only answer, all or nothing at 6; the other '
                  'three and the accepted list were lost',
         why='p9: two adaptive or assistive technologies, each explained; the scheme lists four '
             'and accepts the others it names, each example 1 and its explanation 2 / 1',
         stem=P(9, 'A community centre is installing a computer suite', 'who may have additional needs.'),
         ask=P(9, 'Suggest two types of adaptive or assistive technology', 'someone with additional needs.'),
         rows=[ladder([S(9, 'Braille keyboard - allows the user', 'for the computer in Braille'),
                       S(9, 'Screen reader - software that enables', 'to use a computer'),
                       S(9, 'Screen magnifier - software that provides', 'for visual impairments'),
                       S(9, 'Sip-and-puff - device that allows users', 'computer system via mouth'),
                       S(9, 'Large monitors.'),
                       S(9, 'Alternative types of keyboard and mouse', 'keyboard with modifications, etc.).'),
                       S(9, 'Accessibility tools built into popular OS', 'keyboard filters, etc.).'),
                       S(9, 'Computers with voice output.'), S(9, 'Word prediction software.'),
                       S(9, 'Adapted pointing/input devices', 'chin pointing devices etc.).'),
                       S(9, 'Wands and sticks.'), S(9, 'Joysticks.'), S(9, 'Trackballs.'),
                       S(9, 'Touch screens.'), S(9, 'Spellchecker')], [[1, 2, 3], [1, 2, 3]],
                      instruction=S(9, 'Accept any other relevant examples and explanations such as,'),
                      note=S(9, 'For each example: Valid example 1 mark',
                             'Fair explanation – limited understanding 1 mark'))]),
    # ── Section B ──────────────────────────────────────────────────────────
    dict(key=(13, 'a', 'i'), topic='cs-2-2', qfigure='q13a-table', total=4,
         replaces='batch 1b: the row was the table header "Column A Column B" worth 4; the four '
                  'terms were never rows; the figure held (ii) as well and sat on the answer side',
         why='p10: the term for four definitions; the scheme tables them, 1 mark each (read '
             'from its cells, where the flat text welds the first definition around its term)',
         ask=P(10, 'Select the correct computer science term', 'Conditional Boolean'),
         rows=[pt(Pair(T(10, 'A data structure that can store a collection of elements of the same data type'),
                       T(10, 'Array')), 1, note=S(10, 'Each correct item 1 mark')),
               pt(Pair(T(10, 'A character that represents a mathematical or logical action'), T(10, 'Operator')), 1),
               pt(Pair(T(10, 'A command for handling a decision'), T(10, 'Conditional')), 1),
               pt(Pair(T(10, 'A memory location that can store a value'), T(10, 'Variable')), 1)]),
    dict(key=(13, 'a', 'ii'), topic='cs-2-2', qfigure='q13a-trace', figure='s-q13a-ii', total=10,
         replaces='batch 1b: the row was the trace table\'s header worth 10; the five rows of the '
                  'trace were never rows; the stem was (i)\'s table',
         why='p10: complete the trace table; the scheme prints rows 2 to 6, each fully correct 2, '
             'two or more items 1 (row: row number, i, j, while i < j, print(i))',
         ask=P(10, 'While loops are used in computer science', 'code being executed.'),
         rows=[crit(S(10, '2 2 9 True 2'), 2, [1],
                    note=S(10, 'Fully correct row 2 marks', 'Row with 2 or more correct items 1 mark')),
               crit(S(10, '3 3 8 True 3'), 2, [1]), crit(S(10, '4 4 7 True 4'), 2, [1]),
               crit(S(10, '5 5 6 True 5'), 2, [1]), crit(S(10, '6 6 5 False 6 or blank'), 2, [1])]),
    dict(key=(13, None, None), topic='cs-2-2', qfigure='q13b-fig4', total=18,
         printed=[S(11, '(b) 12 (3, 3, 3, 3) marks'), S(11, '(i) 6 marks')],
         tariff_note='Q13 prints 38 (14, 12, 12); this card holds (b), 12 (3, 3, 3, 3), and '
                     '(c)(i), 6 of (c)\'s 12 (6, 6) -- (a)(i), (a)(ii) and (c)(ii) have cards of '
                     'their own',
         replaces='batch 1b: shipped as all of Q13 with (a)\'s table and trace as unpriced rows, '
                  'duplicating three other cards, while the asks it alone covers -- (b)(i)-(iv) '
                  'and (c)(i) -- had no answer on it',
         why='p11-12: shipped as the whole of Q13, which covers (b)(i)-(iv) and (c)(i) for the '
             'census. (b) four costs from the Figure 4 flowchart, 3 each; (c)(i) the shortest '
             'charging time with workings, 6 / 4 / 2',
         stem=P(11, 'A public electric car charging point', 'answer the questions that follow.'),
         ask=[P(11, '(i) What cost will be printed', 'this algorithm can print?'),
              P(12, '(c) Three cars arrive at an electric vehicle', 'Show your workings below.')],
         rows=[pt(S(11, '(i) €5'), 3, note=S(11, 'Correct answer 3 marks')),
               pt(S(11, '(ii) €3'), 3), pt(S(11, '(iii) €3'), 3), pt(S(11, '(iv) €2'), 3),
               crit(S(11, 'Car 1 & 2 charge for 30 minutes', 'Ans: 1.5 hours (90 minutes)'), 6, [2, 4],
                    note=S(11, 'Correct answer with workings 6 marks', 'Work of merit 2 marks'))]),
    dict(key=(13, 'c', 'ii'), topic='cs-2-1', total=6,
         replaces='batch 1b: the stem was the bare caption "Figure 5"; name and explanation were '
                  'two all-or-nothing rows of 3 that the scheme prices 2 and 4 / 2; Q13\'s table '
                  'sat on the answer side',
         why='p12: name and explain a computational thinking skill; the scheme gives one '
             'explained and lists the others, named 2 and explained 4 / 2',
         stem=Q13C_STEM,
         ask=P(12, 'Name and explain a computational thinking skill', 'solve this problem.'),
         rows=[ladder([S(11, 'Algorithmic thinking – Algorithmic thinking is when', 'the most effective way to the end goal.'),
                       S(11, 'Decomposition, abstraction, pattern recognition', 'considered computational thinking skills.')],
                      [[2, 4, 6]],
                      note=S(11, 'Valid computational thinking skill named 2 marks',
                             'Fair explanation – limited understanding 2 mark'))]),
    dict(key=(14, 'a', 'i'), topic='cs-1-3', total=6,
         replaces='batch 1b: the row was the heading "Stakeholders" worth 6; the stakeholders '
                  'and end users were never rows; Figure 5 (part (b)\'s) sat on the answer side',
         why='p13: who the stakeholders and end users are; the scheme lists example stakeholders, '
             '2 each to 4, and the end users, 2',
         stem=Q14A_STEM,
         ask=P(13, 'Explain who the stakeholders and end users would be in this project.'),
         rows=[anyn([S(12, 'Irish Government'), S(12, 'commercial investors'), S(12, 'App development team'),
                     S(12, 'RTE staff/management/board'), S(12, 'people who use RTE services'),
                     S(12, 'advertisers')], 2, 2, open_list=True, head=S(12, 'Stakeholders'),
                    note=S(12, 'For each stakeholder identified 2 marks (max. 4 marks)')),
               pt(S(12, 'Members of the public who stream RTE services online or use the app'), 2,
                  head=S(12, 'End Users'),
                  note=[S(12, 'Other relevant end users can be accepted as long as an explanation given'),
                        S(12, 'End user identified 2 marks')])]),
    dict(key=(14, 'a', 'ii'), topic='cs-1-3', total=8,
         replaces='batch 1b: the two example roles were all-or-nothing rows of 4 that the scheme '
                  'prices role 1 and description 3 / 2; the other roles were lost; topic was '
                  'Computer systems',
         why='p13: two roles in a software project, each described; the scheme gives two and '
             'names five more, each role 1 and its description 3 / 2. Filed under Designing '
             'and developing, not Computer systems',
         stem=Q14A_STEM,
         ask=P(13, 'Name and describe two different roles in a software development project such as this.'),
         rows=[ladder([S(12, 'Role 1: Tester Description 1:', 'to look for errors.'),
                       S(12, 'Role 2: Project Manager Description 2:', 'running on time.'),
                       S(12, 'Product Owner'), S(12, 'Business Analyst'), S(12, 'System Analyst'),
                       S(12, 'Designer'), S(12, 'Developer/ Programmer/ Coder')], [[1, 2, 3, 4], [1, 2, 3, 4]],
                      instruction=S(12, 'Accept any relevant role and description.'),
                      note=[S(12, 'Note: Where two separate roles', 'Zero is awarded for the other response.'),
                            S(12, 'Apply marks for each (2) role:', 'Fair description – limited understanding 2 marks')])]),
    dict(key=(14, 'b', 'i'), topic='cs-1-3', qfigure='q14-fig0', total=6,
         replaces='batch 1b: each stage\'s answers were welded into one row of 3 that the scheme '
                  'prices 3 / 2; the stem was "Figure 5 This question continues on the next '
                  'page."; Figure 5 sat on the answer side; topic was Computer systems',
         why='p14: one activity in the Create stage and one in the Document stage; the scheme '
             'lists four for each, 3 / 2 each. The shipped crop of Figure 5 was opened and is '
             'complete. Filed under Designing and developing',
         stem=Q14B,
         ask=P(14, 'Describe one activity that will take place in the Create stage', 'for a project such as this.'),
         rows=[ladder([Pair(S(13, 'Create'), S(13, 'Writing the code to implement the design')),
                       S(13, 'Ongoing testing to ensure the code is working'),
                       S(13, 'Creating databases for storing data'),
                       S(13, 'Creating any physical elements of the project')], [[2, 3]],
                      instruction=S(13, 'Accept any other valid tasks that take place within the create stage.'),
                      note=S(13, 'Good description – clear understanding demonstrated 3 marks',
                             'Fair description – limited understanding 2 mark')),
               ladder([Pair(S(13, 'Document'), S(13, 'Documentation of system requirements for software')),
                       S(13, 'Creation of user guide document'), S(13, 'Creation of user maintenance document'),
                       S(13, 'Creation of frequently asked questions')], [[2, 3]],
                      instruction=S(13, 'Accept any other valid tasks that take place within the document stage.'),
                      note=S(13, 'Good description – clear understanding demonstrated 3 marks',
                             'Fair description – limited understanding 2 mark', nth=2))]),
    dict(key=(14, 'b', 'ii'), topic='cs-1-3', qfigure='q14-fig0', total=6,
         replaces='batch 1b: one advantage was the only answer, all or nothing at 6; the other '
                  'seven were lost; topic was Computer systems',
         why='p14: two advantages of agile or iterative over waterfall; the scheme lists eight, '
             '3 each. Filed under Designing and developing',
         stem=Q14B,
         ask=P(14, 'It is often suggested that an agile or iterative approach', 'over the waterfall approach.'),
         rows=[anyn([S(13, 'Flexibility – short sprint-scrum cycles'), S(13, 'Software is produced early on'),
                     S(13, 'Software is developed in fast cycles'), S(13, 'Each version builds on previous'),
                     S(13, 'Each version is thoroughly tested before release'),
                     S(13, 'Good for small, time-critical projects'), S(13, 'User involvement throughout'),
                     S(13, 'Limited planning is needed to get started')], 2, 3,
                    head=P(14, 'List two advantages of using the agile or iterative approach over the waterfall approach.'),
                    note=S(13, 'Each (2) valid advantage 3 marks'))]),
    dict(key=(14, 'c', 'i'), topic='cs-2-5', total=6,
         replaces='batch 1b: two alternative answers were two rows of 3 that the scheme prices '
                  '6 / 4 for one explanation; Figure 5 sat on the answer side; topic was Algorithms',
         why='p15: explain unit testing; the scheme gives two answers, 6 / 4. Filed under '
             'Evaluation and testing',
         stem=Q14C,
         ask=P(15, 'The developers will conduct unit testing.', 'Explain the term ‘unit testing’.'),
         rows=[ladder([S(13, 'Unit testing is when small/specific sections of code', 'while it is being created'),
                       S(13, 'Unit tests can be carried out on functions / modules of code')], [[4, 6]],
                      note=S(13, 'Very good explanation - clear understanding demonstrated 6 marks',
                             'Fair explanation - limited understanding 4 marks'))]),
    dict(key=(14, 'c', 'ii'), topic='cs-2-5', total=6,
         replaces='batch 1b: each list was welded into one row; Figure 5 sat on the answer side; '
                  'topic was Computer systems',
         why='p15: one advantage and one disadvantage of beta testing; the scheme lists both, '
             '3 each. Filed under Evaluation and testing',
         stem=Q14C,
         ask=P(15, 'Beta testing gives a large number of real users', 'disadvantage of conducting beta testing.'),
         rows=[anyn([S(14, 'Real end users try it out'), S(14, 'Tested by public before release'),
                     S(14, 'Feedback improves product quality'), S(14, 'Chance to find errors/ flaws/ issues before release'),
                     S(14, 'Any other valid advantage')], 1, 3, open_list=True,
                    head=S(14, 'Advantages'), note=S(14, 'Valid advantage 3 marks')),
               anyn([S(14, 'Users can leak information about software before it is released'),
                     S(14, 'Process can be time consuming and delay the release'),
                     S(14, 'Can be a waste of time / money if the Beta testers', 'use the software properly'),
                     S(14, 'Beta testers might not be representative of actual end users'),
                     S(14, 'Any other valid disadvantage')], 1, 3, open_list=True,
                    head=S(14, 'Disadvantages'), note=S(14, 'Valid disadvantage 3 marks'))]),
    dict(key=(15, 'a', 'i'), topic='cs-2-3', total=10,
         replaces='batch 1b: one measure was the only answer, all or nothing at 10; the stem was '
                  '"This question continues on the next page."',
         why='p16: two security measures for the school network; the scheme lists eight and '
             'accepts any other relevant one, 5 each',
         stem=Q15_STEM,
         ask=P(16, 'Recommend two different security measures', 'make their network more secure.'),
         rows=[anyn([S(15, 'User accounts setup with secure passwords'),
                     S(15, 'Restricted accounts so not all users have the same privileges'),
                     S(15, 'Firewall to monitor all data moving in and out of the network'),
                     S(15, 'Use of VPN'), S(15, 'Server is kept in a secure location'),
                     S(15, 'All data is up to date and backed up'),
                     S(15, 'Antivirus/ anti-spyware software installed on the network'),
                     S(15, 'Network policy in place for all users')], 2, 5,
                    head=P(16, 'Recommend two different security measures', 'make their network more secure.'),
                    instruction=S(15, 'Accept any other relevant security measure for a network'),
                    note=S(15, 'Each (2) valid recommendation 5 marks'))]),
    dict(key=(15, 'a', 'ii'), topic='cs-2-3', figure='s-q15a-ii', total=4,
         why='p16: explain the client-server model with a diagram; the scheme gives an example '
             'and prices diagram and explanation 4, either alone 3, some information 2',
         stem=Q15_STEM,
         ask=P(16, 'The school intend to implement a client-server model', 'how the client-server model works.'),
         rows=[crit(S(15, 'Client-server model works by servers', 'in the form of a response.'), 4, [2, 3],
                    note=S(15, 'Clear diagram and explanation 4 marks', 'Some relevant information, not complete 2 marks'))]),
    dict(key=(15, 'b', None), topic='cs-1-2', total=12,
         why='p17: two advantages and two disadvantages of e-Government; the scheme lists both, '
             '3 each',
         ask=P(17, 'Estonia has developed a software system for e-Government.', 'two possible disadvantages of using this system.'),
         rows=[anyn([S(16, 'A centralised system can be more efficient'),
                     S(16, 'Faster/ Less time spent on accessing information'),
                     S(16, 'Less money spent on printing and postage'),
                     S(16, 'Easier for citizens to access / update their information'),
                     S(16, 'Services are more accessible in regard to mobility and/or location')], 2, 3,
                    head=S(16, 'Advantages 6 (3, 3) marks'),
                    instruction=S(16, 'Accept any other relevant point'),
                    note=S(16, 'Each (2) valid advantage 3 marks')),
               anyn([S(16, 'System could be hacked, and data stolen'),
                     S(16, 'If the internet goes down the system isn’t usable'),
                     S(16, 'Digital divide - people with no access', 'are disadvantaged'),
                     S(16, 'Governments have too much information', 'invasion of privacy'),
                     S(16, 'Potential job loses with more reliance on technology')], 2, 3,
                    head=S(16, 'Disadvantages 6 (3, 3) marks'), note=S(16, 'Each (2) valid disadvantage 3 marks'))]),
    dict(key=(15, 'c', None), topic='cs-1-2', total=12,
         why='p18: one technology that benefits society and one that endangers it; the scheme '
             'prints only the criteria, name 1 and explanation 5 / 2 for each',
         stem=P(18, 'Technology is a two-edged sword.', 'It is our decision, and ours alone.'),
         ask=P(18, 'In an article written by Doctor Shelly Batra', 'how it could be a danger to society.'),
         rows=[crit(S(16, 'For each benefit:'), 6, [], parts=[(S(16, 'Name:'), 1, []), (S(16, 'Explanation:'), 5, [2])],
                    note=S(16, 'For each benefit:', 'limited understanding 2 mark')),
               crit(S(16, 'For each danger:'), 6, [], parts=[(S(16, 'Name:', nth=2), 1, []),
                                                            (S(16, 'Explanation:', nth=2), 5, [2])],
                    note=S(16, 'For each danger:', 'limited understanding 2 mark'))]),
    # ── Section C ──────────────────────────────────────────────────────────
    dict(key=(16, 'a', 'i'), topic='cs-2-2', qfigure='q16a-code', figure='s-q16a', total=15,
         replaces='batch 1b: the row was "15 marks Correct response"; filed as Section B; the '
                  'stem was the file-saving instructions; the figure held the ask and sat on the '
                  'answer side',
         why='040 p4: print "Times Table program" first; the scheme marks line 4 #(i), B-15 scale',
         stem=Q16A_STEM,
         ask=C(4, 'Currently the first line that is printed by the program', 'Multiplications of 7 0 7 14 21 28 35 42 49 56 63'),
         rows=[crit(S(17, CORRECT), 15, [5, 10],
                    note=S(17, '(i) 15 marks (B-15 scale)', 'Any other reasonable attempt.'))]),
    dict(key=(16, 'a', 'ii'), topic='cs-2-2', qfigure='q16a-code', figure='s-q16a', total=10,
         why='040 p5: rows of asterisks around the title; the scheme marks lines 3 and 5 #(ii), '
             'B-10 scale',
         stem=Q16A_STEM,
         ask=C(5, 'Update the program so that a row of asterisks appears', 'Multiplications of 7 0 7 14 21 28 35 42 49 56 63'),
         rows=[crit(S(17, 'Correct insertion of row of asterisks in both locations'), 10, [5, 8],
                    note=S(17, '(ii) 10 marks (B-10 scale)', 'Any other reasonable attempt.'))]),
    dict(key=(16, 'a', 'iii'), topic='cs-2-2', qfigure='q16a-code', figure='s-q16a', total=10,
         why='040 p5: read the multiplier from the user; the scheme marks line 7 #(iii), C-10 '
             'scale',
         stem=Q16A_STEM,
         ask=C(5, 'Amend the program to ask for and accept the user\'s choice', '0 8 16 24 32 40 48 56 64 72', end_nth=1),
         rows=[crit(S(18, CORRECT), 10, [3, 5, 7],
                    note=S(18, '(iii) 10 marks (C-10 scale)', 'Any other reasonable attempt.'))]),
    dict(key=(16, 'a', 'iv'), topic='cs-2-2', qfigure='q16a-code', figure='s-q16a', total=5,
         replaces='batch 1b: the row was "semantic error." -- the tail of a scale step; filed as '
                  'Section B; the figure held (i)\'s ask and sat on the answer side',
         why='040 p5: refuse a negative number with a message; the scheme marks lines 8-10 '
             '#(iv), B-5 scale',
         stem=Q16A_STEM,
         ask=C(5, 'Currently the user can enter a negative number.', 'This program does not support negative numbers.'),
         rows=[crit(S(18, CORRECT, nth=2), 5, [2, 3],
                    note=S(18, '(iv) 5 marks (B-5 scale)', 'Any other reasonable attempt.'))]),
    dict(key=(16, 'a', 'v'), topic='cs-2-2', qfigure='q16a-code', figure='s-q16a', total=5,
         why='040 p6: multiply by zero to twelve; the scheme marks line 12 #(v), A-5 scale',
         stem=Q16A_STEM,
         ask=C(6, 'Times tables normally shows the result', '72 80 88 96'),
         rows=[crit(S(18, CORRECT, nth=3), 5, [2],
                    note=S(18, '(v) 5 marks (A-5 scale)', 'Any other reasonable attempt.', nth=1))]),
    dict(key=(16, 'a', 'vi'), topic='cs-2-2', qfigure='q16a-code', figure='s-q16a', total=5,
         replaces='batch 1b: the row was "syntax error." -- the tail of a scale step; filed as '
                  'Section B; the figure held (i)\'s ask and sat on the answer side',
         why='040 p6: print each result as "3 x 8 = 24"; the scheme marks line 13 #(vi), B-5 '
             'scale',
         stem=Q16A_STEM,
         ask=C(6, 'Update the program so that it displays the results in the format', '12 x 8 = 96'),
         rows=[crit(S(19, CORRECT), 5, [2, 3],
                    note=S(19, '(vi) 5 marks (B-5 scale)', 'Any attempt at string concatenation, format function or similar'))]),
    dict(key=(16, 'b', None), topic='cs-2-2', qfigure='q16b-table', figure='s-q16b', total=30,
         replaces='batch 1b: the row was "Possible solution:" worth 30; the rubric was lost; '
                  'filed as Section B; the ask was the instruction to open the file; Q16(a)\'s '
                  'listing sat on the answer side',
         why='040 p7: the temperature alert program; the scheme prints a possible solution and '
             'a rubric of four criteria at three levels, standards and inputs 5 / 4 / 3, logic '
             'and outputs 10 / 7 / 5 (read from its cells)',
         ask=C(7, 'Implement a program for a temperature alert system', 'Temperature is just right.'),
         rows=[crit(T(21, '• Program executes with no syntax or runtime errors', 'Meaningful variable/function names'),
                    5, [3, 4], head=T(21, 'Programming Standards'), note=RUBRIC),
               crit(T(21, '• User correctly prompted to enter a temperature value', 'use of assignment statements'),
                    5, [3, 4], head=T(21, 'Program Inputs')),
               crit(T(21, '• Conditional Logic', 'relational/Boolean operators'),
                    10, [5, 7], head=T(21, 'Program Logic (Processing)')),
               crit(T(21, '• Initial welcome message', 'Too warm. Turn down heating'),
                    10, [5, 7], head=T(21, 'Program Outputs'))]),
]
