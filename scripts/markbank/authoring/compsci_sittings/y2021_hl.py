"""Computer Science 2021 Higher Level: every card of the sitting, lifted from the page.

The 44 cards shipped in August are re-authored here under their own ids (batch
1b), and the 9 the lane added for the asks they missed are kept, converted to
the ladder and instruction rules of 5 Nov. Paper pages 3-28 (Sections A and B)
and Section C pages 3-5, and scheme pages 3-26 were opened. Q13(a)'s three
asks are Eircodes the candidate must say are invalid; each is carded with the
paper's instruction and its own code.

cs-2021-hl-q2, -q3, -q4, -q5, -q7, -q8, -q9, -q10 and -q11 are shipped as
whole questions (two parts, no part cards beside them) and stay whole with a
row per part.

Scheme page 4 sets Q2(b)'s answers in Cambria Math, whose text layer doubles
every glyph and misreads its digits; (b)(i)'s line needs glyph id 2783, which
has no settled reading, and (b)(ii)'s needs the letters of log, which the
glyph reader refuses. Both are carded on the words the text layer reads
cleanly, with the scheme's two lines as the solution crop. Scheme page 18 sets
Q14(b)(iv)'s (n, m) the same way; its row is the clean sentence and the
scheme's lines are the solution crop.

Paper page 22 sets Q14(b)(iv)'s and (v)'s (n, m) and n != m in Cambria, whose
text layer files them under U+123A, U+123B and U+0D4D (rendered and looked
at: a parenthesis pair and a not-equals sign), which LANE_GLYPHS folds (added
by the coordinator, 5 Nov).

The Section A questions shipped whole have each row tied to its printed part
with ofpart() (coordinator, 5 Nov).
"""
from compsci_lane import (C, G, P, Pair, S, anyn, crit, crop, ladder, ofpart, pt, stack)  # noqa: F401

CROPS = {
    'q6-code': crop('038', 7, (52, 145, 542, 302), ref='2021 HL Q6',
                    alt='The eleven-line Python program printed with Question 6: the numbers of '
                        'adults and children are read in; if num_adults > 1 and num_children > 0 '
                        'it prints Family discount, elif num_adults >= 10 Large group discount, '
                        'elif num_adults >= 5 Small group discount, else No discount.'),
    'q12-table': crop('038', 12, (128, 106, 468, 236), ref='2021 HL Q12',
                      alt='The table printed with Question 12, columns dog_name, breed, dob and '
                          'microchip: rover, labrador, 22/11/2011, Y; fido, poodle, 02/02/2020, Y; '
                          'fido, jack russell, 15/06/2015, N; champ, greyhound, 01/01/2010, Y; '
                          'spot, dalmation, 24/08/2007, N; buddy, rottweiler, 21/10/2012, Y.'),
    'q13-fig4': crop('038', 13, (96, 279, 499, 390), ref='2021 HL Q13(a)',
                     alt='Figure 4: the Eircode A65 F4E2 split into a three-character Routing '
                         'Key, A65, and a four-character Unique Identifier, F4E2.'),
    'q13c-i': crop('038', 16, (52, 99, 542, 131), ref='2021 HL Q13(c)(i)',
                   alt='Lines 11 and 12 of the program in part (b): if not '
                       'test_eircode[0].isalpha(): return False.'),
    'q13c-ii': stack([('038', 16, (52, 275, 542, 294)), ('038', 16, (84, 372, 511, 478))],
                     ref='2021 HL Q13(c)(ii)',
                     alt='Line 16 of the program, if ((not test_eircode[1].isdigit()) or (not '
                         'test_eircode[2].isdigit())):, above the truth table with columns P, Q, '
                         'not P, not Q and not P or not Q; P and Q are filled in as False False, '
                         'False True, True False and True True, and the other columns are blank.'),
    'q13c-iv': crop('038', 17, (52, 98, 542, 117), ref='2021 HL Q13(c)(iv)',
                    alt='Line 16 of the program: if ((not test_eircode[1].isdigit()) or (not '
                        'test_eircode[2].isdigit())):'),
    's-q12b': crop('scheme', 11, (53, 168, 493, 358), ref='2021 HL Q12(b)', solution=True,
                   alt='The marking scheme\'s redesign for Question 12(b): an owners table '
                       '(owner_id, owner_name, address: 1 Joe Murphy, 1 main street; 2 Ada '
                       'Traore, 9 park ave.; 3 James Tidy, 7 bond st.) above a dogs table '
                       '(dog_id, dog_name, breed, dob, microchip, owner_id) in which rover, fido '
                       'the poodle and champ have owner_id 1, fido the jack russell and spot '
                       'have 2, and buddy has 3.'),
    'q5-flow': stack([('038', 6, (203, 94, 392, 466)), ('038', 6, (142, 518, 484, 629))],
                     ref='2021 HL Q5',
                     alt='Figure 1: a flowchart. Start; INITIALISE count, total and n to 0; while '
                         'count < 3 is TRUE, INPUT n, LET total = total + n, LET count = count + '
                         '1 and loop back; when FALSE, PRINT total/count, then Stop. Below it, the '
                         'trace table with columns n, total and count: a first row 0, 0, 0, then '
                         'rows for n = 7, 3 and 8 with total and count blank.'),
    'q8-fig2': stack([('038', 8, (468, 495, 544, 585)), ('038', 9, (52, 101, 540, 192))],
                     ref='2021 HL Q8',
                     alt='Figure 2: a yellow thumbs-up emoji. Below it, the answer grid for part '
                         '(b): 1F44D above five groups of four boxes, the first group filled in as '
                         '0 0 0 1 and the other sixteen boxes blank.'),
    'q9-fig3': crop('038', 10, (147, 87, 453, 237), ref='2021 HL Q9',
                    alt='Figure 3: four stacked layers of an operating system, from top to '
                        'bottom I/O Management, File System, Memory Management and Processor '
                        'Scheduling.'),
    'q13b-code': crop('038', 14, (52, 88, 542, 378), ref='2021 HL Q13(b)',
                      alt='The 22-line Python function is_valid_eircode(test_eircode) printed with '
                          'Question 13(b): comment lines on what it checks and on isalpha, isdigit '
                          'and isalnum; then if not test_eircode[0].isalpha(): return False; if '
                          '((not test_eircode[1].isdigit()) or (not test_eircode[2].isdigit())): '
                          'return False; if not test_eircode[-4:].isalnum(): return False; and '
                          'return True.'),
    'q13c-iii': stack([('038', 16, (52, 274, 542, 295)), ('038', 16, (134, 538, 480, 645))],
                      ref='2021 HL Q13(c)(iii)',
                      alt='Line 16 of the program, if ((not test_eircode[1].isdigit()) or (not '
                          'test_eircode[2].isdigit())):, above the truth table with columns P, Q, '
                          'P and Q and not (P and Q); P and Q are filled in as False False, False '
                          'True, True False and True True, and the other columns are blank.'),
    'q14a-table': crop('038', 18, (145, 358, 451, 413), ref='2021 HL Q14(a)',
                       alt='The win/loss table printed with Question 14(a): for 0, 1, 2, 3 and 4 '
                           'matchsticks remaining, the positions L, W, W, L, W.'),
    'q14b-tree': crop('038', 21, (68, 351, 460, 554), ref='2021 HL Q14(b)(i)',
                      alt='The partially completed game diagram printed with Question 14(b)(i): '
                          'from state 1, 2 three moves branch out, AX1, AY1 and AY2. Only AX1 is '
                          'completed: it leads to 0, 2, from which BY1 leads to 0, 1 and then AY1 '
                          'to 0, 0, A wins, and BY2 leads to 0, 0, B wins.'),
    'q16a-code': crop('040', 3, (81, 356, 550, 619), ref='2021 HL Q16(a)',
                      alt='The 17-line program Question16_A.py as printed in the Section C '
                          'booklet: a function is_anagram(w1, w2) returning True if sorted(w1) == '
                          'sorted(w2) and False otherwise; word1 read with input, word2 = '
                          '"SILENT"; then if (sorted(word1) == sorted(word2)): print("YES").'),
    's-q2b': stack([('scheme', 4, (83, 569, 445, 590)), ('scheme', 4, (83, 620, 400, 641))],
                   ref='2021 HL Q2(b)', solution=True,
                   alt='The marking scheme\'s two answers to Question 2(b): (i) 2 to the power 4 '
                       '= 16 unique pieces of information can be represented using four-bits; '
                       '(ii) log base 2 of 8 = 3 bits can represent 8 unique pieces of '
                       'information.'),
    's-q5': crop('scheme', 6, (216, 446, 380, 558), ref='2021 HL Q5', solution=True,
                 alt='The marking scheme\'s completed trace table for Question 5: n, total, count '
                     '0 0 0; 7 7 1; 3 10 2; 8 18 3.'),
    's-q14b-i': crop('scheme', 17, (91, 469, 503, 706), ref='2021 HL Q14(b)(i)', solution=True,
                     alt='The marking scheme\'s completed game diagram for Question 14(b)(i): from '
                         '1, 2 the branch AX1 as printed; AY1 to 1, 1, from which BX1 leads to 0, '
                         '1 and AY1 to 0, 0, A wins, and BY1 leads to 1, 0 and AX1 to 0, 0, A '
                         'wins; and AY2 to 1, 0, from which BX1 leads to 0, 0, B wins.'),
    's-q14b-iv': crop('scheme', 18, (90, 580, 540, 650), ref='2021 HL Q14(b)(iv)', solution=True,
                      alt='The marking scheme\'s answer to Question 14(b)(iv): a winning strategy '
                          'from state (n, m) where n is not equal to m would be to even the '
                          'piles, leaving (n, n) or (m, m); for m > n take m - n matchsticks, and '
                          'for m < n take n - m matchsticks.'),
    's-q16a-i': crop('scheme', 23, (57, 321.2, 545, 335.5), ref='2021 HL Q16(a)(i)', solution=True,
                     alt='Line 12 of the marking scheme\'s possible solution: word2 = '
                         'input("Enter the second word: ") # Solution (i).'),
    's-q16a-ii': crop('scheme', 23, (57, 392.8, 545, 407.1), ref='2021 HL Q16(a)(ii)', solution=True,
                      alt='Line 17 of the marking scheme\'s possible solution: print(word1, "is an '
                          'anagram of", word2) # (ii).'),
    's-q16a-iii': crop('scheme', 23, (57, 407.1, 545, 435.8), ref='2021 HL Q16(a)(iii)', solution=True,
                       alt='Lines 18 and 19 of the marking scheme\'s possible solution: else: '
                           'print(word1, "is NOT an anagram of", word2) # (iii).'),
    's-q16a-iv': crop('scheme', 23, (57, 378.5, 545, 392.8), ref='2021 HL Q16(a)(iv)', solution=True,
                      alt='Line 16 of the marking scheme\'s possible solution: if '
                          '(sorted(word1.upper()) == sorted(word2.upper())): # (iv).'),
    's-q16a-v': crop('scheme', 23, (57, 450.2, 545, 521.7), ref='2021 HL Q16(a)(v)', solution=True,
                     alt='Lines 21 to 25 of the marking scheme\'s possible solution: # (v), then if '
                         '(is_anagram(word1.upper(), word2.upper())): print(word1, "is an anagram '
                         'of", word2), else: print(word1, "is NOT an anagram of", word2).'),
    's-q16a-vi': crop('scheme', 23, (57, 550.5, 545, 722.4), ref='2021 HL Q16(a)(vi)', solution=True,
                      alt='Lines 28 to 39 of the marking scheme\'s possible solution, # Part (vi): '
                          'phrase read with input, phrase_no_spaces = phrase.replace(" ", ""), '
                          'then for word1 and for word2 in turn, if is_anagram(word.upper(), '
                          'phrase_no_spaces.upper()) print that it is an anagram of the phrase, '
                          'else that it is NOT.'),
}

Q12_TARIFF = S(10, 'Question 12 2+3 marks')
Q13_STEM = P(13, 'Eircode is the postal address code system', 'is shown below in Figure 4.')
Q13A = P(13, 'Explain why each of the following are not valid Eircodes.')
Q13B = [Q13_STEM, P(14, 'The intention of the Python code shown below is to implement a validation check for an Eircode.')]
Q13C = P(16, 'The following questions are based on the code in part (b).')
Q14A_STEM = P(18, 'Consider a two', 'or 4 matchsticks left on the board.')
Q14B_STEM = P(21, 'Consider a variation of the game described in part (a)', 'removes the last matchstick(s) wins the game.')
Q15_STEM = P(24, 'Charles Stark Draper is often credited', 'the principles of universal design.')
Q15B = [Q15_STEM, P(26, 'According to the description provided in part (a)', 'contain multiple embedded systems.')]
Q16A_STEM = C(3, 'The Python program shown below tests whether the strings', 'will not be used until part (v).')
CORRECT = 'Correct implementation using solution above or similar.'

CARDS = [
    # ── Section A ──────────────────────────────────────────────────────────
    dict(key=(1, None, None), topic='cs-2-2', qfigure='q1-code0', total=5,
         replaces='batch 1b: the output was lost (no answer rows); the listing sat on the answer '
                  'side',
         why='p3: the output of a 12-line program; the scheme prints the four lines, the first '
             'full correct response 2 and each further one 1. The shipped crop of the listing '
             'was opened and is complete',
         ask=P(3, 'What is the output of the following piece of Python code?'),
         rows=[anyn([S(4, 'x is 3'), S(4, '7 3'), S(4, '6 8'), S(4, 'y is y')], 4, 1, steps=[2, 1, 1, 1],
                    head=S(4, 'Output'),
                    note=S(4, 'First full correct response 2 marks', 'Each additional correct response 1 mark'))]),
    dict(key=(2, None, None), topic='cs-2-3', figure='s-q2b', total=5,
         replaces='batch 1b: unpriced question-total rows; (b)\'s answers, set in Cambria Math, '
                  'were lost',
         why='p3-4: shipped as the whole of Q2. (a) why binary, two answers 3 / 1; (b)(i) and '
             '(ii), 1 each: the scheme sets 2 to the 4 = 16 and log2 8 = 3 in Cambria Math, whose '
             'text layer misreads them; both lines are read by glyph id (glyph block of '
             '2021-hl.md) and the solution crop shows them as printed',
         ask=[P(3, '(a) Explain why data is stored in computers in binary format.'),
              P(4, '(b) A single bit can be used to represent two pieces of information.',
                'represent eight unique pieces of information?')],
         rows=[ofpart(P(3, '(a)'), ladder([S(4, 'The circuits in a computer\'s processor are made up of transistors.', 'on and off states of a transistor.'),
                       S(4, 'As there are only two possible states, binary is more reliable', 'number systems.')], [[1, 3]],
                      note=S(4, 'Very good explanation - clear understanding demonstrated 3 marks',
                             'Fair explanation - limited understanding 1 mark'))),
               ofpart(P(4, '(i)'), pt(G(4, '2⁴ = 16', 'four-bits.'), 1,
                                      note=S(4, 'Correct 1 mark'))),
               ofpart(P(4, '(ii)'), pt(G(4, 'log₂ 8 = 3', 'unique pieces of information.'), 1))]),
    dict(key=(3, None, None), topic='cs-2-3', total=5,
         replaces='batch 1b: unpriced question-total rows',
         why='p4-5: shipped as the whole of Q3. (a) two differences between RAM and ROM, nine '
             'listed, 1 each; (b) how more RAM helps, two answers 3 / 1',
         ask=[P(4, '(a) State two differences between RAM and ROM.'),
              P(5, '(b) Explain how increasing the amount of RAM', 'improve its performance.')],
         rows=[ofpart(P(4, '(a)'), anyn([S(5, 'RAM can be written, whereas ROM is read-only.'), S(5, 'RAM chips can be read faster than ROM.'),
                     S(5, 'ROM is non-volatile storage', 'retain information.'),
                     S(5, 'Data/information in ROM is permanent', 'temporary information.'),
                     S(5, 'CPU cannot access data that is stored in ROM directly', 'transferred to RAM first.'),
                     S(5, 'ROM is used primarily in the start-up process', 'loading the operating system.'),
                     S(5, 'Capacity. RAM can store multiple gigabytes', '4-8MB per chip.'),
                     S(5, 'Physically RAM chips are bigger than ROM chips (of the same capacity).'),
                     S(5, 'The cost of RAM chips tends to be higher than ROM.'),
                     S(5, 'Or any similar relevant difference.')], 2, 1, open_list=True,
                    head=P(4, 'State two differences between RAM and ROM.'),
                    note=S(5, 'Each correct response 1 mark'))),
               ofpart(P(5, '(b)'), ladder([S(5, 'More RAM means more applications can be loaded', 'running user applications.'),
                       S(5, 'Better performance means applications run faster', 'response times for user.')], [[1, 3]],
                      note=S(5, 'Very good explanation - clear understanding demonstrated 3 marks',
                             'Fair explanation - limited understanding 1 mark')))]),
    dict(key=(4, None, None), topic='cs-2-2', qfigure='q4-code0', total=5,
         replaces='batch 1b: unpriced question-total rows; the two lines of code sat on the '
                  'answer side',
         why='p5: shipped as the whole of Q4. (a) why the swap fails, two answers, 2; (b) a '
             'working method, four given, 3 / 1. The shipped crop of the two lines was opened '
             'and is complete',
         stem=P(5, 'You are asked to swap the values of two variables', 'which have already been initialised.'),
         ask=P(5, '(a) Why does the method shown not work?', '(b) Describe a method that does work.'),
         rows=[ofpart(P(5, '(a)'), anyn([S(5, 'The method does not work because the contents of x', 'after the first assignment.'),
                     S(5, 'A temporary variable is needed.')], 1, 2,
                    head=P(5, 'Why does the method shown not work?'),
                    note=S(5, 'Good description - clear information 2 marks'))),
               ofpart(P(5, '(b)', nth=2), ladder([S(6, 'Use a temporary variable temp = x x = y y = temp'),
                       S(6, 'use Python’s canonical swap x, y = y, x'),
                       S(6, 'use addition/subtraction operators x = x + y y = x - y x = x - y'),
                       S(6, 'use multiplication/division operators x = x * y y = x / y x = x / y')], [[1, 3]],
                      instruction=S(6, 'or any other valid solution'),
                      note=S(6, 'Very good description - clear understanding demonstrated 3 marks',
                             'Fair description - limited understanding 1 mark')))]),
    dict(key=(5, None, None), topic='cs-2-2', qfigure='q5-flow', figure='s-q5', total=5,
         replaces='batch 1b: unpriced question-total rows; the figure carried (a)\'s ask and sat '
                  'on the answer side',
         why='p6: shipped as the whole of Q5. (a) the trace for 7, 3 and 8 (rows n, total, '
             'count), 3 / 2 / 1; (b) the output, 18/3 = 6, 2',
         stem=P(6, 'The flowchart in Figure 1 is a representation of an algorithm.'),
         ask=P(6, '(a) Using inputs of 7, 3 and 8 for n', 'What output does the algorithm display?'),
         rows=[ofpart(P(6, '(a)'), crit(S(6, '7 7 1', '8 18 3'), 3, [1, 2], head=S(6, 'n total count'),
                                         note=S(6, 'First correct column 2 marks', 'One correct value 1 mark'))),
               ofpart(P(6, '(b)'), pt(S(6, '18/3=6'), 2, note=S(6, 'Full correct response 2 marks')))]),
    dict(key=(6, None, None), topic='cs-1-2', qfigure='q6-code', total=5,
         why='p7: two scenarios where the discount algorithm is unfair; the scheme lists four, '
             'best 3 and second 2',
         stem=P(7, 'You have been asked to assess an algorithm', 'in a travelling group.'),
         ask=P(7, 'Describe two scenarios where the algorithm could be perceived to be unfair.'),
         rows=[anyn([S(7, 'Family discount should be allowed', 'single-parent families.'),
                     S(7, 'You could have any number of children', 'get no discount.'),
                     S(7, 'If num_adults >= 10 and num_children > 0', '(as opposed to family discount).'),
                     S(7, 'Children don\'t contribute to large or small group discounts.'),
                     S(7, 'Any valid scenario.')], 2, 3, steps=[3, 2], open_list=True,
                    head=P(7, 'Describe two scenarios where the algorithm could be perceived to be unfair.'),
                    note=S(7, 'Scenario 1 (best scenario).', 'clear understanding 2 marks'))]),
    dict(key=(7, None, None), topic='cs-2-3', total=5,
         replaces='batch 1b: unpriced question-total rows',
         why='p8: shipped as the whole of Q7. (a) HTTP against HTTPS, four answers, 2; (b) how '
             'TCP is reliable, 3 / 1',
         ask=P(8, '(a) Differentiate between HTTP and HTTPS.', 'reliable communication between computers.'),
         rows=[ofpart(P(8, '(a)'), anyn([S(7, 'HTTP is unsecured while HTTPS is secured.'),
                     S(7, 'HTTP sends data over port 80 while HTTPS uses port 443.'),
                     S(7, 'HTTP operates at application layer, while HTTPS operates at transport layer.'),
                     S(7, 'No SSL certificates are required for HTTP', 'signed by a CA.')], 1, 2,
                    head=P(8, 'Differentiate between HTTP and HTTPS.'),
                    note=S(7, 'Good description - clear information 2 marks'))),
               ofpart(P(8, '(b)'), crit(S(7, 'TCP breaks messages into chunks called packets', 'or the entire message.'), 3, [1],
                                        note=S(7, 'Very good explanation - clear understanding demonstrated 3 marks',
                                               'Fair explanation - limited understanding 1 mark')))]),
    dict(key=(8, None, None), topic='cs-2-3', qfigure='q8-fig2', total=5,
         replaces='batch 1b: unpriced question-total rows; Figure 2 was missing and the binary '
                  'grid sat on the answer side',
         why='p8-9: shipped as the whole of Q8. (a) why ASCII has no emoji, three answers, 2; (b) '
             '1F44D in binary, 3 / 2 / 1',
         stem=P(8, 'The Unicode representation for the ‘thumbs up’ emoji', 'is the hexadecimal number 1F44D.'),
         ask=[P(8, '(a) Explain why emoji characters are not represented', 'Interchange (ASCII).'),
              P(9, '(b) Express the hexadecimal number 1F44D as a binary number.', 'completed for you.')],
         rows=[ofpart(P(8, '(a)', nth=2), anyn([S(8, 'ASCII is a 7-bit system', 'used by old teletype machines.'),
                     S(8, 'Since emoji characters were not ‘invented’', 'part of the ASCII character set.'),
                     S(8, 'Emoji characters are represented using Unicode.')], 1, 2,
                    head=P(8, 'Explain why emoji characters are not represented', 'Interchange (ASCII).'),
                    note=S(8, 'Good explanation - clear information 2 marks'))),
               ofpart(P(9, '(b)'), crit(S(8, '0001 1111 0100 0100 1101'), 3, [1, 2],
                                        note=S(8, 'Correct 3 marks', 'Response with some merit 1 mark')))]),
    dict(key=(9, None, None), topic='cs-2-3', qfigure='q9-fig3', total=5,
         replaces='batch 1b: unpriced question-total rows; Figure 3 sat on the answer side with a '
                  'stray rule',
         why='p9-10: shipped as the whole of Q9. (a) what an OS is, three answers, 2; (b) two '
             'layers explained, 2 / 1 each to a maximum of 3 (one item on [1, 2], one on [1])',
         ask=[P(9, '(a) What is an operating system?'),
              P(10, '(b) The diagram in Figure 3 depicts some of the main layers', 'explain their function.')],
         rows=[ofpart(P(9, '(a)'), anyn([S(8, 'An OS is the software that controls the hardware of a computer.'),
                     S(8, 'Acts as an interface between other software and the hardware.'),
                     S(8, 'Acts as an interface between the user and the machine.')], 1, 2,
                    head=P(9, 'What is an operating system?'),
                    note=S(8, 'Good description - clear information 2 marks'))),
               ofpart(P(10, '(b)'), ladder([Pair(S(8, 'I/O Management'), S(8, 'Controls the user interface', 'screen sizes, resolutions etc.).')),
                       Pair(S(8, 'I/O Management'), S(8, 'Provides access to peripheral devices (through device drivers).')),
                       Pair(S(8, 'File System'), S(8, 'Keeps track of where files are located', 'in FAT systems).')),
                       Pair(S(8, 'File System'), S(8, 'Controls access to files (e.g. sequential vs direct access).')),
                       Pair(S(8, 'File System'), S(8, 'Handles file security.')),
                       Pair(S(8, 'File System'), S(8, 'Implements disk scheduling policy', 'first-served).')),
                       Pair(S(8, 'Memory Management'), S(8, 'Allocation of RAM.')),
                       Pair(S(8, 'Memory Management'), S(9, 'Loads data in from secondary to primary storage.')),
                       Pair(S(8, 'Memory Management'), S(9, 'Swaps data out from primary to secondary.')),
                       Pair(S(9, 'Processor Scheduling'), S(9, 'Decides which job to run next', 'round robin).')),
                       Pair(S(9, 'Processor Scheduling'), S(9, 'Maintains the state of each process', 'ready/waiting/running/ended).')),
                       Pair(S(9, 'Processor Scheduling'), S(9, 'Deadlock avoidance.')),
                       Pair(S(9, 'Processor Scheduling'), S(9, 'Handles multitasking.')),
                       Pair(S(9, 'Processor Scheduling'), S(9, 'Handles multiple users.'))], [[1, 2], [1]],
                      note=S(9, 'For each layer up to a total possible maximum of 3 marks:',
                             'Fair explanation - limited understanding 1 mark')))]),
    dict(key=(10, None, None), topic='cs-1-3', total=5,
         replaces='batch 1b: unpriced question-total rows; topic was Computer systems',
         why='p10-11: shipped as the whole of Q10. (a) two tasks of a project manager, seven '
             'listed, 1 each; (b) low-level against high-level programs, two answers 3 / 1. '
             'Filed under Designing and developing',
         ask=[P(10, '(a) State two tasks that would be undertaken by a project manager', 'software design process.'),
              P(11, '(b) Some programming roles require the knowledge', 'high‐level computer program?')],
         rows=[ofpart(P(10, '(a)'), anyn([S(9, 'To agree requirements with customer.'),
                     S(9, 'To ensure system/project is delivered on time and within budget.'),
                     S(9, 'To oversee project schedule – planning - set key dates/milestones.'),
                     S(9, 'To resource project – staffing, equipment, finance etc.'),
                     S(9, 'To assign tasks related to design, implementation, testing etc.'),
                     S(9, 'To communicate with and motivate team and ongoing liaison with customer.'),
                     S(9, 'To monitor project progress.'), S(9, 'Any relevant task.')], 2, 1, open_list=True,
                    head=P(10, 'State two tasks that would be undertaken by a project manager', 'software design process.'),
                    note=S(9, 'For each correctly stated task 1 mark'))),
               ofpart(P(11, '(b)'), ladder([S(9, 'High level languages such as Python and JavaScript', 'High level languages are machine independent.'),
                       S(9, 'Low level languages are used to write code', 'code written only using 1’s and 0’s).')], [[1, 3]],
                      note=S(9, 'Very good description - clear understanding demonstrated 3 marks',
                             'Fair description - limited understanding 1 mark')))]),
    dict(key=(11, None, None), topic='cs-3-3', total=5,
         replaces='batch 1b: unpriced question-total rows; topic was Algorithms',
         why='p11: shipped as the whole of Q11. (a) two benefits of computer modelling, four '
             'listed, 1 each; (b) agent-based modelling in the pandemic, two answers 3 / 1. '
             'Filed under Modelling and simulation',
         ask=P(11, '(a) State two benefits of computer modelling.', 'influence public health policy.'),
         rows=[ofpart(P(11, '(a)'), anyn([S(10, 'To test the feasibility of some idea', 'is it worthwhile to vaccinate?'),
                     S(10, 'To make predictions/demonstrate emergent behaviour', 'against the spread of a virus).'),
                     S(10, 'To run simulations and be used as a basis for discussion', 'understanding of a phenomena.'),
                     S(10, 'To enable solutions to problems that are difficult to solve analytically', 'scale or complexity).'),
                     S(10, 'Or similar.')], 2, 1, open_list=True,
                    head=P(11, 'State two benefits of computer modelling.'),
                    note=S(10, 'For each correctly stated benefit 1 mark'))),
               ofpart(P(11, '(b)', nth=2), ladder([S(10, 'Agent-based modelling (ABM) for COVID 19 could have behavioural rules', 'during its interactions.'),
                       S(10, 'ABMs can be used to predict outcomes for certain scenarios', 'foreign travel etc.')], [[1, 3]],
                      note=S(10, 'Very good explanation - clear understanding demonstrated 3 marks',
                             'Fair explanation - limited understanding 1 mark')))]),
    dict(key=(12, 'a', None), topic='cs-3-1', qfigure='q12-table', total=2, printed=Q12_TARIFF,
         why='p12: why dog_name and breed are poor primary keys; the scheme gives a reason for '
             'each, 1 mark each',
         stem=P(12, 'The following selection of data is taken from a table', 'information about dogs.'),
         ask=[P(12, 'State why each of the following fields would not be good candidates', 'table shown above.'),
              P(12, 'dog_name: breed:')],
         rows=[pt(S(10, 'dog_name would not be a good PK', 'i.e. fido.'), 1,
                  note=S(10, 'The value of a primary key (PK) must be unique:')),
               pt(S(10, 'breed would not be a good PK because duplicates could exist.'), 1,
                  note=S(10, 'both fields could potentially contain duplicates.'))]),
    dict(key=(12, 'b', None), topic='cs-3-1', qfigure='q12-table', figure='s-q12b', total=3,
         printed=Q12_TARIFF,
         why='p12: how a foreign key improves the design; the scheme explains it and draws the '
             'two tables, 3 / 1',
         stem=P(12, 'The following selection of data is taken from a table', 'information about dogs.'),
         ask=P(12, 'One owner can own many dogs.', 'improve the design of this database.'),
         rows=[crit(S(11, 'A foreign key(FK) links two tables.', 'the FK in the dogs table.'), 3, [1],
                    note=S(11, 'Very good explanation - clear understanding demonstrated 3 marks',
                           'Fair explanation - limited understanding 1 mark'))]),
    # ── Section B ──────────────────────────────────────────────────────────
    dict(key=(13, 'a', 'i'), topic='cs-2-4', qfigure='q13-fig4', total=1,
         why='p13: why GA5 AOK1 is not a valid Eircode; the scheme gives the reason, 1 mark',
         stem=Q13_STEM, ask=[Q13A, P(13, 'GA5 AOK1')],
         rows=[anyn([S(12, 'The second character (‘A’) is not a digit.'), S(12, 'Any other valid reason.', nth=1)],
                    1, 1, head=Q13A, open_list=True)]),
    dict(key=(13, 'a', 'ii'), topic='cs-2-4', qfigure='q13-fig4', total=1,
         why='p13: why X234 Y56 is not a valid Eircode; the scheme gives three reasons, 1 mark',
         stem=Q13_STEM, ask=[Q13A, P(13, 'X234 Y56')],
         rows=[anyn([S(12, 'The routing key must be 3 characters (and not 4).'),
                     S(12, 'The unique ID must be 4 characters (and not 3).'),
                     S(12, 'The unique ID must be after the routing key .'),
                     S(12, 'Any other valid reason.', nth=2)], 1, 1, head=Q13A, open_list=True)]),
    dict(key=(13, 'a', 'iii'), topic='cs-2-4', qfigure='q13-fig4', total=1,
         why='p13: why 8XT A43Y is not a valid Eircode; the scheme gives three reasons, 1 mark',
         stem=Q13_STEM, ask=[Q13A, P(13, '8XT A43Y')],
         rows=[anyn([S(12, 'The first character (‘8’) is not a letter.'),
                     S(12, 'The second character (‘X’) is not a digit.'),
                     S(12, 'The third character (‘T’) is not a digit.'),
                     S(12, 'Any other valid reason.', nth=3)], 1, 1, head=Q13A, open_list=True)]),
    dict(key=(13, 'b', 'i'), topic='cs-2-5', qfigure='q13b-code', total=2,
         replaces='batch 1b: Figure 4 sat on the answer side instead of the code; topic was '
                  'Algorithms',
         why='p14: what a validation check is; the scheme answers it, 2. Filed under Evaluation '
             'and testing',
         stem=Q13B, ask=P(14, 'What is meant by the term ‘validation check’?'),
         rows=[pt(S(12, 'A validation check is a test carried out by a program', 'provided at the start of the question.'), 2,
                  note=S(12, 'Good explanation - clear understanding demonstrated 2 marks'))]),
    dict(key=(13, 'b', 'ii'), topic='cs-2-5', qfigure='q13b-code', total=2,
         replaces='batch 1b: Figure 4 sat on the answer side instead of the code; topic was '
                  'Algorithms',
         why='p14: how a test case tests the code; the scheme answers it, 2. Filed under '
             'Evaluation and testing',
         stem=Q13B, ask=P(14, 'Outline briefly how a test case could be used to test the above code.'),
         rows=[pt(S(13, 'A test case would be any value passed into the function.', 'False otherwise.'), 2,
                  note=S(13, 'Good explanation - clear understanding demonstrated 2 marks'))]),
    dict(key=(13, 'b', 'iii'), topic='cs-2-5', qfigure='q13b-code', total=4,
         replaces='batch 1b: the two kinds of testing were not separated or priced 2 each; '
                  'topic was Algorithms',
         why='p15: unit against system testing; the scheme describes each, 2 each. Filed under '
             'Evaluation and testing',
         stem=Q13B, ask=P(15, 'Two types of testing that could be performed', 'Distinguish between these two types of testing.'),
         rows=[anyn([S(13, 'Usually carried out by the programmer.'), S(13, 'The purpose of unit testing is to test specific units of code.'),
                     S(13, 'Test cases are designed to trigger all execution paths in the code.'), S(13, 'Typically automated.'),
                     S(13, 'A form of white box testing', 'familiar with the code being tested).')], 1, 2,
                    head=S(13, 'Unit Testing'),
                    note=S(13, 'For each of Unit Testing/System Testing Good explanation - clear understanding demonstrated 2 marks')),
               anyn([S(13, 'Usually carried out by testers.'), S(13, 'The overall aim of system testing is to determine', 'supposed/designed to do).'),
                     S(13, 'System testing includes testing how the system operates', 'under stressed conditions.'),
                     S(13, 'Typically carried out by testers (proxies for end-users).'),
                     S(13, 'A form of black box testing', 'unfamiliar with the code being tested).')], 1, 2,
                    head=S(13, 'System Testing'))]),
    dict(key=(13, 'b', 'iv'), topic='cs-2-2', qfigure='q13b-code', total=2,
         replaces='batch 1b: Figure 4 sat on the answer side instead of the code',
         why='p15: why A99 SP@M A1OK passes; the scheme answers it, 2',
         stem=Q13B, ask=P(15, 'This Python code will show that the Eircode', 'indicate that this Eircode is valid?'),
         rows=[pt(S(13, 'The function only looks at the first three characters', 'any characters in between .'), 2,
                  note=S(13, 'Very good explanation - clear understanding demonstrated 2 marks'))]),
    dict(key=(13, 'b', 'v'), topic='cs-2-5', qfigure='q13b-code', total=5,
         replaces='batch 1b: Figure 4 sat on the answer side; topic was Computer systems',
         why='p15: why regression testing matters; the scheme answers it, 5. Filed under '
             'Evaluation and testing',
         stem=Q13B, ask=P(15, 'After code has been changed it is important to conduct regression testing.', 'Why is this important?'),
         rows=[pt(S(14, 'Regression testing is important because', 'implementing a software update.'), 5,
                  note=S(14, 'Good explanation - clear understanding demonstrated 5 marks'))]),
    dict(key=(13, 'c', 'i'), topic='cs-2-2', qfigure='q13c-i', total=2,
         why='p16: what lines 11-12 do; the scheme explains it, 2 marks',
         stem=Q13C,
         ask=P(16, 'Explain what the following code does:'),
         rows=[pt(S(14, 'The Python code checks whether the first character', 'the function will return False'), 2,
                  note=S(14, 'Good explanation - clear understanding demonstrated 2 marks'))]),
    dict(key=(13, 'c', 'ii'), topic='cs-2-3', qfigure='q13c-ii', total=4,
         why='p16: the truth table for not P or not Q; the scheme prints it, 1 per correct row',
         stem=Q13C,
         ask=P(16, 'If we let P represent the possible boolean values', 'for the expression, not P or not Q.'),
         rows=[pt(S(14, 'False False True True True'), 1,
                  note=S(14, '1 Mark per correct row OR', 'more than 2 correct values in each column')),
               pt(S(14, 'False True True False True'), 1),
               pt(S(14, 'True False False True True'), 1),
               pt(S(14, 'True True False False False'), 1)]),
    dict(key=(13, 'c', 'iii'), topic='cs-2-3', qfigure='q13c-iii', total=3,
         replaces='batch 1b: the answer was lost; Figure 4 sat on the answer side instead of the '
                  'table',
         why='p16: the truth table for not (P and Q); the scheme prints it (rows P, Q, P and Q, '
             'not (P and Q)), every value 3, rows and columns for 2 / 1',
         stem=Q13C,
         ask=P(16, 'Using the same meanings for P and Q from part (ii)', 'for the expression, not (P and Q).'),
         rows=[crit(S(15, 'False False False True', 'True True True False'), 3, [1, 2],
                    head=S(15, 'P Q P and Q not (P and Q)'),
                    note=S(15, 'Every value correct 3 marks', '1 mark for any correct value'))]),
    dict(key=(13, 'c', 'iv'), topic='cs-2-3', qfigure='q13c-iv', total=1,
         why='p17: line 16 rewritten from the truth tables; the scheme prints two forms, 1 mark',
         stem=Q13C,
         ask=P(17, 'Use your findings from parts (ii) and (iii)', 'without changing its logical meaning.'),
         rows=[anyn([S(15, 'if not (test_eircode[1].isdigit() and test_eircode[2].isdigit()):'),
                     S(15, 'if not (P and Q):')], 1, 1,
                    head=P(17, 'Use your findings from parts (ii) and (iii)', 'without changing its logical meaning.'),
                    note=S(15, 'Correct response 1 mark', nth=1))]),
    dict(key=(13, 'c', 'v'), topic='cs-2-4', qfigure='q13c-iv', total=2,
         replaces='batch 1b: Figure 4 sat on the answer side instead of line 16',
         why='p17: string slicing instead of line 16; the scheme gives an explanation or the '
             'code, 2',
         stem=Q13C,
         ask=P(17, 'Explain how the technique of string slicing', 'alternative to the statement on line 16.'),
         rows=[anyn([S(15, 'Slicing could be used to extract the 2nd and 3rd characters', 'testing them individually).'),
                     S(15, 'if not (test_eircode[1:3].isdigit()):')], 1, 2,
                    head=P(17, 'Explain how the technique of string slicing', 'alternative to the statement on line 16.'),
                    note=S(15, 'Very good explanation - clear understanding demonstrated 2 marks'))]),
    dict(key=(14, 'a', 'i'), topic='cs-1-1', qfigure='q14a-table', total=2,
         replaces='batch 1b: the matchstick photograph sat on the answer side; the win/loss '
                  'table was not shown',
         why='p18: why 3 is a losing position; the scheme answers it, 2',
         stem=Q14A_STEM, ask=P(18, 'Explain why 3 is a losing position.'),
         rows=[pt(S(16, '3 is a losing position because the only options', 'winning position for my opponent.'), 2,
                  note=S(16, 'Very good explanation - clear understanding demonstrated 2 marks'))]),
    dict(key=(14, 'a', 'ii'), topic='cs-1-1', qfigure='q14a-table', total=2,
         replaces='batch 1b: the matchstick photograph sat on the answer side',
         why='p18: why 4 is a winning position; the scheme answers it, 2',
         stem=Q14A_STEM, ask=P(18, 'Explain why 4 is a winning position.'),
         rows=[pt(S(16, '4 is a winning position because player can take 1 matchstick', '(as per part (i) of the question).'), 2,
                  note=S(16, 'Very good explanation - clear understanding demonstrated 2 marks', nth=2))]),
    dict(key=(14, 'a', 'iii'), topic='cs-1-1', qfigure='q14a-table', total=2,
         replaces='batch 1b: the two answers were not separated, 1 each',
         why='p19: whether 5 and 6 win or lose; the scheme answers each, 1 mark',
         stem=Q14A_STEM, ask=P(19, 'Calculate whether 5 and 6 are winning or losing positions', 'in the table below.'),
         rows=[pt(S(16, '5 is winning positon as a move to take two matchsticks', 'in a losing position.'), 1,
                  note=S(16, 'Each correct response 1 mark')),
               pt(S(16, '6 is a losing position as any move', 'in a winning position'), 1)]),
    dict(key=(14, 'a', 'iv'), topic='cs-1-1', qfigure='q14a-table', total=2,
         replaces='batch 1b: decision and reason were not priced 1 each',
         why='p19: first or second with 21 matchsticks; the scheme prices the decision 1 and the '
             'reason 1',
         stem=Q14A_STEM, ask=P(19, 'Assume you are about to start a new game with 21 matchsticks.', 'Justify your answer.'),
         rows=[pt(S(16, 'Decision: I would ask my opponent to go first. (I would go second.)'), 1,
                  note=S(16, 'Correct decision 1 mark Justification/Reason 1 mark')),
               pt(S(16, 'Reason: 0, 3, 6, 9 etc. are losing positions.', 'it is a losing position.'), 1)]),
    dict(key=(14, 'a', 'v'), topic='cs-1-1', qfigure='q14a-table', total=2,
         replaces='batch 1b: the matchstick photograph sat on the answer side',
         why='p19: the strategy with 20 matchsticks; the scheme answers it, 2',
         stem=Q14A_STEM, ask=P(19, 'What strategy would you recommend in a game that started off with 20 matchsticks?', 'Justify your answer.'),
         rows=[pt(S(17, 'My strategy would be to leave my opponent with a multiple of 3', 'if opponent takes 2 I would take 1.'), 2,
                  note=S(17, 'Very good explanation - clear understanding demonstrated 2 marks'))]),
    dict(key=(14, 'a', 'vi'), topic='cs-1-1', total=2,
         replaces='batch 1b: the answer was lost; the matchstick photograph sat on the answer side',
         why='p20: W or L for 0 to 9 matchsticks when 3 may be taken; the scheme prints the row, '
             '2 / 1',
         stem=Q14A_STEM, ask=P(20, 'Assume the rules of the game are amended', 'place your answers in the table below.'),
         rows=[crit(S(17, 'L W W W L W W W L W'), 2, [1],
                    head=S(17, 'No. of matchsticks remaining 0 1 2 3 4 5 6 7 8 9 Position (W or L)'),
                    note=S(17, 'All W’s and L’s correct 2 marks', 'all W’s or L’s correct 1 mark'))]),
    dict(key=(14, 'b', 'i'), topic='cs-3-3', qfigure='q14b-tree', figure='s-q14b-i', total=5,
         replaces='batch 1b: the scheme\'s drawn diagram was missing and the paper\'s diagram sat on '
                  'the answer side',
         why='p21: complete the game diagram from (1, 2); the scheme draws it, full 5, else path '
             'by path (the scheme\'s top descriptor as the row, as the coordinator did for 2022 HL '
             'Q11(a))',
         stem=Q14B_STEM, ask=P(21, 'Below is a partially completed diagram', 'show who wins in each case.'),
         rows=[crit(S(17, 'Full correct solution'), 5, [1, 2, 3, 4],
                    note=[S(17, 'Full correct solution 5 marks'), S(18, '3 marks as follows:', '1 mark for 3rd full correct path')])]),
    dict(key=(14, 'b', 'ii'), topic='cs-1-1', qfigure='q14b-tree', figure='s-q14b-i', total=2,
         replaces='batch 1b: the paper\'s partial diagram sat on the answer side',
         why='p22: player A\'s best move and why; the scheme answers AY1, best move 1 and reason 1. '
             'The paper\'s diagram is shown with the question and the scheme\'s completed one '
             '(part (i)\'s answer) after the reveal',
         stem=Q14B_STEM, ask=P(22, 'Based on the completed diagram which is player A’s best move? Why?'),
         rows=[crit(S(18, 'AY1 is the best move for player A', 'leads to certain victory for A.'), 2, [1],
                    note=S(18, 'Best move 1 mark Reason 1 mark'))]),
    dict(key=(14, 'b', 'iii'), topic='cs-1-1', total=2,
         replaces='batch 1b: the paper\'s partial diagram sat on the answer side',
         why='p22: a winning move from (2, 3); the scheme answers AY1, 2',
         stem=Q14B_STEM, ask=P(22, 'Describe a winning move from state (2, 3).'),
         rows=[pt(S(18, 'A winning move for player A from state (2, 3) would be AY1.', 'both certain victories for A.'), 2,
                  note=S(18, 'Very good description - clear understanding demonstrated 2 marks'))]),
    dict(key=(14, 'b', 'iv'), topic='cs-1-1', figure='s-q14b-iv', total=2,
         replaces='batch 1b: the paper\'s partial diagram sat on the answer side; the answer\'s '
                  'Cambria Math letters were doubled',
         why='p22: a winning strategy from (n, m); the scheme\'s answer sets n and m in Cambria '
             'Math (doubled in the text layer), so the row is its clean sentence and the solution '
             'crop shows the whole answer, 2',
         stem=Q14B_STEM, ask=P(22, 'Hence, or otherwise, describe a winning strategy from state', '𝑚.'),
         rows=[pt(S(18, 'would be to even the piles. Leave (n, n) or (m, m).'), 2,
                  note=S(18, 'Very good description - clear understanding demonstrated 2 marks', nth=2))]),
    dict(key=(14, 'b', 'v'), topic='cs-1-1', total=2,
         replaces='batch 1b: the paper\'s partial diagram sat on the answer side',
         why='p22: why (n, n, n) wins with three piles; the scheme answers it, 2',
         stem=Q14B_STEM, ask=P(22, 'Explain why', 'where 3 piles are used?'),
         rows=[pt(S(19, 'Since (n, n) is a winning position a winning strategy would be to remove one of the piles.'), 2,
                  note=S(19, 'Very good description - clear understanding demonstrated 2 marks'))]),
    dict(key=(14, 'c', None), topic='cs-2-1', total=5,
         replaces='batch 1b: the answers were lost; the paper\'s partial diagram sat on the answer '
                  'side',
         why='p23: decomposition, abstraction or pattern recognition in these games; the scheme '
             'gives examples of each, best answer 5 / 3 / 1',
         ask=P(23, 'Explain the use of any one of decomposition, abstraction or pattern recognition', 'answering parts (a) and (b).'),
         rows=[ladder([Pair(S(19, 'Abstraction'), S(19, 'By ignoring other details, we can focus on one', 'without considering other moves.')),
                       Pair(S(19, 'Abstraction'), S(19, 'Abstraction allows use to use representations', 'stocks, shares, commodities etc.')),
                       Pair(S(19, 'Decomposition'), S(19, 'We can see how by breaking the problem down', 'decide upon a best move.')),
                       Pair(S(19, 'Decomposition'), S(19, 'In the initial matchstick game if we break the problem down', 'develop a winning strategy.')),
                       Pair(S(19, 'Pattern recognition'), S(19, 'By seeing that multiples of 3 are losing positions', 'devise a winning strategy.')),
                       Pair(S(19, 'Pattern recognition'), S(19, 'By realising that if we always keep the same number', 'possibly 4 or more piles.'))],
                      [[1, 3, 5]], instruction=S(19, 'Any relevant example.'),
                      note=S(19, 'For multiple answers award marks for best answer',
                             'Fair explanation - limited understanding 1 mark'))]),
    dict(key=(15, 'a', 'i'), topic='cs-2-3', total=6,
         replaces='batch 1b: the answers were lost; the stem was missing',
         why='p24: hardware and software, each explained with two examples; the scheme prices '
             'each explanation 1 and each example 1',
         stem=Q15_STEM, ask=P(24, 'Explain the terms hardware and software. Provide two examples of each.'),
         rows=[crit(S(20, 'Hardware is the physical components of a computer system – computer components.'), 3, [],
                    parts=[(S(20, 'Hardware is the physical components of a computer system – computer components.'), 1, []),
                           (S(20, 'Examples processor, memory', 'registers, logic gates etc.'), 2, [1])],
                    note=S(20, 'For each hardware/software Good explanation 1 mark', 'Each relevant example 1 mark + 1 mark')),
               crit(S(20, 'Software is the general term used to describe programs/instructions', 'executed by the processor.'), 3, [],
                    parts=[(S(20, 'Software is the general term used to describe programs/instructions', 'executed by the processor.'), 1, []),
                           (S(20, 'Examples: Any named application or system software package.'), 2, [1])])]),
    dict(key=(15, 'a', 'ii'), topic='cs-3-4', total=2,
         replaces='batch 1b: the answers were lost; the stem was missing',
         why='p24: one digital and one analogue sensor; the scheme lists both, 1 each',
         stem=Q15_STEM, ask=P(24, 'Provide one example of a digital sensor and one example of an analogue sensor.'),
         rows=[pt(S(20, 'Digital sensor: pushbutton, switch, keypad, keyboard or similar.'), 1,
                  note=S(20, 'Example of digital sensor 1 mark', 'Example of analogue sensor 1 mark')),
               pt(S(20, 'Analogue sensor: temperature sensor', 'CO2 or similar.'), 1)]),
    dict(key=(15, 'a', 'iii'), topic='cs-2-3', total=2,
         replaces='batch 1b: the answers were lost; the stem was missing',
         why='p25: digital against analogue input with a diagram; the scheme describes both and '
             'prints no diagram, 2 / 1',
         stem=Q15_STEM, ask=P(25, 'Explain, with the aid of a diagram', 'between digital and analogue input.'),
         rows=[crit(S(20, 'Digital input:', 'Used to represent continuous data.'), 2, [1],
                    note=S(20, 'Difference between digital and analogue 1 mark',
                           'Definition and diagram of either (but not both) 1 marks'))]),
    dict(key=(15, 'a', 'iv'), topic='cs-2-4', total=2,
         replaces='batch 1b: the answer was lost; the stem was missing',
         why='p25: real-time in embedded systems; the scheme answers it, 2',
         stem=Q15_STEM, ask=P(25, 'In the context of embedded systems what is meant by the term', 'time’?'),
         rows=[pt(S(21, 'Real time systems are those that respond', 'detects movement.'), 2,
                  note=S(21, 'Very good description - clear understanding demonstrated 2 marks'))]),
    dict(key=(15, 'a', 'v'), topic='cs-3-4', total=2,
         replaces='batch 1b: the answers were lost; the stem was missing',
         why='p26: two advantages of embedded systems; the scheme lists five, 1 each',
         stem=Q15_STEM, ask=P(26, 'Describe two advantages of embedded systems over general purpose computer systems', 'desktop computers and laptops.'),
         rows=[anyn([S(21, 'Cost – ES are generally cheaper.'), S(21, 'Speed – ES typically run on a dedicated micro-controller.'),
                     S(21, 'Reliability – often less complex and therefore more reliable.'),
                     S(21, 'Automated – once an ES is started it requires minimal user intervention.'),
                     S(21, 'Portability.'), S(21, 'Or similar.')], 2, 1, open_list=True,
                    head=P(26, 'Describe two advantages of embedded systems over general purpose computer systems', 'desktop computers and laptops.'),
                    note=S(21, 'For each relevant advantage (max 2) 1 mark'))]),
    dict(key=(15, 'b', 'i'), topic='cs-3-4', total=2,
         replaces='batch 1b: the answers were lost; the stem was missing',
         why='p26: two embedded systems on mobile devices; the scheme lists four, 1 each',
         stem=Q15B, ask=P(26, 'Describe two examples of embedded systems on mobile devices.'),
         rows=[anyn([S(21, 'Camera'), S(21, 'GPS'), S(21, 'Voice recognition systems'), S(21, 'Microphone'),
                     S(21, 'Any similar named example accepted.')], 2, 1, open_list=True,
                    head=S(21, 'ES that runs on a smartphone/tablet:'),
                    note=S(21, 'Each correct example (max 2) 1 marks'))]),
    dict(key=(15, 'b', 'ii'), topic='cs-1-2', total=2,
         replaces='batch 1b: the answers were lost; the stem was missing',
         why='p27: user interface against universal design; the scheme describes each, 1 each',
         stem=Q15B, ask=P(27, 'In the context of mobile devices distinguish clearly', '‘universal design’.'),
         rows=[pt(S(21, 'User interface on mobile devices are often touchscreen', 'virtual keyboard and voice.'), 1,
                  note=S(21, 'For each part (UI and UD): Good description - clear understanding demonstrated 1 mark')),
               pt(S(21, 'Universal design refers to design principles', 'overall user experience.'), 1)]),
    dict(key=(15, 'b', 'iii'), topic='cs-1-2', total=4,
         replaces='batch 1b: the answers were lost; the stem was missing',
         why='p27: two principles of universal design, each related to an embedded system; the '
             'scheme lists seven, each identified 1 and described 1',
         stem=Q15B, ask=P(27, 'State two principles of universal design.', 'an embedded system of your choice.'),
         rows=[ladder([S(22, 'Principle 1 – Equitable in use', 'people with diverse abilities.'),
                       S(22, 'Principle 2 – Flexibility in use.', 'used in multiple ways.'),
                       S(22, 'Principle 3 – Simplicity to use – easy to understand.'),
                       S(22, 'Principle 4 – Perceptible information', 'user\'s sensory abilities.'),
                       S(22, 'Principle 5 - Tolerance for Error', 'unintended actions.'),
                       S(22, 'Principle 6 - Low Physical Effort', 'minimum of fatigue.'),
                       S(22, 'Principle 7 - Size and Space for Approach and Use', 'posture, or mobility.')],
                      [[1, 2], [1, 2]], head=S(22, 'Principles of universal design:'),
                      note=S(22, 'For each principle 2 marks', 'Good description - clear understanding demonstrated 1 mark'))]),
    dict(key=(15, 'c', None), topic='cs-1-2', total=8,
         replaces='batch 1b: the answers were lost; topic was Computer systems',
         why='p28: the impact of embedded systems on society from two stakeholders\' perspectives; '
             'the scheme lists stakeholders, impacts and alternative perspectives, each stakeholder '
             '4 (identified 1, impact 3 / 1). Filed under Computers and society',
         ask=P(28, 'The market for embedded systems is likely to continue to grow', 'any two stakeholders that you think are relevant.'),
         rows=[crit(S(22, 'Relevant stakeholders include end-users/citizens', 'government etc.'), 4, [],
                    parts=[(S(22, 'Stakeholder identified'), 1, []), (S(22, 'Impact of ES on stakeholder'), 3, [1])],
                    note=[S(22, 'Potential positive impacts:', 'science, exploration'),
                          S(22, 'Alternative perspectives:', 'military uses etc.'),
                          S(22, 'For each stakeholder 4 marks', 'Fair description – limited understanding 1 mark')]),
               crit(S(22, 'Relevant stakeholders include end-users/citizens', 'government etc.'), 4, [],
                    parts=[(S(22, 'Stakeholder identified'), 1, []), (S(22, 'Impact of ES on stakeholder'), 3, [1])])]),
    # ── Section C ──────────────────────────────────────────────────────────
    dict(key=(16, 'a', 'i'), topic='cs-2-2', qfigure='q16a-code', figure='s-q16a-i', total=5,
         replaces='batch 1b: the row was a scale step; filed as Section B; the figure carried '
                  'prose and sat on the answer side',
         why='040 p4: prompt for the second word; the scheme marks line 12 Solution (i), A-5 scale',
         stem=Q16A_STEM,
         ask=C(4, 'Currently the value of the variable word2 is hard', 'Enter the second word: SILENT YES'),
         rows=[crit(S(24, CORRECT), 5, [2, 3], note=S(24, '(i) 5 marks (A-5 scale)', 'Any other reasonable attempt.'))]),
    dict(key=(16, 'a', 'ii'), topic='cs-2-2', qfigure='q16a-code', figure='s-q16a-ii', total=5,
         replaces='batch 1b: the row was a scale step; filed as Section B',
         why='040 p4: print "... is an anagram of ..."; the scheme marks line 17 (ii), A-5 scale',
         stem=Q16A_STEM,
         ask=C(4, 'If both words entered are anagrams the program should display', 'LISTEN is an anagram of SILENT'),
         rows=[crit(S(24, CORRECT, nth=2), 5, [2, 3], note=S(24, '(ii) 5 marks (A-5 scale)', 'Any other reasonable attempt.'))]),
    dict(key=(16, 'a', 'iii'), topic='cs-2-2', qfigure='q16a-code', figure='s-q16a-iii', total=5,
         replaces='batch 1b: the row was a scale step; filed as Section B',
         why='040 p4: print "... is NOT an anagram of ..."; the scheme marks lines 18-19 (iii), '
             'A-5 scale',
         stem=Q16A_STEM,
         ask=C(4, 'Extend the program so that if the words entered are not anagrams', 'LIST is NOT an anagram of ARRAY'),
         rows=[crit(S(24, CORRECT, nth=3), 5, [2, 3], note=S(24, '(iii) 5 marks (A-5 scale)', 'Any other reasonable attempt.'))]),
    dict(key=(16, 'a', 'iv'), topic='cs-2-2', qfigure='q16a-code', figure='s-q16a-iv', total=10,
         replaces='batch 1b: the row was a scale step; filed as Section B',
         why='040 p4: ignore case; the scheme marks line 16 (iv), B-10 scale',
         stem=Q16A_STEM,
         ask=C(4, 'The program currently treats words as case', 'Listen is an anagram of Silent'),
         rows=[crit(S(25, CORRECT), 10, [3, 5, 8], note=S(25, '(iv) 10 marks (B-10 scale)', 'Any other reasonable attempt.'))]),
    dict(key=(16, 'a', 'v'), topic='cs-2-2', qfigure='q16a-code', figure='s-q16a-v', total=10,
         replaces='batch 1b: the row was a scale step; filed as Section B',
         why='040 p4: call is_anagram as well; the scheme marks lines 21-25 (v), B-10 scale',
         stem=Q16A_STEM,
         ask=C(4, 'Extend the program to use the function is_anagram', 'is an anagram of Silent', end_nth=2),
         rows=[crit(S(25, 'Correct implementation using solution above or similar (even if the case is ignored).'), 10, [3, 5, 8],
                    note=S(25, '(v) 10 marks (B-10 scale)', 'Any other reasonable attempt.'))]),
    dict(key=(16, 'a', 'vi'), topic='cs-2-2', qfigure='q16a-code', figure='s-q16a-vi', total=15,
         replaces='batch 1b: the row was a scale step; filed as Section B',
         why='040 p5: test each word against a phrase; the scheme marks lines 28-39 Part (vi), '
             'B-15 scale',
         stem=Q16A_STEM,
         ask=C(5, 'Anagrams of words can also be phrases.', 'Moon is NOT an anagram of moon starer'),
         rows=[crit(S(26, CORRECT), 15, [2, 5, 10], note=S(26, '(vi) 15 marks (B-15 scale)', 'Any other reasonable attempt.'))]),
]
