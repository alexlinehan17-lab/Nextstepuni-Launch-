"""2015 Ordinary Level: every part, from the page.

Paper and scheme as the PDFs number their pages. As in 2016-2019, the automatic
author prices nothing in this sitting: the scheme sets each answer in a left
column and its award in a box to the right ("Name Award 3 @ 4 Marks"), which
its reader does not join to the answer, so every card here is built from the
page by rectangle. The marks grid is on scheme p4: Question 1 is Section A,
"Any six @ 5 marks each", two-part answers 3 + 2, and Section B, "Any three
parts @ 12 + 12 + 11 Marks"; Questions 2-7 are 45 marks each. A Section B card
carries the PRINTED primary price, the 12 the scheme awards a part answered
first or second ("Award 12 (11) Marks"), and says the third part answered
earns 11.
"""
from eng_lift import join, lift

Y, L = 2015, 'ol'


def S(page, *rect):
    return lift(Y, L, 'scheme', page, rect)


def P(page, *rect, more=(), items=()):
    return lift(Y, L, 'paper', page, rect, more=more, items=items)


_B2 = (95, 161, 460, 181)             # paper p3: Q2(b)'s lead-in
_A5 = (95, 462, 442, 481)             # paper p4: Q5(a), the three items
_C6 = (95, 348, 307, 367)             # paper p5: Q6(c), the chuck

_SB = ("Section B is 'Any three parts @ 12 + 12 + 11 Marks': the card carries the 12 a part "
       "earns answered first or second; answered third it earns 11.")
_FURN = 'The furnaces are named at Q2(a): an electric arc, a basic oxygen and a blast furnace.'
_OR3 = ('The paper sets two (d)s either side of an OR, the cooling media and robotics; the '
        'scheme prices both "Award 2 @ 4 Marks", so they are one card, each branch a route.')
_OR6 = ('The paper sets two (c)s either side of an OR: the chuck (c), whose (i)-(iii) are '
        'carded apart, and the CNC (c), carded at the letter.')
_OR7 = ('The paper sets two (c)s either side of an OR: the instruments (c), carded at the '
        'letter, and the electronic components (c), one card for each component '
        'photographed and captioned (i)-(iii).')

CROPS = {
    # ---- paper ------------------------------------------------------------
    'engineering-2015-OL-paper-q1a-crop': dict(
        doc='paper', page=2, rect=(475, 77, 570, 127), image=True, ref='2015 OL Q1(a)'),
    # The cam with A beside it; the end of (f)'s line runs into the box and is
    # whited out.
    'engineering-2015-OL-paper-q1g-crop': dict(
        doc='paper', page=2, rect=(450, 226, 566, 311), mask=[(449, 233, 480, 251)],
        ref='2015 OL Q1(g)', letters=('A',)),
    # The vice and the machine screw with their captions.
    'engineering-2015-OL-paper-q1h-crop': dict(
        doc='paper', page=2, rect=(78, 306, 335, 390), ref='2015 OL Q1(h)'),
    'engineering-2015-OL-paper-q1i-crop': dict(
        doc='paper', page=2, rect=(60, 494, 550, 584), ref='2015 OL Q1(i)'),
    'engineering-2015-OL-paper-q1m-crop': dict(
        doc='paper', page=2, rect=(355, 742, 535, 810), ref='2015 OL Q1(m)'),
    # The three furnaces captioned (i)-(iii); (a)'s own line, which runs
    # between the first two drawings, is whited out.
    'engineering-2015-OL-paper-q2a-crop': dict(
        doc='paper', page=3, rect=(88, 28, 495, 152), mask=[(88, 50, 270, 70)],
        ref='2015 OL Q2(a)'),
    'engineering-2015-OL-paper-q2c-crop': dict(
        doc='paper', page=3, rect=(90, 282, 540, 374), ref='2015 OL Q2(c)'),
    'engineering-2015-OL-paper-q3b-crop': dict(
        doc='paper', page=3, rect=(201, 594, 352, 652), image=True, ref='2015 OL Q3(b)'),
    'engineering-2015-OL-paper-q4civ-crop': dict(
        doc='paper', page=4, rect=(506, 230, 573, 297), image=True, ref='2015 OL Q4(c)(iv)'),
    'engineering-2015-OL-paper-q4d-crop': dict(
        doc='paper', page=4, rect=(373, 288, 442, 378), image=True, ref='2015 OL Q4(d)'),
    'engineering-2015-OL-paper-q5a-crop': dict(
        doc='paper', page=4, rect=(92, 482, 552, 592), ref='2015 OL Q5(a)'),
    'engineering-2015-OL-paper-q6a-crop': dict(
        doc='paper', page=5, rect=(35, 85, 556, 219), ref='2015 OL Q6(a)'),
    'engineering-2015-OL-paper-q6c-crop': dict(
        doc='paper', page=5, rect=(267, 376, 421, 528), image=True, ref='2015 OL Q6(c)'),
    'engineering-2015-OL-paper-q7b-crop': dict(
        doc='paper', page=6, rect=(382, 158, 572, 290), ref='2015 OL Q7(b)'),
    'engineering-2015-OL-paper-q7c-crop': dict(
        doc='paper', page=6, rect=(20, 328, 552, 528), ref='2015 OL Q7(c)'),
    # The OR branch's three components, captioned (i)-(iii).
    'engineering-2015-OL-paper-q7cor-crop': dict(
        doc='paper', page=6, rect=(88, 648, 500, 766), ref='2015 OL Q7(c)'),
    # ---- scheme: the drawings the answers are given with -------------------
    'engineering-2015-OL-scheme-q1i-sol': dict(
        doc='scheme', parts=[(6, (428, 155, 560, 290)), (6, (428, 334, 545, 437)),
                             (6, (318, 512, 566, 666))],
        # The dip tank's labels start left of where the answer's lines end; the
        # four words of those lines inside the box are whited out.
        mask=[(318, 500, 336, 517), (318, 514, 324, 531), (316, 638, 327, 656),
              (318, 652, 332, 666)],
        solution=True, ref='2015 OL Q1(i)'),
    'engineering-2015-OL-scheme-q2bi-sol': dict(
        doc='scheme', parts=[(9, (60, 252, 255, 392)), (9, (60, 418, 240, 596)),
                             (9, (92, 626, 240, 808))],
        mask=[(88, 410, 106, 431)], layout='row', solution=True, ref='2015 OL Q2(b)(i)'),
    'engineering-2015-OL-scheme-q5aii-sol': dict(
        doc='scheme', parts=[(13, (188, 710, 384, 780)), (14, (208, 152, 378, 235)),
                             (14, (216, 322, 360, 377))],
        solution=True, ref='2015 OL Q5(a)(ii)'),
}

CARDS = [
    # ---- Question 1, Section A ("Any six @ 5 marks each") ------------------
    dict(key=(1, 'a', None),
         why='The strip heater is photographed beside (a); scheme p5 numbers two '
             'precautions; "3 + 2 Marks".',
         topic='eng-3-1',
         lifted=[S(5, 88, 383, 400, 401), S(5, 88, 401, 400, 417)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         question_figure='engineering-2015-OL-paper-q1a-crop',
         notes="The scheme prints '3 + 2 Marks'."),
    dict(key=(1, 'b', None),
         why='Scheme p5 explains the term in one sentence, "5 Marks".',
         topic='eng-1-2',
         lifted=[S(5, 70, 424, 430, 459)], marks=[5], total=5,
         notes="The scheme prints '5 Marks'."),
    dict(key=(1, 'c', None),
         why='Scheme p5 numbers two operations under a lead-in; "3 + 2 Marks".',
         topic='eng-2-11',
         lifted=[S(5, 88, 497, 400, 511), S(5, 88, 511, 400, 527)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         notes="The scheme prints '3 + 2 Marks'."),
    dict(key=(1, 'd', None),
         why='Scheme p5 numbers two advantages; "3 + 2 Marks".',
         topic='eng-2-13',
         lifted=[S(5, 88, 537, 420, 568), S(5, 88, 568, 420, 596)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         notes="The scheme prints '3 + 2 Marks'."),
    dict(key=(1, 'e', None),
         why='Scheme p5 numbers two reasons; "3 + 2 Marks".',
         topic='eng-3-14',
         lifted=[S(5, 91, 620, 420, 635), S(5, 91, 635, 420, 651)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         notes="The scheme prints '3 + 2 Marks'."),
    dict(key=(1, 'f', None),
         why='Scheme p5 numbers two reasons; "3 + 2 Marks".',
         topic='eng-3-7',
         lifted=[S(5, 91, 662, 440, 677), S(5, 91, 677, 440, 693)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         notes="The scheme prints '3 + 2 Marks'."),
    dict(key=(1, 'g', None),
         why='The cam is drawn with A beside it; scheme p5 names the mechanism in one '
             'answer, "Cam and Follower.", and prints "3 + 2 Marks" beside it with no '
             'part priced apart: one row for the part\'s 5.',
         topic='eng-2-15',
         lifted=[S(5, 73, 700, 175, 720)], marks=[5], total=5,
         labels={'A': S(5, 73, 700, 175, 720)},
         question_figure='engineering-2015-OL-paper-q1g-crop',
         notes="The scheme prints '3 + 2 Marks' beside the one answer, 'Cam and Follower.'"),
    dict(key=(1, 'h', None),
         why='Scheme p5 names each thread after its item, "3+2 Marks". The reader joins '
             'the Section B heading to (h), so the question is lifted from the page, with '
             'the captions the paper prints under the two pictures.',
         topic='eng-2-11',
         question_lift=P(2, 60, 288, 345, 307, more=[(78, 371, 330, 390)]),
         lifted=[S(5, 73, 728, 420, 746), S(5, 73, 746, 470, 762)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         question_figure='engineering-2015-OL-paper-q1h-crop',
         notes="The scheme prints '3+2 Marks'."),
    # ---- Question 1, Section B ("Any three parts @ 12 + 12 + 11 Marks") ----
    dict(key=(1, 'i', None),
         why='The three items are photographed and captioned under (i); scheme p6 '
             'describes each under its name, beside a drawing of it, shown with the '
             'answer; "Any one", "Award 12 (11) Marks". The question is lifted with each '
             'caption on its own line, as the paper sets them under their pictures.',
         topic='eng-2-15', stem=False,
         question_lift=P(2, 60, 477, 385, 496, items=[(65, 564, 180, 584),
                                                      (228, 564, 370, 584),
                                                      (420, 564, 545, 584)]),
         lifted=[[join(S(6, 85, 139, 210, 159), S(6, 88, 153, 410, 256)),
                  join(S(6, 88, 319, 250, 339), S(6, 88, 332, 430, 432)),
                  join(S(6, 88, 484, 220, 504), S(6, 88, 498, 500, 725))]],
         row_kind='anyN', group=(1, 12), marks=[12], tariff='fixed', total=12,
         question_figure='engineering-2015-OL-paper-q1i-crop',
         figure='engineering-2015-OL-scheme-q1i-sol',
         notes="The scheme prints 'Any one: Good clear description Award 12 (11) Marks'. "
               + _SB),
    dict(key=(1, 'j', None),
         why='Scheme p7 explains each term under its name, "Any two", "Award 6 + 6(5)".',
         topic='eng-3-14', stem=False,
         lifted=[[join(S(7, 88, 98, 145, 118), S(7, 88, 112, 470, 174)),
                  join(S(7, 88, 190, 200, 210), S(7, 88, 204, 470, 280)),
                  join(S(7, 85, 296, 205, 316), S(7, 88, 309, 470, 372)),
                  join(S(7, 88, 378, 145, 398), S(7, 88, 392, 470, 496))]],
         row_kind='anyN', group=(2, 6), marks=[12], tariff='fixed', total=12,
         notes="The scheme prints 'Any two: Good clear description Award 6 + 6(5)'. " + _SB),
    dict(key=(1, 'k', None),
         why='Scheme p7 defines the term and gives an example, each in its own paragraph; '
             '"Definition Award 6", "Example Award 6(5)".',
         topic='eng-3-8', stem=False,
         lifted=[S(7, 85, 602, 420, 636), S(7, 85, 643, 420, 664)],
         marks=[6, 6], total=12,
         notes="The scheme prints 'Definition Award 6' and 'Example Award 6(5)'. " + _SB),
    dict(key=(1, 'l', None),
         why='Scheme p8 explains each term under its name, "Any two", "Award 6 + 6 (5)".',
         topic='eng-3-14', stem=False,
         lifted=[[join(S(8, 88, 100, 240, 118), S(8, 88, 112, 480, 200)),
                  join(S(8, 85, 236, 152, 256), S(8, 88, 250, 500, 325)),
                  join(S(8, 82, 374, 138, 394), S(8, 82, 388, 480, 450)),
                  join(S(8, 82, 484, 212, 504), S(8, 80, 498, 460, 588))]],
         row_kind='anyN', group=(2, 6), marks=[12], tariff='fixed', total=12,
         notes="The scheme prints 'Any two: Good description Award 6 + 6 (5)'. " + _SB),
    dict(key=(1, 'm', None),
         why='The two tools are photographed and captioned (i) and (ii); scheme p8 names '
             'each after its roman, "Name Award 6 + 6 (5)".',
         topic='eng-2-11', stem=False,
         lifted=[S(8, 79, 654, 200, 676), S(8, 205, 654, 320, 676)],
         marks=[6, 6], total=12,
         question_figure='engineering-2015-OL-paper-q1m-crop',
         notes="The scheme prints 'Name Award 6 + 6 (5)', for (i) and (ii) in that order. "
               + _SB),
    # ---- Question 2 --------------------------------------------------------
    dict(key=(2, 'a', None),
         why='The three furnaces are drawn and captioned (i)-(iii); scheme p9 names each '
             'after its roman, "Name Award 3 @ 4 Marks". The reader runs the three captions '
             'on after the ask; they stay with the drawings, so the question is lifted from '
             'the page.',
         topic='eng-1-4',
         question_lift=P(3, 95, 51, 270, 70),
         lifted=[S(9, 88, 127, 240, 142), S(9, 88, 142, 240, 157), S(9, 88, 157, 240, 172)],
         marks=[4, 4, 4], total=12,
         question_figure='engineering-2015-OL-paper-q2a-crop',
         notes="The scheme prints 'Name Award 3 @ 4 Marks'."),
    dict(key=(2, 'b', 'i'),
         why='"Select one of the furnaces": scheme p9 draws each furnace in turn, the '
             'drawing the answer, "Any furnace Award 1 @ 4 Marks". The ask is the row, the '
             'three drawings shown with the answer.',
         topic='eng-1-4', stem=False,
         question_lift=P(3, *_B2, more=[(120, 189, 395, 208)]),
         special={'kind': 'ask'}, total=4,
         question_figure='engineering-2015-OL-paper-q2a-crop',
         figure='engineering-2015-OL-scheme-q2bi-sol',
         notes="The scheme prints 'Any furnace Award 1 @ 4 Marks'. " + _FURN),
    dict(key=(2, 'b', 'ii'),
         why='Scheme p9 gives each furnace\'s charge on its (ii) line, any one, "Award 3 @ '
             '3 Marks".',
         topic='eng-1-4', stem=False,
         question_lift=P(3, *_B2, more=[(120, 203, 290, 222)]),
         lifted=[[S(9, 288, 279, 440, 299), S(9, 288, 431, 440, 451),
                  S(9, 297, 644, 440, 678)]],
         row_kind='anyN', group=(1, 3), marks=[3], tariff='fixed', total=3,
         question_figure='engineering-2015-OL-paper-q2a-crop',
         notes="The scheme prints 'Award 3 @ 3 Marks' for (ii)-(iv), for the furnace "
               "selected. " + _FURN),
    dict(key=(2, 'b', 'iii'),
         why='Scheme p9 says how each furnace heats its charge on its (iii) line, any one, '
             '"Award 3 @ 3 Marks".',
         topic='eng-1-4', stem=False,
         question_lift=P(3, *_B2, more=[(120, 217, 342, 236)]),
         lifted=[[S(9, 288, 306, 520, 354), S(9, 288, 458, 500, 520),
                  S(9, 297, 685, 445, 719)]],
         row_kind='anyN', group=(1, 3), marks=[3], tariff='fixed', total=3,
         question_figure='engineering-2015-OL-paper-q2a-crop',
         notes="The scheme prints 'Award 3 @ 3 Marks' for (ii)-(iv), for the furnace "
               "selected. " + _FURN),
    dict(key=(2, 'b', 'iv'),
         why='Scheme p9 names each furnace\'s metal on its (iv) line, any one, "Award 3 @ '
             '3 Marks".',
         topic='eng-1-4', stem=False,
         question_lift=P(3, *_B2, more=[(120, 231, 252, 250)]),
         lifted=[[S(9, 288, 361, 400, 381), S(9, 288, 527, 340, 547),
                  S(9, 296, 727, 350, 747)]],
         row_kind='anyN', group=(1, 3), marks=[3], tariff='fixed', total=3,
         question_figure='engineering-2015-OL-paper-q2a-crop',
         notes="The scheme prints 'Award 3 @ 3 Marks' for (ii)-(iv), for the furnace "
               "selected. " + _FURN),
    dict(key=(2, 'c', None),
         why='The three components are photographed and captioned; scheme p10 gives a '
             'material for each after its name, "Suitable material Award 3 @ 4 Marks".',
         topic='eng-3-8',
         lifted=[S(10, 79, 95, 430, 111), S(10, 79, 111, 430, 125), S(10, 79, 125, 430, 141)],
         marks=[4, 4, 4], total=12,
         question_figure='engineering-2015-OL-paper-q2c-crop',
         notes="The scheme prints 'Suitable material Award 3 @ 4 Marks'."),
    dict(key=(2, 'd', None),
         why='Scheme p10 gives the metals for each alloy after its name, "Metals Award 2 @ '
             '4 Marks".',
         topic='eng-1-5',
         lifted=[S(10, 79, 206, 430, 226), S(10, 79, 222, 430, 240)],
         marks=[4, 4], total=8,
         notes="The scheme prints 'Metals Award 2 @ 4 Marks'."),
    # ---- Question 3 --------------------------------------------------------
    dict(key=(3, 'a', None),
         why='A lead-in over three terms set as romans, "any two"; scheme p10 describes '
             'each under its name, "Any two descriptions: Award 2 @ 8 marks".',
         topic='eng-2-6',
         lifted=[[join(S(10, 105, 385, 200, 405), S(10, 105, 401, 436, 518)),
                  join(S(10, 105, 526, 170, 546), S(10, 105, 539, 465, 587)),
                  join(S(10, 108, 595, 205, 615), S(10, 108, 608, 475, 683))]],
         row_kind='anyN', group=(2, 8), marks=[16], tariff='fixed', total=16,
         notes="The scheme prints 'Any two descriptions: Award 2 @ 8 marks'."),
    dict(key=(3, 'b', None),
         why='The hammer is photographed under (b); scheme pp10-11 describe the hardening '
             'and the tempering under their headings, "Description Award 1 @ 8 Marks", '
             '"Award 1 @ 7 Marks".',
         topic='eng-2-6',
         lifted=[join(S(10, 90, 719, 160, 739), S(10, 90, 733, 430, 767),
                      S(11, 90, 68, 460, 116)),
                 join(S(11, 90, 137, 160, 157), S(11, 90, 151, 430, 212))],
         marks=[8, 7], total=15,
         question_figure='engineering-2015-OL-paper-q3b-crop',
         notes="The scheme prints 'Description Award 1 @ 8 Marks' and 'Award 1 @ 7 Marks', "
               "for the hardening and the tempering in that order."),
    dict(key=(3, 'c', None),
         why='Scheme p11 numbers two precautions, "Reasons Award 2 @ 3 Marks".',
         topic='eng-3-1',
         lifted=[S(11, 108, 276, 440, 293), S(11, 108, 293, 440, 309)],
         marks=[3, 3], total=6,
         notes="The scheme prints 'Reasons Award 2 @ 3 Marks'."),
    dict(key=(3, 'd', None),
         why='Paper p3 sets two alternative (d)s either side of an OR. Scheme p11 gives the '
             'effect of each cooling medium, "Difference Award 2 @ 4 Marks", and bullets two '
             'applications of robotics, "Robotics Award 2 @ 4 Marks": priced alike, one card '
             'with a route per branch.',
         topic='eng-2-6', stem=False,
         lifted=[S(11, 105, 344, 430, 392), S(11, 111, 413, 440, 475),
                 S(11, 155, 570, 300, 588), S(11, 155, 588, 300, 604)],
         marks=[4, 4, 4, 4], routes=['a', 'a', 'b', 'b'], total=8,
         notes="The scheme prints 'Difference Award 2 @ 4 Marks' and 'Robotics Award 2 @ 4 "
               "Marks'. " + _OR3),
    # ---- Question 4 --------------------------------------------------------
    dict(key=(4, 'a', None),
         why='A lead-in over four terms set as romans, "any three"; scheme p12 describes '
             'each under its name, "Description Award 3 @ 3 Marks".',
         topic='eng-2-10',
         lifted=[[join(S(12, 102, 141, 135, 161), S(12, 102, 155, 440, 203)),
                  join(S(12, 106, 224, 160, 244), S(12, 106, 238, 440, 299)),
                  join(S(12, 109, 321, 180, 341), S(12, 109, 335, 445, 396)),
                  join(S(12, 108, 417, 155, 437), S(12, 108, 431, 450, 479))]],
         row_kind='anyN', group=(3, 3), marks=[9], tariff='fixed', total=9,
         notes="The scheme prints 'Description Award 3 @ 3 Marks'."),
    dict(key=(4, 'b', 'i'),
         why='Scheme p12 names the three flames on one line, each lifted by its own word '
             'rectangle, "Flames Award 3 @ 3 Marks". "Carbursing" is the scheme\'s spelling.',
         topic='eng-2-10',
         lifted=[S(12, 97, 542, 170, 562), S(12, 196, 542, 281, 562), S(12, 304, 542, 395, 562)],
         marks=[3, 3, 3], total=9,
         notes="The scheme prints 'Flames Award 3 @ 3 Marks'."),
    dict(key=(4, 'b', 'ii'),
         why='Scheme p12 gives the proportions for each flame in a sentence each, '
             '"Proportions Award 3 @ 3 Marks".',
         topic='eng-2-10',
         lifted=[S(12, 99, 625, 430, 646), S(12, 99, 652, 430, 673), S(12, 99, 680, 442, 700)],
         marks=[3, 3, 3], total=9,
         notes="The scheme prints 'Proportions Award 3 @ 3 Marks'."),
    dict(key=(4, 'c', 'i'),
         why='One of "Answer any three of the following", "Descriptions Award 3 @ 4 Marks": '
             'scheme p13 answers in a paragraph.',
         topic='eng-2-10',
         lifted=[S(13, 117, 95, 440, 143)], marks=[4], total=4,
         notes="The scheme prints 'Descriptions Award 3 @ 4 Marks' for the three parts "
               "answered."),
    dict(key=(4, 'c', 'ii'),
         why='One of "Answer any three of the following": scheme p13 answers in a sentence.',
         topic='eng-2-10',
         lifted=[S(13, 117, 151, 505, 171)], marks=[4], total=4,
         notes="The scheme prints 'Descriptions Award 3 @ 4 Marks' for the three parts "
               "answered."),
    dict(key=(4, 'c', 'iii'),
         why='One of "Answer any three of the following": scheme p13 gives two precautions '
             'in two sentences, each lifted by its own rectangle; the 4 for the part is not '
             'split between them.',
         topic='eng-2-10',
         lifted=[join(S(13, 117, 192, 460, 212), S(13, 117, 206, 175, 226)),
                 S(13, 175, 206, 485, 226)],
         tariff='questionTotal', total=4,
         notes="The scheme prints 'Descriptions Award 3 @ 4 Marks' for the three parts "
               "answered."),
    dict(key=(4, 'c', 'iv'),
         why='One of "Answer any three of the following": the screw is photographed beside '
             'it; scheme p13 names it and gives its use in a sentence each, the 4 not split '
             'between them.',
         topic='eng-2-10',
         lifted=[S(13, 120, 247, 262, 267), join(S(13, 262, 247, 505, 267),
                                                 S(13, 120, 261, 230, 281))],
         tariff='questionTotal', total=4,
         question_figure='engineering-2015-OL-paper-q4civ-crop',
         notes="The scheme prints 'Descriptions Award 3 @ 4 Marks' for the three parts "
               "answered."),
    dict(key=(4, 'd', None),
         why='The welder is photographed beside (d); scheme p13 bullets two reasons, '
             '"Safety Award 2 @ 3 Marks".',
         topic='eng-3-1',
         lifted=[S(13, 120, 339, 430, 359), S(13, 120, 354, 430, 388)],
         marks=[3, 3], total=6,
         question_figure='engineering-2015-OL-paper-q4d-crop',
         notes="The scheme prints 'Safety Award 2 @ 3 Marks'."),
    # ---- Question 5 --------------------------------------------------------
    dict(key=(5, 'a', 'i'),
         why='The three items are photographed and captioned; scheme p13 names a process '
             'for each after its name, "Name Award 3 @ 3 Marks". The question is lifted with '
             '(a)\'s lead-in.',
         topic='eng-1-9', stem=False,
         question_lift=P(4, *_A5, more=[(118, 600, 492, 633)]),
         lifted=[S(13, 97, 492, 445, 512), S(13, 97, 508, 445, 528), S(13, 97, 521, 445, 541)],
         marks=[3, 3, 3], total=9,
         question_figure='engineering-2015-OL-paper-q5a-crop',
         notes="The scheme prints 'Name Award 3 @ 3 Marks'. \"Caldering\" is the scheme's "
               "spelling."),
    dict(key=(5, 'a', 'ii'),
         why='"Any one process": scheme pp13-14 describe vacuum forming, blow moulding and '
             'injection moulding under their names, each over a drawing, shown with the '
             'answer; "Process Award 9 Marks".',
         topic='eng-1-9', stem=False,
         question_lift=P(4, *_A5, more=[(118, 641, 550, 660)]),
         lifted=[[join(S(13, 88, 590, 190, 610), S(13, 88, 604, 440, 637),
                       S(13, 88, 634, 470, 694)),
                  join(S(14, 88, 68, 180, 88), S(14, 88, 82, 445, 158)),
                  join(S(14, 94, 247, 200, 267), S(14, 94, 261, 430, 310))]],
         row_kind='anyN', group=(1, 9), marks=[9], tariff='fixed', total=9,
         question_figure='engineering-2015-OL-paper-q5a-crop',
         figure='engineering-2015-OL-scheme-q5aii-sol',
         notes="The scheme prints 'Any one process: Process Award 9 Marks'."),
    dict(key=(5, 'b', None),
         why='Scheme p14 bullets two precautions, "Safety Award 2 @ 3 Marks".',
         topic='eng-3-1',
         lifted=[S(14, 120, 414, 440, 462), S(14, 120, 470, 490, 504)],
         marks=[3, 3], total=6,
         notes="The scheme prints 'Any two: Safety Award 2 @ 3 Marks'."),
    dict(key=(5, 'c', None),
         why='A lead-in over four terms set as romans, "any three"; scheme pp14-15 explain '
             'each under its name, "Explanation Award 3 @ 5 Marks". "Figreglass" is the '
             'scheme\'s spelling.',
         topic='eng-1-9',
         lifted=[[join(S(14, 100, 551, 180, 571), S(14, 100, 565, 430, 615)),
                  join(S(14, 100, 635, 165, 655), S(14, 100, 649, 450, 725)),
                  join(S(15, 100, 82, 190, 102), S(15, 100, 96, 450, 172)),
                  join(S(15, 100, 178, 220, 198), S(15, 100, 192, 495, 241))]],
         row_kind='anyN', group=(3, 5), marks=[15], tariff='fixed', total=15,
         notes="The scheme prints 'Any three: Explanation Award 3 @ 5 Marks'."),
    dict(key=(5, 'd', None),
         why='Scheme p15 bullets the steps of one procedure, "Description Award 1 @ 6 '
             'Marks": one row.',
         topic='eng-1-9',
         lifted=[S(15, 120, 290, 420, 340)], marks=[6], total=6,
         notes="The scheme prints 'Description Award 1 @ 6 Marks'."),
    # ---- Question 6 --------------------------------------------------------
    dict(key=(6, 'a', None),
         why='The four components are photographed and captioned (i)-(iv); scheme p15 names '
             'each after its roman, any three, "Name Award 3 @ 5 Marks".',
         topic='eng-2-11',
         lifted=[[S(15, 97, 435, 300, 449), S(15, 97, 449, 300, 463),
                  S(15, 97, 463, 300, 477), S(15, 97, 477, 300, 491)]],
         row_kind='anyN', group=(3, 5), marks=[15], tariff='fixed', total=15,
         question_figure='engineering-2015-OL-paper-q6a-crop',
         notes="The scheme prints 'Any three lathe components: Name Award 3 @ 5 Marks'."),
    dict(key=(6, 'b', None),
         why='A lead-in over four terms set as romans, "any three"; scheme p15 explains '
             'each under its name, "Explanation Award 3 @ 5 Marks".',
         topic='eng-2-11',
         lifted=[[join(S(15, 114, 535, 195, 555), S(15, 114, 549, 420, 583)),
                  join(S(15, 118, 597, 195, 617), S(15, 118, 611, 500, 646)),
                  join(S(15, 119, 652, 200, 672), S(15, 119, 666, 495, 715)),
                  join(S(15, 120, 721, 150, 741), S(15, 120, 735, 480, 770))]],
         row_kind='anyN', group=(3, 5), marks=[15], tariff='fixed', total=15,
         notes="The scheme prints 'Any three terms: Explanation Award 3 @ 5 Marks'."),
    dict(key=(6, 'c', 'i'),
         why='The chuck branch\'s (i), lifted with its cue; scheme p16 names the chuck, '
             '"Centre lathe part Award 3 @ 5 Marks".',
         topic='eng-2-11', stem=False,
         question_lift=P(5, *_C6, more=[(118, 552, 208, 572)]),
         lifted=[S(16, 245, 109, 330, 129)], marks=[5], total=5,
         question_figure='engineering-2015-OL-paper-q6c-crop',
         notes="The scheme prints 'Centre lathe part Award 3 @ 5 Marks'. " + _OR6),
    dict(key=(6, 'c', 'ii'),
         why='The chuck branch\'s (ii): scheme p16 gives two operations, one a line, the 5 '
             'for the part not split between them.',
         topic='eng-2-11', stem=False,
         question_lift=P(5, *_C6, more=[(118, 573, 354, 592)]),
         lifted=[S(16, 245, 123, 420, 143), S(16, 245, 137, 340, 157)],
         tariff='questionTotal', total=5,
         question_figure='engineering-2015-OL-paper-q6c-crop',
         notes="The scheme prints 'Centre lathe part Award 3 @ 5 Marks'. " + _OR6),
    dict(key=(6, 'c', 'iii'),
         why='The chuck branch\'s (iii): scheme p16 gives one precaution, "Centre lathe part '
             'Award 3 @ 5 Marks".',
         topic='eng-3-1', stem=False,
         question_lift=P(5, *_C6, more=[(118, 594, 477, 613)]),
         lifted=[S(16, 243, 151, 430, 185)], marks=[5], total=5,
         question_figure='engineering-2015-OL-paper-q6c-crop',
         notes="The scheme prints 'Centre lathe part Award 3 @ 5 Marks'. " + _OR6),
    dict(key=(6, 'c', None),
         why='The OR branch, "Explain any three of the following" over four CNC terms set as '
             'romans; scheme p16 explains each after its roman, "Explanation Award 3 @ 5 '
             'Marks".',
         topic='eng-2-13', stem=False,
         question_lift=P(5, 95, 697, 515, 730, more=[(98, 739, 520, 758)]),
         lifted=[[S(16, 95, 236, 300, 256), S(16, 95, 249, 370, 269),
                  S(16, 95, 263, 440, 312), S(16, 95, 318, 430, 353)]],
         row_kind='anyN', group=(3, 5), marks=[15], tariff='fixed', total=15,
         notes="The scheme prints 'Any three terms: Explanation Award 3 @ 5 Marks'. " + _OR6),
    # ---- Question 7 --------------------------------------------------------
    dict(key=(7, 'a', None),
         why='A lead-in over three terms set as romans, "any two"; scheme p16 describes '
             'each under its name, "Description Award 2 @ 5 Marks".',
         topic='eng-3-12',
         lifted=[[join(S(16, 108, 473, 175, 493), S(16, 108, 487, 440, 507)),
                  join(S(16, 108, 514, 195, 534), S(16, 108, 528, 460, 576)),
                  join(S(16, 108, 583, 170, 603), S(16, 108, 597, 480, 645))]],
         row_kind='anyN', group=(2, 5), marks=[10], tariff='fixed', total=10,
         notes="The scheme prints 'Any two terms: Description Award 2 @ 5 Marks'."),
    dict(key=(7, 'b', None),
         why='The assembly is drawn with its dimensions beside (b); scheme p16 states each '
             'value after its roman, "Calculations Award 4 @ 5 Marks". The question is '
             'lifted with its romans, which the reader files as parts of their own.',
         topic='eng-3-12',
         question_lift=P(6, 95, 141, 442, 160, more=[(97, 164, 342, 183), (168, 184, 336, 204),
                                                     (168, 205, 344, 224),
                                                     (168, 226, 375, 273)]),
         lifted=[S(16, 108, 683, 340, 697), S(16, 108, 697, 340, 711),
                 S(16, 108, 711, 340, 725), S(16, 108, 725, 340, 739)],
         marks=[5, 5, 5, 5], total=20,
         question_figure='engineering-2015-OL-paper-q7b-crop',
         notes="The scheme prints 'Calculations Award 4 @ 5 Marks'."),
    dict(key=(7, 'c', None),
         why='Paper p6 sets two alternative (c)s either side of an OR. This card is the '
             'first branch, four instruments photographed and captioned (i)-(iv) with no '
             'words; scheme p17 names each with an application after its roman, "Any '
             'three", "Name & application Award 3 @ 5 Marks". The reader runs the OR '
             'branch\'s ask on into this one, so the question is lifted from the page.',
         topic='eng-3-12', stem=False,
         question_lift=P(6, 95, 309, 565, 328),
         lifted=[[S(17, 88, 95, 420, 115), S(17, 88, 109, 490, 129),
                  S(17, 88, 123, 440, 143), S(17, 88, 137, 475, 157)]],
         row_kind='anyN', group=(3, 5), marks=[15], tariff='fixed', total=15,
         question_figure='engineering-2015-OL-paper-q7c-crop',
         notes="The scheme prints 'Any three: Name & application Award 3 @ 5 Marks'. "
               + _OR7),
    dict(key=(7, 'c', 'i'),
         why='The OR branch: "Name each of the electronic components shown below and '
             'outline the function of each", three photographs captioned (i)-(iii); scheme '
             'p17 names each with its use, "Name & function Award 3 @ 5 Marks". The caption '
             'number stays with the picture, not the question text; the card\'s reference '
             'names the roman.',
         topic='eng-2-16', stem=False,
         question_lift=P(6, 95, 615, 525, 648),
         lifted=[join(S(17, 90, 263, 225, 283), S(17, 238, 263, 505, 297))], marks=[5],
         total=5,
         question_figure='engineering-2015-OL-paper-q7cor-crop',
         notes="The scheme prints 'Name & function Award 3 @ 5 Marks'. " + _OR7),
    dict(key=(7, 'c', 'ii'),
         why='The OR branch\'s second component; scheme p17 names it with its use, "Name & '
             'function Award 3 @ 5 Marks".',
         topic='eng-2-16', stem=False,
         question_lift=P(6, 95, 615, 525, 648),
         lifted=[join(S(17, 90, 291, 180, 311), S(17, 238, 291, 460, 325))], marks=[5],
         total=5,
         question_figure='engineering-2015-OL-paper-q7cor-crop',
         notes="The scheme prints 'Name & function Award 3 @ 5 Marks'. " + _OR7),
    dict(key=(7, 'c', 'iii'),
         why='The OR branch\'s third component; scheme p17 names it with its use, "Name & '
             'function Award 3 @ 5 Marks".',
         topic='eng-2-16', stem=False,
         question_lift=P(6, 95, 615, 525, 648),
         lifted=[join(S(17, 90, 318, 180, 338), S(17, 236, 318, 475, 352))], marks=[5],
         total=5,
         question_figure='engineering-2015-OL-paper-q7cor-crop',
         notes="The scheme prints 'Name & function Award 3 @ 5 Marks'. " + _OR7),
]

TOPICS = {}

ATLAS = {
    'eng-2015-ol-q5-b': dict(
        topics=['Polymers'],
        note='Safety when machining acrylic, which the reference files Q5 under; the card\'s '
             'syllabus heading is Health and safety.'),
    'eng-2015-ol-q6-c-iii': dict(
        topics=['CNC & Centre Lathe'],
        note='A safety precaution with the four jaw chuck on the centre lathe; the card\'s '
             'syllabus heading is Health and safety.'),
}
