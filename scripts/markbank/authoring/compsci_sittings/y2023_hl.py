"""Computer Science 2023 Higher Level: all 56 printed asks, re-authored part by part.

39 cards shipped in August out of the automatic author; batch 1b rebuilds each
of them here, keeping its id, from lifts of the paper and the scheme, and the
10 residue cards sit among them in printed order. Paper pages 3-20 and Section
C pages 4-9, and scheme pages 3-26 were opened.

Seven shipped cards are whole short questions with parts and no part cards
beside them (Q2, Q3, Q4, Q6, Q10, Q11, Q12). They stay whole (coordinator,
5 Nov): the ask is each part's printed ask with its label, every row is tied to
its part with ofpart() and the paper's own "(a)" / "(b)", and the rows sum to
the question's 6.

Q8's and Q9's parts carry no tariff of their own on a row; their prices are
quoted from the question head ("1+4(2,2)+1 marks", "4+2 marks"), checked
against each part's own "Correct response" line. Q13(b)(i)'s routes print
Wingdings arrows, folded as in 2026 HL.

Shipped crops reused on the question side, each opened and clean: q1-fig0,
q11-fig0 (Figure 6), q12-fig0 (Figure 7), q15-fig0 (the time-complexity table)
and the curated q10-figure (Figure 5's list, pinned in figures-computer-
science.json, reused unchanged with no CROPS entry). q3-figure and q13-fig0
carry the paper's prose, and q16-figure the prose above the listing, so those
questions have crops of their own. Q16(b)'s rubric is read from the cells of
scheme page 26.
"""
from compsci_lane import (C, G, GAt, P, Pair, S, T, anyn, crit, crop, ladder, ofpart, pt, stack, unprinted)  # noqa: F401

LISTING16 = ('040', 4, (60, 441, 568, 721))

CROPS = {
    's-q2b': crop('scheme', 4, (80, 593, 420, 660), ref='2023 HL Q2(b)', solution=True,
                  alt='The marking scheme\'s two conversions for Question 2(b): C x 16 to the power '
                      '1 + 9 x 16 to the power 0 = 12 x 16 + 9 x 1 = 192 + 9 = 201; OR step 1, C9 = '
                      '1100 1001 in binary, step 2, 1100 1001 = 128 + 64 + 8 + 1 = 201.'),
    'q3-figs': stack([('038', 4, (205, 107, 390, 290)), ('038', 4, (160, 333, 435, 452)),
                      ('038', 4, (200, 502, 395, 697))], ref='2023 HL Q3',
                     alt='Figure 1: an x-y axis through (0, 0) with a point P(x, y) in the top right '
                         'quadrant. Below it, the truth table of part (a), columns x > 0, y > 0 and '
                         'x > 0 and y > 0: its first row is False False False; the next three rows '
                         'give False True, True False and True True with the last column blank. '
                         'Then Figure 2: the same axes with a shaded square in the top left '
                         'quadrant between (-d, d) and (0, 0).'),
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
    's-q9a': crop('scheme', 9, (52, 92, 545, 223), ref='2023 HL Q9(a)', solution=True,
                  alt='The marking scheme\'s working for Question 9(a): a table of the cups and '
                      'the ball\'s position before and after each move of A, B, C, B, C, A, the '
                      'ball ending at position 2.'),
    'q13b-fig8': crop('038', 13, (350, 342, 565, 471), ref='2023 HL Q13(b)',
                      alt='Figure 8: four hubs A, B, C and D joined by roads with distances in '
                          'kilometres: A to C 15, A to B 20, A to D 15, B to C 25, B to D 30 and '
                          'C to D 35.'),
    'q14a-fig10': crop('038', 15, (120, 439, 512, 558), ref='2023 HL Q14(a)(ii)',
                       alt='Figure 10: the CPU cycle drawn as three boxes in a loop, the first '
                           'labelled Fetch Instruction and the next two left blank, labelled (a) '
                           'and (b).'),
    's-q15a-iv': crop('scheme', 19, (110, 298, 480, 382), ref='2023 HL Q15(a)(iv)', solution=True,
                      alt='The marking scheme\'s completed table for Question 15(a)(iv): Linear '
                          'Search, best case O(1), worst case O(N); Binary Search, best case O(1), '
                          'worst case O(log2 N), the 2 written as a subscript.'),
    'q15a-names': crop('038', 18, (55, 137, 510, 168), ref='2023 HL Q15(a)',
                       alt='The list of seven names printed with Question 15(a), in boxes: Amir, Dean, '
                           'Eoin, Helen, Natalia, Steve, Terry.'),
    'q15b-code': crop('038', 19, (52, 73, 557, 331), ref='2023 HL Q15(b)',
                      alt='The sixteen-line binary_search1(v, L) function printed with Question '
                          '15(b): lo = 0 and hi = len(L) - 1; while lo <= hi it sets mid = (lo + '
                          'hi)//2, sets hi = mid - 1 if L[mid] > v, lo = mid + 1 if L[mid] < v, '
                          'and otherwise returns mid on line 14; line 16 returns len(L).'),
    'q15c-code': crop('038', 20, (56, 74, 553, 267), ref='2023 HL Q15(c)',
                      alt='The thirteen-line recursive function binary_search2(v, L, lo, hi) '
                          'printed with Question 15(c): if lo > hi it returns len(L); mid = (lo + '
                          'hi)//2; if L[mid] > v it returns binary_search2(v, L, lo, mid-1), elif '
                          'L[mid] < v it returns binary_search2(v, L, mid+1, hi); otherwise it '
                          'returns mid.'),
    'q16a-code': crop(*LISTING16, ref='2023 HL Q16(a)',
                      alt='The nineteen-line program Question16_A.py as printed in the Section C '
                          'booklet: from random import randint; def guess_game(max_guesses_allowed) '
                          'sets secret_number = randint(1, 5), guess_count = 0 and user_guess = 0, '
                          'then while user_guess != secret_number reads a guess, adds 1 to '
                          'guess_count and prints Congratulations! You win! on a match; then '
                          'print("Welcome to the guessing game!") and guess_game(3).'),
    's-q16a-i': crop('scheme', 22, (55, 478.5, 565, 489.5), ref='2023 HL Q16(a)(i)', solution=True,
                     alt='Line 31 of the marking scheme\'s possible solution: print("You took", '
                         'guess_count, "guesses") # (i).'),
    's-q16a-ii': crop('scheme', 22, (55, 489, 565, 551), ref='2023 HL Q16(a)(ii)', solution=True,
                      alt='Lines 32 to 37 of the marking scheme\'s possible solution, between # (ii) '
                          '- start and # (ii) - end: elif user_guess < secret_number prints Sorry! '
                          'Your guess was too low, else Sorry! Your guess was too high.'),
    's-q16a-iii': crop('scheme', 22, (55, 335, 565, 357), ref='2023 HL Q16(a)(iii)', solution=True,
                       alt='Line 18 of the marking scheme\'s possible solution: while (user_guess != '
                           'secret_number) and (guess_count < max_guesses_allowed): # (iii).'),
    's-q16a-iv': crop('scheme', 22, (55, 570.5, 565, 612), ref='2023 HL Q16(a)(iv)', solution=True,
                      alt='Lines 40 to 43 of the marking scheme\'s possible solution, between # (iv) '
                          '- start and # (iv) - end: num_guesses_allowed = int(input("Enter the '
                          'maximum number of guesses allowed: ")), then '
                          'guess_game(num_guesses_allowed).'),
    's-q16a-v': crop('scheme', 22, (55, 221, 565, 297), ref='2023 HL Q16(a)(v)', solution=True,
                     alt='Lines 7 to 13 of the marking scheme\'s possible solution, between # (v) - '
                         'start and # (v) - end: difficulty is read; if difficulty.upper() == "H" '
                         'secret_number = randint(1, 100), else randint(1, 5).'),
    's-q16a-vi': stack([('scheme', 22, (55, 315.5, 565, 327)), ('scheme', 22, (55, 395, 565, 449))],
                       ref='2023 HL Q16(a)(vi)', solution=True,
                       alt='Lines 16 and 23 to 27 of the marking scheme\'s possible solution: '
                           'guesses = [] # (vi); then, between # (vi) - start and # (vi) - end, if '
                           'user_guess in guesses print You already guessed this number., and '
                           'guesses.append(user_guess).'),
    'q16b-output': crop('040', 9, (94, 70, 531, 359), ref='2023 HL Q16(b)',
                        alt='The example output printed with Question 16(b): four rounds. Guess 35, '
                            'secret number 31, difference 4, You score 20 points, total 20; guess '
                            '91, secret 6, difference 85, You lose 30 points, total -10; guess 54, '
                            'secret 54, difference 0, JACKPOT!!! You score 100 points, total 90; '
                            'guess 50, secret 28, difference 22, total 90; each round ends Play '
                            'again? (Y/N):, answered Y, Y, Y and N.'),
    's-q16b': crop('scheme', 25, (55, 103, 565, 516), ref='2023 HL Q16(b)', solution=True,
                   alt='The marking scheme\'s 37-line possible solution for Question 16(b): '
                       'user_score = 0; in a while True loop a secret number randint(1, 100) is '
                       'generated and a guess read; difference = abs(user_guess-secret_number) is '
                       'printed with both numbers; an exact guess adds 100 (JACKPOT!!! You score '
                       '100 points), a difference under 20 adds 20, over 30 subtracts 30; the total '
                       'is printed and the loop breaks unless Play again? is answered y.'),
}

Q8_STEM = P(7, 'A farmer needs to ferry a wolf', '(E, E, E, E) is the initial state of the system.')
Q8_B = P(7, 'The state (W, E, E, W) is considered a loss state', 'both on the west side).')
Q8_TARIFF = S(8, 'Question 8 1+4(2,2)+1 marks')
Q9_STEM = P(8, 'Chop Cup is a magic routine', 'the right cup is at position 3.')
Q9_TARIFF = S(9, 'Question 9 4+2 marks')
Q13 = P(12, 'The National Hub Network is an initiative', 'rural and remote areas.')
Q13B = [Q13, P(13, 'Figure 8 shows the set of hubs and distances', 'before returning to Hub A.')]
Q14B = P(16, 'As well as having main memory, computer systems tend to have secondary storage', 'programs and files.')
Q15 = P(18, 'Computers can use a choice of different search algorithms', 'the linear search and the binary search.')
Q15A = [Q15, P(18, 'Consider the following list of seven names.', 'Amir Dean Eoin Helen Natalia Steve Terry')]
Q15A_KEY = Q15A + [P(18, 'Search algorithms work by comparing the list elements', 'known as a key.')]
Q15B = [Q15, P(19, 'The Python code below shows an implementation of a binary search function.')]
Q15C = [Q15, P(20, 'An alternative implementation of the binary search', 'using recursion as shown.')]
Q16A_STEM = C(4, 'The program defines a function called guess_game', 'until the user guesses the secret number.')
CORRECT = S(23, 'Correct implementation using solution above or similar.')

CARDS = [
    # ── Section A ──────────────────────────────────────────────────────────
    dict(key=(1, None, None), topic='cs-2-4', qfigure='q1-fig0', total=6,
         replaces='batch 1b: the table was the answer figure and the one row its header "Value Data '
                  'Type" worth 6; now each value\'s data type at 1, the table beside the question',
         why='p3: the data type of six values; the scheme prints each, 1 mark',
         ask=P(3, 'Enter the appropriate data type in Column B to match the values in Column A.'),
         rows=[pt(S(4, 'Ciara String/str'), 1, note=S(4, 'Each correct response 1 mark', nth=1)),
               pt(S(4, '255 int/integer'), 1), pt(S(4, '083-1234567 String/str'), 1),
               pt(S(4, '1.5, 1.7, 1.2, 0.9, 1.3 List/array'), 1), pt(S(4, 'False Boolean/Bool'), 1),
               pt(S(4, '-99.99 Float/real'), 1)]),
    dict(key=(2, None, None), topic='cs-2-3', figure='s-q2b', total=6,
         replaces='batch 1b: the answers were unpriced rows on a question total, one with its '
                  'exponents lost; now (a) any one advantage at 3 / 2 and (b) 201 at 3 / 2 / 1, the '
                  'question kept whole',
         why='p3: whole question (no part cards): (a) one advantage of hexadecimal, the scheme '
             'lists four, 3 / 2; (b) C9 in decimal, 201, 3 / 2 / 1; the scheme\'s first method '
             'prints 16 to the power 1 as "161", so the row is its binary method and both are the '
             'solution crop',
         stem=P(3, 'Information systems can represent numbers', 'Many software developers use hexadecimal numbers.'),
         ask=P(3, '(a) Explain one advantage of using hexadecimal numbers.', 'into a decimal number.'),
         rows=[ofpart(P(3, '(a)'), ladder([S(4, 'Hexadecimal is very concise.', 'other number systems.'),
                                         S(4, 'Every hexadecimal digit/character can be represented', 'than other number systems.'),
                                         S(4, 'Because of their conciseness, humans are less likely', 'hexadecimal numbers.'),
                                         S(4, 'Hexadecimal notation is commonly used', 'error codes, colours etc.')], [[2, 3]],
                                        note=S(4, 'Very good description - clear understanding demonstrated 3 marks',
                                               'Fair description - limited understanding 2 marks'))),
               ofpart(P(3, '(b)'), crit(S(4, 'STEP 1. Convert to binary: C9 = 1100 1001', '128 + 64+ 8 + 1 = 201'), 3, [1, 2],
                                        note=S(4, 'Correct 3 marks', 'Response with some merit e.g. C=12 1 mark')))]),
    dict(key=(3, None, None), topic='cs-2-3', qfigure='q3-figs', total=6,
         replaces='batch 1b: the crop carried the paper\'s prose and the answers were unpriced rows '
                  '(the table header among them); now (a) three rows at 1 and (b) the expression at '
                  '3 / 2 / 1, the question kept whole',
         why='p4: whole question (no part cards): (a) complete the truth table, each correct '
             'response 1; (b) a Boolean expression for the shaded square, 3 / 2 / 1',
         stem=P(4, 'The diagram in Figure 1 below', 'centred on the point (0, 0).'),
         ask=[P(4, '(a) A point P(x, y) is plotted', 'P is inside the top right quadrant.'),
              P(4, '(b) Construct a Boolean expression', 'shown in Figure 2.')],
         rows=[ofpart(P(4, '(a)'), pt(S(5, 'False True False'), 1, note=S(5, 'Each correct response 1 mark', nth=1))),
               ofpart(P(4, '(a)'), pt(S(5, 'True False False'), 1)),
               ofpart(P(4, '(a)'), pt(S(5, 'True True True'), 1)),
               ofpart(P(4, '(b)'), crit(S(5, '(x > -d and x < 0) and (y >0 and y < d)'), 3, [1, 2],
                                        note=S(5, 'Note: brackets not necessary', 'Response with some merit 1 mark')))]),
    dict(key=(4, None, None), topic='cs-1-2', total=6,
         replaces='batch 1b: the definition was split over three unpriced rows and the interface '
                  'types were unpriced; now (a) 3 / 2 and (b) any one type, named 1 and described '
                  '2 / 1, the question kept whole',
         why='p5: whole question (no part cards): (a) define user interface, 3 / 2; (b) name and '
             'describe one type, the scheme lists five and accepts others, name 1 and description '
             '2 / 1',
         stem=P(5, 'User interfaces have evolved constantly', 'user-friendly and accessible.'),
         ask=P(5, '(a) What is meant by the term', 'a computer system might use.'),
         rows=[ofpart(P(5, '(a)'), crit(S(5, 'A user interface is the means by which', 'through the use of i/o devices.'), 3, [2],
                                        note=S(5, 'Very good description - clear understanding demonstrated 3 marks',
                                               'Fair description - limited understanding 2 marks'))),
               ofpart(P(5, '(b)'), ladder([S(5, 'Graphical user interface (GUI)', 'Used on most computers & smartphones.'),
                                         S(5, 'Command line interface (CLI)', 'on a particular machine.'),
                                         S(5, 'Menu driven interfaces', 'menus for food, tickets etc.'),
                                         S(5, 'Touch user interface', 'responds to this touch interaction.'),
                                         S(6, 'Natural Language interface (NLI)', 'examples of these type of interfaces.')],
                                        [[1, 2, 3]],
                                        instruction=S(6, 'Any other acceptable response such as virtual reality', 'form based interfaces.'),
                                        note=S(6, 'Name: Type of user interface correctly named 1 mark',
                                               'Fair description - limited understanding 1 mark')))]),
    dict(key=(5, None, None), topic='cs-2-3', total=6,
         replaces='batch 1b: one layer was the only row, all or nothing; now any one layer, named '
                  '2 and described 4 / 2',
         why='p5: name and describe one TCP/IP layer; the scheme describes four (and accepts the '
             'OSI layers), name 2 and description 4 / 2',
         ask=P(5, 'Transmission Control Protocol / Internet Protocol (TCP/IP)', 'describe what happens within this layer.'),
         rows=[ladder([S(6, 'Application layer - encodes/decodes the message', 'HTTP, FTP and SMTP.'),
                       S(6, 'Transport layer - breaks down the message', 'if there are any missing packets.'),
                       S(6, 'Network layer (aka internet layer)', 'and where it came from.'),
                       S(6, 'Data link layer - enables the physical transfer', 'one network and another.')],
                      [[2, 4, 6]],
                      instruction=S(6, 'Note: Some candidates may refer to the older OSI model', 'These would also be acceptable.'),
                      note=S(6, 'Name of layer: TCP/IP layer correctly named 2 marks',
                             'lacking demonstration of full understanding 2 marks'))]),
    dict(key=(6, None, None), topic='cs-3-4', total=6,
         replaces='batch 1b: twelve unpriced rows on a question total; now (a) any two examples at 1 '
                  'and (b) any two characteristics at 2 / 1, the question kept whole; topic Embedded '
                  'systems',
         why='p6: whole question (no part cards): (a) two smart-home embedded systems, the scheme '
             'lists nine and any acceptable, 1 each; (b) two characteristics, the scheme lists '
             'nine, 2 / 1 each; filed under Embedded systems (the question is about them), not '
             'Computer systems',
         stem=P(6, 'Smart homes make use of embedded systems', 'convenient for home owners.'),
         ask=P(6, '(a) State two examples of embedded systems', 'general computer systems.'),
         rows=[ofpart(P(6, '(a)'), anyn([S(7, 'Programmable appliances e.g. washing machine', 'kettle, fridge'),
                                        S(7, 'Heating, ventilation and air conditioning system.'),
                                        S(7, 'Lighting control system.'), S(7, 'Alarm/security systems.'),
                                        S(7, 'Home robots e.g. Roomba', 'window cleaners, lawnmowers'),
                                        S(7, 'Leak detection, smoke and carbon monoxide detectors.'),
                                        S(7, 'Home safety for the elderly and disabled.'), S(7, 'Pet and baby care.'),
                                        S(7, 'Voice control devices like Amazon Alexa', 'home appliances or systems.'),
                                        S(7, 'Any acceptable smart home embedded system.')], 2, 1, open_list=True,
                                       head=P(6, 'State two examples of embedded systems you might find in a smart home.'),
                                       note=S(7, 'Note: Do not accept Micro:bit, Raspberry Pi as valid examples.',
                                              'Each correct example 1 mark'))),
               ofpart(P(6, '(b)'), ladder([S(7, 'Embedded systems perform some specific function or tasks.', 'which they were designed for.'),
                                         S(7, 'Low Cost – the price of embedded systems is relatively inexpensive.'),
                                         S(7, 'Time Specific –embedded systems perform tasks', '(in real time).'),
                                         S(7, 'Low Power – embedded systems typically', 'much power to operate.'),
                                         S(7, 'Minimal User interface –', 'that are easy to use.'),
                                         S(7, 'Less Human intervention –', 'little or no human intervention.'),
                                         S(7, 'Highly Stable –', 'easier to maintain.'),
                                         S(7, 'High Reliability –', 'perform their tasks consistently well.'),
                                         S(7, 'Use microprocessors or micro controllers –', 'use limited memory.')],
                                        [[1, 2], [1, 2]],
                                        note=S(7, 'For each correctly identified characteristic:',
                                               'Limited distinction between embedded systems and general computer systems 1 mark')))]),
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
    dict(key=(10, None, None), topic='cs-2-2', qfigure='q10-figure', total=6,
         replaces='batch 1b: both partitions, three credit rules and two reasons were unpriced rows; '
                  'now (a) either partition at 1 / 2 / 3 and (b) either reason at 3 / 2, the '
                  'question kept whole',
         why='p9: whole question (no part cards): (a) the list after the first partition, the '
             'scheme prints two acceptable results, 1 each for the split and each sub-list; (b) '
             'why 90 is a poor pivot, 3 / 2',
         stem=P(9, 'Quicksort is widely recognised', 'answer the questions that follow.'),
         ask=P(9, '(a) Using the leftmost element as the pivot', 'list shown in Figure 5.'),
         rows=[ofpart(P(9, '(a)'), ladder([S(9, '30 40 10 50 20 60 80 70 90'), S(9, '50 30 20 40 10 60 80 70 90')],
                                        [[1, 2, 3]],
                                        note=S(9, 'Elements split about the pivot 1 mark', 'Right sub-list correct 1 mark'))),
               ofpart(P(9, '(b)'), ladder([S(10, 'Because 90 is the largest number in the list.'),
                                         S(10, 'Because it would increase the time taken to execute the algorithm.')], [[2, 3]],
                                        note=S(10, 'Very good description - clear understanding demonstrated 3 marks',
                                               'Fair description - limited understanding 2 marks')))]),
    dict(key=(11, None, None), topic='cs-2-2', qfigure='q11-fig0', total=6,
         replaces='batch 1b: the flowchart was the answer figure and the answers unpriced rows; now '
                  '(a) the input and output at 1 each and (b) each explanation at 2 / 1, the '
                  'question kept whole',
         why='p10: whole question (no part cards): (a) one input and one output, 1 each; (b) '
             'string slicing and concatenation in the flowchart, each 2 / 1',
         stem=P(10, 'Figure 6 depicts a flowchart of a Python algorithm', 'format: ddmmyyyy.'),
         ask=P(10, '(a) Name one input and one output of the algorithm.', 'slicing and string concatenation.'),
         rows=[ofpart(P(10, '(a)'), pt(S(10, 'Valid inputs: first_name, surname, date_of_birth.'), 1,
                                       note=S(10, 'Note: No marks awarded for actual names',
                                              'Each correct response (1 input and 1 output) 1 mark'))),
               ofpart(P(10, '(a)'), pt(S(10, 'Valid output: username.'), 1)),
               ofpart(P(10, '(b)'), crit(G(10, 'String slicing: Step 5 of the algorithm', 'year of birth from the date of birth.'),
                                         2, [1], note=S(10, 'For each explanation:', 'Fair explanation - limited understanding 1 mark'))),
               ofpart(P(10, '(b)'), crit(G(10, 'String concatenation: Step 7 of the algorithm', 'to determine the username.'),
                                         2, [1]))]),
    dict(key=(12, None, None), topic='cs-1-3', qfigure='q12-fig0', total=6,
         replaces='batch 1b: the SDLC figure was the answer figure and the reasons and testing '
                  'points unpriced rows; now (a) any two reasons at 1 and (b) the distinction at '
                  '4 / 2, the question kept whole; topic Designing and developing',
         why='p11: whole question (no part cards): (a) two reasons the SDLC matters, the scheme '
             'lists six and any other reasonable, 1 each; (b) functional against non-functional '
             'testing, 4 / 2; filed under Designing and developing (the SDLC), not Computer '
             'systems',
         stem=P(11, 'A Software Development Lifecycle (SDLC)', 'creating information systems.'),
         ask=P(11, '(a) Outline briefly two reasons why the SDLC is important.', 'non-functional testing.'),
         rows=[ofpart(P(11, '(a)'), anyn([S(10, 'provides a structured approach (thereby helping to reduce complexity'),
                                         S(10, 'improves software quality', 'risk of failure/errors.'),
                                         S(10, 'minimises overrun on budgets/cost.'),
                                         S(10, 'minimises the risk of missing project deadline(s).'),
                                         S(10, 'maximises use of resources / staff planning.'),
                                         S(10, 'encourages communication and collaboration among all project stakeholders'),
                                         S(10, 'Any other reasonable reason provided.')], 2, 1, open_list=True,
                                        head=S(10, 'The SDLC is important because it:'),
                                        note=S(11, 'Note: Where two separate responses', 'Each correct response 1 mark'))),
               ofpart(P(11, '(b)'), crit(S(11, 'Functional testing tests whether the system meets its requirements',
                                           'penetration testing and compatibility testing.'), 4, [2],
                                         note=S(11, 'Very good distinction - clear understanding demonstrated 4 marks',
                                                'lacking demonstration of full understanding 2 marks')))]),
    # ── Section B ──────────────────────────────────────────────────────────
    dict(key=(13, 'a', 'i'), topic='cs-1-2', total=8,
         replaces='batch 1b: the one row was the heading "Support" worth 8 and an unrelated figure '
                  'was attached; now one argument each way at 4 / 2',
         why='p12: one argument for and one against a rural digital hub; the scheme lists four '
             'of each and accepts others, each 4 / 2',
         stem=Q13, ask=P(12, 'Consider the impact that a digital working hub might have', 'one argument against.'),
         rows=[ladder([S(12, 'Local community and businesses can avail', 'IT facilities/online services.'),
                       S(12, 'Residents who once had to work in major towns', 'to find work elsewhere.'),
                       S(12, 'Facilities might attract new people to live in the area.'),
                       S(12, 'Boost to local economy.')], [[2, 4]], head=S(12, 'Support'),
                      instruction=S(12, 'Accept any other reasonable positive argument.'),
                      note=S(12, 'For each of support and against:', 'Fair description - limited understanding 2 marks')),
               ladder([S(12, 'House prices could increase due to high earners.'),
                       S(12, 'Possible negative impact local culture, community and way of life.'),
                       S(12, 'Increase population could drain infrastructure and resources in place.'),
                       S(12, 'New businesses coming to the area could impact other businesses.')], [[2, 4]],
                      head=S(12, 'Against'), instruction=S(12, 'Accept any other reasonable negative argument.'),
                      note=S(12, 'For each of support and against:', 'Fair description - limited understanding 2 marks'))]),
    dict(key=(13, 'a', 'ii'), topic='cs-3-3', total=3,
         replaces='batch 1b: one data item was the only row, all or nothing, and an unrelated '
                  'figure was attached; now any one item at 1 with its justification 2 / 1; topic '
                  'Modelling and simulation',
         why='p12: one data item for the hub model, justified; the scheme lists three and any '
             'valid item, item 1 and justification 2 / 1; filed under Modelling and simulation, '
             'not Computational thinking',
         stem=Q13, ask=P(12, 'As the demand for desk space in digital hubs increases', 'Justify your answer.'),
         rows=[ladder([S(12, 'Population –this could be used to determine', 'additional demand on these services.'),
                       S(12, 'Housing figures – could be used to model', 'potential increase in population.'),
                       S(12, 'Broadband availability and broadband speed', 'meet potential extra demands.')],
                      [[1, 2, 3]],
                      instruction=S(12, 'Any data item with a valid justification e.g. hub occupancy rates.'),
                      note=S(12, 'Valid data item 1 mark', 'Fair justification - limited understanding 1 mark'))]),
    dict(key=(13, 'a', 'iii'), topic='cs-1-2', total=8,
         replaces='batch 1b: four technologies were 2-mark points and an unrelated figure was '
                  'attached; now any two, identified 1 and described 3 / 2; topic Computers and '
                  'society',
         why='p13: two assistive technologies and how each supports a user; the scheme lists four '
             'and accepts others, each identified 1 and described 3 / 2; filed under Computers and '
             'society (accessibility), not Computer systems',
         stem=Q13, ask=P(13, 'To ensure that the digital hubs are accessible', 'when using a computer system.'),
         rows=[ladder([S(13, 'Braille keyboard - allows the user', 'for the computer in Braille'),
                       S(13, 'Screen reader - software that enables people', 'to use a computer'),
                       S(13, 'Screen magnifier - software that provides', 'for visual impairments'),
                       S(13, 'Sip-and-puff - device that allows users', 'computer system via mouth')],
                      [[1, 2, 3, 4], [1, 2, 3, 4]],
                      instruction=G(13, 'Accept any other relevant examples and explanations such as,', 'Touch screens.'),
                      note=S(13, 'For each correctly identified type of technology 1 mark',
                             'Fair description – limited understanding 2 marks'))]),
    dict(key=(13, 'b', 'i'), topic='cs-1-1', qfigure='q13b-fig8', total=2,
         why='p13: the shortest round trip from Hub A; the scheme prints 85 km by either '
             'direction, 2 / 1',
         stem=P(13, 'Figure 8 shows the set of hubs and distances', 'before returning to Hub A.'),
         ask=P(13, 'Calculate and state the shortest possible route the technician should take.'),
         rows=[crit(S(13, '85 km Hub A', '(15+30+25+15 = 85)'), 2, [1],
                    note=S(13, 'Correct response 2 mark', 'Response with some merit 1 mark'))]),
    dict(key=(13, 'b', 'ii'), topic='cs-2-1', qfigure='q13b-fig8', total=2,
         replaces='batch 1b: one feature was the only row, worth 2, and the crop carried the '
                  'paper\'s prose; now any two of six at 1 with a clean Figure 8',
         why='p13: two features of abstraction in Figure 8; the scheme lists five and any valid, '
             '1 each',
         stem=Q13B, ask=P(13, 'Outline briefly two features of abstraction contained in Figure 8.'),
         rows=[anyn([S(14, 'Circles and letters are used to represent hubs.'), S(14, 'Lines are used to represent roads.'),
                     S(14, 'Numbers are used to represent distance.'), S(14, 'Scale is ignored.'),
                     S(14, 'Geographic features such as lakes/rivers', 'are all ignored.'),
                     S(14, 'Any valid feature.')], 2, 1, open_list=True,
                    head=P(13, 'Outline briefly two features of abstraction contained in Figure 8.'),
                    note=S(14, 'For each feature: Good description - clear understanding demonstrated 1 mark'))]),
    dict(key=(13, 'b', 'iii'), topic='cs-1-1', qfigure='q13b-fig8', total=3,
         replaces='batch 1b: the one row was the heading "Heuristics" worth 3 and the crop carried '
                  'the paper\'s prose; now the scheme\'s explanation at 3 / 2',
         why='p14: what heuristics are; the scheme answers it, 3 / 2',
         stem=Q13B, ask=P(14, 'At the beginning of each day the technician has a look', 'what is meant by heuristics.'),
         rows=[crit(S(14, 'A heuristic is a problem-solving technique', 'the next nearest city (hub).'), 3, [2],
                    note=S(14, 'Very good explanation - clear understanding demonstrated 3 marks',
                           'Fair explanation - limited understanding 2 marks'))]),
    dict(key=(13, 'c', None), topic='cs-1-2', total=12,
         replaces='batch 1b: the one row was the heading "For" worth 12 and an unrelated figure was '
                  'attached; now two arguments for and two against, each 3 / 2; topic Computers and '
                  'society',
         why='p14: two arguments for and two against facial recognition for law enforcement; the '
             'scheme lists five for and three against and accepts others, each 3 / 2; filed under '
             'Computers and society, not Computer systems',
         ask=P(14, 'In 2022, the Irish Government announced plans', 'use of FRS for law enforcement.'),
         rows=[ladder([S(14, 'Video surveillance is already being used.', 'manually look through video footage.'),
                       S(14, 'Helps to rapidly identify criminals.'), S(14, 'Higher number of convictions.'),
                       S(14, 'Reduced crime.'),
                       S(14, 'Control measures can be put in place', 'GDPR can protect privacy.')], [[2, 3], [2, 3]],
                      head=S(14, 'For', nth=2), instruction=S(14, 'Accept any other reasonable positive argument.'),
                      note=S(15, 'For each argument:', 'Fair argument - limited understanding 2 marks')),
               ladder([G(14, 'Privacy (data protection risks', 'What can the data be used for?'),
                       S(15, 'Potential errors leading to mistaken identities.'),
                       S(15, 'Bias. For example, if system is trained', 'in other types of systems, discrimination).')],
                      [[2, 3], [2, 3]], head=S(14, 'Against'),
                      instruction=S(15, 'Accept any other reasonable negative argument.'),
                      note=S(15, 'Note: Where two separate arguments', 'Fair argument - limited understanding 2 marks'))]),
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
    dict(key=(14, 'a', 'iii'), topic='cs-2-3', total=2,
         replaces='batch 1b: one difference was the only row, all or nothing; now either of the '
                  'scheme\'s two at 2 / 1',
         why='p15: one difference between the PC and the accumulator; the scheme gives two and any '
             'valid, 2 / 1',
         ask=P(15, 'The CPU contains a number of registers', 'one difference between these two registers.'),
         rows=[ladder([S(16, 'The Program Counter (PC) contains the address', 'store data to be operated on.'),
                       S(16, 'The PC is typically located as part of the control unit', 'Arithmetic Logic Unit.')], [[1, 2]],
                      instruction=S(16, 'Any valid difference.'),
                      note=S(16, 'Very good explanation - clear understanding demonstrated 2 marks',
                             'Fair explanation - limited understanding 1 mark'))]),
    dict(key=(14, 'a', 'iv'), topic='cs-2-3', total=6,
         replaces='batch 1b: the one row was the heading "Arithmetic Logic Unit (ALU)" worth 6; now '
                  'each component\'s purpose at 3 / 2',
         why='p16: the purpose of the ALU and the CU; the scheme answers each, 3 / 2',
         ask=P(16, 'The CPU is often described as the brains of the computer.', 'purpose of these two components.'),
         rows=[crit(S(16, 'The purpose of the ALU is to perform', 'arithmetic and logical operations.'), 3, [2],
                    head=S(16, 'Arithmetic Logic Unit (ALU)'),
                    note=S(16, 'For each component:', 'Fair description – limited understanding 2 marks')),
               crit(S(16, 'The overall purpose of the CU', "respond to the program's instructions."), 3, [2],
                    head=S(16, 'Control Unit (CU)'))]),
    dict(key=(14, 'a', 'v'), topic='cs-2-3', total=6,
         replaces='batch 1b: the menu was claimed whole at 3 with its first factor as its head; now '
                  'any two factors at 3 / 2',
         why='p16: two factors in CPU performance; the scheme lists five and any other valid, '
             'each 3 / 2',
         ask=P(16, 'The CPU is the most important component of a computer system', 'performance of the CPU.'),
         rows=[ladder([S(16, 'Number of cores.', 'in a given space of time.'),
                       S(16, 'Clock speed.', 'processed in a given space of time.'),
                       S(16, 'Cache. A cache is a fast', 'instructions to be fetched.'),
                       S(16, 'RAM. This is the short-term memory', '(which is a much slower process).'),
                       S(16, 'Temperature. If CPU gets too hot performance will decrease.')], [[2, 3], [2, 3]],
                      instruction=S(16, 'Any other valid response (e.g. word size, bus width etc.)'),
                      note=S(17, 'For each factor:', 'Fair description – limited understanding 2 marks'))]),
    dict(key=(14, 'b', 'i'), topic='cs-2-3', total=3,
         replaces='batch 1b: the one row was the heading "Reasons for choosing solid state..." '
                  'worth 3; now any one reason for either choice at 3 / 2',
         why='p16: recommend SSD or magnetic and justify; the scheme gives four reasons for SSD and '
             'three for magnetic, 3 / 2',
         stem=Q14B, ask=P(16, 'Sarah is looking to buy a new laptop.', 'Justify your answer.'),
         rows=[ladder([Pair(S(17, 'Reasons for choosing solid state over magnetic hard drives'), S(17, 'SSD is smaller, faster, quieter')),
                       Pair(S(17, 'Reasons for choosing solid state over magnetic hard drives'), S(17, 'SSD has no moving parts', 'better for transportation, etc.')),
                       Pair(S(17, 'Reasons for choosing solid state over magnetic hard drives'), S(17, 'SSD is completely electronic - consumes less power')),
                       Pair(S(17, 'Reasons for choosing solid state over magnetic hard drives'), S(17, 'SSD is safe from magnets')),
                       Pair(S(17, 'Reasons for choosing magnetic over solid state hard drives'), S(17, 'Cheaper (cost per gigabyte', 'greater capacity')),
                       Pair(S(17, 'Reasons for choosing magnetic over solid state hard drives'), S(17, 'Data can be overwritten directly on the disk', 'SSDs can be written)')),
                       Pair(S(17, 'Reasons for choosing magnetic over solid state hard drives'), S(17, 'Magnetic drives have been around longer', 'more proven technology'))],
                      [[2, 3]],
                      note=S(17, 'Very good justification - clear understanding demonstrated 3 marks',
                             'Fair justification – limited understanding 2 marks'))]),
    dict(key=(14, 'b', 'ii'), topic='cs-2-3', total=3,
         replaces='batch 1b: half of the scheme\'s answer was the only row, all or nothing; now the '
                  'answer at 3 / 2',
         why='p17: what virtual memory is; the scheme answers it, 3 / 2',
         stem=Q14B, ask=P(17, 'When a computer is carrying out lots of tasks', '‘virtual memory’?'),
         rows=[crit(S(17, 'Virtual memory is an area of secondary storage', 'as it is no longer in RAM.'), 3, [2],
                    note=S(17, 'Very good explanation - clear understanding demonstrated 3 marks',
                           'Fair explanation - limited understanding 2 marks'))]),
    dict(key=(14, 'b', 'iii'), topic='cs-2-3', total=6,
         replaces='batch 1b: the one row was the heading "Cloud Advantages" worth 6; now an '
                  'advantage and a disadvantage, each any one at 3 / 2',
         why='p17: one advantage and one disadvantage of working in the cloud; the scheme lists six '
             'and five, each 3 / 2',
         stem=Q14B, ask=P(17, 'For a school software development project Sarah has to work', 'disadvantage of working in the cloud.'),
         rows=[ladder([S(17, 'Mobility and accessibility', '(assumes internet connectivity).'),
                       S(17, 'Supports collaboration.'), S(17, 'Automatic back-up and restoration of data.'),
                       S(17, 'Low setup costs (typically)'), S(17, 'Unlimited storage capacity.'),
                       S(17, 'Security – looked after by cloud service provider.')], [[2, 3]], head=S(17, 'Cloud Advantages'),
                      note=S(18, 'For each advantage and disadvantage:', 'Fair description - limited understanding 2 marks')),
               ladder([S(18, 'Internet Connectivity'), S(18, 'Vendor lock-in'),
                       S(18, 'Subscription/maintenance costs can become high'), S(18, 'Limited Control'),
                       S(18, 'Security – out of your control')], [[2, 3]], head=S(18, 'Cloud Disadvantages'),
                      note=S(18, 'For each advantage and disadvantage:', 'Fair description - limited understanding 2 marks'))]),
    dict(key=(14, 'b', 'iv'), topic='cs-1-3', total=6,
         replaces='batch 1b: the whole list of activities was one 6-mark row; now any two '
                  'activities at 3 / 2; topic Designing and developing',
         why='p17: two activities of a Business Analyst; the scheme lists four, each 3 / 2; filed '
             'under Designing and developing (roles in a project), not Computer systems',
         stem=Q14B, ask=P(17, 'As part of the school project Sarah has been assigned the role', 'software development company.'),
         rows=[ladder([S(18, 'Identify areas within a business that need improvement.', 'understand all possible solutions.'),
                       S(18, 'Creating presentations and reports', 'directly involved with the proposed system.'),
                       S(18, 'Work as part of the development team', 'programmers and testers.'),
                       S(18, 'Organise staff training', 'with the current business model.')], [[2, 3], [2, 3]],
                      head=S(18, 'Typical activities of a Business Analyst (BA) include:'),
                      note=S(18, 'Note: Where two separate responses', 'Fair description - limited understanding 2 marks'))]),
    dict(key=(15, 'a', 'i'), topic='cs-2-2', qfigure='q15a-names', total=2,
         replaces='batch 1b: an unrelated table was attached and the two answers were 1-mark points; '
                  'now either justified choice at 2; topic Algorithms',
         why='p18: the better search for the list, justified; the scheme accepts linear or binary '
             'with its reason, 2 (no marks without a valid justification); filed under Algorithms '
             '(searching), not Computer systems',
         stem=Q15A, ask=P(18, 'What search algorithm would be best suited', 'Justify your answer.'),
         rows=[anyn([S(18, 'Linear search because the list is short', 'relatively fast on short lists.'),
                     S(18, 'Binary search because the list is already sorted/search is faster.')], 1, 2,
                    head=P(18, 'What search algorithm would be best suited', 'Justify your answer.'),
                    note=S(18, 'Note: No marks for identifying the search algorithm', 'search algorithm named 2 marks'))]),
    dict(key=(15, 'a', 'ii'), topic='cs-2-2', qfigure='q15a-names', total=2,
         replaces='batch 1b: an unrelated table was attached and the answer and its credit rule '
                  'were two 1-mark points; now the names at 2 / 1',
         why='p18: the names compared by linear search; the scheme answers Amir, Dean, Eoin, Helen, '
             'Natalia, 2 / 1',
         stem=Q15A_KEY, ask=P(18, 'List, in order, the names that would be compared', 'using the linear search algorithm.'),
         rows=[crit(S(19, 'Amir, Dean, Eoin, Helen, Natalia'), 2, [1],
                    note=S(19, 'Full correct response 2 marks', 'All names except Natalia listed 1 mark'))]),
    dict(key=(15, 'a', 'iii'), topic='cs-2-2', qfigure='q15a-names', total=2,
         replaces='batch 1b: an unrelated table was attached and the answer and its credit rule '
                  'were two 1-mark points; now the names at 2 / 1; topic Algorithms',
         why='p18: the names compared by binary search; the scheme answers Helen, Steve, Natalia, '
             '2 / 1; filed under Algorithms like (ii), not Computer systems',
         stem=Q15A_KEY, ask=P(18, 'List, in order, the names that would be compared', 'using the binary search algorithm.'),
         rows=[crit(S(19, 'Helen, Steve, Natalia'), 2, [1],
                    note=S(19, 'Full correct response 2 marks', 'All names except Natalia listed 1 mark', nth=2))]),
    dict(key=(15, 'a', 'iv'), topic='cs-2-2', qfigure='q15-fig0', figure='s-q15a-iv', total=3,
         replaces='batch 1b: the table was the answer figure and its header a row; now the three '
                  'blanks (linear worst, binary best and worst) at 1 each with the scheme\'s table; '
                  'topic Algorithms',
         why='p18: complete the best and worst cases; the scheme prints O(N) for linear worst and '
             'O(1) and O(log2 N) for binary, each 1; filed under Algorithms, not Computer systems; '
             'the binary row is read by glyph id (scheme p19), whose O(log2 N) the text layer '
             'reads in maths letters with its subscript flattened',
         stem=Q15A, ask=P(18, 'Complete the table below to show the best and worst case', 'size of the input is N.'),
         rows=[pt(S(19, 'Linear Search O(1) O(N)'), 1, note=S(19, 'Each correct response 1 mark', nth=1)),
               crit(G(19, 'Binary Search O(1) O(log₂ N)'), 2, [1])]),
    dict(key=(15, 'a', 'v'), topic='cs-2-2', total=3,
         replaces='batch 1b: an unrelated table was attached and the answer, cut mid-sentence, was '
                  'all or nothing; now the whole answer at 3 / 2',
         why='p18: what O(1) means; the scheme answers it, 3 / 2',
         stem=Q15, ask=P(18, 'What is meant by O(1) time complexity?'),
         rows=[crit(S(19, 'O(1) time complexity means that the time needed', 'regardless of the size of the input, N.'), 3, [2],
                    note=S(19, 'Very good description - clear understanding demonstrated 3 marks',
                           'Fair description - limited understanding 2 marks'))]),
    dict(key=(15, 'b', 'i'), topic='cs-2-2', qfigure='q15b-code', total=5,
         replaces='batch 1b: the start line was the only row, worth 5, and an unrelated table was '
                  'attached; now the start line at 1, the end line at 1 and the explanation at 3 / 2, '
                  'with the listing',
         why='p19: where the iteration starts and ends and what it does; the scheme answers 6 and '
             '14 at 1 each and explains it, 3 / 2',
         stem=Q15B, ask=P(19, 'In the code there is one example of iteration.', 'explain what it does.'),
         rows=[pt(S(19, 'Start line number: 6'), 1, note=S(20, 'Correct response for start line number 1 mark')),
               pt(S(19, 'End line number: 14'), 1, note=S(20, 'Correct response for end line number 1 mark')),
               crit(S(19, 'The loop repeatedly divides the list in half', 'crossing over the higher index).'), 3, [2],
                    note=S(20, 'Explanation: Very good explanation', 'Fair explanation - limited understanding 2 marks'))]),
    dict(key=(15, 'b', 'ii'), topic='cs-2-2', qfigure='q15b-code', total=3,
         replaces='batch 1b: one purpose was the only row, all or nothing, and an unrelated table '
                  'was attached; now either at 3 / 2 with the listing',
         why='p19: the purpose of a return statement; the scheme gives two answers, 3 / 2',
         stem=Q15B, ask=P(19, 'The function contains two examples of a return statement', 'purpose of a return statement?'),
         rows=[ladder([S(20, 'The purpose of a return statement is to end the function'),
                       S(20, 'To pass the result of the function back to the calling code.')], [[2, 3]],
                      note=S(20, 'Very good explanation - clear understanding demonstrated 3 marks',
                             'Fair explanation - limited understanding 2 marks'))]),
    dict(key=(15, 'b', 'iii'), topic='cs-2-2', qfigure='q15b-code', total=3,
         why='p19: why line 16 returns len(L); the scheme answers it, 3 / 2',
         stem=Q15B,
         ask=P(19, 'Explain the reason for len(L) on line 16.'),
         rows=[crit(S(20, 'It is used to indicate that the value has not been found.'), 3, [2],
                    note=S(20, 'Very good explanation - clear understanding demonstrated 3 marks',
                           'Fair explanation - limited understanding 2 marks', nth=3))]),
    dict(key=(15, 'c', 'i'), topic='cs-2-2', qfigure='q15c-code', total=6,
         replaces='batch 1b: the one row was the scheme\'s lead-in "Recursive functions have the '
                  'following three properties:" and an unrelated table was attached; now any two '
                  'of the three properties at 3 / 2 with the recursive listing',
         why='p20: two properties of recursive functions; the scheme describes three, each 3 / 2',
         stem=Q15C, ask=P(20, 'Referring to the code above, describe two properties of recursive functions.'),
         rows=[ladder([S(20, 'A recursive function must call itself.', 'lines 9 and 11 of the code provided in the question.'),
                       S(20, 'A recursive function must have a base case', 'when lo > hi (line 3).'),
                       S(20, 'Progressive approach.', 'in each recursive call (lines 9 and 11).')], [[2, 3], [2, 3]],
                      note=S(20, 'For each property:', 'Fair description - limited understanding 2 marks'))]),
    dict(key=(15, 'c', 'ii'), topic='cs-2-2', qfigure='q15c-code', total=6,
         replaces='batch 1b: both menus were claimed whole at 3 with their first point as head, and '
                  'an unrelated table was attached; now an advantage and a disadvantage, each any '
                  'one at 3 / 2',
         why='p20: one advantage and one disadvantage of recursion; the scheme lists three and two, '
             'each 3 / 2',
         stem=Q15C, ask=P(20, 'State one advantage and one disadvantage of using recursion.'),
         rows=[ladder([S(21, 'The main benefits of a recursive approach', 'elegance and conciseness'),
                       S(21, 'Recursion can lead to more readable and efficient algorithm descriptions.'),
                       S(21, 'Recursion lends itself well breaking problems', 'smaller similar problems')], [[2, 3]],
                      head=S(21, 'Advantages'),
                      note=S(21, 'For each advantage/disadvantage:', 'Fair description - limited understanding 2 marks')),
               ladder([S(21, 'Performance. Recursion can lead to slower execution', 'memory overheads'),
                       S(21, 'If recursion is too deep', 'ultimately program crashes.')], [[2, 3]],
                      head=S(21, 'Disadvantages'),
                      note=S(21, 'For each advantage/disadvantage:', 'Fair description - limited understanding 2 marks'))]),
    dict(key=(15, 'c', 'iii'), topic='cs-2-2', qfigure='q15c-code', total=3,
         replaces='batch 1b: an unrelated table was attached and the answer was all or nothing; now '
                  '3 / 2 / 1 with the recursive listing',
         why='p20: a call to binary_search2 for Natalia; the scheme prints it, full 3, almost 2, '
             'some merit 1',
         stem=Q15C, ask=P(20, 'Given a list of names, initialised as shown below', '"Steve", "Terry"]'),
         rows=[crit(S(21, 'result = binary_search2("Natalia", names, 0, len(names)-1)'), 3, [1, 2],
                    note=S(21, 'Full correct response 3 marks', 'Response of some merit 1 mark'))]),
    # ── Section C ──────────────────────────────────────────────────────────
    dict(key=(16, 'a', 'i'), topic='cs-2-2', qfigure='q16a-code', figure='s-q16a-i', total=10,
         replaces='batch 1b: filed as section B with "10 marks Correct response" as its row; now '
                  'section C, the B-10 scale and the scheme\'s line 31',
         why='040 p5: show the number of guesses on a win; the scheme marks line 31 # (i), B-10 '
             'scale',
         stem=Q16A_STEM, ask=C(5, 'Change the program to display an extra line of output', 'You took 3 guesses.'),
         rows=[crit(CORRECT, 10, [3, 7], note=S(23, '(i) 10 marks (B-10 scale)', 'Any other reasonable attempt.'))]),
    dict(key=(16, 'a', 'ii'), topic='cs-2-2', qfigure='q16a-code', figure='s-q16a-ii', total=10,
         replaces='batch 1b: filed as section B, its ask cut to one sentence and its row "10 marks '
                  'Correct response"; now section C, the whole ask, the B-10 scale and the scheme\'s '
                  'lines 32-37',
         why='040 p5: too-low / too-high hints; the scheme marks lines 32-37 # (ii), B-10 scale',
         stem=Q16A_STEM, ask=C(5, 'The program does not display a message unless', 'You took 4 guesses.'),
         rows=[crit(CORRECT, 10, [3, 7], note=S(23, '(ii) 10 marks (B-10 scale)', 'Any other reasonable attempt.'))]),
    dict(key=(16, 'a', 'iii'), topic='cs-2-2', qfigure='q16a-code', figure='s-q16a-iii', total=5,
         replaces='batch 1b: filed as section B with the line number "19" as its row; now section C, '
                  'the whole ask, the B-5 scale and the scheme\'s line 18',
         why='040 p6: at most max_guesses_allowed guesses; the scheme marks line 18 # (iii), B-5 '
             'scale',
         stem=Q16A_STEM, ask=C(6, 'Currently the program has no way of ending', 'Sorry! Your guess was too low', end_nth=2),
         rows=[crit(CORRECT, 5, [2, 3], note=S(23, '(iii) 5 marks (B-5 scale)', 'Any other reasonable attempt.'))]),
    dict(key=(16, 'a', 'iv'), topic='cs-2-2', qfigure='q16a-code', figure='s-q16a-iv', total=5,
         replaces='batch 1b: filed as section B, topic Evaluation and testing, its ask cut to one '
                  'sentence and its row "semantic error."; now section C, Algorithms like its '
                  'siblings, the whole ask, the B-5 scale and the scheme\'s lines 40-43',
         why='040 p6: read the maximum number of guesses; the scheme marks lines 40-43 # (iv), B-5 '
             'scale',
         stem=Q16A_STEM, ask=C(6, 'Currently the number of guesses that the user is allowed', 'Sorry! Your guess was too high'),
         rows=[crit(S(24, 'Correct implementation using solution above or similar.'), 5, [2, 3],
                    note=S(24, '(iv) 5 marks (B-5 scale)', 'Any other reasonable attempt.'))]),
    dict(key=(16, 'a', 'v'), topic='cs-2-2', qfigure='q16a-code', figure='s-q16a-v', total=10,
         replaces='batch 1b: filed as section B, topic Evaluation and testing, its ask cut to one '
                  'sentence and five 2-mark rows of scale furniture; now section C, the whole ask, '
                  'the C-10 scale and the scheme\'s lines 7-13',
         why='040 p6: a difficulty level for the secret number; the scheme marks lines 7-13 # (v), '
             'C-10 scale',
         stem=Q16A_STEM, ask=C(6, 'Currently the secret number is always between 1 and 5 inclusive.',
                               'Enter your guess: 95 Sorry! Your guess was too low'),
         rows=[crit(S(24, 'Correct implementation using solution above or similar.'), 10, [3, 5, 7],
                    note=S(24, '(v) 10 marks (C-10 scale)', 'Any other reasonable attempt.'))]),
    dict(key=(16, 'a', 'vi'), topic='cs-2-2', qfigure='q16a-code', figure='s-q16a-vi', total=10,
         replaces='batch 1b: filed as section B with five 2-mark rows of scale furniture; now '
                  'section C, the C-10 scale and the scheme\'s lines 16 and 23-27',
         why='040 p7: flag a repeated guess; the scheme marks lines 16 and 23-27 # (vi), C-10 scale',
         stem=Q16A_STEM, ask=C(7, 'Modify the code so that if the user guesses a number', 'You took 3 guesses.'),
         rows=[crit(S(24, 'Correct implementation using solution above or similar.'), 10, [3, 5, 7],
                    note=S(24, '(vi) 10 marks (C-10 scale)', 'Any other reasonable attempt.'))]),
    dict(key=(16, 'b', None), topic='cs-2-2', qfigure='q16b-output', figure='s-q16b', total=30,
         replaces='batch 1b: filed as section B, its ask was "Open the program..." and its row '
                  '"Possible solution:" worth 30; now section C, the guessing-game task, the example '
                  'output, and the rubric\'s four criteria at their printed levels',
         why='040 p8-9: write the points-scoring guessing game; the scheme prints a possible '
             'solution and a rubric of four criteria at high / moderate / low (cells of scheme '
             'p26): standards 5 / 4 / 3, inputs 5 / 4 / 3, logic 10 / 7 / 5, outputs 10 / 7 / 5',
         ask=GAt('040', 8, (95, 185, 560, 680), breaks=True),
         rows=[crit(T(26, 'Program executes correctly with no syntax or runtime errors', 'Meaningful variable/function names'),
                    5, [3, 4], head=T(26, 'Programming Standards'),
                    note=[T(26, 'High level of achievement All of the following', 'correctly and efficiently'),
                          T(26, 'Moderate level of achievement Reasonable attempt', 'each of the following'),
                          T(26, 'Low level of achievement Poor attempt to complete any of the following')]),
               crit(T(26, 'Computer correctly generates random number between 1 and 100', 'use of assignment statements'),
                    5, [3, 4], head=T(26, 'Program Inputs')),
               crit(T(26, 'Game loop / “Play again” logic', 'Total scores correctly calculated'), 10, [5, 7],
                    head=T(26, 'Program Logic (Processing)')),
               crit(T(26, 'Message to display secret number', 'at the end of each round'), 10, [5, 7],
                    head=T(26, 'Program Outputs'))]),
]
