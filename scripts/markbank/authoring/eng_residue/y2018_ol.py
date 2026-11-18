"""2018 Ordinary Level: every part, from the page.

Paper and scheme as the PDFs number their pages. As in 2019, the automatic
author prices nothing in this sitting: the scheme sets each answer in a left
column and its award in a box to the right ("Name and function Award 3 @ 4
Marks"), which its reader does not join to the answer, so every card here is
built from the page by rectangle. The marks grid is on scheme p4: Question 1
is Section A, "Any six @ 5 marks each", two-part answers 3 + 2, and Section
B, "Any three parts @ 12 + 12 + 11 marks"; Questions 2-7 are 45 marks each. A
Section B card carries the 12 the scheme awards a part answered first or
second ("Award 12 (11) Marks"), and says the third part answered earns 11.
"""
from eng_lift import join, lift

Y, L = 2018, 'ol'
OWNED = ('never shipped: the automatic author builds this card only from the lifts this '
         'entry records, so the entry owns it')


def S(page, *rect):
    return lift(Y, L, 'scheme', page, rect)


def P(page, *rect, more=(), items=()):
    return lift(Y, L, 'paper', page, rect, more=more, items=items)


_B2 = (82, 300, 482, 316)             # paper p3: Q2(b)'s lead-in
_C4 = (84, 414, 257, 430)             # paper p5: Q4(c)'s "Answer any three of the following:"
_B5 = (84, 383, 391, 399)             # paper p6: Q5(b)'s lead-in
_A5 = (84, 80, 480, 96)               # paper p6: Q5(a)'s lead-in
_C6 = (84, 517, 297, 533)             # paper p7: Q6(c)'s lead-in

_SB = ("Section B is 'Any three parts @ 12 + 12 + 11 marks': the card carries the 12 a part "
       "earns answered first or second; answered third it earns 11.")
_OR3 = ('The paper sets two (d)s either side of an OR, the metal properties and robotics in '
        'industry; the scheme prices both "Award 2 @ 4 Marks", so they are one card, each '
        'branch a route.')
_OR6 = ('The paper sets two (c)s either side of an OR: the toolpost (c), whose (i)-(iii) are '
        'carded apart, and the CNC lathe (c), carded at the letter.')
_OR7 = ('The paper sets two (c)s either side of an OR: the instruments (c), carded at the '
        'letter, and the electronic components (c), whose (i) and (ii) are carded apart.')
_CK = 'the semicolon is the list running on'

CROPS = {
    # ---- paper ------------------------------------------------------------
    # The LED without the end of (d)'s line above it or the corner of the USB
    # cable photographed beside (h).
    'engineering-2018-OL-paper-q1f-crop': dict(
        doc='paper', page=2, rect=(346, 226, 454, 333), mask=[(344, 313, 353, 335)],
        ref='2018 OL Q1(f)'),
    'engineering-2018-OL-paper-q1i-crop': dict(
        doc='paper', page=2, rect=(60, 480, 545, 584), ref='2018 OL Q1(i)'),
    'engineering-2018-OL-paper-q2a-crop': dict(
        doc='paper', page=3, rect=(50, 112, 570, 280), ref='2018 OL Q2(a)'),
    'engineering-2018-OL-paper-q2d-crop': dict(
        doc='paper', page=3, rect=(95, 652, 556, 770), ref='2018 OL Q2(d)'),
    'engineering-2018-OL-paper-q4b-crop': dict(
        doc='paper', page=5, rect=(80, 228, 552, 358), ref='2018 OL Q4(b)'),
    'engineering-2018-OL-paper-q6a-crop': dict(
        doc='paper', page=7, rect=(412, 98, 530, 212), ref='2018 OL Q6(a)'),
    # The hole and shaft with both dimensions; the end of (b)'s first line
    # runs into the drawing's top edge and is whited out.
    'engineering-2018-OL-paper-q7b-crop': dict(
        doc='paper', page=8, rect=(355, 166, 570, 326), mask=[(353, 172, 390, 189)],
        ref='2018 OL Q7(b)'),
    'engineering-2018-OL-paper-q7c-crop': dict(
        doc='paper', page=8, rect=(42, 385, 560, 526), ref='2018 OL Q7(c)'),
    # The OR branch's circuit with its components lettered A-D; the branch's
    # own (i) runs beside the switch and is whited out.
    'engineering-2018-OL-paper-q7cor-crop': dict(
        doc='paper', page=8, rect=(260, 577, 560, 790), mask=[(258, 596, 338, 632)],
        ref='2018 OL Q7(c)', letters=('A', 'B', 'C', 'D')),
    # ---- scheme: the drawings the answers are given with -------------------
    'engineering-2018-OL-scheme-q2bi-sol': dict(
        doc='scheme', page=8, parts=[(8, (135, 186, 430, 395)), (8, (100, 428, 472, 586)),
                                     (8, (100, 628, 450, 812))],
        mask=[(130, 182, 180, 206)], solution=True, ref='2018 OL Q2(b)(i)'),
    'engineering-2018-OL-scheme-q5aii-sol': dict(
        doc='scheme', page=14, parts=[(14, (80, 336, 280, 456)), (14, (80, 498, 275, 586)),
                                      (14, (62, 645, 282, 748))],
        solution=True, ref='2018 OL Q5(a)(ii)'),
    'engineering-2018-OL-scheme-q6aii-sol': dict(
        doc='scheme', page=16, rect=(130, 162, 412, 268), solution=True,
        ref='2018 OL Q6(a)(ii)'),
    'engineering-2018-OL-scheme-q7cori-sol': dict(
        doc='scheme', page=18, rect=(85, 562, 428, 660), solution=True,
        ref='2018 OL Q7(c)(i)'),
}

CARDS = [
    # ---- Question 1, Section A ("Any six @ 5 marks each") ------------------
    dict(key=(1, 'a', None),
         why='The component is photographed beside (a); scheme p5 numbers two '
             'precautions; "3 + 2 Marks".',
         topic='eng-3-1',
         lifted=[S(5, 88, 406, 350, 422), S(5, 88, 421, 215, 437)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         question_figure='engineering-2018-OL-paper-q1a-art',
         notes="The scheme prints '3 + 2 Marks'."),
    dict(key=(1, 'b', None),
         why='Scheme p5 answers in one line, "5 Marks".',
         topic='eng-3-14',
         lifted=[S(5, 67, 450, 199, 466)], marks=[5], total=5,
         notes="The scheme prints '5 Marks'."),
    dict(key=(1, 'c', None),
         why='The ratchet and pawl is drawn beside (c); scheme p5 numbers two '
             'applications; "3 + 2 Marks".',
         topic='eng-2-15',
         lifted=[S(5, 82, 489, 198, 505), S(5, 83, 503, 178, 518)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         question_figure='engineering-2018-OL-paper-q1c-art',
         notes="The scheme prints '3 + 2 Marks'."),
    dict(key=(1, 'd', None),
         why='Scheme p5 numbers two reasons; "3 + 2 Marks".',
         topic='eng-3-14',
         lifted=[S(5, 82, 538, 329, 554), S(5, 83, 553, 352, 569)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         notes="The scheme prints '3 + 2 Marks'."),
    dict(key=(1, 'e', None),
         why='Scheme p5 answers in one sentence, "5 Marks".',
         topic='eng-2-10',
         lifted=[S(5, 67, 589, 399, 620)], marks=[5], total=5,
         notes="The scheme prints '5 Marks'."),
    dict(key=(1, 'f', None),
         why='The LED is photographed beside (f); scheme p5 answers in one line, "5 '
             'Marks".',
         topic='eng-2-16',
         lifted=[S(5, 65, 641, 414, 657)], marks=[5], total=5,
         question_figure='engineering-2018-OL-paper-q1f-crop',
         notes="The scheme prints '5 Marks'."),
    dict(key=(1, 'g', None),
         why='Scheme p5 names the alloy, "5 Marks".',
         topic='eng-1-5',
         lifted=[S(5, 67, 685, 102, 701)], marks=[5], total=5,
         notes="The scheme prints '5 Marks'."),
    dict(key=(1, 'h', None),
         why='Scheme p5 numbers two uses; "3 + 2 Marks".',
         topic='eng-2-16',
         lifted=[S(5, 83, 729, 248, 745), S(5, 83, 743, 261, 759)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         notes="The scheme prints '3 + 2 Marks'."),
    # ---- Question 1, Section B ("Any three parts @ 12 + 12 + 11 marks") ----
    dict(key=(1, 'i', None),
         why='The three items are photographed and captioned under (i); scheme p6 '
             'describes each under its name, "Any one", "Award 12 (11) Marks". The '
             'question is lifted with each caption on its own line, as the paper '
             'sets them under their pictures.',
         topic='eng-2-11', stem=False,
         question_lift=P(2, 60, 454, 390, 472, items=[(60, 565, 215, 583), (260, 565, 335, 583),
                                                 (440, 565, 520, 583)]),
         lifted=[[join(S(6, 88, 116, 233, 132), S(6, 88, 130, 458, 234)),
                  join(S(6, 88, 239, 151, 255), S(6, 88, 254, 446, 387)),
                  join(S(6, 88, 392, 158, 408), S(6, 88, 406, 447, 481))]],
         row_kind='anyN', group=(1, 12), marks=[12], tariff='fixed', total=12,
         question_figure='engineering-2018-OL-paper-q1i-crop',
         notes="The scheme prints 'Describe Award 12 (11) Marks'. " + _SB),
    dict(key=(1, 'j', None),
         why='Scheme pp6-7 explain each term under its name, "Any two", "Award 6 + 6(5)".',
         topic='eng-3-14', stem=False,
         lifted=[[join(S(6, 88, 521, 117, 537), S(6, 88, 536, 443, 625)),
                  join(S(6, 88, 630, 172, 646), S(6, 88, 644, 470, 734)),
                  join(S(6, 88, 737, 171, 753), S(6, 88, 752, 499, 782),
                       S(7, 88, 57, 470, 88)),
                  join(S(7, 88, 93, 159, 109), S(7, 88, 107, 453, 152))]],
         row_kind='anyN', group=(2, 6), marks=[12], tariff='fixed', total=12,
         notes="The scheme prints 'Explain Award 6 + 6(5)'. " + _SB),
    dict(key=(1, 'k', None),
         why='Scheme p7 gives the definition and the material under their headings, '
             '"Definition Award 6", "Example Award 6(5)".',
         topic='eng-2-16', stem=False,
         lifted=[join(S(7, 88, 180, 188, 196), S(7, 88, 195, 396, 226)),
                 join(S(7, 88, 239, 125, 255), S(7, 88, 254, 169, 270))],
         marks=[6, 6], total=12,
         notes="The scheme prints 'Definition Award 6, Example Award 6(5)'. " + _SB),
    dict(key=(1, 'l', None),
         why='Scheme p7 explains each term under its name, "Any two", "Award 6 + 6 (5)".',
         topic='eng-2-16', stem=False,
         lifted=[[join(S(7, 85, 355, 222, 371), S(7, 85, 370, 446, 445)),
                  join(S(7, 85, 459, 169, 475), S(7, 85, 473, 460, 519)),
                  join(S(7, 85, 532, 165, 548), S(7, 88, 547, 450, 577)),
                  join(S(7, 85, 591, 171, 607), S(7, 85, 605, 456, 651))]],
         row_kind='anyN', group=(2, 6), marks=[12], tariff='fixed', total=12,
         notes="The scheme prints 'Explain Award 6 + 6 (5)'. " + _SB),
    dict(key=(1, 'm', None),
         why='The drill is photographed beside (m); scheme p7 gives the name and the '
             'function under their headings, "Name Award 6", "Function Award 6(5)".',
         topic='eng-2-11', stem=False,
         lifted=[join(S(7, 83, 678, 120, 694), S(7, 83, 692, 167, 708)),
                 join(S(7, 83, 722, 133, 738), S(7, 83, 736, 428, 782))],
         marks=[6, 6], total=12,
         question_figure='engineering-2018-OL-paper-q1m-art',
         notes="The scheme prints 'Name Award 6, Function Award 6(5)'. " + _SB),
    # ---- Question 2 --------------------------------------------------------
    dict(key=(2, 'a', None),
         why='Three furnaces drawn and captioned (i)-(iii) with no words; scheme p8 '
             'names each and its function on its own line, "Name and function Award 3 @ '
             '4 Marks".',
         topic='eng-1-4',
         lifted=[S(8, 69, 87, 430, 103), S(8, 69, 101, 415, 117), S(8, 69, 116, 414, 132)],
         marks=[4, 4, 4], total=12,
         question_figure='engineering-2018-OL-paper-q2a-crop',
         notes="The scheme prints 'Name and function Award 3 @ 4 Marks'."),
    dict(key=(2, 'b', 'i'),
         why='"Select one of the furnaces": scheme p8 gives each furnace\'s labelled '
             'diagram under its name, shown with the answer; each option is the '
             'furnace\'s name with the labels on its diagram. "Diagram and parts Award 5 '
             'Marks".',
         topic='eng-1-4', stem=False,
         question_figure='engineering-2018-OL-paper-q2a-crop',
         question_lift=P(3, *_B2, more=[(104, 325, 381, 343)]),
         checked='paper page 3: "(i) Draw a diagram of the furnace and label the main '
                 'parts;" under (b)\'s lead-in; ' + _CK,
         lifted=[[join(S(8, 140, 221, 209, 237), S(8, 240, 189, 275, 205),
                       S(8, 315, 198, 370, 214), S(8, 353, 288, 388, 304),
                       S(8, 202, 320, 259, 336), S(8, 375, 340, 399, 356)),
                  join(S(8, 102, 440, 200, 456), S(8, 227, 431, 281, 447),
                       S(8, 345, 437, 428, 453), S(8, 402, 480, 470, 496),
                       S(8, 146, 498, 219, 515), S(8, 400, 552, 436, 568),
                       S(8, 171, 569, 236, 585)),
                  join(S(8, 104, 631, 213, 647), S(8, 170, 656, 238, 684),
                       S(8, 391, 632, 445, 649), S(8, 368, 688, 448, 704),
                       S(8, 170, 701, 231, 717), S(8, 387, 732, 411, 748),
                       S(8, 180, 751, 229, 767), S(8, 378, 769, 436, 785))]],
         row_kind='anyN', group=(1, 5), marks=[5], tariff='fixed', total=5,
         figure='engineering-2018-OL-scheme-q2bi-sol',
         notes="The scheme prints 'Diagram and parts Award 5 Marks', for the furnace "
               "selected."),
    dict(key=(2, 'b', 'ii'),
         why='Scheme p9 gives each furnace\'s charge on its own line, any one, '
             '"Materials Award3 Marks".',
         topic='eng-1-4', stem=False,
         question_figure='engineering-2018-OL-paper-q2a-crop',
         question_lift=P(3, *_B2, more=[(104, 344, 274, 363)]),
         checked='paper page 3: "(ii) Name the materials in the charge;" under (b)\'s '
                 'lead-in; ' + _CK,
         lifted=[[S(9, 91, 101, 331, 117), S(9, 91, 116, 397, 132),
                  S(9, 91, 130, 397, 146)]],
         row_kind='anyN', group=(1, 3), marks=[3], tariff='fixed', total=3,
         notes="The scheme prints 'Materials Award3 Marks', for the furnace selected."),
    dict(key=(2, 'b', 'iii'),
         why='Scheme p9 describes each furnace\'s metal removal on its own line, any '
             'one, "Describe Award 2 Marks".',
         topic='eng-1-4', stem=False,
         question_figure='engineering-2018-OL-paper-q2a-crop',
         question_lift=P(3, *_B2, more=[(104, 363, 369, 382)]),
         lifted=[[S(9, 91, 218, 493, 234), S(9, 91, 233, 455, 249),
                  S(9, 91, 248, 481, 293)]],
         row_kind='anyN', group=(1, 2), marks=[2], tariff='fixed', total=2,
         notes="The scheme prints 'Describe Award 2 Marks', for the furnace selected."),
    dict(key=(2, 'c', 'i'),
         why='Scheme p9 answers in a two-column table, Material and Reason, one row a '
             'component; each material is lifted with its component\'s name. "Material '
             'Award 3 @ 3 Marks".',
         topic='eng-3-14',
         lifted=[join(S(9, 81, 423, 176, 439), S(9, 180, 423, 268, 439)),
                 join(S(9, 81, 467, 185, 483), S(9, 189, 467, 219, 483)),
                 join(S(9, 81, 511, 161, 527), S(9, 165, 511, 212, 527))],
         marks=[3, 3, 3], total=9, question_figure='engineering-2018-OL-paper-q2ci-art',
         notes="The scheme prints '(i) Material Award 3 @ 3 Marks'."),
    dict(key=(2, 'c', 'ii'),
         why='The Reason column of the same table; each reason is lifted with its '
             'component\'s name. "Reason Award 3 @ 2 Marks".',
         topic='eng-3-14',
         lifted=[join(S(9, 81, 423, 176, 439), S(9, 278, 423, 424, 454)),
                 join(S(9, 81, 467, 185, 483), S(9, 279, 467, 438, 498)),
                 join(S(9, 81, 511, 161, 527), S(9, 278, 511, 459, 542))],
         marks=[2, 2, 2], total=6, question_figure='engineering-2018-OL-paper-q2ci-art',
         notes="The scheme prints '(ii) Reason Award 3 @ 2 Marks'."),
    dict(key=(2, 'd', None),
         why='A lead-in over three photographed metals captioned as romans; scheme p9 '
             'classes each on its own line, "Award 2 @ 4 Marks".',
         topic='eng-1-2',
         lifted=[[S(9, 80, 628, 226, 644), S(9, 80, 643, 223, 659),
                  S(9, 80, 658, 201, 674)]],
         row_kind='anyN', group=(2, 4), marks=[8], tariff='fixed', total=8,
         question_figure='engineering-2018-OL-paper-q2d-crop',
         notes="The scheme prints 'Ferrous / Non-ferrous Award 2 @ 4 Marks'."),
    # ---- Question 3 --------------------------------------------------------
    dict(key=(3, 'a', 'i'),
         why='Scheme p10 names the process and its property on their own lines, "Name '
             'Award 5 Marks", "Property Award 5 Marks".',
         topic='eng-2-6', stem=False,
         question_lift=P(4, 104, 83, 568, 118),
         lifted=[S(10, 103, 106, 239, 122), S(10, 103, 135, 393, 151)],
         marks=[5, 5], total=10,
         notes="The scheme prints 'Name Award 5 Marks, Property Award 5 Marks'."),
    dict(key=(3, 'a', 'ii'),
         why='Scheme p10 names the process and its property on their own lines, "Name '
             'Award 5 Marks", "Property Award 5 Marks".',
         topic='eng-2-6', stem=False,
         question_lift=P(4, 104, 140, 572, 175),
         lifted=[S(10, 104, 223, 240, 239), S(10, 104, 252, 387, 268)],
         marks=[5, 5], total=10,
         notes="The scheme prints 'Name Award 5 Marks, Property Award 5 Marks'."),
    dict(key=(3, 'b', None),
         why='(b) asks to describe each of two processes; scheme p10 prices them '
             'together, "Award 1 @ 6 Marks, Award 1 @ 5 Marks", so the two are one card '
             'at the letter, 6 for one and 5 for the other.',
         topic='eng-2-6',
         lifted=[join(S(10, 107, 399, 272, 415), S(10, 107, 414, 448, 488)),
                 join(S(10, 107, 516, 321, 532), S(10, 107, 531, 448, 576))],
         tariff='orderedSplit', notation='6 + 5', ladder=11, total=11,
         notes="The scheme prints '(i) & (ii) Describe Award 1 @ 6 Marks, Award 1 @ 5 "
               "Marks'."),
    dict(key=(3, 'c', None),
         why='Scheme p10 bullets two precautions; "Award 2 @ 3 Marks".',
         topic='eng-3-1',
         lifted=[S(10, 124, 648, 422, 679), S(10, 124, 693, 350, 709)],
         marks=[3, 3], total=6,
         notes="The scheme prints 'Safety precautions Award 2 @ 3 Marks'."),
    dict(key=(3, 'd', None),
         why='Paper p4 sets two alternative (d)s either side of an OR, both at the '
             'letter. Scheme p11 explains each metal property under its name, "Award 2 '
             '@ 4 Marks", and bullets two robotics applications, "Award 2 @ 4 Marks": '
             'priced alike, one card with a route per branch.',
         topic='eng-3-8', stem=False,
         question_lift=P(4, 84, 563, 332, 579, more=[(84, 595, 500, 611), (274, 649, 296, 667),
                                                     (84, 717, 309, 733)]),
         lifted=[[join(S(11, 103, 101, 173, 117), S(11, 103, 116, 414, 146)),
                  join(S(11, 106, 160, 167, 176), S(11, 105, 174, 419, 205)),
                  join(S(11, 106, 218, 166, 234), S(11, 107, 233, 456, 249))],
                 S(11, 124, 338, 336, 354), S(11, 124, 353, 360, 369)],
         row_kind='anyN', group=[(2, 4), None, None], marks=[8, 4, 4],
         routes=['a', 'b', 'b'], tariff='fixed', total=8, notes=_OR3),
    # ---- Question 4 --------------------------------------------------------
    dict(key=(4, 'a', 'i'),
         why='Scheme p12 names both gases on one line, each lifted by its own word '
             'rectangle; "Name Award 2 @ 2 Marks".',
         topic='eng-2-10',
         lifted=[S(12, 160, 118, 200, 134), S(12, 210, 118, 263, 134)],
         marks=[2, 2], total=4,
         notes="The scheme prints 'Name Award 2 @ 2 Marks'."),
    dict(key=(4, 'a', 'ii'),
         why='Scheme p12 gives each cylinder\'s colour on its own line; "Colour Award 2 @ '
             '2 Marks".',
         topic='eng-2-10',
         lifted=[S(12, 160, 177, 285, 193), S(12, 160, 191, 329, 207)],
         marks=[2, 2], total=4,
         notes="The scheme prints 'Colour Award 2 @ 2 Marks'."),
    dict(key=(4, 'a', 'iii'),
         why='Scheme p12 names the three flames on their own lines; "Award 1 @ 4 Marks, '
             'Award 2 @ 3 Marks", 4 for the first and 3 for each of the others.',
         topic='eng-2-10',
         lifted=[S(12, 160, 249, 239, 265), S(12, 160, 264, 231, 280),
                 S(12, 160, 279, 250, 295)],
         tariff='orderedSplit', notation='4 + 3 + 3', ladder=10, total=10,
         notes="The scheme prints 'Types of flame Award 1 @ 4 Marks, Award 2 @ 3 Marks'."),
    dict(key=(4, 'b', None),
         why='A lead-in over four photographed items captioned as romans; scheme p12 '
             'gives each one\'s function under its name, "Award any 3 @ 3 Marks".',
         topic='eng-2-10',
         lifted=[[join(S(12, 109, 426, 184, 442), S(12, 109, 440, 446, 486)),
                  join(S(12, 109, 514, 165, 530), S(12, 109, 528, 474, 559)),
                  join(S(12, 109, 572, 196, 588), S(12, 109, 587, 410, 618)),
                  join(S(12, 109, 631, 186, 647), S(12, 109, 646, 454, 676))]],
         row_kind='anyN', group=(3, 3), marks=[9], tariff='fixed', total=9,
         question_figure='engineering-2018-OL-paper-q4b-crop',
         notes="The scheme prints 'Function Award any 3 @ 3 Marks'."),
    dict(key=(4, 'c', 'i'),
         why='"Answer any three of the following", four separate asks, carded per roman; '
             'scheme p13 bullets two advantages under "Award 3 @ 4 Marks", one price for '
             'the part.',
         topic='eng-2-10', stem=False,
         question_lift=P(5, *_C4, more=[(104, 447, 413, 463)]),
         lifted=[S(13, 124, 130, 334, 146), S(13, 124, 160, 172, 176)],
         tariff='questionTotal', total=4,
         notes="The scheme prints 'Award 3 @ 4 Marks', 4 for each part answered."),
    dict(key=(4, 'c', 'ii'),
         why='Scheme p13 names the method, "Award 3 @ 4 Marks".',
         topic='eng-2-10', stem=False,
         question_lift=P(5, *_C4, more=[(104, 497, 505, 530)]),
         lifted=[S(13, 110, 234, 162, 250)], marks=[4], total=4,
         notes="The scheme prints 'Award 3 @ 4 Marks', 4 for each part answered."),
    dict(key=(4, 'c', 'iii'),
         why='Scheme p13 answers in one sentence, "Award 3 @ 4 Marks".',
         topic='eng-2-10', stem=False,
         question_lift=P(5, *_C4, more=[(104, 565, 500, 581)]),
         lifted=[S(13, 112, 307, 443, 338)], marks=[4], total=4,
         notes="The scheme prints 'Award 3 @ 4 Marks', 4 for each part answered."),
    dict(key=(4, 'c', 'iv'),
         why='Scheme p13 bullets two hazards under "Award 3 @ 4 Marks", one price for '
             'the part.',
         topic='eng-3-1', stem=False,
         question_lift=P(5, *_C4, more=[(104, 615, 371, 631)]),
         lifted=[S(13, 129, 386, 281, 402), S(13, 129, 416, 341, 432)],
         tariff='questionTotal', total=4,
         notes="The scheme prints 'Award 3 @ 4 Marks', 4 for each part answered."),
    dict(key=(4, 'd', None),
         why='Scheme p13 bullets two precautions; "Award 2 @ 3 Marks".',
         topic='eng-3-1',
         lifted=[S(13, 123, 519, 397, 535), S(13, 123, 549, 363, 565)],
         marks=[3, 3], total=6,
         notes="The scheme prints 'Safety precautions Award 2 @ 3 Marks'."),
    # ---- Question 5 --------------------------------------------------------
    dict(key=(5, 'a', 'i'),
         why='The three components are photographed and captioned above (i); scheme p14 '
             'names a process for each on its own line, "Name Award 3 @ 3 Marks".',
         topic='eng-1-9', stem=False,
         question_lift=P(6, *_A5, more=[(104, 269, 548, 301)]),
         lifted=[S(14, 107, 133, 290, 149), S(14, 107, 162, 280, 178),
                 S(14, 107, 191, 286, 207)],
         marks=[3, 3, 3], total=9, question_figure='engineering-2018-OL-paper-q5ai-art',
         notes="The scheme prints 'Name Award 3 @ 3 Marks'."),
    dict(key=(5, 'a', 'ii'),
         why='Scheme p14 describes each process under its name beside a drawing, shown '
             'with the answer; any one, "Describe Award 9 Marks".',
         topic='eng-1-9', stem=False,
         question_lift=P(6, *_A5, more=[(104, 313, 558, 345)]),
         lifted=[[join(S(14, 87, 338, 167, 354), S(14, 292, 341, 503, 474)),
                  join(S(14, 91, 499, 192, 515), S(14, 291, 495, 493, 599)),
                  join(S(14, 91, 646, 181, 662), S(14, 291, 627, 518, 789))]],
         row_kind='anyN', group=(1, 9), marks=[9], tariff='fixed', total=9,
         question_figure='engineering-2018-OL-paper-q5ai-art',
         figure='engineering-2018-OL-scheme-q5aii-sol',
         notes="The scheme prints 'Describe Award 9 Marks'."),
    dict(key=(5, 'b', 'i'),
         why='"Answer each of the following": scheme p15 names the term, "Award 3 @ 5 '
             'Marks".',
         topic='eng-1-9', stem=False,
         question_lift=P(6, *_B5, more=[(104, 412, 470, 428)]),
         checked='paper page 6: "(i) Name the term used for a plastic which remains hard '
                 'after being heated;" under (b)\'s lead-in; ' + _CK,
         lifted=[S(15, 116, 116, 225, 132)], marks=[5], total=5,
         notes="The scheme prints 'Award 3 @ 5 Marks'."),
    dict(key=(5, 'b', 'ii'),
         why='Scheme p15 names the term, "Award 3 @ 5 Marks".',
         topic='eng-1-9', stem=False,
         question_lift=P(6, *_B5, more=[(104, 442, 409, 458)]),
         checked='paper page 6: "(ii) Name the term used for a plastic which softens when '
                 'heated;" under (b)\'s lead-in; ' + _CK,
         lifted=[S(15, 116, 145, 189, 161)], marks=[5], total=5,
         notes="The scheme prints 'Award 3 @ 5 Marks'."),
    dict(key=(5, 'b', 'iii'),
         why='Scheme p15 names the method, "Award 3 @ 5 Marks".',
         topic='eng-1-9', stem=False,
         question_lift=P(6, *_B5, more=[(104, 471, 428, 487)]),
         lifted=[S(15, 116, 174, 169, 190)], marks=[5], total=5,
         notes="The scheme prints 'Award 3 @ 5 Marks'."),
    dict(key=(5, 'c', None),
         why='A lead-in over three photographed products captioned as romans; scheme '
             'p15 names a plastic for each on its own line, "Name Award 2 @ 3 Marks".',
         topic='eng-1-9',
         lifted=[[S(15, 116, 262, 299, 278), S(15, 116, 292, 348, 308),
                  S(15, 116, 321, 293, 337)]],
         row_kind='anyN', group=(2, 3), marks=[6], tariff='fixed', total=6,
         question_figure='engineering-2018-OL-paper-q5ci-art',
         notes="The scheme prints 'Name Award 2 @ 3 Marks'."),
    dict(key=(5, 'd', None),
         why='Scheme p15 bullets two precautions; "Award 2 @ 3 Marks".',
         topic='eng-3-1',
         lifted=[S(15, 97, 409, 364, 425), S(15, 97, 439, 303, 455)],
         marks=[3, 3], total=6,
         notes="The scheme prints 'Safety precautions Award 2 @ 3 Marks'."),
    # ---- Question 6 --------------------------------------------------------
    dict(key=(6, 'a', 'i'),
         why='The steering wheel is drawn beside (a); scheme p16 lists five operations '
             'on one line, each lifted by its own word rectangle; "Award 1 @ 4 Marks, '
             'Award 2 @ 3 Marks" for three.',
         topic='eng-2-11',
         lifted=[S(16, 104, 133, 176, 149), S(16, 176, 133, 215, 149),
                 S(16, 215, 133, 295, 149), S(16, 295, 133, 347, 149),
                 S(16, 347, 133, 398, 149)],
         tariff='orderedSplit', notation='4 + 3 + 3', ladder=10, total=10,
         question_figure='engineering-2018-OL-paper-q6a-crop',
         notes="The scheme prints '(i) Name Award 1 @ 4 Marks, Award 2 @ 3 Marks'."),
    dict(key=(6, 'a', 'ii'),
         why='Scheme p16 answers (ii) with drawings of three of the operations under '
             'their names and prints no description; the drawings are shown with the '
             'answer. "Award 1 @ 4 Marks, Award 2 @ 3 Marks".',
         topic='eng-2-11',
         special={'kind': 'ask'}, total=10,
         question_figure='engineering-2018-OL-paper-q6a-crop',
         figure='engineering-2018-OL-scheme-q6aii-sol',
         notes="The scheme prints '(ii) Describe Award 1 @ 4 Marks, Award 2 @ 3 Marks'."),
    dict(key=(6, 'b', None),
         why='"A suitable application for each" of two photographed work-holding '
             'methods captioned as romans; scheme p16 describes each under its name, '
             '"Award 2 @ 5 Marks".',
         topic='eng-2-11',
         lifted=[join(S(16, 107, 338, 240, 354), S(16, 107, 353, 461, 398)),
                 join(S(16, 110, 426, 185, 442), S(16, 110, 440, 464, 471))],
         marks=[5, 5], total=10, question_figure='engineering-2018-OL-paper-q6bi-art',
         notes="The scheme prints '(b) (i) & (ii) Describe Award 2 @ 5 Marks'."),
    dict(key=(6, 'c', 'i'),
         why='The toolpost is photographed beside (c); scheme p16 names it, "Award 5 '
             'Marks".',
         topic='eng-2-11', stem=False,
         question_lift=P(7, *_C6, more=[(104, 546, 245, 562)]),
         lifted=[S(16, 106, 558, 235, 574)], marks=[5], total=5,
         question_figure='engineering-2018-OL-paper-q6ci-art',
         notes="The scheme prints '(i) Name Award 5 Marks'. " + _OR6),
    dict(key=(6, 'c', 'ii'),
         why='Scheme p16 describes the function in one sentence, "Award 5 Marks".',
         topic='eng-2-11', stem=False,
         question_lift=P(7, *_C6, more=[(104, 568, 333, 584)]),
         lifted=[join(S(16, 106, 587, 157, 603), S(16, 106, 602, 383, 632))],
         marks=[5], total=5,
         question_figure='engineering-2018-OL-paper-q6ci-art',
         notes="The scheme prints '(ii) Describe Award 5 Marks'. " + _OR6),
    dict(key=(6, 'c', 'iii'),
         why='Scheme p16 bullets two precautions under "Award 5 Marks", one price for the '
             'part.',
         topic='eng-3-1', stem=False,
         question_lift=P(7, *_C6, more=[(104, 590, 324, 620)]),
         lifted=[S(16, 120, 660, 406, 676), S(16, 120, 674, 378, 706)],
         tariff='questionTotal', total=5,
         question_figure='engineering-2018-OL-paper-q6ci-art',
         notes="The scheme prints '(iii) Safety Precautions Award 5 Marks'. " + _OR6),
    dict(key=(6, 'c', None),
         why='The OR branch: "Describe any three" of four CNC terms set as romans, carded '
             'at the letter; scheme p17 describes each under its name, "Award 3 @ 5 '
             'Marks".',
         topic='eng-2-11', stem=False,
         question_lift=P(7, 84, 695, 475, 711, more=[(84, 725, 515, 741)]),
         lifted=[[join(S(17, 109, 101, 176, 117), S(17, 110, 116, 444, 163)),
                  join(S(17, 109, 177, 186, 193), S(17, 110, 191, 443, 266)),
                  join(S(17, 113, 294, 199, 310), S(17, 112, 309, 437, 383)),
                  join(S(17, 112, 397, 140, 413), S(17, 112, 411, 425, 456))]],
         row_kind='anyN', group=(3, 5), marks=[15], tariff='fixed', total=15,
         notes="The scheme prints 'Describe Award 3 @ 5 Marks'. " + _OR6),
    # ---- Question 7 --------------------------------------------------------
    dict(key=(7, 'a', 'i'),
         why='Scheme p18 bullets two methods; "Award 2 @ 3 Marks".',
         topic='eng-3-12',
         lifted=[S(18, 142, 117, 255, 133), S(18, 142, 133, 207, 149)],
         marks=[3, 3], total=6,
         notes="The scheme prints '(i) Methods Award 2 @ 3 Marks'."),
    dict(key=(7, 'a', 'ii'),
         why='Scheme p18 bullets two advantages; "Award 2 @ 2 Marks".',
         topic='eng-3-12',
         lifted=[S(18, 142, 178, 206, 194), S(18, 142, 193, 393, 209)],
         marks=[2, 2], total=4,
         notes="The scheme prints '(ii) Advantages Award 2 @ 2 Marks'."),
    dict(key=(7, 'b', None),
         why='"State the:" over four romans read off the dimensions shown; scheme p18 '
             'answers each on its own line, "Calculations & fit Award 4 @ 5 Marks".',
         topic='eng-3-12', stem=False,
         question_lift=P(8, 84, 173, 388, 189, more=[(84, 198, 321, 214), (140, 218, 315, 236),
                                                     (140, 240, 318, 257),
                                                     (140, 262, 350, 314)]),
         lifted=[S(18, 88, 238, 356, 254), S(18, 88, 253, 356, 269),
                 S(18, 87, 267, 359, 283), S(18, 87, 282, 359, 298)],
         marks=[5, 5, 5, 5], total=20, question_figure='engineering-2018-OL-paper-q7b-crop',
         notes="The scheme prints 'Calculations & fit Award 4 @ 5 Marks'."),
    dict(key=(7, 'c', None),
         why='The instruments branch of (c): four photographs captioned (i)-(iv). Scheme '
             'p18 prices name and application apart, "Name & application (3 + 2)", '
             '"Award 3 @ 5 Marks", so a name is claimed without its application; each '
             'application is shown with the instrument it is for.',
         topic='eng-3-12', stem=False,
         question_lift=P(8, 84, 369, 556, 385),
         lifted=[[S(18, 87, 370, 176, 386), S(18, 87, 399, 214, 415),
                  S(18, 87, 428, 162, 444), S(18, 87, 458, 215, 474)],
                 [S(18, 87, 370, 433, 386), S(18, 87, 399, 416, 415),
                  S(18, 87, 428, 368, 444), S(18, 87, 458, 398, 474)]],
         row_kind='anyN', group=[(3, 3), (3, 2)], marks=[9, 6], tariff='fixed', total=15,
         question_figure='engineering-2018-OL-paper-q7c-crop',
         notes="The scheme prints 'Name & application (3 + 2) Award 3 @ 5 Marks'. " + _OR7),
    dict(key=(7, 'c', 'i'),
         why='The OR branch\'s (i): scheme p18 answers the drawing with the drawn '
             'symbols, lettered, and prints no words; the symbols are shown with the '
             'answer. "Draw & function (3 + 2)", "Award 3 @ 5 Marks", 3 for each '
             'symbol.',
         topic='eng-2-16', stem=False,
         question_lift=P(8, 104, 596, 324, 631),
         special={'kind': 'ask'}, total=9,
         question_figure='engineering-2018-OL-paper-q7cor-crop',
         figure='engineering-2018-OL-scheme-q7cori-sol',
         notes="The scheme prints '(c) (i) & (ii) Draw & function (3 + 2) Award 3 @ 5 "
               "Marks'. " + _OR7),
    dict(key=(7, 'c', 'ii'),
         why='The OR branch\'s (ii): scheme p18 names each component and its function on '
             'its own line, under its letter; "Draw & function (3 + 2)", 2 for each '
             'function.',
         topic='eng-2-16', stem=False,
         question_lift=P(8, 104, 649, 250, 703),
         lifted=[[S(18, 102, 709, 317, 725), S(18, 102, 724, 427, 740),
                  S(18, 102, 738, 424, 754), S(18, 102, 751, 359, 769)]],
         row_kind='anyN', group=(3, 2), marks=[6], tariff='fixed', total=6,
         question_figure='engineering-2018-OL-paper-q7cor-crop',
         notes="The scheme prints '(c) (i) & (ii) Draw & function (3 + 2) Award 3 @ 5 "
               "Marks'. " + _OR7),
]

TOPICS = {}

_MAT = 'Materials: Properties and Uses'

ATLAS = {
    'eng-2018-ol-q2-c-i': dict(
        topics=[_MAT],
        note='Choosing a material for each component shown; the card\'s syllabus heading '
             'is Technology, as every Ordinary Q2(c) card\'s is.'),
    'eng-2018-ol-q2-c-ii': dict(
        topics=[_MAT],
        note='The reason for each material chosen in (c)(i); the card\'s syllabus heading '
             'is Technology, as every Ordinary Q2(c) card\'s is.'),
    'eng-2018-ol-q6-c-iii': dict(
        topics=['CNC & Centre Lathe'],
        note='Safety precautions with the lathe\'s toolpost; the card\'s syllabus heading '
             'is Health and safety.'),
}
