"""Computer Science 2021 Ordinary Level: the 4 printed asks the bank did not hold.

32 of the sitting's 36 asks are covered by the cards shipped in August; these
4 complete it. Paper pages 3, 7-8 and scheme pages 4 and 7 were opened.
Q1's scheme table sets its two columns so that the flat text interleaves them
("a = 5 Integer String b = ..."); its cells are read with find_tables (cells
block, page 4). The census flags Q10(a) and (b) as empty leaves ("x = 21",
"x = 3"): each IS the ask, a value of x under the paper's shared question, and
is carded with it.
"""
from compsci_lane import (P, Pair, S, T, anyn, crit, crop, pt, stack)  # noqa: F401

CROPS = {
    'q1-table': crop('038', 3, (70, 228, 525, 446), ref='2021 OL Q1',
                     alt='The table printed with Question 1: Column A lists the assignments a = 5, '
                         'b = "Hello World", c = True, d = ["apple", "banana", "orange"] and e = '
                         '2.718; Column B (Data Type) is blank.'),
    'q9-code': stack([('038', 7, (52, 118, 542, 222)), ('038', 7, (159, 245, 465, 424)),
                      ('038', 7, (52, 447, 542, 494))],
                     ref='2021 OL Q9',
                     alt='The seven-line Python program printed with Question 9 (a = 1, b = 2, '
                         'while a < 4: a = a + 1, b = b + a, then print(b)), above the trace table '
                         'with columns Step, a, b and a < 4; step 1 is filled in as 1, 2, True and '
                         'steps 2 to 4 and the Output box below it are blank.'),
    'q10-algo': crop('038', 8, (53, 120, 543, 277), ref='2021 OL Q10',
                     alt='The linear search algorithm printed with Question 10, for a list L and '
                         'a value x: Step 1 set i to 0; Step 2 set n to the number of items in L; '
                         'Step 3 if i >= n go to Step 8; Step 4 if L[i] = x go to Step 7; Step 5 '
                         'set i to i + 1; Step 6 go to Step 3; Step 7 print position i and go to '
                         'Step 9; Step 8 print "item not found"; Step 9 exit.'),
}

Q10_STEM = P(8, 'The linear search algorithm shown below is to be applied', 'L = [10, 25, 21, 15, 85, 69, 74, 22, 19, 6]')
Q10_ASK = P(8, 'What is the output of this algorithm', 'the following values of x?')

CARDS = [
    dict(key=(1, None, None), topic='cs-2-4', qfigure='q1-table', total=5,
         why='p3: a data type for five assignments; the scheme\'s table pairs them, 1 each',
         ask=P(3, 'Choose the appropriate Python data type', 'Float Boolean Integer String List'),
         rows=[pt(Pair(T(4, 'a = 5'), T(4, 'Integer')), 1, note=S(4, 'Each correct item 1 mark')),
               pt(Pair(T(4, 'b = "Hello World"'), T(4, 'String')), 1),
               pt(Pair(T(4, 'c = True'), T(4, 'Boolean')), 1),
               pt(Pair(T(4, 'd = ["apple", "banana", "orange"]'), T(4, 'List')), 1),
               pt(Pair(T(4, 'e = 2.718'), T(4, 'Float')), 1)]),
    dict(key=(9, None, None), topic='cs-2-2', qfigure='q9-code', total=5,
         printed=S(7, 'Question 9 3+2 marks'), tariff_note='3 for the trace table and 2 for the output',
         why='p7: a trace table and the output; the scheme prints the rows (each row or column 1, '
             'max 3) and the output 11 (2)',
         ask=P(7, 'Complete the trace table below to determine the output', 'completed for you.'),
         rows=[crit(S(7, '2 2 4 True', '4 4 11 False'), 3, [1, 2],
                    note=S(7, 'Each correct row/column 1 mark (max 3 marks)', 'Any one value correct 1 mark (total)')),
               pt(S(7, 'Answer: 11'), 2, note=S(7, 'Correct output 2 marks'))]),
    dict(key=(10, 'a', None), topic='cs-2-2', qfigure='q10-algo', total=3,
         printed=S(7, 'Question 10 3 + 2 marks'),
         why='p8: the output when searching for 21; the scheme prints 2',
         stem=Q10_STEM, ask=[Q10_ASK, P(8, 'x = 21')],
         rows=[pt(S(7, 'Answer: 2'), 3, note=S(7, 'Both correct 5 marks Any one correct 3 marks'))]),
    dict(key=(10, 'b', None), topic='cs-2-2', qfigure='q10-algo', total=2,
         printed=S(7, 'Question 10 3 + 2 marks'),
         why='p8: the output when searching for 3; the scheme prints item not found',
         stem=Q10_STEM, ask=[Q10_ASK, P(8, 'x = 3')],
         rows=[pt(S(7, 'Answer: item not found'), 2, note=S(7, 'Both correct 5 marks Any one correct 3 marks'))]),
]
