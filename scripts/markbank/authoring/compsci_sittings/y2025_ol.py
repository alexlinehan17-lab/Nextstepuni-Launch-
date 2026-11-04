"""Computer Science 2025 Ordinary Level: the 8 printed asks the bank did not hold.

34 of the sitting's 42 asks are covered by the cards shipped in August; these
8 complete it. Paper pages 3, 5, 7, 9 and Section C pages 4-5, and scheme
pages 4, 6, 7, 8 and 20-21 were opened.

Q9's scheme prints its six answers as a bare list ("• False • False • True •
True • True • False") with no wording of its own, so each answer is paired
with the paper's statement by printed ORDER; both documents print six, and
the scheme page shows the list set beside nothing else.
"""
from compsci_lane import (C, P, Pair, S, anyn, crit, crop, pt, stack)  # noqa: F401

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
    'q16a-code': crop('040', 4, (76, 349, 541, 505), ref='2025 OL Q16(a)',
                      alt='The eleven-line program Question16_A.py as printed in the Section C '
                          'booklet: two comment lines, print("The program"), length = '
                          'float(input("What length is the room?: ")), width = 20, area = length '
                          '* width, and print("The area of the floor is:", area).'),
    's-q16a': crop('scheme', 20, (52, 154, 563, 467), ref='2025 OL Q16(a)', solution=True,
                   alt='The marking scheme\'s possible solution to Question 16(a), lines 1 to 27: '
                       'print("Welcome to the Tilers Mate") marked (i); the width read with '
                       'float(input()) marked (iii); cost_per_square_metre = 15 marked (iv); the '
                       'length and width printed in metres, marked (ii) and (iii); the cost per '
                       'square metre printed, (iv); the total cost calculated and printed, (v); '
                       'and the discount messages for totals over 1000, from 100 to 1000, and '
                       'below 100, (vi).'),
}

Q16A_STEM = C(4, 'The program below is the start of a program to help floor tilers', 'total area of the floor.')
CORRECT = S(20, 'Correct implementation using solution above or similar.')

CARDS = [
    dict(key=(1, None, None), topic='cs-2-2', qfigure='q1-code', total=6,
         why='p3: the output for six ages; the scheme prints each, 1 mark',
         ask=[P(3, 'The Python program below takes a person’s age', 'value entered for the person’s age.'),
              P(3, 'For each value in Column A', 'in Column B.')],
         rows=[pt(S(4, '21 A'), 1, note=S(4, 'Each correct item 1 mark', nth=1)),
               pt(S(4, '-1 B'), 1), pt(S(4, '0 B'), 1), pt(S(4, '16 C'), 1),
               pt(S(4, '100 A'), 1), pt(S(4, '15 B'), 1)]),
    dict(key=(5, None, None), topic='cs-2-4', qfigure='q5-code', total=6,
         why='p5: the data type of five variables; the scheme prints them, all correct 6 or '
             'each correct 1, so the fifth correct is worth 2',
         ask=P(5, 'There are a number of variable declarations', 'integer float bool list string'),
         rows=[anyn([S(6, 'name string'), S(6, 'age integer'), S(6, 'student bool'),
                     S(6, 'exam_marks list'), S(6, 'average_mark float')], 5, 1, steps=[1, 1, 1, 1, 2],
                    head=S(6, 'Column A Column B Variable Python Data Type'),
                    note=S(6, 'All correct 6 marks or Each correct item 1 mark'))]),
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
    dict(key=(11, None, None), topic='cs-2-2', qfigure='q11-boxes', total=6,
         why='p9: the list after swaps 1 to 4 of a selection sort; the scheme prints each, all '
             'rows 6, three 4, two 3, one 2',
         ask=P(9, 'A selection sort (simple sort), which repeatedly selects', 'List = [13, 54, 4, 81, 92, 26]'),
         rows=[anyn([S(8, 'Swap 1 4 54 13 81 92 26'), S(8, 'Swap 2 4 13 54 81 92 26'),
                     S(8, 'Swap 3 4 13 26 81 92 54'), S(8, 'Swap 4 4 13 26 54 92 81')], 4, 2, steps=[2, 1, 1, 2],
                    head=S(8, 'Question 11 Initial state 13 54 4 81 92 26'),
                    note=S(8, 'All rows correct 6 marks', '1 row correct 2 marks'))]),
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
]
