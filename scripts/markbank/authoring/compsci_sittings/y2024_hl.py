"""Computer Science 2024 Higher Level: the 3 printed asks the bank did not hold.

50 of the sitting's 53 asks are covered by the cards shipped in August; these
3 complete it. Paper pages 4, 9 and 18-19 and scheme pages 5, 10-11 and 22
were opened. The shipped q12-fig0 (Figure 5's quote) is reused, opened and
complete.
"""
from compsci_lane import (P, S, anyn, crit, crop, pt, stack)  # noqa: F401

CROPS = {
    'q4-figs': stack([('038', 4, (188, 440, 408, 503)), ('038', 4, (188, 541, 408, 599))],
                     ref='2024 HL Q4',
                     alt='Figure 1 (start state): five squares numbered 0 to 4 holding a white disc '
                         'in squares 0 and 1, square 2 empty, and a black disc in squares 3 and 4. '
                         'Figure 2 (end state): black discs in squares 0 and 1, square 2 empty, and '
                         'white discs in squares 3 and 4.'),
    'q15b-fig7': crop('038', 19, (58, 406, 517, 588), ref='2024 HL Q15(b)(i)',
                      alt='Figure 7: the MEMBERS table (member_id 1 Amy, 2 with its name blank, 3 '
                          'Chloe) and the LOANS table (member_id, book_id, date_borrowed): 3, 2, '
                          '20/05/2024; a blank member_id, 4, 01/05/24; 2, 1 and a blank date; and '
                          'a fourth row left blank.'),
    's-q4': crop('scheme', 5, (200, 74, 395, 340), ref='2024 HL Q4', solution=True,
                 alt='The marking scheme\'s solution to Question 4: eight moves from the start '
                     'state, 1 to 2, 3 to 1, 4 to 3, 2 to 4, 0 to 2, 1 to 0, 3 to 1 and 2 to 3, '
                     'each drawn as the row of discs it leaves, ending with the black discs in '
                     'squares 0 and 1 and the white discs in squares 3 and 4.'),
    's-q15b-i': crop('scheme', 22, (57, 285, 516, 440), ref='2024 HL Q15(b)(i)', solution=True,
                     alt='The marking scheme\'s completed tables for Question 15(b)(i), its answers '
                         'in bold: MEMBERS row 2 named Bill; in LOANS the second row\'s member_id '
                         '1, the third row\'s date 18/05/2024, and a fourth row 3, 3, '
                         '15/05/2024.'),
}

MEMBERS = S(22, 'MEMBERS')
LOANS = S(22, 'LOANS')

CARDS = [
    dict(key=(4, None, None), topic='cs-1-1', qfigure='q4-figs', figure='s-q4', total=6,
         why='p4: swap the discs by legal moves; the scheme draws an eight-move solution, full '
             '6, four or more correct steps in order 4, some merit 2',
         ask=[P(4, 'Figure 1 shows a row of black and white discs', 'jumping over a disc in square 2.'),
              P(4, 'Write a sequence of steps, or an algorithm,', 'single disc in each step.')],
         rows=[crit(S(5, 'Full correct solution'), 6, [2, 4],
                    note=S(5, 'Full correct solution 6 marks', 'Response with some merit 2 marks'))]),
    dict(key=(12, 'b', None), topic='cs-1-2', qfigure='q12-fig0', total=3,
         why='p9: one implication of the Figure 5 quote; the scheme lists three, 3 / 2',
         ask=P(9, 'Provide one implication that the quote could have', 'online applications.'),
         rows=[anyn([S(11, 'Privacy - users often share personal information', 'targeted advertising.'),
                     S(11, 'Manipulation of attention', 'negative impact on mental health.'),
                     S(11, 'Responsible use - on a positive note', 'reading terms and conditions.')], 1, 3,
                    head=P(9, 'Provide one implication that the quote could have', 'online applications.'),
                    note=S(11, 'Very good explanation - clear understanding demonstrated 3 marks',
                           'Fair explanation – limited understanding 2 mark'))]),
    dict(key=(15, 'b', 'i'), topic='cs-3-1', qfigure='q15b-fig7', figure='s-q15b-i', total=6,
         why='p19: six empty cells from three loans; the scheme prints the completed tables, 1 '
             'per cell (the fourth LOANS row holds three)',
         stem=P(19, 'Alex has decided to build a relational database', 'Green Eggs and Ham on 20th May 2024.'),
         ask=P(19, 'Use the information provided below to fill in', 'Horton Hears a Who! 7 days ago.'),
         rows=[pt(S(22, '2 Bill'), 1, head=MEMBERS, note=S(22, 'Each correct response 1 mark', nth=2)),
               pt(S(22, '1 4 01/05/24'), 1, head=LOANS),
               pt(S(22, '2 1 18/05/2024'), 1, head=LOANS),
               crit(S(22, '3 3 15/05/2024'), 3, [1, 2], head=LOANS)]),
]
