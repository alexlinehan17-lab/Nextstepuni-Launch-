"""Computer Science 2020 Higher Level: all 47 printed asks; the bank held none.

Paper pages 3-24 (Sections A and B) and Section C pages 3-10, and scheme
pages 3-27 were opened. 2020 had no Ordinary Level paper.

Q5's scheme prices its two parts "First correct 3 marks / Second correct 2
marks" under "3 + 2 marks"; each part is carded at its place in that sum,
(a) 3 and (b) 2, with the scheme's rule quoted on the row.

Q6(b)'s first limitation prints 2 to the power 7 = 128 in Cambria Math, whose
text layer draws each digit twice and reads the 8 of 128 as a 1. The line is
read by glyph id instead (compsci_lane.append_glyphs, the glyph block of
2020-hl.md): every id it uses has a sane sighting, the 8's in 2021 HL scheme
p4 ("log2 8 = 3"), so it is a claimable option like the rest.

A menu the scheme prices on a good/fair ladder ("Any one of the above points:
Good 2 / Fair 1") is a ladder() row, so the fair price is claimable; a line
among the answers that is not an answer ("Any similar explanation.") is lifted
into the note (coordinator, 5 Nov).

Section C prints a level descriptor for every step of each scale (scheme
pages 19-22, 25-27); each part's row is the scheme's "Correct implementation
using included solution or similar." on that scale's printed steps, with the
descriptors as its note and the lines of the possible solution marked for that
part as its solution crop.
"""
from compsci_lane import (C, G, P, Pair, S, T, anyn, ask_row, crit, crop, ladder, pt, stack)  # noqa: F401

CROPS = {
    'q1-table': crop('038', 3, (148, 185, 447, 388), ref='2020 HL Q1',
                     alt='The JavaScript declarations printed with Question 1, let a = 5; and '
                         'let b = 2;, above a table whose Expression column lists a * b, a ** b, '
                         'a / b, b % a and ++a and whose Result column is blank.'),
    'q5-circuit': crop('038', 5, (82, 106, 499, 322), ref='2020 HL Q5',
                       alt='The half-adder circuit printed with Question 5: inputs A and B feed '
                           'an AND gate whose output is C, and two AND gates, each taking one '
                           'input through a NOT gate, feed an OR gate whose output is S.'),
    'q7-binary': crop('038', 6, (245, 475, 350, 503), ref='2020 HL Q7',
                      alt='The 8-bit binary representation of the ASCII character K printed with '
                          'Question 7: 0100 1011.'),
    'q8-passes': crop('038', 7, (60, 166, 546, 355), ref='2020 HL Q8',
                      alt='The bubble sort diagram printed with Question 8: the list 8 5 9 7 6 is '
                          'scanned in four passes. Pass 1 is complete, ending 5 8 7 6 9; pass 2 '
                          'shows its first two rows and two blank rows; pass 3 starts 5 7 6 8 9 '
                          'with two blank rows; pass 4 starts 5 6 7 8 9 with one blank row, '
                          'marked finished.'),
    's-q8': crop('scheme', 7, (55, 105, 512, 281), ref='2020 HL Q8', solution=True,
                 alt='The marking scheme\'s completed bubble sort diagram for Question 8: pass 2 '
                     'continues 5 7 8 6 9 then 5 7 6 8 9; pass 3 continues 5 7 6 8 9 then 5 6 7 '
                     '8 9; pass 4 continues 5 6 7 8 9, finished; 1M is marked beside the filled '
                     'rows.'),
    'q9-data': crop('038', 7, (168, 414, 428, 555), ref='2020 HL Q9',
                    alt='The 100m race data set printed with Question 9, columns Surname, Gender, '
                        'Age and Time: Murphy M 17 13,12; Ogene M 16 12.14 twice; Mc Intyre F. 17 '
                        '12.87; Lopez F -18 14.01; a blank surname F 17 1 329; McCarthy M 77 '
                        '13.65; Ó Brádaigh f 16 13.09.'),
    'q10-html': stack([('038', 8, (55, 109, 535, 349)), ('038', 8, (55, 420, 510, 586))],
                      ref='2020 HL Q10',
                      alt='The HTML printed with Question 10 beside the web page it displays (the '
                          'heading Menu, a bulleted list of Burger, Fish and Pasta, and a line '
                          'Click here for desserts). Four pieces of the code are replaced by the '
                          'numbers 1 to 4: the html tag name, the heading text, the list tag name '
                          'and the link attribute. Below it, a table numbered 1 to 4 with a blank '
                          'Missing Code column.'),
    's-q10': crop('scheme', 8, (57, 98, 370, 258), ref='2020 HL Q10', solution=True,
                  alt='The marking scheme\'s table for Question 10: number 1 html, number 2 '
                      'Menu, number 3 ul, number 4 href.'),
    'q11-code': stack([('038', 9, (330, 74, 541, 159)), ('038', 9, (55, 179, 541, 356))],
                      ref='2020 HL Q11',
                      alt='The table printed with Question 11 (80 or over Distinction, from 40 to '
                          '79 Pass, less than 40 Unsuccessful) above the twelve-line JavaScript '
                          'function getGradeDescription: gradeDescription starts as Unsuccessful, '
                          'then if (percentageGrade >= 80) sets Distinction and a second, separate '
                          'if (percentageGrade >= 40) sets Pass, before it is returned.'),
    'q12-graph': crop('038', 10, (55, 119, 527, 349), ref='2020 HL Q12',
                      alt='The box printed with Question 12: the quoted problem above a graph of '
                          'six numbered cities joined by roads labelled with their distances, '
                          'city 1 marked Start / Finish.'),
    'q13-code': crop('038', 11, (55, 261, 510, 452), ref='2020 HL Q13(a)',
                     alt='The thirteen-line Python program printed with Question 13(a): names = '
                         '["John", "Mary", "Zoe", "Alex", "Séamas"]; a name is read; found = '
                         'False and index = 0; while (not found) and (index != len(names)), if '
                         'name == names[index] found becomes True, else index is increased by 1; '
                         'then print("Result:", index).'),
    'q13b-list': crop('038', 13, (55, 245, 510, 338), ref='2020 HL Q13(b)(ii)',
                      alt='The list L printed with Question 13(b)(ii): 3, 7, 13, 18, 28, 35, 41, '
                          '50 at indexes 0 to 7, with left pointing at index 0, mid at index 3 '
                          'and right at index 7.'),
    's-q13b-ii': crop('scheme', 11, (52, 62, 440, 203), ref='2020 HL Q13(b)(ii)', solution=True,
                      alt='The marking scheme\'s alternative answer to Question 13(b)(ii): 28 > '
                          '18 so left becomes 4 and mid 5; 28 < 35 so right becomes 4 and mid 4; '
                          '28 = 28, found; and a table of left, mid, right and L[mid] for each '
                          'step: 0 3 7 18, 4 5 7 35, 4 4 4 28.'),
    'q14-fsm': crop('038', 16, (155, 358, 502, 488), ref='2020 HL Q14(b)',
                    alt='The Finite State Machine printed with Question 14(b): state S1 loops on '
                        'itself on 0/0 and on 1/1, and moves to state S2 on B/0; a note reads B '
                        '= blank cell.'),
    'q14-table': stack([('038', 16, (155, 358, 502, 488)), ('038', 16, (182, 639, 414, 736))],
                       ref='2020 HL Q14(b)(ii)',
                       alt='The Finite State Machine of Question 14(b) (S1 loops on 0/0 and 1/1 '
                           'and moves to S2 on B/0) above the state transition table, with '
                           'columns Current State, Input, Output and Next State. Its first row, '
                           'S1 0 0 S1, is filled in; the next two rows begin S1 and are '
                           'otherwise blank.'),
    'q14-tape': stack([('038', 16, (155, 358, 502, 488)), ('038', 17, (88, 205, 505, 591))],
                      ref='2020 HL Q14(b)(iii)',
                      alt='The Finite State Machine of Question 14(b) above the tape diagram '
                          'printed with part (iii): six rows of tape, each with the read/write '
                          'head one cell further right and a Current State box. The first two '
                          'rows read 1 0 1 1 0 B in state S1; the other four show only 1 0 and '
                          'blank cells, their state boxes blank except the last, S2.'),
    's-q14b-iii': crop('scheme', 13, (70, 105, 525, 424), ref='2020 HL Q14(b)(iii)', solution=True,
                       alt='The marking scheme\'s completed rows for Question 14(b)(iii): four '
                           'rows read 1 0 1 1 0 B in state S1 as the head moves right one cell '
                           'at a time, and the last reads 1 0 1 1 0 0 in state S2.'),
    'q15-ui': crop('038', 23, (54, 55, 562, 730), ref='2020 HL Q15(c)',
                   alt='The two Rock Paper Scissors interfaces printed with Question 15(c). User '
                       'Interface 1: a Human panel with Rock, Paper and Scissors buttons; wins 7, '
                       'ties 5 and wins 8 for a Veteran Computer; the history of rounds 13 to '
                       '20; the computer\'s predictions; and Restart Game, Share on Twitter and '
                       'Post on Facebook. User Interface 2: a desktop window with Your Score 2 '
                       'and Computer\'s Score 0, Rock, Paper and Scissors radio buttons, the '
                       'computer\'s move, the message Scissors and Scissors. It\'s a tie, and a '
                       'Play button.'),
    'q16a-code': crop('040', 4, (53, 55, 542, 673), ref='2020 HL Q16(a)',
                      alt='The 42-line program Question16_A.py as printed in the Section C '
                          'booklet: the password is read; LOWER_CASE_LETTERS holds a to z; the '
                          'flags lowercase and uppercase start False and a loop over the '
                          'characters sets them, uppercase tested against the hard-coded string '
                          '"ABCDEFGHIJKLMNOPQRSTUVWXYZ"; score = 0; rule 1 adds 5 if '
                          'len(password) > 7, rule 2 adds 1 if lowercase, rule 3 adds 5 if '
                          'lowercase and uppercase; and print(score).'),
    'q16a-viii': stack([('040', 6, (175, 372, 420, 440)), ('040', 6, (237, 492, 358, 636))],
                       ref='2020 HL Q16(a)(viii)',
                       alt='The two tables printed with Question 16(a)(viii). Password length and '
                          'score: greater than 7 characters +5 points, from 4 to 7 characters +2 '
                          'points, less than 4 characters -2 points. Test passwords and their '
                          'scores: sun -1, Sun 6, sun2 9, 2sun3 12, 3Sunshine 19, 3Sunshine7 22.'),
    's-q16a-i': crop('scheme', 17, (57, 586, 545, 634), ref='2020 HL Q16(a)(i)', solution=True,
                     alt='Lines 30 to 32 of the marking scheme\'s possible solution: # Calculate '
                         'the score based on the rules, then score = 0 # Ans (i): initialise '
                         'score.'),
    's-q16a-ii': crop('scheme', 18, (57, 506, 545, 583), ref='2020 HL Q16(a)(ii)', solution=True,
                      alt='Lines 72 to 76 of the marking scheme\'s possible solution: # Display '
                          'the score, #print(score) commented out, # Ans (ii):, then '
                          'print("Password:", password) and print("Score:", score).'),
    's-q16a-iii': stack([('scheme', 17, (57, 270, 545, 314)), ('scheme', 17, (57, 457, 545, 529))],
                        ref='2020 HL Q16(a)(iii)', solution=True,
                        alt='Lines 8 to 10 and 21 to 25 of the marking scheme\'s possible '
                            'solution: UPPER_CASE_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" # Ans '
                            '(iii) declared under LOWER_CASE_LETTERS, and the loop testing if '
                            'character in UPPER_CASE_LETTERS: # Ans (iii) to set uppercase = '
                            'True.'),
    's-q16a-iv': crop('scheme', 18, (57, 205, 545, 249), ref='2020 HL Q16(a)(iv)', solution=True,
                      alt='Lines 51 to 53 of the marking scheme\'s possible solution: # Ans (iv): '
                          'Rule 4, if uppercase: score = score + 2.'),
    's-q16a-v': stack([('scheme', 17, (57, 270, 545, 558)), ('scheme', 18, (57, 263, 545, 307))],
                      ref='2020 HL Q16(a)(v)', solution=True,
                      alt='Lines 8 to 27 and 55 to 57 of the marking scheme\'s possible '
                          'solution: DIGITS = "0123456789" # Ans (v); a flag digits = False; the '
                          'loop testing if character in DIGITS: # Ans (v) to set digits = True; '
                          'and # Ans (v): Rule 5, if digits: score = score + 5.'),
    's-q16a-vi': crop('scheme', 18, (57, 320, 545, 421), ref='2020 HL Q16(a)(vi)', solution=True,
                      alt='Lines 59 to 65 of the marking scheme\'s possible solution: # Ans (vi): '
                          'Rule 6, if password[0] in DIGITS add 1, if password[-1] in DIGITS add '
                          '1, and if both are in DIGITS add 2.'),
    's-q16a-vii': crop('scheme', 18, (57, 435, 545, 478), ref='2020 HL Q16(a)(vii)', solution=True,
                       alt='Lines 67 to 69 of the marking scheme\'s possible solution: # Ans '
                           '(vii): Rule 7, if digits and not lowercase and not uppercase: score = '
                           'score - 10.'),
    's-q16a-viii': stack([('scheme', 17, (57, 643, 545, 749)), ('scheme', 18, (57, 62, 545, 77))],
                         ref='2020 HL Q16(a)(viii)', solution=True,
                         alt='Lines 34 to 41 of the marking scheme\'s possible solution: # Rule '
                             '1, # Ans (viii), if len(password) > 7 add 5, elif len(password) >= '
                             '4 and len(password) <= 7 add 2, else subtract 2.'),
    'q16b-code': crop('040', 8, (53, 55, 542, 713), ref='2020 HL Q16(b)',
                      alt='The 44-line program Question16_B.py as printed in the Section C '
                          'booklet: LOWER_CASE_LETTERS, then def calculate_score(password): with '
                          'the lowercase and uppercase flags, the loop over the characters, '
                          'rules 1 to 3 and return score; then the test driver, test_passwords = '
                          '["sun", "Sun", "Sunshine", "12345", "123456789"], and a loop that '
                          'prints calculate_score(password) for each password.'),
    's-q16b-i': stack([('scheme', 24, (57, 543, 545, 573)), ('scheme', 24, (57, 672, 545, 687))],
                      ref='2020 HL Q16(b)(i)', solution=True,
                      alt='Lines 78, 79 and 87 of the marking scheme\'s possible solution: '
                          'print("Score\\tPassword") and print("-----\\t--------") marked # Ans '
                          '(i), and inside the loop print(pass_score, "\\t", password) # Ans '
                          '(i).'),
    's-q16b-ii': crop('scheme', 24, (57, 500, 545, 534), ref='2020 HL Q16(b)(ii)', solution=True,
                      alt='Lines 75 and 76 of the marking scheme\'s possible solution: '
                          'test_passwords = ["sun", "Sun", "Sunshine", "12345", "123456789"], '
                          'then test_passwords[4] = "Moonlight" # Ans (ii).'),
    's-q16b-iii': crop('scheme', 24, (57, 572, 545, 749), ref='2020 HL Q16(b)(iii)', solution=True,
                       alt='Lines 80 to 91 of the marking scheme\'s possible solution: '
                           'lowest_score = 999 and weakest_password = "" before the loop; inside '
                           'it, if pass_score < lowest_score, both are updated; after it, '
                           'print("The weakest password is:", weakest_password) and '
                           'print("Score:", lowest_score), each marked # Ans (iii).'),
    's-q16b-iv': crop('scheme', 23, (57, 197, 545, 661), ref='2020 HL Q16(b)(iv)', solution=True,
                      alt='Lines 7 to 38 of the marking scheme\'s possible solution, three '
                          'versions of is_strong marked # Ans (iv): return '
                          '(calculate_score(password) == 11); a version setting strong = True '
                          'when calculate_score(password) == 11; and a version that sets the '
                          'lowercase and uppercase flags itself and returns True if '
                          'len(password) > 7 and lowercase and uppercase.'),
    's-q16b-v': crop('scheme', 25, (57, 76, 545, 200), ref='2020 HL Q16(b)(v)', solution=True,
                     alt='Lines 93 to 100 of the marking scheme\'s possible solution, # Ans (v): '
                         'print(), print("The strong passwords are:"), then for password in '
                         'test_passwords: if is_strong(password): print(password).'),
}

Q2_STEM = P(3, 'Many modern laptops have a hard', 'with a capacity of 512GB.')
Q4_STEM = P(4, 'The World Wide Web (WWW) and the network infrastructure', 'due to the protocols that it uses.')
Q5_STEM = P(5, 'The half', 'from two inputs, A and B.')
Q5_RULE = S(6, 'First correct 3 marks', 'Incorrect 0 mark')
Q6_STEM = P(6, 'The American Standard Code for Information Interchange', 'in 1963.')
Q13_STEM = P(11, 'In his book The Art of Computer Programming', 'substantial increase in speed.”')
Q13A = [Q13_STEM, P(11, 'The Python code below shows an implementation of a search algorithm.',
                    'answer the questions that follow:')]
Q13B = [Q13_STEM, P(13, 'Binary search is generally regarded as a highly efficient search algorithm.')]
Q14_STEM = P(16, 'Alan Turing is widely regarded', 'the Turing Test.')
Q14B = [Q14_STEM, P(16, 'The illustration below depicts a Finite State Machine', 'answer the questions that follow.')]
Q15_STEM = P(20, 'Rock Paper Scissors is a popular two player game', 'interactive computerised Rock Paper Scissors game.')
Q15C = [Q15_STEM, P(22, 'Your project team has identified two user interfaces', 'other Rock Paper Scissors games.')]
Q16A_STEM = [C(3, 'A password strength meter is a mechanism', 'numbers and special symbols.'),
             C(3, 'This program is designed to calculate and display a score', 'contains lowercase letters (1 point).')]
Q16B_STEM = C(7, 'This program is very similar to that provided for part (a)', 'displays the score of each password.')
CORRECT = 'Correct implementation using included solution or similar.'
OPTIMAL = 'Correct implementation using included solution or similar (optimal).'

CARDS = [
    # ── Section A ──────────────────────────────────────────────────────────
    dict(key=(1, None, None), topic='cs-2-2', qfigure='q1-table', total=5,
         why='p3: the result of five JavaScript expressions; the scheme prints each, 1 mark',
         ask=P(3, 'Given the following JavaScript variable declarations', 'expressions in the table below.'),
         rows=[pt(S(4, 'a * b 10'), 1, note=S(4, 'Each correct item 1 mark', nth=1)),
               pt(S(4, 'a ** b 25'), 1), pt(S(4, 'a / b 2.5'), 1), pt(S(4, 'b % a 2'), 1),
               pt(S(4, '++a 6'), 1)]),
    dict(key=(2, 'a', None), topic='cs-2-3', total=2, printed=S(4, 'Question 2 2 + 3 marks'),
         why='p3: what GB and TB stand for; the scheme prints both, 1 each',
         stem=Q2_STEM,
         ask=P(3, 'In terms of storage capacity, what do the letters GB and TB stand for?'),
         rows=[pt(S(4, 'GB: Gigabyte'), 1, note=S(4, 'Each correct item 1 mark', nth=2)),
               pt(S(4, 'TB: Terabyte'), 1)]),
    dict(key=(2, 'b', None), topic='cs-2-3', total=3, printed=S(4, 'Question 2 2 + 3 marks'),
         why='p3: why choose the SSD; the scheme lists four reasons, 3 / 2 / 1',
         stem=Q2_STEM,
         ask=P(3, 'Assuming that neither cost nor capacity were issues', 'rather than the HDD.'),
         rows=[ladder([S(4, 'SSD is smaller, faster, quieter'),
                       S(4, 'SSD has no moving parts', 'better for transportation, etc.'),
                       S(4, 'SSD is completely electronic - consumes less power'),
                       S(4, 'SSD is safe from magnets')], [[1, 2, 3]],
                      note=S(4, 'Very good description - clear understanding demonstrated 3 marks',
                             'Fair description - limited understanding 1 mark'))]),
    dict(key=(3, None, None), topic='cs-2-3', total=5,
         why='p4: the purpose of the program counter; the scheme answers it, 5 / 3 / 1',
         ask=P(4, 'The program counter is a special register', 'purpose of the program counter.'),
         rows=[crit(S(5, 'Contains address of the instruction to be executed in memory or similar'), 5, [1, 3],
                    note=S(5, 'Very good description - clear understanding demonstrated 5 marks',
                           'Fair description - limited understanding 1 mark'))]),
    dict(key=(4, 'a', None), topic='cs-2-3', total=2, printed=S(5, 'Question 4 2 + 3 marks'),
         why='p4: what a protocol is; the scheme gives two forms, any one, 2 / 1',
         stem=Q4_STEM,
         ask=P(4, 'When referring to World Wide Web infrastructure', 'the term protocol?'),
         rows=[ladder([S(5, 'Rules and procedures for network communication or similar'),
                       S(5, 'An agreed way to communicate between two computers/devices/processes')], [[1, 2]],
                      note=S(5, 'Any one of the above points:', 'limited understanding 1 mark'))]),
    dict(key=(4, 'b', None), topic='cs-2-3', total=3, printed=S(5, 'Question 4 2 + 3 marks'),
         why='p4: one protocol, named and its purpose; the scheme prices the name 1 and the '
             'purpose 2 / 1, and tables five protocols with their purposes',
         stem=Q4_STEM,
         ask=P(4, 'State the name and purpose of one such protocol.'),
         rows=[pt(S(5, 'HTTP, HTTPS, TCP, IP, VOIP, or similar', 'Others: Echo, finger, Gopher, POP3, DNS, UDP'), 1,
                  note=S(5, 'Name 1 mark')),
               ladder([Pair(S(5, 'HTTP'), S(5, 'High level protocol used to support the exchange', '(typically HTML)')),
                       Pair(S(5, 'HTTPS'), S(5, 'HTTP + added security layer / encryption-decryption')),
                       Pair(S(5, 'TCP'), S(5, 'Low level protocol', 'orders at the destination')),
                       Pair(S(5, 'IP'), S(5, 'Responsible for the routing of packets', 'inter-connected computers/devices')),
                       Pair(S(5, 'VOIP'), S(5, 'The transmission of voice over IP'))], [[1, 2]],
                      note=S(5, 'Purpose: Good description - clear information 2 marks',
                             'limited understanding 1 mark'))]),
    dict(key=(5, 'a', None), topic='cs-2-3', qfigure='q5-circuit', total=3, printed=S(6, 'Question 5 3 + 2 marks'),
         why='p5: C when A and B are both 0; the scheme answers it, first correct 3',
         stem=Q5_STEM,
         ask=P(5, 'What is the value of C when the inputs A and B are both 0?'),
         rows=[pt(S(6, '0 / False', nth=1), 3, note=Q5_RULE)]),
    dict(key=(5, 'b', None), topic='cs-2-3', qfigure='q5-circuit', total=2, printed=S(6, 'Question 5 3 + 2 marks'),
         why='p5: S when A and B are both 1; the scheme answers it, second correct 2',
         stem=Q5_STEM,
         ask=P(5, 'What is the value of S when the inputs A and B are both 1?'),
         rows=[pt(S(6, '0 / False', nth=2), 2, note=Q5_RULE)]),
    dict(key=(6, 'a', None), topic='cs-2-3', total=3, printed=S(6, 'Question 6 3 + 2 marks'),
         why='p6: why encoding standards matter; the scheme lists three, any one, 3 / 2',
         stem=Q6_STEM,
         ask=P(6, 'Why are encoding standards such as ASCII important?'),
         rows=[ladder([S(6, 'Allows data to be encoded in a standard way'),
                       S(6, 'Provides a means of representing data as information'),
                       S(6, 'Allows for worldwide communication in electronic form or similar')], [[2, 3]],
                      note=S(6, 'Any one of the above points:', 'limited understanding 2 mark'))]),
    dict(key=(6, 'b', None), topic='cs-2-3', total=2, printed=S(6, 'Question 6 3 + 2 marks'),
         why='p6: one limitation of ASCII; the scheme lists four and "and similar", 2 / 1; its '
             'first (2 to the 7 = 128 characters) is read by glyph id',
         stem=Q6_STEM,
         ask=P(6, 'State one limitation of ASCII.'),
         rows=[ladder([G(6, '7 bits so only max of', 'max 256 characters)'),
                       S(6, 'Does not allow for emojis, etc'),
                       S(6, 'Does not support symbols from different languages'),
                       S(6, 'Not enough symbols to support certain languages with large character sets')], [[1, 2]],
                      head=S(6, 'Limitation:'), instruction=S(6, 'And similar'),
                      note=S(6, 'Good description - clear information 2 marks', 'limited understanding 1 mark'))]),
    dict(key=(7, None, None), topic='cs-2-3', qfigure='q7-binary', total=5,
         why='p6: the binary for K in hexadecimal; the scheme answers 4B, 5 / 3 / 1',
         ask=P(6, 'The 8', 'to hexadecimal notation.'),
         rows=[crit(S(6, '4B'), 5, [1, 3], note=S(6, 'Correct 5 marks', 'Response with some merit 1 mark'))]),
    dict(key=(8, None, None), topic='cs-2-2', qfigure='q8-passes', figure='s-q8', total=5,
         why='p7: complete passes 2 to 4 of a bubble sort; the scheme draws the completed '
             'diagram, 1 mark a step, so the check row steps 1 a step under the drawing',
         ask=P(7, 'The diagram below sets out the operation of the bubble sort algorithm', 'only need to fill in the numbers.'),
         rows=[ask_row([1, 2, 3, 4], note=S(7, 'Each correct step 1 mark'))]),
    dict(key=(9, None, None), topic='cs-2-4', qfigure='q9-data', total=5,
         why='p7: three problems with the race data; the scheme lists eight, 2 + 2 + 1',
         ask=P(7, 'The data set below shows the raw data', 'problems with the data in the data set.'),
         rows=[anyn([S(7, 'Repeated record Ogene'), S(7, 'Blank surname'), S(7, 'Dot after F'),
                     S(7, 'Small f'), S(7, 'Negative age'), S(7, '77 age anomaly'), S(7, 'Comma in time'),
                     S(7, 'Space in time, no decimal point')], 3, 2, steps=[2, 2, 1],
                    head=P(7, 'List three problems with the data in the data set.'),
                    note=S(7, 'First two problems 2 marks (each)', 'Third problem 1 mark'))]),
    dict(key=(10, None, None), topic='cs-2-2', qfigure='q10-html', figure='s-q10', total=5,
         why='p8: the four missing pieces of HTML; the scheme tables them, first 2 and each '
             'further 1',
         ask=[P(8, 'The illustrations below show HTML code', 'replaced with the numbers 1 – 4.'),
              P(8, 'Complete the table below with the missing code.')],
         rows=[anyn([S(8, 'html'), S(8, 'Menu'), S(8, 'ul'), S(8, 'href')], 4, 1, steps=[2, 1, 1, 1],
                    head=S(8, 'Number Missing Code'),
                    note=S(8, 'First item correct 2 marks', 'Additional item correct 1 mark'))]),
    dict(key=(11, None, None), topic='cs-2-2', qfigure='q11-code', total=5,
         why='p9: one way to fix the grade function; the scheme gives two and any similar, '
             '5 / 3 / 1',
         ask=P(9, 'The intention of the JavaScript function below', 'so that it works as intended.'),
         rows=[ladder([S(8, 'Change 2nd if to else'), S(8, 'Rearrange code with correct example.')], [[1, 3, 5]],
                      instruction=S(8, 'Similar suitable answer.'),
                      note=S(8, 'Very good description - clear understanding demonstrated 5 marks',
                             'Fair description - limited understanding 1 mark'))]),
    dict(key=(12, None, None), topic='cs-1-1', qfigure='q12-graph', total=5,
         printed=S(8, 'Very good description - clear understanding demonstrated 5 marks', nth=2),
         tariff_note='Section A, twelve questions for 60 marks; the head prints no tariff, the '
                     'top descriptor prints 5',
         why='p10: why heuristics suit the travelling salesperson problem; the scheme gives two '
             'answers, 5 / 3 / 1',
         ask=P(10, 'The travelling salesperson problem is commonly used', 'a problem such as this?'),
         rows=[ladder([S(8, 'Heuristics will find the best approximate solution', 'The best actual solution or similar answer.'),
                       S(8, 'Heuristics is a guess which can be based on previous experience or rule of thumb.')], [[1, 3, 5]],
                      note=S(8, 'Very good description - clear understanding demonstrated 5 marks',
                             'Fair description - limited understanding 1 mark', nth=2))]),
    # ── Section B ──────────────────────────────────────────────────────────
    dict(key=(13, 'a', 'i'), topic='cs-2-2', qfigure='q13-code', total=2,
         why='p11: name the search algorithm; the scheme answers linear search, 2',
         stem=Q13A, ask=P(11, 'State the name of the above search algorithm.'),
         rows=[pt(S(9, 'Linear search'), 2)]),
    dict(key=(13, 'a', 'ii'), topic='cs-2-4', qfigure='q13-code', total=2,
         why='p11: the data type of found; the scheme answers Boolean 2, True / False 1',
         stem=Q13A, ask=P(11, 'What is the data type of the variable called found?'),
         rows=[crit(S(9, 'Boole / Boolean'), 2, [1], note=S(9, 'Boole / Boolean (2 marks)', 'True / False (1 mark)'))]),
    dict(key=(13, 'a', 'iii'), topic='cs-2-2', qfigure='q13-code', total=5,
         why='p12: step through the search for Zoe; the scheme steps through it, 5 / 3 / 1',
         stem=Q13A, ask=P(12, 'Step through how the algorithm finds the name Zoe in the list called names.'),
         rows=[crit(S(9, 'Starts at index 0', 'Or any similar relevant explanation.'), 5, [1, 3],
                    note=S(9, 'Very good description - clear understanding demonstrated 5 marks',
                           'Fair description - limited understanding 1 mark'))]),
    dict(key=(13, 'a', 'iv'), topic='cs-2-2', qfigure='q13-code', total=2,
         why='p12: index after a name not in the list; the scheme answers 5, 2',
         stem=Q13A, ask=P(12, 'What would be the value of index after running the algorithm', 'in the list called names?'),
         rows=[pt(S(9, 'Index = 5'), 2)]),
    dict(key=(13, 'a', 'v'), topic='cs-2-2', qfigure='q13-code', total=3,
         why='p12: the worst-case complexity and why; the scheme prices the answer 1 and the '
             'explanation 2 / 1',
         stem=Q13A, ask=P(12, 'What is the worst', 'Explain your answer.'),
         rows=[pt(S(10, 'Worst case: O(n) / length of list'), 1, note=S(10, 'Answer 1 mark')),
               crit(S(10, 'Worst case would mean that the item is not in the list', 'comparisons -> worst case.'), 2, [1],
                    note=S(10, 'Explanation: Good description - clear information 2 marks',
                           'limited understanding 1 mark'))]),
    dict(key=(13, 'b', 'i'), topic='cs-2-2', total=2,
         why='p13: one disadvantage of binary search; the scheme lists five and any similar, 2',
         stem=Q13B, ask=P(13, 'State one disadvantage of the binary search algorithm.'),
         rows=[anyn([S(10, 'The data set being searched must be sorted and remain sorted.'),
                     S(10, 'Can be slower than linear search', 'search is O(n/2).'),
                     S(10, 'More complicated than linear search and unnecessary for small data sets.'),
                     S(10, 'Only works on data with a “less-than” relationship.'),
                     S(10, 'Data has to be of the same type.'), S(10, 'Or similar answer.')], 1, 2, open_list=True,
                    head=P(13, 'State one disadvantage of the binary search algorithm.'),
                    note=S(10, 'Any suitable answer 2 marks'))]),
    dict(key=(13, 'b', 'ii'), topic='cs-2-2', qfigure='q13b-list', figure='s-q13b-ii', total=5,
         why='p13: step through a binary search for 28; the scheme steps through it and prints '
             'an alternative trace, 5 / 3 / 1',
         stem=Q13B, ask=P(13, 'Step through how the binary search algorithm finds the integer 28', 'list L shown below.'),
         rows=[crit(S(10, '1. Compares 28 to the value in mid (18).', 'Similar explanations acceptable.'), 5, [1, 3],
                    note=S(11, 'Very good description - clear understanding demonstrated 5 marks',
                           'Fair description - limited understanding 1 mark'))]),
    dict(key=(13, 'b', 'iii'), topic='cs-2-2', total=2,
         why='p14: most comparisons for a missing value in 8 items; the scheme answers 4, 2 / 1',
         stem=Q13B, ask=P(14, 'What is the maximum number of comparisons', 'in a list of 8 items?'),
         rows=[crit(S(11, '4'), 2, [1], note=S(11, 'Correct answer 2 marks', 'Any relevant roughwork 1 mark'))]),
    dict(key=(13, 'c', None), topic='cs-2-2', total=7,
         why='p15: why algorithmic efficiency matters; the scheme answers it, 7 / 5 / 3',
         stem=Q13_STEM, ask=P(15, 'Why is the study of algorithmic efficiency considered to be important in computer science?'),
         rows=[crit(S(11, 'It is important to understand the time and efficiency', 'use least amount of memory.'), 7, [3, 5],
                    note=S(11, 'Very good description - clear understanding demonstrated 7 marks',
                           'Fair description - limited understanding 3 marks'))]),
    dict(key=(14, 'a', None), topic='cs-1-2', total=4,
         why='p16: the importance of Turing Machines; the scheme answers it, 4 / 3 / 2',
         stem=Q14_STEM, ask=P(16, 'Explain the importance of Turing Machines as a computational tool.'),
         rows=[crit(S(12, 'Can compute anything that is possible to be computed or any similar explanation.'), 4, [2, 3],
                    note=S(12, 'Very good description - clear understanding demonstrated 4 marks',
                           'Fair description - limited understanding 2 mark'))]),
    dict(key=(14, 'b', 'i'), topic='cs-1-2', qfigure='q14-fsm', total=2,
         why='p16: the significance of state S2; the scheme gives three and any similar, 2 / 1',
         stem=Q14B, ask=P(16, 'What is the significance of state S2?'),
         rows=[ladder([S(12, 'S2 is the end/final/halt state.'), S(12, 'The FSM is finished computing.'),
                       S(12, 'The problem is computable if it reaches this state (deterministic).')], [[1, 2]],
                      instruction=S(12, 'Any similar explanation.'),
                      note=S(12, 'Good explanation - clear information 2 marks', 'Fair explanation - limited understanding 1 mark'))]),
    dict(key=(14, 'b', 'ii'), topic='cs-1-2', qfigure='q14-table', total=2,
         why='p16: the two blank rows of the transition table; the scheme prints them, 1 a row',
         stem=Q14B, ask=P(16, 'Complete the state transition table below', 'The first row has already been completed.'),
         rows=[pt(S(12, 'S1 1 1 S1'), 1, note=S(12, 'Each correct row 1 mark', '(rows can be in any order)')),
               pt(S(12, 'S1 B 0 S2'), 1)]),
    dict(key=(14, 'b', 'iii'), topic='cs-1-2', qfigure='q14-tape', figure='s-q14b-iii', total=4,
         why='p17: trace 10110B on the tape; the scheme draws the completed tape, 1 a row, so the '
             'check row steps 1 a row under the drawing',
         stem=Q14B, ask=P(17, 'Starting from an initial state of S1', 'The first two rows have been completed for you.'),
         rows=[ask_row([1, 2, 3], note=S(13, 'Each correct row 1 mark'))]),
    dict(key=(14, 'c', None), topic='cs-1-2', total=8,
         why='p18: positive and negative effects of AI; the scheme lists six of each, two of '
             'each at 2 / 1',
         stem=P(18, 'In the mid', 'posed by artificial intelligence”.'),
         ask=P(18, 'Discuss the quotation above', 'negative effects of AI on society.'),
         rows=[ladder([S(14, 'Positive impact on human life', 'predicting weather, etc.'),
                       S(14, 'Improving daily life', 'shopping suggestions, etc.'),
                       S(14, 'Analysing large datasets', 'that humans could not do.'),
                       S(14, 'Always available, no emotional decisions, faster decisions, more accuracy.'),
                       S(14, 'New inventions, solutions or ideas that humans may not think of.')], [[1, 2], [1, 2]],
                      head=S(14, 'Positives:'), instruction=S(14, 'Any similar suitable answer.', nth=1),
                      note=S(14, 'Mark 2 best points for positive and 2 best points for negative.',
                             'Fair description - limited understanding 1 marks')),
               ladder([S(14, 'Data privacy issues and potential misuse', 'existing datasets.'),
                       S(14, 'Ethical issues', 'drones in war.'),
                       S(14, 'Unemployment', 'replace humans in jobs.'),
                       S(14, 'No innovation or creativity', 'on which it is based.'),
                       S(14, 'Risk of creating sentient machines that develop a conscience.')], [[1, 2], [1, 2]],
                      head=S(14, 'Negatives:'), instruction=S(14, 'Any similar suitable answer.', nth=2),
                      note=S(14, 'For each of the 4 points', 'Fair description - limited understanding 1 marks'))]),
    dict(key=(15, 'a', None), topic='cs-1-3', total=4,
         why='p20: staged or iterative, with two reasons; the scheme gives example reasons for '
             'each, 2 / 1 a reason',
         stem=Q15_STEM,
         ask=P(20, 'State whether you would use a staged or iterative development process', 'two reasons for your decision.'),
         rows=[crit(S(15, 'Any suitable reasons that demonstrate understanding.', 'easy to understand and use.'), 4, [],
                    parts=[(P(20, 'Reason 1:'), 2, [1]), (P(20, 'Reason 2:'), 2, [1])],
                    note=S(15, 'For each reason:', 'limited understanding 1 mark'))]),
    dict(key=(15, 'b', None), topic='cs-1-3', total=8,
         why='p21: two roles with two responsibilities each; the scheme tables five roles, 2 '
             'for the role and 1 for each responsibility',
         stem=Q15_STEM,
         ask=P(21, 'As project manager one of your main tasks', 'responsibilities associated with that role.'),
         rows=[ladder([Pair(T(15, 'Project Manager (Leader/Team Leader)'), T(15, 'Planning, monitoring, resourcing, communication')),
                       Pair(T(15, 'Analyst'), T(15, 'Understands the problem and define the system scope')),
                       Pair(T(15, 'Designer'), T(15, 'Creates a representation of the system using tools and algorithms')),
                       Pair(T(15, 'Programmer / Developer / Coder / Software Engineer'),
                            T(15, 'Implements design – writes the programs – unit test')),
                       Pair(T(15, 'Testers/Testing'), T(15, 'Determines whether the system works as intended'))],
                      [[1, 2, 3, 4], [1, 2, 3, 4]], instruction=T(15, 'Any similar role'),
                      note=S(15, 'For each role: Any relevant role 2 marks', '1 mark for each'))]),
    dict(key=(15, 'c', 'i'), topic='cs-1-3', qfigure='q15-ui', total=6,
         why='p22: compare the two interfaces; the scheme prices the type of application 2 / 1 '
             'and two points of functionality 2 / 1 each',
         stem=Q15C,
         ask=P(22, 'Compare the two interfaces in terms of the types of applications', 'functionality they offer.'),
         rows=[crit(S(16, 'The game shown in UI1 looks like a web application', 'desktop or laptop device.'), 2, [1],
                    head=S(16, 'Type of application:'),
                    note=S(16, 'Good comparison - clear information, good understanding 2 marks',
                           'Fair comparison - limited understanding 1 mark')),
               ladder([S(16, 'Social media integration (Facebook and Twitter).'),
                       S(16, 'Ability to set and play at different levels', 'veteran level).'),
                       S(16, 'A log of the result history', 'result of the most recent game).'),
                       S(16, 'A display of the number of draws (ties).'),
                       S(16, 'UI 1 is more user friendly', 'twice as many clicks).')], [[1, 2], [1, 2]],
                      head=S(16, 'The basic functionality offered by both examples', 'the following additional functionality:'),
                      note=S(16, 'Mark 2 best points for comparison of functionality.',
                             'Fair comparison - limited understanding 1 mark'))]),
    dict(key=(15, 'c', 'ii'), topic='cs-1-2', total=2,
         why='p24: two examples of adaptive technology in the game; the scheme lists four, 1 each',
         stem=Q15_STEM,
         ask=P(24, 'Provide two examples of how adaptive technology', 'a game of Rock Paper Scissors.'),
         rows=[anyn([S(16, 'voice recognition'), S(16, 'hand gestures'), S(16, 'touch screen interface'),
                     S(16, 'VR/AR (virtual reality/augmented reality)')], 2, 1, open_list=True,
                    head=S(16, 'Possible answers'),
                    note=S(16, 'For each relevant example 1 mark'))]),
    # ── Section C ──────────────────────────────────────────────────────────
    dict(key=(16, 'a', 'i'), topic='cs-2-2', qfigure='q16a-code', figure='s-q16a-i', total=5,
         why='040 p5: a comment to initialise score; the scheme marks line 32 Ans (i), A-5 scale',
         stem=Q16A_STEM,
         ask=C(5, 'Insert a comment to say', 'in an appropriate location in the program.'),
         rows=[crit(S(19, CORRECT), 5, [2, 3],
                    note=S(19, '(i) 5 marks (A-5 scale)', 'Any reasonable attempt at inserting a comment.'))]),
    dict(key=(16, 'a', 'ii'), topic='cs-2-2', qfigure='q16a-code', figure='s-q16a-ii', total=5,
         why='040 p5: print the password and score on two lines; the scheme marks lines 74-76 '
             'Ans (ii), B-5 scale',
         stem=Q16A_STEM,
         ask=C(5, 'Amend the program so that is displays two lines of output', 'Score: 6', end_nth=1),
         rows=[crit(S(19, CORRECT), 5, [2, 3, 4],
                    note=S(19, '(ii) 5 marks (B-5 scale)', 'Attempted use of print or similar.'))]),
    dict(key=(16, 'a', 'iii'), topic='cs-2-2', qfigure='q16a-code', figure='s-q16a-iii', total=5,
         why='040 p5: replace the hard-coded uppercase string with UPPER_CASE_LETTERS; the '
             'scheme marks lines 10 and 24 Ans (iii), B-5 scale',
         stem=Q16A_STEM,
         ask=C(5, 'Currently in the program, the uppercase letters are hard', 'name the variable UPPER_CASE_LETTERS.'),
         rows=[crit(S(19, CORRECT), 5, [2, 3, 4],
                    note=S(19, '(iii) 5 marks (B-5 scale)', 'relevant attempt at changing if statement.'))]),
    dict(key=(16, 'a', 'iv'), topic='cs-2-2', qfigure='q16a-code', figure='s-q16a-iv', total=5,
         why='040 p5: rule 4, 2 points for an uppercase letter; the scheme marks lines 51-53 '
             'Ans (iv), B-5 scale',
         stem=Q16A_STEM,
         ask=C(5, 'Implement a new rule (rule 4)', 'Score: 13'),
         rows=[crit(S(20, CORRECT), 5, [2, 3, 4],
                    note=S(20, '(iv) 5 marks (B-5 scale)', 'but not inside conditional statement or similar.'))]),
    dict(key=(16, 'a', 'v'), topic='cs-2-2', qfigure='q16a-code', figure='s-q16a-v', total=10,
         why='040 p5: rule 5, 5 points for a digit; the scheme marks lines 11, 17, 26-27 and '
             '55-57 Ans (v), C-10 scale',
         stem=Q16A_STEM,
         ask=C(5, 'Implement a new rule (rule 5)', 'Score: 18'),
         rows=[crit(S(20, CORRECT, nth=2), 10, [2, 4, 6, 8],
                    note=S(20, '(v) 10 marks (C-10 scale)', 'no attempt to set or test flag.'))]),
    dict(key=(16, 'a', 'vi'), topic='cs-2-2', qfigure='q16a-code', figure='s-q16a-vi', total=5,
         why='040 p6: rule 6, points for a digit first, last or both; the scheme marks lines '
             '59-65 Ans (vi), B-5 scale',
         stem=Q16A_STEM,
         ask=C(6, 'Implement a new rule (rule 6)', 'Score: 22', end_nth=1),
         rows=[crit(S(21, OPTIMAL), 5, [2, 3, 4],
                    note=S(21, '(vi) 5 marks (B-5 scale)', 'Value of the score changed correctly.'))]),
    dict(key=(16, 'a', 'vii'), topic='cs-2-2', qfigure='q16a-code', figure='s-q16a-vii', total=5,
         why='040 p6: rule 7, minus 10 for a password of digits only; the scheme marks lines '
             '67-69 Ans (vii), B-5 scale',
         stem=Q16A_STEM,
         ask=C(6, 'Implement a new rule (rule 7)', 'Score: -1'),
         rows=[crit(S(21, CORRECT), 5, [2, 3, 4],
                    note=S(21, '(vii) 5 marks (B-5 scale)', 'Value of the score changed correctly.'))]),
    dict(key=(16, 'a', 'viii'), topic='cs-2-2', qfigure='q16a-viii', figure='s-q16a-viii', total=10,
         why='040 p6: rule 1 by password length; the scheme marks lines 35-41 Ans (viii), C-10 '
             'scale',
         stem=Q16A_STEM,
         ask=[C(6, 'Change rule 1 so that the score is adjusted', 'as shown in the following table.'),
              C(6, 'The table below shows the scores', 'to test your program.')],
         rows=[crit(S(22, OPTIMAL), 10, [2, 4, 6, 8],
                    note=S(22, '(viii) 10 marks (C-10 scale)', 'Value of the score changed correctly.'))]),
    dict(key=(16, 'b', 'i'), topic='cs-2-2', qfigure='q16b-code', figure='s-q16b-i', total=5,
         why='040 p9: print a Score / Password table; the scheme marks lines 78, 79 and 87 Ans '
             '(i), B-5 scale',
         stem=Q16B_STEM,
         ask=C(9, 'Amend the program so that the output is displayed in the following format:', '5 123456789'),
         rows=[crit(S(25, CORRECT), 5, [2, 3, 4],
                    note=S(25, '(i) 5 marks (B-5 scale)', 'Attempt at using print statement or similar.'))]),
    dict(key=(16, 'b', 'ii'), topic='cs-2-2', qfigure='q16b-code', figure='s-q16b-ii', total=5,
         why='040 p9: change the password at index 4 to Moonlight; the scheme marks line 76 Ans '
             '(ii), B-5 scale',
         stem=Q16B_STEM,
         ask=C(9, 'Insert a line of code to change the password', '11 Moonlight', end_nth=1),
         rows=[crit(S(25, CORRECT, nth=2), 5, [2, 3, 4],
                    note=S(25, '(ii) 5 marks (B-5 scale)', 'Hard-coded change of the password in the list.'))]),
    dict(key=(16, 'b', 'iii'), topic='cs-2-2', qfigure='q16b-code', figure='s-q16b-iii', total=5,
         why='040 p9: find and display the weakest password; the scheme marks lines 80-91 Ans '
             '(iii), B-5 scale',
         stem=Q16B_STEM,
         ask=C(9, 'Amend the program so that it determines and displays the weakest password', 'Score: 0'),
         rows=[crit(S(26, CORRECT), 5, [2, 3, 4],
                    note=S(26, '(iii) 5 marks (B-5 scale)', 'Attempt at sorting list of scores.'))]),
    dict(key=(16, 'b', 'iv'), topic='cs-2-2', qfigure='q16b-code', figure='s-q16b-iv', total=10,
         why='040 p10: a function is_strong; the scheme gives three versions, lines 7-38 Ans '
             '(iv), C-10 scale',
         stem=Q16B_STEM,
         ask=C(10, 'Write a function definition called is_strong', 'def is_strong(password):'),
         rows=[crit(S(26, CORRECT, nth=2), 10, [2, 4, 6, 8],
                    note=S(26, '(iv) 10 marks (C-10 scale)', 'at an appropriate location in the program).'))]),
    dict(key=(16, 'b', 'v'), topic='cs-2-2', qfigure='q16b-code', figure='s-q16b-v', total=5,
         why='040 p10: display the strong passwords with is_strong; the scheme marks lines '
             '93-100 Ans (v), B-5 scale',
         stem=Q16B_STEM,
         ask=C(10, 'Modify the program so that it calls the function is_strong', 'Sunshine Moonlight'),
         rows=[crit(S(27, CORRECT), 5, [2, 3, 4],
                    note=S(27, '(v) 5 marks (B-5 scale)', 'Use of print statement.'))]),
]
