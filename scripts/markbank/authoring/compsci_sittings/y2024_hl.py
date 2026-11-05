"""Computer Science 2024 Higher Level: all 53 printed asks, re-authored part by part.

50 cards shipped in August out of the automatic author; batch 1b rebuilds each
of them here, keeping its id, from lifts of the paper and the scheme, and the
3 residue cards sit among them in printed order. Paper pages 3-20 and Section
C pages 4-8, and scheme pages 3-29 were opened.

Shipped crops reused on the question side, each opened and clean: q1-fig0
(the logic-gate table), q2-code0, q11-figure (the pseudo code, Figure 4 and the
Step 1 / Step 2 boxes), q12-fig0 (Figure 5's quote) and q14-fig0 (Figure 6's
flowchart). q5-fig0 and q13-fig0 carry a sliver of the next line of print,
q9-code0 the prose above the listing, and q15-figure / q16-figure carry the
paper's prose, so each of those has a crop of its own.

Q14(c)(ii) quotes the scheme's first bullet, whose N squared the text layer
reads as a bold N followed by a bold 2 (the superscript is lost); the scheme's
text is the solution crop, where it reads as printed. Q16(b)'s rubric is read
from the cells of scheme page 29.
"""
from compsci_lane import (C, P, Pair, S, T, anyn, crit, crop, ladder, pt, stack)  # noqa: F401

BOOKS = ('038', 18, (55, 139, 517, 282))
LISTING14 = ('038', 16, (56, 74, 541, 236))

CROPS = {
    's-q1': crop('scheme', 4, (57, 145, 539, 484), ref='2024 HL Q1', solution=True,
                 alt='The marking scheme\'s completed table for Question 1: the six logic gates of '
                     'Column A with their outputs in Column B, AND with inputs 1 and 1 gives 1, '
                     'AND with 0 and 1 gives 0, NOT with 1 gives 0, OR with 1 and 0 gives 1, OR '
                     'with 0 and 0 gives 0, and NAND with 1 and 1 gives 0.'),
    'q4-figs': stack([('038', 4, (188, 440, 408, 503)), ('038', 4, (188, 541, 408, 599))],
                     ref='2024 HL Q4',
                     alt='Figure 1 (start state): five squares numbered 0 to 4 holding a white disc '
                         'in squares 0 and 1, square 2 empty, and a black disc in squares 3 and 4. '
                         'Figure 2 (end state): black discs in squares 0 and 1, square 2 empty, and '
                         'white discs in squares 3 and 4.'),
    's-q4': crop('scheme', 5, (200, 74, 395, 340), ref='2024 HL Q4', solution=True,
                 alt='The marking scheme\'s solution to Question 4: eight moves from the start '
                     'state, 1 to 2, 3 to 1, 4 to 3, 2 to 4, 0 to 2, 1 to 0, 3 to 1 and 2 to 3, '
                     'each drawn as the row of discs it leaves, ending with the black discs in '
                     'squares 0 and 1 and the white discs in squares 3 and 4.'),
    'q5-fig3': crop('038', 5, (55, 120, 540, 306), ref='2024 HL Q5',
                    alt='Figure 3: a timeline from the 1930s to the 1980s with six milestones, '
                        'Turing Machines (1930s), Transistors (1940s), Integrated Circuits (1950s), '
                        'ARPANET (1960s), Microprocessors (1970s) and Personal Computers (1980s).'),
    'q9-code': crop('038', 7, (56, 125, 541, 199), ref='2024 HL Q9',
                    alt='The five-line Python function printed with Question 9: def '
                        'is_leap_year(y):, if (y % 400 == 0) or ((y % 4 == 0) and (y % 100 != 0)): '
                        'return True, else: return False.'),
    'q13-fig5': crop('038', 12, (146, 118, 450, 361), ref='2024 HL Q13(b)',
                     alt='Figure 5: a photograph of two kittens in a bucket, a puppy and a toy duck '
                         'on grass, with a labelled box drawn around each object: cat: 94%, cat: '
                         '85%, dog: 97% and duck: 72%.'),
    'q14b-code': crop(*LISTING14, ref='2024 HL Q14(b)',
                      alt='The ten-line bubble sort program printed with Question 14(b): values = '
                          '[50, 70, 30, 60, 20]; for i in range(len(values)): for j in '
                          'range(len(values)-1): if values[j] > values[j+1], t = values[j+1], '
                          'values[j+1] = values[j], values[j] = t; then print("OUTPUT:", values).'),
    's-q14c-ii': crop('scheme', 19, (57, 565, 545, 733), ref='2024 HL Q14(c)(ii)', solution=True,
                      alt='The marking scheme\'s answer to Question 14(c)(ii): in a list of size N '
                          'bubble sort performs N passes of N-1 compare operations, N squared minus '
                          'N in total, approximately N squared for large N, hence O(N squared); the '
                          'best case (already sorted) and worst case (reverse order) carry out the '
                          'same number of comparisons; the compare operations grow quadratically, '
                          'so doubling the list could multiply them by four.'),
    's-q14c-iii': crop('scheme', 20, (55, 143, 545, 658), ref='2024 HL Q14(c)(iii)', solution=True,
                       alt='The marking scheme\'s two enhancements for Question 14(c)(iii). '
                           'Enhancement 1 reduces the size of the list compared by 1 on each pass, '
                           'with an implementation whose inner loop runs over range(len(L)-1-i). '
                           'Enhancement 2 halts if no swaps are made during a pass, with an '
                           'implementation that sets swap = False before each pass, True when a '
                           'swap is made, and breaks out if swap is still False.'),
    'q15-books': crop(*BOOKS, ref='2024 HL Q15(a)',
                      alt='The BOOKS table printed with Question 15(a), fields book_id, title, '
                          'year, cost, author, author_dob and on_loan: 1 The Cat in the Hat 1957 '
                          '6.95 Dr. Seuss 02/03/1904 Yes; 2 Green Eggs and Ham 1960 8.95 Dr. Seuss '
                          'March 2, 1904 Y; 3 Horton Hears a Who! 1954 euro 10 Doc Seus 02/03/1904 '
                          'N; 4 How the Grinch Stole Christmas! 1957 9.95 Dr. Seuss 03/02/1904 No.'),
    'q15a-iv': stack([BOOKS, ('038', 19, (140, 90, 449, 205))], ref='2024 HL Q15(a)(iv)',
                     alt='The BOOKS table printed with Question 15(a) (book_id, title, year, cost, '
                         'author, author_dob, on_loan, four records), above the table of part (iv): '
                         'Column A, Data Type, lists Boolean, String and Real; Column B, Field '
                         'Name, is blank.'),
    'q15b-fig7': crop('038', 19, (58, 406, 517, 588), ref='2024 HL Q15(b)(i)',
                      alt='Figure 7: the MEMBERS table (member_id 1 Amy, 2 with its name blank, 3 '
                          'Chloe) and the LOANS table (member_id, book_id, date_borrowed): 3, 2, '
                          '20/05/2024; a blank member_id, 4, 01/05/24; 2, 1 and a blank date; and '
                          'a fourth row left blank.'),
    's-q15b-i': crop('scheme', 22, (57, 285, 516, 440), ref='2024 HL Q15(b)(i)', solution=True,
                     alt='The marking scheme\'s completed tables for Question 15(b)(i), its answers '
                         'in bold: MEMBERS row 2 named Bill; in LOANS the second row\'s member_id '
                         '1, the third row\'s date 18/05/2024, and a fourth row 3, 3, '
                         '15/05/2024.'),
    'q16a-code': crop('040', 4, (56, 357, 541, 465), ref='2024 HL Q16(a)',
                      alt='The seven-line program Question16_A.py as printed in the Section C '
                          'booklet: two comment lines, from random import choice, fruits = '
                          '[\'apple\', \'cherry\', \'orange\'], and random_fruit_1 = '
                          'choice(fruits).'),
    's-q16a-i': crop('scheme', 25, (57, 240, 545, 274), ref='2024 HL Q16(a)(i)', solution=True,
                     alt='Lines 9 and 10 of the marking scheme\'s possible solution: a comment for '
                         'part (i), then print("Random Fruit 1:",random_fruit_1) # (i).'),
    's-q16a-ii': crop('scheme', 25, (57, 281, 545, 357), ref='2024 HL Q16(a)(ii)', solution=True,
                      alt='Lines 12 to 17 of the marking scheme\'s possible solution: two comments '
                          'for part (ii), then random_fruit_2 = choice(fruits) and '
                          'random_fruit_3 = choice(fruits), each printed as Random Fruit 2: and '
                          'Random Fruit 3:, every line marked # (ii).'),
    's-q16a-iii': crop('scheme', 25, (57, 375, 545, 419), ref='2024 HL Q16(a)(iii)', solution=True,
                       alt='Lines 20 to 22 of the marking scheme\'s possible solution: a comment for '
                           'part (iii), then if (random_fruit_1 == \'cherry\'): '
                           'print("FIRST FRUIT IS CHERRY").'),
    's-q16a-iv': crop('scheme', 25, (57, 426, 545, 471), ref='2024 HL Q16(a)(iv)', solution=True,
                      alt='Lines 24 to 26 of the marking scheme\'s possible solution: a comment for '
                          'part (iv), then if (random_fruit_1 == random_fruit_2): '
                          'print("FIRST PAIR MATCH").'),
    's-q16a-v': crop('scheme', 25, (57, 478, 545, 523), ref='2024 HL Q16(a)(v)', solution=True,
                     alt='Lines 28 to 30 of the marking scheme\'s possible solution: a comment for '
                         'part (v), then if (random_fruit_1 == random_fruit_2) and (random_fruit_1 '
                         '== \'cherry\'): print("FIRST PAIR ARE CHERRIES ").'),
    's-q16a-vi': crop('scheme', 25, (57, 530, 545, 584), ref='2024 HL Q16(a)(vi)', solution=True,
                      alt='Lines 32 to 34 of the marking scheme\'s possible solution: a comment for '
                          'part (vi), then if any of random_fruit_1 == random_fruit_2, '
                          'random_fruit_1 == random_fruit_3 or random_fruit_2 == random_fruit_3: '
                          'print("MATCHING PAIR").'),
    's-q16a-vii': crop('scheme', 25, (57, 591, 545, 719), ref='2024 HL Q16(a)(vii)', solution=True,
                       alt='Lines 36 to 46 of the marking scheme\'s possible solution, part (vii): '
                           'comments restating the task, random_fruits = [], a loop for i in '
                           'range(100) appending choice(fruits) to random_fruits, then a loop over '
                           'the fruits printing each fruit with random_fruits.count of it.'),
    'q16b-output': crop('040', 8, (56, 70, 545, 497), ref='2024 HL Q16(b)',
                        alt='The two sample outputs printed with Question 16(b). Sample output 1: '
                            'the initial list [\'apple\', \'cherry\', \'orange\'], kiwi entered and '
                            'the list of 4 fruits shown, cherry nominated, The winning fruit you '
                            'selected is cherry, Winner after 38 tries. Sample output 2: kiwi '
                            'added, pear nominated and refused with Error: winning fruit must be '
                            'in the list, orange nominated, Winner after 27 tries.'),
    's-q16b': crop('scheme', 28, (57, 100, 545, 717), ref='2024 HL Q16(b)', solution=True,
                   alt='The marking scheme\'s 50-line possible solution for Question 16(b): the '
                       'fruits list is initialised and printed; an additional fruit is read and '
                       'appended and the list of 4 fruits printed; the winning fruit is read, and '
                       're-read with an error message while it is not in fruits, then printed; '
                       'three random fruits are chosen and re-chosen in a while True loop, '
                       'counting tries, until all three match the winning fruit; then '
                       'print("JACKPOT! after", count, "tries").'),
}

Q9 = [P(7, 'A leap year is a year that contains an additional day', 'is a leap year or not.'),
      P(7, 'Use the code to describe the two rules', 'whether a year is a leap year.')]
Q13A = P(11, 'The term artificial intelligence (AI) was first used in 1955', 'generative AI have emerged.')
Q13B = P(12, 'Computer vision is a field of AI', 'answer the questions that follow.')
Q14A = P(15, 'The flowchart, shown in Figure 6 below', 'displays their new values.')
Q14B = P(16, 'The Python code below shows an implementation of the bubble sort algorithm.')
Q14C = [Q14B, P(17, 'The algorithm takes five passes to complete the bubble sort', 'integers in values.')]
Q15A = P(18, 'Alex wants to keep track of her collection of Dr. Seuss books', 'enter the records shown below.')
Q15B = P(19, 'Alex has decided to build a relational database', 'Green Eggs and Ham on 20th May 2024.')
Q15C = P(20, 'Alex is planning to use the database for a data analytics project.', 'starting with a hypothesis.')
Q16A_STEM = C(4, 'The program initialises a list called fruits', 'The program does not display any output.')
CORRECT = S(26, 'Correct implementation using solution above or similar.')
MEMBERS = S(22, 'MEMBERS')
LOANS = S(22, 'LOANS')

CARDS = [
    # ── Section A ──────────────────────────────────────────────────────────
    dict(key=(1, None, None), topic='cs-2-3', qfigure='q1-fig0', figure='s-q1', total=6,
         replaces='batch 1b: the gate table was the answer figure and the one row its header '
                  '"Column A Column B" worth 6; now the six outputs, 1 each, with the scheme\'s '
                  'completed table',
         why='p3: the output of six logic gates; the scheme prints 1 0 0 1 0 0 beside the gates, '
             'each correct response 1 mark',
         ask=P(3, 'Logic gates have one or more inputs and a single output.', 'either 0 or 1, in Column B.'),
         rows=[crit(S(4, '1 0 0 1 0 0'), 6, [1, 2, 3, 4, 5], note=S(4, 'Each correct response 1 mark', nth=1))]),
    dict(key=(2, None, None), topic='cs-2-2', qfigure='q2-code0', total=6,
         replaces='batch 1b: the listing was the answer figure and the four values one 3-mark row; '
                  'now each value in order 1 and the spacing 2, the listing beside the question',
         why='p3: the output of a while loop; the scheme answers 27 30 33 36, each value in order '
             '1 and the space between values 2',
         ask=P(3, 'What is the output displayed by the following Python code?'),
         rows=[crit(S(4, 'Answer: 27 30 33 36'), 4, [1, 2, 3], note=S(4, 'Each correct value in order (x 4) 1 mark')),
               pt(S(4, 'Space between each value'), 2)]),
    dict(key=(3, None, None), topic='cs-2-3', total=6,
         replaces='batch 1b: the answer was a 3-mark point beside a credit rule ("For each '
                  'calculation error deduct 2 marks") worth 3; now the answer on its printed '
                  'steps, the rules in the note',
         why='p4: 121 as 8-bit binary; the scheme answers 0111 1001, 6 with the leading zero, 5 '
             'without, less 2 a calculation error, some merit 2',
         ask=P(4, 'Express the decimal number 121 as an 8-bit binary number.'),
         rows=[crit(S(4, 'Answer: 0111 1001'), 6, [2, 3, 4, 5],
                    note=S(4, 'Correct including leading zero 6 marks', 'Response with some merit 2 marks'))]),
    dict(key=(4, None, None), topic='cs-1-1', qfigure='q4-figs', figure='s-q4', total=6,
         why='p4: swap the discs by legal moves; the scheme draws an eight-move solution, full '
             '6, four or more correct steps in order 4, some merit 2',
         ask=[P(4, 'Figure 1 shows a row of black and white discs', 'jumping over a disc in square 2.'),
              P(4, 'Write a sequence of steps, or an algorithm,', 'single disc in each step.')],
         rows=[crit(S(5, 'Full correct solution'), 6, [2, 4],
                    note=S(5, 'Full correct solution 6 marks', 'Response with some merit 2 marks'))]),
    dict(key=(5, None, None), topic='cs-1-2', qfigure='q5-fig3', total=6,
         replaces='batch 1b: the answer figure was the timeline with a sliver of print and the row '
                  'the heading "Turing Machines" worth 6; now any one milestone\'s significance at '
                  '6 / 4 / 2; topic Computers and society',
         why='p5: the significance of one milestone in Figure 3; the scheme explains all six, '
             '6 / 4 / 2; filed under Computers and society (the history of computing), not '
             'Computer systems',
         ask=P(5, 'The history of computer hardware is marked', 'explain its significance.'),
         rows=[ladder([S(5, 'Turing Machines', 'limits of computation'),
                       S(5, 'Transistors', 'modern semiconductor technology.'),
                       S(5, 'Integrated Circuits', 'large transistor count.'),
                       S(5, 'ARPANET', 'were developed for ARPANET'),
                       S(5, 'Microprocessors', 'other electronic devices.'),
                       S(6, 'Personal Computers', 'easily accessible to everyone.')], [[2, 4, 6]],
                      note=S(6, 'Very good explanation - clear understanding demonstrated 6 marks',
                             'Fair explanation - limited understanding 2 mark'))]),
    dict(key=(6, None, None), topic='cs-2-5', total=6,
         replaces='batch 1b: one unit test was the only row, worth 6; now a unit test and a system '
                  'test, each any one of the scheme\'s list at 3 / 2',
         why='p5: a unit test case and a system test case; the scheme lists six and five and any '
             'other valid, each 3 / 2',
         ask=P(5, 'Consider a social networking mobile application', 'during the development process.'),
         rows=[ladder([S(6, "Update user's profile picture."),
                       S(6, 'Posting content', 'image sharing'),
                       S(6, 'Connecting with friends'), S(6, 'Displaying online status,'),
                       S(6, 'Privacy settings, work correctly (on their own)'),
                       S(6, 'Evaluate all execution paths (or as many as possible)')], [[2, 3]],
                      head=S(6, 'Examples of Unit Test Cases'), instruction=S(6, 'Any other valid unit test case'),
                      note=S(6, 'For unit test and system test example:', 'Fair example – limited understanding 2 mark')),
               ladder([S(6, 'End-to-end testing of entire application'),
                       S(6, 'Handles a realistic number of simultaneous users'),
                       S(6, 'Handles multiple chat sessions simultaneously'),
                       S(6, 'Ensures that system provides a user-friendly experience'),
                       S(6, 'Complies with privacy and security regulations.')], [[2, 3]],
                      head=S(6, 'Examples of System Test Cases'), instruction=S(6, 'Any other valid system test case'),
                      note=S(6, 'For unit test and system test example:', 'Fair example – limited understanding 2 mark'))]),
    dict(key=(7, None, None), topic='cs-1-2', total=6,
         replaces='batch 1b: the one row was the heading "Potential Advantages of Quantum '
                  'Computing" worth 6; now an advantage and a disadvantage from any of the five '
                  'trends, each 3 / 2; topic Computers and society',
         why='p6: one advantage and one disadvantage of an emerging trend for society; the scheme '
             'answers each trend, each part 3 / 2; filed under Computers and society, not '
             'Computer systems',
         ask=P(6, 'Computing technologies continue to evolve at a rapid pace.', 'on society in the future.'),
         rows=[ladder([Pair(S(6, 'Potential Advantages of Quantum Computing'), S(6, 'Speed - quantum computers', 'climate modelling etc.')),
                       Pair(S(7, 'Potential Advantages of Edge Computing'), S(7, 'Faster response times', 'and remote healthcare.')),
                       Pair(S(7, 'Potential Advantages of Edge Computing'), S(7, 'Improved Privacy and Security:', 'points of potential vulnerability.')),
                       Pair(S(7, 'Potential Advantages of the Internet of Things (IoT)'), S(7, 'Improved Convenience and Efficiency:', 'efficiency in industrial processes.')),
                       Pair(S(7, 'Potential Advantages of Biometric Authentication'), S(7, 'Enhanced Security - biometric authentication', 'method of user authentication.')),
                       Pair(S(7, 'Potential Advantages of Biometric Authentication'), S(7, 'Convenience and User-Friendly', 'positive user experience.')),
                       Pair(S(8, 'Potential advantages of Blockchain Technology:'), S(8, 'Transparency and Security:', 'used in the technology.'))],
                      [[2, 3]], note=S(8, 'For each potential advantage', 'limited understanding of emerging trend 2 mark')),
               ladder([Pair(S(6, 'Potential Disadvantages of Quantum Computing'), S(6, 'Cost – quantum computers', 'run and maintain.')),
                       Pair(S(6, 'Potential Disadvantages of Quantum Computing'), S(7, 'The immense power of quantum computers', 'quantum-resistant cryptography')),
                       Pair(S(7, 'Potential Disadvantages of Edge Computing'), S(7, 'Limited Processing Power and Storage', 'careful resource management.')),
                       Pair(S(7, 'Potential Disadvantages of Edge Computing'), S(7, 'Management Complexity and Scalability Challenges', 'network of edge devices.')),
                       Pair(S(7, 'Potential Disadvantages of the Internet of Things (IoT)'), S(7, 'Privacy Issues: IoT devices', 'critical challenge.')),
                       Pair(S(7, 'Potential Disadvantages of the Internet of Things (IoT)'), S(7, 'Security Concerns: IoT devices', 'entry points for cyberattacks.')),
                       Pair(S(7, 'Potential Disadvantages of Biometric Authentication'), S(7, 'Privacy Concerns - users may be hesitant', 'misused or compromised.')),
                       Pair(S(7, 'Potential Disadvantages of Biometric Authentication'), S(7, 'Biometric Spoofing and False Positives', 'features to gain access.')),
                       Pair(S(8, 'Potential disadvantages of Blockchain Technology:'), S(8, 'Privacy Concerns - while the transparency', 'back to individuals.')),
                       Pair(S(8, 'Potential disadvantages of Blockchain Technology:'), S(8, 'Energy Consumption - many blockchain networks', 'sustainability concerns.'))],
                      [[2, 3]], note=S(8, 'For each potential disadvantage', 'limited understanding of emerging trend 2 mark'))]),
    dict(key=(8, None, None), topic='cs-2-3', total=6,
         replaces='batch 1b: the one row was the heading "Data in RAM" worth 6; now an example '
                  'for RAM and one for ROM, each any one of the scheme\'s list at 3 / 2',
         why='p6: an example of data in RAM and in ROM; the scheme lists four and five, each '
             '3 / 2',
         ask=P(6, 'RAM and ROM are two types of primary memory', 'might be stored in ROM.'),
         rows=[ladder([S(8, 'System Software e.g. operating system'),
                       S(8, 'Application Software e.g. office productivity software'),
                       S(8, 'Programs e.g. python programs and data e.g. documents'),
                       S(8, 'Any temporary data')], [[2, 3]], head=S(8, 'Data in RAM'),
                      note=S(8, 'For each of RAM and ROM:', 'Fair example – limited understanding 2 mark')),
               ladder([S(8, 'Firmware – the software embedded into hardware devices'),
                       S(8, 'Basic Input Output System (BIOS)', "the computer's startup."),
                       S(8, 'Bootstrap programs'), S(8, 'System level configuration data'),
                       S(8, 'Any permanent data necessary for the device to operate')], [[2, 3]],
                      head=S(8, 'Data in ROM'),
                      note=S(8, 'For each of RAM and ROM:', 'Fair example – limited understanding 2 mark'))]),
    dict(key=(9, None, None), topic='cs-2-2', qfigure='q9-code', total=6,
         replaces='batch 1b: the ask lost "365 days." and the listing crop carried prose; the rows '
                  'were the heading "The two rules are:" and two all-or-nothing points; now each '
                  'rule at 3 / 2 and a clean listing',
         why='p7: the two leap-year rules in the code; the scheme states both, each 3 / 2',
         ask=Q9,
         rows=[crit(S(9, 'If the year is evenly divisible by 400', 'e.g. 2000 was a leap year'), 3, [2],
                    note=S(9, 'For each rule:', 'Fair description – limited understanding 2 marks')),
               crit(S(9, 'If the year is evenly divisible by 4 and not 100', '2025 and 2100 are not'), 3, [2])]),
    dict(key=(10, None, None), topic='cs-1-2', total=6,
         replaces='batch 1b: the one row was "Any two from the following:" worth 6; now any two '
                  'of the seven principles, named 1 and explained 2 / 1; topic Computers and '
                  'society',
         why='p7: two universal design principles for a kiosk; the scheme lists seven, each '
             'named 1 and explained 2 / 1; filed under Computers and society (1.15, universal '
             'design), not Algorithms',
         ask=P(7, 'Many fast-food restaurants have begun using interactive kiosks', 'in the design of such systems.'),
         rows=[ladder([S(9, 'Equitable Use - by incorporating accessibility features', 'people with varying abilities.'),
                       S(9, 'Flexibility in Use - this principle could be met', 'touch screen or voice commands.'),
                       S(9, 'Simple and Intuitive Use - this can be achieved', 'different levels of experience.'),
                       S(9, 'Perceptible Information - the system should communicate', 'different sensory capabilities.'),
                       S(9, 'Tolerance for Error - this can be achieved', 'review orders before finalising.'),
                       S(9, 'Low Physical Effort - the system should ensure', 'difficulty with touchscreens.'),
                       S(9, 'Size and Space for Approach and Use', 'approach and interact comfortably.')],
                      [[1, 2, 3], [1, 2, 3]],
                      note=S(9, 'For each correctly named principle of universal design 1 mark',
                             'Fair explanation – limited understanding 1 mark'))]),
    dict(key=(11, 'a', None), topic='cs-2-2', qfigure='q11-figure', total=4,
         replaces='batch 1b: the stem was the pseudo code as text and the crop the answer figure; '
                  'the answer was one 4-mark point; now each step at 2, the pseudo code and '
                  'Figure 4 beside the question',
         why='p8: apply the swap algorithm to Figure 4 in two steps; the scheme describes both '
             'swaps, each correct step 2 (or some merit 2)',
         ask=P(8, 'Apply the algorithm shown in pseudo code below', 'illustrate your answer in the boxes provided.'),
         rows=[pt(S(10, 'In Step 1 the algorithm has swapped', 'triangle in position 7.'), 2,
                  note=S(10, 'For each correct step 2 marks', 'Response with some merit 2 marks')),
               pt(S(10, 'In Step 2 the algorithm has swapped', 'to the left of all the squares.'), 2)]),
    dict(key=(11, 'b', None), topic='cs-1-1', qfigure='q11-figure', total=2,
         replaces='batch 1b: one answer was the only row, all or nothing, and the crop the answer '
                  'figure; now any one of three at 2 / 1; topic Computational thinking',
         why='p8: what a general solution is; the scheme gives three answers, 2 / 1; filed under '
             'Computational thinking (generalisation), not Algorithms',
         ask=P(8, 'The algorithm described in part (a) provides a general solution', '‘a general solution’.'),
         rows=[ladder([S(10, 'A general solution provides a broad approach', 'different situations'),
                       S(10, 'A general solution will always produce the correct output', 'regardless of the input'),
                       S(10, 'The algorithm does not depend on the size of the input', 'squares and triangles.')], [[1, 2]],
                      note=S(10, 'Very good explanation - clear understanding demonstrated 2 marks',
                             'Fair explanation – limited understanding 1 mark'))]),
    dict(key=(12, 'a', None), topic='cs-1-2', qfigure='q12-fig0', total=3,
         replaces='batch 1b: the stem was the caption "Figure 5" and the quote the answer figure; '
                  'one answer was all or nothing; now either answer at 3 / 2 with the quote beside '
                  'the question',
         why='p9: the meaning of the Figure 5 quote; the scheme gives two answers, 3 / 2',
         ask=P(9, 'Explain the meaning of the quote, shown in Figure 5 above', 'in relation to online applications.'),
         rows=[ladder([S(10, 'The meaning of the quote is that when a service', 'influencing user behaviour.'),
                       S(10, 'The quote serves as a reminder', 'personal information and attention.')], [[2, 3]],
                      note=S(10, 'Very good explanation - clear understanding demonstrated 3 marks',
                             'Fair explanation – limited understanding 2 mark'))]),
    dict(key=(12, 'b', None), topic='cs-1-2', qfigure='q12-fig0', total=3,
         why='p9: one implication of the Figure 5 quote; the scheme lists three, 3 / 2',
         ask=P(9, 'Provide one implication that the quote could have', 'online applications.'),
         rows=[ladder([S(11, 'Privacy - users often share personal information', 'targeted advertising.'),
                       S(11, 'Manipulation of attention', 'negative impact on mental health.'),
                       S(11, 'Responsible use - on a positive note', 'reading terms and conditions.')], [[2, 3]],
                      note=S(11, 'Very good explanation - clear understanding demonstrated 3 marks',
                             'Fair explanation – limited understanding 2 mark'))]),
    # ── Section B ──────────────────────────────────────────────────────────
    dict(key=(13, 'a', 'i'), topic='cs-1-2', total=3,
         replaces='batch 1b: the stem was "This question continues on the next page.", an '
                  'unrelated figure was attached and the three definitions were 1-mark points; '
                  'now any one definition at 3 / 2; topic Computers and society',
         why='p11: define artificial intelligence; the scheme accepts the essence of any of three '
             'definitions, 3 / 2; filed under Computers and society as (ii) and (iii) are, not '
             'Abstraction',
         stem=Q13A, ask=P(11, 'What is meant by the term ‘artificial intelligence’?'),
         rows=[ladder([S(12, 'Artificial intelligence can be defined as the science', 'associate with human intelligence.'),
                       S(12, 'The design and study of systems that appear to mimic intelligent behaviour'),
                       S(12, 'The theory and development of computer systems', 'translation between languages.')], [[2, 3]],
                      head=S(12, 'Any response that captures the essence of any of the following:'),
                      note=S(12, 'Very good explanation - clear understanding demonstrated 3 marks',
                             'Fair explanation – limited understanding 2 mark'))]),
    dict(key=(13, 'a', 'ii'), topic='cs-1-2', total=3,
         replaces='batch 1b: the stem was page furniture, an unrelated figure was attached, and the '
                  'row narrow AI alone, all or nothing; now both definitions at 3 / 2',
         why='p11: narrow AI against AGI; the scheme defines both, 3 / 2',
         stem=Q13A, ask=P(11, 'Distinguish between narrow AI and artificial general intelligence (AGI).'),
         rows=[crit(S(12, 'Narrow AI: Refers to AI systems built', 'learn and adapt autonomously.'), 3, [2],
                    note=S(12, 'Very good distinction - clear understanding demonstrated 3 marks',
                           'Fair distinction – limited understanding 2 mark'))]),
    dict(key=(13, 'a', 'iii'), topic='cs-1-2', total=3,
         replaces='batch 1b: the stem was page furniture, an unrelated figure was attached, and the '
                  'answer all or nothing; now 3 / 2',
         why='p11: explain generative AI; the scheme answers it, 3 / 2',
         stem=Q13A, ask=P(11, 'ChatGPT and Gemini are examples of generative AI applications.', '‘generative AI’.'),
         rows=[crit(S(12, 'Generative AI is an Artificial Intelligence (AI) technology', 'known as hallucination.'), 3, [2],
                    note=S(12, 'Very good explanation - clear understanding demonstrated 3 marks',
                           'Fair explanation – limited understanding 2 mark', nth=2))]),
    dict(key=(13, 'a', 'iv'), topic='cs-1-2', total=2,
         replaces='batch 1b: the stem was page furniture and the one row "Any two from the '
                  'following:"; now any two formats at 1; topic Computers and society',
         why='p11: two outputs of generative AI; the scheme lists five and any reasonable '
             'format, 1 each; filed with (a)(i)-(iii), not Computer systems',
         stem=Q13A, ask=P(11, 'Name two types of output that can be produced by generative AI.'),
         rows=[anyn([S(13, 'text (written in any natural language)'),
                     S(13, 'images (e.g. photographs, digital paintings and cartoons)'), S(13, 'videos'),
                     S(13, 'music'), S(13, 'software code'),
                     S(13, 'any reasonable format that could be produced by GenAI')], 2, 1, open_list=True,
                    head=S(13, 'Any two from the following:', nth=1),
                    note=S(13, 'For each correctly identified format 1 mark'))]),
    dict(key=(13, 'b', 'i'), topic='cs-1-2', qfigure='q13-fig5', total=2,
         replaces='batch 1b: the stem was the caption and both (iii) scenarios, the figure carried '
                  'stray print and the answer was all or nothing; now 2 / 1 with a clean Figure 5; '
                  'topic Computers and society',
         why='p12: what the percentages mean; the scheme answers it, 2 / 1; filed under '
             'Computers and society (AI, LO 1.14) with (a), not Algorithms',
         stem=Q13B, ask=P(12, 'In relation to computer vision, what do the percentages shown in Figure 5 represent?'),
         rows=[crit(S(13, 'The percentages represent a level of confidence', 'on this part of the image.'), 2, [1],
                    note=S(13, 'Very good explanation - clear understanding demonstrated 2 marks',
                           'Fair explanation - limited understanding demonstrated 1 mark'))]),
    dict(key=(13, 'b', 'ii'), topic='cs-1-2', qfigure='q13-fig5', total=6,
         replaces='batch 1b: the one row was "Any two from the following:" worth 6; now any two '
                  'applications, named 1 and the benefit 2 / 1; topic Computers and society',
         why='p12: two applications of computer vision and their benefits; the scheme lists '
             'eight and any reasonable, each named 1 and benefit 2 / 1; filed under Computers '
             'and society, not Data',
         stem=Q13B, ask=P(12, 'Suggest two applications for this type of technology', 'benefit society.'),
         rows=[ladder([S(13, 'Computer vision can be used for early detection of diseases', 'medical imaging.'),
                       S(13, 'Computer vision technology can be used in self-driving cars', 'reducing the risk of accidents.'),
                       S(13, 'Computer vision can be applied to eliminate the need for checkouts', 'incidence of theft.'),
                       S(13, 'Computer vision can analyse aerial imagery', 'pesticides and water.'),
                       S(13, 'Facial Recognition technology has the potential', 'other high-security areas.'),
                       S(13, 'Computer vision can be used in robots', 'precision in manufacturing.'),
                       S(13, 'Computer vision can be used to monitor and track endangered species', 'wildlife and their habitats.'),
                       S(14, 'Augmented reality applications using computer vision', 'engaging and accessible.')],
                      [[1, 2, 3], [1, 2, 3]],
                      instruction=S(14, 'Any reasonable application of computer vision and associated benefit.'),
                      note=S(14, 'For each correctly named application', 'Fair explanation – limited understanding 1 mark'))]),
    dict(key=(13, 'b', 'iii'), topic='cs-1-2', qfigure='q13-fig5', total=4,
         replaces='batch 1b: each scenario\'s whole block (AI and Not AI) was one 2-mark point; '
                  'now each scenario\'s justification, either way, at 2 / 1; topic Computers and '
                  'society',
         why='p13: machine learning AI or not, for two scenarios, justified; the scheme gives an '
             'AI and a Not AI justification for each, 2 / 1 (no marks for yes / no)',
         stem=Q13B, ask=P(13, 'Read the two example scenarios below', 'cutting the grass.'),
         rows=[ladder([S(14, 'AI: The system could use machine learning', 'create rules for each user.'),
                       S(14, 'Not AI: Possible reasons include', 'preference for simplicity.')], [[1, 2]],
                      head=S(14, 'Scenario 1. An online streaming service', 'viewing habits.'),
                      note=S(14, 'For each justification (no marks for stating yes/no):',
                             'Fair explanation – limited understanding 1 mark')),
               ladder([S(14, 'AI (robotics): The automated lawnmower', 'path planning.'),
                       S(14, 'Not AI: While it does employ sensors', 'rather than AI.')], [[1, 2]],
                      head=S(14, 'Scenario 2. An automated lawnmower', 'cutting the grass.'),
                      note=S(14, 'For each justification (no marks for stating yes/no):',
                             'Fair explanation – limited understanding 1 mark'))]),
    dict(key=(13, 'b', 'iv'), topic='cs-1-2', qfigure='q13-fig5', total=3,
         replaces='batch 1b: one method was the only row, all or nothing; now any one of five at '
                  '3 / 2; topic Computers and society',
         why='p13: one way to reduce bias in computer vision; the scheme lists five and any other '
             'reasonable, 3 / 2',
         stem=Q13B, ask=P(13, 'In recent years many instances of bias', 'reduce bias in these applications.'),
         rows=[ladder([S(14, 'Diversity of images used in training datasets', 'represent the target population'),
                       S(14, 'Equality of representation of target population', 'representative of the target population'),
                       S(14, 'Size of training datasets', 'trained using smaller datasets.'),
                       S(15, 'Human in the loop', 'in development team'),
                       S(15, 'Monitoring and Bias Auditing', 'inadvertently crept in.')], [[2, 3]],
                      instruction=S(15, 'Any other reasonable method to reduce bias.'),
                      note=S(15, 'Very good explanation - clear understanding demonstrated 3 marks',
                             'Fair explanation – limited understanding 2 mark'))]),
    dict(key=(13, 'c', None), topic='cs-1-2', total=12,
         replaces='batch 1b: the stem was the ask\'s last sentence and both menus were claimed '
                  'whole at 3 with the first point as their head; now two points for and two '
                  'against, each 3 / 2; topic Computers and society',
         why='p14: reasons for and against pausing AI training; the scheme lists five for and '
             'four against, two of each at 3 / 2; filed under Computers and society, not '
             'Computer systems',
         ask=P(14, 'In 2023 an open letter published by the Future of Life Institute', 'others not supporting the initiative.'),
         rows=[ladder([S(15, 'Ethical concerns: time is needed', 'privacy, accountability, and fairness.'),
                       S(15, 'Jobs/Employment/Economy:', 'mitigate economic disparities.'),
                       S(15, 'Security Risks: Advanced AI systems', 'development of AI-driven weaponry.'),
                       S(15, 'Unintended Consequences:', 'unforeseen negative impacts on society.'),
                       S(15, 'Existential Threat:', 'risks and benefits of advanced AI.')], [[2, 3], [2, 3]],
                      head=S(15, 'Points for supporting the initiative:'),
                      instruction=S(15, 'Elaboration of any other reasonable point for pausing', 'advanced AI systems'),
                      note=S(16, 'For each separate point made for and against', 'limited understanding 2 mark')),
               ladder([S(15, 'Innovation and Progress:', 'AI can bring to society.'),
                       S(15, 'Societal Advancements:', 'pressing global issues.'),
                       S(15, 'Competitive Disadvantage:', 'economic, military, and technological spheres.'),
                       [S(15, 'Job Creation and Economic Growth:', 'stimulate economic growth. Pausing'),
                        S(16, 'development could limit the positive economic impact', 'efficiency and innovation.')]],
                      [[2, 3], [2, 3]], head=S(15, 'Points against the initiative:'),
                      instruction=S(16, 'Elaboration of any other reasonable point against pausing', 'advanced AI systems'),
                      note=S(16, 'For each separate point made for and against', 'limited understanding 2 mark'))]),
    dict(key=(14, 'a', 'i'), topic='cs-2-2', qfigure='q14-fig0', total=2,
         replaces='batch 1b: the stem was furniture ("Figure 6 This question continues...") and '
                  'the flowchart the answer figure; now the question\'s stem with Figure 6 beside '
                  'it, the credit rule moved off the second row',
         why='p15: the two input variables; the scheme answers a and b, 1 each',
         stem=Q14A, ask=P(15, 'State the names of the two input variables.'),
         rows=[pt(S(17, 'Input variable 1: a'), 1, note=S(17, 'Each correct response 1 mark', nth=1)),
               pt(S(17, 'Input variable 2: b'), 1)]),
    dict(key=(14, 'a', 'ii'), topic='cs-2-2', qfigure='q14-fig0', total=3,
         replaces='batch 1b: the stem was furniture and the answer half of the scheme\'s, all or '
                  'nothing; now both lines at 3 / 2 with Figure 6',
         why='p15: the purpose of t; the scheme answers it, 3 / 2',
         stem=Q14A, ask=P(15, 'Explain the purpose of the variable t.'),
         rows=[crit(S(17, 't is a temporary variable used to store the value of a', 'when b is assigned to a'), 3, [2],
                    note=S(17, 'Very good explanation - clear understanding demonstrated 3 marks',
                           'Fair explanation – limited understanding 2 mark'))]),
    dict(key=(14, 'a', 'iii'), topic='cs-1-3', qfigure='q14-fig0', total=4,
         replaces='batch 1b: the stem was furniture and the one row the heading "Advantages" worth '
                  '4; now an advantage and a disadvantage, each 2 / 1; topic Designing and '
                  'developing',
         why='p15: one advantage and one disadvantage of flowcharts; the scheme lists four and '
             'three, each 2 / 1; filed under Designing and developing (design tools), not '
             'Algorithms',
         stem=Q14A, ask=P(15, 'Flowcharts are commonly used in the design process', 'disadvantage of using flowcharts.'),
         rows=[ladder([S(17, 'They are easier to understand than code', '(especially for non-programmers).'),
                       S(17, 'The visual representation of flowcharts', 'logic of an algorithm.'),
                       S(17, 'They are independent of any programming language.'),
                       S(17, 'They are flexible tools used to represent algorithms', 'design process.')], [[1, 2]],
                      head=S(17, 'Advantages'),
                      note=S(17, 'For each advantage/disadvantage', 'Fair explanation – limited understanding 1 mark')),
               ladder([S(17, 'They take a significant amount of time to develop.'),
                       S(17, 'They can become unwieldly for detailed and complex algorithms.'),
                       S(17, 'Lack of standards can lead to ambiguity and cause confusion.')], [[1, 2]],
                      head=S(17, 'Disadvantages'),
                      note=S(17, 'For each advantage/disadvantage', 'Fair explanation – limited understanding 1 mark'))]),
    dict(key=(14, 'b', 'i'), topic='cs-2-2', qfigure='q14b-code', total=1,
         replaces='batch 1b: the stem was the listing as text and the answer figure the '
                  'flowchart; now the (b) stem with the listing beside the question',
         why='p16: the data type of values; the scheme answers a list (array), 1',
         stem=Q14B, ask=P(16, 'State the data type of the variable, values.'),
         rows=[pt(S(17, 'the data type of the variable, values. Is a list (array)'), 1)]),
    dict(key=(14, 'b', 'ii'), topic='cs-2-4', qfigure='q14b-code', total=1,
         replaces='batch 1b: the stem was the listing as text and the answer figure the '
                  'flowchart; now the (b) stem with the listing beside the question',
         why='p16: the index of 70; the scheme answers 1, 1',
         stem=Q14B, ask=P(16, 'What is the index of the element 70?'),
         rows=[pt(S(18, 'the index of the element 70 is 1'), 1)]),
    dict(key=(14, 'b', 'iii'), topic='cs-2-2', qfigure='q14b-code', total=1,
         replaces='batch 1b: the stem was the listing as text and the answer figure the '
                  'flowchart; now the (b) stem with the listing beside the question',
         why='p16: what len(values) returns; the scheme answers 5, 1',
         stem=Q14B, ask=P(16, 'What does the Python expression len(values) return?'),
         rows=[pt(S(18, 'the Python expression, len(values) returns 5'), 1)]),
    dict(key=(14, 'b', 'iv'), topic='cs-2-4', qfigure='q14b-code', total=2,
         replaces='batch 1b: the stem was the listing as text, the answer figure the flowchart '
                  'and the answer all or nothing; now 2 / 1 with the listing beside the question',
         why='p16: what values[2:4] returns; the scheme answers [30, 60], full 2, some merit 1',
         stem=Q14B, ask=P(16, 'What does the slice expression values[2:4] return?'),
         rows=[crit(S(18, 'the slice expression, values[2:4] returns the list, [30, 60]'), 2, [1],
                    note=S(18, 'Full correct response 2 marks', 'Response with some merit 1 mark'))]),
    dict(key=(14, 'b', 'v'), topic='cs-2-4', qfigure='q14b-code', total=3,
         replaces='batch 1b: the stem was the listing as text, the answer figure the flowchart '
                  'and the answer all or nothing; now 3 / 2 with the listing beside the question',
         why='p16: why values[5] fails; the scheme answers it, 3 / 2',
         stem=Q14B, ask=P(16, 'Explain why the expression values[5] would generate a runtime error.'),
         rows=[crit(S(18, 'the expression values[5] would generate a runtime error', 'out of bounds'), 3, [2],
                    note=S(18, 'Very good explanation - clear understanding demonstrated 3 marks',
                           'Fair explanation – limited understanding 2 mark'))]),
    dict(key=(14, 'b', 'vi'), topic='cs-2-2', qfigure='q14b-code', total=6,
         replaces='batch 1b: the one row was the heading "Advantages" worth 6; now an advantage '
                  'and a disadvantage, each any one at 3; topic Algorithms',
         why='p16: one advantage and one disadvantage of sorting; the scheme lists three and '
             'five, each valid statement 3; filed under Algorithms (sorting), not Computer '
             'systems',
         stem=Q14B, ask=P(16, 'State one advantage and one disadvantage of sorting a data set.'),
         rows=[anyn([S(18, 'Binary search requires a dataset to be sorted'),
                     S(18, 'Sorted data can be more user friendly', 'sorted by cost etc.'),
                     S(18, 'Sorted data can also make it easier for data analysis', 'patterns/trends and outliers')],
                    1, 3, head=S(18, 'Advantages'), note=S(19, 'For each advantage/disadvantage Valid statement 3 marks')),
               anyn([S(18, 'sorting algorithms can take time'),
                     S(18, 'sorting algorithms can consume valuable computational resources', 'CPU and memory.'),
                     S(18, 'If a dataset is already sorted', 'may not provide significant benefits.'),
                     S(19, 'the efficiency of sorting algorithms can vary dramatically', 'implications under all circumstances.'),
                     S(19, 'Once a dataset is sorted there is a cost to maintaining the dataset in a sorted state')],
                    1, 3, head=S(18, 'Disadvantages'))]),
    dict(key=(14, 'c', 'i'), topic='cs-2-2', qfigure='q14b-code', total=5,
         replaces='batch 1b: the answer figure was the flowchart and the one row the given initial '
                  'state worth 5; now each of the five passes at 1, the listing beside the question',
         why='p17: the list after each of five bubble-sort passes; the scheme prints each pass, '
             '1 mark',
         stem=Q14C, ask=P(17, 'Apply the bubble sort algorithm to sort values.', 'after each of the five passes.'),
         rows=[pt(S(19, 'After pass 1: 50 30 60 20 70'), 1, note=S(19, 'For each pass correctly completed 1 mark')),
               pt(S(19, 'After pass 2: 30 50 20 60 70'), 1), pt(S(19, 'After pass 3: 30 20 50 60 70'), 1),
               pt(S(19, 'After pass 4: 20 30 50 60 70'), 1), pt(S(19, 'After pass 5: 20 30 50 60 70'), 1)]),
    dict(key=(14, 'c', 'ii'), topic='cs-2-2', qfigure='q14b-code', figure='s-q14c-ii', total=5,
         replaces='batch 1b: the stem was the initial state as text, the answer figure the '
                  'flowchart and the answer all or nothing; now 5 / 3 / 1 with the scheme\'s text '
                  'as printed',
         why='p17: what O(n squared) means for compare operations; the scheme answers it, 5 / 3 / '
             '1; its N squared is set in a font whose superscript the text layer loses, so the '
             'scheme\'s text is also the solution crop',
         stem=Q14C, ask=P(17, 'The bubble sort algorithm has O(', 'number of compare operations performed.'),
         rows=[crit(S(19, 'In a list of size N the bubble sort algorithm performs N passes.', 'increase by a factor of four.'),
                    5, [1, 3],
                    note=[S(19, 'Very good explanation - clear understanding demonstrated 5 marks'),
                          S(20, 'Good explanation - clear information', 'Fair explanation - limited understanding 1 mark')])]),
    dict(key=(14, 'c', 'iii'), topic='cs-2-2', qfigure='q14b-code', figure='s-q14c-iii', total=5,
         replaces='batch 1b: the stem was the initial state as text, the answer figure the '
                  'flowchart and the row the heading "Enhancement 1" worth 5; now either '
                  'enhancement at 5 / 3 / 1 with the scheme\'s two implementations',
         why='p17: one improvement to the bubble sort; the scheme prints two, joined by OR, '
             '5 / 3 / 1',
         stem=Q14C, ask=P(17, 'Suggest one possible improvement', 'required to complete the sort.'),
         rows=[ladder([S(20, 'Enhancement 1 (reducing size of list by 1 on each pass)', 'as shown in the implementation below.'),
                       S(20, 'Enhancement 2 (halting if no swaps made during any pass)', 'the algorithm can be terminated.')],
                      [[1, 3, 5]],
                      note=S(20, 'Very good explanation - clear understanding demonstrated 5 marks',
                             'Fair explanation - limited understanding 1 mark'))]),
    dict(key=(15, 'a', 'i'), topic='cs-2-4', qfigure='q15-books', total=4,
         replaces='batch 1b: the stem was the BOOKS table as text, the answer figure another part\'s '
                  'table and the one row the heading "Database" worth 4; now each term at 2 / 1 '
                  'with the BOOKS table beside the question',
         why='p18: define database and record; the scheme answers each, 2 / 1',
         stem=Q15A, ask=P(18, 'Explain the two terms, ‘database’ and ‘record’.'),
         rows=[crit(S(21, 'A database is a collection of structured data', 'country, order, product or book'), 2, [1],
                    head=S(21, 'Database'),
                    note=S(21, 'For each term:', 'Fair explanation – limited understanding 1 mark')),
               crit(S(21, 'Is a single row of data', 'a set of related elements or fields'), 2, [1], head=S(21, 'Record'))]),
    dict(key=(15, 'a', 'ii'), topic='cs-2-4', qfigure='q15-books', total=3,
         replaces='batch 1b: the stem was the table as text and the answer figure another part\'s '
                  'table; the key was the only row, worth 3; now the key at 1 and the '
                  'justification at 2',
         why='p18: a primary key and why; the scheme answers book_id at 1 and its uniqueness at 2',
         stem=Q15A, ask=P(18, 'Suggest which field would be a good choice for the primary key', 'Justify your answer.'),
         rows=[pt(S(21, 'Primary Key: book_id'), 1, note=S(21, 'Primary Key correctly identified 1 mark')),
               pt(S(21, 'Justify: The value of book_id is guaranteed to be unique', 'for each separate record'), 2,
                  note=S(21, 'Justification: Very good justification – clear understanding demonstrated 2 marks'))]),
    dict(key=(15, 'a', 'iii'), topic='cs-2-4', qfigure='q15-books', total=2,
         replaces='batch 1b: the one row was "Any two from the following:" worth 2; now any two of '
                  'the four inconsistencies at 1',
         why='p18: two data inconsistencies; the scheme lists four, 1 each',
         stem=Q15A, ask=P(18, 'Identify any two data inconsistencies', 'shown in the BOOKS table.'),
         rows=[anyn([S(21, 'The use of the euro symbol in the cost field', '6.95, 8.95 and 9.95'),
                     S(21, 'The name of the author in record number 3', 'inconsistent with Dr. Seuss'),
                     S(21, 'the format used in the author_dob field', '(American, mm/dd/yyyy).'),
                     S(21, 'The values used in the on_loan field are inconsistent.', 'values of 3 and 4 are not on loan.')],
                    2, 1, head=S(21, 'Any two from the following:'),
                    note=S(21, 'Each correctly identified inconsistency 1 marks'))]),
    dict(key=(15, 'a', 'iv'), topic='cs-2-4', qfigure='q15a-iv', total=3,
         replaces='batch 1b: the one row was the table header "Column A Column B" worth 3; now the '
                  'three field names, 1 each, with both tables beside the question',
         why='p19: a field for Boolean, String and Real; the scheme answers on_loan, title / '
             'author / author_dob and cost, each 1, and says these are the only acceptable answers',
         stem=Q15A, ask=P(19, 'Assuming all data inconsistencies are fixed', 'shown in Column A.'),
         rows=[pt(S(22, 'Boolean on_loan'), 1,
                  note=S(22, 'Note: The above table shows the only acceptable answers', 'Each correct response 1 mark', end_nth=1)),
               pt(S(22, 'String title, author, author_dob'), 1), pt(S(22, 'Real cost'), 1)]),
    dict(key=(15, 'b', 'i'), topic='cs-3-1', qfigure='q15b-fig7', figure='s-q15b-i', total=6,
         why='p19: six empty cells from three loans; the scheme prints the completed tables, 1 '
             'per cell (the fourth LOANS row holds three)',
         stem=Q15B,
         ask=P(19, 'Use the information provided below to fill in', 'Horton Hears a Who! 7 days ago.'),
         rows=[pt(S(22, '2 Bill'), 1, head=MEMBERS, note=S(22, 'Each correct response 1 mark', nth=2)),
               pt(S(22, '1 4 01/05/24'), 1, head=LOANS),
               pt(S(22, '2 1 18/05/2024'), 1, head=LOANS),
               crit(S(22, '3 3 15/05/2024'), 3, [1, 2], head=LOANS)]),
    dict(key=(15, 'b', 'ii'), topic='cs-3-1', qfigure='q15b-fig7', total=4,
         replaces='batch 1b: the stem was the (b) lead alone, the answer figure a crop with '
                  'another part\'s prose, and the one row "Possible answers are:" worth 4; now '
                  'either key, identified 1 and explained 3 / 2, with Figure 7',
         why='p19: one foreign key and its use; the scheme gives member_id or book_id, key 1 and '
             'explanation 3 / 2',
         stem=Q15B, ask=P(19, 'Identify and explain the use of one foreign key', 'shown in Figure 7.'),
         rows=[ladder([S(22, 'Foreign Key: member_id', 'with the MEMBERS table'),
                       S(22, 'Foreign Key: book_id', 'with the BOOKS table')], [[1, 2, 3, 4]],
                      note=S(22, 'Foreign Key correctly identified 1 mark', 'Fair explanation – limited understanding 2 mark'))]),
    dict(key=(15, 'b', 'iii'), topic='cs-2-4', qfigure='q15b-fig7', total=3,
         replaces='batch 1b: the answer figure carried another part\'s prose and the answer was '
                  'all or nothing; now 3 / 2 with Figure 7',
         why='p20: why on_loan is no longer needed; the scheme answers it, 3 / 2',
         stem=Q15B, ask=P(20, 'Explain how the design shown in Figure 7 removes the need', 'from the BOOKS table.'),
         rows=[crit(S(23, 'The presence of a record in the LOANS table', 'no need to store this information in BOOKS.'),
                    3, [2], note=S(23, 'Very good explanation - clear understanding demonstrated 3 marks',
                                   'Fair explanation – limited understanding 2 mark'))]),
    dict(key=(15, 'b', 'iv'), topic='cs-2-4', qfigure='q15b-fig7', total=3,
         replaces='batch 1b: the answer figure carried another part\'s prose and the answer was '
                  'all or nothing; now 3 / 2',
         why='p20: define data redundancy; the scheme answers it, 3 / 2',
         stem=Q15B, ask=P(20, 'Relational databases reduce the amount of data redundancy.', '‘data redundancy’.'),
         rows=[crit(S(23, 'Data redundancy refers to a situation', 'inefficiency use of storage.'), 3, [2],
                    note=S(23, 'Very good explanation - clear understanding demonstrated 3 marks',
                           'Fair explanation – limited understanding 2 mark', nth=2))]),
    dict(key=(15, 'c', 'i'), topic='cs-3-2', total=4,
         replaces='batch 1b: the stem was "Space for extra work" pages, the answer figure an '
                  'unrelated crop, and the row "Any two statements from the following:" worth 4; '
                  'now any two hypotheses at 2 / 1',
         why='p20: two hypotheses for the analytics project; the scheme lists six and any '
             'reasonable statement, each 2 / 1',
         stem=Q15C, ask=P(20, 'Suggest two possible hypotheses', 'data analytics project to test.'),
         rows=[ladder([S(23, 'The most/least popular book is X.'),
                       S(23, 'The most popular time/season to borrow books is Y'),
                       S(23, 'A particular user demographics', 'prefer certain types of books.'),
                       S(23, 'Certain books (e.g. expensive books)', 'returned on time than others.'),
                       S(23, 'Member A is more likely to return their books in time than member B'),
                       S(23, 'PR campaign results in an increase in borrowing of X%')], [[1, 2], [1, 2]],
                      instruction=S(23, 'Any reasonable hypothesis presented as a statement.'),
                      note=S(23, 'For each hypothesis:', 'Fair explanation – limited understanding 1 mark'))]),
    dict(key=(15, 'c', 'ii'), topic='cs-2-4', total=6,
         replaces='batch 1b: the stem was "Space for extra work" pages and the one row "Any two '
                  'from the following:" worth 6; now any two errors, named 1 and described 2 / 1',
         why='p20: two data errors removed by cleaning; the scheme lists seven and any other '
             'relevant, each identified 1 and described 2 / 1',
         stem=Q15C, ask=P(20, 'Another stage in a typical analytics project is data cleaning.', 'removed using data cleaning.'),
         rows=[ladder([S(23, 'Missing Values:', 'not critical.'),
                       S(23, 'Duplicate Records:', 'each data point is unique.'),
                       S(24, 'Inconsistent Formatting:', 'standardised for consistency.'),
                       S(24, 'Outliers and Anomalies:', 'if they are erroneous.'),
                       S(24, 'Incorrect Data Types:', 'corrected as needed.'),
                       S(24, 'Typographical Errors:', 'consistency and accuracy.'),
                       S(24, 'Inconsistent Categories:', 'unify the categories.')], [[1, 2, 3], [1, 2, 3]],
                      instruction=S(24, 'Any other relevant error e.g. Invalid entries', 'corrected or removed.'),
                      note=S(24, 'For each type of error correctly identified 1 mark',
                             'Fair description – limited understanding 1 mark'))]),
    # ── Section C ──────────────────────────────────────────────────────────
    dict(key=(16, 'a', 'i'), topic='cs-2-2', qfigure='q16a-code', figure='s-q16a-i', total=5,
         replaces='batch 1b: filed as section B with the part asks\' output samples as its stem and '
                  '"semantic error." as its row; now section C, the C-5 scale and the scheme\'s '
                  'line 10',
         why='040 p4: display random_fruit_1; the scheme marks line 10 # (i), C-5 scale',
         stem=Q16A_STEM, ask=C(4, 'Write a line of code to display the value', 'Random Fruit 1: cherry'),
         rows=[crit(CORRECT, 5, [2, 3], note=S(26, '(i) 5 marks (C-5 scale)', 'Any other reasonable attempt.'))]),
    dict(key=(16, 'a', 'ii'), topic='cs-2-2', qfigure='q16a-code', figure='s-q16a-ii', total=5,
         replaces='batch 1b: filed as section B, topic Evaluation and testing, with "semantic '
                  'error." as its row; now section C, Algorithms like its siblings, the C-5 scale '
                  'and the scheme\'s lines 14-17',
         why='040 p4: two more random fruits, displayed; the scheme marks lines 14-17 # (ii), C-5 '
             'scale; filed under Algorithms as the other Q16 parts are',
         stem=Q16A_STEM, ask=C(4, 'Add statements to initialise two new variables', 'Random Fruit 3: cherry'),
         rows=[crit(CORRECT, 5, [2, 3], note=S(26, '(ii) 5 marks (C-5 scale)', 'Any other reasonable attempt.'))]),
    dict(key=(16, 'a', 'iii'), topic='cs-2-2', qfigure='q16a-code', figure='s-q16a-iii', total=5,
         replaces='batch 1b: filed as section B with "semantic error." as its row; now section C, '
                  'the C-5 scale and the scheme\'s lines 20-22',
         why='040 p5: the First fruit is cherry message; the scheme marks lines 20-22, C-5 scale',
         stem=Q16A_STEM, ask=C(5, 'Add code to display the message “First fruit is cherry”', 'First fruit is cherry'),
         rows=[crit(CORRECT, 5, [2, 3], note=S(26, '(iii) 5 marks (C-5 scale)', 'Any other reasonable attempt.'))]),
    dict(key=(16, 'a', 'iv'), topic='cs-2-2', qfigure='q16a-code', figure='s-q16a-iv', total=5,
         replaces='batch 1b: filed as section B with "Any other reasonable attempt." as its row; '
                  'now section C, the B-5 scale and the scheme\'s lines 24-26',
         why='040 p5: the First pair match message; the scheme marks lines 24-26, B-5 scale',
         stem=Q16A_STEM, ask=C(5, 'Add code to display the message “First pair match”', 'First pair match'),
         rows=[crit(CORRECT, 5, [3], note=S(26, '(iv) 5 marks (B-5 scale)', 'Any other reasonable attempt.'))]),
    dict(key=(16, 'a', 'v'), topic='cs-2-2', qfigure='q16a-code', figure='s-q16a-v', total=5,
         replaces='batch 1b: filed as section B with "Any other reasonable attempt." as its row; '
                  'now section C, the B-5 scale and the scheme\'s lines 28-30',
         why='040 p5: the First pair are cherries message; the scheme marks lines 28-30, B-5 scale',
         stem=Q16A_STEM, ask=C(5, 'Add code to display the message “First pair are cherries”', 'First pair are cherries'),
         rows=[crit(S(27, 'Correct implementation using solution above or similar.'), 5, [3],
                    note=S(27, '(v) 5 marks (B-5 scale)', 'Any other reasonable attempt.'))]),
    dict(key=(16, 'a', 'vi'), topic='cs-2-2', qfigure='q16a-code', figure='s-q16a-vi', total=10,
         replaces='batch 1b: filed as section B with five 2-mark rows of scale furniture; now '
                  'section C, the D-10 scale and the scheme\'s lines 32-34',
         why='040 p5: the Matching pair message; the scheme marks lines 32-34, D-10 scale',
         stem=Q16A_STEM, ask=C(5, 'Add code to display the message “Matching pair”', 'Matching pair'),
         rows=[crit(S(27, 'Correct implementation using solution above or similar.'), 10, [3, 5, 7],
                    note=S(27, '(vi) 10 marks (D-10 scale)', 'Any other reasonable attempt.'))]),
    dict(key=(16, 'a', 'vii'), topic='cs-2-2', qfigure='q16a-code', figure='s-q16a-vii', total=15,
         replaces='batch 1b: filed as section B with "15 marks Correct response" as its row; now '
                  'section C, the D-15 scale and the scheme\'s lines 36-46',
         why='040 p6: count 100 random fruits; the scheme marks lines 36-46, D-15 scale',
         stem=Q16A_STEM, ask=C(6, 'Extend the program with a loop that iterates 100 times.', 'orange 31'),
         rows=[crit(S(27, 'Correct implementation using solution above or similar.'), 15, [5, 8, 12],
                    note=S(27, '(vii) 15 marks (D-15 scale)', 'Any other reasonable attempt.'))]),
    dict(key=(16, 'b', None), topic='cs-2-2', qfigure='q16b-output', figure='s-q16b', total=30,
         replaces='batch 1b: filed as section B, its ask was "Open the program..." and its row '
                  '"Possible solution:" worth 30; now section C, the fruit machine task, the '
                  'sample outputs, and the rubric\'s four criteria at their printed levels',
         why='040 p7-8: write the fruit machine simulation; the scheme prints a possible solution '
             'and a rubric of four criteria at high / moderate / low (cells of scheme p29): '
             'standards 10 / 7 / 5, inputs 5 / 4 / 3, logic 10 / 7 / 5, outputs 5 / 4 / 3',
         ask=C(7, 'Implement a simulation of a fruit machine in Python.', 'Winner after 38 tries'),
         rows=[crit(T(29, 'Program executes correctly with no syntax or runtime errors', 'Meaningful variable/function names'),
                    10, [5, 7], head=T(29, 'Programming Standards'),
                    note=[T(29, 'High level of achievement All of the following', 'correctly and efficiently'),
                          T(29, 'Moderate level of achievement Reasonable attempt', 'each of the following'),
                          T(29, 'Low level of achievement Poor attempt to complete any of the following')]),
               crit(T(29, 'Initial list of fruits correctly initialised', 'use of assignment statements'), 5, [3, 4],
                    head=T(29, 'Program Inputs')),
               crit(T(29, 'Additional fruit correctly appended to list of fruits', 'maintain counter variable'), 10, [5, 7],
                    head=T(29, 'Program Logic (Processing)')),
               crit(T(29, 'Initial list of fruits displayed', 'correctly displayed with counter'), 5, [3, 4],
                    head=T(29, 'Program Outputs'))]),
]
