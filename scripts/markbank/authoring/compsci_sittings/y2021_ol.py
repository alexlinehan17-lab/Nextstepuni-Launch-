"""Computer Science 2021 Ordinary Level: every card of the sitting, lifted from the page.

The 25 cards shipped in August are re-authored here under their own ids (batch
1b), and the 4 the lane added for the asks they missed are kept. Paper pages
3-20 (Sections A and B) and Section C pages 3-4, and scheme pages 3-17 were
opened.

Q1's scheme table sets its two columns so that the flat text interleaves them
("a = 5 Integer String b = ..."); its cells are read with find_tables (cells
block, page 4). The census flags Q10(a) and (b) as empty leaves ("x = 21",
"x = 3"): each IS the ask, a value of x under the paper's shared question, and
is carded with it.

cs-2021-ol-q6 is shipped as the whole of Q6 (no part cards) and stays whole,
each row tied to its part with ofpart(). By the coordinator's ruling of 5 Nov
two whole-question cards are split and WITHDRAWN: cs-2021-ol-q15 (beside part
cards for (a), (b)(ii), (c) and (d)) gives way to a card for (b)(i), the one
ask only it covered; cs-2021-ol-q16 (the whole of Section C, seven parts, past
the deck's six-row cap) gives way to a card per part.

Q15(b)(i)'s answers, a 1 and a 0, are printed beside the scheme's gate
drawing and read from it by position.
"""
from compsci_lane import (At, C, P, Pair, S, T, anyn, crit, crop, ladder, ofpart, pt, stack)  # noqa: F401

WITHDRAWN = {'cs-2021-ol-q15': 'cs-2021-ol-q15-b-i', 'cs-2021-ol-q16': 'cs-2021-ol-q16-a-i'}

CROPS = {
    'q1-table': crop('038', 3, (70, 228, 525, 446), ref='2021 OL Q1',
                     alt='The table printed with Question 1: Column A lists the assignments a = 5, '
                         'b = "Hello World", c = True, d = ["apple", "banana", "orange"] and e = '
                         '2.718; Column B (Data Type) is blank.'),
    'q4-fig1': crop('038', 4, (304, 344, 520, 493), ref='2021 OL Q4',
                    alt='Figure 1: a photograph of a warehouse aisle between tall blue racks of '
                        'boxes, with a fleet of small orange robots carrying goods along the '
                        'floor.'),
    'q6-boxes': crop('038', 5, (80, 422, 445, 569), ref='2021 OL Q6(a)',
                     alt='The four choices printed with Question 6(a) under What is HTTP?, each '
                         'with an empty tick box: the language used to program web pages; the '
                         'method for encoding data securely; the web browser; the protocol for '
                         'transferring hypertext for webpages.'),
    'q5-fig2': crop('038', 5, (335, 62, 529, 182), ref='2021 OL Q5',
                    alt='Figure 2: a laptop, a phone and a desktop computer labelled Clients, '
                        'joined through a cloud labelled Internet to a machine labelled Server.'),
    'q7-fig3': crop('038', 6, (120, 62, 504, 153), ref='2021 OL Q7',
                    alt='Figure 3: a smooth wave labelled Analogue input beside a square wave '
                        'labelled Digital input.'),
    'q9-code': stack([('038', 7, (52, 118, 542, 222)), ('038', 7, (159, 245, 465, 424)),
                      ('038', 7, (52, 447, 542, 494))],
                     ref='2021 OL Q9',
                     alt='The seven-line Python program printed with Question 9 (a = 1, b = 2, '
                         'while a < 4: a = a + 1, b = b + a, then print(b)), above the trace table '
                         'with columns Step, a, b and a < 4; step 1 is filled in as 1, 2, True and '
                         'steps 2 to 4 and the Output box below it are blank.'),
    'q10-algo': crop('038', 8, (53, 120, 543, 277), ref='2021 OL Q10',
                     alt='The linear search algorithm printed with Question 10, for a list L and '
                         'a value x: Step 1 set i to 0; Step 2 set n to the number of items in L; '
                         'Step 3 if i >= n go to Step 8; Step 4 if L[i] = x go to Step 7; Step 5 '
                         'set i to i + 1; Step 6 go to Step 3; Step 7 print position i and go to '
                         'Step 9; Step 8 print "item not found"; Step 9 exit.'),
    'q13-fig4': crop('038', 10, (107, 365, 482, 490), ref='2021 OL Q13(a)',
                     alt='Figure 4: an iterative design cycle drawn as arrows, Investigate, Plan, '
                         'Design, Create, Evaluate and Document, with an Iterate arrow looping from '
                         'Evaluate back to Plan.'),
    'q13-fig5': crop('038', 13, (162, 82, 452, 398), ref='2021 OL Q13(c)',
                     alt='Figure 5: two screenshots of the COVID Tracker app. The first shows '
                         'first and second dose vaccination counts, 371 cases and 24 deaths on 23rd '
                         'March, and a bar chart of daily confirmed cases; the second shows the '
                         'national picture, hospital and ICU figures for the last 24 hours, and '
                         'tests completed and the positive rate for the last 7 days. Both have a '
                         'tab bar: Updates, Vaccine Stats, COVID Check-In, Contact Tracing.'),
    'q15b-gates': crop('038', 18, (172, 88, 398, 278), ref='2021 OL Q15(b)(i)',
                       alt='The two logic gates printed with Question 15(b)(i): a NOT gate with '
                           'input 0, and an AND gate with inputs 0 and 1, each output on a blank '
                           'line.'),
    'q15b-fig7': crop('038', 18, (151, 314, 429, 581), ref='2021 OL Q15(b)(ii)',
                      alt='Figure 7: an OR gate with inputs A and B and output out. Below it, the '
                          'truth table, INPUTS A and B reading 0 0, 0 1, 1 0 and 1 1, and the '
                          'OUTPUTS column A OR B blank.'),
    'q15c-fig8': crop('038', 19, (214, 96, 382, 335), ref='2021 OL Q15(c)',
                      alt='Figure 8: four stacked layers of a computer system, from top to bottom '
                          'User, Application, Operating System and Hardware, with arrows passing '
                          'down and up between neighbouring layers.'),
    'q16a-code': crop('040', 3, (75, 348, 541, 479), ref='2021 OL Q16(a)',
                      alt='The nine-line program Question16_A.py as printed in the Section C '
                          'booklet: two comment lines, pin = "1579", userTry = input("Enter '
                          'PIN:"), then if userTry == pin: print("Welcome").'),
    's-q2': crop('scheme', 4, (55, 516, 150, 568), ref='2021 OL Q2', solution=True,
                 alt='The marking scheme\'s working for Question 2: the digits 1 1 0 1 over the '
                     'place values 2 to the powers 3, 2, 1 and 0, then 8 + 4 + 0 + 1 = 13.'),
    's-q15b-i': crop('scheme', 13, (196, 283, 398, 460), ref='2021 OL Q15(b)(i)', solution=True,
                     alt='The marking scheme\'s answers to Question 15(b)(i): the NOT gate with '
                         'input 0 gives 1, and the AND gate with inputs 0 and 1 gives 0.'),
    's-q16a': crop('scheme', 15, (53, 157, 543, 388), ref='2021 OL Q16(a)', solution=True,
                   alt='The marking scheme\'s possible solution to Question 16(a), lines 1 to 20: '
                       'pin = "1579"; loggedIn = False and failedAttempts = 0; while not loggedIn '
                       'and (failedAttempts < 3): read userTry (with the comment #input command is '
                       'asking the user for a PIN); if it equals pin print Welcome and set '
                       'loggedIn = True, else print Incorrect PIN and add 1 to failedAttempts; '
                       'after the loop, if failedAttempts >= 3 print You have entered the PIN '
                       'incorrectly, failedAttempts, times.'),
}

Q10_STEM = P(8, 'The linear search algorithm shown below is to be applied', 'L = [10, 25, 21, 15, 85, 69, 74, 22, 19, 6]')
Q10_ASK = P(8, 'What is the output of this algorithm', 'the following values of x?')
Q13_STEM = [P(10, 'The following article appeared online on July 7th 2020.'),
            P(10, 'Contact tracing: Ireland launches its app following', 'tested positive for COVID‐19.')]
Q14A_STEM = P(14, 'Binary search is an efficient algorithm', 'from a list of items.')
Q14B_STEM = P(15, 'The following list of numbers is to be searched using the binary search algorithm.', '1 2 3 4 5 6 7 8 9 10 11 12')
Q16A_STEM = C(3, 'The program below is for a simple Automatic Teller Machine', 'a message appears saying “Welcome”.')
CORRECT = 'Correct implementation using solution above or similar.'

CARDS = [
    # ── Section A ──────────────────────────────────────────────────────────
    dict(key=(1, None, None), topic='cs-2-4', qfigure='q1-table', total=5,
         why='p3: a data type for five assignments; the scheme\'s table pairs them, 1 each',
         ask=P(3, 'Choose the appropriate Python data type', 'Float Boolean Integer String List'),
         rows=[pt(Pair(T(4, 'a = 5'), T(4, 'Integer')), 1, note=S(4, 'Each correct item 1 mark')),
               pt(Pair(T(4, 'b = "Hello World"'), T(4, 'String')), 1),
               pt(Pair(T(4, 'c = True'), T(4, 'Boolean')), 1),
               pt(Pair(T(4, 'd = ["apple", "banana", "orange"]'), T(4, 'List')), 1),
               pt(Pair(T(4, 'e = 2.718'), T(4, 'Float')), 1)]),
    dict(key=(2, None, None), topic='cs-2-3', figure='s-q2', total=5,
         replaces='batch 1b: no answer rows (an empty card)',
         why='p3: 1101 in decimal; the scheme works it to 13, 5 / 4 / 3 / 2',
         ask=P(3, 'Convert the binary number 1101 to a decimal number.'),
         rows=[crit(S(4, '8 + 4 + 0 + 1 = 13'), 5, [2, 3, 4],
                    note=S(4, 'Correct 5 marks', 'Any correct step 2 marks'))]),
    dict(key=(3, None, None), topic='cs-2-3', total=5,
         replaces='batch 1b: no answer rows (an empty card)',
         why='p4: one advantage of Unicode over ASCII; the scheme gives three, 5 / 3 / 1',
         ask=P(4, 'Unicode and the American Standard Code for Information Interchange', 'rather than ASCII.'),
         rows=[ladder([S(5, 'Unicode can represent a greater range of character sets than ASCII.', 'emojis etc.'),
                       S(5, 'Unicode represents most written languages in the world while ASCII does not.'),
                       S(5, 'ASCII has its equivalent within Unicode.')], [[1, 3, 5]],
                      head=S(5, 'Any one of the above:'),
                      instruction=S(5, 'Or similar positive benefit of Unicode or ASCII.'),
                      note=S(5, 'Very good explanation - clear understanding demonstrated 5 marks',
                             'Fair explanation - limited understanding 1 mark'))]),
    dict(key=(4, None, None), topic='cs-1-1', qfigure='q4-fig1', total=5,
         replaces='batch 1b: no answer rows (an empty card); Figure 1 was missing',
         why='p4: another automated process and its benefit; the scheme prints only the criteria, '
             'a valid example 2 and its explanation 3 / 2',
         ask=P(4, 'The image in Figure 1 shows drones', 'benefit provided by your example.'),
         rows=[crit(S(5, 'Any valid example'), 5, [],
                    parts=[(P(4, 'Example:'), 2, []), (P(4, 'Benefit:'), 3, [2])],
                    note=S(5, 'Any valid example 2 marks', 'Fair explanation - limited understanding 2 mark'))]),
    dict(key=(5, None, None), topic='cs-2-3', qfigure='q5-fig2', total=5,
         replaces='batch 1b: no answer rows (an empty card); the figure carried the ask and sat on '
                  'the answer side',
         why='p5: one everyday use of the client-server model; the scheme lists examples, any '
             'valid one 5',
         ask=P(5, 'The image in Figure 2 depicts a client', 'interaction with technology.'),
         rows=[pt(S(5, 'Answer: online banking, ecommerce', 'where client communicates with server'), 5,
                  note=S(5, 'Any valid example 5 marks'))]),
    dict(key=(6, None, None), topic='cs-2-3', qfigure='q6-boxes', total=5,
         replaces='batch 1b: unpriced question-total rows',
         why='p5: shipped as the whole of Q6. (a) what HTTP is, the ticked box, 2; (b) the Web '
             'against the Internet, 3 / 2',
         ask=P(5, '(a) Answer the following question by putting a tick', 'the World Wide Web (WWW) and the Internet.'),
         rows=[ofpart(P(5, '(a)'), pt(S(5, 'the protocol for transferring hypertext for webpages'), 2,
                                      note=S(5, 'Correct 2 marks', '(Incorrect if more than 1 box is ticked)'))),
               ofpart(P(5, '(b)'), crit(S(6, 'The internet is a global system of interconnected computers', 'uses the HTTP protocol.'),
                                        3, [2],
                                        note=S(6, 'Very good description - clear understanding demonstrated 3 marks',
                                               'Fair description - limited understanding 2 mark')))]),
    dict(key=(7, None, None), topic='cs-2-3', qfigure='q7-fig3', total=5,
         replaces='batch 1b: no answer rows (an empty card); the figure carried a sliver of the ask '
                  'and sat on the answer side',
         why='p6: one difference between analogue and digital input; the scheme answers it, '
             '5 / 3 / 1',
         ask=P(6, 'Figure 3 shows the wave signals', 'between the two types of input.'),
         rows=[crit(S(6, 'Digital input signals are used to represent items', 'temperature or light levels, etc.'), 5, [1, 3],
                    note=S(6, 'Very good description - clear understanding demonstrated 5 marks',
                           'Fair description - limited understanding 1 mark'))]),
    dict(key=(8, None, None), topic='cs-2-2', qfigure='q8-fig0', total=5,
         replaces='batch 1b: no answer rows (an empty card); the flowchart sat on the answer side',
         why='p6: the output of the flowchart; the scheme prints 10 9 8 7 6 5, 5 / 3 / 1. The '
             'shipped crop of the flowchart was opened and is complete',
         ask=P(6, 'What output is produced by the algorithm shown in the flowchart below?'),
         rows=[crit(S(6, '10 9 8 7 6 5'), 5, [1, 3],
                    note=S(6, 'Correct 5 marks', 'Any valid number output 1 mark'))]),
    dict(key=(9, None, None), topic='cs-2-2', qfigure='q9-code', total=5,
         printed=S(7, 'Question 9 3+2 marks'), tariff_note='3 for the trace table and 2 for the output',
         why='p7: a trace table and the output; the scheme prints the rows (each row or column 1, '
             'max 3) and the output 11 (2)',
         ask=P(7, 'Complete the trace table below to determine the output', 'completed for you.'),
         rows=[crit(S(7, '2 2 4 True', '4 4 11 False'), 3, [1, 2],
                    note=S(7, 'Each correct row/column 1 mark (max 3 marks)', 'Any one value correct 1 mark (total)')),
               pt(S(7, 'Answer: 11'), 2, note=S(7, 'Correct output 2 marks'))]),
    dict(key=(10, 'a', None), topic='cs-2-2', qfigure='q10-algo', total=3,
         printed=S(7, 'Question 10 3 + 2 marks'),
         why='p8: the output when searching for 21; the scheme prints 2',
         stem=Q10_STEM, ask=[Q10_ASK, P(8, 'x = 21')],
         rows=[pt(S(7, 'Answer: 2'), 3, note=S(7, 'Both correct 5 marks Any one correct 3 marks'))]),
    dict(key=(10, 'b', None), topic='cs-2-2', qfigure='q10-algo', total=2,
         printed=S(7, 'Question 10 3 + 2 marks'),
         why='p8: the output when searching for 3; the scheme prints item not found',
         stem=Q10_STEM, ask=[Q10_ASK, P(8, 'x = 3')],
         rows=[pt(S(7, 'Answer: item not found'), 2, note=S(7, 'Both correct 5 marks Any one correct 3 marks'))]),
    dict(key=(11, None, None), topic='cs-1-2', total=5,
         replaces='batch 1b: no answer rows (an empty card); topic was Computational thinking',
         why='p9: adaptive technology for an elderly person living alone; the scheme answers it, '
             '5 / 3 / 1. Filed under Computers and society',
         ask=P(9, 'Describe one example of how adaptive or assistive technology', 'elderly person living alone.'),
         rows=[crit(S(8, 'Examples such as robots for social company', 'technology provides an assisting role.'), 5, [1, 3],
                    note=S(8, 'Very good description - clear understanding demonstrated 5 marks',
                           'Fair description - limited understanding 1 mark'))]),
    dict(key=(12, None, None), topic='cs-2-2', total=5,
         replaces='batch 1b: no answer rows (an empty card)',
         why='p9: two checks to validate an email address; the scheme lists five, first 3 and '
             'second 2',
         ask=P(9, 'A programmer has written a program to store the name', 'validate the email address.'),
         rows=[anyn([S(8, 'check that the email address is actually there (not left blank).'),
                     S(8, 'check that the email address does not contain spaces (or other illegal characters).'),
                     S(8, 'check that the email address contains the @ symbol.'),
                     S(8, 'check that the email address contains no more than 256 characters in total .'),
                     S(8, 'check that the email address has a valid domain name e.g. info@test.com'),
                     S(8, 'Or similar email validation check.')], 2, 3, steps=[3, 2], open_list=True,
                    head=P(9, 'Describe two checks that could be used to validate the email address.'),
                    note=S(8, 'First correct 3 marks Second correct 2 marks'))]),
    # ── Section B ──────────────────────────────────────────────────────────
    dict(key=(13, 'a', 'i'), topic='cs-2-5', qfigure='q13-fig4', total=6,
         replaces='batch 1b: no answer rows (an empty card); topic was Algorithms',
         why='p10: two activities in the evaluate stage; the scheme lists eight, 3 / 2 each. '
             'Filed under Evaluation and testing',
         stem=Q13_STEM,
         ask=P(10, 'Assuming that the COVID Tracker app was developed', 'undertaken in the evaluate stage.'),
         rows=[ladder([S(9, 'Unit Testing – to test the functionality of each part of the system.'),
                       S(9, 'System testing – to test the functionality of the entire system.'),
                       S(9, 'User testing – to test the functionality from an end user perspective.'),
                       S(9, 'Beta Testing – early release testing to small group.'),
                       S(9, 'Black box testing – testing of system as a black box.'),
                       S(9, 'Whitebox testing – testing every line of code for code coverage.'),
                       S(9, 'Non-functional testing e.g. Performance testing', 'impacts on mobile phones.'),
                       S(9, 'User survey – to get users feedback.')], [[2, 3], [2, 3]],
                      head=S(9, 'Example Activities:'), instruction=S(9, 'Or similar testing/validation.'),
                      note=S(9, 'For each activity: Very good description', 'Fair description - limited understanding 2 marks'))]),
    dict(key=(13, 'a', 'ii'), topic='cs-1-3', total=10,
         replaces='batch 1b: no answer rows (an empty card); topic was Computer systems',
         why='p11: two roles in developing the app; the scheme names seven, each named 2 and '
             'described 3 / 2. Filed under Designing and developing',
         stem=Q13_STEM,
         ask=P(11, 'The Irish COVID Tracker app was developed by an Irish company', 'development of the app.'),
         rows=[ladder([S(9, 'Software Developer'), S(9, 'Project Manager'), S(9, 'Team Leader'),
                       S(9, 'Product Manager/Owner'), S(9, 'Graphic Designer'), S(9, 'Tester'),
                       S(9, 'Subject Matter Expert (e.g. on infectious diseases)')], [[2, 3, 4, 5], [2, 3, 4, 5]],
                      instruction=S(9, 'or similar role.'),
                      note=S(9, 'For each role: Name 2 marks', 'Fair description - limited understanding 2 marks'))]),
    dict(key=(13, 'b', None), topic='cs-1-2', total=6,
         replaces='batch 1b: no answer rows (an empty card)',
         why='p12: two reasons privacy matters for a contact-tracing app; the scheme names GDPR '
             'and ethical reasons, 3 / 2 each',
         stem=Q13_STEM,
         ask=P(12, 'The Irish COVID Tracker app uses technology from Apple and Google', 'contact tracing app.'),
         rows=[ladder([S(10, 'Any reason related to GDPR requirements.'), S(10, 'Any ethical reason.')], [[2, 3], [2, 3]],
                      instruction=S(10, 'Or similar.'),
                      note=S(10, 'For each explanation: Very good explanation', 'Fair explanation - limited understanding 2 mark'))]),
    dict(key=(13, 'c', None), topic='cs-1-2', qfigure='q13-fig5', total=8,
         replaces='batch 1b: no answer rows (an empty card); Figure 4 sat on the answer side '
                  'instead of Figure 5; topic was Algorithms',
         why='p13: two principles of universal design in the app; the scheme lists universal and '
             'UI design principles, 4 / 2 each. Filed under Computers and society',
         stem=Q13_STEM,
         ask=P(13, 'The screenshots in Figure 5 below', 'when designing this app.'),
         rows=[ladder([S(10, 'Principle 1: Equitable Use'), S(10, 'Principle 2: Flexibility in Use'),
                       S(10, 'Principle 3: Simple and Intuitive Use'), S(10, 'Principle 4: Perceptible Information'),
                       S(10, 'Principle 5: Tolerance for Error'), S(10, 'Principle 6: Low Physical Effort'),
                       S(10, 'Principle 7: Size and Space for Approach and Use'),
                       S(10, 'Place users in control of the interface.'),
                       S(10, 'Make it comfortable to interact with a product.'),
                       S(10, 'Reduce cognitive load.'), S(10, 'Make user interfaces consistent.'),
                       S(10, 'Visibility of system status', 'help and documentation'),
                       S(10, 'Visibility, Feedback, Constraints, Mapping, Consistency, Affordance.')], [[2, 4], [2, 4]],
                      instruction=S(10, 'Accept principles of universal design or UI design.'),
                      note=S(10, 'For each principle: Very good description', 'Fair description - limited understanding 2 mark'))]),
    dict(key=(14, 'a', 'i'), topic='cs-2-2', total=3,
         replaces='batch 1b: no answer rows (an empty card); topic was Computer systems',
         why='p14: why binary search is divide and conquer; the scheme answers it, 3 / 2. Filed '
             'under Algorithms',
         stem=Q14A_STEM, ask=P(14, 'The binary search algorithm is often called', 'Explain why.'),
         rows=[crit(S(11, 'It works by recursively breaking down a problem', 'until the item is found.'), 3, [2],
                    note=S(11, 'Very good description - clear understanding demonstrated 3 marks',
                           'Fair description - limited understanding 2 marks'))]),
    dict(key=(14, 'a', 'ii'), topic='cs-2-2', total=3,
         replaces='batch 1b: no answer rows (an empty card); topic was Computer systems',
         why='p14: why binary beats linear search; the scheme contrasts them, 3 / 2. Filed under '
             'Algorithms',
         stem=Q14A_STEM, ask=P(14, 'Why is the binary search algorithm considered to be more efficient', 'linear search algorithm?'),
         rows=[crit(S(11, 'Linear search has to go through each position until found.', 'splitting in half each time.'), 3, [2],
                    note=S(11, 'Very good description - clear understanding demonstrated 3 marks',
                           'Fair description - limited understanding 2 marks', nth=2))]),
    dict(key=(14, 'a', 'iii'), topic='cs-2-2', total=4,
         replaces='batch 1b: no answer rows (an empty card); topic was Computer systems',
         why='p14: whether binary search works on the unsorted list; the scheme answers no, '
             'because it is not sorted, 2 + 2. Filed under Algorithms',
         stem=Q14A_STEM, ask=P(14, 'The following list of numbers is to be searched for a specific number', 'Explain your answer.'),
         rows=[crit(S(11, 'No, because the list is not sorted.'), 4, [2],
                    note=S(11, 'No 2 marks Needs to be sorted 2 marks'))]),
    dict(key=(14, 'b', 'i'), topic='cs-2-2', total=6,
         replaces='batch 1b: no answer rows (an empty card)',
         why='p15: the steps to find 8; the scheme works them, 6 / 4 / 2 / 1',
         stem=Q14B_STEM, ask=P(15, 'Illustrate the steps taken to find the number 8.'),
         rows=[crit(S(11, 'The List is repeatedly divided in two', 'Low = 8, High = 9. Found'), 6, [1, 2, 4],
                    note=[S(11, 'Note that in step 1 the mid value could be 7', 'change the subsequent steps.'),
                          S(12, 'Fully worked solution including repeated divisions of list 6 marks',
                            'Any correct step (e.g. identify low, high) 1 marks')])]),
    dict(key=(14, 'b', 'ii'), topic='cs-2-2', total=4,
         replaces='batch 1b: no answer rows (an empty card); topic was Computer systems',
         why='p15: the most steps for 60 numbers; the scheme works it to 6, 4 / 2. Filed under '
             'Algorithms',
         stem=Q14B_STEM, ask=P(15, 'A list contains 60 numbers in numerical order.', 'when using a binary search.'),
         rows=[crit(S(12, 'Step 1: 30 number', 'Answer: 6'), 4, [2],
                    note=S(12, 'Correct answer 4 marks', 'Some correct steps in calculation 2 marks'))]),
    dict(key=(14, 'c', None), topic='cs-1-2', total=10,
         replaces='batch 1b: no answer rows (an empty card); topic was Algorithms',
         why='p16: an advantage and a disadvantage of a bail algorithm; the scheme lists two and '
             'four, 5 / 3 / 2 each. Filed under Computers and society',
         ask=P(16, 'In America algorithms are being used increasingly', 'a decision such as this.'),
         rows=[ladder([S(12, 'Algorithm treats everyone the same.'),
                       S(12, 'Avoids any subconscious bias – race and socio-economic factors are ignored.')], [[2, 3, 5]],
                      head=S(12, 'Advantage:'),
                      note=S(12, 'For each advantage/disadvantage: Very good explanation 5 marks', 'Fair explanation 2 mark')),
               ladder([S(12, 'Removes human feelings from decision-making.'),
                       S(12, 'If it was incorrectly coded it could incorrectly leave someone in jail.'),
                       S(12, 'The algorithm was designed by humans so may have bias built into it.'),
                       S(12, 'Algorithm could ignore important factors', 'person’s life recently.')], [[2, 3, 5]],
                      head=S(12, 'Disadvantage'))]),
    dict(key=(15, 'a', None), topic='cs-2-3', qfigure='q15-fig0', total=8,
         replaces='batch 1b: no answer rows (an empty card)',
         why='p17: two specification items slowing the computer; the scheme names five, each '
             'item 1 and its explanation 3 / 2. The shipped crop of the list and Figure 6 was '
             'opened and is complete',
         ask=P(17, 'Your friend complains to you', 'explain their impact.'),
         rows=[ladder([S(13, 'Processor'), S(13, 'RAM'), S(13, 'Graphics Card'), S(13, 'Wireless'),
                       S(13, 'Networking')], [[1, 2, 3, 4], [1, 2, 3, 4]],
                      note=S(13, 'For each item: Valid item 1 mark', 'Fair explanation 2 mark'))]),
    dict(key=(15, 'b', 'i'), topic='cs-2-3', qfigure='q15b-gates', figure='s-q15b-i', total=6,
         printed=S(13, 'Both correct 6 marks'),
         why='p18: the outputs of a NOT and an AND gate; the scheme prints 1 and 0 beside its '
             'drawing (read by position), both 6, one 3. Split out of the withdrawn whole-question '
             'card cs-2021-ol-q15',
         ask=P(18, 'State the output of each of the following logic gates for the inputs given.'),
         rows=[pt(At('scheme', 13, (330, 309, 342, 329)), 3, note=S(13, 'Both correct 6 marks', 'One correct 3 marks')),
               pt(At('scheme', 13, (325, 412, 338, 433)), 3)]),
    dict(key=(15, 'b', 'ii'), topic='cs-2-3', qfigure='q15b-fig7', total=4,
         replaces='batch 1b: no answer rows (an empty card); the specification figure sat on the '
                  'answer side',
         why='p18: the OR truth table; the scheme prints the four rows, 1 each',
         ask=P(18, 'Complete the truth table for the OR logic gate, shown in Figure 7.'),
         rows=[pt(S(13, '0 0 0'), 1, note=S(13, 'Each row correct – 1 mark')), pt(S(13, '0 1 1'), 1),
               pt(S(13, '1 0 1'), 1), pt(S(13, '1 1 1'), 1)]),
    dict(key=(15, 'c', None), topic='cs-2-3', qfigure='q15c-fig8', total=6,
         replaces='batch 1b: no answer rows (an empty card); the specification figure sat on the '
                  'answer side instead of Figure 8',
         why='p19: the purpose of two layers; the scheme describes four, 3 / 2 each',
         ask=P(19, 'The diagram in Figure 8 below', 'any two layers.'),
         rows=[ladder([S(14, 'The hardware layer is the lowest layer', 'mouse, keyboard, scanner etc.'),
                       S(14, 'The operating system (OS) manages computer hardware', 'services for computer programs.'),
                       S(14, 'The application layer is the layer that actually interacts', 'uses an application.'),
                       S(14, 'The user layer contains the user interface that users interact with.')], [[2, 3], [2, 3]],
                      note=S(14, 'For each of the 2 chosen layers:', 'Fair description - limited understanding 2 marks'))]),
    dict(key=(15, 'd', None), topic='cs-1-2', total=6,
         replaces='batch 1b: no answer rows (an empty card); topic was Embedded systems',
         why='p20: another important development and its impact; the scheme prints only the '
             'criteria, the development named 2 and described 4 / 2, and names no example. Filed '
             'under Computers and society',
         ask=P(20, 'Developed in 1971, the first commercially produced microprocessor', 'its impact on computing today.'),
         rows=[crit(S(14, 'Name valid development'), 6, [2, 4],
                    note=S(14, 'Name valid development 2 marks', 'Fair description - limited understanding 2 marks', nth=1))]),
    # ── Section C (split out of the withdrawn whole-question card cs-2021-ol-q16) ──
    dict(key=(16, 'a', 'i'), topic='cs-2-2', qfigure='q16a-code', figure='s-q16a', total=5,
         printed=S(15, '(i) 5 marks (A-5 scale)'),
         why='040 p3: a comment on the input line; the scheme\'s comment on line 9, A-5 scale',
         stem=Q16A_STEM, ask=C(3, 'Insert a comment in the appropriate location', 'doing in this program.'),
         rows=[crit(S(15, CORRECT), 5, [2, 3], note=S(15, '(i) 5 marks (A-5 scale)', 'Any reasonable attempt at inserting a comment.'))]),
    dict(key=(16, 'a', 'ii'), topic='cs-2-2', qfigure='q16a-code', figure='s-q16a', total=10,
         printed=S(15, '(ii) 10 marks (A-10 scale)'),
         why='040 p3: print Incorrect PIN otherwise; the scheme\'s else (lines 15-16), A-10 scale',
         stem=Q16A_STEM, ask=C(3, 'Amend the program so that the following message is displayed', 'Incorrect PIN'),
         rows=[crit(S(15, 'Correct implementation using solution above or similar (included else and a print statement).'), 10, [3, 7],
                    note=S(15, '(ii) 10 marks (A-10 scale)', 'indicating incorrect pin.'))]),
    dict(key=(16, 'a', 'iii'), topic='cs-2-2', qfigure='q16a-code', figure='s-q16a', total=5,
         printed=S(16, '(iii) 5 marks (A-5 scale)'),
         why='040 p3: a Boolean set False first; the scheme\'s loggedIn = False (line 5), A-5 scale',
         stem=Q16A_STEM, ask=C(3, 'Create a suitably named Boolean variable', 'before the user enters a PIN.'),
         rows=[crit(S(16, CORRECT), 5, [2, 3], note=S(16, '(iii) 5 marks (A-5 scale)', 'limited knowledge of Boolean.'))]),
    dict(key=(16, 'a', 'iv'), topic='cs-2-2', qfigure='q16a-code', figure='s-q16a', total=5,
         printed=S(16, '(iv) 5 marks (A-5 scale)'),
         why='040 p3: set the Boolean True on the correct PIN; the scheme\'s line 14, A-5 scale',
         stem=Q16A_STEM, ask=C(3, 'Amend the program so that the new Boolean variable is set to True', 'enters the correct PIN.'),
         rows=[crit(S(16, CORRECT, nth=2), 5, [2, 3], note=S(16, '(iv) 5 marks (A-5 scale)', 'e.g. in the wrong place.'))]),
    dict(key=(16, 'a', 'v'), topic='cs-2-2', qfigure='q16a-code', figure='s-q16a', total=10,
         printed=S(16, '(v) 10 marks (A-10 scale)'),
         why='040 p4: loop until the PIN is right; the scheme\'s while loop (line 8), A-10 scale',
         stem=Q16A_STEM, ask=C(4, 'Using a while loop or similar', 'Enter PIN:1579 Welcome'),
         rows=[crit(S(16, CORRECT, nth=3), 10, [3, 7], note=S(16, '(v) 10 marks (A-10 scale)', 'syntax errors in its implementation.'))]),
    dict(key=(16, 'a', 'vi'), topic='cs-2-2', qfigure='q16a-code', figure='s-q16a', total=5,
         printed=S(17, '(vi) 5 marks (A-5 scale)'),
         why='040 p4: a failed-attempts counter set to 0; the scheme\'s failedAttempts = 0 (line '
             '6), A-5 scale',
         stem=Q16A_STEM, ask=C(4, 'Create a suitably named variable (e.g. failedAttempts)', 'number of failed login attempts.'),
         rows=[crit(S(17, CORRECT), 5, [2, 3], note=S(17, '(vi) 5 marks (A-5 scale)', 'e.g. in the wrong place.'))]),
    dict(key=(16, 'a', 'vii'), topic='cs-2-2', qfigure='q16a-code', figure='s-q16a', total=10,
         printed=S(17, '(vii) 10 marks (B-10 scale)'),
         why='040 p4: stop after three failures with a message; the scheme\'s loop condition, '
             'counter and lines 19-20, B-10 scale',
         stem=Q16A_STEM, ask=C(4, 'The user should only be allowed 3 failed login attempts.', 'You have entered the PIN incorrectly 3 times.'),
         rows=[crit(S(17, 'Correct implementation using solution above or similar for both cases (successful login or total many attempts).'),
                    10, [3, 5, 8], note=S(17, '(vii) 10 marks (B-10 scale)', 'if statement line 19 • print statement', end_nth=3))]),
]
