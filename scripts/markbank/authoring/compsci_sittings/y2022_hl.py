"""Computer Science 2022 Higher Level: the 8 printed asks the bank did not hold.

47 of the sitting's 55 asks are covered by the cards shipped in August; these
8 complete it. Paper pages 6, 10, 14, 22-24 and Section C pages 4-6, and
scheme pages 3, 6, 9, 13, 19-21 were opened. Section C's A-5 scale is "0, 5"
in the scheme's own scale table (page 3), so (i) and (iv) are all or nothing.
The shipped q16-figure (the description and the 21-line listing) is reused,
opened and complete.
"""
from compsci_lane import (C, P, S, anyn, crit, crop, pt, stack)  # noqa: F401

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
    'q15-progs': stack([('038', 22, (53, 94, 542, 211)), ('038', 23, (53, 245, 542, 402))],
                       ref='2022 HL Q15(c)',
                       alt='The two check-digit programs printed with Question 15. Part (b): isbn '
                           'stored as the string "102004110"; a for loop over range(10, 1, -1) '
                           'adds int(isbn[10-i]) * i to total. Part (c): isbn stored as the integer '
                           '102004110 and copied to isbn1; a for loop over range(2, 11) takes '
                           'digit = isbn % 10, adds digit*i to total and sets isbn = isbn//10. '
                           'Both then compute check_digit = 11 - (total % 11) and print it.'),
    's-q11a': crop('scheme', 9, (52, 219, 537, 497), ref='2022 HL Q11(a)', solution=True,
                   alt='The marking scheme\'s completed honey bee ancestry tree for Question '
                       '11(a), extended to Generations 6 and 7 with every bee labelled male or '
                       'female.'),
    's-q16a-i': crop('scheme', 20, (57, 204, 545, 218), ref='2022 HL Q16(a)(i)', solution=True,
                     alt='Line 5 of the marking scheme\'s possible solution: print("Dice '
                         'simulation and analysis program"), marked part (i).'),
    's-q16a-iv': crop('scheme', 20, (57, 476, 545, 489), ref='2022 HL Q16(a)(iv)', solution=True,
                      alt='Line 31 of the marking scheme\'s possible solution: the print of the '
                          'results list commented out with a #, marked part (iv).'),
}

Q16A_STEM = C(4, 'The program simulates the rolling of a die 100 times.')

CARDS = [
    dict(key=(5, None, None), topic='cs-2-2', qfigure='q5-flow', total=5,
         why='p6: the flowchart\'s missing text at A-E; the scheme prints it, 1 each',
         ask=P(6, 'A chemical solution is said to be an acid', 'for the letters A-E.'),
         rows=[pt(S(6, 'A pH < 7'), 1, note=S(6, 'Each correct response 1 mark')),
               pt(S(6, 'B FALSE'), 1), pt(S(6, 'C TRUE'), 1),
               pt(S(6, 'D OUTPUT “Base”'), 1), pt(S(6, 'E OUTPUT “Neutral”'), 1)]),
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
    dict(key=(13, 'b', 'i'), topic='cs-3-1', total=4,
         why='p14: a wireframe of the shop page; the scheme prices four features, 1 each, and '
             'prints no drawing',
         stem=P(14, 'Some weeks after the initial meeting', 'a shop page and a checkout page.'),
         ask=P(14, 'The shop page should allow visitors to browse items.', 'outlining the purpose of the main elements.'),
         rows=[pt(S(13, 'Image and description of item'), 1), pt(S(13, 'Add to cart button'), 1),
               pt(S(13, 'Link to checkout page'), 1), pt(S(13, 'Overall aesthetic'), 1)]),
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
         rows=[anyn([S(19, 'letter/digit errors, such as l → 1 or O → 0'),
                     S(19, 'single digit errors, such as 1 → 2'),
                     S(19, 'transposition errors, such as 12 → 21'),
                     S(19, 'twin errors, such as 11 → 22'),
                     S(19, 'jump transpositions errors, such as 132 → 231'),
                     S(19, 'jump twin errors, such as 131 → 232')], 1, 2,
                    head=P(24, 'Provide an example of one type of data entry error', 'could be used to prevent.'),
                    note=S(19, 'Very good description - clear understanding demonstrated 2 marks',
                           'Fair description - limited understanding 1 mark', nth=2))]),
    dict(key=(16, 'a', 'i'), topic='cs-2-2', qfigure='q16-figure', figure='s-q16a-i', total=5,
         why='040 p5: change the first line of output; the scheme marks line 5 part (i), A-5 '
             'scale (0 or 5)',
         stem=Q16A_STEM,
         ask=C(5, 'Currently the first line in the program output is Dice simulation program.',
               'first line in the output is Dice simulation and analysis program.'),
         rows=[pt(S(21, 'Correct implementation using solution above or similar.'), 5,
                  note=S(21, '(i) 5 marks (A-5 scale)', 'using solution above or similar.'))]),
    dict(key=(16, 'a', 'iv'), topic='cs-2-2', qfigure='q16-figure', figure='s-q16a-iv', total=5,
         why='040 p6: comment out the results line; the scheme marks line 31 part (iv), A-5 '
             'scale (0 or 5)',
         stem=Q16A_STEM,
         ask=C(6, 'Comment out the line that displays the list of individual results.',
               'Frequencies: [17, 21, 17, 18, 11, 16]'),
         rows=[pt(S(21, 'Correct implementation using solution above or similar.', nth=4), 5,
                  note=S(21, '(iv) 5 marks (A-5 scale)', 'using solution above or similar.'))]),
]
