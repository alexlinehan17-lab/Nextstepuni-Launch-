"""Computer Science 2023 Higher Level: the 10 printed asks the bank did not hold.

46 of the sitting's 56 asks are covered by the cards shipped in August; these
10 complete it. Paper pages 6-8, 13, 15 and 19 and scheme pages 8-9, 13, 15
and 20 were opened. Q8's and Q9's parts carry no tariff of their own on a
row; their prices are quoted from the question head ("1+4(2,2)+1 marks",
"4+2 marks"), checked against each part's own "Correct response" line.
Q13(b)(i)'s routes print Wingdings arrows, folded as in 2026 HL.
"""
from compsci_lane import (P, S, anyn, crit, crop, pt, stack)  # noqa: F401

CROPS = {
    'q7-code': stack([('038', 6, (52, 455, 542, 544)), ('038', 6, (230, 557, 366, 665))],
                     ref='2023 HL Q7',
                     alt='The six-line Python program printed with Question 7 (x = 10, y = 5, then '
                         'while x >= y: x = x - 1 and y = y + 1), above the trace table with '
                         'columns x and y whose first row is filled in as 10 and 5 and whose '
                         'other rows are blank.'),
    'q8-fig3': crop('038', 7, (430, 75, 530, 205), ref='2023 HL Q8',
                    alt='Figure 3: a drawing of a farmer rowing a small boat, with a wolf, a goat '
                        'and a cabbage.'),
    'q9-fig4': crop('038', 8, (104, 134, 491, 246), ref='2023 HL Q9',
                    alt='Figure 4: three moves of three cups in positions 1, 2 and 3. Move A '
                        'swaps the cups in positions 1 and 2, move B swaps the cups in positions 1 '
                        'and 3, and move C swaps the cups in positions 2 and 3.'),
    'q13b-fig8': crop('038', 13, (350, 342, 565, 471), ref='2023 HL Q13(b)',
                      alt='Figure 8: four hubs A, B, C and D joined by roads with distances in '
                          'kilometres: A to C 15, A to B 20, A to D 15, B to C 25, B to D 30 and '
                          'C to D 35.'),
    'q14a-fig10': crop('038', 15, (120, 439, 512, 558), ref='2023 HL Q14(a)(ii)',
                       alt='Figure 10: the CPU cycle drawn as three boxes in a loop, the first '
                           'labelled Fetch Instruction and the next two left blank, labelled (a) '
                           'and (b).'),
    'q15b-code': crop('038', 19, (52, 73, 557, 331), ref='2023 HL Q15(b)',
                      alt='The sixteen-line binary_search1(v, L) function printed with Question '
                          '15(b): lo = 0 and hi = len(L) - 1; while lo <= hi it sets mid = (lo + '
                          'hi)//2, sets hi = mid - 1 if L[mid] > v, lo = mid + 1 if L[mid] < v, '
                          'and otherwise returns mid on line 14; line 16 returns len(L).'),
    's-q9a': crop('scheme', 9, (52, 92, 545, 223), ref='2023 HL Q9(a)', solution=True,
                  alt='The marking scheme\'s working for Question 9(a): a table of the cups and '
                      'the ball\'s position before and after each move of A, B, C, B, C, A, the '
                      'ball ending at position 2.'),
}

Q8_STEM = P(7, 'A farmer needs to ferry a wolf', '(E, E, E, E) is the initial state of the system.')
Q8_B = P(7, 'The state (W, E, E, W) is considered a loss state', 'both on the west side).')
Q8_TARIFF = S(8, 'Question 8 1+4(2,2)+1 marks')
Q9_STEM = P(8, 'Chop Cup is a magic routine', 'the right cup is at position 3.')
Q9_TARIFF = S(9, 'Question 9 4+2 marks')

CARDS = [
    dict(key=(7, None, None), topic='cs-2-2', qfigure='q7-code', total=6,
         why='p6: a trace table; the scheme prints the three rows to fill, each correct '
             'response 1 mark',
         ask=P(6, 'Complete the trace table for the Python code shown below.'),
         rows=[crit(S(8, '9 6'), 2, [1], note=S(8, 'Each correct response 1 mark', nth=1)),
               crit(S(8, '8 7'), 2, [1]), crit(S(8, '7 8'), 2, [1])]),
    dict(key=(8, 'a', None), topic='cs-1-1', qfigure='q8-fig3', total=1, printed=Q8_TARIFF,
         why='p7: the final state; the scheme prints (W, W, W, W), 1 mark',
         stem=Q8_STEM,
         ask=P(7, 'Using this notation, what is the desired final state of the system?'),
         rows=[pt(S(8, '(W, W, W, W)'), 1)]),
    dict(key=(8, 'b', 'i'), topic='cs-1-1', qfigure='q8-fig3', total=4, printed=Q8_TARIFF,
         why='p7: two other loss states; the scheme lists five (the one given in the question '
             'earns nothing), 2 each',
         stem=[Q8_STEM, Q8_B],
         ask=P(7, 'Using this notation, name any other two loss states.'),
         rows=[anyn([S(8, '(E, E, W, W)'), S(8, '(E, W, W, E)'), S(8, '(E, W, W, W)'),
                     S(8, '(W, E, E, E)'), S(8, '(W, W, E, E)')], 2, 2,
                    head=P(7, 'Using this notation, name any other two loss states.'),
                    note=S(8, '(W, E, E, W) – No marks awarded', 'Each correct response 2 marks'))]),
    dict(key=(8, 'b', 'ii'), topic='cs-1-1', qfigure='q8-fig3', total=1, printed=Q8_TARIFF,
         why='p7: one non-loss state; the scheme lists eight, any one 1 mark',
         stem=[Q8_STEM, Q8_B],
         ask=P(7, 'Using this notation, name any one non-loss state', 'initial and final states.'),
         rows=[anyn([S(8, '(E, E, E, W)'), S(8, '(E, E, W, E)'), S(8, '(E, W, E, E)'), S(8, '(E, W, E, W)'),
                     S(8, '(W, E, W, E)'), S(8, '(W, E, W, W)'), S(8, '(W, W, E, W)'), S(8, '(W, W, W, E)')],
                    1, 1, head=P(7, 'Using this notation, name any one non-loss state', 'initial and final states.'),
                    note=S(8, 'Any correct response 1 mark'))]),
    dict(key=(9, 'a', None), topic='cs-1-1', qfigure='q9-fig4', figure='s-q9a', total=4,
         printed=Q9_TARIFF,
         why='p8: the ball\'s position after ABCBCA; the scheme works it and prints 2, 4 / 2 / 1',
         stem=Q9_STEM,
         ask=P(8, 'Given that the ball starts under the leftmost cup', 'the sequence of moves, ABCBCA.'),
         rows=[crit(S(9, 'Answer: The ball position after ABCBCA is 2', '(i.e. under the middle cup).'),
                    4, [1, 2], note=S(9, 'Correct 4 marks', 'Response with some merit 1 mark'))]),
    dict(key=(9, 'b', None), topic='cs-1-1', qfigure='q9-fig4', total=2, printed=Q9_TARIFF,
         why='p8: a sequence of three or more moves that returns the ball; the scheme lists '
             'the four-move sequences and two rules, 2 marks',
         stem=Q9_STEM,
         ask=P(8, 'Without knowing which cup the ball is under', 'the same position as it started from.'),
         rows=[anyn([S(9, 'The complete list of 4 move sequences that work is:', "'CCBB', 'CCCC']"),
                     S(9, 'Any ‘same move’ completed an even number of times', 'BBBBBB'),
                     S(9, 'Any palindromic sequence of moves e.g. ABBA, ABCCBA'),
                     S(9, 'Any other correct response')], 1, 2, open_list=True,
                    head=P(8, 'construct a sequence involving at least three moves', 'as it started from.'),
                    note=S(9, 'Note: Odd length sequences will not work', 'Correct response 2 marks'))]),
    dict(key=(13, 'b', 'i'), topic='cs-1-1', qfigure='q13b-fig8', total=2,
         why='p13: the shortest round trip from Hub A; the scheme prints 85 km by either '
             'direction, 2 / 1',
         stem=P(13, 'Figure 8 shows the set of hubs and distances', 'before returning to Hub A.'),
         ask=P(13, 'Calculate and state the shortest possible route the technician should take.'),
         rows=[crit(S(13, '85 km Hub A', '(15+30+25+15 = 85)'), 2, [1],
                    note=S(13, 'Correct response 2 mark', 'Response with some merit 1 mark'))]),
    dict(key=(14, 'a', 'i'), topic='cs-2-3', total=4,
         why='p15: explain output device and give two examples; the scheme prices the '
             'description 2 / 1 and each example 1',
         ask=P(15, 'Explain the term ‘output device’. Provide two examples.'),
         rows=[crit(S(15, 'Any piece of hardware used to convey information from the computer to the user'),
                    2, [1], note=S(15, 'Very good description - clear understanding demonstrated 2 marks',
                                   'Fair description – limited understanding 1 mark')),
               anyn([S(15, 'screen/monitor'), S(15, 'printer/plotter'), S(15, 'speaker/headphones'),
                     S(15, 'web cam'), S(15, 'secondary storage devices')], 2, 1, open_list=True,
                    head=P(15, 'Provide two examples.'),
                    note=S(15, 'For each correct example: Valid output device 1 mark'))]),
    dict(key=(14, 'a', 'ii'), topic='cs-2-3', qfigure='q14a-fig10', total=2,
         why='p15: the two steps after Fetch Instruction; the scheme prints Decode and Execute, '
             '1 each',
         ask=P(15, 'The CPU cycle carried out to process data and instructions', 'labelled (a) and (b).'),
         rows=[pt(S(15, '(a) Decode'), 1,
                  note=S(15, 'For each correct response 1 marks', 'correct names in the wrong order')),
               pt(S(15, '(b) Execute'), 1)]),
    dict(key=(15, 'b', 'iii'), topic='cs-2-2', qfigure='q15b-code', total=3,
         why='p19: why line 16 returns len(L); the scheme answers it, 3 / 2',
         stem=P(19, 'The Python code below shows an implementation of a binary search function.'),
         ask=P(19, 'Explain the reason for len(L) on line 16.'),
         rows=[crit(S(20, 'It is used to indicate that the value has not been found.'), 3, [2],
                    note=S(20, 'Very good explanation - clear understanding demonstrated 3 marks',
                           'Fair explanation - limited understanding 2 marks', nth=3))]),
]
