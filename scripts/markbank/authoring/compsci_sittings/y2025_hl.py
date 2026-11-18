"""Computer Science 2025 Higher Level: all 51 printed asks, re-authored part by part.

36 cards shipped in August out of the automatic author; batch 1b rebuilds each
of them here, keeping its id, from lifts of the paper and the scheme, and the
15 residue cards (the asks the August cards missed) sit among them in printed
order. Paper pages 3-20 and Section C pages 4-9, and scheme pages 3-27 were
opened.

Shipped crops reused on the question side, each opened and complete: q1-code0
(the 12-line Question 1 program), q14-code0 (gcd), q15-fig0 (Figure 5's
dataset) and q16-code0 (the 27-line Question16_A.py). q7-fig0 drops the two
captions that say which tree is Algorithm 1 and which Algorithm 2, so Q7 has a
crop of its own; q9-code0 carries a sliver of the prose above the listing, so
Q9 uses the lane's q9-code.

Q5's scheme prints the green and blue conversions in Cambria Math, which this
text layer reads as Malayalam operators and digits that lose their exponents;
the row is the scheme's "Answer: RGB(10, 51, 240)", one part per colour priced
2 / 1, and the scheme's workings are the solution crop. Q14(c)(iv)'s O(n log n)
and O(n squared) are printed the same way with parentheses no font maps, so
each row lifts the scheme's explanation around the formula and the scheme's
text is the solution crop.

A menu priced on a good/fair ladder is a ladder() row (coordinator, 5 Nov); a
line among the answers that is not an answer ("Any other valid ...") is its
instruction. Q10's two-column table (examples beside limitations) is read from
the cells block of scheme page 8, Q16(b)'s rubric from the cells of page 27.
"""
from compsci_lane import (C, G, GAt, P, S, T, anyn, crit, crop, ladder, pt, stack)  # noqa: F401

CROPS = {
    'q3-table': crop('038', 4, (88, 359, 507, 474), ref='2025 HL Q3',
                     alt='The table printed with Question 3: Ranking 1 to 4 down the left, with '
                         'columns Girl\'s Name and Project theme. Row 1\'s theme is filled in as '
                         'Artificial intelligence and row 3\'s name as Grace; every other cell '
                         'is blank.'),
    's-q5': crop('scheme', 5, (80, 524, 330, 609), ref='2025 HL Q5', solution=True,
                  alt='The marking scheme\'s conversions for Question 5: Red: 0A in hex = 10 in '
                      'decimal; Green: 33 in hex = 3 x 16 to the power 1 + 3 x 16 to the power 0 '
                      '= 51; Blue: F0 in hex = 15 x 16 to the power 1 + 0 x 16 to the power 0 = '
                      '240; Answer: RGB(10, 51, 240).'),
    'q7-figs': crop('038', 6, (70, 122, 506, 306), ref='2025 HL Q7',
                    alt='The two decision trees printed with Question 7. Figure 1: Algorithm 1 '
                        '(tree depth = 5) asks 1?, 2?, 3?, 4? and 5? in turn, each Yes leading '
                        'to that number and each No to the next question, the last No to 6. '
                        'Figure 2: Algorithm 2 (tree depth = 3) asks >=4? first; No leads to 3? '
                        '(Yes 3, No to 2?, which gives 2 or 1) and Yes to 6? (Yes 6, No to 5?, '
                        'which gives 5 or 4).'),
    'q9-code': crop('038', 7, (52, 147, 542, 275), ref='2025 HL Q9',
                    alt='The nine-line Python program printed with Question 9: For i in '
                        'range(1, 21):, then if i % 3 == 0: print("Fizz", elif i % 5 == 0: '
                        'print(Buzz"), elif i % 3 == 0 and i % 5 == 0: print("FizzBuzz"), '
                        'else (no colon) and print(number).'),
    'q13-fig3': stack([('038', 9, (383, 117, 558, 250)), ('038', 9, (440, 253, 515, 271))],
                      ref='2025 HL Q13(a)',
                      alt='Figure 3: a photograph of a Re-turn reverse vending machine. A hand '
                          'feeds a can into its round opening; a screen on the left reads '
                          'Ireland\'s Deposit Return Scheme, Starting 1 February, and a panel on '
                          'the right lists what to return.'),
    'q14a-trace': stack([('038', 13, (55, 184, 541, 331)), ('038', 13, (205, 469, 390, 606))],
                        ref='2025 HL Q14(a)(ii)',
                        alt='The ten-line program gcd printed with Question 14(a): def gcd(a, b):, '
                            'while a != b:, if a > b: a = a - b, elif b > a: b = b - a, return a, '
                            'then print("The GCD is", gcd(45,18)). Below it, the trace table with '
                            'columns a and b: its first row reads 45 18 and the three rows under '
                            'it are blank.'),
    's-q14a-ii': crop('scheme', 14, (205, 246, 390, 381), ref='2025 HL Q14(a)(ii)', solution=True,
                      alt='The marking scheme\'s completed trace table for Question 14(a)(ii), '
                          'columns a and b: 45 18, then 27 18, 9 18 and 9 9.'),
    'q14b-code': crop('038', 14, (52, 76, 542, 165), ref='2025 HL Q14(b)',
                      alt='The six-line recursive program printed with Question 14(b): def '
                          'recursive_gcd(a, b):, if b == 0: return a, return recursive_gcd(b, '
                          'a%b), then print("The GCD is", recursive_gcd(45, 18)).'),
    'q14-both': stack([('038', 13, (55, 184, 541, 331)), ('038', 14, (52, 76, 542, 165))],
                      ref='2025 HL Q14(b)(iii)',
                      alt='The two programs Question 14(b)(iii) compares: gcd from part (a), a '
                          'while loop that subtracts the smaller of a and b from the larger until '
                          'they are equal, then returns a; and recursive_gcd from part (b), which '
                          'returns a if b == 0 and otherwise returns recursive_gcd(b, a%b). Each '
                          'ends by printing The GCD is for 45 and 18.'),
    'q14c-list': crop('038', 15, (188, 170, 407, 214), ref='2025 HL Q14(c)(i)',
                      alt='The unsorted list printed with Question 14(c)(i), in five boxes: 29, '
                          '10, 14, 37, 13.'),
    'q14c-fig4': crop('038', 16, (165, 93, 430, 304), ref='2025 HL Q14(c)(iv)',
                      alt='Figure 4, printed with Question 14(c)(iv): a graph of Time against '
                          'Number of values (n) with two curves, O(n2) (n squared) rising '
                          'steeply from the origin and O(n log(n)) rising gently.'),
    's-q14c-iv': crop('scheme', 17, (55, 286, 545, 492), ref='2025 HL Q14(c)(iv)', solution=True,
                      alt='The marking scheme\'s answer to Question 14(c)(iv). Best case: the '
                          'best-case time complexity of quicksort is O(n log n), because each '
                          'pivot divides the list evenly into two halves, giving a balanced '
                          'recursion tree about log n levels deep with all n elements processed '
                          'at each level, n x log n in total. Worst case: O(n squared), when the '
                          'pivot repeatedly creates very unbalanced splits, giving n levels of n '
                          'elements, n x n = O(n squared), especially on already sorted or '
                          'reverse-sorted lists.'),
    's-q16a-i': crop('scheme', 22, (57, 469, 540, 507), ref='2025 HL Q16(a)(i)', solution=True,
                     alt='Lines 29 to 31 of the marking scheme\'s possible solution: '
                         'arithmetic_mean = total/N (marked part ii), then arithmetic_mean = '
                         'round(arithmetic_mean, 2), marked part i.'),
    's-q16a-ii': crop('scheme', 22, (57, 469, 540, 494), ref='2025 HL Q16(a)(ii)', solution=True,
                      alt='Lines 29 and 30 of the marking scheme\'s possible solution: # Divide by '
                          'the total number of results to give the mean, then arithmetic_mean = '
                          'total/N # part ii.'),
    's-q16a-iii': crop('scheme', 22, (57, 271, 540, 339), ref='2025 HL Q16(a)(iii)', solution=True,
                       alt='Lines 11 to 16 of the marking scheme\'s possible solution, between # '
                           'part iii - start and # part iii - end: elif result >= 50: grade = '
                           '"Lower Merit", elif result >= 40: grade = "Pass".'),
    's-q16a-iv': crop('scheme', 22, (57, 537, 540, 584), ref='2025 HL Q16(a)(iv)', solution=True,
                      alt='Lines 35 to 38 of the marking scheme\'s possible solution, between # '
                          'part (iv) - start and # part (iv) - end: grade = '
                          'get_grade(arithmetic_mean), then print("The grade for the average '
                          'result is", grade).'),
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
    's-q16a-vii': crop('scheme', 23, (57, 122, 540, 326), ref='2025 HL Q16(a)(vii)', solution=True,
                       alt='Lines 59 to 76 of the marking scheme\'s possible solution, part (vii): '
                           'longest_run = [] and current_run = [results[0]]; for i in range(1, N), '
                           'if results[i] > results[i - 1] the result is appended to current_run, '
                           'else, if current_run is longer than longest_run it becomes '
                           'longest_run, and current_run restarts as [results[i]]; after the loop '
                           'the same length check runs once more, then print("Longest run of '
                           'result increases is", longest_run).'),
    'q16b-output': crop('040', 9, (78, 70, 518, 333), ref='2025 HL Q16(b)',
                        alt='The three sample outputs printed with Question 16(b). Sample output '
                            '1: The initial list of values is: [27, 13, 32, 50, 16], The sorted '
                            'list of values is: [13, 16, 27, 32, 50], The median is 27. Sample '
                            'output 2: the list [27, 13, 32, 50, 16, 29], sorted [13, 16, 27, 29, '
                            '32, 50], The median is 28.0. Sample output 3: The initial list of '
                            'values is: [], The list is empty. Cannot compute the median.'),
    's-q16b': crop('scheme', 26, (57, 100, 540, 423), ref='2025 HL Q16(b)', solution=True,
                   alt='The marking scheme\'s 28-line possible solution for Question 16(b): nums = '
                       '[27, 13, 32, 50, 16] is printed, sorted with nums.sort() and printed '
                       'again; N = len(nums); if N == 0 the message The list is empty. Cannot '
                       'compute the median. is printed, else the median is nums[N//2] when N % 2 '
                       '!= 0 and (nums[N//2-1] + nums[N//2])/2 otherwise, and print("The median '
                       'is", median).'),
}

Q7_STEM = P(6, 'A binary question is a question', 'Two different search algorithms are illustrated.')
Q9_STEM = P(7, 'The intention of the Python code below is to scan', 'not divisible by 3 display the word Buzz.')
DRS = P(9, 'The Deposit Return Scheme (DRS) was introduced', 'lifecycle of drink containers.')
Q13B = [DRS, P(10, 'You have identified store staff and customers', 'stakeholders in the system.')]
Q13C = [DRS, P(11, 'You are keen to adopt a user-centred approach', 'inclusive user experience for all users.')]
Q14A = P(13, 'The Greatest Common Divisor (GCD) of two integers', 'GCD of 45 and 18.')
Q14B = P(14, 'The code below shows a recursive implementation', 'GCD of two integers.')
Q14C = P(15, 'Quicksort is a widely used sorting algorithm', 'very long lists of data.')
Q15_STEM = P(17, 'Modelling and simulation are essential tools', 'can influence outcomes.')
Q15A = [Q15_STEM, P(17, 'Consider the dataset shown in Figure 5 below', 'model driving test outcomes.')]
Q15B = [Q15_STEM, P(18, 'The quote below is attributed to statistician George Box', 'but some are useful"')]
Q15C = [Q15_STEM, P(19, 'A health agency wants to predict how an infectious disease', 'containment strategies.')]
Q16A_STEM = C(5, 'Line 15 of the program initialises a list', 'The mean percentage mark is 61.77777777777778')
CORRECT = S(24, 'Correct implementation using solution above or similar.')

CARDS = [
    # ── Section A ──────────────────────────────────────────────────────────
    dict(key=(1, None, None), topic='cs-2-2', qfigure='q1-code0', total=6,
         replaces='batch 1b: the program was the answer figure and the one row read "Output"; '
                  'now the six printed values, 1 mark each',
         why='p3: the output of a 12-line program; the scheme prints six values, each correct '
             'response in order 1 mark (all on one line 4, any two in sequence 2)',
         ask=P(3, 'State the output of the following Python code.'),
         rows=[pt(S(4, '5', nth=2), 1, note=S(4, 'Each correct response in order 1 mark',
                                             'Any two correct values in the proper sequence 2 marks')),
               pt(S(4, '10'), 1), pt(S(4, '20'), 1), pt(S(4, '2', nth=2), 1), pt(S(4, '1', nth=3), 1),
               pt(S(4, 'False'), 1)]),
    dict(key=(2, None, None), topic='cs-2-3', total=6,
         replaces='batch 1b: the one row was the heading "Memory Usage" worth 6; now each '
                  'heading\'s answer, 3 / 2',
         why='p3: compare ASCII and Unicode under two headings; the scheme answers each, 3 / 2',
         ask=P(3, 'ASCII and Unicode are both examples', 'memory usage and compatibility.'),
         rows=[crit(S(4, 'ASCII is a fixed width encoding system', 'mathematical symbols, emojis etc.).'), 3, [2],
                    head=S(4, 'Memory Usage'),
                    note=S(4, 'For each feature:', 'Fair explanation - limited understanding 2 mark')),
               crit(S(4, 'Unicode was designed to be backward compatible', 'communicate seamlessly with one another.'),
                    3, [2], head=S(4, 'Compatibility'))]),
    dict(key=(3, None, None), topic='cs-1-1', qfigure='q3-table', total=6,
         why='p4: a logic puzzle from five clues; the scheme prints the completed table, each '
             'correct response 1 mark (row 1\'s name, row 2\'s name and theme, row 3\'s theme, '
             'row 4\'s name and theme)',
         ask=P(4, 'Four girls recently competed in a coding hackathon', 'roughwork if you need it.'),
         rows=[pt(S(5, '1 Kay Artificial intelligence'), 1, note=S(5, 'Each correct response 1 mark')),
               crit(S(5, '2 Ada Web development'), 2, [1]),
               pt(S(5, '3 Grace Data analytics'), 1),
               crit(S(5, '4 Joy Embedded system'), 2, [1])]),
    dict(key=(4, None, None), topic='cs-2-3', total=6,
         replaces='batch 1b: the two answers were points with no fair step; now 3 / 2 each',
         why='p4: what resource and file management mean; the scheme answers each, 3 / 2',
         ask=P(4, 'Two key functions of an operating system', 'and ‘file management’.'),
         rows=[crit(S(5, 'Resource Management refers to how the operating system', 'and input/output devices.'),
                    3, [2], note=S(5, 'For each function:', 'Fair explanation - limited understanding 2 mark')),
               crit(S(5, 'File management refers to how the operating system', 'accessed or modified when needed.'),
                    3, [2])]),
    dict(key=(5, None, None), topic='cs-2-3', figure='s-q5', total=6,
         replaces='batch 1b: one row "Red: 0A in hex = 10 in decimal" worth 6; now the answer '
                  'with each colour\'s conversion priced 2 / 1 and the scheme\'s workings shown',
         why='p5: convert #0A33F0 to RGB; the scheme answers RGB(10, 51, 240), each conversion '
             '2 / 1; its green and blue workings are Cambria Math the text layer garbles, so they '
             'are the solution crop',
         ask=P(5, 'In web design, colours are often represented', 'to its RGB decimal values.'),
         rows=[crit(S(5, 'Answer: RGB(10, 51, 240)'), 6, [],
                    parts=[(P(5, 'Red:'), 2, [1]), (P(5, 'Green:'), 2, [1]), (P(5, 'Blue:'), 2, [1])],
                    note=S(5, 'For each conversion:', 'Response with some merit 1 mark'))]),
    dict(key=(6, None, None), topic='cs-1-2', total=6,
         replaces='batch 1b: one benefit was the only row, worth 6; now a benefit and a '
                  'limitation, each any one of the scheme\'s list at 3 / 2',
         why='p5: one benefit and one limitation of AI in diagnosis; the scheme lists five of '
             'each and any other valid, each part 3 / 2',
         ask=[P(5, 'Referring to the quote below from Professor Timothy Miller', 'area of medical diagnosis.'),
              P(5, 'Will a computer take your job?', 'age of artificial intelligence.')],
         rows=[ladder([S(6, 'Improved accuracy.', 'more accurate diagnoses.'),
                       S(6, 'Faster diagnosis.', 'reach a diagnosis.'),
                       S(6, 'Early detection.', 'successful treatment.'),
                       S(6, 'Reduced workload for doctors.', 'complex or urgent cases.'),
                       S(6, 'Availability. AI systems can be available', 'limited access to specialists.')],
                      [[2, 3]], head=P(5, 'Benefit:'), instruction=S(6, 'Any other valid benefit described.'),
                      note=S(6, 'For each part:', 'Fair description – limited understanding 2 mark')),
               ladder([S(6, 'Lack of human judgement.', 'well-rounded clinical decisions.'),
                       S(6, 'Possible lack of accuracy.', 'to make a correct diagnosis.'),
                       S(6, 'Ethical concerns regarding patient privacy', 'reduce trust and accountability.'),
                       S(6, 'High costs.', 'technical infrastructure and expertise.')],
                      [[2, 3]], head=S(6, 'Limitations'), instruction=S(6, 'Any other valid limitation described.'),
                      note=S(6, 'For each part:', 'Fair description – limited understanding 2 mark'))]),
    dict(key=(7, 'a', None), topic='cs-2-2', qfigure='q7-figs', total=2,
         replaces='batch 1b: the trees were the answer figure without their captions; now the '
                  'question figure with Figure 1 and Figure 2 named; topic Algorithms',
         why='p6: name the search algorithm of each tree; the scheme answers linear and binary, '
             '1 each; filed under Algorithms (2.2), not Computer systems: the two are search '
             'algorithms',
         stem=Q7_STEM, ask=P(6, 'State the name of each search algorithm.'),
         rows=[pt(S(7, 'Algorithm 1: Linear search'), 1, note=S(7, 'Each correct response: 1 mark')),
               pt(S(7, 'Algorithm 2: Binary search'), 1)]),
    dict(key=(7, 'b', None), topic='cs-2-2', qfigure='q7-figs', total=4,
         replaces='batch 1b: the scheme\'s two alternative answers were two 2-mark points; now '
                  'either one, 4 / 2; topic Algorithms',
         why='p6: which algorithm is more efficient and why; the scheme prints two answers '
             'joined by OR, 4 / 2; filed under Algorithms (2.2)',
         stem=Q7_STEM, ask=P(6, 'Suggest which of the two algorithms is most efficient. Justify your answer.'),
         rows=[ladder([S(7, 'Linear search may be more efficient as there is no sort overhead.',
                         'more efficient than a binary search.'),
                       S(7, 'In general, binary search is more efficient', 'requires O(n) operations.')], [[2, 4]],
                      note=S(7, 'Very good justification - clear understanding demonstrated 4 marks',
                             'Fair justification – limited understanding 2 mark'))]),
    dict(key=(8, None, None), topic='cs-2-3', total=6,
         why='p6: IP against VoIP; the scheme defines both, 6 / 4 / 2, and 1 each for the '
             'protocol names alone',
         ask=P(6, 'Distinguish between the IP and VoIP communication protocols.'),
         rows=[crit(S(7, 'Internet Protocol (IP) is the general protocol', '(e.g. Zoom and WhatsApp).'),
                    6, [1, 2, 4],
                    note=S(7, 'Very good distinction - clear understanding demonstrated 6 marks',
                           'Award 1 mark each for correct protocol name only.'))]),
    dict(key=(9, 'a', None), topic='cs-2-2', qfigure='q9-code', total=2,
         replaces='batch 1b: the one row was the heading "Any two syntax errors from the '
                  'following:"; now the five errors, any two at 1; the clean listing crop',
         why='p7: two syntax errors; the scheme lists five, each syntax error 1 mark',
         stem=Q9_STEM, ask=P(7, 'There are a number of syntax errors in the code. Identify any two of these errors.'),
         rows=[anyn([S(8, 'Line 1. Incorrect case - For instead of for'), S(8, 'Line 3. Missing closing bracket'),
                     S(8, 'Line 5. Missing opening quote'), S(8, 'Line 8. Missing colon after else'),
                     S(8, 'Line 9. Variable number is undefined')], 2, 1,
                    head=S(8, 'Any two syntax errors from the following:'),
                    note=S(8, 'Each syntax error 1 mark'))]),
    dict(key=(9, 'b', None), topic='cs-2-5', qfigure='q9-code', total=4,
         why='p7: the logic error and its fix; the scheme prints both, 2 marks each',
         stem=Q9_STEM,
         ask=P(7, 'Identify the logic error in the code and suggest a solution.'),
         rows=[pt(S(8, 'Logic error: The program never displays FizzBuzz', 'i is 15.'), 2,
                  note=S(8, 'Logic error correctly identified 2 marks', 'Suggested solution 2 mark')),
               pt(S(8, 'Suggested solution: Move the test', 'before the individual tests).'), 2)]),
    dict(key=(10, None, None), topic='cs-1-2', total=6,
         replaces='batch 1b: the one row was the table\'s header "Examples Limitations"; now two '
                  'examples at 2 and one limitation at 2, read from the table\'s cells',
         why='p7: two examples of automation and one limitation; the scheme tables nine examples '
             'beside seven limitations (cells of scheme p8), each example 2, the limitation 2',
         ask=P(7, 'List two examples of how computing technology', 'limitation of either example.'),
         rows=[anyn([T(8, 'Customer support chatbots'), T(8, 'Online shopping recommendations'),
                     T(8, 'Self-driving cars'), T(8, 'Medical diagnosis (or monitoring)'),
                     T(8, 'Smart home systems'), T(8, 'Banking transactions (e.g. payments)'),
                     T(8, 'Payroll systems'), T(8, 'School/college administration systems')], 2, 2,
                    head=T(8, 'Any two from the following:'), note=S(8, 'For each example 2 marks'),
                    instruction=T(8, 'Any other valid example')),
               anyn([T(8, 'High development/maintenance cost'), T(8, 'Job displacement'),
                     T(8, 'Errors in data can lead to mistakes in outcomes.'),
                     T(8, 'Security (vulnerable to cyberattacks)'),
                     T(8, 'Ethical concerns (e.g. privacy, fairness, accountability)'),
                     T(8, 'Limited human understanding'), T(8, 'Any other valid limitation')], 1, 2, open_list=True,
                    head=T(8, 'Limitations'),
                    note=S(8, 'Limitation: Very good explanation - clear understanding demonstrated 2 marks'))]),
    dict(key=(11, None, None), topic='cs-1-2', total=6,
         replaces='batch 1b: the one row was the heading "Advantage" worth 6; now an advantage '
                  'and a risk, each any one of the scheme\'s list at 3 / 2',
         why='p8: one advantage and one risk of personalised content in elections; the scheme '
             'lists four advantages and three risks and any other valid, each 3 / 2',
         ask=P(8, 'Social media platforms often use data from users', 'context of political elections.'),
         rows=[ladder([S(9, 'Voters receive content relevant to their interests.'),
                       S(9, 'Helps voters make informed decisions.'),
                       S(9, 'Encourages greater engagement potentially leading to higher turnouts.'),
                       S(9, 'Political parties can focus their resources', 'saving time and money.')],
                      [[2, 3]], head=S(9, 'Advantage'), instruction=S(9, 'Any other valid advantage.'),
                      note=S(9, 'For each advantage/disadvantage', 'Fair explanation – limited understanding 2 marks')),
               ladder([S(9, 'Users may only see content that agrees with their views', '(echo chambers/filter bubbles).'),
                       S(9, 'Algorithms may spread false or misleading information', "to a user's preferences."),
                       S(9, 'Privacy concerns.')],
                      [[2, 3]], head=S(9, 'Potential Risks'), instruction=S(9, 'Any other valid potential risk.'),
                      note=S(9, 'For each advantage/disadvantage', 'Fair explanation – limited understanding 2 marks'))]),
    dict(key=(12, None, None), topic='cs-2-3', total=6,
         why='p8: two CPU components and their purposes; the scheme lists six, each named 1 '
             'and its purpose 2 / 1',
         ask=P(8, 'The Central Processing Unit (CPU) is often referred to', 'purpose of two CPU components.'),
         rows=[ladder([S(9, 'Arithmetic Logic Unit (ALU):', 'necessary for processing instructions.'),
                       S(9, 'Control Unit (CU):', 'work together efficiently.'),
                       S(9, 'Registers:', 'addresses during processing.'),
                       S(9, 'Cache:', 'improve processing speed.'),
                       S(9, 'Program Counter (PC):', 'in the correct sequence.'),
                       S(9, 'Clock:', 'the CPU processes data.')], [[1, 2, 3], [1, 2, 3]],
                      note=S(9, 'For each correctly identified CPU component 1 mark',
                             'Fair explanation – limited understanding 1 mark'))]),
    # ── Section B ──────────────────────────────────────────────────────────
    dict(key=(13, 'a', 'i'), topic='cs-1-3', qfigure='q13-fig3', total=6,
         why='p9: two team roles with two responsibilities each; the scheme lists seven roles, '
             'each role 1 and each responsibility 1',
         stem=DRS,
         ask=P(9, 'As project manager one of your first responsibilities', 'assign to each role.'),
         rows=[ladder([S(10, 'System architect:', 'promotes technologies.'),
                       S(10, 'Analyst:', 'develops system use cases.'),
                       S(10, 'Designer:', 'produces design documents'),
                       S(10, 'Software developer:', 'unit testing, debugging.'),
                       S(10, 'Software tester:', 'status/progress.'),
                       S(10, 'UI/UX Designer:', 'for the application.'),
                       S(10, 'IT Support Technician:', 'users of the system.')], [[1, 2, 3], [1, 2, 3]],
                      instruction=S(10, 'Any other valid role and associated responsibilities.'),
                      note=S(10, 'For each role correctly identified 1 mark', 'understanding demonstrated 1 mark'))]),
    dict(key=(13, 'a', 'ii'), topic='cs-1-3', qfigure='q13-fig3', total=2,
         why='p10: two software development processes; the scheme lists them, 1 each',
         stem=DRS,
         ask=P(10, 'Once you have the project team in place', 'processes available to you.'),
         rows=[anyn([S(10, 'Waterfall/Staged.'), S(10, 'Agile/Iterative.'),
                     S(10, 'Any valid software development process/methodology.')], 2, 1,
                    head=S(10, 'Any two from the following:'), open_list=True,
                    note=S(10, 'For each correct response 1 mark'))]),
    dict(key=(13, 'a', 'iii'), topic='cs-1-3', qfigure='q13-fig3', total=4,
         why='p10: choose a process and justify it with two features; the scheme answers both '
             'options, each feature 2 / 1, one option only',
         stem=DRS,
         ask=P(10, 'Choose the software development process that should be used', 'methodology you chose.'),
         rows=[ladder([S(11, 'Highly structured, follows a sequence of phases', 'deployment and maintenance.'),
                       S(11, 'Each phase must be completed before moving', 'predictable process.'),
                       S(11, 'Comprehensive documentation such as', 'test cases.'),
                       S(11, 'Suitable for large projects when requirements', 'unlikely to change.')],
                      [[1, 2], [1, 2]], head=S(11, 'Option 1: Waterfall/Staged'), route='Option 1: Waterfall/Staged',
                      note=S(11, 'For each feature:', 'limited understanding 1 mark')),
               ladder([S(11, 'Less structured/more flexible', 'called sprints.'),
                       S(11, 'Functional components are delivered incrementally.'),
                       S(11, 'Customer collaboration throughout the project lifecycle.'),
                       S(11, 'Very responsive to dynamic/changing requirements.')],
                      [[1, 2], [1, 2]], head=S(11, 'Option 2: Agile/Iterative'), route='Option 2: Agile/Iterative',
                      note=S(11, 'For each feature:', 'limited understanding 1 mark'))]),
    dict(key=(13, 'b', 'i'), topic='cs-1-3', qfigure='q13-fig3', total=4,
         replaces='batch 1b: the stem was another part\'s ask and the one row was the heading '
                  '"Store Staff" worth 4; now each stakeholder\'s goal and benefit at 1; topic '
                  'Designing and developing',
         why='p10: a goal and a benefit for store staff and for customers; the scheme answers '
             'each, 1 mark; filed under Designing and developing (1.21, stakeholders), not '
             'Computer systems',
         stem=Q13B,
         ask=P(10, 'For each stakeholder outline one goal they may want from the system',
               'should gain from the system.'),
         rows=[pt(S(11, 'Goal: To have a system that quickly registers', 'System should result in less waste.'), 1,
                  head=S(11, 'Store Staff'),
                  note=S(11, 'For each goal Very good explanation',
                         'For each benefit Very good explanation - clear understanding demonstrated 1 mark')),
               pt(S(11, 'Benefit To provide fast service to customers and reduce workload.'), 1,
                  head=S(11, 'Store Staff')),
               pt(S(11, 'Goal to be able to scan returned bottles and receive an immediate refund.'), 1,
                  head=S(11, 'Customer', nth=2)),
               pt(S(11, 'Benefit is receipt of refund and contribution to cleaner environment.'), 1,
                  head=S(11, 'Customer', nth=2))]),
    dict(key=(13, 'b', 'ii'), topic='cs-1-3', qfigure='q13-fig3', total=1,
         replaces='batch 1b: the stem was another part\'s ask and the one row was "Any from the '
                  'following:"; now the six stakeholders, any one at 1',
         why='p10: one other stakeholder; the scheme lists six and any other valid, 1 mark',
         stem=Q13B, ask=P(10, 'State the name of one other stakeholder of the system once it goes live.'),
         rows=[anyn([S(12, 'Store manager'), S(12, 'Government regulator'), S(12, 'Administrator'),
                     S(12, 'Maintenance technician'), S(12, 'Logistics manager'), S(12, 'Environmental analyst'),
                     S(12, 'Any other valid stakeholder')], 1, 1, open_list=True,
                    head=S(12, 'Any from the following:'), note=S(12, 'Valid stakeholder identified 1 mark'))]),
    dict(key=(13, 'b', 'iii'), topic='cs-2-4', qfigure='q13-fig3', total=4,
         replaces='batch 1b: the stem was this part\'s second sentence, the ask its first, and '
                  'the menu four 1-mark points; now any two use cases at 2 / 1',
         why='p11: two use cases of database management; the scheme lists three and any other '
             'valid, each 2 / 1',
         stem=Q13B, ask=P(11, 'You have identified database management', 'use cases of this component.'),
         rows=[ladder([S(12, 'Machine Details: This database would store machine details', 'status etc.'),
                       S(12, 'Container Tracking: This database system could use unique identifiers',
                         'reuse status for each container.'),
                       S(12, 'Finance Management: This database could be used to store deposit amounts',
                         'transaction and financial reports.')], [[1, 2], [1, 2]],
                      instruction=S(12, 'Any other valid database management use case.'),
                      note=S(12, 'For each use case suggested:', 'Fair explanation – limited understanding 1 mark'))]),
    dict(key=(13, 'b', 'iv'), topic='cs-1-2', qfigure='q13-fig3', total=6,
         why='p11: two uses of AI in the DRS application; the scheme lists five and any valid, '
             'each 3 / 2',
         stem=Q13B,
         ask=P(11, 'Suggest two ways artificial intelligence (AI) technology', 'DRS application.'),
         rows=[ladder([S(12, 'Automated image recognition for bottle scanning.'),
                       S(12, 'Demand prediction for collection logistics.'),
                       S(12, 'Predictive maintenance for return machines.'),
                       S(12, 'Personalised incentives to engage users.'),
                       S(12, 'Data analysis (e.g. for environmental impact reporting).')], [[2, 3], [2, 3]],
                      instruction=S(12, 'Any other valid way AI could be used', 'e.g. chatbot feature.'),
                      note=S(12, 'For each suggestion', 'limited understanding 2 marks'))]),
    dict(key=(13, 'c', 'i'), topic='cs-1-2', qfigure='q13-fig3', total=6,
         replaces='batch 1b: the stem held the ask and the one row was the screen reader alone, '
                  'worth 6; now any two technologies, named 1 and explained 2 / 1; topic '
                  'Computers and society',
         why='p11: two assistive technologies for a visually impaired user; the scheme lists '
             'four and any other valid, each identified 1 and explained 2 / 1; filed under '
             'Computers and society (1.15, user experience and universal design), not Computer '
             'systems',
         stem=Q13C,
         ask=P(11, 'Read the following scenario and answer the question that follows.',
               'enhance accessibility for this user.'),
         rows=[ladder([S(13, 'Screen Reader: A screen reader can help', 'participate in the deposit return scheme.'),
                       S(13, 'Voice Recognition Software: This technology', 'use a keyboard or mouse.'),
                       S(13, 'Braille Display: For users who are blind', 'container details in Braille.'),
                       S(13, 'Simplified User Interface: A simplified interface', 'DRS system more easily.')],
                      [[1, 2, 3], [1, 2, 3]],
                      instruction=S(13, 'Any other valid assistive technology for a visually impaired user.'),
                      note=S(13, 'For each assistive technology correctly identified 1 mark',
                             'Fair explanation – limited understanding 1 mark'))]),
    dict(key=(13, 'c', 'ii'), topic='cs-2-5', qfigure='q13-fig3', total=5,
         replaces='batch 1b: the stem was another part\'s scenario and the row was unit testing '
                  'alone, all or nothing; now both definitions at 5 / 3 / 1; topic Evaluation '
                  'and testing',
         why='p12: unit testing against functional testing; the scheme defines both, 5 / 3 / 1; '
             'filed under Evaluation and testing (2.22), not Computer systems',
         stem=Q13C,
         ask=P(12, 'The system will need to be thoroughly tested', 'between unit testing and functional testing.'),
         rows=[crit(S(13, 'Unit Testing: Focuses on testing individual components', 'later in the development process.'),
                    5, [1, 3],
                    note=S(13, 'Very good distinction - clear understanding demonstrated 5 marks',
                           'Fair distinction – limited understanding 1 mark'))]),
    dict(key=(14, 'a', 'i'), topic='cs-2-2', qfigure='q14-code0', total=2,
         replaces='batch 1b: the stem was the trace table\'s furniture ("a b 45 18 This question '
                  'continues...") and the program was the answer figure; now the question\'s '
                  'stem and the listing beside the ask',
         why='p13: the purpose of def; the scheme answers it, 2',
         stem=Q14A, ask=P(13, 'State the purpose of the def keyword on line 1 of the code.'),
         rows=[pt(S(14, 'To introduce (define) the function gcd.'), 2)]),
    dict(key=(14, 'a', 'ii'), topic='cs-2-2', qfigure='q14a-trace', figure='s-q14a-ii', total=4,
         replaces='batch 1b: the one row was the table header "a b"; now the scheme\'s three '
                  'rows, 1 a row and 4 for the full response, with its completed table',
         why='p13: complete the trace table from 45 18; the scheme prints 27 18, 9 18, 9 9, '
             'each correct row 1 and the full correct response 4',
         stem=Q14A, ask=P(13, 'Starting from line 2 of the code, complete the trace table', 'to 45 and 18 respectively.'),
         rows=[crit(S(14, '27 18 9 18 9 9'), 4, [1, 2, 3],
                    note=S(14, 'For each correct row 1 mark', 'Full correct response 4 marks'))]),
    dict(key=(14, 'a', 'iii'), topic='cs-2-2', qfigure='q14-code0', total=4,
         why='p13: why a for loop would not suit; the scheme prints two reasons, either at 4 / 2',
         stem=Q14A,
         ask=P(13, 'This implementation uses a while loop.', 'not be suitable for this algorithm.'),
         rows=[ladder([S(14, 'The number of iterations is not known in advance', 'running the algorithm.'),
                       S(14, 'The number of iterations required can vary', 'into the function gcd.')], [[2, 4]],
                      note=S(14, 'Very good explanation - clear understanding demonstrated 4 marks',
                             'Fair explanation – limited understanding 2 marks'))]),
    dict(key=(14, 'b', 'i'), topic='cs-2-2', qfigure='q14b-code', total=4,
         replaces='batch 1b: the stem was the listing as text and the one row was the heading '
                  '"Base Case" worth 4; now each case\'s answer, 2 / 1',
         why='p14: base case and recursive case; the scheme answers each, 2 / 1',
         stem=Q14B,
         ask=P(14, 'Every recursive function, including the one shown here', '‘recursive case’.'),
         rows=[crit(S(15, 'the condition that stops the recursive function', 'the condition b == 0 is the base case.'),
                    2, [1], head=S(15, 'Base Case'),
                    note=S(15, 'For each case:', 'Fair explanation – limited understanding 1 mark')),
               crit(S(15, 'the part of the function that calls itself', 'recursive_gcd(b, a % b).'),
                    2, [1], head=S(15, 'Recursive Case'))]),
    dict(key=(14, 'b', 'ii'), topic='cs-2-2', qfigure='q14b-code', total=6,
         why='p14: the variable b and the expression a%b on line 4; the scheme answers each, '
             '3 / 2',
         stem=Q14B,
         ask=P(14, 'Explain the use of the variable b and the expression a%b on line 4 of the code.'),
         rows=[crit(S(15, 'This is the first argument (parameter/value)', 'whether the base case (b == 0) is reached).'),
                    3, [2], head=S(15, 'The variable b:'),
                    note=S(15, 'For each answer:', 'limited understanding 2 marks')),
               crit(S(15, 'This is the second argument (parameter/value)', 'the remainder of a % b).'),
                    3, [2], head=S(15, 'The expression a%b:'),
                    note=S(15, 'For each answer:', 'limited understanding 2 marks'))]),
    dict(key=(14, 'b', 'iii'), topic='cs-2-3', qfigure='q14-both', total=5,
         replaces='batch 1b: the one row was "gcd" worth 5; now the choice at 1 and the '
                  'scheme\'s justification at 4 / 2, with both listings shown',
         why='p14: gcd or recursive_gcd on limited RAM; the scheme answers gcd at 1 and '
             'justifies it, 4 / 2',
         stem=Q14B,
         ask=P(14, 'Given a choice of using gcd shown in part (a)', 'in terms of memory utilisation.'),
         rows=[pt(S(16, 'gcd'), 1, note=S(16, 'Correct response: 1 mark')),
               crit(S(16, 'The non-recursive solution is more suitable', 'leading to a stack overflow error.'),
                    4, [2], note=S(16, 'Very good explanation - clear understanding demonstrated 4 marks',
                                   'Fair explanation - limited understanding 2 marks'))]),
    dict(key=(14, 'c', 'i'), topic='cs-2-2', qfigure='q14c-list', total=2,
         replaces='batch 1b: the stem was page furniture and the answer figure the gcd program; '
                  'now the quicksort stem, the printed list, and each sub-list at 1',
         why='p15: the two sub-lists after one partition around 13; the scheme answers [10] and '
             '[29, 14, 37], 1 each',
         stem=Q14C, ask=P(15, 'Given the unsorted list shown below and a pivot of 13', 'one partitioning step of quicksort.'),
         rows=[pt(S(16, 'Left sub-list: [10]'), 1, note=S(16, 'For each correct sub-list 1 mark')),
               pt(S(16, 'Right sub-list: [29, 14, 37]'), 1)]),
    dict(key=(14, 'c', 'ii'), topic='cs-2-2', total=5,
         replaces='batch 1b: the stem was page furniture, the answer figure the gcd program and '
                  'the row all or nothing; now 5 / 3 / 1',
         why='p15: the next steps of quicksort; the scheme answers it (or an appropriate '
             'diagram), 5 / 3 / 1',
         stem=Q14C, ask=P(15, 'Describe the next steps quicksort would take in order to achieve its objective.'),
         rows=[crit(S(16, 'After the first pass, quicksort continues', 'Appropriate diagram.'), 5, [1, 3],
                    note=S(16, 'Very good explanation - clear understanding demonstrated 5 marks',
                           'Fair explanation - limited understanding 1 mark'))]),
    dict(key=(14, 'c', 'iii'), topic='cs-2-2', total=2,
         replaces='batch 1b: the one row was the heading "Pivot selection strategies" worth 2; '
                  'now the six strategies, any two at 1',
         why='p15: two pivot strategies; the scheme lists six, each correct strategy 1 mark',
         stem=Q14C, ask=P(15, 'Outline two common strategies used when selecting a pivot', 'quicksort algorithm.'),
         rows=[anyn([S(17, 'First element'), S(17, 'Last element'), S(17, 'Middle'),
                     S(17, 'Median of first, middle and last element'), S(17, 'Median of medians'),
                     S(17, 'Random')], 2, 1,
                    head=S(17, 'Pivot selection strategies'), note=S(17, 'For each correct strategy 1 mark'))]),
    dict(key=(14, 'c', 'iv'), topic='cs-2-2', qfigure='q14c-fig4', figure='s-q14c-iv', total=4,
         replaces='batch 1b: the answer figure was the gcd program and the one row the heading '
                  '"Best case:" worth 4; now Figure 4, each case at 2 / 1, and the scheme\'s '
                  'answer as printed',
         why='p16: best and worst-case complexity from Figure 4; the scheme answers each, 2 / 1; '
             'its O(n log n) and O(n squared) are set in a maths font whose brackets, operators '
             'and exponent the text layer cannot read, so each case is read by glyph id (scheme '
             'p17) and lifted whole',
         stem=Q14C, ask=P(16, 'Referring to Figure 4 below', 'quicksort algorithm.'),
         rows=[crit(G(17, 'The best-case time complexity of quicksort', 'all levels is n × log n.'), 2, [1],
                    head=S(17, 'Best case:'),
                    note=S(17, 'For each case (best and worst):', 'Fair explanation – limited understanding 1 mark')),
               crit(G(17, 'The worst-case time complexity of quicksort', 'if no precautions are taken.'),
                    2, [1], head=S(17, 'Worst case:'))]),
    dict(key=(15, 'a', 'i'), topic='cs-3-3', qfigure='q15-fig0', total=1,
         replaces='batch 1b: the stem was the dataset as text, the dataset the answer figure, '
                  'and the row "Output variable:"; now the model\'s stem, Figure 5 beside the '
                  'ask and TEST OUTCOME; topic Modelling and simulation',
         why='p17: the output variable; the scheme answers TEST OUTCOME, 1; filed under '
             'Modelling and simulation as (a)(ii) is, not Algorithms',
         stem=Q15A, ask=P(17, 'State the name of the output variable in the model.'),
         rows=[pt(S(18, 'TEST OUTCOME'), 1)]),
    dict(key=(15, 'a', 'ii'), topic='cs-3-3', qfigure='q15-fig0', total=2,
         why='p17: two input variables of the model; the scheme lists four, 1 each',
         stem=Q15A,
         ask=P(17, 'State the names of two input variables.'),
         rows=[anyn([S(18, 'GENDER'), S(18, 'AGE'), S(18, 'TRANSMISSION'), S(18, 'INSTRUCTOR EXPERIENCE (Years)')],
                    2, 1, head=S(18, 'Input variables: Any two from'),
                    note=S(18, 'For each correct response 1 mark', nth=1))]),
    dict(key=(15, 'a', 'iii'), topic='cs-3-3', qfigure='q15-fig0', total=4,
         replaces='batch 1b: the one row was "Any two from the following:" worth 4; now the '
                  'scheme\'s patterns, any two at 2; topic Modelling and simulation',
         why='p17: two patterns in the model; the scheme lists four and any other valid, 2 each',
         stem=Q15A, ask=P(17, 'Describe two patterns you can identify from the model.'),
         rows=[anyn([S(18, 'Younger drivers (under 20) tend to have higher failure rates.'),
                     S(18, 'Drivers using automatic cars tend to pass', 'higher failure rates.'),
                     S(18, 'More experienced instructors are correlated with higher pass rates.'),
                     S(18, 'The number of females who pass is the same as the number of males who fail.'),
                     S(18, 'Any other valid pattern.')], 2, 2, open_list=True,
                    head=S(18, 'Any two from the following:', nth=1),
                    note=S(18, 'For each pattern correctly identified 2 marks'))]),
    dict(key=(15, 'a', 'iv'), topic='cs-3-3', qfigure='q15-fig0', total=4,
         replaces='batch 1b: the one row was "Any two from the following:" worth 4; now the '
                  'scheme\'s variables, any two at 2; topic Modelling and simulation',
         why='p18: two more variables for the model; the scheme lists five and any other valid, '
             '2 each',
         stem=Q15A, ask=P(18, 'Identify two additional variables', 'driving test outcome model.'),
         rows=[anyn([S(18, 'Number of lessons.'), S(18, 'Number of previous attempts.'),
                     S(18, 'Driving test time of day.'), S(18, 'Weather conditions.'),
                     S(18, 'Familiarity with car.'), S(18, 'Any other valid variable.')], 2, 2, open_list=True,
                    head=S(18, 'Any two from the following:', nth=2),
                    note=S(18, 'Each variable correctly identified 2 marks'))]),
    dict(key=(15, 'b', 'i'), topic='cs-3-3', total=4,
         replaces='batch 1b: the dataset was the answer figure and the one row the heading '
                  '"Limitations" worth 4; now a limitation and a benefit, each any one at 2 / 1; '
                  'topic Modelling and simulation',
         why='p18: one limitation and one benefit of modelling; the scheme lists five and three '
             'and any other valid, each part 2 / 1',
         stem=Q15B, ask=P(18, 'Outline one limitation and one benefit of modelling and simulation.'),
         rows=[ladder([S(19, 'Models are abstractions that simplify complex systems.', 'full complexity of reality.'),
                       S(19, 'Underlying assumptions of model may not always hold true.'),
                       S(19, 'Data limitations (e.g. bias, errors, size) can make models inaccurate.'),
                       S(19, 'Ethical concerns regarding privacy, security and accountability.'),
                       S(19, 'High development costs.')], [[1, 2]],
                      head=S(19, 'Limitations'), instruction=S(19, 'Any other valid limitation.'),
                      note=S(19, 'For each part:', 'Fair description – limited understanding 1 mark')),
               ladder([S(19, 'Models make complex systems easier to understand', 'areas for intervention.'),
                       S(19, 'Models can provide valuable predictions within a defined scope.'),
                       S(19, 'Models help decision-makers weigh options', 'more efficient road systems.')], [[1, 2]],
                      head=S(19, 'Benefits'), instruction=S(19, 'Any other valid benefit.'),
                      note=S(19, 'For each part:', 'Fair description – limited understanding 1 mark'))]),
    dict(key=(15, 'b', 'ii'), topic='cs-2-1', total=4,
         replaces='batch 1b: the dataset was the answer figure and the row all or nothing; now '
                  '4 / 2; topic Abstraction',
         why='p18: why abstraction matters in a model; the scheme answers it, 4 / 2; filed under '
             'Abstraction (2.1), not Algorithms',
         stem=Q15B, ask=P(18, 'Explain why abstraction is important when developing a model.'),
         rows=[crit(S(19, 'Abstraction is important when developing a model because', 'testing different scenarios.'),
                    4, [2], note=S(19, 'Very good explanation - clear understanding demonstrated 4 marks',
                                   'Fair explanation – limited understanding 2 marks'))]),
    dict(key=(15, 'b', 'iii'), topic='cs-3-3', total=8,
         replaces='batch 1b: the dataset was the answer figure and the four areas four fixed '
                  '2-mark points; now any two areas at 4 / 2; topic Modelling and simulation',
         why='p19: how modelling helps in two of four areas; the scheme answers each area, 4 / 2; '
             'filed under Modelling and simulation, not Computational thinking',
         stem=Q15_STEM,
         ask=P(19, 'Modelling and simulation can be used in many situations', 'address a problem and improve outcomes.'),
         rows=[ladder([S(20, 'Education: Modelling can be used to simulate', 'to optimise teaching strategies.'),
                       S(20, 'Mental Wellbeing: Modelling mental wellbeing', 'improving mental health management.'),
                       S(20, 'Environment: Environmental models simulate natural systems', 'sustainable resource management.'),
                       S(20, 'Traffic Management: Traffic flow simulations', 'overall transportation systems.')],
                      [[2, 4], [2, 4]],
                      note=S(20, 'For each area:', 'Fair description – limited understanding 2 marks'))]),
    dict(key=(15, 'c', 'i'), topic='cs-3-3', total=3,
         why='p19: agent-based modelling of disease spread in a school; the scheme answers it, '
             '3 / 2',
         stem=Q15C,
         ask=P(19, 'Describe how agent-based modelling could be used', 'disease spread in this scenario.'),
         rows=[crit(S(20, 'Each student and teacher could be modelled as an agent', 'mask-wearing etc).'),
                    3, [2], note=S(20, 'Very good description - clear understanding demonstrated 3 marks',
                                   'Fair description – limited understanding 2 marks'))]),
    dict(key=(15, 'c', 'ii'), topic='cs-3-3', total=2,
         replaces='batch 1b: the stem was page furniture, the dataset the answer figure and the '
                  'row "Any one from the following:"; now any one behaviour at 2 / 1',
         why='p20: one emergent behaviour; the scheme lists four and any other valid, 2 / 1',
         stem=Q15C, ask=P(20, 'Outline one emergent behaviour that could be revealed by this simulation.'),
         rows=[ladder([S(21, 'Clusters of infection forming in areas with high interaction, like hallways.'),
                       S(21, 'Clusters of infection associated with specific activity', 'musical etc.'),
                       S(21, 'Patterns showing higher infection rates among specific people', '(superspreaders).'),
                       S(21, 'Recovery can lead to patterns such as slowing transmission rates',
                         'eventual end of an outbreak.')], [[1, 2]],
                      instruction=S(21, 'Any other valid emergent behaviour.'),
                      note=S(21, 'Very good description - clear understanding demonstrated 2 marks',
                             'Fair description – limited understanding 1 mark'))]),
    dict(key=(15, 'c', 'iii'), topic='cs-3-3', total=6,
         replaces='batch 1b: the stem was page furniture, the dataset the answer figure and the '
                  'row the heading "Strategies" worth 6; now a strategy at 2 and how to measure '
                  'its success at 4 / 2',
         why='p20: a strategy and how to measure it; the scheme lists six strategies and any '
             'other valid at 2, and two measures at 4 / 2',
         stem=Q15C,
         ask=P(20, 'Suggest one strategy the health agency could test', 'how you would measure its success.'),
         rows=[anyn([S(21, 'Measures to reduce crowding e.g. social distancing', 'quarantine.'),
                     S(21, 'Mask wearing.'), S(21, 'Vaccination/booster campaigns.'),
                     S(21, 'Regular testing / contact tracing.'), S(21, 'Increased hygiene.'),
                     S(21, 'Enhanced air ventilation systems.'), S(21, 'Any other valid strategy.')], 1, 2,
                    open_list=True, head=S(21, 'Strategies - any one from the following:'),
                    note=S(21, 'Correct strategy identified 2 marks')),
               ladder([S(21, 'Compare infection rates before and after the strategy.'),
                       S(21, 'Analyse the time it takes for the disease to stop spreading.')], [[2, 4]],
                      head=S(21, 'Measure success:'),
                      note=S(21, 'For each response:', 'Fair explanation – limited understanding 2 marks'))]),
    # ── Section C ──────────────────────────────────────────────────────────
    dict(key=(16, 'a', 'i'), topic='cs-2-2', qfigure='q16-code0', figure='s-q16a-i', total=5,
         why='040 p5: round the mean to two decimal places; the scheme marks line 31 part i, '
             'B-5 scale',
         stem=Q16A_STEM,
         ask=C(5, 'Round the mean percentage to two decimal places.', 'The mean percentage mark is 61.78', end_nth=1),
         rows=[crit(CORRECT, 5, [3], note=S(24, '(i) 5 marks (B-5 scale)', 'Any other reasonable attempt.'))]),
    dict(key=(16, 'a', 'ii'), topic='cs-2-2', qfigure='q16-code0', figure='s-q16a-ii', total=5,
         replaces='batch 1b: filed as section B with the copy-the-file instructions as its stem '
                  'and "Any other reasonable attempt." as its row; now section C, the B-5 scale '
                  'and the scheme\'s line 30',
         why='040 p5: divide by the length of results; the scheme marks line 30 part ii, B-5 scale',
         stem=Q16A_STEM,
         ask=C(5, 'Currently, the code divides the total by 9', 'The mean percentage mark is 61.78', end_nth=1),
         rows=[crit(CORRECT, 5, [3], note=S(24, '(ii) 5 marks (B-5 scale)', 'Any other reasonable attempt.'))]),
    dict(key=(16, 'a', 'iii'), topic='cs-2-2', qfigure='q16-code0', figure='s-q16a-iii', total=5,
         replaces='batch 1b: filed as section B with "semantic error." as its row; now section '
                  'C, the C-5 scale and the scheme\'s lines 11-16',
         why='040 p5: complete get_grade from the table; the scheme marks lines 11-16 part iii, '
             'C-5 scale',
         stem=Q16A_STEM,
         ask=C(5, 'Complete the function get_grade', 'The mean percentage mark is 61.78', end_nth=1),
         rows=[crit(CORRECT, 5, [2, 3], note=S(24, '(iii) 5 marks (C-5 scale)', 'Any other reasonable attempt.'))]),
    dict(key=(16, 'a', 'iv'), topic='cs-2-2', qfigure='q16-code0', figure='s-q16a-iv', total=5,
         replaces='batch 1b: filed as section B with five 1-mark rows of furniture ("Leaving '
                  'Certificate 2025", "Marking Scheme"); now section C, the C-5 scale and the '
                  'scheme\'s lines 35-38',
         why='040 p6: call get_grade and display the grade; the scheme marks lines 35-38 part '
             '(iv), C-5 scale',
         stem=Q16A_STEM,
         ask=C(6, 'Extend the program so that it calls the function get_grade', 'is Lower Merit', end_nth=1),
         rows=[crit(CORRECT, 5, [2, 3], note=S(24, '(iv) 5 marks (C-5 scale)', 'Any other reasonable attempt.'))]),
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
    dict(key=(16, 'a', 'vii'), topic='cs-2-2', qfigure='q16-code0', figure='s-q16a-vii', total=15,
         replaces='batch 1b: filed as section B with "15 marks Correct response" as its row; '
                  'now section C, the D-15 scale and the scheme\'s lines 59-76',
         why='040 p7: the longest run of increases; the scheme marks lines 59-76 part (vii), '
             'D-15 scale',
         stem=Q16A_STEM,
         ask=C(7, 'Extend the program so that it determines and displays the longest run',
               'is [51, 62, 64, 81]'),
         rows=[crit(CORRECT, 15, [3, 7, 10], note=S(25, '(vii) 15 marks (D-15 scale)', 'Any other reasonable attempt.'))]),
    dict(key=(16, 'b', None), topic='cs-2-2', qfigure='q16b-output', figure='s-q16b', total=30,
         replaces='batch 1b: filed as section B, its ask was "Open the program..." and its row '
                  '"Possible solution:" worth 30; now section C, the median task, the sample '
                  'outputs, and the rubric\'s four criteria at their printed levels',
         why='040 p8-9: write a median program; the scheme prints a possible solution and a '
             'rubric of four criteria at high / moderate / low (cells of scheme p27): inputs 5 / '
             '4 / 3, logic 10 / 7 / 5, outputs 5 / 4 / 3, standards 10 / 7 / 5',
         stem=C(8, 'The median of a list of values is the middle value', 'then dividing the result by two.'),
         ask=GAt('040', 8, (80, 322, 560, 655), breaks=True),
         rows=[crit(T(27, 'Initial list of integers correctly initialised', 'use of assignment statements'),
                    5, [3, 4], head=T(27, 'Inputs'),
                    note=[T(27, 'High level of achievement All of the following', 'correctly and efficiently'),
                          T(27, 'Moderate level of achievement Reasonable attempt', 'each of the following'),
                          T(27, 'Low level of achievement Poor attempt to complete any of the following')]),
               crit(T(27, 'Length of list calculated', 'Logic to test empty list'), 10, [5, 7],
                    head=T(27, 'Program Logic (Processing)')),
               crit(T(27, 'Initial list of integers displayed', 'Error message displayed'), 5, [3, 4],
                    head=T(27, 'Program Outputs')),
               crit(T(27, 'Program executes correctly with no syntax or runtime errors', 'Meaningful variable/function names'),
                    10, [5, 7], head=T(27, 'Programming Standards'))]),
]
