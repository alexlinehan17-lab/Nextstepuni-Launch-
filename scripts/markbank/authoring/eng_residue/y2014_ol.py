"""2014 Ordinary Level: every part, from the page.

Paper and scheme as the PDFs number their pages. As in 2015-2019, the automatic
author prices nothing in this sitting: the scheme sets each answer in a left
column and its award in a box to the right ("Name Award 3 @ 4 Marks"), which
its reader does not join to the answer, so every card here is built from the
page by rectangle. The marks grid is on scheme p4: Question 1 is Section A,
"Any six @ 5 marks each", two-part answers 3 + 2, and Section B, "Any three
parts @ 12 + 12 + 11 Marks", two-part answers "6 + 6 or 6 + 5"; Questions 2-7
are 45 marks each. A Section B card carries the PRINTED primary price, the 12
the scheme awards a part answered first or second ("Award 12 (11) Marks"), and
says the third part answered earns 11.
"""
from eng_lift import join, lift

Y, L = 2014, 'ol'


def S(page, *rect):
    return lift(Y, L, 'scheme', page, rect)


def P(page, *rect, more=(), items=()):
    return lift(Y, L, 'paper', page, rect, more=more, items=items)


_A5 = (118, 565, 500, 584)            # paper p4: Q5(a)(i)'s line
_C6A = (95, 334, 310, 352)            # paper p5: the tailstock (c)
_ORW6 = (277, 479, 302, 498)          # paper p5: the OR between the two (c)s
_C6B = (95, 532, 245, 551)            # paper p5: the CNC lathe (c)

_SB = ("Section B is 'Any three parts @ 12 + 12 + 11 Marks': the card carries the 12 a part "
       "earns answered first or second; answered third it earns 11.")
_OR3 = ('The paper sets two (d)s either side of an OR, the metal properties and robotics in '
        'manufacturing; the scheme prices both "Award 2 @ 4 Marks", so they are one card, each '
        'branch a route.')
_OR6 = ('The paper sets two (c)s either side of an OR, the tailstock and the CNC lathe; the '
        'scheme prices the romans of both "Award 3 @ 5 Marks", so each roman is one card, each '
        'branch a route.')
_OR7 = ('The paper sets two (c)s either side of an OR: the instruments (c), carded at the '
        'letter, and the electronic components (c), one card for each symbol drawn and '
        'captioned (i)-(iii).')

CROPS = {
    # ---- paper ------------------------------------------------------------
    'engineering-2014-OL-paper-q1a-crop': dict(
        doc='paper', page=2, rect=(475, 69, 548, 136), image=True, ref='2014 OL Q1(a)'),
    'engineering-2014-OL-paper-q1d-crop': dict(
        doc='paper', page=2, rect=(470, 171, 530, 203), ref='2014 OL Q1(d)'),
    # The hacksaw with the two arrows drawn under its blade.
    'engineering-2014-OL-paper-q1f-crop': dict(
        doc='paper', page=2, rect=(433, 232, 536, 272), ref='2014 OL Q1(f)'),
    # The two thread forms with their captions (i) and (ii).
    'engineering-2014-OL-paper-q1g-crop': dict(
        doc='paper', page=2, rect=(60, 291.5, 480, 328), ref='2014 OL Q1(g)'),
    'engineering-2014-OL-paper-q1h-crop': dict(
        doc='paper', page=2, rect=(402, 336, 525, 378), image=True, ref='2014 OL Q1(h)'),
    # The three items photographed with their captions.
    'engineering-2014-OL-paper-q1i-crop': dict(
        doc='paper', page=2, rect=(62, 512, 552, 598), ref='2014 OL Q1(i)'),
    # The two drive systems with their captions (i) and (ii).
    'engineering-2014-OL-paper-q1m-crop': dict(
        doc='paper', page=2, rect=(326, 748, 540, 812), ref='2014 OL Q1(m)'),
    # The three components, under the romans that name them.
    'engineering-2014-OL-paper-q2a-crop': dict(
        doc='paper', page=3, rect=(95, 92, 515, 170), ref='2014 OL Q2(a)'),
    'engineering-2014-OL-paper-q3b-crop': dict(
        doc='paper', page=3, rect=(95, 556, 490, 597), ref='2014 OL Q3(b)'),
    'engineering-2014-OL-paper-q3c-crop': dict(
        doc='paper', page=3, rect=(429, 612, 531, 672), image=True, ref='2014 OL Q3(c)'),
    'engineering-2014-OL-paper-q4cii-crop': dict(
        doc='paper', page=4, rect=(501, 196, 559, 250), image=True, ref='2014 OL Q4(c)(ii)'),
    'engineering-2014-OL-paper-q4civ-crop': dict(
        doc='paper', page=4, rect=(497, 271, 543, 316), image=True, ref='2014 OL Q4(c)(iv)'),
    'engineering-2014-OL-paper-q4d-crop': dict(
        doc='paper', page=4, rect=(321, 308, 450, 360), image=True, ref='2014 OL Q4(d)'),
    # The three processes drawn with A, B and C above them.
    'engineering-2014-OL-paper-q5a-crop': dict(
        doc='paper', page=4, rect=(100, 428, 568, 558), ref='2014 OL Q5(a)',
        letters=('A', 'B', 'C')),
    'engineering-2014-OL-paper-q6a-crop': dict(
        doc='paper', page=5, rect=(238, 104, 356, 222), ref='2014 OL Q6(a)'),
    # Both (c)s' pictures: the tailstock, then the CNC lathe.
    'engineering-2014-OL-paper-q6c-crop': dict(
        doc='paper', parts=[(5, (441, 330, 550, 448)), (5, (221, 548, 395, 684))],
        layout='row', ref='2014 OL Q6(c)'),
    # The plate and its hole with the dimension 43 +/- 0.05 mm.
    'engineering-2014-OL-paper-q7b-crop': dict(
        doc='paper', page=6, rect=(383, 160, 580, 326), ref='2014 OL Q7(b)'),
    'engineering-2014-OL-paper-q7c-crop': dict(
        doc='paper', page=6, rect=(35, 416, 572, 546), ref='2014 OL Q7(c)'),
    # The OR branch's three circuit symbols, captioned (i)-(iii).
    'engineering-2014-OL-paper-q7cor-crop': dict(
        doc='paper', page=6, rect=(112, 668, 518, 784), ref='2014 OL Q7(c)'),
    # ---- scheme: the drawings the answers are given with -------------------
    'engineering-2014-OL-scheme-q2cii-sol': dict(
        doc='scheme', parts=[(9, (90, 88, 277, 296)), (9, (48, 297, 236, 432)),
                             (9, (90, 450, 254, 658))],
        layout='row', solution=True, ref='2014 OL Q2(c)(ii)'),
    'engineering-2014-OL-scheme-q4a-sol': dict(
        doc='scheme', parts=[(11, (306, 179, 462, 226)), (11, (322, 278, 462, 327)),
                             (11, (310, 397, 462, 440))],
        solution=True, ref='2014 OL Q4(a)'),
    'engineering-2014-OL-scheme-q5b-sol': dict(
        doc='scheme', parts=[(14, (88, 185, 262, 288)), (14, (95, 418, 345, 565))],
        layout='row', solution=True, ref='2014 OL Q5(b)'),
    'engineering-2014-OL-scheme-q7a-sol': dict(
        doc='scheme', parts=[(16, (225, 586, 428, 660)), (16, (225, 708, 428, 782))],
        solution=True, ref='2014 OL Q7(a)'),
}

CARDS = [
    # ---- Question 1, Section A ("Any six @ 5 marks each") ------------------
    dict(key=(1, 'a', None),
         why='The scroll saw is photographed beside (a); scheme p5 numbers two precautions; '
             '"3 + 2 Marks".',
         topic='eng-3-1',
         lifted=[S(5, 88, 347, 460, 360), S(5, 88, 360, 460, 373)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         question_figure='engineering-2014-OL-paper-q1a-crop',
         notes="The scheme prints '3 + 2 Marks'."),
    dict(key=(1, 'b', None),
         why='Scheme p5 explains the term in one sentence with examples, "5 Marks".',
         topic='eng-2-10',
         lifted=[S(5, 70, 386, 450, 416)], marks=[5], total=5,
         notes="The scheme prints '5 Marks'."),
    dict(key=(1, 'c', None),
         why='Scheme p5 numbers two devices on one line, each lifted by its own word '
             'rectangle; "3 + 2 Marks".',
         topic='eng-3-14',
         lifted=[S(5, 84, 428, 138, 446), S(5, 155, 428, 195, 446)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         notes="The scheme prints '3 + 2 Marks'."),
    dict(key=(1, 'd', None),
         why='The symbol is drawn beside (d); scheme p5 names the component and then gives '
             'its use; "3 + 2 Marks".',
         topic='eng-2-16',
         lifted=[S(5, 70, 465, 117, 483),
                 join(S(5, 117, 465, 470, 483), S(5, 70, 478, 440, 494),
                      S(5, 70, 492, 215, 508))],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         question_figure='engineering-2014-OL-paper-q1d-crop',
         notes="The scheme prints '3 + 2 Marks'."),
    dict(key=(1, 'e', None),
         why='Scheme p5 answers in one sentence, "5 Marks".',
         topic='eng-1-9',
         lifted=[S(5, 68, 534, 340, 552)], marks=[5], total=5,
         notes="The scheme prints '5 Marks'."),
    dict(key=(1, 'f', None),
         why='The hacksaw is photographed beside (f); scheme p5 answers in one sentence, '
             '"5 Marks".',
         topic='eng-3-8',
         lifted=[S(5, 70, 575, 385, 593)], marks=[5], total=5,
         question_figure='engineering-2014-OL-paper-q1f-crop',
         notes="The scheme prints '5 Marks'."),
    dict(key=(1, 'g', None),
         why='The two thread forms are drawn and captioned (i) and (ii); scheme p5 names '
             'each after its roman; "3 + 2 Marks".',
         topic='eng-2-11',
         lifted=[S(5, 70, 616, 180, 632), S(5, 70, 630, 172, 646)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         question_figure='engineering-2014-OL-paper-q1g-crop',
         notes="The scheme prints '3 + 2 Marks'."),
    dict(key=(1, 'h', None),
         why='The instrument is photographed beside (h); scheme p5 names it and then gives '
             'its use; "3+2 Marks". The reader joins the Section B heading to (h), so the '
             'question is lifted from the page.',
         topic='eng-3-12',
         question_lift=P(2, 60, 331, 430, 362),
         lifted=[S(5, 66, 672, 320, 690),
                 join(S(5, 318, 672, 475, 690), S(5, 70, 685, 415, 701),
                      S(5, 70, 699, 315, 715))],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         question_figure='engineering-2014-OL-paper-q1h-crop',
         notes="The scheme prints '3+2 Marks'."),
    # ---- Question 1, Section B ("Any three parts @ 12 + 12 + 11 Marks") ----
    dict(key=(1, 'i', None),
         why='The three items are photographed and captioned under (i); scheme p6 '
             'describes each under its name; "Any one", "Award 12 (11) Marks". The '
             'question is lifted with each caption on its own line, as the paper sets them '
             'under their pictures.',
         topic='eng-2-10', stem=False,
         question_lift=P(2, 60, 491, 385, 510, items=[(73, 578, 160, 597),
                                                      (222, 578, 370, 597),
                                                      (426, 578, 506, 597)]),
         lifted=[[S(6, 88, 115, 445, 229), S(6, 88, 253, 440, 339),
                  S(6, 85, 364, 455, 449)]],
         row_kind='anyN', group=(1, 12), marks=[12], tariff='fixed', total=12,
         question_figure='engineering-2014-OL-paper-q1i-crop',
         notes="The scheme prints 'Any one: Good clear description Award 12 (11) Marks'. "
               + _SB),
    dict(key=(1, 'j', None),
         why='Scheme pp6-7 explain each term under its name, "Any two", "Award 6 + 6(5) '
             'Marks".',
         topic='eng-3-14', stem=False,
         lifted=[[S(6, 88, 499, 445, 585), S(6, 88, 591, 482, 663),
                  S(6, 88, 669, 502, 741), S(7, 64, 71, 442, 157)]],
         row_kind='anyN', group=(2, 6), marks=[12], tariff='fixed', total=12,
         notes="The scheme prints 'Any two: Good clear description Award 6 + 6(5) Marks'. "
               + _SB),
    dict(key=(1, 'k', None),
         why='Scheme p7 defines the term and gives examples, each under its heading; '
             '"Definition Award 6 Marks", "Example Award 6(5) Marks".',
         topic='eng-3-8', stem=False,
         lifted=[S(7, 85, 184, 440, 229), S(7, 85, 239, 440, 270)],
         marks=[6, 6], total=12,
         notes="The scheme prints 'Definition Award 6 Marks' and 'Example Award 6(5) Marks'. "
               + _SB),
    dict(key=(1, 'l', None),
         why='Scheme p7 explains each term under its name, "Any two", "Award 6 + 6 (5) '
             'Marks".',
         topic='eng-3-14', stem=False,
         lifted=[[S(7, 82, 309, 432, 369), S(7, 82, 393, 500, 452),
                  S(7, 82, 462, 505, 521), S(7, 82, 545, 445, 617)]],
         row_kind='anyN', group=(2, 6), marks=[12], tariff='fixed', total=12,
         notes="The scheme prints 'Any two: Good description Award 6 + 6 (5) Marks'. " + _SB),
    dict(key=(1, 'm', None),
         why='The two drives are photographed and captioned (i) and (ii); scheme p7 names '
             'each after its roman, "Name Award 6 + 6 (5)".',
         topic='eng-2-15', stem=False,
         lifted=[S(7, 79, 674, 240, 692), S(7, 240, 674, 370, 692)],
         marks=[6, 6], total=12,
         question_figure='engineering-2014-OL-paper-q1m-crop',
         notes="The scheme prints 'Name Award 6 + 6 (5)', for (i) and (ii) in that order. "
               + _SB),
    # ---- Question 2 --------------------------------------------------------
    dict(key=(2, 'a', None),
         why='The three components are captioned (i)-(iii) over their photographs; scheme '
             'p8 names a material for each after its roman, "Name Award 3 @ 4 Marks". One '
             'card at the letter, a row a component.',
         topic='eng-3-8',
         lifted=[S(8, 88, 144, 360, 160), S(8, 88, 158, 360, 174), S(8, 88, 172, 360, 188)],
         marks=[4, 4, 4], total=12,
         question_figure='engineering-2014-OL-paper-q2a-crop',
         notes="The scheme prints 'Name Award 3 @ 4 Marks'."),
    dict(key=(2, 'b', None),
         why='A lead-in over four terms set as romans, "any three"; scheme p8 describes '
             'each under its name, "Good clear description Award 3 @ 3 Marks".',
         topic='eng-1-4',
         lifted=[[S(8, 82, 269, 440, 313), S(8, 85, 338, 440, 395),
                  S(8, 82, 421, 440, 478), S(8, 82, 504, 450, 561)]],
         row_kind='anyN', group=(3, 3), marks=[9], tariff='fixed', total=9,
         notes="The scheme prints 'Good clear description Award 3 @ 3 Marks'."),
    dict(key=(2, 'c', 'i'),
         why='"Any two of the metals listed": scheme p8 sets each metal beside its furnace '
             'in two columns, "Name Award 2 @ 4 Marks".',
         topic='eng-1-4',
         lifted=[[S(8, 79, 655, 370, 671), S(8, 79, 669, 370, 685), S(8, 79, 683, 370, 699)]],
         row_kind='anyN', group=(2, 4), marks=[8], tariff='fixed', total=8,
         notes="The scheme prints 'Any two: Name Award 2 @ 4 Marks'."),
    dict(key=(2, 'c', 'ii'),
         why='"Any one": scheme p9 describes the cupola, the electric arc and the blast '
             'furnace under their names, each beside a drawing of it, shown with the '
             'answer; "Good clear description Award 8 Marks".',
         topic='eng-1-4',
         lifted=[[S(9, 315, 105, 550, 240), S(9, 286, 298, 560, 413),
                  S(9, 292, 465, 550, 616)]],
         row_kind='anyN', group=(1, 8), marks=[8], tariff='fixed', total=8,
         figure='engineering-2014-OL-scheme-q2cii-sol',
         notes="The scheme prints 'Any one: Good clear description Award 8 Marks'."),
    dict(key=(2, 'd', None),
         why='Scheme p9 sets each alloy beside its uses in two columns, "Name Award 2 @ 4 '
             'Marks". "Statutes" is the scheme\'s spelling.',
         topic='eng-1-5',
         lifted=[S(9, 79, 706, 380, 722), S(9, 79, 720, 380, 736)],
         marks=[4, 4], total=8,
         notes="The scheme prints 'Name Award 2 @ 4 Marks'."),
    # ---- Question 3 --------------------------------------------------------
    dict(key=(3, 'a', 'i'),
         why='Scheme p10 bullets two reasons, "Award 2 @ 4 Marks".',
         topic='eng-2-6',
         lifted=[S(10, 120, 115, 420, 131), S(10, 120, 130, 420, 146)],
         marks=[4, 4], total=8,
         notes="The scheme prints '(i) Award 2 @ 4 Marks'."),
    dict(key=(3, 'a', 'ii'),
         why='Scheme p10 names the three processes on one line, each lifted by its own word '
             'rectangle; "Award 3 @ 3 Marks".',
         topic='eng-2-6',
         lifted=[S(10, 124, 158, 181, 174), S(10, 181, 158, 239, 174),
                 S(10, 239, 158, 300, 174)],
         marks=[3, 3, 3], total=9,
         notes="The scheme prints '(ii) Award 3 @ 3 Marks'."),
    dict(key=(3, 'b', None),
         why='The file is drawn under (b); scheme p10 describes the hardening and the '
             'tempering under their headings, "Good Description Award 2 @ 7 Marks".',
         topic='eng-2-6',
         lifted=[S(10, 105, 200, 440, 271), S(10, 105, 283, 452, 353)],
         marks=[7, 7], total=14,
         question_figure='engineering-2014-OL-paper-q3b-crop',
         notes="The scheme prints 'Good Description Award 2 @ 7 Marks'."),
    dict(key=(3, 'c', None),
         why='The goggles are photographed beside (c); scheme p10 bullets two reasons, '
             '"Reasons Award 2 @ 3 Marks".',
         topic='eng-3-1',
         lifted=[S(10, 124, 420, 440, 436), S(10, 124, 434, 440, 465)],
         marks=[3, 3], total=6,
         question_figure='engineering-2014-OL-paper-q3c-crop',
         notes="The scheme prints 'Reasons Award 2 @ 3 Marks'."),
    dict(key=(3, 'd', None),
         why='Paper p3 sets two alternative (d)s either side of an OR. Scheme p10 explains '
             'each metal property under its name, "Any two terms", "Explanation Award 2 @ 4 '
             'Marks", and bullets two advantages of robotics, "Award 2 @ 4 Marks": priced '
             'alike, one card with a route per branch.',
         topic='eng-3-8', stem=False,
         question_lift=P(3, 95, 665, 350, 684, more=[(97, 688, 520, 707), (258, 726, 285, 746),
                                                     (95, 764, 438, 783)]),
         lifted=[[S(10, 108, 531, 450, 573), S(10, 108, 572, 476, 601),
                  S(10, 108, 600, 470, 643)],
                 S(10, 120, 699, 440, 730), S(10, 120, 727, 440, 758)],
         row_kind='anyN', group=[(2, 4), None, None], marks=[8, 4, 4],
         routes=['a', 'b', 'b'], tariff='fixed', total=8,
         notes="The scheme prints 'Explanation Award 2 @ 4 Marks' and, for the OR, 'Award 2 @ "
               "4 Marks'. " + _OR3),
    # ---- Question 4 --------------------------------------------------------
    dict(key=(4, 'a', None),
         why='"With the aid of suitable diagrams": scheme p11 describes each flame under its '
             'name, over a drawing of it, shown with the answer; "Description Award 3 @ 5 '
             'Marks".',
         topic='eng-2-10',
         lifted=[S(11, 100, 114, 440, 173), S(11, 99, 226, 452, 270), S(11, 99, 322, 470, 393)],
         marks=[5, 5, 5], total=15,
         figure='engineering-2014-OL-scheme-q4a-sol',
         notes="The scheme prints 'Description Award 3 @ 5 Marks'."),
    dict(key=(4, 'b', None),
         why='A lead-in over four terms set as romans, "any three"; scheme pp11-12 explain '
             'each under its name, "Explanation Award 3 @ 4 Marks".',
         topic='eng-2-10',
         lifted=[[S(11, 97, 474, 452, 560), S(11, 99, 571, 456, 643),
                  S(11, 102, 653, 490, 711), S(12, 102, 71, 492, 130)]],
         row_kind='anyN', group=(3, 4), marks=[12], tariff='fixed', total=12,
         notes="The scheme prints 'Any three: Explanation Award 3 @ 4 Marks'."),
    dict(key=(4, 'c', 'i'),
         why='One of "Answer any three of the following", "Award 3 @ 4 Marks": scheme p12 '
             'gives two reasons in two sentences, each lifted by its own rectangle; the 4 '
             'for the part is not split between them.',
         topic='eng-2-10',
         lifted=[S(12, 115, 223, 440, 253), S(12, 115, 251, 400, 267)],
         tariff='questionTotal', total=4,
         notes="The scheme prints 'Any three: Award 3 @ 4 Marks' for the three parts "
               "answered."),
    dict(key=(4, 'c', 'ii'),
         why='One of "Answer any three of the following": the screw is photographed beside '
             'it; scheme p12 names it and gives its use, the 4 not split between them.',
         topic='eng-2-10',
         lifted=[S(12, 115, 292, 240, 308), S(12, 115, 306, 460, 349)],
         tariff='questionTotal', total=4,
         question_figure='engineering-2014-OL-paper-q4cii-crop',
         notes="The scheme prints 'Any three: Award 3 @ 4 Marks' for the three parts "
               "answered."),
    dict(key=(4, 'c', 'iii'),
         why='One of "Answer any three of the following": scheme p12 gives two precautions '
             'on two lines, the 4 for the part not split between them.',
         topic='eng-2-10',
         lifted=[S(12, 118, 375, 490, 391), S(12, 118, 389, 430, 405)],
         tariff='questionTotal', total=4,
         notes="The scheme prints 'Any three: Award 3 @ 4 Marks' for the three parts "
               "answered."),
    dict(key=(4, 'c', 'iv'),
         why='One of "Answer any three of the following": the washer is photographed beside '
             'it; scheme p12 names it and gives its use on one line, each lifted by its own '
             'word rectangle, the 4 not split between them.',
         topic='eng-2-10',
         lifted=[S(12, 118, 430, 195, 446), S(12, 195, 430, 492, 446)],
         tariff='questionTotal', total=4,
         question_figure='engineering-2014-OL-paper-q4civ-crop',
         notes="The scheme prints 'Any three: Award 3 @ 4 Marks' for the three parts "
               "answered."),
    dict(key=(4, 'd', None),
         why='The soldering iron is photographed beside (d); scheme p12 bullets two '
             'precautions, "Safety Precautions Award 2 @ 3 Marks".',
         topic='eng-3-1',
         lifted=[S(12, 124, 553, 440, 569), S(12, 124, 569, 400, 585)],
         marks=[3, 3], total=6,
         question_figure='engineering-2014-OL-paper-q4d-crop',
         notes="The scheme prints 'Safety Precautions Award 2 @ 3 Marks'."),
    # ---- Question 5 --------------------------------------------------------
    dict(key=(5, 'a', 'i'),
         why='The three processes are drawn and lettered A, B and C; scheme p13 names each '
             'after its letter on its own line, "Name Award 3 @ 3 Marks". "molulding" is '
             'the scheme\'s spelling.',
         topic='eng-1-9', stem=False,
         question_lift=P(4, *_A5),
         lifted=[S(13, 96, 129, 290, 145), S(13, 96, 143, 290, 159), S(13, 96, 156, 290, 172)],
         marks=[3, 3, 3], total=9,
         labels={'A': S(13, 158, 129, 290, 145), 'B': S(13, 158, 143, 290, 159),
                 'C': S(13, 158, 156, 290, 172)},
         question_figure='engineering-2014-OL-paper-q5a-crop',
         notes="The scheme prints 'Name Award 3 @ 3 Marks'."),
    dict(key=(5, 'a', 'ii'),
         why='"Any one process": scheme p13 describes each process under its name and ends '
             'each with the components it makes, "Process Award 9 Marks", "Component Award '
             '3 Marks". The description and the component sentence are each lifted by their '
             'own rectangles, whichever process.',
         topic='eng-1-9', stem=False,
         question_lift=P(4, 118, 588, 555, 621),
         lifted=[[S(13, 94, 252, 430, 366), S(13, 90, 433, 460, 531), S(13, 94, 598, 435, 655)],
                 [S(13, 94, 377, 440, 393), S(13, 90, 543, 425, 559), S(13, 94, 667, 450, 697)]],
         marks=[9, 3], total=12,
         question_figure='engineering-2014-OL-paper-q5a-crop',
         notes="The scheme prints 'Any one process: Process Award 9 Marks' and 'Component "
               "Award 3 Marks', for the process chosen."),
    dict(key=(5, 'b', None),
         why='"The operation of one of the following and identify a suitable application": '
             'scheme p14 describes the strip heater and the dip coating tank under their '
             'names, each over a drawing of it, shown with the answer, and gives each one\'s '
             'application beside the drawing; "Any one", "Description Award 9 Marks", '
             '"Application Award 3 Marks". One card, each branch a route.',
         topic='eng-1-9',
         lifted=[S(14, 104, 85, 445, 170), S(14, 278, 209, 455, 253),
                 join(S(14, 106, 306, 232, 322), S(14, 88, 320, 455, 405)),
                 S(14, 389, 452, 530, 552)],
         marks=[9, 3, 9, 3], routes=['a', 'a', 'b', 'b'], total=12,
         figure='engineering-2014-OL-scheme-q5b-sol',
         notes="The scheme prints 'Any one: Description Award 9 Marks, Application Award 3 "
               "Marks'."),
    dict(key=(5, 'c', None),
         why='Scheme p14 bullets two precautions, "Safety precautions Award 2 @ 3 Marks".',
         topic='eng-3-1',
         lifted=[S(14, 122, 610, 435, 626), S(14, 122, 625, 435, 656)],
         marks=[3, 3], total=6,
         notes="The scheme prints 'Safety precautions Award 2 @ 3 Marks'."),
    dict(key=(5, 'd', None),
         why='Scheme p14 sets each item beside its plastic in two columns, "Name Award 2 @ 3 '
             'Marks". One card at the letter, a row an item. "Ploystyrene" is the scheme\'s '
             'spelling.',
         topic='eng-1-9',
         lifted=[S(14, 118, 708, 375, 724), S(14, 118, 722, 375, 738)],
         marks=[3, 3], total=6,
         notes="The scheme prints 'Name Award 2 @ 3 Marks'."),
    # ---- Question 6 --------------------------------------------------------
    dict(key=(6, 'a', None),
         why='The wheel is drawn under (a); scheme p15 describes five turning operations '
             'under their names, any three, "Description Award 3 @ 5 Marks".',
         topic='eng-2-11',
         lifted=[[S(15, 94, 130, 440, 172), S(15, 94, 185, 440, 228), S(15, 97, 240, 455, 297),
                  S(15, 96, 309, 485, 379), S(15, 96, 392, 472, 448)]],
         row_kind='anyN', group=(3, 5), marks=[15], tariff='fixed', total=15,
         question_figure='engineering-2014-OL-paper-q6a-crop',
         notes="The scheme prints 'Any three turning operations: Description Award 3 @ 5 "
               "Marks'."),
    dict(key=(6, 'b', None),
         why='A lead-in over four terms set as romans, "any three"; scheme p15 explains '
             'each under its name, "Explanation Award 3 @ 5 Marks".',
         topic='eng-2-11',
         lifted=[[join(S(15, 105, 513, 440, 529), S(15, 88, 528, 440, 560)),
                  join(S(15, 106, 571, 170, 587), S(15, 88, 585, 465, 629)),
                  join(S(15, 109, 640, 160, 656), S(15, 88, 654, 492, 698)),
                  join(S(15, 108, 709, 195, 725), S(15, 90, 723, 505, 767))]],
         row_kind='anyN', group=(3, 5), marks=[15], tariff='fixed', total=15,
         notes="The scheme prints 'Any three terms: Explanation Award 3 @ 5 Marks'."),
    dict(key=(6, 'c', 'i'),
         why='Both (c)s price their (i) at 5 (scheme p16): the tailstock\'s name, or what '
             'CNC stands for. One card for the printed OR, each branch a route.',
         topic='eng-2-11', stem=False,
         question_lift=P(5, *_C6A, more=[(118, 359, 225, 378), _ORW6, _C6B,
                                         (118, 697, 292, 716)]),
         lifted=[S(16, 230, 113, 285, 131), S(16, 98, 313, 250, 331)],
         marks=[5, 5], routes=['a', 'b'], total=5,
         question_figure='engineering-2014-OL-paper-q6c-crop',
         notes="The scheme prints 'Award 3 @ 5 Marks' for each (c). " + _OR6),
    dict(key=(6, 'c', 'ii'),
         why='Both (c)s price their (ii) at 5 (scheme p16): two operations with the '
             'tailstock, which the scheme names on one line, or one advantage of a CNC '
             'lathe. One card, each branch a route.',
         topic='eng-2-11', stem=False,
         question_lift=P(5, *_C6A, more=[(118, 380, 432, 413), _ORW6, _C6B,
                                         (118, 718, 415, 737)]),
         lifted=[S(16, 230, 140, 460, 158), S(16, 100, 340, 320, 358)],
         marks=[5, 5], routes=['a', 'b'], total=5,
         question_figure='engineering-2014-OL-paper-q6c-crop',
         notes="The scheme prints 'Award 3 @ 5 Marks' for each (c), and names the two "
               "operations on one line. " + _OR6),
    dict(key=(6, 'c', 'iii'),
         why='Both (c)s price their (iii) at 5 (scheme p16): one precaution with the '
             'tailstock, or one with a CNC lathe. One card, each branch a route.',
         topic='eng-3-1', stem=False,
         question_lift=P(5, *_C6A, more=[(118, 414, 432, 447), _ORW6, _C6B,
                                         (118, 739, 470, 758)]),
         lifted=[S(16, 230, 168, 445, 212), S(16, 100, 368, 366, 386)],
         marks=[5, 5], routes=['a', 'b'], total=5,
         question_figure='engineering-2014-OL-paper-q6c-crop',
         notes="The scheme prints 'Award 3 @ 5 Marks' for each (c). " + _OR6),
    # ---- Question 7 --------------------------------------------------------
    dict(key=(7, 'a', None),
         why='"Using sketches": scheme p16 describes each fit under its name, beside a '
             'drawing of it, shown with the answer; "Differences Award 2 @ 5 Marks".',
         topic='eng-3-12',
         lifted=[join(S(16, 103, 537, 175, 553), S(16, 106, 551, 436, 593)),
                 join(S(16, 106, 661, 190, 677), S(16, 106, 675, 460, 714))],
         marks=[5, 5], total=10,
         figure='engineering-2014-OL-scheme-q7a-sol',
         notes="The scheme prints 'Differences Award 2 @ 5 Marks'."),
    dict(key=(7, 'b', None),
         why='The hole is drawn with its dimension beside (b); scheme p17 states each value '
             'after its roman, "Calculations Award 4 @ 5 Marks". The question is lifted '
             'with its romans, which the reader files as parts of their own.',
         topic='eng-3-12', stem=False,
         question_lift=P(6, 95, 141, 395, 160, more=[(97, 164, 340, 183), (168, 184, 340, 204),
                                                     (168, 205, 340, 224),
                                                     (168, 226, 340, 245)]),
         lifted=[S(17, 64, 113, 340, 129), S(17, 85, 126, 340, 142),
                 S(17, 85, 140, 340, 156), S(17, 85, 154, 340, 170)],
         marks=[5, 5, 5, 5], total=20,
         question_figure='engineering-2014-OL-paper-q7b-crop',
         notes="The scheme prints 'Calculations Award 4 @ 5 Marks'."),
    dict(key=(7, 'c', None),
         why='Paper p6 sets two alternative (c)s either side of an OR. This card is the '
             'first branch, four instruments photographed and captioned (i)-(iv) with no '
             'words; scheme p17 names each with an application after its roman, "Any '
             'three", "Name & application Award 3 @ 5 Marks".',
         topic='eng-3-12', stem=False,
         question_lift=P(6, 95, 364, 565, 383),
         lifted=[[S(17, 82, 264, 470, 280), S(17, 82, 278, 486, 294),
                  join(S(17, 82, 292, 490, 308), S(17, 220, 306, 260, 322)),
                  S(17, 82, 320, 450, 336)]],
         row_kind='anyN', group=(3, 5), marks=[15], tariff='fixed', total=15,
         question_figure='engineering-2014-OL-paper-q7c-crop',
         notes="The scheme prints 'Any three: Name & application Award 3 @ 5 Marks'. "
               + _OR7),
    dict(key=(7, 'c', 'i'),
         why='The OR branch: "Name each of the electronic components represented by the '
             'circuit symbols shown and outline the function of each", three symbols '
             'captioned (i)-(iii); scheme p17 names each with its use, "Name & function '
             'Award 3 @ 5 Marks". The caption number stays with the drawing, not the '
             'question text; the card\'s reference names the roman.',
         topic='eng-2-16', stem=False,
         question_lift=P(6, 95, 628, 560, 661),
         lifted=[S(17, 112, 474, 470, 490)], marks=[5], total=5,
         question_figure='engineering-2014-OL-paper-q7cor-crop',
         notes="The scheme prints 'Name & function Award 3 @ 5 Marks'. " + _OR7),
    dict(key=(7, 'c', 'ii'),
         why='The OR branch\'s second symbol; scheme p17 names it with its use, "Name & '
             'function Award 3 @ 5 Marks".',
         topic='eng-2-16', stem=False,
         question_lift=P(6, 95, 628, 560, 661),
         lifted=[S(17, 112, 488, 390, 504)], marks=[5], total=5,
         question_figure='engineering-2014-OL-paper-q7cor-crop',
         notes="The scheme prints 'Name & function Award 3 @ 5 Marks'. " + _OR7),
    dict(key=(7, 'c', 'iii'),
         why='The OR branch\'s third symbol; scheme p17 names it with its use, "Name & '
             'function Award 3 @ 5 Marks".',
         topic='eng-2-16', stem=False,
         question_lift=P(6, 95, 628, 560, 661),
         lifted=[S(17, 113, 501, 422, 517)], marks=[5], total=5,
         question_figure='engineering-2014-OL-paper-q7cor-crop',
         notes="The scheme prints 'Name & function Award 3 @ 5 Marks'. " + _OR7),
]

TOPICS = {}

ATLAS = {
    'eng-2014-ol-q3-c': dict(
        topics=['Heat Treatment'],
        note='Safety goggles when heat treating metals, which the reference files Q3 under; the '
             'card\'s syllabus heading is Health and safety.'),
}
