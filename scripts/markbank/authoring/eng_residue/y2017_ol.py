"""2017 Ordinary Level: every part, from the page.

Paper and scheme as the PDFs number their pages. As in 2018 and 2019, the
automatic author prices nothing in this sitting: the scheme sets each answer in
a left column and its award in a box to the right ("Name of metals Award 3 @ 4
Marks"), which its reader does not join to the answer, so every card here is
built from the page by rectangle. The marks grid is on scheme p4: Question 1 is
Section A, "Any six @ 5 marks each", two-part answers 3 + 2, and Section B,
"Any three parts @ 12 + 12 + 11 Marks"; Questions 2-7 are 45 marks each. A
Section B card carries the PRINTED primary price, the 12 the scheme awards a
part answered first or second ("Award 12 (11) Marks"), and says the third part
answered earns 11.
"""
from eng_lift import join, lift

Y, L = 2017, 'ol'
OWNED = ('never shipped: the automatic author builds this card only from the lifts this '
         'entry records, so the entry owns it')


def S(page, *rect):
    return lift(Y, L, 'scheme', page, rect)


def P(page, *rect, more=(), items=()):
    return lift(Y, L, 'paper', page, rect, more=more, items=items)


_A3 = (84, 82, 450, 98)               # paper p4: Q3(a)'s lead-in
_A5 = (84, 80, 376, 96)               # paper p6: Q5(a)'s lead-in
_C6A = (84, 459, 292, 475)            # paper p7: the chuck (c)
_ORW6 = (277, 610, 298, 628)
_C6B = (84, 657, 344, 673)            # the CNC lathe (c)

_SB = ("Section B is 'Any three parts @ 12 + 12 + 11 Marks': the card carries the 12 a part "
       "earns answered first or second; answered third it earns 11.")
_OR3 = ('The paper sets two (d)s either side of an OR, the metal properties and robotics in '
        'manufacturing; the scheme prices both at 8, "Award 2 @ 4 Marks" and "Award 1 @ 4 '
        'Marks" twice, so they are one card, each branch a route.')
_OR6 = ('The paper sets two (c)s either side of an OR, the lathe chuck and the CNC lathe; '
        'the scheme prices their romans alike, (i) "Award 1 @ 5 Marks", (ii) "Award 2 @ '
        '3+2 Marks" and (iii) "Award 1 @ 5 Marks", so each roman is one card, each branch '
        'a route.')
_OR7 = ('The paper sets two (c)s either side of an OR: the instruments (c), carded at the '
        'letter, and the electronic components (c), whose (i) and (ii) are carded apart.')
_CK = 'the semicolon is the list running on'

CROPS = {
    # ---- paper ------------------------------------------------------------
    'engineering-2017-OL-paper-q1d-crop': dict(
        doc='paper', page=2, rect=(474, 167, 573, 231), image=True, ref='2017 OL Q1(d)'),
    # The two safety symbols with their captions; the tail of (h)'s "shown." and
    # a corner of the drawing beside (g) fall inside the box and are whited out.
    'engineering-2017-OL-paper-q1h-crop': dict(
        doc='paper', page=2, rect=(266, 288, 461, 353),
        mask=[(264, 294, 275, 310), (448, 284, 463, 298)], ref='2017 OL Q1(h)'),
    # The three items under (i), each captioned.
    'engineering-2017-OL-paper-q1i-crop': dict(
        doc='paper', page=2, rect=(60, 478, 535, 586), ref='2017 OL Q1(i)'),
    'engineering-2017-OL-paper-q1m-crop': dict(
        doc='paper', page=2, rect=(411, 728, 508, 827), image=True, ref='2017 OL Q1(m)'),
    # The centre punch with its point circled and labelled (the automatic crop
    # cut off the "Point" label).
    'engineering-2017-OL-paper-q3b-crop': dict(
        doc='paper', page=4, rect=(155, 238, 466, 345), ref='2017 OL Q3(b)'),
    # The three flames with their letters.
    'engineering-2017-OL-paper-q4a-crop': dict(
        doc='paper', page=5, rect=(176, 115, 350, 225), ref='2017 OL Q4(a)',
        letters=('A', 'B', 'C')),
    # Both drawings of process A and both of process B, with the letters (the
    # automatic crop cut off the first drawing of A).
    'engineering-2017-OL-paper-q5a-crop': dict(
        doc='paper', page=6, rect=(100, 100, 545, 250), ref='2017 OL Q5(a)',
        letters=('A', 'B')),
    # The four lathe parts with their captions, without (b)'s ask.
    'engineering-2017-OL-paper-q6b-crop': dict(
        doc='paper', page=7, rect=(33, 292, 570, 403), ref='2017 OL Q6(b)'),
    # Each (c) shows its own machine: the chuck, then the CNC lathe.
    'engineering-2017-OL-paper-q6c-crop': dict(
        doc='paper', parts=[(7, (367, 460, 492, 584)), (7, (397, 654, 533, 760))],
        layout='row', ref='2017 OL Q6(c)'),
    # The hole and shaft with both dimensions; the end of (b)'s line runs into
    # the drawing's top edge, and the ends of (iv)'s lines into its left edge,
    # and are whited out.
    'engineering-2017-OL-paper-q7b-crop': dict(
        doc='paper', page=8, rect=(366, 192, 574, 325),
        mask=[(364, 180, 440, 196), (364, 271, 386, 300)], ref='2017 OL Q7(b)'),
    'engineering-2017-OL-paper-q7c-crop': dict(
        doc='paper', page=8, rect=(26, 403, 563, 545), ref='2017 OL Q7(c)'),
    # The OR branch's circuit with its components lettered A-D.
    'engineering-2017-OL-paper-q7cor-crop': dict(
        doc='paper', page=8, rect=(300, 600, 565, 782), ref='2017 OL Q7(c)',
        letters=('A', 'B', 'C', 'D')),
    # ---- scheme: the drawings the answers are given with -------------------
    'engineering-2017-OL-scheme-q2aii-sol': dict(
        doc='scheme', parts=[(8, (58, 414, 186, 576)), (8, (38, 595, 199, 783)),
                             (9, (26, 79, 198, 203))],
        layout='row', solution=True, ref='2017 OL Q2(a)(ii)'),
}

CARDS = [
    # ---- Question 1, Section A ("Any six @ 5 marks each") ------------------
    dict(key=(1, 'a', None),
         why='Scheme p5 numbers two applications; "3 + 2 Marks".',
         topic='eng-3-14',
         lifted=[S(5, 90, 402, 190, 418), S(5, 90, 416, 196, 432)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         notes="The scheme prints '3 + 2 Marks'."),
    dict(key=(1, 'b', None),
         why='Scheme p5 answers in one line, "5 Marks".',
         topic='eng-1-5',
         lifted=[S(5, 64, 446, 370, 462)], marks=[5], total=5,
         notes="The scheme prints '5 Marks'."),
    dict(key=(1, 'c', None),
         why='Scheme p5 names the source, "5 Marks".',
         topic='eng-3-14',
         lifted=[S(5, 64, 483, 100, 499)], marks=[5], total=5,
         notes="The scheme prints '5 Marks'."),
    dict(key=(1, 'd', None),
         why='The tool is photographed beside (d); scheme p5 gives the name and the '
             'application under their headings; "3 + 2 Marks".',
         topic='eng-2-11',
         lifted=[S(5, 68, 519, 230, 535), S(5, 66, 533, 392, 549)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         question_figure='engineering-2017-OL-paper-q1d-crop',
         notes="The scheme prints '3 + 2 Marks'."),
    dict(key=(1, 'e', None),
         why='Scheme p5 answers in one sentence, "5 Marks".',
         topic='eng-3-12',
         lifted=[S(5, 64, 577, 440, 593)], marks=[5], total=5,
         notes="The scheme prints '5 Marks'."),
    dict(key=(1, 'f', None),
         why='Scheme p5 numbers two devices on one line, each lifted by its own word '
             'rectangle; "3 + 2 Marks".',
         topic='eng-2-16',
         lifted=[S(5, 78, 620, 120, 636), S(5, 214, 620, 270, 636)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         notes="The scheme prints '3 + 2 Marks'."),
    dict(key=(1, 'g', None),
         why='Scheme p5 answers in one sentence over two lines, its award boxed beside '
             'it, "5 Marks".',
         topic='eng-1-9',
         lifted=[join(S(5, 64, 664, 478, 680), S(5, 64, 680, 348, 696))],
         marks=[5], total=5,
         notes="The scheme prints '5 Marks'."),
    dict(key=(1, 'h', None),
         why='Two safety symbols drawn and captioned (i) and (ii); scheme p5 names each '
             'after its roman on one line, each lifted by its own word rectangle; "3 + 2 '
             'Marks". One card for the two captions.',
         topic='eng-3-1',
         question_lift=P(2, 62, 294, 274, 310),
         lifted=[S(5, 66, 721, 166, 737), S(5, 232, 721, 312, 737)],
         tariff='orderedSplit', notation='3 + 2', ladder=5, total=5,
         question_figure='engineering-2017-OL-paper-q1h-crop',
         notes="The scheme prints '3 + 2 Marks'."),
    # ---- Question 1, Section B ("Any three parts @ 12 + 12 + 11 Marks") ----
    dict(key=(1, 'i', None),
         why='The three items are photographed and captioned under (i); scheme p6 '
             'describes each under its name, "Any one", "Award 12 (11) Marks". The '
             'question is lifted with each caption on its own line, as the paper '
             'sets them under their pictures.',
         topic='eng-2-15', stem=False,
         question_lift=P(2, 60, 457, 390, 475, items=[(60, 568, 200, 586), (230, 568, 395, 586),
                                                 (450, 568, 520, 586)]),
         lifted=[[join(S(6, 88, 101, 216, 117), S(6, 88, 116, 436, 234)),
                  join(S(6, 88, 248, 238, 264), S(6, 88, 262, 477, 322)),
                  join(S(6, 88, 336, 141, 352), S(6, 88, 350, 476, 454))]],
         row_kind='anyN', group=(1, 12), marks=[12], tariff='fixed', total=12,
         question_figure='engineering-2017-OL-paper-q1i-crop',
         notes="The scheme prints 'Any one: Award 12 (11) Marks'. " + _SB),
    dict(key=(1, 'j', None),
         why='Scheme pp6-7 explain each term under its name, "Any two", "Award 6 + 6(5)".',
         topic='eng-3-14', stem=False,
         lifted=[[join(S(6, 88, 543, 141, 559), S(6, 88, 558, 426, 618)),
                  join(S(6, 88, 631, 142, 647), S(6, 88, 646, 488, 720)),
                  join(S(7, 88, 50, 178, 66), S(7, 88, 65, 466, 125)),
                  join(S(7, 88, 138, 111, 154), S(7, 88, 153, 442, 213))]],
         row_kind='anyN', group=(2, 6), marks=[12], tariff='fixed', total=12,
         notes="The scheme prints 'Any two: Award 6 + 6(5)'. " + _SB),
    dict(key=(1, 'k', None),
         why='Scheme p7 gives the definition under the term and the application on its '
             'own line, "Definition Award 6", "Application Award 6(5)".',
         topic='eng-3-8', stem=False,
         lifted=[join(S(7, 83, 258, 194, 274), S(7, 83, 272, 396, 303)),
                 S(7, 83, 316, 442, 347)],
         marks=[6, 6], total=12,
         notes="The scheme prints 'Definition Award 6, Application Award 6(5)'. " + _SB),
    dict(key=(1, 'l', None),
         why='Scheme p7 explains each term under its name, "Any two", "Award 6 + 6 (5)".',
         topic='eng-3-14', stem=False,
         lifted=[[join(S(7, 83, 433, 169, 449), S(7, 83, 450, 435, 496)),
                  join(S(7, 83, 509, 166, 525), S(7, 83, 524, 430, 554)),
                  join(S(7, 83, 568, 149, 584), S(7, 83, 582, 467, 628)),
                  join(S(7, 83, 641, 217, 657), S(7, 83, 656, 499, 715))]],
         row_kind='anyN', group=(2, 6), marks=[12], tariff='fixed', total=12,
         notes="The scheme prints 'Any two: Award 6 + 6 (5)'. " + _SB),
    dict(key=(1, 'm', None),
         why='The gears are photographed beside (m); scheme p8 gives the name and the '
             'application on their own lines, "Name Award 6", "Application Award 6(5)".',
         topic='eng-2-15', stem=False,
         lifted=[S(8, 80, 99, 266, 115), S(8, 80, 128, 312, 144)],
         marks=[6, 6], total=12,
         question_figure='engineering-2017-OL-paper-q1m-crop',
         notes="The scheme prints 'Name Award 6, Application Award 6(5)'. " + _SB),
    # ---- Question 2 --------------------------------------------------------
    dict(key=(2, 'a', 'i'),
         why='Scheme p8 names each furnace\'s metal on its own line; each metal is lifted '
             'with its furnace\'s name. "Name of metals Award 3 @ 4 Marks".',
         topic='eng-1-4',
         lifted=[join(S(8, 88, 277, 160, 293), S(8, 265, 277, 305, 293)),
                 join(S(8, 88, 292, 170, 308), S(8, 264, 292, 311, 308)),
                 join(S(8, 88, 306, 190, 322), S(8, 265, 306, 293, 322))],
         marks=[4, 4, 4], total=12,
         notes="The scheme prints 'Name of metals Award 3 @ 4 Marks'."),
    dict(key=(2, 'a', 'ii'),
         why='"Describe the operation of one of the furnaces": scheme pp8-9 describe each '
             'under its name beside a drawing of it, shown with the answer; "Any one '
             'description", "Award 1 @ 10 Marks".',
         topic='eng-1-4',
         lifted=[[join(S(8, 202, 417, 272, 433), S(8, 202, 434, 462, 567)),
                  join(S(8, 206, 588, 285, 604), S(8, 207, 608, 443, 726)),
                  join(S(9, 211, 73, 312, 89), S(9, 211, 91, 502, 195))]],
         row_kind='anyN', group=(1, 10), marks=[10], tariff='fixed', total=10,
         figure='engineering-2017-OL-scheme-q2aii-sol',
         notes="The scheme prints 'Any one description: Award 1 @ 10 Marks'."),
    dict(key=(2, 'b', 'i'),
         why='The go-cart is photographed with its three parts labelled; scheme p9 names a '
             'material for each on its own line, each lifted with its part\'s name. '
             '"Name of material Award 3 @ 3 Marks".',
         topic='eng-3-14',
         lifted=[join(S(9, 88, 284, 127, 300), S(9, 193, 284, 221, 300)),
                 join(S(9, 88, 314, 147, 330), S(9, 192, 314, 249, 330)),
                 join(S(9, 88, 343, 150, 359), S(9, 192, 343, 295, 359))],
         marks=[3, 3, 3], total=9,
         question_figure='engineering-2017-OL-paper-q2bi-art',
         notes="The scheme prints 'Name of material Award 3 @ 3 Marks'."),
    dict(key=(2, 'b', 'ii'),
         why='Scheme p9 gives a reason for each material on its own line, each lifted with '
             'its material. "Reason Award 3 @ 2 Marks".',
         topic='eng-3-14',
         lifted=[join(S(9, 88, 401, 120, 417), S(9, 196, 401, 232, 417)),
                 join(S(9, 88, 430, 150, 446), S(9, 195, 430, 291, 446)),
                 join(S(9, 88, 460, 115, 476), S(9, 195, 460, 342, 476))],
         marks=[2, 2, 2], total=6,
         question_figure='engineering-2017-OL-paper-q2bi-art',
         notes="The scheme prints 'Reason Award 3 @ 2 Marks'."),
    dict(key=(2, 'c', None),
         why='A lead-in over three combinations set as romans, "any two"; scheme p9 names '
             'the alloy of each on its own line, each lifted with its combination. "Name '
             'of alloy Award 2 @ 4 Marks".',
         topic='eng-1-5',
         lifted=[[S(9, 88, 592, 226, 608),
                  join(S(9, 88, 621, 158, 637), S(9, 196, 621, 231, 637)),
                  join(S(9, 88, 651, 171, 667), S(9, 196, 651, 234, 667))]],
         row_kind='anyN', group=(2, 4), marks=[8], tariff='fixed', total=8,
         notes="The scheme prints 'Name of alloy Award 2 @ 4 Marks'."),
    # ---- Question 3 --------------------------------------------------------
    dict(key=(3, 'a', 'i'),
         why='"Describe how to carry out each of the following": scheme p10 describes '
             'case hardening under its name, "Description Award 2 @ 6 marks", 6 for '
             'each.',
         topic='eng-2-6', stem=False,
         question_lift=P(4, *_A3, more=[(84, 104, 188, 120)]),
         checked='paper page 4: "(i) Case hardening;" under (a)\'s lead-in; ' + _CK,
         lifted=[S(10, 104, 126, 447, 244)], marks=[6], total=6,
         notes="The scheme prints 'Description Award 2 @ 6 marks', 6 for each process."),
    dict(key=(3, 'a', 'ii'),
         why='Scheme p10 describes annealing under its name, "Description Award 2 @ 6 '
             'marks", 6 for each.',
         topic='eng-2-6', stem=False,
         question_lift=P(4, *_A3, more=[(84, 126, 160, 142)]),
         lifted=[S(10, 107, 287, 482, 332)], marks=[6], total=6,
         notes="The scheme prints 'Description Award 2 @ 6 marks', 6 for each process."),
    dict(key=(3, 'b', 'i'),
         why='The centre punch is photographed with its point circled; scheme p10 '
             'describes hardening and tempering under their headings, "Describe - '
             'Hardening Award 1 @ 6 marks", "Describe -Tempering Award 1 @ 6 marks".',
         topic='eng-2-6',
         lifted=[join(S(10, 104, 419, 163, 435), S(10, 104, 433, 368, 479)),
                 join(S(10, 104, 507, 165, 523), S(10, 104, 521, 448, 552))],
         marks=[6, 6], total=12,
         question_figure='engineering-2017-OL-paper-q3b-crop',
         notes="The scheme prints 'Describe - Hardening Award 1 @ 6 marks' and 'Describe "
               "-Tempering Award 1 @ 6 marks'."),
    dict(key=(3, 'b', 'ii'),
         why='Scheme p10 restates the ask and answers in one sentence, "Explanation Award '
             '1 @ 7 marks".',
         topic='eng-2-6',
         lifted=[S(10, 104, 609, 380, 640)], marks=[7], total=7,
         question_figure='engineering-2017-OL-paper-q3b-crop',
         notes="The scheme prints 'Explanation Award 1 @ 7 marks'."),
    dict(key=(3, 'c', None),
         why='Scheme p10 names two items on one line, each lifted by its own word '
             'rectangle; "Identify Award 2 @ 3 Marks".',
         topic='eng-3-1',
         lifted=[S(10, 271, 682, 315, 698), S(10, 315, 682, 355, 698)],
         marks=[3, 3], total=6,
         notes="The scheme prints 'Identify Award 2 @ 3 Marks'."),
    dict(key=(3, 'd', None),
         why='Paper p4 sets two alternative (d)s either side of an OR. Scheme p11 explains '
             'each metal property under its name, "Description Award 2 @ 4 Marks", and '
             'gives the advantage and the disadvantage of robotics, "Award 1 @ 4 Marks" '
             'each: priced alike, one card with a route per branch.',
         topic='eng-3-8', stem=False,
         question_lift=P(4, 84, 540, 279, 556, more=[(84, 562, 499, 578), (274, 616, 296, 634),
                                                     (84, 670, 331, 704), (84, 720, 344, 753)]),
         lifted=[[join(S(11, 104, 79, 170, 95), S(11, 104, 94, 424, 125)),
                  join(S(11, 104, 138, 192, 154), S(11, 104, 153, 471, 183)),
                  join(S(11, 104, 197, 193, 213), S(11, 104, 211, 479, 271))],
                 S(11, 104, 359, 446, 375), S(11, 104, 389, 432, 420)],
         row_kind='anyN', group=[(2, 4), None, None], marks=[8, 4, 4],
         routes=['a', 'b', 'b'], tariff='fixed', total=8, notes=_OR3),
    # ---- Question 4 --------------------------------------------------------
    dict(key=(4, 'a', 'i'),
         why='The three flames are drawn and lettered; scheme p11 names each after its '
             'letter on its own line. "Name Award 3 @ 3 Marks".',
         topic='eng-2-10',
         lifted=[S(11, 124, 538, 240, 554), S(11, 124, 553, 251, 569),
                 S(11, 124, 568, 232, 584)],
         marks=[3, 3, 3], total=9,
         labels={'A': S(11, 161, 538, 240, 554), 'B': S(11, 161, 553, 251, 569),
                 'C': S(11, 161, 568, 232, 584)},
         question_figure='engineering-2017-OL-paper-q4a-crop',
         notes="The scheme prints 'Name Award 3 @ 3 Marks'."),
    dict(key=(4, 'a', 'ii'),
         why='Scheme p11 states each flame\'s proportions under its letter. "Proportions '
             'Award 3 @ 3 Marks".',
         topic='eng-2-10',
         lifted=[join(S(11, 124, 641, 223, 657), S(11, 124, 656, 392, 672)),
                 join(S(11, 124, 685, 234, 701), S(11, 124, 699, 478, 715)),
                 join(S(11, 124, 729, 215, 745), S(11, 124, 743, 449, 759))],
         marks=[3, 3, 3], total=9,
         question_figure='engineering-2017-OL-paper-q4a-crop',
         notes="The scheme prints 'Proportions Award 3 @ 3 Marks'."),
    dict(key=(4, 'b', None),
         why='A lead-in over four terms set as romans, "any three"; scheme p12 describes '
             'each under its name, "Description, any three", "Award 3 @ 3 Marks".',
         topic='eng-2-10',
         lifted=[[join(S(12, 104, 109, 217, 125), S(12, 104, 123, 501, 169)),
                  join(S(12, 108, 197, 191, 213), S(12, 104, 211, 499, 271)),
                  join(S(12, 108, 299, 134, 315), S(12, 104, 314, 463, 344)),
                  join(S(12, 108, 372, 147, 388), S(12, 104, 387, 467, 418))]],
         row_kind='anyN', group=(3, 3), marks=[9], tariff='fixed', total=9,
         notes="The scheme prints 'Description, any three: Award 3 @ 3 Marks'."),
    dict(key=(4, 'c', 'i'),
         why='"Answer any three of the following", four separate asks, carded per roman; '
             'the welding machine is photographed beside (c). Scheme p12 answers in one '
             'sentence, "Explanation Award 3 @ 4 Marks".',
         topic='eng-2-10',
         lifted=[S(12, 112, 519, 459, 579)], marks=[4], total=4,
         question_figure='engineering-2017-OL-paper-q4ci-art',
         notes="The scheme prints 'Explanation Award 3 @ 4 Marks', 4 for each part "
               "answered."),
    dict(key=(4, 'c', 'ii'),
         why='Scheme p12 answers in one sentence, "Explanation Award 3 @ 4 Marks".',
         topic='eng-2-11',
         lifted=[S(12, 112, 592, 478, 637)], marks=[4], total=4,
         notes="The scheme prints 'Explanation Award 3 @ 4 Marks', 4 for each part "
               "answered."),
    dict(key=(4, 'c', 'iii'),
         why='Scheme p12 answers in one sentence, "Explanation Award 3 @ 4 Marks".',
         topic='eng-2-10',
         lifted=[S(12, 112, 651, 450, 681)], marks=[4], total=4,
         notes="The scheme prints 'Explanation Award 3 @ 4 Marks', 4 for each part "
               "answered."),
    dict(key=(4, 'c', 'iv'),
         why='Scheme p12 names two precautions on one line, each lifted by its own word '
             'rectangle, under "Explanation Award 3 @ 4 Marks", one price for the part.',
         topic='eng-3-1',
         lifted=[S(12, 114, 695, 229, 711), S(12, 229, 695, 388, 711)],
         tariff='questionTotal', total=4,
         notes="The scheme prints 'Explanation Award 3 @ 4 Marks', 4 for each part "
               "answered."),
    dict(key=(4, 'd', None),
         why='Scheme p13 bullets two reasons; "Reasons Award 2 @ 3 Marks".',
         topic='eng-3-1',
         lifted=[S(13, 105, 94, 355, 110), S(13, 105, 109, 331, 125)],
         marks=[3, 3], total=6,
         notes="The scheme prints 'Reasons Award 2 @ 3 Marks'."),
    # ---- Question 5 --------------------------------------------------------
    dict(key=(5, 'a', 'i'),
         why='The two processes are drawn and lettered A and B; scheme p13 names each '
             'after its letter on its own line. "Name of process Award 2 @ 3 Marks". The '
             'question is lifted with (a)\'s stimulus.',
         topic='eng-1-9', stem=False,
         question_lift=P(6, *_A5, more=[(100, 256, 362, 287)]),
         lifted=[S(13, 99, 274, 245, 290), S(13, 99, 288, 237, 304)],
         marks=[3, 3], total=6,
         labels={'A': S(13, 160, 274, 245, 290), 'B': S(13, 160, 288, 237, 304)},
         question_figure='engineering-2017-OL-paper-q5a-crop',
         notes="The scheme prints 'Name of process Award 2 @ 3 Marks'."),
    dict(key=(5, 'a', 'ii'),
         why='Scheme p13 describes each process in a paragraph of its own; "Describe '
             'difference Award 2 @ 3 Marks".',
         topic='eng-1-9',
         lifted=[S(13, 94, 391, 430, 436), S(13, 94, 449, 444, 495)],
         marks=[3, 3], total=6,
         question_figure='engineering-2017-OL-paper-q5a-crop',
         notes="The scheme prints 'Describe difference Award 2 @ 3 Marks'."),
    dict(key=(5, 'a', 'iii'),
         why='Scheme p13 names a component for each process on its own line, each lifted '
             'with its process. "Identify Component Award 2 @ 3 Marks".',
         topic='eng-1-9',
         lifted=[join(S(13, 100, 522, 190, 538), S(13, 232, 522, 300, 538)),
                 join(S(13, 100, 537, 184, 553), S(13, 232, 537, 270, 553))],
         marks=[3, 3], total=6,
         question_figure='engineering-2017-OL-paper-q5a-crop',
         notes="The scheme prints 'Identify Component Award 2 @ 3 Marks'."),
    dict(key=(5, 'b', None),
         why='Paper p6 asks "Describe any three of the following terms" over four terms '
             'set as romans; scheme pp13-14 head the part "Any two descriptions" but award '
             '"3 @ 5 Marks", "Total (15) Marks", and describe each term under its name. '
             'The paper decides the count a student is asked for, so the card asks for '
             'three at the scheme\'s 5 each, and its note quotes the scheme\'s heading. '
             'The reader joins (a)\'s figure letters to (i), so the question is lifted '
             'from the page.',
         topic='eng-1-9',
         question_lift=P(6, 84, 403, 414, 419, more=[(84, 430, 226, 514)]),
         lifted=[[join(S(13, 101, 640, 176, 656), S(13, 99, 654, 413, 685)),
                  join(S(13, 104, 698, 185, 714), S(13, 104, 713, 428, 744)),
                  join(S(14, 104, 50, 219, 66), S(14, 109, 65, 444, 95)),
                  join(S(14, 108, 109, 229, 125), S(14, 109, 123, 432, 213))]],
         row_kind='anyN', group=(3, 5), marks=[15], tariff='fixed', total=15,
         notes="The paper asks for any three. The scheme heads this part 'Any two "
               "descriptions' but prints 'Award 3 @ 5 Marks' and 'Total (15) Marks'."),
    dict(key=(5, 'c', None),
         why='A lead-in over three plastics set as romans, "any two"; scheme p14 gives '
             'applications for each on its own line, each lifted with its plastic. "Any '
             'two applications", "Award 2 @ 3 Marks".',
         topic='eng-1-9',
         lifted=[[join(S(14, 88, 270, 161, 286), S(14, 196, 270, 315, 286)),
                  join(S(14, 88, 284, 154, 300), S(14, 196, 284, 337, 300)),
                  join(S(14, 88, 299, 115, 315), S(14, 196, 299, 440, 315))]],
         row_kind='anyN', group=(2, 3), marks=[6], tariff='fixed', total=6,
         notes="The scheme prints 'Any two applications: Award 2 @ 3 Marks'."),
    dict(key=(5, 'd', None),
         why='The car is photographed with its acrylic cab labelled; scheme p14 describes '
             'the process in one paragraph, "Description Award 1 @ 6 Marks".',
         topic='eng-1-9',
         lifted=[S(14, 85, 387, 451, 447)], marks=[6], total=6,
         question_figure='engineering-2017-OL-paper-q5d-art',
         notes="The scheme prints 'Description Award 1 @ 6 Marks'."),
    # ---- Question 6 --------------------------------------------------------
    dict(key=(6, 'a', 'i'),
         why='Scheme p14 answers under a heading in one sentence; "1 reason for each '
             'part", "Award 3 @ 5 Marks".',
         topic='eng-2-11',
         lifted=[S(14, 104, 594, 436, 625)], marks=[5], total=5,
         notes="The scheme prints '1 reason for each part Award 3 @ 5 Marks'."),
    dict(key=(6, 'a', 'ii'),
         why='Scheme p14 answers under a heading in one sentence; "1 reason for each '
             'part", "Award 3 @ 5 Marks".',
         topic='eng-2-11',
         lifted=[S(14, 107, 653, 467, 684)], marks=[5], total=5,
         notes="The scheme prints '1 reason for each part Award 3 @ 5 Marks'."),
    dict(key=(6, 'a', 'iii'),
         why='Scheme p14 answers under a heading in three sentences; "1 reason for each '
             'part", "Award 3 @ 5 Marks".',
         topic='eng-2-11',
         lifted=[S(14, 107, 712, 488, 772)], marks=[5], total=5,
         notes="The scheme prints '1 reason for each part Award 3 @ 5 Marks'."),
    dict(key=(6, 'b', None),
         why='Four lathe parts photographed and captioned (i)-(iv) with no words; scheme '
             'p15 names each after its roman, "Any three", "Identify Award 3 @ 5 Marks".',
         topic='eng-2-11',
         lifted=[[S(15, 88, 109, 165, 125), S(15, 88, 123, 153, 139),
                  S(15, 88, 138, 184, 154), S(15, 88, 153, 140, 169)]],
         row_kind='anyN', group=(3, 5), marks=[15], tariff='fixed', total=15,
         question_figure='engineering-2017-OL-paper-q6b-crop',
         notes="The scheme prints 'Any three: Identify Award 3 @ 5 Marks'."),
    dict(key=(6, 'c', 'i'), topic='eng-2-11', stem=False,
         why='Both (c)s price their (i) at 5 (scheme p15): the chuck\'s name, or what '
             'CAD/CAM stands for. One card for the printed OR, each branch a route.',
         question_lift=P(7, *_C6A, more=[(103, 488, 191, 504), _ORW6, _C6B,
                                         (103, 681, 308, 697)]),
         lifted=[S(15, 108, 226, 279, 242),
                 join(S(15, 102, 391, 384, 407), S(15, 175, 405, 242, 421))],
         marks=[5, 5], routes=['a', 'b'], total=5,
         question_figure='engineering-2017-OL-paper-q6c-crop',
         notes="The scheme prints 'Award 1 @ 5 Marks' for each (i). " + _OR6),
    dict(key=(6, 'c', 'ii'), topic='eng-2-11', stem=False,
         why='Both (c)s price their (ii) "Award 2 @ 3+2 Marks" (scheme p15): two other '
             'work-holding methods, or two advantages of CAD/CAM, each pair on one line '
             'and each lifted by its own word rectangle. One card, each branch a route.',
         question_lift=P(7, *_C6A, more=[(103, 510, 344, 541), _ORW6, _C6B,
                                         (103, 703, 381, 734)]),
         lifted=[S(15, 182, 240, 312, 256), S(15, 312, 240, 363, 256),
                 S(15, 177, 435, 282, 451), S(15, 283, 435, 407, 451)],
         marks=[3, 2, 3, 2], routes=['a', 'a', 'b', 'b'], total=5,
         question_figure='engineering-2017-OL-paper-q6c-crop',
         notes="The scheme prints 'Award 2 @ 3+2 Marks' for each (ii), each pair in the "
               "order the scheme names them. " + _OR6),
    dict(key=(6, 'c', 'iii'), topic='eng-2-11', stem=False,
         why='Both (c)s price their (iii) at 5 (scheme p15): one precaution for the chuck, '
             'or one for the CNC lathe. One card, each branch a route.',
         question_lift=P(7, *_C6A, more=[(103, 547, 349, 578), _ORW6, _C6B,
                                         (103, 740, 349, 770)]),
         lifted=[S(15, 226, 255, 377, 271),
                 join(S(15, 177, 480, 408, 496), S(15, 177, 494, 293, 510))],
         marks=[5, 5], routes=['a', 'b'], total=5,
         question_figure='engineering-2017-OL-paper-q6c-crop',
         notes="The scheme prints 'Award 1 @ 5 Marks' for each (iii). " + _OR6),
    # ---- Question 7 --------------------------------------------------------
    dict(key=(7, 'a', None),
         why='A lead-in over three terms set as romans, "any two"; scheme pp15-16 '
             'describe each under its name, "Description Award 2 @ 5 Marks".',
         topic='eng-3-12',
         lifted=[[join(S(15, 104, 627, 186, 643), S(15, 106, 641, 425, 674)),
                  join(S(15, 104, 687, 160, 703), S(15, 106, 702, 498, 753)),
                  join(S(16, 108, 50, 172, 66), S(16, 109, 65, 507, 95))]],
         row_kind='anyN', group=(2, 5), marks=[10], tariff='fixed', total=10,
         notes="The scheme prints 'Description Award 2 @ 5 Marks'."),
    dict(key=(7, 'b', None),
         why='The hole and shaft are drawn with their dimensions; scheme p16 answers each '
             'of (i)-(iv) on its own line after the ask, "Calculations/Name Award 4 @ 5 '
             'Marks". The reader stops at (b)\'s first sentence, so the question is lifted '
             'from the page with its four asks.',
         topic='eng-3-12',
         question_lift=P(8, 98, 180, 442, 196, more=[(98, 205, 385, 316)]),
         lifted=[S(16, 88, 133, 357, 149), S(16, 88, 148, 357, 164),
                 S(16, 87, 162, 356, 178), S(16, 87, 177, 192, 193)],
         marks=[5, 5, 5, 5], total=20,
         question_figure='engineering-2017-OL-paper-q7b-crop',
         notes="The scheme prints 'Calculations/Name Award 4 @ 5 Marks'."),
    dict(key=(7, 'c', None),
         why='Paper p8 sets two alternative (c)s either side of an OR. This card is the '
             'first branch, four instruments photographed and captioned (i)-(iv) with no '
             'words; scheme p16 names each with an application after its roman, "Any '
             'three", "Name & application Award 3 @ 5 Marks".',
         topic='eng-3-12', stem=False,
         lifted=[[S(16, 87, 255, 436, 271),
                  join(S(16, 87, 284, 431, 300), S(16, 212, 299, 278, 315)),
                  join(S(16, 87, 328, 438, 344), S(16, 193, 343, 381, 359)),
                  join(S(16, 87, 372, 457, 388), S(16, 187, 387, 306, 403))]],
         row_kind='anyN', group=(3, 5), marks=[15], tariff='fixed', total=15,
         question_figure='engineering-2017-OL-paper-q7c-crop',
         notes="The scheme prints 'Any three: Name & application Award 3 @ 5 Marks'. "
               + _OR7),
    dict(key=(7, 'c', 'i'),
         why='The OR branch\'s (i): scheme p16 names the four components after their '
             'letters on one line, each lifted by its own word rectangle; "Name Award 3 @ '
             '3 Marks".',
         topic='eng-2-16', stem=False,
         question_lift=P(8, 113, 638, 284, 669),
         lifted=[[S(16, 140, 502, 193, 518), S(16, 197, 502, 246, 518),
                  S(16, 251, 502, 347, 518), S(16, 351, 502, 400, 518)]],
         row_kind='anyN', group=(3, 3), marks=[9], tariff='fixed', total=9,
         # The (i) line sets each letter and name as one word ("A:Battery,"), so
         # each letter's key is the name that heads its line in (ii).
         labels={'A': S(16, 104, 531, 147, 547), 'B': S(16, 104, 546, 144, 562),
                 'C': S(16, 104, 560, 193, 576), 'D': S(16, 104, 575, 142, 591)},
         question_figure='engineering-2017-OL-paper-q7cor-crop',
         notes="The scheme prints 'Name Award 3 @ 3 Marks'. " + _OR7),
    dict(key=(7, 'c', 'ii'),
         why='The OR branch\'s (ii): scheme p16 gives each component\'s function on its own '
             'line; "Function Award 3 @ 2 Marks", for the three named.',
         topic='eng-2-16', stem=False,
         question_lift=P(8, 116, 682, 284, 713),
         lifted=[[S(16, 104, 531, 283, 547), S(16, 104, 546, 264, 562),
                  S(16, 104, 560, 405, 576), S(16, 104, 575, 436, 591)]],
         row_kind='anyN', group=(3, 2), marks=[6], tariff='fixed', total=6,
         question_figure='engineering-2017-OL-paper-q7cor-crop',
         notes="The scheme prints 'Function Award 3 @ 2 Marks'. " + _OR7),
]

_MAT = 'Materials: Properties and Uses'

ATLAS = {
    'eng-2017-ol-q2-b-i': dict(
        topics=[_MAT],
        note='Choosing a material for each part of the go-cart; the card\'s syllabus heading '
             'is Technology, as every Ordinary Q2 material-choice card\'s is.'),
    'eng-2017-ol-q2-b-ii': dict(
        topics=[_MAT],
        note='The reason for each material chosen in (b)(i); the card\'s syllabus heading is '
             'Technology, as every Ordinary Q2 material-choice card\'s is.'),
    'eng-2017-ol-q4-c-ii': dict(
        topics=['Machining & Metrology'],
        note='Drilling a tapping size hole before a thread is cut, a machining operation; the '
             'reference files Q4 under welding and safety only. The card\'s syllabus heading '
             'is Machining.'),
}
