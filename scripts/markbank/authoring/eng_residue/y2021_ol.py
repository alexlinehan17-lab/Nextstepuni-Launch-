"""2021 Ordinary Level: the parts eng_all refuses or gets wrong, from the page.

Paper LC027GLP000EV; scheme pages as the PDF numbers them (its footer reads
one lower). The marks grid on scheme p3 prices every part; Question 1 is
"Any eight. Two @ 7 marks, six @ 6 marks. (Two-part answers @ 4(3) + 3
marks)". Every Question 1 card carries the printed primary price, 7 (two-part
answers 4 + 3), and says that a part marked at the bracketed price earns 6
(3 + 3): a student cannot know in advance which price a part will be marked
at, and the scheme leads with the primary one (PRIMARY, below, for the cards
the automatic author builds).

The scheme sets Question 1's answers (g) and (h) in the opposite order to the
paper: its "(g)" answers the paper's (h), the electronic component, and its
"(h)" the paper's (g). The shipped (g) card already pairs by content.
"""
from eng_lift import join, lift

Y, L = 2021, 'ol'


def S(page, *rect):
    return lift(Y, L, 'scheme', page, rect)


def P(page, *rect, more=(), items=()):
    return lift(Y, L, 'paper', page, rect, more=more, items=items)


Q1_PRICE = ("Question 1 is 'Any eight. Two @ 7 marks, six @ 6 marks': the card carries "
            "the printed price, 7 (two-part answers 4 + 3); a part marked at the bracketed "
            "price earns 6 (3 + 3).")
Q1_NOTE = "The scheme prints '4 (3) + 3 Marks'. " + Q1_PRICE

CROPS = {
    # Paper p2: the LED and its caption "electronic component".
    'engineering-2021-OL-paper-q1h-crop': dict(
        doc='paper', page=2, rect=(484, 327, 552, 438), ref='2021 OL Q1(h)'),
    # Paper p2: the three pictures (i) names and their captions.
    'engineering-2021-OL-paper-q1i-crop': dict(
        doc='paper', page=2, rect=(60, 444, 530, 548), ref='2021 OL Q1(i)'),
    # Paper p2: the chuck key, captioned "component B". Q1(l)'s last option,
    # "Swarf.", ends inside the box above the key and is whited out.
    'engineering-2021-OL-paper-q1m-crop': dict(
        doc='paper', page=2, rect=(340, 712, 510, 792), mask=[(346, 710, 392, 728)],
        ref='2021 OL Q1(m)',
        letters=('B',)),
    # Paper p3: the three furnaces lettered A, B and C.
    'engineering-2021-OL-paper-q2a-crop': dict(
        doc='paper', page=3, rect=(80, 78, 498, 222), ref='2021 OL Q2(a)',
        letters=('A', 'B', 'C')),
    # Paper p3: the wheelchair with its three labelled parts.
    'engineering-2021-OL-paper-q2c-crop': dict(
        doc='paper', page=3, rect=(28, 436, 312, 618), ref='2021 OL Q2(c)'),
    # Paper p5: the tap wrench captioned "tool B".
    'engineering-2021-OL-paper-q4ci-crop': dict(
        doc='paper', page=5, rect=(383, 470, 558, 524), ref='2021 OL Q4(c)(i)',
        letters=('B',)),
    # Paper p6: the three plastic processes drawn and lettered A, B, C.
    'engineering-2021-OL-paper-q5a-crop': dict(
        doc='paper', page=6, rect=(35, 68, 565, 225), ref='2021 OL Q5(a)(i)',
        letters=('A', 'B', 'C')),
    # Paper p7: the four lathe parts captioned (i)-(iv). The ask's own line
    # runs into the top of the box beside the two right-hand photographs, so
    # it is whited out.
    'engineering-2021-OL-paper-q6a-crop': dict(
        doc='paper', page=7, rect=(35, 68, 565, 224), mask=[(35, 66, 330, 86)],
        ref='2021 OL Q6(a)'),
    # Paper p8: the gear and shaft with both dimensions.
    'engineering-2021-OL-paper-q7b-crop': dict(
        doc='paper', page=8, rect=(331, 178, 575, 372), ref='2021 OL Q7(b)'),
    # Paper p8: the four instruments captioned (i)-(iv).
    'engineering-2021-OL-paper-q7c-crop': dict(
        doc='paper', page=8, rect=(25, 427, 570, 612), ref='2021 OL Q7(c)'),
    # Paper p8: the model eRacer (the OR branch of (c)).
    'engineering-2021-OL-paper-q7ci-crop': dict(
        doc='paper', page=8, rect=(362, 646, 566, 800), ref='2021 OL Q7(c)(i)'),
    # Scheme pp9-10: the labelled diagram the scheme prints for each furnace.
    'engineering-2021-OL-scheme-q2bi-sol': dict(
        doc='scheme', solution=True, ref='2021 OL Q2(b)(i)', layout='row',
        parts=[(9, (22, 262, 254, 488)), (9, (40, 515, 254, 770)),
               (10, (40, 72, 262, 326))]),
    # Scheme p22: the motor and switch symbols.
    'engineering-2021-OL-scheme-q7cii-sol': dict(
        doc='scheme', page=22, rect=(70, 156, 350, 274), solution=True,
        ref='2021 OL Q7(c)(ii)'),
}

_FURNACE = ('The scheme answers for whichever furnace was chosen: A, the basic '
            'oxygen furnace, first; then B, the blast furnace; then C, the '
            'electric arc furnace.')
_Q2B = ('Q2(b) asks about one furnace of the candidate\'s choice, and scheme '
        'pp8-9 answer all three in turn, each with its own (i), (ii) and '
        '(iii); the reader files every furnace\'s answer under one key and '
        'welds the diagrams\' callouts into the materials and heating lines.')

CARDS = [
    dict(key=(1, 'e', None),
         why='Tool A is an adjustable spanner, which names no syllabus topic; '
             'loosening and tightening nuts and bolts is mechanical fastening, '
             'under Joining. The scheme answers the name and the use on two '
             'lines and the reader kept the use alone.',
         topic='eng-2-10',
         lifted=[S(4, 50, 530, 440, 546), S(4, 50, 546, 380, 560)],
         marks=[4, 3], total=7, figure='engineering-2021-OL-paper-q1e-art',
         labels={'A': S(4, 119, 530, 220, 547)}, notes=Q1_NOTE),
    dict(key=(1, 'h', None),
         why='The LED is photographed beside (h) with the caption "electronic '
             'component"; the automatic crop for this row took in the '
             'neighbouring parts\' pictures (eng_figures REJECTED). Scheme p4 '
             'answers it under "(g)".',
         lifted=[S(4, 50, 632, 425, 648), S(4, 50, 661, 440, 692)],
         marks=[4, 3], total=7,
         question_figure='engineering-2021-OL-paper-q1h-crop',
         notes=Q1_NOTE + ' The scheme sets this answer as "(g)".'),
    dict(key=(1, 'm', None),
         why='Component B is the chuck key photographed and captioned on p2; '
             '"component B" names no syllabus topic. Scheme p8 prices the name '
             '"Award 4 (3) Marks" and the function "Award 3 Marks".',
         topic='eng-2-11',
         lifted=[S(8, 70, 528, 300, 546), S(8, 70, 572, 300, 633)],
         marks=[4, 3], total=7, figure='engineering-2021-OL-paper-q1m-crop',
         labels={'B': S(8, 70, 530, 130, 546)}, notes=Q1_NOTE),
    dict(key=(1, 'i', None),
         replaces='the shipped question read "any one of the following: '
                  'electronic component Air compressor Strip heater Three-jaw '
                  'chuck." -- (h)\'s caption swept into the list -- and its '
                  'fourth marking point was the chuck diagram\'s label "Jaw 1"; the '
                  'any-one choice is one row at the printed 7, not a question total',
         why='Paper p2 sets the ask on one line and the three choices as '
             'captions under their pictures; "electronic component" is the '
             'LED\'s caption, beside the ask. Scheme pp5-6 describe each '
             'choice, "Award 7 (6) Marks". Each caption is lifted on its own '
             'line, as the paper sets them.',
         question_lift=P(2, 70, 425, 400, 443, items=[(70, 530, 155, 548), (260, 530, 330, 548),
                                                 (430, 530, 525, 548)]),
         lifted=[[S(5, 68, 121, 456, 254), S(5, 68, 413, 456, 531),
                  S(6, 68, 87, 456, 220)]],
         row_kind='anyN', group=(1, 7), marks=[7], tariff='fixed', total=7,
         question_figure='engineering-2021-OL-paper-q1i-crop',
         notes="The scheme prints 'Award 7 (6) Marks', for any one. " + Q1_PRICE),
    dict(key=(1, 'f', None), topic='eng-1-4',
         replaces='the shipped card set both halves of "4 (3) + 3 Marks" as one row, "Steel '
                  'is a ferrous metal. (ii) Brass is a non-ferrous metal.", at 6',
         why='Scheme p4 answers both halves on one line, "(i)" and "(ii)"; each is lifted by '
             'its own word rectangle, at the printed 4 + 3.',
         lifted=[S(4, 58, 589, 190, 605), S(4, 188, 589, 348, 605)],
         marks=[4, 3], total=7, notes=Q1_NOTE),
    dict(key=(1, 'j', None), topic='eng-3-14',
         replaces='the shipped card set the three choices of "Describe any one" as four rows '
                  'of a question total at 6 -- laser cutting split in two -- so no choice '
                  'could be claimed',
         why='Scheme pp6-7 describe each choice under its name, "Any one", "Award 7 (6) '
             'Marks"; each option is the choice\'s heading with its description.',
         lifted=[[join(S(6, 68, 470, 140, 486), S(6, 68, 485, 455, 590)),
                  S(7, 68, 87, 275, 206), S(7, 68, 248, 455, 411)]],
         row_kind='anyN', group=(1, 7), marks=[7], tariff='fixed', total=7,
         notes="The scheme prints 'Explain Award 7 (6) Marks', for any one. " + Q1_PRICE),
    dict(key=(1, 'l', None), topic='eng-2-11',
         replaces='the shipped card set the three choices of "Explain any one" as rows of a '
                  'question total at 6, so no choice could be claimed',
         why='Scheme p8 explains each choice under its name, "Any one", "7 (6) Marks"; each '
             'option is the choice\'s heading with its explanation.',
         lifted=[[S(8, 70, 98, 297, 181), S(8, 70, 244, 297, 344),
                  S(8, 70, 377, 297, 431)]],
         row_kind='anyN', group=(1, 7), marks=[7], tariff='fixed', total=7,
         notes="The scheme prints 'Explain 7 (6) Marks', for any one. " + Q1_PRICE),
    dict(key=(2, 'a', None),
         why='Scheme p9 answers the three furnaces on three lines and the '
             'reader welds them into one; the grid prices "Three parts @ 3 '
             'marks, Three parts @ 2 marks (15)" -- the name and the function '
             'of each furnace.',
         lifted=[S(9, 50, 118, 450, 132), S(9, 50, 133, 450, 147),
                 S(9, 50, 147, 450, 162)],
         marks=[5, 5, 5], total=15, figure='engineering-2021-OL-paper-q2a-crop',
         labels={'A': S(9, 130, 118, 245, 132), 'B': S(9, 130, 133, 245, 147),
                 'C': S(9, 130, 147, 245, 162)},
         notes="The scheme prints 'Name Award 3 @ 3 Marks, Function Award 3 @ 2 "
               "Marks'."),
    dict(key=(2, 'b', 'i'),
         why=_Q2B + ' (i) is answered with a labelled diagram of each furnace.',
         special={'kind': 'ask'}, total=6,
         question_lift=P(3, 90, 224, 530, 260, more=[(90, 268, 305, 286)]),
         question_figure='engineering-2021-OL-paper-q2a-crop',
         figure='engineering-2021-OL-scheme-q2bi-sol',
         checked='paper page 3: "(b) Select one of the furnaces shown at Q2(a) '
                 'above and, with the aid of a suitable diagram, answer each of '
                 'the following:" over "(i) Label the main parts of the '
                 'furnace;" -- the semicolon is the list running on',
         notes=_FURNACE),
    dict(key=(2, 'b', 'ii'),
         why=_Q2B,
         lifted=[[S(9, 258, 338, 452, 369), S(9, 258, 573, 452, 589),
                  S(10, 262, 140, 440, 156)]],
         marks=[3], total=3,
         question_lift=P(3, 90, 224, 530, 260, more=[(90, 291, 305, 308)]),
         question_figure='engineering-2021-OL-paper-q2a-crop',
         checked='paper page 3: "(ii) List the materials used in the charge;" '
                 'the second of (b)\'s three, the semicolon running the list on',
         context=_FURNACE),
    dict(key=(2, 'b', 'iii'),
         why=_Q2B,
         lifted=[[S(9, 258, 401, 452, 480), S(9, 258, 635, 452, 714),
                  S(10, 262, 202, 448, 281)]],
         marks=[3], total=3,
         question_lift=P(3, 90, 224, 530, 260, more=[(90, 313, 300, 331)]),
         question_figure='engineering-2021-OL-paper-q2a-crop',
         context=_FURNACE),
    dict(key=(2, 'c', 'i'),
         why='The wheelchair\'s three callouts are set around the photograph '
             'and the automatic crop clipped them (eng_figures REJECTED). '
             'Scheme p10 answers each part with a material and a reason; the '
             'grid prices the materials "Three parts @ 3 marks".',
         lifted=[S(10, 88, 388, 300, 417), S(10, 88, 458, 300, 488),
                 S(10, 88, 530, 360, 560)],
         marks=[3, 3, 3], total=9,
         question_figure='engineering-2021-OL-paper-q2c-crop'),
    dict(key=(2, 'c', 'ii'),
         why='The same table; the grid prices the reasons "Three parts @ 2 '
             'marks". Each row carries the part and material the reason is for.',
         lifted=[S(10, 88, 388, 300, 432), S(10, 88, 458, 300, 503),
                 S(10, 88, 530, 360, 575)],
         marks=[2, 2, 2], total=6,
         question_figure='engineering-2021-OL-paper-q2c-crop'),
    dict(key=(4, 'a', 'i'), topic='eng-2-10',
         replaces='the shipped question carried the three conditions\' bullets as '
                  'font glyphs (U+F0B7) run into one line, and the three flame names '
                  'were one row under a question total of 9, so no name could be '
                  'claimed alone',
         why='Paper p5 sets the three gas conditions as a bulleted list under the '
             'ask; scheme p14 names the flame for each on its own line, "Flame names '
             'Award 3 @ 3 Marks", and the grid prices them "Three parts @ 3 marks". '
             'The question is lifted without the bullets\' glyphs, each condition on '
             'its own line as printed.',
         question_lift=P(5, 110, 70, 560, 86, items=[(130, 94, 400, 112),
                                                     (130, 110, 400, 128),
                                                     (130, 126, 400, 145)]),
         lifted=[S(14, 70, 163, 300, 180), S(14, 70, 178, 300, 195),
                 S(14, 70, 193, 300, 210)],
         marks=[3, 3, 3], total=9,
         notes="The scheme prints 'Flame names Award 3 @ 3 Marks'."),
    dict(key=(4, 'c', 'i'),
         why='Tool B is the tap wrench photographed and captioned on p5; '
             'priced by the grid\'s "Three parts @ 5 marks".',
         topic='eng-2-11',
         use=[0], marks=[5], total=5, figure='engineering-2021-OL-paper-q4ci-crop',
         labels={'B': S(15, 120, 146, 200, 162)}),
    dict(key=(5, 'a', 'i'),
         why='The three processes are drawn and lettered across the top of '
             'p6; scheme p16 answers "A: Vacuum forming B: Injection moulding C: '
             'Blow moulding", "Award 2 @ 5 Marks".',
         lifted=[[S(16, 80, 154, 230, 170), S(16, 80, 183, 230, 199),
                  S(16, 80, 212, 230, 228)]],
         row_kind='anyN', group=(2, 5), marks=[10], tariff='fixed', total=10,
         figure='engineering-2021-OL-paper-q5a-crop',
         labels={'A': S(16, 110, 154, 230, 170), 'B': S(16, 110, 183, 230, 199),
                 'C': S(16, 110, 212, 230, 228)},
         notes="The scheme prints 'Two parts @ 5 marks'."),
    dict(key=(6, 'a', None),
         why='The four lathe parts are photographs captioned (i)-(iv) with no '
             'words of their own. Scheme p19 names and describes each; "Award 1 '
             '@ 6 Marks, Award 2 @ 5 Marks".',
         lifted=[S(19, 100, 118, 450, 165), S(19, 100, 177, 450, 223),
                 S(19, 100, 236, 450, 282), S(19, 100, 294, 450, 326)],
         tariff='orderedSplit',
         notation='One part @ 6 marks; Two parts @ 5 marks (16)', ladder=16,
         question_figure='engineering-2021-OL-paper-q6a-crop'),
    dict(key=(7, 'b', 'i'),
         topic='eng-3-12',
         checked='paper page 8: (b) reads "A hole and shaft assembly is manufactured to the dimensions shown." over "State the: (i) Nominal diameter of the hole;", (ii), (iii) and (iv) beneath it; each closes on a semicolon because the list runs on, and (iv) on a full stop',
         why='The page is a raster with a drawn gear and shaft; the automatic '
             'crop clipped the arrows and labels (eng_figures REJECTED). Scheme '
             'p21 answers the four romans on four lines with a "Calculations" '
             'cell beside them; "Four part @ 5 marks".',
         lifted=[S(21, 100, 329, 380, 344)], marks=[5], total=5,
         question_figure='engineering-2021-OL-paper-q7b-crop'),
    dict(key=(7, 'b', 'ii'),
         topic='eng-3-12',
         checked='paper page 8: (b) reads "A hole and shaft assembly is manufactured to the dimensions shown." over "State the: (i) Nominal diameter of the hole;", (ii), (iii) and (iv) beneath it; each closes on a semicolon because the list runs on, and (iv) on a full stop', why='The same table, second line.',
         lifted=[S(21, 100, 344, 380, 358)], marks=[5], total=5,
         question_figure='engineering-2021-OL-paper-q7b-crop'),
    dict(key=(7, 'b', 'iii'),
         topic='eng-3-12',
         checked='paper page 8: (b) reads "A hole and shaft assembly is manufactured to the dimensions shown." over "State the: (i) Nominal diameter of the hole;", (ii), (iii) and (iv) beneath it; each closes on a semicolon because the list runs on, and (iv) on a full stop', why='The same table, third line.',
         lifted=[S(21, 100, 361, 380, 376)], marks=[5], total=5,
         question_figure='engineering-2021-OL-paper-q7b-crop'),
    dict(key=(7, 'b', 'iv'),
         topic='eng-3-12',
         checked='paper page 8: (b) reads "A hole and shaft assembly is manufactured to the dimensions shown." over "State the: (i) Nominal diameter of the hole;", (ii), (iii) and (iv) beneath it; each closes on a semicolon because the list runs on, and (iv) on a full stop', why='The same table, fourth line.',
         lifted=[S(21, 100, 376, 405, 391)], marks=[5], total=5,
         question_figure='engineering-2021-OL-paper-q7b-crop'),
    dict(key=(7, 'c', None),
         topic='eng-3-12',
         question_lift=P(8, 85, 407, 580, 426),
         why='The instruments branch of (c): four photographs captioned '
             '(i)-(iv); the reader joins the OR branch\'s romans onto its cue, so '
             'the question is lifted from its own printed line. Scheme p21 names '
             'each and gives an application, and prices the two apart: "Name '
             'Award 3 @ 3 Marks, Application Award 3 @ 3 Marks", so a name is '
             'claimed without its application; each application is shown with '
             'the instrument it is for.',
         lifted=[[S(21, 70, 505, 210, 521), S(21, 70, 547, 210, 563),
                  S(21, 70, 619, 210, 635), S(21, 70, 662, 210, 678)],
                 [S(21, 70, 505, 455, 536), S(21, 70, 547, 455, 607),
                  S(21, 70, 619, 455, 650), S(21, 70, 660, 455, 678)]],
         row_kind='anyN', group=[(3, 3), (3, 3)], marks=[9, 9], tariff='fixed',
         total=18,
         question_figure='engineering-2021-OL-paper-q7c-crop',
         notes="The scheme prints 'Name Award 3 @ 3 Marks, Application Award 3 @ "
               "3 Marks'."),
    dict(key=(7, 'c', 'i'),
         why='The OR branch of (c): the model eRacer photographed beside it, '
             'for which the automatic crop took the instruments instead '
             '(eng_figures REJECTED). Scheme p22 lists the two components; '
             '"One part @ 5 marks, One part @ 4 marks".',
         lifted=[S(22, 100, 112, 260, 129), S(22, 100, 127, 260, 144)],
         tariff='orderedSplit', notation='One part @ 5 marks; One part @ 4 marks',
         ladder=9, question_figure='engineering-2021-OL-paper-q7ci-crop'),
    dict(key=(7, 'c', 'ii'),
         replaces='the shipped card answered "Draw the electronic symbol for each '
                  'electronic component named" with the instruments branch\'s '
                  '(ii): "Digital Vernier calipers - Used for accurately '
                  'measuring the diameter of round bars ..."',
         why='Scheme p22 answers with the motor and switch symbols drawn; '
             '"One part @ 5 marks, One part @ 4 marks".',
         special={'kind': 'ask'}, total=9,
         question_figure='engineering-2021-OL-paper-q7ci-crop',
         figure='engineering-2021-OL-scheme-q7cii-sol',
         notes="The scheme prints 'Award 1 @ 5 Marks, Award 1 @ 4 Marks'."),
    dict(key=(7, 'a', 'i'),
         replaces='the shipped card priced "Name two types of fit" at 4 marks '
                  'with the scheme\'s three fits as one row; the grid prices '
                  'Q7(a) "Three parts @ 4 marks (12)" and scheme p21 "(i) Name '
                  'Award 2 @ 4 Marks"',
         why='Scheme p21 lists the three fits on one line, any two to name.',
         lifted=[[S(21, 96, 158, 163, 174), S(21, 163, 158, 240, 174),
                  S(21, 253, 158, 322, 174)]],
         row_kind='anyN', group=(2, 4), marks=[8], tariff='fixed', total=8,
         notes="The scheme prints '(i) Name Award 2 @ 4 Marks'."),
    dict(key=(3, 'd', None),
         replaces='the shipped question interleaved the two OR branches line by '
                  'line -- "(i) Malleability, OR State two advantages of robotics '
                  'in manufacturing. (ii) Compressive strength, OR ..." -- and its '
                  'options mixed both branches\' answers',
         why='Paper p4 sets two alternative (d)s either side of an OR; the '
             'reader files both branches\' romans under one key and puts the OR '
             'between each pair. This card is the first branch, the four terms; '
             'scheme p13 defines each, "Award 2 @ 6 Marks".',
         topic='eng-3-8', question_lift=P(4, 85, 518, 576, 560),
         lifted=[[S(13, 70, 264, 452, 294), S(13, 70, 306, 452, 337),
                  S(13, 70, 349, 455, 424), S(13, 70, 436, 452, 466)]],
         row_kind='anyN', group=(2, 6), marks=[12], tariff='fixed', total=12,
         notes="The scheme prints 'Award 2 @ 6 Marks'. The paper sets this (d) "
               "and the robotics (d) beneath it either side of an OR."),
    dict(key=(3, 'd', 'i'),
         replaces='the shipped question read "Explain any two of the following '
                  'terms: Malleability, OR State two advantages of robotics in '
                  'manufacturing." and mixed a definition of malleability into its '
                  'answers',
         why='The second branch\'s (i), lifted from its own line on paper p4; '
             'scheme p13 answers it in two bullets, "Award 2 @ 3 Marks".',
         topic='eng-3-14', question_lift=P(4, 110, 648, 560, 666),
         lifted=[S(13, 93, 555, 456, 571), S(13, 93, 570, 456, 602)],
         marks=[3, 3], total=6,
         notes='The paper sets this (d) as the alternative, after an OR, to "(d) '
               'Explain any two of the following terms".'),
    dict(key=(3, 'd', 'ii'),
         replaces='the shipped question read "Explain any two of the following '
                  'terms: Compressive strength, OR State two ways in which the use '
                  'of robotic technology ..." and mixed a definition into its '
                  'answers',
         why='The second branch\'s (ii), lifted from its two lines on paper p4; '
             'scheme p13 answers it in two bullets, "Award 2 @ 3 Marks".',
         topic='eng-3-14', question_lift=P(4, 112, 677, 600, 713),
         lifted=[S(13, 93, 643, 440, 690), S(13, 93, 702, 440, 749)],
         marks=[3, 3], total=6,
         notes='The paper sets this (d) as the alternative, after an OR, to "(d) '
               'Explain any two of the following terms".'),
]

# Cards the automatic author files under the wrong syllabus heading.
# Question 1 parts the scheme prices half and half, which the automatic author
# read from the marks grid as one six-mark total; each row now carries the
# half printed beside it (eng_residue REPRICE). Opened on the scheme page named.
# Question 1 parts the automatic author builds, carded at the printed primary
# price, 7 (4 + 3 for a two-part answer), where it read the bracketed 6 (eng_residue
# PRIMARY). Each opened on the scheme page named.
PRIMARY = {
    'eng-2021-ol-q1-a': ([4, 3], '4 (3) + 3 Marks', Q1_PRICE),  # scheme p4
    'eng-2021-ol-q1-b': ([7], '7 (6) Marks', Q1_PRICE),  # scheme p4
    'eng-2021-ol-q1-c': ([7], '7 (6) Marks', Q1_PRICE),  # scheme p4
    'eng-2021-ol-q1-d': ([4, 3], '4 (3) + 3 Marks', Q1_PRICE),  # scheme p4
    'eng-2021-ol-q1-g': ([7], '7 (6) Marks', Q1_PRICE),  # scheme p4, printed beside its "(h)"
    'eng-2021-ol-q1-k': ([4, 3], 'Definition Award 4 (3), Name Award 3', Q1_PRICE),  # p7
}

TOPICS = {
    'eng-2021-ol-q4-c-iii': ('eng-2-10', 'joining light gauge sheet aluminium (a pop '
                             'rivet) is joining; "aluminium" outvoted it'),
    'eng-2021-ol-q5-a-ii': ('eng-1-9', 'describing a plastic manufacturing process '
                            '(vacuum forming, injection or blow moulding) is plastics '
                            'processing, not manufacturing systems'),
    'eng-2021-ol-q5-d': ('eng-3-1', 'the ask is two safety precautions when bonding '
                         'acrylic; "adhesive" outvoted it'),
}

ATLAS = {
    **{f'eng-2021-ol-q2-c-{p}': dict(
        topics=['Materials: Properties and Uses'],
        note='Choosing a material for each part of a wheelchair, and why: '
             'materials and their properties, which the reference files Q2(c) '
             'under; the card\'s syllabus heading is Technology (selection of '
             'materials).') for p in ('i', 'ii')},
    **{f'eng-2021-ol-q3-d-{p}': dict(
        topics=['Energy, Electronics & Robotics'],
        note='Robotics in manufacturing (the OR branch of Q3(d)), which the '
             'reference files Q3(d) under; the card\'s syllabus heading is '
             'Technology, where the syllabus places robotics.') for p in ('i', 'ii')},
    'eng-2021-ol-q5-d': dict(
        topics=['Health and Safety'],
        note='Safety precautions when bonding acrylic with an adhesive; Q5 is '
             'otherwise filed under Polymers only.'),
}
