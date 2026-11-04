"""Computer Science 2023 Ordinary Level: the 10 printed asks the bank did not hold.

31 of the sitting's 41 asks are covered by the cards shipped in August; these
10 complete it. Paper pages 4-5, 7, 16-18 and Section C pages 4-6, and scheme
pages 5-8, 15-18 were opened.

Q15(c) is answered in the scheme by its marking criteria alone (name 1,
explanation 5 / 2, for the benefit and for the danger), with no example
technology; the card carries those criteria as the components the student
places marks on, in the scheme's own words.
"""
from compsci_lane import (C, P, S, anyn, crit, crop, pt, stack)  # noqa: F401

CROPS = {
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
    'q16a-code': crop('040', 4, (76, 341, 540, 497), ref='2023 OL Q16(a)',
                      alt='The eleven-line program Question16_A.py as printed in the Section C '
                          'booklet: two comment lines, print("Multiplication program"), number = '
                          '7, print("Multiplications of ", number), then for i in range(10): '
                          'print(number*i).'),
    's-q3': crop('scheme', 5, (52, 74, 545, 442), ref='2023 OL Q3', solution=True,
                 alt='The marking scheme\'s examples for Question 3. Pseudocode: input num1, input '
                     'num2, input num3, average = (num1 + num2 + num3) /3, print average. A '
                     'flowchart that does the same: Start, three inputs, the average calculated, '
                     'the average output, Stop.'),
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
}

Q15_STEM = P(16, 'A local school stores student details on their computer network.', 'information held on the network.')
Q16A_STEM = C(4, 'The program below produces a times table', 'ten times in total.')

CARDS = [
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
    dict(key=(6, None, None), topic='cs-2-4', qfigure='q6-table', total=6,
         why='p5: a data type for five variables; the scheme prints them, the first correct 2 '
             'and each further one 1',
         ask=P(5, 'Flying Fit is a fitness club', 'Float Integer Boolean String List'),
         rows=[anyn([S(6, 'Member Name String'), S(6, 'Member Age Integer'), S(6, 'Amount Paid Float'),
                     S(6, 'Most Popular Days to Visit List'), S(6, 'Member Completed Induction – Yes/No Boolean')],
                    5, 2, steps=[2, 1, 1, 1, 1], head=S(6, 'Column A Column B Variable Description Data Type'),
                    note=S(6, 'First correct item 2 marks', 'Additional correct items 1 mark'))]),
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
                    note=S(8, 'Accept False (for 0) and True (for 1)', 'All correct answers 6 marks'))]),
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
                     S(16, 'Services are more accessible in regard to mobility and/or location'),
                     S(16, 'Accept any other relevant point')], 2, 3, head=S(16, 'Advantages 6 (3, 3) marks'),
                    open_list=True, note=S(16, 'Each (2) valid advantage 3 marks')),
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
         rows=[crit(S(18, 'Correct implementation using solution above or similar.'), 10, [3, 5, 7],
                    note=S(18, '(iii) 10 marks (C-10 scale)', 'Any other reasonable attempt.'))]),
    dict(key=(16, 'a', 'v'), topic='cs-2-2', qfigure='q16a-code', figure='s-q16a', total=5,
         why='040 p6: multiply by zero to twelve; the scheme marks line 12 #(v), A-5 scale',
         stem=Q16A_STEM,
         ask=C(6, 'Times tables normally shows the result', '72 80 88 96'),
         rows=[crit(S(18, 'Correct implementation using solution above or similar.', nth=3), 5, [2],
                    note=S(18, '(v) 5 marks (A-5 scale)', 'Any other reasonable attempt.', nth=1))]),
]
