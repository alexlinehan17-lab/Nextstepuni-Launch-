"""Computer Science 2022 Higher Level: every card of the sitting, lifted from the page.

The 40 cards shipped in August are re-authored here under their own ids (batch
1b), and the 8 the lane added for the asks they missed are kept, converted to
the ladder and instruction rules of 5 Nov. Paper pages 3-24 (Sections A and B)
and Section C pages 4-7, and scheme pages 3-22 were opened.

cs-2022-hl-q2, -q3, -q4, -q7, -q9 and -q10 are shipped as whole questions
(two parts each, no part cards beside them); each stays whole with a row per
part. cs-2022-hl-q14 was shipped as the whole of Q14 beside part cards for
(a)(ii)-(v) and (b)(ii)-(iv); by the coordinator's ruling of 5 Nov it is
split: (a)(i) and (b)(i), the two asks only it covered, are cards of their own
and the whole id is WITHDRAWN to the first of them.

Q1's output box and Q13(a)(iii)'s stakeholder table are read from the
scheme's table cells (pages 4 and 11, compsci_lane.append_cells): the flat
text puts each output value on a line of its own, which the provenance gate
drops as a bare mark, and reads the stakeholder table across, so each
stakeholder's role arrives interleaved with the other rows.

Section C's A-5 scale is "0, 5" in the scheme's own scale table (page 3), so
(i) and (iv) are all or nothing; (ii), (iii) are B-5 (0, 2, 3, 5), (v), (vi)
B-10 (0, 3, 7, 10) and (vii) C-10 (0, 3, 5, 8, 10).
"""
from compsci_lane import (C, P, Pair, S, T, anyn, ask_row, crit, crop, ladder, ofpart, pt, stack)  # noqa: F401

WITHDRAWN = {'cs-2022-hl-q14': 'cs-2022-hl-q14-a-i'}

CROPS = {
    'q5-flow': stack([('038', 6, (170, 144, 424, 462)), ('038', 6, (54, 510, 511, 714))],
                     ref='2022 HL Q5',
                     alt='Figure 1: a flowchart. Start, INPUT pH, then a decision whose text is '
                         'missing (A); its TRUE branch outputs "Acid" and its other branch, '
                         'labelled B, leads to the decision pH > 7. That decision\'s branch '
                         'labelled C leads to an output whose text is missing (D), and its FALSE '
                         'branch to another output whose text is missing (E); all paths end at '
                         'Stop. Below it, the table with Letter A to E and a blank Missing Text '
                         'column.'),
    'q11-tree': crop('038', 10, (52, 316, 539, 596), ref='2022 HL Q11',
                     alt='The honey bee ancestry tree printed with Question 11, with the key M = '
                         'Male bee (they only have a mother) and F = Female bee (female bees have '
                         'a mother and a father). Generation 1 is one male; Generation 2 one '
                         'female; Generation 3 a female and a male; Generation 4 a female, a male '
                         'and a female; Generation 5 F, M, F, M, F.'),
    'q12-tm': crop('038', 11, (38, 190, 514, 545), ref='2022 HL Q12',
                   alt='Figure 3: the state transition diagram of a Turing machine with states '
                       'S0, S1, S2 and S3 (S3 the final state), its transitions labelled (1,0), '
                       '(0,0), (1,1), (1,0), (0,1), (0,0) and (B,B). Beside it, the trace to fill '
                       'in: State S0 over the tape ... 0 1 1 0 B ... with the head under the '
                       'first 0, then five rows of a blank State box and a blank tape.'),
    'q14a-algo': stack([('038', 16, (178, 116, 375, 192)), ('038', 16, (178, 234, 375, 311)),
                        ('038', 16, (75, 340, 549, 473))],
                       ref='2022 HL Q14(a)',
                       alt='The two lists printed with Question 14(a): at the start list1 holds '
                           '15, 28, 14, 21 and list2 is four empty boxes; at the end list1 is '
                           'empty and list2 holds 14, 15, 21, 28. Below them, the six-line '
                           'pseudo-code: 1. Let N be the number of elements in list1, 2. '
                           'Initialise an empty list of length N - call this list2, 3. Repeat N '
                           'times:, 4. Select the smallest (minimum) element from list1, 5. Move '
                           'the smallest element from list1 to list2, 6. Stop.'),
    'q14a-i': stack([('038', 16, (75, 340, 549, 473)), ('038', 16, (70, 552, 410, 712)),
                     ('038', 17, (70, 52, 420, 310))],
                    ref='2022 HL Q14(a)(i)',
                    alt='The pseudo-code of Question 14(a) (select the smallest element of list1 '
                        'and move it to list2, N times), then the states to fill in for part '
                        '(i): Initial State list1 15, 28, 14, 21 and list2 empty; State after '
                        'Pass #1 list1 15, 28, a blank, 21 and list2 14 then three blanks; and '
                        'States after Passes #2, #3 and #4, every box blank.'),
    'q14b-i': stack([('038', 19, (80, 87, 532, 210)), ('038', 19, (100, 236, 465, 442))],
                    ref='2022 HL Q14(b)(i)',
                    alt='Figure 4: a shelf of books lettered F B E C A G D becoming B E F C A G '
                        'D after pass #2, the book being inserted shaded. Below it, the grid to '
                        'fill in: Initial List F B E C A G D; After Pass #1 B F E C A G D; After '
                        'Pass #2 B E F C A G D; After Passes #3 to #6 seven blank boxes each.'),
    'q15b-code': crop('038', 22, (53, 93, 542, 212), ref='2022 HL Q15(b)',
                      alt='The eight-line program printed with Question 15(b): a comment, isbn = '
                          '"102004110", total = 0, for i in range(10, 1, -1): total = total + '
                          'int(isbn[10-i]) * i, then check_digit = 11 - (total % 11) and a print '
                          'of the check digit for isbn.'),
    'q15c-listing': crop('038', 23, (53, 244, 542, 403), ref='2022 HL Q15(c)',
                      alt='The eleven-line program printed with Question 15(c): a comment, isbn '
                          '= 102004110, isbn1 = isbn, total = 0, for i in range(2, 11): digit = '
                          'isbn % 10, total = total + digit*i, isbn = isbn//10, then check_digit '
                          '= 11 - (total % 11) and a print of the check digit for isbn1.'),
    'q15c-table': stack([('038', 23, (53, 244, 542, 403)), ('038', 23, (156, 466, 439, 710))],
                        ref='2022 HL Q15(c)(i)',
                        alt='The eleven-line program of Question 15(c) (digit = isbn % 10, total '
                            '= total + digit*i, isbn = isbn//10 for i from 2 to 10) above the '
                            'trace table, columns i, digit, total and isbn: a first row 0, '
                            '102004110, then rows for i = 2 to 6 filled in (0 0 10200411, 1 3 '
                            '1020041, 1 7 102004, 4 27 10200, 0 27 1020) and rows for i = 7 to 10 '
                            'blank.'),
    'q15-progs': stack([('038', 22, (53, 94, 542, 211)), ('038', 23, (53, 245, 542, 402))],
                       ref='2022 HL Q15(c)',
                       alt='The two check-digit programs printed with Question 15. Part (b): isbn '
                           'stored as the string "102004110"; a for loop over range(10, 1, -1) '
                           'adds int(isbn[10-i]) * i to total. Part (c): isbn stored as the integer '
                           '102004110 and copied to isbn1; a for loop over range(2, 11) takes '
                           'digit = isbn % 10, adds digit*i to total and sets isbn = isbn//10. '
                           'Both then compute check_digit = 11 - (total % 11) and print it.'),
    'q16a-code': crop('040', 4, (52, 387, 557, 697), ref='2022 HL Q16(a)',
                      alt='The 21-line program Question16_A.py as printed in the Section C '
                          'booklet: from random import randint; print("Dice simulation '
                          'program"); results = [] and frequencies = [0, 0, 0, 0, 0, 0]; a loop '
                          'of 100 throws, each throw_result = randint(1,6) appended to results, '
                          'counting ones in frequencies[0] and twos in frequencies[1]; then '
                          'print() and print("Results:", results).'),
    's-q4': stack([('scheme', 5, (173, 506, 423, 708)), ('scheme', 6, (115, 80, 480, 184))],
                  ref='2022 HL Q4', solution=True,
                  alt='The marking scheme\'s answers to Question 4: the completed truth table '
                      'for A AND (B OR C), whose last column reads 0, 0, 0, 0, 0, 1, 1, 1 for '
                      'the inputs 000 to 111; and the circuit, B and C into an OR gate giving '
                      'B + C, which joins A in an AND gate giving A.(B + C).'),
    's-q11a': crop('scheme', 9, (52, 219, 537, 497), ref='2022 HL Q11(a)', solution=True,
                   alt='The marking scheme\'s completed honey bee ancestry tree for Question '
                       '11(a), extended to Generations 6 and 7 with every bee labelled male or '
                       'female.'),
    's-q12': crop('scheme', 10, (200, 73, 423, 374), ref='2022 HL Q12', solution=True,
                  alt='The marking scheme\'s completed trace for Question 12: S0 over 0 1 1 0 B '
                      'with the head on the first cell; S2 over 0 1 1 0 B, head on the second '
                      'cell; S1 over 0 0 1 0 B, head on the third; S1 over 0 0 1 0 B, head on '
                      'the fourth; S2 over 0 0 1 1 B, head on the B; S3 over 0 0 1 1 B, head '
                      'past the B.'),
    's-q14a-i': crop('scheme', 14, (100, 340, 445, 550), ref='2022 HL Q14(a)(i)', solution=True,
                     alt='The marking scheme\'s states for Question 14(a)(i): after pass #2 '
                         'list1 holds 28 and 21 and list2 14, 15; after pass #3 list1 holds 28 '
                         'and list2 14, 15, 21; after pass #4 list1 is empty and list2 holds 14, '
                         '15, 21, 28.'),
    's-q14b-i': crop('scheme', 15, (100, 610, 445, 725), ref='2022 HL Q14(b)(i)', solution=True,
                     alt='The marking scheme\'s passes for Question 14(b)(i): after pass #3 B C '
                         'E F A G D (A shaded); after pass #4 A B C E F G D (G shaded); after '
                         'pass #5 A B C E F G D (D shaded); after pass #6 A B C D E F G.'),
    's-q15c-i': crop('scheme', 18, (158, 419, 438, 662), ref='2022 HL Q15(c)(i)', solution=True,
                     alt='The marking scheme\'s completed trace table for Question 15(c)(i): '
                         'the printed rows, then i = 7 digit 0 total 27 isbn 102; i = 8 digit 2 '
                         'total 43 isbn 10; i = 9 digit 0 total 43 isbn 1; i = 10 digit 1 total '
                         '53 isbn 0.'),
    's-q16a-i': crop('scheme', 20, (57, 206.3, 545, 216.5), ref='2022 HL Q16(a)(i)', solution=True,
                     alt='Line 5 of the marking scheme\'s possible solution: print("Dice '
                         'simulation and analysis program"), marked part (i).'),
    's-q16a-ii': crop('scheme', 20, (57, 498.0, 545, 508.4), ref='2022 HL Q16(a)(ii)', solution=True,
                      alt='Line 33 of the marking scheme\'s possible solution: '
                          'print("Frequencies:", frequencies), marked part (ii).'),
    's-q16a-iii': crop('scheme', 20, (57, 352.2, 545, 456.1), ref='2022 HL Q16(a)(iii)', solution=True,
                       alt='Lines 19 to 28 of the marking scheme\'s possible solution, between # '
                           'part (iii) - start and # part (iii) - end: elif branches for '
                           'throw_result == 3, 4, 5 and 6, each adding 1 to frequencies[2], [3], '
                           '[4] and [5].'),
    's-q16a-iv': crop('scheme', 20, (57, 477.3, 545, 487.6), ref='2022 HL Q16(a)(iv)', solution=True,
                      alt='Line 31 of the marking scheme\'s possible solution: the print of the '
                          'results list commented out with a #, marked part (iv).'),
    's-q16a-v': crop('scheme', 20, (57, 519.0, 545, 581.3), ref='2022 HL Q16(a)(v)', solution=True,
                     alt='Lines 35 to 40 of the marking scheme\'s possible solution, # part (v): '
                         'print(), the two header rows printed with a tab, then for i in '
                         'range(6): print(i+1, "\\t", frequencies[i]).'),
    's-q16a-vi': crop('scheme', 20, (57, 591.9, 545, 633.2), ref='2022 HL Q16(a)(vi)', solution=True,
                      alt='Lines 42 to 45 of the marking scheme\'s possible solution, # part (vi): '
                          'print(), largest = max(frequencies), then '
                          'print(frequencies.index(largest)+1, "was rolled most often -", '
                          'largest, "times").'),
    's-q16a-vii': crop('scheme', 20, (57, 644.1, 545, 716.6), ref='2022 HL Q16(a)(vii)', solution=True,
                       alt='Lines 47 to 53 of the marking scheme\'s possible solution, # part '
                           '(vii) Horizontal Bar Chart: print(), then for freq in frequencies: '
                           'for i in range(freq): print("*", end=""), and print() after each '
                           'row.'),
}

Q13_STEM = P(12, 'K-9 Kennels is a small dog boarding business', 'grooming, massage and training.')
Q13A = [Q13_STEM, P(12, 'Mary and John realise that they need an information system', 'asked you to attend.')]
Q13B = [Q13_STEM, P(14, 'Some weeks after the initial meeting', 'a shop page and a checkout page.')]
Q14A_STEM = [P(16, 'A simplified version of the selection sort algorithm', 'list2 is empty as shown.'),
             P(16, 'At the end of the algorithm list1 is empty', 'now sorted in ascending order.'),
             P(16, 'The algorithm is described by the following pseudo-code:')]
Q15_STEM = P(21, 'A check digit is a single digit number', 'the ISBN number is deemed to be valid.')
Q15B = [Q15_STEM, P(22, 'Given a 9-digit number, the Python program below', 'used as the 10th digit.')]
Q15C = [Q15_STEM, P(23, 'The Python program below shows an alternative implementation.')]
Q16A_STEM = C(4, 'The program simulates the rolling of a die 100 times.', 'stored in a list called frequencies.')
CORRECT = 'Correct implementation using solution above or similar.'

CARDS = [
    # ── Section A ──────────────────────────────────────────────────────────
    dict(key=(1, None, None), topic='cs-2-2', qfigure='q1-code0', total=5,
         replaces='batch 1b: the row was the label "Output" worth 5; the five printed values '
                  'were never a row; the listing sat on the answer side',
         why='p3: the output of a 13-line program; the scheme prints the five lines, 1 each in '
             'order (read from its cells: each value is a line of its own in the flat text, '
             'which the provenance gate drops as a bare mark). The shipped crop of the listing '
             'was opened and is complete',
         ask=P(3, 'What is the output of the following Python program?'),
         rows=[crit(T(4, '5 6 15 5 6'), 5, [1, 2, 3, 4],
                    note=S(4, 'Each correct response in the correct order 1 mark'))]),
    dict(key=(2, None, None), topic='cs-2-3', total=5,
         replaces='batch 1b: unpriced question-total rows; (b)\'s pricing line was welded to an '
                  'answer',
         why='p3-4: shipped as the whole of Q2. (a) volatile memory, two answers 3 / 1; (b) two '
             'differences between registers and RAM, five listed, 1 each',
         stem=P(3, 'Registers and RAM are both types of volatile memory.'),
         ask=[P(3, '(a) What is volatile memory?'), P(4, '(b) Describe two differences between registers and RAM.')],
         rows=[ofpart(P(3, '(a)'), ladder([S(4, 'A type of memory used to store data/programs', 'switched on/running.'),
                       S(4, 'Called volatile because entire contents are cleared', 'switched off.')], [[1, 3]],
                      note=S(4, 'Very good description - clear understanding demonstrated 3 marks',
                             'Fair description - limited understanding 1 mark'))),
               ofpart(P(3, '(b)'), anyn([S(4, 'Physical location. Registers are located inside', 'as close to the CPU.'),
                     S(4, 'Access time/speeds. Contents of registers', 'than contents of RAM.'),
                     S(4, 'Cost. Registers are more expensive than RAM (per byte).'),
                     S(4, 'Capacity. Registers hold less than RAM (because of cost).'),
                     S(4, 'Material. Made from different materials.'),
                     S(4, 'Any other valid difference.')], 2, 1, open_list=True,
                    head=P(4, 'Describe two differences between registers and RAM.'),
                    note=S(4, '1 marks for each difference clearly described')))]),
    dict(key=(3, None, None), topic='cs-2-3', total=5,
         replaces='batch 1b: unpriced question-total rows, among them the headings "Transistor" '
                  'and a bullet run into "Integrated Circuit"',
         why='p4: shipped as the whole of Q3. (a) the two terms, four answers for transistor and '
             'one for integrated circuit, 2 / 1 each; (b) why Moore\'s Law may fail, 1',
         stem=P(4, 'In 1965 Gordon Moore', 'very accurate to the present day.'),
         ask=P(4, '(a) Explain the terms transistor and integrated circuit.', 'might not remain accurate in the future.'),
         rows=[ofpart(P(4, '(a)'), ladder([Pair(S(5, 'Transistor'), S(5, 'A transistor is type of electronic switch.')),
                       S(5, 'A transistor is a semiconductor device', 'connection to an external circuit.'),
                       S(5, 'A transistor is the fundamental building block', 'integrated circuits and microprocessors.'),
                       S(5, 'Transistors are used to represent binary 1’s and 0’s.')], [[1, 2]],
                      note=S(5, 'For each term: Very good explanation - clear understanding demonstrated 2 marks',
                             'Fair explanation - limited understanding 1 mark'))),
               ofpart(P(4, '(a)'), crit(S(5, 'An integrated circuit (chip) is an electronic component', 'on a single silicon board.'), 2, [1],
                    head=S(5, 'Integrated Circuit'))),
               ofpart(P(4, '(b)'), pt(S(5, 'There is a physical limitation to the number of transistors that can fit on a single chip.'), 1,
                  note=S(5, 'Full correct response 1 mark')))]),
    dict(key=(4, None, None), topic='cs-2-3', qfigure='q4-fig0', figure='s-q4', total=5,
         replaces='batch 1b: unpriced question-total rows, one per truth-table line, and the '
                  'scheme\'s descriptors as rows; the table sat on the answer side',
         why='p5: shipped as the whole of Q4. (a) complete the truth table, every value 2, three '
             'or more 1 (the six rows the candidate fills, A B C and the result); (b) draw the circuit, '
             'which the scheme draws, 3 / 2 / 1. The shipped crop of the blank table was opened '
             'and is complete',
         stem=P(5, 'An automatic garage door has three inputs:', 'the logical statement: A AND (B OR C).'),
         ask=[P(5, '(a) Complete the truth table for the logical statement A AND (B OR C).'),
              P(5, '(b) Use the relevant gate symbols to draw the circuit diagram for this system.')],
         rows=[ofpart(P(5, '(a)'), crit(S(5, '0 1 0 0', '1 1 1 1', nth=2, end_nth=3), 2, [1], head=S(5, 'A B C A AND (B OR C)'),
                    note=S(5, 'Every value correct 2 marks', '3 (or more) correct values 1 mark'))),
               ofpart(P(5, '(b)'), crit(S(6, 'Gates combined correctly as above'), 3, [1, 2],
                    note=S(6, 'Gates combined correctly as above 3 marks',
                           'Use of AND or OR gates with either inputs correctly labelled 1 mark')))]),
    dict(key=(5, None, None), topic='cs-2-2', qfigure='q5-flow', total=5,
         why='p6: the flowchart\'s missing text at A-E; the scheme prints it, 1 each',
         ask=P(6, 'A chemical solution is said to be an acid', 'for the letters A-E.'),
         rows=[pt(S(6, 'A pH < 7'), 1, note=S(6, 'Each correct response 1 mark')),
               pt(S(6, 'B FALSE'), 1), pt(S(6, 'C TRUE'), 1),
               pt(S(6, 'D OUTPUT “Base”'), 1), pt(S(6, 'E OUTPUT “Neutral”'), 1)]),
    dict(key=(6, None, None), topic='cs-2-3', qfigure='q6-fig0', total=5,
         replaces='batch 1b: the answer was all or nothing at 5 against a 5 / 3 / 1 scale; '
                  'Figure 2 sat on the answer side and its caption ran into the stem',
         why='p7: the client-server model in Figure 2\'s terms; the scheme answers it, 5 / 3 / 1. '
             'The shipped crop of Figure 2 was opened and is complete',
         ask=P(7, 'Figure 2 shows an example of the client-server model', 'terms included in Figure 2.'),
         rows=[crit(S(6, 'A web client sends a browser request to a web server.', 'in the form of a server response.'),
                    5, [1, 3],
                    note=S(6, 'Very good explanation - clear understanding demonstrated 5 marks',
                           'Fair explanation - limited understanding 1 mark'))]),
    dict(key=(7, None, None), topic='cs-2-3', total=5,
         replaces='batch 1b: unpriced question-total rows; (b)\'s pricing line was welded to an '
                  'answer',
         why='p7-8: shipped as the whole of Q7. (a) ransomware, 3 / 1; (b) two measures against '
             'a cyberattack, six listed, 1 each',
         stem=P(7, 'On 14 May 2021, the Health Service Executive', 'to be shut down.'),
         ask=[P(7, '(a) Explain the term ransomware.'),
              P(8, '(b) State two measures individuals or companies', 'reduce the risk of a cyberattack.')],
         rows=[ofpart(P(7, '(a)'), crit(S(7, 'Ransomware is a type of malicious software', 'the ransom increases.'), 3, [1],
                    note=S(7, 'Very good description - clear understanding demonstrated 3 marks',
                           'Fair description - limited understanding 1 mark'))),
               ofpart(P(8, '(b)'), anyn([S(7, 'Company policy and procedures (people controls).'), S(7, 'Password policies.'),
                     S(7, 'Anti-virus software.'), S(7, 'Security systems (e.g. firewall, VPN).'),
                     S(7, 'Encryption.'), S(7, 'Cloud (security services may be better than local organisations).'),
                     S(7, 'Any acceptable measure.')], 2, 1, open_list=True,
                    head=P(8, 'State two measures individuals or companies can take to reduce the risk of a cyberattack.'),
                    note=S(7, 'Each correct response 1 mark')))]),
    dict(key=(8, None, None), topic='cs-2-3', total=5,
         replaces='batch 1b: the row was the heading "Cost (advantage)" worth 5; the answers '
                  'and the scheme\'s split of the five marks were lost',
         why='p8: an advantage and a disadvantage of cloud computing for cost and for the '
             'environment; the scheme lists eight and prices the better heading 3 (its better '
             'answer 2 / 1, the other 1) and the other heading 2 (1 each): one answer on '
             '[1, 2], three on [1]',
         ask=P(8, 'Cloud computing has been described as the third wave', 'impact on the environment.'),
         rows=[ladder([Pair(S(7, 'Cost (advantage)'), S(7, 'No need to for one-off up-front capital costs.')),
                       Pair(S(7, 'Cost (advantage)'), S(7, 'No need for upgrading/replacements costs.')),
                       Pair(S(7, 'Cost (disadvantage)'), S(7, 'Costs are ongoing (pay-as-you-go)', 'more expensive in the long run.')),
                       Pair(S(7, 'Cost (disadvantage)'), S(7, 'Ongoing costs to cloud service provider', 'software and hardware up-to-date')),
                       Pair(S(7, 'Environment (advantage)'), S(7, 'Economy of scale meaning', 'reducing carbon footprint.')),
                       Pair(S(7, 'Environment (advantage)'), S(7, 'Many cloud companies generate their own energy (and supply to grid)')),
                       Pair(S(7, 'Environment (advantage)'), S(7, 'Less paper.')),
                       Pair(S(7, 'Environment (disadvantage)'), S(7, 'Owing to its success', 'greater carbon footprint.'))],
                      [[1, 2], [1], [1], [1]],
                      note=[S(7, 'Award 3 marks for better of cost or environment as follows:',
                              'Fair description - limited understanding 1 mark'),
                            S(8, '1 mark for other advantage/disadvantage', 'clear understanding demonstrated 1 mark',
                              end_nth=3)])]),
    dict(key=(9, None, None), topic='cs-2-2', total=5,
         replaces='batch 1b: unpriced question-total rows; (a)\'s pricing line was welded to an '
                  'answer',
         why='p9: shipped as the whole of Q9. (a) two benefits of machine learning, nine '
             'listed, 1 each; (b) bias, 3 / 1',
         ask=P(9, '(a) Provide two examples of how machine learning', 'in relation to machine learning.'),
         rows=[ofpart(P(9, '(a)'), anyn([S(8, 'Self-driving vehicles – safety/more accessible.'),
                     S(8, 'Healthcare – early detection of chronic illnesses', 'disease spread etc.'),
                     S(8, 'Entertainment – music/concert/movie/book recommender systems etc.'),
                     S(8, 'Online shopping – product recommender systems, ads etc.'),
                     S(8, 'Facial recognition in home/business security systems.'),
                     S(8, 'Environmental protection.'), S(8, 'Fairer justice systems.'),
                     S(8, 'Arts – music/literature.'), S(8, 'Education.'),
                     S(8, 'Any valid example of how machine learning can be used to benefit society.')],
                    2, 1, open_list=True,
                    head=P(9, 'Provide two examples of how machine learning can be used to benefit society.'),
                    note=S(8, 'Each correct response 1 mark'))),
               ofpart(P(9, '(b)'), crit(S(8, 'If the data on which the algorithm makes its decision contains bias', 'will also be biased.'),
                    3, [1],
                    note=S(8, 'Very good description - clear understanding demonstrated 3 marks',
                           'Fair description - limited understanding 1 mark')))]),
    dict(key=(10, None, None), topic='cs-2-1', total=5,
         replaces='batch 1b: (a)\'s answer was lost and (b)\'s was an unpriced question-total row',
         why='p9-10: shipped as the whole of Q10. (a) find the fake coin in the fewest '
             'weighings, the scheme\'s two-weighing method 3 / 2 / 1; (b) abstraction, 2',
         stem=P(9, 'You have eight coins and a two pan scales.', 'heavier than the others.'),
         ask=[P(9, '(a) Explain a way that the fake coin can be found', 'minimum number of weighings.'),
              P(10, '(b) Outline briefly your use of abstraction to tackle this problem.')],
         rows=[ofpart(P(9, '(a)'), crit(S(8, 'The minimum number of weighings to find the fake coin is 2 as follows:',
                      'the heavier coin will be evident from the pan.'), 3, [1, 2],
                    note=S(8, 'Valid solution (2 weighings) 3 marks', 'Reasonable attempt 1 mark'))),
               ofpart(P(9, '(b)'), pt(S(9, 'By ignoring irrelevant details such as coin colour, size and value'), 2,
                  note=S(9, 'Very good description - clear understanding demonstrated 2 marks')))]),
    dict(key=(11, 'a', None), topic='cs-3-3', qfigure='q11-tree', figure='s-q11a', total=3,
         printed=S(9, 'Question 11 3+2 marks'),
         why='p10: draw two further generations; the scheme draws them, full 3, one generation '
             'or two branches of generation 7 2, any correct value 1',
         stem=P(10, 'The reproduction rules for honey bees', 'There are five generations shown.'),
         ask=P(10, 'Draw and label two additional generations.'),
         rows=[crit(S(9, 'Full correct response'), 3, [1, 2],
                    note=S(9, 'Full correct response 3 marks', 'Any correct value 1 mark'))]),
    dict(key=(11, 'b', None), topic='cs-3-3', qfigure='q11-tree', total=2,
         printed=S(9, 'Question 11 3+2 marks'),
         why='p10: the pattern in the generations; the scheme names the Fibonacci sequence, 2 / 1',
         stem=P(10, 'The reproduction rules for honey bees', 'There are five generations shown.'),
         ask=P(10, 'Describe any pattern emerging', 'in any particular generation.'),
         rows=[crit(S(9, 'Number of bees at each generation', '(Fibonacci sequence).'), 2, [1],
                    note=S(9, 'Very good description - clear understanding demonstrated 2 marks',
                           'Fair description - limited understanding 1 mark', nth=2))]),
    dict(key=(12, None, None), topic='cs-2-3', qfigure='q12-tm', figure='s-q12', total=5,
         replaces='batch 1b: the row was the descriptor "Three or more correct tapes" worth 5; '
                  'the figure carried the ask and sat on the answer side; the scheme\'s drawn '
                  'trace was missing',
         why='p11: trace the Turing machine; the scheme draws the six tapes, 5 / 3 / 2 / 1',
         ask=P(11, 'The state transition diagram for a particular Turing machine', 'at the end of each step.'),
         rows=[crit(S(10, 'Full correct response'), 5, [1, 2, 3],
                    note=S(10, 'Full correct response 5 marks', 'One correct tape 1 mark'))]),
    # ── Section B ──────────────────────────────────────────────────────────
    dict(key=(13, 'a', 'i'), topic='cs-2-3', total=2,
         replaces='batch 1b: the answer was split mid-sentence into two rows of 1; the stem was '
                  '"This question continues on the next page." twice',
         why='p12: what an information system is; the scheme answers it, 2 / 1',
         stem=Q13A, ask=P(12, 'What is an information system?'),
         rows=[crit(S(11, 'An information system (IS) is the software', 'operation of a business.'), 2, [1],
                    note=S(11, 'Very good description - clear understanding demonstrated 2 marks',
                           'Fair description - limited understanding 1 mark'))]),
    dict(key=(13, 'a', 'ii'), topic='cs-2-4', total=2,
         replaces='batch 1b: one benefit was the only answer, all or nothing at 2; the stem was '
                  'page furniture',
         why='p12: two benefits of an information system to K-9; the scheme lists four, 1 each',
         stem=Q13A, ask=P(12, 'Provide two examples of how an information system could benefit K-9 Kennels.'),
         rows=[anyn([S(11, 'Improve operational efficiencies', 'dogs, customers or staff.'),
                     S(11, 'Information could be used to improve decision making and strategic planning.'),
                     S(11, 'Improve customer service', 'learn more about K-9 kennels.'),
                     S(11, 'Cost reductions (increase in profits).'),
                     S(11, 'Any valid example of a benefit for K-9 kennels.')], 2, 1, open_list=True,
                    head=P(12, 'Provide two examples of how an information system could benefit K-9 Kennels.'),
                    note=S(11, 'For each unique valid/correct example 1 mark'))]),
    dict(key=(13, 'a', 'iii'), topic='cs-1-3', total=6,
         replaces='batch 1b: the row was the table header "Stakeholder Role" worth 6; topic was '
                  'Computer systems',
         why='p12: two stakeholders and their roles; the scheme tables three, each named 1 and '
             'its role 2 / 1 (read from its cells). Filed under Designing and developing',
         stem=Q13A, ask=P(12, 'Identify two key stakeholders and their respective roles in relation to the new system.'),
         rows=[ladder([Pair(T(11, 'Dog owners / general public / customers'), T(11, 'end-users')),
                       Pair(T(11, 'K9-Kennels / John and Mary and their employees'),
                            T(11, 'client / project sponsor Users of the system')),
                       Pair(T(11, 'Software company including any relevant job title', 'tester etc.'),
                            T(11, 'Any relevant description'))], [[1, 2, 3], [1, 2, 3]],
                      note=S(11, 'For each correctly identified stakeholder 1 mark',
                             'Fair description – limited understanding 1 mark'))]),
    dict(key=(13, 'a', 'iv'), topic='cs-1-3', total=2,
         replaces='batch 1b: one topic was the only answer, all or nothing at 2; topic was '
                  'Computer systems',
         why='p13: two topics for the first meeting; the scheme lists five, 1 each. Filed under '
             'Designing and developing',
         stem=Q13A, ask=P(13, 'Outline briefly two topics relating to the project', 'at the initial meeting.'),
         rows=[anyn([S(12, 'K-9’s existing business services', 'in place to support them.'),
                     S(12, 'Customer requirements.'), S(12, 'Project feasibility (cost-benefit analysis).'),
                     S(12, 'Contract / Memorandum Of Understanding (MOU).'),
                     S(12, 'Project plan (e.g. deliverables, key milestones, schedule etc.).'),
                     S(12, 'Any relevant topic.')], 2, 1, open_list=True,
                    head=P(13, 'Outline briefly two topics relating to the project', 'at the initial meeting.'),
                    note=S(12, 'For each topic: Good description - clear understanding demonstrated 1 marks'))]),
    dict(key=(13, 'a', 'v'), topic='cs-1-2', total=4,
         replaces='batch 1b: the row was the heading "Reasons for choosing Web App" worth 4; the '
                  'reasons were lost',
         why='p13: web or mobile app, with two reasons; the scheme lists reasons for each, 2 / 1 '
             'a reason (the choice itself is not priced)',
         stem=Q13A,
         ask=P(13, 'John and Mary are unsure about whether their system', 'Provide two reasons for this choice.'),
         rows=[ladder([Pair(S(12, 'Reasons for choosing Web App'), S(12, 'Accessibility.')),
                       Pair(S(12, 'Reasons for choosing Web App'), S(12, 'Ease of updates.')),
                       Pair(S(12, 'Reasons for choosing Web App'), S(12, 'Better discovery on search engines. (SEO).')),
                       Pair(S(12, 'Reasons for choosing Web App'), S(12, 'Cost-effective development.')),
                       Pair(S(12, 'Reasons for choosing Web App'), S(12, 'Faster speed to market.')),
                       Pair(S(12, 'Reasons for choosing Mobile App'), S(12, 'Speed and performance.')),
                       Pair(S(12, 'Reasons for choosing Mobile App'), S(12, 'Ability to send push notifications.')),
                       Pair(S(12, 'Reasons for choosing Mobile App'), S(12, 'Improved user experience.')),
                       Pair(S(12, 'Reasons for choosing Mobile App'), S(12, 'Offline access.'))],
                      [[1, 2], [1, 2]], instruction=S(12, 'Any valid reason.'),
                      note=S(12, 'For each reason: Very good description - clear understanding demonstrated 2 marks',
                             'Fair description - limited understanding 1 mark'))]),
    dict(key=(13, 'a', 'vi'), topic='cs-1-3', total=3,
         replaces='batch 1b: the answer was cut at "... (e.g. waterfall, agile etc.) is" and all '
                  'or nothing at 3; topic was Computer systems',
         why='p13: why the choice of development process matters; the scheme answers it, 3 / 1. '
             'Filed under Designing and developing',
         stem=Q13A,
         ask=P(13, 'Explain why the choice of software development process is important', 'developing software systems.'),
         rows=[crit(S(12, 'The choice of software development process/methodology', 'ample time to make adjustments.'),
                    3, [1],
                    note=S(12, 'Very good explanation - clear understanding demonstrated 3 marks',
                           'Fair explanation - limited understanding 1 mark'))]),
    dict(key=(13, 'b', 'i'), topic='cs-3-1', total=4,
         why='p14: a wireframe of the shop page; the scheme prices four features, 1 each, and '
             'prints no drawing',
         stem=P(14, 'Some weeks after the initial meeting', 'a shop page and a checkout page.'),
         ask=P(14, 'The shop page should allow visitors to browse items.', 'outlining the purpose of the main elements.'),
         rows=[pt(S(13, 'Image and description of item'), 1), pt(S(13, 'Add to cart button'), 1),
               pt(S(13, 'Link to checkout page'), 1), pt(S(13, 'Overall aesthetic'), 1)]),
    dict(key=(13, 'b', 'ii'), topic='cs-1-3', total=2,
         replaces='batch 1b: the scheme\'s definition of user-centred design was the only row, '
                  'all or nothing at 2; the seven features were lost',
         why='p15: two user-centred design features; the scheme lists seven, 1 each',
         stem=Q13B, ask=P(15, 'Describe two user-centred design features', 'for John and Mary.'),
         rows=[anyn([S(13, 'Consistent page layout e.g. navigation', 'the same on every page.'),
                     S(13, 'Good balance of content and white space.'),
                     S(13, 'Good contrast between text and background.'),
                     S(13, 'Use of consistent font – size, colour, formatting.'),
                     S(13, 'Visited links change in appearance.'),
                     S(13, 'Good use of basic design principles - repetition, contrast, proximity, alignment.'),
                     S(13, 'Responsive design – works on different device sizes and in different browsers.'),
                     S(13, 'Any valid feature.')], 2, 1, open_list=True,
                    head=S(13, 'User-centred design features – involving the user throughout the design process'),
                    note=S(13, 'For each user-centred design feature: Good description - clear understanding demonstrated 1 marks'))]),
    dict(key=(13, 'b', 'iii'), topic='cs-1-3', total=2,
         replaces='batch 1b: the row was the heading "Wireframe" worth 2; topic was Computer '
                  'systems',
         why='p15: two differences between wireframes and prototypes; the scheme describes '
             'each, 1 a difference. Filed under Designing and developing',
         stem=Q13B, ask=P(15, 'State two differences between wireframes and prototypes.'),
         rows=[anyn([Pair(S(13, 'Wireframe'), S(13, 'A wireframe is a sketch of diagram', 'content area and footer).')),
                     Pair(S(13, 'Wireframe'), S(13, 'Wireframes are drawn during the design stage of the design process.')),
                     Pair(S(13, 'Wireframe'), S(13, 'Wireframes are low-fidelity visual representations of some aspect of a system.')),
                     Pair(S(13, 'Wireframe'), S(13, 'Wireframes do not contain real content', 'they may need to change).')),
                     Pair(S(13, 'Wireframe'), S(13, 'Wireframes are relatively quick to develop and change.')),
                     Pair(S(13, 'Wireframe'), S(13, 'Wireframes are relatively cheap.')),
                     Pair(S(13, 'Prototype'), S(13, 'A prototype is a ‘trimmed down’ working version', 'evaluation purposes.')),
                     Pair(S(13, 'Prototype'), S(13, 'Prototypes are developed in the implementation (create) stage of the design process')),
                     Pair(S(13, 'Prototype'), S(13, 'A prototype is software whereas wireframes are sketches', 'relatively costly to develop.')),
                     Pair(S(13, 'Prototype'), S(13, 'Prototypes provide a mid to high fidelity', '(button clicks etc.).'))],
                    2, 1, head=P(15, 'State two differences between wireframes and prototypes.'),
                    note=S(13, 'For each difference 1 mark'))]),
    dict(key=(13, 'b', 'iv'), topic='cs-2-4', total=3,
         replaces='batch 1b: the row was the heading "String" worth 3; the examples were lost',
         why='p15: one example each of string, integer and Boolean data on the checkout page; '
             'the scheme lists examples for each, 1 each',
         stem=Q13B, ask=P(15, 'The checkout page will allow users to enter', 'collect on the checkout page.'),
         rows=[pt(Pair(S(14, 'String'), S(14, 'Customer name, address, contact details, product details')), 1,
                  note=S(14, 'For each valid/correct example 1 mark')),
               pt(Pair(S(14, 'Integer'), S(14, 'Quantity ordered, credit card number, CCV, phone number')), 1),
               anyn([S(14, 'Delivery address same as customer address?'),
                     S(14, 'Receive product promotions, updates, mailing list etc.'),
                     S(14, 'Accept terms and conditions?')], 1, 1, head=S(14, 'Boolean'))]),
    dict(key=(14, 'a', 'i'), topic='cs-2-2', qfigure='q14a-i', figure='s-q14a-i', total=3,
         why='p16-17: fill in passes 2 to 4 of the two-list selection sort; the scheme draws the '
             'three states, 1 a pass. Split out of the withdrawn whole-question card cs-2022-hl-q14',
         stem=Q14A_STEM,
         ask=P(16, 'Apply the algorithm to sort the list of integers', 'fill in the numbers for passes 2, 3 and 4.'),
         rows=[ask_row()]),
    dict(key=(14, 'a', 'ii'), topic='cs-2-2', qfigure='q14a-algo', total=2,
         replaces='batch 1b: the stem was cut at "1." of the pseudo-code and the lists were '
                  'lost; the figure carried the ask and sat on the answer side',
         why='p17: sort in descending order instead; the scheme answers it, 2',
         stem=Q14A_STEM,
         ask=P(17, 'The algorithm sorts the list in ascending order.', 'sorts the list in descending order?'),
         rows=[pt(S(14, 'Select the largest (instead of the smallest) element from list 1 and move it to list2'), 2,
                  note=[S(14, 'Any valid response.'), S(14, 'Good description - clear understanding demonstrated 2 marks')])]),
    dict(key=(14, 'a', 'iii'), topic='cs-2-2', qfigure='q14a-algo', total=3,
         replaces='batch 1b: the answer was all or nothing at 3 against a 3 / 1 scale; topic was '
                  'Computer systems',
         why='p17: a method to find the smallest element; the scheme answers it, 3 / 1. Filed '
             'under Algorithms',
         stem=Q14A_STEM,
         ask=P(17, 'Step 4 of the algorithm says to select the smallest', 'find the smallest element in any list.'),
         rows=[crit(S(15, 'Initialise the minimum to be the first element in the list.', 'until the end of the list is reached.'),
                    3, [1],
                    note=[S(15, 'Pseudocode / flowchart / code are also acceptable'),
                          S(15, 'Very good description - clear understanding demonstrated 3 marks',
                            'Fair description - limited understanding/use of built in functions 1 mark')])]),
    dict(key=(14, 'a', 'iv'), topic='cs-2-2', qfigure='q14a-algo', total=2,
         replaces='batch 1b: one of three accepted answers was the only row',
         why='p18: why copying would fail; the scheme gives three answers, 2',
         stem=Q14A_STEM,
         ask=P(18, 'Step 5 of the algorithm says to move the smallest element', 'from list1 to list2?'),
         rows=[anyn([S(15, 'The same element would always be copied.'), S(15, 'list1 will remain unchanged.'),
                     S(15, 'This would result in an infinite loop.')], 1, 2,
                    head=P(18, 'Why would the algorithm not work if this step said to copy the smallest element from list1 to list2?'),
                    note=S(15, 'Very good explanation - clear understanding demonstrated 2 marks'))]),
    dict(key=(14, 'a', 'v'), topic='cs-2-2', qfigure='q14a-algo', total=3,
         replaces='batch 1b: the answer was all or nothing at 3 against a 3 / 1 scale; topic was '
                  'Computer systems',
         why='p18: an in-place selection sort; the scheme describes it, 3 / 1. Filed under '
             'Algorithms',
         stem=Q14A_STEM,
         ask=P(18, 'The algorithm relies on two lists to complete the sort.', 'without the need for a second list.'),
         rows=[crit(S(15, 'The selection sort algorithm works by passing across every element', 'moves on to the next element.'),
                    3, [1],
                    note=[S(15, 'Pseudocode / flowchart / code are also acceptable.'),
                          S(15, 'Very good description - clear understanding demonstrated 3 marks',
                            'Fair description - limited understanding 1 mark', nth=2)])]),
    dict(key=(14, 'b', 'i'), topic='cs-2-2', qfigure='q14b-i', figure='s-q14b-i', total=4,
         why='p19: fill in passes 3 to 6 of the insertion sort; the scheme draws them, 1 a pass. '
             'Split out of the withdrawn whole-question card cs-2022-hl-q14',
         stem=P(19, 'A bookshelf is partially sorted, in alphabetic order', 'as shown in Figure 4 below.'),
         ask=P(19, 'Fill in the empty boxes below to complete passes 3, 4, 5 and 6 of the insertion sort.'),
         rows=[ask_row()]),
    dict(key=(14, 'b', 'ii'), topic='cs-2-2', total=4,
         replaces='batch 1b: the answer was 2 and "Pseudocode / flowchart / code are also '
                  'acceptable." another row of 2; the stem was "Figure 4 This question continues '
                  'on the next page."; Q14(a)\'s figure sat on the answer side',
         why='p19: how insertion sort works; the scheme answers it, 4 / 2 / 1',
         ask=P(19, 'Explain how the insertion sort algorithm works.'),
         rows=[crit(S(16, 'The insertion sort works by passing across each element', 'inserted into the sorted list at its correct position.'),
                    4, [1, 2],
                    note=[S(16, 'Pseudocode / flowchart / code are also acceptable.'),
                          S(16, 'Very good explanation - clear understanding demonstrated 4 marks',
                            'Fair explanation - limited understanding 1 mark')])]),
    dict(key=(14, 'b', 'iii'), topic='cs-2-2', total=4,
         replaces='batch 1b: one test case was the only answer, all or nothing at 4; Q14(a)\'s '
                  'figure sat on the answer side',
         why='p20: two more test cases for insertion sort; the scheme lists six, 2 each',
         ask=P(20, 'A list that is already reversed would be considered a good test case', 'to test the insertion sort algorithm.'),
         rows=[anyn([S(16, 'A list that is already sorted.'), S(16, 'A list where all the values are the same.'),
                     S(16, 'A list with only two distinct values.'), S(16, 'A list where all the values are different.'),
                     S(16, 'A list with just one element – list size 1.'), S(16, 'An empty list – list size zero.'),
                     S(16, 'Any valid test case.')], 2, 2, open_list=True,
                    head=P(20, 'Describe two other test cases that could be used to test the insertion sort algorithm.'),
                    note=S(16, 'For each unique test case: Very good description - clear understanding demonstrated 2 marks'))]),
    dict(key=(14, 'b', 'iv'), topic='cs-2-2', total=5,
         replaces='batch 1b: the answer was cut and all or nothing at 5 against a 5 / 3 / 1 '
                  'scale; Q14(a)\'s figure sat on the answer side',
         why='p20: insertion sort in Big O; the scheme answers it, 5 / 3 / 1 (the text layer '
             'reads O(n squared) as "O(n2)")',
         ask=P(20, '"Big O" notation is used to describe the complexity', 'using "Big O" notation.'),
         rows=[crit(S(16, 'Worst case is O(n2) – list in reverse order.', 'no there is need to execute inner loop.'),
                    5, [1, 3],
                    note=S(16, 'Very good discussion - clear understanding demonstrated 5 marks',
                           'Fair discussion - limited understanding 1 mark'))]),
    dict(key=(15, 'a', None), topic='cs-2-2', total=3,
         replaces='batch 1b: the row was "Step 1. 1x10=10" alone worth 3; the stem was page '
                  'furniture',
         why='p21: verify the ISBN 1020041102; the scheme works the four steps, 3 / 2 / 1',
         stem=Q15_STEM, ask=P(21, 'Apply the above procedure to verify that the ISBN number 1020041102 is valid.'),
         rows=[crit(S(17, 'Step 1. 1x10=10', 'Remainder = 0 => ISBN is valid'), 3, [1, 2],
                    note=S(17, 'Full correct response 3 marks', 'Any correct step 1 mark'))]),
    dict(key=(15, 'b', 'i'), topic='cs-2-2', qfigure='q15b-code', total=2,
         replaces='batch 1b: one reason was the only answer, all or nothing at 2; the listing '
                  'was run into the stem as text',
         why='p22: two reasons for comments; the scheme lists four, 1 each',
         stem=Q15B, ask=P(22, 'Line 1 of the above program contains a comment.', 'State two reasons why programmers use comments.'),
         rows=[anyn([S(17, 'Make code more readable / understandable for self / others.'),
                     S(17, 'To enable programmer to isolate a part of the code for testing.'),
                     S(17, 'Comments when used as doc strings can become part of the system documentation.'),
                     S(17, 'Comments can contain information about the author, date, version log etc.'),
                     S(17, 'Any reasonable use for comments should be accepted.')], 2, 1, open_list=True,
                    head=P(22, 'State two reasons why programmers use comments.'),
                    note=S(17, 'Each unique correct response 1 mark'))]),
    dict(key=(15, 'b', 'ii'), topic='cs-2-2', qfigure='q15b-code', total=4,
         replaces='batch 1b: the row was the heading "Variable." worth 4; the definitions and '
                  'examples were lost',
         why='p22: variable and data type, each explained with an example; the scheme prices '
             'the description 1 and the example 1 for each term',
         stem=Q15B, ask=P(22, 'The program makes use of a number of variables and data types.', 'one example of each from the code.'),
         rows=[crit(S(17, 'Variable.'), 2, [],
                    parts=[(S(17, 'A variable is a placeholder for data', 'A parameter is a special kind of variable.'), 1, []),
                           (S(17, 'Examples from code: isbn, total, i, check_digit'), 1, [])],
                    note=S(17, 'For each term: Good description - clear understanding demonstrated 1 mark',
                           'Valid example 1 mark')),
               crit(S(17, 'Datatype'), 2, [],
                    parts=[(S(17, 'A category of data that can be held in a variable.', 'stored in a variable.'), 1, []),
                           (S(17, 'Examples from code: isbn is a string', 'are all integers'), 1, [])])]),
    dict(key=(15, 'b', 'iii'), topic='cs-2-2', qfigure='q15b-code', total=3,
         replaces='batch 1b: the answer was all or nothing at 3 against a 3 / 1 scale; the '
                  'listing was run into the stem as text',
         why='p22: the purpose of int; the scheme answers it, 3 / 1',
         stem=Q15B, ask=P(22, 'The program makes use of the Python int function.', 'as it is used in the code.'),
         rows=[crit(S(18, 'int converts (casts) the string representation', 'by its position.'), 3, [1],
                    note=S(18, 'Very good description - clear understanding demonstrated 3 marks',
                           'Fair description - limited understanding 1 mark'))]),
    dict(key=(15, 'b', 'iv'), topic='cs-2-2', qfigure='q15b-code', total=2,
         replaces='batch 1b: one of three answers was the only row, all or nothing at 2',
         why='p23: one use of range\'s integers; the scheme gives three, 2 / 1',
         stem=Q15B, ask=P(23, 'The range function on line 4 of the program', 'these integers are used in the program.'),
         rows=[ladder([S(18, 'As a loop counter / iterating variable'),
                       S(18, 'As an index into the list, isbn', 'scanning the digits from left to right'),
                       S(18, 'As the digit position')], [[1, 2]],
                      note=S(18, 'Very good description - clear understanding demonstrated 2 marks',
                             'Fair description - limited understanding 1 mark'))]),
    dict(key=(15, 'c', 'i'), topic='cs-2-2', qfigure='q15c-table', figure='s-q15c-i', total=5,
         replaces='batch 1b: the row was the trace table\'s header worth 5; the listing was run '
                  'into the stem as text',
         why='p23: complete the trace table; the scheme prints rows i = 7 to 10 (i, digit, '
             'total, isbn), 5 / 3 / 1',
         stem=Q15C, ask=P(23, 'Complete the trace table below to show the changing states', 'during program execution.'),
         rows=[crit(S(18, '7 0 27 102 8 2 43 10 9 0 43 1 10 1 53 0'), 5, [1, 3],
                    note=S(18, 'Full correct answer 5 marks', 'Any one correct row/col 1 mark'))]),
    dict(key=(15, 'c', 'ii'), topic='cs-2-2', qfigure='q15c-listing', total=3,
         replaces='batch 1b: the answer was all or nothing at 3 against a 3 / 1 scale; the '
                  'listing was run into the stem as text',
         why='p24: the purpose of isbn1; the scheme answers it, 3 / 1',
         stem=Q15C, ask=P(24, 'What is the purpose of the variable called isbn1 in the program?'),
         rows=[crit(S(19, 'isbn1 is used to store the original isbn as the value of isbn is changed'), 3, [1],
                    note=S(19, 'Very good description - clear understanding demonstrated 3 marks',
                           'Fair description - limited understanding 1 mark'))]),
    dict(key=(15, 'c', 'iii'), topic='cs-2-2', qfigure='q15c-listing', total=2,
         replaces='batch 1b: the listing was run into the stem as text and the operators were '
                  'missing from the ask',
         why='p24: the purpose of % and //; the scheme answers each, 1',
         stem=Q15C, ask=P(24, 'The program makes use of a number of arithmetic operators.', 'operators listed below.'),
         rows=[pt(S(19, '% is the modulus/remainder operator.', 'e.g. 9%4 -> 1'), 1,
                  note=S(19, 'For each operator: Good description - clear understanding demonstrated 1 mark')),
               pt(S(19, '// is the floor division operator.', 'e.g. 9//4 -> 2'), 1)]),
    dict(key=(15, 'c', 'iv'), topic='cs-2-2', qfigure='q15-progs', total=4,
         why='p24: two differences between the two programs; the scheme lists four, 2 each',
         ask=P(24, 'Identify two key differences between the algorithms used in parts (b) and (c).'),
         rows=[anyn([S(19, 'Use of string in program 1 and int in program 2', '(to store the ISBN)'),
                     S(19, 'Program 1 traverses string left to right', 'from right to left'),
                     S(19, 'Program 1 uses range to count from 10 down to 2', 'program 2 uses range to count from 2 up to 10'),
                     S(19, 'Program 1 does not modify the original isbn number', 'the original isbn.')], 2, 2,
                    head=P(24, 'Identify two key differences between the algorithms used in parts (b) and (c).'),
                    note=S(19, 'For each difference: Very good description - clear understanding demonstrated 2 marks'))]),
    dict(key=(15, 'c', 'v'), topic='cs-2-4', total=2,
         why='p24: a data entry error a check digit prevents; the scheme lists six, 2 / 1',
         ask=P(24, 'Provide an example of one type of data entry error', 'could be used to prevent.'),
         rows=[ladder([S(19, 'letter/digit errors, such as l → 1 or O → 0'),
                       S(19, 'single digit errors, such as 1 → 2'),
                       S(19, 'transposition errors, such as 12 → 21'),
                       S(19, 'twin errors, such as 11 → 22'),
                       S(19, 'jump transpositions errors, such as 132 → 231'),
                       S(19, 'jump twin errors, such as 131 → 232')], [[1, 2]],
                      note=S(19, 'Very good description - clear understanding demonstrated 2 marks',
                             'Fair description - limited understanding 1 mark', nth=2))]),
    # ── Section C ──────────────────────────────────────────────────────────
    dict(key=(16, 'a', 'i'), topic='cs-2-2', qfigure='q16a-code', figure='s-q16a-i', total=5,
         why='040 p5: change the first line of output; the scheme marks line 5 part (i), A-5 '
             'scale (0 or 5)',
         stem=Q16A_STEM,
         ask=C(5, 'Currently the first line in the program output is Dice simulation program.',
               'first line in the output is Dice simulation and analysis program.'),
         rows=[pt(S(21, CORRECT), 5, note=S(21, '(i) 5 marks (A-5 scale)', 'using solution above or similar.'))]),
    dict(key=(16, 'a', 'ii'), topic='cs-2-2', qfigure='q16a-code', figure='s-q16a-ii', total=5,
         replaces='batch 1b: the row was the almost-correct descriptor worth 5; filed as Section '
                  'B; the stem was the file-saving instructions; the figure carried prose and sat '
                  'on the answer side',
         why='040 p5: print the frequencies list at the end; the scheme marks line 33 part (ii), '
             'B-5 scale',
         stem=Q16A_STEM,
         ask=C(5, 'Insert a new line of code at the end of the program', 'This is the reason they are all zero.'),
         rows=[crit(S(21, CORRECT, nth=2), 5, [2, 3],
                    note=S(21, '(ii) 5 marks (B-5 scale)', 'Any other reasonable attempt.'))]),
    dict(key=(16, 'a', 'iii'), topic='cs-2-2', qfigure='q16a-code', figure='s-q16a-iii', total=5,
         replaces='batch 1b: the row was "error or \'off by one\' index error." -- the tail of a '
                  'scale step; filed as Section B; the stem was the file-saving instructions',
         why='040 p6: count threes to sixes; the scheme marks lines 19-28 part (iii), B-5 scale',
         stem=Q16A_STEM,
         ask=C(6, 'Complete the code to calculate the frequencies for the numbers three', 'the number six has been rolled 19 times.'),
         rows=[crit(S(21, CORRECT, nth=3), 5, [2, 3],
                    note=S(21, '(iii) 5 marks (B-5 scale)', 'Any other reasonable attempt.'))]),
    dict(key=(16, 'a', 'iv'), topic='cs-2-2', qfigure='q16a-code', figure='s-q16a-iv', total=5,
         why='040 p6: comment out the results line; the scheme marks line 31 part (iv), A-5 '
             'scale (0 or 5)',
         stem=Q16A_STEM,
         ask=C(6, 'Comment out the line that displays the list of individual results.',
               'Frequencies: [17, 21, 17, 18, 11, 16]'),
         rows=[pt(S(21, CORRECT, nth=4), 5, note=S(21, '(iv) 5 marks (A-5 scale)', 'using solution above or similar.'))]),
    dict(key=(16, 'a', 'v'), topic='cs-2-2', qfigure='q16a-code', figure='s-q16a-v', total=10,
         replaces='batch 1b: the row was the almost-correct descriptor worth 10; filed as '
                  'Section B; the stem was the file-saving instructions',
         why='040 p6: a Dice / Frequency table; the scheme marks lines 35-40 part (v), B-10 scale',
         stem=Q16A_STEM,
         ask=C(6, 'Extend the program to display the frequency of each number in a tabular format', '5 15 6 20'),
         rows=[crit(S(22, CORRECT), 10, [3, 7],
                    note=S(22, '(v) 10 marks (B-10 scale)', 'Any other reasonable attempt.'))]),
    dict(key=(16, 'a', 'vi'), topic='cs-2-2', qfigure='q16a-code', figure='s-q16a-vi', total=10,
         replaces='batch 1b: the row was the almost-correct descriptor worth 10; filed as '
                  'Section B; the stem was the file-saving instructions',
         why='040 p7: the number rolled most often; the scheme marks lines 42-45 part (vi), B-10 '
             'scale',
         stem=Q16A_STEM,
         ask=C(7, 'Extend the program so that it determines and displays the number', '5 was rolled the most often (25 times)'),
         rows=[crit(S(22, CORRECT, nth=2), 10, [3, 7],
                    note=S(22, '(vi) 10 marks (B-10 scale)', 'Any other reasonable attempt.'))]),
    dict(key=(16, 'a', 'vii'), topic='cs-2-2', qfigure='q16a-code', figure='s-q16a-vii', total=10,
         replaces='batch 1b: the row was "Separate newline for each row" (an almost-correct '
                  'example) worth 10; filed as Section B; topic was Computer systems',
         why='040 p7: a horizontal bar chart of asterisks; the scheme marks lines 47-53 part '
             '(vii), C-10 scale. Filed under Algorithms like the rest of Q16',
         stem=Q16A_STEM,
         ask=C(7, 'Extend the program to display a horizontal bar chart of the frequencies.', '**********', end_nth=49),
         rows=[crit(S(22, CORRECT, nth=3), 10, [3, 5, 8],
                    note=S(22, '(vii) 10 marks (C-10 scale)', 'Any other reasonable attempt.'))]),
]
