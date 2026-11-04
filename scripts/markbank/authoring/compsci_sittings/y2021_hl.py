"""Computer Science 2021 Higher Level: the 9 printed asks the bank did not hold.

54 of the sitting's 63 asks are covered by the cards shipped in August; these
9 complete it. Paper pages 7, 12-17 and scheme pages 7, 10-15 were opened.
Q13(a)'s three asks are Eircodes the candidate must say are invalid; each is
carded with the paper's instruction and its own code.
"""
from compsci_lane import (P, S, anyn, crit, crop, pt, stack)  # noqa: F401

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
}

Q12_TARIFF = S(10, 'Question 12 2+3 marks')
Q13_STEM = P(13, 'Eircode is the postal address code system', 'is shown below in Figure 4.')
Q13A = P(13, 'Explain why each of the following are not valid Eircodes.')
Q13C = P(16, 'The following questions are based on the code in part (b).')

CARDS = [
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
    dict(key=(13, 'c', 'iv'), topic='cs-2-3', qfigure='q13c-iv', total=1,
         why='p17: line 16 rewritten from the truth tables; the scheme prints two forms, 1 mark',
         stem=Q13C,
         ask=P(17, 'Use your findings from parts (ii) and (iii)', 'without changing its logical meaning.'),
         rows=[anyn([S(15, 'if not (test_eircode[1].isdigit() and test_eircode[2].isdigit()):'),
                     S(15, 'if not (P and Q):')], 1, 1,
                    head=P(17, 'Use your findings from parts (ii) and (iii)', 'without changing its logical meaning.'),
                    note=S(15, 'Correct response 1 mark', nth=1))]),
]
