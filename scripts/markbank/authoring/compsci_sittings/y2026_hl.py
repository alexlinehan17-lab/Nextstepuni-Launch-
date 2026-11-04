"""Computer Science 2026 Higher Level: every printed ask, 48 of 48.

Paper: Sections A & B booklet (-038-, 20 pages) and Section C booklet (-040-,
12 pages). Scheme: LC219ALP000EV 2026, 32 pages. Every page of both booklets
and scheme pages 4-27 were opened before this module was written.

The scheme prices every part on its own row ("6(3,3) marks", "(i) 3 marks"),
so every tariff below is the one cs_scheme reads there, unless `printed=`
quotes the cell. Credit bands ("Very good explanation ... 3 marks / Fair
explanation ... 2 marks") are the steps of a criterion row, or the note under
a menu of the scheme's own answers; they are never a row of their own.
"""
from compsci_lane import (C, P, S, T, Pair, allof, anyn, ask_row, crit, crop,  # noqa: F401
                          pt, stack)

BANDS_3_2 = 'Very good explanation - clear understanding demonstrated 3 marks'

CROPS = {
    'q1-code': crop('038', 3, (52, 176, 541, 478), ref='2026 HL Q1',
                    alt='The nine-line Python program printed with Question 1 (a = 0, b = 7, '
                        'then a while loop that runs while b > 0, adding 2 to a and taking 2 '
                        'from b when b is even, otherwise adding 1 to a and taking 1 from b), '
                        'above the blank trace table with columns a and b. Its first row is '
                        'filled in as 0 and 7 and its last row as 7 and 0; the three rows '
                        'between are empty.'),
    'q7-fig1': crop('038', 6, (178, 124, 418, 175), ref='2026 HL Q7',
                    alt='Figure 1: a row of eight boxes holding 4, 6, 9, 12, 5, 10, 3 and 11. '
                        'The first four values, already sorted, are printed in bold.'),
    'q12-fig2': crop('038', 8, (144, 396, 432, 510), ref='2026 HL Q12',
                     alt='Figure 2: a simplified Turing machine. An infinite tape of cells '
                         'holding 1 1 0 1 0 0 0 1 0 1 1, with dots at both ends, runs along the '
                         'top; a double-headed arrow labelled Read/Write Head links the tape to '
                         'a box below labelled Controller, drawn with two cogs.'),
    'q14a-figs': stack([('038', 12, (364, 52, 542, 209)),
                        ('038', 12, (95, 372, 470, 492)),
                        ('038', 12, (118, 610, 476, 754))], ref='2026 HL Q14(a)',
                       alt='Three bridge networks and a table, as printed for Question 14(a). '
                           'Figure 3: a river with two islands; land area A on the north bank, '
                           'B on the south bank, C on the left island and D on the right island, '
                           'joined by seven numbered bridges (1 and 2 from A to C, 3 from A to D, '
                           '4 and 5 from C to B, 6 from D to B, and 7 between C and D). Figures '
                           '4 and 5: alternative networks of the same four land areas; Figure 4 '
                           'has bridges 1 (A to C), 2 (C to B), 3 (A to D) and 4 (D to B); '
                           'Figure 5 has the same four bridges plus bridge 5 joining C and D. '
                           'Below them, the table with Column A listing land areas A, B, C and '
                           'D, Column B (Figure 3) completed as Odd for all four, and Columns C '
                           '(Figure 4) and D (Figure 5) blank.'),
    'q14b-fig6': crop('038', 13, (446, 170, 544, 274), ref='2026 HL Q14(b)(i)',
                      alt='Figure 6: the Königsberg bridges drawn as a graph. Four points '
                          'labelled A (top), B (bottom), C (left) and D (right) are joined by '
                          'seven curved and straight lines, one for each bridge.'),
    'q15-fig7': crop('038', 15, (84, 124, 516, 290), ref='2026 HL Q15',
                     alt='Figure 7: a rounded box headed GREENHOUSE SYSTEM. Example inputs '
                         '(sensors): temperature sensor, humidity sensor, door sensor, natural '
                         'light sensor and motion sensor. Example outputs (actuators): fan '
                         '(ON/OFF), heater (ON/OFF), water pump (ON/OFF), grow lights (ON/OFF) '
                         'and ventilation (OPEN/CLOSE).'),
    'q15b-code': crop('038', 16, (57, 108, 540, 172), ref='2026 HL Q15(b)(i)',
                      alt='The four-line code snippet printed with Question 15(b)(i): line 1 if '
                          'temperature > 30:, line 2 fan = "ON" (indented), line 3 if door_open:, '
                          'line 4 fan = "OFF" (indented).'),
    'q16a-code': crop('040', 4, (55, 241, 527, 724), ref='2026 HL Q16(a)',
                      alt='The 29-line program Question16_A.py as printed in the Section C '
                          'booklet: a function calculate_readability_score(text) that splits the '
                          'text into words, prints the list, sets word_count and '
                          'short_word_count = 0, counts full stops as sentence_count, multiplies '
                          'word_count by sentence_count, rounds the score to 2 decimal places '
                          'and returns it; then text1 and text2 are set and line 29 calls the '
                          'function for text1, storing the result in score1.'),
    'q16a-vi-formula': stack([('040', 7, (108, 376, 432, 412)),
                              ('040', 4, (55, 241, 527, 724))], ref='2026 HL Q16(a)(vi)',
                             alt='The readability formula printed in part (vi): 0.4 multiplied by '
                                 'the bracket of total words over total sentences, plus 100 '
                                 'multiplied by total words minus short words, all over total '
                                 'words. Below it, the 29-line program Question16_A.py as printed '
                                 'in the Section C booklet.'),
    'q16b-output': crop('040', 10, (55, 52, 520, 494), ref='2026 HL Q16(b)',
                        alt='The two sample outputs printed for Question 16(b). Sample output 1: '
                            'python scores 18 and exam 10, the player stops, total 28, highest '
                            'scoring word PYTHON with 18 points. Sample output 2: test123, '
                            'testing 1 2 3 and test@ing! are each rejected as Invalid word; then '
                            'testing scores 17, Examination 23 and computer 18, total 58, highest '
                            'scoring word EXAMINATION with 23 points.'),
    # The scheme's answers that are drawings or programs, shown after the reveal.
    's-q3': crop('scheme', 5, (105, 73, 470, 190), ref='2026 HL Q3', solution=True,
                 alt='The marking scheme\'s logic circuit for Question 3: inputs A and B feed an '
                     'AND gate; the output of the AND gate and input C feed an OR gate, whose '
                     'output is labelled GRANT ACCESS.'),
    's-q6': crop('scheme', 6, (57, 284, 472, 545), ref='2026 HL Q6', solution=True,
                 alt='The marking scheme\'s answer to Question 6 in two forms. Pseudocode: '
                     'Initialise number to 0; Loop while number ≤ 12; Display number; Add 3 to '
                     'number. Flowchart: Start, then NUMBER = 0, then a decision NUMBER <= 12; '
                     'on True, OUTPUT number, then NUMBER += 3 and back to the decision; on '
                     'False, Stop.'),
    's-q13b-ii': crop('scheme', 12, (100, 104, 495, 350), ref='2026 HL Q13(b)(ii)',
                      solution=True,
                      alt='The marking scheme\'s sample wireframe: a title bar over a heading '
                          'and image placeholder, then a form with a Title drop-down, Name, '
                          'Email, Confirm Email, Male and Female radio buttons, Date of Birth, a '
                          'Terms and Conditions check box and a black Submit button. Notes beside '
                          'it read: Appropriate Heading / Image; A drop down list – Mr, Ms and Dr; '
                          'The name cannot be empty and cannot contain numbers; Must contain an @ '
                          'and at least one dot, there must be a dot after the @, the confirm '
                          'email must match the first email; The checkbox must be checked; '
                          'Pushbutton to submit details.'),
    's-q14b-ii': crop('scheme', 15, (80, 558, 432, 653), ref='2026 HL Q14(b)(ii)',
                      solution=True,
                      alt='The marking scheme\'s sequence of crossings for Question 14(b)(ii): A '
                          'and B cross, 3 minutes; A returns, 1 minute (total 4); C and D cross, '
                          '10 minutes (total 14); B returns, 3 minutes (total 17); A and B cross, '
                          '3 minutes (total optimal time 20 minutes).'),
    's-q16a-i': crop('scheme', 22, (57, 229, 480, 284), ref='2026 HL Q16(a)(i)', solution=True,
                     alt='Lines 57 to 60 of the marking scheme\'s possible solution: score1 is '
                         'calculated, then print("Readability Score 1:", score1) and print(), '
                         'both marked # (i).'),
    's-q16a-ii': crop('scheme', 22, (57, 294, 480, 349), ref='2026 HL Q16(a)(ii)',
                      solution=True,
                      alt='Lines 62 to 65 of the marking scheme\'s possible solution: score2 = '
                          'calculate_readability_score(text2), then print("Readability Score '
                          '2:", score2) and print(), each marked # (ii).'),
    's-q16a-iii': crop('scheme', 21, (57, 717, 540, 747), ref='2026 HL Q16(a)(iii)',
                       solution=True,
                       alt='Lines 43 and 44 of the marking scheme\'s possible solution: '
                           'sentence_count = text.count(".") + text.count("!"), marked # (iii).'),
    's-q16a-iv': crop('scheme', 22, (57, 359, 480, 467), ref='2026 HL Q16(a)(iv)',
                      solution=True,
                      alt='Lines 67 to 74 of the marking scheme\'s possible solution: an if, '
                          'elif and else comparing score1 with score2 and printing which text '
                          'is easier to read, or that both scores are the same.'),
    's-q16a-v': crop('scheme', 21, (57, 340, 480, 434), ref='2026 HL Q16(a)(v)', solution=True,
                     alt='Lines 14 to 20 of the marking scheme\'s possible solution: '
                         'short_word_count = 0, a for loop over the words adding 1 when '
                         'len(word) <= 2, then print("Short Words:", short_word_count).'),
    's-q16a-vi': crop('scheme', 22, (57, 66, 540, 131), ref='2026 HL Q16(a)(vi)', solution=True,
                      alt='Lines 46 to 49 of the marking scheme\'s possible solution: the old '
                          'score line commented out and score = 0.4*(word_count/sentence_count + '
                          '100*((word_count-short_word_count)/word_count)), marked # vi, then the '
                          'score rounded to 2 decimal places.'),
    's-q16a-vii': crop('scheme', 21, (57, 444, 480, 708), ref='2026 HL Q16(a)(vii)',
                       solution=True,
                       alt='Lines 22 to 41 of the marking scheme\'s possible solution: '
                           'complex_word_count = 0 and vowels = "AEIOUaeiou"; for each word, '
                           'count its vowels as syllables, subtract 1 if the last character is '
                           '"e", and add 1 to complex_word_count when the syllable count is 3 '
                           'or more; then print("Complex Words:", complex_word_count).'),
    's-q16b': stack([('scheme', 25, (55, 74, 540, 757)),
                     ('scheme', 26, (55, 52, 540, 93))], ref='2026 HL Q16(b)', solution=True,
                    alt='The marking scheme\'s possible solution to Question 16(b), lines 1 to '
                        '51: total_score, high_score and highest_scoring_word are initialised; '
                        'a while True loop asks for a word, re-asks while word.isalpha() is '
                        'False printing Invalid word., converts it to upper case, scores 1 for '
                        'AEIOU, 5 for VWXYZ and 3 for any other letter, adds the score to the '
                        'total, prints the word, score and total, keeps the highest scoring '
                        'word, and breaks unless the player answers Y; finally it prints the '
                        'highest scoring word and its points.'),
}

TRACE = S(4, 'Each correct response 1 mark')
NOTE_Q5 = S(6, 'For each part: Very good explanation', 'limited understanding 2 mark')
NOTE_Q12 = S(9, 'For each part: Very good response', 'limited understanding 2 marks')
NOTE_Q13C = S(13, 'For each heading:', 'limited understanding 1 mark')
NOTE_Q15B = S(18, 'For each part: Very good description', 'limited understanding 2 mark')
NOTE_Q15B3 = S(19, 'For each part: Very good description', 'limited understanding 2 marks')

VALID = S(13, 'Validation examples (x 2)')
VERIFY = S(13, 'Verification example')
Q16A_STEM = C(5, 'A readability score is an estimate', "'unpredictable', 'ways.']")
CORRECT = S(23, 'Correct implementation using solution above or similar.')

CARDS = [
    # ── Section A ─────────────────────────────────────────────────────────
    dict(key=(1, None, None), topic='cs-2-2', figure=None, qfigure='q1-code', total=6,
         why='p3: a nine-line program and a trace table with three blank rows; the scheme '
             'prints the three rows, each correct response 1 mark',
         ask=P(3, 'Use the trace table below', 'during program execution.'),
         rows=[crit(S(4, '1 6'), 2, [1], note=TRACE),
               crit(S(4, '3 4'), 2, [1], note=TRACE),
               crit(S(4, '5 2'), 2, [1], note=TRACE)]),
    dict(key=(2, None, None), topic='cs-2-3', total=6,
         why='p3: compare cache and RAM under two headings; the scheme answers each heading '
             'and prices it 3 / 2',
         ask=P(3, 'Cache and RAM are both important', 'purpose and speed.'),
         rows=[crit(S(4, 'Both cache and RAM are volatile', 'operating system and applications.'),
                    3, [2], head=S(4, 'Purpose'),
                    note=S(4, 'Very good explanation', 'limited understanding 2 mark')),
               crit(S(4, 'Both cache and RAM provide fast access', 'larger amount of working memory.'),
                    3, [2], head=S(4, 'Speed'),
                    note=S(4, 'Very good explanation', 'limited understanding 2 mark'))]),
    dict(key=(3, None, None), topic='cs-2-3', figure='s-q3', total=6,
         why='p4: sketch the circuit for three printed conditions; the scheme draws it and '
             'prices six features at 1 mark',
         ask=P(4, 'A school computer system uses the three conditions',
               'using the appropriate gate symbols.'),
         rows=[pt(S(5, 'Correct AND gate'), 1), pt(S(5, 'Correct OR gate'), 1),
               pt(S(5, 'A connected to AND'), 1), pt(S(5, 'B connected to AND'), 1),
               pt(S(5, 'Output of AND connected to OR'), 1), pt(S(5, 'C connected to OR'), 1)]),
    dict(key=(4, 'a', None), topic='cs-2-3', total=2,
         why='p4: one hexadecimal value; the scheme prints FFFF at 2, some merit 1',
         stem=P(4, 'Binary and hexadecimal numbers are both used', 'represent digital data.'),
         ask=P(4, 'State the highest hexadecimal number', 'using 16 bits.'),
         rows=[crit(S(5, 'FFFF'), 2, [1],
                    note=S(5, 'Correct answer 2 marks', 'Response with some merit 1 mark'))]),
    dict(key=(4, 'b', None), topic='cs-2-3', total=4,
         why='p4: one conversion; the scheme prints 0011 1111 at 4, without leading zeros 3, '
             'some merit 2',
         stem=P(4, 'Binary and hexadecimal numbers are both used', 'represent digital data.'),
         ask=P(4, 'Convert the hexadecimal number 3F', 'binary equivalent.'),
         rows=[crit(S(5, '0011 1111'), 4, [2, 3],
                    note=S(5, 'Correct response 4 marks', 'Response with some merit 2 mark'))]),
    dict(key=(5, 'a', None), topic='cs-1-2', total=3,
         why='p5: one advantage of cloud storage; the scheme lists answers, any one at 3',
         stem=P(5, 'A school is moving its student records', 'cloud-based storage service.'),
         ask=P(5, 'Outline one advantage', 'for the school.'),
         rows=[anyn([S(5, 'Data can be accessed from anywhere with an internet connection'),
                     S(5, 'The school does not need to maintain its own physical servers'),
                     S(5, 'Cloud storage providers usually handle', 'maintenance effort for the school'),
                     S(5, 'Any reasonable response e.g. security, scalability, elasticity')],
                    1, 3, head=P(5, 'Outline one advantage', 'for the school.'),
                    note=NOTE_Q5, open_list=True)]),
    dict(key=(5, 'b', None), topic='cs-1-2', total=3,
         why='p5: one concern about cloud storage; the scheme lists answers, any one at 3',
         stem=P(5, 'A school is moving its student records', 'cloud-based storage service.'),
         ask=P(5, 'Explain one concern', 'student records in the cloud.'),
         rows=[anyn([S(6, 'Student data security and privacy could be at risk', 'is hacked'),
                     S(6, 'The school depends on a reliable internet connection', 'access records'),
                     S(6, 'There may be legal or data protection rules', 'provider must follow'),
                     S(6, 'Any reasonable response e.g. cost')],
                    1, 3, head=P(5, 'Explain one concern', 'student records in the cloud.'),
                    note=NOTE_Q5, open_list=True)]),
    dict(key=(6, None, None), topic='cs-2-2', figure='s-q6', total=6,
         why='p5: construct a while-loop algorithm; the scheme gives pseudocode and a '
             'flowchart, priced 6 / 4 / 2',
         ask=P(5, 'Construct an algorithm that uses a while loop', 'in pseudo code.'),
         rows=[crit(S(6, 'Initialise number to 0', 'Add 3 to number'), 6, [2, 4],
                    note=S(6, 'Full correct response 6 marks', 'limited merit 2 marks'))]),
    dict(key=(7, 'a', None), topic='cs-2-2', qfigure='q7-fig1', total=4,
         why='p6: four insertion-sort passes from Figure 1; the scheme prints each pass, 1 mark',
         stem=P(6, 'A student is applying the insertion sort', 'the next value to be inserted is 5.'),
         ask=P(6, 'Complete the state of the list', 'remaining four passes.'),
         rows=[pt(S(7, 'Pass 5: 4 5 6 9 12 10 3 11'), 1), pt(S(7, 'Pass 6: 4 5 6 9 10 12 3 11'), 1),
               pt(S(7, 'Pass 7: 3 4 5 6 9 10 12 11'), 1), pt(S(7, 'Pass 8: 3 4 5 6 9 10 11 12'), 1)]),
    dict(key=(7, 'b', None), topic='cs-2-2', qfigure='q7-fig1', total=2,
         why='p6: how insertion sort places an element; the scheme answers it, 2 / 1',
         stem=P(6, 'A student is applying the insertion sort', 'the next value to be inserted is 5.'),
         ask=P(6, 'Outline how the insertion sort algorithm decides', 'the sorting process.'),
         rows=[crit(S(7, 'Insertion sort works by taking one item', 'all items in the list are in order.'),
                    2, [1], note=S(7, 'Very good response - clear', 'limited understanding 1 mark'))]),
    dict(key=(8, None, None), topic='cs-1-2', total=6,
         why='p6: two reasons AI makes mistakes; the scheme lists three, each explanation 3 / 2',
         ask=P(6, 'Some students use Artificial Intelligence', 'why AI can make mistakes.'),
         rows=[anyn([S(7, 'AI does not truly understand topics', 'inherent in the way AI works)'),
                     S(7, 'AI is trained on large amounts of data', 'relates to training data)'),
                     S(7, 'AI can be biased because it learns', 'relates to training data)', nth=1)],
                    2, 3, head=P(6, 'Explain two reasons why AI can make mistakes.'),
                    note=S(7, 'For each explanation:', 'limited understanding 2 mark'))]),
    dict(key=(9, 'a', None), topic='cs-2-1', total=3,
         why='p7: modular design; the scheme answers it, 3 / 2',
         stem=P(7, 'A company is developing a software program', 'modular design for this system.'),
         ask=P(7, 'Explain what is meant by modular design', 'software development.'),
         rows=[crit(S(8, 'Modular design in software development means', 'easier to develop, test, and maintain.'),
                    3, [2], note=S(8, 'Very good explanation', 'limited understanding 2 mark'))]),
    dict(key=(9, 'b', None), topic='cs-2-1', total=3,
         why='p7: three modules; the scheme lists seven and any reasonable, 1 mark each',
         stem=P(7, 'A company is developing a software program', 'modular design for this system.'),
         ask=P(7, 'Suggest three modules', 'restaurant ordering system.'),
         rows=[anyn([S(8, 'Order taking module to record customer orders'),
                     S(8, 'Payment processing module to handle bills and payments'),
                     S(8, 'Menu management module to update food items and prices'),
                     S(8, 'User account module to manage staff logins and roles'),
                     S(8, 'Reporting module to track sales and generate reports'),
                     S(8, 'Table management module to track table availability'),
                     S(8, 'Inventory module to monitor ingredient stock levels'),
                     S(8, 'Any reasonable response', nth=1)],
                    3, 1, head=P(7, 'Suggest three modules', 'restaurant ordering system.'),
                    note=S(8, 'For each module correctly identified 1 mark'), open_list=True)]),
    dict(key=(10, None, None), topic='cs-1-2', total=6,
         why='p7: two Universal Design examples; the scheme lists the seven principles, each '
             'named 2 and described 1',
         ask=P(7, 'A company is designing a new educational app', 'specific principle in each example.'),
         rows=[anyn([S(8, 'Equitable Use:', 'information as other students.'),
                     S(8, 'Flexibility in Use:', 'text, audio, or video.'),
                     S(8, 'Simple and Intuitive Use:', 'app without training.'),
                     S(8, 'Perceptible Information:', 'access the information.'),
                     S(8, 'Tolerance for Error:', 'before deleting work.'),
                     S(8, 'Low Physical Effort:', 'touchscreen movements.'),
                     S(8, 'Size and Space for Approach and Use:', 'easy to select.')],
                    2, 3, head=P(7, 'Describe two examples', 'specific principle in each example.'),
                    note=S(8, 'For each correctly named principle 2 marks', 'understanding demonstrated 1 mark'))]),
    dict(key=(11, 'a', None), topic='cs-1-1', total=4,
         why='p8: one heuristic for self-driving cars; the scheme lists five and any reasonable, '
             '4 / 2',
         stem=P(8, 'The algorithms that control self-driving vehicles', 'help them make decisions.'),
         ask=P(8, 'Outline one heuristic', 'self-driving cars.'),
         rows=[anyn([S(9, 'Maintain a minimum following distance based on current speed.'),
                     S(9, 'Reduce speed when visibility decreases.'),
                     S(9, 'Increase stopping distance in wet or icy conditions.'),
                     S(9, 'Choose the route with the least predicted congestion.'),
                     S(9, 'Leave extra space when driving near cyclists or pedestrians.'),
                     S(9, 'Any reasonable response - a good solution', 'short amount of time')],
                    1, 4, head=P(8, 'Outline one heuristic', 'self-driving cars.'),
                    note=S(9, 'Very good response - clear understanding demonstrated 4 marks',
                           'limited understanding 2 marks'), open_list=True)]),
    dict(key=(11, 'b', None), topic='cs-1-1', total=2,
         why='p8: one limitation of heuristics; the scheme lists five and any reasonable, 2',
         stem=P(8, 'The algorithms that control self-driving vehicles', 'help them make decisions.'),
         ask=P(8, 'State one limitation of heuristics.'),
         rows=[anyn([S(9, 'Heuristics do not always give the best or correct decision'),
                     S(9, 'Decisions are based on simple rules, not full understanding'),
                     S(9, 'Heuristics can be biased by the data or rules they are based on'),
                     S(9, 'They may oversimplify complex real-world situations'),
                     S(9, 'Different heuristics can sometimes conflict with each other'),
                     S(9, 'Any reasonable response', nth=2)],
                    1, 2, head=P(8, 'State one limitation of heuristics.'),
                    note=S(9, 'Correctly response 2 marks'), open_list=True)]),
    dict(key=(12, 'a', None), topic='cs-1-2', qfigure='q12-fig2', total=3,
         why='p8: the controller in Figure 2; the scheme answers it, 3 / 2',
         stem=P(8, 'Figure 2 below shows a simplified model of a Turing machine.'),
         ask=P(8, 'Outline the purpose of the controller.'),
         rows=[crit(S(9, "The controller follows the Turing machine's rules.", 'including when to halt.'),
                    3, [2], note=NOTE_Q12)]),
    dict(key=(12, 'b', None), topic='cs-1-2', qfigure='q12-fig2', total=3,
         why='p8: why Turing machines matter; the scheme answers it, 3 / 2',
         stem=P(8, 'Figure 2 below shows a simplified model of a Turing machine.'),
         ask=P(8, 'Explain why Turing machines are considered important', 'computer science.'),
         rows=[crit(S(9, 'Turing machines are important because', 'so central to Computer Science.'),
                    3, [2], note=NOTE_Q12)]),

    # ── Section B: Question 13, the Winter Solstice Lottery ───────────────
    dict(key=(13, 'a', 'i'), topic='cs-3-1', total=3,
         why='p9: define an information system; the scheme prints two definitions, 3 / 2',
         stem=P(9, 'Newgrange is a prehistoric passage tomb', 'inside the chamber during this event.'),
         ask=P(9, 'Explain the term ‘information system’.'),
         rows=[anyn([S(10, 'An information system (IS) is the software', '(transactional) operation of a business.'),
                     S(10, 'An information system is a system that takes in data', 'produces useful information.')],
                    1, 3, head=P(9, 'Explain the term ‘information system’.'),
                    note=S(10, 'Very good explanation - clear understanding demonstrated 3 marks',
                           'limited understanding 2 marks'))]),
    dict(key=(13, 'a', 'ii'), topic='cs-3-1', total=2,
         why='p9: two components; the scheme lists five, any two at 1',
         stem=P(9, 'Newgrange is a prehistoric passage tomb', 'inside the chamber during this event.'),
         ask=P(9, 'State the names of two components', 'every information system.'),
         rows=[anyn([S(10, 'Hardware - physical devices like computers and servers'),
                     S(10, 'Software - programs and applications used by the system'),
                     S(10, 'Data - raw facts that are stored', 'output as information'),
                     S(10, 'People - users who interact with the system'),
                     S(10, 'Processes (procedures) - rules and steps for using the system')],
                    2, 1, head=S(10, 'Any two from the following:'),
                    note=S(10, 'For each correct response 1 mark'))]),
    dict(key=(13, 'a', 'iii'), topic='cs-3-1', total=8,
         why='p9: two functional and two non-functional requirements; the scheme lists both, '
             'best of each 3 and second 1',
         stem=P(9, 'Newgrange is a prehistoric passage tomb', 'inside the chamber during this event.'),
         ask=P(9, 'Suggest two functional requirements', 'Winter Solstice Lottery system.'),
         rows=[anyn([S(10, 'Allow users to submit an online application for the lottery'),
                     S(10, 'Send confirmation or rejection notifications to applicants'),
                     S(10, 'Store and manage applicant details securely'),
                     S(10, 'Randomly select winners and generate a list of successful applicants'),
                     S(10, 'Allow administrators to view and manage, applicants and results'),
                     S(10, 'Data validation e.g. prevent duplicate applications', 'from the same person'),
                     S(10, 'Any reasonable requirement')],
                    2, 3, steps=[3, 1], head=S(10, 'Functional Requirements'), open_list=True,
                    note=S(11, 'For best requirement', 'understanding demonstrated 1 mark')),
               anyn([S(10, 'The system should be easy to use and accessible to all users'),
                     S(10, 'The system should respond quickly, even with many users'),
                     S(11, 'The system should be secure to protect personal data'),
                     S(11, 'The system should be reliable and available during high demand'),
                     S(11, 'The system should comply with data protection laws'),
                     S(11, 'The system should be scalable to handle increased traffic'),
                     S(11, 'Any reasonable requirement')],
                    2, 3, steps=[3, 1], head=S(10, 'Non-Functional Requirements'), open_list=True,
                    note=S(11, 'For best requirement', 'understanding demonstrated 1 mark'))]),
    dict(key=(13, 'b', 'i'), topic='cs-2-4', total=6,
         why='p10: an example field for String, Integer and Boolean, each explained; the scheme '
             'lists examples per datatype, example 1 and explanation 1',
         stem=P(10, 'Applicants must provide certain details', 'submitting their lottery entry.'),
         ask=[P(10, 'For each of the three datatypes named below', 'appropriate for the datatype.'),
              P(10, 'String example: Explain: Integer example:', 'Boolean example: Explain:')],
         rows=[anyn([S(11, 'Name: Stored as a string', 'may include spaces'),
                     S(11, 'Email address: Stored as a string', 'symbols, and numbers'),
                     S(11, 'Home address: Stored as a string', 'words and spaces'),
                     S(11, 'Any reasonable example', nth=1)],
                    1, 2, head=S(11, 'String'), open_list=True,
                    note=S(11, 'For each datatype:', 'understanding demonstrated 1 mark')),
               anyn([S(11, 'Age: Stored as an integer because it is a whole number'),
                     S(11, 'Number of tickets requested: Stored as an integer', 'counts items'),
                     S(11, 'Year of birth: Stored as an integer', 'whole numbers only'),
                     S(11, 'Any reasonable example', nth=2)],
                    1, 2, head=S(11, 'Integer'), open_list=True,
                    note=S(11, 'For each datatype:', 'understanding demonstrated 1 mark')),
               anyn([S(11, 'Agree to terms and conditions: Boolean', 'either true or false'),
                     S(11, 'Resident of Ireland: Boolean', 'response is yes or no'),
                     S(11, 'Over 18 years old: Boolean', 'only two possible values'),
                     S(11, 'Any reasonable example', nth=3)],
                    1, 2, head=S(11, 'Boolean'), open_list=True,
                    note=S(11, 'For each datatype:', 'understanding demonstrated 1 mark'))]),
    dict(key=(13, 'b', 'ii'), topic='cs-3-1', figure='s-q13b-ii', total=6,
         why='p10: sketch a wireframe; the scheme draws a sample and prices heading 1, controls '
             '2 / 1, annotations 2 / 1 and the submit button 1',
         stem=P(10, 'Applicants must provide certain details', 'submitting their lottery entry.'),
         ask=P(10, 'Sketch a simple wireframe', 'purpose of the main elements.'),
         rows=[pt(S(12, 'Clear heading/image'), 1),
               crit(S(12, 'Controls / Widgets:'), 2, [1],
                    note=S(12, 'Very good examples', 'Fair example - limited understanding 1 mark')),
               crit(S(12, 'Annotations / Notes:'), 2, [1],
                    note=S(12, 'Very good response - clear', 'Fair response - limited understanding 1 mark')),
               pt(S(12, 'Submit pushbutton'), 1)]),
    dict(key=(13, 'c', 'i'), topic='cs-1-2', total=4,
         why='p11: compare an app and a responsive website under two headings; the scheme '
             'answers each heading, 2 / 1',
         stem=P(11, 'The development team is deciding', 'a responsive website.'),
         ask=P(11, 'Compare a mobile application and a responsive website', 'user experience and accessibility.'),
         rows=[anyn([S(12, 'A mobile application can provide a smoother', 'notifications and touch controls.'),
                     S(12, 'A responsive website works through a web browser', 'without installing software.'),
                     S(12, 'Any valid response')],
                    1, 2, head=S(12, 'User Experience'), open_list=True, note=NOTE_Q13C),
               anyn([S(13, 'A responsive website is more accessible', 'using any web browser.'),
                     S(13, 'A mobile application may require a compatible device', 'screen reader support.'),
                     S(13, 'Any valid response')],
                    1, 2, head=S(13, 'Accessibility'), open_list=True, note=NOTE_Q13C)]),
    dict(key=(13, 'c', 'ii'), topic='cs-2-4', total=9,
         why='p11: two validation checks and one verification check; the scheme lists both, '
             'best check 5 and the others 2',
         stem=P(11, 'The development team is deciding', 'a responsive website.'),
         ask=P(11, 'Applicants often make mistakes when entering data.', 'correct (verification).'),
         rows=[anyn([Pair(VALID, S(13, 'Range check:', 'for example 18-120')),
                     Pair(VALID, S(13, 'Format check:', 'includes an @ symbol')),
                     Pair(VALID, S(13, 'Presence check:', 'are not left blank')),
                     Pair(VALID, S(13, 'Length check:', 'correct number of digits')),
                     Pair(VALID, S(13, 'Type check:', 'only contain numbers')),
                     Pair(VALID, S(13, 'Any reasonable example', nth=1)),
                     Pair(VERIFY, S(13, 'Double entry:', 'both entries match')),
                     Pair(VERIFY, S(13, 'Visual check:', 'before submitting')),
                     Pair(VERIFY, S(13, 'Email confirmation:', 'their details are correct')),
                     Pair(VERIFY, S(13, 'Any reasonable example', nth=2))],
                    3, 5, steps=[5, 2, 2], head=P(11, 'Applicants often make mistakes when entering data.'),
                    open_list=True,
                    note=S(13, 'For best check', 'clear understanding demonstrated 2 marks'))]),

    # ── Question 14, the Königsberg bridges ───────────────────────────────
    dict(key=(14, 'a', 'i'), topic='cs-1-1', qfigure='q14a-figs', total=3,
         why='p12: why the given route is not an Euler path; the scheme answers it, 3 / 2',
         stem=[P(12, 'Königsberg was a city built around a river', 'crossing the same bridge twice?'),
               P(12, 'An Euler path is a path that crosses all bridges', 'the same bridge twice.', nth=1)],
         ask=P(12, 'Starting from side A,', 'Outline why this path is not an Euler path.'),
         rows=[crit(S(14, 'The path is not continuous', 'next crossing is not possible.'), 3, [2],
                    note=S(14, 'Very good explanation - clear understanding demonstrated 3 marks',
                           'limited understanding 2 marks'))]),
    dict(key=(14, 'a', 'ii'), topic='cs-1-1', qfigure='q14a-figs', total=6,
         why='p12: an Euler path in each of Figures 4 and 5 from C; the scheme lists the paths, '
             '3 each',
         stem=[P(12, 'Königsberg was a city built around a river', 'crossing the same bridge twice?'),
               P(12, 'An Euler path is a path that crosses all bridges', 'the same bridge twice.', nth=1)],
         ask=P(12, 'Figures 4 and 5 both show alternative bridge networks', 'each of the two figures.'),
         rows=[anyn([S(14, '1→ 3 → 4 → 2', nth=1), S(14, '2→ 4 → 3 → 1', nth=1)], 1, 3,
                    head=S(14, 'Euler Paths from Figure 4 (start at land area C):'),
                    note=S(14, 'For each figure/path:', 'Correct response 3 marks')),
               anyn([S(14, '1→ 3 → 4 → 2 → 5'), S(14, '1→ 3 → 5 → 2 → 4'),
                     S(14, '2→ 4 → 5 → 1 → 3'), S(14, '2→ 4 → 3 → 1 → 5'),
                     S(14, '5→ 3 → 1 → 2 → 4'), S(14, '5→ 4 → 2 → 1 → 3')], 1, 3,
                    head=S(14, 'Euler Paths from Figure 5 (start at land area C):'),
                    note=S(14, 'For each figure/path:', 'Correct response 3 marks'))]),
    dict(key=(14, 'a', 'iii'), topic='cs-1-1', qfigure='q14a-figs', total=4,
         why='p12: odd or even for each land area in Figures 4 and 5; the scheme prints the '
             'table, each correct row 1 (or each correct column 2)',
         stem=[P(12, 'Königsberg was a city built around a river', 'crossing the same bridge twice?'),
               P(12, 'An Euler path is a path that crosses all bridges', 'the same bridge twice.', nth=1)],
         ask=P(12, 'Examine the three figures above.', 'completed for Figure 3.'),
         rows=[pt(S(14, 'A ODD (3) EVEN (2) EVEN (2)'), 1,
                  note=S(14, 'Each Correct Column 2 marks', 'Each Correct Row 1 mark')),
               pt(S(14, 'B ODD (3) EVEN (2) EVEN (2)'), 1),
               pt(S(14, 'C ODD (5) EVEN (2) ODD (3)'), 1),
               pt(S(14, 'D ODD (3) EVEN (2) ODD (3)'), 1)]),
    dict(key=(14, 'a', 'iv'), topic='cs-1-1', qfigure='q14a-figs', total=3,
         why='p13: the pattern an Euler path needs; the scheme prints the two conditions, 3 / 2',
         stem=[P(12, 'Königsberg was a city built around a river', 'crossing the same bridge twice?'),
               P(12, 'An Euler path is a path that crosses all bridges', 'the same bridge twice.', nth=1)],
         ask=P(13, 'Deduce one pattern', 'for an Euler path to exist.'),
         rows=[anyn([S(15, 'Every vertex (land mass) has an even number', 'connected to it'),
                     S(15, 'Exactly two vertices (land masses) have an odd number', 'connected to them.')],
                    1, 3, head=S(15, 'For an Euler path to exist, either of the following conditions must be met:'),
                    note=S(15, 'Very good explanation - clear understanding demonstrated 3 marks',
                           'limited understanding 2 marks'))]),
    dict(key=(14, 'b', 'i'), topic='cs-2-1', qfigure='q14b-fig6', total=8,
         why='p13: abstraction in Figure 6 and one limitation; the scheme answers the first '
             '5 / 3 and lists limitations 3 / 2',
         stem=P(13, 'Abstraction and algorithmic thinking', 'aspects of computational thinking.'),
         ask=P(13, 'Using Figure 6 explain how abstraction', 'using abstraction in this context.'),
         rows=[crit(S(15, 'Abstraction is used by simplifying the real city map', 'not important to the problem.'),
                    5, [3], note=S(15, 'Very good explanation - clear understanding demonstrated 5 marks',
                                   'limited understanding 3 marks')),
               anyn([S(15, 'Important real-world details, such as distances', 'are ignored'),
                     S(15, 'The abstract graph cannot show practical issues', 'walking difficulty'),
                     S(15, 'Some real-world constraints may be missed', 'oversimplified'),
                     S(15, 'Any reasonable limitation')],
                    1, 3, head=S(15, 'Any reasonable limitation'), open_list=True,
                    note=S(15, 'Very good limitation', 'Fair limitation - limited understanding 2 marks'))]),
    dict(key=(14, 'b', 'ii'), topic='cs-1-1', figure='s-q14b-ii', total=4,
         why='p13: the fastest sequence of crossings; the scheme prints the sequence, 4 / 3 / 2',
         stem=P(13, 'Abstraction and algorithmic thinking', 'aspects of computational thinking.'),
         ask=P(13, 'Four friends must cross a dangerous bridge', 'so that everyone gets across.'),
         rows=[crit(S(15, 'A and B cross - 3 minutes', '(TOTAL OPTIMAL TIME 20 minutes)'), 4, [2, 3],
                    note=S(15, 'Very good explanation - clear understanding demonstrated 4 marks',
                           'Fair explanation - limited understanding 2 marks'))]),
    dict(key=(14, 'c', None), topic='cs-1-2', total=10,
         why='p14: appraise positive and negative impacts; the scheme lists both, each impact '
             '5 / 4',
         ask=P(14, 'A city council is considering adopting a system', 'on culture and society.'),
         rows=[anyn([S(16, 'Enhanced access to navigation and route planning', 'unfamiliar areas.'),
                     S(16, 'Reduced travel time and commuter stress', 'journeys less stressful.'),
                     S(16, 'Reduced traffic congestion', 'improve traffic flow.'),
                     S(16, 'Faster emergency service response times', 'saving lives and property.'),
                     S(16, 'Lower fuel consumption and emissions', 'environmental pollution.'),
                     S(16, 'Improved transport, logistics and urban planning', 'future infrastructure.'),
                     S(16, 'Any other positive impact.')],
                    1, 5, head=S(16, 'Potential Positive Impacts'), open_list=True,
                    note=S(16, 'For each impact', 'limited understanding 4 marks')),
               anyn([S(16, 'Privacy concerns from location tracking', 'used, stored or shared.'),
                     S(16, 'Increased traffic through certain areas', 'congestion and disruption.'),
                     S(16, 'Over-reliance on algorithms and loss of navigation skills', 'local knowledge.'),
                     S(16, 'Unequal access and digital divide issues', 'benefit equally from these systems.'),
                     S(16, 'Implementation costs and risk of system failures', 'travel disruption.'),
                     S(16, 'Any other negative impact.')],
                    1, 5, head=S(16, 'Potential Negative Impacts'), open_list=True,
                    note=S(16, 'For each impact', 'limited understanding 4 marks'))]),

    # ── Question 15, the greenhouse controller ────────────────────────────
    dict(key=(15, 'a', 'i'), topic='cs-3-4', qfigure='q15-fig7', total=6,
         why='p15: two digital and two analogue sensors; the scheme lists both, first 2 and '
             'second 1 of each',
         stem=[P(15, 'A horticulture company is designing a greenhouse controller', 'shown in Figure 7.'),
               P(15, 'The system uses a combination of digital and analogue sensors.')],
         ask=P(15, 'Name any two digital sensors', 'used in the greenhouse system.'),
         rows=[anyn([S(17, 'Door sensor (open or closed)'), S(17, 'Motion sensor (movement detected or not)'),
                     S(17, 'Any valid response', nth=1)],
                    2, 2, steps=[2, 1], head=S(17, 'Digital sensors:'), open_list=True),
               anyn([S(17, 'Temperature sensor'), S(17, 'Humidity sensor'), S(17, 'Natural light sensor'),
                     S(17, 'Any valid response', nth=2)],
                    2, 2, steps=[2, 1], head=S(17, 'Analogue sensors:'), open_list=True)]),
    dict(key=(15, 'a', 'ii'), topic='cs-3-4', qfigure='q15-fig7', total=4,
         why='p15: two further outputs; the scheme lists three and any valid, 2 each',
         stem=[P(15, 'A horticulture company is designing a greenhouse controller', 'shown in Figure 7.'),
               P(15, 'The system uses a combination of digital and analogue sensors.')],
         ask=P(15, 'List two additional outputs', 'used in the greenhouse system.'),
         rows=[anyn([S(17, 'Automatic window opener to control airflow'),
                     S(17, 'Alarm or buzzer to warn of unsafe conditions'),
                     S(17, 'Shade blinds to reduce light and heat'),
                     S(17, 'Any valid response', nth=3)],
                    2, 2, head=P(15, 'List two additional outputs', 'used in the greenhouse system.'),
                    open_list=True, note=S(17, 'For each correct response 2 marks'))]),
    dict(key=(15, 'a', 'iii'), topic='cs-2-3', qfigure='q15-fig7', total=4,
         why='p15: digital against analogue sensors; the scheme answers it, 4 / 2',
         stem=[P(15, 'A horticulture company is designing a greenhouse controller', 'shown in Figure 7.'),
               P(15, 'The system uses a combination of digital and analogue sensors.')],
         ask=P(15, 'Describe the difference between digital and analogue sensors.'),
         rows=[crit(S(18, 'Digital sensors produce fixed outputs', 'more detailed information than digital sensors.'),
                    4, [2], note=S(18, 'Very good description - clear understanding demonstrated 4 marks',
                                   'limited understanding 2 marks'))]),
    dict(key=(15, 'b', 'i'), topic='cs-2-5', qfigure='q15b-code', total=6,
         why='p16: a problem with the fan rule and a solution; the scheme answers both, 3 / 2 '
             'each',
         stem=P(16, 'The system maintains healthy growing conditions', 'following a set of rules.'),
         ask=[P(16, 'The intention of the code snippet shown below', 'the state of the door.'),
              P(16, 'Identify one potential problem', 'Describe a solution to overcome the problem.')],
         rows=[crit(S(18, 'If the temperature is above 30 and the door is open', 'incorrect fan behaviour'),
                    3, [2], head=S(18, 'Problem'), note=NOTE_Q15B),
               anyn([S(18, 'Use an if-else statement so the door condition', 'whenever the door is open'),
                     S(18, 'Use an and operator to check', 'the state of the door')],
                    1, 3, head=S(18, 'Solution'), note=NOTE_Q15B)]),
    dict(key=(15, 'b', 'ii'), topic='cs-3-4', total=2,
         why='p16: one further sensor rule; the scheme lists three and any valid, 2 / 1',
         stem=P(16, 'The system maintains healthy growing conditions', 'following a set of rules.'),
         ask=P(16, 'Suggest one additional rule that uses sensors', 'in the greenhouse system.'),
         rows=[anyn([S(18, 'If humidity is too low, turn on the misting system'),
                     S(18, 'If light level is too high, close the shade blinds'),
                     S(18, 'If soil moisture is low, activate the irrigation system'),
                     S(18, 'Any other valid rule that could be used', 'in the greenhouse system'),
                     S(18, 'Any reasonable response')],
                    1, 2, head=P(16, 'Suggest one additional rule that uses sensors', 'in the greenhouse system.'),
                    open_list=True,
                    note=S(18, 'Very good description - clear understanding demonstrated 2 marks',
                           'limited understanding 1 marks'))]),
    dict(key=(15, 'b', 'iii'), topic='cs-3-2', total=6,
         why='p16: a benefit of the stored readings and how they improve the system; the '
             'scheme answers each part, 3 / 2',
         stem=P(16, 'The system maintains healthy growing conditions', 'following a set of rules.'),
         ask=P(16, 'The greenhouse system stores sensor readings', 'improve the performance of the system.'),
         rows=[crit(S(19, 'Collecting this data allows the system', 'maintain healthier growing conditions.'),
                    3, [2], head=S(19, 'Benefit'), note=NOTE_Q15B3),
               crit(S(19, 'Storing sensor readings and fan states', 'adjusted to improve performance.'),
                    3, [2], head=S(19, 'Explain'), note=NOTE_Q15B3)]),
    dict(key=(15, 'c', 'i'), topic='cs-3-4', total=4,
         why='p17: two characteristics of embedded systems, each justified; the scheme lists '
             'both, 1 mark each',
         stem=P(17, 'Reflect on the design and development process', 'or as an individual.'),
         ask=P(17, 'State two characteristics of embedded systems', 'design of a greenhouse controller.'),
         rows=[anyn([S(19, 'Designed to perform a specific task'), S(19, 'Built into a larger system or device'),
                     S(19, 'Operates with limited hardware resources'), S(19, 'Often works in real time'),
                     S(19, 'Uses low power and runs continuously'), S(19, 'Fast response times'),
                     S(19, 'Any other valid characteristic')],
                    2, 1, head=S(19, 'Characteristic of Embedded Systems'), open_list=True,
                    note=S(19, 'For each correct characteristic 1 mark')),
               anyn([S(19, 'Specific task: The controller only needs', 'simple and reliable.'),
                     S(19, 'Part of a larger system:', 'to control the greenhouse.'),
                     S(19, 'Limited resources:', 'cost and energy use.'),
                     S(19, 'Real-time operation:', 'to protect plants.'),
                     S(20, 'Low power use:', 'important for efficiency.'),
                     S(20, 'Fast response time:', 'growing conditions for plants.'),
                     S(20, 'Low cost:', 'effective environmental control.'),
                     S(20, 'Any valid justification for a named characteristic')],
                    2, 1, head=S(19, 'Justifications:'), open_list=True,
                    note=S(20, 'For each justification:', 'understanding demonstrated 1 mark'))]),
    dict(key=(15, 'c', 'ii'), topic='cs-2-5', total=6,
         why='p17: two stages of software testing; the scheme lists eight, best 4 / 3 and '
             'second 2 / 1',
         stem=P(17, 'Reflect on the design and development process', 'or as an individual.'),
         ask=P(17, 'A good test strategy is a key aspect', 'applies to the greenhouse system.'),
         rows=[anyn([S(20, 'Unit testing:', 'works correctly on its own.'),
                     S(20, 'System testing:', 'under real greenhouse conditions.'),
                     S(20, 'Integration testing:', 'work correctly when combined.'),
                     S(20, 'Acceptance testing:', 'before final use.'),
                     S(20, 'Regression testing:', 'fan or heater control.'),
                     S(20, 'Functional Testing:', '(as per requirements).'),
                     S(20, 'Non-Functional Testing:', 'reliability, security etc.'),
                     S(20, 'Any other valid stage of software testing', 'black/white box testing etc.')],
                    2, 4, steps=[4, 2], head=S(20, 'Any two from the following:'), open_list=True,
                    note=S(20, 'For best response:', 'limited understanding 1 mark'))]),

    # ── Section C: Question 16 ────────────────────────────────────────────
    dict(key=(16, 'a', 'i'), topic='cs-2-2', qfigure='q16a-code', figure='s-q16a-i', total=10,
         why='040 p5: print score1 and a blank line; the scheme marks its lines # (i), B-10 scale',
         stem=Q16A_STEM,
         ask=C(5, 'Modify the program so that it displays the readability score for text1',
               'Readability Score 1: 9', nth=1),
         rows=[crit(CORRECT, 10, [7], note=S(23, '(i) 10 marks (B-10 scale)', 'Any other reasonable attempt.'))]),
    dict(key=(16, 'a', 'ii'), topic='cs-2-2', qfigure='q16a-code', figure='s-q16a-ii', total=10,
         why='040 p5: score text2; the scheme marks its lines # (ii), B-10 scale',
         stem=Q16A_STEM,
         ask=C(5, 'Extend the program so that it calls the function', 'Readability Score 2: 0'),
         rows=[crit(CORRECT, 10, [7], note=S(23, '(ii) 10 marks (B-10 scale)', 'Any other reasonable attempt.'))]),
    dict(key=(16, 'a', 'iii'), topic='cs-2-2', qfigure='q16a-code', figure='s-q16a-iii', total=10,
         why='040 p6: count exclamation marks as sentence endings; the scheme marks line 44 '
             '# (iii), B-10 scale',
         stem=Q16A_STEM,
         ask=C(6, 'The program uses a full stop to determine', 'Readability Score 2: 32', nth=1),
         rows=[crit(CORRECT, 10, [7], note=S(23, '(iii) 10 marks (B-10 scale)', 'Any other reasonable attempt.'))]),
    dict(key=(16, 'a', 'iv'), topic='cs-2-2', qfigure='q16a-code', figure='s-q16a-iv', total=10,
         why='040 p6: compare the two scores; the scheme marks its lines (iv), C-10 scale',
         stem=Q16A_STEM,
         ask=C(6, 'Extend the program to compare the two scores', 'The first text is easier to read.', end_nth=2),
         rows=[crit(CORRECT, 10, [3, 7], note=S(23, '(iv) 10 marks (C-10 scale)', 'Any other reasonable attempt.'))]),
    dict(key=(16, 'a', 'v'), topic='cs-2-2', qfigure='q16a-code', figure='s-q16a-v', total=5,
         why='040 p7: count the short words; the scheme marks lines 15-20 v, C-5 scale',
         stem=Q16A_STEM,
         ask=C(7, 'Line 13 in the original program', 'The first text is easier to read.'),
         rows=[crit(CORRECT, 5, [2, 3], note=S(24, '(v) 5 marks (C-5 scale)', 'Any other reasonable attempt.'))]),
    dict(key=(16, 'a', 'vi'), topic='cs-2-2', qfigure='q16a-vi-formula', figure='s-q16a-vi', total=5,
         why='040 p7: a new score formula, printed as a built-up fraction the text layer '
             'mangles, so the formula is in the crop; the scheme marks line 48 # vi, C-5 scale',
         stem=Q16A_STEM,
         ask=[C(7, 'Update the code that calculates the readability score to use the formula:'),
              C(7, 'where, • total words is the variable word_count', 'The second text is easier to read.')],
         rows=[crit(CORRECT, 5, [2, 3], note=S(24, '(vi) 5 marks (C-5 scale)', 'Any other reasonable attempt.'))]),
    dict(key=(16, 'a', 'vii'), topic='cs-2-2', qfigure='q16a-code', figure='s-q16a-vii', total=10,
         why='040 p8: count the complex words; the scheme marks lines 22-41 vii, D-10 scale',
         stem=Q16A_STEM,
         ask=C(8, 'Modify the program so that it counts the number of complex words', 'The second text is easier to read.'),
         rows=[crit(CORRECT, 10, [3, 5, 7], note=S(24, '(vii) 10 marks (D-10 scale)', 'Any other reasonable attempt.'))]),
    dict(key=(16, 'b', None), topic='cs-2-2', qfigure='q16b-output', figure='s-q16b', total=20,
         why='040 p9-10: write the word scoring game; the scheme prints a possible solution and '
             'a rubric of four criteria at 5 / 4 / 3',
         ask=C(9, 'You are required to implement a word scoring game.', 'highest scoring word along with its score.'),
         rows=[crit(T(27, '• Word read in correctly • Play again read in correctly', 'use of assignment statements'),
                    5, [3, 4], head=T(27, 'Inputs'),
                    note=[T(27, 'High level of achievement All of the following', 'correctly and efficiently'),
                          T(27, 'Moderate level of achievement Reasonable attempt', 'each of the following'),
                          T(27, 'Low level of achievement Poor attempt to complete any of the following')]),
               crit(T(27, '• Word converted to uppercase', 'Play again logic'), 5, [3, 4],
                    head=T(27, 'Program Logic (Processing)')),
               crit(T(27, '• Word, score and total score correctly displayed', 'Error message displayed'),
                    5, [3, 4], head=T(27, 'Program Outputs')),
               crit(T(27, '• Program executes correctly', 'Program design is well explained with comments'),
                    5, [3, 4], head=T(27, 'Programming Standards'))]),
]
