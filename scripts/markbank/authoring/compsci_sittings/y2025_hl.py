"""Computer Science 2025 Higher Level: the 15 printed asks the bank did not hold.

36 cards shipped in August cover 36 of the sitting's 51 asks and are left as
they are; these 15 complete it. Paper pages 4, 7-11, 13-14, 17, 19 and Section
C pages 4-6, and scheme pages 5, 7-13, 14-15, 18, 20 and 22-25 were opened.

Shipped crops reused on the question side: q15-fig0 (Figure 5's dataset) and
q16-code0 (the 27-line Question16_A.py), both opened and complete. The shipped
q9-code0 carries a sliver of the prose above the listing, so Q9(b) has a crop
of its own; Q14(b) needs the recursive listing, which no shipped crop holds.
"""
from compsci_lane import (C, P, S, anyn, crit, crop, pt, stack)  # noqa: F401

CROPS = {
    'q3-table': crop('038', 4, (88, 359, 507, 474), ref='2025 HL Q3',
                     alt='The table printed with Question 3: Ranking 1 to 4 down the left, with '
                         'columns Girl\'s Name and Project theme. Row 1\'s theme is filled in as '
                         'Artificial intelligence and row 3\'s name as Grace; every other cell '
                         'is blank.'),
    'q13-fig3': stack([('038', 9, (383, 117, 558, 250)), ('038', 9, (440, 253, 515, 271))],
                      ref='2025 HL Q13(a)',
                      alt='Figure 3: a photograph of a Re-turn reverse vending machine. A hand '
                          'feeds a can into its round opening; a screen on the left reads '
                          'Ireland\'s Deposit Return Scheme, Starting 1 February, and a panel on '
                          'the right lists what to return.'),
    'q9-code': crop('038', 7, (52, 147, 542, 275), ref='2025 HL Q9',
                    alt='The nine-line Python program printed with Question 9: For i in '
                        'range(1, 21):, then if i % 3 == 0: print("Fizz", elif i % 5 == 0: '
                        'print(Buzz"), elif i % 3 == 0 and i % 5 == 0: print("FizzBuzz"), '
                        'else (no colon) and print(number).'),
    'q14b-code': crop('038', 14, (52, 76, 542, 165), ref='2025 HL Q14(b)',
                      alt='The six-line recursive program printed with Question 14(b): def '
                          'recursive_gcd(a, b):, if b == 0: return a, return recursive_gcd(b, '
                          'a%b), then print("The GCD is", recursive_gcd(45, 18)).'),
    's-q16a-i': crop('scheme', 22, (57, 469, 540, 507), ref='2025 HL Q16(a)(i)', solution=True,
                     alt='Lines 29 to 31 of the marking scheme\'s possible solution: '
                         'arithmetic_mean = total/N (marked part ii), then arithmetic_mean = '
                         'round(arithmetic_mean, 2), marked part i.'),
    's-q16a-v': crop('scheme', 22, (57, 592, 540, 671), ref='2025 HL Q16(a)(v)', solution=True,
                     alt='Lines 40 to 45 of the marking scheme\'s possible solution: highest = '
                         'max(results), lowest = min(results), then print("The lowest score '
                         'is", lowest) and print("The highest score is", highest).'),
    's-q16a-vi': stack([('scheme', 22, (57, 671, 540, 740)), ('scheme', 23, (57, 55, 540, 113))],
                       ref='2025 HL Q16(a)(vi)', solution=True,
                       alt='Lines 47 to 57 of the marking scheme\'s possible solution: a = 0 and '
                           'b = 0, then a for loop over results adding 1 to a when result < 40 '
                           'and to b when result >= 50 and result <= 79, then the two counts '
                           'printed in their messages.'),
}

Q16A_STEM = C(5, 'Line 15 of the program initialises a list', 'The mean percentage mark is 61.77777777777778')
CORRECT = S(24, 'Correct implementation using solution above or similar.')

CARDS = [
    dict(key=(3, None, None), topic='cs-1-1', qfigure='q3-table', total=6,
         why='p4: a logic puzzle from five clues; the scheme prints the completed table, each '
             'correct response 1 mark (row 1\'s name, row 2\'s name and theme, row 3\'s theme, '
             'row 4\'s name and theme)',
         ask=P(4, 'Four girls recently competed in a coding hackathon', 'roughwork if you need it.'),
         rows=[pt(S(5, '1 Kay Artificial intelligence'), 1, note=S(5, 'Each correct response 1 mark')),
               crit(S(5, '2 Ada Web development'), 2, [1]),
               pt(S(5, '3 Grace Data analytics'), 1),
               crit(S(5, '4 Joy Embedded system'), 2, [1])]),
    dict(key=(8, None, None), topic='cs-2-3', total=6,
         why='p6: IP against VoIP; the scheme defines both, 6 / 4 / 2, and 1 each for the '
             'protocol names alone',
         ask=P(6, 'Distinguish between the IP and VoIP communication protocols.'),
         rows=[crit(S(7, 'Internet Protocol (IP) is the general protocol', '(e.g. Zoom and WhatsApp).'),
                    6, [1, 2, 4],
                    note=S(7, 'Very good distinction - clear understanding demonstrated 6 marks',
                           'Award 1 mark each for correct protocol name only.'))]),
    dict(key=(9, 'b', None), topic='cs-2-5', qfigure='q9-code', total=4,
         why='p7: the logic error and its fix; the scheme prints both, 2 marks each',
         stem=P(7, 'The intention of the Python code below is to scan', 'not divisible by 3 display the word Buzz.'),
         ask=P(7, 'Identify the logic error in the code and suggest a solution.'),
         rows=[pt(S(8, 'Logic error: The program never displays FizzBuzz', 'i is 15.'), 2,
                  note=S(8, 'Logic error correctly identified 2 marks', 'Suggested solution 2 mark')),
               pt(S(8, 'Suggested solution: Move the test', 'before the individual tests).'), 2)]),
    dict(key=(12, None, None), topic='cs-2-3', total=6,
         why='p8: two CPU components and their purposes; the scheme lists six, each named 1 '
             'and its purpose 2 / 1',
         ask=P(8, 'The Central Processing Unit (CPU) is often referred to', 'purpose of two CPU components.'),
         rows=[anyn([S(9, 'Arithmetic Logic Unit (ALU):', 'necessary for processing instructions.'),
                     S(9, 'Control Unit (CU):', 'work together efficiently.'),
                     S(9, 'Registers:', 'addresses during processing.'),
                     S(9, 'Cache:', 'improve processing speed.'),
                     S(9, 'Program Counter (PC):', 'in the correct sequence.'),
                     S(9, 'Clock:', 'the CPU processes data.')], 2, 3,
                    head=P(8, 'Identify and state the purpose of two CPU components.'),
                    note=S(9, 'For each correctly identified CPU component 1 mark',
                           'Fair explanation – limited understanding 1 mark'))]),
    dict(key=(13, 'a', 'i'), topic='cs-1-3', qfigure='q13-fig3', total=6,
         why='p9: two team roles with two responsibilities each; the scheme lists seven roles, '
             'each role 1 and each responsibility 1',
         stem=P(9, 'The Deposit Return Scheme (DRS) was introduced', 'lifecycle of drink containers.'),
         ask=P(9, 'As project manager one of your first responsibilities', 'assign to each role.'),
         rows=[anyn([S(10, 'System architect:', 'promotes technologies.'),
                     S(10, 'Analyst:', 'develops system use cases.'),
                     S(10, 'Designer:', 'produces design documents'),
                     S(10, 'Software developer:', 'unit testing, debugging.'),
                     S(10, 'Software tester:', 'status/progress.'),
                     S(10, 'UI/UX Designer:', 'for the application.'),
                     S(10, 'IT Support Technician:', 'users of the system.'),
                     S(10, 'Any other valid role and associated responsibilities.')], 2, 3, open_list=True,
                    head=S(10, 'Roles and Responsibilities:'),
                    note=S(10, 'For each role correctly identified 1 mark', 'understanding demonstrated 1 mark'))]),
    dict(key=(13, 'a', 'ii'), topic='cs-1-3', qfigure='q13-fig3', total=2,
         why='p10: two software development processes; the scheme lists them, 1 each',
         stem=P(9, 'The Deposit Return Scheme (DRS) was introduced', 'lifecycle of drink containers.'),
         ask=P(10, 'Once you have the project team in place', 'processes available to you.'),
         rows=[anyn([S(10, 'Waterfall/Staged.'), S(10, 'Agile/Iterative.'),
                     S(10, 'Any valid software development process/methodology.')], 2, 1,
                    head=S(10, 'Any two from the following:'), open_list=True,
                    note=S(10, 'For each correct response 1 mark'))]),
    dict(key=(13, 'a', 'iii'), topic='cs-1-3', qfigure='q13-fig3', total=4,
         why='p10: choose a process and justify it with two features; the scheme answers both '
             'options, each feature 2 / 1, one option only',
         stem=P(9, 'The Deposit Return Scheme (DRS) was introduced', 'lifecycle of drink containers.'),
         ask=P(10, 'Choose the software development process that should be used', 'methodology you chose.'),
         rows=[anyn([S(11, 'Highly structured, follows a sequence of phases', 'deployment and maintenance.'),
                     S(11, 'Each phase must be completed before moving', 'predictable process.'),
                     S(11, 'Comprehensive documentation such as', 'test cases.'),
                     S(11, 'Suitable for large projects when requirements', 'unlikely to change.')], 2, 2,
                    head=S(11, 'Option 1: Waterfall/Staged'), route='Option 1: Waterfall/Staged',
                    note=S(11, 'For each feature:', 'limited understanding 1 mark')),
               anyn([S(11, 'Less structured/more flexible', 'called sprints.'),
                     S(11, 'Functional components are delivered incrementally.'),
                     S(11, 'Customer collaboration throughout the project lifecycle.'),
                     S(11, 'Very responsive to dynamic/changing requirements.')], 2, 2,
                    head=S(11, 'Option 2: Agile/Iterative'), route='Option 2: Agile/Iterative',
                    note=S(11, 'For each feature:', 'limited understanding 1 mark'))]),
    dict(key=(13, 'b', 'iv'), topic='cs-1-2', total=6,
         why='p11: two uses of AI in the DRS application; the scheme lists five and any valid, '
             'each 3 / 2',
         stem=P(10, 'You have identified store staff and customers', 'stakeholders in the system.'),
         ask=P(11, 'Suggest two ways artificial intelligence (AI) technology', 'DRS application.'),
         rows=[anyn([S(12, 'Automated image recognition for bottle scanning.'),
                     S(12, 'Demand prediction for collection logistics.'),
                     S(12, 'Predictive maintenance for return machines.'),
                     S(12, 'Personalised incentives to engage users.'),
                     S(12, 'Data analysis (e.g. for environmental impact reporting).'),
                     S(12, 'Any other valid way AI could be used', 'e.g. chatbot feature.')], 2, 3,
                    head=S(12, 'Any two of the following:'), open_list=True,
                    note=S(12, 'For each suggestion', 'limited understanding 2 marks'))]),
    dict(key=(14, 'a', 'iii'), topic='cs-2-2', qfigure='q14-code0', total=4,
         why='p13: why a for loop would not suit; the scheme prints two reasons, 4 / 2',
         stem=P(13, 'The Greatest Common Divisor (GCD) of two integers', 'GCD of 45 and 18.'),
         ask=P(13, 'This implementation uses a while loop.', 'not be suitable for this algorithm.'),
         rows=[anyn([S(14, 'The number of iterations is not known in advance', 'running the algorithm.'),
                     S(14, 'The number of iterations required can vary', 'into the function gcd.')], 1, 4,
                    head=P(13, 'Explain why a for loop would not be suitable for this algorithm.'),
                    note=S(14, 'Very good explanation - clear understanding demonstrated 4 marks',
                           'Fair explanation – limited understanding 2 marks'))]),
    dict(key=(14, 'b', 'ii'), topic='cs-2-2', qfigure='q14b-code', total=6,
         why='p14: the variable b and the expression a%b on line 4; the scheme answers each, '
             '3 / 2',
         stem=P(14, 'The code below shows a recursive implementation', 'GCD of two integers.'),
         ask=P(14, 'Explain the use of the variable b and the expression a%b on line 4 of the code.'),
         rows=[crit(S(15, 'This is the first argument (parameter/value)', 'whether the base case (b == 0) is reached).'),
                    3, [2], head=S(15, 'The variable b:'),
                    note=S(15, 'For each answer:', 'limited understanding 2 marks')),
               crit(S(15, 'This is the second argument (parameter/value)', 'the remainder of a % b).'),
                    3, [2], head=S(15, 'The expression a%b:'),
                    note=S(15, 'For each answer:', 'limited understanding 2 marks'))]),
    dict(key=(15, 'a', 'ii'), topic='cs-3-3', qfigure='q15-fig0', total=2,
         why='p17: two input variables of the model; the scheme lists four, 1 each',
         stem=[P(17, 'Modelling and simulation are essential tools', 'can influence outcomes.'),
               P(17, 'Consider the dataset shown in Figure 5 below', 'model driving test outcomes.')],
         ask=P(17, 'State the names of two input variables.'),
         rows=[anyn([S(18, 'GENDER'), S(18, 'AGE'), S(18, 'TRANSMISSION'), S(18, 'INSTRUCTOR EXPERIENCE (Years)')],
                    2, 1, head=S(18, 'Input variables: Any two from'),
                    note=S(18, 'For each correct response 1 mark', nth=1))]),
    dict(key=(15, 'c', 'i'), topic='cs-3-3', total=3,
         why='p19: agent-based modelling of disease spread in a school; the scheme answers it, '
             '3 / 2',
         stem=P(19, 'A health agency wants to predict how an infectious disease', 'containment strategies.'),
         ask=P(19, 'Describe how agent-based modelling could be used', 'disease spread in this scenario.'),
         rows=[crit(S(20, 'Each student and teacher could be modelled as an agent', 'mask-wearing etc).'),
                    3, [2], note=S(20, 'Very good description - clear understanding demonstrated 3 marks',
                                   'Fair description – limited understanding 2 marks'))]),
    dict(key=(16, 'a', 'i'), topic='cs-2-2', qfigure='q16-code0', figure='s-q16a-i', total=5,
         why='040 p5: round the mean to two decimal places; the scheme marks line 31 part i, '
             'B-5 scale',
         stem=Q16A_STEM,
         ask=C(5, 'Round the mean percentage to two decimal places.', 'The mean percentage mark is 61.78', end_nth=1),
         rows=[crit(CORRECT, 5, [3], note=S(24, '(i) 5 marks (B-5 scale)', 'Any other reasonable attempt.'))]),
    dict(key=(16, 'a', 'v'), topic='cs-2-2', qfigure='q16-code0', figure='s-q16a-v', total=5,
         why='040 p6: the lowest and highest scores; the scheme marks lines 40-45 part (v), C-5 '
             'scale',
         stem=Q16A_STEM,
         ask=C(6, 'Add code so that the program finds the lowest and highest scores', 'The highest score is 88', end_nth=1),
         rows=[crit(CORRECT, 5, [2, 3], note=S(25, '(v) 5 marks (C-5 scale)', 'Any other reasonable attempt.'))]),
    dict(key=(16, 'a', 'vi'), topic='cs-2-2', qfigure='q16-code0', figure='s-q16a-vi', total=10,
         why='040 p6: count two ranges of scores; the scheme marks lines 47-57 part (vi), D-10 '
             'scale',
         stem=Q16A_STEM,
         ask=C(6, 'Add two features to count how many scores', 'between 50 and 79 inclusive is 5'),
         rows=[crit(CORRECT, 10, [3, 5, 7], note=S(25, '(vi) 10 marks (D-10 scale)', 'Any other reasonable attempt.'))]),
]
