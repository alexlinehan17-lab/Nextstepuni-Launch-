"""Computer Science 2022 Ordinary Level: every card of the sitting, lifted from the page.

The 17 cards shipped in August are re-authored here under their own ids (batch
1b), and the 16 the lane added for the asks they missed are kept, converted to
the ladder and instruction rules of 5 Nov. Paper pages 3-20 (Sections A and B)
and Section C pages 4-6, and scheme pages 3-19 were opened. This is the 2022
paper's own format: Section A six of twelve at 5 marks, Section B one long
question of 30. Where the scheme prices a part only in the question head ("3+2
marks"), that head is quoted.

cs-2022-ol-q3, -q5, -q8 and -q10 are shipped as whole questions (two parts,
no part cards beside them) and stay whole with a row per part; so does
cs-2022-ol-q16, the whole of Section C, with a row per part (i)-(vii) headed
by that part's own instruction.

Q13(b)(i)'s scheme lists its four answers as a bare list (True, False, True,
True), paired with the paper's four statements by printed order; both print
four. Its statements carry Wingdings glyphs (a tick, a smiling face), folded
after rendering. Q12's answers are a lone 7 and a lone 1, and Q5(a)'s a lone
3, read from the scheme page by position.

Q1's scheme note on print(a/b) prints a Cambria fraction its text layer reads
as two Oriya digits; the note is not lifted.

Figure 11 (Q15(c)) is printed turned on its side, and its crop shows it as
printed.
"""
from compsci_lane import (At, C, P, Pair, S, anyn, crit, crop, ladder, ofpart, pt, stack)  # noqa: F401

FIG8 = ('038', 10, (54, 130, 551, 296))

CROPS = {
    'q1-table': crop('038', 3, (122, 177, 456, 381), ref='2022 OL Q1',
                     alt='The declarations printed with Question 1, a = 2 and b = 4, above a table '
                         'whose print statement column lists print(a+b), print(b-a), print(a*b), '
                         'print(a/b) and print(a==b), and whose Result column is blank.'),
    'q3-figs': stack([('038', 4, (52, 159, 300, 373)), ('038', 4, (339, 157, 556, 482))],
                     ref='2022 OL Q3',
                     alt='Figure 2, the pseudocode: Start; Set all pins to off; Set pin 0 to on; '
                         'Pause for 2 seconds; Set pin 0 to off; Set pin 1 to on; Pause for 2 '
                         'seconds; Set pin 1 to off; Set pin 2 to on. Below it, Figure 3: a '
                         'Micro:bit with a green LED wired to pin 0, a yellow LED to pin 1 and a '
                         'red LED to pin 2, each returning to GND.'),
    'q4-fig4': crop('038', 5, (422, 71, 572, 230), ref='2022 OL Q4',
                    alt='Figure 4: a photograph of an open desktop computer case showing its '
                        'motherboard, fans, cards and drive bays.'),
    'q15-fig11': crop('038', 19, (62, 54, 539, 752), ref='2022 OL Q15(c)', rotate=90,
                      alt='Figure 11, turned upright (the paper prints it on its side): a screenshot of the website '
                          'www.irishwrecksonline.net, A Diver\'s Guide to the Ship Wrecks around '
                          'Ireland, with a green map of Ireland in the centre, small text in '
                          'several colours, and a column of menu buttons on a blue background.'),
    'q2-fig1': crop('038', 3, (320, 440, 543, 590), ref='2022 OL Q2',
                    alt='Figure 1: an aerial photograph of a busy road junction with cars at '
                        'traffic lights.'),
    'q6-flow': crop('038', 6, (83, 123, 511, 418), ref='2022 OL Q6',
                    alt='Figure 5: a flowchart for a number-guessing game. Start; Number = '
                        'random number between 1 and 10; Guess = user input; a decision Guess = '
                        'Number? whose true branch prints "Correct" and whose false branch leads '
                        'to a decision labelled A, its text missing. A\'s false branch prints '
                        '"Too High" and its true branch prints "Too Low"; every branch ends at '
                        'End.'),
    'q9-fig6': crop('038', 8, (160, 128, 515, 348), ref='2022 OL Q9',
                    alt='Figure 6: a phone app called Movie Rater showing a film poster, a box '
                        'labelled Score out of 10 and a Submit button, beside the scores '
                        'collected: 8, 5, Four, 9.5, 10/10, 6 and 5 or 6.'),
    'q11-fig7': crop('038', 9, (138, 455, 458, 747), ref='2022 OL Q11',
                     alt='Figure 7: an AND gate with inputs A and B. Below it, the truth table '
                         'with columns A, B and A AND B; the inputs read 0 0, 0 1, 1 0 and 1 1 '
                         'and the output column is blank.'),
    'q12a-game': stack([FIG8, ('038', 10, (53, 324, 230, 416))], ref='2022 OL Q12(a)',
                       alt='The game printed with Question 12: a table of the three instructions '
                           '(Step Forward, step forward one square; Turn Right and Turn Left, '
                           'rotate 90 degrees without moving), and Figure 8, a grid of numbered '
                           'squares with a Start square. Below them, part (a)\'s instructions: '
                           'Step Forward, Turn Right, Repeat 2 times: {Step Forward}.'),
    'q12b-game': stack([FIG8, ('038', 10, (53, 448, 230, 559))], ref='2022 OL Q12(b)',
                       alt='The game printed with Question 12: a table of the three instructions '
                           '(Step Forward, step forward one square; Turn Right and Turn Left, '
                           'rotate 90 degrees without moving), and Figure 8, a grid of numbered '
                           'squares with a Start square. Below them, part (b)\'s instructions: '
                           'Repeat 2 times: {Step Forward}, then Repeat 3 times: {Turn Right, '
                           'Step Forward}.'),
    'q13a-ii': stack([('038', 11, (115, 455, 555, 565)), ('038', 11, (115, 596, 310, 701))],
                     ref='2022 OL Q13(a)(ii)',
                     alt='Figure 9: a digital clock showing 12:28, beside its four digits in '
                         'binary (first digit 0001, second 0010, third 0010, fourth 1000). Below, '
                         'the four codes the question asks about: first digit 0010, second 0000, '
                         'third 0101, fourth 1001.'),
    'q13b-tf': crop('038', 12, (100, 122, 540, 262), ref='2022 OL Q13(b)(i)',
                    alt='The four statements printed with Question 13(b)(i), each with an empty '
                        'True box and an empty False box: the letter r can be represented in '
                        'ASCII; the emoji symbol (a smiling face) can be represented in ASCII; the '
                        'number 9 can be represented in Unicode; the symbol @ can be represented '
                        'in Unicode.'),
    'q14b-table': crop('038', 15, (54, 142, 542, 348), ref='2022 OL Q14(b)(i)',
                       alt='The table printed with Question 14(b)(i), with columns Variable Name, '
                           'Description and Data Type; the first row reads firstName, Student\'s '
                           'first name, String, and four rows are blank.'),
    's-q14c': crop('scheme', 14, (54, 337, 541, 600), ref='2022 OL Q14(c)', solution=True,
                   alt='The marking scheme\'s example solution to Question 14(c), a decision '
                       'tree: Student name, then Is student in 6th year?. One branch asks Does '
                       'Student have parental permission, ending in Permission to leave or No '
                       'Permission; the other asks Does student have a sibling in 6th year, '
                       'ending in No Permission or in the parental permission question with '
                       'the same two outcomes.'),
    's-q16': crop('scheme', 17, (81, 184, 550, 600), ref='2022 OL Q16(a)', solution=True,
                  alt='The marking scheme\'s possible solution to Question 16(a), lines 1 to 27: '
                      'a comment # user enters first name; firstName and surname read with '
                      'input; print("Hello", firstName, surname, ...); the items 1 = Book, 2 = '
                      'Ruler and 3 = Pen printed between two dashed lines; shoppingItem read with '
                      'int(input()); then if / elif branches printing You bought a book, a ruler or '
                      'a pen, and else printing Invalid choice. Goodbye.'),
    'q15-fig10': crop('038', 17, (67, 123, 529, 316), ref='2022 OL Q15(a)',
                      alt='Figure 10: a timeline of computing developments: 1943 the first '
                          'mainframe computer; 1946 the first general purpose computer using '
                          'vacuum tubes; 1953 the first computer programming language COBOL; 1958 '
                          'the first integrated circuit (computer chip); 1971 the floppy disk; '
                          '1989 Tim Berners-Lee proposes the World Wide Web.'),
}

Q2_NOTE = S(4, 'First Correct: Very good explanation', 'Fair explanation – limited understanding 1 mark', end_nth=2)
Q6_STEM = P(6, 'The flowchart, in Figure 5 below, is that of an algorithm', 'randomly selected by the computer.')
Q9_STEM = P(8, 'Your friend has designed the app in Figure 6', 'write a Python program to analyse the data.')
Q12_STEM = P(10, 'In a game, shown in Figure 8, a player begins', 'Instructions for the game are provided in pseudocode.')
Q13A_STEM = P(11, 'Computer memory is measured in bits.', 'the bigger the memory.')
Q13B_STEM = P(12, 'ASCII (American Standard Code for Information Interchange) and Unicode', 'digital communication.')
Q14_STEM = P(14, 'A secondary school wants to write a computer program', 'grounds at lunch time.')
Q15_STEM = P(17, 'Computing and technology has made huge progress', 'over the last century.')

Q14A = [Q14_STEM, P(14, 'The school principal has provided the Computer Science class', 'student can leave the school grounds.')]
Q14B = [Q14_STEM, P(15, 'You will need to get data from the school office', 'in order to create the program.')]
Q15C_STEM = P(18, 'It is very important to have a website that has a good user interface', 'answer the questions that follow.')
CORRECT = 'Correct implementation using solution above or similar.'

Q16_STEM = C(4, 'The program above is to simulate an automated shop.', 'confirming the item they chose.')
WITHDRAWN = {'cs-2022-ol-q16': 'cs-2022-ol-q16-a-i'}

CARDS = [
    # ── Section A ──────────────────────────────────────────────────────────
    dict(key=(1, None, None), topic='cs-2-2', qfigure='q1-table', total=5,
         replaces='batch 1b: the five results were lost (no answer rows); the figure was cut '
                  'through its Result column and sat on the answer side',
         why='p3: the result of five print statements; the scheme prints each, 1 mark',
         ask=P(3, 'Given the following variable declarations', 'in the table below.'),
         rows=[pt(S(4, 'print(a+b) 6'), 1, note=S(4, 'Each correct item 1 mark')),
               pt(S(4, 'print(b-a) 2'), 1), pt(S(4, 'print(a*b) 8'), 1),
               pt(S(4, 'print(a/b) 0.5'), 1), pt(S(4, 'print(a==b) FALSE'), 1)]),
    dict(key=(2, None, None), topic='cs-3-3', qfigure='q2-fig1', total=5,
         why='p3: two reasons a computer model helps; the scheme lists five, first 3 / 1 and '
             'second 2 / 1',
         ask=P(3, 'The traffic at a busy road junction', 'useful in this situation.'),
         rows=[ladder([S(4, 'Identifying traffic patterns.'), S(4, 'Help improve traffic flow at the junction.'),
                       S(4, 'Change traffic light times at different times of the day.'),
                       S(4, 'Get information on different modes of transportation being used.'),
                       S(4, 'Save people time, stop delays')], [[1, 3], [1, 2]],
                      head=S(4, 'Any two of the above or similar:'), note=Q2_NOTE)]),
    dict(key=(3, None, None), topic='cs-2-2', qfigure='q3-figs', total=5,
         replaces='batch 1b: unpriced question-total rows; the figure carried (a)\'s ask and sat on '
                  'the answer side',
         why='p4: shipped as the whole of Q3. (a) why the pauses, three answers 3 / 1; (b) the '
             'LEDs at the end, 2 / 1',
         stem=P(4, 'The pseudocode, shown in Figure 2 below', 'Answer the questions that follow.'),
         ask=P(4, '(a) Why are pauses included in this algorithm?', 'at the end of the algorithm.'),
         rows=[ofpart(P(4, '(a)'), ladder([S(5, 'To see the changes of the LED turning on or off'),
                       S(5, 'The code will run too quickly to see LEDS without the pauses'),
                       S(5, 'To see if the code works correctly')], [[1, 3]],
                      head=S(5, 'Any one of the above or similar:'),
                      note=S(5, 'Good explanation – clear understanding demonstrated 3 marks',
                             'Fair explanation – limited understanding 1 mark'))),
               ofpart(P(4, '(b)'), crit(S(5, 'The red LED is on, the yellow and green LEDs are off'), 2, [1],
                    note=S(5, 'Describing correctly all 3 of the LED’s appearance 2 marks', 'but not all 3 1 mark')))]),
    dict(key=(4, None, None), topic='cs-2-3', qfigure='q4-fig4', total=5,
         replaces='batch 1b: one component was the only answer, all or nothing at 5; the figure '
                  'carried the ask and sat on the answer side',
         why='p5: three components and their purpose; the scheme describes six, the best two '
             '2 / 1 each and the third 1',
         ask=P(5, 'If you were to look inside any modern computer', 'briefly describe their purpose.'),
         rows=[ladder([S(5, 'Motherboard -> This is a circuit board', 'connect into.'),
                       S(5, 'Central Processing Unit (CPU) -> Contains', 'instructions that come to it.'),
                       S(5, 'Fan -> Used to keep the computer cool to avoid damage.'),
                       S(5, 'Memory -> Contains data and programs', 'start (‘boot up’).'),
                       S(5, 'Hard Drive -> This component is used', 'switched off.'),
                       S(5, 'Video Card -> Improves video and graphic quality on the computer or device.')],
                      [[1, 2], [1, 2], [1]],
                      note=S(5, 'Best two responses marked out of 2', 'Fair description – limited understanding 1 mark each',
                             end_nth=2))]),
    dict(key=(5, None, None), topic='cs-2-2', total=5,
         replaces='batch 1b: unpriced question-total rows; (a)\'s answer was lost',
         why='p5: shipped as the whole of Q5. (a) the index of 94, 3 (a lone digit, read by '
             'position), 2; (b) a limitation of linear search, three answers 3 / 1',
         stem=P(5, 'A linear search algorithm, written in Python', '62, 47]'),
         ask=P(5, '(a) What index value will be returned', 'limitation of the linear search algorithm.'),
         rows=[ofpart(P(5, '(a)'), pt(At('scheme', 6, (102, 86, 119, 101)), 2, note=S(6, 'Correct response 2 marks'))),
               ofpart(P(5, '(b)'), ladder([S(6, 'Not an efficient way of searching.'),
                       S(6, 'In big data sets it will take a long time to complete the search.'),
                       S(6, 'Will only find the first number even if the number appears more than once.')], [[1, 3]],
                      note=S(6, 'Good description – clear understanding demonstrated 3 marks',
                             'Fair description – limited understanding 1 mark')))]),
    dict(key=(6, 'a', None), topic='cs-2-2', qfigure='q6-flow', figure='q6-flow', total=3,
         printed=S(6, 'Question 6 3+2 marks'),
         labels={'A': S(6, 'Guess < Number (Less than)')},
         why='p6: the missing text of the symbol labelled A; the scheme prints two forms, 3 / 1',
         stem=Q6_STEM,
         ask=P(6, 'What text is missing from the symbol labelled A?'),
         rows=[ladder([S(6, 'Guess < Number (Less than)'), S(6, 'Number greater than Guess (Greater than)')], [[1, 3]],
                      head=S(6, 'Any one of the above or similar:', nth=1),
                      note=S(6, 'Very clear instruction', 'small mistake with symbols or logic 1 mark'))]),
    dict(key=(6, 'b', None), topic='cs-2-2', qfigure='q6-flow', total=2, printed=S(6, 'Question 6 3+2 marks'),
         why='p6: an improvement so the game allows more than one guess; the scheme lists four '
             'and any of merit, 2',
         stem=Q6_STEM,
         ask=P(6, 'This game will end after the user makes one guess.', 'Suggest an improvement to the algorithm.'),
         rows=[anyn([S(6, 'Give user a second chance to guess.'), S(6, 'Error checking to see that guess is between 1 and 10.'),
                     S(6, 'Show the correct answer at the end.'), S(6, 'Ask the user do they want to play again.'),
                     S(6, 'Any improvement of merit.')], 1, 2, open_list=True,
                    head=S(6, 'Any one of the above or similar:', nth=2), note=S(6, 'Any one of the above or similar: Correct 2 marks'))]),
    dict(key=(7, None, None), topic='cs-1-2', total=5,
         replaces='batch 1b: no answer rows (an empty card); topic was Algorithms',
         why='p7: a woman who shaped computer science and her development; the scheme names '
             'four, the name 2 and the description 3 / 1. Filed under Computers and society',
         ask=P(7, 'Name one female that has made a significant impact', 'the development she worked on.'),
         rows=[ladder([S(6, 'Ada Lovelace -> Considered the first computer programmer.', 'the first algorithm.'),
                       S(6, 'Dame Mary Cartwright -> Only woman to be president', 'study Chaos Theory.'),
                       S(6, 'Katherine Johnson -> Mathematician working for NASA.', 'engineering department.'),
                       S(6, 'Margaret Hamilton -> Considered one of the first computer programmers.', 'Apollo’s spacecraft.')],
                      [[1, 2, 3, 5]], head=S(7, 'Any one of the above or alternative:'),
                      note=S(7, 'Name of female who contributed', 'Fair description – limited understanding 1 mark'))]),
    dict(key=(8, None, None), topic='cs-1-2', total=5,
         replaces='batch 1b: unpriced question-total rows; (a)\'s pricing line was lost',
         why='p7: shipped as the whole of Q8. (a) one way technology helped in the pandemic, six '
             'answers 3 / 1; (b) the digital divide, two answers 2 / 1',
         stem=P(7, 'COVID-19 has had a significant impact', 'the “digital divide”.'),
         ask=P(7, '(a) Describe one way digital technology', 'the term “digital divide”.'),
         rows=[ofpart(P(7, '(a)'), ladder([S(7, 'COVID Tracker App'), S(7, 'Online Video Calls.'), S(7, 'Entertainment online.'),
                       S(7, 'Communicate with other people.'), S(7, 'Getting information to stay informed.'),
                       S(7, 'Online working and schooling.')], [[1, 3]],
                      head=S(7, 'Any one of the above or similar:', nth=1),
                      note=S(7, 'Very good description – clear understanding demonstrated 3 marks',
                             'Fair description – limited understanding 1 mark', nth=2))),
               ofpart(P(7, '(b)'), ladder([S(7, 'Some people can afford or get access to technology and others cannot.'),
                       S(7, 'The people who cannot afford or get access to technology', 'being done online.')], [[1, 2]],
                      head=S(7, 'Any one of the above or similar:', nth=2),
                      note=S(7, 'Good explanation – clear understanding demonstrated 2 marks',
                             'Fair explanation – limited understanding 1 mark')))]),
    dict(key=(9, 'a', None), topic='cs-3-2', qfigure='q9-fig6', total=3, printed=S(7, 'Each Correct Item 1 mark'),
         tariff_note='three issues asked, each correct item 1 mark',
         why='p8: three issues in the dataset; the scheme lists four, 1 each',
         stem=Q9_STEM,
         ask=P(8, 'Identify three issues with the dataset', 'from being able to analyse it.'),
         rows=[anyn([S(7, 'Four'), S(7, '9.5'), S(7, '10/10'), S(7, '5 or 6')], 3, 1,
                    head=P(8, 'Identify three issues with the dataset', 'from being able to analyse it.'),
                    note=S(7, 'Each Correct Item 1 mark'))]),
    dict(key=(9, 'b', None), topic='cs-3-2', qfigure='q9-fig6', total=2,
         printed=S(8, 'Good explanation – clear improvement described 2 marks'),
         why='p8: an improvement to the app for cleaner data; the scheme lists three, 2 / 1',
         stem=Q9_STEM,
         ask=P(8, 'Suggest an improvement to the app', 'analysed more easily.'),
         rows=[ladder([S(8, 'Have a drop down menu so only numbers can be picked.'), S(8, 'Have a keypad with numbers 1 – 10'),
                       S(8, 'Have an error message if the user enters an invalid score')], [[1, 2]],
                      head=S(8, 'Any one of the above or similar:', nth=1),
                      note=S(8, 'Good explanation – clear improvement described 2 marks', 'not described 1 mark'))]),
    dict(key=(10, None, None), topic='cs-2-3', qfigure='q10-fig0', total=5,
         replaces='batch 1b: unpriced question-total rows; the figure sat on the answer side',
         why='p9: shipped as the whole of Q10. (a) match three components to their letters, 1 '
             'each; (b) one component\'s purpose, three answers 2 / 1. The shipped crop of the '
             'three pictures and the table was opened and is complete',
         ask=P(9, '(a) Match the picture of the electronic component', 'explain its purpose.'),
         rows=[ofpart(P(9, '(a)'), pt(S(8, 'Transistor C'), 1, note=S(8, 'Each Correct Item 1 mark'))),
               ofpart(P(9, '(a)'), pt(S(8, 'Capacitor A'), 1)), ofpart(P(9, '(a)'), pt(S(8, 'Resistor B'), 1)),
               ofpart(P(9, '(b)'), ladder([S(8, 'Transistor -> Used to control current and voltage in a circuit.'),
                       S(8, 'Capacitor -> Are used to store electrical charge'),
                       S(8, 'Resistors -> Are used to slow down the flow of current in a circuit.')], [[1, 2]],
                      head=S(8, 'Any one of the above or similar:', nth=2),
                      note=S(8, 'Good explanation – clear understanding demonstrated 2 marks',
                             'Fair explanation – limited understanding 1 mark')))]),
    dict(key=(11, None, None), topic='cs-2-3', qfigure='q11-fig7', total=5,
         why='p9: the AND truth table; the scheme prints the four outputs, each 1, full 5',
         ask=P(9, 'Complete the truth table for the AND logic gate, shown in Figure 7.'),
         rows=[anyn([S(9, '0 0 0 / False'), S(9, '0 1 0 / False'), S(9, '1 0 0 / False'), S(9, '1 1 1 / True')],
                    4, 1, steps=[1, 1, 1, 2], head=S(9, 'INPUTS OUTPUTS A B A AND B'),
                    note=S(9, 'Full correct response 5 marks Each Correct Item 1 mark'))]),
    dict(key=(12, 'a', None), topic='cs-1-1', qfigure='q12a-game', total=3, printed=S(9, 'Question 12 3+2 marks'),
         why='p10: the finishing square for part (a)\'s instructions; the scheme prints 7, 3 / 1',
         stem=Q12_STEM,
         ask=P(10, 'What number square will the player finish on when they follow these instructions?', nth=1),
         rows=[crit(At('scheme', 9, (178, 438, 195, 455)), 3, [1],
                    note=S(9, 'Correct answer 3 marks Attempt work of merit 1 mark'))]),
    dict(key=(12, 'b', None), topic='cs-1-1', qfigure='q12b-game', total=2, printed=S(9, 'Question 12 3+2 marks'),
         why='p10: the finishing square for part (b)\'s instructions; the scheme prints 1, 2 / 1',
         stem=Q12_STEM,
         ask=P(10, 'What number square will the player finish on when they follow these instructions?', nth=2),
         rows=[crit(At('scheme', 9, (178, 538, 195, 555)), 2, [1],
                    note=S(9, 'Correct answer 2 marks Attempt work of merit 1 mark'))]),
    # ── Section B ──────────────────────────────────────────────────────────
    dict(key=(13, 'a', 'i'), topic='cs-2-4', total=4,
         why='p11: order four memory sizes; the scheme prints the order, 1 each',
         stem=Q13A_STEM,
         ask=P(11, 'Order the memory sizes in the list below', 'Terabyte Bit Gigabyte Kilobyte'),
         rows=[pt(S(10, '1 (smallest) Bit'), 1, note=S(10, 'Each correct item 1 mark')),
               pt(S(10, '2 Kilobyte'), 1), pt(S(10, '3 Gigabyte'), 1), pt(S(10, '4 (largest) Terabyte'), 1)]),
    dict(key=(13, 'a', 'ii'), topic='cs-2-3', qfigure='q13a-ii', total=8,
         why='p11: the time the binary code shows; the scheme prints 20:59, each digit 2 and '
             'work of merit for a digit 1',
         stem=Q13A_STEM,
         ask=P(11, 'A 24-hour digital alarm clock displays 4 digits', 'with the following binary code?'),
         rows=[crit(S(10, '20:59'), 8, [1, 2, 3, 4, 5, 6, 7],
                    note=S(10, 'Each correct digit 2 marks Work of merit for a digit 1 mark'))]),
    dict(key=(13, 'b', 'i'), topic='cs-2-4', qfigure='q13b-tf', total=4,
         why='p12: four statements true or false; the scheme lists the answers in order, 1 each',
         stem=Q13B_STEM,
         ask=P(12, 'State whether each of the following statements is true or false', 'in the appropriate box.'),
         rows=[pt(Pair(P(12, 'The letter r can be represented in ASCII.'), S(10, 'True', nth=1)), 1,
                  note=S(10, 'Each correct answer 1 mark')),
               pt(Pair(P(12, 'The emoji symbol', 'can be represented in ASCII.'), S(10, 'False', nth=1)), 1),
               pt(Pair(P(12, 'The number 9 can be represented in Unicode.'), S(10, 'True', nth=2)), 1),
               pt(Pair(P(12, 'The symbol @ can be represented in Unicode.'), S(10, 'True', nth=3)), 1)]),
    dict(key=(13, 'b', 'ii'), topic='cs-2-4', total=4,
         why='p12: the extra characters 8 bits give; the scheme prints 128, 4 / 2',
         stem=Q13B_STEM,
         ask=P(12, 'Extended ASCII uses 8 bits per character', 'rather than 7 bits.', end_nth=2),
         rows=[crit(S(10, '128 extra characters'), 4, [2], note=S(10, 'Correct value 4 marks Work of merit 2 mark'))]),
    dict(key=(13, 'c', 'i'), topic='cs-2-3', total=5,
         replaces='batch 1b: no answer rows (an empty card); the stem was missing and Q13(a)(ii)\'s '
                  'figure sat on the answer side',
         why='p12: two differences between primary and secondary storage; the scheme lists four, '
             'first 3 / 1 and second 2 / 1',
         stem=P(12, 'Data in computers is typically stored in primary or secondary storage.'),
         ask=P(12, 'Describe two differences between primary and secondary storage in computers.'),
         rows=[ladder([S(11, 'Primary storage is contained within the device', 'USB, hard- drive.'),
                       S(11, 'Primary storage can be volatile and non-volatile.', 'non- volatile storage.'),
                       S(11, 'Secondary storage has slower access times than primary storage'),
                       S(11, 'Primary storage is usually more expensive than secondary storage.')], [[1, 3], [1, 2]],
                      head=S(11, 'Any two of the above or similar:'),
                      note=S(11, 'First Correct: Good explanation – clear understanding of difference 3 marks',
                             'Fair explanation – limited understanding of difference 1 mark', end_nth=2))]),
    dict(key=(13, 'c', 'ii'), topic='cs-2-3', total=5,
         why='p13: two differences between SSDs and HDDs; the scheme lists five, best 3 / 1 and '
             'second 2 / 1',
         ask=P(13, 'The use of Solid State Drives', 'two differences'),
         rows=[ladder([S(11, 'Solid State drives can operate faster than Hard disk drives.'),
                       S(11, 'Solid state drives are lighter than the Hard disk drive.'),
                       S(11, 'Solid State Drives is smaller in size (takes up less space)'),
                       S(11, 'Hard Disk Drives are cheaper than Solid State Drives'),
                       S(11, 'Solid State drive doesn’t produce noise', 'can create some noise.')], [[1, 3], [1, 2]],
                      head=S(11, 'Best response marked out of 3 and second best response marked out of 2 as follows:'),
                      note=S(11, 'First Correct: Good explanation – clear understanding of difference 3 marks',
                             'limited understanding of difference 1 Mark', nth=2))]),
    dict(key=(14, 'a', 'i'), topic='cs-2-1', total=4,
         replaces='batch 1b: no answer rows (an empty card); the principal\'s information was '
                  'missing from the stem',
         why='p14: two pieces of the principal\'s information not needed; the scheme lists six, '
             '2 each',
         stem=Q14A,
         ask=P(14, 'Using the computational thinking skill of abstraction', 'not needed to solve this problem.'),
         rows=[anyn([S(12, 'There are 700 students in the school'), S(12, 'There are 120 students in 6th year'),
                     S(12, 'The school is a mixed school'), S(12, 'The school has 40% males'),
                     S(12, 'The school has 60% females.'), S(12, 'Lunch break is 1 hour long'),
                     S(12, 'Any valid response')], 2, 2, open_list=True,
                    head=P(14, 'Using the computational thinking skill of abstraction', 'not needed to solve this problem.'),
                    note=S(12, 'Each correct statement 2 marks'))]),
    dict(key=(14, 'a', 'ii'), topic='cs-1-1', total=4,
         replaces='batch 1b: no answer rows (an empty card); topic was Algorithms',
         why='p14: another computational thinking skill and how it is used; the scheme names '
             'three with a description each, named 1 and described 3 / 1. Filed under '
             'Computational thinking',
         stem=Q14A,
         ask=P(14, 'Name one other computational thinking skill', 'how you will use it.'),
         rows=[ladder([Pair(S(12, 'Decomposition'), S(12, 'Description on how the problem can be broken down into manageable pieces.')),
                       Pair(S(12, 'Pattern Recognition'), S(12, 'Description on how the problem can be identified through patterns', 'used to solve it.')),
                       Pair(S(12, 'Algorithmic Thinking'), S(12, 'Description on how the problem can be solved using an algorithm.'))],
                      [[1, 2, 3, 4]], instruction=S(12, 'Any other valid response'),
                      note=S(12, 'Identifying computational technique as above or otherwise: 1 mark',
                             'Fair description – limited understanding 1 mark'))]),
    dict(key=(14, 'b', 'i'), topic='cs-2-4', qfigure='q14b-table', total=8,
         why='p15: four further rows of variable name, description and data type; the scheme '
             'lists examples, each fully correct row 2 and partially correct 1',
         stem=Q14B,
         ask=P(15, 'Complete the table below with four items of data', 'The first row has been completed for you.'),
         rows=[ladder([S(13, 'Last Name (String)'), S(13, 'Year group (Int)'), S(13, 'Sibling in 6th Year (Boolean)'),
                       S(13, 'Permission slip signed (Boolean)'), S(13, 'Parents Name (String)'),
                       S(13, 'Number of Siblings (int)')], [[1, 2], [1, 2], [1, 2], [1, 2]],
                      head=S(13, 'Any variable created regarding the above with appropriate variable name:'),
                      instruction=S(13, 'Any other valid piece of data relevant to the problem'),
                      note=S(13, 'Each fully correct row 2 marks Each partially correct row 1 mark'))]),
    dict(key=(14, 'b', 'ii'), topic='cs-2-5', total=4,
         replaces='batch 1b: no answer rows (an empty card); topic was Algorithms',
         why='p15: a passing and a failing test student; the scheme lists what each must '
             'mention, all 2 and some 1 for each. Filed under Evaluation and testing',
         stem=Q14B,
         ask=P(15, 'When the program is complete you will need to test', 'no parental consent will fail the test.'),
         rows=[crit(S(13, 'Person name', 'Sibling (for person not in 6th year)'), 2, [1],
                    head=S(13, 'Pass test case:'),
                    note=[S(13, 'Test case must mention:'),
                          S(13, 'Pass test case: All of above is included in test case 2 marks',
                            'Some of above are included in test case 1 mark')]),
               crit(S(13, 'Person name', 'Sibling (for person not in 6th year)'), 2, [1],
                    head=S(13, 'Fail test case:'),
                    note=S(13, 'Fail test case: All of above is included in test case 2 marks',
                           '(No marks if example is repeated as a test case)'))]),
    dict(key=(14, 'c', None), topic='cs-2-2', figure='s-q14c', total=10,
         replaces='batch 1b: no answer rows (an empty card); the scheme\'s example flowchart was '
                  'missing',
         why='p16: the algorithm as pseudocode or a flowchart; the scheme prices the three key '
             'decisions 2 each, the layout 2 / 1 and the outcomes 2 / 1, and draws an example',
         stem=Q14A,
         ask=P(16, 'Using either pseudocode or a flowchart', 'for the school principal.'),
         rows=[anyn([S(14, 'Is student in 6th year -> Yes/ No'), S(14, 'Does the student have a sibling in 6th year? Yes/ No'),
                     S(14, 'Does student have parental permission Yes/ No')], 3, 2,
                    head=S(14, 'Key decisions within algorithm and the outcomes correctly stated.'),
                    note=S(14, 'Key decision and outcomes included 2 marks each (max 6)')),
               crit(S(14, 'Layout of pseudocode or flowchart'), 2, [1],
                    note=S(14, 'Layout of pseudocode or flowchart Good 2 marks Fair 1 mark')),
               crit(S(14, 'All outcomes considered correctly'), 2, [1], head=S(14, 'Outcomes'),
                    note=S(14, 'All outcomes considered correctly 2 marks', 'Any outcomes considered correctly 1 mark'))]),
    dict(key=(15, 'a', 'i'), topic='cs-1-2', qfigure='q15-fig10', total=2,
         why='p17: one other important development; the scheme accepts any, 2 marks, and names '
             'no example',
         stem=Q15_STEM,
         ask=P(17, 'Describe one other development from the last 100 years', 'computing and technology.'),
         rows=[pt(S(15, 'Any important development in computing and technology'), 2,
                  note=S(15, 'Good description - clear understanding demonstrated 2 marks', nth=1))]),
    dict(key=(15, 'a', 'ii'), topic='cs-1-2', qfigure='q15-fig10', total=4,
         why='p17: two reasons the development mattered; the scheme prices each reason 2 '
             'detailed, 1 brief, and names no example',
         stem=Q15_STEM,
         ask=P(17, 'Select a development from either Figure 10', 'this development was important.'),
         rows=[crit(S(15, 'Detailed reason why the development was important'), 4, [1, 2, 3],
                    note=S(15, 'For each reason:', 'Brief reason why the development was important 1 mark'))]),
    dict(key=(15, 'b', None), topic='cs-2-3', total=6,
         replaces='batch 1b: no answer rows (an empty card); Figure 10 (part (a)\'s) sat on the '
                  'answer side',
         why='p18: the World Wide Web against the Internet; the scheme gives three answers, '
             '6 / 3 / 1',
         ask=P(18, 'The World Wide Web and the Internet are often thought', 'the World Wide Web and the Internet.'),
         rows=[ladder([S(15, 'The internet is the connections between networks and devices', 'through these connections.'),
                       S(15, 'The world wide web is a collection of websites.', 'connected to the internet.'),
                       S(15, 'The internet is the connections between networks. The world wide web', 'accessed on the internet.')],
                      [[1, 3, 6]],
                      note=S(15, 'Very good explanation - clear understanding demonstrated 6 marks',
                             'Fair explanation - limited understanding 1 mark'))]),
    dict(key=(15, 'c', 'i'), topic='cs-1-2', qfigure='q15-fig11', total=6,
         replaces='batch 1b: no answer rows (an empty card); Figure 10 sat on the answer side '
                  'instead of Figure 11, which the ask is about',
         why='p18: one good and one poor feature of the website\'s interface; the scheme lists '
             'three good and four poor, 3 each',
         stem=Q15C_STEM,
         ask=P(18, 'Identify one good feature and one poor feature', 'design on the website.'),
         rows=[anyn([S(16, 'Clear visual of Ireland'), S(16, 'Menu neatly laid out'), S(16, 'Clear title')], 1, 3,
                    head=S(16, 'Good features:'), note=S(16, 'Any one of the above or similar 3 marks')),
               anyn([S(16, 'Not good colour combinations'), S(16, 'Some text very small'),
                     S(16, 'No navigation bar'), S(16, 'Poor structure to the page')], 1, 3,
                    head=S(16, 'Poor features:'), note=S(16, 'Any one of the above or similar 3 marks', nth=2))]),
    dict(key=(15, 'c', 'ii'), topic='cs-1-2', qfigure='q15-fig11', total=6,
         replaces='batch 1b: no answer rows (an empty card); Figure 10 sat on the answer side '
                  'instead of Figure 11',
         why='p18: three improvements to the website\'s design; the scheme lists six, 2 each',
         stem=Q15C_STEM,
         ask=P(18, 'Suggest three improvements to the design of this website.'),
         rows=[anyn([S(16, 'Spread content across all the webpage'), S(16, 'Be more consistent with text size.'),
                     S(16, 'Use more colours that complement each other.'), S(16, 'Make the website more accessible.'),
                     S(16, 'Add in a navigation bar with links'),
                     S(16, 'Place search bar in more prominent place on the site.')], 3, 2,
                    head=P(18, 'Suggest three improvements to the design of this website.'),
                    note=S(16, 'Any three of the above or similar 2 marks each'))]),
    dict(key=(15, 'd', None), topic='cs-1-2', total=6,
         replaces='batch 1b: no answer rows (an empty card); Figure 10 sat on the answer side',
         why='p20: three ways to make websites and apps accessible; the scheme lists nine, 2 each',
         ask=P(20, 'Accessibility features are vitally important', 'users with different needs.'),
         rows=[anyn([S(16, 'Use plain English'), S(16, 'Use large fonts, buttons'), S(16, 'Use good colour combinations'),
                     S(16, 'Embedded use of screen reader'), S(16, 'Closed captions on videos'),
                     S(16, 'Allow keyboard navigation'), S(16, 'Don’t clutter the website with links'),
                     S(16, 'Use heading correctly and organise the content.'), S(16, 'National Language Support.')], 3, 2,
                    head=P(20, 'Describe three ways by which designers', 'users with different needs.'),
                    note=S(16, 'Any three of the above or similar 2 marks each', nth=2))]),
    # ── Section C ──────────────────────────────────────────────────────────
    # Q16(a)(i)-(vii): shipped as one card for the whole of Section C; seven parts on their own
    # scales cannot sit on one card (the deck's six-row cap), so each part is carded and the
    # whole id withdrawn onto (a)(i) (WITHDRAWN below; coordinator, 5 Nov).
    dict(key=(16, 'a', 'i'), topic='cs-2-2', qfigure='q16-code0', figure='s-q16', total=5,
         printed=S(18, '(i) 5 marks (A-5 scale)'),
         why='040 p5: a comment where the first name is entered; the scheme marks it on the A-5 '
             'scale (0, 2, 3, 5), its possible solution (lines 1-27) the figure',
         stem=Q16_STEM, ask=C(5, 'Insert a comment in an appropriate place to say “user enters first name”.'),
         rows=[crit(S(18, CORRECT), 5, [2, 3],
                    note=S(18, '(i) 5 marks (A-5 scale)', 'Any reasonable attempt at inserting a comment.'))]),
    dict(key=(16, 'a', 'ii'), topic='cs-2-2', qfigure='q16-code0', figure='s-q16', total=10,
         printed=S(18, '(ii) 10 marks (A-10 scale)'),
         why='040 p5: read and store the surname; A-10 scale (0, 3, 7, 10)',
         stem=Q16_STEM, ask=C(5, 'Amend the program to ask for and accept the user\'s surname.', 'What is your surname? Murphy', end_nth=1),
         rows=[crit(S(18, 'Correct implementation using solution above or similar (using input only or print and input commands).'),
                    10, [3, 7], note=S(18, '(ii) 10 marks (A-10 scale)', 'take in the users surname.'))]),
    dict(key=(16, 'a', 'iii'), topic='cs-2-2', qfigure='q16-code0', figure='s-q16', total=5,
         printed=S(18, '(iii) 5 marks (A-5 scale)'),
         why='040 p5: print first name and surname; A-5 scale',
         stem=Q16_STEM, ask=C(5, 'Amend the program so that the user’s first name and their surname are printed', 'Please select from the list of items.'),
         rows=[crit(S(18, CORRECT, nth=2), 5, [2, 3],
                    note=S(18, '(iii) 5 marks (A-5 scale)', 'limited knowledge of print statements.'))]),
    dict(key=(16, 'a', 'iv'), topic='cs-2-2', qfigure='q16-code0', figure='s-q16', total=5,
         printed=S(18, '(iv) 5 marks (A-5 scale)'),
         why='040 p5: add Ruler and Pen to the list; A-5 scale',
         stem=Q16_STEM, ask=C(5, 'Amend the program so that the items 2 = Ruler', '1 = Book 2 = Ruler 3 = Pen', end_nth=1),
         rows=[crit(S(18, CORRECT, nth=3), 5, [2, 3],
                    note=S(18, '(iv) 5 marks (A-5 scale)', 'to the appropriate place.'))]),
    dict(key=(16, 'a', 'v'), topic='cs-2-2', qfigure='q16-code0', figure='s-q16', total=5,
         printed=S(19, '(v) 5 marks (A-5 scale)'),
         why='040 p5: dashed lines above and below the items; A-5 scale',
         stem=Q16_STEM, ask=C(5, 'Amend the program so that a dashed line appears', '3 = Pen ----------------------'),
         rows=[crit(S(19, CORRECT), 5, [2, 3],
                    note=S(19, '(v) 5 marks (A-5 scale)', 'dividers to the list.'))]),
    dict(key=(16, 'a', 'vi'), topic='cs-2-2', qfigure='q16-code0', figure='s-q16', total=10,
         printed=S(19, '(vi) 10 marks (A-10 scale)'),
         why='040 p6: the message for a ruler or a pen; A-10 scale',
         stem=Q16_STEM, ask=C(6, 'Amend the program so that the correct message is printed', 'You bought a ruler'),
         rows=[crit(S(19, CORRECT, nth=2), 10, [3, 7],
                    note=S(19, '(vi) 10 marks (A-10 scale)', 'to complete the task', end_nth=2))]),
    dict(key=(16, 'a', 'vii'), topic='cs-2-2', qfigure='q16-code0', figure='s-q16', total=10,
         printed=S(19, '(vii) 10 marks (A-10 scale)'),
         why='040 p6: an error message for any other number; A-10 scale',
         stem=Q16_STEM, ask=C(6, 'Amend the program to deal with invalid number entries.', 'Invalid choice. Goodbye.'),
         rows=[crit(S(19, CORRECT, nth=3), 10, [3, 7],
                    note=S(19, '(vii) 10 marks (A-10 scale)', 'or equivalent to error check.'))]),
]
