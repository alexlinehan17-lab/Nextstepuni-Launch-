"""Computer Science 2022 Ordinary Level: the 16 printed asks the bank did not hold.

27 of the sitting's 43 asks are covered by the cards shipped in August; these
16 complete it. Paper pages 3, 6, 8-12, 15 and 17 and scheme pages 4, 6-15
were opened. This is the 2022 paper's own format: Section A six of twelve at
5 marks, Section B one long question of 30. Where the scheme prices a part
only in the question head ("3+2 marks"), that head is quoted.

Q13(b)(i)'s scheme lists its four answers as a bare list (True, False, True,
True), paired with the paper's four statements by printed order; both print
four. Its statements carry Wingdings glyphs (a tick, a smiling face), folded
after rendering. Q12's answers are a lone 7 and a lone 1, read from the
scheme page by position.
"""
from compsci_lane import (At, P, Pair, S, anyn, crit, crop, pt, stack)  # noqa: F401

FIG8 = ('038', 10, (54, 130, 551, 296))

CROPS = {
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

CARDS = [
    dict(key=(2, None, None), topic='cs-3-3', qfigure='q2-fig1', total=5,
         why='p3: two reasons a computer model helps; the scheme lists five, first 3 / 1 and '
             'second 2 / 1',
         ask=P(3, 'The traffic at a busy road junction', 'useful in this situation.'),
         rows=[anyn([S(4, 'Identifying traffic patterns.'), S(4, 'Help improve traffic flow at the junction.'),
                     S(4, 'Change traffic light times at different times of the day.'),
                     S(4, 'Get information on different modes of transportation being used.'),
                     S(4, 'Save people time, stop delays')], 2, 3, steps=[3, 2],
                    head=S(4, 'Any two of the above or similar:'), note=Q2_NOTE, open_list=True)]),
    dict(key=(6, 'a', None), topic='cs-2-2', figure='q6-flow', total=3, printed=S(6, 'Question 6 3+2 marks'),
         labels={'A': S(6, 'Guess < Number (Less than)')},
         why='p6: the missing text of the symbol labelled A; the scheme prints two forms, 3 / 1',
         stem=Q6_STEM,
         ask=P(6, 'What text is missing from the symbol labelled A?'),
         rows=[anyn([S(6, 'Guess < Number (Less than)'), S(6, 'Number greater than Guess (Greater than)')], 1, 3,
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
         rows=[anyn([S(8, 'Have a drop down menu so only numbers can be picked.'), S(8, 'Have a keypad with numbers 1 – 10'),
                     S(8, 'Have an error message if the user enters an invalid score')], 1, 2,
                    head=S(8, 'Any one of the above or similar:', nth=1),
                    note=S(8, 'Good explanation – clear improvement described 2 marks', 'not described 1 mark'))]),
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
    dict(key=(13, 'c', 'ii'), topic='cs-2-3', total=5,
         why='p13: two differences between SSDs and HDDs; the scheme lists five, best 3 / 1 and '
             'second 2 / 1',
         ask=P(13, 'The use of Solid State Drives', 'two differences'),
         rows=[anyn([S(11, 'Solid State drives can operate faster than Hard disk drives.'),
                     S(11, 'Solid state drives are lighter than the Hard disk drive.'),
                     S(11, 'Solid State Drives is smaller in size (takes up less space)'),
                     S(11, 'Hard Disk Drives are cheaper than Solid State Drives'),
                     S(11, 'Solid State drive doesn’t produce noise', 'can create some noise.')], 2, 3, steps=[3, 2],
                    head=S(11, 'Best response marked out of 3 and second best response marked out of 2 as follows:'),
                    note=S(11, 'Best response marked out of 3', 'limited understanding of difference 1 Mark'))]),
    dict(key=(14, 'b', 'i'), topic='cs-2-4', qfigure='q14b-table', total=8,
         why='p15: four further rows of variable name, description and data type; the scheme '
             'lists examples, each fully correct row 2 and partially correct 1',
         stem=[Q14_STEM, P(15, 'You will need to get data from the school office', 'in order to create the program.')],
         ask=P(15, 'Complete the table below with four items of data', 'The first row has been completed for you.'),
         rows=[anyn([S(13, 'Last Name (String)'), S(13, 'Year group (Int)'), S(13, 'Sibling in 6th Year (Boolean)'),
                     S(13, 'Permission slip signed (Boolean)'), S(13, 'Parents Name (String)'),
                     S(13, 'Number of Siblings (int)'), S(13, 'Any other valid piece of data relevant to the problem')],
                    4, 2, open_list=True, head=S(13, 'Any variable created regarding the above with appropriate variable name:'),
                    note=S(13, 'Each fully correct row 2 marks Each partially correct row 1 mark'))]),
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
]
